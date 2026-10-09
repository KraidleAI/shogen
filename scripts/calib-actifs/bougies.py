"""Bougies (PROPOSITION §4.2 et §6.1 CA-3 ; E-CA-15, E-CA-16) : six lecteurs de formats (SOURCES-HISTORIQUES §3),
normalisation sur la grille des minutes de la fenêtre. Nombres lus en chaînes puis en Decimal, jamais en flottant ;
minute absente ou à volume nul = sans échange. Ligne illisible, colonne absente, temps hors fenêtre ou hors minute,
minute en double : CA/format."""
from __future__ import annotations

import io
import json
import zipfile
from decimal import Decimal, InvalidOperation

import socle

NL = chr(10)


class Forme(ValueError):
    """Forme d'un fichier contraire à son format ; nommée par serie avec la place et l'actif."""


def _refus(motif, place=None, actif=None):
    return socle.Refus("CA/format", motif, actif, place=place)


def _zip(octets: bytes) -> str:
    """Seul membre d'un mensuel (Binance, OKX), en texte."""
    with zipfile.ZipFile(io.BytesIO(octets)) as z:
        if len(z.namelist()) != 1:
            raise Forme("archive mensuelle à plus d'un membre")
        return z.read(z.namelist()[0]).decode("ascii")


def _lignes(texte: str) -> list:
    return [x.rstrip(chr(13)).split(",") for x in texte.split(NL) if x.strip()]


def _binance(octets):
    """CSV sans en-tête, 12 colonnes ; temps en microsecondes (16 chiffres, depuis 2025) ou en millisecondes (13) ;
    clôture en colonne 4, volume en colonne 5 (T-CA-FMT-1)."""
    for x in _lignes(_zip(octets)):
        if len(x) != 12 or len(x[0]) not in (13, 16):
            raise Forme("ligne de Binance hors forme")
        unite = 10 ** 6 if len(x[0]) == 16 else 1000
        yield (int(x[0]) // unite if int(x[0]) % unite == 0 else -1), x[4], x[5]


def _okx(octets):
    """CSV avec en-tête (instrument_name, …, close, vol, …, open_time, confirm), temps en millisecondes."""
    t = _lignes(_zip(octets))
    i, c, v = (t[0].index(n) if n in t[0] else None for n in ("open_time", "close", "vol"))
    if None in (i, c, v):
        raise Forme("en-tête d'OKX sans open_time, close ou vol")
    for x in t[1:]:
        yield (int(x[i]) // 1000 if int(x[i]) % 1000 == 0 else -1), x[c], x[v]


def _kraken(octets):
    """CSV sans en-tête « timestamp, open, high, low, close, volume, trades », en secondes."""
    for x in _lignes(octets.decode("ascii")):
        if len(x) != 7:
            raise Forme("ligne de Kraken hors forme")
        yield int(x[0]), x[4], x[5]


def _json(octets):
    return json.loads(octets.decode("utf-8"), parse_float=str, parse_int=str)


def _coinbase(octets):
    """JSON [time, low, high, open, close, volume], en secondes : clôture en colonne 4 (T-CA-FMT-2)."""
    for x in _json(octets):
        yield int(x[0]), x[4], x[5]


def _bitstamp(octets):
    """JSON {data: {ohlc: [{timestamp, open, high, low, close, volume}]}}, chaînes, secondes ; minutes reportées à
    volume nul (T-CA-FMT-3)."""
    for x in _json(octets)["data"]["ohlc"]:
        yield int(x["timestamp"]), x["close"], x["volume"]


def _bitfinex(octets):
    """JSON [MTS, OPEN, CLOSE, HIGH, LOW, VOLUME], en millisecondes : clôture en colonne 2 (T-CA-FMT-2)."""
    for x in _json(octets):
        yield (int(x[0]) // 1000 if int(x[0]) % 1000 == 0 else -1), x[2], x[5]


LECTEURS = {"binance": _binance, "bitfinex": _bitfinex, "bitstamp": _bitstamp, "coinbase": _coinbase,
            "kraken": _kraken, "okx": _okx}


def serie(format_: str, fichiers: list, fen: dict, place=None, actif=None) -> dict:
    """{minute : (clôture, active)} des fichiers (octets) d'une (place, actif), active = volume > 0 ; temps hors de la
    fenêtre [debut ; fin) ou hors minute, minute en double, ligne illisible : CA/format (E-CA-16)."""
    out = {}
    try:
        for octets in fichiers:
            for t, cloture, volume in LECTEURS[format_](octets):
                c, v = Decimal(cloture), Decimal(volume)
                if not (c.is_finite() and v.is_finite() and c >= 0 <= v):
                    raise _refus("nombre non fini ou négatif", place, actif)
                if t % 60 or not fen["debut"] <= t < fen["fin"]:
                    raise _refus("temps hors fenêtre ou hors minute", place, actif)
                if t in out:
                    raise _refus("minute en double", place, actif)
                out[t] = (c, v > 0)
    except Forme as e:
        raise _refus(str(e), place, actif) from None
    except (ValueError, KeyError, IndexError, TypeError, InvalidOperation, zipfile.BadZipFile) as e:
        raise _refus(f"ligne illisible ({type(e).__name__})", place, actif) from None
    return out
