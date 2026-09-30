# G1 — lot B-SEG-1 d'ADR-0028 (un seul outil de lecture par horodatage : segment D4 et D2 pt 6, exclusion D5 ; HS2-08), Shōgen S2 — journal

- **Modèle** : `claude-opus-5-5` (identifiant exact déclaré par le harnais en tête de session), effort max selon la commande de lancement (le réglage n'est pas observable depuis l'agent), contexte frais ; worker G1 (R-1 déclaré en tête de session). Aucun commit, aucun workflow déclenché (R-20). Aucune variable `GIT_DIR` ni `GIT_WORK_TREE` posée, aucun `--write-tree`. Écritures git limitées au worktree du lot (§0) : avance rapide de sa branche vers `0abc881`, puis `git add -N` des deux fichiers neufs pour le diff prescrit.
- **Horloge** (`date -u`) : première horloge relevée 2026-09-30T00:19:37Z ; table C-5 entre 00:19:37Z et 00:29:18Z ; estimation R-25 et catégories F2P écrites à 00:29:18Z, avant tout code ; 1a gelé à 00:34:00Z, regelé à 00:38:36Z (§4, A21) ; première mesure de 1b à 00:48:34Z (214 lignes, §1) ; arbre final gelé à 00:57:16Z ; coupe C-8 du test nommé vers 01:04Z ; empreintes à 01:05:30Z ; journal écrit ensuite ; `cargo --locked xtask verify` VERT de 01:10:47Z à 01:10:50Z sur ce journal avant sa dernière édition, rejoué après elle (heures dans `oracles/xtask-lot.out`) ; suites finales de 01:11:22Z à 01:11:44Z (final 203, 1a 195, 1a + N 196, base 193) ; enregistrement d'oracle écrit en dernier (chemin et sha dans `oracles/LIVRABLES.sha256`).
- **Mandat** : commande de mission de l'orchestrateur Shōgen (`claude-fable-5-1`, 2026-09-30), lot B-SEG-1 de l'annexe A (l.15) : D4, D5, D2 pt 6, HS2-08, SHOGEN-J14-TRONCATURE-1, SHOGEN-EXCL-TOUS-TYPES-1, FM-1.5 ; corrections C-1 à C-15 du cp-1 bref. Cadre : ADR-0028 et annexes A à D à `0abc881`.
- **Classification** : bounded. Le chemin existe (lecteur `records` → `r1`/`lm`/`r2` → `report`) ; le lot remplace le filtre de marqueurs du lot A par un outil unique appliqué aux trois types horodatés, au même point des quatre points d'entrée.
- **Résultat** : lot coupé en trois sous-lots, chacun sous 200 lignes : **B-SEG-1a** (outil et D5, 111), **B-SEG-1a-N** (test nommé, 51, séparable par C-8), **B-SEG-1b** (segment, 198). Suite verte (203 tests, 2 sauts, tous deux motivés par `SHOGEN_S2_CAMPAGNE_CONTROL`), TMP neuf à 0 entrée, 0 `__pycache__`, 21 + 21 + 28 mutants tués sans survivant, F2P par famille conforme aux catégories fixées d'avance, épingles et rendus sans option identiques à l'octet, `cargo --locked xtask verify` VERT.

## 0. Préconditions mesurées avant code

- **Base (E-1)** : le harnais a créé le worktree sur la branche `worktree-wf_1c82774a-d5f-2` à `fa0ce5b`, 34 commits derrière `0abc881`, sans `docs/adr-0028/` (mesuré : `git merge-base --is-ancestor fa0ce5b 0abc881` vrai ; `git rev-list --count fa0ce5b..0abc881` = 34). Acte du worker : `git merge --ff-only 0abc881` dans ce seul worktree. Aucun objet écrit ; `main` et l'arbre du dépôt principal ne sont pas touchés. **Écart au geste de B0** (`git switch --detach`, HEAD privé) : l'avance rapide déplace la référence de la branche du worktree, qui vit dans les références partagées du dépôt (`refs/heads/worktree-wf_1c82774a-d5f-2`, de `fa0ce5b` à `0abc881`). Déclaré ; à arbitrer par l'orchestrateur (Q-G1-9).
- **C-8 non satisfaite à la base** : à `0abc881`, l'annexe D l.108 porte encore « proposition du rédacteur, à ratifier » ; `JOURNAL.md` ne consigne ni la ratification de D.4 a (b), ni les lots CI-S2 et B0 (aucune occurrence de `CI-S2`, `lot B0`, `B0-1`, `D.4`) ; l'annexe A n'a pas de ligne B0-1 ni B0-2. Ces actes appartiennent à l'orchestrateur. Application de la clause « à défaut » de C-8 : **le test nommé est livré en sous-lot séparable B-SEG-1a-N** (§1), qui ne touche que `tests/test_exclusion.py`, fichier que B-SEG-1b ne modifie pas : les deux sous-lots commutent.
- **Variable `SHOGEN_S2_CAMPAGNE_CONTROL`** : jamais posée pendant ce G1 (chaque script d'oracle la retire de l'environnement). Les tests (ii) et (ii bis) lèvent donc `SkipTest` : ce sont les deux sauts de chaque exécution.
- **Suite de base** (arbre `0abc881` extrait par `git archive`, TMP neuf) : `Ran 193 tests … OK (skipped=1)`, 0 entrée TMP, 0 `__pycache__` (`oracles/suite-base.out`).
- **Table C-5 (compatibilité mesurée, analogue de la table ok(f, s) de B0 §0)** : sur l'arbre de base, les quatre points d'entrée et la CLI (appels `subprocess`) ont été instrumentés pendant la suite complète. Pour chaque appel à plage non vide, le script compte ce que D5 retirerait : `harness_ts` et `ts` dans [A ; B + w), `window_start` dans [A ; B] pour mémoire (`oracles/table_horodatages_base.py`, sortie `oracles/table-horodatages-base.out`, sha256 `f381586838415bd2010efc19807a9680a9cfe50cbd1478fb2158ba5092a98385`).
  - 193 tests, 0 échec sous instrumentation ; **78 appels** à plage non vide ; **aucune fixture à plage ne porte d'`asn_attribution`** (0 appel) ;
  - des `clock_check` seraient retirés dans **4 tests** seulement : `test_bornes_egales_une_seule_fenetre` (horloges de w0 et w1, plages [w0 ; w0] et [w1 ; w1]), `test_plages_chevauchantes_et_emboitees`, `test_regle_apres_exclusion_strate_videe_hors_de_s` (horloge de w0 dans [w0 ; w2 + w)) et, pour l'appel `r2` seul, `test_epingle_sans_flux_mort_octets_de_base_avec_option` (plage « tout ») ;
  - `r1` et `lm` ne consomment ni horloge ni ASN ; `r2` ne consomme pas d'horloge ; le rendu n'imprime les horloges qu'au bloc 1 ; aucun de ces 4 tests ne compare le bloc 1 ni un octet qui en dépend ;
  - les deux épingles portent sur des rendus sans retrait : `SHA_BASE_SANS_OPTION` (`tests/test_exclusion.py:28`, `a4ffc3e5…49a5`, aucune option) et `SHA_BASE_AVEC_OPTION` (`tests/test_pool_analyse.py:27`, `a4dd4c00…7520`, plage [w2 ; w4], horloges à w0 et w1 hors de [w2 ; w5)).
  - **Prédiction écrite avant code : tests existants verts sans modification, aucune re-capture.** Mesure : les 193 tests passent sur le code 1a avant tout test neuf (`oracles/suite-1a-code-seul.out`), puis sur le code 1b (`oracles/suite-1b-code-seul.out`) ; aucune ligne existante d'un test n'est modifiée (`test_exclusion.py` ne reçoit que des lignes ajoutées, les autres fichiers de test sont intouchés, §2).
