"""Calibration E1 câblée (G0 docs/adr-0029/g0-sim/G0-SIM-BIS.md ; sous-lot SB-11 ; E-S-38 ; ajout daté du G0 du
2026-10-05 15:05:43 UTC, points (1), (3), (6) et (8) ; Q-SI-8 (a) à (e) de SIM-INTEG ; SHOGEN-SIM-BIS-SB11-BRIEF-1,
SHOGEN-SIM-BIS-SB11-IMPRESSIONS-1). SB-11j : réplication d'E1 (courbes de I_t et des dix hôtes du format sur le masque,
issues d'un même appel de calib_fiv.replication), lot d'un point, agrégation d'un point (moyennes exactes, réplications
indéfinies par hôte, variance exacte et écart-type des FIV de I_t). SB-11k : choix de C1 et de C2 (calib_fiv.selection,
FIV_u par calibration.charger_unites, Q-SI-8 (b)), lignes [BORD E1] et phrases (8)(ii) et (iii) (Q-SI-8 (c)),
impressions par hôte du point (6). Entiers, rationnels et Decimal seuls : aucun flottant, aucune puissance, aucune
fonction de libm."""
from decimal import Decimal
from fractions import Fraction

import calib_fiv
import calibration
import executer

PHRASE_II = ("dans la strate {s}, la famille E1 n'atteint pas les FIV_u mesurés ; C1 y est une borne basse de la "
             "mesure, et « borne haute » ne s'applique pas")
PHRASE_III = ("si W*(C1) ≤ 16 et que C1-calme est au bord, le paquet dit que les 16 semaines reposent sur un niveau "
              "que la famille ne peut pas dépasser : information à l'investisseur à l'accord A-1 de S-2, sans "
              "question ; si W*(C1) > 16, A-2 porte la même phrase ; les trois W* sont imprimés (SB-12)")


def _fivs(courbe: list) -> list:
    return [x["fiv"] for x in courbe]


def replication_e1(prm: dict, ep: dict, cal: dict, point, i: int) -> dict:
    """Réplication i du point (C0 : None) d'E1 (Q-SI-8 (a) et (e)) : un seul appel de calib_fiv.replication (cellule
    calib_fiv.cellule du point) ; par strate, FIV exacts par ℓ de calibration.ell (calib_fiv.courbe, None si indéfinis)
    de la série I_t et de la série D*(u) de chacun des dix hôtes du format, sur les positions présentes (masque)."""
    r, k = calib_fiv.replication(prm, ep, cal, point, calib_fiv.cellule(prm, point), i), prm["calibration"]
    return {"i": i, "strates": {s: {"I": _fivs(calib_fiv.courbe(pos, val, k["ell"], k)),
                                    "unites": {h: _fivs(calib_fiv.courbe(pos, d, k["ell"], k))
                                               for h, d in r["unites"][s].items()}}
                                for s, (pos, val) in r["strates"].items()}}


def lot_e1(prm: dict, ep: dict, cal: dict, point, plage, processus: int, dossier: str, entete: list) -> tuple:
    """Lot (cellule du point, [a, b)) d'E1 : réplications i = a à b − 1 (replication_e1, flux par i), en `processus`
    processus dans l'ordre (executer.appliquer), un fichier partiel (executer.ecrire_lot) ; rend (chemin, sha256)."""
    a, b = plage
    recs = executer.appliquer(replication_e1, [(prm, ep, cal, point, i) for i in range(a, b)], processus)
    return executer.ecrire_lot(dossier, calib_fiv.cellule(prm, point), a, b, recs, entete)


def _courbes(xs: list) -> list:
    return [[{"fiv": None if v is None else Fraction(v)} for v in x] for x in xs]


def moyennes_point(recs: list, k: dict) -> dict:
    """Agrégation d'un point sur ses réplications (enregistrements relus, dans l'ordre) : par strate, I_t et chaque
    hôte : calib_fiv.moyenne (moyenne exacte des FIV définis, réplications indéfinies comptées à part : Q-T4-6,
    Q-SI-8 (d)) ; pour I_t, par ℓ, variance exacte des FIV définis (dénominateur m − 1 ; None si m < 2) et écart-type
    par Decimal.sqrt sous le contexte de r1, à l'impression seulement (point (6))."""
    ctx, out = calib_fiv.contexte(k), {}
    for s, x0 in recs[0]["strates"].items():
        ii = [e["strates"][s]["I"] for e in recs]
        m, d = calib_fiv.moyenne(_courbes(ii)), [[Fraction(v) for v in x] for x in ii if x[0] is not None]
        var = [None if len(d) < 2 else sum(((x[j] - m["fiv"][j]) * (x[j] - m["fiv"][j]) for x in d), Fraction(0))
               / (len(d) - 1) for j in range(len(ii[0]))]
        et = [None if v is None else ctx.sqrt(ctx.divide(Decimal(v.numerator), Decimal(v.denominator))) for v in var]
        out[s] = {"I": m, "variance": var, "ecart_type": et,
                  "unites": {h: calib_fiv.moyenne(_courbes([e["strates"][s]["unites"][h] for e in recs]))
                             for h in x0["unites"]}}
    return out


