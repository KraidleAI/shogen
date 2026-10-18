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
CB-7c : ETH coté en USDT chez binance et okx (Q-CA-01 (a) du G0 de CALIB-ACTIFS).
CB-8a : lectures regroupées (CoinGecko, DefiLlama, Bitfinex : quatre actifs, une lecture par hôte, E-C-09),
identifiants exacts ; plafond d'un relevé par actif ; actif, devise et classe des listes fermées du FORMAT §9.1.
CB-8b : Chainlink ETH, USDC et USDT, plafond de 1,05 des stables en extra (E-C-10).
CB-9a (témoin USDC/USDT, ADR-0029 l.174 ; adresses, sélecteurs et décimales lus sur
`docs/adr-0029/g0-calib/PAIRES-ET-TEMOIN.md` §3.1) : OKX `USDC-USDT` ; Uniswap v3, `slot0` du pool 0,01 % ; requête
`eth_call` construite (`eth_call`, CORPS), l'hôte RPC restant celui de la forme (`formes.json`).
CB-9b : Curve, `get_dy` du 3pool (Q-CA-09 du G0 de CALIB-ACTIFS).
CB-9c : unité sur chaîne de chaque décodeur (`unite_sur_chaine`), qui porte la règle « une unité on-chain = un hôte
RPC » de `formes.json` (entree.py).
C-P2D-1 (adjudication Q-1 de la tranche D) : classe `temoin` des trois lectures du témoin, hors des classes du recalcul
(ADR-0029 l.174 : « hors des classes USD et hors du vote »).
GEL-5 (SHOGEN-S2BIS-TEMOIN-BLOC-1 ; avis de l'advisor du lot de gel, Q-B, option 2 encadrée ; FORMAT §9.1) : Uniswap et
Curve en requête groupée [eth_blockNumber, eth_call, eth_blockNumber] (`lot`), blocs encadrants en extra (`_lot`)."""
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
BLOC = re.compile("0x[0-9a-fA-F]{1,16}")              # numéro de bloc (GEL-5) : hexadécimal strict, 64 bits au plus
CHIFFRES, TEXTE = 16, 4300                      # bornes de `_entier` : instant sous 10^16 ; texte de int()
ACTIFS, DEVISES = ("BTC", "ETH", "USDC", "USDT"), ("USD", "USDT")           # listes fermées du FORMAT §9.1
CLASSES = ("place_horodatee", "sans_horodatage", "agregateur", "oracle_chainlink", "temoin")    # témoin : C-P2D-1
PLAFOND = "1.05000000"      # maxSubmissionValue 105000000 à 8 décimales, USDC/USD et USDT/USD (pièce §2 l.72 ; E-C-10)


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


def _groupe(table, objets, lire):
    """Lecture regroupée (CB-8a ; E-C-09 ; ADR-0029 l.236) : `objets(j)` rend {identifiant : objet} ; les identifiants
    rendus sont exactement ceux de `table` {identifiant : actif}, sinon la lecture entière est une panne (pannes
    identiques entre actifs, déclarées) ; un relevé par actif, `lire(objet)`, dans l'ordre de `table`."""
    def lire_groupe(j):
        o = objets(j)
        if type(o) is not dict or sorted(o) != sorted(table):
            raise ValueError("groupe : identifiants")
        return [(actif, *lire(o[k])) for k, actif in table.items()]
    return lire_groupe


def _lignes(j):
    """Bitfinex `v2/tickers` : {symbole : ligne}, chaque ligne [SYMBOLE, puis les champs de `v2/ticker`], 11 éléments au
    moins (S2 en exigeait 10 dans `v2/ticker`), symbole unique."""
    if type(j) is not list or not all(type(x) is list and len(x) >= 11 for x in j) or len({x[0] for x in j}) < len(j):
        raise ValueError("bitfinex : forme regroupée")
    return {x[0]: x for x in j}


def _chainlink(plafond=None):
    """`latestRoundData` d'un proxy (flux à 8 décimales : BTC, ETH, USDC, USDT, pièce §2) ; CB-8b (E-C-10) : `plafond`,
    valeur maximale publiée du flux (USDC et USDT), portée en extra et jamais appliquée : la classe « borné » se juge
    au recalcul (E-C-26) ; None : flux sans plafond."""
    def lire(j):
        h = _champ(j, "result")
        if type(h) is not str or not MOTS.fullmatch(h):
            raise ValueError("chainlink : cinq mots attendus")
        mots = [int(h[2 + 64 * i:66 + 64 * i], 16) for i in range(5)]
        reponse = mots[1] - (1 << 256 if mots[1] >= 1 << 255 else 0)        # answer : int256, 8 décimales
        return Decimal(f"{reponse}E-8"), mots[3] * S, {"round_id": str(mots[0]), **({"plafond": plafond} if plafond
                                                                                    else {})}
    return lire


D_USDC = D_USDT = 6                                         # decimals() de USDC et de USDT (PAIRES-ET-TEMOIN l.89)
UNISWAP, SLOT0 = "0x3416cF6C708Da44DB2624D63ea0AAef7113527C6", "0x3850c7bd"   # pool 0,01 %, token0 USDC (l.90)
CURVE, GET_DY = "0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7", "0x5e0d443f"    # 3pool : coins DAI, USDC, USDT (l.94)
MONTANT = 10 ** 6                                                   # dx de get_dy : 1 USDC, à 6 décimales (l.94)


def eth_call(adresse, selecteur, *arguments):
    """Corps JSON-RPC d'un `eth_call` au bloc « latest », sous la forme du corps de Chainlink en S2 (sources.py
    l.278-282 : json.dumps, séparateurs par défaut) : `data` = sélecteur de 4 octets, puis chaque argument, entier de 0
    à 2^256 exclu, sur 32 octets big-endian. Jamais envoyé ici : la forme qui le porte nomme l'hôte RPC."""
    return json.dumps(_appel(1, adresse, selecteur, *arguments))


def _appel(n, adresse, selecteur, *arguments):
    """Objet JSON-RPC de l'`eth_call` d'identifiant `n` ; adresse, sélecteur ou argument hors forme : ValueError."""
    if not (re.fullmatch("0x[0-9a-fA-F]{40}", adresse) and re.fullmatch("0x[0-9a-f]{8}", selecteur) and all(
            type(a) is int and 0 <= a < 1 << 256 for a in arguments)):
        raise ValueError("eth_call : adresse, sélecteur ou argument")
    return {"jsonrpc": "2.0", "id": n, "method": "eth_call", "params": [
        {"to": adresse, "data": selecteur + "".join(f"{a:064x}" for a in arguments)}, "latest"]}


def lot(adresse, selecteur, *arguments):
    """Requête groupée du témoin sur chaîne (GEL-5) : [eth_blockNumber (id 1), `eth_call` au bloc « latest » (id 2),
    eth_blockNumber (id 3)], json.dumps aux séparateurs par défaut, comme `eth_call`."""
    return json.dumps([{"jsonrpc": "2.0", "id": 1, "method": "eth_blockNumber", "params": []},
                       _appel(2, adresse, selecteur, *arguments),
                       {"jsonrpc": "2.0", "id": 3, "method": "eth_blockNumber", "params": []}])


def _lot(lire):
    """Réponse de `lot` (GEL-5) : trois réponses appariées par `id` (JSON-RPC 2.0 n'en impose pas l'ordre), chacune avec
    `result` et sans `error` ; blocs (id 1 et 3) en hexadécimal strict ; `lire` décode la réponse de l'appel (id 2) ;
    extra : `bloc_avant`, `bloc_apres` en décimal. Lot incomplet, `error`, bloc illisible, `bloc_apres` < `bloc_avant` :
    la lecture entière est une panne. Non atomique : un bloc peut passer entre les appels (écart attendu ≤ 1 bloc)."""
    def lire_lot(j):
        if type(j) is not list or len(j) != 3 or not all(type(x) is dict and "result" in x and "error" not in x
                                                         for x in j):
            raise ValueError("lot : trois réponses sans erreur attendues")
        par = {str(x["id"]): x for x in j if type(x.get("id")) is Decimal}
        if sorted(par) != ["1", "2", "3"] or not all(type(par[k]["result"]) is str and BLOC.fullmatch(
                par[k]["result"]) for k in "13"):
            raise ValueError("lot : identifiants ou blocs")
        avant, apres = (int(par[k]["result"], 16) for k in "13")
        if apres < avant:
            raise ValueError("lot : bloc_apres < bloc_avant")
        p, ts, extra = lire(par["2"])
        return p, ts, {**extra, "bloc_avant": str(avant), "bloc_apres": str(apres)}
    return lire_lot


def _mots(j, n):
    """`result` d'une réponse `eth_call` : exactement n mots de 32 octets en hexadécimal strict (règle de MOTS)."""
    h = j["result"]
    if type(h) is not str or not re.fullmatch("0x[0-9a-fA-F]{%d}" % (64 * n), h):
        raise ValueError(f"eth_call : {n} mots attendus")
    return [int(h[2 + 64 * i:66 + 64 * i], 16) for i in range(n)]


def _quotient(a, b):
    """a / b, entiers, en une seule division sous une copie de CONTEXTE, jamais sous le contexte du fil (E-C-07)."""
    with decimal.localcontext(CONTEXTE):
        return Decimal(a) / Decimal(b)


def _fini(x):
    """Texte d'une valeur lue en chaîne ou en Decimal, finie, > 0, exposant dans les bornes (règle du prix)."""
    p = Decimal(x) if type(x) in (str, Decimal) else None
    if p is None or not (p.is_finite() and p > 0 and CONTEXTE.Emin <= p.adjusted() <= CONTEXTE.Emax):
        raise ValueError("valeur non finie, nulle, négative ou hors bornes")
    return str(p)


def _okx_temoin(j):
    """OKX `USDC-USDT` (l.87) : instrument contrôlé, `last` et `ts` comme `_okx` ; `askPx` et `bidPx` finis et > 0, en
    extra, sans ordre exigé (« Best ask price may be lower than the best bid price during the pre-open period »,
    documentation d'OKX, « GET / Ticker », copie du registre biblio/)."""
    prix, ts, _extra = _okx("last")(j)
    if j["data"][0]["instId"] != "USDC-USDT":
        raise ValueError("okx : instrument")
    return prix, ts, {k: _fini(j["data"][0][k]) for k in ("askPx", "bidPx")}


def _uniswap(j):
    """`slot0()` (l.90) : sept mots ; sqrtPriceX96, mot 1, Q64.96 (de 1 à 2^160 exclu) ; prix de token1 (USDT) par
    token0 (USDC) = sqrtPriceX96² / 2^192 · 10^(D_USDC − D_USDT), une seule division (`_quotient`) ; tick, mot 2,
    entier signé sur 32 octets, en extra. Aucun instant de source : les blocs encadrants vont en extra (`_lot`)."""
    s, tick = _mots(j, 7)[:2]
    if not 0 < s < 1 << 160:
        raise ValueError("uniswap : sqrtPriceX96 hors de Q64.96")
    return _quotient(s * s * 10 ** D_USDC, 10 ** D_USDT << 192), None, {
        "sqrt_price_x96": str(s), "tick": str(tick - (1 << 256 if tick >= 1 << 255 else 0))}


def _curve(j):
    """`get_dy(1, 2, MONTANT)` (l.94) : un mot, dy, unités de USDT rendues pour MONTANT unités de USDC, net des frais
    et du glissement ; prix = dy · 10^D_USDC / (MONTANT · 10^D_USDT), une division (`_quotient`). Sens lu
    (SHOGEN-S2BIS-CURVE-DOC-1, lecture du 2026-10-17 : documentation des pools « plain » anciens et source
    `StableSwap3Pool.vy` du dépôt officiel `curvefi/curve-contract`, branche `master`) : dx et dy en unités natives de
    leurs coins, frais plats déduits (dénominateur 10^10). `price_oracle` du pool Stableswap-NG (moyenne mobile, ni
    nette de frais ni échange simulé) n'est pas retenu. Limites déclarées (C-P2D-2) : identité de la source
    `master` avec le bytecode déployé non vérifiée ; rattachement direct du pool NG à sa fabrique non lu (registre de
    l'API et implémentation commune seulement) ; absence du bogue d'oracle du pool NG non vérifiée sur chaîne (pool
    créé après la correction d'après l'API, inféré)."""
    (dy,) = _mots(j, 1)
    return _quotient(dy * 10 ** D_USDC, MONTANT * 10 ** D_USDT), None, {"dy": str(dy)}


CORPS = {"uniswap_usdc_usdt": lot(UNISWAP, SLOT0),                   # corps de requête, lié au décodeur de la réponse
         "curve_usdc_usdt": lot(CURVE, GET_DY, 1, 2, MONTANT)}       # i = 1 (USDC), j = 2 (USDT)
H, P = "place_horodatee", "sans_horodatage"
CG = {"bitcoin": "BTC", "ethereum": "ETH", "usd-coin": "USDC", "tether": "USDT"}          # identifiants de CoinGecko
DECODEURS = {      # nom : (actif, devise, classe de source, décodeur du JSON lu) ; S2 : SPECS, SIGMA_CLASS_OF_FLUX
    # actif None : lecture regroupée, le décodeur rend [(actif, prix, instant, extra)]
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
    "chainlink_btc": ("BTC", "USD", "oracle_chainlink", _chainlink()),
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
    # CB-8a : lectures regroupées, quatre actifs (E-C-09 ; PROPOSITION de CALIB-ACTIFS §2.2 ; pièce, tableau 1.2)
    "coingecko_groupe": (None, "USD", "agregateur", _groupe(CG, lambda j: j, _coingecko)),
    "defillama_groupe": (None, "USD", "agregateur", _groupe({"coingecko:" + k: a for k, a in CG.items()},
                                                            lambda j: _champ(j, "coins"), _defillama)),
    "bitfinex_groupe": (None, "USD", P, _groupe({"tBTCUSD": "BTC", "tETHUSD": "ETH", "tUDCUSD": "USDC",
                                                 "tUSTUSD": "USDT"}, _lignes, lambda x: (x[7], None, {}))),
    # CB-8b : Chainlink, proxy principal de chaque flux (pièce §2 ; Q-CA-08 du G0 de CALIB-ACTIFS)
    "chainlink_eth": ("ETH", "USD", "oracle_chainlink", _chainlink()),
    "chainlink_usdc": ("USDC", "USD", "oracle_chainlink", _chainlink(PLAFOND)),
    "chainlink_usdt": ("USDT", "USD", "oracle_chainlink", _chainlink(PLAFOND)),
    "okx_usdc_usdt": ("USDC", "USDT", "temoin", _okx_temoin),      # témoin : USDT par USDC, hors du vote
    "uniswap_usdc_usdt": ("USDC", "USDT", "temoin", _lot(_uniswap)),         # GEL-5 : requête groupée
    "curve_usdc_usdt": ("USDC", "USDT", "temoin", _lot(_curve)),
}


SUR_CHAINE = {"uniswap_usdc_usdt": "uniswap", "curve_usdc_usdt": "curve"}           # pièces du témoin sur chaîne


def unite_sur_chaine(nom):
    """Unité sur chaîne que lit le décodeur `nom` (ADR-0029 l.174) : « chainlink » pour tout flux de la classe
    `oracle_chainlink` (une seule unité du pool, ADR-0029 l.168), la pièce du témoin sinon ; None hors chaîne."""
    return "chainlink" if DECODEURS.get(nom, (None,) * 4)[2] == "oracle_chainlink" else SUR_CHAINE.get(nom)


def _releve(actif, devise, classe, prix, ts, extra):
    """Relevé exact : actif, devise et classe des listes fermées (FORMAT §9.1) ; prix lu en chaîne ou en Decimal (jamais
    un flottant), fini, > 0, exposant dans les bornes de CONTEXTE ; instant entier de 0 à 2^53 µs exclu, ou None ;
    extra de chaînes. Tout autre cas lève."""
    if type(prix) not in (str, Decimal) or type(ts) not in (int, type(None)) or type(extra) is not dict:
        raise TypeError("relevé : types")
    if actif not in ACTIFS or devise not in DEVISES or classe not in CLASSES:
        raise ValueError("relevé : actif, devise ou classe hors des listes")
    p = Decimal(prix)
    if not (p.is_finite() and p > 0 and CONTEXTE.Emin <= p.adjusted() <= CONTEXTE.Emax):
        raise ValueError("relevé : prix non fini, nul, négatif ou hors bornes")
    if ts is not None and not 0 <= ts < 1 << 53 or not all(type(k) is str is type(v) for k, v in extra.items()):
        raise ValueError("relevé : instant ou extra")
    return {"actif": actif, "classe": classe, "devise": devise, "extra": extra, "prix": str(p), "ts_source": ts}


def decoder(nom, octets):
    """(statut, valeurs) : ("ok", relevés) ou ("panne_decode", None) ; ne lève jamais (E-C-03, E-C-06). Plafond (CB-8a ;
    FORMAT §9.1) : un relevé par actif au plus, donc quatre ; aucun relevé, ou un actif répété : panne."""
    try:
        with decimal.localcontext(CONTEXTE):
            actif, devise, classe, lire = DECODEURS[nom]
            lu = lire(json.loads(octets, parse_float=Decimal, parse_int=Decimal))
            releves = lu if actif is None else [(actif, *lu)]
            if not releves or len({r[0] for r in releves}) < len(releves):
                raise ValueError("relevés : aucun, ou actif répété")
            valeurs = [_releve(a, devise, classe, p, ts, x) for a, p, ts, x in releves]
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
