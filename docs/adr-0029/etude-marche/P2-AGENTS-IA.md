# Étude de marché Shōgen — P2 : architecte d'agents IA financiers

> *Note de versement de l'orchestrateur* : citations de pages web non versées à `biblio/` passées de « … » à “…” (gate S-G5) ; lectures [lu] web du rapport, copies hors dépôt.

**Gate 0.** Modèle sous lequel je tourne : `claude-sonnet-5-5` (chercheur, effort high). Brief lu en entier, sha256 vérifié `f807cffb…e136`. Rien écrit hors de mon dossier ; aucun accès au dépôt hors lecture des pièces autorisées (docs 02, 04, 07, 10 §3-4, 11 §1-2, ADR-0028 avis produit, ADR-0029 §2.1, §2.5, §3) ; aucune pièce interdite ouverte ; aucune clé, compte ni achat.

**Niveaux.** [lu] = page ouverte et extraite par l'outil de lecture (résumeur automatique : chiffres recopiés du résumé, pas d'une lecture intégrale) ; [2nd] = vu seulement dans un résultat de recherche ou un agrégateur ; [calc] = calcul de ma part ; [inféré] = mon raisonnement. Date de lecture de toutes les sources : 2026-10-04. Une page bloquée ou un refus est un manque déclaré, jamais contourné.

## 1. Résumé