def phrases_bord(sel: dict) -> list:
    """Phrases du point (8) (ajout daté du G0, texte du G0) : (8)(ii) pour chaque strate au bord ; (8)(iii) si C1-calme
    est au bord, sa condition sur W*(C1) écrite telle quelle (les W* sont calculés par SB-12, après E1)."""
    out = [f"[BORD E1] (8)(ii) « {s} » : " + PHRASE_II.format(s=s) for s, x in sel.items() if x["bord"]["au_bord"]]
    return out + (["[BORD E1] (8)(iii) : " + PHRASE_III] if sel.get("calme", {}).get("bord", {}).get("au_bord") else [])


def _par_hote(prm: dict, moy: dict, s: str, h: str, fu: list, c1, ctx) -> dict:
    """Impressions du point (6) pour l'hôte h de la strate s : résidus ln F̄_u,C1(ℓ) − ln F_u(ℓ) aux ℓ retenus (garde
    de fiv_unites.txt tenue, F_u défini ; None si F̄ indéfini) ; point qui minimiserait Q₁ pour cet hôte seul
    (calib_fiv.q1 réduit à l'hôte, égalités par calib_fiv._rang ; diagnostic, jamais candidat ; None sans ℓ retenu) ;
    réplications à FIV indéfini de chaque point (Q-SI-8 (d))."""
    ells, g = prm["calibration"]["ell"], calib_fiv.grille(prm)
    js, mb = [j for j, c in enumerate(fu) if c["garde"] and c["fiv"] is not None], moy[c1][s]["unites"][h]["fiv"]
    q = [(calib_fiv.q1({h: moy[p][s]["unites"][h]}, {h: fu}, ells, ctx), p) for p in g] if js else []
    d = [x for x in q if x[0] is not None]
    return {"residus_C1": [[ells[j], None if mb[j] is None else ctx.subtract(calib_fiv._ln(mb[j], ctx), calib_fiv._ln(
                fu[j]["fiv"], ctx))] for j in js], "point_Q1": min(d, key=calib_fiv._rang)[1] if d else None,
            "indefinies": {calib_fiv.cellule(prm, p): moy[p][s]["unites"][h]["indefinies"] for p in g}}


def calibrer(prm: dict, cal: dict, moy: dict, lus=None, environ=None) -> dict:
    """C2 et C1 de chaque strate et constats d'E1, sur les agrégats des points (moy = {point de la grille, et None
    pour C0 : moyennes_point}) : EP sous ses deux épingles (calibration.charger) ; cible = courbe FIV_série du pool
    e1.pool ; FIV_u de fiv_unites.txt par calibration.charger_unites(prm, cal["presentes"], ep), contrôlés contre le
    masque et EP (Q-SI-9 ; Q-SI-8 (b) : jamais analyser_unites) ; calib_fiv.selection ; par strate, ligne [BORD E1]
    (calib_fiv.ligne_bord) et impressions par hôte (_par_hote) ; phrases du point (8) (phrases_bord)."""
    e, st = calibration.charger(prm, lus, environ), prm["calibration"]["strates"]
    ctx = calib_fiv.contexte(prm["calibration"])
    unites = calibration.charger_unites(prm, cal["presentes"], e["episodes"], lus, environ)
    sel = calib_fiv.selection(prm, {s: e["fiv"][prm["e1"]["pool"], s] for s in st},
                              {p: {s: m[s]["I"] for s in m} for p, m in moy.items()}, unites,
                              {p: {s: m[s]["unites"] for s in m} for p, m in moy.items() if p is not None})
    out = {"strates": {}, "phrases": phrases_bord(sel)}
    for s in st:
        out["strates"][s] = dict(sel[s], ligne_bord=calib_fiv.ligne_bord(s, sel[s]["bord"]), unites={
            h: _par_hote(prm, moy, s, h, fu, sel[s]["C1"], ctx) for h, fu in unites[s].items()})
    return out
