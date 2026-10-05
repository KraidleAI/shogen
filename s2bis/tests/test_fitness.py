"""CB-0, E-C-01, E-C-41 : fonctions de fitness G4 du paquet. Frontière d'imports lue par analyse syntaxique ; mêmes
octets sous cinq graines de hachage ; compilation avec les avertissements en erreur (Q-G-05 de l'AVIS du G0)."""
import ast
import os
import subprocess
import sys
import unittest
import warnings

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Sous-paquet de shogen_s2bis → préfixes admis hors bibliothèque standard (PROPOSITION §1 pt 2). Un sous-paquet absent
# de la table est refusé ; les imports dynamiques aussi : la frontière ne se lirait plus. RB-0a : `recalc` seul admis.
REGLES = {"": (), "collecte": ("shogen_s2bis.collecte",), "recalc": ("shogen_s2bis.recalc",)}
DYNAMIQUES = {"importlib", "imp", "runpy", "pkgutil", "zipimport", "__import__"}


def violations(paquet, source):
    """Imports hors règle d'un module du paquet pointé `paquet` (« shogen_s2bis.collecte » pour collecte/x.py)."""
    p = paquet.split(".")
    admis = REGLES.get(p[1] if len(p) > 1 else "")
    if admis is None:
        return [f"{paquet} : sous-paquet sans règle"]
    cibles = []
    for n in ast.walk(ast.parse(source)):
        if isinstance(n, ast.Import):
            cibles += [a.name for a in n.names]
        elif isinstance(n, ast.ImportFrom):
            cibles.append(".".join((p[:len(p) + 1 - n.level] if n.level else []) + ([n.module] if n.module else [])))
        elif isinstance(n, ast.Name) and n.id == "__import__":
            cibles.append("__import__")
    return [f"{paquet} : {t}" for t in cibles if t.split(".")[0] in DYNAMIQUES or not (
        t.split(".")[0] in sys.stdlib_module_names or any(t == a or t.startswith(a + ".") for a in admis))]


def modules():
    """(paquet pointé, nom, octets) de chaque fichier .py de shogen_s2bis."""
    for d, _s, noms in sorted(os.walk(os.path.join(RACINE, "shogen_s2bis"))):
        for nom in sorted(x for x in noms if x.endswith(".py")):
            with open(os.path.join(d, nom), "rb") as f:
                yield os.path.relpath(d, RACINE).replace(os.sep, "."), nom, f.read()


class Fitness(unittest.TestCase):
    def test_frontiere_du_paquet(self):
        for module in (("shogen_s2bis.collecte", "config.py"), ("shogen_s2bis.recalc", "config_analyse.py")):
            self.assertIn(module, [(p, n) for p, n, _o in modules()])
        self.assertEqual([x for p, _n, o in modules() for x in violations(p, o)], [])

    def test_frontiere_refuse(self):
        c = "shogen_s2bis.collecte"
        for source, attendu in (("import shogen_s2", ["shogen_s2"]), ("from .. import recalc", ["shogen_s2bis"]),
                                ("from shogen_s2.window import w", ["shogen_s2.window"]),
                                ("import importlib.util", ["importlib.util"]), ("__import__('json')", ["__import__"]),
                                ("import json\nfrom . import x\nfrom .y import z", [])):
            self.assertEqual(violations(c, source), [f"{c} : {t}" for t in attendu], source)
        self.assertEqual(violations("shogen_s2bis.autre", ""), ["shogen_s2bis.autre : sous-paquet sans règle"])
        r = "shogen_s2bis.recalc"                               # recalc : ni collecte (hors décodeurs), ni S2
        for source, cible in (("from ..collecte import config", "shogen_s2bis.collecte"),
                              ("from shogen_s2.r1 import classify_ecart", "shogen_s2.r1")):
            self.assertEqual(violations(r, source), [f"{r} : {cible}"], source)
        self.assertEqual(violations(r, "from . import rotation\nfrom .lecteur import Lecteur\nimport hashlib"), [])

    def test_memes_octets_sous_cinq_graines(self):
        code = ("from shogen_s2bis.collecte import config as c\ntry: c.controler({'a': 1, 'zz': 2, 'yy': 3, 'xx': 4},"
                " {'a': (int, 0, 9)})\nexcept c.RefusConfig as e: print(e)")
        sorties = {subprocess.run([sys.executable, "-B", "-c", code], cwd=RACINE, capture_output=True, timeout=60,
                                  env={**os.environ, "PYTHONHASHSEED": str(g)}).stdout for g in range(5)}
        self.assertEqual(sorties, {b"CONFIG/champ-inconnu : $ : xx, yy, zz\n"})

    def test_compilation_avertissements_en_erreur(self):
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            for p, n, octets in modules():
                compile(octets, f"{p}.{n}", "exec")
