"""Bougies (PROPOSITION §4.2 et §6.1 CA-3 ; E-CA-15, E-CA-16) : six lecteurs de formats (SOURCES-HISTORIQUES §3),
normalisation sur la grille des minutes de la fenêtre. Nombres lus en chaînes puis en Decimal, jamais en flottant ;
minute absente ou à volume nul = sans échange. Ligne illisible, colonne absente, temps hors fenêtre ou hors minute,
minute en double : CA/format ; pages et mensuels à mois voisins filtrés à leur fenêtre (DECISION de FORMES-API-1)."""
from __future__ import annotations

import bisect
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


TRONQUEE = "réponse plafonnée ancrée avant le départ : fin de page tronquée"
INCOHERENTE = "demi-page redemandée plafonnée et tronquée"
TROP = "réponse de plus de bougies que de créneaux demandés"
DISCORDE = "couverture double discordante"


def tronquee(ts: list, pas: int, depart: int, derniere: int) -> bool:
    """C-7 : au moins `pas` bougies, une avant `depart`, aucune à `derniere` ou après (fin de réponse coupée)."""
    return len(ts) >= pas and min(ts) < depart and max(ts) < derniere


def instants(format_: str, octets: bytes, illisible=None) -> list:
    """Temps des bougies d'une réponse (C-15) ; illisible : `illisible` s'il est donné, sinon Forme ou erreur levée."""
    try:
        return [t for t, _c, _v in LECTEURS[format_](octets)]
    except (Forme, ValueError, KeyError, IndexError, TypeError, zipfile.BadZipFile):
        if illisible is None:
            raise
        return illisible


def suspecte(format_: str, octets: bytes, pas: int, depart: int, derniere: int) -> bool:
    """C-8 : réponse de page tronquée selon `tronquee` (illisible : non, le chargement la refuse)."""
    try:
        return tronquee([t for t, _c, _v in LECTEURS[format_](octets)], pas, depart, derniere)
    except (Forme, ValueError, KeyError, IndexError, TypeError, zipfile.BadZipFile):
        return False


