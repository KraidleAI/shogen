"""Masque des fenêtres évaluables du segment J28 et FIV_u par hôte, un seul script (lot PLAN-S2BIS-2 ; G0
docs/adr-0029/g0-plan2/G0-PLAN-S2BIS-2.md ; PERIMETRE-REDUIT.md §2, P2R-1 et P2R-2 ; AV l.150 ; E-P2-08, E-P2-11 (b)).
masque_j28.txt : positions de la portée de commun.charger, strate par window.strate_from_spec (calendrier journalisé),
retenue = fenêtre de d["ws"] ; chaîne c/s/-, comptes, lacunes (D5 comprise) ; contrôle (b), sinon P2/masque.
fiv_unites.txt : séries d'écart D_u, contrôle (f), FIV_u par episodes.courbe (E-P2-09, E-P2-11 (f)) ; sensibilité au
voisinage des lacunes (E-P2-13, P-4). Aucune formule de FIV, d'épisode ni de quantile ici. Aucune barre oblique
inverse."""
from __future__ import annotations

import hashlib
import itertools
import sys
from collections import Counter

import socle

OBJET = "masque des fenêtres évaluables de J28 et FIV_u par hôte"
SORTIES = ("masque_j28.txt", "fiv_unites.txt")


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
    à celle du calendrier ; chacun des deux comptes attendus porte exactement les strates de PLAN-S2BIS ; par strate,
    calendrier hors D5 et sautées = parametres.json du lot (ADR-0029 l.31), retenues = n du bloc 3 épinglé ; sinon
    P2/masque."""
    grille = {ws: (st, x) for ws, st, x in pos}
    if any(grille.get(ws) != (st, False) for ws, st in retenues.items()):
        raise socle.Refus("P2/masque", "fenêtre retenue hors de la grille, dans une plage exclue ou hors calendrier")
    if any(set(attendu[k]) != set(strates) for k in ("calendrier_hors_d5", "sautees_hors_d5")):
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


def reduite(serie: list, w: int, d: int) -> list:
    """Sensibilité au voisinage (P-4) : série privée des positions dont une voisine à distance ≤ d (pas w) n'est pas une
    position de la série (lacune de la strate, bords de la portée compris) ; positions réelles."""
    r = {ws for ws, _x in serie}
    return [(ws, x) for ws, x in serie if all(ws + k * w in r for k in range(-d, d + 1))]


def cellules(serie: list) -> int:
    return sum(x for _ws, x in serie)


def ligne_courbe(prefixe: str, c: dict, dec) -> str:
    """Ligne de courbe, forme d'EP l.94 (PS2 episodes.py l.118-120) après le préfixe (P-6)."""
    return (f"  {prefixe} ℓ = {c['ell']} : n = {c['n']} ; K = {c['K']} ; FIV_série = {dec(c['FIV_serie'])} ; "
            f"σ̂²_bloc = {dec(c['sigma2_bloc'])} ; γ̂₀ = {dec(c['gamma0'])} ; cv théorique = {dec(c['cv'])} ; garde : "
            f"{'tenue' if c['garde'] else 'non tenue'}")


