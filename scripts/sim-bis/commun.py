"""Socle du lot SIM-BIS (G0 docs/adr-0029/g0-sim/G0-SIM-BIS.md : PROPOSITION corrigée par AVIS ; sous-lot SB-0 ;
E-S-02, E-S-03, E-S-05, E-S-06, E-S-43, E-S-48) : parametres.json sous schéma fermé, entrées lues par chemin sous deux
épingles, garde de la variable de campagne, écriture atomique sans écrasement, en-tête et étiquette, JSON canonique.
Bibliothèque standard seule ; aucune barre oblique inverse dans ce fichier (saut de ligne : chr(10))."""
import hashlib
import json
import os
import posixpath
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(os.path.dirname(ICI))
PARAMETRES = os.path.join(ICI, "parametres.json")
VARIABLE = "SHOGEN_S2_CAMPAGNE_CONTROL"
ETIQUETTE = ("synthétique ; préparation de S2-bis ; ne lit aucune donnée de S2-bis ni aucun journal de S2 ; ne change "
             "ni R, ni le seuil, ni la règle")
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


def positif(v) -> bool:
    return type(v) is int and v > 0


def jour(v) -> bool:
    return type(v) is int and 0 <= v <= 6


ENTREE = {"chemin": texte, "sha256": hex64}
SCHEMA = {"lot": texte, "schema": texte, "rattachement": texte,
          "entrees": {"sommes": ENTREE, "episodes": ENTREE, "source": texte},
          "aleas": {"prefixe": texte, "graine": positif, "rangs": positif, "garde": positif, "source": texte},
          "calibration": {"strates": [texte], "unites": [(texte, texte)], "types": [texte], "quantiles": [positif],
                          "pools": [texte], "ell": [positif], "garde_blocs": positif, "precision": positif,
                          "source": texte},
          "calendrier": {"w": positif, "jours_stress": [jour], "lundi_reference": positif,
                         "echelle_semaines": [positif], "n_par_semaine": {"calme": positif, "stress": positif},
                         "t_max": (positif, positif), "source": texte},
          "sources": {"composants": [texte], "indices_hotes": [texte], "regroupees": [texte], "longues": [positif],
                      "derive": {"bornes": ((positif, positif), (positif, positif)), "unites_saut": positif,
                                 "transitoire": (positif, positif), "initiale": positif},
                      "classes": {"BTC": [texte], "ETH": [texte], "USDC": [texte], "USDT": [texte]}, "as13335": [texte],
                      "source": texte}}


def controler(v, s, ou: str = "parametres") -> None:
    """`v` contre le schéma `s` : dict = clés exactes ; [s0] = liste non vide d'éléments conformes à s0 ; (s1, …) =
    liste d'autant d'éléments, un schéma chacun ; contrôle récursif ; sinon prédicat. Refus PARAMETRES/schema."""
    if isinstance(s, dict):
        if type(v) is not dict or sorted(v) != sorted(s):
            raise Refus("PARAMETRES/schema", f"{ou} : {sorted(v) if type(v) is dict else type(v).__name__}, "
                                             f"attendu {sorted(s)}")
        for k in sorted(s):
            controler(v[k], s[k], f"{ou}.{k}")
    elif isinstance(s, (list, tuple)):
        if type(v) is not list or not v or (type(s) is tuple and len(v) != len(s)):
            raise Refus("PARAMETRES/schema", f"{ou} : liste non vide attendue"
                                             + (f" de {len(s)} éléments" if type(s) is tuple else ""))
        for j, x in enumerate(v):
            controler(x, s[j] if type(s) is tuple else s[0], f"{ou}[{j}]")
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


def lire_entree(prm: dict, nom: str, lus=None, environ=None, racine: str = RACINE) -> bytes:
    """Octets de l'entrée `nom` (chemin relatif à la racine) : sha256 égal à son épingle de parametres.json, puis,
    sauf pour « sommes », égal à sa ligne « <sha256>  <chemin relatif au dossier des sommes> » du fichier de sommes,
    lui-même lu sous son épingle (E-S-02). Inscrit chaque fichier lu dans `lus`."""
    garde_campagne(environ)
    e = prm["entrees"][nom]
    octets = _lire(os.path.join(racine, e["chemin"]))
    sha = hashlib.sha256(octets).hexdigest()
    if sha != e["sha256"]:
        raise Refus("ENTREE/sha256-parametres", f"{e['chemin']} : {sha}, épingle {e['sha256']}")
    if nom != "sommes":
        s = prm["entrees"]["sommes"]["chemin"]
        ligne = f"{sha}  {posixpath.relpath(e['chemin'], posixpath.dirname(s))}"
        if ligne not in lire_entree(prm, "sommes", lus, environ, racine).decode("utf-8").split(NL):
            raise Refus("ENTREE/sha256-sommes", f"{e['chemin']} : « {ligne} » absente de {s}")
    if lus is not None:
        lus[e["chemin"]] = sha
    return octets


def ecrire(chemin: str, octets: bytes) -> None:
    """Fichier écrit en entier ou pas du tout, jamais par-dessus un fichier existant (E-S-48) : partiel voisin
    « .partiel » créé en exclusif, fsync, lien dur vers `chemin` (refusé si `chemin` existe), partiel retiré ;
    `.jsonl` refusé (E-S-06)."""
    if chemin.lower().endswith(".jsonl"):
        raise Refus("SORTIE/jsonl", chemin)
    partiel = chemin + ".partiel"
    try:
        fd = os.open(partiel, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    except FileExistsError:
        raise Refus("SORTIE/partiel-present", partiel) from None
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(octets)
            f.flush()
            os.fsync(f.fileno())
        try:
            os.link(partiel, chemin)
        except FileExistsError:
            raise Refus("SORTIE/existe", chemin) from None
    finally:
        os.unlink(partiel)


def _sans_flottant(x) -> None:
    if type(x) is float:
        raise Refus("SORTIE/flottant", f"{x!r} (E-S-43)")
    for y in [*x, *x.values()] if type(x) is dict else x if type(x) in (list, tuple) else ():
        _sans_flottant(y)


def json_canonique(obj) -> bytes:
    """UTF-8 du JSON à clés triées, séparateurs fixes, sans échappement, saut de ligne final ; aucun flottant, ni en
    valeur ni en clé (O-2 de la G2) ; aucune heure, aucun hôte, aucune version (E-S-43)."""
    _sans_flottant(obj)
    try:
        t = json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"), allow_nan=False)
    except TypeError as e:
        raise Refus("SORTIE/type", str(e)) from None
    return (t + NL).encode("utf-8")


def entete(lus: dict) -> list:
    """L'étiquette (première ligne de toute sortie, E-S-05), puis « sha256 <chemin> <empreinte> », triées par chemin,
    des modules du lot chargés (empreinte des octets sur disque) et des fichiers lus `lus` (E-S-03)."""
    mods = {}
    for m in list(sys.modules.values()):
        f = getattr(m, "__file__", None)
        if f and os.path.dirname(os.path.realpath(f)) == os.path.realpath(ICI):
            with open(f, "rb") as g:
                mods[os.path.relpath(f, RACINE).replace(os.sep, "/")] = hashlib.sha256(g.read()).hexdigest()
    return [ETIQUETTE] + [f"sha256 {k} {v}" for k, v in sorted({**mods, **lus}.items())]
