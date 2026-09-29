# G1 — lot B0 d'ADR-0028 (règle du pool d'analyse, D1 ; SHOGEN-TESTS-TMP-1), Shōgen S2 — journal

- **Modèle** : `claude-opus-5-5` (déclaré par le harnais), effort max, contexte frais ; worker G1 (R-1 déclaré en tête de session). Aucun commit, aucun workflow déclenché (R-20). Aucune variable `GIT_DIR` ni `GIT_WORK_TREE` posée, aucun `--write-tree`. Écritures git limitées au worktree du lot : `git switch --detach ce2f107` (§0), puis `git add -N .` pour produire le diff prescrit.
- **Horloge** (`date -u`) : début 2026-09-29T20:20:24Z ; table ok(f, s) des fixtures existantes 20:31Z-20:34Z ; estimation R-25 écrite 20:59:48Z, avant tout code ; première mesure R-25 21:06Z (252 lignes, donc coupe) ; B0-1 figé 21:17Z, mutants B0-1 21:19Z ; B0-2 figé 21:31Z, mutants B0-2 21:35Z-21:40Z ; `cargo xtask verify` final 21:46Z ; suites finales 21:47Z ; journal final 21:50Z.
- **Mandat** : commande de mission de l'orchestrateur Shōgen (`claude-fable-5-1`, 2026-09-29), lot B0 de l'annexe A (l.14), avec les corrections C-B0-1 à C-B0-11 du cp-1 bref. Cadre : ADR-0028 et annexes A-E au commit `ce2f107`.
- **Classification** : bounded. Le chemin existe déjà (lecteur `records` → `r1`/`lm`/`r2` → `report`) ; le lot insère une règle entre le filtre d'exclusion du lot A et les calculs.
- **Résultat** : lot coupé en deux sous-lots au G1 (C-B0-7), **B0-1** (D1 cas a et c ; TESTS-TMP-1 ; erratum ADR-0023) et **B0-2** (D1 cas b), chacun sous le seuil de 200 lignes. Suite verte, TMP neuf à 0 entrée, 20 + 19 mutants tués, F2P par assertion, rendus sans flux mort identiques à l'octet, `cargo --locked xtask verify` VERT sur l'arbre final.

## 0. Préconditions mesurées avant code (le §0 du format du lot A est rayé, C-B0-8 i : aucune lecture de copie scellée)

