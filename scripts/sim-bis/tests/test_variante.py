"""Variante non enroulée SB-9 (E-S-33 ; Q-S-09 de la PROPOSITION, adoptée par l'AVIS ; T-VAR-1) : décalages calculés
hors code du lot (graine = sha256sum de « SHOGEN-SB9-VECTEURS » ; s = (entier de sha256sum de
« <graine>:<strate>:minus:<r>:<u> ») mod (2N + 1) − N, reste par bc en base 16, le module écrit lui aussi en base 16) ;
segment central et valeurs de K_H écrites à la main sur 3 unités de 12 fenêtres (n = 12, N = 3, segment [3, 9)) ; chaque
test nomme les mutations qui le rougissent."""
import unittest
from fractions import Fraction

import commun
import variante

PRM = commun.charger_parametres(environ={})
G = "89b463e5562e71fce3960b5b7ca4b1f060d5a4618c13444923e4fb69af7b5c68"
B, F, K = "binance", "bitfinex", "kraken"


def bits(*positions):
    return sum(1 << p for p in positions)


def petit():
    """parametres.json avec α = 1/5 : à R = 4, seuil (4 + 1)/5 − 1 = 0 (cas écrits à la main)."""
    return dict(PRM, regle=dict(PRM["regle"], alpha=[1, 5]))


SERIES = {B: bits(2, 5, 8), F: bits(1, 3, 6, 8), K: bits(1, 10)}


class Cas(unittest.TestCase):
    def refus(self, code, f, *a, **k):
        with self.assertRaises(commun.Refus) as c:
            f(*a, **k)
        self.assertEqual(c.exception.code, code)


class TestDecalages(Cas):
    def test_parametres(self):
        """Section « variante » : diviseur 4 (N = ⌊n/4⌋), sensibilité 8 (N = ⌊n/8⌋), source citée (E-S-33, Q-S-09) ;
        diviseur nul refusé au schéma. Mutations M-9-01 (diviseur 3), M-9-02 (sensibilité 4)."""
        v = PRM.get("variante", {})
        self.assertEqual((v.get("diviseur"), v.get("sensibilite")), (4, 8))
        self.assertTrue(all(x in v["source"] for x in ("E-S-33", "PROPOSITION l.187", "PROPOSITION l.522",
                                                         "AVIS.md l.43-50")))
        with self.assertRaises(commun.Refus) as c:
            commun.controler(dict(PRM, variante=dict(v, diviseur=0)), commun.SCHEMA)
        self.assertEqual(c.exception.code, "PARAMETRES/schema")

    def test_demi_et_segment(self):
        """N = ⌊n/4⌋ : 12 → 3, 15 → 3, 16 → 4, 3 → 0 ; sensibilité 40 → 5 ; segment [N, n − N) : n = 12, bits 3 à 8
        (504) ; n = 13, bits 3 à 9 (1 016) ; n = 3, N = 0, bits 0 à 2 (7) ; diviseur hors de la section :
        VARIANTE/diviseur. Mutations M-VAR-2 (segment [0, n − 2N)), M-9-03 (N = ⌈n/4⌉), M-9-04 (diviseur libre)."""
        self.assertEqual([variante.demi(n, 4, PRM) for n in (12, 15, 16, 3)], [3, 3, 4, 0])
        self.assertEqual((variante.demi(40, 4, PRM), variante.demi(40, 8, PRM)), (10, 5))
        self.assertEqual([variante.segment(n, N) for n, N in ((12, 3), (13, 3), (3, 0))], [504, 1016, 7])
        for d in (5, 0, "4", True):
            self.refus("VARIANTE/diviseur", variante.demi, 12, d, PRM)

    def test_decalages_sha256sum_bc(self):
        """s(r, u) pour n = 12 (N = 3, module 7) : r = 1 : bitfinex +2, kraken +2, binance +1 ; r = 2 : +2, −2, −1 ;
        r = 3 : +1, +2, −3 ; r = 4 : −2, 0, +1 ; en stress, N = 10 (module 21) : bitfinex +3 à r = 1, +2 à r = 9 999.
        Mutations M-9-05 (« minus » omis), M-9-06 (module 2N), M-9-07 (sans le − N), M-9-08 (strate omise), M-9-09
        (octets de queue)."""
        attendus = {1: (2, 2, 1), 2: (2, -2, -1), 3: (1, 2, -3), 4: (-2, 0, 1)}
        for r, s in attendus.items():
            self.assertEqual(tuple(variante.decalage(G, "calme", r, u, 3) for u in (F, K, B)), s, r)
        self.assertEqual([variante.decalage(G, "stress", r, F, 10) for r in (1, 9999)], [3, 2])

    def test_decaler_sans_enroulement(self):
        """x = 0, 5 et 11 sur 12 fenêtres, N = 3 : la valeur de la position t va en t + s, rien ne revient par le bord ;
        s = +3 : 3, 8 ; s = −3 : 8 ; s = 0 : 5 (segment [3, 9) seul). Mutations M-9-10 (sens inversé), M-VAR-1
        (rotation enroulée sur toute la suite)."""
        x = bits(0, 5, 11)
        self.assertEqual([variante.decaler(x, s, 12, 3) for s in (3, -3, 0)], [bits(3, 8), bits(8), bits(5)])

    def test_refus_decalage(self):
        """Refus nommés de la rotation enroulée, par regle._cle : graine, strate, nom d'unité ; r hors de 1..9 999.
        Mutation M-9-15 (contrôles de decalage retirés)."""
        self.refus("REGLE/graine", variante.decalage, G.upper(), "calme", 1, F, 3)
        self.refus("REGLE/libelle", variante.decalage, G, "nuit", 1, F, 3)
        self.refus("REGLE/libelle", variante.decalage, G, "calme", 1, "Bitfinex", 3)
        for r in (0, 10000, True):
            self.refus("REGLE/entier", variante.decalage, G, "calme", r, F, 3)



