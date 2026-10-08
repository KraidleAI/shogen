# G2 — relecture de la cartographie DefiLlama des protocoles DeFi dépendant d'oracles (`CARTO-DEFI-ORACLES.md`)

- **Gate 0** : modèle qui exécute cette relecture : `claude-opus-5-5` (fiche `shogen-worker`, effort max). Réviseur neuf : je n'ai écrit aucune ligne de la pièce, ni de ses scripts.
- **Date** (`date -u`) : 2026-10-04, de 20:36:59 à 20:58:38 UTC (rédaction du rapport ensuite).
- **Brief** : `g2/BRIEF-G2-CARTO.md`, sha256 `14d0b5148001f5e9f86db64c79359bc49d787232a5531306a40ee3d7281b446c`.
- **Pièce relue** : `CARTO-DEFI-ORACLES.md`, sha256 `6b174d70f38767354abb59a0ea7ffee6075dbd7ae8f33e67a9d55649538d4250`. Lecteur : `claude-sonnet-5-5`, effort high, ce qui est conforme au roster des lecteurs. Brief du lecteur : `BRIEF-CARTO-DEFI.md`, `bd8855d9…14bf`.
- **Rattachement (G0)** : ADR-0029, révision 3. Elle porte l'étude de marché versée, `docs/adr-0029/etude-marche/` (l.3 et l.9 ; §6 B, l.415). Ses conventions de niveau sont posées en l.12. La pièce relue est un complément commercial, non normatif, demandé par l'investisseur le 2026-10-04.
- **Base de la copie du dépôt** : `86c07ffe5bc827d818e48d9e735fd63ccbadf070` (branche `claude/compassionate-noether-szmdyj`), arbre propre. Le brief ne fixe pas de base de référence ; je consigne celle-ci.
- **Niveaux** : [lu] = lu dans la pièce, les données brutes ou le dépôt (fichier et ligne nommés) ; [calc] = calcul de mon propre script sur ces données ; [inféré] = mon raisonnement ; [abs] = absent de la source lue.

## 0. Verdict

**ACCEPTE-AVEC-CORRECTIONS** : treize corrections, en liste fermée (§7).

Le corps chiffré de la pièce se reproduit exactement. Mon script est écrit à partir de la seule section 2 de la pièce, sans lire `traite.py`. Avec « mort » = champ `deadFrom` renseigné, il donne 244 cellules ou lignes sur 244 identiques (T0, table par catégorie, T1a à T1d, comptes de T2, T3, T4), ainsi que les nombres de la section 5. La chaîne hors réseau du lecteur rejoue à l'octet près.

Défauts à corriger avant versement :
- La colonne « Valeur déclarée » de T2 n'applique pas la règle écrite en 2.3 : Chaos est surévalué environ 4 fois, RedStone d'environ 23 %, et Chainlink est sous-évalué de 1,3 Md$.
- Trois biais de périmètre ne sont pas déclarés : la définition de « mort », des usages d'oracle sans lien avec un prix, et des paires présentées comme des combinaisons.
- La liste courte s'écarte de sa règle sans le motiver : 4 cibles G sur Ethereum, et Sky, acheteur déjà visé par P1.
- Une citation interne est inexacte (Gauntlet), deux incidents ne sont pas attribués, et trois formulations relèvent du registre 09.

Aucun de ces défauts n'invalide la carte ; tous se corrigent par recalcul de T2 et par des retouches de texte.

## 1. Empreintes (contrôle 1)

`sha256sum -c SHA256SUMS` dans le dossier du lecteur : **48 fichiers sur 48 OK**, sortie 0. Seul `SHA256SUMS` n'est pas listé, ce qui est normal. Un nouveau contrôle en fin de relecture donne aussi 48 sur 48 et aucun fichier modifié hors de `g2/` : je n'ai touché aucun fichier du lecteur.

## 2. Recalcul (contrôle 2)

Mon script, `g2/recalcul_g2.py` (sha256 `0d23545b…2c0e`), est écrit **avant** toute lecture de `traite.py`, `enrichit.py` et `assemble.py`, sur la seule section 2 de la pièce. Les points que la section 2 laisse ouverts y sont des variantes nommées, toutes calculées.

| grandeur | pièce | mon recalcul [calc] | écart |
|---|---:|---:|---:|
| protocoles listés par `/protocols` | 8 483 | 8 483 | 0 |
| périmètre A / B / A+B | 345 / 79 / 424 | 345 / 79 / 424 | 0 (avec « mort » = `deadFrom`) |
| TVL A+B (M$) | 93 313 | 93 313 | 0 |
| avec oracle déclaré | 246 (67 750 M$) | 246 (67 750 M$) | 0 |
| un seul oracle / deux ou plus | 170 / 76 | 170 / 76 | 0 |
| au moins 2 oracles externes (P / M / G) | 73 (48 / 18 / 7) | 73 (48 / 18 / 7) | 0 |
| protocoles qui déclarent Chainlink / Pyth / RedStone | 129 / 66 / 51 | 129 / 66 / 51 | 0 |
| T0, table par catégorie (35 lignes), T1a, T1b, T1c, T1d, T2 (comptes, tailles, trois premières chaînes), T3, T4 | — | 244 cellules ou lignes comparées par `g2/compare_tables.py`, 244 identiques | 0 |
| valeur T2 Chainlink (M$) | 44 722 | 46 060 (règle 2.3) | −1 338 |
| valeur T2 RedStone (M$) | 13 613 | 11 084 (règle 2.3) | +2 529 |
| valeur T2 Chaos (M$) | 3 358 | 828 (règle 2.3) | +2 530 |
| valeur T2 DIA / eOracle / Pyth (M$) | 223 / 185 / 5 941 | 117 / 241 / 5 947 | +106 / −56 / −6 |