- **Fixture « démarrage sans fenêtre » (avis advisor, pt 6)** : `collector.collect(…, n_windows=0)` écrit exactement un `run_params` et un `clock_check` à `harness_ts = t`, aucun marqueur ni `journal.jsonl` ; `effective_run_params` reste concordant sur 5 démarrages ; `r2.collect_asn` date chaque relevé à `now_fn()` (`oracles/valide_collect_n0.py`, sortie `oracles/valide-collect-n0.out`, sha256 `8b1afefb758158944d15b6389515004069fe49bb4b180cf8dd84b0c1f8987841`).

## 1. Coupe R-25 (C-10, C-8)

- **Estimation ascendante écrite avant le code** (00:29:18Z, `oracles/estimation-r25.txt`, sha256 `27a4e18a8ec3f519e7295d942bacbdb5dfa675c133f6b66030baa1e18b573026`) : 1a ≈ 136 (≈ 160 avec la marge du précédent B0 E-3), 1b ≈ 164 (≈ 190 avec marge). Frontière de C-10 reprise telle quelle.
- **Mesures** (méthode du lot A et de B0 : lignes `+` des diffs, fichiers neufs entiers ; diffs produits par `oracles/mkdiff.py`, applicables par `patch -p1`) :
  - 1a gelé à 00:34:00Z : 159 ; + 2 à 00:38:36Z (assertion fail-closed qui tue A21, §5) ; + 1 au rebouclage des docstrings à 110 colonnes : 162 avec le test nommé ;
  - 1b, première mesure à 00:48:34Z : **214 > 200** (tests 146 contre 116 estimés ; code 68 contre 48). Resserrement **sans retrait d'assertion** (précédent du lot A, 222 → 196) : docstrings de l'outil et du point d'application, ligne du bloc 1 de 6 à 4 lignes, aide CLI, fusion des tests « hors grille » et « type vidé », cas n = 6 et n = 0 portés par la boucle de refus existante ; 201, puis 196 ; rebouclage à 110 colonnes : 197 ; assertion `n fixe = 3` ajoutée en préparant les mutants (sans elle, B27 survivait) : **198** (E-2) ;
  - C-8 : le test nommé et ses quatre helpers sortent de 1a en sous-lot séparable.

| sous-lot | modules `shogen_s2` | tests | total ajouté | seuil |
|---|---|---|---|---|
| B-SEG-1a (outil, D5) | +48 −12 (records +38, r1 +2, lm +2, r2 +3, report +3) | `test_exclusion.py` +63 | **111** | ≤ 200 |
| B-SEG-1a-N (test nommé) | 0 | `test_exclusion.py` +51 | **51** | ≤ 200 |
| B-SEG-1b (segment) | +59 −19 (records +30, r1 +4, lm +4, r2 +4, report +17) | `test_segment.py` 139 (neuf) | **198** | ≤ 200 |
| lot entier (diff base → final) | +93 −17 (les lignes de 1a réécrites par 1b n'y comptent qu'une fois) | +253 | 346 | coupe obligatoire |

  Documentation hors compte (précédent du lot A) : ce journal.
- **Lignes datées proposées pour l'annexe A** (amendement daté : acte de l'orchestrateur, non écrit ici ; précédent B0, C-8) :
  - **B-SEG-1a** (2026-09-30, coupe R-25 du G1 de B-SEG-1) : D5, outil unique `records.filtre_horodatage` et point d'application `records.filtre_lecture` aux quatre points d'entrée et au rendu ; `exclude_window_start_ranges` devient un cas de l'outil. Véhicule : `s2-harness/shogen_s2/{records,r1,lm,r2,report}.py`, `tests/test_exclusion.py`. Oracle : suite unittest ; fixture à `clock_check` et `asn_attribution` posés sur A − 1, A, B, B + 59, B + 60 ; fixture « type vidé » ; 21 mutants. Taille 111 [mesuré]. Tuyau : journaux (tous types) → exclusion → points d'entrée, consommateur RENDU (après B-SEG-2). cp-1 bref.
  - **B-SEG-1a-N** (2026-09-30, clause « à défaut » de C-8) : test nommé `tests/test_exclusion.py::TestExclusionJournalReel::test_ii_plage_adr0025_comptes_par_type` et ses helpers. Consommable après la consignation de la ratification de D.4 a (b) et la mise à jour de l'annexe D l.108. Oracle : rejeu par l'orchestrateur seul, variable posée (§6). Taille 51 [mesuré]. cp-1 bref.
  - **B-SEG-1b** (2026-09-30, coupe R-25 du G1 de B-SEG-1) : D4 et D2 pt 6 (segment semi-ouvert sur tous les types, `records.t_fin_n_fixe`, options `--segment-from` et `--segment-to` | `--segment-n-fixe`, ligne `segment` du bloc 1) ; SHOGEN-J14-TRONCATURE-1. Véhicule : mêmes modules, `tests/test_segment.py`. Oracle : module neuf de 7 tests ; 28 mutants. Taille 198 [mesuré]. Consommateur RENDU (J14 ×2, J28). cp-1 bref.

## 2. Changements (worktree du lot, sur `0abc881`)

