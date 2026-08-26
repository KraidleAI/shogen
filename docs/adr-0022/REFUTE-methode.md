# S2 Shōgen — Réfutation MÉTHODE & RÉGIME de la sélection de τ par classe (ADR-0022)

**Nature** : donnée brute pour l'orchestrateur (vérification adversariale R-21). Attaque la
RÈGLE de sélection des τ et les choix de conception — PAS l'arithmétique des P99/percentiles
(revue par un autre worker). Chaque affirmation porte sa preuve reproductible.

| champ | valeur |
| --- | --- |
| Rôle | RÉFUTANT méthode & régime (worker épinglé) |
| Modèle résolu | `claude-opus-4-8[1m]` (effort max) — Gate 0 R-1 conforme (préfixe `claude-opus-4-8`) |
| Date | 2026-08-26 |
| Contexte | Révision de τ (écart RELATIF de concordance inter-sources) par ADR-0022 ; τ par classe |
| Discipline | lecture seule ; écriture SEULE dans `scratchpad\tau-facts\` ; aucun commit (R-20) |
| Artefacts lus | `derive_tau.py` (règle+table) ; `F1-F2.md` (P99/strate, épisodes) ; `r1.py` (classify_ecart) ; `r2.py` (drapeau_2/φ) ; `closure.py` (tau_revision_needed) ; `oracle-research\TAU-recherche.md` (faits externes Q1–Q6, sibling [lu]) |
| Sondes rejouables | `derive_tau.py` (table de décision) ; `refute_probe.py` (max/strate, sensibilité budget, plancher grille, marges) — mêmes machineries `shogen_s2` revues, lecture seule |
| Commande de relance | `python "C:\Users\KACIMI\AppData\Local\Temp\claude\F--Shogen\90684fb2-4e7b-42e9-b820-f042dc4465f3\scratchpad\tau-facts\refute_probe.py"` |

**Provenance des chiffres.** Internes (P99/max par strate, épisodes, sensibilité budget) =
[lu], ma ré-exécution de `derive_tau.py` + `refute_probe.py` sur la machinerie `shogen_s2`
déjà revue (reproductible, commande ci-dessus). Externes (Chainlink 0,5 % ; USDe 0,65 %/4,3 % ;
CAPO 2,85 % ; SPC/EVT/FDR) = cités via `TAU-recherche.md` (sibling que je lis directement,
[lu]) AUX NIVEAUX QU'IL DÉCLARE — pour moi ce sont des entrées de la dérivation que je
critique, non des faits que je re-primarise ; l'orchestrateur les revérifie sur cet artefact.

---

## Résultat structurel dominant (sous-tend les 4 attaques)

`ep26j = 13 × ep48h` (`CALIB_TO_CAMPAIGN=13`, derive_tau l.33) et le budget est un compte
ENTIER d'épisodes ⟹ **`budget ≤ 4` ⟺ `ep48h = 0`** (car 13×1 = 13 > 4). Le compte d'épisodes
est agrégé sur les DEUX strates (`flux_devs`, derive_tau l.114/128-130). Donc, pour toute
classe « quantile », le τ sélectionné = **le plus petit point de grille strictement au-dessus
du max honnête observé sur 48 h (sur les deux strates)** = `grid-ceil(max_both)`. Vérifié :
dans la table, chaque τ CHOISI est exactement la ligne où `ep48h` passe de ≥1 à 0
(place 0,25 %→ep48h 1, 0,30 %→0 ; sans 0,25 %→7, 0,30 %→0 ; agregateur 1,10 %→5, 1,75 %→0).

Conséquence : l'appareil « borne de fausse-alarme Clopper-Pearson × projection d'épisodes ×
budget 4 » ne fait AUCUN travail que « grid-ceil(max_both) » ne ferait — il s'effondre
arithmétiquement sur cette seule règle. Les leviers de conception RÉELS, non nommés dans
l'ADR, sont : (a) le **plancher de grille** (0,15 %), (b) le **pas de grille** (0,05 %),
(c) le choix d'exiger **zéro** épisode 48 h plutôt que d'en tolérer 1–2.

---

## ATTAQUE 1 — Le budget de 4 épisodes/classe/26 j : justifié ou arbitraire ?

### DÉFATEUR 1a (provenance R-21) — la règle ÉNONCÉE ≠ la règle CODÉE ; la chaîne de justification affirme faussement une borne CP

La borne de Clopper-Pearson **n'est pas câblée dans la sélection**. Dans `derive_tau.py` :
- l.172 `cpu = cp_upper(k, N, float(CP_ALPHA))` — calculée ;
- l.176 `okbudget = ep26 <= BUDGET_EPISODES` — le gate teste `ep26` (compte BRUT), pas `cpu` ;
- l.179 `if chosen is None and okq and okbudget and okcapo:` — **aucune référence à `cpu`** ;
- l.183 `{cpu*100:8.4f}` — `cpu` n'apparaît QUE dans l'impression de la table ;
- l.187-188 justification émise par classe : `"borne CP episodes26j <= {BUDGET_EPISODES}"`.

`cpu` (borne sup CP sur la **probabilité** d'excès par fenêtre `k/N`) et `ep26` (**compte**
d'épisodes projeté) sont deux grandeurs distinctes. Le gate utilise `ep26` ; la justification
émise NOMME « borne CP episodes26j ». La docstring (l.7-9) présente de même la borne CP comme
LA borne de fausse-alarme opérante. **L'artefact revendique une preuve (borne CP sur les
épisodes) qu'il n'applique pas** — défaut R-21 direct, vérifiable au regard.

**Correction** : soit câbler réellement la borne CP dans le gate (et alors la justifier comme
telle), soit réécrire la docstring + les chaînes de justification pour dire ce que le code fait
— « τ = plus petit point de grille au-dessus du max honnête 48 h sur les deux strates, sous
CAPO ». **Sans la borne CP, la règle est `grid-ceil(max_both)`, à assumer telle quelle.**

### DÉFATEUR 1b (chiffre nu en position porteuse, doc 03) — pyth τ = plancher de grille, non calibré

`GRID = range(15, 305, 5)` (l.38) : la grille DÉMARRE à 0,15 %. Pour pyth (`max_both` = 0,0746 %),
τ=0,15 % est CHOISI dès la première ligne (ep48h=0 déjà), donc **pyth est fixé par le plancher
de grille, pas par sa donnée**. Sonde (refute_probe P3) :

| plancher de grille | τ pyth obtenu |
| --- | --- |
| 0,05 % | **0,10 %** |
| 0,10 % | **0,10 %** |
| 0,15 % | **0,15 %** (valeur recommandée) |

La valeur pilotée par la donnée (`grid-ceil(max_both 0,0746 %)`) est **0,10 %**. Le 0,15 %
recommandé est +50 % au-dessus, entièrement dû au plancher arbitraire. La classe la plus
critique (l'oracle) a son τ déterminé par une **valeur nue** (aucun commentaire ne justifie
« 15 » dans `range(15,…)`), et le label émis « [quantile] » (l.186) est trompeur : ni le
quantile ni le budget ne lient — seul le plancher lie.

Sous la règle Dettes/zéro-dette, un plancher non sourcé qui détermine à lui seul le τ d'une
classe critique **ne peut pas être porté tel quel**. Correction **binaire, chiffrée des deux
côtés** :
- **soit** adopter `τ_pyth = 0,10 %` (piloté par la donnée) ;
- **soit** sourcer un plancher de robustesse microstructure ~0,15 %. `TAU-recherche.md`
  fournit des ancres CANDIDATES (à adopter explicitement dans l'ADR, pas laissées implicites) :
  Chaos Labs « fee floor » DEX ≈ 5 bps = 0,05 % (Q4, cible d'exactitude) ; Chainlink Base
  ETH/USD seuil 0,15 % (Q1) ; σ/μ interne Pyth live 0,03–0,04 %, exemple doc ~0,1 % (Q2).
  Un plancher 0,15 % ≈ 2× le plafond de bruit interne Pyth se DÉFEND — mais doit être ÉNONCÉ.

### ENTÉRINÉ — la valeur « 4 » elle-même est inoffensive dans son plateau

Sensibilité au budget (refute_probe P1 ; `floor(B/13)` épisodes 48 h tolérés) :

| classe | B=1 | B=4 | B=10 | B=12 | B=13 | B=20 | B=26 | B=39 | B=52 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| oracle_pyth | 0,15 | 0,15 | 0,15 | 0,15 | 0,15 | 0,15 | 0,15 | 0,15 | 0,15 |
| place_horodatee | 0,30 | 0,30 | 0,30 | 0,30 | 0,25 | 0,25 | 0,20 | 0,20 | 0,20 |
| sans_horodatage | 0,30 | 0,30 | 0,30 | 0,30 | 0,30 | 0,30 | 0,30 | 0,30 | 0,30 |
| agregateur | 1,75 | 1,75 | 1,75 | 1,75 | 1,75 | 1,75 | 1,60 | 1,25 | 1,20 |

`B ∈ {1,4,10,12}` donnent des τ **identiques** (plateau `ep48h=0`). Rien ne bouge avant `B≥13`
(≥1 épisode 48 h toléré). Donc « 4 » est arbitraire MAIS inoffensif : « 1 » ou « 12 » donnent
la même réponse. Ce n'est PAS le budget qui pilote — c'est la **quantification entière ×13**
(un épisode 48 h est tout-ou-rien). **Réserve** : nommer dans l'ADR que le vrai choix n'est pas
« 4 » mais « zéro épisode 48 h » ; s'il fallait un vrai budget probabiliste, il faudrait une
grille fine ET un budget en excès ATTENDU (pas en épisodes entiers), sinon ×13 domine.

### Règle plus principielle ? — le canon a été considéré et écarté À BON DROIT

`TAU-recherche.md` Q6 établit ([lu] NIST/SEMATECH primaire) la règle canonique k·σ/ARL
(k=3 → ARL₀≈371 sous **normalité**). derive_tau l.9 la REJETTE explicitement (« pas de normal
k-sigma car queues lourdes — max 1,73 % vs P99 0,375 % ») — rejet **sourcé et correct** (queues
crypto lourdes). EVT/POT (Coles 2001) non requis à N≈34 500 (quantile empirique solide jusqu'à
P99,95, Q6). FDR/BH = mauvais cadre (τ n'est pas un lot de p-valeurs simultanées, Q6). **Je ne
demande donc PAS de règle « principielle » de taux de fausse-alarme** — l'inapplicabilité est
documentée. La critique 1 se réduit à 1a (self-description) + 1b (plancher/pas non sourcés).

**PORTÉE attaque 1** : les 5 VALEURS restent debout SAUF pyth (0,10 % vs 0,15 % — décision à
prendre). Ce qui est invalidé = la **narration/provenance** (« borne CP », « budget 4 »,
label « [quantile] » sur pyth). Correction = réécrire la règle comme `grid-ceil(max_both)` +
plancher sourcé, ou câbler la CP.

---

## ATTAQUE 2 — RÉGIME : calibrer sur la strate « lâche » (calme), n=1 j/régime, étiquettes inversées

### DÉFATEUR 2 (concret) — le max honnête RAPPORTÉ est pris sur la MAUVAISE strate pour 2 classes sur 5

`derive_tau` choisit la strate « lâche » par le **P99** (`looser_strate`, l.119-125) puis lit le
max SUR CETTE SEULE strate (`maxdev = max(dev_sc[st][klass])`, l.147). Or P99 et MAX ne
désignent pas la même strate. Sonde (refute_probe P2) :

| classe | max calme % | max stress % | max_both % (porteur) | max RAPPORTÉ par derive_tau |
| --- | --- | --- | --- | --- |
| oracle_pyth | 0,0746 | 0,0691 | 0,0746 (calme) | 0,0746 ✔ |
| place_horodatee | 0,1568 | **0,2794** | **0,2794 (STRESS)** | **0,1568 — SOUS-ESTIMÉ** |
| sans_horodatage | 0,2962 | 0,2611 | 0,2962 (calme) | 0,2962 ✔ |
| agregateur | 1,7319 | 1,7296 | 1,7319 (calme) | 1,7319 ✔ |
| oracle_chainlink | 0,8969 | **1,0946** | **1,0946 (STRESS)** | **0,8969 — SOUS-ESTIMÉ** |

Pour **place_horodatee** et **oracle_chainlink**, le max honnête réel vit sur STRESS, pas sur
la strate lâche-par-P99 (calme). Le max rapporté sous-estime : place 0,1568 → **0,2794**
(vrai max = 1,78× le rapporté) ; chainlink 0,8969 → **1,0946**. Conséquences directes :
- la **marge** annoncée pour place (τ/max = 0,30/0,1568 = 1,91×) est ILLUSOIRE ; la vraie marge
  sur le max réel est **0,30/0,2794 = 1,074×**. L'orchestrateur lisant la table croirait ~2× là
  où il y a 1,07× ;
- le `k` de la borne CP (l.171, `d > tau` sur la strate lâche SEULE) sous-compte les excès de
  stress — cohérent avec 1a : la CP est doublement inopérante (non câblée ET calme-seule).

Les τ **valeurs** survivent (le budget agrège les deux strates ⟹ τ CHOISI > max_both toujours :
place 0,30 > 0,2794 ✔, chainlink 1,30 > 1,0946 ✔), mais c'est un **sauvetage accidentel** par
l'agrégation du budget, pas par la règle énoncée. La règle « calibrée sur la strate la plus
lâche » (l.6/143) est **non fondée** : « plus lâche » par P99 n'est pas « max ».

**Prémisse du brief testée (2c).** Le brief supposait « des lectures > τ apparaissent côté
stress ». Testé : au τ CHOISI c'est **FAUX** (ep48h=0 sur les DEUX strates par construction —
aucune lecture > τ, ni calme ni stress). La prémisse n'est vraie qu'au niveau du **MAX** (la
strate stress PORTE le max honnête pour place et chainlink) — c'est le sens exact du défateur 2,
et c'est ce niveau-là, pas des dépassements du τ choisi, qui fonde l'attaque.

**Correction** : prendre le **max honnête sur les DEUX strates** explicitement pour la borne
et pour les marges rapportées ; recalculer les marges (place tombe à 1,07×, chainlink cadré sur
son max stress 1,0946 % < ancre 1,29 %).

### RÉSERVES de régime à porter dans l'ADR (concrètes)

- **n = 1 jour par régime.** F1-F2.md : la fenêtre = un seul vendredi (calme, 1440 fen.) + un
  seul samedi (stress, 1440 fen.). Les P99/max sont des estimateurs **d'un jour**. Un τ à
  marge ~1,01× (voir attaque 4) sur un max d'UN jour est à un mauvais jour de campagne d'un
  dépassement honnête non prévu par le « 0 épisode ».
- **Étiquettes calendaires empiriquement INVERSÉES et NON MONOTONES.** L'étiquette ex ante
  « week-end = stress = plus lâche » est fausse sur cette fenêtre : P99 calme 0,414 % > stress
  0,326 % (F1). Pire, la relation n'est même pas cohérente en interne : le MAX vit sur stress
  pour 2 classes (ci-dessus). Le concept de « strate lâche » n'est donc PAS robuste ; s'appuyer
  dessus pour choisir la strate de calibration est fragile.
- **Projection 26 j incluant ~8 jours de « stress » à partir d'1 jour échantillonné.** La
  campagne = 26 j dont 4 week-ends. Le ×13 suppose que le comportement d'excès honnête des 48 h
  représente 26 j, alors qu'UN SEUL jour de week-end est échantillonné. Extrapolation à nommer.

### CORRECTION concrète (machinerie existante, pas un processus inventé)

`closure.tau_revision_needed` existe et est **fail-closed** (closure.py l.169-176 : `tau_classe
= None` si révision requise — « une révision de τ est une DÉCISION ADR, jamais devinée »).
Véhicule proposé : mandater dans l'ADR une **re-dérivation à checkpoint en cours de campagne**
(p. ex. après le PREMIER week-end réel, quand un 2ᵉ échantillon de jour-stress existe), via ce
hook ; traiter **tout** dépassement honnête au τ choisi pendant la campagne comme déclenchant la
clause de révision. La fragilité n=1 j devient une réserve MITIGÉE par l'existant.

**PORTÉE attaque 2** : les 5 τ **valeurs** restent debout (elles franchissent max_both sur les
deux strates). Ce qui est invalidé = le **max/les marges RAPPORTÉS** pour place & chainlink
(recalcul sur deux strates dû) + la **règle énoncée** « strate la plus lâche ». Réserves de
régime + tripwire `tau_revision_needed` à inscrire dans l'ADR.

---

## ATTAQUE 3 — PAR CLASSE vs SCALAIRE : défateur concret ?

### ENTÉRINÉ — aucun défateur ; le par-classe est mécaniquement NÉCESSAIRE

**Acte d'accusation chiffré du scalaire (F2, en main).** Le τ scalaire **actuellement committé**
= 0,50 % (F1-F2.md). À 0,50 %, F2 rapporte **110 lectures honnêtes → 61 épisodes / 48 h** ⟹
**13×61 = 793 épisodes de faux-drapeau honnête projetés / 26 j**, concentrés sur coingecko
(9 ép.), defillama (21 ép.), chainlink (31 ép.) = 61 — toutes des sources HONNÊTES dont le
plancher de bruit dépasse 0,50 %. Le scalaire n'est pas « théoriquement » mauvais : le scalaire
committé projette ~793 faux drapeaux. Le τ par classe (chaque τ > le max de sa classe ⟹ 0
épisode honnête 48 h) les élimine par construction.

**Le scalaire échoue des DEUX côtés (hétérogénéité de bruit ×23).** Plancher de bruit honnête :
pyth `max_both` 0,0746 % vs agregateur 1,7319 % = facteur **23×**.
- Scalaire serré (0,30 %, valeur place/sans) : agregateur (P99 calme 0,72 %) « en écart »
  honnêtement dans >1 % des fenêtres → matrice φ et z-score saturés de bruit → drapeau_2
  faux-positif.
- Scalaire large (1,75 %, valeur agregateur) : pyth devrait dévier **>23× son max honnête** pour
  s'allumer → l'oracle devient invisible à la co-défaillance ; une manipulation pyth de 1 %
  (13× sa déviation normale) ne s'enregistrerait pas.

Le par-classe rend « en écart » = « au-delà du plancher honnête PROPRE à la classe », de sorte
que le test de co-défaillance (z-score pool) et la matrice φ ont un taux de base honnête ~0 par
classe **par construction** (chaque τ est grid-ceil de son max ⟹ 0 épisode 48 h). C'est la
condition d'un test de co-aberrance bien calibré. **Ancrage incident réel** (TAU-recherche.md
Q4, LlamaRisk USDe [lu-extrait]) : pendant le dépeg USDe, Chainlink a dévié 0,65 % — jugé « bien
dans les paramètres de sécurité » (SÛR) — tandis que Pyth a dévié 4,3 %. Un scalaire ne peut
distinguer « 0,65 % chez chainlink = latence sûre » de « 0,65 % chez un exchange = anomalie » ;
le par-classe le fait (chainlink τ=1,30 % tolère sa latence sûre ; place/sans τ=0,30 % signalent
un 0,65 % d'exchange, anormal pour leur classe). C'est un argument DIRECT et daté pour le
par-classe.

### Complexité / interprétabilité de la matrice φ : réserve, pas défateur

- **Coût d'implémentation FAIBLE.** `classify_ecart` prend aujourd'hui un τ **SCALAIRE**
  (r1.py l.121 ; l.166 `abs(price - m_loo) / m_loo > tau`). Le par-classe exige de threader une
  **carte τ par σ-classe** à travers `classify_ecart → classify_cells → compute_r1/compute_lm/
  compute_r2` — MAIS c'est EXACTEMENT le patron déjà en place et revu pour σ (ADR-0021 :
  `sigma_by_class` + `sigma_class_of_flux`). τ par classe RÉUTILISE le même `sigma_class_of_flux`.
  Incrément mineur, miroir d'un motif revu. **Réserve G0** : c'est néanmoins un changement de
  signature (scalaire→carte) qui doit passer par ADR/G0 avant code — le harnais actuel ne le
  fait pas encore.
- **La matrice φ mêle DÉJÀ des seuils par-classe.** Le co-écart `n11` (lm.py l.173) compte les
  fenêtres où deux flux sont tous deux dans `ECARTS` — et `ECARTS = {PANNE, STALENESS,
  HORS_ENVELOPPE}` (r1.py l.76) inclut DÉJÀ la staleness σ **par classe** (ADR-0021). τ par
  classe est le même type de mélange, pas une nouveauté. Comme chaque τ est calé à taux de base
  honnête ~0, `n11 ≈ 0` sur données honnêtes pour toutes les paires → la comparaison
  inter-classes reste licite.
- **Réserve à porter** : les classes ont des **sensibilités de détection hétérogènes** (marges
  1,01×–2,01×, attaque 4) → une même déviation réelle δ s'enregistre « en écart » à des seuils
  différents selon la classe. La localisation inter-clusters (`_localize_intercluster`,
  r2.py l.1013) ne doit pas être lue comme « la classe X co-défaille plus » alors que c'est
  « la classe X a un τ plus serré ». À documenter dans l'ADR.
- **Pas de sur-ajustement 48 h de la STRUCTURE.** L'ASSIGNATION de classe est MÉCANISTE (type de
  source, `sigma_class_of_flux`, ADR-0021), pas ajustée aux 48 h ; seules les VALEURS de τ sont
  calées sur 48 h — c'est le grief de l'attaque 2 (sous-échantillonnage), pas un grief
  par-classe-vs-scalaire.

**PORTÉE attaque 3** : structure par-classe **ENTÉRINÉE** (nécessaire, chiffrée : 793 vs 0
faux drapeaux). Aucune valeur en cause. Requiert un changement de signature scalaire→carte
(G0/ADR) + une note d'interprétation de la sensibilité hétérogène de φ.

---

## ATTAQUE 4 — Cohérence des marges (pyth 0,15 % ≈ 2× max ; sans 0,30 % ≈ 1,01× max)

### ENTÉRINÉ-AVEC-RÉSERVE — l'hétérogénéité des marges est FORCÉE, pas un défaut de conception

Marges réelles sur `max_both` (refute_probe P4) :

| classe | τ % | max_both % | marge τ/max | CAPO/max (plafond de détection) | note |
| --- | --- | --- | --- | --- | --- |
| oracle_pyth | 0,15 | 0,0746 | **2,01×** | 38,2× | plancher de grille (pas le max) |
| place_horodatee | 0,30 | 0,2794 | 1,07× | 10,2× | grid-ceil(max) |
| sans_horodatage | 0,30 | 0,2962 | 1,01× | 9,6× | grid-ceil(max) |
| agregateur | 1,75 | 1,7319 | 1,01× | **1,65×** | grid-ceil(max) |
| oracle_chainlink | 1,30 | 1,0946 | 1,19× | 2,60× | ancre externe 1,29 % > max in-harnais |

Deux constats :
1. **Parmi les classes pilotées-par-max (place/sans/agregateur), les marges sont en fait
   HOMOGÈNES à ~1,01–1,07×** (toutes = grid-ceil du max). La « dispersion » 2× vs 1,01 % que
   l'attaque redoute vient **uniquement de pyth**, seul cas piloté par le plancher de grille
   (défateur 1b) — ce n'est pas une incohérence de calibration par-classe.
2. **Une marge HOMOGÈNE (p. ex. 2× partout) est INFAISABLE.** Le plafond de détection est
   `CAPO / max_both` par classe ; pour agregateur il ne vaut que **1,65×** (max 1,7319 % vs CAPO
   2,85 %). `2 × 1,7319 = 3,46 % > CAPO 2,85 %` : imposer 2× à agregateur **franchirait le
   plancher d'événement réel** (raterait un événement de type CAPO). Les marges DOIVENT être
   hétérogènes : les classes serrées peuvent s'offrir 2×, agregateur est **boîté** dans
   (1,73 % ; 2,85 %). L'attaque « marge homogène » est donc réfutée par la contrainte
   CAPO↔max. **ENTÉRINÉ.**

### RÉSERVE (concrète) — les marges ~1,01× sont MINCES sur un max d'1 jour ; alternative principielle nommée

`grid-ceil(max)` avec `max` estimé sur n=1 j/régime (attaque 2) donne des marges 1,01× pour
place/sans/agregateur : une journée de campagne à peine pire que l'unique jour de calibration
produit des dépassements honnêtes non prévus par le « 0 épisode ». **Alternative principielle
(à adjuger par l'ADR, non imposée)** : faire de la marge la variable de CONTRÔLE explicite —
`τ_classe = grid-ceil(k · max_both)` plafonné à CAPO, avec k un facteur de robustesse. À k=1,5 :

| classe | grid-ceil(1,5×max_both) | vs recommandé actuel |
| --- | --- | --- |
| oracle_pyth | 0,15 % | = 0,15 % |
| place_horodatee | 0,45 % | 0,30 % → 0,45 % |
| sans_horodatage | 0,45 % | 0,30 % → 0,45 % |
| agregateur | 2,60 % (< 2,85 CAPO ✔) | 1,75 % → 2,60 % |
| oracle_chainlink | 1,30 % (mécaniste) | = 1,30 % |

Ce choix échange **robustesse aux faux drapeaux** (marges ~1,5× uniformes, tenant au
sous-échantillonnage) contre **sensibilité de détection** (agregateur passe de 1,75 % — le PLUS
sensible, bas de sa boîte — à 2,60 % — proche de CAPO, rate les manipulations agregateur dans
[1,75 % ; 2,60 %]). **C'est un arbitrage de POLITIQUE que l'ADR doit trancher explicitement**,
en particulier pour agregateur (dont τ=1,75 % maximise la détection au prix de la marge minimale).

### Tableau de puissance de détection à porter dans l'ADR (Type-II, sourcé)

La dérivation est 100 % pilotée par la fausse-alarme (Type-I) ; la détection (Type-II) n'est
vérifiée que par la seule contrainte `τ < CAPO`. `TAU-recherche.md` Q5 donne le paysage
d'événements réels ([lu], niveaux déclarés là-bas) — l'ADR doit porter :

| événement réel | magnitude | niveau (TAU-recherche.md) | rapport aux τ |
| --- | --- | --- | --- |
| CAPO/Aave wstETH (10/03/2026) | 2,85 % (2,96 % par recalcul des ratios) | [lu, primaire non-verbatim] | > tous les τ → capté par toutes les classes |
| USDe Pyth (10/10/2025) | 4,3 % | [lu-extrait LlamaRisk] | > tous les τ → capté |
| USDe Chainlink (10/10/2025) | 0,65 % | [lu-extrait LlamaRisk] | jugé **SÛR** → à NE PAS signaler pour l'oracle (chainlink 1,30 % > 0,65 % ✔) ; anormal pour un exchange (place/sans 0,30 % < 0,65 %) |
| USDe Binance CEX | 35 % | [lu-extrait ×2] | contexte (source CEX unique, pas oracle agrégé) |

Lecture : **aucun événement « à capter » ne tombe SOUS un τ choisi** (0,65 % est sûr, pas à
capter ; le plus petit « à capter » est CAPO 2,85 %, au-dessus de tous les τ). Le plafond
scalaire unique CAPO 2,85 % appliqué à des τ par-classe est **cohérent** ici — mais reste une
asymétrie de conception (un plafond scalaire sur des seuils par-classe) à NOMMER, avec ce
tableau, dans l'ADR.

**PORTÉE attaque 4** : marges hétérogènes **ENTÉRINÉES** (forcées par CAPO↔max). Aucune valeur
invalidée. Réserve = minceur 1,01× sur max d'1 jour → alternative k=1,5× à arbitrer + tableau de
détection Type-II à inscrire.

---

## Points de mécanisme vérifiés (non-défateurs, à consigner)

- **Ancre chainlink 0,5 % — VALEUR correcte, commentaire imprécis.** `CHAINLINK_PARAM=0,005`
  est commenté « ETH/USD mainnet » (derive_tau l.32) alors que le feed suivi est **BTC/USD**
  (r2.py). `TAU-recherche.md` Q1 confirme le seuil 0,5 % pour BTC/USD **aussi** (Ethereum
  Mainnet), [lu, primaire, on-chain, deux méthodes]. Donc la valeur tient ; **corriger le
  commentaire en « BTC/USD mainnet »**. Piège de collision réseau signalé par la source
  elle-même : Base 0,15 %, Arbitrum 0,05 % — seul Ethereum Mainnet est pertinent.
- **Ancre chainlink overshoot 1,29 % — provenance à confier au worker ARITHMÉTIQUE.** La MÉTHODE
  (ancre mécaniste = max lag honnête de l'oracle stale) est saine et sourcée (Q1 : mécanisme
  seuil 0,5 % + latence de congestion, dépassements on-chain observés jusqu'à 1,14 % BTC/USD).
  Le CHIFFRE exact 1,29 % (`CHAINLINK_OVERSHOOT`, l.31, « mesuré, signature R-21 ») est SUPÉRIEUR
  au max Q1 (1,14 %) ET au max in-harnais (1,0946 %) — donc τ=1,30 % est conservateur (ne
  faux-signale aucune latence honnête observée), MAIS l'origine du 1,29 % (fichier signature)
  n'est pas dans mon périmètre méthode : **à vérifier par le worker arithmétique**.
- **CAPO 2,85 % vs 2,96 %.** `TAU-recherche.md` Q5 signale un écart d'arrondi (ratios recalculés
  = 2,96 %) non résolu, sans incidence d'ordre de grandeur. `τ < CAPO` tient dans les deux cas.
  Item arithmétique, hors méthode.

---

## SYNTHÈSE pour l'orchestrateur

### Défateurs CONCRETS trouvés (3)

1. **[1a — R-21/provenance]** La borne Clopper-Pearson n'est pas câblée dans la sélection
   (derive_tau l.172 calculée, l.179 gate sans `cpu`, gate = `ep26 ≤ BUDGET` l.176) ; la chaîne
   de justification émise (l.187-188) et la docstring (l.7-9) affirment faussement une « borne
   CP ». Règle réelle = `grid-ceil(max_both)`. **Correction** : câbler la CP OU réécrire la
   règle/justifications pour dire ce que le code fait.
2. **[1b — chiffre nu porteur / doc 03]** `τ_pyth = 0,15 %` est le **plancher de grille**, pas
   une valeur calibrée (donnée → 0,10 %) ; label « [quantile] » trompeur. **Correction binaire** :
   adopter 0,10 %, OU sourcer le plancher 0,15 % (ancres candidates dans TAU-recherche.md Q1/Q2/Q4).
3. **[2 — régime]** Le max honnête RAPPORTÉ est pris sur la strate lâche-par-P99 (calme) alors
   que le vrai max vit sur STRESS pour **place** (0,1568→0,2794 ; marge réelle 1,07× non 1,91×)
   et **chainlink** (0,8969→1,0946). Règle « strate la plus lâche » non fondée (P99 ≠ max).
   **Correction** : max honnête sur les DEUX strates ; marges recalculées.

### Entérinés AVEC RÉSERVE (les τ valeurs tiennent, sauf pyth au point 2)

- **Attaque 1 (budget)** : « 4 » inoffensif dans son plateau {1..12} ; le vrai levier est la
  quantification ×13 (zéro épisode 48 h). Réserve : nommer la règle réelle ; k·σ/ARL écarté à
  bon droit (queues lourdes, sourcé Q6).
- **Attaque 3 (par-classe)** : nécessaire — scalaire committé 0,50 % ⟹ **793** faux drapeaux
  honnêtes/26 j (F2), et échoue des deux côtés (bruit ×23). Réserves : threading scalaire→carte
  via ADR/G0 (patron ADR-0021 déjà en place, r1.py l.121/166) ; note sur la sensibilité
  hétérogène de la matrice φ.
- **Attaque 4 (marges)** : hétérogénéité FORCÉE (agregateur 2×max = 3,46 % > CAPO 2,85 %).
  Réserves : marges 1,01× minces sur max d'1 jour → alternative k=1,5× à arbitrer ; tableau de
  puissance de détection Type-II (0,65 % sûr / 2,85 % CAPO / 4,3 % Pyth) à inscrire.

### Réserves de régime transverses (attaque 2)

- n=1 jour/régime ; étiquettes calendaires empiriquement inversées ET non monotones (max sur
  stress pour 2 classes) ; projection 26 j (≈8 j week-end) depuis 1 jour-stress échantillonné.
- **Correction par l'existant** : mandater une re-dérivation à checkpoint via
  `closure.tau_revision_needed` (fail-closed, closure.py l.169-176) après le 1ᵉʳ week-end réel ;
  tout dépassement honnête au τ choisi déclenche la clause de révision.

### À confier au worker ARITHMÉTIQUE (hors méthode)

Origine du chiffre `CHAINLINK_OVERSHOOT = 1,29 %` (fichier signature) ; arrondi CAPO
2,85 %/2,96 %. La méthode d'ancrage mécaniste chainlink est saine ; seul le chiffre est à tracer.

---

## Annexe — reproductibilité

- Table de décision : `python "C:\Users\KACIMI\AppData\Local\Temp\claude\F--Shogen\90684fb2-4e7b-42e9-b820-f042dc4465f3\scratchpad\tau-facts\derive_tau.py"` (recalcule τ recommandés + table de sensibilité par classe).
- Sonde de réfutation : `python "C:\Users\KACIMI\AppData\Local\Temp\claude\F--Shogen\90684fb2-4e7b-42e9-b820-f042dc4465f3\scratchpad\tau-facts\refute_probe.py"` — P1 sensibilité budget ; P2 max/P99 par (classe, strate) ; P3 plancher de grille pyth ; P4 marges sur max_both.
- Les deux réutilisent `shogen_s2` (records/r1/closure) déjà revu, lecture seule, n'écrivent
  rien dans le dépôt ni dans les journaux (R-20). Journaux source : `F:\shogen-campagne\
  calibration\{control,journal}.jsonl` (48 h, 2880 fenêtres, N=34533 écarts).
