# G1 — lot B d'ADR-0028 (sensibilité « plage ADR-0025 incluse » et couverture par week-end, ADR-0025 déc. 4 ; bloc 3 : définition d'écart, HS2-06 ; bloc 6 : date de la partition, HS2-07), Shōgen S2 — journal

- **Modèle** : `claude-opus-5-5` (identifiant exact déclaré par le harnais, R-1 déclaré en tête de session), effort max selon la commande de lancement (réglage non observable depuis l'agent) ; worker G1, contexte frais, une session. Aucun commit, aucun workflow déclenché (R-20). Aucune variable `GIT_DIR` ni `GIT_WORK_TREE` posée, aucun `--write-tree`. Écritures git, toutes dans le worktree du lot : `checkout --detach cf696bd` (HEAD du worktree), `apply --3way` de `B-SEG-2/lot.diff` (index du worktree), `add -N` des fichiers neufs (index du worktree) ; la référence de branche `worktree-wf_1c82774a-d5f-10` reste à `fa0ce5b`. `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée (absente de l'environnement, retirée de chaque exécution) ; tests sur fixtures seulement ; rien écrit sur C:.
- **Horloge** (`date -u`, reflog du worktree, heures de fichier) : worktree créé à 07:48:48Z ; HEAD détaché à 07:51:03Z ; suite de base 07:52:57Z ; consultation advisor (canal 1) à 08:06Z ; **estimation R-25 et définitions écrites et scellées avant tout code à 08:10:27Z** (`oracles/estimation-r25.txt`, sha256 `97650774ada0a52350be954b2251338c3d0ce3dc9473b7b502b45c1465c36efb`) ; fixture mesurée à 08:11:00Z ; premier code 08:12Z ; dépassement R-25 mesuré vers 08:18Z, seconde consultation, coupe en trois ; suites a1 08:25:41Z, a2 08:27:22Z, final 08:32:48Z ; P2P 08:36:04Z-08:37:16Z ; première campagne de mutants 08:39:52Z-08:55:47Z ; F2P, chaîne et reprise des arbres de 08:42Z à 08:47Z ; campagne sur les arbres `arbres2` à partir de 08:58Z ; cas dégénéré (E-8), arbres `arbres3`, campagne complémentaire, F2P et chaîne de 09:02Z à 09:08Z ; journal, xtask, contrôle D.2 et enregistrement d'oracle ensuite.
- **Consultations de l'advisor intégré (canal 1, R-26)** : trois. (1) Avant le code (08:06Z) : ordre des gestes, contraintes des tests existants, oracles ; suivi. (2) Au dépassement R-25 (08:18Z, « sinon coupe et consultation » de la commande) : couper B-a sur sa couture plutôt que compacter ; suivi (§1). (3) À la clôture, livrables écrits (§11).
- **Mandat** : commande de mission de l'orchestrateur Shōgen (`claude-fable-5-1`), lot B de l'annexe A (l.17) : ADR-0025 déc. 4, HS2-06, HS2-07 ; corrections C-1 à C-12 du cp-1 bref intégrées à la commande. Lus avant tout travail : ADR-0025 (en entier, l.14 comprise : E-2), ADR-0028 D2 pt 7, §1 bis.1 pt 9, §1 bis.2, D6 (iv), annexes A, B, C, D (D.2, D.4, D.5), ADR-0026 déc. 1, doc 10 §5.2 et §6, `r1.py`, `r2.py`, `records.py`, `window.py`, `report.py` et les tests des lots précédents.
- **Classification** : bounded. Le lecteur existe (`records` → `r1`/`r2` → `report`) ; le lot ajoute des lignes au rendu et deux modules de tests, aucune statistique neuve.
- **Résultat** : trois sous-lots (§1) : **B-a1** (table de sensibilité, 197 lignes ajoutées), **B-a2** (couverture par week-end, 115), **B-b** (blocs 3 et 6, 100). Suites 216 → 219 → 222 → 224 tests, OK (2 sauts, variable absente), 0 entrée TMP, 0 `__pycache__`, sur le worktree et sur une chaîne rejouée depuis une archive fraîche. F2P : 11 FAIL, 0 ERROR. P2P texte : des insertions seules, aux trois endroits prévus. Mutants : §5. Aucune valeur d'ADR-0025 dans `shogen_s2/` (garde grep : 0 ligne).

## 0. Préconditions mesurées, écarts d'entrée

- **E-3 (base du worktree)** : le harnais a créé le worktree à `fa0ce5b` (branche `worktree-wf_1c82774a-d5f-10`), ni `0abc881` (commande) ni `main`. HEAD détaché sur `cf696bd` (= `f5b8269` + ligne JOURNAL seule, C-1 du cp-1), référence de branche inchangée. Le brief à `0abc881` est périmé (C-1) : `B-SEG-1` est commis (`dc39cb8`, `83f86d8`, `05cff36`, `b72509b`, ancêtres de `cf696bd`) ; `git apply --check -R F:/tmp/shogen-lots/B-SEG-1/lot.diff` sort 0 sur `cf696bd` ; il n'est donc pas réappliqué.
- **Base du lot (C-1)** : `cf696bd` + `F:/tmp/shogen-lots/B-SEG-2/lot.diff` (sha256 `eff6e152f0def9d7…`), posé par `git apply --3way` et laissé à l'index (base de diff du lot). Sur deux archives `git archive cf696bd` extraites sous `F:/tmp`, `lot.diff` d'une part et `bseg-2a` → `2b` → `2c` d'autre part donnent un `s2-harness` identique (`diff -r`) ; le worktree lui est identique. `report.py` `706c4b7670d22593a3b3a2fdef3a8ece5f3c5e6f20093de05ff269c1091a60af`, `tests/test_bloc1.py` `73046305ab1b08d1702fb1e40a49f827098ca959b95fcad8f16d9594256f9cbc` : les 16 premiers caractères sont ceux de C-1 ; le 17ᵉ du cp-1 (`f`, `c`) ne concorde pas (`a`, `7`), coquille probable, consignée. Suite de base : 216 tests, OK (skipped=2), 0 entrée TMP. L'observation hors lot de C-12 (`expected.json` du worktree `-2`) ne concerne pas ce worktree (`-10`), dont l'arbre est vérifié contre la base ci-dessus.
- **E-2 (pièce D.2 n° 6, exposition déclarée)** : entre 07:48:48Z et 07:51:03Z, avant la lecture de l'annexe D.2, la commande `git show cf696bd:docs/adr-0025/ADR-0025-periode-doublee-S2.md | head -c 6000` a affiché ADR-0025 en entier, **ligne 14 comprise** (repérée ensuite par son sha256 `0fe88f1a…b71f`, octets 2640-3021, sans nouvel affichage). Mécanisme : la commande dit « Lis ADR-0025 dec. 4 » ; le repérage préalable par sha prescrit par D.2 n° 6 n'a pas été fait. `error_origin` : worker. Aucune valeur de cette ligne n'entre dans le code, les tests, ce journal ni les diffs (contrôle D.2 n° 5-6 : §4.9). Toute lecture ultérieure d'ADR-0025 est passée par plages excluant la ligne repérée. Le contrôle FM-1.1 de l'orchestrateur verra ce chemin dans les appels d'outils de cette session.