| fichier | B-SEG-1a | B-SEG-1b | sha256 base → 1a → 1a + N → final |
|---|---|---|---|
| `shogen_s2/records.py` | `HORODATAGE` (type → champ) ; `filtre_horodatage(recs, ranges, w)` ; `filtre_lecture(params, markers, clock_checks, asn, ranges)` ; `exclude_window_start_ranges` = appel de l'outil | segment dans l'outil ; `t_fin_n_fixe(markers, t0, n, w)` ; `filtre_lecture(…, segment)` rend aussi les bornes | ea4d6da2 → a293e9d4 → a293e9d4 → 50adbc2c |
| `shogen_s2/r1.py`, `lm.py` | l'appel du filtre de marqueurs devient `filtre_lecture` | kwarg `segment` transmis | r1 1e6a115c → ae3a4c76 → ae3a4c76 → 992f841c ; lm 9ff03bf1 → 2117121d → 2117121d → e81ee2f1 |
| `shogen_s2/r2.py` | `filtre_lecture` sur marqueurs et `asn_attribution` | kwarg `segment` transmis | d76170de → e30d5a33 → e30d5a33 → 99a5b9ff |
| `shogen_s2/report.py` | `filtre_lecture` sur marqueurs, `clock_check` et `asn_attribution` | kwarg `segment` ; ligne `segment` du bloc 1 ; options CLI | c1b9210a → ac231d0e → ac231d0e → 3d95818f |
| `tests/test_exclusion.py` | `poser` ; classe `TestExclusionTousTypes` (2 tests) | — | 408731bc → a4c3497d → f02c1a49 → f02c1a49 |
| `tests/test_segment.py` | — | neuf (7 tests) | — → — → — → 2091f213 |

- Empreintes complètes : `oracles/{base,1a,1a-plus-N,final}-sha256.txt`. **Intouchés** (sha égaux à la base dans les quatre états, 22 fichiers) : tous les autres `.py` de `s2-harness`, dont les modules de quarantaine `collector`, `sources`, `run_campaign`, `closure`, `smoke`, `journal`, `model` (D6 i), `window`, et tous les tests existants hors `test_exclusion.py`, où seules des lignes ont été ajoutées (aucune ligne existante modifiée ni retirée).
- **Aucune dépendance neuve** (bibliothèque standard : `itertools.count` dans les tests).

## 3. Définitions appliquées — ce que la mission fixe, ce qu'elle laisse ouvert

- **Un seul outil (C-1, FM-1.5)** : `records.HORODATAGE` associe chaque type de `control.jsonl` à son champ d'horodatage (`window_close` → `window_start`, `asn_attribution` → `ts`, `clock_check` → `harness_ts`, `run_params` → aucun). `records.filtre_horodatage` porte les deux règles, et **une seule fonction** les applique : `records.filtre_lecture`, appelée au même point par `r1.recompute_from_journal`, `lm.recompute_lm_from_journal`, `r2.recompute_r2_from_journal` et `report.render_report` (donc par la CLI).
- **Ordre (C-2)** : `parse_control` (et `parse_asn` pour r2 et le rendu) → `effective_run_params` sur **tous** les `run_params` → `verify_markers_against_spec` sur **tous** les marqueurs → dans `filtre_lecture` : `t_fin_n_fixe` sur les marqueurs non filtrés, puis segment, puis exclusion (dans la boucle de l'outil, le test de segment précède celui d'exclusion) → `analysis_pools` (D1). `journal.jsonl` n'est jamais filtré : les lectures d'un marqueur retiré deviennent orphelines, mécanisme existant.
- **Segment (C-1, D4, D2 pt 6)** : [t0 ; t_fin) semi-ouvert, **la même borne** sur `window_start`, `ts` et `harness_ts`, sans variante par type. Justification de la borne pour les types autres que `window_close` : une fenêtre retenue couvre [ws ; ws + w) ; les fenêtres retenues couvrent donc exactement [t0 ; t_fin) quand t_fin = dernier `window_start` retenu + w, et un enregistrement horodaté dans cet intervalle appartient à la durée d'une fenêtre retenue. Pour le J14 second (270), l'opérateur passe `--segment-to` = 2026-09-04T00:00:00Z + w, soit la dernière fenêtre ≤ 00:00Z incluse, pour tous les types. **Aucune date dans `shogen_s2/`** : bornes en paramètres (API `segment={"t0", "t_fin"}` ou `{"t0", "n_fixe"}` ; CLI `--segment-from` avec `--segment-to` ou `--segment-n-fixe`, ces deux options exclusives entre elles).
- **t_fin à n fixe (C-3)** : `t_fin_n_fixe(markers, t0, n, w)` rend le n-ième `window_start` distinct, trié croissant, parmi les marqueurs à `window_start ≥ t0`, comptés avant segment et exclusion, + w. **Aucun défaut** : n obligatoire (paquet, option CLI), w = `params["w"]`. Hors de [1 ; nombre de fenêtres distinctes] : `ValueError`, jamais un t_fin silencieux (n = 0 compris).
- **Exclusion (D5, C-6)** : `window_start` dans la plage **fermée** [A ; B] (prédicat propre, inchangé depuis le lot A) ; `ts` et `harness_ts` dans [A ; B + w). Les deux prédicats restent distincts : pour des bornes hors grille, « fermé sur `window_start` » n'est pas réductible à [A ; B + w) (mutant A06, tué par `test_fenetre_a_cheval_bornes_hors_grille` et par le test « type vidé » neuf).
- **run_params** : jamais passés à l'outil par les points d'entrée (liste séparée, concordance sur tous les démarrages avant tout filtre) ; pour un appelant direct, la table les conserve.
- **Fail-closed** : type d'enregistrement sans règle ⇒ `ValueError` ; segment sans fin, à deux fins, vide ou inversé (t0 ≥ t_fin) ⇒ `ValueError` ; segment partiel à la CLI ⇒ rc 2 (argparse). **Sans plage ni segment, l'outil rend la liste inchangée** : c'est la condition des épingles.
- **Bloc 1 (C-4)** : B-SEG-1b imprime une ligne `segment = [t0 ; t_fin) = [ISO ; ISO) semi-ouvert, fin exclue, même borne sur window_start, ts, harness_ts (run_params conservés) ; n fixe = N | - — ADR-0028 D4, D2 pt 6`, seulement quand l'option est donnée, avant les lignes d'exclusion. La ligne d'exclusion du lot A reste identique à l'octet (épingle `SHA_BASE_AVEC_OPTION`). **État transitoire déclaré : B-SEG-1 seul n'est pas consommable par RENDU ; B-SEG-2 doit précéder RENDU.** Le rendu ne décrit pas encore l'extension D5 aux `ts` et `harness_ts`, ni les comptes par type (D5 l.56 : « Les comptes sont déclarés au bloc 1 ») ; les dates de campagne restent à HS2-05 (Q-G1-3).
- **Bornes non entières** : l'API du segment compare les bornes telles quelles (aucune troncature) ; `exclusion_ranges` tronque par `int()` (comportement du lot A, inchangé) ; la CLI n'accepte que des entiers (`type=int`). Review Focus 3.

## 4. Tests (bibliothèque standard, forme de `tests/`) — chaque test nomme la mutation qui le rougit

