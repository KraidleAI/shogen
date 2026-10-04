"""Configurations scellées (CB-0, E-C-02 ; ADR-0029 §2.8 l.217, §2.9 l.238) : fichier JSON lu en octets ; le sha256 de
ces octets entre au paquet et à `run_params` ; contrôle par schéma (champs exacts, types, bornes incluses), puis par
règles de cohérence. Tout écart lève RefusConfig, dont `code` nomme le refus ; ni défaut, ni écrêtage ; un nombre à
virgule est refusé (valeurs exactes : décimal en chaîne). Schéma : dict = objet aux champs exacts ; [s] = liste non
vide d'éléments de schéma s ; (type, min, max) = feuille (bornes sur la longueur pour str ; None, None pour bool)."""
import hashlib
import json


class RefusConfig(Exception):
    def __init__(self, code, detail):
        super().__init__(f"{code} : {detail}")
        self.code = code


def _refus(code, detail):
    raise RefusConfig(code, detail)


def _objet(paires):
    vu = {}
    for k, v in paires:
        vu[k] = _refus("CONFIG/cle-double", k) if k in vu else v
    return vu


def _entier(t):
    """Au-delà de 30 caractères, refus nommé plutôt que l'erreur générique de conversion (Python ≥ 3.11)."""
    return int(t) if len(t) <= 30 else _refus("CONFIG/borne", f"entier de {len(t)} chiffres")


def charger(chemin, schema, coherence=()):
    """(données, sha256 hexadécimal des octets lus) ; `coherence` : paires (nom, prédicat sur les données)."""
    with open(chemin, "rb") as f:
        octets = f.read()
    try:
        donnees = json.loads(octets.decode("utf-8"), object_pairs_hook=_objet, parse_int=_entier,
                             parse_float=lambda t: _refus("CONFIG/flottant", t),
                             parse_constant=lambda t: _refus("CONFIG/non-fini", t))
    except (ValueError, RecursionError) as e:                      # RecursionError : imbrication excessive
        raise RefusConfig("CONFIG/json", e) from None
    controler(donnees, schema)
    for nom, regle in coherence:
        if not regle(donnees):
            _refus("CONFIG/incoherent", nom)
    return donnees, hashlib.sha256(octets).hexdigest()


def controler(v, schema, ou="$"):
    """Lève RefusConfig au premier écart de `v` à `schema` ; le détail porte le chemin JSON."""
    if isinstance(schema, dict):
        if type(v) is not dict:
            _refus("CONFIG/type", f"{ou} : objet attendu")
        for code, noms in (("CONFIG/champ-absent", schema.keys() - v.keys()),
                           ("CONFIG/champ-inconnu", v.keys() - schema.keys())):
            if noms:
                _refus(code, f"{ou} : {', '.join(sorted(noms))}")
        for k, s in schema.items():
            controler(v[k], s, f"{ou}.{k}")
    elif isinstance(schema, list):
        if type(v) is not list or not v:
            _refus("CONFIG/type", f"{ou} : liste non vide attendue")
        for i, x in enumerate(v):
            controler(x, schema[0], f"{ou}[{i}]")
    else:
        genre, bas, haut = schema
        if type(v) is not genre:
            _refus("CONFIG/type", f"{ou} : {genre.__name__} attendu")
        if genre is not bool and not bas <= (len(v) if genre is str else v) <= haut:
            _refus("CONFIG/borne", f"{ou} = {v!r} hors [{bas}, {haut}]")
