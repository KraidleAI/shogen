# S2 Shōgen — RÉFUTATION des contraintes & ancres du jeu de τ par classe (support ADR-0022)

| champ | valeur |
| --- | --- |
| Rôle | RÉFUTANT contraintes & ancres τ (attaque, pas validation molle) |
| Modèle résolu (worker) | `claude-opus-4-8[1m]` (effort max) — Gate 0 (R-1) conforme |
| Date | 2026-08-26 |
| Nature | Donnée brute pour l'orchestrateur (vérification adversariale R-21). Aucune décision ; la fixation de τ est une décision ADR. Ne committe rien (R-20). |
| Objet attaqué | jeu de τ RELATIF par classe proposé par `derive_tau.py` (support ADR-0022) : `oracle_pyth=0,15 %` ; `place_horodatee=0,30 %` ; `sans_horodatage=0,30 %` ; `agregateur=1,75 %` ; `oracle_chainlink=1,30 %` |
| Portée | Le drapeau τ (`|vᵢ−médiane_LOO|/médiane_LOO > τ_classe`) alimente la co-aberrance z de R1 → **drapeau_2** (co-défaillance, r2.py:957) |
| Faits internes | `...\tau-facts\F1-F2.md` (P99/max calibration 48 h) |
| Faits externes | `...\oracle-research\TAU-recherche.md` (Q1 Chainlink, Q4/Q5 magnitudes réelles) |
| Scripts rejouables (miens) | `refute_maxes.py` (max par classe/flux, 2 strates) ; `refute_cp.py` (borne CP décorative) |
| Corroboration préexistante | `refute_probe.py` + `claims-capture.txt` (déjà dans le scratchpad, auteur non identifié dans cette session ; recoupe `refute_maxes.py` à l'octet — non-autorité, corroboration) |
| Machinerie réutilisée | `records.*`, `r1.{DECIMAL_PREC,_median,build_window_strate,parse_journal}`, `closure.percentile_nearest_rank` ; écart honnête = mêmes gardes fail-closed que `closure.py:119-147` |

Commandes (recalcul bit-identique, ADR-0003) :
```
cd F:\Shogen\s2-harness
python ...\tau-facts\refute_maxes.py
python ...\tau-facts\refute_cp.py
python ...\tau-facts\derive_tau.py     # l'objet attaqué (sa propre sortie)
```

---

## 1. Synthèse — verdict par classe

| classe | τ reco | MAX honnête **2 strates** (flux, strate) | contrôle #1 (τ>max) | marge | verdict |
| --- | --- | --- | --- | --- | --- |
| oracle_pyth | 0,15 % | **0,0746 %** (pyth, calme) | VÉRIFIÉ | +7,54 bps (2,009×) | **TENU** |
| place_horodatee | 0,30 % | **0,2794 %** (okx_ticker, **stress**) | VÉRIFIÉ | +2,06 bps (1,074×) | **TENU** (#1) + défaut de dérivation |
| sans_horodatage | 0,30 % | **0,2962 %** (bitfinex, calme) | VÉRIFIÉ | **+0,38 bps** (1,013×) | **DÉFAUT** (#4) |
| agregateur | 1,75 % | **1,7319 %** (defillama, calme) | VÉRIFIÉ | +1,81 bps (1,010×) | **DÉFAUT** (#1 marge + #5 structurel) |
| oracle_chainlink | 1,30 % | **1,0946 %** (chainlink, **stress**) | VÉRIFIÉ | +20,54 bps (1,188×) | **VALEUR TENUE / ANCRE DÉFECTUEUSE** (#3) |

**Le contrôle #1 littéral (τ > max des deux strates) est VÉRIFIÉ pour les cinq classes.** Les défauts sont ailleurs — et trois d'entre eux sont TRANSVERSAUX (sections 2-5), plus graves qu'un dépassement de max isolé parce qu'ils touchent la *méthode* de dérivation et le *signal aval* drapeau_2.

bps = point de base = 0,01 point de pourcentage. « marge » = τ − max, en points de %.

---

## 2. DÉFAUT MAÎTRE (transversal) — la borne Clopper-Pearson annoncée est DÉCORATIVE (R-21)

`derive_tau.py` (docstring l.7-9) annonce comme garde-fou de fausse-alarme une **borne supérieure binomiale de Clopper-Pearson exacte, projetée en épisodes sur 26 j**. Le code de sélection ne l'applique jamais :

```
l.172  cpu = cp_upper(k, N, ...)            # borne CP : CALCULÉE
l.174  ep26 = CALIB_TO_CAMPAIGN * ep48      # projection PONCTUELLE naïve = 13 × épisodes OBSERVÉS
l.176  okbudget = ep26 <= BUDGET_EPISODES   # <-- LE GARDE réellement testé
l.179  if chosen is None and okq and okbudget and okcapo:   # sélection : okq & okbudget & okcapo
l.183  print(... cpu ...)                   # cpu n'apparaît QUE dans le print — jamais dans okbudget
```

Reproduction (`refute_cp.py`, `cp_upper` copié verbatim → recoupe la colonne `CP_UB` de `derive_tau.py` à l'octet) :

| classe | τ | N | k | ep26j **(code, naïf)** | CP_UB taux (95 %) | **lectures d'excès 26 j (borne CP)** | épisodes min | méthode annoncée |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| oracle_pyth | 0,15 % | 1440 | 0 | 0 | 0,2078 % | **38,9** | ≥5 | **REJETTE** |
| place_horodatee | 0,30 % | 7200 | 0 | 0 | 0,0416 % | **38,9** | ≥5 | **REJETTE** |
| sans_horodatage | 0,30 % | 4320 | 0 | 0 | 0,0693 % | **38,9** | ≥5 | **REJETTE** |
| agregateur | 1,75 % | 2880 | 0 | 0 | 0,1040 % | **38,9** | ≥5 | **REJETTE** |

Mécanisme : pour k=0, `cp_upper(0,N) ≈ ln(20)/N`, donc la borne sup 95 % du **nombre attendu** de lectures honnêtes d'excès sur 26 j vaut `13 × ln(20) ≈ 38,9`, **indépendamment de N**. Même regroupées en épisodes de longueur maximale observée (8 fenêtres, F1-F2.md), cela fait ≥5 épisodes > budget 4.

**Conséquence.** Le budget « ≤4 épisodes/26 j » n'est « passé » aux τ recommandés que parce que le code projette `13 × 0 = 0` (aucun excès observé en 48 h), en ignorant l'incertitude d'échantillonnage que sa propre méthode annoncée sert à couvrir. La borne CP, si on l'applique comme annoncé, **rejette les quatre τ quantiles** — elle est en fait **insatisfaisable depuis 48 h à budget 4**. C'est une **incohérence méthode/code (R-21)**, pas un jugement : soit le garde statistique annoncé n'est pas appliqué, soit il l'est et il rejette la sélection. Dans les deux cas, la sélection quantile ne porte AUCUNE marge de fausse-alarme démontrée — elle repose sur le seul fait que zéro excès n'a été *observé* en 48 h.

---

## 3. DÉFAUT (transversal) — τ = grid-ceil(max 48 h) : surajustement à l'échantillon de calibration

Pour les trois classes larges (place, sans_horodatage, agrégateur), le τ retenu est **le plus petit pas de grille (0,05 %) au-dessus du plus grand écart honnête unique observé en 48 h** — c.-à-d. `τ = ⌈max_48h⌉` sur la grille (`refute_probe.py` P4 le nomme « grid-ceil(max) »). Signature du surajustement :

- **Cliff de budget** (`refute_probe.py` P1) : `sans_horodatage` sélectionne 0,30 % **à TOUS les budgets de 1 à 52** — parce qu'il existe une falaise de grille (0,25 %→91 épisodes/26 j, 0,30 %→0). Le « 0 épisode » à 0,30 % dépend ENTIÈREMENT du fait qu'un seul relevé (bitfinex 0,2962 %) tombe juste sous 0,30 %. Un unique relevé honnête à 0,31 % en 48 h aurait fait sauter τ à 0,35 %.
- **Queues lourdes** : sur les deux strates, `max/P99` = **2,14** (sans_horodatage), **3,10** (agrégateur). Un ratio >2-3 = distribution à queue lourde ; sur 26 j (≈13× l'échantillon), le max honnête croît nettement — le max 48 h n'est PAS un plafond de campagne.
- **La convention 3σ du harnais lui-même sous-couvre l'agrégateur** : ADR-0020 (:3090) fixe `σ = max(plancher, 3×P99(staleness))`. Appliquée à l'écart : `3 × P99_agregateur(2 str) = 3 × 0,5584 % = 1,675 %`, **< max observé 1,7319 %**. La règle 3σ maison ne couvre même pas le max déjà vu — preuve que la classe agrégateur n'a pas de τ quantile propre.

Un τ posé au ⌈max_48h⌉ n'a, par construction, aucune marge de généralisation ; la section 5 chiffre le coût aval.

---

## 4. DÉFAUT (transversal) — cécité de strate de `derive_tau.py`

`derive_tau.py:looser_strate()` (l.119-125) choisit la strate « la plus lâche » **par P99**, puis calcule et affiche le `max` sur CETTE seule strate (l.146-147). Or le MAX peut être dans l'AUTRE strate (`refute_maxes.py` / `refute_probe.py` P2) :

| classe | max **calme** | max **stress** | max **2 strates** (celui qu'exige le contrôle #1) | derive_tau affiche |
| --- | --- | --- | --- | --- |
| place_horodatee | 0,1568 % | **0,2794 %** | **0,2794 %** (stress) | 0,1568 % (calme) — **sous-estimé de 78 %** |
| oracle_chainlink | 0,8969 % | **1,0946 %** | **1,0946 %** (stress) | 0,8969 % (calme) |

Pour `place_horodatee`, la conséquence est directe : la marge que `derive_tau` laisse croire (0,30 % vs 0,1568 % ≈ 1,9×) est en réalité **+2,06 bps (1,074×)** contre le vrai max 0,2794 %. Le `max` sur lequel la dérivation raisonne n'est le max des deux strates que pour 3 des 5 classes. Le contrôle #1 exige le max des DEUX strates ; `derive_tau` ne le calcule jamais.

---

## 5. DÉFAUT (transversal) — marges minces sur une FENÊTRE CORRÉLÉE → risque de faux drapeau_2

Les maxima honnêtes de plusieurs classes **coïncident à la même fenêtre** `ws=1787375400` = **2026-08-22 05:10 UTC (samedi, strate stress)** — `refute_maxes.py` localise chaque max :

| flux | classe | écart à ws=1787375400 | τ classe | flaggé au τ reco ? |
| --- | --- | --- | --- | --- |
| okx_ticker | place_horodatee | 0,2794 % (= son max 2 str) | 0,30 % | non (0,2794 < 0,30) |
| okx_index | place_horodatee | 0,1519 % | 0,30 % | non |
| binance | sans_horodatage | 0,1870 % | 0,30 % | non |
| kraken | sans_horodatage | 0,2425 % | 0,30 % | non |
| coingecko | agregateur | 1,5654 % (= son max 2 str) | 1,75 % | non |
| chainlink | oracle_chainlink | 1,0946 % (= son max 2 str) | 1,30 % | non |

**Six flux de quatre classes co-culminent à une seule fenêtre honnête** : un mouvement rapide de BTC que toutes les sources lentes (agrégateur, oracle heartbeat-laggé, places) retardent SIMULTANÉMENT par rapport à la médiane. C'est du bruit honnête **corrélé** (facteur marché commun), pas une co-défaillance.

Aux τ recommandés, cette fenêtre ne déclenche AUCUN drapeau (tous sous seuil) — mais avec des marges de **+0,38 à +2,06 bps** (sections 1, 3) sur une distribution à queue lourde et 13× plus de données, la version campagne d'une telle fenêtre franchira **plusieurs τ à la fois**.

**Mécanisme aval vérifié (r2.py, lecture du prédicat exact)** : `drapeau_2` (r2.py:957-1001) est LEVÉ ssi `z_max ≥ 2,33 (SEUIL_Z)` **ET** `k_eff = k_nominal`. Le drapeau τ entre via `r1.classify_cells` → compte de flux en écart par fenêtre → **z de co-aberrance du pool** (testé contre l'indépendance). Des franchissements honnêtes *corrélés* sur une même fenêtre gonflent ce compte → gonflent z. Comme un mouvement de marché commun n'est PAS une dépendance au sens R2 (ni ASN ni copie de contenu), `k_eff` reste `= k_nominal` (partition « propre ») → **z élevé + partition propre = drapeau_2 LEVÉ à tort**. C'est EXACTEMENT le faux positif que drapeau_2 doit éviter (« co-défaillance non expliquée par les axes R2 »).

Précision (ne pas surinterpréter) : `z` est agrégé sur la strate — une seule fenêtre ne « lève » pas mécaniquement le drapeau. L'affirmation exacte est : **des τ à marge mince laissent passer davantage de franchissements honnêtes corrélés, ce qui pousse le z de co-aberrance vers le seuil et alimente drapeau_2 avec le motif même qu'il traite comme signal.** Le déclenchement dépend de l'agrégation z sur l'ensemble des fenêtres. C'est la raison décisive de préférer des marges supérieures au ⌈max_48h⌉.

---

## 6. Contrôles par classe (chiffrés)

### 6.1 oracle_pyth = 0,15 % — **TENU**
- **#1 (τ>max 2 str)** : VÉRIFIÉ. max = **0,0746 %** (pyth, calme) ; marge **+7,54 bps (2,009×)** — la seule classe quantile à marge confortable.
- **#2 (τ<événement réel)** : VÉRIFIÉ. Événement pyth réel documenté = **430 bps = 4,3 %** (oracle Pyth, incident USDe 10 oct. 2025 ; *mesuré sur un feed USDe, transposition d'actif vers BTC/USD assumée* — TAU-recherche Q5). 0,15 % ≪ 4,3 % : capte tout écart pyth ≥0,15 %.
- Note : 0,15 % est le **plancher de grille** (`refute_probe.py` P3 : un plancher à 0,05 %/0,10 % donnerait 0,10 %) ; 0,15 % reste 2× le max honnête → sans danger. Pas un défaut.

### 6.2 place_horodatee = 0,30 % — **TENU (contrôle #1) + DÉFAUT DE DÉRIVATION**
- **#1** : VÉRIFIÉ mais MINCE. Vrai max 2 strates = **0,2794 %** (okx_ticker, **stress**), marge **+2,06 bps (1,074×)** — et non 0,1568 % (calme) comme l'affiche `derive_tau` (section 4).
- **#2** : VÉRIFIÉ. Seule magnitude CEX documentée du corpus = **35 %** (USDe/Binance spot, TAU-recherche Q5). 0,30 % ≪ 35 %. *(Aucun seuil « flash-crash ≥1 % » n'est sourcé dans le corpus — non invoqué.)*
- Verdict : la valeur tient, mais la dérivation a raisonné sur la mauvaise strate et la marge réelle est mince. À recalculer sur les deux strates ; surveiller la tenue en campagne (queue lourde stress).

### 6.3 sans_horodatage = 0,30 % — **DÉFAUT (contrôle #4)**
- **#1 littéral** : VÉRIFIÉ (0,30 % > 0,2962 %). **Le défaut n'est pas #1, c'est #4.**
- **#4 (marge trop fine)** : **VIOLÉ.** max 2 strates = **0,2962 %** (bitfinex, calme) → marge **+0,38 bps (1,013×)** : τ = ⌈max_48h⌉ exact. Budget-insensible par falaise de grille (section 3) ; queue `max/P99 = 2,14` ; rejeté par la borne CP annoncée (section 2). Sur 26 j (13× données), le max honnête franchira très plausiblement 0,2962 % puis 0,30 % → faux drapeaux, corrélés au reste de la fenêtre stress (section 5).
- **#2** : VÉRIFIÉ (0,30 % ≪ 35 %, seule magnitude CEX documentée).
- **τ alternatif proposé : 0,50 %.** Justification : (a) c'est le **τ global déjà committé** (`run_params`, F1-F2.md) — ne pas resserrer *sous* la valeur committée sur la foi d'un seul max 48 h ; (b) F2 (F1-F2.md) montre **0 excès honnête** pour binance/kraken/bitfinex à 0,50 % ; (c) marge +20,4 bps / **1,69× le max** ; (d) 0,50 % ≪ 35 %. **Honnêteté** : 0,50 % ne « certifie » pas mieux le budget CP (le test est insatisfaisable depuis 48 h à budget 4, section 2) — il achète une marge 1,69× au lieu de 1,013×, rien de plus. Le choix final reste ADR.

### 6.4 agregateur = 1,75 % — **DÉFAUT (contrôle #1 marge + contrôle #5 structurel)**
- **#1** : VÉRIFIÉ mais MINCE. max 2 strates = **1,7319 %** (defillama, calme), marge **+1,81 bps (1,010×)** = ⌈max_48h⌉. Queue la plus lourde du pool (`max/P99 = 3,10`) ; **3×P99 = 1,675 % < max 1,7319 %** (section 3 : la règle 3σ maison ne couvre pas le max). Sur 26 j, max honnête > 1,75 % plausible → faux drapeaux.
- **#5 (trop lâche ? manquerait 1-1,7 %)** : l'enveloppe honnête atteint **1,73 %** ; donc **toute dislocation d'agrégateur < ~1,75 % est indétectable par construction** (noyée dans le bruit honnête). Ce n'est PAS un « manque d'événement documenté » (aucune dislocation coingecko/defillama de 1-1,7 % n'est dans le corpus ; CAPO 2,85 % est un taux de change wstETH, pas une erreur d'agrégateur) — c'est une **limite de pouvoir intrinsèque** de la classe, non corrigeable par réglage de τ.
- **#2** : VÉRIFIÉ pour CAPO. Plus petite magnitude réelle pertinente = **CAPO 2,85-2,96 %** (post-mortem Aave 10 mars 2026, [lu] primaire, TAU-recherche Q5) ; 1,75 % < 2,85 % → capte CAPO.
- **Bind assumé** : les deux cornes tirent en sens opposés — durcir #1 (monter τ) aggrave #5 (moins de pouvoir) ; durcir #5 (baisser τ) aggrave #1 (faux drapeaux). **Options ADR (pas un verdict)** : (i) **τ ≥ 2,0 %** pour la robustesse fausse-alarme (marge +26,8 bps / 1,155× ; reste < CAPO 2,85 % de 85 bps) ; (ii) **pondérer/décoter l'agrégateur dans drapeau_2** (traiter ses drapeaux comme basse confiance) puisque la classe ne sépare pas proprement bruit et dislocation < ~2 %. À adjuger.

### 6.5 oracle_chainlink = 1,30 % — **VALEUR TENUE / ANCRE DÉFECTUEUSE (contrôle #3)**
- **#1** : VÉRIFIÉ confortablement. max 2 strates = **1,0946 %** (chainlink, **stress**), marge **+20,54 bps (1,188×)** — seule classe à marge robuste, ironiquement parce qu'elle a utilisé l'ancre gonflée plutôt que le grid-ceil.
- **Ethereum Mainnet vs Base** : **VÉRIFIÉ Ethereum Mainnet.** `sources.py:223-224` lit `_CHAINLINK_RPC="https://ethereum-rpc.publicnode.com"` et le proxy `_CHAINLINK_AGGREGATOR="0xF4030086522a5bEEa4988F8cA5B36dbC97BeE88c"` = **BTC/USD Ethereum Mainnet** (sources.py:215 `# feed BTC/USD` ; ce proxy est vérifié on-chain `description()→"BTC / USD"` dans TAU-recherche Q1 ; ADR-0020 :3136 le nomme « feed Chainlink BTC/USD »). **PAS Base** (qui aurait une autre adresse et un seuil 0,15 %). Le seuil documenté 0,5 % est confirmé pour BTC/USD ET ETH/USD Ethereum Mainnet (TAU-recherche Q1, [lu] primaire on-chain + data.chain.link).
- **#3 ancre « dépassement inter-round max 1,29 % »** : **DÉFAUT — non reproductible depuis les archives désignées.** Le `CHAINLINK_OVERSHOOT=0.0129` (derive_tau.py:31, étiqueté « signature, R-21 ») n'apparaît :
  - ni dans le journal S2 : max chainlink 2 strates = **1,0946 %** (F2 le borne : 0 lecture >1,25 %) ;
  - ni dans TAU-recherche.md : delta inter-round chainlink mesuré = **1,14 %** (BTC/USD, le feed Shōgen) et 0,76 % (ETH/USD) — Q1 ;
  - ni dans ADR-0020/DECISIONS.md (le seul « 1.29 » y est `rustup 1.29.0`, une version).
  Un chiffre présenté comme signature R-21 doit être reproductible : **il ne l'est pas** → défaut de provenance. (Ne PAS conclure « faux » : une mesure orchestrateur hors archives reste possible → **demande de sourçage/procurement**, conforme zéro-dette.)
- **Étiquette erronée** : derive_tau.py:32 dit « seuil documenté **ETH/USD** mainnet » ; Shōgen lit **BTC/USD**. La valeur 0,5 % est identique pour les deux (TAU-recherche Q1), donc immatérielle à la valeur — mais l'étiquette est fausse.
- **La valeur τ=1,30 % tient sur des bases DE DONNÉES** : > max honnête S2 (1,0946 %, +20,5 bps) ; > dépassement mesuré BTC/USD (1,14 %, +16 bps) ; < CAPO (2,85 %). Elle ne tient PAS sur l'ancre *énoncée* (1,29 % non sourcé).
- **⚠ AVERTISSEMENT anti-correction mécanique (à porter à l'ADR)** : si un correcteur pressé remplace l'ancre par le 1,14 % *mesuré* et re-grille, τ tombe à **1,15 %** — soit seulement +5,5 bps sur le max S2 (1,0946 %), aussi fragile que les classes minces. **La bonne correction est de re-justifier 1,30 % sur le max honnête reproductible (1,0946 %) + marge, PAS de swapper le chiffre d'ancre et re-grid.** La valeur n'a pas besoin de changer ; sa justification, si.
- **#2 (détectabilité panne réelle >1,30 %)** : une panne chainlink sévère (staleness/heartbeat → dérive) finit par franchir 1,30 % → détectable. La déviation chainlink de l'incident USDe (65 bps, jugée « sûre » par LlamaRisk, TAU-recherche Q4) est < τ → non flaggée, correctement (chainlink y était la source fiable, pas la dislocation). Bande aveugle inhérente (1,0946 %, 1,30 %) = 20,5 bps.

---

## 7. τ alternatifs proposés (support de décision — l'ADR adjuge, ceci n'est pas un verdict)

| classe | τ reco | statut | τ alternatif proposé | base |
| --- | --- | --- | --- | --- |
| oracle_pyth | 0,15 % | TENU | — (garder) | 2,009× max ; ≪ 4,3 % |
| place_horodatee | 0,30 % | tenu, marge mince | recalculer max **2 strates** ; réévaluer marge vs 0,2794 % | cécité de strate (§4) ; envisager ≥0,40 % si robustesse voulue (≪35 %) |
| sans_horodatage | 0,30 % | **DÉFAUT #4** | **0,50 %** | τ global committé ; F2 : 0 excès ; 1,69× max ; ≪35 % |
| agregateur | 1,75 % | **DÉFAUT #1+#5** | **≥2,0 %** *et/ou* décote drapeau_2 | 1,155× max ; <CAPO ; classe basse puissance (§6.4) |
| oracle_chainlink | 1,30 % | valeur tenue / **ancre défectueuse #3** | garder **1,30 %**, re-justifier sur max S2 1,0946 %+marge ; sourcer ou retirer le 1,29 % | §6.5 + avertissement anti-correction |

**Défaut de méthode à corriger en amont de tout re-choix (§2)** : le garde-fou de fausse-alarme de `derive_tau.py` doit être soit la borne CP réellement appliquée (et alors le budget 4 est à réviser, il est insatisfaisable depuis 48 h), soit assumé comme « τ > max_48h + marge » — mais pas une borne CP annoncée et un `13×observé` appliqué.

---

## 8. Reproductibilité

Tous les chiffres ci-dessus sortent de `refute_maxes.py` et `refute_cp.py` (mes scripts, lecture seule sur `F:\shogen-campagne\calibration`, Decimal à précision fixée, machinerie `shogen_s2` revue). `refute_probe.py` (préexistant, auteur non identifié cette session) recoupe `refute_maxes.py` à l'octet (P2/P4) et fournit P1 (sensibilité budget) et P3 (plancher de grille pyth). `derive_tau.py` est l'objet attaqué. Aucun de ces scripts ne committe ni ne modifie de journal (R-20). Les faits externes (Chainlink 0,5 %/BTC-USD Ethereum Mainnet ; inter-round 1,14 % ; USDe 65 bps/430 bps ; CAPO 2,85-2,96 %) sont dans `TAU-recherche.md` avec leur niveau [lu]/[abs]/[2nd] et leur source datée.
