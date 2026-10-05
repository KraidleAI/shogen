"""Fitness du lot (SB-0 ; E-S-01, E-S-06 ; T-FRO-1, analyse des imports) : frontière lue par `ast` sur chaque module du
moteur (tout `*.py` du dossier du lot, hors tests et hors les deux adaptateurs d'oracle d'E-S-01) ; aucun octet de barre
oblique inverse dans les fichiers du lot (consigne de gabarit, ADR-0028 annexe B.16) ; SB-1 : aucune fonction
transcendante de libm dans le moteur (E-S-43), lue par `ast`."""
import ast
import os
import sys
import unittest

ICI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORACLES = {"oracle_r1.py", "oracle_recalc.py"}
INTERDITS = {"importlib", "runpy", "socket", "ssl", "http", "urllib", "ftplib", "smtplib", "socketserver", "xmlrpc",
             "asyncio"}
MATH_ADMIS = {"nextafter", "isqrt", "gcd", "floor", "ceil", "isfinite"}


def refus_imports(source: str, lot: set) -> list:
    """Motifs de refus d'un module du moteur : import relatif ; module ni de la bibliothèque standard ni du lot
    (`shogen_s2`, `shogen_s2bis` compris) ; module interdit (import dynamique, réseau) ; appel de `__import__`."""
    out = []
    for n in ast.walk(ast.parse(source)):
        if isinstance(n, ast.ImportFrom) and n.level:
            out.append(f"import relatif l.{n.lineno}")
        noms = [a.name for a in n.names] if isinstance(n, ast.Import) else (
            [n.module] if isinstance(n, ast.ImportFrom) and n.module else [])
        for m in noms:
            t = m.split(".")[0]
            if t in INTERDITS or not (t in sys.stdlib_module_names or t in lot):
                out.append(f"{m} l.{n.lineno}")
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "__import__":
            out.append(f"__import__ l.{n.lineno}")
    return out


def refus_libm(source: str) -> list:
    """Usages de libm refusés au moteur (E-S-43) : attribut de `math` hors des fonctions exactes MATH_ADMIS, import
    depuis `math` hors MATH_ADMIS, `math` sous un alias, tout import de `cmath`."""
    out = []
    for n in ast.walk(ast.parse(source)):
        if isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name) and n.value.id == "math":
            out += [] if n.attr in MATH_ADMIS else [f"math.{n.attr} l.{n.lineno}"]
        elif isinstance(n, ast.ImportFrom) and n.module in ("math", "cmath"):
            out += [f"{n.module}.{a.name} l.{n.lineno}" for a in n.names
                    if n.module == "cmath" or a.name not in MATH_ADMIS]
        elif isinstance(n, ast.Import):
            out += [f"{a.name} l.{n.lineno}" for a in n.names if a.name == "cmath" or (a.name == "math" and a.asname)]
    return out


class TestFitness(unittest.TestCase):
    def test_frontiere_du_moteur(self):
        """Chaque module du moteur : aucun refus. Mutations M-FRO-1 (`import shogen_s2` dans commun.py), M-0-24
        (`import socket` dans commun.py)."""
        lot = {f[:-3] for f in os.listdir(ICI) if f.endswith(".py")}
        moteur = sorted(f for f in os.listdir(ICI) if f.endswith(".py") and f not in ORACLES)
        self.assertIn("commun.py", moteur)
        for f in moteur:
            with open(os.path.join(ICI, f), encoding="utf-8") as g:
                self.assertEqual(refus_imports(g.read(), lot), [], f)

    def test_frontiere_refuse(self):
        """Le vérificateur voit chaque forme interdite, et admet bibliothèque standard et lot."""
        for s in ("import shogen_s2", "from shogen_s2bis.collecte import config", "from . import commun",
                  "import importlib", "__import__('os')", "import numpy", "import urllib.request",
                  "from socket import socket"):
            self.assertNotEqual(refus_imports(s, {"commun"}), [], s)
        self.assertEqual(refus_imports("import json, os.path" + chr(10) + "from commun import Refus", {"commun"}), [])

    def test_aucune_barre_oblique_inverse(self):
        """Aucun octet 92 dans les fichiers du lot (E-S-06 ; un texte qui en porte un s'écrit par chr(92)). Mutation
        M-0-25 : barre oblique inverse ajoutée dans un commentaire de commun.py."""
        for d, _s, fs in os.walk(ICI):
            for f in fs if "__pycache__" not in d else ():
                with open(os.path.join(d, f), "rb") as g:
                    self.assertNotIn(92, g.read(), os.path.join(d, f))

    def test_aucune_fonction_transcendante(self):
        """E-S-43 : le moteur n'emploie de `math` que des fonctions exactes (MATH_ADMIS) ; le vérificateur voit
        math.log, from math import exp, math sous un alias, cmath. Mutation M-1-24 : math.log ajouté à aleas.py."""
        for f in sorted(os.listdir(ICI)):
            if f.endswith(".py") and f not in ORACLES:
                with open(os.path.join(ICI, f), encoding="utf-8") as g:
                    self.assertEqual(refus_libm(g.read()), [], f)
        for s in ("math.log(2)", "from math import exp", "import math as m", "import cmath", "from cmath import pi"):
            self.assertNotEqual(refus_libm(s), [], s)
        self.assertEqual(refus_libm("import math" + chr(10) + "math.nextafter(1.0, 0.0)"), [])