- **Fixtures (précédent C-B0-3)** : `build_fixture` du lot A (w0..w5, reprise w1..w3, démarrages à w0 et w1), complétée par `poser(d, instants)` : sur chaque instant, un démarrage sans fenêtre du collecteur réel et une sonde `r2.collect_asn` datée, avec un AS distinct par appel et par hôte. Les survivants se lisent sans ambiguïté : l'`offset` médian du bloc 1 est propre à chaque instant (distinction assertée), et la suite des divergences ASN d'un hôte nomme les relevés retenus. Aucun JSONL écrit à la main, hors le ré-étiquetage d'un marqueur (précédent `test_garde_53_voit_les_marqueurs_exclus`). Aucun nom de flux ni d'hôte : `SKELETON` et `r2.build_flux_hosts`.
- **B-SEG-1a** (`tests/test_exclusion.py`, classe `TestExclusionTousTypes`) :
  - `test_d5_bornes_par_type_aux_points_d_entree_et_cli` : horloges et sondes sur A − 1, A, B, B + 59, B + 60, plage [A ; B] = [w2 ; w4]. n identique aux quatre points ; bloc 1 : horloges gardées exactement pour w0, w1, A − 1 et B + 60 ; `run_params_demarrages = 7` ; `r2` : une divergence par hôte, de A − 1 à B + 60 ; rendu : autant de lignes `DIVERGENCE ASN` que d'hôtes ; CLI = API à l'octet ; type sans règle ⇒ `ValueError`. Rougit si : borne ±1 ; `ts` ou `harness_ts` fermé sans + w ; asn ou horloge non filtré (outil, r2, rendu) ; run_params filtrés ; type sans règle accepté.
  - `test_type_vide_rendu_sans_asn_ni_horloge` (C-15) : [w0 ; w5 − 1] retire toutes les horloges et toutes les sondes (t < w5 + 59), mais garde w5 (fermée sur `window_start`). Le rendu sort : 0 ligne `controle_horloge`, chemin « axe ASN NON MESURÉ », n = 1 en stress ; CLI = API. Rougit si : asn ou horloge non filtré ; `window_start` traité en [A ; B + w).
- **B-SEG-1a-N** (`TestExclusionJournalReel.test_ii_plage_adr0025_comptes_par_type`, §6) : non exécuté par ce G1. Ses deux helpers ont été rejoués **sur fixture**, sans la variable, via `oracles/valide_test_nomme_fixture.py` : sur la fixture de bornes, l'outil et le recompte séparé rendent tous deux {window_close 3, asn 9, clock 3}, valeurs lues sur le script de la fixture. Contrôle négatif : bornes décalées d'une seconde ⇒ {1, 3, 1}, identiques entre les deux voies (`oracles/valide-test-nomme-fixture-final.out`, sha256 `3a6381635c3a0dca1c289ae585bb2db90277c39a549243b917b19c0715b32464`).
- **B-SEG-1b** (`tests/test_segment.py`, module neuf, 7 tests ; fixture + `poser` sur t0 − 1, t0, t_fin − 1, t_fin avec [t0 ; t_fin) = [w1 ; w4)) :
  - `test_bornes_tous_types_aux_quatre_points_et_cli` : n = {calme 2, stress 1} aux quatre points ; horloges gardées exactement sur t0 et t_fin − 1 ; `run_params_demarrages = 6` ; divergences ASN de t0 à t_fin − 1 ; ligne `segment` du bloc 1 en epoch et ISO ; CLI = API.
  - `test_bornes_hors_grille_et_type_vide` : [w1 + 1 ; w3 + 1) garde w3 (= t_fin − 1) et retire w1 (= t0 − 1) ; [w5 ; w5 + w) ne garde aucune horloge ni sonde, le rendu sort.
  - `test_n_fixe_lu_du_journal_avant_exclusion` : n = 3 avec doublons w1-w3, w0 avant t0 et l'exclusion [w2 ; w2] ⇒ t_fin = w4, mêmes sorties `r1`, `lm`, `r2` et même rendu qu'en t_fin explicite, à la mention `n fixe = 3` près ; CLI = API.
  - `test_moins_de_n_fenetres_leve_jamais_silencieux` : n = 5 ⇒ t_fin = w5 + w ; n = 6 ⇒ rc 1 à la CLI, stdout vide.
  - `test_segment_incomplet_double_ou_vide_refuse` : rc 2 pour un début seul, une fin seule, un n seul et deux fins ; `ValueError` aux quatre points pour un segment vide, inversé, sans fin, à deux fins, n = 6 ou n = 0.
  - `test_garde_53_sur_tous_les_marqueurs` : w5, hors segment, ré-étiquetée « calme », lève aux quatre points.
  - `test_run_params_hors_segment_toujours_verifies` : un démarrage à τ divergent posé hors segment lève aux quatre points (§E).
- **F2P par famille (C-11, catégories fixées avant code)** :

| famille | test | arbre parent | résultat | sortie (sha256) |
|---|---|---|---|---|
| F-1 D5 par `exclude_ranges` | 2 tests de `TestExclusionTousTypes` | base `0abc881` | **FAIL** (AssertionError) ×2, jamais ERROR | `oracles/f2p-1a-base.out` |
| F-2 segment (module neuf) | 7 tests de `test_segment.py` | 1a gelé ; base | **ERROR** ×7 (TypeError : kwarg `segment` inconnu), sur les deux | `oracles/f2p-1b-sur-1a.out` (`1aabf7c3…eeef`) ; `oracles/f2p-1b-sur-base.out` (`ff856492…c9f`) |
| F-3 test nommé | `test_ii_plage_adr0025_comptes_par_type` | — | à établir par l'orchestrateur seul (§6), compté à part | — |
| F-4 épingles | `test_iv_…`, `test_epingle_…` | — | inchangées, passent (P2P par construction), comptées à part | — |

- **Exécutions** (TMP neuf, variable non posée, `PYTHONDONTWRITEBYTECODE=1`) : base 193 tests, OK (skipped=1) ; 1a 195, OK (skipped=1) ; 1a + N 196, OK (skipped=2) ; final **203**, OK (skipped=2) ; 0 entrée TMP et 0 `__pycache__` à chaque exécution (`oracles/suite-*.out`). Décompte : 193 + 2 (1a) + 1 (1a-N) + 7 (1b) = 203.
- **Rendus identiques à l'octet (C-5), au-delà des épingles** : `oracles/p2p_rendus.py`, repris tel quel du G1 B0 (sha256 identique), hache chaque sortie de `render_report` et chaque stdout de la CLI dans la suite existante (56 sorties : 45 API, 11 CLI). Base contre final, après le masquage de B0 E-7 (heure murale de `collect_asn` dans `RunSegmentCase`) : **exactement les 6 différences prédites par la table C-5**, toutes des rendus API à plage (2 dans `test_bornes_egales…`, 3 dans `test_plages_chevauchantes…`, 1 dans `test_regle_apres_exclusion…`), et **0 différence CLI** (`oracles/p2p-base-vs-final.out`, sha256 `335cc671f674c805c117a1b56d04e6831bababdc746388a61df3efaf845c989b`). Ces rendus, rejoués sur fixtures par `oracles/diff_rendus.py`, ne diffèrent que par l'absence des lignes `controle_horloge` retirées par D5 ; tout le reste est identique ligne à ligne (`oracles/diff-rendus-base-vs-final.out`, sha256 `1366c83bbd6af20910990d79276fa20bdfa64db2493edbe85bc454b835e88708` ; même verdict sur 1a).

