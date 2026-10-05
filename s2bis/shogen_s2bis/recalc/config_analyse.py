"""Paramètres d'analyse scellés de S2-bis (RB-0 ; G0 docs/adr-0029/g0-collecte/, PROPOSITION §3.1 ; E-R-05, E-R-09,
E-R-16, E-R-17, E-R-20, E-R-25). Fichier `s2bis/config/analyse.json` lu en octets ; leur sha256 entre au paquet et à
`run_params` (E-R-04). JSON strict : clé double, nombre à virgule, constante non finie, entier de plus de 30 chiffres
refusés (lecture reprise de collecte/config.py l.20-46, par copie : la frontière interdit à `recalc` d'importer
`collecte.config`, PROPOSITION §1 pt 2). Un bloc à fixer par un lot amont (null au premier niveau) refuse le fichier,
puis le schéma (champs exacts, types, bornes ; τ, σ et noms d'unité), puis la cohérence (COHERENCE). Tout écart lève
RefusAnalyse (`code` nomme le refus), sans défaut ni écrêtage. τ, P_j : fraction décimale en chaîne (« 0.005 » =
0,5 %, τ de S2, `run_campaign.py` l.120-129) ; σ, D-2 à D-5 : secondes entières."""
import functools
import hashlib
import json
import re
from decimal import Decimal

from .rotation import HOTE

ACTIFS = ("BTC", "ETH", "USDC", "USDT")
# Planchers de σ en secondes, par classe de source (ADR-0029 l.182 : planchers d'ADR-0020) ; 0,05 % <= τ < 2,85 %
# (E-R-09 ; ADR-0029 l.181, l.183 : refus nommé, jamais d'écrêtage).
PLANCHERS = {"place_horodatee": 30, "agregateur": 300, "oracle_chainlink": 5400, "sans_horodatage": None}
TAU = (Decimal("0.0005"), Decimal("0.0285"))
FRACTION = re.compile(r"0\.[0-9]{1,20}")
# Oracles poussés hors BTC (l.188 ; C-1 et Q-RB-4 de la G2 de RB-T1) : τ >= 1,5 × seuil de déviation ; σ >= 1,5 ×
# heartbeat (ETH : 5 400 s, égal au plancher d'ADR-0020 de la classe). τ de BTC sur la grille de 0,05 % (l.181 ; celle
# des autres actifs relève du G0 de CALIB-ACTIFS, l.186). σ des places et des agrégateurs d'un actif au moins égal à
# celui de BTC de la même classe (l.189 ; « planchers seuls » pour les oracles des autres actifs, valeurs de l.188).
TAU_ORACLES = {"ETH": "0.0075", "USDC": "0.00375", "USDT": "0.00375"}
SIGMA_ORACLES = {"USDC": 124200, "USDT": 129600}
GRILLE_BTC = Decimal("0.0005")
SIGMA_BTC = ("place_horodatee", "agregateur")


class RefusAnalyse(Exception):
    def __init__(self, code, detail):
        super().__init__(f"{code} : {detail}")
        self.code = code


def _refus(code, detail):
    raise RefusAnalyse(code, detail)


def _objet(paires):
    vu = {}
    for k, v in paires:
        vu[k] = _refus("ANALYSE/cle-double", k) if k in vu else v
    return vu


def _entier(t):
    return int(t) if len(t) <= 30 else _refus("ANALYSE/borne", f"entier de {len(t)} chiffres")


def _fraction(v, ou):                                        # fraction décimale écrite en chaîne, 0 < x < 1
    if type(v) is not str or not FRACTION.fullmatch(v) or not Decimal(v):
        _refus("ANALYSE/fraction", f"{ou} = {v!r}")


def _nom(v, ou):
    """Unité : nom d'hôte de configuration (E-R-15), règle HOTE des décalages (rotation.py ; Q-RB-13 de la G2 de RB-T1,
    resserrement du complément (3) de l'AVIS Q-R-02)."""
    if type(v) is not str or not HOTE.fullmatch(v):
        _refus("ANALYSE/unite", f"{ou} = {v!r}")


def _table(actif, v, ou):
    """τ et σ d'un actif par classe de source : sous-ensemble non vide des classes ; σ null pour les places sans
    horodatage (staleness non évaluable, `r1.classify_ecart`), entier au moins égal au plancher ailleurs (celui de la
    classe, et celui de l'oracle de l'actif) ; τ au moins égal au plancher de l'oracle de l'actif, sur la grille pour
    BTC."""
    if type(v) is not dict or not v or v.keys() - PLANCHERS.keys():
        _refus("ANALYSE/classe", f"{ou} : {sorted(v) if type(v) is dict else v!r}")
    for classe, x in v.items():
        controler(x, {"sigma": lambda s, o: None, "tau": _fraction}, f"{ou}.{classe}")
        if not TAU[0] <= Decimal(x["tau"]) < TAU[1]:
            _refus("ANALYSE/borne", f"{ou}.{classe}.tau = {x['tau']} hors [0.0005, 0.0285)")
        if classe == "oracle_chainlink" and Decimal(x["tau"]) < Decimal(TAU_ORACLES.get(actif, "0")):
            _refus("ANALYSE/tau-plancher", f"{ou}.{classe}.tau = {x['tau']} (plancher {TAU_ORACLES[actif]})")
        if actif == "BTC" and Decimal(x["tau"]) % GRILLE_BTC:
            _refus("ANALYSE/tau-grille", f"{ou}.{classe}.tau = {x['tau']} hors de la grille de {GRILLE_BTC}")
        plancher, s = PLANCHERS[classe], x["sigma"]
        if classe == "oracle_chainlink":
            plancher = max(plancher, SIGMA_ORACLES.get(actif, 0))
        if (s is not None) if plancher is None else (type(s) is not int or s < plancher):
            _refus("ANALYSE/sigma", f"{ou}.{classe}.sigma = {s!r} (plancher {plancher})")


