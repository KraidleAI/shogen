"""SHOGEN-HOST-DEGRADED-2 (ADR-0028 annexe B.6 l.100) et SHOGEN-HORLOGE-ETENDUE-1 (annexe B.46 l.684 ; paquet §12
pt 17), J28, plage exclue, hors décision.

HOST-DEGRADED-2 : critère sur les seuls enregistrements de diagnostic du harnais, jamais sur un statut de source.
Démarrage : groupe ouvert par un run_params (ou par un clock_check « startup » qui n'en suit pas un), auquel se
rattachent les relevés asn_attribution écrits depuis le dernier marqueur du démarrage précédent (la sonde ASN de chaque
chunk précède son run_params, run_campaign.run_segment). Démarrage dégradé : au moins un asn_attribution
resolve_failed.
Fenêtre retirée : le démarrage de son dernier marqueur (last-wins) est dégradé. Le clock_check n'entre pas au critère :
ses signaux (« non évaluable », offset médian) dépendent des sources du pool qui ont répondu à la sonde ; ses comptes sont
imprimés. Recalcul : D1 (r1.analysis_pools) sur les fenêtres restantes, r1.compute_r1, r1.regle_critere.
HORLOGE-ETENDUE-1 : median_offset des clock_check retenus par le filtre de lecture (Decimal du texte JSON) : nombre, non
évaluables, minimum, médiane, maximum, étendue (max − min). Aucun seuil."""
from __future__ import annotations

import sys
from collections import Counter
from decimal import Decimal, localcontext

import commun
from commun import dec, r1, records


def demarrages(control: str) -> tuple:
    """([{"asn", "clock", "ws"}] dans l'ordre du journal, sonde ASN finale non rattachée, marqueurs hors démarrage)."""
    groupes, attente, hors = [], [], 0
    for o in records.read_jsonl_tolerant(control):
        t = o.get("record")
        if t == "asn_attribution":
            attente.append(o)
        elif t == "run_params" or t == "clock_check" and o.get("phase") == "startup" and not (
                groupes and groupes[-1]["rp"] and not groupes[-1]["clock"] and not groupes[-1]["ws"]):
            groupes.append({"asn": attente, "clock": [o] if t == "clock_check" else [], "ws": [],
                            "rp": t == "run_params"})
            attente = []
        elif t == "clock_check":
            groupes[-1]["clock"].append(o)
        elif t == "window_close":
            hors += not groupes
            if groupes:
                groupes[-1]["ws"].append(int(o["window_start"]))
    return groupes, attente, hors


def degrade(g: dict) -> bool:
    return any(a.get("status") == "resolve_failed" for a in g["asn"])


def retirees(groupes: list) -> set:
    """window_start dont le dernier marqueur appartient à un démarrage dégradé."""
    dernier = {ws: i for i, g in enumerate(groupes) for ws in g["ws"]}
    return {ws for ws, i in dernier.items() if degrade(groupes[i])}


def entrelaces(groupes: list, retenues) -> tuple:
    """Démarrages ouverts par un clock_check qui suit un run_params sans clock_check, marqueurs entre les deux (constat
    de l'exécution, journal G1 §3), et fenêtres de `retenues` dont le dernier marqueur y tombe."""
    ids = {i for i, g in enumerate(groupes) if not g["rp"] and i and groupes[i - 1]["rp"] and not groupes[i - 1]["clock"]}
    dernier = {ws: i for i, g in enumerate(groupes) for ws in g["ws"]}
    return len(ids), sum(dernier.get(ws) in ids for ws in retenues)


