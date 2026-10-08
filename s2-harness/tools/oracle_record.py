"""Enregistreur d'oracle Shōgen, schéma shogen.oracle-record.v1 (ADR-0028 D6 (viii) et §1 bis.6 ;
SHOGEN-ORACLE-ENREG-1 ; G0 docs/adr-0028/G0-partie-2.md §B). Bibliothèque standard seule ; commandes lancées par
listes d'arguments, jamais par un shell. Extrait le commit par `git archive` dans un répertoire temporaire, y lance des
commandes de la liste fermée COMMANDES, écrit dans le répertoire donné la sortie de chacune et l'enregistrement
shogen-<sha court>-<rôle>-<date>-<pid>.json (sorties : chemins relatifs à ce répertoire). SHOGEN_S2_CAMPAGNE_CONTROL
est consignée, posée ou non, jamais posée (annexe D.4 a). SHOGEN-ENREG-VERIF-1 : délai maximal par commande ; la
lecture contrôle aussi auteur et, avec un dépôt, tree.sha256. Partie 2, C3 : auteur contrôlé dès l'écriture
(SHOGEN-ENREG-AUTEUR-ECRITURE-1) ; marqueur JOURNAUX des commandes remplacé par le dossier des journaux ; arrêt au
premier échec sur demande (G0 §C, Q5 et Q8). SHOGEN-S2BIS-ENREG-ROLE-1 (lot COLLECTE-BIS, CB-18 ; G0
docs/adr-0029/g0-collecte/) : suites `s2bis` et `scripts/sim-bis` au même enregistreur, par la ligne du vérificateur
de leur job, lue dans le gates.yml du commit extrait (SHOGEN-S2BIS-G3-LIGNE-JOB-1), jamais recopiée ici.
SHOGEN-S2BIS-LIGNE-JOB-LEURRE-1 (G2 de la tranche C de P1) : cette ligne est lue par l'analyseur unique des cas K du
runner (`lignes_du_job` du vérificateur de l'arbre de l'outil, VERIF), dans les seuls blocs `run:` des étapes
admises. SHOGEN-S2BIS-ENREG-VERIF-COMMIT-1 (lot R-1, réserve R-1 de l'accord de P1, OUT-1b) : le vérificateur que la
ligne lance, celui du commit (sha256 consigné dans tree.sha256), doit être celui de l'outil (VERIF), à l'écriture comme
à la lecture ; il est lancé en mode isolé (-I : aucun module posé à côté de lui par le commit n'est importé).
SHOGEN-S2BIS-SUITE-MASQUE-UNITTEST-1 (lot OUT-2, OUT-2b) : la commande `suite`, que l'outil lance par -m unittest sans
le vérificateur, est refusée avant tout run si la racine de sa suite porte une entrée au nom d'un module standard
(`masques`) ; pour les commandes de JOBS, le vérificateur la refuse lui-même. Règle d'usage
(SHOGEN-S2BIS-ENREG-ANCRE-1, OUT-2c) : `tools/README.md` ; la comparaison des vérificateurs ne vaut que si l'outil
tourne depuis un arbre dont le vérificateur a été relu, et elle est triviale lancée depuis l'arbre du commit
enregistré. SHOGEN-S2BIS-SCRIPT-MASQUE-1 (OUT-2d) : toute commande autre que `suite` est lancée en mode isolé (-I) ;
-I implique -E (mesuré sous 3.10 à 3.13) : ces commandes ignorent PYTHONHASHSEED, PYTHONPATH, PYTHONDEVMODE et
PYTHONWARNINGS de l'environnement consigné, que seule `suite` applique ; racine s2-harness masquée refusée pour toute
commande qui y tourne ; bytecode committé (__pycache__, .pyc) refusé ; VERIF exécuté depuis sa source.
SHOGEN-S2BIS-MASQUES-LECTURE-1 (OUT-2f) : la lecture refuse (masque) un arbre qui porte un masque à la racine de la
suite d'un run, ou du bytecode, que l'outil qui l'a écrit l'ait vu ou non (E7 de la G2 d'OUT-2)."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import io
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
from datetime import datetime, timezone

SCHEMA = "shogen.oracle-record.v1"
ROLES = ("G1", "G2", "cp-2", "rendu")
VARIABLE = "SHOGEN_S2_CAMPAGNE_CONTROL"
ENV = (VARIABLE, "PYTHONHASHSEED", "PYTHONPATH")
JOURNAUX = "<journaux>"     # marqueur d'argument : dossier des journaux, chemin absolu substitué (jamais un shell)
LIGNE = "<ligne du job>"    # marqueur : arguments de la ligne du vérificateur du job, lus dans le gates.yml extrait
PRODUCTION = ("j14-principal", "j14-second", "j28", "recalcul-tiers", "raw")   # rendu unique (G0 §C, Q5 à Q7)
JOBS = {"suite-s2bis": ("s2bis-unittest", "s2bis"), "suite-sim-bis": ("sim-bis-unittest", "scripts/sim-bis")}
COMMANDES = {"suite": ("s2-harness", ["-B", "-m", "unittest", "discover", "-s", "tests", "-t", ".", "-v"]),
             **{n: ("s2-harness", ["-B", "tools/rendu_unique.py", "--produire", n, "--journaux", JOURNAUX])
                for n in PRODUCTION}, **{n: (".", [LIGNE]) for n in JOBS}}  # liste fermée
GATES = os.path.join(".github", "workflows", "gates.yml")
HEX = re.compile(r"[0-9a-f]{64}")
CHAMPS = ("schema", "role", "auteur", "base", "static_only", "served_from", "tree", "python", "env", "runs", "exit",
          "ecrit", "paquet", "sceau")
RUN = ("nom", "arbre", "commande", "exit", "sortie", "tests_avec_variable")
LINT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "enforcement",
                    "lint-model-pinning.sh")      # liste blanche des modèles : seule source de vérité, jamais recopiée
VERIF = os.path.join(os.path.dirname(LINT), "verdict-suite-s2.py")    # analyseur unique des lignes de job, non recopié
VERIF_COMMIT = "enforcement/verdict-suite-s2.py"     # vérificateur que lance la ligne d'un job, dans l'extraction
DELAI_DEFAUT = 3600     # s par commande ; suite mesurée ≈ 30 s (docs/G1-partie-2-etape-B-3.md) : garde de blocage
EXIT_DELAI = 124        # exit consigné au dépassement du délai (convention de timeout(1), GNU coreutils)


def git(depot: str, *args: str) -> bytes:
    """git en lecture seule sur `depot` ; variables GIT_* retirées (un GIT_DIR hérité désignerait un autre dépôt)."""
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    return subprocess.run(["git", "-C", depot, *args], capture_output=True, check=True, env=env).stdout


def commit_complet(depot: str, rev: str) -> str:
    """sha complet ; « rev^{commit} » ne se lit jamais comme une option de rev-parse."""
    return git(depot, "rev-parse", "--verify", rev + "^{commit}").decode().strip()


def sha256_fichier(chemin: str) -> str:
    with open(chemin, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def tests_lances(texte: str) -> list:
    """Tests d'une sortie de unittest -v, ligne « test_x (identifiant) » (avant 3.11 : classe, complétée du nom)."""
    return [i if i.endswith("." + n) else f"{i}.{n}" for n, i in re.findall(r"^(test\w*) \(([\w.]+)\)", texte, re.M)]


