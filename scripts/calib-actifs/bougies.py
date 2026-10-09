"""Bougies (PROPOSITION §4.2 et §6.1 CA-3 ; E-CA-15, E-CA-16) : six lecteurs de formats (SOURCES-HISTORIQUES §3),
normalisation sur la grille des minutes de la fenêtre. Nombres lus en chaînes puis en Decimal, jamais en flottant ;
minute absente ou à volume nul = sans échange. Ligne illisible, colonne absente, temps hors fenêtre ou hors minute,
minute en double : CA/format."""
from __future__ import annotations

import io
import json
import os
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


def derniers(s: dict, fen: dict) -> tuple:
    """(c, a) sur la grille des minutes de la fenêtre (§4.2) : c[i] clôture de la dernière minute active au plus tard
    en t_i, a[i] minutes écoulées depuis elle (0 si t_i est active) ; None avant la première minute active de la
    fenêtre (pas de préchauffe)."""
    c, a, cour, age = [], [], None, None
    for t in socle.minutes(fen):
        x = s.get(t)
        if x is not None and x[1]:
            cour, age = x[0], 0
        elif age is not None:
            age += 1
        c.append(cour)
        a.append(age)
    return c, a


def charger(prm: dict, bruts: str, nom: str, place: str, actif: str, fen: dict) -> dict:
    """Série d'une (place, actif) depuis <bruts>/<nom>/<place>/<actif>/ (fichiers de l'acquisition, triés, .partiel
    exclus) ; dossier absent ou vide : CA/format."""
    d = os.path.join(bruts, nom, place, actif)
    noms = sorted(x for x in os.listdir(d) if not x.endswith(".partiel")) if os.path.isdir(d) else []
    if not noms:
        raise _refus("aucun fichier acquis", place, actif)
    fichiers = []
    for x in noms:
        with open(os.path.join(d, x), "rb") as f:
            fichiers.append(f.read())
    return serie(prm["series"][place]["format"], fichiers, fen, place, actif)


def oracle_sh(prm: dict, series: dict) -> list:
    """E-CA-15, avant toute valeur : minutes actives de la semaine de SH §4 recomptées sur les séries {(actif, place) :
    série}, par place et à au moins 4, 3 et 2 places actives ; un écart : CA/oracle-sh ; un contrôle dont une place
    manque à la lecture : « non applicable », imprimé. Rend les lignes du compte rendu."""
    o, lignes = prm["oracle_sh"], []
    semaine = socle.minutes(o)

    def actives(a, p):
        return {t for t in semaine if series[a, p].get(t, (0, False))[1]}
    for a, p, n in o["actives"]:
        if (a, p) not in series:
            lignes.append(f"oracle de SH §4 : {a} {p} non applicable (place hors lecture)")
        elif len(actives(a, p)) != n:
            raise socle.Refus("CA/oracle-sh", "minutes actives différentes de SH §4", a, place=p)
    for a, places, comptes in o["concurrences"]:
        if any((a, p) not in series for p in places):
            lignes.append(f"oracle de SH §4 : {a} ({', '.join(places)}) non applicable (place hors lecture)")
            continue
        ens = [actives(a, p) for p in places]
        if [sum(sum(t in e for e in ens) >= k for t in semaine) for k in (4, 3, 2)] != comptes:
            raise socle.Refus("CA/oracle-sh", "concurrence différente de SH §4 (" + ", ".join(places) + ")", a)
    return lignes + [f"oracle de SH §4 : {len(o['actives'])} comptes par place et {len(o['concurrences'])} "
                     "concurrences contrôlés, égaux ou non applicables"]

