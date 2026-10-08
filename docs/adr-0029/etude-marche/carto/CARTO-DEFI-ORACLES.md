# CARTO-DEFI-ORACLES — protocoles DeFi qui dependent d oracles, toutes chaines, toutes tailles (source : DefiLlama)

Gate 0 : modele resolu `claude-sonnet-5-5`, effort high (lecteur `shogen-lecteur`), pour la passe initiale et pour la passe de corrections. Date de lecture des donnees : 2026-10-04 (horloge `date -u` : 18:30 a 18:35 UTC) ; passe de corrections G2 : 2026-10-04, `date -u` 21:02 a 21:11 UTC.
Brief : `BRIEF-CARTO-DEFI.md`, sha256 `bd8855d9763fa0f7b4c5560750f8dda6518339737149e4f1d64f7548c31f14bf` (recalcule, identique). Relecture G2 : `g2/G2-CARTO.md`, sha256 `c81e1e09dab00c00f5fadcfba4c89365bf6343e333354dc2180eee1b0c17e9f1` (verdict ACCEPTE-AVEC-CORRECTIONS, corrections C-1 a C-13) ; brief des corrections : `g2/BRIEF-CORRECTIONS-CARTO.md`, sha256 `f7cb7f75b0f5da4f363d60614eadaf0c88b511a64aa8bbc2a478be680c1fb300`. Cette version applique les corrections (section 9) ; la version precedente est gardee hors versement dans `v1/`.
Niveaux : [lu] = lu dans la reponse de l API DefiLlama du jour ou dans le depot ; [abs] = absent de la source ; [inféré] = ma deduction ; [calc] = calcul de mes scripts sur des [lu]. Aucune prise de contact ; aucune operation git ; aucun reseau pendant la passe de corrections.
Attestation d exposition : aucune piece de `docs/15-*`, `docs/16-*`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, aucun `*.jsonl`, aucune piece de la liste D.2 de l annexe D d ADR-0028 ouverte, aucun journal de campagne lu. Pieces du depot lues, en lecture seule, pour la passe de corrections : `docs/09-vocabulaire.md` (en entier, sha256 `001b960674e15cdf4d68301d3a79a65b78249dfa77999b6c47fa441e3e9f2831`) ; `docs/adr-0029/etude-marche/SYNTHESE-CROISEMENT.md` (sha256 `69f9ddbb78f374d82bd062909719e160f05e8e206753ef6bf097a738908eea9b`, lignes 322, 344, 359, 463 et titres) ; `docs/adr-0029/etude-marche/P1-DEFI-PRET.md` (sha256 `b4161c5291c62a754e9fea96e997af8880bea9b91aad2b4c26eac78569ecf7d4`, lignes 8, 42, 117) ; `docs/adr-0029/ADR-0029-campagne-S2-bis.md` (lignes 10 a 13 seulement) ; `CLAUDE.md`. Passe initiale : la piece cite P1 et SYNTHESE (recherche de mots, section 4, ligne USDD) ; le reste de son attestation n est pas reconstitue ici et reste a confirmer par le controle de transcription de l orchestrateur. Aucune ecriture hors du dossier de travail de la carte, aucune cle, aucun compte.

## 1. Resume

- DefiLlama liste **8483 protocoles**. Apres filtre (TVL >= 1 M$, ni CEX, ni chaine, ni mort : mort = champ `deadFrom` renseigne), **424** protocoles dependent d un prix ou declarent un oracle : 345 dans les categories ecrites d avance (A) et 79 dans d autres categories mais avec un oracle declare (B). Trois biais de perimetre sont declares en section 7 (points 11 a 13) : 24 protocoles `deadUrl` restes dans le perimetre, des usages d oracle sans lien avec un prix, des paires presentees comme des combinaisons.
- Seuls **246 sur 424 (58 %)** ont un oracle declare ; ils pesent 67,8 Md$ sur 93,3 Md$ (73 % de la TVL). Le champ est vide pour 42 % des protocoles, dont des geants (Ethena USDe, 4,9 Md$ ; Falcon Finance ; Morpho Blue — deja etudie).
- Parmi les 246 : **170 n ont qu un oracle declare** (dependance unique), **76 en ont deux ou plus** (question des racines communes). Paires d oracles co-declarees les plus frequentes (non additives : un protocole a trois oracles figure dans trois paires) : Chainlink et RedStone sont declares ensemble par 28 protocoles, dont 8 (185 M$) declarent exactement ces deux oracles ; Chainlink et Pyth par 17, dont 9 exactement ces deux (T4).
- Chainlink est declare par 129 protocoles (46,1 Md$ de valeur declaree, regle de la section 2.3 ; la version precedente de la piece donnait 44,7 Md$ par erreur de code, section 9), Pyth par 66, RedStone par 51.
- Liste courte de 30 cibles plus bas : 10 grandes, 10 moyennes, 10 petites, sur 15 chaines principales ; les 7 familles deja etudiees (Aave, Spark, Morpho, Euler, Compound, Kamino, Venus) en sont exclues. Sky Lending, present dans la version precedente, est sorti de la liste : son acheteur, la gouvernance de Sky, est deja vise par P1 sous “Spark/Sky” (P1 l.117 ; SYNTHESE l.322) ; Jito Liquid Staking (Solana) entre a sa place.
- Limite majeure : ce que DefiLlama declare n'est pas verifie (section 7) ; le point d acces officiel par oracle (`/oracles`) est reserve a l offre payante : les tableaux par oracle sont **recalcules par moi** a partir des champs des protocoles.

## 2. Methode (rejouable)

1. [lu] Documentation lue : `https://api-docs.defillama.com/` (copie `raw/api-docs.html`) et `llms-free.txt`. Elle annonce l API gratuite `https://api.llama.fi` “No authentication required” et classe `/api/oracles` et `/api/hacks` dans la liste Pro. Constat du jour : `GET /oracles` repond **402** (“Upgrade to the paid API plan”) ; `GET /hacks` repond 200 sans cle (ecart avec la doc, signale).
2. Reponses brutes gardees (sha256 en section 8) : `/protocols` (9,07 Mo, 8483 entrees), `/lite/protocols2` (gardee, non exploitee), `/oracles` (le refus 402), `/hacks` (1 293 incidents), et `/protocol/{slug}` pour les 30 cibles (composition des actifs ; compresses en .gz).
3. Source des oracles : champ `oraclesBreakdown` (971 protocoles ; nom, role Primary/Secondary/Aggregator/Fallback, preuve, dates, chaines), sinon ancien champ `oracles` (242 protocoles, sans role : marque “champ ancien”). Un oracle dont `endDate` est passee ou `startDate` future n est pas compte. Si DefiLlama liste des chaines pour un oracle, la valeur de cet oracle est limitee a ces chaines, selon la regle suivante : toutes les entrees d un meme oracle pour un protocole sont reunies ; les noms de chaines sont compares sans tenir compte de la casse, avec l alias “bsc” = BNB Chain (ecrit a la main : DefiLlama ne publie pas de table d alias [abs]) ; une chaine presente avec une TVL nulle compte pour 0 ; la TVL totale du protocole n est reprise que si aucune chaine citee ne correspond a une chaine du protocole, et cette part est montree a part dans T2 : RedStone 1 256 M$ (Pendle V2, chaine citee “Redstone”, absente de ses TVL) et Pyth 88 M$ (Usual USD0, chaine citee “Arbitrum”, absente de ses TVL).
4. **Categories dependantes d un prix (A, ecrites avant de regarder les chiffres)** : Lending, CDP, Derivatives, Options, Options Vault, RWA, Leveraged Farming, Synthetics, Basis Trading, Algo-Stables, Partially Algorithmic Stablecoin, Dual-Token Stablecoin, Stablecoin Issuer, NFT Lending. **B** : toute autre categorie (curateurs, rendement, jeux d options, indices, staking liquide, marches de prediction...) des qu un oracle est declare. Exclus : CEX, Chain, Oracle (fournisseurs, pas clients), protocoles marques rugged, deprecated ou morts. **Mort = champ `deadFrom` renseigne**, ecrit tel quel dans les donnees de DefiLlama ; le champ `deadUrl` n est pas utilise, et 24 protocoles `deadUrl: true` restent dans le perimetre (declares en section 7, point 11).
5. **Tailles (seuils ecrits d avance, valeur deposee = champ `tvl` de DefiLlama, qui exclut les emprunts)** : Grande >= 1 Md$ ; Moyenne 50 M$ a 1 Md$ ; Petite 1 a 50 M$. Pourquoi : 1 Md$ isole la vingtaine de protocoles systemiques ; 50 M$ separe, a mon avis [inféré], ceux qui ont une equipe de risque dediee des petits ; sous 1 M$ la valeur securisee est trop faible pour un contrat (7 101 entrees de la liste sont sous 1 M$).
6. **Chaine principale** = chaine ou le protocole a le plus de TVL (champ `chainTvls`, hors `borrowed`, `staking`, `pool2`). “BNB Chain” = cle `Binance` ; “Hyperliquid” = cle `Hyperliquid L1` ([inféré] : c est la couche EVM). Hors des dix chaines demandees : “Autres” (detail T1d).
7. Liste courte : regle dans `cibles.json` (hors familles deja etudiees, un protocole par organisation, au moins deux oracles externes de preference, incident d oracle classe, etalement des chaines) ; choix final a la main. La composition des actifs vient de `/protocol/{slug}` (derniere ligne `tokensInUsd`, 2026-10-04) ; le regroupement BTC / ETH / USDC / USDT est fait **par symbole** [inféré] (BTC = tout symbole contenant BTC ; ETH = ETH et derives liquides courants).

