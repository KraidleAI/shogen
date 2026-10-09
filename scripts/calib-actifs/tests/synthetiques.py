"""Séries synthétiques déterministes (aucun historique réel) : prix autour de 100 à ±0,05, minutes sans échange à
volume nul, pour chaque (actif, place) de la lecture retenue ; valeurs de BTC synthétiques, jamais celles de
tau_sigma.txt. Fenêtre courte à cheval sur le vendredi et le samedi (calme puis stress)."""
from decimal import Decimal

import socle

FEN = {"debut": 1775260500, "fin": 1775261100}                  # 2026-04-03 23:55 à 2026-04-04 00:05 UTC
BTC = {("tau", "agregateur"): Decimal("0.0265"), ("tau", "place_horodatee"): Decimal("0.0045"),
       ("tau", "sans_horodatage"): Decimal("0.0050"), ("sigma", "agregateur"): Decimal(900),
       ("sigma", "place_horodatee"): Decimal(90)}


def serie(j: int, fen=FEN) -> dict:
    """{minute : (clôture, active)} de la place de rang j : active sauf une minute sur cinq (décalée par j)."""
    return {t: (Decimal(100) + Decimal((i * (j + 3)) % 11 - 5) / 100, (i + j) % 5 != 0 or i == 0)
            for i, t in enumerate(socle.minutes(fen))}


def series(prm: dict, actif: str, fen=FEN) -> dict:
    return {p: serie(j, fen) for j, p in enumerate(socle.lecture(prm)["places"][actif])}
