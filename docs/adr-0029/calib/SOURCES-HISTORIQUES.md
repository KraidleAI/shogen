# CALIB-ACTIFS-G0 — sources d'historiques à une minute pour ETH/USD, USDC/USD, USDT/USD (BTC/USD pour mémoire)

**Gate 0** : modèle résolu `claude-sonnet-5-5` (identifiant donné par l'environnement), effort `high`.
**Brief** : `/tmp/claude-0/-home-user-shogen/7ba84933-ba6d-5813-9ef4-ca3ac4febd16/scratchpad/s2bis/calib/BRIEF-CALIB-SOURCES.md`, sha256 `4a0364f1d78947c9b232aec1a61f58d6ac2d7ac8690c6d480af1d69b22072f68` (recalculé, identique).
**Dates** : toutes les lectures du **2026-10-04, 13:23 à 13:40 UTC** (`date -u`). Aucune opération git, aucune écriture hors du dossier `calib/`, aucune clé, aucun compte, aucune dépense.
**Outils** : `curl` seul. `ToolSearch` est désactivé dans cette session : ni WebFetch ni Firecrawl n'ont pu être utilisés (limite rendue, voir §6).
**Pièces du dépôt lues** : ADR-0029 r3 §2.5 et §2.6, `G0-lots-S2BIS.md`, `DECISIONS-ARCHITECTURE-S2BIS.md` (D-4), `AVIS-QUESTIONS-TECHNIQUES-V3.md`, `ETUDE-POOL-BIS.md`. Aucune pièce interdite ouverte, aucun `*.jsonl`, aucun journal de campagne.
**Niveaux** : [lu] lu sur place (URL, date) ; [mesuré] requête réelle de cette passe ; [abs] absent ou non lisible ; [inféré] déduction de l'auteur. Citations web entre “ ” (jamais « »), 25 mots au plus, page = URL (ou page du PDF).
**Ce qui n'est PAS fait** : aucun τ, aucun P99,9, aucune grille. L'ADR §2.6 les réserve au G0, avant tout calcul ; je n'ai calculé que des comptes de disponibilité.

---

## 1. Résultat en une page

| Classe | Places du pool de l'ADR avec un historique 1 min, gratuit, sans clé, avant S2 | ≥ 4 places ? (lecture « disponibilité ») | ≥ 4 places ? (lecture « republication des octets bruts permise ») |
|---|---|---|---|
| **ETH/USD** | **6** : Coinbase, Kraken, Bitstamp, Bitfinex (USD fiat, profonds) + Binance (ETHUSDT) + OKX (ETH-USDT). Gemini : non. | **OUI** (4 en USD fiat pur) | **NON** (permission explicite lue : Binance sous CC BY-NC-SA, Bitstamp sous contrat signé ; les autres : interdit ou non lu) |
| **USDC/USD** | **4 exactement** : Binance (depuis 2025-11 seulement), Kraken, Bitstamp (très mince), Bitfinex (très mince). Coinbase, OKX, Gemini : non. | **OUI, sans aucune marge** (4 sur 4) ; une seule place retirée et la classe tombe à 3 | **NON** |
| **USDT/USD** | **6** : Binance (depuis 2025-11), Coinbase (≈ 2021-05), Kraken, Bitstamp (mince), Bitfinex, OKX (depuis 2024-12). Gemini : non. | **OUI** (5 sans Bitstamp) | **NON** |
| BTC/USD (mémoire) | 6 : Coinbase, Kraken, Bitstamp, Bitfinex, Binance (BTCUSDT), OKX (BTC-USDT). Gemini : non. | OUI | NON |

Points à retenir :

1. **La condition « ≥ 4 places » se lit vraie pour ETH et USDT, et vraie sans marge pour USDC** [lu + mesuré]. Pour USDC, seules 76 minutes sur 10 080 d'une semaine de juin 2026 ont les 4 places actives en même temps (0,8 %) [mesuré, §4].
2. **Aucun historique n'est publié avec une licence qui autorise sans condition la republication des octets bruts** [lu]. Seul Bitstamp écrit que la redistribution est permise, et sous un contrat commercial signé. Binance est en CC BY-NC-SA (non commercial). Coinbase, Bitfinex, Gemini : conditions non lisibles ici [abs].
3. **Gemini n'a aucun historique 1 min utile** : l'API rend les 24 dernières heures seulement [mesuré].
4. **Kraken s'arrête au 2026-06-30** (archive trimestrielle ; le fichier du 3e trimestre n'existe pas encore, 404) : il ne couvre donc pas septembre 2026, mais couvre largement l'avant [lu + mesuré].

