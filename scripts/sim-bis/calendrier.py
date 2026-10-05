"""Calendrier du lot SIM-BIS (G0 docs/adr-0029/g0-sim/G0-SIM-BIS.md ; sous-lot SB-5 ; E-S-14, E-S-25) : grille UTC
de pas w depuis T_début (lundi de référence 00:00 UTC + d jours, d tiré, Q-S-08), strates calme et stress par le
calendrier de S2 (jour UTC, réplique de window.weekday_utc et strate_from_spec de f35a70c), échelle des durées. Masques :
entiers, bit j = fenêtre T_début + j·w."""
from fractions import Fraction

import aleas
import commun

JOURS = aleas.Empirique([(d, 1) for d in range(7)])


def jour_semaine(ws: int) -> int:
    """Jour UTC de l'instant `ws` (epoch s), lundi = 0 : l'époque Unix est un jeudi, d'où (ws // 86400 + 3) % 7."""
    return (ws // 86400 + 3) % 7


def strate(ws: int, cal: dict) -> str:
    """« stress » si le jour UTC est un jour de stress de parametres.json (samedi et dimanche), « calme » sinon."""
    return "stress" if jour_semaine(ws) in cal["jours_stress"] else "calme"


def echelle(cal: dict, semaines: int) -> dict:
    """E-S-25 : n_s = n_par_semaine[s]·W par strate ; T_max = W semaines × facteur t_max, en fenêtres de grille,
    entier exigé (sinon CALENDRIER/t_max)."""
    t = Fraction(semaines * 7 * 86400 // cal["w"]) * Fraction(*cal["t_max"])
    if t.denominator != 1:
        raise commun.Refus("CALENDRIER/t_max", f"{semaines} semaines × {cal['t_max']} : {t} fenêtres")
    return {"n": {s: x * semaines for s, x in cal["n_par_semaine"].items()}, "t_max": int(t)}


def t_debut(cal: dict, u) -> int:
    """T_début (epoch s) : lundi de référence 00:00 UTC (sinon CALENDRIER/lundi) + d jours, d uniforme sur 0..6 par
    seuils exacts (Q-S-08)."""
    if cal["lundi_reference"] % 86400 or jour_semaine(cal["lundi_reference"]):
        raise commun.Refus("CALENDRIER/lundi", f"{cal['lundi_reference']} : lundi 00:00 UTC attendu")
    return cal["lundi_reference"] + 86400 * JOURS.tirer(u)


def masques(cal: dict, debut: int, t_max: int) -> dict:
    """{strate : masque} sur la grille de t_max fenêtres depuis `debut` (minuit UTC exigé, sinon CALENDRIER/debut),
    journée par journée ; aucun bit au-delà de t_max."""
    fpj = 86400 // cal["w"]
    if debut % 86400 or fpj * cal["w"] != 86400:
        raise commun.Refus("CALENDRIER/debut", f"début {debut}, w = {cal['w']} : minuit UTC et w diviseur du jour")
    out, jour = {"calme": 0, "stress": 0}, (1 << fpj) - 1
    for k in range(-(-t_max // fpj)):
        out[strate(debut + 86400 * k, cal)] |= jour << (fpj * k)
    return {s: m & ((1 << t_max) - 1) for s, m in out.items()}