- **Contrôle du comparateur** : trois copies de la pièce, mutées chacune d'une seule cellule (table par catégorie, T1a, T4). Le comparateur rend un écart pour chacune (3 sur 3).
- **Écart localisé : la définition de « mort »**. Ma première lecture, « mort » = `deadUrl` ou `deadFrom`, donnait 400 protocoles, 92 960 M$ et 231 déclarés. Avec `deadFrom` seul, l'écart tombe à 0. Le code du lecteur fait ce choix (`traite.py` l.65), mais la pièce ne l'écrit nulle part (C-2).
- **Écart T2** : je reproduis exactement les valeurs de la pièce en reprenant la logique du lecteur (`g2/t2_variantes.py`, colonne `code_lecteur`). Deux défauts de code, absents de la règle écrite, expliquent l'écart (C-1) :
  - (a) `traite.py` l.25 retire les chaînes à TVL nulle (`and v`), et l.47 reprend la TVL totale quand la somme vaut 0 (`return m if m>0 else p['tvl']`). Résultat : Steakhouse Financial (2 529 M$) est compté en entier chez Chaos (chaîne `Corn`, TVL 0) et chez RedStone (chaîne `Unichain`, TVL 0) ; River Omni-CDP (107 M$) est compté en entier chez DIA (chaîne `BEVM`, TVL 0).
  - (b) l.135 (`if r['id'] in o['ids']: continue`) ne lit que la **première** entrée d'un oracle. Pour Venus Core Pool, l'entrée Chainlink `@Binance` (1 338 M$) est ignorée : seule la première, sur six petites chaînes (environ 4,5 M$), est lue. Pour River, eOracle `@bsc` n'est pas rapproché de `Binance`.
  - Avec la règle 2.3 appliquée telle qu'elle est écrite (`g2/t2_attendu.py`), RedStone passe du 2e au 4e rang, derrière Chronicle (11 856) et Internal (11 180), et Chaos du 6e au 9e. Le repli sur la TVL totale ne joue plus que pour deux lignes : RedStone, 1 256 M$ (Pendle V2, chaîne « Redstone » absente de ses TVL), et Pyth, 88 M$ (Usual USD0, Arbitrum absent).
- **Rejeu** : une copie de `raw/` et des scripts, exécutée hors réseau dans `g2/replay/` (supprimée ensuite), donne `traite.py`, `enrichit.py` et `assemble.py` en sortie 0. `CARTO-DEFI-ORACLES.md`, `out/tables.md`, `out/rows.json`, `out/perimetre.csv` et `out/cibles-actifs.json` sont **identiques à l'octet** (5 sur 5).
- **Variante neutre** : exclure en plus les clés de premier niveau `vesting`, `offers` et `treasury` du calcul de la chaîne principale donne une sortie identique (`g2/sortie-large.txt`).

## 3. Méthode (contrôle 3)

- **Catégories A** : la liste du texte (2.4) est identique à `CORE` (`traite.py` l.10-11). Appliquée telle quelle par mon script, elle redonne 345 protocoles. Son antériorité aux chiffres (« écrites avant de regarder les chiffres ») ne se contrôle pas sur pièce (I-5).
- **Seuils** : ce sont ceux que le brief suggérait (≥ 1 Md$ ; de 50 M$ à 1 Md$ ; de 1 à 50 M$). Ils sont appliqués tels quels et reproduits. Aucun protocole ne tombe sur une borne.
- **Exclusions** : CEX, Chain, Oracle, `rugged` et `deprecated` sont conformes. « Mort » n'est pas défini dans le texte ; le code retient `deadFrom` seul. 24 protocoles à `deadUrl: true` (adresse vidée) restent donc dans le périmètre, pour 353 M$ [calc] : RealT Tokens 155 M$, AZverse Perps 52 M$, Alpaca Leveraged Yield Farming 37 M$, RealT RMM 29 M$, Set Protocol, Rari Capital, etc. Aucun n'est dans la liste courte (C-2).
- **Dates d'oracle** : une `endDate` passée ou une `startDate` future est exclue. Aucune date n'est égale au jour de lecture, donc pas d'effet de bord. Quand toutes les entrées sont closes, il n'y a pas de repli sur l'ancien champ, ce qui est raisonnable. Cas contrôlés [lu] : USDD (WINkLink close au 2025-05-15, puis Chainlink), JustLend (Internal à partir du 2025-05-15), Rhea (Chainlink de repli clos au 2026-09-17), Benqi (Chaos clos au 2026-05-04), Lista (Atlas à partir du 2026-06-02).
- **Chaîne principale** : TVL maximale hors `borrowed`, `staking` et `pool2`. La règle est conforme et reproduite (voir la variante neutre ci-dessus).
- **Biais déclarés** :
  - double comptage entre couches (curateurs au-dessus de Morpho) : déclaré ;
  - `misrepresentedTokens` non filtré : déclaré, sans chiffre (O-3) ;
  - non-additivité de T2 : déclarée.