## 3. Tableaux de synthese

### T0. Perimetre et couverture de la declaration des oracles

| Perimetre (TVL >= 1 M$, hors rugged/deprecated/mort = champ `deadFrom` renseigne) | Protocoles | TVL (M$) | avec oracle declare | % protocoles | TVL declaree (M$) | % TVL |
|---|---:|---:|---:|---:|---:|---:|
| A. categories dependantes d un prix (liste ecrite d avance) | 345 | 79 292 | 167 | 48 % | 53 729 | 68 % |
| B. autres categories avec oracle declare | 79 | 14 021 | 79 | 100 % | 14 021 | 100 % |
| A+B | 424 | 93 313 | 246 | 58 % | 67 750 | 73 % |

Par categorie du perimetre A+B (protocoles >= 1 M$ ; categories B marquees (B)) :

| Categorie | Protocoles | TVL (M$) | oracle declare (nb) | TVL declaree (M$) |
|---|---:|---:|---:|---:|
| Lending | 133 | 55 335 | 92 | 42 699 |
| Risk Curators (B) | 18 | 8 420 | 18 | 8 420 |
| CDP | 40 | 8 139 | 20 | 7 630 |
| Basis Trading | 29 | 7 987 | 0 | 0 |
| RWA | 59 | 4 682 | 12 | 1 474 |
| Derivatives | 53 | 2 191 | 27 | 1 369 |
| Liquid Staking (B) | 4 | 2 048 | 4 | 2 048 |
| Yield (B) | 10 | 1 410 | 10 | 1 410 |
| Yield Aggregator (B) | 8 | 464 | 8 | 464 |
| Prediction Market (B) | 4 | 374 | 4 | 374 |
| Leveraged Farming | 6 | 312 | 2 | 40 |
| Onchain Capital Allocator (B) | 7 | 249 | 7 | 249 |
| Crypto Card Issuer (B) | 1 | 247 | 1 | 247 |
| Dual-Token Stablecoin | 5 | 233 | 3 | 184 |
| Indexes (B) | 3 | 227 | 3 | 227 |
| Stablecoin Issuer | 1 | 200 | 1 | 200 |
| Liquid Restaking (B) | 4 | 136 | 4 | 136 |
| Insurance (B) | 1 | 115 | 1 | 115 |
| CeDeFi (B) | 1 | 107 | 1 | 107 |
| Liquidity Manager (B) | 3 | 94 | 3 | 94 |
| Synthetics | 5 | 74 | 2 | 19 |
| Algo-Stables | 2 | 54 | 2 | 54 |
| Options Vault | 3 | 49 | 3 | 49 |
| Dexs (B) | 5 | 36 | 5 | 36 |
| Options | 5 | 23 | 2 | 10 |
| AI Agents (B) | 1 | 22 | 1 | 22 |
| Cross Chain Bridge (B) | 1 | 21 | 1 | 21 |
| Bridge (B) | 2 | 21 | 2 | 21 |
| Launchpad (B) | 1 | 14 | 1 | 14 |
| NFT Lending | 2 | 11 | 0 | 0 |
| Interest Rate Derivatives (B) | 1 | 8 | 1 | 8 |
| Yield Lottery (B) | 2 | 7 | 2 | 7 |
| Partially Algorithmic Stablecoin | 2 | 3 | 1 | 1 |
| Liquidations (B) | 1 | 2 | 1 | 2 |
| Payments (B) | 1 | 1 | 1 | 1 |

### T1a. Chaine principale x taille — perimetre A+B (nombre de protocoles ; TVL en M$ entre parentheses)

| Chaine principale | Grande | Moyenne | Petite | Total |
|---|---:|---:|---:|---:|
| Ethereum | 10 (55 975) | 39 (8 291) | 92 (1 038) | 141 (65 304) |
| Solana | 3 (3 984) | 8 (2 075) | 18 (229) | 29 (6 289) |
| Base | 2 (4 180) | 4 (560) | 19 (156) | 25 (4 897) |
| Arbitrum | 0 (0) | 3 (600) | 14 (104) | 17 (704) |
| BNB Chain | 2 (2 383) | 8 (928) | 23 (245) | 33 (3 556) |
| Sui | 0 (0) | 3 (423) | 8 (54) | 11 (477) |
| Aptos | 0 (0) | 0 (0) | 4 (43) | 4 (43) |
| Avalanche | 0 (0) | 2 (382) | 9 (57) | 11 (440) |
| Hyperliquid | 0 (0) | 2 (574) | 11 (182) | 13 (756) |
| Tron | 2 (5 175) | 1 (57) | 1 (2) | 4 (5 233) |
| Autres | 0 (0) | 25 (4 511) | 111 (1 104) | 136 (5 615) |
| **Total** | 19 (71 696) | 95 (18 402) | 310 (3 214) | 424 (93 313) |

### T1b. Idem, seulement protocoles avec oracle declare

| Chaine principale | Grande | Moyenne | Petite | Total |
|---|---:|---:|---:|---:|
| Ethereum | 7 (38 080) | 24 (5 629) | 51 (650) | 82 (44 359) |
| Solana | 3 (3 984) | 6 (1 448) | 10 (100) | 19 (5 532) |
| Base | 2 (4 180) | 2 (311) | 9 (97) | 13 (4 588) |
| Arbitrum | 0 (0) | 2 (548) | 7 (39) | 9 (587) |
| BNB Chain | 2 (2 383) | 2 (195) | 11 (111) | 15 (2 690) |
| Sui | 0 (0) | 3 (423) | 6 (40) | 9 (462) |
| Aptos | 0 (0) | 0 (0) | 2 (12) | 2 (12) |
| Avalanche | 0 (0) | 1 (130) | 7 (47) | 8 (177) |
| Hyperliquid | 0 (0) | 1 (393) | 7 (155) | 8 (547) |
| Tron | 2 (5 175) | 1 (57) | 1 (2) | 4 (5 233) |
| Autres | 0 (0) | 15 (2 940) | 62 (621) | 77 (3 561) |
| **Total** | 16 (53 802) | 57 (12 074) | 173 (1 874) | 246 (67 750) |

### T1c. Presence par chaine (TVL posee sur la chaine, tous protocoles A+B ; un protocole multi-chaines compte sur chacune)

