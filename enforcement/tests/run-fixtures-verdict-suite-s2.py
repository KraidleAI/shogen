"""Shōgen, sous-lot D8a-3 (SHOGEN-CI-S2-SAUT-1 ; ADR-0028 annexe B.4 l.79 ; G0-lot-D8a.md §11 item 13 ; lot DETTES-B1) :
cas du vérificateur enforcement/verdict-suite-s2.py. V : sorties de suite écrites ici (résumé, sauts, codes) ; E :
suites factices lancées dans des dossiers temporaires, hors du dépôt (rejeux R8, MT-5, MT-9 du lot CI-S2 ; variable
retirée de l'environnement de la suite) ; C : point d'entrée sur une suite factice de 398 tests. Variable scellée
jamais transmise à un processus (valeur fictive dans un mapping seulement). Lot COLLECTE-BIS, CB-0 (G0
docs/adr-0029/g0-collecte/) : V-14, V-15, C-03 à C-05 (suite s2bis : aucun saut admis, plancher en option) ; K-01, K-02
(SHOGEN-CI-S2-CABLAGE-1 : étapes des deux jobs unittest lues dans gates.yml). CB-2e (G2 de P1, C-4 et Q-2) : C-06 à
C-08, V-16, V-17 (plancher par défaut et option exercés ; `--egal`) ; aucun `if:` dans les deux jobs. Lot SIM-BIS, SB-0
(G0 docs/adr-0029/g0-sim/) : K-03, étapes du job sim-bis-unittest (`--egal`, aucun `if:`). Relecture G2 de la tranche C
de P1 (SHOGEN-S2BIS-LIGNE-JOB-LEURRE-1) : K-01 à K-03 passent aussi par l'analyseur unique du vérificateur (`etapes`,
`lignes_du_job`), partagé avec l'enregistreur de rôle ; L-00 (témoin du gabarit) et L-01 à L-21, leurres refusés :
`name: >`, `if: false`, `continue-on-error`, bloc plié, `set +e`, heredoc, autre job, étape ajoutée,
`working-directory`, `env` de l'étape, autre shell, `env` du job, `defaults`, clé `run` répétée, job répété, U+2028,
commentaire dans le bloc, runner dans un `name: >`, clé de premier niveau `env :`, entre guillemets ou répétée ;
A-01 et A-02, l'analyseur seul (étapes exclues, U+2028), que les contrôles d'avant masquent. CB-18m : K-01 exige
`--egal` à la ligne du job s2-harness-unittest (Ran = PLANCHER du vérificateur) ; L-22, la même ligne sans `--egal`,
refusée. Sortie : 0 tout passe, 1 un cas échoue, 3 erreur."""
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
cas("V-16 --egal : Ran plancher + 1 refusé", v.verdict(sortie(n=v.PLANCHER + 1, sauts=()), 0, egal=True), "--egal")
cas("V-17 --egal : Ran égal au plancher conforme", v.verdict(sortie(sauts=()), 0, egal=True), None)


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
    s2bis = ["--aucun-saut", "--egal", "--plancher", "3"]
    for nom, corps, rc, n, opt in (
            ("C-01 point d'entrée : tests au plancher, deux sauts nommés, code 0", deux, 0, v.PLANCHER - 3, []),
            ("C-02 point d'entrée : os._exit(0), code 1", sortie0, 1, v.PLANCHER, []),
            ("C-03 --aucun-saut --egal --plancher 3 : deux sauts nommés, code 1", deux, 1, 0, s2bis),
            ("C-04 --aucun-saut --egal --plancher 3 : trois tests sans saut, code 0", "    pass", 0, 2, s2bis),
            ("C-05 option illisible, code 3", "    pass", 3, 1, ["--plancher", "x"]),
            ("C-06 point d'entrée : plancher − 1 tests sans saut, code 1", "    pass", 1, v.PLANCHER - 2, []),
            ("C-07 --aucun-saut --plancher 4 : trois tests, code 1", "    pass", 1, 2,
             ["--aucun-saut", "--plancher", "4"]),
            ("C-08 --aucun-saut --egal --plancher 3 : quatre tests, code 1", "    pass", 1, 3, s2bis)):
        d = factice(os.path.join(W, nom[:4]), corps, n=n)
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            r = v.main([d, *opt])
        cas(nom, [] if r == rc else [f"code {r}, attendu {rc}"], None)
