"""Capture des octets (INT-P2-16 ; Q-5 adjugée le 2026-10-17 ; AVIS Q-C-05 l.94 ; E-C-37, E-C-40 ; FORMAT §19) : une
lecture de chaque forme du pool et du témoin (`formes.json`), puis de la carte (`carte.json`), en série, comme le smoke
(une seconde au moins avant une nouvelle lecture d'un hôte à `espace` vrai) ; les octets bruts du corps de chacune
dans `<dossier>/<rôle>-<forme>.bin` (rôle de `smoke.role`, ou `carte`), et une ligne par lecture dans
`<dossier>/captures.txt` : fichier, sha256 des octets, statut, code HTTP, départ (µs UTC). Aucun décodage ; rien
n'est imprimé, ni octet, ni prix (ADR-0029 l.222). Refus avant toute lecture (CaptureRefusee, motif `dossier`, `nom`
ou `fichier`) : dossier absent, nom de forme hors de NOM, fichier déjà présent (jamais écrasé). Lecture HTTP et pause
injectables : tests sur fixtures, sans réseau. Code 0 si toutes les lectures du pool et du témoin sont `ok` ;
1 sinon."""
import hashlib
import os
import re
import time

from shogen_s2bis.collecte import http, smoke

NOM = re.compile("[a-z0-9_][a-z0-9_.-]{0,63}")                     # nom de forme sûr comme nom de fichier
MANIFESTE = "captures.txt"


class CaptureRefusee(Exception):
    def __init__(self, motif, detail):
        super().__init__(f"{motif} : {detail}")


def capturer(formes, carte, delais, dossier, lire=None, pause=time.sleep, tls=http.CONTEXTE):
    """Écrit les octets de chaque lecture puis le manifeste ; rend le code. `delais` : (pool, carte), en µs."""
    lire, plan = lire or http.lire, [(x, delais[0], smoke.role(x)) for x in formes] + [
        (x, delais[1], "carte") for x in carte]
    noms = [f"{r}-{x['nom']}.bin" for x, _d, r in plan]
    if not os.path.isdir(dossier):
        raise CaptureRefusee("dossier", dossier)
    if not all(NOM.fullmatch(x["nom"]) for x, _d, _r in plan) or len(set(noms)) < len(noms):
        raise CaptureRefusee("nom", ", ".join(x["nom"] for x, _d, _r in plan))
    if any(os.path.lexists(os.path.join(dossier, n)) for n in noms + [MANIFESTE]):
        raise CaptureRefusee("fichier", dossier)
    vus, echecs, lignes = set(), 0, []
    for (x, delai, r), nom in zip(plan, noms):
        if x["espace"] and x["hote"] in vus:
            pause(1)
        vus.add(x["hote"])
        req = http.Requete(x["hote"], x["chemin"], x["port"], x["methode"], x["corps"].encode() or None)
        lu = lire(req, {}, delai=delai, tls=tls)
        with open(os.path.join(dossier, nom), "xb") as f:
            f.write(lu.octets)
        echecs += r != "carte" and lu.statut != "ok"
        code = "-" if lu.code is None else lu.code
        lignes.append(f"{nom} {hashlib.sha256(lu.octets).hexdigest()} {lu.statut} {code} {lu.depart}\n")
    with open(os.path.join(dossier, MANIFESTE), "x", encoding="utf-8") as f:
        f.writelines(lignes)
    return 1 if echecs else 0
