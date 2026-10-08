# Journal G1 — partie 2 de S2, étape B, sous-lots B3 à B5

**Nature de ce journal** : journal de provenance du worker de la session cloud, travail du 2026-10-02 de 04:54 à 05:47
UTC (horloge lue par `date -u` : 04:54:39 au départ, 05:41:05 avant la rédaction, 05:45:40 à la clôture). Contrat :
`docs/adr-0028/G0-partie-2.md`, section « B — RENDU-2 » (03:2x UTC) et ses deux ajouts datés (04:0x UTC ; 04:53 UTC :
B3 porte aussi SHOGEN-FMT-CONTEXTE-1). Branche `partie-2-rendu`, base `45b4493` (HEAD inchangé pendant le travail).
Aucune opération git en écriture sur le dépôt ; les seuls dépôts git écrits sont les dépôts jetables des tests, sous
un répertoire temporaire. Livrables : arbre de travail portant B3 et B4 (B4 coupé en B4a, B4b, B4c) ; **B5 rendu en
question, sans code** (§4) ; diffs `B3.diff`, `B4a.diff`, `B4b.diff`, `B4c.diff` dans le scratchpad de la session
(`…/scratchpad/lot-B2/`) ; ce journal.

## 0. Gate 0

Modèle résolu sous lequel le worker a tourné : **`claude-opus-5-5`** (identifiant exact fourni par l'environnement de
la session ; préfixe attendu `claude-opus-5-5` : conforme). Effort : `max` (fiche du worker et brief).

## 1. Provenance commune

### 1.1 Sources lues (toutes [lu] ; aucune [abs] ni [2nd])

- `CLAUDE.md` (racine, rappelé par la session).
- `docs/adr-0028/G0-partie-2.md` l.1-158, en entier (B : l.66-104 ; ajouts datés : l.147-158).
- `docs/adr-0028/ANNEXE-B-items.md` : l.30 (SHOGEN-TASK-72H-1), l.40-46 (dont l.42, SHOGEN-TORN-LINE-1), l.52 et l.108
  (SHOGEN-ORACLE-ENREG-1), l.318 (SHOGEN-D5-RECALCUL-TIERS-1), l.319 (SHOGEN-CENSURE-CAUSES-1), l.335-359 (blocs B.21 et
  B.22, en entier).
- `docs/adr-0028/ADR-0028-decisions-sortie-S2.md` : l.137-145 (§1 bis.5 à 1 bis.7, dont 1 bis.6) et l.190-207 (D6 (ii)
  à (viii) ; champs du schéma `shogen.oracle-record.v1` : l.205) ; lignes repérées par `grep -n` sur ce seul fichier.
- `docs/adr-0028/ANNEXE-A-lots.md` l.36-38 (RENDU-1, RENDU-2) et l.91-93 (B0 à B2) ; `ANNEXE-C-MAST.md` l.13-17 (FM-1.1,
  FM-2.4, FM-3.2, FM-3.3, FM-1.5) ; `ANNEXE-D-preenregistrement.md` l.28-60 (D.2 liste fermée, D.3) et l.107-151 (D.4) ;
  `G0-lot-D8a.md` l.190-197 (CH-4) et l.420-428 (items, dont SHOGEN-R1-FORME-RESOLUE-1).
