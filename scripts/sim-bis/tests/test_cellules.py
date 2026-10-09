"""Cellules SB-11d (SHOGEN-SIM-BIS-SB11-BRIEF-1, L-2 et O-5) : attendus écrits à la main depuis la PROPOSITION, l'AVIS
et EP ; chaque test nomme les mutations qui le rougissent."""
import copy
import unittest
from fractions import Fraction

import calibration
import commun
import executer

PRM = commun.charger_parametres(environ={})
EP = calibration.charger(PRM, environ={})["episodes"]
F = Fraction
N1 = {"nom": "N1", "niveau": "C1", "f": [3, 10], "longues": [0, 1], "autres": [1, 1], "hors_enveloppe": [1, 4000],
      "derive": None, "incidents": None, "faibles": None,
      "couche": {"grille": "nominale", "repli": False, "chemin": {"mode": "reference", "facteur": [1, 1]},
                 "local": None, "artefacts": None, "regionale": [0, 1], "manque": [0, 1]},
      "regle": {"R": 9999, "classes": ["BTC", "ETH", "USDC", "USDT"], "S": False, "variante": [], "evenements": 0,
                "absorption": False},
      "surcharges": {}}


def cel(**k):
    """N1 retouchée : clés de premier niveau, ou « couche.x », « regle.x », remplacées."""
    c = copy.deepcopy(N1)
    for cle, v in k.items():
        a, _p, b = cle.partition("__")
        if b:
            c[a][b] = v
        else:
            c[a] = v
    return c



class TestCellules(unittest.TestCase):
    def test_couches_o_5(self):
        """O-5 de la G2 de la tranche 3 : grille de la couche d'observateurs portée par les cellules, dans
        parametres.json (cellules.couches), recopiée de Q-S-11 (a) (PROPOSITION l.537-538) et de l'AVIS (l.54, point
        large) : nominale 1/200, 1/200, paires 1/30 par jour, sans perte ; dégradée 1/50, 1/50, paires 1/7, perte ;
        large 1/20, 1/20, paires 1/7, perte, défaut local 1/1 000, artefacts 1/20 par jour ; source citée. Mutations
        M-11D-01 (grille dégradée à 1/100), M-11D-02 (perte nominale)."""
        g = PRM.get("cellules", {}).get("couches")
        z = [0, 1]
        self.assertEqual(g, {
            "nominale": {"absences": [1, 200], "degradations": [1, 200], "paires": [1, 30], "perte": False, "local": z,
                         "artefacts": z},
            "degradee": {"absences": [1, 50], "degradations": [1, 50], "paires": [1, 7], "perte": True, "local": z,
                         "artefacts": z},
            "large": {"absences": [1, 20], "degradations": [1, 20], "paires": [1, 7], "perte": True,
                      "local": [1, 1000], "artefacts": [1, 20]}})
        s = PRM.get("cellules", {}).get("source", "")
        self.assertTrue(all(x in s for x in ("PROPOSITION l.537-538", "AVIS.md l.54", "O-5")), s[:80])

    def test_couche_l_2(self):
        """L-2 (SB11-BRIEF-1) : la perte est tirée sur le W de la cellule, celui passé à calendrier.echelle (16), jamais
        sur T_max en semaines (24) ; nominale : aucune perte. Chemin de référence (1 − f)·p̂ : binance calme 7/10 ×
        372/24 585 ; facteur 1/10 : 7/100 × 372/24 585 ; fixe 3/10 000 partout. Surcharges de la cellule : repli,
        défaut local, artefacts, régionales, manques. Mutations M-11D-03 (T_max au lieu de W), M-11D-04 (chemin à f
        au lieu de 1 − f), M-11D-05 (grille ignorée), M-11D-06 (facteur ignoré)."""
        c = executer.couche(PRM, EP, cel(couche__grille="degradee"), 16)
        self.assertEqual((c["perte"], c["absences"], c["degradations"], c["paires"], c["repli"]),
                         (16, F(1, 50), F(1, 50), F(1, 7), False))
        self.assertEqual(c["chemin"]["binance", "calme"], F(7, 10) * F(372, 24585))
        self.assertIsNone(executer.couche(PRM, EP, N1, 16)["perte"])
        c = executer.couche(PRM, EP, cel(couche__chemin={"mode": "reference", "facteur": [1, 10]}), 16)
        self.assertEqual(c["chemin"]["binance", "calme"], F(7, 100) * F(372, 24585))
        c = executer.couche(PRM, EP, cel(couche__chemin={"mode": "fixe", "epsilon": [3, 10000]}, couche__repli=True,
                                         couche__local=[1, 1000], couche__artefacts=[1, 20],
                                         couche__regionale=[1, 5], couche__manque=[1, 4]), 16)
        self.assertEqual(set(c["chemin"].values()), {F(3, 10000)})
        self.assertEqual((c["repli"], c["local"], c["artefacts"], c["regionale"], c["manque"]),
                         (True, F(1, 1000), F(1, 20), F(1, 5), F(1, 4)))


if __name__ == "__main__":
    unittest.main()
