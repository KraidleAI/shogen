# G0 du lot CALIB-ACTIFS (ETH/USD, USDC/USD, USDT/USD : paires servies, historiques, τ, planchers, σ)

Adjugé par l'orchestrateur le 2026-10-08 22:13:03 UTC (heure produite par le script). Rattachement : ADR-0029 révision 3, acceptée (§2.5 l.173-174 ;
§2.7 l.186-191 ; l.212 ; l.214 ; l.310 ; question 10 l.416) ; G0 de collecte (`docs/adr-0029/g0-collecte/`) ;
`docs/adr-0029/calib/SOURCES-HISTORIQUES.md`. Pièces, dans ce dossier : relevé du lecteur (`PAIRES-ET-TEMOIN.md`,
`claude-sonnet-5-5`, sha256 `75535ad5…`) ; proposition du rédacteur (`PROPOSITION.md`, worker `claude-opus-5-5`, sha256 `4514370f…`,
quinze questions techniques Q-CA-01 à Q-CA-15, deux questions à l'investisseur INV-1 et INV-2) ; avis de l'advisor (`AVIS.md`,
`claude-fable-5-1` effort medium, sha256 `6deaf8cd…` : treize questions adoptées, deux modifiées, quatre ajouts datés [G0]) ; briefs.
Contrôle FM-1.1 des trois transcripts : 0 fragment ; modèles résolus conformes au roster.
Seule retouche d'une pièce versée : `PAIRES-ET-TEMOIN.md` l.120, le message d'erreur renvoyé par un hôte RPC est mis en code au
lieu de guillemets (ce n'est pas une citation bibliographique ; S-G5 lit les guillemets comme telle).

## Adjudications
1. **La proposition est le contenu de ce G0, corrigée par l'avis** : pour Q-CA-01 à Q-CA-15, la recommandation de l'avis
   s'applique telle qu'écrite (AVIS §1), y compris ses deux modifications (Q-CA-11 : relevé de cadence des agrégateurs par un
   script séparé d'environ 40 lignes, hors du lanceur épinglé du lot, lancé une fois avant le sceau, sans prix écrit ; Q-CA-15 :
   champ de mode explicite `calibre` ou `planchers_seuls` par actif dans le fragment, et contrôle de cohérence dans E-CA-23 (b))
   et ses précisions (Q-CA-02 : smoke de chaque observateur sur `api.binance.com` avant le gel, jamais de retrait de l'unité ;
   Q-CA-04 : part des cellules de la queue et âge médian imprimés par place ; Q-CA-06 : drapeau descriptif si
   τ_agr < τ_places ; Q-CA-07 : condition dure, le sens de l'horodatage de Bitstamp et de Gemini est établi à CB-7 par deux
   captures avant l'épinglage ; Q-CA-13 : deux vecteurs ajoutés, borne basse exacte et 1/3 %).
2. **Ajouts datés [G0]** : portés le même jour à l'ADR-0029 (après l'ajout du G0 de PLAN-S2BIS-2) : USDC/USD à cinq places,
   Gemini sans historique, OKX sans `ETH-USD` ni `USDC-USD` ; lettre de l.189 (dénominateur ; troisième terme) ; sensibilité
   « USD seules » étendue à ETH (l.212) ; taille du lot (l.310).
3. **Condition des historiques** (l.186, l.191) : remplie classe par classe en lecture « existence » (ETH 6, USDC 4, USDT 6 ;
   SOURCES-HISTORIQUES §1) : constat technique ; le sceau à S+10/11 ne bouge pas de ce chef. L'**usage** de ces fichiers par
   un produit vendu revient à l'investisseur (INV-1, INV-2 de la proposition, §9), posé **avec** sa conséquence sur le pool en
   direct (AVIS §4.4 ; question 13). L'option B d'INV-1 n'est pas exécutable telle qu'écrite (AVIS §4.3) : c'est dit à
   l'investisseur en ces termes. Avis technique retenu : option A.
4. **Lecture préalable de Coinbase et de Bitfinex** (AVIS §4.2 (1)) : faite le 2026-10-08 par la passe « licences et
   abonnements » de l'orchestrateur (recherche, vérification distincte, critique de complétude ; synthèse versée à part) :
   Coinbase, Market Data Terms (mise à jour du 2026-08-07) : usage « personal or research purposes » ; diffusion des
   « Derived Works », indices et benchmarks interdits sans accord écrit ; usage pour l'IA interdit (art. 3.5). Bitfinex,
   Market Data Terms (2022-07-06) : usage interne ou informatif ; indice et redistribution interdits ; compte exigé pour
   l'API. [lu par cette passe ; 2nd ici]. Le tableau d'INV-1 est complet.
5. **Débloqué** : CB-7, CB-8, CB-9 (3pool, Q-CA-09 ; `eth.drpc.org` et `rpc.mevblocker.io`, Q-CA-10 ; la lecture de la
   documentation de `get_dy` du 3pool est une condition de la G2 de CB-9) ; contrôles E-CA-23 (a) à (h) de RB-2 avec le champ
   de mode ; code CA-0 à CA-6 sur fixtures synthétiques, avec G2 neuve. **Attend** : la réponse à INV-1 (A, A′ ou C) et à
   INV-2 pour l'épinglage et le lancement unique ; le sens des horodatages établi à CB-7.
6. **Items** : formés, précisés ou fermés selon le §13 de la proposition et l'avis (annexe B, bloc B.81).
7. **Réservé à l'investisseur** [INV] : INV-1, INV-2 ; toute dépense (avis juridique, licence) ; aucune place n'est contactée
   sans son accord écrit.

*Ajout daté du 2026-10-08 22:42:53 UTC (décision de l'investisseur, verbatim : « option A, on utilise toutes les sources qu'on veut sans restriction, aucune. »)* : INV-1 = **A** ; aucune source retirée au titre de ses conditions d'usage (question 13 révisée, ajout daté du même jour à l'ADR-0029). L'épinglage et le lancement unique du lot CA n'attendent plus que le code CA-0 à CA-6 et sa G2, le sens des horodatages établi à CB-7 et les ajouts datés déjà versés. La liste des places de calibration est celle de l'option A (six places, SOURCES-HISTORIQUES §1).
