"""Lot DETTES-T7 (SHOGEN-S2BIS-MUT-COMMANDE-1, SHOGEN-MUTANTS-ORPHELINS-1 ; ADR-0028 annexe B) : mutants classés par la
commande du job (étapes `run:` de son gates.yml, lues par `etapes` du vérificateur de l'outil, dans l'ordre, par bash
-eo pipefail ; chacune dans un groupe neuf arrêté en entier après elle ; borne pour le job), fichier rendu à ses octets.
Tué : sortie dans --tue (1) ; vivant : toutes à 0 ; FATAL, jamais tué : borne, sortie hors contrat, inapplicable.
Témoin vivant d'abord ; relevé `ps` des groupes vide en fin ; diff et sortie de chaque mutant dans --sortie. POSIX ;
lancé depuis un arbre relu, à part de la copie mutée. Usage : mutants.py <copie> <job> <mutants.json> --sortie D
[--borne S] [--tue C]... ; une ligne JSON par run ; 0 joué, 3 erreur."""
import os                   # garde en tête (SHOGEN-S2BIS-GARDE-EN-TETE-1) : le dossier du script quitte sys.path
import sys                  # avant tout autre import (un json.py posé à côté ne serait jamais lu)
if sys.path and os.path.realpath(sys.path[0]) == os.path.dirname(os.path.realpath(__file__)):
    del sys.path[0]
import argparse
import contextlib
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


def etapes(copie: str, job: str) -> list:
    """Blocs `run:` du job, première étape (checkout) sautée ; toute autre étape non admise : ValueError."""
    v = importlib.util.module_from_spec(importlib.util.spec_from_file_location("verdict_suite_s2", VERIF))
    with open(VERIF, encoding="utf-8") as f:                # la source, jamais un .pyc
        exec(compile(f.read(), VERIF, "exec", dont_inherit=True), v.__dict__)
    with open(os.path.join(copie, ".github", "workflows", "gates.yml"), encoding="utf-8") as f:
        pas = v.etapes(f.read(), job)
    if not pas or None in pas[1:]:
        raise ValueError(f"job {job} : étapes illisibles ou non admises par l'analyseur ({pas!r})")
    return pas[1:]


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
        with contextlib.suppress(ProcessLookupError):       # groupe entier, jamais l'enfant direct seul : à la
            os.killpg(p.pid, signal.SIGKILL)                # borne, ou descendant resté après la sortie
        octets += p.communicate()[0] if code is None else b""
        sortie += octets
        vus.append((code, round(time.monotonic() - debut, 1), hashlib.sha256(octets).hexdigest()))
        if code is None:
            return "FATAL", f"borne de {x.borne:g} s dépassée, groupe arrêté", vus, sortie
        if code:
            return ("tué", f"sortie {code}", vus, sortie) if code in (x.tue or [1]) else (
                "FATAL", f"sortie {code} hors contrat", vus, sortie)
    return "vivant", "toutes les étapes à 0", vus, sortie


def muter(x, m: dict, pas: list, groupes: set, dossier: str) -> tuple:
    """Classement du mutant m ; diff et sortie écrits dans --sortie ; fichier rendu à ses octets, contrôlés."""
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


def main(argv: list) -> int:
    a = argparse.ArgumentParser(prog="mutants.py")
    a.add_argument("copie"), a.add_argument("job"), a.add_argument("mutants"), a.add_argument("--sortie", required=True)
    a.add_argument("--borne", type=float, default=300.0), a.add_argument("--tue", type=int, action="append")
    x, groupes, dossier = a.parse_args(argv), set(), tempfile.mkdtemp(prefix="mutants_")
    try:
        pas = etapes(x.copie, x.job)
        with open(x.mutants, encoding="utf-8") as f:
            mutants = json.load(f)
        os.makedirs(x.sortie, exist_ok=True)
        for m in [{"id": "témoin"}, *mutants]:
            r = jouer(x, pas, groupes, dossier) if m["id"] == "témoin" else muter(x, m, pas, groupes, dossier)
            print(json.dumps({**m, "classement": r[0], "motif": r[1], "etapes": r[2]}, ensure_ascii=False), flush=True)
            if m["id"] == "témoin" and r[0] != "vivant":
                raise ValueError("témoin non vivant : campagne arrêtée")
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
    print(f"mutants : relevé ps de fin : aucun processus des {len(groupes)} groupes de la campagne", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
