# G0 — proposition pour le lot SIM-BIS (SIM-NIVEAU-BIS ‖ SIM-PUISSANCE-BIS), sans code

- **Statut** : proposition d'un worker à l'orchestrateur, à adjuger. Rien n'est décidé ici. Aucun code au dépôt, aucune écriture
  au dépôt, aucune opération git en écriture.
- **Gate 0** : modèle résolu `claude-opus-5-5`, effort max (fiche `shogen-worker`).
- **Dates** (`date -u`) : lecture des pièces du 2026-10-04 de 21:59 à 22:28 UTC ; mesures de 22:05 à 22:21 UTC ; rédaction à
  partir de 22:29 UTC ; interruption par un redémarrage du conteneur vers 22:40 UTC, reprise à 22:43 UTC (dossier de sortie intact,
  sha256 des mesures recontrôlés égaux [mesuré]) ; fin de rédaction à 22:51 UTC.
- **Brief** : `scratchpad/s2bis/sim-g0/BRIEF-G0-SIM-BIS.md`, sha256 `25b3e9da…c04a` [mesuré] ; le brief n'annonce pas de sha256.
- **Base lue** : branche `claude/compassionate-noether-szmdyj`. Tête au début de la lecture : `b742e3c`. Pendant la lecture,
  l'orchestrateur a commis `b9ba2b4` (2026-10-04T22:11:51Z) : sources de la méthode des rotations versées à `biblio/`, ajout daté
  à l'ADR-0029 (l.143, deux lignes insérées après l.141), item SHOGEN-S2BIS-ROTATION-SOURCE-1 clos, deux lignes de JOURNAL. Les
  trois fichiers changés ont été relus par leur diff, et l'ajout daté en entier. Après la reprise, la tête est `1572f50`
  (2026-10-04T22:42:53Z) : dix commits de la tranche A du collecteur (CB-0a à CB-2e, pièces de revue, annexe B.60, JOURNAL).
  L'ADR-0029 n'y change pas (les « l.n » restent valides) ; l'annexe B et le JOURNAL n'y changent que par ajout en fin de fichier
  (B.60, l.991-1014, lue en entier) ; `gates.yml` gagne le job `s2bis-unittest` (diff lu). Le brief ne nomme pas de base ; écart
  rendu à l'orchestrateur (aucune base avancée par moi). Arbre de travail propre au début et à la fin (`git status --short` vide)
  [mesuré].
- **Rattachement** : ADR-0029 révision 3, acceptée, avec ses ajouts datés : §2.2 (l.86-98), §2.3 (l.100-116), §2.4 (l.118-164,
  dont (c) l.135-143, (d) l.145-156, (e) l.158, (g) l.162, (h) l.164), §2.5 (l.166-175), §2.7 (l.194-214, dont pts 2, 5 à 9,
  l.200, l.203-212), §2.8 (l.219, l.226-228), §5 (l.366-367, l.373-374), §6 lot 4 (l.384), §8.1 (l.442-443) ; G0 de vague
  `docs/adr-0029/G0-lots-S2BIS.md` l.16 (ligne SIM-BIS) et l.17 ; sorties de PLAN-S2BIS (`docs/adr-0029/plan-s2bis/`) et
  `scripts/plan-s2bis/` ; AVIS-STATS (Q1, Q2, Q6, Q11) ; AQT (Q5) ; DÉC (§7 n° 7, §8) ; CE (D-5 pts 2 et 4) ; P6 (C7 l.47 ;
  §3.4 l.88-120 ; §3.6 l.131-150) ; annexe B d'ADR-0028 : SHOGEN-FLUX-ABSORPTION-COLLECTIVE-1 (l.872), SHOGEN-FLUX-SERIEL-1 (l.873),
  et leur contexte B.39 (l.547-558) ; G0 adjugé de COLLECTE-BIS, RECALC-BIS et DEPLOI-BIS (`docs/adr-0029/g0-collecte/`) pour Q-R-01,
  Q-R-02, Q-R-05, Q-R-10 et Q-G-02.
- **Modèle de forme** : `docs/adr-0029/g0-collecte/PROPOSITION.md`, `AVIS.md`, `G0-COLLECTE-RECALC-DEPLOI.md` ; pour la discipline
  de simulation : `docs/adr-0028/G0-lot-SIM-NIVEAU.md` (G0 de SIM-NIVEAU de S2).
- **Conventions** : [lu] lu sur la pièce ; [mesuré] commande lancée par le rédacteur (§14) ; [calc] calcul du rédacteur
  (`mesures/calc_g0.py`, §14) ; [inféré] raisonnement du rédacteur ; [abs] absent des pièces lues. Exigences : E-S-nn. Sous-lots :
  SB-n. Tests : T-… ; mutants : M-… ; questions techniques : Q-S-nn ; actes de l'investisseur : A-n. Tailles : lignes ajoutées,
  tests et données compris, documents hors compte (convention de la proposition modèle, l.23-24) ; toutes les tailles sont
  [inféré].
- **Renvois de lignes** : un « l.n » sans autre mention renvoie à l'ADR-0029 à `b9ba2b4`, inchangée à `1572f50` (sha256
  `22474146…`, 567 lignes). « EP » = `docs/adr-0029/plan-s2bis/episodes.txt` (sha256 `c0371ca5…dbc6`) ; « EP l.n » = sa ligne n.
  Un identifiant d'item suivi de « (l.n) » renvoie à l'annexe B d'ADR-0028 (sha256 `b4a43c2b…` à `b9ba2b4`, `fb5c1463…` à
  `1572f50`, lignes citées inchangées [mesuré]) ; « annexe B l.n » aussi. « AVIS-C » = `docs/adr-0029/g0-collecte/AVIS.md` ;
  « PROP-C » = `docs/adr-0029/g0-collecte/PROPOSITION.md`.

## 0. En bref

1. **Objet** : mesurer, sur données synthétiques seules, le niveau de la règle SHOGEN-CRITERE-R1-2 sous l'hypothèse nulle
   (SIM-NIVEAU-BIS) et sa puissance (SIM-PUISSANCE-BIS), avec la couche d'observateurs, le quorum variable, les défauts locaux non
   attrapés, la censure, des épisodes hétérogènes jusqu'à plusieurs jours et des séries à dérive ; fixer n_s et T_max ; imprimer
   les fréquences de NON ÉVALUABLE ; comparer la rotation enroulée à la variante non enroulée ; évaluer S en sensibilité ; mesurer
   la séquence d'ETH sous la loi jointe par hôte (l.384, l.205).
2. **Code** : `scripts/sim-bis/`, bibliothèque standard seule, en 15 sous-lots de 200 lignes au plus, environ 2 450 lignes avec
   tests [inféré] (l'ADR l.310 en annonçait environ 400) ; au rapport mesuré sur la tranche A du collecteur (× 1,78, environ × 2
   avec corrections, SHOGEN-S2BIS-P1-ESTIMATION-1, annexe B.60), plutôt 4 400 à 4 900 lignes [calc]. Sorties sous
   `docs/adr-0029/sim-bis/`. Le moteur est une **réplique** de R1-2, recoupée par un oracle avec RECALC-BIS (RB-6, puis RB-7),
   parce que RB-7 attend la clôture de SIM-NIVEAU-BIS (adjudication du G0 de collecte, pt 3) : un import serait circulaire.
