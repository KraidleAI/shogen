# Étude de marché Shōgen, profil P5 : stablecoins, dépegs et dérivés d'ETH

> *Note de versement de l'orchestrateur* : citations de pages web non versées à `biblio/` passées de « … » à “…” (gate S-G5) ; lectures [lu] web du rapport, copies hors dépôt.

- **Gate 0** : modèle résolu `claude-opus-5-5` (préfixe attendu, CLAUDE.md §7). Date de session : 2026-10-04 ; recherche menée entre 04:49 et 05:10 UTC (`date -u`).
- **Brief** : `etude-marche/BRIEF-P5-STABLECOINS.md`, sha256 `eb52269c…209684b`, vérifié.
- **Exposition** : lus dans le dépôt, en lecture seule : docs 02, 04, 07 ; doc 10 §2-§3 ; doc 11 §1, §2.1-§2.6 et §4 ; `docs/adr-0028/AVIS-PRODUIT-APRES-S2.md` ; ADR-0029 §1, §2.1, §2.2, §2.5 et §2.6. Aucune pièce de `docs/15-*`, `docs/16-*`, `docs/rapports/`, `docs/adr-0025/` ou `docs/adr-0028/monark-m009a/`, aucun `*.jsonl`. Aucune écriture dans le dépôt, aucune opération git, aucune clé, aucun compte, aucun achat.
- **Niveaux** : [lu] lu sur la source (page, API publique ou état de chaîne) ; [2nd] seconde main ; [calc] calcul de l'auteur sur un [lu] ; [inféré] raisonnement de l'auteur. Copies et scripts : `P5-STABLECOINS/web/` (notes, réponses brutes) et `P5-STABLECOINS/calc/` (reconstruction des tours Chainlink, rejeu de mars 2023).

## Résumé

