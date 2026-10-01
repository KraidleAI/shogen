# G0 — lot D8c d'ADR-0028 : hook pre-commit versionné (`enforcement/hooks/pre-commit`), installeur vérifié, motif g5 élargi, note « collision ADR-0020 » — Shōgen, document de planification

- **Statut** : G0 proposé, soumis au **cp-1 complet** (annexe A l.38, colonne cp-1 = « complet »). Aucun code livrable n'est écrit par ce document. Les scripts de `g0-mesures/` sont des sondes de mesure ; l'un d'eux, `proto-pre-commit.sh`, est un prototype de composition déclaré **non livrable** (il ne sert qu'à mesurer la faisabilité et le coût du CH-7 et du CH-8).
  - *Amendement daté du 2026-09-30 (G1 du lot, `claude-opus-5-5`)* : G0 accepté au cp-1 complet avec les corrections C-1 à C-5 (commande de mission du G1 ; Q-G0-1 tranché par le validateur : port). Le texte accepté est conservé à l'identique (sha256 `4193e2b0185adcb3f399422ef426f6a312b91442e14921ff3394563d5925ccd4`, `F:/tmp/shogen-lots/D8c/G0-lot-D8c.md`) ; chaque fait mesuré au G1 qui supplante un point est une puce datée placée sous ce point. Le `diff -u` entre le texte accepté et cette copie est livré avec le G1 (`F:/tmp/shogen-lots/D8c/oracles/G0-copie.diff`, 0 ligne retirée). Journal : `docs/G1-lot-D8c.md`.
  - *Amendement daté du 2026-10-01 (correction de la revue G2 du lot, `claude-opus-5-5`)* : puces datées ajoutées sous les points que la revue G2 supplante (§2, §3, CH-14, CH-15, §7.1, §7.4, §10, §11.2, §13.1), aucune ligne retirée ; `diff -u` du texte accepté vers cette copie : `F:/tmp/shogen-lots/D8c/corr/o/G0-copie.diff`. Journal : `docs/G1-lot-D8c.md` §15.
- **Rédacteur** : worker G0 `claude-opus-5-5` (modèle résolu déclaré en tête de session, R-1), effort max, contexte frais. Destinataire : orchestrateur Shōgen `claude-fable-5-1`. Réviseurs attendus : orchestrateur (R-21), puis validateur-humain (cp-1 complet). Advisor intégré consulté une fois, après l'orientation et avant la rédaction (canal 1).
- **Horloge** (`date -u`) : orientation avant la première heure relevée (20:49:25Z) ; `g0-mesures/horloge-debut.txt` à 20:49:58Z ; sondes de 21:00:39Z (environnement du hook) à 21:2xZ ; rédaction à partir de `g0-mesures/horloge-redaction.txt` ; sceau au §15.
- **Mandat** : commande de mission de l'orchestrateur (workflow du 2026-09-30), lot D8c de l'annexe A. Base de mission : `40b4cfb`. `main` est à `293b7a7` au moment des mesures : un commit de plus, `JOURNAL.md` seul (`git show --stat 293b7a7`). Empilement : D8a commis (`de12b8b`, `84e0462`, puis `7425a49` pour ses documents) ; D8b non commis, diff `F:/tmp/shogen-lots/D8b/lot.diff` (sha256 `ce90419714b0f7d66035f34336b1b5f32f032aa61080216bf8912f90be768e9e`), qui est l'état corrigé de sa revue G2 (§5.1 h). Lecture seule sur `F:/Shogen` ; aucun worktree utilisé.
- **Isolation git** : aucun `GIT_DIR`, aucun `GIT_WORK_TREE`, aucun `--write-tree` posés par le rédacteur ; aucun commit, add, stash, checkout, reset ni push sur `F:/Shogen`. Commandes git sur `F:/Shogen` : `log`, `rev-parse`, `show`, `ls-files`, `ls-tree`, `grep` (sur des commits), `archive` (vers `F:/tmp`), `hash-object` sans `-w`, `config --get`, `worktree list`, `reflog show`, en `--no-optional-locks` sauf l'écart ci-dessous. Clone VibeGates du corpus (C:, lecture seule) : `rev-parse`, `log`, `ls-tree`, `diff`, `show`, `grep`, en `--no-optional-locks`. `init`, `add`, `commit`, `worktree add`, `cherry-pick`, `merge`, `rebase`, `revert`, `reset`, `rm --cached` : dans les seuls dépôts jetables `mktemp` sous `F:/tmp/shogen-tests-tmp/d8c-g0/`, supprimés à la sortie de chaque sonde. Dans un arbre lié, git pose lui-même `GIT_DIR` dans l'environnement du hook (§5.1) : ce n'est pas un acte du rédacteur.
  - **Écart déclaré** : `git status --short` lancé une fois sur `F:/Shogen` à l'orientation (vers 20:45Z), sans `--no-optional-locks`. Mesuré ensuite : `.git/index` à 16:37:55Z et `refs/heads/main` à 16:37:24Z (commit `293b7a7`), inchangés ; mtime du dossier `.git` à 20:45:28Z, attribuable à cette commande ou aux worktrees actifs (`wf_1c82774a-d5f-18`, verrouillé, à `293b7a7`). Même forme que les écarts des G0 de D8a et de D8b. `error_origin` proposé : worker G0.
  - **Refus du garde du harnais** (vers 21:1xZ) : une première version de `sonde-hook-couverture.sh`, qui nommait l'option de contournement de `git commit`, a été refusée par le PreToolUse global (`gate-commit.ps1` du corpus, R-22). Le fichier n'a pas été écrit ; le cas a été retiré, non contourné ; la sonde a tourné sans lui (§5.1 f).
