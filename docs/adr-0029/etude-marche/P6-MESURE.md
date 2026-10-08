# P6 — Mesure : ajouter ETH, USDC et USDT à S2-bis sans casser la décision

> *Note de versement de l'orchestrateur* : citations de pages web non versées à `biblio/` passées de « … » à “…” (gate S-G5) ; lectures [lu] web du rapport, copies hors dépôt.

- **Gate 0** : modèle résolu `claude-opus-5-5` (identifiant exact déclaré par la session ; préfixe attendu conforme). Rédigé le 2026-10-04 (début 04:52 UTC, `date -u`).
- **Brief** : `etude-marche/BRIEF-P6-MESURE.md`, sha256 `57b6d9a6…9655` (vérifié).
- **Lu dans le dépôt (lecture seule)** : ADR-0029 révision 2 en entier ; docs 02, 04 §2, 10 §2-§3 et §5.1-§5.4, 11 §1 et §4.2-§4.4, avis produit ; `s2-harness/shogen_s2/sources.py` l.320-362 ; `docs/adr-0029/AVIS-STATS.md` (une ligne, Q6). Aucune pièce interdite ouverte, aucun `*.jsonl` du dépôt.
- **Niveaux** : [lu] lu sur la source (URL, lecture du 2026-10-04) ; [2nd] seconde main ; [calc] mon calcul ou ma simulation ; [inféré] mon raisonnement.
- **Manques déclarés** : lecture directe de `latestRoundData` par RPC public refusée (HTTP 403, puis refus de l'environnement ; non contournée) : l'âge réel des flux Chainlink n'est pas mesuré ici. Le PDF BIS Papers 141 n'a pas été servi (page HTML à la place) : seul l'extrait de recherche est cité.

## 1. Résumé

1. **Ne pas changer la décision BTC.** BTC/USD reste la **seule classe confirmatoire** de R1-2 (famille de 2 strates, 0,01 chacune, borne 0,02 ; ADR-0029 §2.7), avec le pool de 10 hôtes et la cellule cible déjà scellables.
2. **ETH/USD entre en confirmation secondaire, par séquence fixe** : testé à 0,01 dans la strate s *seulement si* BTC rejette dans s. Le risque global reste ≤ 0,02, sans aucun α retiré à BTC (méthode « fixed-sequence », FDA 2022 [lu]).
3. **USDC et USDT restent exploratoires dans S2-bis** : le même moteur R1-2 tourne sur eux, mais **hors décision**. Raisons : aucune donnée de calibration de τ, des flux Chainlink à heartbeat de 23-24 h et plafonnés à 1,05, des pools plus petits, et peu d'écarts attendus, donc NON ÉVALUABLE probable.
4. **Une classe = un actif ; les unités restent des hôtes.** Mettre BTC et ETH du même hôte dans un même pool fabriquerait des co-pannes par construction (le défaut OKX de S2, §1.2 pt 5).
5. **L'« écart au peg » n'est pas un écart de source.** Pendant un décrochage, toutes les sources justes s'écartent de 1. Le peg devient une **variable d'état** publiée (descriptive et analyse conditionnelle pré-déclarée), pas un 4ᵉ axe.
6. **τ et σ par couple (actif, classe de source)**, fixés avant le sceau par une règle écrite : historique public à 1 minute (Coinbase, Binance) pour les places, plancher égal au seuil de déviation pour les oracles poussés (Chainlink 0,5 % ETH ; 0,25 % stables), σ = 1,5 × heartbeat.
7. **Taille du pool** : passer de 10 à 15-25 unités *fait chuter* la puissance de K≥2 (règle R1-2), de 0,91 à 0,54 à 25 unités diluées, et jusqu'à 0,03 si les ajouts sont exposés au mode commun. La statistique de paires S = Σ C(m_j, 2) reste entre 0,96 et 1,00 dans les scénarios « incident sur plusieurs hôtes », et égale K≥2 sur 2 hôtes ; niveau tenu sous H0 (§3.4 [calc, synthétique]). Le pool confirmatoire BTC reste à 10 unités ; si le pool grandit, S est à évaluer en règle avant le sceau.
8. **Débit** : 4 observateurs × 4 actifs restent loin des limites lues, sauf CoinGecko sans clé (« 5 to 15 calls per minute » [lu, extrait]) : une seule requête groupée par minute et par observateur y est obligatoire.
9. **Coût** : nul en infrastructure (mêmes VPS) ; environ +30 à 50 % de lignes pour la collecte et le rendu ; un lot de calibration avant le sceau.
10. **Ce qu'on y gagne** : un énoncé confirmatoire sur un 2ᵉ actif sans perte sur BTC, et la première mesure publiée de diversité des sources stablecoin, déclarée exploratoire, qui prépare une confirmation en S3.

## 2. Constats sourcés

**C1. Cadences Chainlink (Ethereum mainnet)** [lu, `https://reference-data-directory.vercel.app/feeds-mainnet.json`, répertoire de données de docs.chain.link, 2026-10-04, sha256 `31626527…2722`, copie `web/feeds-mainnet.json`] :

| flux (proxy « ens ») | seuil de déviation | heartbeat | particularité |
|---|---|---|---|
| BTC/USD `0xF403…E88c` | 0,5 % | 3 600 s | celui de S2 |
| ETH/USD `0x5f4e…8419` | 0,5 % | 3 600 s | — |
| USDC/USD `0x8fFf…18f6` | 0,25 % | **82 800 s** | `stablecoinCapped: true`, `maxSubmissionValue` = 1,05 |
| USDT/USD `0x3E7d…e32D` | 0,25 % | 86 400 s | idem |

Le répertoire liste aussi, pour chaque paire, des variantes « SVR » (Aave SVR, Shared SVR) : d'autres proxys et agrégateurs. Ce sont des chemins de livraison d'un même flux, donc **une seule unité** [inféré]. La doc Chainlink définit le déclenchement : “The first condition that is met triggers an update” (déviation ou heartbeat) [lu, `docs.chain.link/architecture-overview/architecture-decentralized-model.md`]. Pour les flux bornés : “caps the on-chain reported price at a pre-defined maximum (e.g., $1.05) … the most recently written on-chain price will be the value returned … would not include a lower bound” [lu, `docs.chain.link/data-feeds/selecting-data-feeds.md`, l.276]. Au-dessus du plafond, un flux stable **paraît donc vieilli par conception**. Pour ETH, le seuil de 0,5 % autorise un écart légitime au marché allant jusqu'à 0,5 % plus le mouvement depuis la dernière mise à jour [inféré].

**C2. Pyth** : « pull oracles only update the on-chain price when requested » [lu, `docs.pyth.network/price-feeds/core/pull-updates`]. Une lecture on-chain sans clé (voie B′ d'ADR-0029 §2.5) a donc une staleness pilotée par les utilisateurs, pas par l'oracle. σ n'y est pas transposable depuis un heartbeat [inféré].

**C3. Homogénéité des cotations** [lu, 2026-10-04] : Kraken liste `USDCUSD`, `USDTZUSD`, `XETHZUSD`, `XXBTZUSD`, tous `online` (`api.kraken.com/0/public/AssetPairs`, via Firecrawl). Coinbase Exchange liste `USDT-USD`, `ETH-USD`, `BTC-USD` et `USDT-USDC`, mais **pas `USDC-USD`** (`api.exchange.coinbase.com/products`, extraction automatisée de Firecrawl, cache du 2026-10-03 ; à recontrôler à la main). Gemini liste `usdcusd`, `usdtusd`, `ethusd` et `btcusd` (`api.gemini.com/v1/symbols`). Bitstamp liste les quatre `Enabled` (`/api/v2/trading-pairs-info/`, extraction automatisée). En S2, 2 flux sur 12 cotaient en USDT (doc 10 §2). CoinGecko construit son prix en mélangeant des tickers USD, USDT, USDC et EUR (doc 10 §2). Les écarts entre places sont « much larger across than within countries » et co-varient (Makarov et Schoar, JFE 135(2), 2020, résumé [lu, `hdl.handle.net/1721.1/130495`]). Conséquence [inféré] : pour USDT/USD et USDC/USD, seules les places à USD fiat sont dans la classe. Une paire stable/stable (USDC-USDT) n'est pas une cotation USD.

**C4. Décrochages : des événements rares, mais réels.** USDC est tombé à 0,8726 $ le 11 mars 2023 (agrégat CCCAGG) après l'annonce de 3,3 Md$ de réserves bloquées chez SVB [lu, `data.coindesk.com/blogs/market-analysis-silicon-valley-bank-circle-usdc` ; même montant chez la Fed, FEDS Notes du 2025-12-17, extrait lu]. BIS Papers 141 : “We study 68 stablecoins and show that not one of them has been able to maintain parity with its peg at all times” [extrait de recherche ; PDF non servi]. En 16 semaines, la probabilité d'un décrochage majeur est faible et non estimée ici [inféré].

**C5. Limites de débit** [lu sauf mention] : CoinGecko sans clé, « IP-based rate limiting — shared across all users on the same IP » (`docs.coingecko.com/docs/errors-and-rate-limits`) ; « 5 to 15 calls per minute » (page support CoinGecko, extrait de recherche). Bitfinex : “between 10 and 90 requests per minute … the IP is blocked for 60 seconds” (`docs.bitfinex.com/docs/requirements-and-limitations`, modifiée le 2025-06-10). OKX : « Public unauthenticated REST rate limits are based on IP address » (`okx.com/docs-v5/en/`). Kraken ≤ 1 appel/s, Gemini 120/min et Coinbase 10/s ne sont pas re-lus : ce sont des lectures worker de doc 10 §3.3 [2nd]. Les limites étant par adresse IP, chaque observateur a son propre budget. La charge vue par une source est ×4, mais par adresses distinctes [inféré].

**C6. Multiplicité, sources réglementaires.** ICH E9 : “A confirmatory trial is an adequately controlled trial in which the hypotheses are stated in advance” ; « There should generally be only one primary variable » ; “any aspects of multiplicity which remain … should be identified in the protocol” [lu, PDF EMA ICH E9 Step 5, pp. 6, 7, 28 du fichier, sha256 `6dd74185…6b96`]. FDA, *Multiple Endpoints in Clinical Trials* (oct. 2022) [lu, PDF sha256 `40284a05…a9563`] : “Exploratory endpoints do not need multiplicity adjustment because they are generally not used to support conclusions” (p. 10) ; Holm “is useful for endpoints with any degree of correlation” (p. 21) ; séquence fixe : “Testing begins with the first endpoint at the full alpha level and continues through the sequence only until an endpoint is not statistically significant” (p. 27) ; rééchantillonnage de Westfall et Young : “the power increases as the correlation increases” (p. 24). Holm (1979) et Westfall et Young (1993) ne sont cités que via la FDA [2nd].

**C7. Test par rotations : la littérature (item SHOGEN-S2BIS-ROTATION-SOURCE-1)** [lu, résumés]. Harris, *A Shift Test for Independence in Generic Time Series*, arXiv:2012.06862 (2020). Le décalage sans enroulement de −N à N donne un test **conservatif** : « at most m/(N+1) », avec “half the power of an approximate test valid in the large N limit”. Il exige une série stationnaire. Kalyuzhny, Global Ecol. Biogeogr., doi:10.1111/geb.13083 (préprint bioRxiv 762278). L'algorithme à décalage cyclique “does not preserve temporal autocorrelation due to the need to "wrap" the time series”, avec un taux d'erreur de 1ʳᵉ espèce « highly elevated » quand les séries ont une tendance ou un état initial hors équilibre. Mrkvička et al., arXiv:1911.00240 : la « toroidal correction » rend le décalage aléatoire libéral. Harms et al., J. Ecol. 89 (2001) 947-959 : l'origine du « torus-translation test », référence seulement. Conséquence [inféré] : la prémisse de stationnarité par strate d'ADR-0029 §2.7 pt 7 porte toute la validité. SIM-NIVEAU-BIS doit comparer la rotation enroulée à la variante de Harris (non enroulée, conservative) sur des séries à dérive.

**C8. Pré-enregistrement** : « preregistration can establish a bright line between prediction and postdiction » (Nosek et al., PNAS 115(11), 2018, extrait lu sur `pnas.org`).

## 3. Analyse et recommandations

### 3.1 Structure : une classe par actif, des hôtes pour unités, une famille hiérarchique

- **Ce qu'il faut faire.** Quatre classes R1 : BTC/USD, ETH/USD, USDC/USD, USDT/USD. Chacune a son pool d'hôtes, ses τ et σ par classe de source, ses deux strates (même calendrier pour toutes) et sa loi de rotations propre. Les rotations décalent **toutes les séries d'un même hôte du même décalage** quand une statistique multi-classes est calculée. Cela conserve la dépendance entre actifs propre à chaque hôte ; seule l'indépendance entre hôtes est testée [inféré].
- **Pourquoi.** La panne de transport d'un hôte frappe tous ses actifs. Un pool mêlant (hôte, actif) compterait ces co-pannes « structurelles », exactement le défaut OKX de S2. Les quatre tests sont donc **fortement corrélés positivement** sur l'axe panne : ajouter des classes confirmatoires apporte peu d'information indépendante sur la disponibilité. L'apport nouveau est sur les axes de prix (hors-enveloppe, staleness) [inféré].
- **Plan de multiplicité recommandé (option A).**
  - F1, inchangée : BTC calme et BTC stress, Bonferroni à 0,01 chacune. « R1 discrimine (S2-bis) » reste défini **sur BTC seul**.
  - F2, séquence fixe par strate : ETH_s testé à 0,01 seulement si BTC_s rejette. P(au moins un rejet à tort) ≤ 0,02, sous toute dépendance (la séquence fixe ne dépense pas d'α au-delà du premier test ; principe de clôture, C6) [inféré].
  - F3, exploratoire : USDC et USDT. Le moteur complet tourne, imprimé « hors décision », aucune phrase de registre confirmatoire.
- **Alternatives.**
  - **(B) Quatre classes confirmatoires**, Holm sur 8 hypothèses à 0,02. Le seuil BTC tombe à 0,0025 au premier pas (C_s ≤ 24 avec R = 9 999). La perte de puissance BTC est chiffrée au §3.4 ; c'est **casser la décision**, puisque la cellule cible et 16 semaines étaient calculées à 0,01.
  - **(C) Westfall-Young min-P** sur les rotations jointes par hôte : la plus puissante sous corrélation (C6). Plus complexe à sceller ; à garder en sensibilité.
  - **(A′)** Placer USDT puis USDC en fin de séquence (BTC → ETH → USDT → USDC) ne coûte aucun α. Je ne le recommande pas en S2-bis, faute de calibration (§3.3) : un REJETTE stable sous un τ mal posé serait une surclamation [inféré].
- **Ce que ça apporte.** Un énoncé confirmatoire possible sur ETH sans retirer d'α à BTC. Si BTC ne rejette pas, ETH ne peut pas être confirmé : c'est le prix de la séquence fixe (“the important hypotheses further down the hierarchy might never get tested”, FDA p. 10 [lu]).

### 3.2 Définition d'écart par classe

- **Actifs volatils (BTC, ETH)** : écart relatif à la médiane leave-one-out, inchangé (doc 10 §5.2). Il est sans dimension, donc comparable entre actifs. τ est distinct par actif, car le décalage des instants de lecture (quelques secondes, δ = 20 s) produit une dispersion proportionnelle à la volatilité à 1 minute [inféré].
- **Stablecoins** : même écart leave-one-out (relatif = absolu, puisque le prix vaut environ 1), **pas d'axe peg.**
  - *Variable d'état* P_j = |médiane consolidée − 1|, imprimée par fenêtre.
  - *Analyse conditionnelle pré-déclarée, exploratoire* : K et la loi de rotation sur les fenêtres où P_j > 50 points de base, seuil à sceller.
  - Motif : sous K&L, une défaillance est une réponse fausse. Pendant un décrochage, la réponse juste est le prix de marché ; la source qui affiche 1,0000 (figée ou plafonnée) est celle qui défaille. L'écart leave-one-out et la staleness l'attrapent déjà [inféré].
- **Plafond Chainlink à 1,05** (C1) : une fenêtre où le marché consolidé dépasse 1,05 classe l'écart Chainlink stable en **« borné par conception »**. Il est compté à part, ni dans p̂_u ni dans K.
- **Cotation USDT dans BTC et ETH** : garder les unités cotées en USDT (continuité avec S2, devise en champ), sans conversion. Convertir par un taux USDT/USD créerait une dépendance commune à la source du taux. Pré-déclarer deux choses : (i) la sensibilité « unités USD seules » ; (ii) la co-occurrence des écarts hors-enveloppe des unités USDT avec P_j de la classe USDT, en descriptif. Cela rend mesurable un mode commun de cotation au lieu de le supposer [inféré].

### 3.3 τ, σ, cadences et staleness

- **σ des oracles poussés** = 1,5 × heartbeat, comme la règle d'ADR-0020 pour Chainlink BTC : ETH 5 400 s ; USDC 124 200 s ; USDT 129 600 s [calc sur C1]. Avec un heartbeat de 23-24 h, l'axe staleness des stables ne voit qu'un battement manqué de plus de 12 h. C'est une limite à écrire, pas un défaut [inféré].
- **τ des oracles poussés** : τ ≥ seuil de déviation + dispersion de marché. Plancher proposé : 1,5 × seuil, soit 0,75 % pour ETH et 0,375 % pour les stables. Le maximum avec la règle de calibration est retenu [inféré].
- **τ des places et agrégateurs pour ETH, USDC et USDT.** S2 n'a aucune donnée pour eux, donc la règle TAU-SIGMA-S2BIS (ADR-0029 §2.6) ne s'applique pas. Proposition : un lot **CALIB-ACTIFS** avant le sceau, sur un historique public à 1 minute antérieur à S2-bis, donc disjoint.
  - Sources : Coinbase candles, granularité 60 s et 300 bougies par requête [lu, `docs.cdp.coinbase.com/…/get-product-candles`] ; Binance `data.binance.vision`, fichiers 1m avec `.CHECKSUM` sha256 [lu, `github.com/binance/binance-public-data`] ; Kraken.
  - Règle : τ = grid-ceil(1,5 × P99,9 de |clôture_i − médiane LOO des clôtures|) par actif.
  - Caveats déclarés : une clôture de bougie n'est pas un ticker lu à un instant ; peu de places disposent d'un historique 1m public.
  - Le rodage ne peut pas servir à cette calibration : il interdit toute lecture de prix (ADR-0029 §2.8).
- **Staleness des places sans horodatage** : axe non évaluable, comme en S2.

### 3.4 Taille du pool (15, 20, 25 unités) et puissance des rotations [calc, synthétique]

Mon modèle est recodé à partir de la description du scénario B d'ADR-0029 §2.4 d ; le code d'ADR n'est pas versé. Paramètres : calme, 16 semaines (n = 109 440 fenêtres) ; taux de faute propre 0,005 × f par unité, épisodes de 20 fenêtres en moyenne ; ρ = 0,1 incident commun par jour, 20 fenêtres en moyenne, touchant chaque unité du sous-ensemble partagé avec probabilité 0,7 ; R = 999 rotations ; 300 réplications sous H1, 500 sous H0. Script : `calc/sim_pool.py` (sha256 `8985c9d5…a8a3`). « Dilué » = les ajouts sont hors du mode commun (sous-ensemble de 7) ; « proportionnel » = 70 % du pool est exposé.

Chaque cellule donne la puissance à α = 0,01 / α = 0,0025 (le second seuil est celui du 1ᵉʳ pas de Holm de l'option B). K2 : fenêtres à ≥ 2 écarts (règle R1-2) ; S : paires coïncidentes Σ C(m_j, 2).

| pool N (exposés) | B : K2 | B : S | C (bruit de S2) : K2 | C : S |
|---|---|---|---|---|
| 10 (7) | **0,91** / 0,81 | 1,00 / 1,00 | 0,37 / 0,20 | 0,99 / 0,98 |
| 15 dilué (7) | 0,83 / 0,65 | 1,00 / 1,00 | 0,17 / 0,07 | 0,99 / 0,97 |
| 15 proportionnel (10) | 0,72 / 0,46 | 1,00 / 1,00 | 0,08 / 0,02 | 1,00 / 1,00 |
| 20 dilué (7) | 0,59 / 0,38 | 1,00 / 0,99 | 0,08 / 0,03 | 0,97 / 0,96 |
| 20 proportionnel (14) | 0,26 / 0,07 | 0,99 / 0,99 | 0,02 / 0,00 | 0,99 / 0,99 |
| 25 dilué (7) | 0,54 / 0,31 | 0,99 / 0,98 | 0,03 / 0,01 | 0,96 / 0,94 |
| 25 proportionnel (18) | 0,03 / 0,01 | 1,00 / 1,00 | 0,00 / 0,00 | 1,00 / 1,00 |
| *stress 16 sem., B* : 10 / 25 dilué / 25 prop. | 0,57 / 0,22 / 0,04 | 0,93 / 0,86 / 0,95 | — | — |
| *incident sur 2 hôtes seulement, B* : 10 / 25 | 0,93 / 0,68 | 0,93 / 0,66 | C, 10 : 0,42 | C, 10 : 0,41 |

Sous H0 (ρ = 0 ; N = 10 et 25 ; f = 0,3 et 1 ; 300 réplications chacune), le taux de rejet à 0,01 va de 0,003 à 0,010 pour K2, K≥3 et S (erreur-type ≈ 0,006). K≥3 n'est pas dans la table : il atteint 0,97 à 1,00 quand environ 5 hôtes tombent ensemble, mais seulement 0,14 quand 2 hôtes tombent ensemble. Sorties : `calc/sim_pool_out1.txt` (sha256 `e58c0d36…788d`) et `calc/sim_pool_out3.txt` (`67b944ea…5a36`). Le lot principal a été arrêté à sa limite de temps ; les 4 tâches H0 restantes ont été relancées à 300 réplications.

**Lecture.**
1. Ma calibration retrouve le chiffre d'ADR-0029 pour le scénario B à 10 unités et 16 semaines (0,91 contre 0,91). Ce n'est pas le cas pour le scénario C (0,37 contre 0,22) : les hétérogénéités de taux diffèrent.
2. **K2 se sature quand le pool grandit**, et plus encore quand les ajouts sont *exposés*. K2 compte une fenêtre d'incident une seule fois ; sous rotation, les épisodes d'incident de nombreuses unités exposées se recouvrent au hasard et gonflent la loi nulle de K2 [inféré, sur le mécanisme].
3. **S tient à toutes les tailles**, et fait aussi bien que K2 quand l'incident ne touche que 2 hôtes. C'est la seule des trois statistiques qui ne perd dans aucun scénario simulé.
4. Ajouter des unités hors du mode commun coûte dans tous les cas : avec 2 hôtes touchés, la puissance passe de 0,93 à environ 0,66 entre 10 et 25 unités.
5. L'option B (seuil 0,0025) retire environ 10 points à BTC dans la cellule cible (0,91 → 0,81) et environ 27 points en stress (0,57 → 0,30).

**Recommandation.**
- Garder le pool confirmatoire BTC à 10 unités pour S2-bis, comme prévu.
- Élargir les trois types de sources dans des classes ou des unités exploratoires.
- Si le pool BTC doit grandir, faire évaluer par SIM-PUISSANCE-BIS la statistique **S en règle**, avant le sceau. S reste fidèle à K&L et à Littlewood et Miller : elle compte des coïncidences de défaillances entre paires de sources.

**Limites.** Le modèle est homogène et synthétique : sans couche d'observateurs, sans censure, sans garde d'information. S pèse lourd sur les fenêtres où beaucoup d'unités tombent ensemble ; elle est donc plus sensible aux modes communs résiduels d'observateurs que le quorum laisse passer. La garde « au moins 2 runs » et la sensibilité (v) d'ADR-0029 doivent s'y appliquer.

### 3.5 Débit à 4 observateurs et 4 actifs

Budget par observateur [calc] : environ 12 hôtes × 4 actifs, soit environ 48 requêtes par minute ; par hôte, 4 requêtes par minute et par IP.
- **CoinGecko** : une seule requête groupée (`ids=bitcoin,ethereum,usd-coin,tether`), obligatoire. Avec 4 requêtes séparées plus les reprises, on sortirait de « 5 to 15 » par minute (C5).
- **Bitfinex** : un dépassement bloque l'IP 60 s, ce qui ferait une panne sur 1 à 2 fenêtres pour les 4 actifs ; une seule requête multi-symboles est préférable.
- **Autres hôtes** : soit des requêtes séparées décalées de ≥ 1 s par actif (Kraken lu à ≤ 1/s, worker [2nd]), soit une requête groupée là où l'API l'admet.

**Règle à sceller** : la forme de requête par (hôte, actif) est fixée au paquet. La requête BTC de S2 est gardée telle quelle là où c'est possible. Un regroupement imposé par le débit est déclaré : il rend les pannes identiques entre actifs du même hôte, sans effet sur R1 par classe, mais il augmente la corrélation entre classes. La séquence fixe et Holm restent valides (C6). Le pool de fils doit absorber environ 50 lectures concurrentes dans δ.

### 3.6 Ce qu'il faut pré-enregistrer (en plus du paquet d'ADR-0029 §2.8)

1. La liste des classes, le rôle de chacune (F1 confirmatoire, F2 séquence fixe, F3 exploratoire) et la phrase « R1 discrimine = BTC seul ».
2. Le pool par classe : hôte = nom d'hôte, variantes SVR fusionnées, paires stable/stable exclues, devise de cotation en champ.
3. La forme de requête par (hôte, actif) et les regroupements imposés par le débit.
4. τ et σ par (actif, classe de source) : règle CALIB-ACTIFS, planchers « seuil de déviation », σ = 1,5 × heartbeat, catégorie « borné par conception ».
5. La variable d'état P_j, son seuil conditionnel et la sensibilité « unités USD seules ».
6. La statistique de test, K≥2 ou S, choisie **avant** le sceau. Si le pool BTC dépasse 10 unités, la puissance à la cellule cible est recalculée par SIM-PUISSANCE-BIS.
7. Pour F2 : la cellule cible ETH et sa puissance, imprimée. Pour F3 : la fréquence attendue de NON ÉVALUABLE, mesurée par SIM-NIVEAU-BIS.
8. La règle de rotation jointe par hôte pour toute statistique multi-classes (option C en sensibilité).
9. La variante de rotation non enroulée de Harris, en sensibilité de niveau (C7).

**Coût** : aucun VPS de plus. Environ +300 à 500 lignes pour la collecte (décodeurs par actif, fixtures) et +200 pour le rendu multi-classes [inféré, par analogie avec ADR-0029 §3]. Un lot CALIB-ACTIFS d'environ 200 lignes. Journaux environ ×4 (environ 40 Go par observateur et par mois au plus [inféré sur l'estimation d'ADR-0029 §3], sous les quotas lus). Le jalon du sceau est décalé d'une à deux semaines.

**Risques** :
- F2 est vide si BTC ne rejette pas.
- F3 est presque sûrement NON ÉVALUABLE en l'absence de décrochage.
- Une calibration sur clôtures de bougies peut sous-estimer la dispersion à l'instant de lecture : le facteur 1,5 la couvre, sans garantie.
- Coinbase n'a pas de `USDC-USD` : le pool USDC est plus petit.
- La dérive de τ entre 2025-2026 et la campagne est une dérive de régime déclarée.

## 4. Ce qui reste incertain

- La puissance réelle : mes simulations sont synthétiques et homogènes, sans couche d'observateurs ; elles orientent, elles ne fondent rien.
- L'âge réel des flux Chainlink (lecture RPC refusée) ; les paires USD de Binance et Bitfinex (non lues ici ; je suppose, sans l'avoir vérifié, que Binance n'a pas de USDT/USD fiat [inféré]).
- **Déviation au brief déclarée** : en plus du rapport et de `web/`, j'ai écrit un dossier `calc/` (script de simulation, listes de tâches, sorties) dans mon dossier P6-MESURE. Aucune écriture dans le dépôt, aucune opération git.
- L'existence d'un historique 1m public pour assez de places stable/USD.
- Le comportement des agrégateurs (CoinGecko, DefiLlama) sur les stables pendant un décrochage, non documenté sur pièce.
- La validité du niveau des rotations sur des séries non stationnaires (C7) : SIM-NIVEAU-BIS la mesurera.

## 5. Trois questions à l'investisseur

1. **Acceptez-vous que seul BTC décide**, qu'ETH ne soit « confirmé » qu'à la suite d'un rejet BTC, et que les stablecoins soient publiés comme *mesure exploratoire* dans S2-bis ? L'alternative, quatre décisions de même rang, réduit la capacité de BTC à détecter le type d'incident visé, ou allonge la campagne.
2. **Voulez-vous une mesure stablecoin qui parle des décrochages ?** En 16 semaines calmes, elle dira surtout « rien à signaler, information insuffisante ». Pour qu'elle conclue, il faudrait une campagne plus longue ou une campagne déclenchée par un événement, à décider à part.
3. **Pool plus grand ou pool plus ciblé ?** Ajouter 5 à 15 sources aide seulement si elles partagent l'infrastructure qu'on veut tester. Sinon, cela dilue le signal et demande soit plus de semaines, soit une statistique différente fixée d'avance. Préférez-vous la couverture (beaucoup de sources) ou la décision (un pool BTC resserré) ?
