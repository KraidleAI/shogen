"""Règle R1-2 répliquée, SB-7 et SB-8 (E-S-24 à E-S-35 ; T-ROT-1, T-ROT-2, T-REG-1 à T-REG-3, T-ABS-1) : décalages
calculés hors du code (`sha256sum`, puis `bc` en base 16, journal de la tranche 3 « vecteurs-t-rot-1.txt »), séries,
listes de K^(r) et décisions écrites à la main ; chaque test nomme les mutations qui le rougissent."""
import unittest

import aleas
import commun
import regle

PRM = commun.charger_parametres(environ={})
A = PRM["aleas"]
G = "26455ac198150c505226ead3117413190f3c1639660290a216bee811e157e0b2"   # printf … T-ROT-1|0 | sha256sum


def bits(*positions) -> int:
    m = 0
    for p in positions:
        m |= 1 << p
    return m


class TestRotation(unittest.TestCase):
    def refus(self, code, f, *a):
        with self.assertRaises(commun.Refus) as c:
            f(*a)
        self.assertEqual(c.exception.code, code)

    def test_decalages_t_rot_1(self):
        """T-ROT-1 : o(r, u) = entier big-endian des 32 octets de SHA-256 de « <graine>:<strate>:<r>:<u> » modulo n
        (E-S-27 ; AVIS-C Q-R-02) ; graine de règle de la réplication (T-ROT-1, 0) recalculée par sha256sum (E-S-41) ;
        cinq vecteurs par sha256sum et bc, dont o = 0 (gemini, n = 7) et o = n − 1 (bitstamp, n = 19). Graine non
        hexadécimale minuscule de 64 caractères : REGLE/graine ; « : » ou caractère hors ASCII imprimable dans la strate
        ou l'unité : REGLE/libelle ; r ou n nul : REGLE/entier. Mutations M-ROT-1 (classe dans l'entrée), M-7A-01 (huit
        premiers octets seulement), M-7A-02 (petit-boutiste), M-7A-03 (séparateur « | »), M-7A-04 (graine non
        contrôlée), M-7A-05 (libellés non contrôlés), M-7A-06 (r sur quatre chiffres)."""
        self.assertEqual(aleas.graine_regle(A, "T-ROT-1", 0), G)
        for s, r, u, n, o in (("calme", 1, "kraken", 109440, 38692), ("stress", 9999, "binance", 43776, 21459),
                              ("calme", 10, "okx", 24585, 4167), ("stress", 2, "gemini", 7, 0),
                              ("calme", 3, "bitstamp", 19, 18)):
            self.assertEqual(regle.decalage(G, s, r, u, n), o, (s, r, u))
        for code, a in (("REGLE/graine", (G.upper(), "calme", 1, "okx", 7)),
                        ("REGLE/graine", (G[1:], "calme", 1, "okx", 7)), ("REGLE/libelle", (G, "cal:me", 1, "okx", 7)),
                        ("REGLE/libelle", (G, "calme", 1, "okx" + chr(233), 7)),
                        ("REGLE/entier", (G, "calme", 0, "okx", 7)), ("REGLE/entier", (G, "calme", 1, "okx", 0))):
            self.refus(code, regle.decalage, *a)

    def test_sens_de_rotation(self):
        """Sens fixé (AVIS-C Q-R-02) : la valeur de la position t va en (t + o) mod n. n = 8 : positions 0, 1 décalées
        de 3 → 3, 4 ; positions 6, 7 → 1, 2 (enroulement) ; o = 0 : inchangé. Mutation M-ROT-4 : sens inversé."""
        self.assertEqual([regle.tourner(bits(0, 1), 3, 8), regle.tourner(bits(6, 7), 3, 8),
                          regle.tourner(bits(0, 2), 0, 8)], [bits(3, 4), bits(1, 2), bits(0, 2)])

    def test_k_et_s_t_rot_2(self):
        """T-ROT-2, à la main, trois unités sur 8 fenêtres : A = {0, 1, 4}, B = {1, 2, 4}, C = {4, 7} : m = 1, 2, 1, 0,
        3, 0, 0, 1 → K = 2 (fenêtres 1 et 4), S = C(2, 2) + C(3, 2) = 4. B décalée de 1 ({2, 3, 5}), C de 6 ({2, 5}) : K
        = 2 (2 et 5), S = 2. B de 7 ({0, 1, 3}), C de 1 ({0, 5}) : m = 3, 2, 0, 1, 1, 1 → K = 2 (0 et 1), S = 4. Puis 1
        000 essais aléatoires (2 à 10 unités, 1 à 64 fenêtres) : K et S égaux au comptage naïf position par position.
        Mutations M-ROT-5 (« au moins un »), M-ROT-6 (S sans le terme croisé des plans), M-7A-07 (coefficient d'un plan
        sans la division par 2)."""
        a, b, c = bits(0, 1, 4), bits(1, 2, 4), bits(4, 7)
        cas = [([a, b, c], bits(1, 4), 4), ([a, regle.tourner(b, 1, 8), regle.tourner(c, 6, 8)], bits(2, 5), 2),
               ([a, regle.tourner(b, 7, 8), regle.tourner(c, 1, 8)], bits(0, 1), 4)]
        for series, i, s in cas:
            self.assertEqual((regle.deux(series), regle.paires(series)), (i, s))
        for k in range(1000):
            u = aleas.flux(A, "T-ROT-2", k, "essai", 0)
            n, nu = 1 + int(64 * u()), 2 + int(9 * u())
            series = [sum(1 << t for t in range(n) if u() < 0.3) for _j in range(nu)]
            m = [sum(x >> t & 1 for x in series) for t in range(n)]
            self.assertEqual((regle.deux(series).bit_count(), regle.paires(series)),
                             (sum(1 for v in m if v >= 2), sum(v * (v - 1) // 2 for v in m)), k)
        with self.assertRaises(commun.Refus) as e:
            regle.paires([1] * 16)
        self.assertEqual(e.exception.code, "REGLE/plans")
        self.assertEqual(regle.paires([1] * 15), 105)
