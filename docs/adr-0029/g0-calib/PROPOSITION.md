# G0 — proposition pour le lot CALIB-ACTIFS (ETH/USD, USDC/USD, USDT/USD : paires servies, historiques, τ, planchers, σ), sans code

- **Statut** : proposition d'un worker à l'orchestrateur, à adjuger. Rien n'est décidé ici. Aucun code, aucune écriture au dépôt,
  aucune opération git en écriture, aucun calcul sur un historique.
- **Gate 0** : modèle résolu `claude-opus-5-5` (identifiant donné par l'environnement), fiche `shogen-worker`, effort `max`
  demandé ; l'effort n'est pas vérifiable depuis la session.
- **Dates** (`date -u`) : lecture des pièces et recomptes le 2026-10-08 de 19:40 à 20:04 UTC ; rédaction de 20:09 à 20:19 UTC,
  relecture et corrections jusqu'à 20:20 UTC.
- **Brief** : `scratchpad/s2bis/calib2/BRIEF-G0-CALIB.md`, 27 lignes, sha256 `0714e2a4…ee34` [mesuré] ; il n'annonce ni sha256 ni
  base.
- **Base lue** : branche `claude/compassionate-noether-szmdyj`, tête `5cfe746` au début de la lecture, au début de la
  rédaction et à 20:18 UTC, `git status --short` vide à chaque relevé [mesuré]. Le brief ne nomme pas de base : base consignée, rien n'est avancé (E-3, §15).
- **Relevé du lecteur** : `calib2/PAIRES-ET-TEMOIN.md` (« PT », 140 lignes, sha256 `fe884dec…943e`), présent, lu en entier.
  Ses faits sont [2nd] ici ; ceux qui fondent un choix sont **recomptés** sur ses copies brutes (46 fichiers, §15) [recompté].
- **Rattachement** : ADR-0029 révision 3, acceptée : §2.6 (l.177-192, dont l.185-191 CALIB-ACTIFS) ; tableau l.63 (D-4) ; §2.5
  (l.166-175, dont l.173 pools et l.174 témoin) ; §2.2 pt 9 (l.98) ; §2.7 pts 2, 8, 9, 11 (l.200, l.207, l.210, l.212, l.214) ;
  §2.9 (l.236) ; §3 (l.281, l.310) ; §6 lot 3 (l.383), jalons (l.395) et ajout daté du G0 de collecte (l.397) ; §6 q. 9 à 13
  (l.415-419) ; §8.1 (l.451, l.457-460) ; §8.2 q. 2 et 3 (l.469-470). DÉC D-4 (l.34-37), §7 n° 3 (l.103) et n° 5 (l.105). AQT
  Q2 (l.41-62), Q3 (l.64-81), Q4 (l.83-100). G0 de vague l.14. G0 de collecte : PROP-C l.167-171, l.198, l.201, l.204-232,
  l.310-321 ; AVIS-C l.94, l.96, l.99, l.103. Annexe B d'ADR-0028 : SHOGEN-S2BIS-CALIB-L189-1 (B.65, l.1086), adjudication
  Q-RBc-1 (B.65, l.1074), B.52 (l.845-850). Réponses de l'investisseur du 2026-10-04 (JOURNAL l.382, verbatim).
- **Modèle de forme** : `docs/adr-0029/g0-plan2/PROPOSITION.md` et `docs/adr-0029/g0-sim/PROPOSITION.md`.
- **Conventions** : [lu] lu sur la pièce ; [mesuré] commande lancée par le rédacteur ; [recompté] fait du relevé PT ou de SH
  recompté par le rédacteur sur la copie brute du lecteur ; [calc] calcul du rédacteur (jamais sur un historique) ; [inféré]
  raisonnement du rédacteur ; [abs] absent des pièces lues ; [2nd] fait lu par un lecteur, non relu ici. Exigences : E-CA-nn.
  Sous-lots : CA-n. Tests : T-CA-… ; mutants : M-CA-nn ; questions techniques : Q-CA-nn ; questions à l'investisseur : INV-n.
  **[ADR]** = touche la lettre de l'ADR-0029 ; **[G0-C]** = touche la lettre du G0 de collecte. Tailles : lignes ajoutées,
  tests et données compris, documents hors compte ; toutes [inféré].
- **Renvois** : « l.n » = ADR-0029 à `5cfe746` (sha256 `35563d8f…9eb8`, 571 lignes). « SH » = `docs/adr-0029/calib/
  SOURCES-HISTORIQUES.md` (`f649e30f…73cf`). « PT » = relevé ci-dessus. « EP » = `docs/adr-0029/ETUDE-POOL-BIS.md`
  (`d3780f13…e11e`). « DÉC », « AQT » = `DECISIONS-ARCHITECTURE-S2BIS.md` (`603abda2…1920`), `AVIS-QUESTIONS-TECHNIQUES-V3.md`
  (`836ece5e…c79d`). « PROP-C », « AVIS-C » = `docs/adr-0029/g0-collecte/PROPOSITION.md` (`0cdf84c2…bfd0`), `AVIS.md`
  (`a919b307…16ce`). « config » = `s2bis/shogen_s2bis/recalc/config_analyse.py` (`82abdba5…8b26`). « B.nn l.n » = annexe B
  d'ADR-0028 à `5cfe746` (`3f738722…d0d2`).

## 0. En bref

1. **Objet** : fixer, avant tout calcul, ce que l'ADR laisse au G0 de CALIB-ACTIFS (l.186 : paires servies, historiques,
   « la grille de τ et ce que les décisions laissent ouvert » ; l.189 : valeurs des formules de σ et du plancher de τ des
   agrégateurs), puis décrire le lot de calcul (CA-0 à CA-6) qui produira τ et σ d'ETH, d'USDC et d'USDT sur des historiques
   à une minute, après la réponse de l'investisseur et l'épinglage. Rien n'est calculé ici sur un historique.
2. **Paires servies** (PT, recomptées) : ETH/USD en dollar chez 9 hôtes sur 10 (OKX n'a pas `ETH-USD`) ; USDC/USD chez 8 (ni
   Coinbase ni OKX) ; USDT/USD chez les 10. Pools proposés : **ETH 10 unités** si binance et okx y entrent cotés en USDT comme
   pour BTC (Q-CA-01, recommandé ; 9 sinon), **USDC 8**, **USDT 10**. USDC/USD est servi par **cinq places**, non trois
   (binance `USDCUSD` s'ajoute à kraken, bitstamp, gemini, bitfinex) : constat contraire à l.173 et l.214 (§10).
3. **Historiques** (SH) : en lecture « disponibilité », la condition se lit remplie classe par classe : ETH 6 places, USDC 4
   (sans marge pour « ≥ 4 », avec marge pour le « ≥ 3 » de F3), USDT 6. En lecture « republication des octets bruts permise »,
   aucune place ne la remplit : ETH en seconde vague, stables aux « planchers seuls ». La lecture engage une licence et le
   calendrier : **questions à l'investisseur** INV-1 et INV-2 (§9), non tranchées ici.
4. **Règles proposées** (§4) : fenêtre du deuxième trimestre 2026, strates du calendrier de S2 ; τ des places =
   grid-ceil(1,5 × max_s P99,9 des écarts relatifs à la médiane leave-one-out des clôtures au « dernier prix connu », 0,05 %) ;
   τ des agrégateurs par la formule de l.189, avec pour BTC le **maximum de ses deux classes de places** au dénominateur
   (Q-CA-06, choisi sans ouvrir les valeurs de BTC) ; τ des oracles = planchers exacts, 0,75 % et 0,375 % ; σ des oracles =
   1,5 × heartbeat, 5 400 s, 124 200 s et 129 600 s (paramètres relus le 2026-10-08, recomptés) ; σ des places horodatées =
   max(30 s, σ_BTC, troisième terme pris sur les seules places dont l'horodatage est celui de la dernière transaction,
   Q-CA-07) ; σ des agrégateurs = max(300 s, σ_BTC) ; places sans horodatage : σ nul (staleness non évaluable).
5. **Avant le sceau** : tout se calcule avant le sceau, en un lancement épinglé ; les planchers des oracles sont calculés
   ici ; τ et σ des places attendent INV-1 ; rien ne se calcule sur des données de S2-bis (§4.8).
6. **L'adjudication débloque** (§2.6) CB-7 (formes des places), CB-8 (agrégateurs regroupés ; Chainlink : adresses,
   décimales, plafond), CB-9 (témoin, après Q-CA-09 et Q-CA-10) et les contrôles de RB-2 (grilles, formule de τ des
   agrégateurs, planchers : SHOGEN-S2BIS-CALIB-L189-1). Le calcul des valeurs attend INV-1.
7. **Constat neuf, horodatage** : parmi les places horodatées, seul Coinbase porte l'heure de la **dernière transaction** [lu
   sur la copie de la doc ; recompté]. OKX porte une heure de **génération** [lu sur la copie de la doc] ; Bitstamp et Gemini
   une heure de génération ou de fenêtre [inféré, une mesure chacun]. Le motif du troisième terme de σ (AQT l.48 : « le ticker
   porte alors un horodatage ancien ») ne vaut donc que pour Coinbase (Q-CA-07).
8. **Constat neuf, témoin** : les deux lectures sur chaîne (Uniswap, Curve) demandent **deux** hôtes RPC distincts de celui de
   Chainlink, non trois (écart de compte de PT l.124) : `eth.drpc.org` et `rpc.mevblocker.io` suffisent ; un remplaçant écrit
   d'avance reste à essayer depuis les observateurs (Q-CA-10).
9. **Taille** : lot de calcul ≈ 1 100 à 1 300 lignes en 7 sous-lots de 200 lignes au plus, plus ≈ 80 à 120 lignes de contrôles
   dans RB-2 [inféré] ; l'ADR l.310 annonçait ≈ 200 (§10). Calendrier : ≈ 1 à 2 jours de session après la réponse de
   l'investisseur, hors du chemin critique du sceau (S+10/11) [inféré].
10. **Questions** : 15 techniques (§8) ; 2 à l'investisseur et 2 informations (§9).

## 1. Objet, rattachements, périmètre

### 1.1 Objet et rattachements

- **ADR-0029** l.185-191 : « G0 d'abord » (l.186 : historiques publics à une minute, antérieurs à la campagne, pour « au moins
  4 places par classe » ; paires servies ; grille de τ et ce que les décisions laissent ouvert) ; τ des places (l.187) ;
  planchers des oracles et σ = 1,5 × heartbeat (l.188) ; agrégateurs et oracles en « planchers seuls », formules de σ et du
  plancher de τ des agrégateurs, valeurs au G0 (l.189) ; deux méthodes de τ (l.190) ; décalage du sceau sous condition, lue
  classe par classe, F3 « ≥ 3 places ou planchers seuls, sans seconde vague » (l.191) ; rodage hors calibration (l.192).
- **DÉC** D-4 (l.34-37) et §7 n° 5 (l.105) ; **AQT** Q2 (formules, l.51 et l.58) et Q3 (lecture classe par classe, l.70-73).
- **Investisseur** (JOURNAL l.382, verbatim) : « Les 4 ensemble (Recommandé) » (q. 9) ; recommandations acceptées en bloc,
  dont « USDC : les deux mesures, contre le dollar réel et telle que la DeFi la consomme, avec leur écart » (q. 10), « accès
  gratuits sans clé avec remplaçants écrits d'avance » (q. 12), « sources qui interdisent la republication : retirées et
  citées comme amonts » (q. 13).
- **G0 de vague** l.14 (CALIB-ACTIFS-G0 : « conditions d'usage lues », sortie SH). **G0 de collecte** : CB-7 dépend des
  « paires servies (SHOGEN-S2BIS-PAIRES-1, G0 de CALIB-ACTIFS) » (PROP-C l.215) ; CB-8 (l.216) ; CB-9 dépend des « adresses
  des contrats et hôtes RPC lus sur pièce » (l.217) ; budget d'OKX (l.318-319 ; AVIS-C Q-C-10, l.99).
- **Annexe B** : SHOGEN-S2BIS-CALIB-L189-1 (B.65 l.1086) : « contrôles de l.189 non faits : plancher de τ des agrégateurs des
  autres actifs (formule de l.189, CAPO comprise), autres termes de σ ; la grille de 0,05 % de τ des agrégateurs ne dépend
  d'aucune valeur et peut se contrôler dès RB-2 » ; Q-RBc-1 adoptée, « σ ≥ σ_BTC sur les places et les agrégateurs, lettre de
  l.189 » (B.65 l.1074) ; B.52 (l.849-850) : restent ouvertes « les valeurs de σ, des planchers et d'une éventuelle vague (G0
  de CALIB-ACTIFS) ».

### 1.2 Ce que le lot fait

1. **Ce G0, à l'adjudication** : composition des pools et formes par (hôte, actif) (§2) ; lecture de la condition des
   historiques, soumise à l'investisseur (§3, §9) ; règles de calcul complètes (§4) ; contrôles à écrire dans RB-2 (§5.6).
