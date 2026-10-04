# Rapport lecteur — pool de sources pour S2-bis (oracles, agrégateurs, places, DEX)

> *Note de versement de l'orchestrateur* : citations anglaises de pages web non versées à `biblio/` passées de « … » à “…” (gate S-G5) ; lectures [lu] web du rapport, copies hors dépôt.


Lecteur : `claude-sonnet-5-5` (Gate 0 : identifiant déclaré en tête de session ; l'effort `high` n'est pas vérifiable depuis la session).
Brief : `pool-bis/BRIEF-POOL-BIS.md`, sha256 `c3ccacc743ba7986ed03fc8ee6e4130140cf56e28a96d71179e3dcd30cdde48d` (vérifié).
Extension de périmètre (agrégateurs, places, DEX, « taille du pool ») reçue de l'orchestrateur en cours de passe, traitée ici.
Dates : toutes les lectures sont du **2026-10-04, 04:36 à 04:55 UTC** (`date -u`). Copies et sondes : `pool-bis/web/`, `pool-bis/probes/`,
journaux `pool-bis/probe-log.txt` et `pool-bis/fetch-log.txt`. Scripts rejouables : `asn.py` (DNS-over-HTTPS Cloudflare + Google, RIPEstat,
Team Cymru par DoH), `rpc.py`, `univ3.py`.
Niveaux : [lu] lu sur place (URL, date) ; [sonde] requête réelle de cette passe ; [2nd] seconde main ; [inféré] déduction de l'auteur ; [abs] absent de la source ;
[manque] page refusée ou inaccessible, jamais contournée.
Interdits respectés : aucune pièce de `docs/15-*`, `docs/16-*`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, aucun `*.jsonl` ouvert ;
aucune clé, aucun compte, aucune installation, aucun fichier suivi modifié.

---

## 0. Réponses courtes aux questions de l'investisseur

1. **Comment a-t-on sélectionné nos sources ?** Pas par un échantillonnage de l'univers des sources. Le pool est ce qu'une passe de faisabilité du 2026-08-05
   a trouvé lisible sans clé en BTC/USD, plus une décision de périmètre. Pièces : doc 10 §3.1 (table : « classe BTC/USD, endpoint public sans clé, HTTP 200, valeur
   et horodatage lisibles », CryptoCompare écartée en 401) [lu, `docs/10-mesures-pilotes-design.md` l.82-98] ; doc 10 §9 pt 1 : la question posée au mainteneur était
   « les 7 places primaires seules, ou les 11 sources répondantes », avec la recommandation « inclure CoinGecko, DefiLlama, Pyth et Chainlink *précisément parce que*
   la détection de leur dépendance par l'instrument est le résultat qui tranche » [lu, doc 10 l.656-660]. Aucun critère écrit de représentativité du marché ne figure
   dans les pièces lues [abs]. Le pool de S2-bis (10 unités-hôtes, Pyth retiré ex ante) en est le descendant [lu, ADR-0029 §2.5, l.137-142].
2. **Avons-nous sélectionné Hyperlane ?** Non, et à raison pour la classe BTC/USD : Hyperlane n'apparaît nulle part dans le dépôt lisible [sonde : grep, 0 occurrence hors
   dossiers interdits] et ce n'est **pas un oracle de prix** (§1). Il n'est d'ailleurs pas dans la liste CoinGecko « oracle » (62 identifiants, relevé orchestrateur) ;
   CoinGecko le classe « Cross-chain Communication », « Interoperability », « Infrastructure » [sonde : `api.coingecko.com/api/v3/coins/hyperlane`, 04:37Z].
3. **Faut-il en rajouter ?** Oui pour le produit, avec une réserve de méthode pour la décision R1 de S2-bis (§6, §8). Le pool actuel couvre 7 places, 2 agrégateurs
   (dont l'un copie l'autre), 1 oracle. Il manque : plus de places primaires (5 des 10 premières places du classement de confiance CoinGecko n'y sont pas : Gate, Bitget, MEXC, Crypto.com, Bybit), les oracles
   dont on peut lire un prix sans clé (peu), les agrégateurs à lecture libre (peu, et à licence restrictive), et une famille absente : l'état d'un pool DEX lu par RPC.
4. **Fait majeur de mesure (§4)** : sur 28 hôtes mesurés aujourd'hui, la couche de livraison se range presque entièrement dans deux ASN, Cloudflare (AS13335) et Amazon
   (AS16509). Ajouter des hôtes de cette famille **ne fait presque pas monter k_eff sur l'axe ASN** ; seuls Akamai (MEXC), Hetzner (Band, hors pool) et Google Cloud
   (RPC Tenderly) sont hors de ces deux familles parmi les candidats lus. Les ajouts valent donc d'abord par la **racine d'amont** (axe contenu), pas par l'ASN.

---

## 1. Hyperlane (établi)

- **Nature** : « Hyperlane is a permissionless interoperability protocol for cross-chain communication across different blockchain environments. » [lu, `docs.hyperlane.xyz/docs/intro`, 04:36Z].
  Messagerie inter-chaînes et ponts de jetons (Warp Routes, Interchain Accounts) ; modules de sécurité configurables (ISM) [lu, même page].
- **A-t-il un « oracle » ?** Oui, mais d'un autre genre : un *gas oracle* (contrat `StorageGasOracle`) qui sert à tarifer la livraison d'un message : “Exchange rates and gas prices
  are up to the relayer to decide.” [lu, `docs.hyperlane.xyz/docs/reference/hooks/interchain-gas.md`]. Taux de change entre jetons de gaz et prix du gaz, fixés par le relayeur ; ce n'est pas
  un flux BTC/USD. Le document complet des docs (`llms-full.txt`, 867 287 octets) contient **0 occurrence de « BTC »** [sonde : grep, 04:37Z].
- **Peut-il transporter des prix d'un autre oracle ?** Oui : un exemple de la doc, “The `ChainlinkISM` is initialized with a set of Chainlink oracles and verifies the price feed data
  provided has been signed over” [lu, `llms-full.txt` l.12825] ; et « smart contracts can use interchain queries to look up oracle exchange rates » [lu, l.18614]. C'est un **transport**, pas une source.
- **Conclusion** : Hyperlane n'a pas de BTC/USD à lire ; il ne relève pas de la classe. Ce que le certificat pourrait dire de lui (dépendance d'un pont à un oracle de prix) est un autre produit.
  Non retenu, motif : nature. Aucune sonde de prix n'est possible (rien à lire).

---

## 2. Table des candidats (grille du brief ; BTC/USD lisible sans clé, cadence, horodatage, licence, amonts, ASN, sonde)

Légende ASN : mesure rejouable du jour (`asn.py` : DNS en DoH Cloudflare **et** Google, RIPEstat, Team Cymru ; concordance RIPEstat = Cymru sur toutes les IP lues). Résolution depuis un seul point
(ce poste), donc mono-vantage (résidu 3 de doc 10 §4.1) et côté livraison (résidu 1).