3. **Calibration** : sur les seules sorties versées de PLAN-S2BIS (EP), aucun journal relu. Constat central : les épisodes de S2
   sont courts (moyenne de 1,05 à 1,45 fenêtre par unité en calme, EP l.13-52), mais I_t est groupée à longue portée
   (FIV_série(240) = 22,9 en calme et 34,6 en stress sur le pool D1-bis, EP l.140, l.157). La part de ce groupement qui tient à
   chaque source (et non à l'observateur unique de S2) n'est pas identifiable depuis EP : elle est **encadrée** par trois niveaux
   (C0 aucun, C1 intermédiaire, C2 « équivalent S2 ») fixés par une calibration épinglée (E1), avant toute mesure de niveau.
4. **La couche d'observateurs n'est calibrée sur aucune mesure de S2-bis** : grille de conception écrite ici ; contrôle de
   couverture par l'orchestrateur seul après le rodage (Q-S-11), pour ne jamais faire passer un taux du rodage au paquet.
5. **Règle de niveau pré-déclarée** (§4) : pour chaque cellule nulle et chaque strate, si le taux de REJETTE dépasse 0,01 à deux
   erreurs-types (à 10⁴ réplications : 122 rejets ou plus [calc]), une phrase de limite, au gabarit fixé ici, va au paquet ;
   rien d'autre ne change.
6. **n_s et T_max** (§3) : plus petite durée d'une échelle de 12 à 24 semaines qui donne une puissance ≥ 0,8 à la cible en calme,
   avec deux bornes de NON ÉVALUABLE ; plancher à 16 semaines (durée acceptée) ; toute durée au-delà de 16 semaines est une
   question de l'orchestrateur à l'investisseur avant le sceau.
7. **Calcul mesuré** : une rotation de dix unités coûte 1,7·10⁻⁴ s pour K seul et 2,5·10⁻⁴ s avec S à n = 109 440 ; R = 9 999
   coûte 2,5 s en calme et 1,0 s en stress [mesuré]. Ordre de grandeur du lot : 90 à 155 h de CPU, 23 à 39 h de mur sur les 4 vCPU
   de l'hôte de session, en lots détachés de 90 min au plus [inféré]. Aucune dépense ; au-delà d'un seuil, question de valeur.
8. **Sources de la méthode** : l'item ROTATION-SOURCE est clos depuis 22:10 UTC (ajout daté l.143) ; ce G0 a lu Harris en entier
   et les passages utiles de Mrkvička et al. et de Kalyuzhny [lu]. Deux nuances de l'ajout daté sont intégrées : chez Harris,
   seule la série décalée doit être stationnaire (la première unité, non décalée, peut ne pas l'être ; le scénario d'état initial
   hors équilibre vise donc une unité décalée, E-S-13) ; chez Kalyuzhny, l'élévation de l'erreur se lit « sous stationnarité, état
   initial hors équilibre », non « sous tendance » (les deux sont simulés, à part). Aucune des trois sources ne valide la rotation
   enroulée sur une statistique de coïncidence : elle reste [inféré], et c'est SIM-NIVEAU-BIS qui la mesure. La « variante non
   enroulée de Harris » ne peut pas être son test conservatif, qui ne se transpose pas utilement à neuf séries décalées
   (Q-S-09) ; la variante comparée est la forme approchée, sans enroulement, sur segment central (correction « minus » de
   Mrkvička et al.).
9. **22 questions techniques** (§10), dont 7 écarts à la lettre de l'ADR signalés sans être appliqués (§11). Les plus lourdes :
   réplications hors cellules nulles (Q-S-06), fond de référence de la cible (Q-S-04), identification du groupement (Q-S-03),
   seuils de « fréquence élevée de NON ÉVALUABLE » (Q-S-13), variante non enroulée (Q-S-09).

## 1. Périmètre exact

### 1.1 Ce que le lot fait

- **SIM-NIVEAU-BIS** : taux de rejet à tort de la règle R1-2 (valeur REJETTE de BTC/USD par strate) sous des modèles nuls
  synthétiques à couche d'observateurs (exigences du §2.2 au §2.4 ci-dessous), au moins 10⁴ réplications par cellule, avec
  erreur-type ; taux familial de la séquence BTC puis ETH ; comparaison de la rotation enroulée et de la variante non enroulée ;
  S en sensibilité ; fréquences de NON ÉVALUABLE sous H0 par strate et en F3 (l.205, l.204, l.366).
- **SIM-PUISSANCE-BIS** : puissance de R1-2 à la cellule cible et sur la grille de l.158, sur une échelle de durées ; puissance
  de la séquence d'ETH à la cible d'ETH (l.162) ; fréquence de NON ÉVALUABLE à la cible ; puissance de S et de la variante ;
  scénarios d'absorption et sériels des deux items de l'annexe B (l.872, l.873) ; tolérance g du compte d'événements
  (PROP-C Q-R-05, adjugée « tolérance à SIM-BIS », AVIS-C l.110).
- **Sorties pour le paquet** : n_s, T_max, puissances, niveaux, fréquences, phrases de limite, dans un bloc
  `[VALEURS POUR LE PAQUET DE S2-BIS]` produit par le script (l.219 : « sorties de SIM-NIVEAU-BIS et SIM-PUISSANCE-BIS ») ; n_s
  et T_max passent ensuite dans la configuration d'analyse de RECALC-BIS (E-R-07, PROP-C l.433).

### 1.2 Entrées

| entrée | usage | état |
|---|---|---|
| EP (`episodes.txt`, sha256 `c0371ca5…dbc6`) | taux de panne et d'écart, histogrammes d'épisodes, censure, par unité et par strate ; courbe FIV_série(ℓ) | versé, sha256 égal à `SHA256SUMS` [mesuré] |
| `okx.txt` (`cb977936…7276`) | pour mémoire : la paire OKX ne pèse que 4 fenêtres sur 154 en calme et 1 sur 133 en stress (l.16, l.22) ; rien n'en est calé | versé |
| ADR-0029 §2.4 e à h, §2.5, §2.7 | cellule cible, grille, pools, règle | acceptée |
| sous-ensemble AS13335 de S2 | bitfinex, coingecko, coinbase, kraken, defillama, chainlink, okx ; singletons binance, gemini, bitstamp (`docs/11-mesures-pilotes.md` l.340, l.355-357) [lu] | rapport de S2 validé |
| pools d'ETH, d'USDC, d'USDT | provisoires (CALIB-ACTIFS-G0 §1, P6 C3) ; finals au paquet (SHOGEN-S2BIS-PAIRES-1) | ouverts |
| identifiants d'unité | ceux de la configuration scellée de COLLECTE-BIS (Q-S-07) | ouverts |
| adjudications du G0 de collecte | axe des runs (Q-R-01), entrée de SHA-256 et sens (Q-R-02), tolérance (Q-R-05), critère collectif (Q-R-10) | adjugées |

### 1.3 Hors périmètre

- Toute donnée de S2-bis (aucune n'existe ; le rodage n'est jamais lu par ce lot, Q-S-11) ; tout journal de S2, tout `*.jsonl` ;
  tout calcul sur les journaux scellés (s'il en faut un, c'est un autre lot, Q-S-03 (b)).
- Les sensibilités (i) à (viii) sur les données (RECALC-BIS), sauf S, la variante non enroulée et deux sensibilités proposées en
  Q-S-19 ; z_s, z_bloc, FIV et la garde §5.4 (niveau déjà mesuré par SIM-NIVEAU de S2) ; le drapeau 2 ; R2.
- Les tailles de pool 15, 20 et 25 (P6 §3.4) : le pool BTC est fixé à 10 unités (DÉC §8 l.122 ; l.164) ; un ajout futur au vote
  rejouerait SIM-BIS sur la cellule redéfinie (l.172, DÉC §7 n° 7 l.107).
- La classe « borné » et la variable d'état P_j : sous H0 sans décrochage, aucune fenêtre n'y entre (E-S-22, Q-S-22).

### 1.4 Items traités

| item | ce que le lot en fait |
|---|---|
| SHOGEN-S2BIS-SIM-1 (ADR l.443) | fermé à la clôture du lot : les simulations du rédacteur de l'ADR (scratchpad, non versées) sont remplacées ; la simulation de taille de pool de P6 n'est pas rejouée (§1.3) |
| SHOGEN-FLUX-ABSORPTION-COLLECTIVE-1 (l.872) | mesuré (E-S-16, E-S-35) ; un critère collectif candidat est proposé ; adoption ou limite écrite décidée par l'orchestrateur avant le gel de RB-5 et RB-7 (Q-S-15 ; Q-R-10) |
| SHOGEN-FLUX-SERIEL-1 (l.873) | transposé à R1-2 et mesuré : unités faibles markoviennes, co-défaillance de triplet, co-défaillance impliquant l'unité faible (E-S-16) |
| SHOGEN-S2BIS-ROTATION-SOURCE-1 (ADR l.442) | clos par l'orchestrateur (ajout daté l.143) ; ses conséquences sont intégrées (E-S-13, E-S-33, Q-S-09) |
| SHOGEN-WORKER-TMPDIR-1 (annexe B l.971) | consigne appliquée au lot (E-S-06) |

## 2. Exigences numérotées

### 2.1 Cadre

| n° | exigence (testable) | rattachement |
|---|---|---|
| E-S-01 | Code sous `scripts/sim-bis/` (Q-S-01), bibliothèque standard seule. Le moteur n'importe ni `shogen_s2` ni `shogen_s2bis` ; deux adaptateurs d'oracle seulement : `oracle_r1.py` (harnais extrait de `f35a70c`, forme de PLAN-S2BIS) et `oracle_recalc.py` (paquet `s2bis` au commit cité). Frontière testée par analyse syntaxique des imports | l.233-234 ; R-8 ; G0 de vague l.16 |
| E-S-02 | Entrées de calibration lues par chemin, sha256 contrôlés contre `docs/adr-0029/plan-s2bis/SHA256SUMS` et contre `parametres.json` ; refus nommé sinon. Aucun journal de campagne, aucun `*.jsonl` lu ; refus si `SHOGEN_S2_CAMPAGNE_CONTROL` est posée | G0 de vague l.16 (« non ») ; annexe D.4 a |
| E-S-03 | Tous les paramètres dans `scripts/sim-bis/parametres.json` (cellules, grilles, graine, R, réplications, échelle des durées, seuils, gabarits de phrases, pools par classe, sous-ensemble AS13335, identifiants), chacun avec sa source ; schéma contrôlé, refus nommés ; sha256 de chaque fichier chargé imprimé en tête des sorties | forme de `scripts/plan-s2bis/parametres.json` |
| E-S-04 | Épinglage avant exécution : l'orchestrateur inscrit au JOURNAL les sha256 des scripts et de `parametres.json` avant toute exécution de niveau ou de puissance ; une sortie dont l'en-tête diffère des épingles n'est pas versée ; tout changement après lecture d'une sortie est une déviation déclarée, les deux sorties gardées | SHOGEN-POSTPREREG-PARAMS-SCEAU-1, règle maintenue (B.58) ; G0 SIM-NIVEAU l.46 |
| E-S-05 | Première ligne de chaque sortie : « synthétique ; préparation de S2-bis ; ne lit aucune donnée de S2-bis ni aucun journal de S2 ; ne change ni R, ni le seuil, ni la règle » | l.205 ; forme de PLAN-S2BIS |
| E-S-06 | Fichiers partiels de calcul sous une extension autre que `.jsonl` ; `TMPDIR` dans le dossier de travail du lot ; tout texte à barre oblique inverse écrit par gabarit (`chr(92)`) et contrôlé sur les octets | consignes de gabarit (B.16) ; SHOGEN-WORKER-TMPDIR-1 |

### 2.2 Modèle génératif : couche des sources

| n° | exigence (testable) | rattachement |
|---|---|---|
| E-S-07 | Unités = hôtes. Pool BTC = les 10 hôtes D1-bis (binance, bitfinex, bitstamp, chainlink, coinbase, coingecko, defillama, gemini, kraken, okx) ; pools d'ETH, d'USDC et d'USDT lus dans `parametres.json` (provisoires, puis ceux du paquet) ; identifiants selon Q-S-07 | l.168 ; l.173 ; EP l.8 (aucun retrait D1-bis) |
| E-S-08 | **Loi jointe par hôte** : par hôte u, un processus de panne d'hôte H(u, ·) commun à toutes les classes que l'hôte sert ; par (u, c), un processus d'écart propre au flux F(u, c, ·) ; état vrai D*(u, c, t) = H ∨ F. Sous H0, processus indépendants d'un hôte à l'autre ; la dépendance entre classes d'un même hôte est admise | l.162 (g) ; DÉC D-2 l.25-26 ; P6 §3.1 l.55-56 |
| E-S-09 | Taux par unité et par strate : H calé sur le taux de « panne » d'EP, F de BTC sur « écart − panne », multipliés par f ∈ {0,3 ; 1} ; F d'ETH et des stables = F de BTC du même hôte (déclaré), sensibilité × 2 ; composante hors-enveloppe additionnelle due au τ re-dérivé, grille {0 ; 2,5·10⁻⁴ ; 10⁻³} par fenêtre (Q-S-21 ; item SHOGEN-SIM-BIS-TAU-NEUF-1) | l.158 (e) ; EP l.12 (classement sous τ et σ de S2) ; `tau_sigma.txt` l.51-58 |
| E-S-10 | Longueurs d'épisodes : loi empirique des épisodes complets par unité et par strate (histogrammes d'EP). En stress, les épisodes complets sont rares (chainlink 3 sur 112, coingecko 8 sur 127, kraken 2 sur 46, bitfinex 2 sur 51, EP l.67, l.75, l.87, l.59) : loi regroupée sur les unités de la strate (Q-S-04) | EP l.13-92 |
| E-S-11 | **Épisodes hétérogènes jusqu'à plusieurs jours** : composante de pannes longues (1 h, 1 jour, 3 jours) portant une part déclarée du taux marginal (0 ; 0,2 ; 0,5), le taux total restant celui d'E-S-09 | l.205 (pt 7) |
| E-S-12 | Groupement temporel propre à chaque unité : régime caché à deux états (normal, dégradé), de paramètres (φ part du temps en régime dégradé, κ rapport des taux, τ_D durée moyenne du régime dégradé) aux trois niveaux C0, C1, C2 fixés par la calibration E1 (E-S-38) ; taux marginal conservé | EP l.128-161 ; §5 (E1) |
| E-S-13 | **Séries à dérive** : (a) tendances indépendantes (multiplicateur de taux linéaire de 0,1 à 1,9 au long de la campagne, sens tiré par unité) ; (b) saut de niveau à un instant tiré, sur trois unités ; (c) état initial hors équilibre : une unité décalée commence la campagne dans une panne longue ; (d) non-stationnarité commune (tendance de même sens sur toutes les unités ; transitoire initial commun : taux × 3 la première semaine), étiquetée « hors prémisse » | l.141, l.143 (Kalyuzhny : élévation sous stationnarité avec état initial hors équilibre) ; l.205 ; l.206 (énoncé REJETTE) |
| E-S-14 | Calendrier : grille UTC w = 60 s, strates calme et stress par le calendrier de S2 (week-end UTC), réplique testée contre `shogen_s2.window` extrait de `f35a70c` ; T_début = lundi 00:00 UTC + décalage de 0 à 6 jours tiré par réplication (Q-S-08) ; simulation jusqu'à T_max | l.196 ; l.158 (e) |
| E-S-15 | Alternatives (H1) : incidents communs à ρ par jour de strate, durée D (forme : Q-S-05), hôtes touchés selon la cellule (2 hôtes ; chacun des 7 hôtes AS13335 avec probabilité 0,7 ; les 10), sur fond f ; un incident coupe le transport de l'hôte, donc frappe toutes ses classes (cible d'ETH) | l.158 (e) ; l.162 (g) ; AVIS-STATS Q6 l.42 |
| E-S-16 | Alternatives d'absorption et sérielles : k ∈ {1 ; 2 ; 4} unités faibles à p_w ∈ {0,25 ; 0,4}, épisodes markoviens de longueur moyenne L_w ∈ {1 ; 20} ; co-défaillance de paire (la cible), de triplet, et impliquant l'unité faible ; avec et sans critère collectif (E-S-35) : 72 cellules ; bascule à une unité faible, p_w de 0 à 0,6 par pas de 0,1, L_w ∈ {1 ; 20} : 14 cellules | annexe B l.872, l.873 ; B.39 (annexe B l.555-557) |

### 2.3 Modèle génératif : couche des observateurs

