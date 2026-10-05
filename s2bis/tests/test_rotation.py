"""RB-6 : loi de rotation de R1-2 (E-R-16 à E-R-18 ; AVIS Q-R-02). Vecteurs de o(r, u) calculés hors du code :
`printf '%s' "<graine>:<strate>:<r>:<u>" | sha256sum`, puis entier big-endian et modulo par `bc` (journal G1 de RB-6a,
script vecteurs_rb6.sh) ; masques décalés écrits à la main. Mutant obligatoire « modulo n_s au lieu de n′_s »
(PROPOSITION §3.4) : dû au sous-lot RB-7, où n_s et n′_s coexistent ; ce module ne reçoit que n (Q-RB-14 de la G2 de
RB-T1 ; ROTATION-S2BIS.md §7)."""
import hashlib
import os
import random
import subprocess
import sys
import unittest
from fractions import Fraction

from shogen_s2bis.recalc import rotation as rot

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

G = "6fce4df75bac7db6ff01817b407f6331e49ec2ebf31f02e6672d3ab8a3bc9688"      # sha256 de « SHOGEN-RB6-VECTEURS »


class Decalage(unittest.TestCase):
    def test_vecteurs_calcules_hors_du_code(self):
        for strate, r, u, n, o in (("calme", 1, "api.binance.com", 109440, 107527),          # sha256 d7916cde…5a07
                                   ("stress", 9999, "ethereum-rpc.publicnode.com", 43776, 24225),   # d4930a57…fba1
                                   ("calme", 4242, "api.kraken.com", 54720, 39743),          # e8e92c3a…4b7f
                                   ("calme", 1, "api.coinbase.com", 7, 0),                   # o = 0 ; c6c0e4bc…c1a0
                                   ("calme", 7, "api.coinbase.com", 7, 6),                   # o = n − 1 ; 55a70a48…d47e
                                   ("calme", 1, "api.binance.com", 54720, 52807)):           # n′ = n/2, même entrée
            with self.subTest(strate=strate, r=r, u=u, n=n):
                self.assertEqual(rot.decalage(G, strate, r, u, n), o)

    def test_refus_nommes(self):
        g = ("calme", 1, "a", 7)
        for code, args in (("ROTATION/graine", (G.upper(), *g)), ("ROTATION/graine", (G + "0", *g)),
                           ("ROTATION/graine", (G[1:], *g)), ("ROTATION/graine", (bytes.fromhex(G), *g)),
                           ("ROTATION/strate", (G, "Calme", 1, "a", 7)), ("ROTATION/strate", (G, "crise", 1, "a", 7)),
                           ("ROTATION/n", (G, "calme", 1, "a", 0)), ("ROTATION/n", (G, "calme", 1, "a", True)),
                           ("ROTATION/r", (G, "calme", 0, "a", 7)), ("ROTATION/r", (G, "calme", 10000, "a", 7)),
                           ("ROTATION/r", (G, "calme", True, "a", 7)), ("ROTATION/r", (G, "calme", "01", "a", 7)),
                           ("ROTATION/unite", (G, "calme", 1, "a:4", 7)), ("ROTATION/unite", (G, "calme", 1, "", 7)),
                           ("ROTATION/unite", (G, "calme", 1, "é", 7)), ("ROTATION/unite", (G, "calme", 1, "a\x7f", 7)),
                           ("ROTATION/unite", (G, "calme", 1, "a\tb", 7))):
            with self.subTest(code=code, args=args):
                with self.assertRaises(rot.RefusRotation) as e:
                    rot.decalage(*args)
                self.assertEqual(e.exception.code, code)
        for u in (" !", "~", "A", "api.Kraken.com", "a b", "a_b", "a" * 254):            # Q-RB-13 : nom d'hôte
            with self.subTest(u=u):
                with self.assertRaises(rot.RefusRotation) as e:
                    rot.decalage(G, "calme", 1, u, 7)
                self.assertEqual(e.exception.code, "ROTATION/unite")
        self.assertEqual([rot.decalage(G, "calme", 9999, u, 1) for u in ("-", ".", "0", "z", "a" * 253)], [0] * 5)


class Tourner(unittest.TestCase):
    def test_sens_du_decalage_a_la_main(self):              # la valeur de la position t va en (t + o) mod n
        for m, o, n, attendu in ((0b1001001, 2, 7, 0b0100110),       # {0, 3, 6} + 2 -> {2, 5, 1}
                                 (0b1001001, 6, 7, 0b1100100),       # {0, 3, 6} + 6 -> {6, 2, 5}
                                 (0b1001001, 0, 7, 0b1001001), (0b10000, 1, 5, 0b00001), (0b1, 3, 5, 0b01000),
                                 (0b11111, 4, 5, 0b11111), (0, 3, 5, 0), (1, 0, 1, 1)):
            self.assertEqual(rot.tourner(m, o, n), attendu, (bin(m), o, n))


