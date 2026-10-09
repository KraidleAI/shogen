"""Socle du lot CALIB-ACTIFS (G0 docs/adr-0029/g0-calib/, PROPOSITION §5.1, §5.7, §6.1 CA-0, corrigée par AVIS) :
refus nommés (E-CA-24) ; garde de la variable sur un environnement passé en argument (E-CA-03) ; parametres.json lu
strictement (E-CA-06, E-CA-12) ; tau_sigma.txt de PLAN-S2BIS sous son épingle (E-CA-02). Bibliothèque standard
seule ; aucune barre oblique inverse (E-CA-05)."""
from __future__ import annotations

import hashlib
import json
import os
import re
from decimal import Decimal
from fractions import Fraction

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(os.path.dirname(ICI))
PARAMETRES = os.path.join(ICI, "parametres.json")
NL = chr(10)
ETIQUETTE = ("préparation de S2-bis ; calibration d'ETH, d'USDC et d'USDT sur historiques publics ; ne lit aucune "
             "donnée de S2 ni de S2-bis")
VARIABLE = "SHOGEN_S2_CAMPAGNE_CONTROL"
ACTIFS = ("ETH", "USDC", "USDT")
CLASSES = ("agregateur", "oracle_chainlink", "place_horodatee", "sans_horodatage")
HOTE = re.compile("[a-z0-9.-]{1,253}")
DECIMAL = re.compile("[0-9]+(?:[.][0-9]+)?")
F3 = ("USDC", "USDT")                   # classes exploratoires : seules admises en « planchers seuls » (l.191)
BLOC = "[VALEURS POUR LE PAQUET DE S2-BIS]"         # bloc machine de tau_sigma.txt (scripts/plan-s2bis/tau_sigma.py)
LIGNE_BTC = re.compile("(tau|sigma) (" + "|".join(CLASSES) + ") (?:([0-9]+(?:[.][0-9]+)?)|REFUS .*|- .*|aucun)")


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
          "passes": {"variable": str, "A": int, "B": int, "source": str},
          "plan_s2bis": {"tau_sigma": str, "sha256": str, "source": str},
          "chainlink": _par_actif({"proxy": str, "seuil": "dec", "heartbeat_s": int})
          | {"facteur": "dec", "source": str},
          "oracles_attendus": {"tau": _par_actif("dec"), "sigma_s": _par_actif(int), "source": str},
          "reseau": {"agent": str, "delai_s": int, "essais": int, "pause_s": int, "source": str}}


def conforme(x, s) -> bool:
    """x conforme à s : dict à clés exactes ; [s] liste non vide ([s, « vide admise »] : vide admise) ; « hote »
    (règle HOTE) ; « mode » (calibre ou planchers_seuls) ; sinon type exact (un booléen n'est pas un entier)."""
    if isinstance(s, dict):
        return type(x) is dict and set(x) == set(s) and all(conforme(x[k], v) for k, v in s.items())
    if isinstance(s, list):
        return type(x) is list and (len(x) > 0 or len(s) > 1) and all(conforme(e, s[0]) for e in x)
    if s == "hote":
        return type(x) is str and HOTE.fullmatch(x) is not None
    if s == "dec":
        return type(x) is str and DECIMAL.fullmatch(x) is not None
    if s == "mode":
        return x in ("calibre", "planchers_seuls")
    return type(x) is s


def _trie(xs) -> bool:
    return all(a < b for a, b in zip(xs, xs[1:]))


def coherent(p: dict) -> bool:
    """Fenêtres alignées à la minute, non vides ; strates partition de 0..6 ; unités triées, classées une fois ;
    par lecture : places triées parmi les unités, N_min entre 2 et le nombre de places, dernière transaction parmi les
    places horodatées de la lecture, planchers seuls pour F3 seulement ; lecture retenue déclarée."""
    fen = [p[k] for k in ("fenetre", "fenetre_descriptive")]
    classees = [h for k in CLASSES for h in p["classes"][k]]
    ok = all(f["debut"] % 60 == 0 == f["fin"] % 60 and f["debut"] < f["fin"] for f in fen)
    ok = ok and sorted(p["strates"]["calme"] + p["strates"]["stress"]) == list(range(7))
    ok = ok and len(classees) == len(set(classees)) and all(_trie(p["unites"][a]) for a in ACTIFS)
    ok = ok and all(set(p["unites"][a]) <= set(classees) for a in ACTIFS) and p["lecture"] in ("A", "A-prime")
    for lec in (p["lectures"]["A"], p["lectures"]["A-prime"]):
        for a in ACTIFS:
            pl = lec["places"][a]
            ok = ok and _trie(pl) and set(pl) <= set(p["unites"][a]) and 2 <= lec["n_min"][a] <= len(pl)
            ok = ok and set(lec["derniere_transaction"][a]) <= set(pl) & set(p["classes"]["place_horodatee"])
            ok = ok and (lec["modes"][a] == "calibre" or a in F3)
    return ok