def serie(format_: str, fichiers: list, fen: dict, place=None, actif=None, fenetres=None, garde=None,
          t0=()) -> dict:
    """{minute : (clôture, active)} des fichiers (octets), active = volume > 0 ; hors minute, ligne illisible, double
    dans un fichier : CA/format (E-CA-16). Sans `fenetres` : hors de [debut ; fin) ou double : CA/format. `fenetres`
    [(a, b)] par fichier (FORMES-API-1, pts 2 et 3) : hors de [a ; b) ∩ [debut ; fin) écartée ; minute de deux
    fichiers aux mêmes clôture et volume (chevauchement) gardée une fois, aux valeurs différentes : CA/format. `garde`
    (mois voisins, C-1 de la G2) : une minute hors fenêtre n'est écartée que dans [garde[0] ; garde[1]).
    Page (a, b, pas, départ, dernière, motif, borne, cœur) : plus de bougies à partir du départ que de créneaux de
    [départ ; borne] : CA/format (C-9). C-13 : une bougie d'un des fichiers dans [min(première bougie, cœur) ;
    dernière] absente de la page : CA/format nommé par le motif (TRONQUEE pour une page `tronquee`, C-7 ; sinon
    DISCORDE ; demi-page : son motif) ; mêmes minutes aux valeurs différentes, un fichier du second découpage (motif
    DISCORDE) en cause : DISCORDE. `t0` (C-15) : (T0 ou None, aucune sonde non vide) ; une bougie au plus tard en
    T0, ou aucune bougie servie ni sondée : CA/avant-historique."""
    out, vals, tous, controles = {}, {}, [], []
    try:
        for k, octets in enumerate(fichiers):
            a, b, *plafond = fenetres[k] if fenetres else (fen["debut"], fen["fin"])
            a, b, vus, ts, motif = max(a, fen["debut"]), min(b, fen["fin"]), set(), [], (plafond or [0] * 4)[3]
            for t, cloture, volume in LECTEURS[format_](octets):
                c, v = Decimal(cloture), Decimal(volume)
                ts.append(t)
                tous.append(t)
                if not (c.is_finite() and v.is_finite() and c >= 0 <= v):
                    raise _refus("nombre non fini ou négatif", place, actif)
                dehors = not a <= t < b
                if t % 60 or (dehors and (not fenetres or garde and not garde[0] <= t < garde[1])):
                    raise _refus("temps hors fenêtre ou hors minute", place, actif)
                if dehors:
                    continue
                if t in vus or (t in vals and not fenetres):
                    raise _refus("minute en double", place, actif)
                if vals.setdefault(t, (c, v, motif))[:2] != (c, v):
                    raise _refus(DISCORDE if DISCORDE in (motif, vals[t][2]) else
                                 "minute en double aux valeurs différentes", place, actif)
                vus.add(t)
                out[t] = (c, v > 0)
            if plafond and sum(t >= plafond[1] for t in ts) > (plafond[4] - plafond[1]) // 60 + 1:   # C-9
                raise _refus(TROP, place, actif)
            if plafond:
                nom = motif if motif != TRONQUEE or tronquee(ts, *plafond[:3]) else DISCORDE
                controles.append((min(ts + [plafond[5]]), plafond[2], set(ts), nom))
        tous.sort()
        if t0 and (t0[1] if not tous else t0[0] is not None and tous[0] <= t0[0]):         # C-15
            raise socle.Refus("CA/avant-historique", "réponse portant la première bougie de l'historique" if tous else
                              "aucune bougie servie", actif, place=place)
        for bas, derniere, recus, nom in controles:       # C-13 : bougie connue absente d'une réponse qui la couvre
            if any(t not in recus for t in tous[bisect.bisect_left(tous, bas):bisect.bisect_right(tous, derniere)]):
                raise _refus(nom, place, actif)
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
    exclus) ; dossier absent ou vide : CA/format. Place paginée : fichiers exactement ceux de socle.pages (sinon
    CA/format), chacun filtré à [départ ; borne + 60) ; mensuels à mois voisins : filtrés à la fenêtre."""
    d, s, fenetres, garde, t0 = os.path.join(bruts, nom, place, actif), prm["series"][place], None, None, ()
    noms = sorted(x for x in os.listdir(d) if not x.endswith(".partiel")) if os.path.isdir(d) else []
    if not noms:
        raise _refus("aucun fichier acquis", place, actif)
    if s["acces"] == "pages":
        plan, c = {}, s["chevauchement"]
        for x, motif, dec in (("page", TRONQUEE, socle.pages(prm, place, fen)),
                              ("double", DISCORDE, socle.doubles(prm, place, fen))):      # C-13 : second découpage
            for a, b, dep, borne in dec:
                plan[f"{x}-{a}.json"] = (dep, borne + 60, s["pas"], dep, b - 60, motif, borne, dep + 60 * c)
                if f"{x}-{a}.1.json" in noms or f"{x}-{a}.2.json" in noms:          # C-8 : demi-pages redemandées
                    plan[f"{x}-{a}.json"] = (dep, borne + 60)
                    for k, (dk, bk, dern) in enumerate(socle.demis(prm, place, dep, borne, b), 1):   # filtre de la demi
                        plan[f"{x}-{a}.{k}.json"] = (max(dk, dep), min(bk, borne) + 60, s["pas"], dk, dern,
                                                     INCOHERENTE if x == "page" else motif, bk, dk + 60 * c)
        if s["couverture"] == 2:
            t0, noms = _sonde(prm, d, place, actif, fen, noms), [x for x in noms if not x.startswith("sonde-")]
        if set(plan) != set(noms):
            raise _refus("pages différentes du découpage de la fenêtre", place, actif)
        fenetres = [plan[x] for x in noms]
    elif s["voisins"]:                                               # garde : mois acquis ± 14 h (C-1 de la G2)
        r, fenetres = socle.rangs_mois(fen, s["voisins"]), [(fen["debut"], fen["fin"])] * len(noms)
        garde = (socle.debut_mois(r.start) - 50400, socle.debut_mois(r.stop) + 50400)
    fichiers = []
    for x in noms:
        with open(os.path.join(d, x), "rb") as f:
            fichiers.append(f.read())
    return serie(s["format"], fichiers, fen, place, actif, fenetres, garde, t0)


def _sonde(prm: dict, d: str, place: str, actif: str, fen: dict, noms: list) -> tuple:
    """C-15 : dichotomie rejouée sur les sondes acquises (fichiers exactement ses sondes, sinon CA/format) ; T0 =
    première bougie de la sonde non vide la plus précoce ; requête de la fenêtre partant moins de pas − ⌊pas/2⌋ + 1
    minutes après T0 : CA/avant-historique. Rend (T0 ou None, aucune sonde non vide)."""
    s, lues = prm["series"][place], {}

    def lire(x):
        try:
            with open(os.path.join(d, f"sonde-{x}.json"), "rb") as f:
                lues[x] = instants(s["format"], f.read())
        except (OSError, Forme, ValueError, KeyError, IndexError, TypeError):
            raise _refus("sonde absente ou illisible", place, actif) from None
        return not lues[x]
    chemin, x = socle.sonde(prm, place, fen, lire)
    if {f"sonde-{y}.json" for y in chemin} != {n for n in noms if n.startswith("sonde-")}:
        raise _refus("sondes différentes de la recherche", place, actif)
    depart = min(p[2] for p in socle.pages(prm, place, fen) + socle.doubles(prm, place, fen))
    if x is not None and depart < min(lues[x]) + 60 * (s["pas"] - s["pas"] // 2 + 1):
        raise socle.Refus("CA/avant-historique", "fenêtre commencée moins d'une page après la première bougie servie",
                          actif, place=place)
    return (None if x is None else min(lues[x]), x is None)


def comptes(prm: dict, place: str, fen: dict, s: dict) -> list:
    """[(début, reçues, attendues)] par page de socle.pages (place paginée), sinon une seule pour la fenêtre : minutes
    de la série s dans [début ; fin) de la page, minutes de cet intervalle (DECISION de FORMES-API-1, pt 5)."""
    plan = socle.pages(prm, place, fen) if prm["series"][place]["acces"] == "pages" else [(fen["debut"], fen["fin"])]
    ts = sorted(s)
    return [(a, bisect.bisect_left(ts, b) - bisect.bisect_left(ts, a), (b - a) // 60) for a, b, *_r in plan]


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
