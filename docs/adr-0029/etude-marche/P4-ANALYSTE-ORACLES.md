# P4 — Analyste du marché des oracles et des données : paysage, parts, graphe des amonts, pool de S2-bis

Gate 0 : modèle résolu `claude-sonnet-5-5` (profil P4, brief sha256 `ebc51aaf…85fa` vérifié). Date de lecture de toutes les sources : 2026-10-04 (04:49–05:00 UTC), sauf mention. Niveaux : [lu] lu sur la source ; [2nd] seconde main ; [inféré] mon raisonnement ; [calc] calcul sur données lues. Copies : `web/` (même dossier). Lecture seule du dépôt (docs 02, 04, 07, 10 §3, 11, ADR-0028 avis produit, ADR-0029 §1-2.5) ; aucune pièce interdite ouverte ; aucune écriture hors de ce dossier.

## 1. Résumé (10 lignes)

1. Le marché oracle est très concentré : DefiLlama (page « Oracles ranked by TVS », 2026-10-04) donne Chainlink 38,3 Md$ (534 protocoles), « Internal » 8,2 Md$, Chronicle 5,1 Md$ (13), RedStone 4,3 Md$ (90), Pyth 3,7 Md$ (320) [lu]. Chainlink pèse environ 60 % du total listé, 69 % hors « Internal » [calc] ; la TVS compte un protocole sous chacun de ses oracles, donc les parts ne s'additionnent pas proprement [inféré].
2. Parmi les cinq premiers, **seuls Chainlink (par RPC) et RedStone (passerelle) sont lisibles sans clé** en ce moment ; Pyth exige une clé (« Hermes now requires an API Key », 401), Chronicle est protégé par liste blanche en mainnet [2nd], Stork 401. Switchboard a cessé le 2026-09-25 [2nd].
3. Le graphe des amonts est **nettement plus resserré que le nombre de logos** : CoinGecko est un amont déclaré de DefiLlama [lu], de RedStone [lu], de Chainlink (billet 2020, nommé « e.g. BraveNewCoin, CoinGecko ») [lu], d'API3 et de Band [2nd] ; Binance et Coinbase sont des éditeurs de Pyth [lu], des sources de RedStone [lu], et Binance/OKX des entrées de l'oracle de Hyperliquid [lu].
4. Mes plus beaux « copies d'amonts déjà au pool » : `okx_index` (composants lus en direct : Kraken, Bitstamp, Crypto.com, Coinbase pour BTC ; OKX, Bybit, Coinbase, Binance, Kraken pour ETH) ; DefiLlama = f(CoinGecko) ; `oraclePx` de Hyperliquid = médiane Binance/OKX/Bybit/Gate/MEXC ; RedStone en partie.
5. Les sources lisibles sans clé existent pour les quatre actifs, avec des cadences très différentes : de la seconde (places, RedStone 10 s) à des **heartbeats d'un jour** pour Chainlink USDC/USDT (82 800 s et 86 400 s, déviation 0,25 %) [lu].
6. Ma mesure d'ASN, faite depuis un autre point de vue, retrouve la partition de S2 (4 ASN sur 10 hôtes, 7 derrière Cloudflare) [calc] : le pool de S2-bis est reproductible, et les candidats se répartissent entre Cloudflare (CoinPaprika, KuCoin, Crypto.com, les RPC publicnode/drpc/mevblocker/blastapi) et le reste (RedStone, DIA, Hyperliquid, Gate : AWS ; MEXC : Akamai ; Tenderly : Google).
7. Élargir le pool **n'augmente pas mécaniquement k_eff/k** : avec 9 ajouts, 5 ASN pour 19 hôtes ; avec 6 ajouts hors Cloudflare, 6 ASN pour 16 [calc]. L'axe ASN sature vers 5-6, car peu de fournisseurs d'infrastructure portent tout.
8. Recommandation : ajouter d'abord **RedStone (paquets signés), DIA, un second chemin de lecture RPC pour Chainlink, CoinPaprika, MEXC, Gate, KuCoin, Hyperliquid, un pool Uniswap v3 lu par RPC** (liste §4), en classes séparées par actif et par nature (places ; agrégateurs ; oracles à heartbeat).
9. Consolidation en cours : Kaiko a racheté Amberdata (2026-06-02) [2nd], CoinGecko étudie une vente à environ 500 M$ [2nd], CoinMarketCap appartient à Binance depuis 2020 [2nd] : les « amonts indépendants » se réduisent, ce qui nourrit la thèse de Shōgen et fragilise l'accès sans clé à CoinGecko [inféré].
10. Limites : TVS à une date, une seule vue réseau, textes d'usage non lus pour la plupart des API (redistribution des octets bruts d'ADR-0003 non établie).

