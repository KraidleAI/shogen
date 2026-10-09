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