def consigne(environ) -> dict:
    """Valeurs des variables consignées, None si non posée."""
    return {k: environ.get(k) for k in ENV}


def liste_blanche() -> tuple:
    """Identifiants admis, lus sur l'unique ligne ALLOWED='…' du lint d'épinglage (LINT) ; lint illisible, ligne
    absente, répétée ou vide : ValueError."""
    try:
        with open(LINT, encoding="utf-8") as f:
            lignes = re.findall(r"^ALLOWED='([^']*)'\r?$", f.read(), re.M)
    except OSError as e:
        raise ValueError(f"lint illisible ({e})") from e
    if len(lignes) != 1 or not lignes[0].split():
        raise ValueError(f"{LINT} : une seule ligne ALLOWED='…' non vide exigée, {len(lignes)} lue(s)")
    return tuple(lignes[0].split())


def auteur_admis(a) -> bool:
    """Identifiant de la liste blanche du lint, ou cet identifiant suivi exactement de [1m] (égalité exacte) ; liste
    illisible : ValueError (liste_blanche)."""
    admis = liste_blanche()
    return isinstance(a, str) and (a in admis or a.endswith("[1m]") and a[:-4] in admis)


def masquants(noms) -> list:
    """SHOGEN-S2BIS-SUITE-MASQUE-UNITTEST-1 (OUT-2b) : `noms` d'entrées au nom d'un module de la bibliothèque standard
    (sys.stdlib_module_names, nom pris avant le premier point), triés. Règle de `masques` du vérificateur, écrite ici
    parce que la commande `suite` ne charge pas VERIF : le rendu de production tourne d'un arbre sans vérificateur
    (test_rendu_production) ; appliquée à l'extraction (`masques`) et, à la lecture, à tree.sha256 (OUT-2f).
    sys.stdlib_module_names n'existe qu'à partir de Python 3.10 : version minimale réelle de l'outil et de sa suite."""
    return sorted(x for x in noms if x.split(".")[0] in sys.stdlib_module_names)


