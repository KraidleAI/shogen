"""Adaptateur d'oracle r1 SB-14 (E-S-01, E-S-39 ; T-FIV-1, T-CAL-2 ; SHOGEN-SIM-BIS-WINDOW-EPINGLE-1) : épingles des
cinq modules du harnais de f35a70c égales à celles de PLAN-S2BIS (scripts/plan-s2bis/parametres.json) et, pour
window.py, à `git show f35a70c:s2-harness/shogen_s2/window.py | sha256sum` ; refus nommés d'une épingle fausse et d'un
commit absent ; FIV_série de r1 extrait égal à calib_fiv sur la même entrée (série de la fixture de PLAN-S2BIS, série
à lacune, 10 réplications d'E1) ; l'écart mesuré est le nombre de valeurs différentes, déclaré nul. T-CAL-2 contre
window extrait : tests/test_calendrier.py. Chaque test nomme les mutations qui le rougissent."""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from fractions import Fraction

import calib_fiv
import calibration
import commun
import oracle_r1

PRM = commun.charger_parametres(environ={})
K_ = PRM["calibration"]
H = oracle_r1.charger(PRM)
COMMIT = "f35a70c19ba8269f1f7e2bcd31775e4fc513da20"
WINDOW = "f8c3b79f7f7893f343a00b6d6563cbbb502e2bd7af7888db958f895b5bc5fb94"
CHAMPS = ("n", "K", "numerateur", "gamma0", "sigma2_bloc", "FIV_serie")


def bits(*positions):
    return sum(1 << p for p in positions)


def ecarts(pres, val, ells):
    """Valeurs (champ, ℓ) où calib_fiv et r1 extrait diffèrent sur la même entrée, chaînes décimales comparées."""
    a, b = calib_fiv.courbe(pres, val, ells, K_), oracle_r1.courbe(H, pres, val, ells, PRM["calendrier"]["w"])
    return [(c, x["ell"]) for x, y in zip(a, b) for c in CHAMPS if str(x[c]) != str(y[c])]