- **Écritures** : `F:/tmp/shogen-lots/D8c/` seulement (ce document ; `g0-mesures/`, scellé au §15 ; `work/arbre/`, extraction `git archive 293b7a7 ':!biblio'` plus D8b appliqué, fins de ligne ramenées en LF) et dépôts jetables sous `F:/tmp/shogen-tests-tmp/d8c-g0/` (compte restant au sceau). Rien sur C: : `/tmp` de Git Bash résout vers `F:\tmp` (`cygpath -w /tmp`, mesuré).
- **Interdits (annexe D.2 et D.4 a)** : aucune pièce de D.2 ouverte ; `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée ; aucune statistique S2 lue ni calculée. Les `git grep` du §5.3 sur l'arbre n'ont imprimé que des comptes. Aucun z, K, P̂_more ni φ vu.

## 0. Résumé (une phrase par tâche, CA-1)

1. **Versionner** le hook pre-commit en `enforcement/hooks/pre-commit`, **porté** (non copié octet pour octet) du blob `9c4c846`, avec pour étape R-13 l'image locale exacte du job g5 élargi, lue dans l'index (D8c-1).
2. **Installer** par `enforcement/hooks/install-pre-commit.sh`, qui copie le blob committé vers le dossier des hooks après contrôle de sha256, refuse tout hook inconnu et vérifie la copie ; il n'est lancé par le lot que dans des dépôts jetables (D8c-1).
3. **Élargir** le motif g5 à celui d'`adb2213` (l.39) et faire tourner le runner du hook dans le job g5 (D8c-1).
4. **Consigner** la collision ADR-0020 par une note datée sous le titre ADR-0020 de `docs/DECISIONS.md` (D8c-1, documentation).
5. **Brancher** dans le hook le lint d'épinglage (sur une extraction de l'index) et la gate secrets (mode indexé) : ce sont les consommateurs 2 de D8a et de D8b (D8c-2).
6. **Trancher** SHOGEN-LINT-IMBRIQUE-1 et SHOGEN-LINT-JSON-ECHAPPEMENT-1 : les formes lisibles ligne à ligne sont construites en refus fail-closed, et la lecture JSON passe aux jetons, avec une garde de résidu (D8c-3).

**Point de bascule, à trancher au cp-1 (Q-G0-1).** Une copie octet pour octet du hook local **rougit g5**, au motif courant (l.73) comme au motif élargi (l.70 et l.73) : c'est mesuré (§5.2). Il n'existe donc pas de copie fidèle sans autre acte. Ce G0 retient le port à écarts nommés ; l'autre voie, la copie assortie d'une exclusion nommée dans g5, est écrite et motivée au CH-1.

Faits nouveaux (FM-2.4), tous mesurés au §5 :
- le mode harnais du hook est inerte sous git : le hook reçoit 0 octet sur son entrée, même quand un JSON arrive sur l'entrée de git ;
- git exporte `GIT_DIR` au hook d'un arbre lié, et les hooks sont partagés entre arbres : tout commit local d'un worker dans `.claude/worktrees/` passera par le hook installé ;
- `cherry-pick` et `rebase` ne lancent pas pre-commit ; une fusion sans avance rapide lance `pre-merge-commit` ;
- un `git apply` hors dépôt écrit du CRLF sous le `core.autocrlf=true` du système ;
- dans une commande tapée au harnais, une double barre oblique inverse est arrivée simple à bash, et une séquence d'échappement unicode décodée, sans que ce soit stable d'une commande à l'autre : seuls les octets écrits font foi.

## 1. Objet et décisions rattachées

| rattachement | lieu (à `293b7a7`) | ce qu'il fixe pour D8c |
|---|---|---|
| D8 | `docs/adr-0028/ADR-0028-decisions-sortie-S2.md` l.212-220 | lots D8a-c ; copie versionnée du hook pre-commit et motif g5 élargi (l.213) ; source canonique : blobs d'`adb2213`, hook `1da91c72…` (l.214) ; collision ADR-0020 consignée à DECISIONS, cause sessions concurrentes, `error_origin` orchestrateur (l.219) ; tag puis suppression, acte de l'investisseur (l.220) |
| ligne de lot | `docs/adr-0028/ANNEXE-A-lots.md` l.38 | véhicule `enforcement/`, `gates.yml`, `docs/DECISIONS.md` ; oracle : sonde du hook (git-ci §2.e) ; ≈ 120 = 78 [mesuré] + ≈ 40 [inféré] ; tuyau hook versionné → commits ; cp-1 complet |
| items à déclencheur « G0 de D8c » | annexe B.11 l.196-198 ; `docs/G1-lot-D8a.md` §11 l.286, l.288, l.292 ; journal de D8b (non commis ; extraction de `lot.diff`) l.369, l.373, l.465-468 | douze items, tranchés au §11.1 |
| précondition | ADR-0028 l.279 ; `JOURNAL.md` l.122 | PC-1 : lecture (b) consignée (couvert par la délégation, veto non exercé, révocable), qui nomme le hook versionné et les jobs g1/g3/g5 ; la confirmation explicite reste à l'investisseur (§2) |
| G3 opérant | ADR-0028 §4.11 l.286-295 ; `JOURNAL.md` l.141 | oracle local rejoué par l'orchestrateur ; forge arrêtée faute de paiement, passage public = acte de l'investisseur |
| menaces | `docs/17-modele-de-menace.md` l.68 (T-10), l.69 (T-11), l.70 (T-12), l.82 | le G0 de D8c cite les T-xx qu'il traite (§13.2) |
| portage | `docs/adr-0028/ANNEXE-B-items.md` l.24 | SHOGEN-ENFORCEMENT-PORTAGE-1 : D8a, D8b, D8c, puis tag, puis suppression |
| RUNNERS-1 | annexe B l.80 | image flottante et checkout v4.4.0 du job `g5-dette` : CH-10 |
| avis | AVIS-advisor Q8 l.93-99, pt 3 l.99 (sha256 `87e04420…c047`, égal à la citation d'ADR-0028) | contenu de l'entrée « collision » : cause mesurée, contenu reporté sous le numéro neuf, état réel de la décision du 2026-08-20 ; pas de renumérotation de l'ADR-0020 de `main` |
| corpus | doc 02 l.98 (R-13), l.109 (R-20), l.111 (R-22) | marqueurs de dette nus interdits dans le code intégré ; seul l'orchestrateur committe ; gates non discrétionnaires |

## 2. Précondition PC-1 (§4.10 a) — lecture (b) consignée, elle couvre D8c

- `JOURNAL.md` l.122 (2026-09-30, 04:5x UTC) consigne la lecture (b) : le portage `enforcement/`, soit le lint, la gate secrets, le hook versionné et les jobs g1/g3/g5, est couvert par la délégation du 2026-09-30, veto §4.10 a non exercé, révocable jusqu'à l'exécution unique. D8c y est nommé par son contenu.
- Restent des actes de l'investisseur : la confirmation explicite de la décision du 2026-08-20 (forme (a) du §2 du G0 de D8a ; annexe E l.31, E-D8c), puis le tag `archive/roster-ban-2026-08-20` sur `adb2213` et la suppression de la branche (SHOGEN-D8-PC-1, annexe B l.201). La lecture (b) n'est pas une confirmation. D8c ne les touche pas ; la note de DECISIONS les cite (CH-14).
  - *Amendement daté du 2026-10-01 (correction de la revue G2, C-G2-1)* : ces actes sont faits pendant le G1 du lot. L'investisseur a confirmé la décision le 2026-09-30 à 23:33 UTC (forme (a) ; JOURNAL, commit `87bc4e4`) ; l'orchestrateur a posé le tag annoté `archive/roster-ban-2026-08-20` sur `adb2213` (23:33:51 UTC), puis supprimé la branche et son journal de refs : SHOGEN-D8-PC-1 est fermé. La note de DECISIONS est mise à cet état (CH-14).
- Si le veto est exercé avant le commit : D8 passe en ADR de retrait, le worktree est abandonné, aucun commit, et le hook n'est pas installé.

## 3. Périmètre

**IN**

| fichier | nature | sous-lot |
|---|---|---|
| `enforcement/hooks/pre-commit` | neuf ; porté du blob `9c4c846` (CH-1 à CH-4) | D8c-1 ; étapes lint et secrets en D8c-2 |
| `enforcement/hooks/install-pre-commit.sh` | neuf (CH-5) | D8c-1 ; empreinte attendue mise à jour en D8c-2 |
| `enforcement/tests/run-fixtures-hooks.sh` | neuf ; dépôts jetables, commits réels ; cas H, I, C du §7 | D8c-1, D8c-2 |
| `.github/workflows/gates.yml` | bloc `g5-dette` : motif élargi, étape du runner, image, checkout, borne de temps (CH-9, CH-10) ; en-tête l.3-8 et l.19-20 | D8c-1 |
| `enforcement/lint-model-pinning.sh` | formes imbriquées (CH-12), lecture JSON à jetons (CH-13), en-tête l.21-24 | D8c-3 |
| `enforcement/tests/run-fixtures-model-pinning.sh` | cas T-77 et suivants (§7.4) | D8c-3 |
| `docs/DECISIONS.md` | note datée sous le titre ADR-0020 (CH-14) | D8c-1 (documentation) |
| `docs/G1-lot-D8c.md` | journal G1, au format de `docs/G1-lot-D8a.md` | tous |
| `docs/adr-0028/G0-lot-D8c.md` | copie de ce G0 (précédent de D8a et de D8b) | tous |

**OUT**, avec motif :
- `.git/hooks/pre-commit` de `F:/Shogen` : jamais modifié par le lot, ni par le G1, ni par le G2. L'installation est un acte de l'orchestrateur, après le G7 du dernier sous-lot (CH-6, Q-G0-4). Rappel mesuré : les hooks sont partagés, un installeur lancé dans un worktree de `F:/Shogen` écrirait dans `F:/Shogen/.git/hooks` (§5.1 e).
- `.claude/` et les agents : entrée des tuyaux, jamais touchés.
- Gate secrets (`enforcement/gate-secrets.sh`) et son runner : pièces de D8b. Les cinq items que D8b route vers ce G0 (messages, noms de chemin, chemin d'étage, statut de `grep`, masquage) passent au lot proposé **D8d** (§11.1, Q-G0-6).
- Jobs g1, g3 et s2 de `gates.yml`, et les onze autres définitions de job de RUNNERS-1.
- Mode harnais (PreToolUse) : servi sur cette machine par `gate-commit.ps1` du corpus, depuis les réglages globaux (§5.1 g) ; hors dépôt.
- `pre-merge-commit`, `cherry-pick`, `rebase` : item SHOGEN-HOOK-COUVERTURE-1 (§11.2). `main` refuse les fusions (`required_linear_history`, git-ci l.179).
  - *Amendement daté du 2026-10-01 (correction de la revue G2, C-G2-9)* : prémisse retirée. Depuis la méthode par parties (`docs/adr-0028/PARTIES-S2.md` l.19, adoptée le 2026-10-01, JOURNAL), `main` reçoit chaque partie par un commit de fusion `--no-ff`, qui lance `pre-merge-commit` et non pre-commit (sonde de fusion de la revue G2) ; item 2 du §11.2 re-formé.
- Suite `s2-harness` et workflows cargo dans le hook : item SHOGEN-HOOK-SUITE-S2-1 (§11.2) ; le hook est l'image des trois gates textuelles de `gates.yml` (g5, g1, g3), pas de tout le workflow.
- Index de `docs/DECISIONS.md` (il s'arrête à ADR-0023, l.27 ; REG-02 ; acte 4 du §8 d'ADR-0028) : non touché, signalé.
- `docs/17-modele-de-menace.md` : les lignes T-10 (l.68) et T-12 (l.70) sont périmées sur `main` (le lint y est depuis `de12b8b`) ; texte proposé au journal G1, acte de l'orchestrateur (§11.2).
- `s2-harness/`, ADR-0028 et ses annexes : les lignes datées des sous-lots sont un acte de l'orchestrateur (ADR-0028 §6, l.307).
- `docs/AUDIT-ENTREE.md` l.42-43 (G5 mécanisé par la CI et deux hooks) : inchangé, le hook git reste.

## 4. Sources lues (niveau, lieu)

| source | lieu | niveau | usage |
|---|---|---|---|
| hook local | `.git/hooks/pre-commit`, 78 l., 3 487 o, sha256 `1da91c723b7f4747edb35dcc2cce7492e334b648c5e00c41f239cca5ab61277d`, blob `9c4c846` (`hash-object` sans `-w`), 0 octet CR | [lu] en entier | l.1-13 (en-tête : deux modes et leurs revendications), l.15-51 (mode harnais), l.53-55 (exclusions), l.56-68 (mise en scène), l.70-71 (classe de marqueurs), l.72-78 (verdict) |
| amont VibeGates | clone du corpus `…\vibegates` (HEAD `1263f2a`) : `52a569d:enforcement/gate-commit.sh` = blob `9c4c846` ; `0b4f3f9:enforcement/gate-commit.sh` = blob `9dade29` (136 l., sha256 `18984c60ca4312de5920eb890eeb7b109cae78da1bfedf80333d9db07b597e24`) ; `docs/adr/ADR-0010-section7-adjudication-retire-commit-guards.md` à `0b4f3f9`, l.1, 6, 11, 15, 22, 26, 31 ; liste de `enforcement/hooks/` à `0b4f3f9` | [lu] | provenance ; revendication de garde de commit retirée par l'amont ; condition de réduction ; le dossier amont `enforcement/hooks/` porte des hooks du harnais, pas de hook git |
| `gates.yml` | `293b7a7` l.1-122 (sha256 `bc3aea17…af53`) ; état après D8b (extraction, sha256 `13dc5177…79fb`) ; `adb2213` (blob `493ae8c`) l.31-43 | [lu] | g5 l.34-53 ; motif élargi `adb2213` l.39 |
| lint committé | `enforcement/lint-model-pinning.sh` (sha256 `1c57e8c4…4fa9`) l.21-24, 34-37, 81-106, 108-126 | [lu] | CH-12, CH-13 |
| runner du lint | `enforcement/tests/run-fixtures-model-pinning.sh` (sha256 `4e65eee7…f7e3`) l.27-52, 100-134 | [lu] | forme des cas |
| gate secrets, état corrigé de D8b | extraction : `enforcement/gate-secrets.sh` (sha256 `47f2c35e…1722`) l.8-31 (portée, hors portée, échec fermé), l.50-55, l.80-84, l.110-140 | [lu] | mode indexé, `cd` à la racine, exclusions de contrat |
| D8a | G0 (`docs/adr-0028/G0-lot-D8a.md`, sha256 `a5d70848…81e7`) §5.1, §6, §10, §11 ; journal (`docs/G1-lot-D8a.md`, sha256 `d466a140…383a`) §11 l.283-296 ; rapport de correction §8 l.119-120 et ses sondes `corr-oracles/sonde-formes.sh`, `sonde_yaml.py`, `sonde-c4.py`, `sonde-c4-segments.sh` | [lu] | items B.11, formes mesurées |
| D8b | G0 (`F:/tmp/shogen-lots/D8b/G0-lot-D8b.md`, sha256 `2b928edd…13c8`) §3, §10, §11 ; journal (extraction, sha256 `3f3dd394…2017`) l.78, 318, 363-373, 465-468 ; rapport de correction (sha256 `0a8ce413…7df6`) §0-§2 | [lu] | consommateur 2, items routés vers ce G0 |
| cartographie git-ci | `F:/tmp/shogen-carto-2026-09-29/git-ci.md` (sha256 `9203d737…d3`) l.23, 90-119, 167-181 | [lu] | P7, §2.b, §2.e |
| avis | AVIS-advisor Q8 l.86-105 | [lu] | CH-14 |
| ADR-0028, annexes A, B, C, E | lignes citées au fil du texte | [lu] | cadre |
| JOURNAL | l.31, 122, 137, 141 | [lu] | tir contrôlé du hook le 2026-08-13 ; PC-1 ; D8a accepté ; fait investisseur sur la CI |
| DECISIONS | `293b7a7` l.1-27 (index), l.3054-3056 (titre et statut d'ADR-0020) ; `adb2213` l.24 et l.3051-3077 (homonyme) | [lu] | CH-14 |
| modèle de menace | `docs/17-modele-de-menace.md` l.34-51, 59-70, 82 | [lu] | §13.2 |
| corpus | doc 02 l.98, 108-111 ; `templates/ci-gates.yml` l.82-88 | [lu] | R-13, R-20, R-22 ; le gabarit g5 est un emplacement vide |
| réglages globaux | `F:/claude-config/settings.json` : fragments seuls (commande et filtre du PreToolUse), par `grep -o` ; aucun autre contenu affiché | [mesuré] | mode harnais servi ailleurs |
| gates xtask | `xtask/src/sg4.rs` l.36-92 et l.147 ; `xtask/src/sg5.rs` l.1-31 | [lu] | contraintes d'écriture de la copie de ce G0 (§15) |

Aucune source amont n'est versée à `biblio/INDEX.md` : ce document paraphrase l'amont VibeGates et n'en cite rien entre guillemets (S-G5).

## 5. Faits mesurés au G0 (`F:/tmp/shogen-lots/D8c/g0-mesures/`)

### 5.1 Environnement d'un hook pre-commit (`sonde-hook-env.sh`, `sonde-hook-couverture.sh`)

- **(a) Entrée standard** : non-tty, 0 octet, dans les quatre cas de `sonde-hook-env.out`, y compris quand un JSON de harnais arrive sur l'entrée de git (cas 2). Le mode harnais du hook local (l.28-51) ne s'active donc jamais sous git : `CMD` reste vide.
- **(b) Répertoire courant** : racine de l'arbre de travail, arbre lié compris.
- **(c) Index vu par le hook** : `GIT_INDEX_FILE` vaut `.git/index` (commit simple), `.git/index.lock` (`commit -a`), `.git/next-index-<pid>.lock` (commit avec chemin), `.git/worktrees/wt/index.lock` (arbre lié). `git diff --cached` et `git ls-files -s` lus dans le hook voient l'index du commit en préparation : le blob de `a.txt` diffère à chaque cas.
- **(d) `GIT_DIR`** : exporté par git au hook de l'arbre lié (cas 4), absent dans l'arbre principal.
- **(e) Hooks partagés** : depuis l'arbre lié, `git rev-parse --git-path hooks` désigne `<dépôt>/.git/hooks`.
- **(f) Couverture** (dépôt jetable, branche `main`) : `commit` et `commit --amend` lancent pre-commit ; `cherry-pick` et `rebase` n'en lancent aucun ; une fusion sans avance rapide lance `pre-merge-commit`, pas pre-commit ; `revert` sort en 128 dans la sonde, non conclusif. Le cas de l'option de contournement a été retiré (refus du garde, en-tête).
- **(g) Réglages globaux** : PreToolUse `Bash|PowerShell` vers `…\enforcement\gate-commit.ps1` du corpus, même relevé que git-ci l.175 ; ce garde a refusé une commande de sonde (en-tête).
- **(h) Pièges d'écriture** :
  - `git apply` hors dépôt a écrit les fichiers de D8b en CRLF (140 CR pour les 140 lignes de la gate) ; CR retirés, les sha256 sont ceux de l'état corrigé de D8b : gate `47f2c35e…`, runner `7eb01b39…`, fixture `6b558bd2…`, `gates.yml` `13dc5177…` (rapport de correction de D8b, §1) ;
  - dans les commandes tapées au harnais, une double barre oblique inverse est arrivée simple à bash, et une séquence d'échappement unicode (barre, lettre u, quatre chiffres hexadécimaux) est arrivée décodée, en commande directe comme dans un heredoc (`sonde-echappements.out`, `od -c`) ; une première écriture par heredoc de `sonde-json-d8c.sh` avait pourtant gardé la séquence unicode intacte : le comportement n'est pas stable d'une commande à l'autre, et seuls les octets écrits font foi ; une barre simple suivie d'une autre lettre est arrivée intacte ;
  - `grep -c` d'un CR sous Git Bash rend le nombre de lignes du fichier (145 sur le lint), alors que `tr -cd` y compte 0 CR.
- **(i) Temporaires** : `/tmp` de Git Bash vaut `F:\tmp` ; `mktemp -d` sans `TMPDIR` crée sous `F:\tmp`.
- **(j) Outillage local** : git 2.55.0.windows.5, GNU bash 5.3.15, GNU grep 3.0, GNU sed 4.9, Python 3.14.5, PyYAML 6.0.3.

### 5.2 Hook local et motifs g5 (`sonde-hook-local.sh`, `sonde-g5-motif.sh`)

- **Motif courant** (`gates.yml` l.49) : il reconnaît la l.73 du hook local. **Motif élargi** (`adb2213:gates.yml` l.39) : l.70 et l.73. g5 n'exclut que `biblio/`, `.claude/` et `.github/workflows/gates.yml` : une copie octet pour octet sous `enforcement/` rougit g5 dès aujourd'hui.
- La ligne qui porte le motif lui-même (celle d'`adb2213` l.39, et la même chaîne en affectation de variable) ne se reconnaît pas : 0 ligne sur 2.
- **Sonde git-ci §2.e rejouée** sur une copie du hook local (sha256 `1da91c72…`), dépôts jetables, marqueurs formés à l'exécution ; « direct » = hook lancé seul, entrée `/dev/null` ; « commit » = code de `git commit` :

| cas | fichier indexé | direct | commit | lecture |
|---|---|---|---|---|
| S1 | `docs/probe.md`, marqueur introduit par un dièse | 2 | 1 | bloqué |
| S2 | `docs/probe.md`, texte propre | 0 | 0 | accepté |
| S3 | `src/a.rs`, marqueur introduit par une double barre, suivi de deux-points | 2 | 1 | bloqué |
| S4 | `docs/probe.md`, marqueur suivi de deux-points, sans délimiteur | 0 | 0 | accepté par le hook, pris par g5 |
| S5 | `enforcement/x.sh`, marqueur introduit par un dièse | 0 | 0 | exclu du hook, balayé par g5 |
| S6 | `.github/workflows/x.yml`, idem | 0 | 0 | exclu du hook, balayé par g5 |
| S7 | `docs/probe.md`, commentaire HTML | 2 | 1 | bloqué |
| S8 | `docs/probe.md`, le mot dans de la prose | 0 | 0 | accepté |
| S9 | `.claude/agents/a.md`, marqueur introduit par un dièse | 2 | 1 | bloqué par le hook, exclu de g5 |

- **Motifs, par `git grep --cached -E` de Git for Windows** (`sonde-g5-motif.out`) : formes P1 à P9 (deux-points ; dièse, double barre, double tiret, point-virgule, ouverture de commentaire C, astérisque, commentaire HTML, dièse collé) : courant 1 sur P1 seulement, élargi 1 sur les neuf ; formes N1 à N5 (prose, pluriel, mot collé à gauche, texte du motif, message sans deux-points) : 0 aux deux ; N6, le message du hook local suivi de deux-points : 1 aux deux.
- **Non-recouvrement** : le hook et g5 ne se recouvrent ni en classe (S4) ni en portée (S5, S6, S9).
- **`9c4c846` contre `9dade29`** : en mode pre-commit (l.51-78 contre l.109-136), une seule ligne diffère, la condition de mise en scène, fausse dans les deux fichiers quand `CMD` est vide (`diff-mode-precommit-9c4c846-9dade29.txt`).

### 5.3 Arbre, coût et composition (`mesure-composition.sh`, prototype `proto-pre-commit.sh`)

- Motif élargi, exclusions de g5, sur `293b7a7` et sur `40b4cfb` : 0 occurrence ; sur les lignes ajoutées par D8b (`lot.diff`) : 0.
- Fichiers suivis : `.claude/` = 3 (deux agents, `launch.json`) ; 0 script `*.js`, `*.mjs` ou `*.cjs` ; `.vibegates-secretscan-exclude` absent ; `biblio/` = 1 fichier suivi.
- Taille des commits (40 derniers de `main`) : 1 à 11 fichiers, médiane 3, 90ᵉ centile 8.
- Dépôt jetable de 310 fichiers (`293b7a7` sans `biblio/`, plus D8b), prototype en hook, temps en millisecondes :

| scénario | image g5 | lint (extraction) | gate secrets (indexé) | commit |
|---|---|---|---|---|
| A : 1 fichier | 0 (57) | 0 (436 ; 3 fichiers extraits) | 0 (437) | 0 |
| B : 3 fichiers | 0 (57) | 0 (427) | 0 (730) | 0 |
| B : 8 fichiers | 0 (59) | 0 (471) | 0 (1 671) | 0 |
| B : 11 fichiers | 0 (59) | 0 (478) | 0 (2 155) | 0 |
| C : index `model: opus`, arbre de travail remis bon | 0 | **2** `R-1/tier-nu` | 0 | refusé |
| D : forme d'identifiant indexée | 0 | 0 | **2** `SECRETS/forme` | refusé |
| E : marqueur de dette indexé | **2** | 0 | 0 | refusé |
| F : arbre lié, 1 fichier ; `GIT_DIR` posé par git | 0 | 0 | 0 | 0 |
| G : `commit -a` (`index.lock`), puis commit avec chemin (`next-index-*.lock`) | 0 | 0 | 0 | 0 et 0 |

- Au scénario C, le lint lancé sur l'arbre de travail sort en 0 (2 fichiers) : un lint de l'arbre de travail laisserait committer l'index fautif. Coût par commit du hook composé : ≈ 1,2 s à la médiane (3 fichiers), ≈ 2,2 s au 90ᵉ centile (8), ≈ 2,7 s au maximum observé (11) [mesuré sur le dépôt jetable ; sommes des trois étapes].

### 5.4 Items B.11 rejoués sur le lint committé (`sonde-formes-d8a.sh`, `sonde_yaml_d8c.py`, `sonde-json-d8c.sh`, `mesure-reglage-local.sh`)

- **Formes imbriquées** (sonde de la correction de D8a, plus quatre formes ajoutées par ce G0) : le lint committé (sha256 `1c57e8c4…`) **accepte** les six (sortie 0) : entrée de séquence, suite d'une valeur imbriquée, mapping en flux imbriqué, clé imbriquée entre guillemets, séquence de flux, suite après un commentaire. PyYAML y lit un modèle hors liste pour cinq d'entre elles (`opus` quatre fois, `claude-opus-5-5 x` une fois) et lève une `ParserError` sur la sixième. Les formes de premier niveau (ancre, étiquette, alias, fusion, flux) restent refusées en `R-1/cle-model`.
- **Réglages JSON** (fichier construit à l'exécution ; colonne « jetons » = prototype de mesure : chaînes JSON entières sous `LC_ALL=C`, clés = jetons suivis de deux-points, résidu hors chaînes limité à la ponctuation et aux littéraux JSON) :

| cas | contenu | lint committé | jetons : clés, clés à barre, résidu | JSON strict (Python) |
|---|---|---|---|---|
| J1 | valeur légitime avec guillemet échappé suivi de deux-points | 2 `R-1/hors-liste` (faux refus) | 3, 0, vide | oui |
| J2 | clé échappée qui forme `model` | 2 | 1, **1**, vide | oui |
| J3 | `advisorModel` admis | 0 | 1, 0, vide | oui |
| J4 | commentaire, puis clé `model` à `opus` | 2 `R-1/tier-nu` | 2, 0, **non vide** | non |
| J5 | commentaire qui porte un guillemet isolé, puis `model` à `opus` | 2 `R-1/tier-nu` | **1** (clé masquée), 0, **non vide** | non |
| J6 | virgule finale | 0 | 1, 0, vide | non |
| J7 | clé `advisorModel` sans guillemets | 0 | 0, 0, **non vide** | non |
| J8 | valeur avec guillemet échappé, sans deux-points | 0 | 2, 0, vide | oui |
| J9 | clé `model` sans guillemets, valeur `opus` | **0** (trou du sens accepter) | 1, 0, **non vide** | non |

- Lecture : le motif C-4 donne un faux refus (J1) et laisse passer une clé non entre guillemets (J9) ; la lecture à jetons seule se désaligne sur un commentaire (J5 : la clé `model` disparaît) ; **la lecture à jetons avec garde de résidu** refuse J2, J4, J5, J7 et J9 et accepte J1, J3 et J8. Seule J6 (virgule finale) passe les deux lectures, sans effet sur les clés lues.
- **Réglage local réel** (`F:/Shogen/.claude/settings.local.json`, comptes seuls) : 1 146 octets, 19 lignes, JSON strict, 3 clés, 0 clé à barre, résidu vide, 0 segment du motif C-4, 1 clé de modèle.
- **Agents globaux** (copies de `F:/claude-config/agents/*.md`, `mesure-hors-depot.sh`) : 9 fichiers ; dans la disposition du dossier global, le lint sort en 2 `R-1/vide` ; replacés sous `.claude/agents/`, sortie 0, 9 fichiers.
- **Frontmatters réels** : une ligne `model` chacun, 0 clé `model` hors de la forme canonique.

### 5.5 Collision ADR-0020 (lecture seule : `reflog show`, `log -1`)

- Journal de refs de la branche `roster-ban-alignment-2026-08-20` : créée depuis `886adce` et commit `adb2213` à 2026-08-20T06:20:27+01:00 ; commit `60fd8e1` (walking skeleton du harnais S2) posé **sur la branche** à 08:20:27+01:00 ; branche ramenée à `adb2213` à 12:44:40+01:00.
- Journal de refs de `HEAD` : retour à `main` et report de `60fd8e1` par cherry-pick en `f11bdca`, à 12:44:22+01:00.
- `2d02276` (2026-08-20T16:54:27+01:00) porte l'ADR-0020 de `main` (paramètres ex ante de la campagne S2) : titre l.3054, statut l.3056 à `293b7a7`.
- L'homonyme vit à `adb2213:docs/DECISIONS.md` l.24 (index) et l.3051-3077 : application d'AgileGates, roster aligné du 2026-08-14, gates VibeGates g1, g3 et g5 élargi câblées.
- Ces faits recoupent git-ci §2.b l.98 ; ils ont été relus ici, sans rien écrire.

## 6. Choix tranchés (option retenue, motif, test)

- **CH-1 — Le hook est porté, pas copié octet pour octet.**
  - Retenu : `enforcement/hooks/pre-commit` neuf, qui garde du blob `9c4c846` la mécanique du mode pre-commit (lecture de l'index, marqueurs introduits par un délimiteur de commentaire, sortie 2 sur refus) ; écarts nommés aux CH-2 à CH-4.
  - Motifs :
    - (a) la copie octet pour octet rougit g5 (§5.2) ;
    - (b) son mode harnais est inerte sous git (§5.1 a) et servi ailleurs sur cette machine (§5.1 g) ;
    - (c) l'amont a lui-même retiré la revendication de garde de commit qui lit une chaîne de commande (VibeGates, ADR-0010 à `0b4f3f9`, l.11 et l.15, paraphrasés) ; versionner l'en-tête du blob, l.5-6, versionnerait une revendication retirée ;
    - (d) le hook local et g5 ne se recouvrent pas (§5.2) ; R-22 n'admet pas qu'un vert local soit rougi par la CI sur le même contenu.
  - Condition posée par l'amont : il n'admet une réduction de `gate-commit.sh` que contre une preuve par mutation (ADR-0010 l.22, paraphrasé). Le runner du lot tue donc les mutants de l'étape R-13 (MH, §8), et ne se contente pas de la sonde §2.e.
  - **Rejetée** : copie octet pour octet, plus une exclusion nommée dans g5 (`':!enforcement/hooks/pre-commit'`, sur le précédent de l'auto-exclusion de `gates.yml`). Motifs du rejet : une exclusion par chemin ouvre ce chemin aux marqueurs (raisonnement du CH-15 du G0 de D8b) ; elle versionne une revendication retirée et environ 35 lignes de code mort (l.16-51) ; elle laisse le non-recouvrement de classe et de portée. Si le cp-1 renverse CH-1 (Q-G0-1), le reste du plan tient : seul le texte du hook change, et le §9 perd environ 10 lignes.
- **CH-2 — Mode harnais retiré.** Le versionné ne lit pas son entrée standard. Motif : §5.1 a (0 octet, même avec un JSON sur l'entrée de git) et §5.1 g. Aucun contrôle perdu : les l.16-51 du blob ne peuvent pas s'exécuter sous git. Test : cas H-16 à H-18, commits réels.
- **CH-3 — L'étape R-13 est l'image locale exacte du job g5, lue dans l'index.**
  - Commande : `git grep --cached -nE "$M"`, avec les trois exclusions de g5 (`':!biblio/' ':!.claude/' ':!.github/workflows/gates.yml'`). `M` est le motif élargi d'`adb2213` l.39, **octet pour octet égal** à celui du job g5 (contrôle H-20, O-7).
  - Codes de `git grep` : 1 (aucune ligne) → étape verte ; 0 → refus `HOOK/g5`, cinq premières lignes affichées ; tout autre code → refus `HOOK/echec` (fail-closed).
  - Portée : l'index entier, et non les seules lignes ajoutées. Le hook refuse donc tant que l'index porte un marqueur, même ancien : g5 serait rouge sur le même contenu. Coût : 56 à 66 ms sur 310 fichiers (§5.3).
  - Changements de comportement voulus (à lire au G2) : S4, S5 et S6 passent de « accepté » à « refusé » (classe et portée de g5) ; S9 passe de « refusé » à « accepté » (`.claude/` est exclu de g5, instructions d'agents, `gates.yml` l.46-47). R-13 vise le code intégré (doc 02 l.98). Q-G0-2.
  - Rejetée : la classe amont sur les seules lignes ajoutées, avec ses exclusions propres (`enforcement/`, `.github/`) : c'est le non-recouvrement mesuré.
- **CH-4 — Texte et contrat du hook.**
  - En-tête : provenance (blob `9c4c846` = VibeGates `52a569d:enforcement/gate-commit.sh` ; l'amont a évolué vers `0b4f3f9`, blob `9dade29`, même corps en mode pre-commit, §5.2) ; écarts CH-1 à CH-3 (et CH-7, CH-8 en D8c-2) ; portée ; rattachements (ADR-0028 D8, lot D8c) ; installation (CH-5).
  - Messages en français ; jetons ASCII sur stderr : `REFUS (HOOK/g5)`, `REFUS (HOOK/lint)`, `REFUS (HOOK/secrets)`, `REFUS (HOOK/echec)`. Succès : une ligne `OK (hook) : …` sur stdout.
  - Sorties : 0 si toutes les étapes sont vertes, 2 sinon ; toute erreur (git, `mktemp`, pièce absente) → 2. Toutes les étapes tournent avant le verdict, pour que l'auteur voie tous les refus d'un coup.
  - Aucune ligne du hook, de l'installeur ni du runner ne répond aux motifs g5 (O-3). Les marqueurs et les valeurs sensibles des cas sont formés à l'exécution (pratique de D8a et de D8b).
  - Le hook ne lance jamais un runner ni un dépôt jetable : dans un arbre lié, `GIT_DIR` est posé (§5.1 d), classe de l'incident du 2026-09-24.
  - Mode du fichier dans l'index : 100644 suffit (`core.filemode=false`, mesuré) ; l'installeur pose le bit d'exécution sur la copie.
  - *Amendement du 2026-09-30 (G1)* : le hook se place d'abord à la racine de l'arbre (`git rev-parse --show-toplevel`, puis `cd`), sinon `HOOK/echec` ; aucun autre `cd` ne précède une commande git (arbre lié : `GIT_DIR` posé par git). Besoin mesuré : sans ce `cd`, un lancement direct depuis un sous-dossier ne balaye que ce sous-dossier (cas H-22). En D8c-2, un dossier `mktemp -d` est créé à l'entrée (échec : `HOOK/echec`) et retiré à la sortie.
- **CH-5 — Installeur `enforcement/hooks/install-pre-commit.sh [--verifier]`.**
  - Refus préalables, sortie 2 : hors d'un dépôt ; `GIT_DIR`, `GIT_WORK_TREE` ou `GIT_INDEX_FILE` posées ; lancé depuis un arbre lié (`--git-dir` différent de `--git-common-dir`, chemins résolus) ; `core.hooksPath` posé. L'installation depuis un worktree écrirait dans le dossier partagé (§5.1 e) : ce refus est la garde système contre FM-1.1.
  - Source : **le blob committé**, `git show HEAD:enforcement/hooks/pre-commit`, jamais le fichier de l'arbre de travail (motif : §5.1 h, un fichier réécrit hors attributs du dépôt peut porter du CRLF ; seul le committé a été revu). Son sha256 doit égaler la constante `ATTENDU` de l'installeur, sinon refus. L'installeur contrôle aussi que son propre fichier égale son blob committé, sinon refus (installeur modifié hors commit).
  - Destination : `$(git rev-parse --git-path hooks)/pre-commit`. Cas :
    - absente : copie ;
    - sha256 égal à `ATTENDU` : « déjà conforme », sortie 0, rien d'écrit ;
    - sha256 dans la liste `CONNUS` (aujourd'hui le hook local `1da91c72…` seul) : sauvegarde en `pre-commit.<12 premiers caractères du sha>`, puis copie ;
    - tout autre sha256 : refus, sortie 2, rien d'écrit (hook inconnu, examen manuel).
  - Copie : fichier temporaire dans le dossier des hooks, `chmod 755`, `mv -f`, puis contrôle du sha256 installé contre `ATTENDU` ; écart → sortie 2. Sortie 0 : une ligne qui porte le sha256 avant et après, pour le JOURNAL.
  - `--verifier` : lecture seule ; sortie 0 si le hook installé égale `ATTENDU`, 2 s'il est absent ou différent (sha256 affiché). C'est la forme que prend l'installation dans le G3 opérant (Q-G0-7).
  - Les constantes vivent dans le script, comme la liste blanche du lint (CH-2 du G0 de D8a) ; tout changement du hook change `ATTENDU` dans le même commit (contrôle I-10).
  - Tests : cas I-01 à I-13 (§7.2), dans des dépôts jetables seulement.
  - *Amendement du 2026-09-30 (G1)* : deux refus ajoutés, fail-closed : sauvegarde `pre-commit.<sha court>` déjà présente et différente → 2, rien écrit (même sha : rien n'est réécrit) ; `core.hooksPath` illisible (code de `git config` autre que 1) → 2. Les refus préalables, le contrôle de soi et le contrôle du blob committé valent aussi en `--verifier`. Jeton unique `REFUS (HOOK/installation)`, messages distincts contrôlés par le runner (fragments). Chemins résolus par `git rev-parse --path-format=absolute`.
- **CH-6 — L'installation sur `F:/Shogen` est un acte de l'orchestrateur**, après le G7 du dernier sous-lot de D8c, jamais un acte du G1 ni du G2 (lecture de la mission : « jamais exécuté par le lot » ; Q-G0-3). Séquence proposée :
  1. `install-pre-commit.sh --verifier` : 2 attendu (hook local `1da91c72…`) ;
  2. `bash enforcement/hooks/install-pre-commit.sh` : sauvegarde et copie ;
  3. `--verifier` : 0 ;
  4. exécution directe du hook installé, index sans changement, sous `GIT_OPTIONAL_LOCKS=0` : sortie 0 (lecture seule : `grep --cached`, extraction vers `F:\tmp`, gate en mode indexé sur 0 fichier) ;
  5. ligne de JOURNAL : sha256 avant et après, nom de la sauvegarde.
  - Retour arrière : remettre la sauvegarde en place par `mv`, consigné.
- **CH-7 — Étape lint (D8c-2) : extraction de l'index, lint pris dans l'index.**
  - Le lint est lu par `git show :enforcement/lint-model-pinning.sh` et lancé sur `$T/a`, extraction par `git ls-files -z` des chemins `':(glob)**/.claude/**'`, `':(glob)**/*.js'`, `':(glob)**/*.mjs'`, `':(glob)**/*.cjs'`, passés à `git checkout-index -z --stdin --prefix="$T/a/"`, **sans `-u`** (l'index n'est pas réécrit).
  - Motifs : le scénario C (§5.3) montre qu'un lint de l'arbre de travail laisse committer un index fautif ; le job g1 juge le commit avec le lint du commit, et l'étape en est l'image locale ; 422 à 514 ms mesurés.
  - Conséquence écrite noir sur blanc : **le hook ne lit pas `.claude/settings.local.json`**, ignoré et donc absent de l'index. La prémisse de SHOGEN-LINT-JSON-ECHAPPEMENT-1 et de SHOGEN-LINT-ENV-MODEL-1 (« le hook lira le réglage local à chaque commit ») ne tient plus ; ces items sont tranchés au §11.1 sur leur autre motif (le G3 opérant lit ce réglage sur l'arbre principal).
  - Pièce absente de l'index (base antérieure à D8a) → `REFUS (HOOK/echec)`, avec le remède : avancer la base (`git merge --ff-only` vers `main`) avant tout commit local.
