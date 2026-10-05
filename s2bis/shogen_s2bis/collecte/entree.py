"""Points d'entrée du collecteur (CB-18c, CB-18d ; E-C-02, E-C-16, E-C-23 ; ADR-0029 §2.9 l.238 ; PROPOSITION §2.1).
`configurer` charge et contrôle les configurations scellées (`formes.json` : paramètres de la boucle et formes de
requête ; `sante.json` : sondes) et le descripteur de l'observateur (refus nommés CONFIG/…, BOUCLE/…) ; `construire`
câble lectures, plan, sondes et boucle (SHOGEN-S2BIS-PLAN-CABLAGE-1). Commande `pool` (CB-18d) : ouvre le journal du
pool, y écrit `run_params` (commit, sha256 des octets de chaque fichier chargé, contenus, version de Python) à la
première fenêtre admise, puis fait tourner la boucle. Le journal est fermé à la sortie, quelle qu'elle soit ; une
OSError ou un refus de l'écrivain (JOURNAL/casse compris) arrête la boucle et le processus, que systemd relance
(SHOGEN-S2BIS-ECRIVAIN-USAGE-1). Sortie : 0 après les fenêtres demandées (`--fenetres`, essais), 1 arrêt sur le
journal, 2 refus avant l'ouverture du journal."""
import argparse
import ipaddress
import os
import re
import sys

from shogen_s2bis.collecte import boucle, config, dns, http, journal, sante
from shogen_s2bis.collecte.lecture import S, horloge

MAX = 3600 * S
FORME = {"nom": (str, 1, 64), "hote": (str, 1, 253), "port": (int, 1, 65535), "chemin": (str, 1, 2048),
         "methode": (str, 3, 4), "corps": (str, 0, 65536), "espace": (bool, None, None)}
SCHEMAS = {"formes": {"w": (int, 1, 3600), "delta": (int, 1, MAX), "delai": (int, 1, MAX), "marge": (int, 1, MAX),
                      "places": (int, 1, 4096), "formes": [FORME]},
           "sante": {"commande": [(str, 1, 4096)], "temoins": [(str, 7, 15)], "noms": [(str, 1, 253)],
                     "delai": (int, 1, MAX)},
           "descripteur": {"observateur": (str, 1, 16), "fournisseur": (str, 1, 64), "region": (str, 1, 64),
                           "asn": (int, 1, 4294967295), "resolveur": (str, 7, 15), "config_resolveur": (str, 1, 4096),
                           "versions": [(str, 1, 256)], "empreinte": (str, 64, 64)}}


def _ipv4(a):
    """Adresse IPv4 littérale canonique (forme rendue par `ipaddress`), comme l'exige le client DNS (§12)."""
    try:
        return str(ipaddress.IPv4Address(a)) == a
    except ValueError:
        return False


def _nom_dns(nom):
    try:
        return bool(dns.requete(0, nom, "A"))
    except ValueError:                                              # UnicodeError comprise
        return False


def _plan(f):
    """Plan de la boucle : décalages par hôte (`espace` : la limite de l'hôte impose l'espacement)."""
    return boucle.planifier([(x["nom"], x["hote"]) for x in f["formes"]],
                            {x["hote"] for x in f["formes"] if x["espace"]})


COHERENCE = {"formes": (("w-divise-l-heure", lambda f: 3600 % f["w"] == 0),
                        ("marge-delta-fenetre", lambda f: f["marge"] < f["delta"] <= f["w"] * S),
                        ("noms-uniques", lambda f: len({x["nom"] for x in f["formes"]}) == len(f["formes"])),
                        ("methode-corps", lambda f: all((x["methode"], x["corps"] == "") in (("GET", True), (
                            "POST", False)) for x in f["formes"])),
                        ("espace-par-hote", lambda f: len({(x["hote"], x["espace"]) for x in f["formes"]}) == len(
                            {x["hote"] for x in f["formes"]})),
                        ("budget", lambda f: _plan(f)[-1][0] + f["delai"] + f["marge"] <= f["delta"])),
             "sante": (("temoins-ipv4", lambda s: all(map(_ipv4, s["temoins"]))),
                       ("noms-dns", lambda s: all(map(_nom_dns, s["noms"])))),
             "descripteur": (("resolveur-ipv4", lambda d: _ipv4(d["resolveur"])),
                             ("empreinte-hex", lambda d: re.fullmatch("[0-9a-f]{64}", d["empreinte"]) is not None))}


