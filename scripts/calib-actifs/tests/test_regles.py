"""Règles pures réimplémentées (Q-CA-13 ; E-CA-18) contre le fichier de vecteurs tests/vecteurs_regles.json, écrit à
la main et relu, hors du lot, par scripts/plan-s2bis/regles.py (jamais importé ici). Chaque test nomme sa mutation."""
import json
import os
import unittest
from fractions import Fraction

import socle

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "vecteurs_regles.json"), encoding="utf-8") as f:
    V = json.load(f)


def valeurs(v):
    return [Fraction(x) for x in v["valeurs"]] if "valeurs" in v else list(range(v["plage"][0], v["plage"][1] + 1))


class TestRegles(unittest.TestCase):
    def test_quantile(self):
        """T-CA-Q-1 : N = 1 000 : rang 999 ; N = 1 001 : rang 1 000 ; P99, P90, P50, doublons, rationnels non décimaux,
        N = 1, N = 0 (aucune valeur). Mutation M-CA-12 : rang par troncature."""
        for v in V["quantile"]:
            attendu = None if v["attendu"] is None else Fraction(v["attendu"])
            self.assertEqual(socle.quantile(valeurs(v), v["num"], v["den"]), attendu, v)

    def test_regle(self):
        """T-CA-G-1 : 1,5 × 0,00123 = 0,001845 donne 0,0020 ; 1,5 × 0,0002 donne 0,0005 sans drapeau ; borne basse
        exacte (1,5 × 1/3000 = 0,0005) sans drapeau ; 0 donne 0,0005 avec drapeau ; multiple exact 0,0045 ; 0,003 +
        1E-60 donne 0,0050 ; 1/3 % : 0,0035 (facteur 1), 0,0050 (facteur 1,5) ; 0,0280 donne 0,0280 ; 0,02801 et 0,0285
        : refus, valeur de la règle 0,0285. Mutations M-CA-13 : arrondi au plus proche ; M-CA-14 : borne haute incluse ;
        produit en Decimal arrondi."""
        for v in V["regle"]:
            x = None if v["x"] is None else sum(Fraction(y) for y in v["x"].split(" + "))
            tau, drapeau, valeur = socle.regle(v["facteur"], x, "0.0005", "0.0005", "0.0285")
            attendus = tuple(None if y is None else Fraction(y) for y in (v["tau"], v["valeur"]))
            self.assertEqual((tau, valeur), attendus, v)
            self.assertEqual(None if drapeau is None else drapeau[:len(v["drapeau"])].lower(),
                             None if v["drapeau"] is None else v["drapeau"].lower(), v)


if __name__ == "__main__":
    unittest.main()
