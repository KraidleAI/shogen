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
seul ; L-37 à L-41. CB-18w (O-2 de la relecture de SIM-T4) : la ligne y est exigée ; L-42. CB-18x (CC4-1 du
contre-contrôle cc4) : L-43 (indentation 8) et L-44 (après le nom de l'étape du runner) fixent l'égalité exacte et la
place de la ligne. CB-19h (C-5 (b) de la relecture d'intégration de P1) : toute exception au chargement du
vérificateur, SystemExit compris, donne la sortie 3 ; R-01 et R-02, copie du runner avec un vérificateur qui sort
en 0 ou lève à son chargement. Lot R-1 (réserve R-1 de l'accord de P1 ; SHOGEN-S2BIS-RUNNER-SORTIE-1, OUT-1a) : le
runner ne charge plus le vérificateur ; un sous-processus le charge et répond à chaque attribut ou appel par une
ligne JSON entière (Q-1 : le runner compte et juge seul) ; la sortie 0 exige CAS cas joués, ni plus ni moins (Q-2).
R-03 à R-08 : os._exit(0) au chargement ; sys.exit(0) ou os._exit(0) pendant un cas (réponse absente) ; réponse
tronquée ; exception pendant un cas ; copie à CAS + 1. B-01 à B-04 : `bilan`. La valeur fictive de la variable
scellée (E-05) passe au sous-processus comme donnée d'un appel, jamais comme environnement. Lot OUT-2
(SHOGEN-S2BIS-RUNNER-REJEU-1, OUT-2a) : chaque requête porte un nonce imprévisible (secrets, 128 bits) que sa
réponse doit renvoyer ; une réponse écrite avant sa requête, ou rejouée d'un transcript capturé du canal (D7 du
contre-contrôle de R-1), est refusée et nommée : R-09 à R-11. Garantie réelle : la sortie 0 dit que les CAS cas ont
été joués et jugés sur le canal, chaque réponse écrite après sa requête par un code qui l'a lue ; elle ne dit pas que
les réponses viennent du code relu. Limite : un vérificateur qui reconnaît `--serveur`, ou lit les requêtes, peut
répondre juste au runner et mentir à l'étape du job ; la lecture humaine du diff du vérificateur reste nécessaire.
SHOGEN-S2BIS-SUITE-MASQUE-UNITTEST-1 (OUT-2b) : M-01 à M-03, racine de suite qui masque la bibliothèque standard pour
-m unittest (unittest.py, paquet unittest/, argparse.py chargé avant la découverte), refus nommé, suite non lancée ;
M-04, témoin au nom libre ; M-05, `masques` (nom pris avant le premier point : json.abi3.so, extension que
l'import prendrait pour json, C-1 de la G2 d'OUT-2). SHOGEN-S2BIS-SCRIPT-MASQUE-1 (OUT-2d) : le dossier du script
quitte sys.path avant tout import qu'un fichier posé à côté masquerait (runner, serveur, copies ; vérificateur lancé en
script) et le serveur exécute la source du vérificateur, jamais un .pyc de son __pycache__ ; I-01 à I-03, copies du
runner où sont posés un module sous le nom de chaque import qui suit sa garde, secrets.py, ou ce .pyc ; I-04, un module
sous le nom de chaque import qui suit la garde du vérificateur, posé à côté de lui (C-1 et C-2 de la revue de la vague
2 : la place de chaque garde est épinglée, plus seulement json et subprocess). Sortie : 0 tout
passe (CAS cas), 1 un cas échoue ou le vérificateur rompt pendant un cas, 3 erreur (vérificateur illisible au
chargement compris). SHOGEN-S2BIS-SUITE-RESUME-FORGE-1 (OUT-2e) : F-01 à F-09, `accord` sur des comptes écrits ici ;
F-10 à F-14, `main` sur des suites qui forgent leur résumé (os._exit(0), flux réécrit et atexit, compte au nonce
deviné), dont un .pyc non vérifié remplacerait un module de test, ou qui lisent sys.path (comme sous -m unittest) ;
E-01 à E-05 jugés aussi par `accord`."""
import os                   # SCRIPT-MASQUE-1 (OUT-2d) : os et sys sont chargés au démarrage, avant que le dossier du
import sys                  # script entre dans sys.path ; il en sort ici, avant tout autre import (I-01, I-02)
if sys.path and os.path.realpath(sys.path[0]) == os.path.dirname(os.path.realpath(__file__)):
    del sys.path[0]
import atexit
import contextlib
import importlib.util
import io
import json
import py_compile
import re
import secrets
import shutil
import subprocess
import tempfile

ICI = os.path.dirname(os.path.abspath(__file__))
GY = os.path.join(ICI, "..", "..", ".github", "workflows", "gates.yml")
if not os.path.isfile(GY):
    print(f"ERREUR : {GY} introuvable", file=sys.stderr)
    sys.exit(3)


def servir():
    """Sous-processus du vérificateur (Q-1) : le charge, écrit « pret », puis répond à chaque requête (ligne JSON :
    nonce, puis attribut, ou appel et ses arguments) par une ligne JSON sur le canal, stdout d'origine, qui renvoie le
    nonce de la requête (RUNNER-REJEU-1) ; ce que le vérificateur imprime va sur stderr. SystemExit n'est pas
    rattrapée : le runner reste sans réponse."""
    canal, sys.stdout = sys.stdout, sys.stderr
    s = importlib.util.spec_from_file_location("verdict", os.path.join(ICI, "..", "verdict-suite-s2.py"))
    m = importlib.util.module_from_spec(s)
    with open(s.origin, "rb") as f:             # SCRIPT-MASQUE-1 : la source, jamais un .pyc de son __pycache__ (I-03)
        exec(compile(f.read(), s.origin, "exec", dont_inherit=True), m.__dict__)
    print("pret", file=canal, flush=True)
    for ligne in sys.stdin:
        n, *q = json.loads(ligne)
        try:
            x = getattr(m, q[1])
            r = json.dumps([n, "fonction", None] if q[0] == "attr" and callable(x) else [
                n, "valeur", x(*q[2], **q[3]) if q[0] == "appel" else x])
        except Exception as e:
            r = json.dumps([n, "exception", repr(e)])
        print(r, file=canal, flush=True)


if sys.argv[1:] == ["--serveur"]:
    servir()
    sys.exit(0)


class Rompu(Exception):
    """Vérificateur rompu pendant un cas : réponse absente, tronquée, illisible ou sans le nonce de sa requête, ou
    exception levée (sortie 1)."""


class Distant:
    """Le vérificateur vu du runner, qui ne le charge jamais (Q-1) : chaque attribut et chaque appel est une requête au
    sous-processus, dont la réponse doit être une ligne JSON entière qui renvoie le nonce de la requête."""

    def __init__(self, p):
        self.p = p

    def __getattr__(self, nom):
        genre, x = self.demande(["attr", nom])
        return (lambda *a, **k: self.demande(["appel", nom, a, k])[1]) if genre == "fonction" else x

    def demande(self, q):
        n = secrets.token_hex(16)               # RUNNER-REJEU-1 (Q-1 de OUT-2) : imprévisible, propre à la requête
        try:
            self.p.stdin.write(json.dumps([n, *q]) + chr(10))
            self.p.stdin.flush()
            ligne = self.p.stdout.readline()
        except OSError:
            ligne = ""
        if not ligne.endswith(chr(10)):
            raise Rompu(f"réponse {'tronquée' if ligne else 'absente'} à {q[:2]} (code {self.p.poll()}) : {trace()}")
        try:
            r = json.loads(ligne)
        except ValueError:
            r = None
        if not (isinstance(r, list) and len(r) == 3 and r[1] in ("valeur", "fonction", "exception")):
            raise Rompu(f"réponse illisible à {q[:2]} : {ligne[:80]!r}")
        if r[0] != n:
            raise Rompu(f"réponse sans le nonce de sa requête à {q[:2]} : écrite avant elle, ou rejouée")
        if r[1] == "exception":
            raise Rompu(f"le vérificateur a levé {r[2]} à {q[:2]}")
        return r[1:]


def trace():
    """Fin de ce que le sous-processus a écrit sur stderr."""
    TRACE.seek(0)
    t = TRACE.read()[-240:].decode("utf-8", "replace")
    TRACE.seek(0, 2)
    return repr(t)


def bilan(ok, ko, attendus):
    """Sortie du runner (Q-2) : 0 si `attendus` cas exactement sont joués et passent, 1 sinon."""
    return 0 if (ok, ko) == (attendus, 0) else 1


TRACE = tempfile.TemporaryFile()
P = subprocess.Popen([sys.executable, *["-X", "dev"][:2 * sys.flags.dev_mode], *("-W" + w for w in sys.warnoptions),
                      "-B", os.path.abspath(__file__), "--serveur"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                     stderr=TRACE, text=True, encoding="utf-8")


@atexit.register
def fermer():
    for f in (P.stdin, P.stdout):
        with contextlib.suppress(OSError):
            f.close()
    try:
        P.wait(timeout=60)
    except subprocess.TimeoutExpired:
        P.kill()
        P.wait()
    TRACE.close()


if P.stdout.readline() != "pret" + chr(10):        # C-5 (b) et RUNNER-SORTIE-1 : sortie au chargement, échec fermé
    print(f"ERREUR : vérificateur illisible (aucun « pret », code {P.poll()}) : {trace()}", file=sys.stderr)
    sys.exit(3)
v = Distant(P)
sys.excepthook = lambda t, e, tb: print(f"ÉCHEC vérificateur rompu : {e}", file=sys.stderr) if t is Rompu else (
    sys.__excepthook__(t, e, tb))
VAR, TIRETS = "SHOGEN_S2_CAMPAGNE_CONTROL", "-" * 70
NOMME = f"'{VAR} absente : copie du control.jsonl scellé non fournie'"


def sortie(n=v.PLANCHER, sauts=(NOMME, NOMME), statut=None, apres=""):
    """Sortie -v de unittest : une ligne par saut, puis tirets, « Ran n tests in 1.234s », statut."""
    corps = "".join(f"test_{i} (tests.t.T.test_{i}) ... skipped {m}\n" for i, m in enumerate(sauts))
    st = statut or ("OK" + (f" (skipped={len(sauts)})" if sauts else ""))
    return f"{corps}test_z (tests.t.T.test_z) ... ok\n\n{TIRETS}\nRan {n} tests in 1.234s\n\n{st}\n{apres}"


OK_ = KO = 0
CAS = 123                   # cas joués exigés, ni plus ni moins (Q-2) : un cas ajouté ou retiré la change (PLANCHER)


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
        err, _out, code, compte, nonce = v.lancer(factice(os.path.join(W, nom[:4]), corps, fichier, n), environ)
        cas(nom, v.verdict(err, code, plancher) + v.accord(err, compte, nonce), attendu)     # OUT-2e : compte réel
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
    MARQUE = os.path.join(W, "masque-importe")          # SUITE-MASQUE-UNITTEST-1 : leurre importé, donc suite lancée
    LEURRE = ["import sys", f"open({MARQUE!r}, 'w').close()", "sys.stderr.write(chr(10) + '-' * 70 + chr(10) + 'Ran 3 "
              "tests in 0.001s' + chr(10) * 2 + 'OK' + chr(10))", "sys.exit(0)"]      # résumé conforme forgé, code 0

    def masquee(rep, *noms):
        """Suite factice verte de 3 tests (C-04), et le leurre sous chacun des `noms` à sa racine."""
        d = factice(os.path.join(W, rep), "    pass", n=2)
        for x in noms:
            os.makedirs(os.path.dirname(os.path.join(d, x)), exist_ok=True)
            with open(os.path.join(d, x), "w", encoding="utf-8") as f:
                f.write(chr(10).join(LEURRE) + chr(10))
        return d
    r = v.main([masquee("M-01", "unittest.py"), *s2bis])     # refus lu sur le stderr du vérificateur (trace)
    cas("M-01 unittest.py à la racine, résumé forgé : sortie 1, refus nommé, suite non lancée", [] if (
        r, "masque la bibliothèque standard" in trace(), os.path.exists(MARQUE)) == (1, True, False) else [
        f"code {r}, leurre importé : {os.path.exists(MARQUE)} : {trace()}"], None)
    for nom, noms, rc in (("M-02 paquet unittest/ à la racine : sortie 1", ["unittest/__init__.py"], 1),
                          ("M-03 argparse.py à la racine, chargé par unittest avant la découverte : sortie 1",
                           ["argparse.py"], 1),
                          ("M-04 témoin, module au nom libre à la racine (commun.py) : conforme", ["commun.py"], 0)):
        r = v.main([masquee(nom[:4], *noms), *s2bis])
        cas(nom, [] if r == rc else [f"code {r}, attendu {rc}"], None)
    cas("M-05 masques : noms de modules standard seuls, pris avant le premier point (json.abi3.so), triés", [] if (
        v.masques(masquee("M-05", "unittest.py", "json.py", "json.abi3.so", "commun.py", "unittest_notes.md",
                          "README.md")) == ["json.abi3.so", "json.py", "unittest.py"]) else ["écart"], None)
    N, PL = "a" * 32, v.PLANCHER                # SUITE-RESUME-FORGE-1 (OUT-2e) : nonce du run et comptes écrits ici
    for nom, compte, attendu in (
            ("F-01 compte réel d'accord avec le résumé (Ran plancher, deux sautés) : conforme", f"{N} {PL} 0 0 2 0 0",
             None),
            ("F-02 compte réel absent (programme de test arrêté avant sa fin)", None, "compte réel absent"),
            ("F-03 compte réel sans le nonce du run (écrit avant lui, ou rejoué)", f"{'b' * 32} {PL} 0 0 2 0 0",
             "sans le nonce"),
            ("F-04 compte réel à six champs", f"{N} {PL} 0 0 2 0", "sans le nonce"),
            ("F-05 désaccord : lancés", f"{N} {PL - 1} 0 0 2 0 0", "désaccord"),
            ("F-06 désaccord : un échec réel sous un résumé OK", f"{N} {PL} 1 0 2 0 0", "désaccord"),
            ("F-07 désaccord : une erreur réelle sous un résumé OK", f"{N} {PL} 0 1 2 0 0", "désaccord"),
            ("F-08 désaccord : sautés", f"{N} {PL} 0 0 1 0 0", "désaccord"),
            ("F-09 désaccord : échec attendu et succès inattendu", f"{N} {PL} 0 0 2 1 1", "désaccord")):
        cas(nom, v.accord(sortie(), compte, N), attendu)

    def forgee(rep, *lignes):
        """Suite factice sous W/rep : un module de test (lignes)."""
        os.makedirs(os.path.join(W, rep, "tests"))
        open(os.path.join(W, rep, "tests", "__init__.py"), "w").close()
        with open(os.path.join(W, rep, "tests", "test_f.py"), "w", encoding="utf-8") as f:
            f.write(chr(10).join(lignes) + chr(10))
        return os.path.join(W, rep)
    ROUGE, DEUX = ["import atexit, os, sys, unittest", "", "", "class T(unittest.TestCase):", "    def test_a(self):",
                   "        self.fail('rouge')", ""], ["--aucun-saut", "--egal", "--plancher", "2"]
    FORGE = "sys.stderr.write(chr(10) + '-' * 70 + chr(10) + 'Ran 2 tests in 0.001s' + chr(10) * 2 + 'OK' + chr(10))"
    for nom, lignes, motif in (
            ("F-10 résumé forgé puis os._exit(0) dans un test (RESUME-FORGE-1) : sortie 1, compte réel absent", [
                *ROUGE, "    def test_z(self):", "        " + FORGE, "        sys.stderr.flush()",
                "        os._exit(0)"], "compte réel absent"),
            ("F-11 flux réécrit (FAILED devient OK), sortie forcée à 0 par atexit : sortie 1, désaccord", [
                *ROUGE, "    def test_z(self):", "        pass", "", "", "class F:", "    def __init__(self, f):",
                "        self.f = f", "", "    def write(self, s):", "        return self.f.write(s.replace('FAILED', "
                "'OK').replace(' (failures=1)', ''))", "", "    def flush(self):", "        self.f.flush()", "", "",
                "sys.stderr = F(sys.stderr)", "atexit.register(os._exit, 0)"], "désaccord"),
            ("F-12 compte écrit par un test au nonce deviné (0…0), résumé forgé, os._exit(0) : sortie 1, refus", [
                *ROUGE, "    def test_z(self):", "        with open(os.path.join(__import__('__main__').t, "
                "'compte'), 'x', encoding='utf-8') as f:", "            f.write('0' * 32 + ' 2 0 0 0 0 0')",
                "        " + FORGE,
                "        sys.stderr.flush()", "        os._exit(0)"], "sans le nonce")):
        r = v.main([forgee(nom[:4], *lignes), *DEUX])
        cas(nom, [] if (r, motif in trace()) == (1, True) else [f"code {r} : {trace()}"], None)
    MARQUE_U = os.path.join(W, "F-13-marque")       # F-13 : .pyc non vérifié d'un module de test, vert et marqué
    d = forgee("F-13", *ROUGE, "    def test_z(self):", "        pass")
    with open(os.path.join(W, "F-13.py"), "w", encoding="utf-8") as f:
        f.write(chr(10).join(["import unittest", f"open({MARQUE_U!r}, 'a').close()", "", "",
                              "class T(unittest.TestCase):", "    def test_a(self):", "        pass", "",
                              "    def test_z(self):", "        pass", ""]))
    py_compile.compile(os.path.join(W, "F-13.py"), importlib.util.cache_from_source(os.path.join(d, "tests",
                       "test_f.py")), doraise=True, invalidation_mode=py_compile.PycInvalidationMode.UNCHECKED_HASH)
    r = v.main([d, *DEUX])
    cas("F-13 .pyc non vérifié d'un module de test (vert, marqué), source rouge : jamais exécuté, sortie 1", [] if (
        r, os.path.exists(MARQUE_U)) == (1, False) else [f"code {r}, .pyc exécuté : {os.path.exists(MARQUE_U)}"], None)
    r = v.main([forgee("F-14", *ROUGE[:5], "        self.assertNotIn('', sys.path)", "", "    def test_z(self):",
                       "        self.assertEqual(sys.path[0], os.getcwd())"), *DEUX])
    cas("F-14 racine de la suite en tête de sys.path en chemin absolu, '' absent (comme -m unittest) : conforme",
        [] if r == 0 else [f"code {r} : {trace()}"], None)
    PAS = ["PLANCHER = 406", "def verdict(*a, **k):"]          # RUNNER-SORTIE-1 : vérificateur rompu pendant V-01
    T = os.path.join(W, "transcript")        # RUNNER-REJEU-1 : canal du vérificateur réel, recopié par R-09a (D7)
    CAPTURE = ["import os, threading", "_r, _w = os.pipe()", "_s = os.dup(1)", "os.dup2(_w, 1)",
               f"_f = os.open({T!r}, os.O_WRONLY | os.O_CREAT | os.O_EXCL)", "def _tee():",
               "    for b in iter(lambda: os.read(_r, 65536), b''):", "        os.write(_f, b)",
               "        os.write(_s, b)", "threading.Thread(target=_tee, daemon=True).start()"]
    LIRE = [f"with open({T!r}, encoding='utf-8') as f:", "    lignes = f.read().split(chr(10))"]
    ECRIRE, FIN = "sys.__stdout__.write({})" + chr(10) + "sys.__stdout__.flush()", ["for _ in sys.stdin:", "    pass",
                                                                                    "os._exit(0)"]

    def copie(rep, corps, plus=0, avant=None):
        """Copie du runner (CAS + plus) et de gates.yml réel sous W/rep, vérificateur `corps` (lignes ; None : le réel),
        lancée en --copie (C-5 (b)) après avant(d), d le dossier du runner copié (SCRIPT-MASQUE-1) ; rend le processus
        fini."""
        d = os.path.join(W, rep, "enforcement", "tests")
        os.makedirs(d)
        os.makedirs(os.path.join(W, rep, ".github", "workflows"))
        shutil.copy(GY, os.path.join(W, rep, ".github", "workflows"))
        with open(os.path.abspath(__file__), encoding="utf-8") as f:
            src = f.read()
        with open(os.path.join(d, os.path.basename(__file__)), "w", encoding="utf-8") as f:
            f.write(src.replace(f"CAS = {CAS} ", f"CAS = {CAS + plus} ", 1))
        if corps is None:
            shutil.copy(os.path.join(ICI, "..", "verdict-suite-s2.py"), os.path.join(d, ".."))
        else:
            with open(os.path.join(d, "..", "verdict-suite-s2.py"), "w", encoding="utf-8") as f:
                f.write(chr(10).join(corps) + chr(10))
        if avant:
            avant(d)
        return subprocess.run([sys.executable, "-B", os.path.join(d, os.path.basename(__file__)), "--copie"],
                              capture_output=True, text=True, timeout=120)
    for nom, rc, motif, *corps in (
            ("R-01 vérificateur qui sort en 0 à son chargement : runner en sortie 3", 3, "vérificateur illisible",
             "import sys", "sys.exit(0)"),
            ("R-02 vérificateur qui lève à son chargement : runner en sortie 3", 3, "vérificateur illisible",
             "raise RuntimeError()"),
            ("R-03 os._exit(0) au chargement du vérificateur : runner en sortie 3", 3, "vérificateur illisible",
             "import os", "os._exit(0)"),
            ("R-04 sys.exit(0) pendant un cas : réponse absente, runner en sortie 1", 1, "réponse absente",
             "import sys", *PAS, "    sys.exit(0)"),
            ("R-05 os._exit(0) pendant un cas : réponse absente, runner en sortie 1", 1, "réponse absente",
             "import os", *PAS, "    os._exit(0)"),
            ("R-06 réponse sans fin de ligne, puis os._exit(0) : réponse tronquée, runner en sortie 1", 1,
             "réponse tronquée", "import json, os, sys", *PAS, "    sys.__stdout__.write(json.dumps(['valeur', []]))",
             "    sys.__stdout__.flush()", "    os._exit(0)"),
            ("R-07 vérificateur qui lève pendant un cas : runner en sortie 1", 1, "a levé", *PAS,
             "    raise RuntimeError('rompu')"),
            ("R-08 copie du runner, vérificateur réel, CAS + 1 : runner en sortie 1", 1, "cas attendus"),
            ("R-09 rejeu au chargement du transcript capturé (D7), aucun code du vérificateur : runner en sortie 1", 1,
             "nonce de sa requête", "import os, sys", *LIRE, ECRIRE.format("chr(10).join(lignes)"), *FIN),
            ("R-10 réponse au format du canal écrite avant toute requête : runner en sortie 1", 1,
             "nonce de sa requête", "import json, sys",
             ECRIRE.format("'pret' + chr(10) + json.dumps(['f' * 32, 'valeur', 0]) + chr(10)")),
            ("R-11 rejeu du transcript au nonce lu dans la première requête : runner en sortie 1", 1,
             "nonce de sa requête", "import json, os, sys", *LIRE, ECRIRE.format("lignes[0] + chr(10)"),
             "n = json.loads(sys.stdin.readline())[0]", ECRIRE.format(
                 "''.join(json.dumps([n, *json.loads(x)[1:]]) + chr(10) for x in lignes[1:-1])"), *FIN)):
        if sys.argv[1:] == ["--copie"]:                 # dans une copie : aucune copie de plus (récursion), cas compté
            cas(nom, [], None)
            continue
        capture = 0                                     # R-09 : d'abord la capture, copie au vérificateur réel recopié
        if nom[:4] == "R-09":
            with open(os.path.join(ICI, "..", "verdict-suite-s2.py"), encoding="utf-8") as f:
                capture = copie("R-09a", CAPTURE + [f.read()]).returncode
        p = copie(nom[:4], corps or None, 0 if corps else 1)
        cas(nom, [] if (capture, p.returncode, motif in p.stderr) == (0, rc, True) else [
            f"capture {capture}, sortie {p.returncode} : {p.stderr[-160:]!r}"], None)
    ILLISIBLE, ANTICIPEE = ["import sys", "sys.exit(0)"], ["import json, sys", ECRIRE.format(
        "'pret' + chr(10) + json.dumps(['f' * 32, 'valeur', 0]) + chr(10)")]       # corps de R-01 et de R-10

    def voisin(rel, *lignes):
        """avant(d) qui pose le module `rel` (lignes ; un chemin relatif, ou un tuple de chemins, paquet compris) dans
        le dossier d du runner copié (SCRIPT-MASQUE-1)."""
        def poser(d):
            for r in (rel,) if isinstance(rel, str) else rel:
                os.makedirs(os.path.dirname(os.path.join(d, r)), exist_ok=True)
                with open(os.path.join(d, r), "w", encoding="utf-8") as f:
                    f.write(chr(10).join(lignes) + chr(10))
        return poser

    def pyc(d):
        """I-03 : .pyc à invalidation non vérifiée du vérificateur, au corps de R-10, dans son __pycache__."""
        with open(os.path.join(W, "I-03.py"), "w", encoding="utf-8") as f:
            f.write(chr(10).join(ANTICIPEE) + chr(10))
        py_compile.compile(os.path.join(W, "I-03.py"), importlib.util.cache_from_source(os.path.join(
            d, "..", "verdict-suite-s2.py")), doraise=True,
                           invalidation_mode=py_compile.PycInvalidationMode.UNCHECKED_HASH)
    APRES = ("atexit.py", "contextlib.py", "importlib/__init__.py", "io.py", "json.py", "py_compile.py", "re.py",
             "secrets.py", "shutil.py", "subprocess.py", "tempfile.py")      # I-01 : chaque import qui suit la garde,
    # dans l'ordre du fichier (C-1 de la revue de la vague 2) ; atexit (intégré) et io (préchargé) ne sont jamais
    # cherchés dans sys.path (mesuré sous 3.10 à 3.13), posés pour que la liste suive les imports
    for nom, rc, motif, corps, avant in (     # SCRIPT-MASQUE-1 (OUT-2d) : rien de posé à côté n'est exécuté
            ("I-01 json.py, et chaque module importé après la garde, posés à côté du runner (« 999 ok », os._exit(0))"
             " : jamais importés, runner en sortie 3", 3, "vérificateur illisible", ILLISIBLE,
             voisin(APRES, "import os", "print('verdict-suite-s2 : 999 ok')", "os._exit(0)")),
            ("I-02 secrets.py posé à côté du runner (nonce prévu) : jamais importé, réponse anticipée refusée", 1,
             "nonce de sa requête", ANTICIPEE, voisin("secrets.py", "def token_hex(n=16):", "    return 'f' * 2 * n")),
            ("I-03 .pyc non vérifié du vérificateur (__pycache__) : jamais exécuté, sa source l'est (sortie 3)", 3,
             "vérificateur illisible", ILLISIBLE, pyc)):
        if sys.argv[1:] == ["--copie"]:                 # comme R-01 à R-11 : aucune copie dans une copie, cas compté
            cas(nom, [], None)
            continue
        p = copie(nom[:4], corps, 0, avant)
        cas(nom, [] if (p.returncode, motif in p.stderr) == (rc, True) else [
            f"sortie {p.returncode} : {p.stderr[-160:]!r}"], None)
    # I-04 : sous le nom de chaque import qui suit la garde du vérificateur (C-2 de la revue de la vague 2), un module
    # marqué posé à côté de lui, transparent (il se retire et recharge le vrai module)
    MARQUE4, D4 = os.path.join(W, "I-04", "marque"), os.path.join(W, "I-04")
    d = factice(os.path.join(W, "I-04", "s"), "    def test_x(self):" + chr(10) + "        self.fail()", n=1)
    shutil.copy(os.path.join(ICI, "..", "verdict-suite-s2.py"), D4)
    for x in ("re", "secrets", "shutil", "subprocess", "tempfile"):
        voisin(x + ".py", "import os, sys", f"open({MARQUE4!r}, 'a').close()", "sys.path[:] = [p for p in sys.path if "
               f"os.path.realpath(p) != os.path.realpath({D4!r})]", f"del sys.modules[{x!r}]", f"import {x}")(D4)
    # dans une copie (--copie), comme I-01 à I-03 : cas compté, rien de lancé ; le vérificateur copié y est un leurre,
    # ou l'enveloppe de capture de R-09a, qui lève avant toute garde (sous 3.13, l'affichage de son exception, écrit en
    # Python, importe re depuis le dossier du script ; 3.10 à 3.12 non : mesuré)
    p = None if sys.argv[1:] == ["--copie"] else subprocess.run([sys.executable, "-B", os.path.join(
        D4, "verdict-suite-s2.py"), d, *s2bis], stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=120)
    cas("I-04 re.py, secrets.py, shutil.py, subprocess.py, tempfile.py posés à côté du vérificateur lancé en script "
        "(suite rouge) : jamais importés", [] if p is None or not os.path.exists(MARQUE4) else [
            f"importé, sortie {p.returncode}"], None)                               # la sortie n'est pas jugée (E-4)
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
    une chaîne entre guillemets écrite sur plusieurs lignes avalerait sinon des lignes du gabarit. CB-18v (Q-T4-11) et
    CB-18w (O-2) : dans le seul job sim-bis-unittest, la ligne FETCH (`fetch-depth: 0`, valeur exacte) suit
    `persist-credentials: false`, exigée ; l'adaptateur oracle_r1 y extrait f35a70c par git archive."""
    b = job(texte, nom)
    if nom == "sim-bis-unittest":
        if b[7:8] != [FETCH]:
            return False
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
    (entier), `steps`, le checkout épinglé et son `with:` réduit à `persist-credentials: false` (et `fetch-depth: 0`,
    exigé dans le seul job sim-bis, CB-18v et CB-18w), le runner (`name` en scalaire simple, `shell: bash`, `run:` du
    runner), une étape `name` (scalaire simple), `shell: bash`, `run: |`, puis seulement des lignes d'indentation 10 ;
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
         + [FD + "0"] + SIM[8:] + SIM_SUITE, False),
        ("L-42 job sim-bis sans fetch-depth: 0 (ligne exigée, CB-18w, O-2)", SIM + SIM_SUITE, False),
        ("L-43 job sim-bis, fetch-depth: 0 à l'indentation 8 (égalité exacte, CB-18x)", SIM[:9] + [FD[2:] + "0"]
         + SIM[9:] + SIM_SUITE, False),
        ("L-44 job sim-bis, fetch-depth: 0 après le nom de l'étape du runner (place exacte, CB-18x)", SIM[:10]
         + [FD + "0"] + SIM[10:] + SIM_SUITE, False)):
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
for nom, ok, ko, rc in (("B-01 CAS cas joués, tous passés : sortie 0", CAS, 0, 0),      # RUNNER-SORTIE-1 (Q-2)
                        ("B-02 un cas de moins que CAS : sortie 1", CAS - 1, 0, 1),
                        ("B-03 un cas de plus que CAS : sortie 1", CAS + 1, 0, 1),
                        ("B-04 un cas en échec : sortie 1", CAS - 1, 1, 1)):
    cas(nom, [] if bilan(ok, ko, CAS) == rc else [f"bilan {bilan(ok, ko, CAS)}, attendu {rc}"], None)
print(f"verdict-suite-s2 : {OK_} ok, {KO} échec")
if OK_ + KO != CAS:
    print(f"ÉCHEC compte des cas : {OK_ + KO} joués, {CAS} cas attendus (CAS)", file=sys.stderr)
sys.exit(1 if KO else bilan(OK_, KO, CAS))           # un cas en échec suffit, même si `bilan` est faux (A8)
