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
refusée. Contre-contrôle de CB-18 (CC-1, remède (a)) : `cable` exige `gabarit`, les lignes brutes du job à indentation
exacte, et `analyseur` ; L-01 à L-21 sont refusés par l'analyseur seul ; L-23 à L-32, leurres qu'il admet (ligne cachée
dans un nom plié ou dans un `with:`, checkout ou `runs-on` réels autres), par le gabarit ; G-01, le gabarit seul. CC-2 :
L-33 (`env:` de premier niveau), L-34 (clé de job répétée) et A-03 (étapes imitées hors de `steps`) figent trois refus
de l'analyseur. CC2-1 : les valeurs libres du gabarit sont des scalaires simples ; L-35 et L-36, un nom entre guillemets
écrit sur plusieurs lignes qui avalerait des lignes du gabarit ; G-02, `timeout-minutes` entier ; G-03 et G-04, le
nom du job et celui de l'étape 3, guillemet fermé à la dernière ligne du bloc, le gabarit seul. CB-18v (Q-T4-11) : le
job sim-bis admet `fetch-depth: 0` sous le `with:` du checkout, après `persist-credentials: false`, valeur exacte, lui
seul ; L-37 à L-41. Sortie : 0 tout passe, 1 un cas échoue, 3 erreur."""
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
    """Lignes brutes du job `nom` du texte de gates.yml, indentation comprise : de sa clé (exclue) à la première ligne
    d'indentation inférieure à 4 qui n'est ni vide ni un commentaire ; lignes vides et commentaires d'indentation 8 au
    plus omis (aucun n'est une ligne d'un bloc `run:`, à l'indentation 10) ; [] s'il manque."""
    lignes, sortie = texte.split(chr(10)), []
    for x in lignes[lignes.index(f"  {nom}:") + 1:] if f"  {nom}:" in lignes else []:
        n, t = len(x) - len(x.lstrip(" ")), x.strip()
        if t and n < 4 and t[0] != "#":
            break
        sortie += [x] if t and (n > 8 or t[0] != "#") else []
    return sortie


RUNNER = "python3 -B enforcement/tests/run-fixtures-verdict-suite-s2.py"
ETAPES = ("runs-on: ubuntu-24.04", "- uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # tag v7.0.1",
          "run: " + RUNNER)
LIBRE = "[0-9A-Za-z].*"      # CC2-1 : valeur libre en scalaire simple, jamais un guillemet qui avalerait des lignes
GABARIT = ("    name: " + LIBRE, "    " + re.escape(ETAPES[0]), "    timeout-minutes: [1-9][0-9]*", "    steps:",
           "      " + re.escape(ETAPES[1]), "        with:", "          persist-credentials: false",
           "      - name: " + LIBRE, "        shell: bash", "        " + re.escape(ETAPES[2]), "      - name: " + LIBRE,
           "        shell: bash", "        run: [|]")
FETCH = "          fetch-depth: 0"   # CB-18v (Q-T4-11) : historique complet du job sim-bis, git archive de f35a70c


def gabarit(texte, nom):
    """CC-1 du contre-contrôle de CB-18, remède (a) : les lignes brutes du job (`job`), à indentation exacte, suivent
    GABARIT ligne à ligne, puis ne sont plus que des lignes d'indentation 10 exactement, celles du bloc de la troisième
    étape. Soit, sur ces lignes et dans cet ordre : `name`, `runs-on: ubuntu-24.04`, `timeout-minutes`, `steps`, puis
    trois étapes et rien d'autre : le checkout épinglé, son `with:` réduit à `persist-credentials: false` ; le runner
    (`name`, `shell: bash`, `run:` du runner) ; une étape `name`, `shell: bash`, `run: |`. Une ligne cachée dans un nom
    plié ou dans un `with:` n'a pas l'indentation de la ligne qu'elle imite. CC2-1 : les trois `name` sont des scalaires
    simples (premier caractère alphanumérique : ni guillemet, ni bloc, ni ancre, ni flux), `timeout-minutes` un entier ;
    une chaîne entre guillemets écrite sur plusieurs lignes avalerait sinon des lignes du gabarit. CB-18v (Q-T4-11) :
    dans le seul job sim-bis-unittest, la ligne FETCH (`fetch-depth: 0`, valeur exacte) peut suivre
    `persist-credentials: false` ; l'adaptateur oracle_r1 y extrait f35a70c par git archive."""
    b = job(texte, nom)
    if nom == "sim-bis-unittest" and b[7:8] == [FETCH]:
        del b[7]
    return len(b) > len(GABARIT) and all(re.fullmatch(g, x) for g, x in zip(GABARIT, b)) and all(
        re.fullmatch(" {10}[^ ].*", x) for x in b[len(GABARIT):])


def analyseur(texte, nom, appel):
    """Analyseur unique `v.etapes`, partagé avec l'enregistreur de rôle (SHOGEN-S2BIS-LIGNE-JOB-LEURRE-1) : trois
    étapes, la première non admise, la deuxième le runner seul ; puis `v.lignes_du_job` : la ligne `appel` une fois,
    dans un bloc `run:` admis sans autre ligne que v.LIBRES."""
    pas = v.etapes(texte, nom) or []
    return len(pas) == 3 and pas[:2] == [None, [RUNNER]] and len(v.lignes_du_job(texte, nom, appel) or []) == 1


def cable(texte, nom, appel):
    """Câblage du job `nom`, contrôlé exactement ainsi, et rien d'autre : (1) `gabarit` : ses lignes brutes, à
    indentation exacte, sont dans l'ordre `name` (scalaire simple), `runs-on: ubuntu-24.04`, `timeout-minutes`
    (entier), `steps`, le checkout épinglé et son `with:` réduit à `persist-credentials: false` (et `fetch-depth: 0`
    dans le seul job sim-bis, CB-18v), le runner (`name` en scalaire simple, `shell: bash`, `run:` du runner), une
    étape `name` (scalaire simple), `shell: bash`, `run: |`, puis seulement des lignes d'indentation 10 ;
    (2) `analyseur`, lecture de l'enregistreur de rôle : trois étapes, la première non admise, la deuxième le runner
    seul, et la ligne `appel` une fois, dans un bloc `run:` admis sans autre ligne que v.LIBRES."""
    return gabarit(texte, nom) and analyseur(texte, nom, appel)


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
        ("L-21 clé jobs répétée", DEBUT + SUITE + ["jobs:", "  autre:"]),
        ("L-33 env du workflow, forme simple (CC-2, CA-01)", ["env: {PATH: leurre}"] + DEBUT + SUITE),
        ("L-34 clé de job runs-on répétée (CC-2, CA-07)", DEBUT[:4] + ["    runs-on: macos-15"] + DEBUT[4:] + SUITE)):
    attendu = nom.startswith("L-00")                    # leurres de l'analyseur : refusés par l'analyseur seul (CC-1)
    admis = (cable if attendu else analyseur)(chr(10).join(lignes), "s2bis-unittest", APPEL)
    cas(nom + (" : admis" if attendu else " : refusé"), [] if admis == attendu else [f"admis : {admis}"], None)
