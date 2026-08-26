# TAU — recherche des faits externes fondant une décision de seuil τ (campagne S2 Shōgen)

## Gate 0
Modèle résolu : `claude-sonnet-5` (Sonnet 5), effort max. Préfixe conforme à l'attendu
(`claude-sonnet-5`). Poursuite autorisée.

## Identification de la mission
- Mandant : orchestrateur Shōgen.
- Objet : établir les FAITS EXTERNES ACTUELS (2025-2026) fondant une décision de seuil τ
  (écart RELATIF de concordance inter-sources au-delà duquel une source est signalée
  hors-enveloppe) pour la campagne S2. Périmètre STRICT : PAS de re-conception de
  l'enveloppe, PAS de balayage de littérature de détection d'anomalies en général — six
  questions fermées, sources nommées.
- Chercheur : agent `chercheur` (Sonnet 5, effort max), doc 03 (sources avant travail,
  [lu]/[abs]/[2nd], chiffres copiés avec unité+source+date+localisation, verbatim ≤30 mots,
  jamais de seconde main présentée comme primaire, « NON TROUVÉ » valide).
- Date de la passe : 2026-08-26.
- Fichier écrit AU FIL DE L'EAU : chaque section complétée dès que la recherche
  correspondante est faite. **Passe de correction post-advisor incluse** (voir notes
  « [CORRECTION POST-ADVISOR] » ci-dessous) : deux erreurs de synthèse auto-détectées par
  l'advisor puis vérifiées et corrigées avant remise, une troisième correction déclenchée par
  un nouvel échantillon pris sur recommandation de l'advisor qui a en fait INFIRMÉ (pas
  seulement nuancé) une conclusion précédente — traité honnêtement, pas maquillé.

---

## Statut d'outillage (constaté avant travail)
- Outils disponibles cette session (confirmés via le rappel système + ToolSearch) :
  Read, Write, Glob, Grep, Bash, WebSearch, WebFetch, advisor, ToolSearch, et les outils
  firecrawl sous l'UUID connecteur `mcp__8aa0cccf-8b75-49a2-b5b7-f037a083f6da__*`
  (firecrawl_search, firecrawl_research_search_papers, firecrawl_research_read_paper,
  firecrawl_research_inspect_paper, firecrawl_research_related_papers,
  firecrawl_research_search_github).
- **[CONFIRMÉ NON DISPONIBLE]** `mcp__memstack` — recherche ToolSearch `"memstack memory"`
  → aucun résultat. La règle CLAUDE.md (2026-08-21) exige memstack pour tout sous-agent ;
  son absence ici est une contrainte de configuration de CETTE session, hors de mon
  contrôle en tant qu'agent exécutant — consignée, non contournée. Aucune conséquence
  bloquante attendue pour cette mission (six questions fermées, sources externes nommées,
  pas de dépendance à la mémoire de projet).

---

## [ÉCART CONSTATÉ AVANT TRAVAIL — doc 03 §1, à signaler EN PREMIER]
La mission (question 5) indique : « RÉUTILISE l'archive C1 déjà en maison —
`...\oracle-research\C1-attaques.md` (USDe, CAPO, KelpDAO) AVEC sa réserve G2 (C1-bis a
auto-détecté un cas fabriqué). »

**Vérification faite avant extraction** (lecture intégrale de C1-attaques.md, 837 lignes,
+ grep ciblé `USDe|CAPO|KelpDAO|Kelp DAO|Ethena|rsETH`) : **AUCUNE occurrence** de USDe,
CAPO, KelpDAO, Ethena ou rsETH dans C1-attaques.md. Ce fichier traite exclusivement de la
taxonomie académique des attaques d'oracle 2018-2023 (SoK DeFi Attacks, SoK Oracles, Liu et
al., TWAP, BonqDAO, Venus/LUNA, Mango Markets, Compound/Coinbase, bZx) — aucun de ces trois
incidents 2025-2026 n'y figure.

Le contenu USDe/CAPO/KelpDAO existe réellement, mais dans **deux AUTRES fichiers** du même
répertoire : `SONDE-artefact.md` (§3 « Douleur récente — incidents oracle 2025-2026 »,
lignes 115-147) et son résumé `ARTEFACT-sonde-keff.md`. Aucun fichier nommé « C1-bis »
n'existe dans le répertoire (`Glob **/*C1-bis*` → 0 résultat) ni ailleurs dans l'arborescence
temp de cette session.

Le « cas fabriqué auto-détecté » que la mission attribue à un hypothétique « C1-bis » est en
réalité documenté DANS C1-attaques.md lui-même, sous le nom **« piège méthodologique #3 »**
(lignes 40-45 et 268 du fichier) : un chercheur précédent a un temps écrit un paragraphe sur
un « cas Synthetix sKRW juin 2019 » (perte ~1 milliard USD, bot de trading, négociation de
bug bounty) en le présentant comme lu directement, **avant** d'avoir réellement effectué la
lecture — auto-détecté en se relisant, corrigé par une vraie lecture ensuite (le texte réel
dit tout autre chose : cas Synthetix à 2 feeders, manipulation ×1000, perte qualifiée
seulement de « several million dollars », aucun chiffre précis, aucune mention de « sKRW »).

**Traitement retenu pour cette archive** : je réutilise le contenu USDe/CAPO/KelpDAO
effectivement présent dans `SONDE-artefact.md` (qui porte SA PROPRE discipline de niveaux
[lu]/[abs]/[2nd] déjà appliquée par le chercheur précédent, avec réserve G2 explicite
« méritent une revue G2 avant tout usage probatoire élargi » dans `ARTEFACT-sonde-keff.md`
ligne 75-76), et je traite le « cas fabriqué » comme désignant le piège #3 de C1-attaques.md.
Tout chiffre destiné à la décision τ est re-vérifié sur source primaire dans la section 5
ci-dessous, conformément à l'instruction de la mission. Cet écart de nom de fichier est signalé
à l'orchestrateur dans le résumé de retour — ce n'est pas une collision qui invalide le
contenu, mais une imprécision de référence à corriger dans le brief source.

---

## Q1 — Chainlink ETH/USD (+ BTC/USD) : seuil de déviation + heartbeat

### Identification des feeds (vérifiée avant extraction)
- ETH/USD mainnet : proxy `0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419` (adresse donnée par la
  mission). **Vérifié on-chain aujourd'hui 2026-08-26** : `description()` → `"ETH / USD"`,
  agrégateur courant → `0x7d4e742018fb52e48b08be73d041c18b21de6fb5` (identique à celui déjà lu
  le 2026-08-21 par SONDE-artefact.md — stable sur 5 jours). Pas de collision de nom : c'est
  bien le feed attendu. [lu, primaire, on-chain, ce jour]