- **CH-8 — Étape secrets (D8c-2) : gate prise dans l'index, mode indexé.**
  - `git show :enforcement/gate-secrets.sh`, lancée sans argument depuis la racine. Elle lit `git diff --cached` et `git show ":$f"` (l.113, l.122 et l.125 de l'état corrigé), donc l'index du commit en préparation (§5.1 c), et elle s'est comportée correctement sous `GIT_DIR` posé (scénario F).
  - Coût mesuré : 0,38 à 2,2 s de 1 à 11 fichiers (§5.3), soit environ 0,18 s par fichier après 0,25 s de base. Aucun réglage de coût n'est nécessaire au 90ᵉ centile (≈ 1,7 s).
  - Limites héritées de la gate, non levées par D8c (lot proposé D8d, §11.1) : noms de chemin non balayés, messages de commit non balayés, statut de `grep` confondu, chemin d'étage sous Linux.
- **CH-9 — Job g5 : motif élargi et runner du hook.**
  - Motif : celui d'`adb2213` l.39, substitué à celui de la l.49 ; exclusions inchangées. Aucune occurrence sur l'arbre (§5.3) : le job reste vert. Sa note l.45 est redatée (0 marqueur mesuré à `293b7a7`, lot D8c).
  - Étape 1 neuve : `bash enforcement/tests/run-fixtures-hooks.sh`, `shell: bash`. Le hook est la jumelle locale de g5 ; l'amont faisait déjà de g5 le filet du hook (en-tête du blob, l.10-12). Étape 2 : le `git grep` du job, inchangé hors motif.
  - `id` (`g5-dette`) et `name` (`g5-no-naked-todo`) inchangés : aucun contrôle requis n'existe (GC-09) ; aligner l'identifiant sur le nom relève de RUNNERS-1 ou d'une décision de forge.
  - En-tête l.3-8 et l.19-20 : le job g5 porte aussi le runner du hook ; item de forge SHOGEN-G5-FORGE-1 (§11.2).
- **CH-10 — Job g5 : image `ubuntu-24.04`, checkout v7.0.1 épinglé par SHA, `timeout-minutes: 10`.** C'est la part de g5 dans SHOGEN-CI-RUNNERS-1 (annexe B l.80), tirée en avance.
  - Motifs : même règle que g1 et g3 à leur création (CH-15 du G0 de D8a ; D8b) ; le lot réécrit déjà ce bloc ; le job porte désormais des tests (runner), qu'une bascule d'image changerait sans revue (Ubuntu 26 à partir du 2026-10-19, `gates.yml` l.92-96).
  - Conséquence : RUNNERS-1 passe de 12 à 11 définitions de job (acte de l'orchestrateur à l'annexe B). Rejetée : attendre RUNNERS-1, qui laisserait un job de tests neuf sur une image flottante. Q-G0-5.
- **CH-11 — Runner du hook `enforcement/tests/run-fixtures-hooks.sh [hook] [installeur]`.**
  - Garde : sortie 3 si `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE`, `GIT_COMMON_DIR` ou `GIT_OBJECT_DIRECTORY` est posée (classe de l'incident du 2026-09-24 ; garde de D8b).
  - Chaque cas : dépôt jetable sous `mktemp -d`, `git init -b main`, configuration locale (identité factice, `commit.gpgsign=false`, `core.autocrlf=false`), commit de base **avant** l'installation du hook (aucun contournement nécessaire), installation par l'installeur réel, puis `git commit` réel : sortie et jeton vérifiés.
  - Les dépôts jetables portent dès D8c-1 deux agents valides (copies des fixtures de D8a) et, dès D8c-2, le lint et la gate : les cas propres de D8c-1 restent propres quand les étapes lint et secrets s'ajoutent. Jamais sous un `.claude/agents/` du dépôt Shōgen (CA-D8a-3).
  - Marqueurs et formes d'identifiant formés à l'exécution par concaténation, formes d'identifiant à partir des fragments tronqués de D8b (`enforcement/tests/fixtures/secrets/sondes.tsv`).
  - Le cas du hook connu (I-03) utilise une copie de l'installeur dont la liste `CONNUS` est remplacée à l'exécution par le sha256 d'un double de test : le runner ne porte jamais les octets du hook local, dont deux lignes répondent à g5 (§5.2). Un cas distinct (I-10) lit les constantes du vrai installeur.
  - Résumé unique : `hooks : <n> ok, <m> échec` ; sortie 0 si tout passe, 1 si un cas échoue, 3 en erreur fatale.
  - *Amendement du 2026-09-30 (G1)* : dépôt modèle construit une fois, copié par cas (`cp -r`), hook installé une fois par l'installeur réel dans le modèle (cas I-01) ; à partir de D8c-2, modèle à deux commits (agents seuls, puis `enforcement/`), pour C-12. Défaut du runner trouvé par la campagne de mutants (MH-9 survivant) : dans H-20 et I-10, l'affectation du message placée entre le test et le décompte remettait le code à 0 ; corrigé avant la campagne v2 (journal G1, E-3).
- **CH-12 — SHOGEN-LINT-IMBRIQUE-1, tranché : construit en D8c-3 pour ce qui se lit ligne à ligne ; le reste passe à LECTEUR-CC-1.**
  - (a) Ligne canonique élargie aux entrées de séquence : une ligne `model` compte, et sa valeur est jugée, si elle a la forme `^[[:space:]]*(-[[:space:]]+)*model[[:space:]]*:` ; la valeur est prise après le même préfixe. Le compte de premier niveau des agents est inchangé.
  - (b) Sentinelle fail-closed : toute ligne du frontmatter où `model` fait office de clé hors de la forme canonique est refusée en `R-1/cle-model`, soit une clé placée après une accolade ou une virgule (flux), ou une clé entre guillemets à toute profondeur. Forme proposée : `(^[[:space:]]*(-[[:space:]]+)*|[{,][[:space:]]*)["']?model["']?[[:space:]]*:`, appliquée seulement quand la forme canonique ne s'applique pas. Une prose de description où `model` suit un mot (« le model: x ») n'est pas prise (T-84).
  - (c) Suite d'une valeur, à toute profondeur : après une ligne `model` dont la clé est en colonne i, la première ligne suivante qui n'est ni vide ni un commentaire, et dont l'indentation dépasse i, est refusée en `R-1/hors-liste`. Les lignes de commentaire sont sautées, ce qui ferme la suite après commentaire. Cela généralise la règle de premier niveau des l.90-91.
  - Motifs : B.11 fixe le prix de la forme séquence (environ 1 ligne et 1 cas) ; les six formes du §5.4 passent aujourd'hui ; PyYAML lit un modèle hors liste dans cinq d'entre elles ; le sens du refus ne dépend pas du lecteur de Claude Code. Les frontmatters réels n'ont aucune ligne concernée (§5.4) : 0 faux refus mesuré sur l'entrée réelle.
  - Reste à LECTEUR-CC-1 : échappements dans une clé imbriquée, ancres, étiquettes et alias imbriqués, clés dupliquées imbriquées, et toute relaxation d'un refus de (b).
  - *Amendement du 2026-09-30 (G1, mesure `F:/tmp/shogen-lots/D8c/oracles/sonde-residu-imbrique.out`)* : cinq formes imbriquées, lues `model=opus` par PyYAML 6.0.3, passent le lint du lot : clé complexe (`? model` puis `: opus`, forme absente de la liste ci-dessus), ancre, étiquette, alias et échappement. Elles restent à LECTEUR-CC-1, dont la demande reçoit la clé complexe imbriquée.
  - Tests : T-77 à T-84 et T-92 (§7.4).
- **CH-13 — SHOGEN-LINT-JSON-ECHAPPEMENT-1, tranché : lecture à jetons avec garde de résidu, construite en D8c-3.**
  - La passe JSON (l.111-126) lit le fichier aplati comme une suite de chaînes JSON entières sous `LC_ALL=C` : une chaîne est un guillemet, puis des caractères qui ne sont ni guillemet ni barre oblique inverse, ou une barre suivie d'un caractère quelconque, puis un guillemet. Forme exacte des octets : `g0-mesures/sonde-json-d8c.sh` l.11 (variable `RX`), écrite par `tr` depuis un gabarit (§5.1 h).
  - Une clé est un jeton suivi de deux-points. Refus en `R-1/hors-liste` : (i) une clé qui porte une barre oblique inverse (J2 ; T-60 inchangé) ; (ii) un **résidu non vide** : après retrait des chaînes, de `true`, `false`, `null`, des chiffres et de la ponctuation JSON, il reste un caractère, ce qui signale un JSON non strict (commentaire, clé sans guillemets : J4, J5, J7, J9) ; (iii) une clé `model` ou `advisorModel` dont le jeton suivant n'est pas une chaîne (T-45 inchangé).
  - Les valeurs de `model` et `advisorModel` sont prises aux jetons qui suivent ces clés et passent au verdict de la liste blanche (inchangé).
  - Motifs : le motif C-4 donne un faux refus sur un réglage légitime (J1), que Claude Code peut écrire lui-même dans le réglage local quand une règle de permission porte des guillemets [inféré : mécanisme non lu, voir LECTEUR-CC-1] ; il laisse passer une clé sans guillemets (J9) ; la lecture à jetons seule se désaligne sur un commentaire (J5). La garde de résidu ferme J5 et J9 ; J1 et J8 passent. Réglage local réel : strict, résidu vide, 0 faux refus (§5.4).
  - Prix de fail-closed : si Claude Code admet des commentaires dans ses réglages (non établi), un réglage commenté est refusé. C'est le seul point que LECTEUR-CC-1 doit trancher avant toute relaxation. La virgule finale (J6) passe, sans effet sur les clés lues ; déclaré.
  - Tests : T-85 à T-91 (§7.4), plus T-38 à T-45, T-60 et T-61 inchangés (P2P).
- **CH-14 — Note « collision ADR-0020 » : une note datée sous le titre de l'ADR-0020 de `main`, rien dans l'index.**
  - Placement : entre le titre (l.3054) et la ligne de statut (l.3056) de `docs/DECISIONS.md` à `293b7a7`. C'est la forme de l'erratum en tête d'ADR du §8 pt 1 d'ADR-0028 ; aucune convention d'erratum n'existe dans `DECISIONS.md` (mesuré : une seule mention de `error_origin`, l.3179). L'ADR-0020 de `main` n'est pas renumérotée (avis Q8 pt 3).
  - Index : non touché. Il s'arrête à ADR-0023 (l.27) ; son extension est l'acte 4 du §8 d'ADR-0028 (REG-02). Signalé.
  - Texte proposé, transcrit tel quel par le G1 (documentation, hors compte R-25) ; il ne porte ni guillemets anglais, ni marqueur de dette, ni locution du registre 09 :

> **Note datée du 2026-09-30 — collision de numéro (ADR-0028 D8, lot D8c ; `error_origin` : orchestrateur).** Le numéro ADR-0020 a été attribué deux fois le 2026-08-20. Seule l'ADR-0020 ci-dessous (paramètres ex ante de la campagne S2, commit `2d02276`, 16:54:27+01:00) appartient à ce registre ; elle n'est pas renumérotée. L'homonyme vit sur la branche `roster-ban-alignment-2026-08-20`, jamais fusionnée (commit `adb2213`, 06:20:27+01:00, `docs/DECISIONS.md` l.3051 de ce commit) : il consignait l'application d'AgileGates, le roster aligné du 2026-08-14 et le câblage des gates VibeGates g1, g3 et g5 élargi. Cause mesurée : deux sessions concurrentes sur le même arbre de travail. Le journal de refs montre la branche créée et `adb2213` à 06:20:27, un commit d'une autre session (`60fd8e1`, harnais S2) posé sur cette branche à 08:20:27, puis à 12:44:22 le retour à `main` et le report de ce commit par cherry-pick (`f11bdca`), et à 12:44:40 la branche ramenée à `adb2213`. Devenir du contenu : le roster qu'il consignait est supplanté (`36593b6`, puis les décisions de roster du 2026-09-22 au 2026-09-28) ; ses gates et la copie versionnée du hook pre-commit sont portées sous ADR-0028 D8, lots D8a, D8b et D8c (commits au JOURNAL). La décision de l'investisseur du 2026-08-20 a été prise et exécutée sur la branche ; elle a commencé d'entrer sur `main` avec le lot D8a (2026-09-30, job g1), et ses gates et le hook y sont tous au commit de D8c. Ce portage est couvert par la délégation du 2026-09-30 (lecture (b), consignée au JOURNAL le 2026-09-30) : veto §4.10 a non exercé, révocable jusqu'à l'exécution unique. Sa confirmation explicite (ADR-0028 §4.10 a), le tag `archive/roster-ban-2026-08-20` puis la suppression de la branche restent des actes de l'investisseur (SHOGEN-D8-PC-1).

  - Le G1 relit les hash et les heures par `git log -1` et `git reflog show`, en lecture seule, avant la transcription (O-11).
  - *Amendement daté du 2026-10-01 (correction de la revue G2, C-G2-1)* : le texte transcrit est amendé, PC-1 ayant été exécuté pendant le G1 (§2) ; il n'est plus mot pour mot celui ci-dessus. Texte de `F:/tmp/shogen-lots/D8c/g2/o/note_c1.py`, 21 lignes repliées à 94 colonnes : homonyme au commit `adb2213`, que conserve le tag annoté ; journal de refs de la branche cité tel que relevé au §5.5, avant sa suppression ; confirmation, tag et suppression consignés.
- **CH-15 — Ce que D8c ne revendique pas.**
  - Le hook n'est pas une garde de commit : il juge le contenu de l'index quand `git commit` le lance. Il ne voit ni `cherry-pick`, ni `rebase` (§5.1 f), ni un commit fait avec l'option de contournement, qu'interdit R-22 et que refuse le garde du harnais (§5.1 g, mesuré). Ses verts ne sont pas une preuve de CI : la forge est arrêtée (GC-01).
  - Il ne remplace ni le G3 opérant, ni la revue G2 : une modification d'un contrôleur passe avec le contrôleur qu'elle modifie (CH-7 lit le lint dans l'index), comme au job g1.
  - L'installeur contrôle des empreintes, pas l'intégrité de l'hôte (T-11) : un hôte compromis réécrit hook et installeur.
  - *Amendement daté du 2026-10-01 (correction de la revue G2, C-G2-9)* : le hook ne voit pas non plus une fusion sans conflit (`git merge --no-ff` lance `pre-merge-commit`, mesuré par la revue G2) ; l'en-tête du hook le dit.

## 7. Table des cas (contrat des runners ; sortie attendue et jeton)

Notation : « refus » = `git commit` en échec et jeton attendu sur stderr ; « 0 » = commit fait et ligne `OK (hook)`. Marqueurs formés à l'exécution ; « délimité » = introduit par un délimiteur de commentaire de la classe g5.

### 7.1 Étape R-13 (D8c-1), runner du hook

| id | index du commit | attendu | lien |
|---|---|---|---|
| H-01 | `docs/x.md`, marqueur délimité par un dièse | refus `HOOK/g5` | S1 |
| H-02 | `docs/x.md`, propre | 0 | S2 |
| H-03 | `src/a.rs`, marqueur délimité par une double barre, deux-points | refus | S3 |
| H-04 | marqueur suivi de deux-points, sans délimiteur | refus (était accepté) | S4, CH-3 |
| H-05 | `enforcement/x.sh`, marqueur délimité | refus (était accepté) | S5 |
| H-06 | `.github/workflows/x.yml`, marqueur délimité | refus (était accepté) | S6 |
| H-07 | commentaire HTML portant un marqueur | refus | S7 |
| H-08 | le mot dans de la prose | 0 | S8 |
| H-09 | `.claude/agents/b.md` (agent valide), marqueur délimité dans le corps | 0 (était refusé) | S9, CH-3 |
| H-10 | `.github/workflows/gates.yml`, marqueur délimité | 0 (exclu, comme g5) | CH-3 |
| H-11 | `biblio/x.md`, marqueur délimité | 0 (exclu) | CH-3 |
| H-12 | marqueur déjà présent dans l'index, commit d'un autre fichier propre | refus | index entier |
| H-13 | marqueur indexé, arbre de travail remis propre | refus | `--cached` |
| H-14 | marqueur dans l'arbre de travail seul, non indexé | 0 | `--cached` |
| H-15 | fichier binaire (octets NUL) qui porte un marqueur délimité | refus (comme g5 ; mesure au G1) | CH-3 |
| H-16 | `commit -a` d'un fichier suivi marqué | refus | §5.1 c |
| H-17 | commit avec chemin, fichier marqué | refus | §5.1 c |
| H-18 | arbre lié : fichier marqué, puis fichier propre | refus, puis 0 | §5.1 d-e |
| H-19 | hook lancé hors d'un dépôt | 2 `HOOK/echec` | CH-3 |
| H-20 | motif et exclusions du hook = ceux du job g5 de `gates.yml`, octet pour octet | égalité | CH-3, O-7 |

- *Amendement du 2026-09-30 (G1)* : cas ajoutés, mesurés avant d'être écrits (`F:/tmp/shogen-lots/D8c/oracles/sonde-h21-h22.out`) : **H-21**, index illisible (fichier d'index tronqué), hook lancé directement → 2 `HOOK/echec` (`git grep` sort en 128 ; tue MH-8, que H-19 ne tue pas : dans le hook livré, le refus hors d'un dépôt précède `git grep`) ; **H-22**, hook lancé directement depuis un sous-dossier, marqueur indexé ailleurs → 2 `HOOK/g5` (sans le `cd` vers la racine : sortie 0, mesurée).
- *Amendement daté du 2026-10-01 (correction de la revue G2, C-G2-4 et C-G2-7)* : **H-23** ajouté : fichier propre committé, marqueur ajouté puis indexé, `git commit --amend` → refus `HOOK/g5` (consommateur 1 du §10, sans cas jusque-là ; rouge sous le mutant de verdict GH-1). Le runner ramène ses deux arguments à des chemins absolus avant tout `cd` : lancé depuis la racine avec des chemins relatifs, il sortait H-19 et H-22 en échec à tort (48 ok, 2 échecs, mesure de la revue G2). Normalisation par `dirname` et `basename`, paire cohérente sous Git Bash comme sous Linux : écart mesuré au texte de la revue G2, qui donnait le nom par `${HOOK##*/}` (sortie 3 sur un argument à barre oblique inverse sous Git Bash ; journal §15).

### 7.2 Installeur (D8c-1), runner du hook

| id | situation | attendu |
|---|---|---|
| I-01 | dépôt neuf, aucun hook | 0 ; hook installé, sha256 = `ATTENDU`, exécutable |
| I-02 | relance | 0, « déjà conforme » ; fichier inchangé |
| I-03 | hook existant d'empreinte connue (double de test, CH-11) | 0 ; sauvegarde `pre-commit.<sha court>` égale à l'ancien ; hook installé |
| I-04 | hook existant d'empreinte inconnue | 2 ; hook inchangé |
| I-05 | `core.hooksPath` posé | 2 ; rien d'écrit |
| I-06 | lancé depuis un arbre lié | 2 ; rien d'écrit dans le dossier partagé |
| I-07 | blob committé du hook différent de `ATTENDU` | 2 |
| I-08 | hook modifié dans l'arbre de travail, non committé | 0 ; c'est le blob committé qui est installé |
| I-09 | `--verifier` : conforme, différent, absent | 0, 2, 2 ; aucune écriture (empreintes et dates du dossier des hooks inchangées) |
| I-10 | constantes du vrai installeur | `CONNUS` contient `1da91c72…1277d` ; `ATTENDU` = sha256 de `enforcement/hooks/pre-commit` de l'arbre |
| I-11 | `GIT_DIR` posée pour le seul appel | 2 |
| I-12 | hors d'un dépôt | 2 |
| I-13 | installeur modifié hors commit | 2 |

- *Amendement du 2026-09-30 (G1)* : **I-14** ajouté, argument inconnu (`--verify`) → 2, rien écrit (sans ce refus, une faute de frappe installerait au lieu de vérifier ; tue MI-11). **I-11** pose `GIT_INDEX_FILE` vers un chemin inexistant, pour le seul appel de l'installeur, et non `GIT_DIR` : règle d'isolation du 2026-09-25 et CA-D8c-14 ; la présence de `GIT_DIR` et de `GIT_WORK_TREE` dans la liste de refus se contrôle par lecture (précédent : O-11 de D8b).

### 7.3 Branchement (D8c-2), runner du hook

| id | situation | attendu |
|---|---|---|
| C-01 | agent indexé à `model: opus`, arbre de travail remis bon | refus `HOOK/lint` (`R-1/tier-nu`) |
| C-02 | agent indexé bon, arbre de travail à `model: opus`, non indexé | 0 |
| C-03 | lint de l'arbre de travail remplacé par un `exit 0` non indexé ; agent indexé fautif | refus (le lint vient de l'index) |
| C-04 | `.claude/settings.local.json` non suivi, clé `model` bannie | 0 ; déclaré (CH-7) |
| C-05 | forme d'identifiant indexée, formée depuis les fragments de D8b | refus `HOOK/secrets` (`SECRETS/forme`) |
| C-06 | gate de l'arbre de travail remplacée par un `exit 0` ; forme indexée | refus (la gate vient de l'index) |
| C-07 | lint absent de l'index | refus `HOOK/echec`, remède « avancer la base » |
| C-08 | gate absente de l'index | refus `HOOK/echec` |
| C-09 | marqueur, modèle et forme à la fois | trois jetons, sortie 2 |
| C-10 | arbre lié, propre | 0 (`GIT_DIR` posé par git) |
| C-11 | `commit -a` d'un agent modifié en fautif | refus |
| C-12 | base sans `enforcement/` | refus `HOOK/echec` |

- *Amendement du 2026-09-30 (G1)* : **C-13** ajouté, objet d'un agent indexé retiré du dépôt jetable, hook lancé directement → 2 `HOOK/echec` (extraction de l'index impossible ; tue MC-8). C-12 est construit sur un arbre lié créé sur le commit parent du modèle, sans `enforcement/` : forme mesurée du risque SHOGEN-WORKTREE-BASE-HOOK-1. **C-14** ajouté : hook installé lancé directement, forme d'O-13 (`GIT_OPTIONAL_LOCKS=0`) → 0 et `.git/index` inchangé (sha256 avant et après ; sonde `oracles/sonde-index.out`).

