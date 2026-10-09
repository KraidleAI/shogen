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
import observateurs
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
            x = {"i": i, "jour": 0, "strates": {"calme": {"M": mc}, "stress": {"M": ms}}}
            return dict(x, impressions=imp) if imp else x
        v = {"longues": {"calme": {}, "stress": {}}, "absences": {}, "sauts": [], "initiale": None}
        a = dict(v, fenetres={"calme": 10, "stress": 4}, F={"BTC": {"calme": {"u": [1, 0]}, "stress": {"u": [0, 2]}}})
        b = dict(v, fenetres={"calme": 10, "stress": 4}, F={"BTC": {"calme": {"u": [2, 1]}, "stress": {"u": [0, 0]}}})
        recs = [rec(0, [1, 2, 3], [0, 1, 1], a), rec(1, [0, 0, 6], [2, 0, 0], b), rec(2, [4, 0, 0], [1, 1, 0])]
        self.assertEqual(executer.agreger_impressions(recs), {
            "M": {"calme": [5, 2, 9], "stress": [3, 2, 1]}, "impressions": 2,
            "F": {"BTC": {"calme": {"u": [F(3, 20), F(1, 20)]}, "stress": {"u": [F(0), F(1, 4)]}}},
            "longues": {"calme": {}, "stress": {}}, "absences": {}, "sauts": {"0": 2},
            "initiale": {"0": {"n": 2, "presentes": 0, "visible": {"calme": 0, "stress": 0}}}})
        self.assertEqual(executer.agreger_impressions(copy.deepcopy(recs[2:])),
                         {"M": {"calme": [4, 0, 0], "stress": [1, 1, 0]}, "impressions": 0})



def compte(segs, m, durees):
    """Recompte : segments qui ont au moins une fenêtre dans m, par longueur ; hors de `durees` : « autre »."""
    out = {}
    for a, b in segs:
        if any((m >> j) & 1 for j in range(a, b)):
            k = str(b - a) if b - a in durees else "autre"
            out[k] = out.get(k, 0) + 1
    return out


def cel(**k):
    c = copy.deepcopy(CEL)
    for cle, v in k.items():
        a, _p, b = cle.partition("__")
        c[a] = dict(c[a], **{b: v}) if b else v
    return c


