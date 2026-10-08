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
    def refus(self, code, texte, k=None):
        """Refus nommé `code` exigé ; toute autre exception échoue en la nommant par son type (O-1, R-12 de la G2)."""
        try:
            calibration.analyser(texte, k or PRM["calibration"])
        except Exception as e:
            self.assertEqual(getattr(e, "code", type(e).__name__), code)
        else:
            self.fail(f"{code} attendu, aucun refus")

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

    def test_lecture_fiv_t_cal_1(self):
        """EP l.140 (D1-bis, calme, ℓ = 240, garde tenue) et l.144 (ℓ = 1440, garde non tenue) ; 4 courbes de 17 points.
        Mutation M-CAL-2 : garde ignorée (lue tenue partout)."""
        d = calibration.charger(PRM, environ={})["fiv"]
        self.assertEqual(d["D1-bis", "calme"][12], {
            "ell": 240, "n": 24585, "K": 148, "fiv": Fraction("22.875107619499139688158815002722346438402490494255"),
            "sigma2": Fraction("3365.1353559023660984670112023097760840941942530323"),
            "gamma0": Fraction("147.10905023388244864754931869025828757372381533455"),
            "cv": Fraction("0.11408797792643129814123654880491384644099142081780"), "garde": True})
        self.assertEqual((d["D1-bis", "calme"][16]["ell"], d["D1-bis", "calme"][16]["garde"]), (1440, False))
        self.assertEqual([(cle, len(v)) for cle, v in d.items()],
                         [(("S2 (D1)", "calme"), 17), (("S2 (D1)", "stress"), 17), (("D1-bis", "calme"), 17),
                          (("D1-bis", "stress"), 17)])

    def test_refus_fiv(self):
        """ℓ hors grille : CALIB/forme ; FIV ≠ σ̂²/γ̂₀, γ̂₀ ≠ (nK − K²)/n (σ̂² et γ̂₀ retouchés ensemble à ℓ = 1,
        FIV = 1 tenu), garde ≠ (n ≥ 30ℓ), cv ≠ √(4ℓ/3n) : CALIB/coherence. Mutations M-2-17 à M-2-20, un contrôle
        retiré chacune."""
        self.refus("CALIB/forme", retouche(161, "ℓ = 1440", "ℓ = 1441"))
        g = "147.10905023388244864754931869025828757372381533455"
        for t in (retouche(140, "494255 ;", "494256 ;"),
                  retouche(128, f"σ̂²_bloc = {g} ; γ̂₀ = {g}", "σ̂²_bloc = 2 ; γ̂₀ = 2"),
                  retouche(140, "garde : tenue", "garde : non tenue"), retouche(140, "4099142081780", "4099142081781")):
            self.refus("CALIB/coherence", t)

    def test_quotient_indefini_nomme(self):
        """C-5 de la G2 (R-12) : EP l.13 « n_s = 0 ; cellules = 0 » : 0/0 lève InvalidOperation, qui n'est pas une
        ZeroDivisionError ; rendu CALIB/coherence. Mutation R-12 : seules les divisions par zéro nommées."""
        self.refus("CALIB/coherence", retouche(13, "n_s = 24585 ; cellules = 372 ;", "n_s = 0 ; cellules = 0 ;"))

    def test_longueur_repetee_refusee(self):
        """C-5 de la G2 (R-13) : EP l.14 « 1×301 » écrit « 1×300 1×1 » (332 épisodes, 372 cellules, maximum et
        quantiles inchangés, `bc`) : longueurs non strictement croissantes, CALIB/coherence. Mutation R-13 :
        « sorted(lg) » au lieu de « sorted(set(lg)) »."""
        self.refus("CALIB/coherence", retouche(14, "1×301", "1×300 1×1"))

    def test_quantile_au_dela_de_100(self):
        """O-1 de la G2 : un quantile au-delà de 100 n'a pas de rang (P101 : rang 336 > 332 épisodes, `bc`) : refus
        nommé CALIB/coherence, et non StopIteration. Mutation : next sans valeur par défaut."""
        k = dict(PRM["calibration"], quantiles=[50, 90, 101])
        self.refus("CALIB/coherence", EP.replace("P99 = ", "P101 = "), k)
