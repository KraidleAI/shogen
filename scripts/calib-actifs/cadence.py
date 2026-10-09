"""Relevé de cadence des agrégateurs (AVIS Q-CA-11 modifiée ; item SHOGEN-S2BIS-CADENCE-AGREG-1 ; ADR-0029 l.189) :
script séparé, hors de lancer.sh et hors du lancement du lot, lancé une fois avant le sceau et versé daté. N lectures
groupées de CoinGecko (last_updated_at) et de DefiLlama (timestamp), espacées de pas_s secondes ; les nombres à virgule
(les prix) sont jetés dès l'analyse JSON : seuls les horodatages entiers sont gardés ; aucun prix n'est gardé ni écrit.
Sortie : par (agrégateur, actif), intervalles entre horodatages distincts successifs (nombre, minimum, médiane, P90,
maximum, liste) et « plus lent que BTC » (médiane) ; une lecture en échec est comptée, jamais devinée.
Usage : python3 cadence.py --sortie <fichier> [--parametres <fichier>]"""
from __future__ import annotations

import json
import os
import sys

import acquerir
import socle

AGREGATEURS = ("coingecko", "defillama")


def horodatages(nom: str, corps: bytes, ids: dict) -> dict:
    """{actif : horodatage entier} d'une réponse groupée ; prix jetés (parse_float) ; champ absent : actif omis."""
    d = json.loads(corps.decode("utf-8"), parse_float=lambda _x: None)
    d = d["coins"] if nom == "defillama" else d
    cle = "timestamp" if nom == "defillama" else "last_updated_at"
    return {a: d[i][cle] for a, i in ids.items() if type(d.get(i, {}).get(cle)) is int}


def releve(prm: dict) -> tuple:
    """({(agrégateur, actif) : horodatages distincts, dans l'ordre}, lectures en échec)."""
    c, vus, echecs = prm["cadence"], {}, 0
    for k in range(c["lectures"]):
        for nom in AGREGATEURS:
            ids = c[nom]["ids"]
            try:
                url = c[nom]["url"].format(ids=",".join(ids.values()), options=c[nom]["options"])
                h = horodatages(nom, acquerir.lire_url(prm, url), ids)
            except (socle.Refus, ValueError, KeyError, AttributeError):
                echecs += 1
                continue
            for a, t in h.items():
                if vus.setdefault((nom, a), [])[-1:] != [t]:
                    vus[nom, a].append(t)
        if k + 1 < c["lectures"]:
            acquerir.DORMIR(c["pas_s"])
    return vus, echecs


def lignes(prm: dict, vus: dict, echecs: int) -> list:
    c, out = prm["cadence"], []
    out.append(f"relevé de cadence : {c['lectures']} lectures, pas de {c['pas_s']} s ; lectures en échec : {echecs}")
    med = {}
    for (nom, a), ts in sorted(vus.items()):
        iv = [y - x for x, y in zip(ts, ts[1:])]
        med[nom, a] = socle.quantile(iv, 50, 100)
        stats = [min(iv, default=None), med[nom, a], socle.quantile(iv, 90, 100), max(iv, default=None)]
        out.append(f"{nom} {a} : {len(iv)} intervalles ; minimum, médiane, P90, maximum (s) : "
                   + ", ".join("-" if x is None else str(x) for x in stats) + " ; " + " ".join(map(str, iv)))
    for (nom, a), m in sorted(med.items()):
        b = med.get((nom, "BTC"))
        if a != "BTC" and None not in (m, b):
            out.append(f"{nom} {a} plus lent que BTC (médiane) : {'oui' if m > b else 'non'}")
    return out


def main(argv=None, env=None) -> int:
    a = list(sys.argv[1:] if argv is None else argv)
    if len(a) not in (2, 4) or a[0] != "--sortie" or (len(a) == 4 and a[2] != "--parametres"):
        print("REFUS CA/usage : cadence.py --sortie <fichier> [--parametres <fichier>]", file=sys.stderr)
        return 2
    try:
        socle.garde(os.environ if env is None else env)
        prm = socle.lire(a[3] if len(a) == 4 else socle.PARAMETRES)
    except socle.Refus as r:
        print(r, file=sys.stderr)
        return 3
    socle.ecrire(os.path.dirname(os.path.abspath(a[1])), os.path.basename(a[1]), lignes(prm, *releve(prm)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
