"""intervalles.py : épisodes, pauses complètes et de bord, épisodes complets, contrôle (e). Attendus écrits à la main
(rang ⌈num·N/den⌉) ; chaque test nomme la mutation qui le rougit."""
import os
import unittest

import intervalles
import tests
from tests.test_masque_fiv import NL, fixture_fiv, lire

W = 60
EP = tests.MODS["episodes"]
QS = [[50, 100], [90, 100], [99, 100]]


def serie(vrais, absentes=(), n=10):
    """Fenêtres [(ws, {« a » : classe}, {})] aux positions 0 à n − 1 hors absentes ; « x » si vraie, « y » sinon."""
    return [(tests.fx.VEN + W * i, {"a": "x" if i in vrais else "y"}, {}) for i in range(n) if i not in absentes]


def entree(fen):
    return intervalles.entree(intervalles.serie(fen, "a"), W, "x".__eq__, EP)


class TestIntervalles(unittest.TestCase):
    def test_episodes(self):
        """T-P2-EPI-1. Positions 0 à 9, la 5 absente, vrai en 0, 1, 2, 4, 6, 7, 9 : (3, censuré à gauche), (1, à
        droite), (2, à gauche), (1, à droite) (PS2 tests/test_episodes.py l.19-24) ; deux segments. Mutation M-P2-14 :
        positions renumérotées par le lot."""
        e = entree(serie((0, 1, 2, 4, 6, 7, 9), (5,)))
        self.assertEqual((e["episodes"], len(e["segments"])),
                         ([(3, True, False), (1, False, True), (2, True, False), (1, False, True)], 2))

    def test_pauses(self):
        """T-P2-INT-1. Segment [0 ; 11] vrai en 2, 3 et 7 ; lacune en 12 ; segment [13 ; 16] sans épisode : pause
        complète 3 (4 à 6) ; pauses de bord 2 (0-1), 4 (8-11), 4 (13-16), dont un segment sans épisode. Mutation
        M-P2-16 : pause de bord comptée complète ; M-P2R3-1 : segment sans épisode non distingué."""
        e = entree(serie((2, 3, 7), (12,), 17))
        bord = [(2, True, False), (4, False, True), (4, True, True)]
        self.assertEqual((e["completes"], e["bord"], e["vides"]), ([(3, False, False)], bord, [(4, True, True)]))

    def test_resume_et_complets(self):
        """T-P2-INT-2 et T-P2-EPI-3. Pauses complètes 1, 2, 2, 7 et une de bord de 30 : compte 4, moyenne 3, max 7,
        P50 = 2 (rang 2), P90 = P99 = 7 (rang 4), bord 1, 30×1 ; épisodes : un censuré, quatre complets de longueur 1 :
        histogramme des complets 1×4. Mutation M-P2-18 : statistiques sur toutes les pauses (moyenne 42/5, max 30) ;
        M-P2-34 : épisode censuré compté complet."""
        f = [(1, False, False), (2, False, False), (2, False, False), (7, False, False)]
        e = {"segments": [(47, True, True)], "episodes": [(1, True, False)] + [(1, False, False)] * 4, "completes": f,
             "bord": [(30, False, True)], "vides": []}
        lignes = intervalles.lignes("« calme » a (hôte ua) ecart", e, 47, QS, EP.resume, tests.MODS["commun"].dec)
        self.assertEqual(lignes, [
            "  « calme » a (hôte ua) ecart : pauses complètes = 4 ; segments = 1 ; épisodes = 5 (complets 4) ; "
            "moyenne = 3 ; max = 7 ; P50 = 2 ; P90 = 7 ; P99 = 7 ; pauses de bord = 1 (dont segments sans épisode 0)",
            "    histogramme des pauses (longueur×nombre) : 1×1 2×2 7×1",
            "    histogramme des pauses de bord (longueur observée×nombre) : 30×1",
            "    histogramme des épisodes complets (longueur×nombre) : 1×4"])

    def test_contre_ep(self):
        """T-P2-EPI-2. Fixture de FIV, EP produit par episodes.main épinglé : (e) égal, code 0 ; entrées « a ecart »
        (épisodes 2, 1, 1, 1 tous censurés ; pauses complètes 2 et 2) et « c ecart » (deux segments sans épisode, 5
        et 4) écrites à la main ; EP altéré d'un chiffre, ou portant une entrée de plus (deux lignes) : P2/ep, code 1,
        aucune valeur (lettre de (e) : EP l.13-92, chaîne pour chaîne). Mutation M-P2-15 : contrôle (e) neutralisé ;
        M-P2R3-2 : complets pris aux pauses ; G-21 (G2) : compte des lignes d'épisodes retiré ; M-P2R3-4 : seules les
        lignes manquantes refusées ; M-P2R3-5 : une entrée en trop admise."""
        argv, s = fixture_fiv(self)
        self.assertEqual(intervalles.main(argv), 0)
        lignes = lire(s, "intervalles.txt")
        for entree_, attendu in (("a (hôte ua) ecart", ["pauses complètes = 2 ; segments = 2 ; épisodes = 4 (complets "
                                 "0) ; moyenne = 2 ; max = 2 ; P50 = 2 ; P90 = 2 ; P99 = 2 ; pauses de bord = 0 (dont "
                                 "segments sans épisode 0)", "2×2", "aucune pause de bord", "aucun épisode complet"]),
                                 ("c (hôte uc) ecart", ["pauses complètes = 0 ; segments = 2 ; épisodes = 0 (complets "
                                 "0) ; moyenne = - ; max = - ; P50 = - ; P90 = - ; P99 = - ; pauses de bord = 2 (dont "
                                 "segments sans épisode 2)", "aucune pause", "4×1 5×1", "aucun épisode complet"])):
            self.assertIn(f"  « calme » {entree_} : {attendu[0]}", lignes)
            i = lignes.index(f"  « calme » {entree_} : {attendu[0]}")
            self.assertEqual([x.split(" : ", 1)[1] for x in lignes[i + 1:i + 4]], attendu[1:])
        a = "  « calme » b (hôte ub) panne : n_s = 9 ; cellules = 1 ; épisodes = 1, dont censurés 1 ;"

        def alterer(texte):
            self.assertIn(a, texte)
            return texte.replace(a, a.replace("dont censurés 1", "dont censurés 0"))

        def de_plus(texte):
            x = [y for y in texte.split(NL) if y.startswith(("  « ", "    histogramme (longueur×nombre) : "))]
            return texte + NL.join(x[-2:]) + NL
        for f in (alterer, de_plus):
            argv, s = fixture_fiv(self, f)
            self.assertEqual(intervalles.main(argv), 1)
            lignes = lire(s, "intervalles.txt")
            self.assertEqual((lignes[-2].split(" : ")[0], [x[:1] for x in lignes].count("[")), ("REFUS P2/ep", 0))
            self.assertEqual(os.listdir(s), ["intervalles.txt"])
