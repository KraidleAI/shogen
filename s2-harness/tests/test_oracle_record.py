"""SHOGEN-ORACLE-ENREG-1 (G0-partie-2.md §B ; ADR-0028 D6 (viii), §1 bis.6) : tools/oracle_record.py sur dépôt
git jetable (fixtures seulement, D.4 a ; variable scellée jamais posée). Attendus indépendants de l'outil : sha256
des octets écrits par le test, sha complets de git rev-parse, liste fermée écrite à la main ; un mutant par test."""
from __future__ import annotations

import hashlib
import importlib.machinery
import importlib.util
import json
import os
import py_compile
import re
import shutil
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
LENT = {**OK, "s2-harness/tests/test_t.py": T.replace(b"pass", b"__import__('time').sleep(20)")}
SUITE = [sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests", "-t", ".", "-v"]
SHA = "ab" * 32
GIT_ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
LINT = os.path.join(os.path.dirname(HARNESS), "enforcement", "lint-model-pinning.sh")
BANNI = "claude-opus-" + "5"                    # construit à l'exécution, comme dans le lint (aucun littéral)
STUB = b"import sys\nprint('argv', sys.argv[1:])\n"    # tools/rendu_unique.py de fixture : imprime ses arguments


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
        cls.c1, cls.c2, cls.c3 = depot(cls.depot, [OK, KO, LENT])

    def test_enregistrement_champs_et_sha(self):
        """Rôle G2, commit court : champs de D6 (viii), paquet.sha256 et sceau.genTime nuls, sha256 par fichier et de la
        sortie, nom shogen-<sha court>-<rôle>-<date>-<pid>.json. Rougit si : autre commit extrait, sha d'un fichier
        faux, commande hors liste, sortie non hachée, static_only vrai, variable non consignée ou tests comptés lancés
        avec elle, exit faux, champ nul hors rendu rempli, env non consigné (PYTHONHASHSEED posé ; C-11, R17).
        Hermétique (SHOGEN-TEST-ENV-HERMETIQUE-1) : variable scellée retirée de l'environnement du test, posée ou non
        dans celui de la suite ; os.environ rendu intact à la sortie (mock.patch.dict)."""
        with mock.patch.dict(os.environ, {"PYTHONHASHSEED": "17"}):       # jamais la variable scellée
            os.environ.pop("SHOGEN_S2_CAMPAGNE_CONTROL", None)
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
            "env": {"SHOGEN_S2_CAMPAGNE_CONTROL": None, "PYTHONHASHSEED": "17", "PYTHONPATH": os.environ.get(
                "PYTHONPATH")},
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
        """Lecture : enregistrements conformes acceptés (G2, rendu à six runs écrits ici, served_from conforme), puis un
        refus nommé par contrôle sur copie modifiée. Rougit si un contrôle manque ou se relâche : champs, schema, rôle,
        tree.commit (sha complet exigé), static_only (false exact), exit (0 entier, chaque commande), sha256 et présence
        de chaque sortie, paquet.sha256 et runs (suite puis D.4 b, dans l'ordre ; C-6) au rôle « rendu », champs nuls
        hors rendu, served_from (sha, conformité du servi)."""
        d, a = tempfile.mkdtemp(dir=self.d), "claude-opus-5-5"
        g2, rendu1, ko = (orc.enregistrer(d, r, a, self.depot, c, **kw)[0] for r, c, kw in (
            ("G2", self.c1, {}), ("rendu", self.c1, {"paquet_sha256": SHA}), ("G2", self.c2, {})))
        sha = {p: hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in (g2, ko)}

        def copie(src, nom, f=None, **maj):
            rec = json.loads(Path(src).read_text(encoding="utf-8"))
            rec.update(maj)
            f and f(rec)
            Path(d, nom).write_text(json.dumps(rec), encoding="utf-8")
            return os.path.join(d, nom)
        six = ["suite", "j14-principal", "j14-second", "j28", "recalcul-tiers", "raw"]    # C-6 : suite, puis D.4 b
        for n in six:
            Path(d, f"{n}.out").write_bytes(n.encode())
        runs = [{"nom": n, "arbre": "s2-harness", "commande": [n], "exit": 0, "tests_avec_variable": [],
                 "sortie": {"chemin": f"{n}.out", "sha256": hashlib.sha256(n.encode()).hexdigest()}} for n in six]
        rendu = copie(rendu1, "rendu.json", runs=runs)
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
                ("runs", rendu1, "rendu", self.c1, None, {}), ("runs", rendu, "rendu", self.c1,
                                                               lambda r: r["runs"].reverse(), {}),
                ("runs", rendu, "rendu", self.c1, lambda r: r["runs"][0].update(nom="raw"), {}),   # tête ≠ suite (M24)
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
        self.assertEqual((v.returncode, v.stdout), (0, f"conforme : {chemin} (rôle cp-2, tree.commit {self.c1} ; "
                                                       "tree.sha256 non recalculé : --depot absent)\n"))
        self.assertEqual(r.returncode, 2)
        self.assertRegex(r.stderr, r"^oracle_record : refus \(tree\.commit\) : ")
        self.assertEqual((m.returncode, "--verifier" in m.stderr), (2, True))
        s = cli("--role", "G2", "--auteur", "a", "--depot", self.depot, "--commit", self.c1)
        self.assertEqual((s.returncode, "exige --auteur, --depot et --sortie" in s.stderr), (2, True))
        a = ("--role", "G2", "--auteur", "claude-opus-5-5", "--depot", self.depot, "--sortie", d)
        n = cli(*a, "--commit", "0" * 40)
        self.assertEqual((n.returncode, sorted(os.listdir(d))), (2, avant))
        k = cli(*a, "--commit", self.c2)
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

    def copie(self, d: str, src: str, nom: str, f) -> str:
        """Copie de l'enregistrement `src` modifiée par f(rec), écrite dans d sous `nom` (sorties relatives
        intactes)."""
        rec = json.loads(Path(src).read_text(encoding="utf-8"))
        f(rec)
        Path(d, nom).write_text(json.dumps(rec), encoding="utf-8")
        return os.path.join(d, nom)

    def test_verifier_auteur_liste_blanche_du_lint(self):
        """SHOGEN-ENREG-VERIF-1 (i) : auteur égal à un identifiant de la liste blanche (oracle : celle qu'imprime le
        lint d'épinglage lui-même), ou à cet identifiant suivi exactement de « [1m] » ; toute autre forme : refus
        (auteur). Liste lue dans le lint : un lint de fixture qui en porte une autre la remplace ; ligne ALLOWED répétée
        ou lint absent : refus. Rougit si : préfixe, casse, autre suffixe ou blancs admis ; [1m] refusé ; liste
        recopiée dans l'outil ; première de deux lignes ALLOWED lue ; contrôle absent."""
        d, bash = tempfile.mkdtemp(dir=self.d), shutil.which("bash")    # PATH (CreateProcess lirait System32 d'abord)
        self.assertTrue(bash and os.path.isfile(LINT), f"bash ({bash}) ou lint d'épinglage ({LINT}) absent")
        os.makedirs(os.path.join(d, "arbre", ".claude", "agents"))
        Path(d, "arbre", ".claude", "agents", "a.md").write_text("---\nmodel: opus\n---\n", encoding="utf-8")
        refus = subprocess.run([bash, LINT, os.path.join(d, "arbre")], capture_output=True, text=True).stderr
        admis = re.search(r"liste blanche : (.+) \(R-1\)\.$", refus, re.M).group(1).split()
        x, g2 = admis[0], orc.enregistrer(d, "G2", admis[0], self.depot, self.c1)[0]

        def auteur(a, ok, nom="a.json"):
            p = self.copie(d, g2, nom, lambda r: r.update(auteur=a))
            if ok:
                return self.assertEqual(orc.verifier(p, "G2", self.c1)["auteur"], a)
            with self.assertRaisesRegex(ValueError, r"^refus \(auteur\) : "):
                orc.verifier(p, "G2", self.c1)
        for a in [*admis, *(y + "[1m]" for y in admis)]:
            auteur(a, True)
        for a in (BANNI, BANNI + "[1m]", "opus", x + "x", x[:-1], x.upper(), x + "[1M]", x + "[2m]", x + "[1m][1m]",
                  " " + x, x + " ", "[1m]", None, 5):
            with self.subTest(auteur=a):
                auteur(a, False)
        faux = os.path.join(d, "lint.sh")
        for contenu, a, ok in (("# ALLOWED='en-commentaire'\nALLOWED='modele-fixture-1'\n", "modele-fixture-1", True),
                               ("ALLOWED='modele-fixture-1'\n", x, False),
                               ("ALLOWED='modele-fixture-1'\nALLOWED='modele-fixture-1'\n", "modele-fixture-1", False),
                               (None, x, False)):
            Path(faux).write_text(contenu, encoding="utf-8") if contenu else Path(faux).unlink(missing_ok=True)
            with self.subTest(lint=contenu, auteur=a), mock.patch.object(orc, "LINT", faux):
                auteur(a, ok)

    def test_verifier_depot_recalcule_tree_sha256(self):
        """SHOGEN-ENREG-VERIF-1 (ii) : avec --depot, tree.commit ré-extrait et tree.sha256 égal par fichier (attendu :
        sha256 des octets du test) ; refus (tree.sha256) sur un sha changé, un fichier en trop ou en moins, un dépôt
        sans le commit ; servi contrôlé au même dépôt (refus served_from) ; sans --depot, ces copies passent et la CLI
        dit « non recalculé ». Rougit si : --depot ignoré ; clés seules, ou valeurs communes seules, comparées ; autre
        commit ré-extrait ; servi non recalculé ; ré-extraction impossible admise ; option non transmise par la CLI."""
        d, autre = tempfile.mkdtemp(dir=self.d), os.path.join(self.d, "autre-depot")
        list(depot(autre, [{"x": b"x"}]))
        g2 = orc.enregistrer(d, "G2", "claude-opus-5-5", self.depot, self.c1)[0]
        self.assertEqual(orc.verifier(g2, "G2", self.c1, self.depot)["tree"]["sha256"],
                         {k: hashlib.sha256(v).hexdigest() for k, v in OK.items()})
        for i, f in enumerate((lambda t: t.update({"LISEZ-MOI": "0" * 64}), lambda t: t.update({"en-trop": "0" * 64}),
                               lambda t: t.pop("LISEZ-MOI"))):
            p = self.copie(d, g2, f"arbre-{i}.json", lambda r: f(r["tree"]["sha256"]))
            self.assertEqual(orc.verifier(p, "G2", self.c1)["tree"]["commit"], self.c1)
            with self.subTest(i=i), self.assertRaisesRegex(ValueError, r"^refus \(tree\.sha256\) : "):
                orc.verifier(p, "G2", self.c1, self.depot)
        with self.assertRaisesRegex(ValueError, r"^refus \(tree\.sha256\) : .*ré-extraction impossible"):
            orc.verifier(g2, "G2", self.c1, autre)
        sert = {"chemin": "arbre-0.json", "sha256": hashlib.sha256(Path(d, "arbre-0.json").read_bytes()).hexdigest()}
        p = self.copie(d, g2, "sert.json", lambda r: r.update(served_from=sert))
        self.assertEqual(orc.verifier(p, "G2", self.c1)["served_from"], sert)
        with self.assertRaisesRegex(ValueError, r"^refus \(served_from\) : .*refus \(tree\.sha256\)"):
            orc.verifier(p, "G2", self.c1, self.depot)
        for x, code, sortie in ((g2, 0, f"conforme : {g2} (rôle G2, tree.commit {self.c1} ; tree.sha256 recalculé sur "
                                       f"{self.depot})\n"), (Path(d, "arbre-0.json"), 2, "")):
            v = subprocess.run([sys.executable, "-B", OUTIL, "--verifier", x, "--role", "G2", "--commit", self.c1,
                                "--depot", self.depot], capture_output=True, text=True)
            self.assertEqual((v.returncode, v.stdout, "refus (tree.sha256)" in v.stderr), (code, sortie, code == 2))

    def test_delai_depasse_exit_non_nul_enregistrement_ecrit(self):
        """SHOGEN-ENREG-VERIF-1 (iii) : test qui dort 20 s sous un délai de 1 s : commande arrêtée, exit 124 consigné
        dans le run, ligne de dépassement en fin de sortie hachée, enregistrement écrit (exit 1), refus (exit) à la
        lecture ; délai par défaut déclaré (3 600 s) appliqué sans argument ; délai nul, négatif, infini ou NaN refusé
        sans rien écrire ; CLI --delai, refusé avec --verifier. Rougit si : aucun délai, ou défaut non appliqué ;
        dépassement consigné 0 ; enregistrement non écrit ; ligne absente ; option non transmise, ou admise en
        lecture."""
        d = tempfile.mkdtemp(dir=self.d)
        self.assertEqual((orc.DELAI_DEFAUT, orc.EXIT_DELAI), (3600, 124))
        chemin, code = orc.enregistrer(d, "G2", "claude-opus-5-5", self.depot, self.c3, delai=1)
        rec = json.loads(Path(chemin).read_text(encoding="utf-8"))
        out = Path(d, rec["runs"][0]["sortie"]["chemin"]).read_bytes()
        self.assertEqual((code, rec["exit"], rec["runs"][0]["exit"], rec["runs"][0]["sortie"]["sha256"]),
                         (1, 1, 124, hashlib.sha256(out).hexdigest()))
        self.assertTrue(out.endswith("\n[oracle_record] délai maximal de 1 s dépassé : commande arrêtée, exit 124\n"
                                     .encode()), out[-200:])
        with self.assertRaisesRegex(ValueError, r"^refus \(exit\) : "):
            orc.verifier(chemin, "G2", self.c3)
        with mock.patch.object(orc, "DELAI_DEFAUT", 1):
            chemin = orc.enregistrer(d, "G1", "claude-opus-5-5", self.depot, self.c3)[0]
        self.assertEqual(json.loads(Path(chemin).read_text(encoding="utf-8"))["runs"][0]["exit"], 124)
        avant = sorted(os.listdir(d))
        for x in (0, -1, float("inf"), float("nan")):
            with self.subTest(delai=x), self.assertRaisesRegex(ValueError, r"— refus$"):
                orc.enregistrer(d, "cp-2", "claude-opus-5-5", self.depot, self.c1, delai=x)
        self.assertEqual(sorted(os.listdir(d)), avant)
        p, m = (subprocess.run([sys.executable, "-B", OUTIL, *a, "--role", "cp-2", "--commit", self.c3, "--delai", "1"],
                               capture_output=True, text=True) for a in (
            ("--auteur", "claude-opus-5-5", "--depot", self.depot, "--sortie", d), ("--verifier", chemin)))
        self.assertEqual((p.returncode, m.returncode, "--verifier" in m.stderr), (1, 2, True))
        self.assertEqual(json.loads(Path(p.stdout.strip()).read_text(encoding="utf-8"))["runs"][0]["exit"], 124)


    def test_auteur_refuse_a_l_ecriture(self):
        """SHOGEN-ENREG-AUTEUR-ECRITURE-1 : à l'écriture, auteur hors de la liste blanche du lint (identifiant banni, nu
        ou suivi de [1m] ; tier nu ; casse ; autre suffixe ; blanc ; non-chaîne) : refus avant tout git et toute
        commande, rien d'écrit ; identifiant admis suivi de [1m] : écrit et conforme ; CLI : code 2, rien d'écrit.
        Rougit si : contrôle absent à l'écriture ou placé après git, prédicat autre que celui de --verifier."""
        d, x = tempfile.mkdtemp(dir=self.d), "claude-opus-5-5"
        with mock.patch.object(orc, "git", side_effect=AssertionError("git lancé avant le refus")):
            for a in (BANNI, BANNI + "[1m]", "opus", x.upper(), x + "[2m]", " " + x, None, 5):
                with self.subTest(auteur=a), self.assertRaisesRegex(ValueError, r"— refus$"):
                    orc.enregistrer(d, "G2", a, self.depot, self.c1)
        self.assertEqual(os.listdir(d), [])
        p = subprocess.run([sys.executable, "-B", OUTIL, "--role", "G2", "--auteur", BANNI, "--depot", self.depot,
                            "--commit", self.c1, "--sortie", d], capture_output=True, text=True)
        self.assertEqual((p.returncode, "auteur" in p.stderr, os.listdir(d)), (2, True, []))
        chemin = orc.enregistrer(d, "G2", x + "[1m]", self.depot, self.c1)[0]
        self.assertEqual(orc.verifier(chemin, "G2", self.c1)["auteur"], x + "[1m]")

    def test_journaux_substitues_et_arret_au_premier_echec(self):
        """G0 §C (Q5, Q8) : le marqueur JOURNAUX d'une commande de la liste fermée est remplacé par le chemin absolu du
        dossier des journaux (chemin relatif rendu absolu), consigné dans « commande » et reçu par la commande ; sans
        dossier : refus avant toute écriture. Arrêt au premier échec : run en échec, les suivants ne sont pas lancés ;
        sans l'option, ou sans échec, tous le sont. Rougit si : marqueur non remplacé, chemin relatif laissé, dossier
        absent admis, arrêt absent ou inconditionnel."""
        d, jx, dep = tempfile.mkdtemp(dir=self.d), tempfile.mkdtemp(dir=self.d), os.path.join(self.d, "depot-essai")
        ok, ko = depot(dep, [{**x, "s2-harness/tools/rendu_unique.py": STUB} for x in (OK, KO)])
        essai = ["-B", "tools/rendu_unique.py", "--produire", "essai", "--journaux"]
        with mock.patch.dict(orc.COMMANDES, {"essai": ("s2-harness", essai + [orc.JOURNAUX])}):
            with self.assertRaisesRegex(ValueError, r"— refus$"):
                orc.enregistrer(d, "G2", "claude-opus-5-5", dep, ok, commandes=("essai",))
            self.assertEqual(os.listdir(d), [])
            chemin, code = orc.enregistrer(d, "G2", "claude-opus-5-5", dep, ok, commandes=("essai",),
                                           journaux=os.path.relpath(jx))
            run = json.loads(Path(chemin).read_text(encoding="utf-8"))["runs"][0]
            self.assertEqual((code, run["commande"], Path(d, run["sortie"]["chemin"]).read_text(encoding="utf-8")),
                             (0, [sys.executable, "-I", *essai, jx], f"argv {essai[2:] + [jx]}\n"))   # -I : OUT-2d
            for commit, arret, noms in ((ko, True, ["suite"]), (ko, False, ["suite", "essai"]),
                                        (ok, True, ["suite", "essai"])):
                chemin = orc.enregistrer(tempfile.mkdtemp(dir=self.d), "cp-2", "claude-opus-5-5", dep, commit,
                                         ("suite", "essai"), journaux=jx, arret_premier_echec=arret)[0]
                with self.subTest(commit=commit, arret=arret):
                    self.assertEqual([r["nom"] for r in json.loads(Path(chemin).read_text(encoding="utf-8"))["runs"]],
                                     noms)


    def test_suites_s2bis_et_sim_bis_par_la_ligne_du_job(self):
        """SHOGEN-S2BIS-ENREG-ROLE-1 : `suite-s2bis` et `suite-sim-bis` lancent, depuis la racine de l'extraction, la
        ligne du vérificateur de leur job telle qu'écrite dans le gates.yml du commit (plancher committé compris),
        python3 remplacé par l'interpréteur en mode isolé (-I, OUT-1b du lot R-1) ; vérificateur réel du dépôt.
        Conforme : exit 0 et enregistrement conforme ;
        plancher du commit faux : exit 1 consigné ; ligne répétée, job absent, ligne d'une autre suite ou ligne du
        vérificateur de s2bis présente dans le seul job suivant (C-2 de la G2 de la tranche C), leurres C1 (ligne dans
        un bloc `name: >`) et C4 (ligne dans une étape `if: false`), la vraie ligne étant affaiblie
        (SHOGEN-S2BIS-LIGNE-JOB-LEURRE-1), plancher 0 ou à zéro de tête (C-5 (a) de la relecture d'intégration de P1,
        comme K-02 du runner) : refus avant toute écriture ; la CLI admet les deux noms. Rougit si : noms
        hors liste fermée, ligne recopiée dans l'outil, autre job (MR-24 : lecture au-delà du job) ou autre suite lus,
        ligne lue hors d'un bloc `run:` ou dans une étape `if:`, ligne répétée admise, refus après écriture."""
        self.assertLessEqual({"suite-s2bis", "suite-sim-bis"}, set(orc.COMMANDES))      # liste fermée, étendue
        d, dep = tempfile.mkdtemp(dir=self.d), os.path.join(self.d, "depot-s2bis")
        verif = Path(os.path.dirname(HARNESS), "enforcement", "verdict-suite-s2.py").read_bytes()

        v = "          python3 -B enforcement/verdict-suite-s2.py {} --aucun-saut --egal --plancher {}"
        etape, faible = ["        shell: bash", "        run: |"], v.format("s2bis", 0).replace(" --egal", "")

        def gates(p1, p2, n1=1, apres=(), bis=None):               # lignes du vérificateur des deux jobs
            return chr(10).join(["jobs:", "  s2bis-unittest:", "    steps:", *(bis or ["      - name: suite", *etape, *[
                v.format("s2bis", p1)] * n1]), "  sim-bis-unittest:", "    steps:", "      - name: suite", *etape,
                                 v.format("scripts/sim-bis", p2), *apres, ""]).encode()
        base = {"enforcement/verdict-suite-s2.py": verif, **{f"{x}/tests/{n}": c for x in (
            "s2bis", "scripts/sim-bis", "s2-harness") for n, c in (("__init__.py", b""), ("test_t.py", T))}}
        autre = gates(1, 1).replace(b"verdict-suite-s2.py s2bis ", b"verdict-suite-s2.py s2-harness ")
        loin = gates(1, 1, 0, [v.format("s2bis", 1)])               # ligne de s2bis dans le seul job suivant (C-2)
        c1 = gates(1, 1, bis=["      - name: >", v.format("s2bis", 1), *etape, faible])
        c4 = gates(1, 1, bis=["      - name: leurre", "        if: false", *etape, v.format("s2bis", 1),
                              "      - name: suite", *etape, faible])
        complaisant = chr(10).join(["import re", "lignes_du_job = lambda t, j, m: [x.strip() for x in t.split(chr(10))"
                                    " if re.fullmatch(m, x.strip())]", ""]).encode()   # analyseur complaisant du commit
        ok, ko, double, sans, mauvaise, suivant, zero, zero7, leurre1, leurre4 = depot(dep, [
            {**base, ".github/workflows/gates.yml": g} for g in (gates(1, 1), gates(2, 1), gates(1, 1, 2), gates(
                1, 1).split(b"  sim-bis")[0], autre, loin, gates(0, 1), gates(1, "07"))] + [
                {**base, ".github/workflows/gates.yml": c1, "enforcement/verdict-suite-s2.py": complaisant},
                {**base, ".github/workflows/gates.yml": c4}])
        chemin, code = orc.enregistrer(d, "G2", "claude-opus-5-5", dep, ok, ("suite-s2bis", "suite-sim-bis"))
        rec = json.loads(Path(chemin).read_text(encoding="utf-8"))
        ligne = [sys.executable, "-I", "-B", "enforcement/verdict-suite-s2.py", "{}", "--aucun-saut", "--egal",
                 "--plancher", "1"]                                 # -I : OUT-1b (lot R-1)
        self.assertEqual((code, [(r["nom"], r["arbre"], r["commande"], r["exit"]) for r in rec["runs"]]), (0, [
            ("suite-s2bis", ".", [x.format("s2bis") for x in ligne], 0),
            ("suite-sim-bis", ".", [x.format("scripts/sim-bis") for x in ligne], 0)]))
        for r in rec["runs"]:
            self.assertIn(b"verdict-suite-s2 : conforme (code 0, r", Path(d, r["sortie"]["chemin"]).read_bytes())
        self.assertEqual(orc.verifier(chemin, "G2", ok, dep)["tree"]["commit"], ok)
        chemin, code = orc.enregistrer(d, "G2", "claude-opus-5-5", dep, ko, ("suite-s2bis", "suite-sim-bis"))
        self.assertEqual((code, [r["exit"] for r in json.loads(Path(chemin).read_text(encoding="utf-8"))["runs"]]),
                         (1, [1, 0]))                               # Ran 1 < plancher 2 du commit
        avant = sorted(os.listdir(d))
        for commit, c in ((double, "suite-s2bis"), (sans, "suite-sim-bis"), (mauvaise, "suite-s2bis"),
                          (suivant, "suite-s2bis"), (leurre1, "suite-s2bis"), (leurre4, "suite-s2bis"),
                          (zero, "suite-s2bis"), (zero7, "suite-sim-bis")):
            with self.subTest(commande=c), self.assertRaisesRegex(ValueError, "— refus$"):
                orc.enregistrer(d, "cp-2", "claude-opus-5-5", dep, commit, ("suite", c))
        self.assertEqual(sorted(os.listdir(d)), avant)
        p = subprocess.run([sys.executable, "-B", OUTIL, "--role", "G1", "--auteur", "claude-opus-5-5", "--depot", dep,
                            "--commit", ok, "--sortie", d, "--commande", "suite-sim-bis"], capture_output=True,
                           text=True)
        self.assertEqual((p.returncode, p.stderr), (0, ""))


    def test_verificateur_du_commit_egal_a_celui_de_l_outil(self):
        """SHOGEN-S2BIS-ENREG-VERIF-COMMIT-1 (lot R-1, OUT-1b) : pour une commande de JOBS, le vérificateur du commit
        (sha256 consigné dans tree.sha256) doit être celui de l'outil (VERIF). Leurre L2 de la G2 d'intégration de P1
        (vérificateur complaisant, test rouge) : refus nommé avant toute écriture ; à la lecture, tree.sha256 qui porte
        un autre vérificateur : refus (vérificateur). Vérificateur égal, module subprocess.py posé à côté par le
        commit : vérificateur lancé en -I, module sans effet, exit 1 consigné. ligne_du_job : exception au chargement
        de l'analyseur (RuntimeError, SystemExit) ou gates.yml non UTF-8 : refus qui la nomme. Rougit si :
        comparaison absente, sur un autre fichier ou après l'écriture ; lecture sans ce contrôle ; -I retiré ;
        exception au chargement non rattrapée ou non nommée."""
        d, dep, a = tempfile.mkdtemp(dir=self.d), os.path.join(self.d, "depot-verif"), "claude-opus-5-5"
        cle, verif, nl = "enforcement/verdict-suite-s2.py", Path(orc.VERIF).read_bytes(), chr(10)
        gates = nl.join(["jobs:", "  s2bis-unittest:", "    steps:", "      - name: suite", "        shell: bash",
                         "        run: |", "          python3 -B " + cle + " s2bis --aucun-saut --egal --plancher 1",
                         ""]).encode()
        faux = nl.join(["import sys", "print('verdict-suite-s2 : conforme')", "sys.exit(0)", ""]).encode()   # L2
        masque = nl.join(["class P:", "    returncode, stdout = 0, b''", "    stderr = (chr(10) + '-' * 70 + chr(10) + "
                          "'Ran 1 test in 0.001s' + chr(10) * 2 + 'OK' + chr(10)).encode()", "", "",
                          "def run(*a, **k):", "    return P()", ""]).encode()    # subprocess complaisant
        base = {".github/workflows/gates.yml": gates, "s2bis/tests/__init__.py": b"", cle: verif}
        rouge = T.replace(b"pass", b"self.fail()")
        honnete, l2, cache = depot(dep, [{**base, "s2bis/tests/test_t.py": T},
                                         {**base, "s2bis/tests/test_t.py": rouge, cle: faux},
                                         {**base, "s2bis/tests/test_t.py": rouge, "enforcement/subprocess.py": masque}])
        chemin, code = orc.enregistrer(d, "G2", a, dep, honnete, ("suite-s2bis",))
        self.assertEqual((code, json.loads(Path(chemin).read_text(encoding="utf-8"))["tree"]["sha256"][cle],
                          orc.verifier(chemin, "G2", honnete, dep)["exit"]), (0, hashlib.sha256(verif).hexdigest(), 0))
        avant = sorted(os.listdir(d))
        with self.assertRaisesRegex(ValueError, rf"^vérificateur du commit {cle} .* — refus$"):
            orc.enregistrer(d, "G2", a, dep, l2, ("suite-s2bis",))
        self.assertEqual(sorted(os.listdir(d)), avant)
        c, code = orc.enregistrer(d, "G2", a, dep, cache, ("suite-s2bis",))
        run = json.loads(Path(c).read_text(encoding="utf-8"))["runs"][0]
        self.assertEqual((code, run["exit"], run["commande"][:4]), (1, 1, [sys.executable, "-I", "-B", cle]))
        p = self.copie(d, chemin, "autre.json", lambda r: r["tree"]["sha256"].update({cle: hashlib.sha256(
            faux).hexdigest()}))
        with self.assertRaisesRegex(ValueError, r"^refus \(vérificateur\) : "):
            orc.verifier(p, "G2", honnete)
        arbre = os.path.join(d, "arbre")
        os.makedirs(os.path.join(arbre, ".github", "workflows"))
        Path(arbre, ".github", "workflows", "gates.yml").write_bytes(gates)
        for nom, corps, motif in (("leve.py", "raise RuntimeError('analyseur')", "RuntimeError"),
                                  ("sort.py", "import sys" + nl + "sys.exit(0)", "SystemExit")):
            Path(d, nom).write_text(corps + nl, encoding="utf-8")
            with self.subTest(analyseur=nom), mock.patch.object(orc, "VERIF", os.path.join(d, nom)):
                with self.assertRaisesRegex(ValueError, rf"{motif}.* — refus$"):
                    orc.ligne_du_job(arbre, "s2bis-unittest", "s2bis")
        Path(arbre, ".github", "workflows", "gates.yml").write_bytes(bytes([255]) + gates)
        with self.assertRaisesRegex(ValueError, r"UnicodeDecodeError.* — refus$"):
            orc.ligne_du_job(arbre, "s2bis-unittest", "s2bis")

    def test_racine_de_suite_qui_masque_la_bibliotheque_standard(self):
        """SHOGEN-S2BIS-SUITE-MASQUE-UNITTEST-1 (lot OUT-2, OUT-2b) : un unittest.py à la racine d'une suite, qui
        imprime un résumé conforme et sort en 0, masquerait le module standard pour -m unittest. Commande `suite`
        (unittest lancé par l'outil, sans le vérificateur) : refus nommé avant tout run, rien d'écrit ; commande
        `suite-s2bis` (ligne du job, vérificateur égal à VERIF) : refus nommé du vérificateur, suite non lancée, exit 1
        consigné, refus (exit) à la lecture ; `masques` : noms de modules standard seuls (paquet compris), triés.
        Rougit si : contrôle absent, sur un autre dossier ou après le run, ou limité à `suite` en première commande
        (C-3 de la G2 d'OUT-2) ; vérificateur sans ce refus ; règle de `masques` réduite à unittest, au nom complet,
        au nom pris avant le dernier point (json.abi3.so, C-2), ou élargie à tout module."""
        d, dep, a, nl = tempfile.mkdtemp(dir=self.d), os.path.join(self.d, "depot-masque"), "claude-opus-5-5", chr(10)
        leurre = nl.join(["import sys", "sys.stderr.write(chr(10) + '-' * 70 + chr(10) + 'Ran 1 test in 0.001s' + "
                          "chr(10) * 2 + 'OK' + chr(10))", "sys.exit(0)", ""]).encode()      # résumé conforme forgé
        gates = nl.join(["jobs:", "  s2bis-unittest:", "    steps:", "      - name: suite", "        shell: bash",
                         "        run: |", "          python3 -B enforcement/verdict-suite-s2.py s2bis --aucun-saut "
                         "--egal --plancher 1", ""]).encode()
        s2, s2bis = depot(dep, [{**KO, "s2-harness/unittest.py": leurre}, {
            ".github/workflows/gates.yml": gates, "enforcement/verdict-suite-s2.py": Path(orc.VERIF).read_bytes(),
            "s2bis/tests/__init__.py": b"", "s2bis/tests/test_t.py": KO["s2-harness/tests/test_t.py"],
            "s2bis/unittest.py": leurre}])
        avant = sorted(os.listdir(d))
        with self.assertRaisesRegex(ValueError, "unittest[.]py.* — refus$"):
            orc.enregistrer(d, "G2", a, dep, s2)
        with self.assertRaisesRegex(ValueError, "unittest[.]py.* — refus$"):          # `suite` après une autre (C-3)
            orc.enregistrer(d, "G2", a, dep, s2bis, ("suite-s2bis", "suite"))
        self.assertEqual(sorted(os.listdir(d)), avant)
        chemin, code = orc.enregistrer(d, "G2", a, dep, s2bis, ("suite-s2bis",))
        run = json.loads(Path(chemin).read_text(encoding="utf-8"))["runs"][0]
        out = Path(d, run["sortie"]["chemin"]).read_text(encoding="utf-8")
        self.assertEqual((code, run["exit"], "masque la bibliothèque standard" in out, "Ran 1 test" in out),
                         (1, 1, True, False))
        with self.assertRaisesRegex(ValueError, "^refus [(]exit[)] : "):
            orc.verifier(chemin, "G2", s2bis)
        racine = os.path.join(d, "racine")
        os.makedirs(os.path.join(racine, "argparse"))
        for n in ("unittest.py", "json.py", "json.abi3.so", "commun.py", "unittest_notes.md", "README.md"):
            Path(racine, n).write_bytes(b"")
        self.assertEqual(orc.masques(racine), ["argparse", "json.abi3.so", "json.py", "unittest.py"])    # à la main

    def test_commandes_hors_suite_en_mode_isole(self):
        """SHOGEN-S2BIS-SCRIPT-MASQUE-1 (lot OUT-2, OUT-2d) : toute commande autre que `suite` (production, JOBS) est
        lancée en mode isolé (-I, consigné dans « commande ») : un json.py posé à côté du script lancé (tools/) n'est
        pas importé, la sortie est celle du vrai module. Rougit si : -I réservé à JOBS, ou retiré."""
        d, dep, nl = tempfile.mkdtemp(dir=self.d), os.path.join(self.d, "depot-isole"), chr(10)
        essai = ["-B", "tools/rendu_unique.py", "--produire", "essai"]
        (isole,) = depot(dep, [{**OK, "s2-harness/tools/rendu_unique.py": nl.join([
            "import json, sys", "print(json.dumps(sys.argv[1:]))", ""]).encode(), "s2-harness/tools/json.py": nl.join([
                "def dumps(x):", "    return 'masqué'", ""]).encode()}])
        with mock.patch.dict(orc.COMMANDES, {"essai": ("s2-harness", essai)}):
            chemin, code = orc.enregistrer(d, "G2", "claude-opus-5-5", dep, isole, ("essai",))
        run = json.loads(Path(chemin).read_text(encoding="utf-8"))["runs"][0]
        self.assertEqual((code, run["commande"], Path(d, run["sortie"]["chemin"]).read_text(encoding="utf-8")),
                         (0, [sys.executable, "-I", *essai], '["--produire", "essai"]' + nl))

    def test_racine_de_s2_harness_masquee_refusee_pour_toute_commande(self):
        """SHOGEN-S2BIS-SCRIPT-MASQUE-1 (OUT-2d) : la production met la racine s2-harness en tête de sys.path
        (rendu_unique.py) ; -I ne l'écarte pas (mesuré, D-P3 du lot) : une entrée de cette racine au nom d'un module
        standard est refusée, nommée, avant tout run, pour toute commande lancée dans s2-harness, même sans `suite` ;
        rien d'écrit. Rougit si : contrôle de la racine réservé à la commande `suite`."""
        d, dep = tempfile.mkdtemp(dir=self.d), os.path.join(self.d, "depot-racine")
        (racine,) = depot(dep, [{**OK, "s2-harness/tools/rendu_unique.py": STUB, "s2-harness/dataclasses.py": b""}])
        with mock.patch.dict(orc.COMMANDES, {"essai": ("s2-harness", ["-B", "tools/rendu_unique.py"])}):
            with self.assertRaisesRegex(ValueError, "'dataclasses[.]py'. à la racine de s2-harness .* — refus$"):
                orc.enregistrer(d, "G2", "claude-opus-5-5", dep, racine, ("essai",))
        self.assertEqual(os.listdir(d), [])

    def test_bytecode_committe_refuse_pour_toute_commande(self):
        """SHOGEN-S2BIS-SCRIPT-MASQUE-1 (OUT-2d) : un fichier de bytecode committé (__pycache__, .pyc) remplacerait la
        source relue à l'import (.pyc à invalidation non vérifiée : mesuré, D-P4 et D-U1 du lot) et l'isolement ne
        l'écarte pas : refus nommé avant tout run, quelle que soit la commande, rien d'écrit ; cache d'un __pycache__,
        ou module sans source (tests/aide.pyc, seul fichier compilé de son commit). SHOGEN-S2BIS-SUITE-CODE-COMPILE-1
        (OUT-2h) : de même tests/aide.pyo, et les extensions tests/aide.so (suffixe nu) et tests/aide.pyd, chacun seul
        dans son commit ; COMPILES, liste écrite ici à la main. Rougit si : contrôle absent, réservé à une commande, ou
        au cache d'un __pycache__ (C-3 de la revue de la vague 2) ; suffixe .pyo, .so, .pyd ou d'extension omis."""
        dep, sans = os.path.join(self.d, "depot-pyc"), os.path.join(self.d, "depot-pyc-sans-source")
        (pyc,) = depot(dep, [{**OK, "s2-harness/tools/rendu_unique.py": STUB,
                              "s2-harness/tests/__pycache__/test_t.cpython-312.pyc": b"leurre"}])
        (seul,) = depot(sans, [{**OK, "s2-harness/tools/rendu_unique.py": STUB, "s2-harness/tests/aide.pyc": b"x"}])
        cas = [(dep, pyc, "'s2-harness/tests/__pycache__/test_t[.]cpython-312[.]pyc'"),
               (sans, seul, "'s2-harness/tests/aide[.]pyc'")]
        for s in (".pyo", ".so", ".pyd"):
            dp = os.path.join(self.d, "depot-compile" + s)
            (commit,) = depot(dp, [{**OK, "s2-harness/tools/rendu_unique.py": STUB, "s2-harness/tests/aide" + s: b"x"}])
            cas.append((dp, commit, f"'s2-harness/tests/aide[.]{s[1:]}'"))
        with mock.patch.dict(orc.COMMANDES, {"essai": ("s2-harness", ["-B", "tools/rendu_unique.py"])}):
            for dp, commit, motif in cas:
                for c in ("suite", "essai"):
                    d = tempfile.mkdtemp(dir=self.d)
                    with self.subTest(commande=c, motif=motif):
                        with self.assertRaisesRegex(ValueError, motif + ".* — refus$"):
                            orc.enregistrer(d, "G2", "claude-opus-5-5", dp, commit, (c,))
                        self.assertEqual(os.listdir(d), [])
        self.assertEqual(orc.COMPILES, (".pyc", ".pyo", ".so", ".pyd", *importlib.machinery.EXTENSION_SUFFIXES))

    def test_verificateur_de_l_outil_lu_dans_sa_source(self):
        """SHOGEN-S2BIS-SCRIPT-MASQUE-1 (OUT-2d) : ligne_du_job exécute VERIF depuis sa source ; un .pyc à
        invalidation non vérifiée posé dans son __pycache__ (analyseur complaisant) est ignoré : job absent du
        gates.yml, refus. Rougit si : VERIF chargé par le chargeur d'import (exec_module), qui lit ce .pyc."""
        d, nl = tempfile.mkdtemp(dir=self.d), chr(10)
        v, src = os.path.join(d, "enforcement", "verdict-suite-s2.py"), os.path.join(d, "complaisant.py")
        os.makedirs(os.path.join(d, "arbre", ".github", "workflows"))
        Path(d, "arbre", ".github", "workflows", "gates.yml").write_text("jobs:" + nl, encoding="utf-8")
        os.makedirs(os.path.dirname(v))
        shutil.copy(orc.VERIF, v)
        Path(src).write_text(nl.join(["def lignes_du_job(t, j, m):", "    return ['x --plancher 9']", ""]),
                             encoding="utf-8")
        py_compile.compile(src, importlib.util.cache_from_source(v), doraise=True,
                           invalidation_mode=py_compile.PycInvalidationMode.UNCHECKED_HASH)
        with mock.patch.object(orc, "VERIF", v), self.assertRaisesRegex(ValueError, "^job s2bis-unittest absent"):
            orc.ligne_du_job(os.path.join(d, "arbre"), "s2bis-unittest", "s2bis")

    def test_verifier_refuse_un_arbre_qui_porte_un_masque(self):
        """SHOGEN-S2BIS-MASQUES-LECTURE-1 (lot OUT-2, OUT-2f) : la lecture refuse, nommément (masque), un
        enregistrement dont l'arbre (tree.sha256) porte, à la racine de la suite d'un run (s2-harness pour `suite` et la
        production, dossier de la suite pour JOBS), une entrée au nom d'un module standard, ou un fichier de bytecode.
        E7 de la G2 d'OUT-2 : enregistrement `suite` d'un commit dont la racine est masquée (écrit par un outil d'avant
        OUT-2b ; tree.sha256 juste, recalculé avec --depot) ; paquet json/ à la racine de s2bis pour `suite-s2bis` ;
        .pyc de cache, ou sans source (C-3 de la revue de la vague 2) ; .pyo, extension .so ou .pyd (OUT-2h). Témoin :
        masque hors de la racine d'un run lancé (s2bis/ pour `suite`, tools/), conforme. Rougit si : contrôle absent ;
        racine des JOBS, paquet, ou fichier compilé (cache, module sans source, .pyo, extension), non lus ; contrôle
        étendu aux racines d'aucun run."""
        d, dep, nl = tempfile.mkdtemp(dir=self.d), os.path.join(self.d, "depot-lecture"), chr(10)
        masque = {**OK, "s2-harness/unittest.py": nl.join(["import sys", "sys.exit(0)", ""]).encode()}
        (sale,) = depot(dep, [masque])
        g2 = orc.enregistrer(d, "G2", "claude-opus-5-5", self.depot, self.c1)[0]
        e7 = self.copie(d, g2, "e7.json", lambda r: r["tree"].update(commit=sale, sha256={
            k: hashlib.sha256(x).hexdigest() for k, x in masque.items()}))
        verif = {orc.VERIF_COMMIT: hashlib.sha256(Path(orc.VERIF).read_bytes()).hexdigest()}
        jobs = self.copie(d, g2, "jobs.json", lambda r: (r["runs"][0].update(nom="suite-s2bis"), r["tree"][
            "sha256"].update({**verif, "s2bis/json/__init__.py": "0" * 64})))                     # paquet masquant
        pyc = self.copie(d, g2, "pyc.json", lambda r: r["tree"]["sha256"].update({
            "s2-harness/tests/__pycache__/test_t.cpython-312.pyc": "0" * 64}))
        seul = self.copie(d, g2, "pyc-sans-source.json", lambda r: r["tree"]["sha256"].update({
            "s2-harness/tests/aide.pyc": "0" * 64}))                         # module sans source, seul compilé (C-3)
        temoin = self.copie(d, g2, "temoin.json", lambda r: r["tree"]["sha256"].update({
            "s2bis/json.py": "0" * 64, "s2-harness/tools/json.py": "0" * 64}))
        compiles = [self.copie(d, g2, f"compile{s}.json", lambda r, s=s: r["tree"]["sha256"].update({
            "s2-harness/tests/aide" + s: "0" * 64})) for s in (".pyo", ".so", ".pyd")]     # OUT-2h, un par copie
        for p, commit, depot_ in ((e7, sale, dep), (jobs, self.c1, None), (pyc, self.c1, None), (seul, self.c1, None),
                                  *((x, self.c1, None) for x in compiles)):
            with self.subTest(enregistrement=os.path.basename(p)), self.assertRaisesRegex(ValueError,
                                                                                          "^refus [(]masque[)] : "):
                orc.verifier(p, "G2", commit, depot_)
        self.assertEqual(orc.verifier(temoin, "G2", self.c1)["tree"]["commit"], self.c1)


if __name__ == "__main__":
    unittest.main()