def fiv(d: dict, ps2: dict, prm: dict, ep: list) -> list:
    """D_u = 1{cellule (ws, u) dans r1.ECARTS}, classement de commun.classer sur le pool D1-bis (l'appel d'EP), aux
    fenêtres retenues de la strate, positions réelles ; contrôle (f) : (i) n et K de chaque D_u = n_s et cellules
    « ecart » d'EP (P-5) ; (ii) courbe de I_t = 1{Σ_u D_u ≥ 2} = lignes « D1-bis » d'EP ; sinon P2/ep. Puis FIV_u par
    episodes.courbe aux ℓ de fiv.ell, et la sensibilité au voisinage (d du parametres.json du lot)."""
    commun, courbe = sys.modules["commun"], sys.modules["episodes"].courbe
    r1, dec, w, ells, strates = commun.H["r1"], commun.dec, d["w"], ps2["fiv"]["ell"], ps2["strates"]
    par, unites = commun.classer(d, d["pools_bis"]), list(ps2["pool_d1bis"]["unites"].items())
    D = {(st, h, f): [(ws, int(cls[f] in r1.ECARTS)) for ws, cls, _r in par[st]] for st in strates for h, f in unites}
    for (st, h, f), s in D.items():
        tete = f"  « {st} » {f} (hôte {h}) ecart : n_s = {len(s)} ; cellules = {cellules(s)} ; "
        if not any(x.startswith(tete) for x in ep):
            raise socle.Refus("P2/ep", "contrôle (f) : n ou K de la série d'écart différent d'EP", st, h)
    publie = [x for x in ep if x.startswith("  D1-bis « ")]
    it = [(st, c) for st in strates for c in courbe([(ws, int(sum(D[st, h, f][i][1] for h, f in unites) >= 2))
                                                      for i, (ws, _c, _r) in enumerate(par[st])], w, ells)]
    for i, (st, c) in enumerate(it):
        if publie[i:i + 1] != [ligne_courbe(f"D1-bis « {st} »", c, dec)]:
            raise socle.Refus("P2/ep", "contrôle (f) : courbe de I_t recalculée depuis les D_u différente d'EP", st,
                              ell=c["ell"])
    if len(publie) != len(it):
        raise socle.Refus("P2/ep", "contrôle (f) : nombre de lignes « D1-bis » différent d'EP")
    v = prm["voisinage"]
    R = {k: reduite(s, w, v["d"]) for k, s in D.items()}
    out = [f"[FIV_u(ℓ)] série d'écart de l'hôte u (r1.ECARTS) sur les fenêtres retenues de la strate, pool D1-bis ; "
           f"FIV_série = σ̂²_bloc/γ̂₀ de r1.block_long_run_variance (forme d'EP l.94) ; garde n ≥ {r1.GARDE_BLOCS}·ℓ "
           "imprimée", "  contrôle : n et K de chaque hôte = n_s et cellules « ecart » d'EP ; FIV_série de I_t "
           f"(D1-bis) recalculée depuis les D_u = EP aux {len(ells)} ℓ : égaux"]
    out += [ligne_courbe(f"« {st} » {f} (hôte {h})", c, dec) for (st, h, f), s in D.items() for c in courbe(s, w, ells)]
    out.append(f"[SENSIBILITÉ VOISINAGE] {v['nom']}, d = {v['d']}, imprimée hors C1 : position retenue retirée si une "
               f"position à distance ≤ d n'est pas retenue dans la strate ; lacune : {v['lacune']} ; {v['bords']} ; "
               f"grille : {v['grille']} ; garde : {v['garde']}")
    for st in strates:
        n2 = len(R[st, unites[0][0], unites[0][1]])
        kk = [cellules(D[st, h, f]) - cellules(R[st, h, f]) for h, f in unites]
        out.append(f"  « {st} » : positions retirées = {len(par[st]) - n2} ; n′ = {n2} ; cellules d'écart voisines "
                   "d'une lacune (K − K′) : " + " ; ".join(f"{h} {k}" for (h, _f), k in zip(unites, kk)))
    return out + [ligne_courbe(f"« {st} » {f} (hôte {h})", c, dec) for (st, h, f), s in R.items()
                  for c in courbe(s, w, ells)]


def analyse(d: dict, ps2: dict, prm: dict, ep: list) -> dict:
    window = sys.modules["commun"].H["window"]
    pos = portee(d["bornes"], d["w"], d["plages"], d["params"]["strate_calendar"], window)
    m = masque(pos, d["ws"])
    controle_b(pos, m, d["ws"], ps2["strates"], ps2["rendu_j28"]["bloc3"], prm["masque"])
    return {"masque_j28.txt": lignes_masque(d["bornes"], pos, m, ps2["strates"], d["plages"]),
            "fiv_unites.txt": fiv(d, ps2, prm, ep)}


def main(argv=None) -> int:
    return socle.executer("masque_fiv", OBJET, SORTIES, analyse, argv)


if __name__ == "__main__":
    raise SystemExit(main())
