# Les mesures pilotes S2 — conception de l'instrument (v0, 2026-08-05)

> Statut : **conception**. Ce document dessine l'instrument du jalon S2
> (05 §S2) — le harnais R1/R2 jetable qui tranche — pas le produit, pas son
> code. Rien ici n'est proven ; l'instrument n'a pas tourné, donc rien de
> l'instrument n'est tested. Les seuls énoncés d'observation sont des
> mesures datées du 2026-08-05, citées avec leur passe.
>
> **Provenance et règle d'entrée.** Trois passes de workers (Opus 4.8) ont
> mesuré et lu le 2026-08-05 (faisabilité des sources ~11:44–11:50 UTC ;
> observables R2 ~11:42–11:46 UTC ; lectures R1 aux PDF). Cinq
> vérificateurs indépendants (Opus 4.8), à l'aveugle, ont re-mesuré ou relu
> chaque affirmation empirique le même jour : V1 (DNS→ASN, double
> attribution RIPEstat + Team Cymru), V2 (12 sondes d'endpoints,
> ~12:02–12:04 UTC), V3 (5 pages d'amont), V4 (citations K&L/L&M/E&L aux
> PDF détenus, texte **et** rendu), V5 (deux dettes bibliographiques).
> **N'entre ici comme fait que ce qu'une re-vérification a re-établi
> (verdict CONFIRME)** ; ce que la re-mesure a corrigé est écrit à la
> valeur re-mesurée — frontière de passe : le briefing est une piste, la
> re-mesure est la mesure ; ce qui n'a pas été re-établi est marqué « non
> re-établi cette passe » et ne fonde aucune conclusion. La passe de
> rédaction (2026-08-05) a en outre grepé les chaînes citées sur les PDF
> détenus (`biblio/`) et re-décodé elle-même les deux payloads conservés
> (`chainlink.json`, `pyth.json`) aux valeurs rapportées.

## 1. Objet et non-objet

**L'objet** : un instrument qui tranche la question posée par 05 §S2 —
les axes R2 sont-ils observables en pratique, et le test R1 discrimine-t-il
quelque chose sur données réelles ? Si non, le cœur différenciant est une
hypothèse morte, et il faut le savoir avant toute ligne de produit.

- **Jetable** : le harnais n'est pas un ancêtre du produit ; il meurt
  après le rapport.
- **Résultat négatif = résultat** : « les axes ne discriminent pas »
  s'écrit avec les chiffres et déclenche la révision de 04.

**Les non-objets**, pour que personne ne lise plus que ce qui est là :

1. Pas de témoignage canonique ni de transport attesté (S3) : la collecte
   S2 est une lecture HTTPS nue par le harnais. L'historique produit vaut
   pour la faisabilité de la mesure ; ce n'est pas un lot de témoignages,
   et aucun résidu de transport A(...) n'est engagé par la collecte.
2. Pas de verdict de quorum ni d'estimateur de confinement (S4).
3. Pas de notation d'amont : le certificat nomme, il ne note pas
   (ADR-0007).
4. Pas de calcul on-chain (ADR-0006) ; la seule interaction chaîne est une
   lecture `eth_call` par RPC public, remontée en décision (§9.2).

## 2. La classe de fait pilote et son homogénéité

La classe candidate est « prix spot BTC contre dollar », la classe de
faits du premier produit (05 §S2). La re-mesure du 2026-08-05 montre
qu'elle n'est pas homogène :

- Sur les **12 flux de cotation** re-mesurés (11 sources répondantes —
  OKX en fournit deux), **10 rapportent USD et 2 rapportent USDT** :
  Binance spot (`BTCUSDT`) et le ticker spot OKX (`BTC-USDT`) [V2].
  Kraken cote `ZUSD` (USD dans sa nomenclature à préfixe Z) sous la clé
  retournée `XXBTZUSD`.
- L'hétérogénéité est aussi **interne aux agrégats** : la méthodologie
  CoinGecko re-établie construit son prix par VWAP de tickers BTC/USD,
  BTC/USDT, BTC/USDC et BTC/EUR après filtre d'outliers (§4.3) — un flux
  étiqueté USD peut embarquer de l'USDT par construction.

Conséquences de conception, indépendantes de la décision de classe :

- **La devise de cotation est un champ du relevé, jamais une constante de
  la classe.** Le décodeur l'enregistre par flux (A(typer-correctness)).
- L'écart USDT/USD est un mode commun potentiel des flux USDT entre eux,
  que la statistique (2a) de §4.2 rendrait visible si la classe les
  mélange. (À l'instant re-mesuré, les deux flux USDT ne bornaient pas la
  fourchette du pool — le maximum était Bitfinex, en USD ; un seul
  instant, aucune inférence.)

**La définition de la classe est une décision remontée (§9.4)** : BTC/USD
strict (écarte les 2 flux USDT, dont la place au plus gros flux nominal),
classe « BTC/USD-stable » avec devise marquée par flux, ou deux classes.

## 3. Le pool de sources

### 3.1 La table re-mesurée — observé le 2026-08-05, ~12:02–12:04 UTC (V2, re-mesure aveugle)

