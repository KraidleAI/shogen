# P8 — Actions tokenisées : les inclure dans Shōgen, quand et comment

> *Note de versement de l'orchestrateur* : citations de pages web non versées à `biblio/` passées de « … » à “…” (gate S-G5) ; lectures [lu] web du rapport, copies hors dépôt.

- **Gate 0** : modèle résolu `claude-opus-5-5` (chercheur P8). Date : 2026-10-04 ; sondes faites entre 05:11 et 05:14 UTC, un **dimanche**, marché américain fermé.
- **Brief** : `BRIEF-P8-ACTIONS-TOKENISEES.md`, sha256 `2edc34e5…87eaf` (empreinte vérifiée).
- **Exposition** : je n'ai ouvert aucune pièce de `docs/15-*`, `docs/16-*`, `docs/rapports/`, `docs/adr-0025/` ou `docs/adr-0028/monark-m009a/`, ni aucun `*.jsonl`. Pièces du dépôt lues : docs 02 (vision), 10 §2-3, 11 §1-2 et §4, `adr-0028/AVIS-PRODUIT-APRES-S2.md`, ADR-0029 §1.3, §2.1 et §2.5, ADR-0023 (invariant « sans clé ») ; doc 04 et doc 07 survolés par grep.
- **Niveaux** : [lu] = lu sur la source primaire ou observé par une sonde sans clé ; [2nd] = presse ou tiers ; [inféré] = mon raisonnement ; [calc] = calcul fait sur des valeurs [lu]. Notes de lecture, PDF et sorties brutes : `P8-ACTIONS-TOKENISEES/web/` (`notes-lectures.md`, `snapshot-2026-10-04.txt`, `cl-eth.json`, `cl-eth-equity.txt`, `sec-iex-2025-21.pdf`, `esma-trv-2-2026.pdf`).

## Résumé (10 lignes)