- **Base du G1 (C-B0-10 i)** : `ce2f107` (`main`). Le worktree fourni par le harnais était sur la branche `worktree-wf_a90c2c74-1cd-5` à `fa0ce5b`, 30 commits en arrière de `ce2f107`, sans `docs/adr-0028/` (mesuré : `git merge-base --is-ancestor fa0ce5b ce2f107` vrai, `git rev-list --count fa0ce5b..ce2f107` = 30). Acte du worker : `git switch --detach ce2f107` dans ce seul worktree (HEAD privé du worktree ; aucune référence partagée déplacée ; la branche du worktree reste à `fa0ce5b` ; le dépôt principal n'est pas touché). Le worktree voisin `wf_a90c2c74-1cd-4` est lui aussi à `fa0ce5b` (`git worktree list`) : le lot CI-S2 a probablement la même base fausse.
- **Ordre CI-S2 puis B0 (C-B0-10 i)** : fichiers disjoints, mesuré sur les diffs de ce lot (aucun fichier de `.github/`). L'orchestrateur déclare l'inversion ou le parallélisme.
- **C-B0-1 non satisfaite au lancement** : à `ce2f107`, la ligne E-D1b (annexe E, l.14) et D.4 a (annexe D, l.108) portent encore « à ratifier » ; `JOURNAL.md` ne porte aucune ratification du cas (b) de D1 ni de l'option (b) de C-11 (une seule occurrence de « RATIFI », qui porte sur la borne 15:08Z). Ces ratifications sont des actes de l'orchestrateur : ce G1 ne les écrit pas. Il met en œuvre le cas (b) comme la mission l'ordonne, mais dans un sous-lot séparé (B0-2, §1). **B0-2 n'est consommable au G2 et au G7 qu'après le commit de consignation.**
- **Variable `SHOGEN_S2_CAMPAGNE_CONTROL` (C-B0-8 ii)** : non posée pendant tout le G1 (mission : fixtures seulement ; ratification C-11 absente). Le test (ii) de `test_exclusion` lève donc `SkipTest` : c'est le « skipped=1 » de chaque exécution.
- **Suite de base** (arbre `ce2f107`, TMP neuf, variable non posée) : `Ran 188 tests … OK (skipped=1)`, **71 entrées** laissées dans le TMP neuf : la mesure du validateur (C-B0-6), reproduite.
- **Table ok(f, s) des fixtures existantes (C-B0-4, FM-3.3)**, mesurée sur l'arbre de base. Les quatre points d'entrée et la CLI en sous-processus ont été instrumentés, et le comptage réimplémenté hors du code du lot (`oracles/table_ok_fixtures.py`). Résultat : 188 tests, 0 échec sous instrumentation, **124 appels** issus de **44 tests**. **Aucune fixture existante n'a de flux mort** : 0 couple (flux, strate retenue) avec ok = 0, et les prédicats étroit et large ne diffèrent sur aucune fixture. `test_report` l.151 met deux flux en panne dans une seule fenêtre sur trois : ok = 2, aucun retrait. Un appel existant (`test_g2_adversarial.test_plages_chevauchantes_et_emboitees`) porte un segment **sans aucune fenêtre retenue** : la règle ne doit rien y retirer (§3 vii). Aucun doré n'est à re-capturer.

## 1. Coupe R-25 (C-B0-7)

- **Estimation ascendante écrite avant le code** (20:59:48Z) : code ≈ 63, tests ≈ 125, TESTS-TMP-1 ≈ 5, soit ≈ 193.
- **Première mesure** (lot entier, 21:06Z) : modules +81, `tests/__init__.py` +8, fichier de tests neuf 163, soit **252 > 200**. L'estimation était fausse (tests sous-estimés de 38 lignes, code de 18 ; E-3). Le lot est donc **coupé**.
- **Frontière de coupe** : elle suit la frontière de ratification de C-B0-1. Le cas (b), encore « à ratifier » au commit de base, forme son propre sous-lot. B0-1 est complet et cohérent seul : un flux mort dans une seule strate y reste au pool, ce qui est le comportement d'avant le lot. B0-2 doit précéder RENDU.
- **Mesures** (méthode du lot A : `git diff --numstat` des fichiers suivis, `wc -l` des fichiers neufs ; pour B0-2, lignes `+` du diff contre l'arbre B0-1 figé) :

| sous-lot | modules `shogen_s2` | `tests/__init__.py` | `tests/test_pool_analyse.py` | total ajouté | seuil |
|---|---|---|---|---|---|
| B0-1 | +43 −7 (r1 +23, lm +2, r2 +2, report +16) | +8 | 138 (neuf) | **189** | ≤ 200 |
| B0-2 | +43 −31 (r1 +12, lm +10, r2 +7, report +14) | 0 | +35 | **78** | ≤ 200 |

  Documentation hors compte (précédent du lot A) : ADR-0023 +5 lignes ; ce journal.
- **Lignes datées proposées pour l'annexe A** (amendement daté : acte de l'orchestrateur, non écrit ici) :
  - **B0-1** (2026-09-29, coupe R-25 du G1 de B0) : D1 cas (a) et (c) aux quatre points d'entrée ; bloc 1 (retraits nommés avec leurs comptes, k nominal par strate) ; SHOGEN-TESTS-TMP-1 ; erratum ADR-0023 (C-B0-9). Véhicule : `s2-harness/shogen_s2/{r1,lm,r2,report}.py`, `tests/__init__.py`, `tests/test_pool_analyse.py`, `docs/adr-0023/ADR-0023.md`. Oracle : suite unittest ; fixture à source morte dans toutes les strates ; strate vidée par l'exclusion ; épingle ; 20 mutants. Taille 189 [mesuré]. Tuyau : journaux → pool d'analyse → R1/L&M/R2 → blocs 1-6, consommateur RENDU. cp-1 bref.
  - **B0-2** (2026-09-29, coupe R-25 du G1 de B0) : D1 cas (b), c'est-à-dire pool par strate pour R1 et L&M, R2 au seul cas (a), k nominal et N par strate, drapeau 2 sur le z du bloc 3 ; consommable après consignation de la ratification (C-B0-1). Véhicule : mêmes modules, `tests/test_pool_analyse.py`. Oracle : fixture à source morte dans une seule strate (re-collecte last-wins, ok à prix nul, lecture orpheline, z publié, un AS par hôte) ; 19 mutants. Taille 78 [mesuré]. Même tuyau. cp-1 bref.

## 2. Changements (worktree du lot, sur `ce2f107`)

| fichier | B0-1 | B0-2 | sha256 base → B0-1 → B0-2 |
|---|---|---|---|
| `shogen_s2/r1.py` | `analysis_pools(markers, readings, pool)` : règle D1 sur les fenêtres retenues ; point d'entrée : pool du segment | `compute_r1(…, pool_by_strate=None)` ; point d'entrée : pools par strate | 3d8931f7… → 3e51a102… → 1e6a115c… |
| `shogen_s2/lm.py` | point d'entrée : pool du segment | `compute_lm(…, pool_by_strate=None)`, N = taille du pool de la strate | d21f8d08… → ff779947… → f91937a0… |
| `shogen_s2/r2.py` | point d'entrée : pool du segment | `compute_r2(…, pool_by_strate=None)` : R2 sur le cas (a) seul ; R1 et L&M internes du drapeau 2 par strate | 1acf2ba3… → 5e3b5d87… → d76170de… |
| `shogen_s2/report.py` | règle après l'exclusion ; blocs 3-6 sur le pool d'analyse ; bloc 1 : une ligne par retrait (flux, strate, ok, lectures, n, cas) et k nominal par strate, seulement s'il y a retrait ; bloc 3 : pool de la strate | pools par strate aux trois calculs ; lignes de cas (b) ; bloc 4 : N par strate, seulement en cas (b) | 74d0408b… → a6b7d5a5… → de5ac3c7… |
| `tests/__init__.py` | SHOGEN-TESTS-TMP-1 (§3 viii) | — | e3b0c442… (vide) → 3237899d… |
| `tests/test_pool_analyse.py` | neuf : 3 tests | + test (b) | — → e5a63de7… → c9498dda… |
| `docs/adr-0023/ADR-0023.md` | erratum et statut en tête (C-B0-9) | — | 981ec407… → ca9dc5d4… |

- **Intouchés** (sha = base, mesuré sur les 22 autres `.py` de `s2-harness`) : les modules de quarantaine `collector`, `sources`, `run_campaign`, `closure`, `smoke`, `journal`, `model` (D6 i), ainsi que `records`, `window` et tous les tests existants.
- **Ligne de bloc 1 rendue** (fixture du test b) : `pool_analyse_retrait     = <flux> strate « stress » : ok = 0 / 60 lectures, n = 60 — hors R1 et L&M de la strate, cas (b), gardé par R2 (ADR-0028 D1)`, suivie de `k_nominal_strate         = « calme » : 3 sources / 3 flux (pool d'analyse, ADR-0028 D1)` et de la ligne analogue pour « stress » (2 sources / 2 flux).
- **C-B0-10 (iv)** : dans les lignes ajoutées de `shogen_s2/` et `tests/`, aucun nom de flux et aucune constante de campagne. Le flux mort est `SKELETON[0]` et les hôtes n'apparaissent pas. La recherche porte sur les 12 `flux_id` de `sources.SPECS`, sur les bornes et comptes d'ADR-0025 et d'ADR-0028, et sur les dates de campagne, dans les lignes `+` des deux diffs (189 et 78 lignes) : 0 occurrence (`oracles/grep_c_b0_10_iv.py`, `oracles/grep-c-b0-10-iv.out`). La cause de la perte de Pyth (Hermes gaté par clé) reste un texte de documentation (C-B0-10 v).
- **C-B0-10 (iii)** : aucune dépendance neuve (bibliothèque standard seulement : `collections.Counter`, `itertools.count`, `atexit`, `shutil`).

## 3. Définitions appliquées (C-B0-2) — ce que la mission fixe, ce qu'elle laisse ouvert

- **(ii), (iii), (iv) et (v) : appliquées telles que fixées.** Les strates de S sont celles qui ont au moins une fenêtre retenue. ok(f, s) se compte sur les lectures last-wins jointes aux fenêtres retenues, après la garde §5.3 et après `exclude_window_start_ranges`, orphelines exclues. La règle est placée juste après le point d'exclusion, aux quatre points d'entrée. Le bloc 1 porte ok(f, s), les lectures de f dans s et n de s. Le k nominal par strate vaut `(len(r2.hosts_of_pool(flux_hosts, pool_s)), len(pool_s))` ; le k nominal R2 du bloc 6 n'applique que le cas (a).
- **(i) Prédicat ok — non tranché dans la mission ; appliqué : statut `ok` ET prix présent** (le prédicat de réponse de `r1.classify_ecart` et de `r1._classify_window`). Dérivation tirée de la mission elle-même :
  - C-B0-5 exige de tuer un mutant « prédicat ok élargi » et C-B0-11 une fixture « ok à prix nul » : les deux supposent le prédicat étroit ;
  - le motif de D1 (un flux sans lecture est en écart dans chaque fenêtre, SUP-01) donne l'équivalence exacte ok(f, s) = 0 ⇔ f en panne (iii) dans chaque fenêtre retenue de s. Sous le prédicat large, un flux « ok sans prix » partout serait gardé alors qu'il est en écart partout.
  - Q-G1-1 : ratification par l'orchestrateur. Le prédicat large coûterait une ligne (`r1.py`, `analysis_pools`).
- **(vi) Pool parcouru par les blocs de rendu.**
  - C-B0-2 (vi) nomme `report.py:178` « bloc 2 » ; à `ce2f107`, cette ligne est dans le **bloc 3** (E-5).
  - Bloc 3 : pool d'analyse de la strate (`for f in blk["per_source"]`). C'est forcé : sans cela, un flux retiré lève `KeyError`.
  - Bloc 2 (journal brut, `classify_cells` de l.96) : **pool de `run_params`**, code inchangé. Motifs : c'est le journal brut (ADR-0005, sha de chaque lecture), et un flux mort dans une strate n'y répond jamais, donc la classification des autres flux y est identique avec ou sans lui.
  - Q-G1-2 : ratification. L'autre choix coûte une ligne.
- **(vii) S sans strate** (toutes les fenêtres exclues) : **aucun retrait**. Choix du G1, conservateur : la base se comporte ainsi, un test existant atteint ce cas et le mutant M18 le fixe. Q-G1-4.
- **(viii) SHOGEN-TESTS-TMP-1, forme centrale — écart déclaré à la forme par site que suggèrent C-B0-6 et C-B0-7** (18 sites dans 7 fichiers). `tests/__init__.py` range tout `mkdtemp` de la suite sous un dossier unique, retiré à la fin du processus (`tempfile.tempdir` + `atexit`).
  - Motifs : contre-mesure système préférée à une consigne (annexe C) ; les tests futurs sont couverts sans discipline par site ; les tests de quarantaine ne sont pas touchés du tout.
  - Critère falsifiable tenu : **0 entrée** dans un TMP neuf après la suite complète (71 sur la base).
  - Mutants redéfinis : M19 retire le nettoyage (1 entrée laissée) ; M20 retire la redirection (74 entrées).
  - Coût de la forme par site : environ 25 lignes, qui auraient porté B0-1 à environ 206. Q-G1-5.
- **(ix)** Les lignes de bloc 1 et la note de N par strate du bloc 4 n'apparaissent que s'il y a retrait (respectivement cas b) : le rendu sans flux mort garde ses octets (§4).
- **(x)** Sorties API : aucune clé neuve ; le pool d'analyse se lit dans `pool` (pool du segment) et, par strate, dans `per_source` (R1) et `N` (L&M).

## 4. Tests (bibliothèque standard, forme de `tests/`) — chaque test nomme la mutation qui le rougit

- **Fixtures (C-B0-3)** : produites par le collecteur réel (`collector.collect`, `journal.append_jsonl`), horloge scriptée, calendrier week-end. La source morte est scriptée en échec (`Reading` à statut `panne_http`, HTTP 401 ; ou statut `ok` sans prix). Aucun JSONL écrit à la main. Le flux mort est `SKELETON[0]`, pris par indice. `fixture_b` (w0-w2 calme, w3-w62 stress) :
  - le flux mort est vivant en calme ; en stress, aucune de ses lectures n'est ok une fois retenue : w3 ok puis re-collectée en panne (last-wins), w4 ok à prix nul, w5-w62 panne ;
  - w63 porte une lecture ok orpheline (harnais coupé avant le marqueur) ;
  - les deux autres flux tombent ensemble aux fenêtres stress impaires, si bien que z est publié en stress : n·P̂_more·(1−P̂_more) = 11,25 ≥ 10 ;
  - pour le test (b), un AS distinct par hôte est produit par `r2.collect_asn`, résolveur simulé, sans nom d'hôte.
- **Attendus métamorphiques (C-B0-4)** : chaque attendu vient du code d'avant le lot, `compute_r1`, `compute_lm`, `compute_r2` et `drapeau_2` aux signatures inchangées, appliqué à P privé du flux mort (par strate au cas b). Aucun attendu n'est lu dans une sortie du code neuf. Les comptes du bloc 1 (0 / 3 et n = 3, 0 / 60 et n = 60) viennent du script de la fixture ; le k nominal attendu vient de `r2.hosts_of_pool` appliqué aux `SPECS`.
- **(a)** `test_a_flux_mort_partout_hors_r1_lm_r2_aux_quatre_points` : les trois `recompute_*` égalent le code de base sur P privé du flux. Les blocs 3 à 6 du rendu sont identiques, à l'octet, à ceux de la même collecte faite **sans** le flux. Le bloc 1 porte deux retraits (un par strate), comptés, et k nominal par strate. La CLI tourne dans un processus neuf. Rougit si : règle désactivée ou omise à un point d'entrée ; N de L&M laissé à la taille du pool configuré ; retrait absent, en trop ou mal compté ; k nominal absent.
- **(exclusion)** `test_regle_apres_exclusion_strate_videe_hors_de_s` : [w0 ; w2] vide la strate calme, S = {stress}, le flux mort y est retiré au cas (a), et rien n'apparaît pour la strate vide. Rougit si : règle placée avant l'exclusion ; strate vide comptée dans S ; prédicat élargi ; last-wins ignoré ; orphelines comptées.
- **(épingle, CA-13 bis)** `test_epingle_sans_flux_mort_octets_de_base_avec_option` : sans flux mort, le rendu **avec** l'option d'exclusion a le sha capturé sur l'arbre de base (`a4dd4c00…7520`, deux captures identiques par `oracles/capture_epingle_base.py`, qui confirment aussi le sha sans option du lot A, `a4ffc3e5…49a5`). La CLI émet ces octets. Avec S vide, R2 égale le code de base sur P. P2P par construction.
- **(b, sous-lot B0-2)** `test_b_mort_en_stress_seul_retire_de_cette_strate_seulement` : R1 et L&M par strate égalent le code de base (P en calme, P privé du flux en stress). R2, drapeau 2 excepté, égale le code de base sur P entier : le flux reste dans R2. Le drapeau 2 égale `drapeau_2` appliqué aux R1 et L&M de base par strate et à la partition de base (état « levé », localisation comprise). Le bloc 1 porte un seul retrait (cas b) et le k nominal des deux strates ; le bloc 4, N = 2 en stress ; la CLI émet les mêmes octets.
- **F2P (C-B0-8 vi)**, chaque test neuf lancé sur l'arbre parent copié (`oracles/f2p-*.out`) :

| test | sur `ce2f107` | sur B0-1 (parent de B0-2) |
|---|---|---|
| (a) | FAIL (AssertionError) | — (test de B0-1) |
| (exclusion) | FAIL (AssertionError) | — |
| (b) | FAIL (AssertionError) | FAIL (AssertionError) |
| épingle | passe (P2P, déclaré) | passe |

- **Exécutions** (TMP neuf, variable non posée, `PYTHONDONTWRITEBYTECODE=1`, `oracles/suite-*.out`) : base, 188 tests, OK (skipped=1), 71 entrées ; B0-1, 191 tests, OK (skipped=1), 0 entrée ; B0-2, 192 tests, OK (skipped=1), 0 entrée.
- **Rendus sans flux mort identiques à l'octet (C-B0-4), au-delà de l'épingle** : `oracles/p2p_rendus.py` hache chaque sortie de `render_report` et chaque stdout de la CLI de la suite existante, soit 46 sorties (38 API, 8 CLI). Base contre B0-1 et base contre B0-2 : **0 différence** après masquage d'un seul champ, l'heure murale ISO à microsecondes de la table ASN de `test_run_campaign.RunSegmentCase` (`collect_asn` y prend l'horloge réelle). Ce champ diffère aussi entre deux exécutions de la base, en 2 sorties (E-7).

## 5. Mutants (sur copies sous `F:\tmp\shogen-lots\B0\work\`, suite complète, TMP neuf) — `oracles/mutants.py`, `oracles/mutants_b0_2.py`

**B0-1 (arbre B0-1 figé) : 20 mutants, 20 tués** (`oracles/mutants-b0-1.out`).

| # | mutant | rougi par |
|---|---|---|
| M01 | règle désactivée | (a), exclusion |
| M02-M05 | règle omise à un point d'entrée : r1, lm, r2, rendu | (a), exclusion |
| M06 | N de L&M laissé à la taille du pool configuré (bloc 4) | (a) |
| M07 | règle placée avant l'exclusion (quatre points) | exclusion |
| M08 | lectures orphelines comptées (strate prise au calendrier) | exclusion |
| M09 | prédicat ok élargi (statut seul) | exclusion |
| M10 | last-wins ignoré | exclusion |
| M11 | retrait absent du bloc 1 | (a), exclusion |
| M12 | lectures mal comptées (toutes strates) | (a) |
| M13 | n mal compté (tous les marqueurs) | (a), exclusion |
| M14 | ligne de retrait sans retrait | `test_exclusion` (iv), épingle |
| M15 | k nominal par strate sans retrait | `test_exclusion` (iv), épingle |
| M16 | k nominal par strate absent | (a), exclusion |
| M17 | strate sans fenêtre retenue comptée dans S | épingle, exclusion |
| M18 | S vide lu comme « tout est mort » | épingle |
| M19 | nettoyage `mkdtemp` retiré (`atexit`) | critère TMP : 1 entrée laissée |
| M20 | nettoyage `mkdtemp` retiré (redirection) | critère TMP : 74 entrées laissées |

**B0-2 (arbre combiné figé) : 19 mutants, 19 tués** (`oracles/mutants-b0-2.out`). Tous les N sont rougis par (b) ; N04, N15 et N16 le sont aussi par (a), et N17 à N19 par `test_exclusion` (iv) et l'épingle.
- N01 : cas (b) traité comme (a).
- N02 : cas (b) appliqué à R2.
- N03 : k nominal par strate pris sur le pool du segment.
- N04 : k nominal par strate absent.
- N05 : N de L&M laissé à la taille du pool en cas (b).
- N06 : R1 interne du drapeau 2 sans pools par strate.
- N07 : L&M interne du drapeau 2 sans pools par strate. Ce mutant a survécu à la première campagne : sans ASN, le drapeau 2 ne localise pas. Il est tué une fois l'AS par hôte ajouté au test (b).
- N08 à N11 : pools par strate omis au point d'entrée r1, lm, r2, ou aux trois appels du rendu.
- N12 et N13 : `compute_r1` ou `compute_lm` ignore `pool_by_strate`.
- N14 : N par strate absent du bloc 4.
- N15 : libellé de cas inversé.
- N16 à N18 : retrait absent ; ligne de retrait sans retrait ; k nominal sans retrait (les équivalents de M11, M14 et M15 sur le code combiné).
- N19 : en-tête du bloc 4 annoté sans cas (b).

**Campagne B0-1 rejouée sur l'arbre combiné** : les 16 mutants applicables sont tués ; M11, M14, M15 et M16 ne s'appliquent plus (lignes réécrites par B0-2), et leurs équivalents sont N16, N17, N18 et N04. Après chaque mutant, la copie est jetée ; le worktree n'a jamais porté de mutant.
- **Mutant équivalent déclaré** : afficher n à la place du nombre de lectures. Sur tout journal produit par le collecteur, le marqueur est écrit après les lectures de la fenêtre (`collector.py` l.244-249) : une fenêtre retenue porte donc une lecture de chaque flux du pool, et les deux comptes sont égaux. Ils ne diffèrent que sur un journal qui viole ce contrat.

## 6. (rayé, C-B0-8 i : aucune mesure sur `control.jsonl`)

## 7. Tuyaux CA-11 (règle Branchement)
- **Entrée** : `control.jsonl` et `journal.jsonl` produits par le collecteur (ici, fixtures du collecteur réel).
- **Lecteur** : `parse_control` → `effective_run_params` → `verify_markers_against_spec` → `exclude_window_start_ranges` (lot A) → `r1.analysis_pools` (règle D1, ce lot) → `compute_r1`, `compute_lm`, `compute_r2` ; `render_report` en fait autant, puis imprime les retraits au bloc 1. Les quatre points d'entrée appellent la même fonction.
- **Chemin servi** : la CLI `python -m shogen_s2.report` (RUNBOOK §9 e), rejouée dans un processus neuf par (a), (b) et l'épingle.
- **Sortie aval** : le lot RENDU. Il n'est pas branché : item formé, déclencheur **G0 de RENDU-1** (C-B0-3).
- **État** : aucun état persistant ; les retraits sont recalculés depuis le journal à chaque appel et consignés dans la sortie.

## 8. Risques MAST nommés (C-B0-11, CA-5) et contre-mesures
- **FM-1.1** (pièces D.2) : liste fermée recopiée de la mission ; aucune pièce de D.2 ouverte ; aucun de leurs chemins tapé dans une entrée d'outil (renvois par numéro) ; variable non posée ; recherche a posteriori par l'orchestrateur (C-B0-8 v).
- **FM-3.3** (doré re-capturé, attendus tirés du code neuf) : aucun doré existant touché (§0 : 0 fixture à flux mort) ; épingle capturée sur l'arbre de base ; attendus métamorphiques uniquement ; P2P octet sur les 46 sorties de la suite.
- **FM-2.3** (ni segment, ni strate poolée, ni rc 2 dans B0) : aucun segment J14/J28, aucune strate poolée, aucun code de retour neuf. Le seul hors-champ est l'erratum d'ADR-0023, désigné par D1.
- **FM-3.2** (fixtures sans « ok à prix nul » ni strate vide) : les deux cas sont présents (w4 ; calme vidée par l'exclusion ; S vide), avec en plus la re-collecte last-wins et la lecture orpheline.

## 9. `error_origin` proposés (à assigner au G7)
- **E-1** : worktree créé à `fa0ce5b` au lieu de `ce2f107`. Origine : harnais du workflow.
- **E-2** : incident rustup (§13). Origine : worker.
- **E-3** : estimation R-25 à ≈ 193, mesure à 252. Origine : worker (tests sous-estimés). Corrigé par la coupe, sans retrait d'assertion.
- **E-4** : `test_exclusion.cli()`, réutilisé par les tests neufs, lance `python` sans `-B`, si bien que la suite écrit `__pycache__` dans l'arbre testé. Origine : tests du lot A. Mitigé dans les oracles de ce G1 (`PYTHONDONTWRITEBYTECODE=1`) ; les dossiers écrits par les premières exécutions ont été retirés (fichiers ignorés par `.gitignore`).
- **E-5** : C-B0-2 (vi) désigne `report.py:178` comme « bloc 2 », alors que c'est le bloc 3. Origine : cp-1.
- **E-6** : `no_std` ROUGE dans `cargo xtask verify` sur la base, sous le home rustup de F: (cible absente à 20:52Z), puis VERT à 21:46Z une fois la cible installée par un tiers (§13). Origine : environnement.
- **E-7** : le rendu de `RunSegmentCase.test_end_to_end_table6_renders` n'est pas déterministe d'une exécution à l'autre (heure murale de `collect_asn`). Origine : test existant (quarantaine) ; constat seulement.

## 10. Review Focus
1. **Composition de devise du bloc 1** : elle est calculée sur les lectures (code inchangé) et compte donc un flux retiré s'il porte une devise. Elle décrit le journal, non le pool d'analyse.
2. **Fixtures à trois flux** : l'enveloppe (N ≥ 4 répondantes) n'y est jamais évaluable. L'argument « un flux mort ne change la classification d'aucun autre flux » tient par construction (il ne répond jamais), sans test à cinq flux.
3. **B0-1 seul** laisse au pool un flux mort dans une seule strate : état intermédiaire, B0-2 doit précéder RENDU.
4. **`analysis_pools` vit dans `r1.py`**, non dans `records.py` : `records` est importé par `r1`, et `build_window_strate`/`build_reading_map` vivent dans `r1`.
5. **Lectures ≠ n** : impossibles à produire par le collecteur réel (§5). Un journal réparé à la main (précédents REPAIR du RUNBOOK) pourrait les faire différer ; le bloc 1 l'afficherait.

## 11. Questions ouvertes Q-G1-n (pour l'orchestrateur)
- **Q-G1-1** : ratifier le prédicat ok étroit (§3 i).
- **Q-G1-2** : nommer le pool du bloc 2 : pool de `run_params` appliqué, pool d'analyse possible (§3 vi).
- **Q-G1-3** : k nominal par strate imprimé dès qu'il y a retrait, cas (a) compris (uniforme) ; D1 ne l'exige qu'au cas (b).
- **Q-G1-4** : S vide ⇒ aucun retrait (§3 vii).
- **Q-G1-5** : TESTS-TMP-1 sous forme centrale (§3 viii).
- **Q-G1-6** : coupe B0-1 / B0-2 et les deux lignes datées de l'annexe A (§1).
- **Q-G1-7** : consigner les ratifications de C-B0-1 (cas b de D1, option b de C-11) avant de consommer B0-2.
- **Q-G1-8** : base fausse du worktree voisin (CI-S2 probable, §0).
- **Q-G1-9** : l'erratum d'ADR-0023 couvre aussi la seconde mention de la même heure, dans « Méthode / sources vérifiées ». La conséquence 2 (J14/J28, D4) reste à l'orchestrateur (§8 d'ADR-0028, point 1).

## 12. Livrables (`F:\tmp\shogen-lots\B0\`)
- `lot.diff` : diff complet du worktree (`git add -N .` puis `git diff HEAD`), lot entier contre `ce2f107`. Pour le lot entier, les modules font +77 −29 (les lignes de B0-1 réécrites par B0-2 n'y comptent qu'une fois), `tests/__init__.py` +8 et le test neuf 173, soit 258 lignes : d'où la coupe.
- `b0-1.diff` (sha256 `57d8d1c8c15a51e5…`) et `b0-2.diff` (B0-2 sur B0-1, sha256 `b3b5fe79d922ea64…`). Base + `b0-1.diff` + `b0-2.diff`, et base + `lot.diff`, rejoués par `patch -p1` sur une copie de `ce2f107`, redonnent les arbres figés à l'identique (`oracles/check_apply.sh`).
- `G1-rapport.md` : ce journal, avec en tête les empreintes des livrables.
- `oracles/` :
  - scripts : `run_suite.sh`, `table_ok_fixtures.py`, `capture_epingle_base.py`, `f2p.sh`, `p2p_rendus.py`, `p2p.sh`, `mutants.py`, `mutants_b0_2.py`, `check_apply.sh`, `grep_c_b0_10_iv.py`, `rendu_fixture_b.py`, `cargo_env.sh`, `oracle_record.py` ;
  - leurs sorties ;
  - les sha des fichiers à chaque état (`base-`, `b0-1-`, `b0-2-sha256.txt`) ;
  - les sorties de `cargo xtask verify` (`xtask-base.out`, `xtask-lot.out`).
- Enregistrement d'oracle `shogen.oracle-record.v1` du G1 (C-B0-8 viii), sous `F:\tmp\oracle-results\shogen-ce2f107-G1-2026-09-29-<pid>.json`. Ses runs sont les trois suites finales (lot, B0-1, base), aucune lancée avec la variable, exit 0. xtask, mutants, F2P et P2P y sont cités hors runs, avec leur sha.

## 13. Incident déclaré — accès réseau par rustup (worker)
- **2026-09-29T20:34:28Z** : `cargo --version` lancé dans le worktree, avec `RUSTUP_HOME=F:/rust/rustup` et `CARGO_NET_OFFLINE=true`. `rust-toolchain.toml` déclare la cible `thumbv7em-none-eabi`, absente du home F: depuis son retrait par l'orchestrateur (ADR-0028 §4.12). rustup a alors synchronisé le canal 1.97.1 et commencé le téléchargement de `rust-std`, soit un **accès réseau**. `CARGO_NET_OFFLINE` ne gouverne pas rustup.
- **20:37:01Z** : processus `rustup.exe` tué. Résidu unique : `F:/rust/rustup/downloads/630f546a….partial` (3 897 872 o, sha256 `9eaf0ec76fed655b4cc364a946618da626f3b729ec027399b0c8edf57e87ba18`). **Acte du worker sur un état partagé : fichier supprimé à 20:51:37Z.** Aucune cible installée (`rustlib` ne liste que `x86_64-pc-windows-msvc` ; manifestes datés de 19:54Z, heure du retrait par l'orchestrateur).
- **Garde appliquée ensuite** (`oracles/cargo_env.sh`) : `RUSTUP_TOOLCHAIN=1.97.1-x86_64-pc-windows-msvc`, qui écarte le fichier toolchain ; `RUSTUP_AUTO_INSTALL=0` ; serveurs rustup vers `127.0.0.1:9` ; `CARGO_TARGET_DIR` sous `F:\tmp\shogen-lots\B0\target`. `downloads/` est resté vide ensuite.
- **Conséquence pour G3** :
  - Run sous garde sur la **base** (20:52:34Z-20:52:59Z, `oracles/xtask-base.out`) : S-G1 à S-G8, `fmt` et `clippy` VERT, `no_std` ROUGE (E0463, cible absente), verdict global ROUGE (exit 1).
  - Run sous garde sur l'**arbre final du lot** (21:46:07Z-21:46:17Z, `oracles/xtask-lot.out`) : **tout VERT, verdict global VERT (exit 0)**. La cible était alors présente dans le home F:.
- **Constat, sans acte de ce worker** : `thumbv7em-none-eabi` apparaît dans `F:/rust/rustup/toolchains/1.97.1-x86_64-pc-windows-msvc/lib/rustlib/` à **2026-09-29T20:59:18Z** (horodatage des fichiers). Entre 20:53Z et 21:46Z, ce worker n'a lancé aucune commande `cargo` ni `rustup` ; ses runs étaient sous la garde ci-dessus, et `downloads/` est resté vide. Un autre processus l'a donc installée, peut-être le lot CI-S2 du worktree voisin. À établir par l'orchestrateur : c'est un nouvel accès réseau sur l'état partagé, après le retrait de 19:54Z.
- **Item proposé** : SHOGEN-RUSTUP-HOME-F-1. Le fichier toolchain déclare une cible ; si elle manque au home F:, tout agent qui pointe `RUSTUP_HOME` vers F: sans garde déclenche un accès réseau. Décision attendue : garder la cible installée (état à constater) ou imposer la garde ci-dessus à tout lancement de `cargo`.

## 14. Attestation (C-B0-8 iv ; forme d'ADR-0028 D.3)
- **Pièces lues** :
  - ADR-0028 et annexes A-E (`ce2f107`) ; `docs/G1-lot-adr0025-filtre.md` ; `JOURNAL.md` l.84-98 ; ADR-0023 ;
  - le code de `s2-harness/shogen_s2` (`records`, `r1`, `lm`, `report`, `collector`, `journal`, `model` en entier ; `r2` l.183-235, l.341-400, l.777-1103) ;
  - les tests (`test_exclusion`, `test_report` en entier ; des extraits de `test_collector`, `test_r2`, `test_run_campaign`, `test_closure`, `test_g2_adversarial`) ;
  - `xtask/src` (`lib.rs`, en-têtes de `sg4.rs`, `sg5.rs`, `sg8.rs`) ; `rust-toolchain.toml`.
- **Exposé à** :
  - les comptes de Pyth (ADR-0023, D1 ; D.1 n° 7) ;
  - les diagnostics `resolve_failed` (D5 ; santé du harnais, D.1 n° 8) ;
  - des comptes de fenêtres et de doublons, et des heures par strate (lot A, JOURNAL, ADR-0028 ; D.1 n° 9).
- **Non ouverts** : les pièces D.2 n° 1 à 9, toutes ; aucune copie scellée.
- **Balayage mécanique** : `cargo xtask verify` (S-G4, S-G5) lit tout `docs/`, y compris les fichiers des pièces D.2 n° 5 et 6. Seules les lignes de verdict ont été affichées. Comptage sur les sorties : aucune ligne de ces deux pièces n'y est citée.
- **Aucune statistique S2 calculée sur les journaux de campagne. Aucun z, aucun K, aucun P̂_more ni aucun φ de campagne vu.** Les z, K et P̂_more des tests portent sur les fixtures synthétiques du collecteur scripté.

## 15. Corrections de la revue G2 (2026-09-29, ajout daté ; lignes précédentes inchangées)
- **Générateur** : `claude-opus-5-5` (R-1 déclaré en tête de session), effort max, contexte frais, worker G1 de correction, distinct du réviseur. Même worktree (`ce2f107`, HEAD détaché). Aucun commit, aucun workflow (R-20) ; aucun `GIT_DIR` ni `GIT_WORK_TREE`, aucun `--write-tree`. Première horloge relevée : 2026-09-29T22:52Z.
- **Mandat** : commande de mission de l'orchestrateur Shōgen (`claude-fable-5-1`) ; liste fermée C-1 à C-6 de la revue G2 (`F:\tmp\shogen-lots\B0\G2-rapport.md`, sha256 `1c2d2b32…d892`, verdict ACCEPTE-AVEC-CORRECTIONS).
- **C-1** (`report.py`, bloc 1) : la composition de devise ne compte que les flux du pool d'analyse, comme les paires de peg de R2 (D1 : 11 flux « dans tout texte »). Test : la panne scriptée de `collecte()` porte la devise, comme `sources.read` ; le test (a) exige la ligne `devise_composition` de la collecte faite sans le flux.
- **C-2** (`tests/__init__.py`) : `sys.dont_write_bytecode`, et `PYTHONDONTWRITEBYTECODE=1` hérité par les sous-processus de `cli()`. La suite n'écrit plus de `__pycache__` dans l'arbre testé (solde E-4).
- **C-3** (`tests/test_pool_analyse.py`) : `test_a_mort_hors_tete_et_hote_partage`. Le flux mort est en fin de pool ; les deux flux vifs partagent un hôte et sont choisis par hôte (C-B0-10 iv). Le test tue MG05 (retrait par position) et MG17 (sources comptées comme des flux), qui survivaient à la suite du G1.
- **C-4** (`lm.py`, docstring de module) : amendement daté de « N constant ». Au cas (b), N est la taille du pool d'analyse de la strate.
- **Écart au texte proposé par le réviseur** (`g2-oracles/corrections-G2-proposees.diff`) : un seul, la date de C-4 (« amendé le 2026-09-29 par … »), qu'exige « amendement daté ». Les trois autres fichiers corrigés sont identiques, à l'octet, à ceux de l'arbre `g2-fix2` du réviseur.
- **C-5 et C-6 : actes de l'orchestrateur, non exécutés ici.** C-5 (consignations CB-8, C-B0-1, C-B0-2 et prédicat ok retenu) est encore dû à `e99927b`. Pour C-6, les deux découpes sont mesurées, chaque sous-lot sous 200 lignes : B0-1 189, B0-2 78 et B0-3 24 ; ou B0-1 198 (avec C-1 et C-2) et B0-2 93 (avec C-3 et C-4).
- **Taille des corrections** : +24 −2 lignes de code et de tests ; ce journal est hors compte (précédent du lot A).
- **Oracles** (détail, chemins et sha au rapport de correction, `F:\tmp\shogen-lots\B0\correction-rapport.md`) :
  - suite : 193 tests OK (skipped = 1), 0 entrée TMP, 0 `__pycache__` ;
  - épingles inchangées ; P2P : 44 sorties sur 44 identiques ;
  - mutants : 59 tués sur 59 applicables (MG01-MG24, N01-N19, M01-M20 ; M11, M14, M15 et M16 inapplicables à l'arbre combiné, comme au §5) ;
  - C-B0-10 (iv) : 0 occurrence dans les lignes ajoutées ;
  - `cargo --locked xtask verify` : VERT sur l'arbre corrigé avant cette section ; le rejeu sur l'arbre final est au rapport de correction.
- **Livrables** : `lot.diff` régénéré contre `ce2f107` ; la version du G1 est conservée sous `lot-G1-c8fdf403.diff`, objet de la revue G2.
- **Tuyaux** : inchangés (§7).
- **Attestation** (forme D.3) :
  - pièces D.2 n° 1 à 9 non ouvertes ; variable `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée ;
  - lignes D.2 n° 5 et 6 repérées par leur sha256 par un script qui n'affiche que des numéros et des comptes, jamais affichées, absentes des sorties de `cargo xtask verify` ;
  - exposé aux comptes et bornes que portent l'annexe D (D.1) et le script de recherche C-B0-10 (iv) du G1 (D.1 n° 9) ;
  - aucune statistique S2 calculée sur les journaux de campagne ; aucun z, K, P̂_more ni φ de campagne vu.
