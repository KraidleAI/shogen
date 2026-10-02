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
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock

from tests.test_exclusion import HARNESS

OUTIL = os.path.join(HARNESS, "tools", "oracle_record.py")
_SPEC = importlib.util.spec_from_file_location("oracle_record", OUTIL)
orc = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(orc)
T = b"import unittest\n\n\nclass T(unittest.TestCase):\n    def test_a(self):\n        pass\n"
OK = {"s2-harness/tests/__init__.py": b"", "s2-harness/tests/test_t.py": T, "LISEZ-MOI": "dépôt jetable\n".encode()}
KO = {**OK, "s2-harness/tests/test_t.py": T.replace(b"pass", b"self.fail()")}
SUITE = [sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests", "-t", ".", "-v"]
SHA = "ab" * 32
GIT_ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}


def g(d: str, *args: str, entree: bytes = None) -> str:
    """git sur le dépôt jetable d : identité de fixture, signature coupée, variables GIT_* retirées."""
    return subprocess.run(["git", "-C", d, "-c", "user.name=fixture", "-c", "user.email=fixture@invalid", "-c",
                           "commit.gpgsign=false", *args], input=entree, check=True, capture_output=True,
                          env=GIT_ENV).stdout.decode().strip()


def depot(d: str, commits):
    """Dépôt git jetable : un commit par mapping {chemin : octets} ; rend les sha complets (git rev-parse HEAD)."""
    os.makedirs(d)
    g(d, "init", "-q")
    g(d, "config", "core.autocrlf", "false")
    for fichiers in commits:
        for rel, octets in fichiers.items():
            os.makedirs(os.path.dirname(os.path.join(d, rel)), exist_ok=True)
            with open(os.path.join(d, rel), "wb") as f:
                f.write(octets)
        g(d, "add", "-A"), g(d, "commit", "-q", "-m", "fixture")
        yield g(d, "rev-parse", "HEAD")


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

    def test_verifier_un_refus_nomme_par_controle(self):
        """Lecture : enregistrements conformes acceptés (G2, rendu, served_from conforme), puis un refus nommé par
        contrôle sur copie modifiée. Rougit si un contrôle manque ou se relâche : champs, schema, rôle, tree.commit (sha
        complet exigé), static_only (false exact), exit (0 entier, chaque commande), sha256 et présence de chaque
        sortie, paquet.sha256 au rôle « rendu », champs nuls hors rendu, served_from (sha, conformité du servi)."""
        d, a = tempfile.mkdtemp(dir=self.d), "claude-opus-5-5"
        g2, rendu, ko = (orc.enregistrer(d, r, a, self.depot, c, **kw)[0] for r, c, kw in (
            ("G2", self.c1, {}), ("rendu", self.c1, {"paquet_sha256": SHA}), ("G2", self.c2, {})))
        sha = {p: hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in (g2, ko)}

        def copie(src, nom, f=None, **maj):
            rec = json.loads(Path(src).read_text(encoding="utf-8"))
            rec.update(maj)
            f and f(rec)
            Path(d, nom).write_text(json.dumps(rec), encoding="utf-8")
            return os.path.join(d, nom)
        sert = {"chemin": os.path.basename(g2), "sha256": sha[g2]}
        for chemin, role in ((g2, "G2"), (rendu, "rendu"), (copie(g2, "sert.json", served_from=sert), "G2")):
            self.assertEqual(orc.verifier(chemin, role, self.c1)["tree"]["commit"], self.c1)
        for controle, src, role, commit, f, maj in (
                ("champs", g2, "G2", self.c1, lambda r: r.pop("ecrit"), {}),
                ("champs", g2, "G2", self.c1, lambda r: r["runs"][0].pop("tests_avec_variable"), {}),
                ("schema", g2, "G2", self.c1, None, {"schema": "shogen.oracle-record.v0"}),
                ("rôle", g2, "cp-2", self.c1, None, {}), ("tree.commit", g2, "G2", self.c2, None, {}),
                ("tree.commit", g2, "G2", self.c1[:7], None, {}),
                ("static_only", g2, "G2", self.c1, None, {"static_only": 0}),
                ("exit", ko, "G2", self.c2, None, {}), ("exit", g2, "G2", self.c1, None, {"exit": False}),
                ("exit", g2, "G2", self.c1, lambda r: r["runs"][0].update(exit=1), {}),
                ("exit", g2, "G2", self.c1, None, {"runs": []}),
                ("sortie", g2, "G2", self.c1, lambda r: r["runs"][0]["sortie"].update(sha256="0" * 64), {}),
                ("sortie", g2, "G2", self.c1, lambda r: r["runs"][0]["sortie"].update(chemin="absente.out"), {}),
                ("paquet.sha256", rendu, "rendu", self.c1, lambda r: r["paquet"].update(sha256=SHA[:-1]), {}),
                ("nuls hors rendu", g2, "G2", self.c1, lambda r: r["sceau"].update(genTime="2026-10-02T05:00Z"), {}),
                ("served_from", g2, "G2", self.c1, None, {"served_from": {**sert, "sha256": "0" * 64}}),
                ("served_from", g2, "G2", self.c1, None, {"served_from": {"chemin": ko, "sha256": sha[ko]}})):
            with self.subTest(controle=controle, maj=maj):
                with self.assertRaisesRegex(ValueError, rf"^refus \({controle}\) : "):
                    orc.verifier(copie(src, f"mutant-{controle}.json", f, **maj), role, commit)

    def test_cli_ecriture_verifier_et_git_dir_herite(self):
        """CLI : écriture (rôle cp-2) sous un GIT_DIR hérité qui désigne un autre dépôt, --verifier conforme (code 0),
        refus nommé (code 2) ; options d'écriture mêlées à --verifier refusées ; commit inconnu : code 2, rien d'écrit ;
        commande en échec : code 1.
        Rougit si : variables GIT_* héritées gardées (autre dépôt lu), code ou motif de refus perdus, mélange admis,
        écriture sans --sortie admise."""
        d, autre = tempfile.mkdtemp(dir=self.d), os.path.join(self.d, "autre")
        list(depot(autre, [{"x": b"x"}]))

        def cli(*args, **env):
            return subprocess.run([sys.executable, "-B", OUTIL, *args], capture_output=True, text=True,
                                  env={**os.environ, **env})
        p = cli("--role", "cp-2", "--auteur", "claude-opus-5-5", "--depot", self.depot, "--commit", self.c1[:10],
                "--sortie", d, GIT_DIR=os.path.join(autre, ".git"))
        self.assertEqual(p.returncode, 0, p.stderr)
        chemin, avant = p.stdout.strip(), sorted(os.listdir(d))
        v, r, m = (cli("--verifier", chemin, "--role", "cp-2", *x) for x in (
            ("--commit", self.c1), ("--commit", self.c2), ("--commit", self.c1, "--auteur", "claude-opus-5-5")))
        self.assertEqual((v.returncode, v.stdout), (0, f"conforme : {chemin} (rôle cp-2, tree.commit {self.c1})\n"))
        self.assertEqual(r.returncode, 2)
        self.assertRegex(r.stderr, r"^oracle_record : refus \(tree\.commit\) : ")
        self.assertEqual((m.returncode, "--verifier" in m.stderr), (2, True))
        s = cli("--role", "G2", "--auteur", "a", "--depot", self.depot, "--commit", self.c1)
        self.assertEqual((s.returncode, "exige --auteur, --depot et --sortie" in s.stderr), (2, True))
        n = cli("--role", "G2", "--auteur", "a", "--depot", self.depot, "--commit", "0" * 40, "--sortie", d)
        self.assertEqual((n.returncode, sorted(os.listdir(d))), (2, avant))
        k = cli("--role", "G2", "--auteur", "a", "--depot", self.depot, "--commit", self.c2, "--sortie", d)
        self.assertEqual((k.returncode, os.path.dirname(k.stdout.strip())), (1, d))

    def test_collision_sans_ecrasement_et_lien_sortant(self):
        """Même instant, même pid, même rôle et commit : la seconde écriture lève FileExistsError sans écraser la
        sortie de la première ; commit qui porte un lien symbolique absolu (posé par la plomberie git, aucun lien sur
        le disque) : refus nommé du filtre « data » de tarfile, rien d'écrit. Rougit si : sortie ouverte en
        écrasement ; extraction sans filtre."""
        d, lien = tempfile.mkdtemp(dir=self.d), os.path.join(self.d, "lien")
        fixe = datetime(2026, 10, 2, 5, 0, tzinfo=timezone.utc)
        with mock.patch.object(orc, "datetime", mock.Mock(now=lambda tz: fixe)):
            chemin = orc.enregistrer(d, "G1", "claude-opus-5-5", self.depot, self.c1)[0]
            sortie = Path(d, json.loads(Path(chemin).read_text(encoding="utf-8"))["runs"][0]["sortie"]["chemin"])
            sortie.write_bytes(sortie.read_bytes() + b"marque")
            with self.assertRaises(FileExistsError):
                orc.enregistrer(d, "G1", "claude-opus-5-5", self.depot, self.c1)
        self.assertTrue(sortie.read_bytes().endswith(b"marque"))
        list(depot(lien, [{"x": b"x"}]))
        blob = g(lien, "hash-object", "-w", "--stdin", entree=b"/inexistant-shogen")
        g(lien, "update-index", "--add", "--cacheinfo", f"120000,{blob},lien")
        g(lien, "commit", "-q", "-m", "lien")
        avant = sorted(os.listdir(d))
        with self.assertRaisesRegex(ValueError, r"filtre data .* — refus$"):
            orc.enregistrer(d, "G2", "claude-opus-5-5", lien, "HEAD")
        self.assertEqual(sorted(os.listdir(d)), avant)


if __name__ == "__main__":
    unittest.main()
