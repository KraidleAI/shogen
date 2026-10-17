"""Lot DETTES-T7 (SHOGEN-S2BIS-MUT-COMMANDE-1, SHOGEN-MUTANTS-ORPHELINS-1 ; ADR-0028 annexe B) : mutants classés par la
commande du job (étapes `run:` de son gates.yml, lues par `etapes` du vérificateur de l'outil, dans l'ordre, par bash
-eo pipefail ; chacune dans un groupe neuf arrêté en entier après elle ; borne pour le job), fichier rendu à ses octets.
Tué : sortie dans --tue (1) ; vivant : toutes à 0 ; FATAL, jamais tué : borne, sortie hors contrat, inapplicable.
Témoin vivant d'abord ; relevé `ps` des groupes vide en fin ; diff et sortie de chaque mutant dans --sortie. POSIX ;
lancé depuis un arbre relu, à part de la copie mutée. Usage : mutants.py <copie> <job> <mutants.json> --sortie D
[--borne S] [--tue C]... ; une ligne JSON par run ; 0 joué, 3 erreur. G2 du lot DETTES-T7 (C-1) : à la borne, les
groupes de tous les descendants de l'étape (relevé ps par parenté : la suite que le vérificateur lance dans sa propre
session depuis DT7-d) sont arrêtés et comptés au relevé de fin ; la sortie n'est plus attendue que RELIQUAT s
(descendant détaché qui garde le tuyau) ; la première étape du job est le checkout, exigé ; les étapes sont
relues sur la copie mutée (mutant de gates.yml classé par la ligne qu'il écrit ; illisibles : FATAL). Réserve R-1
du contre-contrôle : ce checkout est celui du gabarit K, lu sur les lignes brutes du job, jamais une autre étape.
Réserve R-2 : sous Linux, l'outil est moissonneur de ses descendants (`moissonneur`) ; après chaque étape, à la borne
comme à la sortie, tout descendant vivant, orphelin compris (double fork, setsid, parent sorti), est arrêté par
`balayer` jusqu'au dernier, et le relevé de fin exige qu'il n'en reste aucun."""
import os                   # garde en tête (SHOGEN-S2BIS-GARDE-EN-TETE-1) : le dossier du script quitte sys.path
import sys                  # avant tout autre import (un json.py posé à côté ne serait jamais lu)
if sys.path and os.path.realpath(sys.path[0]) == os.path.dirname(os.path.realpath(__file__)):
    del sys.path[0]
import argparse
import contextlib
import ctypes
import difflib
import hashlib
import importlib.util
import json
import shutil
import signal
import subprocess
import tempfile
import time

VERIF = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "enforcement",
                     "verdict-suite-s2.py")                 # analyseur unique des étapes, jamais recopié
ENV = {k: v for k, v in os.environ.items() if k != "SHOGEN_S2_CAMPAGNE_CONTROL"}        # variable scellée jamais passée
RELIQUAT = 5.0      # s de lecture après l'arrêt des groupes à la borne (descendant détaché : plus attendu, C-1)
PASSES = 50         # passes au plus de `balayer` (réserve R-2) : au-delà, des descendants renaissent, erreur