### 2.1 Places de marché (au-delà des sept du pool)

Sonde = une requête GET sans clé, 04:39:49–04:40:05Z ; valeur BTC en USDT sauf mention. Classement = rang de confiance CoinGecko, `api.coingecko.com/api/v3/exchanges` [sonde, 04:48Z] ; ce rang est un
classement de CoinGecko, pas une mesure de volume (le champ de volume est revenu à 0 dans la réponse).

| place (rang CG) | endpoint lu | HTTP | valeur lue | horodatage porté | ASN du nom d'hôte (hébergeur) | limite lue | remarques |
|---|---|---|---|---|---|---|---|
| Gate (5) | `api.gateio.ws/api/v4/spot/tickers?currency_pair=BTC_USDT` | 200 | 84 820,5 USDT | **aucun** | AS16509 Amazon (ELB Tokyo) | non lue (page 403 : manque) | docs refusées (`www.gate.com/docs/...`, 403) |
| Bitget (6) | `api.bitget.com/api/v2/spot/market/tickers?symbol=BTCUSDT` | 200 | 84 815,04 USDT | `ts` ms | AS13335 Cloudflare | non lue (page de limite non extraite) | |
| MEXC (8) | `api.mexc.com/api/v3/ticker/price?symbol=BTCUSDT` | 200 | 84 814,15 USDT | **aucun** | **AS20940 Akamai** (seul hôte hors Cloudflare/Amazon de la liste) | « HTTP 429 return code is used when breaking a request rate limit » [lu, doc MEXC] | CNAME `edgesuite.net` |
| Crypto.com (9) | `api.crypto.com/exchange/v1/public/get-tickers?instrument_name=BTC_USD` | 200 | 84 817,86 **USD** | `t` ms | AS13335 | non lue | cotation USD native |
| Bybit (10) | `api.bybit.com/v5/market/tickers?category=spot&symbol=BTCUSDT` | **403** | — | — | AS16509 (CloudFront) | — | « configured to block access from your country » [sonde] : bloqué depuis ce point ; **à essayer depuis chaque observateur au smoke** ; je ne contourne pas |
| KuCoin (11) | `api.kucoin.com/api/v1/market/orderbook/level1?symbol=BTC-USDT` | 200 | 84 819,2 USDT | `time` ms | AS13335 | non lue (page 404) | |
| HTX (56) | `api.huobi.pro/market/detail/merged?symbol=btcusdt` | 200 | 84 793,01 USDT | `ts` ms | AS16509 (CloudFront) | non lue (page JS) | |
| Upbit (30) | `api.upbit.com/v1/ticker?markets=KRW-BTC,USDT-BTC` | 200 | KRW 115 300 000 ; USDT-BTC 84 823,17 | `trade_timestamp` ms (USDT-BTC : 04:31:59Z, soit 8 min de retard, marché mince) | AS16509 (Séoul) | « Up to 10 requests per second », par IP [lu, `global-docs.upbit.com/reference/rate-limits`] | la devise principale est le KRW, donc hors classe sans conversion ; seul USDT-BTC est compatible |
| Bitso (27) | `api.bitso.com/v3/ticker/?book=btc_usd` | 200 | 84 816 **USD** | `created_at` ISO | AS13335 | non lue (page 404) | volume 24 h lu : 4,24 BTC (marché très mince) |
| Binance (pool) | `api.binance.com/api/v3/ticker/price` | **451** depuis ce point | — | — | AS16509 (CloudFront) | | « Service unavailable from a restricted location » [sonde] ; même cause que le caveat 451 de doc 10 §3.3 ; déjà au pool, hors de ma portée de vérification |

Remarque de redistribution : aucune des pages de conditions de ces places n'a été lue sur les données publiques [abs] ; la question « peut-on republier les octets bruts » (ADR-0003/0005, motif du retrait de Pyth,
ADR-0029 §2.5) **n'est pas tranchée pour ces places**. À lire avant tout ajout, place par place.

### 2.2 Agrégateurs (au-delà de CoinGecko et DefiLlama)

| agrégateur | lisible sans clé ? | sonde | cadence / horodatage | licence de redistribution | amonts déclarés | ASN |
|---|---|---|---|---|---|---|
| **CoinPaprika** | **oui** : `api.coinpaprika.com/v1/tickers/btc-bitcoin` | 04:40:00Z, 200, 84 799,49 USD | `last_updated` = 04:35:15Z ; résolution des prix “up to 10 minutes, up to 3 minutes, or up to 1 minute, depending on your plan” [lu, `docs.coinpaprika.com/faq.md`] ; la gratuite est vraisemblablement la plus lente [inféré] | **“only the Enterprise package allows data to be redistributed or shared”** [lu, même page] ; limite 10 req/s par IP [lu] | “a volume-weighted average across the markets we track” ; « over 350 active exchanges » [lu, même page] : copie des racines places | AS13335 |
| **Coinlore** | oui : `api.coinlore.net/api/ticker/?id=90` | 04:40:01Z, 200, 84 810,11 USD | **aucun horodatage** dans la charge utile [sonde] ; « no strict rate limit, we recommend around one request per second » [lu, `coinlore.com/cryptocurrency-data-api`] | non lue [abs] | « 300+ exchanges » ; méthode de pondération non lue [abs] | AS13335 |
| Blockchain.com | oui : `blockchain.info/ticker` | 04:40:05Z, 200 | aucun horodatage lu ; prix par devise | non lue [abs] | non déclarés [abs] | AS13335 |
| Coinbase « spot » (v2) | oui : `api.coinbase.com/v2/prices/BTC-USD/spot` | 04:40:05Z, 200, 84 803,935 | aucun horodatage | non lue | **même opérateur que la place Coinbase du pool** : copie | AS13335 |
| CoinMarketCap | **non** : 401 « API key missing » (`pro-api.coinmarketcap.com`) [sonde] | | | | | |
| Kaiko | **non** : 403 « Please provide authentication details » [sonde] | | | | | |
| CoinAPI | **non** : 401 « You did not provided API Key » [sonde] | | | | | |
| CryptoCompare / CoinDesk Data | **non** : 401 « API key required » sur `min-api.cryptocompare.com` et `data-api.coindesk.com` [sonde, 04:40:04Z] ; reconfirme l'écart de S2 | | | | | |
| Messari | liste d'actifs lisible (1 000 entrées, sans prix) ; les points de prix répondent 403 « invalid auth mechanism » [sonde] | | | | | |
| CF Benchmarks BRR | page publique, pas de lecture : l'indice est « a once a day benchmark » ; “Use and distribution of the CF Benchmarks data requires a license” [lu, `cfbenchmarks.com/data/indices/BRR`] | | quotidien | licence requise | “exchanges that conform to the CME CF Constituent Exchange Criteria” | |
| « Binance price index » (`fapi.../premiumIndex`) | 451 depuis ce point [sonde] ; composition de l'indice non lue [abs] | | | | | |
| DefiLlama (pool) | `api.llama.fi/oracles` : **402** “Upgrade to the paid API plan” ; `defillama.com/oracles` : 403 [sonde/manque] | | | | | |

