"""Impressions des cellules (SB-11q ; SHOGEN-SIM-BIS-SB11-IMPRESSIONS-1 ; avis Q-T2-4 de la tranche 2 ; ADR-0029
l.97 a) : référence = la réplication refaite ici depuis les modules du moteur (forme de tests/test_replication.py),
identités exactes entre composantes rejouées et état généré, ou comptes écrits à la main ; chaque test nomme les
mutations qui le rougissent."""
import copy
import unittest
from fractions import Fraction

import aleas
import calendrier
import calibration
import commun
import executer
import sources

PRM = commun.charger_parametres(environ={})
P99 = dict(PRM, regle=dict(PRM["regle"], R=99))
EP = calibration.charger(PRM, environ={})["episodes"]
F = Fraction
POINTS = {"C1": {"calme": (F(1, 100), F(5), 60), "stress": (F(1, 50), F(10), 240)}}
CEL = {"nom": "T-imp", "niveau": "C1", "f": [3, 10], "longues": [0, 1], "autres": [2, 1], "hors_enveloppe": [1, 4000],
       "derive": None, "incidents": None, "faibles": None,
       "couche": {"grille": "nominale", "repli": False, "chemin": {"mode": "reference", "facteur": [1, 1]},
                  "local": None, "artefacts": None, "regionale": [0, 1], "manque": [0, 1]},
       "regle": {"R": 99, "classes": ["BTC"], "S": False, "variante": [], "evenements": 0, "absorption": False},
       "surcharges": {}}


def refaite(cel, i, W=1):
    """Cellule (executer.cellule), T_début (flux « debut » d'indice 0), masques de strate et sources.Replication de la
    réplication i, refaits ici."""
    c, cal = executer.cellule(P99, EP, cel, POINTS, W), P99["calendrier"]
    e = calendrier.echelle(cal, W)
    debut = calendrier.t_debut(cal, aleas.flux(P99["aleas"], cel["nom"], i, "debut", 0))
    m = calendrier.masques(cal, debut, e["t_max"])
    return c, sources.Replication(c["prm"], EP, c["fond"], cel["nom"], i, m, e["t_max"]), m


class TestImpressionsF(unittest.TestCase):
    def test_f_propre_et_hors_enveloppe(self):
        """Avis Q-T2-4 : pour chaque (classe, strate, hôte servi), F séparé en propre et hors-enveloppe (f_separe) :
        leur union égale F(hôte, classe) généré (sources.Replication.ecarts) dans les fenêtres de la strate ;
        enregistrement de la réplication 0 : [fenêtres propres, fenêtres hors-enveloppe] et fenêtres de chaque strate,
        égaux aux comptes de la réplication refaite ; hors-enveloppe exercé (au moins une fenêtre) ; réplication 200,
        hors du sous-ensemble pré-déclaré : aucune impression. Mutations M-11Q-01 (emplacement du flux propre),
        M-11Q-02 (emplacement du flux hors-enveloppe), M-11Q-03 (τ doublé), M-11Q-04 (multiplicateur hors de BTC
        ignoré), M-11Q-05 (f ignoré), M-11Q-06 (composantes hors des fenêtres de la strate), M-11Q-07 (sous-ensemble
        à i ≤ 200), M-11Q-08 (fenêtres de l'autre strate), M-11Q-12 (loi « panne » pour le propre), M-11Q-13 (pool
        de BTC pour toutes les classes)."""
        c, rep, m = refaite(CEL, 0)
        r = executer.replication(P99, EP, CEL, POINTS, 1, 0)["impressions"]
        self.assertEqual(r["fenetres"], {s: m[s].bit_count() for s in ("calme", "stress")})
        hors, att = 0, {}
        for k, (cl, pool) in enumerate(sources.classes(P99)):
            for s in ("calme", "stress"):
                for h in pool:
                    pr, ho = executer.f_separe(c, rep, h, k, s)
                    self.assertEqual(pr | ho, rep.ecarts(h, k) & m[s], (cl, s, h))
                    att.setdefault(cl, {}).setdefault(s, {})[h] = [pr.bit_count(), ho.bit_count()]
                    hors += ho.bit_count()
        self.assertEqual(r["F"], att)
        self.assertGreater(hors, 0)
        self.assertNotIn("impressions", executer.replication(P99, EP, CEL, POINTS, 1, 200))


class TestAgregerImpressions(unittest.TestCase):
    def test_comptes_exacts(self):
        """Trois enregistrements écrits à la main, le dernier hors du sous-ensemble (sans impressions) : M_j sommé sur
        les trois, par strate ; taux effectifs exacts sur les deux premiers : propre (1 + 2)/(10 + 10) = 3/20 et
        hors-enveloppe 1/20 en calme, 0 et 2/(4 + 4) = 1/4 en stress ; sans impression : comptes seuls. Mutations
        M-11Q-09 (fenêtres du premier enregistrement seul), M-11Q-10 (M_j des seuls enregistrements à impressions),
        M-11Q-11 (propre et hors-enveloppe permutés)."""
        def rec(i, mc, ms, imp=None):
            x = {"i": i, "strates": {"calme": {"M": mc}, "stress": {"M": ms}}}
            return dict(x, impressions=imp) if imp else x
        a = {"fenetres": {"calme": 10, "stress": 4}, "F": {"BTC": {"calme": {"u": [1, 0]}, "stress": {"u": [0, 2]}}}}
        b = {"fenetres": {"calme": 10, "stress": 4}, "F": {"BTC": {"calme": {"u": [2, 1]}, "stress": {"u": [0, 0]}}}}
        recs = [rec(0, [1, 2, 3], [0, 1, 1], a), rec(1, [0, 0, 6], [2, 0, 0], b), rec(2, [4, 0, 0], [1, 1, 0])]
        self.assertEqual(executer.agreger_impressions(recs), {
            "M": {"calme": [5, 2, 9], "stress": [3, 2, 1]}, "impressions": 2,
            "F": {"BTC": {"calme": {"u": [F(3, 20), F(1, 20)]}, "stress": {"u": [F(0), F(1, 4)]}}}})
        self.assertEqual(executer.agreger_impressions(copy.deepcopy(recs[2:])),
                         {"M": {"calme": [4, 0, 0], "stress": [1, 1, 0]}, "impressions": 0})


if __name__ == "__main__":
    unittest.main()
