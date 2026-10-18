# Avis de l'advisor du lot GEL-COLLECTEUR-1 (hôte Binance, bloc du témoin, Q-C-07) (transcrit)

> Transcription par l'orchestrateur le 2026-10-18 15:17:59 UTC du fichier s2bis/gel/AVIS-ADVISOR.md ; contrôle FM-1.1 du transcript du advisor par le fm11.py versé : fragments_l51_l14 = 0 ; modèle résolu : claude-fable-5-1 (37 occurrences, aucune autre) ; 20 citations de pages web non versées passées de « » à “ ” (précédent du 2026-10-04). Texte ci-dessous avec 20 retouche(s) (E35, E38) : noms de marqueur de dette et locutions de la gate S-G4 cités en clair, mis en code, segments de code à doubles accents graves réécrits en segments simples, heures sans date mises en code (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Avis advisor — lot GEL-COLLECTEUR-1 (gel du collecteur de S2-bis, Q-C-06)

Advisor `claude-fable-5-1`, effort `medium` (CLAUDE.md §7). Date : 2026-10-17. Pièces lues : celles du brief, aux
lignes indiquées, plus `s2bis/shogen_s2bis/collecte/entree.py`, `config.py`, `lecture.py`, `secondaire.py` et le reste
de `decodeurs.py` (nécessaires pour juger ce qu'une “forme” peut porter). Aucune pièce de la liste D.2 ouverte ;
aucune commande git ; rien d'écrit hors de ce fichier. Niveaux : [lu] pièce lue ; [inféré] déduction de l'advisor ;
[non lu] fait dont la source n'est pas dans le lot.

## Q-A. Hôte de l'unité “binance”

Faits.
- `api.binance.com` (hôte du harnais S2) rend HTTP 451 “Service unavailable from a restricted location” depuis le
  poste de mesure ; les valeurs mesurées viennent de `data-api.binance.vision` ; l'inscription de cet hôte comme unité
  “binance” est « une décision, non prise ici » [lu, `docs/adr-0029/g0-calib/PAIRES-ET-TEMOIN.md:37`, `:131`].
- `data-api.binance.vision` : même chemin que `api.binance.com` ; documentation Binance : “For APIs that only send
  public market data, please use the base endpoint https://data-api.binance.vision” ; “These URLs do not require any
  authentication” ; limite `REQUEST_WEIGHT` 6000/min, poids 2 par symbole ; réserve : doc lue sur le dépôt GitHub
  `binance-spot-api-docs`, pas sur `developers.binance.com` [lu, `PAIRES-ET-TEMOIN.md:44`].
- `ticker/price` ne porte aucun horodatage sur l'un comme sur l'autre hôte [lu, `:44`] : la classe `sans_horodatage`
  du décodeur `binance_*` ne change pas [lu, `s2bis/shogen_s2bis/collecte/decodeurs.py:267`, `:279-280`, `:290`].
- L'unité du pool s'appelle “binance” et l'unité R1 est « le nom d'hôte de configuration, jamais l'adresse IP »
  [lu, `docs/adr-0029/ADR-0029-campagne-S2-bis.md:168`] ; « la requête BTC de S2 est gardée telle quelle là où c'est
  possible » [lu, `:236`].
- État du fichier : les quatre formes Binance pointent encore `api.binance.com` [lu, `s2bis/config/formes-pool.json:2`,
  `:9`, `:10`, `:11`] ; `hote` est un champ libre `[a-z0-9.-]{1,253}` [lu, `entree.py:47`, `:95`] ; le nom de la forme
  (`binance_btc`…) est indépendant de l'hôte, donc le choix n'interagit pas avec SHOGEN-S2BIS-NOM-FORME-1 [lu,
  `docs/adr-0028/ANNEXE-B-items.md:1983`] [inféré].
- Q-C-08 adoptée : liste fermée de remplaçants par unité au paquet, décodeurs au collecteur dès le gel, lus par le
  processus secondaire hors du vote, bascule avant le sceau seulement, rodage refait selon Q-C-06 [lu,
  `docs/adr-0029/g0-collecte/PROPOSITION.md:347-351` ; `docs/adr-0029/g0-collecte/AVIS.md:97`]. Un remplaçant refait
  7 jours de rodage ; une correction du chemin de lecture refait les 14 jours [lu, `AVIS.md:95` ; ADR `:224`, `:226`].

Options.
1. `data-api.binance.vision` au gel. Pour : seul hôte qui a répondu depuis le poste de mesure ; documenté par Binance
   comme point public sans clé, ce qui est exactement l'invariant « sans clé » du pool ; même chemin, même décodeur,
   zéro code. Contre : rupture avec la requête S2 (déclarée, l'ADR l.236 ne l'exige que « là où c'est possible », et
   ici ce n'est pas possible : 451) ; la bonne réponse depuis des hôtes européens n'est pas mesurée (le poste de
   mesure n'est pas localisé dans les pièces lues) [non lu].
2. `api.binance.com` au gel. Pour : continuité S2. Contre : 451 mesuré ; si les observateurs européens sont aussi
   “restricted”, l'unité binance est morte dès le rodage et la correction d'hôte, qui touche le chemin de lecture,
   refait 14 jours (AVIS l.95) ; on paie le délai maximal pour une information déjà connue.
3. Option 1 avec `api.binance.com` écrit comme remplaçant (Q-C-08). Coût nul : même chemin, décodeur existant ;
   une bascule éventuelle coûte 7 jours (remplaçant) et non 14 (correction). Limite : si 451 vient d'une géolocalisation
   de l'adresse source, le remplaçant répondra 451 aussi depuis l'Europe ; il ne vaut que contre une panne propre à
   `data-api.binance.vision` (DNS, TLS, retrait du point d'accès), pas contre la restriction géographique [inféré].
   Les hôtes de secours `api1`–`api4.binance.com` que Binance documente ne sont pas dans les pièces lues [non lu] : ne
   pas les inscrire sans lecture.

Risques de l'option retenue.
- Le rodage est l'instrument prévu : codes HTTP par (hôte, actif) et par observateur sont des lectures admises [lu,
  ADR `:223`] ; un 451 depuis un seul observateur relève de R-b (remplacement de l'observateur, jamais retrait de
  l'unité) [lu, ADR `:226`] ; un 451 partout relève de la bascule vers le remplaçant avant le sceau.
- Deux hôtes d'un même opérateur partagent sans doute transport et amont : “chemin de LECTURE ≠ amont” [lu, ADR
  `:168`] ; le remplaçant ne crée aucune unité nouvelle, il reste la même unité “binance”.
- Le smoke (`smoke`, une lecture par forme sans prix) et `capture` sont admissibles avant le gel pour vérifier que les
  quatre formes répondent 200 depuis un hôte européen [lu, `entree.py:30-33`] ; le faire avant le gel évite le cas 2.

**Recommandation Q-A** : inscrire `data-api.binance.vision` dans les quatre formes `binance_*` (btc, usdc, usdt, eth),
déclarer l'écart à la requête S2 (451), et écrire `api.binance.com` comme remplaçant Q-C-08 de l'unité binance
(même chemin, même décodeur, hors du vote) ; vérifier par `smoke` depuis un hôte européen avant le gel.

## Q-B. SHOGEN-S2BIS-TEMOIN-BLOC-1 : dater une lecture on-chain du témoin

Faits.
- Item : « un champ bloc dans l'extra du relevé, lu par eth_blockNumber ou dans la réponse, ≈ 30 lignes » ; échéance
  “au plus tard le gel du collecteur” [lu, `ANNEXE-B-items.md:1980`]. Les décodeurs `_uniswap` et `_curve` rendent
  `ts_source` None et le notent : “Le bloc lu n'est pas rendu : aucun instant de source” [lu, `decodeurs.py:239`,
  `:243`, `:258`].
- Architecture : **une forme = une requête HTTP = une lecture** (“une lecture par forme”, `_lecteur` construit une
  `Requete` unique et `appliquer` décode son seul corps) [lu, `entree.py:178-180`, `:184` ; `decodeurs.py:351-356`] ;
  `Connection: close` sur chaque requête [lu, `http.py:44`] ; le corps d'un `eth_call` est fixé à “latest” et la
  forme doit porter **ce corps exact** (`corps-du-decodeur`) [lu, `decodeurs.py:194-201`, `:261-262` ;
  `entree.py:27-28`, `:102-103`]. Une unité on-chain = un hôte RPC, bijection contrôlée (`rpc-par-unite`) [lu,
  `entree.py:83-88`, `:104` ; ADR `:174`]. Un relevé exige un prix fini > 0 et un extra de chaînes [lu,
  `decodeurs.py:317-330`].
- Budget : délai 10 s par requête, au plus cinq lectures séparées par hôte et par fenêtre, requête groupée quand
  l'API l'admet [lu, ADR `:235-236`] ; un relevé par actif au plus [lu, `decodeurs.py:333-335`].
- Hôtes RPC du témoin : `eth.drpc.org` (Uniswap), `rpc.mevblocker.io` (Curve) [lu, `formes-pool.json:33-34`].
- Le recalc (RB-2) datera la mesure à partir du bloc ; l'horodatage du bloc n'est donc pas nécessaire au collecteur
  [énoncé du brief].

Options.
1. `eth_blockNumber`, puis `eth_call` épinglé au bloc (le troisième aller, `eth_getBlockByNumber`, est inutile
   puisque RB-2 date) : datation exacte. Contre : deux ou trois requêtes séquentielles dans **une** lecture, ce que
   ni `http.lire` ni `_lecteur` ni la règle `corps-du-decodeur` ne permettent : c'est un changement du chemin de
   lecture (nouveau type de forme à corps dépendant d'une réponse précédente), bien au-delà des “≈ 30 lignes” de
   l'item, à relire en G2 et à roder 14 jours ; deux allers sous le même délai de 10 s ; les RPC publics sont
   répartis sur plusieurs nœuds : un `eth_call` épinglé sur un bloc que le nœud suivant n'a pas encore vu rend une
   erreur (“header not found”) et la lecture entière devient `panne_decode` [inféré ; non mesuré sur ces hôtes].
2. Requête JSON-RPC groupée `[eth_blockNumber, eth_call latest]` en un aller. Pour : une requête, une lecture, un
   corps exact scellé (il suffit d'étendre `eth_call`/`CORPS` à un tableau et le décodeur à une réponse tableau
   appariée par `id`) : tient dans l'architecture et dans l'ordre de grandeur de l'item ; un seul appel RPC par
   fenêtre et par hôte, budget inchangé ; le bloc va en extra (`"bloc": "<décimal>"`, chaîne, règle de `_releve`).
   Contre : pas d'atomicité : JSON-RPC 2.0 autorise le serveur à traiter un lot dans n'importe quel ordre ; un bloc
   peut passer entre les deux éléments (écart d'un bloc, ~12 s, borne réaliste sur un même nœud) [inféré] ; les RPC
   publics peuvent refuser ou limiter les lots sans clé : **non lu** pour `eth.drpc.org` et `rpc.mevblocker.io`.
   Variante 2′ (encadrement) : `[eth_blockNumber, eth_call latest, eth_blockNumber]` ; si les deux numéros sont égaux,
   le bloc est certain (sous l'hypothèse de traitement séquentiel sur un même nœud, non garantie par la spec) ; sinon
   l'extra porte `bloc_avant` et `bloc_apres` et RB-2 tranche (intervalle). Coût : un sous-appel de plus, même aller.
3. `eth_call` “latest” et `eth_blockNumber` par une lecture séparée. Contre : une forme = un relevé avec prix > 0,
   un numéro de bloc n'est pas un relevé (`_releve` refuse) : il faut un type de forme ou de relevé nouveau au FORMAT ;
   deux lectures concurrentes sur le même hôte sans ordre garanti (fils `concurrent.futures`, ADR `:235`) : le bloc
   lu n'encadre rien ; double la charge de l'hôte RPC pour une information plus faible qu'en 2.

Risques de l'option retenue (2 / 2′).
- Lot refusé par un hôte : la lecture est `panne_http` ou `panne_decode` dès le smoke ; c'est précisément ce que
  `smoke`/`capture` montrent sans prix avant le gel [lu, `entree.py:30-33`]. Si l'un des deux hôtes refuse le lot,
  ne pas mélanger : choisir un hôte RPC public qui l'admet (remplaçant Q-C-08 de l'unité, bijection `rpc-par-unite`
  conservée), plutôt qu'un décodeur à deux régimes.
- Semantique de `bloc` à écrire au FORMAT : « numéro de bloc courant du nœud dans la même requête groupée, non
  atomique avec l'appel ; écart attendu ≤ 1 bloc » ; `ts_source` reste None (le collecteur n'a pas l'horodatage) ;
  RB-2 date par le bloc (un `eth_getBlockByNumber` au recalc, ou une source de blocs), item TEMOIN-RECALC-1 voisin
  [lu, `ANNEXE-B-items.md:1982`].
- Apparier par `id` et non par position (la spec n'impose pas l'ordre des réponses) ; refuser un lot incomplet ou
  un élément `error` : panne entière, cohérent avec `_groupe` (« la lecture entière est une panne ») [lu,
  `decodeurs.py:152-161`].
- Tests : fixtures d'un lot ordonné, inversé, incomplet, avec `error`, et numéros encadrants différents (2′).

**Recommandation Q-B** : option 2, de préférence sous la variante 2′ (encadrement par deux `eth_blockNumber`), en une
seule requête groupée par forme, bloc(s) en extra en chaînes décimales, sémantique “non atomique” écrite au FORMAT,
appariement par `id` ; prise en charge du lot vérifiée par `smoke` sur les deux hôtes RPC avant le gel ; option 1
écartée (changement du chemin de lecture, nœuds répartis), option 3 écartée (pas un relevé, pas d'ordre).

## Q-C. Q-C-07 : USDC, « les deux mesures et leur écart »

Faits.
- Lecture de l'avis G0 : « contre le dollar réel » = classe USDC/USD des places fiat (ADR l.171) ; “telle que la DeFi
  la consomme” = Chainlink USDC/USD (classe « borné ») et ensemble témoin sur chaîne (l.172) ; « leur écart » = écart
  au pair des médianes des classes USD (Q-R-04) et P_j ; “si oui, aucune forme nouvelle” [lu, `AVIS.md:96`] ; la
  traduction technique était absente de l'ADR, à trancher avant le gel [lu, `PROPOSITION.md:343-346`].
- ADR : pool USDC/USD = hôtes du paquet qui servent la paire ; trois places fiat seulement (Kraken, Bitstamp,
  Bitfinex ; Gemini liste la paire ; aucune chez Coinbase) ; N ≥ 4 dépend des agrégateurs et de l'oracle, limite
  écrite [lu, ADR `:173`] ; ensemble témoin USDC/USDT chez OKX et sur chaîne (Uniswap, Curve), hors des classes USD
  et hors du vote, porteur de P_j [lu, ADR `:174`].
- `formes.json` contient les trois composantes : places USDC/USD `kraken_usdc`, `bitstamp_usdc`, `gemini_usdc`,
  `binance_usdc`, Bitfinex `tUDCUSD` dans `bitfinex_groupe`, agrégateurs `coingecko_groupe` et `defillama_groupe`
  (usd-coin) [lu, `formes-pool.json:9`, `:15`, `:20`, `:23`, `:25-27`] ; `chainlink_usdc` [lu, `:30`] avec le plafond
  1,05 porté en extra, jamais appliqué, classe « borné » jugée au recalcul [lu, `decodeurs.py:53`, `:172-184`,
  `:300`] ; témoin `okx_usdc_usdt`, `uniswap_usdc_usdt`, `curve_usdc_usdt` en classe `temoin` [lu,
  `formes-pool.json:32-34` ; `decodeurs.py:302-304`].
- L'écart est un calcul sur ces relevés, pas une lecture : il relève de RB-2 (TEMOIN-RECALC-1 : filtrer la classe
  `temoin` hors des classes USD et du vote, « le filtrage des relevés au recalcul ne l'est pas encore ») [lu,
  `ANNEXE-B-items.md:1982`].

Lecture et risques.
- Je confirme : les deux mesures existent déjà comme formes ; l'écart n'est pas une forme. Aucune forme manquante au
  gel pour Q-C-07.
- Ce qui manque n'est pas au collecteur : (a) la définition écrite de l'écart au paquet (écart au pair de la médiane
  USDC/USD par classe ; écart entre la médiane fiat et Chainlink ; P_j du témoin), portée par RB-2/Q-R-04 ; (b) le
  filtre TEMOIN-RECALC-1 ; (c) la datation du témoin (Q-B) sans laquelle « leur écart » entre une place fiat
  horodatée et un relevé on-chain non daté est fragile [inféré].
- Limite déclarée à garder visible : la classe fiat USDC/USD ne compte que trois à quatre places (ADR `:173`), donc
  « le dollar réel » repose en partie sur les agrégateurs ; c'est écrit à l'ADR, à recopier au paquet avec Q-C-07.

**Recommandation Q-C** : confirmer la lecture de `AVIS.md:96`, aucune forme nouvelle au gel de `formes.json` ; écrire
au paquet la traduction (classes et calcul de l'écart) et renvoyer l'écart à RB-2 (Q-R-04, TEMOIN-RECALC-1).

## Recommandation (une ligne par question)
- Q-A : `data-api.binance.vision` dans les quatre formes `binance_*`, écart à S2 déclaré, `api.binance.com` écrit comme
  remplaçant Q-C-08 hors du vote, `smoke` depuis l'Europe avant le gel.
- Q-B : option 2 (requête JSON-RPC groupée en un aller), variante encadrée `[blockNumber, call, blockNumber]`, bloc(s)
  en extra, non-atomicité écrite au FORMAT, prise en charge du lot vérifiée par `smoke` sur les deux hôtes RPC.
- Q-C : lecture confirmée, aucune forme nouvelle ; l'écart se définit au paquet et se calcule à RB-2.