### 2.3 Oracles (liste CoinGecko et hors liste)

| oracle | BTC/USD lisible sans clé ? (preuve) | cadence, horodatage | licence | amonts déclarés | verdict de lecture |
|---|---|---|---|---|---|
| **Chainlink** (au pool) | oui : `eth_call latestRoundData()` sur `0xF403…E88c`, 6 RPC publics sans clé sur 18 essayés ont répondu [sonde 04:42Z] : 84 837,37 USD, `updatedAt` 03:53:59Z, `roundId` 0x70000000000006107 | `updatedAt` en mot 4 ; la dernière mise à jour lue a ≈ 48 min d'âge au moment de la sonde [sonde] | licence des données non lue [abs] | **nouveau, lu** : « 3+ crypto price data aggregators and/or market data vendors using CEX and/or DEX data » [lu, `docs.chain.link/data-feeds/data-sources`] ; noms des agrégateurs non donnés [abs] | reste au pool ; son amont n'est plus « non documenté » (dette doc 10 §10.6) mais documenté **au niveau catégorie** |
| **Pyth** | **non, aujourd'hui** : Hermes répond 401 « unauthorized » [sonde 04:40:22Z] ; « the Hermes API requires a Pyth API Key (since August 26, 2026) » [lu, `docs.pyth.network/llms.txt`] | — | page de plans : voir ADR-0029 §2.5 | « 120+ first-party publishers including major exchanges, trading firms, and market makers » [lu, `llms-price-feeds-core.txt`] | **voie B′ testée** : contrat Pyth EVM Ethereum `0x4305…69C6` (adresse issue de ma mémoire, vérifiée par la réponse du contrat) : `getPriceUnsafe` du flux BTC/USD renvoie 64 735,61 USD publié le **2026-07-23 18:42:56Z**, soit 73 jours de retard [sonde 04:48Z]. « anyone can push a price update » [lu, `llms-price-feeds-core.txt`] : le contrat ne porte une valeur fraîche que si quelqu'un la pousse. **Pyth reste dehors** (conforme ADR-0029 §2.5) |
| **RedStone** | **deux voies** : (a) **contrat Ethereum** `0xAB7f623fb2F6fea6601D4350FA0E2290663C28Fc`, `description()` = « RedStone Price Feed for BTC », 8 décimales : 84 833,82 USD, horodaté 04:04:23Z, âge ≈ 43 min [sonde 04:47Z, RPC Tenderly] ; l'adresse n'est pas tirée d'une page primaire lue (la page des feeds `app.redstone.finance/push-feeds` est un rendu JS non lu) ; (b) passerelle `oracle-gateway-1.a.redstone.finance/data-packages/latest/redstone-primary-prod` : **HTTP 200 sans clé**, 5 signatures valides pour BTC à 04:38:20Z (84 805,6), mais **1 972 925 octets par lecture** et la doc dit que la lecture exige une clé | push : paramètres de mise à jour non lus ; gateway : horodatage ms par paquet, cadence 10 s | conditions du site : interdiction d'extraction systématique et d'« automated use » sur *le site* [lu, `redstone.finance/terms-of-use`] ; aucune licence de données lue [abs] | « over 30 premier cryptocurrency exchanges and derivatives platforms, including industry leaders such as Binance, Coinbase, OKX, Bybit, and Kraken » ; « more than 50 on-chain trading protocol deployments » ; agrégateurs « Kaiko, CoinMarketCap » [lu, `docs.redstone.finance/docs/technical-reference/data-quality/data-flow/`] | (b) **contradiction à signaler** : “requires an authenticatedGateways parameter: a list of gateways to query, each with its own API key” et « Rate limit on RedStone's own gateway: 1 request/second per API key » [lu, `.../price-feeds/pull-model/`], alors que l'hôte a répondu sans clé : lecture **hors contrat**, à ne pas fonder (invariant « strictement sans clé » = accès documenté sans clé). (a) est lisible, mais amont = mêlée de places déjà au pool + DEX + agrégateurs |
| **DIA** | **oui** : `api.diadata.org/v1/quotation/BTC` → 84 798,72 USD, `Time` 04:35:59Z (110 s d'âge) [sonde 04:37:48Z] ; pas de limite lue dans les en-têtes | `Time` ISO ; cadence non lue | **manque** : `docs.diadata.org` renvoie un défi Cloudflare (403) ; seule la page d'accueil via `/llms.txt` a été lue | « Direct exchange sourcing, no third-party API dependencies » ; « 100+ data sources integrated » ; « Outlier filtering, VWAP aggregation » [lu, `www.diadata.org`] | **candidat sérieux** pour un ajout, sous réserve de lire licence et limites |
| **Hyperliquid** (oracle natif de L1 de dérivés) | **oui** : `POST api.hyperliquid.xyz/info {"type":"metaAndAssetCtxs"}` → `oraclePx` BTC = 84 817,1 ; `markPx` 84 787,0 [sonde 04:37:55Z] | « validators … publishing spot oracle prices … every 3 seconds » [lu, `.../hypercore/oracle.md`] ; **pas d'horodatage** dans la charge utile (72 057 octets) [sonde] | non lue [abs] | « weighted median of Binance, OKX, Bybit, Kraken, Kucoin, Gate IO, MEXC, and Hyperliquid spot mid prices » ; poids 3, 2, 2, 1, 1, 1, 1, 1 [lu, même page] | **copie à 100 % d'amonts de places** (3 sur 7 déjà au pool) ; limite : « REST requests share an aggregated weight limit of 1200 per minute » par IP, poids 20 pour ce type de requête [lu, `.../rate-limits-and-user-limits`] soit 60 lectures/min |
| **dYdX v4** (oracle natif de chaîne) | oui : `indexer.dydx.trade/v4/perpetualMarkets?ticker=BTC-USD` → `oraclePrice` 84 820 [sonde 04:39:31Z] | pas d'horodatage dans ce champ [sonde] | non lue [abs] | « each validator runs a sidecar that pulls prices from oracle providers and external exchanges, such as Binance, Bitfinex, Bitstamp, Bybit, Coinbase » [lu, `docs.dydx.xyz/concepts/trading/oracle`] | copie de places + « oracle providers » non nommés ; pas d'horodatage |
| **Band** | **pas établi** : le point documenté `…/oracle/v1/request_prices?symbols=BTC` répond 200 mais avec `resolve_time` = 1758787715, soit **2025-09-25**, 374 jours de retard [sonde 04:37:49Z, `laozi1.bandchain.org`] ; le module `feeds` (“At the end of each block, BandChain computes the weighted medianized price data” [lu, `docs.bandchain.org/concurrent-price-stream/offchain-consumption`]) renvoie 501 sur le chemin que j'ai essayé ; lecture EVM v3 par `PacketConsumerProxy.getPrice("CS:BTC-USD")` [lu, `…/using-band-dataset/v3`] : adresse du contrat non trouvée | | | non lus | **écarté faute de lecture fraîche établie** ; hôte REST sur Hetzner (AS24940), donc ASN hors Cloudflare/Amazon si une lecture fraîche était trouvée |
| **Supra** | **non** : API REST avec « x-api-key … Please request your key here » [lu, `docs.supra.com/oracles/apis-real-time-and-historical-data/rest-api`] ; lecture on-chain push non sondée | | | « prices derived from up to 21 data sources » [lu, `docs.supra.com/oracles/data-feeds`] | écarté (clé) ; push on-chain non examiné |
| **SEDA** | **non** : « All API requests (except /health and /info) require authentication using a bearer token » [lu, `docs.seda.xyz/.../seda-fast/api-reference/rest-api.md`] | | | programmes d'oracle définis par l'utilisateur | écarté (clé) |
| **APRO** | REST : « All routes require the following two headers for user authentication » [lu, `docs.apro.com/en/data-pull-evm-chain/api-and-websocket-guide.md`] ; push on-chain : BTC/USD **5 % / 180 jours** sur Base, **2 % / 24 h** sur CORE, un feed à 0,5 % / 3 600 s [lu, `.../data-push/price-feed-contract.md`] | cadence très lâche | non lue | TVWAP déclaré, sources non nommées [lu, `.../data-service/data-serivce.md`] | non sondé ; cadence trop lâche pour un pas de 60 s |
| **Switchboard** | instance publique « Crossbar » documentée, « best-effort », « rate-limited by IP » [lu, `docs.switchboard.xyz/tooling/crossbar.md`] ; **hôte inaccessible depuis ce poste** (502 du proxy, politique ou panne) [manque] ; flux définis par chaque propriétaire (jobs), pas de BTC/USD canonique [inféré] | | | définis par les jobs du flux | non sondé ; écarté |
| **Chronicle** | lecture protégée : “Functions to read the oracle's value are protected via chronicle-std's Toll module” [lu, `raw.githubusercontent.com/chronicleprotocol/scribe/main/docs/Scribe.md` l.29] ; licence **BUSL-1.1** [lu, README du dépôt] ; docs `docs.chroniclelabs.org` : défi Vercel (429) [manque] | | BUSL-1.1 | non lus | écarté sur pièce (accès par liste ; la possibilité d'un appel depuis une adresse non listée n'est pas établie) |
| **API3** | feeds par **plan acheté** : « API3 Market only offers a 24-hour heartbeat interval » ; plans de 3 mois sur mainnet [lu, `docs.api3.org/dapps/integration/index.html`] | heartbeat 24 h | | premier niveau (API) non lu | écarté : pas de flux public garanti |
| **Tellor** | BTC/USD « Market: A median of market prices from exchange APIs » [lu, `docs.tellor.io/.../production-spot-price-list.md`] ; relais on-chain à la demande ; exemple de garde « at least 12 hours without being disputed » [lu, `.../integrating-tellor-data.md`] | latence de dispute de l'ordre de 12 h | | exchanges | écarté (latence) |
| **UMA** | oracle optimiste de requêtes discrètes : « optimistic oracle that resolves wide-ranging requests for information » [lu, `docs.uma.xyz/protocol-overview/how-does-umas-oracle-work.md`] | | | | **pas un flux de prix** ; écarté (nature) |
| **Umbrella, Razor** | sites bloqués par Cloudflare (403, « You have been blocked ») [manque] | | | | maturité et lecture non établies |
| **Flux** | hôte inaccessible (échec TLS) [manque] | | | | non établi |
| **Orochi** | site lu ; « Orocle : the decentralized oracle for verifiable off-chain data » [lu, `orochi.network`] ; pas de flux BTC/USD documenté dans les pages lues [abs] | | | | non établi |
| **Hyperlane** | voir §1 | | | | pas un oracle de prix |

Les identifiants de la liste CoinGecko (environ 45 sur 62) non nommés ci-dessus (WINkLink, Oraichain, Phala, XYO, iExec, zkPass, Kleros, Augur, Charli3, Gora, Modefi, PureFi, HAPI, Plugin, Integritee, Unmarshal,
Kaiko-jeton, etc.) **ne sont pas examinés** dans cette passe (temps, et aucun n'est cité par le brief) [abs]. La liste mêle des oracles de prix, des réseaux de vérification de données, des marchés de prédiction
et des jetons génériques (par exemple `2027-token`, `company`, `peak`) [inféré, à la lecture des identifiants] : l'appartenance à la catégorie n'est pas un critère de « source de prix ».

### 2.4 Place décentralisée lisible par RPC (état d'un pool Uniswap v3)

Méthode [sonde, 04:43:35–04:43:57Z] : `eth_call` sur la fabrique Uniswap v3 `getPool(WBTC, USDC, frais)`, vérification `token0()`/`token1()` du pool, puis `slot0()` (`sqrtPriceX96`) et `liquidity()` ;
prix = (sqrtP / 2^96)² × 10^(8−6) ; horodatage = bloc `latest` (`eth_getBlockByNumber`). Les adresses de fabrique et de jetons viennent de ma mémoire et sont **vérifiées par les réponses des contrats** (les pools
renvoyés portent bien les bons `token0`/`token1`), pas par une page primaire lue (page de déploiement Uniswap non lue : manque).

| réseau, RPC | pool | prix lu (BTC en USDC) | bloc, horodatage | liquidité (unités de L) |
|---|---|---|---|---|
| Ethereum, `mainnet.gateway.tenderly.co` | WBTC/USDC 0,05 % `0x9a772018…7d16` | 84 785,64 | 26 116 674, 04:43:35Z | 3,37·10¹⁰ |
| Ethereum | WBTC/USDC 0,3 % `0x99ac8ca7…bc35` | 84 769,98 | idem | 2,11·10¹² |
| Arbitrum, `arb1.arbitrum.io/rpc` | WBTC/USDC 0,05 % `0x0e483131…b44f` | 84 794,53 | 511 511 881, 04:43:51Z | 2,38·10¹² |
| Base, `mainnet.base.org` | cbBTC/USDC 0,05 % `0xfbb6eed8…43ef` | 84 824,05 | 52 149 844, 04:43:55Z | 2,33·10¹² |

Réserves : (i) l'actif n'est pas BTC/USD mais WBTC (ou cbBTC) contre **USDC** : deux wrappers, la devise de cotation est un champ du relevé (doc 10 §2) [inféré, lecture de doc 10] ; (ii) `slot0` est un prix
instantané manipulable dans le bloc ; la moyenne temporelle (`observe`) n'a pas été sondée [abs] ; (iii) l'horodatage est celui du bloc, pas de la dernière transaction du pool ; (iv) l'amont est la
suite des échanges du pool, **une racine d'un type nouveau** (état de marché on-chain), que Chainlink (« DEX pool state data ») et RedStone (« 50 on-chain trading protocol deployments ») consomment aussi [lu, données ci-dessus]. Coût : lecture gratuite ;
RPC testés : voir §4.2.

---

## 3. Ce que chaque ajout apporte à la mesure (racine, ASN, k nominal, coût)

Racines d'amont du pool actuel [lu, doc 10 §3.2 et ADR-0029 §2.5] : 7 places primaires (Binance, Coinbase, Kraken, OKX, Bitstamp, Gemini, Bitfinex) ; coingecko = f(tickers de places) ; defillama = f(coingecko)
(un seul chemin d'amont pour BTC) ; chainlink = f(agrégateurs/fournisseurs, catégorie documentée aujourd'hui, noms non donnés). k nominal = 10 (hôtes), k_eff mesuré = 4 (7 hôtes sur AS13335) [lu, doc 11 §4 et ADR-0029 §1.1].

| ajout | nouvelle racine ? | copie de racine déjà au pool ? | ASN (nouveau pour le pool ?) | effet sur k nominal | coût (lecture, limites, volume) |
|---|---|---|---|---|---|
| Bitget, KuCoin, Crypto.com, Bitso | **oui**, une racine chacune (carnet propre) | non | AS13335 (déjà là) | +1 chacun | une requête de ~0,4 Ko par minute ; limites non lues (sauf à lire) |
| HTX, Upbit (USDT-BTC), Gate | oui | non | AS16509 (déjà là) | +1 chacun | idem ; Gate et MEXC sans horodatage : axe staleness aveugle (comme Binance, Kraken, Bitfinex en S2) |
| **MEXC** | oui | non | **AS20940 Akamai (nouveau)** | +1 | idem ; seul à faire monter k_eff sur l'axe ASN parmi les places |
| Bybit | oui | non | AS16509 | +1 | **inaccessible depuis ce point (403)**, dépend du smoke de chaque observateur |
| Hyperliquid (oracle) | non : f(Binance, OKX, Kraken + Bybit, KuCoin, Gate, MEXC) | **oui**, 3 des 7 places du pool + 4 candidates | AS16509 (CloudFront), déjà là | +1 | 72 Ko par lecture (≈ 104 Mo/jour/observateur en octets bruts), 1 lecture/min = 20 de poids sur 1 200/min |
| dYdX (oracle natif) | non | oui (Binance, Bitfinex, Bitstamp, Coinbase …) | AS13335 | +1 | 0,6 Ko ; pas d'horodatage |
| DIA | **inconnu** (« direct exchange sourcing ») | probablement des places du pool [inféré] | AS16509 (AWS eu-west-1) | +1 | 0,3 Ko ; limites et licence non lues |
| RedStone, contrat Ethereum | non : places + DEX + agrégateurs | oui (Binance, Coinbase, OKX, Kraken) | dépend de l'hôte RPC choisi | +1 | 1 `eth_call` ; mise à jour de ≈ 43 min d'âge (paramètres non lus) |
| RedStone, passerelle | idem | idem | AS16509 (CloudFront) | +1 | **1,97 Mo par lecture, ≈ 2,8 Go/jour/observateur en octets bruts** [calc : 1 972 925 × 1 440], impraticable pour un journal d'octets bruts (ADR-0003/0005) |
| Uniswap v3, Ethereum (pool WBTC/USDC) | **oui, nouveau type** (état de marché on-chain) | non (les arbitres relient indirectement le prix aux places, [inféré]) | dépend de l'hôte RPC (Tenderly = **AS396982 Google Cloud, nouveau**) | +1 | 3-5 `eth_call` batchables en une requête ; RPC publics limités (429 vus) |
| Uniswap v3 sur L2 (Arbitrum, Base) | même type | **corrélé au pool Ethereum** par arbitrage [inféré] | RPC sur AS13335 | +1 si unité distincte, mais redondant | idem |
| Chainlink sur une autre chaîne | non | oui (même fournisseur ; réseau d'opérateurs séparé non établi) | selon RPC | 0 à +1 | à éviter comme « nouvelle unité » |
| CoinPaprika | non : VWAP de places | oui (copie de la famille places, comme CoinGecko) | AS13335 | +1 nominal, 0 en racines | **licence : redistribution réservée à l'offre Enterprise**, résolution de 10 min en offre libre ; recommandation : écarter |
| Coinlore | non | oui | AS13335 | idem | sans horodatage, licence non lue ; écarter |
| Coinbase v2 « spot » | non | **oui (Coinbase)** | AS13335 | 0 en racines | doublon, à écarter |

Notes :

- **Une unité on-chain = un hôte RPC.** ADR-0029 §2.5 fait de l'unité le nom d'hôte de configuration (« hôte = nom d'hôte de configuration », Chainlink = `ethereum-rpc.publicnode.com`) parce que deux flux d'un même hôte
  partagent transport, DNS et TLS [lu, l.139]. Appliqué aux ajouts on-chain, **chaque flux lu par RPC doit passer par son propre hôte RPC**, sinon deux feeds (Chainlink + RedStone + Uniswap) se confondent en une seule unité
  ou deviennent dépendants par construction [inféré]. RPC publics qui ont répondu sans clé le 2026-10-04 : `ethereum-rpc.publicnode.com`, `eth.drpc.org`, `rpc.mevblocker.io`, `eth-mainnet.public.blastapi.io`
  (tous AS13335), `mainnet.gateway.tenderly.co` et `gateway.tenderly.co` (AS396982 Google Cloud) ; refus ou limite : `rpc.ankr.com` (clé), `1rpc.io` (plafond), `eth.merkle.io` et `eth.api.onfinality.io` (429),
  `eth.llamarpc.com` (525), `cloudflare-eth.com` (erreur −32603, comme en doc 10 §3.2), `rpc.flashbots.net` (méthode non autorisée), `endpoints.omniatech.io` et `ethereum.blockpi.network` (521) [sonde 04:42Z].
  Le gain d'ASN d'une lecture Chainlink via Tenderly (GCP) au lieu de PublicNode (Cloudflare) serait, si l'on déplaçait l'hôte, de sortir cette unité du bloc de 7 [inféré] ; cela change l'unité par rapport à S2 (même nom d'hôte
  qu'en S2 = continuité) et est une décision, pas un correctif.
- **Le plafond de k_eff sur l'axe ASN est structurel** : sur les 28 hôtes que j'ai mesurés (pool actuel, candidats, RPC), les ASN rencontrés sont AS13335 (16 hôtes), AS16509 (8), AS396982 (2), AS20940 (1), AS24940 (1) [calc sur `asn-results-*.json`]. Un pool de 25 unités choisies parmi les meilleurs candidats **ne dépasserait guère 6 à 7 classes** sur cet axe, quel que soit le nombre d'unités [inféré]. Le message produit à porter est donc
  « les amonts sont distincts *et* la livraison est concentrée chez deux fournisseurs », ce que la mesure montre déjà.

---

## 4. Hébergeur et ASN : mesure rejouable de ce jour

Commande rejouable : `python3 pool-bis/asn.py <hôte> …` (résolveurs DoH `cloudflare-dns.com` et `dns.google` : deux familles ; RIPEstat `prefix-overview` ; Team Cymru par requête TXT `origin.asn.cymru.com` en DoH).
Concordance RIPEstat = Cymru : toutes les IP lues (premières deux IP par hôte). Les deux résolveurs ont renvoyé le même jeu d'IP pour la moitié des hôtes (jeux d'IP tournants pour les autres) ; l'ASN n'en diffère jamais.

Résultats du 2026-10-04 ~04:36-04:49Z (28 hôtes) (`pool-bis/asn-batch1.txt`, `asn-batch2.txt`, `asn-results-*.json`) :

| ASN | hôtes mesurés |
|---|---|
| AS13335 Cloudflare | `api.bitget.com`, `api.kucoin.com`, `api.crypto.com`, `api.bitso.com`, `api.coinpaprika.com`, `api.coinlore.net`, `blockchain.info`, `api.coinbase.com`, `indexer.dydx.trade`, `ethereum-rpc.publicnode.com`, `api.coingecko.com`, `eth.drpc.org`, `rpc.mevblocker.io`, `eth-mainnet.public.blastapi.io`, `arb1.arbitrum.io`, `mainnet.base.org` |
| AS16509 Amazon | `api.diadata.org` (ELB eu-west-1), `oracle-gateway-1.a.redstone.finance` (CloudFront), `api.hyperliquid.xyz` (CloudFront), `api.upbit.com`, `api.gateio.ws`, `api.huobi.pro` (CloudFront), `api.bybit.com` (CloudFront), `api.binance.com` (CloudFront) |
| AS20940 Akamai | `api.mexc.com` |
| AS24940 Hetzner | `laozi1.bandchain.org` |
| AS396982 Google Cloud | `mainnet.gateway.tenderly.co`, `gateway.tenderly.co` |

Résidus (ceux de doc 10 §4.1, inchangés) : fronting CDN (l'ASN est celui de la livraison, pas de l'origine) ; mono-vantage ; instantané daté ; mon chemin de mesure passe par des résolveurs Cloudflare et Google (un des deux est Cloudflare, résidu 5).
Cette mesure **n'est pas** l'enquête ASN du harnais S2-bis, qui se fait depuis chaque observateur sur les adresses réelles (ADR-0029 §2.1).

---

## 5. Qui l'usage réel cite le plus, et quelles copies

Sourçage : bon pour les oracles (en seconde main), mince pour les places (classement CoinGecko), **absent pour les agrégateurs**.

- **Oracles** : « Chainlink ~33 Md$ de TVS sur ~505 protocoles (part estimée 60-70 % selon les sources), mais Chronicle ~7,5 Md$, RedStone ~3,6 Md$, Pyth ~3,1 Md$ » [2nd, `docs/07-gtm.md` l.44-49, relevé web du 2026-07-30 par une passe antérieure].
  Je n'ai pas pu re-lire de source primaire de parts de marché : `api.llama.fi/oracles` est payant (402) et `defillama.com/oracles` est derrière un défi Cloudflare (403) [manque]. Autres chiffres lus, déclaratifs du fournisseur :
  RedStone « 200+ protocols across 110+ chains » [lu, `redstone.finance`, 04:40Z] ; un billet comparatif de RedStone (partie intéressée) : « securing over $10 billion in TVL » [lu, `blog.redstone.finance/2026/03/30/…`]. Ordre d'usage = Chainlink ≫ Chronicle,
  RedStone, Pyth. **Parmi eux, seul Chainlink est lisible sans clé de façon établie, RedStone par contrat avec réserves, Pyth et Chronicle non.** Conclusion d'ingénierie : l'oracle le plus utilisé est déjà au pool ; les suivants sont soit fermés, soit
  en accès conditionnel. Un ajout d'« oracle » ne ressemblera donc pas à la part de marché.
- **Places** : classement de confiance CoinGecko (source : l'API publique, 04:48Z) : 1 Binance, 2 Coinbase (`gdax`), 3 Kraken, 4 OKX, 5 Gate, 6 Bitget, 7 Bitstamp, 8 MEXC, 9 Crypto.com, 10 Bybit, 11 KuCoin, 16 Gemini, 27 Bitso, 30 Upbit,
  35 Bitfinex, 56 HTX. Le pool contient 5 des 7 premières places plus Gemini et Bitfinex ; il **manque Gate, Bitget, MEXC, Crypto.com, Bybit, KuCoin**. Hyperliquid cite lui-même sept places comme amonts (Binance, OKX, Bybit,
  Kraken, KuCoin, Gate, MEXC), dYdX et RedStone des listes voisines : les places « les plus utilisées » sont aussi celles qui alimentent les oracles [lu].
- **Agrégateurs** : aucune part de marché ni valeur sécurisée établie sur pièce [abs]. Ceux qui exigent une clé (CoinMarketCap, Kaiko, CoinAPI, CryptoCompare/CoinDesk, Messari) sont **hors invariant**. Ceux qui sont lisibles (CoinGecko, CoinPaprika, Coinlore)
  sont tous des VWAP/médianes de places [lu] : **copies de la famille places**, avec un trait de plus : leur fraîcheur est celle de leur propre cycle (10 min chez Paprika en offre libre).
- **Copies d'amonts déjà au pool** : Hyperliquid (3 places du pool), dYdX (Binance, Bitfinex, Bitstamp, Coinbase), RedStone (Binance, Coinbase, OKX, Kraken), Coinbase v2 (Coinbase), CoinPaprika/Coinlore (places agrégées), DefiLlama (CoinGecko, déjà).
  Racines **non** couvertes par le pool : places Gate/Bitget/MEXC/Crypto.com/Bybit/KuCoin/HTX/Upbit/Bitso ; état on-chain de DEX ; DIA (inconnue).

---

## 6. Faut-il élargir, comment, pourquoi, qu'est-ce que cela apporterait

**Pourquoi (le but produit : usage dans la DeFi, les agents, les acteurs du marché).** Le certificat dit « vos N sources cachent k racines ». Sa crédibilité dépend de ce que le pool contient
**ce que les clients lisent vraiment** : les grandes places, les oracles (Chainlink, RedStone, Pyth, Chronicle, Hyperliquid), les agrégateurs, et des lectures on-chain. Un pool à 7 places + 3 copies est un bon
banc d'essai (S2 l'a montré : 7 hôtes sur 10 derrière Cloudflare), pas une carte du marché. Aussi : le pool de S2-bis sera le seul à passer le sceau ; ce qu'on n'y met pas ne sera pas mesuré avant longtemps.

**Mais la décision R1 de S2-bis a ses propres contraintes** : (i) le pool est fixé ex ante et scellé ; (ii) τ et σ par classe sont re-dérivés **sur les données de S2** (ADR-0029 §2.6 : « Re-dérivation sur S2, scellée pour S2-bis »),
or **aucune source nouvelle n'a de donnée de S2** : il faudrait une calibration (type rodage, fenêtres exclues de l'inférence) ou des valeurs de classe écrites à l'avance [inféré] ; (iii) la puissance du §2.4(d) est simulée pour 10 unités
dont « 7 hôtes AS13335 » touchés avec probabilité 0,7 par un incident commun [lu, ADR-0029 l.120, l.133] : changer la composition **change la cellule cible** et exige de rejouer SIM-NIVEAU-BIS / SIM-PUISSANCE-BIS avant le sceau.

**Comment (deux voies, au choix de l'investisseur, non tranchées ici).**

- **Voie A, ajouts mesurés dans S2-bis (5 unités au plus)** : choisir des unités à racine nouvelle, lecture documentée sans clé, horodatage porté, licence lue. Ordre proposé ci-dessous.
- **Voie B, S2-bis inchangé à 10 unités + cartographie descriptive parallèle de tout le reste** : lectures des 15 à 25 sources supplémentaires sur les mêmes observateurs, **hors du vote R1**, avec les axes R2 (ASN, corrélation de contenu) et un
  rapport descriptif. Elle sert le produit (la carte du marché) sans toucher à la décision confirmatoire. Coût marginal : des requêtes, pas d'inférence nouvelle [inféré]. C'est la voie qui protège le plus le calendrier scellé.

**Ce que cela apporterait.** À l'axe contenu : de nouvelles racines (places non encore au pool ; un état de marché DEX) donnent à R1/R2 des paires dont l'indépendance n'est pas acquise d'avance, donc de vrais tests de dépendance (Hyperliquid, dYdX, RedStone
ressemblent à des copies de places : les mesurer est exactement l'objet du certificat). À l'axe ASN : presque rien (§3). À la puissance : voir §7.

### 6.1 Liste ordonnée d'ajouts pour S2-bis (voie A) et ce qu'il faut écrire au paquet

Critère d'ordre : racine nouvelle, lecture documentée sans clé, horodatage, licence lisible, accessible depuis des observateurs hors États-Unis.

1. **Crypto.com `BTC_USD`** (USD natif, horodatage, rang 9, Cloudflare). Licence à lire.
2. **Bitget `BTCUSDT`** (horodatage, rang 6, Cloudflare).
3. **KuCoin `BTC-USDT`** (horodatage, rang 11, Cloudflare).
4. **HTX `btcusdt`** (horodatage, rang 56, Amazon/CloudFront) ; **MEXC `BTCUSDT`** (pas d'horodatage ; mais seul hôte Akamai : utile à l'axe ASN).
5. **Uniswap v3 Ethereum WBTC/USDC 0,3 % via un hôte RPC distinct de celui de Chainlink** (ex. Tenderly, AS396982) : seule famille nouvelle ; à réserver à une lecture `observe` (moyenne) si l'on veut limiter la manipulabilité ; devise (USDC) et enveloppe (WBTC) à enregistrer au relevé.
6. **DIA `quotation/BTC`** : sous condition de lire licence et limites (docs derrière un défi Cloudflare ; essayer un second chemin primaire, par exemple le dépôt GitHub de DIA ou un contact) avant tout ajout.
7. **Hyperliquid `oraclePx`** : à ajouter comme « oracle natif de L1 », **pas** comme racine neuve ; sans horodatage, donc mêmes limites que Binance/Kraken (axe staleness aveugle).

À **écarter** (motif) : Pyth (clé et contrat on-chain figé au 2026-07-23, §2.3), Chronicle (accès par liste, BUSL-1.1), API3 (plan acheté), Supra, SEDA, APRO (clé ou cadence 24 h à 180 j), Band (aucune lecture fraîche établie),
Tellor (latence de dispute), UMA (pas un flux), Hyperlane (pas un oracle de prix), CoinMarketCap, Kaiko, CoinAPI, CryptoCompare/CoinDesk Data, Messari (clé), CF Benchmarks BRR (quotidien, licence), CoinPaprika (redistribution Enterprise),
Coinlore, Blockchain.com, Coinbase v2 (doublon ou sans horodatage ni licence), RedStone passerelle (clé documentée, 1,97 Mo par lecture), Upbit KRW (hors classe), Bitso (marché de 4,24 BTC/24 h : bruit), Chainlink sur une autre chaîne (pas de racine neuve).
**Réservé** : Bybit (bloqué depuis ce point, tranche au smoke des observateurs), RedStone contrat Ethereum (adresse à confirmer sur une page primaire, paramètres de mise à jour à lire).

Ce qu'il faut écrire au paquet (si voie A) [inféré] : (a) critères d'entrée explicites de la liste (C1 lecture documentée sans clé, C2 BTC/USD ou devise marquée, C3 horodatage ou drapeau « sans horodatage », C4 licence compatible avec la publication d'octets
bruts, C5 amonts déclarés, C6 ASN mesuré à l'observateur, C7 lecture réussie depuis les quatre observateurs) ; (b) la famille de chaque unité (place, agrégateur, oracle, DEX) pour une lecture stratifiée ; (c) la règle « une unité on-chain = un hôte RPC »
et la liste des hôtes RPC ; (d) τ_c et σ_c de chaque nouvelle classe, avec la méthode (calibration exclue de l'inférence) ; (e) la cellule cible recalculée ; (f) l'hôte de chaque unité inscrit comme nom, jamais comme adresse (règle existante).

### 6.2 À re-mesurer à l'aveugle avant le sceau

- Chaque nouvel endpoint : HTTP, valeur, horodatage, devise, depuis **chacun des quatre observateurs** (smoke, ADR-0029 §2.1) : Bybit et Binance bloquent selon la juridiction ; Binance 451 vu depuis ce point.
- Les ASN de chaque hôte ajouté, depuis l'observateur (ADR-0029 §2.1).
- Licence et limites lues sur pièce : Crypto.com, Bitget, KuCoin, HTX, MEXC, DIA, Hyperliquid (la limite est lue, la licence non), Uniswap (rien à lire : lecture de chaîne).
- Pour les lectures on-chain : adresse du contrat sur une page primaire (RedStone, Uniswap), décodage et fixtures, rafraîchissement (`updatedAt` vs fenêtre), hôte RPC, comportement 429.
- La puissance (SIM) pour la nouvelle composition.

---

## 7. Taille du pool : 15, 20 ou 25 unités

Sources : ADR-0029 §2.4 (puissance), §2.5 (pool), §2.6 (τ, σ), §2.9 (collecte) ; doc 10 §3.3.

- **Paires** [calc] : N(N−1)/2 : 10 → 45 (déjà dans l'ADR « 45 paires au lieu de 55 »), 15 → 105, 20 → 190, 25 → 300.
- **Puissance** (qualitatif) : la statistique de décision est K = nombre de fenêtres avec au moins deux écarts parmi N unités [lu, ADR-0029 l.97], non une moyenne de paires. La formule du §2.4(a) donne
  n ∝ (1+λ)(1−(1+λ)P)/(λ² P) [lu, l.99] : à excès relatif λ et FIV fixés, **n décroît quand P (la fréquence de fenêtres à ≥ 2 écarts) augmente**, et P croît avec le nombre de paires d'unités bruyantes [inféré]. Plus d'unités peut donc
  réduire le nombre de fenêtres nécessaires, **à condition** que (i) l'excès λ à la cellule cible soit défini sur la nouvelle composition (la cible actuelle est « chacun des 7 hôtes AS13335 avec probabilité 0,7 » [lu, l.133]),
  (ii) le FIV de série et la garde §5.4 tiennent encore (la garde échoue déjà dans 62 à 100 % des réplications de A et B à 8 et 12 semaines [lu, l.131]), (iii) les nouvelles unités ne sont pas des quasi-copies (Hyperliquid, dYdX, RedStone, CoinPaprika) qui
  crée des co-écarts réels : cela **améliore la sensibilité à une dépendance vraie mais déplace l'hypothèse nulle** (indépendance des unités) pour la rotation [inféré]. Les unités sans horodatage (Gate, MEXC, Hyperliquid, dYdX) laissent l'axe staleness aveugle (même résidu qu'en S2). Aucun chiffre de puissance n'est donné ici : il faut rejouer SIM-PUISSANCE-BIS.
- **Limites de débit avec 4 observateurs** : les limites lues sont **par IP** (Hyperliquid 1 200 de poids/min/IP ; Upbit 10 req/s/IP ; CoinPaprika 10 req/s/IP ; Coinlore ~1 req/s recommandé) [lu] ; chaque observateur est un VPS distinct, donc les quatre quotas sont indépendants [inféré, ADR-0029 §2.1].
  Cible de conception : « 1 relevé/source/fenêtre, fenêtre ≥ 60 s → ~1 req/min/source » [lu, doc 10 §3.3] ; N = 25 unités donne donc 25 requêtes par minute par observateur (≈ 0,4 req/s), 100 par minute au total. Les points durs sont : les RPC publics
  (429 sur deux des dix-huit essayés, un plafond d'usage sur un, un refus par clé sur un autre), à regrouper par lot JSON-RPC ; CoinGecko (déjà « not suitable for scheduled polling », doc 10 §3.3) ; Hyperliquid (poids 20 par lecture, 1,7 % du budget). Les limites des places candidates sont, pour la plupart,
  non lues [abs] : à lire avant l'ajout.
- **Volume de journal** (octets bruts conservés, ADR-0003/0005) [calc] : places et DEX ≈ 0,3 à 0,6 Ko par lecture ; Hyperliquid 72 Ko ; RedStone passerelle 1,97 Mo (rédhibitoire) ; vingt-cinq unités à ≈ 1 Ko donnent ≈ 36 Mo/jour/observateur hors Hyperliquid.
- **Complexité d'exploitation** [inféré] : chaque unité apporte un décodeur et ses fixtures (relus G2), un smoke par observateur, une règle de statut (devise, horodatage, `ok`/`panne`), un τ et un σ, une mesure ASN, une page de licence, une surveillance. À 10 unités, la réécriture de la collecte (§2.9) est un lot ; à
  20 et 25, la charge de G2 et de maintenance des décodeurs (formats propres à chaque API : par exemple, Upbit renvoie des nombres JSON non cités, Bitfinex 11 champs pour un schéma de 10 en doc 10 §3.1) croît linéairement, mais **les dépendances à un tiers fragile croissent aussi** (un hôte qui change de licence, ou
  qui passe à la clé comme Pyth le 2026-08-26 [lu, ADR-0023]). Chaque retrait ex ante (D1-bis, ADR-0029 §2.5) protège la décision, au prix d'un n′ par strate variable. Recommandation d'ingénierie : **15 est gérable dans le calendrier de S2-bis ; 20 et 25 relèvent de la voie B (cartographie descriptive)**.

---

## 8. Limites, manques et ce qui reste

- **Pages refusées ou inaccessibles (aucune contournée)** : `docs.diadata.org` (défi Cloudflare, 403) ; `docs.chroniclelabs.org` (défi Vercel, 429) ; `www.umb.network`, `razor.network` et `docs.razor.network` (Cloudflare, « blocked ») ;
  `docs.umb.network`, `crossbar.switchboard.xyz`, `api.umbrellanet.io`, `api.tellor.io`, `rest.laozi1.bandchain.org` (502 du proxy sortant, politique ou panne ; non diagnostiqué) ; `fluxprotocol.org` (échec TLS) ; `defillama.com/oracles` (403) et `api.llama.fi/oracles` (402) ;
  `www.gate.com/docs` (403) ; `api.github.com` et pages `github.com` (403 du proxy : « access … not enabled ») ; les pages de licence des places et d'Uniswap n'ont pas été lues.
- **Non examiné** : environ 45 identifiants de la liste CoinGecko non nommés (§2.3) ; l'ensemble des conditions de licence des places ; la moyenne `observe` d'Uniswap ; les contrats on-chain de Supra, APRO, Switchboard, Band, Chronicle ; les paramètres de mise à jour du feed RedStone ;
  les noms des agrégateurs consommés par Chainlink.
- **Mono-vantage** : toutes les sondes viennent d'un seul poste (cloud Anthropic), dont l'accès est restreint pour Binance (451) et Bybit (403).
- **Adresses de contrat non issues de pages primaires lues** : RedStone BTC Ethereum, Pyth Ethereum, fabrique et jetons Uniswap ; elles sont vérifiées par les réponses mêmes des contrats (`description()`, `token0/1`), pas par une page.
- **Contradiction relevée** : la passerelle RedStone répond sans clé alors que la documentation en exige une (§2.3) : cas à ne pas fonder.
- **Écart avec ADR-0029 §2.5** : la réintégration de Pyth « par lecture sur chaîne sans clé » (voie B′) demande un « flux BTC/USD lisible sans clé, cadence documentée » ; la sonde du contrat Ethereum de Pyth le 2026-10-04 montre une valeur de 73 jours : la condition n'est pas remplie sur cette chaîne.
- **Chiffres calculés ici (non lus)** : tous les [calc] sont rejouables à partir des fichiers cités.

## 9. Fichiers produits (tous sous `pool-bis/`)

`RAPPORT-POOL-BIS.md` (ce rapport) ; `probes/*.body|*.hdr` et `probe-log.txt` (sondes) ; `web/*` (copies des pages, `fetch-log.txt`) ; `asn.py`, `asn-batch1.txt`, `asn-batch2.txt`, `asn-results-*.json` ;
`rpc.py`, `univ3.py` (lecture on-chain) ; `fetch.sh`, `probe.sh`, `refetch.py` (outils).
