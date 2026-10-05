"""Calibration E1 du groupement (G0 docs/adr-0029/g0-sim/G0-SIM-BIS.md ; sous-lot SB-10 ; E-S-38, E-S-39) : SB-10a :
estimateur FIV_série(ℓ) de la forme de PLAN-S2BIS (r1.block_long_run_variance de f35a70c, forme de r1.bloc_strate ;
scripts/plan-s2bis/episodes.py, courbe) sur masques entiers : bit j = position j de la grille de la strate, présente
ou non ; une position absente ne forme aucune paire. Numérateur entier exact, valeurs publiées en Decimal sous le
contexte de r1 (précision calibration.precision, ROUND_HALF_EVEN, le reste du DefaultContext), FIV exact en Fraction.
SB-10b : portée du segment J28 lue sur EP l.6, calendrier de la grille, réplication du modèle d'E1 (unités
indépendantes vues d'un seul observateur, f = 1, régime caché d'E-S-12), moyenne des courbes d'un point. Entiers et
rationnels seuls : aucun flottant, aucune puissance."""
import re
from decimal import ROUND_HALF_EVEN, Context, Decimal
from fractions import Fraction

import calendrier
import commun
import regle
import sources

NOMBRE = re.compile("(?<![a-z])[0-9]+")         # nombres d'EP l.6 (« t0 » exclu)


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


def portee(texte: str, cal: dict) -> dict:
    """Portée du segment J28 de S2, lue sur EP l.6 (E-S-38 : « calendrier du segment J28 de S2, portée et plage D5
    d'EP l.6 ») : segment [t0 ; t_fin), n fixe, plages exclues [(a, b)]. Forme exigée : la ligne, réécrite depuis ses
    nombres sous la forme de scripts/plan-s2bis/commun.py (executer), lui est identique ; t0 répété, instants multiples
    du pas w, t0 < t_fin, a ≤ b ; sinon CALIB/forme."""
    lignes = texte.split(commun.NL)
    ligne = lignes[5] if len(lignes) > 5 else ""
    x = [int(y) for y in NOMBRE.findall(ligne)]
    plages, ok = list(zip(x[4::2], x[5::2])), len(x) >= 4 and len(x) % 2 == 0
    canon = ok and (f"portée : segment [{x[0]} ; {x[1]}) (t0 = {x[2]}, n fixe = {x[3]}), plages exclues ["
                    + ", ".join(f"({a}, {b})" for a, b in plages) + "]")
    if not (ok and ligne == canon and x[0] == x[2] < x[1] and all(a <= b for a, b in plages)
            and all(y % cal["w"] == 0 for y in x[:2] + x[4:])):
        raise commun.Refus("CALIB/forme", "EP l.6 : portée du segment J28 illisible")
    return {"t0": x[0], "t_fin": x[1], "n_fixe": x[3], "plages": plages}


def calendrier_j28(seg: dict, cal: dict) -> dict:
    """Grille de pas w sur [t0 ; t_fin) : position j = instant t0 + j·w ; strate de chaque journée UTC
    (calendrier.strate, réplique de window de f35a70c), jours partiels compris ; les positions des plages exclues,
    bornes incluses (forme de records.filtre_horodatage de f35a70c), ne sont dans aucune strate. Rend {"masques" :
    {strate : masque}, "horizon" : nombre de positions}."""
    w, t0, tf = cal["w"], seg["t0"], seg["t_fin"]
    out, t = {"calme": 0, "stress": 0}, t0
    while t < tf:
        b = min(tf, (t // 86400 + 1) * 86400)
        out[calendrier.strate(t, cal)] |= ((1 << ((b - t) // w)) - 1) << ((t - t0) // w)
        t = b
    for a, b in seg["plages"]:
        ja, jb = max(0, -(-(a - t0) // w)), min((tf - t0) // w - 1, (b - t0) // w)
        trou = ((1 << (jb - ja + 1)) - 1) << ja if ja <= jb else 0
        out = {s: x & ~trou for s, x in out.items()}
    return {"masques": out, "horizon": (tf - t0) // w}


def replication(prm: dict, ep: dict, cal: dict, point, cellule: str, i: int) -> dict:
    """Une réplication d'E1 (E-S-38) : unités indépendantes vues d'un seul observateur (aucun observateur simulé), à
    f = 1, régime `point` = (φ, κ, τ_D), ou None (C0), dans chaque strate ; ni pannes longues, ni hors-enveloppe, ni
    dérive, ni incident, ni unité faible (sources.Replication, flux de la cellule `cellule`, réplication i) ; état
    D*(u) = H(u) ∪ F(u, BTC) de chaque hôte du pool BTC D1-bis (calibration.unites) ; I_t = 1 si au moins deux hôtes
    sont en écart (regle.deux), sur les positions de chaque strate. Rend {"strates" : {s : (positions, I)},
    "etats" : {hôte : D*}}."""
    fond = {"f": Fraction(1), "regime": {s: point for s in cal["masques"]}, "longues": Fraction(0),
            "autres": Fraction(1), "hors_enveloppe": Fraction(0)}
    rep = sources.Replication(prm, ep, fond, cellule, i, cal["masques"], cal["horizon"])
    etats = {h: rep.pannes(h) | rep.ecarts(h, 0) for h, _f in prm["calibration"]["unites"]}
    i_t = regle.deux(list(etats.values()))
    return {"strates": {s: (m, i_t & m) for s, m in cal["masques"].items()}, "etats": etats}


def moyenne(courbes: list) -> dict:
    """Courbe d'un point d'E1 sur ses réplications (courbes de courbe(), mêmes ℓ) : par ℓ, moyenne exacte des FIV
    définis ; une réplication à FIV indéfini (K ∈ {0, n}, indéfini à tout ℓ) est comptée à part ; aucune définie :
    None ; liste vide : FIV/entree."""
    if not courbes:
        raise commun.Refus("FIV/entree", "aucune courbe")
    definies = [c for c in courbes if c[0]["fiv"] is not None]
    nb = len(definies)
    fiv = [sum((c[j]["fiv"] for c in definies), Fraction(0)) / nb if nb else None for j in range(len(courbes[0]))]
    return {"fiv": fiv, "definies": nb, "indefinies": len(courbes) - nb}
