"""Fitness des tirages (SB-3b ; I-3 de la tranche 1, étendu par sa G2 ; E-S-42, E-S-43), lue par `ast` sur le moteur
(tout `*.py` du dossier du lot, hors tests et adaptateurs d'oracle) : aucune puissance (`**`, `pow`), qui pourrait
porter sur un flottant (pow de libm) ; une puissance de deux s'écrit par décalage. Du module `random`, la classe
`Random` seule ; d'une instance, la méthode `random()` seule (E-S-42 : seule garantie de stabilité d'une version de
Python à l'autre)."""
import ast
import os
import random
import unittest

from tests import test_fitness

ICI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORACLES = {"oracle_r1.py", "oracle_recalc.py"}
METHODES = {n for n in dir(random.Random) if not n.startswith("_")} - {"random"}


def moteur() -> list:
    """[(fichier, source)] des modules du moteur."""
    out = []
    for f in sorted(os.listdir(ICI)):
        if f.endswith(".py") and f not in ORACLES:
            with open(os.path.join(ICI, f), encoding="utf-8") as g:
                out.append((f, g.read()))
    return out


PUISSANCES = {"pow", "ipow", "__pow__", "__rpow__", "__ipow__"}


def refus_puissance(source: str) -> list:
    """`**` (binaire ou augmenté) ; nom de PUISSANCES, appelé ou pris comme valeur ; attribut de PUISSANCES sur tout
    objet (operator.pow, operator.ipow, même sous alias ; (2.0).__pow__ ; x.__rpow__) ; import depuis `operator`
    d'un nom de PUISSANCES ou de `*` (C-4 de la G2 de la tranche 2, LIBM-POW-1). Limite écrite : un accès dynamique
    (getattr d'une chaîne calculée, R-28 du réviseur) échappe à toute lecture syntaxique ; il reste à la relecture."""
    out = []
    for n in ast.walk(ast.parse(source)):
        if isinstance(n, (ast.BinOp, ast.AugAssign)) and isinstance(n.op, ast.Pow):
            out.append(f"** l.{n.lineno}")
        elif isinstance(n, ast.Name) and n.id in PUISSANCES:
            out.append(f"{n.id} l.{n.lineno}")
        elif isinstance(n, ast.Attribute) and n.attr in PUISSANCES:
            out.append(f".{n.attr} l.{n.lineno}")
        elif isinstance(n, ast.ImportFrom) and n.module == "operator":
            out += [f"operator.{a.name} l.{n.lineno}" for a in n.names if a.name in PUISSANCES | {"*"}]
    return out


def refus_hasard(source: str) -> list:
    """Attribut du module `random` autre que `Random` ; attribut, sur tout objet, nommé comme une méthode publique de
    random.Random autre que `random` ; `from random import` autre que `Random`. Limite écrite (C-4 de la G2 de la
    tranche 2) : une méthode obtenue par getattr d'une chaîne calculée (R-28 du réviseur) n'est pas vue."""
    out = []
    for n in ast.walk(ast.parse(source)):
        if isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name) and n.value.id == "random":
            out += [] if n.attr == "Random" else [f"random.{n.attr} l.{n.lineno}"]
        elif isinstance(n, ast.Attribute) and n.attr in METHODES:
            out.append(f".{n.attr} l.{n.lineno}")
        elif isinstance(n, ast.ImportFrom) and n.module == "random":
            out += [f"random.{a.name} l.{n.lineno}" for a in n.names if a.name != "Random"]
    return out


class TestTirages(unittest.TestCase):
    def test_aucune_puissance(self):
        """Ni `**` ni `pow` dans le moteur ; le vérificateur voit x ** 2, x **= 2 et pow(2, 3), et, depuis C-4 de la G2
        de la tranche 2 (LIBM-POW-1) : pow pris comme valeur, operator.pow et operator.ipow (attribut, même sous alias,
        ou importés, `*` compris), les attributs __pow__, __rpow__ et __ipow__ ; il admet le décalage et operator.mul.
        Mutations M-3B-13 (`2 ** 3` ajouté à sources.py), R-26 (operator.pow), R-27 ((2.0).__pow__), M-C4-01 à M-C4-03
        (contrôle des noms, des attributs ou des imports retiré)."""
        for f, s in moteur():
            self.assertEqual(refus_puissance(s), [], f)
        for s in ("x ** 2", "x **= 2", "pow(2, 3)", "f = pow", "operator.pow(2, 3)",
                  "import operator as o" + chr(10) + "o.ipow(x, 2)", "from operator import pow",
                  "from operator import ipow as p", "from operator import __pow__", "from operator import *",
                  "(2.0).__pow__(0.5)", "x.__rpow__(2)", "x.__ipow__(2)"):
            self.assertNotEqual(refus_puissance(s), [], s)
        for s in ("1 << 53", "import operator" + chr(10) + "operator.mul(2, 3)"):
            self.assertEqual(refus_puissance(s), [], s)

    def test_random_seule(self):
        """Du module random, Random seule ; d'une instance, random() seule ; le vérificateur voit random.random(),
        random.seed(1), random.Random(1).uniform(0, 1), u.__self__.choice(x) et from random import shuffle, et admet
        random.Random(1).random(). Mutation M-3B-14 : `.uniform(0, 1)` au lieu de `.random` dans aleas.flux."""
        for f, s in moteur():
            self.assertEqual(refus_hasard(s), [], f)
        for s in ("random.random()", "random.seed(1)", "random.Random(1).uniform(0, 1)", "u.__self__.choice(x)",
                  "from random import shuffle"):
            self.assertNotEqual(refus_hasard(s), [], s)
        self.assertEqual(refus_hasard("import random" + chr(10) + "random.Random(1).random()"), [])

    def test_adaptateurs(self):
        """Brief de la tranche 4 (garde `ast` des puissances et du hasard appliquée à ses modules, LIBM-POW-1) : les
        adaptateurs d'oracle présents (hors du moteur pour la seule frontière d'imports, E-S-01) ne portent ni
        puissance, ni hasard, ni fonction transcendante de libm. Mutation M-14-07 (`2 ** 3` ajouté à oracle_r1.py)."""
        presents = sorted(f for f in ORACLES if os.path.exists(os.path.join(ICI, f)))
        self.assertIn("oracle_r1.py", presents)
        for f in presents:
            with open(os.path.join(ICI, f), encoding="utf-8") as g:
                s = g.read()
            self.assertEqual((refus_puissance(s), refus_hasard(s), test_fitness.refus_libm(s)), ([], [], []), f)