- `docs/G1-partie-2-etape-B-1.md` l.1-369, en entier.
- Sources de B5 (§4.1) : `docs/G1-lot-D5-AMEND-descriptifs.md` l.50-62 et l.138-146, plus les lignes l.7, 39, 113, 136,
  152, 179-184 sorties d'un `grep -n` ciblé sur ce fichier ; `docs/G1-lot-B-SEG-1-segment.md` et
  `docs/G1-lot-B-SEG-2-bloc1.md` (lignes sorties d'un `grep -n -i` ciblé : démarrage, reprise, chunk, started_epoch,
  startup, sautée, trou, NUL, ordonnanceur ; B-SEG-1 l.21, 72, 163, 171 ; B-SEG-2 l.53, 69, 77, 101) ;
  `docs/adr-0024/ADR-0024-prolongation-campagne-S2.md` l.1-29, en entier ; `JOURNAL.md` l.43, l.44 et l.48 seulement
  (lignes des réparations, repérées par `grep -n -o` sur « REPAIR ») ; `docs/rapports/cartographie-2026-09-29.md`
  l.33-34 et l.36-50, par **lecture gardée** (§1.2) ; `docs/rapports/cartographie-2026-10-02.md` l.45 (seule ligne
  sortie d'un `grep` ciblé) ; `s2-harness/RUNBOOK-campagne.md` l.40-100.
- Code : `s2-harness/shogen_s2/r1.py` l.1-70, l.296-420, l.500-784 ; `report.py` l.1-270, l.386-478, l.739-771 ;
  `records.py` l.1-399 (en entier) ; `collector.py` l.1-252 (en entier) ; `run_campaign.py` l.1-120 et l.150-349.
- Tests : `test_d5_amend.py` (en entier), `test_contexte_decimal.py` (en entier), `tests/__init__.py`,
  `test_exclusion.py` l.30-70 et l.261-304, `test_rendu_blocs.py` l.47-80 et l.146-148, `test_critere.py` l.63-86,
  `test_run_campaign.py` l.1-80 et l.196-245.
- Gates : `xtask/src/sg4.rs` l.1-140, `xtask/src/sg5.rs` l.1-200, `xtask/src/documents.rs` l.75-135 ;
  `.github/workflows/gates.yml` l.8-23 et l.138-176 (job `s2-harness-unittest`) ; `.gitattributes` (en entier) ;
  `enforcement/gate-secrets.sh` l.1-60 (motifs, rejoués sur les fichiers neufs : 0 occurrence).
- Bibliothèque standard : `/usr/lib/python3.11/_pydecimal.py` l.1041-1092 (`__str__` : lettre de l'exposant lue dans
  `context.capitals`, l.1089).
- Scratchpad : `regle_fixtures.py` (sha256 `5557fb56…`) et `render_fixture.py` (`4084c42b…`), imposés par le brief et
  utilisés tels quels ; `lot-B/outils/faire_diff_b.py` (`1d7e4b56…`), recopié à l'identique en
  `lot-B2/outils/faire_diff.py`.

### 1.2 Pré-enregistrement (annexe D)

- D.4 a : fixtures seulement (collecteur et driver réels sur horloge factice, dépôts git jetables) ; aucun journal de
  campagne lu.
- D.2 : aucune pièce ouverte. `docs/rapports/cartographie-2026-09-29.md` a été lue par un script gardé
  (`lecture_gardee.py`) qui repère la ligne interdite par son sha256 (`5cc89b56…`, D.2 pt 5), sans l'afficher, puis
  n'imprime que des lignes autres : il a repéré **l.51** et ne l'a jamais imprimée ; lignes affichées : l.33-34, l.36-50
  (plages admises par D.2 pt 5). ADR-0025 n'a pas été ouverte. Aucun `grep` large sur `docs/` : recherches limitées
  aux fichiers nommés au §1.1, plus un `grep -n` des noms du schéma (`static_only`, `served_from`, `oracle-record`,
  `CA-12`) sur `docs/adr-0028/*.md` (ADR-0028 et ses annexes, non interdites par D.2), `docs/PASSATION-CLOUD.md`,
  `docs/METHODE-PARTIES.md` et `.claude/agents/*.md` (lignes sorties : ADR-0028 l.143, 202-207 ; annexes A l.38, B l.52,
  l.108, l.318, C l.16 ; G0-lot-D8a l.424 ; G0-partie-2 l.70, 91, 94 ; PLAN-PARTIE-2 l.24 ; PASSATION-CLOUD l.84), et
  un `grep -n` de « HS2-04 » sur quatorze fichiers nommés (dont `ANNEXE-E-avis-non-suivis.md` et `PARTIES-S2.md`, sans
  sortie). La copie de `JOURNAL.md` présente dans le scratchpad n'a pas été ouverte.
- Exposition déclarée (D.3, FM-2.4) : comptes de fenêtres perdues par incident et durées de trous (cartographie l.34,
  l.47, l.49 ; ADR-0024 l.9-11) ; comptes de lignes excisées et de fenêtres (JOURNAL l.43-44, l.48). Aucun taux par
  source, aucun z, K, P̂ ni φ. Ces chiffres n'entrent dans aucun code ni test.
- `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée : `env | grep -c` rend 0 au départ et à la fin ; le moteur de mutants la
  retire de l'environnement de ses sous-processus ; un seul test passe la clé dans un **mapping** à une fonction pure
  (`consigne`, §3.2), qu'aucun processus ne reçoit.

### 1.3 Outils écrits (scratchpad `lot-B2/outils/`, sha256)

`lecture_gardee.py` `6a3fa303…` ; `mutants.py` `2f0dcc09…` (copie de l'arbre, une mutation textuelle dont l'ancien
texte doit figurer une fois exactement, tests nommés, variable scellée retirée) ; `mutants_b3.py` `5dc1aa89…` ;
`mutants_b4a.py` `07092c80…` ; `mutants_b4b.py` `1ea0ff01…` ; `mutants_b4c.py` `67b6cf8c…` ; `signatures_b5.py`
`7ff4ec7a…` ; `faire_diff.py` `1d7e4b56…`. Brouillon mis de côté (§6, E3) : `brouillons/oracle_record-B4a-brouillon.py`
`70dd761a…`.

### 1.4 État de départ (arbre `45b4493`, exporté par `git archive` dans `lot-B2/arbres/HEAD`, égal à l'arbre de travail)

- Suite : `Ran 328 tests in 25.825s`, `OK (skipped=2)`.
- `cargo --locked xtask verify` : `=== VERDICT GLOBAL : VERT ===`, rc 0 (`preuves/verify-depart.out` `83e6d078…` ;
  S-G4 74 fichiers sur 74, S-G5 75 sur 75, 252 fragments contrôlés, corpus complet, 125 artefacts sur 125).
- Règle scellée SHOGEN-CRITERE-R1-1 : `regle_fixtures.py` sur `HEAD`, 16 entrées, sha256 `ea3a2d94…` (= référence).
- Rendus épinglés (`render_fixture.py`) : sans option `37dfcacb…`, avec option `7b6059f5…` (= épingles en vigueur).

## 2. B3 — SHOGEN-D5-RECALCUL-TIERS-1 et SHOGEN-FMT-CONTEXTE-1

### 2.1 Construction (décisions du G0 appliquées)

- `r1.recompute_d5_from_journal(control_path, journal_path, exclude_ranges=(), segment=None)` (r1.py l.787) : appelle
  `recompute_from_journal` (garde §5.3, filtre de lecture `records.filtre_lecture`, R1), relit les marqueurs du
  journal entier, normalise les plages par `records.exclusion_ranges` (comme le rendu), lit la portée du segment au 4e
  terme de `filtre_lecture`, puis rend deux clés : `fenetres_sautees` = s par strate, par `r1.fenetres_sautees` sur
  les marqueurs du journal entier, `strate_calendar` et w de `run_params`, la portée et les plages ; `bornes_censure`
  = par strate de R1, None si z_s n'est pas publiée (garde §5.4), sinon `r1.bornes_censure` avec n, K, P̂_more, s et
  σ̂²_bloc si z_bloc est publiée. Ce sont les appels des blocs 1 et 3 du rendu (report.py l.244 et l.461-470), dans le
  même ordre.
- `report._fmt_dec` écrit sous `localcontext(CONTEXTE_DECIMAL)` (report.py l.72-77) : la lettre de l'exposant suit
  `capitals = 1` du contexte nommé, jamais celui de l'appelant.

### 2.2 Tests

1. `tests/test_d5_amend.py::TestRendu::test_recalcul_tiers_d5_egal_au_rendu` (6 sous-tests) : sur la fixture RF du lot
   D5-AMEND (collecteur réel, rangs 0-239 puis 250-269) et sur la fixture « week-end entier sauté », égalité entre les
   valeurs servies (`recompute_d5_from_journal`, écrites par `_fmt_dec`) et celles lues dans le rendu (s du bloc 1 ;
   s, z_bas, z_haut, z_bloc_bas, z_bloc_haut du bloc 3), même journal, mêmes options. Attendus de s écrits à la main
   depuis la géométrie des fixtures, indépendants du code : sans option `{stress: 10}` (trou des rangs 240-249) ; même
   chose à ℓ = 2 par la couture (z_bloc publiée, variante σ̂_bloc) ; plage `[rang 245 + 0,5 ; rang 252]`, normalisée à
   `[245 ; 252]` comme au rendu : `{stress: 5}` (rangs 240-244) ; plage `[rang 250 ; rang 300]`, qui retire les 20
   marqueurs d'après le trou : `{stress: 10}` (portée du journal entier, `[rang 0 ; rang 270)`) ; segment
   `[rang −5 ; rang 255)` : `{calme: 5, stress: 10}` ; week-end : `{calme: 23, stress: 48}`, calme sous la garde
   (bornes None). Puis, à s = 0 (calme, sans option) : z_bas = z_haut = z_s de `recompute_from_journal`, z_bloc_bas
   None.
2. `tests/test_contexte_decimal.py::TestContexteDecimalNomme::test_fmt_dec_sous_capitals_0` : sous `capitals = 0`
   ambiant, `_fmt_dec` rend `2E-75`, `-1.5E+7`, `0` (pour `0E-69`), `0.25`, `-` ; contexte ambiant intact (même objet,
   capitals 0). Attendus : règle `__str__` de `_pydecimal.py` l.1041-1092 (exposant ajusté, lettre l.1089).

Échec avant (tests B3 ajoutés au code de `45b4493` : `preuves/B3-avant.out` `b165018d…`) : `FAILED (failures=1,
errors=7)` — `AttributeError: module 'shogen_s2.r1' has no attribute 'recompute_d5_from_journal'` (6 sous-tests et
l'assertion finale) ; `Lists differ: ['2e-75', '-1.5e+7', '0', '0.25', '-'] != ['2E-75', '-1.5E+7', '0', '0.25', '-']`.
Succès après : `Ran 2 tests … OK`.

### 2.3 Mutants (`mutants_b3.py`, `preuves/B3-mutants.out` `31030806…`) : 10 tués sur 10

D1 s sur les marqueurs filtrés (tué par la plage `[250 ; 300]`) ; D2 s sans la portée du segment ; D3 s sans les
plages ; D4 plages non normalisées (borne fractionnaire : `TypeError` dans `fenetres_sautees`) ; D5 bornes à s = 0 ;
D6 variante σ̂_bloc absente (tué à ℓ = 2) ; D7 variante σ̂_bloc sans z_bloc publiée ; D8 bornes sous la garde §5.4 ;
F1 `_fmt_dec` hors contexte nommé ; F2 `_fmt_dec` sous copie du contexte appelant.

### 2.4 Règle, rendus, suite, taille

- Règle : 16 entrées, `ea3a2d94…`, `cmp` identique à l'octet au JSON de `HEAD` (`regle/B3.json`).
- Rendus épinglés : `37dfcacb…` et `7b6059f5…`, identiques à l'octet (`cmp`) : aucune re-capture.
- Suite : `Ran 330 tests in 26.446s`, `OK (skipped=2)` (328 + 2).
- Numstat (`preuves/B3-numstat.out`) : r1.py +16 −0 ; report.py +4 −2 ; test_contexte_decimal.py +11 −1 ;
  test_d5_amend.py +40 −1 ; total +71 −4 = **75 lignes**.

## 3. B4 — SHOGEN-ORACLE-ENREG-1 (coupe en trois sous-lots)

### 3.1 Construction (`s2-harness/tools/oracle_record.py`, bibliothèque standard seule)

- **Écriture** (`enregistrer`) : sha complet du commit par `git rev-parse --verify <rev>^{commit}` ; extraction par
  `git archive --format=tar <sha>` dans un répertoire temporaire, `tarfile` avec le filtre `data` ; sha256 de chaque
  fichier extrait ; commandes de la **liste fermée** `COMMANDES = {suite}` lancées par listes d'arguments, jamais par un
  shell : `suite` = `[python, -B, -m, unittest, discover, -s, tests, -t, ., -v]` dans `s2-harness/` de l'extraction (la
  commande du job `s2-harness-unittest`, gates.yml l.172-176, sous l'interpréteur de l'enregistreur) ; sortie de chaque
  commande (stdout et stderr) écrite dans le répertoire passé en argument, hachée ; enregistrement écrit à côté.
- **Champs** : `schema` (`shogen.oracle-record.v1`), `role` (G1, G2, cp-2, rendu), `auteur` (tel que fourni), `tree`
  (`commit` sha complet, `extraction` = `git archive <sha>`, `sha256` par fichier), `base` (sha complet ou null),
  `static_only` false, `served_from` null, `python` (`sys.version`), `env` (SHOGEN_S2_CAMPAGNE_CONTROL, PYTHONHASHSEED,
  PYTHONPATH : valeur ou null), `runs` (`nom`, `arbre`, `commande`, `sortie` {`chemin` relatif au répertoire de
  l'enregistrement, `sha256`}, `exit`, `tests_avec_variable` : identifiants lus dans la sortie `-v` si la variable est
  posée, sinon liste vide), `exit` (0 si chaque commande sort 0, sinon 1), `ecrit` (ISO UTC à la seconde), `paquet`
  {`sha256`} et `sceau` {`genTime`} : exigé (64 hex) et facultatif au rôle « rendu », nuls hors de ce rôle (sinon
  refus avant toute écriture).
- **Nom** : `shogen-<7 premiers hex>-<rôle>-<AAAAMMJJTHHMMSSZ>-<pid>.json` (sans deux-points : valable sous Windows) ;
  sorties `<nom>.<i>-<commande>.out` ; ouvertures exclusives (`x`), jamais d'écrasement.
- **Lecture** (`verifier`, mode `--verifier`) : refus nommé `refus (<contrôle>) : …`, au premier contrôle non conforme,
  dans cet ordre : champs (clés exactes à chaque niveau), schema, rôle attendu, tree.commit égal au sha complet attendu
  (égalité exacte, jamais un préfixe), static_only false exact, exit (0 entier, au premier niveau et pour chaque
  commande ; au moins une commande), sortie (fichier présent et sha256 recalculé égal), paquet.sha256 (rôle « rendu »)
  ou nuls hors rendu, served_from (null, ou chemin et sha256 d'un enregistrement qui passe les mêmes contrôles, même
  rôle, même commit).
- **CLI** : écriture `--role --auteur --depot --commit --sortie [--base] [--commande] [--paquet-sha256]
  [--sceau-gentime]` ; lecture `--verifier ENREGISTREMENT --role R --commit SHA_COMPLET` ; codes 0 (écrit et vert, ou
  conforme), 1 (une commande a échoué), 2 (refus) ; options d'écriture mêlées à `--verifier` refusées.

### 3.2 B4a — écriture (bibliothèque)

- Tests (`tests/test_oracle_record.py`, dépôt git jetable de deux commits : test vert, puis test rouge) :
  `test_enregistrement_champs_et_sha` (rôle G2, commit court : enregistrement entier comparé à un attendu écrit à la
  main, sha256 des fichiers recalculés depuis les octets du test, sha complet de `git rev-parse`, sortie hachée et
  contenant `test_a (tests.test_t.T.test_a) ... ok`, nom de fichier) ; `test_rendu_base_echec_et_refus` (rôle rendu sur
  le commit rouge, base courte résolue, exit 1 ; sept refus sans écriture) ; `test_consigne_et_tests_lances` (fonctions
  pures : mapping ; sorties `-v` de 3.11 et de forme antérieure).
- Échec avant (tests ajoutés à l'arbre B3, outil absent : `preuves/B4a-avant.out` `7e5bafb1…`) : `FileNotFoundError`
  au chargement de `tools/oracle_record.py`. Succès après : `Ran 3 tests … OK`.
- Mutants (`mutants_b4a.py` sur l'arbre B4a, `preuves/B4a-mutants.out` `f423c632…`) : **20 tués sur 22** (W1 à W20 :
  autre commit extrait, sha d'un fichier faux, commande hors liste, sortie non hachée, static_only vrai, variable non
  consignée, tests comptés avec la variable, exit forcé à 0, base non résolue, garde du rôle rendu retirée, format hex,
  nuls hors rendu non gardés, liste fermée ouverte, rôle hors liste, genTime rempli, nom de fichier, format de `ecrit`,
  docstring lue comme test, identifiant non complété, variable absente consignée vide). Vivants à B4a : **W21**
  (écrasement admis, `wb` au lieu de `xb`) et **W22** (extraction sans filtre `data`) ; tués à B4c (§3.4).
- Mesure d'un risque de poste (`preuves/B4-autocrlf.out` `8670d091…`) : sous un `HOME` dont la configuration git porte
  `core.autocrlf = true` (défaut de Git pour Windows), `git archive` réécrit les fins de ligne du dépôt jetable et
  `test_enregistrement_champs_et_sha` échoue ; la fixture pose `core.autocrlf = false` dans son dépôt (une ligne) :
  vert sous ce même `HOME`. Le dépôt réel n'est pas touché par ce risque (`.gitattributes` : `* text=auto eol=lf`).
- Numstat : tools/oracle_record.py +95 ; tests/test_oracle_record.py +105 ; total **200 lignes** (plafond atteint).
- Suite : `Ran 333 tests`, `OK (skipped=2)` (330 + 3).

### 3.3 B4b — lecture (`verifier`)

- Test : `test_verifier_un_refus_nomme_par_controle` : trois enregistrements conformes acceptés (G2, rendu,
  served_from conforme), puis 17 copies modifiées, chacune refusée sous le nom de son contrôle (champs ×2, schema,
  rôle, tree.commit ×2 dont sha court, static_only à 0, exit ×4 dont `false` JSON, commande en échec sous exit 0 et
  liste vide, sortie ×2, paquet.sha256 à 63 hex, genTime hors rendu, served_from ×2 dont enregistrement servi non
  conforme).
- Échec avant (`preuves/B4b-avant.out` `d6809809…`) : `AttributeError: module 'oracle_record' has no attribute
  'verifier'`. Succès après : `Ran 4 tests … OK`.
- Mutants (`mutants_b4b.py`, `preuves/B4b-mutants.out` `829db8dc…`) : **16 tués sur 16**, chacun par le seul sous-test
  de son contrôle (`failures=1`) : V1-V2 champs, V3 schema, V4 rôle, V5 tree.commit par préfixe, V6 static_only par
  fausseté, V7-V10 exit (premier niveau, commandes, `false` admis, aucune commande), V11-V12 sortie (sha, présence), V13
  paquet.sha256 sans format, V14 nuls hors rendu, V15-V16 served_from (sha, conformité du servi).
- Numstat : outil +50 ; tests +38 ; total **88 lignes**. Suite : `Ran 334 tests`, `OK (skipped=2)`.

### 3.4 B4c — CLI et durcissement

- Code : `main` (écriture et `--verifier`), variables `GIT_*` retirées de l'environnement de `git` (un `GIT_DIR` hérité
  désignerait un autre dépôt), rejet du filtre `data` converti en refus nommé.
- Tests : `test_cli_ecriture_verifier_et_git_dir_herite` (écriture CLI sous un `GIT_DIR` qui désigne un autre dépôt
  jetable ; `--verifier` conforme, code 0 et message ; refus `tree.commit`, code 2, préfixe `oracle_record : refus` ;
  options mêlées, code 2 ; écriture sans `--sortie`, code 2 ; commit inconnu, code 2, rien d'écrit ; commande en échec,
  code 1) ; `test_collision_sans_ecrasement_et_lien_sortant` (horloge figée par `mock` : seconde écriture même instant,
  même pid, `FileExistsError`, sortie de la première intacte ; commit portant un lien symbolique absolu posé par la
  plomberie git, sans lien sur le disque : refus nommé, rien d'écrit).
- Échec avant (`preuves/B4c-avant.out` `6fe25c5b…`) : `FAILED (failures=1, errors=1)` — sortie vide de la CLI absente ;
  `tarfile.AbsoluteLinkError` non nommée. Succès après : `Ran 6 tests … OK`.
- Mutants (`mutants_b4c.py`, `preuves/B4c-mutants.out` `afd812f4…`) : **12 tués sur 12** (X1 `GIT_*` gardées, X2 = W21,
  X3 = W22, X4 refus du filtre non nommé, X5-X12 : codes et messages de la CLI, options mêlées, échec git non capturé,
  commande par défaut, `--sortie` exigée). Rejouées sur l'arbre final : B4a **22 sur 22**, B4b 16 sur 16
  (`preuves/B4ab-mutants-sur-B4c.out` `afd4f8e7…`).
- Numstat : outil +41 −3 ; tests +68 −8 ; total **120 lignes**. Suite : `Ran 336 tests in 28.422s`, `OK (skipped=2)`.

### 3.5 Règle, rendus

`shogen_s2/` n'est touché par aucun sous-lot B4. Règle : `ea3a2d94…` sur les arbres B4a, B4b, B4c et l'arbre final
(`regle/B4a.json`, `B4b.json`, `B4c.json`, `final.json`). Rendus : `37dfcacb…`, `7b6059f5…` partout : aucune re-capture.

## 4. B5 — SHOGEN-CENSURE-CAUSES-1 : question rendue, aucun code

### 4.1 Sources (§1.1) et définition de HS2-04 lisible au dépôt

HS2-04 n'est défini en clair dans aucune ligne lisible du dépôt (sa source, `harnais-s2.md`, n'est pas versionnée ;
recherche gardée de la cartographie : seules l.33, l.34, l.49 répondent, l.51 jamais affichée). Ce que le dépôt en dit :
« lignes NUL » comme classe de défaut des journaux réels (annexe C l.15) ; « isolement d'une ligne NUL non finale à la
reprise » (SHOGEN-TORN-LINE-1, annexe B l.42) ; le lecteur « ne traite pas les boucles NUL » (G1 de D5-AMEND l.57) ;
mécanisme : « ligne NUL non finale → lecteur qui refuse de lire → boucle de relance » (cartographie l.34, l.49).

### 4.2 Signatures lisibles dans un journal réparé et scellé

1. **Démarrages** : `run_params` et `clock_check` de phase « startup » sont écrits à **chaque appel** de
   `collector.collect` (collector.py l.149, l.224, l.227), donc à chaque chunk de `run_campaign.run_segment` (l.222,
   l.253-276) ; ADR-0024 l.17 : « réécrit par le driver à la relance et à chaque chunk » ; test existant
   `test_two_chunks_distinct_windows_and_concordant_run_params` (deux chunks, deux `run_params`). Un démarrage marque
   donc un chunk **ou** une reprise du processus ; aucun champ ne distingue l'un de l'autre (pas d'identité de
   processus), seul l'horodatage diffère.
2. **Marqueurs** `window_close` (window_start, harness_ts) et relevés `asn_attribution` (ts, un jeu par chunk).
3. **Lignes NUL** : **absentes** du journal réparé. Les réparations les ont excisées, « 0 NUL » après chacune (JOURNAL
   l.43, l.44 ; l.48 : « 5 lignes NUL excisées »). Le lecteur B1 refuse d'ailleurs une ligne illisible non finale.
   Pendant la boucle, le driver refuse au démarrage (`distinct_completed`, l.246) **avant toute écriture**, et le
   wrapper relance toutes les 30 s (RUNBOOK l.56-65) : la boucle ne laisse aucun enregistrement.
4. **Limite d'exécution de tâche** (72 h, code `0x41306`) : aucun enregistrement (G0 ; cartographie l.34, l.47 ;
   annexe B l.30) ; source hors journal : journal d'événements de l'ordonnanceur du poste local.

### 4.3 Mesure sur fixtures (`signatures_b5.py`, `preuves/B5-signatures.out` `6d1e2f5c…`)

Driver réel, horloge factice, lectures gelées, ASN simulé : (1) un processus, trois chunks : trois `run_params`, trois
`clock_check` ; (2) arrêt puis reprise dix fenêtres plus tard : mêmes types d'enregistrements, seul l'horodatage
diffère ; (3) ligne NUL non finale : refus au démarrage (`ligne JSON corrompue NON finale … (ligne 7)`), taille de
`control.jsonl` inchangée ; (4) après excision : 0 octet NUL, lecture normale ; (5) un chunk dont la lecture déborde :
fenêtre sautée **entre deux marqueurs d'un même démarrage** (harnais vivant) ; (6) deux chunks d'un même processus dont
la mesure ASN déborde : fenêtre sautée **entre deux démarrages**, harnais vivant, structure identique au cas (2).

### 4.4 Pourquoi la construction n'est pas codée

La construction de l'item suppose que les démarrages marquent les arrêts et reprises du harnais, et que les lignes NUL
se comptent au lecteur. Sur un journal réparé écrit par `run_campaign`, les deux prémisses tombent : (i) une seule cause
a une signature mécanique, la fenêtre sautée entre deux marqueurs d'un même démarrage (harnais vivant, cas 5) ; (ii)
hors de la portée d'un démarrage, le journal ne sépare pas un arrêt (coupure, limite de tâche, boucle NUL, redémarrage)
d'un passage entre deux chunks d'un processus vivant (cas 6 contre cas 2) : imprimer « arrêt du harnais, cause non
attribuée par le journal » pour toutes ces fenêtres affirmerait un arrêt là où le harnais tournait ; (iii) « boucles
NUL » n'a plus de signature après réparation. Les signatures ne suffisent pas à la ventilation demandée : conformément
au brief, aucune signature n'est inventée et la question est rendue (Q1, §8).

### 4.5 Options pour la décision (prix [inféré])

- (a) Deux lignes par strate au bloc 1, sur la seule signature mécanique : « entre deux marqueurs d'un même démarrage
  (harnais vivant) » ; reste : « hors de la portée d'un démarrage : arrêt du harnais ou passage entre deux démarrages
  (`run_params` réécrit à chaque chunk), cause non attribuée par le journal », sources hors journal nommées (journal
  d'événements de l'ordonnanceur ; JOURNAL l.43-48 et notes REPAIR pour les boucles NUL). Décision annexe : les
  fenêtres entre `started_epoch` et le premier marqueur d'un démarrage (l'item dit « de started_epoch au dernier
  marqueur » pour la portée, et « entre deux marqueurs » pour le harnais vivant). Environ 30 lignes de code, 40 de
  tests, une re-capture des deux épingles.
- (b) (a) plus un seuil de temps pour lire un passage entre chunks (par exemple `started_epoch` du démarrage k+1 moins
  `harness_ts` du dernier marqueur du démarrage k inférieur à w) : paramètre neuf, à écrire au paquet avant le
  scellement.
- (c) Aucun code : la ligne reste « toutes causes confondues » (H_perte) ; limite écrite au paquet ; ventilation
  reportée aux collectes futures, avec une identité de processus dans `run_params` (collecte en quarantaine : G0 neuf,
  D6 vi).

## 5. Empreintes

- Diffs (étiquettes `a/s2-harness/…`, `b/s2-harness/…`, sans opération git) : `B3.diff`
  `39b0322a8c7b578197f2807b97167e961014d2997f650a778766139116ffac58` (par rapport à `45b4493`) ; `B4a.diff`
  `01152441061c6a8b3a68b7931fd405a7a19c3ba375745227415909a68dc71440` (par rapport à B3) ; `B4b.diff`
  `9252e2a3d3d73274de752b6187080986b5d8234578bc92eb5ae64fc21330a77c` (par rapport à B4a) ; `B4c.diff`
  `2efab7d54fc9ff235d1e7de8d3570cbdb2ff63d2e3826268db65783032e94013` (par rapport à B4b). Pas de `B5.diff` (§4).
  Contrôle : export de `45b4493` par `git archive`, `patch -p1` de B3, B4a, B4b, B4c, `diff -r` avec l'arbre de
  travail : identique.
- Fichiers finaux (sha256) : `shogen_s2/r1.py` `9814e6c49939b9e385051c0871d528fda1f4fdb0dd5bf0e8c5eb0a30d6d24298` ;
  `shogen_s2/report.py` `34ff4d03c56661d82bed2d4f85befdad20b944857ad099d904e3b636043cb518` ;
  `tests/test_contexte_decimal.py` `2d02f50b80a00a9dbe3ddfef42ecef13e334c785017c4c9a51684e753d3f7b0b` ;
  `tests/test_d5_amend.py` `5a2e29739e04254910e8ba07c751c681e16242db99271bdfff8454206b6d2a68` ;
  `tests/test_oracle_record.py` `2b1d9c09b647af5c08da978ae1c79899eb8621337a0f7c4eddb6f082cdbc01dc` ;
  `tools/oracle_record.py` `841f6fdab83a4b2982c191e966d787edc75a6193a080cf32588e50bd0744f244`.
- `git status` final : modifiés r1.py, report.py, test_contexte_decimal.py, test_d5_amend.py ; neufs
  `tests/test_oracle_record.py`, `tools/oracle_record.py`, ce journal.
- Suites recomptées : 328 → 330 (B3) → 333 (B4a) → 334 (B4b) → 336 (B4c), deux sauts à chaque pas (les deux tests
  de la variable scellée).

## 6. Écarts au G0

- **E1 (B4, coupe)** : B4 coupé en B4a (écriture), B4b (lecture), B4c (CLI et durcissement), chacun sous 200 lignes ;
  B4a atteint exactement 200 lignes.
- **E2 (B4a)** : deux mutants vivants à B4a (W21, W22), tués par les tests de B4c, rejoués sur l'arbre final.
- **E3 (B4a, ordre de rédaction)** : un premier état de l'outil a été écrit avant ses tests ; il a été retiré de
  l'arbre (`brouillons/oracle_record-B4a-brouillon.py`), les tests écrits, l'échec montré sur l'arbre sans outil, puis
  l'outil remis et retravaillé.
- **E4 (B4, serrages)** : au-delà des cinq contrôles nommés, le `--verifier` contrôle les champs, le schéma, le sha256
  recalculé de chaque sortie **pour tout rôle**, les champs nuls hors rendu, l'exit de chaque commande, et refuse
  `false` pour 0 et un sha court ; l'écriture refuse paquet.sha256 ou genTime hors rendu, n'écrase jamais, retire les
  variables `GIT_*`, extrait sous le filtre `data`.
- **E5 (B4, served_from)** : l'écriture pose toujours null (chaque réviseur lance ses propres commandes) ; la lecture
  exige du servi les mêmes contrôles, **même rôle et même commit** (lecture la plus stricte de « conforme »).
- **E6 (B4, env et genTime)** : `env` consigne trois variables (la variable scellée, PYTHONHASHSEED, PYTHONPATH) ;
  au rôle « rendu », genTime est facultatif (voie sans ancre de D.4 b (6)).
- **E7 (B3, tests)** : test placé dans `TestRendu` de `test_d5_amend.py` (fixture RF réutilisée), avec une borne
  fractionnaire pour tenir la normalisation des plages ; aucun champ de portée n'est rendu par la fonction.
- **E8 (B5)** : aucun code ; question rendue (§4).

## 7. Limites rencontrées (items à former, règle PAROXYSME)

- **L1 — champs D5 de l'enregistrement d'oracle (fin de SHOGEN-D5-RECALCUL-TIERS-1)** : la liste fermée ne contient
  que `suite` ; s_s et les bornes n'entrent dans un enregistrement que par la sortie d'une commande nommée du recalcul
  tiers (D.4 b : « l'oracle tiers `recompute_*` sur chaque sortie »), qui n'a pas d'interface de ligne de commande.
  Construction proposée : commande nommée `recalcul-tiers` (JSON de `recompute_from_journal` et de
  `recompute_d5_from_journal` par sortie), au sous-lot C3 [inféré : ≈ 25 lignes et 25 de tests].
- **L2 — tree.sha256 non relu** : `--verifier` ne recalcule pas les sha256 de l'arbre (il faudrait le dépôt) ; ils
  sont consignés, non contrôlés. Construction possible : option `--depot` du `--verifier`, ré-extraction et égalité.
- **L3 — branche « variable posée »** : testée sur fonctions pures seulement (mapping ; texte `-v`) ; aucun processus
  ne reçoit la variable (règle) ; `tests_avec_variable` d'une exécution réelle sous la variable n'est pas exercé.
- **L4 — format de `unittest -v`** : `tests_avec_variable` dépend du format de la sortie (3.11 et forme antérieure
  lues) ; un format futur viderait la liste sans erreur, sous-déclaration possible.
- **L5 — fins de ligne** : `tree.sha256` est celui de l'extraction sous la configuration git du poste ; sans attribut
  `eol`, deux postes peuvent différer (mesuré, §3.2) ; le dépôt réel fixe LF par `.gitattributes`.
- **L6 — `auteur` non contrôlé** : SHOGEN-R1-FORME-RESOLUE-1 (déclencheur « G0 de RENDU-2 », G0-lot-D8a l.424 ; CH-4 :
  égalité exacte avec `<id>` ou `<id>[1m]`, jamais un préfixe) n'est pas porté par le G0 §B ; l'outil écrit `auteur`
  tel quel, le `--verifier` ne le lit pas.
- **L7 — commandes sans délai maximal** : une commande bloquée bloque l'enregistreur, sans enregistrement écrit.
- **L8 — `capitals` hors `_fmt_dec`** : SHOGEN-FMT-CONTEXTE-1 couvre `_fmt_dec` (décision du G0) ; les autres écritures
  de valeurs de `report.py` n'ont pas été auditées pour `capitals`.
- **L9 — ventilation des pertes** (B5) : voir §4 et Q1.
- **L10 — arbre non commis** : l'enregistreur n'extrait qu'un commit (`git archive`) ; un enregistrement de rôle G1 sur
  un travail non commis (cas des workers, qui ne committent pas) n'est pas productible : il suppose le commit du lot par
  l'orchestrateur, puis l'enregistrement sur ce commit.

## 8. Questions ouvertes

- **Q1** (B5, §4.5) : option (a), (b) ou (c) pour SHOGEN-CENSURE-CAUSES-1, et, sous (a), le traitement des fenêtres
  entre `started_epoch` et le premier marqueur d'un démarrage.
- **Q2** (L1) : la commande nommée du recalcul tiers entre-t-elle à C3 (liste fermée de l'enregistreur étendue), ou en
  item daté ?
- **Q3** (L6) : SHOGEN-R1-FORME-RESOLUE-1 (contrôle exact d'`auteur`) entre-t-il dans un sous-lot de l'étape B ou C,
  et contre quelle liste blanche (celle de `enforcement/lint-model-pinning.sh`, une seule vérité) ?
- **Q4** (E5) : « served_from conforme » doit-il admettre un enregistrement servi d'un autre rôle ?
- **Q5** (L2) : le `--verifier` doit-il recalculer `tree.sha256` (option `--depot`), au cp-2 ?

## 9. Clôture

- Suite finale : `Ran 336 tests in 28.422s`, `OK (skipped=2)` ; `SHOGEN_S2_CAMPAGNE_CONTROL` absente
  (`env | grep -c` : 0).
- `cargo --locked xtask verify` lancé à 05:43 UTC avec ce journal dans `docs/` (version qui précède l'ajout du présent
  paragraphe et de L10) : `=== VERDICT GLOBAL : VERT ===`, rc 0 (`preuves/verify-final.out` `025ed79f…`) ; S-G4 :
  75 fichiers examinés sur 75 ; S-G5 : 76 sur 76, corpus complet (125 artefacts sur 125), 252 fragments contrôlés, 2 825
  écartés sous seuil, 0 violation. Relance sur la version finale : verdict et sha256 de ce fichier dans le rapport de
  remise à l'orchestrateur (un fichier ne porte pas son propre sha).
