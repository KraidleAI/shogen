# G0 — lot D8b d'ADR-0028 : gate secrets (`enforcement/gate-secrets.sh`), mode historique, job g3 — Shōgen, document de planification

- **Statut** : G0 proposé, soumis au **cp-1 complet** (annexe A l.31, colonne cp-1 = « complet »). Aucun code n'est écrit par ce document.
  - *Amendement daté du 2026-09-30 (G1 du lot, `claude-opus-5-5`)* : G0 accepté au cp-1 complet du validateur-humain, décision ACCEPTE-AVEC-CORRECTIONS, liste fermée C-1 à C-9 (`F:/tmp/cp1-D8b/CP1-D8b.md`, sha256 `f17ad25ea4f7ad9138362def74c898d60ca4872558bc520ee6bba7843ba0a725`). Le texte accepté est conservé à l'identique (sha256 `2b928eddedcd37b7fdad473104dc0c8e502dd310e99c931c32c75c223fc213c8`, `F:/tmp/shogen-lots/D8b/G0-lot-D8b.md`) ; chaque correction, et chaque fait du G1 qui supplante une ligne, est une puce datée placée sous le point visé, indexée au §16 (C-9). Le `diff -u` entre le texte accepté et cette copie est livré avec le G1 (`F:/tmp/shogen-lots/D8b/oracles/G0-copie.diff`, 0 ligne retirée).
- **Rédacteur** : worker G0 `claude-opus-5-5` (modèle résolu déclaré en tête de session, R-1), effort max, contexte frais. Destinataire : orchestrateur Shōgen `claude-fable-5-1`. Réviseurs attendus : orchestrateur (R-21), puis validateur-humain (cp-1 complet).
- **Horloge** (`date -u`) : première heure relevée 08:26:31Z, l'orientation la précède de peu ; mesures G0 de 08:33:09Z (`g0-mesures/horloge-debut.txt`) à 09:02:54Z ; `action.yml` d'actions/checkout lu juste après 08:45:03Z (heure relevée avant la lecture) ; advisor intégré consulté deux fois, après l'orientation (avant la rédaction) puis avant la remise ; rédaction à partir de 09:06:03Z ; sceau de `g0-mesures/` à 09:14:33Z (§15), contrôles du texte final au §15 bis.
- **Mandat** : commande de mission de l'orchestrateur (workflow du 2026-09-30, reprise après limite), lot D8b de l'annexe A. Base de mission : `fb089dc`. `main` est à `cf696bd` au moment des mesures : 11 commits de plus, aucun sur `enforcement/` ni sur `.github/workflows/gates.yml` (blob `1839bc2` aux deux commits). D8a n'est pas commis : sa correction est livrée (`F:/tmp/shogen-lots/D8a/lot.diff`, sha256 `9b6027eb826f0d3e40376d7b9e2c884b24bca83af3b66a2b06bf83f5a990e0a0`). Lecture seule sur `F:/Shogen` ; aucun worktree utilisé.
  - *Amendement daté du 2026-09-30 (cp-1 C-1)* : la prémisse de la commande de mission, un gate qui balaierait l'arbre et l'historique d'après sa source, est fausse, comme le mesurent le §0 (a) et le §5.1 : le blob `6789a30` n'a que les modes `--tree` et indexé (l.37, l.76-80) ; l'historique est une fonction neuve, portée par D8b-3. La ligne du lot à l'annexe A est la l.31 à `cf696bd` (la l.37 à `40b4cfb`). Base du G1 : `40b4cfb`, `main` après les commits de D8a, E1, DOCS-S2-a et SIM-NIVEAU ; `gates.yml` y est au blob de l'état cible du §4 (sha256 `bc3aea17…af53`, 122 lignes, mesuré).
- **Isolation git** : aucun `GIT_DIR`, aucun `GIT_WORK_TREE`, aucun `--write-tree` ; aucun commit, add, stash, checkout, reset ni push sur `F:/Shogen`. Commandes employées sur `F:/Shogen` : `rev-parse`, `log`, `merge-base --is-ancestor`, `diff --stat` entre deux commits, `show`, `cat-file`, `ls-tree`, `ls-files`, `count-objects`, `for-each-ref`, `config --get`, `hash-object` sans `-w`, `worktree list`, `archive` (vers `F:/tmp`, copie du contrôle xtask), et, en contrôle final, `status --porcelain=v1 --untracked-files=no` et `diff --name-only` (0 fichier suivi modifié). Sur le clone VibeGates du corpus (C:, lecture seule) : `log`, `ls-tree`, `show`, `grep`, `rev-parse`, toutes en `--no-optional-locks`. Copie de travail : `git clone --shared` de `F:/Shogen` vers `F:/tmp/shogen-lots/D8b/work/clone` (forme admise par la règle du 2026-09-25), puis `checkout --detach cf696bd` dans ce clone seulement. `git init`, `add` et `commit` n'ont eu lieu que dans des dépôts jetables `mktemp` sous `F:/tmp/shogen-tests-tmp/d8b-g0/`, hors de tout dépôt.
  - **Écart déclaré** : `git status --short` a été lancé une fois sur `F:/Shogen`, à l'orientation (08:26:31Z). `git status` peut poser un `index.lock` transitoire. Mesuré à 08:28:30Z : `.git/index` à 07:42:11Z et `refs/heads/main` à 07:41:49Z (commit `cf696bd`), inchangés ; mtime du dossier `.git` à 08:26:33Z, attribuable à cette commande ou aux worktrees de la vague 2, actifs. Toutes les lectures suivantes sont en `git --no-optional-locks`. Même forme que l'écart du G0 de D8a. `error_origin` proposé : worker G0.
