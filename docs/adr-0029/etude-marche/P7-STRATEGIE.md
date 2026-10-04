# Étude de marché Shōgen — P7 Stratégie produit et standardisation (2026-10-04)

> *Note de versement de l'orchestrateur* : citations de pages web non versées à `biblio/` passées de « … » à “…” (gate S-G5) ; lectures [lu] web du rapport, copies hors dépôt.

- **Gate 0** : modèle résolu `claude-fable-5-1` (Fable 5.1). Écart de roster déclaré : CLAUDE.md §7 prévoit `claude-sonnet-5-5` (effort high) ou `claude-opus-5-5` pour les chercheurs ; je ne suis ni l'un ni l'autre. Signalé en tête de réponse à l'orchestrateur ; ce rapport est à relire sous ce jour.
- **Brief** : `BRIEF-P7-STRATEGIE.md`, sha256 `ef0e6892…d868` vérifié.
- **Attestation d'exposition** : aucune pièce de `docs/15-*`, `docs/16-*`, matière Pocket, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, aucun `*.jsonl`. Pièces lues : docs 02, 04, 07 ; 11 §1 et §4 ; 10 §3 ; `adr-0028/AVIS-PRODUIT-APRES-S2.md` ; `adr-0029/ADR-0029-campagne-S2-bis.md` §1, §2.5, §2.6, §3. Aucune écriture dans le dépôt, aucune opération git, aucune clé, aucun compte, aucun achat.
- **Niveaux** : [lu] lu sur la source le 2026-10-04 (URL et extraits dans `web/SOURCES.md`) ; [2nd] seconde main ; [repo] pièce du dépôt ; [inféré] raisonnement du rédacteur. Le compte Firecrawl a signalé des crédits bas ; les lectures ont été limitées aux pages décisives (5 pages entières, 31 recherches).

## 1. Résumé (10 lignes)

1. Toutes les mesures devenues standards de fait (L2BEAT, DefiLlama, OpenSSF Scorecard, clientdiversity, Coin Metrics, CF Benchmarks) partagent cinq traits : gratuité de la mesure, méthodologie publiée et versionnée, recalculabilité par un tiers, gouvernance explicite des conflits, financement déclaré. Shōgen en possède déjà trois par construction (ADR-0003, doc 04 §4) ; il lui manque le document de méthodologie public et la déclaration de financement.
2. Le marché « risque » converge vers les oracles : RedStone a acheté Credora (sept. 2025), LlamaRisk opère sur Chainlink CRE, Chaos Labs vend son propre oracle Edge, Gauntlet est devenu curateur de vaults. Les mesureurs deviennent des parties mesurées : la place de **tiers non conflité** se vide, c'est celle de Shōgen.
3. Les amonts sont structurellement communs : Chainlink lit « exclusivement » des agrégateurs premium (CoinGecko cité), Pyth publie Coinbase/OKX, Hyperliquid prend la médiane pondérée de 7 CEX (Binance poids 3). Personne ne publie le graphe d'amonts d'un feed ; S2 a montré qu'il est mesurable (k_eff = 4/10, 7 hôtes derrière Cloudflare) [repo].
4. Les incidents de 2025 vendent la mesure : Cloudflare 18 nov. (Coinbase, Kraken, Etherscan, Aave, DefiLlama hors ligne), AWS us-east-1 20 oct. (Coinbase « market data impacted »), krach du 10 oct. (USDe à 0,65 $ sur Binance, Bybit et MEXC contaminés parce qu'ils lisaient le prix Binance).
5. Le vocabulaire réglementaire existe : DORA art. 29 parle de « closely connected ICT third-party service providers » et de chaînes de sous-traitance ; IOSCO DeFi rec. 5 de « concentration of critical service providers » ; EEA de « too few data sources ». Un k_eff daté est une pièce pour ces registres.
6. Actifs : ajouter ETH/USD d'abord (mêmes endpoints, 58,7 % du collatéral Aave est ETH-lié), puis USDC et USDT ensemble comme **classe de peg** (306,8 Md$ d'encours ; USDT 60 %). L'apport décisif : USDT est un amont caché du prix « BTC/USD » lui-même (paires BTCUSDT), ce que la mesure rendra visible.
7. Offre : (i) benchmark public gratuit « Root Count » par feed/pool ; (ii) rapport de concentration sur pool nommé, payant ; (iii) abonnement monitoring/alertes ; (iv) dossier DORA/registre pour CASP ; (v) le certificat R1 seulement après S2-bis.
8. Prix de référence du marché : données 150–500 $/mois (Data Streams, DefiLlama Pro, Token Terminal, Messari, Pyth Starter) ; risque institutionnel 3–8 M$/an (Chaos Labs/Aave). Shōgen se place entre les deux, sans jamais vendre la mesure elle-même.
9. Premiers clients : les oracles challengers (Chronicle 5,1 Md$ TVS ; RedStone 4,3 Md$, ambivalent), Aave V4 orphelin de Chaos Labs (avril 2026), les CASP MiCA soumis à DORA. Canal : préavis privé puis publication nominative.
10. Risques dominants : conflit « émetteur-payeur » (leçon des agences de notation), capture par un oracle partenaire (leçon Credora), mesure de l'observateur (leçon S2), redistribution des données (CGU CoinGecko/Pyth).

