"""Adaptateur d'oracle croisé avec RECALC-BIS, SB-13 première passe (E-S-01, E-S-51 ; SHOGEN-SIM-BIS-CONTRAT-RB6-1).
SB-13a : épingles du paquet s2bis au commit f458980 égales aux valeurs de `git show f458980:s2bis/<chemin> | sha256sum`
(rotation.py : 4183fbe6…, l'empreinte que cite le contre-contrôle de la tranche 3), extraction, refus nommés d'une
épingle fausse et d'un commit absent, frontière d'E-S-01 lue par `ast`. SB-13b : chargement sous shogen_s2bis.
Chaque test nomme les mutations qui le rougissent."""
import ast
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

import commun
import oracle_recalc
from tests import test_fitness, test_fitness_tirages

PRM = commun.charger_parametres(environ={})
COMMIT = "f45898040e10858d5f7ed8944ad66f5ec7e9bdde"
FICHIERS = {"config/analyse.json": "e9243c79ff942c3444fbd93495644b6b5556435fe193a0f959ad1708233a1d00",
            "shogen_s2bis/__init__.py": "3908b0944bac803df5d2e447dddc9344d5dc61db2e5531d729b5c926425762d8",
            "shogen_s2bis/recalc/__init__.py": "42e2623a7d8fd15b6a90aeb4b7551bc45198df176187af526e7657cd12ca78d1",
            "shogen_s2bis/recalc/config_analyse.py": "82abdba525d90c829998dd4539b7fb16b9366e4599f33d13c3916f155bcd8b26",
            "shogen_s2bis/recalc/rotation.py": "4183fbe6bf633f394e8d289066c0dd0323cfa5561f173b54b15b9f0ad13a4202",
            "tests/test_rotation.py": "049e0b5165450011b8870e03660465de546bdf573516e13c4bc46287dfa8dc0a"}