def configurer(chemins, commit):
    """{nom : (données, sha256 des octets lus)} des trois fichiers de `chemins`, contrôlés, puis le commit (40
    chiffres hexadécimaux minuscules) et le délai des sondes (joint avant l'échéance) ; refus nommé au premier écart
    (RefusConfig, RefusBoucle) ; un fichier illisible lève OSError (E-C-02)."""
    lus = {n: config.charger(chemins[n], SCHEMAS[n], COHERENCE[n]) for n in SCHEMAS}
    if not re.fullmatch("[0-9a-f]{40}", commit):
        raise config.RefusConfig("CONFIG/commit", commit)
    if lus["sante"][0]["delai"] + lus["formes"][0]["marge"] > lus["formes"][0]["delta"]:
        raise config.RefusConfig("CONFIG/incoherent", "delai-sondes")
    return lus


def _lecteur(x, delai, tls):
    req = http.Requete(x["hote"], x["chemin"], x["port"], x["methode"], x["corps"].encode() or None)
    return lambda suivi: http.lire(req, suivi, delai=delai, tls=tls)


def construire(f, s, d, dossier, tls=http.CONTEXTE, fsync=os.fsync):
    """(écrivain non ouvert, boucle) câblés depuis les configurations : une lecture par forme, plan par hôte, sondes
    de `sante.json` vers le résolveur du descripteur, disque du dossier du journal (PLAN-CABLAGE-1)."""
    sondes = sante.Sondes(s["commande"], s["temoins"], s["noms"], d["resolveur"], dossier, d["config_resolveur"],
                          s["delai"])
    jl = journal.Journal(dossier, "pool", w=f["w"], fsync=fsync)
    return jl, boucle.Boucle(jl, {x["nom"]: _lecteur(x, f["delai"], tls) for x in f["formes"]}, _plan(f), f["places"],
                             w=f["w"], delta=f["delta"], marge=f["marge"], sondes=sondes)


def main(argv, tls=http.CONTEXTE, fsync=os.fsync):
    p = argparse.ArgumentParser(prog="python3 -m shogen_s2bis.collecte", description="collecteur de S2-bis")
    pool = p.add_subparsers(dest="commande", required=True).add_parser("pool", help="processus du pool")
    for option in ("--formes", "--sante", "--descripteur", "--journal", "--commit"):
        pool.add_argument(option, required=True)
    pool.add_argument("--fenetres", type=int, help="nombre de fenêtres, puis sortie 0 (essais) ; sans fin par défaut")
    a = p.parse_args(argv)
    try:
        lus = configurer({n: getattr(a, n) for n in SCHEMAS}, a.commit)
        f = lus["formes"][0]
        jl, b = construire(f, lus["sante"][0], lus["descripteur"][0], a.journal, tls, fsync)
    except (config.RefusConfig, boucle.RefusBoucle, OSError) as e:
        print(f"collecte : refus : {e}", file=sys.stderr)
        return 2
    try:
        jl.ouvrir(horloge() // (S * f["w"]) * f["w"])
        jl.ecrire("run_params", jl.suivante, commit=a.commit, sha256={n: lus[n][1] for n in lus}, python=sys.version,
                  **{n: lus[n][0] for n in lus})
        b.tourner(a.fenetres)
    except (OSError, journal.ErreurJournal) as e:
        print(f"collecte : arrêt : {getattr(e, 'code', type(e).__name__)} : {e}", file=sys.stderr)
        return 1
    finally:
        jl.fermer()
    return 0