| Chaine | Protocoles presents (>= 1 M$ sur la chaine) | TVL sur la chaine (M$) | dont avec oracle declare (M$) |
|---|---:|---:|---:|
| Ethereum | 167 | 55 521 | 40 346 |
| Solana | 39 | 6 655 | 5 983 |
| Base | 43 | 7 388 | 2 636 |
| Arbitrum | 40 | 1 718 | 1 557 |
| BNB Chain | 44 | 4 142 | 3 438 |
| Sui | 12 | 480 | 462 |
| Aptos | 5 | 49 | 12 |
| Avalanche | 21 | 785 | 586 |
| Hyperliquid | 23 | 1 009 | 576 |
| Tron | 4 | 5 182 | 5 182 |
| Autres | 241 | 10 401 | 6 973 |

### T1d. Detail de la ligne Autres (chaine principale, A+B) : 15 premieres des 67 chaines (52 des 136 protocoles de la ligne Autres)

| Chaine | Protocoles | TVL (M$) |
|---|---:|---:|
| Monad | 13 | 1 470 |
| Optimism | 4 | 556 |
| Polygon | 4 | 421 |
| Provenance | 1 | 242 |
| Plume Mainnet | 2 | 235 |
| Plasma | 3 | 213 |
| Stellar | 3 | 203 |
| Near | 1 | 196 |
| xDai | 2 | 184 |
| Algorand | 4 | 175 |
| Robinhood Chain | 4 | 155 |
| Starknet | 3 | 138 |
| Ink | 1 | 138 |
| Bitcoin | 6 | 136 |
| Pharos | 1 | 134 |

### T2. Par oracle declare (perimetre A+B, TVL >= 1 M$ ; valeur = somme des TVL des protocoles qui le declarent, limitee aux chaines indiquees quand DefiLlama les donne ; un protocole a plusieurs oracles est compte pour chacun : NE PAS additionner les lignes)

| Oracle | Protocoles | Valeur declaree (M$) | dont repli sur la TVL totale (M$) | Seul oracle | Un parmi plusieurs | Grandes | Moyennes | Petites | Chaines principales (top 3) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Chainlink | 129 | 46 060 | 0 | 78 | 51 | 11 | 34 | 84 | Ethereum 61, Autres 21, Base 12 |
| Chronicle | 10 | 11 856 | 0 | 3 | 7 | 4 | 5 | 1 | Ethereum 6, Base 2, Autres 2 |
| Internal | 12 | 11 180 | 0 | 9 | 3 | 2 | 3 | 7 | Autres 5, Ethereum 3, Tron 2 |
| RedStone | 51 | 11 084 | 1 256 | 16 | 35 | 7 | 12 | 32 | Ethereum 19, Autres 17, Hyperliquid 6 |
| Pyth | 66 | 5 947 | 88 | 30 | 36 | 2 | 13 | 51 | Autres 26, Solana 14, Sui 9 |
| Atlas | 4 | 2 576 | 0 | 0 | 4 | 2 | 2 | 0 | BNB Chain 2, Autres 2 |
| Switchboard | 10 | 1 483 | 0 | 4 | 6 | 1 | 2 | 7 | Solana 6, Sui 2, Aptos 1 |
| Binance Oracle | 4 | 1 133 | 0 | 0 | 4 | 1 | 1 | 2 | BNB Chain 4 |
| Chaos | 5 | 828 | 0 | 0 | 5 | 1 | 3 | 1 | Autres 2, Base 1, Solana 1 |
| UMA | 3 | 391 | 0 | 3 | 0 | 0 | 1 | 2 | Ethereum 2, Autres 1 |
| Stork | 16 | 303 | 0 | 7 | 9 | 0 | 2 | 14 | Autres 10, Ethereum 2, Hyperliquid 1 |
| eOracle | 16 | 241 | 0 | 4 | 12 | 0 | 4 | 12 | Autres 9, Ethereum 5, BNB Chain 1 |
| Supra | 5 | 228 | 0 | 0 | 5 | 0 | 1 | 4 | Sui 4, Autres 1 |
| OutLayer | 1 | 196 | 0 | 0 | 1 | 0 | 1 | 0 | Autres 1 |
| Reflector | 1 | 164 | 0 | 0 | 1 | 0 | 1 | 0 | Autres 1 |
| DIA | 7 | 117 | 0 | 3 | 4 | 0 | 2 | 5 | Autres 3, Ethereum 3, BNB Chain 1 |
| Api3 | 10 | 108 | 0 | 2 | 8 | 1 | 2 | 7 | Autres 5, Ethereum 3, BNB Chain 2 |
| TWAP | 5 | 97 | 0 | 2 | 3 | 0 | 0 | 5 | Autres 3, BNB Chain 1, Ethereum 1 |
| Curve | 1 | 42 | 0 | 1 | 0 | 0 | 0 | 1 | Autres 1 |
| Pragma | 2 | 19 | 0 | 2 | 0 | 0 | 0 | 2 | Autres 2 |
| Acurast | 1 | 18 | 0 | 1 | 0 | 0 | 0 | 1 | Autres 1 |
| Band | 3 | 9 | 0 | 2 | 1 | 0 | 0 | 3 | Ethereum 1, Avalanche 1, BNB Chain 1 |
| COTI's Oracle | 1 | 6 | 0 | 1 | 0 | 0 | 0 | 1 | Autres 1 |
| Chainsight | 1 | 5 | 0 | 0 | 1 | 0 | 1 | 0 | Ethereum 1 |
| Oracles.Cash | 1 | 4 | 0 | 1 | 0 | 0 | 0 | 1 | Autres 1 |
| Witnet | 1 | 2 | 0 | 1 | 0 | 0 | 0 | 1 | Autres 1 |
| Coingecko | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | Autres 1 |
| cLabs | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | Autres 1 |

Repli sur la TVL totale (aucune chaine citee par DefiLlama ne correspond a une chaine de TVL du protocole), montre a part : RedStone 1 256 M$ (Pendle V2, chaine citee “Redstone”); Pyth 88 M$ (Usual USD0, chaine citee “Arbitrum”). Pour toutes les autres lignes la valeur est la somme des TVL des chaines correspondantes (casse ignoree, alias bsc = BNB Chain, chaine a TVL nulle = 0).

### T3. Nombre d oracles actifs declares par protocole (perimetre A+B declare)

| Nb d oracles | Protocoles | TVL (M$) |
|---|---:|---:|
| 1 | 170 | 42 097 |
| 2 | 42 | 8 970 |
| 3 | 25 | 12 460 |
| 4 | 6 | 4 021 |
| 5 | 3 | 202 |

Nb d oracles **externes** (hors TWAP, Internal, Uniswap, Curve, PulseX, LP-token, Coingecko, Coinmarketcap) :

| Nb externes | Protocoles | TVL (M$) |
|---|---:|---:|
| 0 | 12 | 5 106 |
| 1 | 161 | 42 963 |
| 2 | 42 | 3 264 |
| 3 | 23 | 12 195 |
| 4 | 5 | 4 019 |
| 5 | 3 | 202 |

### T4. Paires d oracles co-declarees les plus frequentes (NON additives ; ce ne sont pas des combinaisons : un protocole a trois oracles figure dans trois paires)

| Paire | Protocoles qui declarent les deux | TVL cumulee (M$) | dont protocoles qui declarent exactement ces deux oracles | TVL de ceux-la (M$) |
|---|---:|---:|---:|---:|
| Chainlink + RedStone | 28 | 15 730 | 8 | 185 |
| Chainlink + Pyth | 17 | 2 851 | 9 | 1 583 |
| Chainlink + eOracle | 9 | 275 | 0 | 0 |
| Pyth + RedStone | 8 | 425 | 1 | 6 |
| RedStone + eOracle | 8 | 274 | 0 | 0 |
| Api3 + RedStone | 7 | 1 749 | 0 | 0 |
| Chronicle + RedStone | 6 | 10 253 | 0 | 0 |
| Api3 + Chainlink | 6 | 1 737 | 0 | 0 |
| Pyth + Switchboard | 6 | 139 | 2 | 100 |
| Chainlink + Chronicle | 5 | 10 241 | 0 | 0 |
| Binance Oracle + Chainlink | 4 | 1 133 | 2 | 4 |
| Pyth + Supra | 4 | 223 | 2 | 193 |
| Pyth + Stork | 4 | 72 | 3 | 63 |
| Chainlink + Chaos | 3 | 3 357 | 1 | 8 |
| Atlas + Chainlink | 3 | 2 879 | 0 | 0 |