- **Biais non déclarés ou sous-déclarés** :
  - le repli de T2, dit « léger », vaut 2,5 Md$ pour Chaos (C-1) ;
  - les 24 protocoles `deadUrl` (C-2) ;
  - les usages d'oracle sans lien avec un prix (C-3) ;
  - T4 compte des paires et non des combinaisons (C-4) ;
  - limite T1d présentée sans le dire (C-12).

## 4. Les 30 cibles (contrôle 4)

Règle de `cibles.json`, appliquée à chaque taille : périmètre A+B ; hors familles déjà étudiées et hors fournisseurs d'oracle ; un seul protocole par organisation (parent). On privilégie ensuite (1) au moins 2 oracles externes, (2) un incident d'oracle classé, (3) l'étalement sur les chaînes, avec au plus 2 à 3 cibles par chaîne principale.

| # | cible | taille | périmètre | parent DefiLlama | oracles externes | incidents d'oracle classés (id ou parent) | chaîne principale |
|---|---|---|---|---|---:|---:|---|
| 1 | Sky Lending | G (ok) | A | parent#maker | 1 | 0 | Ethereum |
| 2 | Lista Lending | G (ok) | A | parent#lista-dao | 4 | 0 | Binance |
| 3 | Jupiter Lend | G (ok) | A | parent#jupiter | 1 | 0 | Solana |
| 4 | Steakhouse Financial | G (ok) | B | (aucun) | 4 | 0 | Base |
| 5 | Gauntlet | G (ok) | B | (aucun) | 3 | 0 | Base |
| 6 | Maple | G (ok) | A | parent#maple-finance | 1 | 0 | Ethereum |
| 7 | USDD | G (ok) | A | (aucun) | 1 | 0 | Tron |
| 8 | Ethena USDe | G (ok) | A | parent#ethena | 0 | 0 | Ethereum |
| 9 | Pendle V2 | G (ok) | B | parent#pendle | 1 | 0 | Ethereum |
| 10 | JustLend V1 | G (ok) | A | parent#justlend | 0 | 0 | Tron |
| 11 | Dolomite | M (ok) | A | (aucun) | 4 | 0 | Ethereum |
| 12 | HyperLend Pooled | M (ok) | A | parent#hyperlend | 3 | 0 | Hyperliquid L1 |
| 13 | NAVI Lending | M (ok) | A | parent#navi-protocol | 2 | 0 | Sui |
| 14 | Rhea Lend | M (ok) | A | parent#rhea-finance | 3 | 1 | Near |
| 15 | Blend Pools V2 | M (ok) | A | parent#blend | 2 | 1 | Stellar |
| 16 | Save | M (ok) | A | parent#save-protocol | 2 | 1 | Solana |
| 17 | River Omni-CDP | M (ok) | B | parent#river-inc | 5 | 0 | Binance |
| 18 | GMX V2 Perps | M (ok) | A | parent#gmx | 1 | 0 | Arbitrum |
| 19 | Benqi Lending | M (ok) | A | parent#benqi | 1 | 0 | Avalanche |
| 20 | Usual USD0 | M (ok) | A | parent#usual | 2 | 0 | Ethereum |
| 21 | Echelon Market | P (ok) | A | (aucun) | 3 | 0 | Aptos |
| 22 | Scallop Lend | P (ok) | A | parent#scallop | 3 | 0 | Sui |
| 23 | Silo V2 | P (ok) | A | parent#silo-finance | 3 | 1 | Avalanche |
| 24 | Moonwell Lending | P (ok) | A | parent#moonwell | 1 | 3 | Base |
| 25 | EVAA Protocol | P (ok) | A | (aucun) | 3 | 0 | TON |
| 26 | Folks Finance Lending | P (ok) | A | parent#folks-finance | 2 | 0 | Algorand |
| 27 | Gearbox | P (ok) | A | (aucun) | 3 | 0 | Ethereum |
| 28 | HypurrFi Pooled | P (ok) | A | parent#hypurfi | 2 | 0 | Hyperliquid L1 |
| 29 | YeiLend | P (ok) | A | parent#yei-finance | 3 | 0 | Sei |
| 30 | Ostium | P (ok) | A | (aucun) | 2 | 0 | Arbitrum |

