# REFUTE-arith — réfutation arithmétique indépendante de `derive_tau.py` (S2 Shōgen)

**Rôle** : worker RÉFUTANT ARITHMÉTIQUE (R-21). **Modèle résolu (GATE 0, R-1)** :
`claude-opus-4-8[1m]` (préfixe `claude-opus-4-8` conforme), effort max.
**Date** : 2026-08-26. **Discipline** : lecture seule sur `F:\Shogen` et
`F:\shogen-campagne` ; écriture uniquement dans `scratchpad\tau-facts\` ; aucun commit (R-20).

## 0. Portée et méthode

Je ne fais PAS confiance à `derive_tau.py`. Je **recalcule chaque affirmation avec mon
propre code**, puis compare. La machinerie de **chargement** est réutilisée (déjà revue,
mandat) : `records.parse_control/effective_run_params/sigma_tau_from_params`, `r1._median`,
`build_window_strate`, `parse_journal`, `DECIMAL_PREC`, `closure.percentile_nearest_rank`.
Toute l'**arithmétique de dérivation** (écart honnête, P99 nearest-rank, Clopper-Pearson,
épisodes, sélection) est **réécrite ex nihilo** depuis la définition de la mission.

**Artefacts** (tous dans `…\scratchpad\tau-facts\`) :
- `refute_independent.py` — mon recalcul indépendant complet (**inliné verbatim en Annexe §8.1**) ;
- `spotcheck_dev.py` — vérif à la main des maxima décisifs d'écart (§4 ; **inliné en Annexe §8.2**) ;
- `claims-capture.txt` — **stdout de `derive_tau.py`, capturé UNE fois comme ARTEFACT DE
  CLAIM** (comparaison, PAS preuve ; la preuve est mon recalcul). `derive_tau.py` n'a été
  ni modifié ni réexécuté comme preuve. (Note : `claims-capture.txt` porte quelques « � »
  d'encodage console Windows ; les chiffres sont intacts — sans effet sur la comparaison.)

**Données** (journal de calibration close 48h, `F:\shogen-campagne\calibration\`) :
`control.jsonl` (6638 lignes), `journal.jsonl` (34572 lignes). Recalcul confirmé :
w=60 s, n_min=4, DECIMAL_PREC=50, **2880 fenêtres = 1440 calme + 1440 stress**, pas de
fenêtre constant = 60 s (2879/2879 écarts), pool = 12 flux. La carte de classes issue du
journal (`sigma_class_of_flux`) est **identiquement égale** à la carte de la mission
(assert dans le script) :
`oracle_pyth={pyth}`, `oracle_chainlink={chainlink}`, `agregateur={coingecko,defillama}`,
`place_horodatee={coinbase,gemini,okx_ticker,okx_index,bitstamp}`,
`sans_horodatage={binance,kraken,bitfinex}`.

**Clopper-Pearson — 4 implémentations, dont 2 génuinement indépendantes de la méthode
float log-space du script** : (M1) bissection float log-space, écriture propre ; (M2)
bissection sur CDF binomiale par **récurrence Decimal prec=80** (ni log ni float —
précision-indépendante) ; (CERT) certificat **exact par `Fraction`** (`math.comb` +
`Fraction(float)`) encadrant p_U au dernier bracket ; (K0) forme fermée k=0 :
p_U = 1 − α^(1/N). Référence côté-script = transcription verbatim de `cp_upper`
(pour tabuler la valeur du script, jamais comme preuve).

---

## 1. CLAIM 1 — P99 (nearest-rank) de l'écart relatif honnête par (classe, strate)

Écart honnête recalculé indépendamment (`|prix − médiane_LOO| / médiane_LOO`, si
`status=='ok'`, `price` non None, `n_resp ≥ 4`, `médiane_LOO > 0`, Decimal prec=50).
Percentile nearest-rank réécrit (rang = ⌈0.99·N⌉ = `-(-(99*N)//100)`) **et** croisé avec
`percentile_nearest_rank` (bénie) : **identiques bit-à-bit sur les 10 cellules**.

| classe | strate | N | P99 (recalc, pleine préc.) | P99 script (imprimé) | max | strate lâche |
|---|---|---|---|---|---|---|
| oracle_pyth | **calme** | 1440 | **0.054633 %** | 0.0546 % | 0.074649 % | ✅ lâche |
| oracle_pyth | stress | 1435 | 0.031684 % | (non imprimé) | 0.069058 % | |
| place_horodatee | **calme** | 7200 | **0.068685 %** | 0.0687 % | 0.156820 % | ✅ lâche |
| place_horodatee | stress | 7190 | 0.046046 % | (non imprimé) | 0.279436 % | |
| sans_horodatage | **calme** | 4320 | **0.153130 %** | 0.1531 % | 0.296191 % | ✅ lâche |
| sans_horodatage | stress | 4314 | 0.129529 % | (non imprimé) | 0.261088 % | |
| agregateur | **calme** | 2880 | **0.717712 %** | 0.7177 % | 1.731879 % | ✅ lâche |
| agregateur | stress | 2876 | 0.384941 % | (non imprimé) | 1.729581 % | |
| oracle_chainlink | **calme** | 1440 | **0.540174 %** | 0.5402 % | 0.896858 % | ✅ lâche |
| oracle_chainlink | stress | 1438 | 0.485249 % | (non imprimé) | 1.094640 % | |

- Les 5 P99 de **strate lâche** recalculés arrondissent **exactement** aux valeurs imprimées
  par le script (%.4f). Les 5 max imprimés (0.0746/0.1568/0.2962/1.7319/0.8969 %) coïncident.
- **Strate lâche = calme** pour les 5 classes : confirmé en calculant aussi la strate stress
  (P99 stress < P99 calme partout). Départage strict `>` + ordre `calme` avant `stress` :
  répliqué.
- N calme = n_flux × 1440 (aucune cellule non-évaluable en calme) ; N stress légèrement <
  (quelques pannes/non-évaluables en stress). Le N imprimé (strate lâche = calme) est exact.

**VERDICT CLAIM 1 : ✅ CONFIRMÉ.** Écart nul. Arithmétique d'écart en outre vérifiée à la
main sur 3 maxima décisifs (§4).

---

## 2. CLAIM 2 — Clopper-Pearson borne supérieure unilatérale 95 %, strate lâche

Pour chaque classe à sa strate lâche (calme), aux τ ∈ {0.15 ; 0.30 ; 1.00 ; 1.30 ; 1.75 %}.
`k` = nb d'écarts de la classe (strate lâche) `> τ` (strict, comme le script) ; N ci-dessus.

| classe (N) | τ | k | CP M1 (log float) | CP M2 (Decimal) | \|M1−M2\| | CP script | \|M2−script\| | certificat |
|---|---|---|---|---|---|---|---|---|
| pyth (1440) | 0.15–1.75 % | 0 | 0.207821 % | 0.207821 % | 4e-19 | 0.207821 % | 4e-19 | K0=0.207821 %, Δ=0 |
| place (7200) | 0.15 % | 2 | 0.087420 % | 0.087420 % | 4e-16 | 0.087420 % | 4e-16 | Fraction ✅ |
| place (7200) | 0.30–1.75 % | 0 | 0.041599 % | 0.041599 % | 5e-20 | 0.041599 % | 5e-20 | K0=0.041599 %, Δ=0 |
| sans (4320) | 0.15 % | 48 | 1.411150 % | 1.411150 % | 2e-15 | 1.411150 % | 2e-15 | Fraction ✅ |
| sans (4320) | 0.30–1.75 % | 0 | 0.069322 % | 0.069322 % | 1e-19 | 0.069322 % | 1e-19 | K0=0.069322 %, Δ=0 |
| agregateur (2880) | 0.15 % | 844 | 30.733185 % | 30.733185 % | 5e-16 | 30.733185 % | 5e-16 | (sauté, k grand) |
| agregateur (2880) | 0.30 % | 235 | 9.048037 % | 9.048037 % | 5e-16 | 9.048037 % | 5e-16 | Fraction ✅ |
| agregateur (2880) | 1.00 % | 7 | 0.456043 % | 0.456043 % | 1e-15 | 0.456043 % | 1e-15 | Fraction ✅ |
| agregateur (2880) | 1.30 % | 2 | 0.218441 % | 0.218441 % | 4e-17 | 0.218441 % | 4e-17 | Fraction ✅ |
| agregateur (2880) | 1.75 % | 0 | 0.103964 % | 0.103964 % | 2e-19 | 0.103964 % | 2e-19 | K0=0.103964 %, Δ=0 |
| chainlink (1440) | 0.15 % | 694 | 50.396330 % | 50.396330 % | 1e-14 | *(script SAUTE)* | — | (sauté, k grand) |
| chainlink (1440) | 0.30 % | 260 | 19.805466 % | 19.805466 % | 1e-14 | *(script SAUTE)* | — | Fraction ✅ |
| chainlink (1440) | 1.00–1.75 % | 0 | 0.207821 % | 0.207821 % | 4e-19 | *(script SAUTE)* | — | K0=0.207821 %, Δ=0 |

- **Référence de vérité = M2** (bissection Decimal prec=80 sur CDF par récurrence exacte,
  300 itérations → exacte à ~1e-80). **max \|M1−M2\| (méthodes indépendantes) = 1.21e-14** ;
  **max \|M2−script\| = 1.21e-14**. Ce max se produit à une cellule à **k grand non décisive**
  (chainlink 0.15 %, k=694 : le float log-space somme 695 termes, plus d'accumulation) ; les
  cellules **décisives k=0** (les seules qui compteraient si la CP pilotait la décision)
  s'accordent à **~1e-16 à 1e-19**.
- Cellules k=0 : la forme fermée p_U = 1 − 0.05^(1/N) reproduit M2 à **Δ = 0** exact.
- Certificat `Fraction` (arithmétique rationnelle **exacte**) : la CDF binomiale exacte est
  évaluée aux **deux bornes flottantes** du bracket final ; elle traverse 1/20 dans le
  voisinage flottant du p_U rapporté (dans certaines cellules le vrai p_U tombe juste
  au-dessus de `hi`, dans d'autres juste au-dessous de `lo` — décalage sous la précision
  flottante), cohérent avec l'accord ≤ 1.21e-14 vs M2. Sauté pour 2 cellules à k très grand
  (agregateur/chainlink 0.15 %), non décisives, où M1==M2 suffit.
- k recalculés = k imprimés par le script (place 0.15 %→2 ; sans 0.15 %→48 ; agregateur
  1.00 %→7, 1.75 %→0 ; pyth→0).

**VERDICT CLAIM 2 (valeurs CP) : ✅ CONFIRMÉ.** Toutes les valeurs CP du script sont
arithmétiquement correctes (accord < 1.3e-14 sur 4 méthodes). **Mais voir OBSERVATION O1 :
la borne CP n'entre PAS dans le prédicat de sélection** — elle est calculée/imprimée mais
jamais testée, alors que la docstring et les justifications l'annoncent comme le pilote du
budget de fausse alarme. La correction des **valeurs** est confirmée ; leur **rôle annoncé**
est infirmé par le code (O1).

---

## 3. CLAIM 3 — épisodes 48 h et projection 26 j (= 13 ×), aux τ de la mission

Épisode = run maximal de fenêtres consécutives (pas = 60 s), agrégé (somme) par flux dans la
classe. Comptage réécrit indépendamment (compte des **débuts de run** ; le script compte les
sauts+1 — mêmes résultats). ep26 = 13 × ep48.

| classe | 0.15 % | 0.30 % | 1.00 % | 1.30 % | 1.75 % |
|---|---|---|---|---|---|
| oracle_pyth | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 |
| place_horodatee | 6 / **78** | **0 / 0** | 0 / 0 | 0 / 0 | 0 / 0 |
| sans_horodatage | 53 / **689** | **0 / 0** | 0 / 0 | 0 / 0 | 0 / 0 |
| agregateur | 476 / 6188 | 142 / 1846 | 6 / **78** | 3 / 39 | **0 / 0** |
| oracle_chainlink | 238 / 3094 | 154 / 2002 | 1 / 13 | **0 / 0** | 0 / 0 |

(format `ep48h / ep26j` ; **gras** = τ retenu de la classe / valeur imprimée par le script.)

Recoupements avec les valeurs **imprimées** par `derive_tau.py` (toutes exactes) :
place 0.15 %→ep48=6, ep26=78 ; sans 0.15 %→53, 689 ; agregateur 1.00 %→6, 78 ; 1.75 %→0, 0 ;
chainlink 1.30 %→ep26≈0. La projection 13× est correcte.

**VERDICT CLAIM 3 : ✅ CONFIRMÉ.** Écart nul aux τ vérifiables.

---

## 4. Contre-preuve à la main des maxima DÉCISIFS (arithmétique d'écart)

Recalcul de l'écart LOO **depuis les prix bruts** du journal, médiane réécrite (tri+milieu),
sans réutiliser la boucle de §1 (`spotcheck_dev.py`) :

- **sans_horodatage max = 0.296191 %** — bitfinex, ws=1787296560 (calme), N_resp=12.
  prix=76799 ; médiane_LOO (11 autres, 6ᵉ trié) = 76572.2 ;
  |76799 − 76572.2|/76572.2 = 226.8/76572.2 = **0.00296191…** ✔. **Décisif** : à un cheveu
  sous la grille 0.30 % (voir O2, sensibilité outlier).
- **place_horodatee max = 0.279436 %** — okx_ticker, ws=1787375400 (**stress**), N_resp=12.
  prix=76789.9 ; médiane_LOO=77005.08 ; 215.18/77005.08 = **0.00279436…** ✔. Confirme O3
  (le max décisif de place est en STRESS, pas dans la strate « lâche » calme).
- **agregateur max = 1.731879 %** — defillama, ws=1787302980 (calme), N_resp=12.
  prix=79194.13768868503 ; médiane_LOO=77845.94 ; 1348.19768868503/77845.94 =
  **0.01731879…** ✔.

---

## 5. CLAIM 4 — τ recommandés + invariant grid-ceil(global_max)

Sélection réécrite indépendamment. Classes quantile : plus petit τ de la grille
(0.15 % → 3.00 % pas 0.05 %) tel que `τ > P99(lâche)` **et** `13·ep48(τ) ≤ 4` **et** `τ < CAPO`
(2.85 %). Classe chainlink : `min{τ grille : τ ≥ 1.29 % (overshoot) et τ < CAPO}`.

| classe | τ recalculé | τ CLAIM 4 | verdict | P99(lâche) | global_max (2 strates) | grid-ceil(gmax) | invariant |
|---|---|---|---|---|---|---|---|
| oracle_pyth | 0.15 % | 0.15 % | ✅ | 0.054633 % | 0.074649 % | 0.15 % | chosen==grid-ceil ✅ |
| place_horodatee | 0.30 % | 0.30 % | ✅ | 0.068685 % | 0.279436 % | 0.30 % | ✅ |
| sans_horodatage | 0.30 % | 0.30 % | ✅ | 0.153130 % | 0.296191 % | 0.30 % | ✅ |
| agregateur | 1.75 % | 1.75 % | ✅ | 0.717712 % | 1.731879 % | 1.75 % | ✅ |
| oracle_chainlink | 1.30 % | 1.30 % | ✅ | 0.540174 % | 1.094640 % | (méca. 1.29 %→1.30 %) | overshoot ✅ |

**VERDICT CLAIM 4 : ✅ CONFIRMÉ.** Les 5 τ recommandés sont reproduits à l'identique.
Note de portée : la constante d'ancrage chainlink **1.29 %** (« dépassement inter-round max
mesuré ») est un **INTRANT EXTERNE** au journal (non recalculable depuis la calibration) —
je confirme seulement que la **dérivation** 1.30 % = plus petit pas grille ≥ 1.29 % (< CAPO)
est arithmétiquement juste ; la valeur 1.29 % relève d'une vérification de source, hors
périmètre du réfutant arithmétique.

---

## 6. OBSERVATIONS structurelles (matériel pour l'orchestrateur — pas des FAIL de 1–4)

Les 4 affirmations chiffrées sont arithmétiquement exactes. Les points suivants ne sont pas
des réfutations des valeurs, mais des **écarts méthode-annoncée / code** et des
**caractérisations** qui changent l'**interprétation** des τ. Ils sont, eux, matériels.

- **O1 — La borne Clopper-Pearson ne pilote RIEN dans la sélection.** Dans `derive_tau.py`,
  le prédicat de choix est `if chosen is None and okq and okbudget and okcapo`, avec
  `okbudget = (ep26 <= BUDGET_EPISODES)` et `ep26 = 13 * class_episodes_48h(...)` (l.174-176).
  `cpu = cp_upper(...)` (l.172) est **calculé et imprimé mais jamais lu** dans le test. Or la
  docstring (l.7-9 : « Borne de fausse-alarme : borne SUPÉRIEURE binomiale de
  Clopper-Pearson ») et la chaîne de justification (l.188 : « borne CP episodes26j <= 4 »,
  reprise dans la SÉLECTION imprimée) **attribuent le budget à la borne CP**. C'est faux : le
  budget est piloté par le **compte brut d'épisodes**, pas par la CP. Valeurs CP correctes
  (CLAIM 2), rôle annoncé infirmé.

- **O2 — Le « budget ≤ 4 épisodes/26 j » s'effondre en un ancrage EXTREME-VALUE (max).**
  `13·ep48 ≤ 4` avec ep48 entier ≥ 0 ⟺ **ep48 = 0** (car 4/13 < 1) ⟺ aucun écart `> τ` sur
  aucune fenêtre/flux de la classe (les 2 strates) ⟺ **τ ≥ global_max**. Vérifié
  empiriquement : « ep48==0 ⟺ τ≥gmax » vrai sur toutes les cellules. Donc, pour les 4 classes
  quantile, **τ recommandé = grid-ceil du plus grand écart honnête observé en 48 h** — un
  ancrage sur le **maximum**, ni un quantile ni un taux de fausse alarme. Conséquences :
  (a) **sensible à un seul outlier** — sans_horodatage gmax=0.296191 % est à ~4e-5 sous la
  grille 0.30 % ; un unique écart de 0.30001 % ferait basculer τ à 0.35 % ;
  (b) le plancher P99 (`τ > P99`) **n'est jamais contraignant** (grid-ceil(gmax) > P99 dans
  les 5 cas) — la « borne quantile » annoncée est structurellement inactive.