2. **Le lot de calcul** (CA-0 à CA-6, §6) : acquisition des historiques du deuxième trimestre 2026 avec manifeste ;
   normalisation des bougies ; σ, puis τ des places, puis τ des agrégateurs ; planchers des oracles ; sorties versées et
   fragment `tau_sigma` et `unites` pour `s2bis/config/analyse.json`. Un lancement unique, épinglé, sur le patron de
   PLAN-S2BIS, sans aucune lecture de journal.

### 1.3 Entrées

| entrée | usage | état |
|---|---|---|
| PT (2026-10-08) | paires, formes, Chainlink, témoin | présent ; 46 copies brutes recomptées (§15) |
| SH et `docs/adr-0029/calib/SHA256SUMS-ECHANTILLONS.txt` (`988534f0…b5fb`) | places à historique, profondeurs, conditions, comptes du §4 (oracle d'exécution) | versés ; les 148 fichiers listés sont encore dans `scratchpad/s2bis/calib/`, sha256 égaux (148 OK) [mesuré] ; hors dépôt, lus par leur seul sha256 |
| `docs/adr-0029/plan-s2bis/tau_sigma.txt` (`409b2a5e…e6d9`, commit `c11fc82`) | τ et σ de BTC par classe de source, termes des formules de l.189 | versé ; **non ouvert par le rédacteur** (E-6, §15) |
| config et `s2bis/config/analyse.json` (`e9243c79…1d00`) | schéma de `tau_sigma` et `unites` ; constantes (config l.21-31) ; contrôles (l.68-87, l.113-122) | commis ; `tau_sigma` et `unites` à `null` [lu] |
| `scripts/plan-s2bis/regles.py` (`a0140188…88a6`) | rang ⌈999·N/1000⌉, grid-ceil en rationnels, bornes et refus (l.12-36) | commis, égal à son `SHA256SUMS` [mesuré] |
| `s2-harness/shogen_s2/sources.py` (`0c81fc33…afe4`), `window.py`, `r1.py` | formes et classes de S2 (l.239-281, l.305-313, l.330-336) ; strates (`window.py` l.50-56) ; population de la médiane leave-one-out (`r1.py` l.149-208) | lus, non modifiés |

### 1.4 Hors périmètre

- τ et σ de BTC (PLAN-S2BIS, versés) ; le pool BTC de 10 unités (l.168), hors l'hôte de l'unité binance, rendu à
  l'orchestrateur (Q-CA-02) ; la carte (l.252-262) ; le seuil de P_j (0,5 %, scellé, l.212) ; la forme d'une seconde vague
  (AQT Q3, tranchée) hors sa calibration (§3.5) ; le rodage ; Pyth.
- Le code des décodeurs (CB-7 à CB-9) et des contrôles (RB-2) : ce G0 leur donne des entrées et des exigences ; le code relève
  de leurs sous-lots et de leurs G2.

### 1.5 Items traités

| item | ce que ce G0 en fait |
|---|---|
| SHOGEN-S2BIS-PAIRES-1 (l.458) | construction : §2 ; fermeture proposée à l'adjudication ; le reste passe à SHOGEN-S2BIS-FORMES-DOC-1 (§13) |
| SHOGEN-S2BIS-SIGMA-ACTIFS-1 (l.457) | règles complètes (§4) ; valeurs par le lot de calcul ; fermeture au versement |
| SHOGEN-S2BIS-CALIB-L189-1 (B.65 l.1086) | contrôles écrits (§5.6) ; RB-2 pour la grille et la formule ; fermeture au commit de RB-2 et au versement |
| SHOGEN-S2BIS-SECONDE-VAGUE-1 (l.460) | dépend d'INV-1 (§3, §9) ; lacune de calibration sous la lecture 2 (§3.5) |
| SHOGEN-S2BIS-LICENCES-API-1 (l.451) | précisé : historiques et hôtes RPC (§3.4, §13) |

## 2. Paires servies et pools

### 2.1 Tableau hôte × paire (PT §1.1, recompté sur les corps de réponse)

| hôte (unité) | ETH | USDC | USDT | recompte du rédacteur |
|---|---|---|---|---|
| binance | `ETHUSD` (USD) et `ETHUSDT` (USDT) | `USDCUSD` (USD) | `USDTUSD` (USD) | `exchangeInfo` de `data-api.binance.vision` : `ETHUSD`, `ETHUSDT`, `USDCUSD`, `USDTUSD`, `USDCUSDT` en `TRADING`, avec leur quote ; `REQUEST_WEIGHT` 6 000 par minute ; `api.binance.com` : HTTP 451, “Service unavailable from a restricted location” |
| coinbase | `ETH-USD` | **absent** | `USDT-USD` | `USDC-USD` : 404 “NotFound” ; 842 produits, dont `USDC-AUD`, `-BRL`, `-CAD`, `-EUR`, `-GBP`, `-INR`, `-SGD`, et `USDT-USDC` |
| kraken | `ETHUSD` (clé de réponse `XETHZUSD`) | `USDCUSD` | `USDTUSD` (clé `USDTZUSD`) | clés de la réponse groupée ; aucun champ d'heure (a, b, c, h, l, o, p, t, v) |
| okx | **absent** (51001) ; `ETH-USDT` servi | **absent** (51001) | `USDT-USD` | 1 144 instruments SPOT, une seule quote USD : `USDT-USD` ; `USDC-USDT` et `ETH-USDT` présents |
| bitstamp | `ethusd` | `usdcusd` | `usdtusd` | corps 200 |
| gemini | `ethusd` | `usdcusd` | `usdtusd` | 348 symboles, dont les trois |
| bitfinex | `tETHUSD` | `tUDCUSD` (code `UDC`) | `tUSTUSD` (code `UST`) | réponse groupée : 4 lignes de 12 éléments ; l'élément 11 est l'heure de la première transaction (2016-03-09, 2018-12-04, 2018-11-27), égale à la première bougie de SH |
| coingecko | `ethereum` | `usd-coin` | `tether` | premier appel 429, second 200 ; `last_updated_at` par actif |
| defillama | `coingecko:ethereum` | `coingecko:usd-coin` | `coingecko:tether` | hôte `coins.llama.fi` (celui de S2, `sources.py` l.269) ; corps vide sur `api.llama.fi` (404 selon PT) |
| chainlink | flux ETH / USD | flux USDC / USD | flux USDT / USD | §2.4 |

### 2.2 Formes proposées par (hôte, actif) : entrées de CB-7 et CB-8

Classe de source = celle de S2 pour l'hôte (`sources.py` l.305-313), parce que la présence d'un horodatage est une propriété de
la forme de requête, inchangée d'un actif à l'autre [inféré].

| unité | classe | ETH | USDC | USDT | horodatage porté, et son sens | devise |
|---|---|---|---|---|---|---|
| binance | sans_horodatage | `ticker/price?symbol=ETHUSDT` (Q-CA-01 a) | `symbol=USDCUSD` | `symbol=USDTUSD` | aucun | USDT pour ETH (comme BTC), USD pour les stables ; hôte : Q-CA-02 |
| coinbase | place_horodatee | `products/ETH-USD/ticker` | — | `products/USDT-USD/ticker` | `time` = heure de la **dernière transaction** : “snapshot information about the last trade (tick)” [lu sur la copie `cb-ticker.md`] ; `USDT-USDC` mesuré à 33 s de la requête [recompté] | USD |
| kraken | sans_horodatage | `Ticker?pair=ETHUSD` | `pair=USDCUSD` | `pair=USDTUSD` | aucun (`c` = dernière transaction) | USD ; une paire par requête : le décodeur de S2 exige une seule clé (`sources.py` l.135-142) |
| okx | place_horodatee | `market/ticker?instId=ETH-USDT` (Q-CA-01 a) | — | `instId=USDT-USD` | `ts` : “Ticker data generation time” [lu sur la copie `okx-docs.html`] | USDT pour ETH, USD pour USDT |
| bitstamp | place_horodatee | `ticker/ethusd/` | `ticker/usdcusd/` | `ticker/usdtusd/` | `timestamp` égal à l'heure de la requête sur les quatre paires sondées, y compris `usdcusdt` au volume de 8 560 sur 24 h : heure de génération [inféré, une mesure] | USD |
| gemini | place_horodatee | `v1/pubticker/ethusd` (forme de S2, `sources.py` l.167-170) | `v1/pubticker/usdcusd` | `v1/pubticker/usdtusd` (non sondé [abs]) | `volume.timestamp` arrondi à la minute (19:29:00 pour un appel à 19:29:2x) : heure de fenêtre [inféré, une mesure] | USD |
| bitfinex | sans_horodatage | groupée `v2/tickers?symbols=tBTCUSD,tETHUSD,tUDCUSD,tUSTUSD` (E-C-09) | même requête | même requête | aucun ; dans la réponse groupée, symbole à l'indice 0 et **dernier prix à l'indice 7** (6 dans `v2/ticker` seul) [recompté] | USD |
| coingecko | agregateur | groupée `simple/price?ids=bitcoin,ethereum,usd-coin,tether&vs_currencies=usd&include_last_updated_at=true` (E-C-09) | même requête | même requête | `last_updated_at` par actif ; rafraîchissement sans clé “publicRate 60 seconds” [lu sur la copie `cg-simple-price.md`] | USD |
| defillama | agregateur | groupée `prices/current/coingecko:bitcoin,coingecko:ethereum,coingecko:usd-coin,coingecko:tether` | même requête | même requête | `timestamp` par actif ; champ `confidence` | USD |
| chainlink | oracle_chainlink | `latestRoundData()` sur le proxy ETH / USD (§2.4) | proxy USDC / USD | proxy USDT / USD | `updatedAt` (4e mot) | USD |

Lectures par hôte et par fenêtre, BTC compris : binance 4, coinbase 3, kraken 4, okx 5 (`BTC-USDT`, index `BTC-USD`,
`ETH-USDT`, `USDT-USD`, témoin `USDC-USDT`), bitstamp 4, gemini 4, bitfinex 1, coingecko 1, defillama 1, chainlink 4 (ou un lot
JSON-RPC, choix de CB-8). OKX est à la limite de cinq lectures séparées (l.236 : 5 + 4 + 10 + 1 = 20 s [calc]) ; sans sixième
forme, aucun regroupement n'est requis (AVIS-C Q-C-10).

### 2.3 Pools par classe (l.173 : « unités = hôtes de la liste du paquet qui servent la paire »)

| classe | unités, ordre des points de code | N | places horodatées | places sans horodatage | agrégateurs | oracle | unités cotées en USDT |
|---|---|---|---|---|---|---|---|
| ETH/USD, Q-CA-01 (a) | binance, bitfinex, bitstamp, chainlink, coinbase, coingecko, defillama, gemini, kraken, okx | 10 | coinbase, okx, bitstamp, gemini | binance, kraken, bitfinex | coingecko, defillama | chainlink | binance, okx |
| ETH/USD, Q-CA-01 (b) | les mêmes sans okx ; binance sur `ETHUSD` | 9 | coinbase, bitstamp, gemini | binance, kraken, bitfinex | coingecko, defillama | chainlink | aucune |
| USDC/USD | binance, bitfinex, bitstamp, chainlink, coingecko, defillama, gemini, kraken | 8 | bitstamp, gemini | binance, kraken, bitfinex | coingecko, defillama | chainlink, borné à 1,05 | aucune |
| USDT/USD | les 10 hôtes | 10 | coinbase, okx, bitstamp, gemini | binance, kraken, bitfinex | coingecko, defillama | chainlink, borné à 1,05 | aucune |

Conséquences :

1. **N ≥ 4 répondantes** : avec 8 à 10 unités, la condition ne dépend plus des agrégateurs et de l'oracle pour USDC/USD (contre
   l.173) ; deux des cinq places d'USDC sont minces (SH l.129 : 6,9 % et 10,9 % de minutes actives en juin) [2nd].
2. **Unité non décalée** (l.200) : binance, première dans l'ordre des points de code, présente dans les trois classes.
3. **Identifiant d'unité** : la même chaîne pour un hôte dans les quatre classes (rotation jointe, l.200 ; contrôle
   `unites-btc`, config l.119) ; la règle `HOTE` (`[a-z0-9.-]`) exclut `okx_ticker` : l'unité est `okx`, comme à l.168.
4. **Cotation** : sous Q-CA-01 (a), l'énoncé d'ETH (l.210) s'applique tel qu'écrit (« un décrochage de l'USDT, qui écarte
   ensemble les unités cotées en USDT, y compte comme co-défaillance de cotation ») ; mais la sensibilité « USD seules » (vii)
   n'est écrite que pour BTC (l.212) : item SHOGEN-S2BIS-ETH-USD-SEULES-1, décision de l'orchestrateur sur une liste fermée
   [ADR].
5. **Sens d'« USDC »** (q. 10) : le dollar réel est porté par les places de la classe USDC/USD ; l'usage DeFi par chainlink
   USDC / USD (borné) et par le témoin sur chaîne ; « leur écart » par l'écart au pair des médianes et par P_j. Aucune forme
   nouvelle n'est requise [inféré, conforme à AVIS-C Q-C-07, l.96].