def masques(dossier: str) -> list:
    """Entrées de `dossier` retenues par `masquants` : -m unittest lancé de ce dossier les importerait à la place."""
    return masquants(os.listdir(dossier))


def bytecode(chemins) -> list:
    """SHOGEN-S2BIS-SCRIPT-MASQUE-1 (OUT-2d) : `chemins` de fichiers de bytecode (.pyc : cache d'un __pycache__, ou
    module sans source), triés ; à l'import, un .pyc à invalidation non vérifiée remplace la source relue, -I ou non
    (mesuré)."""
    return sorted(k for k in chemins if k.endswith(".pyc"))


def ligne_du_job(arbre: str, job: str, suite: str) -> list:
    """Arguments de la ligne du vérificateur du job `job` de GATES dans l'extraction `arbre`, telle qu'écrite
    (plancher committé compris) : « python3 -B enforcement/verdict-suite-s2.py <suite> --aucun-saut --egal --plancher
    N », une seule fois dans les blocs `run:` des étapes admises du job, lue par `lignes_du_job` de VERIF (étapes
    `if:` et `continue-on-error` exclues, `name: >` jamais lu). Job absent, ligne absente ou répétée, analyseur
    illisible, plancher 0 ou à zéro de tête (N suit `[1-9][0-9]*`, comme K-02 du runner : C-5 (a) de la relecture
    d'intégration de P1) : ValueError (refus). Toute exception au chargement est rattrapée et nommée (OUT-1b)."""
    try:
        with open(os.path.join(arbre, GATES), encoding="utf-8") as f:
            texte = f.read()
        spec = importlib.util.spec_from_file_location("verdict_suite_s2", VERIF)
        analyseur = importlib.util.module_from_spec(spec)
        with open(VERIF, "rb") as f:                # OUT-2d : la source, jamais un .pyc de son __pycache__
            exec(compile(f.read(), VERIF, "exec", dont_inherit=True), analyseur.__dict__)
    except BaseException as e:                     # OUT-1b : toute exception au chargement, SystemExit comprise
        raise ValueError(f"{GATES} de l'extraction ou analyseur {VERIF} illisible ({e!r}) — refus") from e
    motif = ("python3 -B enforcement/verdict-suite-s2[.]py " + re.escape(suite)
             + " --aucun-saut --egal --plancher [1-9][0-9]*")      # C-5 (a) : plancher 0 refusé, comme K-02
    trouves = analyseur.lignes_du_job(texte, job, motif)
    if trouves is None:
        raise ValueError(f"job {job} absent ou répété dans {GATES}, ou {GATES} illisible — refus")
    if len(trouves) != 1:
        raise ValueError(f"job {job} : {len(trouves)} ligne(s) du vérificateur de {suite}, une exigée — refus")
    return trouves[0].split()[1:]


