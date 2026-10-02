# Journal G1 — partie 3 de S2, lot P3

**Nature** : journal de provenance du worker du lot P3 (session cloud), travail du 2026-10-02 de 14:16 à 15:0x UTC
(horloge lue par `date -u` : 14:16:07 au départ, 14:58:08 avant la rédaction ; clôture au §10). Contrat :
`docs/adr-0028/G0-partie-3.md`, section « P3 » (l.6-30, six items, constructions décidées). Branche `partie-3-paquet`,
base des diffs `32044eb`. Aucune opération git en écriture sur le dépôt ; dépôts jetables seulement (scratchpad et
dossiers temporaires des tests). Livrables : six sous-lots P3a à P3f (diffs dans `<S>/lot-P3/`, où `<S>` est le
scratchpad de la session, `/tmp/claude-0/-home-user-shogen/7ba84933-ba6d-5813-9ef4-ca3ac4febd16/scratchpad`) et ce
journal ; rien n'est commis (R-19, R-20).

## 0. Gate 0 et cadre

- **Modèle résolu sous lequel le worker a tourné : `claude-opus-5-5`** (identifiant exact fourni par l'environnement de
  la session ; préfixe attendu `claude-opus-5-5` : conforme). Effort : `max` (fiche du worker et brief).
- Dépôt : HEAD `32044eb` au départ (14:16 UTC), `git status` vide. L'orchestrateur a commis pendant le travail `074dfab`
  (14:27:25 UTC, `docs/R-8-outillage.md`), `70c5004` (14:31:51 UTC, annexe D : D.1 l.15, D.2 points 10 et 11,
  `JOURNAL.md`) et `3414e0f` (14:32:13 UTC, G0 de l'étape S ajouté à `G0-partie-3.md`) ; `s2-harness/` et `scripts/`
  sont identiques entre `32044eb` et `3414e0f` (`git diff --quiet 32044eb HEAD -- s2-harness scripts`) : les diffs,
  calculés contre `32044eb`, valent pour la tête ; la section P3 du G0 (l.6-30) est inchangée (même sha256,
  `a85e88d9…`). Points 10 et 11 de D.2, lus pour s'en garder : registre PAROXYSME hors dépôt et transcription de la
  session de l'orchestrateur, jamais à ma portée.
- Rattachement (G0) : les six lignes d'annexe citées par le brief, lues avant tout code
  (`docs/adr-0028/ANNEXE-B-items.md` l.343, 357, 391, 413, 435, 436) et les décisions du G0 P3 (l.12-27).
- Fichiers d'un autre worker apparus pendant le travail, non suivis, hors de mon fait et non touchés :
  `docs/G1-partie-3-S.md` (vu à 14:52 UTC ; trois premières lignes affichées pour l'identifier, rien d'autre) et
  `scripts/sim/sim_garde_niveau_oracle_r1.py` (vu à 14:57 UTC ; un seul `grep -n` à 15:02 UTC, qui affiche ses lignes
  d'import et ses deux lignes qui nomment `r1.CONTEXTE_DECIMAL`, l.90 et l.137 : conflit avec P3c, Q4) ; à 15:07 UTC, un
  troisième, `scripts/sim/sim_garde_niveau.py` (un `grep -c` : 0 occurrence de `CONTEXTE_DECIMAL`, comme les quatre
  fichiers suivis de `scripts/sim/`). Mes outils ne copient que `s2-harness/`, `enforcement/` et `scripts/sceau/` : ces
  fichiers n'entrent ni dans mes diffs ni dans mes mutants ; le premier entre au périmètre de S-G4 et S-G5 de
  `xtask verify` (disque, non l'index).

## 1. Provenance commune

### 1.1 Sources lues (toutes [lu] ; aucune [abs] ni [2nd])

- `CLAUDE.md` (racine, `04200485…`, rappelé par la session) ; `docs/PASSATION-CLOUD.md` (`698978f2…`) : titres, §4 et §6
  (l.95-151, l.190-210).
- `docs/adr-0028/G0-partie-3.md` à `32044eb` (`8df9da17…`) l.1-30, en entier ; `docs/adr-0028/ANNEXE-B-items.md`
  (`a9fd473e…`) : l.1-30 (en-tête et B.1), l.330-342, l.343, l.350-358, l.385-392, l.405-414, l.425-438.
- Contexte : `docs/G1-partie-2-etape-C-1.md` (`cc4f63cd…`) l.1-402, en entier (dont §7 L1, la sonde du sceau) ;
  `docs/G1-partie-2-corrections-G2.md` (`73651658…`) l.1-64, l.99-160, l.274-393 (dont §7 : STATUS-HEAD, PICKAXE) ;
  `docs/G2-partie-2.md` (`0b45a458…`) l.256-272 (§7) ; `docs/G1-partie-2-etape-A.md` (`1e62ec9e…`) l.36-75
  (SENS-PLAGES-1 et Q2) ; `docs/G1-partie-2-etape-B-1.md` (`903a94d2…`) l.345-356 (L9, contexte nommé mutable).
- Code, à `32044eb`, en entier : `scripts/sceau/make-tsq.sh` (`f8b04b5a…`, 20 lignes), `scripts/sceau/verify.sh`
  (`cf55f897…`, 18 lignes), `s2-harness/tools/rendu_unique.py` (`fac88ec2…`, 489 lignes),
  `s2-harness/tests/test_rendu_unique.py` (`90973bde…`), `s2-harness/tests/test_rendu_production.py` (`8a56fbbc…`),
  `s2-harness/tests/test_contexte_decimal.py`, `s2-harness/tests/__init__.py` ; en partie : `shogen_s2/r1.py` l.1-100,
  `shogen_s2/report.py` l.38-60 et l.660-785, `shogen_s2/r2.py` l.60-80, `shogen_s2/lm.py` l.45-55,
  `tests/test_sensibilite.py` l.1-358, `tests/test_rendu_libelles.py` l.1-40 et l.70-93, `tests/test_exclusion.py` l.44,
  `tests/test_oracle_record.py` l.22-41 et l.225-250.
- Gates et CI : `.github/workflows/gates.yml` (`5d6e2bf9…`) en entier ; `enforcement/tests/run-fixtures-hooks.sh`
  l.1-60 ; `enforcement/hooks/pre-commit` (`00131872…`) l.15-35 ; `enforcement/gate-secrets.sh` (`47f2c35e…`) l.50-62 et
  l.100-115 ; `xtask/src/sg4.rs` l.1-120 (locutions interdites, périmètre) ; `xtask/src/sg5.rs` l.1-80 (extraction des
  fragments anglais) ; `xtask/src/documents.rs` l.75-100 (citations blanchies).
- Scratchpad : `regle_fixtures.py` (`5557fb56…`) et `render_fixture.py` (`4084c42b…`), imposés par le brief, utilisés
  tels quels ; `faire_diff.py` (`e03caf95…`), lu, non employé (limité à `s2-harness/`, E2) ;
  `lot-G2corr/outils/instantane.sh` et `moteur.py`, lus pour la forme, et ses listes `mutants_G2*.py` (rejouées, §4) ;
  `lot-C1/outils/mutants.py` et `mutants_c2b.py`, lus pour la forme.
- Après les commits de l'orchestrateur (§0) : `docs/adr-0028/ANNEXE-D-preenregistrement.md` (`329d5794…` à la tête) :
  lignes d'un `grep -n` sur les titres et les points 10 et 11 (l.7, 22, 23, 31, 42, 43, 47, 110, 155) et lignes ajoutées
  par `git diff 074dfab HEAD` (D.1 l.15, D.2 points 10 et 11) ; `docs/adr-0028/G0-partie-3.md` à la tête (`226d0099…`)
  l.32-45 (section S, pour Q4).
- Système : Python 3.11.15 (module `decimal` en C), git 2.43.0, OpenSSL 3.0.13, GNU coreutils 9.4, bash 5.2.21.

### 1.2 Pré-enregistrement (annexe D)

- D.4 a : fixtures seulement (dépôts jetables, journaux de fixture du collecteur réel, autorité RFC 3161 de test
  produite par `openssl`) ; aucun journal de campagne, aucune copie scellée, aucun réseau.
- D.2 : aucune pièce ouverte ; ADR-0025 et la cartographie du 2026-09-29 jamais lues ni affichées ; une recherche de
  noms de fichiers les a parcourues avant un filtre de sortie, sans rien afficher d'elles (écart E11). `JOURNAL.md` non
  ouvert ; deux commandes l'ont parcouru sans rien en afficher : la même recherche (E11) et la mesure de coût de
  `git log -S` et `-G` avec un sha256 tiré au hasard (0 commit trouvé, seuls le compte et la durée sortent, §3.6).
- `SHOGEN_S2_CAMPAGNE_CONTROL` et `SHOGEN_RENDU_PRODUCTION` jamais posées, absentes de l'environnement de la session
  (`env | grep -c` : 0 au départ et à la clôture) ; les suites tournent de plus sous `env -u` des deux variables, la
  règle, les épingles et `xtask verify` sous `env -u SHOGEN_S2_CAMPAGNE_CONTROL`, et le moteur de mutants retire les
  deux de l'environnement de ses sous-processus. `TMPDIR` posé sur `<S>/lot-P3/tmp`.

### 1.3 Sondes (`<S>/lot-P3/sondes/`, dépôts et dossiers jetables)

- `sonde_sceau.sh` (`b68b65c8…`), sortie sur les scripts de `32044eb` (`sonde_sceau-base.out`, `b929ca36…`) : sonde L1
  du G1 C-1 rejouée : `make-tsq.sh` écrit `<sha> *docs/adr-0028/PAQUET-PREREG-S2.md`, `verify.sh` sort
  `MANIFESTE : ÉCART`, code 2, à la racine comme depuis `docs/`. Sur une copie corrigée (`sonde_sceau-corrige.out`,
  `8f9f43d6…`) : code 0 et `SCEAU : VÉRIFIÉ HORS LIGNE` dans les deux cas.
- `sonde_sceau_data.sh` (`e589f2bd…`, `sonde_sceau_data.out` `9a93f26d…`) : paquet et manifeste réécrits d'accord après
  le jeton : `verify.sh` corrigé sort encore code 0 et `SCEAU : VÉRIFIÉ HORS LIGNE` ;
  `openssl ts -verify -data PAQUET.sha256` refuse (empreinte du message différente, code 1). Limite L1 (§8).
- `sonde_pickaxe.py` (`55ff601e…`, `.out` `b3c9f233…`) : `-S<sha>` liste le commit qui ajoute `f<sha>` (sous-chaîne) et
  manque celui qui réécrit `f<sha>` en ligne entière à nombre d'occurrences égal ; `-G<sha>` liste les trois commits ;
  `-G` lit les expressions étendues ; le textconv s'applique à `-G` sauf sous `--no-textconv` ; le commit racine est
  listé ; `git show <commit>:JOURNAL.md` rend le blob brut sous textconv.
- `sonde_diff_arbre.py` (`93d22d68…`, `.out` `0b0bba49…`) : `git diff --quiet <X> -- CHEMINS` juge l'arbre de travail
  contre X : date de modification seule 0, non suivi 0, ignoré 0 (vus par `git status`), indexé puis rétabli 0, retiré
  de l'index 1, modifié 1 ; HEAD sur Y, arbre égal à Y : `git diff` 1 et `git status` vide (le défaut de
  RENDU-STATUS-HEAD-1) ; HEAD sur Y, arbre et index égaux à X : `git diff` 0, `git status` non vide.
- `sonde_rename.py` (`73c9dc2a…`, `.out` `095bea6b…`) : sous POSIX, `os.rename` d'un répertoire remplace une cible
  vide ; refuse une cible non vide, un fichier, un lien pendant ; `os.mkdir` refuse les quatre.
- `sonde_contexte.py` (`0fd8dd45…`, `.out` `6270a7c8…`) : un `Context` partagé modifié passe son piège à tout
  `localcontext` qui le copie ; une fabrique rend un contexte neuf ; surcoût d'un `localcontext(fabrique())` : 0,80 µs
  par usage (200 000 usages). `sonde_contexte_base.py` (`5db1d45c…`, `.out` `8489211f…`), sur l'arbre de base : §3.3.

### 1.4 Outils écrits (`<S>/lot-P3/outils/`, sha256)

`instantane.sh` `1094ef60…` (copie des fichiers suivis et neufs non ignorés de `s2-harness/` et `scripts/sceau/` dans le
dépôt jetable `jetable/`, diff contre l'instantané précédent, numstat ; base : `git archive 32044eb`) ; `moteur.py`
`717c7a49…` (copie des fichiers suivis et neufs non ignorés de `s2-harness/`, `enforcement/`, `scripts/sceau/`, une
mutation dont l'ancien texte figure une fois exactement, tests nommés, témoin vert d'abord) ; listes `mutants_P3a.py`
`ef645dc9…`, `mutants_P3b.py` `84c2e448…`, `mutants_P3c.py` `1e934a21…`, `mutants_P3c_cible.py` `8ab75e59…`,
`mutants_P3d.py` `fbfc582e…`, `mutants_P3e.py` `3eb39780…`, `mutants_P3f.py` `5190cf09…`, `mutants_final_P3.py`
`a0485992…` ; `rejeu_final.sh` `72f73ca8…`.

### 1.5 État de départ (arbre `32044eb`)

- Suite : `Ran 376 tests in 42.570s`, `OK (skipped=2)` (`preuves/suite-depart.out`, `2d24a791…`).
- Règle scellée SHOGEN-CRITERE-R1-1 : `regle_fixtures.py` sur l'instantané de base, sha256 du JSON
  `ea3a2d94ef1075603e8f7cfc53c68b26e51729b61714028e3fb03dc32f79cb29` (= référence).
- Épingles : `render_fixture.py` sur la base : `sans_option` `4e62fbb8…`, `avec_option` `d079dd9d…`, égales à
  `SHA_BASE_SANS_OPTION` (`tests/test_exclusion.py` l.42) et `SHA_BASE_AVEC_OPTION` (`tests/test_pool_analyse.py` l.41).
- Préexistant, hors de mon fait : `s2-harness/tests/__pycache__/__init__.cpython-311.pyc` (04:36:57 UTC, ignoré),
  laissé ; aucun autre cache créé sous `s2-harness/` ni `scripts/` (contrôle de clôture).

## 2. Sous-lots (un par item ; chacun ≤ 200 lignes de code et tests)

| sous-lot | item | numstat par fichier | total | suite après | sha256 du diff |
|---|---|---|---|---|---|
| P3a | SCEAU-VERIFY-CHEMINS-1 | `tests/test_sceau.py` +78 (neuf) ; `make-tsq.sh` +3 ; `verify.sh` +3 −2 | +84 −2 = 86 | 378, OK (2 sauts) | `ac45937f8208c71d116e271ab969c33615432aa52b43eaa61d56534b4e11af1d` |
| P3b | SENS-PLAGES-2 | `report.py` +3 −2 ; `test_rendu_libelles.py` +15 −2 ; `test_sensibilite.py` +5 −3 | +23 −7 = 30 | 379, OK (2 sauts) | `b65d56f8089c6fcaf9062c393b8802e3a54e6829337fd1cc98f313821cff9309` |
| P3c | CONTEXTE-MUTABLE-1 | `lm.py` +4 −4 ; `r1.py` +25 −19 ; `r2.py` +11 −11 ; `report.py` +3 −3 ; `test_contexte_decimal.py` +21 −5 ; `test_rendu_production.py` +1 −1 ; `rendu_unique.py` +1 −1 | +66 −44 = 110 | 380, OK (2 sauts) | `b816486e42bee728a9cd8b1494ece7dd214a78dc027d8be4f3885ccbc028320f` |
| P3d | RENDU-RENAME-POSIX-1 | `test_rendu_production.py` +16 ; `rendu_unique.py` +11 −3 | +27 −3 = 30 | 381, OK (2 sauts) | `c2a0f013ffa22c122a67a332148e22635f0515ff1017f2179d3066675d7d57e1` |
| P3e | RENDU-STATUS-HEAD-1 | `test_rendu_unique.py` +7 −4 ; `rendu_unique.py` +6 −2 | +13 −6 = 19 | 381, OK (2 sauts) | `16f3a580043e4579148fc8a2a6077e9dfaf23460862d87066bf39bae5691a123` |
| P3f | GO-PICKAXE-1 | `test_rendu_unique.py` +31 ; `rendu_unique.py` +13 −10 | +44 −10 = 54 | 382, OK (2 sauts) | `50f9cbda2b03162f9ca831462facf0a5dbb8ecf460a9f5a7f705fe5e597e1ef7` |

Diffs : `<S>/lot-P3/P3a.diff` à `P3f.diff` (étiquettes `a/…`, `b/…` relatives à la racine), chacun contre l'instantané
précédent, à appliquer dans l'ordre ; numstat : `P3a.numstat` à `P3f.numstat`. Diff total `32044eb` → arbre final :
`total-32044eb-final.diff`, 13 fichiers, +257 −72, sha256
`ad1b6860735ca7734427058a53d702368356b29c806be02cc77795ff9ea8761e`. Contrôle : export de `32044eb` (`git archive`),
`patch -p1` des six diffs dans l'ordre, puis `cmp` de chaque fichier suivi de `s2-harness/` et `scripts/sceau/` et de
`tests/test_sceau.py` contre l'arbre de travail : aucune différence.

## 3. Par sous-lot

Méthode commune : test écrit d'abord et lancé sur l'arbre du sous-lot précédent (échec consigné dans
`preuves/<sous-lot>-avant.out`), code, test vert (`-apres.out`), mutants (`-mutants.out`, témoin vert d'abord), suite
entière (`suite-<sous-lot>.out`), instantané ; règle scellée et épingles sur chaque instantané qui touche `shogen_s2/`.

### 3.1 P3a — SCEAU-VERIFY-CHEMINS-1 (annexe B l.391)

- Construction : `verify.sh`, étape (1) : `sha256sum -c "$D/PAQUET.sha256"` lancé depuis la racine du dépôt (où le
  script se place déjà), au lieu d'un sous-shell placé dans le dossier de sceau ; l'en-tête nomme la convention.
  `make-tsq.sh` (serrage, E3) : avant toute écriture, chaque fichier du paquet doit être un chemin relatif à la racine,
  sans segment `..`, sans lettre de lecteur ni barre oblique inverse (`case "/$f/" in //*|*/../*|/[A-Za-z]:*|*\\*`) ;
  sinon ligne `refus : <chemin> hors de la convention du manifeste`, code 2.
- Lieu du test (choix motivé, brief) : `s2-harness/tests/test_sceau.py`, dans la suite du harnais plutôt qu'un runner
  `enforcement/tests/` : l'autorité RFC 3161 de test (`autorite`, `o`, configuration minimale) et les aides de dépôt
  jetable (`g`, `poser`, `GIT_ENV`) existent déjà et ont été relues (C2a, G2) ; la suite tourne à chaque sous-lot
  (brief) et dans le job `s2-harness-unittest` existant, sans retouche de `gates.yml` ; précédent d'un test du harnais
  sur un fichier hors de `s2-harness/` : `LINT` (`tests/test_oracle_record.py` l.33). Les scripts du dépôt sont lancés
  par `bash` (résolu dans le PATH, comme `test_oracle_record` l.233) depuis le dépôt jetable ; `bash` ou `openssl`
  absent : le test échoue, il ne saute pas.
- Tests : `test_make_tsq_puis_verify_depuis_la_racine` (manifeste attendu écrit à la main,
  `<sha256 des octets écrits> *docs/adr-0028/PAQUET-PREREG-S2.md` ; réponse de la TSA de test sur la requête de
  `make-tsq.sh`, chaîne posée ; `verify.sh` à la racine puis depuis `docs/` : code 0, dernière ligne
  `SCEAU : VÉRIFIÉ HORS LIGNE …` ; paquet changé : code 2, `MANIFESTE : ÉCART`, étape (2) jamais atteinte) ;
  `test_make_tsq_refuse_un_chemin_hors_convention` (absolu, `docs/../…`, `C:/…`, barres inverses : code 2, ligne
  `refus : …`, dossier de sceau réduit à `chain`).
- Échec avant (scripts de `32044eb` ; `P3a-avant.out`, `a4774684…`) : `FAILED (failures=6)` : `verify.sh` code 2 et
  `MANIFESTE : ÉCART` aux deux dossiers de lancement (la sonde L1) ; `make-tsq.sh` accepte les quatre chemins (codes 0,
  0, 1, 1 ; manifeste et requête écrits). Après : `Ran 2 tests`, `OK` (`302616ba…`).
- Mutants (`P3a-mutants.out`, `ceee5e8a…`) : **8 tués sur 8** — A1 lecture depuis le dossier de sceau rétablie, A2 étape
  (1) neutralisée, A3 à A6 chacun des quatre motifs de la garde retiré, A7 garde après la troncature du manifeste, A8
  garde retirée.
- Suite : `Ran 378 tests in 39.776s`, `OK (skipped=2)` (`2b562e13…`). Règle : `ea3a2d94…`, identique à l'octet.

### 3.2 P3b — SENS-PLAGES-2 (annexe B l.343)

- Construction : dans la couverture par week-end de `[SENSIBILITÉ]`, `pl` vaut `la plage` pour une plage et
  `les <k> plages` sinon (même critère `len(ranges)` que le titre de SENS-PLAGES-1) ; lignes `… ; retirées par <pl> <n>`
  et `… ; retirés en totalité par <pl> : <n>`. La ligne générique
  `comptes de pertes …, retirés par la plage, plage par plage puis union` n'est pas une ligne de week-end : inchangée
  (hors item).
- Tests : `test_lignes_week_end_accordees_au_nombre_de_plages` (neuf, `tests/test_rendu_libelles.py`, une, deux et trois
  plages : les trois lignes de week-end et la ligne des totaux) ; aides `attendu_we` et `TestSensibilite.week_ends` de
  `tests/test_sensibilite.py` accordées au nombre de plages (attendus écrits à la main).
- Échec avant (`report.py` de base ; `P3b-avant.out`, `f8299702…`) : `FAILED (failures=4)` : le test neuf à deux et
  trois plages, `test_couverture_week_ends_recomptee` et `test_forme_j28_cli_segment_n_fixe_et_plages` (deux plages).
  Après : `Ran 17 tests`, `OK` (`a2a40f53…`).
- Mutants (`P3b-mutants.out`, `d5d070c0…`) : **6 tués sur 6** — B1 singulier gardé, B2 nombre codé à 2, B3 pluriel sans
  le nombre, B4 ligne de week-end seule au singulier, B5 ligne des totaux seule au singulier, B6 singulier jusqu'à deux
  plages.
- Suite : `Ran 379 tests in 40.095s`, `OK (skipped=2)` (`cdbe0d7f…`). Règle identique. Épingles : rendus de l'instantané
  P3b égaux à ceux de la base (`diff -r` vide ; une seule plage dans la fixture épinglée) : aucune re-capture.

### 3.3 P3c — CONTEXTE-MUTABLE-1 (annexe B l.357)

- Construction (première branche du G0) : la fabrique `r1.contexte_decimal()` rend un `Context` neuf à chaque appel,
  valeurs identiques (prec 50, ROUND_HALF_EVEN, Emin −999999, Emax 999999, capitals 1, clamp 0, aucun drapeau, pièges
  InvalidOperation, DivisionByZero, Overflow) ; l'objet `CONTEXTE_DECIMAL` disparaît. Sites :
  `localcontext(contexte_decimal())` aux 32 usages (r1 14, lm 3, r2 10, report 2, `tools/rendu_unique.py` 1,
  `tests/test_rendu_production.py` 1, test 1 de `test_contexte_decimal`) ; imports de lm, r2, report. Seconde branche
  (objet figé) écartée : il faudrait fermer toutes les voies d'écriture d'un `Context` (attributs, dictionnaires `traps`
  et `flags`, méthodes de calcul du contexte qui lèvent ses drapeaux, `clear_flags`, `clear_traps`) [inféré, non sondé].
- Défaut montré sur la base (`sonde_contexte_base.out`, `8489211f…` ; r1 et lm de l'instantané sont ceux de `32044eb`) :
  `CONTEXTE_DECIMAL.prec = 10` fait rendre `0.1666666667` au site de lm ; `Emin = -20` fait rendre `0E-69` à la médiane
  de r1 ; le piège Inexact posé lève au site de lm ; quatre objets `Context` de module (r1, lm, r2, report).
- Tests : test 1 lu sur la fabrique ; `test_contexte_nomme_non_modifiable` (neuf) : affectations sur un contexte rendu
  (prec 10, ROUND_DOWN, Emin −20, piège et drapeau Inexact) ; le contexte suivant garde les valeurs nommées ; un site de
  lm et un de r1 rendent leurs attendus (oracle du test des sites : `0.1` suivi de 48 `6` puis `7`, et `2E-75`) ; aucun
  objet `Context` dans les modules r1, lm, r2, report.
- Échec avant (`P3c-avant.out`, `e43fbaf6…`) : `FAILED (errors=2)`, fabrique absente (`AttributeError`) ; le défaut
  sémantique est celui de la sonde. Après : `Ran 5 tests`, `OK` (`5dbe4a84…`).
- Mutants (`P3c-mutants.out`, `f8b61eb3…`) : **4 tués sur 4** — C1 fabrique en cache (objet partagé), C2 contexte de
  module réintroduit, C3 Emin changé, C4 site de `_median` rendu au contexte appelant. C1 contamine les tests suivants
  du module (le contexte partagé reste modifié) : C1 et C2 rejoués sur le seul test neuf, tués (`P3c-mutants-cible.out`,
  `c8cf0c96…`).
- Suite : `Ran 380 tests in 44.359s`, `OK (skipped=2)` (`d9e2e48d…`). Règle identique ; épingles identiques. Coût :
  règle des fixtures (dont la fixture longue J4), trois passes : base 2,24 à 2,56 s, P3c 2,03 à 2,43 s (`P3c-temps.out`,
  `2f971f77…`) : aucun écart mesurable.

### 3.4 P3d — RENDU-RENAME-POSIX-1 (annexe B l.413)

- Construction : dans `produire_tout`, juste avant le renommage final : sous POSIX (`os.name != "nt"`),
  `os.mkdir(cible)` (création exclusive : `FileExistsError` si quoi que ce soit existe à cet instant, sonde §1.3), puis
  `os.rename(tmp, cible)` sur cette réserve vide ; sous Windows, `os.rename` seul, qui ne remplace jamais
  (`FileExistsError`). À l'échec, la réserve, la nôtre, est retirée si elle est vide ; une cible apparue d'ailleurs
  n'est jamais touchée.
- Test : `test_cible_apparue_avant_le_renommage` (neuf, `tests/test_rendu_production.py`) : répertoire vide posé à la
  place de `--sortie` pendant le dernier run (crochet `pendant` de `faux_runs`), après le contrôle de destination : code
  1, `gardes levées` seul sur la sortie standard, tous les runs lancés, le répertoire posé reste vide, aucun temporaire
  voisin, `FileExistsError` nommée sur stderr.
- Échec avant (`P3d-avant.out`, `ff15951d…`) : code 0, la cible vide est remplacée par les sorties. Après :
  `Ran 7 tests`, `OK` (`bc7b86e8…`).
- Mutants (`P3d-mutants.out`, `9c93b855…`) : **4 tués sur 4** — D1 création exclusive retirée (`os.rename` seul), D2
  branche inversée, D3 réserve laissée à l'échec (tué par le cas `renommage` existant de
  `test_echec_a_chaque_pas_rien_ne_reste`), D4 nettoyage qui retire la cible d'autrui.
- Suite : `Ran 381 tests in 42.283s`, `OK (skipped=2)` (`d802401a…`).

### 3.5 P3e — RENDU-STATUS-HEAD-1 (annexe B l.435)

- Construction : la garde (2) ajoute `git diff --quiet --no-ext-diff --no-textconv <head> -- CHEMINS` (arbre de travail
  contre le commit résolu, fichiers suivis), entre le diff des deux commits et `git status` ; motif
  `arbre de travail ≠ commit gardé <head> sur … (git diff : code <n>)`. `git status` est gardé (fichiers non suivis et
  ignorés, E3 du G1 C-1) ; il juge encore l'index et l'arbre contre le HEAD courant : plus strict, jamais plus lâche
  (E5, Q1).
- Test : l'attendu du test C-2 (i) `test_gardes_lisent_le_head_resolu_une_fois` encodait le défaut (gardes levées sur X
  alors que l'arbre de travail porte le code de Y) ; réécrit : HEAD sur Y, arbre propre sur Y, résolution rendue à X :
  seule (2) refuse, motif `arbre de travail ≠ commit gardé <X> …`, contexte `head` = X (E6).
- Échec avant (`P3e-avant.out`, `485724fd…`) : gardes levées (`[]`). Après : `Ran 17 tests`, `OK` (`2f69001e…`).
- Mutants (`P3e-mutants.out`, `42511ca3…`), sur le seul test réécrit : **7 tués sur 7** — E1 contrôle retiré, E2 arbre
  jugé contre HEAD, E3 code 1 admis ; mutants C-2 du correcteur G2 rejoués : C2-f ((1) relit HEAD), C2-g (diff des
  commits de (2) contre HEAD : tué par le motif seul, §7), C2-h ((4) relit HEAD), C2-i (voie (b) relit HEAD).
- Suite : `Ran 381 tests in 44.456s`, `OK (skipped=2)` (`182a76d5…`).

### 3.6 P3f — GO-PICKAXE-1 (annexe B l.436)

- Construction : `premier(c, sha)` prend les candidats de
  `git log --no-textconv --reverse --format="%H %ct" -G<sha> <head> -- JOURNAL.md` (commits dont le diff ajoute ou
  retire une ligne qui contient le sha) et rend le premier dont `git show <commit>:JOURNAL.md` porte une ligne qui
  contient le sha entier (`lignes_avec`, le prédicat de (1)) ; aucun : `ValueError`, la voie (b) ne s'établit pas. `-G`
  plutôt que `-S` confirmé (proposition du G1 de correction, §7) : la sonde montre que `-S` manque un commit qui réécrit
  `f<sha>` en ligne entière à nombre d'occurrences égal (E7). Coût sur l'historique réel (103 commits touchent
  `JOURNAL.md`, sha256 tiré au hasard, 0 commit trouvé) : `-S` 0,70 s, `-G` 0,08 s.
- Test : `test_voie_b_premiere_ligne_entiere_pas_une_sous_chaine` (neuf ; trois cas en `subTest`) : (a) go cité d'abord
  en `f<sha>` (08-31 13:00, après la date du go), puis sur sa ligne (09-01) : T0 = `2026-09-01T00:00:00Z`, refus (5) à
  09-01 14:00 ; (b) paquet cité d'abord en `f<sha>` (00:00), puis sur sa ligne (06:00) : go daté de 03:00 refusé ((5) et
  (6)), daté de 12:00 levé (témoin) ; (c) `f<sha>` réécrit en ligne entière (09-01), même nombre d'occurrences : T0 =
  `2026-09-01T00:00:00Z`.
- Échec avant (`P3f-avant.out`, `449abbee…`) : `FAILED (failures=3)` : (a) T0 = `2026-08-31T13:00:00Z` (la garde (5)
  s'ouvrait onze heures trop tôt) ; (b) go de 03:00 levé ; (c) T0 = `2026-08-31T13:00:00Z`. Après : `Ran 18 tests` du
  module, `OK` (`25f5fca9…`).
- Mutants (`P3f-mutants.out`, `ca1756b5…`) : **7 tués sur 7** — F1 construction de C-3 (`-S`, premier commit), F2
  premier candidat de `-G` non confirmé, F3 `-S` confirmé (tué par (c) seul), F4 confirmation par sous-chaîne, F5
  confirmation sur `JOURNAL.md` à HEAD, F6 textconv appliqué et F7 `--reverse` retiré (tués par le test existant à
  textconv hostile, go cité de nouveau dix jours plus tard).
- Suite : `Ran 382 tests in 43.145s`, `OK (skipped=2)` (`d53bf86f…`). Règle identique ; épingles identiques.

## 4. Rejeu de toutes les listes sur l'arbre final

`preuves/final-mutants.out` (`6f6c56f0…`), moteur du lot, témoin vert avant chaque liste :

- listes P3a à P3f et cibles de P3c : **38 tués sur 38** ; C2-i ré-ancré sur `-G` (son ancre `-S` a disparu en P3f) ;
- listes du correcteur G2 de la partie 2 (`lot-G2corr/outils/mutants_G2*.py`, même format), arbre final : G2a 5 sur 5,
  G2b 8 tués (C2-i : ancre disparue, couvert par le C2-i ré-ancré), G2c 8 tués et C3-b vivant (équivalence déclarée par
  le correcteur G2, §6 de son journal, inchangée), G2c_head (C2-i', même mutation, même ancre disparue), G2d 5 sur 5,
  G2e 7 sur 7, G2f 6 sur 6.

## 5. Empreintes

- Diffs : §2 (six sous-lots) et total (`ad1b6860…`).
- Fichiers finaux (sha256 ; base `32044eb` entre parenthèses ; lignes) :

| fichier | final | base | lignes |
|---|---|---|---|
| `s2-harness/shogen_s2/lm.py` | `7ef175350fde8dacdae49b91eaf1c2107e701ed40aecf4741492f8040048ac84` | `1a815ede…` | 239 |
| `s2-harness/shogen_s2/r1.py` | `791868909992028733318238999f15d44c006e63aa7345df65b8412dd5bfdb5e` | `cde3a78d…` | 836 |
| `s2-harness/shogen_s2/r2.py` | `27e7da73a4cf9a3db98ceebcb57ea5c37c14f4ab83aace2d6962aae7170fe779` | `316337c0…` | 1092 |
| `s2-harness/shogen_s2/report.py` | `54e735482115d706d73c487214fe13183a29607c60f801c2b7aac33c25e0a3c3` | `52bbae68…` | 786 |
| `s2-harness/tests/test_contexte_decimal.py` | `984ea45a10cf5df37f2cf256621a56a48a45f80aacc3b9ffc939164c06669916` | `2d02f50b…` | 113 |
| `s2-harness/tests/test_rendu_libelles.py` | `f75dc6cd6febd54f0e69bdb0a47131961de2452133b0e2b9e3f596e688fccfd6` | `d60776e8…` | 106 |
| `s2-harness/tests/test_rendu_production.py` | `b9da16414bc3821993964dc0ba02dc015a8e43d44d5efd50bab43f8dd4f2e00d` | `8a56fbbc…` | 435 |
| `s2-harness/tests/test_rendu_unique.py` | `c56e5f4633b24c1cd1578acba82970d2ccbb0baf4d2f4fd98b911ce7ac8ea4f5` | `90973bde…` | 534 |
| `s2-harness/tests/test_sceau.py` | `1e4eb2648514e7cc19b1e3554bbbf01301aba80bab895bc95f82f78c7d001fa4` | neuf | 78 |
| `s2-harness/tests/test_sensibilite.py` | `a51b6e802403f40fd16b2e9b69a19e6e79384574034592bb2921f20f32411df6` | `faab6cfb…` | 360 |
| `s2-harness/tools/rendu_unique.py` | `67b897a949b76071e1b3f8508d877217ac33f957f92463dd8e9b5e672ab8f8d9` | `fac88ec2…` | 504 |
| `scripts/sceau/make-tsq.sh` | `ef66fe838ae019d82280a65d4284c9f28bb2d58939aaf25fd68b2c0e6e18d3c5` | `f8b04b5a…` | 23 |
| `scripts/sceau/verify.sh` | `f47198693dbd08448e56909a726b99b7f80048e271a0d20aaf6072ab126b21ee` | `cf55f897…` | 19 |

- Suites recomptées : 376 (départ) → 378 (P3a) → 379 (P3b) → 380 (P3c) → 381 (P3d) → 381 (P3e : test réécrit, aucun
  ajout) → 382 (P3f), deux sauts à chaque pas (les deux tests de la variable scellée). Règle scellée : `ea3a2d94…` sur
  la base, P3a, P3b, P3c et l'arbre final (`cmp` identique au JSON de base). Épingles : identiques sur P3b, P3c et
  l'arbre final.
- R-13 et secrets : motif R-13 du hook et motifs VENDOR et GENERIC de la gate des secrets rejoués par `grep` sur les
  treize fichiers touchés : 0 occurrence ; ce journal : contrôlé à la clôture (§10). Aucune dépendance neuve
  (bibliothèque standard ; `git`, `openssl`, `bash` et `sha256sum` : programmes déjà requis par les tests du harnais et
  par les scripts de sceau).

## 6. Écarts

- **E1 (git status initial)** : la première commande du lot (`git status --short`, 14:16 UTC) a tourné sans
  `--no-optional-locks` (rafraîchissement possible des métadonnées de l'index, aucun contenu) ; ensuite, toutes les
  lectures git du dépôt portent `--no-optional-locks`.
- **E2 (outil de diff)** : `faire_diff.py` ne couvre que `s2-harness/` ; remplacé par un dépôt git jetable d'instantanés
  (`instantane.sh`) qui couvre aussi `scripts/sceau/`.
- **E3 (serrage, P3a)** : au-delà de la correction de `verify.sh`, `make-tsq.sh` refuse avant toute écriture un chemin
  hors de la convention (absolu, segment `..`, lettre de lecteur, barre inverse) : sans ce contrôle, un chemin absolu
  donné à `make-tsq.sh` entrerait au manifeste scellé et ne se relirait que sur la même machine. Retirable si
  l'orchestrateur s'en tient à `verify.sh` (Q2).
- **E4 (lieu du test du sceau)** : `s2-harness/tests/test_sceau.py`, motif au §3.1.
- **E5 (P3e, `git status` gardé)** : le G0 dit que (2) juge l'arbre de travail contre le commit résolu, pas contre le
  HEAD courant ; la garde juge désormais contre le commit résolu, et `git status` (non suivis, ignorés, et index contre
  HEAD courant) reste : un état que l'ancienne garde refusait reste refusé (règle : serrer, jamais desserrer). Q1.
- **E6 (P3e, attendu réécrit)** : l'attendu du test C-2 (i) passe de gardes levées à refus (2) seul, avec son motif ;
  correction du test commandée par la construction, non du code (comme E11 du G1 C-1).
- **E7 (P3f, `-G` au lieu de `-S` confirmé)** : la proposition du G1 de correction (confirmer S et Gc sur
  `git show <commit>:JOURNAL.md`) est tenue ; la liste des candidats vient de `-G` : pour tout commit qui n'est pas une
  fusion, la première ligne entière ajoute une ligne qui contient le sha, donc figure parmi les candidats ; `-S` la
  manque à nombre d'occurrences égal (sonde, mutant F3).
- **E8 (P3c, migration d'API)** : `tests/test_rendu_production.py` l.58 lit la fabrique ; changement mécanique fait avec
  le code (il ne teste pas l'item). Les journaux, G0 et annexes datés citent encore `CONTEXTE_DECIMAL` (sept documents ;
  recherche relancée avec les exclusions à la source, E11) : écrits datés, non réécrits ; le seul code qui le nomme
  encore est le script de l'autre worker (Q4).
- **E9 (preuves remplacées)** : `P3a-avant.out` d'une première passe (`00faa4d4…`, `SyntaxError` : littéral d'octets non
  ASCII dans le premier jet du test, corrigé avant toute preuve citée) et `P3f-avant.out` d'une première passe
  (`a0b5928e…`, arrêtée au premier écart, avant la mise en `subTest`) remplacés ; les fichiers cités sont les seconds.
- **E10 (périmètre du rejeu)** : les mutants des listes du correcteur G2 tournent sur l'arbre final avec mon moteur
  (même format de liste) ; aucune liste du G1 C-1 (autre moteur, arbre `s2-harness/` seul) n'a été rejouée.
- **E11 (recherche hors périmètre, pré-enregistrement)** : entre 14:56 et 14:58 UTC, un `grep -rl CONTEXTE_DECIMAL` sur
  l'arbre entier (fichiers `.md`, `.py`, `.rs`, `.sh`, `.yml`) a parcouru `docs/adr-0025/`, la cartographie du
  2026-09-29 et `JOURNAL.md`, dont les noms n'étaient retirés qu'à la sortie (`grep -v`) : le brief exigeait l'exclusion
  à la source. Exposition : aucune ; l'option `-l` n'imprime que des noms, ceux de ces fichiers ont été filtrés avant
  affichage, aucun contenu n'a été affiché (`grep` seul en a parcouru les octets) ; je ne sais pas s'ils contiennent la
  chaîne. Recherche relancée à 15:02 UTC avec
  `--exclude-dir=adr-0025 --exclude=cartographie-2026-09-29.md --exclude=JOURNAL.md` (et `biblio/`, `target/`,
  `.git/`) : mêmes sept documents datés, plus ce journal et le script de l'autre worker.

## 7. Équivalences

- **C2-g (P3e)** : avec le contrôle neuf et `git status` gardé, (2) refuse dès que le code de HEAD diffère de celui du
  commit résolu sur CHEMINS (arbre égal à HEAD : le diff contre X refuse ; arbre égal à X : `git status` refuse) ; s'il
  ne diffère pas, les deux diffs de commits rendent le même code. Aucune entrée ne distingue C2-g par la liste des
  refus ; son motif le distingue, et le test réécrit le lit (tué). Le diff des commits contre le commit résolu est gardé
  tel que la construction de C-2 le nomme.
- **C3-b (G2c)** : vivant, équivalence déclarée par le correcteur G2 (Gc = S implique ct(Gc) = ct(S)) ; inchangée.

## 8. Limites rencontrées (items à former, règle PAROXYSME)

| item proposé | objet et construction | propriétaire | déclencheur | prix |
|---|---|---|---|---|
| SHOGEN-SCEAU-VERIFY-DATA-1 | l'étape (2) de `verify.sh` vérifie le jeton contre la requête (`-queryfile`) seulement, jamais contre le manifeste sur le disque, et l'étape (3) imprime l'étiquette `Message data:` sans l'empreinte (lignes suivantes, filtrées) : paquet et manifeste réécrits d'accord après le jeton passent avec `SCEAU : VÉRIFIÉ HORS LIGNE` (sonde `sonde_sceau_data`). `rendu_unique` n'en dépend pas (voie (a), E2 du G1 C-1). Construction : ajouter à l'étape (2) `openssl ts -verify -in paquet.tsr -data "$D/PAQUET.sha256" -CAfile … -untrusted …`, et un cas à `test_sceau` (réécriture après le jeton : code 3) | orch. | G0 du PAQUET, avant la vérification hors ligne par l'investisseur | ≈ 2 lignes et un cas de test [inféré] |
| SHOGEN-P3-HOTE-1 | non éprouvé en session cloud : (a) la branche Windows du renommage final (`os.rename` seul) ; (b) les prérequis de `test_sceau` sur l'hôte (`bash`, `sha256sum` et `sed` de GNU dans le PATH, `openssl`), dont l'absence fait échouer le test, sans saut. Construction : la suite sur l'hôte, déjà exigée par SHOGEN-RENDU-HOTE-1 | orch. | SHOGEN-RENDU-HOTE-1 | une exécution [inféré] |
| SHOGEN-RENDU-RENAME-FENETRE-1 | sous POSIX, entre la création exclusive de la cible et le renommage, un acteur qui retirerait la réserve vide et poserait un autre répertoire vide le verrait remplacé (vide : aucune perte). Une construction atomique (`renameat2` et `RENAME_NOREPLACE`) n'existe pas dans la bibliothèque standard. Construction : limite écrite au PAQUET (garde contre l'erreur, pas contre un adversaire, comme SHOGEN-RENDU-JETON-MAIN-1) | orch. | G0 du PAQUET (texte) | une ligne de texte [inféré] |
| SHOGEN-GO-PICKAXE-FUSION-1 | `-G`, comme `-S`, ne lit pas le diff d'un commit de fusion : une ligne introduite par la résolution d'une fusion elle-même n'est pas candidate ; effet : S ou Gc plus tardif, ou refus (échec fermé). Construction : `--diff-merges=first-parent` sur l'appel, fixture d'une ligne posée par la résolution d'une fusion ; ou limite écrite si les lignes de scellement et de go ne sont jamais commises par une fusion | orch. | G0 du PAQUET | ≈ 1 ligne et une fixture [inféré] |

## 9. Questions pour l'orchestrateur

- **Q1 (E5)** : `git status` de (2) reste-t-il entier (plus strict : il juge encore l'index et l'arbre contre le HEAD
  courant), ou se réduit-il aux fichiers non suivis et ignorés (lecture littérale de la décision) ?
- **Q2 (E3)** : le contrôle de convention de `make-tsq.sh` est-il retenu comme part de la construction ?
- **Q3 (L1)** : SHOGEN-SCEAU-VERIFY-DATA-1 se corrige-t-il dans un complément de P3 ou au lot PAQUET ?
- **Q4 (P3c, intégration)** : `scripts/sim/sim_garde_niveau_oracle_r1.py` (autre worker, étape S, non suivi) appelle
  `localcontext(r1.CONTEXTE_DECIMAL)` (l.90 et l.137) ; après P3c, ce nom n'existe plus : s'il charge `r1` depuis
  l'arbre de travail, le script lève `AttributeError`. Remède à décider : le script lit `r1.contexte_decimal()` (deux
  lignes), ou il charge un `r1` figé à un commit antérieur à P3c ; un alias `CONTEXTE_DECIMAL` rétablirait l'objet
  partagé que l'item retire (non fait).

## 10. Clôture

- Suite finale (arbre de travail) : `Ran 382 tests in 43.145s`, `OK (skipped=2)` (`preuves/suite-P3f.out`,
  `d53bf86f…`) ; `SHOGEN_S2_CAMPAGNE_CONTROL` et `SHOGEN_RENDU_PRODUCTION` absentes (`env | grep -c` : 0).
- `cargo --locked xtask verify` avant ce journal (14:55 UTC) : `=== VERDICT GLOBAL : VERT ===`, rc 0 (S-G4 84 fichiers
  sur 84, S-G5 85 sur 85, corpus complet 125 artefacts sur 125, 252 fragments contrôlés ;
  `preuves/xtask-avant-journal.out`, `fcbc166b…`). Relance avec ce journal en place, et hook pre-commit versionné rejoué
  dans un clone jetable où le diff total et ce journal sont indexés : verdicts et sha256 dans le rapport de remise (un
  fichier ne porte pas son propre sha).
- `git status` final : douze fichiers modifiés (§5, `test_sceau.py` excepté), `s2-harness/tests/test_sceau.py` et ce
  journal neufs ; les trois fichiers de l'autre worker (§0) non touchés (Q4).
- Dettes : aucune hors des items proposés au §8 et des questions du §9.
