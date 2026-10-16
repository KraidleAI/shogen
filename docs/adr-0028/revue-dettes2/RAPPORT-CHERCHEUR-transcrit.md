# Sens des bornes de pagination des bougies (lecture des documentations des places) (transcrit)

> Transcription par l'orchestrateur le 2026-10-15 13:51:21 UTC du fichier formes-api/RAPPORT.md ; contrôle FM-1.1 du transcript du chercheur, par le fm11.py versé et par celui de DT3-E : fragments_l51_l14 = 0 ; modèle résolu : claude-sonnet-5-5. Texte ci-dessous avec trois retouches, déclarées : l. 38 et l. 40 de l'original, une espace rétablie entre `integer` et le crochet ouvrant des domaines de `start` et de `limit` de Bitstamp, forme de la page détenue `bitstamp-api-v2-docs-2026-10-10.html` (la graphie collée venait de la copie Firecrawl) ; l. 64 de l'original, le guillemet fermant de la citation de la carte d'OKX est placé après « Candlestick » et le deux-points mis hors des guillemets, forme de `biblio/INDEX.md` : la page détenue `okx-en-us-historical-data-2026-10-10.html` porte le titre de la carte et sa description sans deux-points ; un erratum daté suit le texte (fuseau des mensuels d'OKX) ; le chemin du scratchpad est abrégé en `<scratchpad>`.

# SHOGEN-CALIB-FORMES-API-1 : sens des bornes de pagination des bougies d'une minute

Modèle résolu : `claude-sonnet-5-5` (chercheur, lecture sur pièce). Aucune API de données appelée : seulement des pages de
documentation (Firecrawl scrape/search). Dépôt non touché. Lectures du 2026-10-09, `date -u` : 11:32Z à 11:36Z.
Niveaux : [lu] page officielle, citation mot pour mot ; [2nd] source secondaire ; [abs] introuvable.
Code comparé (lecture seule) : `.../calib3/travail/snap/CA-6e/scripts/calib-actifs/` (`acquerir.py`, `bougies.py`, `parametres.json`).

## 1. Coinbase Exchange, GET /products/{product_id}/candles

Page : https://docs.cdp.coinbase.com/api-reference/exchange-api/rest-api/products/get-product-candles
(redirection de https://docs.cdp.coinbase.com/exchange/reference/exchangerestapi_getproductcandles ; version Markdown
brute : même URL + `.md`). Lue le 2026-10-09 ~11:33Z.

| Question | Réponse | Citation | Niveau |
|---|---|---|---|
| `start` inclus ou exclu ? | NON DIT | seule description : « Timestamp for starting range of aggregations » | [abs] |
| `end` inclus ou exclu ? | NON DIT | « Timestamp for ending range of aggregations » | [abs] |
| Réponse hors bornes | La doc prévient que des bougies PRÉCÈDENT `start` | « If data points are readily available, your response may contain as many as `300` candles and some of those candles may precede your declared `start` value. » | [lu] |
| Format de `start`/`end` (ISO 8601 ou secondes Unix) | NON DIT sur cette page (type `string`, « Timestamp »). La page voisine des types ne parle que des réponses : « Unless otherwise specified, all timestamps from API are returned in ISO 8601 with microseconds. » (https://docs.cdp.coinbase.com/exchange/rest-api/types) | voir à gauche | [abs] pour la requête ; [lu] pour les réponses ISO 8601 en général |
| Maximum de bougies par réponse | 300 ; au-delà, la requête est REJETÉE (pas tronquée) | « The maximum number of data points for a single request is `300` candles. » ; « If your selection of start/end time and granularity results in more than `300` data points, your request is rejected. » | [lu] |
| Granularité | `{60, 300, 900, 3600, 21600, 86400}` secondes, sinon rejet | « The `granularity` field must be one of the following "second" values: `{60, 300, 900, 3600, 21600, 86400}`, or your request is rejected. » | [lu] |
| Ordre des bougies | NON DIT | aucune phrase sur l'ordre ; le schéma de réponse OpenAPI est `items: object, properties: {}` | [abs] |
| Défaut sans bornes | « If the `start` or `end` fields are not provided, both fields are ignored. If a custom time range is not declared, then one ending now is selected. » (une seule borne donnée = les deux ignorées) | idem | [lu] |
| Forme d'une bougie | `time` = « bucket start time », puis low, high, open, close, volume ; « No data is published for intervals where there are no ticks. » | idem | [lu] |

Remarque : le format de requête (ISO ou secondes) et le caractère inclus/exclu ne sont pas établis par la documentation
officielle actuelle. Je ne les affirme pas ; seul un essai empirique (hors mandat) ou une page officielle plus ancienne
(pro.coinbase.com a été redirigé vers la page ci-dessus, la capture Wayback de 2023 n'a pas rendu le texte) peut les
trancher.

## 2. Bitstamp, GET /api/v2/ohlc/{market_symbol}/

Page : https://www.bitstamp.net/api/ (section « OHLC data », ancre `#tag/Market-info/operation/GetOHLCData`). Lue le
2026-10-09 ~11:33Z.

| Question | Réponse | Citation | Niveau |
|---|---|---|---|
| Sens de `start` | début de la plage ; inclus/exclu NON DIT | « Unix timestamp from when OHLC data will be started. » (`integer [ 0 .. 253402297199 ]`) | [lu] pour le sens ; [abs] pour l'inclusion |
| Sens de `end` | fin de la plage ; inclus/exclu NON DIT | « Unix timestamp to when OHLC data will be shown. » | [lu] pour le sens ; [abs] pour l'inclusion |
| `limit` maximal | 1000, minimum 1, obligatoire (avec `step`) | « integer [ 1 .. 1000 ] ... Limit OHLC results. » ; erreur : « Must be between 1 and 1000. Limit value must be between 1 and 1000. » ; « Step and limit parameters are missing. » | [lu] |
| Priorité si `start`, `end`, `limit` ensemble | `end` l'emporte sur `start` | « If both start and end timestamps are posted, end timestamp will be used. » ; sans aucune des deux : « returns OHLC data to current unixtime ». Rien sur l'articulation exacte avec `limit` (compte-t-on `limit` bougies en arrière depuis `end` ?) | [lu] pour end > start ; [abs] pour `limit` |
| Unité des horodatages | secondes Unix. La doc dit « Unix timestamp » sans écrire « seconds » ; l'échantillon de réponse porte `"timestamp": "1643630400"` (10 chiffres = secondes) ; `step` : « Timeframe in seconds. » (enum 60...259200) | idem | [lu] (déduction directe de l'échantillon, pas d'énoncé « seconds » pour start/end) |
| Ordre des bougies | NON DIT | l'échantillon n'a qu'une bougie | [abs] |
| Autre | `exclude_current_candle` : « If set, results won't include current (open) candle. » | | [lu] |

## 3. Bitfinex, GET /v2/candles/trade:1m:{symbol}/hist

Page : https://docs.bitfinex.com/reference/rest-public-candles (modifiée le 2026-02-23 selon la méta de la page). Lue le
2026-10-09 ~11:33Z.

| Question | Réponse | Citation | Niveau |
|---|---|---|---|
| `start` (ms), inclus ? | INCLUS | « If start is given, only records with MTS >= start (milliseconds) will be given as response. » | [lu] |
| `end` (ms), inclus ? | INCLUS | « If end is given, only records with MTS <= end (milliseconds) will be given as response. » | [lu] |
| `limit` maximal | 10000 ; défaut 100 | « Number of records in response (max. 10000). » ; méta : « The endpoint provides the last 100 candles by default, but a limit and a start and/or end timestamp can be specified. » | [lu] |
| `sort` | +1 croissant, -1 décroissant, sur MTS ; ordre par défaut NON DIT | « +1: sort in ascending order \| -1: sort in descending order (by MTS field). » | [lu] ; défaut [abs] |
| Unité de MTS | millisecondes | « Millisecond epoch timestamp » ; ordre des champs : [0] MTS, [1] OPEN, [2] CLOSE, [3] HIGH, [4] LOW, [5] VOLUME | [lu] |
| Débit | 30 requêtes par minute | « Rate Limit: 30 reqs/min (requests per minute) » | [lu] |

## 4. OKX

### 4a. Archives mensuelles (données historiques téléchargeables)

Pages : https://www.okx.com/en-us/historical-data (« Candlestick » : « OHLC chart history from July 2023 onwards. », page
rendue sans autre texte, les liens de téléchargement sont dynamiques) et le point d'accès documenté
https://www.okx.com/docs-v5/en/ , section « Get historical market data », `GET /api/v5/public/market-data-history`
(module `2` = « 1-minute candlestick », `dateAggrType` `daily` ou `monthly`). Lues le 2026-10-09 ~11:34Z.

| Question | Réponse | Citation | Niveau |
|---|---|---|---|
| Alignement des mois : UTC ou UTC+8 ? | NON DIT pour les fichiers mensuels de bougies. Aucune phrase sur le fuseau des fichiers. Indice dans l'exemple de réponse (fichiers QUOTIDIENS de transactions, `BTC-USDT-SWAP-trades-2025-09-01.zip`) : `dateTs`/`dateRangeEnd` = `1756656000000`, soit 2025-08-31T16:00:00Z (vérifié `date -u -d @1756656000`) = minuit du 2025-09-01 en UTC+8 ; le fichier `...2025-08-31.zip` porte `1756569600000` = 2025-08-30T16:00:00Z. Le jour du nom de fichier semble donc compté en UTC+8. | exemple : `"dateTs": "1756656000000", "filename": "BTC-USDT-SWAP-trades-2025-09-01.zip"` | [abs] pour les mensuels de bougies ; indice [lu] sur l'exemple quotidien (déduction, pas énoncé) |
| Paramètres | `begin`/`end` en ms « (inclusive) » ; « Maximum range: 10 days for daily, 10 months for monthly » ; `dateRangeStart`/`dateRangeEnd` « (inclusive) » | citations entre guillemets ci-contre | [lu] |
| Fuseau ailleurs dans la doc OKX | Les barres longues de l'API de bougies existent dans les deux fuseaux : « UTC+8 opening price k-line: [6H/12H/1D/2D/3D/1W/1M/3M] » et « UTC+0 opening price k-line: [6Hutc/12Hutc/1Dutc/2Dutc/3Dutc/1Wutc/1Mutc/3Mutc] » ; et ailleurs « dataDate ... (UTC+8) ». La barre `1m` n'est pas concernée par ce choix, mais le découpage des FICHIERS mensuels n'est pas dit. | | [lu] (sens) |

### 4b. `GET /api/v5/market/history-candles`

Page : https://www.okx.com/docs-v5/en/ , section « GET / Candlesticks history » (aussi `#order-book-trading-market-data-get-candlesticks-history`). Lue le 2026-10-09 ~11:34Z.

| Question | Réponse | Citation | Niveau |
|---|---|---|---|
| `after` | enregistrements PLUS ANCIENS que `ts` ; inclus/exclu NON DIT | « Pagination of data to return records earlier than the requested `ts` » | [lu] sens ; [abs] inclusion |
| `before` | enregistrements PLUS RÉCENTS que `ts` ; seul, renvoie les plus récents | « Pagination of data to return records newer than the requested `ts`. The latest data will be returned when using `before` individually » | [lu] sens ; [abs] inclusion |
| `limit` | maximum 300, défaut 100 | « Number of results per request. The maximum is `300`. The default is `100`. » | [lu] |
| `ts` | début de bougie, ms | « Opening time of the candlestick, Unix timestamp format in milliseconds » | [lu] |
| Ordre | NON DIT (l'échantillon de réponse est trompeur : deux `ts` identiques) | | [abs] |
| Débit | « Rate Limit: 20 requests per 2 seconds » | | [lu] |

Hors sujet mais noté : la page GitHub freqtrade #7700 ([2nd]) ne traite que des barres 1D, pas des mensuels de 1 minute.

## Écarts entre le code du lot et la documentation

Le code ne lit PAS les bornes d'après un énoncé de la documentation pour Coinbase, Bitstamp et OKX : il suppose, sans que la
documentation le dise, que les deux bornes sont incluses (ou que les mois sont en UTC). Bitfinex est le seul conforme [lu].

| Place | Lecture par le code | Constat | Ligne(s) à changer (sans changer) |
|---|---|---|---|
| Bitfinex | `parametres.json` : `start={debut_ms}&end={fin_ms}&limit=10000&sort=1`, `pas`=10000 ; `acquerir.py:170-171` : `fin = min(debut + 60*(pas-1), fen["fin"]-60)` ; `bougies.py:83-85` lit MTS en ms, clôture en colonne 2 | CONFORME : `>=` et `<=` inclusifs, 10000 = maximum, `sort` explicite, ms, colonne CLOSE = [2]. La page de 10000 minutes inclusives tient exactement dans `limit` (marge nulle, correcte). Dernière page : 1040 bougies. | aucune |
| Coinbase | `parametres.json` : `start={debut_iso}&end={fin_iso}` (ISO `%Y-%m-%dT%H:%M:%SZ`, `acquerir.py:162-163`), `pas`=300 donc 300 minutes inclusives, soit exactement le maximum | NON ÉTABLI : doc muette sur inclusion et format de requête, et elle annonce que des bougies peuvent précéder `start`. Si `end` était exclu : 299 bougies par page, la minute `fin` de chaque page manque et est lue silencieusement « sans échange » (`bougies.py:68-72` ne vérifie pas la complétude ; `derniers`, l.115-125, reporte le dernier prix). Si des bougies précèdent `start` : `bougies.py:103` (`not fen["debut"] <= t < fen["fin"]`) ou `bougies.py:105` (`minute en double`) refuse tout le lot : échec fermé, donc sûr, mais bloquant. L'ordre n'est pas supposé (dictionnaire, `bougies.py:100-108`) : aucun écart sur ce point. | `acquerir.py:171` (calcul de `fin` ; à passer à une borne vérifiée avant épinglage) ; `bougies.py:70-73` + `:103/:105` (tolérer ou écarter, par page, les bougies hors `[debut, fin]` de la page) ; et à ajouter un contrôle de complétude (compte de minutes par page) sinon l'absence d'un `end` exclu passe pour du « sans échange ». À trancher avant par un essai empirique autorisé, hors mandat de lecture. |
| Bitstamp | `start={debut}&end={fin}&limit={n}&step=60` (secondes), `n = (fin-debut)/60 + 1`, `pas`=1000 (= maximum) ; `bougies.py:76-80` | CONFORME sur : unité (secondes), `limit` <= 1000, `step`+`limit` présents, `end` prioritaire (le code donne les deux, donc cohérent avec « end timestamp will be used »). NON ÉTABLI : inclusion de `end` et de `start`, et si `limit` compte à rebours depuis `end`. Avec `end` inclus et `limit=n`, la fenêtre calculée sur `end` retombe sur `[debut, fin]` exactement : le code est correct SI `end` est inclus. Si `end` est exclu, la page est décalée d'une minute (première page : minute avant `fen["debut"]` → refus `bougies.py:103` ; pages suivantes : doublon → refus `:105`) : échec fermé. | `acquerir.py:171` seulement si l'essai établit `end` exclu (alors `fin + 60` et `n` inchangé) ; sinon aucune. |
| OKX (mensuels) | `acquerir.py:79-83` `mois()` : mois UTC de `[fen["debut"], fen["fin"]-60]` ; `bougies.py:103` exige `debut <= t < fin` en UTC | RISQUE : si les fichiers mensuels sont alignés sur UTC+8 (indice [lu] sur l'exemple quotidien, jamais énoncé pour les mensuels), le fichier `2026-04` commence le 2026-03-31T16:00Z, hors fenêtre : refus CA/format à la première ligne (échec fermé). Et les 8 dernières heures de la fenêtre (2026-06-30T16:00Z à 2026-07-01T00:00Z) seraient dans le fichier `2026-07`, que `mois()` ne télécharge pas : sans le refus précédent, elles seraient lues « sans échange ». | `acquerir.py:79-83` (ajouter le mois suivant, et le mois précédent, puis laisser `bougies.serie` écarter les minutes hors fenêtre pour OKX seulement : `bougies.py:100-104`) ; à décider après lecture de l'en-tête réel d'un fichier OKX (hors mandat). |
| OKX (API) | non utilisée par le code | sans objet pour le lot ; `after`/`before` : sens établi [lu], inclusion [abs] | aucune |

## Restent [abs] (non trouvés dans la documentation officielle)

1. Coinbase : `start` et `end` inclus ou exclus ; format de requête (ISO 8601 ou secondes) ; ordre des bougies.
2. Bitstamp : `start` et `end` inclus ou exclus ; articulation de `limit` avec `end` ; ordre des bougies ; mot « seconds » pour start/end (déduit de l'échantillon).
3. Bitfinex : ordre par défaut quand `sort` est omis (le code met `sort=1`, donc sans effet).
4. OKX : alignement UTC ou UTC+8 des fichiers mensuels de bougies de 1 minute ; inclusion de `after`/`before` ; ordre de `history-candles`.

Les points [abs] de Coinbase, Bitstamp et OKX ne se résolvent que par un essai sur données réelles (hors mandat de lecture :
"aucune API de données") ou par un contact avec les places. Le lot échoue fermé dans la plupart des cas (refus
`CA/format`), mais pas dans le cas « borne `end` exclue » de Coinbase, où la minute manquante est lue comme une minute sans
échange : c'est le risque à lever avant l'épinglage.

> **Erratum daté du 2026-10-15 13:51:21 UTC (heure produite par `date -u`) : fuseau des mensuels d'OKX (§4a)**, porté par l'orchestrateur au versement (lot DETTES-T16, B.99, relecture G2). Les l. 71, 73 et 100 de l'original et le premier point de sa l. 108 disent qu'aucune phrase de la documentation d'OKX ne donne le fuseau des fichiers mensuels, niveau [abs] : ce [abs] vient d'une copie de la page (extraction Firecrawl du 2026-10-09) qui ne porte que 2 des 248 encadrés de la page ; un [abs] établi sur une telle copie n'est pas une absence. La page détenue (`okx-docs-v5-en-api-guide-2026-10-10.html`), section « Get historical market data », porte l'encadré « Timezone specifications for timestamp parsing » : « When converting Unix timestamps to dates, the following timezone conventions are applied to all timestamp fields (begin, end, dateRangeStart, dateRangeEnd, dataTs) » ; « All other data modules (modules 1, 2, 3, 11): UTC+8 » (module 2 : « 1-minute candlestick ») ; et l'encadré « Data query rules » : « Only the date portion (yyyy-mm-dd) of timestamps is used; time components are ignored » ; « Both begin and end timestamps are inclusive ». Le fuseau des dates des fichiers de bougies est donc écrit : UTC+8 [lu] ; les minutes que contient un mensuel ne sont pas dites par la page, elles sont établies sur pièce par la DECISION (ajout daté du 2026-10-09 19:51:45 UTC). Les bornes inclusives visent `begin` et `end` de `GET /api/v5/public/market-data-history`, au jour près ; elles ne disent rien de `after` ni de `before` de `GET /api/v5/market/history-candles`, dont l'inclusion et l'ordre restent [abs]. Le code de `scripts/calib-actifs/` n'appelle aucun de ces deux points d'accès : il lit les mensuels à leur URL statique, mois voisins compris.
