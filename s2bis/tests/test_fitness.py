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
# Lecture JSON stricte de collecte/config.py (l.20-46) recopiée dans recalc/config_analyse.py, la frontière interdisant
# l'import (Q-RB-1 de la G2 de RB-T1) ; seuls le préfixe des refus et le nom de l'exception diffèrent.
COPIE = ("shogen_s2bis/collecte/config.py", "shogen_s2bis/recalc/config_analyse.py")


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


def lecture_stricte(chemin):
    """Texte, lu en octets sans import, des pièces de la lecture JSON stricte d'un module : `_objet`, `_entier`, et
    dans `charger` la lecture des octets, l'appel de json.loads avec ses crochets et son except, le retour (données,
    sha256)."""
    with open(os.path.join(RACINE, chemin), "rb") as f:
        source = f.read().decode("utf-8")
    defs = {n.name: n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef)}
    pieces = [defs["_objet"], defs["_entier"]] + [n for n in defs["charger"].body if isinstance(n, (ast.With, ast.Try,
                                                                                                    ast.Return))]
    return [ast.get_source_segment(source, n) for n in pieces]


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
        r = "shogen_s2bis.recalc"               # recalc : bibliothèque standard et recalc seuls (règle codée, plus
        # serrée que PROPOSITION §1 pt 2) : ni collecte, décodeurs compris, ni S2
        for source, cible in (("from ..collecte import config", "shogen_s2bis.collecte"),
                              ("from ..collecte.decodeurs import decoder", "shogen_s2bis.collecte.decodeurs"),
                              ("from shogen_s2.r1 import classify_ecart", "shogen_s2.r1")):
            self.assertEqual(violations(r, source), [f"{r} : {cible}"], source)
        self.assertEqual(violations(r, "from . import rotation\nfrom .lecteur import Lecteur\nimport hashlib"), [])

    def test_copie_de_la_lecture_json_stricte(self):       # Q-RB-1 : égalité du texte, l'une ne bouge pas sans l'autre
        source, copie = (lecture_stricte(c) for c in COPIE)
        self.assertEqual((len(copie), [p.replace("CONFIG/", "ANALYSE/").replace("RefusConfig", "RefusAnalyse")
                                       for p in source]), (5, copie))

    def test_copie_du_compte_des_niveaux(self):        # CB-6d : écrivain et lecteur du recalcul (RB-1j), texte égal
        def pieces(chemin):
            with open(os.path.join(RACINE, chemin), encoding="utf-8") as f:
                source = f.read()
            return [ast.get_source_segment(source, n) for n in ast.parse(source).body if isinstance(
                n, ast.FunctionDef) and n.name == "_trop_profonde" or isinstance(n, ast.Assign) and getattr(
                n.targets[0], "id", None) in ("BARRE", "HORS_CROCHETS", "NIVEAUX")]
        ecrivain = pieces("shogen_s2bis/collecte/journal.py")
        self.assertEqual((len(ecrivain), ecrivain), (4, pieces("shogen_s2bis/recalc/lecteur.py")))

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