- **Écritures** : `F:/tmp/shogen-lots/D8b/` seulement : ce document et `G0-lot-D8b.md.sha256` ; `g0-mesures/`, scellé au §15 ; `work/`, jetable (clone, reconstitution de `gates.yml` après D8a, copie du contrôle xtask, petits scripts d'édition) ; `target/` (109 Mo, cible cargo du contrôle xtask) ; `xtask-g0-v2.*` (contrôle du texte final, §15 bis). Dépôts jetables sous `F:/tmp/shogen-tests-tmp/d8b-g0/`, supprimés à la sortie de chaque script (0 dépôt restant, mesuré) ; seul y reste le sous-dossier `cargo`, vide, TMP du contrôle xtask. Rien sur C: (`TMPDIR`, `TMP` et `TEMP` posés sur `F:/tmp/shogen-tests-tmp/d8b-g0` pour chaque mesure).
- **Interdits (annexe D.2 et D.4 a)** : aucune pièce de campagne ouverte (`F:/shogen-campagne/*`, `F:/tmp/shogen-j28/*`, `measure-M009a.md`, `F:/tmp/shogen-carto-2026-09-29/campagne.md`) ; `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée ; aucune statistique S2 lue ni calculée. Le balayage mécanique de l'arbre et de l'historique (§5.3) a lu des fichiers suivis, dont deux portent une ligne de D.2 (annexe D l.35-36) : seuls des comptes, des temps et des codes de sortie ont été imprimés, aucune ligne de contenu.

## 0. Résumé (une phrase par tâche, CA-1)

1. **Porter** le plancher canonique (blob `6789a30`) pour les modes indexé et `--tree`, avec les écarts nommés au §6 (références réattribuées, chiffres de seconde main retirés, jetons, argument inconnu refusé, `LC_ALL=C`).
2. **Ajouter** un mode `--history`, fonction neuve : il balaie toutes les refs par un seul flux `git log -p` ; le verdict vient de `grep` sur les lignes ajoutées, l'attribution d'un `awk` qui ne sert qu'au message.
3. **Tester** par un runner qui forme les valeurs à l'exécution, dans des dépôts jetables, à partir de fragments tronqués rangés sous `enforcement/tests/fixtures/secrets/`. Aucun fichier suivi ne porte une forme complète.
4. **Brancher** le tout au job `g3-secrets` de `gates.yml` (runner, arbre, historique ; `fetch-depth: 0`).

Faits nouveaux à porter en tête (FM-2.4) :
- (a) la prémisse de la mission, selon laquelle le gate balaie l'historique d'après sa source, ne tient pas pour le blob `6789a30` (§5.1) ;
- (b) le runner amont n'est pas portable tel quel : 19 de ses lignes portent une forme complète d'identifiant (§5.2) ;
- (c) le contrat canonique s'appuie sur un scanner dédié en CI, absent de Shōgen (§5.5) ;
- (d) les neuf références nues à `ADR-0004` du canonique désigneraient, dans Shōgen, l'ADR multi-attestor (§5.5) ;
- (e) taille : ≈ 404 lignes au lieu des ≈ 130 de l'annexe A, qui ne comptait pas les tests ; coupe en trois sous-lots (§9).

## 1. Objet et décisions rattachées

| rattachement | lieu | ce qu'il fixe pour D8b |
|---|---|---|
| D8 | `docs/adr-0028/ADR-0028-decisions-sortie-S2.md` l.212-220 à `cf696bd` (l.93-101 à `fb089dc`) | lots D8a-c ; `enforcement/` (gate secrets) et jobs g1/g3 (l.213) ; source canonique = blob d'`adb2213`, sha cité `6789a30` (l.214) |
| ligne de lot | `docs/adr-0028/ANNEXE-A-lots.md` l.31 | véhicule `enforcement/`, `gates.yml` ; oracle : sonde positive et négative (rejeu de git-ci §2.b, sortie 0 sur l'arbre propre) ; ≈ 130 : 107 [mesuré] + ≈ 22 [inféré] ; tuyau arbre et historique → gate → job g3 ; cp-1 complet |
| ordre | annexe A l.9 et l.11 ; G0 de D8a §13 | lots D8 en parallèle de la voie A ; D8a, D8b, D8c dans cet ordre, chacun sur le commit du précédent (conflit de fichier `gates.yml`) |
| item | `docs/adr-0028/ANNEXE-B-items.md` l.24 | SHOGEN-ENFORCEMENT-PORTAGE-1 (lots D8a, D8b, D8c, puis tag, puis suppression de la branche) |
| précondition | ADR-0028 l.279 ; `JOURNAL.md` l.122 | PC-1 : lecture (b) consignée pour la gate secrets et les jobs g1/g3/g5 (§2) |
| G3 opérant | ADR-0028 l.196 (D6 iii) et l.290 (§4.11) | forge morte : le G3 opérant est l'oracle local rejoué par l'orchestrateur ; le job ne sert de preuve qu'à la forge vivante |
| custodie | ADR-0028 l.211 (D7) | aucune réécriture d'historique : conséquence au CH-15 |
| corpus | doc 02 l.46-47 (G3, mutation), l.89 (R-8), l.98 (R-13), l.112 (R-23), l.114 (R-25) ; `templates/ci-gates.yml` l.44-60 | le job G3 du gabarit porte un outil dédié plus le plancher `gate-secrets.sh --tree` |
| précédent | G0 de D8a (`F:/tmp/shogen-lots/D8a/G0-lot-D8a.md`, sha256 `8afa3f7dd2c7232ea459bd7308e97391b61c99055084cd6035262d10afe4c387`) et son `lot.diff` | forme du G0, jetons, runner, O-10 par PyYAML, coupe en sous-lots, état cible de `gates.yml` |

## 2. Précondition PC-1 (§4.10 a) — consignée, non bloquante pour le G1

- ADR-0028 l.279 fait de la confirmation de la décision du 2026-08-20 (forme g1/g3/g5) un préalable de D8.
- `JOURNAL.md` l.122 (orchestrateur, 2026-09-30 04:5x UTC) consigne la lecture (b) du §2 du G0 de D8a : le portage `enforcement/`, gate secrets et jobs g1/g3/g5 compris, est couvert par la délégation du 2026-09-30, veto §4.10 a non exercé et révocable jusqu'à l'exécution unique. Le commit du lot ne dépend pas de PC-1.
- Restent un acte de l'investisseur : la pose du tag `archive/roster-ban-2026-08-20` et la suppression de la branche. Ce G0 ne les touche pas.
- Si le veto est exercé avant le commit : D8 passe en ADR de retrait, le worktree du G1 est abandonné, aucun commit.

## 3. Périmètre

**IN**

| fichier | nature |
|---|---|
| `enforcement/gate-secrets.sh` | neuf ; porté du blob `6789a30` (D8b-1), plus le mode `--history` (D8b-3) |
| `enforcement/tests/run-fixtures-secrets.sh` | neuf ; conçu d'après l'amont `enforcement/tests/run-fixtures.sh` (blob `7960238`, section secrets l.35-169) ; chemin du gate en `$1` |
| `enforcement/tests/fixtures/secrets/sondes.tsv` | neuf ; fragments tronqués, une ligne par sonde (CH-4) |
| `.github/workflows/gates.yml` | job `g3-secrets` ; en-tête (l.3-7 et l.19-20 de l'état après D8a) |
| `docs/G1-lot-D8b.md` | journal G1, au format de `docs/G1-lot-B0-pool-analyse.md` |
| `docs/adr-0028/G0-lot-D8b.md` | copie de ce G0 (précédent de D8a, `lot.diff` l.435) |

**OUT**, avec motif :
- Lint et job g1 : lot D8a. Hook versionné, motif g5 élargi, entrée « collision ADR-0020 » : lot D8c. Le mode indexé est porté et testé ici, mais son consommateur, le hook, relève de D8c (item 4).
- Tag et suppression de la branche `roster-ban-alignment-2026-08-20` : acte de l'investisseur (§2).
- `enforcement/gate-gist.sh` de l'amont et la section GIST de son runner : hors D8 (ADR-0028 l.213 ne nomme que le lint, la gate secrets et le hook).
- Scanner dédié du gabarit (l.57-58) et balayage des secrets par la forge (P10) : items 1 et 2.
- Réécriture de la boucle par fichier du canonique, pour la vitesse : hors lot (fidélité ; coût mesuré au §5.3 ; CH-11).
- Objets inatteignables, commits connus des seuls journaux de refs, bundles de custodie : item 5.
- `s2-harness/` en entier (vague 2 en vol ; mission). ADR-0028 et ses annexes : les lignes datées des sous-lots sont un acte de l'orchestrateur (ADR-0028 §6, l.305-307).
- Tout autre fichier de `F:/Shogen`.

## 4. Sources lues (niveau, lieu)

| source | lieu | niveau | usage |
|---|---|---|---|
| blob canonique `6789a30` | `git show adb2213:enforcement/gate-secrets.sh` (107 l., sha256 `565c81af1acf66708b16fd68ef66341be8925d42398180368a7d6bd211f16d8c`, égal à la copie de la cartographie) | [lu] en entier | base du port ; l.2-37 (contrat), 40, 43-46, 48-49 (motifs), 51-70 (exclusions), 71, 73-74, 76-80 (modes), 82-100 (boucle), 102-107 |
| job g3 d'origine | `adb2213:.github/workflows/gates.yml` (blob `493ae8c`) l.59-68 | [lu] | `--tree` seul, checkout v4.4.0 sans `fetch-depth` |
| `gates.yml` courant et après D8a | `cf696bd` l.1-92 (blob `1839bc2`, identique à `fb089dc`) ; état reconstitué par `patch -p1` des l.1-62 du `lot.diff` de D8a : 122 l., sha256 `bc3aea1773b827f32c9293e37856138704912f71e054397983cc07267223af53` | [lu] | en-tête l.3-20, règle d'un seul nom (l.60 à `cf696bd`), job g1 l.55-82, job s2 l.84-122 |
| amont VibeGates | clone du corpus `…/vibegates` (HEAD `1263f2a`, branche `pass-4-u4`) : `enforcement/gate-secrets.sh`, `enforcement/tests/run-fixtures.sh` (blob `7960238`, 239 l.), `docs/adr/ADR-0004-guard-escalation-adjudication.md` l.11-17 et l.25 | [lu] | provenance ; conception des cas ; filet du scanner dédié |
| cartographie git-ci | `F:/tmp/shogen-carto-2026-09-29/git-ci.md` l.22, 26, 90-119, 225, 230 | [lu] | P6, P10, §2.b (rejeux l.116-117, amont non localisée l.118), GC-05, GC-10 |
| hook local | `.git/hooks/pre-commit` (sha256 `1da91c723b7f4747edb35dcc2cce7492e334b648c5e00c41f239cca5ab61277d`, égal à `guard.sh` de la cartographie) | [lu] | ne lance aucun balayage de secrets : consommateur 2 absent |
| ADR-0028, annexes A, B, C, D | lignes citées au fil du texte, à `cf696bd` | [lu] | cadre |
| JOURNAL | l.122, l.127 | [lu] | PC-1 ; D8b et D8c suivent D8a dans le même run |
| DECISIONS | `docs/DECISIONS.md` l.8 et l.194 | [lu] | ADR-0004 de Shōgen = multi-attestor |
| corpus | doc 02 l.46-47, 89, 98, 112, 114 ; `templates/ci-gates.yml` l.44-60 | [lu] | G3, R-8, R-13, R-23, R-25 ; job G3 du gabarit |
| gates xtask | `xtask/src/sg4.rs` l.1-20 et l.30-60 ; `sg5.rs` l.1-30 ; `documents.rs` l.75-89 et l.206-250 | [lu] | S-G4 : 15 locutions, guillemets ASCII orphelins = incident ; S-G5 : fragments anglais entre guillemets français |
| actions/checkout | `https://raw.githubusercontent.com/actions/checkout/3d3c42e5aac5ba805825da76410c181273ba90b1/action.yml`, Firecrawl `maxAge: 0`, lu juste après 08:45:03Z ; extrait recopié dans `g0-mesures/action-checkout-3d3c42e5.yml` | [lu] | `fetch-depth`, `persist-credentials`, `set-safe-directory` (§5.7 a) |
| git 2.55.0.windows.5 | documentation HTML locale `C:/Program Files/Git/mingw64/share/doc/git-doc/` (git-log, git-rev-parse, git-rev-list, git-cat-file, git-diff), extraite en texte dans `g0-mesures/*-2.55.0.txt` ; lignes citées dans ces extraits | [lu] | §5.7 b-d |
| précédents de lot | G0 de D8a (en entier) ; `F:/tmp/shogen-lots/D8a/G1-rapport.md` l.56, 214, 285-330 ; `G2-rapport.md` l.107 ; `correction-rapport.md` l.85 ; `oracles/o10.py` | [lu] | forme, compte R-25 des documents, contraintes du harnais au G1, O-10 |

Aucune de ces pages externes n'est versée à `biblio/INDEX.md`. Ce document les paraphrase ; les noms d'options et de clés sont en police de code, ce ne sont pas des citations (item 7).

## 5. Faits mesurés au G0 (`F:/tmp/shogen-lots/D8b/g0-mesures/`)

### 5.1 La source n'a que deux modes

- Blob `6789a30` : usage `gate-secrets.sh [--tree]` (l.37) ; modes l.76-80 : `git ls-files` (arbre suivi) ou `git diff --cached` (contenu indexé). Aucun `git log`, aucune lecture d'historique.
- Le job d'origine (`adb2213:gates.yml` l.59-68) ne lance que `--tree`, avec le checkout par défaut : un seul commit récupéré (§5.7 a).
- L'historique n'apparaît que dans deux pièces :
  - le rejeu ad hoc de git-ci §2.b l.117 : 32 commits non poussés, lignes ajoutées, comptes seuls ;
  - l'étape « outil dédié » du gabarit du corpus (l.57-58), qui n'est qu'un commentaire et n'a pas d'équivalent dans Shōgen.
- Conséquence : la prémisse de la mission ne tient pas pour le blob. Le tuyau de l'annexe A l.31 (arbre et historique) demande une **fonction neuve**, portée par D8b-3.
- Sonde S1 (§5.4) : un secret ajouté puis retiré passe le canonique en `--tree` et en mode indexé (sorties 0) ; le flux d'historique le voit (1 ligne).

### 5.2 L'amont VibeGates et son runner

- `enforcement/gate-secrets.sh` : blob `6789a30` = HEAD de l'amont (`1263f2a`) ; dernier changement au commit `1eb1b33`, 2026-08-13T19:20:08+01:00 (`git log -- enforcement/gate-secrets.sh` dans le clone). Même chaîne que le §5.1 du G0 de D8a : à joindre à SHOGEN-D8-AMONT-ERRATUM-1 (item 11 de D8a).
- Runner amont `enforcement/tests/run-fixtures.sh` (blob `7960238`, 239 l.) : 24 cas `SEC` (l.35-169) et 15 cas `GIST`. Aide `new_repo` l.17-22 (dépôt jetable, `git init`, commit initial) ; `check` et `run` l.24-33.
- **Mesure** : les deux motifs du gate, évalués depuis ses l.48-49 et appliqués au runner amont sous `LC_ALL=C`, trouvent **14 lignes VENDOR et 5 lignes GENERIC**. Le runner porte des formes complètes d'identifiant en clair ; sa copie dans Shōgen violerait la contrainte de la mission (jamais un format qui déclenche un scanner tiers). Le CH-4 en découle.
- Le blob du gate et le `gates.yml` d'origine : 0 et 0 (aucune auto-correspondance).
- La section GIST et `gate-gist.sh` restent hors lot (§3).

### 5.3 Coûts mesurés

Clone `--shared` de `F:/Shogen` sous `F:/tmp`, Git Bash, git 2.55.0.windows.5.

| mesure | valeur | fichier |
|---|---|---|
| canonique `--tree` à `cf696bd` | sortie 0 ; 286 fichiers ; 84 768 ms (boucle par fichier ; une dizaine de processus par fichier, [inféré] de la lecture des l.83-99) | `canon-tree-cf696bd.out` |
| P1 : flux `git log -p` unique, ascendance de `fb089dc` | 112 commits ; 4 086 945 octets ; 56 848 lignes ajoutées ; 0 VENDOR, 0 GENERIC ; 464 ms | `mesure-historique.out` |
| P1, ascendance de `cf696bd` | 123 commits ; 4 347 718 octets ; 57 771 lignes ; 0 et 0 ; 491 ms | idem |
| P2 : blob par blob (quatre processus par blob) | 630 blobs à `fb089dc` : 77 667 ms ; 662 à `cf696bd` : 83 429 ms ; aucun blob avec constat | idem |
| P1 sur `--all`, chemins d'exclusion et drapeaux du CH-2 | 128 commits, 16 refs ; 4 456 259 octets ; 58 203 lignes ; 0 et 0 ; 578 ms | `mesure-all.out` |
| prototype complet (`proto-historique.sh`, `--all`) | 128 commits, sortie 0 ; 1 008 ms | `proto-reel.out` |

Lecture :
- l'historique complet coûte environ une seconde ; la boucle par blob du canonique, appliquée à l'historique, en coûterait environ 80 ;
- aucune borne de profondeur n'est donc nécessaire (CH-3) ;
- l'arbre, par la boucle canonique, coûte environ 85 s en local ; ce coût pèse sur l'oracle local, pas sur le verdict.

### 5.4 Sondes de conception

Dépôts jetables ; valeurs formées à l'exécution ; seuls des comptes et des codes de sortie sont imprimés. Scripts `mesure-sondes.sh`, `mesure-s3bis.sh`, `proto-sondes.sh`.

| sonde | question | mesure | conséquence |
|---|---|---|---|
| S1 | ajout puis retrait | canonique `--tree` 0, indexé 0 ; flux 1 | mode historique requis |
| S2 | fusion qui introduit seule la valeur | flux sans `--diff-merges` : 0 ; avec `--diff-merges=first-parent` : 1 | drapeau requis |
| S3 | branche latérale ajout puis retrait, fusion identique au premier parent, chemin donné | 1, 1, 1 | voir S3 bis |
| S3 bis | quelles options parcourent la branche latérale | défaut et `-p` seul : `m base` (branche élaguée) ; `--diff-merges=first-parent` seul, ou `--full-history` seul : les cinq commits | `--full-history` posé d'après la documentation ; le mutant qui le retire survit sur git 2.55 (M-24) |
| S4 | commit racine porteur, `log.showRoot=false` en config locale | 0 ; avec `-c log.showRoot=true` : 1 | forcer la config |
| S5 | binaire marqué `-diff` | sans `--text` : 0 ; avec : 1 ; canonique `--tree` : 2 | `--text` requis |
| S6 | `textconv` qui vide le contenu | avec : 0 ; `--no-textconv` : 1 | `--no-textconv` requis |
| S7 | clone superficiel (profondeur 1) | `--is-shallow-repository` rend `true` ; flux 0 contre 1 sur le dépôt complet | refus, fail-closed |
| prototype | propre ; ajout-retrait ; lignes `++` ; UTF-16LE ; chemins du contrat ; `enforcementX/` ; superficiel ; branche non fusionnée ; notes de commit | 0 ; 2 `c.py:2` ; 2 `f.c:3` ; 2 `w.ps1:1` ; 0 ; 2 ; 2 (refus) ; 2 `c.py:1` ; 0 | attribution exacte par comptage des hunks ; `--all` couvre une branche hors de HEAD |

### 5.5 Références du canonique qui deviennent fausses dans Shōgen

- `ADR-0004` figure sur neuf lignes (l.2, 18, 28, 35, 53, 61, 62, 66, 71). Dans VibeGates, c'est l'ADR d'adjudication de l'escalade des gardes. Dans Shōgen, ADR-0004 est la décision multi-attestor (`docs/DECISIONS.md` l.8 et l.194) : chaque référence nue pointerait vers la mauvaise décision.
- `docs/passes/pass-4-report.md` (l.28) n'existe pas dans Shōgen.
- l.29-30 et l.103 : deux pourcentages attribués à Sakib et al., au niveau [abs] dans l'amont lui-même. Aucune entrée à `biblio/INDEX.md` ; l'identité complète manque au corpus, qui ne porte que la forme courte (amont, `docs/passes/pass-2-backlog.md` l.10). Pour Shōgen, ce sont des chiffres de seconde main (doc 03).
- l.20-21 : le contrat fait d'un scanner dédié en CI son filet, et l'ADR-0004 de VibeGates le maintient (l.17, l.25). Dans Shōgen, aucun job ne porte ce scanner, et la forge a le balayage des secrets, la protection des poussées et code security désactivés (git-ci l.26, P10 ; l.230, GC-10). Le filet annoncé est absent.
- Messages préfixés `VibeGates G3/G6` et `VibeGates R-23`. R-23 est une règle du corpus (doc 02 l.112 : paramètres de projet fixés par ADR sourcé), que Shōgen applique ; elle reste, sans le préfixe.

### 5.6 Environnement de l'oracle local

- git 2.55.0.windows.5 ; GNU bash 5.3.15 (cygwin) ; GNU grep 3.0 ; GNU Awk 5.4.1 ; GNU sed 4.9 ; GNU libiconv 1.19 (`/usr/bin/iconv`) ; Python 3.14.5 ; PyYAML 6.0.3 ; locale `C.UTF-8`.
- Config système : `core.autocrlf=true`, `init.defaultbranch=master`, `core.symlinks=false`. Aucune config globale parmi les clés relevées (`core.hooksPath`, `commit.gpgsign`, `log.showRoot`, `diff.noprefix`, `color.ui`, `diff.external`, `log.showSignature`).
- Variables `GIT_*` de l'environnement : `GIT_EDITOR` seule. `F:/tmp` n'est dans aucun dépôt (`rev-parse` échoue).
- `.vibegates-secretscan-exclude` et `enforcement/` : absents à `cf696bd` (`ls-tree`, 0 et 0).
- Image `ubuntu-24.04` : rien de mesuré (item 3).

### 5.7 Faits [lu] qui contraignent la conception (paraphrasés)

- **(a) actions/checkout au SHA épinglé `3d3c42e5…` (v7.0.1)** : `fetch-depth` vaut 1 par défaut ; la valeur 0 récupère tout l'historique de toutes les branches et de tous les tags. `persist-credentials` et `set-safe-directory` valent vrai par défaut.
- **(b) git-log 2.55** (`git-log-2.55.0.txt`) :
  - sans variante `--diff-merges`, une fusion ne montre pas de diff, même avec `--patch` (l.1989-1993) ; la valeur par défaut est `off` (l.2046) ; `first-parent` montre le diff complet contre le premier parent (l.2072) ;
  - `log.showRoot` est vrai par défaut et montre le commit racine comme une création (l.3397-3402) : c'est donc un réglage, qu'une config peut couper (S4) ;
  - `--text` (l.2827), `--no-ext-diff` (l.2888), `--no-textconv` (l.2894), `--no-notes` (l.1163-1165) ;
  - avec un chemin donné, le mode par défaut ne suit, pour une fusion identique à l'un de ses parents, que ce parent (l.712-718) ; `--full-history` suit toujours tous les parents (l.738-739) ;
  - `--all` prend toutes les refs de `refs/` plus HEAD (l.410-413) et, par défaut, examine tous les arbres de travail (l.481-486).
- **(c) git-rev-parse** : `--is-shallow-repository` imprime `true` ou `false` (l.345-347).
- **(d) git-cat-file** : avec `%(rest)`, la ligne d'entrée se coupe au premier blanc (l.359-362). Seule la mesure P2 s'en sert.

## 6. Choix tranchés (option retenue, motif, test)

- **CH-1 — Moteur canonique porté pour l'arbre et l'index.**
  - Boucle par fichier, contenu lu dans l'index (`git show :<chemin>`) comme des octets, NUL retirés, deux `grep` (VENDOR sensible à la casse, GENERIC insensible) ; motifs l.48-49 inchangés ; exclusions l.51-71 inchangées dans leur logique ; sortie masquée l.90-98.
  - Écarts nommés, et eux seuls : CH-5 à CH-9 et CH-14.
  - Motifs : D8 (source canonique) ; le moteur est la cinquième version, après quatre rejets en revue dans l'amont (l.26-28) ; aucune réécriture sans défaut mesuré (FM-2.3).
  - Tests : T-01 à T-30.
  - *Amendement daté du 2026-09-30 (correction de la revue G2, C-G2-1, C-G2-2, C-G2-8, C-G2-9)* : quatre écarts au blob s'ajoutent, chacun contre une sortie à tort en 0 ou une forme en clair mesurée par le G2 (A2, A3, A10, A12b) : type d'entrée lu par `git ls-files -s -- ":(literal)$f"`, un nom à caractère de glob n'étant plus pris pour une autre entrée ; `GIT_NO_REPLACE_OBJECTS=1` exporté (objets réels, ceux que la poussée transmet) ; `GIT_LITERAL_PATHSPECS`, `GIT_GLOB_PATHSPECS`, `GIT_NOGLOB_PATHSPECS` et `GIT_ICASE_PATHSPECS` retirées (pathspecs du contrat lues telles qu'écrites) ; fonction `masque` sur les chemins imprimés (CH-14). Tests : T-71, T-71b, T-72, T-73, T-77 à T-80. Les défauts corrigés par C-G2-1 et C-G2-8 sont ceux du blob amont : transmission à SHOGEN-D8-AMONT-ERRATUM-1 (Q-G2-4).