def lire(chemin: str = PARAMETRES) -> dict:
    """parametres.json du lot conforme à SCHEMA et cohérent, sans clé dupliquée ni flottant ; sinon CA/parametres."""
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
    if not conforme(prm, SCHEMA) or not coherent(prm):
        raise Refus("CA/parametres", "parametres.json du lot hors schéma ou incohérent")
    return prm


def lecture(prm: dict) -> dict:
    """Lecture retenue (A : six places, INV-1 = A ; A-prime : variante)."""
    return prm["lectures"][prm["lecture"]]


def empreinte(chemin: str) -> str:
    h = hashlib.sha256()
    with open(chemin, "rb") as f:
        for bloc in iter(lambda: f.read(1 << 20), b""):
            h.update(bloc)
    return h.hexdigest()


def tau_sigma(prm: dict, racine: str = RACINE) -> str:
    """Chemin de tau_sigma.txt de PLAN-S2BIS, de sha256 égal à l'épingle (E-CA-02 ; T-CA-SOC-1) ; sinon CA/plan-s2bis.
    Aucun octet n'en est interprété avant ce contrôle."""
    chemin = os.path.join(racine, prm["plan_s2bis"]["tau_sigma"])
    if not os.path.isfile(chemin) or empreinte(chemin) != prm["plan_s2bis"]["sha256"]:
        raise Refus("CA/plan-s2bis", "tau_sigma.txt absent ou de sha256 différent de l'épingle")
    return chemin


def valeurs_btc(chemin: str) -> dict:
    """{(tau ou sigma, classe) : Decimal} du bloc machine de tau_sigma.txt, forme apprise du code qui l'écrit
    (scripts/plan-s2bis/tau_sigma.py l.67-78), jamais du fichier : une ligne REFUS, « - » ou « aucun » ne donne aucune
    valeur (absente : CA/btc à l'usage). Bloc absent ou répété, ligne hors forme, valeur répétée : CA/btc."""
    with open(chemin, encoding="utf-8") as f:
        lignes = f.read().split(NL)
    if lignes.count(BLOC) != 1:
        raise Refus("CA/btc", "bloc machine de tau_sigma.txt absent ou répété")
    out, vues = {}, set()
    for x in filter(None, lignes[lignes.index(BLOC) + 1:]):
        m = LIGNE_BTC.fullmatch(x)
        if not m or (m[1], m[2]) in vues:
            raise Refus("CA/btc", "ligne du bloc machine de tau_sigma.txt hors forme ou répétée")
        vues.add((m[1], m[2]))
        if m[3] is not None:
            out[m[1], m[2]] = Decimal(m[3])
    return out


def minutes(fen: dict) -> range:
    """Débuts des minutes de la fenêtre [debut ; fin) (E-CA-16 ; T-CA-FEN-1)."""
    return range(fen["debut"], fen["fin"], 60)


def strate(t: int, prm: dict) -> str:
    """Strate de la minute t : jour de la semaine UTC (lundi = 0 ; le 1970-01-01 est un jeudi), calendrier de S2."""
    jour = (t // 86400 + 3) % 7
    return "stress" if jour in prm["strates"]["stress"] else "calme"


def oracles(prm: dict) -> dict:
    """{actif : (τ, σ)} des oracles, planchers exacts jamais arrondis à la grille (l.188, l.189 ; E-CA-23 c, f) :
    τ = facteur × seuil de déviation, σ = facteur × heartbeat, en rationnels ; égalité exigée aux valeurs attendues
    (config_analyse.py l.28-29), sinon CA/chainlink (E-CA-10 ; jamais une valeur devinée)."""
    c, att, out = prm["chainlink"], prm["oracles_attendus"], {}
    for a in ACTIFS:
        tau = Decimal(c["facteur"]) * Decimal(c[a]["seuil"])
        sigma = Fraction(c["facteur"]) * c[a]["heartbeat_s"]
        if tau != Decimal(att["tau"][a]) or sigma != att["sigma_s"][a]:
            raise Refus("CA/chainlink", "plancher d'oracle différent de la valeur attendue", a, "oracle_chainlink")
        out[a] = (Decimal(att["tau"][a]), att["sigma_s"][a])
    return out


def ecrire(dossier: str, nom: str, lignes: list) -> str:
    """Sortie `nom` : étiquette mot pour mot en première ligne (E-CA-04), puis lignes ; écrite en .partiel puis
    renommée (E-CA-05). Rend le chemin."""
    cible = os.path.join(dossier, nom)
    with open(cible + ".partiel", "w", encoding="utf-8", newline=NL) as f:
        f.write(NL.join([ETIQUETTE, *lignes]) + NL)
    os.replace(cible + ".partiel", cible)
    return cible
