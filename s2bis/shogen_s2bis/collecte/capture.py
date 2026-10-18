"""Capture des octets (INT-P2-16 ; Q-5 adjugée le 2026-10-17 ; AVIS Q-C-05 l.94 ; E-C-37, E-C-40 ; FORMAT §19) : une
lecture de chaque forme du pool et du témoin (`formes.json`), puis de la carte (`carte.json`), en série, comme le smoke
(une seconde au moins avant une nouvelle lecture d'un hôte à `espace` vrai) ; les octets bruts du corps de chacune
dans `<dossier>/<rôle>-<forme>.bin` (rôle de `smoke.role`, ou `carte`), et une ligne par lecture dans
`<dossier>/captures.txt` : fichier, sha256 des octets, statut, code HTTP, départ (µs UTC). Aucun décodage ; rien
n'est imprimé, ni octet, ni prix (ADR-0029 l.222). Refus avant toute lecture (CaptureRefusee, motif `dossier`, `nom`
ou `fichier`) : dossier absent, nom de forme hors de NOM, fichier déjà présent (jamais écrasé). Lecture HTTP et pause
injectables : tests sur fixtures, sans réseau. Code 0 si toutes les lectures du pool et du témoin sont `ok` ;
1 sinon. GEL-4 (SHOGEN-S2BIS-CAPTURE-PARTIELLE-1 ; FORMAT §19.5) : le manifeste est créé en exclusif avant la première
lecture, et sa ligne écrite et vidée (`flush`) après chaque fichier ; `reprise` complète une capture coupée : lignes
lues, sha256 de chaque fichier listé recontrôlé (refus `somme`), formes listées sautées, fichier présent non listé
refusé (`fichier`), manifeste absent ou ligne illisible refusés (`manifeste`), lectures restantes ajoutées. C-4 de la
G2 du lot : à la reprise, manifeste et fichiers listés ouverts sans suivre de lien ni attendre, fichier ordinaire
exigé (`_ordinaire`), manifeste en ajout : rien n'est lu ni écrit hors du dossier, un tube nommé ne bloque pas."""
import hashlib
import os
import re
import stat
import time

from shogen_s2bis.collecte import http, smoke

NOM = re.compile("[a-z0-9_][a-z0-9_.-]{0,63}")                     # nom de forme sûr comme nom de fichier
MANIFESTE = "captures.txt"


class CaptureRefusee(Exception):
    def __init__(self, motif, detail):
        super().__init__(f"{motif} : {detail}")


def _ordinaire(chemin, drapeaux):
    """Descripteur de `chemin` ouvert sans suivre de lien ni attendre (O_NOFOLLOW, O_NONBLOCK), fichier ordinaire
    exigé (C-4 de la G2) ; sinon OSError."""
    fd = os.open(chemin, drapeaux | os.O_NOFOLLOW | os.O_NONBLOCK)
    if not stat.S_ISREG(os.fstat(fd).st_mode):
        os.close(fd)
        raise OSError(f"pas un fichier ordinaire : {os.path.basename(chemin)}")
    return fd


def _listes(dossier, noms):
    """{fichier : statut} du manifeste d'une capture à reprendre (GEL-4) : lignes complètes de cinq champs, chacune d'un
    fichier de `noms`, une fois, dont le sha256 des octets est celui de la ligne ; sinon CaptureRefusee."""
    try:
        with open(_ordinaire(os.path.join(dossier, MANIFESTE), os.O_RDONLY), "rb") as f:
            texte = f.read().decode("utf-8")
    except (OSError, UnicodeError) as e:
        raise CaptureRefusee("manifeste", type(e).__name__) from None
    if texte and not texte.endswith("\n"):
        raise CaptureRefusee("manifeste", "dernière ligne coupée")
    lus = {}
    for ligne in texte.split("\n")[:-1]:
        c = ligne.split(" ")
        if len(c) != 5 or c[0] not in noms or c[0] in lus:
            raise CaptureRefusee("manifeste", ligne[:80])
        try:
            with open(_ordinaire(os.path.join(dossier, c[0]), os.O_RDONLY), "rb") as f:
                egal = hashlib.sha256(f.read()).hexdigest() == c[1]
        except OSError:
            egal = False
        if not egal:
            raise CaptureRefusee("somme", c[0])
        lus[c[0]] = c[2]
    return lus


def capturer(formes, carte, delais, dossier, lire=None, pause=time.sleep, tls=http.CONTEXTE, reprise=False):
    """Écrit le manifeste, puis les octets de chaque lecture et sa ligne ; rend le code. `delais` : (pool, carte), en
    µs ; `reprise` : complète la capture du manifeste présent (GEL-4)."""
    lire, plan = lire or http.lire, [(x, delais[0], smoke.role(x)) for x in formes] + [
        (x, delais[1], "carte") for x in carte]
    noms = [f"{r}-{x['nom']}.bin" for x, _d, r in plan]
    if not os.path.isdir(dossier):
        raise CaptureRefusee("dossier", dossier)
    if not all(NOM.fullmatch(x["nom"]) for x, _d, _r in plan) or len(set(noms)) < len(noms):
        raise CaptureRefusee("nom", ", ".join(x["nom"] for x, _d, _r in plan))
    lus = _listes(dossier, noms) if reprise else {}
    if any(os.path.lexists(os.path.join(dossier, n)) for n in noms + [MANIFESTE] * (not reprise) if n not in lus):
        raise CaptureRefusee("fichier", dossier)
    vus, echecs, chemin = set(), 0, os.path.join(dossier, MANIFESTE)
    try:                                          # C-4 de la G2 : à la reprise, ajout sans suivre de lien
        cible = _ordinaire(chemin, os.O_WRONLY | os.O_APPEND) if reprise else chemin
    except OSError as e:
        raise CaptureRefusee("manifeste", type(e).__name__) from None
    with open(cible, "a" if reprise else "x", encoding="utf-8") as m:
        for (x, delai, r), nom in zip(plan, noms):
            if nom in lus:                                          # forme listée : sautée, son statut compte
                echecs += r != "carte" and lus[nom] != "ok"
                continue
            if x["espace"] and x["hote"] in vus:
                pause(1)
            vus.add(x["hote"])
            req = http.Requete(x["hote"], x["chemin"], x["port"], x["methode"], x["corps"].encode() or None)
            lu = lire(req, {}, delai=delai, tls=tls)
            with open(os.path.join(dossier, nom), "xb") as f:
                f.write(lu.octets)
            echecs += r != "carte" and lu.statut != "ok"
            code = "-" if lu.code is None else lu.code
            m.write(f"{nom} {hashlib.sha256(lu.octets).hexdigest()} {lu.statut} {code} {lu.depart}\n")
            m.flush()
    return 1 if echecs else 0
