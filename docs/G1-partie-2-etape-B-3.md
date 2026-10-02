# Journal G1 — partie 2 de S2, étape B, sous-lots B5 et B6

**Nature de ce journal** : journal de provenance du worker de la session cloud, travail du 2026-10-02 de 05:58 à 07:1x
UTC (horloge lue par `date -u` : 05:58:15 au départ, 06:47:26 avant la rédaction, 07:12:10 avant la clôture). Contrat :
`docs/adr-0028/G0-partie-2.md`, section « B — RENDU-2 » (l.66-104) et ses trois ajouts datés (l.147-164 ; le troisième,
05:56 UTC, fixe B5 et B6) ; annexe B l.319 (SHOGEN-CENSURE-CAUSES-1) et bloc B.23 (l.361-372 : décision option (a),
SHOGEN-ENREG-VERIF-1) ; `docs/G1-partie-2-etape-B-2.md` §3 (l.143-232) et §4 (l.234-294), relus, non refaits. Branche
`partie-2-rendu`, base `d4db81d` (HEAD inchangé pendant le travail). Aucune opération git en écriture sur le dépôt ;
seuls les dépôts jetables des tests, sous un répertoire temporaire, sont écrits. Livrables : arbre de travail portant B5
puis B6 (B6 coupé en B6a et B6b) ; diffs dans `…/scratchpad/lot-B3/` ; ce journal.

## 0. Gate 0

Modèle résolu sous lequel le worker a tourné : **`claude-opus-5-5`** (identifiant exact fourni par l'environnement de la
session ; préfixe attendu `claude-opus-5-5` : conforme). Effort : `max` (fiche du worker et brief).

## 1. Provenance commune

### 1.1 Sources lues (toutes [lu] ; aucune [abs] ni [2nd])

- `CLAUDE.md` (racine, rappelé par la session) ; `docs/PASSATION-CLOUD.md` l.1-273, en entier, après un `grep -n` de
  contrôle (ADR-0025, cartographie, l.51, l.14 : seules l.126-128 répondent, texte de règle).
- `docs/adr-0028/G0-partie-2.md` l.1-164, en entier.
- `docs/adr-0028/ANNEXE-B-items.md` l.312-372 (blocs B.19 à B.23, dont l.319) et la liste des titres de blocs
  (`grep -n`).
- `docs/adr-0028/ANNEXE-D-preenregistrement.md` l.30-43 (D.2, liste fermée) et l.107-125 (D.4 a, début de D.4 b), plus
  les titres et lignes sorties d'un `grep -n` sur `D\.2\|D\.4\|^#` (l.1, 3, 7, 24, 26, 28, 30, 44, 54, 107, 126,
  140, 143, 144, 152).
- `docs/adr-0028/ANNEXE-A-lots.md` l.38 et l.85-110 ; `docs/adr-0028/ADR-0028-decisions-sortie-S2.md` l.202-207 (D6
  viii, champs du schéma) et les lignes sorties d'un `grep -n` sur `oracle-record\|D6\b\|(viii)` ;
  `docs/adr-0028/G0-lot-D8a.md` l.188-198 (CH-4 : forme `<id>` ou `<id>[1m]` admise en journal de modèle résolu, par
  égalité exacte) et l.418-430 (items, dont SHOGEN-R1-FORME-RESOLUE-1).
- `docs/G1-partie-2-etape-B-2.md` l.1-381, en entier.
- Code : `s2-harness/shogen_s2/r1.py` l.45-55, l.380-420, l.690-800 ; `report.py` l.1-300 et les lignes d'un `grep -n` ;
  `records.py` l.1-399, en entier ; `collector.py` l.1-252, en entier ; `run_campaign.py` l.150-349 ; `window.py`
  l.1-139, en entier ; `tools/oracle_record.py` l.1-183, en entier.
- Tests : `test_d5_amend.py` l.1-433, en entier ; `test_exclusion.py` l.1-140 et l.155-200 ; `test_pool_analyse.py`
  l.1-40 et l.180-202 ; `test_bloc1.py` l.1-150 ; `test_sensibilite.py` l.1-80 ; `test_collector.py` l.60-110 et les
  lignes d'un `grep -n` (l.47-57) ; `test_oracle_record.py` l.1-203, en entier.
