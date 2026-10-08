"""Socle du lot PLAN-S2BIS-2 (G0 docs/adr-0029/g0-plan2/G0-PLAN-S2BIS-2.md ; PERIMETRE-REDUIT.md §1, §2, §9 ; E-P2-03 à
E-P2-05, E-P2-11 (c) et (d), E-P2-12). Refus nommés ; garde de la variable de campagne sur un environnement passé en
argument ; schéma du parametres.json du lot ; huit pièces de PLAN-S2BIS contrôlées contre leurs épingles, puis commun,
regles et episodes chargés par chemin, sous ces noms et dans cet ordre (P-1) ; sous-arbres déclarés (P-3) seuls lus du
parametres.json de PLAN-S2BIS ; contrôles (c) pool D1-bis et (d) type « ecart ». Aucune barre oblique inverse : saut
de ligne par chr(10)."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(os.path.dirname(ICI))
PARAMETRES = os.path.join(ICI, "parametres.json")
NL = chr(10)
VARIABLE = "SHOGEN_S2_CAMPAGNE_CONTROL"
MODULES = ("commun", "regles", "episodes")
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


def empreinte(chemin: str) -> str:
    with open(chemin, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def piece(prm: dict, cle: str) -> str:
    """Chemin réel de la pièce `cle` (relatif à la racine du dépôt), de sha256 égal à son épingle ; sinon
    P2/plan-s2bis."""
    p = prm["plan_s2bis"]
    chemin = os.path.realpath(os.path.join(RACINE, p["chemins"][cle]))
    if not os.path.isfile(chemin) or empreinte(chemin) != p["sha256"][cle]:
        raise Refus("P2/plan-s2bis", f"pièce « {cle} » de PLAN-S2BIS absente ou de sha256 différent de l'épingle")
    return chemin


def charger_module(nom: str, chemin: str):
    """Module `nom` du fichier `chemin` (déjà contrôlé) ; module de ce nom chargé d'ailleurs : P2/plan-s2bis."""
    if nom not in sys.modules:
        spec = importlib.util.spec_from_file_location(nom, chemin)
        sys.modules[nom] = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(sys.modules[nom])
    if os.path.realpath(getattr(sys.modules[nom], "__file__", None) or "") != chemin:
        raise Refus("P2/plan-s2bis", f"module {nom} chargé hors de son chemin épinglé")
    return sys.modules[nom]


def charger(prm: dict) -> tuple:
    """Huit pièces contrôlées avant tout import ; commun, regles, episodes chargés (P-1) ; parametres.json de
    PLAN-S2BIS réduit aux sous-arbres et épingles déclarés (P-3) ; lignes d'EP. Rend (chemins, modules, ps2, ep)."""
    chemins = {k: piece(prm, k) for k in PIECES}
    mods = {n: charger_module(n, chemins[n]) for n in MODULES}
    cles = prm["sous_arbres"]["lus"] + prm["sous_arbres"]["epingles"]
    with open(chemins["parametres"], encoding="utf-8") as f:
        brut = json.load(f)
    if any(k not in brut for k in cles):
        raise Refus("P2/plan-s2bis", "sous-arbre déclaré absent du parametres.json de PLAN-S2BIS")
    with open(chemins["ep"], encoding="utf-8") as f:
        ep = f.read().split(NL)
    return chemins, mods, {k: brut[k] for k in cles}, ep


def controle_d(ps2: dict, r1) -> None:
    """(d) : type « ecart » de PLAN-S2BIS = r1.ECARTS ; sinon P2/ecarts."""
    if sorted(ps2["episodes"]["types"]["ecart"]) != sorted(e.value for e in r1.ECARTS):
        raise Refus("P2/ecarts", "type « ecart » de PLAN-S2BIS différent de r1.ECARTS")


def ligne_pool_bis(d: dict) -> str:
    """Ligne « pool D1-bis » de l'en-tête de PLAN-S2BIS (forme de PS2 commun.py l.192-194)."""
    return ("pool D1-bis : " + " ; ".join(f"« {s} » {len(v)} hôtes" for s, v in d["pools_bis"].items())
            + " ; retraits : " + (" ; ".join(f"« {s} » {h} ({f}, ok {k} sur n = {n}, {m})"
                                             for s, h, f, k, n, m in d["retraits_bis"]) or "aucun"))


def controle_c(d: dict, ps2: dict, ep: list) -> None:
    """(c) : pool D1-bis de chaque strate = flux de pool_d1bis.unites, dans leur ordre ; aucun retrait ; ligne
    « pool D1-bis » = EP l.8, chaîne pour chaîne ; sinon P2/pool."""
    flux = list(ps2["pool_d1bis"]["unites"].values())
    for st in ps2["strates"]:
        if d["pools_bis"].get(st) != flux:
            raise Refus("P2/pool", "pool D1-bis de la strate différent des unités de PLAN-S2BIS", st)
    if d["retraits_bis"] or ep[7:8] != [ligne_pool_bis(d)]:
        raise Refus("P2/pool", "retrait au pool D1-bis, ou ligne « pool D1-bis » différente d'EP l.8")