finally:
    shutil.rmtree(W)


def job(texte, nom):
    """Lignes, sans indentation, du job `nom` du texte de gates.yml : de sa clé à la clé de job suivante ; [] s'il
    manque."""
    lignes = texte.splitlines()
    if f"  {nom}:" not in lignes:
        return []
    i = lignes.index(f"  {nom}:") + 1
    fin = next((k for k in range(i, len(lignes)) if re.fullmatch(r"  [\w-]+:", lignes[k])), len(lignes))
    return [x.strip() for x in lignes[i:fin]]


RUNNER = "python3 -B enforcement/tests/run-fixtures-verdict-suite-s2.py"
ETAPES = ("runs-on: ubuntu-24.04", "- uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # tag v7.0.1",
          "run: " + RUNNER)


def cable(texte, nom, appel):
    """Câblage du job `nom` : contrôles d'avant sur ses lignes (une ligne `appel`, les étapes de ETAPES avant elle,
    ni `-m unittest`, ni `continue-on-error`, ni `if:`), puis ceux de l'analyseur unique `v.etapes`, partagé avec
    l'enregistreur de rôle (SHOGEN-S2BIS-LIGNE-JOB-LEURRE-1) : trois étapes, le checkout, le runner seul, puis un bloc
    `run:` admis où la ligne figure une fois, sans autre ligne que v.LIBRES."""
    l, pas = job(texte, nom), v.etapes(texte, nom) or []
    k = [i for i, x in enumerate(l) if re.fullmatch(appel, x)]
    return (len(k) == 1 and all(e in l[:k[0]] for e in ETAPES) and not any(
        "-m unittest" in x or "continue-on-error" in x or x.startswith(("if:", "- if:")) for x in l) and len(pas) == 3
        and pas[:2] == [None, [RUNNER]] and len(v.lignes_du_job(texte, nom, appel) or []) == 1)


with open(GY, encoding="utf-8") as f:
    GYT = f.read()
APPEL = "python3 -B enforcement/verdict-suite-s2[.]py s2bis --aucun-saut --egal --plancher [1-9][0-9]*"
APPEL_S2 = "python3 -B enforcement/verdict-suite-s2[.]py --egal"          # CB-18m : Ran = PLANCHER du vérificateur
for nom, appel in (("K-01 s2-harness-unittest", APPEL_S2),
                   ("K-02 s2bis-unittest", APPEL),
                   ("K-03 sim-bis-unittest", APPEL.replace(" s2bis ", " scripts/sim-bis "))):
    bon = cable(GYT, nom[5:], appel)
    cas(f"{nom} : étapes du job lues dans gates.yml (runner, puis vérificateur)", [] if bon else [
        f"{job(GYT, nom[5:])!r}"], None)
V = "python3 -B enforcement/verdict-suite-s2.py"
L, LIGNE, FAIBLE = " " * 10, V + " s2bis --aucun-saut --egal --plancher 7", V + " s2bis --aucun-saut --plancher 0"
DEBUT = ["jobs:", "  s2bis-unittest:", "    name: s2bis-unittest", "    " + ETAPES[0], "    timeout-minutes: 10",
         "    steps:", "      " + ETAPES[1], "        with:", "          persist-credentials: false",
         "      - name: cas", "        shell: bash", "        " + ETAPES[2]]