class TestImpressionsN4N5N9(unittest.TestCase):
    def test_longues_n4(self):
        """N4 (f = 1, part 1/2, C0, W = 2), sans dérive puis sous tendances : chaque panne longue rejouée
        (executer.longues), vue dans les fenêtres d'une strate, est dans H(u) généré (sources.Replication.pannes) en
        entier, ou, sous dérive seulement, en dehors en entier (épisode aminci) ; au moins une gardée par cellule sur
        les réplications 0 à 11 ; enregistrement : nombres par durée (60, 1 440, 4 320, « autre » pour les tronqués),
        sommés sur les hôtes, égaux au recompte. Mutations M-11R-01 (flux d'un autre emplacement), M-11R-02 (part des
        pannes longues doublée), M-11R-03 (maximum de la dérive ignoré sur f·p), M-11R-04 (durées comptées hors de la
        strate), M-11R-14 (premier hôte seul)."""
        c4 = cel(f=[1, 1], longues=[1, 2], niveau="C0")
        for cx in (c4, dict(c4, derive=["tendances"])):
            gardees = 0
            for i in range(12):
                c, rep, m = refaite(cx, i, 2)
                r = executer.replication(P99, EP, cx, POINTS, 2, i)["impressions"]["longues"]
                for s in ("calme", "stress"):
                    att = {}
                    for h, _f in P99["calibration"]["unites"]:
                        segs, hh = executer.longues(c, rep, h, s), rep.pannes(h)
                        for a, b in segs:
                            x = (((1 << (b - a)) - 1) << a) & m[s]
                            self.assertIn(x & hh, (x, 0) if cx["derive"] else (x,), (i, s, h))
                            gardees += bool(x) and x & hh == x
                        for k, n in compte(segs, m[s], [60, 1440, 4320]).items():
                            att[k] = att.get(k, 0) + n
                    self.assertEqual(r[s], att, (i, s))
            self.assertGreater(gardees, 0, cx["derive"])

    def test_absences_n5(self):
        """N5 (grille « large », absences 1/20, W = 1, réplication 2) : absences D-1 rejouées (executer.absences) hors
        des validités de leur observateur (observateurs.Couche.validites) ; nombres par durée (5, 180, 4 320,
        « autre ») sommés sur les observateurs, égaux au recompte ; repli : aucune absence de l'observateur du repli.
        Mutations M-11R-05 (flux d'un autre observateur), M-11R-06 (part d'absence de la grille nominale), M-11R-07
        (repli ignoré)."""
        for cx in (cel(couche__grille="large"), cel(couche__grille="large", couche__repli=True)):
            c, rep, m = refaite(cx, 2)
            cou = observateurs.Couche(c["prm"], c["couche"], cx["nom"], 2, rep.horizon)
            val, att = cou.validites(), {}
            for o in range(P99["observateurs"]["M"]):
                segs = executer.absences(c, cou, o)
                self.assertEqual(sources.masque(segs) & val[o], 0, o)
                if cx["couche"]["repli"] and o == P99["observateurs"]["repli"]:
                    self.assertEqual(segs, [])
                for k, n in compte(segs, cou.grille, [5, 180, 4320]).items():
                    att[k] = att.get(k, 0) + n
            self.assertEqual(executer.replication(P99, EP, cx, POINTS, 1, 2)["impressions"]["absences"], att)
            self.assertGreater(sum(att.values()), 0)

    def test_sauts_et_initiale_n9(self):
        """N9 (dérive « sauts » et « initiale », W = 1) : sauts réalisés [hôte, hausse, instant] des dérives de la
        réplication (sources.Replication.derives, refaite) ; panne initiale : hôte et fenêtres visibles par strate,
        les 4 320 premières fenêtres de la grille dans les fenêtres de la strate (selon T_début) ; transitoire commun
        (genre « saut » sans saut) : aucun saut, aucune panne initiale. Mutations M-11R-08 (transitoire compté en
        saut), M-11R-09 (sens inversé), M-11R-10 (panne initiale visible sur la grille entière)."""
        for i in (0, 1, 2):
            c9 = cel(derive=["sauts", "initiale"])
            c, rep, m = refaite(c9, i)
            r = executer.replication(P99, EP, c9, POINTS, 1, i)["impressions"]
            d = rep.derives()
            self.assertEqual(r["sauts"], [[h, x[1] < x[2], x[3]] for h, x in d["specs"].items()])
            self.assertEqual(len(r["sauts"]), 3)
            h = d["initiale"]
            self.assertEqual(r["initiale"], h and {"hote": h, "visible": {s: (m[s] & ((1 << 4320) - 1)).bit_count()
                                                                       for s in ("calme", "stress")}})
        r = executer.replication(P99, EP, cel(derive=["transitoire"]), POINTS, 1, 0)["impressions"]
        self.assertEqual((r["sauts"], r["initiale"]), ([], None))

    def test_agreger_n4_n5_n9(self):
        """Trois enregistrements à impressions écrits à la main : distribution, par durée, du nombre de pannes longues
        par réplication et par strate (« 60 » : 0, 1, 2 fois une), d'absences par réplication ; nombre de sauts par
        réplication ; panne initiale par jour tiré : présences et fenêtres visibles sommées. Mutations M-11R-11
        (durée absente comptée à part au lieu de 0), M-11R-12 (visible d'une autre strate), M-11R-13 (jour ignoré)."""
        def rec(i, j, lg, ab, sauts, ini):
            return {"i": i, "jour": j, "strates": {"calme": {"M": [0]}, "stress": {"M": [0]}}, "impressions": {
                "fenetres": {"calme": 1, "stress": 1}, "F": {}, "longues": {"calme": lg, "stress": {}},
                "absences": ab, "sauts": sauts, "initiale": ini}}
        recs = [rec(0, 2, {"60": 1}, {"5": 2}, [["a", True, 7]], {"hote": "a", "visible": {"calme": 3, "stress": 4}}),
                rec(1, 2, {"60": 2, "autre": 1}, {}, [], None),
                rec(2, 5, {}, {"5": 2, "4320": 1}, [["a", False, 1], ["b", True, 2]],
                    {"hote": "b", "visible": {"calme": 0, "stress": 9}})]
        g = executer.agreger_impressions(recs)
        self.assertEqual(g["longues"], {"calme": {"60": {"0": 1, "1": 1, "2": 1}, "autre": {"0": 2, "1": 1}},
                                        "stress": {}})
        self.assertEqual(g["absences"], {"5": {"2": 2, "0": 1}, "4320": {"0": 2, "1": 1}})
        self.assertEqual(g["sauts"], {"1": 1, "0": 1, "2": 1})
        self.assertEqual(g["initiale"], {"2": {"n": 2, "presentes": 1, "visible": {"calme": 3, "stress": 4}},
                                         "5": {"n": 1, "presentes": 1, "visible": {"calme": 0, "stress": 9}}})

if __name__ == "__main__":
    unittest.main()
