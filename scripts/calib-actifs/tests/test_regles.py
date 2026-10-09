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


if __name__ == "__main__":
    unittest.main()
