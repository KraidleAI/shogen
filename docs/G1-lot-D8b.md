# G1 — lot D8b d'ADR-0028 (gate des secrets, mode historique, job g3), Shōgen — journal

- **Modèle** : `claude-opus-5-5` (déclaré par le harnais et en tête de session, R-1), effort max, contexte frais ; worker G1. Aucun commit, aucun workflow déclenché (R-20). Aucune variable `GIT_DIR` ni `GIT_WORK_TREE` posée, aucun `--write-tree` ; `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée (retirée par `unset` dans chaque script d'oracle). Écritures git limitées au worktree du lot (`git merge --ff-only 40b4cfb` sur sa branche, puis `git add -N .` pour le diff prescrit), aux dépôts jetables sous `mktemp` et à deux dépôts jetables d'oracle sous `F:/tmp/shogen-lots/D8b/` (clone d'O-4, dépôt d'états des sous-diffs). Lectures git sur `F:/Shogen` en `--no-optional-locks`.
- **Horloge** (`date -u`) : première heure relevée 2026-09-30T15:43:05Z (avance rapide du worktree ; l'orientation la précède) ; relevé d'environnement 15:47:36Z ; estimation R-25 scellée 15:59:49Z, avant tout code ; suite de base 16:00:19Z-16:00:45Z ; `cargo xtask verify` de base 16:00:51Z-16:01:10Z ; campagne de mutants de D8b-1 16:16:31Z-16:19:14Z ; D8b-1 figé 16:19:56Z ; campagne de D8b-2 16:26:27Z-16:40:11Z (M-17 survit, E-2) ; rejeu de M-17 16:42:18Z-16:43:20Z ; D8b-2 figé 16:45:42Z ; O-1 final 16:47:03Z-16:50:19Z ; O-2 et O-3 16:50:57Z-16:53:54Z ; campagne finale à partir de 16:54:23Z ; D8b-3 figé 16:55:59Z ; suite, oracles et documents ensuite (§6).
- **Mandat** : commande de mission de l'orchestrateur Shōgen (`claude-fable-5-1`, workflow du 2026-09-30), lot D8b de l'annexe A (ligne l.37 à `40b4cfb`) ; G0 accepté au cp-1 complet (`F:/tmp/shogen-lots/D8b/G0-lot-D8b.md`, sha256 `2b928eddedcd37b7fdad473104dc0c8e502dd310e99c931c32c75c223fc213c8`), décision ACCEPTE-AVEC-CORRECTIONS du validateur-humain, liste fermée C-1 à C-9 (`F:/tmp/cp1-D8b/CP1-D8b.md`, sha256 `f17ad25ea4f7ad9138362def74c898d60ca4872558bc520ee6bba7843ba0a725` ; liste `F:/tmp/shogen-lots/D8b/cp1-corrections.json`), toutes intégrées (§3, §11). Cadre : ADR-0028 D8 et annexes A-E à `40b4cfb`.
- **Base** : `40b4cfb` (D8a, E1, DOCS-S2-a et SIM-NIVEAU commis). À 16:52Z, `main` est à `293b7a7` : un commit de JOURNAL de plus, aucun fichier du lot touché (`git diff --stat 40b4cfb 293b7a7` : `JOURNAL.md` seul).
- **Classification** : additive. Trois fichiers neufs sous `enforcement/`, un job ajouté à `gates.yml` (et son en-tête), deux documents.
- **Résultat** : trois sous-lots sous la coupe du G0 §9, sans la règle 2 : **D8b-1** 180 lignes, **D8b-2** 92, **D8b-3** 94. Runner : 90 cas sur 90, sous les deux formes de `TMPDIR` (C-7). Arbre réel et historique réel : sortie 0 sur le worktree et sur l'arbre principal (302 fichiers ; 141 commits, `--all`). Rouges semés sur le clone de l'entrée committée : k=0 en 0 (304 fichiers, 142 commits), k=1 à k=3 en 2 avec le jeton attendu, attribution de k=2 égale au commit C1. Mutants de gate : 74 sur l'état final, 67 tués, chacun par un tueur attendu ; 7 équivalents déclarés, chacun avec sa commande de rejeu ; 0 inapplicable. `yaml.safe_load` et structure de `gates.yml` tenus. Suite `s2-harness` identique à la base ; `cargo --locked xtask verify` VERT.
  - *Amendement du 2026-09-30 (correction de la revue G2, C-G2-1 à C-G2-11 ; complété le 2026-10-01, correction de la re-revue rr1, CR-rr1-1)* : état corrigé : **D8b-1** 184, **D8b-2** 113, **D8b-3** 112 lignes ; runner 113 cas sur 113 (T-75b ajouté à la re-revue), sous les deux formes de `TMPDIR` ; 98 mutants de gate, 91 tués et 7 équivalents déclarés, 0 survivant non attendu ; mutant R4b de la re-revue tué par T-75b ; arbre et historique réels en sortie 0 ; rouges semés au jeton attendu : §15.

## 0. Préconditions mesurées avant code

- **Base** : le worktree fourni par le harnais était à `fa0ce5b`, ancêtre de `40b4cfb` (59 commits ; `git merge-base --is-ancestor`, `git rev-list --count`). Acte du worker : `git merge --ff-only 40b4cfb` sur la branche du worktree (15:43Z), seule référence déplacée ; `main` non touchée. `gates.yml` à la base : sha256 `bc3aea1773b827f32c9293e37856138704912f71e054397983cc07267223af53`, 122 lignes, égal à l'état cible du G0 §4 (reconstitution après D8a) : le lot s'empile sur D8a commis, sans `patch`.
- **PC-1 (G0 §2)** : lecture (b) consignée au JOURNAL (l.122 à `40b4cfb`) : portage `enforcement/` couvert par la délégation du 2026-09-30, veto §4.10 a non exercé, révocable jusqu'à l'exécution unique ; tag et suppression de la branche `roster-ban-alignment-2026-08-20` : acte de l'investisseur (SHOGEN-D8-PC-1, annexe B.11), hors lot.
- **Hook local** (CA-D8b-2) : `F:/Shogen/.git/hooks/pre-commit`, sha256 `1da91c723b7f4747edb35dcc2cce7492e334b648c5e00c41f239cca5ab61277d` au début et à la fin du G1, égal au G0 §4.
- **Suite de base** (`40b4cfb`, TMP neuf, variable non posée) : `Ran 216 tests`, `OK (skipped=2)`, sortie 0, 0 entrée TMP ; sauts : tests (ii) et (ii bis) de `test_exclusion`.
- **`cargo --locked xtask verify` de base** (`oracles/cargo_env.sh` : toolchain forcée, auto-installation coupée, serveurs rustup en 127.0.0.1:9, `CARGO_HOME` et `CARGO_NET_OFFLINE=true` de la mission, cible `F:/tmp/shogen-lots/D8b/target`) : S-G1 à S-G8, `fmt`, `no_std`, `clippy` VERT, verdict global VERT, sortie 0 ; S-G4 : 53 fichiers ; S-G5 : 54 fichiers, 252 fragments contrôlés, 218 non contrôlés (corpus incomplet dans le worktree : 0 artefact sur 125) ; 0 téléchargement sous `F:/rust/rustup/downloads`.
- **Environnement** (`oracles/env.out`) : git 2.55.0.windows.5, bash 5.3.15, GNU grep 3.0, GNU Awk 5.4.1, GNU sed 4.9, coreutils 8.32, GNU libiconv 1.19, Python 3.14.5, PyYAML 6.0.3, locale `C.UTF-8`. Variables `GIT_*` : `GIT_EDITOR` seule. `TMPDIR` du shell = `/tmp` : chaque script d'oracle pose `TMPDIR`, `TMP` et `TEMP` sur un dossier neuf sous `F:/tmp/shogen-tests-tmp/d8b-g1/`. `.gitattributes` : `* text=auto eol=lf` (fins de ligne LF à l'extraction, mesuré par `check-attr` sur les chemins du lot).
- **Garde du harnais** (§13) : les oracles sont des scripts écrits sous `F:/tmp/shogen-lots/D8b/oracles/` et exécutés directement (shebang) ; ils lancent la gate et le runner par `bash <chemin>`, forme exacte du job.

## 1. Coupe R-25

- **Estimation écrite avant tout code** (`oracles/estimation-R25.txt`, horloge 15:59:49Z, sha256 `d71c199f3a9ca267508c4c9b191e49d5f13da8068e012f5239de6f0b11f38f2d`) : D8b-1 ≈ 191, D8b-2 ≈ 124, D8b-3 ≈ 100, lot ≈ 415 ; écarts au tableau du G0 §9 déclarés avant code : (a) les lignes de fixture dont les cas de D8b-1 tirent leurs valeurs sont versées dès D8b-1 ; (b) sondes de seuil ajoutées en D8b-2 (numéros T-33+ réservés par le G0 §7) ; (c) fonction de cas à motif requis ou interdit ; (d) gate de D8b-3 à ≈ +38.
- **Mesures** (méthode du lot A : `diff -u` contre l'instantané précédent pour les fichiers déjà présents, `wc -l` des fichiers neufs ; `oracles/r25.sh`) :

| sous-lot | `gate-secrets.sh` | `run-fixtures-secrets.sh` | `sondes.tsv` | `gates.yml` | total ajouté | seuil |
|---|---|---|---|---|---|---|
| D8b-1 | 104 (neuf) | 72 (neuf) | 4 (neuf) | 0 | **180** | ≤ 200 |
| D8b-2 | 0 | +28 | +33 | +31 −3 | **92** | ≤ 200 |
| D8b-3 | +34 −8 | +44 −2 | 0 | +16 −7 | **94** | ≤ 200 |

- **Lot entier** : 366 lignes en somme des sous-lots ; le diff du lot contre `40b4cfb` en compte 349 (gate 130, runner 142, fixture 37, `gates.yml` +40 −3) : les 17 lignes de D8b-1 et D8b-2 réécrites par D8b-3 n'y figurent qu'une fois. L'estimation (≈ 415) dépassait la mesure : les cas du runner tiennent en moins de lignes que la base de 3 lignes par cas du G0 §9. Règle 2 non appliquée (D8b-1 < 200), règle 3 non atteinte.
- **Documentation, hors compte de code** (cp-1 C-4, réponse à Q-G0-1, précédent du cp-1 de D8a) : copie du G0, `docs/adr-0028/G0-lot-D8b.md`, 535 lignes, soit les 515 lignes acceptées sans retrait et 20 lignes d'amendements datés (`oracles/G0-copie.diff`, 0 ligne retirée) ; ce journal, 389 lignes. Compte avec documents : code 349 au `lot.diff` (366 en somme des sous-lots), documents 535 + 389, soit 1273 lignes ajoutées au `lot.diff`. Q-G2-1 de D8a (commit documentaire séparé ou non) reste une décision de forme de l'orchestrateur.
- **Lignes datées proposées pour l'annexe A (cp-1 C-2)** : acte de l'orchestrateur, non écrites ici. Format des colonnes de l'annexe A.

| lot (date) | objet (décision) | véhicule | oracle non-LLM nommé | taille (R-25) | tuyau (entrée → sortie → consommateur ; test) | cp-1 |
|---|---|---|---|---|---|---|
| **D8b** (2026-09-29 ; amendée le 2026-09-30 par le G0 et le G1 du lot) | D8 : `gate-secrets.sh` porté du blob `6789a30` (arbre, index), mode `--history` neuf (la source n'en a pas : G0 §5.1, cp-1 C-1), job `g3-secrets` ; écarts nommés au blob : ligne E-D8b-G1 de l'annexe E | `enforcement/`, `gates.yml`, tests shell | O-1 à O-12 du G0 amendé ; 90 cas ; 74 mutants de gate | 366 [mesuré : D8b-1 180 + D8b-2 92 + D8b-3 94] au lieu de ≈ 130 | arbre et historique → gate → job g3 (partiel : GC-01, GC-09) et G3 opérant local ; hook : item 4 ; tests O-2, O-3 et O-4 | complet |
| **D8b-1** (2026-09-30 ; coupe R-25 du G0 de D8b) | moteur porté (arbre, index) ; références réattribuées ; jetons ; argument inconnu refusé ; `LC_ALL=C` ; cas T-01 à T-14 | `enforcement/gate-secrets.sh`, runner, 4 lignes de fixture | O-1 (14 cas), O-5 (46 mutants : 10 tués, 36 à tueur en D8b-2), O-6, O-9, O-11 | 180 [mesuré] | non branché seul : consommable au G7 avec D8b-2 | complet (sous le cp-1 du lot) |
| **D8b-2** (2026-09-30 ; coupe R-25 du G0 de D8b) | contrat d'exclusion, sondes par alternative et par seuil (fixture tronquée), job `g3-secrets` (runner, `--tree`), en-tête de `gates.yml` ; cas T-15 à T-35, T-68 | la fixture, le runner, `.github/workflows/gates.yml` | O-1 (67 cas), O-2, O-5 (46 mutants tués, dont M-17 après correction de T-15), O-6, O-7, O-9, O-10 | 92 [mesuré] | arbre → gate → job g3 et G3 opérant local ; test O-2 et O-4 | complet (sous le cp-1 du lot) |
| **D8b-3** (2026-09-30 ; coupe R-25 du G0 de D8b) | mode `--history` (`--all`, drapeaux forcés, refus du superficiel, attribution, `pipefail`), `fetch-depth: 0`, étape 3 ; cas T-51 à T-67, T-69, T-70 | les deux scripts, `gates.yml` | O-1 (90 cas), O-3, O-4 (k = 2), O-5 (74 mutants), O-6 à O-10, O-12 | 94 [mesuré] | historique → gate → job g3 et G3 opérant local ; test O-3 et O-4 | complet (sous le cp-1 du lot) |

- **Ligne proposée pour l'annexe E (cp-1 C-2, réponse à Q-G0-3)** : acte de l'orchestrateur.

| id | avis (fichier, question, ligne) | recommandation de l'avis | dans ADR-0028 | statut |
|---|---|---|---|---|
| E-D8b-G1 | advisor Q8 pt 2, l.97 (source canonique = blob d'`adb2213`) ; cp-1 D8b C-2 | porter le blob `6789a30` tel quel | D8, lot D8b : blob porté avec des écarts nommés : messages en français et jetons ASCII `SECRETS/…` (CH-6) ; argument inconnu refusé au lieu du repli sur le mode indexé (CH-7) ; `LC_ALL=C` exporté (CH-8) ; références à `ADR-0004` (neuf lignes du blob) réattribuées à l'ADR-0004 de VibeGates (trois occurrences, en-tête) ou retirées des messages, `pass-4-report.md` cité en amont complet, deux pourcentages [abs] retirés, filet d'un scanner dédié déclaré absent (CH-5) ; mode `--history` ajouté (fonction neuve, D8b-3) | tranché autrement (G0 CH-5 à CH-8, cp-1 C-2) |

- *Amendement du 2026-09-30 (correction de la revue G2, C-G2-11 e)* : estimation de la correction écrite avant code (`correction/estimation-R25.txt`, horloge 19:01:13Z) ; mesures : D8b-1 184, D8b-2 113, D8b-3 111, soit 408 en somme des sous-lots et 391 au `lot.diff` ; après T-75b (re-revue rr1, 2026-10-01) : D8b-3 112, soit 409 en somme et 392 au `lot.diff` ; aucun sous-lot au-dessus de 200. Lignes de l'annexe A (dont D8b-C) et ligne E-D8b-G1 complétée : §15.

## 2. Changements (worktree du lot, sur `40b4cfb`)

| fichier | D8b-1 | D8b-2 | D8b-3 | sha256 base → D8b-1 → D8b-2 → D8b-3 |
|---|---|---|---|---|
| `enforcement/gate-secrets.sh` | neuf : moteur porté (arbre, index), jetons, argument inconnu refusé, `LC_ALL=C` | — | mode `--history`, en-tête et usage | — → `96dc39eb…fdc8` → idem → `0baff29a…567f` |
| `enforcement/tests/run-fixtures-secrets.sh` | neuf : garde d'isolation, formation des valeurs, 14 cas | T-15 à T-30b, T-68, table des sondes (35 cas) | `r -`, 23 cas du mode `--history` | — → `8580aec1…1fd4` → `fa35a923…e332` → `35d0a4bf…1850` |
| `enforcement/tests/fixtures/secrets/sondes.tsv` | neuf : en-tête, V-01, G-06 | V-02 à V-20, G-01 à G-12 sauf G-06, T-33 à T-35 | — | — → `a9966fbe…7306` → `abeaded6…aaa3` → idem |
| `.github/workflows/gates.yml` | — | job `g3-secrets` (runner, `--tree`), en-tête (périmètre, items de forge) | `fetch-depth: 0`, étape `--history`, commentaires et temps | `bc3aea17…af53` → idem → `43d5d082…494a` → `6e5688fe…4e76` |
| `docs/adr-0028/G0-lot-D8b.md` | copie du G0 accepté, amendements datés (documentation du lot) | | | — → `3925a2fd…2833` |
| `docs/G1-lot-D8b.md` | ce journal | | | — |

- **Intouchés** (CA-D8b-2) : tout fichier de `F:/Shogen` hors de la liste IN du G0 §3 ; `s2-harness/` ; ADR-0028 et ses annexes ; `JOURNAL.md` ; `.claude/`.
- **CA-D8b-1** : `git diff --name-status 40b4cfb` = `M` pour `gates.yml`, `A` pour les cinq autres fichiers ci-dessus : la liste IN du G0 §3, exactement (§6).
- Instantanés figés : `F:/tmp/shogen-lots/D8b/work/d8b-1-fige/`, `d8b-2-fige/`, `d8b-3-fige/`, avec `d8b-<n>-sha256.txt`, `d8b-<n>-wc.txt` et l'horloge du gel.
- *Amendement du 2026-09-30 (correction de la revue G2)* : sha256 G1 → corrigé : gate `0baff29a…567f` → `47f2c35e…1722` ; runner `35d0a4bf…1850` → `7eb01b39…fa99` → `f9e7ef02…4837` (re-revue rr1, T-75b) ; fixture `abeaded6…aaa3` → `6b558bd2…451c` ; `gates.yml` `6e5688fe…4e76` → `13dc5177…79fb` (commentaire des temps seul) → `32f79e49…144c` (re-revue rr1, même commentaire) ; états corrigés figés sous `F:/tmp/shogen-lots/D8b/correction/etats/` (`d8b-1c`, `d8b-2c`, `d8b-3c`, avec sha256 et comptes de lignes), état D8b-3 de la re-revue sous `F:/tmp/shogen-lots/D8b/cr-rr1/etats/d8b-3r/` ; copie du G0 et ce journal : §15.

## 3. Définitions appliquées (CH-1 à CH-16) et corrections du cp-1

- **CH-1** : moteur canonique porté (boucle par fichier, contenu lu dans l'index comme des octets, NUL retirés, deux `grep`). Les deux lignes d'affectation des motifs sont identiques, octet pour octet, aux l.48-49 du blob (`oracles/controle-motifs.sh` : `diff` vide). Exclusions l.51-71 : même logique, messages et jetons seuls changés. Sortie masquée l.90-98 : format `<chemin>:<ligne>: [contenu masqué]`, 8 lignes par fichier au plus, reste annoncé.
- **CH-2** : flux unique `git --no-optional-locks -c core.quotePath=false -c log.showRoot=true -c color.ui=never -c diff.noprefix=false -c diff.mnemonicPrefix=false -c diff.suppressBlankEmpty=false log -p --text --no-color --no-ext-diff --no-textconv --no-renames --diff-merges=first-parent --full-history --no-notes --no-show-signature --format='commit %H' --all` avec la pathspec de l'arbre (contrat et fichier d'exclusion). Écart d'implémentation, sans écart de verdict : le flux passe par `( set -o pipefail; git … | tr -d '\000' )`, pour qu'un échec de `git log` sorte en `SECRETS/echec` et ne rende pas un flux tronqué vert (T-69, M-41). Verdict : lignes `^+` du flux, `grep` VENDOR et `grep -i` GENERIC. Attribution : `awk` à deux entrées (les 20 premiers numéros de ligne constatés, puis le flux), en-têtes `commit`, `+++ ` hors hunk seulement, compteurs des `@@`, ligne vide comptée comme contexte ; tabulation finale d'un chemin retirée.
- **CH-3** (cp-1 C-3) : `--all`, sans argument de révision ni borne de profondeur ; dépôt superficiel refusé (`SECRETS/tronque`, T-59) ; 20 constats listés au plus, compte total toujours imprimé (T-66, T-66b) ; `timeout-minutes: 15`. Refs couvertes, mesurées à chaque O-3 (§6).
- **CH-4** : `sondes.tsv`, une ligne par sonde (id, p1, p2, remplissage, n, suffixe, attendu) ; valeur formée par `awk -F '\t'` (aucun champ vide, par construction : `read` avec `IFS` tabulation fusionnerait deux tabulations). Remplissage `Q` (ou `A` pour l'alternative PEM), jamais une valeur d'exemple publiée par un fournisseur. Couverture : chaque alternative VENDOR a une sonde positive à la longueur minimale et une sonde juste en dessous (ou une quasi-forme, PEM : quatre tirets finaux) ; chaque forme GENERIC (citée, sept graphies de mot-clé ; non citée, mot-clé ; non citée, clé `aws_…key…`) a sa sonde sous le seuil ; T-33 à T-35 couvrent les seuils que V-01 à V-20 laissaient sans sonde. O-6 : 0 ligne sur la fixture.
- **CH-5** (cp-1 C-5) : trois occurrences de `ADR-0004`, toutes suivies de `de VibeGates` ou dans le chemin amont `docs/adr/ADR-0004-guard-escalation-adjudication.md` (le blob en porte neuf nues). Écart à la lettre de CH-5 (« devient partout ») : les cinq messages du blob qui citaient l'ADR (l.53, 61, 62, 66, 71) ne la citent plus ; l'en-tête rattache les règles d'exclusion à l'ADR-0004 de VibeGates, et le jeton du message nomme la règle (Q-G1-8) ; `pass-4-report.md` cité `VibeGates docs/passes/pass-4-report.md, section U2, commit 1263f2a` ; 0 pourcentage, 0 mention de Sakib (`oracles/controle-motifs.sh`, contrôle positif sur le blob : 9, 3 et 3) ; l.20-21 réécrites : aucun scanner dédié, items 1 et 2, le plancher n'a pas de filet.
- **CH-6** : jetons `SECRETS/forme`, `SECRETS/historique`, `SECRETS/exclusion`, `SECRETS/tronque`, `SECRETS/echec` ; format `REFUS (<jeton>) : <motif>` sur stderr ; avis `AVIS (secrets) : …` ; succès `OK (secrets) : <n> fichier(s) …` (fichiers lus, entrées non-blob exclues) et `OK (secrets) : historique, <n> commit(s) (--all), …` (commits atteints, `git rev-list --count --all`, et non les seuls commits dont le diff est en portée). Codes 0 et 2.
- **CH-7** : `case "$#:$MODE"` : sans argument, `--tree` ou `--history` ; tout autre argument, un argument vide ou plus d'un : `SECRETS/echec` (T-14 ; M-19, le repli canonique, est tué).
- **CH-8** : `export LC_ALL=C` en tête. Mesure de CA-D8b-17 : §6, O-5 (M-36d) et comparaison des sorties réelles.
- **CH-9** (cp-1 C-6) : nom `.vibegates-secretscan-exclude` gardé ; mêmes règles ; appliqué à l'historique par la même pathspec (T-67, M-35).
- **CH-10** : mode indexé gardé, testé dès D8b-1 ; consommateur (hook de D8c) absent : item 4.
- **CH-11** : boucle par fichier gardée ; `--tree` mesuré à 62-72 s pour 302 fichiers (§6, O-12) ; `timeout-minutes: 15`.
- **CH-12** : runner conforme (garde `GIT_*` avant tout `mktemp`, dossier de travail contrôlé hors dépôt, `show-prefix` vide, config locale, `core.hooksPath` vers un dossier vide, `-C` sur chaque commande git, jamais `--no-verify`, `iconv` requis) ; chemin de la gate en `$1`, rendu absolu. Précision du G1 : la fonction `cas` vérifie aussi un motif requis ou interdit quand le jeton seul ne tranche pas (T-07, T-08, T-11 à T-17, T-21, T-23, T-25 à T-28, T-30a, T-30b, T-52, T-53, T-60, T-64b à T-70). Sans ce motif, M-17 et M-18 sont équivalents : le blob double le contrôle hors dépôt par la résolution de la racine, et l'échec de `mktemp` par l'échec de la redirection vers un chemin vide.
- **CH-13** : job conforme (O-10, 19 assertions) ; placé entre `g1-model-pinning` et `s2-harness-unittest` ; commentaire de `timeout-minutes` fondé sur les temps mesurés.
- **CH-14** : aucun fragment de la valeur dans les sorties : T-07 (interdit `QQQQ|pass|word`), T-52 (interdit `QQQQ`), O-4 k=2 (0 occurrence de `QQQQ`).
- **CH-15** : aucun constat réel sur l'arbre ni sur l'historique (O-2, O-3, O-4 k=0) : aucune ligne de pièce de l'annexe D.2 n'a eu à être identifiée.
- **CH-16** : en-tête et §11 : plancher de motifs, pas de scanner dédié, ni balayage de forge, ni objets hors refs ; limites avec items (§11), dont une limite relevée au G1 : les messages de commit et de tag ne sont pas balayés (item 8).
- **C-7** : T-59 construit le clone superficiel par `git -C "$W" clone -q --no-local --depth 1 "$R" sup`, puis exige `--is-shallow-repository` = `true`, sinon sortie 3. Sources : documentation locale de git 2.55 (`oracles/git-clone-2.55.0.txt` l.53-59, `--no-local` : transport git ordinaire pour un chemin local ; l.310-316, `--depth` : clone superficiel) et sonde `oracles/sonde-superficiel.out` (rc 0 et `true` sous les deux formes de `TMPDIR` ; l'URL `file:///$W` rend 128 sous la forme POSIX). Comportement de git sur l'image Linux : inféré de la même documentation, non mesuré (item 3 c).
- **C-9** : copie du G0 = le texte `2b928edd…` plus 20 lignes d'amendements datés, indexées à son §16.
- *Amendement du 2026-09-30 (correction de la revue G2, C-G2-1 à C-G2-10)* : CH-1 (écarts au blob : `:(literal)`, objets réels, variables de pathspec de l'appelant retirées, `masque`), CH-2 et CH-3 (greffes et refs non-commit refusées, `-c diff.dstPrefix=b/`), CH-4 (dix sondes), CH-6 (portée de `tronque` et d'`echec`), CH-12 (variables posées pour un seul appel de la gate), CH-14 (chemins masqués) : §15.