def extraire(depot: str, sha: str, arbre: str) -> dict:
    """`git archive` de `sha` extrait dans `arbre` sous le filtre data de tarfile ; rend {chemin : sha256} par
    fichier."""
    with tarfile.open(fileobj=io.BytesIO(git(depot, "archive", "--format=tar", sha))) as t:
        try:
            t.extractall(arbre, filter="data")
        except tarfile.FilterError as e:
            raise ValueError(f"extraction de {sha} rejetée par le filtre data de tarfile ({e}) — refus") from e
    return {os.path.relpath(os.path.join(d, f), arbre).replace(os.sep, "/"): sha256_fichier(os.path.join(d, f))
            for d, _sous, fs in os.walk(arbre) for f in fs}


def ecarts_arbre(depot: str, commit: str, consignes) -> list:
    """Chemins dont le sha256 de la ré-extraction de `commit` diffère de `consignes` (fichiers en trop ou en moins
    compris) ; ré-extraction impossible : un écart unique qui la nomme."""
    arbre = tempfile.mkdtemp(prefix="oracle_")
    try:
        h = extraire(depot, commit, arbre)
    except (ValueError, OSError, subprocess.CalledProcessError) as e:
        return [f"ré-extraction impossible ({e})"]
    finally:
        shutil.rmtree(arbre)
    t = consignes if isinstance(consignes, dict) else {}
    return sorted(k for k in set(h) | set(t) if h.get(k) != t.get(k))


