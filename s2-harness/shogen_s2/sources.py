"""Les douze flux de prix et leurs décodeurs — un décodeur par flux.

Conception : docs/10-mesures-pilotes-design.md §3.1 (table re-mesurée le
2026-08-05, 11 sources / 12 flux ; CryptoCompare 401 → écartée) et §3.2
(graphe d'amonts : 7 places = nœuds, agrégateurs/oracles = fonctions).

Chaque décodeur porte le piège que la re-vérification aveugle (V2, 10 §3.1)
a constaté sur pièce, et le cite :
  - Bitfinex : LAST_PRICE en POSITION 6, jamais « dernier élément » (le v2
    a renvoyé 11 champs là où le schéma en documente 10 — 10 §3.1).
  - Kraken : indexer par la CLÉ RETOURNÉE `XXBTZUSD`, pas par `XBTUSD`.
  - Pyth : prix = mantisse · 10^expo (10 §3.1).
  - Chainlink : `answer` = 2ᵉ mot de 32 octets ; `updatedAt` = 4ᵉ (10 §3.1).

Zéro dépendance externe (urllib + décodage hex à la main) — instrument
jetable (10 §1). `A(typer-correctness)` (08) : ces décodeurs SONT les
typeurs ; ils sont testés (test_sources.py), jamais prouvés, et un
indécodable devient une panne, jamais une valeur inventée.
"""

from __future__ import annotations

import json
import socket
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from typing import Callable, Optional

from .model import Currency, DecodeError, Reading, Status

# ── Réseau ────────────────────────────────────────────────────────────────

# UA navigateur non-credential : la re-mesure (10 §3.1) a constaté qu'il ne
# débloque aucun 403 — les statuts « sans clé » tiennent tels quels. Aucune
# clé, aucun token, aucun cookie n'est jamais envoyé (décision « strictement
# sans clé », 10 §9.3).
_UA = "Mozilla/5.0 (Shogen-S2-harness; +https://github.com/KraidleAI/shogen)"
_DEFAULT_TIMEOUT = 10.0


class TransportError(Exception):
    """Aucune réponse HTTP (timeout, DNS, reset) — distincte d'un statut != 200."""


