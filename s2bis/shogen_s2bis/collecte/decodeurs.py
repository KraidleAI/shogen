"""Décodeurs (CB-6 ; E-C-06, E-C-08 ; ADR-0029 l.231 ; PROPOSITION §2.1, §2.4) : un décodeur par (hôte, actif), du
corps d'une lecture `ok` à des relevés {actif, classe, devise, prix, ts_source, extra}. Décodeurs BTC de S2 repris
par copie (`s2-harness/shogen_s2/sources.py` l.84-218 ; places en CB-6a, agrégateurs et Chainlink en CB-6b ; Pyth
retiré, ADR-0029 l.167) : même lecture des octets (JSON, nombres en Decimal depuis leur texte), mêmes pièges (Bitfinex
position 6, Kraken clé rendue, Chainlink mots 2 et 4) ; devise par flux (SPECS, l.239-283), classe de source de S2
(l.305-313), noms d'`analyse.json`. Écarts à S2, nommés : aucun flottant (prix :
texte du Decimal lu, comme `expected.json` de S2 ; instant de la source en microsecondes entières, S2 en secondes
flottantes ; extra en chaînes) ; finitude (prix fini, > 0, exposant dans les bornes de CONTEXTE ; instant de 0 à
2^53 µs exclu, FORMAT §9.2) ; ISO lu par un motif, `fromisoformat` changeant de 3.10 à 3.13 ; mots de Chainlink en
hexadécimal strict, prix construit exactement (mantisse, exposant -8), sans division ; `decoder` ne lève jamais (S2
laissait sortir AttributeError) ; sous CONTEXTE, recopie du contexte nommé de S2 (r1.py l.62-68 ; Q-C-14). CB-6c
(SHOGEN-S2BIS-ECRIVAIN-REFUS-ARRET-1 ; FORMAT §9.1) : des valeurs que l'écrivain refuserait (`journal.canonique`) ou
de plus de VALEURS octets canoniques ne sont jamais rendues : la lecture est `panne_decode` ; `appliquer` décode le
corps d'une lecture `ok` dans le fil de la lecture.
CB-7a (SHOGEN-S2BIS-DECODEURS-TYPES-1) : chaque conteneur lu est de la sorte attendue (`_champ`), écart à S2 qui
indexait une chaîne comme une liste.
CB-7b (E-C-06 ; G0 de CALIB-ACTIFS, PROPOSITION §2.2) : un décodeur par (hôte, actif) pour ETH, USDC et USDT des places,
paires lues sur pièce (`docs/adr-0029/g0-calib/PAIRES-ET-TEMOIN.md`, tableau 1.1), classe de S2 pour l'hôte, devise de
la paire ; l'instrument que la réponse rend (Binance `symbol`, Kraken clé, OKX `instId`) est exigé, sauf pour BTC (S2
ne le lisait pas) ; aucun décodeur pour une paire non servie (Coinbase USDC/USD, OKX ETH/USD et USDC/USD).
CB-7c : ETH coté en USDT chez binance et okx (Q-CA-01 (a) du G0 de CALIB-ACTIFS)."""
import datetime
import decimal
import json
import re
from decimal import Decimal

from shogen_s2bis.collecte import journal
from shogen_s2bis.collecte.lecture import Lecture

CONTEXTE = decimal.Context(prec=50, rounding=decimal.ROUND_HALF_EVEN, Emin=-999999, Emax=999999, capitals=1, clamp=0,
                           flags=[], traps=[decimal.InvalidOperation, decimal.DivisionByZero, decimal.Overflow])
S = 1_000_000                                                       # microsecondes par seconde
VALEURS = 1 << 21                   # octets canoniques des valeurs au plus, saut de ligne compris (FORMAT §9.1)
ISO = re.compile("([0-9]{4})-([0-9]{2})-([0-9]{2})T([0-9]{2}):([0-9]{2}):([0-9]{2})([.][0-9]+)?"
                 "(Z|[+-][0-9]{2}:[0-9]{2})?")                    # date, heure, fraction, décalage (RFC 3339 §5.6)