def enregistrer(dossier: str, role: str, auteur: str, depot: str, commit: str, commandes=("suite",), base=None,
                paquet_sha256=None, sceau_gentime=None, delai=None, journaux=None, arret_premier_echec=False) -> tuple:
    """Lance les commandes nommées sur l'extraction du commit, écrit sorties et enregistrement sans jamais écraser ;
    rend (chemin, exit). paquet.sha256 exigé au rôle « rendu » ; nul, comme sceau.genTime, hors de ce rôle. Délai
    maximal par commande (s ; None : DELAI_DEFAUT) : au dépassement, commande arrêtée, exit EXIT_DELAI consigné, ligne
    de dépassement en fin de sortie, enregistrement écrit quand même. auteur hors liste blanche : refus avant tout git.
    journaux : dossier substitué au marqueur JOURNAUX (exigé si une commande le porte). arret_premier_echec : aucun
    run lancé après un run en échec. Commandes de JOBS : ligne du job lue dans l'extraction, vérificateur du commit
    égal à VERIF (sha256), sinon refus avant tout run (OUT-1b) ; ligne lancée en mode isolé (-I)."""
    delai = DELAI_DEFAUT if delai is None else delai
    if role not in ROLES or not commandes or any(c not in COMMANDES for c in commandes):
        raise ValueError(f"rôle {role!r} ou commande(s) {list(commandes)} hors des listes fermées {ROLES}, "
                         f"{sorted(COMMANDES)} — refus")
    if role == "rendu" and not (isinstance(paquet_sha256, str) and HEX.fullmatch(paquet_sha256)) or (
            role != "rendu" and (paquet_sha256, sceau_gentime) != (None, None)):
        raise ValueError("paquet.sha256 (64 hex) exigé au rôle « rendu » ; paquet.sha256 et sceau.genTime nuls hors "
                         "de ce rôle — refus")
    if not 0 < delai < math.inf:
        raise ValueError(f"délai {delai!r} : nombre de secondes fini et positif exigé — refus")
    if not auteur_admis(auteur):
        raise ValueError(f"auteur {auteur!r} hors de la liste blanche de {LINT} (identifiant exact, ou suivi de [1m]) "
                         "— refus")
    if not journaux and any(JOURNAUX in COMMANDES[c][1] for c in commandes):
        raise ValueError(f"dossier des journaux exigé par {list(commandes)} — refus")
    journaux = journaux and os.path.abspath(journaux)
    sha, base = commit_complet(depot, commit), commit_complet(depot, base) if base else None
    maintenant = datetime.now(timezone.utc)
    nom = f"shogen-{sha[:7]}-{role}-{maintenant:%Y%m%dT%H%M%SZ}-{os.getpid()}"
    arbre, runs = tempfile.mkdtemp(prefix="oracle_"), []
    try:
        hashes = extraire(depot, sha, arbre)
        lignes = {c: ligne_du_job(arbre, *JOBS[c]) for c in commandes if c in JOBS}     # refus avant tout run
        if lignes and hashes.get(VERIF_COMMIT) != sha256_fichier(VERIF):              # OUT-1b : leurre L2
            raise ValueError(f"vérificateur du commit {VERIF_COMMIT} (sha256 {hashes.get(VERIF_COMMIT)}) autre que "
                             f"celui de l'outil {VERIF} (sha256 {sha256_fichier(VERIF)}) — refus")
        racine = COMMANDES["suite"][0]               # OUT-2b, OUT-2d : -m unittest, ou racine mise en tête par la
        masque = masques(os.path.join(arbre, racine)) if any(COMMANDES[c][0] == racine for c in commandes) else []
        if masque:                                   # production (rendu_unique.py), que -I n'écarte pas
            raise ValueError(f"{masque} à la racine de {racine} masque la bibliothèque standard pour -m unittest et la "
                             "production — refus")
        pyc = bytecode(hashes)
        if pyc:                                      # OUT-2d : le .pyc remplacerait la source relue, -I ou non
            raise ValueError(f"bytecode committé dans l'extraction {pyc[:3]} : il remplacerait la source à l'import — "
                             "refus")
        for i, c in enumerate(commandes):
            sous, args = COMMANDES[c][0], lignes.get(c, COMMANDES[c][1])
            cmd = [sys.executable, *["-I"][:c != "suite"], *(journaux if x == JOURNAUX else x for x in args)]
            sortie = f"{nom}.{i}-{c}.out"
            try:
                p = subprocess.run(cmd, cwd=os.path.join(arbre, sous), stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT, timeout=delai)
                octets, code = p.stdout, p.returncode
            except subprocess.TimeoutExpired as e:
                octets, code = (e.stdout or b"") + (f"\n[oracle_record] délai maximal de {delai:g} s dépassé : "
                                                    f"commande arrêtée, exit {EXIT_DELAI}\n").encode(), EXIT_DELAI
            with open(os.path.join(dossier, sortie), "xb") as f:
                f.write(octets)
            runs.append({"nom": c, "arbre": sous, "commande": cmd, "exit": code,
                         "sortie": {"chemin": sortie, "sha256": hashlib.sha256(octets).hexdigest()},
                         "tests_avec_variable": tests_lances(octets.decode("utf-8", "replace"))
                         if os.environ.get(VARIABLE) is not None else []})
            if arret_premier_echec and code:
                break
    finally:
        shutil.rmtree(arbre)
    rec = {"schema": SCHEMA, "role": role, "auteur": auteur, "base": base, "static_only": False, "served_from": None,
           "tree": {"commit": sha, "extraction": f"git archive {sha}", "sha256": dict(sorted(hashes.items()))},
           "python": sys.version, "env": consigne(os.environ), "runs": runs,
           "exit": 0 if all(r["exit"] == 0 for r in runs) else 1, "ecrit": f"{maintenant:%Y-%m-%dT%H:%M:%SZ}",
           "paquet": {"sha256": paquet_sha256}, "sceau": {"genTime": sceau_gentime}}
    chemin = os.path.join(dossier, nom + ".json")
    with open(chemin, "x", encoding="utf-8", newline="\n") as f:
        json.dump(rec, f, ensure_ascii=False, indent=1, sort_keys=True)
    return chemin, rec["exit"]


