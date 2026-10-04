#!/usr/bin/env python3
"""Extraction verbatim des valeurs imprimées par le rendu J28 (blocs 3 et 4) vers des lignes de table Markdown,
pour éviter toute recopie à la main. Rédacteur du rapport docs/11, 2026-10-04. Aucun calcul : des chaînes.
Usage : python3 -B extraire_tables.py <rendu_j28>
"""
import re
import sys

T = open(sys.argv[1], encoding="utf-8").read().split("\n")
NUM = r"(-?[0-9]+(?:\.[0-9]+)?(?:E-?[0-9]+)?)"


def L(n):
    return T[n - 1]


def g(n, motif, i=1):
    m = re.search(motif, L(n))
    if not m:
        raise SystemExit(f"l.{n} : motif absent {motif!r}")
    return m.group(i)


C = {"tete": 435451, "P0": 435465, "P1": 435466, "Pm": 435467, "garde": 435468, "z": 435469, "bloc": 435494,
     "fiv": 435495, "zb": 435496, "runs": 435497, "regle": 435516, "emd": 435518}
S = {"tete": 435471, "P0": 435485, "P1": 435486, "Pm": 435487, "garde": 435488, "z": 435489, "bloc": 435498,
     "fiv": 435499, "zb": 435500, "runs": 435501, "regle": 435519, "emd": 435521}


def ligne(nom, motif, cle, i=1):
    vc = g(C[cle], motif, i)
    vs = g(S[cle], motif, i)
    print(f"| {nom} | `{vc}` | `{vs}` | l.{C[cle]} ; l.{S[cle]} |")


print("| entrée (pt 1) | calme | stress | J28 |")
print("|---|---|---|---|")
ligne("n_s (fenêtres complétées)", r"n = (\d+) fenêtres", "tete")
ligne("K_s (fenêtres à ≥ 2 écarts)", r"K = (\d+)", "tete")
ligne("P̂₀", r"= " + NUM, "P0")
ligne("P̂₁", r"= " + NUM, "P1")
ligne("P̂_more,s", r"= " + NUM, "Pm")
ligne("garde n_s·P̂_more,s(1−P̂_more,s) (seuil 10)", r"= " + NUM, "garde")
ligne("z_s", r"= " + NUM, "z")
ligne("ℓ", r"ℓ = (\d+)", "bloc")
ligne("γ̂₀,s", r"γ̂₀ = " + NUM, "bloc")
ligne("σ̂²_bloc,s", r"σ̂²_bloc = " + NUM, "bloc")
ligne("FIV_s", r"FIV = " + NUM, "fiv")
ligne("R_centrage,s", r"R_centrage = " + NUM, "fiv")
ligne("FIV_série,s", r"FIV_série = " + NUM, "fiv")
ligne("z_bloc,s", r"z_bloc = " + NUM, "zb")
ligne("run maximal de I_t", r"run maximal = (\d+)", "runs")
ligne("EMD_s (fenêtres)", r"\) = " + NUM + r" fenêtres", "emd")
ligne("fraction EMD_s/n_s", r"fraction de n_s = " + NUM, "emd")
vc = L(C["regle"]).split("→ ")[-1].strip()
vs = L(S["regle"]).split("→ ")[-1].strip()
print(f"| valeur de la règle (pt 5) | {vc} | {vs} | l.{C['regle']} ; l.{S['regle']} |")
print()
print("| flux | classe | calme : écart (panne / stale / horsE / nonÉv) | stress : écart (panne / stale / horsE / nonÉv) | J28 |")
print("|---|---|---|---|---|")
classes = {"binance": "sans_horodatage", "coinbase": "place_horodatee", "kraken": "sans_horodatage",
           "okx_ticker": "place_horodatee", "okx_index": "place_horodatee", "bitstamp": "place_horodatee",
           "gemini": "place_horodatee", "bitfinex": "sans_horodatage", "coingecko": "agregateur",
           "defillama": "agregateur", "chainlink": "oracle_chainlink"}
for k in range(11):
    lc, ls = 435453 + k, 435473 + k
    fc, fs = L(lc).split(), L(ls).split()
    assert fc[0] == fs[0]
    print(f"| {fc[0]} | `{classes[fc[0]]}` | {fc[2]} ({fc[3]} / {fc[4]} / {fc[5]} / {fc[6]}) | "
          f"{fs[2]} ({fs[3]} / {fs[4]} / {fs[5]} / {fs[6]}) | l.{lc} ; l.{ls} |")