1. Le marché est réel mais petit : 3,22 Md$ d'encours distribué (rwa.xyz, 2026-10-04 [lu]) ; l'ESMA compte ~1,9 Md€ fin juin 2026, soit 6,5 fois plus en 18 mois [lu].
2. Il est concentré chez quelques émetteurs : Ondo, bStocks (Binance), xStocks (Backed, groupe Kraken), Securitize et Robinhood. Presque tous émettent des **titres de dette ou des certificats** adossés à des actions détenues par un dépositaire, pas des actions [lu].
3. La lecture du prix dépend de l'émetteur et de la chaîne. Le prix d'un jeton est le cours de l'action multiplié par un **multiplicateur** (dividendes réinvestis, splits), et la façon d'appliquer ce multiplicateur change selon la chaîne [lu].
4. La thèse de Shōgen se vérifie ici dans les textes mêmes des oracles. Chainlink écrit « Single provider for Extended & Overnight Data » ; ses flux en heures régulières sont « multi-sourced from consolidated tape data », c'est-à-dire tirés d'une seule bande consolidée ; Pyth a l'exclusivité on-chain des données de nuit de Blue Ocean ATS jusqu'à fin 2026 [lu/2nd]. On voit plusieurs flux, mais très peu de racines.
5. Côté accès sans clé : Pyth est devenu payant (31 juillet 2026) et les Data Streams de Chainlink demandent une clé. Restent lisibles sans clé les Data Feeds Chainlink on-chain (25 flux actions sur Ethereum), les places crypto, les agrégateurs et les DEX [lu].
6. La donnée boursière elle-même (bande consolidée SIP, flux des bourses) est sous licence payante. Le différé de 15 minutes d'IEX est gratuit [lu]. La règle « lisible sans clé et redistribuable » exclut donc la racine du sous-jacent, sauf par des voies indirectes.
7. **Recommandation** : ne pas mettre les actions tokenisées dans le volet confirmatoire de S2-bis. Les traiter dans une **campagne dédiée (S3-actions), pré-enregistrée après S2-bis**, éventuellement précédée d'un relevé descriptif hors décision.
8. Classes de fait proposées : prix de référence du sous-jacent, prix du jeton (par chaîne et par place), **écart jeton/sous-jacent normalisé par le multiplicateur**, et valeur publiée par l'émetteur.
9. Règle centrale : un marché fermé, ou une pause annoncée pour une opération sur titres, est un **état** et non une panne. La panne se juge contre un calendrier et contre le champ `marketStatus`.
10. Actifs pilotes : SPY (ETF à dividendes, qui fait jouer le multiplicateur), NVDA (jeton le plus échangé dans l'instantané Kraken) et TSLA (sans dividende, sert de témoin du multiplicateur).

## 1. Paysage (émetteurs, structures, chaînes, encours)

| émetteur / produit | structure juridique | juridiction, accès | chaînes | encours (rwa.xyz 2026-10-04 [lu]) |
|---|---|---|---|---|
| **Ondo Global Markets** | « a structured note: a debt instrument » émise par Ondo Global Markets (BVI) Ltd ; adossement 1:1 chez un broker-dealer américain ; Security Agent Ankura ; droit de rachat “for the then-value of the underlying assets” [lu docs.ondo.finance] | Reg S, personnes non américaines | Ethereum, BNB Chain, Solana [2nd] | 922,5 M$, 408 actifs |
| **bStocks** (Binance) | certificat BEP-20 « 1:1-backed … held by a regulated custodian » (dépositaire non nommé) [lu bnbchain.org] ; émetteur BTECH Holdings Ltd, SPV [2nd] | n.d. | BNB Chain | 851,3 M$, 87 actifs |
| **xStocks** (Backed Assets (JE) Ltd, groupe Kraken [2nd]) | « bearer debt instrument classified as a tracker certificate » ; prospectus FMA Liechtenstein ; Security Agent [lu docs.xstocks.fi] | hors U.S. Persons | EVM (Ethereum, Arbitrum, BSC : même adresse SPYx), Solana, TON, HyperEVM [lu CoinGecko] | 582,6 M$, 1 271 actifs |
| **Securitize** | inclut SECZ, action Securitize cotée au NYSE ; « tokenized shares represent the same NYSE-listed equity » [lu RedStone] : émission native | n.d. | Avalanche, Solana [2nd] | 432,4 M$, 3 actifs (dont SECZ 355,6 M$) |
| **Robinhood Stock Tokens** | « tokenised debt securities issued by Robinhood Assets (Jersey) Limited », sans droit sur l'émetteur sous-jacent ; souscription réservée aux Authorised Participants [lu docs.robinhood.com] | interdit aux États-Unis, au Canada, au Royaume-Uni et en Suisse | Arbitrum, puis Robinhood Chain (Arbitrum Orbit, mainnet juillet 2026 [2nd]) | 142,6 M$, 189 actifs |
| Dinari (dShares) | broker-dealer enregistré à la SEC (juin 2025) ; 724 actions ouvertes aux investisseurs américains le 4 août 2026 [2nd] | États-Unis éligibles | Ethereum, Arbitrum [2nd] | non listé dans l'extrait |
| Superstate Opening Bell | émission native d'actions enregistrées à la SEC [2nd] | n.d. | Solana, Ethereum | non listé dans l'extrait |

- **Vue d'ensemble [lu rwa.xyz]** : 3,22 Md$ d'encours distribué (+9,4 % sur 30 j) ; 12,08 Md$ de transferts mensuels (−66,8 % sur un mois) ; 4,22 M de détenteurs ; 7 845 produits recensés. La ventilation par chaîne n'est pas visible sans compte (manque déclaré). Le chiffre « BNB Chain ≈ 1 Md$, ≈ 34 % » est [2nd].
- **Cadre réglementaire.** Le 18 mars 2026, la SEC a approuvé la règle Nasdaq : actions du Russell 1000 et ETF d'indices tokenisés, échangés « on the same order book » à condition d'être fongibles, avec le même CUSIP et les mêmes droits ; la règle s'appuie sur le pilote de la DTC [2nd juridique, Dechert]. Pour l'ESMA [lu, TRV n°2 2026, p. 47-48], les structures « wrapped » dominent, l'émission native est « rare », et « token transfers do not convey legal title » ; elle signale le risque de fragmentation entre représentations non fongibles d'une même action, « particularly in periods of stress ».
- [inféré] Il faut donc distinguer deux familles qui ne posent pas le même problème de prix. La plupart des produits sont des **créances sur un SPV** : leur prix est un dérivé du sous-jacent, plus un risque émetteur et un risque de dépositaire. Les **actions natives** (SECZ, Opening Bell, futur Nasdaq/DTC) sont l'action elle-même, inscrite sur une autre chaîne d'enregistrement.

## 2. Comment le prix se forme et se lit

**Sessions.** Chainlink distingue un régime « regular 9:30–16:00 » et un régime 24/5 : pré-marché 4:00–9:30, post-marché 16:00–20:00 et nuit 20:00–4:00 du dimanche soir au vendredi matin. Le champ `marketStatus` vaut 0 (inconnu), 1 (pré), 2 (ouvert), 3 (post), 4 (nuit) ou 5 (fermé). La documentation prévient : “Do not use `observationsTimestamp` … timestamps indicate when data was last recorded, not whether the market is currently active” [lu docs.chain.link/data-streams/market-hours].

**Comportement des oracles.**
- **Chainlink Data Feeds (on-chain).** Le flux rapporte “the last onchain value published before the market closed”. Il ne publie aucune mise à jour pendant la fermeture, « including heartbeat updates ». Les heures régulières sont « Multi-sourced from consolidated tape data » ; les sessions étendues et de nuit « may be sourced from fewer providers ». La documentation prévient aussi d'« a reported price of zero » dans des cas limites [lu docs.chain.link/data-feeds/tokenized-equity-feeds].
- **Classement de risque Chainlink.** Les 25 flux actions sur Ethereum sont tous classés `new` ou `custom` (heartbeat 86 400 s, seuil 0,5 %) [lu, annuaire `feeds-mainnet.json`]. Chainlink définit « Custom » comme pouvant « differ materially from standard market price feeds » et demande d'évaluer “the risk of single source feeds” [lu].
- **Chainlink Data Streams 24/5.** On y lit « Single provider for Extended & Overnight Data » ; le week-end, « all three feeds will carry stale values » ; en début de nuit, des valeurs `mid` atypiques, « including zero », peuvent apparaître. L'accès se fait **par identifiants API** [lu, guide 24/5].
- **Pyth.** Les flux de séance étendue sont passés en offre Pro le 15 juin 2026. Depuis le 31 juillet : « all Pyth Core data access requires an active Starter or Pro plan » (U.S. Equities 5 000 $/mois) [lu, blog Pyth du 12 juin 2026]. Les données de nuit viennent de Blue Ocean ATS, en exclusivité on-chain jusqu'à fin 2026 [2nd, annonce Pyth].
- **RedStone.** Pour les actifs sans marché continu, RedStone propose le « TSSO » : « NAV originates from a single authoritative source ». Le flux SECZ est un flux de clôture quotidienne [lu blog RedStone]. Le modèle est **mono-source par construction**.

**Multiplicateur et opérations sur titres.**
- Ondo : « Token Price = Underlying Equity Market Price × Multiplier (sValue) », avec un multiplicateur tiré du contrat `SyntheticSharesOracle` d'Ondo. Pendant une opération sur titres, le prix est figé « at the last known good value » jusqu'à une reprise manuelle [lu docs.chain.link/…/ondo].
- Robinhood : « underlying share price times the multiplier » ; solde brut statique (`uiMultiplier`, ERC-8056) ; oracle « paused » pendant les opérations sur titres [lu docs.robinhood.com].
- xStocks : dividendes réinvestis nets de retenue à la source, appliqués par le multiplicateur à « 00:30 UTC » le lendemain de la date ex. **Sur EVM, le solde est ajusté par le contrat ; sur Solana et TON, le solde reste constant et le multiplicateur est dans les métadonnées** [lu docs.xstocks.fi].
- [inféré] Conséquence : un même ticker (SPYx) n'a pas la même unité de prix selon la chaîne. Comparer des flux sans normaliser par le multiplicateur crée de faux écarts.

**Prix observés le dimanche 2026-10-04, 05:11-05:14 UTC (une seule prise, aucune inférence statistique)** [lu ; ratios calc] :

| objet | valeur | ratio à la clôture SPY du vendredi (769,64, Cboe différé) |
|---|---|---|
| Chainlink SPY-USD (24/5), Ethereum | 770,614, mis à jour 2026-10-02T12:30Z | 1,0013 (valeur figée **avant** la clôture : seuil de 0,5 % non franchi) |
| Kraken SPYx/USD (place centralisée) | 770,74 ; 97 transactions sur 24 h | 1,0014 |
| SPYx sur les DEX Solana (Raydium, Orca, Meteora…) ; CoinGecko | ≈ 774,8 ; 774,92 | 1,0067-1,0069 |
| Chainlink SPYon (Calculated) / SPYon (Ondo API) | 776,789 / 777,330 (ce dernier mis à jour **samedi** 12:31Z) | 1,0080 (rapporté au flux SPY) |

- [inféré, à vérifier] L'écart d'environ 0,5 % entre Kraken et les DEX Solana pour le même SPYx est cohérent avec la différence de représentation du multiplicateur, ou avec un simple écart de week-end. Une prise unique ne permet pas de trancher.
- La valeur on-chain de Chainlink, le week-end, **n'est pas la clôture** : c'est la dernière valeur poussée par le seuil d'écart.
- Les flux « (Ondo API) » se mettent à jour pendant la fermeture du marché (STRCon : dimanche 01:12Z). Ce sont des prix de l'émetteur, pas des prix de marché.

**Incidents documentés.**
- Ventuals, marché perpétuel SPACEX-USDH sur Hyperliquid, 28 mai 2026 : le split 5:1 n'a pas été intégré par le fournisseur hors chaîne Notice.co, l'une des composantes de l'oracle ; le prix a chuté de 45 %, avec 1,51 M$ liquidés et 405 traders touchés [2nd, cryptotimes.io ; post-mortem primaire non trouvé].
- Les documentations primaires citées plus haut décrivent elles-mêmes d'autres modes de défaillance : prix zéro, valeurs figées, pauses manuelles.
- Je n'ai trouvé aucun post-mortem primaire portant sur un écart xStocks, Ondo ou bStocks (manque déclaré).

## 3. Indépendance des sources : combien de racines ?

| session | racines observables sur pièce | conséquence pour k_eff |
|---|---|---|
| heures régulières | la bande consolidée (SIP CTA/UTP), qui agrège les bourses ; Chainlink se dit « multi-sourced from consolidated tape data » | [inféré] des flux nominalement multiples (Chainlink, Pyth, Cboe, agrégateurs, jetons) remontent largement à **une racine de prix** ; seule exception visible : une bourse lue en propre (IEX, Cboe) |
| pré- et post-marché | « fewer providers », « single provider » (Chainlink) | k_eff ≈ 1 par oracle, selon la déclaration de l'oracle lui-même |
| nuit (20:00-4:00 ET) | Blue Ocean ATS (exclusif chez Pyth jusqu'à fin 2026) ; fournisseur unique non nommé chez Chainlink | une ou deux racines au plus, identité incomplète |
| week-end et jours fériés | **aucune** racine de sous-jacent ; seuls existent les prix des jetons (DEX, places crypto, cotation de l'émetteur) | le « prix » est une formation propre au marché crypto ; une valeur figée est attendue, ce n'est pas une panne |
| opérations sur titres | multiplicateur publié par **l'émetteur** (Ondo `SyntheticSharesOracle`, `uiMultiplier` Robinhood, métadonnées xStocks) | racine unique, l'émetteur, pour chaque jeton |

**Licences.**
- La bande consolidée est payante : 1 000 $/mois de redistribution par réseau au barème CTA [2nd, recherche ; barème non lu à la source].
- IEX : « Delayed IEX Market Data » (au moins 15 min) est gratuite, et IEX « does not … charge fees for, its "Delayed" market data products » ; en temps réel, DEEP+ coûte 3 500 $/mois depuis le 1er octobre 2025 [lu, SEC Release 34-103807]. La redistribution gratuite avec attribution « Data provided for free by IEX » est [2nd]. Le statut tarifaire de TOPS en 2026 et le mode d'accès HTTP sans compte ne sont pas établis.
- Cboe sert un JSON différé sans clé (`cdn-api.cboe.com/api/global/delayed_quotes`, HTTP 200 [lu]), mais je n'ai pas lu ses conditions d'utilisation.

**Ce que cela implique pour l'invariant « strictement sans clé » (ADR-0023) et la publication des octets bruts (ADR-0003/0005)** [inféré] :
- Sont publiables : les valeurs on-chain (Chainlink Data Feeds, multiplicateurs), les tickers des places crypto et des DEX, et probablement le différé IEX avec attribution.
- Ne le sont pas, ou restent douteux : les flux temps réel de la bande consolidée, Pyth (« No redistribution rights », ADR-0029 §2.5) et les Data Streams.
- Shōgen peut donc mesurer la **chaîne jeton → oracle → émetteur**. Il ne mesure le sous-jacent qu'à travers des intermédiaires, ou avec un différé de 15 minutes. C'est à écrire comme axe non mesuré, à son rang.

## 4. Recommandations

**R1 — S2-bis : ne pas inclure les actions tokenisées dans le volet confirmatoire.**
- Pourquoi : ADR-0029 vise à rendre la règle R1 décisive sur des classes à marché continu 24/7. Les actions introduisent un calendrier (sessions, fermetures, pauses), une normalisation par multiplicateur et des racines sous licence. Sans pré-enregistrement propre, ce sont trois sources nouvelles d'écarts mal définis ; S2 a montré qu'un écart mal défini mesure l'observateur (avis produit §1) [inféré].
- Option à coût marginal faible : un **relevé descriptif hors décision** sur les observateurs de S2-bis, avec 3 pilotes et 6 à 8 flux sans clé (voir R3). Il ne sert qu'à mesurer la disponibilité, à figer les définitions d'état et à dimensionner S3-actions. À annoncer au paquet comme « hors famille, hors décision », ou à exécuter à part.
- Ce que ça coûte : quelques décodeurs et un module calendrier ; aucun achat [inféré].

**R2 — Campagne S3-actions, pré-enregistrée après le rendu de S2-bis.**
- Classes de fait, une par grandeur, jamais mélangées :
  - F1, prix de référence du sous-jacent ;
  - F2, prix du jeton, avec émetteur, chaîne et place marqués par relevé (comme la devise en S2, doc 10 §2) ;
  - F3, écart normalisé `e = prix_jeton / (prix_sous-jacent × multiplicateur) − 1` ;
  - F4, valeur publiée par l'émetteur (flux « Ondo API », NAV, prix de rachat).
- **Définition d'état avant la définition d'écart** :
  - fermé (calendrier NYSE et `marketStatus` = 5) ;
  - pause d'opération sur titres annoncée (≥ 24 h à l'avance chez Ondo) ;
  - session étendue ou de nuit, marquée « mono-fournisseur déclaré ».
- La panne se mesure seulement à l'état « ouvert » : non-réponse vue par au moins 2 observateurs, conformément à l'écart à quorum d'ADR-0029. Un prix nul ou négatif compte comme panne. La staleness est jugée contre la cadence propre à chaque session, et jamais le week-end.
- La strate de stress de S2 (le week-end) devient ici une strate « marché fermé », où seuls F2 et F3 existent. C'est d'ailleurs la question à forte valeur : **que vaut un jeton quand sa racine dort ?**

**R3 — Pool candidat (vérifié sans clé le 2026-10-04 [lu]).**
- Chainlink Data Feeds sur Ethereum, lus par `eth_call` comme en S2 : SPY-USD, NVDA-USD et TSLA-USD (24/5) ; SPYon et TSLAon (Calculated) ; SPYon et TSLAon (Ondo API).
- Kraken : xStocks NVDAx, SPYx et TSLAx (354 paires `tokenized_asset`).
- CoinGecko et DefiLlama, tout en notant que DefiLlama = f(CoinGecko) pour ces identifiants, comme pour BTC.
- Une lecture DEX Solana par une voie sans clé à établir.
- Multiplicateurs on-chain.
- Sous-jacent : IEX différé ou Cboe différé, sous réserve des conditions d'utilisation.
- Exclus : Pyth (payant) et Data Streams (clé). Bybit est bloqué géographiquement depuis le conteneur (CloudFront) ; il est peut-être lisible depuis les observateurs hors des États-Unis d'ADR-0029, à tester. Binance bStocks n'a pas été testé.

**R4 — Ce que cela apporte au produit** [inféré] :
- La mesure R2 (racines et ASN) est la plus vendable : les oracles déclarent eux-mêmes leurs racines uniques (« single provider », « single authoritative source »), et Shōgen peut les publier datées et recalculables.
- Acheteurs :
  - (a) protocoles qui acceptent ces jetons en garantie : Venus et Lista sur BNB Chain [lu], Kamino et Loopscale [2nd], les marchés DeFi de Robinhood Chain ;
  - (b) émetteurs (Ondo, Kraken/Backed, Robinhood) qui veulent montrer la qualité de leur chaîne de prix ;
  - (c) marchés perpétuels HIP-3, que l'incident Ventuals concerne directement ;
  - (d) acteurs régulés, l'ESMA ayant nommé la fragmentation comme risque.
- C'est un deuxième terrain réel pour la thèse de Knight & Leveson, hors crypto pure.

**R5 — Coût et risques.**
- Coût (estimé sans devis) [inféré] :
  - un module calendrier (jours fériés NYSE, demi-séances) ;
  - des lecteurs RPC pour 2 à 4 chaînes de plus (Arbitrum, BNB, Solana, Robinhood Chain), chacune avec son caveat « chemin de lecture ≠ amont » ;
  - une revue juridique des conditions d'utilisation (IEX, Cboe, conditions des oracles) avant toute publication d'octets bruts.
- Risques :
  - **licences** : publier des octets sous licence ;
  - **juridique** : prix de produits non offerts aux personnes américaines ; neutralité de Shōgen à garder (« qualifie, ne choisit pas », doc 02) ;
  - **fragmentation** : un même ticker sur N chaînes, avec N multiplicateurs ;
  - **évolution rapide** : pilote Nasdaq/DTC, changements tarifaires d'oracles (Pyth a basculé en deux mois) ;
  - un marché de 3 Md$, encore petit par rapport aux stablecoins.

## 5. Ce qui reste incertain

- Je n'ai pas vu la ventilation par chaîne ni par détenteur sur rwa.xyz (compte requis).
- Je n'ai trouvé ni l'identité du fournisseur unique de Chainlink pour les sessions étendues et de nuit, ni l'oracle utilisé par Venus et Lista pour les bStocks.
- Je n'ai pas lu le barème CTA ni les conditions d'utilisation de Cboe et d'IEX à la source. Le statut de TOPS reste inconnu.
- L'explication de l'écart Kraken/Solana sur SPYx, qui tient au multiplicateur selon mon hypothèse, n'est pas vérifiée.
- Les pages de Bybit (blocage géographique), Superstate, Dinari et Securitize n'ont pas été lues à la source (seulement [2nd]). Je n'ai trouvé aucun post-mortem primaire Ventuals.
- Les ratios du §2 viennent d'une prise unique, un dimanche : ils décrivent un instant et ne mesurent pas un écart typique.

## 6. Trois questions à l'investisseur

1. **Périmètre juridique** : Shōgen peut-il publier, gratuitement, des mesures sur des produits interdits aux personnes américaines (xStocks, Ondo, Robinhood) ? Faut-il au contraire commencer par les actions natives (SECZ, Opening Bell, pilote Nasdaq/DTC), plus petites mais au statut plus clair ?
2. **Invariant « sans clé »** : accepte-t-on que le sous-jacent ne soit lu qu'en différé de 15 minutes (IEX/Cboe), ou indirectement par les oracles on-chain ? Ou bien finance-t-on une licence de données (par exemple 5 000 $/mois chez Pyth), ce qui rend une partie des journaux non redistribuable ?
3. **Acheteur visé en premier** : protocoles de prêt qui acceptent ces jetons en garantie, émetteurs, ou marchés perpétuels ? La réponse fixe les pilotes (chaîne BNB et bStocks, Ethereum et Ondo, ou Solana et xStocks) et la classe de fait prioritaire (F3, l'écart, ou F4, la valeur de l'émetteur).