### 7.4 Lint (D8c-3), runner du lint : cas neufs, forme des T-01 à T-76

| id | arbre (copie D de la fixture devops, lignes ajoutées au frontmatter) | attendu |
|---|---|---|
| T-77 | `hooks:`, `  Stop:`, `    - model: opus` | 2 `R-1/tier-nu` (entrée de séquence lue) |
| T-78 | idem, `    - model: claude-opus-5-5` | 0 |
| T-79 | `hooks: {Stop: [{type: prompt, model: opus}]}` | 2 `R-1/cle-model` (flux) |
| T-80 | `hooks:`, `  s:`, clé imbriquée entre guillemets à `opus` | 2 `R-1/cle-model` |
| T-81 | `hooks:`, `  - {model: opus}` | 2 `R-1/cle-model` |
| T-82 | `hooks:`, `  s:`, `    model: claude-opus-5-5`, `      x` | 2 `R-1/hors-liste` (suite imbriquée) |
| T-83 | idem avec une ligne de commentaire avant la suite | 2 `R-1/hors-liste` |
| T-84 | `description:` en prose où `model` suit un mot, puis deux-points | 0 (garde contre le faux refus) |
| T-85 | J1 : réglage légitime, guillemet échappé suivi de deux-points dans une valeur | 0 (faux refus levé) |
| T-86 | J2 : clé échappée qui forme `model` | 2 `R-1/hors-liste` |
| T-87 | J4 : commentaire, puis clé `model` | 2 `R-1/hors-liste` (JSON non strict) |
| T-88 | J5 : commentaire qui porte un guillemet isolé, puis clé `model` | 2 `R-1/hors-liste` |
| T-89 | J9 : clé `model` sans guillemets | 2 `R-1/hors-liste` |
| T-90 | J8 : guillemet échappé sans deux-points | 0 |
| T-91 | J6 : virgule finale | 0 (déclaré) |
| T-92 | premier niveau : `model: claude-opus-5-5`, commentaire en colonne 0, puis ligne indentée | 2 `R-1/hors-liste` |