def _http_get(url: str, timeout: float) -> tuple[int, bytes]:
    req = urllib.request.Request(
        url, headers={"User-Agent": _UA, "Accept": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as e:  # réponse reçue, statut d'erreur (ex. 401)
        return e.code, e.read()
    except (urllib.error.URLError, socket.timeout, TimeoutError) as e:
        raise TransportError(str(e)) from e


def _http_post_json(url: str, body: dict, timeout: float) -> tuple[int, bytes]:
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        method="POST",
        headers={
            "User-Agent": _UA,
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()
    except (urllib.error.URLError, socket.timeout, TimeoutError) as e:
        raise TransportError(str(e)) from e


# ── Aides de décodage ─────────────────────────────────────────────────────

def _loads(raw: bytes):
    """JSON en préservant l'exactitude : tout nombre devient Decimal depuis
    sa forme textuelle (recalculable à l'octet, ADR-0003)."""
    try:
        return json.loads(raw, parse_float=Decimal, parse_int=Decimal)
    except (json.JSONDecodeError, ValueError) as e:
        raise DecodeError(f"JSON illisible: {e}") from e


def _iso_to_epoch(s: str) -> float:
    """ISO-8601 → epoch s. Tolère 'Z' et une fraction à précision variable
    (Coinbase émet des ns) en tronquant à la microseconde. Un horodatage
    naïf (sans offset) est lu en UTC."""
    s = s.strip().replace("Z", "+00:00")
    if "." in s:
        head, frac = s.split(".", 1)
        i = 0
        while i < len(frac) and frac[i].isdigit():  # chiffres de la fraction
            i += 1
        s = f"{head}.{frac[:min(i, 6)]}{frac[i:]}"   # garde l'offset intact
    dt = datetime.fromisoformat(s)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.timestamp()


def _u256(word_hex: str) -> int:
    return int(word_hex, 16)


def _i256(word_hex: str) -> int:
    """int256 signé (complément à deux sur 256 bits)."""
    v = int(word_hex, 16)
    if v >= 1 << 255:
        v -= 1 << 256
    return v


# ── Décodeurs (raw bytes → (price, source_ts, extra)) ─────────────────────
# Chacun lève DecodeError si la forme n'est pas EXACTEMENT celle attendue.

def _d_binance(raw):
    j = _loads(raw)
    return Decimal(str(j["price"])), None, {}


def _d_coinbase(raw):
    j = _loads(raw)
    return Decimal(str(j["price"])), _iso_to_epoch(str(j["time"])), {}


def _d_kraken(raw):
    j = _loads(raw)
    if j.get("error"):  # Kraken porte ses erreurs dans une liste, pas le statut
        raise DecodeError(f"kraken error: {j['error']}")
    result = j["result"]
    if len(result) != 1:  # une paire demandée, une clé attendue
        raise DecodeError(f"kraken result keys inattendus: {list(result)}")
    (pair_data,) = result.values()          # clé retournée XXBTZUSD, pas XBTUSD
    return Decimal(str(pair_data["c"][0])), None, {}  # c[0] = dernier trade


def _d_okx_ticker(raw):
    j = _loads(raw)
    if str(j.get("code")) != "0":
        raise DecodeError(f"okx code={j.get('code')}")
    d = j["data"][0]
    return Decimal(str(d["last"])), int(d["ts"]) / 1000.0, {}


def _d_okx_index(raw):
    j = _loads(raw)
    if str(j.get("code")) != "0":
        raise DecodeError(f"okx code={j.get('code')}")
    d = j["data"][0]
    return Decimal(str(d["idxPx"])), int(d["ts"]) / 1000.0, {}


def _d_bitstamp(raw):
    j = _loads(raw)
    return Decimal(str(j["last"])), float(int(j["timestamp"])), {}


def _d_gemini(raw):
    j = _loads(raw)
    ts = int(j["volume"]["timestamp"]) / 1000.0
    return Decimal(str(j["last"])), ts, {}


def _d_bitfinex(raw):
    arr = _loads(raw)
    # Piège re-établi (10 §3.1) : le v2 a renvoyé 11 champs (schéma : 10) ;
    # LAST_PRICE est la POSITION 6, jamais le dernier élément. On décode par
    # position fixe ou c'est une panne.
    if not isinstance(arr, list) or len(arr) < 10:
        raise DecodeError(f"bitfinex forme inattendue (len={len(arr)})")
    return Decimal(str(arr[6])), None, {}


def _d_coingecko(raw):
    j = _loads(raw)
    b = j["bitcoin"]
    return Decimal(str(b["usd"])), float(int(b["last_updated_at"])), {}


def _d_defillama(raw):
    j = _loads(raw)
    c = j["coins"]["coingecko:bitcoin"]
    extra = {"confidence": str(c["confidence"])} if "confidence" in c else {}
    return Decimal(str(c["price"])), float(int(c["timestamp"])), extra


def _d_pyth(raw):
    j = _loads(raw)
    p = j["parsed"][0]["price"]
    expo = int(p["expo"])
    price = Decimal(str(p["price"])) * (Decimal(10) ** expo)
    conf = Decimal(str(p["conf"])) * (Decimal(10) ** expo)
    return price, float(int(p["publish_time"])), {"conf": str(conf)}


def _d_chainlink(raw):
    j = _loads(raw)
    result = str(j["result"])
    if not result.startswith("0x"):
        raise DecodeError(f"chainlink result non-hex: {result[:16]}")
    h = result[2:]
    if len(h) != 5 * 64:  # latestRoundData renvoie 5 mots de 32 octets
        raise DecodeError(f"chainlink attend 5 mots, reçu {len(h)//64}")
    words = [h[i * 64:(i + 1) * 64] for i in range(5)]
    answer = _i256(words[1])                       # answer = 2ᵉ mot (int256)
    price = Decimal(answer) / (Decimal(10) ** 8)   # feed BTC/USD, 8 décimales
    updated_at = float(_u256(words[3]))            # updatedAt = 4ᵉ mot
    round_id = _u256(words[0])                     # roundId (phase-encodé)
    return price, updated_at, {"round_id": str(round_id)}


# ── Spécification d'un flux ───────────────────────────────────────────────

_CHAINLINK_RPC = "https://ethereum-rpc.publicnode.com"
_CHAINLINK_AGGREGATOR = "0xF4030086522a5bEEa4988F8cA5B36dbC97BeE88c"
_CHAINLINK_CALLDATA = "0xfeaf968c"  # latestRoundData()


@dataclass(frozen=True)
class SourceSpec:
    flux_id: str
    kind: str                    # "place" | "aggregator" | "oracle"
    endpoint: str
    currency: Currency
    decode: Callable[[bytes], tuple]
    method: str = "GET"
    post_body: Optional[dict] = None


SPECS: list[SourceSpec] = [
    SourceSpec("binance", "place",
               "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT",
               Currency.USDT, _d_binance),
    SourceSpec("coinbase", "place",
               "https://api.exchange.coinbase.com/products/BTC-USD/ticker",
               Currency.USD, _d_coinbase),
    SourceSpec("kraken", "place",
               "https://api.kraken.com/0/public/Ticker?pair=XBTUSD",
               Currency.USD, _d_kraken),
    SourceSpec("okx_ticker", "place",
               "https://www.okx.com/api/v5/market/ticker?instId=BTC-USDT",
               Currency.USDT, _d_okx_ticker),
    SourceSpec("okx_index", "place",
               "https://www.okx.com/api/v5/market/index-tickers?instId=BTC-USD",
               Currency.USD, _d_okx_index),
    SourceSpec("bitstamp", "place",
               "https://www.bitstamp.net/api/v2/ticker/btcusd/",
               Currency.USD, _d_bitstamp),
    SourceSpec("gemini", "place",
               "https://api.gemini.com/v1/pubticker/btcusd",
               Currency.USD, _d_gemini),
    SourceSpec("bitfinex", "place",
               "https://api-pub.bitfinex.com/v2/ticker/tBTCUSD",
               Currency.USD, _d_bitfinex),
    SourceSpec("coingecko", "aggregator",
               "https://api.coingecko.com/api/v3/simple/price"
               "?ids=bitcoin&vs_currencies=usd&include_last_updated_at=true",
               Currency.USD, _d_coingecko),
    SourceSpec("defillama", "aggregator",
               "https://coins.llama.fi/prices/current/coingecko:bitcoin",
               Currency.USD, _d_defillama),
    SourceSpec("pyth", "oracle",
               "https://hermes.pyth.network/v2/updates/price/latest"
               "?ids[]=0xe62df6c8b4a85fe1a67db44dc12de5db330f7ac66b72dc658afedf0f4a415b43"
               "&parsed=true",
               Currency.USD, _d_pyth),
    SourceSpec("chainlink", "oracle",
               _CHAINLINK_RPC, Currency.USD, _d_chainlink, method="POST",
               post_body={
                   "jsonrpc": "2.0", "id": 1, "method": "eth_call",
                   "params": [{"to": _CHAINLINK_AGGREGATOR,
                               "data": _CHAINLINK_CALLDATA}, "latest"],
               }),
]

# Écartée du pool (à clé, 401 sans clé — 10 §3.1, décision 10 §9). Gardée ici
# pour que le smoke test RECONFIRME le 401 à chaque campagne (une exclusion
# vérifiée, pas postulée).
EXCLUDED_CRYPTOCOMPARE = (
    "https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD"
)


# ── Taxonomie σ/τ ADR-0020 — SOURCE UNIQUE DE VÉRITÉ (ADR-0021 item 2/8) ──────
# La classe σ d'un flux est une PROPRIÉTÉ DE LA SOURCE : elle vit ici, avec SPECS
# et les décodeurs qui décident de la disponibilité de source_ts. Auparavant
# dupliquée en données dans `run_campaign.SIGMA_CLASS_OF_FLUX` (CONSTAT M2) ; ADR-0021
# la centralise ICI (« ne le duplique pas »). `collector`, `run_campaign` et
# `closure` l'importent ; `r1.classify_ecart` la reçoit VIA run_params (aucun
# paramètre hors-bande, ADR-0003), écrite par `collector` depuis cette constante.

# Flux → classe σ (ADR-0020 déc. 3, :3086-3094). CONCORDANCE mesurée avec les
# décodeurs : les trois « sans_horodatage » sont EXACTEMENT les flux dont le
# décodeur rend source_ts=None (_d_binance/_d_kraken/_d_bitfinex ci-dessus) ;
# vérifiée sur fixtures par test_run_campaign (décodage réel, pas un ensemble crû).
SIGMA_CLASS_OF_FLUX: dict = {
    "binance": "sans_horodatage", "kraken": "sans_horodatage",
    "bitfinex": "sans_horodatage",
    "coinbase": "place_horodatee", "okx_ticker": "place_horodatee",
    "okx_index": "place_horodatee", "bitstamp": "place_horodatee",
    "gemini": "place_horodatee",
    "coingecko": "agregateur", "defillama": "agregateur",
    "pyth": "oracle_pyth", "chainlink": "oracle_chainlink",
}

# Planchers σ PAR CLASSE (ADR-0020 déc. 3, :3090-3094), en SECONDES. `None` =
# axe (ii) staleness « non évaluable » pour la classe (jamais un seuil deviné).
#   - place_horodatee : places à horodatage porté → 30 s ;
#   - agregateur      : CoinGecko/DefiLlama → 300 s ;
#   - sans_horodatage : Binance/Kraken/Bitfinex → « non évaluable » (déjà honoré
#                       par la garde `src_ts is not None`, r1) ;
#   - oracle_pyth     : Pyth = 1,5 × heartbeat établi → 30 s ;
#   - oracle_chainlink: Chainlink = 1,5 × heartbeat 3600 s → 5400 s. PS-S2-01 RÉSOLU
#                       (heartbeat ~1 h dérivé du countdown live ; repli fail-closed
#                       levé — WISHLIST/RUNBOOK §7) : 5400 est la valeur COURANTE. La
#                       confirmation feed-doc exacte (3600 s) reste un raffinement
#                       ORCHESTRATEUR (navigateur) ; VALEUR INJECTABLE (ADR-0021 item 7),
#                       `None` si un jour non confirmée. Point d'injection ICI et dans
#                       `closure`/`run_campaign` (sigma_by_class committé), JAMAIS un
#                       littéral dans `r1.classify_ecart` (lit sigma_by_class agnostiquement).
SIGMA_FLOORS_ADR0020_SECONDS: dict = {
    "place_horodatee": 30,
    "agregateur": 300,
    "sans_horodatage": None,
    "oracle_pyth": 30,
    "oracle_chainlink": 5400,
}

# τ RELATIF, une seule valeur pour la classe « BTC/USD-stable » (ADR-0020 déc. 2,
# :3081-3085 : `|vᵢ − médiane_LOO| / médiane_LOO > τ`). FRACTION (0,5 % = 0.005),
# ni un pourcentage « 0,5 » ni un montant en dollars (anti-piège 100×).
TAU_CLASSE_ADR0020_FRACTION = Decimal("0.005")

# Seuil de la clause de révision τ (ADR-0020 :3085-3086 : « Révisé par ADR avant
# lancement si la calibration montre P99(|écart relatif|) > 0,25 % »). FRACTION.
TAU_REVISION_THRESHOLD_FRACTION = Decimal("0.0025")


def default_sigma_by_class() -> dict:
    """σ par classe PROVISOIRE = les planchers ADR-0020 (Decimal ou None), avant la
    clôture de calibration (`closure.compute_closure` calcule `max(plancher,
    3×P99)`). Sert la phase `demo`/`calibration` du driver (capture SANS SEUIL,
    ADR-0020 reframe : la valeur provisoire n'altère pas l'archive)."""
    return {k: (None if v is None else Decimal(v))
            for k, v in SIGMA_FLOORS_ADR0020_SECONDS.items()}


def sigma_class_of_flux_for(pool: list) -> dict:
    """flux→classe restreint au `pool`, écrit dans run_params par `collector`
    (recalculable). LÈVE si un flux du pool n'a pas de classe déclarée
    (fail-closed : jamais un dispatch σ deviné)."""
    missing = [f for f in pool if f not in SIGMA_CLASS_OF_FLUX]
    if missing:
        raise ValueError(
            f"flux sans classe σ déclarée dans SIGMA_CLASS_OF_FLUX : {missing} "
            "— fail-closed (ADR-0021 : aucun dispatch σ deviné)"
        )
    return {f: SIGMA_CLASS_OF_FLUX[f] for f in pool}


def read(spec: SourceSpec, fetch_ts: float,
         timeout: float = _DEFAULT_TIMEOUT) -> Reading:
    """Fait UNE lecture d'un flux et rend un Reading. Ne lève jamais : toute
    anomalie devient une panne typée (fail-closed, 10 §5.2)."""
    base = dict(flux_id=spec.flux_id, kind=spec.kind, endpoint=spec.endpoint,
                fetch_ts=fetch_ts, currency=spec.currency)
    try:
        if spec.method == "POST":
            http_status, raw = _http_post_json(spec.endpoint, spec.post_body, timeout)
        else:
            http_status, raw = _http_get(spec.endpoint, timeout)
    except TransportError:
        return Reading(status=Status.PANNE_TRANSPORT, **base)

    if http_status != 200:
        return Reading(status=Status.PANNE_HTTP, http_status=http_status,
                       raw=raw, **base)
    try:
        price, source_ts, extra = spec.decode(raw)
    except (DecodeError, KeyError, IndexError, ValueError, TypeError,
            ArithmeticError) as e:
        return Reading(status=Status.PANNE_DECODE, http_status=http_status,
                       raw=raw, extra={"decode_error": str(e)}, **base)
    return Reading(status=Status.OK, http_status=http_status, raw=raw,
                   price=price, source_ts=source_ts, extra=extra, **base)