- **Conforme** :
  - les 30 sont dans le périmètre et dans leur taille ;
  - aucune n'appartient à une famille étudiée (parent, slug, nom) ;
  - **aucun parent en double** ; les parentés voisines sont tenues à l'écart, chacune avec sa raison : Jupiter Perps (`parent#jupiter`) est en réserve, Lista CDP, Folks Finance xChain et JustLend V2 ne sont pas retenus ;
  - les incidents des lignes Rhea, Blend, Save, Silo V2 et Moonwell sont exacts (date, technique, montant) au regard de `raw/hacks.json` [lu]. Seule réserve, sur la chaîne : l'incident Moonwell du 2025-11-04 touche Base et Optimism (C-9) ;
  - la réserve est exacte (Jupiter Perps 820 M$, Fluid 714 M$, Bonzo Lend avec son incident du 2026-07-11 à 9,05 M$, Neverland 8,4 M$), sauf Angle (C-11) ;
  - les superlatifs se vérifient : « plus grosse CDP » (Sky, 5 919 M$, devant USDD), « plus gros prêt de Tron » (JustLend V1), « aucun protocole ≥ 50 M$ sur Aptos » [calc].
- **Préférences** : en G, 3 cibles sur 10 ont au moins 2 oracles externes ; c'est le maximum possible, car les 7 grands à 2 oracles externes ou plus comprennent 4 familles étudiées. En M, 8 sur 10 : GMX et Benqi sont motivés par le panier S2-bis et par la couverture d'Avalanche. En P, 9 sur 10, et Moonwell y entre par ses 3 incidents.
- **Écarts non motivés** :
  - en G, 4 cibles sur Ethereum (Sky, Maple, Ethena, Pendle) alors que le plafond écrit est de 2 à 3 par chaîne principale (C-6) ;
  - Sky Lending est conforme au sens DefiLlama (`parent#maker` ≠ `parent#spark`), mais P1 traite SparkLend comme un produit de Sky et vise « Spark/Sky » comme premier acheteur (C-7).

## 5. Affirmations, niveaux, vocabulaire, citations (contrôle 5)

- **Affirmations hors DefiLlama** :
  - « Tron est absent des deux notes de contexte (P1, SYNTHESE) » est exact : une recherche par mot entier, casse ignorée, ne trouve rien dans les deux fichiers [lu] ;
  - « Ex-Solend », « ex-Maker », « prêt institutionnel » (Maple), « réserves crypto » (USDD), « FX, métaux, énergie » (Ostium) et « même parent que Folks Finance xChain (6,7 M$, Chainlink seul) » se lisent dans les champs `previousNames`, `description` et `parentProtocol` de `raw/protocols.json` [lu]. Ces affirmations sont en réalité [lu] alors que la colonne « Pourquoi » les range par défaut en [inféré], ce qui est sans conséquence ;
  - **inexact** : Gauntlet n'est pas « cité dans SYNTHESE-CROISEMENT parmi les cabinets de risque » (C-8).
- **Défaillances de protocoles nommés** : Rhea, Blend, Save, Silo V2, Moonwell et Bonzo sont attribuées à DefiLlama, avec mention du champ source vide. **Deux ne sont pas attribuées** : Ostium (clé privée) et Scallop (récompenses). Moonwell met trois incidents à côté de son seul oracle déclaré (Chainlink) sans la réserve écrite pour Rhea (C-9).
- **Registre 09** (`docs/09-vocabulaire.md`, `001b9606…2f9`, lu en entier) : trois formulations sont visées (C-10). Les emplois de « vérifié » sont des négations ou des actes (« non vérifié », « vérifier par la documentation »), donc licites.
- **Citations** : aucun « » dans la pièce. Les citations web sont entre “ ” : “No authentication required” (`raw/api-docs.html`, l.56 du texte rendu [lu]) et “Upgrade to the paid API plan” (`raw/oracles.json` [lu]).
- **Affirmations de 2.1 sur la documentation** : `/api/oracles` et `/api/hacks` figurent bien dans “Pro-Only API Endpoints” de `raw/api-docs.html` [lu].

## 6. Sondages réseau (3 requêtes sur les 5 permises, 2026-10-04 à 20:46 UTC, `https://api.llama.fi`)

| requête | HTTP | octets | constat |
|---|---:|---:|---|
| `GET /oracles` | 402 | 66 | sha256 `77af6ecf…2a`, **identique** à `raw/oracles.json` |
| `GET /hacks` | 200 | 352 054 | sha256 `1b329996…6b42`, **identique** à `raw/hacks.json`, servi sans clé, ce qui confirme l'écart avec la doc signalé en 2.1 |
| `GET /protocols` | 200 | 9 070 787 | réponse vivante (sha256 `a3c3d7c9…be1f`). Mêmes 8 483 identifiants que `raw/protocols.json`, `oraclesBreakdown` **identique pour tous**, seules 3 463 TVL ont bougé. Les cas Steakhouse (`Corn` et `Unichain`) et Venus (deux entrées Chainlink) sont toujours présents. Réponse gardée en `g2/sonde-protocols.out.gz` |

## 7. Corrections exigées (liste fermée)

