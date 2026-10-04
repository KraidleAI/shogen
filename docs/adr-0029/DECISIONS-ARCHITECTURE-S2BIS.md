# Décisions d'architecture de S2-bis et du produit, après l'étude de marché à neuf profils (orchestrateur, 2026-10-04 05:46:42 UTC)

Statut : **proposées par l'orchestrateur** (choix techniques et de conception, délégués par l'investisseur le 2026-10-04 : « tu es
l architecte, le visionnaire, et le stratége ») ; soumises à une contre-expertise par un advisor frais, puis reportées dans
l'ADR-0029 (v3) avant le sceau de S2-bis ; les décisions de valeur restent à l'investisseur (§6). Heure produite par le script.

Pièces : neuf études (profils P1 à P8 et étude des sources candidates `docs/adr-0029/ETUDE-POOL-BIS.md`), croisement
(`docs/adr-0029/etude-marche/SYNTHESE-CROISEMENT.md`), ADR-0029 v2 validée, rapport de S2 `docs/11-mesures-pilotes.md`.
Réserve de provenance : trois profils (P1, P3, P7) ont tourné sous `claude-fable-5-1` ; deux de leurs faits sont contredits par les
pièces (C1 : les pannes Cloudflare et AWS d'octobre à décembre 2025 précèdent S2 d'environ dix mois, la mesure ne les a pas
« précédées » ; C2 : il n'existe pas de marché USDC-USD chez Coinbase, 404 mesuré par trois profils) ; leurs positions de marché sont
pondérées en conséquence, leurs faits non corroborés ne sont pas repris.

> **Révision datée du 2026-10-04 06:02:17 UTC (v2)** : contre-expertise d'un advisor frais (`docs/adr-0029/CONTRE-EXPERTISE-DECISIONS.md`) : « adopter avec corrections » ; **les dix-huit corrections sont adoptées par l'orchestrateur** et recopiées au §7 ; **là où le §7 et les §1 à §6 diffèrent, le §7 prévaut**. Conséquences principales : RedStone n'est pas une racine nouvelle (copie d'amonts du pool, il va à la carte) ; tout ajout au pool BTC exige niveau ≤ 0,01 et puissance non dégradée en simulation, et la licence lue ; le Root Count v0 part des données de S2 ; la gouvernance (méthodologie, changelog, réclamations, comité sans oracle, page de financement, règle « nulle partie mesurée ne paie sa propre mesure sans publication », préavis privé) est un livrable ; « appartenance déclarée aux amonts » est de rang R3 ; USDC/USDT entre comme témoin de la variable d'état ; un décrochage de l'USDT est nommé dans l'énoncé REJETTE de BTC ; nouveau cp-1 sur l'ADR-0029 v3 avant le sceau.

## 1. Ce que S2-bis décide, et comment (structure)

**D-1 — BTC décide seul ; ETH suit en séquence ; USDC et USDT sont mesurés en exploratoire** (option B du croisement, plan de P6
§3.1). « R1 discrimine (S2-bis) » reste défini **sur BTC/USD seul**, au seuil et à la puissance de l'ADR-0029 v2 (aucun α retiré).
ETH/USD est testé à 0,01 dans chaque strate **seulement si** BTC rejette dans cette strate (séquence fixe : P(au moins un rejet à
tort) ≤ 0,02 sous toute dépendance). USDC/USD et USDT/USD : moteur complet, sorties imprimées « hors décision ». Motif : une
classe par actif mais des tests fortement corrélés sur l'axe panne (même hôte) ; mettre quatre actifs au même rang diviserait le
seuil de BTC par quatre et casserait la cellule cible calculée à 0,01 (P6 §3.1 ; croisement §3, options C et D écartées).

**D-2 — Unité = hôte ; rotations jointes par hôte.** Toutes les séries d'un même hôte sont décalées du même pas dans toute
statistique multi-actifs (la co-panne structurelle d'un hôte n'est jamais comptée comme une co-défaillance : leçon OKX de S2).

**D-3 — Stablecoins : écart de source, pas écart au pair.** Même écart leave-one-out que pour BTC ; le décrochage du marché entier
(P_j = |médiane − 1|) est une **variable d'état** imprimée par fenêtre, avec une analyse conditionnelle exploratoire au-delà d'un
seuil scellé ; un flux plafonné par conception (Chainlink au-dessus de 1,05) est classé « borné », compté à part (P5, P6 ;
désaccord de P7 tranché : sous Knight & Leveson, la source fautive pendant un décrochage est celle qui reste à 1,000). Trois faits
mesurés pour les stables : USDC/USD et USDT/USD contre le dollar, et la devise de cotation comme axe R2 (D-6).

