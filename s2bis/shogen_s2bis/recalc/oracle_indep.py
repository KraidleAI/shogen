"""Lecteur indépendant des journaux de S2-bis (RB-18 ; E-R-33 ; PROPOSITION du G0 de RECALC-BIS l.396, l.459, l.486,
l.539-540, l.551 ; AVIS Q-R-08). Écrit d'après le seul FORMAT (docs/adr-0029/s2bis/FORMAT-JOURNAUX-S2BIS.md) par un
autre auteur que le lecteur principal (RB-1) ; n'importe ni lui ni l'écrivain : bibliothèque standard seule.
Ligne (§1.1, §1.2, §7.1, §8.3) : octets terminés par 0x0A, objet JSON canonique, sans flottant ni NaN ; échappements
de `json` (Q-R18-3). Champs communs (§1.3) : `type` chaîne, `seq` entier, `prec` 64 chiffres hexadécimaux minuscules.
Entier de plus de CHIFFRES chiffres (signe exclu) dans un objet JSON par ailleurs lisible : refus nommé
ORACLE/entier-long, la ligne n'est pas jugée (Q-R18-2 ; E-R-01 ; SHOGEN-JSON-ENTIER-LONG-1). Fichiers (§6.1, §7.2) :
`<préfixe>-AAAA-MM-JJ-k.jsonl`, k décimal sans zéro de tête, dans l'ordre (jour, k entier) ; autres noms ignorés
(Q-R18-5)."""
import json
import os
import re

CHIFFRES = 640              # sys.int_info.str_digits_check_threshold (CPython 3.10 à 3.13) : lu sous tout réglage
NL = bytes((10,))
HEX = re.compile("[0-9a-f]{64}")


class RefusOracle(Exception):
    def __init__(self, code, detail):
        super().__init__(f"{code} : {detail}")
        self.code = code


def objet(ligne):
    """Objet canonique porté par `ligne` (octets, 0x0A final compris), ou None : la ligne n'en porte pas."""
    marques = set()

    def entier(t):
        if len(t) - t.startswith("-") > CHIFFRES:
            marques.add("long")
            return 0
        return int(t)

    def interdit(_t):
        marques.add("flottant")
        return 0
    if not ligne.endswith(NL):
        return None
    try:
        e = json.loads(ligne[:-1].decode("utf-8"), parse_int=entier, parse_float=interdit, parse_constant=interdit)
    except (ValueError, RecursionError):                    # UnicodeDecodeError et JSONDecodeError : ValueError
        return None
    if "flottant" in marques or type(e) is not dict:
        return None
    if marques:
        raise RefusOracle("ORACLE/entier-long", f"plus de {CHIFFRES} chiffres")
    try:
        forme = json.dumps(e, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8") + NL
    except (ValueError, RecursionError):                    # surrogat seul (UnicodeEncodeError), imbrication
        return None
    return e if forme == ligne else None


def champs(e):
    """Champs communs du FORMAT §1.3 ; un booléen n'est pas un entier."""
    return (type(e.get("type")) is str and type(e.get("seq")) is int and type(e.get("prec")) is str
            and HEX.fullmatch(e["prec"]) is not None)


def fichiers(dossier, prefixe):
    """Noms des fichiers du journal `prefixe` de `dossier`, dans l'ordre de la chaîne."""
    motif = re.compile(re.escape(prefixe) + "-([0-9]{4}-[0-9]{2}-[0-9]{2})-(0|[1-9][0-9]*)[.]jsonl")
    return [n for _j, _k, n in sorted((m[1], int(m[2]), m[0]) for m in map(motif.fullmatch, os.listdir(dossier)) if m)]