- **CH-2 — Mode `--history` : fonction neuve, un seul flux.**
  - Commande, drapeaux forcés : `git --no-optional-locks -c core.quotePath=false -c log.showRoot=true -c color.ui=never -c diff.noprefix=false -c diff.mnemonicPrefix=false -c diff.suppressBlankEmpty=false log -p --text --no-color --no-ext-diff --no-textconv --no-renames --diff-merges=first-parent --full-history --no-notes --no-show-signature --format='commit %H' --all -- . <exclusions>`.
  - Exclusions : celles du contrat (`enforcement/gate-*`, `enforcement/lint-*`, `enforcement/tests/`) et celles du fichier d'exclusion suivi, exactement comme en `--tree`, sous forme de pathspecs.
  - **Verdict** : NUL retirés du flux, puis lignes qui commencent par `+` ; une telle ligne qui répond à VENDOR ou à GENERIC (mêmes motifs, mêmes options) est un constat. Le verdict ne dépend que de `grep` : aucune analyse de diff n'y entre. C'est la leçon de l'amont, dont une version a été rejetée pour un analyseur de diff qui s'ouvrait (canonique l.26-28).
  - **Attribution**, pour le message seulement : un `awk` suit les lignes `commit <sha>`, les en-têtes `+++` hors hunk et les compteurs des en-têtes `@@`. Il imprime `<12 premiers caractères du commit>:<chemin>:<ligne>`, ou `(chemin)` pour une ligne d'en-tête. Une ligne vide dans un hunk compte comme contexte. Une erreur d'attribution ne change pas le verdict.
  - **Refus**, sortie 2 : dépôt superficiel (`rev-parse --is-shallow-repository` différent de `false`, jeton `SECRETS/tronque`) ; échec de `git log` ou de `mktemp` (`SECRETS/echec`).
  - Rejetées :
    - P2, blob par blob : environ 80 s pour le même verdict (§5.3) ;
    - une plage bornée, `origin/main..HEAD` : le rejeu de git-ci l.117 était une mesure ; une plage laisse hors portée ce qui est déjà poussé, alors que l'historique entier est la matière d'un passage public (ADR-0028 D10) ;
    - `git grep` sur des révisions : il relit chaque version, et il perd le retrait des NUL qui rend UTF-16 lisible ;
    - une révision en argument (`--history <rev>`) : voir CH-3.
  - Base de l'estimation : le prototype `proto-historique.sh`, 27 lignes [mesuré].
  - Tests : T-51 à T-67.
  - *Amendement daté du 2026-09-30 (correction de la revue G2, C-G2-3, C-G2-4, C-G2-5)* : deux refus précèdent le flux. Un fichier de greffes (chemin rendu par `git rev-parse --git-path info/grafts`, qui suit `GIT_GRAFT_FILE`) sort en `SECRETS/tronque` : l'historique affiché n'est pas celui des objets. Une ref dont l'objet pelé n'est pas un commit (blob ou arbre, directement ou par un tag) sort en `SECRETS/echec` : `git log --all` l'ignore en silence ; une ref de remplacement vers un blob en fait partie (mesuré, journal G1 §15). Drapeau forcé ajouté : `-c diff.dstPrefix=b/`, pour l'attribution contre la config locale. Jetons proposés par le G2, décision de forme Q-G2-1. Tests : T-74, T-74b, T-75, T-75b (tag annoté vers un commit, sortie 0 : ajouté à la re-revue rr1, 2026-10-01), T-65 (config hostile étendue).