def naif(graine, strate, n, classes, premiere, R):
    """(K, S) position par position pour r = 0 (sans décalage) à R, par classe : o(r, u) recalculé ici (hashlib et
    int(…, 16)), la valeur de la position t portée en (t + o) mod n ; code indépendant du module."""
    sortie = {}
    for c in sorted(classes):
        K, S = [], []
        for r in range(R + 1):
            compte = [0] * n
            for u, bits in classes[c].items():
                o = 0 if r == 0 or u == premiere else int(hashlib.sha256(
                    f"{graine}:{strate}:{r}:{u}".encode()).hexdigest(), 16) % n
                for t in range(n):
                    compte[(t + o) % n] += bits >> t & 1
            K.append(sum(x >= 2 for x in compte))
            S.append(sum(x * (x - 1) // 2 for x in compte))
        sortie[c] = (K, S)
    return sortie


class Lois(unittest.TestCase):
    def test_masques_egaux_au_comptage_naif_classes_jointes_par_hote(self):
        alea = random.Random(20261005)
        for essai in range(24):
            n, strate = alea.randint(1, 24), ("calme", "stress")[essai % 2]
            btc = {u: alea.getrandbits(n) & alea.getrandbits(n) for u in ("a.b", "a.c", "api.okx.com", "e.f", "z")
                   if alea.random() < 0.8}
            eth = {u: alea.getrandbits(n) for u in sorted(btc) if alea.random() < 0.7}
            premiere = (min(btc) if btc else None, "a.b", None)[essai % 3]
            loi, ref = rot.lois(G, strate, n, {"ETH": eth, "BTC": btc}, premiere, 40, 3), naif(G, strate, n, {
                "ETH": eth, "BTC": btc}, premiere, 40)
            self.assertEqual(list(loi), ["BTC", "ETH"])
            for c, (K, S) in ref.items():
                with self.subTest(essai=essai, classe=c):
                    for x, nom, compte in ((K, "K", "C"), (S, "S", "C_S")):
                        crit = next(k for k in range(max(x) + 2) if sum(v >= k for v in x[1:]) <= 3)   # définition
                        cles = (nom, nom + "_r", compte, nom + "_crit", nom + "_moyen")
                        self.assertEqual([loi[c][cle] for cle in cles],
                                         [x[0], x[1:], sum(v >= x[0] for v in x[1:]), crit, Fraction(sum(x[1:]), 40)])

    def test_R_9999_jusqu_a_la_derniere_rotation(self):
        classes = {"BTC": {"a": 0b00011, "b": 0b00110, "c": 0b01100}}
        loi, (K, S) = rot.lois(G, "stress", 5, classes, "a", 9999, 99)["BTC"], naif(G, "stress", 5, classes, "a",
                                                                                    9999)["BTC"]
        self.assertEqual((len(loi["K_r"]), loi["K_r"] == K[1:], loi["S_r"] == S[1:]), (9999, True, True))   # sans diff

    def test_resume_a_la_main(self):                         # C compte les égalités (>=) ; K_crit : seuil 99 exact
        self.assertEqual(rot.resume(5, [3, 5, 5, 2, 7, 5, 1, 0, 4, 5], 2), (5, 6, Fraction(37, 10)))
        self.assertEqual(rot.resume(10, [0] * 9900 + [10] * 99, 99), (99, 1, Fraction(990, 9999)))
        self.assertEqual(rot.resume(10, [0] * 9899 + [10] * 100, 99), (100, 11, Fraction(1000, 9999)))
        self.assertEqual(rot.resume(0, [0] * 50, 99), (50, 0, 0))

    def test_refus_nommes(self):
        bon = {"BTC": {"a": 1}}
        for code, args in (("ROTATION/R", (G, "calme", 3, bon, None, 0, 0)), ("ROTATION/R", (G, "calme", 3, bon, None,
                                                                                            10000, 99)),
                           ("ROTATION/R", (G, "calme", 3, bon, None, 9999, -1)),
                           ("ROTATION/classes", (G, "calme", 3, [bon], None, 9, 0)),
                           ("ROTATION/classes", (G, "calme", 3, {1: {"a": 1}}, None, 9, 0)),
                           ("ROTATION/unite", (G, "calme", 3, {"BTC": {"a:b": 1}}, None, 9, 0)),
                           ("ROTATION/unite", (G, "calme", 3, bon, "", 9, 0)),
                           ("ROTATION/unite", (G, "calme", 3, {"BTC": {"A": 1}}, None, 9, 0)),
                           ("ROTATION/masque", (G, "calme", 3, {"BTC": {"a": 8}}, None, 9, 0)),
                           ("ROTATION/masque", (G, "calme", 3, {"BTC": {"a": -1}}, None, 9, 0)),
                           ("ROTATION/masque", (G, "calme", 3, {"BTC": {"a": True}}, None, 9, 0)),
                           ("ROTATION/graine", ("0" * 63, "calme", 3, bon, None, 9, 0)),
                           ("ROTATION/strate", (G, "poolee", 3, bon, None, 9, 0)), ("ROTATION/n", (G, "calme", 0, bon,
                                                                                                 None, 9, 0))):
            with self.subTest(code=code):
                with self.assertRaises(rot.RefusRotation) as e:
                    rot.lois(*args)
                self.assertEqual(e.exception.code, code)

    def test_memes_octets_sous_cinq_graines_de_hachage(self):
        code = (f"from shogen_s2bis.recalc import rotation as r\nprint(r.lois('{G}', 'calme', 9, {{'ETH': {{'b': 5, "
                "'a': 3}, 'BTC': {'c': 7, 'a': 9, 'b': 1}}, None, 30, 2))")
        sorties = {subprocess.run([sys.executable, "-B", "-c", code], cwd=RACINE, capture_output=True, timeout=60,
                                  env={**os.environ, "PYTHONHASHSEED": str(g)}).stdout for g in range(5)}
        self.assertEqual((len(sorties), next(iter(sorties))[:7]), (1, b"{'BTC':"))
