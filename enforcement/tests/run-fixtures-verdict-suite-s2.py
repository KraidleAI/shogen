"""Shōgen, sous-lot D8a-3 (SHOGEN-CI-S2-SAUT-1 ; ADR-0028 annexe B.4 l.79 ; G0-lot-D8a.md §11 item 13 ; lot DETTES-B1) :
cas du vérificateur enforcement/verdict-suite-s2.py. V : sorties de suite écrites ici (résumé, sauts, codes) ; E :
suites factices lancées dans des dossiers temporaires, hors du dépôt (rejeux R8, MT-5, MT-9 du lot CI-S2 ; variable
retirée de l'environnement de la suite) ; C : point d'entrée sur une suite factice de 398 tests. Variable scellée
jamais transmise à un processus (valeur fictive dans un mapping seulement). Lot COLLECTE-BIS, CB-0 (G0
docs/adr-0029/g0-collecte/) : V-14, V-15, C-03 à C-05 (suite s2bis : aucun saut admis, plancher en option) ; K-01, K-02
(SHOGEN-CI-S2-CABLAGE-1 : étapes des deux jobs unittest lues dans gates.yml). Sortie : 0 tout passe, 1 un cas échoue, 3
erreur."""
import contextlib
import importlib.util
import io
import os
import re
import shutil
import sys
import tempfile

ICI = os.path.dirname(os.path.abspath(__file__))
GY = os.path.join(ICI, "..", "..", ".github", "workflows", "gates.yml")
if not os.path.isfile(GY):
    print(f"ERREUR : {GY} introuvable", file=sys.stderr)
    sys.exit(3)
try:
    _S = importlib.util.spec_from_file_location("verdict", os.path.join(ICI, "..", "verdict-suite-s2.py"))
    v = importlib.util.module_from_spec(_S)
    _S.loader.exec_module(v)
except (OSError, SyntaxError) as e:
    print(f"ERREUR : vérificateur illisible ({e})", file=sys.stderr)
    sys.exit(3)
VAR, TIRETS = "SHOGEN_S2_CAMPAGNE_CONTROL", "-" * 70
NOMME = f"'{VAR} absente : copie du control.jsonl scellé non fournie'"


def sortie(n=v.PLANCHER, sauts=(NOMME, NOMME), statut=None, apres=""):
    """Sortie -v de unittest : une ligne par saut, puis tirets, « Ran n tests in 1.234s », statut."""
    corps = "".join(f"test_{i} (tests.t.T.test_{i}) ... skipped {m}\n" for i, m in enumerate(sauts))
    st = statut or ("OK" + (f" (skipped={len(sauts)})" if sauts else ""))
    return f"{corps}test_z (tests.t.T.test_z) ... ok\n\n{TIRETS}\nRan {n} tests in 1.234s\n\n{st}\n{apres}"


OK_ = KO = 0


def cas(nom, refus, attendu):
    """attendu : None (conforme), ou fragment du premier motif de refus."""
    global OK_, KO
    bon = not refus if attendu is None else bool(refus) and attendu in refus[0]
    OK_, KO = OK_ + bon, KO + (not bon)
    print(f"{'ok' if bon else 'ÉCHEC'} {nom}" + ("" if bon else f" : {refus!r}"))


cas("V-01 conforme : au plancher, deux sauts nommant la variable", v.verdict(sortie(), 0), None)
cas("V-02 saut ajouté à motif autre (R8, MT-7)", v.verdict(sortie(sauts=(NOMME, NOMME, "'autre motif'")), 0),
    "ne nomme pas")
cas("V-03 Ran plancher − 1 (MT-5, MT-6)", v.verdict(sortie(n=v.PLANCHER - 1), 0), f"plancher {v.PLANCHER}")
cas("V-04 Ran plancher + 12 : sans égalité figée", v.verdict(sortie(n=v.PLANCHER + 12), 0), None)
cas("V-05 aucune ligne Ran, code 0 (MT-9)", v.verdict(sortie().split(TIRETS)[0], 0), "résumé final absent")
cas("V-06 code 1, résumé OK", v.verdict(sortie(), 1), "code de sortie 1")
cas("V-07 FAILED (failures=1)", v.verdict(sortie(statut="FAILED (failures=1, skipped=2)"), 1), "code de sortie 1")
cas("V-08 FAILED avec code 0", v.verdict(sortie(statut="FAILED (failures=1, skipped=2)"), 0), "résumé final absent")
cas("V-09 une ligne skipped pour skipped=2", v.verdict(sortie(statut="OK (skipped=2)", sauts=(NOMME,)), 0),
    "1 ligne(s)")
cas("V-10 OK (expected failures=1)", v.verdict(sortie(sauts=(), statut="OK (expected failures=1)"), 0),
    "résumé final absent")
cas("V-11 ligne non vide après le résumé", v.verdict(sortie(apres="Ran 999 tests in 0.001s\n"), 0),
    "résumé final absent")
