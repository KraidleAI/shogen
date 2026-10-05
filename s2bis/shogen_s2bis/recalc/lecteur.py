"""Lecteur en flux des journaux d'observateur de S2-bis (RB-1 ; G0 docs/adr-0029/g0-collecte/, PROPOSITION E-R-01,
E-R-02 ; FORMAT docs/adr-0029/s2bis/FORMAT-JOURNAUX-S2BIS.md §1 à §8). Ligne intègre au sens de l'écrivain de
référence (FORMAT §7.1, `collecte/journal.py` `_lire`) : terminée par 0x0A, JSON canonique, chaînée à la précédente du
fichier, première ligne `ouverture` ou `reprise`, champs typés comme l'écrivain les relit ; sinon cause nommée
(`LECTEUR/entier-long` pour un entier de plus de CHIFFRES chiffres, quel que soit le réglage `int_max_str_digits` de
l'interpréteur). Fichiers d'un préfixe dans l'ordre de la chaîne (FORMAT §6.1, §7.2)."""
import hashlib
import json
import os
import re

RESERVES = {"ouverture", "marqueur", "point", "cloture", "reprise", "trou"}
CHIFFRES = 640                         # entier JSON : 640 chiffres au plus, plus petit int_max_str_digits non nul


class RefusLecteur(Exception):
    def __init__(self, code, detail):
        super().__init__(f"{code} : {detail}")
        self.code = code


class _NonIntegre(Exception):
    pass


def _cause(code):
    def lever(*_a):
        raise _NonIntegre(code)
    return lever


def _entier(t):
    if len(t.lstrip("-")) > CHIFFRES:
        raise _NonIntegre("LECTEUR/entier-long")
    return int(t)


def _integre(ligne, etat):
    """(enregistrement, état) d'une ligne intègre, état = (seq, sha256 de la ligne, attendu, dernière fenêtre) comme
    l'écrivain le calcule ; sinon _NonIntegre(cause)."""
    if not ligne.endswith(b"\n"):
        raise _NonIntegre("LECTEUR/fin")
    try:
        e = json.loads(ligne, parse_int=_entier, parse_float=_cause("LECTEUR/flottant"),
                       parse_constant=_cause("LECTEUR/flottant"))
        canon = json.dumps(e, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode() + b"\n"
    except (ValueError, RecursionError):
        raise _NonIntegre("LECTEUR/json") from None
    if canon != ligne:
        raise _NonIntegre("LECTEUR/canonique")
    try:
        t = e["type"]
        lien = (e["seq"], e["prec"]) == etat[:2] if etat else t in ("ouverture", "reprise") and type(e["seq"]) is int
        if t in ("ouverture", "reprise"):
            attendu = e["suivante"]
        elif t in ("marqueur", "trou"):
            attendu = e["ws" if t == "marqueur" else "a"] + 0          # type de « ws + w » chez l'écrivain
        else:
            attendu = etat[2] if etat else None                  # première ligne : seules ouverture et reprise
        derniere = e["ws"] if t == "marqueur" or t not in RESERVES else etat and etat[3]
    except (KeyError, TypeError):
        raise _NonIntegre("LECTEUR/champ") from None
    if not lien:
        raise _NonIntegre("LECTEUR/chaine")
    if type(attendu) is not int or not (derniere is None or type(derniere) is int):
        raise _NonIntegre("LECTEUR/champ")
    return e, (e["seq"] + 1, hashlib.sha256(ligne).hexdigest(), attendu, derniere)


class Lecteur:
    """Journal d'un préfixe dans un dossier : `fichiers()` rend ses fichiers quotidiens dans l'ordre de la chaîne
    (jour, puis numéro de segment en entier) ; aucun fichier : refus nommé `LECTEUR/absent`."""

    def __init__(self, dossier, prefixe):
        self.dossier, self.prefixe = dossier, prefixe

    def fichiers(self):
        motif = re.compile(re.escape(self.prefixe) + r"-([0-9]{4}-[0-9]{2}-[0-9]{2})-([0-9]+)[.]jsonl")
        noms = sorted((m[1], int(m[2]), m[0]) for m in map(motif.fullmatch, os.listdir(self.dossier)) if m)
        if not noms:
            raise RefusLecteur("LECTEUR/absent", f"aucun fichier {self.prefixe}-*.jsonl dans {self.dossier}")
        return [n for _j, _k, n in noms]
