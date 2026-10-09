"""Shōgen, lot DETTES-T4, DT4-a (SHOGEN-DOCS-SHA256SUMS-GATE-1 ; ADR-0028 annexe B, B.90, B.87). Chaque SHA256SUMS de
docs/ hors d'INTERDITS (liste de S-G5, xtask/src/sg5.rs, égalité exigée par un cas ; jamais lus) se rejoue comme
`sha256sum --strict -c` : ligne « <64 hex minuscules> <espace ou *><chemin relatif sous le dossier> », sans `.`, `..`,
composant vide, barre oblique inverse ni retour chariot ; chemin interdit, *.jsonl, ou hors du dossier par un lien
(SHA256SUMS compris) : refusé sans ouverture ; fichier présent, de sha256 égal. ABSENTS_ADMIS (adjudication Q-1 de
DETTES-T4) : l.1-10 et l.12 de sim-niveau, fichiers jamais versés (sorties du lot SIM-NIVEAU restées sur le poste
local), lignes gardées à la clôture de SHOGEN-SIM-SOMMES-1 (04beacd) parce que le paquet les cite par numéro ; admises
tant que le fichier manque et que ces lignes jointes par un saut de ligne ont le sha256 écrit ; toute autre ligne
absente est refusée. Fichier non listé : compté, non refusé (un SHA256SUMS scelle ce qu'il nomme). Usage : python3 -B
docs-sha256sums.py <racine> ; 0 conforme, 1 refus (motifs sur stderr), 3 erreur (jamais un refus)."""
import hashlib
import os
import pathlib
import re
import sys

INTERDITS = ("docs/15-", "docs/16-", "docs/pocket-report/", "docs/rapports/", "docs/adr-0025/",
             "docs/adr-0028/monark-m009a/", "docs/adr-0028/execution/")
LIGNE = re.compile(rb"([0-9a-f]{64}) [ *](.+)")
EXCLUS, NL = {chr(92), chr(13)}, bytes([10])     # barre oblique inverse (nom échappé), retour chariot ; saut de ligne
ABSENTS_ADMIS = {"docs/adr-0028/sim-niveau/SHA256SUMS": (
    (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12), "7f45c55ed2056da107e6f34db5c0bba43b5f8f3e30b9c196b365b984fce45596")}


def interdit(relatif: str) -> bool:
    return relatif.startswith(INTERDITS) or relatif.endswith(".jsonl")


def parcourir(racine: str, dossier: str, garder):
    for base, dossiers, fichiers in os.walk(os.path.join(racine, dossier)):
        rel = os.path.relpath(base, os.path.join(racine, dossier)).replace(os.sep, "/")
        pre = "" if rel == "." else rel + "/"
        dossiers[:] = sorted(x for x in dossiers
                             if not interdit(f"{dossier}/{pre}{x}/") and garder(os.path.join(base, x)))
        yield from (pre + x for x in sorted(fichiers) if not interdit(f"{dossier}/{pre}{x}"))


def verifier(racine: str, somme: str, motifs: list) -> tuple:
    """Rejoue `somme` ; ajoute ses motifs ; rend (lignes, absentes admises, fichiers non listés)."""
    dossier, admis, listes = os.path.dirname(somme), 0, set()
    reel_dossier, reel_racine = os.path.realpath(os.path.join(racine, dossier)), os.path.realpath(racine)
    if not os.path.realpath(os.path.join(racine, somme)).startswith(reel_dossier + os.sep):
        motifs.append(f"{somme} : lien hors de son dossier (non ouvert)")
        return 0, 0, 0
    lignes = pathlib.Path(racine, somme).read_bytes().removesuffix(NL).split(NL)
    nums, epingle = ABSENTS_ADMIS.get(somme, ((), ""))
    bloc = NL.join(lignes[k - 1] for k in nums if k <= len(lignes))
    nums = nums if hashlib.sha256(bloc).hexdigest() == epingle else ()
    for n, ligne in enumerate(lignes, 1):
        m, ici = LIGNE.fullmatch(ligne), f"{somme} l.{n}"
        chemin = m.group(2).decode("utf-8", "replace") if m else ""
        parts = chemin.split("/")
        if not m or chemin.startswith("/") or any(p in ("", ".", "..") for p in parts) or set(chemin) & EXCLUS:
            motifs.append(f"{ici} : ligne hors forme {ligne[:100]!r}")
            continue
        listes.add(chemin)
        cible = os.path.join(racine, dossier, *parts)
        reel, ecrite = os.path.realpath(cible), m.group(1).decode("ascii")
        if interdit(f"{dossier}/{chemin}") or interdit(os.path.relpath(reel, reel_racine).replace(os.sep, "/")):
            motifs.append(f"{ici} : {chemin} sous un emplacement interdit (non ouvert)")
        elif not reel.startswith(reel_dossier + os.sep):
            motifs.append(f"{ici} : {chemin} hors du dossier par un lien (non ouvert)")
        elif not os.path.lexists(cible) and n in nums:
            admis += 1
        elif not os.path.isfile(cible):
            motifs.append(f"{ici} : {chemin} absent")
        else:
            reelle = hashlib.sha256(pathlib.Path(cible).read_bytes()).hexdigest()
            if reelle != ecrite:
                motifs.append(f"{ici} : {chemin} : somme écrite {ecrite}, réelle {reelle}")
    autres = parcourir(racine, dossier, lambda d: not os.path.exists(os.path.join(d, "SHA256SUMS")))
    return len(lignes), admis, sum(1 for x in autres if x != "SHA256SUMS" and x not in listes)


def main(argv: list) -> int:
    if len(argv) != 1 or not os.path.isdir(os.path.join(argv[0], "docs")):
        print(f"docs-sha256sums : erreur : racine illisible {argv!r}", file=sys.stderr)
        return 3
    motifs, totaux = [], [0, 0, 0]
    try:
        liste = ["docs/" + x for x in parcourir(argv[0], "docs", lambda d: True) if x.split("/")[-1] == "SHA256SUMS"]
        for somme in liste:
            totaux = [a + b for a, b in zip(totaux, verifier(argv[0], somme, motifs))]
    except Exception as e:      # une erreur n'est jamais un refus
        print(f"docs-sha256sums : erreur : {e}", file=sys.stderr)
        return 3
    for m in motifs:
        print(f"docs-sha256sums : refus : {m}", file=sys.stderr)
    if not motifs:
        print(f"docs-sha256sums : conforme : {len(liste)} SHA256SUMS, {totaux[0]} ligne(s), dont {totaux[1]} absente(s)"
              f" admise(s) (SHOGEN-SIM-SOMMES-1) ; {totaux[2]} fichier(s) non listé(s), non refusés")
    return 1 if motifs else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