cas("V-12 aucun saut, OK (variable posée hors du job)", v.verdict(sortie(sauts=()), 0), None)
cas("V-13 motif entre guillemets doubles", v.verdict(sortie(sauts=(NOMME, f"\"{VAR} : l'autre\"")), 0), None)
cas("V-14 aucun saut admis : sauts nommant la variable refusés", v.verdict(sortie(), 0, variable=None), "aucun admis")
cas("V-15 aucun saut admis : suite sans saut conforme", v.verdict(sortie(sauts=()), 0, variable=None), None)


def factice(d, corps, nom="test_f.py", n=1):
    """Dossier s2-harness factice : tests/__init__.py, test_g.py (un test vide) et un module ; n tests vides en plus
    du corps donné."""
    os.makedirs(os.path.join(d, "tests"))
    open(os.path.join(d, "tests", "__init__.py"), "w").close()
    with open(os.path.join(d, "tests", "test_g.py"), "w", encoding="utf-8") as f:
        f.write("import unittest\n\n\nclass G(unittest.TestCase):\n    def test_g(self):\n        pass\n")
    with open(os.path.join(d, "tests", nom), "w", encoding="utf-8") as f:
        f.write("import os, unittest\n\n\nclass T(unittest.TestCase):\n" + corps + "\n\n"
                f"for i in range({n}):\n    setattr(T, f'test_v{{i:03d}}', lambda self: None)\n")
    return d


W = tempfile.mkdtemp(prefix="verdict_cas_")
try:
    def e(nom, corps, attendu, plancher=1, fichier="test_f.py", environ=None, n=1):
        err, _out, code = v.lancer(factice(os.path.join(W, nom[:4]), corps, fichier, n), environ)
        cas(nom, v.verdict(err, code, plancher), attendu)
    e("E-01 suite factice conforme", "    pass", None)
    e("E-02 os._exit(0) avant le résumé (MT-9)", "    def test_x(self):\n        os._exit(0)", "résumé final absent")
    e("E-03 saut à motif autre (R8)", "    def test_x(self):\n        self.skipTest('autre motif')", "ne nomme pas")
    e("E-04 module sorti du motif test*.py (MT-5)", "    pass", "plancher 2", 2, "verif_f.py")    # 2 sans renommage
    e("E-05 variable retirée de l'environnement de la suite", f"    def test_x(self):\n        assert '{VAR}' not "
      "in os.environ", None, environ={**os.environ, VAR: "/chemin/fictif/inexistant"})
    deux = "".join(f"    def test_s{i}(self):\n        self.skipTest({NOMME})\n" for i in (1, 2))
    sortie0 = "    def test_x(self):\n        os._exit(0)"
    s2bis = ["--aucun-saut", "--plancher", "3"]
    for nom, corps, rc, n, opt in (
            ("C-01 point d'entrée : tests au plancher, deux sauts nommés, code 0", deux, 0, v.PLANCHER - 3, []),
            ("C-02 point d'entrée : os._exit(0), code 1", sortie0, 1, v.PLANCHER, []),
            ("C-03 --aucun-saut --plancher 3 : deux sauts nommés, code 1", deux, 1, 0, s2bis),
            ("C-04 --aucun-saut --plancher 3 : trois tests sans saut, code 0", "    pass", 0, 2, s2bis),
            ("C-05 option illisible, code 3", "    pass", 3, 1, ["--plancher", "x"])):
        d = factice(os.path.join(W, nom[:4]), corps, n=n)
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            r = v.main([d, *opt])
        cas(nom, [] if r == rc else [f"code {r}, attendu {rc}"], None)
finally:
    shutil.rmtree(W)


def job(nom):
    """Lignes, sans indentation, du job `nom` de gates.yml : de sa clé à la clé de job suivante ; [] s'il manque."""
    with open(GY, encoding="utf-8") as f:
        lignes = f.read().splitlines()
    if f"  {nom}:" not in lignes:
        return []
    i = lignes.index(f"  {nom}:") + 1
    fin = next((k for k in range(i, len(lignes)) if re.fullmatch(r"  [\w-]+:", lignes[k])), len(lignes))
    return [x.strip() for x in lignes[i:fin]]


ETAPES = ("runs-on: ubuntu-24.04", "- uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # tag v7.0.1",
          "run: python3 -B enforcement/tests/run-fixtures-verdict-suite-s2.py")
for nom, appel in (("K-01 s2-harness-unittest", r"python3 -B enforcement/verdict-suite-s2\.py"),
                   ("K-02 s2bis-unittest", r"python3 -B enforcement/verdict-suite-s2\.py s2bis --aucun-saut "
                                           r"--plancher [1-9][0-9]*")):
    l = job(nom[5:])
    k = [i for i, x in enumerate(l) if re.fullmatch(appel, x)]
    bon = (len(k) == 1 and all(e in l[:k[0]] for e in ETAPES)
           and not any("-m unittest" in x or "continue-on-error" in x for x in l))
    cas(f"{nom} : étapes du job lues dans gates.yml (runner, puis vérificateur)", [] if bon else [f"{l!r}"], None)
print(f"verdict-suite-s2 : {OK_} ok, {KO} échec")
sys.exit(1 if KO else 0)