class TestExtraction(unittest.TestCase):
    def test_epingles(self):
        """Section « oracle_recalc » : commit f458980 complet, dossier s2bis, six empreintes égales aux valeurs de
        sha256sum. Mutations M-13A-01 (empreinte de rotation.py de RB-6b, 7ff0d437…), M-13A-02 (commit de RB-6b)."""
        o = PRM["oracle_recalc"]
        self.assertEqual((o["commit"], o["dossier"], o["fichiers"]), (COMMIT, "s2bis", FICHIERS))

    def test_extraction(self):
        """extraire écrit sous le dossier donné les six fichiers épinglés, et eux seuls, aux empreintes de sha256sum ;
        il rend le dossier s2bis de l'extraction. Mutations M-13A-03 (dossier rendu sans s2bis), M-13A-04 (dernier
        fichier non écrit), M-13A-05 (fichier tronqué d'un octet à l'écriture)."""
        with tempfile.TemporaryDirectory() as d:
            racine = oracle_recalc.extraire(PRM, d)
            ecrits = sorted(os.path.relpath(os.path.join(x, f), racine) for x, _s, fs in os.walk(d) for f in fs)
            lus = {}
            for f in ecrits:
                with open(os.path.join(racine, f), "rb") as g:
                    lus[f] = hashlib.sha256(g.read()).hexdigest()
        self.assertEqual((racine, lus), (os.path.join(d, "s2bis"), FICHIERS))

    def test_schema(self):
        """Commit abrégé, en majuscules ou de 41 caractères, fichier en moins ou en plus, empreinte en majuscules :
        PARAMETRES/schema. Mutations M-13A-06 (commit non contraint), M-13A-07 (fichiers non contraints)."""
        for f in (lambda o: o.update(commit="f458980"), lambda o: o.update(commit=COMMIT.upper()),
                  lambda o: o.update(commit=COMMIT + "0"), lambda o: o["fichiers"].pop("config/analyse.json"),
                  lambda o: o["fichiers"].update({"shogen_s2bis/collecte/config.py": "0" * 64}),
                  lambda o: o["fichiers"].update({"config/analyse.json": FICHIERS["config/analyse.json"].upper()})):
            p = json.loads(json.dumps(PRM))
            f(p["oracle_recalc"])
            with self.assertRaises(commun.Refus) as c:
                commun.controler(p, commun.SCHEMA)
            self.assertEqual(c.exception.code, "PARAMETRES/schema")

    def test_refus(self):
        """Variable de la copie scellée posée : CAMPAGNE/variable (E-S-02) ; empreinte fausse : ORACLE/sha256 ; commit
        absent, fichier absent du commit (2fe7d9c, RB-0a : sous-paquet recalc sans rotation.py), dépôt sans git :
        ORACLE/extraction. Mutations M-13A-08 (empreintes non contrôlées), M-13A-09 (sortie de git non contrôlée),
        M-13A-10 (garde de campagne retirée)."""
        with mock.patch.object(commun.os, "environ", {commun.VARIABLE: ""}), tempfile.TemporaryDirectory() as d:
            with self.assertRaises(commun.Refus) as c:
                oracle_recalc.extraire(PRM, d)
            self.assertEqual(c.exception.code, "CAMPAGNE/variable")
        o = PRM["oracle_recalc"]
        for faux, depot, code in ((dict(o, fichiers=dict(FICHIERS, **{"config/analyse.json": "0" * 64})), commun.RACINE,
                                   "ORACLE/sha256"),
                                  (dict(o, commit="0" * 40), commun.RACINE, "ORACLE/extraction"),
                                  (dict(o, commit="2fe7d9c56f63471d61ef5d5371f41a4a90002266"), commun.RACINE,
                                   "ORACLE/extraction"),
                                  (o, os.path.join(commun.RACINE, "inexistant"), "ORACLE/extraction")):
            with tempfile.TemporaryDirectory() as d, self.assertRaises(commun.Refus) as c:
                oracle_recalc.extraire(dict(PRM, oracle_recalc=faux), d, depot)
            self.assertEqual(c.exception.code, code, faux["commit"][:8])

    def test_frontiere_e_s_01(self):
        """E-S-01 : oracle_recalc.py présent et adaptateur pour les deux gardes `ast` (frontière et tirages) ; ses
        imports écrits : bibliothèque standard et modules du moteur seuls (le paquet s2bis n'entre que par l'extraction
        épinglée) ; un module du moteur qui l'importe est refusé. Mutations M-13A-11 (import shogen_s2bis écrit dans
        l'adaptateur), M-13A-12 (oracle_recalc.py hors des adaptateurs de test_fitness_tirages)."""
        f = "oracle_recalc.py"
        self.assertTrue(os.path.exists(os.path.join(commun.ICI, f)))
        self.assertIn(f, test_fitness.ORACLES & test_fitness_tirages.ORACLES)
        with open(os.path.join(commun.ICI, f), encoding="utf-8") as g:
            arbre = ast.parse(g.read())
        noms = {a.name.split(".")[0] for n in ast.walk(arbre) if isinstance(n, ast.Import) for a in n.names}
        noms |= {n.module.split(".")[0] for n in ast.walk(arbre) if isinstance(n, ast.ImportFrom)}
        moteur = {x[:-3] for x in os.listdir(commun.ICI) if x.endswith(".py") and x not in test_fitness.ORACLES}
        self.assertEqual(sorted(x for x in noms if x not in sys.stdlib_module_names and x not in moteur), [])
        self.assertNotEqual(test_fitness.refus_imports("import oracle_recalc", moteur | {"oracle_recalc"}), [])


H = oracle_recalc.charger(PRM)


def processus(lignes: list, tmpdir=None) -> subprocess.CompletedProcess:
    """Processus neuf lancé depuis le dossier du lot, sans la variable de campagne (TMPDIR donné le cas échéant)."""
    env = {k: v for k, v in os.environ.items() if k != commun.VARIABLE}
    if tmpdir:
        env["TMPDIR"] = tmpdir
    return subprocess.run([sys.executable, "-B", "-c", chr(10).join(lignes)], cwd=commun.ICI, env=env,
                          capture_output=True, text=True, timeout=120)


