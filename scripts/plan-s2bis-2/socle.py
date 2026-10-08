"""Socle du lot PLAN-S2BIS-2 (G0 docs/adr-0029/g0-plan2/G0-PLAN-S2BIS-2.md ; PERIMETRE-REDUIT.md §1, §2, §9 ; E-P2-03 à
E-P2-05, E-P2-11 (c) et (d), E-P2-12). Refus nommés ; garde de la variable de campagne sur un environnement passé en
argument ; schéma du parametres.json du lot ; huit pièces de PLAN-S2BIS contrôlées contre leurs épingles, puis commun,
regles et episodes chargés par chemin, sous ces noms et dans cet ordre (P-1) ; sous-arbres déclarés (P-3) seuls lus du
parametres.json de PLAN-S2BIS ; contrôles (c) pool D1-bis et (d) type « ecart ». Aucune barre oblique inverse : saut
de ligne par chr(10)."""
from __future__ import annotations

import json
import os

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(os.path.dirname(ICI))
PARAMETRES = os.path.join(ICI, "parametres.json")
NL = chr(10)
VARIABLE = "SHOGEN_S2_CAMPAGNE_CONTROL"
PIECES = ("commun", "regles", "episodes", "parametres", "fixtures", "sha256sums", "ep", "ep_sha256sums")
SCHEMA = {"lot": str, "rattachement": str,
          "plan_s2bis": {"chemins": dict.fromkeys(PIECES, str), "sha256": dict.fromkeys(PIECES, str), "source": str},
          "masque": {"calendrier_hors_d5": "comptes", "sautees_hors_d5": "comptes", "source": str},
          "voisinage": dict.fromkeys(("nom", "lacune", "bords", "grille", "garde", "source"), str) | {"d": int},
          "passes": {"variable": str, "A": int, "B": int, "source": str},
          "sous_arbres": {"lus": list, "epingles": list, "source": str}}


class Refus(Exception):
    """Refus nommé (E-P2-12) : code, motif, puis strate, hôte et ℓ s'ils sont connus ; ni ligne de journal ni
    valeur."""

    def __init__(self, code: str, motif: str, strate=None, hote=None, ell=None):
        self.code = code
        lieu = [f"{n} {v}" for n, v in (("strate", strate), ("hôte", hote), ("ℓ =", ell)) if v is not None]
        super().__init__(" ; ".join([f"REFUS {code} : {motif}", *lieu]))


def garde(env) -> None:
    """P2/variable si SHOGEN_S2_CAMPAGNE_CONTROL est posée dans `env` (présence, quelle que soit sa valeur)."""
    if VARIABLE in env:
        raise Refus("P2/variable", f"{VARIABLE} est posée")


def conforme(x, s) -> bool:
    """x conforme à s : dict à clés exactes ; « comptes » (dict à valeurs entières) ; liste de chaînes ; ou type exact
    (un booléen n'est pas un entier ; aucun flottant n'est admis)."""
    if isinstance(s, dict):
        return type(x) is dict and set(x) == set(s) and all(conforme(x[k], v) for k, v in s.items())
    if s == "comptes":
        return type(x) is dict and all(type(v) is int for v in x.values())
    return type(x) is s and (s is not list or all(type(e) is str for e in x))


def lire(chemin: str = PARAMETRES) -> dict:
    """parametres.json du lot conforme à SCHEMA, sans clé dupliquée ; sinon P2/parametres."""
    def paires(p):
        if len({k for k, _v in p}) < len(p):
            raise ValueError("clé dupliquée")
        return dict(p)
    try:
        with open(chemin, encoding="utf-8") as f:
            prm = json.load(f, object_pairs_hook=paires)
    except (OSError, ValueError) as e:
        raise Refus("P2/parametres", f"parametres.json du lot illisible ({type(e).__name__})") from None
    if not conforme(prm, SCHEMA):
        raise Refus("P2/parametres", "parametres.json du lot hors schéma (clé en trop ou manquante, type, flottant)")
    return prm