## 2. Constats sourcés

### 2.1 Comment une mesure devient un standard de fait

| Mesure | Gratuite | Méthodologie publiée | Recalculable | Gouvernance / conflits | Financement | Adoption tierce |
|---|---|---|---|---|---|---|
| L2BEAT (rollups) | oui | oui, exigences de « Stage » débattues sur forum public [lu] | partiellement (code ouvert) | « public goods company », partenaires et donateurs listés par palier [lu] | Partnership Fund et EF > 500 k$, Optimism RPGF, Celestia, Starknet… [lu] | cité par tout l'écosystème ; conflit visible : ses partenaires (Superchain, Agglayer, EigenLayer) sont aussi notés [inféré] |
| DefiLlama (TVL) | oui, « open API … free » [lu] | adaptateurs open source ; choix du double comptage assumé publiquement dès 2021 [lu] | oui | équipe réduite, pas de comité | kickbacks LlamaSwap + abonnements ; Pro API 300 $/mois [lu][2nd] | « most TVL numbers cited elsewhere are DeFiLlama » [2nd] |
| Coin Metrics Reference Rates | non (payant) | oui : sélection des marchés par règles, fenêtre 61 min, changelog [lu] | oui sur données payantes | administrateur, comité, politique conflits, réclamations [lu] | commercial | « on-chain oracles republish them » [lu] |
| CF Benchmarks BRR | non | oui, critères de places constituantes | oui | FCA (FRN 847100), audit ISAE 3000 KPMG, minutes du comité publiées [lu] | licences CME | règlement des futures CME, ETF |
| clientdiversity.org | oui | oui, trois sources affichées | non (estimations) | aucune ; trois estimations incompatibles affichées en sept. 2026 (Teku 99,8 % / 53,9 %, Lighthouse 51,3 %) [lu] | bénévole | institution de l'écosystème malgré la divergence |
| OpenSSF Scorecard | oui | oui, checks 0-10 ouverts [lu] | oui | fondation Linux, WG | fondation (Google, GitHub, Microsoft, JPMorgan) [2nd] | « billions of evaluations monthly » [2nd] |
| Chainlink PoR | pour le lecteur | principes publiés par le vendeur | non (réseau Chainlink) | émetteur-payeur (Backed, 21.co, Bedrock…) [lu] | commercial | produit, pas standard tiers [inféré] |
| Agences de notation | non | méthodologie publiée (obligation) | non | émetteur-payeur depuis les années 1970 : « fundamental conflict of interest » (SEC) ; 90-95 % des revenus viennent des émetteurs [lu][2nd] | émetteurs | standard par licence réglementaire |

