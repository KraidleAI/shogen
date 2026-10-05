"""Socle du lot SIM-BIS (G0 docs/adr-0029/g0-sim/G0-SIM-BIS.md : PROPOSITION corrigée par AVIS ; sous-lot SB-0 ;
E-S-02, E-S-03, E-S-43) : parametres.json sous schéma fermé, garde de la variable de campagne. Bibliothèque standard
seule ; aucune barre oblique inverse dans ce fichier (saut de ligne : chr(10))."""
import hashlib
import json
import os

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(os.path.dirname(ICI))
PARAMETRES = os.path.join(ICI, "parametres.json")
VARIABLE = "SHOGEN_S2_CAMPAGNE_CONTROL"
NL = chr(10)


class Refus(Exception):
    """Refus nommé : `code` de la forme « DOMAINE/motif », puis le détail."""

    def __init__(self, code: str, detail: str = ""):
        super().__init__(f"{code} : {detail}")
        self.code = code


def texte(v) -> bool:
    return type(v) is str and v != ""


def hex64(v) -> bool:
    return type(v) is str and len(v) == 64 and all(c in "0123456789abcdef" for c in v)


ENTREE = {"chemin": texte, "sha256": hex64}
SCHEMA = {"lot": texte, "schema": texte, "rattachement": texte,
          "entrees": {"sommes": ENTREE, "episodes": ENTREE, "source": texte}}


def controler(v, s, ou: str = "parametres") -> None:
    """`v` contre le schéma `s` : dict = clés exactes, contrôle récursif ; sinon prédicat. Refus PARAMETRES/schema."""
    if isinstance(s, dict):
        if type(v) is not dict or sorted(v) != sorted(s):
            raise Refus("PARAMETRES/schema", f"{ou} : {sorted(v) if type(v) is dict else type(v).__name__}, "
                                             f"attendu {sorted(s)}")
        for k in sorted(s):
            controler(v[k], s[k], f"{ou}.{k}")
    elif not s(v):
        raise Refus("PARAMETRES/schema", f"{ou} : {v!r} refusé ({s.__name__})")


def garde_campagne(environ=None) -> None:
    """Refus si la variable de la copie scellée de S2 est posée, même vide (E-S-02 ; ADR-0028 annexe D.4 a)."""
    if VARIABLE in (os.environ if environ is None else environ):
        raise Refus("CAMPAGNE/variable", f"{VARIABLE} posée : ce lot ne lit aucune donnée de campagne")


def _lire(chemin: str) -> bytes:
    if chemin.lower().endswith(".jsonl"):
        raise Refus("ENTREE/jsonl", f"{chemin} : aucun journal lu (E-S-02)")
    with open(chemin, "rb") as f:
        return f.read()


def _paires(paires: list) -> dict:
    d = {}
    for k, x in paires:
        if k in d:
            raise Refus("PARAMETRES/cle-double", k)
        d[k] = x
    return d


def _flottant(t: str):
    raise Refus("PARAMETRES/flottant", f"{t} : nombre non entier à écrire en chaîne (E-S-43)")


def charger_parametres(chemin: str = PARAMETRES, lus=None, environ=None) -> dict:
    """parametres.json : aucun flottant, aucune clé double, schéma fermé (E-S-03) ; empreinte des octets lus inscrite
    dans `lus` ({chemin relatif à la racine : sha256}) ; Refus nommé sinon."""
    garde_campagne(environ)
    octets = _lire(chemin)
    try:
        prm = json.loads(octets.decode("utf-8"), object_pairs_hook=_paires, parse_float=_flottant,
                         parse_constant=_flottant)
    except (ValueError, RecursionError) as e:
        raise Refus("PARAMETRES/json", str(e)[:200]) from None
    controler(prm, SCHEMA)
    if lus is not None:
        lus[os.path.relpath(chemin, RACINE).replace(os.sep, "/")] = hashlib.sha256(octets).hexdigest()
    return prm
