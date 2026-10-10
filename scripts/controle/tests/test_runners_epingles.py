"""Cas de enforcement/runners-epingles.py (lot DETTES-T5, adjudication Q-2 du 2026-10-09 ; SHOGEN-CI-RUNNERS-1) : aucun
libellé de runner en `-latest` dans `runs-on` ni dans une clé `os`, sous toutes les formes lues. Arbres temporaires,
sauf le premier cas (l'arbre du dépôt : rouge tant qu'un `windows-latest` y reste)."""
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

RACINE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
SCRIPT = os.path.join(RACINE, "enforcement", "runners-epingles.py")
NL = chr(10)


def controler(*argv):
    p = subprocess.run([sys.executable, "-B", SCRIPT, *argv], capture_output=True, text=True, timeout=60)
    return p.returncode, p.stdout, p.stderr


class RunnersEpingles(unittest.TestCase):
    def arbre(self, fichiers):
        d = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, d)
        os.makedirs(os.path.join(d, ".github", "workflows"))
        for nom, texte in fichiers.items():
            os.makedirs(os.path.dirname(os.path.join(d, ".github", "workflows", nom)), exist_ok=True)
            with open(os.path.join(d, ".github", "workflows", nom), "wb") as f:
                f.write(texte if isinstance(texte, bytes) else texte.encode("utf-8"))
        return d

    def refuse(self, texte, attendus, nom="w.yml"):
        code, _out, err = controler(self.arbre({nom: texte}))
        self.assertEqual((code, sorted(re.findall(r"image flottante \(-latest\) : (\S+:\d+ : \S+)", err))),
                         (1, sorted(f".github/workflows/{nom}:{a}" for a in attendus)), err)

    def test_arbre_du_depot_conforme(self):
        code, out, err = controler(RACINE)
        self.assertEqual(code, 0, err)
        self.assertRegex(out, r"^runners-epingles : conforme \([1-9][0-9]* workflow\(s\), [1-9][0-9]* clé")

    def test_runs_on_en_ligne(self):
        self.refuse("jobs:" + NL + "  a:" + NL + "    runs-on: ubuntu-latest" + NL + "  b:" + NL
                    + "    runs-on: ubuntu-latest-4core  # grand runner" + NL + "  c:" + NL
                    + "    runs-on: ubuntu-24.04" + NL, ["3 : ubuntu-latest", "5 : ubuntu-latest-4core"])

    def test_matrice_en_flux_et_include(self):
        self.refuse("    strategy:" + NL + "      matrix:" + NL + "        os: [ubuntu-24.04, windows-latest]" + NL
                    + "        include:" + NL + "          - os: macos-latest" + NL
                    + "          - {os: windows-2025, x: 1}" + NL, ["3 : windows-latest", "5 : macos-latest"])

    def test_formes_en_bloc(self):
        self.refuse("    runs-on:" + NL + "      - self-hosted" + NL + "      - ubuntu-latest" + NL
                    + "    matrix:" + NL + "      os:" + NL + "        - ubuntu-24.04" + NL + NL
                    + "        - windows-latest" + NL + "      os2: [windows-latest]" + NL
                    + "      os: [ubuntu-24.04," + NL + "        macos-latest]" + NL,
                    ["3 : ubuntu-latest", "8 : windows-latest", "11 : macos-latest"])

    def test_guillemets_et_extension_yaml(self):
        self.refuse("    runs-on: \"ubuntu-latest\"" + NL + "    'os': ['windows-latest']" + NL
                    + "    \"runs-on\": 'macos-latest' # x" + NL, ["1 : ubuntu-latest", "2 : windows-latest",
                                                                  "3 : macos-latest"], nom="w.yaml")

    def test_admis(self):
        """Commentaires, expression de matrice, libellés épinglés, autres clés, sous-dossier (la forge ne le lit pas)."""
        d = self.arbre({"w.yml": "# runs-on: ubuntu-latest" + NL + "    runs-on: ${{ matrix.os }}  # windows-latest"
                        + NL + "        os: [ubuntu-24.04, windows-2025] # macos-latest" + NL
                        + "      - run: echo ubuntu-latest" + NL + "    runs-on: 'a#b' # ubuntu-latest" + NL,
                        "sous/x.yml": "    runs-on: ubuntu-latest" + NL, "w.txt": "    runs-on: ubuntu-latest" + NL})
        code, out, err = controler(d)
        self.assertEqual((code, err), (0, ""))
        self.assertIn("conforme (1 workflow(s), 3 clé(s) runs-on/os lues)", out)

    def test_erreurs_sortie_3(self):
        """Racine sans .github/workflows, arguments en trop ou absents, workflow illisible (UTF-8 invalide) : 3."""
        vide = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, vide)
        illisible = self.arbre({"w.yml": b"    runs-on: ubuntu-24.04\n\xff\n"})
        for argv in ((vide,), (illisible, illisible), (), (illisible,)):
            self.assertEqual(controler(*argv)[0], 3, argv)
