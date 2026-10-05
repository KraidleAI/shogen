"""Calibration du lot SIM-BIS (G0 docs/adr-0029/g0-sim/G0-SIM-BIS.md ; sous-lot SB-2 ; E-S-37, E-S-02) : lecture d'EP
(`episodes.txt` versé par PLAN-S2BIS, forme de scripts/plan-s2bis/episodes.py l.92-120) sous ses deux épingles. Forme
exigée ligne à ligne, dans l'ordre de parametres.json (strates, unités, types) : sinon CALIB/forme ; section FIV :
en-tête et nombre de lignes seuls à ce sous-lot.
Nombres pris en rationnels exacts depuis leur écriture décimale. Contrôles de cohérence, sinon CALIB/coherence : chaque
quotient imprimé est refait sous le contexte décimal de r1 de f35a70c (précision 50, ROUND_HALF_EVEN, le reste du
DefaultContext) et comparé chaîne pour chaîne. L'histogramme d'EP compte tous les épisodes, censurés compris."""
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


def _forme(i: int, ligne: str, attendu: str):
    raise commun.Refus("CALIB/forme", f"EP l.{i + 1} : {ligne[:90]!r}, attendu {attendu}")


def _egal(i: int, quoi: str, lu, attendu) -> None:
    if lu != attendu:
        raise commun.Refus("CALIB/coherence", f"EP l.{i + 1} : {quoi} : lu {lu}, attendu {attendu}")


def _episode(i: int, m, h, k: dict, ctx) -> dict:
    """Enregistrement d'une ligne d'épisodes et de son histogramme, après contrôle de cohérence."""
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
          [next(x for c, x in rang_val if c >= -(-q * ep // 100)) for q in k["quantiles"]])
    return {"n_s": n_s, "cellules": cel, "episodes": ep, "censures": cens, "complets": e[-1], "max": mx,
            "taux": Fraction(m.group(5)), "moyenne": Fraction(m.group(6)), "quantiles": e[:-1],
            "moyenne_complets": Fraction(m.group(9 + nq)), "histogramme": hist}


def analyser(texte: str, k: dict) -> dict:
    """{"episodes": {(strate, hôte, type): enregistrement}} d'EP ; `k` : section
    « calibration » de parametres.json. Refus nommé sur tout écart de forme ou de cohérence, quotient par zéro
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
    lignes, out = texte.split(commun.NL), {"episodes": {}}
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
    return out


def charger(prm: dict, lus=None, environ=None) -> dict:
    """EP lu sous ses deux épingles (commun.lire_entree, E-S-02), puis analysé."""
    return analyser(commun.lire_entree(prm, "episodes", lus, environ).decode("utf-8"), prm["calibration"])