**D-4 — Calibration par actif avant le sceau (lot CALIB-ACTIFS).** τ et σ d'ETH, USDC et USDT ne peuvent pas venir de S2 :
historiques publics à une minute antérieurs à la campagne (Coinbase, Binance `data.binance.vision`, Kraken), règle
τ = arrondi supérieur de 1,5 × P99,9 ; planchers des oracles poussés (τ ≥ 1,5 × seuil de déviation ; σ = 1,5 × heartbeat :
ETH 5 400 s, USDC 124 200 s, USDT 129 600 s). Décalage du sceau : une à deux semaines.

**D-5 — Taille du pool BTC confirmatoire : 10 unités de l'ADR-0029, plus au plus cinq ajouts, seulement si la simulation de
puissance (P6 §3.4, en cours) montre que la puissance à la cellule cible n'est pas dégradée**, et seulement des ajouts qui
apportent une **racine nouvelle** : (a) une place décentralisée (pool Uniswap v3 WBTC/USDC ou cbBTC/USDC) lue par un RPC d'opérateur
distinct ; (b) RedStone lu **sur son contrat on-chain** (jamais sa passerelle) ; (c) une ou deux places constituantes des oracles et
des indices de référence hors du pool (Crypto.com, constituant du benchmark CME CF ; MEXC, hébergé hors Cloudflare). Sinon le pool
reste à 10 et ces sources vont à la carte descriptive (D-7). La décision finale tombe au retour de la simulation.

## 2. Ce que S2-bis cartographie (hors décision)