Chaque cas vérifie la sortie ET le jeton, comme les T-01 à T-76 ; les 76 cas existants restent verts (P2P). Les formes de T-77 à T-83 et de T-85 à T-89 ont été mesurées au G0 sur le lint committé (§5.4) : ce sont des F2P établis avant code.
- *Amendement du 2026-09-30 (cp-1 C-5 ; mesure du G1 avant code, `F:/tmp/shogen-lots/D8c/oracles/c5-mesure-lint-committe.out`, lint committé `1c57e8c4`)* : **11 F2P** (T-77, T-79 à T-83, T-85, T-87 à T-89, T-92) et **5 épingles** (T-78, T-84, T-86, T-90, T-91). T-86 est une épingle, contrairement à la phrase ci-dessus : le lint committé refuse déjà J2 en `R-1/hors-liste` (comme T-60). T-92 est un F2P. Tueurs nommés des épingles : T-78 → ML-9 (préfixe de séquence non retiré de la valeur) ; T-84 → ML-8 ; T-86 → ML-6 ; T-90 → ML-10 (jeton de chaîne sans échappement) ; T-91 → ML-11 (virgule finale refusée).
- *Amendement daté du 2026-10-01 (correction de la revue G2, C-G2-2 et C-G2-3)* : sentinelle étendue au crochet ouvrant (classe `[[{,]`) : une clé `model` en flux de séquence, que PyYAML 6.0.3 lit (mesure de la revue G2, six formes), sortait en 0. Cas ajoutés : **T-93** `hooks: [model: opus]` → 2 `R-1/cle-model` ; **T-94** `hooks: {Stop: [model: opus]}` → 2 `R-1/cle-model` ; **T-95** `hooks:`, `  Stop:`, `    - model: claude-opus-5-5`, `      type: prompt` → 0, 1 fichier (colonne de clé d'une entrée de séquence, ligne sœur lue). Prix : une forme de flux est refusée quelle que soit sa valeur, comme T-79. Catégories mesurées par le runner corrigé (`F:/tmp/shogen-lots/D8c/corr/o/lot-lint.out`) : T-93 et T-94 F2P (rouges sur le lint du lot et sur le lint committé `1c57e8c4`) ; T-95 épingle (verte sur les deux, tueur GL-5b). Comptes : 13 F2P, 6 épingles.

## 8. Oracles non-LLM nommés

- **O-1 — Runners.** `TMPDIR=<TMP neuf> bash enforcement/tests/run-fixtures-hooks.sh` → sortie 0, `hooks : <n> ok, 0 échec`, n = cas du §7.1 à §7.3 retenus dans le sous-lot ; `bash enforcement/tests/run-fixtures-model-pinning.sh` → sortie 0, `model-pinning : 92 ok, 0 échec` après D8c-3 (76 avant).
- **O-2 — Sonde git-ci §2.e rejouée sur le hook versionné** : `g0-mesures/sonde-hook-local.sh <hook>` : la table S1-S9 du §5.2 est reproduite, avec les seuls changements voulus du CH-3 (S4, S5, S6 refusés ; S9 accepté). Toute autre différence est un défaut.
- **O-3 — Compatibilité g5 et texte.** Motif courant et motif élargi : 0 ligne sur chaque fichier ajouté ou modifié par le lot, documents compris (copie de ce G0, journal, note de DECISIONS) ; commande du job g5 élargi rejouée sur le worktree : sortie 0.
- **O-4 — Rouge semé sur l'entrée committée.** `git archive <gel> ':!biblio'` extrait dans un dépôt jetable, committé, hook installé par l'installeur ; puis (k=0) un changement propre → 0 ; (k=1) marqueur délimité indexé → refus `HOOK/g5` ; en D8c-2 : (k=2) agent de l'arbre committé passé à `opus` dans l'index → refus `HOOK/lint` ; (k=3) forme d'identifiant indexée → refus `HOOK/secrets`. La composition part de l'artefact committé, jamais d'une forme reconstruite à la main.
- **O-5 — Mutants de gate** (copies hors dépôt ; runner lancé avec le chemin du mutant en argument ; chaque mutant rougit le runner, cas tueur nommé) :
  - hook, D8c-1 : MH-1 verdict inversé (H-01) ; MH-2 motif ramené au motif courant (H-01) ; MH-3 motif ramené à la classe amont (H-04) ; MH-4 `--cached` retiré (H-13) ; MH-5 exclusion `.claude/` retirée (H-09) ; MH-6 exclusion de `gates.yml` retirée (H-10) ; MH-7 exclusion `enforcement/` ajoutée (H-05) ; MH-8 erreur de `git grep` rendue verte (H-19) ; MH-9 motif différent de celui du job (H-20) ;
  - installeur, D8c-1 : MI-1 empreinte de la source non contrôlée (I-07) ; MI-2 empreinte inconnue écrasée (I-04) ; MI-3 `core.hooksPath` ignoré (I-05) ; MI-4 arbre lié admis (I-06) ; MI-5 pas de sauvegarde (I-03) ; MI-6 source prise dans l'arbre de travail (I-08) ; MI-7 `--verifier` vert sur un hook différent (I-09) ; MI-8 contrôle de soi retiré (I-13) ; le contrôle après copie est un mutant probablement équivalent, à mesurer et déclarer ;
  - branchement, D8c-2 : MC-1 étape lint retirée (C-01) ; MC-2 lint lancé sur l'arbre de travail (C-01, C-02) ; MC-3 lint pris dans l'arbre de travail (C-03) ; MC-4 étape secrets retirée (C-05) ; MC-5 gate prise dans l'arbre de travail (C-06) ; MC-6 pièce absente tenue pour verte (C-07, C-08) ; MC-7 verdict réduit à la dernière étape (C-09) ;
  - lint, D8c-3 : ML-1 préfixe de séquence retiré (T-77) ; ML-2 sentinelle retirée (T-79, T-80, T-81) ; ML-3 suite imbriquée retirée (T-82) ; ML-4 commentaires non sautés (T-83, T-92) ; ML-5 garde de résidu retirée (T-88, T-89) ; ML-6 refus des clés à barre retiré (T-86) ; ML-7 retour au motif C-4 (T-85) ; ML-8 sentinelle étendue à toute occurrence de `model` suivie de deux-points (T-84).
  - F2P : hook, installeur et runner du hook sont neufs (catégorie « nouveau module ») ; D8c-3 modifie une pièce existante, et ses F2P sont mesurés au G0 (§5.4).
  - *Amendement du 2026-09-30 (G1)* : mutants ajoutés : MH-10 (`cd` vers la racine retiré, H-22), MH-11 (exclusion `biblio/` retirée, H-11), MH-13 (refus hors d'un dépôt rendu vert, H-19) ; MI-9 (contrôle après copie) à MI-15 ; MI-16 (hook conforme réécrit, I-02) ; MC-8 (C-13), MC-9 (`-u` ajouté à `checkout-index` : équivalent, mesuré, `-u` sans effet avec `--prefix`), MC-10 (le hook indexe l'arbre de travail, C-02 et C-14) ; ML-9 à ML-13. MH-8 est tué par H-21 et MC-7 par H-01 et C-01. Résultats : journal G1 §5.
- **O-6 — Installeur sur dépôts jetables** : les treize cas I du §7.2, avec les empreintes avant et après publiées au journal G1.
- **O-7 — Égalité des motifs** : la chaîne du motif et les trois exclusions extraites de l'étape g5 de `gates.yml` égalent, octet pour octet, celles du hook (H-20 ; rejeu hors runner au journal G1).
- **O-8 — Non-régression** : `cargo --locked xtask verify` VERT (S-G4, S-G5 et S-G8 lisent la copie de ce G0, le journal et la note de DECISIONS) ; suite `(cd s2-harness && python -B -m unittest discover -s tests -t .)` : compte et sauts identiques à la base (216, 2 sauts à `293b7a7`, à remesurer) ; `run-fixtures-model-pinning.sh` et `lint-model-pinning.sh .` (3 fichiers sur l'arbre principal, 2 sur une copie propre) ; `run-fixtures-secrets.sh` (112 ok à l'état corrigé de D8b), `gate-secrets.sh --tree` et `--history` : sortie 0. Environnement : `CARGO_HOME`, `CARGO_NET_OFFLINE=true`, `TMPDIR`, `TMP` et `TEMP` de la mission.
- **O-9 — TMP** : 0 entrée neuve dans un TMP neuf après chaque runner.
- **O-10 — `gates.yml`** : `yaml.safe_load` (PyYAML 6.0.3, déjà présent, aucune installation) ; structure comparée à la base : jobs g1, g3 et s2 identiques ; bloc g5 conforme aux CH-9 et CH-10 ; aucun job neuf.
- **O-11 — Faits de la note** : `git log -1` sur `2d02276`, `adb2213`, `60fd8e1`, `f11bdca`, `36593b6`, et `git reflog show` de la branche et de `HEAD`, en lecture seule : les hash et heures de la note sont ceux-là.
- **O-12 — Coût par commit** (D8c-2) : le hook composé rejoué sur un dépôt jetable issu du gel, pour 1, 3, 8 et 11 fichiers ; bornes publiées au journal et dans le commentaire du job si elles le fixent.
- **O-13 — Après installation** (acte de l'orchestrateur, CH-6) : `--verifier` sortie 0 ; hook installé lancé directement sur `F:/Shogen`, index sans changement, sous `GIT_OPTIONAL_LOCKS=0` : sortie 0.
- **Enregistrement** : le G1, puis le G2 par ses propres commandes, produisent un enregistrement d'oracle substitut au format de CI-S2 (annexe B l.79), champs de D6 (viii) (ADR-0028 l.201-207), sous `F:/tmp/shogen-lots/D8c/oracles/`.
- **Ce que l'oracle local ne prouve pas** : `git grep -E` et le mot-frontière de l'image Linux, `mktemp`, `sha256sum`, `checkout-index` et les modes de fichier sur Linux ; la lecture du workflow par la forge. Item SHOGEN-G5-FORGE-1 (§11.2), même classe que SHOGEN-G1-FORGE-1 (c) de D8a.

## 9. Estimation R-25 (ascendante, par fichier ; [inféré] sauf mention)

| fichier | D8c-1 | D8c-2 | D8c-3 | base de l'estimation |
|---|---|---|---|---|
| `enforcement/hooks/pre-commit` | ≈ 28 | ≈ +18 | 0 | en-tête ≈ 16 (le lint de D8a en porte 25, la gate de D8b 41) ; étape R-13 ≈ 12 ; étapes lint et secrets ≈ 6 chacune, verdict agrégé ≈ 3, en-tête ≈ 3 (prototype de mesure : 23 lignes pour les trois étapes, en-tête de 5 lignes compris, sans messages ni remèdes) |
| `enforcement/hooks/install-pre-commit.sh` | ≈ 48 | ≈ +1 | 0 | en-tête ≈ 12 ; refus préalables ≈ 6 ; source et contrôle de soi ≈ 6 ; `--verifier` ≈ 5 ; états de la destination ≈ 9 ; copie et contrôle ≈ 6 ; sorties ≈ 4 |
| `enforcement/tests/run-fixtures-hooks.sh` | ≈ 70 | ≈ +18 | 0 | outillage ≈ 32 (garde, `mktemp`, `trap`, constructeur de dépôt, assertion ; le runner de D8a en compte 52 pour le sien) ; une ligne par cas : 20 H, 13 I, 12 C ; commentaires ≈ 5 |
| `.github/workflows/gates.yml` | ≈ 16 | 0 | 0 | motif ≈ 1 ; étape du runner ≈ 3 ; image, checkout et borne ≈ 5 ; commentaires ≈ 4 ; en-tête ≈ 3 (g1 de D8a : +33 −4 pour un job entier) |
| `enforcement/lint-model-pinning.sh` | 0 | 0 | ≈ +15 | ligne canonique ≈ 2 ; sentinelle ≈ 2 ; suite à toute profondeur ≈ 4 ; jetons, résidu, paires ≈ 5 ; en-tête ≈ 2 |
| `enforcement/tests/run-fixtures-model-pinning.sh` | 0 | 0 | ≈ +18 | 16 cas, commentaire ≈ 2 |
| **total** | **≈ 162** | **≈ 37** | **≈ 33** | lot ≈ 232 > 200 : coupe prévue d'avance |

- **Documentation, hors compte** (précédent ratifié : Q-G2-1 de D8a, `JOURNAL.md` l.137) : la note de DECISIONS (≈ 14 lignes), la copie de ce G0 et le journal G1. Le G1 publie les deux comptes.
- **Marge d'erreur** : D8a a mesuré 213 lignes pour ≈ 188 estimées par son G0 au premier sous-lot (+13 %), et 286 pour ≈ 239 sur le lot (+20 %) (`docs/G1-lot-D8a.md` §1) ; B0 : 252 pour 193 (+30 %). D8c-1 à +25 % donnerait ≈ 203 : la règle de coupe ci-dessous le traite d'avance (FM-1.5).
- **Règle de coupe** (mesure : `git diff --numstat` des fichiers suivis, `wc -l` des fichiers neufs ; estimation scellée avant tout code) :
  1. chaque sous-lot ≤ 200 : trois sous-lots, D8c-1, D8c-2, D8c-3 ;
  2. si D8c-1 dépasse 200 : il se coupe en **D8c-1a** (hook, cas H, g5, note de DECISIONS) et **D8c-1b** (installeur, cas I) ; les deux vont au même G2 et au même commit, car le tuyau exige l'installeur ;
  3. si D8c-2 et D8c-3 sont chacun sous 100, le G1 peut les réunir en un sous-lot, avec le motif écrit ;
  4. si un sous-lot dépasse encore 200 : **arrêt et consultation formée** (R-26). On ne comprime jamais un contrôle pour passer le seuil.
- Ordre : D8c-1, puis D8c-2, puis D8c-3, chacun sur le précédent, tous sur D8b empilé. Un seul G2 pour les trois ; l'installation (CH-6) suit le G7 du dernier.
- *Amendement du 2026-09-30 (G1, règle 2 appliquée)* : D8c-1 mesure 223 lignes > 200 (hook 40, installeur 51, runner 103, `gates.yml` +29) : coupe en **D8c-1a** (hook, cas H, g5, note de DECISIONS ; 141) et **D8c-1b** (installeur, cas I ; 99), au même G2 et au même commit. D8c-2 mesure 65 et D8c-3 51 ; lot : 356 lignes ajoutées (G0 : ≈ 232 ; G1 : ≈ 260). Règle 3 non appliquée : D8c-3 reste un sous-diff séparable (C-4). Mesures : journal G1 §1.
- **Lignes datées proposées pour l'annexe A** (acte de l'orchestrateur, ADR-0028 §6 l.307 ; colonnes de l'annexe) :

| lot (date) | objet (décision) | véhicule | oracle non-LLM nommé | taille (R-25) | tuyau (entrée → sortie → consommateur ; test) | cp-1 |
|---|---|---|---|---|---|---|
| **D8c** (2026-09-29 ; amendée le 2026-09-30 par le G0) | D8 : hook versionné, porté de `9c4c846` (étape R-13 = image de g5 sur l'index), installeur vérifié, motif g5 élargi, note « collision ADR-0020 » ; branchement du lint et de la gate secrets ; SHOGEN-LINT-IMBRIQUE-1 et SHOGEN-LINT-JSON-ECHAPPEMENT-1 tranchés | `enforcement/hooks/`, `enforcement/tests/`, `enforcement/lint-model-pinning.sh`, `gates.yml`, `docs/DECISIONS.md` | O-1 à O-13 du G0 ; mutants MH, MI, MC, ML | ≈ 232 [inféré, G0 §9] au lieu de ≈ 120 ; coupé en D8c-1, D8c-2, D8c-3 | index du commit → hook installé → `git commit` accepté ou refusé ; test : runner du hook (installeur réel, commits réels) et O-4 | complet |
| **D8c-1** (2026-09-30 ; coupe R-25 du G0 de D8c) | hook (étape R-13), installeur, runner (cas H et I), job g5 (motif élargi, runner, image, checkout, borne), note de DECISIONS | `enforcement/hooks/pre-commit`, `enforcement/hooks/install-pre-commit.sh`, `enforcement/tests/run-fixtures-hooks.sh`, `gates.yml`, `docs/DECISIONS.md` | O-1 (33 cas), O-2, O-3, O-4 (k = 0, 1), O-5 (MH, MI), O-6 à O-11 | ≈ 162 [inféré] | index → hook → commits ; job g5 et G3 opérant local | complet (sous le cp-1 du lot) |
| **D8c-2** (2026-09-30 ; même coupe) | étapes lint (extraction de l'index) et secrets (mode indexé) du hook ; cas C | le hook, l'installeur (`ATTENDU`), le runner du hook | O-1 (45 cas), O-4 (k = 2, 3), O-5 (MC), O-12 | ≈ 37 [inféré] | lint et gate → hook → commits (consommateurs 2 de D8a et de D8b) | complet (sous le cp-1 du lot) |
| **D8c-3** (2026-09-30 ; même coupe) | lint : formes imbriquées (CH-12), lecture JSON à jetons et garde de résidu (CH-13) ; cas T-77 à T-92 | `enforcement/lint-model-pinning.sh`, son runner | O-1 (92 cas du lint), O-5 (ML), O-8 | ≈ 33 [inféré] | `.claude/` et réglages → lint → job g1, hook et G3 opérant | complet (sous le cp-1 du lot) |

## 10. Tuyaux (CA-11 durci)

| rôle | objet | état |
|---|---|---|
| entrée | index du commit en préparation, produit par `git add` de l'auteur (orchestrateur sur `main` ; workers dans leurs worktrees : hooks partagés, §5.1 e) | présent |
| entrée (D8c-2) | lint et gate secrets, lus dans cet index | présents : D8a commis ; D8b à commettre avant D8c |
| pièce | `enforcement/hooks/pre-commit`, versionnée ; copie installée en `.git/hooks/pre-commit` par l'installeur | à construire ; installation : acte (CH-6) |
| sortie | code 0 ou 2 ; jetons `HOOK/…` sur stderr | à construire |
| consommateur 1 | `git commit` et `git commit --amend` du dépôt principal et de tout arbre lié | **absent jusqu'à l'installation**, puis câblé ; preuve : O-13. Non couverts : `cherry-pick`, `rebase` ; `pre-merge-commit` non installé, et `main` refuse les fusions (git-ci l.179) : item SHOGEN-HOOK-COUVERTURE-1 |
| consommateur 2 | job g5 (étape 1 : runner du hook) | **partiel déclaré**, comme g1 et g3 : forge arrêtée (GC-01), aucun contrôle requis (GC-09) ; G3 opérant = rejeu local ; item SHOGEN-G5-FORGE-1 |
| état | `ATTENDU` et `CONNUS` dans l'installeur ; la copie installée ; sa sauvegarde | — |
| test de composition | runner du hook : dépôts jetables, installeur réel, `git commit` réels (non-LLM) ; O-4 sur l'artefact committé ; O-13 sur le dépôt réel après installation | l'exécution sur la forge relève de SHOGEN-G5-FORGE-1 |

- Les tuyaux que ce lot ferme : consommateur 2 du lint (D8a, item 9) et consommateur 2 du mode indexé de la gate (D8b, item 4), à l'installation.
- Conséquences opérationnelles à déclarer au JOURNAL lors de l'installation : tout commit local d'un worker passe par le hook ; un worktree dont la base précède D8a et D8b voit ses commits refusés en `HOOK/echec` tant que sa base n'est pas avancée (C-07, C-12) ; la consigne « avancer la base avant tout commit local » entre aux commandes de mission.
- G3 opérant (ADR-0028 §4.11, Q-G0-7) : à partir de l'installation, la liste reçoit `bash enforcement/tests/run-fixtures-hooks.sh` (sortie 0) et `bash enforcement/hooks/install-pre-commit.sh --verifier` (sortie 0). Texte proposé au journal G1 ; l'amendement est un acte de l'orchestrateur.
- *Amendement daté du 2026-10-01 (correction de la revue G2, C-G2-9)* : consommateur 1, non couverts : `cherry-pick`, `rebase` et les fusions sans conflit (`git merge --no-ff` lance `pre-merge-commit`), mode d'intégration de `main` depuis la méthode par parties (`docs/adr-0028/PARTIES-S2.md` l.19) ; la prémisse du tableau selon laquelle `main` refuse les fusions est retirée ; item 2 du §11.2 re-formé. `git commit --amend` reçoit son cas (H-23).

## 11. Items (règles Dettes et PAROXYSME)

### 11.1 Items entrants à déclencheur « G0 de D8c » : décision de ce G0

Règle d'admission appliquée : un item entre dans D8c si son absence rend le hook faux ou non branché, ou si la mission le nomme ; sinon il est re-formé, avec son autre déclencheur et un motif écrit. Les items de D8b sont ceux de son journal, non commis : la décision vaut s'ils sont versés tels quels.

| item | source | décision | véhicule ou nouveau déclencheur |
|---|---|---|---|
| SHOGEN-D8-HOOK-LINT-1 | journal D8a l.292 | **construit** (CH-7) | D8c-2 |
| SHOGEN-D8-HOOK-SECRETS-1 | journal D8b l.369 | **construit** (CH-8) ; coût mesuré (§5.3), aucun réglage requis | D8c-2 |
| SHOGEN-LINT-IMBRIQUE-1 | annexe B l.196 | **construit** pour les formes ligne à ligne (CH-12) ; reste nommé à LECTEUR-CC-1 | D8c-3 |
| SHOGEN-LINT-JSON-ECHAPPEMENT-1 | annexe B l.197 | **construit** : jetons et garde de résidu (CH-13) ; la prémisse « le hook lira le réglage local » tombe (CH-7), l'item tient par le G3 opérant sur l'arbre principal | D8c-3 |
| SHOGEN-LINT-LECTEUR-CC-1 | annexe B l.198 | **demande formée** ci-dessous ; non bloquante pour D8c-3, dont les constructions sont des refus fail-closed ; bloquante pour toute relaxation d'un refus de CH-12 ou CH-13 | avant toute relaxation, ou au premier faux refus sur l'arbre principal |
| SHOGEN-LINT-ENV-MODEL-1 | journal D8a l.286 | **re-formé** : le hook ne lit pas les réglages locaux (CH-7) ; aucun `.claude/settings.json` suivi (§5.3) ; les noms `ANTHROPIC_DEFAULT_*_MODEL` ne sont pas dans les FAITS de l'orchestrateur (E-3 de D8a) | premier `.claude/settings.json` suivi, ou FAITS de la page de configuration du modèle, au premier des deux ; la lecture à jetons de CH-13 en fixe le prix (≈ 1 ligne et 2 cas [inféré]) |
| SHOGEN-LINT-HORS-DEPOT-1 | journal D8a l.288 | **re-formé avec sa mesure** : le lint sort en `R-1/vide` sur la disposition du dossier global ; les 9 agents globaux, replacés sous `.claude/agents/`, passent (§5.4). Construction : un mode du lint pour la disposition globale, ou une procédure de copie à la cartographie. Le hook juge des commits, pas la configuration de la machine | prochaine décision de roster, ou cartographie de clôture de phase, au premier des deux |
| SHOGEN-SECRETS-MESSAGES-1 | journal D8b l.373 | **re-formé vers le lot proposé D8d** : pièce de la gate (flux `--history`) ; côté hook, un `commit-msg` étendrait l'installeur de D8c | G0 de D8d, ouvert au commit de D8b ; au plus tard avant l'acte de publication (`JOURNAL.md` l.141) |
| SHOGEN-SECRETS-CHEMIN-ETAGE-1 (I-G2-1) | journal D8b l.465 | **re-formé vers D8d** : non mesurable en local (chemin refusé par Git for Windows) | G0 de D8d, ou forge rétablie |
| SHOGEN-SECRETS-GREP-STATUT-1 (I-G2-2) | journal D8b l.466 | **re-formé vers D8d** : c'est une recherche (capter les statuts sans changer le verdict) ; le hook en hérite, D8c ne le masque pas (CH-8) | G0 de D8d |
| extension de HOOK-SECRETS-1, noms de chemin (I-G2-3) | journal D8b l.467 | **re-formé vers D8d** : changement de la gate, que le hook reprend sans modification | G0 de D8d |
| SHOGEN-SECRETS-MASQUE-EXCLUSION-1 (I-G2-4) | journal D8b l.468 | **re-formé** : aucun fichier d'exclusion n'existe (§5.3) et D8c n'en crée pas | première entrée du fichier d'exclusion, ou G0 de D8d |

**Demande formée pour SHOGEN-LINT-LECTEUR-CC-1** (procurement adressé à l'orchestrateur ; lecture sur place, acte de l'orchestrateur) :
- pages primaires à lire, puis à consigner en FAITS datés : réglages de Claude Code (`https://code.claude.com/docs/en/settings`), sous-agents (`…/sub-agents`), skills (`…/skills`), hooks (`…/hooks`) ; si les pages ne tranchent pas, le code du paquet npm de Claude Code, après lecture de ses conditions d'usage et sur go (téléchargement) ;
- questions : (1) les réglages admettent-ils des commentaires ou une virgule finale ? (2) quel lecteur YAML lit le frontmatter, et qui gagne entre deux clés dupliquées ? (3) un frontmatter invalide est-il ignoré en entier ou lu en partie ? (4) une clé échappée est-elle décodée ? (5) un hook déclaré dans un frontmatter porte-t-il une clé `model` ?
- usage : relâcher un refus de CH-12 ou CH-13 seulement sur FAITS ; fermer le reste d'IMBRIQUE-1 ; établir le sens « accepter » (toute forme acceptée par le lint est lue de même par Claude Code) ;
- tentatives du G0 : aucune lecture de page, à dessein (règle de lecture sur place ; E-3 de D8a) ; les mesures du §5.4 prennent PyYAML comme lecteur de référence local, déclaré différent de celui de Claude Code.

### 11.2 Items formés par ce G0

| # | item | objet | propriétaire | déclencheur | origine |
|---|---|---|---|---|---|
| 1 | SHOGEN-HOOK-INSTALL-1 | installation sur `F:/Shogen` selon CH-6, ligne de JOURNAL (empreintes avant et après, sauvegarde), puis `--verifier` au G3 opérant ; réinstallation à chaque lot qui change le hook | orch. | G7 du dernier sous-lot de D8c | CH-6 ; tuyau du §10 |
| 2 | SHOGEN-HOOK-COUVERTURE-1 | `cherry-pick` et `rebase` créent des commits sans pre-commit (mesuré, §5.1 f ; précédent : `f11bdca`, cherry-pick du 2026-08-20) ; **recherche** d'une construction côté client (piste à lire : le hook `reference-transaction` de git, qui peut refuser une mise à jour de ref ; non lu), ou rejeu du G3 opérant après chaque commit de ce type ; `pre-merge-commit` inutile sur `main` (fusions refusées, git-ci l.179) | orch. | premier commit sur `main` produit par `cherry-pick` ou `rebase`, ou prochain lot qui touche aux hooks | CH-15 ; PAROXYSME |
| 3 | SHOGEN-G5-FORGE-1 | (a) `g5-no-naked-todo` aux contrôles requis (GC-09) ; (b) premier run sur la forge (GC-01) ; (c) ce que l'oracle local ne prouve pas : `git grep -E` et le mot-frontière sur l'image, `mktemp`, `sha256sum`, `checkout-index`, modes de fichier, durée du runner sur Linux | orch. ; (a) investisseur ou mainteneur | forge rétablie (dépôt public, `JOURNAL.md` l.141) | modèle : SHOGEN-G1-FORGE-1 ; O-8 |
| 4 | SHOGEN-HOOK-SUITE-S2-1 | le hook est l'image des gates textuelles (g5, g1, g3), pas du job `s2-harness-unittest` (suite ≈ 10 s, `gates.yml` l.98) ni des workflows cargo ; décider l'ajout de la suite au hook, lue sur une extraction de l'index, variable scellée retirée | orch. | premier commit sur `main` qui rougit la suite sans que le G3 opérant l'ait vu, ou G0 de RENDU-1, au premier des deux | §3 OUT ; PAROXYSME |
| 5 | SHOGEN-D8D-SECRETS-1 | ouvrir le lot proposé **D8d** (gate secrets : messages, noms de chemin, chemin d'étage, statut de `grep`, masquage), G0 bref, ligne datée à l'annexe A | orch. | commit de D8b ; construction avant l'acte de publication | §11.1 ; Q-G0-6 |
| 6 | SHOGEN-MENACES-D8-MAJ-1 | `docs/17-modele-de-menace.md` : la colonne des contrôles de T-10 (l.68 : hook non versionné, marqueurs seulement) et de T-12 (l.70 : pas de lint sur `main`) est périmée depuis `de12b8b`, et le sera pour T-10 à l'installation ; puce datée proposée au journal G1 | orch. | commit de D8c | §13.2 ; `docs/17` l.82 |
| 7 | SHOGEN-HARNAIS-ECHAPPEMENTS-1 (transmission) | une double barre oblique inverse et une séquence d'échappement unicode tapées dans une commande peuvent arriver transformées à bash, sans stabilité d'une commande à l'autre (§5.1 h) : tout regex écrit par un worker doit être contrôlé sur les octets écrits (`od -c`, sha256), et les barres écrites depuis un gabarit (`tr`, `printf` en octal) ; consigne aux commandes de mission | orch. (gabarit de mission) | prochaine commande de mission qui porte un regex | §5.1 h |
| 8 | SHOGEN-WORKTREE-BASE-HOOK-1 | après l'installation, un worktree dont la base précède D8a et D8b voit ses commits refusés (C-07, C-12) ; consigne « avancer la base avant tout commit local » aux commandes de mission ; le harnais crée parfois les worktrees sur une base ancienne (E-1 des G1 de B0 et de D8a) | orch. | installation (item 1) | CH-7 ; §10 |

- *Amendement daté du 2026-10-01 (correction de la revue G2, C-G2-9)* : item 2 re-formé. (a) Fusions : `git merge --no-ff` ne lance pas pre-commit (mesuré par la revue G2 : une branche marquée, committée avant l'installation, fusionne sans refus) ; construction mesurée : le même blob installé aussi en `pre-merge-commit` (branche marquée refusée en `HOOK/g5`, fusion propre acceptée) ; prix ≈ 12 à 20 lignes [inféré] (installeur : deuxième nom, même `ATTENDU`, `--verifier` sur les deux ; runner : deux cas) ; décision de construire : question Q-G2-1 de la revue G2 ; déclencheur : au plus tard avant la première fusion d'une partie dans `main` après l'installation (CH-6). (b) `cherry-pick` et `rebase` : interdits par la méthode par parties (PARTIES-S2 l.19) ; rejeu du G3 opérant. La prémisse `pre-merge-commit` inutile sur `main` est retirée.

Aucune limite nommée dans ce document n'est laissée sans item ou sans décision : les limites de CH-15 sont portées par les items 2, 3 et 4, par T-11 (§13.2) et par la revue G2.

## 12. Critères d'acceptation fermés

- **CA-D8c-1** : `git diff --name-status <base>` = exactement les fichiers IN du §3, base = état après D8b empilé (`293b7a7` ou le `main` du lancement, plus D8b).
- **CA-D8c-2** : `.git/hooks/pre-commit` de `F:/Shogen` inchangé à la fin du G1 et du G2 (sha256 `1da91c72…1277d`) ; aucun appel de l'installeur hors d'un dépôt jetable ; `.claude/agents/*.md` inchangés.
- **CA-D8c-3** : O-1 vert, table du §7 intégrale pour le lot, part de chaque sous-lot publiée.
- **CA-D8c-4** : O-2 : la table S1-S9 est reproduite avec les seuls changements voulus du CH-3.
- **CA-D8c-5** : O-3 = 0 ligne aux deux motifs g5 sur tout fichier ajouté ou modifié, documents compris ; commande du job g5 élargi : sortie 0.
- **CA-D8c-6** : O-4 : k = 0 à 3, jetons attendus.
- **CA-D8c-7** : O-5 : chaque mutant tué par le cas nommé, sauf les équivalents déclarés avec leur commande de rejeu ; catégorie F2P déclarée.
- **CA-D8c-8** : O-6 et O-7 tenus.
- **CA-D8c-9** : O-8 (xtask VERT ; suite identique à la base ; runners de D8a et de D8b et leurs commandes d'arbre verts) et O-9 (0 entrée neuve dans TMP).
- **CA-D8c-10** : O-10 : bloc g5 conforme aux CH-9 et CH-10, autres jobs identiques.
- **CA-D8c-11** : note de DECISIONS transcrite telle que CH-14, faits relus par O-11 ; index non touché.
- **CA-D8c-12** : R-25 mesuré ≤ 200 par sous-lot, estimation scellée avant tout code, règle de coupe du §9 appliquée ; lignes datées proposées pour l'annexe A.
- **CA-D8c-13** : en-tête du hook et de l'installeur conformes aux CH-4 et CH-5 : provenance, écarts, et aucune revendication de garde de commit.
- **CA-D8c-14** : `GIT_DIR` et `GIT_WORK_TREE` absents de toute commande du G1 et du G2 ; garde du runner mesurée (sortie 3).
  - *Amendement du 2026-09-30 (G1)* : garde du runner mesurée avec `GIT_INDEX_FILE` posée vers un chemin inexistant (sortie 3) ; `GIT_DIR` et `GIT_WORK_TREE` ne sont posées par aucune commande du G1 (précédent : O-11 de D8b).
- **CA-D8c-15** : journal G1 au format de `docs/G1-lot-D8a.md` ; vocabulaire 09 respecté (S-G4) ; aucune citation anglaise entre guillemets d'une source non versée (S-G5).
- **CA-D8c-16** : enregistrement d'oracle substitut produit au G1, puis refait par le G2.
- **CA-D8c-17** : items du §11 repris au journal G1 ; versement à l'annexe B par l'orchestrateur.

## 13. Risques

### 13.1 MAST (libellés : annexe C l.13-18 ; les 14 modes restent la liste de revue)

| mode | forme dans D8c | contre-mesure système | preuve |
|---|---|---|---|
| FM-1.1 | le G1 ou le G2 installe le hook, ou lance l'installeur dans son worktree, qui écrirait dans le dossier partagé de `F:/Shogen` (§5.1 e) ; ou pose `GIT_DIR` pour un test ; ou place un agent de cas sous un `.claude/agents/` du dépôt | refus de l'installeur dans un arbre lié (I-06) ; garde `GIT_*` du runner (sortie 3) ; dépôts jetables `mktemp` ; CA-D8c-2 | sha256 du hook réel, `find` |
| FM-3.3 | des tests verts sur un hook trop permissif, ou des cas amont portés sans leur changement voulu (S4, S5, S6, S9) | table S du §5.2 rejouée (O-2) ; égalité des motifs (O-7) ; sortie ET jeton ; mutants MH, MI, MC, ML | O-5 |
| FM-3.2 | l'oracle local ne prouve pas l'image Linux ; le hook ne voit ni `cherry-pick` ni `rebase` | items 2 et 3 du §11.2 ; CH-15 | déclaré |
| FM-2.3 | glissement vers la gate secrets, RUNNERS-1 entier, la suite S2, les réglages globaux | règle d'admission du §11.1 ; lot D8d proposé ; OUT du §3 ; CA-D8c-1 | revue G2 |
| FM-2.4 | faits retenus : copie qui rougit g5, mode harnais inerte, `GIT_DIR` exporté, hooks partagés, CRLF de `git apply`, barres repliées, refus du garde, items de D8b routés ici | §0, §5 et en-tête ; §11.1 | sceaux du §15 |
| FM-1.5 | coupe R-25 improvisée ; hook sans fin sur un gros commit | règle de coupe écrite d'avance (§9) ; coût mesuré par fichier (§5.3), O-12 | journal G1 §1 |
| FM-2.2 | un choix ouvert tranché sans le dire | Q-G0 du §14 | — |

- *Amendement daté du 2026-10-01 (correction de la revue G2, C-G2-9)* : FM-3.2 : le hook ne voit pas non plus une fusion sans conflit ; item 2 du §11.2 re-formé.

Topologie (CA-4) : un G1 mono-agent en worktree, puis un G2 sur une instance séparée, à contexte frais. Aucun autre fan-out : le partage n'a pour motif que la séparation de vérification imposée par le système.

### 13.2 Menaces du modèle de menace traitées (`docs/17-modele-de-menace.md`, l.82 : chaque G0 cite ses T-xx)

- **T-10, fuite de secrets** (l.68 ; surface S-18) : D8c-2 ajoute un contrôle au moment du commit sur le contenu indexé (gate en mode indexé). Hors de ce contrôle : noms de chemin et messages (D8d), commits par `cherry-pick` ou `rebase` (item 2). Résidu inchangé : A(host-integrity).
- **T-12, modèle LLM comme adversaire interne** (l.70 ; S-19) : le hook applique R-13, R-1 et le plancher G3 à chaque `git commit`, y compris aux commits locaux des workers dans leurs worktrees (hooks partagés, mesuré) ; c'est une contre-mesure système, pas une consigne. L'option de contournement est interdite (R-22) et refusée par le garde du harnais (mesuré au §5.1 g) ; l'effacement ou la réécriture du hook installé est vu par `--verifier` au G3 opérant (item 1), sans être empêché.
- **T-11, hôte compromis** (l.69) : non traitée ; l'installeur contrôle des empreintes, pas l'hôte (CH-15).
- **T-09, chaîne d'approvisionnement** (l.67) : un commit peut changer un contrôleur et passer avec lui (CH-7, CH-15) ; défenses : revue G2, CI (arrêtée), G3 opérant.

## 14. Questions pour l'orchestrateur (cp-1)

- **Q-G0-1** : port à écarts nommés (CH-1) plutôt que copie octet pour octet assortie d'une exclusion dans g5 ?
- **Q-G0-2** : étape R-13 = image exacte de g5 sur l'index entier (CH-3), avec ses changements voulus (S4, S5, S6 refusés ; S9, `.claude/`, accepté) ?
- **Q-G0-3** : lecture de « jamais exécuté par le lot » : jamais sur `F:/Shogen` ni sur l'un de ses worktrees, mais exécuté dans des dépôts jetables par le runner (cas I) ?
- **Q-G0-4** : installation = acte de l'orchestrateur après le G7 du dernier sous-lot (CH-6), ou acte de l'investisseur ?
- **Q-G0-5** : part de g5 dans RUNNERS-1 tirée en avance (CH-10) ?
- **Q-G0-6** : lot D8d pour les cinq items de la gate que D8b route ici, plutôt qu'un sous-lot D8c-4 ?
- **Q-G0-7** : amender ADR-0028 §4.11 à l'installation : runner du hook et `--verifier` au G3 opérant ?
- **Q-G0-8** : note de DECISIONS sous le titre de l'ADR-0020 de `main`, index non touché (CH-14) ?
- **Q-G0-9** : les écarts au blob `9c4c846` (CH-1 à CH-3) demandent-ils une ligne à l'annexe E, comme les écarts au canonique de D8a (Q-G0-5 de D8a) ?

## 15. Consignes au G1 et sceaux

- **Worktree** : avancer la base sur le `main` du lancement (`git merge --ff-only`), consigner le sha ; empiler D8b par `git apply --3way F:/tmp/shogen-lots/D8b/lot.diff` **dans le worktree** (attributs du dépôt : LF), contrôler les sha256 de l'état corrigé (§5.1 h), puis un commit local d'empilement. Ce commit passe par le hook local actuel : les lignes ajoutées de D8b ne portent aucun marqueur (O-7 de D8b, remesuré au §5.3).
- **Jamais** : lancer l'installeur hors d'un dépôt jetable ; écrire sous `F:/Shogen/.git/` ; poser `GIT_DIR`, `GIT_WORK_TREE` ou `SHOGEN_S2_CAMPAGNE_CONTROL` ; utiliser `--write-tree` ; taper l'option de contournement de `git commit` dans une commande (R-22 ; le garde du harnais la refuse) ; ouvrir une pièce de D.2.
- **Écriture des scripts** : toute barre oblique inverse double d'un regex s'écrit depuis un gabarit (`tr`, `printf` en octal) et se contrôle sur les octets (`od -c`) ; sha256 de chaque état publié (§5.1 h, item 7).
- **TMP** : `TMPDIR`, `TMP` et `TEMP` sur un dossier neuf sous `F:/tmp/shogen-tests-tmp/d8c-g1/` pour chaque rejeu compté (O-9) ; `CARGO_HOME` et `CARGO_NET_OFFLINE=true` de la mission ; garde de B0 pour `cargo xtask`.
- **Documents** : la copie de ce G0 et le journal sont lus par S-G4, S-G5 et g5 élargi : aucun marqueur de dette littéral (O-3), aucune citation anglaise entre guillemets, guillemets droits seulement dans des spans de code.
- **Journal `docs/G1-lot-D8c.md`**, au format de `docs/G1-lot-D8a.md` : en-tête (modèle, horloge, mandat, base) ; §0 préconditions (PC-1, empilement de D8b) ; §1 coupe R-25 (estimation scellée avant code, puis mesure) ; §2 changements (sha256) ; §3 CH-1 à CH-15 appliqués ; §4 tests, chacun nommant sa mutation ; §5 mutants ; §6 oracles ; §7 tuyaux et texte proposé pour §4.11 ; §8 MAST ; §9 `error_origin` ; §10 Review Focus ; §11 questions et items ; §12 livrables ; §13 contraintes d'environnement ; §14 attestation.
- **Textes proposés par le G1, actes de l'orchestrateur** : lignes datées de l'annexe A (§9) ; versement des items du §11 à l'annexe B ; RUNNERS-1 ramené à 11 définitions ; puce datée de `docs/17` (item 6) ; amendement de §4.11 (Q-G0-7).
- **Sceaux** : `F:/tmp/shogen-lots/D8c/g0-mesures/SHA256SUMS.txt` liste les sondes, leurs sorties, les copies (`hook-local-9c4c846.copie`, `amont-9dade29.sh`) et les horloges ; son sha256 et celui de ce document sont écrits à côté (`G0-lot-D8c.md.sha256`). Rejeu : chaque sonde se relance depuis `g0-mesures/` (lint ou hook en argument quand elle en prend un) et reproduit sa sortie ; `mesure-composition.sh` lit `work/arbre/`, à reconstruire par `git archive 293b7a7 ':!biblio'`, application de `lot.diff` de D8b et retrait des CR.

## 16. Attestation (forme d'ADR-0028 D.3)

- **Pièces lues** : celles du §4. **Non ouvertes** : toutes les pièces de l'annexe D.2 ; `F:/shogen-campagne/*`, `F:/tmp/shogen-j28/*`, `campagne.md` et le dossier `campagne` de la cartographie (leurs noms ont été vus dans une liste de répertoire, aucun fichier ouvert).
- **Balayages mécaniques** : `git grep` sur `293b7a7`, `40b4cfb` et `lot.diff` de D8b, comptes seuls affichés.
- **Aucune statistique S2 calculée ; aucun z, K, P̂_more ni φ vu.** `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée.
- **Isolation git** : aucun `GIT_DIR`, aucun `GIT_WORK_TREE`, aucun `--write-tree` posés par le rédacteur ; écarts consignés en tête (`git status` sans verrou optionnel désactivé ; refus du garde du harnais). Morceaux de commande sous 6 Ko, sauf le premier (6,4 Ko, sous le seuil de lexage de 7,6 Ko).