| # | source | endpoint (rejouable) | sans clé | HTTP | valeur lue (devise) | horodatage porté | nature |
|---|---|---|---|---|---|---|---|
| 1 | Binance | `api.binance.com/api/v3/ticker/price?symbol=BTCUSDT` | oui | 200 | 64 102,40 (USDT) | — (absent du payload) | place primaire |
| 2 | Coinbase Exchange | `api.exchange.coinbase.com/products/BTC-USD/ticker` | oui | 200 | 64 050,65 (USD) | 12:03:37.68Z | place primaire |
| 3 | Kraken | `api.kraken.com/0/public/Ticker?pair=XBTUSD` | oui | 200 (`error:[]`) | 64 025,00 (USD) | — | place primaire |
| 4a | OKX ticker | `www.okx.com/api/v5/market/ticker?instId=BTC-USDT` | oui | 200 (code 0) | 64 109 (USDT) | ~12:03Z | place primaire |
| 4b | OKX indice | `www.okx.com/api/v5/market/index-tickers?instId=BTC-USD` | oui | 200 (code 0) | 64 046,3 (USD) | ~12:03Z | indice composé par la place (composition non établie) |
| 5 | Bitstamp | `www.bitstamp.net/api/v2/ticker/btcusd/` | oui | 200 | 64 046,34 (USD) | epoch 1785931433 | place primaire |
| 6 | Gemini | `api.gemini.com/v1/pubticker/btcusd` | oui | 200 | 64 052,73 (USD) | epoch ms 1785931380000 | place primaire |
| 7 | Bitfinex | `api-pub.bitfinex.com/v2/ticker/tBTCUSD` | oui | 200 | 64 122 (USD) | — | place primaire |
| 8 | CoinGecko | `api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_last_updated_at=true` | oui (cette passe, sans 429) | 200 | 64 023 (USD) | epoch 1785931310 | agrégateur |
| 9 | DefiLlama | `coins.llama.fi/prices/current/coingecko:bitcoin` | oui | 200 | 64 028,97 (USD par convention d'endpoint, non étiqueté dans le JSON) | epoch 1785931300 | agrégateur de 2ᵉ niveau |
| 10 | CryptoCompare | `min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD` | **non** | **401** « API key required » | — | **écartée** |
| 11 | Pyth (Hermes) | `hermes.pyth.network/v2/updates/price/latest?ids[]=0xe62df6c8b4a85fe1a67db44dc12de5db330f7ac66b72dc658afedf0f4a415b43&parsed=true` | oui | 200 | 64 051,12 ± 21,40 (USD) | epoch 1785931439 (12:03:59Z) | oracle |
| 12 | Chainlink | `eth_call latestRoundData()` (`0xfeaf968c`) sur `0xF4030086522a5bEEa4988F8cA5B36dbC97BeE88c` via `ethereum-rpc.publicnode.com` | oui | 200 | 64 019,74 (USD) | `updatedAt` = 0x6a732667 (12:02:47Z) | oracle, lu par RPC public (§9.2) |

Notes (toutes V2, sauf mention) :

- **Cohérence croisée** : les 11 répondantes tiennent dans
  [64 019,74 ; 64 122,00], soit ~102 USD ≈ 0,16 % d'écart, et tous les
  horodatages décodables tombent le 2026-08-05 entre ~12:02 et ~12:04 UTC,
  mutuellement cohérents.
- **CryptoCompare** : point critique re-établi — 401 sans clé, aucune
  valeur retournée ; écartée du pool sans-clé. (Le message d'erreur
  renvoie vers developers.coindesk.com — rebranding CoinDesk.)
- **Bitfinex, anomalie de forme** : le tableau v2 renvoie **11 champs là
  où le schéma documenté en compte 10** ; le 11ᵉ (1358182043000 → 2013)
  est hors-schéma ; `LAST_PRICE` = position 7 (index 6), intact. Seul
  écart de forme observé sur les 12 sondes. Règles de décodage qui en
  découlent : **position fixe, jamais « dernier élément »** ; clé
  retournée, jamais clé demandée (Kraken normalise `XBTUSD` →
  `XXBTZUSD`).
- **Pyth** : décodage `price · 10^expo` — re-décodé en passe de rédaction
  depuis les octets conservés : 6 405 111 500 002 × 10⁻⁸ = 64 051,12,
  conf 21,40 ; blocs `binary` (VAA hex) et `parsed` tous deux présents ;
  id retourné = id demandé (feed BTC/USD).
- **Chainlink** : réponse = 5 mots de 32 octets ; `answer` = 2ᵉ mot —
  re-décodé en passe de rédaction : `0x5d2935dcb94` = 6 401 973 668 756,
  8 décimales ; `updatedAt` = 4ᵉ mot ; `roundId` phase-encodé (phase 7).
  La cadence de publication du feed n'est **pas** une horloge de fenêtre
  et ses paramètres (déviation/heartbeat) ne sont pas établis sur pièce
  (§10.6) : l'instrument **stocke `roundId` et `updatedAt`**, jamais le
  seul prix.
- Aucune clé ni token envoyé nulle part ; un User-Agent navigateur
  (non-credential) n'a débloqué aucun 403 — les statuts « sans clé »
  tiennent tels quels.

### 3.2 Le graphe d'amonts : des nœuds et des fonctions

- **Nœuds** (places primaires, seules productrices d'observations de
  marché dans ce pool) : Binance, Coinbase, Kraken, OKX, Bitstamp,
  Gemini, Bitfinex — 7.
- **Fonctions de nœuds** :
  - **CoinGecko** = f(tickers de places) — estimateur re-établi (§4.3) :
    filtre MAD puis VWAP des tickers restants. L'intégration de Binance
    chez CoinGecko est re-établie (page exchange ouverte : 1 372 paires
    au 2026-08-05 — chiffre daté, qui dérive) ; l'appartenance des
    tickers Binance au ticker-set exact du VWAP BTC n'est pas montrée par
    la page : arête `basis:doc`, granularité « intégration », pas
    « ticker-set ».
  - **DefiLlama** = f(CoinGecko) pour BTC — re-établi (llms-full.txt,
    §4.3) : pour BTC, `coins.llama.fi` n'est pas un chemin d'amont
    distinct de `api.coingecko.com` ; les deux flux comptent comme un
    seul chemin d'amont.
  - **Pyth** = médiane sur votes de publishers (mécanisme re-établi,
    §4.3), panel déclaré ; **Coinbase re-établi comme publisher au niveau
    réseau** ; l'attribution au feed BTC/USD précis n'est pas établie
    (dette §10.3) : arête `basis:doc`, granularité « réseau ».
  - **Chainlink** = fonction d'amonts **non établis cette passe** (la
    lecture worker d'une composition « agrégateurs/vendors » n'a pas été
    re-établie) : aucune arête d'amont n'est portée ; le nœud est marqué
    « amont non documenté sur pièce » (dette §10.6).
- **Chemin de lecture ≠ amont** : pour la lecture on-chain, l'ASN mesuré
  (§4.1) est celui du fournisseur RPC (`ethereum-rpc.publicnode.com`) —
  une infrastructure de chemin de lecture, pas l'amont du feed. Le
  contre-essai worker d'un second RPC (cloudflare-eth : 200 mais erreur
  JSON-RPC −32603) n'a pas été re-établi et reste au rang (c).
- Sous la règle proposée en §4.3, une arête `basis:doc` seule **ne
  partitionne pas** : elle déclenche la mesure de contenu (b) sur la
  paire. La partition de §5.6 ne fusionne qu'au rang `measured`.

### 3.3 Budgets de débit — lectures worker, non re-établies

Aucune limite de débit n'a été re-établie par une re-mesure ; la table
ci-dessous est la **lecture doc de la passe worker A (2026-08-05)**, à
re-lire avant implémentation (dette §10.9). Elle suffit au dimensionnement
de conception, qui reste très en deçà de toutes les limites lues :

| source | limite lue (worker, doc — non re-établie) |
|---|---|
| Binance | REQUEST_WEIGHT 6000/min/IP, ticker de poids 2 (lu par le worker dans la réponse `/exchangeInfo` elle-même) |
| Coinbase Exchange | 10 req/s, burst 15 |
| Kraken | ≤ 1 appel/s public |
| Bitstamp | 400 req/s, 10 000/10 min |
| Gemini | 120 req/min, burst 5 |
| Bitfinex | 10–90 req/min/endpoint ; dépassement = IP bloquée 60 s |
| CoinGecko | keyless « not suitable for scheduled polling » (doc) — décision §9.3 |
| Pyth (Hermes) | 10 req/10 s/IP — la plus contraignante lue |
| Chainlink (PublicNode) | « sans limite » = supposition (c), non vérifiée |

**Cible de conception** : 1 relevé/source/fenêtre, fenêtre ≥ 60 s → ~1
req/min/source, marge large sur toute limite lue. Les suppositions (c) du
worker (OKX 20 req/2 s ; paramètres Chainlink ; retrait du palier gratuit
CryptoCompare au 2026-05-21 ; géo-blocage 451 de Binance selon
juridiction ; PublicNode) **ne fondent rien** : à établir sur pièce ou à
abandonner en S2.

### 3.4 Les trois rangs de preuve du dossier S2

| rang | définition | statut dans ce document |
|---|---|---|
| (a) exécuté | mesuré, puis re-établi à l'aveugle | seul rang écrit comme fait ; porte passe et date |
| (b) doc | page primaire ouverte, URL et date | re-établi uniquement pour les cinq liens d'amont de §4.3 ; le reste (débits) marqué « lecture worker » |
| (c) supposition | rapporté sans pièce | listé, ne fonde rien |

C'est la même distinction que la sous-annotation `basis: measured | doc`
des arêtes R2 (§4.3) — le dossier S2 se l'applique à lui-même.

## 4. Les observables R2

### 4.1 (a) L'axe ASN/hébergeur — méthode rejouable, résultat re-mesuré

**Méthode** (trois commandes, rejouables telles quelles) :

