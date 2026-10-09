"""Exécution du lot SIM-BIS (G0 docs/adr-0029/g0-sim/G0-SIM-BIS.md : PROPOSITION corrigée par AVIS, ajouts datés compris
; sous-lot SB-11 ; E-S-40 à E-S-48, E-S-52). SB-11a : taux d'une cellule (x sur R réplications, r̂ exact, erreur-type en
Decimal sous le contexte de r1, borne unilatérale à 95 % quand x = 0 ; E-S-40, E-S-43) ; fréquences des valeurs et des
causes de NON ÉVALUABLE, par cause et par combinaison (E-S-52). Entiers, rationnels et Decimal seuls : aucun flottant,
aucune puissance, aucune fonction de libm."""
from decimal import Decimal
from fractions import Fraction

import calib_fiv
import commun
import regle

VALEURS = ("REJETTE", "NE REJETTE PAS", "NON ÉVALUABLE")
INSUFFISANTE = ("unites", "k_crit", "runs")         # information insuffisante (E-S-52) ; n_prime compté à part


def taux(x: int, R: int, k: dict) -> dict:
    """E-S-40 : x sur R réplications : r̂ = x/R exact ; SE = √(r̂(1 − r̂)/R) = √(x(R − x)/R³), une division puis une
    racine sous le contexte de r1 (calib_fiv.contexte de la section « calibration » : précision 50, ROUND_HALF_EVEN) ;
    borne unilatérale à 95 % 1 − 0,05^(1/R) quand x = 0, soit 1 − exp(ln(1/20)/R) par Decimal.ln et Decimal.exp sous
    le même contexte (aucune fonction de libm, E-S-43), None sinon. x, R entiers, 0 ≤ x ≤ R, R ≥ 1, sinon EXEC/taux."""
    if type(x) is not int or type(R) is not int or not 0 <= x <= R or R < 1:
        raise commun.Refus("EXEC/taux", f"x = {x!r}, R = {R!r} : entiers, 0 ≤ x ≤ R, R ≥ 1")
    ctx = calib_fiv.contexte(k)
    se = ctx.sqrt(ctx.divide(Decimal(x * (R - x)), Decimal(R * R * R)))
    borne = None
    if x == 0:
        ln = ctx.ln(ctx.divide(Decimal(1), Decimal(20)))
        borne = ctx.subtract(Decimal(1), ctx.exp(ctx.divide(ln, Decimal(R))))
    return {"x": x, "R": R, "r": Fraction(x, R), "SE": se, "borne": borne}


def frequences(resultats: list) -> dict:
    """E-S-52 (et AVIS-SIM-T3, observation 3) : sur les résultats d'une classe dans une strate ({"valeur", "causes"}
    par réplication), comptes par valeur, par cause de NON ÉVALUABLE (non exclusives, ordre de regle.CAUSES),
    information insuffisante (au moins une cause parmi unites, k_crit, runs) et par combinaison de causes (jointes par
    « + » dans l'ordre de regle.CAUSES ; les combinaisons somment au compte de NON ÉVALUABLE). Valeur hors de VALEURS,
    causes hors de regle.CAUSES, dans le désordre ou en double, NON ÉVALUABLE sans cause, valeur évaluée avec une
    cause : EXEC/frequences."""
    out = {"valeurs": dict.fromkeys(VALEURS, 0), "causes": dict.fromkeys(regle.CAUSES, 0), "insuffisante": 0,
           "combinaisons": {}}
    for x in resultats:
        v, c = x.get("valeur"), x.get("causes")
        if (v not in VALEURS or type(c) is not list or c != [y for y in regle.CAUSES if y in c]
                or (v == VALEURS[2]) != bool(c)):
            raise commun.Refus("EXEC/frequences", f"valeur {v!r}, causes {c!r}")
        out["valeurs"][v] += 1
        for y in c:
            out["causes"][y] += 1
        if c:
            out["insuffisante"] += any(y in INSUFFISANTE for y in c)
            cle = "+".join(c)
            out["combinaisons"][cle] = out["combinaisons"].get(cle, 0) + 1
    return out