SUITE = ["      - name: suite", "        shell: bash", "        run: |", L + "python3 --version", L + LIGNE]
for nom, lignes in (                                    # leurres contre l'analyseur (SHOGEN-S2BIS-LIGNE-JOB-LEURRE-1)
        ("L-00 témoin du gabarit des leurres", DEBUT + SUITE),
        ("L-01 leurre dans un bloc name: > (C1)", DEBUT + ["      - name: >", L + LIGNE] + SUITE[1:3]
         + [L + FAIBLE]),
        ("L-02 leurre dans une étape if: false (C4)", DEBUT + ["      - name: x", "        if: false"] + SUITE[1:]
         + SUITE[:3] + [L + FAIBLE]),
        ("L-03 étape continue-on-error", DEBUT + SUITE[:2] + ["        continue-on-error: true"] + SUITE[2:]),
        ("L-04 bloc plié run: >", DEBUT + SUITE[:2] + ["        run: >"] + SUITE[3:]),
        ("L-05 set +e et exit 0 autour de la ligne (C5)", DEBUT + SUITE[:3] + [L + "set +e", L + LIGNE, L + "exit 0"]),
        ("L-06 ligne dans un heredoc", DEBUT + SUITE[:3] + [L + "cat > /dev/null <<'FIN'", L + LIGNE, L + "FIN"]),
        ("L-07 ligne dans le seul job suivant (MR-24)", DEBUT + SUITE[:4] + ["  autre:", "    steps:"] + SUITE),
        ("L-08 étape ajoutée avant le vérificateur", DEBUT + SUITE[:2] + ["        run: sed -i s/7/0/ " + V[11:]]
         + SUITE),
        ("L-09 working-directory de l'étape", DEBUT + SUITE[:2] + ["        working-directory: leurre"] + SUITE[2:]),
        ("L-10 env de l'étape", DEBUT + SUITE[:2] + ["        env:", L + "PATH: leurre"] + SUITE[2:]),
        ("L-11 shell autre que bash", DEBUT + SUITE[:1] + ["        shell: cat {0}"] + SUITE[2:]),
        ("L-12 env du job (en flux)", DEBUT[:5] + ["    env: {PYTHONPATH: leurre}"] + DEBUT[5:] + SUITE),
        ("L-13 defaults du workflow", ["defaults:", "  run:", "    working-directory: leurre"] + DEBUT + SUITE),
        ("L-14 clé run répétée", DEBUT + SUITE[:2] + ["        run: python3 --version"] + SUITE[2:]),
        ("L-15 job répété", DEBUT + SUITE + DEBUT[1:] + SUITE),
        ("L-16 séparateur U+2028 dans un nom", DEBUT + ["      - name: x" + chr(8232) + "        if: false"]
         + SUITE[1:]),
        ("L-17 commentaire entre run: | et son bloc", DEBUT + SUITE[:3] + ["        # c"] + SUITE[3:]),
        ("L-18 runner dans un bloc name: > seulement", DEBUT[:9] + ["      - name: >", L + ETAPES[2]] + SUITE),
        ("L-19 env du workflow, espace avant les deux-points", ["env : {PATH: leurre}"] + DEBUT + SUITE),
        ("L-20 defaults du workflow, clé entre guillemets", ['"defaults": {run: {shell: cat {0}}}'] + DEBUT + SUITE),
        ("L-21 clé jobs répétée", DEBUT + SUITE + ["jobs:", "  autre:"])):
    attendu = nom.startswith("L-00")
    admis = cable(chr(10).join(lignes), "s2bis-unittest", APPEL)
    cas(nom + (" : admis" if attendu else " : refusé"), [] if admis == attendu else [f"admis : {admis}"], None)
S2 = [x.replace("s2bis-unittest", "s2-harness-unittest") for x in DEBUT] + SUITE[:3] + [L + V]
cas("L-22 job S2 sans --egal : refusé (CB-18m)", ["admis"] if cable(chr(10).join(S2), "s2-harness-unittest", APPEL_S2)
    else [], None)
EXCLUES = DEBUT + SUITE[:1] + ["        if: false"] + SUITE[1:] + SUITE[:1] + ["        continue-on-error: true"]
EXCLUES += SUITE[1:]
for nom, texte, attendu in (                            # analyseur seul : ce que les contrôles d'avant voyaient déjà
        ("A-01 étapes if: et continue-on-error exclues", EXCLUES, [None, [RUNNER], None, None]),
        ("A-02 séparateur U+2028 : job illisible", DEBUT + SUITE[:1] + [L + chr(8232)] + SUITE[1:], None)):
    cas(f"{nom} (analyseur unique)", [] if v.etapes(chr(10).join(texte), "s2bis-unittest") == attendu else ["écart"],
        None)
print(f"verdict-suite-s2 : {OK_} ok, {KO} échec")
sys.exit(1 if KO else 0)
