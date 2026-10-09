"""Identité bit à bit (T-CA-DET-1 ; E-CA-21) : tau.py en sous-processus sur un même banc synthétique, PYTHONHASHSEED 0
et 1, sous python3.10 à 3.13 : les deux sorties égales à l'octet dans les huit exécutions. Mutation M-CA-23 : itération
sur un ensemble dans une sortie."""
import os
import shutil
import subprocess
import unittest

import socle
import tau
from tests.test_cli import banc

ICI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestIdentite(unittest.TestCase):
    def test_identite(self):
        argv, d = banc(self)
        pythons = [shutil.which(f"python3.{v}") for v in (10, 11, 12, 13)]
        self.assertNotIn(None, pythons)
        empreintes = []
        for py in pythons:
            for graine in ("0", "1"):
                s = os.path.join(d, f"{os.path.basename(py)}-{graine}")
                env = {k: v for k, v in os.environ.items() if k != "SHOGEN_S2_CAMPAGNE_CONTROL"}
                r = subprocess.run([py, "-B", os.path.join(ICI, "tau.py"), *argv[:3], s, *argv[4:]],
                                   capture_output=True, text=True,
                                   env=dict(env, PYTHONHASHSEED=graine, PYTHONDONTWRITEBYTECODE="1"))
                self.assertEqual(r.returncode, 0, r.stderr)
                empreintes.append([socle.empreinte(os.path.join(s, n)) for n in tau.SORTIES])
        self.assertEqual(empreintes, empreintes[:1] * 8)


if __name__ == "__main__":
    unittest.main()