### T5. Fournisseurs listes par DefiLlama en categorie Oracle (TVL > 0 ; ce sont des fournisseurs, pas des clients)

| Nom | TVL (M$) | Chaines |
|---|---:|---|
| openOracle | 0 | Base |


Lecture : T1a et T1b comptent les protocoles par chaine principale (un protocole = une case) ; T1c compte la TVL posee sur chaque chaine (un protocole multi-chaines y figure plusieurs fois). **Les TVL ne s additionnent pas entre couches** : curateurs, agregateurs de rendement et protocoles de base deposent les uns chez les autres (par ex. Steakhouse et Gauntlet au-dessus de Morpho) ; les totaux surestiment donc la valeur reellement exposee [inféré].

## 4. Liste courte de 30 cibles

Colonnes : chaines = toutes les chaines a 1 M$ ou plus, liste entiere ; TVL en M$ ; oracles tels que declares par DefiLlama [lu] avec leur role et les chaines indiquees ; panier = part du BTC, ETH, USDC, USDT dans les actifs deposes, par symbole [inféré] ; incidents = classes “Oracle Manipulation” par DefiLlama dans `/hacks` (champ `source` vide pour tous : cause non verifiee). La colonne “Pourquoi” est mon interpretation [inféré] sauf mention [lu]/[abs].

### Grandes (>= 1 Md$)

