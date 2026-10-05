"""Calibration SB-2 (E-S-37, E-S-02 ; T-CAL-1) : EP l.13, l.14, l.140 et l.144 recopiées à la main, nombres pris en
`Fraction` depuis leur écriture décimale ; une retouche par contrôle de forme et de cohérence ; chaque test nomme les
mutations qui le rougissent. Contrôle hors code : `bc` donne 372/24585 = 0,0151311775472849298352654057352043929225137
278828553… et 372/332 = 1,12048192771084337349397590361445783132530120481927710…, dont les 50 chiffres significatifs
arrondis au plus proche sont les valeurs imprimées par EP l.13."""
import unittest
from fractions import Fraction

import calibration
import commun

NL = chr(10)
PRM = commun.charger_parametres(environ={})
EP = commun.lire_entree(PRM, "episodes", environ={}).decode("utf-8")


def retouche(numero: int, avant: str, apres: str) -> str:
    """EP avec, à la ligne `numero` (1 = première), l'unique occurrence de `avant` remplacée par `apres`."""
    lignes = EP.split(NL)
    assert lignes[numero - 1].count(avant) == 1, (numero, avant)
    lignes[numero - 1] = lignes[numero - 1].replace(avant, apres)
    return NL.join(lignes)


class TestCalibration(unittest.TestCase):
    def refus(self, code, texte):
        with self.assertRaises(commun.Refus) as c:
            calibration.analyser(texte, PRM["calibration"])
        self.assertEqual(c.exception.code, code)

    def test_lecture_t_cal_1(self):
        """EP l.13 et l.14 ; 40 lignes d'épisodes (2 strates × 10 unités × 2 types). Mutations M-CAL-1 (censurés
        ajoutés aux complets), M-2-03 (nombre décimal lu en flottant)."""
        c = calibration.charger(PRM, environ={})
        self.assertEqual(c["episodes"]["calme", "binance", "panne"], {
            "n_s": 24585, "cellules": 372, "episodes": 332, "censures": 51, "complets": 281, "max": 5,
            "taux": Fraction("0.015131177547284929835265405735204392922513727882855"),
            "moyenne": Fraction("1.1204819277108433734939759036144578313253012048193"), "quantiles": [1, 1, 3],
            "moyenne_complets": Fraction("1.1209964412811387900355871886120996441281138790036"),
            "histogramme": [(1, 301), (2, 24), (3, 6), (5, 1)]})
        self.assertEqual(len(c["episodes"]), 40)

    def test_parametres_et_epingles(self):
        """Section « calibration » ; EP sous une épingle fausse : refus du socle. Mutation M-2-04 : EP lu sans
        commun.lire_entree."""
        k = PRM["calibration"]
        self.assertEqual((k["strates"], k["types"], k["pools"], k["quantiles"], k["garde_blocs"], k["precision"]),
                         (["calme", "stress"], ["panne", "ecart"], ["S2 (D1)", "D1-bis"], [50, 90, 99], 30, 50))
        self.assertEqual([h for h, _f in k["unites"]], ["binance", "bitfinex", "bitstamp", "chainlink", "coinbase",
                                                        "coingecko", "defillama", "gemini", "kraken", "okx"])
        faux = dict(PRM, entrees=dict(PRM["entrees"], episodes=dict(PRM["entrees"]["episodes"], sha256="0" * 64)))
        with self.assertRaises(commun.Refus) as c:
            calibration.charger(faux, environ={})
        self.assertEqual(c.exception.code, "ENTREE/sha256-parametres")

    def test_refus_de_forme(self):
        """Première ligne, type hors d'ordre, exposant, ligne d'histogramme ôtée, ligne en trop, saut final ôté, valeur
        « - », virgule décimale : CALIB/forme. Mutations M-2-05 (nombre de lignes non contrôlé), M-2-06 (identité de
        ligne non contrôlée), M-2-07 (première ligne non contrôlée)."""
        h14 = "    histogramme (longueur×nombre) : 1×301 2×24 3×6 5×1" + NL
        for t in (retouche(1, "S2-bis", "S2bis"), retouche(17, ") panne", ") ecart"),
                  retouche(13, "P99 = 3", "P99 = 3E0"), EP.replace(h14, "", 1), EP + "x" + NL, EP[:-1],
                  retouche(25, "moyenne = 1.15 ;", "moyenne = - ;"), retouche(65, "taux = 0.0", "taux = 0,0")):
            self.refus("CALIB/forme", t)

    def test_refus_de_coherence(self):
        """Une retouche par contrôle, qui ne rougit que lui : taux ≠ cellules/n_s (E-S-37), moyenne, complets ≠
        épisodes − censurés, maximum, somme des nombres, somme des longueurs, ordre des longueurs, quantile, n_s = 0
        (quotient impossible) : CALIB/coherence. Mutations M-2-08 à M-2-16, un contrôle retiré chacune ; M-2-33
        (nombre nul admis)."""
        for t in (retouche(13, "727882855 ;", "727882856 ;"), retouche(13, "2048193 ;", "2048194 ;"),
                  retouche(13, "censurés 51", "censurés 52"), retouche(13, "max = 5", "max = 6"),
                  retouche(14, "1×301 2×24", "1×303 2×23"), retouche(14, "1×301 2×24", "1×302 2×23"),
                  retouche(14, "3×6 5×1", "5×1 3×6"), retouche(14, "3×6 5×1", "3×6 4×0 5×1"),
                  retouche(13, "P99 = 3", "P99 = 2"),
                  retouche(13, "n_s = 24585 ;", "n_s = 0 ;")):
            self.refus("CALIB/coherence", t)