def etapes(copie: str, job: str) -> list:
    """Blocs `run:` du job, première étape (checkout, non admise par l'analyseur, exigée) sautée ; toute autre étape
    non admise : ValueError. Réserve R-1 du contre-contrôle : la première étape est le checkout épinglé du gabarit K,
    lignes brutes du job (`job` du vérificateur) égales à ETAPES[1], `with:` et `persist-credentials: false`, puis
    FETCH admis ; toute autre première étape non admise (action, `if:`, `with:` autre) : ValueError."""
    v = importlib.util.module_from_spec(importlib.util.spec_from_file_location("verdict_suite_s2", VERIF))
    with open(VERIF, encoding="utf-8") as f:                # la source, jamais un .pyc
        exec(compile(f.read(), VERIF, "exec", dont_inherit=True), v.__dict__)
    with open(os.path.join(copie, ".github", "workflows", "gates.yml"), encoding="utf-8") as f:
        texte = f.read()
    pas, b = v.etapes(texte, job), v.job(texte, job)
    i = b.index("    steps:") + 1 if "    steps:" in b else len(b)
    j = next((n for n in range(i + 1, len(b)) if b[n].startswith("      - ")), len(b))      # fin de la 1re étape
    tete = ["      " + v.ETAPES[1], "        with:", "          persist-credentials: false"]   # checkout du gabarit K
    if not pas or pas[0] is not None or None in pas[1:] or b[i:j] not in (tete, tete + [v.FETCH]):
        raise ValueError(f"job {job} : étapes illisibles ou non admises par l'analyseur, ou première étape autre que "
                         f"le checkout épinglé du gabarit K ({pas!r})")
    return pas[1:]


def descendants(racine: int) -> set:
    """Groupe de `racine` et groupes de ses descendants vivants ou zombies, lus par `ps -A -o pid=,ppid=,pgid=` : un
    descendant parti dans sa propre session est suivi par son parent (forme de `groupes` de l'enregistreur de rôle,
    s2-harness/tools/oracle_record.py) ; ps illisible : erreur (sortie 3)."""
    t = [tuple(map(int, y.split())) for y in subprocess.run(["ps", "-A", "-o", "pid=,ppid=,pgid="], capture_output=True,
                                                             text=True, check=True).stdout.splitlines()]
    arbre, plus = {racine}, None
    while plus != set():
        plus = {y[0] for y in t if y[1] in arbre} - arbre
        arbre |= plus
    return {racine} | {y[2] for y in t if y[0] in arbre}


def moissonneur() -> bool:
    """Réserve R-2 du contre-contrôle : sous Linux, prctl(PR_SET_CHILD_SUBREAPER, 1) : tout orphelin d'une étape est
    rattaché à l'outil, donc vu par parenté depuis lui ; ailleurs, ou refus du noyau : False (limite du README)."""
    if not sys.platform.startswith("linux"):
        return False
    try:
        return ctypes.CDLL(None, use_errno=True).prctl(36, ctypes.c_ulong(1), ctypes.c_ulong(0), ctypes.c_ulong(0),
                                                       ctypes.c_ulong(0)) == 0
    except (OSError, AttributeError):
        return False


def balayer(groupes: set, garde: int) -> None:
    """Réserve R-2 : descendants vivants de l'outil hors de son groupe (orphelins rattachés compris) arrêtés par
    groupe, groupes comptés au relevé de fin ; zombies rattachés recueillis, sauf `garde` (l'enfant direct qu'attend
    Popen) ; jusqu'à ce qu'il n'en reste aucun, en PASSES passes au plus (sinon ValueError, sortie 3)."""
    for _ in range(PASSES):
        t = [tuple(y.split()) for y in subprocess.run(["ps", "-A", "-o", "pid=,ppid=,pgid=,stat="],
                                                      capture_output=True, text=True, check=True).stdout.splitlines()]
        t = [(int(a), int(b), int(c), s) for a, b, c, s in t]
        arbre, plus = {os.getpid()}, None
        while plus != set():
            plus = {y[0] for y in t if y[1] in arbre} - arbre
            arbre |= plus
        for y in t:                                       # zombies rattachés à l'outil : recueillis
            if y[1] == os.getpid() and y[3].startswith("Z") and y[0] != garde:
                with contextlib.suppress(ChildProcessError):
                    os.waitpid(y[0], os.WNOHANG)
        vivants = {y[2] for y in t if y[0] in arbre - {os.getpid()} and not y[3].startswith("Z")
                   and y[2] != os.getpgrp()}               # le groupe de l'outil n'a que ps : jamais arrêté
        if not vivants:
            return
        groupes |= vivants
        for g in vivants:
            with contextlib.suppress(ProcessLookupError, PermissionError):
                os.killpg(g, signal.SIGKILL)
        time.sleep(0.05)
    raise ValueError(f"balayage : descendants de l'outil encore vivants après {PASSES} passes")


