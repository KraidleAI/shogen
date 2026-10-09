"""Séries synthétiques déterministes (aucun historique réel) : prix autour de 100 à ±0,05, minutes sans échange à
volume nul, pour chaque (actif, place) de la lecture retenue ; valeurs de BTC synthétiques, jamais celles de
tau_sigma.txt. Fenêtre courte à cheval sur le vendredi et le samedi (calme puis stress)."""
import io
import json
import os
import zipfile
from decimal import Decimal

import socle

NL = chr(10)
FEN = {"debut": 1775260500, "fin": 1775261100}                  # 2026-04-03 23:55 à 2026-04-04 00:05 UTC
BTC = {("tau", "agregateur"): Decimal("0.0265"), ("tau", "place_horodatee"): Decimal("0.0045"),
       ("tau", "sans_horodatage"): Decimal("0.0050"), ("sigma", "agregateur"): Decimal(900),
       ("sigma", "place_horodatee"): Decimal(90)}
BTC_PH = BTC | {("tau", "place_horodatee"): Decimal("0.0050"), ("tau", "sans_horodatage"): Decimal("0.0045")}  # C-1


def serie(j: int, fen=FEN) -> dict:
    """{minute : (clôture, active)} de la place de rang j : active sauf une minute sur cinq (décalée par j)."""
    return {t: (Decimal(100) + Decimal((i * (j + 3)) % 11 - 5) / 100, (i + j) % 5 != 0 or i == 0)
            for i, t in enumerate(socle.minutes(fen))}


def series(prm: dict, actif: str, fen=FEN) -> dict:
    return {p: serie(j, fen) for j, p in enumerate(socle.lecture(prm)["places"][actif])}


def _zip(texte: str) -> bytes:
    b = io.BytesIO()
    with zipfile.ZipFile(b, "w") as z:
        z.writestr("m.csv", texte)
    return b.getvalue()


def octets(format_: str, s: dict) -> bytes:
    """Fichier synthétique au format de la place : minutes sans échange absentes (Kraken, Coinbase, Bitfinex) ou à
    volume nul (Binance, OKX, Bitstamp), comme les sources (SOURCES-HISTORIQUES §3)."""
    rangs = sorted(s.items())
    act = [(t, c) for t, (c, a) in rangs if a]
    entete = "instrument_name,open,high,low,close,vol,vol_ccy,vol_quote,open_time,confirm" + NL
    lignes = {"binance": lambda: _zip("".join(f"{t * 10 ** 6},1,1,1,{c},{int(a)},0,0,0,0,0,0{NL}"
                                              for t, (c, a) in rangs)),
              "okx": lambda: _zip(entete + "".join(f"X,1,1,1,{c},{int(a)},0,0,{t * 1000},1{NL}"
                                                   for t, (c, a) in rangs)),
              "kraken": lambda: "".join(f"{t},1,1,1,{c},1,1{NL}" for t, c in act).encode(),
              "coinbase": lambda: json.dumps([[t, 1, 1, 1, str(c), 1] for t, c in act]).encode(),
              "bitstamp": lambda: json.dumps({"data": {"ohlc": [
                  {"timestamp": str(t), "close": str(c), "volume": str(int(a))} for t, (c, a) in rangs]}}).encode(),
              "bitfinex": lambda: json.dumps([[t * 1000, 1, str(c), 1, 1, 1] for t, c in act]).encode()}
    return lignes[format_]()


def ecrire_bruts(prm: dict, bruts: str, nom: str, fen=FEN) -> None:
    """<bruts>/<nom>/<place>/<actif>/f.dat de chaque (actif, place) de la lecture retenue (fenêtre descriptive : sans
    ses places exclues)."""
    for actif in socle.ACTIFS:
        for p, s in series(prm, actif, fen).items():
            if nom == "principale" or p not in prm["fenetre_descriptive"]["sans"]:
                os.makedirs(os.path.join(bruts, nom, p, actif), exist_ok=True)
                with open(os.path.join(bruts, nom, p, actif, "f.dat"), "wb") as f:
                    f.write(octets(prm["series"][p]["format"], s))