def cles(x, attendues) -> bool:
    return isinstance(x, dict) and set(x) == set(attendues)


def zero(x) -> bool:
    return type(x) is int and x == 0                  # 0 entier ; false JSON refusé


def verifier(chemin: str, role: str, commit: str, depot=None) -> dict:
    """Relit un enregistrement ; refus nommé, ValueError « refus (<contrôle>) : … », au premier contrôle non conforme :
    champs, schema, rôle attendu, auteur (identifiant de la liste blanche du lint, ou cet identifiant suivi de [1m],
    par égalité exacte), tree.commit égal au sha complet attendu, vérificateur du commit (tree.sha256) égal à VERIF si
    une commande de JOBS a été lancée (OUT-1b), tree.sha256 égal par fichier à la ré-extraction du commit si `depot`
    est donné, static_only false, exit 0 (et chaque commande), sha256 de chaque sortie recalculé,
    masque (OUT-2f : tree.sha256 sans entrée au nom d'un module standard à la racine de la suite d'un run, s2-harness
    pour `suite` et la production, dossier de la suite pour JOBS, ni bytecode), paquet.sha256 et runs (suite, puis
    PRODUCTION, dans l'ordre ; G2, C-6) au rôle « rendu » ou champs nuls hors de ce rôle, served_from nul, ou chemin et
    sha256 d'un
    enregistrement conforme aux mêmes contrôles (même dépôt). Rend l'enregistrement."""
    def exige(ok, controle, detail=""):
        if not ok:
            raise ValueError(f"refus ({controle}) : {chemin}{detail} — enregistrement d'oracle non conforme (D6 viii)")
    try:
        with open(chemin, encoding="utf-8") as f:
            rec = json.load(f)
    except (OSError, ValueError):
        rec = None
    exige(cles(rec, CHAMPS) and cles(rec["tree"], ("commit", "extraction", "sha256")) and cles(rec["paquet"], [
        "sha256"]) and cles(rec["sceau"], ["genTime"]) and isinstance(rec["runs"], list) and all(
        cles(r, RUN) and cles(r["sortie"], ("chemin", "sha256")) for r in rec["runs"]), "champs")
    exige(rec["schema"] == SCHEMA, "schema")
    exige(rec["role"] == role, "rôle", f" : {rec['role']!r}, attendu {role!r}")
    try:
        ok = auteur_admis(rec["auteur"])
    except ValueError as e:
        exige(False, "auteur", f" : liste blanche illisible ({e})")
    exige(ok, "auteur", f" : {rec['auteur']!r}, attendu un identifiant de la liste blanche de {LINT}, ou cet "
          "identifiant suivi de [1m]")
    exige(rec["tree"]["commit"] == commit, "tree.commit", f" : {rec['tree']['commit']!r}, attendu {commit!r}")
    if any(r["nom"] in tuple(JOBS) for r in rec["runs"]):     # OUT-1b : vérificateur lancé par la ligne du job
        v = rec["tree"]["sha256"].get(VERIF_COMMIT) if isinstance(rec["tree"]["sha256"], dict) else None
        exige(v == sha256_fichier(VERIF), "vérificateur", f" : {VERIF_COMMIT} {v!r}, attendu le sha256 de {VERIF}")
    if depot is not None:
        e = ecarts_arbre(depot, commit, rec["tree"]["sha256"])
        exige(not e, "tree.sha256", f" : {e[:3]}{' …' if len(e) > 3 else ''} (ré-extraction depuis {depot})")
    exige(rec["static_only"] is False, "static_only")
    exige(zero(rec["exit"]) and rec["runs"] and all(zero(r["exit"]) for r in rec["runs"]), "exit")
    racine = os.path.dirname(os.path.abspath(chemin))
    for r in rec["runs"]:
        p = os.path.join(racine, str(r["sortie"]["chemin"]))
        exige(os.path.isfile(p) and sha256_fichier(p) == r["sortie"]["sha256"], "sortie", f" : {p}")
    t = rec["tree"]["sha256"] if isinstance(rec["tree"]["sha256"], dict) else {}       # OUT-2f : lecture des masques
    noms = [r["nom"] for r in rec["runs"] if r["nom"] in tuple(COMMANDES)]
    racines = sorted({JOBS[c][1] if c in JOBS else COMMANDES[c][0] for c in noms} - {"."})
    m = [f"{x}/{y}" for x in racines for y in masquants({k[len(x) + 1:].split("/")[0] for k in t if k.startswith(
        x + "/")})] + bytecode(t)
    exige(not m, "masque", f" : {m[:3]} (module standard à la racine de la suite d'un run, ou bytecode)")
    if role == "rendu":
        exige(isinstance(rec["paquet"]["sha256"], str) and HEX.fullmatch(rec["paquet"]["sha256"]), "paquet.sha256")
        noms = [r["nom"] for r in rec["runs"]]
        exige(noms == ["suite", *PRODUCTION], "runs", f" : {noms}, attendu {['suite', *PRODUCTION]}")
    else:
        exige((rec["paquet"]["sha256"], rec["sceau"]["genTime"]) == (None, None), "nuls hors rendu")
    sf = rec["served_from"]
    if sf is not None:
        p = os.path.join(racine, str(sf.get("chemin"))) if isinstance(sf, dict) else ""
        exige(cles(sf, ("chemin", "sha256")) and os.path.isfile(p) and sha256_fichier(p) == sf["sha256"], "served_from")
        try:
            verifier(p, role, commit, depot)
        except ValueError as e:
            exige(False, "served_from", f" → {e}")
    return rec


