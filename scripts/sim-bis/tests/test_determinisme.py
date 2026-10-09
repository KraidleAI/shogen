"""Identité bit à bit SB-11h (T-DET-1 ; E-S-42, E-S-44, E-S-45 ; P-9) : trois cellules réduites (W = 1, R = 99) dont
une exerce un retrait (bascule P-abs à p_w = 3/5, type panne : 2·ok < n_s), calculées par lots dans des processus
neufs : une en un processus sous PYTHONHASHSEED 0, une en quatre processus sous PYTHONHASHSEED 1, une en deux
processus et deux lots ; fichiers égaux à l'octet, agrégats et empreintes égaux quel que soit le découpage."""
import copy
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from fractions import Fraction

import calibration
import commun
import executer

ICI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRM = commun.charger_parametres(environ={})
P99 = dict(PRM, regle=dict(PRM["regle"], R=99))
EP = calibration.charger(PRM, environ={})["episodes"]
F, K = Fraction, 6
POINTS = {"C1": {"calme": (F(1, 100), F(5), 60), "stress": (F(1, 50), F(10), 240)}}
BASE = {"nom": "D-1", "niveau": "C1", "f": [3, 10], "longues": [0, 1], "autres": [1, 1], "hors_enveloppe": [1, 4000],
        "derive": None, "incidents": None, "faibles": None,
        "couche": {"grille": "nominale", "repli": False, "chemin": {"mode": "reference", "facteur": [1, 1]},
                   "local": None, "artefacts": None, "regionale": [0, 1], "manque": [0, 1]},
        "regle": {"R": 99, "classes": ["BTC", "ETH", "USDC", "USDT"], "S": False, "variante": [], "evenements": 0,
                  "absorption": False},
        "surcharges": {}}


def cellules() -> list:
    """D-1 (N1 réduite), D-2 (incidents à ρ = 1/2 par jour, chacun des 7 hôtes AS13335 à 7/10, C0), D-3 (bascule :
    une unité faible à 3/5, L = 1, panne)."""
    c2, c3 = copy.deepcopy(BASE), copy.deepcopy(BASE)
    c2.update(nom="D-2", niveau="C0", incidents={"rho": [1, 2], "duree": 20, "geometrique": False, "mode": "chacun",
                                                 "population": "as13335", "p": [7, 10]})
    c3.update(nom="D-3", faibles={"k": 1, "p": [3, 5], "L": 1, "type": "panne"})
    return [BASE, c2, c3]


def lancer(dossier: str, processus: int, plages: list) -> None:
    """Calcul des trois cellules par lots (executer.calculer_lot), relecture (executer.lire_lots), agrégat écrit
    (executer.ecrire_agrege) ; appelé dans un processus neuf par le test."""
    lus = {}
    commun.charger_parametres(lus=lus, environ={})
    calibration.charger(PRM, lus, environ={})
    entete = commun.entete(lus)
    for c in cellules():
        for a, b in plages:
            executer.calculer_lot(P99, EP, c, POINTS, 1, (a, b), processus, dossier, entete)
        executer.ecrire_agrege(dossier, c["nom"], executer.agreger(P99["calibration"],
                                                                    executer.lire_lots(dossier, c["nom"], K, entete)),
                               entete)


def octets(dossier: str) -> dict:
    out = {}
    for f in sorted(os.listdir(dossier)):
        with open(os.path.join(dossier, f), "rb") as g:
            out[f] = g.read()
    return out


class TestDeterminisme(unittest.TestCase):
    def test_calculer_lot(self):
        """E-S-45 : lot (D-1, [2, 4)) en ce processus : enregistrements des réplications 2 et 3, égaux à
        executer.replication de mêmes arguments (JSON) ; sha256 rendu = celui du fichier. Mutations M-11I-04 (points
        d'E1 perdus), M-11I-05 (W différent), M-11I-06 (cellule d'un autre nom)."""
        d = tempfile.mkdtemp(dir=os.environ.get("TMPDIR"))
        self.addCleanup(shutil.rmtree, d)
        c, h = executer.calculer_lot(P99, EP, BASE, POINTS, 1, (2, 4), 1, d, ["e"])
        self.assertEqual(os.path.basename(c), "D-1.000002-000004.lot")
        with open(c, "rb") as f:
            lot = json.loads(f.read().split(commun.NL.encode(), 1)[1])
        attendu = [executer.jsonable(executer.replication(P99, EP, BASE, POINTS, 1, i)) for i in (2, 3)]
        self.assertEqual(lot["enregistrements"], attendu)
        with open(c, "rb") as f:
            self.assertEqual(hashlib.sha256(f.read()).hexdigest(), h)

    def executer(self, graine: str, processus: int, plages: list) -> dict:
        d = tempfile.mkdtemp(dir=os.environ.get("TMPDIR"))
        self.addCleanup(shutil.rmtree, d)
        env = {k: v for k, v in os.environ.items() if k != commun.VARIABLE}
        env["PYTHONHASHSEED"] = graine
        drap = (["-X", "dev"] if sys.flags.dev_mode else []) + [f"-W{w}" for w in sys.warnoptions]
        code = ("import json, sys; import tests.test_determinisme as t; t.lancer(sys.argv[1], int(sys.argv[2]), "
                "json.loads(sys.argv[3]))")
        p = subprocess.run([sys.executable, "-B", *drap, "-c", code, d, str(processus), json.dumps(plages)], cwd=ICI,
                           env=env, capture_output=True, timeout=240)
        self.assertEqual((p.returncode, p.stderr.decode("utf-8", "replace")[-300:]), (0, ""))
        return octets(d)

    def test_t_det_1(self):
        """T-DET-1 (E-S-44) : un processus et PYTHONHASHSEED 0, contre quatre processus et PYTHONHASHSEED 1 : mêmes
        fichiers de lot et d'agrégat, octet pour octet ; deux processus et lots [0, 2) et [2, 6) : mêmes agrégats
        (empreinte des six enregistrements comprise) ; D-3 exerce un retrait « presque mort » de son unité faible
        (P-9) ; empreinte de l'agrégat de D-3 = celle de ses enregistrements relus, dans l'ordre. Mutations M-DET-1
        (graine dérivée de l'indice de tâche), M-DET-2 (itération sur un ensemble), M-11H-01 (enregistrements du lot
        dans l'ordre d'achèvement), M-11H-09 (empreinte à rebours)."""
        a = self.executer("0", 1, [[0, K]])
        b = self.executer("1", 4, [[0, K]])
        c = self.executer("0", 2, [[0, 2], [2, K]])
        self.assertEqual(sorted(a), sorted(b))
        self.assertEqual([f for f in a if a[f] != b[f]], [])
        ag = {f: x for f, x in a.items() if f.endswith(".agrege.json")}
        self.assertEqual((len(ag), {f: c.get(f) for f in ag} == ag), (3, True))
        lots = [json.loads(x.split(commun.NL.encode(), 1)[1]) for f, x in sorted(a.items())
                if f.startswith("D-3.") and f.endswith(".lot")]
        recs = [e for x in lots for e in x["enregistrements"]]
        self.assertEqual(json.loads(a["D-3.agrege.json"])["empreinte"], executer.empreinte(recs))
        retraits = [r for e in recs for s in e["strates"].values() for r in s["retraits"]["BTC"]]
        self.assertIn(["bitfinex", "presque mort"], retraits)


if __name__ == "__main__":
    unittest.main()
