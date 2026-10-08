"""Identité bit à bit sur fixtures (T-P2-DET-1 ; E-P2-16, E-P2-17) : masque_fiv.py et intervalles.py en sous-processus
sur une même fixture, PYTHONHASHSEED 0 et 1, sous python3.11, python3.12 et python3.13 (3.10 exclu : hashlib.file_digest
de commun.py épinglé, Q-P2R-1) ; les trois sorties égales à l'octet. Chaque test nomme la mutation qui le rougit."""
import os
import shutil
import subprocess
import unittest

from tests.test_masque_fiv import fixture, h

ICI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIES = ("fiv_unites.txt", "intervalles.txt", "masque_j28.txt")


class TestIdentite(unittest.TestCase):
    def test_identite(self):
        """T-P2-DET-1. Fixture de MAS-1 (deux strates, cinq hôtes) ; trois interpréteurs × deux graines : codes 0,
        sha256 des trois sorties égaux. Mutation M-P2-20 : itération sur un ensemble."""
        argv, s = fixture(self)
        i = argv.index("--sortie")
        pythons = [shutil.which(v) for v in ("python3.11", "python3.12", "python3.13")]
        self.assertNotIn(None, pythons)
        empreintes = []
        for py in pythons:
            for graine in ("0", "1"):
                d = os.path.join(s, f"{os.path.basename(py)}-{graine}")
                env = dict(os.environ, PYTHONHASHSEED=graine, PYTHONDONTWRITEBYTECODE="1")
                for script in ("masque_fiv.py", "intervalles.py"):
                    r = subprocess.run([py, "-B", os.path.join(ICI, script), *argv[:i], "--sortie", d, *argv[i + 2:]],
                                       env=env, capture_output=True, text=True)
                    self.assertEqual(r.returncode, 0, r.stderr)
                empreintes.append([h(os.path.join(d, n)) for n in SORTIES])
        self.assertEqual(empreintes, empreintes[:1] * 6)