## 5. Mutants (copies sous `F:/tmp/shogen-lots/B-SEG-1/work/mut-*`, suite complète, TMP neuf, variable jamais posée) — `oracles/mutants.py`

**B-SEG-1a : 21 mutants, 21 tués** sur l'arbre 1a gelé (`oracles/mutants-1a.out`, sha256 `90da76af0c219d62c7cecf3ae6d361d46c14d23240ba98fabce8d70caa682e87`) ; rejoués sur l'arbre final avec les motifs adaptés : 21 tués (`oracles/mutants-1a-sur-final.out`, sha256 `ed50770737412ef1c98edff539b17dc958ba970b60368bb86b53ca4f89fcaec4`) ; rejoués sur l'arbre du sous-lot 1a sans le test nommé : 21 tués (`oracles/mutants-1a-sans-nomme.out`, sha256 `53b22f852be12afcea26755afa75a3cbdcc379e6f2ec284c2556ffb17d9aa324`). Le test nommé, sauté sans la variable, ne tue aucun mutant.

| # | mutant | rougi par |
|---|---|---|
| A01 | borne A exclusive sur `ts`/`harness_ts` | D5 bornes, type vidé |
| A02 | A − 1 inclus | D5 bornes |
| A03 | `ts` fermé [A ; B + w] | D5 bornes ; `test_plage_hors_campagne…` (G2 lot A, attendu par C-14) |
| A04 | fin B + w − 1 (B + 59 gardé) | D5 bornes |
| A05 | `ts` fermé [A ; B] sans + w | D5 bornes, type vidé |
| A06 | `window_start` traité en [A ; B + w) | `test_fenetre_a_cheval_bornes_hors_grille` (attendu par C-6), type vidé |
| A07 | `window_start` à borne haute exclusive | 8 tests existants et D5 bornes |
| A08, A09 | type oublié à l'outil (asn ; horloge) | D5 bornes, type vidé |
| A10 | `r2` : asn non filtré | D5 bornes |
| A11, A12 | rendu : horloge ; asn non filtré | D5 bornes, type vidé |
| A13-A16 | filtre omis à un point d'entrée (r1, lm, r2, rendu) | 8 à 10 tests existants et neufs chacun |
| A17 | w remplacé par 0 | D5 bornes, type vidé |
| A18 | run_params filtrés par `started_epoch` (rendu) | D5 bornes (`run_params_demarrages = 7`) |
| A19 | filtre du rendu avant la garde §5.3 | `test_garde_53_voit_les_marqueurs_exclus` |
| A20 | `exclude_window_start_ranges` devenu l'identité | D5 bornes, `test_doublons…`, épingle, `test_regle_apres…` |
| A21 | type sans règle conservé | D5 bornes (survivant de la première campagne : l'assertion fail-closed a été ajoutée, §1) |

**B-SEG-1b : 28 mutants, 28 tués** sur l'arbre final (`oracles/mutants-1b.out`, sha256 `7325dca35bf8abe31b04ea2478f447aa7bc5dd69ac310de2cd12fb6f5a2c954f`).
- B01 fin incluse ; B02 début exclu ; B03 t0 − 1 inclus ; B04 t_fin − 1 exclu ; B05 à B07 segment sur `window_start` seul, sans asn, sans horloge : `test_bornes_tous_types…` (et `test_bornes_hors_grille…` sauf B01).
- B08 à B11 segment omis à un point d'entrée (r1, lm, r2, rendu) ; B12 option CLI non transmise ; B13 ligne `segment` absente ; B28 bornes ISO absentes : `test_bornes_tous_types…` et d'autres.
- B14 ligne `segment` imprimée sans option : `test_iv_sans_option…` et l'épingle `test_epingle…` (existants).
- B15 t_fin calculé après l'exclusion ; B27 `n fixe` absent de la ligne : `test_n_fixe…`.
- B16 doublons comptés ; B17 fenêtre avant t0 comptée ; B19 + w omis ; B20 rang décalé : `test_n_fixe…` et `test_moins_de_n…` (B16, B17 aussi par `test_segment_incomplet…`).
- B18 t_fin silencieux sous n ; B21 segment vide accepté ; B22 deux fins acceptées ; B23 exclusivité CLI retirée ; B24 segment partiel accepté : `test_segment_incomplet…` (B18 aussi par `test_moins_de_n…`).
- B25 garde §5.3 après le segment : `test_garde_53_sur_tous_les_marqueurs`.
- B26 run_params filtrés par le segment : `test_run_params_hors_segment…`, `test_bornes_tous_types…`, `test_n_fixe…`.

Après chaque mutant, la copie est jetée ; le worktree n'a jamais porté de mutant.
- **Mutants équivalents déclarés** : (1) segment appliqué après l'exclusion : l'intersection des deux filtres commute, seul t_fin dépend de l'ordre (B15, tué) ; (2) retrait du retour anticipé « sans plage ni segment » : sur tout chemin servi, `parse_control` et `parse_asn` ne livrent que des types connus, donc la boucle rend la même liste ; seul un appelant direct passant un type inconnu sans option verrait la différence (`ValueError` au lieu de l'identité).

## 6. Test nommé (B-SEG-1a-N) — protocole de rejeu pour l'orchestrateur (C-9, C-11, D.4 a pt 2)