EPOQUE = datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)
MOTS = re.compile("0x[0-9a-fA-F]{320}")                             # latestRoundData : cinq mots de 32 octets
CHIFFRES, TEXTE = 16, 4300                      # bornes de `_entier` : instant sous 10^16 ; texte de int()


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


def _entier(x):
    """int() de S2 sur un instant, borné avant la conversion (C-1 de la G2 de P2A) : int() d'un Decimal coûte un
    temps quadratique en son exposant et tient le GIL (1E+200000 : 0,4 s ; 1E+1000000 : 10 s, mesurés), int() d'un
    texte aussi si la limite de l'interpréteur est levée (PYTHONINTMAXSTRDIGITS=0 ; 10^6 chiffres : 3,8 s sous 3.10).
    Refus : Decimal fini d'exposant ajusté ≥ CHIFFRES (2^53 = 9007199254740992 < 10^16 : un tel instant, en secondes
    ou en millisecondes, dépasse 2^53 µs, FORMAT §9.2 ; aucun instant non nul recevable n'est refusé, et 0E+16,
    l'instant 0 écrit avec un exposant, sans objet pour une source, l'est : DT6-b, O-A2 du contre-contrôle de P2A) ;
    texte de plus de TEXTE caractères (limite par défaut de int(), 4 300 chiffres de 3.10.20 à 3.13.14, mesurée), quelle
    que soit la configuration de l'interpréteur. Borne figée par un test (DT6-b, DECODEURS-BORNE-TEST-1)."""
    if type(x) is Decimal and x.is_finite() and x.adjusted() >= CHIFFRES or type(x) is str and len(x) > TEXTE:
        raise ValueError("instant : hors bornes avant int()")
    return int(x)


def _champ(j, *chemin):
    """j[c1][c2]… : une clé de texte lit un objet JSON, un indice entier une liste ; toute autre sorte lève
    (SHOGEN-S2BIS-DECODEURS-TYPES-1, O-1 de la G2 de P2A : Kraken `c` en chaîne rendait son premier caractère)."""
    for c in chemin:
        if type(j) is not (list if type(c) is int else dict):
            raise TypeError(f"{c!r} : conteneur {type(j).__name__}")
        j = j[c]
    return j


def _okx(champ, inst=None):
    """OKX : code "0", premier élément de `data` ; `instId` rendu égal à `inst` (None pour BTC, comme S2)."""
    def lire(j):
        if str(_champ(j, "code")) != "0":
            raise ValueError(f"okx : code {j['code']}")
        d = _champ(j, "data", 0)
        if inst is not None and _champ(d, "instId") != inst:
            raise ValueError("okx : instrument")
        return _champ(d, champ), _entier(_champ(d, "ts")) * 1000, {}
    return lire


def _kraken(cle=None):
    """Kraken : erreurs dans une liste, pas dans le statut ; une paire demandée, une clé rendue (XXBTZUSD ; XETHZUSD,
    USDCUSD, USDTZUSD : pièce, tableau 1.2), égale à `cle` (None pour BTC, comme S2)."""
    def lire(j):
        if type(j) is not dict or j.get("error"):                   # liste d'erreurs absente admise (S2)
            raise ValueError("kraken : erreur")
        ((k, paire),) = _champ(j, "result").items()
        if cle is not None and k != cle:
            raise ValueError("kraken : clé")
        return _champ(paire, "c", 0), None, {}
    return lire


def _binance(symbole=None):
    def lire(j):
        if symbole is not None and _champ(j, "symbol") != symbole:
            raise ValueError("binance : symbole")
        return _champ(j, "price"), None, {}
    return lire


def _coinbase(j):
    return _champ(j, "price"), _iso_us(str(_champ(j, "time"))), {}


def _bitstamp(j):
    return _champ(j, "last"), _entier(_champ(j, "timestamp")) * S, {}


def _gemini(j):
    return _champ(j, "last"), _entier(_champ(j, "volume", "timestamp")) * 1000, {}


def _bitfinex(j):
    if type(j) is not list or len(j) < 10:                          # LAST_PRICE en position 6 (11 champs rendus)
        raise ValueError("bitfinex : forme")
    return j[6], None, {}


def _coingecko(c):
    return _champ(c, "usd"), _entier(_champ(c, "last_updated_at")) * S, {}


