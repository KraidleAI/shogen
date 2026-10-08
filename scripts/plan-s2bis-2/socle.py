"""Socle du lot PLAN-S2BIS-2 (G0 docs/adr-0029/g0-plan2/G0-PLAN-S2BIS-2.md ; PERIMETRE-REDUIT.md §1, §2, §9 ; E-P2-03 à
E-P2-05, E-P2-11 (c) et (d), E-P2-12). Refus nommés ; garde de la variable de campagne sur un environnement passé en
argument ; schéma du parametres.json du lot ; huit pièces de PLAN-S2BIS contrôlées contre leurs épingles, puis commun,
regles et episodes chargés par chemin, sous ces noms et dans cet ordre (P-1) ; sous-arbres déclarés (P-3) seuls lus du
parametres.json de PLAN-S2BIS ; contrôles (c) pool D1-bis et (d) type « ecart ». Aucune barre oblique inverse : saut
de ligne par chr(10)."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(os.path.dirname(ICI))
PARAMETRES = os.path.join(ICI, "parametres.json")
NL = chr(10)
ETIQUETTE = "préparation de S2-bis ; ne change pas le verdict de S2 (« R1 discrimine » = FAUX)"
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


def provenance(d: dict, ps2: dict, commun) -> list:
    """Lignes de provenance de l'en-tête, forme de PS2 commun.py l.184-194 : harnais, journaux (sha256 seuls), portée,
    pool S2 (D1), pool D1-bis."""
    seg = ps2["segment"]
    return [f"harnais : extraction du commit d'analyse {ps2['commit_analyse']} ; modules épinglés : "
            + " ; ".join(f"{os.path.basename(k)} {v}" for k, v in ps2["harnais_sha256"].items()),
            f"journaux : control.jsonl sha256 {commun.sha256(d['control'])} ; journal.jsonl sha256 "
            f"{commun.sha256(d['journal'])}",
            f"portée : segment [{d['bornes'][0]} ; {d['bornes'][1]}) (t0 = {seg['t0']}, n fixe = {seg['n_fixe']}), "
            f"plages exclues {d['plages']}",
            "pool S2 (D1) : " + " ; ".join(f"« {s} » {len(v)} flux" for s, v in d["pools_s2"].items())
            + " ; retraits : " + (" ; ".join(f"« {s} » {f} (ok {k} sur {t} lectures)"
                                             for s, f, k, t, _n in d["retraits_s2"]) or "aucun"),
            ligne_pool_bis(d)]


def executer(nom: str, objet: str, sorties: tuple, analyse, argv=None, env=None) -> int:
    """CLI des scripts du lot (P2R-1 ; P-2) : --journaux, --harnais, --sortie (dossier), --parametres (du lot), --rendu.
    Variable ; schéma ; pièces de PLAN-S2BIS ; harnais par commun.importer_harnais (P2/harnais) ; (d) ; lecture par
    commun.charger ; (a) par commun.controle (P2/coherence) ; (c) ; puis analyse(d, ps2, prm, ep), qui rend {sortie :
    lignes}. Chaque sortie : étiquette, en-tête, corps (code 0) ou une ligne de refus (code 1) ; écrite en .partiel,
    puis renommée."""
    a = argparse.ArgumentParser(prog=nom)
    for o in ("--journaux", "--harnais", "--sortie"):
        a.add_argument(o, required=True)
    a.add_argument("--parametres", default=PARAMETRES)
    a.add_argument("--rendu")
    x = a.parse_args(argv)
    tete = [f"{nom} — {objet} (PLAN-S2BIS-2 ; SHOGEN-SIM-BIS-FIV-IDENTIF-1)"]
    try:
        garde(os.environ if env is None else env)
        prm = lire(x.parametres)
        chemins, mods, ps2, ep = charger(prm)
        commun, lus = mods["commun"], prm["sous_arbres"]
        fichiers = [os.path.abspath(__file__), sys.modules[analyse.__module__].__file__, *(chemins[n] for n in MODULES)]
        tete += ["modules chargés : " + " ; ".join(f"{os.path.basename(q)} sha256 {empreinte(q)}" for q in fichiers),
                 f"parametres.json du lot sha256 {empreinte(x.parametres)} ; parametres.json de PLAN-S2BIS sha256 "
                 f"{empreinte(chemins['parametres'])} ; EP {os.path.basename(chemins['ep'])} sha256 "
                 f"{empreinte(chemins['ep'])}",
                 f"sous-arbres lus dans {prm['plan_s2bis']['chemins']['parametres']} : " + ", ".join(lus["lus"])
                 + " ; épingles : " + ", ".join(lus["epingles"])]
        try:
            commun.importer_harnais(x.harnais, ps2["harnais_sha256"])
        except ValueError:
            raise Refus("P2/harnais", "module du harnais hors des épingles ou de sha256 différent") from None
        controle_d(ps2, commun.H["r1"])
        d = commun.charger(x.journaux, ps2)
        ok, ctrl = commun.controle(d, ps2, x.rendu or os.path.join(commun.RACINE, ps2["rendu_j28"]["chemin"]))
        tete += provenance(d, ps2, commun) + ctrl
        if not ok:
            raise Refus("P2/coherence", "bloc 3 recompté différent de l'épingle (contrôle (a))")
        controle_c(d, ps2, ep)
        corps, code = analyse(d, ps2, prm, ep), 0
    except Refus as r:
        corps, code = {s: [str(r)] for s in sorties}, 1
    os.makedirs(x.sortie, exist_ok=True)
    for s in sorties:
        cible = os.path.join(x.sortie, s)
        with open(cible + ".partiel", "w", encoding="utf-8", newline=NL) as f:
            f.write(NL.join([ETIQUETTE, *tete, *corps[s]]) + NL)
        os.replace(cible + ".partiel", cible)
    return code