## 2. Constats sourcés

### 2.1 Parts de marché des oracles (valeur sécurisée, intégrations)

| Oracle | TVS | Protocoles | Source / niveau |
|---|---|---|---|
| Chainlink | 38,281 Md$ | 534 | DefiLlama `/oracles` [lu] |
| « Internal » (oracle propre au protocole) | 8,199 Md$ | 51 | idem [lu] |
| Chronicle | 5,133 Md$ | 13 | idem [lu] |
| RedStone | 4,265 Md$ | 90 | idem [lu] |
| Pyth | 3,663 Md$ | 320 | idem [lu] |
| Atlas | 1,769 Md$ | 5 | idem [lu] ; nature non élucidée (probablement le cadre OEV lié aux feeds SVR de Chainlink, [inféré]) |
| Chaos Labs | 0,820 Md$ | 6 | idem [lu] |
| UMA / Stork / Supra / Switchboard / eOracle / Band / DIA | 370 / 243 / 217 / 146 / 141 / 117 / 116 M$ | 9 / 39 / 15 / 22 / 18 / 22 / 51 | idem [lu] |
| API3 / Pragma / Tellor / Umbrella | 22 M$ / 19 M$ / 0 / 317 $ | 44 / 8 / 2 / 1 | idem [lu] |
| CoinGecko / CoinMarketCap listés « oracles » | 0,51 M$ / 0,47 M$ | 7 / 1 | idem [lu] |

Fichier : `web/defillama-oracles.md` (la page est protégée par une épreuve Cloudflare : `curl` a reçu un 403 ; c'est le lecteur Firecrawl du harnais qui l'a rendue ; à déclarer, voir §5). Recoupements : oracles.ink (juin 2026) donne Chainlink ~33 Md$, Chronicle ~7,5, RedStone ~3,6, Pyth ~3,1 [2nd] ; Messari (T4 2025) : parts Chainlink 73,1 %, Chronicle 12,8 %, RedStone 7,8 %, Pyth 6,3 % [2nd, extrait de recherche]. Les ordres sont stables ; les niveaux dépendent du jour et du périmètre. La TVS est la valeur des protocoles qui utilisent un oracle, pas la valeur réellement exposée à son prix [inféré].

Capitalisation (CoinGecko, catégorie « oracle », 2026-10-04) : LINK 10,47 Md$, PYTH 0,62, RED 0,096, PHA 0,062, TRB 0,057, API3 0,044, BAND 0,042, UMA 0,038, AT (APRO) 0,031, DIA 0,020, SEDA 0,015, SUPRA 0,0076, UMB 0,0001 [lu, `web/cg-oracle.json`]. La capitalisation du jeton ne dit pas la part de marché du service.

Signaux de structure : (a) Switchboard a annoncé le 2026-09-19 sa fin au 2026-09-25, citant le coût de construire son propre oracle avec l'IA, le marché baissier et les partenariats directs entre places et fournisseurs (Hyperliquid–S&P) [2nd, Solana Compass] ; (b) panne de plus de quatre heures de Pythnet le 2026-05-22, sans post-mortem au moment de l'article [2nd, CryptoTimes] ; (c) incident Moonwell du 2026-02-15 (feed OEV mal configuré, 1,78 M$ de mauvaise dette) [2nd] : la mauvaise configuration pèse autant que l'amont.

### 2.2 Agrégateurs et fournisseurs de données

