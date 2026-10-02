"""Enregistreur d'oracle Shōgen, schéma shogen.oracle-record.v1 (ADR-0028 D6 (viii) et §1 bis.6 ;
SHOGEN-ORACLE-ENREG-1 ; G0 docs/adr-0028/G0-partie-2.md §B). Bibliothèque standard seule ; commandes lancées par
listes d'arguments, jamais par un shell. Extrait le commit par `git archive` dans un répertoire temporaire, y lance des
commandes de la liste fermée COMMANDES, écrit dans le répertoire donné la sortie de chacune et l'enregistrement
shogen-<sha court>-<rôle>-<date>-<pid>.json (sorties : chemins relatifs à ce répertoire). SHOGEN_S2_CAMPAGNE_CONTROL
est consignée, posée ou non, jamais posée (annexe D.4 a)."""
from __future__ import annotations

import hashlib
import io
import json
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
COMMANDES = {"suite": ("s2-harness", ["-B", "-m", "unittest", "discover", "-s", "tests", "-t", ".", "-v"])}  # fermée
HEX = re.compile(r"[0-9a-f]{64}")


def git(depot: str, *args: str) -> bytes:
    """git en lecture seule sur `depot`."""
    return subprocess.run(["git", "-C", depot, *args], capture_output=True, check=True).stdout


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


def enregistrer(dossier: str, role: str, auteur: str, depot: str, commit: str, commandes=("suite",), base=None,
                paquet_sha256=None, sceau_gentime=None) -> tuple:
    """Lance les commandes nommées sur l'extraction du commit, écrit sorties et enregistrement sans jamais écraser ;
    rend (chemin, exit). paquet.sha256 exigé au rôle « rendu » ; nul, comme sceau.genTime, hors de ce rôle."""
    if role not in ROLES or not commandes or any(c not in COMMANDES for c in commandes):
        raise ValueError(f"rôle {role!r} ou commande(s) {list(commandes)} hors des listes fermées {ROLES}, "
                         f"{sorted(COMMANDES)} — refus")
    if role == "rendu" and not (isinstance(paquet_sha256, str) and HEX.fullmatch(paquet_sha256)) or (
            role != "rendu" and (paquet_sha256, sceau_gentime) != (None, None)):
        raise ValueError("paquet.sha256 (64 hex) exigé au rôle « rendu » ; paquet.sha256 et sceau.genTime nuls hors "
                         "de ce rôle — refus")
    sha, base = commit_complet(depot, commit), commit_complet(depot, base) if base else None
    maintenant = datetime.now(timezone.utc)
    nom = f"shogen-{sha[:7]}-{role}-{maintenant:%Y%m%dT%H%M%SZ}-{os.getpid()}"
    arbre, runs = tempfile.mkdtemp(prefix="oracle_"), []
    try:
        with tarfile.open(fileobj=io.BytesIO(git(depot, "archive", "--format=tar", sha))) as t:
            t.extractall(arbre, filter="data")
        hashes = {os.path.relpath(os.path.join(d, f), arbre).replace(os.sep, "/"): sha256_fichier(os.path.join(d, f))
                  for d, _sous, fs in os.walk(arbre) for f in fs}
        for i, c in enumerate(commandes):
            sous, args = COMMANDES[c]
            cmd, sortie = [sys.executable, *args], f"{nom}.{i}-{c}.out"
            p = subprocess.run(cmd, cwd=os.path.join(arbre, sous), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            with open(os.path.join(dossier, sortie), "xb") as f:
                f.write(p.stdout)
            runs.append({"nom": c, "arbre": sous, "commande": cmd, "exit": p.returncode,
                         "sortie": {"chemin": sortie, "sha256": hashlib.sha256(p.stdout).hexdigest()},
                         "tests_avec_variable": tests_lances(p.stdout.decode("utf-8", "replace"))
                         if os.environ.get(VARIABLE) is not None else []})
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

