# Croisement des neuf études — étude de marché Shōgen (2026-10-04)

- **Gate 0** : modèle résolu `claude-opus-5-5` (analyste de synthèse), conforme au préfixe attendu.
- **Brief** : `etude-marche/BRIEF-SYNTHESE.md`, sha256 `3676e074…2085`, vérifié.
- **Date** (`date -u`) : 2026-10-04, début 05:36 UTC.
- **Exposition** : lus en entier : les huit rapports P1 à P8 et les huit briefs de profils ; `docs/adr-0029/ETUDE-POOL-BIS.md` ; ADR-0029 §1 à §6 ; doc 11 §1, §2.1-§2.3 et §4. Aucune pièce interdite ouverte, aucun `*.jsonl` (en particulier pas `P6-MESURE/calc/sim_pool_out.jsonl`). Aucune écriture hors de ce fichier, aucune opération git, aucune recherche web.
- **Registre** : chaque fait garde le niveau que lui donne son rapport ([lu], [lu-extrait], [2nd], [calc], [inféré], [dépôt]/[repo]). **[synthèse]** marque un rapprochement ou un calcul de ma part : il n'ajoute aucun fait nouveau.
- **Abréviations** : P1 DeFi prêt ; P2 agents IA ; P3 institutionnel ; P4 analyste oracles ; P5 stablecoins ; P6 mesure ; P7 stratégie ; P8 actions tokenisées ; **EP** = `docs/adr-0029/ETUDE-POOL-BIS.md` ; **ADR** = ADR-0029 révision 2 ; **D11** = `docs/11-mesures-pilotes.md`. Un renvoi « P4 §4 » désigne `etude-marche/P4-ANALYSTE-ORACLES/RAPPORT.md`, section 4.

## 0. Réserves de provenance (avant de pondérer les avis)

| pièce | modèle déclaré (Gate 0 de la pièce) | réserves que la pièce déclare elle-même |
|---|---|---|
| P1 | `claude-fable-5-1`, **hors roster** (écart déclaré) | crédits Firecrawl bas : la plupart des faits viennent d'extraits indexés ([lu-extrait]) |
| P2 | `claude-sonnet-5-5` | [lu] = résumé automatique de page, pas une lecture intégrale |
| P3 | `claude-fable-5-1`, **hors roster** (écart déclaré) | crédits bas ; eur-lex lu par extraits ou par miroirs |
| P4 | `claude-sonnet-5-5` | un seul point de vue réseau ; un appel `eth_call` vers Alchemy avec le jeton public « demo », déclaré et non utilisé ; page DefiLlama `/oracles` obtenue par le lecteur Firecrawl après un 403 de `curl` |
| P5 | `claude-opus-5-5` | rejeu sur bougies, pas sur témoignages |
| P6 | `claude-opus-5-5` | **simulation de taille de pool non versée** : le §3.4 porte encore les marqueurs `TABLE_SIM` et `RESULTATS_SIM` (relu à 05:38 et à la clôture, voir §6) ; lecture RPC refusée |
| P7 | `claude-fable-5-1`, **hors roster** (écart déclaré) | crédits bas : 5 pages entières, 31 recherches |
| P8 | `claude-opus-5-5` | sondes faites un dimanche, marché fermé : une seule prise |
| EP | `claude-sonnet-5-5` (lecteur) | un seul point de vue ; adresses de contrats non tirées de pages primaires, vérifiées par les réponses des contrats |

**Conséquence [synthèse]** : P1, P3 et P7 portent l'essentiel des positions sur le produit, les acheteurs, le prix et la gouvernance. Ils ont tourné hors roster. L'orchestrateur décide du poids à leur donner. Deux erreurs factuelles relevées plus bas (§2, C1 et C2) viennent de ces trois rapports.

---

## 1. Matrice par sujet

### 1.1 Actifs à ajouter

**Positions.**

| profil | position | renvoi |
|---|---|---|
| P1 | ETH/USD, USDC/USD et USDT/USD. **Aucun dérivé ETH comme classe multi-sources** : les taux wstETH et weETH sont un observable R2 à journaliser. ETH/USD est le facteur commun d'environ 60 % des garanties Aave | P1 §3 R-1, §2.1 |
| P2 | ETH/USD, USDC/USD, USDT/USD. Commencer par ETH et USDC complets, **USDT ensuite** (dilution de la puissance R1). Écarter la longue traîne | P2 §3 R1 (risque iii), §2.5 |
| P3 | ETH/USD sur un pool aligné CME CF. USDC et USDT en classes « peg ». Actifs tokenisés (NAV) en 2027 | P3 §3 R1, R2, R7 |
| P4 | Les quatre actifs, en classes séparées par actif **et par nature** (places, agrégateurs, oracles à heartbeat) | P4 §4 |
| P5 | **Six classes jamais fusionnées** : USDC/USD, USDT/USD, USDC/USDT, ETH/USD, LST/ETH « marché », taux de rachat LST (k nominal = 1 déclaré) | P5 §3 A, F |
| P6 | Quatre classes R1 (BTC, ETH, USDC, USDT) ; une classe = un actif ; paires stable/stable hors des classes USD | P6 §3.1, §2 C3 |
| P7 | **ETH d'abord**, puis **USDC et USDT ensemble** comme classe de peg | P7 §3 R2 |
| P8 | Actions tokenisées hors S2-bis (voir §1.7) | P8 §4 R1 |

**Accords.**
- Les trois actifs ajoutés par l'investisseur sont soutenus par tous les profils.
- ETH/USD a le coût marginal le plus faible : mêmes hôtes, mêmes points d'accès, autre symbole (P2, P5 C, P6, P7).
- Les stablecoins ne se traitent pas comme BTC (P1, P3, P5, P6, P7).

**Désaccords.**
- **USDT : avec USDC ou après ?** P2 le place après ETH et USDC (puissance). P7 veut USDC et USDT ensemble (même nature de peg ; USDT est un amont caché du prix BTC).
- **LST et LRT.** P5 en fait deux classes (prix de marché ; taux de rachat). P1 refuse toute classe multi-sources pour eux (taux déterministe) et n'en fait qu'un observable R2. P6 ne les mentionne pas.
- **Paire USDC/USDT.** P5 en fait une classe à part entière. P6 l'exclut des classes USD (ce n'est pas une cotation USD). P3 et P1 l'utilisent comme source « croisée » dans la classe peg.

**Faits chiffrés qui comptent.**
- Aave Ethereum V3 [lu-extrait, aavescan, P1 §2.1] : WETH 5,72 Md$ ; weETH 4,13 ; WBTC 2,90 ; USDT 2,85 ; wstETH 2,69 ; USDC 2,43 ; cbBTC 1,48 ; rsETH 0,97.
- Garanties Aave liées à ETH : 58,7 % (WETH 25 %, weETH 21 %, wstETH 14 %), WBTC 13 %, mai 2026 [lu, P7 §2.6]. Ce sont les mêmes parts que Galaxy, non datées chez P1 [lu-extrait, P1 §2.1].
- Encours stablecoins : 306,8 Md$ ; USDT 184,0 Md$ (60 %) ; USDC 74,2 Md$ [lu, P7 §2.6].
- Règlements x402 : 99,6 % en USDC [lu, TRM, P2 §2.4].
- Aave aligne USDe sur USDT, au motif que « approximately 76% » de l'intérêt ouvert ETH et BTC est libellé en USDT [lu, P7 §2.6].

**Incertain.**
- Aucune mesure publique des paires demandées par les agents (P2 §2.5).
- Les parts Galaxy ne sont pas datées dans l'extrait de P1.

### 1.2 Classes de fait et définitions d'écart

**Positions.**

