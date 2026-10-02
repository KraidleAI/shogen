"""SHOGEN-ORACLE-ENREG-1 (G0-partie-2.md §B ; ADR-0028 D6 (viii), §1 bis.6) : tools/oracle_record.py sur dépôt
git jetable (fixtures seulement, D.4 a ; variable scellée jamais posée). Attendus indépendants de l'outil : sha256
des octets écrits par le test, sha complets de git rev-parse, liste fermée écrite à la main ; un mutant par test."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tests.test_exclusion import HARNESS

_SPEC = importlib.util.spec_from_file_location("oracle_record", os.path.join(HARNESS, "tools", "oracle_record.py"))
orc = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(orc)
T = b"import unittest\n\n\nclass T(unittest.TestCase):\n    def test_a(self):\n        pass\n"
OK = {"s2-harness/tests/__init__.py": b"", "s2-harness/tests/test_t.py": T, "LISEZ-MOI": "dépôt jetable\n".encode()}
KO = {**OK, "s2-harness/tests/test_t.py": T.replace(b"pass", b"self.fail()")}
SUITE = [sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests", "-t", ".", "-v"]
SHA = "ab" * 32
GIT_ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}


def depot(d: str, commits):
    """Dépôt git jetable : un commit par mapping {chemin : octets} ; rend les sha complets (git rev-parse HEAD)."""
    def g(*args):
        return subprocess.run(["git", "-C", d, "-c", "user.name=fixture", "-c", "user.email=fixture@invalid", "-c",
                               "commit.gpgsign=false", *args], check=True, capture_output=True, env=GIT_ENV).stdout
    os.makedirs(d)
    g("init", "-q")
    g("config", "core.autocrlf", "false")
    for fichiers in commits:
        for rel, octets in fichiers.items():
            os.makedirs(os.path.dirname(os.path.join(d, rel)), exist_ok=True)
            with open(os.path.join(d, rel), "wb") as f:
                f.write(octets)
        g("add", "-A"), g("commit", "-q", "-m", "fixture")
        yield g("rev-parse", "HEAD").decode().strip()


class TestOracleRecord(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = tempfile.mkdtemp(prefix="oracle_test_")
        cls.depot, cls.sortie = os.path.join(cls.d, "depot"), os.path.join(cls.d, "sorties")
        os.makedirs(cls.sortie)
        cls.c1, cls.c2 = depot(cls.depot, [OK, KO])

    def test_enregistrement_champs_et_sha(self):
        """Rôle G2, commit court : champs de D6 (viii), paquet.sha256 et sceau.genTime nuls, sha256 par fichier et de la
        sortie, nom shogen-<sha court>-<rôle>-<date>-<pid>.json. Rougit si : autre commit extrait, sha d'un fichier
        faux, commande hors liste, sortie non hachée, static_only vrai, variable non consignée ou tests comptés lancés
        avec elle, exit faux, champ nul hors rendu rempli."""
        chemin, code = orc.enregistrer(self.sortie, "G2", "claude-opus-5-5", self.depot, self.c1[:10])
        self.assertRegex(os.path.basename(chemin), rf"^shogen-{self.c1[:7]}-G2-\d{{8}}T\d{{6}}Z-\d+\.json$")
        rec = json.loads(Path(chemin).read_text(encoding="utf-8"))
        out = Path(self.sortie, rec["runs"][0]["sortie"]["chemin"]).read_bytes()
        self.assertIn(b"test_a (tests.test_t.T.test_a) ... ok", out)
        self.assertRegex(rec.pop("ecrit"), r"^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ$")
        self.assertEqual((code, rec), (0, {
            "schema": "shogen.oracle-record.v1", "role": "G2", "auteur": "claude-opus-5-5", "base": None,
            "tree": {"commit": self.c1, "extraction": f"git archive {self.c1}",
                     "sha256": {k: hashlib.sha256(v).hexdigest() for k, v in sorted(OK.items())}},
            "static_only": False, "served_from": None, "python": sys.version, "exit": 0,
            "env": {"SHOGEN_S2_CAMPAGNE_CONTROL": None, **{k: os.environ.get(k) for k in ("PYTHONHASHSEED",
                                                                                      "PYTHONPATH")}},
            "runs": [{"nom": "suite", "arbre": "s2-harness", "commande": SUITE, "exit": 0, "tests_avec_variable": [],
                      "sortie": {"chemin": os.path.basename(chemin)[:-5] + ".0-suite.out",
                                 "sha256": hashlib.sha256(out).hexdigest()}}],
            "paquet": {"sha256": None}, "sceau": {"genTime": None}}))

    def test_rendu_base_echec_et_refus(self):
        """Rôle « rendu », commit dont le test échoue, base = premier commit : paquet.sha256 et genTime écrits, exit 1 ;
        refus sans rien écrire : rendu sans paquet.sha256, paquet.sha256 ou genTime hors rendu, commande ou rôle hors
        liste. Rougit si : exit forcé à 0, base non résolue, garde du rôle « rendu » retirée, liste fermée ouverte."""
        chemin, code = orc.enregistrer(self.sortie, "rendu", "claude-opus-5-5", self.depot, self.c2, base=self.c1[:8],
                                       paquet_sha256=SHA, sceau_gentime="2026-10-02T05:00:00Z")
        rec = json.loads(Path(chemin).read_text(encoding="utf-8"))
        self.assertEqual((code, rec["exit"], rec["runs"][0]["exit"], rec["base"], rec["paquet"], rec["sceau"]),
                         (1, 1, 1, self.c1, {"sha256": SHA}, {"genTime": "2026-10-02T05:00:00Z"}))
        avant = sorted(os.listdir(self.sortie))
        for role, kw in (("rendu", {}), ("rendu", {"paquet_sha256": SHA[:-1]}), ("G2", {"paquet_sha256": SHA}),
                         ("cp-2", {"sceau_gentime": "2026-10-02T05:00:00Z"}), ("G2", {"commandes": ("rapport",)}),
                         ("G3", {}), ("G1", {"commandes": ()})):
            with self.subTest(role=role, kw=kw), self.assertRaisesRegex(ValueError, r"— refus$"):
                orc.enregistrer(self.sortie, role, "claude-opus-5-5", self.depot, self.c1, **kw)
        self.assertEqual(sorted(os.listdir(self.sortie)), avant)

    def test_consigne_et_tests_lances(self):
        """Fonctions pures, sur un mapping (aucun processus ne reçoit la variable) et des sorties -v de 3.11 et 3.10.
        Rougit si : variable absente non nulle ; valeur posée perdue ; docstring lue comme test ; id 3.10 incomplet."""
        self.assertEqual(orc.consigne({"SHOGEN_S2_CAMPAGNE_CONTROL": "/chemin/fictif", "AUTRE": "x"}),
                         {"SHOGEN_S2_CAMPAGNE_CONTROL": "/chemin/fictif", "PYTHONHASHSEED": None, "PYTHONPATH": None})
        texte = ("test_a (tests.t.T.test_a)\nDoc (tests.t.T) ... ok\ntest_b (tests.t.T.test_b) ... skipped 'm'\n"
                 "test_c (tests.t.U) ... ok\n")
        self.assertEqual(orc.tests_lances(texte), ["tests.t.T.test_a", "tests.t.T.test_b", "tests.t.U.test_c"])


if __name__ == "__main__":
    unittest.main()
