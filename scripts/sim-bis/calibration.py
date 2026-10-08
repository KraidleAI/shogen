"""Calibration du lot SIM-BIS (G0 docs/adr-0029/g0-sim/G0-SIM-BIS.md ; sous-lot SB-2 ; E-S-37, E-S-02) : lecture d'EP
(`episodes.txt` versé par PLAN-S2BIS, forme de scripts/plan-s2bis/episodes.py l.92-120) sous ses deux épingles. Forme
exigée ligne à ligne, dans l'ordre de parametres.json (strates, unités, types ; pools, strates, ℓ) : sinon CALIB/forme.
Nombres pris en rationnels exacts depuis leur écriture décimale. Contrôles de cohérence, sinon CALIB/coherence : chaque
quotient imprimé est refait sous le contexte décimal de r1 de f35a70c (précision 50, ROUND_HALF_EVEN, le reste du
DefaultContext) et comparé chaîne pour chaîne. L'histogramme d'EP compte tous les épisodes, censurés compris. SB-15d
(ajout daté du G0 du 2026-10-05 15:05:43 UTC, point (1)) : lecture de fiv_unites.txt de PLAN-S2BIS-2, même analyseur de
ligne de courbe que pour EP (SHOGEN-SIM-BIS-POOL-EP-SEPARES-1, précision de l'annexe B, B.77)."""
import re
from decimal import ROUND_HALF_EVEN, Context, Decimal
from fractions import Fraction

import commun

ETIQUETTE_EP = "préparation de S2-bis ; ne change pas le verdict de S2 (« R1 discrimine » = FAUX)"
TETE_EPISODES = ("[ÉPISODES] descriptif, pour calibrer SIM-NIVEAU-BIS et SIM-PUISSANCE-BIS ; classement sous les σ "
                 "et τ committés de S2 ; unités du pool D1-bis de la strate ; quantiles au rang le plus proche (P50, "
                 "P90, P99)")
TETE_FIV = ("[FIV_SÉRIE(ℓ)] σ̂²_bloc(ℓ)/γ̂₀, série I_t = 1{au moins deux écarts} ; garde n ≥ 30·ℓ imprimée ; pool S2 "
            "contrôlé égal au bloc de compute_r1 à ℓ = 240")
EN, NB = "([0-9]+)", "([0-9]+(?:[.][0-9]+)?)"
L_FV = re.compile(" : n = " + EN + " ; K = " + EN + " ; FIV_série = ([0-9]+(?:[.][0-9]+)?|-) ; σ̂²_bloc = " + NB +
                  " ; γ̂₀ = " + NB + " ; cv théorique = " + NB + " ; garde : (tenue|non tenue)")
TETE_UNITES = ("[FIV_u(ℓ)] série d'écart de l'hôte u (r1.ECARTS) sur les fenêtres retenues de la strate, pool D1-bis ; "
               "FIV_série = σ̂²_bloc/γ̂₀ de r1.block_long_run_variance (forme d'EP l.94) ; garde n ≥ 30·ℓ imprimée")
CONTROLE_UNITES = ("  contrôle : n et K de chaque hôte = n_s et cellules « ecart » d'EP ; FIV_série de I_t (D1-bis) "
                   "recalculée depuis les D_u = EP aux {} ℓ : égaux")
SUITE_UNITES = "[SENSIBILITÉ VOISINAGE] "


def _forme(i: int, ligne: str, attendu: str, src: str = "EP"):
    raise commun.Refus("CALIB/forme", f"{src} l.{i + 1} : {ligne[:90]!r}, attendu {attendu}")


def _egal(i: int, quoi: str, lu, attendu, src: str = "EP") -> None:
    if lu != attendu:
        raise commun.Refus("CALIB/coherence", f"{src} l.{i + 1} : {quoi} : lu {lu}, attendu {attendu}")