**D-6 — Deux axes R2 nouveaux** : (i) **devise de cotation** (USD contre USDT : six profils sur huit ; un mode commun mesurable,
notamment pendant un décrochage de l'USDT) ; (ii) **appartenance déclarée aux amonts d'oracles** (quelles places nourrissent quels
oracles et agrégateurs : Hyperliquid, Pyth, RedStone publient leurs sources ; Chainlink ne nomme plus ses agrégateurs).

**D-7 — Carte élargie descriptive, la donnée du produit** : toutes les sources lisibles sans clé et redistribuables, sur les quatre
actifs, hors du vote R1 : places (Bitget, KuCoin, Gate, HTX, Upbit, Bitso, MEXC, Crypto.com, Bybit si lisible depuis les
observateurs), agrégateurs (CoinPaprika seulement si la licence permet la republication ; GeckoTerminal), oracles (Chainlink sur
plusieurs chaînes, RedStone, DIA si sa licence est lue), Hyperliquid déclaré dérivé, DEX par chaîne. Pour chaque source : racines
déclarées, hébergeur et ASN mesurés, devise de cotation, cadence. Les sources à clé (CoinMarketCap, Kaiko, CoinAPI, Pyth, Chronicle
sur liste blanche) restent dehors : la règle « lisible sans clé, redistribuable » est le fondement de la recalculabilité (ADR-0003).

## 3. Actions tokenisées

**D-8 — Pas dans S2-bis ; campagne dédiée S3-actions, pré-enregistrée après le rendu de S2-bis.** Quatre classes de fait séparées
(sous-jacent, jeton par chaîne et par place, écart jeton/sous-jacent normalisé par le multiplicateur, valeur de l'émetteur) ; marché
fermé ou pause annoncée = état, pas panne ; pilotes SPY, NVDA, TSLA (P8). Motif : calendrier de marché, multiplicateurs différents
selon la chaîne, racines sous licence ; mais l'apport produit est fort, puisque les oracles déclarent eux-mêmes une racine unique.
Questions juridiques et de licence à l'investisseur (§6).

## 4. Produit (ordre de sortie)

**D-9** — (1) **Rejeu historique public et recalculable des décrochages 2022-2026** (USDC mars 2023, USDT mai 2022, stETH 2022) :
gratuit, sans VPS, faisable maintenant, première démonstration de la méthode sur des épisodes réels (P5). (2) **Benchmark public
« Root Count »** : classement daté de la lisibilité et de la concentration des sources par actif (carte D-7), méthodologie publiée
et versionnée, changelog, procédure de réclamation (forme IOSCO, sans statut d'administrateur BMR : P3, P7). (3) **Sorties machine
gratuites** : attestation JSON signée, vérificateur hors ligne, serveur MCP en lecture seule pour les agents (P2). (4) **Payant,
après un premier recalcul externe** : rapport de concentration sur pool nommé, dossier de preuve DORA (chaîne de sous-traitance
au format B_05.01/B_05.02), surveillance. (5) **Certificat R1 + R2** seulement après un S2-bis décisif.

## 5. Ce qui change dans l'ADR-0029 (v3)

Classes et rôles (D-1) ; rotations jointes (D-2) ; définitions par classe et variable d'état (D-3) ; lot CALIB-ACTIFS et décalage du
sceau (D-4) ; pool BTC selon la simulation (D-5) ; axes R2 et carte descriptive (D-6, D-7) ; débit : requêtes groupées par hôte
quand l'API le permet (CoinGecko obligatoire), forme de requête par (hôte, actif) scellée ; journaux environ × 4 (sous les quotas
lus) ; budget VPS inchangé (aucun observateur de plus) ; coût d'ingénierie ≈ + 700 lignes.

## 6. Décisions de valeur pour l'investisseur (issues de l'étude ; en plus des huit de l'ADR-0029 §6)

1. Premier acheteur visé dans les 12 mois : oracle challenger, protocole (Spark ou Aave V4) ou acteur régulé (sponsor d'ETF, CASP
   sous DORA, banque exposée à USDC).
2. Nommer publiquement les acteurs mesurés (protocoles, plateformes d'agents, administrateurs régulés), avec préavis privé, ou
   anonymiser.
3. Financements d'acteurs mesurés, déclarés et publiés (modèle L2BEAT), ou exclusion stricte.
4. Assurance indépendante (ISAE 3000 / SOC 2) avant ou après le premier client payant.
5. Sources qui interdisent la republication : publier des empreintes et des valeurs dérivées, ou les retirer (recommandation de
   l'orchestrateur : les retirer de la mesure, les citer comme amonts déclarés).
6. Actions tokenisées : périmètre juridique (produits interdits aux résidents américains, ou actions natives d'abord) ; sous-jacent en
   différé de 15 minutes gratuit, ou licence payante qui rend une partie des journaux non republiable.

## 7. Corrections adoptées après contre-expertise (prévalent sur les §1 à §6)

| # | décision | texte actuel | texte proposé |
|---|---|---|---|
| 1 | D-1 | « ETH/USD est testé à 0,01 dans chaque strate seulement si BTC rejette dans cette strate » | ajouter : « ; énoncés d'ETH scellés au paquet (registre doc 09), cellule cible et puissance d'ETH imprimées (P6 §3.6 pt 7) ; le co-écart inter-classe par hôte (P5 C) est imprimé en descriptif ; limite écrite : les quatre classes partagent la même couche de livraison » |
| 2 | D-1 | « croisement §3, options C et D écartées » | « options C et D écartées : D pour la perte de puissance BTC (Holm 0,0025) ; C (Westfall-Young) pour la complexité de scellement, sa puissance sous corrélation n'étant pas chiffrée ; C reste en sensibilité (P6 §3.6 pt 8) » |
| 3 | D-3 | « Trois faits mesurés pour les stables : USDC/USD et USDT/USD contre le dollar, et la devise de cotation comme axe R2 » | « Quatre : USDC/USD, USDT/USD, **USDC/USDT (OKX, Uniswap, Curve : ensemble témoin de la variable d'état, hors des classes USD)**, devise de cotation ; limites écrites : pool USDC/USD fiat à trois places, pas de prix 1e-5 près de τ » |
| 4 | D-3 | (fin) | ajouter : « Pour BTC, un décrochage de l'USDT atteint les unités binance et okx ensemble ; l'énoncé REJETTE nomme ce cas (« co-défaillance de cotation ») et la sensibilité « USD seules » est imprimée avec le verdict » |
| 5 | D-4 | « Décalage du sceau : une à deux semaines. » | « Décalage du sceau : une à deux semaines, **si** le lot CALIB-ACTIFS établit d'abord (G0) l'existence d'historiques à 1 minute pour ≥ 4 places par classe ; sinon ETH et stables passent en seconde vague et le sceau BTC n'est pas décalé. Deux méthodes de τ (cellules de S2 pour BTC, clôtures de bougies pour les autres) : τ non comparables entre classes, déclaré ; τ des agrégateurs et oracles sur ETH et stables = planchers seuls, axe hors-enveloppe des oracles stables aveugle par construction » |
| 6 | D-5 | « (b) RedStone lu sur son contrat on-chain (jamais sa passerelle) » | « (b) RedStone contrat : **copie d'amonts du pool (EP §3), pas une racine nouvelle** ; va à la carte D-7 sauf page primaire de l'adresse et paramètres lus » |
| 7 | D-5 | « seulement si la simulation de puissance … montre que la puissance à la cellule cible n'est pas dégradée » | « seulement si SIM-NIVEAU-BIS et SIM-PUISSANCE-BIS, rejoués sur la cellule cible redéfinie, montrent un **niveau ≤ 0,01 et** une puissance non dégradée ; et si la licence de redistribution est lue (EP C4) ; décision à écrire au paquet, non ici » |
| 8 | D-6 | « (ii) appartenance déclarée aux amonts d'oracles » | « (ii) appartenance déclarée aux amonts d'oracles, **rang R3** (`basis:doc`, ne fusionne pas) ; devient R2 seulement par corrélation de contenu mesurée » |
| 9 | D-7 | « CoinPaprika seulement si la licence permet la republication » | « CoinPaprika exclu (redistribution Enterprise seule, EP §2.2) ; RedStone **contrat** seulement » |
| 10 | D-7 | « la règle « lisible sans clé, redistribuable » est le fondement de la recalculabilité (ADR-0003) » | ajouter : « ; elle n'est établie sur pièce pour aucune source nouvelle ni pour CoinGecko (SHOGEN-S2BIS-LICENCES-API-1) : lecture des conditions **avant** l'entrée à la carte ; relevé descriptif actions (P8 R1) admis à la carte » |
| 11 | D-7/D-9 | (absent) | « La carte lue par les observateurs de S2-bis n'est servie qu'au rendu unique (ADR §7). Le Root Count v0 part des données de S2 (J28) ; la carte S2-bis le met à jour après le rendu, ou est collectée hors paquet sur un flux déclaré non scellé » |
| 12 | D-9 | « Rejeu historique … première démonstration de la méthode » | « Rejeu historique au rang descriptif (bougies, pas des témoignages), publié comme **test public de la variable d'état D-3** » |
| 13 | D-9 | « Benchmark public « Root Count » : classement daté » | « compte de racines par actif et par feed, daté (nommer, jamais noter, ADR-0007) » |
| 14 | D-9 | « attestation JSON signée » | « attestation portable recalculable, champ `non_claims` obligatoire ; signature = cache (doc 04 §5) » |
| 15 | D-9 | « dossier de preuve DORA (chaîne de sous-traitance au format B_05.01/B_05.02) » | « export au format du registre d'information (B_05.01/B_05.02), sans prétention au statut de sous-traitant, texte DORA détenu avant toute phrase commerciale » |
| 16 | D-9 | (absent) | ajouter aux livrables gratuits : méthodologie v1.0, changelog, réclamations, **comité sans oracle, page de financement, règle « nulle partie mesurée ne paie sa propre mesure sans publication », préavis privé de 14 à 30 jours** ; fiche de racines par actif avec taux de rachat LST (P1 R-7, P5 F) |
| 17 | §6 | six questions | ajouter : séquencement (sceller BTC maintenant ou décaler pour les quatre actifs) ; définition d'USDC (fiat / DeFi / les deux) ; accepter une mesure stablecoin « rien à signaler » ; clés payantes ou non ; aucun revenu protocole avant 2027 ; temps borné pour les agents ; q.1 : nommer le risque de capture pour « oracle challenger » |
| 18 | §5 | « coût d'ingénierie ≈ + 700 lignes » | « ≈ + 700 à 900 lignes pour les quatre actifs (P6 §3.6) **plus** un décodeur, ses fixtures, un smoke et une page de licence par source de la carte (EP §7) ; ADR §6 q.3 passe à 9-10 semaines de préparation si D-4 bloque le sceau » |

## 8. Décision finale sur D-5 (ajout daté du 2026-10-04 06:16:47 UTC, retour de la simulation de P6)

Simulation synthétique de P6 (`docs/adr-0029/etude-marche/P6-MESURE.md` §3.4, script `calc/sim_pool.py`) : la puissance de la statistique K≥2 de R1-2 à la cellule cible est de 0,91 à 10 unités et 16 semaines (chiffre de l'ADR retrouvé), mais tombe à 0,54 à 25 unités ajoutées hors du mode commun et à 0,03 à 25 unités ajoutées dans le mode commun ; la statistique des paires coïncidentes S = Σ C(m_j, 2) reste entre 0,96 et 1,00 ; niveau tenu par les trois statistiques sous H0 (0,003 à 0,010 pour 0,01) ; quatre classes confirmatoires sous Holm coûteraient environ 10 points de puissance à BTC en calme et 27 en stress (option D écartée, chiffre à l'appui). **Décision : le pool BTC confirmatoire reste à 10 unités** ; aucun ajout au vote ; les candidats de D-5 (DEX, places constituantes, RedStone contrat) vont à la carte descriptive D-7. La statistique S est évaluée par SIM-PUISSANCE-BIS comme sensibilité, et comme statistique de décision seulement pour une campagne ultérieure à pool élargi. Sources de la loi par rotations trouvées par P6 (Harris arXiv:2012.06862 ; Kalyuzhny, doi 10.1111/geb.13083 ; Mrkvička et al. arXiv:1911.00240) : à verser pour SHOGEN-S2BIS-ROTATION-SOURCE-1 ; SIM-NIVEAU-BIS compare la rotation enroulée à la variante non enroulée de Harris.
