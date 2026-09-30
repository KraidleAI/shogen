# G1 — lot B-SEG-2 d'ADR-0028 (bloc 1 : segment, dates de campagne, bornes par type, comptes retirés ; refus des epochs négatifs ; SHOGEN-EXCL-COMPTE-1, SHOGEN-NEG-EPOCH-1, HS2-05), Shōgen S2 — journal

- **Modèle** : `claude-opus-5-5` (identifiant exact déclaré par le harnais en tête de session), effort max selon la commande de lancement (le réglage n'est pas observable depuis l'agent) ; worker G1, R-1 déclaré en tête de chacune des deux sessions (première : `oracles/estimation-r25.txt` l.2). Aucun commit, aucun workflow déclenché (R-20). Aucune variable `GIT_DIR` ni `GIT_WORK_TREE` posée, aucun `--write-tree`. Seule écriture git : le HEAD du worktree du lot déplacé en HEAD détaché (§0, E-2). `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée (retirée de chaque exécution) ; tests sur fixtures seulement.
- **Deux sessions, un worker, un worktree** : la première (première mesure vers 03:11Z, dernière écriture 03:38:02Z) s'est arrêtée sur la limite de compte (arrêt consigné par l'orchestrateur au commit `e263bc7`, 03:42:15Z) ; la seconde a repris à 04:56:32Z sur l'état laissé (worktree et `F:/tmp/shogen-lots/B-SEG-2/`), sans le contexte de la première : ses scripts et sorties datés sous `oracles/` sont sa seule trace, relus avant toute suite.
- **Horloge** (`date -u` et heures de fichier) : première session : empilement contrôlé vers 03:11Z (`oracles/verif_empilement.out`) ; suite de base 03:21:20Z ; **estimation R-25 et définitions écrites avant tout code à 03:26:14Z** (`oracles/estimation-r25.txt`, sha256 `97a98116008104868d68d50f5cfd42819269db81b31053dbbfd185cf7e289bf6`, inchangé) ; code 03:32:45Z ; tests 03:38:02Z. Seconde session : reprise 04:56:32Z ; lecture des rapports G2 et de correction de B-SEG-1 et du cp-1 bref ; consultation advisor (canal 1) vers 05:06Z ; C-4 (iv), rebouclage et frontière du cp-1 de 05:07Z à 05:28Z ; suites finales 05:28:06Z-05:29:22Z ; P2P texte rejoué sur le code final, achevé à 05:45:27Z (`oracles/p2p.out`, §4.4) ; mutants 05:29:28Z-05:42:08Z (v2), puis 05:44:54Z-05:56:04Z (v3, qui fait foi) ; `xtask` et enregistrement d'oracle en dernier (§12).
- **Consultations de l'advisor intégré (canal 1, R-26)** : première session, une, avant le code (`estimation-r25.txt` l.7 : « avis advisor canal 1 suivi ») ; seconde session, deux : au plan, vers 05:06Z, et à la clôture, vers 05:59Z, livrables écrits. Avis suivis : frontière de coupe du cp-1 à la lettre, (e) en 2b (E-1) ; aucun code pour SHOGEN-SEG-DEMARRAGE-1, question formée (Q-G1-3) ; épingle de C-4 (iv) ; table C-3 complète, renommage explicite, `test_iii` déclaré non périmé ; P2P ligne à ligne comme justification des re-captures ; déclaration de ces consultations et relecture du vocabulaire avant la chaîne finale.
- **Mandat** : commande de mission de l'orchestrateur Shōgen (`claude-fable-5-1`, 2026-09-30), lot B-SEG-2 de l'annexe A (l.16, amendée à `6f3b9a7` : points (a) à (e) de la revue G2 de B-SEG-1) : SHOGEN-EXCL-COMPTE-1, SHOGEN-NEG-EPOCH-1 (rc 2, Q-G2-5), HS2-05 ; corrections C-1 à C-8 du cp-1 bref (`F:/tmp/cp1-B-SEG-2/CP1-BREF-B-SEG-2.md`, sha256 `bf13cd734971505c46e93960b700c802a15344938db77ad31b1ae53b15b81d05`). Lus en entier avant tout travail : la revue G2 de B-SEG-1 (`F:/tmp/shogen-lots/B-SEG-1/G2-rapport.md`, sha256 `cc8f2b50dd33df44b70af460104ab796c0398e948fab25e8e6ea1c33fe1e9c5c`) et son rapport de correction (`correction-rapport.md`, sha256 `dd90f4dbcfdd4565ca76f2d08f3c3efa2c3cb1bb9edac6c30987b4868d979b75`).
- **Classification** : bounded. Le lecteur existe (`records` → `r1`/`lm`/`r2` → `report`) ; le lot ajoute des lignes au bloc 1, change un message du bloc 5 et refuse les epochs négatifs.
- **Résultat** : coupe R-25 obligatoire (236 lignes), frontière du cp-1 (C-5) : **B-SEG-2a** (bloc 1 et comptes, 176) et **B-SEG-2b** (rc 2, bloc 5, portée des `run_params`, 71). Suites 206 → 212 → 214 tests, OK (2 sauts, variable absente), 0 entrée TMP, 0 `__pycache__`. F2P par famille : FAIL seulement, 0 ERROR. P2P texte sur toute la suite de base : des lignes insérées au bloc 1, plus le message du bloc 5 et le rc 2 de la CLI en 2b ; **aucune ligne existante modifiée**. Mutants : 39 hors témoin, 66 exécutions, 66 tués (§5). `xtask` : §12.

## 0. Préconditions mesurées avant code

- **Base (C-6)** : `b72509b`, commit de B-SEG-1a-N. Le HEAD du worktree est `8643a67`, qui ne diffère de `b72509b` que par `biblio/INDEX.md` (1 ligne, `git diff --stat b72509b 8643a67`). `main` est à `e263bc7` : `git diff --stat b72509b e263bc7 -- s2-harness` est vide, et `b72509b` est ancêtre de `8643a67`, lui-même ancêtre de `e263bc7` (`git merge-base --is-ancestor`). Le diff du lot, pris contre `b72509b`, s'applique donc à l'identique sur les trois.
- **Registre G0 (C-6)** : l'amendement des lignes B-SEG-2 (points (a) à (e)) et RENDU-1 de l'annexe A, et la section B.5 (SHOGEN-SEG-DEMARRAGE-1), sont commis par l'orchestrateur à `6f3b9a7` (2026-09-30T03:09:48Z), avant la première mesure de ce G1. Lus par `git diff 8643a67 e263bc7 -- docs/adr-0028/ANNEXE-A-lots.md docs/adr-0028/ANNEXE-B-items.md`.
- **Empilement demandé par le brief** (`F:/tmp/shogen-lots/B-SEG-1/lot.diff` sur `0abc881`) : **sans objet**, B-SEG-1 est commis (`dc39cb8`, `83f86d8`, `05cff36`, `b72509b`). Contrôle de la première session, sur des archives extraites sous `F:/tmp` : `0abc881` + `lot.diff` (sha256 `e3128c12…abccf630`) = `b72509b` à l'octet sur `s2-harness` et sur le journal G1 de B-SEG-1 ; `b72509b` = `8643a67` sur `s2-harness` (`oracles/verif_empilement.sh`, sortie `verif_empilement.out`). Aucun commit « empilement ».
- **HEAD du worktree (E-2)** : le harnais a créé le worktree sur la branche `worktree-wf_1c82774a-d5f-6` à `fa0ce5b`. La première session l'a placé en HEAD détaché sur `8643a67` (reflog du worktree : « checkout: moving from worktree-wf_1c82774a-d5f-6 to 8643a67 ») ; la référence de branche reste à `fa0ce5b` (`git rev-parse`). C'est le geste de B0 (HEAD privé), recommandé par la revue G2 de B-SEG-1 (Q-G1-9). Aucun `git add` : `tests/test_bloc1.py` et ce journal restent non suivis ; les diffs sont produits hors dépôt (§12).
- **Suite de base** (archive `git archive 8643a67`, TMP neuf) : 206 tests, OK (skipped=2) ; 0 entrée TMP ; 0 `__pycache__` (`oracles/suite-base2.summary`). Les deux sauts : `test_ii_plage_adr0025_retire_2618_fenetres` et `test_ii_plage_adr0025_comptes_par_type`, motif « SHOGEN_S2_CAMPAGNE_CONTROL absente ».

## 1. Coupe R-25 (C-5 du cp-1)

- **Estimation ascendante écrite avant tout code** (03:26:14Z, `oracles/estimation-r25.txt`) : ≈ 179 lignes (≈ 200 avec la marge du précédent B0 E-3), frontière de coupe pré-déclarée.
- **Écart corrigé (E-1)** : cette estimation plaçait (e) en 2a, contre la lettre de C-5 du cp-1 (« 2a : bloc 1 + comptes ; 2b : rc 2 + bloc 5 + (e) »), sans le signaler. La seconde session applique la frontière du cp-1 telle quelle. Conséquence assumée : `SHA_BASE_SANS_OPTION` et `SHA_BASE_AVEC_OPTION` sont re-capturés deux fois, une fois par sous-lot, chaque fois avec son propre P2P texte (§4.4).
- **Mesure** (lignes `+` des diffs de `oracles/mkdiff.py`, repris tel quel du G1 de B-SEG-1, sha256 identique ; fichiers neufs entiers) :

| sous-lot | code `shogen_s2` | tests | ajoutées | retirées | seuil 200 |
|---|---|---|---|---|---|
| **B-SEG-2a** : bloc 1 et comptes ((a), (b), dates de campagne HS2-05, « segment = aucun ») | `report.py` +35 −3 | `test_bloc1.py` 128 (neuf) ; `test_exclusion.py` +6 −5 ; `test_pool_analyse.py` +5 −4 ; `test_g2_adversarial.py` +2 −2 | **176** | 14 | conforme |
| **B-SEG-2b** : rc 2 ((d)), bloc 5 ((c)), portée des `run_params` ((e)) | `records.py` +10 −4 ; `report.py` +10 −1 | `test_bloc1.py` +45 −9 ; `test_exclusion.py` +1 −1 ; `test_pool_analyse.py` +1 −1 ; `test_g2_adversarial.py` +4 −4 | **71** | 20 | conforme |
| lot entier (base → final) | +55 −8 | +181 −15 | 236 | 23 | coupe obligatoire (faite) |

- Aucune fixture déclarative neuve : le module neuf réutilise `build_fixture`, `poser` et `fixture_w120` des lots précédents. Les chaînes attendues des assertions sont des tests, comptées. Les modifications d'épingles supersédées sont comptées dans leur sous-lot (§4.6).
- **Lignes datées proposées pour l'annexe A** (amendement : acte de l'orchestrateur, non écrit ici) :
  - **B-SEG-2a** (2026-09-30, coupe R-25 du G1 de B-SEG-2, frontière de C-5 du cp-1) : SHOGEN-EXCL-COMPTE-1 et HS2-05 ; points (a) et (b) du G0 : lignes ajoutées au bloc 1 (`campagne_fenetres`, `segment = aucun`, `segment_retraits`, `exclusion_ts_harness_ts`, `exclusion_retraits`, `exclusion_retraits_union`). Véhicule : `s2-harness/shogen_s2/report.py`, `tests/test_bloc1.py` (neuf), épingles re-capturées. Oracle : 6 tests neufs, suite 212 tests après ce commit ; P2P texte ; mutants de §5. Taille 176 [mesuré]. Tuyau : bornes et comptes → bloc 1 ; consommateur : lecteur tiers du rapport, puis RENDU-1. cp-1 bref.
  - **B-SEG-2b** (2026-09-30, même coupe) : SHOGEN-NEG-EPOCH-1 étendu au segment (point (d)) ; message du bloc 5 (point (c)) ; ligne `portee_run_params` (point (e)). Véhicule : `records.py`, `report.py`, `tests/test_bloc1.py`, épingles. Oracle : 2 tests neufs, suite 214 tests après ce commit ; mutants de §5. Taille 71 [mesuré]. cp-1 bref.

## 2. Changements (worktree du lot, sur `8643a67` = `b72509b` pour `s2-harness`)

| fichier | B-SEG-2a | B-SEG-2b | sha256 base → 2a → final |
|---|---|---|---|
| `shogen_s2/report.py` | import de `r1.build_window_strate` ; `_comptes`, `_retires` ; assiette `tous` avant filtre ; lignes `campagne_fenetres`, `segment = aucun`, `segment_retraits`, et par plage `exclusion_ts_harness_ts`, `exclusion_retraits`, puis `exclusion_retraits_union` | ligne `portee_run_params` ; message du bloc 5 ; refus CLI des epochs négatifs (`p.error`, rc 2) | 3d95818f → 94a5a4b2 → 93be84cf |
| `shogen_s2/records.py` | — | `exclusion_ranges` : borne < 0 ⇒ `ValueError`, avant `int()` ; `filtre_lecture` : t0 < 0 ⇒ `ValueError` | 50adbc2c → 50adbc2c → 97c1952b |
| `tests/test_bloc1.py` | neuf (6 tests) | 2 tests ; assertions (e) | — → 0c592b1d → 14822b45 |
| `tests/test_exclusion.py` | `SHA_BASE_SANS_OPTION` re-capturé, commentaire et docstring de `test_iv` | sha re-capturé | bd2520e0 → a6bb1c07 → 105b2b9e |
| `tests/test_pool_analyse.py` | `SHA_BASE_AVEC_OPTION` re-capturé, commentaire et docstring de l'épingle | sha re-capturé | 8e2f1af4 → 3623d9ce → fb2e8069 |
| `tests/test_g2_adversarial.py` | `test_plage_hors_campagne_sans_effet_ligne_bloc1_seule` : filtre des lignes `  exclusion_` | `test_cli_non_entier_rc2_et_negatif_accepte` → `test_cli_non_entier_et_negatif_rc2` (rc 2) | 80c28861 → 8ca690b8 → ec362712 |

- Tous les autres fichiers de `s2-harness` sont intouchés (`diff -r` arbre de base contre arbre final : 6 fichiers). `r1`, `lm`, `r2` inchangés : les points d'entrée héritent du refus par `records`. Aucune dépendance neuve.

## 3. Définitions appliquées (C-1 et C-4 du cp-1 : choix du G1, à ratifier, Q-G1-1)

Le cp-1 voulait ces points fixés au G0 ; la commande de mission les a transmis comme corrections « à intégrer », avec leurs options. Le G1 a donc choisi, par écrit avant le code (`estimation-r25.txt`), sur avis de l'advisor (canal 1) ; la seconde session a complété D-5 et D-4.
- **D-1 (C-1)** : option (i). Sans option, le bloc 1 gagne `campagne_fenetres` et `segment = aucun (journal entier)` (2a), puis `portee_run_params` (2b). Aucune ligne existante ne change. Épingles re-capturées dans chaque sous-lot ; justification : P2P texte (§4.4).
- **D-2 ((e), C-5)** : la lettre de C-5 (« étiqueter ces lignes (journal entier) ») aurait modifié trois lignes existantes du bloc 1, contre le critère de C-1 (lignes ajoutées seulement). Le critère de C-1 l'emporte. Une ligne **ajoutée**, `portee_run_params`, déclare que `run_params_demarrages` (tous les démarrages), `started_utc` et `n_windows_demande` (dernier démarrage) portent sur le journal entier et ne sont jamais segmentés ni exclus (§E). Les dates de campagne et la ligne `segment` portent le segment. Imprimée toujours : HS2-05 vise le rendu par défaut.
- **D-3 (C-4 i)** : le compte **par plage** est ce que la plage retire seule de l'assiette de la ligne `segment` (le journal entier sans segment). Il ne dépend pas de l'ordre des plages. La ligne d'union est imprimée dès qu'une plage est donnée ; sous chevauchement, la somme des comptes par plage dépasse l'union (test dédié).
- **D-4 (C-4 iii)** : epoch négatif à l'API ⇒ `ValueError`, symétrique de la plage inversée. Plages : dans `records.exclusion_ranges`, donc pour `render_report`, les `recompute_*` et `filtre_horodatage` ; contrôle fait avant la troncature `int()`, sur les deux bornes (−0,5 et (0 ; −0,5) refusés). Segment : t0 < 0 dans `records.filtre_lecture` ; t_fin < 0 ≤ t0 est déjà un segment inversé (`ValueError`), sans second contrôle, qui serait un mutant équivalent. CLI : contrôle avant l'appel ; `p.error` ⇒ rc 2, message ASCII sur stderr, stdout vide.
- **D-5 (C-4 iv)** : `--segment-n-fixe` ≤ 0 reste hors de ce contrôle : rc 1 (`ValueError` de `t_fin_n_fixe`, MG33) ; épinglé par un test (n = −1 ⇒ rc 1, stdout vide).
- **D-6 (C-4 ii)** : dates de campagne et nombre de fenêtres distinctes sur les marqueurs après la garde §5.3 (qui ne filtre pas), avant segment et exclusion : même assiette que `t_fin_n_fixe`. Sans marqueur, la ligne est imprimée sans première ni dernière fenêtre.
- **D-7 (C-4 v)** : plage vide ⇒ lignes de la plage et de l'union imprimées, tous comptes à 0, rc 0.
- **D-8** : strates listées = strates de tous les marqueurs du journal (avant filtre), triées ; une plage vide imprime donc « calme 0, stress 0 ».
- **D-9** : fenêtres retirées = `window_start` distincts (`r1.build_window_strate`, même dédoublonnage que n) ; `asn_attribution` et `clock_check` = nombre d'enregistrements, comptes bruts comme D5 et le test nommé.
- **D-10 ((c))** : bloc 5. Journal sans `asn_attribution` : message d'origine, vrai. Journal avec des `asn_attribution` dont aucune n'est retenue pour les hôtes du pool : message neuf, avec les deux comptes (au journal ; retenus par le filtre). Le préfixe « axe ASN NON MESURÉ » est gardé : deux tests existants en comptent 2, l'autre occurrence étant `r2.py` l.886.
- **D-11 ((b))** : ligne **ajoutée** par plage, `exclusion_ts_harness_ts` = [a ; b + w) en epoch et ISO, w lu de `run_params`. La ligne `exclusion_window_start` est inchangée : `test_iii_deterministe_et_bloc1_par_la_cli` reste vert, son compte « harnais dégradé, ADR-0025 » = 2 inchangé.
- **D-12 ((a))** : sous segment, ligne **ajoutée** `segment_retraits` : fenêtres par strate, `asn_attribution` et `clock_check` retirés par le segment (journal entier moins segment). La ligne `segment` existante est inchangée.
- **D-13 (C-2 (a))** : les comptes sont calculés dans `report.py` en rappelant `records.filtre_lecture` sur les enregistrements complets, sans seconde implémentation de la règle. `filtre_lecture` et `filtre_horodatage` ne lisent aucune clé de plus et rendent les trois mêmes premiers éléments ; seul ajout, la `ValueError` des epochs négatifs (D-4), sans effet sur des bornes positives.

## 4. Tests (bibliothèque standard, forme de `tests/`) — chaque test nomme la mutation qui le rougit

### 4.1 Fixtures
- `build_fixture` du lot A (w0..w5, reprise w1..w3, démarrages à w0 et w1), plus `poser(d, (A − 1, A, B, B + 59, B + 60))` de B-SEG-1a : un démarrage sans fenêtre et une sonde `r2.collect_asn` par instant, un AS distinct par appel et par hôte. Plage D5 : [A ; B] = [w2 ; w4] (w2 calme, w3 et w4 stress). `fixture_w120` de B-SEG-1c pour w = 120 s. Aucun JSONL écrit à la main ; aucun nom de flux ni d'hôte (`SKELETON`, `r2.build_flux_hosts`).

### 4.2 B-SEG-2a (`tests/test_bloc1.py`, classe `TestBloc1`, 6 tests)
- `test_plage_bornes_par_type_et_retraits_par_strate_et_type` : [w2 ; w4] ; ligne `exclusion_ts_harness_ts` exacte ([A ; B + w), ISO, w de `run_params`) ; `exclusion_retraits` et union : calme 1, stress 2, `asn_attribution` 3 × H, `clock_check` 3 ; **motif `test_a7` (C-2 (b))** : `comptes_outil` et `recompte_independant`, les deux helpers du test nommé, rejoués sur la fixture (projection `CLES`, `filtre_lecture({"w": w}, …)[:3]`) rendent {window_close 3, asn 3 × H, clock 3}, les comptes de la ligne du bloc 1 (3 = 1 + 2) ; CLI = API à l'octet. Rougit si : strate confondue ; type oublié ou interverti ; B sans + w ; ligne d'union absente.
- `test_plages_chevauchantes_chaque_plage_seule_puis_union` : [w2 ; w4] et [w1 ; w3] ; chaque plage seule, en ordre trié, puis l'union (calme 2, stress 2, asn 4 × H, clock 5) ; la somme des plages dépasse l'union. Rougit si : union = somme ; plage comptée après une autre.
- `test_plage_vide_comptes_a_zero_visibles_rc0` : plage avant la campagne, par la CLI ; rc 0 ; lignes de la plage et de l'union à 0. Rougit si : ligne omise quand tout est à 0 ; plage vide refusée.
- `test_dates_de_campagne_avant_filtre_et_retraits_du_segment` : segment [w1 ; w4) et plage [w3 ; w5] ; `campagne_fenetres` identique avec et sans option (6 fenêtres distinctes malgré les doublons, première w0, dernière w5, epoch et ISO) ; `segment = aucun` sans option ; `segment_retraits` (calme 1, stress 2, asn 3 × H, clock 4) ; la plage comptée sur l'assiette du segment (stress 1, 0, 0) ; sous segment, une seule ligne `segment`. Rougit si : dates après filtre ; doublons comptés ; première et dernière inversées ; plage comptée sur le journal entier ; lignes absentes ; « aucun » imprimé aussi sous segment (MB27).
- `test_bornes_ts_harness_ts_w_lu_de_run_params` : w = 120 s ; [A ; B + 120) et ses retraits. Rougit si : + 60 codé en dur.
- `test_journal_sans_fenetre_dates_de_campagne_sans_lever` : un démarrage sans fenêtre (0 marqueur) : la ligne sort, sans première ni dernière. Rougit si : la première fenêtre est lue sur une liste vide.

### 4.3 B-SEG-2b (même module, 2 tests et 4 assertions ajoutées)
- `test_epoch_negatif_rc2_cli_et_valueerror_api` : CLI rc 2, stdout vide, `SHOGEN-NEG-EPOCH-1` sur stderr pour `--segment-from` −5, `--segment-to` −1, et une plage négative par chacune de ses bornes ; `--segment-n-fixe -1` ⇒ rc 1 (D-5) ; `ValueError` aux quatre points d'entrée pour une plage négative, un segment à t0 négatif (t_fin ou n fixe) et un segment à t_fin négatif ; `records.exclusion_ranges` refuse (−0,5 ; 10) et (0 ; −0,5). Rougit si : rc 1 au lieu de 2 ; segment ou plage négatifs acceptés (CLI ou API) ; −0,5 tronqué en 0 ; n fixe refusé comme un epoch.
- `test_bloc5_sondes_toutes_retirees_message_vrai` : [w0 ; w5 − 1] retire toutes les sondes ; le bloc 5 donne les deux comptes (5 × H au journal, 0 retenues) et plus « collect_asn non lancé » ; sur un journal sans sonde, le message d'origine reste. Rougit si : ancien message gardé après un filtre total ; message neuf sur un journal sans sonde.
- Dans `test_dates_de_campagne_…`, point (e) : `portee_run_params` exacte avec et sans option, et `started_utc` = B + w, dernier démarrage, hors du segment [w1 ; w4) : la situation mesurée par la revue G2 de B-SEG-1.

### 4.4 P2P texte (C-1 : justification ligne par ligne des re-captures)
- **Instrument** : `oracles/p2p_texte.py`, variante de `p2p_rendus.py` (G1 B0, repris au G1 de B-SEG-1) qui garde le texte de chaque sortie de `render_report` et de chaque stdout de la CLI, avec son rc ; `oracles/p2p_lignes.py` classe chaque différence (`difflib`, sans auto-junk) : (i) insertion au bloc 1 d'une ligne à clé autorisée (la clé `segment` seulement avec la valeur « aucun ») ; (ii) au bloc 5, remplacement de l'ancien message par le neuf ; (iii) CLI rc 0 → rc 2, stdout vide. Toute autre différence est un défaut. Prédictions écrites dans l'en-tête de `oracles/p2p.sh` avant la mesure. Tests de **base** (206) sur le code de base, deux fois, puis sur le code 2a et sur le code final (`oracles/p2p.out`).
- **Résultats** :
  - base contre base : 76 sorties, 76 identiques après le masquage de l'heure murale de `collect_asn` (E-7 du G1 B0) ;
  - base contre code 2a : 74 sorties comparées, 8 identiques ; insertions au bloc 1 : `campagne_fenetres` 66, `segment = aucun` 58, `segment_retraits` 8, `exclusion_ts_harness_ts` 43, `exclusion_retraits` 43, `exclusion_retraits_union` 34 ; **aucune autre différence** ;
  - code 2a contre code final : `portee_run_params` 65 ; message neuf du bloc 5 : 4 ; CLI [−5 ; 10] rc 0 → 2 : 1 ; **aucune autre différence** ;
  - base contre code final : la somme des deux lignes précédentes, rien d'autre ;
  - 2 sorties de la base n'ont pas d'homologue côté lot : les appels CLI de `test_iv_…` et `test_epingle_…`, que ces épingles, rouges sur le code du lot, n'atteignent pas (échec au sha, avant l'appel). Sur l'arbre du lot, les mêmes tests re-capturés assertent CLI = API : verts.
- **Rendus épinglés, lignes ajoutées mot pour mot** (fixture d'exclusion ; la base en a 171 sans option, 163 avec [w2 ; w4]) :
  - sans option, B-SEG-2a (171 → 173 lignes, sha `510dd28e89bbe0b3dc7c5414229d5d50c219200e82835729e4014aa4d3597e4f`), avant la l.27 de la base :
    - `  campagne_fenetres        = 6 fenêtres distinctes au journal (window_close, avant segment et exclusion) : première 1786147020 = 2026-08-07T23:57:00+00:00 ; dernière 1786147320 = 2026-08-08T00:02:00+00:00 (window_start) — HS2-05`
    - `  segment                  = aucun (journal entier) — ADR-0028 D4`
  - avec [w2 ; w4], B-SEG-2a (163 → 168, sha `c627719ed3083f3bdec71a166a51d63cf17143501aea18bc1eb539258db8539c`) : les deux mêmes lignes avant la l.27, puis, après `exclusion_window_start` (inchangée) :
    - `  exclusion_ts_harness_ts  = [1786147140 ; 1786147320) = [2026-08-07T23:59:00+00:00 ; 2026-08-08T00:02:00+00:00) semi-ouvert : asn_attribution (ts), clock_check (harness_ts), w = 60 s de run_params — ADR-0028 D5`
    - `  exclusion_retraits       = [1786147140 ; 1786147260] seule (assiette : ligne segment) : fenêtres distinctes (window_close) calme 1, stress 2 ; asn_attribution 0 ; clock_check 0`
    - `  exclusion_retraits_union = 1 plage(s), union (assiette : ligne segment) : fenêtres distinctes (window_close) calme 1, stress 2 ; asn_attribution 0 ; clock_check 0 — SHOGEN-EXCL-COMPTE-1`
  - B-SEG-2b, dans les deux rendus (174 lignes sans option, sha `b054a0f4fe74fc1b7c65afdc480b9fbca56172dc1a3ba5b9ef18d2f8669ac01e` ; 169 avec, sha `677b1bfcba168e015b0af282c45c4457a34f8f893a0a6bc1eabd81a30a422114`), après `campagne_fenetres` :
    - `  portee_run_params        = journal entier, jamais segmenté ni exclu (§E) : run_params_demarrages = tous les démarrages ; started_utc, n_windows_demande = dernier démarrage (HS2-05)`
  - Recapture des sha par `oracles/epingle.py` (repris du G2 B0, reviseur distinct) : base `a4ffc3e5…f649a5` et `a4dd4c00…537520`, égaux aux constantes d'avant le lot (première session, `epingle-base.out`) ; 2a et final ci-dessus (`mk2a.out`, `epingle-final-wt.out`).

### 4.5 F2P par famille (catégories fixées avant code : FAIL, jamais ERROR)

| famille | tests | arbre parent | résultat |
|---|---|---|---|
| F-1 bloc 1 (2a) | les 6 tests de §4.2 | base | **FAIL ×6** (AssertionError), 0 ERROR |
| F-2 épingles re-capturées en 2a | `test_iv_…`, `test_epingle_…` | base | FAIL ×2 (sha), comptées à part (§4.6) |
| F-3 2b | `test_epoch_…`, `test_bloc5_…`, `test_dates_de_campagne_…` (assertions (e)) | 2a | **FAIL ×3**, 0 ERROR |
| F-4 épingles de 2b | `test_iv_…`, `test_epingle_…`, `test_cli_non_entier_et_negatif_rc2` | 2a | FAIL ×3, comptées à part (§4.6) |

- Sorties : `oracles/suite-f2p-2a.out` (212 tests, 8 FAIL, 0 ERROR) et `oracles/suite-f2p-2b.out` (214 tests, 6 FAIL, 0 ERROR). La modification de `test_plage_hors_campagne_…` (2a) élargit un filtre : elle passe sur la base comme sur le lot, ce n'est pas un F2P.
- **Trace remplacée** : un premier rejeu F2P de la première session (`oracles/suite-f2p.out`, 03:37:28Z) montrait 1 ERROR (`IndexError`). Il portait sur une version antérieure de `tests/test_bloc1.py` (copie `copies/f2p` différente du worktree dès la l.105) : l'assertion `ligne(…)[0]` y a été remplacée par une égalité de listes. Il ne compte pas.

### 4.6 Épingles supersédées (C-3 du cp-1 ; ni F2P ni épingle CA-13 bis : à compter à part au G2 et au cp-2)

| test (nom de base → nom au lot) | sous-lot | décision qui le périme | modification | lignes + / − |
|---|---|---|---|---|
| `test_exclusion.py::TestExclusionFixture::test_iv_sans_option_octets_d_avant_le_lot` (nom inchangé) | 2a, 2b | D-1 (C-1 option (i)) ; D-2 ((e)) | `SHA_BASE_SANS_OPTION` re-capturé à chaque sous-lot ; commentaire et docstring | 2a +6 −5 ; 2b +1 −1 |
| `test_pool_analyse.py::TestPoolAnalyse::test_epingle_sans_flux_mort_octets_de_base_avec_option` (nom inchangé) | 2a, 2b | D-1, D-11 ((b)), D-3 ; D-2 | `SHA_BASE_AVEC_OPTION` re-capturé ; commentaire et docstring | 2a +5 −4 ; 2b +1 −1 |
| `test_g2_adversarial.py::TestG2Adversarial::test_plage_hors_campagne_sans_effet_ligne_bloc1_seule` (nom inchangé ; non nommé par le cp-1, trouvé par le P2P de la première session) | 2a | D-7, D-11 : les plages hors campagne impriment désormais des lignes `exclusion_*` (comptes à 0, bornes par type) | filtre `"exclusion_window_start" not in ln` → `not ln.startswith("  exclusion_")` ; le compte `exclusion_window_start` = 2 reste asserté ; docstring | +2 −2 |
| `test_g2_adversarial.py::TestG2Adversarial::test_cli_non_entier_rc2_et_negatif_accepte` → **`test_cli_non_entier_et_negatif_rc2`** (renommé : l'ancien nom affirmait l'acceptation) | 2b | D-4 (SHOGEN-NEG-EPOCH-1, Q-G2-5) | rc 0 et ligne `[-5 ; 10]` → rc 2, stdout vide, `SHOGEN-NEG-EPOCH-1` sur stderr | +4 −4 |
| `test_exclusion.py::TestExclusionFixture::test_iii_deterministe_et_bloc1_par_la_cli` | — | **non périmé** : forme « = [a ; b] = [iso ; iso] fermée » et compte « harnais dégradé, ADR-0025 » = 2 inchangés (D-11) | aucune | 0 |

- Rejeu des tests de base sur le code du lot (`oracles/suite-p2p-2a.out`, `suite-p2p-fin.out`) : rouges exactement les épingles ci-dessus, 3 sur le code 2a, 4 sur le code final ; aucun autre test de base ne rougit.

## 5. Mutants (copies sous `F:/tmp/shogen-lots/B-SEG-2/mut/`, suite complète, TMP neuf, variable jamais posée) — `oracles/mutants_bseg2.py`, `oracles/mutants_def_bseg2.py`

- **Colonnes** : A = arbre du sous-lot 2a seul (212 tests) ; F = arbre final, 2a + 2b (214 tests). Une copie neuve par mutant et par colonne, suite complète, TMP neuf, variable retirée, copie jetée. Critère de mort : code de retour ≠ 0. Définitions : chaîne exacte, une occurrence exigée (`oracles/verif_mutants_def.py` : 0 problème sur 40). Les mutants de 2a tournent en A (les tests de 2a seuls doivent les tuer) et en F ; ceux de 2b en F.
- **Campagne v2** (05:29:28Z-05:42:08Z, `oracles/mutants-bseg2-v2-0529Z.*`) : 64 exécutions tuées sur 66, un survivant, MB27 (« segment = aucun » imprimé aussi sous segment), en A et en F. Trou d'oracle : aucun test ne comptait les lignes `segment` sous segment. Correction à 05:43Z (`oracles/fix_mb27.py`) : une assertion dans `test_dates_de_campagne_…`, une seule ligne `segment` sous segment (2a : +2 lignes).
- **Campagne v3, qui fait foi** (05:44:54Z-05:56:04Z, `oracles/mutants-bseg2.{json,out,start,end}`, sur les arbres finaux) : table ci-dessous, tirée du JSON par `oracles/table_mutants.py` (`oracles/table-mutants.md`).
- **Classes exigées** : strate confondue MB01 ; type oublié MB04, MB05 (interverti MB03) ; rc 1 au lieu de 2 MB34 ; C-8 du cp-1 : chevauchement compté deux fois ou union fausse MB23, MB24 ; dates après filtre MB06 ; segment négatif accepté à la CLI MB35 ; compte 0 omis sur plage vide MB21, MB25.
- **Mutant équivalent évité** : le contrôle `t_fin < 0` du segment (t_fin < 0 ≤ t0 est déjà un segment inversé) a été retiré du code avant les campagnes v2 et v3 (D-4). Aucun mutant équivalent déclaré.

| # | mutant | A (2a, 212 tests) | F (final, 214 tests) | rougi par (colonne F, sinon A) |
|---|---|---|---|---|
| MB00 | temoin (aucune mutation) | vert (témoin) | vert (témoin) | — |
| MB01 | strate confondue (toute fenetre comptee dans chaque strate) | tué (5) | tué (5) | bornes et retraits, chevauchantes, dates et segment, w = 120, épingle avec option |
| MB02 | fenetres non dedupliquees (marqueurs comptes) | tué (4) | tué (4) | bornes et retraits, chevauchantes, dates et segment, épingle avec option |
| MB03 | asn et horloge intervertis | tué (4) | tué (4) | bornes et retraits, chevauchantes, dates et segment, w = 120 |
| MB04 | type oublie : asn_attribution | tué (4) | tué (4) | bornes et retraits, chevauchantes, dates et segment, w = 120 |
| MB05 | type oublie : clock_check | tué (4) | tué (4) | bornes et retraits, chevauchantes, dates et segment, w = 120 |
| MB06 | dates de campagne apres filtre | tué (2) | tué (2) | dates et segment, épingle avec option |
| MB07 | doublons comptes (marqueurs, non fenetres distinctes) | tué (3) | tué (3) | dates et segment, épingle avec option, épingle iv |
| MB08 | premiere et derniere inversees | tué (3) | tué (3) | dates et segment, épingle avec option, épingle iv |
| MB09 | ligne campagne_fenetres absente | tué (4) | tué (4) | dates et segment, sans fenêtre, épingle avec option, épingle iv |
| MB10 | strates listees apres filtre | tué (1) | tué (1) | dates et segment |
| MB11 | ligne segment = aucun absente | tué (3) | tué (3) | dates et segment, épingle avec option, épingle iv |
| MB12 | ligne segment_retraits absente | tué (1) | tué (1) | dates et segment |
| MB13 | segment_retraits compte aussi l'exclusion | tué (1) | tué (1) | dates et segment |
| MB14 | borne ts/harness_ts : B + 60 code en dur | tué (1) | tué (1) | w = 120 |
| MB15 | borne ts/harness_ts : B sans + w | tué (3) | tué (3) | bornes et retraits, w = 120, épingle avec option |
| MB16 | borne ts/harness_ts : ISO de fin sans + w | tué (3) | tué (3) | bornes et retraits, w = 120, épingle avec option |
| MB17 | ligne exclusion_ts_harness_ts absente | tué (3) | tué (3) | bornes et retraits, w = 120, épingle avec option |
| MB18 | ligne exclusion_retraits absente | tué (6) | tué (6) | bornes et retraits, chevauchantes, dates et segment, plage vide, w = 120, épingle avec option |
| MB19 | plage comptee sur le journal entier (assiette hors segment) | tué (1) | tué (1) | dates et segment |
| MB20 | plage comptee cumulativement (apres les plages precedentes) | tué (1) | tué (1) | chevauchantes |
| MB21 | compte 0 omis : ligne de plage absente si rien n'est retire | tué (1) | tué (1) | plage vide |
| MB22 | ligne d'union absente | tué (4) | tué (4) | bornes et retraits, chevauchantes, plage vide, épingle avec option |
| MB23 | union = somme des plages (chevauchement compte deux fois) | tué (1) | tué (1) | chevauchantes |
| MB24 | union = premiere plage seule (total d'union faux) | tué (1) | tué (1) | chevauchantes |
| MB25 | compte 0 omis : ligne d'union absente si rien n'est retire | tué (1) | tué (1) | plage vide |
| MB26 | w = 60 code en dur dans le texte de la borne | tué (1) | tué (1) | w = 120 |
| MB27 | segment = aucun imprime aussi sous segment | tué (1) | tué (1) | dates et segment |
| MB30 | ligne portee_run_params absente | — | tué (3) | dates et segment, épingle avec option, épingle iv |
| MB31 | bloc 5 : ancien message garde apres filtre total | — | tué (1) | bloc 5 |
| MB32 | bloc 5 : message neuf sur un journal sans sonde | — | tué (3) | bloc 5, épingle avec option, épingle iv |
| MB33 | bloc 5 : comptes du message intervertis | — | tué (1) | bloc 5 |
| MB34 | rc 1 au lieu de 2 (controle CLI retire) | — | tué (2) | CLI négatif (G2 lot A), epoch négatif |
| MB35 | segment negatif accepte a la CLI | — | tué (1) | epoch négatif |
| MB36 | exclusion negative acceptee a la CLI | — | tué (2) | CLI négatif (G2 lot A), epoch négatif |
| MB37 | n fixe traite en epoch (rc 2) | — | tué (1) | epoch négatif |
| MB38 | exclusion negative acceptee a l'API | — | tué (1) | epoch négatif |
| MB39 | -0,5 tronque en 0 (int au lieu de float) | — | tué (1) | epoch négatif |
| MB40 | borne haute de plage non controlee | — | tué (1) | epoch négatif |
| MB41 | segment negatif accepte a l'API | — | tué (1) | epoch négatif |

Bilan : 39 mutants hors témoin, 66 exécutions ; tués 66, survivants 0 ; témoin MB00 vert en A et en F ; TMP laissé 0, __pycache__ 0.

Après chaque mutant, la copie est jetée (`restant sous mut/ : 0`) ; le worktree n'a jamais porté de mutant.

## 6. Test nommé (C-2 du cp-1)

- **Contrat invariant (C-2 (a))** : le lot ne touche ni `CLES`, ni `_proj`, ni `comptes_outil`, ni `recompte_independant`, ni le test nommé (`tests/test_exclusion.py` l.261-281 à l'arbre final ; seules les l.28-30 et l.145-147 de ce fichier changent). `records.filtre_lecture({"w": w}, m, c, s, ranges=[(a, b)])[:3]` sur des enregistrements projetés sur `CLES` rend les mêmes trois listes : la seule ligne neuve de `filtre_lecture` est le contrôle `t0 < 0`, sous `segment is not None`, et celle d'`exclusion_ranges` ne lève que sur une borne négative.
- **Rejeu sur fixture (C-2 (b))** : `test_plage_bornes_par_type_et_retraits_par_strate_et_type` appelle les deux helpers du test nommé sur la fixture à bornes et compare leurs comptes à ceux de la ligne du bloc 1 (§4.2). Passe sur 2a et sur le final.
- **Rejeu sur la copie scellée (C-2 (c))** : acte de l'orchestrateur seul, au G7 de ce lot, variable posée, arbre gelé : `cd s2-harness && SHOGEN_S2_CAMPAGNE_CONTROL=<copie de control.jsonl> python -B -m unittest -v tests.test_exclusion.TestExclusionJournalReel`. Attendu : les deux tests verts, comme à `b72509b`. Ce worker ne l'a pas exécuté.

## 7. Tuyaux CA-11 (règle Branchement)
- **Entrée** : `control.jsonl` (quatre types) et `journal.jsonl` du collecteur ; ici, fixtures du collecteur réel et de `r2.collect_asn`.
- **Composition** : `parse_control`, `parse_asn` → `effective_run_params` → `verify_markers_against_spec` → `records.filtre_lecture` (segment, exclusion D5 ; refus des epochs négatifs : ce lot) → `analysis_pools` → R1, L&M, R2 → `render_report`, dont le bloc 1 déclare à présent les dates de campagne, le segment (ou son absence), les bornes par type et les comptes retirés.
- **Chemin servi** : CLI `python -m shogen_s2.report` (RUNBOOK §9 e), rejouée en processus neuf par 3 tests neufs et par les tests d'épingle ; CLI = API à l'octet.
- **Sortie aval** : lecteur tiers du rapport ; RENDU-1 et RENDU-2 absents (item SHOGEN-RENDU-UNIQUE-1, annexe B l.57). La précondition « B-SEG-2 avant RENDU-1 » (ligne RENDU-1 amendée à `6f3b9a7`) est levée au commit de B-SEG-2b.
- **État** : aucun état persistant ; bornes et comptes dans la sortie. S2 reste « upcoming » (ADR-0028 §3) : aucune revendication neuve.

## 8. Risques MAST nommés (C-7 du cp-1) et contre-mesures
- **FM-1.5 (bornes ; plages chevauchantes ; assiette des dates)** : une seule assiette par ligne, écrite (D-3, D-6, D-12) ; plage vide, plages chevauchantes, segment et plage croisés, journal sans fenêtre, w = 120 s ; mutants de borne (MB14-MB16), d'assiette (MB06, MB10, MB13, MB19, MB20) et d'union (MB23-MB25).
- **FM-3.3 (épingle re-capturée sans justification ; rouge tautologique)** : chaque re-capture a son P2P texte (§4.4), qui montre les lignes ajoutées mot pour mot et aucune ligne changée ; les tests neufs assertent des lignes entières, construites à partir de la fixture (`WS`, `W`, `H`), jamais recopiées d'un rendu ; F2P : FAIL sur le parent, jamais ERROR (§4.5).
- **FM-2.3 (dérive vers le lot B)** : ni sensibilité, ni blocs 3 et 6, ni z poolé ; `r1`, `lm`, `r2` intouchés ; seul le message du bloc 5 visé par (c) change hors du bloc 1. Non faits, portés en questions (§11) : comptes retenus par hôte (SHOGEN-SEG-DEMARRAGE-1), ventilation des `resolve_failed`.
- **FM-1.1 (pièces D.2 ; variable)** : aucune pièce D.2 ouverte ; variable jamais posée (retirée de chaque exécution) ; test nommé non exécuté ; `xtask` lit `docs/` mécaniquement, seules ses lignes de verdict sont affichées (§12).
- **FM-3.2 (vérification incomplète)** : mutants trouvés en écrivant la liste et tués par des cas ajoutés : borne haute de plage à −0,5 (MB40), n fixe négatif (MB37), t_fin négatif à l'API ; survivant de la campagne v2, MB27, tué en v3 par une assertion ajoutée (§5).

## 9. `error_origin` proposés (à assigner au G7)
- **E-1** : frontière de coupe de l'estimation (e en 2a) contraire à la lettre de C-5 du cp-1, non signalée. Origine : worker (première session). Corrigé : frontière du cp-1 appliquée (§1).
- **E-2** : le harnais a créé le worktree à `fa0ce5b`, non à la base nommée ; la première session a détaché le HEAD sur `8643a67`. Origine : harnais du workflow (même cause que B0 E-1 et B-SEG-1 E-1) ; geste du worker déclaré.
- **E-3** : lignes ajoutées au-delà de 110 caractères (9, toutes dans `tests/test_bloc1.py`) jusqu'au rebouclage de 05:27:39Z (`oracles/rewrap.py`), sans retrait ni changement d'assertion. Origine : worker.
- **E-4** : premier rejeu F2P sur une copie antérieure à la version finale des tests (§4.5) ; première campagne de mutants interrompue par le worker (dernière écriture 05:26:21Z, arrêt par `taskkill` de son seul arbre de processus), avant le rebouclage, sur des arbres qu'il allait régénérer : sortie conservée (`oracles/mutants-bseg2-v1-interrompu.out`), sans valeur de preuve. Origine : worker.
- **E-5** : arrêt de la première session sur la limite de compte, sans journal écrit. Origine : environnement ; reprise sur les traces datées, sans perte de livrable.
- **E-6** : MB27 survivant de la campagne v2 (trou d'oracle : lignes `segment` non comptées sous segment) ; assertion ajoutée, campagne v3 complète : 0 survivant. Origine : worker (liste de tests).

## 10. Review Focus
1. **(e) par ligne ajoutée** plutôt que par étiquette des lignes existantes (D-2) : le choix tient au critère de C-1 ; à confirmer.
2. **Comptes par plage sur l'assiette du segment** (D-3) : sous segment, la ligne d'une plage ne compte que ce qui était dans le segment ; le texte le dit (« assiette : ligne segment »).
3. **Journal sans marqueur et plage** : la ligne de comptes n'a alors aucune strate à lister (« fenêtres distinctes (window_close)  ; … ») ; cas dégénéré, non testé.
4. **Message du bloc 5** : il distingue « aucune sonde au journal » de « aucune retenue pour le pool » ; l'autre occurrence du préfixe, dans la note de k_eff (`r2.py` l.886), dit « aucun enregistrement asn_attribution » sans préciser « au journal » : hors du lot (c).
5. **Refus CLI avant l'API** : un epoch négatif ne produit jamais de trace Python (rc 2 d'`argparse`) ; `--segment-n-fixe` négatif garde sa trace (rc 1, D-5).

## 11. Questions ouvertes Q-G1-n (pour l'orchestrateur)
- **Q-G1-1** : ratifier D-1 à D-13 (§3), dont D-2 (lettre de C-5 contre critère de C-1) et D-3 (assiette et union).
- **Q-G1-2** : la coupe 2a / 2b et les lignes datées du §1 ; E-1.
- **Q-G1-3 (SHOGEN-SEG-DEMARRAGE-1, annexe B.5)** : l'item attend du bloc 1 la mesure, par segment, des `asn_attribution` (par hôte) et des `clock_check` retenus. Le bloc 1 donne les comptes **retirés** par type (point (a)) ; les comptes retenus par hôte ne sont pas imprimés ; le cas décisif, « aucune sonde retenue ⇒ k_eff non évaluable », est imprimé au bloc 5 avec ses deux comptes (D-10). Faut-il une ligne de comptes retenus (par type, voire par hôte) ? Estimation ≈ 5 à 15 lignes ; à décider au G0 de PAQUET ou de RENDU-1 (déclencheur de l'item).
- **Q-G1-4** : D5 écrit « 5 313 dont 815 `resolve_failed` » ; le bloc 1 ne ventile pas les `asn_attribution` retirées par statut. Ventilation voulue au rendu ? (≈ 3 lignes ; hors du brief, non faite.)
- **Q-G1-5** : le renommage `test_cli_non_entier_rc2_et_negatif_accepte` → `test_cli_non_entier_et_negatif_rc2` (§4.6).
- **Q-G1-6** : l'état transitoire « B-SEG-2 avant RENDU-1 » peut être déclaré levé au commit de B-SEG-2b (§7).

## 12. Livrables (`F:/tmp/shogen-lots/B-SEG-2/`)

- `lot.diff` : le lot seul contre `b72509b` (7 fichiers, dont 2 neufs : `tests/test_bloc1.py` et ce journal), produit sans écrire l'index par `oracles/mklot.sh` : `git --no-optional-locks diff b72509b -- s2-harness`, puis `git diff --no-index /dev/null` pour les deux fichiers neufs. Recomposition (`oracles/mklot.out`) : archive de `8643a67` + `patch -p1` = worktree (`diff -r` sur `s2-harness`, `cmp` sur ce journal) ; `patch --dry-run` rc 0 sur les archives de `b72509b` et de `e263bc7`. 0 octet CR.
- `bseg-2a.diff`, `bseg-2b.diff` : sous-lots, par `oracles/mkdiff.py` (fichiers `.py` seulement ; ce journal va dans l'un des commits, hors compte, convention de B-SEG-1). Composition (`oracles/check_souslots.sh`, sortie `check-souslots.out`) : base + 2a = `arbres/2a` ; + 2b = `arbres/final` = worktree ; 2a puis 2b = `lot.diff` sur `s2-harness`.
- `G1-rapport.md` : copie de ce journal.
- `arbres/` (`base`, `2a`, `final`), `copies2/` (F2P et tests de base sur code du lot), `souslots/`, `recompo/` : copies de travail de la seconde session ; `verif/` et `copies/` : première session (`copies/` périmée, §4.5).
- `oracles/` :
  - scripts de la première session : `verif_empilement.sh`, `run_suite.sh`, `epingle.py` (repris du G2 B0), `essai_rendu.py`, `longueurs.py` (repris du G1 de B-SEG-1), `copies.sh` (remplacé par `copies2.sh`) ;
  - scripts de la seconde : `arbres.sh`, `mk2a.py` (arbre 2a tiré du final et de la base, sans retaper un bloc de base), `copies2.sh`, `suites.sh`, `regen.sh`, `mkdiff.py` (repris du G1 de B-SEG-1), `p2p_texte.py`, `p2p_lignes.py`, `p2p.sh`, `mutants_def_bseg2.py`, `mutants_bseg2.py` (lanceur adapté du G2 de B-SEG-1), `verif_mutants_def.py`, `resume_mutants.py`, `table_mutants.py`, `grep_c_b0_10_iv.py` (repris de la correction de B-SEG-1, chemin de base et trois motifs HS2-05 ajoutés), `longues.py`, `rewrap.py`, `fix_mb27.py`, `maj_journal_*.py`, `xtask.sh` (repris de la correction de B-SEG-1, chemins seuls changés), `mklot.sh`, `check_souslots.sh`, `oracle_record_bseg2.py` ;
  - sorties : `suite-*.out` et `.summary`, `suites.out` (et ses versions antérieures `suites-v*.out`), `p2p-*.json`, `p2p.out` (et `p2p-v*.out`), `mutants-bseg2.{json,out,start,end}` (et les traces `mutants-bseg2-v1-interrompu.*`, `mutants-bseg2-v2-0529Z.*`), `epingle-*.out`, `mk2a.out`, `regen.out`, `copies2.out`, `grep-c-b0-10-iv.out`, `longueurs.out`, `xtask-final*.{out,summary}`, `rustup-downloads-*.txt`, `d2-check-xtask-final.out`, `mklot.out`, `check-souslots.out`, `estimation-r25.txt` ;
  - `LIVRABLES.sha256` : empreintes des livrables et chemin de l'enregistrement d'oracle `shogen.oracle-record.v1` (rôle G1, aucun run avec la variable), sous `F:/tmp/oracle-results/`.
  - Première émission de cet enregistrement, remplacée et conservée : `F:/tmp/oracle-results/shogen-b72509b-G1-B-SEG-2-2026-09-30-56392.json` (écrite à 05:58:19Z, avant la dernière retouche de ce journal) ; seule `…-128232.json` (06:01:17Z) fait foi (revue G2 de B-SEG-2, C-5).
- **C-B0-10 (iv)** : dans les lignes ajoutées des deux sous-diffs (176 et 71), aucune occurrence des 12 `flux_id`, des 11 hôtes de `sources.SPECS` ni des 40 bornes, comptes et dates d'ADR-0024, ADR-0025, ADR-0028 et de HS2-05 ; le lot ne touche pas le test nommé (`oracles/grep-c-b0-10-iv.out`).
- **Longueur de ligne** : aucune ligne ajoutée au-delà de 110 caractères, la plus longue en fait 110 (`oracles/longueurs.out`).
- **`cargo --locked xtask verify`** (copie `arbres/final`, ce journal compris ; garde `oracles/xtask.sh` : `RUSTUP_TOOLCHAIN=1.97.1-x86_64-pc-windows-msvc`, `RUSTUP_AUTO_INSTALL=0`, serveurs rustup vers 127.0.0.1:9, `CARGO_NET_OFFLINE=true`, `CARGO_HOME` du brief, cible sous `F:/tmp/shogen-lots/B-SEG-2/target`) : VERT : S-G1 à S-G6, S-G7a et S-G8 (8 lignes « VERDICT : VERT (0 violation(s)) »), `cargo fmt --check`, `no_std` et `cargo clippy -D warnings` VERT, « VERDICT GLOBAL : VERT », 0 ligne ROUGE ; `F:/rust/rustup/downloads/` : 0 entrée avant, 0 après. Rejoué sur la copie finale qui contient ce journal dans sa forme livrée ; heures, code de sortie et sha256 de la sortie dans `oracles/xtask-final.summary` (hors journal : ce fichier est lu par `xtask`). Seules les lignes de verdict ont été affichées. Garde D.2 n° 5 et 6 : `F:/tmp/shogen-lots/B0/corr/oracles/d2_check.py` (correction de B0, réutilisé tel quel, sha256 `983c6c32dd8c5aca936d07b238c752c19b690e912f5fd32d6e5432c258dd26b5`), qui repère les deux lignes par leur sha256 sans les afficher et compte leur texte dans la sortie de `xtask` : résultat dans `oracles/d2-check-xtask-final.out`.

## 13. Attestation (forme d'ADR-0028 D.3)
- **Pièces lues** :
  - la revue G2 de B-SEG-1 et son rapport de correction, en entier ; le cp-1 bref de B-SEG-2, en entier ; ADR-0028 l.45-62 (D4, D5) ; annexe A et B : le diff `8643a67..e263bc7` ; annexe D l.25-60 (D.1 n° 13, D.2, D.3 a et b) ; `harnais-s2.md` l.212 (HS2-05), pièce autorisée (D.2, dernier alinéa) ;
  - `docs/G1-lot-B-SEG-1-segment.md` en entier ; la liste des sections de `docs/G1-lot-B0-pool-analyse.md` et `docs/G1-lot-adr0025-filtre.md` ;
  - code : `records.py` l.280-375 ; `report.py` l.56-185, l.288-310 et l.420-475 ; `r1.py` l.287-310 ; `r2.py` l.770-800, l.880-915 ; `xtask/src/sg4.rs` (liste) et `sg5.rs` (en-tête et seuils) ;
  - tests : `tests/test_exclusion.py` l.1-245 (dont la docstring du test (ii), qui porte des comptes de fenêtres d'ADR-0025) ; `tests/test_segment.py` l.14-40 et noms ; `tests/__init__.py` ; `tests/test_bloc1.py` en entier ;
  - scripts : ceux de la première session (`oracles/`), `mkdiff.py` du G1 de B-SEG-1, `mutants_g2.py` et l'en-tête de `mutants_def.py` du G2 de B-SEG-1, `grep_c_b0_10_iv.py` et `xtask.sh` de la correction de B-SEG-1.
- **Exposé à** : les comptes et bornes que portent ces pièces (D5 : 5 313 dont 815, 483, bornes de la plage ; D4 : 17 314 et 9 261 ; 2 618 et 35 982 ; ADR-0025 : 38 600 → 35 982 = 1 709 + 909 ; D.1 n° 7 à 9) ; HS2-05 : dernier `started_utc` et `n_windows_demande` sur 4 093 `run_params` (classe M). Aucune de ces valeurs n'est reproduite dans le code ni dans les tests du lot (C-B0-10 (iv), §12) ; ce journal ne les recopie qu'ici, pour déclarer l'exposition.
- **Non ouverts** : les pièces D.2 n° 1 à 9, toutes ; aucune copie scellée ; ADR-0025 et la cartographie : jamais affichées, lues en octets par `d2_check.py` seulement, dans la copie `arbres/final`, qui ne rend que des numéros de ligne et des comptes ; `JOURNAL.md` : non affiché (sujets de commit seulement, par `git log`) ; le corps du test nommé (l.261-281) : non affiché.
- **Balayage mécanique** : `cargo xtask verify` (S-G4, S-G5) lit tout `docs/`, dont les fichiers des pièces D.2 n° 5 et 6 ; seules les lignes de verdict ont été affichées.
- **Aucune statistique S2 calculée sur les journaux de campagne. Aucun z, aucun K, aucun P̂_more ni aucun φ de campagne vu.** Les rendus manipulés portent sur les fixtures synthétiques du collecteur scripté.

## 14. Corrections de la revue G2 (ajout daté du 2026-09-30 ; l.1-252 : texte revu, plus la ligne de C-5)
- **Générateur** : `claude-opus-5-5` (identifiant exact déclaré par le harnais en tête de session, R-1), effort max selon la commande de lancement (non observable depuis l'agent), contexte frais ; générateur G1 de correction, instance distincte du réviseur G2. Mandat : commande de mission de l'orchestrateur Shōgen (`claude-fable-5-1`, 2026-09-30). Aucun commit, aucun workflow (R-20) ; aucune variable `GIT_DIR` ni `GIT_WORK_TREE` posée, aucun `--write-tree`, aucun `git add` ; `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée.
- **Horloge** (`date -u`) : corrections appliquées au worktree à 2026-09-30T07:03:01Z ; oracles de 07:04:22Z à 07:16:53Z ; cette section écrite ensuite ; `lot.diff`, suites, `cargo --locked xtask verify` et enregistrement d'oracle refaits après elle, sur les copies qui la contiennent (heures au rapport de correction).
- **Revue appliquée** : `F:/tmp/shogen-lots/B-SEG-2/G2-rapport.md` (sha256 `e778cef1b224436e925502f5502f68430bea4d01995d374373efeafb21d222de`), verdict ACCEPTE-AVEC-CORRECTIONS, liste fermée C-1 à C-9.
- **C-1 à C-5, sous-lot B-SEG-2c** : texte du réviseur, `g2-oracles/corrections-G2-bseg-2c.diff` (sha256 `1aee48cf077b6668ac08ed730558cc4b90535e0615df752e164260a8e3224eac`), appliqué tel quel par `patch -p1`, sans décalage ni fuzz. Provenance : 40 lignes ajoutées (code +1 −1, tests +38 −3, ce journal +1), rédigées par le réviseur G2 (`claude-opus-5-5`) et appliquées sans retouche ; `s2-harness` du worktree est identique à l'arbre `g2-fix` du réviseur (`diff -r`), et ce journal l'était aussi avant l'ajout de cette section (`cmp`).
  - C-1 : `test_epoch_zero_accepte_t0_fractionnaire_refuse` : 0 accepté à la CLI et à l'API ; t0 = −0,5 refusé aux quatre points d'entrée, à fin comme à n fixe (bord de SHOGEN-NEG-EPOCH-1 ; D-4, D-5).
  - C-2 : dans `test_dates_de_campagne_…`, la ligne `exclusion_retraits_union` sous segment (assiette de D-3).
  - C-3 : `test_premiere_et_derniere_fenetre_hors_ordre_du_journal` : campagne écrite hors ordre par le collecteur réel ; première et dernière fenêtre par tri (D-6).
  - C-4 : `_retires` (`report.py`) imprime « 0 (aucune fenêtre au journal) » quand le journal n'a aucune fenêtre, au lieu d'un compte vide ; assertion dans `test_journal_sans_fenetre_…` (D-7, D-8). Le cas « non testé » du Review Focus 3 (§10) est ainsi corrigé et tenu par un test.
  - C-5 : au §12, la première émission de l'enregistrement d'oracle (`…-56392.json`), remplacée.