```
Resolve-DnsName -Name <hôte> -Type A -Server <résolveur>                                # DNS
Invoke-RestMethod "https://stat.ripe.net/data/prefix-overview/data.json?resource=<IP>"  # RIPEstat
Resolve-DnsName -Name "<d.c.b.a>.origin.asn.cymru.com" -Type TXT -Server <résolveur>    # Team Cymru
```

Deux étages d'attribution croisés à dessein : Team Cymru répond par DNS
sur une base BGP distincte de RIPEstat.

**Résultat** — observé le 2026-08-05 (V1, re-mesure aveugle, hôte
Windows, résolveur 1.1.1.1 ; 5 hôtes, 8 IP testées dont 3 secondaires) :

| hôte | IP primaire (secondaire) | préfixe | ASN (RIPEstat = Cymru) |
|---|---|---|---|
| api.binance.com | 3.160.181.62 — via CNAME `d3h36i1mno13q3.cloudfront.net` | 3.160.180.0/22 | **AS16509** AMAZON-02 |
| api.exchange.coinbase.com | 172.64.151.78 (104.18.36.178) | 172.64.151.0/24 | **AS13335** CLOUDFLARENET |
| api.kraken.com | 104.17.186.205 (plage .185–.189) | 104.17.176.0/20 | **AS13335** CLOUDFLARENET |
| api.coingecko.com | 104.20.41.132 (172.66.172.219) | 104.20.32.0/20 | **AS13335** CLOUDFLARENET |
| hermes.pyth.network | 104.20.36.70 (172.66.151.6) | 104.20.32.0/20 | **AS13335** CLOUDFLARENET |

- Concordance RIPEstat ↔ Cymru : **8 IP sur 8**, aucune étape non
  attribuable ; les 4 hôtes Cloudflare le sont sur *toutes* leurs IP
  renvoyées ; les préfixes Cloudflare observés sont des allocations ARIN
  de 2014–2015, cohérentes entre elles.
- **Le fait saillant, re-établi : exactement 4 hôtes sur 5 partagent
  AS13335 (Cloudflare).** L'hors-classe unique, Binance, est un CNAME
  déterministe vers CloudFront — il reste dans la famille Amazon depuis ce
  point d'observation quel que soit l'edge ; le caveat « l'IP peut
  varier » ne le fait pas basculer.
- **Partition sur cet axe** (arithmétique sur la table, recalculable) :
  {coinbase, kraken, coingecko, pyth-hermes} ∪ {binance} → **k_eff = 2
  pour k nominal = 5, côté livraison**. Le chiffre mesure le *fronting*,
  pas l'origine (résidu 1).
- **Périmètre** : 5 des 11 hôtes du pool candidat sondés dans la passe
  re-établie. L'instrument étend la même chaîne aux 6 autres (okx,
  bitstamp, gemini, bitfinex, coins.llama.fi,
  ethereum-rpc.publicnode.com) et re-mesure à chaque quorum.

**Les sept résidus de l'observable** — un observable R2 est lui-même un
témoignage avec ses résidus (04 §4, pt 4) ; ils se publient avec lui :

1. **Fronting CDN/anycast** : l'IP observée est la couche de livraison,
   pas l'origine. Double lecture, publiée : (i) côté origine, le
   regroupement peut être un faux positif (origines possiblement
   disjointes derrière le même CDN) ; (ii) côté livraison, le mode commun
   est réel (une défaillance du CDN partagé co-interrompt les 4 chemins).
   Le certificat dit laquelle il compte ; le k_eff = 2 ci-dessus est
   explicitement « côté livraison ».
2. Même ASN ≠ même opérateur ; ASN distincts ≠ opérateurs distincts.
3. **Mono-vantage** : la re-mesure provient d'un seul point d'observation
   (un hôte, un résolveur). La sonde worker multi-résolveurs
   (1.1.1.1/8.8.8.8/9.9.9.9 → même IP Binance depuis ce point) n'a pas
   été re-établie, et ne démontrait de toute façon pas l'indépendance
   géographique — sonde négative, non comptée. L'instrument sonde
   multi-résolveurs de familles distinctes et, si disponible,
   multi-vantage.
4. **Instantanéité** : TTL court (60 s lu par le worker sur
   l'enregistrement CloudFront — non re-établi) ; l'attribution est un
   instantané daté, re-mesuré au moment de chaque quorum.
5. **Le chemin de mesure appartient à la classe mesurée** : la résolution
   passe par 1.1.1.1, opéré par Cloudflare, pour mesurer une dépendance à
   Cloudflare. Atténuation de conception : résolveurs de familles
   distinctes + attribution croisée.
6. RIPEstat et Team Cymru sont eux-mêmes des témoins (vues BGP,
   registres) ; leur concordance 8/8 du 2026-08-05 est une observation,
   pas une décharge — portée par A(asn-attribution) au registre (§8).
7. La chaîne CNAME est un fait daté : le CNAME re-établi de Binance est
   déterministe aujourd'hui et peut changer demain.

### 4.2 (b) L'axe corrélation de contenu — quatre statistiques [conception, non exécutée]

Grille commune alignée sur l'époque UTC : `t_j = [j·w, (j+1)·w)` ;
`p_s(j)` = dernier relevé de la source s dans la fenêtre j. w = 1 s pour
les flux de place, 10 s pour les agrégats. Cible N_min = 300 fenêtres
communes par paire (transformation de Fisher : SE = 1/√(N−3) ≈ 0,058 →
IC ≈ ±0,11 sur ρ ; source de manuel à enregistrer, dette §10.7).

**Erratum du 2026-09-30 (SHOGEN-REPORT-FISHER-1, ADR-0028 D3) — ajout daté : les lignes qui précèdent
sont conservées telles qu'écrites le 2026-08-05 (précédent : ADR-0023 l.3).** Le mot « Fisher » de la
rédaction du 2026-08-05 désigne la **transformation z′ = artanh(r)** (Fisher 1921, *Metron* 1:3-32 ;
primaire en procurement L-46, non détenu). Forme de manuel détenue : `biblio/INDEX.md` l.328 (Penn
State STAT 509, leçon 7, §7.8) : z′ suit approximativement N(ζ, sd = 1/√(n−3)), n étant la taille de
l'échantillon ; l'intervalle sur ζ est z′ ± t(n−3 ; 1 − α/2)/√(n−3) (quantile de Student à n−3 degrés
de liberté), soit à 95 % z′ ± t(n−3 ; 0,975)/√(n−3). À N = 300 : SE(z′) = 1/√297 ≈ 0,058 et
t(297 ; 0,975)/√297 ≈ 0,114 [calculé], soit ≈ ±0,11 **sur l'échelle z′**. Sur ρ, l'IC s'obtient par la
transformation inverse (tanh) et n'est de l'ordre de ±0,11 que près de ρ = 0 : il se resserre quand
|ρ| croît. L'énoncé antérieur « IC ≈ ±0,11 sur ρ » est **corrigé par cet erratum** (il vaut sur z′, non
sur ρ). N_min = 300 est un **choix de conception**, fixé ex ante dans ce document, non dérivé d'un
calcul de puissance (à porter au paquet de pré-enregistrement, ADR-0028 D2). Le rapport n'a jamais
publié d'IC sur ρ ; le point est corrigé avant le paquet (l'erratum doit y figurer avant son scellement).