SECONDES = ENTIER = (int, 1, None)
SCHEMA = {
    "degradation": {"d2_retard_s": SECONDES, "d3_borne_s": SECONDES, "d3_age_s": SECONDES, "d4_echecs": (int, 1, 3),
                    "d4_delai_s": SECONDES, "d5_echecs": (int, 1, 2), "d5_delai_s": SECONDES},
    "gardes": {"diviseur_n": ENTIER, "k_crit": ENTIER, "runs": ENTIER, "unites": ENTIER},
    "n_s": {"calme": ENTIER, "stress": ENTIER},
    "p_j": {"grille": [_fraction], "seuil": _fraction},
    "rotations": {"R": (int, 9999, 9999), "seuil": (int, 99, 99)},        # Q-RB-6 : valeurs de l.139, l.200, l.202
    "t_max_s": (int, 60, None),
    "tau_sigma": {a: functools.partial(_table, a) for a in ACTIFS},
    "tolerance_evenements": (int, 0, None),
    "unites": {a: [_nom] for a in ACTIFS},
}


def _croissante(xs):
    return all(a < b for a, b in zip(xs, xs[1:]))


# (nom du refus, prédicat). Unités : ordre strict des points de code (« ordre alphabétique », ADR-0029 l.200) ; pools
# d'ETH, d'USDC et d'USDT pris parmi les hôtes de BTC (l.173) ; alpha : C <= seuil ⇔ (C + 1)/(R + 1) <= 0,01 (l.202),
# seconde garde de R et du seuil (Q-RB-6) ; sigma-btc (l.189) : σ_BTC de la classe exigé, une classe absente de BTC
# est refusée (pools des autres actifs pris parmi les hôtes de BTC, l.173).
COHERENCE = (
    ("alpha", lambda d: d["rotations"]["R"] + 1 == 100 * (d["rotations"]["seuil"] + 1)),
    ("t_max-grille", lambda d: d["t_max_s"] % 60 == 0),
    ("p_j-grille", lambda d: _croissante([Decimal(x) for x in d["p_j"]["grille"]])),
    ("p_j-seuil", lambda d: Decimal(d["p_j"]["seuil"]) in [Decimal(x) for x in d["p_j"]["grille"]]),
    ("unites-ordre", lambda d: all(_croissante(u) for u in d["unites"].values())),
    ("unites-btc", lambda d: all(set(u) <= set(d["unites"]["BTC"]) for u in d["unites"].values())),
    ("sigma-btc", lambda d: all(c in d["tau_sigma"]["BTC"] and x["sigma"] >= d["tau_sigma"]["BTC"][c]["sigma"]
                                for t in d["tau_sigma"].values() for c, x in t.items() if c in SIGMA_BTC)),
)


def charger(chemin):
    """(données, sha256 hexadécimal des octets lus)."""
    with open(chemin, "rb") as f:
        octets = f.read()
    try:
        d = json.loads(octets.decode("utf-8"), object_pairs_hook=_objet, parse_int=_entier,
                       parse_float=lambda t: _refus("ANALYSE/flottant", t),
                       parse_constant=lambda t: _refus("ANALYSE/non-fini", t))
    except (ValueError, RecursionError) as e:                      # RecursionError : imbrication excessive
        raise RefusAnalyse("ANALYSE/json", e) from None
    if vides := sorted(k for k in SCHEMA if type(d) is dict and k in d and d[k] is None):
        _refus("ANALYSE/a-fixer", ", ".join(vides))
    controler(d, SCHEMA)
    for nom, regle in COHERENCE:
        if not regle(d):
            _refus("ANALYSE/incoherent", nom)
    return d, hashlib.sha256(octets).hexdigest()


def controler(v, schema, ou="$"):
    """Lève RefusAnalyse au premier écart de `v` à `schema` : objet aux champs exacts ; [s] liste non vide ; (type,
    min, max) feuille, max None sans borne haute ; fonction (valeur, chemin) pour une feuille propre."""
    if callable(schema):
        schema(v, ou)
    elif isinstance(schema, dict):
        if type(v) is not dict:
            _refus("ANALYSE/type", f"{ou} : objet attendu")
        for code, noms in (("ANALYSE/champ-absent", schema.keys() - v.keys()),
                           ("ANALYSE/champ-inconnu", v.keys() - schema.keys())):
            if noms:
                _refus(code, f"{ou} : {', '.join(sorted(noms))}")
        for k, s in schema.items():
            controler(v[k], s, f"{ou}.{k}")
    elif isinstance(schema, list):
        if type(v) is not list or not v:
            _refus("ANALYSE/type", f"{ou} : liste non vide attendue")
        for i, x in enumerate(v):
            controler(x, schema[0], f"{ou}[{i}]")
    else:
        genre, bas, haut = schema
        if type(v) is not genre:
            _refus("ANALYSE/type", f"{ou} : {genre.__name__} attendu")
        if v < bas or haut is not None and v > haut:
            _refus("ANALYSE/borne", f"{ou} = {v!r} hors [{bas}, {haut}]")
