"""Masque des fenêtres évaluables du segment J28 et FIV_u par hôte, un seul script (lot PLAN-S2BIS-2 ; G0
docs/adr-0029/g0-plan2/G0-PLAN-S2BIS-2.md ; PERIMETRE-REDUIT.md §2, P2R-1 et P2R-2 ; AV l.150 ; E-P2-08, E-P2-11 (b)).
masque_j28.txt : positions de la portée de commun.charger, strate par window.strate_from_spec (calendrier journalisé),
retenue = fenêtre de d["ws"] ; chaîne c/s/-, comptes, lacunes (D5 comprise) ; contrôle (b), sinon P2/masque. Aucune
formule de FIV, d'épisode ni de quantile ici. Aucune barre oblique inverse."""
from __future__ import annotations

import hashlib
import itertools
import sys
from collections import Counter

import socle

OBJET = "masque des fenêtres évaluables de J28 et FIV_u par hôte"
SORTIES = ("masque_j28.txt",)


def portee(bornes: tuple, w: int, plages: list, spec: dict, window) -> list:
    """[(ws, strate du calendrier, dans une plage exclue)] des positions de [t0 ; t_fin), pas w ; plages fermées."""
    return [(ws, window.strate_from_spec(ws, spec), any(a <= ws <= b for a, b in plages))
            for ws in range(bornes[0], bornes[1], w)]


def masque(pos: list, retenues: dict) -> dict:
    """Chaîne (initiale de la strate du calendrier si retenue, « - » sinon), comptes par strate du calendrier hors
    plages exclues et des retenues, lacunes [(j début, j fin, {strate : positions})], plages exclues comprises."""
    chaine = "".join(st[0] if ws in retenues else "-" for ws, st, _x in pos)
    lacunes = []
    for vide, g in itertools.groupby(range(len(pos)), key=lambda j: chaine[j] == "-"):
        if vide:
            js = list(g)
            lacunes.append((js[0], js[-1], Counter(pos[j][1] for j in js)))
    return {"chaine": chaine, "calendrier": Counter(st for _ws, st, x in pos if not x), "lacunes": lacunes,
            "retenues": Counter(st for ws, st, _x in pos if ws in retenues)}


def controle_b(pos: list, m: dict, retenues: dict, strates: list, bloc3: dict, attendu: dict) -> None:
    """(b) : chaque fenêtre retenue est une position de la grille, hors des plages exclues, de strate journalisée égale
    à celle du calendrier ; par strate, calendrier hors D5 et sautées = parametres.json du lot (ADR-0029 l.31),
    retenues = n du bloc 3 épinglé ; sinon P2/masque."""
    grille = {ws: (st, x) for ws, st, x in pos}
    if any(grille.get(ws) != (st, False) for ws, st in retenues.items()):
        raise socle.Refus("P2/masque", "fenêtre retenue hors de la grille, dans une plage exclue ou hors calendrier")
    if {s for c in attendu.values() if isinstance(c, dict) for s in c} != set(strates):
        raise socle.Refus("P2/masque", "strates des comptes attendus différentes de celles de PLAN-S2BIS")
    for s in strates:
        cal, ret = m["calendrier"][s], m["retenues"][s]
        if (cal, cal - ret, ret) != (attendu["calendrier_hors_d5"][s], attendu["sautees_hors_d5"][s], bloc3[s][0]):
            raise socle.Refus("P2/masque", "calendrier hors D5, sautées ou retenues différents de l'attendu", s)


def lignes_masque(bornes: tuple, pos: list, m: dict, strates: list, plages: list) -> list:
    """Section [MASQUE J28], forme de PROPOSITION.md §2.2 (E-P2-08)."""
    d5 = " ; ".join(f"j = {js[0]} à {js[-1]} ({len(js)} positions)" if js else "aucune position" for js in
                    ([j for j, (ws, _st, _x) in enumerate(pos) if a <= ws <= b] for a, b in plages)) or "aucune"
    empreinte = hashlib.sha256(m["chaine"].encode("ascii")).hexdigest()
    out = ["[MASQUE J28] positions j = (ws − t0)/w de la portée ; strate par jour UTC ; retenue = fenêtre retenue de "
           "la strate", f"  portée : t0 = {bornes[0]} ; t_fin = {bornes[1]} ; positions = {len(pos)} ; plage D5 : {d5}"]
    out += [f"  « {s} » : calendrier hors D5 = {m['calendrier'][s]} ; retenues = {m['retenues'][s]} ; sautées hors "
            f"D5 = {m['calendrier'][s] - m['retenues'][s]}" for s in strates]
    out += ["  contrôle : retenues = n du bloc 3 ; sautées = ADR-0029 l.31 ; strate de chaque retenue = calendrier : "
            "égaux", f"  empreinte : sha256 de la chaîne de {len(pos)} caractères (c calme retenue, s stress "
            f"retenue, - non retenue) = {empreinte}", f"  lacunes : {len(m['lacunes'])} suites maximales de positions "
            "non retenues, plage D5 comprise, en ordre croissant"]
    return out + [f"  lacune j = {a} à {b} : {b - a + 1} positions (" + ", ".join(f"{s} {c[s]}" for s in strates)
                  + ")" for a, b, c in m["lacunes"]]


def analyse(d: dict, ps2: dict, prm: dict, ep: list) -> dict:
    window = sys.modules["commun"].H["window"]
    pos = portee(d["bornes"], d["w"], d["plages"], d["params"]["strate_calendar"], window)
    m = masque(pos, d["ws"])
    controle_b(pos, m, d["ws"], ps2["strates"], ps2["rendu_j28"]["bloc3"], prm["masque"])
    return {"masque_j28.txt": lignes_masque(d["bornes"], pos, m, ps2["strates"], d["plages"])}


def main(argv=None) -> int:
    return socle.executer("masque_fiv", OBJET, SORTIES, analyse, argv)


if __name__ == "__main__":
    raise SystemExit(main())
