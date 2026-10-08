"""Règles pures : quantile au rang le plus proche, grille et bornes de τ, règle de σ (ADR-0029 §2.6). Attendus
écrits à la main ; chaque test nomme la mutation qui le rougit."""
import unittest
from decimal import Decimal

import regles
from tests import fixtures  # noqa: F401  (harnais épinglé : contexte Decimal nommé)


class TestRegles(unittest.TestCase):
    def test_quantile_rang_le_plus_proche(self):
        """Rang ⌈num·N/den⌉ : sur 1..10, P99,9 et P99 au rang 10, P90 au rang 9, P50 au rang 5 ; sur 1..1000, P99,9 au
        rang 999 et P99 au rang 990. Mutation MR-1 : rang ⌊num·N/den⌋ (P99,9 de 1..10 rendu 9)."""
        q, dix, mille = regles.quantile, list(range(10, 0, -1)), list(range(1, 1001))
        self.assertEqual([q(dix, 999, 1000), q(dix, 99, 100), q(dix, 90, 100), q(dix, 50, 100)], [10, 10, 9, 5])
        self.assertEqual([q(mille, 999, 1000), q(mille, 99, 100), q([7], 999, 1000), q([], 99, 100)], [999, 990, 7, None])

    def test_regle_tau_grille_exacte_et_bornes(self):
        """(τ, drapeau, valeur de la règle), τ = grid-ceil(1,5·x, 0,0005) : 0,003 → 0,0045 (multiple exact) ; 0,003 +
        1E-60 → 0,0050 (le produit exact dépasse 0,0045 de 1,5E-60, sous les 50 chiffres du contexte) ; 0,00301 → 0,0050 ;
        0,0186 → 0,0280 sans drapeau ; 0,019 → 0,0285 ≥ borne haute exclue : REFUS nommé, aucun τ, valeur de la règle
        0,0285 (adjudication A-2) ; 0 → borne basse 0,0005. Mutation MR-2 : produit en Decimal sous le contexte ; MR-3 :
        borne haute incluse (0,0285 rendu) ; MR-5 : écrêtage au lieu du refus (0,0280 rendu)."""
        def t(x):
            return regles.regle_tau(Decimal("1.5"), x, Decimal("0.0005"), Decimal("0.0005"), Decimal("0.0285"))
        self.assertEqual(t(Decimal("0.003")), (Decimal("0.0045"), None, Decimal("0.0045")))
        self.assertEqual(t(Decimal("0.003" + "0" * 56 + "1"))[0], Decimal("0.0050"))     # 0,003 + 1E-60, exact
        self.assertEqual(t(Decimal("0.00301"))[0], Decimal("0.0050"))
        self.assertEqual(t(Decimal("0.0186")), (Decimal("0.0280"), None, Decimal("0.0280")))
        v, drapeau, regle = t(Decimal("0.019"))
        self.assertEqual((v, drapeau.startswith("REFUS"), regle), (None, True, Decimal("0.0285")))
        v, drapeau, regle = t(Decimal(0))
        self.assertEqual((v, drapeau.startswith("borne basse"), regle), (Decimal("0.0005"), True, Decimal(0)))
        self.assertEqual(t(None), (None, "aucune cellule", None))

    def test_regle_sigma(self):
        """σ = max(plancher, 3 × max des P99 des strates) : (5, 20) et 30 s → 60 ; (5, aucune) → 30 ; aucune → plancher
        et motif ; plancher None → None. Mutation MR-4 : P99 de la première strate seule (rendrait 30)."""
        s = regles.regle_sigma
        self.assertEqual(s(Decimal(3), [Decimal(5), Decimal(20)], 30), (Decimal(60), None))
        self.assertEqual(s(Decimal(3), [Decimal(5), None], 30), (Decimal(30), None))
        self.assertEqual(s(Decimal(3), [None, None], 300)[0], Decimal(300))
        self.assertTrue(s(Decimal(3), [None, None], 300)[1].startswith("aucune staleness"))
        self.assertEqual(s(Decimal(3), [Decimal(1)], None)[0], None)


if __name__ == "__main__":
    unittest.main()
