"""Décodeurs (CB-6 ; E-C-06, E-C-08 ; ADR-0029 l.231 ; PROPOSITION §2.1, §2.4) : un décodeur par (hôte, actif), du
corps d'une lecture `ok` à des relevés {actif, classe, devise, prix, ts_source, extra}. CB-6a : décodeurs BTC des
huit places de S2 repris par copie (`s2-harness/shogen_s2/sources.py` l.84-180) : même lecture des octets (JSON,
nombres en Decimal depuis leur texte), mêmes pièges (Bitfinex position 6, Kraken clé rendue) ; devise par flux (SPECS,
l.239-283), classe de source de S2 (l.305-313), noms d'`analyse.json`. Écarts à S2, nommés : aucun flottant (prix :
texte du Decimal lu, comme `expected.json` de S2 ; instant de la source en microsecondes entières, S2 en secondes
flottantes ; extra en chaînes) ; finitude (prix fini, > 0, exposant dans les bornes de CONTEXTE ; instant de 0 à
2^53 µs exclu, FORMAT §9.2) ; ISO lu par un motif, `fromisoformat` changeant de 3.10 à 3.13 ; `decoder` ne lève
jamais (S2 laissait sortir AttributeError) ; sous CONTEXTE, recopie du contexte nommé de S2 (r1.py l.62-68 ; Q-C-14)."""
import datetime
import decimal
import json
import re
from decimal import Decimal

CONTEXTE = decimal.Context(prec=50, rounding=decimal.ROUND_HALF_EVEN, Emin=-999999, Emax=999999, capitals=1, clamp=0,
                           flags=[], traps=[decimal.InvalidOperation, decimal.DivisionByZero, decimal.Overflow])
S = 1_000_000                                                       # microsecondes par seconde
ISO = re.compile("([0-9]{4})-([0-9]{2})-([0-9]{2})T([0-9]{2}):([0-9]{2}):([0-9]{2})([.][0-9]+)?"
                 "(Z|[+-][0-9]{2}:[0-9]{2})?")                    # date, heure, fraction, décalage (RFC 3339 §5.6)
EPOQUE = datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)


def _iso_us(texte):
    """Instant ISO-8601 en microsecondes : fraction tronquée à la microseconde comme en S2 (`_iso_to_epoch`, l.93-107),
    instant sans décalage lu en UTC."""
    m = ISO.fullmatch(texte.strip())
    a, mo, j, h, mi, s = map(int, m.groups()[:6])
    tz = m[8] or "Z"
    decalage = datetime.timedelta(0) if tz == "Z" else int(tz[0] + "1") * datetime.timedelta(hours=int(tz[1:3]),
                                                                                              minutes=int(tz[4:]))
    t = datetime.datetime(a, mo, j, h, mi, s, int(((m[7] or ".")[1:] + "00000")[:6]), datetime.timezone(decalage))
    return (t - EPOQUE) // datetime.timedelta(microseconds=1)


def _okx(champ):
    def lire(j):
        if str(j.get("code")) != "0":
            raise ValueError(f"okx : code {j.get('code')}")
        d = j["data"][0]
        return d[champ], int(d["ts"]) * 1000, {}
    return lire


def _kraken(j):
    if j.get("error"):                                              # erreurs dans une liste, pas dans le statut
        raise ValueError("kraken : erreur")
    (paire,) = j["result"].values()                                 # une paire demandée : une clé rendue (XXBTZUSD)
    return paire["c"][0], None, {}


def _bitfinex(j):
    if not isinstance(j, list) or len(j) < 10:                      # LAST_PRICE en position 6 (11 champs rendus)
        raise ValueError("bitfinex : forme")
    return j[6], None, {}


DECODEURS = {      # nom : (actif, devise, classe de source, décodeur du JSON lu) ; S2 : SPECS, SIGMA_CLASS_OF_FLUX
    "binance_btc": ("BTC", "USDT", "sans_horodatage", lambda j: (j["price"], None, {})),
    "coinbase_btc": ("BTC", "USD", "place_horodatee", lambda j: (j["price"], _iso_us(str(j["time"])), {})),
    "kraken_btc": ("BTC", "USD", "sans_horodatage", _kraken),
    "okx_ticker_btc": ("BTC", "USDT", "place_horodatee", _okx("last")),
    "okx_index_btc": ("BTC", "USD", "place_horodatee", _okx("idxPx")),
    "bitstamp_btc": ("BTC", "USD", "place_horodatee", lambda j: (j["last"], int(j["timestamp"]) * S, {})),
    "gemini_btc": ("BTC", "USD", "place_horodatee", lambda j: (j["last"], int(j["volume"]["timestamp"]) * 1000, {})),
    "bitfinex_btc": ("BTC", "USD", "sans_horodatage", _bitfinex),
}


def _releve(actif, devise, classe, prix, ts, extra):
    """Relevé exact : prix lu en chaîne ou en Decimal (jamais un flottant), fini, > 0, exposant dans les bornes de
    CONTEXTE ; instant entier de 0 à 2^53 µs exclu, ou None ; extra de chaînes. Tout autre cas lève."""
    if type(prix) not in (str, Decimal) or type(ts) not in (int, type(None)) or type(extra) is not dict:
        raise TypeError("relevé : types")
    p = Decimal(prix)
    if not (p.is_finite() and p > 0 and CONTEXTE.Emin <= p.adjusted() <= CONTEXTE.Emax):
        raise ValueError("relevé : prix non fini, nul, négatif ou hors bornes")
    if ts is not None and not 0 <= ts < 1 << 53 or not all(type(k) is str is type(v) for k, v in extra.items()):
        raise ValueError("relevé : instant ou extra")
    return {"actif": actif, "classe": classe, "devise": devise, "extra": extra, "prix": str(p), "ts_source": ts}


def decoder(nom, octets):
    """(statut, valeurs) : ("ok", relevés) ou ("panne_decode", None) ; ne lève jamais (E-C-03, E-C-06)."""
    try:
        with decimal.localcontext(CONTEXTE):
            actif, devise, classe, lire = DECODEURS[nom]
            return "ok", [_releve(actif, devise, classe, *lire(json.loads(octets, parse_float=Decimal,
                                                                          parse_int=Decimal)))]
    except Exception:                                               # attrape-tout : un indécodable est une panne
        return "panne_decode", None