- **CoinGecko** : API sans clé fonctionnelle aujourd'hui (`simple/price`, horodatage `last_updated_at`, âge 90-130 s). Une vente à ~500 M$ est étudiée (Moelis) [2nd]. Positionnement : « meilleur choix général » dans les comparatifs, 17 400+ actifs, 1 700+ places [2nd, spark.money].
- **CoinMarketCap** : propriété de Binance depuis 2020, avec une clause d'indépendance déclarée [2nd] ; clé exigée (401 code 1002) [lu].
- **Kaiko** : fournisseur institutionnel (références pour Cboe, Gemini ; ~250 clients après le rachat d'Amberdata le 2026-06-02) [2nd] ; Binance a cité Kaiko pour la liquidité lors du 10/10 [2nd]. Clé exigée (non testé, pas de compte).
- **CoinDesk Data (ex-CCData/CryptoCompare)** : 401 « API key required » [lu] ; déjà écarté (doc 10 §3.1).
- **Messari** : l'ancien point `data.messari.io` répond 404 (non conclu) ; Blockworks l'aurait acquis [2nd, titre seul].
- **DefiLlama coins** : sans clé ; « Almost all tokens are priced using CoinGecko's API » [lu, `docs.llama.fi/llms-full.txt`]. **Changement notable** : `api.llama.fi/oracles` répond désormais 402 (offre payante) ; `/protocols` et `coins.llama.fi` restent ouverts [lu]. Le champ `oracles` de `/protocols` est trop lacunaire pour recalculer la TVS (2,6 Md$ couverts sur ~294 Md$) [calc] : on ne peut donc pas recalculer soi-même la part de marché à partir d'un point ouvert.
- **CoinPaprika** : sans clé, 4 actifs, horodatage `last_updated` (âge 1-4 min) [lu] ; amont non déclaré lu [manque].
- **CoinLore** : sans clé mais stablecoins à deux décimales (« 1.00 ») : inutilisable pour USDC/USDT [lu].
- **CoinCap** : v2 non joignable depuis ma session (502 du relais) ; v3 exige une clé [inféré] : non conclu.

### 2.3 Places de marché (volume « réel »)

CoinGecko `/exchanges` (note de confiance, volume 24 h converti au cours BTC du jour, **volume déclaré** [lu, `web/cg-exch.json`]) : Binance 10 (≈4,6 Md$), Coinbase 10 (0,73), Kraken 10 (0,48), OKX 10 (1,21), Gate 10 (0,80), Bitget 10 (0,34), puis Bitstamp 9 (0,10), MEXC 9 (0,78), Crypto.com 9 (0,22), Bybit 9 (0,75), KuCoin 9 (0,70), Gemini 9 (0,01), Bitfinex 8 (0,06), Upbit 8 (0,84). Les tickers bruts de CoinGecko classent en tête CoinUp.io, BTCC, Azbit, Pionex pour BTC, ETH et USDT : le **volume déclaré n'est pas le volume réel**, il faut filtrer par la note de confiance (la note par ticker est vide dans la réponse sans clé) [lu, `web/cg-tickers.json`]. Volume DEX 24 h (DefiLlama, 2026-10-04) : 6,79 Md$ au total ; Uniswap V4 19,3 %, Uniswap V3 8,1 %, PumpSwap 5,9 %, PancakeSwap V3 5,1 % [lu].

### 2.4 Graphe des amonts déclarés (qui consomme qui)

| Consommateur | Amonts déclarés | Niveau |
|---|---|---|
| CoinGecko | tickers de places (VWAP après filtre MAD, doc 10 §4.3) | [lu, par le dépôt] |
| DefiLlama coins | CoinGecko (presque tous les jetons), sinon pools Uniswap V2 | [lu] |
| Chainlink Feeds | « 3+ agrégateurs/fournisseurs de données de marché » (page actuelle, **sans noms**) ; billet du 2020-12-31 : « exclusivement des agrégateurs premium (e.g. BraveNewCoin, CoinGecko) » ; Kaiko opérateur-fournisseur (annonce 2019) | [lu] ; [2nd] |
| RedStone | Binance, Coinbase, Uniswap, Sushiswap, CoinMarketCap, CoinGecko, « 150+ sources » ; Kaiko, CoinMarketCap cités au flux de données | [lu] |
| Pyth | éditeurs de première main : Coinbase, Binance, OKX, Hyperliquid, Cboe, Jane Street, Virtu, Revolut… (+ Bitstamp, Bybit, Wintermute [2nd]) | [lu] |
| Hyperliquid (prix oracle) | médiane des mid perps Binance, OKX, Bybit, Gate, MEXC, poids 3/2/2/1/1, mise à jour ~3 s | [lu] |
| API3 | CoinGecko (source centrale d'une partie des dAPIs) | [2nd, CoinGecko] |
| Band | Binance, CoinGecko « partenaires de données » | [2nd] |
| Chronicle | validateurs qui interrogent CEX/DEX, tableau de bord par validateur (docs en 429 : non lues) | [2nd] |
| DIA | trades directs de 100+ places, « 100 % de transparence » (auto-déclaré ; doc en 403 : non lue) | [2nd] |
| `okx_index` | BTC-USD : Kraken 27,27 %, Bitstamp 18,18 %, Crypto.com 27,27 %, Coinbase 27,27 % ; ETH-USD : OKX 23,52 %, Bybit 17,64 %, Coinbase 17,64 %, Binance 23,52 %, Kraken 17,64 % | [lu en direct, `index-components`] |
| CoinMarketCap | propriété de Binance (indépendance déclarée) | [2nd] |
| Kaiko | a absorbé Amberdata (2026-06-02) ; les deux étaient des agrégateurs nommés par Chainlink en 2019-2020 | [2nd] |

Lecture [inféré] : la couche « places » se réduit à Binance, Coinbase, OKX, Kraken (plus Bybit, Gate) ; la couche « agrégateurs » à CoinGecko, CoinMarketCap/Binance, Kaiko(+Amberdata), CoinDesk ; la couche « oracles » les lit. Les chemins de lecture ajoutent un autre nœud : tous les RPC publics que j'ai essayés sans clé pour Ethereum rendent le **même** `roundId` et `updatedAt` (même chaîne), mais les hôtes sont soit derrière Cloudflare (publicnode, drpc, mevblocker, blastapi), soit hors (Tenderly sur Google) [calc].

Incidents d'appui à la thèse des racines : panne AWS us-east-1 (2025-10-20, Coinbase, Robinhood) et panne Cloudflare (2025-11-18, environ 3 h : Coinbase, Kraken, Aave, Etherscan) [2nd, The Block, Cointelegraph] ; 10/10/2025 : Binance a versé 283 M$ après des écarts d'indice sur USDe, WBETH, BNSOL (21:36-22:16 UTC) [2nd, The Block]. Un seul observateur Cloudflare n'aurait pas distingué ces cas.

### 2.5 Lisibilité sans clé et cadence, pour BTC, ETH, USDC, USDT (sonde du 2026-10-04 ~04:53 UTC, un seul point de vue)

| Source (hôte) | BTC | ETH | USDC | USDT | Horodatage / cadence observée | ASN (hôte) |
|---|---|---|---|---|---|---|
| Coinbase Exchange | oui | oui | **404** (USDC-USD absent) | oui | dernier trade, âge <1 s (BTC) à 9 s (USDT) | 13335 |
| Kraken | oui | oui | oui | oui | aucun horodatage | 13335 |
| Bitstamp | oui | oui | oui | oui | epoch s, âge ≤ 25 s | 19551 |
| Gemini | oui | oui | oui | oui | ms, granularité ~60 s (âge ~80 s) [inféré] | 14618 |
| Bitfinex | oui | oui | oui | oui | aucun | 13335 |
| OKX ticker / indice | oui | oui | oui (USDC-USDT) | oui | ms ; indice : composants lisibles | 13335 |
| Binance | **451** (restriction de lieu) | 451 | 451 | 451 | – | 16509 |
| Bybit | **403** (CloudFront, pays) | 403 | 403 | – | – | 16509 |
| KuCoin / Gate / HTX / Bitget / MEXC | oui | oui | oui | non essayé | ms (sauf Gate, MEXC : aucun) | 13335 / 16509 / 16509 / 13335 / 20940 |
| Crypto.com | oui | oui | nom de paire rejeté | non essayé | ms | 13335 |
| Hyperliquid (`allMids`, `metaAndAssetCtxs`) | oui | oui | – | – | prix oracle ~3 s | 16509 |
| CoinGecko | oui | oui | oui | oui | âge 90-130 s | 13335 |
| CoinPaprika | oui | oui | oui | oui | âge 1-4 min | 13335 |
| DefiLlama coins | oui | oui | oui | oui | âge 150-340 s | 13335 |
| DIA (`assetQuotation`, champ `Signature`) | oui | oui | oui | oui | âge ~1-1,5 min | 16509 |
| RedStone (passerelle, paquets signés) | oui | oui | oui | oui | **10 s**, 5 signataires ; réponse de 1,97 Mo | 16509 |
| Chainlink (`latestRoundData` par RPC) | oui | oui | oui | oui | heartbeat : BTC, ETH 3 600 s (0,5 %) ; USDC 82 800 s (mainnet, 0,25 %) ; USDT 86 400 s (0,25 %) [lu, annuaire officiel] ; âges mesurés : 59 min, 39 min, 8,3 h, 14,3 h | RPC : 13335 / 396982 |
| Pyth | **401** (Hermes) ; pas d'accès en direct | – | – | – | contrat Ethereum lu : valeurs figées (BTC 64 735 vieux de 72 jours) | 13335 |
| Chronicle, Stork, CoinDesk, CMC, CryptoCompare | clé ou liste blanche | | | | | |
| Band (REST) | 200 mais **dernier prix résolu il y a ~130 jours** (76 370 $) | | | | à exclure | – |
| Supra, API3 Market | non conclu (404 sur mon essai ; page sans JSON) | | | | | |

Écarts entre sources lisibles, BTC à 04:53 : 84 792 à 84 837 $, soit ~0,05 % ; USDC et USDT : quelques points de base, sauf GeckoTerminal USDT 1,00397 (valeur de jeton agrégée sur pools) [calc]. Contrôle de décodage : pool Uniswap v3 ETH/USDC 0,05 % lu en `slot0` : 2 690,44 $ contre 2 691,5 sur les places [calc]. Binance en 451 depuis cette session est cohérent avec le doc 10 (supposition (c) sur le géo-blocage) et se vérifiera depuis chaque observateur.

Conséquence de cadence pour R1 [inféré] : (1) Chainlink est un flux **piloté par seuil et heartbeat**, pas une horloge ; son silence est normal (USDC jusqu'à 23 h) ; un σ de 180 s le déclarerait périmé à tort ; la classe « oracle à heartbeat » doit avoir son propre σ écrit d'avance (l'ADR-0029 §2.6 écrit déjà une « limite Chainlink »). (2) BTC/USD d'une place est souvent BTC/USDT (Binance, OKX, Bybit, KuCoin…) : **l'USDT est un amont caché** de beaucoup de « prix BTC », donc ajouter USDT couple les classes.

## 3. Copies d'amonts déjà au pool (ou qui en dérivent)

Fort (à marquer `basis:doc` ou `measured`, jamais compter comme racine indépendante) : `okx_index` (déjà hors R1, à garder pour l'axe contenu) ; DefiLlama (déjà au pool) ; prix oracle de Hyperliquid (Binance, OKX déjà au pool) ; dYdX `oraclePrice` (non lu, supposé construit sur un jeu de places, [manque]). Partiel : RedStone (Binance, Coinbase, CoinGecko, CoinMarketCap, Kaiko : intersection avec 3 unités du pool) ; Chainlink (CoinGecko peut figurer dans ses agrégateurs selon un billet de 2020 : la page actuelle ne nomme rien, donc **l'arête vers `coingecko` reste ouverte**, ce qui est précisément une mesure de contenu que S2-bis peut faire). Non lisibles donc non testables : Pyth (éditeurs communs avec le pool), Chronicle.

## 4. Recommandations : ajouts ordonnés au pool de S2-bis

Principe : une unité = un hôte (ADR-0029 §2.5) ; l'ajout doit **figurer dans le paquet scellé** avant le sceau (aucune décision après) ; chaque nouvelle classe (ETH, USDC, USDT) porte son τ et son σ ; les oracles à heartbeat sont une classe à part. Je ne recommande pas de mélanger les trois natures dans une seule statistique.

**Oracles (3 ajouts, 1 contrôle).**
1. **RedStone, paquets signés** (`oracle-gateway-1.a.redstone.finance`, hôte AWS). Raison : n°4 par la TVS, seul oracle majeur lisible sans clé en direct avec **signatures vérifiables hors ligne** (adéquat à l'ADR-0003), cadence de 10 s, quatre actifs. Coûts et risques : réponse de 1,97 Mo par lecture, soit environ 2,8 Go par jour et par observateur à une lecture par minute (à extraire et hacher, pas à publier brut) ; la documentation parle désormais de clés d'API et de passerelles authentifiées : l'accès sans clé est toléré aujourd'hui, pas garanti [lu] ; termes d'usage non lus. Amont déclaré : arêtes `basis:doc` vers coingecko, binance, coinbase.
2. **Chainlink pour ETH, USDC, USDT** (BTC déjà là) et **un deuxième chemin de lecture** (RPC de familles distinctes : publicnode d'un côté, Tenderly ou drpc de l'autre ; le doc 10 distingue déjà chemin de lecture et amont). Raison : n°1 par la TVS, c'est le critère de référence ; le second chemin sépare la panne du RPC de la panne du feed. Risque : heartbeats longs, donc très peu d'observations par fenêtre sur les stablecoins.
3. **DIA** (`api.diadata.org`, AWS). Raison : source qui déclare lire directement 100+ places (amont à tester contre CoinGecko), cotation signée (champ `Signature`), quatre actifs. Réserve : TVS faible (116 M$) et documentation non lue (403) : la place dans le pool tient à son rôle de **racine alternative**, pas à sa part de marché.
4. Contrôle négatif : ne pas ajouter Pyth (clé), Chronicle (liste blanche), Band (REST périmé), Switchboard (arrêté), Stork (401). Ajouter une ligne « non lisible sans clé » au rapport pour chacun, avec date : c'est une donnée de marché utile (la moitié du TVS n'est pas mesurable de l'extérieur sans clé).

**Agrégateurs (2 ajouts, 2 étiquetés).**
1. **CoinPaprika** (sans clé, quatre actifs, horodaté). Raison : seul agrégateur général sans clé de plus ; amont non déclaré, donc candidat à une mesure de contenu. Hôte Cloudflare : il pèse sur k_eff.
2. **GeckoTerminal** (prix de jeton agrégé sur pools, quatre actifs, sans clé, Cloudflare). Raison : agrégateur à méthode **on-chain**, autre racine de données que les places. Réserve : valeur USDT à 40 points de base dans ma lecture : surveiller l'axe hors-enveloppe.
3. Garder CoinGecko et DefiLlama, étiquetés « copie déclarée » pour les quatre actifs (DefiLlama = f(CoinGecko)). Ne pas ajouter CoinLore (précision). Ne rien lire chez Kaiko/CMC/CoinDesk (clé) ; **les nommer au graphe** (Kaiko+Amberdata, CMC=Binance) sans lecture.

**Places (ordre, avec classes et actifs).**
1. **MEXC** (Akamai, seul hôte hors des quatre grands ASN ; note de confiance 9 ; BTC, ETH, USDC). Raison : diversité d'infrastructure.
2. **Gate** (AWS ; note 10 ; 0,8 Md$). 3. **KuCoin** (Cloudflare ; note 9). 4. **Hyperliquid, `midPx` seulement** (place perps sur chaîne propre, ~3 s ; son `oraclePx` est une copie). 5. **Crypto.com** (BTC, ETH). 6. **Bitget, HTX** en réserve.
7. **DEX par RPC** : pool Uniswap v3 ETH/USDC 0,05 % (`slot0`, vérifié) ; pour BTC (WBTC) et USDT/USDC (Curve, Uniswap 0,01 %), **adresses à établir sur pièce avant le sceau** [manque]. Raison : Uniswap pèse ~27 % du volume DEX [lu] ; mode de défaillance propre (chaîne, RPC), très différent de celui des API HTTP. Réserve : un TWAP est manipulable, on ne lit ici que le prix spot comme **témoin de contenu**.
Écarter Binance du **confirmatoire** si un observateur de l'UE le reçoit en 451 : c'est le critère d'essai déjà écrit (smoke avant sceau).

**Effet sur l'axe R2 [calc]** : base (10 hôtes) : 4 ASN ; base + RedStone, DIA, CoinPaprika, MEXC, Gate, Hyperliquid, KuCoin, Crypto.com, drpc (19 hôtes) : 5 ASN ; base + RedStone, DIA, MEXC, Gate, Hyperliquid, Tenderly (16 hôtes) : 6 ASN. Messages à tenir à l'investisseur : élargir ne « diversifie » pas l'infrastructure au-delà de 5-6 ASN ; ce qui s'élargit, ce sont les **types de racines** (places, agrégateurs, oracles signés, DEX sur chaîne), donc le contenu du certificat (partition nommée, arêtes déclarées) plus que son chiffre.

**Ce que ça apporte** : un jeu de classes (BTC, ETH, USDC, USDT × trois natures) où R1 peut trancher sur autre chose que BTC/USD place ; un tableau de lisibilité sans clé daté, qui est déjà un livrable de position institutionnelle (DefiLlama a fermé `/oracles` au gratuit : la mesure ouverte et recalculable devient rare) [inféré].

**Ce que ça coûte** : zéro licence (tout est sans clé) ; ingénierie : un décodeur par source (RedStone signé, `slot0`, Chainlink ABI, sept formats JSON) ; débit : lectures par lot (CoinGecko `ids=` multiples, Kraken multi-paires) pour rester sous les limites, environ 60-80 lectures par minute et par observateur au total [inféré] ; stockage : RedStone domine. La puissance (ADR-0029 §2.4) est à recalculer par classe : ETH et USDC/USDT portent des taux de panne et des FIV propres, non mesurés.

**Risques** : (a) retrait d'un accès sans clé en cours de campagne (RedStone : doc de clés ; CoinGecko : vente, politique de sondage « pas adapté à une interrogation planifiée », doc 10 §3.3) : règle R-b d'ADR-0029 (remplacement de l'observateur, jamais retrait d'unité) à étendre aux unités ; (b) multiplication des tests : déclarer une seule statistique confirmatoire par classe, le reste en sensibilité ; (c) stablecoins : une « panne » USDT peut être un vrai événement de marché ; (d) sur-promesse : jamais « indépendant », toujours « racines mesurées + déclarées ».

## 5. Incertain, manques et divulgations

- **Parts de marché des agrégateurs** : aucun chiffre d'usage primaire trouvé (seulement des comparatifs et des communiqués) [manque]. TVS des oracles : un seul jour, DefiLlama + deux recoupements de seconde main.
- **Sources bloquées, non contournées** : docs Chronicle (429), docs DIA (403), `defillama.com` par `curl` (épreuve Cloudflare 403) ; la page a été obtenue par le lecteur Firecrawl du harnais : à votre appréciation si ce chemin vous convient. `api.llama.fi/oracles` : 402. Hermes de Pyth : 401, non contourné (je n'ai pas insisté au-delà d'un essai sur `benchmarks.pyth.network`, même 401). Binance 451 et Bybit 403 : constatés, non contournés ; je n'ai pas testé de miroir.
- **Une requête hors règle** : dans le lot de RPC, j'ai envoyé un seul appel `eth_call` à une URL Alchemy portant le jeton public « demo » ; c'est une sorte de clé, je ne m'en sers pour aucune recommandation (les autres RPC suffisent). À signaler à l'orchestrateur.
- **Un seul point de vue** pour tous les codes HTTP, ASN et horodatages ; résolveur : Google DoH ; ASN : RIPEstat `prefix-overview` d'une seule adresse par hôte ; CDN et anycast peuvent différer par observateur.
- Non établi : conditions d'usage (redistribution des octets bruts, ADR-0003/0005) pour RedStone, DIA, CoinPaprika, GeckoTerminal, places ; composition des agrégateurs actuels de Chainlink ; amont de CoinPaprika, dYdX, Supra ; nature de « Atlas » ; les 4 hôtes autres que Cloudflare/AWS pourraient en réalité être derrière CloudFront selon l'adresse.
- Sources de seconde main non relues à la source : Messari T4 2025, Moonwell, Switchboard (une seule dépêche lue), Kaiko–Amberdata, vente de CoinGecko, éditeurs Pyth hors page officielle, API3 et Band.

## 6. Trois questions à l'investisseur

1. Voulez-vous que S2-bis reste **confirmatoire sur BTC/USD (10 hôtes, déjà scellable)** et que ETH, USDC, USDT et les nouvelles natures soient une **seconde vague exploratoire** (avec sa propre règle), ou que tout entre dans le paquet scellé au prix d'un retard et d'une puissance à recalculer ?
2. Acceptez-vous de dépendre d'accès **sans clé tolérés mais non garantis** (RedStone, CoinGecko), avec remplacement écrit d'avance, ou préférez-vous financer une ou deux clés payantes (Pyth, Kaiko, CoinGecko Pro) pour mesurer aussi la moitié du TVS aujourd'hui illisible, au risque de ne plus pouvoir publier les octets bruts ?
3. Le produit visé est-il un **certificat sur un pool nommé par le client** (partition + arêtes déclarées, ASN plafonnés à 5-6) ou un **classement public de la lisibilité et de la concentration des oracles** (le tableau §2.5 et le graphe §2.4, daté et rejouable) ? Le second tient la position institutionnelle plus vite et n'attend pas R1.

## Sources principales (lues le 2026-10-04)

DefiLlama `https://defillama.com/oracles` (copie `web/defillama-oracles.md`) ; `https://api.llama.fi/protocols`, `/overview/dexs`, `https://coins.llama.fi/prices/current/…`, `https://docs.llama.fi/llms-full.txt` ; CoinGecko `api.coingecko.com/api/v3/coins/markets?category=oracle`, `/exchanges`, `/coins/{id}/tickers`, `/simple/price` ; Chainlink `https://docs.chain.link/data-feeds/data-sources`, `https://chain.link/blog/levels-of-data-aggregation-in-chainlink-price-feeds` (2020-12-31), `https://reference-data-directory.vercel.app/feeds-mainnet.json` ; Pyth `https://www.pyth.network/publishers` (extrait de recherche), `https://docs.pyth.network/price-feeds/core/api-instances-and-providers/hermes` ; RedStone `https://docs.redstone.finance/docs/technical-reference/architecture/`, `…/data-quality/data-flow/`, `…/price-feeds/pull-model/`, passerelle `https://oracle-gateway-1.a.redstone.finance/data-packages/latest/redstone-primary-prod` ; Hyperliquid `https://hyperliquid.gitbook.io/hyperliquid-docs/trading/robust-price-indices` ; OKX `https://www.okx.com/api/v5/market/index-components` ; DIA `https://api.diadata.org/v1/assetQuotation/…` ; seconde main : oracles.ink, Solana Compass (Switchboard), CryptoTimes (Pyth 2026-05-22), The Block, Cointelegraph, A-Team et Cointelegraph (Kaiko–Amberdata), PYMNTS et DL News (CoinGecko), pages de documentation Chronicle, Polygon, Arbitrum (liste blanche) vues par moteur de recherche. Sondes brutes : `web/probe1.txt`, `web/asn.txt`, `web/rpc.txt`, `web/pyth-onchain.txt`, `web/feeds-mainnet.json`.
