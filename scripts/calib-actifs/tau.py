"""τ des places, des agrégateurs et des oracles (PROPOSITION §4.3 à §4.5 ; ADR-0029 l.187, l.189 et ajout daté l.403
(2) ; AVIS Q-CA-04, Q-CA-06). Population de τ des places : cellules (t, p) au dernier prix connu, au moins N_min
places définies en t ; cellules d'une place à horodatage de dernière transaction exclues quand 60·âge > σ (borne basse
de l'âge, déclarée), leur prix gardé dans la médiane des autres ; écart e = |c − m| / m à la médiane leave-one-out m
des autres places définies (moyenne des deux du milieu pour un nombre pair) ; m ≤ 0 : CA/mediane. Rationnels exacts
(Fraction), jamais de flottant (E-CA-18)."""
from __future__ import annotations

from fractions import Fraction

import socle


def rationnels(c: list) -> list:
    """Clôtures (Decimal ou None) en Fraction, chaque valeur distincte convertie une fois."""
    vus = {}
    return [None if x is None else vus.setdefault(x, Fraction(x)) for x in c]


def mediane(valeurs: list) -> Fraction:
    v, m = sorted(valeurs), len(valeurs)
    return v[m // 2] if m % 2 else (v[m // 2 - 1] + v[m // 2]) / 2


def ecarts(actif: str, closes: dict, ages: dict, strates: list, n_min: int, exclusion: dict) -> dict:
    """{strate : (écarts, places, âges)} des cellules de la population (§4.3 pt 1 et 2 ; Q-CA-04) : closes et ages
    {place : liste sur la grille des minutes} ; exclusion {place : σ en secondes} des places à horodatage de
    dernière transaction."""
    places, out = sorted(closes), {st: ([], [], []) for st in ("calme", "stress")}
    for i, st in enumerate(strates):
        definies = [p for p in places if closes[p][i] is not None]
        if len(definies) < n_min:
            continue
        for p in definies:
            if p in exclusion and 60 * ages[p][i] > exclusion[p]:
                continue
            m = mediane([closes[q][i] for q in definies if q != p])
            if m <= 0:
                raise socle.Refus("CA/mediane", "médiane leave-one-out nulle ou négative", actif, strate=st, place=p)
            e, pl, ag = out[st]
            e.append(abs(closes[p][i] - m) / m)
            pl.append(p)
            ag.append(ages[p][i])
    return out


def places(prm: dict, actif: str, cel: dict) -> dict:
    """τ des places (§4.3 pt 3 ; ADR-0029 l.187) : P99,9 au rang ⌈999·N/1000⌉ par strate, maximum sur les strates, ×
    1,5, grid-ceil à 0,05 %, bornes ; P99 et maximum par strate imprimés ; strate sans cellule : CA/population ; règle à
    la borne haute ou au-delà : CA/borne (la valeur n'entre pas au refus, §5.7)."""
    t, par = prm["tau"], {}
    for st, (e, _pl, _ag) in cel.items():
        if not e:
            raise socle.Refus("CA/population", "aucune cellule à N_min places définies", actif, strate=st)
        par[st] = (len(e), socle.quantile(e, *t["rang"]), socle.quantile(e, 99, 100), max(e))
    p999 = max(v[1] for v in par.values())
    tau, drapeau, valeur = socle.regle(t["facteur"], p999, t["pas"], t["borne_basse"], t["borne_haute_exclue"])
    if tau is None:
        raise socle.Refus("CA/borne", "τ des places à la borne haute exclue ou au-delà", actif)
    return {"tau": tau, "drapeau": drapeau, "regle": valeur, "p999": p999, "strates": par,
            "regle_au_maximum": socle.regle(t["facteur"], max(v[3] for v in par.values()), t["pas"], 0, 1)[2]}


def agregateurs(prm: dict, actif: str, tau_places, btc: dict) -> dict:
    """τ des agrégateurs (§4.4 ; ADR-0029 l.189, ajout daté l.403 (2)) : grid-ceil(τ_places × τ_agr_BTC /
    max(τ_BTC des deux classes de places), 0,05 %), bornes ; imprimés : la règle sous les autres dénominateurs
    (horodatée, sans horodatage, minimum), τ_agr_BTC tel quel, drapeau τ_agr < τ_places (Q-CA-06), jamais un refus.
    τ de BTC absent, refusé ou nul pour une classe lue : CA/btc."""
    cles = [("tau", c) for c in ("agregateur", "place_horodatee", "sans_horodatage")]
    if any(k not in btc or btc[k] <= 0 for k in cles):
        raise socle.Refus("CA/btc", "τ de BTC absent, refusé ou nul", actif, "agregateur")
    a, ph, sh, t = (*(Fraction(btc[k]) for k in cles), prm["tau"])

    def r(den):
        return socle.regle(1, Fraction(tau_places) * a / den, t["pas"], t["borne_basse"], t["borne_haute_exclue"])
    tau, drapeau, valeur = r(max(ph, sh))
    if tau is None:
        raise socle.Refus("CA/borne", "τ des agrégateurs à la borne haute exclue ou au-delà", actif, "agregateur")
    return {"tau": tau, "drapeau": drapeau, "regle": valeur, "sous_places": tau < tau_places,
            "autres": {"place_horodatee": r(ph)[2], "sans_horodatage": r(sh)[2], "minimum": r(min(ph, sh))[2],
                       "tel_quel": btc["tau", "agregateur"]}}

