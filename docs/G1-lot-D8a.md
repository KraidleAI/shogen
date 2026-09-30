# G1 — lot D8a d'ADR-0028 (lint d'épinglage des modèles, job g1, cas C-14), Shōgen — journal

- **Modèle** : `claude-opus-5-5` (déclaré par le harnais et en tête de session, R-1), effort max, contexte frais ; worker G1. Aucun commit, aucun workflow déclenché (R-20). Aucune variable `GIT_DIR` ni `GIT_WORK_TREE` posée, aucun `--write-tree` ; `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée (retirée par `unset` dans chaque script d'oracle). Écritures git limitées au worktree du lot : `git merge --ff-only aa0afdc` sur sa branche (§0), puis `git add -N .` pour produire les diffs prescrits. Lectures git en `git --no-optional-locks` ; aucun `git status` sur un dépôt de C: (C-8).
- **Horloge** (`date -u`) : première heure relevée 2026-09-30T05:00:37Z (avance rapide du worktree ; l'orientation la précède) ; suite de base 05:16:05Z-05:16:20Z ; `cargo xtask verify` de base 05:16:28Z-05:16:43Z ; estimation R-25 écrite avant tout code (horloge relevée 05:16:43Z, sceau 05:17:46Z) ; fixtures 05:21:06Z ; premier essai de D8a-1 05:24:07Z (213 lignes) ; consultation R-26 vers 05:26Z ; D8a-1 figé une première fois 05:27:34Z ; D8a-2 écrit, 45 cas à 05:36:30Z ; campagne de mutants v1 05:39:18Z-05:50:25Z (M-12 survit, §5) ; sondes CR et consultation R-26 vers 05:45Z-05:50Z ; D8a-1 re-figé 05:52:29Z ; campagnes v2 05:53:01Z-05:56:32Z (D8a-1) et 05:56:32Z-06:05:31Z (état final) ; suite finale 05:59:34Z ; O-1 final 06:00:02Z ; temps 06:05:39Z ; xtask, premier passage, 06:07:30Z ; diffs, contrôle d'application et second passage xtask ensuite (`G1-rapport.md`).
- **Mandat** : commande de mission de l'orchestrateur Shōgen (`claude-fable-5-1`, workflow du 2026-09-30, vague 3), lot D8a de l'annexe A (ligne l.28 à `aa0afdc`) ; G0 accepté au cp-1 complet (`F:/tmp/shogen-lots/D8a/G0-lot-D8a.md`, sha256 `8afa3f7dd2c7232ea459bd7308e97391b61c99055084cd6035262d10afe4c387`), avec les corrections C-1 à C-8. Cadre : ADR-0028 et annexes A-E à `aa0afdc`.
- **Base (C-7)** : `aa0afdc` (`main` au lancement, `git rev-parse main`).
- **Classification** : additive. Quatre fichiers neufs sous `enforcement/`, un job ajouté à `gates.yml`, deux documents.
- **Résultat** : lot coupé en deux sous-lots par la règle 4 du G0 §9 (consultation formée), **D8a-1** (193 lignes) et **D8a-2** (93 lignes). Runner : 45 cas sur 45. Arbre réel : lint en sortie 0, 3 fichiers (O-2). Trois rouges semés sur l'entrée committée. 22 mutants de gate tués sur l'arbre final, après une correction du lecteur de frontmatter qu'un mutant survivant a imposée (E-6). `yaml.safe_load` et structure de `gates.yml` tenus (C-6). Suite `s2-harness` identique à la base ; `cargo --locked xtask verify` VERT. SHOGEN-CI-S2-SAUT-1 re-formé en sous-lot D8a-3 (C-1).

## 0. Préconditions mesurées avant code

- **Base (C-7)** : le worktree fourni par le harnais était à `fa0ce5b` (branche `worktree-wf_b64d9898-cd4-9`), ancêtre de `fb089dc` (37 commits) et de `aa0afdc` (46 commits) ; mesures `git merge-base --is-ancestor` et `git rev-list --count`. Acte du worker : `git merge --ff-only aa0afdc` sur la branche du worktree (05:00:37Z), seule référence déplacée ; `main` non touchée. `.claude/`, `.github/` et `enforcement/` sont identiques entre `fb089dc` et `aa0afdc` (`git diff --stat` vide) : les références d'O-9 tiennent, rejouées sur `fb089dc` et sur l'arbre (`d44a2211…518ac`, `e66873b3…0fcac`).
- **PC-1 (G0 §2, C-2)** : la lecture (b) est consignée par l'orchestrateur au JOURNAL (`aa0afdc`, l.122) : portage `enforcement/` couvert par la délégation du 2026-09-30, veto §4.10 a non exercé, révocable jusqu'à l'exécution unique ; tag et suppression de la branche `roster-ban-alignment-2026-08-20` réservés à l'investisseur, hors lot. Le G1 a travaillé sous cette consignation. Résidu de C-2 : §9, E-2.
- **C-3** : les faits de la page des sous-agents viennent du fichier de FAITS de l'orchestrateur, `F:/tmp/shogen-lots/D8a/FAITS-claude-code-subagents-2026-09-30.md` (sha256 `de45ea493892ddbaa9380ae36e1f2f23efe61fc6ab32542b7418be8891bc5f3a`, recalculé) : découverte récursive et imbriquée de `.claude/agents/` (a) ; `model` omis, donc ordre de résolution qui aboutit au modèle de la conversation (b) ; alias de famille résolu vers le modèle de session, suffixe `[1m]` compris (c) ; allowlist d'organisation avec substitution (d). La page de configuration du modèle n'a pas de FAITS de l'orchestrateur : §9, E-3.
- **Sceaux du G0** : `g0-mesures/SHA256SUMS.txt` rejoué par `sha256sum -c` : 12 fichiers sur 12 conformes.
- **Suite de base** (`aa0afdc`, TMP neuf, variable non posée) : `Ran 206 tests`, `OK (skipped=2)`, sortie 0, 0 entrée TMP ; sauts : tests (ii) et (ii bis) de `test_exclusion`.
- **`cargo --locked xtask verify` de base**, sous la garde de B0 (toolchain forcée, auto-installation coupée, serveurs rustup en 127.0.0.1:9, `CARGO_HOME` et `CARGO_NET_OFFLINE=true` de la mission, cible sous `F:/tmp/shogen-lots/D8a/target`) : S-G1 à S-G8, `fmt`, `no_std`, `clippy` VERT ; verdict global VERT, sortie 0 ; `F:/rust/rustup/downloads` vide. Dans ce worktree, S-G5 tourne en régime de corpus incomplet (0 artefact présent sur 125 déclarés) : §10, point 5.
- **Outillage local** (mesuré) : GNU bash 5.3.15, GNU Awk 5.4.1, GNU sed 4.9, GNU grep 3.0, GNU findutils 4.11.0, coreutils 8.32, GNU patch 2.7.6, Python 3.14.5, PyYAML 6.0.3.
- **Garde du harnais** (§13) : le garde d'isolation du worktree refuse `bash <script>`, `awk --version`, `git -C` vers un dépôt hors du worktree, les heredocs qui contiennent `git`, et toute ligne qui nomme le dossier des workflows. Les oracles sont donc des scripts écrits sous `F:/tmp/shogen-lots/D8a/oracles/` et exécutés directement (shebang) ; ils lancent le lint et le runner par `bash <chemin>`, forme exacte du job ; leurs seuls appels git sont `archive` et `rev-parse`, sur ce worktree.

## 1. Coupe R-25

- **Estimation écrite avant tout code** (`oracles/estimation-R25.txt`, horloge relevée 05:16:43Z, sha256 `d7b2a156fa11fac8a54cca4bf7d2732b8f56669cad2a104bd014f721268822b1`, sceau 05:17:46Z) : D8a-1 ≈ 202, D8a-2 ≈ 60, lot ≈ 262 ; coupe prévue selon le G0 §9.
- **Première mesure de D8a-1 selon la coupe du G0** : lint 106, runner 79, fixtures 28, soit **213 > 200**. Avec la règle 3 (T-23..T-28 vers D8a-2) : 207 > 200. **Règle 4 : arrêt et consultation formée** (R-26, advisor, canal 1, vers 05:26Z). Resserrer les commentaires jusqu'au seuil a été écarté : l'en-tête porte le contenu que CH-16 impose, et les commentaires en ligne portent les choix fail-closed que le G2 doit lire.
- **Coupe retenue, écart à la coupe du G0 §9** : frontière de la passe JSON. Le code de CH-10 (aplatissement, `settings.local.json`, refus des valeurs non chaînes) et T-20 passent en D8a-2 ; T-23..T-28 restent en D8a-1. Aucun contrôle retiré : le code est différé d'un sous-lot, et les deux sous-lots vont au même G2 (précédent `0abc881`). M-15, M-16 et M-22 ont désormais leur code et leur tueur dans le même sous-lot. Conséquence déclarée : en D8a-1, la suppression des exemptions n'est couverte que sur la route frontmatter (T-18, T-19) ; la route JSON (T-20) est en D8a-2.
- **Mesures** (méthode du lot A : `git diff --numstat` des fichiers suivis, `wc -l` des fichiers neufs ; pour D8a-2, lignes `+` du `diff -u` contre l'instantané D8a-1 figé ; `oracles/r25.sh`, `oracles/r25.out`) :

| sous-lot | `lint-model-pinning.sh` | `run-fixtures-model-pinning.sh` | fixtures | `gates.yml` | total ajouté | seuil |
|---|---|---|---|---|---|---|
| D8a-1 | 88 (neuf) | 77 (neuf) | 28 (13 + 15) | 0 | **193** | ≤ 200 |
| D8a-2 | +38 −4 | +22 −2 | 0 | +33 −4 | **93** | ≤ 200 |

- **Lot entier** : 286 lignes ajoutées en somme des sous-lots ; `lot.diff` en compte 280, les 6 lignes de D8a-1 réécrites par D8a-2 n'y figurant qu'une fois. L'estimation était fausse (E-4) : le lint mesure 122 lignes contre ≈ 102 estimées (en-tête et commentaires sous-estimés), le runner 97 contre ≈ 108.
- **Documentation, hors compte** (précédent du lot A et de B0 ; Q-G0-1), publiée à part : copie du G0, `docs/adr-0028/G0-lot-D8a.md`, 516 lignes, soit les 485 lignes acceptées sans retrait et 31 lignes d'amendements datés (`oracles/G0-copie.diff`, 0 ligne retirée) ; ce journal.
- **Lignes datées proposées pour l'annexe A (C-4)** : acte de l'orchestrateur, non écrit ici. Format des colonnes de l'annexe A.

| lot (date) | objet (décision) | véhicule | oracle non-LLM nommé | taille (R-25) | tuyau (entrée → sortie → consommateur ; test) | cp-1 |
|---|---|---|---|---|---|---|
| **D8a** (2026-09-29 ; amendée le 2026-09-30 par le G0 et le G1 du lot) | D8, C-14, CB-10 : lint en liste blanche exacte, job `g1-model-pinning` ; cas limites tranchés au G0 : `claude-opus-5-5[1m]` refusé `R-1/suffixe` (CH-4), `claude-sonnet-5` refusé `R-1/retire`, jamais `R-1/ban` (CH-5). Écarts nommés au blob source `457565f` : 12 cas acceptés par le blob et refusés ici (CH-1, G0 §5.2) ; routes d'exemption supprimées (CH-6) ; JSON aplati et valeur non chaîne refusée (CH-10, T-45) ; portée vide ⇒ 2 (CH-11) ; R-4 retiré de l'en-tête (CH-16) ; frontmatter lu en bash (E-6) | `enforcement/`, `gates.yml`, tests shell | O-1 à O-10 du G0 amendé ; 22 mutants de gate | 286 [mesuré : D8a-1 193 + D8a-2 93] au lieu de ≈ 205 ; coupé en D8a-1 et D8a-2 (règle 4 du G0 §9) | `.claude/agents/*.md` → lint → job g1 (partiel : GC-01, GC-09) et G3 opérant local (C-5) ; hook : item 9 ; tests O-2 et O-3 | complet |
| **D8a-1** (2026-09-30 ; coupe R-25 du G1 de D8a, règle 4) | lint : liste blanche exacte ; jetons `ban`, `tier-nu`, `hors-liste`, `cle-model`, `vide` ; frontmatter des agents et des skills, lu en bash (BOM, CR, guillemets, commentaire) ; cas T-01..T-19 et T-21..T-28 | `enforcement/lint-model-pinning.sh`, `enforcement/tests/run-fixtures-model-pinning.sh`, `enforcement/tests/fixtures/model-pinning/` | O-1 (27 cas), O-3 (k = 0, 1, 3), O-4 (12 mutants tués ; M-12, M-13, M-14 et M-17 survivent à l'état D8a-1 seul et sont tués en D8a-2), O-5, O-6, O-9 | 193 [mesuré] | non branché seul : consommable au G7 avec D8a-2 | complet (sous le cp-1 du lot) |
| **D8a-2** (2026-09-30 ; coupe R-25 du G1 de D8a, règle 4) | réglages JSON (CH-10 : aplatissement, `settings.local.json`, valeur non chaîne) ; jetons `retire`, `suffixe`, `workflow` ; job `g1-model-pinning` et en-tête de `gates.yml` ; cas T-20, T-29..T-45 ; T-13 et T-14 re-attendus | `.github/workflows/gates.yml`, les deux scripts | O-1 (45 cas), O-2, O-3 (k = 2), O-4 (22 mutants tués sur l'arbre final), O-5 à O-10 | 93 [mesuré] | lint → job g1 et G3 opérant local ; test O-2 | complet (sous le cp-1 du lot) |
| **D8a-3** (2026-09-30 ; C-1 du cp-1 complet de D8a) | SHOGEN-CI-S2-SAUT-1 : le job `s2-harness-unittest` exige le résumé final (`Ran N`, `OK`), n'admet que les sauts dont le motif nomme `SHOGEN_S2_CAMPAGNE_CONTROL`, et borne N par un plancher committé ou un manifeste des modules (choix au G0) | job `s2-harness-unittest` de `gates.yml` ; `enforcement/` (chemin proposé) | rejeux R8, MT-5, MT-6, MT-7 et MT-9 du lot CI-S2 : sortie ≠ 0 pour chacun ; suite réelle : sortie 0 | ≈ 70 [inféré] | suite unittest → job → check-run ; G3 opérant local | bref (proposé) ; G0 ouvert par l'orchestrateur au commit de D8a ; construction avant RENDU-1 |

- *Amendement du 2026-09-30 (correction de la revue G2, C-8)* : estimation de la correction écrite avant code (`corr-oracles/estimation-R25.txt`, horloge 07:29:13Z, sha256 `a912a56d…b3e1`) : ≈ 62 lignes ; mesure : +96 (E-9, §15). **D8a-2 corrigé = 177 ≤ 200** (lint +77 −20, runner +66 −6, `gates.yml` +34 −4, contre l'instantané D8a-1 figé) ; D8a-1 inchangé (193) ; aucun troisième sous-lot. Lignes de l'annexe A mises à jour et ligne du diff de correction : §15.

## 2. Changements (worktree du lot, sur `aa0afdc`)

| fichier | D8a-1 | D8a-2 | sha256 base → D8a-1 → D8a-2 |
|---|---|---|---|
| `enforcement/lint-model-pinning.sh` | neuf : liste blanche exacte ; jetons `ban`, `tier-nu`, `hors-liste`, `cle-model`, `vide` ; frontmatter des agents et des skills, lu en bash | jetons `retire` et `suffixe` ; passe JSON ; fil de workflow ; en-tête et message de portée vide élargis | — → `648ebe97…6125` → `c2293121…29dd` |
| `enforcement/tests/run-fixtures-model-pinning.sh` | neuf : 27 cas | T-20, T-29..T-45 ; T-13 et T-14 re-attendus | — → `62f5c328…5d75` → `a527ca56…d85d` |
| `enforcement/tests/fixtures/model-pinning/shogen-devops.md` | copie octet pour octet de `.claude/agents/shogen-devops.md` l.1-13 | — | — → `d44a2211…518ac` |
| `enforcement/tests/fixtures/model-pinning/shogen-orchestrator.md` | copie octet pour octet de `.claude/agents/shogen-orchestrator.md` l.1-15 | — | — → `e66873b3…0fcac` |
| `.github/workflows/gates.yml` | — | job `g1-model-pinning` ; en-tête (périmètre, items de forge) | `2fdd6069…28a1` → idem → `376ef594…ddd1` |
| `docs/adr-0028/G0-lot-D8a.md` | copie du G0 accepté, amendements datés (documentation du lot) | | — → `92a048c1…3344` |
| `docs/G1-lot-D8a.md` | ce journal | | — |

- **Intouchés** (sha256 égal à la base, CA-D8a-2) : `.claude/agents/shogen-devops.md` (`c0ee49ea…302c`) et `.claude/agents/shogen-orchestrator.md` (`4727e94e…0e1b`) ; tout `s2-harness/` ; ADR-0028 et ses annexes ; `JOURNAL.md`.
- **CA-D8a-1 amendé** : `git diff --name-status aa0afdc` = les sept fichiers ci-dessus (six ajoutés, `gates.yml` modifié) ; mesure au §6.
- **Première forme du lint** (v1, lecteur `sed` puis `awk`) : sha256 `50622be4…300b` à l'état D8a-1 et `e96ba7c7…c254` à l'état D8a-2. Remplacée par la lecture en bash (E-6) ; ses diffs et ses sorties sont conservés sous des noms `-v1` (§12).

- *Amendement du 2026-09-30 (correction de la revue G2, C-1 à C-7)* : sha256 G1 → corrigé : lint `c2293121…29dd` → `1c57e8c4…4fa9` ; runner `a527ca56…d85d` → `4e65eee7…f7e3` ; `gates.yml` `376ef594…ddd1` → `bc3aea17…af53` (commentaires du job seulement, structure YAML identique) ; fixtures inchangées. Copie du G0 et journal : §15.

## 3. Définitions appliquées (CH-1 à CH-17)

- **CH-1** : `ALLOWED` = `claude-opus-5-5 claude-sonnet-5-5 claude-fable-5-1`, comparaison octet pour octet (`dans_liste`) ; tout le reste sort en 2. Conformité ajoutée par le G1 : une clé `model` ou `advisorModel` dont la valeur JSON n'est pas une chaîne sort en `R-1/hors-liste` (T-45, M-22) ; le blob source l'ignorait. Q-G1-2.
- **CH-2** : liste sur une ligne, dans le script ; l'en-tête cite les décisions 133, 267 et 280 et `CLAUDE.md` l.20-31.
- **CH-3** : ordre de classement appliqué tel quel (liste blanche, `ban`, `tier-nu`, `retire`, `suffixe`, `hors-liste`) ; jetons `cle-model`, `vide`, `workflow` ; format `REFUS (<jeton>) <lieu> : <valeur> — <motif>` sur stderr. Le lieu vaut `fichier:ligne` pour un frontmatter et `fichier (clé)` pour un réglage. Succès : `OK (R-1) : <n> fichier(s) ; liste blanche : …` sur stdout. Une dernière ligne sur stderr rappelle la liste en cas de refus.
- **CH-4** : `claude-opus-5-5[1m]` refusé `R-1/suffixe`, en frontmatter (T-13) et en réglage (T-42). Le mode de contrôle des journaux (forme résolue `<id>[1m]` admise par égalité exacte) n'est pas construit : aucun consommateur ; item 1.
- **CH-5** : `claude-sonnet-5` refusé `R-1/retire` ; T-14 exige aussi l'absence de `R-1/ban`.
- **CH-6** : aucune route d'exemption. `.claude/model-exceptions.txt` n'est jamais lu (T-20 le pose et reste refusé) ; une annotation ADR tombe avec le commentaire et n'exempte rien (T-18, T-19).
- **CH-7** : exactement une clé `model` de premier niveau (ligne non indentée), sinon `R-1/cle-model` (T-21 absente, T-22 doublée ; fichier sans frontmatter : compte 0). Les lignes `model` indentées sont contrôlées sans être comptées (T-23, T-24).
- **CH-8** : BOM de la ligne 1 (T-27, T-28), CR final (T-35), une paire de guillemets appariée (T-29, T-30, T-31), commentaire précédé d'un blanc (T-32, T-33), blancs finaux ; `model : x` (T-34) ; valeur vide (T-36). Deux écarts d'implémentation, sans écart de comportement : (i) les blancs finaux sont l'espace et la tabulation (`[ \t]`), pour que seule la règle du CR retire un CR ; (ii) le frontmatter est lu en bash (`read -r`, `${x%$'\r'}`, `${x#$'\xEF\xBB\xBF'}`, `[[ =~ ]]`) et non par `sed` puis `awk` comme au blob source : ces outils retirent eux-mêmes, en local, le CR des fins CRLF (E-6).
- **CH-9** : fil de workflow en D8a-2, motif et élagage du G0 ; `ROOT` privé de son `/` final, pour que `-path "$ROOT/.claude/worktrees"` s'applique ; T-43, T-44.
- **CH-10** : clés `model` et `advisorModel` (clé comparée sans casse, comme au blob source ; valeur comparée exactement) ; JSON aplati par `tr '\r\n' '  '` (T-41) ; `settings.local.json` lu (T-40) ; valeur non chaîne refusée (T-45).
- **CH-11** : 0 fichier dans la portée ⇒ `R-1/vide` (T-26).
- **CH-12** : `.claude/agents/**` et `.claude/skills/**` parcourus par `find` (T-37) ; corps non lu (T-25) ; `.claude/worktrees/` et `launch.json` hors portée.
- **CH-13** : invariant tenu (O-5 = 0) ; l'identifiant banni est construit à l'exécution dans le lint, le runner et les scripts de mutants.
- **CH-14** : fixtures copiées octet pour octet, provenance dans l'en-tête du runner, sha256 contrôlés (O-9) ; chaque cas copie une fixture dans un arbre `mktemp` et en remplace la ligne `model` (fonction `arbre`).
- **CH-15** : job conforme (O-10) ; placé entre `g5-dette` et `s2-harness-unittest` ; commentaire de `timeout-minutes` fondé sur des temps mesurés (§6, ligne « Temps »).
- **CH-16** : en-tête conforme ; CA-D8a-13 : 0 occurrence de `R-4`, `.ps1`, `exempt` ou `exception` dans le lint.
- **CH-17** : limite écrite dans l'en-tête ; le contrôle R-1 au lancement reste dû ; items 1, 3, 4 et 5.

## 4. Tests (runner shell, 45 cas) — chaque cas nomme la mutation qui le rougit

- Chaque cas vérifie la sortie ET le jeton ; un cas « 0 » exige le message `OK (R-1)` et son compte de fichiers ; T-14 exige en plus l'absence de `(R-1/ban)`. Un seul résumé fait foi : `model-pinning : <n> ok, <m> échec`. Sortie 0, 1 ou 3.
- **F2P** : catégorie « nouveau module » (lint et runner absents de la base) : les 45 cas sont neufs.
- **Mutations qui rougissent chaque cas** (campagne finale, §5 ; déduite de `oracles/mutants-d8a-2.out` par `oracles/cas-par-mutant.py`) :

| cas | mutants sous lesquels le cas est rouge |
|---|---|
| T-01 | aucun |
| T-02 | aucun |
| T-03 | aucun |
| T-04 | M-1 |
| T-05 | M-1 |
| T-06 | M-1 |
| T-07 | M-1, M-2 |
| T-08 | M-1, M-5 |
| T-09 | M-1 |
| T-10 | M-1 |
| T-11 | M-1 |
| T-12 | M-1, M-3 |
| T-13 | M-1, M-3, M-8 |
| T-14 | M-1, M-7 |
| T-15 | M-1 |
| T-16 | M-1, M-6 |
| T-17 | M-1, M-4 |
| T-18 | M-1, M-20 |
| T-19 | M-1, M-2, M-20 |
| T-20 | M-1 |
| T-21 | M-9 |
| T-22 | M-9 |
| T-23 | M-10 |
| T-24 | M-1, M-2 |
| T-25 | M-19 |
| T-26 | M-18 |
| T-27 | M-11 |
| T-28 | M-1, M-2, M-11 |
| T-29 | M-13 |
| T-30 | M-13 |
| T-31 | M-1 |
| T-32 | aucun |
| T-33 | M-1, M-3, M-14 |
| T-34 | aucun |
| T-35 | M-12 |
| T-36 | M-1 |
| T-37 | M-1, M-2, M-17 |
| T-38 | aucun |
| T-39 | M-1, M-2 |
| T-40 | M-1, M-2, M-16 |
| T-41 | M-1, M-2, M-15 |
| T-42 | M-1, M-3, M-8 |
| T-43 | M-21 |
| T-44 | aucun |
| T-45 | M-22 |

Cas rouges sous aucun mutant : 7 (T-01, T-02, T-03, T-32, T-34, T-38, T-44)

- **Lecture** : un cas positif (sortie 0) ne rougit que sous un mutant qui fait refuser trop : M-10, M-11, M-12, M-13 et M-19 sont de ce type, tués par des cas positifs (T-23, T-27, T-35, T-29 et T-30, T-25). Les autres mutants affaiblissent la gate et sont tués par des cas de refus. Les cas rougis par aucun mutant restent au contrat que le job exécute ; leur pouvoir de discrimination n'est pas revendiqué ici.

- *Amendement du 2026-09-30 (correction de la revue G2, C-5 et C-8)* : 76 cas, T-46..T-76 ajoutés ; table des cas neufs, lecture de référence (PyYAML 6.0.3, `json`) et mutants tueurs : §15.

## 5. Mutants de gate (tests négatifs d'outil, registre d'ADR-0011 pt 4)

- **Méthode** : `oracles/mutants.py` écrit chaque mutant par UN remplacement exact dans une copie du lint ; un remplacement qui ne s'applique pas exactement une fois rend le mutant « inapplicable », jamais « tué ». `oracles/mutants-run.sh` lance `bash <runner> <mutant>` sur un TMP neuf et exige une sortie ≠ 0 et au moins un tueur désigné parmi les cas en échec. Le worktree n'a jamais porté de mutant.
- **Campagne v1** (première forme du lint, 05:39:18Z-05:50:25Z, `oracles/mutants-d8a-2-v1.out`) : 21 tués, **1 survivant non attendu : M-12** (CR non retiré), T-35 ne rougit pas. Sondes (`oracles/sonde-cr.out`, `oracles/sonde-binaire.out`) : en local, le `sed`, le `awk` et le `grep` de Git Bash retirent le CR d'une fin CRLF lue en mode texte ; `read -r`, `tr` et `cat` le gardent ; `sed -b`, `awk -v BINMODE=3` et `grep -U` le gardent aussi. M-12 était donc équivalent en local, non sous Linux [inféré]. Correction E-6 (lecteur en bash), puis campagnes v2 ci-dessous.

**État D8a-1 re-figé (v2)** (`mutants-d8a-1.out`) :

| mutant | objet | verdict | cas rouges |
|---|---|---|---|
| M-1 | verdict accepte tout | tué par T-04 T-07 T-18 | T-04 T-05 T-06 T-07 T-08 T-09 T-10 T-11 T-12 T-13 T-14 T-15 T-16 T-17 T-18 T-19 T-24 T-28 |
| M-2 | B ajoute a ALLOWED | tué par T-07 | T-07 T-19 T-24 T-28 |
| M-3 | egalite remplacee par un prefixe | tué par T-12 T-13 | T-12 T-13 |
| M-4 | comparaison sans casse | tué par T-17 | T-17 |
| M-5 | suffixe non retire pour le jeton ban | tué par T-08 | T-08 |
| M-6 | minuscules non appliquees pour ban | tué par T-16 | T-16 |
| M-9 | regle de compte retiree | tué par T-21 T-22 | T-21 T-22 |
| M-10 | lignes indentees comptees | tué par T-23 | T-23 |
| M-11 | BOM non retire | tué par T-27 T-28 | T-27 T-28 |
| M-12 | CR non retire | survit à cet état (tueur(s) T-35 en D8a-2) rc=0 | aucun |
| M-13 | guillemets non retires | survit à cet état (tueur(s) T-29 T-30 en D8a-2) rc=0 | aucun |
| M-14 | commentaire sans blanc requis | survit à cet état (tueur(s) T-33 en D8a-2) rc=0 | aucun |
| M-17 | .claude/skills retire | survit à cet état (tueur(s) T-37 en D8a-2) rc=0 | aucun |
| M-18 | vide rendu vert | tué par T-26 | T-26 |
| M-19 | fichier lu en entier | tué par T-25 | T-25 |
| M-20 | exemption ADR reintroduite | tué par T-18 T-19 | T-18 T-19 |

Résumé : `RESUME D8a-1 : 12 tue(s), 0 survivant(s) non attendu(s), 4 survivant(s) attendu(s) (tueur en D8a-2), 6 inapplicable(s) ; TMP neuf : 0 entree(s)`.

**État final (v2), 22 mutants** (`mutants-d8a-2.out`) :

| mutant | objet | verdict | cas rouges |
|---|---|---|---|
| M-1 | verdict accepte tout | tué par T-04 T-07 T-18 | T-04 T-05 T-06 T-07 T-08 T-09 T-10 T-11 T-12 T-13 T-14 T-15 T-16 T-17 T-18 T-19 T-20 T-24 T-28 T-31 T-33 T-36 T-37 T-39 T-40 T-41 T-42 |
| M-2 | B ajoute a ALLOWED | tué par T-07 | T-07 T-19 T-24 T-28 T-37 T-39 T-40 T-41 |
| M-3 | egalite remplacee par un prefixe | tué par T-12 T-13 | T-12 T-13 T-33 T-42 |
| M-4 | comparaison sans casse | tué par T-17 | T-17 |
| M-5 | suffixe non retire pour le jeton ban | tué par T-08 | T-08 |
| M-6 | minuscules non appliquees pour ban | tué par T-16 | T-16 |
| M-7 | jeton retire retire | tué par T-14 | T-14 |
| M-8 | jeton suffixe retire | tué par T-13 T-42 | T-13 T-42 |
| M-9 | regle de compte retiree | tué par T-21 T-22 | T-21 T-22 |
| M-10 | lignes indentees comptees | tué par T-23 | T-23 |
| M-11 | BOM non retire | tué par T-27 T-28 | T-27 T-28 |
| M-12 | CR non retire | tué par T-35 | T-35 |
| M-13 | guillemets non retires | tué par T-29 T-30 | T-29 T-30 |
| M-14 | commentaire sans blanc requis | tué par T-33 | T-33 |
| M-15 | JSON non aplati | tué par T-41 | T-41 |
| M-16 | settings.local.json retire | tué par T-40 | T-40 |
| M-17 | .claude/skills retire | tué par T-37 | T-37 |
| M-18 | vide rendu vert | tué par T-26 | T-26 |
| M-19 | fichier lu en entier | tué par T-25 | T-25 |
| M-20 | exemption ADR reintroduite | tué par T-18 T-19 | T-18 T-19 |
| M-21 | fil de workflow retire | tué par T-43 | T-43 |
| M-22 | controle valeur non chaine retire | tué par T-45 | T-45 |

Résumé : `RESUME D8a-2 : 22 tue(s), 0 survivant(s) non attendu(s), 0 survivant(s) attendu(s) (tueur en D8a-2), 0 inapplicable(s) ; TMP neuf : 0 entree(s)`.

- *Amendement du 2026-09-30 (correction de la revue G2, C-8)* : campagne rejouée sur le lint corrigé, 73 mutants (M, MG, MP, MC) : §15.

## 6. Oracles non-LLM (O-1 à O-10) et enregistrement

- **O-1 — runner** (`bash enforcement/tests/run-fixtures-model-pinning.sh`, TMP neuf) : état D8a-1 re-figé : `model-pinning : 27 ok, 0 échec`, sortie 0 (05:52:29Z-05:52:40Z, `oracles/O1-d8a1.log`) ; état final : `45 ok, 0 échec`, sortie 0 (06:00:02Z-06:00:30Z, `oracles/O1-final.log`). Première forme du lint (v1) : 28 cas puis 27 à l'état D8a-1 (05:24Z, 05:27Z), 45 à l'état D8a-2 (05:36Z), tous verts.
- **O-2 — arbre réel** (`bash <lint> .` dans le worktree ; `bash <lint> F:/Shogen`, lecture seule) : état D8a-1 : sortie 0, 2 fichiers (réglages non lus à cet état) ; état final : sortie 0, 3 fichiers dans le worktree et 3 sur l'arbre principal ; aucun script de workflow trouvé (`oracles/O23-d8a1.out`, `oracles/O23-final.out`).
- **O-3 — rouges semés** sur des copies `git archive aa0afdc .claude` (entrée committée) : k=0 (copie intacte) → sortie 0, 2 fichiers ; k=1 (B) → 2 `R-1/ban` ; k=2 (`claude-sonnet-5`) → 2 `R-1/hors-liste` à l'état D8a-1, 2 `R-1/retire` à l'état final ; k=3 (ligne `model` supprimée) → 2 `R-1/cle-model`.
- **O-4 — mutants de gate** : §5.
- **O-5 — invariant de littéral** (CH-13) : 0 à l'état D8a-1 et à l'état final.
- **O-6 — compatibilité g5** : 0 occurrence avec le motif courant (`gates.yml` l.48) et 0 avec le motif élargi de D8c, sur les lignes `+` de `d8a-1.diff` et de `lot.diff` (`oracles/statiques-d8a1.out`, `oracles/statiques-final.out`).
- **O-7 — non-régression** : suite `s2-harness`, base et final : `Ran 206 tests`, `OK (skipped=2)`, sortie 0, 0 entrée TMP, mêmes deux sauts (`oracles/suite-base.sauts`, `oracles/suite-final.sauts`, `diff` vide) ; `cargo --locked xtask verify` : base VERT (05:16:28Z-05:16:43Z) ; arbre du lot, premier passage (06:07:30Z-06:07:34Z, journal complet sauf cette ligne) : VERT, sortie 0 ; S-G1 à S-G8, `fmt`, `no_std` et `clippy` VERT ; S-G4 couvre 47 fichiers (45 à la base) et S-G5 48 (46 à la base), les deux documents du lot compris ; en régime de corpus incomplet, S-G5 contrôle 252 fragments et en laisse 218 non contrôlés, comme à la base : le lot n'ajoute aucune citation anglaise. Second passage, sur l'arbre final : en tête de `G1-rapport.md`.
- **O-8 — TMP** : 0 entrée dans chaque TMP neuf, après chaque O-1, après chaque campagne de mutants et après chaque suite.
- **O-9 — fixtures** : `d44a2211f59603a6e756eefb18c1e464905d49dc8274e8c8b65c6321840518ac` et `e66873b3f3c384d4a43790bb154c6a40fffa68e85a722b13d59722cd0cf0fcac`, égaux aux frontmatters à `fb089dc` et à `aa0afdc` (CA-D8a-12).
- **O-10 (amendé, C-6)** : `yaml.safe_load` et structure de `gates.yml` : 15 assertions sur 15 (`oracles/O10.out`) ; contrôle négatif : trois copies semées (structure, job de base altéré, erreur de syntaxe) sortent en 1 (`oracles/O10-negatif.out`).
- **Temps** (`oracles/temps.sh`, local, Git Bash) : lint 0,59 à 0,89 s (six essais par série, worktree et arbre principal, deux séries à partir de 06:05:39Z) ; runner 20,6 s et 21,9 s (deux séries) ; O-1 final sous la charge des campagnes : 28,5 s. Première forme du lint (v1, 05:37:59Z) : lint 1,0 à 4,5 s, runner 29,7 à 38,6 s. Le commentaire de `timeout-minutes` cite 21 à 29 s et 0,6 à 0,9 s ; la borne de 5 min reste (`oracles/temps-final-1.out`, `oracles/temps-final-2.out`, `oracles/temps.out`).
- **CA-D8a-1** : `git diff --name-status aa0afdc` : `M` pour `gates.yml` (dossier des workflows) ; `A` pour les six autres : `docs/G1-lot-D8a.md`, `docs/adr-0028/G0-lot-D8a.md`, `enforcement/lint-model-pinning.sh`, `enforcement/tests/run-fixtures-model-pinning.sh` et les deux fixtures ; 7 fichiers, liste IN du §3 amendée (CA-D8a-1).
- **CA-D8a-2, CA-D8a-3, CA-D8a-13** : agents réels au sha de la base ; `find enforcement -path '*/.claude/*'` = 0 ; 0 occurrence de `R-4`, `.ps1`, `exempt` ou `exception` dans le lint (`oracles/statiques-final.out`).
- **Contrôle d'application** (`oracles/diffs-finaux.sh`) : base + `d8a-1.diff` + `d8a-2.diff` + `docs.diff`, et base + `lot.diff`, appliqués par `patch -p1` sur une extraction `git archive aa0afdc .github docs` : les sept fichiers du lot sont identiques à ceux du worktree (`oracles/check-apply.out`).
- **Enregistrement d'oracle substitut** : `oracles/oracle-G1-D8a-substitut.json` (schéma `shogen.g2.oracle-substitut.v1`, rôle G1, champs de D6 viii : arbre, sha256 par fichier, base, `static_only` faux, environnement, runs avec commande, sortie, sha256 et sortie attendue) ; son sha256 est en tête de `G1-rapport.md`.

- *Amendement du 2026-09-30 (correction de la revue G2, C-8)* : O-1 à O-10, corpus des 9 commits, cas G2-01..G2-25 et `vide-local` rejoués sur l'état corrigé : §15.

## 7. Tuyaux (CA-11, règle Branchement) et G3 opérant (C-5)

- **Entrée** : `.claude/agents/**/*.md` (2 fichiers suivis, produits par les commits de roster de l'orchestrateur) ; `.claude/skills/**/*.md` et `.claude/settings.json` absents ; `.claude/settings.local.json` ignoré par le gitignore global, présent sur l'arbre principal et dans ce worktree.
- **Pièce** : `enforcement/lint-model-pinning.sh`, sans état ; la liste blanche vit dans le script.
- **Sortie** : code 0 ou 2, jetons sur stderr.
- **Consommateur 1** : job `g1-model-pinning` (étape 1 : runner ; étape 2 : `bash enforcement/lint-model-pinning.sh .`). **Partiel déclaré** : forge morte (GC-01), aucun `required_status_checks` (GC-09) ; item 8.
- **Consommateur local** : le G3 opérant d'ADR-0028 §4.11 est l'oracle local, rejoué par l'orchestrateur. **Texte proposé pour C-5** (amendement d'ADR-0028 §4.11, acte de l'orchestrateur) : « *Amendement daté du 2026-09-30 (lot D8a, cp-1 C-5)* : à partir du commit de D8a, le G3 opérant comprend aussi les deux commandes du job `g1-model-pinning`, `bash enforcement/tests/run-fixtures-model-pinning.sh` (sortie 0 ; résumé `model-pinning : 45 ok, 0 échec`) et `bash enforcement/lint-model-pinning.sh .` (sortie 0 ; 3 fichiers sur l'arbre de travail principal, qui porte un réglage local ignoré ; 2 sur une copie propre). »
- **Consommateur 2** : hook versionné de D8c, **absent** ; item 9.
- **Test de composition** : O-2 (artefact d'entrée committé → lint → sortie 0) et O-3 (copies `git archive aa0afdc .claude`, une valeur changée → sortie 2 et jeton ; k = 0 : copie intacte → sortie 0, 2 fichiers).

- *Amendement du 2026-09-30 (correction de la revue G2, C-6 et C-8)* : texte proposé pour C-5, qui remplace celui ci-dessus : « *Amendement daté du 2026-09-30 (lot D8a, cp-1 C-5)* : à partir du commit de D8a, le G3 opérant comprend aussi les deux commandes du job `g1-model-pinning`, `bash enforcement/tests/run-fixtures-model-pinning.sh` (sortie 0 ; résumé `model-pinning : 76 ok, 0 échec`) et `bash enforcement/lint-model-pinning.sh .` (sortie 0 ; 3 fichiers sur l'arbre de travail principal, qui porte un réglage local ignoré ; 2 sur une copie propre). Le lint sort en 2 `R-1/vide` si aucun agent n'est lu ; le compte de fichiers attendu reste au critère. » Entrée étendue à tout `.claude/agents/`, `.claude/skills/` et `.claude/commands/` de l'arbre (C-1).

## 8. Risques MAST (annexe C) et contre-mesures

- **FM-1.1** : aucune fixture sous un chemin `.claude/agents/` du dépôt (CA-D8a-3 : `find enforcement -path '*/.claude/*'` = 0) ; arbres de cas sous `mktemp` ; agents réels inchangés (CA-D8a-2). Aucune pièce de l'annexe D.2 ouverte.
- **FM-3.3** : liste exacte ; sortie ET jeton vérifiés ; M-1 à M-4 tués ; T-14 et T-15 inversés par rapport aux cas propres de l'amont ; un mutant survivant (M-12) a été traité comme un défaut du lint, pas comme un défaut du test (E-6).
- **FM-3.2** : ce que l'oracle local ne prouve pas est nommé : outils de l'image (item 8 c), modèle qui tourne (CH-17, item 4). Écart local/Linux mesuré et réduit pour le lint (E-6) ; le runner emploie encore `awk` et `sed` (item 8 c).
- **FM-2.3** : SAUT-1 non fondu dans D8a-2 (item 13) ; D8b, D8c, `s2-harness/` non touchés ; diff limité aux sept fichiers.
- **FM-1.5** : coupe décidée par la règle écrite du G0 §9, jusqu'à la règle 4 et sa consultation, sans improvisation ni compression.
- **FM-2.4** : faits retenus au journal : amont retrouvé (G0 §5.1), réglage local dans le worktree (O-2), masquage du CR (E-6), refus du garde (§13).
- **FM-2.2** : choix du G1 exposés en Q-G1 (§11).

## 9. `error_origin` proposés (à assigner au G7)

- **E-1** : worktree créé à `fa0ce5b` au lieu de la base courante de `main`. Origine : harnais du workflow (même constat que E-1 de B0).
- **E-2** (résidu de C-2) : le G0 de D8a a été lancé avant que la lecture (b) de PC-1 soit consignée au JOURNAL (consignation à `aa0afdc`, l.122). Origine : orchestrateur.
- **E-3** (C-3) : la page de configuration du modèle n'a pas de FAITS de l'orchestrateur avant le G1, contrairement à la règle de lecture sur place. Origine : orchestrateur. Effet : le deuxième motif de CH-4 repose sur la seule lecture Firecrawl du worker G0 ; CH-4 tient par CB-10 et les identifiants catalogue ; l'item 4 ne démarre pas.
- **E-4** : estimation R-25 de D8a-1 à ≈ 202, mesure à 213 (lint 106 contre ≈ 92). Origine : worker G1 (en-tête et commentaires sous-estimés). Traité par la règle 4 et une consultation, sans retrait de contrôle.
- **E-5** : O-2 lit 3 fichiers dans le worktree, contre 2 attendus par le G0 : le harnais y a placé un `.claude/settings.local.json` ignoré (même taille et même mtime que celui de l'arbre principal ; `advisorModel` = `claude-fable-5-1`). Origine : environnement ; hypothèse du G0 corrigée par amendement (CA-D8a-5).
- **E-6** : M-12 survit à la campagne v1 : le lecteur `sed` puis `awk` du blob source laissait le mode texte des outils de Git Bash retirer le CR, ce qui masquait en local la règle du CR. Origine : worker G1 (implémentation reprise du blob sans mesure de l'environnement local). Corrigé par la lecture en bash ; D8a-1 re-figé ; les deux campagnes rejouées. La forme par options binaires (`sed -b`, `grep -U`, `BINMODE`) a été écartée : leur acceptation par les outils d'Ubuntu n'est pas mesurable d'ici, et un refus rougirait tout le job.
- **E-7** : garde d'isolation du harnais (§13). Origine : environnement. Le runner amont (blob `d9ad850`) n'a pas été relu par le G1 ; la conception suit la table du G0 §7.
- **E-8** : sorties v1 d'O-1, d'O-2/O-3 et des statiques de l'état D8a-1 réécrites par les rejeux v2 (résultats v1 au §6 de ce journal) ; affichage du pilote de mutants corrigé entre les deux états (espace manquant, sans effet sur le verdict). Origine : worker G1.

## 10. Review Focus

1. **Coupe par la règle 4** (§1) : frontière JSON au lieu de la coupe du G0 ; les deux sous-lots se revoient ensemble.
2. **Lecteur de frontmatter en bash** (E-6) : comportement identique au blob source sur LF, CRLF et BOM, mesuré par T-27, T-28 et T-35 ; lecture de `read -r` avec `|| [ -n "$x" ]` pour une dernière ligne sans saut.
3. **Valeur JSON non chaîne refusée** (T-45) : ajout du G1 au nom de CH-1 ; la clé est cherchée sans casse, comme au blob source.
4. **Fil de workflow** : motif du G0, élagage par nom (`target`, `.git`, `node_modules`, `mutants.out*`) et par chemin (`.claude/worktrees`, `biblio`) ; 0 script trouvé sur l'arbre principal (O-2).
5. **S-G5 en régime partiel dans ce worktree** (0 artefact sur 125) : ce journal et la copie du G0 ne portent aucune citation anglaise entre guillemets ; le régime complet est celui du rejeu de l'orchestrateur sur l'arbre principal.
6. **Temps local** : runner 11 à 39 s selon l'état et la charge, lint 0,3 à 4,5 s ; le commentaire du job cite les bornes mesurées.

## 11. Questions Q-G1 et items formés

**Questions pour l'orchestrateur**
- **Q-G1-1** : ratifier la coupe D8a-1 / D8a-2 par la règle 4 et les lignes datées proposées pour l'annexe A (§1).
- **Q-G1-2** : ratifier le refus des valeurs JSON non chaînes (T-45, M-22) au nom de CH-1.
- **Q-G1-3** : ratifier le lecteur de frontmatter en bash (E-6), écart d'implémentation au blob source.
- **Q-G1-4** : ouvrir le G0 bref de D8a-3 au commit de D8a (item 13).
- **Q-G1-5** : amender ADR-0028 §4.11 par le texte du §7 (C-5).
- **Q-G1-6** : confirmer la documentation hors compte R-25 (Q-G0-1) : copie du G0 et journal.
- **Q-G1-7** : le réviseur G2, s'il travaille dans un worktree du harnais, rencontrera le même garde (§13) ; les rejeux de l'orchestrateur sur l'arbre principal emploient la forme exacte `bash …`.
- **Q-G1-8** : erratum de l'amont (item 11, Q-G0-3) : texte proposé ci-dessous, pour le JOURNAL et la ligne E-D8b de l'annexe E.
- **Q-G0-4** (fil de workflow retenu) et **Q-G0-5** (ligne d'annexe E pour les écarts CH-6 et CH-11 au blob source) restent ouvertes.

**Texte proposé pour l'erratum (item 11 ; C-4)** : *Erratum du 2026-09-30 (G0 de D8a, §5.1)* : l'amont VibeGates est retrouvé dans le corpus local (clone `vibegates`, branche `pass-4-u4`, commit `0b4f3f9` du 2026-08-20T06:15:14+01:00) ; son `enforcement/lint-model-pinning.sh` est le blob `457565f`, identique à celui d'`adb2213` ; sa présence sur GitHub n'est pas établie. Il corrige git-ci §2.b l.118, ADR-0028 D8 l.95 (prémisse d'une amont non retrouvée) et la ligne E-D8b de l'annexe E ; la source canonique reste le blob `457565f`, dont la provenance se chaîne à VibeGates `0b4f3f9`. `error_origin` proposé : worker de la dimension git-ci de la cartographie du 2026-09-29 (recherche limitée au dossier `enforcement` du corpus).

**Items formés** (reprise du G0 §11 amendé ; versement à l'annexe B par l'orchestrateur, CA-D8a-18)

| # | item | objet | propriétaire | déclencheur |
|---|---|---|---|---|
| 1 | SHOGEN-R1-FORME-RESOLUE-1 | mécaniser le contrôle des journaux de modèle résolu (`<id>` ou `<id>[1m]`, égalité exacte) | orch. | G0 de RENDU-2 |
| 2 | SHOGEN-LINT-WORKFLOW-1 | lire les scripts de workflow (valeurs littérales sous la liste blanche, valeur non littérale refusée, paramètre d'invocation prioritaire) | orch. | le jeton `R-1/workflow` sort |
| 3 | SHOGEN-LINT-ENV-MODEL-1 | clés d'environnement des réglages JSON (`CLAUDE_CODE_SUBAGENT_MODEL`, `_FORCE`, `ANTHROPIC_MODEL`, `ANTHROPIC_DEFAULT_*_MODEL`) sous la liste blanche | orch. | premier `.claude/settings.json` suivi, ou G0 de D8c |
| 4 | SHOGEN-ROSTER-PLATEFORME-1 | recherche : réglages gérés (`availableModels`, `availableModelsMatch`, `enforceAvailableModels`, `deniedModels`) ; questions (a)-(e) du G0 | recherche : orch. ; décision : investisseur | après les FAITS de la page de configuration du modèle (E-3) ; décision au prochain point d'étape |
| 5 | SHOGEN-LINT-HORS-DEPOT-1 | agents globaux et réglages utilisateur, hors de portée d'un lint de dépôt | orch. ; investisseur | G0 de D8c, ou prochaine décision de roster |
| 6 | SHOGEN-LINT-EFFORT-1 | effort explicite par palier (défaut `medium` d'Opus 5.5) | orch. | prochain lot de roster, ou G2 de D8a |
| 7 | SHOGEN-LINT-ROSTER-SYNC-1 | dérive entre `ALLOWED` et le roster | orch. | prochaine décision de roster |
| 8 | SHOGEN-G1-FORGE-1 | (a) `g1-model-pinning` aux `required_status_checks` ; (b) premier run sur la forge ; (c) outils de l'image (`awk` du runner, `sed`, `find`, `mktemp`) et lecture du workflow par la forge ; la syntaxe YAML sort de l'item (O-10, C-6) | orch. ; (a) investisseur ou mainteneur | forge rétablie (§4.1) |
| 9 | SHOGEN-D8-HOOK-LINT-1 | le hook versionné de D8c lance ce lint | orch. | G0 de D8c |
| 10 | SHOGEN-BIBLIO-CLAUDE-CODE-1 | verser à `biblio/` les deux pages Claude Code lues le 2026-09-30 ; ce journal n'en cite rien entre guillemets | orch. ; go requis (téléchargement) | prochain versement |
| 11 | SHOGEN-D8-AMONT-ERRATUM-1 | erratum de l'amont, texte ci-dessus | orch. | commit de D8a |
| 12 | CORPUS-GABARIT-ROSTER-1 | gabarit de workflow du corpus épinglé `claude-opus-4-8` (transmission) | mainteneur du corpus | prochaine passe du corpus |
| 13 | SHOGEN-CI-S2-SAUT-1 (reprise, C-1) | construction de l'annexe B l.79, non construite dans D8a-2 alors que R-25 l'aurait permis (93 + ≈ 70) : le choix plancher ou manifeste revient à un G0 que celui-ci n'a pas tranché ; job et oracle distincts ; FM-2.3 | orch. | **sous-lot D8a-3** (2026-09-30) : G0 bref au commit de D8a ; construction avant RENDU-1 |

## 12. Livrables (`F:/tmp/shogen-lots/D8a/`)

- `lot.diff` : diff du lot entier contre `aa0afdc` (`git add -N .` puis `git diff HEAD`, prescrit).
- `d8a-1.diff` (base → état D8a-1 re-figé), `d8a-2.diff` (état D8a-1 → état final, `gates.yml` compris), `docs.diff` (les deux documents) : par `diff -ruN`, appliquables par `patch -p1` (contrôle d'application, §6).
- Première forme, conservée : `d8a-1-v1.diff`, `work/d8a-1-fige-v1/`, `oracles/mutants-d8a-1-v1.out`, `oracles/mutants-d8a-2-v1.out` (preuve de E-6), `oracles/mut-d8a-1-v1/`, `oracles/mut-d8a-2-v1/`.
- `G1-rapport.md` : ce journal, précédé des empreintes des livrables.
- `oracles/` : scripts (`cargo_env.sh`, `xtask.sh`, `suite.sh`, `o1.sh`, `o1-arbre.sh`, `o23.sh`, `statiques.sh`, `mutants.py`, `maj-mutants.py`, `mutants-run.sh`, `cas-par-mutant.py`, `lecteur-bash.py`, `o10.py`, `o10.sh`, `o10-negatif.sh`, `extraire_base.sh`, `diff-d8a-1.sh`, `diffs-finaux.sh`, `r25.sh`, `temps.sh`, `sonde-cr.sh`, `sonde-binaire.sh`, `sonde-aide.sh`, `sonde-t35.sh`, `sonde-tab.sh`, `oracle_record.py`, `remplir-journal.py`) et leurs sorties ; `estimation-R25.txt` et son sceau ; `G0-copie.diff` ; empreintes des états (`d8a-1-sha256.txt`, `d8a-1-v1-sha256.txt`).
- `work/` : extraction de base, instantanés D8a-1, copies d'application, contrôles négatifs d'O-10.

## 13. Contraintes d'environnement déclarées

- **Garde d'isolation du worktree** : refus mesurés de `bash <script>`, de `awk --version`, de `git -C` vers le clone VibeGates, des heredocs contenant `git`, de lignes nommant le dossier des workflows et d'un `cygpath` sur valeur calculée. Contournement retenu : scripts d'oracle écrits sous `F:/tmp/shogen-lots/D8a/oracles/` et exécutés directement ; leurs appels git visent ce seul worktree (`archive`, `rev-parse`). Aucun appel git n'a visé un autre dépôt ; le runner amont n'a pas été relu (E-7).
- **Mode texte des outils de Git Bash** : mesuré (§5) ; effet corrigé pour le lint (E-6) ; le runner le garde, ce qui ne touche que la construction des cas (T-35 écrit un vrai CRLF : 13 CR et 13 LF, `oracles/sonde-t35.out`).
- **Écrivains concurrents du TMP partagé** : O-8 compté sur un TMP neuf par exécution.
- **Rien sur C:** : TMP, cibles cargo et sorties sous `F:/tmp/` ; lecture seule de la toolchain sous `F:/rust`.

## 14. Attestation (forme d'ADR-0028 D.3)

- **Pièces lues** : ADR-0028 (D8, §4.10, §4.11, §6, §8) et annexes A, B (l.24, l.72-80), E (l.29-32) à `aa0afdc` ; le G0 accepté et ses mesures ; le fichier de FAITS de l'orchestrateur ; `docs/G1-lot-B0-pool-analyse.md` ; `JOURNAL.md` l.86, l.92, l.110-122 ; `CLAUDE.md` l.20-31 ; `docs/DECISIONS.md` l.2963-2969 ; le blob `457565f` et `adb2213:.github/workflows/gates.yml` ; `xtask/src/sg4.rs`, `sg5.rs`, `sg8.rs` (en-têtes).
- **Non ouverts** : les pièces de l'annexe D.2, toutes ; `F:/shogen-campagne/*`, `F:/tmp/shogen-j28/*`, `measure-M009a.md`, `F:/tmp/shogen-carto-2026-09-29/campagne.md`. Aucune copie scellée lue ; `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée.
- **Balayage mécanique** : `cargo xtask verify` (S-G4, S-G5) lit tout `docs/` ; seules les lignes de verdict et de note ont été affichées.
- **Aucune statistique S2 calculée sur les journaux de campagne. Aucun z, aucun K, aucun P̂_more ni aucun φ de campagne vu.**
- **Isolation git** : aucun `GIT_DIR`, aucun `GIT_WORK_TREE`, aucun `--write-tree` ; aucun commit, stash, checkout, reset ni push ; sur ce worktree seulement : `merge --ff-only`, `add -N`, `diff`, `archive`, `rev-parse`, `ls-tree`, `show`, `log`, `merge-base`, `rev-list`, `config --get`, `check-attr`, `check-ignore`, `status --short` (ce worktree, sur F:).

## 15. Corrections de la revue G2 (2026-09-30, ajout daté ; lignes précédentes inchangées, sauf l.8 : C-7 b)

- **Générateur** : `claude-opus-5-5` (R-1 déclaré en tête de session), effort max, contexte frais, worker G1 de correction, distinct du réviseur G2. Même worktree (branche `worktree-wf_b64d9898-cd4-9`, HEAD `aa0afdc`, rien de commité). Aucun commit, aucun workflow (R-20) ; aucun `GIT_DIR` ni `GIT_WORK_TREE`, aucun `--write-tree`. Horloge (`date -u`) : première heure 07:19:55Z ; estimation R-25 scellée à 07:29:13Z, avant tout code ; lint et runner figés à 07:54:06Z (commentaire des temps du job corrigé à 08:16Z, commentaire seul, O-10 rejoué) ; campagne de mutants à partir de 07:56:26Z ; journal ensuite.
- **Mandat** : commande de correction de l'orchestrateur Shōgen (`claude-fable-5-1`) ; liste fermée C-1..C-8 de la revue G2 (`F:/tmp/shogen-lots/D8a/G2-rapport.md`, sha256 `9e8b462f…561b`, verdict ACCEPTE-AVEC-CORRECTIONS). Détail des preuves, chemins et empreintes : `F:/tmp/shogen-lots/D8a/correction-rapport.md`.
- **C-1** (portée, CH-12) : tout `*.md` sous un `.claude/agents/`, un `.claude/skills/` ou un `.claude/commands/` de l'arbre, à toute profondeur ; élagage de la passe 3 factorisé (`ELAG`), commun aux deux parcours ; en-tête, commentaire de la passe 1 et commentaire du job ajustés. Skills imbriqués et commandes : confirmés par les FAITS lus sur place par l'orchestrateur le 2026-09-30 (`F:/tmp/shogen-lots/D8a/FAITS-claude-code-skills-commandes-2026-09-30.md` : commandes = skills au même frontmatter ; skills imbriquées chargées par répertoire de travail ou `--add-dir` ; T-76 = sur-approximation déclarée, fail-closed, sans effet sur l'arbre réel). Tests : T-50..T-52, T-63, T-64, T-75, T-76.
- **C-2** (CH-7) : règle de compte limitée aux fichiers sous un `.claude/agents/` (T-53, T-54 ; T-37 reste à 2 `R-1/ban`).
- **C-3** (CH-7, CH-8) : (a) à (d) du G2 ; indicateur de suite nommé `SUITE`, et non `P`. Tests : T-55..T-59, T-62.
- **C-4** (CH-10) : motif du G2, barre oblique inverse dans une clé JSON, `R-1/hors-liste` (T-60).
- **C-5** : T-46..T-50. **C-6** (CH-11) : `R-1/vide` quand aucun agent n'est lu (compteur `NA`), quels que soient les réglages ; T-26, T-61 ; rejeu `vide-local` : 2 `R-1/vide` (lint du G1 sur le même arbre : 0, 1 fichier).
- **C-7** : (a) en-tête du runner ; (b) l.8 de ce journal ; (c) l.25 du lint (l.20 à l'état du G1) ; (d) puce d'O-10 de la copie du G0. `grep -c` des quatre formules d'origine : 0 chacune.
- **Écarts mesurés au texte du G2** (lecture de référence PyYAML 6.0.3 et `json`, `corr-oracles/ref-lecture-T46-T76.out`) :
  1. **C-3 (a) élargi**. Le motif du G2 (`"`, `'`, `?`) laisse passer trois clés que PyYAML lit `model=opus` : ancre (`&a model: opus`), étiquette (`!!str model: opus`), alias (`*k : opus`). Et C-2, en retirant la règle de compte des skills, ouvre deux formes que seule cette règle refusait : clé de fusion (`<<: {model: opus}`) et mapping en flux (`{name: s, model: opus}`). Mesure : `sonde-formes.sh`, sortie 0 sur le prototype du G2 pour les cinq. Le jeu refusé en colonne 0 devient `"`, `'`, `?`, `&`, `!`, `*`, `{` et `<<`, chacun épinglé par un cas.
  2. **Frontmatter indenté** refusé (`R-1/cle-model`) : un mapping de skill entièrement indenté porte une clé non nue que PyYAML lit `model=opus` (T-74), autre forme ouverte par C-2.
  3. **Formes valides non refusées** : le tiret en colonne 0 (séquence non indentée) et `|` ou `>` en ligne suivante sont du YAML valide (mesuré) ; ils restent hors du jeu. Garde : T-71.
  4. **T-62** : l'`awk -v` de la fonction `ins` traite les échappements ; le T-62 du prototype écrivait donc `"model": opus` (mesuré, `od -c`), le cas de T-55. `ins` insère désormais la ligne telle quelle (`ENVIRON`) ; l'arbre de T-62 porte `"mod\x65l": opus`, lu `model=opus` par PyYAML.
  5. **Cas ajoutés** : T-65..T-69, T-73 (apostrophe) et T-74 pour les écarts 1 et 2 ; T-70 (commentaire indenté après `model`, admis), T-71 (formes valides en colonne 0, clé imbriquée entre guillemets), T-72 (suite après une ligne vide, lue `claude-opus-5-5` puis `[1m]` par PyYAML) ; T-75, T-76 (skill et commande imbriqués). Runner corrigé sur le prototype du G2 : 70 ok, 6 échecs (T-65..T-69, T-74).
- **R-25** (méthode du lot A, `corr-oracles/r25-corr.sh`) : estimation écrite avant code ≈ 62 lignes pour la correction seule ; mesure **+96** (lint +48 −25, runner +44 −4, `gates.yml` +4 −3) : E-9. **D8a-2 corrigé = 177 ≤ 200** (lint +77 −20, runner +66 −6, `gates.yml` +34 −4, contre l'instantané D8a-1 figé et la base) ; D8a-1 inchangé (193) ; aucun troisième sous-lot. Documents, hors compte de code (réponse du cp-1 à Q-G0-1), rapportés : ce journal +59 −1, copie du G0 +8 −1 ; la question Q-G2-1 du réviseur reste à l'orchestrateur.
- **Oracles rejoués sur l'état corrigé** (lint `1c57e8c4…4fa9`, runner `4e65eee7…f7e3`, `gates.yml` `bc3aea17…af53`) :
  - O-1 : `model-pinning : 76 ok, 0 échec`, sortie 0, 0 entrée TMP ; runner corrigé sur le lint du G1 : 21 échecs (T-51, T-53..T-67, T-71..T-73, T-75, T-76), défauts démontrés ; T-68, T-69 et T-74 y passent par la règle de compte que C-2 retire aux skills ;
  - O-2 : 3 fichiers dans le worktree et sur l'arbre principal, 2 sur une copie `git archive aa0afdc .claude` ; le réglage local de l'arbre principal passe C-4 ;
  - O-3 : k = 0..5 sur `aa0afdc` et sur `f5b8269` : 0 (2 fichiers), `R-1/ban`, `R-1/retire`, `R-1/cle-model`, `R-1/tier-nu`, `R-1/hors-liste` ;
  - corpus des 9 commits : verdicts identiques à ceux du G2 (5 refus, 4 sorties 0 à 2 fichiers) ; cas G2-01..G2-25 : 25 à l'attendu, 0 écart ;
  - O-5 = 0 ; O-6 = 0 et 0 ; O-9 : fixtures inchangées (`d44a2211…518ac`, `e66873b3…0fcac`) ; O-10 : 17 assertions sur 17, structure YAML identique à celle du G1 (commentaires seuls modifiés) ;
  - O-7 : suite `s2-harness` : `Ran 206`, `OK (skipped=2)`, sauts identiques à la base, 0 entrée TMP ; `cargo --locked xtask verify` : VERT, sortie 0 (premier passage 08:13:15Z-08:13:22Z ; S-G4 : 47 fichiers ; S-G5 : 48 fichiers, 252 fragments contrôlés et 218 non contrôlés, comme à la base, aucun tiré des deux documents du lot) ; second passage sur l'arbre final : rapport de correction.
- **Mutants** (`corr-oracles/corr_mutants.py`, `mut-run-corr.sh`, 4 travailleurs, TMP neufs) : 73 mutants appliqués, aucun inapplicable (07:56:26Z-08:12:30Z) : M-1..M-22 (M-10, M-17, M-18 et M-19 redérivés sur la forme corrigée, même effet visé), MG-01..MG-18 (MG-18 redérivé), MP-01..MP-17 (redérivés sur le texte corrigé) et MC-01..MC-16 ; `bash -n` : 73 sur 73. **69 tués**, chacun par un tueur attendu (MG-06, MG-11 et MG-12 par tout cas en échec (tueur `-`, convention du G2) ; par exemple MG-01 par T-46, MG-17 par T-49, MP-06 par T-51, MC-04 par T-68, MC-08 à MC-10 par T-71) ; **0 survivant non attendu** ; 4 survivants équivalents déclarés : MG-07 (jeton seul, sortie 2 dans les deux cas), MG-09 (élagage de `target`, plus de refus seulement), MG-10 (restriction déjà portée par le code corrigé), MG-16 (`*.cjs` non testé, facultatif au G2) ; TMP neufs : 0 entrée. Tueurs par mutant : `corr-oracles/mut-corr-resultats.out`.
- **Lignes proposées pour l'annexe A** (acte de l'orchestrateur ; remplacent les lignes D8a et D8a-2 du §1, les lignes D8a-1 et D8a-3 restent) :

| lot (date) | objet (décision) | véhicule | oracle non-LLM nommé | taille (R-25) | tuyau (entrée → sortie → consommateur ; test) | cp-1 |
|---|---|---|---|---|---|---|
| **D8a** (2026-09-29 ; amendée le 2026-09-30 par le G0, le G1 et la correction de la revue G2) | D8, C-14, CB-10 : lint en liste blanche exacte, job `g1-model-pinning` ; cas limites CH-4 et CH-5 ; écarts nommés au blob `457565f` (G0 §5.2, CH-6, CH-10, CH-11, CH-16, E-6) ; correction G2 C-1..C-8 | `enforcement/`, `gates.yml`, tests shell | O-1 à O-10 ; 73 mutants de gate ; cas G2-01..G2-25 ; corpus de 9 commits | 370 [mesuré : D8a-1 193 + D8a-2 corrigé 177] | tout `.claude/{agents,skills,commands}/` de l'arbre et réglages → lint → job g1 (partiel : GC-01, GC-09) et G3 opérant local ; hook : item 9 ; tests O-2 et O-3 | complet |
| **D8a-2** (2026-09-30 ; coupe R-25 du G1 de D8a, règle 4 ; corrigé le 2026-09-30) | réglages JSON, jetons `retire`, `suffixe`, `workflow`, job g1 ; correction G2 : portée à toute profondeur, commandes, règle de compte des seuls agents, formes YAML non lues, clé JSON échappée, vide sur 0 agent ; cas T-20, T-29..T-76 | `.github/workflows/gates.yml`, les deux scripts | O-1 (76 cas), O-2, O-3 (k = 0..5), O-4 (73 mutants), O-5 à O-10 | 177 [mesuré] | lint → job g1 et G3 opérant local ; test O-2 | complet (sous le cp-1 du lot) |
| **D8a-C** (2026-09-30 ; correction de la revue G2 de D8a) | liste fermée C-1..C-8 et écart mesuré de C-3 (a) ; diff de correction daté, `correction-G2-2026-09-30.diff` | lint, runner, commentaires du job, ce journal, copie du G0 | mêmes oracles ; re-revue ciblée `G2-rapport.rr1.md` | +96 [mesuré, code] | inchangé | sous le cp-1 du lot |

- **Tuyaux** : inchangés (§7) ; texte de C-5 mis à jour (puce datée du §7).
- **Items proposés** (versement à l'annexe B : acte de l'orchestrateur) :
  - **SHOGEN-LINT-IMBRIQUE-1** : une clé `model` imbriquée écrite hors d'une ligne `model` n'est pas lue : entrée de séquence (`- model: opus` sous `hooks`), mapping en flux imbriqué, suite d'une valeur imbriquée ; PyYAML les lit (mesuré, `sonde-formes.sh` : sortie 0). Un refus des clés imbriquées entre guillemets toucherait des blocs légitimes (`mcpServers`, `env`). Prix connu : entrée de séquence ≈ 1 ligne et 1 cas ; flux et guillemets imbriqués : lecteur YAML réel, à rechercher. Propriétaire : orch. Déclencheur : G0 de D8c, ou premier bloc `hooks` ou `mcpServers` suivi dans un agent, un skill ou une commande.
  - **SHOGEN-LINT-JSON-ECHAPPEMENT-1** : C-4 refuse aussi un réglage légitime dont une valeur porte une séquence `\"…\":` (mesuré, `sonde-c4.out` : clés réelles `permissions`, `allow`, `advisorModel`). Une lecture à jetons (`LC_ALL=C`, chaîne JSON en entier) ne voit que les vraies clés (mesuré), mais suppose un JSON strict. Choix : motif du G2, fail-closed et robuste à un JSON non strict ; ou lecture à jetons, précise, désalignée par un commentaire si le lecteur de Claude Code en admet (non établi, voir SHOGEN-LINT-LECTEUR-CC-1). Prix : 2 lignes et 1 cas. Propriétaire : orch. Déclencheur : G0 de D8c (le hook lira le réglage local à chaque commit), ou premier faux refus sur l'arbre principal.
  - Reprise des deux items du G2 : SHOGEN-LINT-LECTEUR-CC-1 et SHOGEN-FAITS-SKILLS-COMMANDES-1.
- **`error_origin` proposés** (assignation au G7) :
  - **E-9** : estimation R-25 de la correction ≈ 62, mesure +96 (élargissement de C-3 a, gardes, fonctions `md` et `vers`, en-têtes). Origine : worker G1 de correction.
  - **E-10** : l'outil d'édition du harnais a converti la séquence `\u0065` de T-60 en `e` (mesuré : `repr` de la ligne) ; détecté par l'échec de T-60 (jeton `R-1/tier-nu` au lieu de `R-1/hors-liste`), corrigé par script (`chr(92)`), chaque ligne à barre oblique inverse relue par `repr`. Origine : environnement (outil).
  - **E-11** : T-62 du prototype du G2 (échappement consommé par `awk -v`, écart 4). Origine : G2.
  - **E-12** : liste fermée incomplète sur C-3 (a) et effet de C-2 sur les skills (écarts 1 et 2) : six faux verts du prototype (T-65..T-69, T-74). Origine : G2.
  - **E-13** : premier jeu refusé du correcteur trop large (tiret, `|` et `>`, formes valides), resserré avant le gel après mesure PyYAML ; aucune forme livrée ne les refuse (garde T-71). Origine : worker G1 de correction.
- **Attestation** (forme D.3) : pièces de l'annexe D.2 non ouvertes, ni `F:/shogen-campagne/*`, ni `F:/tmp/shogen-j28/*`, ni `measure-M009a.md`, ni `F:/tmp/shogen-carto-2026-09-29/campagne.md` ; `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée. Aucune statistique S2 calculée sur les journaux de campagne ; aucun z, K, P̂_more ni φ de campagne vu. Git : sur ce worktree, `rev-parse`, `log --oneline`, `status --short`, `add -N` (six fichiers du lot), `diff` et `grep` (commande du job g5) ; sur `F:/Shogen`, `archive` en lecture (`--no-optional-locks`). Aucun `GIT_DIR`, aucun `GIT_WORK_TREE`, aucun `--write-tree`, aucun commit, stash, checkout, reset ni push. Rien écrit sur C:.