*Ajout daté du 2026-10-02 (SHOGEN-DOC-ERRATA-P3-1 ; l'erratum qui précède est inchangé)* : « primaire en procurement L-46, non détenu » est périmé : Fisher 1921 (*Metron* 1:3-32) est versé (`biblio/INDEX.md` l.337) et lu (`docs/adr-0028/LECTURES-PARTIE-3.md`) ; il n'imprime pas « 1/√(n−3) » ; la formulation retenue est au paquet de pré-enregistrement (`docs/adr-0028/PAQUET-PREREG-S2.md` §12 pt 12 : poids N−3 sur l'échelle z, pp. 14 et 18), où figure l'erratum z′/ρ, scellé le 2026-10-02.

| stat | définition | ce qu'elle capte |
|---|---|---|
| (1) ρ_raw | Pearson des log-rendements `r_s(j) = ln p_s(j) − ln p_s(j−1)`, par paire | plancher commun, PAS discriminant : ≈ 1 pour toute paire honnête de la classe (facteur marché) ; un ρ_raw *bas* est le signal étrange |
| (2a) ρ_resid | résidus au pool `e_s(j) = ln p_s(j) − ln m_{−s,−s′}(j)`, médiane leave-two-out (k ≥ 4), Pearson des résidus | s'écarter du pool *ensemble* = signal d'amont commun |
| (2b) T, T_Δ | quantification au tick `q_s(j)`, taux d'identité T contre deux lignes de base (contrôle décalé Δ = 60 s ; collision attendue au tick) | identité répétée sur 6–8 décimales = quasi-signature de copie |
| (2c) K, z | co-aberrance : aberrant si `\|e_s(j)\| > κ·MAD_j(pool)` (κ = 5) ou staleness ; K = fenêtres co-aberrantes de même sens à lag ≤ ℓ ; z par la machinerie binomiale de §5.1 recalculée sur les résidus | fautes partagées ; un choc de marché entier est absorbé par la médiane — seules les déviations *au pool* co-occurrent |
| (2d) δ | sauts `\|r_s(j)\| > 4σ`, corrélation croisée aux lags −L..+L | **seul axe qui donne la direction** de la dépendance (qui précède qui) |

Publication par paire : ρ_raw, ρ_resid, (T, T_Δ), (K, z), δ — **l'arête
nomme sa statistique**, jamais un score fusionné (la règle « les résidus
ne se moyennent pas », transposée aux statistiques).

Résidu de l'axe : un amont qui **bruite ses copies** échappe aux quatre
statistiques — mode commun non mesuré, porté par A(axis-coverage), écrit
au certificat.

Précédent académique de (2c) — détection de copie par fautes partagées :
Dong et al., PVLDB 3(1), 2010, identité re-établie en page de titre (V5),
**corps non lu** (dette §10.1) ; le mécanisme pairwise naît dans le
prédécesseur PVLDB 2009 (piste, non attribuée). (2c) ne cite pas ce
précédent tant que le corps n'est pas lu.

**Ratification du 2026-08-20 (adjudication M1c).** L'instrument retire le
disjoint « ou staleness » du compte co-aberrant (2c) : K comptant les
co-aberrances **de même sens** (lag ≤ ℓ), la staleness — qui n'a **pas de
signe** — ne peut y entrer sans dénaturer le compte signé. La **co-staleness**
reste captée ailleurs, sans perte de couverture : par l'écart (ii) de §5.2 (R1)
et par la matrice de co-écarts φ/n₁₁ que le drapeau 2 (§5.6) consomme. Écart au
texte littéral de (2c), déclaré au rapport (`COAB_STALENESS_NOTE`) et ratifié par
l'orchestrateur (R-21).

### 4.3 (c) L'axe méthode commune — liens re-établis, règle `basis`

Les cinq faits d'amont re-établis (V3, pages ouvertes le 2026-08-05 ; les
citations des quatre pages HTML sont passées par le résumeur de fetch —
copie octets-exacts en dette §10.4 ; seul llms-full.txt est
verbatim-fiable) :

1. **CoinGecko, estimateur** : filtre d'outliers par bornes MAD, puis
   « the VWAP of all remaining tickers » (coingecko.com/en/methodology,
   fetch 2026-08-05) — familles de paires BTC/USD, USDT, USDC, EUR.
2. **CoinGecko ← Binance** : intégration re-établie
   (coingecko.com/en/exchanges/binance, fetch 2026-08-05 : table des
   marchés spot, 1 372 paires — chiffre daté) ; granularité
   « intégration », voir §3.2.
3. **Pyth, mécanisme d'agrégation** : chaque publisher émet **trois
   votes** — son prix p, p + c et p − c (c = son intervalle de
   confiance) — puis **médiane non pondérée de l'ensemble des votes** ;
   confiance agrégée par distance aux 25ᵉ/75ᵉ percentiles ; auto-décrit
   « a hybrid between a mean and a median »
   (docs.pyth.network/price-feeds/how-pyth-works/price-aggregation,
   fetch 2026-08-05). **Correction de passe** : la formulation vulgarisée
   « médiane pondérée par la confiance » est inexacte au sens strict —
   une vraie médiane pondérée et cette construction peuvent diverger
   numériquement ; ne pas la réintroduire.
4. **Pyth ← Coinbase, niveau réseau** : Coinbase est nommé parmi les
   institutions « already publishing data to Pyth Network »
   (pyth.network/publishers, fetch 2026-08-05). Rien sur le feed BTC/USD
   précis (dette §10.3).
5. **DefiLlama ← CoinGecko** : « Almost all tokens are priced using
   CoinGecko's API. » (docs.llama.fi/llms-full.txt, fetch 2026-08-05 —
   la page coin-prices-api elle-même est illisible par fetch, dette
   §10.5). BTC est un token majeur : la direction « pas un chemin d'amont
   distinct » tient.

**Forme d'enregistrement d'une arête méthode** :
`method:{estimator, outlier_rule, panel_declared, doc_url, doc_fetched,
basis:doc}`, et chaque arête R2 porte `basis: measured | doc`.

**Règle proposée** (structurante — ADR à écrire, §9.6) : une arête
`basis:doc` seule **ne réduit pas k_eff** ; elle *déclenche* la mesure (b)
sur la paire, et ne partitionne qu'une fois corroborée `measured`. C'est
la hiérarchie des rangs appliquée à l'intérieur de R2 : une déclaration
d'amont, seule, ne fait pas chuter un quorum — elle désigne où mesurer.

## 5. La statistique R1

### 5.1 Le test K&L §5, transposé — formules re-établies

Pagination re-établie (V4, texte **et** rendu ; grep de rédaction sur le
PDF détenu `biblio/knight-leveson-1986-full.pdf`) : §5 « MODEL OF
INDEPENDENCE » = pp. imprimées 12–14 (pp. fichier 13–15 ; offset
imprimée = fichier − 1). Le scope opérationnel déjà cité en 04 §2 est
localisé p. imprimée 13. Les formules, aux pages :

- `P₀ = (1 − p₁)(1 − p₂)···(1 − p_N)` (p. impr. 13) ;
- `P_more = 1 − P₀ − P₁` (p. impr. 13) — P₁ est la probabilité
  d'exactement une défaillance ; sa forme imprimée n'a pas été
  re-vérifiée cette passe : l'instrument utilise l'identité élémentaire
  `P₁ = Σᵢ pᵢ·Πⱼ≠ᵢ(1 − pⱼ)`, indépendante de la citation (dette de
  relecture, §10.9) ;