**C-1 — T2, colonne « Valeur déclarée » ; §1 puce 4 ; §2.3 ; §7.5.**
- Recalculer selon la règle écrite en 2.3 :
  - prendre toutes les entrées d'un même oracle ;
  - comparer les chaînes sans tenir compte de la casse, avec l'alias `bsc` → `Binance` ;
  - une chaîne présente avec une TVL nulle compte pour 0 ;
  - reprendre la TVL totale **seulement** quand aucune chaîne ne correspond, et montrer cette part à part.
- Valeurs attendues [calc, `g2/sortie-t2-attendu.txt`] : Chainlink 46 060 ; Chronicle 11 856 ; Internal 11 180 ; RedStone 11 084, dont 1 256 de repli ; Pyth 5 947, dont 88 de repli ; Atlas 2 576 ; Switchboard 1 483 ; Binance Oracle 1 133 ; Chaos 828 ; eOracle 241 ; DIA 117. Les autres lignes ne changent pas.
- §1 : « 44,7 Md$ » devient « 46,1 Md$ ».
- §2.3 : « léger surcomptage possible » devient le montant du repli : RedStone 1 256 M$ (Pendle V2, chaîne « Redstone ») et Pyth 88 M$ (Usual USD0, Arbitrum).
- §7.5 : « bornes hautes » ne vaut que pour ces deux lignes ; Chainlink était sous-évalué.

**C-2 — Définition de « mort » (§1 « ni mort » ; §2.4 ; T0).** Écrire « mort = champ `deadFrom` renseigné ». Déclarer en plus que 24 protocoles à `deadUrl: true` restent dans le périmètre (353 M$ ; 20 en A et 4 en B ; 15 avec un oracle déclaré ; aucun parmi les cibles). Autre possibilité : les exclure et recompter, ce qui donne A+B 400, 92 960 M$, 231 déclarés et 67 667 M$ [calc].

**C-3 — Usages d'oracle sans lien avec un prix (§1 puce 1 ; §2.3 ; §2.4 ; §7).**
- Cas typés par DefiLlama [lu] :
  - Re (RWA, 398 M$) : son seul oracle est Chainlink de type `PoR`. Il est compté « avec oracle déclaré » et chez Chainlink comme « seul oracle » ;
  - PoolTogether V5 (2,4 M$) : son seul oracle est Witnet de type `RNG`, et c'est la seule raison de son entrée en B.
- Cas sans type, d'après mon raisonnement [inféré] : Polymarket International (UMA, 368 M$) et Across (UMA, 21 M$) résolvent des événements ou des relais, pas un prix. PoolTogether V3 (Chainlink) sert à un tirage au sort.
- À faire : déclarer ces cas, ou retirer `RNG` et `PoR` du compte. Le retrait donne B 78, A+B 423, 244 déclarés (67 349 M$), Chainlink 128 protocoles, et supprime la ligne Witnet [calc, `g2/sortie-sans-RNG-PoR.txt`].
- §1 : « 424 protocoles dépendent d'un prix » devient « dépendent d'un prix ou déclarent un oracle ».

**C-4 — T4 et §1 puce 3.** T4 compte des **paires co-déclarées**, non additives, et non des combinaisons. Chainlink et RedStone sont déclarés ensemble par 28 protocoles, mais **exactement** ces deux-là par 8 (185 M$) ; Chainlink et Pyth par 17, et exactement ces deux-là par 9 [calc]. Corriger le titre et la phrase de §1.

**C-5 — §5, puce 2.** « Les grands multi-oracles sont les curateurs (Steakhouse, Gauntlet) et Lista » n'est vrai que hors familles déjà étudiées. Sur les 7 grands à au moins 2 oracles externes, 4 sont SparkLend, Compound V3, Venus Core Pool et Kamino Lend [calc]. Le dire et les nommer.

**C-6 — Liste courte G : 4 cibles sur Ethereum** (Sky, Maple, Ethena, Pendle), alors que `cibles.json` fixe « max 2-3 par chaîne principale » pour chaque taille. Le vivier G hors familles étudiées compte 13 protocoles, dont 7 hors Ethereum ; 6 sont retenus. Le 7e est Jito Liquid Staking (Solana, 1 269 M$, Switchboard seul, catégorie B). Il faut soit motiver l'écart dans la pièce, soit remplacer une cible Ethereum.

**C-7 — Sky Lending (n° 1 et §1 puce 5).** P1 écrit « SparkLend (Sky) » (l.42) et demande s'il faut « viser d'abord **Spark/Sky** » (l.117) ; SYNTHESE l.322 reprend « **Spark/Sky** » [lu]. Il faut dire dans la ligne et en §1 que l'acheteur, la gouvernance de Sky, est celui que P1 vise déjà : la cible n'est pas une organisation nouvelle. Autre possibilité : la remplacer, par exemple par Sentora Curator, Falcon Finance ou Jito.