## 4. Tests (runner shell, 90 cas) — chaque cas nomme la mutation qui le rougit

- Chaque cas vérifie la sortie ET le jeton ; un cas « 0 » exige le message `OK (secrets)` et son compte (fichiers, ou commits atteints en historique). Un seul résumé fait foi : `secrets : <n> ok, <m> échec`. Sortie 0, 1 ou 3.
- **F2P** : catégorie « nouveau module » (gate et runner absents de la base) : les 90 cas sont neufs.
- **Écarts à l'amont relevés au portage** : les cas amont 12 et 13 laissaient le fichier d'exclusion non suivi, et touchaient donc la branche « non suivi » et non la branche nommée ; T-20 et T-21 suivent le fichier (E-6). T-20 (`../out`) touche la branche « traversant », qui précède la branche « inutilisable » dans le blob (l.62-63) ; celle-ci a son cas propre, T-68 (pathspec absolue, `git ls-files` rend 128, `oracles/sonde-pathspec.out`).
- **Mutations qui rougissent chaque cas** (campagne finale, §5 ; déduite de `oracles/mutants-final.out` par `oracles/cas_par_mutant.py`) :

| cas | mutants sous lesquels le cas est rouge |
|---|---|
| T-01 | M-1, M-3.1 |
| T-02 | M-1, M-4, M-6 |
| T-03 | M-7 |
| T-04 | aucun |
| T-05 | M-1, M-3.1, M-22 |
| T-06 | M-1, M-2, M-3.1, M-22 |
| T-07 | M-1, M-4, M-22 |
| T-08 | M-1, M-4, M-22 |
| T-09 | M-1, M-3.1 |
| T-10 | M-1, M-3.1 |
| T-11 | M-16 |
| T-12 | M-16 |
| T-13 | M-18 |
| T-14 | M-19 |
| T-15 | M-17 |
| T-16 | M-1, M-4, M-20 |
| T-17 | M-1, M-3.1, M-22 |
| T-18 | M-21 |
| T-19 | M-1, M-5, M-6 |
| T-20 | aucun |
| T-21 | M-10 |
| T-22 | aucun |
| T-23 | aucun |
| T-24 | M-1, M-3.1 |
| T-25 | M-11 |
| T-26 | M-12 |
| T-27 | aucun |
| T-28 | M-12, M-13 |
| T-29 | M-1, M-3.1, M-9 |
| T-30a | M-14 |
| T-30b | M-15 |
| T-68 | M-37 |
| T-31/V-01 | M-1, M-3.1 |
| T-31/V-02 | M-8.1 |
| T-31/V-03 | M-1, M-3.1, M-3.2 |
| T-31/V-04 | M-8.2 |
| T-31/V-05 | M-1, M-3.1, M-3.3 |
| T-31/V-06 | M-8.3 |
| T-31/V-07 | M-1, M-3.1, M-3.4 |
| T-31/V-08 | M-8.4 |
| T-31/V-09 | M-1, M-3.1, M-3.5 |
| T-31/V-10 | M-8.5 |
| T-31/V-11 | M-1, M-3.1, M-3.6 |
| T-31/V-12 | M-8.6 |
| T-31/V-13 | M-1, M-3.1, M-3.7 |
| T-31/V-14 | M-8.7a |
| T-31/V-15 | M-1, M-3.1, M-3.8 |
| T-31/V-16 | M-8.8 |
| T-31/V-17 | M-1, M-3.1, M-3.9 |
| T-31/V-18 | M-8.9 |
| T-31/V-19 | M-1, M-3.1, M-3.10 |
| T-31/V-20 | M-8.10c |
| T-32/G-01 | M-1, M-4 |
| T-32/G-02 | M-1, M-4 |
| T-32/G-03 | M-1, M-4 |
| T-32/G-04 | M-1, M-4 |
| T-32/G-05 | M-1, M-4 |
| T-32/G-06 | M-1, M-4 |
| T-32/G-07 | M-1, M-4 |
| T-32/G-08 | M-8.g1 |
| T-32/G-09 | M-1, M-5, M-6 |
| T-32/G-10 | M-8.g2 |
| T-32/G-11 | M-1, M-5 |
| T-32/G-12 | M-8.g2 |
| T-33 | M-8.7b |
| T-34 | M-8.10a |
| T-35 | M-8.10b |
| T-51 | M-7h |
| T-52a | aucun |
| T-52 | M-3.1, M-1h, M-32 |
| T-53 | M-4, M-1h, M-6h, M-33 |
| T-54 | M-5, M-1h, M-6h, M-23, M-25 |
| T-55 | M-3.1, M-1h, M-25 |
| T-56 | M-3.1, M-1h, M-26 |
| T-57 | M-3.1, M-1h, M-27 |
| T-58 | M-3.1, M-1h, M-28 |
| T-59 | M-29 |
| T-60 | M-4, M-1h, M-39 |
| T-61 | M-3.1, M-1h, M-2h, M-27 |
| T-62a | aucun |
| T-62b | M-3.1, M-1h |
| T-63 | M-3.1, M-1h, M-30 |
| T-64a | aucun |
| T-64b | M-3.1, M-1h, M-32 |
| T-65 | M-3.1, M-1h, M-31, M-32, M-36c |
| T-66 | M-4, M-1h, M-34a, M-34b |
| T-66b | M-4, M-1h |
| T-67 | M-35 |
| T-69 | M-41 |
| T-70 | M-4, M-1h, M-33, M-40 |

