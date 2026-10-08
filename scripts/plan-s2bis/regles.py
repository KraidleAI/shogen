"""Règles pures du lot PLAN-S2BIS (ADR-0029 §2.6, recopiée dans parametres.json) : quantile au rang le plus proche,
τ (grille, bornes, plafond en rationnels exacts), σ ; Decimal sous le contexte nommé du harnais (commun.H)."""
from __future__ import annotations

import math
from decimal import Decimal, localcontext
from fractions import Fraction

import commun


def quantile(valeurs, num: int, den: int):
    """Valeur au rang ⌈num·N/den⌉ (1-indexé, borné à [1, N]) des valeurs triées : rang le plus proche, méthode de
    closure.percentile_nearest_rank (citée ; module en quarantaine, non importé) et de r1._tau_observe ; N = 0 : None."""
    v = sorted(valeurs)
    return v[min(max((num * len(v) + den - 1) // den, 1), len(v)) - 1] if v else None


def regle_tau(facteur: Decimal, x, pas: Decimal, basse: Decimal, haute: Decimal) -> tuple:
    """τ = grid-ceil(facteur × x, pas), contraint par basse ≤ τ < haute (ADR-0029 §2.6 ; ADR-0022) : produit et plafond en
    rationnels exacts. Sous la borne basse, premier multiple ≥ basse, avec drapeau ; à ou au-delà de la borne haute, REFUS
    nommé et aucun τ (adjudication A-2 de l'orchestrateur, 2026-10-04). Rend (τ ou None, drapeau ou None, valeur de la
    règle) ; x None : (None, « aucune cellule », None)."""
    if x is None:
        return None, "aucune cellule", None
    p = Fraction(pas)
    k = math.ceil(Fraction(facteur) * Fraction(x) / p)
    k_bas, k_haut = math.ceil(Fraction(basse) / p), math.ceil(Fraction(haute) / p) - 1
    with localcontext(commun.H["r1"].contexte_decimal()):
        regle = Decimal(k) * pas
        if k > k_haut:
            return None, f"REFUS : valeur de la règle {regle} ≥ borne haute exclue {haute} (A-2)", regle
        if k < k_bas:
            return Decimal(k_bas) * pas, f"borne basse appliquée (valeur de la règle : {regle})", regle
        return regle, None, regle


def regle_sigma(facteur: Decimal, p99s: list, plancher) -> tuple:
    """σ = max(plancher, facteur × max des P99 de staleness des strates) (règle de clôture d'ADR-0021, maximum sur les
    strates, ADR-0029 §2.6) ; plancher None : (None, motif) ; aucune staleness : (plancher, motif)."""
    if plancher is None:
        return None, "aucun plancher : axe staleness non évaluable pour la classe"
    vals = [v for v in p99s if v is not None]
    if not vals:
        return Decimal(plancher), "aucune staleness observée : plancher (repli de la règle de clôture)"
    with localcontext(commun.H["r1"].contexte_decimal()):
        return +max(Decimal(plancher), facteur * max(vals)), None