- BTC/USD mainnet : proxy `0xF4030086522a5bEEa4988F8cA5B36dbC97BeE88c` — adresse trouvée
  **dans le corps du texte de docs.chain.link lui-même** (page « Chainlink Data Feeds »,
  section « Updates to proxy and aggregator contracts », citée en exemple d'Etherscan), donc
  déjà une identification P1 avant même la vérification on-chain. **Vérifié on-chain
  aujourd'hui** : `description()` → `"BTC / USD"`, agrégateur courant →
  `0x4a3411ac2948b33c69666b35cc6d055b27ea84f1`. [lu, primaire, on-chain, ce jour]
- **Piège de collision explicitement documenté par la source elle-même** (docs.chain.link,
  verbatim ci-dessous) : la même paire d'actifs a des heartbeat/seuils DIFFÉRENTS selon le
  réseau. Confirmé empiriquement : ETH/USD Base Mainnet = seuil 0,15% (pas 0,5%) ; ETH/USD
  Arbitrum Mainnet = seuil 0,05% ; BTC/USD Polygon Mainnet = seuil 0,1%. **Seul « Ethereum
  Mainnet » est pertinent pour Shōgen** — vérifié à chaque extraction ci-dessous.

### Mécanisme documenté (docs.chain.link, page "Chainlink Data Feeds", section "Monitoring
data feeds" — [lu] via firecrawl_search, texte retourné brut, pas une synthèse IA)

Verbatim exact (≤30 mots par extrait, source : `https://docs.chain.link/data-feeds`) :
> « the aggregator updates its latestAnswer when the value deviates beyond a specified
> threshold or when the heartbeat idle time has passed »

> « When the node detects that the heartbeat is reached, it initiates the latest round.
> Depending on congestion and network conditions, there may be a slight delay for the latest
> round to get onchain. »

> « Heartbeat and deviation thresholds can also differ for the same asset across different
> blockchains. Combining data from multiple feeds, even those with a common denominator,
> might result in a margin of error that users must account for in their risk mitigation
> practices. »

Complément, page « Getting Historical Data » (`https://docs.chain.link/data-feeds/historical-
data`), table à deux lignes, [lu] verbatim :
> « Deviation Threshold | Chainlink nodes are monitoring data offchain. The deviation of the
> real-world data beyond a certain interval triggers all the nodes to update. »
> « Heartbeat Threshold | If the data values stay within the deviation parameters, it will
> only trigger an update every X minutes / hours. »

**Portée de ce constat pour le P99 mesuré S2 (~0,53% pour Chainlink)** : la phrase sur le
« slight delay... depending on congestion » explique MÉCANIQUEMENT pourquoi un écart mesuré
peut légèrement DÉPASSER le seuil nominal de 0,5% — le déclenchement a lieu quand le prix
off-chain franchit 0,5% par rapport à la DERNIÈRE valeur on-chain, mais le prix continue de
bouger pendant la latence de transaction jusqu'à l'écriture effective on-chain. Ceci est
confirmé empiriquement ci-dessous (dépassements jusqu'à ~0,75% observés en pratique).

### Valeurs statiques affichées — data.chain.link (deux extraits indépendants par feed,
[lu-extrait, brut] via firecrawl_search, PAS une synthèse IA)

| Feed | Réseau | Deviation threshold (constant sur 2 extraits) | Heartbeat affiché (VARIE entre extraits — voir analyse) |
|---|---|---|---|
| ETH / USD | Ethereum Mainnet | **0,5%** (idem sur les 2 extraits, `data.chain.link/feeds/ethereum/mainnet/eth-usd` et `data.chain.link/feeds`) | `00:40:33` puis `00:32:37` (~8 min plus tard) |
| BTC / USD | Ethereum Mainnet | **0,5%** (idem sur les 2 extraits, `data.chain.link/feeds/ethereum/mainnet/btc-usd` et `data.chain.link/feeds`) | `00:20:20` puis `00:32:01` |

**Constat méthodologique important, auto-détecté avant de conclure** : le champ « Heartbeat »
affiché par l'interface data.chain.link N'EST PAS une valeur statique configurée — il VARIE
entre deux extraits du même feed pris à quelques minutes d'intervalle (40:33 → 32:37,
décroissant d'environ le temps écoulé entre les deux extractions). C'est un **compte à rebours
en temps réel** (probablement : temps restant avant le prochain déclenchement heartbeat prévu),
pas la durée configurée. **Je refuse de rapporter "00:40:33" comme "le heartbeat est de 40 min
33 s"** — ce serait une lecture erronée d'un widget dynamique comme s'il s'agissait d'un
paramètre statique. Seule la colonne « Deviation threshold » s'est montrée stable entre les
deux extraits de chaque feed — traitée comme fiable pour la valeur statique.

Tentative infructueuse de trouver le heartbeat STATIQUE documenté (ex. « 3600 secondes ») sur
la table des adresses de contrats (`docs.chain.link/data-feeds/price-feeds/addresses`) :
WebFetch a échoué (page trop volumineuse, `maxContentLength size of 10485760 exceeded`) ;
firecrawl_search ciblé (`"ETH / USD" ethereum mainnet ... heartbeat 3600 ...`) → 0 résultat.
**Pivot méthodologique vers la vérification empirique on-chain (ci-dessous), plus robuste et
datée du jour même.**

### Vérification empirique on-chain — méthode et résultats (P1, primaire, ce jour, reproductible)

**Méthode** : lecture directe des 60 derniers rounds de l'agrégateur via `getRoundData()`
(RPC public `https://ethereum.publicnode.com`, requêtes batch JSON-RPC), pour chaque feed.
Calcul de l'écart de temps (`updatedAt`) et de l'écart de prix relatif entre rounds consécutifs.
Logique de vérification : si le mécanisme documenté est exact, (a) les rounds séparés par un
grand écart de temps (~heartbeat) doivent avoir un delta de prix SOUS le seuil de déviation
(sinon ils auraient été déclenchés plus tôt par la déviation) ; (b) les rounds séparés par un
écart de temps court doivent avoir un delta de prix PROCHE OU AU-DESSUS du seuil de déviation
(c'est ce qui les a déclenchés).

**Sélecteurs de fonction vérifiés via 4byte.directory avant l'appel** (pas de valeur devinée) :
`description()`=`0x7284e416`, `aggregator()`=`0x245a7bfc`, `latestRoundData()`=`0xfeaf968c`,
`getRoundData(uint80)`=`0x9a6fc8f5`.

**Résultat ETH/USD (60 rounds, aggRoundId 32925-32984, période couverte : 2026-08-25T00:44:47
→ 2026-08-26T12:49:11 UTC)** — table complète des gaps calculée, extrait représentatif :

| aggRoundId | gap au round précédent | delta prix |
|---|---|---|
| 32983 | **3600s (1h0m0s)** | -0,1385% |
| 32982 | 3624s (1h0m24s) | -0,2976% |
| 32981 | 936s (0h15m36s) | **+0,5021%** |
| 32980 | 2712s (0h45m12s) | **+0,5056%** |
| 32979 | 2808s (0h46m48s) | **-0,5325%** |
| 32956 | 3660s (1h1m0s) | -0,2095% |
| 32964 | 1416s (0h23m36s) | **-0,7644%** |
| 32941 | 120s (0h2m0s) | **+0,5022%** |
| 32940 | 84s (0h1m24s, minimum observé) | **-0,5670%** |

Statistiques sur 59 écarts : min 84s, max **3660s**, médiane 2016s, moyenne 2201s.

**[CORRECTION POST-ADVISOR — erreur de synthèse détectée et corrigée avant remise]** Une
première rédaction de ce constat citait par erreur trois rounds à GAP LONG (32967/32974/32973,
gaps ~3600-3636s) comme des « exceptions au gap court » — confusion de catégorie, incohérente
avec sa propre parenthèse (ces trois rounds ONT un gap proche de 3600s, ils n'appartiennent pas
au groupe « gap court »). Détecté par l'advisor, **re-vérifié programmatiquement sur les 59
lignes complètes** (script Python sur les données brutes déjà collectées, aucune nouvelle
requête nécessaire) avant correction. Constat exact, reproductible :

- **22 rounds à gap long (≥3600s, ≤3660s)** : delta de prix bas dans 21/22 cas (fourchette
  absolue 0,0342% à 0,3787%) ; **UNE exception** : aggRoundId 32969 (gap 3624s, delta +0,5108%)
  — le heartbeat déclenche à ~1h même si le prix a, par coïncidence, aussi franchi 0,5% à ce
  moment-là (les deux causes de déclenchement ne s'excluent pas mutuellement).
- **37 rounds à gap court (84s à ~2800s)** : delta de prix proche ou au-dessus de 0,5% dans
  35/37 cas (fourchette absolue 0,50% à 0,76%) ; **DEUX exceptions** : aggRoundId 32977 (gap
  1464s, delta -0,1275%) et aggRoundId 32942 (gap 420s, delta +0,0862%) — gap court mais delta
  faible, non investiguées en détail (hors périmètre du temps alloué), signalées sur le même
  modèle honnête que l'exception unique déjà notée pour BTC/USD ci-dessous plutôt que masquées.

**Conclusion empirique, INCHANGÉE par cette correction — seule la description de l'échantillon
était fautive, pas le résultat** : heartbeat = 3600 secondes (1 heure), confirmée par le
plafond net des gaps observés (jamais >3660s sur 59 échantillons, aucune exception sur ce
point) ; seuil de déviation = 0,5%, confirmé par le plancher NETTEMENT MAJORITAIRE (35/37, soit
95% des gaps courts) des deltas associés — majoritaire et non absolu. Les dépassements observés
au-delà de 0,5% (jusqu'à 0,76%) sur les gaps courts corroborent EXACTEMENT le texte
docs.chain.link sur le délai de congestion cité plus haut ; les trois exceptions (une par
groupe, plus une seconde côté gap court) restent non expliquées en détail mais cohérentes avec
le fait que le déclenchement s'évalue off-chain contre la DERNIÈRE valeur on-chain — un round
antérieur peut avoir déjà partiellement absorbé un mouvement de prix.

**Résultat BTC/USD (60 rounds, aggRoundId 23668-23727)** — même méthode, résultat directionnel
identique mais légèrement plus bruité :
- Max gap observé : 3648s (~1h1m) — cohérent avec heartbeat ≈ 1h.
- 26 rounds à gap >3000s : deltas de prix majoritairement bas (médiane ~0,23%, max 0,528%) ;
  2 valeurs basses isolées (0,011%, 0,013%) sans lien avec le seuil.
- 24 rounds à gap <2000s : deltas de prix majoritairement ≥0,5% (0,503% à 1,14%), avec UNE
  exception notable (0,009% sur un gap court) — non expliquée par cette passe, signalée
  honnêtement plutôt que masquée. **Cette exception ne contredit pas le mécanisme documenté
  (le seuil de déviation n'est qu'UNE des deux causes de déclenchement — un round peut aussi
  se déclencher par heartbeat alors qu'un gap précédent était déjà court pour une autre
  raison) mais n'a pas été investiguée en détail, hors périmètre du temps alloué.**
- **Conclusion BTC/USD : même verdict que ETH/USD, avec un signal légèrement plus bruité** —
  heartbeat ≈ 3600-3648s, seuil de déviation ≈ 0,5%, cohérent avec la valeur statique lue sur
  data.chain.link.

### Verdict sur l'hypothèse de la mission (« 0,5% / 1h »)

**CONFIRMÉ, par DEUX méthodes indépendantes convergentes** :
1. Valeur statique affichée par data.chain.link (« Deviation threshold » = 0,5% pour ETH/USD
   ET BTC/USD Ethereum Mainnet, stable sur deux extraits chacun) — [lu-extrait, brut].
2. Mesure empirique on-chain directe, ce jour, sur les deux feeds (60 rounds chacun) — le
   plafond des gaps « calmes » et le plancher (majoritaire, pas absolu) des deltas « courts »
   convergent respectivement vers ~3600s et ~0,5% — [lu, primaire, on-chain].

Le champ « heartbeat » de data.chain.link n'a PAS pu être cité comme preuve directe de la
valeur « 1h » (c'est un compte à rebours dynamique, pas la valeur configurée) — corrigé par la
méthode empirique on-chain, qui est en fait une preuve PLUS forte (primaire, datée, reproductible,
indépendante de l'interface web).

**Explication mécanique du P99 ~0,53% mesuré par S2 pour Chainlink** : un paramètre documenté
(seuil 0,5%) explique la quasi-totalité de la masse du P99 mesuré, PAS du bruit. Le petit
excédent au-delà de 0,5% (jusqu'à 0,53% au P99, jusqu'à 0,76%/1,14% observés dans cet
échantillon pour les cas extrêmes) est lui-même documenté et expliqué mécaniquement par le
délai de congestion entre déclenchement du seuil off-chain et écriture on-chain — verbatim
docs.chain.link cité plus haut, PAS une anomalie.

### Journal des URL — Q1
- `firecrawl_search` "Chainlink ETH/USD price feed deviation threshold heartbeat mainnet",
  domaine `data.chain.link` → succès, 5 résultats dont la page ETH/USD directe (0,5%).
- `firecrawl_search` "ETH / USD ethereum mainnet ... heartbeat 3600 deviation 0.5%", domaine
  `docs.chain.link` → **0 résultat** (échec de cette formulation précise).
- `WebFetch https://docs.chain.link/data-feeds/price-feeds/addresses?...` → **ÉCHEC** :
  `maxContentLength size of 10485760 exceeded` (page trop volumineuse).
- `firecrawl_search` "Chainlink price feed contract addresses ETH/USD mainnet heartbeat
  deviation table", domaine `docs.chain.link` → succès partiel : a retourné la page
  `docs.chain.link/data-feeds` (mécanisme complet, verbatim ci-dessus) et
  `docs.chain.link/data-feeds/historical-data` (table Deviation/Heartbeat Threshold), mais PAS
  la table d'adresses elle-même.
- `firecrawl_search` "BTC/USD price feed deviation threshold heartbeat mainnet", domaine
  `data.chain.link` → succès, page BTC/USD directe (0,5%) + bonus : liste de 28 opérateurs
  nommés avec leur soumission individuelle de prix (hors périmètre Q1, noté pour mémoire —
  confirme que data.chain.link publie des noms d'opérateurs au moins pour ce feed, cohérent
  avec le constat déjà fait par SONDE-artefact.md §1.3a pour rsETH).
- 4byte.directory ×4 (résolution de sélecteurs `description()`, `aggregator()`,
  `latestRoundData()`, `getRoundData(uint80)`) → tous succès.
- RPC `https://ethereum.publicnode.com` : `description()`, `aggregator()`, `latestRoundData()`
  sur les proxies ETH/USD et BTC/USD (4 appels simples) → tous succès ; 2 requêtes batch
  JSON-RPC de 60 `getRoundData()` chacune (ETH/USD, BTC/USD) → toutes deux succès complet
  (60/60 réponses avec `result`, aucune erreur).
- Script Python local (re-catégorisation gap long/court sur les 59 lignes ETH/USD, déclenché
  par la correction post-advisor) → succès, aucune nouvelle requête réseau nécessaire.

---

## Q2 — Pyth Network : intervalle de confiance ETH/USD

### Sémantique (docs.pyth.network/price-feeds/core/best-practices, section « Confidence
Intervals » — [lu-extrait, brut] via firecrawl_search, texte retourné intégralement,
pas une synthèse IA)

Verbatim (extraits ≤30 mots chacun, source : `https://docs.pyth.network/price-feeds/core/
best-practices#confidence-intervals`) :

> « At every point in time, Pyth publishes both a price and a confidence interval for each
> product. [...] Pyth may publish the current price of bitcoin as $50000 ± $10. »

> « Pyth publishes a confidence interval because, in real markets, there is no one single
> price for a product. »

> « In a Pyth feed, each publisher specifies an interval (p_i-c_i, p_i+c_i) [...] This
> interval is intended to achieve 95% coverage, i.e. the publisher expresses the belief that
> this interval contains the "true" price with 95% probability. »

> « The resulting aggregate interval (μ-σ, μ+σ), where μ represents the aggregate price and σ
> represents the aggregate confidence, is a good estimate of a range in which the true price
> lies. »

**Deux régimes explicitement distingués par la doc (paraphrase fidèle, pas verbatim continu)** :
1. **Recouvrement total des intervalles publishers** (« normal operating conditions ») →
   l'intervalle agrégé = l'intervalle individuel, couverture à 100%.
2. **Intervalles disjoints entre publishers** (« atypical scenario », cité comme survenant
   « during market volatility or unusual events ») → l'intervalle agrégé se comporte comme un
   analogue d'un **écart interquartile** (IQR) sur l'ensemble des 3 points soumis par chaque
   publisher (prix, prix+conf, prix-conf) — **propriété anti-manipulation explicite** : « this
   property is necessary to ensure that a small group of publishers cannot manipulate the
   aggregate confidence interval » [lu, verbatim].

**Recommandation d'usage — LE point directement pertinent pour un seuil τ**, verbatim :
> « It can decide that there is too much uncertainty when σ/μ exceeds some threshold and
> choose to pause any new activity that depends on the price of this asset. »

**Distinction conceptuelle à ne pas fondre avec τ Shōgen (franchise imposée)** : ce σ/μ Pyth
est l'incertitude AGRÉGÉE INTERNE À UNE SEULE SOURCE (dispersion entre publishers Pyth,
compressée dans un seul chiffre de confiance par le protocole Pyth lui-même), alors que le τ
Shōgen mesure l'écart RELATIF ENTRE SOURCES EXTERNES DISTINCTES (Chainlink vs Pyth vs
DefiLlama vs CoinGecko...). Ce sont deux objets mathématiquement analogues (un ratio
relatif comparé à un seuil pour déclencher une action) mais mesurant des choses différentes —
**cité comme précédent conceptuel canonique de la pratique du secteur** (« un protocole oracle
majeur formalise déjà l'idée d'un seuil relatif d'incertitude »), pas comme une preuve
directe transposable telle quelle.

Autre usage documenté (même page, [lu] verbatim) — asymétrie de valorisation collatéral/dette :
> « a lending protocol valuing a user's collateral can use the lower valuation price μ-σ. [...]
> it can use the higher end of the interval by using the price μ+σ. »

### Magnitude typique — deux sources convergentes

**(a) Exemple illustratif de la doc elle-même** (même page, [lu] verbatim, PAS daté
explicitement sur la page) :
> « Note that $1000 is an unusually large confidence interval for bitcoin; the confidence
> interval is typically $50 dollars ».
Sur un prix illustratif de $50 000, cela correspond à un ratio σ/μ ≈ **0,1%** — mais ceci est un
chiffre D'EXEMPLE dans la documentation, pas nécessairement calé sur le marché actuel (page non
datée explicitement).

**(b) Mesure empirique LIVE, ce jour (2026-08-26), via l'API Hermes** (`hermes.pyth.network`),
feed ETH/USD identifié via l'endpoint de découverte officiel `/v2/price_feeds?query=ETH/USD`
(PAS deviné) : id `ff61491a931112ddf1bd8147cd1b641375f79f5825126d665480874634fd0ace`
(« ETHEREUM / US DOLLAR », base ETH). Feed BTC/USD (comparaison) : id
`e62df6c8b4a85fe1a67db44dc12de5db330f7ac66b72dc658afedf0f4a415b43` — recoupé indépendamment
avec un exemple de code déjà présent dans `docs.pyth.network` (page Stacks pull-integration)
qui cite exactement le même identifiant comme « the official BTC price feed id » — [lu],
concordance exacte. [lu, primaire, live, ce jour]

**Trois échantillons ETH/USD, espacés dans le temps** (`/v2/updates/price/latest`, champ
`parsed`, PAS un résumé — valeurs brutes JSON décodées avec `expo=-8`) :

| Heure (UTC) | Prix | Confidence | σ/μ (relatif) |
|---|---|---|---|
| 2026-08-26T12:55:11 | $2 454,44 | $0,8624 | **0,0351%** |
| 2026-08-26T12:55:25 | $2 455,48 | $0,8680 | **0,0354%** |
| 2026-08-26T12:55:46 | $2 455,70 | $0,8979 | **0,0366%** |

**Un échantillon BTC/USD (même instant, 12:55:46 UTC)** : prix $78 311,71, confidence $21,93,
σ/μ = **0,028%**. Notablement plus SERRÉ que le chiffre illustratif « typiquement $50 » de la
doc (qui donnerait ~0,1% à ce niveau de prix — la doc n'étant pas datée, il n'y a pas de
contradiction établie, seulement un écart entre un exemple pédagogique non daté et une mesure
live d'aujourd'hui).

**Verdict Q2** : magnitude typique σ/μ pour ETH/USD en régime calme (échantillon de ce jour) ≈
**0,03-0,04%** — un ordre de grandeur SOUS le seuil de déviation Chainlink (0,5%, Q1) et bien
en dessous des P99 inter-sources mesurés par S2 (0,43%-0,71%). Ceci situe le bruit interne
propre à Pyth (dispersion inter-publishers Pyth agrégée en un seul chiffre) comme un plancher
largement inférieur à l'écart inter-sources visé par τ — cohérent avec le fait que τ doit
capturer un phénomène inter-sources plus large que le simple bruit de collecte intra-Pyth.

### Journal des URL — Q2
- `firecrawl_search` "Pyth Network price confidence interval what does it mean best
  practices", domaine `docs.pyth.network` → succès, 5 résultats, page « Best Practices »
  retournée en texte quasi intégral (section Confidence Intervals complète).
- `curl https://hermes.pyth.network/v2/price_feeds?query=ETH/USD&asset_type=crypto` → succès,
  liste de 18 feeds contenant ETH, id canonique identifié sans ambiguïté (« ETHEREUM / US
  DOLLAR », base=ETH exact).
- `curl https://hermes.pyth.network/v2/updates/price/latest?ids[]=<eth_id>&parsed=true` ×2 →
  succès (échantillons 1 et 2).
- `curl https://hermes.pyth.network/v2/price_feeds?query=BTC/USD&asset_type=crypto` → succès,
  id BTC/USD confirmé.
- `curl https://hermes.pyth.network/v2/updates/price/latest?ids[]=<eth_id>&ids[]=<btc_id>&
  parsed=true` → succès (échantillon 3 ETH + échantillon BTC).

---

## Q3 — DefiLlama et CoinGecko : méthodologie de prix + cadence

### CoinGecko — méthodologie ([lu-extrait, brut] via firecrawl_search sur
`www.coingecko.com/en/methodology`, texte retourné quasi intégralement, pas une synthèse IA)

Verbatim (≤30 mots par extrait) :
> « By aggregating data across multiple tickers through a comprehensive algorithm, we
> calculate the market price of each coin. »

> « an initial ticker set is constructed based on the top 600 tickers by volume of a
> particular coin »

> « For coins with three tickers or more, CoinGecko applies an outlier detection algorithm
> by calculating the lower and upper bounds based on the median absolute deviation (MAD). »

> « For coins with less than three tickers, any ticker price change that is greater than
> 100x from the previous price will be classified as an outlier. »

> « Once outliers have been removed, we calculate the VWAP of all remaining tickers in the
> ticker set to arrive at the final aggregated price. »

> « In certain cases, our operations team may intervene to exclude outliers if the team
> believes a certain ticker price to be anomalous but was not excluded by our outlier
> detection algorithm. »

**Résumé méthodologique fidèle (paraphrase)** : (1) construction d'un ensemble initial jusqu'à
600 tickers par volume ; (2) filtrage des outliers par MAD (Median Absolute Deviation, ≥3
tickers) ou règle simple ×100 (<3 tickers) ; (3) VWAP (Volume-Weighted Average Price) des
tickers restants = prix final ; (4) intervention manuelle possible de l'équipe CoinGecko en
supplément de l'algorithme. Prérequis : conversion BTC via un Bitcoin Price Index (BPI) lui-même
en VWAP de tickers BTC/USD, BTC/USDT, BTC/USDC, BTC/EUR sur des exchanges sélectionnés.
**Ceci est une méthode de LISSAGE STATISTIQUE ROBUSTE** (MAD + VWAP), pas un point de marché
brut — explique mécaniquement une partie de la latitude/décalage face à un prix Chainlink/Pyth
quasi-instantané d'une seule source.

### CoinGecko — cadence de mise à jour : **TROIS chiffres officiels DIVERGENTS trouvés,
rapportés séparément, non fondus (contradiction à consigner)**

1. `docs.coingecko.com/reference/simple-price` (documentation de référence API, endpoint
   `/simple/price`), [lu-extrait, brut], verbatim : « Cache / Update Frequency: Every 20
   seconds (Paid API) — Every 60 seconds (Demo / Keyless API) »
2. `support.coingecko.com` (FAQ support, article « How often does data get updated or
   refreshed? »), [lu-extrait, brut], verbatim : « Most endpoints are cached for around 1 to 5
   minutes [...] Pro API (paid plans) generally have equal or faster update frequency, i.e.,
   30 sec for simple/price endpoint. »
3. `www.coingecko.com/en/faq` (FAQ publique du site), [lu-extrait, brut], verbatim : « Price,
   trading volume, market capitalization - Updated every 1 to 10 minutes »
   Même page : « Circulating supply - Updated every 5 minutes » ; « Blockchain information
   (Mining difficulty, total blocks, transactions per second etc.) - updated every 1 hour ».

**Constat honnête** : (1) et (2) se contredisent légèrement sur le chiffre EXACT pour l'API
Pro/Paid du même endpoint `/simple/price` (20s vs 30s) — divergence mineure entre deux pages
officielles CoinGecko elles-mêmes, aucune des deux datée explicitement sur la page. (3) donne
un chiffre différent et plus large (1-10 min) mais concerne apparemment l'affichage SITE plutôt
que l'API brute. **Aucune des trois pages n'est datée explicitement** — impossible de trancher
laquelle est la plus à jour ; toutes trois sont d'accès libre aujourd'hui (2026-08-26).

### DefiLlama — méthodologie de prix ([lu-extrait, brut] via firecrawl_search, page
`https://docs.llama.fi/`, section « Our Methodology » / « Valuing different tokens »)

Verbatim exact :
> « Almost all tokens are priced using CoinGecko's API. Where this can't be done, we can
> accommodate using on-chain methods to quantify the value of a token. This is most commonly
> done by comparing the pool weights of a very liquid Uniswap V2 market. »

**Implication directe pour Q3** : DefiLlama n'est PAS une source de prix indépendante au sens
strict pour la majorité des actifs — elle **hérite structurellement de CoinGecko** comme source
primaire, avec un REPLI on-chain (pool Uniswap V2) uniquement quand CoinGecko ne couvre pas
l'actif. Ceci est la page de méthodologie GÉNÉRALE (contexte TVL) ; NON confirmé si l'API
`coins.llama.fi` (utilisée pour un prix ponctuel programmable, distincte du contexte TVL)
applique exactement la même règle à 100% du temps.

**Piste explorée et non concluante** : page `docs.llama.fi/list-your-project/oracles-tvs.md`
(« Oracle Price Sourcing and Validation ») — [lu] via WebFetch — NE décrit PAS la méthodologie
de tarification propre de DefiLlama ; c'est un guide destiné aux PROJETS listés pour classifier
LEURS PROPRES oracles (primary/aggregator/reference) dans le cadre du calcul TVS (Total Value
Secured), hors sujet direct pour Q3. Mentionné pour mémoire, écarté du verdict.

**Confirmation empirique d'une source DUALE dans l'API `coins.llama.fi` elle-même** — requête
live ce jour (2026-08-26T12:57:50 UTC) sur trois clés simultanément :
```
coingecko:ethereum        → price $2456.091688111294, confidence 0.99
ethereum:0xC02aaA...756Cc2 (WETH) → price $2457.713558510655, confidence 0.99
coingecko:bitcoin         → price $78383.42728127395, confidence 0.99
```
[lu, primaire, live, ce jour] — Le prix retourné pour la clé `coingecko:ethereum` DIFFÈRE de
celui retourné pour la clé `ethereum:0xC02a...` (contrat WETH), au MÊME timestamp exact
(1787749070) : écart relatif ≈ **0,066%**. Ceci confirme EMPIRIQUEMENT que DefiLlama calcule au
moins DEUX pipelines de prix distincts pour « le même » actif sous-jacent selon la clé
interrogée (CoinGecko direct vs dérivé on-chain/DEX pour la clé par adresse de contrat) —
cohérent avec le texte de méthodologie ci-dessus, et **mécanisme plausible expliquant en partie
pourquoi le P99 DefiLlama mesuré par S2 (~0,71%) est PLUS LARGE que celui de CoinGecko seul
(~0,43%)** : DefiLlama peut inclure un chemin de tarification on-chain/DEX (spread, profondeur
de liquidité, staleness de bloc) en plus/à la place d'un chemin CEX-agrégé propre.

**Champ « confidence » (valeur observée : 0,99 sur les trois clés testées)** : AUCUNE page de
documentation officielle DÉFINISSANT précisément ce champ n'a été trouvée malgré plusieurs
tentatives (voir Journal des URL) — recherché sur `api-docs.defillama.com` (page racine +
`/llms-free.txt`, tous deux [lu] via WebFetch, silencieux sur ce champ), et par recherche
GitHub ciblée (`defillama-server`, aucun résultat direct). **NON TROUVÉ** — signalé comme tel,
procurement formé ci-dessous plutôt que deviné.

### DefiLlama — cadence de mise à jour : mesure empirique directe, **CORRIGÉE après un 3e
échantillon (P1, primaire, ce jour, résultat honnêtement révisé — pas juste nuancé)**

**[CORRECTION POST-ADVISOR]** La première rédaction concluait à une « granularité de 300
secondes pile » à partir de DEUX échantillons (donc UN seul intervalle mesuré). L'advisor a
signalé qu'un seul intervalle ne suffit pas à établir une périodicité fixe et a suggéré un
troisième échantillon, à coût quasi nul. **Ce troisième échantillon INFIRME la conclusion
initiale plutôt que de la confirmer** — traité honnêtement ci-dessous.

Trois requêtes live sur la même clé `coingecko:ethereum`, horodatage RÉEL noté avant chaque
appel :

| # | Heure réelle (UTC) | Timestamp interne renvoyé | Écart au précédent |
|---|---|---|---|
| 1 | 13:02:08 | 2026-08-26T12:58:40 | (référence) |
| 2 | 13:06:58 | 2026-08-26T13:03:40 | **exactement 300s** |
| 3 | 13:30:07 | 2026-08-26T13:24:50 | **1270s** (= 4×300s + 70s — PAS un multiple simple de 300) |

**Constat honnête, révisé** : le premier intervalle (300s pile) était probablement une
coïncidence, pas une preuve de minuteur à phase fixe. Le second intervalle mesuré (1270s) n'est
PAS un multiple entier de 300s, et l'horodatage renvoyé ne tombe plus sur le même « alignement
de seconde » (`:40` pour les échantillons 1 et 2, `:50` pour l'échantillon 3) — incompatible
avec un minuteur strictement périodique à phase fixe débutant sur une epoch commune. **La
cadence de rafraîchissement de `coins.llama.fi` sur cette clé n'est donc PAS démontrée comme
une période fixe de 300s** ; elle est probablement de l'ordre de quelques minutes (compatible
avec la fourchette générale revendiquée par CoinGecko elle-même, « 1 à 5 » / « 1 à 10 » minutes
selon la page citée plus haut), mais avec une composante non périodique (jitter, dépendance à
la disponibilité amont, ou polling non synchronisé) que cette passe ne caractérise pas plus
précisément — **NON TROUVÉ pour une valeur de cadence unique et fixe**, consigné comme tel
plutôt que de forcer une fausse précision.

### Verdict Q3 — ce qui explique la latitude des P99 mesurés (0,71% DefiLlama, 0,43% CoinGecko)

1. **CoinGecko (P99 ~0,43%)** : prix = VWAP après filtrage MAD sur jusqu'à 600 tickers — un
   LISSAGE ROBUSTE actif, PAS un point de marché unique — plus une cadence de rafraîchissement
   revendiquée de 1 à 10 minutes selon la page CoinGecko citée, donc un potentiel de staleness
   de plusieurs minutes face à une source quasi temps réel (Chainlink/Pyth).
2. **DefiLlama (P99 ~0,71%, PLUS LARGE)** : hérite de CoinGecko pour « presque tous » les
   tokens MAIS bascule sur un calcul ON-CHAIN/DEX (pool Uniswap V2 ou équivalent) quand
   CoinGecko ne couvre pas l'actif — et la preuve empirique ci-dessus montre qu'au moins DEUX
   pipelines de prix distincts (CoinGecko-direct vs contrat) coexistent avec un écart mesuré de
   0,066% même sur un actif aussi liquide que WETH, au même instant, PLUS une cadence de
   rafraîchissement mesurée comme non strictement périodique (quelques minutes, avec jitter).
   Un chemin on-chain/DEX ajoute nativement spread, profondeur, latence de bloc — plausiblement
   la source du P99 plus large que CoinGecko seul. **Hypothèse motivée par les faits
   rassemblés, pas confirmée par une déclaration explicite de DefiLlama chiffrant cet écart**
   — présentée comme telle.

### Journal des URL — Q3
- `firecrawl_search` "CoinGecko methodology how prices are calculated cache update frequency",
  domaines coingecko.com/docs.coingecko.com → succès, 6 résultats : méthodologie complète
  (VWAP/MAD/600 tickers), page API reference (20s/60s), FAQ support (30s/1-5min), FAQ site
  (1-10min).
- `firecrawl_search` "DefiLlama coins API price methodology confidence how prices calculated",
  domaine defillama.com → échec de pertinence (résultats hors-sujet : pages TVL de protocoles
  individuels, dashboards).
- `firecrawl_search` "DefiLlama coins API pricing confidence field documentation current
  prices endpoint", domaine api-docs.defillama.com → **0 résultat**.
- `WebFetch https://api-docs.defillama.com/` → succès d'accès, mais page racine ne contient
  pas le détail cherché ; réfère à `/llms-free.txt`.
- `WebFetch https://api-docs.defillama.com/llms-free.txt` → succès d'accès, confirme
  l'endpoint `/prices/current/{coins}` existe mais SANS détailler confidence/méthodologie/
  cadence.
- `firecrawl_research_search_github` "DefiLlama coins pricing confidence methodology README"
  → succès d'accès (9 résultats) mais AUCUN ne définit le champ confidence.
- `firecrawl_search` "defillama-server confidence 0.99 spot price DEX price source coins",
  catégorie github → **0 résultat**.
- `firecrawl_search` "coins prices methodology sources DEX volume weighted confidence",
  domaine docs.llama.fi → **0 résultat**.
- `WebFetch https://docs.llama.fi/` → succès, a révélé la section méthodologie générale
  (« Valuing different tokens ») + le chemin `/list-your-project/oracles-tvs.md`.
- `WebFetch https://docs.llama.fi/list-your-project/oracles-tvs.md` → succès d'accès, mais
  hors-sujet pour la méthodologie de tarification propre de DefiLlama (guide de classification
  d'oracles pour projets listés).
- `firecrawl_search` "Valuing different tokens CoinGecko API on-chain Uniswap V2 pool
  weights", domaine docs.llama.fi → succès, verbatim propre obtenu directement.
- `firecrawl_search` "DefiLlama coins API prices update frequency cache minutes seconds cron"
  → résultats hors-sujet (pollution : sites tiers non-officiels, contenu non pertinent).
- `curl https://coins.llama.fi/prices/current/coingecko:ethereum,ethereum:0xC02a...,
  coingecko:bitcoin` → succès (structure duale confirmée).
- `curl https://coins.llama.fi/prices/current/coingecko:ethereum` ×3 (13:02, 13:06, 13:30 UTC)
  → tous succès ; le 3e échantillon (ajouté sur suggestion advisor) infirme la périodicité
  fixe de 300s suggérée par les 2 premiers — voir correction ci-dessus.

---

## Q4 — Moniteurs de risque oracle (LlamaRisk, Chaos Labs, Gauntlet) : écart traité comme alerte

### Constat global (à énoncer en premier, honnête) : AUCUN des trois moniteurs nommés ne publie
de seuil numérique UNIVERSEL d'alerte pour l'écart relatif de prix — chacun explicite pourquoi

### Chaos Labs — trois sources, aucune ne publie de seuil universel

**(1) « Oracle Data Freshness, Accuracy, Latency Pt. 5 »**, Chaos Labs, auteur Omer Goldberg,
**16 septembre 2024** (hors fenêtre 2025-2026 stricte, mais série méthodologique de référence
citée pour son contenu). [lu-extrait via WebFetch, prompt ciblé, portions entre guillemets
présentées comme verbatim par l'outil] :
> « We expect this value to be less than the asset's fee floor on its most liquid DEX pools
> (e.g. 5 bps for an ETH/USD oracle, corresponding to Uniswap V3's 0.05% WETH/USDC fee
> floor) »
Ceci est un objectif/cible D'EXACTITUDE (accuracy target), PAS un seuil d'ALERTE au sens strict
— présenté comme la précision attendue en régime normal, avec un raisonnement économique
(arbitrage CEX/DEX) plutôt qu'un chiffre arbitraire. Méthode citée : « percentage deviation
from the benchmark [...] across multiple data point samples ».

**(2) « Oracle Risk Portal »**, Chaos Labs, auteur Omer Goldberg, **8 mai 2024** (hors fenêtre).
[lu-extrait via WebFetch] : le portail rapporte les déviations de prix en **percentiles
statistiques (moyenne, médiane, P75, P95)** — méthodologiquement proche de l'approche P99 de
S2 — mais **« no specific numeric thresholds, percentages, or basis points are defined to
classify oracle risk levels or trigger alerts »** (constat du fetch, pas un verbatim direct de
la page). Défini comme un choix EXPLICITE de ne pas figer de seuil universel.

**(3) « Risk Oracles: One Step Beyond Price Oracles »**, Chaos Labs, **22 août 2025** (DANS la
fenêtre demandée). [lu-extrait via WebFetch] : cite le OWASP Smart Contract Top 10 (édition
2025) plaçant la manipulation d'oracle de prix au 2e rang des risques DeFi ; déclare que les
Risk Oracles opèrent « within governance-dictated and predefined limits » **sans divulguer ces
limites chiffrées**. Aucun seuil numérique trouvé dans ce post non plus.

**(4) Page produit live `chaoslabs.xyz/oracles`** (« The Oracle Built for Real-Time Risk »,
Edge, consultée ce jour 2026-08-26, PAS un post daté — page produit dynamique). [lu-extrait via
WebFetch] : widget « Threshold » affichant des valeurs **0,25% à 0,5%** selon l'actif/réseau —
décrit contextuellement comme des SEUILS DE DÉCLENCHEMENT DE MISE À JOUR DE PRIX (mécanisme de
type Chainlink deviation-threshold), PAS explicitement comme des seuils d'ALERTE de risque.
Verbatim de positionnement : « High-precision, low-latency price data with real-time anomaly
filtering » ; données consommées « 5× per second ». **Convergence notable, non forcée** : ce
propre produit oracle de Chaos Labs utilise des seuils du MÊME ORDRE DE GRANDEUR que Chainlink
(0,25-0,5%) — un point de convergence industrie, pas une preuve d'un standard partagé déclaré.

### LlamaRisk — la source la plus concrète trouvée pour Q4 (ET directement réutilisable en Q5)

**« When Pricing Breaks: A USDe Case »**, LlamaRisk, **18 octobre 2025** (DANS la fenêtre,
8 jours après l'incident USDe du 10 octobre 2025). [lu-extrait via WebFetch, deux fetches
indépendantes convergentes, portions entre guillemets présentées comme verbatim par l'outil] :

> « The Chainlink oracle deviated by a maximum of 65 bps. The Pyth oracle deviated by a
> maximum of 430 bps (4.3%). The Binance Spot Price deviated by over 3,500 bps (35%). »

> « A deviation of 65 bps is well within the safety parameters of a well-configured lending
> protocol. »

**C'est le jugement le plus direct et le plus concrètement daté trouvé dans toute cette
question** : un moniteur de risque nommé, 8 jours après un incident RÉEL de grande ampleur,
qualifie explicitement **65 bps (0,65%)** de déviation d'oracle décentralisé (Chainlink) comme
« bien dans les paramètres de sécurité » — implicitement, un déclencheur d'alerte utile se
situerait AU-DESSUS de cet ordre de grandeur. Le contraste avec Pyth (430 bps/4,3%, non
qualifié explicitement de dangereux dans l'extrait obtenu) et Binance (3500 bps/35%, présenté
comme un échec systémique) donne une ÉCHELLE empirique et datée : ~0,65% = sûr ; ~4,3% = notable
mais le protocole (Aave) a survécu ; ~35% = catastrophique (mais c'est un prix CEX interne, pas
un oracle décentralisé). **Référence non explicitée avec certitude** pour le calcul de ces
déviations (le fetch indique : probablement le peg $1, contexte non confirmé en toutes lettres
dans l'extrait obtenu) — signalé en NON TROUVÉ ci-dessous, procurement formé pour lecture
intégrale de la page.

**Autres pistes LlamaRisk identifiées mais NON approfondies (timebox Q4, notées pour mémoire)** :
- `gov.curve.finance/t/llamarisk-progress-update-july-december-2025/10981` — « Developed
  methodology and internal tooling for monitoring Oracle setups using Curve AMM as price
  source » — [abs, titre/extrait seulement, PAS ouvert intégralement].
- `llamarisk.com/research/risk-alternative-prisma-oracles-comparative-analysis` — décrit une
  étude comparative « using historical data to determine the mean and standard deviation of
  Oracle deviations against a reference spot price » — approche statistique proche de SPC
  (moyenne/écart-type), potentiellement pertinente pour Q6, **NON ouverte intégralement dans
  cette passe** faute de budget — piste signalée, pas creusée.

### Gauntlet — un seul document trouvé, hors fenêtre, sans chiffre

`governance.aave.com/t/bgd-correlated-asset-price-oracle/16133/4` (réponse de Gauntlet au fil
de gouvernance BGD sur CAPO), **22 janvier 2024** (hors fenêtre 2025-2026). [lu-extrait via
WebFetch] : Gauntlet soutient l'introduction de CAPO, recommande « a mechanism to prevent
upward price dislocations from the expected fixed value » pour les stablecoins mais déconseille
un plancher (downward threshold) pour ne pas bloquer les liquidations en cas de dépeg réel.
**Aucun chiffre numérique de seuil trouvé dans ce post.** Utile comme contexte de conception
CAPO pour Q5, pas comme réponse chiffrée à Q4.

### Verdict Q4

**Aucun seuil universel publié par les trois moniteurs nommés** — constat NÉGATIF mais robuste
(6 documents consultés au total : 4 Chaos Labs dont 1 page produit live, 1 LlamaRisk, 1
Gauntlet). L'ancrage empirique le plus concret et le mieux daté est le jugement LlamaRisk du
18 octobre 2025 : **65 bps (0,65%) qualifié explicitement de « bien dans les paramètres de
sécurité »** pour un oracle décentralisé pendant un épisode de stress RÉEL et sévère. Ceci est
cohérent d'ordre de grandeur avec le seuil de déviation Chainlink documenté en Q1 (0,5%) et les
seuils Chaos Labs Edge observés live (0,25-0,5%) — trois sources indépendantes convergent sur
un ordre de grandeur de quelques dixièmes de pourcent comme « normal/sûr », sans qu'aucune ne
le formalise comme un seuil d'ALERTE universel chiffré et publié comme tel.

### Journal des URL — Q4
- `firecrawl_search` "Chaos Labs oracle risk monitoring deviation threshold alert 2025 2026"
  → succès, 8 résultats dont les 3 posts Chaos Labs + la page produit `/oracles`.
- `WebFetch https://chaoslabs.xyz/posts/oracle-data-freshness-accuracy-latency-pt-5` → succès.
- `firecrawl_search` "Chaos Labs oracle risk portal deviation threshold methodology 2025 2026",
  domaine chaoslabs.xyz → **0 résultat**.
- `WebFetch https://chaoslabs.xyz/posts/oracle-risk-portal` → succès.
- `WebFetch https://chaoslabs.xyz/oracles` → succès.
- `firecrawl_search` "Gauntlet oracle price deviation alert threshold risk parameter 2025 2026"
  → succès, 8 résultats (avec pollution notable « Oracle Corp »/ORCL stock — filtrée, non
  citée) ; a mené à OWASP Smart Contract Top 10 2026 et au post Chaos Labs du 22 août 2025.
- `WebFetch https://raw.githubusercontent.com/OWASP/www-project-smart-contract-top-10/main/
  2026/en/src/SC03-price-oracle-manipulation.md` → succès.
- `WebFetch https://chaoslabs.xyz/posts/risk-oracles-one-step-beyond-price-oracles` → succès.
- `WebFetch https://governance.aave.com/t/bgd-correlated-asset-price-oracle/16133/4` → succès.
- `firecrawl_search` "LlamaRisk price oracle deviation threshold alert monitoring 2025 2026"
  → succès, 8 résultats dont « When Pricing Breaks: A USDe Case » (trouvaille décisive).
- `WebFetch https://llamarisk.com/research/when-pricing-breaks-usde` ×2 (prompts différents,
  second plus ciblé sur le verbatim exact) → succès les deux fois, résultats convergents.

---

## Q5 — Magnitudes de vraies dislocations (USDe, CAPO, KelpDAO) — réutilisation + re-vérification

### Rappel du contenu réutilisé (voir section ÉCART ci-dessus pour la localisation réelle)
Contenu de base réutilisé depuis `SONDE-artefact.md` §3 (« Douleur récente — incidents oracle
2025-2026 »), lui-même déjà porteur de sa propre discipline [lu]/[abs]/[2nd]. Conformément à
l'instruction de la mission, **chaque chiffre destiné à la décision τ est re-vérifié sur source
primaire ci-dessous** — je ne recopie pas tel quel, je vérifie.

### 5.1 CAPO / Aave (10 mars 2026) — RE-VÉRIFIÉ EN PRIMAIRE, upgrade [2nd]→[lu]

**Avant** (SONDE-artefact.md §3.3) : chiffre de « ≈2,85% » en **[2nd]** (WebSearch, aucune
source primaire ouverte, CoinDesk 429, dev.to 404).

**Après re-vérification** : post-mortem OFFICIEL Aave gouvernance, `governance.aave.com/t/
post-mortem-exchange-rate-misallignment-on-wsteth-core-and-prime-instances/24269` — **[lu via
WebFetch, extraction en liste à puces, PAS entre guillemets — précision de niveau ajoutée après
relecture advisor]**, prompt ciblé sur les chiffres exacts. **P1, primaire, source du protocole
lui-même**, mais le chiffre « 2,85% » lui-même n'est pas un verbatim textuel exact retrouvé
entre guillemets — c'est une extraction fidèle mais reformulée par l'outil, à distinguer des
citations verbatim entre « » utilisées ailleurs dans cette archive.

Faits confirmés, avec mécanisme PRÉCIS (plus détaillé que SONDE) :
- **Date/heure** : 10 mars 2026, 19h50 (heure du post).
- **Ratios exacts** : configuration précédente `snapshotRatio` ≈ **1,1572** ; cible voulue
  ≈ **1,2282** ; valeur effectivement atteinte après la mise à jour contrainte ≈ **1,1919**.
- **Cause mécanique EXACTE** (absente de SONDE, ajout de cette re-vérification) : un
  RATE-LIMITER on-chain plafonne les mises à jour de `snapshotRatio` à **« maximum 3% increase
  every 3 days »** — ce plafond a empêché d'atteindre en une seule transaction la cible réelle
  (vieille de 7 jours), tandis que le paramètre d'horodatage (`snapshotTimestamp`), lui, a
  avancé sans validation correspondante → désynchronisation ratio/horodatage. Caractérisation
  officielle verbatim (via le fetch, celle-ci ENTRE guillemets dans la sortie de l'outil) : « The
  root cause was differing update constraints at the smart contract level, which ultimately
  resulted in a misalignment between the snapshot ratio and snapshot timestamp onchain. »
- **Impact** : ~$26-27M de liquidations, **10 938 wstETH liquidés**, **34 comptes** touchés.
- **Déviation effective du taux de change** : **≈2,85%** — chiffre identique à celui déjà
  trouvé par SONDE en [2nd] (`spendnode.io`, `finance.yahoo.com` : « undervalued wstETH by
  2.85% ») — **trois sources indépendantes convergent sur 2,85%** (2 presse [2nd] + 1 primaire
  [lu, non-verbatim] désormais).
- **Caractérisation officielle** : « configuration issue », explicitement PAS un piratage/
  exploit malveillant d'oracle.

**[CORRECTION POST-ADVISOR] Tension arithmétique non signalée dans la première rédaction,
détectée et vérifiée** : `(1,2282 − 1,1919) / 1,2282 = 2,956 %` — soit **~2,96%**, PAS 2,85%,
si on recalcule directement à partir des deux ratios rapportés par le même post-mortem. Les
deux chiffres (les ratios arrondis à 4 décimales, et le « 2,85% » de déviation effective
annoncé séparément) proviennent de la MÊME source primaire mais ne se recoupent pas exactement
à l'arithmétique simple — probablement un effet d'arrondi sur les ratios affichés ou une base
de calcul légèrement différente (ex. déviation mesurée à un bloc différent de celui des ratios
cités, ou prenant en compte un autre point de référence). **Non résolu, signalé plutôt que
lissé** ; sans incidence d'ordre de grandeur sur l'usage pour τ (2,85% et 2,96% pointent tous
deux vers la même fourchette « quelques % », pas un ordre de grandeur différent).

**Contradiction mineure additionnelle, déjà notée avant la relecture advisor** : un post
X/Twitter (@ManoppoMarco, [2nd], non ouvert en primaire) cite un taux plafonné « ~1,1939 »
légèrement différent des « ≈1,1919 » du post-mortem officiel ([lu]) — écart de 0,002 point,
non tranché.

**Verdict Q5/CAPO** : le chiffre ≈2,85% (ou ≈2,96% par recalcul direct des ratios — les deux
émanant de la même source primaire) est maintenant établi en lecture primaire du protocole,
pas seulement en [2nd] de presse. La réserve G2 de la mission est levée pour ce chiffre, avec
la tension arithmétique ci-dessus honnêtement signalée plutôt que masquée. Le mécanisme réel
(rate-limiter de mise à jour + désynchronisation d'horodatage) est plus riche que ce que SONDE
avait absorbé, et confirme le cadrage de SONDE (« bug de configuration/fraîcheur, pas un défaut
de diversité de sources ») : **CAPO reste hors du périmètre k_eff/diversité**, mais devient un
bon POINT D'ANCRAGE POUR τ dans un autre sens — c'est un exemple RÉEL, DATÉ, PRIMAIRE d'une
déviation de l'ordre de **2,85-2,96%** provoquée par de la mécanique de contrat AUTOUR d'un
oracle (pas l'oracle lui-même) qui a déclenché des liquidations forcées. Une valeur de τ
voisine de 2-3% capturerait ce type d'événement ; une valeur beaucoup plus large (ex. >5%) le
manquerait.

### 5.2 USDe / Binance (10 octobre 2025) — RE-VÉRIFIÉ, MAGNITUDE PRÉCISÉE AU-DELÀ DE SONDE

**Avant** (SONDE-artefact.md §3.1) : fourchette **[abs/2nd]** « ~0,65-0,68 $ sur Binance ...
alors qu'il restait proche de 0,99-1 $ ailleurs » — pas de chiffre de déviation relative
explicite, pas de source primaire ouverte pour CE chiffre précis (seuls les montants $283M/
$346M étaient [lu] par SONDE).

**Après re-vérification, DEUX chiffres relatifs désormais disponibles, convergents et mieux
sourcés que SONDE** :

**(a) Ampleur du dépeg lui-même** — CoinGecko (source nommée du corpus Q3), page
`coingecko.com/learn/october-10-crypto-crash-explained`, mise à jour le 6 février 2026 (dans la
fenêtre). [lu-extrait via WebFetch], verbatim : « USDe fell to $0.65 on Binance (35% below its
$1 peg) » pendant la fenêtre « 21:36-22:15 UTC » le 10 octobre 2025. **Convergence
supplémentaire, non ouverte en primaire mais fortement corroborante** : 7 sources de presse/
recherche indépendantes (Galaxy Digital, FTI Consulting, CoinDesk Data, Lexology, TradingView/
Coinpedia — celle-ci avec la précision maximale « $0.6567 » —, BitPinas) convergent toutes sur
un prix plancher de ~$0,65-0,657 sur Binance spécifiquement, pendant la même fenêtre horaire
que celle déjà notée par SONDE (~21:36-22:16 UTC).

**(b) Déviation D'ORACLE mesurée pendant le même incident** — LlamaRisk, « When Pricing Breaks:
A USDe Case », 18 octobre 2025 (déjà établi en Q4 ci-dessus, réutilisé ici pour Q5) : «
Chainlink oracle deviated by a maximum of 65 bps [...] Pyth oracle deviated by a maximum of
430 bps (4.3%) [...] Binance Spot Price deviated by over 3,500 bps (35%). » **Le chiffre «
35% » de LlamaRisk pour Binance CONCORDE EXACTEMENT avec le « 35% below peg » de CoinGecko** —
deux sources indépendantes et nommées, [lu-extrait] toutes les deux, convergent sur la même
valeur au point de pourcentage près.

**Distinction cruciale à ne jamais fondre (répétée de SONDE, confirmée par cette re-
vérification)** : le -35% est la déviation du PRIX SPOT INTERNE DE BINANCE (carnet d'ordres
propriétaire, PAS un oracle décentralisé) ; le 65bps Chainlink et le 430bps Pyth sont les
déviations des ORACLES DÉCENTRALISÉS pendant le MÊME incident, sur Aave — bien plus proches du
peg, précisément PARCE QUE ces oracles agrègent plusieurs venues et ne dépendent pas de la
seule Binance. **C'est exactement la distinction oracle-agrégé vs source-CEX-unique pertinente
pour la calibration de τ (concordance INTER-ORACLES, pas prix CEX brut).**

**Verdict Q5/USDe** : pour un τ calibré sur la concordance INTER-SOURCES-ORACLE (pas sur un
carnet d'ordres CEX isolé), l'ancrage le plus directement pertinent de cet incident est le
couple **65bps (Chainlink, jugé sûr) / 430bps=4,3% (Pyth, plus large mais protocole non
défaillant)** — PAS le -35% Binance, qui est un événement de nature différente (source-CEX-
unique-défaillante, déjà cadrée par SONDE comme « k=1 visible »). Le -35% reste la mesure
utile pour illustrer l'AMPLEUR MAXIMALE possible d'une dislocation de source unique non
agrégée, à des fins de contexte, mais ne doit pas être confondu avec une magnitude d'ORACLE.

**Rappel non re-vérifié dans cette passe (déjà [lu] par SONDE, non re-testé)** : montants $ —
283 M$ compensés par Binance, 346 M$ de liquidations imputées à USDe. Le chiffre « ~328 M$ »
du brief de mission original (SONDE) reste NON CONFIRMÉ en primaire — statut inchangé.

### 5.3 KelpDAO / LayerZero (18 avril 2026) — CONFIRMÉ HORS PÉRIMÈTRE MAGNITUDE, PAS UN TROU

**Ré-examen du cadrage SONDE (§3.2)** : l'incident KelpDAO est une falsification de message
cross-chain via un DVN (Decentralized Verifier Network) configuré en « 1-of-1 », compromis par
ingénierie sociale — **aucun oracle de PRIX n'est impliqué dans le mécanisme de l'attaque**.
Aucun smart contract de prix n'a été exploité ; c'est une attestation de pont falsifiée.

**Décision méthodologique pour cette re-vérification (suivant l'avis advisor)** : je NE cherche
PAS un « depeg rsETH » pour cet incident — il n'y en a structurellement pas, car ce n'est pas un
événement de PRIX. Confirmé par relecture du cadrage SONDE lui-même : « Preuve de la douleur
(292 M$, l'exploit le plus coûteux de l'année), **pas** preuve du besoin d'un k_eff MESURÉ ».

**Verdict Q5/KelpDAO** : **AUCUN chiffre τ-pertinent applicable à cet incident** — ce n'est pas
un NON TROUVÉ (une recherche infructueuse), c'est une **exclusion motivée** : KelpDAO appartient
à une famille de risque différente (intégrité de message cross-chain / diversité de
vérificateurs de pont) que la famille visée par τ (concordance relative de PRIX inter-sources).
Consigné explicitement pour que l'orchestrateur ne le cherche pas non plus.

### Synthèse Q5 — tableau de calibration τ (magnitudes RÉELLES, re-vérifiées)

| Incident | Date | Magnitude relative | Niveau de preuve | Pertinence directe pour τ (concordance inter-oracles) |
|---|---|---|---|---|
| CAPO/Aave (wstETH) | 10 mars 2026 | **2,85% (rapporté) / 2,96% (recalculé des ratios — écart d'arrondi non résolu)** | [lu, non-verbatim] primaire (post-mortem Aave officiel) | OUI — mécanique de contrat autour de l'oracle, magnitude directement comparable à un τ candidat |
| USDe/Aave, oracles Chainlink+Pyth | 10 oct. 2025 | **65 bps (0,65%) Chainlink / 430 bps (4,3%) Pyth** | [lu-extrait] LlamaRisk (P2, daté, nommé) | OUI — DEUX oracles décentralisés, écart mesuré ENTRE eux et vs peg pendant un stress réel |
| USDe/Binance (carnet CEX interne) | 10 oct. 2025 | **35% (convergence CoinGecko + LlamaRisk, 7 sources presse corroborantes)** | [lu-extrait] × 2 sources nommées convergentes | Contexte seulement — PAS une déviation d'oracle agrégé, source CEX unique |
| KelpDAO/LayerZero (pont) | 18 avril 2026 | **N/A — pas un événement de prix** | N/A | EXCLU explicitement, pas un NON TROUVÉ |

### Journal des URL — Q5
- `firecrawl_search` "Aave CAPO incident March 2026 post-mortem wstETH desynchronized snapshot
  percentage" → succès, 8 résultats dont le post-mortem officiel Aave gouvernance et 5 sources
  de presse convergentes (spendnode.io, finance.yahoo.com, tradingview.com, rekt.news,
  rattibha.com/x.com).
- `WebFetch https://governance.aave.com/t/post-mortem-exchange-rate-misallignment-on-wsteth-
  core-and-prime-instances/24269` → succès, source primaire officielle du protocole.
- `firecrawl_search` "USDe price low October 10 2025 Binance crash $0.65 exact lowest price"
  → succès, 8 résultats, convergence forte (Galaxy, FTI Consulting, CoinDesk Data, Lexology,
  TradingView/Coinpedia, BitPinas, CoinGecko learn).
- `WebFetch https://www.coingecko.com/learn/october-10-crypto-crash-explained` → succès,
  verbatim « 35% below its $1 peg » confirmé, daté (mise à jour 6 février 2026).
- (Réutilisation, non re-fetchée) `llamarisk.com/research/when-pricing-breaks-usde` — déjà
  fetché deux fois en Q4, chiffres réutilisés ici tels quels avec la même discipline de niveau.
- Calcul Python local (vérification arithmétique des ratios CAPO, déclenché par la correction
  post-advisor) → succès, aucune nouvelle requête réseau nécessaire.

---

## Q6 — Citations canoniques de méthode (SPC/ARL ; EVT/POT ; FDR/Benjamini-Hochberg)

### (a) SPC — limites de contrôle pour un taux de fausse-alarme cible / ARL depuis une période
de calibration — [lu] intégral, primaire

**Source** : NIST/SEMATECH e-Handbook of Statistical Methods, section 6.3 (« Univariate and
Multivariate Control Charts »), pages `itl.nist.gov/div898/handbook/pmc/section3/pmc32.htm`
(« 6.3.2. What are Variables Control Charts? ») et `.../pmc321.htm` (« 6.3.2.1. Shewhart X-bar
and R and S Control Charts »). [lu-extrait, brut] via firecrawl_search, texte HTML retourné
intégralement (tableaux compris), PAS une synthèse IA. Organisme : NIST (agence fédérale
américaine de normalisation) + SEMATECH — référence manuel/survey canonique du domaine, pas un
article de recherche isolé.

**Limites de contrôle — formule et convention k=3, verbatim** :
> « UCL=μw+kσw, Center Line = μw, LCL=μw−kσw where k is the distance of the control limits
> from the center line, expressed in terms of standard deviation units. When k is set to 3,
> we speak of 3-sigma control charts. Historically, k=3 has become an accepted standard in
> industry. »

**ARL — définition et valeur numérique canonique, verbatim** :
> « For an X̄ chart, with no change in the process, we wait on the average 1/p points before
> a false alarm takes place, with p denoting the probability of an observation plotting
> outside the control limits. For a normal distribution, p=0.0027 and the ARL is
> approximately 371. »

Complément sur le compromis sensibilité/fausses-alarmes (règles WECO), même page, verbatim :
> « you will have "false alarms" every 371 points on the average [...] Adding the WECO rules
> increases the frequency of false alarms to about once in every 91.75 points, on the average
> (see Champ and Woodall, 1987). »

**Calibration depuis une période préliminaire** (paraphrase fidèle, formules lues) : σ est
estimé à partir de `m` échantillons préliminaires de taille `n`, en moyennant les écarts-types
individuels (`s̄`), corrigé par un facteur `c4` pour l'estimation non biaisée — méthode
directement transposable à un calibrage de τ sur une fenêtre de données passées.

**Applicabilité directe à Shōgen** : c'est EXACTEMENT la citation canonique demandée par la
mission — limites à k écarts-types (k=3 conventionnel) calibrées sur une période de référence,
avec un ARL/taux de fausse-alarme cible dérivé directement de k sous hypothèse de normalité
(ARL₀≈371 pour k=3, p=0,0027). **Réserve méthodologique que j'ajoute moi-même (pas une
affirmation NIST)** : cette relation ARL↔p suppose la NORMALITÉ de la statistique surveillée —
à vérifier avant transposition si la distribution empirique des écarts relatifs inter-sources
Shōgen s'avère à queue lourde (plausible pour des données crypto).

### (b) EVT/POT — citation identifiée, NON requise pour cette décision (critère de la mission
lui-même)

**Citation canonique** : Stuart Coles, *An Introduction to Statistical Modeling of Extreme
Values*, Springer Series in Statistics, Springer-Verlag/Springer London, 2001, 208 pages, DOI
10.1007/978-1-4471-3675-0. Identité bibliographique confirmée par recoupement de 3 sources
indépendantes : listing officiel Springer (`link.springer.com/book/10.1007/978-1-4471-3675-0`,
« Cited by 12931 » — confirme le statut de référence la plus citée du domaine), Google Books,
catalogue de bibliothèque universitaire (East Carolina University). [lu-extrait, brut] pour
l'identité bibliographique seulement — **livre NON lu** (voir ci-dessous, non requis).

**Accès** : ouvrage complet, PAS en accès libre (Springer = paywall confirmé ; Google Books =
aperçu seulement). Un lien Scribd est apparu dans les résultats de recherche — **délibérément
NON utilisé** comme source (plateforme de partage dont la légalité de la copie déposée n'est
pas garantie, non citable comme accès légitime).

**Verdict d'applicabilité, appliquant le critère posé par la mission elle-même** : « pertinent
SEULEMENT si extrapolation au-delà de ~P99,95 (ici N≈34 500, le quantile empirique est solide
jusque-là) ». Avec N≈34 500, le P99,95 correspond à environ les 17 valeurs les plus extrêmes de
l'échantillon (34 500 × 0,0005 ≈ 17,25) — masse empirique suffisante pour ne PAS nécessiter
d'extrapolation paramétrique EVT/POT si τ est fixé à un niveau ≤P99. **Citation identifiée et
vérifiée, lecture approfondie NON effectuée — exclusion motivée par le périmètre de la mission
elle-même, PAS une dette ni un blocage.** Aucun procurement formé pour ce livre : son usage
n'est pas requis par la décision actuelle ; à demander formellement seulement si une future
passe décide d'extrapoler au-delà de P99,95.

### (c) FDR (Benjamini-Hochberg) — [lu] intégral au niveau MANUEL, pertinence conditionnelle
explicitée

**Identité bibliographique de l'article fondateur**, triple-confirmée indépendamment (JSTOR,
Wiley/RSS, PMC — tous consultés en page d'index/abstract, pas le texte intégral) : Benjamini,
Y., & Hochberg, Y. (1995). « Controlling the False Discovery Rate: A Practical and Powerful
Approach to Multiple Testing. » *Journal of the Royal Statistical Society, Series B
(Methodological)*, 57(1), 289-300. DOI 10.1111/j.2517-6161.1995.tb02031.x. JSTOR stable ID
2346101. **Accès direct à l'article original : ÉCHOUÉ** (WebFetch sur
`rss.onlinelibrary.wiley.com/doi/10.1111/j.2517-6161.1995.tb02031.x` → HTTP 403 Forbidden).

**Contournement réussi — EXACTEMENT le niveau « manuel » demandé par la mission** : Bradley
Efron, *Large-Scale Inference: Empirical Bayes Methods for Estimation, Testing, and
Prediction*, Institute of Mathematical Statistics Monographs (Series Number 1), Cambridge
University Press, 2010 (réimpression 2012 confirmée par Google Books) — Chapitre 4, « False
Discovery Rate Control ». Copie hébergée en accès libre par l'Université de Toronto (cours
STA2212, `utstat.toronto.edu/reid/sta2212s/2021/EfronLSIChapter4.pdf`). **[lu] intégralement,
8 pages (pp. 41-48), via Read direct sur le PDF sauvegardé localement par WebFetch** (même
technique productive que celle documentée dans C1-attaques.md) — un vrai chapitre de manuel de
référence lu page par page, PAS un résumé d'outil.

**Règle BH — formule exacte, [lu] verbatim, p.43, éq. 4.9-4.10** :
> « The Benjamini–Hochberg (BH) algorithm uses this rule: for a fixed value of q in (0,1),
> let i_max be the largest index for which p_(i) ≤ (i/N)q, and reject H_0(i) [...] if
> i ≤ i_max, accepting H_0(i) otherwise. »

**Théorème de contrôle du FDR, [lu] verbatim, p.43, éq. 4.11** :
> « If the p-values corresponding to the correct null hypotheses are independent of each
> other, then the rule BH(q) [...] controls the expected false discovery proportion at q,
> E{Fdp_BH(q)} = π0 q ≤ q where π0 = N0/N. »

**Condition d'indépendance et sa relaxation, [lu] verbatim, p.45** :
> « Theorem 4.1 depends on independence among the p-values of the null cases [...] usually an
> unrealistic assumption. This limitation can be removed if the rejection boundary [...] is
> lowered [...] The independence condition in Theorem 4.1 can be weakened to positive
> regression dependence (PRD) »

**Calibration pratique de q, [lu] verbatim, p.45** :
> « How should q be chosen? The literature hasn't agreed upon a conventional choice, such as
> α = 0.05 for single-case testing, though q = 0.1 seems to be popular. »

**Applicabilité à Shōgen, appliquant le critère posé par la mission elle-même** (« pertinent
SEULEMENT si les drapeaux sont posés comme tests simultanés ») : le chapitre lu distingue
explicitement le FWER (contrôle horizontal, un test à la fois, classique) du FDR (contrôle
vertical, ENSEMBLE ORDONNÉ de p-valeurs comparées à une limite croissante `(i/N)q`). **Si τ est
appliqué comme un seuil FIXE, testé indépendamment source par source ou round par round (pas un
ensemble de p-valeurs ordonnées et comparées les unes aux autres dans le même lot), la procédure
BH n'est PAS le cadre statistique pertinent** — ce serait un test simple répété, pas un test
multiple simultané au sens de ce chapitre. Ma lecture confirme donc, depuis la source primaire,
exactement la conditionnalité que la mission avait déjà posée par hypothèse.

### Verdict Q6

Trois citations obtenues, niveau de preuve élevé pour deux des trois :
- **(a) SPC/ARL** : **[lu] intégral, primaire**, NIST/SEMATECH — directement transposable
  (k=3σ conventionnel, ARL₀≈371 pour p=0,0027 sous normalité, méthode de calibration de σ
  depuis une période préliminaire décrite en détail).
- **(b) EVT/POT** : identifiée (Coles 2001), **non lue** — exclusion MOTIVÉE par le critère
  d'applicabilité posé par la mission elle-même (N≈34 500 suffit jusqu'à P99,95), pas une
  dette. Procurement NON formé (pas nécessaire pour cette décision).
- **(c) FDR** : **[lu] intégral (8 pages)** au niveau manuel canonique (Efron 2010, Ch.4),
  formule exacte et conditions d'application confirmées depuis la source ; identité
  bibliographique de l'article fondateur original (Benjamini & Hochberg 1995) triple-vérifiée
  mais non lue directement (paywall, 403). Conditionnalité de pertinence (tests simultanés)
  CONFIRMÉE depuis la lecture, pas seulement supposée.

### Journal des URL — Q6
- `firecrawl_search` "NIST SEMATECH engineering statistics handbook control charts average run
  length false alarm rate", domaine itl.nist.gov → succès, 6 résultats, texte quasi intégral
  des pages pmc32.htm et pmc321.htm obtenu directement (verbatim ci-dessus).
- `firecrawl_search` "Benjamini Hochberg 1995 false discovery rate controlling procedure
  definition" → succès, 6 résultats (JSTOR, Wiley, Columbia Mailman, Springer, PMC, r-bloggers)
  — identité bibliographique triple-confirmée, définition partielle obtenue via sources
  secondaires ouvertes (PMC, Columbia).
- `firecrawl_search` "extreme value theory peaks over threshold POT method Coles introduction
  survey open access" → succès, 6 résultats, tous payants ou secondaires (ScienceDirect
  paywall, pyextremes doc technique, SAGE journals) — aucun accès primaire ouvert au canon
  (Coles 2001) trouvé, cohérent avec l'exclusion motivée ci-dessus.
- `firecrawl_search` "Coles An Introduction to Statistical Modeling of Extreme Values 2001
  Springer" → succès, identité bibliographique confirmée (Springer, Google Books, catalogue
  universitaire), aucun accès libre au texte intégral.
- `WebFetch https://rss.onlinelibrary.wiley.com/doi/10.1111/j.2517-6161.1995.tb02031.x` →
  **ÉCHEC : HTTP 403 Forbidden**.
- `firecrawl_search` "Benjamini Hochberg 1995 controlling false discovery rate pdf", catégorie
  pdf → succès, 6 résultats dont le chapitre Efron hébergé par l'Université de Toronto
  (trouvaille décisive).
- `WebFetch https://utstat.toronto.edu/reid/sta2212s/2021/EfronLSIChapter4.pdf` → échec de
  parsing direct (PDF binaire), sauvegardé localement → **relu avec succès via Read, pages
  1-8** → source [lu] intégrale du Chapitre 4.
- `firecrawl_search` "Efron Large-Scale Inference Empirical Bayes Methods Estimation Testing
  Prediction book year publisher" → succès, identité bibliographique du livre confirmée
  (Cambridge University Press, 2010/2012, IMS Monographs).

---

## Contradictions relevées (synthèse consolidée, toutes questions)

1. **CoinGecko — cadence de mise à jour, trois chiffres officiels non alignés** (Q3) :
   20s payant/60s démo (`docs.coingecko.com/reference/simple-price`) vs 30s payant/1-5min
   général (`support.coingecko.com` FAQ) vs 1-10min (`coingecko.com/en/faq`). Aucune des trois
   pages n'est datée explicitement ; aucune ne l'emporte sur les deux autres par primauté
   temporelle démontrable. Rapportées séparément, non fondues.
2. **DefiLlama — cadence NON périodique, découverte par correction post-advisor** (Q3) : un
   premier intervalle mesuré à exactement 300s a suggéré une périodicité fixe ; un second
   intervalle mesuré (après ajout d'un 3e échantillon) donne 1270s, PAS un multiple de 300s —
   la clé `coingecko:ethereum` de `coins.llama.fi` n'a PAS une cadence strictement périodique
   démontrée. Traité comme une correction de fond (pas une simple contradiction mineure) :
   voir Q3.
3. **CAPO/Aave — tension arithmétique entre ratios et déviation rapportée** (Q5.1) :
   (1,2282−1,1919)/1,2282 ≈ 2,96%, alors que le post-mortem rapporte séparément « 2,85% » de
   déviation effective — même source primaire, chiffres non exactement recoupés par le calcul
   direct. Écart d'arrondi/base de calcul non résolu, sans incidence d'ordre de grandeur.
4. **CAPO/Aave — ratio plafonné exact, écart mineur entre source officielle et un post X**
   (Q5.1) : post-mortem officiel Aave [lu] indique ≈1,1919 ; un post X/Twitter non ouvert en
   primaire ([2nd]) indique ≈1,1939. Écart de 0,002 point, non tranché, sans incidence sur les
   chiffres de déviation finale (2,85%/2,96%).
5. **Pyth — exemple doctrinal « confidence typiquement $50 pour BTC » vs mesure live du jour**
   (Q2) : la doc (non datée) donnerait ~0,1% relatif à $50 000 ; la mesure live de ce jour
   donne 0,028% à ~$78 300. PAS établi comme une contradiction stricte (la doc n'étant pas
   datée, on ne peut affirmer qu'elle décrivait le marché d'aujourd'hui) — signalé comme un
   écart non résolu, pas une contradiction ferme.
6. **[Rappel, déjà consigné par SONDE, non re-tranché dans cette passe]** Montants USDe/Binance
   en dollars : 346 M$ (liquidations imputées) / 283 M$ (compensation payée) / ~328 M$ (chiffre
   de brief non confirmé) — trois dénominateurs distincts, statut inchangé par cette passe (qui
   s'est concentrée sur les magnitudes RELATIVES, pas les montants absolus, pour Q5).

## NON TROUVÉ (synthèse consolidée)

1. Valeur STATIQUE documentée en toutes lettres du heartbeat ETH/USD et BTC/USD mainnet (ex.
   « 3600 secondes ») sur la table d'adresses `docs.chain.link/data-feeds/price-feeds/
   addresses` — page inaccessible (trop volumineuse pour WebFetch, non indexée assez finement
   par firecrawl_search pour cette requête précise). **Compensé** par une mesure empirique
   on-chain équivalente et plus forte (primaire, datée, reproductible) — voir Q1.
2. Définition officielle documentée du champ `confidence` (valeur observée : 0,99) de l'API
   `coins.llama.fi` de DefiLlama — recherché sur api-docs.defillama.com (racine + llms-free.txt)
   et par recherche GitHub ciblée, non trouvé. Voir Q3, procurement formé.
3. Référence exacte contre laquelle LlamaRisk calcule les déviations 65bps/430bps/3500bps de
   l'article USDe (peg $1 supposé mais non confirmé en toutes lettres dans les extraits
   obtenus). Voir Q4/Q5, procurement formé.
4. Texte intégral de l'article original Benjamini & Hochberg (1995) — paywall Wiley (403),
   JSTOR non tenté directement (payant, connu). **Compensé** par la lecture intégrale du
   traitement canonique niveau manuel (Efron 2010, Ch.4) — voir Q6(c). Pas un trou pour la
   mission (le niveau « manuel/survey » demandé est satisfait), signalé par transparence.
5. **[NOUVEAU]** Cadence de rafraîchissement EXACTE et fixe de `coins.llama.fi` (clé
   `coingecko:ethereum`) — trois échantillons montrent un premier intervalle de 300s et un
   second de 1270s (non multiple de 300), incompatibles avec une période fixe unique. La
   cadence réelle (probablement variable, de l'ordre de quelques minutes) n'est pas
   caractérisée précisément par cette passe — voir Q3. Pas de procurement formé (nécessiterait
   soit une documentation interne DefiLlama non publiée, soit une instrumentation prolongée
   hors périmètre budgétaire de cette mission).

## Demandes de procurement formées

**P1 — Définition du champ `confidence` de l'API coins DefiLlama.**
Identité : documentation officielle DefiLlama, `https://api-docs.defillama.com/` et
`https://api-docs.defillama.com/llms-free.txt`, potentiellement le code source du repo GitHub
`DefiLlama/defillama-server` (non localisé précisément dans cette passe).
Tentatives faites : WebFetch sur les deux URLs officielles (accès réussi, contenu ne définit
pas le champ) ; firecrawl_search ciblé sur api-docs.defillama.com (0 résultat) ; recherche
GitHub ciblée sur « confidence » + « defillama-server » (0 résultat direct).
Usage prévu : savoir si `confidence: 0.99` (valeur observée uniformément sur 3 clés testées)
est un signal de qualité de source variable (utile pour informer τ) ou une constante peu
significative.

**P2 — Texte intégral de « When Pricing Breaks: A USDe Case » (LlamaRisk, 18 octobre 2025).**
Identité : `https://llamarisk.com/research/when-pricing-breaks-usde`, article de recherche
LlamaRisk (P2, cabinet de risque DeFi indépendant).
Tentatives faites : 2× WebFetch avec prompts ciblés différents (tous deux réussis en accès,
mais chacun ne retourne qu'un extrait traité par le modèle d'extraction, pas la page complète).
Usage prévu : confirmer la référence exacte de mesure des déviations (peg $1 ou autre), et
vérifier s'il existe une section « recommandations » chiffrant un seuil pour l'avenir, au-delà
du dual-feed LlamaGuard déjà identifié par SONDE (pas un seuil numérique fixe).

**Note explicite — PAS un procurement formé** : le livre Coles (2001), *An Introduction to
Statistical Modeling of Extreme Values*, identifié en Q6(b), n'est PAS demandé en procurement
dans cette passe : son usage n'est pas requis par la décision τ actuelle (critère
d'applicabilité EVT/POT non atteint, N≈34 500 suffisant jusqu'à P99,95 — voir Q6(b)). À
demander formellement seulement si une passe future décide d'extrapoler au-delà de P99,95.

## Journal des URL — synthèse
Le détail complet (succès et échecs, avec URL exactes) est consigné en fin de chaque section
Q1 à Q6 ci-dessus, au fil de l'eau. Aucune requête ni tentative n'a été omise du journal.

---

## Rapport de synthèse pour l'orchestrateur (résumé final — ne remplace pas l'archive ci-dessus,
qui fait foi en détail)

1. **Gate 0** : `claude-sonnet-5`, conforme, déclaré en tête. Aucun commit effectué (R-20).
2. **Écart de référence signalé en premier** (doc 03 §1) : le contenu USDe/CAPO/KelpDAO demandé
   par la mission n'est PAS dans `C1-attaques.md` comme indiqué, mais dans `SONDE-artefact.md` ;
   aucun fichier « C1-bis » n'existe — le « cas fabriqué » désigne le piège #3 déjà documenté
   dans C1-attaques.md lui-même. Contenu réutilisé quand même (au bon endroit), rien n'est
   perdu, mais le brief source mérite une correction de référence pour la prochaine fois.
3. **Passe de correction post-advisor** (avant remise) : l'advisor a détecté une erreur de
   catégorisation dans la synthèse Q1 (deux vraies exceptions gap-court/delta-faible omises,
   trois rounds gap-long cités à tort comme si c'étaient des exceptions gap-court) — corrigée
   après re-vérification programmatique sur les données déjà collectées. L'advisor a aussi
   suggéré un 3e échantillon DefiLlama « pour confirmer un second intervalle » — ce
   3e échantillon a en fait **infirmé** la conclusion « cadence de 300s pile » de la première
   rédaction (le second intervalle mesuré, 1270s, n'est pas un multiple de 300s) ; traité comme
   une correction de fond et non comme un simple raffinement. Une tension arithmétique CAPO
   (2,85% rapporté vs 2,96% recalculé des ratios) a aussi été identifiée et signalée. Aucune de
   ces corrections ne change les verdicts principaux (0,5%/1h Chainlink confirmé ; CAPO reste
   ~2,85-2,96%) mais toutes ont amélioré la fidélité de l'archive aux données réellement
   collectées.
4. **Q1 (Chainlink)** : hypothèse « 0,5% / 1h » CONFIRMÉE par deux méthodes indépendantes —
   valeur statique data.chain.link (0,5%) ET mesure empirique on-chain de ce jour sur 120
   rounds au total (60 ETH/USD + 60 BTC/USD, méthode reproductible, RPC public), avec trois
   exceptions minoritaires honnêtement caractérisées après correction. Le champ « heartbeat »
   du site s'est révélé être un compte à rebours dynamique, pas une valeur statique — corrigé
   par la méthode on-chain, plus forte. Le P99 mesuré S2 (~0,53%) est mécaniquement expliqué :
   seuil documenté 0,5% + délai de congestion documenté pour le léger excédent.
5. **Q2 (Pyth)** : sémantique complète lue (σ/μ, recommandation « pause si σ/μ dépasse un
   seuil » — précédent conceptuel pour τ, pas une preuve directe transposable). Magnitude
   typique ETH/USD mesurée live ce jour : ~0,03-0,04% — un plancher de bruit bien en dessous
   des P99 inter-sources visés par τ.
6. **Q3 (DefiLlama/CoinGecko)** : méthodologies complètes lues (VWAP+MAD pour CoinGecko ;
   héritage CoinGecko + repli on-chain pour DefiLlama). Preuve empirique originale (requête
   live) : DefiLlama calcule au moins deux pipelines de prix distincts pour un même actif
   (écart 0,066% observé sur WETH), plausible explication partielle du P99 DefiLlama plus
   large que CoinGecko. **Cadence DefiLlama : NON établie comme fixe** après correction (300s
   puis 1270s sur deux intervalles mesurés — voir NON TROUVÉ n°5).
7. **Q4 (moniteurs de risque)** : constat négatif robuste — aucun seuil universel publié par
   Chaos Labs (3 posts + 1 page produit), LlamaRisk, ou Gauntlet. L'ancrage le plus concret et
   le mieux daté : LlamaRisk, 18 octobre 2025, qualifie 65bps (0,65%) de déviation Chainlink de
   « bien dans les paramètres de sécurité » pendant un stress réel — cohérent avec le 0,5%
   Chainlink et les 0,25-0,5% Chaos Labs Edge (convergence d'ordre de grandeur, pas de standard
   déclaré).
8. **Q5 (dislocations réelles)** : CAPO upgradé de [2nd] à **[lu, non-verbatim] primaire**
   (post-mortem officiel Aave, ~2,85-2,96% selon la méthode de calcul + mécanisme exact du
   rate-limiter). USDe précisé au-delà de SONDE : -35% pour le prix spot Binance (convergence
   CoinGecko + LlamaRisk + 7 sources presse) VS 65bps Chainlink/430bps Pyth pour les ORACLES
   DÉCENTRALISÉS pendant le même incident — distinction cruciale pour ne pas confondre un échec
   de source CEX unique avec une déviation d'oracle agrégé. KelpDAO confirmé structurellement
   hors périmètre (pas un événement de prix), exclusion motivée et non un trou.
9. **Q6 (citations canoniques)** : SPC/ARL lu intégralement en primaire (NIST/SEMATECH, k=3σ,
   ARL₀≈371). FDR lu intégralement au niveau manuel (Efron 2010 Ch.4, formule BH exacte,
   condition d'indépendance/tests simultanés confirmée depuis la source). EVT/POT identifié
   (Coles 2001) mais non lu, exclusion motivée par le critère d'applicabilité posé par la
   mission elle-même (non un trou).
10. **Cinq points en NON TROUVÉ, deux procurements formés, aucune dette nue** : chaque point
    non résolu est en NON TROUVÉ avec piste précise, en procurement formé, ou en exclusion
    explicitement motivée par un critère de la mission elle-même.
11. **Chiffres clés prêts pour l'ADR τ** (rappel condensé, tous re-sourcés ci-dessus) :
    Chainlink 0,5%/1h (mécanique, confirmé) ; Pyth ~0,03-0,04% (bruit interne, plancher) ;
    CoinGecko VWAP+MAD, cadence 20s-10min selon la page citée ; DefiLlama hérite CoinGecko +
    repli on-chain, cadence NON fixe (quelques minutes, non périodique) ; LlamaRisk
    65bps=sûr/430bps=notable (18 oct. 2025, daté) ; CAPO ~2,85-2,96% (10 mars 2026, primaire,
    tension d'arrondi signalée) ; USDe -35% source unique CEX (10 oct. 2025, double
    convergence) ; SPC k=3σ/ARL₀≈371 (NIST, transposable) ; FDR pertinent SEULEMENT si tests
    simultanés (confirmé par la source) ; EVT/POT non requis ici (N≈34 500 suffisant).
