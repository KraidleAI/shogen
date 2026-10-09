"""Socle du lot CALIB-ACTIFS (G0 docs/adr-0029/g0-calib/, PROPOSITION §5.1, §5.7, §6.1 CA-0, corrigée par AVIS) :
refus nommés (E-CA-24) ; garde de la variable sur un environnement passé en argument (E-CA-03) ; parametres.json lu
strictement (E-CA-06, E-CA-12). Bibliothèque standard seule ; aucune barre oblique inverse (E-CA-05)."""
from __future__ import annotations

import json
import os
import re

ICI = os.path.dirname(os.path.abspath(__file__))
PARAMETRES = os.path.join(ICI, "parametres.json")
NL = chr(10)
ETIQUETTE = ("préparation de S2-bis ; calibration d'ETH, d'USDC et d'USDT sur historiques publics ; ne lit aucune "
             "donnée de S2 ni de S2-bis")
VARIABLE = "SHOGEN_S2_CAMPAGNE_CONTROL"
ACTIFS = ("ETH", "USDC", "USDT")
CLASSES = ("agregateur", "oracle_chainlink", "place_horodatee", "sans_horodatage")
HOTE = re.compile("[a-z0-9.-]{1,253}")


class Refus(Exception):
    """Refus nommé (E-CA-24) : code, motif, puis actif, classe, strate et place s'ils sont connus ; jamais une
    valeur."""

    def __init__(self, code: str, motif: str, actif=None, classe=None, strate=None, place=None):
        self.code = code
        lieu = [f"{n} {v}" for n, v in (("actif", actif), ("classe", classe), ("strate", strate), ("place", place))
                if v is not None]
        super().__init__(" ; ".join([f"REFUS {code} : {motif}", *lieu]))


def garde(env) -> None:
    """CA/variable si SHOGEN_S2_CAMPAGNE_CONTROL est posée dans `env` (présence, quelle que soit sa valeur)."""
    if VARIABLE in env:
        raise Refus("CA/variable", f"{VARIABLE} est posée")


def _par_actif(s):
    return dict.fromkeys(ACTIFS, s)


LECTURE = {"places": _par_actif(["hote"]), "n_min": _par_actif(int), "modes": _par_actif("mode"),
           "derniere_transaction": _par_actif(["hote", "vide admise"])}
SCHEMA = {"lot": str, "rattachement": str,
          "fenetre": {"debut": int, "fin": int, "source": str},
          "fenetre_descriptive": {"debut": int, "fin": int, "sans": ["hote"], "source": str},
          "strates": {"calme": [int], "stress": [int], "source": str},
          "lecture": str, "lectures": {"A": LECTURE, "A-prime": LECTURE, "source": str},
          "unites": _par_actif(["hote"]) | {"source": str},
          "classes": dict.fromkeys(CLASSES, ["hote"]) | {"source": str},
          "passes": {"variable": str, "A": int, "B": int, "source": str}}


def conforme(x, s) -> bool:
    """x conforme à s : dict à clés exactes ; [s] liste non vide ([s, « vide admise »] : vide admise) ; « hote »
    (règle HOTE) ; « mode » (calibre ou planchers_seuls) ; sinon type exact (un booléen n'est pas un entier)."""
    if isinstance(s, dict):
        return type(x) is dict and set(x) == set(s) and all(conforme(x[k], v) for k, v in s.items())
    if isinstance(s, list):
        return type(x) is list and (len(x) > 0 or len(s) > 1) and all(conforme(e, s[0]) for e in x)
    if s == "hote":
        return type(x) is str and HOTE.fullmatch(x) is not None
    if s == "mode":
        return x in ("calibre", "planchers_seuls")
    return type(x) is s


def lire(chemin: str = PARAMETRES) -> dict:
    """parametres.json du lot conforme à SCHEMA, sans clé dupliquée ni flottant ; sinon CA/parametres."""
    def paires(ps):
        if len({k for k, _v in ps}) < len(ps):
            raise ValueError("clé dupliquée")
        return dict(ps)

    def flottant(_t):
        raise ValueError("flottant")
    try:
        with open(chemin, encoding="utf-8") as f:
            prm = json.load(f, object_pairs_hook=paires, parse_float=flottant, parse_constant=flottant)
    except (OSError, ValueError) as e:
        raise Refus("CA/parametres", f"parametres.json du lot illisible ({type(e).__name__})") from None
    if not conforme(prm, SCHEMA):
        raise Refus("CA/parametres", "parametres.json du lot hors schéma")
    return prm


def lecture(prm: dict) -> dict:
    """Lecture retenue (A : six places, INV-1 = A ; A-prime : variante)."""
    return prm["lectures"][prm["lecture"]]
