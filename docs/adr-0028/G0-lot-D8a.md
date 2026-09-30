# G0 — lot D8a d'ADR-0028 : lint d'épinglage des modèles (`enforcement/lint-model-pinning.sh`), job g1, cas C-14 — Shōgen, document de planification

- **Statut** : G0 proposé, soumis au **cp-1 complet** (annexe A l.22, colonne cp-1 = « complet »). Aucun code n'est écrit par ce document.
  - *Amendement daté du 2026-09-30 (G1 du lot, `claude-opus-5-5`)* : G0 accepté au cp-1 complet avec les corrections C-1 à C-8 (commande de mission du G1). Le texte accepté est conservé à l'identique (sha256 `8afa3f7dd2c7232ea459bd7308e97391b61c99055084cd6035262d10afe4c387`, `F:/tmp/shogen-lots/D8a/G0-lot-D8a.md`) ; chaque correction est une puce datée placée sous le point qu'elle supplante, indexée au §16. Le `diff -u` entre le texte accepté et cette copie est livré avec le G1 (`F:/tmp/shogen-lots/D8a/oracles/G0-copie.diff`).
- **Rédacteur** : worker G0 `claude-opus-5-5` (modèle résolu déclaré en tête de session, R-1), effort max, contexte frais. Destinataire : orchestrateur Shōgen `claude-fable-5-1`. Réviseurs attendus : orchestrateur (R-21), puis validateur-humain (cp-1 complet).
- **Horloge** (`date -u`) : orientation commencée avant la première heure relevée (02:47:58Z) ; mesures G0 de 02:53:53Z à 03:15:49Z (sceau final de `g0-mesures/`) ; pages Claude Code lues entre 02:55:16Z et 03:03:42Z (seules ces deux bornes sont des relevés d'horloge) ; faits de l'amont VibeGates relevés à 03:03:42Z ; rédaction à partir de 03:09:14Z.
- **Mandat** : commande de mission de l'orchestrateur (workflow du 2026-09-30), lot D8a de l'annexe A. Base : `fb089dc` (`main`). Lecture seule sur `F:/Shogen` ; aucun worktree utilisé.
- **Isolation git** : aucun `GIT_DIR`, aucun `GIT_WORK_TREE`, aucun `--write-tree` ; aucun commit, add, stash, checkout, reset ni push. Commandes git employées : `show`, `rev-parse`, `log`, `ls-tree`, `archive` (vers `F:/tmp`), `hash-object` sans `-w`, `cat-file -e`, `worktree list`, `branch --contains`.
  - **Écart déclaré** : `git status --short` a été lancé une fois sur `F:/Shogen` (orientation) et une fois dans le clone VibeGates du corpus, sur C:. `git status` peut poser un `index.lock` transitoire. Dans le clone VibeGates, le mtime du dossier `.git` est passé à 2026-09-30T02:44:53Z ; `index`, objets et références sont inchangés (mtimes du 2026-08-12 au 2026-08-20). Sur `F:/Shogen`, `.git/index` et `refs/heads/main` restent à 02:36:52Z (commit `fb089dc`) ; le mtime du dossier `.git` (02:39:27Z) n'est pas attribuable, les worktrees de la vague 2 étant actifs. Toutes les lectures suivantes sont en `git --no-optional-locks`. `error_origin` proposé : worker G0.
- **Écritures** : `F:/tmp/shogen-lots/D8a/` seulement (ce document et `g0-mesures/`, scellé §15). Rien sur C: : le `mktemp` de Git Bash résout vers `F:\tmp` (mesuré : `cygpath -w /tmp`), et aucun dossier temporaire ne reste après les mesures (0, mesuré).
- **Interdits (annexe D.2 et D.4 a)** : aucune pièce de campagne ouverte, `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée, aucune statistique S2 lue ni calculée. Aucun z, K, P̂_more ni φ vu.

## 0. Résumé (une phrase par tâche, CA-1)

1. **Porter** le lint canonique (blob `457565f`) en **liste blanche exacte** (CB-10) : tout identifiant hors {`claude-opus-5-5`, `claude-sonnet-5-5`, `claude-fable-5-1`} est refusé, sortie 2.
2. **Tester** ce lint sur des copies datées des deux frontmatters réels, dans des arbres temporaires, jamais sur `.claude/agents/`.
3. **Brancher** le lint au job `g1-model-pinning` de `gates.yml` (tests, puis arbre réel).

Fait nouveau à porter en tête : l'amont VibeGates **est retrouvé** dans le corpus (§5.1). Le blob canonique est identique à l'amont, octet pour octet. Le constat de git-ci §2.b et la prémisse de D8 (« faute d'une amont retrouvée ») sont faux, mais la source canonique ne change pas.

## 1. Objet et décisions rattachées

| rattachement | lieu | ce qu'il fixe pour D8a |
|---|---|---|
| D8 | `docs/adr-0028/ADR-0028-decisions-sortie-S2.md` l.93-101 | lots D8a-c ; source canonique = blob de `adb2213` (l.95) ; pas les fichiers d'agents supplantés (l.94) |
| C-14 (G1 de D8a) | même fichier l.96-99 | acceptés, refusés, deux cas limites « tranchés et testés au G0 de D8a » |
| CB-10 (cp-1 bis) | `F:/tmp/cp1-adr0028/CP1-BIS-ADR-0028.md` l.89, l.132 | liste blanche **exacte** plutôt qu'une règle de préfixe ; suffixes entre crochets décidés séparément en frontmatter et en journal |
| ligne de lot | `docs/adr-0028/ANNEXE-A-lots.md` l.22 | véhicule, oracle, ≈ 205 lignes, tuyau `.claude/agents/*.md` → lint → job g1 (et hook), cp-1 complet |
| item | `docs/adr-0028/ANNEXE-B-items.md` l.24 | SHOGEN-ENFORCEMENT-PORTAGE-1 : déclencheur « G0 de D8a, après la confirmation §4.10 a » |
| avis | `F:/tmp/shogen-carto-2026-09-29/avis-adr0028/AVIS-advisor-2026-09-29.md` l.86-105 ; annexe E l.29-32 | périmètre (l.96), source amont (l.97), risque du roster daté (l.103), confirmation de l'investisseur (l.105) |
| roster en vigueur | `CLAUDE.md` l.20-31 ; `docs/DECISIONS.md` l.2965-2968 (ADR-0019 D5, bannissement) | les trois identifiants admis ; `claude-opus-5` banni ; jamais un tier nu |

## 2. Précondition PC-1 (§4.10 a) — non tranchée ici (CA-2)

- ADR-0028 l.160 fait de la confirmation de l'investisseur un préalable de D8 : la décision du 2026-08-20 doit tenir dans sa forme g1/g3/g5, sinon D8 devient un ADR de retrait motivé (avis Q8, l.105).
- **Mesuré** : aucune confirmation n'est consignée. La recherche de `full opérationnel` et `4.10 a` dans `JOURNAL.md` et `docs/DECISIONS.md` ne trouve que les lignes d'ADR-0028 elles-mêmes.
- La délégation du 2026-09-30 couvre les lots de l'annexe A (`JOURNAL.md` l.112). L'avis Q5 du même jour rejette la lecture « veto réputé levé » : le veto n'est pas exercé, et sa fenêtre est prolongée jusqu'à l'exécution unique (`JOURNAL.md` l.114, erratum adopté).
- **Règle proposée** (précédent de B0-2, `docs/G1-lot-B0-pool-analyse.md` l.13) : le G1 peut travailler en worktree. Le lot est additif (fichiers neufs, plus un job) et se défait par un seul revert. En revanche, la consommation au G2, le G7 et le commit restent bloqués tant que l'orchestrateur n'a pas consigné au JOURNAL l'une des deux formes suivantes :
  - la confirmation de l'investisseur ;
  - la lecture « couvert par la délégation du 2026-09-30, veto non exercé, révocable jusqu'à l'exécution unique ».
  Si le veto est exercé : D8 passe en ADR de retrait, le worktree est abandonné, aucun commit.

## 3. Périmètre

**IN**

| fichier | nature |
|---|---|
| `enforcement/lint-model-pinning.sh` | neuf, porté du blob `457565f` (§6) |
| `enforcement/tests/run-fixtures-model-pinning.sh` | neuf ; nom de l'amont (blob `d9ad850`) ; accepte le chemin du lint en `$1` |
| `enforcement/tests/fixtures/model-pinning/shogen-devops.md` | copie octet pour octet de `fb089dc:.claude/agents/shogen-devops.md` l.1-13 (frontmatter) |
| `enforcement/tests/fixtures/model-pinning/shogen-orchestrator.md` | copie de `fb089dc:.claude/agents/shogen-orchestrator.md` l.1-15 |
| `.github/workflows/gates.yml` | job `g1-model-pinning` ; en-tête l.3-19 mis à jour pour nommer g1 |
| `docs/G1-lot-D8a.md` | journal G1, au format de `docs/G1-lot-B0-pool-analyse.md` |

**OUT**, avec motif :
- `.claude/agents/*.md` : jamais touchés, ils sont l'entrée du tuyau (mission ; D8 l.94).
- `gate-secrets.sh` et job g3 : lot D8b. Hook versionné, motif g5 élargi, entrée « collision ADR-0020 » : lot D8c.
- Tag `archive/roster-ban-2026-08-20` et suppression de la branche : acte de l'investisseur (§4.10 a), hors lot (mission ; ADR-0028 l.101).
- Jumeau `.ps1` de l'amont (blob `d9425cf`) : non porté. La CI est un `bash` Ubuntu et l'oracle local un Git Bash ; aucun des deux côtés n'en a besoin.
- Contrôle de l'effort, clés d'environnement des réglages, scan complet des scripts de workflow, mécanisation de la règle « journal », agents et réglages hors dépôt, liste blanche au niveau de la plateforme : items §11 (discipline de périmètre, FM-2.3).
- `s2-harness/` en entier (vague 2 en vol ; mission). ADR-0028 et ses annexes : les lignes datées des sous-lots sont un acte de l'orchestrateur (ADR-0028 §6 l.188).

## 4. Sources lues (niveau, lieu)

| source | lieu | niveau | usage |
|---|---|---|---|
| blob canonique `457565f` | `git show adb2213:enforcement/lint-model-pinning.sh` (143 l., sha256 `983ba152…`) | [lu] en entier | base du port ; l.2, 10-12, 13-19, 20-22, 23-34, 39, 42, 52-58, 66, 72, 79, 84-88, 96, 114, 124-132, 138-139 |
| job g1 d'origine | `adb2213:.github/workflows/gates.yml` (blob `493ae8c`) l.45-57 | [lu] | `ubuntu-latest`, checkout v4.4.0 `11d5960a…`, name `g1-pinned-models` |
| `gates.yml` courant | `fb089dc` l.1-92 | [lu] | en-tête l.3-19, règle du nom l.60, image l.62-67, checkout l.77 |
| amont VibeGates | clone `…\compiliance et ingénierie locielle et architecturale\vibegates\` | [mesuré] (§5.1) | provenance ; runner amont `run-fixtures-model-pinning.sh` l.21-27, 29-31, 33-40, 85-86 |
| hook local | `.git/hooks/pre-commit` (78 l., sha256 `1da91c72…`) | [lu] | exclusions l.53-55, motif l.71 ; ne lance aucun lint (consommateur 2 absent) |
| cartographie git-ci | `F:/tmp/shogen-carto-2026-09-29/git-ci.md` l.22-23, 90-119, 221, 225, 229, 231 | [lu] | P6, P7, §2.b, GC-01, GC-05, GC-09, GC-11 |
| cp-1 bis | `CP1-BIS-ADR-0028.md` l.31, 61, 89, 132 | [lu] | CB-10 |
| avis advisor Q8 | AVIS l.86-105 | [lu] | options (c), risque du roster daté |
| ADR-0028, annexes A, B, C, D, E | l. citées au fil du texte | [lu] | cadre |
| JOURNAL | l.86 (G1 du lot A en `claude-opus-5-5[1m]`), l.92 (8 agents en `claude-opus-5-5`), l.112, l.114 | [lu] | formes résolues observées, PC-1 |
| roster | `CLAUDE.md` l.20-31 ; `docs/DECISIONS.md` l.2965-2968 ; `F:/Monark/docs/roster/FAITS-opus-5-5-2026-09-22.md` l.7, l.20 ; `FAITS-sonnet-5-5-2026-09-28.md` l.6, l.24, l.26 | [lu] | identifiants catalogue, retrait non-ban de `claude-sonnet-5`, effort par défaut `medium` d'Opus 5.5 |
| précédent MONARK | `F:/Monark/scripts/mission/lint.mjs` l.15, l.54, l.178 | [lu] | liste `TIERS` fermée ; `claude-sonnet-5` refusé hors rejeu `--rev` |
| corpus | doc 02 l.80 (R-1), l.83 (R-4 = effort), l.114 (R-25) ; `templates/ci-gates.yml` l.9-14 ; `templates/workflow-passe-agilegates.js` l.28-29, 137, 141 | [lu] | R-4 n'est pas un contrôle d'épinglage ; gabarit de workflow épinglé `claude-opus-4-8` |
| Claude Code, sous-agents | https://code.claude.com/docs/en/sub-agents, lue le 2026-09-30 entre 02:55:16Z (heure relevée juste avant la première lecture) et 03:03:42Z (Firecrawl, `maxAge: 0`, trois extractions) | [lu] | découverte, champ `model`, ordre de résolution (§5.4 a-c) |
| Claude Code, configuration du modèle | https://code.claude.com/docs/en/model-config, lue le 2026-09-30 dans la même fenêtre, après la précédente (deux extractions) | [lu] | contexte étendu et suffixe `[1m]`, `availableModels`, `deniedModels` (§5.4 d-e, item 4) |

- *Amendement du 2026-09-30 (cp-1 C-3)* : les faits de la page des sous-agents (§5.4 a-c et l'allowlist de d-e) sont repris de la lecture sur place de l'orchestrateur, `F:/tmp/shogen-lots/D8a/FAITS-claude-code-subagents-2026-09-30.md` (sha256 `de45ea493892ddbaa9380ae36e1f2f23efe61fc6ab32542b7418be8891bc5f3a`), qui les confirme ; c'est ce fichier que citent le G1 et le lint, non l'extraction Firecrawl. La page de configuration du modèle n'a pas de FAITS de l'orchestrateur : déviation consignée au journal G1 §9 (`error_origin` orchestrateur). Le deuxième motif de CH-4 (fenêtre de 1 M native) repose donc sur la seule lecture du worker G0 ; CH-4 tient par CB-10 et par les identifiants catalogue sans suffixe. L'item 4 ne démarre pas sans ces FAITS.
| gates xtask | `xtask/src/sg4.rs` l.18-20 ; `sg5.rs` l.1-7 | [lu] | S-G4 et S-G5 ne lisent que `docs/**/*.md` : ni `enforcement/` ni `gates.yml` |
| vocabulaire | `docs/09-vocabulaire.md` l.11-13, l.41, l.45 | [lu] | registre des mutants ; « CI verte donc… » interdit |
| validateur | `F:/claude-config/agents/validateur-humain.md` l.38-56, l.130-141, l.169-170 | [lu] | CA-1..CA-5, CA-11 durci |
| précédents de lot | `docs/G1-lot-B0-pool-analyse.md` l.3, 13, 18-33, 97, 141, 225 ; annexe B l.78-80 | [lu] | format du journal, coupe R-25, documentation hors compte, forge |

Aucune page Claude Code n'est versée à `biblio/INDEX.md`. Ce document la paraphrase ; les noms de clés de configuration sont en police de code, ce ne sont pas des citations (item 10).

## 5. Faits mesurés au G0 (`F:/tmp/shogen-lots/D8a/g0-mesures/`)

### 5.1 L'amont VibeGates est retrouvé

Mesure : `amont-vibegates.txt`, lectures en `git --no-optional-locks`, 03:03:42Z.

- Clone : `C:\Users\KACIMI\compiliance et ingénierie locielle et architecturale\vibegates`. HEAD `1263f2a`, branche locale `pass-4-u4`, remote `https://github.com/Kraidle/vibegates.git`.
- `0b4f3f9:enforcement/lint-model-pinning.sh` = blob **`457565f`**, le même qu'`adb2213`.
  - Commit `0b4f3f9` (sujet dans `amont-vibegates.txt`) : 2026-08-20T06:15:14+01:00, 5 min 13 s avant `adb2213` (06:20:27+01:00).
  - Aucune branche distante de suivi du clone ne contient `0b4f3f9` ; aucun fetch n'a été fait. La présence de ce commit sur GitHub **n'est pas établie**.
- Conséquence pour les sources de la cartographie et de D8 :
  - git-ci §2.b l.118 écrit « Source amont non localisée » : elle a cherché dans `…\enforcement\` du corpus, pas dans `…\vibegates\enforcement\` ;
  - la prémisse de D8 (l.95, « faute d'une amont retrouvée ») est fausse ;
  - l'issue est inchangée : la source canonique reste le blob `457565f`, dont la provenance se chaîne désormais à VibeGates `0b4f3f9` ;
  - le repli « procurement VibeGates » de l'avis Q8 pt 2 (l.97) devient sans objet ;
  - l'erratum est un acte de l'orchestrateur (item 11).
- À transmettre aux lots voisins (mesuré, une ligne chacun) :
  - D8b : `gate-secrets.sh` d'`adb2213` (blob `6789a30`) = HEAD amont ;
  - D8c : le hook local (blob git `9c4c846`, obtenu par `hash-object` sans `-w`) = amont `52a569d:enforcement/gate-commit.sh` (2026-08-12) ; l'amont a évolué ensuite (`0b4f3f9`, blob `9dade29`) et porte un dossier `enforcement/hooks/` (six fichiers) ;
  - D8a : le runner amont `run-fixtures-model-pinning.sh` (blob `d9ad850`, 290 l.) est la source de conception des tests. Ses cas « propres » `claude-opus-4-8` et `claude-sonnet-5` (l.85-86) sont **à inverser** : ils sont refusés sous le roster en vigueur (FM-3.3).

### 5.2 Écart entre le canonique et D8/CB-10

Mesure : `mesure-canonique.sh` sur le blob `457565f`, arbres temporaires, identifiant banni construit par concaténation.

| cas | valeur | canonique | décision du G0 |
|---|---|---|---|
| acceptés C-14 | `claude-opus-5-5`, `claude-sonnet-5-5`, `claude-fable-5-1` | 0 | 0 |
| tiers nus | `opus`, `fable`, `sonnet` | 2 | 2 |
| banni | `claude-opus-5`, `CLAUDE-OPUS-5`, banni `# ADR-9999` | 2 | 2 |
| **banni suffixé** | `claude-opus-5[1m]` | **0** | 2 |
| **préfixe du banni** | `claude-opus-5x`, `claude-opus-50`, `claude-opus-5-0`, `claude-opus-5-50` | **0** | 2 |
| **cas limite 1** | `claude-opus-5-5[1m]` | **0** | 2 en frontmatter (CH-4) |
| **cas limite 2** | `claude-sonnet-5` | **0** | 2 (CH-5) |
| **hors roster** | `claude-opus-4-8`, `claude-fable-5` | **0** | 2 (CH-1) |
| **exemption ADR** | `fable   # ADR-0003` | **0** | 2 (CH-6) |
| **clé absente** | aucune ligne `model` | **0** | 2 (CH-7) |
| **dièse collé** | `claude-opus-5-5#x` | **0** | 2 (CH-8) |

Sur 21 cas, le canonique en traite 9 comme ce G0 : 3 acceptés, 6 refusés. Il accepte (sortie 0) les **12 autres**, que ce G0 refuse. Ces 12 cas forment le delta que le G1 doit coder. Détail ligne à ligne dans `mesure-canonique.out`.

### 5.3 Autres mesures

- **Arbre réel** : canonique rejoué sur `git archive fb089dc .claude` (`reel-canonique.out`) : sortie 0, 2 fichiers. C'est le rejeu de git-ci l.115, refait à `fb089dc`. Sur l'arbre de travail de `F:/Shogen` : sortie 0 en 614 ms.
- **Littéral contigu** :
  - `grep -c claude-opus-5` rend 0 sur le canonique comme sur le runner amont ;
  - l'identifiant admis `claude-opus-5-5` contient le banni en préfixe, si bien que l'invariant canonique (l.29-30) ne peut plus être littéral ;
  - forme redéfinie (CH-13) : `grep -rhoE 'claude-opus-5(-5)?' enforcement/ | grep -cvx 'claude-opus-5-5'` = 0 ; ce motif a été éprouvé sur une sonde de cinq lignes, lignes 2 et 3 attendues et trouvées (`mesure-complements.out`).
- **Route d'exemption du canonique** (T-20) : un tier nu dans `advisorModel`, excepté par `model-exceptions.txt`, sort en 0 au canonique (`mesure-complements.out`).
- **Motif du fil de workflow** (CH-9) : sur une sonde de cinq lignes, il signale `agent(`, `await agent (` et un `agent(` indenté, mais ni `useragent(` ni `x.agent(` (`mesure-complements.out`).
- **Scripts de workflow** :
  - 0 fichier `*.js`, `*.mjs`, `*.cjs` ou `*.ts` suivi à `fb089dc` ;
  - 0 fichier `*.js`, `*.mjs` ou `*.cjs` présent hors de `target/`, `.git/`, `.claude/worktrees/`, `biblio/`, `node_modules/`, `fuzz/target/` et `mutants.out*` (find élagué : 268 ms) ;
  - le gabarit du corpus (`templates/workflow-passe-agilegates.js` l.28-29, 137, 141) épingle `claude-opus-4-8`, hors roster : transmission, item 12.
- **Réglages** :
  - `git ls-files .claude` → deux agents et `launch.json` ; aucun `settings.json` suivi ;
  - `.claude/settings.local.json` est ignoré par le gitignore global de l'utilisateur (mesuré, `git check-ignore -v`) et ne porte qu'une clé de modèle, `advisorModel` = `claude-fable-5-1`.
- **Exemptions** : aucun `.claude/model-exceptions.txt`, et aucune ligne `model` annotée d'un ADR dans l'arbre à `fb089dc`.
- **Frontmatters réels** :
  - `shogen-devops.md` : l.1-13, `model: claude-opus-5-5` l.10 ;
  - `shogen-orchestrator.md` : l.1-15, `model: claude-fable-5-1` l.12 ;
  - les deux portent une `description: >-` pliée sur plusieurs lignes indentées ; celle de l'orchestrateur cite `claude-fable-5-1` dans sa prose ;
  - sha256 de référence des copies : devops `d44a2211…518ac`, orchestrateur `e66873b3…0fcac` (commande en CA-D8a-12).

### 5.4 Faits [lu] qui contraignent la conception (paraphrasés)

Source : pages Claude Code du §4, lues le 2026-09-30.

- **(a) Découverte des agents.** Les sous-agents de projet sont découverts dans **chaque** `.claude/agents/` rencontré en remontant du répertoire courant jusqu'à la racine du dépôt, et chaque dossier est parcouru récursivement.
  - Conséquence dure : une copie de fixture placée sous un chemin `.claude/agents/` du dépôt serait chargée comme agent réel. Un cas négatif (banni, tier nu) le serait aussi, par tout agent dont le répertoire courant est en dessous.
  - Les fixtures vivent donc sous `enforcement/tests/fixtures/model-pinning/`. Le runner ne crée `.claude/agents/` que dans des dossiers `mktemp`, hors du dépôt (CA-D8a-3).
- **(b) Champ `model` d'un sous-agent** : un alias, un identifiant complet ou `inherit`. S'il est omis, le modèle suit l'ordre de résolution, qui aboutit au modèle de la conversation principale : c'est l'héritage. Un paramètre `model` passé à l'invocation **prime** sur le frontmatter.
- **(c) Variables d'environnement.** `CLAUDE_CODE_SUBAGENT_MODEL` est un défaut ; avec `CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1`, il s'impose à tout sous-agent, coéquipier et agent de workflow. Les variables `ANTHROPIC_DEFAULT_{OPUS,SONNET,HAIKU,FABLE}_MODEL` redirigent les alias.
- **(d) Suffixe `[1m]`.** Un alias de famille peut résoudre vers le modèle exact de la conversation principale, suffixe `[1m]` compris : c'est ce qui explique la forme résolue du JOURNAL l.86.
  - Sur l'API Anthropic, Fable 5.1, Sonnet 5 et suivants, et Opus 4.7 et suivants tournent nativement avec la fenêtre de 1 M. Aucune variante `[1m]` n'est à choisir pour eux.
  - Le suffixe s'accole à un alias ou à un nom complet, et Claude Code le lit quelle que soit la casse.
- **(e) Liste blanche de plateforme.** `availableModels` s'applique au frontmatter des sous-agents, au paramètre `model` de l'outil Agent, à `CLAUDE_CODE_SUBAGENT_MODEL`, aux skills et à `advisorModel`.
  - Par défaut, une entrée permet aussi les versions ultérieures qui la prolongent : l'exemple de la page est `claude-opus-5`, qui permet Opus 5.5.
  - `deniedModels` et `availableModelsMatch` (valeur `exact`) ne se lisent que dans les réglages gérés, à partir de la v2.1.283.
  - Une valeur bloquée d'un sous-agent est **substituée** par un modèle de repli ; elle n'est pas refusée. L'avertissement n'apparaît qu'en session interactive.

## 6. Choix tranchés (option retenue, motif, test)

- **CH-1 — Liste blanche exacte.** `ALLOWED` = `claude-opus-5-5 claude-sonnet-5-5 claude-fable-5-1`. La comparaison est sensible à la casse, octet pour octet, après la normalisation syntaxique de CH-8. Tout le reste sort en 2.
  - Motifs : CB-10 ; CP1-BIS l.89 (la règle de préfixe accepterait `claude-opus-5-50`) ; delta mesuré au §5.2 ; roster (`CLAUDE.md` l.20-31) ; précédent MONARK (`lint.mjs` l.54).
  - Rejetée : la règle « `claude-opus-5` suivi de tout autre chose que `-5` » (C-14 l.98), satisfaite par construction mais non exacte.
  - Tests : T-01..T-17.
- **CH-2 — La liste vit dans le script**, sur une ligne, avec ses décisions (133/267/280, `CLAUDE.md` l.20-31). La changer demande un lot.
  - Motifs : précédent MONARK (constante `TIERS`, item ROSTER-TIERS-SONNET-5-5-1 : `FAITS-sonnet-5-5` l.26) ; un point de modification unique.
  - Couplage auto-contrôlé dans un sens : un agent passé à un modèle neuf rougit g1 tant que la liste n'est pas amendée. L'autre sens (roster changé, liste oubliée) relève de l'item 7 (avis Q8, risque l.103).
- **CH-3 — Diagnostics, contrat de test** : jetons ASCII sur stderr, format `REFUS (<jeton>) <fichier>[:<ligne>] : <valeur> — <motif>`. On appelle **base** la valeur mise en minuscules, puis privée d'un suffixe final `[…]`. Classement dans l'ordre, première règle vraie :
  1. liste blanche (égalité exacte sur la valeur, pas sur la base) → OK ;
  2. banni → `R-1/ban` : la base vaut l'identifiant banni ;
  3. tier nu → `R-1/tier-nu` : la valeur est dans `opus|sonnet|haiku|fable|inherit|default|opusplan`, sans casse (canonique l.39) ;
  4. retiré → `R-1/retire` : la base vaut `claude-sonnet-5` (D8a-2) ;
  5. suffixe → `R-1/suffixe` : la valeur contient `[`, et ce qui précède le premier `[` est exactement dans la liste blanche (D8a-2) ;
  6. `R-1/hors-liste`.
  Autres jetons : `R-1/cle-model` (CH-7), `R-1/vide` (CH-11), `R-1/workflow` (CH-9, D8a-2). **Le jeton ne change pas le verdict** : tout refus sort en 2. Succès sur stdout : `OK (R-1) : <n> fichier(s) ; liste blanche : …`.
- **CH-4 — Cas limite `claude-opus-5-5[1m]`.**
  - En frontmatter et en réglages : **refusé**, `R-1/suffixe`. Motifs :
    - CB-10 ;
    - les modèles admis tournent nativement avec 1 M (§5.4 d) : le suffixe n'apporte rien à un épinglage ;
    - les identifiants catalogue lus en page primaire n'en portent pas (`FAITS-opus-5-5` l.7, `FAITS-sonnet-5-5` l.6) ;
    - Claude Code le lit quelle que soit la casse (§5.4 d) : l'admettre exigerait une règle de casse.
  - En journal de modèle résolu (JOURNAL, journaux G1/G2, champ `auteur` d'un enregistrement d'oracle) : **admis**, sous la seule forme `<id admis>` ou `<id admis>[1m]`, par égalité exacte, **jamais par un test de préfixe**. Motif : la forme résolue suit le modèle de la conversation principale (§5.4 d ; JOURNAL l.86 et l.92 montrent les deux formes).
  - D8a n'a aucun consommateur pour ce contrôle de journal : il n'en construit pas le mode, qui serait une pièce non branchée. La mécanisation relève de l'item 1.
  - Tests : T-13 (frontmatter), T-42 (réglages).
- **CH-5 — Cas limite `claude-sonnet-5`.** **Refusé**, `R-1/retire`, jamais `R-1/ban`.
  - Motifs : décision 280, retiré mais non banni (`FAITS-sonnet-5-5` l.24) ; CB-10 ; précédent MONARK (`lint.mjs` l.54, l.178 : admis seulement en rejeu `--rev`). Le lint Shōgen n'a pas de mode rejeu, il lit l'arbre courant.
  - Le jeton garde la distinction de procédure : la réadmission demande une décision de roster et un lot ; une dérogation au bannissement n'appartient qu'au mainteneur.
  - Test : T-14, avec la sortie 2, `R-1/retire` et l'absence de `R-1/ban`.
- **CH-6 — Les deux routes d'exemption sont supprimées** : l'annotation ADR sur la ligne, et `.claude/model-exceptions.txt`. Un tel fichier, s'il existe, n'est pas lu et ne débloque rien.
  - Motifs :
    - C-14 liste les refus sans exemption (l.98) ;
    - la règle globale interdit tout tier nu ;
    - le tier nu `opus` a été mesuré résolvant vers le banni le 2026-08-05 (canonique l.4-6) : une exemption rouvrirait le bannissement ;
    - un alias peut résoudre vers le modèle de la conversation principale (§5.4 d) ;
    - aucune exemption n'est en usage (§5.3) ; environ 20 lignes en moins.
  - Tests : T-18, T-19, T-20.
- **CH-7 — Exactement une clé `model` de premier niveau par agent** (ligne non indentée).
  - Une clé absente, un fichier sans frontmatter, ou plusieurs clés sortent en `R-1/cle-model`. Motifs : absente, c'est l'héritage (§5.4 b ; règle globale « jamais l'héritage de session ») ; plusieurs, le modèle retenu dépend du lecteur YAML.
  - Une ligne `model:` indentée (dans une description pliée ou une table imbriquée) ne compte pas, mais sa valeur est contrôlée ; c'est le comportement du canonique, fail-closed.
  - Les skills n'ont pas de règle de compte : un skill n'est pas un lancement d'agent [inféré].
  - Tests : T-21..T-24.
  - *Amendement du 2026-09-30 (correction de la revue G2, C-2 et C-3)* : la règle de compte ne s'applique qu'aux fichiers situés sous un `.claude/agents/` (lettre de CH-7 tenue : T-53, T-54). Les formes YAML hors du sous-ensemble lu ligne à ligne sont refusées : clé non nue en colonne 0 (guillemets, `?`, ancre `&`, étiquette `!`, alias `*`, flux `{`, clé de fusion `<<`) et frontmatter indenté, en `R-1/cle-model` ; clé `model` comptée seulement si les deux-points sont suivis d'un blanc ou de la fin de ligne ; première ligne non vide indentée, hors commentaire, après la clé `model`, en `R-1/hors-liste` ; frontmatter ouvert et non fermé, en `R-1/cle-model`. Les indicateurs au-delà de `"`, `'` et `?`, et le frontmatter indenté, sont un ajout du correcteur : C-2 ouvrait ces formes sur les skills (mesure au journal G1 §15). Tests : T-55..T-59, T-62, T-65..T-74.
- **CH-8 — Normalisation syntaxique** :
  - BOM de la ligne 1 retiré (canonique l.52-58) ;
  - CR final retiré ;
  - une seule paire de guillemets, **appariée**, retirée ;
  - un commentaire n'est retiré que s'il est précédé d'un blanc (` #…`) ;
  - blancs finaux retirés.
  La règle exacte de YAML sur `#` n'a pas été lue. Le choix est fail-closed dans les deux cas : `claude-opus-5-5#x` garde son `#x`, n'est pas dans la liste blanche, et sort en 2. Tests : T-27..T-36.
- **CH-9 — Scripts de workflow (option de la mission) : fil de déclenchement, pas de scan complet.**
  - Motifs : 0 script suivi ou présent (§5.3) ; mais le paramètre `model` à l'invocation prime sur le frontmatter (§5.4 b), si bien qu'un script versionné serait une vraie surface d'épinglage.
  - Retenu, en D8a-2 : tout `*.js`, `*.mjs` ou `*.cjs` sous la racine qui contient un appel `agent(` sort en `R-1/workflow` (« script non couvert, item 2 »). Motif proposé : `grep -lE '(^|[^A-Za-z0-9_$.])agent[[:space:]]*\('`, pour ne pas prendre `useragent(` ni `x.agent(`. Élagage : `target/`, `.git/`, `.claude/worktrees/`, `node_modules/`, `biblio/`, `fuzz/target/`, `mutants.out*` (268 ms mesurés ; le hook D8c le paiera à chaque commit).
  - Le déclencheur de l'item 2 devient mécanique. Coût : environ 4 lignes et 2 cas (T-43 rouge, T-44 un `.js` sans `agent(` qui passe).
  - Rejeté : l'OUT pur (déclencheur de processus seulement). Détachable : si D8a-2 dépasse le seuil, le fil passe à l'item 2.
- **CH-10 — Réglages JSON.**
  - Clés `model` et `advisorModel` conservées (canonique l.89-122), sous la liste blanche.
  - Le JSON est **aplati** (retours de ligne remplacés) avant l'extraction. Cela lève la limite déclarée l.84-88 (clé et valeur sur deux lignes) pour environ 0 ligne.
  - Clés d'environnement (§5.4 c) : hors lot, item 3. Aucun réglage n'est suivi (§5.3).
  - Tests : T-37..T-42.
  - *Amendement du 2026-09-30 (correction de la revue G2, C-4)* : un réglage dont une clé porte une barre oblique inverse sort en `R-1/hors-liste` : un échappement peut former `model` ou `advisorModel`. Test : T-60.
- **CH-11 — Aucun vert par absence** : 0 fichier dans la portée sort en `R-1/vide`.
  - C'est un écart nommé au canonique (l.138-139), qui déclarait cette limite. Règle PAROXYSME : lever plutôt que déclarer.
  - Dans Shōgen, l'entrée du tuyau existe (2 agents suivis) : sa disparition doit rougir. Test : T-26.
  - *Amendement du 2026-09-30 (correction de la revue G2, C-6 ; décision de l'orchestrateur, portée par sa commande de correction)* : la lettre « 0 fichier dans la portée » devient « aucun agent lu », quels que soient les réglages ; le motif est inchangé. Tests : T-26, T-61 ; rejeu `vide-local` au journal G1 §15.
- **CH-12 — Portée** :
  - frontmatter seul, le corps n'est pas lu (canonique l.10-12) ;
  - `.claude/agents/**` et `.claude/skills/**` parcourus récursivement, comme la découverte (§5.4 a) ;
  - `.claude/worktrees/` hors portée (hors de `ROOT/.claude/agents`) ;
  - `launch.json` non lu (aucune clé de modèle : git-ci l.115).
  - Test : T-25.
  - *Amendement du 2026-09-30 (correction de la revue G2, C-1)* : la passe du frontmatter lit tout `*.md` situé sous un `.claude/agents/`, un `.claude/skills/` ou un `.claude/commands/` de l'arbre, à toute profondeur, avec l'élagage de la passe 3, factorisé (`ELAG`). Les skills imbriqués et les commandes reposent sur la lecture du réviseur G2 (Firecrawl, 2026-09-30), confirmés par les FAITS lus sur place par l'orchestrateur le 2026-09-30 (`FAITS-claude-code-skills-commandes-2026-09-30.md`, dossier du lot) ; le sens est fail-closed. Tests : T-50..T-52, T-63, T-64, T-75, T-76.
- **CH-13 — Invariant de littéral redéfini** : sous `enforcement/`, aucun jeton `claude-opus-5` qui ne soit pas suivi de `-5` (motif du §5.3). Toute valeur dérivée du banni se construit à l'exécution par concaténation (pratique de l'amont, runner l.21-27). Oracle : O-5.
- **CH-14 — Fixtures.** Copies octet pour octet des frontmatters réels à `fb089dc`, jamais sous un chemin `.claude/agents/` (§5.4 a).
  - Chaque cas copie une fixture dans un arbre `mktemp`, puis remplace la ligne `model` de la copie.
  - Fidélité contrôlée par sha256 (O-9).
  - Aucune ligne de provenance n'est ajoutée dans la copie, pour qu'elle reste identique. La provenance va dans l'en-tête du runner.
- **CH-15 — Job g1** :
  - id = name = `g1-model-pinning` (règle d'un seul nom, `gates.yml` l.60), et non le `g1-pinned-models` canonique ;
  - `runs-on: ubuntu-24.04` (l.62-67 ; SHOGEN-CI-RUNNERS-1, annexe B l.80) ;
  - `actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # tag v7.0.1` (l.77), et non le v4.4.0 canonique ;
  - `persist-credentials: false` ; `shell: bash` ; `timeout-minutes: 5` (le G1 mesure le temps local) ;
  - étape 1 : le runner ; étape 2 : `bash enforcement/lint-model-pinning.sh .` ;
  - aucune action ni installation neuve (R-8) ;
  - en-tête l.3-19 : g1 nommé.
- **CH-16 — Texte du lint** :
  - messages en français, jetons ASCII ;
  - en-tête qui cite les pièces suivantes :
    - blob `457565f`, soit VibeGates `0b4f3f9` ;
    - ADR-0028 D8, C-14, et CB-10 ;
    - décisions 133/267/280 ;
    - bannissement du 2026-08-14 (`docs/DECISIONS.md` l.2965-2968).
  - **aucune mention** de R-4 (c'est l'effort, doc 02 l.83, que ce lint ne contrôle pas), du jumeau `.ps1` ni des exemptions.
- **CH-17 — Ce que D8a ne revendique pas.** Le lint contrôle le texte des épinglages versionnés. Il ne contrôle pas le modèle qui tourne : paramètre d'invocation, variables d'environnement, réglages hors dépôt, substitution par la plateforme.
  - Le contrôle R-1 au lancement reste obligatoire.
  - Limites avec items : 1, 3, 4, 5.

## 7. Table des cas (contrat du runner ; sortie attendue, jeton)

Notation : B = identifiant banni construit à l'exécution. D = copie de la fixture devops, O = copie de la fixture orchestrateur, ligne `model` remplacée.

| id | arbre | attendu | sous-lot |
|---|---|---|---|
| T-01 | O telle quelle | 0 | D8a-1 |
| T-02 | D telle quelle | 0 | D8a-1 |
| T-03 | D, `claude-sonnet-5-5` | 0 | D8a-1 |
| T-04..T-06 | D, `opus` / `fable` / `sonnet` | 2 `R-1/tier-nu` | D8a-1 |
| T-07 | D, B | 2 `R-1/ban` | D8a-1 |
| T-08 | D, B`[1m]` | 2 `R-1/ban` | D8a-1 |
| T-09..T-12 | D, B`x`, B`0`, B`-0`, B`-50` | 2 `R-1/hors-liste` | D8a-1 |
| T-13 | D, `claude-opus-5-5[1m]` | 2 ; le runner de D8a-1 attend `R-1/hors-liste`, D8a-2 change l'attendu en `R-1/suffixe` | D8a-1 |
| T-14 | D, `claude-sonnet-5` | 2, jamais `R-1/ban` ; le runner de D8a-1 attend `R-1/hors-liste`, D8a-2 change l'attendu en `R-1/retire` | D8a-1 |
| T-15 | D, `claude-opus-4-8` | 2 `R-1/hors-liste` | D8a-1 |
| T-16 | D, B en majuscules | 2 `R-1/ban` | D8a-1 |
| T-17 | D, `CLAUDE-OPUS-5-5` | 2 `R-1/hors-liste` | D8a-1 |
| T-18 | D, `fable   # ADR-0003` | 2 `R-1/tier-nu` | D8a-1 |
| T-19 | D, B`   # ADR-9999` | 2 `R-1/ban` | D8a-1 |
| T-20 | D telle quelle, `settings.json` `{"advisorModel": "fable"}`, `.claude/model-exceptions.txt` avec `advisorModel=fable ADR-0003` : la route canonique (l.114), sortie 0 au canonique | 2 `R-1/tier-nu` | D8a-1 |
| T-21 | D sans ligne `model` | 2 `R-1/cle-model` | D8a-1 |
| T-22 | D avec deux clés `model` admises | 2 `R-1/cle-model` | D8a-1 |
| T-23 | O plus une ligne indentée `  model: claude-opus-5-5` dans la description | 0 | D8a-1 |
| T-24 | O plus une ligne indentée `  model:` B | 2 `R-1/ban` | D8a-1 |
| T-25 | O, corps qui mentionne `model:` B | 0 | D8a-1 |
| T-26 | arbre vide | 2 `R-1/vide` | D8a-1 |
| T-27 | BOM plus D | 0 | D8a-1 |
| T-28 | BOM plus D, B | 2 `R-1/ban` | D8a-1 |
| T-29, T-30 | D, `"claude-opus-5-5"` ; O, `'claude-fable-5-1'` | 0 | D8a-2 |
| T-31 | D, `"claude-opus-5-5'` (guillemets non appariés) | 2 `R-1/hors-liste` | D8a-2 |
| T-32 | D, `claude-opus-5-5  # note` | 0 | D8a-2 |
| T-33 | D, `claude-opus-5-5#x` | 2 `R-1/hors-liste` | D8a-2 |
| T-34 | D, `model : claude-opus-5-5` | 0 | D8a-2 |
| T-35 | D en CRLF (construit à l'exécution) | 0 | D8a-2 |
| T-36 | D, valeur vide | 2 `R-1/hors-liste` | D8a-2 |
| T-37 | skill B, plus D | 2 `R-1/ban` | D8a-2 |
| T-38 | `settings.json` `advisorModel` `claude-fable-5-1`, plus D | 0 | D8a-2 |
| T-39, T-40 | `settings.json` puis `settings.local.json`, `model` B | 2 `R-1/ban` | D8a-2 |
| T-41 | `settings.json`, clé et valeur B sur deux lignes | 2 `R-1/ban` | D8a-2 |
| T-42 | `settings.json`, `model` `claude-opus-5-5[1m]` | 2 `R-1/suffixe` | D8a-2 |
| T-43 | D plus `wf.mjs` contenant `agent(` | 2 `R-1/workflow` | D8a-2 |
| T-44 | D plus `x.js` sans `agent(` | 0 | D8a-2 |

Chaque cas vérifie **la sortie ET le jeton**, et un cas « 0 » exige le message OK avec son compte de fichiers. Un seul résumé fait foi (règle de l'amont, l.29-31) : `model-pinning : <n> ok, <m> échec`. Sortie du runner : 0 si tout passe, 1 si un cas échoue, 3 en cas d'erreur fatale.

- *Amendement du 2026-09-30 (G1, règle 4 du §9)* : T-20 passe en D8a-2, avec la passe JSON (journal G1 §1). Cas ajouté par le G1, en D8a-2 : **T-45**, `settings.json` `{"model": null}` → 2 `R-1/hors-liste` (une clé `model` ou `advisorModel` dont la valeur n'est pas une chaîne n'épingle rien ; conformité à CH-1, tout ce qui n'est pas exactement dans la liste sort en 2). Table exécutée : 27 cas en D8a-1, 45 en D8a-2.
- *Amendement du 2026-09-30 (correction de la revue G2, C-5 et C-8)* : cas T-46..T-64 de la revue G2, puis T-65..T-76 du correcteur (C-3 élargi, gardes contre le refus de formes valides, C-1 hors de la racine) ; table et lecture de référence au journal G1 §15. Table exécutée : 76 cas.

## 8. Oracles non-LLM nommés

- **O-1 — Runner.** `TMPDIR=F:/tmp/shogen-tests-tmp bash enforcement/tests/run-fixtures-model-pinning.sh` → sortie 0, `<n> ok, 0 échec`, où n est le nombre de cas du §7 retenus dans le (sous-)lot.
- **O-2 — Arbre réel.** À la racine du worktree : `bash enforcement/lint-model-pinning.sh .` → sortie 0, 2 fichiers. Sur l'arbre de travail principal, l'orchestrateur attend 3 fichiers (`settings.local.json` local). Même commande que l'étape 2 du job.
  - *Amendement du 2026-09-30 (fait mesuré au G1)* : le worktree créé par le harnais porte lui aussi un `.claude/settings.local.json` ignoré (même taille et même mtime que celui de l'arbre principal ; `advisorModel` = `claude-fable-5-1`). O-2 y lit donc 3 fichiers. La forme du checkout de la CI (copie `git archive`, fichiers suivis seuls) lit 2 fichiers : cas k=0 ajouté à O-3.
- **O-3 — Rouge semé sur l'entrée réelle** (CA-11 durci).
  - Préparation : `git archive <gel> .claude | tar -x -C F:/tmp/shogen-lots/D8a/oracles/rouge-<k>/`, puis, sur **la copie**, la ligne `model` de `shogen-devops.md` est remplacée par (k=1) B construit à l'exécution, (k=2) `claude-sonnet-5`, ou (k=3) supprimée.
  - Attendu : sortie 2 avec `R-1/ban` (k=1), `R-1/retire` (k=2, jeton de D8a-2 ; `R-1/hors-liste` si D8a-1 est jugé seul) et `R-1/cle-model` (k=3). La composition part de l'artefact d'entrée committé, jamais d'une forme reconstruite à la main.
  - *Amendement du 2026-09-30 (G1)* : k=0, la copie non modifiée → sortie 0, 2 fichiers (forme du checkout de la CI). `<gel>` = la base consignée au journal G1 (`aa0afdc`).
- **O-4 — Mutants de gate** (tests négatifs d'outil ; registre d'ADR-0011 pt 4, `docs/09-vocabulaire.md` l.41).
  - Ils s'appliquent sur des copies du lint sous `F:/tmp/shogen-lots/D8a/oracles/`, et le runner est lancé avec le chemin du mutant en `$1`.
  - Chaque mutant doit faire sortir le runner en ≠ 0, le cas tueur nommé en rouge. Le script de mutation vit hors du dépôt (précédent de B0, §5 de son journal).

  | mutant | tué par |
  |---|---|
  | M-1 le verdict accepte tout | T-04..T-22 |
  | M-2 B ajouté à `ALLOWED` | T-07 |
  | M-3 égalité remplacée par un préfixe | T-12, T-13 |
  | M-4 comparaison sans casse | T-17 |
  | M-5 suffixe non retiré pour le jeton `ban` | T-08 (jeton) |
  | M-6 minuscules non appliquées pour `ban` | T-16 (jeton) |
  | M-7 jeton `retire` retiré | T-14 (D8a-2) |
  | M-8 jeton `suffixe` retiré | T-13, T-42 (D8a-2) |
  | M-9 règle de compte retirée | T-21, T-22 |
  | M-10 lignes indentées comptées | T-23 |
  | M-11 BOM non retiré | T-27, T-28 |
  | M-12 CR non retiré | T-35 |
  | M-13 guillemets non retirés | T-29, T-30 |
  | M-14 commentaire sans blanc requis (`s/#.*$//`) | T-33 |
  | M-15 JSON non aplati | T-41 |
  | M-16 `settings.local.json` retiré | T-40 |
  | M-17 `.claude/skills` retiré | T-37 |
  | M-18 vide rendu vert | T-26 |
  | M-19 fichier lu en entier | T-25 |
  | M-20 exemption ADR réintroduite (`grep -v ADR-`) | T-18 |
  | M-21 fil de workflow retiré | T-43 (D8a-2) |

  F2P : le runner et le lint sont absents de la base, donc tous les tests sont neufs (catégorie « nouveau module »), à déclarer comme tels.
  - *Amendement du 2026-09-30 (correction de la revue G2, C-8)* : campagne rejouée sur le lint corrigé : M-1..M-22 (M-10, M-17, M-18 et M-19 redérivés), MG-01..MG-18 (MG-18 redérivé), MP-01..MP-17 (redérivés) et MC-01..MC-16 ; résultats au journal G1 §15.
  - *Amendement du 2026-09-30 (G1)* : M-22, le refus des valeurs non chaînes retiré, tué par T-45. Avec la coupe du journal G1 §1, M-15, M-16 et M-22 sont des mutants de D8a-2 (code et tueur dans le même sous-lot) ; M-12, M-13, M-14 et M-17 restent de code D8a-1 et de tueur D8a-2, et survivent à l'état D8a-1 seul (déclaré, mesuré).
- **O-5 — Invariant de littéral** (CH-13) : 0.
- **O-6 — Compatibilité g5.** Le motif courant (`gates.yml` l.48) et le motif élargi que portera D8c (`adb2213:gates.yml` l.39) rendent 0 occurrence dans les lignes ajoutées sous `enforcement/` et dans le diff de `gates.yml`.
- **O-7 — Non-régression** :
  - `cargo --locked xtask verify` VERT, qui couvre le journal G1 (S-G4, S-G5, S-G8) ;
  - `(cd s2-harness && python -B -m unittest discover -s tests -t .)` : compte et sauts identiques à la base, mesurés avant et après (D8a ne touche pas `s2-harness/`) ;
  - environnement : `CARGO_HOME` et `CARGO_NET_OFFLINE=true` de la mission, `TMPDIR` sur `F:/tmp/shogen-tests-tmp`.
  - *Amendement du 2026-09-30 (cp-1 C-7)* : la base de la comparaison est le sha consigné au journal G1 (`aa0afdc`, `main` au lancement), et non `fb089dc`.
- **O-8 — TMP** : 0 entrée neuve dans `F:/tmp/shogen-tests-tmp` après O-1, mesurée par comptes avant et après (précédent de SHOGEN-TESTS-TMP-1).
  - *Amendement du 2026-09-30 (G1)* : le dossier partagé porte des écrivains concurrents (vague 2) ; le compte se fait sur un TMP **neuf** par exécution, sous `F:/tmp/shogen-tests-tmp/d8a-g1/`, vide avant et compté après.
- **O-9 — Fidélité des fixtures.** sha256 de chaque fixture = sha256 de `git show fb089dc:.claude/agents/<nom> | sed -n '1,<13|15>p'` (valeurs de référence au §5.3).
- **O-10 — Syntaxe YAML de `gates.yml`** : non prouvable en local. Aucun lecteur YAML dans la bibliothèque standard, aucune installation (R-8). Couverture : lecture au G2 contre le bloc de CH-15, puis item 8 (c).
  - *Amendement du 2026-09-30 (cp-1 C-6), qui supplante la puce ci-dessus* : la syntaxe de `gates.yml` est contrôlée en local par `yaml.safe_load` (PyYAML 6.0.3, YAML 1.1) ; la lecture de la forge n'est pas mesurée (item 8 c). PyYAML est déjà présent dans le Python local 3.14.5 (mesuré ; aucune installation, R-8 intact). Le même oracle compare la structure à celle de la base : jobs de la base inchangés, un seul job neuf, bloc g1 conforme à CH-15. Il ne reste à l'item 8 (c) que la sémantique de la forge.
- **Enregistrement.** Le G1, puis le G2 par ses propres commandes, produisent un enregistrement d'oracle substitut, au format de CI-S2 (annexe B l.79) et avec les champs de D6 (viii) (ADR-0028 l.85). Chemin : `F:/tmp/shogen-lots/D8a/oracles/oracle-<rôle>-D8a-substitut.json`, avec les commandes, les sorties, leurs sha256 et les codes de sortie.

## 9. Estimation R-25 (ascendante, par fichier ; [inféré] sauf mention)

| fichier | D8a-1 | D8a-2 | base de l'estimation |
|---|---|---|---|
| `enforcement/lint-model-pinning.sh` | ≈ 85 | ≈ +7 (jetons `retire` et `suffixe`, fil de workflow) | en-tête ≈ 16, réglages ≈ 7, verdict ≈ 14, passe frontmatter ≈ 26, passe JSON ≈ 10, fin ≈ 7 ; canonique 143 [mesuré], dont 20 lignes d'exemptions supprimées (CH-6) |
| `enforcement/tests/run-fixtures-model-pinning.sh` | ≈ 75 | ≈ +20 | outillage ≈ 47 (en-tête, `mktemp`, `trap`, constructeurs, assertion) ; une ligne par cas : T-01..T-28, puis T-29..T-44 |
| fixtures (2 copies) | 28 [mesuré : 13 + 15] | 0 | frontmatters du §5.3 |
| `.github/workflows/gates.yml` | 0 | ≈ 24 | bloc de CH-15 ≈ 21, en-tête ≈ 3 (CI-S2 : `gates.yml` +57 −5 pour un job plus un en-tête, `19db9d9`, mesuré par `git show --stat`) |
| **total** | **≈ 188** | **≈ 51** | lot entier ≈ 239 > 200 : coupe prévue |

- **Documentation** : le journal `docs/G1-lot-D8a.md` est **hors compte**, selon le précédent (`docs/G1-lot-B0-pool-analyse.md` l.30 et l.225). La mission écrit « compte tout de même » pour le texte de G0/ADR ; la lecture est ambiguë. Le G1 publie les deux comptes, avec et sans journal (Q-G0-1).
- **Marge d'erreur** : B0 avait estimé 193 lignes et en a mesuré 252 (+30 %, sous-estimation des tests ; journal B0 l.20-21). La coupe est donc décidée d'avance, ce qui évite de l'improviser (FM-1.5).
- **Règle de coupe** (méthode de mesure du lot A : `git diff --numstat` des fichiers suivis, `wc -l` des fichiers neufs, estimation écrite avant tout code) :
  1. total ≤ 200 : un seul lot ;
  2. sinon, deux sous-lots :
     - **D8a-1** : lint, fixtures, runner avec T-01..T-28. Il couvre C-14, la suppression des exemptions et les invariants canoniques ;
     - **D8a-2** : job g1, en-tête, jetons `retire` et `suffixe`, fil de workflow, T-29..T-44.
  3. si D8a-1 dépasse encore 200 : T-23..T-28 passent en D8a-2 (les cas seulement, pas le code) ;
  4. si D8a-1 dépasse toujours : **arrêt et consultation formée** (R-26). On ne comprime jamais le lint en retirant des contrôles.
- Chaque sous-lot reçoit sa ligne datée à l'annexe A (acte de l'orchestrateur, ADR-0028 l.188). Lignes proposées, au format des colonnes de l'annexe A (précédent : `docs/G1-lot-B0-pool-analyse.md` l.31-33), à coller si le G1 confirme la coupe :

| lot (date) | objet (décision) | véhicule | oracle non-LLM nommé | taille estimée (R-25) | tuyau (entrée → sortie → consommateur ; test) | cp-1 |
|---|---|---|---|---|---|---|
| **D8a** (2026-09-30, amendement daté du G0) | D8, C-14, CB-10 : lint en liste blanche exacte, job g1, cas limites tranchés (CH-4, CH-5) ; ligne l.22 amendée | `enforcement/`, `gates.yml`, tests shell | O-1 à O-9 de ce G0 ; 21 mutants de gate | ≈ 239 [inféré, bases du §9] au lieu de ≈ 205 ; coupe prévue en D8a-1 et D8a-2 | `.claude/agents/*.md` → lint → job g1 (partiel : GC-01, GC-09) ; hook : item 9 ; test O-2 et O-3 | complet |
| **D8a-1** (2026-09-30, coupe R-25 du G0 de D8a) | lint (liste blanche, jetons `ban`, `tier-nu`, `hors-liste`, `cle-model`, `vide`), fixtures, cas T-01..T-28 | `enforcement/lint-model-pinning.sh`, `enforcement/tests/run-fixtures-model-pinning.sh`, `enforcement/tests/fixtures/model-pinning/` | O-1, O-3 (k=1, k=3), O-4 (M-1..M-6, M-9..M-11, M-18..M-20), O-5 à O-9 | ≈ 188 [inféré : 85 + 75 + 28 mesuré] | non branché seul : consommable au G7 avec D8a-2 | complet (sous le cp-1 du lot) |
| **D8a-2** (2026-09-30, coupe R-25 du G0 de D8a) | job `g1-model-pinning`, en-tête de `gates.yml`, jetons `retire`, `suffixe` et `workflow`, cas T-29..T-44 | `.github/workflows/gates.yml`, les deux scripts | O-1, O-2, O-3 (k=2), O-4 (M-7, M-8, M-12..M-17, M-21), O-5 à O-8 | ≈ 51 [inféré : 24 + 7 + 20] | lint → job g1 ; test O-2 | complet (sous le cp-1 du lot) |

- Conséquence de la coupe, à lire par le G2 : le code que visent M-12 à M-17 (CR, guillemets, commentaire, aplatissement JSON, `settings.local.json`, skills) est écrit en D8a-1, mais ses cas tueurs sont en D8a-2. D8a-1 n'est donc ni branché ni entièrement tué seul ; les deux sous-lots se revoient ensemble au même G2, comme B0-1 et B0-2 (commit unique `0abc881`).
- **D8a-1 seul n'est pas branché**, faute de consommateur : il ne passe au G7 qu'avec D8a-2 (précédent de B0-2).
- *Amendement du 2026-09-30 (G1, règle 4 appliquée)* : D8a-1 selon la coupe ci-dessus mesure 213 lignes, et 207 après la règle 3. Règle 4 : arrêt et consultation formée (advisor, canal 1, 2026-09-30 vers 05:26Z). Coupe retenue sur la frontière de la passe JSON : le code de CH-10, avec le refus des valeurs non chaînes, et T-20 passent en D8a-2 ; T-23..T-28 restent en D8a-1. Mesures : **D8a-1 = 193**, **D8a-2 = 93** (journal G1 §1). Aucun contrôle retiré ; les deux sous-lots se revoient au même G2. Lignes datées proposées pour l'annexe A : journal G1 §1 (C-4), qui remplacent les deux lignes ci-dessus.

## 10. Tuyaux (CA-11 durci)

| rôle | objet | état |
|---|---|---|
| entrée | `.claude/agents/**/*.md` : 2 fichiers suivis, produits par les commits de roster de l'orchestrateur | présent |
| entrée | `.claude/skills/**/*.md` et `.claude/settings.json` | absents |
| entrée | `.claude/settings.local.json` | ignoré, local seulement |
| sortie | code de sortie 0 ou 2 ; jetons sur stderr | à construire |
| consommateur 1 | job `g1-model-pinning` (étapes O-1 et O-2) | **partiel déclaré**, comme CI-S2 : forge morte (GC-01), aucun `required_status_checks` (GC-09). G3 opérant = rejeu local des deux commandes du job par l'orchestrateur (ADR-0028 §4.11 l.171). Item 8 |
| consommateur 2 | hook versionné (D8c), annoncé à l'annexe A l.22 | **absent** : le hook actuel ne lance aucun lint (`.git/hooks/pre-commit` l.53-77). Item 9, déclencheur G0 de D8c |
| état | aucun (lint sans état) ; la liste blanche vit dans le script (CH-2) | — |
| test de composition | O-2 : artefact d'entrée committé → lint → sortie 0 ; O-3 : copie de ce même artefact, une valeur changée → sortie 2 et jeton | l'exécution du job sur la forge relève de l'item 8 |

- *Amendement du 2026-09-30 (cp-1 C-5)* : pour que le consommateur local soit une étape listée et non une discipline, la liste des commandes du G3 opérant (ADR-0028 §4.11 l.171) reçoit, à partir du commit de D8a, les deux commandes du job g1. Le texte proposé est au journal G1 §7 ; l'amendement d'ADR-0028 est un acte de l'orchestrateur (ADR-0028 §8).

## 11. Items formés (règle Dettes et PAROXYSME)

| # | item | objet | propriétaire | déclencheur | origine |
|---|---|---|---|---|---|
| 1 | SHOGEN-R1-FORME-RESOLUE-1 | mécaniser la règle « journal » de CH-4 (égalité exacte avec `<id>` ou `<id>[1m]`) là où s'écrit le modèle résolu : champ `auteur` de `shogen.oracle-record.v1`, ligne « Modèle » des journaux G1/G2 | orch. | G0 de RENDU-2 | CB-10 ; CH-4 ; ADR-0028 l.85 |
| 2 | SHOGEN-LINT-WORKFLOW-1 | scan des scripts de workflow : valeurs littérales sous la liste blanche, valeur non littérale refusée, `model:` dans un commentaire, paramètre d'invocation prioritaire (§5.4 b) | orch. | le jeton `R-1/workflow` sort (premier script versionné qui contient `agent(`) | option de la mission ; CH-9 |
| 3 | SHOGEN-LINT-ENV-MODEL-1 | clés d'environnement des réglages JSON : `CLAUDE_CODE_SUBAGENT_MODEL` (et `_FORCE`), `ANTHROPIC_MODEL`, `ANTHROPIC_DEFAULT_{OPUS,SONNET,HAIKU,FABLE}_MODEL`, sous la liste blanche | orch. | premier `.claude/settings.json` suivi, ou G0 de D8c (le hook lit les réglages locaux) | §5.4 c ; CH-10 |
| 4 | SHOGEN-ROSTER-PLATEFORME-1 | **recherche** de la construction qui couvre ce qu'un lint textuel ne voit pas (CH-17) : réglages gérés `availableModels` + `availableModelsMatch` (`exact`) + `enforceAvailableModels` + `deniedModels` (voir la note sous la table) | recherche : orch. ; décision : investisseur (configuration de la machine) | maintenant (recherche sans code) ; décision au prochain point d'étape | PAROXYSME (CH-17) ; §5.4 e |
| 5 | SHOGEN-LINT-HORS-DEPOT-1 | agents globaux (`F:/claude-config/agents/*.md` : worker, lecteur, chercheur…) et réglages utilisateur, hors de portée d'un lint de dépôt ; proposer un passage du lint sur ces dossiers dans le hook ou à la cartographie | orch. (proposition) ; investisseur (configuration globale) | G0 de D8c, ou prochaine décision de roster | §5.4 a ; CH-17 |
| 6 | SHOGEN-LINT-EFFORT-1 | effort explicite par palier : l'effort par défaut d'Opus 5.5 est `medium` (`FAITS-opus-5-5` l.20 ; `CLAUDE.md` l.21-22). Le canonique cite R-4 (l.2) sans rien contrôler de l'effort | orch. | prochain lot de roster, ou G2 de D8a s'il le juge dans C-14 | canonique l.2 ; doc 02 l.83 |
| 7 | SHOGEN-LINT-ROSTER-SYNC-1 | dérive entre `ALLOWED` et le roster (`CLAUDE.md` l.20-31 et règle globale) : chaque décision de roster ouvre un lot qui amende `ALLOWED` ; la cartographie de clôture compare les deux listes | orch. | prochaine décision de roster | avis Q8, risque l.103 ; CH-2 |
| 8 | SHOGEN-G1-FORGE-1 | (a) `g1-model-pinning` aux `required_status_checks` (GC-09) ; (b) première exécution sur la forge (GC-01) ; (c) ce que l'oracle local ne prouve pas : `awk` de l'image (Git Bash local : GNU Awk 5.4.1 [mesuré] ; Ubuntu : mawk [inféré, non mesuré]) pour `[[:space:]]`, `sed` GNU et `\xEF`, `find`, `mktemp`, syntaxe YAML telle que la forge la lit | orch. | forge rétablie (§4.1) | modèle : SHOGEN-CI-S2-FORGE-1 (annexe B l.78) ; O-10 |
| 9 | SHOGEN-D8-HOOK-LINT-1 | le hook versionné de D8c lance ce lint (consommateur 2) | orch. | G0 de D8c | annexe A l.22 ; §10 |
| 10 | SHOGEN-BIBLIO-CLAUDE-CODE-1 | verser à `biblio/` (entrées `INDEX.md`, compte S-G6) les deux pages Claude Code lues le 2026-09-30 | orch. ; le versement est un téléchargement : go requis, règle « lecture sur place » | avant le journal G1 s'il cite ces pages entre guillemets ; sinon au prochain versement | S-G5 ; §4 |
| 11 | SHOGEN-D8-AMONT-ERRATUM-1 | erratum : l'amont VibeGates est retrouvé (§5.1). Il corrige git-ci §2.b l.118, D8 l.95 et l'annexe E l.30 (source inchangée, provenance chaînée à `0b4f3f9`) ; transmissions D8b et D8c du §5.1. `error_origin` proposé, à assigner au G7 : worker de la dimension git-ci de la cartographie du 2026-09-29 (recherche limitée à `…\enforcement\` du corpus) | orch. | commit de D8a, ou avec SHOGEN-ERRATA-ADR0028-1 | §5.1 |
| 12 | CORPUS-GABARIT-ROSTER-1 (transmission) | le gabarit `templates/workflow-passe-agilegates.js` du corpus épingle `claude-opus-4-8` (l.28-29, 137, 141), hors roster (décisions 133/267) | mainteneur du corpus ; transmission par l'orch. | prochaine passe du corpus | §5.3 |
| 13 | SHOGEN-CI-S2-SAUT-1 (reprise ; ligne ajoutée le 2026-09-30, cp-1 C-1) | construction de l'annexe B l.79 : le job `s2-harness-unittest` exige le résumé final (`Ran N` et `OK`), n'admet que les sauts dont le motif nomme `SHOGEN_S2_CAMPAGNE_CONTROL`, et borne N par un plancher committé ou par un manifeste des modules de test. **Non construite dans D8a-2**, alors que R-25 l'aurait permis (D8a-2 = 93 [mesuré] + ≈ 70 [inféré]). Motifs : le choix plancher ou manifeste revient à un G0 et ce G0 ne l'a pas tranché ; job et oracle distincts (rejeux R8, MT-5, MT-6, MT-7, MT-9) ; FM-2.3 | orch. | **sous-lot D8a-3** (2026-09-30) : G0 bref ouvert par l'orchestrateur au commit de D8a ; construction avant RENDU-1 ; ligne datée proposée pour l'annexe A au journal G1 §1 | annexe B l.79 ; cp-1 C-1 ; consultation advisor du G1 |

Note sur l'item 4 (questions ouvertes de la recherche) :
- (a) `deniedModels: [claude-opus-5]` bloque-t-il aussi `claude-opus-5-5` ? Par défaut, une entrée permet les versions qui la prolongent (§5.4 e) : risque de collision de préfixe au niveau de la plateforme.
- (b) Chemin des réglages gérés sous Windows : probablement sur C:, donc acte de l'investisseur.
- (c) La version installée de Claude Code est-elle ≥ v2.1.283 ?
- (d) Sémantique de substitution, et non de refus (§5.4 e), face à la doctrine fail-closed.
- (e) Effets de bord pour les modèles hors liste employés en interne par le harnais.
- Prix : 0 $ de configuration ; coût = un fichier géré et un rejeu R-1.

*Amendements du 2026-09-30 à la table ci-dessus* : item 8 (c), cp-1 C-6 : la syntaxe YAML sort de l'item (O-10 amendé) ; restent la sémantique de la forge et les outils de l'image (`awk`, `sed`, `find`, `mktemp`). Item 10 : le G1 ne cite aucune des deux pages entre guillemets ; il cite le fichier de FAITS de l'orchestrateur (C-3).

## 12. Critères d'acceptation fermés

- **CA-D8a-1** : `git diff --name-status fb089dc` = exactement les fichiers IN du §3 (plus le journal).
  - *Amendement du 2026-09-30 (cp-1 C-7 ; consultation advisor du G1)* : la base est le sha consigné au journal G1 (`aa0afdc`, `main` au lancement), et non `fb089dc`. `.claude/`, `.github/` et `enforcement/` sont identiques entre les deux (diff vide, mesuré), donc CA-D8a-12 tient. La liste IN comprend aussi la copie de ce G0, `docs/adr-0028/G0-lot-D8a.md`, imposée par la mission.
- **CA-D8a-2** : `.claude/agents/*.md` inchangés (sha256 égaux à `fb089dc`).
- **CA-D8a-3** : `find enforcement -path '*/.claude/*'` = 0 ; le runner n'écrit que sous `mktemp`.
- **CA-D8a-4** : O-1 vert, avec la table du §7 intégrale pour le lot et la part de chaque sous-lot en cas de coupe.
- **CA-D8a-5** : O-2 vert : 2 fichiers dans le worktree, 3 sur l'arbre principal.
  - *Amendement du 2026-09-30 (fait mesuré au G1, O-2)* : 3 fichiers dans le worktree du harnais (réglage local ignoré, présent), 3 sur l'arbre principal, 2 sur une copie propre (O-3, k=0).
- **CA-D8a-6** : O-3, trois rouges, jetons attendus.
- **CA-D8a-7** : O-4, chaque mutant tué, lignes de commande et sorties au journal G1 ; catégorie F2P déclarée.
- **CA-D8a-8** : O-5 = 0. **CA-D8a-9** : O-6 = 0.
- **CA-D8a-10** : O-7 (xtask VERT, suite `s2-harness` identique à la base) et O-8 (0 entrée neuve dans TMP).
- **CA-D8a-11** : bloc `gates.yml` conforme à CH-15 ; aucun autre job modifié, diff limité à l'ajout et à l'en-tête.
- **CA-D8a-12** : O-9 : sha256 des fixtures = `d44a2211f59603a6e756eefb18c1e464905d49dc8274e8c8b65c6321840518ac` (devops) et `e66873b3f3c384d4a43790bb154c6a40fffa68e85a722b13d59722cd0cf0fcac` (orchestrateur).
- **CA-D8a-13** : en-tête du lint conforme à CH-16 (pas de R-4, pas de `.ps1`, pas d'exemption ; sources citées).
- **CA-D8a-14** : R-25 mesuré ≤ 200 par (sous-)lot, méthode écrite ; en cas de coupe, lignes datées proposées pour l'annexe A.
- **CA-D8a-15** : journal G1 au format B0 (§15), vocabulaire 09 respecté (ni « garantit », ni « indépendant » comme fait, ni « verified », ni « CI verte donc… »), aucune citation entre guillemets d'une source non versée.
- **CA-D8a-16** : enregistrement d'oracle substitut produit (G1), puis refait par le G2.
- **CA-D8a-17** : PC-1 consignée avant le G7.
- **CA-D8a-18** : items 1-12 repris au journal G1 ; versement à l'annexe B par l'orchestrateur.

## 13. Risques MAST (libellés : annexe C l.13-18 ; les 14 modes restent la liste de revue)

| mode | forme dans D8a | contre-mesure système | preuve |
|---|---|---|---|
| FM-1.1 | le G1 modifie un agent réel, ou pose une fixture sous `.claude/agents/`, que le harnais chargerait comme agent (§5.4 a) | fixtures hors `.claude/`, arbres `mktemp`, CA-D8a-2 et CA-D8a-3 | sha256, `find` |
| FM-3.3 | des tests verts sur un lint trop permissif ; ou des cas « propres » de l'amont (l.85-86) portés tels quels, qui certifieraient un roster supplanté | liste exacte ; sortie ET jeton vérifiés ; M-1 à M-4 ; T-14 et T-15 inversés par rapport à l'amont | O-4 |
| FM-3.2 | l'oracle local ne prouve ni les outils Linux ni la syntaxe du workflow ; le lint ne voit que le texte | item 8 ; CH-17 et item 4 | déclaré |
| FM-2.3 | glissement de périmètre (effort, environnement, workflows, D8b, D8c, `s2-harness`) | liste OUT (§3), items 2, 3, 6, 9 ; diff limité (CA-D8a-1) | revue G2 |
| FM-2.4 | faits retenus : écart mesuré, amont retrouvé, écart `git status` | §5.1, §5.2 et en-tête de ce document ; item 11 | sceaux du §15 |
| FM-1.5 | la coupe R-25 est improvisée après coup | règle de coupe écrite d'avance (§9), avec arrêt et consultation au-delà | journal G1 §1 |
| FM-2.2 | un choix ouvert est tranché sans le dire | Q-G0 du §14 | — |

Topologie (CA-4) : un G1 mono-agent en worktree, puis un G2 sur instance séparée à contexte frais. Aucun autre fan-out : le partage n'a pour motif que l'indépendance de vérification imposée par le système. Conflit de fichier : D8b et D8c modifient eux aussi `gates.yml`. Ordre recommandé : D8a, D8b, D8c, chacun sur le commit du précédent.

## 14. Questions pour l'orchestrateur

- **Q-G0-1** : compte R-25 du journal G1 (mission contre précédent B0 l.30) ?
- **Q-G0-2** : forme de la consignation de PC-1 (§2) ?
- **Q-G0-3** : erratum de l'amont (item 11) : au JOURNAL, ou dans l'entrée DECISIONS de D8c (« collision ADR-0020 ») ? La citation canonique devient-elle « VibeGates `0b4f3f9` = blob `457565f` » ?
- **Q-G0-4** : fil de workflow (CH-9) retenu plutôt que l'OUT pur. À confirmer ou à renverser au cp-1.
- **Q-G0-5** : écart CH-11 (vide ⇒ 2) au canonique, et suppression des exemptions (CH-6) : ces deux écarts au blob source demandent-ils une ligne à l'annexe E (avis ou canonique non suivis) ?

## 15. Consignes au G1 et sceaux

- **Worktree** : détaché sur la base courante de `main` au lancement (au moins `fb089dc`). Variables : `TMPDIR`, `TMP` et `TEMP` sur `F:/tmp/shogen-tests-tmp` ; `CARGO_HOME` et `CARGO_NET_OFFLINE=true` de la mission. Ni `GIT_DIR`, ni `--write-tree`, ni `SHOGEN_S2_CAMPAGNE_CONTROL` ; aucune pièce D.2. Seul un commit local d'empilement dans le worktree est admis.
- **Journal `docs/G1-lot-D8a.md`**, au format de B0 :
  - en-tête : modèle, horloge `date -u`, mandat, base ;
  - §0 préconditions (PC-1 incluse) ; §1 coupe R-25 (estimation avant code, puis mesure) ; §2 changements (sha256 avant et après) ; §3 définitions appliquées (CH-1..CH-17) ; §4 tests, chaque test nommant sa mutation ; §5 mutants ; §7 tuyaux ; §8 MAST ; §9 `error_origin` ; §10 Review Focus ; §11 Q-G1 ; §12 livrables ; §14 attestation.
- **Runner** : conçu d'après l'amont (`d9ad850`), mais compact. Pas de mutants dans le dépôt, pas de parité `.ps1` ; les cas « propres » de l'amont sont inversés (§5.1).
- **Sceaux** : `F:/tmp/shogen-lots/D8a/g0-mesures/SHA256SUMS.txt` (sha256 `cd73655e6d3b55e1e6b9fd889456f7c72a5b2379913bad7dfbe78809f92e0a36`, scellé à 03:15:49Z) liste :
  - `lint-canonique-457565f.sh` (`983ba152…`) ;
  - `gates-493ae8c.yml` ;
  - `arbre-reel-fb089dc/` (3 fichiers) ;
  - `mesure-canonique.sh`, `mesure-canonique.out` (`7884b2c0…`) ;
  - `mesure-complements.sh`, `mesure-complements.out` (`8c0efb10…`) ;
  - `reel-canonique.out` ;
  - `amont-vibegates.txt` (`6f5b557b…`) ;
  - `horloge-debut.txt`.
- **Rejeu** : `bash mesure-canonique.sh lint-canonique-457565f.sh` et `bash mesure-complements.sh lint-canonique-457565f.sh`, lancés dans `g0-mesures/`, reproduisent les deux sorties.

  Le sha256 de ce document est écrit à côté, dans `G0-lot-D8a.md.sha256`.

## 16. Index des amendements datés du 2026-09-30 (G1 du lot ; texte accepté inchangé au-dessus)

- **C-1** (SHOGEN-CI-S2-SAUT-1) : item 13 du §11, re-formé en sous-lot D8a-3 daté ; même ligne au journal G1 §11.
- **C-2** (PC-1, lecture (b) consignée au JOURNAL l.122) : le résidu, l'`error_origin` orchestrateur de la première déviation, est porté au journal G1 §9.
- **C-3** (lecture sur place) : puce sous la table du §4.
- **C-4** (lignes datées de l'annexe A, erratum de l'amont) : propositions au journal G1 §1 et §11 ; actes de l'orchestrateur au commit.
- **C-5** (G3 opérant) : puce sous la table du §10 ; texte proposé au journal G1 §7.
- **C-6** (O-10) : puce sous O-10 et note sous la table du §11 (item 8 c).
- **C-7** (base) : puces sous O-7 et sous CA-D8a-1.
- **C-8** (consignes git et TMP) : appliquées, attestées au journal G1 (en-tête et §14).
- **Faits du G1** : coupe R-25 selon la règle 4 (puce du §9) ; T-45 et M-22 (puces du §7 et d'O-4) ; worktree à 3 fichiers et copie propre à 2 (puces d'O-2, d'O-3 et de CA-D8a-5) ; TMP neuf pour O-8 (puce d'O-8).
- **Correction de la revue G2** (2026-09-30, C-1..C-8) : puces sous CH-7, CH-10, CH-11, CH-12, la table du §7 et O-4 ; puce d'O-10 amendée en place (C-7 d).
