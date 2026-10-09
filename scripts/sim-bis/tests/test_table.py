"""Table des cellules (SB-11s ; PROPOSITION §5.1 l.282-301 et §5.2 l.314-321 ; AVIS Q-S-21 ; ajout daté du G0 du
2026-10-05 15:05:43 UTC, point (5)) : table du §5.1 recopiée ici à la main, ligne par ligne, depuis la PROPOSITION ;
cellules du §5.2 écrites ici depuis leurs lignes ; chaque test nomme les mutations qui le rougissent."""
import copy
import unittest
from fractions import Fraction

import calibration
import commun
import executer

PRM = commun.charger_parametres(environ={})
EP = calibration.charger(PRM, environ={})["episodes"]
F = Fraction
POINTS = {n: {"calme": (F(1, 100), F(5), 60), "stress": (F(1, 50), F(10), 240)} for n in ("C1", "C2")}
TOUTES = ["BTC", "ETH", "USDC", "USDT"]


def n1(**k):
    """Référence N1 du §5.1 (l.276-277 : f = 0,3, fond d'EP, C1, couche nominale, ε = (1 − f)·p̂, ni défaut local, ni
    artefact, ni dérive ; hors-enveloppe 2,5·10⁻⁴ par fenêtre, Q-S-21 (a) adoptée), règle à R = 9 999, BTC et ETH
    (séquence familiale du §4 pt 4), retouchée par k (« couche__x », « regle__x »)."""
    c = {"nom": "N1", "niveau": "C1", "f": [3, 10], "longues": [0, 1], "autres": [1, 1], "hors_enveloppe": [1, 4000],
         "derive": None, "incidents": None, "faibles": None,
         "couche": {"grille": "nominale", "repli": False, "chemin": {"mode": "reference", "facteur": [1, 1]},
                    "local": None, "artefacts": None, "regionale": [0, 1], "manque": [0, 1]},
         "regle": {"R": 9999, "classes": ["BTC", "ETH"], "S": False, "variante": [], "evenements": 0,
                   "absorption": False}, "surcharges": {}}
    for cle, v in k.items():
        a, _p, b = cle.partition("__")
        if b:
            c[a] = dict(c[a], **{b: v})
        else:
            c[a] = v
    return c


V = [4, 8]
ATTENDU = [n1(nom="N0", f=[1, 1], niveau="C0", couche__chemin={"mode": "fixe", "epsilon": [1, 10000]}),
           n1(regle__classes=TOUTES, regle__S=True, regle__variante=V),
           n1(nom="N1-tau0", hors_enveloppe=[0, 1]),
           n1(nom="N2", niveau="C0"),
           n1(nom="N3", niveau="C2", regle__variante=V),
           n1(nom="N4", longues=[1, 2], regle__variante=V),
           n1(nom="N5", couche__grille="degradee"),
           n1(nom="N6", couche__local=[1, 1000]),
           n1(nom="N7", couche__regionale=[1, 5], couche__manque=[1, 5]),
           n1(nom="N8", derive=["tendances"], regle__variante=V),
           n1(nom="N9", derive=["sauts", "initiale"], regle__variante=V),
           n1(nom="N10", f=[1, 10]),
           n1(nom="N11", faibles={"k": 2, "p": [2, 5], "L": 1, "type": "ecart"}, regle__absorption=True),
           n1(nom="N12", couche__repli=True),
           n1(nom="X1", derive=["commune"], regle__variante=V),
           n1(nom="X2", derive=["transitoire"]),
           n1(nom="X3", couche__artefacts=[1, 20])]


class TestTable(unittest.TestCase):
    def test_table_5_1(self):
        """Les 17 cellules nulles de parametres.json (cellules.nulles), dans l'ordre du §5.1, N1 à τ = 0 après N1
        (AVIS Q-S-21 : « la cellule N1 à 0 doit être imprimée à côté »), égales à la table recopiée ici ; variante sur
        N1, N3, N4, N8, N9, X1 et F3 sur N1 (l.301) ; chacune passe le schéma fermé et ses refus nommés
        (executer.cellule, W = 16). Mutations M-11S-01 à M-11S-06 (une valeur de la table changée), M-11S-07 (ordre
        des cellules), M-11S-08 (schéma des cellules sans nom admis)."""
        t = PRM["cellules"].get("nulles", [])
        self.assertEqual([c["nom"] for c in t], [c["nom"] for c in ATTENDU])
        for c, a in zip(t, ATTENDU):
            self.assertEqual(c, a, a["nom"])
            self.assertEqual(executer.cellule(PRM, EP, c, POINTS, 16)["nom"], a["nom"])
        mauvais = dict(PRM, cellules=dict(PRM["cellules"], nulles=[{"niveau": "C0"}]))
        with self.assertRaises(commun.Refus) as r:
            commun.controler(mauvais, commun.SCHEMA)
        self.assertEqual(r.exception.code, "PARAMETRES/schema")

    def test_cellules_5_2_exprimables(self):
        """Une cellule de chaque famille du §5.2 s'écrit dans le même schéma et passe ses refus (même mécanique) :
        P-cible (incident tous les 10 jours de strate, 20 fenêtres, chacun des 7 hôtes AS13335 avec probabilité 0,7,
        §3 pt 1) aux trois niveaux (point (5)) ; P-ETH, P-F3 (classes) ; P-grille aux coins (ρ = 1/2, D = 60, les 10,
        f = 1 ; ρ = 1/20, D = 5, 2 hôtes parmi AS13335, f = 3/10) ; P-abs : paire, triplet et impliquant l'unité
        faible (k = 4, p_w = 2/5, L_w = 20, critère collectif), bascule p_w = 0 et 3/5 ; P-év (g sur les 2 000
        premières). Mutation M-11S-09 (imposés « faibles » refusés)."""
        cible = {"mode": "chacun", "rho": [1, 10], "duree": 20, "geometrique": False, "population": "as13335",
                 "p": [7, 10]}
        fa = {"k": 4, "p": [2, 5], "L": 20, "type": "ecart"}
        cs = [n1(nom=f"P-cible-{n}", niveau=n, incidents=cible) for n in ("C0", "C1", "C2")]
        cs += [n1(nom="P-ETH", incidents=cible), n1(nom="P-F3", incidents=cible, regle__classes=TOUTES),
               n1(nom="P-g-max", f=[1, 1], incidents=dict(cible, rho=[1, 2], duree=60, population="pool", p=[1, 1]),
                  regle__R=999),
               n1(nom="P-g-min", incidents={"mode": "parmi", "rho": [1, 20], "duree": 5, "geometrique": False,
                                            "population": "as13335", "k": 2, "imposes": "aucun"}, regle__R=999),
               n1(nom="P-ev", incidents=cible, regle__evenements=2000)]
        for k, imp in ((2, "aucun"), (3, "aucun"), (2, "faibles")):
            cs.append(n1(nom=f"P-abs-{k}-{imp}", faibles=fa, regle__R=999, regle__absorption=True,
                         incidents={"mode": "parmi", "rho": [1, 10], "duree": 20, "geometrique": False,
                                    "population": "as13335", "k": k, "imposes": imp}))
        cs += [n1(nom=f"P-bascule-{p}", faibles={"k": 1, "p": [p, 10], "L": 1, "type": "panne"}, regle__R=999)
               for p in (0, 6)]
        for c in cs:
            self.assertEqual(executer.cellule(PRM, EP, copy.deepcopy(c), POINTS, 16)["nom"], c["nom"])


if __name__ == "__main__":
    unittest.main()