| n° | exigence (testable) | rattachement |
|---|---|---|
| E-S-17 | Quatre observateurs. Validité par fenêtre : absences D-1 (courtes, de quelques heures, de plusieurs jours ; perte définitive à un instant tiré), dégradations D-2 à D-5 (épisodes courts), pannes simultanées de paires ; M_j. Valeurs : grille de conception (Q-S-11), dont la valeur 2 % de la règle R-a | l.90 ; l.94 ; l.106-110 ; l.226 (R-a) |
| E-S-18 | Repli M = 3 : O4 absent toute la campagne ; quorum 2 sur 3, puis 2 sur 2 quand un second observateur manque | l.78 ; l.94 |
| E-S-19 | Vote : un observateur valide vote « écart » sur (u, c, t) si D* = 1 (manque β par type ; panne régionale vue par un sous-ensemble d'observateurs avec probabilité π), ou si son chemin échoue seul (ε_u, indépendant par (o, u, t) ; référence ε_u = (1 − f)·p̂_u, Q-S-12). Deux types seulement : panne, écart non-panne (Q-S-22) | l.91-93 ; l.96 |
| E-S-20 | **Défaut local non attrapé par D-2 à D-5** : à taux λ_loc ∈ {0 ; 10⁻⁴ ; 10⁻³} par observateur et par fenêtre, durée moyenne 2 fenêtres, l'observateur vote « panne » pour toutes les unités de toutes les classes | l.97 (b) ; AVIS-STATS Q2 l.26 |
| E-S-21 | Artefacts simultanés d'au moins q_j observateurs : à ρ_art ∈ {0 ; 0,05} par jour, durée 20 fenêtres, sur les hôtes AS13335, pour les trois observateurs de l'UE | l.205 (pt 7) ; l.367 ; l.214 (pt 11) |
| E-S-22 | Consolidation : q_j = ⌊M_j/2⌋ + 1 ; D(u, c, t) = 1 si au moins q_j observateurs valides votent « écart » (vote tout axe) ; fenêtre évaluable si M_j ≥ 2 ; « ok » consolidé si au moins q_j observateurs valides ont un statut non-panne. Classe « borné » et P_j hors du modèle nul (aucun décrochage) | l.92 ; l.94 ; l.170 |

### 2.4 Strates, censure, n_s

| n° | exigence (testable) | rattachement |
|---|---|---|
| E-S-23 | Par strate : suite comprimée des fenêtres évaluables depuis T_début, dans l'ordre ; fenêtres retenues = les n_s premières, ou les n′_s présentes à T_max ; règle n′_s ≥ n_s/2 ; date d'atteinte de n_s imprimée (distribution) | l.113 ; l.158 ; l.203 |
| E-S-24 | D1-bis (a), (b) et flux presque mort 2·ok(u, s) < n_s (ou n′_s), par classe, avant K ; retraits comptés et imprimés | l.170 ; l.173 |
| E-S-25 | Échelle des durées W (semaines) : n_calme(W) = 6 840·W, n_stress(W) = 2 736·W, T_max(W) = 1,5·W [calc : W = 16 donne 109 440, 43 776 et 24 semaines, valeurs de l.158] | l.158 (e) |

### 2.5 Statistiques calculées à chaque réplication (réplique de R1-2)

| n° | exigence (testable) | rattachement |
|---|---|---|
| E-S-26 | K_s par compteur « au moins deux » sur masques de bits ; S = Σ_j C(m_j, 2) par plans de bits (additionneur sur 4 plans) ; égalités exigées avec un comptage naïf position par position | l.200 ; l.212 ; AQT Q5 l.111 |
| E-S-27 | Rotations jointes par hôte, selon Q-R-02 adjugée : graine de la réplication = 64 hexadécimaux minuscules (E-S-41) ; o(r, u) = entier big-endian des 32 octets de SHA-256 de la chaîne ASCII `<graine>:<strate>:<r>:<u>` modulo n_s (ou n′_s) de la strate ; r de 1 à 9 999, en décimal sans zéro de tête ; libellés `calme` et `stress` ; la valeur de la position t va en (t + o) mod n ; la première unité du pool BTC D1-bis n'est décalée dans aucune classe ; si elle manque à une classe, toutes les unités de la classe sont décalées | l.200 ; AVIS-C l.57-63 |
| E-S-28 | C_s = #{r : K^(r) ≥ K_s} ; C1 = #{r : K^(r) ≥ 1} ; K_crit,s ≥ 2 ⇔ C1 ≥ 100 [calc : K_crit,s = plus petit k tel que #{r : K^(r) ≥ k} ≤ 99, et k = 0 ne l'est jamais] ; REJETTE ⇔ testable ∧ C_s ≤ 99 ; testable ⇔ au moins 2 unités avec au moins un écart consolidé, K_crit,s ≥ 2, au moins 2 runs de I_t sur la **suite comprimée**, n′_s ≥ n_s/2 ; NON ÉVALUABLE compté par cause | l.202-203 ; AVIS-C l.48-55 (Q-R-01 : « SIM-BIS doit mesurer la fréquence de NON ÉVALUABLE avec cet axe ») |
| E-S-29 | **Arrêt anticipé exact** : les rotations r = 1, 2, … s'arrêtent dès que C_s ≥ 100 et C1 ≥ 100 (et C_S ≥ 100 quand S est suivie). La classification est identique au calcul à R complet [inféré : compteurs non décroissants en r] ; oracle d'équivalence à R complet sur un sous-ensemble pré-déclaré (les 200 premières réplications de chaque cellule) | — |
| E-S-30 | Séquence d'ETH : ETH évalué dans s seulement si BTC REJETTE dans s, sinon NON TESTÉ ; ETH évalué aussi sans condition, en diagnostic imprimé à part (niveau propre d'ETH sous la loi jointe) | l.204 ; l.162 (g) |
| E-S-31 | F3 : USDC/USD et USDT/USD évalués par le même moteur ; valeurs et causes de NON ÉVALUABLE | l.204 ; l.373 |
| E-S-32 | S en sensibilité : C_S = #{r : S^(r) ≥ S} sur les mêmes rotations ; taux de « C_S ≤ 99 » imprimés sous H0 et H1, sans garde ni valeur de règle | l.164 (h) ; l.212 ; DÉC §8 l.122 |
| E-S-33 | **Variante non enroulée** (forme approchée de Harris ; correction « minus » de Mrkvička et al.) : sur la suite comprimée de longueur n, segment central [N, n − N) ; pour chaque r, décalages s(r, u) ∈ {−N, …, N} indépendants, s = (entier de SHA-256 de `<graine>:<strate>:minus:<r>:<u>` modulo 2N + 1) − N, première unité non décalée, **aucun enroulement** ; K_H calculé sur le segment central pour r = 0 (observé) et pour chaque r ; C_H = #{r : K_H^(r) ≥ K_H^(0)} ; même R, même seuil, même garde, évaluée sur le segment central ; N = ⌊n/4⌋ (Q-S-09) | l.141 ; l.143 ; l.205 ; Harris p. 1 et corollaire p. 5 [lu] ; Mrkvička et al. §2.1.2 (sidecar l.285-299) [lu] |
| E-S-34 | Compte d'événements : runs de I_t fusionnés à tolérance g ∈ {0 ; 5 ; 20 ; 60} fenêtres de la suite comprimée, loi de rotation sur les mêmes r ; puissance à la cible ; g proposé à l'orchestrateur (Q-S-18) | l.212 ; PROP-C l.590 ; AVIS-C l.110 |
| E-S-35 | Critère collectif d'absorption, candidat : par classe et par strate, après D1-bis, retrait des unités par p̂_u décroissant (p̂_u = écarts consolidés / n_s) tant que Σ_u p̂_u/(1 − p̂_u) > c*, c* = 1/2 ; il ne lit que des marges, invariantes par rotation [inféré : la loi de rotation reste conditionnellement valide] ; valeurs avec et sans | annexe B l.872 (signe de 1 − Σ p_j/(1 − p_j)) ; Q-R-10 (PROP-C l.604) |
| E-S-36 | Aucune autre statistique hors décision n'est simulée (z_s, z_bloc, FIV, sensibilités (i) à (viii) autres que S et la variante), sauf Q-S-19 | §1.3 |

### 2.6 Calibration sur les sorties de PLAN-S2BIS