def _episode(i: int, m, h, k: dict, ctx) -> dict:
    """Enregistrement d'une ligne d'épisodes et de son histogramme, après contrôle de cohérence ; un quantile sans
    rang (au-delà de 100) vaut None, d'où un refus nommé (O-1 de la G2)."""
    nq = len(k["quantiles"])
    n_s, cel, ep, cens, mx, *e = (int(m.group(j)) for j in (1, 2, 3, 4, 7, *range(8, 9 + nq)))
    hist = [tuple(int(y) for y in x.split("×")) for x in h.group(1).split(" ")]
    lg = [x for x, _n in hist]
    _egal(i, "taux = cellules/n_s", m.group(5), str(ctx.divide(Decimal(cel), Decimal(n_s))))
    _egal(i, "moyenne = cellules/épisodes", m.group(6), str(ctx.divide(Decimal(cel), Decimal(ep))))
    _egal(i, "complets = épisodes − censurés", e[-1], ep - cens)
    _egal(i, "maximum de l'histogramme", mx, max(lg))
    _egal(i + 1, "épisodes = somme des nombres", ep, sum(n for _x, n in hist))
    _egal(i + 1, "cellules = somme des longueurs", cel, sum(x * n for x, n in hist))
    _egal(i + 1, "longueurs ≥ 1 strictement croissantes, nombres ≥ 1",
          lg == sorted(set(lg)) and min(lg + [n for _x, n in hist]) >= 1, True)
    cumul, rang_val = 0, []
    for x, n in hist:
        cumul += n
        rang_val.append((cumul, x))
    _egal(i, "quantiles au rang le plus proche", e[:-1],
          [next((x for c, x in rang_val if c >= -(-q * ep // 100)), None) for q in k["quantiles"]])
    return {"n_s": n_s, "cellules": cel, "episodes": ep, "censures": cens, "complets": e[-1], "max": mx,
            "taux": Fraction(m.group(5)), "moyenne": Fraction(m.group(6)), "quantiles": e[:-1],
            "moyenne_complets": Fraction(m.group(9 + nq)), "histogramme": hist}


def _point(i: int, ell: int, m, k: dict, ctx, src: str = "EP") -> dict:
    """Point (ℓ) d'une courbe FIV_série, après contrôle de cohérence ; FIV « - » (indéfini, forme de dec de
    scripts/plan-s2bis/commun.py) si et seulement si γ̂₀ = 0 : fiv None."""
    n, kk, fiv, s2, g0, cv = int(m.group(1)), int(m.group(2)), *m.group(3, 4, 5, 6)
    garde = m.group(7) == "tenue"
    _egal(i, "FIV_série = σ̂²_bloc/γ̂₀", fiv,
          "-" if Decimal(g0) == 0 else str(ctx.divide(Decimal(s2), Decimal(g0))), src)
    _egal(i, "γ̂₀ = (nK − K²)/n", g0, str(ctx.divide(Decimal(n * kk - kk * kk), Decimal(n))), src)
    _egal(i, "garde = (n ≥ garde_blocs·ℓ)", garde, n >= k["garde_blocs"] * ell, src)
    _egal(i, "cv = √(4ℓ/3n)", cv, str(ctx.sqrt(ctx.divide(Decimal(4 * ell), Decimal(3 * n)))), src)
    return {"ell": ell, "n": n, "K": kk, "fiv": None if fiv == "-" else Fraction(fiv), "sigma2": Fraction(s2),
            "gamma0": Fraction(g0), "cv": Fraction(cv), "garde": garde}


def _ligne_fiv(i: int, ligne: str, tete: str, ell: int, k: dict, ctx, unites: bool = False) -> dict:
    """Ligne de courbe FIV_série de la forme d'EP l.94 après le préfixe `tete` : un seul analyseur pour EP et
    fiv_unites.txt (SHOGEN-SIM-BIS-POOL-EP-SEPARES-1) ; FIV « - » admis dans fiv_unites.txt seul (`unites` ; hôte à
    K ∈ {0, n}), sinon CALIB/forme ; cohérence : _point."""
    src, m = "fiv_unites.txt" if unites else "EP", L_FV.fullmatch(ligne[len(tete):])
    if not (ligne.startswith(tete) and m) or (m.group(3) == "-" and not unites):
        _forme(i, ligne, tete, src)
    return _point(i, ell, m, k, ctx, src)


def analyser(texte: str, k: dict) -> dict:
    """{"episodes": {(strate, hôte, type): enregistrement}, "fiv": {(pool, strate): [point par ℓ]}} d'EP ; `k` :
    section « calibration » de parametres.json. Refus nommé sur tout écart de forme ou de cohérence, quotient par zéro
    compris."""
    try:
        return _analyser(texte, k)
    except ArithmeticError as e:
        raise commun.Refus("CALIB/coherence", f"quotient impossible ({type(e).__name__})") from None


def _analyser(texte: str, k: dict) -> dict:
    ctx = Context(prec=k["precision"], rounding=ROUND_HALF_EVEN)
    l_ep = re.compile(" : n_s = " + EN + " ; cellules = " + EN + " ; épisodes = " + EN + ", dont censurés " + EN +
                      " ; taux = " + NB + " ; moyenne = " + NB + " ; max = " + EN + " ; " +
                      " ; ".join(f"P{q} = " + EN for q in k["quantiles"]) + " ; complets : " + EN + ", moyenne " + NB)
    l_hi = re.compile("    histogramme [(]longueur×nombre[)] : ([0-9]+×[0-9]+(?: [0-9]+×[0-9]+)*)")
    s, u, t = len(k["strates"]), len(k["unites"]), len(k["types"])
    lignes, out = texte.split(commun.NL), {"episodes": {}, "fiv": {}}
    n = 14 + 2 * s * u * t + len(k["pools"]) * s * len(k["ell"])
    if (len(lignes), lignes[0], lignes[11], lignes[12 + 2 * s * u * t], lignes[-1]) != (
            n, ETIQUETTE_EP, TETE_EPISODES, TETE_FIV, ""):
        _forme(0, lignes[0], f"{n - 1} lignes, étiquette et en-têtes de PLAN-S2BIS, saut de ligne final")
    i = 12
    for st in k["strates"]:
        for hote, f in k["unites"]:
            for ty in k["types"]:
                tete = f"  « {st} » {f} (hôte {hote}) {ty}"
                m, h = l_ep.fullmatch(lignes[i][len(tete):]), l_hi.fullmatch(lignes[i + 1])
                if not (lignes[i].startswith(tete) and m and h):
                    _forme(i, lignes[i], tete)
                out["episodes"][st, hote, ty] = _episode(i, m, h, k, ctx)
                i += 2
    for pool in k["pools"]:
        for st in k["strates"]:
            out["fiv"][pool, st] = []
            for ell in k["ell"]:
                i += 1
                out["fiv"][pool, st].append(_ligne_fiv(i, lignes[i], f"  {pool} « {st} » ℓ = {ell}", ell, k, ctx))
    return out


def charger(prm: dict, lus=None, environ=None) -> dict:
    """EP lu sous ses deux épingles (commun.lire_entree, E-S-02), puis analysé."""
    return analyser(commun.lire_entree(prm, "episodes", lus, environ).decode("utf-8"), prm["calibration"])


def analyser_unites(texte: str, k: dict) -> dict:
    """fiv_unites.txt de PLAN-S2BIS-2 (point (1)) : {strate : {hôte : [point par ℓ]}} de la section [FIV_u(ℓ)] seule
    (la sensibilité au voisinage, imprimée hors C1, n'est pas lue) : étiquette d'EP, en-tête et ligne de contrôle de la
    section, puis les lignes dans l'ordre de parametres.json (strates, hôtes du format calibration.unites, ℓ), préfixe
    « « strate » flux (hôte h) », analysées par _ligne_fiv (FIV « - » admis), puis la section suivante et le saut de
    ligne final ; n commun à toutes les lignes d'une strate (garde commune à ses hôtes) ; sinon CALIB/forme ou
    CALIB/coherence, quotient impossible compris."""
    try:
        ctx, lignes = Context(prec=k["precision"], rounding=ROUND_HALF_EVEN), texte.split(commun.NL)
        i = lignes.index(TETE_UNITES) if lignes.count(TETE_UNITES) == 1 else 0
        j, out = i + 2, {}
        fin = j + len(k["strates"]) * len(k["unites"]) * len(k["ell"])
        if (i == 0 or lignes[0] != ETIQUETTE_EP or lignes[i + 1:i + 2] != [CONTROLE_UNITES.format(len(k["ell"]))]
                or not (lignes[fin:] or [""])[0].startswith(SUITE_UNITES) or lignes[-1] != ""):
            _forme(i, lignes[i], "étiquette, section [FIV_u(ℓ)] et son contrôle, section suivante", "fiv_unites.txt")
        for st in k["strates"]:
            out[st] = {}
            for hote, f in k["unites"]:
                out[st][hote] = []
                for ell in k["ell"]:
                    tete = f"  « {st} » {f} (hôte {hote}) ℓ = {ell}"
                    out[st][hote].append(_ligne_fiv(j, lignes[j], tete, ell, k, ctx, True))
                    j += 1
            _egal(j - 1, f"n commun aux lignes de « {st} »", len({x["n"] for xs in out[st].values() for x in xs}), 1,
                  "fiv_unites.txt")
        return out
    except ArithmeticError as e:
        raise commun.Refus("CALIB/coherence", f"fiv_unites.txt : quotient impossible ({type(e).__name__})") from None


def charger_unites(prm: dict, lus=None, environ=None) -> dict:
    """fiv_unites.txt lu sous ses deux épingles (commun.lire_entree, sommes de PLAN-S2BIS-2), puis analysé."""
    texte = commun.lire_entree(prm, "fiv_unites", lus, environ, sommes="sommes_plan2").decode("utf-8")
    return analyser_unites(texte, prm["calibration"])