def main(argv: list) -> int:
    """Écriture (--role, --auteur, --depot, --commit, --sortie ; options --base, --commande, --paquet-sha256,
    --sceau-gentime, --delai), ou lecture (--verifier ENREGISTREMENT --role R --commit SHA_COMPLET ; option --depot :
    tree.sha256 recalculé). Code 0 : enregistrement écrit et commandes vertes, ou conforme ; 1 : une commande a échoué
    ou dépassé son délai ; 2 : refus."""
    p = argparse.ArgumentParser(prog="oracle_record.py", description="enregistrement shogen.oracle-record.v1 (D6 viii)")
    p.add_argument("--verifier", metavar="ENREGISTREMENT")
    p.add_argument("--role", required=True, choices=ROLES)
    p.add_argument("--commit", required=True)
    for opt in ("--auteur", "--depot", "--sortie", "--base", "--paquet-sha256", "--sceau-gentime"):
        p.add_argument(opt)
    p.add_argument("--commande", action="append", choices=sorted(COMMANDES))
    p.add_argument("--delai", type=float, help=f"secondes par commande (défaut {DELAI_DEFAUT})")
    a = p.parse_args(argv)
    ecriture = (a.auteur, a.sortie, a.base, a.commande, a.paquet_sha256, a.sceau_gentime, a.delai)
    if a.verifier is not None and any(x is not None for x in ecriture) or a.verifier is None and None in (
            a.auteur, a.depot, a.sortie):
        p.error("--verifier n'admet que --role, --commit et --depot ; l'écriture exige --auteur, --depot et --sortie")
    try:
        if a.verifier is not None:
            verifier(a.verifier, a.role, a.commit, a.depot)
            print(f"conforme : {a.verifier} (rôle {a.role}, tree.commit {a.commit} ; tree.sha256 " + (
                "non recalculé : --depot absent)" if a.depot is None else f"recalculé sur {a.depot})"))
            return 0
        chemin, code = enregistrer(a.sortie, a.role, a.auteur, a.depot, a.commit, tuple(a.commande or ("suite",)),
                                   a.base, a.paquet_sha256, a.sceau_gentime, a.delai)
    except (ValueError, OSError, subprocess.CalledProcessError) as e:
        print(f"oracle_record : {e}", file=sys.stderr)
        return 2
    print(chemin)
    return code


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