1. Il n'existe pas un seul « prix d'USDC » : il y a un prix contre le dollar fiat sur une poignée de places (Kraken, Bitstamp, Bitfinex ; Coinbase n'a **pas** de marché USDC-USD), un prix contre USDT (OKX, Uniswap, Curve, Binance), et des flux d'oracles qui mélangent les deux [lu].
2. Pendant le dépeg de mars 2023, les sources ont divergé fortement. Dans notre rejeu sans clé, la dispersion entre places est passée de 0,06 % à 0,86 % (médianes), avec un maximum de 7,6 %. Les plus bas vont de 0,8256 (Bitstamp) à 0,8816 (Chainlink) [calc].
3. Chainlink USDC/USD a bien suivi la baisse sur chaîne : 348 mises à jour en 66 h, plus bas 0,8800. En stress, il était plus proche de la place cotée en USDT (convertie en USD) que des places en dollar fiat : écart moyen de 0,21 % contre 0,55 % et 0,72 % [calc]. Lecture probable [inféré] : la liquidité en USDT pèse le plus dans sa « racine » effective.
4. Deux plafonds jouent dans des sens opposés : Chainlink borne les stablecoins à 1,05 $ (au-delà, la dernière valeur reste servie), et l'adaptateur CAPO d'Aave les plafonne vers 1,04 $ ; les baisses restent transmises [lu].
5. Les pires incidents récents viennent de **racines uniques ou de références substituées**, pas de pannes de réseau d'oracles. Exemples : l'index interne de Binance (USDe à 0,65 $ alors que Chainlink USDe/USD ne déviait que de 70 points de base), Compound v2 avec USDC codé en dur à 1 $, Aave qui prix USDe sur le flux USDT/USD, les erreurs de composition sur les LST (CAPO 2026 : −2,85 %, 26,6 M$ liquidés ; Moonwell : cbETH à 1,12 $) [lu].
6. Pour Shōgen, un dépeg est un **état du marché**, pas une panne de source. Il faut deux notions séparées : « écart de source » (hors de l'enveloppe des autres sources de la même classe) et « dépeg » (le consensus s'éloigne du pair) ; ce dernier sert de variable de régime.
7. Recommandations : ajouter six classes de faits jamais mélangées (USDC/USD, USDT/USD, USDC/USDT, ETH/USD, LST/ETH « marché », LST « taux de rachat ») ; ajouter un axe R2 **« devise de cotation et composition »** ; publier d'abord un **rejeu historique recalculable** des dépegs de 2022-2025.
8. Coût modeste en collecte (sources sans clé, testées ce jour) mais réel en statistique : une famille de tests plus grande, un dépeg probablement absent sur 16 semaines, un axe hors-enveloppe qui risque de ne jamais tirer en régime calme.

## 1. Constats sourcés

### 1.1 Comment se mesure aujourd'hui le prix d'USDC et d'USDT

Relevé sans clé du 2026-10-04 entre 04:54 et 04:55 UTC (`web/probe-*.txt`) [lu] :

| référence | sources lisibles sans clé (valeur) | remarques |
|---|---|---|
| USDT/USD fiat | Kraken 0,99982 ; Coinbase 0,99984 ; Bitstamp 0,99983 ; Gemini 0,99981 ; Bitfinex `tUSTUSD` 0,99986 ; indice OKX 0,99983 ; Crypto.com 0,9999 (achat/vente) | les 7 places se tiennent en 0,9 point de base [calc] |
| USDC/USD fiat | Kraken 0,9999 ; Bitstamp 0,99993 ; Bitfinex `tUDCUSD` 0,99999 | Coinbase `USDC-USD` : 404 (conversion 1:1, pas de carnet) |
| USDC/USDT | OKX 1,00012 ; Uniswap v3 0,01 % (lu sur chaîne) 1,00013 ; Curve 3pool : 10 USDC donnent 10,0003 USDT | Binance : HTTP 451, Bybit : 403 depuis ce point d'observation (géo-blocage) |
| agrégateurs | CoinGecko USDT 0,9999 / USDC 1,0 ; DefiLlama 0,99990 / 1,00001 | DefiLlama dérive de CoinGecko (doc 10 §3.2) |
| oracles | Chainlink USDT/USD 0,99982784 (tour du 03/10 à 14:35Z, 16 opérateurs, minimum 11/16) ; Chainlink USDC/USD 0,99998274 (03/10 à 20:35:59Z) ; RedStone (API publique) USDT 0,9998, USDC 0,99991 | Pyth : clé exigée (ADR-0023 du dépôt) ; Chronicle : lecture sur chaîne réservée à une liste blanche [2nd, docs Chronicle] |

**Paramètres Chainlink sur Ethereum** (répertoire JSON public, 298 flux, `web/cl-feeds-mainnet.json`) [lu] :
- USDC/USD : seuil de déviation 0,25 %, heartbeat de 82 800 s ;
- USDT/USD : 0,25 %, 86 400 s ;
- les deux sont marqués `stablecoinCapped: true` et « Bounded (upper) $1.05 » ;
- ETH/USD : 0,5 %, 3 600 s ; STETH/USD : 1 %, 3 600 s ; STETH/ETH : 0,5 %, 86 400 s ;
- CBETH/ETH : 1 % ; RETH/ETH : 2 % ; weETH/ETH : 0,5 % ; ezETH/ETH : 0,5 % (24 h chacun) ;
- USDe/USD : 0,5 %.

La documentation précise qu'au-delà de la borne, “the price will not be reported on-chain. Instead, the most recently written on-chain price will be the value returned”. Elle distingue aussi les flux de **prix de marché** des flux de **taux d'échange** (« internal redemption rates ») [lu, docs.chain.link/data-feeds/selecting-data-feeds].

**Composition publiée par RedStone** (`web/redstone-2026-10-04.json`) [lu] :
- USDT : 7 sources, toutes cotées en USD (binance, bitget, bitstamp, bybit, coinbase, kraken, okx) ;
- USDC : 18 sources, dont **11 cotées en USDT**, plus Curve (DAI, USDT) et Uniswap v3 (DAI) ;
- ETH : 14 sources sur 18 cotées en USDT ou en USDC.

**Conséquence [inféré]** : un « USDC/USD » d'oracle dépend en partie d'USDT/USD, et un « ETH/USD » dépend des deux. C'est l'hétérogénéité de devise déjà vue sur BTC en S2 (2 flux USDT sur 11, doc 11 §2.1), mais structurelle ici.

### 1.2 Dépegs chiffrés et comportement des oracles

| épisode | marché | oracles et protocoles |
|---|---|---|
| **USDC, 10-13 mars 2023** (3,3 Md$ de réserves bloquées chez SVB, environ 7,8 %) | plus bas sous 0,88 vers 08:00 UTC le 11 ; au-dessus de 0,99 le 13 vers 00:00 UTC [lu, Chaos Labs 30/03/2023 ; Gauntlet 17/03/2023]. Coinbase suspend les conversions USDC↔USD pendant la fermeture bancaire du week-end ; Binance suspend la conversion automatique [2nd, CoinDesk 11/03/2023] | **Chainlink USDC/USD, reconstruit sur chaîne** (`calc/usdc-usd-2023-03.txt`) : 1 tour par jour avant l'épisode, puis 348 tours entre le 10 à 22:27Z et le 13 à 16:13Z ; plus bas **0,8800** au tour 983 (11 à 07:51:23Z) ; sous 0,99 du 11 à 01:54Z au 13 à 09:39Z ; écart médian de 240 s entre tours, maximum de 4 h 32 [lu sur chaîne, calc]. Compound v2 : USDC, USDT, TUSD et USDP en **prix fixe codé en dur** [lu, CIP-4, 17/10/2023]. Aave : gel d'Avalanche vers 13:00Z le 11 ; environ 300 k$ d'insolvabilités ; « liquidations below ~98 cents were harmful » [lu, Gauntlet] |
| **USDT, 12 mai 2022** (contagion Terra) | Kraken 0,92 ; Binance.US 0,95 ; Bittrex 0,57 [2nd, Protos, qui note « exchanges do not provide detailed time and sales »] | Chainlink USDT/USD : plus bas **0,95182** le 12 à 07:22:33Z, au-dessus de 0,99 dès 11:09Z [lu sur chaîne] : 3,2 cents au-dessus du bas de Kraken, 38 cents au-dessus de celui de Bittrex |
| **USDT, juin 2023** | 0,995 ; 3pool Curve à 48,5 % d'USDT [lu, Kaiko 19/06/2023] | sans incident oracle notable relevé |
| **FDUSD, 2 avril 2025** | 0,87 sur Binance ; 0,76 rapporté contre USDC [2nd, The Block, BeInCrypto] | sans donnée oracle lue |
| **USDe, wBETH et BNSOL, 10 octobre 2025** (21:36-22:16Z) | USDe à **0,65 $ sur Binance** ; les marchés sur chaîne restent près de 1 $ [lu, LlamaRisk sur le forum Aave ; 2nd, 21Shares] | Chainlink USDe/USD : « minor 70 basis point deviation » [lu, LlamaRisk 24/10/2025]. Aave prix USDe **avec le flux USDT/USD** [lu]. Binance : 283 M$ d'indemnisation ; le 14/10, l'index WBETH passe de 20 % `WBETHUSDT` / 80 % `WBETHETH×ETHUSDT` à 0/100, et le prix de rachat entre dans les index [2nd, PANews, The Block] |
| **stETH, juin 2022** (Celsius, 3AC, pool Curve vidé) | environ 0,93-0,94 ETH [2nd, CoinDesk/Nansen] | Chainlink STETH/ETH : 19 tours en 17 jours (cadence d'environ 24 h) ; plus bas **0,93502** le 18/06 à 09:09Z ; le 13/06, aller-retour 0,941 → 0,962 → 0,942 entre deux tours [lu sur chaîne] |
| **ezETH, 24 avril 2024** | 688 $ sur Uniswap ; environ 56 M$ liquidés (Gearbox, Morpho) ; retraits Renzo fermés [2nd, DL News, Cointelegraph] | — |
| **wstETH, Aave, 10 mars 2026** | sans dépeg de marché | erreur de configuration de CAPO : taux maximal calculé à environ 1,1939, soit **−2,85 %** ; environ 10 938 wstETH liquidés sur 34 comptes, environ 26,6 M$ ; pas de mauvaise dette [lu, post-mortem Chaos Labs, governance.aave.com] |
| **cbETH, Moonwell, 15 février 2026** | sans dépeg de marché | taux cbETH/ETH utilisé sans la multiplication par ETH/USD : environ 1,12 $ au lieu d'environ 2 200 $ pendant 4 min ; 1 779 044,83 $ de mauvaise dette [lu, forum Moonwell] |

### 1.3 Rejeu de mars 2023 : ce qu'une mesure multi-sources aurait vu [calc]

Matériau : 935 fenêtres de 5 min, du 10/03 à 12:00Z au 13/03 à 18:00Z. Sources : bougies publiques sans clé Bitstamp `usdcusd`, Bitfinex `tUDCUSD`, OKX `USDC-USDT` multiplié par Coinbase `USDT-USD`, et Chainlink (dernier tour avant la fin de la fenêtre). Scripts et sorties : `calc/replay.py`, `calc/replay-2023-03/resultats.txt`.

- **Fragmentation** : entre 03:45 et 04:15Z le 11, Bitstamp USDC/USD cote encore 0,997-0,999 avec du volume réel (588 k USDC à 03:45). Au même moment, OKX USDC/USDT est entre 0,93 et 0,945 et Bitfinex entre 0,96 et 0,98. Plus tard, Bitstamp descend le plus bas (0,8256 à 07:15Z), sur un carnet mince [lu].
- **USDT monte pendant qu'USDC baisse** : Coinbase USDT-USD atteint 1,0163 (12/03 à 19:45Z). La conversion par USDT déplace donc le niveau d'USDC d'environ 1,6 point au pire. La devise de cotation est un mode commun à part entière.
- **Effet sur l'axe hors-enveloppe** (médiane leave-one-out, 4 sources) : K = 153 fenêtres à au moins deux écarts avec τ = 0,45 % (le τ « places » de S2), 43 avec τ = 1 %, 11 avec τ = 2 %. Le consensus s'écarte du pair de plus de 1 % dans 566 fenêtres sur 935.
- **Chainlink contre les places** : écart médian de +0,02 %, P1 à −1,9 %, minimum à −4,1 % (11 à 04:10Z, quand Bitstamp n'avait pas encore bougé). Écart moyen en stress : 0,21 % à OKX×USDT, 0,55 % à Bitfinex, 0,72 % à Bitstamp.
- **Limites** : bougies, pas des témoignages ; closes reportés (241 closes identiques consécutifs sur 935 chez Bitstamp) ; historique Kraken limité à 720 points ; aucun prix sur chaîne de DEX (pas de nœud d'archive essayé).

### 1.4 ETH et dérivés : flux et taux

Relevé du 2026-10-04 vers 04:55Z [lu] :
- taux de rachat sur chaîne : wstETH `stEthPerToken` 1,24548 ; rETH 1,17303 ; cbETH 1,14086 ; weETH 1,10502 ;
- prix de marché CoinGecko, en ETH : 1,24517 ; 1,16969 ; 1,14108 ; 1,10463 ;
- STETH/ETH : Chainlink 0,99972 ; Curve 0,99957 pour 1 stETH vendu.

L'écart entre marché et rachat se mesure donc sans clé ; rETH est ce jour 0,28 % sous son taux [calc]. Deux familles de prix coexistent [lu, docs Chainlink ; README de bgd-labs/aave-capo] :
- le **prix de marché** (stETH/ETH, cbETH/ETH : dépend de la profondeur d'un pool ou de places) ;
- le **taux de rachat × ETH/USD**, utilisé par Aave via CAPO, avec une croissance plafonnée par un `snapshotRatio` : une racine **unique par construction**, le contrat du protocole.

Binance est passé du premier au second après le 10/10/2025 [2nd].

## 2. Pour Shōgen : « écart » et « panne commune » sur un stablecoin

1. **Le dépeg n'est pas une défaillance de source** [inféré]. Quand toutes les places baissent ensemble, elles décrivent fidèlement un marché en crise. Les compter comme co-défaillance gonflerait K par le régime ; c'est la rupture de A(window-stationarity) que doc 04 §2 (b) anticipe.
   - **Dépeg** : état du marché, |médiane consolidée − 1| > d, avec une échelle publiée et datée. Seuils en usage chez les acteurs : 0,25 % (déviation Chainlink), 0,5 % (déclencheur Etherisc à 0,995 [2nd]), 1 % (gel LlamaRisk sous 0,99 [lu]), 2 % (« harmful » sous 0,98, Gauntlet [lu]). Kaiko pondère par le volume [lu] ; S&P : page et PDF en HTTP 403, manque déclaré.
   - **Écart de source** : écart à la médiane leave-one-out **de la même classe et de la même devise** au-delà de τ_classe, staleness, ou panne, avec la précédence de S2 inchangée. τ se dérive par la règle d'ADR-0029 §2.6 sur une calibration, jamais choisi ici. Ordre de grandeur à vérifier : dispersion calme de 0,9 point de base aujourd'hui, 0,06 % en médiane dans le rejeu calme [calc].
   - **Plafond** : un flux borné (1,05 $) qui cesse de se mettre à jour au-dessus de la borne est « plafonné », pas « en staleness ». Un nouveau statut à journaliser.
2. **Panne commune** : deux familles à ne jamais confondre.
   - (a) La co-panne d'infrastructure, comme en S2 (hôte, CDN, RPC partagés). Le cluster AS13335 de S2 couvre déjà Kraken, Coinbase, Bitfinex, CoinGecko, DefiLlama, OKX et le RPC public : les nouvelles classes héritent de ces racines.
   - (b) La co-déviation de contenu dans le même sens par des sources qui partagent une **devise de cotation**, une **conversion** (×USDT/USD), un **amont** (DefiLlama dérivé de CoinGecko) ou un **rail de règlement** (dollar fiat fermé le week-end).
3. **La stratification se heurte à la règle du calendrier.** Doc 04 exige des strates fixées ex ante, « jamais déduites des données », alors qu'un dépeg est imprévisible. Option [inféré] : une règle de régime pré-enregistrée, calculée sur un **ensemble témoin disjoint** du pool R1 (par exemple le pool Curve et Uniswap lu sur chaîne), avec les fenêtres « dépeg » censurées de R1 ou testées à part. C'est une décision de conception pour l'orchestrateur.

## 3. Recommandations

| # | quoi | pourquoi | comment | apport | coût | risques |
|---|---|---|---|---|---|---|
| **A** | Six classes, devise marquée, jamais fusionnées : **USDC/USD**, **USDT/USD**, **USDC/USDT**, **ETH/USD**, **LST/ETH marché** (stETH, cbETH, rETH, weETH ; wstETH par stETH × taux), **taux de rachat LST** (k nominal = 1 déclaré) | le rejeu montre qu'un mélange USD/USDT crée des co-déviations par construction (USDT à +1,6 %) | sources testées sans clé ce jour : USDT/USD : Kraken, Coinbase, Bitstamp, Gemini, Bitfinex, indice OKX, Crypto.com, CoinGecko, DefiLlama, Chainlink, RedStone ; USDC/USD : Kraken, Bitstamp, Bitfinex, CoinGecko, DefiLlama, Chainlink, RedStone ; USDC/USDT : OKX, Uniswap v3 et Curve sur chaîne ; LST : Chainlink (4 flux de marché), Curve stETH, CoinGecko, contrats de taux | rend lisible ce qui est réellement mesuré par classe ; ouvre les acheteurs stablecoin et LST (émetteurs, protocoles de prêt, trésoreries) | environ 30 décodeurs ; environ 10 `eth_call` par minute et par observateur ; budgets de débit très en deçà des limites (doc 10 §3.3) | USDC/USD fiat n'a que 3 places liquides (Coinbase absent) : N ≥ 4 répondantes atteint de justesse ; Binance et Bybit géo-bloqués depuis certains pays |
| **B** | Nouvel axe R2 **« devise et composition »** : arête `measured` quand une valeur est dérivée d'une autre classe (×USDT/USD) ; arête `doc` pour les compositions publiées (RedStone, CoinGecko) | Chainlink USDC/USD suit en stress la place USDT convertie (0,21 % contre 0,55-0,72 %) ; RedStone : 11 sources USDC sur 18 cotées en USDT | composition RedStone lue à chaque quorum (API publique) ; corrélation de contenu entre le flux d'oracle et chaque devise | c'est « Many lights. How many roots? » dans sa forme la plus vendable : *combien de devises de cotation derrière votre USDC/USD ?* | faible (lectures existantes) | une composition déclarée n'est pas mesurée (règle `basis:doc`, ADR-0008) ; l'attribution du comportement de Chainlink reste [inféré] |
| **C** | **ETH/USD comme seconde classe d'identification** de R1 | en S2, K était fait de pannes de transport (doc 11 §5.2) ; une co-panne simultanée sur BTC et ETH du même hôte désigne l'infrastructure, une co-déviation dans une seule classe désigne le contenu [inféré] | mêmes hôtes que BTC ; descriptif « co-écart inter-classe par hôte » pré-enregistré | aide à trancher la discordance que S2 n'a pas levée | quasi nul en collecte | une famille de tests plus grande (Bonferroni) : garder BTC confirmatoire et ETH descriptif, sauf calcul de puissance dédié |
| **D** | Écart en deux niveaux et statut « plafonné » (§2), règle de régime sur ensemble témoin, à verser au lot DOC04-REV | sans cela, un dépeg compterait comme co-défaillance, ou masquerait tout | textes de doc 04 §2 et ADR-0029 §2.2 ; seuils d au paquet | évite le faux positif structurel le plus probable du projet | rédaction | tension avec « strates jamais déduites des données » : arbitrage explicite requis |
| **E** | **Rejeu historique public des dépegs** (USDC 2023, USDT 2022, stETH 2022, USDe et wBETH 2025, cbETH 2026) | gratuit, recalculable, et fait voir aujourd'hui ce que S2-bis ne verra sans doute pas (pas de dépeg attendu en 16 semaines) | tours Chainlink lus sur chaîne (déjà fait) ; bougies Bitstamp, Bitfinex, Coinbase et OKX ; DEX via un nœud d'archive (à établir) | premier artefact « position institutionnelle » sur les stablecoins, sans VPS ; base des seuils d et τ | environ 1 à 2 semaines-lot [inféré] | les bougies ne sont pas des témoignages : à publier au rang descriptif ; reports de close ; trous d'historique (Kraken) |
| **F** | **Taux de rachat contre prix de marché** comme observable publié pour les LST | les incidents de 2024-2026 viennent de la racine unique du taux (CAPO, Moonwell) ou de la profondeur d'un seul pool (stETH 2022, ezETH 2024) | écart marché/rachat par fenêtre ; arête « racine unique : contrat X » nommée (ADR-0007) | nomme la racine plutôt que de la noter ; utile aux curateurs de marchés de prêt | faible | une erreur de composition (Moonwell) relève de A(typer-correctness), pas de l'indépendance : ne pas la vendre comme telle |

**Exclusions à confirmer ex ante** : Pyth (clé, ADR-0023) ; Chronicle (liste blanche de lecture) ; Kaiko et CF Benchmarks (payants, non essayés). Une seconde passerelle RPC hors AS13335 est à établir pour ne pas ajouter toutes les lectures sur chaîne au cluster Cloudflare (doc 11 §4.4).

## 4. Ce qui reste incertain

1. La méthodologie exacte de Chainlink pour USDC/USD (fournisseurs de données, poids des paires USDT) n'est pas publiée : l'attribution de 1.3 est une inférence sur un épisode.
2. Les bas par place de 2022 sont de seconde main. Sans historiques détaillés, pour le dire comme Protos, aucun chiffre de place n'est rejouable au trade près.
3. Ni la disponibilité d'un nœud d'archive public pour rejouer Curve et Uniswap, ni Binance et Bybit depuis les régions prévues par ADR-0029 n'ont été essayés.
4. Il est possible qu'aucun dépeg n'ait lieu pendant S2-bis. Les classes stablecoin mesureraient alors le calme, où l'axe hors-enveloppe risque de ne jamais tirer (même défaut qu'en S2, ADR-0029 §1.2 pt 6), et le pas de prix (1e-5) est proche de τ.
5. Les droits de redistribution des données de place restent la même question qu'en S2.
6. Textes réglementaires non détenus : déclaration ESMA du 17/01/2025 (restriction des stablecoins non conformes à MiCA) et GENIUS Act du 18/07/2025 (réserves 1:1, divulgation mensuelle), lus en seconde main seulement.

## 5. Trois questions à l'investisseur

1. Les classes stablecoin et ETH entrent-elles dans S2-bis comme **confirmatoires**, ce qui allonge la campagne ou réduit la puissance par la correction de Bonferroni, ou comme **descriptives** (benchmark), BTC restant seul juge ?
2. Pour le marché visé, « USDC/USD » doit-il s'entendre **contre le dollar fiat** (3 places liquides, Coinbase absent) ou **tel que la DeFi le consomme** (dominé par USDT) ? Le produit doit-il publier les deux et leur écart ?
3. Acceptez-vous de publier d'abord un **rejeu historique des dépegs** (descriptif, recalculable, sans témoignage attesté), comme premier artefact de position avant les données de S2-bis ?

## Sources (lues le 2026-10-04 sauf mention)

- **Chainlink** : reference-data-directory.vercel.app/feeds-mainnet.json ; data.chain.link/feeds/ethereum/mainnet/usdc-usd et usdt-usd ; docs.chain.link/data-feeds/selecting-data-feeds.
- **État de chaîne Ethereum** (via ethereum-rpc.publicnode.com) : `getRoundData` des proxys `0x8fFf…18f6`, `0x3E7d…e32D`, `0x8639…2812` ; contrats wstETH, rETH, cbETH, weETH ; Uniswap v3 `0x3416…27C6` ; Curve `0xbEbc…F1C7` et `0xDC24…7022`.
- **API publiques** : Kraken, Coinbase Exchange, Bitstamp, Gemini, Bitfinex, OKX, Crypto.com, CoinGecko, DefiLlama, api.redstone.finance.
- **Post-mortems et gouvernance** : chaoslabs.xyz/posts/chaos-labs-usdc-depeg-summary (30/03/2023) ; gauntlet.xyz/resources/aave-resilient-through-usdc-volatility (17/03/2023) ; comp.xyz/t/cip-4-upgrade-compound-v2-oracle-to-disable-uav/4728 (17/10/2023) ; governance.aave.com/t/…/24269 (10/03/2026) ; governance.aave.com/t/…/23303 (24/10/2025) ; forum.moonwell.fi/t/mip-x43-cbeth-oracle-incident-summary/2068 ; github.com/bgd-labs/aave-capo.
- **Kaiko** : kaiko.com/resources/defining-depegs-a-new-metric-for-stablecoin-stability (31/08/2023) ; kaiko.com/resources/the-data-behind-tethers-depeg (19/06/2023).
- **Presse et seconde main** : The Block 374278 et 374295 ; CoinDesk (11/03/2023 ; 10/03/2026) ; Protos (historique du peg USDT) ; 21Shares ; PANews ; DL News et Cointelegraph (ezETH) ; TechTimes (27/08/2026) ; arXiv 2606.07442 (sans données oracle).
- **Bloqué** : S&P Global, « Stablecoins: A Deep Dive into Valuation and Depegging » : HTTP 403, non contourné.