**C-8 — Gauntlet (n° 5).** « Cité dans SYNTHESE-CROISEMENT parmi les cabinets de risque » est inexact. SYNTHESE cite Gauntlet comme **comparable de prix** (§1.10, l.359 : « Gauntlet : 1,6-2 M$/an (P1, citant doc 07) » ; l.463, C20). Les cabinets qu'elle nomme sont Chaos Labs et LlamaRisk (l.322) [lu]. Corriger la citation.

**C-9 — Incidents (n° 18, 22, 24, 30 ; n° 13 et 20).**
- Ostium : écrire « classé par DefiLlama “Private Key Compromised”, 23,75 M$, 2026-07-15, source vide [lu] ».
- Scallop : écrire « classé par DefiLlama “Reward Logic Flaw”, 0,142 M$, 2026-04-26, source vide [lu] ».
- Moonwell : ajouter la réserve de la ligne Rhea (« cela ne dit pas que l'oracle déclaré a failli »). L'incident du 2025-11-04 touche Base **et** Optimism.
- Par cohérence avec « à connaître avant tout contact » (Ostium), citer aussi les incidents non oracle liés par identifiant ou par parent :
  - GMX, par son parent GMX V1 : réentrance de 42 M$ le 2025-07-09 ; “Stale Price Arbitrage” de 0,565 M$ le 2022-09-18, classé Market Manipulation ;
  - NAVI, par son parent Volo Vault : clé privée compromise, 3,5 M$, le 2026-04-21 ;
  - Usual USD0 : entrée non validée, 0,043 M$, le 2025-05-27 [lu, `raw/hacks.json`].

**C-10 — Registre 09.**
- l.246, JustLend : « second avis indépendant ». « Indépendant » est interdit (registre l.21).
- l.259, GMX : « argument de vérification externe ». C'est évaluer la valeur d'une source (registre l.24 et l.30 : « nous mesurons une relation entre sources, pas la valeur de l'une »).
- l.258, River : « la plus forte diversité du périmètre ». C'est une diversité déclarée prise pour mesurée (registre l.20), et c'est inexact : 5 oracles sont aussi déclarés par Re7 Labs (94 M$) et ZeroLend Lending (1,4 M$) [calc].
- Formulations proposées :
  - « mesurer les racines communes entre l'oracle déclaré et d'autres sources » ;
  - « cinq fournisseurs déclarés, le nombre le plus élevé du périmètre, à égalité avec Re7 Labs et ZeroLend Lending (déclaré, non mesuré) ».

**C-11 — Paniers et chiffres de ligne** [calc, `g2/cibles_g2.py`].
- Ethena : « 99 % USDe » devient USDe 97,3 %, USDtb 1,4 %, USDC 1,3 %.
- Benqi : « BTC.b 5 % » devient « BTC 5,5 %, dont BTC.b 3,7 % et WBTC.e 1,9 % ».
- JustLend, tableau : « BTC 14 » devient 15 (14,53 %). C'est un double arrondi : `enrichit.py` arrondit au dixième, puis `assemble.py` arrondit à l'unité.
- Gearbox, texte : « USDC 5 % » devient 4 % (4,47 %).
- §7.8 : nommer les symboles non classés qui changent la lecture :
  - Gearbox : `SAVETH` (37,7 %) et `WMOOCURVEETH+-WETH` (16,2 %) ne sont pas comptés en ETH, alors que la ligne dit ETH 20 % ;
  - `AVALANCHEUSDC` n'est pas compté en USDC (GMX : 43 % au lieu de 41 % ; Benqi : 3 % au lieu de 0 %).
- Réserve : Angle n'a pas « quatre fournisseurs » mais trois fournisseurs externes (Chainlink, RedStone, Pyth) et un TWAP, dans l'ancien champ.

**C-12 — Libellés des tableaux.**
- « Par catégorie du périmètre A » devient « … du périmètre A+B (catégories B marquées (B)) ».
- T1d : écrire « 15 premières des 67 chaînes (52 des 136 protocoles) » [calc].
- Colonne « Chaînes (M$) » des cibles : elle est coupée à 70 caractères au milieu d'un nom (« Arb », « Hyperliq », « Solana 8, »). Donner la liste entière, ou marquer la coupure par « … ».

**C-13 — Section 8 et en-tête (versement).**
- Remplacer le chemin `/tmp/claude-0/…`, qui disparaîtra, par les fichiers versés. Déclarer `raw/` hors dépôt, empreintes seules, comme le fait P1.
- Corriger l'ordre de rejeu. `fetch_detail.sh` lit `out/rows.json`, que produit `traite.py`. L'ordre est donc : traite, fetch_detail, gzip -n, enrichit, assemble. Signaler aussi que la compression n'est pas scriptée et que `enrichit.py` lit un `.json.gz` ancien avant un `.json` frais.
- Citer `out/perimetre.csv` (424 lignes, sha256 `d452e2db…eec`), qui porte la liste « pour chacun » du point 4 du brief du lecteur et que la pièce ne cite jamais. Décider s'il est versé.
- Ajouter une ligne d'exposition comme celle de P1 : pièces du dépôt lues, dont P1 et SYNTHESE, et interdits non ouverts. C'est au lecteur de la fournir, ou au contrôle de transcription de l'orchestrateur.

## 8. Observations non bloquantes

- **O-1** : la pièce est en français sans accents ni apostrophes (« d un prix », « n est »), alors que P1 et SYNTHESE, dans le dossier de destination, sont accentués. C'est une question de lisibilité pour l'investisseur ; à rétablir au versement si l'orchestrateur le veut.
- **O-2** : §2.3 « 242 protocoles » (ancien champ) : 242 portent la clé, 238 la remplissent, et 233 servent de repli (5 ont aussi `oraclesBreakdown`). §2.5 « 7 101 entrées sous 1 M$ » : 1 284 n'ont pas de TVL et 5 817 ont une TVL inférieure à 1 M$ [calc].
- **O-3** : `misrepresentedTokens` concerne 38 protocoles du périmètre (2 533 M$), dont 2 cibles, Folks Finance Lending et Gearbox [calc]. On peut le signaler dans ces deux lignes.
- **O-4** : le cadrage « un seul oracle = dépendance unique ; plusieurs = question des racines communes, notre sujet » vient du brief du lecteur (point 4). P1 (§1, pt 4) place aussi le sujet **à l'intérieur** d'un seul oracle, puisque l'ensemble d'agrégateurs d'un feed Chainlink “remains unnamed” (citation de Chaos Labs). Cela touche la §5, puce 1 (« terrain étroit ») ; c'est à harmoniser par l'orchestrateur, pas une faute du lecteur.
- **O-5** : vivier M à au moins 2 oracles externes, ni retenu ni mis en réserve : K3 Capital (496 M$, Monad), EtherFi Borrowing Market (305 M$, Chaos et Pyth), KPK (235 M$), Enzyme (100 M$), Re7 Labs (94 M$, 5 oracles), Zest V2 (75 M$, Stacks). Le choix à la main est permis par la règle ; ces noms pourraient aller en réserve.
- **O-6** : incidents d'oracle classés en petite taille et non retenus : KiloEx (Chainlink et Pyth, 7,5 M$), Moola Market (8,4 M$), Makina (4,2 M$). Pour Dolomite (2024-03-20, contrôle d'accès, 1,8 M$) et Silo Finance (2025-06-25), un incident n'est rapproché **que par le nom**, hors de la règle de liaison déclarée [calc].
- **O-7** : la pièce dit « valeur sécurisée » en §2.5 et « valeur déclarée » en T2 ; il faudrait unifier. Ses tableaux recalculés relèvent du niveau [calc] de la convention de l'ADR-0029 (l.12).
- **O-8** : la docstring de `traite.py` annonce un `out/shortlist.json` que le script ne produit pas.

## 9. Prête à verser ? (contrôle 6)

**Non en l'état ; oui après C-1 à C-13.** Seule C-1 demande un recalcul : T2, plus une phrase en §1, une en §2.3 et une en §7.5. Si l'orchestrateur exclut les types `RNG` et `PoR`, C-3 en demande un autre, limité à quelques comptes (T0 et la ligne Chainlink). Toutes les autres corrections sont des retouches de texte. Destination prévue : `docs/adr-0029/etude-marche/`, comme pièce de contexte commercial non normative. Fichiers à verser selon C-13 : la pièce, ses scripts, `cibles.json`, `pourquoi.json`, `SHA256SUMS` et, au choix de l'orchestrateur, `out/perimetre.csv`. `raw/` reste hors dépôt avec ses empreintes.

## 10. Journal de provenance (G1)

**Sources lues** :
- [lu] la pièce et son dossier : `CARTO-DEFI-ORACLES.md` en entier ; `BRIEF-CARTO-DEFI.md` ; `traite.py`, `enrichit.py`, `assemble.py` et `fetch_detail.sh` en entier, **après** l'écriture de `recalcul_g2.py` ; `cibles.json` ; `pourquoi.json` (30 entrées) ; `out/cibles-actifs.json`. `out/perimetre.csv` est lu par script (424 lignes, même ensemble de noms que mon périmètre).
- [lu] les données brutes, par mes scripts : `raw/protocols.json`, `raw/hacks.json`, `raw/oracles.json`, `raw/api-docs.html` (texte rendu, 85 lignes), `raw/llms-free.txt` (en-tête et recherches), `raw/detail/*.json.gz` (30 fichiers). `raw/lite_protocols2.json` est contrôlé par empreinte seulement, car la pièce ne l'exploite pas.
- [lu] le dépôt :
  - `docs/09-vocabulaire.md`, en entier ;
  - `docs/adr-0029/etude-marche/SYNTHESE-CROISEMENT.md` (`69f9ddbb…ea9b`) : l.1-30 et l.340-372, plus les lignes trouvées par recherche ciblée (322, 325, 334, 338, 359, 401, 451, 463) ;
  - `docs/adr-0029/etude-marche/P1-DEFI-PRET.md` (`b4161c52…d4`) : l.1-16 et les lignes trouvées (17, 33, 41-43, 48, 50, 117) ;
  - `docs/adr-0029/ADR-0029-campagne-S2-bis.md` : lignes trouvées (3, 6, 9, 12, 49) et titres ;
  - `docs/adr-0028/ANNEXE-D-preenregistrement.md` : titres et l.32-47, c'est-à-dire **la liste D.2 seule**, sans ouvrir aucune des pièces qu'elle nomme ;
  - `enforcement/lint-model-pinning.sh` l.1-60, pour sa portée ;
  - `CLAUDE.md`.

**Commandes et sorties** (toutes depuis `g2/` ou le dossier du lecteur) :
- `sha256sum -c SHA256SUMS` : 48 OK, sortie 0, en début et en fin de relecture.
- `python3 -B recalcul_g2.py` (variante par défaut, `sortie-defaut.txt`) : 400 / 92 960. Avec `--variant=mort=deadFrom` (`sortie-deadFrom.txt`) : 424 / 93 313, 246, 170 / 76, 73. Avec `--variant=mort=deadFrom --variant=suffixes=large` (`sortie-large.txt`) : sortie identique. Avec `--variant=mort=deadFrom --variant=types_non_prix=exclure` (`sortie-sans-RNG-PoR.txt`) : 423, 244, Chainlink 128.
- `python3 -B compare_tables.py` : « 244 comparées ; 244 identiques ; 0 écart ». Les trois mutations sont détectées, 3 sur 3.
- `python3 -B t2_variantes.py` : la logique du lecteur reproduit exactement les valeurs de la pièce ; écarts par protocole listés. `python3 -B t2_attendu.py` : valeurs de C-1.
- `python3 -B cibles_g2.py` (`sortie-cibles.txt`) : contrôle des 30 lignes (parent, oracles actifs, panier, incidents par identifiant, parent ou nom).
- Rejeu hors réseau dans une copie : trois sorties 0, cinq fichiers identiques à l'octet.
- `curl` vers `api.llama.fi` (3 requêtes) : voir §6.
- Contrôle des octets de mon regex (consigne sur les barres obliques inverses) : `od -c` montre deux `\W` à barre simple dans `cibles_g2.py`.

**Fichiers produits** dans `g2/`, empreintes dans `g2/SHA256SUMS-G2` (16 lignes, `sha256sum -c` : 16 OK) : `recalcul_g2.py`, `cibles_g2.py`, `t2_variantes.py`, `t2_attendu.py`, `compare_tables.py`, `g2-lignes.json`, `sortie-*.txt` (8 fichiers), `sonde-protocols.out.gz`, et ce rapport. Les sondes `/oracles` et `/hacks`, identiques à `raw/`, ont été retirées après comparaison par `cmp`.

**Attestation d'exposition** :
- Je n'ai ouvert ni `docs/15-*`, ni `docs/16-*`, ni `docs/pocket-report/`, ni `docs/rapports/`, ni `docs/adr-0025/`, ni `docs/adr-0028/monark-m009a/`, ni aucun `*.jsonl`, ni aucune pièce de la liste D.2.
- Je n'ai fait aucune recherche récursive sur `docs/` : seulement des `ls` non récursifs de `docs/adr-0028/`, `docs/adr-0029/` et `docs/adr-0029/etude-marche/`, et des recherches ciblées fichier par fichier.
- Une recherche `grep -rln` hors de `docs/` (`enforcement`, `scripts`, `xtask`, `justfile`), faite pour trouver une gate de citations, n'a affiché que des noms de fichiers ; je n'ai ouvert que `lint-model-pinning.sh`.
- Je n'ai vu ni calculé aucune donnée de campagne.
- Je n'ai fait aucune opération git en écriture (seulement `rev-parse` et `status`), aucune prise de contact, aucune dépendance nouvelle.

**Limites rencontrées, à former comme items (règle PAROXYSME)** :
- **I-1** : le sens des champs `deadUrl` et `deadFrom` n'est pas documenté dans les copies de doc lues [abs]. La définition de « mort » reste un choix.
- **I-2** : DefiLlama ne type l'usage d'un oracle (prix, aléa, réserve, résolution) que pour 9 entrées sur 1 201 (`RNG` 7, `PoR` 2) [lu]. La part de B qui dépend vraiment d'un prix n'est pas établie.
- **I-3** : les noms de chaînes des entrées d'oracle ne sont pas normalisés (`bsc`, `hemi`, `scroll` et `optimism` en minuscules ; « Redstone » est une chaîne homonyme de l'oracle), et aucune table d'alias n'est publiée [abs]. Tout plafonnement par chaîne dépend d'un alias écrit à la main.
- **I-4** : l'identité du jeton `SAVETH` (37,7 % de Gearbox, présent aussi chez Dolomite) n'est pas établie [abs] ; je ne l'ai pas cherchée, mon réseau étant limité à `api.llama.fi`.
- **I-5** : l'antériorité des catégories A et des seuils sur les chiffres ne se contrôle pas sur pièce : il n'existe aucun horodatage distinct de la liste.