def jouer(x, pas: list, groupes: set, dossier: str) -> tuple:
    """(classement, motif, [(code, durée, sha256 de sa sortie)] par étape, octets) du job sur la copie."""
    fin, vus, sortie = time.monotonic() + x.borne, [], b""
    for k, bloc in enumerate(pas):
        script, debut = os.path.join(dossier, f"etape-{k}.sh"), time.monotonic()
        with open(script, "w", encoding="utf-8") as f:
            f.write(chr(10).join(bloc) + chr(10))
        p = subprocess.Popen(["bash", "--noprofile", "--norc", "-eo", "pipefail", script], cwd=x.copie, env=ENV,
                             stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             start_new_session=True)
        groupes.add(p.pid)
        try:
            octets, code = p.communicate(timeout=max(fin - debut, 0.001))[0], p.returncode
        except subprocess.TimeoutExpired:
            octets, code = b"", None
        cibles = descendants(p.pid) if code is None else {p.pid}      # C-1 : à la borne, l'arbre entier
        groupes |= cibles
        for g in {y for y in cibles if y > 1} - {os.getpgrp()}:      # groupes entiers, jamais l'enfant direct seul :
            with contextlib.suppress(ProcessLookupError, PermissionError):     # à la borne, ou descendant resté
                os.killpg(g, signal.SIGKILL)                         # après la sortie
        if x.moissonneur:
            balayer(groupes, p.pid)                 # R-2 : orphelins rattachés à l'outil, arrêtés jusqu'au dernier
        if code is None:
            try:
                octets = p.communicate(timeout=RELIQUAT)[0]
            except subprocess.TimeoutExpired as e:      # C-1 : descendant détaché qui garde le tuyau, plus attendu
                octets = e.output or b""
                p.stdout.close()
                p.wait()
        sortie += octets
        vus.append((code, round(time.monotonic() - debut, 1), hashlib.sha256(octets).hexdigest()))
        if code is None:
            return "FATAL", f"borne de {x.borne:g} s dépassée, groupe arrêté", vus, sortie
        if code:
            return ("tué", f"sortie {code}", vus, sortie) if code in (x.tue or [1]) else (
                "FATAL", f"sortie {code} hors contrat", vus, sortie)
    return "vivant", "toutes les étapes à 0", vus, sortie


def muter(x, m: dict, groupes: set, dossier: str) -> tuple:
    """Classement du mutant m ; diff et sortie écrits dans --sortie ; fichier rendu à ses octets, contrôlés ; étapes
    relues sur la copie mutée (C-1 de la G2 : un mutant de gates.yml est classé par la ligne qu'il écrit)."""
    chemin = os.path.join(x.copie, m["fichier"])
    with open(chemin, "rb") as f:
        avant = f.read()
    texte = avant.decode("utf-8")
    apres, n = texte.replace(m["avant"], m["apres"]), texte.count(m["avant"])
    r = ("FATAL", f"inapplicable : texte avant présent {n} fois", [], b"")
    with open(os.path.join(x.sortie, f"{m['id']}.diff"), "w", encoding="utf-8") as f:
        f.writelines(difflib.unified_diff(texte.splitlines(True), apres.splitlines(True), m["fichier"], m["fichier"]))
    if n == 1:
        try:
            with open(chemin, "wb") as f:
                f.write(apres.encode("utf-8"))
            try:
                pas = etapes(x.copie, x.job)
            except ValueError as e:
                r = ("FATAL", f"étapes illisibles sous le mutant : {e}", [], b"")
            else:
                r = jouer(x, pas, groupes, dossier)
        finally:
            with open(chemin, "wb") as f:
                f.write(avant)
        with open(chemin, "rb") as f:
            if f.read() != avant:
                raise ValueError(f"{m['fichier']} non rendu à ses octets après {m['id']}")
    with open(os.path.join(x.sortie, f"{m['id']}.out"), "wb") as f:
        f.write(r[3])
    return r