- **Coupe, mesurée** (`oracles/mkdiff.py`, hors dépôt) : B-SEG-2a 176, B-SEG-2b 71, **B-SEG-2c 39** (code +1 −1, tests +38 −3 ; ce journal hors compte). Empilés dans l'ordre 2a, 2b, 2c sur des copies de `b72509b` : 212, 214 puis 216 tests, tous OK (2 sauts, variable absente).
- **Oracles** : suite 216 tests OK (2 sauts), 0 entrée TMP, 0 `__pycache__`, sur le worktree et sur les copies ; F2P : code livré avec les tests corrigés, un seul FAIL (le test de C-4), 0 ERROR ; mutants de la revue : MH01, MH02 et MH11 à MH15 survivent à la suite livrée et sont tués sur l'arbre corrigé, chacun par le seul test prévu ; colonne P complète : 21 tués sur 21, dont MH22 (C-4 retirée), témoin vert ; campagne du G1 (§5) rejouée sur l'arbre corrigé : 39 tués sur 39, témoin vert ; P2P texte (instrument du réviseur) : les 86 sorties de la suite de base et les 107 de la suite livrée sont identiques sous le code corrigé ; épingles inchangées (`b054a0f4…`, `677b1bfc…`).
- **C-6 à C-9** : actes de l'orchestrateur, non exécutés ici. C-6 (lignes datées 2a, 2b, 2c ; plan de commits) et C-9 (trois items proposés) : diff séparé, hors dépôt ; C-7 (ratification de D-1 à D-13 et du renommage) : aucun texte proposé ; C-8 (rejeu du test nommé, clôture de SHOGEN-EXCL-COMPTE-1, SHOGEN-NEG-EPOCH-1 et HS2-05, précondition de RENDU-1) : commande et contrôles au rapport de correction (`F:/tmp/shogen-lots/B-SEG-2/correction-rapport.md`).
- **Écarts** : déclarés au rapport de correction, dont une écriture transitoire sur C: (repli de `tempfile` sur un TMP inexistant, dossier retiré à la sortie, 0 entrée laissée), sans effet sur le lot.
- **Attestation** (forme D.3) : pièces D.2 n° 1 à 9 non ouvertes ; aucune copie scellée ; `JOURNAL.md` non affiché ; test nommé non affiché (la première ligne de sa docstring vue dans une sortie verbeuse de la suite, ligne de saut). Exposé aux bornes, comptes et taux de santé du harnais que portent ADR-0028 D5, la revue G2 et ce journal ; aucun n'est reproduit ici. Aucune statistique S2 calculée sur les journaux de campagne. Aucun z, aucun K, aucun P̂_more ni aucun φ de campagne vu.