| profil | position | renvoi |
|---|---|---|
| P1 | Sur les stables, R1 hors-enveloppe sera « presque toujours silencieux » ; la valeur vient de la panne, de la staleness et de R2. À écrire au pré-enregistrement | P1 §3 R-1 |
| P2 | τ et σ propres aux stables, scellés avant la campagne | P2 §3 R1 |
| P3 | Écarts nouveaux pour les stables : « divergence inter-places » (τ en points de base) et « CEX contre DEX ». Prix de rachat (1,00) comme référence R3 déclarée. Strates calme/stress committées | P3 §3 R2 |
| P4 | Une classe « oracle à heartbeat » avec son σ ; ne jamais mélanger les natures dans une même statistique | P4 §2.5, §4 |
| P5 | Deux notions séparées. « **Écart de source** » : leave-one-out de même classe et de même devise. « **Dépeg** » : état du marché, servant de variable de régime. Plus un statut « plafonné » (borne Chainlink à 1,05 $). Règle de régime pré-enregistrée sur un ensemble témoin disjoint (Curve, Uniswap) ; tension avec la règle des strates « jamais déduites des données » | P5 §2, §3 D |
| P6 | Leave-one-out inchangé ; **pas d'axe peg** ; P_j = \|médiane − 1\| comme variable d'état ; analyse conditionnelle exploratoire au-delà de 50 points de base ; « borné par conception » compté à part ; unités cotées en USDT gardées dans BTC et ETH sans conversion, avec une sensibilité « USD seules » | P6 §3.2 |
| P6 | σ des oracles poussés = 1,5 × heartbeat ; plancher de τ = 1,5 × seuil de déviation (0,75 % ETH, 0,375 % stables) ; lot **CALIB-ACTIFS** sur historiques publics à 1 minute (Coinbase, Binance, Kraken) | P6 §3.3 |
| P7 | Deux sous-classes : « **prix secondaire** » (places fiat) et « **prix implicite** » (places cotées en USDT). Hors-enveloppe défini par rapport au peg **et** à la médiane LOO ; strate de stress visant les fenêtres de dépeg | P7 §3 R2 |
| P8 | Pour les actions : définir l'**état** (fermé, pause d'opération sur titres, session mono-fournisseur) avant l'écart ; un prix nul compte comme panne | P8 §4 R2 |
| EP | Les sources nouvelles n'ont aucune donnée de S2, donc la règle TAU-SIGMA-S2BIS ne s'y applique pas : calibration séparée, ou valeurs de classe écrites d'avance | EP §6 (ii) |

**Accords.**
- Un dépeg est un état du marché, pas une défaillance de source (P5, P6 ; P1 implicitement).
- τ et σ se fixent par classe avant le sceau, sur des données disjointes de S2-bis (P2, P5, P6, EP ; ADR §2.6 pour BTC).
- Chainlink stable : la borne haute à 1,05 $ et le heartbeat d'environ 24 h exigent un traitement propre (P4, P5, P6).

**Désaccords.**
- **Le peg dans la définition d'écart.** P7 le met dans le hors-enveloppe, avec une strate de stress visant les dépegs. P5 et P6 le refusent : variable d'état. P6 ajoute que des strates ciblées sur les dépegs heurtent la règle « strates fixées ex ante ».
- **Écarts supplémentaires pour les stables.** P3 propose « CEX contre DEX » et « inter-places ». P6 n'en veut aucun : le leave-one-out et la staleness attrapent déjà la source figée.
- **Unités cotées en USDT dans ETH.** P6 les garde, sans conversion. P5 ne fusionne jamais les devises. P7 sépare prix secondaire et prix implicite.

**Faits chiffrés qui comptent.**
- Chainlink Ethereum [lu, annuaire, P5 §1.1, P6 C1] :
  - ETH/USD 0,5 % / 3 600 s ;
  - USDC/USD 0,25 % / 82 800 s ; USDT/USD 0,25 % / 86 400 s ;
  - borne « Bounded (upper) $1.05 » ;
  - au-delà de la borne, la dernière valeur écrite reste servie.
- Dispersion USDT/USD fiat entre 7 places : 0,9 point de base le 2026-10-04 [calc, P5 §1.1].
- Rejeu de mars 2023 [calc, P5 §1.3] :
  - dispersion médiane de 0,06 % en calme, 0,86 % en stress, maximum 7,6 % ;
  - avec τ = 0,45 % (le τ des places en S2) : K = 153 fenêtres sur 935 ;
  - consensus à plus de 1 % du pair dans 566 fenêtres.
- S2 [dépôt, ADR §1.2 pt 6] : τ observé (P99) 0,085 % contre τ = 0,45 % pour les places horodatées ; aucune fenêtre K faite d'écarts hors-enveloppe.

**Incertain.**
- Existence d'historiques à 1 minute pour assez de places stable/USD (P6 §4).
- Comportement des agrégateurs pendant un dépeg (P6 §4).
- Pas de prix (1e-5) proche de τ (P5 §4).

### 1.3 Sources à ajouter, par type

**Oracles.**

| source | pour | contre ou réserve | renvoi |
|---|---|---|---|
| Chainlink ETH, USDC, USDT par RPC | tous | heartbeats de 23-24 h sur les stables (P4, P6) | P1 R-1 ; P2 R1 ; P3 R1 ; P4 §4 ; P5 A ; P6 §3.3 ; P7 R3 |
| **Second chemin RPC d'un autre ASN** (une unité on-chain = un hôte RPC) | P1, P3, P4, P5, P7, EP | change l'unité par rapport à S2 : c'est une décision, pas un correctif (EP) | P1 R-3 ; P3 R2 ; P4 §4 ; P5 §3 ; P7 R3 ; EP §3 |
| Chainlink sur une **seconde chaîne** (Base) | P2 (battements différents) | EP : pas de racine neuve, « à éviter comme nouvelle unité » ; P6 : les variantes SVR forment une seule unité | P2 R1 ; EP §3 ; P6 C1 |
| **RedStone** | P1 (push on-chain) ; **P4 : premier ajout**, paquets signés vérifiables hors ligne, 10 s ; P5 (API publique, composition par devise) ; P7 (à vérifier) | **EP : passerelle à écarter** (la documentation exige une clé : lecture « hors contrat » ; 1,97 Mo par lecture). Contrat Ethereum « réservé » (adresse à confirmer). P4 note aussi que l'accès est « toléré, pas garanti » | P1 R-3 ; P4 §4 ; P5 §1.1 ; P7 R3 ; EP §2.3, §6.1 |
| **Chronicle** | P1 (troisième source de Spark) ; P7 (« lisible on-chain ») | **P4, P5, EP** : lecture protégée par liste blanche (module Toll), licence BUSL-1.1 (EP [lu]) | P1 R-3 ; P7 R3 ; P4 §2.5 ; P5 §3 ; EP §2.3 |
| Contrats Aggor de Spark | P1 | — | P1 R-3 |
| **DIA** | P4 (racine alternative, cotation signée) | EP : candidat sous réserve de licence et de limites (docs en 403) | P4 §4 ; EP §6.1 |
| Hyperliquid | P2 (lieu dérivé, parents déclarés) ; P4 : **`midPx` seulement** (`oraclePx` est une copie) ; EP : **`oraclePx`** comme « oracle natif de L1 », pas comme racine | désaccord sur le champ à lire | P2 R1 ; P4 §4 ; EP §6.1 |
| Pyth | personne en lecture directe (clé ; « No redistribution rights ») ; voie B′ seulement | EP : contrat Ethereum figé, valeur vieille de 73 jours | tous ; EP §2.3 |
| Band, API3, Supra, SEDA, APRO, Tellor, UMA, Switchboard, Stork | écartés (P4, EP) ; P7 propose d'« évaluer » API3 | — | P4 §4 ; EP §6.1 ; P7 R3 |

**Agrégateurs.**

| source | pour | contre | renvoi |
|---|---|---|---|
| CoinGecko, DefiLlama | à garder (tous) ; DefiLlama est étiqueté « copie déclarée de CoinGecko » (P4, EP) | CoinGecko sans clé « not suitable for scheduled polling » (lecture worker non re-établie, ADR §5) | P4 §4 ; EP §5 |
| **CoinMarketCap** | **P2** : second défaut des agents | **P4 et EP : clé exigée (401)**. P7 : seulement si sans clé et redistribuable. P2 déclare n'avoir pas lu l'accès sans clé | P2 R1, §4 ; P4 §2.2 ; EP §2.2 |
| **CoinPaprika** | **P4** (seul agrégateur général sans clé en plus) ; P1 et P7 (candidat, sous condition) | **EP : redistribution réservée à l'offre Enterprise** ; résolution de 10 min en offre libre ; « écarter » | P4 §4 ; EP §2.2, §3 |
| GeckoTerminal | P4 (méthode on-chain) | USDT lu à 1,00397 (P4) | P4 §4 |
| Coinlore, Kaiko, CoinAPI, CryptoCompare, Messari | écartés : précision, clé (P4, EP) | — | P4 §2.2 ; EP §2.2 |

**Places et DEX.**