## 1. Coupe R-25 (C-11 du cp-1)

- **Estimation ascendante scellée avant tout code** (08:10:27Z) : B-a ≈ 170 (code ≈ 55, tests ≈ 110), B-b ≈ 57 ; frontière du cp-1 (B-a : table, couverture, étiquettes ; B-b : blocs 3 et 6).
- **E-1 (estimation fausse)** : B-a mesuré à **281** lignes ajoutées (81 de code, 194 de tests, 6 d'amendements), contre ≈ 170. Causes : lignes blanches et docstrings comptées, fixture et assistants de test plus longs que prévu, et une borne de 110 caractères par ligne (précédent E-3 du G1 de B-SEG-2) qui allonge le code. `error_origin` : worker. Le fichier scellé n'est pas réécrit.
- **Cas fermé (FM-2.4)** : consultation (canal 1), puis **coupe de B-a sur sa couture** : B-a1 (table) et B-a2 (couverture) ; B-b inchangé. Autre forme possible : compacter B-a sous 200 lignes ; écartée (il aurait fallu retirer docstrings ou assertions). Le test mono-strate passe en B-a2 (son objet principal est la ligne « non applicable » de la couverture), ce qui garde B-a1 sous le seuil ; en B-a1, la branche mono-strate de la table n'est donc exercée par aucun test (mutant MA14 : colonne F seulement, §5).
- **Mesure** (`oracles/mkdiff_nfm.py`, repris de `mkdiff.py` du G1 de B-SEG-2 avec la ligne `new file mode` ; fichiers neufs entiers ; aucune ligne ajoutée au-delà de 110 caractères, `oracles/longueurs.py`) :

| sous-lot | `report.py` | tests | ajoutées | retirées | seuil 200 |
|---|---|---|---|---|---|
| **B-a1** : table de sensibilité, étiquettes, pools D1 de la variante | +44 −2 | `test_sensibilite.py` 145 (neuf) ; `test_g2_adversarial.py` +5 −1 ; `test_pool_analyse.py` +3 −2 | **197** | 5 | conforme |
| **B-a2** : couverture par week-end ; cas dégénéré de la queue | +40 −2 | `test_sensibilite.py` +72 −10 ; `test_pool_analyse.py` +3 −2 | **115** | 14 | conforme |
| **B-b** : bloc 3 (définition, paramètres), bloc 6 (date) | +15 | `test_bloc3_bloc6.py` 78 (neuf) ; `test_exclusion.py` +3 −2 ; `test_pool_analyse.py` +2 −2 ; `test_sensibilite.py` +2 | **100** | 4 | conforme |
| lot entier (base → final, `s2-harness`) | +97 −2 | `test_sensibilite.py` 209 ; `test_bloc3_bloc6.py` 78 ; `test_g2_adversarial.py` +5 −1 ; `test_pool_analyse.py` +4 −2 ; `test_exclusion.py` +3 −2 | 396 | 7 | coupe obligatoire (faite) |

- **Lignes datées proposées pour l'annexe A** (acte de l'orchestrateur, non écrit ici) :
  - **B-a1** (2026-09-30, coupe R-25 du G1 de B) : ADR-0025 déc. 4 et ADR-0028 D2 pt 7 : section `[SENSIBILITÉ]` (avec une plage seulement), par strate du calendrier : variante exclue (principale) et incluse (sensibilité) en n, K, P̂_more, z ou garde §5.4 et queue exacte, drapeau 1 ; écart de z ; pools D1 de la variante s'ils diffèrent ; étiquettes de D.5 et « causalité non établie ». Véhicule : `report.py`, `tests/test_sensibilite.py` (neuf), amendement de `test_g2_adversarial.py`, épingle. Oracle : `r1.recompute_from_journal`, écart recalculé en Decimal ; 219 tests. Taille 197 [mesuré]. Tuyau : `report` → section ; consommateur : RENDU puis `docs/11`. cp-1 bref.
  - **B-a2** (2026-09-30, même coupe) : couverture par week-end calendaire UTC (dérivée de `strate_calendar`), heures = fenêtres × w, comptes « en totalité / partiellement / retirés en totalité par la plage » ; « non applicable » en mono-strate. Oracle : recompte en bibliothèque standard ; cas dégénéré de la queue (E-8) ; 222 tests. Taille 115 [mesuré]. cp-1 bref.
  - **B-b** (2026-09-30, même coupe) : HS2-06 (définition d'écart et paramètres de `run_params` au bloc 3) ; HS2-07 (date de la partition au bloc 6, descriptif seulement). Véhicule : `report.py`, `tests/test_bloc3_bloc6.py` (neuf), épingles. 224 tests. Taille 100 [mesuré]. cp-1 bref.

## 2. Changements (worktree du lot, sur la base empilée)

| fichier | B-a1 | B-a2 | B-b |
|---|---|---|---|
| `shogen_s2/report.py` | imports (`localcontext`, `DECIMAL_PREC`, `STRATE_DEFAUT`) ; `_ligne_variante` ; section `[SENSIBILITÉ]` après le bloc 6, avec une plage seulement | import `weekday_utc` ; `_duree`, `_week_ends` ; couverture par week-end en fin de section | 2 lignes sous l'en-tête du bloc 3 ; 1 ligne au bloc 6 après `k_eff` |
| `tests/test_sensibilite.py` | neuf : fixture w = 3600 s, 3 tests (table, forme J28, plage sans effet) | recompte stdlib ; cas dégénéré de `cellule()` ; 3 tests (couverture, mono-strate, queue dégénérée) ; 2 assertions dans les tests de B-a1 | 1 assertion (blocs 3 et 6 dans la forme J28) |
| `tests/test_bloc3_bloc6.py` | — | — | neuf : 2 tests |
| `tests/test_g2_adversarial.py` | `test_plage_hors_campagne_sans_effet_ligne_bloc1_seule` : section retirée avant comparaison, présence exigée | — | — |
| `tests/test_pool_analyse.py` | `SHA_BASE_AVEC_OPTION` re-capturé | re-capturé | re-capturé |
| `tests/test_exclusion.py` | — | — | `SHA_BASE_SANS_OPTION` re-capturé |

- sha256 de `report.py` : base `706c4b76…a60af` ; a1 `bb5e2199…` ; a2 `151c39ac…` ; final `93d27ba8…` (16 premiers caractères, `oracles/LIVRABLES.sha256` pour les valeurs entières). `r1`, `lm`, `r2`, `records`, `window` inchangés ; aucune dépendance neuve.

## 3. Définitions appliquées (cas fermés par le G1, signalés ; forme retenue, autre forme)

Écrites avant le code dans le fichier scellé (§1), sauf D-10 bis et D-12, fixées pendant le code et signalées ici.
- **D-1 (C-5 i)** : pool D1 de la variante incluse **mécanique** : `analysis_pools` sur les fenêtres de la variante, forme de `r1.recompute_from_journal` (l'oracle de C-4). Pools imprimés par strate s'ils diffèrent du principal. Autre forme : gelé au pool principal.
- **D-2 (C-5 ii)** : la variante recalcule R1 seul (n, K, P̂_more, z ou garde §5.4 et queue exacte, drapeau 1) sur les marqueurs du segment sans exclusion, `dans_seg` déjà calculé au bloc 1 (même `t_fin` à n fixe, lu avant segment et exclusion), dédoublonnés last-wins ; ni L&M ni R2.
- **D-3 (C-5 iii)** : date de la partition, axe ASN = `ts` du relevé `asn_attribution` retenu (last-wins de `compute_partition`, après le filtre de lecture) de chaque hôte du pool ; min et max, epoch et ISO, avec le compte k / N hôtes du pool ; aucun relevé retenu : « non mesurée » ; suffixe « descriptif seulement (ADR-0028 annexe D.5) ». Amende HS2-07 (« sur tout le journal »). Autre forme : une date par hôte (la table ASN du bloc 5 en donne déjà l'heure ISO).
- **D-4 (C-5 iv)** : plage qui ne retire rien : section imprimée, lignes des deux variantes égales, écart 0 si z est publié (sinon « non calculable »), 0 retirée par week-end.
- **D-5 (C-5 v)** : étiquettes verbatim de l'annexe D.5 amendée (« sensibilité — biaisée vers le haut par construction ; documente l'exclusion D5 ; pas un estimateur alternatif ») et d'ADR-0025 (« causalité non établie »).
- **D-6** : écart de z = z(incluse) − z(exclue), en `Decimal` à `DECIMAL_PREC` (50), convention imprimée ; un zéro exact s'imprime `0` (et non `0E-49`) ; « non calculable » si un z manque. Autre forme : exclue − incluse.
- **D-7 (C-2)** : week-end = suite maximale de jours UTC consécutifs dont le jour (`window.weekday_utc`, lundi = 0) est dans `stress_weekdays` ; bornes [premier jour 00:00Z ; lendemain du dernier 00:00Z) ; fenêtres distinctes de la strate stress de chaque variante ; « complet » = nombre de débuts de grille (pas w) dans les bornes, soit 48 h = 48 × 3600 / w fenêtres pour [5, 6], jamais codé ; « en totalité » = complet, « partiellement » = entre 0 et complet exclus, « retiré en totalité par la plage » = 0 dans la variante exclue et au moins 1 dans l'incluse ; « non applicable » pour un calendrier mono-strate, ou `stress_weekdays` vide ou plein. Autre forme : heures décimales arrondies (style d'ADR-0025 déc. 4), écartée : il faudrait fixer une règle d'arrondi.
- **D-7 bis** : durée imprimée **exacte**, « H h MM min » (plus « SS s » si non nul) = fenêtres × w secondes, w de `run_params`.
- **D-8** : format de la table en lignes `  <strate> <variante> : n = … ; K = … ; P̂_more = … ; z … ; drapeau 1 = …`, qui ne reprend jamais la phrase du bloc 3 `strate « s » : n = … fenêtres complétées` ni `axe ASN NON MESURÉ`. Motif : `test_plage_vidant_une_strate` et `test_type_vide_rendu_sans_asn_ni_horloge` restent à leur portée (blocs 3-6) sans amendement. Autre forme : amender ces tests.
- **D-9** : section `[SENSIBILITÉ]` après le bloc 6, avant la ligne de clôture, avec une plage seulement (C-6).
- **D-10** : strates de la table = strates du calendrier (`weekend_utc` : calme et stress ; `single` : sa strate) ; strate absente d'une variante : « absente (0 fenêtre retenue) ».
- **D-10 bis** : la ligne « non mesurée » du bloc 6 est formulée « aucun hôte du pool n'a de relevé asn_attribution retenu » : la première forme contenait la sous-chaîne du message du bloc 5 de B-SEG-2 que `test_bloc5_sondes_toutes_retirees_message_vrai` exclut d'un journal sans sonde (E-4).
- **D-11 (C-8)** : le texte du bloc 3 est fidèle à `r1.classify_ecart` (l.131-196) : précédence panne > staleness > hors-enveloppe ; N < n_min, médiane_LOO ≤ 0 ou τ_classe absent : non évaluable (pas un écart) ; **sinon pas d'écart**. Le littéral du renvoi de C-8 finit par « sinon non évaluable », qui ne décrit pas `classify_ecart` (qui rend `PAS_ECART` quand N ≥ n_min et que le prix est dans l'enveloppe). Écart au littéral, signalé ; le mutant MB05 montre que le test fige la forme fidèle. Autre forme : imprimer le littéral de C-8 tel quel. Paramètres : `sigma_classe` et `tau_classe` (mappings bruts de `run_params`, comme au bloc 1) et `n_min_hors_enveloppe` ; jamais `sigma_class_of_flux` (`test_a_flux_mort_partout` compare tout le texte après `[BLOC 3]` entre deux pools).
- **D-12** : la ligne du bloc 6 dit « axe ASN » : la date porte sur les relevés `asn_attribution` ; l'axe contenu de la partition porte sur les fenêtres retenues du bloc 1, sans ligne neuve.