class TestChargement(unittest.TestCase):
    def test_modules_charges(self):
        """charger rend rotation et config_analyse, chargés sous shogen_s2bis.recalc depuis un dossier
        « oracle_recalc_… » de TMPDIR, et analyse.json lu (bloc rotations R = 9 999, seuil = 99, lu à la main).
        Mutations M-13B-01 (modules chargés sous un autre nom), M-13B-02 (analyse.json non lu)."""
        d = os.path.join(tempfile.gettempdir(), "oracle_recalc_")
        self.assertEqual((sorted(H), H["rotation"].__name__, H["config_analyse"].__name__, H["analyse"]["rotations"],
                          [H[m].__file__.startswith(d) for m in ("rotation", "config_analyse")]),
                         (["analyse", "config_analyse", "rotation"], "shogen_s2bis.recalc.rotation",
                          "shogen_s2bis.recalc.config_analyse", {"R": 9999, "seuil": 99}, [True, True]))

    def test_nettoyage_du_dossier(self):
        """Dans un processus neuf, à TMPDIR vide (E-S-06) : un seul dossier « oracle_recalc_… », d'où rotation est
        chargée, retiré à la sortie du processus. Mutation M-13B-03 (dossier jamais retiré)."""
        code = ["import os, tempfile, commun, oracle_recalc",
                "h = oracle_recalc.charger(commun.charger_parametres(environ={}))",
                "d = tempfile.gettempdir()",
                "print(sorted(x[:14] for x in os.listdir(d)), h['rotation'].__file__.startswith(d))"]
        with tempfile.TemporaryDirectory() as d:
            p = processus(code, d)
            self.assertEqual((p.stdout.strip(), os.listdir(d)), ("['oracle_recalc_'] True", []), p.stderr[-300:])

    def test_cache_indexe_sur_l_epingle(self):
        """Même épingle (source changée), mêmes modules sans nouvelle extraction ; autre commit, autre dossier ou autre
        empreinte : ORACLE/epingle. Mutations M-13B-04 (épingle non comparée), M-13B-05 (empreintes hors de
        l'épingle), M-13B-06 (source dans l'épingle), M-13B-07 (extraction refaite à chaque appel)."""
        o = PRM["oracle_recalc"]
        self.assertIs(oracle_recalc.charger(dict(PRM, oracle_recalc=dict(o, source="autre")))["rotation"],
                      H["rotation"])
        for faux in (dict(o, commit="0" * 40), dict(o, dossier="ailleurs"),
                     dict(o, fichiers=dict(o["fichiers"], **{"shogen_s2bis/recalc/rotation.py": "0" * 64}))):
            with self.assertRaises(commun.Refus) as c:
                oracle_recalc.charger(dict(PRM, oracle_recalc=faux))
            self.assertEqual(c.exception.code, "ORACLE/epingle")

    def test_modules_hors_epingles(self):
        """Dans un processus neuf : un shogen_s2bis déjà chargé d'ailleurs, ou un module shogen_s2bis.* hors des
        fichiers épinglés : ORACLE/modules. Mutations M-13B-08 (contrôle des modules chargés retiré), M-13B-09
        (shogen_s2bis déjà chargé admis), M-13B-10 (modules chargés comptés sur le seul paquet de tête)."""
        for intrus in ("shogen_s2bis", "shogen_s2bis.intrus"):
            code = ["import sys, types", f"m = types.ModuleType({intrus!r})", "m.__file__ = '/hors/x.py'",
                    f"sys.modules[{intrus!r}] = m", "import commun, oracle_recalc", "try:",
                    "    oracle_recalc.charger(commun.charger_parametres(environ={}))",
                    "except commun.Refus as e:", "    print(e.code)"]
            p = processus(code)
            self.assertEqual(p.stdout.strip(), "ORACLE/modules", (intrus, p.stderr[-300:]))

    def test_analyse_lu_dans_l_extraction(self):
        """C-6 de la G2 (O-1) : dans un processus neuf, config/analyse.json est écrit puis lu en octets dans le dossier
        s2bis extrait du commit épinglé, jamais dans l'arbre de travail (dont les octets sont aujourd'hui les mêmes) :
        fichiers ouverts par builtins.open pendant charger, relevés avec leur mode. Mutations M-G2-12 (lu sous
        commun.RACINE), M-13B-13 (lu par un chemin tiré de commun.ICI), M-13B-14 (arbre de travail préféré s'il
        existe)."""
        code = ["import builtins, os, commun, oracle_recalc", "lus, vrai = [], builtins.open",
                "def ouvrir(f, mode='r', *a, **k):", "    lus.append((os.path.realpath(f), mode))",
                "    return vrai(f, mode, *a, **k)", "builtins.open = ouvrir",
                "h = oracle_recalc.charger(commun.charger_parametres(environ={}))", "builtins.open = vrai",
                "s2bis = os.path.realpath(os.path.join(os.path.dirname(h['rotation'].__file__), '..', '..'))",
                "print(sorted((os.path.relpath(f, s2bis), m) for f, m in lus if f.endswith('analyse.json')))"]
        p = processus(code)
        self.assertEqual(p.stdout.strip(), "[('config/analyse.json', 'rb'), ('config/analyse.json', 'wb')]",
                         p.stderr[-300:])


if __name__ == "__main__":
    unittest.main()