- **CH-3 — Portée et bornes de l'historique.**
  - **Portée : `--all`**, sans argument de révision : toutes les refs de `refs/`, HEAD, et les HEAD de tous les arbres de travail (§5.7 b).
  - Motifs : largeur fail-closed ; un secret sur une ref poussée est dans le dépôt distant ; coût mesuré d'environ une seconde (§5.3) ; en CI, `fetch-depth: 0` récupère toutes les branches et tous les tags (§5.7 a).
  - Conséquence déclarée : un secret sur n'importe quelle ref récupérée rougit aussi le job de `main`. C'est voulu (Q-G0-2).
  - Dans un worktree de `F:/Shogen` (12 arbres de travail, arbre principal compris, `worktree list` mesuré), `--all` lit aussi les HEAD des lots en vol : O-3 y dépend de leur contenu, pas seulement de l'ascendance de D8b. Règle : un constat hors de l'ascendance du lot est rapporté à l'orchestrateur, avec commit et chemin masqués comme au CH-14 ; D8b ne le corrige pas, et ce rouge n'est pas un défaut de D8b. Mesure du G0 : 0 constat sur les 16 refs du clone (§5.3).
  - **Aucune borne de profondeur**, d'après la mesure du §5.3.
  - Bornes structurelles, déclarées et testées : dépôt superficiel refusé (T-59) ; liste des constats plafonnée à 20 lignes, compte total toujours imprimé (T-66) ; `timeout-minutes` du job (CH-13).
  - Hors portée déclarée : objets inatteignables, commits connus des seuls journaux de refs, bundles de custodie (item 5).
  - *Amendement daté du 2026-09-30 (cp-1 C-3)* : portée `--all` confirmée. Le journal G1 déclare, pour chaque exécution d'O-3, l'ensemble de refs couvert ; mesure du G1 (16:51Z, depuis le worktree et depuis l'arbre principal) : 17 refs (15 branches locales, 1 ref distante, 1 tag), 14 arbres de travail dont 5 à HEAD détaché, aucun `refs/stash`, 141 commits atteints, dont 134 dans l'ascendance de `40b4cfb` ; 0 constat.
  - *Amendement daté du 2026-09-30 (correction de la revue G2, C-G2-2 à C-G2-4)* : bornes structurelles ajoutées et testées : historique greffé refusé (T-74, T-74b), ref vers un blob ou un arbre refusée (T-75), tag annoté vers un commit accepté (T-75b, re-revue rr1), objets de remplacement ignorés (T-73). Sur `F:/Shogen`, sur le worktree et sur le clone du lot corrigé : aucun fichier de greffes, aucune ref de remplacement, toutes les refs vers des commits, 0 refus (journal G1 §15).
- **CH-4 — Valeurs formées à l'exécution, fixture tronquée.**
  - `enforcement/tests/fixtures/secrets/sondes.tsv` porte, par sonde : un identifiant, deux fragments de préfixe, un caractère de remplissage, une longueur, un suffixe et l'attendu.
  - Le runner forme la valeur (fragments, caractère répété, suffixe) dans un dépôt jetable. Aucun fragment ne répond seul aux motifs, aucune ligne de la fixture non plus (O-6). La forme complète n'existe qu'à l'exécution.
  - Caractères de remplissage neutres : aucune valeur d'exemple publiée par un fournisseur.
  - Couverture par alternative : pour chacune des 10 alternatives de VENDOR, et pour chaque forme de GENERIC (citée ou non, par mot-clé), une sonde positive à la longueur minimale exacte (attendu 2), et une sonde juste en dessous ou une quasi-forme (attendu 0). Motif : doc 02 l.47, un test qui ne tue pas de mutants ne prouve rien ; chaque alternative retirée du motif doit faire rougir une sonde.
  - Motifs du choix : mesure du §5.2 ; mission (fixture sous `enforcement/tests/`, jamais un format qui déclenche un scanner tiers).
  - Tests : T-31 et T-32 (table) ; invariant O-6.
  - *Amendement daté du 2026-09-30 (correction de la revue G2, C-G2-6, C-G2-7, C-G2-10)* : la couverture s'étend aux mots-clés de la forme non citée de GENERIC (G-13 à G-16), à la longueur minimale exacte de deux alternatives (V-21 : en-tête PEM sans mot entre BEGIN et PRIVATE ; G-17 : clé `aws_` suivie aussitôt de `key`) et aux cinq membres de la classe du jeton `xox` (V-22 à V-25, avec V-11). Sans ces sondes, sept mutants de motif survivaient (N-1 à N-4, N-7, N-8, N-9). Fixture : 45 sondes.
- **CH-5 — Références et chiffres.**
  - `ADR-0004` devient partout « ADR-0004 de VibeGates », avec le chemin amont ; jamais une référence nue.
  - `pass-4-report.md` devient la référence amont complète (VibeGates, `docs/passes/pass-4-report.md`, section U2, commit `1263f2a`).
  - Les deux pourcentages des l.29-30 et l.103 sont retirés, avec leur mention de source : ce sont des chiffres de seconde main (doc 03), et le gate n'en a pas besoin pour fonctionner. Une réintroduction exige d'abord un procurement formé (Q-G0-4).
  - l.20-21 réécrites : aucun scanner dédié dans Shōgen à ce jour, items 1 et 2 ; le plancher ne se présente pas comme un filet.
  - En-tête : provenance (blob `6789a30`, soit VibeGates `1eb1b33`, HEAD amont `1263f2a` ; runner conçu d'après `7960238`), ADR-0028 D8, ce G0.
  - *Amendement daté du 2026-09-30 (cp-1 C-5)* : retrait des deux pourcentages [abs] accepté ; aucun procurement dû tant qu'ils ne sont réintroduits nulle part ; toute réintroduction exige d'abord une demande de procurement formée (Sakib et al., identité bibliographique complète à établir).
- **CH-6 — Messages et jetons.**
  - Messages en français, jetons ASCII sur stderr (précédent : CH-3 du G0 de D8a) :
    - `SECRETS/forme` : contenu en forme d'identifiant dans l'arbre ou dans l'index ;
    - `SECRETS/historique` : idem dans l'historique ;
    - `SECRETS/exclusion` : entrée du fichier d'exclusion refusée (sans marqueur `ADR-`, globale, traversante, portée entière, fichier non suivi, pathspec inutilisable) ;
    - `SECRETS/tronque` : historique superficiel ;
    - `SECRETS/echec` : le balayage ne peut pas tourner (hors dépôt, erreur git, `mktemp`, argument inconnu).
  - Avis `AVIS (secrets)` : exclusions du contrat, exclusions appliquées avec leur compte, entrées non-blob ignorées (parité d'avis de l'ADR-0004 de VibeGates, l.16 pt a).
  - Succès sur stdout : `OK (secrets) : <n> fichier(s)` pour l'arbre et l'index ; `OK (secrets) : historique, <n> commit(s) (--all)`.
  - Codes 0 et 2, comme le canonique. Le jeton ne change pas le verdict.
  - Le runner vérifie **la sortie ET le jeton** de chaque cas ; un cas attendu à 0 exige aussi le message OK.
  - *Amendement daté du 2026-09-30 (correction de la revue G2, C-G2-3, C-G2-4 ; Q-G2-1 ouverte)* : `SECRETS/tronque` couvre l'historique superficiel ou greffé ; `SECRETS/echec` couvre aussi une ref vers un blob ou un arbre.
- **CH-7 — Arguments.** Sans argument (index), `--tree` ou `--history`. Tout autre argument, ou plus d'un, sort en 2 avec `SECRETS/echec`.
  - Écart au canonique (l.40, l.76-80), où un argument inconnu retombe sur le mode indexé. Une faute de frappe dans l'étape `--history` du job y passerait en vert, faute de contenu indexé en CI.
  - Test : T-14.
- **CH-8 — `LC_ALL=C` exporté en tête du gate.**
  - Motif : même comportement de `grep` et d'`awk` sous la locale de Git Bash (`C.UTF-8`, grep 3.0) et sous celle de l'image ; plages et `-i` en ASCII ; octets traités comme des octets.
  - Condition : le G1 rejoue les cas portés sous la locale ambiante et sous `C`. Toute divergence arrête le lot (consultation R-26).
  - Mutant attendu équivalent sur les cas du §7 : à mesurer au G1, et à déclarer s'il survit.
- **CH-9 — Fichier d'exclusion.** Nom `.vibegates-secretscan-exclude` gardé (canonique ; gabarit du corpus), absent de Shōgen (§5.6). Règles inchangées : fichier suivi, marqueur `ADR-` (marqueur d'attribution, non contrôlé comme référence), refus des formes globales, traversantes ou qui retirent toute la portée, avis avec le compte retiré. Il s'applique aussi à l'historique (CH-2). Tests : T-20 à T-30 et T-67.
  - *Amendement daté du 2026-09-30 (cp-1 C-6)* : nom `.vibegates-secretscan-exclude` gardé (canonique, gabarit du corpus).
- **CH-10 — Mode indexé.** Gardé, comme défaut du canonique. Son consommateur est le hook de D8c, absent aujourd'hui (item 4). Il est testé dès D8b-1 : les cas amont tournent en mode indexé.
- **CH-11 — Coût de `--tree`.** Boucle par fichier gardée : 84,8 s en local (§5.3). Pas de réécriture dans D8b : fidélité au moteur revu dans l'amont ; le coût sur l'image Linux est inféré plus bas, et l'item 3 le mesure. Le G1 fixe `timeout-minutes` d'après ses mesures ; 15 est proposé.
- **CH-12 — Runner.**
  - Nom `enforcement/tests/run-fixtures-secrets.sh` (forme de D8a). Chemin du gate en `$1` (mutants, O-5), par défaut `../gate-secrets.sh` relatif au runner.
  - Isolation (TEST-GIT-ENV-ISOLATION-1, incidents du 2026-09-24) :
    1. refus, sortie 3, si l'une de `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE`, `GIT_OBJECT_DIRECTORY`, `GIT_COMMON_DIR`, `GIT_NAMESPACE` ou `GIT_ALTERNATE_OBJECT_DIRECTORIES` est posée ;
    2. dossier de travail `mktemp -d`, contrôlé hors de tout dépôt (`rev-parse --is-inside-work-tree` doit échouer) ;
    3. chaque dépôt jetable : `git init -q -b main`, puis `rev-parse --show-prefix` vide ; config locale `user.name`, `user.email` en `example.invalid`, `commit.gpgsign=false`, `core.autocrlf=false`, `core.hooksPath` vers un dossier vide ;
    4. toute commande git du runner porte `-C <dépôt jetable>`, et le gate se lance depuis ce dépôt ;
    5. jamais `--no-verify` (garde R-22) : les crochets sont neutralisés par `core.hooksPath`.
  - **R-20** : les `git commit` du runner n'ont lieu que dans ces dépôts jetables, hors de tout dépôt ; ce ne sont pas des commits du projet. Le commit d'empilement du worktree du G1 relève d'une autre clause de la mission.
  - **Test de la garde** : par `GIT_NAMESPACE` seule, sans effet si la garde échouait (O-11). `GIT_DIR` et `GIT_WORK_TREE` ne sont jamais posées, même pour un test (règle du 2026-09-25) : leur présence dans la liste se contrôle par lecture au G2.
  - `iconv` est requis (T-06, T-61) : son absence est un échec, jamais un saut.
  - Sortie : 0 si tout passe, 1 si un cas échoue, 3 en erreur fatale. Un seul résumé fait foi : `secrets : <n> ok, <m> échec`.
  - *Amendement daté du 2026-09-30 (G1)* : la fonction de cas vérifie, en plus de la sortie et du jeton, un motif requis ou un motif interdit quand le jeton seul ne tranche pas : sans lui, M-17 et M-18 seraient équivalents (le blob double le contrôle hors dépôt par la résolution de la racine, et l'échec de `mktemp` par l'échec de la redirection). Le motif requis de T-15 est le message de la gate (`mktemp a échoué`) : le message d'erreur de `mktemp` lui-même contient le mot `mktemp` (mesuré : M-17 a survécu à la première campagne de D8b-2 ; journal G1, E-2).
  - *Amendement daté du 2026-09-30 (correction de la revue G2)* : deux cas posent une variable pour le seul appel de la gate, en préfixe de la fonction de cas, jamais dans l'environnement du runner : `GIT_ICASE_PATHSPECS=1` (T-78) et `GIT_GRAFT_FILE` vers un fichier du dossier de travail jetable (T-74b). Aucune n'est une variable de la garde (point 1) ; `GIT_DIR` et `GIT_WORK_TREE` ne sont jamais posées. T-72, T-73, T-75 et T-75b écrivent objets, remplacements et tags dans le dépôt jetable ; T-74 écrit un fichier de greffes sous son `.git/info/`, créé s'il manque. Table exécutée : 113 cas (T-75b depuis la re-revue rr1, 2026-10-01).
- **CH-13 — Job g3.**
  - id = name = `g3-secrets` (règle d'un seul nom, `gates.yml` l.60 à `cf696bd`) ;
  - `runs-on: ubuntu-24.04` (SHOGEN-CI-RUNNERS-1, annexe B l.80) ;
  - `actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # tag v7.0.1`, avec `persist-credentials: false` ; `fetch-depth: 0` en D8b-3 (sans lui, l'historique n'a qu'un commit et le gate refuse, §5.7 a et CH-3) ;
  - `shell: bash` ; `timeout-minutes` fixé par le G1 (CH-11) ;
  - étapes : (1) `bash enforcement/tests/run-fixtures-secrets.sh` ; (2) `bash enforcement/gate-secrets.sh --tree` ; (3) `bash enforcement/gate-secrets.sh --history` (D8b-3) ;
  - position après `g1-model-pinning` ; aucune action ni installation neuve (R-8) ;
  - en-tête : G3 secrets nommé (l.3-7 de l'état après D8a) ; item SHOGEN-G3-FORGE-1 ajouté aux l.19-20.
- **CH-14 — Sortie masquée.** Le gate n'imprime que le chemin et la ligne qu'il calcule lui-même, jamais un octet de la valeur (canonique l.24-25). En historique, le commit s'y ajoute. Tests T-07 et T-52 : aucun fragment de la valeur formée dans la sortie.
  - *Amendement daté du 2026-09-30 (correction de la revue G2, C-G2-8)* : un chemin qui a lui-même la forme d'un identifiant était imprimé en clair dans les trois modes (A10). Fonction `masque` (`sed -E`, mêmes motifs, GENERIC sans casse) sur l'attribution d'historique, l'avis non-blob, les lignes `chemin:ligne` et la ligne de reste. Tests : T-76 (historique), T-77 (index, forme vendeur), T-79 (avis non-blob) et T-80 (index, forme générique en majuscules), ces deux derniers ajoutés par le correcteur. Restent en clair les messages du contrat d'exclusion et les messages d'échec : item SHOGEN-SECRETS-MASQUE-EXCLUSION-1 (I-G2-4, étendu par le correcteur au message d'échec de `git show` et au chemin des greffes).
- **CH-15 — Constat réel, et pièces de D.2.**
  - Remède du canonique : révoquer la valeur, car la retirer ne suffit pas.
  - Dans Shōgen, D7 interdit toute réécriture d'historique (ADR-0028 l.211) : un constat réel dans l'historique ne se purge pas. La seule issue du canonique serait une exclusion par chemin, qui ouvrirait ce chemin pour toujours, arbre compris. Item 6 : une liste de constats révoqués, par commit, chemin et empreinte de ligne, sous ADR.
  - Le gate balaie les fichiers suivis et leur historique, dont `docs/rapports/cartographie-2026-09-29.md` et ADR-0025 (annexe D l.35-36). Ce balayage est mécanique et n'affiche aucune ligne. Si une ligne signalée tombe dans une pièce de D.2, elle s'identifie par son sha256 et n'est jamais affichée, même pour l'inspecter.
- **CH-16 — Ce que D8b ne revendique pas.**
  - Un plancher de motifs : ni entropie, ni secret coupé sur deux lignes, ni format nouveau (canonique l.19-21).
  - Ni un scanner dédié, ni le balayage de la forge.
  - Ni les objets hors refs.
  - Le vert du job ne dit que l'absence de ces formes dans la portée déclarée.
  - Limites avec items : 1, 2, 5 et 6.
  - *Amendement daté du 2026-09-30 (correction de la revue G2)* : limites neuves, avec items (journal G1 §15) : chemins `<0-3>:<reste>` lus comme une entrée d'étage (I-G2-1) ; statut de `grep` confondu (I-G2-2, recherche) ; noms de chemin non balayés en modes arbre et indexé (I-G2-3, extension de l'item 4) ; messages d'exclusion et d'échec non masqués (I-G2-4).

## 7. Table des cas (contrat du runner ; sortie attendue, jeton)

Notation : V = valeur de forme vendeur, G = affectation de forme générique ; toutes deux formées à l'exécution (CH-4). « index » = gate sans argument, sur un fichier ajouté à l'index d'un dépôt jetable. « amont n » = n-ième cas `SEC` du runner amont.

| id | arbre et geste | attendu | origine | sous-lot |
|---|---|---|---|---|
| T-01 | index : fichier portant V | 2 `SECRETS/forme` | amont 1 | D8b-1 |
| T-02 | index : G, mot-clé en majuscules, valeur citée | 2 `SECRETS/forme` | amont 2 | D8b-1 |
| T-03 | index : préfixe vendeur en minuscules | 0 | amont 3 | D8b-1 |
| T-04 | index : fichier propre | 0, message OK | amont 4 | D8b-1 |
| T-05 | index : octet NUL, puis V dans le même fichier | 2 | amont 5 | D8b-1 |
| T-06 | index : V en UTF-16LE (`iconv`) | 2 | amont 6 | D8b-1 |
| T-07 | index : G dans `résumé.py` ; sortie avec chemin et masque, sans aucun fragment de la valeur | 2 | amont 7 | D8b-1 |
| T-08 | index : lignes `++i;` et `++ b/HIJACK.txt`, puis G en l.3 ; attribution `f.c:3:`, aucun `HIJACK` | 2 | amont 8 | D8b-1 |
| T-09 | index, gate lancé depuis un sous-dossier | 2 | amont 9 | D8b-1 |
| T-10 | `--tree`, lancé depuis un sous-dossier | 2 | amont 10 | D8b-1 |
| T-11 | gitlink (mode 160000) : ignoré avec avis | 0, avis | amont 11 | D8b-1 |
| T-12 | lien symbolique (mode 120000, par `update-index --cacheinfo`) : ignoré avec avis | 0, avis | neuf (l.18-19) | D8b-1 |
| T-13 | gate lancé hors de tout dépôt | 2 `SECRETS/echec` | neuf (l.44) | D8b-1 |
| T-14 | dépôt propre, argument inconnu (`--hstory`) ; le canonique rend 0 | 2 `SECRETS/echec` | neuf (CH-7) | D8b-1 |
| T-15 | `TMPDIR` inexistant | 2 `SECRETS/echec` | amont 15 | D8b-2 |
| T-16 | 12 lignes G dans un fichier : troncature annoncée | 2, mention du reste | amont 16 | D8b-2 |
| T-17 | fichier commité avec V en l.1, modification indexée de la l.5 : le mode indexé lit le fichier entier | 2 | neuf (l.6-7) | D8b-2 |
| T-18 | suppression indexée d'un fichier porteur de V : les retraits ne sont pas balayés (T-52 les voit dans l'historique) | 0 | neuf (l.7) | D8b-2 |
| T-19 | affectation non citée, forme dotenv | 2 | amont 23 | D8b-2 |
| T-20 | pathspec d'exclusion inutilisable (`../out` avec marqueur) | 2 `SECRETS/exclusion` | amont 12 | D8b-2 |
| T-21 | ligne d'exclusion sans marqueur `ADR-` | 2 `SECRETS/exclusion` | amont 13 | D8b-2 |
| T-22 | exclusion de `fx/` avec marqueur, V sous `fx/` | 0 | amont 14 | D8b-2 |
| T-23 | V sous `enforcement/tests/` : exclusions du contrat annoncées | 0, avis | amont 17 | D8b-2 |
| T-24 | V sous `enforcementX/` | 2 | amont 18 | D8b-2 |
| T-25 | fichier d'exclusion non suivi | 2 `SECRETS/exclusion` | amont 19 | D8b-2 |
| T-26 | pathspec global `.` | 2 `SECRETS/exclusion` | amont 20 | D8b-2 |
| T-27 | exclusion appliquée : avis avec le compte (1 fichier) | 0, compte | amont 21 | D8b-2 |
| T-28 | équivalent global `.//` | 2 `SECRETS/exclusion` | amont 22 | D8b-2 |
| T-29 | V sous `enforcement/policies/` : le reste d'`enforcement/` est balayé | 2 | amont 24 | D8b-2 |
| T-30 | (a) traversée parente ; (b) exclusion qui retire toute la portée | 2 `SECRETS/exclusion`, deux fois | neuf (l.62, l.66) | D8b-2 |
| T-31 | table VENDOR, V-01 à V-20 : 10 alternatives, chacune positive et sous le seuil | 2 puis 0, par alternative | neuf (CH-4) | D8b-2 |
| T-32 | table GENERIC, G-01 à G-12 : forme citée (7 mots-clés, `:` et `=`), forme non citée (mot-clé, clé de type `aws_…key…`), une sonde sous le seuil par forme | 2 ou 0 selon la ligne | neuf (CH-4) | D8b-2 |
| T-51 | historique propre (`--all`) | 0, OK avec compte de commits | neuf | D8b-3 |
| T-52 | `résumé.py` : V ajoutée en l.2 puis retirée ; `--tree` rend 0 ; `--history` rend 2 avec `<commit>:résumé.py:2`, sans fragment de la valeur | 0 puis 2 `SECRETS/historique` | S1 | D8b-3 |
| T-53 | fichier de 5 lignes, puis modification de sa l.4 qui y met G : attribution `:4` (lignes de contexte comptées) | 2 | neuf | D8b-3 |
| T-54 | fusion qui introduit seule G (résolution) | 2 | S2 | D8b-3 |
| T-55 | branche latérale ajout puis retrait, fusion identique au premier parent | 2 | S3 | D8b-3 |
| T-56 | commit racine porteur, `log.showRoot=false` en config locale | 2 | S4 | D8b-3 |
| T-57 | binaire marqué `-diff`, V après un NUL | 2 | S5 | D8b-3 |
| T-58 | `textconv` qui vide le contenu | 2 | S6 | D8b-3 |
| T-59 | clone superficiel (`--depth 1` par `file://`) | 2 `SECRETS/tronque` | S7 | D8b-3 |
| T-60 | lignes `++` avant G, dans l'historique : attribution `f.c:3` | 2 | prototype | D8b-3 |
| T-61 | V en UTF-16LE, ajoutée puis retirée | 2 | prototype | D8b-3 |
| T-62 | V sous `enforcement/tests/` dans l'historique, puis sous `enforcementX/` | 0 puis 2 | prototype | D8b-3 |
| T-63 | V sur une branche non fusionnée, hors de l'ascendance de HEAD | 2 | prototype (`--all`) | D8b-3 |
| T-64 | note de commit portant des lignes `+…` et `commit …` : verdict et attribution de T-52 inchangés | 0 ; puis 2 identique à T-52 | prototype | D8b-3 |
| T-65 | config locale hostile (`color.ui=always`, `diff.noprefix=true`, `diff.suppressBlankEmpty=true`, `core.quotePath=true`) : T-52 rejoué | 2, même attribution | neuf (drapeaux forcés) | D8b-3 |
| T-66 | 25 lignes G dans l'historique : 20 constats listés, compte total 25 | 2 | neuf (CH-3) | D8b-3 |
| T-67 | exclusion de `fx/` avec marqueur, appliquée à l'historique | 0, avis | neuf (CH-9) | D8b-3 |

Chaque cas vérifie la sortie ET le jeton. La table T-31 et T-32 compte une ligne par sonde : 32 cas. Total : 14 cas en D8b-1, 48 en D8b-2, 17 en D8b-3, soit 79. Les numéros T-33 à T-50 sont laissés libres pour des sondes que le G1 ajouterait (une ligne de fixture chacune).

- *Amendement daté du 2026-09-30 (cp-1 C-7 ; G1)* : T-59 construit le clone superficiel par `git -C <dossier jetable> clone --no-local --depth 1 <chemin>`, et non par une URL `file://` : documentation de git 2.55 (page git-clone : `--no-local` emploie le transport git ordinaire pour un chemin local ; `--depth` fait un clone superficiel ; extrait `F:/tmp/shogen-lots/D8b/oracles/git-clone-2.55.0.txt` l.53-59 et l.310-316) et sonde `F:/tmp/shogen-lots/D8b/oracles/sonde-superficiel.out` (rc 0 et `--is-shallow-repository` = `true` sous `TMPDIR=F:/…` comme sous `TMPDIR=/f/…` ; l'URL `file:///$W` rend 128 sous la forme POSIX, le constat du cp-1). Tout échec de construction d'une fixture sort en 3. O-1 est rejoué sous les deux formes de `TMPDIR`.
- *Amendement daté du 2026-09-30 (G1)* : cas ajoutés ou scindés. T-30 devient T-30a et T-30b. T-33 à T-35 : sondes de seuil (second `{20,}` de l'alternative `sk-…T3BlbkFJ…` ; premier et second segments `+` de l'alternative `eyJ…`), une ligne de fixture chacune. T-52a : `--tree` du dépôt de T-52. T-62a et T-62b, T-64a et T-64b, T-66b (vingtième ligne listée). T-68 : pathspec absolue avec marqueur, seule entrée de la branche « inutilisable » (T-20, `../out`, est intercepté par la branche « traversant », qui précède dans le blob, l.62-63). T-69 : objet manquant dans un dépôt jetable, échec de `git log` ; tueur du retrait de `pipefail`. T-70 : ligne vide de contexte sous `diff.suppressBlankEmpty=true`. T-65 porte son fichier sous `b/` : le retrait de `-c diff.noprefix=false` change alors l'attribution (tueur de M-36c). T-51 porte une quasi-forme en minuscules (tueur de M-7h) et T-53 un mot-clé en majuscules (tueur de M-6h). T-20 et T-21 suivent le fichier d'exclusion : dans l'amont, les cas 12 et 13 le laissaient non suivi et touchaient la branche « non suivi ». Table exécutée : 90 cas (14 en D8b-1, 53 en D8b-2, 23 en D8b-3).
- *Amendement daté du 2026-09-30 (correction de la revue G2)* : cas ajoutés. D8b-2 : T-71 et T-71b (entrée régulière `[A]x.py` portant V et lien `Ax.py`, index et `--tree`, C-G2-1) ; T-72 (`--tree`, blob porteur remplacé, C-G2-2) ; T-77 (index, fichier nommé V, C-G2-8) ; T-78 (`--tree`, `GIT_ICASE_PATHSPECS=1`, `Enforcement/Tests/x.py` portant V, C-G2-9) ; T-79 (index, lien nommé V : avis masqué) et T-80 (index, fichier nommé d'après une forme générique en majuscules), ajoutés par le correcteur ; dix sondes (C-G2-6, C-G2-7, C-G2-10). D8b-3 : T-73 (commit porteur remplacé) ; T-74 (greffe) ; T-74b (greffe par `GIT_GRAFT_FILE`, ajout du correcteur) ; T-75 (tag léger vers un blob porteur) ; T-76 (fichier nommé V, ajouté puis retiré) ; T-75b (tag annoté vers un commit, sortie 0 et `historique, 1 commit(s)` : sens ouvert de C-G2-4, ajouté à la re-revue rr1 du 2026-10-01, tueur du mutant R4b) ; T-65 ajoute `diff.dstPrefix=zz/` à sa config hostile (C-G2-5). Table exécutée : 113 cas (14 en D8b-1, 70 en D8b-2, 29 en D8b-3).

## 8. Oracles non-LLM nommés

- **O-1 — Runner.** `TMPDIR=F:/tmp/shogen-tests-tmp/<frais> bash enforcement/tests/run-fixtures-secrets.sh` → sortie 0, `secrets : <n> ok, 0 échec`, où n est le nombre de cas du §7 retenus dans le (sous-)lot.
  - *Amendement daté du 2026-09-30 (cp-1 C-7)* : O-1 est lancé deux fois, `TMPDIR` en forme Windows (`F:/…`) puis POSIX (`/f/…`).
  - *Amendement daté du 2026-09-30 (correction de la revue G2)* : état corrigé, `secrets : 113 ok, 0 échec` sous les deux formes de `TMPDIR` (T-75b compris, re-revue rr1, 2026-10-01) ; runner corrigé lancé avec la gate du lot : 100 ok, 13 échecs, exactement les cas qui visent un défaut de la gate du lot (T-65, T-71, T-71b, T-72 à T-80, T-74b ; T-75b y passe ; journal G1 §15).
- **O-2 — Arbre réel, sonde négative** (rejeu de git-ci §2.b l.116). À la racine du worktree : `bash enforcement/gate-secrets.sh --tree` → sortie 0, message OK et compte de fichiers. L'orchestrateur le rejoue sur l'arbre de travail principal.
  - *Amendement daté du 2026-09-30 (G1)* : dans un worktree, les fichiers neufs du lot sont absents de l'index avant `git add -N`, et y sont lus vides après (`F:/tmp/shogen-lots/D8b/oracles/sonde-ita.out`) : O-2 y balaie donc la base (302 fichiers). Les fichiers du lot entrent au balayage dans le clone d'O-4, où le lot est committé (k=0).
- **O-3 — Historique réel, sonde négative.** `bash enforcement/gate-secrets.sh --history` → sortie 0, OK avec le compte de commits (128 dans le clone du G0, §5.3 ; le compte suit les refs présentes). Même commande que l'étape 3 du job.
- **O-4 — Rouge semé sur l'entrée réelle** (CA-11 durci).
  - Préparation : `git clone --shared` de `F:/Shogen` vers `F:/tmp/shogen-lots/D8b/oracles/rouge/`, puis `checkout --detach <sha du lot>` dans ce clone (geste du clone du G0) ; rien n'est écrit dans `F:/Shogen`.
  - Dans le clone : (k=1) un fichier portant V formée à l'exécution, ajouté à l'index → mode indexé 2 `SECRETS/forme` ; (k=2) commit C1 qui l'ajoute, commit C2 qui le retire → `--tree` 0, `--history` 2 avec `<C1>:<chemin>:<ligne>` ; (k=3) fichier d'exclusion suivi dont une ligne n'a pas de marqueur → 2 `SECRETS/exclusion`.
  - La composition part de l'historique réel committé, jamais d'une forme reconstruite à la main.
- **O-5 — Mutants de gate** (tests négatifs d'outil ; registre d'ADR-0011 pt 4, `docs/09-vocabulaire.md` l.41). Copies du gate sous `F:/tmp/shogen-lots/D8b/oracles/`, runner lancé avec le chemin du mutant en `$1`. Chaque mutant doit faire sortir le runner en ≠ 0, cas tueur nommé en rouge. Le script de mutation vit hors du dépôt.

  | mutant | tué par |
  |---|---|
  | M-1 verdict neutralisé (constat jamais levé) | T-01 et tous les positifs |
  | M-2 retrait des NUL supprimé (index, arbre) | T-05, T-06 |
  | M-3.k (k = 1 à 10) alternative k de VENDOR retirée | sonde positive de l'alternative k (T-31) |
  | M-4 forme citée de GENERIC retirée | T-02, T-32 |
  | M-5 forme non citée de GENERIC retirée | T-19, T-32 |
  | M-6 GENERIC sans `-i` | T-02 |
  | M-7 VENDOR avec `-i` | T-03 |
  | M-8 un seuil de longueur abaissé d'une unité | sonde sous le seuil de l'alternative (T-31, T-32) |
  | M-9 exclusion du contrat élargie à tout `enforcement/` | T-29 |
  | M-10 contrôle du marqueur `ADR-` retiré | T-21 |
  | M-11 fichier d'exclusion non suivi accepté | T-25 |
  | M-12 contrôle de la forme globale retiré | T-26 |
  | M-13 normalisation des `//` retirée | T-28 |
  | M-14 contrôle de traversée retiré | T-30 (a) |
  | M-15 contrôle de portée entière retiré | T-30 (b) |
  | M-16 avis de saut non-blob retiré | T-11, T-12 |
  | M-17 échec de `mktemp` ignoré | T-15 |
  | M-18 contrôle hors dépôt retiré | T-13 |
  | M-19 argument inconnu ramené au mode indexé (comportement canonique) | T-14 |
  | M-20 annonce de troncature retirée | T-16 |
  | M-21 `--diff-filter=d` retiré | T-18 |
  | M-22 le mode indexé lit les lignes du diff au lieu du contenu entier | T-17 |
  | M-23 `--diff-merges=first-parent` retiré | T-54 |
  | M-24 `--full-history` retiré | **équivalent mesuré sur git 2.55** : S3 bis montre que `--diff-merges=first-parent` seul parcourt la branche latérale ; rejeu `bash g0-mesures/mesure-s3bis.sh` ; survivant déclaré, pas un trou de tests |
  | M-25 M-23 et M-24 ensemble | T-55 |
  | M-26 `-c log.showRoot=true` retiré | T-56 |
  | M-27 `--text` retiré | T-57 |
  | M-28 `--no-textconv` retiré | T-58 |
  | M-29 refus du dépôt superficiel retiré | T-59 |
  | M-30 `--all` remplacé par `HEAD` | T-63 |
  | M-31 `-c color.ui=never` et `--no-color` retirés ensemble | T-65 |
  | M-32 `-c core.quotePath=false` retiré | T-52 (chemin non ASCII), T-65 |
  | M-33 compteur de contexte de l'`awk` retiré | T-53 |
  | M-34 plafond, ou compte total, retiré | T-66 |
  | M-35 exclusions du fichier non appliquées à l'historique | T-67 |
  | M-36 `--no-notes`, `-c diff.suppressBlankEmpty=false`, `-c diff.noprefix=false` ou `LC_ALL=C` retirés un à un | équivalence attendue (chacun est doublé par l'`awk` ou par le format) : mesurée au G1, chaque survivant déclaré avec sa commande de rejeu |

  F2P : le runner et le gate sont absents de la base ; tous les tests sont neufs (catégorie « nouveau module »), à déclarer comme tels.
- *Amendement daté du 2026-09-30 (cp-1 C-8 ; G1)* : le script de mutation, hors dépôt, est cité au journal G1 par chemin et sha256, avec la commande exacte par mutant ; M-24 est re-mesuré sur la gate du lot. Mutants ajoutés par le G1 : M-8 par seuil (M-8.1 à M-8.10c, M-8.g1, M-8.g2), sites du mode `--history` (M-1h, M-2h, M-6h, M-7h), M-34a et M-34b, M-36a à M-36f, M-37 (branche « inutilisable »), M-38 (`--no-renames`), M-39 (garde hors hunk de l'en-tête `+++`), M-40 (ligne vide de contexte), M-41 (`pipefail`). Résultats : journal G1 §5.
- *Amendement daté du 2026-09-30 (correction de la revue G2)* : campagne rejouée sur la gate corrigée : les 74 mutants du G1 (M-16 et M-41 redérivés, leur ancre ayant changé), les retours K-1 à K-7 et les mutants de motif N-1 à N-9, N-8a, N-8p, N-8r et N-8s du G2, et cinq retours de sous-site du correcteur (K-3b, K-6c à K-6f), soit 98 mutants ; résultats au journal G1 §15. Re-revue rr1 (2026-10-01) : le mutant R4b (alternative `tag commit` retirée du contrôle des refs), qui survivait au runner à 112 cas, est tué par T-75b ; journal G1 §15.
- **O-6 — Invariant de littéral.** Les deux motifs du gate du lot, évalués depuis ses propres lignes d'affectation, sous `LC_ALL=C`, appliqués à chaque fichier ajouté ou modifié par le lot (dont la fixture, le runner, `gates.yml`, le journal G1 et la copie de ce G0) → 0 ligne. Ce contrôle a été appliqué à ce document avant sa remise (§15).
- **O-7 — Compatibilité g5.** Le motif courant (`gates.yml` l.48 à `cf696bd`) et le motif élargi que portera D8c (`adb2213:gates.yml` l.39) rendent 0 occurrence dans les lignes ajoutées sous `enforcement/` et dans le diff de `gates.yml`.
- **O-8 — Non-régression.** `cargo --locked xtask verify` VERT, qui couvre le journal G1 et la copie du G0 (S-G4, S-G5) ; `(cd s2-harness && python -B -m unittest discover -s tests -t .)` : compte et sauts identiques à la base, mesurés avant et après (D8b ne touche pas `s2-harness/`). Environnement : `CARGO_HOME` et `CARGO_NET_OFFLINE=true` de la mission, `TMPDIR` sous `F:/tmp/shogen-tests-tmp`.
- **O-9 — TMP.** 0 entrée neuve dans un TMP frais après O-1 et O-3, par comptes avant et après.
- **O-10 — Structure de `gates.yml`.** Lecture par `yaml.safe_load` (PyYAML 6.0.3 déjà présent, aucune installation, R-8 ; précédent `F:/tmp/shogen-lots/D8a/oracles/o10.py`), comparée à l'état après D8a : clés de premier niveau inchangées ; un seul job neuf, `g3-secrets` ; jobs de la base inchangés ; `name` = identifiant ; `runs-on` = `ubuntu-24.04` ; checkout au SHA `3d3c42e5…` avec `persist-credentials: false` et, en D8b-3, `fetch-depth: 0` ; étapes et commandes exactes du CH-13 ; aucun `continue-on-error` ; ordre g5, g1, g3, s2.
- **O-11 — Garde d'isolation du runner.** `GIT_NAMESPACE=d8b-garde bash enforcement/tests/run-fixtures-secrets.sh` → sortie 3, aucun dossier temporaire créé (comptes avant et après). `GIT_DIR` et `GIT_WORK_TREE` ne sont jamais posées (règle du 2026-09-25).
- **O-12 — Temps.** Temps de O-1, O-2 et O-3 sur le worktree, relevés pour fixer `timeout-minutes`.
- **Enregistrement.** Le G1, puis le G2 par ses propres commandes, produisent un enregistrement d'oracle substitut, au format de CI-S2 (annexe B l.79) et avec les champs de D6 (viii) : `F:/tmp/shogen-lots/D8b/oracles/oracle-<rôle>-D8b-substitut.json` (commandes, sorties, sha256, codes de sortie).

## 9. Estimation R-25 (ascendante, par fichier ; [inféré] sauf mention)

| fichier | D8b-1 | D8b-2 | D8b-3 | base de l'estimation |
|---|---|---|---|---|
| `enforcement/gate-secrets.sh` | ≈ 104 | 0 | ≈ +36 | canonique 107 [mesuré] : en-tête de 37 lignes réécrit en ≈ 32, code de 70 lignes porté en ≈ 72 (`LC_ALL=C`, contrôle d'argument) ; historique : prototype de 27 lignes [mesuré] plus ≈ 9 (exclusions partagées, messages, en-tête) |
| `enforcement/tests/run-fixtures-secrets.sh` | ≈ 82 | ≈ +58 | ≈ +56 | squelette ≈ 40 (aides amont l.17-33, soit 17 lignes [mesuré] ; garde d'isolation ≈ 8 ; formation des valeurs ≈ 6 ; en-tête ≈ 5 ; résumé ≈ 4) ; ≈ 3 lignes par cas (D8a : runner de 137 lignes [mesuré, rapport de correction de D8a l.85] pour 76 cas [commentaire du job g1, `lot.diff` de D8a]) ; boucle de la table ≈ 10 |
| `enforcement/tests/fixtures/secrets/sondes.tsv` | 0 | ≈ 34 | 0 | 32 sondes plus 2 lignes d'en-tête |
| `.github/workflows/gates.yml` | 0 | ≈ 30 | ≈ +4 | D8a : +34 pour un job et son en-tête [mesuré, même rapport l.85] ; D8b-3 : `fetch-depth` et étape 3 |
| **total** | **≈ 186** | **≈ 122** | **≈ 96** | **≈ 404** |

- **Écart à l'annexe A (≈ 130 = 107 + ≈ 22)** : la ligne de lot, sans détail, ne nomme pas de tests, à la différence de celle de D8a (≈ 50 de tests, annexe A l.30). Les ≈ 274 lignes de plus viennent du runner (≈ 196, absent de l'estimation d'origine), de la fixture (≈ 34), du mode historique dans le gate (≈ +36, moins ≈ 3 d'en-tête gagnées au port) et du job complet (≈ +12). Aucune ligne ne vient d'un contrôle hors mandat : la table du §7 est la liste de ce que ces lignes paient.
- **Documentation** : le journal `docs/G1-lot-D8b.md` (≈ 300 lignes, précédent D8a : 366) et la copie de ce G0 (≈ 480 lignes) sont **hors compte de code**, selon le précédent : le cp-1 de D8a a répondu à Q-G0-1 que le compte de code gouverne et que le compte avec documents est rapporté (`G2-rapport.md` de D8a l.107 et l.307). La mission écrit que le texte de G0 et d'ADR compte tout de même, et Q-G2-1 de D8a reste ouverte. Le G1 publie les deux comptes (Q-G0-1).
- **Marge d'erreur** : B0 avait estimé 193 lignes et en a mesuré 252, soit +30 % (journal de B0 l.20-21) ; D8a-1, 202 estimées et 213 mesurées (journal G1 de D8a, E-4). D8b-1 (≈ 186) est sous le seuil, mais sans grande marge : la coupe est décidée d'avance (FM-1.5).
- **Règle de coupe** (méthode du lot A : `git diff --numstat` des fichiers suivis, `wc -l` des fichiers neufs, estimation écrite et scellée avant tout code) :
  1. trois sous-lots, dans l'ordre D8b-1 → D8b-2 → D8b-3, chacun sur l'état du précédent ;
  2. si D8b-1 dépasse 200 à la mesure : T-11 à T-14 passent en D8b-2 (les cas seulement, pas le code) ;
  3. si un sous-lot dépasse encore 200 : arrêt et consultation formée (R-26). On ne comprime jamais le gate ni le runner en retirant un contrôle ou un cas.
- **Branchement des sous-lots** : D8b-1 n'est pas branché seul (aucun job) ; il est consommable au G7 avec D8b-2, comme D8a-1 avec D8a-2. D8b-2 branche l'arbre (job g3, étapes 1 et 2). D8b-3 branche l'historique (étape 3, `fetch-depth: 0`). Les trois se revoient au même G2 ; commit unique ou commits empilés, au choix de l'orchestrateur (précédent B0-1 et B0-2, commit `0abc881`).
- **Coupe inverse, offerte au cp-1 et non retenue** : port seul (arbre et index), 24 cas amont reconstruits, job `--tree`. Estimation ≈ 104 + 112 + 30 ≈ 246 : plus de 200 encore, donc deux sous-lots ; et le tuyau d'historique de l'annexe A l.31 resterait absent, sous un item daté. Elle ne se rapproche des ≈ 130 qu'en retirant les tests.
- Lignes proposées pour l'annexe A (acte de l'orchestrateur, ADR-0028 §6), au format de ses colonnes :

| lot (date) | objet (décision) | véhicule | oracle non-LLM nommé | taille estimée (R-25) | tuyau (entrée → sortie → consommateur ; test) | cp-1 |
|---|---|---|---|---|---|---|
| **D8b** (2026-09-30, amendement daté du G0) | D8 : `gate-secrets.sh` porté (arbre, index), mode `--history` neuf (§5.1 du G0 : la source n'en a pas), job g3 ; ligne l.31 amendée | `enforcement/`, `gates.yml`, tests shell | O-1 à O-12 du G0 ; 36 familles de mutants de gate | ≈ 404 [inféré, bases du §9 du G0] au lieu de ≈ 130 ; coupe en D8b-1, D8b-2, D8b-3 | arbre et historique → gate → job g3 (partiel : GC-01, GC-09) ; hook : item 4 ; test O-2, O-3 et O-4 | complet |
| **D8b-1** (2026-09-30, coupe R-25 du G0 de D8b) | moteur porté (arbre, index) ; références réattribuées ; jetons ; argument inconnu refusé ; `LC_ALL=C` ; cas T-01 à T-14 | `enforcement/gate-secrets.sh`, `enforcement/tests/run-fixtures-secrets.sh` | O-1 (14 cas), O-5 (M-1, M-2, M-6, M-7, M-16, M-18, M-19), O-6, O-8, O-9, O-11 | ≈ 186 [inféré] | non branché seul : consommable au G7 avec D8b-2 | complet (sous le cp-1 du lot) |
| **D8b-2** (2026-09-30, coupe R-25 du G0 de D8b) | contrat d'exclusion, sondes par alternative (fixture tronquée), job `g3-secrets` (runner, `--tree`), en-tête ; cas T-15 à T-32 | la fixture, les deux scripts, `.github/workflows/gates.yml` | O-1 (48 cas), O-2, O-4 (k=1, k=3), O-5 (M-3 à M-5, M-8 à M-15, M-17, M-20 à M-22), O-6 à O-10, O-12 | ≈ 122 [inféré] | arbre → gate → job g3 et G3 opérant local ; test O-2 et O-4 | complet (sous le cp-1 du lot) |
| **D8b-3** (2026-09-30, coupe R-25 du G0 de D8b) | mode `--history` (`--all`, drapeaux forcés, refus du superficiel, attribution), `fetch-depth: 0`, étape 3 ; cas T-51 à T-67 | les deux scripts, `gates.yml` | O-1 (17 cas), O-3, O-4 (k=2), O-5 (M-23 à M-36), O-6, O-8 à O-10, O-12 | ≈ 96 [inféré] | historique → gate → job g3 ; test O-3 et O-4 | complet (sous le cp-1 du lot) |

- *Amendement daté du 2026-09-30 (G1 ; cp-1 C-2, C-4)* : mesures du G1 (journal G1 §1) : D8b-1 180, D8b-2 92, D8b-3 94 lignes de code, soit 366 en somme des sous-lots et 349 au `lot.diff` ; la coupe du §9 tient sans la règle 2. Écarts déclarés avant code (`oracles/estimation-R25.txt`) : les 4 lignes de fixture dont D8b-1 tire ses valeurs sont versées dès D8b-1 ; sondes T-33 à T-35 et cas T-68 à T-70 ajoutés. Les lignes datées de l'annexe A et la ligne d'annexe E des écarts au blob sont proposées au journal G1, pour l'acte de l'orchestrateur. Le compte de code gouverne la coupe ; le compte avec documents est publié (C-4).

## 10. Tuyaux (CA-11 durci)

| rôle | objet | état |
|---|---|---|
| entrée 1 | arbre suivi, lu dans l'index : 286 fichiers à `cf696bd`, produits par les commits du dépôt | présent |
| entrée 2 | historique atteignable depuis les refs : 128 commits et 16 refs dans le clone, `--all` | présent |
| entrée 3 | contenu indexé d'un commit en préparation (mode sans argument) | présent en local ; son consommateur est absent |
| sortie | code 0 ou 2 ; jetons sur stderr ; constats masqués (chemin, ligne, commit) | à construire |
| consommateur 1 | job `g3-secrets` (runner, `--tree`, `--history`) | **partiel déclaré**, comme CI-S2 et D8a : forge morte (GC-01), aucun `required_status_checks` (GC-09). G3 opérant = rejeu local des commandes du job par l'orchestrateur (ADR-0028 l.196, l.290). Item 3 |
| consommateur 2 | hook versionné (D8c), en mode indexé | **absent** : le hook actuel ne lance aucun balayage de secrets (§4). Item 4, déclencheur G0 de D8c |
| état | aucun ; le fichier d'exclusion, absent, en tiendrait lieu | — |
| test de composition | O-2 et O-3 : entrée réelle committée → gate → 0 ; O-4 : copie de cette entrée, un commit rouge semé → 2 et jeton | l'exécution du job sur la forge relève de l'item 3 |

## 11. Items formés (règle Dettes et PAROXYSME)

| # | item | objet | propriétaire | déclencheur | origine |
|---|---|---|---|---|---|
| 1 | SHOGEN-SECRETS-SCANNER-DEDIE-1 | **recherche** du scanner dédié que prévoit le gabarit du corpus (l.57-58) et sur lequel s'appuie le contrat canonique (l.20-21) : outil de la classe citée par le gabarit, vérification de registre (R-8), épinglage par empreinte, fonctionnement hors ligne, règles au-delà du plancher (entropie, formats nouveaux, secrets coupés), prix et licence ; puis ADR sourcé (R-23) | recherche : orch. ; installation : go du mainteneur (R-8) | maintenant (recherche sans code) ; décision au prochain point d'étape | PAROXYSME (CH-16) ; §5.5 |
| 2 | SHOGEN-FORGE-SECRET-SCANNING-1 | balayage des secrets, protection des poussées et code security de la forge, désactivés (git-ci l.26, P10) : lecture sur place, par l'orchestrateur, des conditions et du prix pour un dépôt privé ; question à l'investisseur | recherche : orch. ; décision : investisseur | prochain point d'étape | PAROXYSME ; GC-10 |
| 3 | SHOGEN-G3-FORGE-1 | (a) `g3-secrets` aux `required_status_checks` (GC-09) ; (b) première exécution sur la forge (GC-01) ; (c) ce que l'oracle local ne prouve pas : `grep`, `awk`, `tr`, `mktemp` et `iconv` de l'image, effet réel de `fetch-depth: 0`, temps sur Linux, lecture du workflow par la forge | orch. ; (a) investisseur ou mainteneur | forge rétablie (§4.1) | modèle : SHOGEN-G1-FORGE-1 (D8a) ; O-10 et O-12 |
| 4 | SHOGEN-D8-HOOK-SECRETS-1 | le hook versionné de D8c lance le mode indexé du gate (consommateur 2) ; y régler le coût par commit | orch. | G0 de D8c | annexe A l.31 ; §10 |
| 5 | SHOGEN-SECRETS-HORS-REFS-1 | objets inatteignables (la cartographie en a sorti une liste brute, `dangling.txt`, git-ci l.8 ; contenu non lu par ce G0), commits connus des seuls journaux de refs, bundles de custodie : un balayage unique par les mêmes motifs, comptes seuls, sans afficher de contenu | orch. | avant toute copie brute de `.git` en custodie, ou avant le passage public (D10), au premier des deux | CH-3 |
| 6 | SHOGEN-SECRETS-REVOQUE-1 | **recherche** d'une liste de constats révoqués, par commit, chemin et empreinte de ligne, sous ADR, compatible avec D7 (aucune réécriture d'historique) : un constat réel dans l'historique rougirait le job pour toujours, et une exclusion par chemin ouvrirait ce chemin | orch. | premier constat réel | CH-15 |
| 7 | SHOGEN-BIBLIO-GIT-CHECKOUT-1 | verser à `biblio/` (entrées `INDEX.md`, compte S-G6) les pages de git 2.55 et l'`action.yml` d'actions/checkout au SHA `3d3c42e5…` lues au G0 | orch. ; go requis pour un téléchargement (règle de lecture sur place) | avant le journal G1 s'il les cite entre guillemets ; sinon au prochain versement | S-G5 ; §4 |

Transmission, sans item neuf : la chaîne de provenance du §5.2 rejoint SHOGEN-D8-AMONT-ERRATUM-1 (item 11 du G0 de D8a).

## 12. Critères d'acceptation fermés

- **CA-D8b-1** : `git diff --name-status <base>` = exactement les fichiers IN du §3, base = état après D8a.
- **CA-D8b-2** : aucun fichier de `F:/Shogen` hors IN modifié ; `.git/hooks/pre-commit` inchangé (sha256 du §4).
- **CA-D8b-3** : O-1 vert, table du §7 intégrale pour le lot, part de chaque sous-lot publiée.
- **CA-D8b-4** : O-2 et O-3 verts, sur le worktree et sur l'arbre principal.
- **CA-D8b-5** : O-4, trois rouges, jetons attendus, attribution de k=2 égale au commit C1.
- **CA-D8b-6** : O-5, chaque mutant tué, sauf les équivalents déclarés (M-24, et ceux de M-36 que le G1 mesure), chacun avec sa commande de rejeu ; lignes de commande et sorties au journal G1 ; catégorie F2P déclarée.
- **CA-D8b-7** : O-6 = 0 sur tous les fichiers ajoutés ou modifiés, copie de ce G0 comprise.
- **CA-D8b-8** : O-7 = 0.
- **CA-D8b-9** : O-8 (xtask VERT, suite `s2-harness` identique à la base) et O-9 (0 entrée neuve dans TMP).
- **CA-D8b-10** : O-10 tenu ; aucun autre job modifié ; diff de `gates.yml` limité à l'ajout et à l'en-tête.
- **CA-D8b-11** : O-11 : sortie 3 et aucun dossier créé ; `GIT_DIR` et `GIT_WORK_TREE` absentes de toute commande du G1 et du G2.
- **CA-D8b-12** : en-tête du gate conforme au CH-5 : aucune référence nue à `ADR-0004`, aucun pourcentage, provenance citée, filet absent déclaré.
- **CA-D8b-13** : R-25 mesuré ≤ 200 par sous-lot, méthode écrite ; estimation scellée avant tout code ; lignes datées proposées pour l'annexe A.
- **CA-D8b-14** : journal G1 au format de B0 (§15) ; vocabulaire 09 respecté (ni « garantit », ni « indépendant » comme fait, ni `verified`, ni « CI verte donc… ») ; aucune citation entre guillemets d'une source non versée.
- **CA-D8b-15** : enregistrement d'oracle substitut produit au G1, puis refait par le G2.
- **CA-D8b-16** : items 1 à 7 repris au journal G1 ; versement à l'annexe B par l'orchestrateur.
- **CA-D8b-17** : CH-8 : les cas portés rendent les mêmes sorties sous la locale ambiante et sous `C`, mesuré au journal G1.

## 13. Risques MAST (libellés : annexe C l.13-18 ; les 14 modes restent la liste de revue)

| mode | forme dans D8b | contre-mesure système | preuve |
|---|---|---|---|
| **FM-1.1 Disobey task specification** | (a) le runner écrit dans le dépôt réel (classe des incidents du 2026-09-24) ; (b) une forme complète d'identifiant entre dans un fichier suivi ; (c) une ligne de D.2 signalée est affichée pour l'inspecter | (a) garde `GIT_*`, contrôles hors dépôt et `show-prefix`, `-C` partout (CH-12) ; (b) fixture tronquée et O-6 ; (c) règle du CH-15 : identification par sha256 seul | O-11, O-6, CA-D8b-2 |
| **FM-3.3 Incorrect verification** | tests verts sur un gate trop permissif : alternative non testée, cas amont portés sans le jeton, mode historique qui ne voit pas une fusion ou un binaire | sondes par alternative ; sortie ET jeton ; sondes S2 à S7 devenues cas ; mutants M-1 à M-36 | O-5 |
| **FM-3.2 No or incomplete verification** | l'oracle local ne prouve ni les outils de l'image, ni `fetch-depth: 0` en situation, ni la lecture du workflow par la forge ; le gate ne voit que des formes | item 3 ; CH-16 et items 1, 2, 5 | déclaré |
| **FM-2.3 Task derailment** | glissement vers le scanner dédié, la forge, le hook, la vitesse de `--tree`, `gate-gist.sh`, `s2-harness` | liste OUT (§3) ; items 1 à 5 ; diff limité (CA-D8b-1) | revue G2 |
| **FM-2.4 Information withholding** | faits retenus : prémisse de mission corrigée, runner amont non portable, filet absent, références ADR-0004, écart `git status` | §0, §5.1, §5.2, §5.5 et en-tête de ce document | sceaux du §15 |
| **FM-1.5 Unaware of termination conditions** (ici : coupe R-25 improvisée, ou historique sans fin) | la coupe se décide après coup ; le balayage d'historique n'a pas de borne | règle de coupe écrite d'avance, avec arrêt et consultation (§9) ; coût mesuré, refus du superficiel, plafond de constats, `timeout-minutes` (CH-3) | journal G1 §1 ; T-59, T-66 |

Topologie (CA-4) : un G1 mono-agent en worktree, puis un G2 sur instance séparée à contexte frais. Aucun autre fan-out : le partage n'a pour motif que la séparation de vérification imposée par le système. Conflit de fichier : D8a et D8c modifient aussi `gates.yml` ; ordre D8a, D8b, D8c.

## 14. Questions pour l'orchestrateur

- **Q-G0-1** : compte R-25 des documents (journal et copie du G0) : le précédent du cp-1 de D8a vaut-il pour D8b, alors que la mission les compte ? Si non, les deux documents forment un commit documentaire séparé.
- **Q-G0-2** : portée `--all` (CH-3) plutôt que l'ascendance de HEAD. Conséquence : un secret sur toute ref récupérée rougit le job de `main`. À confirmer ou à renverser au cp-1.
- **Q-G0-3** : messages en français et jetons (CH-6), argument inconnu refusé (CH-7), `LC_ALL=C` (CH-8) : ces écarts au blob source demandent-ils une ligne à l'annexe E, comme Q-G0-5 de D8a ?
- **Q-G0-4** : retrait des deux pourcentages du canonique (CH-5). Si l'orchestrateur veut garder cette base chiffrée, un procurement doit être formé ; l'identité bibliographique complète est à établir (tentative du G0 : recherche dans le corpus et dans l'amont, forme courte seulement).
- **Q-G0-5** : trois sous-lots (≈ 404) plutôt que la coupe inverse (≈ 246, historique en item) : à confirmer.
- **Q-G0-6** : nom du fichier d'exclusion gardé (`.vibegates-secretscan-exclude`, CH-9) plutôt qu'un nom propre à Shōgen.

## 15. Consignes au G1 et sceaux

- **Base** : `main` après le commit de D8a. À défaut, un worktree sur `main` avec le `lot.diff` final de D8a appliqué par `patch -p1`, déclaré au journal. `gates.yml` cible : l'état après D8a (job `g1-model-pinning` présent, en-tête l.3-20 déjà amendé).
  - *Amendement daté du 2026-09-30 (G1)* : base consignée `40b4cfb` (worktree avancé de `fa0ce5b` par `git merge --ff-only 40b4cfb`, dans le worktree seulement). À 16:52Z, `main` est à `293b7a7` (un commit de JOURNAL de plus, aucun fichier du lot touché, mesuré).
- **Worktree et environnement** : `TMPDIR`, `TMP` et `TEMP` sur `F:/tmp/shogen-tests-tmp` (un sous-dossier frais par exécution) ; `CARGO_HOME` et `CARGO_NET_OFFLINE=true` de la mission, toolchain locale sans installation (précédent : `F:/tmp/shogen-lots/D8a/corr-oracles/cargo_env.sh`, avec un `CARGO_TARGET_DIR` propre à D8b). Ni `GIT_DIR`, ni `GIT_WORK_TREE`, ni `--write-tree`, ni `SHOGEN_S2_CAMPAGNE_CONTROL` ; aucune pièce de D.2. Seul un commit local d'empilement dans le worktree est admis.
- **Écriture des scripts** : le harnais a refusé, au G1 de D8a, des heredocs Bash qui contenaient `git` (journal G1 de D8a §13). Le runner en est plein : il s'écrit par l'outil d'écriture de fichiers, ou par un fichier assemblé hors heredoc, et le journal le déclare.
- **Valeurs formées** : jamais dans une commande affichée, jamais dans le journal ; seuls les fragments de la fixture apparaissent dans les fichiers suivis. O-6 se lance sur le journal et sur la copie du G0 avant la remise.
- **Lignes de D.2** : si le gate signale une ligne d'une pièce de D.2, le G1 et le G2 l'identifient par son sha256 et ne l'affichent pas (CH-15).
- **Journal `docs/G1-lot-D8b.md`**, au format de B0 :
  - en-tête : modèle, horloge `date -u`, mandat, base ;
  - §0 préconditions (PC-1 citée, §2) ; §1 coupe R-25 (estimation scellée avant code, puis mesure, deux comptes) ; §2 changements (sha256 avant et après) ; §3 définitions appliquées (CH-1 à CH-16) ; §4 tests, chaque test nommant sa mutation ; §5 mutants ; §7 tuyaux ; §8 MAST ; §9 `error_origin` ; §10 Review Focus ; §11 Q-G1 ; §12 livrables ; §14 attestation.
- **Runner** : conçu d'après l'amont (`7960238`), compact ; aucune valeur formée en clair ; pas de mutants dans le dépôt ; pas de section GIST.
- **Sceaux** : `F:/tmp/shogen-lots/D8b/g0-mesures/SHA256SUMS.txt` (30 entrées, sha256 `b197e15c565e376541dc8e0866abcfba08d7a63cc6959369377f52c17de04186`, scellé à 09:14:33Z ; `sha256sum -c` : 30 OK) liste :
  - `gate-secrets-6789a30.sh`, `gates-493ae8c.yml`, `amont-run-fixtures-7960238.sh`, `action-checkout-3d3c42e5.yml` ;
  - `canon-tree-cf696bd.out` ;
  - `mesure-historique.sh`, `.out`, `.horloge` ; `mesure-all.sh`, `.out` ;
  - `mesure-sondes.sh`, `.out`, `.horloge` ; `mesure-s3bis.sh`, `.out` ;
  - `proto-historique.sh` ; `proto-sondes.sh`, `.out`, `.horloge` ; `proto-reel.out` ;
  - `git-log-2.55.0.txt`, `git-rev-parse-2.55.0.txt`, `git-rev-list-2.55.0.txt`, `git-cat-file-2.55.0.txt`, `git-diff-2.55.0.txt` ;
  - `horloge-debut.txt` ;
  - `cargo_env.sh`, `xtask-g0-v1.log`, `.exit`, `.horloge` (contrôle de ce document, §15 bis).
- **Copie amont à ne jamais verser** : `amont-run-fixtures-7960238.sh` porte les 19 formes complètes du §5.2. Elle reste sous `F:/tmp` comme pièce de mesure ; aucun fichier du lot ne la recopie.
- **Rejeu** : dans `g0-mesures/`, avec `TMPDIR` sur `F:/tmp` : `bash mesure-historique.sh <clone> <rev>`, `bash mesure-all.sh <clone>`, `bash mesure-sondes.sh`, `bash mesure-s3bis.sh`, `bash proto-sondes.sh`, et `bash proto-historique.sh` lancé depuis la racine d'un clone. Les sorties reproduisent les comptes et les codes ; les temps varient.
- **Contrôles de ce document avant remise** : §15 bis.
- Le sha256 de ce document est écrit à côté, dans `G0-lot-D8b.md.sha256`.

## 15 bis. Contrôles non-LLM appliqués à ce document

- **O-6 sur ce G0** : motifs du blob `6789a30` (évalués depuis ses l.48-49), `LC_ALL=C`, appliqués au fichier : 0 ligne VENDOR, 0 ligne GENERIC. Même contrôle, par une boucle sur `g0-mesures/*.sh`, sur les huit scripts autres que la copie amont : 0 et 0 chacun. La copie amont `amont-run-fixtures-7960238.sh` rend 14 et 5, par construction (§5.2).
- **Vocabulaire** : aucune des 15 locutions de S-G4 hors code ou citation ; aucun guillemet ASCII hors code ; aucun fragment anglais entre guillemets français.
- **`cargo --locked xtask verify`** (environnement `g0-mesures/cargo_env.sh` : toolchain locale forcée, aucune installation, `CARGO_HOME` et `CARGO_NET_OFFLINE=true` de la mission, cible `F:/tmp/shogen-lots/D8b/target`) sur une copie `git archive cf696bd`, avec les 152 fichiers de `F:/Shogen/biblio/` copiés pour le corpus complet et ce G0 posé en `docs/adr-0028/G0-lot-D8b.md` :
  - de 09:11:28Z à 09:12:44Z, sortie 0, **VERDICT GLOBAL : VERT** (`g0-mesures/xtask-g0-v1.log`) ;
  - S-G4 : 46 fichiers examinés, 0 violation ; S-G5 : 47 fichiers, corpus complet (125 artefacts sur 125 déclarés), 0 violation ;
  - 0 téléchargement sous `F:/rust/rustup/downloads` (compté avant et après).
- Ce premier passage portait le texte d'avant les corrections de relecture et d'avant ce §15 bis. Le texte final est recontrôlé par les mêmes commandes après l'écriture de ce paragraphe (`xtask-g0-v2.*`, hors sceau, sous `F:/tmp/shogen-lots/D8b/`) ; le résultat est rendu à l'orchestrateur avec le chemin de ce document.

## 16. Index des amendements du G1 (2026-09-30)

- Statut (C-9 : forme de la copie) ; Mandat (C-1) ; CH-3 (C-3) ; CH-5 (C-5) ; CH-9 (C-6) ; CH-12 (G1 : motifs requis ou interdits) ; §7, après la table (C-7 ; cas du G1) ; O-1 (C-7) ; O-2 (G1) ; O-5, après la ligne F2P (C-8 ; mutants du G1) ; §9, lignes proposées pour l'annexe A (C-2, C-4) ; §15, Base (G1).
- C-2 (lignes datées de l'annexe A, ligne d'annexe E) et C-4 (deux comptes) : propositions au journal G1 (`docs/G1-lot-D8b.md` §1), actes de l'orchestrateur. C-9 : le journal G1 renvoie au rapport du cp-1 et à son sha256.
- **Correction de la revue G2** (2026-09-30, C-G2-1 à C-G2-11) : puces sous CH-1, CH-2, CH-3, CH-4, CH-6, CH-12, CH-14, CH-16, la table du §7, O-1 et O-5 ; cas, mutants et mesures au journal G1 §15.
- **Correction de la re-revue rr1** (2026-10-01, CR-rr1-1) : T-75b ; puces sous CH-2, CH-3, CH-12, la table du §7, O-1 et O-5 complétées, compte du runner porté à 113 ; mesures au journal G1 §15.
