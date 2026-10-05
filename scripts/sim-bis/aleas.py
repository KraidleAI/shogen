"""Aléas du lot SIM-BIS (G0 docs/adr-0029/g0-sim/G0-SIM-BIS.md ; sous-lot SB-1 ; E-S-41, E-S-42) : flux par (cellule,
réplication, composant, indice) dérivés de SHA-256, dont seule la méthode random() est rendue ; graine de règle par
réplication."""
import hashlib
import random

import commun


def _texte(v, nom: str) -> str:
    if type(v) is str and v != "" and v.isascii() and "|" not in v:
        return v
    raise commun.Refus("ALEAS/champ", f"{nom} = {v!r} : texte ASCII non vide, sans « | »")


def _rang(v, nom: str) -> str:
    if type(v) is int and v >= 0:
        return str(v)
    raise commun.Refus("ALEAS/champ", f"{nom} = {v!r} : entier ≥ 0")


def chaine(a: dict, cellule: str, i: int, composant=None, indice=None) -> str:
    """« <prefixe>|<graine>|<cellule>|<i> », suivie de « |<composant>|<indice> » pour un flux (E-S-41) ; entiers en
    décimal sans zéro de tête. `a` : section « aleas » de parametres.json."""
    champs = [a["prefixe"], str(a["graine"]), _texte(cellule, "cellule"), _rang(i, "i")]
    if composant is not None or indice is not None:
        champs += [_texte(composant, "composant"), _rang(indice, "indice")]
    return "|".join(champs)


def graine_flux(a: dict, cellule: str, i: int, composant: str, indice: int) -> int:
    """Entier big-endian des 8 premiers octets de SHA-256 de la chaîne ASCII du flux (E-S-41)."""
    return int.from_bytes(hashlib.sha256(chaine(a, cellule, i, composant, indice).encode("ascii")).digest()[:8], "big")


def flux(a: dict, cellule: str, i: int, composant: str, indice: int):
    """Méthode random() liée d'un random.Random semé par graine_flux : la seule méthode appelée (E-S-42)."""
    return random.Random(graine_flux(a, cellule, i, composant, indice)).random


def graine_regle(a: dict, cellule: str, i: int) -> str:
    """Graine de règle de la réplication : SHA-256 hexadécimal (minuscules) de « <prefixe>|<graine>|<cellule>|<i> »."""
    return hashlib.sha256(chaine(a, cellule, i).encode("ascii")).hexdigest()