1. Les agents financiers obtiennent aujourd'hui leurs prix par cinq voies : plugins d'API à clé (CoinGecko, CMC, Birdeye, DexScreener), serveurs MCP des agrégateurs et des oracles, lecture d'oracles sur chaîne, appels payants x402, et agents-oracles (Virtuals ACP). Leur pile par défaut est faite d'agrégateurs, donc de sources dont l'amont est partagé.
2. Le risque central est celui que Shōgen mesure. Un papier de septembre 2026 nomme la « fausse corroboration » : plusieurs enregistrements issus d'un seul amont lus comme un consensus indépendant (arXiv 2609.02127). L'incident du 10 octobre 2025 (USDe à 0,65 $ sur un seul lieu, 283 M$ d'indemnisation) est le cas d'école d'une source unique.
3. Aucun produit trouvé ne mesure l'indépendance : le MCP communautaire qui croise Chainlink et Pyth déclare ne pas arbitrer ni mesurer l'indépendance. L'angle reste libre, sous réserve d'une recherche incomplète.
4. La demande payante des agents est, en 2026, quasi nulle et mal mesurée : sur x402, TRM Labs estime la part « plausiblement agentique » à 0,6-7,5 % du commerce filtré, soit 5 000 à 11 000 $/mois. Aucun modèle de revenu par appel ne tient en 2026.
5. Ce qui existe est de la distribution : MCP (~97 M de téléchargements de SDK par mois, mars 2026 [2nd]), x402 (fondation Linux Foundation), ERC-8004 (mainnet 29 janvier 2026, encore en brouillon). Les acheteurs réels sont les vendeurs de données et de plateformes d'agents, pas les agents.
6. Recommandation : ajouter ETH/USD, USDC/USD, USDT/USD avec les sources que les agents consomment réellement (CMC en agrégateur nouveau ; Chainlink sur Base et sur Ethereum ; un pool DEX sur Base ; Hyperliquid déclaré dérivé de ses amonts), et un axe « devise de cotation » en R2.
7. Livrer d'abord une attestation JSON signée, un vérificateur hors-ligne et un serveur MCP en lecture seule, gratuits. L'attestation qualifie les sources que l'agent désigne ; elle ne décide rien et ne dit jamais « prix juste ».
8. Se placer dans les standards ouverts qui manquent d'une preuve de contenu : x402 `response-provenance` (issue ouverte le 23 août 2026, sans réponse), ERC-8004 Validation Registry.
9. Coût marginal faible (quelques dizaines de dollars par mois d'API, hébergement déjà budgété par ADR-0029 §3) ; le coût réel est le temps de S2-bis et le risque de licence sur la republication des octets des agrégateurs.
10. Incertitude principale : R1 n'a pas tranché en S2 ; ce qui est vendable aujourd'hui est R2 (concentration d'infrastructure), pas un « certificat de diversité » complet.

## 2. Constats sourcés

### 2.1 Comment les agents obtiennent leurs prix

| voie | fait | niveau, source |
|---|---|---|
| Plugins d'API à clé | ElizaOS : `plugin-coingecko` (action GET_PRICE), `plugin-coinmarketcap`, plugins Birdeye et DexScreener | [2nd] recherche ; dépôts github.com/elizaos-plugins/plugin-coingecko et plugin-coinmarketcap |
| | solana-agent-kit : « Pyth Price feeds » et « CoinGecko Pro API » ; AgentKit de Coinbase : Pyth et DefiLlama parmi les fournisseurs d'actions | [lu] github.com/sendaifun/solana-agent-kit ; github.com/coinbase/agentkit |
| MCP des agrégateurs | CoinGecko : serveur MCP sans clé (`mcp.api.coingecko.com/mcp`, « shared rate limits ») et serveur à clé ; CMC : MCP et point d'accès x402 ; Crypto.com : MCP de données de marché | [lu] docs.coingecko.com/ai-integration/mcp-server ; [2nd] coinmarketcap.com/api ; [2nd] news.bitcoin.com (mars 2026) |
| MCP des oracles | Pyth Pro pour agents (31 mars 2026) : « 3 000+ flux », 4 outils dont 3 gratuits (historique, bougies, recherche de symboles), prix temps réel avec jeton Pyth Pro | [lu] pyth.network/blog/pyth-pro-for-ai-agents-institutional-market-data-for-autonomous-finance |
| | Chainlink for Agents (bêta) : Data Streams à la demande, « pay-per-call in USDC on Base. No accounts, API keys, or subscriptions » ; approche « Skill.md » | [lu] chain.link/agents |
| | Serveurs MCP communautaires Chainlink + Pyth, 7 outils, drapeau `stale` par défaut au-delà de 1 h ; ne réconcilie pas : « oracle-reported prices as-is » ; indépendance non traitée | [lu] glama.ai/mcp/servers/rileybuilds/oracle-feeds-mcp |
| Appel payant x402 | Nansen 0,01 à 0,05 $ par appel ; Messari 0,10 à 1,00 $ pour des séries ; prix médian par appel sur 19 338 points d'accès chiffrés : 0,02 $ (instantané du 10 juillet 2026) | [2nd] docs.nansen.ai, docs.messari.io ; [2nd] theaicareerlab.com/blog/x402-pricing-report-2026 |
| Agent à agent | Virtuals ACP : un agent de trading demande des prix à un « data oracle agent », puis un agent évaluateur confirme l'exécution | [2nd] whitepaper.virtuals.io (via recherche) |

Lecture [inféré] : la pile par défaut d'un agent est CoinGecko ou CMC, plus DefiLlama, plus un oracle sur chaîne. Or S2 a mesuré que `coins.llama.fi` n'est pas un chemin d'amont distinct de CoinGecko (ρ_résid 0,78, `basis:doc` ; docs/11 §1 et avis produit), et que 7 hôtes sur 10 passent par Cloudflare (k_eff = 4 sur 10). Les agents empilent donc des lumières qui ont probablement peu de racines.

Une étude empirique de 2026 observe que, pour les agents d'investissement, “many projects do not yet provide clear evidence of autonomous trade execution” et que la plupart des déploiements visibles restent de « basic API integrations » (arXiv 2605.29174) [lu, résumé]. Le marché des agents réellement autonomes est donc plus petit que le récit.

### 2.2 Risques propres aux agents

- **Source unique, cas d'école.** Le 10 octobre 2025, entre 21:36 et 22:16 UTC, USDe est tombé sous 0,66 $ sur Binance ; Binance a versé 283 M$ en deux lots à des utilisateurs de contrats, de marge et de prêt ; l'écart était « isolated to a single venue » pendant que Curve, Fluid et Uniswap restaient à 0,3 % près. Le fondateur d'Ethena l'attribue à l'indice que Binance tirait de son propre carnet [lu] theblock.co/post/374295 ; [lu] cointelegraph.com/news/usde-depeg-oracle-issues-ethena-founder. La cause exacte reste discutée (attaque coordonnée alléguée, non établie).
- **Amont commun, même au niveau d'un lieu dérivé.** Le prix de marque de Hyperliquid est la médiane de trois entrées, dont les prix médians de perpétuels de « Binance, OKX, Bybit, Gate IO, MEXC avec les poids 3, 2, 2, 1, 1 » ; l'oracle est une médiane pondérée de prix de places centralisées [lu] hyperliquid.gitbook.io, « robust price indices ». Un agent qui croit croiser Hyperliquid et Binance en croise partiellement un seul.
- **Données externes comme surface d'attaque.** Princeton et Sentient définissent la « context manipulation » : canaux d'entrée, mémoire et flux de données externes ; avec CrAIBench (150+ tâches, 500+ cas d'attaque) sur ElizaOS, les modèles sont nettement plus vulnérables à l'injection de mémoire qu'à l'injection de prompt [lu] arxiv.org/abs/2503.16248. Un papier d'août 2026 conclut qu'aucune architecture multi-agents de trading n'est « inherently robust » face à des signaux adverses dans les données sources [lu] arxiv.org/abs/2608.24069. OWASP classe « Memory & Context Poisoning » (ASI06) et « Agentic Supply Chain » (ASI04) dans son Top 10 agentique de décembre 2025 [2nd].
- **Fausse corroboration.** « When multiple retrieved summaries or records derived from a single upstream source are treated as independent consensus » : arXiv 2609.02127 (2 septembre 2026) propose des graphes de provenance typés ; c'est le même objet que Shōgen, vu côté mémoire d'agent [lu, résumé ; la citation exacte vient d'un résultat de recherche, [2nd]].
- **Absence de preuve de contenu.** x402 prouve qu'un paiement a réglé, pas ce qui a été livré : « a paid calculator/data API can return any body and the receipt still verifies ». Une proposition `response-provenance` (hachage RFC 8785 de la réponse dans le reçu signé) a été ouverte le 23 août 2026, sans réponse des mainteneurs à ma lecture [lu] github.com/x402-foundation/x402/issues/3234. Trois autres issues voisines (#2833 delivery-receipt, #1802 facilitator-attestation, #3389 stark-receipt) montrent que le besoin est reconnu et qu'aucun profil n'est adopté [2nd, titres de recherche]. L'auteur de #3234 note lui-même que le hachage prouve la ré-dérivation, “not that the answer is correct” : même ligne que la phrase fondatrice de Shōgen.
- **Incidents d'oracle en 2026.** Quantstamp compte 37 incidents d'oracle ou de manipulation de prix en 2026 contre 17 en 2025 et 135,87 M$ (53 %) des pertes d'août 2026 [2nd] nhimg.org (relais du rapport Quantstamp ; rapport non lu). Ostium (15 juillet 2026, 18 M$) vient d'un rôle privilégié qui soumet des prix à horodatage futur : ce n'est pas un défaut d'indépendance des sources, je ne le compte pas comme preuve du besoin [lu] coindesk.com. **Exclu :** le récit d'une « exploitation de 45 M$ d'agents IA par empoisonnement d'oracle » (bex.co, 12 avril 2026) : aucune source primaire, aucune transaction citée ; je n'en tire aucun chiffre.

### 2.3 Ce dont un agent a besoin d'un produit comme Shōgen [inféré, appuyé par 2.1-2.2]

- **Lisible par machine** : objet JSON typé, pas un PDF ; champs `k_nominal`, `k_eff`, partition nommée, rang de chaque énoncé (R1/R2/R3), liste des axes non mesurés, `as_of`, `valid_until`, version de méthode, empreinte des journaux. Les agents savent déjà lire des `stale: bool` (serveur Chainlink/Pyth ci-dessus) ; il leur faut le même format pour l'indépendance.
- **Vérifiable hors-ligne** : signature sur clé épinglée plus recalcul depuis le lot ; sans quoi l'attestation est un score de plus à croire (A(self-attestation), doc 08).
- **Latence** : l'indépendance varie lentement (R2 par jour, R1 sur fenêtres). Un score précalculé, mis en cache et servi en moins de 200 ms (cible [inféré]) suffit ; il n'a pas à être dans le chemin chaud d'un ordre. Les oracles à faible latence se vendent à la milliseconde (Pyth Pro « up to 1ms », 2 500 $/mois et plus ; Starter 500 $/mois, « up to 1 second », crypto seule [lu] app.pyth.com/plans) ; ce n'est pas la dimension de Shōgen.
- **Prix par appel** : repères de marché ci-dessus : 0,01 à 0,05 $ (Nansen), 0,02 $ médian, 0,10 à 1,00 $ (Messari séries). CoinGecko Analyst : 129 $ pour 500 000 crédits, soit 0,00026 $ le crédit [lu] coingecko.com/en/api/pricing ; [calc]. Un score d'indépendance qui change peu devrait coûter zéro ou une fraction de millime ; au-dessus de 0,01 $ il est hors norme pour une donnée de contrôle.
- **Intégration** : MCP (lecture seule), JSON statique à adresse stable, et à terme point d'accès x402 gratuit ou quasi gratuit et enregistrement de validation ERC-8004 (voir R4).

### 2.4 Taille et croissance : ce qui est mesuré, ce qui ne l'est pas

| indicateur | valeur | niveau, source |
|---|---|---|
| x402, règlements cumulés depuis mai 2025 | 52,7 M$ sur 198,9 M de transactions (Base, Solana, Polygon) | [lu] trmlabs.com/trm-tech-blog/whos-actually-paying-measuring-ai-agent-payments-onchain (9 sept. 2026) |
| x402, commerce plausiblement authentique après filtres | 25,62 M$ | idem |
| x402, part « plausiblement agentique » | 0,6 à 7,5 %, soit 154 000 à 1,92 M$ au total, 5 000 à 11 000 $/mois en rythme 2026 | idem ; TRM précise qu'un script et un agent laissent le même enregistrement |
| x402, USDC | 99,6 % de la valeur réglée | idem |
| x402, activité artificielle | environ la moitié des transactions (auto-paiement, aller-retour de fonds) ; ~28 000 $/jour et ~131 000 transactions/jour, paiement moyen 0,20 $ | [lu] coindesk.com (11 mars 2026, analyse Artemis) |
| Compteur x402.org (« 30 derniers jours » : 75,41 M transactions, 24,24 M$) | figé depuis mars selon un relevé indépendant ; aucune méthodologie sur la page | [lu] x402.org ; [2nd] danielmcglynn.com |
| MCP | ~97 M de téléchargements mensuels de SDK ; plus de 10 000 serveurs actifs (mars 2026) ; 110 M cités plus tard | [2nd] news.bitcoin.com ; digitalapplied.com |
| ERC-8004 | mainnet le 29 janvier 2026 ; 45 000+ agents enregistrés [2nd] ; mais seulement 3 %, 4 %, 15 % (Ethereum, BSC, Base) exposent un fichier d'enregistrement valide, et 73,5 %, 59,2 %, 90,6 % des évaluateurs relèvent d'un comportement Sybil coordonné | [lu] arxiv.org/abs/2606.26028 ; EIP toujours « Draft » [lu] eips.ethereum.org/EIPS/eip-8004 |
| Capitalisation « agents IA » | 15 à 22,6 Md$ selon la source, Virtuals ~5 Md$ ; mesure spéculative, ne dit rien de la demande de données | [2nd] altrady.com ; bex.co |
| Prévisions de commerce agentique | 3 à 5 000 Md$ mondiaux en 2030 (McKinsey), 15 000 Md$ d'achats B2B intermédiés en 2028 (Gartner) | [2nd] ; portent sur le commerce de détail et B2B, pas sur les données de prix ; je ne les utilise pas pour dimensionner Shōgen |

Conclusion honnête : **je ne produis pas de taille de marché pour un score d'indépendance destiné aux agents.** Les seules séries chiffrées de cet écosystème sont gonflées, figées ou spéculatives ; la part agentique réelle des paiements est de l'ordre de dizaines de milliers de dollars par an à un million. Un revenu par appel n'a pas de base en 2026 [calc/inféré]. La valeur actuelle est la légitimité et la distribution, pas le chiffre d'affaires.

### 2.5 Quelles paires et quels actifs les agents consomment

**Je n'ai trouvé aucune mesure publique de la distribution des paires demandées par les agents** ; c'est un manque déclaré (ni CoinGecko, ni CMC, ni Pyth ne publient d'usage par actif pour leurs serveurs MCP). Ce que l'on peut établir :

- L'argent des agents est en USDC : 99,6 % des règlements x402 [lu TRM] ; les portefeuilles agentiques de Coinbase gèrent USDC, ETH, POL, SOL et échangent des jetons sur Base ou Polygon [lu] github.com/coinbase/agentic-wallet-skills. Donc USDC/USD, ETH/USD et les paires de gaz sont le risque de trésorerie d'un agent [inféré].
- Les agents de trading cités par les plateformes opèrent sur BTC, ETH, SOL et une longue traîne (Hyperliquid : 229+ marchés perpétuels) [2nd] recherche ; aucun pourcentage fiable (le chiffre de volume par actif que j'ai vu est un instantané de 24 h ambigu, écarté).
- La longue traîne des jetons (Birdeye, DexScreener) n'a souvent qu'un pool DEX comme source : l'indépendance y est mal définie, pas mesurable avec 10 sources [inféré]. À écarter du périmètre.
- Les paramètres de mise à jour des oracles pèsent sur un agent. Chainlink sur Base : ETH/USD battement 1 200 s, seuil 0,15 % ; BTC/USD 1 200 s, 0,1 % ; USDC/USD et USDT/USD 86 400 s, 0,3 %. Sur Ethereum : ETH/USD 3 600 s, 0,5 % ; USDC/USD et USDT/USD 86 400 s, 0,25 % [lu] reference-data-directory.vercel.app (copies dans `web/`). Un flux stable peut donc rester 24 h sans mise à jour tant qu'il ne dévie pas de 0,25-0,3 % : un agent qui lit USDC/USD chez Chainlink ne voit pas un écart plus fin.
- Cotations en USDT : « BTC-USDT ≠ BTC-USD. Stablecoin de-pegs happen » [lu] qveris.ai (guide de fournisseur, avis commercial). Et selon docs/10 §4.3, CoinGecko calcule son prix par VWAP de tickers BTC/USD, BTC/USDT, BTC/USDC et BTC/EUR : un dépeg de stablecoin peut donc traverser un agrégateur [lu, dépôt]. C'est un axe commun de défaillance que S2 n'a pas modélisé (S2 marquait déjà la devise par flux : 9 USD, 2 USDT).

## 3. Recommandations

### R1. Ajouter ETH/USD, USDC/USD, USDT/USD à S2-bis avec les sources des agents (priorité 1)

- **Quoi.** Pour ETH/USD : mêmes 10 hôtes que BTC/USD, plus (a) CoinMarketCap en agrégateur (c'est le deuxième défaut des agents, avec MCP et x402) ; (b) Chainlink lu sur Base et sur Ethereum, deux déploiements du même flux nominal, avec battements différents (1 200 s contre 3 600 s) ; (c) un pool DEX ETH/USDC sur Base, lieu d'exécution des agents Coinbase [inféré, à vérifier] ; (d) Hyperliquid, déclaré lieu dérivé avec ses parents nommés (Binance, OKX, Bybit, Gate, MEXC) en R2. Pour USDC/USD et USDT/USD : mêmes places où la paire existe, Chainlink, agrégateurs, et un pool de stables sur Ethereum et sur Base. Les trois types d'élargissement demandés par l'investisseur sont couverts : oracles (Chainlink ×2), agrégateurs (CMC), places (pool DEX, Hyperliquid).
- **Pourquoi.** C'est ce que consomment les agents (2.1, 2.5) ; c'est l'endroit où l'amont commun est le plus plausible (agrégateurs, lieux dérivés) ; et c'est ce qui permet de tester si l'axe R2 « concentration » est stable d'un actif à l'autre (S2 n'a qu'une classe).
- **Comment.** Collecte S2-bis (4 observateurs déjà prévus, ADR-0029 §2.1) ; une classe de faits par paire ; pour les stables, τ et σ propres (un prix à ±0,1 % n'a pas la dynamique d'un BTC) à sceller avant la campagne ; les arêtes `basis:doc` (CoinGecko ← tickers USDT/USDC, Hyperliquid ← CEX) saisies au paquet. Pyth reste dehors : mon essai public sans clé du 2026-10-04 à 04:56Z rend HTTP 401 `unauthorized` [lu, `web/pyth-hermes.txt`], ce qui confirme ADR-0029 §2.5 ; refus non contourné.
- **Apporte.** Une mesure R2 comparée sur 4 classes (BTC, ETH, USDC, USDT) plutôt qu'une ; un cas parlant pour les agents (l'écart de panier entre un agent « CoinGecko + DefiLlama + Chainlink » et un agent « 3 places + Chainlink »).
- **Coûte.** Ordre de grandeur [calc/inféré] : trois classes de plus multiplient les flux par ~3 ; la collecte S2-bis (165 à 605 € pour toute la campagne, ADR-0029 §3) reste dominée par l'hébergement. Côté API : CoinGecko Demo = 10 000 crédits/mois, alors qu'une lecture par minute en consomme 43 200 [calc] ; il faut grouper les identifiants dans un appel ou prendre Basic (35 $/mois, 100 000 crédits) [lu pricing]. CMC : prix et accès sans clé non lus (manque). Clé Pyth écartée (500 $/mois, pas de droits de redistribution).
- **Risques.** (i) Licences : republier les octets bruts d'un agrégateur peut être interdit (même mécanisme que « No redistribution rights » chez Pyth) ; publier des empreintes et des valeurs dérivées si besoin ; (ii) un RPC public (comme `publicnode`) est un chemin de lecture, pas l'amont de Chainlink ; le caveat existe déjà au rendu ; (iii) trop de classes diluent la puissance de R1 : commencer par ETH/USD et USDC/USD complets, USDT/USD ensuite.

### R2. Ajouter l'axe « devise de cotation » à R2

- **Quoi.** Pour chaque source, publier la devise de cotation observée (USD, USDT, USDC) et la déclarer partageant le risque de dépeg de cette devise ; deux sources cotées en USDT partagent une racine « USDT ».
- **Pourquoi.** Cas d'école 10 octobre 2025 et dépeg USDC de mars 2023 [2nd, non relu en primaire] ; invisible dans les axes actuels (hébergeur, amont déclaré).
- **Comment.** Champ déclaratif au rang R3 d'abord, puis observable (comparer le prix de la paire USDT et USD sur la même place) ; aucune surclamation.
- **Apporte.** Un énoncé que les agents comprennent tout de suite : « votre panier a 4 sources, mais 3 dépendent de la tenue de l'USDT ». **Coûte** : un champ et des tests. **Risque** : traiter comme une mesure ce qui reste déclaré.

### R3. Livrer d'abord l'attestation signée, le vérificateur et un MCP en lecture seule, gratuits

- **Quoi.** (a) Format `attestation-diversite` : JSON canonique (RFC 8785) avec les champs de 2.3, signé sur clé épinglée, ancré (RFC 3161 prévu par ADR-0028) ; (b) vérificateur hors-ligne ; (c) serveur MCP à trois outils : `get_independence(pool)`, `verify_attestation(blob)`, `list_pools()` ; il sert la dernière attestation publiée, il ne calcule rien en direct. L'agent désigne ses sources, Shōgen les qualifie, conformément à « ne choisit pas les sources d'un client » (doc 02).
- **Pourquoi.** C'est le seul format qui entre dans les piles existantes (MCP, JSON) et qui reste conforme aux non-buts : aucun composant en chemin de décision, aucun jugement de vérité.
- **Apporte.** Un point d'entrée que tout intégrateur essaie en une minute ; un livrable de crédibilité pour la position institutionnelle.
- **Coûte.** Faible (développement léger [inféré]) ; l'hébergement statique suffit. **Risque.** Les agents liront « k_eff élevé » comme « prix correct » : écrire dans le schéma un champ `non_claims` obligatoire (le vocabulaire interdit de doc 09 est repris tel quel).

### R4. Se positionner dans les standards ouverts qui manquent de preuve de contenu

- **Quoi.** (a) Commenter x402 #3234 et #2833 avec le format de témoignage de Shōgen comme profil candidat de la preuve de livraison (hachage de la réponse, source, instant) ; (b) étudier une réponse de validation ERC-8004 (`validationResponse` : 0 à 100 plus une étiquette) qui publie l'attestation d'un pool ; (c) inscrire le serveur MCP aux registres (Glama, registre officiel).
- **Pourquoi.** Les mainteneurs x402 n'ont pas répondu à #3234 ; l'ERC-8004 nomme pour les validateurs « stake-secured inference re-execution, zkML verifiers or TEE oracles » et accepte « any address » comme validateur [lu EIP] : une attestation de provenance de données n'y est pas encore traitée [inféré]. Aucune de ces voies ne rapporte de revenu en 2026 ; elles rapportent une place dans le standard.
- **Coûte.** Du temps de rédaction. **Risques.** Le registre ERC-8004 est dégradé (Sybil, fichiers vides) et l'EIP est en brouillon ; ne pas lier la réputation de Shōgen à ce registre ; attendre une réponse des mainteneurs x402 avant d'investir.

### R5. Publier un cas « pile par défaut d'un agent » dans le benchmark gratuit

- **Quoi.** Une note recalculable : « le panier par défaut de ElizaOS (CoinGecko, CMC), AgentKit (Pyth, DefiLlama) et solana-agent-kit (Pyth, CoinGecko Pro) : combien de racines ? », avec les arêtes déclarées et mesurées ; préavis privé aux projets concernés selon doc 07 §6.
- **Pourquoi.** C'est ce que l'architecte d'agents lit ; la neutralité du tiers est l'atout (doc 07 §4). **Coûte.** Faible si R1 est exécuté. **Risque.** Dire plus que ce qui est mesuré : n'écrire que R2 constaté et les arêtes `basis:doc`, jamais « risque pour l'agent » ; ne pas publier avant la clôture de S2-bis pour les noms.

### R6. Ne pas bâtir de revenu « agents » en 2026

Un revenu au passage d'appel de l'agent n'a pas de base chiffrée (2.4) ; l'acheteur plausible est une plateforme ou un vendeur de données (Coinbase CDP, Virtuals, ElizaOS, Pyth, Chainlink for Agents, CMC, CoinGecko), conflité pour certains (même logique que doc 07 §2) et à approcher après publication. C'est cohérent avec « position institutionnelle d'abord, revenu ensuite ».

## 4. Ce qui reste incertain

- Aucune mesure publique des paires les plus demandées par les agents ; mon tableau 2.5 est indirect.
- Les chiffres x402 sont contestés (mesure de l'activité artificielle, compteur figé) ; la part agentique de TRM dépend de ses filtres, que je n'ai pas audités.
- Rapport Quantstamp (août 2026), OWASP ASI, Virtuals ACP et les chiffres MCP vus en [2nd] seulement ; lectures primaires à refaire avant toute citation publique.
- Je n'ai pas lu la documentation Coinbase du « trade » (jetons pris en charge, source de prix ; page non détaillée par l'outil) : la source de liquidité des agents sur Base (R1 point c) est une inférence.
- Accès, prix et conditions de redistribution de CMC sans clé : non lus.
- RedStone, Chronicle, API3 (doc 07, 2026-07-30) : non revérifiés ici ; non proposés.
- R1 n'a pas tranché en S2 (docs/11 §1) ; tout ce qui précède suppose que S2-bis produit une mesure exploitable ; sinon le produit reste R2.
- Cette étude ne dit rien de la fidélité d'un prix, ni de l'efficacité d'un score d'indépendance à prévenir une perte : aucun incident documenté que j'aie lu n'a été attribué à une corrélation de sources mesurable, hors le cas Binance (source unique).

## 5. Trois questions à l'investisseur

1. Acceptez-vous de publier un cas nominatif sur les piles par défaut des plateformes d'agents (ElizaOS, AgentKit, solana-agent-kit), avec préavis privé, ou préférez-vous des cas anonymisés pour ne pas fâcher les futurs partenaires de distribution ?
2. Si CMC, CoinGecko ou d'autres agrégateurs interdisent la republication des octets bruts, préférez-vous publier des empreintes et des valeurs dérivées (recalcul moins complet) ou retirer ces sources du pool ?
3. Quelle part du temps de S2-bis consacrez-vous à l'intégration agents (format signé, MCP, commentaires de standards), sachant que la demande payante des agents est à peu près nulle en 2026 : une semaine pour le MCP et l'attestation, ou rien avant le premier recalcul externe (critère D9 (ii) d'ADR-0028) ?

## 6. Sources (lues le 2026-10-04 ; niveaux en §2)

TRM Labs x402 (9 sept. 2026) trmlabs.com/trm-tech-blog/whos-actually-paying-measuring-ai-agent-payments-onchain · CoinDesk x402 (11 mars 2026) coindesk.com/markets/2026/03/11/coinbase-backed-ai-payments-protocol-wants-to-fix-micropayment-but-demand-is-just-not-there-yet · x402.org · github.com/x402-foundation/x402/issues/3234 · eips.ethereum.org/EIPS/eip-8004 · arxiv.org/abs/2606.26028, 2503.16248, 2608.24069, 2609.02127, 2605.29174 · theblock.co/post/374295 · cointelegraph.com/news/usde-depeg-oracle-issues-ethena-founder · hyperliquid.gitbook.io/hyperliquid-docs/trading/robust-price-indices · pyth.network/blog/pyth-pro-for-ai-agents-institutional-market-data-for-autonomous-finance · app.pyth.com/plans · chain.link/agents · reference-data-directory.vercel.app (copies dans `web/`) · docs.coingecko.com/ai-integration/mcp-server · coingecko.com/en/api/pricing · github.com/coinbase/agentkit, coinbase/agentic-wallet-skills, sendaifun/solana-agent-kit · glama.ai/mcp/servers/rileybuilds/oracle-feeds-mcp · coindesk.com/business/2026/07/15/ostium-suffers-usd18-million-exploit-as-oracle-attack-wave-continues-to-hit-defi. Vus en [2nd] seulement : nhimg.org (Quantstamp), danielmcglynn.com (compteur x402), news.bitcoin.com (MCP), theaicareerlab.com (prix x402), docs.nansen.ai, docs.messari.io, OWASP ASI. Écarté, sans source primaire : bex.co/blog/2026/04/12/ai-trading-agent-45m-exploit-defi-security-breach.
