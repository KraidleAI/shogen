"""Calibration E1 câblée (G0 docs/adr-0029/g0-sim/G0-SIM-BIS.md ; sous-lot SB-11 ; E-S-38 ; ajout daté du G0 du
2026-10-05 15:05:43 UTC, points (1), (3), (6) et (8) ; Q-SI-8 (a) à (e) de SIM-INTEG ; SHOGEN-SIM-BIS-SB11-BRIEF-1,
SHOGEN-SIM-BIS-SB11-IMPRESSIONS-1). SB-11j : réplication d'E1 (courbes de I_t et des dix hôtes du format sur le masque,
issues d'un même appel de calib_fiv.replication), lot d'un point, agrégation d'un point (moyennes exactes, réplications
indéfinies par hôte, variance exacte et écart-type des FIV de I_t). Entiers, rationnels et Decimal seuls : aucun
flottant, aucune puissance, aucune fonction de libm."""
from decimal import Decimal
from fractions import Fraction

import calib_fiv
import executer


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