S2 = [x.replace("s2bis-unittest", "s2-harness-unittest") for x in DEBUT] + SUITE[:3] + [L + V]
cas("L-22 job S2 sans --egal : refusé (CB-18m)", ["admis"] if cable(chr(10).join(S2), "s2-harness-unittest", APPEL_S2)
    else [], None)
RO, CO = DEBUT[3].strip(), DEBUT[6].strip()             # CC-1 : leurres que l'analyseur admet, refusés par le gabarit
for nom, lignes in (
        ("L-23 runs-on réel ubuntu-latest, ligne runs-on dans un nom plié (N-01)", DEBUT[:3]
         + ["    runs-on: ubuntu-latest"] + DEBUT[4:9] + ["      - name: >", L + RO] + DEBUT[10:] + SUITE),
        ("L-24 checkout @v4, ligne épinglée dans un nom plié (N-02)", DEBUT[:6] + ["      - uses: actions/checkout@v4"]
         + DEBUT[7:9] + ["      - name: >", L + CO] + DEBUT[10:] + SUITE),
        ("L-25 première étape run: en sh, checkout dans un nom plié (N-03)", DEBUT[:6] + ["      - shell: sh",
         "        run: sed -i s/7/0/ " + V[11:]] + ["      - name: >", L + CO] + DEBUT[10:] + SUITE),
        ("L-26 runs-on réel macos-15, ligne runs-on dans le with: du checkout (N-04)", DEBUT[:3] + [
         "    runs-on: macos-15"] + DEBUT[4:9] + [L + RO] + DEBUT[9:] + SUITE),
        ("L-27 runs-on dans le nom plié du job, réel windows-latest (N-17)", DEBUT[:2] + ["    name: >", L + RO,
         "    runs-on: windows-latest"] + DEBUT[4:] + SUITE),
        ("L-28 checkout dans le nom littéral du job, étape uses: tierce (N-18)", DEBUT[:2] + ["    name: |", L + CO]
         + DEBUT[3:6] + ["      - uses: tiers/action@main"] + DEBUT[7:] + SUITE),
        ("L-29 with: du checkout vers un dépôt tiers", DEBUT[:8] + ["          repository: tiers/r"] + DEBUT[9:]
         + SUITE),
        ("L-30 if: sur l'étape du checkout", DEBUT[:7] + ["        if: false"] + DEBUT[7:] + SUITE),
        ("L-31 runs-on qui prolonge l'étiquette (ubuntu-24.04-arm)", DEBUT[:3] + ["    runs-on: ubuntu-24.04-arm"]
         + DEBUT[4:] + SUITE),
        ("L-32 checkout épinglé à un autre commit", DEBUT[:6] + ["      " + ETAPES[1].replace("@3d3c", "@0d3c")]
         + DEBUT[7:] + SUITE),
        ("L-35 nom d'étape entre guillemets sur trois lignes : le runner avalé (CC2-1, LC-03)", DEBUT[:9]
         + ['      - name: "cas'] + DEBUT[10:] + ['      - name: suite"'] + SUITE[1:]),
        ("L-36 nom du job entre guillemets : runs-on avalé (CC2-1, LC-01)", DEBUT[:2]
         + ['    name: "s2bis-unittest', DEBUT[3], '    timeout-minutes: 10"'] + DEBUT[5:] + SUITE)):
    cas(nom + " : refusé", ["admis"] if cable(chr(10).join(lignes), "s2bis-unittest", APPEL) else [], None)