| source | proposée par | réserve | renvoi |
|---|---|---|---|
| Crypto.com | EP (n° 1 : USD natif, horodatée), P3 (constituant CME CF), P4 (n° 5) | AS13335 ; licence non lue | EP §6.1 ; P3 R1 ; P4 §4 |
| Bitget, KuCoin, HTX | EP, P4 (KuCoin n° 3 ; Bitget et HTX en réserve), P7 (KuCoin) | KuCoin et Bitget sur AS13335 | EP §6.1 ; P4 §4 |
| **MEXC** | EP, P4 (n° 1), P7 | seul hôte Akamai ; sans horodatage | EP §3 ; P4 §4 |
| Gate | P4 (n° 2), P7 | sans horodatage | P4 §4 ; EP §3 |
| Bybit | P7, P1 | **bloqué (403, pays) depuis le conteneur** ; à essayer au smoke de chaque observateur | EP §2.1 ; P4 §2.5 |
| Bullish, LMAX | P3 (constituants CME CF) ; P7 (Bullish) | lisibilité sans clé non vérifiée (P3 §4) | P3 R1 |
| Uniswap v3 (pools ETH/USDC, WBTC/USDC, 0,01 % USDC/USDT) | P1, P2 (sur Base), P3, P4, P5, P7, EP | prix `slot0` manipulable ; témoin de contenu seulement (P4, EP) ; adresses à établir sur pièce | P4 §4 ; EP §2.4 |
| Curve (3pool, stETH) | P1, P3, P5, P7 | chemin de lecture partagé avec Chainlink si même RPC (P7, EP) | P5 §3 A |
| Binance | déjà au pool | 451 depuis le conteneur ; P4 propose de l'écarter du confirmatoire s'il est bloqué depuis un observateur UE | P4 §4 |

**Accords.**
- Chainlink étendu aux trois actifs, plus un second hôte RPC hors AS13335.
- Pyth et les agrégateurs à clé restent dehors (invariant « sans clé »).
- DefiLlama est une copie de CoinGecko.
- Un pool DEX lu par RPC apporte une racine d'un type nouveau (P1, P3, P4, P5, P7, EP).

**Désaccords les plus lourds.**
1. RedStone : passerelle (P4) ou rien tant que la documentation exige une clé (EP).
2. Chronicle : P1 et P7 contre P4, P5 et EP.
3. CoinPaprika : P4 contre EP (licence).
4. CoinMarketCap : P2 contre P4 et EP (clé).
5. Chainlink multi-chaînes : P2 contre EP et P6.
6. Hyperliquid : `midPx` (P4) ou `oraclePx` (EP).

**Faits chiffrés qui comptent.**
- TVS des oracles (DefiLlama, 2026-10-04) : Chainlink 38,3 Md$ (534 protocoles) ; Internal 8,2 ; Chronicle 5,1 ; RedStone 4,3 ; Pyth 3,7 [lu, P4 §2.1 ; mêmes chiffres chez P7 §2.2].
- Parmi les cinq premiers, seuls Chainlink (par RPC) et RedStone (passerelle) sont lisibles sans clé [P4 §1 pt 2 ; EP §5, avec réserves sur RedStone].
- Volume DEX : Uniswap V4 19,3 %, V3 8,1 % [lu, P4 §2.3].
- RedStone, passerelle : 1 972 925 octets par lecture, soit environ 2,8 Go par jour et par observateur [calc, EP §3 ; P4 §4].
- Composition RedStone [lu, P5 §1.1] : USDC 18 sources, dont 11 cotées en USDT ; ETH 14 sur 18 cotées en USDT ou USDC.

**Incertain.**
- Licences de redistribution des places, de DIA, de GeckoTerminal, de RedStone et d'Uniswap : non lues (P4 §5, EP §8).
- Composition actuelle des agrégateurs de Chainlink : non publiée (P4, P7, EP).
- L'accès sans clé à RedStone est toléré aujourd'hui (P4) et contredit par sa documentation (EP).

### 1.4 Taille du pool

**Positions.**

| profil | position | renvoi |
|---|---|---|
| EP | 15 unités gérables dans le calendrier ; 20 et 25 relèvent de la « voie B » (cartographie descriptive hors vote R1). L'axe ASN plafonne à 6-7 classes quel que soit N. Tout changement de composition change la cellule cible (« 7 hôtes AS13335 ») et impose de rejouer SIM-NIVEAU-BIS et SIM-PUISSANCE-BIS | EP §3, §6, §7 |
| P4 | Base + 9 ajouts (19 hôtes) : 5 ASN ; base + 6 ajouts hors Cloudflare (16 hôtes) : 6 ASN. Environ 60-80 lectures par minute et par observateur | P4 §4 [calc] |
| P6 | Passer de 10 à 15-25 unités **baisse** la puissance de K≥2 si les ajouts sont hors du mode commun, et l'augmente s'ils en font partie. Statistique de paires S = Σ C(m_j, 2) plus robuste à la taille, à fixer avant le sceau | P6 §1 pt 7, §3.4 (table non versée) |
| P2 | Trop de classes diluent la puissance de R1 | P2 R1 (iii) |
| P7, P1 | Élargir pour couvrir les constituants réels des oracles | P7 R3 ; P1 R-5 |

**Accords.**
- Élargir n'augmente presque pas k_eff sur l'axe ASN (P4, EP).
- Le gain porte sur les types de racines et sur l'axe contenu (P4, EP).
- Toute composition nouvelle se re-simule avant le sceau (EP, P6, ADR §2.4 e).

**Désaccords.**
- Pour la couverture : P7, P1 et, partiellement, P4.
- Pour un pool BTC resserré : P6 (question 3), EP (≤ 15, sinon voie B).

**Faits chiffrés qui comptent.**
- Paires : 10 → 45, 15 → 105, 20 → 190, 25 → 300 [calc, EP §7].
- Sur 28 hôtes mesurés : AS13335 16, AS16509 8, AS396982 2, AS20940 1, AS24940 1 [calc, EP §3].

**Incertain.**
- Aucune valeur de puissance pour N > 10 n'est versée (P6 §3.4 vide ; EP n'en donne pas).

### 1.5 Confirmatoire contre exploratoire

**Positions.**

| profil | position | renvoi |
|---|---|---|
| P6 | **F1** : BTC seul confirmatoire (Bonferroni 0,01 × 2 strates). **F2** : ETH en séquence fixe, testé à 0,01 dans la strate s seulement si BTC rejette dans s. **F3** : USDC et USDT exploratoires. Alternatives : B (quatre classes, Holm sur 8 hypothèses, seuil BTC à 0,0025 au premier pas, « casser la décision ») ; C (Westfall-Young, en sensibilité) ; A′ (USDT puis USDC en fin de séquence, déconseillé faute de calibration) | P6 §3.1 |
| P4 | Question : BTC confirmatoire (10 hôtes, déjà scellable) et le reste en **seconde vague exploratoire** ? Ou tout dans le paquet, au prix d'un retard ? | P4 §6 Q1 |
| P5 | BTC confirmatoire, ETH descriptif sauf calcul de puissance dédié | P5 §3 C, §5 Q1 |
| EP | Voie A (au plus 5 ajouts mesurés dans S2-bis) ou voie B (10 unités + cartographie hors vote) | EP §6 |
| P7 | « S2-bis étendue aux 4 actifs » ; les observateurs sont partagés, mais « la règle de décision reste **par classe** » | P7 R2, R5 |
| P8 | Actions hors confirmatoire ; relevé descriptif possible | P8 R1 |
| P1 | R1 annoncé « probablement silencieux » sur les stables | P1 §5 Q2 |

**Accords.**
- BTC reste le juge de « R1 discrimine » (P4, P5, P6, EP).
- Les stables seraient presque sûrement NON ÉVALUABLE en 16 semaines calmes (P5 §4, P6 §3.6, P1).

**Désaccords.**
- **ETH** : confirmation secondaire en séquence (P6) ou descriptif (P5) ?
- **Décision par classe pour les quatre actifs** (P7) contre la famille hiérarchique (P6). P7 ne chiffre pas la multiplicité.

**Faits chiffrés qui comptent.**
- Puissance à la cellule cible (scénario B, synthétique) [calc, dépôt, ADR §2.4 d-e] :
  - en calme : 0,91 à 16 semaines, 0,77 à 12 semaines ;
  - en stress : 0,54 à 16 semaines.
- n_calme = 109 440 ; n_stress = 43 776 ; T_max = 24 semaines.
- Seuil entier à R = 9 999 : C_s ≤ 99 pour α = 0,01 [dépôt, ADR §2.4 c]. P6 donne C_s ≤ 24 pour 0,0025 [P6 §3.1].

**Incertain.**
- Puissance d'ETH à sa cellule cible : non calculée (P6 §3.6 pt 7).
- Validité des rotations sur des séries non stationnaires (P6 C7, Harris, Kalyuzhny).

### 1.6 Axes R2 nouveaux