def hote_degrade(d: dict) -> dict:
    groupes, attente, hors = demarrages(d["control"])
    out = retirees(groupes)
    m = [x for x in d["markers"] if int(x["window_start"]) not in out]
    pools, _seg, retraits = r1.analysis_pools(m, d["readings"], list(d["params"]["pool"]))
    r = commun.calculer(d, m, pools)
    v = r1.regle_critere(r)
    n0 = Counter(x["strate"] for x in {int(y["window_start"]): y for y in d["markers"]}.values())
    nd, nonev = sum(map(degrade, groupes)), [any(c.get("median_offset") is None for c in g["clock"]) for g in groupes]
    echecs = sum(a.get("status") == "resolve_failed" for g in groupes for a in g["asn"])
    lignes = ["[SHOGEN-HOST-DEGRADED-2] fenêtres retirées : dernier marqueur dans un démarrage dont la sonde ASN porte "
              "au moins un resolve_failed ; clock_check hors critère (dépend des sources qui répondent à la sonde)",
              f"démarrages : {len(groupes)} (ouverts par run_params : {sum(g['rp'] for g in groupes)}) ; dégradés : "
              f"{nd} ; relevés asn_attribution rattachés : {sum(len(g['asn']) for g in groupes)}, dont resolve_failed "
              f"{echecs} ; sonde finale non rattachée : {len(attente)} ; marqueurs hors démarrage : {hors}",
              f"démarrages à clock_check non évaluable : {sum(nonev)}, dont dégradés : "
              f"{sum(x and degrade(g) for x, g in zip(nonev, groupes))}",
              *(f"« {s} » : fenêtres retenues par la règle scellée {n0[s]} ; retirées "
                f"{n0[s] - r['strates'].get(s, {}).get('n', 0)} ; pool D1 restant {len(pools.get(s, []))} flux"
                for s in sorted(n0)),
              "démarrages ouverts par un clock_check après un run_params sans clock_check, marqueurs entre les deux ; "
              "fenêtres retenues dont le dernier marqueur y tombe (constat de l'exécution) : "
              + " ; ".join(map(str, entrelaces(groupes, {int(y["window_start"]) for y in d["markers"]}))),
              f"retraits D1 sur les fenêtres restantes : {[(s, f) for s, f, *_ in retraits] or 'aucun'}"]
    for s, b in r["strates"].items():
        e = v["strates"][s]
        lignes.append(f"règle recalculée « {s} » : n = {b['n']} ; K = {b['K']} ; P̂_more = {dec(b['P_more'])} ; "
                      f"garde = {dec(b['gate_value'])} ; z_s = {dec(b['z'])} ; σ̂²_bloc = "
                      f"{dec(b['bloc']['sigma2_bloc'])} ; z_bloc = {dec(b['bloc']['z_bloc'])} ; valeur = "
                      f"{e['valeur']} ({e['cas']}) ; EMD_s = {dec(e['emd'])}")
    lignes.append("« R1 discrimine » recalculé sous cette sensibilité (hors décision ; ne change pas le verdict) = "
                  f"{v['r1_discrimine']}")
    return {"r1": r, "regle": v, "retirees": out, "lignes": lignes}


def horloge(d: dict) -> dict:
    vals = [Decimal(repr(c["median_offset"])) for c in d["clock"] if c.get("median_offset") is not None]
    with localcontext(r1.contexte_decimal()):
        h = {"n": len(d["clock"]), "non_evaluables": len(d["clock"]) - len(vals), "min": min(vals, default=None),
             "max": max(vals, default=None), "mediane": r1._median(vals) if vals else None}
        h["etendue"] = None if not vals else +(h["max"] - h["min"])
    h["lignes"] = ["[SHOGEN-HORLOGE-ETENDUE-1] offset médian (harness_ts − source_ts, médiane par relevé) des "
                   "clock_check retenus par le filtre de lecture (segment, plage D5 sur harness_ts) ; descriptif, sans "
                   "seuil",
                   f"relevés retenus : {h['n']} (phases : {dict(Counter(c.get('phase') for c in d['clock']))}) ; non "
                   f"évaluables (médiane nulle) : {h['non_evaluables']}",
                   f"minimum = {dec(h['min'])} s ; médiane = {dec(h['mediane'])} s ; maximum = {dec(h['max'])} s ; "
                   f"étendue = {dec(h['etendue'])} s"]
    return h


ANALYSES = {"hote": ("SHOGEN-HOST-DEGRADED-2", lambda d: hote_degrade(d)["lignes"]),
            "horloge": ("SHOGEN-HORLOGE-ETENDUE-1", lambda d: horloge(d)["lignes"])}


def main(argv: list) -> int:
    """hote_horloge.py {hote | horloge} --journaux D --sortie F (options de commun.executer)."""
    quoi, *reste = argv
    items, analyse = ANALYSES[quoi]
    return commun.executer(f"hote_horloge.py {quoi}", items, analyse, reste)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
