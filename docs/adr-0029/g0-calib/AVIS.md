# Avis de l'advisor — proposition de G0 du lot CALIB-ACTIFS (`PROPOSITION-CALIB.md`)

- **Gate 0** : modèle résolu `claude-fable-5-1` (identifiant donné par l'environnement), fiche `shogen-advisor` (R-26), effort
  `medium` (fiche du 2026-10-02 ; non vérifiable depuis la session). Date : 2026-10-08.
- **Rôle** : avis seulement ; aucune décision, aucun code, aucune écriture hors de ce fichier, aucune requête réseau, aucune
  opération git, `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée.
- **Pièces lues** [lu] : brief `BRIEF-AVIS-CALIB.md` ; `PROPOSITION-CALIB.md` (830 lignes, en entier ; « PROP ») ;
  `PAIRES-ET-TEMOIN.md` (140 lignes, en entier ; « PT ») ; `NOTES.md` (lecteur et rédacteur, en entier) ;
  `docs/adr-0029/calib/SOURCES-HISTORIQUES.md` (en entier ; « SH ») ; ADR-0029 (« l.n ») l.94-99, l.160-239, l.305-312,
  l.380-473 ; `DECISIONS-ARCHITECTURE-S2BIS.md` (« DÉC », en entier) ; `AVIS-QUESTIONS-TECHNIQUES-V3.md` (« AQT ») l.40-101 ;
  `docs/adr-0029/g0-collecte/PROPOSITION.md` (« PROP-C ») l.160-234, l.308-323 ; `g0-collecte/AVIS.md` (« AVIS-C ») l.88-107.
  Non ouverts : `tau_sigma.txt`, tout `*.jsonl`, tout dossier interdit, toute pièce de D.2, les séries de `calib/` ; rien sur
  Pocket. Les faits de PT et de SH sont [2nd] ici ; les recomptes de PROP sont [2nd] aussi (non refaits).
- **Écart déclaré E-1** : pour localiser deux pièces nommées par le brief, deux `Glob` à motif étroit (`ADR-0029*`,
  `DECISIONS-ARCHITECTURE-S2BIS.md`) ont été lancés sur `docs/` et ont rendu un chemin chacun ; un `Glob *` sur le seul dossier
  `calib2/` a listé des noms de fichiers de ses sous-dossiers `probes/` et `web/` (noms seulement, aucun ouvert). Aucun dossier
  interdit n'a été parcouru ni lu ; aucune recherche sur le dépôt ni sur le scratchpad entier.
- Niveaux : [lu], [2nd], [calc] (calcul de l'advisor, jamais sur un historique), [inféré]. **[G0]** = touche la lettre de
  l'ADR-0029 ou d'un G0 versé (ajout daté à prévoir).

## 0. En bref

1. **Verdict** : adopter la proposition avec deux modifications (Q-CA-15 : champ de mode explicite ; Q-CA-11 : mesure des cadences
   hors du lanceur du lot) et quatre ajouts datés [G0] (lettre de l.189 pour Q-CA-06 et Q-CA-07 ; constat USDC à cinq places,
   l.173 ; sensibilité « USD seules » étendue à ETH, l.212). Les treize autres questions : adoptées telles quelles.
2. **Pools et formes** (§2 de PROP) : justes et suffisants pour CB-7 et CB-8 ; CB-9 peut partir sur le 3pool, la lecture de
   sa documentation étant une condition de sa G2, non de son démarrage.
3. **Règles de calcul** (§4 de PROP) : conformes à l.181, l.187-189 et à AQT Q2/Q3 ; deux lectures de l.189 sont des choix
   (dénominateur, population et statistique du troisième terme), faits sans voir les valeurs de BTC, donc admissibles comme
   pré-enregistrement, à écrire dans l'ADR par ajout daté avant l'épinglage.
4. **Condition des historiques** : la lettre de l.186 (« existence d'historiques publics ») est **remplie** classe par classe
   (SH §1 : 6, 4, 6 places) ; c'est un constat technique. Ce qui revient à l'investisseur : l'usage de ces fichiers par un
   produit vendu (INV-1, INV-2). L'option B d'INV-1 n'est pas exécutable telle qu'écrite (§4.3 ci-dessous).
5. **Ce qui part à l'adjudication** : CB-7, CB-8, CB-9, les contrôles E-CA-23 de RB-2, et le code CA-0 à CA-6 sur fixtures
   synthétiques. **Ce qui attend INV-1** : l'épinglage et le lancement unique du calcul.

## 1. Questions techniques Q-CA-01 à Q-CA-15

| n° | verdict | motif sourcé | marque |
|---|---|---|---|
| Q-CA-01 cotation d'ETH | **Adopté (a)** : binance `ETHUSDT`, okx `ETH-USDT`, pool ETH de 10 | l.98 l'anticipe (« et de leurs flux ETH s'ils sont cotés de même ») et l'énoncé REJETTE d'ETH nomme déjà la co-défaillance de cotation (l.210) ; `ETHUSD` chez binance : 90,2 % de minutes à volume nul (SH l.45) et 6 mois de profondeur (SH l.130) [2nd] : au « dernier prix connu » (Q-CA-04), il entrerait des clôtures périmées dans la médiane des autres. Limite à écrire au paquet : τ_places(ETH) absorbe l'écart USDT/USD (≈ 0,07 % le 2026-10-08, PT l.23-27 [2nd]) ; c'est voulu (l.98 : cotation gardée sans conversion). | **[G0]** pour la sensibilité (vii) : l'étendre à ETH (pool ETH sans binance et okx, imprimée avec les sorties d'ETH) par ajout daté à l.212 ; coût nul, même code que BTC. Item SHOGEN-S2BIS-ETH-USD-SEULES-1 : décision à l'adjudication, pas après. |
| Q-CA-02 hôte de binance | **Adopté (a)** : `api.binance.com` reste l'unité ; fixtures depuis `data-api.binance.vision`, déclarées | Unité = nom d'hôte (l.168) ; le 451 est géographique (« restricted location », PT l.37) et vu d'un seul poste (SH l.131, PT l.137) ; l.81 : un observateur bloqué est remplacé avant le sceau ; la forme Q-C-05 (AVIS-C l.94) admet des fixtures capturées hors campagne avec date et sha256. Condition : le smoke de **chaque** observateur sur `api.binance.com` (E-C-37) avant le gel ; si un seul échoue, décision de l'orchestrateur (remplacement de l'observateur, l.226 R-b, jamais retrait de l'unité). | [G0-C] (CB-6/CB-7) |
| Q-CA-03 fenêtre | **Adopté (a)** : deuxième trimestre 2026, septembre imprimé | Dernier trimestre couvert par Kraken (SH l.47 : archive au 2026-06-30, Q3 en 404) ; disjoint de S2-bis ; contient la semaine-oracle de SH §4. Dates et comptes de PROP §4.1 recalculés : 2026-04-01 = mercredi, 1775001600 ; 2026-07-01 = 1782864000 ; 91 jours, 26 jours de week-end, 131 040 minutes [calc]. Dérive de régime de 5 à 8 mois jusqu'à la campagne : déjà déclarée (l.190). | — |
| Q-CA-04 population de τ | **Adopté (a)** : « dernier prix connu », exclusion des cellules Coinbase au-delà de σ, N_min = 4 (3 pour F3 à trois places), maximum sur les strates | C'est la transposition de l.180 (cellules arrivées à l'axe hors-enveloppe sous σ) et de ce qu'un ticker porte ; l.189 lit déjà la minute absente comme bougie à volume nul (donc clôture reportée). (b) « minutes actives seules » laisse USDC à 76 minutes sur 10 080 avec 4 places actives (SH l.107) : population vide. Deux précisions à écrire : (i) sous INV-1 = A′, Coinbase sort et l'exclusion n'a plus d'objet ; (ii) imprimer, par place, la part des cellules de la queue au-delà du P99,9 (déjà §4.3 pt 5) **et** l'âge médian des cellules de la queue, pour montrer si τ vient de prix périmés. | — |
| Q-CA-05 grille | **Adopté (a)** : 0,05 % partout ; planchers exacts hors grille | l.186 laisse la grille au G0 ; l.181 et l.189 fixent 0,05 % pour BTC et pour les agrégateurs ; une grille unique rend E-CA-23 (a)-(b) simple. Limite à écrire : sur les stables, le pas (5·10⁻⁴) vaut cinq fois le pas de cotation (PROP l.585) ; l'arrondi est un plafond (conservateur vers moins d'écarts) et la valeur avant arrondi est imprimée (§4.3 pt 5). Si l'orchestrateur voulait une grille plus fine pour les stables, 0,025 % (option c) rendrait 0,375 % multiple et casserait Q-CA-15 (b) ; d'où ma préférence pour (a) **avec** un champ de mode explicite (Q-CA-15). | — |
| Q-CA-06 dénominateur | **Adopté (c)** : maximum des deux classes de places de BTC ; (a), (b), (d) imprimés | l.189 écrit « τ_places_BTC » au singulier alors que BTC a deux classes de places (l.181) : lettre ambiguë. Les bougies donnent un τ unique pour les deux classes de l'actif (l.187) ; le τ unique de BTC qui couvrirait ses deux classes est borné par le plus grand des deux : le maximum au dénominateur donne le plus petit τ_agr, donc l'axe le moins aveugle, ce que l.181 et l.189 cherchent. Choix fait sans ouvrir `tau_sigma.txt` (PROP E-6) : conforme à « fixée avant tout calcul » (l.184). (e) (τ poolé recalculé sur S2) coûterait une extraction de `f35a70c` pour un gain de lettre seulement. Ajouter un drapeau descriptif si τ_agr(actif) < τ_places(actif) (jamais un refus). | **[G0]** ajout daté à l.189 |
| Q-CA-07 troisième terme | **Adopté (b) et (i)** : population = places dont l'horodatage est celui de la dernière transaction (Coinbase) ; P99 sur les cellules | Le motif du terme (AQT l.48 : « le ticker porte alors un horodatage ancien ») ne vaut que si l'horodatage vieillit avec l'inactivité : vrai pour Coinbase (“last trade”, PT l.45 [lu par PT]), faux pour OKX (“generation time”, PT l.47), Bitstamp et Gemini (heure de requête ou de fenêtre, PT l.48-49, une mesure chacun [inféré]). Sous (a), le terme d'USDC viendrait du seul bitstamp (97 % de minutes à volume nul, SH l.62) et aveuglerait l'axe staleness de quatre places. Statistique : σ de BTC est un P99 de staleness **par cellule** (l.182) ; l'âge a_p(t) par minute en est l'analogue exact ; le P99 des suites sous-pondère les longues suites (T-CA-SIG-1 : 1 440 s contre 180 s, PROP l.537). Condition dure : le sens de l'horodatage de Bitstamp et de Gemini est établi à CB-7 (E-CA-07, deux captures) **avant l'épinglage** ; si l'un des deux s'avère « dernière transaction », il entre dans la population de (b) et le paramètre change avant tout calcul. | **[G0]** ajout daté à l.189 (« durée des suites » lu comme P99 des âges par cellule ; population nommée) |
| Q-CA-08 Chainlink | **Adopté** : un proxy principal par actif ; variantes SVR jamais lues ; paramètres relus au paquet | l.173 (« variantes SVR fusionnées en une unité ») ; heartbeats différents entre proxy principal et variante `usdc-usd-svr` (PROP l.212) : lire deux proxies créerait deux σ pour une unité. Précision : `maxSubmissionValue` = 1,05 pour USDC et USDT est lu sur l'enregistrement du flux (PT l.72 [lu par PT]) : suffisant pour E-C-10. | [G0-C] (CB-8) |
| Q-CA-09 pool Curve | **Adopté (a)** : 3pool, pool NG en remplaçant écrit d'avance | Profondeur (≈ 159,8 M contre ≈ 5,0 M, PT l.97 [2nd]) ; pool NG déséquilibré (0,70 M USDC pour 4,31 M USDT, PROP l.229) et petit : un pool de cette taille peut être vidé ou migré pendant 16 semaines, le 3pool non. `get_dy` a répondu avec la signature attendue (PT l.94) ; la lecture de la documentation du 3pool (SHOGEN-S2BIS-CURVE-DOC-1) est une condition de la **G2** de CB-9, pas de son démarrage. Écart constant entre pièces (3pool 1,000393 ; Uniswap 1,000669 ; OKX 1,00062, PT l.99) : trois ordres de grandeur sous le seuil de 0,5 % de P_j (l.212) ; sans effet sur l'état. | [G0-C] (CB-9) |
| Q-CA-10 hôtes RPC | **Adopté** : `eth.drpc.org` (Uniswap), `rpc.mevblocker.io` (Curve), Tenderly en remplaçant | Deux lectures sur chaîne, donc deux hôtes distincts de celui de Chainlink (l.174) ; le « trois » de PT l.124 comptait un hôte de trop (PROP E-7, correct). Réserves à écrire : `rpc.mevblocker.io` est un point d'entrée de protection de transactions (PT l.110), `eth_call` y répond mais n'y est pas documenté comme service ; limites et conditions non lues [abs] ; Tenderly en 429 depuis une adresse partagée (PT l.112) peut l'être aussi depuis un VPS. Le smoke de chaque observateur (E-C-37) tranche ; une panne d'hôte RPC rend l'observateur sans voix, c'est voulu (AQT l.98). | [G0-C] (CB-9) |
| Q-CA-11 cadence des agrégateurs | **Modifié** : (b) oui, mais **hors de `lancer.sh`** et hors du lot CA | l.189 demande le contrôle au G0 ; une mesure d'horodatages seuls, sans prix, n'est pas une donnée de S2-bis (aucune campagne n'existe ; même raisonnement que Q-C-05, AVIS-C l.94). Mais le lot CA est un lancement unique épinglé « étape réseau puis calcul » (E-CA-28) : y greffer une mesure de 2 h depuis l'hôte de session brouille l'épingle et la frontière. Faire un relevé séparé (script de ≈ 40 lignes, sortie = intervalles entre `last_updated_at` distincts par actif, aucun prix écrit), lancé une fois avant le sceau, versé avec sa date ; conséquence pré-déclarée inchangée (cadence d'un actif plus lente que BTC = limite écrite et décision de l'orchestrateur, jamais un σ deviné). 120 lectures en 2 h tiennent sous la limite sans clé de CoinGecko (5 à 15 appels par minute, l.236). | — |
| Q-CA-12 bruit de P_j | **Adopté** : hors de ce lot, au G0 de REJEU-DECROCHAGES | l.212 et l.471 : le seuil de 0,5 % est scellé dans l'ADR ; « le rejeu historique, s'il précède le sceau, est le test public de ce seuil, sinon le seuil reste » ; AQT l.95 (« à confirmer sur l'historique de CALIB-ACTIFS ») est antérieur à cette lettre. SH n'a relevé aucun historique stable/stable [abs]. Recommandation : que le G0 de REJEU-DECROCHAGES soit lancé pour précéder le sceau, puisque ses données sont disjointes. | — |
| Q-CA-13 réemploi de `regles.py` | **Adopté** : réimplémentation (≈ 20 lignes) croisée avec `regles.quantile` et un fichier de vecteurs | `regles.regle_tau` entraîne `commun` et le contexte décimal du harnais extrait (PROP l.625-628) : l'importer ferait lire `f35a70c` par un lot qui ne doit lire aucune donnée de S2 (E-CA-02). Les vecteurs de T-CA-G-1 couvrent les bords (multiple exact, 2,80 %, 2,801 %, 2,85 %). Ajouter un vecteur à la borne basse exacte (1,5 × P99,9 = 0,0005) et un en rationnel non décimal (1/3 %). | — |
| Q-CA-14 épinglage | **Adopté** | Même protocole que PLAN-S2BIS (B.58) ; E-CA-25 (aucune statistique de dispersion avant l'épinglage) est la clause qui fait de ce lot un pré-enregistrement ; l'exposition du lecteur de SH (comptes, fractions à volume nul) est déclarée (SH l.9) et ne porte aucune dispersion. | — |
| Q-CA-15 mode « planchers seuls » | **Modifié : (a)**, un champ de mode par actif dans le fragment (`calibre` ou `planchers_seuls`), **et** le contrôle de cohérence (mode `planchers_seuls` ⇔ τ des places = 0,00375) dans E-CA-23 (b) | Un mode reconnu par une valeur magique hors grille est un artefact de lecture : il dépend de la grille (Q-CA-05), il n'est pas lisible par le validateur frais du paquet sans cette convention, et le mode doit de toute façon être « déclaré au paquet » (l.191 ; AQT l.72). Le schéma de `analyse.json` est encore à `null` pour `tau_sigma` et `unites` (PROP l.113) et E-CA-23 n'est pas encore écrit dans RB-2 : ajouter un champ maintenant coûte une ligne de schéma et un test. Si l'orchestrateur garde (b), la convention doit être écrite au README du paquet. | [G0-C] (RB-2) |

## 2. Paires servies et pools (PROP §2)

1. **Justes** : le tableau hôte × paire (PROP §2.1) est cohérent avec PT §1.1 et avec SH §3 [2nd] ; les trois constats contraires
   à l'ADR sont réels et à verser par ajout daté : USDC/USD servi par **cinq** places (binance `USDCUSD` s'ajoute aux quatre de
   l.173), Gemini sans historique (SH l.26), OKX sans `ETH-USD` ni `USDC-USD` (PT l.26). **[G0]** l.173, l.214, l.416 (note à
   la question 10 de l'investisseur : « trois places liquides » devient cinq, dont deux minces).
2. **Suffisants pour CB-7** : par (hôte, actif) la proposition donne point d'accès, symbole, devise, classe de source, sens de
   l'horodatage avec sa pièce, les pièges de décodage (clés `XETHZUSD`/`USDTZUSD` de Kraken, dernier prix à l'indice 7 de la
   réponse groupée Bitfinex, codes `UDC`/`UST`) (PROP §2.2). Deux trous, tous deux portés par SHOGEN-S2BIS-FORMES-DOC-1 :
   Gemini v1 `usdtusd` non sondé et champs de Gemini non documentés dans les pages lues (PT l.49) ; à combler à CB-7 par une
   capture datée, avant le gel de `formes.json`.
3. **Suffisants pour CB-8** : identifiants CoinGecko et clés DefiLlama groupés (E-C-09), trois proxies Chainlink avec décimales
   8 et plafond 1,05 (PT §2). Réserve d'hôte : `coins.llama.fi` est l'hôte de S2 (`sources.py` l.269) mais absent de la
   documentation lue (PT l.52) : continuité de S2, à déclarer, pas à changer.
4. **Compte des lectures par fenêtre** : OKX à cinq lectures séparées, à la limite de l.236 (5 + 4 + 10 + 1 = 20 s) : juste,
   sans marge ; toute sixième forme (carte comprise) impose le regroupement `/market/tickers` (AVIS-C Q-C-10). À écrire au G0 de
   la carte.
5. **N ≥ 4 répondantes** : avec 8 à 10 unités par classe, la condition d'écart (l.98) ne dépend plus des agrégateurs et de
   l'oracle pour USDC/USD ; une place mince répond quand même avec un dernier prix, donc elle compte comme répondante ; ce que la
   minceur change, c'est la staleness (σ nul pour binance, kraken, bitfinex sans horodatage ; heure de génération pour bitstamp
   et gemini) : l'axe staleness d'USDC est presque aveugle par construction, limite à écrire avec celle de l.214.

## 3. Règles de calcul (PROP §4) : justesse et ce qui se scelle

1. **τ des places** : grid-ceil(1,5 × max_s P99,9, 0,05 %), rang ⌈999·N/1000⌉, bornes 0,05 % ≤ τ < 2,85 % avec refus nommé en
   haut : conforme à l.181, l.183 et à l.187 ; une valeur par actif pour les deux classes de places : conforme à l.187 (« par
   actif »). Population : voir Q-CA-04.
2. **τ des agrégateurs** : formule de l.189 au mot près, dénominateur selon Q-CA-06 ; exacte, contrôlée dans RB-2 (E-CA-23 d).
3. **τ et σ des oracles** : 0,75 % ; 0,375 % ; 5 400 s ; 124 200 s ; 129 600 s : égaux à l.188 et à DÉC l.36-37 [calc
   refait : 1,5 × 0,5 ; 1,5 × 0,25 ; 1,5 × 3 600 ; 1,5 × 82 800 ; 1,5 × 86 400]. Exacts, jamais arrondis à la grille : juste
   (l.189 « planchers seuls »). Heartbeat d'USDC à 82 800 s et non 86 400 s : l.188 le portait déjà (124 200 = 1,5 × 82 800).
4. **σ** : places horodatées max(30 s, σ_BTC, troisième terme) ; agrégateurs max(300 s, σ_BTC) ; sans horodatage nul ;
   conforme à l.189 et à `config` l.21, l.86 [2nd]. Ordre σ puis τ (E-CA-17) : nécessaire, puisque l'exclusion de Q-CA-04 lit σ ;
   déclaré, sans circularité.
5. **Mode « planchers seuls »** : τ des places = 0,375 % (AQT l.72), τ_agr par la formule, σ sans troisième terme : cohérent ;
   l'extension à τ_agr et à σ est [inféré] et doit être écrite dans l'ajout daté de Q-CA-15.
6. **À sceller avant l'épinglage** (donc avant tout calcul), dans `parametres.json` et dans l'ajout daté de l'ADR : la fenêtre et
   les strates ; la liste (place, paire, URL, format) **par lecture d'INV-1** (A, A′ : la liste change) ; « dernier prix
   connu », N_min et la règle d'exclusion ; la grille, les bornes, les rangs, le facteur 1,5 ; le dénominateur (Q-CA-06) ; la
   population et la statistique du troisième terme (Q-CA-07), avec le sens de l'horodatage établi à CB-7 ; l'épingle de
   `tau_sigma.txt`. **À sceller au paquet** (l.219) : les valeurs produites, le mode par actif, les limites écrites (dérive de
   régime, τ non comparables entre méthodes, axe staleness des stables, écart USDT/USD dans τ_places(ETH)).
7. **Ce qui ne doit jamais se calculer avant le sceau** : tout prix ou staleness du rodage (l.192, l.224) ; PROP §4.8 est juste.
8. **Oracles d'exécution** (E-CA-14, E-CA-15) : justes et utiles ; ils contrôlent l'ingestion, pas la statistique ; l'archive
   Kraken peut être republiée avec d'autres octets (refus `CA/kraken` prévu, puis décision) : conséquence déjà pré-déclarée.

## 4. Condition des historiques et licence : technique contre investisseur

### 4.1 Technique (constat)

- La lettre de l.186 demande d'« établir sur pièce l'**existence** d'historiques publics à une minute, antérieurs à la campagne,
  pour au moins 4 places par classe ». SH l'établit : ETH 6, USDC 4, USDT 6 (SH §1) [2nd]. Lue classe par classe (AQT Q3,
  l.191) : F2 (ETH) ≥ 4 : oui ; F3 ≥ 3 : oui pour USDC et USDT. **La condition de l.191 est remplie** ; le décalage du sceau
  (une à deux semaines) est déjà absorbé par le calendrier à S+10/11 (l.397) et n'est pas consommé (PROP §11) [inféré par PROP,
  cohérent avec l.395-397].
- La question de la republication des octets bruts ne vient pas de l.186 mais de la règle générale ADR-0003/ADR-0005 et de la
  question 13 de l'investisseur, qui porte sur les **sources du pool** (réponses en direct), non sur des fichiers d'archive. Le
  lot ne republie aucun octet d'historique (E-CA-05, E-CA-13 : manifeste URL, taille, sha256) : la recalculabilité par un tiers
  est par référence, tant que la place sert le fichier ; c'est une limite écrite, pas une contradiction.

### 4.2 Investisseur (en langage clair)

- **Ce qui ne dépend pas de lui** : les prix passés existent, gratuits et sans compte, sur assez de places pour régler les seuils
  des trois actifs ; le calendrier du scellement ne bouge pas (vers le 13 ou le 20 décembre 2026, PROP §11 [calc par PROP]).
- **Ce qui dépend de lui (INV-1, INV-2)** : ces fichiers sont téléchargeables, mais les conditions des places restreignent leur
  **usage**, pas seulement leur republication : Binance les donne sous une licence non commerciale, OKX interdit l'usage
  commercial sans autorisation, Kraken demande une permission préalable (SH l.47, l.50, l.92 [lu par SH]) ; Coinbase et Bitfinex
  n'ont pas pu être lues (SH l.125). Shōgen veut vendre un standard : la question « est-ce un usage commercial ? » est juridique
  et lui revient (INV-2), ainsi que la dépense d'un avis juridique ou d'une licence (option C).
- **Ordre des actes** : (1) faire lire Coinbase et Bitfinex par un lecteur avec un outil qui exécute le JavaScript (Firecrawl,
  CLAUDE.md §7), 1 à 2 h, **avant** de poser INV-1, pour que le tableau soit complet ; (2) poser INV-1 et INV-2 ensemble ; (3)
  coder le lot pendant l'attente ; (4) épingler et lancer après la réponse.

### 4.3 Les options d'INV-1, vues de la technique

- **A** (six places, sans republier) : la meilleure techniquement : seule option qui garde Coinbase, unique place à horodatage de
  dernière transaction, donc seule source du troisième terme de σ (Q-CA-07) ; marge sur la condition (6, 4, 6).
- **A′** (places aux conditions lues : binance, kraken, okx, bitstamp) : ETH 4 (sans marge), USDC 3, USDT 4 ; aucun troisième
  terme (σ = max(30 s, σ_BTC)) ; USDC calibré sur une médiane de deux dont un bitstamp à 97 % de minutes reportées (SH l.62) :
  τ(USDC) y reposerait surtout sur des prix périmés ; F3 est hors décision, mais c'est à écrire. A′ ne réduit le risque qu'en
  apparence : les conditions « lues » sont les plus restrictives (Binance NC, OKX 9.4).
- **B** (données republiables seulement) : **non exécutable telle qu'écrite** : aucune place ne le permet sans contrat (SH §1),
  donc ETH part en seconde vague **sans source de calibration** (PROP §3.5 : les historiques sont exclus par la même lecture, et
  les lectures de S2-bis avant le rendu sont D.2-bis, l.228). B suppose C, ou une méthode de calibration qui n'existe pas. À dire
  à l'investisseur en ces termes, pour qu'il ne choisisse pas une option vide.
- **C** (licences) : coût et délai inconnus ; compatible avec A en attendant (calcul d'abord, licence ensuite) si le juriste
  l'admet.
- Le rédacteur ne recommande pas d'option (PROP l.665) : juste, la question est de valeur. Mon avis technique : A, avec INV-2
  posée en même temps et la lecture de Coinbase et Bitfinex faite avant.

### 4.4 Couplage avec le pool en direct (SHOGEN-S2BIS-LICENCES-API-1)

Les mêmes conditions régissent les réponses en direct de binance, okx et kraken que la mesure journalise et publie en octets
bruts (l.175, l.451 ; E-C-17). La réponse du 2026-10-04 à la question 13 (« sources qui interdisent la republication : retirées »)
appliquée à la lettre pourrait retirer jusqu'à trois unités du pool BTC confirmatoire, changer la cellule cible et faire rejouer
SIM-NIVEAU-BIS et SIM-PUISSANCE-BIS (l.175, PROP-C l.317). Ce n'est pas une question de CALIB-ACTIFS, mais INV-1 et INV-2 doivent
être posées **avec** cette conséquence, sinon la réponse de l'investisseur sur les archives préjugera du pool sans qu'il le sache.

## 5. Ce que l'adjudication débloque, ce qui attend

| sous-lot | débloqué à l'adjudication | attend |
|---|---|---|
| CB-7 | formes du §2.2 de PROP, devises, classes, sens des horodatages (Coinbase, OKX : documentés ; Bitstamp, Gemini : à établir par deux captures, E-CA-07), fixtures capturées depuis l'hôte de session (binance : `data-api.binance.vision`, déclaré) | rien d'autre ; `formes.json` gelé après FORMES-DOC-1 (Gemini `usdtusd`, codes Bitfinex) |
| CB-8 | agrégateurs groupés ; trois proxies, décimales, plafonds | relecture des paramètres au paquet (E-CA-10) |
| CB-9 | OKX `USDC-USDT` ; Uniswap `slot0` du palier 0,01 % ; Curve 3pool `get_dy(1, 2, 10⁶)` ; hôtes drpc et mevblocker ; remplaçants (pool NG, Tenderly) | lecture de la documentation de `get_dy` du 3pool avant la G2 de CB-9 ; smoke des observateurs sur les hôtes RPC |
| RB-2 | contrôles E-CA-23 (a)-(h) avec le champ de mode (Q-CA-15 modifiée) ; schéma de `tau_sigma` et `unites` | les valeurs (fragment), au lot du paquet |
| lot CA-0 à CA-6 | tout le code, sur fixtures synthétiques ; G2 | épinglage et lancement : INV-1 (A, A′ ou C) ; sens des horodatages établi à CB-7 ; ajouts datés de l'ADR (Q-CA-06, Q-CA-07) versés |
| relevé de cadence (Q-CA-11 modifiée) | script séparé, une exécution avant le sceau | — |
| ajouts datés [G0] | l.173/l.214/l.416 (USDC cinq places, Gemini sans historique, OKX) ; l.189 (dénominateur ; troisième terme) ; l.212 (sensibilité (vii) sur ETH) ; l.310 (taille ≈ 1 100 à 1 300 au lieu de ≈ 200, item P1-ESTIMATION-1) | à l'adjudication |

## 6. Trois risques

1. **Licence d'usage et pool en direct** (§4.4) : le risque n'est pas le calcul sur archives, c'est qu'une lecture stricte de la
   question 13 retire binance, okx ou kraken du pool confirmatoire après que les simulations ont fixé n_s et T_max. Parade :
   lire Coinbase et Bitfinex maintenant ; poser INV-1 et INV-2 avec la conséquence sur le pool écrite ; trancher les licences du
   pool avant le gel de `formes.json`, pas avant le sceau seulement.
2. **Marchés minces et dernier prix connu sur USDC** : avec bitstamp (6,9 %) et bitfinex (10,9 % de minutes actives en juin, SH
   l.129), la queue de τ(USDC) et, sous A′, la médiane elle-même reposent sur des clôtures périmées ; la grille de 0,05 % ajoute
   une quantification de l'ordre de la dispersion mesurée. Parade : contributions par place et âge des cellules de la queue
   imprimés (Q-CA-04), variante « minutes actives » imprimée, limite écrite au paquet ; F3 reste hors décision ; refus nommé si
   N_min n'est pas tenu dans une strate.
3. **Paramètres inférés d'une seule mesure** : le sens de l'horodatage de Bitstamp et de Gemini (une mesure chacun) fixe la
   population du troisième terme et l'exclusion de Q-CA-04 ; les agrégateurs Chainlink d'USDC et d'USDT ont au plus 25 à 26 jours
   (PROP l.217-219 [calc par PROP]) et leurs paramètres peuvent encore changer. Parade : E-CA-07 (deux captures) avant
   l'épinglage ; E-CA-10 (relecture au paquet, refus nommé en cas d'écart) ; un changement pendant la campagne reste descriptif,
   jamais un re-réglage (l.184).

## 7. Points de forme relevés sur la proposition (sans effet sur le verdict)

- PROP l.9 et l.780 : le sha256 annoncé pour `BRIEF-AVIS-CALIB.md` (`558915f2…56d8`) n'a pas été recalculé ici.
- PROP §2.5 et PT l.94 : « net des frais » pour `get_dy` : juste ; le dénominateur des frais du 3pool reste [abs] (PT l.135),
  sans effet sur le témoin (P_j lit la médiane, l.212).
- PROP l.690 : « 11,5 h pour USDC » : juste (82 800 s = 23 h, battement manqué vu après 1,5 × 23 h = 34,5 h ; la phrase de l.188
  parle de 12 h de battement, non du délai de détection) ; constat à verser avec les autres.
- Taille : ≈ 1 100 à 1 300 lignes contre ≈ 200 (l.310) : écart plausible (PLAN-S2BIS : 1 477 lignes réalisées, PROP l.515) ;
  calendrier « hors chemin critique » [inféré] tenable si l'adjudication et INV-1 tombent dans la semaine.

## 8. Provenance de cet avis

Lecture seule des pièces listées en tête ; aucun calcul sur un historique ; calculs de contrôle [calc] : dates et comptes de la
fenêtre (jours de la semaine par comptage depuis le 2026-01-01, jeudi ; 1767225600 + 90 × 86 400 = 1775001600 ; + 91 × 86 400 =
1782864000), planchers des oracles, 1,5 × 82 800 = 124 200. Aucune pièce de D.2 ouverte ; aucune attestation D.3 demandée par le
brief. Écart E-1 déclaré en tête. Fichier écrit : celui-ci seulement.