cas("G-01 ligne du bloc à l'indentation 12 : refusée par le gabarit (indentation exacte)", ["admis"] if gabarit(
    chr(10).join(DEBUT + SUITE[:4] + ["  " + SUITE[4]]), "s2bis-unittest") else [], None)
cas("G-02 timeout-minutes entre guillemets : refusé par le gabarit (entier, CC2-1)", ["admis"] if gabarit(
    chr(10).join(DEBUT[:4] + ['    timeout-minutes: "10"'] + DEBUT[5:] + SUITE), "s2bis-unittest") else [], None)
for nom, lignes in (                                    # CC2-1 : guillemet fermé à la dernière ligne, le gabarit seul
        ("G-03 nom du job", DEBUT[:2] + ['    name: "s2bis-unittest'] + DEBUT[3:] + SUITE[:4] + [L + LIGNE + '"']),
        ("G-04 nom de l'étape 3", DEBUT + ['      - name: "suite'] + SUITE[1:4] + [L + LIGNE + '"'])):
    cas(nom + " entre guillemets, fermé à la dernière ligne du bloc : refusé par le gabarit (scalaire simple, CC2-1)",
        ["admis"] if gabarit(chr(10).join(lignes), "s2bis-unittest") else [], None)
SIM = [x.replace("s2bis-unittest", "sim-bis-unittest") for x in DEBUT]        # CB-18v : job sim-bis (Q-T4-11)
SIM_SUITE, FD = SUITE[:4] + [L + LIGNE.replace(" s2bis ", " scripts/sim-bis ")], "          fetch-depth: "
APPEL_SIM = APPEL.replace(" s2bis ", " scripts/sim-bis ")
for nom, lignes, attendu in (
        ("L-37 job sim-bis, fetch-depth: 0 sous le with: du checkout (CB-18v)", SIM[:9] + [FD + "0"] + SIM[9:]
         + SIM_SUITE, True),
        ("L-38 job sim-bis, fetch-depth: 1 (valeur exacte, CB-18v)", SIM[:9] + [FD + "1"] + SIM[9:] + SIM_SUITE,
         False),
        ("L-39 job s2bis, fetch-depth: 0 (job sim-bis seul, CB-18v)", DEBUT[:9] + [FD + "0"] + DEBUT[9:] + SUITE,
         False),
        ("L-40 job sim-bis, autre clé du with: après fetch-depth: 0 (CB-18v)", SIM[:9] + [FD + "0", L + "ref: main"]
         + SIM[9:] + SIM_SUITE, False),
        ("L-41 job sim-bis, fetch-depth: 0 avant persist-credentials (ordre du gabarit, CB-18v)", SIM[:8]
         + [FD + "0"] + SIM[8:] + SIM_SUITE, False)):
    nom_job = lignes[1].strip(" :")                     # s2bis-unittest ou sim-bis-unittest
    admis = cable(chr(10).join(lignes), nom_job, APPEL_SIM if nom_job == "sim-bis-unittest" else APPEL)
    cas(nom + (" : admis" if attendu else " : refusé"), [] if admis == attendu else [f"admis : {admis}"], None)
EXCLUES = DEBUT + SUITE[:1] + ["        if: false"] + SUITE[1:] + SUITE[:1] + ["        continue-on-error: true"]
EXCLUES += SUITE[1:]
for nom, texte, attendu in (                            # analyseur seul : ce que les contrôles d'avant voyaient déjà
        ("A-01 étapes if: et continue-on-error exclues", EXCLUES, [None, [RUNNER], None, None]),
        ("A-02 séparateur U+2028 : job illisible", DEBUT + SUITE[:1] + [L + chr(8232)] + SUITE[1:], None),
        ("A-03 étapes imitées dans le nom plié du job, hors de steps (CC-2, CA-12)", DEBUT[:2] + ["    name: >",
         "      - name: x", "        shell: bash", "        run: |", L + LIGNE] + DEBUT[3:] + SUITE[:3] + [L + FAIBLE],
         [])):
    cas(f"{nom} (analyseur unique)", [] if v.etapes(chr(10).join(texte), "s2bis-unittest") == attendu else ["écart"],
        None)
print(f"verdict-suite-s2 : {OK_} ok, {KO} échec")
sys.exit(1 if KO else 0)
