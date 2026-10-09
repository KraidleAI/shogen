"""σ par actif et par classe de source (PROPOSITION §4.6 ; ADR-0029 l.189 et son ajout daté l.403 (3) ; AVIS Q-CA-07),
calculé avant τ (E-CA-17) : places horodatées max(30 s, σ_BTC, troisième terme), le troisième terme étant
grid-ceil(3 × max sur les strates du P99 des âges par cellule, 60 s) sur les seules places à horodatage de dernière
transaction de la lecture (aucune : terme absent) ; agrégateurs max(300 s, σ_BTC) ; places sans horodatage : aucun σ ;
oracles : 1,5 × heartbeat (socle.oracles). σ_BTC lu dans tau_sigma.txt, arrondi à la seconde supérieure. Entiers et
rationnels seuls ; le P99 des suites et la population de toutes les places horodatées sont descriptifs."""
from __future__ import annotations

import math
from fractions import Fraction

import socle


def population(prm: dict, actif: str) -> list:
    """Places du troisième terme : horodatage de dernière transaction, dans la lecture retenue (Q-CA-07 (b))."""
    return socle.lecture(prm)["derniere_transaction"][actif]


def cellules(ages: list, strates: list) -> dict:
    """{strate : âges des cellules définies} d'une place (âge en minutes, None avant la première minute active)."""
    out = {}
    for a, st in zip(ages, strates):
        if a is not None:
            out.setdefault(st, []).append(a)
    return out


def suites(ages: list, strates: list) -> dict:
    """{strate : durées des suites sans échange} (descriptif) : une suite finit à la dernière minute d'âge non nul
    avant une minute active ou la fin de la fenêtre ; elle compte dans la strate de cette minute."""
    out = {}
    for i, (a, st) in enumerate(zip(ages, strates)):
        if a and (i + 1 == len(ages) or not ages[i + 1]):
            out.setdefault(st, []).append(a)
    return out


def troisieme_terme(prm: dict, ages: dict, strates: list) -> tuple:
    """(σ du terme en secondes ou None, détail {strate : (N, P99 des cellules, P99 des suites)}) sur les places de
    `ages` {place : âges} : P99 au rang ⌈99·N/100⌉ par strate, maximum sur les strates, × 3 × 60 s, grid-ceil à 60 s."""
    s, cel, sui = prm["sigma"], {}, {}
    for a in ages.values():
        for st, v in cellules(a, strates).items():
            cel.setdefault(st, []).extend(v)
        for st, v in suites(a, strates).items():
            sui.setdefault(st, []).extend(v)
    detail = {st: (len(cel.get(st, [])), socle.quantile(cel.get(st, []), *s["rang"]),
                   socle.quantile(sui.get(st, []), *s["rang"])) for st in ("calme", "stress")}
    p99 = [d[1] for d in detail.values() if d[1] is not None]
    if not p99:
        return None, detail
    k = math.ceil(Fraction(s["facteur"]) * max(p99) * 60 / s["pas_s"])
    return k * s["pas_s"], detail


def sigmas(prm: dict, actif: str, btc: dict, terme, mode: str) -> dict:
    """{classe : σ en secondes ou None} d'un actif ; en « planchers seuls », aucun troisième terme (§4.7) ; σ_BTC
    absent pour une classe qui le lit : CA/btc."""
    pl, out = prm["sigma"]["planchers_s"], {"sans_horodatage": None, "oracle_chainlink": socle.oracles(prm)[actif][1]}
    for classe in ("agregateur", "place_horodatee"):
        if ("sigma", classe) not in btc:
            raise socle.Refus("CA/btc", "σ de BTC absent ou refusé", actif, classe)
        termes = [pl[classe], math.ceil(Fraction(btc["sigma", classe]))]
        if classe == "place_horodatee" and mode == "calibre" and terme is not None:
            termes.append(terme)
        out[classe] = max(termes)
    return out
