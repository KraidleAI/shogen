"""Pauses entre épisodes, par hôte du pool D1-bis, strate et type (lot PLAN-S2BIS-2 ; G0
docs/adr-0029/g0-plan2/G0-PLAN-S2BIS-2.md ; PERIMETRE-REDUIT.md §2, P2R-3 ; AV l.39-40 ; E-P2-10, E-P2-11 (e)). Série
[(ws, classe)] aux positions réelles ; segments, épisodes et pauses par episodes.episodes (prédicat toujours vrai, le
type, son contraire) : pause complète sans drapeau de censure, pause de bord avec un drapeau au moins, segment sans
épisode avec deux ; résumés par episodes.resume (quantiles par regles.quantile) ; contrôle (e) : lignes d'épisodes
régénérées (forme de PS2 episodes.py l.106-112) = EP l.13-92, sinon P2/ep. Aucune formule d'épisode, de pause, de
quantile ni d'histogramme ici. Aucune barre oblique inverse."""
from __future__ import annotations

import sys

import socle

OBJET = "pauses entre épisodes et épisodes complets, par hôte du pool D1-bis, strate et type"
SORTIES = ("intervalles.txt",)


def serie(fen: list, f: str) -> list:
    """[(ws, classe du flux f)] aux fenêtres retenues de la strate, positions réelles, jamais renumérotées."""
    return [(ws, cls[f]) for ws, cls, _r in fen]


def entree(s: list, w: int, pred, episodes) -> dict:
    """Segments, épisodes, pauses complètes, pauses de bord et segments sans épisode de la série s."""
    pauses = episodes.episodes(s, w, lambda x: not pred(x))
    return {"segments": episodes.episodes(s, w, lambda x: True), "episodes": episodes.episodes(s, w, pred),
            "completes": [p for p in pauses if not (p[1] or p[2])], "bord": [p for p in pauses if p[1] or p[2]],
            "vides": [p for p in pauses if p[1] and p[2]]}


def histogramme(r: dict, vide: str) -> str:
    return " ".join(f"{k}×{v}" for k, v in r["histogramme"]) or vide


def lignes(etiquette: str, e: dict, n_s: int, qs: list, resume, dec) -> list:
    """Entrée de intervalles.txt (PROPOSITION.md §2.4), compte des pauses complètes en premier (AV l.39)."""
    rc, rb, re = (resume(x, n_s, qs) for x in (e["completes"], e["bord"], e["episodes"]))
    rx = resume([x for x in e["episodes"] if not (x[1] or x[2])], n_s, qs)
    return [f"  {etiquette} : pauses complètes = {rc['episodes']} ; segments = {len(e['segments'])} ; épisodes = "
            f"{re['episodes']} (complets {re['complets']}) ; moyenne = {dec(rc['moyenne'])} ; max = {dec(rc['max'])} ; "
            + " ; ".join(f"P{a} = {dec(v)}" for (a, _b), v in zip(qs, rc["q"]))
            + f" ; pauses de bord = {rb['episodes']} (dont segments sans épisode {len(e['vides'])})",
            "    histogramme des pauses (longueur×nombre) : " + histogramme(rc, "aucune pause"),
            "    histogramme des pauses de bord (longueur observée×nombre) : "
            + histogramme(rb, "aucune pause de bord"),
            "    histogramme des épisodes complets (longueur×nombre) : " + histogramme(rx, "aucun épisode complet")]


def lignes_ep(etiquette: str, r: dict, n_s: int, qs: list, dec) -> list:
    """Lignes d'épisodes d'EP (forme de PS2 episodes.py l.106-112), régénérées pour le contrôle (e)."""
    return [f"  {etiquette} : n_s = {n_s} ; cellules = {r['cellules']} ; épisodes = {r['episodes']}, dont censurés "
            f"{r['censures']} ; taux = {dec(r['taux'])} ; moyenne = {dec(r['moyenne'])} ; max = {dec(r['max'])} ; "
            + " ; ".join(f"P{a} = {dec(v)}" for (a, _b), v in zip(qs, r["q"])) + f" ; complets : {r['complets']}, "
            f"moyenne {dec(r['moyenne_complets'])}",
            "    histogramme (longueur×nombre) : " + histogramme(r, "aucun épisode")]


def analyse(d: dict, ps2: dict, prm: dict, ep: list) -> dict:
    commun, episodes = sys.modules["commun"], sys.modules["episodes"]
    r1, dec, qs, w = commun.H["r1"], commun.dec, ps2["episodes"]["quantiles"], d["w"]
    types = {nom: {r1.Ecart(v) for v in vals} for nom, vals in ps2["episodes"]["types"].items()}
    par, k = commun.classer(d, d["pools_bis"]), 0
    publie = [x for x in ep if x.startswith(("  « ", "    histogramme (longueur×nombre) : "))]
    out = ["[PAUSES] par hôte du pool D1-bis, strate et type ; segment, épisode, censure : définitions d'EP ; pause "
           "entre deux épisodes d'un même segment ; pause de bord censurée, comptée à part",
           "  contrôle : épisodes recomptés = EP l.13-92 (n_s, cellules, épisodes, censurés, complets, max, "
           + ", ".join(f"P{a}" for a, _b in qs) + ", histogramme) : égaux"]
    for st in ps2["strates"]:
        for h, f in ps2["pool_d1bis"]["unites"].items():
            for nom, ens in types.items():
                s, etiquette = serie(par[st], f), f"« {st} » {f} (hôte {h}) {nom}"
                e = entree(s, w, ens.__contains__, episodes)
                if publie[k:k + 2] != lignes_ep(etiquette, episodes.resume(e["episodes"], len(s), qs), len(s), qs, dec):
                    raise socle.Refus("P2/ep", f"contrôle (e) : épisodes de type « {nom} » différents d'EP", st, h)
                out, k = out + lignes(etiquette, e, len(s), qs, episodes.resume, dec), k + 2
    if k != len(publie):
        raise socle.Refus("P2/ep", "contrôle (e) : nombre de lignes d'épisodes différent d'EP")
    return {"intervalles.txt": out}


def main(argv=None) -> int:
    return socle.executer("intervalles", OBJET, SORTIES, analyse, argv)


if __name__ == "__main__":
    raise SystemExit(main())
