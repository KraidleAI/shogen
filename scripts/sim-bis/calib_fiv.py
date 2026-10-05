"""Calibration E1 du groupement (G0 docs/adr-0029/g0-sim/G0-SIM-BIS.md ; sous-lot SB-10 ; E-S-38, E-S-39) : SB-10a :
estimateur FIV_série(ℓ) de la forme de PLAN-S2BIS (r1.block_long_run_variance de f35a70c, forme de r1.bloc_strate ;
scripts/plan-s2bis/episodes.py, courbe) sur masques entiers : bit j = position j de la grille de la strate, présente
ou non ; une position absente ne forme aucune paire. Numérateur entier exact, valeurs publiées en Decimal sous le
contexte de r1 (précision calibration.precision, ROUND_HALF_EVEN, le reste du DefaultContext), FIV exact en Fraction.
Entiers et rationnels seuls : aucun flottant, aucune puissance."""
from decimal import ROUND_HALF_EVEN, Context, Decimal
from fractions import Fraction

import commun


def _entree(pres, val, ells) -> None:
    """Masques entiers ≥ 0 (booléen refusé), I_t ⊂ positions présentes, ℓ liste non vide d'entiers ≥ 1, sinon
    FIV/entree."""
    if not (type(pres) is int and type(val) is int and pres >= 0 and val >= 0 and not val & ~pres):
        raise commun.Refus("FIV/entree", f"masques {pres!r}, {val!r} : entiers ≥ 0, série dans les positions présentes")
    if type(ells) is not list or not ells or any(type(e) is not int or e < 1 for e in ells):
        raise commun.Refus("FIV/entree", f"ℓ = {ells!r} : liste non vide d'entiers ≥ 1")


def courbe(pres: int, val: int, ells: list, k: dict) -> list:
    """Par ℓ de `ells` (dans leur ordre), sur la série I (val) des positions présentes (pres) : n, K, numérateur
    N = ℓ·n²·σ̂²_bloc = ℓ·n·K(n − K) + Σ_{j=1}^{ℓ−1} 2(ℓ − j)·A_j, A_j = n²·C_j − n·K·(S_g + S_d) + M_j·K² (paires de
    lag j : M_j présentes aux deux bouts, C_j à 1 aux deux bouts, S_g à 1 au début, S_d à 1 à la fin ; r1 de f35a70c,
    formule de block_long_run_variance), calculé par sommes préfixes des A_j jusqu'au plus grand ℓ ; γ̂₀ = (nK − K²)/n
    et σ̂²_bloc = N/(ℓn²) en Decimal (une division chacun), FIV_serie = σ̂²_bloc/γ̂₀ (division des deux valeurs
    publiées, forme d'episodes.courbe) ; fiv = N/(ℓ·n·K(n − K)) exact ; garde = n ≥ garde_blocs·ℓ (k : section
    « calibration » de parametres.json). n = 0 : γ̂₀, σ̂² et FIV à None ; γ̂₀ = 0 (K ∈ {0, n}) : FIV à None."""
    _entree(pres, val, ells)
    ctx = Context(prec=k["precision"], rounding=ROUND_HALF_EVEN)
    n, K, voulus = pres.bit_count(), val.bit_count(), set(ells)
    sommes, a, b = {1: (0, 0)}, 0, 0
    for j in range(1, max(ells)):
        pj, vj = pres >> j, val >> j
        aj = (n * n * (val & vj).bit_count() + (pres & pj).bit_count() * K * K
              - n * K * ((val & pj).bit_count() + (pres & vj).bit_count()))
        a, b = a + aj, b + j * aj
        if j + 1 in voulus:
            sommes[j + 1] = (a, b)
    out = []
    for ell in ells:
        num = ell * (n * K * (n - K) + 2 * sommes[ell][0]) - 2 * sommes[ell][1]
        g0 = ctx.divide(Decimal(n * K - K * K), Decimal(n)) if n else None
        s2 = ctx.divide(Decimal(num), Decimal(ell * n * n)) if n else None
        defini = n and 0 < K < n
        out.append({"ell": ell, "n": n, "K": K, "numerateur": num, "gamma0": g0, "sigma2_bloc": s2,
                    "FIV_serie": ctx.divide(s2, g0) if defini else None,
                    "fiv": Fraction(num, ell * n * K * (n - K)) if defini else None,
                    "garde": n >= k["garde_blocs"] * ell})
    return out