- Gates : `enforcement/lint-model-pinning.sh` l.1-160, en entier (liste blanche l.33 ; sortie de succès et d'échec
  l.152-160) ; `enforcement/hooks/pre-commit` l.15-60 (motif R-13, l.21) ; `enforcement/gate-secrets.sh` l.1-60 (motifs
  VENDOR et GENERIC) ; `xtask/src/sg4.rs` l.31-157 (locutions de S-G4, lignes d'un `grep -n`).
- Système : `timeout --help` (GNU coreutils de l'hôte), l.33 : code 124 quand la commande dépasse son délai.
- Scratchpad : `regle_fixtures.py` (`5557fb56…`) et `render_fixture.py` (`4084c42b…`), imposés par le brief et
  utilisés tels quels ; `lot-B2/outils/signatures_b5.py` et `lot-B2/preuves/B5-signatures.out` (relus, non relancés) ;
  `lot-B2/outils/mutants.py` (`2f0dcc09…`) et `faire_diff.py` (`1d7e4b56…`), recopiés à l'identique dans
  `lot-B3/outils/` ; `lot-B2/outils/mutants_b4a.py`, `mutants_b4b.py`, `mutants_b4c.py` (listes relues, rejouées au
  §3.4 sans modification de leurs fichiers).

### 1.2 Pré-enregistrement (annexe D)

- D.4 a : fixtures seulement (collecteur réel sur horloge factice, dépôts git jetables, journal synthétique de mesure de
  coût au §2.4) ; aucun journal de campagne lu, aucune copie scellée cherchée.
- D.2 : aucune pièce ouverte. `docs/rapports/cartographie-2026-09-29.md` n'a pas été ouverte, même par lecture gardée ;
  ADR-0025 n'a pas été ouverte ; `JOURNAL.md` n'a pas été ouvert. Recherches limitées aux fichiers nommés au §1.1.
- Exposition déclarée (D.3, FM-2.4) : par le journal G1 de B-2 (§4.2, relu), un compte de lignes excisées par une
  réparation ; rien d'autre. Aucun taux par source, aucun z, K, P̂ ni φ. Ce compte n'entre dans aucun code ni test.
- `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée : `env | grep -c` rend 0 au départ et après chaque suite ; les moteurs de
  mutants la retirent de l'environnement de leurs sous-processus.

### 1.3 Outils écrits (scratchpad `lot-B3/outils/`, sha256)

`mutants_b5.py` `a751181a…` ; `cout_v4.py` `9647081d…` (coût sur journal synthétique) ; `mutants_enf.py` `677cce97…`
(moteur de `mutants.py` dont l'arbre copié reçoit `enforcement/lint-model-pinning.sh` en voisin, disposition du dépôt) ;
`mutants_b6a.py` `011d90b6…` ; `mutants_b6b.py` `b34eb0ae…` ; `mutants_b4_sur_final.py` `d1a8a8d3…` (listes de B4 lues
dans `lot-B2/outils/`, cinq ancres déplacées par B6 remplacées par leur forme finale, mutation identique) ;
`faire_b6a.py` `7e368fc6…` (construit l'arbre intermédiaire B6a depuis l'arbre final) ; `reconstruire_b6.sh`
`123ef31d…` ; `rewrap_md_b3.py` `d86a1ee6…` (copie de `lot-B2/outils/rewrap_md.py` `6592c791…`, blocs clôturés laissés
intacts) pour la mise en page de ce journal, puis `lot-B2/outils/precheck_md.py` `1b46b7cb…` tel quel (locutions de
S-G4, citations d'allure anglaise, guillemets : aucun constat).

### 1.4 État de départ (arbre `d4db81d`, exporté par `git archive` dans `lot-B3/arbres/HEAD`, égal à l'arbre de travail)

- Suite : `Ran 336 tests in 30.318s`, `OK (skipped=2)` (`preuves/suite-depart.out` `9b9a0060…`).
- Règle scellée SHOGEN-CRITERE-R1-1 : `regle_fixtures.py` sur `HEAD`, 16 entrées, sha256 `ea3a2d94…` (= référence).
- Rendus épinglés (`render_fixture.py`) : sans option `37dfcacb…`, avec option `7b6059f5…` (= épingles en vigueur).

## 2. B5 — SHOGEN-CENSURE-CAUSES-1, option (a)

### 2.1 Construction (décision de l'orchestrateur appliquée, annexe B.23)

- `records.demarrages(path)` (records.py l.316) : relit `control.jsonl` dans l'ordre du journal (lecteur tolérant) ;
  un démarrage s'ouvre à chaque `run_params` **et** à chaque `clock_check` de phase `startup` (les deux sont écrits en
  tête de chaque appel de `collector.collect`, chunk ou reprise : l'un suffit si l'autre manque) ; rend le
  `window_start` des marqueurs `window_close` de chaque démarrage ; marqueurs écrits avant toute ligne de démarrage :
  hors de tout démarrage.
- `r1.fenetres_sautees_vivant(ws_journal, demarrages, spec, w, borne, ranges)` (r1.py l.734) : part « harnais vivant »
  des fenêtres sautées = fenêtres comptées par `fenetres_sautees` (mêmes marqueurs du journal entier, même portée,
  mêmes plages D5) qui tombent dans l'union des intervalles [premier marqueur ; dernier marqueur] des démarrages
  (bornes marquées, jamais sautées ; chevauchements comptés une fois). Aucun seuil de temps. Le calcul appelle
  `fenetres_sautees` sur chaque intervalle de l'union, avec les seuls marqueurs de l'intervalle (tranche par `bisect`) :
  même règle de grille, de plages et de strates que s_s.
- Rendu (report.py l.255-265) : juste après la ligne `fenetres_sautees`, pour chaque strate de cette ligne (strates du
  journal et strates sautées), deux lignes : `sautees_harnais_vivant` = part vivante ; `sautees_non_attribuees` = s −
  part vivante, libellé “arrêt ou passage entre démarrages, cause non attribuée par le journal (fenêtres entre
  started_epoch et le premier marqueur d'un démarrage comprises)” ; chaque ligne porte aussi
  `sur s = <s de la strate>`.
- `started_epoch` n'entre pas dans le calcul : une fenêtre entre `started_epoch` et le premier marqueur d'un démarrage
  n'est entre deux marqueurs d'aucun démarrage ; elle tombe donc dans la seconde ligne, comme la décision le demande.

### 2.2 Tests (`tests/test_censure_causes.py`, neuf, 4 tests)

Fixture : collecteur réel, w = 60, calendrier week-end, rang 0 = ven. 2026-08-07 22:00Z (rang 120 = sam. 00:00Z,
stress ; jours contrôlés par `datetime`). Cinq démarrages, dans l'ordre du journal : rangs 100-124 sauf 110, 121, 123 ;
départ au rang 127 + 30 s, rangs 129-135 sauf 132 ; départ au rang 140, rangs 141-143, ligne `run_params` excisée ;
départ au rang 150, rangs 152 et 154, ligne `clock_check` excisée ; départ au rang 120, rangs 120 et 122 (horloge qui
recule, portée incluse dans celle du premier). Un `clock_check` de phase `controle` est posé après le marqueur 109.
Attendus écrits à la main depuis cette géométrie (triplets part vivante, non attribuées, s) :

1. `test_vivant_entre_deux_marqueurs_reste_non_attribue` : sans option, calme (1, 0, 1) ; stress (4, 17, 21) — vivantes
   121, 123, 132, 153 ; non attribuées 125-128, 136-140, 144-151.
2. `test_plages_et_segment` : plages [110 ; 110], [122 ; 124], [154 ; 154] : calme (0, 0, 0), stress (3, 17, 20) ;
   segment [105 ; 128) : calme (1, 0, 1), stress (2, 3, 5).
3. `test_marqueurs_avant_tout_demarrage_et_week_end_sans_marqueur` : marqueurs 96 et 98 écrits en tête : calme (1, 2,
   3) ; fixture de `test_sensibilite` (w = 3 600, week-end entier sauté, strate stress sans marqueur) : calme (0, 23,
   23), stress (0, 48, 48) ; fixture des épingles, sans et avec PLAGE : quatre lignes à 0.
4. `test_somme_des_deux_lignes_egale_s` : valeurs lues dans le rendu (sans option, plages, segment) : part vivante + non
   attribuées = s de la ligne `fenetres_sautees`, et `sur s` = s, par strate.

Contrôle indépendant de la géométrie : les s de la ligne `fenetres_sautees` rendus par le code d'**avant** B5 (arbre
`HEAD`) sur ces fixtures égalent les s écrits à la main (calme 1 / stress 21 ; 0 / 20 ; 1 / 5 ; 3 / 21).

### 2.3 Échec avant, succès après

- Tests finaux ajoutés à l'arbre `HEAD` (`preuves/B5-avant.out` `e5b7698f…`) : `FAILED (failures=7, errors=1)` — lignes
  absentes du bloc 1 (la ligne qui suit `fenetres_sautees` est `devise_composition` ou `pool_analyse_retrait`).
- Après : `Ran 4 tests … OK`.

### 2.4 Mutants (`mutants_b5.py`, `preuves/B5-mutants.out` `01c5eb05…`) : 17 tués sur 18, un équivalent déclaré

Tués : R1 démarrage ouvert par `clock_check` seul ; R2 par `run_params` seul ; R3 `clock_check` de toute phase ; R4
marqueurs d'avant tout démarrage tenus pour un démarrage ; R5 journal entier tenu pour un démarrage ; V1 portées
chevauchantes non fusionnées ; V2 part vivante hors de la portée du segment ; V3 part vivante sans les plages ; V5
garde du journal vide retirée (tué par `test_bloc1.test_journal_sans_fenetre_dates_de_campagne_sans_lever`) ; V8 fin
d'union non étendue ; V9 dernier marqueur de l'intervalle retiré de la tranche ; P1 reste = s ; P2 part vivante sans
le segment ; P3 sans les plages ; P4 strates à marqueur seules ; P5 valeurs permutées ; P6 marqueurs filtrés (segment,
plages) pour la part vivante. **Vivant : V4** (tranche des marqueurs remplacée par tous les marqueurs), équivalent par
construction : `fenetres_sautees` filtre elle-même les marqueurs par la borne. La tranche ne sert que le coût, mesuré
sur un journal **synthétique** de 30 jours à w = 60 s, un démarrage par tranche de 10 fenêtres (`cout_v4.py`,
`preuves/B5-cout-v4.out` `5b10c9ea…`) : 0,055 s avec la tranche, 18,8 s sans, valeurs identiques.

### 2.5 Rendus et épingles (re-capture, diff textuel complet)

Rendus « avant » (arbre `HEAD`) = épingles en vigueur (`37dfcacb…`, `7b6059f5…`). Diff textuel complet
(`preuves/B5-rendus.diff` `d47cd18d…`, 26 lignes) : **insertions seules**, quatre lignes par rendu, juste après la
ligne `fenetres_sautees` (l.31 sans option, l.35 avec option) ; aucune ligne retirée ni modifiée. Les quatre lignes,
identiques dans les deux rendus :

```
  sautees_harnais_vivant   = « calme » : 0 sur s = 0 — sautées entre deux marqueurs window_close d'un même démarrage (run_params ou clock_check « startup », ordre du journal) : harnais vivant — SHOGEN-CENSURE-CAUSES-1
  sautees_non_attribuees   = « calme » : 0 sur s = 0 — arrêt ou passage entre démarrages, cause non attribuée par le journal (fenêtres entre started_epoch et le premier marqueur d'un démarrage comprises) — SHOGEN-CENSURE-CAUSES-1
  sautees_harnais_vivant   = « stress » : 0 sur s = 0 — sautées entre deux marqueurs window_close d'un même démarrage (run_params ou clock_check « startup », ordre du journal) : harnais vivant — SHOGEN-CENSURE-CAUSES-1
  sautees_non_attribuees   = « stress » : 0 sur s = 0 — arrêt ou passage entre démarrages, cause non attribuée par le journal (fenêtres entre started_epoch et le premier marqueur d'un démarrage comprises) — SHOGEN-CENSURE-CAUSES-1
```

Épingles re-capturées : `SHA_BASE_SANS_OPTION` (`tests/test_exclusion.py`) `37dfcacb…0c00a96` →
`4e62fbb8a4a7a29c0761c719c8f731a8247ef407be7a7a04c44219bd093c9a01` ; `SHA_BASE_AVEC_OPTION`
(`tests/test_pool_analyse.py`) `7b6059f5…e0dbf90` → `d079dd9d62a3f585a136779330cb21017a300ae853bef5cb63024bb6412de608` ;
historique des commentaires d'épingle complété (« puis au sous-lot B5 … avant … »).

### 2.6 Règle, suite, taille

- Règle : 16 entrées, `ea3a2d94…`, `cmp` identique à l'octet au JSON de `HEAD` (`regle/B5.json`).
- Suite sur l'arbre B5 : `Ran 340 tests in 30.206s`, `OK (skipped=2)` (336 + 4 ; `preuves/B5-suite.out` `9cadb1a6…`).
- Numstat (`preuves/B5-numstat.out`, recoupé par `git diff --numstat`, lecture seule) : r1.py +26 ; records.py +14 ;
  report.py +12 ; test_censure_causes.py +123 (neuf) ; test_exclusion.py +3 −2 ; test_pool_analyse.py +3 −2 ; total
  +181 −4 = **185 lignes**.

## 3. B6 — SHOGEN-ENREG-VERIF-1 (coupe en deux sous-lots : B6a, B6b)

B6 d'un seul tenant mesure 237 lignes (`B6.diff`, +207 −30) : coupé en **B6a** (i, ii) et **B6b** (iii), chacun sous
200. L'arbre B6a est construit depuis l'arbre final par `faire_b6a.py` (retrait textuel des parties du délai), puis
contrôlé : `B5 + B6a.diff + B6b.diff` = arbre final (§4).

### 3.1 Construction (`s2-harness/tools/oracle_record.py`, bibliothèque standard seule)

- (i) `liste_blanche()` (l.65) lit `LINT` = `enforcement/lint-model-pinning.sh` du dépôt de l'outil (chemin relatif à
  l'outil, l.33), sur l'**unique** ligne `ALLOWED='…'` ancrée en début de ligne ; lint illisible, ligne absente, répétée
  ou vide : erreur. Aucune liste n'est recopiée dans le code Python. Le `--verifier` (l.183-189), après le rôle, exige
  `auteur` chaîne égale à un identifiant de la liste, ou à cet identifiant suivi exactement de `[1m]` ; sinon, et si la
  liste est illisible : refus nommé `auteur`.
- (ii) `extraire()` (l.78) : l'extraction de l'écriture (`git archive`, filtre `data`, sha256 par fichier), mise en
  fonction et partagée ; `ecarts_arbre()` (l.90) : ré-extraction du commit attendu dans un répertoire temporaire,
  chemins dont le sha256 diffère, fichiers en trop ou en moins compris ; ré-extraction impossible : un écart qui la
  nomme. `verifier(chemin, role, commit, depot=None)` : avec un dépôt, refus nommé `tree.sha256` au premier écart
  (l.191-193) ; l'enregistrement servi (`served_from`) est contrôlé au même dépôt. CLI : `--depot` admis avec
  `--verifier` ; le message de conformité imprime la couverture (`tree.sha256 recalculé sur <dépôt>`, ou
  `non recalculé : --depot absent`).
- (iii) `DELAI_DEFAUT = 3600` s par commande (l.35 ; base déclarée : la suite mesurée ici dure ≈ 30 s, marge ×120 ;
  les commandes de C3 sur un journal de campagne ne sont pas mesurables avant l'exécution unique, D.4 a : le défaut
  est une garde contre le blocage, pas une borne de coût) ; argument `delai` de `enregistrer` et `--delai` de la CLI ;
  délai nul, négatif, infini ou NaN refusé avant toute écriture. Au dépassement : commande arrêtée, `exit` =
  `EXIT_DELAI` = 124 (convention de `timeout` de GNU coreutils, §1.1) consigné dans le run, ligne
  `[oracle_record] délai maximal de <d> s dépassé : commande arrêtée, exit 124` ajoutée en fin de sortie (hachée avec
  elle), enregistrement écrit quand même (exit 1, code CLI 1).

### 3.2 B6a — auteur et tree.sha256

- Tests (`tests/test_oracle_record.py`) : `test_verifier_auteur_liste_blanche_du_lint` — oracle indépendant de l'outil :
  la liste qu'imprime le lint lui-même (`bash enforcement/lint-model-pinning.sh` sur un arbre de fixture dont
  l'agent porte un tier nu : ligne « liste blanche : … (R-1). » de sa sortie d'échec ; `bash` résolu par
  `shutil.which`, dans l'ordre du PATH : sous Windows, `CreateProcess` chercherait d'abord dans System32, où peut se
  trouver le `bash.exe` de WSL ; bash ou lint absent : échec, jamais saut) ; admis : chaque identifiant et
  sa forme `[1m]` ; refusés `auteur` : l'identifiant banni (construit à l'exécution, comme dans le lint) nu et avec
  `[1m]`, un tier nu, un préfixe, un identifiant tronqué, la casse haute, `[1M]`, `[2m]`, `[1m][1m]`, un blanc avant
  ou après, `[1m]` seul, `null`, un entier ; lint de fixture (`mock` de `LINT`) : une autre liste la remplace (ligne
  `ALLOWED` en commentaire ignorée), ligne répétée ou lint absent : refus. `test_verifier_depot_recalcule_tree_sha256`
  — attendu : sha256 des octets écrits par le test ; refus `tree.sha256` sur un sha changé, un fichier en trop, un
  fichier en moins (copies acceptées sans dépôt), sur un dépôt sans le commit (« ré-extraction impossible ») ; servi
  altéré : accepté sans dépôt, refus `served_from` avec ; CLI avec `--depot` : code 0 et message de couverture exact,
  code 2 et refus nommé sur la copie altérée. `test_cli_ecriture_verifier_et_git_dir_herite` : message de conformité
  attendu complété de la couverture.
- Échec avant (tests B6a sur l'outil de l'arbre B5, `preuves/B6a-avant.out` `1e3b2e6b…`) : `FAILED (failures=15,
  errors=5)` — 14 formes d'`auteur` admises (`ValueError not raised`), `LINT` absent du module, `verifier()` à 3
  arguments, message sans couverture. Après : `Ran 8 tests … OK`.
- Mutants (`mutants_b6a.py`, `preuves/B6a-mutants.out` `e05f82b5…`) : **20 tués sur 20**, chacun par le test de son
  contrôle : A1 préfixe admis, A2 préfixe inverse, A3 casse ignorée, A4 blancs retirés, A5 `[1m]` refusé, A6 tout
  suffixe entre crochets, A7 suffixe sans casse, A8 contrôle retiré, A9 liste recopiée dans l'outil, A10 première de
  deux lignes `ALLOWED` lue, A11 ligne non ancrée (commentaire lu) ; D1 `--depot` ignoré, D2 clés seules comparées, D3
  valeurs communes seules, D4 `HEAD` ré-extrait au lieu du commit, D5 servi sans le dépôt, D6 ré-extraction impossible
  admise, D7 `--depot` non transmis par la CLI, D8 `--depot` refusé avec `--verifier`, D9 couverture inversée. Rejoués
  sur l'arbre final : 20 sur 20 (`preuves/B6a-mutants-sur-final.out`, même sha256 `e05f82b5…`).
- Suite sur l'arbre B6a : `Ran 342 tests in 30.178s`, `OK (skipped=2)` (`preuves/B6a-suite.out` `ce352927…`).
- Numstat (`preuves/B6a-numstat.out`) : outil +71 −20 ; tests +79 −1 ; total **171 lignes**.

### 3.3 B6b — délai maximal par commande

- Test : `test_delai_depasse_exit_non_nul_enregistrement_ecrit` — commit de fixture dont le test dort 20 s, délai 1 s :
  `exit` 124 du run, exit 1 de l'enregistrement, ligne de dépassement en fin de sortie, sha256 de la sortie
  recalculé égal, refus `exit` à la lecture ; `DELAI_DEFAUT` remplacé par 1 (`mock`) et aucun délai passé : run à 124 ;
  délais 0, −1, infini, NaN : refus sans rien écrire ; CLI `--delai 1` : code 1 et run à 124 ; `--delai` avec
  `--verifier` : code 2.
- Échec avant (test final sur l'outil de l'arbre B6a, `preuves/B6b-avant.out` `f1282cba…`) : `FAILED (errors=1)` —
  `AttributeError: module 'oracle_record' has no attribute 'DELAI_DEFAUT'`. Après : `Ran 9 tests … OK`.
- Mutants (`mutants_b6b.py`, `preuves/B6b-mutants.out` `9bfcdfb9…`) : **8 tués sur 8** : T1 aucun délai transmis, T2
  dépassement consigné 0, T3 enregistrement non écrit au dépassement, T4 ligne de dépassement absente, T5 défaut figé
  (constante non lue), T6 validation retirée, T7 `--delai` non transmis par la CLI, T8 `--delai` admis avec
  `--verifier`.
- Suite sur l'arbre final : `Ran 343 tests in 32.367s`, `OK (skipped=2)` (`preuves/B6b-suite.out` `b28c1a6d…`).
- Numstat (`preuves/B6b-numstat.out`) : outil +29 −14 ; tests +34 −1 ; total **78 lignes**.

### 3.4 Rejeu des mutants de B4 sur l'arbre final

B6 déplace l'extraction dans `extraire()` et touche la CLI : les 50 mutants de B4a, B4b et B4c (listes de
`lot-B2/outils/`) sont rejoués sur l'arbre final par `mutants_b4_sur_final.py`, cinq ancres déplacées remplacées par
leur forme finale (W4, V16, X8, X10, X12 ; mutation identique) : **50 tués sur 50** (`preuves/B4-mutants-sur-final.out`
`93d22fc1…`).

### 3.5 Règle, rendus

`shogen_s2/` n'est touché par aucun sous-lot B6. Règle : `ea3a2d94…` sur les arbres B6a et final (`regle/B6a.json`,
`regle/B6.json`, `cmp` identiques à `HEAD`). Rendus : `4e62fbb8…`, `d079dd9d…` sur B6a et final (= épingles de B5).

## 4. Empreintes

- Diffs (étiquettes `a/s2-harness/…`, `b/s2-harness/…`, sans opération git) : `B5.diff`
  `61e573b44fe0abf696d5fb1ae9e5a46ecb34bf601b54c6ff38a60b1af3907407` (contre `d4db81d`) ; `B6.diff`
  `8a070b861dbca572767e6a7d01d412e06bd15afc0403490704e15a71165774a2` (contre l'arbre B5, B6 d'un seul tenant) ; coupe :
  `B6a.diff` `88deb91a224745096247b5cf307905f2e95abf301d48af77eddcc7077c2eb92d` (contre l'arbre B5) ; `B6b.diff`
  `1bb17e947b9f770610f7880a5d1c4385810a49b7d3c5a2cb7888972b597a27eb` (contre l'arbre B6a). Contrôle par `patch -p1` sur
  l'export de `d4db81d` : `B5.diff` donne l'arbre B5, puis `B6a.diff` l'arbre B6a, puis `B6b.diff` l'arbre de travail
  final (`diff -r` vide) ; l'arbre B5 plus `B6.diff` donne le même arbre final.
- Fichiers finaux (sha256) : `shogen_s2/r1.py` `27a6e3d4e2258c5b9150017881b534a52dde343b617f4b2d5c6b4244bf7dfc57` ;
  `shogen_s2/records.py` `22924dfaa55f2072b6e964bc2ba576e6c10eed5bd7b5e5b924c05a5497cae503` ; `shogen_s2/report.py`
  `52bbae680c6e38115b8effc7bac616def99edb8b74f1dc0a23074cb7477ab338` ; `tests/test_censure_causes.py`
  `7494d5069c02f79679702152edb81211ebd6d9f5f3b3e381b46708f0ef76295b` ; `tests/test_exclusion.py`
  `4b321b54cf9e250ee657d6603c5ea0948f784edf89a706489d7c5a9d1c1db2b2` ; `tests/test_pool_analyse.py`
  `26e3b3c07ca3fd9ea06570a281f66a97eba7a61509e044de599697b731e8e5d2` ; `tests/test_oracle_record.py`
  `5fbd5cd882f1d364fa1ce5109d642fb32478536737f78a9d1fdd871e09e54b0a` ; `tools/oracle_record.py`
  `9d8553f33d1f44721072b65d225f1d1db1a649d49b9f1f35eda58c20cb4ee509`.
- Suites recomptées : 336 (départ) → 340 (B5) → 342 (B6a) → 343 (B6b), deux sauts à chaque pas (les deux tests de la
  variable scellée).
- R-13 et secrets : motif R-13 du hook (l.21) et motifs VENDOR et GENERIC de la gate des secrets rejoués par `grep` sur
  les huit fichiers touchés : 0 occurrence. Aucune dépendance neuve (`bisect`, `math` : bibliothèque standard).
- Preuves antérieures aux trois dernières retouches du test B6 (garde d'existence du lint ; ligne `ALLOWED` en
  commentaire dans le lint de fixture ; `bash` résolu dans l'ordre du PATH) et aux versions antérieures de ce journal
  rangées à part, non citées comme preuves : `preuves/anterieur/`. Après la dernière retouche, tout est rejoué : échec
  avant de B6a et de B6b, suites B6a et finale, mutants de B6a (arbre B6a et arbre final), de B6b et de B4, règle,
  rendus, chaîne de `patch`.

## 5. Écarts

- **E1 (B6, coupe)** : B6 coupé en B6a (i, ii) et B6b (iii) ; l'arbre B6a est reconstruit depuis l'arbre final par
  retrait textuel (`faire_b6a.py`), puis éprouvé seul (échec avant, suite, mutants).
- **E2 (B5, libellés)** : libellés développés au-delà des formes courtes de la décision : la première ligne définit le
  démarrage (`run_params` ou `clock_check` de phase `startup`, ordre du journal) ; chaque ligne porte `sur s = <s>` pour
  que la décomposition se lise sans recalcul.
- **E3 (B5, délimitation des démarrages)** : l'item dit « lus aux enregistrements run_params et clock_check de phase
  startup » sans fixer la règle de découpe : ordre du journal, l'une ou l'autre ligne ouvre un démarrage (choix
  prudent : une ligne excisée ne fusionne pas deux démarrages) ; marqueurs écrits avant toute ligne de démarrage :
  hors démarrage ; portées chevauchantes : union.
- **E4 (B6, serrages)** : au-delà du brief, le `--verifier` refuse aussi `auteur` quand la liste blanche est illisible
  ou ambiguë (ligne `ALLOWED` répétée), contrôle le servi au même dépôt, et la CLI imprime la couverture de
  `tree.sha256` ; le message de conformité de B4c change donc (test mis à jour).
- **E5 (B6, extraction)** : l'extraction de `enregistrer` est mise en fonction (`extraire`) pour que l'écriture et la
  relecture suivent la même procédure ; mutants de B4 rejoués (§3.4).

## 6. Limites rencontrées (items à former, règle PAROXYSME)

- **L1 — SHOGEN-CENSURE-CAUSES-TIERS-1** : la ventilation n'est servie ni au recalcul tiers
  (`r1.recompute_d5_from_journal` ne rend que s et les bornes) ni à l'enregistrement d'oracle. Construction proposée :
  clé `fenetres_sautees_vivant` dans `recompute_d5_from_journal` (même appel que le rendu : `records.demarrages`,
  portée, plages), test d'égalité avec les deux lignes du bloc 1 ; consommateur : la commande `recalcul-tiers` de C3
  (SHOGEN-RECALCUL-TIERS-CLI-1). Déclencheur : sous-lot C3. Prix ≈ 5 lignes et 15 de tests [inféré].
- **L2 — SHOGEN-CENSURE-VIVANT-PORTEE-1** : « harnais vivant » signifie « même démarrage avant et après la fenêtre »,
  pas « harnais en marche pendant la fenêtre » : une mise en veille du poste ou un blocage du processus sans
  redémarrage, à l'intérieur d'un démarrage, est compté vivant (le collecteur saute alors à la fenêtre courante sans
  écrire de démarrage) ; à l'inverse, une frontière de chunk d'un processus vivant est non attribuée (signature
  identique à un arrêt, B-2 §4.3 cas 6). Sans seuil (décision), le journal ne sépare pas ces cas. Construction :
  portée du libellé écrite au paquet ; source hors journal (journal système du poste : événements de veille) nommée
  pour l'exécution unique. Déclencheur : G0 du PAQUET (partie 3). Prix : deux à trois lignes de texte [inféré].
- **L3 — SHOGEN-ENREG-DELAI-ARBRE-1** : au dépassement, seul le processus enfant direct est arrêté ; ses propres
  sous-processus survivent, et sous Windows `subprocess.run` relit le tube jusqu'à sa fermeture après l'arrêt : un
  petit-enfant qui garde le tube peut prolonger le blocage au-delà du délai. Construction : groupe de processus
  (`start_new_session` et `os.killpg` sous POSIX ; groupe de processus ou objet de tâche et arrêt de l'arbre sous
  Windows), test avec un petit-enfant qui garde le tube. Déclencheur : avant l'exécution unique (poste Windows), au plus
  tard C3. Prix ≈ 15 lignes et 20 de tests [inféré].
- **L4 — SHOGEN-ENREG-DELAI-CHAMP-1** : le délai appliqué n'est pas consigné dans l'enregistrement (la liste des
  champs de D6 viii est ratifiée ; une clé de plus amenderait le schéma) ; seule la ligne de dépassement le porte, et
  seulement au dépassement. Construction : champ `delai` par run (décision de schéma) ou texte au paquet. Déclencheur :
  décision de l'orchestrateur (Q3). Prix ≈ 3 lignes et une ligne de test [inféré].
- **L5 — SHOGEN-ENREG-TEST-BASH-1** : `test_verifier_auteur_liste_blanche_du_lint` lance `bash` (oracle : le lint
  lui-même) ; c'est le premier test de `s2-harness` qui dépend de bash. Sur le poste Windows de l'exécution unique, il
  faut le bash de Git en tête du PATH (session Git Bash) : sans bash, le test échoue, et l'enregistrement d'oracle du
  rendu, qui lance la suite, porterait exit 1. Construction : rejouer la suite sur le poste local avant l'exécution
  unique ; à défaut, oracle sans bash (ligne `ALLOWED` lue par le lexeur `shlex`, plus faible). Déclencheur : revue
  de partie 2 (rejeu des oracles) ou première suite sur le poste Windows. Prix : une commande [inféré].

## 7. Questions ouvertes

- **Q1** (B6 i) : la liste blanche est lue dans le lint du dépôt de l'outil qui vérifie (roster courant), pas dans le
  commit enregistré (roster du jour de l'enregistrement) : un enregistrement d'un modèle retiré entre-temps serait
  refusé. Lecture voulue, ou lecture dans l'extraction du commit quand `--depot` est donné ?
- **Q2** (B6 i) : l'écriture (`enregistrer`) doit-elle refuser elle aussi un `auteur` hors liste, avant toute commande,
  ou le contrôle reste-t-il au seul `--verifier` (état actuel) ?
- **Q3** (L4) : le délai appliqué entre-t-il au schéma `shogen.oracle-record.v1` (champ neuf), ou au texte du paquet ?
- **Q4** (L2) : la portée du libellé « harnais vivant » s'écrit-elle au paquet, ou le libellé du rendu doit-il la dire
  lui-même (une re-capture d'épingles de plus) ?

## 8. Clôture

- Suite finale (arbre de travail, après la dernière retouche) : `Ran 343 tests in 32.367s`, `OK (skipped=2)`
  (`preuves/B6b-suite.out`) ; `SHOGEN_S2_CAMPAGNE_CONTROL` absente (`env | grep -c` : 0).
- `cargo --locked xtask verify` : avant la rédaction (06:43 UTC), `=== VERDICT GLOBAL : VERT ===`, rc 0 (S-G4 75
  fichiers sur 75, S-G5 76 sur 76, corpus complet 125 artefacts sur 125, 252 fragments contrôlés) ; relancé avec des
  versions intermédiaires de ce journal dans `docs/` (06:51 et 06:53 UTC) : VERT, rc 0 (S-G4 76 sur 76, S-G5 77 sur
  77, 252 fragments contrôlés, 2 850 écartés sous seuil, 0 violation ; sorties dans `preuves/anterieur/`). Relance sur
  la version finale : verdict et sha256 de ce fichier dans le rapport de remise à l'orchestrateur (un fichier ne porte
  pas son propre sha).
- `git status` final : modifiés `shogen_s2/r1.py`, `records.py`, `report.py`, `tests/test_exclusion.py`,
  `tests/test_pool_analyse.py`, `tests/test_oracle_record.py`, `tools/oracle_record.py` ; neufs
  `tests/test_censure_causes.py` et ce journal.