class TestOracleR1(unittest.TestCase):
    def test_epingles(self):
        """Section « oracle_r1 » : commit f35a70c (complet), dossier s2-harness, cinq empreintes égales à celles de
        PLAN-S2BIS (commit_analyse et harnais_sha256), celle de window.py égale à la valeur de sha256sum ; modules
        chargés : r1 et window de ces fichiers. Mutation M-14-01 (empreinte de r1 de la tête)."""
        o = PRM["oracle_r1"]
        with open(os.path.join(commun.RACINE, "scripts", "plan-s2bis", "parametres.json"), encoding="utf-8") as f:
            plan = json.load(f)
        self.assertEqual((o["commit"], o["dossier"], o["fichiers"]), (COMMIT, "s2-harness", plan["harnais_sha256"]))
        self.assertEqual((plan["commit_analyse"], o["fichiers"]["shogen_s2/window.py"]), (COMMIT, WINDOW))
        self.assertEqual(sorted(H), ["r1", "window"])

    def test_schema_du_commit(self):
        """O-1 de la G2 de la tranche 4 : le commit épinglé est un hexadécimal minuscule de 40 caractères (schéma de
        parametres.json) ; abrégé, en majuscules ou de 41 caractères : PARAMETRES/schema. Mutation R-15 du réviseur
        (commit non contraint)."""
        for faux in ("f35a70c", COMMIT.upper(), COMMIT + "0"):
            p = json.loads(json.dumps(PRM))
            p["oracle_r1"]["commit"] = faux
            with self.assertRaises(commun.Refus) as c:
                commun.controler(p, commun.SCHEMA)
            self.assertEqual(c.exception.code, "PARAMETRES/schema", faux)

    def test_nettoyage_du_dossier(self):
        """Q-T4-12 (O-1 de la G2 de la tranche 4) : dans un processus neuf, à TMPDIR vide (E-S-06), charger extrait le
        harnais dans un seul dossier « oracle_r1_… » de TMPDIR, d'où r1 est chargé ; ce dossier est retiré à la sortie
        du processus. Mutation R-08 du réviseur (dossier jamais retiré)."""
        code = chr(10).join(["import os, tempfile, commun, oracle_r1",
                             "h = oracle_r1.charger(commun.charger_parametres(environ={}))",
                             "d = tempfile.gettempdir()",
                             "print(sorted(x[:10] for x in os.listdir(d)), h['r1'].__file__.startswith(d))"])
        with tempfile.TemporaryDirectory() as d:
            env = {k: v for k, v in os.environ.items() if k != commun.VARIABLE}
            env["TMPDIR"] = d
            p = subprocess.run([sys.executable, "-B", "-c", code], cwd=commun.ICI, env=env, capture_output=True,
                               text=True, timeout=120)
            self.assertEqual((p.stdout.strip(), os.listdir(d)), ("['oracle_r1_'] True", []), p.stderr[-300:])

    def test_cache_indexe_sur_l_epingle(self):
        """O-3 de la G2 de la tranche 4 (Q-T4-12) : un chargement par processus, cache indexé sur l'épingle (commit,
        dossier, fichiers et leurs empreintes) : même épingle, mêmes modules, sans nouvelle extraction (la source n'est
        pas de l'épingle) ; autre commit, autre dossier ou autre empreinte : ORACLE/epingle, jamais le harnais d'une
        autre épingle. Mutations M-14E-01 (épingle non comparée), M-14E-02 (empreintes hors de l'épingle), M-14E-03
        (source dans l'épingle), M-14E-04 (commit hors de l'épingle)."""
        o = PRM["oracle_r1"]
        self.assertIs(oracle_r1.charger(dict(PRM, oracle_r1=dict(o, source="autre")))["r1"], H["r1"])
        for faux in (dict(o, commit="0" * 40), dict(o, dossier="ailleurs"),
                     dict(o, fichiers=dict(o["fichiers"], **{"shogen_s2/r1.py": "0" * 64}))):
            with self.assertRaises(commun.Refus) as c:
                oracle_r1.charger(dict(PRM, oracle_r1=faux))
            self.assertEqual(c.exception.code, "ORACLE/epingle")

    def test_modules_hors_epingles(self):
        """Dans un processus neuf : un shogen_s2 déjà chargé d'ailleurs, ou un module shogen_s2.* hors des fichiers
        épinglés : ORACLE/modules. Mutations M-14-08 (contrôle des modules chargés retiré), M-14-09 (shogen_s2 déjà
        chargé admis)."""
        for intrus in ("shogen_s2", "shogen_s2.intrus"):
            code = chr(10).join(["import sys, types", f"m = types.ModuleType({intrus!r})", "m.__file__ = '/hors/x.py'",
                                 f"sys.modules[{intrus!r}] = m", "import commun, oracle_r1", "try:",
                                 "    oracle_r1.charger(commun.charger_parametres(environ={}))",
                                 "except commun.Refus as e:", "    print(e.code)"])
            env = {k: v for k, v in os.environ.items() if k != commun.VARIABLE}
            p = subprocess.run([sys.executable, "-B", "-c", code], cwd=commun.ICI, env=env, capture_output=True,
                               text=True, timeout=120)
            self.assertEqual(p.stdout.strip(), "ORACLE/modules", (intrus, p.stderr[-300:]))

    def test_refus(self):
        """Épingle fausse : ORACLE/sha256, rien chargé ; commit absent du dépôt : ORACLE/extraction ; dépôt sans git :
        ORACLE/extraction ; variable de la copie scellée posée : CAMPAGNE/variable (E-S-02). Mutations M-14-02
        (empreintes non contrôlées), M-14-03 (sortie de git non contrôlée), M-14-12 (garde de campagne retirée)."""
        with mock.patch.object(commun.os, "environ", {commun.VARIABLE: ""}), tempfile.TemporaryDirectory() as d:
            with self.assertRaises(commun.Refus) as c:
                oracle_r1.extraire(PRM, d)
            self.assertEqual(c.exception.code, "CAMPAGNE/variable")
        faux = dict(PRM["oracle_r1"], fichiers=dict(PRM["oracle_r1"]["fichiers"], **{"shogen_s2/r1.py": "0" * 64}))
        for o, depot, code in ((faux, commun.RACINE, "ORACLE/sha256"),
                               (dict(PRM["oracle_r1"], commit="0" * 40), commun.RACINE, "ORACLE/extraction"),
                               (PRM["oracle_r1"], os.path.join(commun.RACINE, "inexistant"), "ORACLE/extraction")):
            with tempfile.TemporaryDirectory() as d, self.assertRaises(commun.Refus) as c:
                oracle_r1.extraire(dict(PRM, oracle_r1=o), d, depot)
            self.assertEqual(c.exception.code, code)

    def test_t_fiv_1_r1(self):
        """T-FIV-1 : r1 extrait sur 1, 1, 0, 0 : FIV(2) = 1.25 (écrit à la main), et toutes les valeurs égales à
        calib_fiv à ℓ = 1 à 3 ; série à lacune 1, 1, ·, 0, 0 : FIV(2) = 1.5 et aucun écart ; série nulle : FIV
        indéfini (None). Mutations M-14-04 (ℓ − 1 passé à r1), M-14-15 (γ̂₀ = 0 divisé)."""
        r = oracle_r1.courbe(H, bits(0, 1, 2, 3), bits(0, 1), [1, 2, 3], 60)
        self.assertEqual([str(x["FIV_serie"]) for x in r], ["1", "1.25", "1"])
        self.assertEqual(str(oracle_r1.courbe(H, bits(0, 1, 3, 4), bits(0, 1), [2], 60)[0]["FIV_serie"]), "1.5")
        self.assertIsNone(oracle_r1.courbe(H, bits(0, 1, 2), 0, [2], 60)[0]["FIV_serie"])           # γ̂₀ = 0
        self.assertEqual(ecarts(bits(0, 1, 2, 3), bits(0, 1), [1, 2, 3]) + ecarts(bits(0, 1, 3, 4), bits(0, 1), [2, 3]),
                         [])

    def test_oracle_e_s_39(self):
        """E-S-39 : 10 réplications d'E1 (5 sous C0, 5 au point (1/10, 50, 1 440)), deux strates, les 17 ℓ d'EP :
        n, K, numérateur, γ̂₀, σ̂²_bloc et FIV_série de calib_fiv égaux, chaîne pour chaîne, à r1 extrait de f35a70c
        (forme d'episodes.courbe) ; écart mesuré : 0 valeur sur 2 040. Mutation M-14-05 (FIV_série en une seule
        division, sans passer par les valeurs publiées)."""
        texte = commun.lire_entree(PRM, "episodes", environ={}).decode("utf-8")
        ep = calibration.analyser(texte, K_)["episodes"]
        cal = calib_fiv.calendrier_j28(calib_fiv.portee(texte, PRM["calendrier"]), PRM["calendrier"])
        vus = []
        for point in [None] * 5 + [(Fraction(1, 10), Fraction(50), 1440)] * 5:
            r = calib_fiv.replication(PRM, ep, cal, point, "E1-oracle", len(vus) // 2)
            for s in ("calme", "stress"):
                vus.append(ecarts(*r["strates"][s], K_["ell"]))
        self.assertEqual((len(vus), sum(len(x) for x in vus)), (20, 0))


if __name__ == "__main__":
    unittest.main()