- **O3 — Le max décisif de `place_horodatee` vit dans la strate STRESS, pas dans la strate
  « lâche ».** gmax(place)=0.279436 % est en stress (max calme = 0.156820 % seulement). La
  calibration « sur la strate la plus lâche » (calme) ne décrit donc pas d'où vient l'écart
  qui FIXE τ pour place_horodatee. Cohérent avec O2 (l'ancre est le max global 2-strates).

- **O4 — `oracle_chainlink` : CP non calculée par le script** (saut `continue` l.162). Je l'ai
  calculée pour complétude (strate lâche calme, N=1440) : à 1.00/1.30/1.75 % → k=0 →
  CP=0.207821 %. Sans effet (chainlink suit l'ancre mécaniste ; CP décorative de toute façon,
  cf. O1). Note : gmax(chainlink)=1.094640 % < 1.30 %, donc l'ancre mécaniste (1.29 %→1.30 %)
  domine bien le max observé.

---

## 7. Verdict global et clôture (zéro dette)

| Affirmation | Verdict | Écart chiffré |
|---|---|---|
| CLAIM 1 — P99 par (classe, strate) | ✅ **CONFIRMÉ** | 0 (P99 recalc == imprimé ; nearest-rank == béni) |
| CLAIM 2 — bornes CP (valeurs) | ✅ **CONFIRMÉ** | ≤ 1.21e-14 sur 4 méthodes indép. |
| CLAIM 3 — épisodes 26 j (=13×) | ✅ **CONFIRMÉ** | 0 aux τ vérifiables |
| CLAIM 4 — τ recommandés | ✅ **CONFIRMÉ** | 0 (5/5 reproduits) |

**Aucun défaut arithmétique** dans les 4 affirmations chiffrées de `derive_tau.py`.
**Réserves méthodologiques matérielles** O1–O2 (la CP est morte dans la décision ; le
« budget » = ancrage sur le max 48 h, sensible à un outlier, plancher P99 inactif) et O3–O4,
à porter au G7 de l'orchestrateur — ce ne sont pas des « dûs » nus : ce sont des constats
sourcés dans le code (numéros de ligne) et dans mes recalculs reproductibles ci-dessus.

**Dette : néant.** Aucun point non résolu. Aucun intrant externe manquant sauf la constante
chainlink 1.29 % (explicitement hors périmètre arithmétique, relève d'une vérif de source —
signalée, non « due »). Modèle épinglé `claude-opus-4-8[1m]` effort max ; recalcul Decimal
prec fixée → bit-identique ; artefacts reproductibles listés au §0.

---

## 8. Annexe — scripts (verbatim, recalculables tels quels)

### 8.1 `refute_independent.py`

```python
"""REFUTANT ARITHMETIQUE (R-21) — recalcul INDEPENDANT de derive_tau.py (S2 Shogen).

Ne reexecute PAS derive_tau.py comme preuve : reimplemente chaque affirmation avec
son propre code. Machinerie de CHARGEMENT reutilisee (deja revue) : records.parse_control,
effective_run_params, sigma_tau_from_params ; r1._median, build_window_strate, parse_journal,
DECIMAL_PREC. L'ARITHMETIQUE de derivation (ecart honnete, P99 nearest-rank, Clopper-Pearson,
episodes, selection) est reecrite ici, ex nihilo, depuis la definition de la mission.

Clopper-Pearson : implemente 4 fois de facon INDEPENDANTE, dont 2 genuinement independantes
de la methode float log-space du script :
  (M1) bissection float log-space (methode prescrite par la mission ; ecriture propre) ;
  (M2) bissection sur CDF binomiale par RECURRENCE Decimal haute precision (prec=80) —
       precision-independante (ni log ni float) ;
  (CERT) certificat EXACT par Fraction (math.comb + Fraction(float)) au dernier bracket :
       CDF(lo) >= 1/20 >= CDF(hi), arithmetique rationnelle infinie (ou faisable) ;
  (K0) forme fermee k=0 : p_U = 1 - alpha^(1/N).
Reference cote-SCRIPT (transcription verbatim de cp_upper, PAS une preuve) pour tabuler la
valeur que le script produirait aux 25 cellules.
"""
import math
import os
import sys
from collections import defaultdict
from decimal import Decimal, localcontext
from fractions import Fraction

sys.path.insert(0, r"F:\Shogen\s2-harness")
from shogen_s2 import records
from shogen_s2.r1 import DECIMAL_PREC, _median, build_window_strate, parse_journal
from shogen_s2.closure import percentile_nearest_rank  # BLESSED — cross-check seulement

D = r"F:\shogen-campagne\calibration"
CAPO = Decimal("0.0285")
CHAINLINK_OVERSHOOT = Decimal("0.0129")
CALIB_TO_CAMP = 13
BUDGET = 4
GRID = [Decimal(x) / Decimal(10000) for x in range(15, 305, 5)]
CLASS_ORDER = ["oracle_pyth", "place_horodatee", "sans_horodatage", "agregateur", "oracle_chainlink"]
TAU_CP = [Decimal("0.0015"), Decimal("0.0030"), Decimal("0.0100"), Decimal("0.0130"), Decimal("0.0175")]
CLAIM4 = {"oracle_pyth": Decimal("0.0015"), "place_horodatee": Decimal("0.0030"),
          "sans_horodatage": Decimal("0.0030"), "agregateur": Decimal("0.0175"),
          "oracle_chainlink": Decimal("0.0130")}
# Mission class map (explicite) — verifie contre sigma_class_of_flux du journal.
MISSION_CLASSES = {
    "oracle_pyth": {"pyth"}, "oracle_chainlink": {"chainlink"},
    "agregateur": {"coingecko", "defillama"},
    "place_horodatee": {"coinbase", "gemini", "okx_ticker", "okx_index", "bitstamp"},
    "sans_horodatage": {"binance", "kraken", "bitfinex"},
}


# ============================= CHARGEMENT (machinerie revue) =============================
params_list, _ck, markers = records.parse_control(os.path.join(D, "control.jsonl"))
params = records.effective_run_params(params_list)
readings = parse_journal(os.path.join(D, "journal.jsonl"))
_sbc, sigma_class_of_flux, _tau = records.sigma_tau_from_params(params)
pool = list(params["pool"])
w = int(params["w"])
n_min = int(params["n_min_hors_enveloppe"])
win_strate = build_window_strate(markers)
rmap = {}
for r in readings:
    rmap[(int(r["window_start"]), r["flux_id"])] = r

# classes depuis sigma_class_of_flux (comme le script) + ASSERT contre la carte mission.
classes = defaultdict(list)
for f in pool:
    classes[sigma_class_of_flux.get(f)].append(f)
CLASSES = {k: list(v) for k, v in classes.items()}
for kl, members in MISSION_CLASSES.items():
    assert set(CLASSES.get(kl, [])) == members, (kl, CLASSES.get(kl), members)
assert set(pool) == set().union(*MISSION_CLASSES.values())
print(f"[check] carte de classes journal == carte mission : OK")
print(f"[check] w={w} n_min={n_min} DECIMAL_PREC={DECIMAL_PREC} "
      f"n_fenetres={len(win_strate)} pool={len(pool)}")


# ============ ECART RELATIF HONNETE — recalcul INDEPENDANT (definition mission) ============
dev_sc = defaultdict(lambda: defaultdict(list))   # strate -> classe -> [dev]
flux_devs = defaultdict(list)                      # flux -> [(ws, dev)]
strate_windows = defaultdict(int)
class_of = {f: sigma_class_of_flux.get(f) for f in pool}
with localcontext() as ctx:
    ctx.prec = DECIMAL_PREC
    for ws in sorted(win_strate):
        st = win_strate[ws]
        strate_windows[st] += 1
        resp = [f for f in pool
                if rmap.get((ws, f)) is not None
                and rmap[(ws, f)].get("status") == "ok"
                and rmap[(ws, f)].get("price") is not None]
        rp = {f: Decimal(rmap[(ws, f)]["price"]) for f in resp}
        if len(resp) >= n_min:
            for f in resp:
                m = _median([rp[g] for g in resp if g != f])
                if m > 0:
                    d = abs(rp[f] - m) / m
                    dev_sc[st][class_of[f]].append(+d)
                    flux_devs[f].append((ws, +d))
strates = sorted(strate_windows)
print(f"[check] fenetres/strate : " + " ; ".join(f"{s}={strate_windows[s]}" for s in strates))


# ================================= P99 nearest-rank INDEPENDANT =================================
def my_p99(values):
    """nearest-rank : rang = ceil(99*N/100) (1-indexe), entier exact via -(-a//b)."""
    if not values:
        return None
    s = sorted(values)
    N = len(s)
    rank = -(-(99 * N) // 100)      # ceil(99N/100)
    rank = max(1, min(rank, N))
    return s[rank - 1]


def loose_strate(kl):
    best, bp = None, None
    for st in strates:                      # ordre trie -> calme avant stress ; strict >
        p = my_p99(dev_sc[st][kl])
        if p is not None and (bp is None or p > bp):
            bp, best = p, st
    return best, bp


def class_global_max(kl):
    vals = [d for f in CLASSES[kl] for (_ws, d) in flux_devs[f]]
    return max(vals) if vals else None


def strate_class_max(st, kl):
    v = dev_sc[st][kl]
    return max(v) if v else None


def pct(x):
    return "None" if x is None else f"{(x * 100):.6f}%"


# ================================= CLOPPER-PEARSON — 4 methodes =================================
def _log_pmf(i, n, p):
    return (math.lgamma(n + 1) - math.lgamma(i + 1) - math.lgamma(n - i + 1)
            + i * math.log(p) + (n - i) * math.log1p(-p))


def _cdf_float(k, n, p):                      # P(X<=k), float log-space + shift (M1, propre)
    if p <= 0.0:
        return 1.0
    if p >= 1.0:
        return 1.0 if k >= n else 0.0
    xs = [_log_pmf(i, n, p) for i in range(k + 1)]
    mx = max(xs)
    return math.exp(mx) * sum(math.exp(t - mx) for t in xs)


def cp_M1(k, n, alpha=0.05):                  # bissection float log-space
    if n == 0 or k >= n:
        return 1.0
    lo, hi = k / n, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2.0
        if _cdf_float(k, n, mid) > alpha:
            lo = mid
        else:
            hi = mid
    return hi


def _cdf_decimal(k, n, p, prec=80):           # P(X<=k) par recurrence pmf, Decimal (M2)
    with localcontext() as ctx:
        ctx.prec = prec
        p = p if isinstance(p, Decimal) else Decimal(p)
        q = Decimal(1) - p
        if p <= 0:
            return Decimal(1)
        if q <= 0:
            return Decimal(1) if k >= n else Decimal(0)
        term = q ** n                          # pmf(0)
        total = term
        for i in range(0, k):                  # pmf(i+1)=pmf(i)*(n-i)/(i+1)*p/q
            term = term * Decimal(n - i) / Decimal(i + 1) * p / q
            total += term
        return +total


def cp_M2(k, n, alpha=Decimal("0.05"), prec=80, iters=300):
    if n == 0 or k >= n:
        return Decimal(1)
    with localcontext() as ctx:
        ctx.prec = prec
        lo, hi = Decimal(k) / Decimal(n), Decimal(1)
        for _ in range(iters):
            mid = (lo + hi) / 2
            if _cdf_decimal(k, n, mid, prec) > alpha:
                lo = mid
            else:
                hi = mid
        return +hi


def cp_K0_closed(n, alpha=Decimal("0.05"), prec=80):   # p_U = 1 - alpha^(1/N)
    with localcontext() as ctx:
        ctx.prec = prec
        return +(Decimal(1) - (alpha.ln() / Decimal(n)).exp())


def _cdf_fraction(k, n, p_float):             # CDF exacte (rationnelle) au float p ; tail min
    p = Fraction(p_float)
    q = 1 - p
    if k >= n:
        return Fraction(1)
    if k < 0:
        return Fraction(0)
    if k + 1 <= n - k:                          # somme basse (k+1 termes)
        return sum(math.comb(n, i) * p ** i * q ** (n - i) for i in range(k + 1))
    return 1 - sum(math.comb(n, i) * p ** i * q ** (n - i) for i in range(k + 1, n + 1))


def cp_cert_fraction(k, n, alpha=Fraction(1, 20), max_terms=400):
    """Certificat exact : bracket float [lo,hi] adjacent tel que CDF_exact(lo) >= 1/20 >= CDF_exact(hi).
    Retourne (lo, hi, cdf_lo>=alpha, cdf_hi<=alpha, applique?)."""
    if n == 0 or k >= n:
        return (None, None, None, None, False)   # CP=1 trivial
    if min(k + 1, n - k) > max_terms:
        return (None, None, None, None, False)   # trop couteux — saute (note)
    lo, hi = k / n, 1.0
    af = float(alpha)
    for _ in range(200):                          # bissection float -> bracket ULP-adjacent
        mid = (lo + hi) / 2.0
        if _cdf_float(k, n, mid) > af:
            lo = mid
        else:
            hi = mid
    clo = _cdf_fraction(k, n, lo)
    chi = _cdf_fraction(k, n, hi)
    return (lo, hi, clo >= alpha, chi <= alpha, True)


# transcription VERBATIM de derive_tau.cp_upper (reference cote-SCRIPT, PAS une preuve)
def _script_log_binom_pmf(k, n, p):
    if p <= 0.0:
        return 0.0 if k == 0 else float("-inf")
    if p >= 1.0:
        return 0.0 if k == n else float("-inf")
    return (math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)
            + k * math.log(p) + (n - k) * math.log1p(-p))


def _script_binom_cdf(k, n, p):
    terms = [_script_log_binom_pmf(i, n, p) for i in range(k + 1)]
    m = max(terms)
    return math.exp(m) * sum(math.exp(t - m) for t in terms)


def script_cp_upper(k, n, alpha=0.05):
    if n == 0:
        return 1.0
    if k >= n:
        return 1.0
    lo, hi = k / n, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2.0
        if _script_binom_cdf(k, n, mid) > alpha:
            lo = mid
        else:
            hi = mid
    return hi


# ===================================== EPISODES INDEPENDANT =====================================
def n_episodes_indep(ws_list, w):
    """runs maximaux de fenetres consecutives (pas=w) ; compte les DEBUTS de run."""
    if not ws_list:
        return 0
    s = sorted(ws_list)
    return sum(1 for i in range(len(s)) if i == 0 or s[i] - s[i - 1] != w)


def class_episodes_48h(kl, tau):
    return sum(n_episodes_indep([ws for (ws, d) in flux_devs[f] if d > tau], w)
               for f in CLASSES[kl])


# ===================================== SELECTION INDEPENDANTE =====================================
def grid_ceil(x):
    for tau in GRID:
        if tau >= x:
            return tau
    return None


def select_quantile(kl):
    st, p99 = loose_strate(kl)
    for tau in GRID:
        if tau >= CAPO:
            break
        ep26 = CALIB_TO_CAMP * class_episodes_48h(kl, tau)
        okq = tau > p99
        okbudget = ep26 <= BUDGET
        okcapo = tau < CAPO
        if okq and okbudget and okcapo:
            return tau, st, p99
    return None, st, p99


def select_chainlink():
    cand = [t for t in GRID if t >= CHAINLINK_OVERSHOOT and t < CAPO]
    return min(cand)


# ========================================= AFFICHAGE =========================================
print("\n" + "=" * 90)
print("CLAIM 1 — P99 (nearest-rank) par (classe, strate), N, max ; strate lache")
print("=" * 90)
p99_loose = {}
for kl in CLASS_ORDER:
    row = []
    for st in strates:
        v = dev_sc[st][kl]
        p_mine = my_p99(v)
        p_blessed = percentile_nearest_rank(v, 99)
        agree = (p_mine == p_blessed)
        row.append((st, len(v), p_mine, p_blessed, agree, strate_class_max(st, kl)))
    st_l, p_l = loose_strate(kl)
    p99_loose[kl] = (st_l, p_l)
    gmax = class_global_max(kl)
    print(f"\n### {kl}  [{','.join(CLASSES[kl])}]  -> strate lache = {st_l}")
    for (st, N, pm, pb, ag, mx) in row:
        flag = "  <== LACHE" if st == st_l else ""
        print(f"   {st:7s} N={N:5d}  P99={pct(pm)}  (blessed={pct(pb)} {'==' if ag else '!!DIFF'})"
              f"  max={pct(mx)}{flag}")
    print(f"   global_max(2 strates)={pct(gmax)}   grid_ceil(global_max)={pct(grid_ceil(gmax))}")

print("\n" + "=" * 90)
print("CLAIM 2 — Clopper-Pearson borne SUP unilaterale 95%, strate lache, 4 methodes independantes")
print("   colonnes: k/N  M1(logspace)  M2(Decimal)  |M1-M2|  scriptRef  |M2-script|  K0/CERT")
print("=" * 90)
cp_maxdiff_indep = 0.0
cp_maxdiff_script = 0.0
for kl in CLASS_ORDER:
    st_l, p_l = p99_loose[kl]
    v = dev_sc[st_l][kl]
    N = len(v)
    note = "  (script SAUTE chainlink CP via continue)" if kl == "oracle_chainlink" else ""
    print(f"\n### {kl}  strate lache={st_l}  N={N}{note}")
    for tau in TAU_CP:
        k = sum(1 for d in v if d > tau)
        m1 = cp_M1(k, N, 0.05)
        m2 = float(cp_M2(k, N))
        sref = script_cp_upper(k, N, 0.05)
        d_indep = abs(m1 - m2)
        d_script = abs(m2 - sref)
        cp_maxdiff_indep = max(cp_maxdiff_indep, d_indep)
        cp_maxdiff_script = max(cp_maxdiff_script, d_script)
        extra = ""
        if k == 0:
            k0 = float(cp_K0_closed(N))
            extra = f"  K0={k0*100:.6f}% (|M2-K0|={abs(m2-k0):.2e})"
        else:
            lo, hi, clo_ok, chi_ok, applied = cp_cert_fraction(k, N)
            if applied:
                extra = f"  CERT[CDF(lo)>=1/20:{clo_ok}, CDF(hi)<=1/20:{chi_ok}]"
            else:
                extra = f"  CERT skip (k={k}, min-terms>{min(k+1,N-k)})"
        print(f"   tau={float(tau)*100:5.2f}%  k={k:5d}/{N:<5d}  M1={m1*100:8.5f}%  M2={m2*100:8.5f}%"
              f"  |M1-M2|={d_indep:.2e}  script={sref*100:8.5f}%  |M2-scr|={d_script:.2e}{extra}")
print(f"\n[CP] max |M1-M2| (methodes independantes) = {cp_maxdiff_indep:.3e}")
print(f"[CP] max |M2-script|  (independant vs script)  = {cp_maxdiff_script:.3e}")

print("\n" + "=" * 90)
print("CLAIM 3 — episodes 48h et projection 26j (=13x), par classe, aux tau CP + tau choisi")
print("=" * 90)
for kl in CLASS_ORDER:
    taus = list(TAU_CP)
    ch = CLAIM4[kl]
    if ch not in taus:
        taus.append(ch)
    taus = sorted(set(taus))
    print(f"\n### {kl}  gmax={pct(class_global_max(kl))}")
    for tau in taus:
        ep48 = class_episodes_48h(kl, tau)
        ep26 = CALIB_TO_CAMP * ep48
        tag = "  <-- tau CLAIM4" if tau == ch else ""
        print(f"   tau={float(tau)*100:5.2f}%  ep48h={ep48:4d}  ep26j={ep26:5d}"
              f"  (ep48==0 <=> tau>=gmax: {tau >= class_global_max(kl)}){tag}")

print("\n" + "=" * 90)
print("CLAIM 4 — selection recommandee INDEPENDANTE + invariant grid-ceil(global_max)")
print("=" * 90)
final = {}
for kl in CLASS_ORDER:
    if kl == "oracle_chainlink":
        chosen = select_chainlink()
        final[kl] = chosen
        claim = CLAIM4[kl]
        ok = (chosen == claim)
        print(f"   {kl:18s} [mecaniste] chosen={float(chosen)*100:.2f}%  "
              f"(min grid >= overshoot {float(CHAINLINK_OVERSHOOT)*100:.2f}%, < CAPO)  "
              f"claim4={float(claim)*100:.2f}%  {'PASS' if ok else 'FAIL'}")
        continue
    chosen, st_l, p99 = select_quantile(kl)
    final[kl] = chosen
    claim = CLAIM4[kl]
    gmax = class_global_max(kl)
    gc = grid_ceil(gmax)
    ok = (chosen == claim)
    inv = (chosen == gc)
    print(f"   {kl:18s} [quantile ] chosen={float(chosen)*100:.2f}%  claim4={float(claim)*100:.2f}%  "
          f"{'PASS' if ok else 'FAIL'}   | P99({st_l})={pct(p99)}  gmax={pct(gmax)}  "
          f"grid_ceil={pct(gc)}  invariant(chosen==grid_ceil): {'OK' if inv else 'X'}")

print("\n[VERDICT-DATA] final selection recomputee :",
      {k: f"{float(v)*100:.2f}%" for k, v in final.items()})
print("[VERDICT-DATA] claim4                      :",
      {k: f"{float(v)*100:.2f}%" for k, v in CLAIM4.items()})
print("[VERDICT-DATA] selection == claim4 :", all(final[k] == CLAIM4[k] for k in CLASS_ORDER))
```

### 8.2 `spotcheck_dev.py`

```python
"""Spot-check EXACT et tracable a la main de l'ecart honnete, pour les maxima DECISIFS.
Recalcule l'ecart LOO d'une cellule (fenetre,flux) DEPUIS LES PRIX BRUTS du journal,
sans reutiliser la boucle de refute_independent : preuve que l'arithmetique d'ecart est juste.
"""
import os
import sys
from decimal import Decimal, localcontext
from collections import defaultdict

sys.path.insert(0, r"F:\Shogen\s2-harness")
from shogen_s2 import records
from shogen_s2.r1 import DECIMAL_PREC, build_window_strate, parse_journal

D = r"F:\shogen-campagne\calibration"
params_list, _ck, markers = records.parse_control(os.path.join(D, "control.jsonl"))
params = records.effective_run_params(params_list)
readings = parse_journal(os.path.join(D, "journal.jsonl"))
_sbc, scof, _tau = records.sigma_tau_from_params(params)
pool = list(params["pool"]); w = int(params["w"]); n_min = int(params["n_min_hors_enveloppe"])
win_strate = build_window_strate(markers)
rmap = {}
for r in readings:
    rmap[(int(r["window_start"]), r["flux_id"])] = r

CLASSES = defaultdict(list)
for f in pool:
    CLASSES[scof.get(f)].append(f)


def median_by_hand(xs):
    """mediane INDEPENDANTE (tri + milieu), sans r1._median."""
    s = sorted(xs)
    m = len(s)
    if m % 2 == 1:
        return s[m // 2]
    return (s[m // 2 - 1] + s[m // 2]) / Decimal(2)


def all_devs_for_class(kl):
    out = []  # (dev, ws, flux)
    with localcontext() as ctx:
        ctx.prec = DECIMAL_PREC
        for ws in sorted(win_strate):
            resp = [f for f in pool
                    if rmap.get((ws, f)) is not None
                    and rmap[(ws, f)].get("status") == "ok"
                    and rmap[(ws, f)].get("price") is not None]
            if len(resp) < n_min:
                continue
            rp = {f: Decimal(rmap[(ws, f)]["price"]) for f in resp}
            for f in resp:
                if f not in CLASSES[kl]:
                    continue
                others = [rp[g] for g in resp if g != f]
                m = median_by_hand(others)
                if m > 0:
                    out.append((abs(rp[f] - m) / m, ws, f))
    return out


for kl in ["sans_horodatage", "place_horodatee", "agregateur"]:
    devs = all_devs_for_class(kl)
    dmax, ws, f = max(devs, key=lambda t: t[0])
    st = win_strate[ws]
    resp = [g for g in pool
            if rmap.get((ws, g)) is not None
            and rmap[(ws, g)].get("status") == "ok"
            and rmap[(ws, g)].get("price") is not None]
    with localcontext() as ctx:
        ctx.prec = DECIMAL_PREC
        rp = {g: Decimal(rmap[(ws, g)]["price"]) for g in resp}
        others = sorted(rp[g] for g in resp if g != f)
        m = median_by_hand([rp[g] for g in resp if g != f])
        dev = abs(rp[f] - m) / m
    print(f"\n### {kl}: MAX ecart honnete = {dev*100:.6f}%  (strate={st}, flux={f}, ws={ws}, N_resp={len(resp)})")
    print(f"    prix[{f}] = {rp[f]}")
    print(f"    mediane_LOO (n={len(others)} autres) = {m}")
    print(f"    |prix - mediane|/mediane = |{rp[f]} - {m}| / {m}")
    print(f"       = {abs(rp[f]-m)} / {m} = {dev} = {dev*100:.6f}%")
    print(f"    prix des autres (tries): {[str(x) for x in others]}")
```

Fin de l'annexe. Les deux scripts s'exécutent tels quels (Python 3.11, stdlib seule +
`numpy` non requis ; `scipy`/`mpmath` absents — d'où l'implémentation Clopper-Pearson maison).