---

## 2. Pool de l'ADR (rappel)

Pool BTC (ADR-0029 §2.5) : binance, coinbase, kraken, okx, bitstamp, gemini, bitfinex (7 places), plus coingecko, defillama (agrégateurs) et chainlink (oracle) [lu, ADR-0029 §2.5]. Les pools d'ETH, USDC, USDT sont « pris parmi les hôtes de BTC » [lu, §2.5]. Les agrégateurs et l'oracle n'ont pas de bougies : seules les 7 places comptent pour la condition. Bybit (non au pool) est traité en annexe (§5) et **n'est pas compté**.

---

## 3. Tableau par classe et par place

Légende : « USD fiat » = paire cotée en dollar ; « USDT » = cotée en tether. Échantillons : fichiers dans `samples/`, sha256 complets au §7 et dans `SHA256SUMS-ECHANTILLONS.txt`.

### 3.1 ETH/USD

| Place | Paire exacte et URL exacte lue | Format | Profondeur | Couvre sept. 2026 ? | Accès | Licence / republication | Échantillon (lignes) |
|---|---|---|---|---|---|---|---|
| **Binance** | `ETHUSDT` (USDT) : `https://data.binance.vision/data/spot/monthly/klines/ETHUSDT/1m/ETHUSDT-1m-2026-08.zip` ; `ETHUSD` (USD fiat, `quoteAsset":"USD"`, `TRADING` [lu, `data-api.binance.vision/api/v3/exchangeInfo?symbol=ETHUSD`]) : `…/ETHUSD/1m/ETHUSD-1m-2026-08.zip` | Zip de CSV sans en-tête, 12 colonnes (ouverture, haut, bas, clôture, volume, …), temps en **microsecondes** depuis 2025 [lu, README binance-public-data] | ETHUSDT : 2017-08 à 2026-08 mensuel (218 clés dont sommes de contrôle) ; **ETHUSD : 2026-03 à 2026-08 seulement** [mesuré, liste S3] | **Oui** : fichiers quotidiens jusqu'au 2026-10-03 ; `ETHUSDT-1m-2026-09-15.zip` répond 200 [mesuré] | Libre, sans clé, S3 public [mesuré] | **CC BY-NC-SA 4.0, non commercial** (voir §3.5) | ETHUSDT août 2026 : 44 640 lignes ; ETHUSD août 2026 : 44 640 lignes dont **90,2 % à volume nul** (40 272) [mesuré] |
| **Coinbase** | `ETH-USD` (USD fiat) : `https://api.exchange.coinbase.com/products/ETH-USD/candles?granularity=60&start=…&end=…` | JSON, tableaux `[temps, bas, haut, ouverture, clôture, volume]` (secondes) [mesuré] | 2016-05-30 → aujourd'hui (premier mois avec bougies, sondage par mois) [mesuré] ; 300 bougies max par requête : “The maximum number of data points for a single request is 300 candles.” [lu, `docs.cdp.coinbase.com/exchange/reference/exchangerestapi_getproductcandles`] | **Oui** | Sans clé ; 10 requêtes/s/IP [lu, `…/exchange/rest-api/rate-limits`] ; mais “Historical rates should not be polled frequently.” [lu, même page candles] | **Non lu** : `coinbase.com/legal/market_data_terms` et `…/exchange-api-terms` répondent 403 (défi Cloudflare) [mesuré] ; [abs] | 300 lignes (05 h le 2026-08-15) ; pas de bougie sans transaction : “No data is published for intervals where there are no ticks.” [lu, même page] |
| **Kraken** | `ETHUSD` (USD fiat ; paire `XETHZUSD` à l'API [mesuré, AssetPairs]) : fichier `ETHUSD_1.csv` dans `https://assets.kraken.com/marketing/institutions/Kraken_OHLCVT_2026Q2.zip` (538 MB, `Accept-Ranges`) [mesuré] | CSV sans en-tête `timestamp, open, high, low, close, volume, trades` (secondes) ; minutes sans échange **absentes** : “Only intervals in which trades occurred are included (gaps are not zero-filled).” [lu, `support.kraken.com/hc/en-us/articles/360047124832`, mis à jour le 2026-09-16] | Historique complet « de la première transaction » au 2026-06-30 : “each pair from its first trade on Kraken through 30 June 2026” [lu, même page] ; première transaction ETH/USD **2015-08-07** [mesuré, API `Trades since=0`] | **Non** : fin au 2026-06-30 ; `Kraken_OHLCVT_2026Q3.zip` : 404 le 2026-10-04 [mesuré]. L'API REST rend au plus 720 bougies récentes : “Returns up to 720 of the most recent entries” [lu, `docs.kraken.com/api/docs/rest-api/get-ohlc-data/`] | Sans clé ; téléchargement direct (lecture par plages d'octets possible [mesuré]) | Page de l'archive : aucune licence [abs]. CGU globales (mises à jour 2026-10-01) : “If you wish to use Our Content for any other purpose you must seek prior permission” [lu, `kraken.com/legal/global-terms`] ; extraction interdite : “use any web scraping, web harvesting, or data extraction methods to extract any data from Our Content” [lu, même page] ; que ces clauses visent l'archive est [inféré] | `ETHUSD_1.csv` du 2026-Q2 : 130 240 lignes (2026-04-01 → 2026-06-30) |
| **Bitstamp** | `ethusd` (USD fiat, `ETH/USD` `Enabled` [mesuré, `/api/v2/trading-pairs-info/`]) : `https://www.bitstamp.net/api/v2/ohlc/ethusd/?step=60&limit=1000&start=<epoch>` | JSON `{"data":{"ohlc":[{timestamp,open,high,low,close,volume}]}}` ; **minutes vides remplies** par report du dernier prix, volume 0 [mesuré] | Données au plus tard au 2017-09-01 [mesuré, sondage mensuel] ; 1000 bougies par requête [lu, `bitstamp.net/api/`] | **Oui** | Sans clé ; “400 requests per second”, plafond 10 000 requêtes/10 min [lu, `bitstamp.net/api/`] | **Lu et explicite** : “Bitstamp allows the incorporation and redistribution of our exchange data for commercial purposes.” et il faut “contact partners@bitstamp.net to receive and sign a commercial use Data License Agreement” [lu, `https://www.bitstamp.net/api/`]. Usage commercial = **contrat signé** ; la page `terms-of-use` n'a pas répondu (jeton Incapsula) [abs] | 1000 lignes (00:00-16:39 UTC le 2026-08-15) ; 162 à volume nul (16,2 %) |
| **Bitfinex** | `tETHUSD` (USD fiat ; `ETHUSD` dans `pub:list:pair:exchange` [mesuré]) : `https://api-pub.bitfinex.com/v2/candles/trade:1m:tETHUSD/hist?start=<ms>&end=<ms>&limit=10000&sort=1` | JSON `[MTS, OPEN, CLOSE, HIGH, LOW, VOLUME]` (ms) ; minutes sans échange absentes [mesuré] | Première bougie **2016-03-09** (`start=0`, tri croissant) [mesuré] ; “Number of records in response (max. 10000).” [lu, `docs.bitfinex.com/reference/rest-public-candles`] | **Oui** | Sans clé ; “Rate Limit: 30 reqs/min (requests per minute)” [lu, même page] | `bitfinex.com/legal/general/market-data/` (« Market Data Terms ») existe mais **le corps n'est pas dans la page servie** (rendu côté navigateur) [abs] ; rien lu sur la republication | 264 bougies (05 h le 2026-08-15) ; 9 571 bougies sur 10 080 minutes (2026-08-10 à 17) [mesuré] |
| **OKX** | `ETH-USDT` (USDT) : fichier mensuel `https://static.okx.com/cdn/okex/traderecords/candlesticks/monthly/202608/ETH-USDT-candlesticks-2026-08.zip` (lien obtenu par `GET /api/v5/public/market-data-history?module=2&instType=SPOT&…`, lu et exécuté) ; `ETH-USD` : même chemin, `…/ETH-USD-candlesticks-2026-08.zip` | Zip de CSV **avec en-tête** `instrument_name,open,high,low,close,vol,vol_ccy,vol_quote,open_time,confirm` (ms) [mesuré] ; module 2 = “1-minute candlestick” [lu, `okx.com/docs-v5/en/`] | ETH-USDT : **2021-01** à **2026-09** (69 fichiers) ; ETH-USD : **2024-12** à 2026-09 (22 fichiers) [mesuré] ; la page publique dit “Candlestick OHLC chart history from July 2023 onwards.” [lu, `okx.com/historical-data`] : **écart non résolu** avec les fichiers d'avant 2023-07 | **Oui** (fichier de septembre 2026 listé, disponible à T+2 [lu, docs]) | Sans clé ; limite 5 requêtes/2 s [lu, docs] | CGU (mises à jour 2026-09-17) : “You may not use the OKX Platform or the Services for any commercial purpose unless otherwise explicitly authorized by OKX.” [lu, `okx.com/help/terms-of-service`, art. 9.4] ; art. 8.1 interdit de “copy, transmit, distribute, sell, license” [lu] ; pas de licence de données propre à la page d'archive [abs] | ETH-USDT août 2026 : 44 640 lignes ; ETH-USD août 2026 : 44 640 lignes. **Réserve** : la paire `ETH-USD` n'existe pas dans `GET /api/v5/public/instruments?instType=SPOT` (seule `USDT-USD` est cotée en USD) ni au ticker (code 51001), alors que les fichiers existent [mesuré] : à confirmer avant de la compter |
| **Gemini** | `ethusd` : `https://api.gemini.com/v2/candles/ethusd/1m` | JSON `[ms, ouverture, haut, bas, clôture, volume]` | **24 heures seulement** : 1 440 bougies, de 2026-10-03 13:34 à 2026-10-04 13:33 ; les paramètres `timestamp`, `start/end`, `since` sont sans effet (toujours les 24 dernières heures) [mesuré] ; la doc ne dit pas la profondeur [abs, `docs.gemini.com/trading/rest-api/market-data/list-candles`] | Non | — | CGU : corps non lisible (PDF rendu côté navigateur) [abs] | 1 440 lignes (instantané) |

**ETH/USD : 6 places utilisables** (Coinbase, Kraken, Bitstamp, Bitfinex, Binance via ETHUSDT, OKX via ETH-USDT) ; Gemini non. En USD fiat pur : Coinbase, Kraken, Bitstamp, Bitfinex (4), auxquelles Binance ETHUSD (6 mois, 23 % de minutes actives en juin) et OKX ETH-USD (réserve ci-dessus) ne devraient pas être ajoutées sans précaution [inféré].

### 3.2 USDC/USD

| Place | Paire exacte et URL lue | Profondeur | Couvre sept. 2026 ? | Licence / republication | Échantillon (lignes) |
|---|---|---|---|---|---|
| **Binance** | `USDCUSD` (`quoteAsset":"USD"`, `TRADING` [lu, `data-api.binance.vision/api/v3/exchangeInfo?symbol=USDCUSD`]) : `https://data.binance.vision/data/spot/monthly/klines/USDCUSD/1m/USDCUSD-1m-2026-08.zip` | **2025-11 à 2026-08 mensuel** (≈ 10 mois) ; quotidiens du 2025-11-18 au 2026-10-03 [mesuré] | **Oui** (30 fichiers quotidiens de septembre 2026) | CC BY-NC-SA 4.0 (§3.5) | 44 640 lignes (août 2026), 3,8 % à volume nul [mesuré] |
| **Coinbase** | **aucun marché USDC-USD** : la liste `GET /products` (839 produits) ne contient que `USDC-CAD, -EUR, -AUD, -GBP, -BRL, -SGD, -INR` et `USDT-USDC` [mesuré, `api.exchange.coinbase.com/products`, 2026-10-04] | — | — | — | — |
| **Kraken** | `USDCUSD` (`USDC/USD`, `online` [mesuré]) : `USDCUSD_1.csv` dans `Kraken_OHLCVT_2026Q2.zip` ; première transaction **2020-01-08** [mesuré] | 2020-01 → 2026-06-30 | **Non** (fin au 2026-06-30) | CGU, voir ETH/USD | `USDCUSD_1.csv` du 2026-Q2 : 127 621 lignes |
| **Bitstamp** | `usdcusd` (`USDC/USD` `Enabled`) : `https://www.bitstamp.net/api/v2/ohlc/usdcusd/?step=60&limit=1000&start=<epoch>` | Données au plus tard au **2020-11-01** [mesuré] | Oui | Contrat commercial signé, voir ETH/USD | 1000 lignes, **972 à volume nul (97 %)** : bougies reportées, pas de transaction [mesuré] |
| **Bitfinex** | `tUDCUSD` (le code Bitfinex d'USDC est `UDC` ; `UDCUSD` dans la liste des paires [mesuré]) | Première bougie **2018-12-04** [mesuré] | Oui | Non lu | 4 bougies en 5 h le 2026-08-15 ; **417 bougies sur 10 080 minutes (4 %)** du 2026-08-10 au 17 [mesuré] |
| **OKX** | **aucune paire USDC-USD** : ticker `USDC-USD` code 51001 ; `market-data-history` renvoie 0 fichier ; seule `USDC-USDT` existe (stable/stable, exclue des classes USD par l'ADR §2.5) [mesuré] | — | — | — | — |
| **Gemini** | `usdcusd` listé dans `/v1/symbols` [mesuré] ; 1 439 bougies = 24 h seulement | 24 h | Non | non lu | 1 439 lignes |

**USDC/USD : 4 places, exactement** (Binance, Kraken, Bitstamp, Bitfinex). Ni Coinbase, ni OKX, ni Gemini (24 h). Cela confirme sur pièce le fait que l'ADR §2.5 annonçait comme « serré » (Kraken, Bitstamp, Bitfinex, Gemini) ; **Binance est une place de plus que l'ADR ne comptait, mais avec moins d'un an d'historique** ; **Gemini, comptée par l'ADR, n'a pas d'historique** [lu + mesuré].

### 3.3 USDT/USD

| Place | Paire exacte et URL lue | Profondeur | Couvre sept. 2026 ? | Licence | Échantillon (lignes) |
|---|---|---|---|---|---|
| **Binance** | `USDTUSD` (`quoteAsset":"USD"`, `TRADING` [lu]) : `…/spot/monthly/klines/USDTUSD/1m/USDTUSD-1m-2026-08.zip` | **2025-11 → 2026-08** mensuel ; quotidiens depuis 2025-11-18 | Oui | CC BY-NC-SA 4.0 | 44 640 lignes, 0,2 % à volume nul |
| **Coinbase** | `USDT-USD` (`online` [mesuré]) : `https://api.exchange.coinbase.com/products/USDT-USD/candles?granularity=60&…` | Premières bougies vues le **2021-05-06** (sondage tous les 5 jours : aucune avant) [mesuré] | Oui | non lu | 300 lignes |
| **Kraken** | `USDTUSD` (`USDT/USD` → paire `USDTZUSD`) : `USDTUSD_1.csv` | Première transaction **2017-03-29** [mesuré] | Non (2026-06-30) | CGU | 130 715 lignes (2026-Q2) |
| **Bitstamp** | `usdtusd` | Données au plus tard au **2021-07-01** [mesuré] | Oui | contrat signé | 1000 lignes, 902 à volume nul (90 %) |
| **Bitfinex** | `tUSTUSD` (`UST` = USDT ; `USTUSD` dans la liste) | Première bougie **2018-11-27** | Oui | non lu | 179 bougies en 5 h ; 6 627 sur 10 080 minutes (2026-08-10 à 17) |
| **OKX** | `USDT-USD` (instrument `live`, `listTime` 1733452200000 = **2024-12-06** [lu, `GET /api/v5/public/instruments`]) : `…/monthly/202608/USDT-USD-candlesticks-2026-08.zip` | 2024-12 → 2026-09 (22 fichiers) | Oui | CGU OKX (§3.1) | 44 640 lignes |
| **Gemini** | `usdtusd` ; 24 h seulement | 24 h | Non | non lu | 1 439 lignes |

**USDT/USD : 6 places utilisables** ; 5 sans Bitstamp (très mince).

### 3.4 BTC/USD (pour mémoire)

Coinbase `BTC-USD` : premières bougies vues **2015-01-30** (sondage mensuel) ; Kraken `XBTUSD_1.csv` (première transaction 2013-10-06 [mesuré]) ; Bitstamp `btcusd` : données au plus tard au 2015-01-01 ; Bitfinex `tBTCUSD` : première bougie 2013-04-01 ; Binance `BTCUSDT` mensuel 2017-08 → 2026-08 (`BTCUSD` seulement 2025-12 → ) ; OKX `BTC-USDT` 2021-01 → 2026-09 (pas de `BTC-USD`) ; Gemini : 24 h. **6 places, ≥ 4 : oui** [lu + mesuré]. Échantillons : `coinbase-BTC-USD-1m-20260815.json` (300), `kraken-Q2-2026-XBTUSD_1.csv` (130 969), `bitstamp-btcusd…` (1000), `bitfinex-tBTCUSD…` (265), `binance-BTCUSDT…` (44 640).

### 3.5 Conditions d'usage de Binance Vision (lues en entier, 4 pages)

Source : `https://data.binance.vision/Binance_Vision-Terms_of_Use.pdf` (sha256 `94d6f61a39b5f821ef1d38f968aea1f2aa136e374f2061a2131db9a6af96bc3b`), « Binance Vision Dataset Terms », version 1.0, “Last Updated: August 26, 2026” (p. 1).

- Licence (p. 2, art. 3.1) : “Datasets are provided to You under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Public License” [lu].
- Usage commercial (p. 2, art. 3.4) : “Commercial licensing is strictly excluded under this agreement; any commercial utilization requires a separate, written enterprise data license agreement executed with Binance.” [lu]
- Republication (p. 2, art. 4.5) : toute œuvre dérivée redistribuée porte l'attribution et “remains licensed under the identical CC BY-NC-SA 4.0 terms” [lu]. Donc republication des octets bruts permise **sous CC BY-NC-SA, non commerciale seulement** [lu + inféré].
- Les conditions sont postérieures de moins de six semaines à ce jour ; l'art. 1.4 dit qu'elles s'appliquent aux données mises à disposition après leur entrée en vigueur [lu, p. 1].
- Que le produit Shōgen (certificat) soit un « usage commercial » est une question de valeur, non tranchée ici [inféré].

---

## 4. Faisabilité mesurée sur une semaine (comptes seulement, aucun τ)

Fenêtre : du **2026-06-08 00:00 UTC** au **2026-06-15 00:00 UTC** (10 080 minutes), choisie parce que l'archive Kraken s'arrête au 2026-06-30. « Place active » = minute avec volume > 0 (les minutes reportées de Bitstamp et les minutes à volume nul de Binance ne comptent pas). Données dans `window/`, comptes dans `window/concurrence.txt`, script `window.py` et `conc.py`.

| Classe | Jeu de places | Minutes (sur 10 080) avec ≥ 4 places actives | avec ≥ 3 | avec ≥ 2 |
|---|---|---|---|---|
| ETH/USD | Coinbase, Kraken, Bitstamp, Bitfinex | 9 799 (97,2 %) | 10 075 (100 %) | 10 080 |
| ETH/USD | les 4 ci-dessus + Binance ETHUSDT + OKX ETH-USDT | 10 080 (100 %) | 10 080 | 10 080 |
| USDC/USD | Binance, Kraken, Bitstamp, Bitfinex | **76 (0,8 %)** | 1 626 (16,1 %) | 9 565 (94,9 %) |
| USDT/USD | Binance, Coinbase, Kraken, Bitstamp, Bitfinex, OKX | 10 031 (99,5 %) | 10 079 | 10 080 |
| USDT/USD | sans Bitstamp (5 places) | 10 025 (99,5 %) | 10 079 | 10 080 |

Minutes actives par place pour USDC/USD sur la semaine : Binance 9 998, Kraken 9 551, Bitstamp **693**, Bitfinex **1 098** [mesuré]. Pour ETH/USD : Binance ETHUSD 2 289 seulement ; USDT/USD : Bitstamp 1 542.

Lecture [inféré] : si la médiane leave-one-out est calculée sur les clôtures **de toutes les bougies**, y compris reportées, Bitstamp USDC et Bitfinex USDC y entrent avec des prix périmés ; si elle n'est calculée que sur les minutes avec échange, la classe USDC n'a presque jamais 4 séries simultanées. Le choix est à écrire au G0, avec la grille de τ ; il n'est pas fait ici.

---

## 5. Hors pool, pour information (non compté)

**Bybit** : `https://public.bybit.com/spot/<PAIRE>/` (liste de répertoires publique, sans clé) contient des **ticks de transactions** (`<PAIRE>_AAAA-MM-JJ.csv.gz`, colonnes `id,timestamp,price,volume,side,rpi`), pas des bougies d'une minute : une minute se dérive par agrégation [inféré]. Paires présentes : `ETHUSDT` et `USDCUSDT` depuis 2022-11 ; `ETHUSD`, `USDTUSD`, `BTCUSD` depuis 2026-04, jusqu'au 2026-10-03 [mesuré]. L'API `api.bybit.com` et `api.bytick.com` répondent 403 (CloudFront, « configured to block access from your country ») [mesuré]. Conditions : pages `bybit.com` rendues côté navigateur, corps non lu [abs]. Échantillons : `bybit-spot-ETHUSDT_2026-08-15.csv.gz` (42 474 lignes), `…ETHUSD…` (3 004), `…USDTUSD…` (2 221).

---

## 6. Ce qui manque et limites rencontrées

1. **Conditions d'usage non lues** [abs] : Coinbase (403 Cloudflare sur `coinbase.com/legal/market_data_terms` et `exchange-api-terms`) ; Bitfinex (page « Market Data Terms » dont le corps n'est pas dans le HTML servi) ; Gemini (contrat d'utilisateur rendu côté navigateur) ; Bitstamp `terms-of-use` (jeton Incapsula, seule la page d'API a été lue) ; Bybit. **Pas de comblement** : à lire avec un outil capable d'exécuter le JavaScript (Firecrawl ou WebFetch, indisponibles dans cette session) ou par le mainteneur.
2. **Aucune licence propre à l'archive** pour Kraken et OKX [abs] : seules leurs CGU générales ont été lues, et leur application à ces fichiers est [inféré].
3. **Kraken** : pas de fichier du 3e trimestre 2026 à ce jour ; l'historique de septembre 2026 n'est donc pas disponible chez Kraken (ni via l'API : 720 bougies au plus) [lu + mesuré].
4. **OKX** : écart entre la page (« from July 2023 onwards ») et les fichiers (2021-01 pour ETH-USDT) ; et `ETH-USD` présent en fichiers mais absent de l'API des instruments [mesuré].
5. **USDC/USD** : 4 places sur 4 ; deux sont très minces (Bitstamp 6,9 %, Bitfinex 10,9 % de minutes actives en juin) ; Binance n'a que ≈ 10 mois ; aucune marge. Gemini, que l'ADR comptait, n'a pas d'historique. Coinbase n'a pas le marché [lu].
6. **Profondeur de Binance en paires USD** : ETHUSD depuis 2026-03, USDCUSD et USDTUSD depuis 2025-11, BTCUSD depuis 2025-12 [mesuré] : la période d'avant-S2 disponible est de 5 à 11 mois, pas plusieurs années, pour la jambe USD fiat de Binance.
7. **Position mono-vantage** : toutes les sondes viennent d'un seul poste cloud ; `api.binance.com` y est bloqué (451, étude du pool) mais `data.binance.vision` et `data-api.binance.vision` répondent [mesuré].
8. **Aucun τ, σ ni P99,9 calculé** ; la décision « bougies reportées ou non » (§4) reste à fixer au G0.

---

## 7. Échantillons et empreintes

Dossier : `/tmp/claude-0/-home-user-shogen/7ba84933-ba6d-5813-9ef4-ca3ac4febd16/scratchpad/s2bis/calib/`
- `samples/` : 33 fichiers (liste, lignes et sha256 complets dans `samples-index.tsv` ; sha256 de tous les fichiers dans `SHA256SUMS-ECHANTILLONS.txt`, 148 lignes).
- `web/` : copies des pages et listes lues (listes S3 de Binance, pages de conditions, produits Coinbase, paires Bitfinex, instruments OKX, etc.).
- `window/` : séries de la semaine du §4 et `concurrence.txt`.
- Scripts : `dl.sh`, `rangezip.py` (lecture par plages d'octets de l'archive Kraken), `kr_extract.py`, `cb_first.py`, `txt.py`, `window.py`, `conc.py`.

Échantillons principaux (nom, lignes, sha256) :

| Fichier | Lignes | sha256 |
|---|---|---|
| binance-ETHUSDT-1m-2026-08.zip | 44 640 | `f2f2fe8da85467fb8ec8185e07f16f3af9f4ebcb266633ba494e76ac73c40c0c` |
| binance-ETHUSD-1m-2026-08.zip | 44 640 | `8a02b2fb875f9282bfdf517dcfe33dbc1d0fc5cf69a0da6ea8347ef5a6fb035d` |
| binance-USDCUSD-1m-2026-08.zip | 44 640 | `1fc21b52dac75d253c29c43eea475dfa292f3d14932386b2378edd313b1f54e3` |
| binance-USDTUSD-1m-2026-08.zip | 44 640 | `616ccf0bf65d89b56e2c3c1e4d70c33479d1fdf342ae3eaad868cca1692618f4` |
| binance-BTCUSDT-1m-2026-08.zip | 44 640 | `acab442e02745177063031d402929703ae983715010064b40cf811c4beb843d4` |
| coinbase-ETH-USD-1m-20260815.json | 300 | `3f973f4bc3434cb5ce65c1712921ea838a2034dfb5258852cc164b42a93414e1` |
| coinbase-USDT-USD-1m-20260815.json | 300 | `77bcc8d209341725007173cef0971b8b2c8779a1352d327c33c7774569d67533` |
| coinbase-BTC-USD-1m-20260815.json | 300 | `a4f2271da3dbfa8890aa312459e8378607a83ee2cdd0c59fb233b98ceed3c128` |
| kraken-Q2-2026-ETHUSD_1.csv | 130 240 | `652981209f6c2aa151dafb65aa219506ba34c71df012e6f69e801f2f81fcdd76` |
| kraken-Q2-2026-USDCUSD_1.csv | 127 621 | `e649464516c86381aa58a2a83f6ce91560394231cfff3213965c93068409cb3c` |
| kraken-Q2-2026-USDTUSD_1.csv | 130 715 | `db584f24c7f0d4783fbdac82e88c9a089c7930945fc052b8fbdc9694374e2104` |
| kraken-Q2-2026-XBTUSD_1.csv | 130 969 | `bedc82a0eb85f0a56f5ac29d103f4d667423de0b90681bd7d1d12db7f92ee613` |
| kraken-Q2-2026-MANIFEST.json | manifeste | `ef2ef64e738426937c6a4702816c49fd59ebeca2553ca11ca59fd35edfe631d9` |
| bitstamp-ethusd-1m-20260815.json | 1000 | `18b02b207676fd895c41684014586a5e53ba0c430987dd46265d07f6ab9ac774` |
| bitstamp-usdcusd-1m-20260815.json | 1000 | `c2e6ae0ccd4e567cdf9542f5d5fda0fff9cb8c2f7d30b549ed94ccdefbc4ae0e` |
| bitstamp-usdtusd-1m-20260815.json | 1000 | `3674083d091fc22f630a12dfced5eaeb98854d407be1a28a83dff9dacfb6413b` |
| bitstamp-btcusd-1m-20260815.json | 1000 | `6e7817f89b878db1dcfb6ae624fedbabae835a62387adf1b2f1c8207cc4c047f` |
| bitfinex-tETHUSD-1m-20260815.json | 264 | `9922f35817cab3964c697bd6e037d55fb6d431d9828d6b51d918be63853bd29e` |
| bitfinex-tUDCUSD-1m-20260815.json | 4 | `8f4c05dd5847e798da09c63f3f94858832ff01a6e2cfd9ff58a010ca8c576a9f` |
| bitfinex-tUSTUSD-1m-20260815.json | 179 | `f9efebf27e76df1a4588e2939156fbd8f20a1ea2142e4220be5c0987ad206c08` |
| bitfinex-tBTCUSD-1m-20260815.json | 265 | `85b229f6d3f9bd60f8f2a6f1edd8c05a4c6fcb6670760270eed814a5f4fd5fdd` |
| okx-ETH-USDT-candlesticks-2026-08.zip | 44 640 | `b3573a45b7968ec52b394d6270335fcc05daec2ec6a5f5123e18be0d75472302` |
| okx-ETH-USD-candlesticks-2026-08.zip | 44 640 | `7f1b8db121d9a16123f1154f04c0966f63c269c0ff4f600c2e53a5e3ea1ea56a` |
| okx-USDT-USD-candlesticks-2026-08.zip | 44 640 | `3591387a89c5b0812f58e1e5d874e2fd46450c44cee18cd9cd8989db12ccf65e` |
| gemini-{eth,usdc,usdt,btc}usd-1m-latest.json | 1 440 / 1 439 / 1 439 / 1 440 | voir `samples-index.tsv` |
| bybit-spot-ETHUSDT / ETHUSD / USDTUSD_2026-08-15.csv.gz | 42 474 / 3 004 / 2 221 | voir `samples-index.tsv` |
| Binance_Vision-Terms_of_Use.pdf (`web/`) | 4 pages | `94d6f61a39b5f821ef1d38f968aea1f2aa136e374f2061a2131db9a6af96bc3b` |

---

## 8. Conclusion par classe (réponse à « ≥ 4 places ? »)

- **ETH/USD : OUI** (6 places ; 4 en USD fiat profond). Réserves : conditions d'usage non lisibles pour 2 places sur 4 en USD fiat (Coinbase, Bitfinex) ; republication des octets bruts non établie.
- **USDC/USD : OUI, sans marge** (4 sur 4 : Binance depuis 2025-11, Kraken, Bitstamp, Bitfinex), avec deux places presque inactives. Une exclusion (licence, minceur, fenêtre) fait passer la classe à NON. Pour la décision de vague (ADR §2.6, F3 « ≥ 3 places ou planchers seuls »), la condition de F3 est satisfaite sans équivoque.
- **USDT/USD : OUI** (6 places, 5 sans Bitstamp).
- **Sur la lecture « republication permise »** : NON pour les trois classes, car la permission explicite n'existe que chez Binance (non commercial, CC BY-NC-SA) et Bitstamp (contrat signé). Si l'ADR n'exige que l'**existence** de l'historique et que seul le τ dérivé est publié (octets bruts référencés par URL et sha256, non republiés), la lecture « disponibilité » s'applique [inféré] ; c'est une décision de l'orchestrateur (ADR-0003, ADR-0005).
- Ce qui manque pour trancher : lire Coinbase, Bitfinex, Gemini ; décider si un certificat est un usage commercial au regard de Binance (NC), d'OKX (art. 9.4) et de Kraken (« for your own benefit ») ; décider du traitement des bougies reportées.