| axe | proposé par | forme proposée | renvoi |
|---|---|---|---|
| **Devise de cotation (USD, USDT, USDC)** | P1, P2, P4, P5, P6, P7 | P1 : partition par cotation à côté de la partition ASN. P2 : déclaratif R3 d'abord, puis observable. P5 : arête `measured` quand une valeur dérive d'une autre classe (×USDT/USD), arête `doc` pour les compositions publiées. P6 : sensibilité et co-occurrence, en descriptif. P7 : arête `basis:doc` « quote = USDT » vers Tether | P1 R-2 ; P2 R2 ; P4 §2.5 ; P5 B ; P6 §3.2 ; P7 R2 |
| **Appartenance déclarée aux amonts d'oracles** (graphe places → agrégateurs → oracles) | P1, P4, P7 | fichier d'arêtes daté par classe, au rang R3 pour l'appartenance exacte | P1 R-6 ; P4 §2.4 ; P7 §2.2 |
| Chaîne de valorisation (adaptateurs, CAPO, plafonds, paramètres hors chaîne) | P1, P5 | fiche par actif ; arête « racine unique : contrat X » | P1 §2.5, R-7 ; P5 F |
| Écart entre taux de rachat et prix de marché des LST | P5 | observable publié | P5 F |
| Rang de sous-traitance, LEI (sémantique DORA B_05.02) | P3 | export CSV depuis le bloc 6 ; LEI via GLEIF | P3 R3 |
| Lisibilité sans clé, datée | P4 | tableau public | P4 §4, §6 Q3 |
| Mono-fournisseur déclaré par session (actions) | P8 | état de session | P8 §3 |

**Accords.**
- La devise de cotation est l'axe le plus consensuel : six profils.
- Collecte nulle ou faible (P1 : « une colonne et une règle »).
- S2 portait déjà l'écart de peg USDT/USD dans ρ_resid [dépôt, D11 §4.2 (b)].

**Désaccords.**
- Statut de l'axe : déclaratif (P2, P7) ou mesuré (P5) ?
- P6 en fait une sensibilité descriptive, pas un axe.

**Faits chiffrés qui comptent.**
- Pool S2 : 9 flux USD, 2 USDT [dépôt, D11 §2.1].
- Chainlink USDC/USD suit en stress la place USDT convertie : écart moyen de 0,21 %, contre 0,55 % et 0,72 % pour les places fiat [calc, P5 §1.3, attribution [inféré]].
- USDT à 1,0163 sur Coinbase le 12/03/2023 [calc, P5 §1.3].

**Incertain.**
- La méthodologie de Chainlink pour USDC/USD (poids des paires USDT) n'est pas publiée (P5 §4).

### 1.7 Actions tokenisées