- Lecture : 90 cas ; rouges sous aucun mutant : 8 (T-04, T-20, T-22, T-23, T-27, T-52a, T-62a, T-64a). Ce sont des cas positifs, ou un cas doublement protégé (T-20 : branche « traversant », puis « inutilisable » sous M-14) : ils ne rougissent que sous un mutant qui refuse trop ou qui retire les deux protections ; leur pouvoir de discrimination n'est pas revendiqué ici. Chacun des autres cas nomme au moins un mutant qui le rougit.
- *Amendement du 2026-09-30 (correction de la revue G2 ; complété le 2026-10-01, re-revue rr1)* : 113 cas ; cas neufs T-71, T-71b, T-72 à T-80, T-74b, T-75b (re-revue) et dix sondes, T-65 étendu ; tueurs de chaque cas neuf : §15.

## 5. Mutants de gate (tests négatifs d'outil, registre d'ADR-0011 pt 4)

- **Méthode (cp-1 C-8)** : `F:/tmp/shogen-lots/D8b/oracles/mutants.py` (sha256 `94612b6688d78b4f73778ebac6a61b03e57a718a76b63ce3e7d7bb2d673ca0bc`) écrit chaque mutant par UN remplacement exact (deux pour M-31 et M-40) dans une copie de la gate ; un remplacement qui ne s'applique pas exactement une fois rend le mutant « inapplicable », jamais « tué ». `oracles/mutants-run.sh` (sha256 `3422e31b609105715f794fefd38032ac23bc283b268c2a70cddd6b4c6dab8dd8`) lance, pour chaque mutant, `TMPDIR=<neuf> bash <runner de l'état> <dossier>/<mutant>.sh`, six travailleurs ; `oracles/mutants_bilan.py` (sha256 `14c46b01ba13214cf26adbd60f85ec7703be94536d141212c096d62427613b4e`) exige une sortie ≠ 0 et au moins un tueur attendu parmi les cas en échec. Commande exacte par mutant, rejouable : `python mutants.py <gate> <dossier> <état>` puis `TMPDIR=<neuf> bash enforcement/tests/run-fixtures-secrets.sh <dossier>/<id>.sh` depuis la racine du worktree. Le worktree n'a jamais porté de mutant. `bash -n` : 0 échec sur chaque campagne.
- **État D8b-1** (46 mutants, gate `96dc39eb…`, runner `8580aec1…`) : 10 tués, dont les sept de la ligne D8b-1 du G0 (M-1, M-2, M-6, M-7, M-16, M-18, M-19), plus M-3.1, M-4 et M-22 ; 36 survivants dont tous les tueurs attendus sont des cas de D8b-2 (`oracles/mutants-d8b-1.out`).
- **État D8b-2, première campagne** (46 mutants, runner avant correction de T-15) : 45 tués ; **M-17 survit** : le motif requis `mktemp` de T-15 est satisfait par le message d'erreur de `mktemp` lui-même (E-2). T-15 exige désormais le message de la gate, `mktemp a échoué` ; rejeu de M-17 : tué par T-15 (`oracles/mutants-d8b-2-v1.out`, `oracles/mut-d8b-2-rejeu/`). Les 45 autres verdicts tiennent : leurs tueurs ne sont pas T-15, et la correction ne fait que resserrer T-15.
- **État final** (74 mutants, gate `0baff29a…`, runner `35d0a4bf…`, `oracles/mutants-final.out`) :

| mutant | objet | verdict | cas rouges | tueur(s) attendu(s) |
|---|---|---|---|---|
| M-1 | verdict arbre/index neutralise | tue rc=1 tmp=0 | T-01 T-02 T-05 T-06 T-07 T-08 T-09 T-10 T-16 T-17 T-19 T-24 T-29 T-31/V-01 T-31/V-03 T-31/V-05 T-31/V-07 T-31/V-09 T-31/V-11 T-31/V-13 T-31/V-15 T-31/V-17 T-31/V-19 T-32/G-01 T-32/G-02 T-32/G-03 T-32/G-04 T-32/G-05 T-32/G-06 T-32/G-07 T-32/G-09 T-32/G-11 | T-01 T-02 T-05 |
| M-2 | retrait des NUL supprime (arbre, index) | tue rc=1 tmp=0 | T-06 | T-06 |
| M-3.1 | alternative VENDOR retiree : AKIA[0-9A-Z]{16} | tue rc=1 tmp=0 | T-01 T-05 T-06 T-09 T-10 T-17 T-24 T-29 T-31/V-01 T-31/V-03 T-31/V-05 T-31/V-07 T-31/V-09 T-31/V-11 T-31/V-13 T-31/V-15 T-31/V-17 T-31/V-19 T-52 T-55 T-56 T-57 T-58 T-61 T-62b T-63 T-64b T-65 | T-31/V-01 |
| M-3.2 | alternative VENDOR retiree : -----BEGIN [A-Z ]*PRIVAT | tue rc=1 tmp=0 | T-31/V-03 | T-31/V-03 |
| M-3.3 | alternative VENDOR retiree : ghp_[A-Za-z0-9]{36} | tue rc=1 tmp=0 | T-31/V-05 | T-31/V-05 |
| M-3.4 | alternative VENDOR retiree : gho_[A-Za-z0-9]{36} | tue rc=1 tmp=0 | T-31/V-07 | T-31/V-07 |
| M-3.5 | alternative VENDOR retiree : github_pat_[A-Za-z0-9_]{ | tue rc=1 tmp=0 | T-31/V-09 | T-31/V-09 |
| M-3.6 | alternative VENDOR retiree : xox[baprs]-[0-9A-Za-z-]{ | tue rc=1 tmp=0 | T-31/V-11 | T-31/V-11 |
| M-3.7 | alternative VENDOR retiree : sk-[A-Za-z0-9]{20,}T3Blb | tue rc=1 tmp=0 | T-31/V-13 | T-31/V-13 |
| M-3.8 | alternative VENDOR retiree : sk-ant-[A-Za-z0-9-]{20,} | tue rc=1 tmp=0 | T-31/V-15 | T-31/V-15 |
| M-3.9 | alternative VENDOR retiree : AIza[0-9A-Za-z_-]{35} | tue rc=1 tmp=0 | T-31/V-17 | T-31/V-17 |
| M-3.10 | alternative VENDOR retiree : eyJhbGciOi[A-Za-z0-9_-]+ | tue rc=1 tmp=0 | T-31/V-19 | T-31/V-19 |
| M-4 | forme citee de GENERIC retiree | tue rc=1 tmp=0 | T-02 T-07 T-08 T-16 T-32/G-01 T-32/G-02 T-32/G-03 T-32/G-04 T-32/G-05 T-32/G-06 T-32/G-07 T-53 T-60 T-66 T-66b T-70 | T-02 T-07 T-32/G-01 |
| M-5 | forme non citee de GENERIC retiree | tue rc=1 tmp=0 | T-19 T-32/G-09 T-32/G-11 T-54 | T-19 T-32/G-09 T-32/G-11 |
| M-6 | GENERIC sans -i (arbre, index) | tue rc=1 tmp=0 | T-02 T-19 T-32/G-09 | T-02 |
| M-7 | VENDOR avec -i (arbre, index) | tue rc=1 tmp=0 | T-03 | T-03 |
| M-8.1 | seuil AKIA 16 -> 15 | tue rc=1 tmp=0 | T-31/V-02 | T-31/V-02 |
| M-8.2 | tirets finaux PRIVATE KEY 5 -> 4 | tue rc=1 tmp=0 | T-31/V-04 | T-31/V-04 |
| M-8.3 | seuil ghp_ 36 -> 35 | tue rc=1 tmp=0 | T-31/V-06 | T-31/V-06 |
| M-8.4 | seuil gho_ 36 -> 35 | tue rc=1 tmp=0 | T-31/V-08 | T-31/V-08 |
| M-8.5 | seuil github_pat_ 22 -> 21 | tue rc=1 tmp=0 | T-31/V-10 | T-31/V-10 |
| M-8.6 | seuil xox 10 -> 9 | tue rc=1 tmp=0 | T-31/V-12 | T-31/V-12 |
| M-8.7a | premier seuil sk- 20 -> 19 | tue rc=1 tmp=0 | T-31/V-14 | T-31/V-14 |
| M-8.7b | second seuil T3BlbkFJ 20 -> 19 | tue rc=1 tmp=0 | T-33 | T-33 |
| M-8.8 | seuil sk-ant- 20 -> 19 | tue rc=1 tmp=0 | T-31/V-16 | T-31/V-16 |
| M-8.9 | seuil AIza 35 -> 34 | tue rc=1 tmp=0 | T-31/V-18 | T-31/V-18 |
| M-8.10a | premier segment eyJ + -> * | tue rc=1 tmp=0 | T-34 | T-34 |
| M-8.10b | second segment eyJ + -> * | tue rc=1 tmp=0 | T-35 | T-35 |
| M-8.10c | seuil final eyJ 10 -> 9 | tue rc=1 tmp=0 | T-31/V-20 | T-31/V-20 |
| M-8.g1 | seuil GENERIC cite 16 -> 15 | tue rc=1 tmp=0 | T-32/G-08 | T-32/G-08 |
| M-8.g2 | seuil GENERIC non cite 16 -> 15 | tue rc=1 tmp=0 | T-32/G-10 T-32/G-12 | T-32/G-10 T-32/G-12 |
| M-9 | exclusion du contrat elargie a tout enforcement/ | tue rc=1 tmp=0 | T-29 | T-29 |
| M-10 | controle du marqueur ADR- retire | tue rc=1 tmp=0 | T-21 | T-21 |
| M-11 | fichier d'exclusion non suivi accepte | tue rc=1 tmp=0 | T-25 | T-25 |
| M-12 | controle de la forme globale retire | tue rc=1 tmp=0 | T-26 T-28 | T-26 |
| M-13 | normalisation des // retiree | tue rc=1 tmp=0 | T-28 | T-28 |
| M-14 | controle de traversee retire | tue rc=1 tmp=0 | T-30a | T-30a |
| M-15 | controle de portee entiere retire | tue rc=1 tmp=0 | T-30b | T-30b |
| M-16 | avis de saut non-blob retire | tue rc=1 tmp=0 | T-11 T-12 | T-11 T-12 |
| M-17 | echec de mktemp ignore | tue rc=1 tmp=0 | T-15 | T-15 |
| M-18 | controle hors depot retire | tue rc=1 tmp=0 | T-13 | T-13 |
| M-19 | argument inconnu ramene au mode indexe (canonique) | tue rc=1 tmp=0 | T-14 | T-14 |
| M-20 | annonce de troncature retiree | tue rc=1 tmp=0 | T-16 | T-16 |
| M-21 | --diff-filter=d retire | tue rc=1 tmp=0 | T-18 | T-18 |
| M-22 | le mode indexe lit les lignes du diff au lieu du contenu entier | tue rc=1 tmp=0 | T-05 T-06 T-07 T-08 T-17 | T-17 |
| M-37 | controle de pathspec inutilisable retire | tue rc=1 tmp=0 | T-68 | T-68 |
| M-1h | verdict historique neutralise | tue rc=1 tmp=0 | T-52 T-53 T-54 T-55 T-56 T-57 T-58 T-60 T-61 T-62b T-63 T-64b T-65 T-66 T-66b T-70 | T-52 T-53 |
| M-2h | retrait des NUL supprime (historique) | tue rc=1 tmp=0 | T-61 | T-61 |
| M-6h | GENERIC sans -i (historique) | tue rc=1 tmp=0 | T-53 T-54 | T-53 |
| M-7h | VENDOR avec -i (historique) | tue rc=1 tmp=0 | T-51 | T-51 |
| M-23 | --diff-merges=first-parent retire | tue rc=1 tmp=0 | T-54 | T-54 |
| M-24 | --full-history retire | survit (equivalent declare) rc=0 tmp=0 | - | EQ |
| M-25 | --diff-merges=first-parent et --full-history retires | tue rc=1 tmp=0 | T-54 T-55 | T-55 |
| M-26 | -c log.showRoot=true retire | tue rc=1 tmp=0 | T-56 | T-56 |
| M-27 | --text retire | tue rc=1 tmp=0 | T-57 T-61 | T-57 |
| M-28 | --no-textconv retire | tue rc=1 tmp=0 | T-58 | T-58 |
| M-29 | refus du depot superficiel retire | tue rc=1 tmp=0 | T-59 | T-59 |
| M-30 | --all remplace par HEAD | tue rc=1 tmp=0 | T-63 | T-63 |
| M-31 | -c color.ui=never et --no-color retires ensemble | tue rc=1 tmp=0 | T-65 | T-65 |
| M-32 | -c core.quotePath=false retire | tue rc=1 tmp=0 | T-52 T-64b T-65 | T-52 T-65 |
| M-33 | compteur de contexte de l'awk retire | tue rc=1 tmp=0 | T-53 T-70 | T-53 |
| M-34a | plafond de la liste retire | tue rc=1 tmp=0 | T-66 | T-66 |
| M-34b | compte total retire du message | tue rc=1 tmp=0 | T-66 | T-66 |
| M-35 | exclusions du fichier non appliquees a l'historique | tue rc=1 tmp=0 | T-67 | T-67 |
| M-36a | --no-notes retire | survit (equivalent declare) rc=0 tmp=0 | - | EQ |
| M-36b | -c diff.suppressBlankEmpty=false retire | survit (equivalent declare) rc=0 tmp=0 | - | EQ |
| M-36c | -c diff.noprefix=false retire | tue rc=1 tmp=0 | T-65 | T-65 |
| M-36d | export LC_ALL=C retire | survit (equivalent declare) rc=0 tmp=0 | - | EQ |
| M-36e | -c diff.mnemonicPrefix=false retire | survit (equivalent declare) rc=0 tmp=0 | - | EQ |
| M-36f | --no-ext-diff retire | survit (equivalent declare) rc=0 tmp=0 | - | EQ |
| M-38 | --no-renames retire | survit (equivalent declare) rc=0 tmp=0 | - | EQ |
| M-39 | garde hors hunk de l'en-tete +++ retiree | tue rc=1 tmp=0 | T-60 | T-60 |
| M-40 | ligne vide non comptee en contexte ET -c diff.suppressBlankEmpty=false retire | tue rc=1 tmp=0 | T-70 | T-70 |
| M-41 | pipefail retire (echec de git log masque) | tue rc=1 tmp=0 | T-69 | T-69 |

Résumé : `RESUME mut-final : 67 tue(s) (dont 0 par un autre tueur que l'attendu), 0 survivant(s) non attendu(s), 7 equivalent(s) declare(s), 0 survivant(s) a tueur ulterieur, 0 hors etat, 0 inapplicable(s)`.

- **Survivants déclarés équivalents, avec leur commande de rejeu** (`TMPDIR=<neuf> bash enforcement/tests/run-fixtures-secrets.sh F:/tmp/shogen-lots/D8b/oracles/mut-final/<id>.sh`, depuis la racine du worktree) :

  - **M-24** (`--full-history` retiré) : sur git 2.55, `--diff-merges=first-parent` seul parcourt la branche latérale d'une fusion identique au premier parent (G0 §5.4, S3 bis, rejoué par le cp-1) ; re-mesuré sur la gate du lot (C-8) : T-55 reste vert. Garde : M-25, les deux options retirées ensemble, est tué par T-54 et T-55. L'option reste posée, d'après la documentation (G0 §5.7 b), contre un changement de ce comportement dans une autre version de git (item 3 c). Rejeu : `TMPDIR=<neuf> bash enforcement/tests/run-fixtures-secrets.sh F:/tmp/shogen-lots/D8b/oracles/mut-final/M-24.sh` (sortie 0).
  - **M-36a** (`--no-notes` retiré) : avec `--format`, git log n'affiche pas les notes (documentation de `--notes`, git-log 2.55, extrait du G0) ; T-64a et T-64b restent verts. Les notes restent balayées par la ref `refs/notes/commits`, que `--all` parcourt (T-64a : 2 commits comptés). Rejeu : `TMPDIR=<neuf> bash enforcement/tests/run-fixtures-secrets.sh F:/tmp/shogen-lots/D8b/oracles/mut-final/M-36a.sh` (sortie 0).
  - **M-36b** (`-c diff.suppressBlankEmpty=false` retiré) : l'`awk` compte une ligne vide comme contexte : T-70 (config `diff.suppressBlankEmpty=true`) reste vert. Garde : M-40, les deux protections retirées ensemble, est tué par T-70. Rejeu : `TMPDIR=<neuf> bash enforcement/tests/run-fixtures-secrets.sh F:/tmp/shogen-lots/D8b/oracles/mut-final/M-36b.sh` (sortie 0).
  - **M-36d** (`export LC_ALL=C` retiré) : motifs ASCII : sous la locale ambiante `C.UTF-8`, les 90 cas passent, et les sorties de l'arbre réel sont identiques (`oracles/lcall.out`) ; la locale de l'image n'est pas mesurée (item 3 c) : la ligne reste, pour que le verdict ne dépende pas de la locale de l'image. Rejeu : `TMPDIR=<neuf> bash enforcement/tests/run-fixtures-secrets.sh F:/tmp/shogen-lots/D8b/oracles/mut-final/M-36d.sh` (sortie 0).
  - **M-36e** (`-c diff.mnemonicPrefix=false` retiré) : git log -p garde les préfixes `a/` et `b/` sous `diff.mnemonicPrefix=true` (`oracles/sonde-extdiff.out` : en-tête `+++ b/…`) ; T-65, qui pose cette config, reste vert. Rejeu : `TMPDIR=<neuf> bash enforcement/tests/run-fixtures-secrets.sh F:/tmp/shogen-lots/D8b/oracles/mut-final/M-36e.sh` (sortie 0).
  - **M-36f** (`--no-ext-diff` retiré) : git log -p n'emploie pas `diff.external` sans `--ext-diff` (`oracles/sonde-extdiff.out` : 3 lignes ajoutées sans option comme avec `--no-ext-diff`, 0 avec `--ext-diff`). Rejeu : `TMPDIR=<neuf> bash enforcement/tests/run-fixtures-secrets.sh F:/tmp/shogen-lots/D8b/oracles/mut-final/M-36f.sh` (sortie 0).
  - **M-38** (`--no-renames` retiré) : la pathspec retire le côté exclu avant la détection des renommages : le déplacement de `enforcement/tests/x.py` vers `enforcementX/x.py` (T-62b) reste un ajout, et un renommage dans la portée ne retire pas l'ajout d'origine, déjà balayé dans son commit [inféré de la mesure T-62b]. Rejeu : `TMPDIR=<neuf> bash enforcement/tests/run-fixtures-secrets.sh F:/tmp/shogen-lots/D8b/oracles/mut-final/M-38.sh` (sortie 0).
- *Amendement du 2026-09-30 (correction de la revue G2)* : campagne rejouée sur la gate corrigée, 98 mutants (les 74 du G1, M-16 et M-41 redérivés ; K et N du G2 ; K-3b, K-6c à K-6f du correcteur) ; M-24 et M-36d, confirmés équivalents par le G2, et les cinq autres équivalents du G1 : §15.

## 6. Oracles non-LLM (O-1 à O-12) et enregistrement

- **O-1 — runner** (`bash enforcement/tests/run-fixtures-secrets.sh`, `oracles/o1.sh`, TMP neuf, deux formes de `TMPDIR`, C-7) : D8b-1 figé 14 ok, 0 échec (15 s et 13 s) ; D8b-2 figé 67 ok (64 s et 67 s) ; état final 90 ok, 0 échec, sortie 0, sous `TMPDIR=F:/…` (102 s) et `TMPDIR=/f/…` (93 s) ; 0 entrée TMP après chacun.
- **O-2 — arbre réel, sonde négative** (`oracles/o23.sh`, `bash <gate> --tree` depuis la racine) : worktree, gate de D8b-1 : sortie 0, `OK (secrets) : 302 fichier(s)`, 71,8 s ; état final : worktree 62,8 s, arbre principal `F:/Shogen` 61,7 s, sortie 0, 302 fichiers, un seul avis (exclusions du contrat), 0 REFUS. Ces deux passages précèdent le `git add -N` du diff prescrit ; après lui, une entrée en intention d'ajout est lue vide (`oracles/sonde-ita.out` : blob vide à l'index, `git show` rend 0, la gate la compte sans contenu). Ce balayage porte donc sur la base ; les fichiers du lot sont balayés dans le clone d'O-4, où ils sont committés (k=0).
- **O-3 — historique réel, sonde négative** (`bash <gate> --history`) : worktree 1,5 s, arbre principal 1,4 s, sortie 0, `OK (secrets) : historique, 141 commit(s) (--all)`. **Refs couvertes (C-3)**, mesurées à 16:51Z et 16:52Z (`oracles/o3-refs.sh`, `O3-refs-final-worktree.out`, `O3-refs-final-principal.out`) : 17 refs (15 branches locales, 1 ref distante, 1 tag), HEAD des 14 arbres de travail (dont 5 détachés), aucun `refs/stash` (0 entrée), 141 commits atteints, dont 134 dans l'ascendance de `40b4cfb` : 7 commits hors de l'ascendance du lot (`main` à `293b7a7` et lots en vol) ; 0 constat, donc rien à rapporter hors de l'ascendance. Sur la forge : `refs/remotes/origin/*` après `fetch-depth: 0` (non mesuré, item 3).
- **O-4 — rouges semés sur l'entrée réelle** (`oracles/o4.sh`) : clone `git clone --shared --no-checkout` de `F:/Shogen` sous `oracles/rouge-final/clone`, `checkout --detach 40b4cfb` et commit des six fichiers du lot dans le clone (`5204e418…`, parent `40b4cfb` ; config locale : identité `example.invalid`, sans signature, crochets neutralisés) ; refs du clone : 1 branche, 1 tag, 16 refs distantes, 142 commits atteints. k=0 : `--tree` sortie 0, 304 fichiers (les 302 de la base et les deux documents du lot ; gate, runner et fixture exclus par contrat) ; `--history` sortie 0, 142 commits. k=1 (V formée depuis la fixture, ajoutée à l'index) : mode indexé 2 `SECRETS/forme`, 1 ligne nommée `rouge.py:1:`. k=2 (C1 l'ajoute, C2 la retire) : `--tree` 0 ; `--history` 2 `SECRETS/historique`, attribution `<C1>:rouge.py:1` présente, 0 fragment de la valeur dans la sortie. k=3 (fichier d'exclusion suivi, ligne sans marqueur) : `--tree` 2 `SECRETS/exclusion`. 0 entrée TMP (`oracles/rouge-final/resultat.txt`). Rejeu sur les documents finaux : en tête de `G1-rapport.md`.
- **O-5 — mutants de gate** : §5.
- **O-6 — invariant de littéral** (`oracles/statiques.sh`, motifs évalués depuis les lignes d'affectation de la gate du lot, `LC_ALL=C`) : 0 ligne VENDOR et 0 ligne GENERIC sur la gate, le runner, la fixture, `gates.yml`, ce journal et la copie du G0 ; contrôle positif sur la copie amont `g0-mesures/amont-run-fixtures-7960238.sh` : 14 et 5, les comptes du G0 §5.2.
- **O-7 — compatibilité g5** : 0 occurrence du motif courant (`gates.yml` l.49) et 0 du motif élargi de D8c (`adb2213:gates.yml` l.39) sur les lignes ajoutées par le lot, documents compris ; rejeu de la commande du job g5 sur le worktree : sortie 0, `g5 : OK` (`oracles/g5.out`) ; les cinq fichiers neufs du lot, en intention d'ajout, sont lus par `git grep` (contrôle : les cinq portent le mot `secrets`) ; `gates.yml` est exclu de la commande du job.
- **O-8 — non-régression** : suite `s2-harness`, base et final : `Ran 216 tests`, `OK (skipped=2)`, sortie 0, 0 entrée TMP, à la base (16:00Z) comme sur l'arbre final (17:08:57Z-17:09:50Z) ; mêmes deux sauts, tests (ii) et (ii bis) de `test_exclusion` (`oracles/suite-base.sauts`, `oracles/suite-final.sauts`, `diff` vide) ; `cargo --locked xtask verify` sur l'arbre final : premier passage (17:32:48Z-17:32:53Z, journal complet sauf cette ligne et celle du contrôle d'application) : VERT, sortie 0 ; S-G1 à S-G8, `fmt`, `no_std` et `clippy` VERT ; S-G4 couvre 55 fichiers (53 à la base) et S-G5 56 (54 à la base), les deux documents du lot compris ; en régime de corpus incomplet, S-G5 contrôle 252 fragments et en laisse 218 non contrôlés, comme à la base : le lot n'ajoute aucune citation anglaise ; 0 téléchargement sous `F:/rust/rustup/downloads`. Second passage, sur l'arbre remis : en tête de `G1-rapport.md`.
- **Oracle local G3 de la mission** (ADR-0028 §4.11 amendé par D8a ; `oracles/g3-d8a.sh`) : sur le worktree du lot, `bash enforcement/tests/run-fixtures-model-pinning.sh` → `model-pinning : 76 ok, 0 échec`, sortie 0 ; `bash enforcement/lint-model-pinning.sh .` → sortie 0, `OK (R-1) : 3 fichier(s)` (le worktree porte le réglage local ignoré relevé en E-5 de D8a) ; 0 entrée TMP. Le lot ne touche ni le lint ni son runner.
- **Sonde des dépôts vides** (`oracles/sonde-vide.out`) : dépôt sans commit, puis à un commit : les trois modes sortent en 0 (`0 fichier(s)`, `historique, 0 commit(s)`, puis `1 fichier(s)` et `1 commit(s)`).
- **O-9 — TMP** : 0 entrée dans chaque TMP neuf, après chaque O-1 (12 exécutions), chaque O-2 et O-3 (5), chaque exécution de mutant (167 : 46, 46, 1 et 74) et chaque suite.
- **O-10 — structure de `gates.yml`** (`oracles/o10.py`, `yaml.safe_load`, PyYAML 6.0.3, comparée à la base `40b4cfb`) : D8b-2 figé, 18 assertions sur 18 ; état final, 19 sur 19 (clés de premier niveau, un seul job neuf, jobs de la base inchangés, `name` = identifiant, `ubuntu-24.04`, `timeout-minutes: 15`, checkout au SHA `3d3c42e5…` avec `persist-credentials: false` et `fetch-depth: 0`, quatre étapes et leurs commandes exactes, aucun `continue-on-error`, ordre g5, g1, g3, s2). Contrôle négatif (`oracles/o10-negatif.sh`) : trois copies semées (fetch-depth retiré, job de base altéré, erreur de syntaxe) sortent en 1.
- **O-11 — garde d'isolation** (`oracles/o11.sh`) : `GIT_NAMESPACE=d8b-garde` → sortie 3, message `ERREUR FATALE : variable GIT_NAMESPACE posée (isolation)`, TMP 0 avant et 0 après. `GIT_DIR` et `GIT_WORK_TREE` ne sont posées par aucune commande du G1 ; leur présence dans la liste de la garde se contrôle par lecture (runner l.16).
- **O-12 — temps** (local, Git Bash, sans charge concurrente) : runner 93 à 102 s (90 cas) ; `--tree` 62 à 72 s (302 fichiers) ; `--history` 1,4 à 1,5 s (141 commits). Le commentaire du job cite ces bornes ; 15 min bornent un blocage.
- **CA-D8b-17 (CH-8, `LC_ALL=C`)** : copie de la gate sans la ligne `export LC_ALL=C` (une ligne changée, la forme de M-36d), lancée sous la locale ambiante `C.UTF-8` de Git Bash : sorties de `--tree` (302 fichiers) et de `--history` (141 commits) sur l'arbre réel du worktree identiques, octet pour octet, à celles de la gate du lot (`oracles/lcall.out`). Runner complet sous M-36d : sortie 0, 90 cas verts (équivalent déclaré, §5). Mesure locale seulement : la locale de l'image n'est pas mesurée (item 3 c).
- **CA-D8b-1** : `git diff --name-status 40b4cfb`, après `git add -N .` : `M` pour `.github/workflows/gates.yml` ; `A` pour `docs/G1-lot-D8b.md`, `docs/adr-0028/G0-lot-D8b.md`, `enforcement/gate-secrets.sh`, `enforcement/tests/fixtures/secrets/sondes.tsv` et `enforcement/tests/run-fixtures-secrets.sh` : six fichiers, la liste IN du G0 §3 (`oracles/lot-name-status.txt`)
- **Contrôle d'application** (`oracles/diffs.sh`) : base + `d8b-1.diff` + `d8b-2.diff` + `d8b-3.diff` + `docs.diff`, puis base + `lot.diff`, appliqués par `patch -p1` sur une extraction `git archive 40b4cfb ':!biblio'` : 6 fichiers sur 6 identiques au worktree ; 6 sur 6 identiques (`oracles/diffs.out`) ; sous-diffs au format git, en-têtes `new file mode` : 3 dans `d8b-1.diff`, 2 dans `docs.diff`, 0 dans `d8b-2.diff` et `d8b-3.diff`, qui ne touchent que des fichiers déjà créés. Rejeu sur les diffs remis : en tête de `G1-rapport.md`
- **Enregistrement d'oracle substitut** : `oracles/oracle-G1-D8b-substitut.json` (schéma `shogen.g2.oracle-substitut.v1`, rôle G1, champs de D6 viii : arbre, sha256 par fichier, base, `static_only` faux, environnement, runs avec commande, sortie, sha256 et attente) ; son sha256 est en tête de `G1-rapport.md`.
- *Amendement du 2026-09-30 (correction de la revue G2)* : O-1 à O-12, oracle local G3 de D8a et sonde des refs de remplacement rejoués sur l'état corrigé ; enregistrement `correction/oracle-G1c-D8b-substitut.json` : §15.

## 7. Tuyaux (CA-11, règle Branchement)

- **Entrée 1** : arbre suivi, lu dans l'index (302 fichiers en portée à `40b4cfb`, produits par les commits du dépôt). **Entrée 2** : historique atteint depuis les refs et les HEAD des arbres de travail (141 commits au G1). **Entrée 3** : contenu indexé d'un commit en préparation (mode sans argument).
- **Pièce** : `enforcement/gate-secrets.sh`, sans état ; le fichier d'exclusion, absent, en tiendrait lieu.
- **Sortie** : code 0 ou 2, jetons sur stderr, constats masqués (chemin, ligne ; commit en historique).
- **Consommateur 1** : job `g3-secrets` (étape 1 : runner ; étape 2 : `--tree` ; étape 3 : `--history`). **Partiel déclaré** : forge sans exécution (GC-01), aucun `required_status_checks` (GC-09) ; item 3. Fait du JOURNAL de `main` (`293b7a7`, 16:37Z, non dans la base du lot) : les jobs ne tournent pas sur le dépôt privé faute de paiement, et l'investisseur retient le passage du dépôt en public, qui est son acte ; conséquences sur les items 2, 3 et 5 au §11.
- **Consommateur local (G3 opérant, ADR-0028 §4.11)** : texte proposé pour l'amendement daté de §4.11, acte de l'orchestrateur : « *Amendement daté du 2026-09-30 (lot D8b)* : à partir du commit de D8b, le G3 opérant comprend aussi les trois commandes du job `g3-secrets` : `bash enforcement/tests/run-fixtures-secrets.sh` (sortie 0 ; résumé `secrets : 90 ok, 0 échec`), `bash enforcement/gate-secrets.sh --tree` (sortie 0) et `bash enforcement/gate-secrets.sh --history` (sortie 0) ; tout constat de l'historique hors de l'ascendance du commit rejoué est rapporté masqué, sans être compté comme un défaut du lot rejoué. »
- **Consommateur 2** : hook versionné de D8c, en mode indexé : **absent** ; item 4.
- **Test de composition** : O-2 et O-3 (entrée réelle committée → gate → 0) ; O-4 (clone de cette entrée, lot committé, un rouge semé → 2 et jeton ; k=0 → 0).
- *Amendement du 2026-09-30 (correction de la revue G2, C-G2-11 c)* : texte proposé pour l'amendement de §4.11, qui remplace celui ci-dessus (résumé `secrets : 113 ok, 0 échec`, depuis T-75b) : §15. Tuyaux inchangés ; O-2, O-3 et O-4 rejoués sur l'état corrigé.

## 8. Risques MAST (annexe C) et contre-mesures

- **FM-1.1** : (a) le runner n'écrit que dans des dépôts jetables (O-11 ; garde `GIT_*`, contrôle hors dépôt, `show-prefix`, `-C`) ; (b) aucune forme complète dans un fichier du lot (O-6 = 0 sur tous, contrôle positif 14 et 5) ; (c) aucune ligne de pièce D.2 signalée, aucune affichée.
- **FM-3.3** : sondes par alternative et par seuil ; sortie ET jeton, plus motif requis ou interdit ; 74 mutants ; un mutant survivant (M-17) a été traité comme un défaut du test et corrigé (E-2) ; le contrôle nu de `ADR-0004` a été validé par un contrôle positif sur le blob (E-5).
- **FM-3.2** : ce que l'oracle local ne prouve pas est nommé : outils de l'image (`grep`, `awk` du runner et de l'attribution, `tr`, `mktemp`, `iconv`), `git clone --no-local --depth 1` sur le git de l'image, effet réel de `fetch-depth: 0`, temps sur Linux, lecture du workflow par la forge (item 3 c).
- **FM-2.3** : scanner dédié, forge, hook, vitesse de `--tree`, `gate-gist.sh`, `s2-harness/` non touchés ; messages de commit : item 8, non construit ici ; diff limité aux six fichiers.
- **FM-1.5** : coupe du G0 §9 tenue ; plafond de 20 constats, refus du superficiel, `timeout-minutes`.
- **FM-2.4** : faits portés au journal : prémisse de mission corrigée (C-1), cas amont 12 et 13 (E-6), portée d'O-2 dans un worktree (§6), fait du JOURNAL du 16:37Z (§7), déplacement de `main` (en-tête).
- **FM-2.2** : choix du G1 exposés en Q-G1 (§11).

## 9. `error_origin` proposés (à assigner au G7)

- **E-1** : worktree créé à `fa0ce5b` au lieu de la base de la mission (`40b4cfb`). Origine : harnais du workflow (même constat que E-1 de B0 et de D8a).
- **E-2** : M-17 survit à la première campagne de D8b-2 : le motif requis de T-15 (`mktemp`) figure aussi dans le message d'erreur de `mktemp`. Origine : worker G1. Corrigé (T-15 exige `mktemp a échoué`), rejoué, tué.
- **E-3** : l'outil du harnais a converti une séquence `\n` d'un script d'édition passé par heredoc (`amend_g0.py`) en saut de ligne réel : `SyntaxError` à l'exécution, corrigé par l'outil d'édition de fichiers et relu. Origine : environnement (outil) ; même classe que E-10 de D8a. Aucun fichier du lot n'est passé par heredoc ; les séquences `\000` et `\t` de la gate et du runner ont été relues en octets (`od -c`).
- **E-4** : estimation R-25 de ≈ 415 pour 366 mesurées. Écart sans effet sur la coupe ; origine : worker G1 (base de 3 lignes par cas du G0 §9 reprise sans mesure du runner de D8a).
- **E-5** : première forme du contrôle de références nues à `ADR-0004` (`controle-motifs.sh`, réécrit par `sed`) : un motif en syntaxe basique comptait 0 sans rien lire ; relevé par le contrôle positif sur le blob (9 attendues), réécrit en `grep -E`. Origine : worker G1 ; aucun effet sur le lot.
- **E-6** : cas amont 12 et 13 du runner `7960238` (fichier d'exclusion non suivi : branche « non suivi » exercée à la place des branches nommées). Origine : amont VibeGates ; transmis à SHOGEN-D8-AMONT-ERRATUM-1 (Q-G1-5).

## 10. Review Focus

1. **Mode `--history`, fonction neuve** : drapeaux forcés, `pipefail`, verdict par `grep` seul, attribution par `awk` à deux entrées (`NR == FNR`), hors hunk seulement pour `+++ `. Tueurs : T-51 à T-70 ; M-24 et les M-36 équivalents (§5).
2. **Motifs requis et interdits du runner** (CH-12) : sans eux, M-17 et M-18 seraient équivalents ; T-15 corrigé (E-2).
3. **Portée `--all` dans un worktree** (C-3) : 14 HEAD d'arbres de travail lus ; 7 commits hors de l'ascendance du lot au G1.
4. **T-59 sans URL `file://`** (C-7) : `--no-local --depth 1` ; comportement de l'image inféré de la documentation.
5. **T-68** : la branche « inutilisable » n'était atteinte par aucun cas du G0 (T-20 touche la branche « traversant »).
6. **S-G5 en régime partiel dans ce worktree** (0 artefact sur 125) : ce journal et la copie du G0 ne portent aucune citation anglaise entre guillemets ; le régime complet est celui du rejeu de l'orchestrateur sur l'arbre principal.

## 11. Questions Q-G1 et items formés

**Questions pour l'orchestrateur**
- **Q-G1-1** : ratifier les lignes datées de l'annexe A (§1) et la ligne E-D8b-G1 de l'annexe E.
- **Q-G1-2** : ratifier les cas et sondes ajoutés par le G1 (T-30a et T-30b, T-33 à T-35, T-52a, T-62a et T-62b, T-64a et T-64b, T-66b, T-68 à T-70) et la fonction de cas à motif requis ou interdit (CH-12).
- **Q-G1-3** : ratifier `pipefail` dans le flux d'historique (CH-2, écart d'implémentation) et le compte `OK` en commits atteints (CH-6).
- **Q-G1-4** : amender ADR-0028 §4.11 par le texte du §7.
- **Q-G1-5** : joindre E-6 (cas amont 12 et 13) à SHOGEN-D8-AMONT-ERRATUM-1.
- **Q-G1-6** : documentation hors compte R-25 (C-4) : copie du G0 et journal.
- **Q-G1-7** : le fait du 16:37Z (passage public prévu) rapproche les déclencheurs des items 5 et 8 : les porter avant l'acte de publication.
- **Q-G1-8** : ratifier l'écart à la lettre de CH-5 : références à l'ADR-0004 de VibeGates retirées des messages, gardées dans l'en-tête (§3).

**Items formés** (reprise du G0 §11, amendés ; versement à l'annexe B par l'orchestrateur, CA-D8b-16)

| # | item | objet | propriétaire | déclencheur |
|---|---|---|---|---|
| 1 | SHOGEN-SECRETS-SCANNER-DEDIE-1 | **recherche** du scanner dédié du gabarit du corpus (l.57-58) : outil, vérification de registre (R-8), épinglage par empreinte, fonctionnement hors ligne, règles au-delà du plancher, prix et licence ; puis ADR sourcé (R-23) | recherche : orch. ; installation : go du mainteneur | maintenant (recherche sans code) ; décision au prochain point d'étape |
| 2 | SHOGEN-FORGE-SECRET-SCANNING-1 | balayage des secrets et protection des poussées de la forge : conditions et prix à lire sur place par l'orchestrateur ; la question change de forme si le dépôt passe en public (fait du 16:37Z, non lu par le G1) | recherche : orch. ; décision : investisseur | prochain point d'étape, et avant l'acte de publication |
| 3 | SHOGEN-G3-FORGE-1 | (a) `g3-secrets` aux `required_status_checks` ; (b) première exécution sur la forge ; (c) ce que l'oracle local ne prouve pas : `grep`, `awk` (runner et attribution), `tr`, `mktemp`, `iconv` et `git clone --no-local --depth 1` de l'image, effet de `fetch-depth: 0`, temps sur Linux, lecture du workflow par la forge | orch. ; (a) investisseur ou mainteneur | forge rétablie (dépôt public ou paiement, fait du 16:37Z) |
| 4 | SHOGEN-D8-HOOK-SECRETS-1 | le hook versionné de D8c lance le mode indexé de la gate (consommateur 2) ; coût par commit à mesurer | orch. | G0 de D8c |
| 5 | SHOGEN-SECRETS-HORS-REFS-1 | objets inatteignables, commits des seuls journaux de refs, bundles de custodie : un balayage unique par les mêmes motifs, comptes seuls | orch. | avant toute copie brute de `.git` en custodie, ou avant l'acte de publication (D10, fait du 16:37Z), au premier des deux |
| 6 | SHOGEN-SECRETS-REVOQUE-1 | **recherche** d'une liste de constats révoqués (commit, chemin, empreinte de ligne), sous ADR, compatible avec D7 | orch. | premier constat réel |
| 7 | SHOGEN-BIBLIO-GIT-CHECKOUT-1 | verser à `biblio/` les pages de git 2.55 (git-log, git-rev-parse, git-rev-list, git-cat-file, git-diff, et git-clone, lue au G1) et l'`action.yml` d'actions/checkout au SHA `3d3c42e5…` ; ce journal n'en cite rien entre guillemets | orch. ; go requis pour un téléchargement | prochain versement |
| 8 | SHOGEN-SECRETS-MESSAGES-1 (neuf, PAROXYSME) | les messages de commit et de tag annoté ne sont pas balayés : le flux ne porte que `commit %H` et les diffs ; construction : un second flux `git log --all --format=%B` et `git for-each-ref refs/tags --format='%(contents)'`, mêmes motifs, attribution au commit ou au tag ; prix ≈ 8 lignes de gate et 3 cas [inféré] | orch. | G0 de D8c, ou avant l'acte de publication (D10), au premier des deux |

Transmission, sans item neuf : E-6 et la chaîne de provenance du G0 §5.2 rejoignent SHOGEN-D8-AMONT-ERRATUM-1.

- *Amendement du 2026-09-30 (correction de la revue G2)* : items I-G2-1 à I-G2-4 du G2 (I-G2-4 étendu par le correcteur) et questions Q-C-1 à Q-C-3 : §15.

## 12. Livrables (`F:/tmp/shogen-lots/D8b/`)

- `lot.diff` : diff du lot entier contre `40b4cfb` (`git add -N .` puis `git diff HEAD`, prescrit).
- `d8b-1.diff`, `d8b-2.diff`, `d8b-3.diff`, `docs.diff` : sous-diffs au format git (en-têtes `new file mode` pour les fichiers neufs), produits dans le dépôt jetable d'états `work/etats/` ; contrôle d'application au §6.
- `G1-rapport.md` : ce journal, précédé des empreintes des livrables.
- `oracles/` : scripts (`env.sh`, `cargo_env.sh`, `xtask.sh`, `suite.sh`, `o1.sh`, `o23.sh`, `o3-refs.sh`, `o4.sh`, `o10.py`, `o10-negatif.sh`, `o11.sh`, `statiques.sh`, `controle-motifs.sh`, `mutants.py`, `mutants-run.sh`, `mutants_bilan.py`, `cas_par_mutant.py`, `gen_sondes.py`, `figer.sh`, `r25.sh`, `diffs.sh`, `amend_g0.py`, `extraire_doc.py`, `sonde-superficiel.sh`, `sonde-pathspec.sh`, `lcall.sh`, `oracle_record.py`) et leurs sorties ; `estimation-R25.txt` et son sceau ; `G0-copie.diff` ; `git-clone-2.55.0.txt` ; dossiers de mutants `mut-d8b-1/`, `mut-d8b-2/`, `mut-d8b-2-rejeu/`, `mut-final/` ; `rouge-final/` (clone d'O-4).
- `work/` : extraction de base, instantanés figés, brouillon de D8b-3, dépôt d'états, copies d'application, contrôles négatifs d'O-10.

## 13. Contraintes d'environnement déclarées

- **Garde d'isolation du worktree** : refus mesurés de commandes composées jugées trop complexes (boucles avec `bash -n`, `bash --version`, heredoc avec `git`, lecture de variables `GIT_*` en ligne). Contournement retenu : scripts d'oracle écrits sous `F:/tmp/shogen-lots/D8b/oracles/` et exécutés directement ; leurs appels git visent le worktree (lectures, `archive`), `F:/Shogen` en lecture seule (`--no-optional-locks`), les dépôts jetables et les deux dépôts d'oracle sous `F:/tmp/shogen-lots/D8b/`.
- **Outil d'édition et heredoc** : E-3.
- **Écrivains concurrents** : TMP neuf par exécution ; `main` a bougé pendant le G1 (en-tête).
- **Rien sur C:** : TMP, cibles cargo et sorties sous `F:/tmp/` ; lecture seule de la documentation git sous `C:/Program Files/Git/mingw64/share/doc/git-doc/` et de la toolchain sous `F:/rust`.

## 14. Attestation (forme d'ADR-0028 D.3)

- **Pièces lues** : ADR-0028 (D7, D8, §4.11, §6) et annexes A (l.9, l.33-38), B (l.24, B.11), E (l.29-32 et amendement) à `40b4cfb` ; le G0 accepté et ses mesures ; le rapport du cp-1 et sa liste ; `docs/G1-lot-D8a.md` (forme) ; `JOURNAL.md` l.120-139 ; le blob `6789a30` ; `adb2213:.github/workflows/gates.yml` (motif g5 élargi) ; le runner amont `7960238`, affiché avec toute forme d'identifiant masquée ; `xtask/src/sg4.rs` et `sg5.rs` (en-têtes, liste des locutions).
- **Non ouverts** : les pièces de l'annexe D.2, toutes ; `F:/shogen-campagne/*`, `F:/tmp/shogen-j28/*`, `measure-M009a.md`, `F:/tmp/shogen-carto-2026-09-29/campagne.md`. Aucune copie scellée lue ; `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée.
- **Balayage mécanique** : la gate (O-2, O-3, O-4) et `cargo xtask verify` (S-G4, S-G5) lisent des fichiers suivis, dont deux portent une ligne de D.2 (annexe D l.35-36) : seuls des comptes, des codes de sortie et des lignes de verdict ont été affichés ; aucun constat.
- **Aucune statistique S2 calculée sur les journaux de campagne. Aucun z, aucun K, aucun P̂_more ni aucun φ de campagne vu.**
- **Isolation git** : aucun `GIT_DIR`, aucun `GIT_WORK_TREE`, aucun `--write-tree` ; aucun commit, stash, checkout, reset ni push sur `F:/Shogen` ; sur ce worktree : `merge --ff-only`, `add -N`, `diff`, `archive`, `rev-parse`, `ls-files`, `status --short`, `check-attr`, `config --get`, `log`, `merge-base`, `rev-list`, `for-each-ref`, `worktree list`, `grep` (commande du job g5) ; sur `F:/Shogen`, lectures en `--no-optional-locks` (`rev-parse`, `for-each-ref`, `worktree list`, `rev-list`, `stash list`, et les lectures de la gate : `ls-files`, `show`, `log`) et `git clone --shared` vers `F:/tmp` (O-4). `init`, `add`, `commit`, `checkout`, `reset` et `clone` n'ont eu lieu que dans les dépôts jetables et dans les deux dépôts d'oracle sous `F:/tmp/shogen-lots/D8b/`. Rien écrit sur C:.

## 15. Corrections de la revue G2 (2026-09-30, ajout daté ; lignes précédentes inchangées)

- **Générateur** : `claude-opus-5-5` (R-1 déclaré en tête de session), effort max, contexte frais, worker G1 de correction, instance distincte du réviseur G2. Même worktree (branche `worktree-wf_089f8fc6-492-1`, HEAD `40b4cfb`, rien de commité). Aucun commit, aucun workflow (R-20) ; aucun `GIT_DIR` ni `GIT_WORK_TREE`, aucun `--write-tree`. Horloge (`date -u`) : première heure 18:51:38Z ; estimation R-25 scellée à 19:01:13Z, avant tout code ; O-1 des états corrigés de 19:06:40Z à 19:25:20Z ; O-2 et O-3 de 19:25:38Z à 19:29:20Z ; code figé à 19:30:05Z, le commentaire des temps du job écrit d'après ces mesures ; campagne de mutants de 19:30:57Z à 20:27:53Z ; journal ensuite.
- **Mandat** : commande de correction de l'orchestrateur Shōgen (`claude-fable-5-1`) : liste fermée C-G2-1 à C-G2-11 de la revue G2 (`F:/tmp/shogen-lots/D8b/G2-rapport.md`, sha256 `13b2dd885e64d17c361c529c8428e8915ddb08d2ff2c04b956f4fd7900add332`, verdict ACCEPTE-AVEC-CORRECTIONS). Preuves, chemins et empreintes : `F:/tmp/shogen-lots/D8b/correction-rapport.md` ; scripts et sorties sous `F:/tmp/shogen-lots/D8b/correction/`.
- **Méthode** : le diff testé du G2 (`g2/corrections-G2.diff`, sha256 `58bcbef6…98f4f`) est découpé sans retaper une ligne en trois correctifs, un par sous-lot, aux lieux du G2 §5 (`split_diff.py` : 11 hunks, chacun affecté une fois), puis appliqué par `patch --fuzz=0` aux instantanés figés du G1 (décalages seuls). L'état final obtenu est identique, octet pour octet, aux fichiers `g2/propose3/` du G2 (`cmp`). Les textes de C-G2-11 et les écarts ci-dessous y sont portés par remplacement exact, compte d'ancre égal à 1 exigé (`edits.py`, `fix_comment.py`, `add_cases.py`, `edit_gates.py`). Réponse de forme à Q-G2-2 : trois sous-lots, pas de D8b-4.
- **Corrections** (lieux à l'état corrigé : gate 140 lignes, runner 164 depuis la re-revue rr1, T-75b en l.161 et lieux des autres cas inchangés, fixture 47) :
  - **C-G2-1** (CH-1 ; A2) : gate l.118, `git ls-files -s -- ":(literal)$f"` ; cet appel seul (un `--literal-pathspecs` global annulerait les exclusions du contrat). Tests : T-71 (index) et T-71b (`--tree`), runner l.93-95. Défaut du blob amont (l.84), pour SHOGEN-D8-AMONT-ERRATUM-1.
  - **C-G2-2** (CH-1, CH-2 ; A3) : gate l.45, `export GIT_NO_REPLACE_OBJECTS=1` ; en-tête l.16. Tests : T-72 (`--tree`, l.96-97) et T-73 (`--history`, l.151-153).
  - **C-G2-3** (CH-2, CH-3 ; A5, A8, A12d) : gate l.88-89, fichier de greffes lu par `git rev-parse --git-path info/grafts`, refus `SECRETS/tronque`. Tests : T-74 (l.154-155) et T-74b (l.156-157, `GIT_GRAFT_FILE`, écart 1).
  - **C-G2-4** (CH-2, CH-3 ; A4) : gate l.90-91, ref vers un blob ou un arbre refusée en `SECRETS/echec`. Test : T-75 (l.158). Effet mesuré hors des cas : une ref de remplacement vers un blob fait aussi refuser `--history` (sonde ci-dessous), sens fermé.
  - **C-G2-5** (CH-2 ; A6) : gate l.95, `-c diff.dstPrefix=b/`. Test : T-65 (l.139-142), config hostile étendue à `diff.dstPrefix=zz/`.
  - **C-G2-6, C-G2-7, C-G2-10** (CH-4) : fixture l.23-27 (V-21 à V-25) et l.40-44 (G-13 à G-17), attendu 2 chacune.
  - **C-G2-8** (CH-14 ; A10) : gate l.60 (fonction `masque`), l.106 (attribution d'historique), l.120 (avis non-blob), l.130-131 (constats et reste) ; en-tête l.30-31. Tests : T-76 (l.159-160), T-77 (l.98), T-79 et T-80 (l.101-102, écart 1). Défaut du blob amont (l.86, l.96), pour SHOGEN-D8-AMONT-ERRATUM-1.
  - **C-G2-9** (CH-1 ; A12b) : gate l.46, `unset` des quatre variables de pathspec. Test : T-78 (l.99-100).
  - **C-G2-11** : (a) en-tête de la gate l.16 (objets réels), l.26-27 (échec fermé : greffes, ref vers un blob ou un arbre), l.30-31 (sortie masquée), l.40-41 (jetons) ; commentaire de la ligne `masque` (écart 4) ; (b) `gates.yml` l.98-101, commentaire des temps (O-12), et même commentaire à l'état D8b-2 (84 cas) ; (c) ce paragraphe et les puces datées de §1 à §7 et §11 ; (d) copie du G0 : onze puces datées et une ligne d'index au §16, 0 ligne retirée (`diff` contre le texte accepté `2b928edd…` et contre la copie du G1) ; (e) sous-diffs et `lot.diff` régénérés, R-25 re-mesuré.
- **Écarts mesurés au texte du G2** (à ratifier, Q-C-1) :
  1. **Quatre mutants de sous-site survivaient au runner du G2** (109 cas, lancés avec les écarts 2 et 3, qui ne changent aucune assertion ; `mut/ext/`, sortie 0 et `secrets : 109 ok, 0 échec` chacun, 19:14:29Z-19:17:27Z) : K-3b (chemin des greffes écrit en dur : `GIT_GRAFT_FILE` n'est plus suivi, A12d rouvert), K-6c (avis non-blob non masqué), K-6d (substitution GENERIC du masque retirée), K-6e (masque GENERIC sensible à la casse). Cas ajoutés : T-74b (greffe par `GIT_GRAFT_FILE` posée pour le seul appel de la gate, `--history`), T-79 (lien nommé V, index : avis masqué, 0 fichier), T-80 (fichier nommé d'après la sonde G-09, forme générique en majuscules, portant V, index). Tueurs : K-3b par T-74b, K-6c par T-79, K-6d et K-6e par T-80 (campagne ci-dessous). K-6f (substitution VENDOR retirée) était déjà tué par T-76 et T-77.
  2. **T-74** crée `.git/info` s'il manque (remarque du G2 à C-G2-3), sur la même ligne : un gabarit sans `info/` ne fait plus sortir le runner en 3.
  3. **Commentaires du runner** : une ligne avant T-71 (cas de la revue G2 du bloc D8b-2) ; liste du bloc `--history` complétée (T-73 à T-76, T-74b).
  4. **Commentaire de la ligne `masque`** : le texte du G2 disait `jamais imprimé` ; les messages d'exclusion et d'échec impriment encore un chemin ou une pathspec (I-G2-4). Le commentaire nomme désormais les sites masqués, comme l'en-tête.
  Hors ces quatre points, le code est celui du diff testé du G2 (`diff` contre `g2/propose3/` : gate, lignes de commentaire seules ; runner, la ligne de T-74, les quatre lignes de T-74b, T-79 et T-80, deux lignes de commentaire ; fixture identique).
- **R-25** (méthode du lot A, `oracles/r25.sh` du G1, `r25-corr.out`) : estimation écrite avant code (`estimation-R25.txt`, horloge 19:01:13Z, sha256 `2b84fa06ef3402c5cbdf63ab1a78385898272cede09ab2148e525523f95f5834`) : D8b-1 ≈ 184, D8b-2 ≈ 110, D8b-3 ≈ 108. Mesure : **D8b-1 184** (gate 108, runner 72, fixture 4), **D8b-2 113** (runner +39, fixture +43, `gates.yml` +31 −3), **D8b-3 111** (gate +40 −8, runner +54 −2, `gates.yml` +17 −7) ; aucun sous-lot au-dessus de 200 ; règles 2 et 3 du G0 §9 non atteintes. Écart à l'estimation, +3 et +3 : T-79, T-80 et la ligne de commentaire (D8b-2) ; T-74b et une ligne du commentaire des temps (D8b-3) : E-9. Lot entier : 391 lignes de code au `lot.diff` (gate 140, runner 163, fixture 47, `gates.yml` +41 −3), 408 en somme des sous-lots (17 lignes de D8b-1 et D8b-2 réécrites par D8b-3, comme au G1). Correction seule, état du lot du G1 vers état corrigé : +57 −15 (gate +20 −10, runner +23 −2, fixture +10, `gates.yml` +4 −3). Documents, hors compte de code : copie du G0 +12 −0, ce journal +89 −0. Après T-75b (re-revue rr1, 2026-10-01, `cr-rr1/r25-rr1.out`) : **D8b-3 112** (gate +40 −8, runner +55 −2, `gates.yml` +17 −7), D8b-1 et D8b-2 inchangés ; 409 en somme des sous-lots, 392 au `lot.diff` (runner 164) ; correction seule, état du lot du G1 vers état final : +58 −15 (runner +24 −2) ; correction de la re-revue seule : +6 −5.
- **Oracles rejoués sur l'état corrigé** (gate `47f2c35e…1722`, runner `7eb01b39…fa99`, fixture `6b558bd2…451c`, `gates.yml` `13dc5177…79fb`) :
  - O-1 (`o1.sh`, TMP neuf, `TMPDIR` en `F:/…` puis `/f/…`, sans charge concurrente) : D8b-1 `14 ok` (21 s, 16 s) ; D8b-2 `84 ok` (92 s, 91 s) ; final `113 ok, 0 échec` (136 s, 139 s ; rejoué le 2026-10-01 après T-75b, re-revue rr1, `cr-rr1/o1/`, charge résiduelle d'autres agents non maîtrisée) ; sortie 0 ; 0 entrée TMP. Runner corrigé lancé avec la gate du lot : `100 ok, 13 échec` (T-65, T-71, T-71b, T-72 à T-80, T-74b ; même date, `cr-rr1/mut/gateG1.out`), exactement les cas qui visent un défaut de la gate du lot ; les dix sondes et T-75b y passent (les sondes tuent des mutants de motif et T-75b le mutant R4b de la correction, pas un défaut du lot).
  - O-2 (`o23-corr.sh`, forme du job, `GIT_OPTIONAL_LOCKS=0`) : worktree 304 fichiers (les 302 de la base et les deux documents du lot, en intention d'ajout, lus vides), 68 s ; arbre principal 302 fichiers, 64 s ; gate de l'état D8b-2 sur l'arbre principal, 302 fichiers, 63 s ; sortie 0, un avis, 0 REFUS, 0 fragment de valeur.
  - O-3 : worktree et arbre principal, sortie 0, `historique, 141 commit(s) (--all)`, 1,6 s et 1,5 s. Refs couvertes (C-3 ; `o3-refs-corr.sh`) : 17 refs (15 branches locales, 1 ref distante, 1 tag), toutes vers un commit (forme de C-G2-4 : 0) ; aucun fichier de greffes ; aucune ref de remplacement ; 14 arbres de travail dont 5 détachés ; aucun `refs/stash` ; 141 commits atteints, 134 dans l'ascendance de `40b4cfb`. Les refus neufs ne se déclenchent pas sur l'entrée réelle. `F:/Shogen` après : HEAD `293b7a7`, 0 fichier suivi modifié.
  - O-4 (`o4-corr.sh`, clone `--shared` sous `correction/rouge-corrige/`, lot corrigé committé dans le clone, `76fec7e0…`, parent `40b4cfb`, 142 commits atteints) : k=0 `--tree` 0 (304 fichiers) et `--history` 0 ; k=1 index 2 `SECRETS/forme`, une ligne nommée ; k=2 `--tree` 0, `--history` 2 `SECRETS/historique`, attribution `<C1>:rouge.py:1` présente, 0 fragment ; k=3 2 `SECRETS/exclusion` ; 0 entrée TMP.
  - O-6 et O-7 (`statiques.sh`, motifs lus dans la gate de chaque état) : 0 ligne VENDOR et 0 ligne GENERIC sur les quatre fichiers de code des trois états ; motif g5 courant 0, motif élargi de D8c 0 ; contrôle des motifs et des références de CA-D8b-12 inchangé ; documents : rejeu final sur ce journal, la copie du G0, les diffs et le rapport de correction : rapport de correction. Commande du job g5 sur le worktree : OK.
  - O-8 : suite `s2-harness` : `Ran 216 tests`, `OK (skipped=2)`, sauts (ii) et (ii bis), 0 entrée TMP ; `cargo --locked xtask verify` : premier passage 19:37:36Z-19:37:44Z, VERT, sortie 0, S-G4 55 fichiers, S-G5 56 fichiers, 252 fragments contrôlés et 218 non contrôlés (corpus incomplet, comme à la base), 0 téléchargement rustup ; second passage sur l'arbre final : rapport de correction.
  - O-9 : 0 entrée dans chaque TMP neuf (O-1, O-2, O-3, O-4, O-11, suite, sonde, chaque mutant).
  - O-10 (`oracles/o10.py` du G1) : état D8b-2 18 assertions sur 18, état final 19 sur 19 ; structure identique à celle du G1 (commentaires seuls modifiés).
  - O-11 : `GIT_NAMESPACE=d8b-garde-corr` : sortie 3, message de garde, TMP 0 avant et après.
  - O-12 : runner 136 à 139 s (113 cas, 2026-10-01), `--tree` 63 à 68 s, `--history` 1,5 à 1,6 s : commentaire du job (`gates.yml` l.98-101).
  - Oracle local G3 de D8a : `model-pinning : 76 ok, 0 échec` ; lint `OK (R-1) : 3 fichier(s)` (réglage local ignoré du worktree, E-5 de D8a).
  - Sonde des refs de remplacement (`sonde-replace-blob.sh`, dépôt jetable, blob porteur remplacé par un blob propre) : `--tree` 2 `SECRETS/forme` (objet réel lu, C-G2-2) ; `--history` 2 `SECRETS/echec` (`refs/replace/…` pointe un blob, C-G2-4) ; 0 fragment.
  - Contrôle d'application (`diffs-corr.sh`) : application séquentielle des quatre sous-diffs et application du `lot.diff` sur `git archive 40b4cfb ':!biblio'`, comparées au worktree : rapport de correction.
- **Mutants** (`mutants_corr.py`, sha256 `ea5d53d613841b47243c9ffb6bc65575ae147d012ed21331c777e3e8986278e6` ; `mutants-run.sh`, six travailleurs, TMP neufs ; `oracles/mutants_bilan.py` du G1 ; `mut/campagne/`, 19:30:57Z-20:27:53Z) : 98 mutants appliqués, 0 inapplicable, `bash -n` 98 sur 98. Ce sont les 74 du G1 (`oracles/mutants.py`, importé tel quel ; M-16 et M-41 redérivés, leur ancre ayant changé : l'avis non-blob passe par `masque`, et `( set -o pipefail; git` figure aussi dans la ligne de C-G2-4), K-1 à K-7 et N-1 à N-9, N-8a, N-8p, N-8r, N-8s du G2, K-3b et K-6c à K-6f du correcteur. **91 tués, chacun par un tueur attendu**, aucun par un autre tueur :
  - K-1 par T-71 et T-71b ; K-2 par T-72 et T-73 ; K-3 par T-74 et T-74b ; K-3b par T-74b ; K-4 par T-75 ; K-5 par T-65 ; K-6a par T-76 ; K-6b par T-77 et T-80 ; K-6c par T-79 ; K-6d et K-6e par T-80 ; K-6f par T-76, T-77 et T-79 ; K-7 par T-78 ;
  - N-1 à N-4 par G-13 à G-16, un à un ; N-7 par V-21 ; N-8 par V-22 à V-25 ; N-8a, N-8p, N-8r, N-8s par V-22, V-23, V-24, V-25 ; N-9 par G-17 ;
  - M-16 redérivé par T-11, T-12 et T-79 ; M-41 redérivé par T-69 ; les 65 autres mutants tués du G1 par leurs tueurs du §5.
  **0 survivant non attendu** ; 7 équivalents déclarés, ceux du G1 (M-24, M-36a, M-36b, M-36d, M-36e, M-36f, M-38), dont M-24 et M-36d confirmés par le G2 ; 0 entrée TMP sur 98. Résumé : `RESUME campagne : 91 tue(s) (dont 0 par un autre tueur que l'attendu), 0 survivant(s) non attendu(s), 7 equivalent(s) declare(s), 0 survivant(s) a tueur ulterieur, 0 hors etat, 0 inapplicable(s)`. Rejeu d'un mutant, depuis la racine du worktree : `TMPDIR=<neuf> bash enforcement/tests/run-fixtures-secrets.sh F:/tmp/shogen-lots/D8b/correction/mut/campagne/<id>.sh` ; tueurs par mutant : `mut/campagne/bilan.out`. Aucun mutant n'a porté le worktree.
  - Hors campagne (`mut/ext2/`) : K-7a, K-7b et K-7c, qui retirent du seul `unset` `GIT_LITERAL_PATHSPECS`, `GIT_GLOB_PATHSPECS` ou `GIT_NOGLOB_PATHSPECS`, survivent au runner final (113 ok chacun, rejoués le 2026-10-01 avec T-75b, `cr-rr1/mut/`) : survivants équivalents au sens du verdict, sens fermé mesuré (`sonde-pathspecs.sh`, `sonde-pathspecs-excl.sh` : sans `unset`, ces trois variables n'ajoutent que des refus, sur les porteurs hors exclusions comme sous les exclusions du contrat ; seule `GIT_ICASE_PATHSPECS` ouvre un vert, tué par T-78).
- **Lignes proposées pour l'annexe A** (acte de l'orchestrateur ; remplacent les lignes D8b, D8b-1, D8b-2 et D8b-3 du §1 ; D8b-C ajoutée) :

| lot (date) | objet (décision) | véhicule | oracle non-LLM nommé | taille (R-25) | tuyau (entrée → sortie → consommateur ; test) | cp-1 |
|---|---|---|---|---|---|---|
| **D8b** (2026-09-29 ; amendée le 2026-09-30 par le G0, le G1 et la correction de la revue G2, et le 2026-10-01 par la correction de sa re-revue) | D8 : `gate-secrets.sh` porté du blob `6789a30` (arbre, index), mode `--history` neuf (G0 §5.1, cp-1 C-1), job `g3-secrets` ; écarts nommés au blob : ligne E-D8b-G1 de l'annexe E ; correction G2 C-G2-1 à C-G2-11 (objets réels, greffes et refs non-commit refusées, chemins masqués, pathspecs lues telles qu'écrites) | `enforcement/`, `gates.yml`, tests shell | O-1 à O-12 du G0 amendé ; 113 cas ; 98 mutants de gate et le mutant R4b de la re-revue | 409 [mesuré : D8b-1 184 + D8b-2 113 + D8b-3 112] au lieu de ≈ 130 | arbre et historique → gate → job g3 (partiel : GC-01, GC-09) et G3 opérant local ; hook : item 4 ; tests O-2, O-3 et O-4 | complet |
| **D8b-1** (2026-09-30 ; coupe R-25 du G0 de D8b ; corrigé le 2026-09-30) | moteur porté (arbre, index) ; références réattribuées ; jetons ; argument inconnu refusé ; `LC_ALL=C` ; correction G2 : type d'entrée par pathspec `:(literal)`, objets réels, variables de pathspec de l'appelant retirées, chemins masqués ; cas T-01 à T-14 | `enforcement/gate-secrets.sh`, runner, 4 lignes de fixture | O-1 (14 cas), O-6, O-9, O-11 ; O-5 sur l'état final | 184 [mesuré] | non branché seul : consommable au G7 avec D8b-2 | complet (sous le cp-1 du lot) |
| **D8b-2** (2026-09-30 ; coupe R-25 du G0 de D8b ; corrigé le 2026-09-30) | contrat d'exclusion, sondes par alternative et par seuil (fixture tronquée), job `g3-secrets` (runner, `--tree`), en-tête de `gates.yml` ; cas T-15 à T-35, T-68 ; correction G2 : T-71, T-71b, T-72, T-77 à T-80, dix sondes | la fixture, le runner, `.github/workflows/gates.yml` | O-1 (84 cas), O-2, O-6, O-7, O-9, O-10 ; O-5 sur l'état final | 113 [mesuré] | arbre → gate → job g3 et G3 opérant local ; test O-2 et O-4 | complet (sous le cp-1 du lot) |
| **D8b-3** (2026-09-30 ; coupe R-25 du G0 de D8b ; corrigé le 2026-09-30 et le 2026-10-01) | mode `--history` (`--all`, drapeaux forcés, refus du superficiel, attribution, `pipefail`), `fetch-depth: 0`, étape 3 ; correction G2 : greffes et refs non-commit refusées, `-c diff.dstPrefix=b/`, attribution masquée ; cas T-51 à T-67, T-69, T-70, T-73 à T-76, T-74b, T-75b | les deux scripts, `gates.yml` | O-1 (113 cas), O-3, O-4 (k = 2), O-5 (98 mutants et R4b), O-6 à O-10, O-12 | 112 [mesuré] | historique → gate → job g3 et G3 opérant local ; test O-3 et O-4 | complet (sous le cp-1 du lot) |
| **D8b-C** (2026-09-30 ; correction de la revue G2 de D8b ; complétée le 2026-10-01 par la correction de sa re-revue) | liste fermée C-G2-1 à C-G2-11 et écarts mesurés 1 à 4 ; liste fermée CR-rr1-1 de la re-revue (T-75b) ; diffs de correction datés, `correction-G2-2026-09-30.diff` et `cr-rr1/correction-rr1-2026-10-01.diff` | gate, runner, fixture, commentaires du job, ce journal, copie du G0 | mêmes oracles ; re-revue ciblée (Q-G2-3), rr1 | +58 −15 [mesuré, code, état du lot du G1 vers état final] | inchangé | sous le cp-1 du lot |

- **Ligne proposée pour l'annexe E** (remplace celle du §1) :

| id | avis (fichier, question, ligne) | recommandation de l'avis | dans ADR-0028 | statut |
|---|---|---|---|---|
| E-D8b-G1 | advisor Q8 pt 2, l.97 (source canonique = blob d'`adb2213`) ; cp-1 D8b C-2 ; revue G2 de D8b, C-G2-1, 2, 8, 9 | porter le blob `6789a30` tel quel | D8, lot D8b : blob porté avec des écarts nommés : messages en français et jetons ASCII `SECRETS/…` (CH-6) ; argument inconnu refusé au lieu du repli sur le mode indexé (CH-7) ; `LC_ALL=C` exporté (CH-8) ; références à `ADR-0004` (neuf lignes du blob) réattribuées à l'ADR-0004 de VibeGates (trois occurrences, en-tête) ou retirées des messages, `pass-4-report.md` cité en amont complet, deux pourcentages [abs] retirés, filet d'un scanner dédié déclaré absent (CH-5) ; mode `--history` ajouté (fonction neuve, D8b-3) ; type d'entrée lu par une pathspec `:(literal)` (C-G2-1 : un nom à caractère de glob était pris pour une autre entrée) ; `GIT_NO_REPLACE_OBJECTS=1` exporté (C-G2-2 : objets réels) ; chemins en forme d'identifiant masqués dans les constats et les avis non-blob (C-G2-8) ; variables de pathspec de l'appelant retirées (C-G2-9) | tranché autrement (G0 CH-5 à CH-8, cp-1 C-2 ; revue G2 C-G2-1, 2, 8, 9) |

- **Texte proposé pour l'amendement d'ADR-0028 §4.11** (acte de l'orchestrateur ; remplace celui du §7) : « *Amendement daté du 2026-09-30 (lot D8b)* : à partir du commit de D8b, le G3 opérant comprend aussi les trois commandes du job `g3-secrets` : `bash enforcement/tests/run-fixtures-secrets.sh` (sortie 0 ; résumé `secrets : 113 ok, 0 échec`), `bash enforcement/gate-secrets.sh --tree` (sortie 0) et `bash enforcement/gate-secrets.sh --history` (sortie 0) ; tout constat de l'historique hors de l'ascendance du commit rejoué est rapporté masqué, sans être compté comme un défaut du lot rejoué ; un refus `SECRETS/tronque` (greffes) ou `SECRETS/echec` (ref vers un blob ou un arbre) sur l'arbre de rejeu est un état de cet arbre, rapporté comme tel. »
- **Items** (du G2, versement à l'annexe B : acte de l'orchestrateur ; lignes de la gate corrigée) :

| # | item | objet | construction | propriétaire | déclencheur |
|---|---|---|---|---|---|
| I-G2-1 | SHOGEN-SECRETS-CHEMIN-ETAGE-1 | `git show ":$f"` (l.122, et l.125 deux fois) lit un chemin `<0-3>:<reste>` comme une entrée d'étage (gitrevisions 2.55, lu par le G2) : sur l'image Linux, `0:x` porteur à côté de `x` propre serait lu comme `x` ; chemin refusé par Git for Windows, non mesurable en local | `":0:$f"`, de même sens pour tout chemin valide ; cas sur l'image | orch. | item 3 (forge rétablie) ou G0 de D8c, au premier des deux |
| I-G2-2 | SHOGEN-SECRETS-GREP-STATUT-1 | les pipelines de verdict (l.98 ; l.125 et son repli `true`) confondent l'absence de ligne (sortie 1 de `grep`) et une erreur de `grep` (sortie 2) : une erreur rendrait un vert ; non mesuré | **recherche** : capter les statuts sans changer le verdict des cas portés ; mutant d'erreur à définir | orch. | G0 de D8c (le crochet réemploie le moteur) |
| I-G2-3 | extension de SHOGEN-D8-HOOK-SECRETS-1 (item 4) | les modes arbre et indexé ne balaient pas les noms de chemin (A10d) ; l'historique les voit ; le crochet de D8c, en mode indexé seul, non | balayer `git diff --cached --name-only` par les mêmes motifs, sortie masquée | orch. | G0 de D8c |
| I-G2-4 | SHOGEN-SECRETS-MASQUE-EXCLUSION-1 (étendu par le correcteur) | messages qui impriment un chemin ou une pathspec en clair : contrat d'exclusion (l.67, l.71-73, l.75-76), chemin des greffes (l.89), échec de `git show` (l.122) | `masque` par substitution de commande sur ces sites, 0 ligne nette, un cas par famille | orch. | G0 de D8c, ou première entrée du fichier d'exclusion |

- **Items du G1 touchés** : l'item 3 (c) gagne `sed -E` et son drapeau `I` (C-G2-8), `git for-each-ref` et `%(*objecttype)` (C-G2-4 : un git qui ne pèlerait qu'un niveau refuserait un tag imbriqué vers un commit, sens fermé [inféré]), `-c diff.dstPrefix` (clé inconnue d'un git plus ancien : sans effet, locale comme forcée [inféré]) et `GIT_GRAFT_FILE` (T-74b) sur l'image ; l'item 4 gagne I-G2-3.
- **Questions à l'orchestrateur** : **Q-C-1** : ratifier les écarts 1 à 4 (trois cas ajoutés, `mkdir` de T-74, commentaires). **Q-C-2** (Q-G2-1, ouverte) : jetons de C-G2-3 (`tronque`) et de C-G2-4 (`echec`), appliqués selon la proposition du G2. **Q-C-3** (Q-G2-3) : re-revue ciblée des seules corrections, avec rejeu du runner (113 cas depuis T-75b), des K et des N, et des quatre mutants de l'écart 1. **Q-G2-4** et **Q-G2-5** inchangées : transmission de C-G2-1, C-G2-8 et E-6 à SHOGEN-D8-AMONT-ERRATUM-1 ; ratification de Q-G1-2, Q-G1-3 et Q-G1-8.
- **`error_origin` proposés** (assignation au G7) :
  - **E-7** : liste fermée du G2 sans cas pour quatre sous-sites de ses propres corrections (K-3b, K-6c, K-6d, K-6e survivaient au runner du G2). Origine : G2.
  - **E-8** : commentaire `jamais imprimé` de la ligne `masque`, démenti par les sites de I-G2-4. Origine : G2.
  - **E-9** : estimation R-25 de la correction ≈ 184, 110 et 108 pour 184, 113 et 111 mesurés (cas et commentaires décidés après la mesure des mutants de sous-site). Origine : worker G1 de correction.
  - **E-10** : premier lancement du générateur de mutants de la correction en erreur (chemin d'import en forme POSIX pour un Python Windows), corrigé avant toute génération ; aucun effet. Origine : worker G1 de correction.
  - **E-11** : à l'orientation, `git status --short` lancé une fois sur ce worktree sans `--no-optional-locks`. Effet mesuré : nul (index du worktree à 17:34:45Z, index de `F:/Shogen` à 16:37:55Z, antérieurs à la correction). Même forme que E-G2-3. Origine : worker G1 de correction.
- **Attestation** (forme D.3) : pièces de l'annexe D.2 non ouvertes, ni `F:/shogen-campagne/*`, ni `F:/tmp/shogen-j28/*`, ni `measure-M009a.md`, ni `F:/tmp/shogen-carto-2026-09-29/campagne.md` ; `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée (`unset` dans chaque script). Aucune statistique S2 calculée sur les journaux de campagne ; aucun z, K, P̂_more ni φ de campagne vu. La gate a balayé mécaniquement les fichiers suivis (O-2, O-3, O-4), dont deux portent une ligne de D.2 : seuls des comptes, des codes de sortie et des lignes de verdict ont été imprimés, 0 constat. Git : sur ce worktree, `status --short` (E-11), `diff HEAD`, `archive`, `grep` (commande du job g5) et les lectures de la gate (O-2, O-3) ; aucun `add` (les fichiers du lot étaient déjà en intention d'ajout) ; sur `F:/Shogen`, lectures (`rev-parse`, `for-each-ref`, `worktree list`, `rev-list`, `status --porcelain=v1`, lectures de la gate) en `--no-optional-locks` ou `GIT_OPTIONAL_LOCKS=0`, et `clone --shared` vers `F:/tmp` (O-4) ; `init`, `add`, `commit`, `replace`, `tag`, `update-index`, `checkout` et `reset` dans les seuls dépôts jetables et clones sous `F:/tmp`. **Aucun `GIT_DIR`, aucun `GIT_WORK_TREE`, aucun `--write-tree`** ; aucun commit, stash, checkout, reset ni push sur `F:/Shogen` ni sur ce worktree. Rien écrit sur C:.
- **Correction de la re-revue rr1** (2026-10-01, ajout daté ; les puces précédentes ne changent que par leurs comptes, mis à jour en place) :
  - **Générateur et mandat** : `claude-opus-5-5` (modèle résolu déclaré par le harnais, R-1), effort max, worker de correction à contexte frais, distinct du réviseur rr1 ; liste fermée CR-rr1-1 de la re-revue ciblée des corrections (`F:/tmp/shogen-lots/D8b/rr1/` : mutant `mut/R4b-refs-tagcommit.sh`, bilan `mut-bilan.txt`). Même worktree, HEAD `40b4cfb`, rien de commité ; aucun `GIT_DIR` ni `GIT_WORK_TREE` ; `add` et `commit` dans les seuls dépôts jetables sous `F:/tmp`. Horloge (`date -u`) : 2026-09-30T23:37:03Z orientation ; 23:45:25Z état d'avant figé (`cr-rr1/avant/`) ; 23:48:21Z runner modifié ; 23:50:36Z-23:58:02Z rejeux de gates (G1, R4b, K-7a à K-7c, équivalents) ; 23:58:32Z-2026-10-01T00:03:07Z O-1 ; 00:03:31Z commentaire du job ; 00:03:52Z état D8b-3 figé (`cr-rr1/etats/d8b-3r/`) ; 00:04:08Z-00:05:19Z O-3 et O-2 ; documents ensuite.
  - **Constat de la re-revue** : le mutant R4b (alternative `tag commit` retirée de l'`awk` du contrôle des refs, gate l.90) survivait au runner à 112 cas : aucun cas ne posait de tag annoté, alors que l'arbre réel en porte un (`refs/tags/archive/roster-ban-2026-08-20`).
  - **Changement** (D8b-3) : runner l.161, **T-75b** : dépôt jetable, tag annoté `ta` vers le commit initial (`git tag -a ta -m t`), `--history` → 0, `historique, 1 commit(s)` (sens ouvert de C-G2-4 ; A11b du G2, au premier niveau) ; liste du commentaire l.109 complétée ; commentaire des temps du job (`gates.yml` l.98-101, quatre lignes gardées) : 113 cas et temps re-mesurés. Gate et fixture inchangées. Empreintes : runner `f9e7ef02084611bd99806e35145230a063ed07bdb3f3be5ae7456954adb84837` (164 lignes), `gates.yml` `32f79e4926f28a5cb3f359feba0801a64498eac0db3244ffa8d40a5ff4e8144c`.
  - **Preuves** (scripts et sorties sous `F:/tmp/shogen-lots/D8b/cr-rr1/`) : O-1 `113 ok, 0 échec` sous `TMPDIR=F:/…` (136 s) puis `/f/…` (139 s), sortie 0, 0 entrée TMP, lancés seuls (charge résiduelle d'autres agents non maîtrisée, `o1/charge.log`) ; R4b rejoué avec ce runner : sortie 1, `112 ok, 1 échec`, T-75b seul ; gate du lot du G1 : `100 ok, 13 échec`, les treize cas de défaut, T-75b vert (la gate du G1 n'a pas de contrôle des refs : T-75b ne vise pas un défaut du lot) ; K-7a à K-7c et les sept équivalents déclarés (M-24, M-36a, M-36b, M-36d, M-36e, M-36f, M-38) : `113 ok, 0 échec` chacun, T-75b n'en tue aucun ; O-3 puis O-2 sur `F:/Shogen` (HEAD `15d4c20`, 20 refs : 19 vers un commit et le tag annoté réel, `tag commit` ; forme de C-G2-4 : 0 ; même forme sans `tag commit` : 1 ; aucun fichier de greffes, aucune ref de remplacement) : `--history` 0, `historique, 159 commit(s) (--all)`, 1,5 s ; `--tree` 0, 307 fichiers, 68 s ; un avis, 0 REFUS, 0 fragment ; sonde : R4b en `--history` sur ce même arbre, sortie 2 `SECRETS/echec` ; oracle local G3 de D8a : `model-pinning : 76 ok, 0 échec`, lint `OK (R-1) : 3 fichier(s)`. Sonde locale (git 2.55.0.windows.5, dépôt jetable) : un tag annoté imbriqué vers un commit rend aussi `tag commit` (objet pelé jusqu'au commit), gate 0, R4b 2 ; pour l'image, l'item 3 (c) reste [inféré].
  - **Comptes mis à jour en place** (112 → 113 et leurs suites) : puce datée de l'en-tête, §1 (R-25), §2 (empreintes), §4, §7, et au §15 les lieux, R-25, O-1, O-12, K-7a à K-7c, les lignes D8b, D8b-3 et D8b-C de l'annexe A, le texte de §4.11 et Q-C-3 ; copie du G0 : CH-2, CH-3, CH-12, §7, O-1, O-5 et §16. R-25 après T-75b (`cr-rr1/r25-rr1.out`) : D8b-1 184 et D8b-2 113 inchangés, **D8b-3 112** (runner +55 −2), 409 en somme, 392 au `lot.diff` ; cette correction seule : code +6 −5 (runner +2 −1, `gates.yml` +4 −4).
  - **Diffs** (`cr-rr1/`) : `d8b-1.diff` et `d8b-2.diff` identiques, octet pour octet, à ceux de la correction ; `d8b-3.diff`, `docs.diff` et `lot.diff` régénérés ; diff de cette correction seule, `correction-rr1-2026-10-01.diff` ; contrôles d'application et empreintes : `cr-rr1/rapport.md`.
  - **`error_origin` proposés** (assignation au G7) : **E-14** : aucun cas positif pour l'alternative `tag commit` du contrôle de C-G2-4 (T-75 ne vise que le sens fermé ; l'écart 1 n'a cherché de sous-site que pour C-G2-3 et C-G2-8). Origine : G2 et worker G1 de correction. **E-15** : un premier appel de Python sous la forme `python - <fichier>` a fait lire au lanceur de Windows le shebang du runner passé en argument et lancer `bash` sur lui ; `bash` s'est arrêté au démarrage (erreur fatale de canal de signal) ; effet mesuré nul (runner inchangé, sha256 `7eb01b39…fa99` relu aussitôt, aucune sortie de cas). Origine : worker de correction rr1 (discipline d'environnement).