| n° | exigence (testable) | rattachement |
|---|---|---|
| E-S-37 | Lecture d'EP : par unité, strate et type (panne, écart), taux, comptes de cellules, d'épisodes, de censurés et de complets, histogramme ; courbe FIV_série(ℓ) du pool D1-bis et du pool de S2 ; nombres pris en rationnels exacts depuis leur écriture décimale ; refus nommé sur tout écart de forme ; contrôle de cohérence : cellules / n_s = taux imprimé, pour chaque ligne | EP l.12-161 ; `episodes.py` l.4-11 |
| E-S-38 | **Calibration E1 du groupement**, par strate : modèle d'E-S-12 pour des unités indépendantes vues d'un seul observateur, à f = 1, sur le calendrier du segment J28 de S2 (portée et plage D5 d'EP l.6) ; grille pré-déclarée φ ∈ {0,01 ; 0,02 ; 0,05 ; 0,1}, κ ∈ {5 ; 10 ; 20 ; 50}, τ_D ∈ {60 ; 240 ; 1 440 ; 4 320} fenêtres ; critère : somme des carrés des écarts de log FIV_série(ℓ) aux ℓ d'EP où la garde est tenue ; C2 = meilleur point ; C1 = point dont log FIV_série(240) est le plus proche de la moyenne des logs de C0 et de C2 ; égalités départagées par le plus petit κ, puis le plus petit τ_D ; 200 réplications par point ; sortie épinglée avant toute exécution de niveau ou de puissance | EP l.128-161 ; §5 |
| E-S-39 | Oracles du générateur : sous C0, sans observateurs, taux marginal et histogramme d'épisodes reproduits à 5 erreurs-types près ; FIV_série calculé par la même forme que PLAN-S2BIS (`r1.block_long_run_variance`, forme de `bloc_strate`), égal à r1 extrait de `f35a70c` sur 10 réplications | `episodes.py` l.59-70 ; G0 SIM-NIVEAU oracle (4) l.194-197 |

### 2.7 Réplications, erreur-type, identité bit à bit

| n° | exigence (testable) | rattachement |
|---|---|---|
| E-S-40 | **Au moins 10⁴ réplications** pour chaque cellule nulle et pour la cible à la durée retenue, dans chaque strate ; autres familles selon Q-S-06 ; pour chaque taux : x, r̂ = x/R_rep, SE = √(r̂(1 − r̂)/R_rep), et la borne unilatérale à 95 % 1 − 0,05^(1/R_rep) quand x = 0 (≈ 3,0·10⁻⁴ à 10⁴ [calc]) | l.205 ; l.384 |
| E-S-41 | Graines : GRAINE = 20261004, fixée ici, aucune autre essayée (le chronométrage du G1 utilise l'étiquette distincte `SIM-BIS-proto`) ; flux de génération par (cellule, réplication i, composant, indice) : 8 premiers octets de SHA-256 de la chaîne ASCII `SHOGEN-SIM-BIS|20261004|<cellule>|<i>|<composant>|<indice>`, puis `random.Random` ; graine de règle de la réplication = SHA-256 hexadécimal de `SHOGEN-SIM-BIS|20261004|<cellule>|<i>` | G0 SIM-NIVEAU §4 (l.101-104) |
| E-S-42 | Ordre : seule la méthode `random()` est appelée (seule garantie de stabilité d'une version de Python à l'autre, d'après la documentation citée par G0 SIM-NIVEAU l.103 [2nd]) ; ordre des tirages fixé par flux ; aucune itération sur un ensemble ; agrégation dans l'ordre des réplications ; sorties indépendantes du nombre de processus et de `PYTHONHASHSEED` | G0 SIM-NIVEAU §4, §7 |
| E-S-43 | Flottants : aucune fonction transcendante de libm dans les générateurs ; lois géométriques et empiriques tirées par tables de seuils calculées en arithmétique exacte (`Fraction` ou `Decimal` sous contexte nommé), puis `bisect` sur `random()` ; statistiques en entiers et rationnels ; SE en `Decimal` sous contexte nommé (précision 50, `ROUND_HALF_EVEN`) ; la comparaison « au-dessus de 0,01 à deux erreurs-types » en arithmétique exacte (§4) ; JSON à clés triées, séparateurs fixes, sans heure, hôte ni version (journal d'exécution à part) | PROP-C Q-C-14 (contexte de `r1`) ; G0 SIM-NIVEAU §6 |
| E-S-44 | **Identité bit à bit** de deux exécutions A et B (portée : Q-S-10) : sha256 égaux des sorties et des empreintes par cellule (sha256 de la suite ordonnée des enregistrements par réplication) ; invariance au nombre de processus (1 contre 4) et à `PYTHONHASHSEED` (0 contre 1) | l.384 ; G0 SIM-NIVEAU oracles (1), (1b) |
| E-S-45 | Lots de calcul reprenables : un fichier partiel par lot (cellule, plage de i), sha256 consigné ; l'agrégation exige chaque i une fois et une seule ; un lot interrompu par la borne de temps est refait, jamais compté | consigne « tâches longues » (B.16) |

### 2.8 Calcul, sorties, paquet

| n° | exigence (testable) | rattachement |
|---|---|---|
| E-S-46 | **Budget mesuré** avant toute campagne : chronométrage sur le code commis, 100 réplications par famille de cellules ; plan de lots (chacun sous 90 min mesurées), lancés détachés (`setsid nohup`, PID et fichier de sortie consignés, fin constatée en sondant le PID) ; plan écrit au G1 et approuvé par l'orchestrateur | brief ; consigne « tâches longues » |
| E-S-47 | Lieu du calcul : hôte de session ; aucune dépense ; au-delà du seuil de Q-S-16, question de l'orchestrateur à l'investisseur (§13, A-3) | brief ; G0 de vague l.7-8 |
| E-S-48 | Sorties sous `docs/adr-0029/sim-bis/` : `calibration_e1.{json,txt}`, `sim_niveau_bis.{json,txt}`, `sim_puissance_bis.{json,txt}`, `SHA256SUMS`, README ; schéma `shogen.sim-bis.v1` ; écrites seulement si tous les oracles internes passent, jamais par-dessus un fichier existant | G0 SIM-NIVEAU §6 |
| E-S-49 | La règle de niveau du §4 est appliquée par le script ; les phrases de limite sont produites depuis le gabarit du §4 | l.205 |
| E-S-50 | La règle de n_s et de T_max du §3 est appliquée par le script ; bloc `[VALEURS POUR LE PAQUET DE S2-BIS]` | l.158 (e) ; l.219 |
| E-S-51 | **Oracle croisé avec RECALC-BIS** : o(r, u) et K^(r) égaux à ceux de RB-6 sur 5 vecteurs de test (dont o = 0 et o = n − 1, AVIS-C l.63) et 100 séries synthétiques, dès le commit de RB-6 ; valeur de la règle égale à RB-7 sur 100 séries consolidées synthétiques, avant le sceau (item SHOGEN-SIM-BIS-ORACLE-RB7-1) | G0 de collecte, adjudication pt 3 ; E-R-16, E-R-17, E-R-20 |
| E-S-52 | Fréquences de NON ÉVALUABLE par strate et par cause (information insuffisante, détaillée en ≤ 1 unité en écart, K_crit,s < 2, moins de 2 runs ; n′_s < n_s/2) : sous H0 de référence, à la cible, en F3 ; imprimées au paquet | l.366 ; l.204 ; l.219 |

### 2.9 Tests

| n° | exigence (testable) | rattachement |
|---|---|---|
| E-S-53 | Tests d'abord ; valeurs de référence indépendantes du code (écrites à la main, ou produites par un outil distinct : `sha256sum`, `bc`) ; échec montré avant le code ; une mutation par test | règle 4 de la fiche |
| E-S-54 | Campagne de mutants classée par la sortie du runner : 0 vivant, 1 tué, 3 ou toute autre sortie FATAL, campagne relancée après correction | SHOGEN-MUT-FATAL-1 (consignes B.16) |
| E-S-55 | Suite `scripts/sim-bis` verte à chaque sous-lot ; suite `s2-harness` inchangée (405 tests, OK, skipped=2 [mesuré à `b9ba2b4`]) | règle 4 de la fiche |

## 3. Ce qui fixe n_s et T_max, et comment cela s'écrit au paquet

1. **Fond de référence** de la cible (Q-S-04, recommandé) : cellule opérationnelle de l.158 (un incident tous les 10 jours de
   strate, de 20 minutes, touchant chacun des 7 hôtes AS13335 avec probabilité 0,7), sur un fond propre de S2 multiplié par
   f = 0,3, calé par EP, au niveau de groupement C2, couche d'observateurs nominale (Q-S-11).
2. **Échelle** : W ∈ {12 ; 14 ; 16 ; 18 ; 20 ; 22 ; 24} semaines ; n_calme(W) = 6 840·W, n_stress(W) = 2 736·W, T_max(W) =
   1,5·W semaines (rapport de l.158).
3. **Critère** : W* = plus petite durée de l'échelle telle que, au fond de référence : (a) puissance de R1-2 pour BTC à la cible
   en calme ≥ 0,80 ; (b) NON ÉVALUABLE à la cible en calme ≤ 5 % ; (c) NON ÉVALUABLE sous H0 de référence (cellule N1) en calme
   ≤ 20 % (seuils de (b) et (c) : Q-S-13). Puissance par estimation ponctuelle, SE imprimée ; 2 000 réplications par durée de
   l'échelle pour la cible et pour N1, puis 10⁴ à la durée retenue (Q-S-06). Les cellules nulles du §5.1 tournent ensuite à la
   durée retenue.
4. **Plancher et acte** : W retenue = max(16, W*) (Q-S-14). Si W* > 16, ou si aucune durée de l'échelle ne tient (a) à (c), le
   script imprime les valeurs et la limite, mais **la durée écrite au paquet reste 16 semaines** jusqu'à la décision de
   l'investisseur sur la durée et le coût, posée par l'orchestrateur avant le sceau (A-2). Repères [calc] : à 16 semaines, la
   cible donne 7,6 incidents attendus en calme et 3,04 en stress ; la probabilité d'au plus un incident vaut 0,4 % en calme et
   19 % en stress (loi de Poisson) : la garde des deux runs pèse surtout en stress.
5. **Stress** : aucune exigence de puissance ; puissance imprimée avec le verdict (l.158, l.206).
6. **Écriture au paquet** : un bloc `[VALEURS POUR LE PAQUET DE S2-BIS]` produit par le script, sans retouche : W, n_calme,
   n_stress, T_max ; puissance à la cible en calme et en stress, avec SE ; puissance de la séquence d'ETH ; fréquences de NON
   ÉVALUABLE (H0 par strate, cible, F3) ; taux de rejet de chaque cellule nulle avec SE, et les phrases de limite du §4 ;
   comparaison enroulée et non enroulée ; puissance de S ; g ; état du critère collectif ; sha256 des sorties, commit et sha256 des
   scripts et de `parametres.json`. n_s et T_max passent ensuite dans la configuration d'analyse de RECALC-BIS (E-R-07) ; le cp-1
   du paquet vérifie l'égalité du bloc et du JSON.

## 4. Règle de niveau pré-déclarée

1. Pour chaque cellule nulle c (§5, table des cellules) et chaque strate s, sur R_rep réplications : x = nombre de valeurs
   REJETTE de BTC ; r̂ = x/R_rep ; SE = √(r̂(1 − r̂)/R_rep).
2. « Niveau au-dessus de 0,01 à deux erreurs-types » ⇔ r̂ > 0,01 et (r̂ − 0,01)² > 4·r̂(1 − r̂)/R_rep, évalué en rationnels exacts.
   À R_rep = 10⁴, la condition tient exactement pour x ≥ 122 [calc].
3. **Conséquence** : une phrase de limite au paquet, gabarit fixé ici : « Limite (SIM-NIVEAU-BIS, cellule <c>, strate <s>) : sous
   le modèle nul synthétique <description>, la règle R1-2 rejette à tort dans <x> réplications sur <R_rep> (<r̂>, erreur-type
   <SE>), au-dessus de 0,01 à deux erreurs-types ; R, le seuil, la garde et la règle ne changent pas. » **Rien d'autre ne
   change** : ni R, ni le seuil 99, ni la garde, ni la règle, ni n_s.
4. Même règle, même gabarit, pour le taux familial de la séquence BTC puis ETH par strate (au moins un rejet à tort).
5. Hors règle, imprimés avec leur SE et sans phrase de limite : S, la variante non enroulée, ETH sans condition, F3, le critère
   collectif candidat (Q-S-15).
6. Les cellules « hors prémisse » (non-stationnarité commune) et celle des artefacts simultanés suivent la même règle ; leur
   phrase porte leur description, qui renvoie aux limites déjà écrites (l.206, l.214).
7. Aucune correction de multiplicité entre cellules : une cellule de plus ne peut qu'ajouter une limite. Au niveau exact 0,01,
   la probabilité d'une phrase par hasard vaut 1,8 % par cellule et par strate, et 43 % sur 32 cellules-strates supposées
   indépendantes [calc, binomiale exacte] : la liste des phrases est imprimée avec ce rappel.
8. Ni les paramètres, ni R, ni la graine, ni la liste des cellules, ni les définitions des taux ne changent après la lecture
   d'une sortie (E-S-04).

## 5. Cellules, calibration et ordre d'exécution

### 5.1 Cellules nulles (SIM-NIVEAU-BIS), 10⁴ réplications chacune

Référence N1 : f = 0,3 ; fond calé par EP ; groupement C1 ; couche d'observateurs nominale ; ε_u = 0,7·p̂_u ; ni défaut local,
ni artefact, ni dérive ; T_début tiré.

| cellule | écart à N1 | ce qu'elle mesure |
|---|---|---|
| N0 | f = 1, C0, ε = 10⁻⁴ | fond f = 1 du scénario C de l.145-156 (« bruit de S2 »), sans son L = 20 |
| N1 | — | référence ; critère (c) du §3 |
| N2 | C0 | niveau sans groupement |
| N3 | C2 | groupement équivalent S2 ; portée de corrélation longue (la correction torique devient de plus en plus libérale quand la portée croît, au-delà du double du niveau nominal pour les champs les plus lisses : Mrkvička et al. p. 17, sidecar l.797-800 [lu]) |
| N4 | pannes longues : part 0,5 du taux, 1 h à 3 jours | épisodes jusqu'à plusieurs jours |
| N5 | observateurs dégradés : 2 % D-1, 2 % D-2 à D-5, perte d'un observateur à un instant tiré, pannes de paires | M_j variable, quorums 3/4, 2/3, 2/2 |
| N6 | λ_loc = 10⁻³ | défauts locaux non attrapés (l.97 b) |
| N7 | π = 0,2 ; β = 0,2 | pannes régionales et manques partiels |
| N8 | tendances indépendantes (E-S-13 a) | dérive propre à chaque unité |
| N9 | état initial hors équilibre (E-S-13 c) et sauts (b) | mécanisme de Kalyuzhny (l.143) |
| N10 | f = 0,1 | fond bas : n·P_more ≈ 1,4 en calme et 0,64 en stress à 16 semaines [calc, indépendance] |
| N11 | deux unités faibles à p_w = 0,4 | niveau avec et sans critère collectif |
| N12 | repli M = 3 | quorum 2/3 permanent |
| X1 | tendance commune (E-S-13 d) | hors prémisse : non-stationnarité commune comptée comme dépendance |
| X2 | transitoire initial commun | hors prémisse |
| X3 | ρ_art = 0,05 par jour | modes communs d'au moins q_j observateurs (l.214) |

La variante non enroulée est calculée sur N1, N3, N4, N8, N9 et X1 ; F3 sur N1 ; ETH sans condition sur N1 et N3.

Repères de fond [calc, fenêtres indépendantes, taux d'écart d'EP] : à 16 semaines, n·P_more vaut 12,2 en calme et 5,7 en stress
à f = 0,3, et 134 et 63 à f = 1. Sous H0, la garde des deux runs est donc peu liante à f = 0,3 sans groupement, et liante à
f = 0,1 (N10) [inféré] ; le groupement (C1, C2) réunit les fenêtres K en moins de runs.

### 5.2 Cellules de puissance (SIM-PUISSANCE-BIS)

| famille | contenu | réplications (Q-S-06 b) |
|---|---|---|
| P-cible | cible, fond de référence (§3), sept durées de l'échelle ; N1 aux mêmes durées (critère (c) du §3) | 2 000 par durée ; 10⁴ à la durée retenue |
| P-ETH | séquence BTC puis ETH à la cible d'ETH, durée retenue | 2 000 |
| P-F3 | F3 à la cible (les incidents coupent le transport, donc toutes les classes) | 2 000 |
| P-var | variante non enroulée et S à la cible | sur les réplications de P-cible |
| P-év | compte d'événements, g ∈ {0 ; 5 ; 20 ; 60} | sur 2 000 réplications de P-cible |
| P-grille | ρ ∈ {0,05 ; 0,1 ; 0,2 ; 0,5} × D ∈ {5 ; 20 ; 60} × hôtes ∈ {2 ; 0,7 × 7 ; 10} × f ∈ {0,3 ; 1}, soit 72 cellules, durée retenue | 1 000, R = 999 |
| P-abs | E-S-16 : 72 cellules (k × p_w × L_w × alternative × critère) et 14 cellules de bascule | 1 000, R = 999 |
| P-L20 | lettre du scénario B (L = 20, sans groupement), durée retenue | 2 000 |

### 5.3 Calibration E1 (avant toute cellule)

Pourquoi un encadrement : EP donne des taux et des histogrammes par unité, mais un seul indicateur de groupement, celui de I_t
(au moins deux écarts), sur le pool d'un observateur unique. Son FIV_série croît de 1 à ℓ = 1 à 22,9 à ℓ = 240 et 34,0 à
ℓ = 1 440 en calme (EP l.128, l.140, l.144), bien au-delà de ce que des épisodes de 1 à 6 fenêtres expliquent seuls [inféré].
Ce groupement mêle trois causes que EP ne sépare pas : régimes propres à chaque source, modes communs entre sources, artefacts de
l'observateur unique de S2 (l.38-41). Sous H0, seule la première existe. E1 cherche donc, dans une famille de régimes propres et
indépendants, le point qui reproduit la courbe de S2 (C2 : « tout le groupement de S2 tient aux sources, chacune pour soi », cas
le plus défavorable plausible pour une loi par rotations) ; C0 n'a aucun groupement ; C1 est entre les deux. Si la famille
n'atteint pas la courbe de S2, C2 est le point le plus proche et la limite est écrite. Une mesure par unité (FIV_u(ℓ), intervalles
entre épisodes) lèverait l'ambiguïté : elle exige un passage sur les journaux scellés, hors de ce lot (Q-S-03 b).

### 5.4 Ordre d'exécution

1. **E0** : épinglage des scripts et de `parametres.json` au JOURNAL (E-S-04).
2. **E1** : calibration ; sortie versée et épinglée.
3. **Exécution provisoire** (pools de l'ADR, identifiants courts) : N1, N3, N11, P-cible à W = 16, P-abs, P-év. Elle sert à clore la
   conception : critère collectif (Q-S-15), g (Q-S-18), variante en sensibilité ou non ; elle **débloque RB-7** (adjudication du
   G0 de collecte, pt 3).
4. **Exécution finale épinglée**, après le gel des pools (licences, paires, identifiants ; Q-S-17), dans cet ordre : (a) échelle
   des durées, P-cible et N1 à 2 000 réplications par durée ; (b) durée retenue par la règle du §3, imprimée ; (c) à cette durée,
   cellules nulles du §5.1 (10⁴ chacune), P-cible porté à 10⁴, P-ETH, P-F3, P-var, P-év, P-L20, P-grille, P-abs ; (d) exécution B
   (Q-S-10) ; (e) versement et bloc du paquet. Si la durée retenue attend l'acte A-2, les étapes (c) à (e) tournent à 16 semaines
   et sont refaites à la durée décidée.

## 6. Sous-lots, tests attendus, mutants

### 6.1 Sous-lots (≤ 200 lignes ajoutées chacun, tests et données compris)

| sous-lot | objet | taille | dépend de |
|---|---|---|---|
| SB-0 | socle : `parametres.json` (schéma), `commun.py` (chargement, sha256 des entrées, refus nommés, garde de la variable de campagne, écriture atomique, en-tête et étiquette) | ≈ 190 | — |
| SB-1 | `aleas.py` : flux par SHA-256, tables de seuils exactes, tirages Bernoulli, géométriques et empiriques par `bisect` | ≈ 170 | SB-0 |
| SB-2 | `calibration.py` : lecture d'EP en rationnels exacts, contrôles de forme et de cohérence | ≈ 160 | SB-0 |
| SB-3 | `sources.py` I : processus par hôte (régime, épisodes empiriques, pannes longues, dérives) sur la grille | ≈ 190 | SB-1, SB-2 |
| SB-4 | `sources.py` II : classes jointes par hôte, incidents (cible, grille, ETH), unités faibles, triplets | ≈ 180 | SB-3 |
| SB-5 | `calendrier.py` : strates, T_début tiré, compression, n_s premières, T_max, n′_s, runs sur la suite comprimée ; test croisé avec `window` | ≈ 170 | SB-0 |
| SB-6 | `observateurs.py` : validité, M_j, votes, défauts locaux, artefacts, consolidation à q_j, « ok » consolidé | ≈ 190 | SB-1, SB-5 |
| SB-7 | `regle.py` I : D1-bis et flux presque mort, K et S par tranches, décalages SHA-256, rotation enroulée, C_s, C1, arrêt anticipé, garde, valeur | ≈ 200 | SB-5 |
| SB-8 | `regle.py` II : séquence d'ETH, F3, mode à R complet, oracle d'équivalence de l'arrêt anticipé, compte d'événements, critère collectif | ≈ 180 | SB-7 |
| SB-9 | `variante.py` : rotation non enroulée sur segment central | ≈ 140 | SB-7 |
| SB-10 | `calib_fiv.py` : estimateur FIV_série (forme de PLAN-S2BIS), grille et critère d'E1 ; oracle contre `r1` extrait | ≈ 190 | SB-3, SB-5 |
| SB-11 | `executer.py` : cellules, strates, réplications, processus ordonnés, lots reprenables, agrégation exacte, SE en `Decimal`, sorties | ≈ 200 | SB-6 à SB-10 |
| SB-12 | `paquet.py` : règle de niveau du §4, règle de n_s du §3, phrases de limite, bloc pour le paquet | ≈ 170 | SB-11 |
| SB-13 | `oracle_recalc.py` : oracle croisé avec RB-6, puis RB-7 | ≈ 120 | SB-7 ; RB-6 ; RB-7 |
| SB-14 | `oracle_r1.py` : adaptateur r1 de `f35a70c` (FIV, `window`) | ≈ 100 | SB-5, SB-10 |

Total : environ 2 450 lignes avec tests [inféré]. Pour comparaison : l'ADR l.310 annonce environ 400 lignes de simulations ;
les simulations de S2 font 2 255 lignes sans tests unitaires (`scripts/sim/*.py`) et PLAN-S2BIS 1 392 lignes avec tests [mesuré,
`wc -l`]. Le collecteur de S2-bis a mesuré × 1,78 son estimation de G0 sur CB-0 à CB-2, environ × 2 avec les corrections
(SHOGEN-S2BIS-P1-ESTIMATION-1, annexe B.60) : appliqué ici, environ 4 400 à 4 900 lignes, soit 25 à 30 sous-lots [calc] ; le
découpage ci-dessus se sous-coupe alors au G1, chaque sous-lot gardant sa ligne datée à l'annexe A.

**Parties** (METHODE-PARTIES l.30, l.39) : S-1 « moteur » (SB-0 à SB-6, ≈ 1 250 lignes) ; S-2 « règle, calibration et
exécution » (SB-7 à SB-12, SB-14, ≈ 1 180 lignes) ; S-3 « exécution finale et oracle croisé » (SB-13, exécutions épinglées,
sorties). Chacune : relecture G2 neuve à 100 % avec la checklist et l'enregistrement de rôle, revue de l'orchestrateur, accord de
l'investisseur.

### 6.2 Tests attendus (valeurs de référence indépendantes du code)

| test | valeur de référence | mutants qu'il doit tuer |
|---|---|---|
| T-AL-1 graines | 3 chaînes ASCII ; sha256 par `sha256sum`, 8 premiers octets convertis par `bc` | M-AL-1 octets de queue au lieu de tête ; M-AL-2 séparateur omis |
| T-AL-2 tables | seuils de la loi géométrique p = 1/700 aux rangs 1, 10, 100, calculés à la main en `Fraction` ; histogramme empirique d'EP l.14 (301, 24, 6, 1) en seuils cumulés | M-AL-3 seuil décalé d'un rang ; M-AL-4 `random()` remplacé par `uniform` |
| T-CAL-1 lecture d'EP | trois lignes recopiées à la main (EP l.13, l.14, l.140) et leurs rationnels | M-CAL-1 censurés ajoutés aux complets ; M-CAL-2 garde ignorée |
| T-GEN-1 taux | chaîne à deux états : taux stationnaire b/(1 − a + b) écrit à la main en rationnel ; moyenne simulée à 5 SE | M-GEN-1 a et b inversés ; M-GEN-2 état initial non stationnaire |
| T-GEN-2 jointe par hôte | une panne d'hôte écrite à la main frappe les 4 classes de l'hôte, aucune autre | M-GEN-3 panne tirée par classe |
| T-CAL-2 calendrier | dates de week-end UTC écrites à la main, et `window` de `f35a70c` | M-CAL-3 week-end en heure locale |
| T-OBS-1 quorum | table écrite à la main des votes pour M_j = 2, 3 et 4 | M-OBS-1 q = 2 fixe ; M-OBS-2 ⌈M_j/2⌉ ; M-OBS-3 non valide compté comme votant |
| T-OBS-2 défaut local | un observateur en défaut local abaisse d'un vote le quorum de toutes les unités (exemple à la main) | M-OBS-4 défaut appliqué à une seule classe |
| T-SEQ-1 compression | suite de 12 fenêtres dont 3 censurées : positions retenues, n_s premières, n′_s à T_max, à la main | M-SEQ-1 rotation sur la grille ; M-SEQ-2 n′_s ≥ n_s/2 en « > » |
| T-RUN-1 runs | un incident coupé par une perte de quorum : 1 run sur la suite comprimée, 2 sur la grille (AVIS-C l.51-53) | M-RUN-1 runs comptés sur la grille |
| T-ROT-1 décalages | o(r, u) pour 5 vecteurs dont o = 0 et o = n − 1, calculés par `sha256sum` et `bc` | M-ROT-1 classe dans l'entrée ; M-ROT-2 première unité décalée ; M-ROT-3 modulo n_s au lieu de n′_s ; M-ROT-4 sens inversé |
| T-ROT-2 K et S | 3 unités, 8 fenêtres, décalages fixés : K^(r) et S^(r) à la main ; égalité avec le comptage naïf sur 1 000 essais aléatoires | M-ROT-5 « au moins un » ; M-ROT-6 S sans le terme croisé des plans |
| T-REG-1 décision | listes de K^(r) injectées : C_s = 99 et 100 ; C1 = 99 et 100 ; deux runs et un run | M-REG-1 `< 99` ; M-REG-2 K_crit ≥ 1 ; M-REG-3 un run suffit ; M-REG-4 R = 9 998 ; M-REG-5 `>` au lieu de `≥` dans C_s |
| T-REG-2 arrêt anticipé | 200 instances : classification identique à R complet | M-REG-6 arrêt à C_s ≥ 99 ; M-REG-7 C1 non suivi |
| T-REG-3 séquence et F3 | ETH testé seulement si BTC rejette ; F3 sans valeur de registre | M-REG-8 ETH toujours testé |
| T-VAR-1 variante | segment central et décalages écrits à la main sur 3 unités de 12 fenêtres | M-VAR-1 enroulement réintroduit ; M-VAR-2 segment non central |
| T-ABS-1 critère | pool de 5 unités à p̂ écrits à la main : unités retirées et indice final | M-ABS-1 retrait par p̂ croissant |
| T-FIV-1 estimateur | FIV_série(2) = 5/4 sur une série de la fixture de PLAN-S2BIS (G1 PLAN-S2BIS l.92) ; égalité avec `r1` extrait | M-FIV-1 poids 1 − (k+1)/ℓ |
| T-NIV-1 règle du §4 | x = 121 et 122 à R_rep = 10⁴ (borne exacte, §4 pt 2) ; phrase produite égale au gabarit | M-NIV-1 « ≥ » au lieu de « > » ; M-NIV-2 SE en flottants |
| T-NS-1 règle du §3 | table de puissances fictive écrite à la main : W choisi, plancher 16, cas « aucune durée » | M-NS-1 plancher omis ; M-NS-2 critère (c) omis |
| T-DET-1 identité | deux exécutions sur 3 cellules × 200 réplications : sorties égales à l'octet ; 1 contre 4 processus ; `PYTHONHASHSEED` 0 contre 1 | M-DET-1 graine dérivée de l'indice de tâche ; M-DET-2 itération sur un ensemble |
| T-FRO-1 frontière | analyse des imports ; variable de campagne posée : refus ; entrée à sha256 faux : refus | M-FRO-1 `import shogen_s2` dans le moteur ; M-FRO-2 contrôle sha sauté |

Mutants de spécification sans oracle (à tuer par relecture, déclarés) : définition de C1 contre K_crit, tolérance g fusionnée sur
la grille au lieu de la suite comprimée.

## 7. Calcul : budget mesuré et lieu

**Mesures** [mesuré, hôte de session, Python 3.11.15, 4 vCPU, charge ≈ 0,3 à 0,9, `mesures/`] :

| mesure | n = 109 440 (calme, 16 semaines) | n = 43 776 (stress) |
|---|---|---|
| par rotation, 10 unités : 9 décalages SHA-256 | 9,0·10⁻⁶ s | 9,5·10⁻⁶ s |
| 9 rotations de masques | 6,5·10⁻⁵ s | 2,9·10⁻⁵ s |
| K par tranches (par paires) | 9,2·10⁻⁵ s (1,7·10⁻⁴ s) | 2,6·10⁻⁵ s (6,8·10⁻⁵ s) |
| S par plans (par paires) | 8,7·10⁻⁵ s (3,0·10⁻⁴ s) | 3,2·10⁻⁵ s (1,0·10⁻⁴ s) |
| R = 9 999 rotations : K seul ; K et S | 1,66 s ; 2,52 s | 0,64 s ; 0,96 s |

Chaîne de génération (sonde 2, grille de 24 semaines = 241 920 fenêtres, 4 observateurs, 4 classes × 10 unités, tirage fenêtre par
fenêtre) : validité 0,06 s, sources 0,73 s, votes et quorum 2,10 s, compression 0,19 s, runs 0,0002 s ; 3,2 s par réplication. Le
tirage clairsemé (sauts géométriques) de 10 unités à n = 109 440 coûte 2,9·10⁻³ s, mais il emploie `math.log` (libm), que E-S-43
exclut : le G1 le refait par tables. Estimation [inféré] : 0,3 s par réplication hors rotations, à mesurer (E-S-46).

**Ordre de grandeur** [inféré, sur ces mesures] :

| phase | contenu | estimation (h de CPU) |
|---|---|---|
| E1 | 64 points × 2 strates × 200 réplications | 2 à 3 |
| E2 | 16 cellules nulles × 10⁴, arrêt anticipé (≈ 560 rotations en moyenne sous une p-valeur uniforme [calc]) | 25 à 45 |
| E3 | P-cible (échelle, puis 10⁴), P-ETH, P-F3, P-év, P-L20 | 30 à 40 |
| E3 | P-grille (72 cellules) et P-abs (86 cellules), 1 000 réplications à R = 999 | 25 à 30 |
| B | identité (Q-S-10 b) | 10 à 35 |
| total | | 90 à 155 h, soit 23 à 39 h de mur sur 4 vCPU libres |

Avec 10⁴ réplications et R = 9 999 partout (Q-S-06 a), la grille seule demanderait environ 600 h, et la grille avec les
cellules d'absorption plus de 1 000 h [inféré] : hors de portée de l'hôte de session. L'hôte est partagé avec d'autres workers :
le mur peut doubler.

**Lieu** (Q-S-16) : l'hôte de session, en lots détachés de 90 min au plus (borne de fond de 2 h), sans dépense. Le conteneur est
éphémère (PASSATION §5 bis) : chaque phase est versée par l'orchestrateur dès sa fin ; un lot perdu se refait à l'identique
(graines par réplication). **R-8** : bibliothèque standard seule ; aucune dépendance n'est proposée. Si l'orchestrateur voulait
NumPy ou PyPy pour gagner du temps, la vérification au registre se ferait avant toute installation (non faite ici) ; je ne le
recommande pas : la voie par entiers en masques de bits tient dans le budget, et NumPy n'accélérerait pas une rotation de masques
déjà en C [inféré, non mesuré].

## 8. Dépendances

| dépendance | effet sur le lot | état |
|---|---|---|
| PLAN-S2BIS | entrées de calibration | fait, sorties épinglées (B.58) |
| SHOGEN-S2BIS-ROTATION-SOURCE-1 | définition de la variante, scénarios de dérive | **clos** à 22:10 UTC (ajout daté l.143 : deux nuances, stationnarité de la seule série décalée chez Harris, « sous stationnarité, état initial hors équilibre » chez Kalyuzhny ; aucune source ne valide la rotation enroulée sur une statistique de coïncidence, [inféré], mesurée par SIM-NIVEAU-BIS) ; Harris lu en entier par ce G0, Mrkvička et al. et Kalyuzhny par passages [lu] ; aucun procurement restant |
| pools d'ETH, d'USDC, d'USDT (SHOGEN-S2BIS-PAIRES-1) | P-ETH, P-F3, ETH sans condition | provisoires ; exécution finale après le gel |
| licences du pool (SHOGEN-S2BIS-LICENCES-API-1 ; q. 13 : recommandation « les retirer », l.415, acceptée avec les autres recommandations, l.6) | un retrait d'unité impose de rejouer (l.175, l.374) ; un retrait dans le sous-ensemble AS13335 change la cible | ouvert ; risque majeur : la pièce CALIB-ACTIFS-G0 ne trouve de permission explicite de republication que chez deux places, et pour leurs historiques seulement (§1 de cette pièce) ; les conditions des API en direct ne sont pas encore lues |
| identifiants d'unité (COLLECTE-BIS, `formes.json`) | unité non décalée, oracle croisé | ouvert (Q-S-07) ; la tranche A du collecteur (CB-0 à CB-2, `1572f50`) ne fixe pas encore les formes (CB-6 à CB-9) |
| RB-6 (rotation) | oracle croisé | autorisé à commencer (adjudication pt 3) ; aucun module `recalc` à `1572f50` [mesuré, diff des commits] |
| RB-7 (règle) | oracle croisé avant le sceau | attend la clôture de conception de SIM-NIVEAU-BIS (§5.4 pt 3) |
| Q-R-01, Q-R-02, Q-R-05, Q-R-10 | E-S-27, E-S-28, E-S-34, E-S-35 | adjugées (AVIS-C) ; Q-R-11 (analyse conditionnelle) est hors du modèle nul (E-S-22) |

## 9. Critères de sortie

1. **Par sous-lot** : suite `scripts/sim-bis` verte, plancher relevé ; suite `s2-harness` inchangée (405, OK, skipped=2) ;
   campagne de mutants conforme au contrat ; hook, gate des secrets, `cargo --locked xtask verify` verts (lignes de verdict
   seules) ; journal G1 ; ligne d'annexe A ; ligne JOURNAL.
2. **Par partie** (S-1, S-2, S-3) : relecture G2 neuve à 100 % avec checklist et enregistrement de rôle (l'enregistreur ne couvre
   pas encore `s2bis` : SHOGEN-S2BIS-ENREG-ROLE-1, annexe B.60 ; sa portée est à étendre à `scripts/sim-bis`, §12) ; corrections
   rouges avant, vertes après ; contrôle FM-1.1 des transcriptions ; revue de l'orchestrateur ; accord de l'investisseur.
3. **Lot** :
   - épinglage E0 consigné ; E1 versée et épinglée avant E2 et E3 ;
   - exécution finale A et B identiques à l'octet sur la portée adjugée ; invariance au nombre de processus ;
   - oracles internes passés (générateur, FIV, arrêt anticipé, comptages naïfs) ; oracle croisé avec RB-6 passé ; oracle avec RB-7
     passé avant le sceau, ou item SHOGEN-SIM-BIS-ORACLE-RB7-1 ouvert avec ce déclencheur ;
   - sorties versées sous `docs/adr-0029/sim-bis/` avec `SHA256SUMS` ; bloc du paquet produit ;
   - items : SHOGEN-S2BIS-SIM-1 fermé ; SHOGEN-FLUX-SERIEL-1 fermé (transposé à R1-2) ; SHOGEN-FLUX-ABSORPTION-COLLECTIVE-1 fermé
     par la décision de Q-S-15 (critère adopté par ajout daté, ou limite écrite) ; items du §12 formés ;
   - g, critère collectif et statut de la variante transmis à RECALC-BIS avant le gel de RB-5 et RB-7.
4. **G0** : cp-1 bref de ce G0 par un validateur frais avant tout code, puisque ses sorties entrent au paquet scellé.
5. **G7** : à la clôture de S2-bis.

## 10. Questions techniques (adjudication : orchestrateur ; advisors désignés)

- **Q-S-01 Emplacement.** (a) `scripts/sim-bis/` et `docs/adr-0029/sim-bis/` ; (b) `s2bis/shogen_s2bis/sim/`, dans le paquet du
  recalcul. **Recommandé : (a)**. La simulation n'est pas un maillon du chemin de recalcul ; le paquet cite son commit et ses
  sorties (forme de `scripts/sim/` en S2, G0 SIM-NIVEAU §7) ; l'indépendance vis-à-vis du code de RECALC-BIS est voulue (Q-S-02).
  [orchestrateur]
- **Q-S-02 Réplique ou import de RECALC-BIS.** (a) réplique propre, oracle croisé avec RB-6 dès son commit et avec RB-7 avant le
  sceau ; (b) import de RB-6 et RB-7 : RB-7 attend SIM-NIVEAU-BIS (adjudication du G0 de collecte, pt 3), d'où une dépendance
  circulaire ; (c) import de RB-6 seul, règle répliquée. **Recommandé : (a)** ; une réplique recoupée est aussi un second auteur
  du calcul (forme de SHOGEN-LECTEUR-INDEP-1). [orchestrateur ; STATS sur demande]
- **Q-S-03 Groupement propre à chaque unité.** (a) encadrement C0, C1, C2 par E1 ; (b) lot complémentaire PLAN-S2BIS-2, à
  `f35a70c`, scripts épinglés avant exécution : FIV_u(ℓ) par unité et loi des intervalles entre épisodes, par strate ; (c) (a),
  puis (b) seulement si W* diffère entre C0 et C2. **Recommandé : (c)**. Motif : le niveau se mesure de toute façon aux trois
  niveaux ; seule la durée retenue peut dépendre du niveau inconnu. [STATS]
- **Q-S-04 Fond de référence de la cible.** L'ADR dit à la fois « fond propre de S2 divisé par 3 (scénario B) », scénario dont
  L = 20 (l.145-154), et « L calibré sur S2 (lot PLAN-S2BIS) » pour la grille (l.158). EP donne des épisodes moyens de 1,05 à
  1,45 fenêtre en calme. (a) lettre du scénario B (L = 20, sans groupement) ; (b) fond calé par EP, groupement C2 (prudent) ;
  (c) fond calé, C1. **Recommandé : (b)**, (a) imprimé (P-L20) et (c) imprimé ; en stress, loi des longueurs regroupée sur les
  unités (épisodes complets rares, E-S-10). [STATS]
- **Q-S-05 Forme de l'incident.** Durée : (a) fixe, D fenêtres (« de 20 minutes », l.158) ; (b) géométrique de moyenne D
  (« durée moyenne 20 fenêtres », l.145). « 2 hôtes » : (c) paire tirée par incident parmi les 7 hôtes AS13335 ; (d) paire fixe
  déclarée. « Les 10 » : les dix hôtes touchés avec probabilité 1. **Recommandé : (a) et (c)**, (b) en sensibilité à la cible.
  [STATS]
- **Q-S-06 Réplications et R par famille.** (a) 10⁴ et R = 9 999 partout (plus de 1 000 h de CPU [inféré], §7) ; (b) 10⁴ et
  R = 9 999 pour les cellules nulles et la cible à la durée retenue ; 2 000 pour l'échelle, ETH, F3, la variante, les
  événements ; grille et absorption à R = 999 (seuil C ≤ 9, même α nominal (9 + 1)/(999 + 1) = 0,01) et 1 000 réplications,
  approximation déclarée (une loi de Monte-Carlo plus courte perd un peu de puissance [inféré]) ; (c) comme (b), grille à R = 9 999. **Recommandé : (b)**. Écart à
  « ≥ 10⁴ réplications » (l.384) pour les familles autres que les cellules nulles et la cible : à adjuger (§11). [orchestrateur ;
  STATS]
- **Q-S-07 Identifiants et unité non décalée.** La première unité de l'ordre alphabétique dépend des identifiants : avec des noms
  courts, binance ; avec des noms DNS, `api-pub.bitfinex.com` passe avant `api.binance.com` [calc, ordre des octets]. (a) noms
  courts ; (b) identifiants de la configuration scellée de COLLECTE-BIS. **Recommandé : (b)** à l'exécution finale, (a) à la
  provisoire. Le niveau ne dépend pas de l'unité non décalée [inféré] ; l'oracle croisé, si. [orchestrateur]
- **Q-S-08 T_début simulé.** (a) lundi 00:00 UTC fixe ; (b) jour de départ tiré par réplication. **Recommandé : (b)** : la date
  réelle est inconnue et la place des jonctions de week-end varie avec elle. [STATS]
- **Q-S-09 Variante non enroulée.** Harris [lu, pp. 1-2, 4-5] : deux séries, dont une seule doit être stationnaire (la décalée) ;
  décalages de −N à N d'un segment central de longueur T − 2N ; m = nombre de décalages (décalage nul compris) dont la statistique
  atteint celle du décalage nul ; P(m ≤ M) ≤ M/(N + 1) ; test conservatif : rejet si m ≤ α(N + 1) ; test approché : rejet si
  m ≤ α(2N + 1), deux fois plus puissant, valide quand N est grand.
  (a) **forme approchée multi-séries** : décalages indépendants tirés dans {−N, …, N} pour les neuf unités décalées, segment
  central, rang de Monte-Carlo, N = ⌊n/4⌋, sensibilité N = ⌊n/8⌋ ; c'est aussi la correction « minus » de Mrkvička et al., qui
  tient le niveau au prix de la puissance (ajout daté l.143) ; (b) test conservatif de Harris transposé : la preuve de son lemme 1
  et de son théorème 2 se transpose à une boîte de côté N + 1 en dimension 9 et donne M/(N + 1)⁹ [inféré, non publié] ; le rang
  exigé parmi les (2N + 1)⁹ vecteurs serait environ 2⁹ = 512 fois plus petit que celui du test approché, soit de l'ordre de
  0,01/512 ≈ 2·10⁻⁵, sous la résolution 10⁻⁴ d'une loi de Monte-Carlo à R = 9 999 [calc] : inapplicable avec R = 9 999, et de
  puissance très réduite [inféré] ; (c) Harris à deux séries, l'unité non décalée contre le bloc des neuf autres décalées
  ensemble : teste une autre hypothèse (l'indépendance d'une unité et du reste), pas l'indépendance mutuelle. **Recommandé :
  (a)**, (b) et (c) écartées par écrit, limite formée (SHOGEN-SIM-BIS-HARRIS-MULTI-1). [STATS]
- **Q-S-10 Portée de l'identité bit à bit.** (a) deux exécutions complètes ; (b) A complète ; B complète sur N1 et sur la cible à
  la durée retenue, et sur les 2 000 premières réplications de chaque autre cellule ; invariance au nombre de processus sur 2 000
  réplications de 4 cellules ; (c) en plus de (a) ou (b), identité sous les quatre versions de Python de l'hôte (3.10 à 3.13
  [mesuré : `/usr/bin/python3.10` à `python3.13`]) sur 200 réplications de 3 cellules, forme des tests du collecteur (49 tests
  sous Python 3.10 à 3.13, annexe B.60) : c'est ce que fera un tiers qui rejoue. **Recommandé : (b) et (c)** si le budget mesuré
  de (a) dépasse 48 h de mur, (a) et (c) sinon. Les graines par réplication rendent toute réplication rejouable seule.
  [orchestrateur]
- **Q-S-11 Couche d'observateurs sans mesure de S2-bis.** (a) grille de conception fixée ici (nominale : absences 0,5 %,
  dégradations 0,5 %, une panne de paire par mois de 60 fenêtres ; dégradée : 2 % et 2 %, perte d'un observateur, panne de paire
  par semaine) ; (b) seconde exécution calée sur les taux lus au rodage : ces taux sont interdits aux rédacteurs et validateurs
  frais du paquet (D.2-bis, l.228), et les sorties de SIM-BIS les porteraient ; (c) (a), plus un contrôle de couverture par
  l'orchestrateur seul après le rodage : « taux du rodage dans la grille : oui ou non », seul ce motif codé va au paquet ; si
  « non », SIM-BIS est rejouée sur un point plus large fixé ici (absences et dégradations à 5 %), jamais sur les taux lus.
  **Recommandé : (c)**. [OPS et STATS]
- **Q-S-12 Taux de faux écart de chemin.** (a) ε_u = (1 − f)·p̂_u(S2) : la part du bruit de S2 que la cible attribue à
  l'observateur ; (b) grille fixe {10⁻⁴ ; 10⁻³}. **Recommandé : (a)**, (a)/10 en sensibilité sur N1. [STATS]
- **Q-S-13 « Fréquence élevée de NON ÉVALUABLE »** (l.366, non chiffrée). (a) 5 % à la cible en calme ; 20 % sous H0 de référence
  (N1) en calme ; au-delà, allongement selon le §3 ; sous fond bas (N10), NON ÉVALUABLE est l'issue attendue sous H0 et
  l'allongement n'y remédie pas dans l'enveloppe acceptée : limite écrite, sans allongement, et information de l'investisseur ;
  (b) un seul seuil de 10 % ; (c) imprimer sans seuil. **Recommandé : (a)**. [STATS ; investisseur informé si allongement]
- **Q-S-14 Plancher de la durée.** (a) W = max(16, W*) ; (b) W = W*, qui peut descendre sous 16. **Recommandé : (a)** : 16
  semaines acceptées (q. 3), fond incertain ; une durée plus courte serait une économie à proposer à part. [orchestrateur]
- **Q-S-15 Critère collectif d'absorption.** (a) aucun ; limite écrite avec la courbe de puissance mesurée ; (b) candidat E-S-35
  adopté par ajout daté au §2.5 de l'ADR si l'exécution provisoire montre un gain de puissance sans perte de niveau ; (c) seuil par unité
  resserré. **Recommandé : mesurer (a) et (b)** à l'exécution provisoire, décision de l'orchestrateur avant le gel de RB-5 et
  RB-7 (Q-R-10), (a) par défaut. Le critère lit les écarts consolidés, pas seulement les « ok », pour couvrir aussi le cas d'une
  source à « ok » élevé et à écarts fréquents (SHOGEN-FLUX-DEVIANT-1, l.556). [STATS]
- **Q-S-16 Lieu et seuil du calcul.** (a) hôte de session, lots détachés ; (b) poste de l'investisseur (acte ; Windows, bash :
  SHOGEN-HARNAIS-BASH-WSL-1) ; (c) serveur loué quelques heures (prix à lire avant, acte de l'investisseur). **Recommandé : (a)** ;
  (c) proposé seulement si le budget mesuré dépasse 72 h de mur, avec un prix lu le jour même. [orchestrateur ; investisseur]
- **Q-S-17 Exécution provisoire, puis finale.** (a) une seule exécution, après le gel des pools ; (b) provisoire sur le pool de
  l'ADR pour clore la conception et débloquer RB-7, finale épinglée après le gel. **Recommandé : (b)** ; la finale ne diffère que
  par les pools, les identifiants et ce qui en dépend (sous-ensemble AS13335 si une unité sort) ; tout autre changement est une
  déviation déclarée. [orchestrateur]
- **Q-S-18 Tolérance g du compte d'événements.** (a) g de puissance maximale à la cible parmi {0 ; 5 ; 20 ; 60}, à égalité le plus
  petit ; (b) g = 20, durée de la cible, sans mesure. **Recommandé : (a)**. [STATS]
- **Q-S-19 Sensibilités simulées en plus de S et de la variante.** (iii) rotation par jours entiers ; (iv) M_j = M seulement ;
  (vii) « USD seules ». **Recommandé** : (vii) en puissance à la cible (imprimée avec le verdict, l.212), (iii) en niveau sur N1 et
  N3 ; (iv) non (elle change l'échantillon, pas la loi). [STATS]
- **Q-S-20 CI.** (a) job `sim-bis-unittest` sur l'image épinglée, calqué sur `s2bis-unittest` (ajouté par CB-0b) : même
  vérificateur paramétré, qui prend le dossier en argument (`enforcement/verdict-suite-s2.py scripts/sim-bis --aucun-saut --egal
  --plancher N`, usage lu l.13) ; le cas K-02 du runner, qui lit les étapes des jobs, est à étendre (SHOGEN-CI-S2-CABLAGE-1) ;
  (b) tests rejoués par l'orchestrateur seulement, forme de `scripts/plan-s2bis/`. **Recommandé : (a)** : on serre ; et la consigne
  SHOGEN-S2BIS-G3-LIGNE-JOB-1 (annexe B.60) vaut aussi pour ce job tant que la forge ne lance pas les jobs. [orchestrateur]
- **Q-S-21 Hors-enveloppe dû aux τ re-dérivés.** Les taux d'EP sont classés sous les τ et σ committés de S2 (EP l.12) ; les τ
  re-dérivés pour S2-bis sont plus bas pour trois classes sur quatre (agrégateurs 1,1 % contre 2,6 % ; Chainlink 0,9 % contre
  1,65 % ; places horodatées 0,2 % contre 0,45 %, `tau_sigma.txt` l.13-58). (a) composante additionnelle encadrée {0 ; 2,5·10⁻⁴ ;
  10⁻³} [inféré : un τ à 1,5 × P99,9 laisse au plus de l'ordre de 10⁻³ des cellules au-delà, sur S2] ; (b) l'ignorer. **Recommandé :
  (a)**, 2,5·10⁻⁴ à la référence. [STATS]
- **Q-S-22 Simplifications.** Deux types (panne, écart non-panne) ; classe « borné » et P_j hors du modèle nul. **Recommandé :
  oui**, écrit au paquet. [STATS]

**Advisors proposés** : STATS : Q-S-03, Q-S-04, Q-S-05, Q-S-06, Q-S-08, Q-S-09, Q-S-11, Q-S-12, Q-S-13, Q-S-15, Q-S-18, Q-S-19,
Q-S-21, Q-S-22 ; OPS : Q-S-11 ; l'orchestrateur seul : Q-S-01, Q-S-02, Q-S-07, Q-S-10, Q-S-14, Q-S-16, Q-S-17, Q-S-20.

## 11. Écarts à la lettre de l'ADR, signalés et non appliqués

| où | lettre de l'ADR | écart proposé | question |
|---|---|---|---|
| l.384 | « ≥ 10⁴ réplications » | 10⁴ pour les cellules nulles et la cible ; moins ailleurs | Q-S-06 |
| l.158 | cible = scénario B (L = 20) ; grille à « L calibré sur S2 » | fond calé par EP, groupement C2 ; L = 20 imprimé | Q-S-04 |
| l.141, l.205 | « variante non enroulée de Harris » | forme approchée multi-séries ; le test conservatif de Harris n'est pas transposable utilement | Q-S-09 |
| l.366 | « fréquence élevée » non chiffrée | 5 % et 20 % ; limite sous fond bas | Q-S-13 |
| l.158 | « valeurs finales fixées par SIM-PUISSANCE-BIS » | plancher de 16 semaines ; au-delà, acte de l'investisseur | Q-S-14 |
| l.443 | SHOGEN-S2BIS-SIM-1 remplace aussi la simulation de taille de pool de P6 | pool fixé à 10 : aucune cellule à 15, 20 ou 25 unités | §1.3 |
| l.310 | « simulations ≈ 400 lignes » | environ 2 450 lignes avec tests | §6.1 |

## 12. Items à former (règle PAROXYSME)

| item | constat | construction | prix [inféré] | déclencheur |
|---|---|---|---|---|
| SHOGEN-SIM-BIS-FIV-IDENTIF-1 | le groupement propre à chaque source n'est pas identifiable depuis les sorties de PLAN-S2BIS (un seul indicateur, I_t, d'un observateur unique) | encadrement E1 ; lot PLAN-S2BIS-2 (FIV_u(ℓ), intervalles entre épisodes) | ≈ 150 lignes et un passage épinglé sur les journaux | W* différente entre C0 et C2 |
| SHOGEN-SIM-BIS-OBS-GRILLE-1 | couche d'observateurs calée sur une grille de conception, sans mesure | contrôle de couverture par l'orchestrateur après le rodage, motif codé au paquet | une lecture de classe M | fin du rodage |
| SHOGEN-SIM-BIS-HARRIS-MULTI-1 | la borne conservative de Harris ne se transpose pas utilement à neuf décalages indépendants ; la variante approchée n'a qu'une validité asymptotique | mesure de son niveau (E-S-33) ; limite écrite | aucun | sortie de SIM-NIVEAU-BIS |
| SHOGEN-SIM-BIS-ORACLE-RB7-1 | l'oracle croisé avec RB-7 n'est possible qu'après RB-7, qui attend SIM-NIVEAU-BIS | SB-13, seconde passe | ≈ 40 lignes | commit de RB-7, avant le sceau |
| SHOGEN-SIM-BIS-FOND-BAS-1 | sous fond consolidé bas, NON ÉVALUABLE est l'issue attendue sous H0 ; l'allongement n'y remédie pas dans l'enveloppe | limite écrite ; information de l'investisseur | aucun | sortie de N10 |
| SHOGEN-SIM-BIS-CALCUL-1 | 90 à 155 h de CPU sur un hôte éphémère à 4 vCPU, partagé avec d'autres workers ; perte possible d'un lot | versement par phase ; lots reprenables ; option payante en question de valeur | 0 € sur l'hôte de session | plan de lots du G1 |
| SHOGEN-SIM-BIS-TAU-NEUF-1 | taux d'écart de S2 mesurés sous les τ et σ de S2, plus hauts que ceux de S2-bis pour trois classes | composante encadrée (Q-S-21) | aucun | sortie de SIM-PUISSANCE-BIS |
| SHOGEN-SIM-BIS-STRESS-EPISODES-1 | épisodes complets rares en stress (2 à 8 pour quatre unités) | loi regroupée (E-S-10) ; limite écrite | aucun | sortie d'E1 |

Extension de portée proposée pour un item existant, sans item neuf : SHOGEN-S2BIS-ENREG-ROLE-1 (annexe B.60 : l'enregistreur
`s2-harness/tools/oracle_record.py` ne couvre pas `s2bis`) couvre aussi `scripts/sim-bis` ; même déclencheur, avant la G2 de la
partie S-1. Et SHOGEN-S2BIS-P1-ESTIMATION-1 (même bloc) s'applique à l'estimation de taille du §6.1.

Aucune limite rencontrée n'est laissée sans item. Aucun procurement n'est demandé : les trois sources de la méthode sont détenues
depuis 22:10 UTC.

## 13. Actes de l'investisseur (en langage clair)

- **A-1 Accords.** Donner votre accord une fois par partie (trois parties). Aucune question technique ne vous est posée.
- **A-2 Durée, seulement si la simulation le montre.** Si la simulation montre que 16 semaines de mesure ne suffisent pas à
  détecter l'incident visé avec 80 % de chances, on vous demandera de choisir, avant le scellement, entre une mesure plus longue
  (coût et date chiffrés) et une mesure de 16 semaines moins puissante, dite telle quelle dans le rapport.
- **A-3 Calcul, seulement si nécessaire.** Si le calcul dépasse ce que la session peut faire en temps raisonnable, on vous
  demandera de choisir entre attendre (gratuit) et louer un serveur quelques heures (prix lu et donné avant). Sans votre accord
  écrit, aucune dépense.

## 14. Provenance

**Pièces lues dans le dépôt** [lu] (préfixes de sha256 à `b9ba2b4`, sauf mention) :
- `CLAUDE.md` (`04200485…`, contexte de session) ; `docs/PASSATION-CLOUD.md` (`c7d40a0f…`), en entier ;
- ADR-0029 (`22474146…`), en entier à `b742e3c` (l.1-565), puis le diff `b742e3c..b9ba2b4` (ajout daté l.143, lu en entier) ;
- `docs/adr-0029/G0-lots-S2BIS.md` (`db49d5f2…`) et `docs/adr-0029/G0-lot-PLAN-S2BIS.md` (`81bf3f33…`), en entier ;
- `docs/adr-0029/g0-collecte/PROPOSITION.md` (`0cdf84c2…`), en entier ; `AVIS.md` (`a919b307…`), en entier ;
  `G0-COLLECTE-RECALC-DEPLOI.md` (`56f9ca73…`), en entier ;
- `docs/adr-0029/plan-s2bis/` : `README.md` (`93fd70c2…`), `SHA256SUMS` (`f21f9293…`), `tau_sigma.txt`, `episodes.txt`, `okx.txt`
  (sha256 égaux à `SHA256SUMS` [mesuré]), en entier ; `G1-lot-PLAN-S2BIS.md` (`cb9d1be0…`), en entier ; `G2-lot-PLAN-S2BIS.md`
  (`7fc6b8a8…`), lignes trouvées par recherche et l.74-90 ;
- `scripts/plan-s2bis/README.md` (`e3cfa68b…`, égal à l'épingle du JOURNAL) et `episodes.py` (`90c7842d…`, égal à l'épingle), en
  entier ;
- `docs/adr-0029/AVIS-STATS.md` (`52a1a69b…`), `AVIS-QUESTIONS-TECHNIQUES-V3.md` (`836ece5e…`), `DECISIONS-ARCHITECTURE-S2BIS.md`
  (`603abda2…`), `CONTRE-EXPERTISE-DECISIONS.md` (`79618e48…`), en entier ;
- `docs/adr-0029/etude-marche/P6-MESURE.md` (`1167e605…`), en entier ;
- annexe B d'ADR-0028 (`b4a43c2b…`) : l.101, l.547-558, l.855-880, l.956-973, et les lignes des items par `grep -n` dans ce seul
  fichier ; annexe D (`deb64179…`) : l.30-51 (liste D.2 : noms seulement, aucune pièce ouverte) ;
- `docs/adr-0028/G0-lot-SIM-NIVEAU.md` (`1da137e6…`), en entier (modèle de discipline) ; `docs/adr-0028/sim-dettes/flux.txt`
  (`6341ec1d…`), l.1-40 ;
- `docs/adr-0029/calib/SOURCES-HISTORIQUES.md` (`f649e30f…`) : l.1-40 et l.178-184 ; `docs/adr-0029/ETUDE-POOL-BIS.md`
  (`d3780f13…`) : lignes de « AS13335 » par recherche ; `docs/11-mesures-pilotes.md` (`fcf93b87…`) : lignes de « AS13335 » par
  recherche, et l.354-358 (partition de S2) ;
- `JOURNAL.md` : l.396-428 à `b742e3c`, puis les diffs jusqu'à `b9ba2b4` (l.429-430) et jusqu'à `1572f50` (l.431-432) ;
  `docs/METHODE-PARTIES.md` (`609b500d…`) : l.30, l.39 par recherche ; `.github/workflows/gates.yml` : lignes de « unittest » et
  « python » par recherche, puis le diff `b9ba2b4..1572f50` (job `s2bis-unittest`) ; `biblio/INDEX.md` : diff de `b9ba2b4` et
  recherche de « harris », « kalyuzhny », « mrkvi », « rotation ».
- Après la reprise (tête `1572f50`) : annexe B l.991-1014 (B.60), en entier ; `enforcement/verdict-suite-s2.py` l.1-20 et l.55-70
  (usage et arguments).

**Sources de la méthode** [lu] (`biblio/`, versées à 22:09 UTC) :
- Harris, *A Shift Test for Independence in Generic Time Series*, arXiv:2012.06862v1 (PDF sha256 `f69b1324…1635` [mesuré], égal à l'index) : pp. 1
  à 6 lues en entier sur le PDF (cadre du test, exemple, discussion, lemme 1, théorème 2, corollaire, théorème 3). Paraphrasé, non
  cité.
- Mrkvička et al., arXiv:1911.00240v1 : sidecar (`c771b8b8…`) l.108-130 (libéralité de la correction torique, échangeabilité),
  l.146-154 (portée de dépendance longue), l.275-312 (corrections torique, « minus » et de variance) et l.792-806 (taux de rejet
  de la correction torique selon la portée, p. 17), plus recherche de « toroidal », « minus », « liberal », « scale parameter ».
  Paraphrasé.
- Kalyuzhny, manuscrit d'auteur accepté, extraction texte (`0e838f40…`) : l.240-260 (algorithme), l.320-392 (autocorrélation et
  enroulement), l.423-460 (erreurs de première espèce), plus les lignes trouvées par recherche (l.104-123, l.496-514). Paraphrasé.

**Mesures** [mesuré, 2026-10-04, hôte de session, Python 3.11.15, 4 vCPU, `nproc` = 4] :
1. `git rev-parse HEAD` : `b742e3c…` au début, `b9ba2b4…` à 22:14 UTC, `1572f50…` à 22:43 UTC ; `git status --short` vide à
   chaque relevé ; `git diff --stat b742e3c b9ba2b4` : 3 fichiers (JOURNAL, `biblio/INDEX.md`, ADR-0029) ; `git log
   b9ba2b4..1572f50` : 10 commits ; `git diff --stat b9ba2b4 1572f50` : 28 fichiers ; parmi les fichiers que ce G0 cite par
   numéro de ligne, seuls l'annexe B et le JOURNAL y changent (ajouts en fin), et `enforcement/verdict-suite-s2.py`, lu à `1572f50`.
2. `sha256sum` des trois sorties de PLAN-S2BIS : égaux à leur `SHA256SUMS`.
3. Suite `s2-harness` (`env -u SHOGEN_S2_CAMPAGNE_CONTROL`, `TMPDIR` dans le dossier du lot, `python3 -B -m unittest discover -s
   tests -t .`) : « Ran 405 tests in 46.781s », « OK (skipped=2) » (22:20:53 à 22:21:41 UTC).
4. Sondes de temps, hors dépôt, dans `scratchpad/s2bis/sim-g0/mesures/` ; elles n'implémentent pas la règle et n'impriment aucun
   taux de rejet ; aucun octet de barre oblique inverse, de tabulation ni de retour chariot [mesuré] :
   - `sonde_temps.py` (`bf0fec55…2a6f`), sortie `sonde_temps.out.txt` (`f10d5f5f…07fb`), 22:05 UTC ; contrôle interne : K et S par
     tranches, par paires et naïfs égaux sur une série de 3 000 fenêtres ;
   - `sonde_chaine.py` (`8782a9a6…023d`), sortie `sonde_chaine.out.txt` (`57ac5824…fcc1`), 22:17 UTC.
5. `calc_g0.py` (`268050af…ba35`), sortie `calc_g0.out.txt` (`e3a645b1…38dd`) : les [calc] de ce G0 (taux d'EP recomptés depuis
   les comptes de cellules, P_more de Poisson-binomiale exacte, échelle des durées, incidents attendus, arrêt anticipé, borne
   x ≥ 122, probabilité de phrase par hasard, ordre des identifiants). Calculs de tête, vérifiables sur la page : 2 450 × 1,78 ≈
   4 360 et 2 450 × 2 = 4 900 ; 0,01/512 ≈ 1,95·10⁻⁵ ; 1/(9 999 + 1) = 10⁻⁴.
6. `ls /usr/bin/python3*` : interpréteurs 3.10, 3.11, 3.12 et 3.13 présents (Q-S-10 c) ; après la reprise, sha256 des six
   fichiers de `mesures/` et du brief recontrôlés égaux aux valeurs ci-dessus.

**Non ouverts** : `docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`,
`docs/adr-0028/execution/`, tout `*.jsonl`, toute pièce de la liste D.2, le rendu J28, le JOURNAL hors l.396-432. Aucune recherche
récursive sur `docs/`. `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée. Le dossier de travail de la procuration parallèle
(`scratchpad/s2bis/biblio-rot/`) a été listé (noms de fichiers, `ls`) avant le versement, aucun contenu ouvert.

**Exposition** : valeurs de S2 post-rendu portées par l'ADR §1.1 et par les sorties de PLAN-S2BIS (taux par unité, épisodes, FIV,
τ et σ re-dérivés), et la partition AS13335 du rapport de S2 ; aucune donnée de S2-bis n'existe. Aucune valeur de seconde main
n'entre dans un chiffre de ce G0, sauf la garantie de stabilité de `random()` (E-S-42), marquée [2nd].

**Réviseur attendu** : l'orchestrateur et les advisors désignés, puis un validateur frais pour un cp-1 bref (proposition). Le
rédacteur n'a généré aucun des lots qu'il décrit.