- **Nom** : `tests/test_exclusion.py::TestExclusionJournalReel::test_ii_plage_adr0025_comptes_par_type`, l.245-265 de l'arbre final.
- **Attendus**, cités par fichier:ligne dans sa docstring : `docs/adr-0028/ADR-0028-decisions-sortie-S2.md` l.56-57 (D5 : `asn_attribution` 5 313 et `clock_check` 483 sur [1790273880 ; 1790435340)) ; `window_close` : 2 618 fenêtres distinctes sur [A ; B] (ADR-0025 l.3 et l.44, test (ii)). Comptes bruts (lignes) pour asn et horloges, fenêtres distinctes pour les marqueurs ; repère de rejeu 5 313 = 11 × 483.
- **Lecture** : chaque enregistrement est projeté sur `record`, `window_start`, `ts`, `harness_ts` dès sa lecture (`CLES`, `_proj`) ; aucune autre clé n'est lue ni affichée ; w = 60 s (ADR-0028 l.35) en constante du test, jamais lu de `run_params`. Deux voies, assertées dans cet ordre : `recompte_independant` (bibliothèque standard, sans `records`), puis `comptes_outil` (`records.filtre_lecture` sur les listes de `parse_control` et `parse_asn`, comme en production, avant − après par type).
- **Commande de rejeu** (arbre gelé, copie scellée vérifiée par `SHA_CONTROL_SCELLE`) : `cd s2-harness && SHOGEN_S2_CAMPAGNE_CONTROL=<copie de control.jsonl> python -B -m unittest -v tests.test_exclusion.TestExclusionJournalReel`.
- **Comportement attendu sur la base** (fichier de test final copié sur `0abc881`) : le recompte séparé passe, puis `comptes_outil` lève `AttributeError` (`records.filtre_lecture` absent) ; le test est donc en ERROR, ni FAIL ni vert. Sur le gel : OK si les attendus d'ADR-0028 sont exacts. **Divergence : escalade, jamais le test ajusté à l'outil.** Un lecteur strict : une ligne illisible, même finale, fait lever le recompte séparé (Review Focus 5).

## 7. Tuyaux CA-11 (règle Branchement)
- **Entrée** : `control.jsonl` (les quatre types) et `journal.jsonl` produits par le collecteur ; ici, fixtures du collecteur réel et de `r2.collect_asn`.
- **Lecteur** : `parse_control`, `parse_asn` → `effective_run_params` → `verify_markers_against_spec` → `records.filtre_lecture` (t_fin à n fixe, segment, exclusion D5 : ce lot) → `r1.analysis_pools` (B0) → `compute_r1`, `compute_lm`, `compute_r2` ; `render_report` en fait autant et imprime la ligne `segment` au bloc 1. Les quatre points d'entrée appellent la même fonction.
- **Chemin servi** : la CLI `python -m shogen_s2.report` (RUNBOOK §9 e), rejouée dans un processus neuf par les tests D5, le test « type vidé » et 4 tests du segment.
- **Sortie aval** : le lot RENDU, qui n'est pas branché ; item formé, déclencheur **G0 de RENDU-1**, avec la condition B-SEG-2 d'abord (§3).
- **État** : aucun état persistant ; bornes et plages vivent dans les arguments et sont consignées dans la sortie.

## 8. Risques MAST nommés (C-11, CA-5) et contre-mesures
- **FM-1.5** (bornes de segment mal appliquées) : un seul outil et une seule borne pour tous les types ; enregistrements posés sur t0 − 1, t0, t_fin − 1, t_fin et sur A − 1, A, B, B + 59, B + 60 ; 49 mutants tués (21 de 1a, 28 de 1b), dont ceux de borne, de type et de point d'entrée ; bornes imprimées au bloc 1 en epoch et ISO ; aucune date dans le code.
- **FM-1.1** (pièces D.2) : aucune pièce de D.2 ouverte ; variable jamais posée ; ADR-0025 l.14 et cartographie l.51 repérées par sha256 par un script qui n'imprime que des numéros de ligne, jamais affichées (geste de B0 §15) ; ADR-0025 lue par plages (l.1-13, l.15-45) ; cartographie non lue au-delà de ce repérage. Chemins des fichiers des pièces D.2 n° 5 et 6 apparus dans des entrées d'outil : le script de repérage, les lectures par plages d'ADR-0025, et l'écriture de ce journal, qui les nomme pour les déclarer ; aucun autre chemin de D.2 (recherche a posteriori : orchestrateur).
- **FM-3.3** (oracle qui certifie une valeur supersédée) : attendus du test nommé tirés d'ADR-0028 D5 l.56-57 et d'ADR-0025 l.3 (errata ratifié 15:08Z), cités par fichier:ligne ; deux voies de comptage ; épingles existantes intactes ; compatibilité prédite par la table C-5, puis mesurée par P2P.
- **FM-2.3** (dérive de périmètre) : ni comptes par type au bloc 1, ni dates de campagne, ni refus des epochs négatifs (B-SEG-2) ; ni sensibilité, ni strate poolée ; les modules de quarantaine sont intouchés (§2). Le seul ajout hors brief est l'assertion fail-closed « type sans règle », qui tue A21.
- **FM-3.2** (vérification incomplète) : fixtures « type vidé » par plage et par segment ; doublons, fenêtre avant t0, bornes hors grille ; garde §5.3 et run_params hors segment ; n = 0 et n trop grand.

## 9. `error_origin` proposés (à assigner au G7)
- **E-1** : worktree créé à `fa0ce5b` au lieu de `0abc881` (même cause que B0 E-1). Origine : harnais du workflow.
- **E-2** : estimation 1b à ≈ 164, première mesure à 214. Origine : worker (tests sous-estimés de 30 lignes, code de 20). Corrigé par resserrement à 198, sans retrait d'assertion.
- **E-3** : deux erreurs d'outillage du worker, sans effet sur les livrables : `run_suite.sh` lancé une fois avec un chemin de sortie relatif (redirection refusée, aucun fichier écrit ; `git status` inchangé) ; `diff_rendus.py` a écrit une fois son JSON dans les copies `work/base` et `work/bseg-1a` (déplacé ; gel 1a revérifié identique au worktree par `diff -r` ; script corrigé en chemin absolu).
- **E-4** : 1a regelé deux fois (A21, puis rebouclage des docstrings à 110 colonnes). Les campagnes 1a ont été rejouées sur l'arbre gelé en dernier.
- **E-5** : écart au geste git de B0 (§0). Origine : worker. À arbitrer (Q-G1-9).

## 10. Review Focus
1. **Enregistrements de démarrage avant t0** : le `clock_check` de démarrage est daté `start_ts` (`collector.py` l.149, l.227) et les sondes ASN sont datées au lancement, **avant** le premier `window_start`. Un segment [t0 ; …) dont t0 est le premier `window_start` d'une campagne retire donc les enregistrements de démarrage de ce lancement. Si aucune reprise ne tombe dans le segment, le bloc 5 du J14 passe par « axe ASN NON MESURÉ » et k_eff n'est pas évaluable. La borne reste celle du brief (C-1) ; Q-G1-2.
2. **Message du bloc 5** (`report.py`, chemin « axe ASN NON MESURÉ ») : « aucun enregistrement asn_attribution au journal (collect_asn non lancé…) » est faux quand le filtre a tout retiré (fixture « type vidé »). Non corrigé ici (FM-2.3) ; Q-G1-3.
3. **Bornes non entières** : l'exclusion tronque (`int()`, lot A), le segment ne tronque pas ; la CLI n'accepte que des entiers.
4. **Unicité du point d'application** : elle tient par construction (les quatre points appellent `filtre_lecture`) et par les mutants B08-B11 et A13-A16 ; un point d'entrée futur devra l'appeler aussi.
5. **Test nommé** : le recompte séparé lit la copie scellée en strict (une ligne illisible fait lever) ; l'outil tolère une dernière ligne tronquée (`read_jsonl_tolerant`). Une divergence sur ce seul point signalerait une ligne finale coupée.

