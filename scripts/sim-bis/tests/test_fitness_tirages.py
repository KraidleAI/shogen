"""Fitness des tirages (SB-3b ; I-3 de la tranche 1, étendu par sa G2 ; E-S-42, E-S-43), lue par `ast` sur le moteur
(tout `*.py` du dossier du lot, hors tests et adaptateurs d'oracle) : aucune puissance (`**`, `pow`), qui pourrait
porter sur un flottant (pow de libm) ; une puissance de deux s'écrit par décalage. Du module `random`, la classe
`Random` seule ; d'une instance, la méthode `random()` seule (E-S-42 : seule garantie de stabilité d'une version de
Python à l'autre)."""
import ast
import os
import random
import unittest

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


def refus_puissance(source: str) -> list:
    """`**` (binaire ou augmenté) et appel de `pow`."""
    out = []
    for n in ast.walk(ast.parse(source)):
        if isinstance(n, (ast.BinOp, ast.AugAssign)) and isinstance(n.op, ast.Pow):
            out.append(f"** l.{n.lineno}")
        elif isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "pow":
            out.append(f"pow l.{n.lineno}")
    return out


def refus_hasard(source: str) -> list:
    """Attribut du module `random` autre que `Random` ; attribut, sur tout objet, nommé comme une méthode publique de
    random.Random autre que `random` ; `from random import` autre que `Random`."""
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
        """Ni `**` ni `pow` dans le moteur ; le vérificateur voit x ** 2, x **= 2 et pow(2, 3), et admet le décalage.
        Mutation M-3B-13 : `2 ** 3` ajouté à sources.py."""
        for f, s in moteur():
            self.assertEqual(refus_puissance(s), [], f)
        for s in ("x ** 2", "x **= 2", "pow(2, 3)"):
            self.assertNotEqual(refus_puissance(s), [], s)
        self.assertEqual(refus_puissance("1 << 53"), [])

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