- K (nombre de cas où plus d'une version échoue) suit
  `P(K = x) = C(n,x)·(P_more)^x·(1 − P_more)^(n−x)` (pp. impr. 13–14) ;
- `z = (K − n·P_more)/√(n·P_more·(1 − P_more))` (p. impr. 14), test
  unilatéral ; chez K&L : N = 27, n = 10⁶, K = 1255, **z = 100,51 >
  2,33** (le point à 99 % de la normale standard), d'où le rejet du
  modèle d'indépendance.

**Transposition** (04 §2, inchangée) : version → **source** ; cas de
test → **fenêtre d'observation** ; défaillance → **écart observable**.
p̂ᵢ = (fenêtres où la source i est en écart)/n ; P̂₀, P̂₁, P̂_more par
plug-in des p̂ᵢ ; K = fenêtres à ≥ 2 écarts ; z ; seuil 2,33 (celui de
K&L). Un z au-delà du seuil rejette **le modèle d'indépendance du pool** —
il n'établit jamais la dépendance d'une paire précise (04 §2 ; 09).

**Note de transcription** (V4, trouvaille transverse ; corroborée par le
grep de rédaction) : les signes « − » des formules K&L sont tracés dans
une police Symbol non embarquée — **perdus au rendu image, préservés par
la couche texte** (**U+2212** MINUS SIGN — codepoint mesuré sur le sidecar le
2026-08-20, dette 9b ; la première rédaction disait U+002D par inadvertance) ;
profil inverse chez L&M (couche texte brouillée sur les équations, rendu net) ; et
le « ⩾ » de la source UConn (§5.4) tombe à l'extraction texte. Protocole pour toute
relecture/sidecar : K&L au texte, L&M au rendu, et jamais un seul canal pour un
signe — **et pour les formules FRACTIONNAIRES de K&L (P₁), la structure
numérateur/dénominateur se lit au RENDU et les signes au TEXTE : la couche texte
seule linéarise les dénominateurs à part et donne un P₁ faux (dette 9b, fermée le
2026-08-20 — la forme quotient imprimée `Σᵢ P₀pᵢ/(1−pᵢ)` = l'identité élémentaire
de l'instrument, par équivalence algébrique exacte).**

### 5.2 Les définitions d'écart par classe [conception]

Trois écarts, par fenêtre j et source i :

- **(i) hors-enveloppe** : `|vᵢ(j) − m₋ᵢ(j)| > τ_classe`, où m₋ᵢ est la
  **médiane leave-one-out** des autres répondantes de la fenêtre ;
  N ≥ 4 répondantes requises pour que l'enveloppe existe. Résidu de
  circularité, écrit : une majorité coordonnée (> N/2) déplace toutes les
  m₋ᵢ et flague la minorité honnête — la limite du confinement médian
  (04 §4, pt 3), irréductible ici. Fenêtre à enveloppe non définie =
  **non évaluable**, marquée telle — jamais comptée « pas d'écart »
  (fail-closed de publication).
- **(ii) staleness** : `t_fin(j) − horodatageᵢ > σ_classe`, sur
  l'horodatage porté par le relevé (celui de la source ou du transport,
  jamais celui du harnais — la ligne de 03 §1).
- **(iii) panne** : non-réponse avant clôture de fenêtre, erreur de
  transport, ou **indécodable** — l'anomalie Bitfinex (§3.1) est le cas
  d'école : un 11ᵉ champ inattendu ne se « tolère » pas, il se décode par
  position fixe ou c'est une panne.

**Combinaison** : écart si (i) ∨ (ii) ∨ (iii), précédence
panne > staleness > hors-enveloppe (une panne n'a pas de valeur : (i) non
évaluable). τ_classe et σ_classe sont des paramètres de classe, publiés
dans la sortie (§6.1).

### 5.3 La fenêtre par classe [conception]

- Durée w par classe ; grille **alignée sur l'époque UTC** — la
  contre-mesure structurelle à la « fenêtre de complaisance » (04 §5) :
  personne ne choisit ses bords de fenêtre (A(history-integrity)).
- 1 relevé/source/fenêtre : le dernier de la fenêtre.
- **Deux strates ex ante, calme/stress**, fixées par calendrier de place
  (heures d'ouverture, pré-marché), jamais déduites des données testées ;
  n et le critère de §5.4 se comptent par strate. Cas motivant, daté :
  l'ouverture de pré-marché illiquide SK Hynix du 2026-07-28 (ADR-0007) —
  le régime où A(window-stationarity) casse.
- **A(window-stationarity) est écrite dans chaque sortie R1** (04 §2 ;
  registre 08). Son ancre est re-établie cette passe : Eckhardt & Lee,
  TM-86369 détenu, p. fichier 2 (SUMMARY), hypothèse (ii) — « stationary
  input series » (grep de rédaction : présent au texte, deux
  occurrences). Nota d'identité de source (V4) : le TM s'intitule
  « Redundant Software Subject to Coincident Errors » ; la version
  journal IEEE porte « Multiversion Software » — l'artefact détenu et
  cité est le TM.

### 5.4 « Historique insuffisant » — le critère chiffré, sourcé

K&L ne donnent **aucune règle chiffrée** pour « n suffisamment grand » :
le texte renvoie à [16], et la liste des références résout [16] =
M.S. Raff, « On approximating the point binomial », J. Amer. Statist.
Ass., vol. 51, 1956 (re-établi V4 ; grep de rédaction — la liste imprime
« (16) » là où le texte cite « [16] »). Le critère de l'instrument vient
donc d'une source externe, re-établie cette passe (V5, PDF lu, octets
conservés) :

- **Critère** : publier z seulement si
  `n·P̂_more·(1 − P̂_more) ≥ 10` — la forme produit-variance, en une
  inégalité. Source : University of Connecticut, OER Math 3160, ch. 9,
  p. 121, note sous le théorème 9.1 : « This approximation is good if
  np(1 − p) ⩾ 10 » (le « ⩾ » au rendu ; la phrase au grep — note §5.1).
- **En dessous** : pas de z publié ; queue binomiale exacte
  `P(K ≥ K_obs | Bin(n, P̂_more))` (la loi de K, re-établie §5.1) ou
  approximation de Poisson(n·P̂_more) ; et si l'historique ne permet ni
  l'un ni l'autre proprement, la sortie dit **« historique
  insuffisant »** — jamais un z non significatif présenté comme une
  absence de dépendance (04 §2 ; 09, ligne dédiée).
- **Le paysage des seuils, re-établi — trois formes distinctes, à ne
  jamais confondre** : (a) `np(1−p) ≥ 10`, produit-variance, une
  inégalité [UConn — la forme du critère] ; (b) `min{np, n(1−p)} ≥ 5`
  [NIST/SEMATECH e-Handbook §7.2.4, qui exige aussi N > 30] ; (c)
  `np ≥ 10 ∧ n(1−p) ≥ 10` [Penn State STAT 200 §8.1.1.1]. Piège
  re-établi (verdict REFUTE) : la page NIST « Binomial Distribution »
  (§1.3.6.6.18, eda366i.htm) **ne contient aucun seuil
  d'approximation** — ne jamais la citer pour cette règle.
- **Choix de conception** : la forme produit-variance à 10 — la plus
  stricte des trois (dérivation d'une ligne, recalculable :
  `np(1−p) ≥ 10 ⟹ np ≥ 10 ∧ n(1−p) ≥ 10 ⟹` la forme NIST à 5).

### 5.5 L'estimateur L&M — formules re-établies, transposition en conception

Formules re-établies aux pages du PDF détenu
`biblio/littlewood-miller-1989-tse.pdf` (V4, au rendu — la couche texte
de ce scan est brouillée sur les équations, note §5.1) :

- éq. (14), p. journal 1598 : `P(Π₁ et Π₂ échouent sur X) =
  Σ(θ(x))²Q(x) = E(Θ²)` — la probabilité de co-échec est le second
  moment de la fonction de difficulté ;
- éq. (16), p. j. 1599 : `E(Θ²) = Var(Θ) + (E(Θ))²`, et « The degree of
  departure from independent behavior is governed by Var(Θ) » — l'écart
  au modèle d'indépendance EST Var(Θ) ;
- éq. (28), p. j. 1602 : `P(Π_B | Π_A)/P(Π_B) = 1 +
  Corr(Θ_A,Θ_B)·CV(Θ_A)·CV(Θ_B)` — le facteur d'élévation conditionnel
  entre deux méthodologies (Corr = corrélation, CV = coefficient de
  variation) ;
- **Cov(Θ_A, Θ_B) < 0 est possible** (p. j. 1601) : un pool anti-corrélé
  fait *mieux* que le modèle d'indépendance — l'instrument doit savoir
  l'écrire, donc publier des corrélations **signées** ;
- ρ(Θ_A, Θ_B) = 0,1808 (éq. 35, p. j. 1603) — l'exemple travaillé sur
  les données K&L en deux méthodologies, déjà porté par 04 §2.

**Transposition Shōgen** (conception — la transposition n'est pas L&M) :
m_j = nombre de sources en écart dans la fenêtre j, N évaluables :

1. `Θ̂_j = m_j/N` ; `Ê(Θ) = (1/n)·Σ_j m_j/N` ;
2. `Ê(Θ²) = (1/n)·Σ_j m_j(m_j − 1)/(N(N − 1))` — **forme par paires**.
   Re-dérivation de la passe de rédaction (recalculable, deux lignes) :
   sous le modèle conditionnel de L&M (dans la fenêtre j, écarts
   indépendants de probabilité commune θ_j, soit
   m_j | θ_j ~ Binomiale(N, θ_j)), le moment factoriel donne
   `E[m(m−1)] = N(N−1)·θ²` — l'estimateur vise E(Θ²) sans biais *sous ce
   modèle* ; l'estimateur naïf (variance empirique des Θ̂_j) est gonflé
   de `E[Θ(1−Θ)]/N` par le bruit binomial intra-fenêtre. Ni proven ni
   tested : dérivation de rédaction, à exercer par test de propriété
   en S2.
3. `Var̂(Θ) = Ê(Θ²) − (Ê(Θ))²`.
4. Corrélations par paires, deux étages : entre clusters R2 (≥ 2
   membres) via les séries (Θ̂_A,j, Θ̂_B,j) — l'analogue de l'éq. 35 ;
   entre singletons via le coefficient phi des indicatrices d'écart — un
   proxy bruité de l'éq. 28, publié avec ce caveat. Toujours **signées**
   (Cov < 0 existe).

### 5.6 k_eff et les deux drapeaux

- **k_eff = nombre de classes de la partition R2 constatée** (04 §3),
  clusters nommés avec leurs amonts (ADR-0007 : « cluster A = {src1,
  src2} via place X », jamais des comptes anonymes). R3 ne modifie
  jamais k_eff. Publié en tête, avec k nominal (09 : « k nominal, k_eff
  mesuré »).
- **z n'est jamais composé dans k_eff** : pas de métrique fusionnée. Les
  deux chiffres sont publiés côte à côte, avec deux drapeaux :
  1. **« historique insuffisant »** (§5.4) ;
  2. **« co-défaillance observée non expliquée par les axes R2 »**
     (04 §3) — déclencheur v0 : `z ≥ 2,33` avec partition sans
     recouvrement (k_eff = k nominal) ; raffinement prévu : localiser
     l'excès sur les paires inter-clusters via la matrice de co-écarts.
     C'est le signal qui teste A(axis-coverage) en continu.

## 6. La table de sortie du prototype — recalculable offline (ADR-0003)

Le rapport de S2 embarque (ou référence par hash, récupérable) le journal
brut, et **tout chiffre du rapport se recalcule depuis le journal par un
lecteur sans accès à Shōgen** — la règle d'ADR-0003 appliquée à
l'instrument lui-même. Six blocs :

1. **Paramètres** : classe (et décision de devise, §9.4), pool, fenêtre
   w, strates ex ante, seuils (τ_classe, σ_classe, κ), dates de la
   campagne, version du harnais.
2. **Journal brut** : par fenêtre × source — valeur, devise, horodatage
   porté, statut (ok / panne / staleness / hors-enveloppe / non
   évaluable), hash des octets bruts de la réponse (la ligne d'ADR-0005 :
   hash toujours).
3. **R1** : p̂ᵢ par source ; n, K par strate ; P̂₀, P̂₁, P̂_more ; z (ou
   queue exacte, ou « historique insuffisant ») ; la définition d'écart
   et A(window-stationarity) écrites dans le bloc (04 §2).
4. **L&M** : Ê(Θ), Ê(Θ²), Var̂(Θ) ; corrélations signées par paire et
   par cluster ; matrice de co-écarts.
5. **R2** : table ASN datée (par hôte : IP, préfixe, ASN, les deux
   attributions, résolveur, heure) ; statistiques de contenu par paire
   (ρ_raw, ρ_resid, T/T_Δ, (K, z), δ) ; arêtes méthode avec `basis` et
   leurs `doc_url`/`doc_fetched` ; les sept résidus de §4.1.
6. **Tête de certificat** : partition nommée, **k_eff, k nominal**, les
   deux drapeaux.

## 7. Le critère de sortie S2 — binaire, inchangé

Tel quel (05 §S2) : un rapport avec les chiffres réels — **n fenêtres, K,
z du pool, la partition R2 constatée, k_eff vs k nominal** ; *résultat
négatif = résultat* : « les axes ne discriminent pas » s'écrit avec les
chiffres et déclenche la révision de 04.

Nota de nommage : 05 §S2 nommait le rapport `07-mesures-pilotes.md`, mais
07 est occupé par `07-gtm.md` depuis l'écriture de la feuille de route ;
**réconcilié le 2026-08-05 en `11-mesures-pilotes.md`** (05 §S2 amendée),
sans effet sur le critère lui-même (dette §10.10, fermée).

## 8. Assumptions engagées

Toutes résolues dans `08-assumptions.md` (le registre qui fait foi), y
compris la dernière, enregistrée cette passe :

- **A(window-stationarity)** — engagée par le test agrégé (§5.1) et
  écrite dans chaque sortie R1 (§5.3). Ancre re-établie cette passe
  (E&L, TM-86369, p. fichier 2). La stratification ex ante de §5.3 est le
  début de sa trajectoire de décharge (08 : « stratification par régime
  quand S2 aura mesuré »).
- **A(axis-coverage)** — engagée par tout §4 : trois axes seulement ; un
  amont qui bruite ses copies échappe à (b) ; le drapeau 2 de §5.6 est
  précisément son test en continu (08).
- **A(history-integrity)** — engagée par §5.3 : la grille alignée UTC est
  la contre-mesure de construction à la fenêtre de complaisance (04 §5) ;
  le journal S2 n'est pas encore un lot de témoignages (S3), sa décharge
  récursive reste S4 (08).
- **A(typer-correctness)** — engagée par §3.1 et §5.2 : douze formes de
  réponse distinctes ; l'anomalie Bitfinex comme cas d'école ; décodage
  par position fixe et par clé retournée ; indécodable ⇒ panne. Le
  rapport S2 publie le compte d'exécutions de chaque décodeur — première
  marche vers la cible de 08 (tested à S3, avec compte d'itérations).

- **A(asn-attribution)** — **enregistrée dans `08-assumptions.md` le
  2026-08-05** (résidus de couche), engagée par l'axe ASN de §4.1 :
  *l'attribution IP → ASN rapportée par les services (RIPEstat, Team
  Cymru) reflète l'annonce BGP effective au moment de la mesure.* Source
  du résidu : §4.1, résidu 6 (les services d'attribution sont eux-mêmes
  des témoins). Assurance : aucune — la concordance 8/8 du 2026-08-05 est
  une observation, pas une décharge. Décharge : jamais totale ;
  attribution croisée sur ≥ 2 bases BGP distinctes + re-mesure à chaque
  quorum.

## 9. Décisions remontées au mainteneur — prises le 2026-08-05

**Résolutions (mainteneur, 2026-08-05 — assurance *reviewed*)** :

1. Périmètre → **les 11 sources répondantes, oracles inclus** (donc
   lecture on-chain admise, cf. 2).
2. Lecture on-chain par RPC → **admise** : un `eth_call` en lecture est la
   surface « lire » qu'ADR-0006 distingue explicitement de « calculer »
   (interdit) ; aucun calcul on-chain n'est introduit.
3. CoinGecko → **strictement sans clé** ; un throttle (429) est compté en
   panne (iii) — comportement publié de l'instrument (§5.2).
4. Homogénéité → **« BTC/USD-stable », devise marquée par flux** (§2) :
   garde les 2 flux USDT, l'écart de peg devient mesurable par (2a).
5. Budget → **≈ 2 semaines, w = 60 s, 2 strates** (calme/stress) : n
   bien au-delà du seuil §5.4 dans les deux régimes. **Amendé par ADR-0020
   (ratification investisseur 2026-08-20)** : « ≈ 2 semaines » et « week-end=stress »
   sont incompatibles (la strate rare gouverne : 5 760 fenêtres week-end en 14 j
   < 10 010 requises) — le calendrier réel est **week-end=stress → ~24-28 jours**,
   avec **calibration 48 h ex ante** (vendredi, fenêtres exclues de l'inférence)
   fixant les seuils, **τ_classe = 0,5 % relatif**, **σ par classe de source**, et un
   calendrier de publication J0/J14/J28 à date fixe (3 z toujours publiés).
6. Règle `basis:doc` → **ADR-0008, acceptée le 2026-08-05** (décision
   déléguée à l'orchestrateur, fondée sur INDaaS / Chainlink v1 / 04 §1),
   avec alternative et coût.

La justification de chaque option et les alternatives restent consignées
ci-dessous, telles qu'écrites avant la décision.

1. **Périmètre du pool S2** : les 7 places primaires seules, ou les 11
   sources répondantes (12 flux, avec agrégateurs et oracles) ?
   Recommandation portée au briefing par l'orchestrateur : inclure
   CoinGecko, DefiLlama, Pyth et Chainlink *précisément parce que* la
   détection de leur dépendance par l'instrument est le résultat qui
   tranche. La décision est celle du mainteneur.
2. **Lecture on-chain par RPC public** : ADR-0006 interdit token et
   calcul on-chain et distingue explicitement « y *lire* une valeur » ;
   un `eth_call` en lecture (re-établi fonctionnel, §3.1) entre-t-il au
   pool S2 ? À confirmer.
3. **CoinGecko, clé Demo gratuite vs strictement sans clé** : la
   re-mesure a répondu sans clé et sans 429 ; la doc lue par le worker
   (non re-établie) dit le keyless impropre au polling planifié.
   Options : clé Demo gratuite, marquée « à clé » dans la table ; ou
   keyless best-effort, ses throttlings comptés en panne (iii) — un
   comportement publié de l'instrument, pas un biais, tant que c'est
   écrit.
4. **Homogénéité de la classe** (§2) : BTC/USD strict / « BTC/USD-stable »
   avec devise marquée par flux / deux classes. Le choix fixe τ_classe et
   la composition du pool.
5. **Budget de campagne** : semaines d'historique, fréquence de fenêtre,
   taille du pool. Contrainte arithmétique de conception (recalculable,
   pas une mesure) : publier un z exige `n·P̂_more·(1−P̂_more) ≥ 10` — si
   P̂_more ≈ 10⁻³, n ≳ 10 010 fenêtres, soit ≈ 7,0 jours à w = 60 s, par
   strate.
6. **La règle « une arête `basis:doc` ne partitionne pas »** (§4.3) :
   structurante pour k_eff — à fixer par ADR avant tout calcul de
   partition sur données réelles.

## 10. Dettes nommées — fetch, registre, relecture

| # | dette | ce qui la décharge |
|---|---|---|
| 1 | **Dong et al. 2010**, « Global Detection of Complex Copying Relationships Between Sources », PVLDB 3(1), pp. 1358–1369 — identité re-établie en page de titre (V5), URL `vldb.org/pvldb/vol3/R120.pdf` (**R120**, pas R121), octets en scratchpad de passe (`vldb_R120.pdf`), **corps non lu** | fetch dans `biblio/` + INDEX + lecture du corps avant que (2c) ne le cite comme précédent ; et trancher 2009 (« Integrating Conflicting Data: The Role of Source Dependence », PVLDB 2 — le mécanisme y naît ; non lu) vs 2010 comme citation porteuse — **Re-statuée le 2026-09-30 : ouverte, périmètre résiduel nommé** : identité re-établie et corps non lu (`biblio/INDEX.md` l.57) ; prédécesseur PVLDB 2009 non détenu. Items formés : SHOGEN-DONG-CORPS-1 (lecture du corps ; demande de procurement du PVLDB 2009), annexe B d'ADR-0028 ; la dépendance de (2c) à ce précédent reste conditionnelle (aucune citation avant lecture) |
| 2 | ~~**Seuil produit-variance** : source lue et citée (UConn OER Math 3160, ch. 9, p. 121 ; octets `uconn_ch9.pdf`) — déchargée sur le fond ; voisines détenues en garde-fou (`nist_prc24.html`, `psu_8111.html`)~~ — **barrée le 2026-09-30 (condition remplie depuis le 2026-08-05)** : les trois sources sont enregistrées à `biblio/INDEX.md` (UConn l.54, NIST l.55, Penn State STAT 200 l.56), la note des trois formes est à §5.4 | — |
| 3 | **Roster des publishers du feed Pyth BTC/USD** — l'arête Pyth ← Coinbase n'est établie qu'au niveau réseau | fetch de la page du feed (ou du roster via l'API Hermes) ; jusque-là l'arête reste `basis:doc`, granularité réseau |
| 4 | **Copies octets-exacts des 4 pages HTML** citées §4.3 (citations passées par le résumeur de fetch) | re-fetch brut (navigateur) dans `biblio/` avant tout enregistrement ou ADR citant verbatim — **Re-statuée le 2026-09-30 : ouverte, périmètre résiduel 3/4** : détenue, la page méthodologie de CoinGecko (`biblio/INDEX.md` l.264, copie du 2026-08-12) ; restent la page « exchanges/binance » de CoinGecko, la page « price-aggregation » de Pyth et la page « publishers » de Pyth. Item formé SHOGEN-BIBLIO-PAGES-4-3-1 (annexe B d'ADR-0028), sous SHOGEN-FETCH-AVANT-PUB-1 |
| 5 | **docs.llama.fi/coin-prices-api** : page JS, illisible par fetch (404) ; le verdict est porté par `llms-full.txt` | re-tenter par navigateur si le libellé exact devient porteur |
| 6 | **Chainlink** : paramètres du feed (déviation/heartbeat) et composition d'amont non établis (`data.chain.link` 403, doc volumineuse en échec — passe worker) | établir sur pièce, ou laisser le nœud sans arête d'amont et le dire (§3.2) |
| 7 | ~~**Transformation de Fisher** (SE = 1/√(N−3), §4.2)~~ — **fermée le 2026-09-30** pour la forme de manuel : source enregistrée à `biblio/INDEX.md` l.328 (Penn State STAT 509 L7 §7.8) ; erratum daté à §4.2 (b) (l'IC vaut sur l'échelle z′, pas sur ρ) ; le primaire (Fisher 1921, *Metron* 1:3-32) reste en procurement L-46 | — |
| 8 | ~~**Registre** : « asn-attribution » à résoudre dans `08-assumptions.md`~~ — **fermée le 2026-08-05** : A(asn-attribution) enregistrée (résidus de couche), citée à §8 et §4.1 | — |
| 9 | **Relectures avant implémentation** : limites de débit (§3.3, lectures worker non re-établies) ; forme imprimée de P₁ chez K&L (§5.1, non re-vérifiée) | re-lire les docs de débit à l'implémentation ; relire P₁ au PDF à l'implémentation du calcul |
| 10 | ~~**Collision de nommage** du rapport (05 §S2 : `07-mesures-pilotes.md` vs `07-gtm.md`)~~ — **fermée le 2026-08-05** : 05 §S2 réconcilié en `11-mesures-pilotes.md` (le nom de fichier, jamais le critère) | — |
| 11 | **Fermetures à reporter dans 04 §2** : les [à décider] « définitions d'écart par classe » et « taille minimale d'historique » reçoivent ici leur conception (§5.2, §5.4) ; la stratification y gagne son dessin (§5.3) | reporter dans 04 §2 (et entériner) à la prochaine passe docs — l'édition de 04 est hors du périmètre de cette passe |

---

**Relecture de passe.** Les seules phrases de ce document qui affirment un
fait du monde portent un verdict de re-mesure daté du 2026-08-05 ; les
autres sont des choix de conception et se lisent comme tels. La phrase qui
serait embarrassante à l'audit — « les axes R2 discriminent » — n'y figure
pas : c'est la question que l'instrument existe pour trancher, et sa
réponse s'écrira avec n, K, z, la partition constatée et k_eff vs
k nominal, quel que soit son signe.

## Ajouts datés en fin de document

*Ajout daté du 2026-10-10 04:55:14 UTC (`date -u`) ; lot DETTES-T14* : les ajouts datés du lot DETTES-T14
sont placés ici, en fin de document, pour n'en décaler aucune ligne, ce document étant cité ailleurs par
numéro de ligne ; chacun nomme la section qu'il vise, dont le texte est inchangé.

**Vise §4.2 (b).** *Ajout daté du 2026-10-10 04:55:14 UTC (`date -u`) ; lot DETTES-T14 ; P-03, décision
Q-E de l'adjudication du procurement du 2026-10-09 ; l'erratum du 2026-09-30 et l'ajout du 2026-10-02 de
cette section sont inchangés* : le primaire est détenu et lu : Fisher 1921, *Metron* 1(3) : 3-32
(`biblio/fisher1921-metron-1-3-32.pdf`), pp. 14 et 18, lues sur l'image et contrôlées sur l'OCR. P. 14 :
exprimée en z, la courbe d'échantillonnage est « sufficiently normal and constant in deviation », et son
erreur probable « may be obtained from the same table as before entered with the value » n − 3. P. 18 :
« The weight of each sample measured on the scale of z is taken to be » (n − 3). La forme littérale
1/√(n−3) n'y est pas imprimée : c'est celle du manuel (Penn State STAT 509 L7, `biblio/INDEX.md` l.328),
que nomme la ligne imprimée de `report.py` (« transformation de Fisher ; Penn State STAT 509 L7 »),
inchangée. Limite : un poids (n − 3) vaut une variance 1/(n − 3) [inféré : le poids est l'inverse de la
variance]. Les racines imprimées aux pp. 10 (cas fraternel) et 11 (erreur probable de r), vues sur
l'image, visent d'autres cas : elles ne se citent jamais pour cette ligne. P-03 est fermé.

**Vise §4.2 (b), précédent académique de (2c).** *Ajout daté du 2026-10-10 04:55:14 UTC (`date -u`) ; lot
DETTES-T14 ; SHOGEN-DONG-CORPS-1 ; le paragraphe visé est inchangé* : le corps de Dong 2010 est lu (pp.
1358-1361 et 1365, PDF pp. 1-4 et 8 : lecteur du procurement le 2026-10-09, citations recontrôlées par
script au lot DETTES-T14) et le prédécesseur est détenu et lu (PVLDB 2(1) : 550-561, 2009 ;
`biblio/INDEX.md`, section du lot DETTES-T14). Dong 2010 situe lui-même en 2009 la décision par paires :
« In particular, [6] makes pairwise decisions based on common mistakes made by the sources » (p. 1358),
[6] étant le papier de 2009 (références, p. 1365) ; 2009 pose que « two independent sources providing the
same false value is a rare event » (§3.1). Les deux modélisent la copie par une analyse bayésienne
(probabilité des données observées sous indépendance ou sous copie), non par un compte binomial de
co-aberrances (« binomial » : 0 occurrence dans le texte de 2009). (2c) peut donc citer cette lignée pour
l'idée que des fautes partagées signalent une dépendance, jamais pour sa statistique z, qui reste celle
de §5.1.

**Vise §4.3 (c), points 2 à 4.** *Ajout daté du 2026-10-10 04:55:14 UTC (`date -u`) ; lot DETTES-T14 ;
SHOGEN-BIBLIO-PAGES-4-3-1, décision Q-D de l'adjudication du procurement du 2026-10-09 ; les cinq points
de cette section sont inchangés* : état des trois pages au 2026-10-09 (copies, sha256 et conditions à
`biblio/INDEX.md`, section du lot DETTES-T14). Point 2 (CoinGecko ← Binance) : la page HTML répond 403
derrière un contrôle anti-robot, non contourné ; le chiffre est re-vérifié sur l'API officielle
(`api.coingecko.com/api/v3/exchanges/binance`, copie JSON datée) : `pairs` = 1372, égal au chiffre daté
du 2026-08-05 ; la copie octets-exacts de la page reste non détenue. Point 3 (Pyth, agrégation) : la
citation est gardée avec sa date (vérifiée le 2026-08-05). La page a été retirée par Pyth : la page de
renvoi, détenue, dit « Pythnet is being shut down as part of the Pyth Core sunset », et l'expression
citée y a 0 occurrence. La copie du 2026-08-05 n'est pas détenue : la citation n'est plus re-vérifiable
et décrit le mécanisme d'un produit en extinction. Point 4 (Pyth ← Coinbase) : la copie du jour range
Coinbase sous « Crypto », et le libellé cité y a 0 occurrence ; elle atteste l'arête au niveau réseau à
sa date, sans valoir copie de la page du 2026-08-05.

**Vise §10, dettes 1, 4 et 7.** *Ajout daté du 2026-10-10 04:55:14 UTC (`date -u`) ; lot DETTES-T14 ; la
table de cette section est inchangée* : dette 1 **fermée** (SHOGEN-DONG-CORPS-1) : corps de Dong 2010 lu
aux pp. 1358-1361 et 1365 (lecteur du procurement), citations recontrôlées par script ; PVLDB 2009 détenu
et lu ; la lignée 2009-2010 se cite pour l'idée de (2c), non pour sa statistique (ajout ci-dessus visant
§4.2 (b), précédent académique de (2c)). Dette 4 **fermée par la décision Q-D**
(SHOGEN-BIBLIO-PAGES-4-3-1), avec un résidu écrit : aucune copie octets-exacts du 2026-08-05 n'est
détenue pour les points 2 à 4 de §4.3 ; leur état daté est à l'ajout ci-dessus qui vise ces points
(substitut d'API pour CoinGecko ; page Pyth retirée, citation datée gardée ; copie du jour de la page des
publishers), et leurs citations ne se reprennent dans aucun ADR comme texte courant de ces pages. Dette
7 : le primaire est détenu et lu (P-03 fermé ; ajout ci-dessus visant §4.2 (b)).
