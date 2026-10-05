"""Paramètres d'analyse scellés de S2-bis (RB-0 ; G0 docs/adr-0029/g0-collecte/, PROPOSITION §3.1 ; E-R-05, E-R-09,
E-R-16, E-R-17, E-R-20, E-R-25). Fichier `s2bis/config/analyse.json` lu en octets ; leur sha256 entre au paquet et à
`run_params` (E-R-04). JSON strict : clé double, nombre à virgule, constante non finie, entier de plus de 30 chiffres
refusés (lecture reprise de collecte/config.py l.20-46, par copie : la frontière interdit à `recalc` d'importer
`collecte.config`, PROPOSITION §1 pt 2). Un bloc à fixer par un lot amont (null au premier niveau) refuse le fichier,
puis le schéma (champs exacts, types, bornes). Tout écart lève RefusAnalyse (`code` nomme le refus), sans défaut ni
écrêtage. τ, P_j : fraction décimale en chaîne (« 0.005 » = 0,5 %, τ de S2, `run_campaign.py` l.120-129) ; σ, D-2 à
D-5 : secondes entières."""
import hashlib
import json

ACTIFS = ("BTC", "ETH", "USDC", "USDT")
# Planchers de σ en secondes, par classe de source (ADR-0029 l.182 : planchers d'ADR-0020).
PLANCHERS = {"place_horodatee": 30, "agregateur": 300, "oracle_chainlink": 5400, "sans_horodatage": None}


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


def _fraction(v, ou):                                        # fraction décimale écrite en chaîne
    if type(v) is not str:
        _refus("ANALYSE/fraction", f"{ou} = {v!r}")


def _nom(v, ou):                                             # unité : nom d'hôte de configuration (E-R-15)
    if type(v) is not str or not v:
        _refus("ANALYSE/unite", f"{ou} = {v!r}")


def _table(v, ou):
    """τ et σ d'un actif par classe de source : sous-ensemble non vide des classes, champs `sigma` et `tau`."""
    if type(v) is not dict or not v or v.keys() - PLANCHERS.keys():
        _refus("ANALYSE/classe", f"{ou} : {sorted(v) if type(v) is dict else v!r}")
    for classe, x in v.items():
        controler(x, {"sigma": lambda s, o: None, "tau": _fraction}, f"{ou}.{classe}")


SECONDES = ENTIER = (int, 1, None)
SCHEMA = {
    "degradation": {"d2_retard_s": SECONDES, "d3_borne_s": SECONDES, "d3_age_s": SECONDES, "d4_echecs": (int, 1, 3),
                    "d4_delai_s": SECONDES, "d5_echecs": (int, 1, 2), "d5_delai_s": SECONDES},
    "gardes": {"diviseur_n": ENTIER, "k_crit": ENTIER, "runs": ENTIER, "unites": ENTIER},
    "n_s": {"calme": ENTIER, "stress": ENTIER},
    "p_j": {"grille": [_fraction], "seuil": _fraction},
    "rotations": {"R": (int, 1, 9999), "seuil": (int, 0, None)},
    "t_max_s": (int, 60, None),
    "tau_sigma": {a: _table for a in ACTIFS},
    "tolerance_evenements": (int, 0, None),
    "unites": {a: [_nom] for a in ACTIFS},
}


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