6. **Règle D1-bis et seuil de flux presque mort** appliqués par classe (l.173), inchangés.

### 2.4 Chainlink (PT §2 ; recompté sur `cl-feeds-mainnet.json`, 300 entrées, et sur la sortie on-chain du lecteur)

| flux (chemin) | proxy lu | agrégateur | seuil | heartbeat | décimales | `maxSubmissionValue` | plancher de τ | σ |
|---|---|---|---|---|---|---|---|---|
| ETH / USD (`eth-usd`) | `0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419` | `0x7d4E7420…6Fb5` | 0,5 | 3 600 s | 8 | aucun plafond (valeur maximale du type) | 0,75 % | 5 400 s |
| USDC / USD (`usdc-usd`) | `0x8fFfFfd4AfB6115b954Bd326cbe7B4BA576818f6` | `0x54bCC589…5b07` | 0,25 | 82 800 s | 8 | `105000000`, soit 1,05 | 0,375 % | 124 200 s |
| USDT / USD (`usdt-usd`) | `0x3E7d1eAB13ad0104d2750B8863b489D65364e32D` | `0x9c41663b…73e3` | 0,25 | 86 400 s | 8 | `105000000`, soit 1,05 | 0,375 % | 129 600 s |
| BTC / USD (contrôle) | `0xF4030086…E88c`, égal à `sources.py` l.224 | `0x4a3411ac…84f1` | 0,5 | 3 600 s | 8 | aucun plafond | — | — |

- Planchers [calc] : 1,5 × 0,5 % = 0,75 % ; 1,5 × 0,25 % = 0,375 % ; 1,5 × 3 600 = 5 400 ; 1,5 × 82 800 = 124 200 ; 1,5 × 86 400 =
  129 600. Égaux à l.188 et aux constantes de config l.28-29 (`TAU_ORACLES`, `SIGMA_ORACLES`) [recompté]. L'unité « pourcent »
  du champ `threshold` est [inféré] (PT l.59) ; `data.chain.link` n'a pas été lu (429, PT l.75) [abs].
- Variantes SVR : la variante `usdc-usd-svr` porte un heartbeat de 86 400 s, différent des 82 800 s du proxy principal
  [recompté] ; lire deux proxies pour une unité poserait la question du heartbeat. Proposition : le seul proxy principal
  (Q-CA-08).
- `stablecoinCapped` est absent du JSON ; la page `docs.chain.link` copiée le porte 158 fois, à `true` ; son rattachement à
  chaque flux n'a pas été vérifié par le rédacteur [2nd, PT l.72]. Le plafond utile est `maxSubmissionValue`, lu dans le JSON.
- Âges à la lecture du 2026-10-08 : 480 s, 14 184 s (3,9 h), 17 784 s (4,9 h) [recompté]. Les `roundId` d'USDC/USD et d'USDT/USD
  sont en phase 4 aux tours 26 et 25 (ETH : phase 7, tour 34 445) [calc sur les valeurs] : à un tour au moins par heartbeat,
  leurs agrégateurs auraient au plus 25 à 26 jours [inféré] ; des paramètres récemment changés peuvent changer encore
  (E-CA-10).

### 2.5 Témoin (entrées de CB-9 ; l.174)