| # | Protocole | Categorie | Chaines (M$, >= 1 M$) | TVL | Oracles declares (n) | Panier S2-bis | Incidents d oracle | Pourquoi |
|---|---|---|---|---:|---|---|---|---|
| 1 | Jito Liquid Staking | Liquid Staking | Solana 1269 | 1 269.0 | Switchboard (Secondary) (1) | BTC 0 / ETH 0 / USDC 0 / USDT 0 % | aucun classe | Solana, grande taille (1 269 M$), categorie Liquid Staking (B). Un seul oracle declare, Switchboard, en role Secondary et sans Primary declare [lu] : dependance unique a documenter. Entre a la place de Sky Lending (correction C-6/C-7) : c est le septieme du vivier des grands hors familles deja etudiees (13 protocoles, dont 7 hors Ethereum ; 6 de ces 7 etaient deja retenus) et il ramene Ethereum a 3 cibles G. Panier : SOL 100 % (aucun actif de S2-bis), detail `/protocol/jito-liquid-staking` telecharge par l orchestrateur le 2026-10-04 a 21:11 UTC, meme jour que les 29 autres lignes [lu]. Aucun incident, oracle ou autre, lie par identifiant ou par parent (parent#jito) dans `raw/hacks.json` [lu]. |
| 2 | Lista Lending | Lending | BNB Chain 1026, Ethereum 14 | 1 040.1 | Atlas (Primary); RedStone (Primary); Chainlink (Secondary); Binance Oracle (Secondary) (4) | BTC 25 / ETH 1 / USDC 0 / USDT 0 % | aucun classe | Quatre oracles declares (Atlas et RedStone en principal, Chainlink et Binance Oracle en secondaire) : cas d ecole de racines communes a mesurer. Surtout BNB Chain ; BTC (BTCB) a 25 % du panier. |
| 3 | Jupiter Lend | Lending | Solana 1318 | 1 318.1 | Pyth (Primary) (1) | BTC 2 / ETH 0 / USDC 5 / USDT 0 % | aucun classe | Un seul oracle declare (Pyth) : dependance unique sur Solana. Meme equipe que Jupiter Perps (820 M$, Chainlink + Chaos + Pyth, preuve donnee par DefiLlama) : un seul contact, deux produits. Peu de BTC/ETH/USDC dans le panier (JLP, JupSOL). |
| 4 | Steakhouse Financial | Risk Curators | Base 1120, Ethereum 747, Robinhood Chain 532, Solana 70, Monad 47, Arbitrum 7, Katana 6 | 2 529.1 | Chronicle (Primary) @Monad,Arbitrum; Chaos (Primary) @Corn; RedStone (Primary) @Unichain; Chainlink (Primary) @Katana,Ethereum,Base (4) | BTC 0 / ETH 4 / USDC 59 / USDT 7 % | aucun classe | Curateur de coffres : declare 4 fournisseurs (Chainlink, Chronicle, RedStone, Chaos) repartis par chaine. Il choisit sans doute des oracles pour des marches ([inféré]). Panier : 59 % USDC. TVL en partie deja comptee dans les protocoles de pret sous-jacents. |
| 5 | Gauntlet | Risk Curators | Base 614, BNB Chain 575, Ethereum 383, Morph 42, Stable 22, Solana 8, Hyperliquid 2, Arbitrum 2 | 1 650.7 | RedStone (Primary) @Unichain,Katana,Monad; Chainlink (Primary) @Polygon,Base,Ethereum; Chronicle (Primary) @Tempo (3) | BTC 1 / ETH 7 / USDC 51 / USDT 3 % | aucun classe | Curateur de risque (Chainlink, RedStone, Chronicle selon les chaines) : son metier est de juger le risque, dont celui des oracles. SYNTHESE-CROISEMENT cite Gauntlet comme comparable de prix (1,6-2 M$/an, §1.10 l.359 ; contradiction C20, l.463) ; les cabinets de risque qu elle nomme sont Chaos Labs et LlamaRisk (l.322) [lu] : client ou concurrent, a trancher. Panier 51 % USDC. TVL en partie double avec les protocoles sous-jacents. |
| 6 | Maple | Lending | Ethereum 3004 | 3 003.8 | Chainlink (Primary) (1) | BTC 0 / ETH 0 / USDC 80 / USDT 13 % | aucun classe | Pret institutionnel, un seul oracle declare (Chainlink). Panier : 80 % USDC, 13 % USDT (S2-bis). Le prix des garanties BTC/ETH n est pas visible dans ce panier : a demander ([inféré]). |
| 7 | USDD | CDP | Tron 1223, Ethereum 31, BNB Chain 18 | 1 271.9 | Chainlink (Primary) (1) | BTC 0 / ETH 0 / USDC 0 / USDT 7 % | aucun classe | Stablecoin adosse a des reserves crypto sur Tron, un seul oracle declare (Chainlink). Tron est absent des deux notes de contexte lues (P1, SYNTHESE) [lu par recherche de mots]. Panier surtout TRX, USDT 7 % : couverture S2-bis faible. |
| 8 | Ethena USDe | Basis Trading | Ethereum 4905 | 4 905.4 | **non renseigne [abs]** (0) | BTC 0 / ETH 0 / USDC 1 / USDT 0 % | aucun classe | 4,9 Md$, categorie Basis Trading, aucun oracle declare par DefiLlama ([abs]) : plus gros cas de dependance non documentee. Ses prix de reference BTC/ETH sont a documenter avec eux ([inféré]). Panier : USDe 97,3 %, USDtb 1,4 %, USDC 1,3 %. |
| 9 | Pendle V2 | Yield | Ethereum 742, Monad 205, Arbitrum 174, X Layer 71, Plasma 44, Hyperliquid 10, BNB Chain 8, Base 3 | 1 256.4 | RedStone (Primary) @Redstone (1) | BTC 0 / ETH 2 / USDC 0 / USDT 0 % | aucun classe | Un seul oracle declare (RedStone, limite a la chaine Redstone). Prix de jetons de rendement : peu de BTC/ETH direct. Interet : tres grande surface (Ethereum, Monad, Arbitrum) ou la source de prix est peu documentee. |
| 10 | JustLend V1 | Lending | Tron 3903 | 3 902.6 | Internal (Primary) (1) | BTC 15 / ETH 34 / USDC 0 / USDT 3 % | aucun classe | Plus gros pret de Tron du perimetre (3,9 Md$) avec un oracle declare interne seulement : question de la source de prix sans fournisseur externe. Panier : ETH 34 %, BTC 15 %, USDT 3 %. Cible pour documenter la source de prix interne plutot que pour des racines communes entre fournisseurs : on mesurerait la relation entre cette source declaree et d autres sources, sans juger la valeur de l une. |

### Moyennes (50 M$ a 1 Md$)

| # | Protocole | Categorie | Chaines (M$, >= 1 M$) | TVL | Oracles declares (n) | Panier S2-bis | Incidents d oracle | Pourquoi |
|---|---|---|---|---:|---|---|---|---|
| 11 | Dolomite | Lending | Ethereum 329, Arbitrum 25, Berachain 5 | 359.9 | Chainlink (Primary) @Arbitrum,Polygon zkEVM,X Layer; Chronicle (Primary) @Mantle; RedStone (Primary) @Berachain; Chainsight (Secondary) @Berachain (4) | BTC 2 / ETH 17 / USDC 8 / USDT 0 % | aucun classe | Quatre fournisseurs declares (Chainlink, Chronicle, RedStone, Chainsight) mais seulement pour Arbitrum, Mantle, Berachain... et aucun declare pour Ethereum (329 M$ sur 360) : manque de documentation a combler. Panier : ETH 17 %, USDC 8 %. |
| 12 | HyperLend Pooled | Lending | Hyperliquid 393 | 392.7 | Chainlink (Primary); Pyth (Secondary); RedStone (Primary) (3) | BTC 3 / ETH 0 / USDC 2 / USDT 0 % | aucun classe | Trois fournisseurs declares (Chainlink, RedStone en principal ; Pyth en secondaire) sur Hyperliquid : racines communes a mesurer sur une chaine peu etudiee. Panier dominé par kHYPE ; BTC 3 %. |
| 13 | NAVI Lending | Lending | Sui 189 | 189.0 | Supra (champ ancien); Pyth (champ ancien) (2) | BTC 33 / ETH 1 / USDC 8 / USDT 1 % | aucun classe | Sui, Pyth + Supra (champ ancien de DefiLlama, sans type ni preuve). Panier : BTC 33 % (enzoBTC), USDC 8 %. Bonne cible Sui, deux fournisseurs. Incident non oracle rattache au parent NAVI Protocol (entree Volo Vault, id 3711) : cle privee compromise, 3,5 M$, 2026-04-21 (champ source vide) [lu]. |
| 14 | Rhea Lend | Lending | Near 196 | 196.1 | Atlas (Aggregator); Pyth (Aggregator); OutLayer (Aggregator) (3) | BTC 0 / ETH 0 / USDC 1 / USDT 1 % | 2026-04-16 Spot Price Manipulation 18.40 M$ | Incident classe par DefiLlama : manipulation de prix au comptant, 18,4 M$, 2026-04-16 (champ source vide ; cela ne dit pas que l oracle declare a failli). Trois agregateurs declares (Atlas, Pyth, OutLayer) sur NEAR. Panier hors S2-bis (LiNEAR, stNEAR). |
| 15 | Blend Pools V2 | Lending | Stellar 164 | 163.9 | RedStone (Aggregator); Reflector (Aggregator) (2) | BTC 0 / ETH 0 / USDC 7 / USDT 0 % | 2026-02-22 Spot Price Manipulation 10.97 M$ | Incident classe par DefiLlama : manipulation de prix, 10,97 M$, 2026-02-22 (champ source vide). Deux fournisseurs declares (RedStone, Reflector) sur Stellar. Panier : XLM 93 %, USDC 7 %. |
| 16 | Save | Lending | Solana 98 | 97.9 | Pyth (Primary); Switchboard (Fallback) (2) | BTC 2 / ETH 0 / USDC 6 / USDT 2 % | 2022-11-02 Spot Price Manipulation 1.26 M$ | Ex-Solend, Solana : Pyth principal + Switchboard en repli. Incident classe par DefiLlama en 2022 (1,26 M$ ; un autre cas, abus de parametres, la veille). Panier : surtout LST Solana ; USDC 6 %. |
| 17 | River Omni-CDP | CeDeFi | BNB Chain 56, Base 29, BSquared 21 | 106.6 | Chainlink (Primary) @BOB,BNB Chain,Arbitrum; DIA (Primary) @BEVM; Api3 (Primary) @BOB; eOracle (Primary) @bsc,hemi; RedStone (Secondary) @hemi; Chainlink (Secondary) @bsc (5) | BTC 100 / ETH 0 / USDC 0 / USDT 0 % | aucun classe | Cinq fournisseurs declares (Chainlink, DIA, Api3, eOracle, RedStone) selon la chaine : le nombre le plus eleve du perimetre, a egalite avec Re7 Labs (94 M$) et ZeroLend Lending (1,4 M$) (declare, non mesure). Panier : 99,5 % BTC (derives de BTC), c est le coeur de S2-bis (BTC). Multi-chaines (BNB, Base, BSquared). |
| 18 | GMX V2 Perps | Derivatives | Arbitrum 204, Avalanche 9 | 213.4 | Chainlink (Primary) (1) | BTC 24 / ETH 26 / USDC 41 / USDT 0 % | aucun classe | Perps de 213 M$ sur Arbitrum, un seul oracle (Chainlink). Panier : USDC 41 %, ETH 26 %, BTC 24 % : exactement les actifs de S2-bis. Dependance unique : cas pour mesurer les racines communes entre l oracle declare et d autres sources. Incidents non oracle, lies par le parent GMX (GMX V1 Perps, id 337) : reentrance de 42 M$ le 2025-07-09 (40 M$ restitues) ; “Stale Price Arbitrage” de 0,565 M$ le 2022-09-18, classe Market Manipulation (champ source vide) [lu]. |
| 19 | Benqi Lending | Lending | Avalanche 130 | 130.2 | Chainlink (Primary) (1) | BTC 6 / ETH 1 / USDC 0 / USDT 2 % | aucun classe | Avalanche, un seul oracle declare (Chainlink). Panier surtout sAVAX ; BTC 5,5 %, dont BTC.b 3,7 % et WBTC.e 1,9 %. Cible pour la couverture Avalanche ; interet limite sur S2-bis. |
| 20 | Usual USD0 | RWA | Ethereum 88 | 87.8 | Chainlink (Primary) @Ethereum; Pyth (Primary) @Arbitrum (2) | BTC 0 / ETH 0 / USDC 0 / USDT 0 % | aucun classe | Chainlink sur Ethereum et Pyth sur Arbitrum : deux fournisseurs selon la chaine. Panier en actifs reels tokenises (USYC, USTBL) : categorie RWA demandee, mais hors BTC/ETH/USDC/USDT. Incident non oracle : classe par DefiLlama “Missing Input Validation”, 0,043 M$, 2025-05-27 (champ source vide) [lu]. |

### Petites (1 a 50 M$)

| # | Protocole | Categorie | Chaines (M$, >= 1 M$) | TVL | Oracles declares (n) | Panier S2-bis | Incidents d oracle | Pourquoi |
|---|---|---|---|---:|---|---|---|---|
| 21 | Echelon Market | Lending | Aptos 8 | 8.1 | Chainlink (Primary) @Aptos; Pyth (Primary) @Move; Pyth (Secondary) @Aptos; Switchboard (Secondary) @Aptos (3) | BTC 7 / ETH 1 / USDC 24 / USDT 1 % | aucun classe | Aptos : Chainlink, Pyth (principal) et Switchboard (secondaire). Aucun protocole du perimetre >= 50 M$ n a Aptos pour chaine principale : bon test petite chaine. Panier : USDC 24 %, BTC 7 %. |
| 22 | Scallop Lend | Lending | Sui 12 | 11.6 | Supra (champ ancien); Switchboard (champ ancien); Pyth (champ ancien) (3) | BTC 10 / ETH 11 / USDC 7 / USDT 4 % | aucun classe | Sui : Pyth, Supra, Switchboard (champ ancien). Trois fournisseurs sur un petit protocole : bon terrain d essai. Panier : BTC 10 %, ETH 11 %, USDC 7 %. Un incident hors oracle : classe par DefiLlama “Reward Logic Flaw”, 0,142 M$, 2026-04-26, source vide [lu]. |
| 23 | Silo V2 | Lending | Avalanche 2, Sonic 2, Ethereum 2 | 6.2 | RedStone (Primary) @Sonic,Ethereum; eOracle (Primary) @Avalanche,Arbitrum; Chainlink (Secondary) (3) | BTC 31 / ETH 1 / USDC 4 / USDT 0 % | 2026-04-03 Oracle Misconfiguration 0.36 M$ | Incident classe par DefiLlama : mauvaise configuration d oracle, 0,36 M$, 2026-04-03 (Arbitrum). Trois fournisseurs declares (RedStone, eOracle, Chainlink en secondaire). Panier : BTC 31 % (savBTC). |
| 24 | Moonwell Lending | Lending | Base 12, Optimism 1 | 13.7 | Chainlink (Primary) (1) | BTC 36 / ETH 32 / USDC 0 / USDT 0 % | 2025-11-04 Spot Price Manipulation 1.00 M$; 2026-02-15 Oracle Misconfiguration 1.78 M$; 2026-08-27 Spot Price Manipulation 8.70 M$ | Trois incidents d oracle classes par DefiLlama en 2025-2026 (1,0 M$ le 2025-11-04, sur Base et Optimism ; 1,78 M$ le 2026-02-15 ; 8,7 M$ le 2026-08-27, sur Base ; champ source vide) pour un seul oracle declare (Chainlink) : cela ne dit pas que l oracle declare a failli. Le plus fort argument de besoin concret. Panier : ETH 32 %, BTC 36 %. |
| 25 | EVAA Protocol | Lending | TON 9 | 9.3 | Stork (Aggregator); RedStone (Aggregator); Pyth (Aggregator) (3) | BTC 0 / ETH 0 / USDC 0 / USDT 95 % | aucun classe | TON : Pyth, RedStone, Stork (agregateurs). Trois fournisseurs sur une chaine hors liste. Panier : USDT 95 % : S2-bis (USDT). |
| 26 | Folks Finance Lending | Lending | Algorand 30 | 30.3 | Internal (champ ancien); Pyth (champ ancien); Chainlink (champ ancien) (3) | BTC 0 / ETH 0 / USDC 0 / USDT 100 % | aucun classe | Algorand : Chainlink, Pyth et un oracle interne (champ ancien). Panier 100 % USDT. Meme parent que Folks xChain (6,7 M$, Chainlink seul). |
| 27 | Gearbox | Lending | Ethereum 24, Etherlink 1 | 25.5 | RedStone (Primary) @Ethereum; Chainlink (Primary) @Ethereum; eOracle (Primary) @Hemi (3) | BTC 5 / ETH 20 / USDC 4 / USDT 0 % | aucun classe | Ethereum : RedStone et Chainlink en principal, eOracle sur Hemi : racines communes a mesurer sur un protocole de levier. Panier : ETH 20 %, BTC 5 %, USDC 4 %. |
| 28 | HypurrFi Pooled | Lending | Hyperliquid 6 | 5.5 | Pyth (Aggregator); RedStone (Aggregator) (2) | BTC 1 / ETH 0 / USDC 2 / USDT 4 % | aucun classe | Hyperliquid : Pyth + RedStone (agregateurs). Petit protocole sur une chaine demandee. Panier peu lie a S2-bis (kHYPE). |
| 29 | YeiLend | Lending | Sei 6 | 6.3 | Api3 (Primary); Pyth (Fallback); RedStone (Secondary) (3) | BTC 3 / ETH 1 / USDC 5 / USDT 1 % | aucun classe | Sei : Api3 principal, Pyth en repli, RedStone secondaire : trois fournisseurs avec role distinct, utile pour tester les racines communes. Panier : WSEI, un peu d USDC. |
| 30 | Ostium | Derivatives | Arbitrum 8 | 7.7 | Stork (champ ancien); Chainlink (champ ancien) (2) | BTC 0 / ETH 0 / USDC 100 / USDT 0 % | aucun classe | Perps sur FX, metaux et energie (Arbitrum) : Stork + Chainlink (champ ancien). Panier 100 % USDC. Incident non oracle, a connaitre avant tout contact : classe par DefiLlama “Private Key Compromised”, 23,75 M$, 2026-07-15, source vide [lu]. |

Repartition par chaine principale : Ethereum 6, Solana 3, Base 3, BNB Chain 2, Tron 2, Hyperliquid 2, Sui 2, Arbitrum 2, Avalanche 2, Near 1, Stellar 1, Aptos 1, TON 1, Algorand 1, Sei 1. Soit 15 chaines.

Reserve (non retenus, meme profil) : Sky Lending (CDP, 5 919 M$, Chronicle + Internal ; sorti de la liste courte par la correction C-7 : son acheteur, la gouvernance de Sky, est deja vise par P1 sous “Spark/Sky” — P1 l.117, SYNTHESE l.322 [lu] — donc la cible n est pas une organisation nouvelle ; DefiLlama le range sous un autre parent, parent#maker, que SparkLend, parent#spark), Jupiter Perps (820 M$, meme equipe que Jupiter Lend ; Chainlink + Chaos + Pyth, preuve fournie par DefiLlama), Fluid (714 M$, Chainlink seul), Bonzo Lend (Hedera, 5,4 M$, Chainlink + Supra ; incident classe 2026-07-11, 9,05 M$), Angle (1,8 M$, trois fournisseurs externes — Chainlink, RedStone, Pyth — et un TWAP, tous dans l ancien champ), Neverland (Monad, 8,4 M$, Chainlink + RedStone).

Cas particuliers a ne pas confondre : (a) Steakhouse, Gauntlet : couches de curation, TVL en partie comptee ailleurs ; (b) Ethena USDe : aucun oracle declare [abs] ; (c) JustLend et USDD : dependance unique, sans question de racines communes ; (d) Dolomite : aucun oracle declare pour Ethereum, ou se trouvent 329 M$ sur 360 [lu].

## 5. Ce que la carte dit des clients possibles [inféré]

- Le terrain des racines communes est etroit en valeur mais large en nombre : 73 protocoles ont au moins 2 oracles externes declares (48 petits, 18 moyens, 7 grands) ; 76 en ont au moins 2 en comptant les sources internes. Par chaine principale (les 76) : hors liste 26, Ethereum 19, BNB Chain 8, Solana 6, Base 4, Sui 4, Hyperliquid 3, Arbitrum 3, Aptos 2, Avalanche 1, Tron 0.
- Parmi les grandes declarees, la plupart sont en dependance unique ou interne (Maple, USDD, Jupiter Lend, JustLend, Pendle, Jito Liquid Staking) ou en couple (Sky Lending : Chronicle + interne, hors liste courte). Sept grands protocoles declarent au moins 2 oracles externes ; **quatre sont des familles deja etudiees** (SparkLend, Compound V3, Venus Core Pool, Kamino Lend). Hors familles deja etudiees, les grands multi-oracles sont les curateurs (Steakhouse, Gauntlet) et Lista.
- Arbitrum, Sui, Aptos, Avalanche et Hyperliquid n ont aucun protocole de plus de 1 Md$ comme chaine principale ; Tron en a deux (JustLend, USDD), a source unique ou interne (T1a).
- Chiffres a ne pas surinterpreter : l absence d oracle declare (42 % du perimetre) est un manque de documentation DefiLlama, pas une preuve d absence d oracle.

## 6. Pistes pour la suite (aucune action prise)

- Verifier par la documentation propre de chaque cible (lecture de pages officielles) les oracles declares avant tout contact : surtout Dolomite (Ethereum), Ethena, Pendle.
- Lire les post-mortems des incidents “Oracle Manipulation” de la liste (champ source vide chez DefiLlama) avant de les citer.
- Cette carte a ete relue par un reviseur different (G2, verdict ACCEPTE-AVEC-CORRECTIONS) ; les corrections sont appliquees (section 9) et restent a faire controler (reviseur ou controle de transcription de l orchestrateur).

## 7. Limites

1. **Declaratif non verifie** : tous les oracles, roles et dates viennent de DefiLlama (preuves en liens, non ouvertes par moi). Je n ai lu aucune documentation de protocole.
2. **Couverture partielle** : 971 protocoles sur 8483 ont `oraclesBreakdown` et 242 l ancien champ ; 42 % du perimetre n a rien [abs]. Les protocoles a champ ancien n ont ni role ni preuve.
3. **Oracles par chaine** : quand DefiLlama liste des chaines, la chaine principale peut rester sans oracle declare (Dolomite sur Ethereum).
4. **TVL** : valeur deposee declaree par DefiLlama, hors emprunts, hors staking ; peut compter deux fois la meme valeur entre couches ; peut etre mal evaluee (champ `misrepresentedTokens` non filtre). Pas de verification sur chaine.
5. **Tableau par oracle recalcule par moi** : l endpoint officiel `/oracles` est payant (402) ; les lignes ne sont pas additives (un protocole a plusieurs oracles est compte dans chacun) ; les valeurs suivent la regle de la section 2.3. Seules les deux parts de repli montrees a part dans T2 sont des bornes hautes : RedStone 1 256 M$ (Pendle V2) et Pyth 88 M$ (Usual USD0). La version precedente de la piece sous-evaluait Chainlink de 1,3 Md$ et surevaluait Chaos, RedStone et DIA (section 9, C-1).
6. **Classification des chaines** : chaine principale = plus forte TVL ; les noms de chaines suivent DefiLlama (“Binance”, “Hyperliquid L1”).
7. **Incidents** : `/hacks` classe “Oracle Manipulation” dont la grande majorite en “Spot Price Manipulation” (prix de pool), ce qui ne designe pas une faute d un fournisseur comme Chainlink ou Pyth. Champ `source` vide pour tous les incidents du fichier : non verifiables ici. Lecture des incidents limitee aux liens par `defillamaId` ou parent. La colonne “Incidents d oracle” ne montre que les incidents classes oracle ; les incidents d un autre type, lies par identifiant ou par parent, sont cites dans la colonne “Pourquoi” (GMX, NAVI, Usual USD0, Ostium, Scallop).
8. **Panier S2-bis** : regroupement par symbole, approximatif (par ex. un symbole ETH sur Tron). Symboles non classes qui changent la lecture : Gearbox, `SAVETH` (37,7 %) et `WMOOCURVEETH+-WETH` (16,2 %) ne sont pas comptes en ETH alors que la ligne dit ETH 20 % (l identite de `SAVETH` n est pas etablie [abs]) ; `AVALANCHEUSDC` n est pas compte en USDC (GMX : 43 % au lieu de 41 % ; Benqi : 3 % au lieu de 0 %). Le panier de Jito Liquid Staking (SOL 100 %) vient d un detail telecharge apres les 29 autres, le meme jour (2026-10-04, 21:11 UTC).
9. **Hors perimetre** : aucune donnee sur les montants empruntes, les liquidations, ni sur le prix reel paye pour un oracle ; aucune verification de l appetit commercial.
10. Donnees vivantes : elles changent chaque jour ; la lecture date du 2026-10-04.
11. **Definition de mort et protocoles `deadUrl`** : la regle ecrite d avance retient `deadFrom` renseigne, tel quel. Le sens des champs `deadUrl` et `deadFrom` n est pas documente dans les copies de la documentation lues [abs]. **24 protocoles a `deadUrl: true` restent dans le perimetre** : 353 M$ de TVL (0,4 % des 93 313 M$), 20 en A et 4 en B, 15 avec un oracle declare (82 M$) ; les plus grands : RealT Tokens 155 M$, AZverse Perps 52 M$, Alpaca Leveraged Yield Farming 37 M$, RealT RMM Marketplace V2 29 M$. Aucun n est parmi les 30 cibles [calc]. Pas de recomptage : les chiffres des tables incluent ces 24 protocoles.
12. **Usages d oracle sans lien avec un prix** : DefiLlama ne type l usage d une entree d oracle que pour 9 entrees sur 1 201 (`RNG` 7, `PoR` 2) [lu]. Dans le perimetre : Re (RWA, 398 M$) a pour seul oracle Chainlink de type `PoR` (preuve de reserves) ; il est compte comme ayant un oracle declare, et chez Chainlink comme seul oracle ; PoolTogether V5 (Yield Lottery, 2,4 M$) a pour seul oracle Witnet de type `RNG` (aleatoire), seule raison de son entree en B. Cas sans type, d apres mon raisonnement [inféré] : Polymarket International (UMA, 368 M$) et Across (UMA, 21 M$) resolvent des evenements ou des relais, pas un prix ; PoolTogether V3 (Chainlink, 5,0 M$) sert a un tirage au sort. Ils restent comptes. **Chiffres indicatifs** sans les deux entrees typees `RNG`/`PoR` [calc, `out/biais.json`] : B 78, A+B 423, 244 avec oracle declare (67 349 M$), Chainlink 128 protocoles, ligne Witnet supprimee. La part du perimetre qui depend reellement d un prix n est pas etablie [abs].
13. **T4 : des paires, pas des combinaisons** : T4 compte les protocoles qui declarent deux oracles donnes (paires co-declarees, non additives) ; la colonne “exactement ces deux oracles” donne les protocoles qui n en declarent pas d autres.
14. **T1d partielle** : T1d ne montre que les 15 premieres des 67 chaines de la ligne Autres (52 des 136 protocoles).

## 8. Fichiers, versement et empreintes

**Versement prevu** : `docs/adr-0029/etude-marche/carto/`, comme piece de contexte commercial non normative d ADR-0029. Fichiers verses :
- la piece `CARTO-DEFI-ORACLES.md` ;
- les scripts `traite.py`, `enrichit.py`, `assemble.py`, `fetch_detail.sh` ;
- les entrees de choix `cibles.json` et `pourquoi.json` ;
- `out/perimetre.csv` (424 lignes, sha256 `d452e2dbe20f5b981bfb99e71b9e00b3a318193c57fd6d5cbb99d04342faa945`) : liste “pour chacun” du perimetre (identifiant, nom, parent, categorie, perimetre A ou B, TVL, taille, chaine principale, TVL par chaine, oracles actifs avec role et chaines, source des oracles, nombres d oracles et d oracles externes, famille deja etudiee, nombre d incidents d oracle classes) ;
- `SHA256SUMS` (empreintes de tous les fichiers de la carte, `raw/` compris).

**`raw/` reste hors depot** : seules ses empreintes sont versees (`SHA256SUMS`). Les reponses changent chaque jour ; une relecture ne peut donc rejouer la chaine que sur une copie de `raw/` conservee ailleurs.

**Ordre de rejeu** (chaque etape lit la sortie de la precedente) :
1. `python3 traite.py` (hors reseau ; lit `raw/protocols.json` et `raw/hacks.json` ; ecrit `out/rows.json`, `out/perimetre.csv`, `out/tables.md`, `out/biais.json`) ;
2. `bash fetch_detail.sh` (reseau ; lit `out/rows.json` et `cibles.json` ; ecrit `raw/detail/{slug}.json`) ;
3. `gzip -n raw/detail/*.json` : **la compression n est pas scriptee** ; `enrichit.py` lit `{slug}.json.gz` avant `{slug}.json`, donc un `.json.gz` ancien l emporte sur un `.json` frais (supprimer les `.gz` perimes avant de rejouer) ;
4. `python3 enrichit.py` (hors reseau ; ecrit `out/cibles-actifs.json`) ;
5. `python3 assemble.py` (hors reseau ; ecrit cette piece).
Hors reseau, avec `raw/` et `raw/detail/` deja presents : etapes 1, 4 et 5. Le detail `raw/detail/jito-liquid-staking.json.gz` a ete telecharge seul par l orchestrateur (2026-10-04 21:11 UTC, HTTP 200, `gzip -n`), apres la passe de corrections ; meme jour que les 29 autres lignes.

Empreintes des reponses brutes (sha256) : voir `SHA256SUMS`. Principales :

- `raw/protocols.json` `a6733371011e428ab1394a59b511f092b2236ee9db6e71a2c9b5709aa2c52068`
- `raw/lite_protocols2.json` `a8eaa5a79a90b3efbda1de88775cc138f0f0afdb131b6588c3de852f9d8383b9`
- `raw/oracles.json` `77af6ecfa9bf69c017f1d642d816fa1db0e8bdb8a5dd77009c8454b6441c0f2a`
- `raw/hacks.json` `1b329996176ae10dc1396aa2322f4a80dfc0068fb93bfb44c663a22fe70b6842`
- `raw/api-docs.html` `7e1aa5e499f331aa6fca16f15ab5dd34e4e10922c308786a7893d795ea94c6dd`
- `raw/llms-free.txt` `8e9451172731b3580e7c8bc8dac4fdb3f47c05a3ff16816bdcec3fe90224f170`


## 9. Corrections G2 appliquees (relecture `g2/G2-CARTO.md`, section 7, C-1 a C-13)

Adjudications de l orchestrateur appliquees la ou la G2 laissait un choix (brief des corrections). Passe : 2026-10-04, `date -u` 21:02 a 21:11 UTC, sans reseau.

- **C-1 (T2, valeur declaree)** : appliquee. `traite.py` corrige sur les quatre points : toutes les entrees d un meme oracle sont reunies (Venus ne perd plus son entree `@Binance`) ; chaines comparees sans casse, alias “bsc” = BNB Chain ; une chaine presente a TVL nulle compte pour 0 (Steakhouse n est plus compte en entier chez Chaos et RedStone, River chez DIA) ; repli sur la TVL totale seulement sans correspondance, montre a part (nouvelle colonne de T2). Resultat : Chainlink 46 060 ; Chronicle 11 856 ; Internal 11 180 ; RedStone 11 084 dont 1 256 de repli ; Pyth 5 947 dont 88 de repli ; Atlas 2 576 ; Switchboard 1 483 ; Binance Oracle 1 133 ; Chaos 828 ; eOracle 241 ; DIA 117 ; egal a `g2/sortie-t2-attendu.txt` sur les 18 lignes (comparaison par script, 0 ecart) ; les autres lignes de T2 inchangees. Textes corriges : §1 (44,7 devient 46,1 Md$), §2.3 (le montant du repli), §7.5 (bornes hautes limitees aux deux parts de repli ; Chainlink etait sous-evalue). Le reste de la chaine est inchange : `out/perimetre.csv` garde le meme sha256.
- **C-2 (definition de mort)** : appliquee, sans recomptage. Mort = champ `deadFrom` renseigne (§1, §2.4, T0). Declare en §7 point 11 : 24 protocoles `deadUrl` restes dans le perimetre, 353 M$, 20 en A et 4 en B, 15 avec un oracle declare, aucun parmi les cibles (verifie par l assemblage).
- **C-3 (usages sans lien avec un prix)** : appliquee. Comptes inchanges ; cas Re (`PoR`), PoolTogether V5 (`RNG`), PoolTogether V3, Polymarket International et Across (UMA, [inféré]) declares en §7 point 12, avec les chiffres sans `RNG`/`PoR` a titre indicatif (B 78, A+B 423, 244 declares, 67 349 M$, Chainlink 128, ligne Witnet supprimee ; retrouves par mon propre script, `out/biais.json`). §1 reformule : “dependent d un prix ou declarent un oracle”.
- **C-4 (T4)** : appliquee. T4 retitre en paires co-declarees non additives, avec la colonne “exactement ces deux oracles” (Chainlink et RedStone : 28 dont 8, 185 M$ ; Chainlink et Pyth : 17 dont 9) ; §1 puce 3 et §7 point 13 corriges.
- **C-5 (grands multi-oracles)** : appliquee. §5 puce 2 : sur les 7 grands a au moins 2 oracles externes, 4 sont SparkLend, Compound V3, Venus Core Pool et Kamino Lend ; Steakhouse, Gauntlet et Lista le sont hors familles deja etudiees.
- **C-6 et C-7 (liste courte G, Sky)** : appliquees. Sky Lending sort de la liste (son acheteur, la gouvernance de Sky, est deja vise par P1 sous “Spark/Sky” : dit dans la reserve et en §1) ; Jito Liquid Staking entre a sa place (Solana, Switchboard seul declare, B) avec sa ligne ; Ethereum tombe a 3 cibles G ; repartition par chaine recalculee (Ethereum 6, Solana 3, Base 3, BNB Chain 2, Tron 2, Hyperliquid 2, Sui 2, Arbitrum 2, Avalanche 2, Near 1, Stellar 1, Aptos 1, TON 1, Algorand 1, Sei 1). **Ecart motive** : le panier de Jito n est pas calcule (detail `/protocol/jito-liquid-staking` absent de `raw/detail/`, reseau interdit par le brief) ; la ligne le disait [abs] et la limite a ete rendue a l orchestrateur, qui a telecharge le detail le meme jour (2026-10-04 21:11 UTC) et rejoue enrichit puis assemble : panier SOL 100 %.
- **C-8 (Gauntlet)** : appliquee. SYNTHESE cite Gauntlet comme comparable de prix (§1.10 l.359, C20 l.463) ; ses cabinets de risque sont Chaos Labs et LlamaRisk (l.322).
- **C-9 (incidents)** : appliquee. Ostium (“Private Key Compromised”, 23,75 M$, 2026-07-15) et Scallop (“Reward Logic Flaw”, 0,142 M$, 2026-04-26) attribues a DefiLlama, source vide ; Moonwell : reserve de la ligne Rhea ajoutee, incident du 2025-11-04 sur Base et Optimism ; incidents non oracle ajoutes pour GMX (parent GMX V1), NAVI et Usual USD0. Precision : l incident cite pour NAVI est une entree Volo Vault (id 3711) dont le champ parent est `parent#navi-protocol`.
- **C-10 (registre 09)** : appliquee. Trois formulations de la version precedente reecrites : JustLend (l.246), GMX (l.259), River (l.258). JustLend et GMX parlent maintenant d une relation mesuree entre l oracle declare et d autres sources, sans juger la valeur de l une ; River : cinq fournisseurs declares, le nombre le plus eleve du perimetre, a egalite avec Re7 Labs et ZeroLend Lending (declare, non mesure ; verifie par `out/biais.json`). Citations web entre “”, aucun guillemet francais ; relecture de la piece contre les entrees du registre.
- **C-11 (paniers)** : appliquee. Ethena : USDe 97,3 %, USDtb 1,4 %, USDC 1,3 % ; Benqi : BTC 5,5 % dont BTC.b 3,7 % et WBTC.e 1,9 % ; JustLend : BTC 15 (14,53 %) dans le tableau, par arrondi a deux decimales dans `enrichit.py` (le double arrondi disparait) ; Gearbox : USDC 4 % ; symboles non classes nommes en §7.8 ; Angle : trois fournisseurs externes et un TWAP, ancien champ.
- **C-12 (libelles)** : appliquee. “Par categorie du perimetre A+B (categories B marquees (B))” ; T1d : 15 premieres des 67 chaines (52 des 136 protocoles) ; colonne des chaines des cibles : **liste entiere** a 1 M$ ou plus, sans coupure.
- **C-13 (versement)** : appliquee. Section 8 : chemins de versement `docs/adr-0029/etude-marche/carto/`, `raw/` hors depot (empreintes seules), `out/perimetre.csv` verse et cite avec son sha256, ordre de rejeu corrige (traite, fetch_detail, gzip -n, enrichit, assemble), compression non scriptee et priorite du `.json.gz` signalees ; ligne d exposition en tete de piece. **Ecart motive** : l attestation de la passe initiale n est pas reconstituable par la passe de corrections ; elle est limitee a ce que la piece cite et reste a confirmer par le controle de transcription.
- **Hors liste** : la docstring de `traite.py` n annonce plus un `out/shortlist.json` qu il ne produit pas (O-8) ; accents (O-1), unification “valeur securisee”/“valeur declaree” (O-7) et vivier M (O-5) non traites.