Lecture P7 : le palier d'entrée (L2BEAT, DefiLlama, Scorecard) est **gratuit, ouvert, financé par des tiers déclarés** ; le palier institutionnel (Coin Metrics, CF Benchmarks) ajoute **administrateur nommé, comité, politique de conflits, procédure de réclamation, changelog**, c'est-à-dire les Principes IOSCO pour les benchmarks (méthodologie “with sufficient detail to allow Stakeholders to understand how the Benchmark is derived”, conflits d'intérêts, transition) [lu]. Shōgen n'est pas un benchmark de prix et n'a pas à s'enregistrer sous BMR ; mais la **forme** IOSCO est le chemin le moins cher vers la crédibilité institutionnelle : un document de méthodologie numéroté, un changelog, un comité (même de trois personnes), une page de financement. Le cas clientdiversity montre le risque inverse : une mesure citée partout mais non gouvernée finit par afficher des chiffres contradictoires.

### 2.2 Le marché visé : fournisseurs de risque et oracles fusionnent

- **RedStone + Credora** (sept. 2025) : “the first oracle that delivers real-time prices and risk ratings” ; Credora « widely used in Morpho » ; argument commercial « rated vaults grow faster » [lu]. Le noteur appartient désormais à un oracle noté.
- **LlamaRisk** : LlamaGuard tourne dans « three independent Chainlink Runtime Environment (CRE) » et Chainlink annonce que CRE « enable LlamaGuard to initiate automated management actions » [lu]. Le gestionnaire de risque d'Aave est hébergé par l'oracle d'Aave.
- **Chaos Labs** : Oracle Risk Portal public (mai 2024) qui compare les fournisseurs à un « benchmark oracle » (déviation, latence par cross-corrélation, Granger) mais **ne mesure aucun amont ni infrastructure commune** [lu] ; vend l'oracle Edge ; a quitté Aave le 6 avril 2026 : budget 3 M$ en 2025, offre de 5 M$ refusée, besoin déclaré 8 M$, « last remaining technical contributor » après BGD Labs et ACI [lu].
- **Gauntlet** : « industry's largest vault curator » sur Morpho [lu] : le mesureur alloue le capital qu'il mesure.
- **Oracles** (TVS DefiLlama, lu 2026-10-04) : Chainlink 38,3 Md$ / 534 protocoles ; Chronicle 5,1 Md$ ; RedStone 4,3 Md$ ; Pyth 3,7 Md$ ; Atlas 1,8 Md$ [lu]. Amonts déclarés : Chainlink « exclusively pull data from premium data aggregators » (BraveNewCoin, CoinGecko cités), médiane de nœuds avec seuil (ex. 14/21) [lu] ; Pyth : plus de 120 éditeurs dont Coinbase et OKX [lu] ; Hyperliquid : médiane pondérée Binance 3, OKX 2, Bybit 2, Kraken/Kucoin/Gate/MEXC 1 [lu]. Trois couches (places → agrégateurs → oracles) où les mêmes places reviennent partout : l'indépendance affichée entre un oracle, un agrégateur et une place est largement nominale [inféré, cohérent avec S2 : coingecko × defillama ρ_resid = 0,78, doc 11 §4 [repo]].

Conséquence : le seul acteur qui puisse publier « combien de racines derrière N sources » sans être lui-même une racine est un tiers qui ne vend ni prix, ni notation, ni paramètres de risque. C'est la position que doc 07 §2 appelait « l'anti-cible » ; elle est devenue le marché entier [inféré].

### 2.3 Les incidents de mode commun de 2025 : le cas client est écrit

- **Cloudflare, 18 nov. 2025** : « worst outage since 2019 » (post-mortem Cloudflare) ; Coinbase, Kraken, Etherscan, Aave et DefiLlama touchés (The Block) ; récidive le 5 déc. 2025 [lu]. S2 avait mesuré le 28 sept. 2025 que 7 des 10 hôtes du pool BTC/USD étaient derrière AS13335 [repo] : la mesure précède l'incident de sept semaines.
- **AWS us-east-1, 20 oct. 2025** : Coinbase « market data … impacted » (rétrospective Coinbase) [lu] ; Binance et Gemini sont sur AWS dans la partition S2 [repo].
- **10 oct. 2025** : 19 Md$ liquidés ; USDe à ~0,62-0,65 $ sur Binance seulement ; LlamaRisk : l'oracle de marge de Binance pondérait son propre carnet ; « contagion also affected other venues like Bybit and MEXC, which utilized Binance's spot price in their own internal oracles » ; Aave (USDe prix = USDT, CAPO) n'a pas liquidé [lu]. C'est, mot pour mot, un amont commun non déclaré entre trois « sources » indépendantes en apparence.
- **USDC, 11 mars 2023** : 3,3 Md$ chez SVB, creux 0,86 $ (Fed) ; liquidations sur Aave/Compound [lu].

### 2.4 Cadre réglementaire : le vocabulaire existe, la mesure manque

- **DORA art. 28-29** : registre d'information de tous les tiers ICT ; art. 29 : substituabilité, “multiple contractual arrangements … with the same ICT third-party service provider or with closely connected ICT third-party service providers”, chaînes de sous-traitance [lu]. Les CASP MiCA sont des entités financières DORA (art. 2(1)(s)) ; RPC et oracles comptent comme tiers ICT selon les commentateurs [2nd].
- **IOSCO DeFi (déc. 2023), rec. 5** : « concentration of critical service providers », « reliance on oracles » [lu]. **EEA DeFi Risk Guidelines v1** : “"Single" Point of Failure : oracles that rely on too few or insecure data sources”, mitigation « Multiple Oracles, or Multiple Data Sources » [lu]. Aucun des deux ne dit comment compter les sources : c'est le trou que k_eff remplit [inféré].
- **BCBS SCO60** (en vigueur 2026-01-01) : redemption risk test et « operational risk and resilience framework » pour les stablecoins [lu]. **GENIUS Act** (PL 119-27, 18 juil. 2025) : réserves 1:1, publication mensuelle, examen par cabinet d'audit [lu]. **MiCA** : USDC/EURC autorisés (24 émetteurs EMT au 11 sept. 2026) ; USDT non autorisé, délisté pour l'EEE début 2025 [2nd]. **ISO 24165 DTI** : identifiant de jeton recommandé par la DTIF dans les formulaires GENIUS [lu].

### 2.5 Prix de référence observés

Données : Chainlink Data Streams « starting at $150/month » [lu] ; DefiLlama Pro 300 $/mois [2nd] ; Token Terminal Pro 350 $/mois [lu] ; Messari Pro 500 $/mois [2nd] ; Pyth Starter 500 $/mois, « No redistribution rights » [repo]. Risque institutionnel : Chaos Labs 3 M$ (2025), 5 M$ offerts, 8 M$ réclamés [lu] ; doc 07 : Gauntlet 1,6–2,3 M$/an [repo]. Mesure publique : L2BEAT vit de paliers > 500 k$ (EF, Partnership Fund, RPGF) [lu].

### 2.6 Actifs

Encours stablecoins 306,8 Md$ ; USDT 184,0 Md$ (60 %) ; USDC 74,2 Md$ ; Ethereum 146 Md$, Tron 94,8 Md$ dont 97,8 % USDT [lu]. Aave (mai 2026) : 10,7 Md$ de dette / 17,4 Md$ de collatéral ; collatéral ETH-lié 58,7 % (WETH 25 %, weETH 21 %, wstETH 14 %), WBTC 13 % ; emprunts WETH 51 %, USDT 21 %, USDC 18 % [lu]. Aave ne lit pas USDC/USDT au marché : « FixCapAdapter (stablecoins) … fixed 1:1 peg » [lu] ; le feed Chainlink USDC/USD a un seuil de déviation de 0,25 % [lu]. Aave a aligné le prix d'USDe sur USDT au motif que “approximately 76% of total market open interest for ETH and BTC is denominated in USDT” [lu]. Paires fiat : Kraken cote USDT/USD ; Binance ne cote qu'USDC/USDT [lu].

## 3. Recommandations

### R1 — Le produit d'ouverture : « Root Count », benchmark public et gratuit, sous forme IOSCO-lite

- **Quoi** : une page par feed ou pool nommé, portant ce que S2 sait déjà écrire sans vocabulaire interdit (avis produit §3 [repo]) : k nominal, k_eff côté livraison, partition nommée et datée (ASN, CDN, hôte), amonts déclarés `basis:doc`, corroborations de contenu, **liste exhaustive des axes non mesurés**, lien vers les journaux et le recalcul. Ni note, ni verdict R1 avant S2-bis.
- **Pourquoi** : c'est le palier d'entrée commun à L2BEAT, DefiLlama et Scorecard (§2.1) ; c'est l'« angle vide n°2 » (doc 06 [repo]) que ni le portail Chaos Labs ni les comparatifs d'oracles ne couvrent ; c'est ce que DORA art. 29 et EEA §3.1.5 demandent sans savoir compter.
- **Comment** : (a) `METHODOLOGIE-v1.0.md` public : définitions (hôte, ASN, livraison vs origine, amont déclaré vs mesuré), règles de partition, fenêtre de datation, procédure de réclamation, changelog ; (b) comité de méthodologie de 3 personnes dont une externe, minutes publiées (forme CF Benchmarks, coût nul) ; (c) page « Financement » par paliers (forme L2BEAT) ; (d) sorties lisibles par machine (JSON signé, identifiants ISO 24165 DTI pour les actifs, `llms.txt`), pour les agents IA que l'investisseur cible ; (e) préavis privé de 14 jours aux entités nommées avant publication (doc 07 §6 [repo]).
- **Apport** : antériorité datée (le J28 précède la panne Cloudflare), demande entrante mesurable (critère D9 (ii) [repo]), vocabulaire commun avec les registres DORA.
- **Coût** : rédaction et revue ; VPS déjà budgétés dans ADR-0029 (165–605 € la campagne) [repo] ; aucun code neuf au-delà du rendu existant.
- **Risques** : chiffres contestés par les nommés (parade : tout est recalculable, dates et résolveur imprimés) ; dérive « notation » à refuser dans le vocabulaire (doc 09).

### R2 — Actifs : ETH d'abord, puis USDC et USDT ensemble comme classe de peg

- **Ordre** : (1) **ETH/USD** : mêmes 10 hôtes, mêmes endpoints avec un autre symbole, feed Chainlink ETH/USD le plus consommé, 58,7 % du collatéral Aave ETH-lié ; coût marginal minimal, double la surface du benchmark sans nouvel observateur [inféré]. (2) **USDC/USD et USDT/USD** dans la même passe : encours 258 Md$ cumulés, 40 % des emprunts Aave, réglementation dédiée (MiCA, GENIUS, SCO60) qui crée des lecteurs institutionnels.
- **Pourquoi ensemble** : la classe de fait n'est pas la même que pour BTC. Un stablecoin a un **peg** (1 $) et un **prix secondaire** ; les protocoles choisissent l'un ou l'autre (Aave : cap fixe ; Chainlink : marché, seuil 0,25 %). Le hors-enveloppe doit être défini par rapport au peg **et** à la médiane leave-one-out, et le stress calendaire doit viser les fenêtres de dépeg (10 oct. 2025, 11 mars 2023 sont les cas d'école). Décision de conception à prendre par P4/P6 ; je recommande deux sous-classes : « prix secondaire » (places fiat : Kraken, Coinbase, Bitstamp, Gemini) et « prix implicite » (places USDT-quotées).
- **L'apport caché** : la plupart des « BTC/USD » du pool S2 sont des BTC/USDT (Binance, OKX ticker [repo]) ; mesurer USDT/USD révèle qu'**USDT est un amont du prix BTC** lui-même, et que la partition du pool BTC doit porter une arête `basis:doc` « quote = USDT » vers Tether. C'est la phrase qu'un comité de risque institutionnel n'a jamais lue et que personne ne publie [inféré].
- **Comment** : un lot de conception (classes de fait, τ/σ par classe, calendrier stress) **avant** le sceau S2-bis, sinon la règle n'est plus pré-enregistrée ; pas de Pyth sans lecture sans clé (ADR-0029 §2.5 [repo]).
- **Coût** : environ ×4 sur le volume de journaux (≈ 40 Go/mois/observateur contre 10 estimés [repo, calc]), sous les quotas lus ; rate limits à re-lire par symbole (doc 10 §3.3 [repo]).
- **Risque** : élargir avant d'avoir un R1 décisif disperse S2-bis ; parade : les quatre actifs partagent les observateurs, mais la règle de décision reste **par classe**.