## 11. Questions ouvertes Q-G1-n (pour l'orchestrateur)
- **Q-G1-1** : ratifier les définitions du §3 (unicité de la borne de segment, t_fin à n fixe ≥ t0, rc 2 pour un segment partiel, `ValueError` pour un segment vide ou un type sans règle).
- **Q-G1-2** : item proposé **SHOGEN-SEG-DEMARRAGE-1** (enregistrements de démarrage datés avant t0, Review Focus 1). Propriétaire : orchestrateur. Déclencheur : avant le scellement du paquet. Mesure demandée, en comptes seulement (forme D.4 a) : nombre d'`asn_attribution` par hôte et de `clock_check` dans chaque segment (J14 principal, J14 second, J28). Si un segment n'a aucune sonde ASN, décision au paquet (k_eff « non évaluable » déclaré, ou règle d'appartenance des enregistrements de démarrage, qui amenderait C-1).
- **Q-G1-3** : items proposés pour le G0 de **B-SEG-2**, avec SHOGEN-EXCL-COMPTE-1 et HS2-05 : (a) comptes par type retirés, au bloc 1, par la plage et par le segment (D5 l.56) ; (b) ligne d'exclusion qui déclare l'extension D5 aux `ts` et `harness_ts` ; (c) message du bloc 5 quand le filtre a retiré toutes les sondes (Review Focus 2) ; (d) SHOGEN-NEG-EPOCH-1 étendu à `--segment-from` et `--segment-to`, qui acceptent aujourd'hui un epoch négatif, comme l'option d'exclusion.
- **Q-G1-4** : consigner la ratification de D.4 a (b) et mettre à jour l'annexe D l.108 (C-8) avant de consommer B-SEG-1a-N ; consigner les lots CI-S2 et B0 au JOURNAL ; ajouter les lignes datées B0-1, B0-2 et celles du §1 à l'annexe A.
- **Q-G1-5** : SHOGEN-J14-TRONCATURE-1 et SHOGEN-EXCL-TOUS-TYPES-1 **déclarés fermés** (C-7) : preuve sur fixtures aux §4-§5 (tous les types, aux quatre points et à la CLI) ; la preuve sur la copie scellée pour D5 est le rejeu du test nommé (§6), acte de l'orchestrateur.
- **Q-G1-6** : hors périmètre déclaré (C-7) : SHOGEN-NEG-EPOCH-1, SHOGEN-EXCL-COMPTE-1, HS2-05 (B-SEG-2).
- **Q-G1-7** : la coupe en trois sous-lots et les lignes datées du §1.
- **Q-G1-8** : F2P du test nommé (§6) : l'ERROR attendu sur la base est-il recevable comme « compté à part » ?
- **Q-G1-9** : l'avance rapide de la branche du worktree (§0) plutôt qu'un HEAD détaché.

## 12. Livrables (`F:/tmp/shogen-lots/B-SEG-1/`)
- `lot.diff` : diff complet du worktree (`git add -N` des deux fichiers neufs, puis `git diff HEAD`), lot entier contre `0abc881`, ce journal compris.
- `bseg-1a.diff`, `bseg-1a-nomme.diff`, `bseg-1b.diff` : sous-lots, diffs unifiés de `oracles/mkdiff.py`. Rejeu `patch -p1` sur une copie de la base : `oracles/check_apply.sh`, sortie `oracles/check-apply.out`.
- `G1-rapport.md` : copie de ce journal.
- `oracles/` : scripts (`run_suite.sh`, `table_horodatages_base.py`, `valide_collect_n0.py`, `valide_test_nomme_fixture.py`, `mutants.py`, `f2p_1a.sh`, `f2p_1b.sh`, `p2p_rendus.py`, `p2p.sh`, `p2p_compare.py`, `diff_rendus.py`, `mkdiff.py`, `sans_test_nomme.py`, `longueurs.py`, `grep_c_b0_10_iv.py`, `empreintes.py`, `cargo_env.sh`, `xtask.sh`, `suites_finales.sh`, `reperage_sha_lignes.py`, `check_apply.sh`, `oracle_record.py`), leurs sorties, l'estimation R-25 et les empreintes par état. Empreintes des livrables et chemin de l'enregistrement d'oracle `shogen.oracle-record.v1` (rôle G1, aucun run avec la variable) : `oracles/LIVRABLES.sha256`.
- **C-B0-10 (iv)** : dans les lignes ajoutées des trois diffs (111, 51, 198), aucune occurrence hors du test nommé des 12 `flux_id`, des 11 hôtes de `sources.SPECS` ni des 37 bornes, comptes et dates d'ADR-0024, ADR-0025 et ADR-0028 ; 14 occurrences dans le test nommé, admis (`oracles/grep-c-b0-10-iv.out`).
- **Longueur de ligne** : aucune ligne ajoutée au-delà de 110 colonnes (usage mesuré du dépôt : au plus 111 ; `oracles/longueurs.py`).

## 13. Attestation (forme d'ADR-0028 D.3)
- **Pièces lues** :
  - ADR-0028 en entier et ses annexes A, B, C, D (l'annexe E n'a pas été ouverte) ; ADR-0025 l.1-13 et l.15-45 ; `docs/G1-lot-B0-pool-analyse.md` et `docs/G1-lot-adr0025-filtre.md` en entier ; `JOURNAL.md` par recherche de motifs (ratifications, lots) ;
  - code de `s2-harness/shogen_s2` : `records`, `report`, `r1`, `collector`, `window` en entier ; `lm` l.180-240 ; `r2` l.336-405, l.770-919 et l.1030-1106 ;
  - tests : `test_exclusion`, `test_pool_analyse`, `test_g2_adversarial` et `tests/__init__.py` en entier ; `test_collector` l.1-120 ;
  - `xtask/src` : en-têtes et listes de `sg4.rs`, `sg5.rs` (l.1-80) et `sg8.rs` ; `rust-toolchain.toml` ; `docs/09-vocabulaire.md` par recherche de motifs ; `s2-harness/README.md` l.1-40 ; `CLAUDE.md` du dépôt ;
  - scripts d'oracle du G1 B0 (`p2p_rendus.py`, `p2p.sh`, `cargo_env.sh`, `check_apply.sh`, `grep_c_b0_10_iv.py`, `oracle_record.py`), les lignes de verdict de son `xtask-lot.out` et l'en-tête de son `b0-2.diff`.
- **Exposé à** :
  - les comptes et bornes que portent la mission, ADR-0028 et ses annexes (D5 : 5 313 dont 815 `resolve_failed`, 483 ; diagnostics `resolve_failed` dans et hors plage, D5 l.58 ; D.1 n° 8) ;
  - des comptes de fenêtres, de doublons et des heures par strate (ADR-0025 l.10-13 et amendement ; D4 et D2 pt 6 d'ADR-0028 ; journaux G1 du lot A et de B0 ; D.1 n° 9) ; les comptes de Pyth (D1 ; D.1 n° 7).
- **Non ouverts** : les pièces D.2 n° 1 à 9, toutes ; aucune copie scellée ; les lignes D.2 n° 5 et 6 ont été repérées par leur sha256, jamais affichées.
- **Balayage mécanique** : `cargo xtask verify` (S-G4, S-G5) lit tout `docs/`, y compris les fichiers des pièces D.2 n° 5 et 6 ; seules les lignes de verdict ont été affichées (`oracles/xtask.sh`).
- **Aucune statistique S2 calculée sur les journaux de campagne. Aucun z, aucun K, aucun P̂_more ni aucun φ de campagne vu.** Les z, K et P̂_more des tests et des sorties d'oracle portent sur les fixtures synthétiques du collecteur scripté.

## 14. Corrections de la revue G2 (ajout daté du 2026-09-30 ; l.1-200 inchangées)
- **Générateur** : `claude-opus-5-5` (identifiant exact déclaré par le harnais en tête de session, R-1), effort max selon la commande de lancement (non observable depuis l'agent), contexte frais ; générateur G1 de correction, instance distincte du réviseur G2. Mandat : commande de mission de l'orchestrateur Shōgen (`claude-fable-5-1`, 2026-09-30). Aucun commit, aucun workflow (R-20) ; aucune variable `GIT_DIR` ni `GIT_WORK_TREE` posée, aucun `--write-tree` ; `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée.
- **Horloge** (`date -u`) : corrections appliquées au worktree à 2026-09-30T02:20:29Z ; oracles de 02:22:52Z à 02:38:14Z ; cette section écrite ensuite ; suite, `cargo --locked xtask verify` et enregistrement d'oracle rejoués après elle, sur la copie finale qui la contient (heures au rapport de correction).
- **Revue appliquée** : `F:/tmp/shogen-lots/B-SEG-1/G2-rapport.md` (sha256 `cc8f2b50dd33df44b70af460104ab796c0398e948fab25e8e6ea1c33fe1e9c5c`), verdict ACCEPTE-AVEC-CORRECTIONS, liste fermée C-1 à C-6.
- **C-1, C-2, C-3** (tests seuls, sous-lot B-SEG-1c ; aucune ligne de `shogen_s2/`, dont les cinq modules gardent leur sha) : texte du réviseur, `g2-oracles/corrections-G2-bseg-1c.diff` (sha256 `ea46f11c8be8a34f59fb1fab02a305ddbd5da5b90ef40ec23ca4978a5a5521cb`), appliqué tel quel par `patch -p1`, sans décalage ni fuzz. Provenance : 51 lignes rédigées par le réviseur G2 (`claude-opus-5-5`), appliquées sans retouche ; `tests/test_exclusion.py` et `tests/test_segment.py` sont identiques à l'octet à ceux de l'arbre `g2-fix` du réviseur (`cmp`).
  - C-1 : `test_v_window_start_bornes_a_une_seconde`. La mention « borne ±1 » des §4 et §8 couvre désormais aussi la branche `window_start` (O-5 de la revue).
  - C-2 : `fixture_w120` (collecteur réel à w = 120 s) et `TestSegmentW120` : w lu de `run_params` par l'exclusion et par le n fixe.
  - C-3 : `test_d5_deux_plages_sur_ts_et_harness_ts` : union de deux plages sur `ts` et `harness_ts`.
- **Coupe, mesurée** (`git apply --numstat`, hors dépôt) : B-SEG-1a 111, B-SEG-1b 198, **B-SEG-1c 51** (dont 15 lignes de fixture, `fixture_w120` et sa grille, comptées), B-SEG-1a-N 51. Empilés dans l'ordre de C-6 (1a, 1b, 1c, puis 1a-N) sur des copies de `0abc881` : 195, 202, 205 puis 206 tests, tous OK. 1a-N s'applique après 1c avec un décalage de 15 lignes, sans fuzz ; le test nommé passe de `tests/test_exclusion.py` l.245-265 à l.260-280.
- **Oracles** : suite 206 tests OK (2 sauts, variable absente), 0 entrée TMP, 0 `__pycache__`, sur le worktree et sur les copies ; MG01, MG15, MG36, MG57 et MG58 de la revue survivent à la suite livrée et sont tués sur l'arbre corrigé comme sur 1a + 1b + 1c, chacun par le seul test prévu ; campagne complète de la revue sur l'arbre corrigé : 58 mutants tués sur 58, témoin vert ; épingles inchangées.
- **C-4, C-5, C-6** : actes de l'orchestrateur, aucun n'est exécuté ici. C-4 est consignée par l'orchestrateur au commit `3a17edf` (tests de la liste fermée rejoués à `fb089dc` : 0 occurrence de « à ratifier » à l'annexe D l.108, 1 ligne de ratification de D.4 a au JOURNAL). C-5 et C-6 : état mesuré à `fb089dc`, propositions (lignes datées de l'annexe A, item SHOGEN-SEG-DEMARRAGE-1, plan de commits) et diff séparé hors dépôt : `F:/tmp/shogen-lots/B-SEG-1/correction-rapport.md`. Aucun texte de ratification n'est proposé.
- **Observation** : la classe `TestSegmentW120` est suivie d'une seule ligne vide avant `if __name__` (PEP 8 en demande deux) ; texte exact de la liste fermée, conservé.
- **Attestation** (forme D.3) : pièces D.2 n° 1 à 9 non ouvertes ; aucune copie scellée ; `tests/test_exclusion.py` affiché l.1-186 seulement, test nommé non affiché. Exposé aux bornes et comptes que portent la revue G2, le cp-1 bref et la liste de constantes du script C-B0-10 (iv) du G1 (D.1 n° 8 et 9) ; aucun n'est reproduit ici. Aucune statistique S2 calculée sur les journaux de campagne. Aucun z, aucun K, aucun P̂_more ni aucun φ de campagne vu.