def chaine_en_cours() -> bool:
    """Lot CAUSES (E37) : vrai si une chaîne de commits tourne sur l'hôte (pgrep -f du motif ancré lu dans
    garde/motif-chaine.txt, partagé avec avant_acte.py et le crochet) ; motif absent ou pgrep en erreur : ValueError
    (sortie 3 : une campagne ne part jamais sans savoir)."""
    chemin = os.path.join(os.path.dirname(os.path.realpath(__file__)), "garde", "motif-chaine.txt")
    with open(chemin, encoding="utf-8") as f:
        lignes = [x for x in f.read().split(chr(10)) if x.strip()]
    if len(lignes) != 1 or not lignes[0].startswith("^"):
        raise ValueError("garde/motif-chaine.txt : une seule ligne, motif ancré par ^, attendue")
    p = subprocess.run(["pgrep", "-f", lignes[0]], capture_output=True, text=True, timeout=30)
    if p.returncode not in (0, 1):
        raise ValueError(f"pgrep : sortie {p.returncode}")
    return p.returncode == 0


def main(argv: list) -> int:
    a = argparse.ArgumentParser(prog="mutants.py")
    a.add_argument("copie"), a.add_argument("job"), a.add_argument("mutants"), a.add_argument("--sortie", required=True)
    a.add_argument("--borne", type=float, default=300.0), a.add_argument("--tue", type=int, action="append")
    x, groupes, dossier = a.parse_args(argv), set(), tempfile.mkdtemp(prefix="mutants_")
    x.moissonneur = moissonneur()                   # R-2 : avant toute étape
    try:
        if chaine_en_cours():                       # lot CAUSES (E37) : un seul lot lourd à la fois sur l'hôte
            raise ValueError("une chaîne de commits tourne sur l'hôte (garde/motif-chaine.txt) : campagne refusée, "
                             "attendre sa fin (until ! pgrep -f <motif> ; do sleep 30; done)")
        pas = etapes(x.copie, x.job)
        with open(x.mutants, encoding="utf-8") as f:
            mutants = json.load(f)
        os.makedirs(x.sortie, exist_ok=True)
        for m in [{"id": "témoin"}, *mutants]:
            r = jouer(x, pas, groupes, dossier) if m["id"] == "témoin" else muter(x, m, groupes, dossier)
            print(json.dumps({**m, "classement": r[0], "motif": r[1], "etapes": r[2]}, ensure_ascii=False), flush=True)
            if m["id"] == "témoin" and r[0] != "vivant":
                raise ValueError("témoin non vivant : campagne arrêtée")
        if x.moissonneur:
            balayer(groupes, 0)                     # R-2 : aucun descendant vivant de l'outil à la fin
        lignes = subprocess.run(["ps", "-eo", "pid=,pgid=,stat="], capture_output=True, text=True, check=True).stdout
        restes = [y for y in (z.split() for z in lignes.splitlines()) if len(y) == 3 and int(y[1]) in groupes
                  and not y[2].startswith("Z")]             # zombies exclus
        if restes:
            raise ValueError(f"relevé ps : {len(restes)} processus des groupes de la campagne restent : {restes[:3]}")
    except (OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError) as e:
        print(f"mutants : erreur : {e}", file=sys.stderr)
        return 3
    finally:
        shutil.rmtree(dossier, ignore_errors=True)
    print(f"mutants : relevé ps de fin : aucun processus des {len(groupes)} groupes de la campagne" + (
        ", aucun descendant vivant de l'outil (moissonneur)" if x.moissonneur else
        " (moissonneur absent : un descendant détaché n'est pas suivi)"), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
