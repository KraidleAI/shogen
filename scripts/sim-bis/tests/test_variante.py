"""Variante non enroulée SB-9 (E-S-33 ; Q-S-09 de la PROPOSITION, adoptée par l'AVIS ; T-VAR-1) : décalages calculés
hors code du lot (graine = sha256sum de « SHOGEN-SB9-VECTEURS » ; s = (entier de sha256sum de
« <graine>:<strate>:minus:<r>:<u> ») mod (2N + 1) − N, reste par bc en base 16, le module écrit lui aussi en base 16) ;
segment central et valeurs de K_H écrites à la main sur 3 unités de 12 fenêtres (n = 12, N = 3, segment [3, 9)) ; chaque
test nomme les mutations qui le rougissent."""
import unittest

import commun
import variante

PRM = commun.charger_parametres(environ={})
G = "89b463e5562e71fce3960b5b7ca4b1f060d5a4618c13444923e4fb69af7b5c68"
B, F, K = "binance", "bitfinex", "kraken"


def bits(*positions):
    return sum(1 << p for p in positions)


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


if __name__ == "__main__":
    unittest.main()