def _defillama(c):
    return _champ(c, "price"), _entier(_champ(c, "timestamp")) * S, (
        {"confidence": str(c["confidence"])} if "confidence" in c else {})


def _chainlink(j):
    h = _champ(j, "result")
    if type(h) is not str or not MOTS.fullmatch(h):
        raise ValueError("chainlink : cinq mots attendus")
    mots = [int(h[2 + 64 * i:66 + 64 * i], 16) for i in range(5)]
    reponse = mots[1] - (1 << 256 if mots[1] >= 1 << 255 else 0)   # answer : int256, flux BTC/USD à 8 décimales
    return Decimal(f"{reponse}E-8"), mots[3] * S, {"round_id": str(mots[0])}


H, P = "place_horodatee", "sans_horodatage"
DECODEURS = {      # nom : (actif, devise, classe de source, décodeur du JSON lu) ; S2 : SPECS, SIGMA_CLASS_OF_FLUX
    "binance_btc": ("BTC", "USDT", P, _binance()),
    "coinbase_btc": ("BTC", "USD", H, _coinbase),
    "kraken_btc": ("BTC", "USD", P, _kraken()),
    "okx_ticker_btc": ("BTC", "USDT", H, _okx("last")),
    "okx_index_btc": ("BTC", "USD", H, _okx("idxPx")),
    "bitstamp_btc": ("BTC", "USD", H, _bitstamp),
    "gemini_btc": ("BTC", "USD", H, _gemini),
    "bitfinex_btc": ("BTC", "USD", P, _bitfinex),
    "coingecko_btc": ("BTC", "USD", "agregateur", lambda j: _coingecko(_champ(j, "bitcoin"))),
    "defillama_btc": ("BTC", "USD", "agregateur", lambda j: _defillama(_champ(j, "coins", "coingecko:bitcoin"))),
    "chainlink_btc": ("BTC", "USD", "oracle_chainlink", _chainlink),
    # CB-7b : places, paires de la pièce (tableau 1.1) et formes de la PROPOSITION de CALIB-ACTIFS (§2.2)
    "binance_usdc": ("USDC", "USD", P, _binance("USDCUSD")),
    "binance_usdt": ("USDT", "USD", P, _binance("USDTUSD")),
    "coinbase_eth": ("ETH", "USD", H, _coinbase),
    "coinbase_usdt": ("USDT", "USD", H, _coinbase),
    "kraken_eth": ("ETH", "USD", P, _kraken("XETHZUSD")),
    "kraken_usdc": ("USDC", "USD", P, _kraken("USDCUSD")),
    "kraken_usdt": ("USDT", "USD", P, _kraken("USDTZUSD")),
    "okx_ticker_usdt": ("USDT", "USD", H, _okx("last", "USDT-USD")),
    **{f"{h}_{a.lower()}": (a, "USD", H, lire) for h, lire in (("bitstamp", _bitstamp), ("gemini", _gemini))
       for a in ("ETH", "USDC", "USDT")},
    # CB-7c : ETH coté en USDT chez binance et okx, comme BTC (Q-CA-01 (a) du G0 de CALIB-ACTIFS ; ADR-0029 l.98)
    "binance_eth": ("ETH", "USDT", P, _binance("ETHUSDT")),
    "okx_ticker_eth": ("ETH", "USDT", H, _okx("last", "ETH-USDT")),
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
            valeurs = [_releve(actif, devise, classe, *lire(json.loads(octets, parse_float=Decimal,
                                                                       parse_int=Decimal)))]
        if len(journal.canonique(valeurs)) <= VALEURS:              # règles de l'écrivain, avant lui (REFUS-ARRET-1)
            return "ok", valeurs
    except Exception:                                               # attrape-tout : un indécodable est une panne
        pass
    return "panne_decode", None


def appliquer(nom, lu):
    """La lecture `lu` décodée par le décodeur `nom` si elle est `ok` (valeurs, ou `panne_decode`), sinon `lu`."""
    if lu.statut != "ok":
        return lu
    statut, valeurs = decoder(nom, lu.octets)
    return Lecture(statut, lu.depart, lu.fin, lu.phases, lu.adresse, code=lu.code, octets=lu.octets, valeurs=valeurs)