**Positions.**
- **P8** (seule étude dédiée) : hors du volet confirmatoire de S2-bis ; campagne **S3-actions** pré-enregistrée après le rendu de S2-bis ; relevé descriptif facultatif. Classes F1 à F4 : sous-jacent, jeton, écart normalisé par le multiplicateur, valeur publiée par l'émetteur. Pilotes : SPY, NVDA, TSLA (P8 §4 R1-R3).
- **P3** : la NAV tokenisée est à mesurer en 2027 (chemin de livraison seulement : k_eff de livraison, jamais k_eff d'amont) (P3 R7).
- Aucun autre profil ne traite le sujet.

**Accords** (P3, P8) : pas dans S2-bis ; un seul amont par construction pour la NAV ou le multiplicateur.

**Faits chiffrés qui comptent.**
- Encours distribué : 3,22 Md$ [lu, rwa.xyz] ; ESMA : environ 1,9 Md€ fin juin 2026 [lu].
- Émetteurs : Ondo 922,5 M$ ; bStocks 851,3 M$ ; xStocks 582,6 M$ ; Securitize 432,4 M$ ; Robinhood 142,6 M$ [lu].
- Pyth : tout accès Core payant depuis le 31 juillet 2026 ; actions américaines à 5 000 $/mois [lu].
- Chainlink : 25 flux actions sur Ethereum, tous `new` ou `custom` (86 400 s, 0,5 %) ; « Single provider for Extended & Overnight Data » [lu].
- IEX DEEP+ : 3 500 $/mois ; différé IEX gratuit [lu].
- Incident Ventuals : 1,51 M$ liquidés [2nd].
- Tous ces chiffres viennent de P8 §1-§3.

**Incertain.**
- Fournisseur unique de Chainlink en sessions étendues : non identifié.
- Conditions d'utilisation de Cboe et d'IEX : non lues.
- Écart SPYx entre Kraken et Solana : une seule prise.
- Statut juridique de la publication de mesures sur des produits interdits aux personnes américaines (P8 §5, Q1).

### 1.8 Produit et livrables

| profil | livrable d'ouverture | ensuite | renvoi |
|---|---|---|---|
| P1 | **Fiche de racines par actif**, au format d'un post de gouvernance, gratuite, pour six actifs d'Aave et les feeds Aggor de Spark | tableau public par feed ; alerte (« seul objet payant plausible à 12 mois ») ; API ; certificat après S2-bis | P1 §2.5, R-7 |
| P2 | **Attestation JSON signée** (RFC 8785, champ `non_claims` obligatoire), vérificateur hors ligne, serveur MCP en lecture seule, gratuits | cas « pile par défaut d'un agent » ; positionnement dans x402 et ERC-8004 | P2 R3-R5 |
| P3 | **Rapport de concentration de livraison** exportable dans la sémantique du registre DORA ; paquet de gouvernance IOSCO | assurance ISAE 3000 / SOC 2 quand un client paie | P3 R3, R5 |
| P4 | **Classement public de la lisibilité et de la concentration des oracles** (tableau et graphe datés) ; « n'attend pas R1 » | certificat sur pool nommé | P4 §6 Q3 |
| P5 | **Rejeu historique public des dépegs** (2022-2026), sans VPS | observable rachat contre marché | P5 E, F |
| P7 | **« Root Count »**, benchmark public gratuit IOSCO-lite (méthodologie v1.0, JSON signé, `llms.txt`, identifiants DTI) | rapport payant sur pool nommé ; monitoring ; dossier DORA ; certificat après S2-bis | P7 R1, R4 |
| P8 | (actions) publication R2 des racines uniques déclarées par les oracles | — | P8 R4 |

**Accords.**
- Une mesure **gratuite, publique, recalculable** d'abord (tous, en ligne avec « position d'abord »).
- Le certificat R1 seulement après un S2-bis décisif (P1, P3, P7 ; P2 : « R2 vendable aujourd'hui »).
- Des sorties lisibles par machine (P2, P7).
- Ne jamais dire « prix juste » ni « indépendant » (tous).

**Désaccords.** Aucun désaccord de fond ; ce sont des priorités différentes pour le premier artefact (fiche, attestation, rapport DORA, classement, rejeu, Root Count). Plusieurs sont compatibles [synthèse] :
- Root Count (P7) et le classement (P4) se recouvrent ;
- la fiche de P1 est une vue par actif du même contenu ;
- l'export DORA de P3 est une mise en forme du bloc 6 ;
- le rejeu de P5 est indépendant de S2-bis.

**Incertain.** Aucun livrable n'a été montré à un acheteur.

### 1.9 Acheteurs et canal

| profil | acheteurs | canal | renvoi |
|---|---|---|---|
| P1 | Grands protocoles de prêt ; **Spark/Sky** (trois oracles) ou Aave ? Les cabinets (Chaos Labs, LlamaRisk) sont conflités : ils opèrent des oracles | forums de gouvernance, préavis privé ; aucun revenu P1 avant 2027 [inféré] | P1 §2.4, §5 |
| P2 | Plateformes et vendeurs de données (Coinbase CDP, Virtuals, ElizaOS, Pyth, Chainlink for Agents, CMC, CoinGecko), conflités pour certains ; **pas les agents** | MCP, JSON, registres ; commentaires x402 #3234 | P2 R4, R6 |
| P3 | Sponsor d'ETP (CME CF), CASP MiCA (DORA via MiCA art. 68(7)), banque exposée à USDC (Bâle 1b) | préavis aux places et aux administrateurs ; vocabulaire du registre | P3 §5 Q1, R6 |
| P7 | **Oracles challengers** (Chronicle, RedStone), Aave V4 privé de Chaos Labs, CASP MiCA et émetteurs EMT ; agents par MCP | préavis privé de 14 jours puis publication nominative | P7 R4 |
| P8 | Protocoles qui acceptent des actions tokenisées en garantie (Venus, Lista, Kamino), émetteurs, marchés perpétuels HIP-3, régulés | — | P8 R4 |

**Accords.**
- Le revenu viendra après la position (tous).
- La place de tiers non conflité se vide (P1 §2.4, P7 §2.2).
- Préavis privé avant toute publication nominative (P1, P2, P3, P7).

**Désaccords.**
- **Faire des oracles des clients.** P7 cite Chronicle et RedStone comme premiers clients, en précisant que RedStone est « ambivalent ». P1 et P2 insistent sur le conflit des vendeurs et des cabinets. P7 lui-même pose la règle « jamais de paiement de la partie mesurée pour être mesurée », assouplie pour un rapport publié.
- Préavis : 14 jours (P7 R1) ou 30 jours (P3 R6).

**Faits chiffrés qui comptent.**
- Chaos Labs chez Aave : 3 M$ par an (environ 2 % d'un revenu 2025 de 142 M$) ; 8 M$ demandés ; 5 M$ offerts ; départ le 6 avril 2026 [lu-extrait, P1 §2.4 ; lu, P7 §2.2].
- Kaiko : environ 250 clients après le rachat d'Amberdata [2nd, P4 §2.2].
- x402 « plausiblement agentique » : 5 000 à 11 000 $/mois [lu, TRM, P2 §2.4].

**Incertain.** Aucun acheteur interrogé (P1 §4, P7 §4) ; la demande réglementaire est inférée, non constatée (P3 §4 pt 1).

### 1.10 Prix

| profil | hypothèse | niveau | renvoi |
|---|---|---|---|
| P1 | Module « racines des feeds » : 50 à 200 k$/an par grand protocole | [inféré, non étayé] | P1 §2.5 |
| P2 | Score d'indépendance : gratuit ou une fraction de millime ; au-dessus de 0,01 $ par appel, hors norme | [inféré] sur repères [lu]/[2nd] | P2 §2.3 |
| P7 | Rapport sur pool nommé : 10-30 k€. Monitoring : 500-2 000 $/mois par feed. Dossier DORA : 20-50 k€/an. Certificat : après S2-bis | [inféré] par comparables | P7 R4 |
| P3 | Tarifs des benchmarks régulés et de l'assurance ISAE : non obtenus | manque | P3 §4 pt 5 |

**Comparables chiffrés.**
- Pyth : Starter 500 $/mois (« No redistribution rights ») ; Pro à partir de 2 500 $/mois ; actions américaines 5 000 $/mois [lu, P2, P8, ADR §3].
- Chainlink Data Streams : à partir de 150 $/mois [lu, P7].
- DefiLlama Pro 300 $/mois [2nd] ; Token Terminal 350 $ [lu] ; Messari 500 $ [2nd] (P7).
- CoinGecko : Basic 35 $/mois pour 100 000 crédits ; Analyst 129 $ pour 500 000 crédits [lu, P2].
- x402 : prix médian par appel 0,02 $ [2nd, P2].
- Gauntlet : 1,6-2 M$/an (P1, citant doc 07) ou 1,6-2,3 M$/an (P7, citant doc 07).

**Accords.** Tous les prix proposés sont des inférences. Aucun ne s'applique avant la publication et un recalcul externe.

**Désaccords.** Des ordres de grandeur incompatibles selon l'acheteur [synthèse] :
- P1 : 50-200 k$/an par protocole ;
- P7 : monitoring à 6-24 k$/an par feed, rapport à 10-30 k€ ;
- P2 : environ 0 pour les agents.
C'est cohérent avec trois acheteurs différents, mais aucune des trois fourchettes n'est étayée.

**Incertain.** Tout.

### 1.11 Gouvernance et standardisation

**Positions.**
- **P7** : forme IOSCO-lite.
  - `METHODOLOGIE-v1.0.md` public, changelog, procédure de réclamation ;
  - comité de trois personnes dont une externe, minutes publiées ;
  - page « Financement » par paliers ;
  - identifiants DTI (ISO 24165) ;
  - soumission aux groupes EEA DeFi Risk ;
  - pas de BMR (P7 R1, R5).
- **P3** : méthodologie au format IOSCO (P9, item h « concentration of inputs ») ; recalcul tiers ; assurance ISAE 3000 ou SOC 2 ; horodatage RFC 3161 ; vocabulaire DORA. Pas de statut BMR (révision 2025/914). Un comité externe est un canal de conflit si des oracles y siègent (P3 R5, §2.5).
- **P2** : place dans x402 (`response-provenance`) et ERC-8004 (registre de validation) ; ne pas lier la réputation au registre ERC-8004, dégradé par du Sybil (P2 R4).
- **P1** : nommer, ne jamais noter (ADR-0007) ; publier seulement du recalculable (P1 R-3, R-7).

**Accords.**
- Pas de BMR (P3, P7).
- La forme IOSCO est le chemin le moins cher vers la crédibilité (P3, P7).
- Recalcul tiers (tous) ; horodatage opposable (P3 ; ADR §2.8).

**Désaccords.**
- **Financement par des acteurs mesurés.** P7 (question 1) l'admet s'il est déclaré, sur le modèle de L2BEAT. P3 veut une règle d'indépendance écrite pour le comité. La règle d'or de P7 interdit le paiement « pour être mesuré ».
- **Assurance tierce.** Avant le premier client (option posée par P3, question 2) ou à 9-18 mois (P7 R5) ?

**Faits chiffrés qui comptent.**
- BMR 2025/914 : à partir du 1er janvier 2026, seuls les benchmarks critiques ou significatifs restent dans le périmètre [lu, P3 §2.1].
- CF Benchmarks : FRN 847100 ; audit ISAE 3000 par KPMG [lu, P3, P7].
- clientdiversity.org : trois estimations incompatibles affichées en septembre 2026 [lu, P7 §2.1].

**Incertain.**
- Aucun texte DORA ou MiCA détenu dans biblio (P3 §4 pt 3 ; P7 §4).
- L'attribution « RPC et oracles = tiers ICT » est un commentaire de cabinet [2nd] (P7).

### 1.12 Licences

| objet | état | renvoi |
|---|---|---|
| Pyth | « No redistribution rights » ; clé exigée | ADR §2.5 ; P2 ; P8 |
| CoinGecko sans clé | « not suitable for scheduled polling » (lecture worker non re-établie) ; « 5 to 15 calls per minute » [lu, extrait] ; offre Demo de 10 000 crédits/mois, alors qu'une lecture par minute en consomme 43 200 [calc] | ADR §5 ; P6 C5 ; P2 R1 |
| CoinPaprika | redistribution réservée à l'offre Enterprise [lu] | EP §2.2 |
| RedStone | conditions du site : pas d'usage automatisé ; la documentation de la passerelle exige une clé [lu] ; licence des données non lue | EP §2.3 ; P4 §5 |
| Chronicle | BUSL-1.1 [lu] | EP §2.3 |
| CF Benchmarks | licence requise [lu] | EP §2.2 |
| Places (Crypto.com, Bitget, KuCoin, HTX, MEXC, Gate…) | conditions non lues | EP §2.1, §6.2 ; P4 §5 ; P5 §4 pt 5 |
| Actions : SIP, IEX, Cboe | SIP payant (1 000 $/mois de redistribution, [2nd]) ; différé IEX gratuit [lu] ; conditions Cboe non lues | P8 §3 |
| Item du dépôt | SHOGEN-S2BIS-LICENCES-API-1 (republication des octets bruts) | ADR §5 |

**Accords.** La question de la redistribution des octets bruts (ADR-0003/0005) n'est tranchée pour **aucune** source nouvelle. Elle se lit avant le sceau.

**Désaccords.** Que faire d'une source non redistribuable ? P2 (question 2) propose de publier des empreintes et des valeurs dérivées. P7 R3 et EP veulent la garder dehors.

### 1.13 Risques

| risque | cité par | renvoi |
|---|---|---|
| Multiplicité et dilution de puissance si l'on ajoute des classes confirmatoires ou des unités | P2, P4, P5, P6, EP | P6 §3.1, §3.4 ; EP §7 |
| Stables NON ÉVALUABLE (pas de dépeg en 16 semaines ; axe hors-enveloppe silencieux) | P1, P5, P6 | P5 §4 pt 4 ; P6 §3.6 |
| F2 vide si BTC ne rejette pas | P6 | P6 §3.6 |
| Retrait d'un accès sans clé en cours de campagne (RedStone, CoinGecko en vente vers 500 M$ [2nd], bascule de Pyth) | P4, P8, EP | P4 §4 (a) ; EP §7 |
| Géo-blocage (Binance 451, Bybit 403) | P4, P5, P8, EP | EP §2.1 |
| Chemin de lecture RPC concentré sur AS13335 | P3, P4, P5, EP | EP §3 |
| Calibration sur clôtures de bougies qui sous-estime la dispersion | P6 | P6 §3.6 |
| Conflit d'intérêts, capture par un oracle partenaire (Credora absorbé par RedStone) | P1, P3, P7 | P7 R6 |
| Contestation juridique après nomination ; produits interdits aux personnes américaines | P2, P3, P7, P8 | P7 R6 ; P8 R5 |
| Surclamation (« indépendant », « prix juste ») | tous | — |
| Sceau décalé d'une à deux semaines par CALIB-ACTIFS | P6 | P6 §3.6 |
| Volume de la passerelle RedStone | P4, EP | EP §3 |

---

## 2. Contradictions factuelles entre rapports

| # | fait | version 1 | version 2 | lecture [synthèse] |
|---|---|---|---|---|
| **C1** | **Antériorité de la mesure S2 sur les pannes de 2025** | P7 §2.3 : « S2 avait mesuré le **28 sept. 2025** … la mesure précède l'incident de sept semaines » ; P7 R1 : « le J28 précède la panne Cloudflare ». P3 §2.3 : « La mesure de Shōgen avait nommé en septembre le mode commun qui s'est manifesté en novembre » | D11 §2.3 et §4.1 [dépôt] : segment S2 du **2026-08-26** au **2026-09-28** ; partition ASN datée du 2026-09-28. Pannes AWS (2025-10-20) et Cloudflare (2025-11-18, 2025-12-05) : P1, P3, P4, P7 | **Erreur d'année chez P7 et P3** : S2 vient environ **10 mois après** ces pannes. L'argument « la mesure a précédé l'incident » est faux. P1 §2.3 donne la lecture compatible avec les pièces : aucune perte de feed documentée ne vient d'un mode commun d'hébergeur, et Shōgen mesure « avant le sinistre ». P3 précise d'ailleurs que S2 n'a pas observé ces pannes |
| **C2** | Coinbase a-t-il un marché USDC-USD ? | P1 R-1 : USDC/USD « lisibles sur Kraken, Bitstamp, Coinbase ». P3 R2 : « Kraken, Coinbase, Bitstamp USDC/USD ». P7 R2 : « places fiat : Kraken, Coinbase, Bitstamp, Gemini » | P4 §2.5 : **404** ; P5 §1.1 : 404 (« conversion 1:1, pas de carnet ») ; P6 C3 : absent de `/products` (cache, à recontrôler) | Trois sondes concordantes contre trois affirmations non sondées. Le pool USDC/USD fiat se réduit à Kraken, Bitstamp, Bitfinex (et Gemini, oui chez P4) |
| C3 | Heartbeat de Chainlink USDC/USD sur Ethereum | P2 §2.5 : 86 400 s | P4 §2.5, P5 §1.1, P6 C1 : **82 800 s** (même annuaire) | Trois lectures concordantes contre une |
| C4 | Composition de l'oracle Hyperliquid | P2 §2.2 et P4 §2.4 : médiane Binance, OKX, Bybit, Gate, MEXC, poids 3/2/2/1/1 (page « robust price indices », mid des perpétuels) | EP §2.3 [lu, `oracle.md`] : Binance, OKX, Bybit, Kraken, KuCoin, Gate, MEXC et Hyperliquid spot, poids 3/2/2/1/1/1/1/1. P7 §2.2 : 7 CEX (Kraken, KuCoin, Gate, MEXC à 1) | Probablement deux objets différents (indice de marque des perps contre oracle spot). P4 range le premier sous « prix oracle ». À trancher sur pièce |
| C5 | Montant compensé par Binance (10 oct. 2025) | P1, P2, P4, P5 : 283 M$ | P3 §2.3 : 283 puis **328 M$** [2nd] | 328 vient d'une seconde main seule |
| C6 | Fin de la fenêtre USDe et prix bas | P1, P2, P4 : 21:36-22:16 UTC ; P1, P5 : environ 0,65 $ ; P2 : sous 0,66 | P3 : 21:36-22:15, 0,6567 $ ; P7 : environ 0,62-0,65 $ | Écarts mineurs de source |
| C7 | Incident Moonwell (cbETH) | P1 §2.3 : **18 fév. 2026**, cbETH à environ **1 $**, environ 1,8 M$ [2nd] | P5 §1.2 : **15 fév. 2026**, environ **1,12 $** pendant 4 min, 1 779 044,83 $ [lu, forum Moonwell]. P4 §2.1 : 2026-02-15, 1,78 M$, « feed OEV mal configuré » [2nd] | P5 seul cite le post-mortem primaire. P4 attribue une cause différente (OEV) de celle de P5 (taux sans multiplication par ETH/USD) |
| C8 | Plus bas d'USDC en mars 2023 | P3, P7 : 0,86 $ (Fed) | P6 C4 : 0,8726 $ (agrégat CCCAGG) ; P5 : Chainlink 0,8800, Bitstamp 0,8256 (bougie), « sous 0,88 » (Chaos Labs) | Objets différents (marché secondaire, agrégat, oracle, une place). Il faut nommer l'objet à chaque citation |
| C9 | Ce que fait le FixCapAdapter d'Aave sur les stables | P7 §2.6 : « fixed 1:1 peg », Aave ne lit pas USDC/USDT au marché | P1 §2.2 : plafond fixe, par exemple 1,04 $. P5 §1 pt 4 : plafond vers 1,04 $, **baisses transmises** | P7 décrit un prix fixe ; P1 et P5 un plafond haut seulement. À relire sur `aave-price-feeds` |
| C10 | Lisibilité de Chronicle | P7 R3 : « lisible on-chain » ; P1 R-3 : liste blanche « pour certains contrats », non vérifiée | EP §2.3 [lu, Scribe.md] : lecture protégée par le module Toll. P4, P5 [2nd] : liste blanche | EP seul cite le code primaire |
| C11 | Candidats « hors Cloudflare » | P1 R-5 : Bybit, Crypto.com, Bitget comme places « hors Cloudflare » (statut non vérifié) | P4 §2.5 et EP §4 : Crypto.com et Bitget sur **AS13335** ; Bybit sur AS16509 (CloudFront) | P1 avait déclaré ne pas avoir vérifié |
| C12 | Accès sans clé à CoinMarketCap | P2 R1 : CMC comme « agrégateur nouveau » (accès sans clé non lu, P2 §4) | P4 §2.2 : 401 code 1002 [lu] ; EP §2.2 : 401 « API key missing » [sonde] | CMC est hors de l'invariant « sans clé » |
| C13 | Dernier prix REST de Band | P4 §2.5 : il y a environ 130 jours (76 370 $) | EP §2.3 : `resolve_time` du 2025-09-25, soit 374 jours | Points d'accès ou chemins différents, possiblement. Les deux concluent à l'exclusion |
| C14 | Date du passage de Pyth au payant | P8 §2 : « all Pyth Core data access » payant depuis le **31 juillet 2026** [lu, blog du 12 juin] | EP §2.3 [lu, `llms.txt`] : clé Hermes exigée « since August 26, 2026 ». D11 et ADR : 401 dès le 2026-08-26 à 19:00Z | Peut-être deux étapes ou deux produits (Core contre Hermes) ; non tranché |
| C15 | Nombre d'éditeurs Pyth | P1 : « 135+ institutions » [lu-extrait] | EP, P7 : 120+ [lu] | Pages ou dates différentes |
| C16 | Parts de TVS des oracles | P4, P7 (2026-10-04) : Chainlink 38,3 Md$ / 534 ; Chronicle 5,1 ; RedStone 4,3 ; Pyth 3,7 | EP §5 (doc 07, juillet 2026, [2nd]) et P4 (oracles.ink, juin) : Chainlink environ 33 Md$ / 505 ; Chronicle environ 7,5 ; RedStone 3,6 ; Pyth 3,1. Messari T4 2025 : Chainlink 73,1 % [2nd]. RedStone déclare plus de 10 Md$ de TVL [lu, partie intéressée, EP] | Dates et périmètres différents. Chronicle passe de 7,5 à 5,1 entre juin et octobre |
| C17 | Composition des garanties Aave | P1 (Token Terminal, mars 2026) : WETH 16,8 %, USDT 13,2 %, weETH 11,8 %, USDC 10,7 % | P1 (Galaxy) et P7 (mai 2026) : WETH 25 %, weETH 21 %, wstETH 14 %, WBTC 13 % | Mesures différentes (composition de l'offre contre garanties activées) |
| C18 | Taille d'Aave | P1 : total fourni 33,77 Md$, emprunté 13,30 Md$ (aavescan, instantané) ; dépôts Aave V3 de 16,8 à 17,6 Md$ (DefiLlama) | P7 : 10,7 Md$ de dette pour 17,4 Md$ de garanties (mai 2026) | Dates et définitions différentes |
| C19 | Âge du prix Pyth sur le contrat Ethereum | P4 : 72 jours | EP : 73 jours (publié le 2026-07-23 à 18:42:56Z) | Mineur (arrondi, instant de sonde) |
| C20 | Coût de Gauntlet (doc 07) | P1 : 1,6-2 M$/an | P7 : 1,6-2,3 M$/an | Lectures différentes d'une même pièce du dépôt |
| C21 | Flux cotés en USDT en S2 | P6 C3 : 2 sur 12 | P2, P5 : 2 sur 11 ; D11 §2.1 : pool configuré de 12 flux, pool d'analyse 9 USD / 2 USDT | Pas une contradiction : P6 compte le pool configuré, Pyth compris |
| C22 | Ce que lisent les agents chez RedStone | P4 : « 150+ sources » [lu] | EP : « over 30 premier cryptocurrency exchanges » et « more than 50 on-chain trading protocol deployments » [lu] | Pages différentes de la même documentation |

---

## 3. Options d'architecture pour S2-bis (sans trancher)

**Socle commun à toutes les options**, fixé par l'investisseur et par l'ADR :
- M = 4 observateurs sur VPS, quorum majoritaire, rotations, pré-enregistrement prospectif ;
- ETH, USDC et USDT **entrent au périmètre** sous une forme ou une autre ;
- Pyth dehors ; actions tokenisées hors S2-bis (P8 ; relevé descriptif facultatif).

Hypothèses communes, issues des pièces :
- Budget VPS de l'ADR : **environ 165 € à 605 €** pour toute la campagne (16 semaines nominales, T_max 24 ; 5 à 7 mois facturés) [dépôt, ADR §3].
- Ajouter des actifs ne demande **aucun VPS de plus** (P2 R1, P6 §3.6, P7 R2).
- Puissance de référence, BTC, 10 unités, cellule cible : 0,91 en calme et 0,54 en stress à 16 semaines (synthétique) [dépôt, ADR §2.4 d].
- Jalons de l'ADR : sceau à S+8, fin attendue S+25, T_max S+32 [dépôt, ADR §6].

### Option A — BTC seul confirmatoire, pool BTC inchangé ; ETH, USDC, USDT exploratoires ; cartographie élargie hors vote

**Composition.**
- F1 = BTC/USD, 10 unités-hôtes de l'ADR §2.5, règle R1-2 inchangée.
- ETH/USD, USDC/USD et USDT/USD : même moteur, imprimé « hors décision ».
- « Voie B » d'EP : sources supplémentaires (places, DEX, DIA, RedStone contrat, Hyperliquid…) lues par les mêmes observateurs, R2 et contenu seulement.

**Puissance.** Celle de l'ADR, sans perte [dépôt]. Les nouvelles classes ne consomment aucun α.

**Durée.** Calendrier de l'ADR. La calibration τ/σ des nouvelles classes reste nécessaire pour un descriptif propre, sans bloquer le sceau BTC [synthèse, d'après P6 §3.3 et EP §6].

**Budget.**
- VPS : fourchette de l'ADR.
- Code : collecte et décodeurs par actif, environ +300 à 500 lignes (P6) ; un décodeur par source de la cartographie (P4, EP).
- Volume : si la passerelle RedStone entre dans la cartographie avec ses octets bruts, environ 2,8 Go par jour et par observateur (EP §3). Sur 7 mois et 4 observateurs, de l'ordre de 2,4 To, plus que la Storage Box de 1 To budgétée [calc synthèse sur EP §3 et ADR §3]. Hors RedStone, les journaux restent petits (S2 : 395 Mo pour 28 jours [dépôt, ADR §3]).

**Ce que cela permet de vendre.**
- Un énoncé confirmatoire sur BTC.
- Une carte R2 et contenu sur quatre actifs et sur les trois natures de sources : Root Count (P7), classement de lisibilité (P4), fiches par actif (P1), axe « devise de cotation ».
- Aucune phrase confirmatoire sur ETH ou les stables.

**Risques.**
- Le message « ETH, USDC et USDT ajoutés » ne porte que du descriptif.
- La cartographie élargie double la charge de décodeurs et de licences à lire.

**Ce que disent les profils.** Soutenue par P4 (question 1, première branche), P5 (BTC confirmatoire, ETH descriptif) et EP (voie B). Proche du plan de P6 sans la séquence ETH.

### Option B — BTC confirmatoire, ETH en séquence fixe, stables exploratoires (« option A » de P6)

**Composition.**
- F1 = BTC (10 unités, inchangé).
- F2 = ETH/USD, pool d'hôtes propre (mêmes hôtes, symbole ETH), testé à 0,01 dans la strate s **seulement si** BTC rejette dans s.
- F3 = USDC et USDT exploratoires.
- Pré-enregistrement : les 9 points de P6 §3.6.

**Puissance.**
- BTC : inchangée.
- ETH : à calculer par SIM-PUISSANCE-BIS à une cellule cible propre (non calculée, P6 §3.6 pt 7).
- P(au moins un rejet à tort) ≤ 0,02 sous toute dépendance (P6 §3.1, d'après la FDA 2022 [lu]).

**Durée.** Sceau décalé d'**une à deux semaines** : lot CALIB-ACTIFS d'environ 200 lignes, sur historiques à 1 minute antérieurs et disjoints (P6 §3.3, §3.6).

**Budget.** VPS inchangés. Code : +300 à 500 lignes de collecte, +200 de rendu, +200 pour CALIB-ACTIFS (P6 §3.6).

**Ce que cela permet de vendre.**
- Un énoncé confirmatoire possible sur **deux actifs**, sans α retiré à BTC.
- Une première mesure stablecoin publiée, déclarée exploratoire, qui prépare une confirmation en S3 (P6 §1 pt 10).

**Risques.**
- F2 vide si BTC ne rejette pas (P6 §3.6) : alors ETH ne peut pas être confirmé.
- Calibration sur clôtures de bougies (P6).
- Rotation jointe par hôte à sceller pour toute statistique multi-classes (P6 §3.6 pt 8).

### Option C — BTC et ETH confirmatoires de même rang ; stables descriptifs

**Composition.** Deux classes confirmatoires, quatre hypothèses (deux actifs × deux strates). Au choix, à sceller :
- Bonferroni à 0,005 par hypothèse : seuil C_s ≤ 49 à R = 9 999 [calc synthèse : (49 + 1)/10 000] ;
- Holm sur quatre hypothèses ;
- Westfall-Young min-P sur rotations jointes par hôte (P6 alternative C, la plus puissante sous corrélation, plus complexe à sceller).

**Puissance.**
- BTC **plus faible** qu'à l'ADR (seuil divisé par deux pour Bonferroni). La cellule cible et les 16 semaines avaient été calculées à 0,01 (P6 §3.1 sur l'alternative B).
- P6 note aussi que les tests BTC et ETH sont fortement corrélés sur l'axe panne : un second actif apporte peu d'information indépendante sur la disponibilité (P6 §3.1).
- Valeurs à produire par SIM-PUISSANCE-BIS ; non chiffrées dans les pièces.

**Durée.** Pour revenir à une puissance de 0,8 à la cellule cible en calme, il faudrait probablement allonger la campagne au-delà de 16 semaines, ou déclarer une cible plus forte [inféré, P6 §3.1 ; ADR §4, ligne « campagne de 12 semaines »]. Allongement non chiffré. Le T_max de 24 semaines est déjà dans la fourchette haute du budget.

**Budget.** Comme B, plus des mois de VPS si la campagne s'allonge : environ 23 à 60 € par mois selon la fourchette [dépôt, ADR §3].

**Ce que cela permet de vendre.** Un énoncé symétrique sur deux actifs, indépendant du résultat BTC.

**Risques.** P6 la juge « casser la décision », puisque la cellule cible a été scellée au niveau 0,01. Ni ETH ni BTC n'ont de puissance calculée à ce niveau.

### Option D — Quatre classes confirmatoires (lecture littérale de P7)

**Composition.** BTC, ETH, USDC et USDT, chacun avec deux strates : huit hypothèses, Holm à 0,02 (P6 alternative B), ou séquence fixe BTC → ETH → USDT → USDC (P6 A′).

**Puissance.**
- Holm : seuil BTC à 0,0025 au premier pas, soit C_s ≤ 24 (P6 §3.1).
- Stables probablement NON ÉVALUABLE faute d'écarts (P5, P6).
- A′ ne coûte aucun α, mais un REJETTE stable sous un τ mal calibré serait une surclamation (P6 §3.1).

**Durée.** CALIB-ACTIFS obligatoire pour USDC et USDT. Des campagnes plus longues, ou déclenchées par un événement, pour que les stables parlent des dépegs (P6 question 2).

**Budget.** VPS inchangés à durée égale. Code : environ 30 décodeurs côté stables et LST si l'on suit P5 A.

**Ce que cela permet de vendre.** Le message « quatre actifs certifiés de même rang » (P7), si le résultat le permet.

**Risques.**
- Puissance BTC dégradée.
- Stables NON ÉVALUABLE à forte probabilité.
- Règle de régime à concilier avec les strates ex ante (P5 §2.3).

### Option E — Pool BTC élargi à environ 15 unités dans le confirmatoire (« voie A » d'EP), avec B ou A pour les autres actifs

**Composition.**
- BTC : 10 unités + au plus 5 ajouts d'EP §6.1 : Crypto.com, Bitget, KuCoin, HTX ou MEXC, et Uniswap v3 WBTC/USDC sur un **hôte RPC distinct** (Tenderly, AS396982).
- Critères d'entrée C1 à C7 écrits au paquet.
- Statistique S (paires) éventuellement préférée à K≥2, fixée avant le sceau (P6 §1 pt 7).
- ETH, USDC, USDT selon A ou B.

**Puissance.**
- La cellule cible (« 7 hôtes AS13335 ») doit être redéfinie et re-simulée (EP §6, §7).
- Selon P6, la puissance baisse si les ajouts sont hors du mode commun : MEXC (Akamai), Uniswap via Google Cloud.
- La simulation de P6 n'est pas versée.

**Durée.** CALIB pour les unités nouvelles (aucune donnée de S2 : EP §6 (ii)), plus la lecture des licences des places : décalage du sceau non chiffré dans les pièces.

**Budget.** VPS inchangés. Un décodeur et des fixtures par unité. Environ 15 requêtes par minute et par observateur côté BTC, sous les limites lues (EP §7).

**Ce que cela permet de vendre.** Un confirmatoire plus proche de « ce que les clients lisent » : plus de grandes places et une racine DEX. Le k_eff ASN monte au plus de 4 à 6 (P4, EP).

**Risques.**
- Ajouts quasi-copies qui déplacent l'hypothèse nulle (EP §7).
- Licences non lues.
- Bybit et Binance dépendent du smoke de chaque observateur.

### Variante transversale (combinable avec A à E) : seconde vague, ou campagne événementielle, pour les stables

**Composition.** S2-bis garde sa forme. Les stables, voire ETH, reçoivent leur propre pré-enregistrement après calibration, en seconde vague (P4 question 1), ou dans une campagne déclenchée par un dépeg (P6 question 2). En attendant, un **rejeu historique public des dépegs** (P5 E) tient lieu d'artefact.

**Conséquences.**
- Aucun effet sur le sceau BTC.
- Second sceau et seconde exécution unique à prévoir.
- Coût du rejeu : 1 à 2 semaines-lot sans VPS (P5 E).
- Une campagne événementielle pose une question de pré-enregistrement : déclencheur écrit d'avance, ensemble témoin disjoint (P5 §2.3).

### Tableau comparatif [synthèse]

| | α retiré à BTC | énoncé confirmatoire possible | décalage du sceau | puissance chiffrée dans les pièces | charge principale |
|---|---|---|---|---|---|
| A | non | BTC | aucun pour BTC | oui (ADR, synthétique) | cartographie, licences |
| B | non | BTC ; ETH si BTC rejette | 1-2 semaines (P6) | BTC oui ; ETH non | CALIB-ACTIFS |
| C | oui (÷ 2 au moins) | BTC et ETH | 1-2 semaines + allongement probable | non | re-simulation, durée |
| D | oui (÷ 4 au moins avec Holm) | quatre actifs | CALIB + campagne plus longue | non | stables NON ÉVALUABLE |
| E | selon le choix pour ETH | BTC élargi | CALIB des unités + licences | non (simulation non versée) | cellule cible à redéfinir |

---

## 4. Questions de valeur pour l'investisseur (dédoublonnées, en langage clair)

Les questions proposées par les huit profils, regroupées. Les numéros renvoient au §5 (ou §6) de chaque rapport.

1. **Qui décide ?** Acceptez-vous que seul BTC tranche la question « les sources tombent-elles en panne ensemble ? » ? ETH serait confirmé seulement à la suite de BTC, et les stablecoins publiés comme mesure exploratoire. L'alternative : tout mettre au même rang, au prix d'une mesure plus longue ou moins sensible (P6 Q1, P5 Q1, P4 Q1).
2. **Pool plus grand ou pool plus ciblé ?** Beaucoup de sources donnent une carte plus complète du marché mais une décision moins nette ; un petit pool BTC resserré décide mieux (P6 Q3 ; EP voies A et B).
3. **Que veut-on mesurer sur les stablecoins ?** Leur prix contre le dollar réel (3 places liquides, Coinbase absent) ? Leur prix tel que la DeFi le consomme (dominé par USDT) ? Leur écart au pair de 1 $ ? Ou les trois, avec leurs écarts ? Ce choix doit être fait avant le sceau (P5 Q2, P7 Q2).
4. **Accepte-t-on une mesure stablecoin qui dira surtout « rien à signaler » ?** En 16 semaines calmes, c'est le résultat probable. Pour parler des décrochages, il faudrait une campagne plus longue ou déclenchée par un événement. Ou ne rien publier en R1 sur les stables, et seulement les racines (P6 Q2, P1 Q2).
5. **Premier artefact : un rejeu des décrochages passés ?** Publier d'abord, sans serveur, un rejeu recalculable des dépegs de 2022-2026 ? (P5 Q3)
6. **Accès sans clé fragile ou clés payantes ?** Dépendre d'accès gratuits tolérés mais non garantis (RedStone, CoinGecko), avec remplacement écrit d'avance ? Ou financer une ou deux clés payantes (Pyth, Kaiko, CoinGecko Pro), au risque de ne plus pouvoir republier les données brutes ? (P4 Q2 ; même logique pour les actions, sous-jacent en différé de 15 minutes ou licence, P8 Q2)
7. **Sources qui interdisent la republication.** Publier des empreintes et des valeurs dérivées (recalcul moins complet), ou retirer ces sources ? (P2 Q2)
8. **Quel produit d'abord ?** Un classement public, daté, de la lisibilité et de la concentration des oracles (vite, sans attendre R1) ? Ou un certificat sur un pool nommé par le client ? (P4 Q3)
9. **Quel premier acheteur dans 12 mois ?** Trois familles de réponses :
   - un oracle challenger : rapide, risque de capture ;
   - un protocole : Spark (trois oracles, plus démonstratif) ou Aave V4 (budget, gouvernance instable) ;
   - un acteur régulé : sponsor d'ETF, plateforme crypto européenne sous DORA, ou banque exposée à USDC ; lent, mais c'est la position institutionnelle.
   Pour les actions tokenisées : prêteurs, émetteurs ou marchés perpétuels (P7 Q3, P1 Q1, P3 Q1, P8 Q3).
10. **Nommer publiquement ?** Publier gratuitement et nominativement, avec préavis privé : fiches de racines des protocoles, piles par défaut des plateformes d'agents, administrateurs régulés (CF Benchmarks, Kaiko) ? Ou anonymiser pour ménager de futurs partenaires ? Nommer les administrateurs crée le canal institutionnel… et l'adversaire le mieux armé juridiquement (P1 Q3, P2 Q1, P3 Q3).
11. **Revenu différé.** Acceptez-vous qu'il n'y ait aucun revenu des protocoles avant 2027, le payant attendant un recalcul externe ? (P1 Q3)
12. **Financement par des acteurs mesurés.** Accepter des financements déclarés de fondations ou de partenaires, y compris d'acteurs que Shōgen nommera, à condition de tout publier (modèle L2BEAT) ? Ou une exclusion stricte, qui retarde le revenu ? (P7 Q1)
13. **Assurance tierce.** Payer une assurance indépendante (ISAE 3000 / SOC 2) avant le premier client, pour en faire une pièce de dossier de conformité, ou seulement après ? (P3 Q2)
14. **Temps consacré aux agents IA.** Une semaine pour le format signé, le serveur MCP et les commentaires de standards, sachant que la demande payante des agents est quasi nulle en 2026 ? Ou rien avant le premier recalcul externe ? (P2 Q3)
15. **Actions tokenisées, périmètre juridique.** Shōgen peut-il publier, gratuitement, des mesures sur des produits interdits aux personnes américaines (xStocks, Ondo, Robinhood) ? Ou faut-il commencer par les actions émises nativement, plus petites mais au statut plus clair ? (P8 Q1)

Les huit questions de l'ADR §6 (budget, comptes, durée, Pyth, brin notarié, accès, horodatage quotidien, publication) restent ouvertes à part. La question 4 sur Pyth est confirmée par tous les profils.

---

## 5. Ce qui reste incertain, transversalement

- Aucun acheteur interrogé, aucun prix étayé (P1, P2, P7).
- Licences de redistribution : non lues pour toutes les sources nouvelles (EP, P4, P5, P8).
- Puissance de toute composition autre que « BTC, 10 unités » : non calculée ou non versée (P6 §3.4, EP §7).
- Lisibilité depuis les régions des observateurs (Singapour, UE) : non essayée. Binance et Bybit dépendent du smoke (P4, P5, EP).
- Les trois rapports hors roster (P1, P3, P7) portent les positions de marché et de gouvernance ; deux erreurs factuelles en viennent (C1, C2).

## 6. Statut de clôture

- P6 §3.4 relu au début et à la clôture de la passe : les marqueurs `TABLE_SIM` et `RESULTATS_SIM` sont toujours présents (voir la ligne finale). La simulation de taille de pool **n'est pas intégrée** à cette synthèse. Si elle est versée, les §1.4 et §3 (options A, C, E) sont à compléter sur ce point seulement.

- Relecture finale de P6 à 05:44:59 UTC : RAPPORT.md inchangé depuis 04:59 ; marqueurs toujours présents (2 occurrences). Passe close à cette heure.