| pièce | lecture | orientation | hôte proposé | état |
|---|---|---|---|---|
| OKX `USDC-USDT` | `market/ticker` : `last`, `ts` (ms, génération) | USDT par USDC | `www.okx.com` (5e forme d'OKX) | servi [recompté] |
| Uniswap v3 USDC/USDT, palier 0,01 %, `0x3416cF6C708Da44DB2624D63ea0AAef7113527C6` | `slot0()` (`0x3850c7bd`) ; prix = (sqrtPriceX96 / 2^96)² ; token0 = USDC, token1 = USDT, 6 décimales chacun | USDT par USDC | `eth.drpc.org` (Q-CA-10) | fabrique `0x1F98431c…F984` lue sur la page officielle des déploiements [2nd] ; prix 1,000669 recalculé depuis sqrtPriceX96 [calc] ; palier le plus profond (liquidity 3,09·10^16 contre 2,01·10^14 au palier 0,05 %) [recompté] |
| Curve 3pool `0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7` | `get_dy(1, 2, 10^6)` (`0x5e0d443f`) ; coins = DAI, USDC, USDT | USDT par USDC, net des frais | `rpc.mevblocker.io` (Q-CA-10) | Q-CA-09 ; documentation de `get_dy` du 3pool non lue [abs] |
| Curve NG `0x4f493B7dE8aAC7d55F71853688b1F7C8F0243C85` (remplaçant proposé) | `get_dy(0, 1, 10^6)` ; coins = USDC, USDT | USDT par USDC, net des frais | même hôte que la pièce Curve retenue | soldes 0,70 M USDC et 4,31 M USDT [recompté] ; rattachement à la fabrique NG non vérifié [abs] |

Les trois pièces lues sont toutes en « USDT par USDC » (E-CA-11). Chaque lecture sur chaîne passe par son propre hôte RPC,
distinct de celui de Chainlink (l.174) : deux hôtes, un pour Uniswap, un pour Curve.

### 2.6 Ce que l'adjudication débloque, et ce qui attend

| sous-lot | débloqué à l'adjudication | attend |
|---|---|---|
| CB-7 (places ETH, USDC, USDT) | formes du §2.2, devises, classes, sens de l'horodatage, indices de Bitfinex, clés de Kraken ; fixtures capturées depuis l'hôte de session (forme de Q-C-05, AVIS-C l.94), celles de binance depuis `data-api.binance.vision` (même chemin, même forme), déclarées (E-CA-08) | Q-CA-01, Q-CA-02 ; SHOGEN-S2BIS-FORMES-DOC-1 avant le gel de `formes.json` |
| CB-8 (agrégateurs ; Chainlink) | identifiants CoinGecko et clés DefiLlama groupés ; trois proxies, décimales 8, plafond 1,05 pour USDC et USDT, aucun pour ETH | Q-CA-08 ; relecture des paramètres au paquet (E-CA-10) |
| CB-9 (témoin) | OKX `USDC-USDT` ; adresses et sélecteurs Uniswap ; orientation | Q-CA-09, Q-CA-10 ; SHOGEN-S2BIS-CURVE-DOC-1 si le 3pool est retenu |
| RB-2 (configuration d'analyse) | contrôles du §5.6 : grille de 0,05 % des τ des agrégateurs et des places hors BTC, formule de τ des agrégateurs, σ des agrégateurs, planchers exacts des oracles, mode « planchers seuls » | Q-CA-05, Q-CA-06, Q-CA-15 |
| lot de calcul CA-0 à CA-6 | code sur fixtures synthétiques | exécution : réponse à INV-1 (A, A′ ou C), G2, épinglage au JOURNAL |

## 3. Historiques : la condition « au moins 4 places par classe »

### 3.1 Ce que SH établit, sur les places des pools du §2.3 et la paire lue

| classe | places du pool avec historique gratuit, sans clé, à une minute (SH §3) | sans historique | deuxième trimestre 2026 | conditions d'usage (SH §3, §3.5, §6) |
|---|---|---|---|---|
| ETH (Q-CA-01 a) | binance `ETHUSDT` (2017-08 et après), coinbase (2016-05), kraken (2015-08, jusqu'au 2026-06-30), okx `ETH-USDT` (2021-01), bitstamp (au plus tard 2017-09), bitfinex (2016-03) : **6** | gemini (24 h seulement) | couvert pour les six | lues : binance (CC BY-NC-SA 4.0), bitstamp (redistribution sous contrat commercial signé), kraken et okx (conditions générales restrictives ; application à l'archive [inféré par SH]) ; non lues : coinbase (403), bitfinex (corps non servi) |
| USDC | binance `USDCUSD` (2025-11), kraken (2020-01, jusqu'au 2026-06-30), bitstamp (au plus tard 2020-11 ; 97 % de minutes à volume nul dans l'échantillon du 2026-08-15), bitfinex (2018-12 ; 4 % de minutes actives du 10 au 17 août 2026) : **4** | gemini | couvert | lues : binance, kraken, bitstamp ; non lue : bitfinex |
| USDT | binance `USDTUSD` (2025-11), coinbase (2021-05), kraken (2017-03, jusqu'au 2026-06-30), okx `USDT-USD` (2024-12), bitstamp (au plus tard 2021-07 ; mince), bitfinex (2018-11) : **6** | gemini | couvert | lues : binance, kraken, okx, bitstamp ; non lues : coinbase, bitfinex |

Sous Q-CA-01 (b), ETH compte 5 places : binance y passe sur `ETHUSD` (depuis 2026-03 ; 90,2 % de minutes à volume nul en août
2026 ; 2 289 minutes actives sur 10 080 la semaine du 8 juin, SH l.45, l.111), et okx sort du pool.

### 3.2 Les lectures de la condition (l.186, l.191 ; AQT Q3)

| lecture | ce qu'elle exige | ETH (F2, au moins 4) | USDC (F3, au moins 3, sinon planchers seuls) | USDT (F3) | conséquence |
|---|---|---|---|---|---|
| 1a « disponibilité » | historique public, gratuit, sans clé, à une minute, antérieur à la campagne | 6 : remplie | 4 : remplie | 6 : remplie | les quatre actifs scellés ensemble (q. 9) ; calcul par le lot CA |
| 1b « disponibilité, conditions lues » (variante) | 1a, et conditions d'usage lues, quel qu'en soit le contenu | 4 (binance, kraken, okx, bitstamp) sous Q-CA-01 (a) : remplie sans marge ; 3 sous (b) : non remplie | 3 (binance, kraken, bitstamp) : remplie pour F3 | 4 : remplie | comme 1a, sur moins de places ; sous Q-CA-01 (b), ETH en seconde vague |
| 2 « republication des octets bruts permise » | permission lue de republier les fichiers, sans contrat | 0 : non remplie | 0 : planchers seuls | 0 : planchers seuls | ETH en seconde vague (paquet-2), stables à τ des places = 0,375 % ; contredit « les 4 ensemble » |

- Sous la lecture 2, le compte est nul : Binance ne permet la republication que sous CC BY-NC-SA 4.0, donc sans usage commercial
  (SH l.91-93, art. 3.1, 3.4, 4.5) ; Bitstamp, que sous un contrat commercial signé (SH l.48) [2nd].
- SH l.183 propose que la lecture « disponibilité » vaille si seul le τ dérivé est publié, les octets bruts étant référencés
  par URL et sha256 [inféré par SH] ; c'est une décision qui engage une licence et le calendrier : elle est rendue à
  l'investisseur (brief), non tranchée ici.

### 3.3 Ce qui est technique, ce qui revient à l'investisseur

- **Technique** (ce G0, l'advisor, l'orchestrateur) : fenêtre (Q-CA-03) ; population et N_min (Q-CA-04) ; « dernier prix
  connu » ; recalcul par un tiers **par référence** (manifeste URL, taille, sha256, date ; E-CA-13) ; aucun octet d'historique
  réel au dépôt, quelle que soit la lecture (fixtures synthétiques, E-CA-05).
- **Investisseur** : INV-1 (utiliser sans republier ; n'utiliser que des données republiables ; acheter une licence) et INV-2
  (usage commercial ; avis juridique). Les conditions lues ne restreignent pas que la republication : elles restreignent aussi
  l'**usage** (Binance, art. 3.4 : “any commercial utilization requires a separate, written enterprise data license
  agreement” ; OKX, art. 9.4 : usage “for any commercial purpose” interdit sans autorisation ; Kraken : “must seek prior
  permission”) [2nd, SH l.47, l.50, l.92]. La lecture 1a n'est donc pas sans risque juridique.

### 3.4 Couplage avec SHOGEN-S2BIS-LICENCES-API-1 et la réponse à la q. 13

- Les mêmes conditions (Kraken, OKX, Binance, Coinbase, Bitfinex) régissent les réponses en direct que la mesure journalise et
  publie ; elles sont lues avant le sceau (l.175, l.451) ; une source qui interdit la republication est retirée (q. 13). Un
  retrait parmi les 7 hôtes AS13335 change la cellule cible et fait rejouer SIM-NIVEAU-BIS et SIM-PUISSANCE-BIS (l.374).
- La réponse à INV-1 ne tranche pas ce point, mais une lecture 2 pour les historiques annoncerait, par cohérence, une lecture
  stricte pour le pool [inféré].
- Proposé : avant INV-1, faire lire par un lecteur, avec un outil qui exécute le JavaScript (connecteur Firecrawl, CLAUDE.md
  §7), les conditions de Coinbase et de Bitfinex, que SH n'a pas pu lire (SH l.125).

### 3.5 Lacune sous la lecture 2 : une seconde vague d'ETH n'a pas de source de calibration écrite

AQT Q3 (l.77) met τ et σ d'ETH dans le paquet-2 et tient « hors inférence » les lectures entre T_début_1 et T_début_2. Mais
(i) les historiques sont exclus par la même lecture ; (ii) calibrer sur des lectures de S2-bis avant le rendu exposerait des
statuts de source de S2-bis (D.2-bis, l.228), et les pannes d'ETH sont celles de BTC sur les mêmes hôtes (l.162) [inféré].
Item SHOGEN-S2BIS-VAGUE2-CALIB-1 : décision de l'orchestrateur avant toute seconde vague.

## 4. Règles de calcul proposées

### 4.1 Fenêtre et strates

- **Fenêtre** : du 2026-04-01 00:00 UTC (1775001600) inclus au 2026-07-01 00:00 UTC (1782864000) exclu : 91 jours, 131 040
  minutes [calc]. Motifs : dernier trimestre couvert par toutes les places à historique, Kraken compris (archive arrêtée au
  2026-06-30, `Kraken_OHLCVT_2026Q3.zip` en 404 le 2026-10-04, SH l.47) ; antérieur à S2-bis, donc disjoint ; contient la
  semaine du 2026-06-08 au 2026-06-15 de SH §4, qui sert d'oracle d'exécution (E-CA-15).
- **Strates** : calendrier de S2, stress = samedi et dimanche UTC (`window.py` l.50-56, jours 5 et 6, lundi = 0) ; 26 jours de
  stress (37 440 minutes), 65 jours de calme (93 600 minutes) [calc].
- **Descriptif** : le mois de septembre 2026, sans Kraken, imprimé à côté, jamais décisif (Q-CA-03).

### 4.2 Séries de bougies

- Une série par (place, paire lue), sur la grille des minutes de la fenêtre : clôture et volume. Minute **active** = volume > 0
  (définition de SH l.101). Minute absente = sans échange (l.189, [inféré par AQT]) : Coinbase “No data is published for
  intervals where there are no ticks”, Kraken “gaps are not zero-filled”, Bitfinex : minutes absentes [2nd, SH]. Minute
  reportée de Bitstamp (volume 0) = sans échange.
- **Dernier prix connu** c_p(t) = clôture de la dernière minute active au plus tard en t ; **âge** a_p(t) = nombre de minutes
  écoulées depuis elle (0 si t est active). c_p est indéfini avant la première minute active de la place dans la fenêtre (pas
  de préchauffe).
- Formats (SH §3) : Binance, CSV de 12 colonnes, temps en **microsecondes** depuis 2025, clôture en colonne 4 ; Kraken, CSV
  `timestamp, open, high, low, close, volume, trades` en secondes ; OKX, CSV avec en-tête, temps en ms ; Coinbase, JSON
  `[time, low, high, open, close, volume]` en secondes (clôture en colonne 4) ; Bitstamp, JSON en chaînes, secondes ; Bitfinex,
  `[MTS, OPEN, CLOSE, HIGH, LOW, VOLUME]` en ms (clôture en **colonne 2**). Les deux ordres de colonnes sont des pièges testés.
- Arithmétique exacte : Decimal lu depuis les chaînes, rapports et produits en Fraction, aucun flottant.

### 4.3 τ des places (l.187), un par actif

1. **Population** (transposition de l.180 et de `r1.classify_ecart`, `r1.py` l.149-208) : cellules (t, p), p parmi les places
   de la classe à historique, c_p(t) défini, au moins N_min places définies en t (N_min = 4 ; 3 pour F3 quand la classe n'a
   que 3 places) ; sont exclues les cellules d'une place dont l'horodatage est celui de la dernière transaction (Coinbase) quand
   60·a_p(t) > σ(actif, place_horodatee) (60·a_p(t) est la borne basse de l'âge, la transaction tombant dans la minute
   active ; déclaré) : dans la campagne, elles seraient des écarts de staleness, qui précède l'hors-enveloppe. La médiane leave-one-out m_p(t) est celle des c_q(t) définis, q ≠ p, cellules exclues comprises (r1 passe
   les prix des autres répondantes, staleness comprise).
2. **Écart relatif** e = |c_p(t) − m_p(t)| / m_p(t) (ADR-0020 déc. 2 ; `sources.py` l.338-341 ; `r1.py` l.195-208) ; m ≤ 0 :
   refus nommé.
3. **Règle** : P99,9 par strate au rang ⌈999·N/1000⌉ (`regles.py` l.12-16), maximum sur les deux strates (comme l.181),
   multiplié par 1,5, grid-ceil au pas g = 0,05 % (Q-CA-05), borne basse 0,05 % (premier multiple, avec drapeau), borne haute
   2,85 % exclue : refus nommé de la classe, décision de l'orchestrateur avant le sceau (l.183 ; `regles.py` l.19-36).
4. Une valeur par actif, appliquée aux deux classes de places de l'actif (`place_horodatee` et `sans_horodatage`).
5. **Descriptifs**, jamais décisifs : variante « minutes actives seules » (SH l.113) ; nombre de cellules au-delà du P99,9 par
   place ; fenêtre de septembre 2026 ; valeur de la règle au maximum (1,5 × maximum), comme pour BTC (l.181).

### 4.4 τ des agrégateurs (l.189), un par actif

- τ_agr(actif) = grid-ceil(τ_places(actif) × τ_agr_BTC / τ_places_BTC, 0,05 %), 0,05 % ≤ τ < 2,85 % (refus nommé en haut), τ
  de BTC pris dans `tau_sigma.txt` (re-dérivés au P99,9, jamais les τ committés de S2, l.189).
- **τ_places_BTC = maximum de τ_BTC(place_horodatee) et de τ_BTC(sans_horodatage)** (Q-CA-06) : les bougies donnent un τ
  unique pour les deux classes de places de l'actif ; le τ unique de places de BTC qui couvrirait ses deux classes serait le
  plus grand des deux [inféré]. Choix fait sans ouvrir les valeurs de BTC (E-6, §15).
- Imprimés à côté : les valeurs sous les autres dénominateurs (horodatée, sans horodatage, minimum) et τ_agr_BTC « tel quel »
  (l.189).
- τ de BTC absent ou refusé pour une de ces classes : refus nommé, aucun τ_agr ; décision de l'orchestrateur.
- La valeur est exacte (« planchers seuls », l.189) et se vérifie dans RB-2 depuis `analyse.json` (E-CA-23 d).

### 4.5 τ des oracles

- τ_oracle(actif) = 1,5 × seuil de déviation, **exactement** : 0,75 % (ETH), 0,375 % (USDC, USDT) [calc] ; jamais arrondi à la
  grille (0,375 % vaut 7,5 pas de 0,05 %) ; « planchers seuls » (l.189).
- Paramètres relus au paquet, datés (E-CA-10) ; égalité exigée à config l.28 et à l.188 ; sinon refus et décision de
  l'orchestrateur avant le sceau, jamais une valeur devinée.

### 4.6 σ, par actif et par classe de source

| classe | règle | termes connus | terme à calculer |
|---|---|---|---|
| place_horodatee | max(30 s, σ_BTC(place_horodatee), grid-ceil(3 × P99 de la durée sans échange, 60 s)), maximum sur les strates (l.189) | 30 s ; σ_BTC (PLAN-S2BIS) | troisième terme : population et statistique, Q-CA-07 |
| sans_horodatage | nul : staleness non évaluable (`sources.py` l.333 ; config l.21, l.86) | — | aucun |
| agregateur | max(300 s, σ_BTC(agregateur)) (l.189 : « les deux premiers termes seuls ») | 300 s ; σ_BTC | aucun |
| oracle_chainlink | 1,5 × heartbeat : 5 400 s, 124 200 s, 129 600 s (au moins 5 400 s) | heartbeat relu au paquet | aucun |

**Troisième terme** (recommandation de Q-CA-07) : population = places de la classe dont l'horodatage est celui de la
dernière transaction, soit Coinbase `ETH-USD` pour ETH et `USDT-USD` pour USDT ; aucune pour USDC : terme absent, σ(USDC,
place_horodatee) = max(30 s, σ_BTC(place_horodatee)). Statistique : P99 sur les cellules (t, p) de d_p(t) = nombre de minutes
consécutives sans échange qui finissent en t (0 si t est active), au rang ⌈99·N/100⌉, par strate, maximum sur les strates,
fois 3 fois 60 s, grid-ceil à 60 s ; le P99 sur les suites elles-mêmes est imprimé à côté. σ se calcule avant τ, qui en dépend
(§4.3 pt 1) ; aucune circularité.

### 4.7 Grille et mode « planchers seuls »

- **Grille** g = 0,05 % pour τ des places et τ des agrégateurs des quatre actifs (Q-CA-05). Les planchers restent des valeurs
  exactes : 0,375 % hors grille n'est admis qu'à deux endroits, la classe oracle d'USDC et d'USDT, et le mode « planchers
  seuls ».
- **Mode « planchers seuls »** (F3 seulement : lecture 2, ou condition non remplie pour un stable) : τ des deux classes de
  places = 0,375 % (AQT Q3, précision citée à l.191) ; τ_agr par la formule du §4.4 appliquée à ce τ, et σ des places
  horodatées = max(30 s, σ_BTC), sans troisième terme [inféré : AQT ne fixe que τ des places]. Déclaré au paquet.
- RB-2 reconnaît le mode sans champ nouveau : un τ de places égal à 0,375 % est hors de la grille de 0,05 %, donc ne peut venir
  que du mode (Q-CA-15).

### 4.8 Ce qui se calcule avant le sceau, et ce qui ne le peut pas

| grandeur | quand | sur quoi | état |
|---|---|---|---|
| planchers de τ et σ des oracles | maintenant | paramètres lus le 2026-10-08 (PT ; recomptés), relus au paquet | calculés ici [calc] |
| σ des agrégateurs ; σ des places sans troisième terme (USDC) | dès l'adjudication de Q-CA-06 et Q-CA-07 | sorties de PLAN-S2BIS | lot CA, sans historique |
| troisième terme de σ, τ des places | après INV-1 et l'épinglage | bougies du deuxième trimestre 2026 | lot CA |
| τ des agrégateurs | après τ des places | τ des places et τ de BTC | lot CA |
| contrôles de cohérence | dès RB-2 | `analyse.json` | RB-2 |
| cadence des agrégateurs par actif | avant le sceau, en option | horodatages seuls, hôte de session (Q-CA-11) | CA-6, option |
| τ et σ observés de S2-bis ; cadence vue des observateurs ; dérive de régime | jamais avant le sceau | données de S2-bis | imprimés au rendu, descriptifs (l.184, l.190) |
| tout prix, toute staleness, tout hors-enveloppe du rodage | jamais | rodage (l.192, l.224) | interdit |

## 5. Exigences numérotées

### 5.1 Cadre et frontière

| n° | exigence (testable) | rattachement |
|---|---|---|
| E-CA-01 | Code sous `scripts/calib-actifs/` (README, `parametres.json`, `socle.py`, `acquerir.py`, `bougies.py`, `sigma.py`, `tau.py`, `lancer.sh`, `SHA256SUMS`, `tests/`) ; sorties sous `docs/adr-0029/calib-actifs/` ; bibliothèque standard seule (R-8 sans objet) ; aucun fichier de `s2-harness/`, `s2bis/`, `scripts/plan-s2bis/` modifié (contrôle sur la liste des chemins de chaque diff) | patron de PLAN-S2BIS ; Q-CA-13 |
| E-CA-02 | Frontière : aucun journal de S2 ni de S2-bis lu, aucune extraction de `f35a70c` ; entrées : historiques publics (§4), `tau_sigma.txt` par chemin et sha256 (`409b2a5e…e6d9`), paramètres Chainlink relus | l.179, l.383 ; annexe D |
| E-CA-03 | Refus si `SHOGEN_S2_CAMPAGNE_CONTROL` est posée, au lanceur et au socle ; aucun test ne la pose, sauf celui du lanceur à une valeur fictive dans son seul sous-processus | règle 3 de la fiche ; forme d'E-P2-05 |
| E-CA-04 | En tête de chaque sortie, mot pour mot : « préparation de S2-bis ; calibration d'ETH, d'USDC et d'USDT sur historiques publics ; ne lit aucune donnée de S2 ni de S2-bis » ; aucune heure, aucun hôte, aucune version dans une valeur | forme du G0 de PLAN-S2BIS |
| E-CA-05 | Hygiène : `TMPDIR` dans le dossier de travail ; partiels `.partiel` puis renommage ; 0 octet 92 dans les fichiers du lot ; aucun octet d'historique réel au dépôt (fixtures synthétiques seulement) | B.16 ; §3.3 |

### 5.2 Pools, formes, témoin (entrées de CB-7 à CB-9)

| n° | exigence (testable) | rattachement |
|---|---|---|
| E-CA-06 | Pools du §2.3 selon Q-CA-01 ; une même chaîne par hôte dans les quatre classes, ordre des points de code ; fragment `unites` pour `analyse.json` | l.173, l.200 ; config l.118-119 |
| E-CA-07 | Formes du §2.2 transmises à CB-7 et CB-8 : (hôte, actif) donne point d'accès, symbole, devise, classe de source, sens de l'horodatage (dernière transaction, génération, fenêtre, aucun) avec sa pièce ; un sens [inféré] est établi à CB-7, par une page citée ou par deux captures d'une paire mince où l'horodatage suit l'heure de requête quand le prix ne change pas | PROP-C l.215-216 ; E-C-08 |
| E-CA-08 | Fixtures de CB-7 capturées depuis l'hôte de session (forme de Q-C-05) ; celles de binance depuis `data-api.binance.vision`, même chemin et même forme, déclarées, tant que `api.binance.com` répond 451 | AVIS-C l.94 ; PT l.37 |
| E-CA-09 | Chainlink : un seul proxy lu par actif (§2.4) ; décimales 8 et plafond (1,05 pour USDC et USDT, aucun pour ETH) portés par la forme (E-C-10) ; variantes SVR jamais lues | l.173 ; PROP-C l.171 ; Q-CA-08 |
| E-CA-10 | Paramètres Chainlink relus au paquet, datés (seuil, heartbeat, décimales, `maxSubmissionValue`, adresse de l'agrégateur) ; égalité exigée au §2.4, sinon refus nommé et décision de l'orchestrateur avant le sceau ; un changement de phase de `roundId` pendant la campagne est imprimé en descriptif, jamais un re-réglage | l.184 ; Q-CA-08 |
| E-CA-11 | Témoin : trois pièces en « USDT par USDC » ; Uniswap `slot0` du palier 0,01 % ; Curve selon Q-CA-09 ; chaque lecture sur chaîne par son hôte RPC, distinct de celui de Chainlink et de l'autre ; remplaçants écrits d'avance (q. 12) | l.174 ; JOURNAL l.382 ; Q-CA-09, Q-CA-10 |

### 5.3 Historiques : sources, acquisition, contrôles

| n° | exigence (testable) | rattachement |
|---|---|---|
| E-CA-12 | Sources et paires du §3.1 pour la lecture adjugée (INV-1) ; fenêtre du §4.1 ; la liste exacte (place, paire, URL, format, pièce de SH qui la fonde) est dans `parametres.json` | SH §3 ; l.186 |
| E-CA-13 | Acquisition, étape réseau séparée du calcul : fichiers mensuels de Binance (2026-04 à 2026-06) contrôlés contre leur fichier `.CHECKSUM` ; archive Kraken du deuxième trimestre lue par plages ; fichiers mensuels d'OKX ; Coinbase, Bitstamp et Bitfinex par pages, débit sous les limites lues (Coinbase 3 requêtes par seconde au plus ; Bitfinex 30 par minute au plus) ; manifeste versé (URL, date, taille, sha256) ; octets bruts hors dépôt | SH §3 ; PT l.45-50 |
| E-CA-14 | Contrôle d'octets : les trois CSV de Kraken (ETH, USDC, USDT) extraits par le lot ont les sha256 de SH l.156-158 (`65298120…`, `e6494645…`, `db584f24…`) ; sinon refus | SH l.156-158 |
| E-CA-15 | Oracle d'exécution, avant toute valeur : sur ses séries, le lot recompte les minutes actives de la semaine du 2026-06-08 au 2026-06-15 et les compare à SH §4 : par place, USDC 9 998 (binance), 9 551 (kraken), 693 (bitstamp), 1 098 (bitfinex) ; USDT bitstamp 1 542 ; et les concurrences : ETH (coinbase, kraken, bitstamp, bitfinex) 9 799 minutes à au moins 4 actives ; USDC 76, 1 626 et 9 565 à au moins 4, 3 et 2 ; USDT (six places) 10 031 à au moins 4. Un écart : refus nommé, aucune valeur | SH l.103-111 |
| E-CA-16 | Normalisation du §4.2 : minute absente = sans échange ; microsecondes de Binance ; colonne de clôture par format ; aucune bougie hors fenêtre ; minute en double : refus | SH §3 ; l.189 |

### 5.4 Calcul

| n° | exigence (testable) | rattachement |
|---|---|---|
| E-CA-17 | Ordre : σ (§4.6), puis τ des places (§4.3), puis τ des agrégateurs (§4.4) ; oracles (§4.5) | §4 |
| E-CA-18 | Arithmétique exacte : Decimal depuis les chaînes ; Fraction pour rapports et produits ; rangs ⌈999·N/1000⌉ et ⌈99·N/100⌉ ; grid-ceil en rationnels | `regles.py` l.12-36 |
| E-CA-19 | Refus nommés plutôt qu'écrêtage : borne haute (l.183), médiane ≤ 0, classe sous N_min, τ de BTC absent ou refusé | l.183 |
| E-CA-20 | Descriptifs du §4.3 pt 5, du §4.4 et du §4.6 imprimés à part ; aucune valeur décisive n'en dépend (test : les retirer ne change aucun octet du fragment) | brief, item 4 |
| E-CA-21 | Déterminisme : `PYTHONHASHSEED` 0 et 1, Python 3.11 à 3.13, sorties égales à l'octet ; deux passes A et B dans le lancement | forme d'E-P2-17, E-P2-18 |

### 5.5 Sorties

| n° | exigence (testable) | rattachement |
|---|---|---|
| E-CA-22 | `calib_actifs.txt` (par actif et par classe : τ, σ, chaque terme, N par strate, P99,9 et P99 par strate, drapeaux, refus, descriptifs) ; `fragment_analyse.json` (`tau_sigma` et `unites` d'ETH, d'USDC et d'USDT) ; `manifeste.tsv` ; README ; `SHA256SUMS`. Complété par un bloc BTC synthétique, le fragment passe `config.charger` (test) | config l.125-141 |

### 5.6 Contrôles côté recalcul (RB-2 ; SHOGEN-S2BIS-CALIB-L189-1)

Tous resserrent la configuration d'analyse ; aucun ne la desserre.

| n° | exigence (testable) | rattachement |
|---|---|---|
| E-CA-23 | (a) τ des agrégateurs de chaque actif sur la grille de 0,05 % ; (b) τ des places hors BTC sur la grille g, ou exactement 0,00375 pour USDC et USDT (mode « planchers seuls ») ; (c) τ des oracles hors BTC égal au plancher (0,0075 ; 0,00375), non plus seulement supérieur ou égal ; (d) τ_agr(actif) égal à grid-ceil(τ_places(actif) × τ_agr(BTC) / max(τ des deux classes de places de BTC), 0,05 %), recalculé depuis `analyse.json` ; (e) σ_agr(actif) égal à σ_agr(BTC) ; (f) σ des oracles égal à 1,5 × heartbeat (5 400 ; 124 200 ; 129 600) ; (g) σ nul pour les places sans horodatage (déjà, config l.86) ; (h) τ égal pour les deux classes de places d'un actif hors BTC. Refus `ANALYSE/incoherent` nommé par règle ; tests et mutants dans RB-2 | B.65 l.1086 ; config l.68-122 ; l.187, l.189 |

### 5.7 Refus nommés du lot (E-CA-24)

| code | cause | où |
|---|---|---|
| CA/usage | arguments du lanceur (code 2) | lanceur |
| CA/variable | `SHOGEN_S2_CAMPAGNE_CONTROL` posée | lanceur ; socle |
| CA/sortie | dossier de sortie non vide | lanceur |
| CA/epingle | `SHA256SUMS` du code différent de l'argument ; `sha256sum -c` en échec | lanceur |
| CA/plan-s2bis | sha256 de `tau_sigma.txt` différent de l'épingle | socle |
| CA/acquisition | téléchargement impossible ; `.CHECKSUM` de Binance différent (code 4) | `acquerir.py` |
| CA/kraken | sha256 d'un CSV de Kraken différent de SH (E-CA-14) | `acquerir.py` |
| CA/format | ligne illisible, colonne absente, temps hors fenêtre, minute en double | `bougies.py` |
| CA/oracle-sh | compte de SH §4 différent (E-CA-15) | `bougies.py` |
| CA/population | classe sous N_min dans une strate | `tau.py` |
| CA/mediane | médiane leave-one-out ≤ 0 | `tau.py` |
| CA/borne | valeur de la règle à 2,85 % ou au-delà (l.183) | `tau.py` |
| CA/btc | τ de BTC absent ou refusé pour une classe du dénominateur | `tau.py` |
| CA/chainlink | paramètres relus différents du §2.4 | socle |
| CA/identite | passes A et B différentes (code 5) | lanceur |

Codes du lanceur : 0 (tout en 0, A = B), 2 usage, 3 refus avant tout lancement, 4 acquisition impossible, 5 calcul hors 0 ou
A ≠ B. Un refus nomme le code, l'actif, la classe et la strate, jamais une valeur.

### 5.8 Épinglage, exécution, versement

| n° | exigence (testable) | rattachement |
|---|---|---|
| E-CA-25 | Aucune statistique de dispersion n'est calculée ni affichée sur les historiques avant l'épinglage, par aucun agent ; SH n'a calculé que des comptes (SH l.9) | l.186 « avant tout calcul » ; Q-CA-14 |
| E-CA-26 | Répétition sur bougies synthétiques à l'échelle (131 040 minutes, six places), durée et mémoire mesurées | forme d'E-P2-20 |
| E-CA-27 | Épinglage au JOURNAL (sha256 de chaque fichier du lot et de son `SHA256SUMS`) après la G2 et la réponse à INV-1 ; le lanceur reçoit l'épingle en argument | SHOGEN-POSTPREREG-PARAMS-SCEAU-1 (B.58) |
| E-CA-28 | Exécution unique, détachée, par l'orchestrateur (`setsid nohup`, PID et fichier de sortie consignés, fin constatée en sondant le PID) ; un second lancement est une déviation déclarée ; un lancement coupé par une borne de temps se refait et ne se compte pas | B.16 ; forme d'E-P2-22, E-P2-23 |
| E-CA-29 | Versement : sorties, manifeste, README, G1 et G2 dans `docs/adr-0029/calib-actifs/` ; bloc d'annexe B ; ligne JOURNAL ; le fragment entre à `analyse.json` au lot du paquet, par l'orchestrateur, avec les valeurs de BTC | §6 lot 9 de l'ADR |
| E-CA-30 | Exposition : sorties lisibles par les rôles frais du paquet, dont elles sont le contenu ; aucune donnée de S2-bis n'existe | l.228 |

### 5.9 Tests

| n° | exigence (testable) | rattachement |
|---|---|---|
| E-CA-31 | Tests d'abord, sur fixtures synthétiques ; valeurs de référence indépendantes du code (à la main, `sha256sum`, `date -u -d`, `regles.quantile` épinglé) ; rouge montré avant le vert ; une mutation nommée par test | règle 4 de la fiche |
| E-CA-32 | Mutants classés par la sortie du runner : 0 vivant, 1 tué, 3 ou toute autre sortie FATAL, campagne relancée après correction | SHOGEN-MUT-FATAL-1 (B.16) |
| E-CA-33 | Suite `scripts/calib-actifs` verte à chaque sous-lot ; suites `s2bis`, `scripts/plan-s2bis`, `s2-harness` inchangées et vertes | règle 4 de la fiche |

## 6. Sous-lots, tests attendus, mutants

### 6.1 Sous-lots (≤ 200 lignes ajoutées chacun, tests et données compris)

| sous-lot | objet | taille | dépend de |
|---|---|---|---|
| CA-0 | socle : `parametres.json` (fenêtre, strates, places et paires par classe et par lecture, formats, grille, bornes, facteurs, rangs, N_min, épingle de `tau_sigma.txt`), `socle.py` (garde de la variable, schéma, refus, CLI, en-tête, `.partiel`) ; tests | ≈ 190 | — |
| CA-1 | `acquerir.py` I : fichiers (Binance et `.CHECKSUM`, OKX, Kraken par plages), manifeste ; tests sans réseau (serveur local de fichiers synthétiques) | ≈ 190 | CA-0 |
| CA-2 | `acquerir.py` II : API paginées (Coinbase, Bitstamp, Bitfinex), débit borné, reprise ; tests | ≈ 170 | CA-0 |
| CA-3 | `bougies.py` : six lecteurs de formats, normalisation, dernier prix connu, âges, oracle de SH §4 ; tests | ≈ 190 | CA-0 |
| CA-4 | `sigma.py`, `tau.py` I : troisième terme, σ par classe, population de τ, médiane leave-one-out ; tests | ≈ 190 | CA-3 |
| CA-5 | `tau.py` II : quantiles, maximum sur les strates, grille, bornes ; τ des agrégateurs ; oracles ; sorties et fragment ; tests | ≈ 180 | CA-4 |
| CA-6 | `lancer.sh` (épingle en argument, étape réseau puis calcul, passes A et B, sommes) ; tests du lanceur ; identité ; option : cadence des agrégateurs (Q-CA-11) | ≈ 190 | CA-1 à CA-5 |

Total ≈ 1 100 à 1 300 lignes [inféré], par analogie avec un réalisé : PLAN-S2BIS, 1 477 lignes en 9 diffs (g0-plan2 l.58)
[2nd]. Côté RB-2, ≈ 80 à 120 lignes pour E-CA-23, dans ses propres sous-lots et sa G2. Une seule partie pour le lot de calcul,
une G2 neuve à 100 % à la fin.

### 6.2 Tests attendus (fixtures synthétiques seulement ; valeurs de référence indépendantes du code)

| test | valeur de référence | mutant qu'il doit tuer |
|---|---|---|
| T-CA-SOC-1 épingle | sha256 de `tau_sigma.txt` par `sha256sum` ; un octet altéré dans une copie : CA/plan-s2bis | M-CA-01 contrôle retiré |
| T-CA-SOC-2 variable | environnement passé en argument avec la variable : CA/variable ; sans : aucun refus | M-CA-02 garde retirée |
| T-CA-FEN-1 fenêtre | 1775001600 (mercredi 2026-04-01 00:00 UTC) inclus, 1782864000 exclu ; 131 040 minutes ; 37 440 en stress, 93 600 en calme ; 1775260800 (samedi 2026-04-04) en stress ; 1775433600 (lundi 2026-04-06) en calme [calc] | M-CA-03 jour pris en heure locale ; M-CA-04 borne haute incluse |
| T-CA-FMT-1 Binance | deux lignes synthétiques à 1775001600000000 µs et à 1775001600000 ms donnent la même minute ; clôture en colonne 4 | M-CA-05 microsecondes lues en millisecondes |
| T-CA-FMT-2 colonnes | Bitfinex `[MTS, OPEN, CLOSE, HIGH, LOW, VOLUME]` : clôture en colonne 2 ; Coinbase `[time, low, high, open, close, volume]` : clôture en colonne 4 | M-CA-06 colonne de Coinbase prise pour Bitfinex |
| T-CA-FMT-3 minutes vides | minute absente chez Kraken ; minute reportée à volume 0 chez Bitstamp : non actives | M-CA-07 minute reportée comptée active |
| T-CA-SER-1 dernier prix | actives en 0, 1 et 4, clôtures 10, 11 et 14 : c(2) = c(3) = 11, âges 1 et 2 ; indéfini avant la première active | M-CA-08 âge compté depuis le début de la fenêtre |
| T-CA-TAU-1 médiane | quatre places à 100, 101, 102 et 110 en t : pour 110, médiane des autres 101, écart 9/101 ; pour 100, médiane 102, écart 2/102 [calc à la main] | M-CA-09 médiane qui inclut la place |
| T-CA-TAU-2 N_min | trois places définies, N_min = 4 : minute exclue | M-CA-10 N_min = 3 |
| T-CA-TAU-3 exclusion | Coinbase à l'âge de 4 minutes, σ de 180 s : cellule exclue de la population, gardée dans la médiane des autres | M-CA-11 cellule retirée aussi des médianes |
| T-CA-Q-1 rang | N = 1 000 : rang 999 ; N = 1 001 : rang 1 000 [calc] ; égal à `regles.quantile` épinglé | M-CA-12 rang par troncature |
| T-CA-G-1 grille | 1,5 × 0,00123 = 0,001845 donne 0,0020 ; 1,5 × 0,0002 donne 0,0005 sans drapeau ; 0 donne 0,0005 avec drapeau ; 0,0280 donne 0,0280 ; 0,02801 et 0,0285 : refus [calc] | M-CA-13 arrondi au plus proche ; M-CA-14 borne haute incluse |
| T-CA-AGR-1 agrégateurs | valeurs synthétiques (non celles de BTC) : τ_places 0,0010, τ_agr_BTC 0,0265, classes de places de BTC 0,0045 et 0,0050 : dénominateur 0,0050, produit 0,0053, τ_agr 0,0055 ; avec le minimum, 0,0060 [calc] | M-CA-15 minimum des deux classes |
| T-CA-ORA-1 oracles | seuils 0,5 % et 0,25 % : 0,0075 et 0,00375 (hors grille admis) ; heartbeats 3 600, 82 800, 86 400 : 5 400, 124 200, 129 600 [calc] ; égaux à config l.28-29 | M-CA-16 plancher arrondi à la grille (0,0040) |
| T-CA-SIG-1 troisième terme | une strate de 212 minutes : 100 fois (active, sans échange), puis active, 10 minutes sans échange, active ; d sur les 212 cellules : P99 au rang 210 = 8, donc 3 × 8 × 60 = 1 440 s ; sur les 101 suites, P99 au rang 100 = 1, donc 180 s [calc] | M-CA-17 P99 sur les suites au lieu des cellules |
| T-CA-SIG-2 classe sans dernière transaction | USDC : terme absent, σ = max(30 s, σ_BTC) | M-CA-18 terme pris sur bitstamp |
| T-CA-SIG-3 sans horodatage | σ nul | M-CA-19 σ = 30 s |
| T-CA-ORX-1 oracle de SH | séries synthétiques d'une semaine aux comptes connus ; un compte altéré : CA/oracle-sh | M-CA-20 contrôle retiré |
| T-CA-KRA-1 Kraken | fichier synthétique et sa somme par `sha256sum` ; un octet altéré : CA/kraken | M-CA-21 contrôle retiré |
| T-CA-FRG-1 fragment | complété par un bloc BTC synthétique, chargé par `config.charger` ; un τ_agr décalé d'un pas : refus côté RB-2 (après E-CA-23) | M-CA-22 fragment non contrôlé |
| T-CA-DET-1 identité | deux exécutions, `PYTHONHASHSEED` 0 et 1 : sorties égales à l'octet | M-CA-23 itération sur un ensemble |
| T-CA-LAN-1 à 6 lanceur | épingle, sortie non vide, variable, acquisition impossible (4), A ≠ B (5), usage (2) | M-CA-24 à M-CA-29, un contrôle retiré par mutant |

## 7. Oracles

1. **Vecteurs à la main** : T-CA-FEN-1, T-CA-TAU-1, T-CA-G-1, T-CA-AGR-1, T-CA-ORA-1, T-CA-SIG-1.
2. **`scripts/plan-s2bis/regles.py`, épinglé** : `quantile` est une fonction pure (l.12-16) ; `regle_tau` dépend du contexte
   décimal de `r1` par `commun` (l.29) : ses vecteurs passent par un fichier relu des deux côtés, et par un passage du réviseur
   G2 sur une copie où `commun` se charge (Q-CA-13).
3. **SH §4**, comptes produits par d'autres scripts (`window.py`, `conc.py` du lecteur de SH), contrôlés à l'exécution
   (E-CA-15) ; **sha256 de SH** pour Kraken (E-CA-14) et fichiers `.CHECKSUM` de Binance (E-CA-13).
4. **config** : constantes des planchers (l.28-29) et chargeur (T-CA-FRG-1).
5. **Chainlink** : JSON de la documentation (`feeds-mainnet.json`) ; `decimals()` et `description()` on-chain au smoke.

## 8. Questions techniques (adjudication : orchestrateur ; avis : advisor)

- **Q-CA-01 Cotation d'ETH chez binance et okx.** (a) USDT, comme BTC : binance `ETHUSDT`, okx `ETH-USDT` ; pool ETH de 10
  unités ; l.98 l'anticipe (« et de leurs flux ETH s'ils sont cotés de même ») et l'énoncé d'ETH nomme la co-défaillance de
  cotation (l.210) ; marché profond ; OKX à cinq formes, sans regroupement. (b) USD seul : binance `ETHUSD` (90,2 % de minutes à
  volume nul en août 2026, SH l.45), okx hors du pool : 9 unités ; au « dernier prix connu », les clôtures périmées de binance
  élargiraient la queue de τ_places(ETH) [inféré]. (c) mélange (binance USDT, okx hors) : incohérent avec BTC. **Recommandé :
  (a)**, avec l'item SHOGEN-S2BIS-ETH-USD-SEULES-1. Advisor ; [ADR] pour la seule sensibilité.
- **Q-CA-02 Hôte de l'unité binance.** `api.binance.com` répond 451 depuis l'hôte de session (EP l.74, 2026-10-04 ; PT l.37,
  2026-10-08 [recompté]) ; `data-api.binance.vision` est documenté “market data only” [2nd, PT l.44], même chemin et même
  forme. L'unité est l'hôte (l.168) : changer d'hôte change l'unité BTC du pool confirmatoire et sa mesure ASN. (a) Garder
  `api.binance.com` pour les quatre classes (continuité ; l.81 : un observateur bloqué est remplacé avant le sceau) ; fixtures
  depuis `data-api.binance.vision`, déclarées (E-CA-08). (b) Passer à `data-api.binance.vision` pour les quatre classes :
  perd la continuité de S2, ASN inconnu [abs]. (c) Un hôte par classe : rejeté (unité = hôte, rotation jointe). **Recommandé :
  (a)** ; si aucun emplacement d'observateur n'atteint `api.binance.com` au smoke, décision de l'orchestrateur avant le sceau.
  Orchestrateur ; [G0-C] (formes de CB-6).
- **Q-CA-03 Fenêtre des historiques.** (a) Deuxième trimestre 2026, fixée ici ; (b) la fenêtre la plus récente avant le calcul
  (sans Kraken : USDC tombe à 3 places, dont deux minces) ; (c) une règle « dernier trimestre complet publié à la date du
  calcul » (dépend de l'heure du calcul). **Recommandé : (a)**, septembre 2026 imprimé en descriptif (§4.1). Advisor.
- **Q-CA-04 Population de τ des places.** (a) « dernier prix connu », sans plafond d'âge, sauf exclusion des cellules d'une
  place à horodatage de dernière transaction au-delà de σ ; médiane des autres places définies ; N_min = 4 (3 pour F3 à trois
  places) ; maximum sur les strates ; (b) minutes actives seules (SH l.113 : 76 minutes par semaine à 4 places actives pour
  USDC, SH l.107) ; (c) dernier prix avec un âge plafonné (paramètre d'échelle de la nature de ℓ). **Recommandé : (a)**, (b)
  imprimée. Motif : c'est ce que lit un ticker (le dernier prix de la dernière transaction), et c'est la population de BTC
  (l.180 ; `r1.py` l.149-208). Advisor.
- **Q-CA-05 Grille g de τ des places hors BTC** (l.186 : « grille fixée au G0 »). (a) 0,05 %, comme BTC (l.181) et les
  agrégateurs (l.189) ; la borne basse 0,05 % en est le premier pas ; (b) 0,01 % pour les stables (finesse au-dessus de 0,05 %
  seulement) ; (c) 0,025 % (rend 0,375 % multiple). **Recommandé : (a)** ; planchers exacts hors grille, aux deux endroits du
  §4.7. Limite écrite : sur les stables, le pas de la grille (5·10⁻⁴) ne vaut que cinq fois le pas de cotation de Coinbase
  (10⁻⁴, d'après la forme des prix mesurés) [inféré]. Advisor.
- **Q-CA-06 Dénominateur de la formule de τ des agrégateurs** (l.189 : « τ_places_BTC », alors que BTC a deux classes de
  places). (a) horodatée ; (b) sans horodatage ; (c) maximum des deux ; (d) minimum ; (e) un τ de places de BTC poolé, calculé
  à neuf sur les journaux de S2 (protocole d'exception, coût). **Recommandé : (c)**, (a), (b) et (d) imprimés. Choix fait sans
  ouvrir `tau_sigma.txt` ; le rédacteur a vu les P99 observés de S2 imprimés par l'ADR (l.43), déclaré (§15). Advisor ; [ADR]
  (lecture d'une lettre ambiguë, SHOGEN-S2BIS-CALIB-L189-1).
- **Q-CA-07 Troisième terme de σ des places horodatées : population et statistique.** Population : (a) lettre, toutes les
  places horodatées de la classe à historique ; (b) les seules places dont l'horodatage est celui de la dernière transaction
  (Coinbase) ; (c) toutes les places de l'actif. Sous (a), le terme d'USDC viendrait du seul bitstamp (97 % de minutes à volume
  nul dans l'échantillon, SH l.62), dont l'horodatage ne vieillit pas avec l'inactivité : il aveuglerait l'axe staleness de
  bitstamp et de gemini sans motif [inféré]. Statistique : (i) P99 sur les cellules (pondéré par le temps, comme le P99 de
  staleness de BTC sur des cellules) ; (ii) P99 sur les suites (lettre « durée des suites »). **Recommandé : (b) et (i)**, (a) et
  (ii) imprimés. Advisor ; [ADR] (lecture de l.189).
- **Q-CA-08 Chainlink.** Un seul proxy principal par actif (variantes SVR non lues : « fusionnées en une unité », l.173, lu
  comme « jamais deux lectures pour une unité ») ; paramètres relus au paquet et égalité exigée (E-CA-10) ; phase de `roundId`
  imprimée. **Recommandé : oui.** Orchestrateur ; [G0-C] (CB-8).
- **Q-CA-09 Pool Curve du témoin.** (a) 3pool (≈ 159,8 M $ selon l'API Curve [2nd, PT l.97] ; ancien pool à trois jetons ;
  documentation de `get_dy` non lue [abs]) ; (b) pool NG « Strategic USD Reserves » (≈ 5,0 M $ ; déséquilibré, 0,70 M USDC
  pour 4,31 M USDT [recompté] ; documentation NG lue ; rattachement à la fabrique non vérifié [abs]). **Recommandé : (a)**,
  après lecture sur pièce de la documentation de `get_dy` du 3pool (SHOGEN-S2BIS-CURVE-DOC-1), (b) en remplaçant écrit
  d'avance (q. 12). Orchestrateur ; [G0-C] (CB-9).
- **Q-CA-10 Hôtes RPC du témoin.** Deux lectures sur chaîne, donc deux hôtes, distincts de `ethereum-rpc.publicnode.com`
  (l.174), et non trois (PT l.124) ; proposition : Uniswap par `eth.drpc.org`, Curve par `rpc.mevblocker.io` (réponses
  `eth_call` le 2026-10-08 [recompté]) ; `ethereum.publicnode.com` écarté (même éditeur que l'hôte de Chainlink) ;
  `eth-mainnet.public.blastapi.io` écarté (“Blast has been deprecated” [2nd, PT l.111]) ; remplaçant écrit d'avance :
  `mainnet.gateway.tenderly.co` (accès public sans clé documenté [2nd, PT l.112] ; 429 depuis l'adresse partagée de la
  session), essayé au smoke des observateurs. Limites et conditions des hôtes RPC non lues [abs] ; les quatre hôtes
  répondants de 2026-10-04 étaient sur AS13335 (EP l.171, l.190) [2nd]. **Recommandé : la proposition.** Orchestrateur ;
  [G0-C] (CB-9).
- **Q-CA-11 Cadence des agrégateurs par actif** (l.189 : « à contrôler au G0 » ; AQT l.60). Établi : un rafraîchissement sans
  clé documenté pour la page (“publicRate 60 seconds”) ; `last_updated_at` et `timestamp` par actif ; une mesure de chaque.
  (a) S'en tenir là, déclaré ; (b) mesurer les seuls horodatages (aucun prix gardé) depuis l'hôte de session, par exemple 120
  lectures sur 2 h, et imprimer la loi des intervalles entre `last_updated_at` distincts, par actif ; conséquence écrite
  d'avance : une cadence d'actif plus lente que celle de BTC devient une limite écrite au paquet, et une décision de
  l'orchestrateur avant le sceau, jamais un σ deviné. **Recommandé : (b)**, en option de CA-6. Advisor.
- **Q-CA-12 Bruit de P_j sur des historiques.** AQT l.95 : seuil de 0,5 % « à confirmer sur l'historique de CALIB-ACTIFS » ;
  l.212 : le rejeu des décrochages est le test public du seuil. Les historiques des paires stable/stable n'ont pas été relevés
  par SH [abs]. **Recommandé : hors de ce lot**, renvoyé au G0 de REJEU-DECROCHAGES (item SHOGEN-S2BIS-PJ-BRUIT-1) ; le seuil
  scellé ne change pas. Orchestrateur.
- **Q-CA-13 Réemploi de `regles.py`.** `regles.regle_tau` dépend de `commun` et du contexte décimal du harnais extrait
  (`regles.py` l.29) : l'importer entraînerait l'extraction de `f35a70c`. **Recommandé : réimplémentation** dans
  `scripts/calib-actifs/` (≈ 20 lignes, même rang, même grid-ceil en rationnels, mêmes bornes et drapeaux), croisée avec
  `regles.quantile` et un fichier de vecteurs (§7 pt 2). Orchestrateur.
- **Q-CA-14 Épinglage et aveuglement.** Même protocole que PLAN-S2BIS (code et paramètres épinglés au JOURNAL avant toute
  acquisition et tout calcul), sans extraction de `f35a70c` ; aucune statistique de dispersion sur les historiques avant
  l'épinglage (E-CA-25) ; l'exposition du lecteur de SH (comptes, fractions à volume nul) est déclarée. **Recommandé : oui.**
  Orchestrateur.
- **Q-CA-15 Mode « planchers seuls » dans `analyse.json`.** (a) Un champ de mode par actif (change le schéma) ; (b)
  reconnaissance sans champ : un τ de places égal à 0,00375 est hors de la grille de 0,05 %, il ne peut venir que du mode.
  **Recommandé : (b).** Orchestrateur ; [G0-C] (RB-2).

**Advisor** : Q-CA-01, -03, -04, -05, -06, -07, -11 ; **orchestrateur seul** : Q-CA-02, -08, -09, -10, -12, -13, -14, -15.

## 9. Questions à l'investisseur (en langage clair ; aucune n'est tranchée ici)

**INV-1 — Peut-on régler les seuils d'ETH, d'USDC et d'USDT sur des prix passés publics, sans republier ces fichiers ?**
(licence et calendrier)

Pour régler les seuils des trois actifs ajoutés, il faut les prix minute par minute du passé, sur au moins quatre places par
actif (trois suffisent pour les stablecoins). Ils existent, gratuits et sans compte, chez Coinbase, Kraken, Bitstamp,
Bitfinex, Binance et OKX. Mais aucune place n'autorise clairement à republier ces fichiers tels quels : Binance seulement pour
un usage non commercial, Bitstamp seulement avec un contrat commercial signé ; Kraken et OKX ont des conditions générales
restrictives ; celles de Coinbase et de Bitfinex n'ont pas pu être lues.

- **Option A** : calculer sur ces fichiers sans les republier. Nous publierions leurs adresses, leurs empreintes et les seuils
  obtenus ; un tiers pourrait retélécharger les mêmes fichiers et refaire le calcul tant que les places les servent. Les quatre
  actifs restent scellés ensemble, comme vous l'avez choisi le 4 octobre, sans délai au-delà de ce qui est prévu. Risque :
  un usage qui pourrait être jugé contraire aux conditions de certaines places (voir INV-2).
- **Option A′** : la même chose, avec les seules places dont les conditions ont été lues (Binance, Kraken, OKX, Bitstamp) :
  quatre places pour ETH et USDT, trois pour USDC, ce qui suffit si l'ETH est lu contre l'USDT chez Binance et OKX, comme le
  Bitcoin (sinon trois places pour ETH, ce qui ne suffit pas). Le risque se réduit aux conditions connues, qui restent
  restrictives.
- **Option B** : n'utiliser que des données qu'on a le droit de republier. Aucune place ne le permet sans contrat : ETH passe
  dans une seconde mesure scellée à part (location des serveurs prolongée, de l'ordre de 26 à 52 € HT pour 2 à 4 semaines
  selon l'avis de l'advisor, dates et méthode de réglage encore à écrire), et USDC et USDT reçoivent des seuils par défaut.
  Cela défait votre choix « les 4 ensemble ».
- **Option C** : demander une licence (contrat de données commercial de Bitstamp, licence entreprise de Binance). Coût et délai
  inconnus ; personne n'est contacté sans votre accord.

Le rédacteur ne recommande pas d'option : la question est juridique et engage le calendrier.

**INV-2 — Faut-il traiter Shōgen comme un « usage commercial » au sens de ces conditions ?**

Binance (licence non commerciale) et OKX (usage commercial interdit sans autorisation) excluent l'usage commercial de leurs
données sans licence. La même question touchera les prix que la mesure lira en direct sur ces places pendant la campagne : les
conditions de chaque source seront lues avant le scellement, et une source qui interdit la republication sera retirée, selon
votre réponse du 4 octobre. Si vous ne savez pas, voulez-vous un avis juridique (une dépense) avant le scellement ?

**Information I-1 — calendrier.** Sous A ou A′, le calcul prend une à deux journées de travail des agents après votre réponse,
en parallèle des autres préparations ; le scellement reste prévu vers le 13 ou le 20 décembre 2026 (préparation de 11 à 12
semaines, déjà annoncée) [inféré].

**Information I-2 — USDC.** Cinq places cotent USDC contre le dollar (et non trois, comme écrit en octobre) : Binance, Kraken,
Bitstamp, Gemini et Bitfinex ; Coinbase n'a toujours pas ce marché ; deux places sont très peu actives ; Gemini n'a pas
d'historique mais sera mesurée en direct.

## 10. Écarts à la lettre, signalés et non appliqués

| où | lettre | écart constaté ou proposé | question |
|---|---|---|---|
| l.173, l.214, l.416 | USDC/USD : « trois places liquides » contre le dollar fiat ; N ≥ 4 « dépend des agrégateurs et de l'oracle » | cinq places servent USDC/USD (binance `USDCUSD` depuis 2025-11, kraken, bitstamp, gemini, bitfinex), quatre avec historique, deux minces | constat ; ajout daté proposé à l'adjudication |
| l.189 | « τ_places_BTC », une valeur | BTC a deux classes de places : maximum des deux | Q-CA-06 |
| l.189 | troisième terme « par actif », population et statistique non dites | places à horodatage de dernière transaction ; P99 sur les cellules | Q-CA-07 |
| l.187 | τ des places « par actif », strates non dites | maximum sur les strates, comme l.181 | Q-CA-04 |
| l.188 | « l'axe staleness des stables ne voit qu'un battement manqué de plus de 12 h » | 11,5 h pour USDC (heartbeat de 82 800 s), 12 h pour USDT [calc] | constat |
| l.310 | « CALIB-ACTIFS ≈ 200 » lignes | ≈ 1 100 à 1 300, plus ≈ 80 à 120 dans RB-2 | §6.1 |
| AQT l.95 | seuil de P_j « à confirmer sur l'historique de CALIB-ACTIFS » | renvoyé au rejeu des décrochages (l.212) | Q-CA-12 |
| PT l.124 | « trois hôtes distincts, hors celui de Chainlink » | deux (Uniswap, Curve) | Q-CA-10 |
| config l.81 | grille contrôlée pour BTC seul | grille pour tous les actifs, planchers exacts | E-CA-23 |

## 11. Calendrier

| étape | contenu | durée [inféré] |
|---|---|---|
| 0 | avis de l'advisor ; adjudication ; INV-1 et INV-2 posées par l'orchestrateur ; lecture des conditions de Coinbase et de Bitfinex par un lecteur, outil JavaScript (§3.4) | 1 à 2 h, plus le délai de l'investisseur |
| 1 | dès l'adjudication, en parallèle : CB-7, CB-8, CB-9 (partie P2 du collecteur) ; RB-2 (E-CA-23) | leurs propres sous-lots et G2 |
| 2 | CA-0 à CA-6, worker `claude-opus-5-5` effort max ; G2 neuve à 100 % ; corrections ; commits | 3 à 5 h de session |
| 3 | après INV-1 (A, A′ ou C) : épinglage, acquisition et calcul détachés, versement | ≈ 1 h [calc : Coinbase 437 requêtes par paire à 3 par seconde, ≈ 2,5 min ; Bitstamp 132 par paire ; Bitfinex 14 par paire ; Kraken par plages] |
| 4 | fragment à `analyse.json` au lot du paquet, avec les valeurs de BTC | au paquet |

Le sceau est prévu à S+10/11 depuis l'acceptation du 2026-10-04, soit vers le 2026-12-13 ou le 2026-12-20 [calc ; ajout daté
l.397]. Le lot CA n'est pas sur le chemin critique [inféré] ; le décalage d'une à deux semaines de l.191 reste un maximum, non
consommé. Sous l'option B d'INV-1 : dates et chiffrage de la seconde vague à fixer (SHOGEN-S2BIS-SECONDE-VAGUE-1) et méthode
de calibration à écrire (§3.5).

## 12. Risques

1. **Conditions d'usage** : l'usage, non seulement la republication, est restreint (§3.3) ; couplage avec les sources en direct
   du pool (§3.4). Parade : INV-1, INV-2, lecture des conditions manquantes avant la réponse.
2. **Marchés minces et dernier prix connu** : sur USDC, la queue de τ peut venir des clôtures périmées de bitstamp et de
   bitfinex. Parade : contributions par place et variante « minutes actives » imprimées ; limite écrite au paquet.
3. **Dérive de régime** du deuxième trimestre 2026 à la campagne : déclarée (l.190) ; septembre 2026 imprimé à côté.
4. **Paramètres de Chainlink** changés avant le sceau (relus, E-CA-10) ou pendant (phase imprimée) ; agrégateurs d'USDC et
   d'USDT récents (§2.4) [inféré].
5. **Binance** : 451 depuis l'hôte de session ; le smoke de chaque observateur tranche (l.81).
6. **Témoin** : deux hôtes RPC, tous deux sur AS13335 au 2026-10-04, conditions non lues, remplaçant non essayé ; une panne d'hôte
   ôte une voix (voulu, AQT l.98).
7. **Sens des horodatages** inféré pour Bitstamp et Gemini (une mesure chacun) : Q-CA-07 en dépend (E-CA-07).
8. **Taille** : ≈ 1 100 à 1 300 lignes contre ≈ 200 annoncées ; SHOGEN-S2BIS-P1-ESTIMATION-1 reçoit le chiffre mesuré.

## 13. Items (règle PAROXYSME)

| item | constat | construction | déclencheur |
|---|---|---|---|
| SHOGEN-S2BIS-PAIRES-1 (existant, l.458) | paires lues sur pièce et recomptées (§2) | ce G0 ; fermeture proposée à l'adjudication | adjudication |
| SHOGEN-S2BIS-SIGMA-ACTIFS-1 (existant, l.457) | règles complètes, valeurs à calculer | lot CA | versement |
| SHOGEN-S2BIS-CALIB-L189-1 (existant, B.65 l.1086) | contrôles de l.189 écrits (E-CA-23) | RB-2 et lot CA | commit de RB-2 ; versement |
| SHOGEN-S2BIS-SECONDE-VAGUE-1 (existant, l.460) | dépend d'INV-1 ; sous A, A′ ou C, aucune seconde vague | — | réponse à INV-1 |
| SHOGEN-S2BIS-LICENCES-API-1 (existant, l.451) | précisé : conditions des archives (Binance Vision, Bitstamp, Kraken, OKX lues ; Coinbase, Bitfinex non lues) et des hôtes RPC (non lues) | lecteur, outil JavaScript ; INV-1, INV-2 | avant INV-1 ; avant le sceau |
| SHOGEN-S2BIS-FORMES-DOC-1 (neuf) | champs de réponse de Gemini non documentés dans les pages lues ; Gemini v1 `usdtusd` non sondé ; codes `UDC` et `UST` de Bitfinex non cités sur une page ; hôte `coins.llama.fi` absent de la documentation lue (BTC compris) ; limites publiques de Kraken non trouvées | CB-7, CB-8 | gel de `formes.json` |
| SHOGEN-S2BIS-HORODATAGE-SENS-1 (neuf) | sens de l'horodatage par forme : documenté pour Coinbase et OKX, inféré d'une mesure pour Bitstamp et Gemini | E-CA-07, à CB-7 | avant le lancement du lot CA |
| SHOGEN-S2BIS-BINANCE-HOTE-1 (neuf) | `api.binance.com` en 451 depuis l'hôte de session ; fixtures depuis `data-api.binance.vision` ; hôte de l'unité | Q-CA-02 ; smoke des observateurs | avant le sceau |
| SHOGEN-S2BIS-TEMOIN-RPC-1 (neuf) | deux hôtes RPC, AS13335, conditions et limites non lues, remplaçant non essayé | Q-CA-10 ; smoke | avant le sceau |
| SHOGEN-S2BIS-CURVE-DOC-1 (neuf) | documentation de `get_dy` du 3pool non lue ; rattachement du pool NG non vérifié ; sens de `price_oracle` non lu | lecteur | avant CB-9 |
| SHOGEN-S2BIS-CHAINLINK-PARAMS-1 (neuf) | unité du seuil inférée ; `data.chain.link` non lu (429) ; `stablecoinCapped` non rattaché par flux par le rédacteur ; agrégateurs récents | E-CA-10 | paquet |
| SHOGEN-S2BIS-ETH-USD-SEULES-1 (neuf) | la sensibilité « USD seules » n'est écrite que pour BTC ; sous Q-CA-01 (a), ETH porte deux unités cotées en USDT | décision de l'orchestrateur [ADR] | avant le sceau |
| SHOGEN-S2BIS-VAGUE2-CALIB-1 (neuf, conditionnel) | sous la lecture 2, la seconde vague d'ETH n'a pas de source de calibration écrite (§3.5) | décision de l'orchestrateur | INV-1 = B |
| SHOGEN-S2BIS-PJ-BRUIT-1 (neuf, si Q-CA-12 adoptée) | bruit de P_j sur historiques stable/stable non mesuré | G0 de REJEU-DECROCHAGES | ce G0 |
| SHOGEN-S2BIS-P1-ESTIMATION-1 (existant, B.61) | s'applique : ≈ 200 contre ≈ 1 100 à 1 300 lignes | une ligne à la clôture | clôture du lot |

Aucune limite rencontrée n'est laissée sans item.

## 14. Critères de sortie

1. **Par sous-lot** : suite `scripts/calib-actifs` verte, plancher relevé ; suites `s2bis`, `scripts/plan-s2bis` et
   `s2-harness` inchangées ; mutants conformes au contrat du runner ; hook, gate des secrets et `cargo --locked xtask verify`
   verts (lignes de verdict) ; journal G1 ; ligne JOURNAL.
2. **Lot** : G2 neuve à 100 % (réviseur différent du générateur) ; corrections rouges avant, vertes après ; contrôle FM-1.1 ;
   répétition (E-CA-26) ; épinglage (E-CA-27) ; un lancement au code 0, A = B ; oracles d'exécution passés (E-CA-14, E-CA-15) ;
   versement (E-CA-29) ; bloc d'annexe B ; items du §13 formés ou fermés.
3. **G0** : avis de l'advisor ; adjudication ; réponses à INV-1 et INV-2 avant l'exécution (pas avant le code) ; ajout daté
   à l'ADR pour les constats du §10 si l'orchestrateur le retient.
4. **Suite** : CB-7, CB-8, CB-9 sur les entrées du §2 ; RB-2 avec E-CA-23 ; fragment à `analyse.json` au paquet.

## 15. Provenance

**Pièces lues dans le dépôt** [lu] (sha256 à `5cfe746`) :
- ADR-0029 (`35563d8f…9eb8`, 571 lignes), en entier, par plages.
- `DECISIONS-ARCHITECTURE-S2BIS.md` (`603abda2…1920`), `AVIS-QUESTIONS-TECHNIQUES-V3.md` (`836ece5e…c79d`), `ETUDE-POOL-BIS.md`
  (`d3780f13…e11e`), `G0-lots-S2BIS.md` (`db49d5f2…00a3`), SH (`f649e30f…73cf`), en entier ; `SHA256SUMS-ECHANTILLONS.txt`
  (`988534f0…b5fb`) : 20 premières lignes et décompte par dossier.
- G0 de collecte : `PROPOSITION.md` l.1-60, l.160-240, l.296-335 et lignes trouvées par `grep` ; `AVIS.md` l.85-110 et lignes
  trouvées par `grep` ; `G0-COLLECTE-RECALC-DEPLOI.md` (`0e9001f3…2a90`) en entier.
- Forme : `g0-plan2/PROPOSITION.md` (`4b3107a7…1749`) l.1-135, l.300-449, l.505-660 et titres ; `g0-sim/PROPOSITION.md`
  (`0e78afab…9dd6`) l.1-80 et titres.
- Annexe B (`3f738722…d0d2`) : lignes contenant « CALIB » par `grep` ; l.838-852 ; l.1072-1087 ; titres B.51 à B.67. Annexe D
  (`deb64179…0eaf`) : titres par `grep`, puis l.32-47 (liste D.2, noms seulement) ; aucune pièce de D.2 ouverte.
- Code : config (`82abdba5…8b26`) en entier ; `analyse.json` (`e9243c79…1d00`) ; `sources.py` (`0c81fc33…afe4`) l.100-195,
  l.196-345 ; `window.py` (`f8c3b79f…fb94`) lignes trouvées par `grep` ; `r1.py` (`c5666e8d…7a4b`) l.149-209 ;
  `scripts/plan-s2bis/regles.py` (`a0140188…88a6`) l.12-36 ; `scripts/plan-s2bis/tau_sigma.py` : lignes trouvées par `grep`
  (définitions, rang) ; `G0-lot-PLAN-S2BIS.md` (`81bf3f33…b5ad`) en entier ; `docs/adr-0029/plan-s2bis/README.md` : titre seul.
- `JOURNAL.md` (`a833dd7a…aff7`) : l.380 et l.382 seules, après un comptage du mot « pocket » sur chacune (0).

**Pièces lues hors du dépôt** [lu] : le brief (`0714e2a4…ee34`) ; `BRIEF-LECTEUR-PAIRES.md` (`3863ee7e…4c1a`) et
`BRIEF-AVIS-CALIB.md` (`558915f2…56d8`) ; PT (`fe884dec…943e`) et les notes du lecteur (`07e25c7c…b5aa`), en entier.

**Recomptes** [recompté, 2026-10-08 entre 19:50 et 20:04 UTC], sur les copies brutes du lecteur, par `python3 -I` sans
installation, scripts passés en entrée standard (aucun fichier de script écrit) : liste des produits Coinbase, relevé SPOT
d'OKX et ses trois réponses 51001, `exchangeInfo` de Binance, symboles Gemini, réponse groupée Kraken, réponses Bitfinex
(groupée et seule), CoinGecko, DefiLlama, horodatages de Bitstamp, Gemini, Coinbase et OKX, journal de sondes, sortie RPC,
sortie on-chain Chainlink, Uniswap et Curve, `feeds-mainnet.json` (`bb3cf35e…b8df`, 300 entrées), données embarquées de la
page `docs.chain.link` (motif `stablecoinCapped`), copies des pages Coinbase, OKX et CoinGecko (phrases citées). Empreinte de
l'ensemble des 46 fichiers : `cd calib2 && sha256sum probes/*.body probes/*.txt web/cl-feeds-mainnet.json
web/cg-simple-price.md web/okx-docs.html web/cb-ticker.md web/cl-addr-eth.html | sort -k2 | sha256sum` donne `c8459312…e00c`.
Intégrité des échantillons de SH : `sha256sum -c` du fichier versé depuis `scratchpad/s2bis/calib/` : 148 OK ; résumé
`window/concurrence.txt` (comptes seulement), égal à SH l.103-111.

**Calculs** [calc, jamais sur un historique ; `python3 -I` en entrée standard, de 20:00 à 20:30 UTC] : dates et strates de la
fenêtre ; planchers des oracles ; vecteurs de grille, de rang et du troisième terme (T-CA-SIG-1, suite synthétique) ; prix
Uniswap depuis sqrtPriceX96 ; phases des `roundId` ; budget de temps d'OKX ; dates du sceau (S+10, S+11). Vérifiables sur la
page : 1,5 × 82 800 = 124 200 ; 1,5 × 86 400 = 129 600 ; 91 × 1 440 = 131 040 ; 26 × 1 440 = 37 440 ; 65 × 1 440 = 93 600 ;
131 040 / 300 = 436,8, soit 437 requêtes ; ⌈99 × 212 / 100⌉ = 210 ; ⌈99 × 101 / 100⌉ = 100.

**Non ouverts** : `docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`,
`docs/adr-0028/monark-m009a/`, `docs/adr-0028/execution/`, tout `*.jsonl`, toute pièce de D.2 ; `tau_sigma.txt` (valeurs de BTC,
volontairement, E-6) ; le reste du JOURNAL ; les séries de `scratchpad/s2bis/calib/window/` et `samples/` (sha256 seulement) ;
rien sur Pocket. Aucune recherche récursive, aucun Glob ; `ls` de dossiers nommés seulement. `SHOGEN_S2_CAMPAGNE_CONTROL` jamais
posée. Aucune requête réseau du rédacteur.

**Exposition** : valeurs de S2 post-rendu portées par l'ADR §1.1 et §1.2 (z, K, P̂_more, FIV ; P99 observés par classe de
S2, l.43) ; prix instantanés du 2026-10-08 dans PT ; comptes et fractions à volume nul de SH. Aucune donnée de S2-bis n'existe.
Aucune valeur re-dérivée de BTC vue.

**Écarts du rédacteur** :
- **E-1** : barres obliques inverses tapées dans 16 commandes, contre la consigne de gabarit (B.16) : 15 commandes de lecture
  (motifs `grep` et expressions régulières de deux scripts Python en entrée standard), dont les faits sont recoupés par une
  autre lecture (lignes relues par `sed` ou `Read`, valeurs relues par analyse JSON), dont la quatorzième a corrigé trois
  renvois de ce document (`sources.py` l.333, `r1.py` l.208, `regles.py` l.29) et dont la quinzième, un contrôle de ces
  renvois, n'a rien trouvé (recoupé par un comptage Python) ; une commande d'écriture (changement des
  guillemets des citations anglaises de ce document, un saut de ligne écrit en échappement dans le script) : octets écrits
  contrôlés, 0 octet 92, 13 paires de guillemets anglais, chacune relue. Ce document et les notes sont contrôlés à 0 octet 92
  (NOTES).
- **E-2** : pièces lues hors de la liste du brief, pour les exigences et les recomptes : code (config, `analyse.json`,
  `sources.py`, `window.py`, `r1.py`, `regles.py`, `tau_sigma.py` par `grep`), `G0-lot-PLAN-S2BIS.md`, JOURNAL l.380 et l.382,
  annexe D l.32-47, copies brutes du lecteur, intégrité des échantillons de SH.
- **E-3** : le brief ne nomme pas de base ; base relevée `5cfe746`.
- **E-4** : `NOTES.md` existait (notes du lecteur) : une section du rédacteur y est **ajoutée**, rien n'est écrasé.
- **E-5** : un fichier temporaire `calib2/.recompte-tmp` (liste de sha256 des copies du lecteur) a été écrit puis effacé vers
  20:03 UTC, hors des deux fichiers permis.
- **E-6** : `tau_sigma.txt` non ouvert, pour choisir le dénominateur de Q-CA-06 sans voir les valeurs de BTC.
- **E-7** : le compte d'hôtes RPC du relevé (trois) est corrigé à deux (Q-CA-10).

**Réviseur attendu** : l'advisor (`BRIEF-AVIS-CALIB.md`), puis l'orchestrateur. Le rédacteur n'a généré aucun des lots qu'il
décrit.
