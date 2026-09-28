# G1 — lot « filtre d'exclusion » ADR-0025 (Shōgen S2), lot A — journal

- **Modèle** : `claude-opus-5-5` (identifiant résolu déclaré par le harnais : `claude-opus-5-5[1m]`), effort max, contexte frais ; worker G1 (aucun git écrivant, aucun commit).
- **Horloge** (`date -u`) : début 2026-09-28T03:09:19Z ; scellés vérifiés 03:11:24Z ; campagne de mutants 03:29:09Z → 03:30:06Z ; suites finales 03:30:15Z et 03:30:17Z ; mesure du déclencheur 03:30:39Z ; journal écrit 03:33Z.
- **Mandat** : `F:\tmp\shogen-j28\mission-adr0025-filtre.md`, Partie 2, avec les corrections C-1..C-8 du checkpoint-1. Décision investisseur 269 : « go pour ADR-0025, exclusion de la plage entière » ; DOCTRINE D-5 : le dossier Shōgen fait le plan, rien n'y est réécrit ici.
- **Classification (D-4 (e))** : **bounded**. Le flux à modifier existait déjà (lecteur `records` → `r1`/`lm`/`r2` → `report`).
- **Base** : `F:\Shogen`, branche `main`, HEAD `5f4d40b`, arbre propre. Le harnais n'a pas changé depuis `ed479c5` (2026-08-26).
- **Destination de ce fichier** : `F:\Shogen\docs\G1-lot-adr0025-filtre.md`. Il est livré dans `adr0025-deliver\` parce que le dépôt est en lecture seule hors fichiers du harnais (voir Q-G1-1).

## 0. Étape 0 — baseline D-4 (c), arbre de base, avant tout code
- `sha256sum -c SHA256SUMS-cloture-2026-09-28.txt` dans `campagne\` (lecture seule) : OK pour les cinq fichiers. Copies de travail dans `work\campagne-copie\` : `control.jsonl` 351f51b2…66ff et `journal.jsonl` 98c5793e…5d74, identiques aux scellés, en lecture seule.
- Copie de l'arbre de base dans `work\base-s2-harness\` (= HEAD). Le sha de chaque fichier est dans `sorties\base-sha256.txt`.
- Suite sur la base : **173 tests OK** en 1,8 s. Le README du harnais dit « 136 verts » : c'est périmé (Q-G1-5).
- `r1.recompute_from_journal` (base) sur les copies : **10,7 s**. `effective_run_params` ne lève pas sur **4 093** `run_params`. 40 807 lignes `window_close`, **38 600** fenêtres distinctes, **2 207** doublons. **n calme 26 294, n stress 12 306.** Les autres chiffres R1 de cette sortie ne sont pas repris : leur lecture revient au lot J28 (sortie caviardée livrée, Q-G1-6).
- Mesure indépendante de la borne sur la copie (C-1) : intervalle fermé ⇒ **2 617** (calme 1 709, stress 908). [A;B) ⇒ 2 616 (stress 907) ; (A;B] ⇒ 2 616 (calme 1 708). Il existe donc une fenêtre exactement sur A (18:18Z) et une exactement sur B (15:07Z).

## 1. Coupe R-25 (C-6)
- Estimation ascendante faite avant le code : lot A ≈ 190 lignes (code ≈ 55, tests ≈ 135) ; lot B (sensibilité + couverture week-end) ≈ 85 lignes (table ≈ 22, couverture ≈ 18, tests ≈ 45). **A + B ≈ 275 > 200, donc le G1 s'arrête au lot A.** Le lot B devient le lot suivant sous la même ADR (Q-G1-3).
- Méthode de mesure : `git diff --numstat` sur les cinq modules (**+48 −9**), plus `wc -l` du fichier neuf `tests/test_exclusion.py` (**148**). Total : **196 lignes ajoutées ≤ 200**. La première mesure donnait 222 lignes, gonflées par des docstrings et commentaires redondants. Je les ai resserrés sans retirer aucune assertion ; le cas « plage inversée » est passé dans le test (i).

## 2. Changements (en place, `F:\Shogen\s2-harness`)
| fichier | changement | sha256 avant → après |
|---|---|---|
| `shogen_s2/records.py` | `exclusion_ranges(ranges)` : bornes entières, **triées**, `from > to` ⇒ `ValueError`. `exclude_window_start_ranges(markers, ranges)` : filtre **fermé** `[from, to]` sur `window_start`, pur | 21daf729… → ea4d6da2… |
| `shogen_s2/r1.py` | `recompute_from_journal(…, exclude_ranges=())` : filtre **après** `verify_markers_against_spec` | 084aeaa5… → 3d8931f7… |
| `shogen_s2/lm.py` | `recompute_lm_from_journal(…, exclude_ranges=())`, même point d'application | 2a25d187… → d21f8d08… |
| `shogen_s2/r2.py` | `recompute_r2_from_journal(…, exclude_ranges=())`, même point d'application | 8c42f336… → 1acf2ba3… |
| `shogen_s2/report.py` | `render_report(…, exclude_ranges=())` : plages normalisées d'abord, filtre après la garde, blocs 2 à 6 sur les fenêtres retenues. Bloc 1 : une ligne par plage (epoch, ISO-8601 UTC, motif « harnais dégradé, ADR-0025 »), **seulement si un filtre est posé**. `main` passe à `argparse` avec l'option répétable `--exclude-window-start-range FROM_EPOCH TO_EPOCH` ; le dossier reste positionnel | fc81f753… → 74d0408b… |
| `tests/test_exclusion.py` | neuf (5 tests) | — → f90218ab… |

- **Modules intouchés** (sha = base) : `journal.py` (l'écrivain, contrat `records.py` l. 3-4), `model.py`, `sources.py`, `closure.py`, `window.py`, `collector.py`, `run_campaign.py`.
- **Lectures non filtrées** (C-2, défense non retenue) : les lectures d'une fenêtre retirée deviennent orphelines. Aucune sortie ne consomme de lecture sans marqueur (`test_absent_and_orphan_windows_not_counted`). Aucun mutant n'est revendiqué sur ce point.
- **C-7** : `grep -rn "1790273880\|1790435220\|2617\|2 617\|18:18\|15:07\|35983\|1709" shogen_s2/` ne renvoie rien. Les valeurs d'ADR-0025 ne figurent que dans `tests/` et dans ce journal.
- **Commande pour le lot J28** (non lancée ici) : `python -m shogen_s2.report <dir> --exclude-window-start-range 1790273880 1790435220`, soit [2026-09-24T18:18:00Z ; 2026-09-26T15:07:00Z]. Ligne de bloc 1 rendue sur la fixture (plage [w2 ; w4]) :
  `exclusion_window_start   = [1786147140 ; 1786147260] = [2026-08-07T23:59:00+00:00 ; 2026-08-08T00:01:00+00:00] fermée, bornes incluses : hors n, K, P̂_more de toutes les strates (filtre du lecteur, journal intact) — harnais dégradé, ADR-0025`
- **Entrées fautives** : une plage inversée lève `ValueError` (rc=1). Sans dossier, argparse affiche son usage et sort avec rc=2, le même code qu'avant.

## 3. Dédoublonnage (point 2)
Le lecteur fait déjà deux choses. `r1.build_window_strate` déduplique les marqueurs par `window_start` ; le dernier marqueur fixe la strate, et toutes les strates ont été vérifiées contre le calendrier avant le filtre. `r1.build_reading_map` applique last-wins par (fenêtre, flux) pour les lectures. Des tests existants couvrent ces deux règles : `test_marker_dedup_counts_window_once`, `test_reading_last_wins`, `test_duplicate_window_counted_once_end_to_end`, `test_second_run_appends_and_is_idempotent`.

Mesures sur la copie :
- Les **2 207** fenêtres doublées sont **toutes** dans [18:18Z ; 15:07Z]. Hors plage : 0. Première : 18:18Z, dernière : 15:07Z, multiplicité au plus 2. Une fois la plage exclue, la déduplication n'a **aucun effet sur n**.
- Le « +11 depuis » de la CLÔTURE s'explique : l'incident comptait 2 196 doublons au recompte de 14:57Z, et il y a exactement 11 fenêtres doublées de 14:57Z à 15:07Z. Toutes sont dans la plage.
- Lectures : 26 205 paires (fenêtre, flux) doublées, dont 26 199 dans la plage. Hors plage, une seule fenêtre est touchée : **2026-09-26T15:08Z**, avec 6 flux doublés et 1 marqueur. La chaîne B a été tuée à 15:08:53Z en pleine fenêtre. Last-wins s'y applique ; voir Q-G1-2.

## 4. Tests (stdlib `unittest`, forme de `tests/`) — chaque test nomme la mutation qui le rougit
- **Fixture synthétique** : collecteur réel, horloge scriptée, calendrier week-end. Six fenêtres w0..w5, du ven. 23:57Z au sam. 00:02Z. Une reprise w1..w3 crée des doublons : w1 hors plage, w2 et w3 dans la plage. La plage [w2 ; w4] est posée sur des débuts de fenêtre des deux strates ; w4 est une fenêtre de la plage à écriture unique.
- **(i)** `test_i_n_exact_bornes_fermees_doublons` : n par strate identique aux **quatre** points d'entrée (r1, lm, `r2.content.n_windows`, bloc 3 du rendu). Sans plage : {calme 3, stress 3}. Avec la plage : {calme 2, stress 1}. Une plage inversée lève. Rougit si : une borne est exclusive ; la plage est ignorée dans une strate ; la déduplication est cassée ; un point d'entrée ignore la plage ; une plage inversée est acceptée.
- **garde §5.3** `test_garde_53_voit_les_marqueurs_exclus` : w3 (samedi, dans la plage) est ré-étiqueté « calme » ; les quatre points d'entrée lèvent quand même. Rougit si le filtre passe avant `verify_markers_against_spec`.
- **(iii)** `test_iii_deterministe_et_bloc1_par_la_cli` : deux processus CLI (PYTHONHASHSEED 1 et 2, plages en ordre inverse) produisent les mêmes octets, identiques à l'API suivie d'un saut de ligne. Le bloc 1 porte chaque plage en epoch et en ISO avec le motif. Rougit si : le tri est retiré ; les paramètres manquent au bloc 1 ; l'option n'est pas transmise.
- **(iv)** `test_iv_sans_option_octets_d_avant_le_lot` : sans option, le sha256 du rendu vaut **a4ffc3e5…49a5**. Ce sha a été capturé sur l'**arbre de base** par `capture_golden_base.py`, deux fois, avec des fixtures identiques à l'octet. La CLI `report <dir>` (RUNBOOK §9 e) émet ces octets tels quels. Rougit si une ligne est ajoutée sans filtre ou si la sortie de la CLI sans option change. Contrôle croisé pour G2, sans rien rejouer : `sha256sum sorties/golden-render-base.txt` = `SHA_BASE_SANS_OPTION` (a4ffc3e5…49a5, voir `DELIVERED.sha256`).
- **(ii)** `test_ii_plage_adr0025_retire_2617_fenetres` : lit `control.jsonl` seul, via `SHOGEN_S2_CAMPAGNE_CONTROL`. Sans la variable, il lève `SkipTest` avec un message explicite. Il vérifie le sha 351f51b2… et que `effective_run_params` et la garde §5.3 passent. Avant : {calme 26 294, stress 12 306} (38 600). Après : {calme 24 585, stress 11 398} (35 983). Différence : {calme 1 709, stress 908} = **2 617, soit le chiffre d'ADR-0025 sans ajustement**. Rougit si une borne est exclusive (2 616) ou si la plage est ignorée dans une strate.
- **Exécutions** (TMP et TEMP sur `F:\tmp\shogen-j28\work\tmp`) :
  - Sans la variable, 03:30:15Z : `Ran 178 tests … OK (skipped=1)`, avec le message « SHOGEN_S2_CAMPAGNE_CONTROL absente : copie du control.jsonl scellé non fournie, test (ii) NON exécuté ».
  - Avec `SHOGEN_S2_CAMPAGNE_CONTROL=F:\tmp\shogen-j28\work\campagne-copie\control.jsonl`, 03:30:17Z : `Ran 178 tests in 3.008s — OK`, et `test_ii_plage_adr0025_retire_2617_fenetres … ok`. Les sorties complètes sont dans `sorties\suite-{sans,avec}-variable.out`.
  - Bilan : 173 tests de base, plus 5 nouveaux, donne 178.

## 5. Mutants (en place, suite complète avec la variable posée, sans bytecode) — `mutants.py`, sortie `sorties\mutants.out`
| # | mutant | rougi par |
|---|---|---|
| M1a | borne exclusive haute [A;B) (`records`) | (i), (ii) |
| M1b | borne exclusive basse (A;B] (`records`) | (i), (ii) |
| M2 | plage ignorée dans la strate stress (`records`) | (i), (ii) |
| M3 | déduplication des marqueurs cassée : `compute_r1` groupe les marqueurs bruts (`r1`) | (i), (iv), `test_second_run_appends_and_is_idempotent`, `test_duplicate_window_counted_once_end_to_end` |
| M4 | paramètres d'exclusion absents du bloc 1 (`report`) | (iii) |
| M5 ×4 | plage ignorée par un point d'entrée : r1, lm, r2, report | (i) |
| M6 ×4 | filtre appliqué **avant** la garde §5.3 : r1, lm, r2, report | garde §5.3 |
| M7 | tri des plages retiré (`records`) | (iii) |
| M8 | ligne « exclusion : aucune » sans filtre (`report`) | (iv) |
| M9 | plage inversée acceptée (`records`) | (i) |
| M10 | option CLI non transmise à `render_report` (`report`) | (iii) |

**17 mutants, 17 tués, 0 survivant.** Les quatre mutants demandés par la mission sont M1, M2, M3 et M4. Après chaque mutant, le module a été restauré et son sha256 vérifié contre `sorties\post-lot-sha256.txt` : tous OK. La suite complète est verte après la campagne.

## 6. Déclencheur ADR-0025 point 5 (C-8) — fait mesuré, aucune décision
Mesure faite avec le code du lot (`mesure_declencheur.py`) sur la copie de `control.jsonl` (sha 351f…), marqueurs seulement, avec w = 60 s tiré de `run_params`.
- **Strate stress après exclusion : 11 398 fenêtres = 189,97 h ≈ 190,0 h ≥ 166,8 h.** Le déclencheur du point 5 **n'est pas atteint**. La projection « ≈ 190,0 h » d'ADR-0025 se vérifie, à la valeur attendue par C-8.
- Calme après exclusion : 24 585 fenêtres = **409,8 h**. Avant exclusion : stress 205,1 h, calme 438,2 h.

## 7. Tuyaux CA-11 (règle Branchement)
- **Entrée** : les journaux scellés `campagne\control.jsonl` et `journal.jsonl`, produits par le pilote `run_campaign`, clos le 28/09 à 01:27Z. Les plages sont données par l'opérateur sur la ligne de commande, avec les valeurs d'ADR-0025 déc. 1.
- **Lecteur** : `parse_control` → `effective_run_params` → `verify_markers_against_spec` sur **tous** les marqueurs → `exclude_window_start_ranges` → `compute_r1`, `compute_lm`, `compute_r2`. Les quatre points d'entrée prennent le même paramètre.
- **Table** : `render_report`. Le bloc 1 consigne les plages ; les blocs 2 à 6 portent sur les fenêtres retenues. Le **chemin servi** est la CLI `python -m shogen_s2.report` (RUNBOOK §9 e).
- **Sortie aval** : le rapport J28, qui est **le lot suivant**, après le G2 de celui-ci. Ce tuyau n'est pas encore branché. Il est suivi comme item formé, avec pour déclencheur le G0 du lot J28, qui doit reprendre la commande du §2.
- **État** : aucun état persistant. Les plages vivent dans l'argument de ligne de commande et sont consignées dans la sortie. Le journal n'est jamais modifié.
- **Tests qui rejouent la composition** : (i) pour les quatre points d'entrée et le rendu ; (iii) et (iv) pour la CLI dans un processus neuf ; (ii) pour les marqueurs du journal réel scellé.

## 8. Risques MAST nommés (CA-5) et contre-mesures
- **FM-2.3, dérive de tâche** (lancer le rapport J28 complet, ou calculer le z filtré sur le journal réel). Contre-mesure : (ii) et le déclencheur ne lisent que `control.jsonl` ; aucun rendu ni recompute filtré n'a tourné sur le journal réel ; aucune statistique R1 n'est reprise ici.
- **FM-1.1 / FM-3.3, désobéissance à la spécification ou vérification incorrecte** (ajuster le 2 617 en silence). Contre-mesure : (ii) affirme le chiffre de l'ADR contre le sha scellé ; la sensibilité aux bornes est mesurée et consignée au §0 ; aucun paramètre n'a été réglé.
- **FM-2.6, écart entre raisonnement et action** (fabriquer un z poolé). Contre-mesure : aucune strate poolée n'est ajoutée (C-3, Q-1) ; la sensibilité est reportée au lot B.
- **FM-1.5, conditions d'arrêt ignorées** (gros lot « efficace »). Contre-mesure : coupe C-6 appliquée ; mesure à 196 lignes.

## 9. `error_origin` proposés (à assigner au G7)
- **E-1** : README du harnais, « 136 verts » contre 173 mesurés sur la base. Origine : documentation non mise à jour aux lots driver et clôture.
- **E-2** : fenêtre 2026-09-26T15:08Z, 6 lectures doublées hors de la plage d'ADR-0025. Origine : harnais (garde de relance, INCIDENT). La plage n'a pas été ajustée.
- **E-3** : chemin du journal (`docs/…`) incompatible avec un dépôt en lecture seule. Origine : mission (spécification).
- **E-4** : estimation R-25 à ≈ 190 contre 222 à la première mesure. Origine : worker (docstrings sous-estimées). Corrigé à 196 sans retirer d'assertion.
- **E-5** : fichier de test écrit d'abord en CRLF (`grep -c $'\r'` mal lu sous Git Bash) alors que le dépôt est en LF (`git ls-files --eol` : w/lf). Origine : worker (outillage). Détecté par la campagne de mutants et converti en LF avant le sha post-lot ; les livrables ne sont pas touchés.

## 10. Review Focus (cinq classes d'entrée non couvertes)
1. **Plages chevauchantes ou emboîtées** (liée au test (iii)) : seul le cas de plages disjointes est testé. `any()` les traite par construction, mais il n'y a pas de test dédié.
2. **Bornes hors grille** (18:18:30Z, par exemple ; liée à (ii)) : le filtre porte sur des valeurs de `window_start`, pas sur une couverture temporelle. L'opérateur doit passer des débuts de fenêtre, ce que fait l'ADR.
3. **Plage qui vide une strate entière** (liée à (i)) : la strate disparaît du bloc 3 au lieu d'afficher n = 0. C'est le comportement déjà existant pour une strate jamais observée. Il ne se produit pas avec la plage d'ADR-0025 (11 398 fenêtres stress restent).
4. **Arguments CLI non entiers ou négatifs** (liée à (iii)) : `type=int` refuse les flottants ; un nombre négatif serait lu comme une option. Non testé.
5. **Plage inversée via la CLI** (liée à (i)) : fail-closed par `ValueError` avec trace (rc=1), comme les autres refus du harnais. Aucun message d'usage dédié.

## 11. Questions ouvertes Q-G1-n
- **Q-G1-1** : où placer ce journal ? Il est livré dans `adr0025-deliver\`. Je propose `F:\Shogen\docs\G1-lot-adr0025-filtre.md`, placé et commité par l'orchestrateur.
- **Q-G1-2** : la fenêtre **2026-09-26T15:08Z** (stress) a 6 flux doublés et 1 marqueur ; la chaîne B a été tuée à 15:08:53Z en pleine fenêtre. Elle est **hors** de la plage d'ADR-0025, qui s'arrête au dernier `window_start` à deux marqueurs, 15:07Z, et elle entre donc dans n avec des lectures last-wins. Garder la définition de l'ADR ou l'amender (B = 15:08Z, soit 2 618 fenêtres) relève du propriétaire d'ADR-0025. Le G1 n'ajuste rien (D-5).
- **Q-G1-3** : le **lot B** (sensibilité R1 par strate réelle × {exclue, incluse}, couverture week-end par week-end calculée depuis les marqueurs, mention « causalité non établie ») est le lot suivant sous ADR-0025. Estimation ≈ 85 lignes. Valeurs à reproduire (C-3) : 29/08 19,0 h ; 05/09 46,7 ; 12/09 43,5 ; 19/09 47,9 ; 26/09 48,0 → 32,9 h. Déclencheur : **avant** le G0 du rapport J28, puisque le point 4 exige la sensibilité dans le rapport final.
- **Q-G1-4** : la strate **poolée** est nommée par ADR-0025 déc. 1 et par RUNBOOK §5 (« trois z »), mais elle est absente du harnais (grep vide). C'est la Q-1 du cp-1, non traitée par ce lot. Il faut une décision avant le G0 du rapport J28.
- **Q-G1-5** : trois points de documentation. Le README du harnais est périmé (« 136 verts » ; 173 sur la base, 178 après le lot). L'option n'est pas documentée dans son « Usage ». RUNBOOK §9 e ne porte pas l'option pour J28 ; c'est un document de plan, donc l'orchestrateur décide sous D-5.
- **Q-G1-6** : la sortie brute de l'étape 0 (`work\baseline_step0.out`) contient le bloc R1 **non filtré**, conséquence de C-7. Elle n'est ni reprise ici ni livrée : seule une version caviardée est livrée. Faut-il la conserver ou la purger (RUNBOOK §8) ?
- **Q-G1-7** : le motif « harnais dégradé, ADR-0025 » est un texte fixe du rapport (C-1). Une exclusion future sous une autre ADR demanderait un changement de code ou une option de motif. C'est acceptable tant qu'ADR-0025 est la seule exclusion autorisée.

## 12. Livrables (`F:\tmp\shogen-j28\adr0025-deliver\`, empreintes dans `DELIVERED.sha256`)
- `s2-harness\shogen_s2\{records,r1,lm,r2,report}.py` et `s2-harness\tests\test_exclusion.py` : copies post-lot, identiques aux fichiers en place.
- `lot-adr0025-filtre.diff` : `git diff` des cinq modules plus le fichier neuf.
- Ce journal.
- Scripts : `capture_golden_base.py` (rejoue le sha du test (iv) sur l'arbre de base), `mesure_declencheur.py` (point 4), `mutants.py` (campagne).
- `sorties\` : `baseline_step0.caviardee.out`, `base-sha256.txt`, `post-lot-sha256.txt`, `golden-render-base.txt`, `mutants.out`, `suite-sans-variable.out`, `suite-avec-variable.out`, `declencheur.out`.
- Non fait, par mandat : le rapport J28 complet n'a pas été lancé ; aucun git écrivant ; rien sur C: ; aucun réseau.