## 4. Oracles (sorties sous `F:/tmp/shogen-lots/B/oracles/`)

### 4.1 Suites
- Worktree : 224 tests, OK (skipped=2), 0 entrée TMP, 0 `__pycache__` (suite finale, §10).
- Arbres des sous-lots (`arbres3/{a1,a2,final}`, livrés) : 219, 222, 224, OK (skipped=2), 0 entrée TMP, 0 `__pycache__` (`suite-arbres3-*.out`).
- Chaîne sur archive fraîche `cf696bd` : `B-SEG-2/lot.diff` puis `B-a1.diff`, `B-a2.diff`, `B-b.diff` (`patch -p1`, dry-run d'abord, 0 `.orig`, 0 `.rej`) ; 216 → 219 → 222 → 224, OK ; `s2-harness` final égal au worktree (`chaine.out`). `B-a1.diff` passe aussi `git apply --cached --check` sur l'index du worktree (base empilée).
- Les deux sauts de chaque suite sont les tests nommés de D.4 a (motif « SHOGEN_S2_CAMPAGNE_CONTROL absente »).

### 4.2 Précondition de la fixture (C-3), mesurée avant les tests
`mesure-fixture.out` (08:11:00Z), sur la fixture de conception à w = 3600 s : stress, variante exclue n = 49, K = 25, garde 11,96 ≥ 10, z publié ; incluse n = 57, K = 28, garde 13,77, z publié, différent ; calme, sous la garde dans les deux variantes, queue exacte applicable (n = 4 et 5) ; pool calme de la variante exclue sans bitstamp (D1 cas b), celui de l'incluse avec. Chiffres de fixture synthétique, sans rapport avec la campagne. Le test `test_table_cellules_ecart_pools_etiquettes` asserte ces préconditions.

### 4.3 Oracle des cellules (C-4)
Chaque ligne de variante est écrite par le test depuis `r1.recompute_from_journal(c, j, exclude_ranges=[…])` et `(…, exclude_ranges=())`, même segment (test J28), jamais depuis le rendu ; l'écart est recalculé dans le test en `Decimal` à précision 50 ; les week-ends sont recomptés en bibliothèque standard (`datetime.weekday`) depuis les lignes `window_close` de `control.jsonl`, plages fermées sur `window_start`, segment à n fixe recalculé dans le test. Le sha d'un rendu n'est qu'une épingle de déterminisme.

### 4.4 F2P
Tests finaux sur le code de base (`copies/f2p`) : 11 FAIL, 0 ERROR : les 8 tests neufs, `test_plage_hors_campagne_sans_effet_ligne_bloc1_seule` (amendé : section exigée) et les deux épingles. **E-5** : une première mesure donnait 6 ERROR (`str.index` sur une section absente) ; `section()` rend `[]` et l'amendement g2 asserte la présence : FAIL seulement.

### 4.5 P2P texte (C-6), justification des re-captures
`p2p.sh` : les 216 tests de BASE sur le code base (deux fois), a1, a2 et final (`p2p_texte.py` du G1 de B-SEG-2, sans changement ; classificateur neuf `p2p_lignes_B.py`, prédictions écrites dans le script avant la mesure) :
- base-1 contre base-2 : 96 sorties identiques, 0 défaut ;
- base → a1 : 42 insertions de la section `[SENSIBILITÉ]`, toutes dans une sortie avec plage, avant la clôture ; 53 identiques ;
- a1 → a2 : 42 insertions de lignes de couverture dans la section ; 53 identiques ; 0 défaut ;
- a2 → final : 80 insertions de 2 lignes sous l'en-tête du bloc 3 et 80 d'une ligne au bloc 6 après `k_eff` ; 14 identiques (sorties vides de CLI en erreur) ;
- aucune ligne existante modifiée ni retirée. Seuls « défauts » : l'appel CLI des deux tests d'épingle manque côté nouveau code, parce que l'assertion du sha, placée avant l'appel, échoue (conséquence attendue de la re-capture) ; avec les épingles re-capturées, ces deux tests passent, CLI comprise (§4.1).
- Épingles : `SHA_BASE_AVEC_OPTION` 677b1bfc…422114 → a1 `7a4ff05c…663734` → a2 `30f5c0fb…9ff0e1` → b `4d511faf…b25819` ; `SHA_BASE_SANS_OPTION` inchangé en a1 et a2 (`b054a0f4…69ac01e`, la section n'existe qu'avec une plage), puis b `9518d21b…4b62a92` (`epingle-*.out`, script `epingle.py` du G2 de B0 repris tel quel). Chaque re-capture est comptée à part (« épingle supersédée »).

### 4.6 Mutants
§5.

### 4.7 Garde grep (C-2)
`grep -rnE` sur `shogen_s2/` des valeurs d'ADR-0025 et de sa décision 4 (epochs 1790273880, 1790435280, 1790435340, 1790435220 ; comptes 2618, 2617, 1709, 909, 908, 35982 ; heures 189,95, 157,4, 19,0, 46,7, 43,5, 47,9, 166,8, formes à point ; dates 29/08, 05/09, 12/09, 19/09, 26/09 ; 15:07, 15:08, 18:18) : 0 ligne (`garde-grep-adr0025.out`). Les heures de déc. 4 ne servent d'attendu nulle part (C-12).

### 4.8 xtask
`cargo --locked xtask verify` sur l'arbre `F:/tmp/shogen-lots/B/lotcheck` (arbre entier : archive `cf696bd` + `B-SEG-2/lot.diff` + `lot.diff` de ce lot, ce journal compris, `patch -p1` ; `s2-harness` et journal égaux au worktree, `oracles/lot-check.out` ; `oracles/xtask.sh` du G1 de B-SEG-2, chemins seuls changés ; toolchain forcée, serveurs rustup vers 127.0.0.1:9, `CARGO_NET_OFFLINE=true`, `CARGO_HOME` sous F:) : rejoué en dernier sur ce journal final, résultat au §10.

### 4.9 Contrôle D.2 n° 5 et 6
`oracles/d2_check.py` repère la cartographie l.51 et ADR-0025 l.14 par leur sha256, sans les afficher, et compte dans chaque livrable la ligne entière et ses fragments de 40 caractères (pas de 20) : résultat au §10.

### 4.10 Longueur de ligne
Aucune ligne ajoutée au-delà de 110 caractères dans les trois sous-lots (plus longue : 110 ; `oracles/longueurs.py`, précédent E-3 du G1 de B-SEG-2).

## 5. Mutants (C-4 : chacun tué par le test prévu)

Lanceur `oracles/mutants_B2.py` (adapté de `mutants_bseg2.py` du G1 de B-SEG-2) : copie neuve par mutant et par colonne, suite complète, TMP neuf, variable retirée ; mort = code de retour ≠ 0 ; critère C-4 = chaque test prévu figure parmi les rouges. Colonnes : A1 = arbre de B-a1, A2 = arbre de B-a2, F = arbre final ; les mutants d'un sous-lot tournent sur son arbre (ses tests seuls doivent les tuer) et sur F. 38 définitions (`mutants_def_B.py`), contrôle à sec : 38 applicables (`verif-mutants-def.out`). Liste : brief (variante inversée, colonne manquante, écart faux, week-end mal compté), C-4, C-5, C-8, et ceux trouvés en écrivant le code.

- **Campagne principale** sur les arbres `arbres2` (code livré, identique à l'octet ; tests d'avant E-8), `mutants-B2.json` :

| id | mutation | colonne : état (rouges) | test(s) prévu(s) rouge(s) |
|---|---|---|---|
| MB00 | temoin (aucune mutation) | A1 : survit (0) ; A2 : survit (0) ; F : survit (0) | — (témoin) : oui |
| MA01 | variante inversee (exclue <-> incluse) | A1 : tué (3) ; F : tué (4) | `test_table_cellules_ecart_pools_etiquettes`, `test_forme_j28_cli_segment_n_fixe_et_plages` : oui |
| MA02 | colonne K manquante | A1 : tué (3) ; F : tué (4) | `test_table_cellules_ecart_pools_etiquettes` : oui |
| MA03 | colonne P_more manquante | A1 : tué (3) ; F : tué (4) | `test_table_cellules_ecart_pools_etiquettes` : oui |
| MA04 | ecart de z de signe inverse | A1 : tué (2) ; F : tué (3) | `test_table_cellules_ecart_pools_etiquettes` : oui |
| MA05 | ecart de z a la precision par defaut (28) | A1 : tué (2) ; F : tué (3) | `test_table_cellules_ecart_pools_etiquettes` : oui |
| MA06 | ecart nul imprime brut (0E-49) | A1 : tué (1) ; F : tué (1) | `test_plage_sans_effet_variantes_egales_ecart_0` : oui |
| MA07 | variante incluse = exclue (marqueurs filtres) | A1 : tué (3) ; F : tué (4) | `test_table_cellules_ecart_pools_etiquettes` : oui |
| MA08 | variante incluse sur le journal entier (segment ignore) | A1 : tué (1) ; F : tué (1) | `test_forme_j28_cli_segment_n_fixe_et_plages` : oui |
| MA09 | pool de la variante gele au pool principal | A1 : tué (8) ; F : tué (8) | `test_table_cellules_ecart_pools_etiquettes` : oui |
| MA10 | pools differents jamais imprimes | A1 : tué (1) ; F : tué (1) | `test_table_cellules_ecart_pools_etiquettes` : oui |
| MA11 | etiquette de sensibilite reecrite | A1 : tué (2) ; F : tué (2) | `test_table_cellules_ecart_pools_etiquettes` : oui |
| MA12 | causalite non etablie absente | A1 : tué (2) ; F : tué (2) | `test_table_cellules_ecart_pools_etiquettes` : oui |
| MA13 | section imprimee sans option | A1 : tué (3) ; F : tué (3) | `test_table_cellules_ecart_pools_etiquettes` : oui |
| MA14 | strate du calendrier ignoree (weekend_utc suppose) | F : tué (1) | `test_mono_strate_sans_week_end_ni_exception` : oui |
| MA15 | ecart calcule quand un z manque | A1 : tué (23) ; F : tué (25) | `test_table_cellules_ecart_pools_etiquettes` : oui |
| MW01 | week-end complet code 2880 fenetres | A2 : tué (3) ; F : tué (3) | `test_couverture_week_ends_recomptee` : oui |
| MW02 | duree a w = 60 codee | A2 : tué (3) ; F : tué (3) | `test_couverture_week_ends_recomptee` : oui |
| MW03 | doublons de reprise comptes (marqueurs, non fenetres) | A2 : tué (4) ; F : tué (4) | `test_couverture_week_ends_recomptee` : oui |
| MW04 | borne de week-end : pas de remontee au premier jour | A2 : tué (3) ; F : tué (3) | `test_couverture_week_ends_recomptee` : oui |
| MW05 | borne de week-end : jour courant teste au lieu de la veille | A2 : tué (4) ; F : tué (4) | `test_couverture_week_ends_recomptee` : oui |
| MW06 | variantes inversees dans la couverture | A2 : tué (3) ; F : tué (3) | `test_couverture_week_ends_recomptee` : oui |
| MW07 | retires en totalite : partiellement retires comptes | A2 : tué (3) ; F : tué (3) | `test_couverture_week_ends_recomptee` : oui |
| MW08 | partiellement : complet compte aussi | A2 : tué (3) ; F : tué (3) | `test_couverture_week_ends_recomptee` : oui |
| MW09 | mono-strate envoyee au calcul des week-ends | A2 : tué (1) ; F : tué (1) | `test_mono_strate_sans_week_end_ni_exception` : oui |
| MW10 | retirees par la plage : compte exclu imprime | A2 : tué (4) ; F : tué (4) | `test_couverture_week_ends_recomptee` : oui |
| MB01 | tau code en dur (valeurs de la fixture standard) | F : tué (1) | `test_bloc3_definition_et_parametres_de_run_params` : oui |
| MB02 | sigma code en dur (valeurs de la fixture standard) | F : tué (1) | `test_bloc3_definition_et_parametres_de_run_params` : oui |
| MB03 | n_min code en dur (4) | F : tué (1) | `test_bloc3_definition_et_parametres_de_run_params` : oui |
| MB04 | definition : precedence reecrite | F : tué (3) | `test_bloc3_definition_et_parametres_de_run_params` : oui |
| MB05 | definition : litteral de C-8 (sinon non evaluable) | F : tué (3) | `test_bloc3_definition_et_parametres_de_run_params` : oui |
| MB06 | date lue sur les sondes avant filtre (tous[2]) | F : tué (1) | `test_bloc6_date_releve_retenu_apres_filtre` : oui |
| MB07 | date : premier releve retenu au lieu du dernier | F : tué (1) | `test_bloc6_date_releve_retenu_apres_filtre` : oui |
| MB08 | date : ts maximal au lieu du dernier retenu | F : tué (1) | `test_bloc6_date_releve_retenu_apres_filtre` : oui |
| MB09 | date : min et max inverses | F : tué (1) | `test_bloc6_date_releve_retenu_apres_filtre` : oui |
| MB10 | date : hote hors pool compte | F : tué (1) | `test_bloc6_date_releve_retenu_apres_filtre` : oui |
| MB11 | mention descriptif seulement absente | F : tué (3) | `test_bloc6_date_releve_retenu_apres_filtre` : oui |
| MB12 | date non mesuree : libelle change | F : tué (3) | `test_bloc6_date_releve_retenu_apres_filtre` : oui |

exécutions : 64 ; tuées : 61 ; survivantes : 3 (témoins compris) ; inapplicables : 0

- **Campagne complémentaire** sur les arbres livrés `arbres3` (= `arbres2` + le cas dégénéré de `cellule()` et `test_queue_degeneree_fixture_d_exclusion` en B-a2 ; code identique), `mutants-B3.json` et `mutants-B4.json` : témoins sur A1, A2, F ; MA16 (branche dégénérée de la queue) ; rejeu, colonne F, de MA07, MA08 et MA09, seuls mutants qui changent l'assiette ou le pool de la variante incluse, donc seuls candidats à dépendre du cas dégénéré ajouté :

| id | mutation | colonne : état (rouges) | test(s) prévu(s) rouge(s) |
|---|---|---|---|
| MB00 | temoin (aucune mutation) | A1 : survit (0) ; A2 : survit (0) ; F : survit (0) | — (témoin) : oui |
| MA16 | queue degeneree imprimee comme une queue exacte | A1 : tué (1) ; A2 : tué (2) ; F : tué (2) | `test_queue_degeneree_fixture_d_exclusion` : oui en A2 et F ; en A1, test prévu absent par construction (ajouté en B-a2), mutant tué par l'épingle seule |
| MA07 | variante incluse = exclue (marqueurs filtres) | F : tué (5) | `test_table_cellules_ecart_pools_etiquettes` : oui |
| MA08 | variante incluse sur le journal entier (segment ignore) | F : tué (1) | `test_forme_j28_cli_segment_n_fixe_et_plages` : oui |
| MA09 | pool de la variante gele au pool principal | F : tué (8) | `test_table_cellules_ecart_pools_etiquettes` : oui |

exécutions : 6 ; tuées : 3 ; survivantes : 3 (témoins compris) ; inapplicables : 0 (arbres3, témoins et MA16) ; exécutions : 3 ; tuées : 3 ; survivantes : 0 (témoins compris) ; inapplicables : 0 (arbres3, MA07-MA09).

- **Portée** : les tests d'`arbres3` ne diffèrent de ceux d'`arbres2` que pour une ligne à queue dégénérée ; aucune ligne de la fixture de conception n'est dégénérée (§4.2), sauf sous MA07-MA09, rejoués ; les morts de la campagne principale valent donc pour les arbres livrés. MA16 en A1 n'est tué que par l'épingle : le test prévu est ajouté en B-a2 (E-8).

## 6. Application des corrections du cp-1 bref

| correction | traitement |
|---|---|
| C-1 | base mesurée et nommée (§0) ; `B-SEG-1` non réappliqué (commis) ; diff du lot pris contre l'index (base empilée) |
| C-2 | heures par week-end, deux variantes, « complet » dérivé du calendrier et de w (D-7) ; aucune valeur d'ADR-0025 dans `shogen_s2/` (§4.7) ; mono-strate : « non applicable », sans exception (`test_mono_strate_sans_week_end_ni_exception`) |
| C-3 | fixture à z publié dans les deux variantes de stress ; calme sous la garde avec queue exacte, écart « non calculable », drapeau 1 visible (§4.2) |
| C-4 | oracle hors du doré (§4.3) ; mutants tués par le test prévu (§5) |
| C-5 | D-1 à D-5 |
| C-6 | re-captures justifiées par le P2P (§4.5) ; section avec une plage seulement |
| C-7 | `test_forme_j28_cli_segment_n_fixe_et_plages` : `--segment-from`, `--segment-n-fixe` et deux plages, processus neuf, sortie = API + « \n », section, bloc 3 et bloc 6 présents |
| C-8 | paramètres lus de `run_params`, fixture à τ = 0,0123, σ = 7777 s, n_min = 5 (MB01-MB03) ; renvoi fidèle au code (D-11, MB05) ; date avant filtre tuée (MB06) |
| C-9 | items proposés au §8, non écrits dans l'annexe B |
| C-10 | modes MAST au §7 |
| C-11 | estimation scellée avant code ; coupe mesurée en trois sous-lots (§1) |
| C-12 | aucune lecture de journal réel ; aucun test de comptes nommé ajouté ; heures de déc. 4 jamais reproduites |

## 7. Risque résiduel MAST (C-10 ; libellés de l'annexe C)

- **FM-3.3 Incorrect verification** (doré pris pour oracle) : cellules, écart et week-ends vérifiés contre `recompute_from_journal`, un calcul Decimal du test et un recompte stdlib ; les épingles ne sont que du déterminisme, justifiées par le P2P.
- **FM-1.5 Unaware of termination conditions** (bornes) : bornes de week-end dérivées de `stress_weekdays`, jamais codées, avec un test à w = 3600 s ; plage qui ne retire rien (D-4) ; calendrier mono-strate (D-7) ; segment à n fixe dans la forme J28.
- **FM-2.3 Task derailment** : ni strate poolée (POOLEE), ni comptes de pertes (D5-AMEND), ni z_bloc (B-DEP-2), ni τ observé (D5-AMEND) dans ce lot : items proposés au §8.
- **FM-1.1 Disobey task specification** : variable jamais posée, fixtures seulement ; exposition à D.2 n° 6 déclarée (E-2), sans usage.
- **FM-2.4 Information withholding** : cas fermés listés au §3, avec l'autre forme.
- **FM-3.2 No or incomplete verification** : F2P (§4.4) et P2P (§4.5) sur toute la suite de base.

## 8. Items proposés pour l'annexe B (C-9 ; acte de l'orchestrateur)

| item | objet | propriétaire | déclencheur |
|---|---|---|---|
| troisième ligne de la table de sensibilité | strate poolée stratifiée dans les deux variantes, étiquetée exploratoire (ADR-0025 déc. 4 : « trois z ») ; même section, hors décision | orch. | G0 du lot POOLEE (SHOGEN-POOLEE-STRATIFIEE-1) |
| comptes de pertes dans la variante incluse | comptes de pertes par type d'enregistrement dans la section, SHOGEN-DP-JOURNAL-LOSS-1 (annexe D.5 amendée) | orch. | G0 du lot D5-AMEND |
| z_bloc,s dans la sensibilité | oui ou non, forme de l'écart si oui | orch. | G0 de B-DEP-2 ou de CRITERE, fixé à ce G0 |

## 9. Questions à l'orchestrateur

- **Q-G1-1** : ratification des cas fermés D-1 à D-12, en particulier D-11 (écart au littéral de C-8), D-7 bis (durée exacte) et D-8 (format de la table).
- **Q-G1-2** : frontière en trois sous-lots (B-a1, B-a2, B-b) contre deux au cp-1 (C-11) ; trois lignes datées proposées (§1).
- **Q-G1-3** : suite à donner à l'exposition E-2 (D.2 n° 6) pour les rôles futurs de ce worker (contrôle FM-1.1 du paquet).
- **Q-G1-4** : le script de vague crée les worktrees à `fa0ce5b` (E-3), ni à la base de la commande ni à `main` ; précédent : le worktree `-6` de B-SEG-2.

## 10. Clôture

- **Suites finales** (`oracles/run_suite.sh`, résumés `suite-*.summary`) : worktree 224, chaîne sur archive fraîche 224, arbre B-a1 219, arbre B-a2 222 ; toutes OK (skipped=2), exit 0, 0 entrée TMP, 0 `__pycache__`, variable jamais posée.
- **xtask** : `cargo --locked xtask verify` VERT (8 verdicts verts, 0 rouge, aucun téléchargement rustup) sur l'arbre `lotcheck` (archive `cf696bd` + `B-SEG-2/lot.diff` + `lot.diff`, ce journal compris ; suite 224 OK sur le même arbre ; `oracles/lot-check.out`, `oracles/xtask-final.summary`).
- **D.2 n° 5 et 6** : 0 occurrence de la ligne entière et de ses fragments de 40 caractères dans chaque livrable (`lot.diff`, sous-lots, ce journal, `G1-rapport.md`, estimation scellée ; `oracles/d2-check-final.out`).
- **Enregistrement d'oracle** `shogen.oracle-record.v1` (rôle G1, aucun run avec la variable) et empreintes des livrables : `oracles/LIVRABLES.sha256` ; chemin sous `F:/tmp/oracle-results/`.
  - Émissions (ajout daté du 2026-09-30, revue G2 du lot B, C-6) : la première, `F:/tmp/oracle-results/shogen-cf696bd-G1-B-2026-09-30-130576.json` (écrite à 09:13:06Z, sha256 `f544d063f947f63273744e98ea3c0b472ee14f90f210f75795254ed425d61533`), est remplacée et conservée ; seule `F:/tmp/oracle-results/shogen-cf696bd-G1-B-2026-09-30-175088.json` (09:16:30Z, sha256 `a9fbbfc1d627b2559a738f28c3d6a479ce7d24bb4f6bf4ad45038df21060a6d5`) fait foi. Les deux ne diffèrent que par le sha256 de ce journal, celui de `oracles/xtask-final.summary` et l'heure d'écriture (`json.tool`, puis `diff` : 3 lignes). Leur note F2P dit « 10 FAIL » ; la sortie qu'elles citent (`oracles/suite-f2p-F__tmp_shogen-lots_B_copies_f2p.out`) en compte 11, comme le §4.4 : note périmée, consignée ici, enregistrements non réécrits.
- **Livrables** (`F:/tmp/shogen-lots/B/`) : `lot.diff` (lot entier contre la base empilée, produit par `git diff` du worktree après `git add -N` des fichiers neufs ; ce journal compris) ; `B-a1.diff`, `B-a2.diff`, `B-b.diff` (sous-lots, `mkdiff_nfm.py`, chaîne vérifiée §4.1) ; `G1-rapport.md` (copie de ce journal) ; `oracles/` (scripts, sorties, estimation scellée).
- **Tuyau** (règle Branchement) : entrée = journaux (fixtures ici) ; sortie = section `[SENSIBILITÉ]` et lignes des blocs 3 et 6 du rendu ; chemin servi = la CLI `python -m shogen_s2.report` (RUNBOOK §9 e), couverte par le test J28 en processus neuf ; consommateurs : RENDU puis `docs/11` (absents à ce jour, annexe A).
- **Dette** : aucune nue ; points ouverts = items proposés (§8) et questions (§9), actes de l'orchestrateur.
- **Écarts consignés** (`error_origin`) : E-1 estimation R-25 fausse (worker, §1) ; E-2 exposition à D.2 n° 6 (worker, §0) ; E-3 worktree créé à `fa0ce5b` (script de vague, §0) ; E-4 sous-chaîne du message du bloc 5 reprise par la première forme de « non mesurée », vue par la suite et corrigée avant livraison (worker, D-10 bis) ; E-5 six ERROR au F2P, corrigés en FAIL (worker, §4.4) ; E-6 le mot « indépendant » dans une docstring de test (« oracle … du doré »), remplacé par « hors du doré » avant livraison, règle de vocabulaire de la commande (worker) ; E-7 brief à `0abc881` et empilement de `B-SEG-1` périmés, traités selon C-1 (commande) ; E-8 la branche « queue dégénérée » de la table n'était couverte que par une épingle (FM-3.3), vu en relecture après la première campagne de mutants : cas dégénéré ajouté à `cellule()` et test `test_queue_degeneree_fixture_d_exclusion` en B-a2 (worker).

## 11. Consultations et provenance

- Consultation de clôture (canal 1), livrables écrits : avis : deux retouches de libellé (§4.8 et §10 : l'arbre `lotcheck` du xtask final nommé avec sa recette ; D-11 : autre forme explicite), aucun changement de code ni de test ; suivi, puis `G1-rapport.md`, `lot.diff`, `lotcheck` (suite, xtask), contrôle D.2 et enregistrement d'oracle régénérés dans cet ordre.
- Scripts du G1 (`F:/tmp/shogen-lots/B/oracles/`) : `essai_rendu.py`, `essai_sens.py`, `mesure_fixture.py`, `maj_journal_1.py`, `maj_journal_2.py` (ces cinq sous `work/scripts/`), `mutants_B3.py`, `mutants_def_B3.py`, `mutants_def_B4.py`, `epingle.py` (repris du G2 de B0), `p2p_texte.py` (repris du G1 de B-SEG-2), `p2p_lignes_B.py`, `p2p.sh`, `mkdiff.py` (repris), `mkdiff_nfm.py`, `longueurs.py` (repris), `mutants_def_B.py`, `mutants_B.py`, `mutants_B2.py`, `verif_mutants_def.py`, `table_mutants_B.py`, `suites.sh`, `run_suite.sh`, `chaine.sh`, `xtask.sh` (repris), `d2_check.py`, `oracle_record_B.py`. Première campagne de mutants (`mutants-B.json`, sur les arbres d'avant E-5 et le changement de docstring, même code) : 64 exécutions, 61 tuées par le test prévu, 3 témoins survivants ; la table du §5 est celle des arbres livrés.

## 12. Corrections de la revue G2 (ajout daté du 2026-09-30 ; l.1-225 : texte revu, plus la ligne de C-6 au §10)
- **Générateur** : `claude-opus-5-5` (identifiant exact déclaré par le harnais en tête de session, R-1), effort max selon la commande de lancement (non observable depuis l'agent), contexte frais ; générateur G1 de correction, instance distincte du réviseur G2 et du worker G1 de ce lot. Mandat : commande de mission de l'orchestrateur Shōgen (`claude-fable-5-1`, 2026-09-30). Aucun commit, aucun workflow (R-20) ; aucune variable `GIT_DIR` ni `GIT_WORK_TREE` posée, aucun `--write-tree`, aucun `git add` ; `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée.
- **Horloge** (`date -u`) : première horloge 15:30:43Z ; corrections appliquées au worktree à 2026-09-30T15:38:37Z ; oracles de 15:38:51Z à 15:50:38Z ; ligne de C-6 écrite à 15:50:36Z, cette section ensuite ; `lot.diff`, suites, `cargo --locked xtask verify`, contrôle D.2 et enregistrement d'oracle refaits après elle, sur les copies qui la contiennent (heures au rapport de correction).
- **Revue appliquée** : `F:/tmp/shogen-lots/B/G2-rapport.md` (sha256 `473071596f0897c959cffab411bd9674f36ea95f28460d16c9279be04d62bef8`), verdict ACCEPTE-AVEC-CORRECTIONS, liste fermée C-1 à C-10.
- **C-1 à C-5, sous-lot B-c** : texte du réviseur, `g2r/oracles/corrections-G2-B-c.diff` (sha256 `c31aea8225818f650e95b28570bc31e575f2d2cf6f1eac5418e05882566eaf70`, recalculé égal ; copie `B-c.diff`), appliqué tel quel par `patch -p1`, sans décalage ni fuzz, 0 `.orig`, 0 `.rej`. Provenance : 130 lignes ajoutées et 9 retirées, rédigées par le réviseur G2 (`claude-opus-5-5`) et appliquées sans retouche ; `s2-harness` du worktree est identique aux arbres `fix`, `fixchk` et `fix-full` du réviseur (`diff -r`), et ce journal était celui de la version revue (sha256 `a093c3f5…acff5`) avant la ligne de C-6 et cette section.
  - C-1 : `test_g2_couverture_calendriers_et_w` : `stress_weekdays` [6, 0] (le week-end enjambe la semaine), [4, 5, 6] et [2], puis [5, 6] à w = 90 s ; en-tête et lignes par week-end comparés à `attendu_we`, recompte `datetime` depuis `control.jsonl`, écrit sans `report` ; un littéral à w = 90 s (branche « SS s » de `_duree`, D-7 bis).
  - C-2 : `test_g2_non_applicable_absente_et_mono_nommee` : `stress_weekdays` vide puis sur sept jours (« non applicable », strate absente des deux variantes, écart « non calculable ») ; calendrier `single` à strate « unique » (D-10).
  - C-3 : `test_g2_bloc6_k_sur_n` : un seul hôte du pool sondé, « 1 / 3 hôtes du pool » (D-3).
  - C-4 : `test_g2_pool_cas_a_entre_variantes` : bitstamp hors des deux pools de la variante exclue (D1 cas a), dans les deux pools de l'incluse ; cellules par l'oracle du §4.3 (D-1). `fixture()` généralisée (blocs, w, pannes), défauts inchangés.
  - C-5 (code) : couverture par week-end de `report.py` : les week-ends calendaires qui coupent l'intervalle [jour de la première ; jour de la dernière fenêtre de l'assiette] sont listés, à 0 s'ils n'ont aucune fenêtre ; « retirés en totalité par la plage » ne compte que les week-ends couverts dans l'incluse ; ligne neuve « non couverts (0 fenêtre dans les deux variantes, entre la première et la dernière fenêtre de l'assiette) : N ». Test : `test_g2_week_end_sans_fenetre_visible`, plus l'assertion « non couverts … : 0 » de l'assistant `week_ends` (§4.3). D-7 est complété en ce sens (revue G2, §9) : l'énumération porte sur les week-ends calendaires de l'assiette, vides compris.
  - C-6 (ce journal) : au §10, les deux émissions de l'enregistrement d'oracle du G1, `shogen-cf696bd-G1-B-2026-09-30-130576.json` (remplacée) et `shogen-cf696bd-G1-B-2026-09-30-175088.json` (fait foi).
- **Épingles** : `SHA_BASE_AVEC_OPTION` re-capturée par B-c, quatrième re-capture du lot après a1, a2 et b (`4d511faf…b25819` → `43cc5f854c8f8b3b95083056738eeda1f574c2fbda9ad796eed426d78a1f2897`), une ligne insérée, « non couverts … : 0 » ; `SHA_BASE_SANS_OPTION` inchangée (`9518d21b…4b62a92`) ; les deux, recapturées sur l'arbre corrigé, égalent les constantes.
- **Coupe, mesurée** (`git apply --numstat`, hors dépôt) : B-a1 197, B-a2 115, B-b 100, **B-c 130** (code +8 −1 ; tests +122 −8, dont `test_sensibilite.py` +119 −6 : classe `TestSensibiliteG2` 82, oracle `attendu_we` 28, généralisation de `fixture()` +6 −5 ; épingle +3 −2 ; ce journal hors compte) ; aucune ligne ajoutée au-delà de 110 caractères (plus longue : 110). Empilés dans l'ordre a1, a2, b, c par `patch -p1`, sans décalage ni fuzz : sur une archive `cf696bd` + `B-SEG-2/lot.diff`, 216, 219, 222, 224 puis 229 tests, `s2-harness` final égal au worktree ; sur une archive `1a63d80` (HEAD de `main` pendant la correction), 219, 222, 224 puis 229 ; tous OK (2 sauts, variable absente).
- **Oracles** :
  - suite : 229 tests OK (2 sauts), 0 entrée TMP, 0 `__pycache__`, sur le worktree et sur les copies ;
  - F2P, code du lot et tests corrigés : 5 FAIL, 0 ERROR : le test de C-5, l'épingle, et `test_couverture_week_ends_recomptee`, `test_forme_j28_cli_segment_n_fixe_et_plages`, `test_plage_sans_effet_variantes_egales_ecart_0`, qui passent par l'assistant `week_ends` ; les tests de C-1 à C-4 passent sur le code du lot (trous d'oracle, comportement juste) ;
  - mutants de la revue (colonne P, arbre corrigé, définitions du réviseur importées sans recopie) : MR01, MR03, MR04, MR06 à MR09, MR11, MR13, MR15, MR21 et MR22 tués, chacun par le seul test prévu ; MR05 tué par dépassement du délai de 240 s (boucle sans fin) ; MR10 tué (9 rouges) ; le témoin et MR02 (équivalent pour tout w qui divise 86 400) survivent ;
  - campagne du G1 (§5) rejouée en colonne P : les 38 définitions (37 de `mutants_def_B.py`, plus MA16) ; 37 tuées, test prévu parmi les rouges pour chacune ; MW07, dont C-5 réécrit l'ancre, est inapplicable telle quelle et rejouée en MW07P (même mutation, ancre adaptée) : tuée, `test_couverture_week_ends_recomptee` parmi les rouges ; témoin vert ;
  - P2P texte (instruments du réviseur) : tests du lot, code du lot contre code corrigé : 125 sorties comparées, 76 identiques, 49 insertions de la seule ligne « non couverts … : 0 », 0 défaut ; tests corrigés contre tests du lot, sur le code corrigé : 125 identiques (neutralité de la généralisation de `fixture()`) ;
  - garde grep des valeurs d'ADR-0025 (§4.7) sur `shogen_s2/` corrigé et sur les lignes ajoutées de B-c : 0 ligne.
- **C-7 à C-10** : actes de l'orchestrateur, non exécutés ici : C-7 (README, compte re-mesuré au commit ; 229 mesurés sur `1a63d80` et le lot corrigé), C-8 (inventaire D.1, rôle de l'instance G1 de ce lot, gabarit des commandes qui lisent ADR-0025), C-9 (lignes datées et plan de commits a1, a2, b, c), C-10 (ratifications et items). Mesures et propositions, hors dépôt : `F:/tmp/shogen-lots/B/correction-rapport.md`.
- **Observation** : la docstring de `TestSensibiliteG2` cite un chemin sous `F:/tmp` (`mutants_def_g2r.py` du réviseur) ; la revue laisse à l'orchestrateur la faculté de le remplacer par « revue G2 du lot B, §8 », sans effet sur les tests ni sur les épingles ; texte exact de la liste fermée, conservé.
- **Livrables de la correction** (`F:/tmp/shogen-lots/B/`) : `lot.diff` régénéré (lot entier contre la base empilée, ce journal compris ; `git --no-optional-locks diff`, les trois fichiers neufs déjà en intention d'ajout) ; `lot-G1-86b01b68.diff` (le `lot.diff` revu, conservé) ; `B-c.diff` ; `correction-rapport.md` ; `corr/` (copies, oracles). `G1-rapport.md` reste la version revue (sha256 `a093c3f5…acff5`) ; ce journal en diffère par la ligne de C-6 et cette section.
- **Attestation** (forme D.3) : pièces D.2 n° 1 à 9 non ouvertes ; ADR-0025 et la cartographie non ouvertes par cette instance ; le contrôle D.2 n° 5 et 6 des livrables passe par l'instrument du réviseur, `d2_check_g2r.py` (sha256 `8128128d…2047643`), qui repère les deux lignes par sha256 et n'imprime que numéros et comptes ; aucune copie scellée ; test nommé non affiché (la première ligne de sa docstring vue dans une sortie verbeuse de la suite, ligne de saut). Exposé aux valeurs d'ADR-0025 déc. 4 que ce journal liste au §4.7, reprises comme motif de la garde grep et nulle part ailleurs. Aucune statistique S2 calculée sur les journaux de campagne. Aucun z, aucun K, aucun P̂_more ni aucun φ de campagne vu.