### R3 — Élargir les trois types de sources par le critère « sans clé, redistribuable, documenté »

- **Oracles** : Chainlink (ETH/USD, USDC/USD, USDT/USD par RPC ; ajouter un **second RPC d'une autre famille** pour sortir le chemin de lecture de la partition, caveat « chemin de lecture ≠ amont » [repo]) ; **Chronicle** (5,1 Md$ TVS, lisible on-chain) ; **RedStone** (4,3 Md$ ; pull, passerelle HTTP publique à vérifier) ; Pyth seulement par voie B′ ; API3 à évaluer. Apport : la comparaison oracle-à-oracle sur amonts nommés est exactement ce que le portail Chaos Labs ne fait pas.
- **Agrégateurs** : garder CoinGecko et DefiLlama (amont commun déjà corroboré), ajouter CoinPaprika et CoinMarketCap **si** sans clé et redistribuables (CGU à lire) ; écarter Kaiko, Coin Metrics, CryptoCompare (payants ou à clé) mais les **citer** comme amonts déclarés des oracles.
- **Places** : aligner le pool sur les constituants réels des oracles : Bybit, Gate, KuCoin, MEXC (Hyperliquid), Bullish (CF Benchmarks) ; pour les stablecoins, les **pools on-chain** (Curve, Uniswap) lus par RPC, en notant qu'ils partagent le chemin de lecture avec Chainlink.
- **Apport** : un pool qui contient les constituants d'Hyperliquid, de CF Benchmarks et de Chainlink permet de calculer le k_eff **de chaque oracle tel qu'il se compose**, pas seulement du pool Shōgen.
- **Coût** : un adaptateur et une fiche par source (doc 10 §3 [repo]) ; vérification CGU par source (R-8). **Risque** : CGU « not suitable for scheduled polling » (CoinGecko, [repo]) et « No redistribution rights » (Pyth) : une source non redistribuable casse la recalculabilité et doit rester dehors.

### R4 — Offre et prix

| Produit | Qui paie | Prix indicatif [inféré, comparables §2.5] | Préalable |
|---|---|---|---|
| Benchmark public « Root Count » (pages, JSON, recalcul) | personne ; paliers de financement déclarés (fondations, RPGF, partenaires **non mesurés**) | 0 | docs/11 publié |
| Rapport de concentration sur pool nommé (one-shot, recalculable, livré avec journaux) | protocole, oracle challenger, CASP | 10–30 k€ par rapport [inféré : entre un abonnement data et 1 % d'un budget risque Aave] | méthodologie v1.0 |
| Monitoring et alertes (k_eff, nouvel amont commun, dégradation), API | protocole, desk, agent IA | 500–2 000 $/mois par feed [inféré : Data Streams 150 $, Pyth 500 $, Messari 500 $] | observateurs multiples (S2-bis) |
| « Evidence pack » DORA art. 28-29 (annexe au registre : fournisseurs ICT derrière les feeds, dates, ASN) | CASP MiCA, émetteurs EMT | forfait annuel 20–50 k€ [inféré] | texte DORA/MiCA détenu dans biblio (dette avis produit §3 [repo]) |
| Certificat de diversité R1+R2 | oracle challenger, protocole | à fixer après S2-bis | S2-bis décisive |

Règle d'or : **jamais de paiement de la partie mesurée pour être mesurée** ; un oracle peut acheter un rapport sur son **propre** pool si la méthodologie, les journaux et le résultat sont publiés et si le paiement est déclaré sur la page Financement (parade au conflit émetteur-payeur, §2.1). **Canal** : (1) Chronicle et RedStone (ce dernier est aussi concurrent via Credora : partenariat de données, pas d'exclusivité) ; (2) Aave V4, orphelin de Chaos Labs depuis avril 2026 et réduit à LlamaRisk ; (3) les CASP MiCA et émetteurs EMT (Circle est listée MiCA ; Tether non : deux dossiers différents) ; (4) pour les agents IA : MCP/JSON signé plutôt qu'un tableau de bord (RedStone publie déjà un serveur MCP [lu]).

### R5 — Chemin de standardisation (18 mois)

1. **0–3 mois** : publication docs/11 + méthodologie v1.0 + page Financement + préavis privé ; soumission du métrique aux groupes EEA DeFi Risk (le guide v1 cite « too few data sources » sans définir le compte) ; identifiants DTI.
2. **3–9 mois** : S2-bis multi-observateurs (ADR-0029) étendue aux 4 actifs ; deux recalculs externes nommés (critère D9 (ii)) ; premier rapport payant.
3. **9–18 mois** : si R1 tranche, certificat ; statement de conformité « IOSCO-like » (gouvernance, conflits, méthodologie, transition) ; candidature au registre de fournisseurs cités dans les registres DORA des premiers CASP clients. Ne pas viser BMR : Shōgen ne produit pas un prix de référence.

### R6 — Risques

- **Conflit d'intérêts** : la leçon des CRA (90-95 % de revenus émetteurs) et de L2BEAT (partenaires notés) : publier les paliers, refuser l'exclusivité, séparer comité de méthodologie et ventes.
- **Dépendance à un oracle partenaire** : Credora a disparu dans RedStone en 13 mois ; LlamaRisk tourne dans CRE. Clause : aucune infrastructure d'un oracle mesuré dans la chaîne de mesure ; vantage et RPC hors des réseaux d'oracles.
- **Mesure de l'observateur** : S2 a mesuré son propre hôte (avis produit §1 [repo]) ; sans ≥ 3 observateurs, aucun produit payant au-delà du R2.
- **Juridique et narratif** : nommer Cloudflare, Tether ou Binance dans une partition appelle des contestations ; n'écrire que des faits datés, resolveur et méthode imprimés, et le mot « livraison », jamais « origine ».
- **Données** : CGU et clés (CoinGecko, Pyth, CryptoCompare) ; une source retirée après sceau est une trouvaille, pas un re-tune (ADR-0022 [repo]).

## 4. Ce qui reste incertain

- Les prix indicatifs du §R4 sont des inférences par comparables ; aucun devis, aucun acheteur interrogé.
- La lisibilité sans clé et la redistribuabilité de RedStone, Chronicle, CoinPaprika, CoinMarketCap, Bybit, Gate, KuCoin, MEXC n'ont pas été vérifiées sur pièce (travail P4/P5).
- L'attribution « RPC et oracles = tiers ICT DORA » est un commentaire de cabinet [2nd], pas un texte d'autorité ; aucun texte DORA/MiCA n'est détenu dans biblio/ (dette déjà notée [repo]).
- Le chiffre Chainlink « agrégateurs premium » date de 2020 ; la liste actuelle des fournisseurs de données par feed n'est pas publiée [inféré].
- Le marché des « agents IA » comme acheteurs n'a pas été étudié ici (profil P2).
- Le volume ×4 des journaux est un calcul d'ordre de grandeur, non une mesure.

## 5. Trois questions à l'investisseur

1. Acceptez-vous un financement par paliers déclarés (fondations, RPGF, partenaires) **y compris** de la part d'acteurs que Shōgen nommera dans ses partitions, à condition de publication, comme L2BEAT, ou voulez-vous une règle d'exclusion stricte qui retarde le revenu ?
2. Pour USDC/USDT, la classe de fait est-elle le **prix secondaire** (ce que Chainlink publie) ou l'**écart au peg** (ce qu'Aave suppose) ? Le choix fixe τ, le calendrier stress et le message au régulateur, et il doit être scellé avant S2-bis.
3. Quel est le premier acheteur que vous voulez pouvoir citer dans 12 mois : un oracle challenger (vitesse, risque de capture), un protocole (Aave V4, budget mais gouvernance instable), ou un CASP sous DORA (lent, mais c'est la position institutionnelle demandée) ? La réponse ordonne le lot d'après S2-bis.