class TestVariante(Cas):
    def test_t_var_1(self):
        """T-VAR-1, R = 4, seuil 0 : binance 2 5 8 (non décalée), bitfinex 1 3 6 8, kraken 1 10. Segment [3, 9) :
        K_H^(0) = 1 (position 8), un run, deux unités à écart sur le segment (kraken n'en a aucun). r = 1 : bitfinex
        3 5 8 10, kraken 3 : K = 3 (3, 5, 8) ; r = 2 : 3 5 8 10 et 8 : K = 2 (5, 8) ; r = 3 : 2 4 7 9 et 3 : K = 0 ;
        r = 4 : 1 4 6 et 1 10 : K = 0. Complet : loi {0 : 2, 2 : 1, 3 : 1}, C = 2, C1 = 2, K_crit = 4, moyenne 5/4 ;
        NON ÉVALUABLE (« runs ») ; anticipé : arrêt à r = 1. Sensibilité (diviseur 8) : N = 1, segment [1, 11),
        K_H^(0) = 2 (1 et 8), deux runs. Mutations M-VAR-1 (enroulement sur toute la suite), M-VAR-2 (segment non
        central), M-9-10 (sens), M-9-11 (première unité décalée), M-9-12 (unités et runs comptés sur toute la suite),
        M-9-22 (diviseur passé ignoré)."""
        a, c = variante.deux_modes(SERIES, B, G, "calme", 12, 12, petit(), 4)
        self.assertEqual((c["K"], c["runs"], c["unites"], c["N"]), (1, 1, 2, 3))
        h = variante.tester(SERIES, B, G, "calme", 12, 12, petit(), 4, diviseur=8)
        self.assertEqual((h["N"], h["K"], h["runs"]), (1, 2, 2))
        self.assertEqual((c["loi"], c["C"], c["C1"], c["K_crit"], c["moyenne"]),
                         ([(0, 2), (2, 1), (3, 1)], 2, 2, 4, Fraction(5, 4)))
        self.assertEqual((c["valeur"], c["causes"], a["valeur"], a["causes"], a["r"], a["C"]),
                         ("NON ÉVALUABLE", ["runs"], "NON ÉVALUABLE", ["runs"], 1, 1))

    def test_rejette(self):
        """Binance 2 8 10, bitfinex 1 4, kraken 4 7 8 : K_H^(0) = 2 (4 et 8, deux runs), trois unités ; r = 1 à 4 :
        K = 1 (6), 1 (6), 0, 1 (8) ; C = 0 ≤ 0, C1 = 3 : REJETTE, sans arrêt (r = 4) ; K_crit = 2 ; tester rend la
        valeur anticipée. Mutation M-9-13 (séries non décalées dans les rotations : K^(r) = K, C = 4)."""
        s = {B: bits(2, 8, 10), F: bits(1, 4), K: bits(4, 7, 8)}
        a, c = variante.deux_modes(s, B, G, "calme", 12, 12, petit(), 4)
        self.assertEqual((a["valeur"], a["C"], a["C1"], a["r"], c["K_crit"], c["loi"], a["K"], a["unites"]),
                         ("REJETTE", 0, 3, 4, 2, [(0, 1), (1, 3)], 2, 3))
        self.assertEqual(variante.tester(s, B, G, "calme", 12, 12, petit(), 4), a)

    def test_premiere_unite(self):
        """Première unité absente (None, ou hors des séries) : binance décalée aussi (+1, −1, −3, +1) : r = 1 : binance
        3 6 9 : K = 1 (3) ; r = 2 : 1 4 7 : K = 1 (8) ; r = 3 : 2 5 : K = 0 ; r = 4 : 3 6 9 : K = 1 (6) ; loi
        {0 : 1, 1 : 3}. Mutation M-9-11 (première unité toujours la plus petite)."""
        for premier in (None, "coinbase"):
            c = variante.deux_modes(SERIES, premier, G, "calme", 12, 12, petit(), 4)[1]
            self.assertEqual((c["loi"], c["C"]), ([(0, 1), (1, 3)], 3), premier)

    def test_suite_courte_et_n_prime(self):
        """n = 3 : N = 0, segment entier, décalages nuls : K^(r) = K = 1 pour tout r, C = 4 ; n′ = 3 < n_s/2 pour
        n_s = 7 : cause « n_prime ». Cas de test_rejette : n_s = 24 (2·12 = 24) : REJETTE ; n_s = 25 : « n_prime » (la
        règle n′_s ≥ n_s/2 porte sur la suite, pas sur le segment de 6 positions). Mutations M-9-14 (n′_s comparé au
        segment), M-9-19 (« > » au lieu de « ≥ »)."""
        c = variante.deux_modes({B: bits(0, 1), F: bits(1)}, B, G, "calme", 3, 7, petit(), 4)[1]
        self.assertEqual((c["N"], c["K"], c["loi"], c["C"], c["causes"]), (0, 1, [(1, 4)], 4, ["runs", "n_prime"]))
        s = {B: bits(2, 8, 10), F: bits(1, 4), K: bits(4, 7, 8)}
        self.assertEqual([variante.tester(s, B, G, "calme", 12, n_s, petit(), 4)["causes"] for n_s in (24, 25)],
                         [[], ["n_prime"]])

    def test_serie_hors_segment(self):
        """Une série nulle sur le segment peut y entrer par décalage : binance 3, bitfinex 1 (hors de [3, 9)) : une
        seule unité à écart sur le segment, mais r = 1 et 2 portent bitfinex en 3 : K = 1, 1, 0, 0, C1 = 2 ; causes
        « unites » et « runs », pas « k_crit ». Mutation M-9-21 (raccourci K^(r) = 0 décidé sur les unités du
        segment)."""
        c = variante.deux_modes({B: bits(3), F: bits(1)}, B, G, "calme", 12, 12, petit(), 4)[1]
        self.assertEqual((c["unites"], c["loi"], c["C1"], c["causes"]), (1, [(0, 2), (1, 2)], 2, ["unites", "runs"]))

    def test_refus(self):
        """Mêmes refus nommés que la rotation enroulée (regle._controler), avant tout calcul : graine, strate, nom
        d'unité, unité non décalée, masque hors de [0, 2^n) ; diviseur hors de la section. Mutation M-9-16 (contrôles
        des entrées de tester retirés)."""
        p = petit()
        self.refus("REGLE/graine", variante.tester, SERIES, B, G.upper(), "calme", 12, 12, p, 4)
        self.refus("REGLE/libelle", variante.tester, SERIES, B, G, "nuit", 12, 12, p, 4)
        self.refus("REGLE/libelle", variante.tester, {"Binance": 1}, None, G, "calme", 12, 12, p, 4)
        self.refus("REGLE/libelle", variante.tester, SERIES, "x:y", G, "calme", 12, 12, p, 4)
        self.refus("REGLE/masque", variante.tester, {B: 1 << 12}, B, G, "calme", 12, 12, p, 4)
        self.refus("VARIANTE/diviseur", variante.tester, SERIES, B, G, "calme", 12, 12, p, 4, diviseur=6)

if __name__ == "__main__":
    unittest.main()
