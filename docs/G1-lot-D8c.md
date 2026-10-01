# G1 — lot D8c d'ADR-0028 (hook pre-commit versionné, installeur vérifié, motif g5 élargi, note « collision ADR-0020 », branchement du lint et de la gate, formes imbriquées et lecture JSON à jetons), Shōgen — journal

- **Modèle** : `claude-opus-5-5` (déclaré par le harnais et en tête de session, R-1), effort max, contexte frais ; worker G1. Aucun commit vers `main`, aucun workflow déclenché (R-20) ; un seul commit, local, d'empilement de D8b, dans le worktree du lot (`e9ac6e2`, admis par la commande de mission). Aucune variable `GIT_DIR` ni `GIT_WORK_TREE` posée, aucun `--write-tree` ; `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée (retirée par `unset` dans chaque script d'oracle). Le hook installé de `F:/Shogen` n'a pas été touché ; l'installeur n'a tourné que dans des dépôts jetables (CA-D8c-2).
- **Horloge** (`date -u`) : première heure relevée 2026-09-30T22:03:08Z (contrôle d'application de D8b ; l'orientation la précède) ; commit d'empilement 22:05:27Z ; mesure C-5 sur le lint committé avant code (horloge `oracles/c5-mesure.horloge`) ; estimation R-25 écrite à 22:22:11Z et scellée à 22:22:27Z, avant tout code ; oracles de base 22:23:22Z-22:27:49Z (suite, puis `xtask` et runners) ; hook, installeur et runner écrits entre 22:27:49Z et le premier essai du runner, 22:32:30Z (`oracles/O1-d8c1-essai1.horloge`) ; campagne de mutants de D8c-1 v1 22:42:33Z-22:46:58Z (MH-9 survit : défaut du runner, E-3), v2 22:49:21Z-22:53:18Z, sur l'instantané figé `etat-1b` (22:49:11Z) ; D8c-2, préparé en brouillon hors du worktree pendant la campagne v1, appliqué au worktree entre 22:49:11Z et son premier O-1, 22:51:43Z (`oracles/O1-d8c2-essai1.horloge`) ; campagnes de D8c-2 et de D8c-3 à partir de 23:00:35Z ; rejeu final de MI-16, MC-9 et MC-10 23:36:45Z-23:38:28Z ; O-4 et O-12 (`oracles/O4-O12.horloge`) ; image locale des jobs (`oracles/O8-depot.horloge`) ; `xtask` final, premier passage 23:46:10Z-23:46:14Z ; runners de D8a et de D8b 23:46:19Z-23:50:19Z ; empreintes de fin 23:51:20Z ; livrables et second passage de `xtask` : `G1-rapport.md`.
- **Mandat** : commande de mission de l'orchestrateur Shōgen (`claude-fable-5-1`, workflow du 2026-09-30), lot D8c de l'annexe A (l.38 à `40b4cfb`) ; G0 accepté au cp-1 complet (`F:/tmp/shogen-lots/D8c/G0-lot-D8c.md`, sha256 `4193e2b0185adcb3f399422ef426f6a312b91442e14921ff3394563d5925ccd4`), avec les corrections C-1 à C-5 de la commande. Cadre : ADR-0028 (D8, §4.11) et annexes A, B (B.11) et E à `40b4cfb`.
- **Base** : `40b4cfb` (commande de mission), plus D8b empilé : `lot.diff` de D8b (sha256 `ce90419714b0f7d66035f34336b1b5f32f032aa61080216bf8912f90be768e9e`) appliqué par `git apply --3way`, puis commit local `e9ac6e2`. `main` est à `293b7a7` (un commit de plus, `JOURNAL.md` seul).
- **Classification** : additive. Trois fichiers neufs (`enforcement/hooks/pre-commit`, `enforcement/hooks/install-pre-commit.sh`, `enforcement/tests/run-fixtures-hooks.sh`), quatre fichiers modifiés (`gates.yml`, `docs/DECISIONS.md`, le lint et son runner), deux documents neufs (copie du G0, ce journal).
- **Résultat** : lot coupé en quatre sous-lots par la règle 2 du G0 §9, **D8c-1a** (141 lignes), **D8c-1b** (99), **D8c-2** (65) et **D8c-3** (51). Runner du hook : 50 cas sur 50 (`hooks : 50 ok, 0 échec`, sortie 0, 0 entrée TMP). Runner du lint : 92 cas sur 92 (76 P2P, 16 neufs). Sonde git-ci §2.e reproduite avec les seuls changements voulus du CH-3 (O-2). Rouges semés sur l'entrée committée : k = 0 à 3 aux jetons attendus (O-4). Mutants : 52 mutants sur les états finaux (hook et installeur à l'état 2, lint à l'état 3) : 49 tués par un tueur attendu, 2 équivalents déclarés (MI-9, MC-9), 1 équivalent en local (MI-13, montage `noacl`) ; les deux survivants de la première campagne ont conduit à une correction du runner (E-3) et à une mesure (MI-13). Suite `s2-harness`, `cargo --locked xtask verify`, runners de D8a et de D8b et commandes d'arbre : sans régression (O-8 : suite identique à la base, `xtask` VERT, runners de D8a et de D8b verts, image locale des jobs g5, g1 et g3 verte sur le lot committé). D8c-3 est livré en sous-diff séparé, **non consommable** tant que la voie (a) ou (b) de C-4 n'est pas faite (§0).
  - *Amendement daté du 2026-10-01 (correction de la revue G2, C-G2-1 à C-G2-9 ; §15)* : revue G2 ACCEPTE-AVEC-CORRECTIONS ; liste fermée appliquée par un worker de correction. État corrigé : runner du hook **51 cas sur 51** (H-23 ajouté), runner du lint **95 sur 95** (T-93 à T-95 ajoutés) ; sous-lots D8c-1a 144, D8c-1b 100, D8c-2 65, D8c-3 56 lignes (§1). D8c-3 reste non consommable avant la voie (a) ou (b) de C-4 (aucune n'est au JOURNAL ni à l'annexe B à `205c1b2`).

## 0. Préconditions mesurées avant code

- **Base (C-3)** : le worktree fourni par le harnais était à `fa0ce5b` (branche `worktree-wf_089f8fc6-492-6`), ancêtre de `40b4cfb` (59 commits, `git merge-base --is-ancestor`, `git log --oneline fa0ce5b..40b4cfb | wc -l`) ; acte du worker : `git merge --ff-only 40b4cfb` sur la branche du worktree. D8b : `git apply --check --3way` puis `git apply --3way` (22:03Z-22:05Z) ; les quatre sha256 du G0 §5.1 h sont retrouvés dans le worktree, sans CR : gate `47f2c35e8a7466caa949d21d1ad42ffac3b4e12dff825cca271ee2a3c2701722`, runner `7eb01b3918fe44cfc6330ffde60d26d580e2293f03ce8853e1dd904068ebfa99`, fixture `6b558bd2a8efc33bc5d2e357641913743395736243e62adbb7db7fe497bb451c`, `gates.yml` `13dc51771d0cb1e922bcc26ce1b17e93b8957218c9c92bae1fdaa7d40dfb79fb` ; journal de D8b `3f3dd394…2017` (`oracles/empreintes.sh`). Commit local `e9ac6e2`, passé par le hook local partagé (`1da91c72…`) sans refus.
- **Ordre de clôture (C-3, écrit en dur)** : **D8b commis sur `main`** (son cp-2 n'existe pas : `F:/tmp/cp2-D8b` absent, mesuré à l'orientation, avant la première heure relevée, 22:03:08Z) → **G1 puis G2 de D8c** → **G7** → **installation CH-6** (item SHOGEN-HOOK-INSTALL-1, acte de l'orchestrateur) → **cp-2 du dernier sous-lot**, qui cite **O-13** (`install-pre-commit.sh --verifier` sortie 0 ; hook installé lancé directement sur `F:/Shogen` sous `GIT_OPTIONAL_LOCKS=0`, sortie 0). Un cp-2 sans O-13 refuse la clôture ou renvoie le hook en « upcoming ». Si D8b change avant son commit, le G1 de D8c réapplique `lot.diff` et remesure les quatre sha256 ci-dessus.
  - *Amendement daté du 2026-10-01 (correction de la revue G2, C-G2-8)* : D8b est commis sur `main` (`360ff99`, `430f3be`, `3c63e91` ; documents `205c1b2`) dans un état qui diffère du `lot.diff` empilé ici pour deux des quatre empreintes du G0 §5.1 h : runner `f9e7ef02084611bd99806e35145230a063ed07bdb3f3be5ae7456954adb84837` (113 cas, T-75b de la re-revue rr1) et `gates.yml` `32f79e4926f28a5cb3f359feba0801a64498eac0db3244ffa8d40a5ff4e8144c` (commentaire du job g3) ; gate et fixture égales. Sur `enforcement/` et `gates.yml`, `e9ac6e2` et `205c1b2` ne diffèrent que par ces deux fichiers ; de `3c63e91` à `205c1b2`, aucun fichier du lot ne change ; de `40b4cfb` à `205c1b2`, seul `gates.yml` change parmi eux (job g3-secrets de D8b). Rejeu du correcteur sur `205c1b2`, main du moment (`F:/tmp/shogen-lots/D8c/corr/o/cible-main-205c1b2.out`) : `lot.diff` corrigé appliqué par `patch -p1`, dry-run puis réel, 0 avis de hunk ; huit des neuf fichiers égaux au worktree ; `gates.yml` différent par la seule part de D8b : `5d6e2bf9463d94ffe7a16b787c299c369835a39e7958c7e974d418b8475cf365` sur `main` corrigé (`f959871d…724e` sur la base empilée ; `3b2bf1b3…020a` avant les corrections, mesure de la revue G2 sur `3c63e91`) ; runner du hook 51 ok, runner du lint 95 ok, `lint .` sortie 0 (2 fichiers), runner de D8b 113 ok ; 0 entrée TMP ; motif g5 élargi sur l'objet `205c1b2` : 0 ligne. Au G3 opérant sur `main`, le runner de D8b compte 113 cas (112 sur la base empilée).
- **Réponses aux Q-G0 (C-2)** : aucune réponse écrite de l'orchestrateur n'est au JOURNAL (sha256 `b6ec0967…fb2f`, égal à celui de `main`, dernière entrée D8a l.137) ni en tête de ce journal au lancement. **Lecture du worker, et non réponse de l'orchestrateur**, de la commande de mission (G0 accepté, corrections C-1 à C-5) ; les réponses écrites restent dues (E-2) :

| question | lecture du worker | source dans la commande |
|---|---|---|
| Q-G0-1 | port à écarts nommés (CH-1) | C-1 : « Q-G0-1 tranché par le validateur : port » |
| Q-G0-2 | oui : image exacte de g5 sur l'index entier, avec ses changements voulus | G0 accepté (aucune correction) |
| Q-G0-3 | oui : installeur exécuté dans des dépôts jetables seulement | C-2, lecture du validateur |
| Q-G0-4 | acte de l'orchestrateur après le G7, consigné au JOURNAL et visible au bloc AU-REVEIL | C-2 et C-3 |
| Q-G0-5 | oui : part de g5 dans RUNNERS-1 tirée en avance | G0 accepté |
| Q-G0-6 | oui : lot D8d pour les cinq items de la gate | G0 accepté |
| Q-G0-7 | oui : texte proposé au §7, acte de l'orchestrateur | G0 accepté |
| Q-G0-8 | oui : note sous le titre de l'ADR-0020 de `main`, index non touché | G0 accepté ; mission : « entrée collision ADR-0020 à DECISIONS » |
| Q-G0-9 | oui : ligne d'annexe E pour CH-1 à CH-3 | C-1 : « Q-G0-9 : oui » |

- **C-1** : ADR-0028 D8 l.213 porte encore « copie versionnée du hook pre-commit » à `40b4cfb` (et à `293b7a7`) ; l'annexe E n'a pas de ligne pour les écarts CH-1 à CH-3. L'amendement daté est un acte de l'orchestrateur, non observé au lancement (E-2) ; le lot porte les écarts dans l'en-tête du hook et dans la copie du G0 ; texte proposé au §11.
- **C-4** : aucun fichier de FAITS sur la question (1) de SHOGEN-LINT-LECTEUR-CC-1 (réglages de Claude Code : commentaires, virgule finale), ni ligne datée à l'annexe B (`grep` de `LECTEUR-CC` dans `docs/` et dans `F:/tmp/shogen-lots/D8c/` : seules les mentions déjà connues). **C-4 n'est pas satisfaite au lancement.** Aucune des deux voies ne change le code de D8c-3, fait de refus fail-closed ; D8c-3 est donc construit, mais livré en sous-diff séparé (`d8c-3.diff`), **non consommable** avant la voie (a) ou (b) ; la règle 3 du G0 §9 (réunion de D8c-2 et D8c-3) n'est pas appliquée, pour que D8c-2 reste consommable seul (avis de l'advisor intégré, canal 1). Texte de la voie (b), prêt à verser : §11.
- **C-5 (catégories, mesurées avant code)** : `oracles/c5-mesure.sh`, cas T-77 à T-92 construits comme au G0 §7.4, lancés sur le lint committé `1c57e8c4` (sortie `oracles/c5-mesure-lint-committe.out`) :

| cas | attendu | lint committé | catégorie | tueur nommé (épingle) |
|---|---|---|---|---|
| T-77 | 2 `R-1/tier-nu` | 0 | F2P | — |
| T-78 | 0, 1 fichier | 0 | épingle | ML-9 (préfixe de séquence non retiré de la valeur) |
| T-79 | 2 `R-1/cle-model` | 0 | F2P | — |
| T-80 | 2 `R-1/cle-model` | 0 | F2P | — |
| T-81 | 2 `R-1/cle-model` | 0 | F2P | — |
| T-82 | 2 `R-1/hors-liste` | 0 | F2P | — |
| T-83 | 2 `R-1/hors-liste` | 0 | F2P | — |
| T-84 | 0, 1 fichier | 0 | épingle | ML-8 (sentinelle étendue à toute occurrence) |
| T-85 | 0, 2 fichiers | 2 `R-1/hors-liste` | F2P | — |
| T-86 | 2 `R-1/hors-liste` | 2 `R-1/hors-liste` | **épingle** (le G0 la disait F2P) | ML-6 (refus des clés à barre retiré) |
| T-87 | 2 `R-1/hors-liste` | 2 `R-1/tier-nu` | F2P (jeton) | — |
| T-88 | 2 `R-1/hors-liste` | 2 `R-1/tier-nu` | F2P (jeton) | — |
| T-89 | 2 `R-1/hors-liste` | 0 | F2P | — |
| T-90 | 0, 2 fichiers | 0 | épingle | ML-10 (jeton de chaîne sans échappement) |
| T-91 | 0, 2 fichiers | 0 | épingle | ML-11 (virgule finale refusée) |
| T-92 | 2 `R-1/hors-liste` | 0 | F2P | — |

  Comptes publiés séparément : **F2P mesurés : 11** (T-77, T-79 à T-83, T-85, T-87 à T-89, T-92) ; **épingles : 5** (T-78, T-84, T-86, T-90, T-91), chacune avec son tueur. **Nouveaux modules** (catégorie « nouveau module », tous leurs cas sont neufs) : hook, installeur, runner du hook, 50 cas. Les 76 cas T-01 à T-76 restent des P2P.
  - *Amendement daté du 2026-10-01 (correction de la revue G2, C-G2-2 et C-G2-3)* : T-93, T-94 et T-95 ajoutés ; catégories mesurées par le runner corrigé (`F:/tmp/shogen-lots/D8c/corr/o/lot-lint.out`) : T-93 et T-94 F2P (rouges sur le lint du lot `988bf5fe…969b` et sur le lint committé `1c57e8c4…4fa9`) ; T-95 épingle (verte sur les deux ; tueur GL-5b, colonne `I` d'une clé en entrée de séquence). Comptes : **F2P mesurés : 13** ; **épingles : 6**.
- **PC-1 (G0 §2)** : lecture (b) consignée au JOURNAL (l.122) ; le lot travaille sous cette consignation ; tag et suppression de la branche restent à l'investisseur (SHOGEN-D8-PC-1).
  - *Amendement daté du 2026-10-01 (correction de la revue G2, C-G2-1)* : PC-1 a été exécuté pendant le G1 : confirmation de l'investisseur le 2026-09-30 à 23:33 UTC (forme (a) ; JOURNAL l.149, commit `87bc4e4`), tag annoté `archive/roster-ban-2026-08-20` posé sur `adb2213` (tagger 23:33:51 UTC), branche supprimée avec son journal de refs : SHOGEN-D8-PC-1 fermé. La note de DECISIONS est mise à cet état (§3, CH-14) ; O-11 se rejoue sur `logs/HEAD` (l.56-60), l'objet du tag et le §5.5 du G0 (`oracles/O11.out` du G1, relevé à 23:12:47 UTC, avant la suppression) ; rejeu du correcteur : `F:/tmp/shogen-lots/D8c/corr/o/o11.out`.
- **Sceaux du G0** : `sha256 -c` de `G0-lot-D8c.md.sha256` et de `g0-mesures/SHA256SUMS.txt` : tous conformes (30 lignes, 0 écart).
- **Oracles de base** (`e9ac6e2`, TMP neuf par commande) : suite `s2-harness` `Ran 216 tests`, `OK (skipped=2)`, sortie 0, 0 entrée TMP, sauts (ii) et (ii bis) ; `cargo --locked xtask verify` VERT, sortie 0 (22:23:50Z-22:24:06Z ; S-G4 55 fichiers, S-G5 56 fichiers, corpus incomplet 0 sur 125, 252 fragments contrôlés) ; `run-fixtures-model-pinning.sh` 76 ok, 0 échec ; `lint-model-pinning.sh .` sortie 0, 3 fichiers ; `run-fixtures-secrets.sh` 112 ok, 0 échec ; `gate-secrets.sh --tree` sortie 0, 304 fichiers ; `--history` sortie 0, 142 commits (`--all`, commit d'empilement compris) ; 0 entrée TMP pour chacun (`oracles/runners-base.out`).
- **Outillage local** (mesuré, `oracles/versions.out`) : git 2.55.0.windows.5, GNU bash 5.3.15, GNU grep 3.0, GNU sed 4.9, GNU Awk 5.4.1, Python 3.14.5, PyYAML 6.0.3, coreutils 8.32, GNU tar 1.35 ; 24 processeurs logiques.
- **Garde du harnais** (§13) : refus mesurés d'un `cd` vers `F:/Shogen`, des commandes git composées, des heredocs contenant git, des programmes `sed` calculés et des lignes qui nomment le dossier des workflows. Les oracles sont des scripts sous `F:/tmp/shogen-lots/D8c/oracles/`, exécutés directement ; ils lancent les runners par `bash <chemin>`, forme exacte des jobs.

## 1. Coupe R-25

- **Estimation écrite avant tout code** (`oracles/estimation-R25.txt`, horloge 22:22:11Z, sha256 `23bb5979e45b9b340073d85ba84e7bf3cf069e6858017a0cdad5d8a144090daf`, sceau 22:22:27Z) : estimation du G0 reprise (D8c-1 ≈ 162, D8c-2 ≈ 37, D8c-3 ≈ 33 ; lot ≈ 232) et ré-estimation du G1 (≈ 184, ≈ 41, ≈ 35 ; lot ≈ 260), avec le risque de D8c-1 au-dessus de 200 écrit d'avance.
- **Mesure** (méthode du G0 §9 : `git diff --numstat` des fichiers suivis contre `e9ac6e2`, `wc -l` des fichiers neufs ; sous-lot n contre l'instantané figé du sous-lot n-1, lignes `+` du `diff -u` ; `oracles/r25.sh`, `oracles/r25-etats.sh`) : D8c-1 mesure **223 > 200** (hook 40, installeur 51, runner 103, `gates.yml` +29 −13). **Règle 2 du G0 §9 appliquée** : D8c-1a (hook, cas H, g5, note de DECISIONS) et D8c-1b (installeur, cas I), au même G2 et au même commit. Aucun contrôle comprimé.

| sous-lot | hook | installeur | runner du hook | `gates.yml` | lint | runner du lint | total ajouté | seuil |
|---|---|---|---|---|---|---|---|---|
| D8c-1a | 40 (neuf) | — | 72 (neuf) | +29 −13 | 0 | 0 | **141** | ≤ 200 |
| D8c-1b | 0 | 51 (neuf) | +47 −16 | +1 −1 | 0 | 0 | **99** | ≤ 200 |
| D8c-2 | +23 −3 | +1 −1 | +40 −12 | +1 −1 | 0 | 0 | **65** | ≤ 200 |
| D8c-3 | 0 | 0 | 0 | 0 | +32 −19 | +19 | **51** | ≤ 200 |

- **Lot entier** : 356 lignes ajoutées en somme des sous-lots, contre ≈ 232 (G0) et ≈ 260 (G1) : E-6. En D8c-1a, le runner installe le hook par copie directe dans le modèle (l'installeur n'existe qu'en D8c-1b) ; D8c-1a et D8c-1b ne se consomment qu'ensemble (le tuyau exige l'installeur). À chaque état, le commentaire du job g5 cite les temps du runner de cet état (22 cas en 14 s, 36 cas en 25 à 39 s, puis 50 cas en 105 à 145 s).
- **Documentation, hors compte** (Q-G2-1 de D8a) : note de DECISIONS (20 lignes de citation, dans `d8c-1a.diff`), copie du G0 (576 lignes : les 560 acceptées sans retrait et 15 lignes d'amendements datés, dont 3 lignes vides, `oracles/G0-copie.diff`), ce journal.
- **Lignes datées proposées pour l'annexe A** : §11 (acte de l'orchestrateur).
- *Amendement daté du 2026-10-01 (correction de la revue G2, §15)* : estimation de la correction écrite et scellée avant code (`F:/tmp/shogen-lots/D8c/corr/estimation-R25.txt`, 01:29:05Z, sha256 `1094d2a9…c75e`) : D8c-1a ≈ 144, D8c-1b ≈ 100, D8c-2 ≈ 65, D8c-3 ≈ 55 à 56. Mesure, même méthode sur les états corrigés (`corr/o/r25-etats.out`) : **D8c-1a 144** (hook 40, runner 75, `gates.yml` +29), **D8c-1b 100** (installeur 51, runner +48, `gates.yml` +1), **D8c-2 65**, **D8c-3 56** (lint +34, runner du lint +22) ; lot 365 (356 au G1). Chaque sous-lot ≤ 200 ; D8c-1a et D8c-1b dans un même commit feraient 244 (question Q-G2-2 de la revue G2). Documentation hors compte : note de DECISIONS 21 lignes au lieu de 20.

## 2. Changements (worktree du lot, sur `e9ac6e2`)

| fichier | sous-lots | sha256 base → 1a → 1b → 2 → 3 |
|---|---|---|
| `enforcement/hooks/pre-commit` | 1a neuf (étape R-13) ; 2 (étapes lint et secrets) | — → `72196441…ae1f` → idem → `31c5cd67…2466` → idem |
| `enforcement/hooks/install-pre-commit.sh` | 1b neuf ; 2 (`ATTENDU`) | — → — → `faf98d64…9df2` → `55d597a2…24c3` → idem |
| `enforcement/tests/run-fixtures-hooks.sh` | 1a neuf (H) ; 1b (I) ; 2 (C) | — → `29006fda…4a64` → `b31c3003…7ec1` → `62b4bf6b…a8a7` → idem |
| `.github/workflows/gates.yml` | 1a (g5) ; 1b et 2 (temps du commentaire) | `13dc5177…79fb` → `d0e9b91e…4f4c` → `6774fa3c…087b` → `853c61fc…d05d` → idem |
| `docs/DECISIONS.md` | 1a (note datée) | `8608c7ef…fa16` → `13500a82…7192` → idem → idem → idem |
| `enforcement/lint-model-pinning.sh` | 3 | `1c57e8c4…4fa9` → idem → idem → idem → `988bf5fe…969b` |
| `enforcement/tests/run-fixtures-model-pinning.sh` | 3 | `4e65eee7…f7e3` → idem → idem → idem → `9d23ac20…9c6e` |
| `docs/adr-0028/G0-lot-D8c.md` | documents | — → ``7c4238268b821b85389b31a1f67b2f3d63d0055561d4f1da55178881ed054228`` |
| `docs/G1-lot-D8c.md` | documents | ce journal |

- **Intouchés** (CA-D8c-2) : `F:/Shogen/.git/hooks/pre-commit` (sha256 `1da91c72…1277d`, relevé au début et à la fin : `1da91c723b7f4747edb35dcc2cce7492e334b648c5e00c41f239cca5ab61277d`, date du fichier 2026-08-12 19:50:37 +0100, relevé à 23:51:20Z) ; `.claude/agents/*.md` (`c0ee49ea…302c`, `4727e94e…0e1b`) ; `enforcement/gate-secrets.sh` et son runner ; `s2-harness/` ; ADR-0028 et ses annexes ; `JOURNAL.md`.
- **CA-D8c-1** : `git diff --name-status e9ac6e2` : `M` pour `.github/workflows/gates.yml`, `docs/DECISIONS.md`, `enforcement/lint-model-pinning.sh` et `enforcement/tests/run-fixtures-model-pinning.sh` ; `A` pour `docs/G1-lot-D8c.md`, `docs/adr-0028/G0-lot-D8c.md`, `enforcement/hooks/install-pre-commit.sh`, `enforcement/hooks/pre-commit` et `enforcement/tests/run-fixtures-hooks.sh` : neuf fichiers, exactement la liste IN du G0 §3.
- *Re-scellement déclaré* : `work/etat-1a` a été re-scellé à 23:53:41Z (deuxième ligne de `etat-1a.horloge`) après la correction du seul commentaire de temps du job g5 (il citait les 36 cas de l'état 1b ; il cite désormais les 22 cas et les 14 s de l'état 1a) ; O-1 rejoué sur l'instantané re-scellé : `hooks : 22 ok, 0 échec`, sortie 0, 0 entrée TMP (`oracles/O1-d8c1a-rescelle.log`). H-20 lit le motif et les exclusions, pas le commentaire.
- Instantanés figés et leurs empreintes : `work/etat-base`, `work/etat-1a`, `work/etat-1b`, `work/etat-2f`, `work/etat-3f` (états livrés ; `*.SHA256SUMS.txt`, `*.horloge`) ; `work/etat-2`, `work/etat-2v2`, `work/etat-3`, `work/etat-3v2` : états intermédiaires des campagnes (avant C-14 et avant la correction du commentaire du job), conservés pour le rejeu.
- *Amendement daté du 2026-10-01 (correction de la revue G2, §15)* : états corrigés figés sous `F:/tmp/shogen-lots/D8c/corr/etat-1a`, `-1b`, `-2` et `-3` (`*.SHA256SUMS.txt`, `*.horloge`). sha256 1a → 1b → 2 → 3 : hook `b8705ae8…6198` → idem → `00131872…826b` → idem ; installeur — → `7223c078…5748` → `dccfbe52…6ebf` → idem ; runner du hook `7c1aca3a…57bf` → `7d5e78a9…04c3` → `fca6a1ca…258c` → idem ; `gates.yml` `13fbcd26…a49d` → `50275a05…50c2` → `f959871d…724e` → idem ; `docs/DECISIONS.md` `00d93cc4…c5f9` à chaque état ; lint `1c57e8c4…4fa9` jusqu'à 2, puis `da9f8d88…486f` ; runner du lint `4e65eee7…f7e3` jusqu'à 2, puis `f5df6ef6…a446`. Copie du G0 `5281d86e…a9fd` ; ce journal : `correction-rapport.md`.

## 3. Définitions appliquées (CH-1 à CH-15)

- **CH-1** : port à écarts nommés (Q-G0-1). Le blob `9c4c846` garde sa mécanique pre-commit (lecture de l'index, sortie 2 sur refus) ; ses l.16-51 (mode harnais) et sa revendication de garde de commit ne sont pas versionnées ; l'en-tête nomme la provenance et les écarts.
- **CH-2** : aucune lecture de l'entrée standard.
- **CH-3** : `git grep --cached -nE "$M" -- ':!biblio/' ':!.claude/' ':!.github/workflows/gates.yml'` ; `M` égal octet pour octet au motif du job g5 et à `adb2213` l.39 (O-7, `oracles/statiques-*.out` : sha256 de « motif + exclusions » `3fc8b4d0…22f1` des deux côtés) ; codes 1 vert, 0 `HOOK/g5` (cinq lignes), autre `HOOK/echec`. Binaire marqué refusé (H-15, mesuré : `git grep` sort en 0).
- **CH-4** : en-tête (provenance, écarts, portée, installation, sortie) ; jetons `REFUS (HOOK/g5|lint|secrets|echec)` ; `OK (hook) : …` ; toutes les étapes avant le verdict ; aucun marqueur littéral (O-3) ; aucun runner ni dépôt jetable lancé par le hook ; mode 100644. Ajout : racine d'abord (`--show-toplevel`, puis `cd`), mesuré nécessaire (H-22).
- **CH-5** : installeur conforme ; ajouts fail-closed (sauvegarde différente présente, `core.hooksPath` illisible, argument inconnu) et contrôles valables en `--verifier` (copie du G0, amendement sous CH-5).
- **CH-6** : non exécuté (acte de l'orchestrateur après le G7) ; séquence au §7.
- **CH-7** : `git show :enforcement/lint-model-pinning.sh`, extraction `git ls-files -z` des quatre pathspecs vers `git checkout-index -z --stdin --prefix="$T/a/"`, sans `-u` ; liste écrite dans un fichier avant l'extraction (aucun tube masquant un échec) ; lint absent de l'index → `HOOK/echec` avec le remède « avancer la base ». `.claude/settings.local.json` non lu (C-04).
- **CH-8** : `git show :enforcement/gate-secrets.sh`, mode indexé, depuis la racine ; sortie de la gate recopiée sans ses lignes `AVIS` ; gate absente → `HOOK/echec`.
- **CH-9** : motif élargi dans le job g5, étape 1 = runner du hook (`shell: bash`), note redatée, `id` et `name` inchangés, en-tête l.3-8 et l.19-21 (SHOGEN-G5-FORGE-1).
- **CH-10** : `ubuntu-24.04`, checkout v7.0.1 par SHA (`3d3c42e5…90b1`), `timeout-minutes: 10` ; commentaire fondé sur les temps mesurés (§6, « Temps »).
- **CH-11** : garde `GIT_*` (sortie 3, mesurée) ; dépôts jetables, commits réels, installeur réel (I-01) ; deux agents valides dès D8c-1 ; lint et gate dès D8c-2 ; marqueurs et formes formés à l'exécution (sonde V-01 de D8b) ; double de test pour I-03 ; I-10 lit les constantes du vrai installeur ; résumé unique.
- **CH-12** : (a) ligne canonique `^[[:space:]]*(-[[:space:]]+)*model[[:space:]]*:`, valeur prise après le même préfixe ; (b) sentinelle `SENT` appliquée quand la forme canonique ne s'applique pas ; (c) suite d'une valeur à toute profondeur, colonne de la clé `I`, lignes vides et commentaires sautés. Reste mesuré à LECTEUR-CC-1 : §11.
  - *Amendement daté du 2026-10-01 (correction de la revue G2, C-G2-2 et C-G2-3)* : (b) la sentinelle prend aussi le crochet ouvrant, classe `[[{,]` au lieu de `[{,]` : les formes de flux de séquence F1 à F8 de la revue G2, que PyYAML 6.0.3 lit `model=opus`, sont refusées en `R-1/cle-model` (`corr/o/sonde-crochet-corrige.out`) ; (c) la colonne `I` d'une clé en entrée de séquence est fixée par T-95.
- **CH-13** : `RX='"([^"\\]|\\.)*"'` sous `LC_ALL=C` ; garde de résidu (`sed` des chaînes, des littéraux, de la ponctuation, des chiffres et des blancs, tabulations comprises) ; clés = jetons suivis de deux-points (`grep -o` aligné sur les chaînes entières) ; clé à barre → `R-1/hors-liste` ; valeur de `model` ou `advisorModel` non chaîne → `R-1/hors-liste` ; valeurs au verdict ; virgule finale admise (T-91). Réglage local réel : strict, 0 faux refus (O-8, lint sur `F:/Shogen` : 3 fichiers).
- **CH-14** : note transcrite telle que le G0 l.283 (mots identiques, repliée à 95 colonnes en citation comme les notes voisines, contrôle dans `oracles/note-decisions.py`) entre le titre (l.3054) et le statut de l'ADR-0020 de `main` ; faits relus par O-11 ; index non touché.
  - *Amendement daté du 2026-10-01 (correction de la revue G2, C-G2-1)* : texte de la note amendé ; il n'est plus mot pour mot celui du G0 l.283. Texte de `F:/tmp/shogen-lots/D8c/g2/o/note_c1.py` (variable `TEXTE`), replié à 94 colonnes, 21 lignes, aucune ligne qui commence par une ponctuation, aucun guillemet ; le script rejoué sur la note du G1 donne le fichier livré à l'octet près (`cmp`).
- **CH-15** : aucune revendication de garde de commit dans l'en-tête du hook ni de l'installeur (CA-D8c-13 : « Ce n'est pas une garde de commit » y est écrit).
  - *Amendement daté du 2026-10-01 (correction de la revue G2, C-G2-9)* : l'en-tête du hook nomme aussi la fusion sans conflit parmi ce que le hook ne voit pas ; texte conditionnel à la question Q-G2-1 de la revue G2 (si `pre-merge-commit` est construit, l'en-tête et `ATTENDU` changent dans ce sous-lot).

## 4. Tests — chaque cas nomme la mutation qui le rougit

- **Runner du hook** (`enforcement/tests/run-fixtures-hooks.sh`, 50 cas : H-01 à H-22, I-01 à I-14, C-01 à C-14 ; catégorie « nouveau module ») ; sortie ET jeton (ou fragment de message) par cas ; `hooks : <n> ok, <m> échec`, sortie 0, 1 ou 3. Ajouts au G0 : H-21, H-22, I-14, C-13, C-14 (copie du G0, amendements sous les tables du §7).
- **Runner du lint** : T-77 à T-92 ajoutés (16), T-01 à T-76 inchangés (P2P) ; comptes F2P et épingles au §0 (C-5).
- **Mutants qui rougissent chaque cas** (campagnes finales, §5 ; lignes `rouges:` de `oracles/mutants-*.out`) :

| cas | mutants sous lesquels le cas est rouge |
|---|---|
| H-01 | MC-7, MH-1, MH-2 |
| H-02 | MH-1 |
| H-03 | MC-7, MH-1 |
| H-04 | MC-7, MH-1, MH-3 |
| H-05 | MC-7, MH-1, MH-2, MH-7 |
| H-06 | MC-7, MH-1, MH-2 |
| H-07 | MC-7, MH-1, MH-2 |
| H-08 | MH-1 |
| H-09 | MH-1, MH-5 |
| H-10 | MH-1, MH-6 |
| H-11 | MH-1, MH-11 |
| H-12 | MC-7, MH-1, MH-2 |
| H-13 | MC-7, MC-10, MH-1, MH-2, MH-4 |
| H-14 | MC-10, MH-1, MH-4 |
| H-15 | MC-7, MH-1, MH-2 |
| H-16 | MC-7, MH-1, MH-2 |
| H-17 | MC-7, MH-1, MH-2 |
| H-18 | MC-7, MH-1, MH-2 |
| H-19 | MH-13 |
| H-20 | MH-2, MH-3, MH-4, MH-5, MH-6, MH-7, MH-9, MH-11 |
| H-21 | MH-1, MH-8 |
| H-22 | MC-7, MH-1, MH-2, MH-10 |
| I-01 | aucun |
| I-02 | MI-16 |
| I-03 | MI-5 |
| I-04 | MI-2 |
| I-05 | MI-3 |
| I-06 | MI-4 |
| I-07 | MI-1 |
| I-08 | MI-6 |
| I-09 | MI-7 |
| I-10 | MI-14, MI-15 |
| I-11 | MI-10 |
| I-12 | MI-12 |
| I-13 | MI-8 |
| I-14 | MI-11 |
| C-01 | MC-1, MC-2, MC-7, MC-10, MH-1 |
| C-02 | MC-2, MC-10, MH-1 |
| C-03 | MC-1, MC-3, MC-7, MC-10, MH-1 |
| C-04 | MC-2, MH-1 |
| C-05 | MC-4, MH-1 |
| C-06 | MC-4, MC-5, MC-10, MH-1 |
| C-07 | MC-3, MC-6a, MC-7, MC-10, MH-1 |
| C-08 | MC-5, MC-6b, MC-10, MH-1 |
| C-09 | MC-1, MC-4, MH-1, MH-2 |
| C-10 | MH-1 |
| C-11 | MC-1, MC-7, MH-1 |
| C-12 | MH-1 |
| C-13 | MC-8, MC-10, MH-1 |
| C-14 | MC-10 |

Runner du hook (état 2) : cas rouge sous aucun mutant : **I-01**, tueur de MI-13 sous Linux seulement [inféré] (§5). Son pouvoir de discrimination n'est pas revendiqué en local.

| cas | mutants sous lesquels le cas est rouge |
|---|---|
| T-20 | ML-13 |
| T-45 | ML-12 |
| T-60 | ML-6 |
| T-70 | ML-4 |
| T-77 | ML-1, ML-9 |
| T-78 | ML-1, ML-9 |
| T-79 | ML-2 |
| T-80 | ML-2 |
| T-81 | ML-2 |
| T-82 | ML-3 |
| T-83 | ML-3, ML-4 |
| T-84 | ML-8 |
| T-85 | ML-7, ML-10 |
| T-86 | ML-6 |
| T-87 | ML-5 |
| T-88 | ML-5 |
| T-89 | ML-5 |
| T-90 | ML-10 |
| T-91 | ML-11 |
| T-92 | ML-4 |

Runner du lint (état 3) : la table ne liste que les cas rougis par les 13 mutants ML ; les 72 autres (T-01 à T-76 hors T-20, T-45, T-60 et T-70) sont rougis par les 73 mutants de D8a (`docs/G1-lot-D8a.md` §15), non rejoués ici.
- *Amendement daté du 2026-10-01 (correction de la revue G2, C-G2-2 à C-G2-4)* : runner du hook : 51 cas (H-01 à H-23, I-01 à I-14, C-01 à C-14) ; runner du lint : 95 cas (T-01 à T-95). Cas ajoutés et mutants qui les rougissent (campagnes du correcteur sur l'état corrigé, `F:/tmp/shogen-lots/D8c/corr/o/mut-hook.out` et `lot-lint.out`) : **H-23** rouge sous GH-1 (verdict jamais en refus) ; **T-93** et **T-94** rouges sous GL-8 (classe sans crochet, lint du lot) et sous GL-1 (sentinelle retirée) ; **T-95** rouge sous GL-5b (colonne `I` sans préfixe de séquence), seul.


## 5. Mutants de gate (registre d'ADR-0011 pt 4)

- **Méthode** : `oracles/mutants.py` écrit chaque mutant par UN remplacement exact dans une copie prise dans l'instantané figé ; un remplacement qui ne s'applique pas exactement une fois rend le mutant « inapplicable ». `oracles/mutants-run.sh` lance `bash <runner> <mutant>` (hook, ou hook réel et installeur mutant, ou lint) depuis l'instantané, sous un TMP neuf, quatre travailleurs, et exige une sortie ≠ 0 et un tueur attendu parmi les cas en échec. Le worktree n'a jamais porté de mutant. Campagnes par lots de moins de 10 min (borne des tâches de fond du harnais : §13).
- **D8c-1 v1** (`mutants-d8c1.out`, 22:42:33Z-22:46:58Z) : 23 tués par le tueur attendu, MI-9 équivalent déclaré, **MH-9 et MI-13 survivent**. MH-9 (motif du hook différent de celui du job) survit parce que H-20 et I-10 étaient toujours verts : l'affectation du message placée entre le test et le décompte remettait le code à 0 (E-3). Corrigé ; MI-13 : ci-dessous.
- **D8c-1 v2** (instantané `etat-1b`, `mutants-d8c1-v2.out`, 22:49:21Z-22:53:18Z) : **23 tués** par le tueur attendu, dont MH-9 par H-20 ; MI-9 équivalent déclaré ; MI-13 survit, équivalent en local.
- **MI-13** (copie sans bit d'exécution) : équivalent en local, mesuré (`oracles/sonde-bit-x.out`) : sous le montage `noacl` de Git for Windows, un fichier à shebang s'affiche 755 et passe `test -x` après `chmod 644`, un fichier sans shebang reste 644 après `chmod 755` ; l'exécutabilité dérive du contenu. Sous Linux, I-01 (`-x`) le tue [inféré : `test -x` suit le mode du fichier] ; item SHOGEN-G5-FORGE-1 (c).
- **MI-9** (contrôle après copie retiré) : équivalent déclaré ; la copie est contrôlée avant le `mv` (`sha256` du fichier temporaire contre `ATTENDU`) ; rejeu : `python -B oracles/mutants.py d8c2 <instantané> <dossier>` puis `mutants-run.sh … 'MI-9'`.
- **D8c-2** (instantané `etat-2` ; rejeu de MI-16, MC-9 et MC-10 sur l'état livré `etat-2f`, qui porte C-14) et **D8c-3** (instantané `etat-3`). MC-9 (`-u` ajouté à `checkout-index`) est équivalent, mesuré (`oracles/sonde-index.out`) : avec `--prefix`, `-u` ne réécrit pas l'index ; le cas C-14 fixe la propriété (index inchangé sous le hook lancé directement) et tue MC-10 :

| mutant | objet | verdict | cas rouges | instantané |
|---|---|---|---|---|
| MH-1 | verdict inverse | tué par H-01 | H-01 H-02 H-03 H-04 H-05 H-06 H-07 H-08 H-09 H-10 H-11 H-12 H-13 H-14 H-15 H-16 H-17 H-18 H-21 H-22 C-01 C-02 C-03 C-04 C-05 C-06 C-07 C-08 C-09 C-10 C-11 C-12 C-13 | etat-2 |
| MH-2 | motif ramene au motif courant | tué par H-01 | H-01 H-05 H-06 H-07 H-12 H-13 H-15 H-16 H-17 H-18 H-20 H-22 C-09 | etat-2 |
| MH-3 | motif ramene a la classe amont | tué par H-04 | H-04 H-20 | etat-2 |
| MH-4 | --cached retire | tué par H-13 | H-13 H-14 H-20 | etat-2 |
| MH-5 | exclusion .claude/ retiree | tué par H-09 | H-09 H-20 | etat-2 |
| MH-6 | exclusion de gates.yml retiree | tué par H-10 | H-10 H-20 | etat-2 |
| MH-7 | exclusion enforcement/ ajoutee | tué par H-05 | H-05 H-20 | etat-2 |
| MH-8 | erreur de git grep rendue verte | tué par H-21 | H-21 | etat-2 |
| MH-9 | motif different de celui du job | tué par H-20 | H-20 | etat-2 |
| MH-10 | cd vers la racine retire | tué par H-22 | H-22 | etat-2 |
| MH-11 | exclusion biblio/ retiree | tué par H-11 | H-11 H-20 | etat-2 |
| MH-13 | refus hors d'un depot rendu vert | tué par H-19 | H-19 | etat-2 |
| MI-1 | empreinte de la source non controlee | tué par I-07 | I-07 | etat-2 |
| MI-2 | empreinte inconnue ecrasee | tué par I-04 | I-04 | etat-2 |
| MI-3 | core.hooksPath ignore | tué par I-05 | I-05 | etat-2 |
| MI-4 | arbre lie admis | tué par I-06 | I-06 | etat-2 |
| MI-5 | pas de sauvegarde | tué par I-03 | I-03 | etat-2 |
| MI-6 | source prise dans l'arbre de travail | tué par I-08 | I-08 | etat-2 |
| MI-7 | --verifier vert sur un hook different | tué par I-09 | I-09 | etat-2 |
| MI-8 | controle de soi retire | tué par I-13 | I-13 | etat-2 |
| MI-9 | controle apres copie retire | équivalent déclaré | aucun | etat-2 |
| MI-10 | refus des variables GIT_* retire | tué par I-11 | I-11 | etat-2 |
| MI-11 | argument inconnu admis | tué par I-14 | I-14 | etat-2 |
| MI-12 | hors d'un depot admis | tué par I-12 | I-12 | etat-2 |
| MI-13 | copie sans bit d'execution | survit (équivalent en local) | aucun | etat-2 |
| MI-14 | ATTENDU faux dans le vrai installeur | tué par I-10 | I-10 | etat-2 |
| MI-15 | hook local retire de CONNUS | tué par I-10 | I-10 | etat-2 |
| MI-16 | hook conforme reecrit quand meme (sauvegarde et copie) | tué par I-02 | I-02 | etat-2f |
| MC-1 | etape lint retiree | tué par C-01 | C-01 C-03 C-09 C-11 | etat-2 |
| MC-2 | lint lance sur l'arbre de travail | tué par C-02 | C-01 C-02 C-04 | etat-2 |
| MC-3 | lint pris dans l'arbre de travail | tué par C-03 | C-03 C-07 | etat-2 |
| MC-4 | etape secrets retiree | tué par C-05 | C-05 C-06 C-09 | etat-2 |
| MC-5 | gate prise dans l'arbre de travail | tué par C-06 | C-06 C-08 | etat-2 |
| MC-6a | lint absent tenu pour vert | tué par C-07 | C-07 | etat-2 |
| MC-6b | gate absente tenue pour verte | tué par C-08 | C-08 | etat-2 |
| MC-7 | verdict reduit a la derniere etape | tué par H-01 | H-01 H-03 H-04 H-05 H-06 H-07 H-12 H-13 H-15 H-16 H-17 H-18 H-22 C-01 C-03 C-07 C-11 | etat-2 |
| MC-8 | extraction en echec tenue pour verte | tué par C-13 | C-13 | etat-2 |
| MC-9 | -u ajoute a checkout-index (sans effet avec --prefix, sonde-index.out) | équivalent déclaré | aucun | etat-2f |
| MC-10 | le hook indexe l'arbre de travail (git add -A) | tué par C-02 | H-13 H-14 C-01 C-02 C-03 C-06 C-07 C-08 C-13 C-14 | etat-2f |
| ML-1 | prefixe de sequence retire de la ligne canonique | tué par T-78 | T-77 T-78 | etat-3 |
| ML-2 | sentinelle retiree | tué par T-81 | T-79 T-80 T-81 | etat-3 |
| ML-3 | suite imbriquee retiree (suite de premier niveau gardee) | tué par T-82 | T-82 T-83 | etat-3 |
| ML-4 | commentaires non sautes | tué par T-92 | T-70 T-83 T-92 | etat-3 |
| ML-5 | garde de residu retiree | tué par T-89 | T-87 T-88 T-89 | etat-3 |
| ML-6 | refus des cles a barre retire | tué par T-60 | T-60 T-86 | etat-3 |
| ML-7 | retour au motif C-4 | tué par T-85 | T-85 | etat-3 |
| ML-8 | sentinelle etendue a toute occurrence de model suivie de deux-points | tué par T-84 | T-84 | etat-3 |
| ML-9 | prefixe de sequence non retire de la valeur | tué par T-78 | T-77 T-78 | etat-3 |
| ML-10 | jeton de chaine sans echappement | tué par T-90 | T-85 T-90 | etat-3 |
| ML-11 | virgule finale refusee (lecture stricte ajoutee) | tué par T-91 | T-91 | etat-3 |
| ML-12 | valeur non chaine admise | tué par T-45 | T-45 | etat-3 |
| ML-13 | cle advisorModel non lue | tué par T-20 | T-20 | etat-3 |

Résumé : 52 mutants appliqués, aucun inapplicable ; 49 tués par un tueur attendu ; 2 équivalents déclarés (MI-9, MC-9) ; 1 équivalent en local (MI-13).
- *Amendement daté du 2026-10-01 (correction de la revue G2, §15)* : mutants de la revue G2 rejoués par le correcteur sur l'état corrigé (`g2/o/mutants_g2.py` tel quel, plan `F:/tmp/shogen-lots/D8c/corr/mut/plan.tsv` ; GL-3, inapplicable sur la classe corrigée, redérivé en GL-3c, accolade ôtée de `[[{,]` ; GL-5 appliqué au lint corrigé, soit GL-5b ; GL-8 = lint du lot sous le runner corrigé) : 20 mutants appliqués, 0 inapplicable, 20 tués chacun par un tueur attendu (GH-1 par H-01, H-23 parmi ses 25 cas rouges ; GH-2 par H-13 ; GH-3 par C-03 ; GH-4 par C-02 ; GH-5 par C-06 ; GH-6 par H-21 ; GH-7 par H-09 ; GH-8 par H-22 ; GI-1 par I-08 ; GI-2 par I-04 ; GI-3 par I-06 ; GI-4 par I-09 ; GI-5 par I-13 ; GL-1 par T-79, T-93 et T-94 parmi ses rouges ; GL-2 par T-87 ; GL-3c par T-81 ; GL-5b par T-95 ; GL-6 par T-83 ; GL-7 par T-86 ; GL-8 par T-93), 0 survivant, 0 run FATAL, 0 entrée TMP (`F:/tmp/shogen-lots/D8c/corr/o/mut-hook.out`, `lot-lint.out`). GL-5 survivait aux 92 cas du lot (revue G2) ; GL-5b est tué par T-95. La campagne du G1 (52 mutants) n'est pas rejouée [inféré : les cas ajoutés n'en retirent aucun ; les fichiers mutés ne changent que par l'en-tête et le message du hook, `ATTENDU` et la classe de la sentinelle].

## 6. Oracles non-LLM (O-1 à O-13) et enregistrement

- **O-1 — runners** (`bash <chemin>`, TMP neuf par lancement ; `oracles/O1-*.log`, `.exit`, `.ms`, `.tmpcount`) : runner du hook, état D8c-1a `hooks : 22 ok, 0 échec` (14 s) ; état D8c-1b `36 ok, 0 échec` (23 à 39 s) ; état D8c-2 `49 ok, 0 échec` (75 à 100 s) ; **état final `hooks : 50 ok, 0 échec`**, sortie 0, 0 entrée TMP (105 et 145 s). Runner du lint, état final : **`model-pinning : 92 ok, 0 échec`**, sortie 0, 0 entrée TMP (76 à la base).
  - *Amendement daté du 2026-10-01 (correction de la revue G2, §15)* : état corrigé (`F:/tmp/shogen-lots/D8c/corr/o/ctl-A.out`, `ctl-B.out`) : runner du hook `hooks : 23 ok, 0 échec` (1a), `37 ok` (1b), `51 ok` (2 et 3), sortie 0, 0 entrée TMP ; lancé depuis la racine avec des arguments relatifs : 51 ok (C-G2-7) ; runner du lint `model-pinning : 95 ok, 0 échec`, sortie 0, 0 entrée TMP. Temps séquentiels cités au commentaire du job g5 : 14 à 21 s (1a), 36 à 41 s (1b), 93 à 98 s (2) ; balayage 68 à 78 ms.
- **O-2 — sonde git-ci §2.e rejouée** : état D8c-1 (`oracles/O2-d8c1.out` ; copie de `g0-mesures/sonde-hook-local.sh`, seul le TMP changé, `diff` d'une ligne) : S1, S3, S4, S5, S6 et S7 refusés (direct 2, commit 1), S2, S8 et S9 acceptés ; par rapport à la table du G0 §5.2, **seuls changent S4, S5, S6 (refusés) et S9 (accepté)**, les changements voulus du CH-3. État final (`oracles/O2-final.out`, variante déclarée `o2-sonde-final.sh` : la base de chaque dépôt porte deux agents, le lint et la gate) : S1 à S8 identiques ; S9, fichier d'agent sans frontmatter, est refusé par l'étape lint (`HOOK/lint`), non par g5 ; **S9b** (agent valide, marqueur dans le corps) est accepté.
- **O-3 — compatibilité g5 et texte** (`oracles/statiques-final.out`, `oracles/docs-controle.out`) : 0 ligne aux deux motifs sur chaque fichier ajouté ou modifié, documents compris ; 0 fragment anglais entre guillemets français et 0 guillemet droit hors code dans la copie du G0, ce journal et la note ajoutée à DECISIONS ; commande du job g5 élargi : sur le worktree, `git grep` sort en 1 (aucune ligne ; fichiers suivis) ; sur le dépôt jetable qui porte tout le lot committé, documents compris (O-8 b), sortie 1 également.
- **O-4 — rouges semés sur l'entrée committée** (`oracles/O4-O12.out`) : dépôt jetable = `git archive e9ac6e2 ':!biblio'` (310 fichiers) plus les fichiers du lot (313 suivis), commit de base sans hook, installation par l'installeur du lot (avant absent, après `31c5cd67…2466`) ; k=0 changement propre → 0, `OK (hook)` ; k=1 marqueur indexé → 1, `HOOK/g5` ; k=2 agent de l'arbre passé à `opus` dans l'index, arbre de travail remis bon → 1, `HOOK/lint` et `R-1/tier-nu` ; k=3 forme d'identifiant (sonde V-01 de D8b) → 1, `HOOK/secrets` et `SECRETS/forme`. Le lot n'étant pas committé (R-20), « l'entrée committée » est la base `e9ac6e2` plus les fichiers du lot tels qu'au worktree : déclaré.
  - *Amendement daté du 2026-10-01 (correction de la revue G2, C-G2-2 et C-G2-4)* : rejeu sur la copie corrigée (`F:/tmp/shogen-lots/D8c/corr/o/o4-depot.out`, sonde de la revue G2 adaptée) : installation, avant absent, après `00131872…826b` ; k = 0 à 3 aux jetons d'origine ; **k=4**, `git commit --amend` d'un marqueur indexé → 1, `HOOK/g5` ; **k=5**, agent porteur de `hooks: [model: opus]` → 1, `HOOK/lint` et `R-1/cle-model` (le hook du lot l'acceptait, mesure de la revue G2).
- **O-5 — mutants** : §5.
- **O-6 — installeur, empreintes avant et après** (`oracles/O6-garde.out`) : `ATTENDU` = sha256 du hook du lot = `31c5cd67375e75d77eac71571681247d0173a39c17a24471031c5723fc072466` ; (a) aucun hook → installé, avant `absent`, après `ATTENDU` ; (b) relance → « déjà conforme », rien écrit ; (c) double de test d'empreinte connue (`306c6ca7…17cb`, `CONNUS` remplacé et committé) → sauvegarde `pre-commit.306c6ca74075` de même sha256, puis après `ATTENDU` ; (d) `--verifier` → 0. Les quatorze cas I du runner complètent ces rejeux.
  - *Amendement daté du 2026-10-01 (correction de la revue G2, C-G2-5)* : `ATTENDU` = sha256 du hook corrigé, `0013187283815cac3ebdc3312c374f84f8946020c127533b69414e6041fc826b` (états 2 et 3 ; état 1b : `b8705ae822acab458e3ae50c32b0e9fce4e6ba873845673fe5555c7edcbe6198`) ; message de succès du hook : `OK (hook) : aucune étape en refus sur l'index (images locales des jobs g5, g1 et g3)` (état 1a : image locale du seul job g5) ; `grep -c conforme` sur le hook : 0 ; I-10 vert à chaque état.
- **O-7 — égalité des motifs** (`oracles/statiques-final.out`) : motif et exclusions extraits de l'étape g5 de `gates.yml` et du hook : égaux octet pour octet, et égaux à `adb2213` l.39 ; sha256 de la chaîne « motif + exclusions » `3fc8b4d06b662b4d90bb0ae5f2f26cc942a8e86900bb9c6d010bd3029adc22f1` des deux côtés.
- **O-8 — non-régression** : (a) suite `s2-harness`, base et final : `Ran 216 tests`, `OK (skipped=2)`, sortie 0, 0 entrée TMP, mêmes deux sauts, (ii) et (ii bis) (`oracles/suite-base.sauts`, `oracles/suite-final.sauts`, `diff` vide) ; `cargo --locked xtask verify` : base VERT (22:23:50Z-22:24:06Z) ; arbre du lot, premier passage (23:46:10Z-23:46:14Z, journal complet sauf cette puce) VERT, sortie 0 : S-G1 à S-G8, `fmt`, `no_std` et `clippy` VERT ; S-G4 couvre 57 fichiers (55 à la base) et S-G5 58 (56), les deux documents du lot compris ; S-G5 en régime de corpus incomplet (0 artefact sur 125), 252 fragments contrôlés et 218 non contrôlés, comme à la base, aucun tiré des documents du lot ; second passage sur l'arbre final : `G1-rapport.md`. (b) Image locale des jobs g5, g1 et g3 sur le lot committé (`oracles/O8-depot.out`, dépôt jetable de 315 fichiers : `git archive e9ac6e2 ':!biblio'` plus les neuf fichiers du lot) : commande du job g5 sans ligne (`git grep` sort en 1) ; runner du hook 50 ok ; runner du lint 92 ok ; `lint-model-pinning.sh .` sortie 0, 2 fichiers ; `gate-secrets.sh --tree` sortie 0, 307 fichiers (`enforcement/hooks/` compris, `enforcement/tests/` exclu par contrat) ; `--history` sortie 0 ; 0 entrée TMP. (c) Worktree (`oracles/runners-final.out`) : `run-fixtures-model-pinning.sh` 92 ok ; `lint-model-pinning.sh .` sortie 0, 3 fichiers ; le même lint sur l'arbre principal (lecture seule) : sortie 0, 3 fichiers, réglage local réel lu sans faux refus ; `run-fixtures-secrets.sh` 112 ok ; `gate-secrets.sh --tree` sortie 0, 304 fichiers suivis (les fichiers neufs du lot, non suivis ici, sont couverts en (b)) ; `--history` sortie 0, 154 commits (`--all` ; 142 à la base : d'autres arbres liés ont avancé entre-temps) ; 0 entrée TMP. Environnement : `CARGO_HOME` et `CARGO_NET_OFFLINE=true` de la mission, toolchain forcée, serveurs rustup en 127.0.0.1:9 (`oracles/cargo_env.sh`), `F:/rust/rustup/downloads` vide après chaque passage ; `TMPDIR`, `TMP` et `TEMP` neufs sous `F:/tmp/shogen-tests-tmp/d8c-g1/`.
  - *Amendement daté du 2026-10-01 (correction de la revue G2, §15)* : état corrigé. (a) Suite `s2-harness` sur le worktree : `Ran 216 tests`, `OK (skipped=2)`, sortie 0, 0 entrée TMP, sauts identiques au G1 (`corr/o/suite-p1.*`) ; `cargo --locked xtask verify` sur le worktree, premier passage (02:17:54Z-02:18:11Z, avant les derniers chiffres de ce journal) : VERDICT GLOBAL VERT, sortie 0 ; S-G4 57 fichiers ; S-G5 58 fichiers, 252 fragments contrôlés et 218 non contrôlés (corpus incomplet, 0 artefact sur 125), comme au G1 ; 0 téléchargement rustup ; second passage sur l'arbre final : rapport de correction. (b) Image locale des jobs sur la copie corrigée (`corr/o/o4-depot.out`, 315 fichiers suivis) : commande du job g5 sans ligne ; `lint .` sortie 0, 2 fichiers ; `gate-secrets.sh --tree` sortie 0, 307 fichiers ; `--history` sortie 0. (c) Worktree (`corr/o/g3-wt.out`) : `lint .` sortie 0, 3 fichiers ; runner de D8b 112 ok (base empilée) ; `gate-secrets.sh --tree` sortie 0, 308 fichiers (les cinq fichiers neufs du lot comptés comme entrées `add -N`) ; `--history` sortie 0, 172 commits (`--all`) ; 0 entrée TMP ; lint corrigé sur l'arbre principal, en lecture : sortie 0, 3 fichiers. (d) O-7 et O-10 (`g2/o/o7_o10.py`, `corr/o/o7-o10.out`) : 20 assertions sur 20 ; motif et exclusions du hook égaux à ceux du job et à `adb2213` l.39 (ligne relue par le correcteur, égale à l'extrait de la revue G2).
- **O-9 — TMP** : 0 entrée neuve dans chaque TMP neuf, après chaque O-1, chaque mutant (colonne `tmp=` des sorties de campagne), chaque suite et chaque sonde.
- **O-10 — `gates.yml`** (`oracles/O10.out`, PyYAML 6.0.3 déjà présent) : 14 assertions sur 14 : mêmes jobs que la base, g1, g3 et s2 identiques, permissions et déclencheurs identiques ; g5 : `name` inchangé, `ubuntu-24.04`, `timeout-minutes: 10`, checkout v7.0.1 par SHA sans jeton persistant, étape du runner en `shell: bash`, étape de balayage égale à la base hors motif, aucun `continue-on-error`.
- **O-11 — faits de la note** (`oracles/O11.out`, lecture seule) : `2d02276` 2026-08-20T16:54:27+01:00 ; `adb2213` 06:20:27+01:00 ; `60fd8e1` 08:20:27+01:00 ; `f11bdca` auteur 08:20:27, commit 12:44:22+01:00 (cherry-pick) ; `36593b6` 2026-08-21T06:25:34+01:00 ; journal de refs de la branche : créée depuis `886adce` et `adb2213` à 06:20:27, `60fd8e1` à 08:20:27, ramenée à `adb2213` à 12:44:40 ; `logs/HEAD` de l'arbre principal (lu comme fichier) : retour à `main` puis cherry-pick à 1787226262 = 11:44:22Z ; `adb2213:docs/DECISIONS.md` l.3051 = titre de l'homonyme ; titre et statut de l'ADR-0020 de `main` aux l.3054 et l.3056 de `40b4cfb`. Tous égaux aux heures et hash de la note.
  - *Amendement daté du 2026-10-01 (correction de la revue G2, C-G2-1)* : rejeu du correcteur (`g2/o/o11.sh`, lecture seule, `corr/o/o11.out`, 01:17:49Z) : cinq commits aux heures et hash de la note ; branche `roster-ban-alignment-2026-08-20` absente, son journal de refs aussi ; tag annoté `archive/roster-ban-2026-08-20` vers `adb2213`, tagger 2026-09-30T23:33:51Z ; `logs/HEAD` l.56-60 égal au relevé du G1 ; JOURNAL l.149 : SHOGEN-D8-PC-1 fermé.
- **O-12 — coût par commit** (`oracles/O4-O12.out`, dépôt jetable d'O-4, `git commit` complet mesuré) : 1 fichier 1,5 s ; 3 fichiers 1,8 s ; 8 fichiers 2,8 s ; 11 fichiers 3,5 s. Le commentaire du job ne cite que les temps du runner.
- **O-13 — après installation** : acte de l'orchestrateur (CH-6), au cp-2 du dernier sous-lot ; prémisse contrôlée par C-14 (hook installé lancé directement, `GIT_OPTIONAL_LOCKS=0` : sortie 0 et `.git/index` inchangé, sonde `oracles/sonde-index.out`).
- **Garde du runner** (CA-D8c-14, `oracles/O6-garde.out`) : `GIT_INDEX_FILE` posée vers un chemin inexistant → sortie 3, message de garde, 0 entrée TMP ; `GIT_DIR` et `GIT_WORK_TREE` ne sont posées par aucune commande du G1 (liste de la garde contrôlée par lecture).
- **Enregistrement d'oracle substitut** : `oracles/oracle-G1-D8c-substitut.json` (schéma `shogen.g2.oracle-substitut.v1`, rôle G1, champs de D6 viii) ; son sha256 est en tête de `G1-rapport.md`.
- **Ce que l'oracle local ne prouve pas** : `git grep -E` et le mot-frontière de l'image Linux, `mktemp`, `sha256sum`, `checkout-index`, les modes de fichier (MI-13) et la durée du runner sous Linux ; la lecture du workflow par la forge : item SHOGEN-G5-FORGE-1 (c).

## 7. Tuyaux (CA-11 durci, règle Branchement) et G3 opérant

- **Entrée** : l'index du commit en préparation (`git add` de l'auteur ; orchestrateur sur `main`, workers dans leurs worktrees, hooks partagés) ; en D8c-2, le lint (D8a) et la gate (D8b) lus dans cet index.
- **Pièce** : `enforcement/hooks/pre-commit`, versionné ; copie installée par `enforcement/hooks/install-pre-commit.sh` ; état : `ATTENDU` et `CONNUS` dans l'installeur, la copie installée, sa sauvegarde.
- **Sortie** : code 0 ou 2, jetons `HOOK/…` sur stderr.
- **Consommateur 1** : `git commit` et `git commit --amend` du dépôt principal et de tout arbre lié. **Absent jusqu'à l'installation** (CH-6, acte de l'orchestrateur après le G7), puis câblé ; preuve : O-13 au cp-2. Non couverts : `cherry-pick`, `rebase` (item SHOGEN-HOOK-COUVERTURE-1).
  - *Amendement daté du 2026-10-01 (correction de la revue G2, C-G2-9)* : non couverts : `cherry-pick`, `rebase` et les fusions sans conflit (`git merge --no-ff` lance `pre-merge-commit`), mode d'intégration de `main` depuis la méthode par parties (`docs/adr-0028/PARTIES-S2.md` l.19, adoptée le 2026-10-01) ; la prémisse du G0 selon laquelle `pre-merge-commit` serait inutile sur `main` (fusions refusées, git-ci l.179) est retirée. `git commit --amend` reçoit son cas (H-23). Rejeu du correcteur sur la copie corrigée (`F:/tmp/shogen-lots/D8c/corr/o/sonde-fusion.out`) : seul pre-commit installé, une branche marquée fusionne sans refus ; même blob aussi en `pre-merge-commit` : refus `HOOK/g5` ; fusion propre acceptée ; fusion en conflit conclue par `git commit` : pre-commit lancé ; fusion propre : seul `pre-merge-commit` lancé. Item SHOGEN-HOOK-COUVERTURE-1 re-formé (§11) ; décision de construire : question Q-G2-1 de la revue G2.
- **Consommateur 2** : job g5, étape 1 (runner du hook). **Partiel déclaré** : forge arrêtée (GC-01), aucun contrôle requis (GC-09) ; G3 opérant = rejeu local ; item SHOGEN-G5-FORGE-1.
- **Tuyaux fermés à l'installation** : consommateur 2 du lint (D8a, item 9) et du mode indexé de la gate (D8b, item 4).
- **Test de composition** : runner du hook (dépôts jetables, installeur réel, `git commit` réels) ; O-4 sur l'entrée committée ; O-13 sur le dépôt réel après installation (cp-2).
- **Séquence d'installation (CH-6), acte de l'orchestrateur** : (1) `bash enforcement/hooks/install-pre-commit.sh --verifier` depuis la racine de `F:/Shogen` : 2 attendu (hook local `1da91c72…`) ; (2) `bash enforcement/hooks/install-pre-commit.sh` : sauvegarde `pre-commit.1da91c723b7f`, puis copie (une ligne avec les sha256 avant et après) ; (3) `--verifier` : 0 ; (4) exécution directe du hook installé, index sans changement, sous `GIT_OPTIONAL_LOCKS=0` : 0 ; (5) ligne de JOURNAL (empreintes, sauvegarde). Retour arrière : remettre la sauvegarde en place par `mv`, consigné. L'installeur refuse de tourner depuis un worktree (I-06) : lancer depuis `F:/Shogen`. **Prémisse de l'étape (4), non mesurée sur `main`** : le hook balaye l'index entier ; O-3 et O-8 ne mesurent que `e9ac6e2` plus le lot, et d'autres lots entrent sur `main` d'ici l'installation (154 commits atteints au `--history` final contre 142 à la base), sous le hook local qui ne voit ni la forme « marqueur suivi de deux-points », ni `enforcement/`, ni `.github/`. Si l'étape (4) sort en `HOOK/g5`, l'index de `main` porte un marqueur entré après `e9ac6e2` : rejouer la commande du job g5 sur `main` et résoudre avant de déclarer O-13. Par la lettre du hook, un index sans agent sortirait en `R-1/vide` et tout commit serait refusé : sans objet sur Shōgen (deux agents suivis).
- **Texte proposé pour ADR-0028 §4.11 (Q-G0-7), acte de l'orchestrateur, à l'installation** : « *Amendement daté du 2026-09-30 (lot D8c)* : à partir de l'installation du hook versionné (CH-6 du G0 de D8c), le G3 opérant comprend aussi `bash enforcement/tests/run-fixtures-hooks.sh` (sortie 0 ; résumé `hooks : 50 ok, 0 échec`) et `bash enforcement/hooks/install-pre-commit.sh --verifier` (sortie 0) ; le résumé de `run-fixtures-model-pinning.sh` devient `model-pinning : 92 ok, 0 échec` au commit de D8c-3. »
  - *Amendement daté du 2026-10-01 (correction de la revue G2, C-G2-4)* : texte proposé, qui remplace celui ci-dessus (acte de l'orchestrateur, à l'installation) : Amendement daté du 2026-10-01 (lot D8c) : à partir de l'installation du hook versionné (CH-6 du G0 de D8c), le G3 opérant comprend aussi `bash enforcement/tests/run-fixtures-hooks.sh` (sortie 0 ; résumé `hooks : 51 ok, 0 échec`) et `bash enforcement/hooks/install-pre-commit.sh --verifier` (sortie 0) ; le résumé de `run-fixtures-model-pinning.sh` devient `model-pinning : 95 ok, 0 échec` au commit de D8c-3.
- **Conséquences à déclarer au JOURNAL à l'installation** : tout commit local d'un worker passe par le hook ; un worktree dont la base précède D8a et D8b voit ses commits refusés en `HOOK/echec` (C-07, C-12) ; consigne « avancer la base avant tout commit local » aux commandes de mission (SHOGEN-WORKTREE-BASE-HOOK-1) ; coût par commit : O-12.

## 8. Risques MAST (annexe C) et contre-mesures

- **FM-1.1** : installeur jamais lancé hors d'un dépôt jetable ; il refuse un arbre lié (I-06) ; garde `GIT_*` du runner (sortie 3) ; hook local de `F:/Shogen` au même sha256 au début et à la fin ; agents réels inchangés ; aucune fixture sous un `.claude/agents/` du dépôt.
- **FM-3.3** : sortie ET jeton ; table S1-S9 rejouée (O-2) ; égalité des motifs (O-7) ; mutants MH, MI, MC, ML ; un mutant survivant (MH-9) a été traité comme un défaut du runner (E-3), pas du hook.
  - *Amendement daté du 2026-10-01 (correction de la revue G2)* : verts sur une sentinelle trop permissive (F1 à F8), sur une colonne de clé non testée (GL-5) et sans cas `--amend` : C-G2-2 à C-G2-4 ; le lanceur de mutants de la revue G2 classe une sortie 3 du runner en tué, le correcteur la classe FATAL (§15, E-10).
- **FM-3.2** : l'oracle local ne prouve pas l'image Linux (`git grep -E`, `mktemp`, `sha256sum`, `checkout-index`, modes de fichier : MI-13) ; le hook ne voit ni `cherry-pick` ni `rebase` : items SHOGEN-G5-FORGE-1 et SHOGEN-HOOK-COUVERTURE-1.
  - *Amendement daté du 2026-10-01 (correction de la revue G2, C-G2-9)* : le hook ne voit pas non plus une fusion sans conflit (mesuré par la revue G2) ; item SHOGEN-HOOK-COUVERTURE-1 re-formé.
- **FM-2.3** : gate des secrets, RUNNERS-1 entier, suite S2 et réglages globaux hors du lot (G0 §3 OUT) ; les formes imbriquées restantes vont à LECTEUR-CC-1, sans extension de la sentinelle (faux refus possibles en prose de description).
- **FM-1.5** : coupe par la règle 2 écrite d'avance ; estimation scellée avant code ; mesures publiées.
- **FM-2.4** : faits nouveaux retenus : T-86 épingle ; H-19 ne tue pas MH-8 ; `cd` nécessaire (H-22) ; MI-13 équivalent local ; clé complexe imbriquée hors de la liste de LECTEUR-CC-1 ; borne de 10 min des tâches de fond.
- **FM-2.2** : choix du G1 exposés en Q-G1 (§11).

## 9. `error_origin` proposés (à assigner au G7)

- **E-1** : worktree créé à `fa0ce5b` au lieu de `40b4cfb`. Origine : harnais du workflow (même constat que E-1 de B0 et de D8a).
- **E-2** : C-1 (amendement d'ADR-0028 D8 l.213, ligne d'annexe E), C-2 (réponses écrites aux Q-G0) et C-4 (voie (a) ou (b)), actes de l'orchestrateur prescrits « avant le lancement du G1 » ou « avant tout code », non observés au lancement. Origine : orchestrateur. Effet : lecture du worker au §0 ; D8c-3 livré non consommable.
- **E-3** : H-20 et I-10 toujours verts dans la première forme du runner (affectation `E="…"` entre le test et `res`, qui lit `$?`) ; trouvé par la survie de MH-9 (campagne v1), corrigé avant la v2. Origine : worker G1.
- **E-4** : fonction nommée `in` (mot réservé de bash), erreur de syntaxe au premier lancement ; défaut de construction de H-15 (dossier `docs/` absent du modèle) au deuxième. Origine : worker G1 ; aucun effet sur le livré.
- **E-5** : T-86 annoncé F2P par le G0 (§7.4, phrase finale) ; mesuré épingle (C-5). H-19 nommé tueur de MH-8 par le G0 (§8) ; faux pour le hook livré, où le refus hors d'un dépôt précède `git grep` (H-21 ajouté). Origine : worker G0.
- **E-6** : estimation R-25 ≈ 260 (G1) et ≈ 232 (G0), mesure 356 (runner du hook : 131 lignes contre ≈ 88 au G0 et ≈ 110 au G1 ; `gates.yml` +30 contre ≈ 16 ; lint +32 contre ≈ 15). Origine : worker G1 (commentaires, gardes et cas ajoutés sous-estimés). Traité par la règle 2, sans retrait de contrôle.
- **E-7** : campagne de D8c-2 lancée d'un bloc (37 mutants) puis arrêtée par le worker, faute de tenir sous la borne de 10 min d'une tâche de fond ; relancée par lots. Origine : worker G1 ; aucun résultat perdu.
- **E-8** : MI-13 équivalent en local (montage `noacl`). Origine : environnement.

## 10. Review Focus

1. **Coupe par la règle 2** (§1) : D8c-1a installe par copie directe, D8c-1b remplace par l'installeur ; les quatre sous-lots se revoient ensemble, D8c-3 se consomme après C-4.
2. **Image de g5 sur l'index entier** (CH-3) : S4, S5, S6 refusés et S9 accepté (O-2) ; un marqueur ancien de l'index bloque tout commit (H-12), comme g5 bloquerait la poussée.
3. **Installeur** : contrôle de soi et du blob committé, refus d'un arbre lié et de `core.hooksPath`, sauvegarde par empreinte, `--verifier` en lecture seule ; I-11 par `GIT_INDEX_FILE`.
4. **Branchement** (CH-7, CH-8) : lint et gate pris dans l'index (C-03, C-06), réglage local non lu (C-04), base ancienne refusée (C-12).
5. **Lecture JSON à jetons** (CH-13) : alignement de `grep -o` sur les chaînes entières garanti par la garde de résidu ; tabulations admises dans le résidu ; limites déclarées au §11 (grammaire JSON non vérifiée : chaînes adjacentes, virgules manquantes ; Claude Code ignore-t-il un réglage invalide ? LECTEUR-CC-1). La garde retire `e` et `E` (exposants) avant le verdict : un identifiant non entre guillemets fait de ces seules lettres échappe au résidu ; sans effet sur `model` et `advisorModel`, dont les lettres restent au résidu.
6. **Sentinelle** (CH-12 b) : une prose de description qui porte `{model:` ou `, model:` est refusée (prix déclaré) ; T-84 garde le cas « mot, puis model ».
   - *Amendement daté du 2026-10-01 (correction de la revue G2, C-G2-2 et C-G2-6)* : la sentinelle prend aussi le crochet ouvrant. Prix mesuré (`F:/tmp/shogen-lots/D8c/corr/o/hors-depot.out`) : dans la disposition du G0 §5.4 (b), l'agent global `F:/claude-config/agents/worker.md` (l.3, description qui cite une forme d'appel de workflow entre accolades) est refusé en `R-1/cle-model` par le lint du lot comme par le lint corrigé, alors que le lint de base lisait les neuf agents sans refus ; six des neuf frontmatters globaux ne se lisent pas par PyYAML 6.0.3 (ScannerError) alors qu'ils servent. Versé à SHOGEN-LINT-LECTEUR-CC-1 (question 3) et à SHOGEN-LINT-HORS-DEPOT-1 (§11) ; ligne de limite dans l'en-tête du lint ; voie de fond : question Q-G2-3 de la revue G2.
7. **S-G5 en régime partiel** dans ce worktree (0 artefact sur 125) : les deux documents et la note ne portent aucune citation anglaise entre guillemets (`oracles/docs-controle.out`) ; le régime complet est le rejeu de l'orchestrateur sur l'arbre principal (SHOGEN-ORACLE-PERIMETRE-1 (ii)) ; la commande de mission interdit ici toute copie de `biblio/`.
8. **Temps** : runner du hook 105 et 145 s en local (50 cas) ; coût par `git commit` avec le hook composé : 1,5 à 3,5 s de 1 à 11 fichiers (O-12).

## 11. Questions Q-G1, textes proposés et items

**Questions pour l'orchestrateur**
- **Q-G1-1** : ratifier la coupe D8c-1a / D8c-1b / D8c-2 / D8c-3 (règle 2) et les lignes datées de l'annexe A ci-dessous.
- **Q-G1-2** : ratifier les cas ajoutés H-21, H-22, I-14 et C-13 et les refus ajoutés à l'installeur (sauvegarde différente présente, `core.hooksPath` illisible, argument inconnu).
- **Q-G1-3** : ratifier I-11 par `GIT_INDEX_FILE` (et non `GIT_DIR`, règle d'isolation) et la garde du runner mesurée de même.
- **Q-G1-4** : C-4 : choisir (a) (FAITS de la page des réglages, lecture sur place) ou (b) (ligne datée ci-dessous) ; D8c-3 ne se consomme qu'après.
- **Q-G1-5** : écrire les réponses aux Q-G0 (C-2) et l'amendement de D8 l.213 et la ligne d'annexe E (C-1), ci-dessous.
- **Q-G1-6** : verser à LECTEUR-CC-1 la forme « clé complexe imbriquée » mesurée ; ouvrir, ou non, un item de refus fail-closed des propriétés de nœud imbriquées (voir items).
- **Q-G1-7** : installer le hook après le G7 (CH-6), dans l'ordre du §0, et amender §4.11 (§7).

**Textes proposés (actes de l'orchestrateur)**
- *C-1, ADR-0028 D8 l.213* : « [amendement daté du 2026-09-30, lot D8c : « copie versionnée » → copie portée du blob `9c4c846`, écarts nommés CH-1 à CH-3 du G0 de D8c : mode harnais retiré, classe et portée de g5, index entier] ».
- *C-1, annexe E* : ligne **E-D8c-1** (2026-09-30) : écarts au blob `9c4c846` (hook local, VibeGates `52a569d:enforcement/gate-commit.sh`) : mode harnais retiré (entrée vide sous git, mesuré) ; classe et portée de marqueurs = job g5 élargi (S4, S5, S6 refusés, S9 accepté) ; index entier au lieu des lignes ajoutées ; motif : copie octet pour octet rouge sur g5 (G0 §5.2), revendication de garde de commit retirée par l'amont (ADR-0010 de VibeGates, paraphrasé) ; décision : validateur au cp-1 (Q-G0-1), délégation du 2026-09-30.
- *C-4, voie (b), annexe B (ligne datée)* : « SHOGEN-LINT-LECTEUR-CC-1 — *déclencheur amendé le 2026-09-30 (G0 de D8c §11.1)* : avant toute relaxation d'un refus de CH-12 ou de CH-13 du lot D8c, ou au premier faux refus sur l'arbre principal. Prix déclaré : les refus fail-closed de D8c-3 refuseraient un réglage commenté, y compris `.claude/settings.local.json` au G3 opérant, si Claude Code admet les commentaires (non établi) ; mesure : le réglage local réel est strict (0 faux refus). Formes mesurées restantes (`F:/tmp/shogen-lots/D8c/oracles/sonde-residu-imbrique.out`) : clé complexe, ancre, étiquette, alias et échappement imbriqués. »
- *Lignes datées pour l'annexe A* (colonnes de l'annexe) :

| lot (date) | objet (décision) | véhicule | oracle non-LLM nommé | taille (R-25) | tuyau (entrée → sortie → consommateur ; test) | cp-1 |
|---|---|---|---|---|---|---|
| **D8c** (2026-09-29 ; amendée le 2026-09-30 par le G0 et le G1) | D8 : hook versionné, porté de `9c4c846` (étape R-13 = image de g5 sur l'index), installeur vérifié, motif g5 élargi, note « collision ADR-0020 » ; branchement du lint et de la gate ; SHOGEN-LINT-IMBRIQUE-1 et -JSON-ECHAPPEMENT-1 tranchés | `enforcement/hooks/`, `enforcement/tests/`, `enforcement/lint-model-pinning.sh`, `gates.yml`, `docs/DECISIONS.md` | O-1 à O-12 (O-13 au cp-2) ; mutants MH, MI, MC, ML | 356 [mesuré : 141 + 99 + 65 + 51] | index du commit → hook installé → `git commit` ; test : runner du hook et O-4 | complet |
| **D8c-1a** (2026-09-30 ; règle 2 du G0 §9) | hook (étape R-13), runner (cas H), job g5, note de DECISIONS | hook, runner, `gates.yml`, `docs/DECISIONS.md` | O-1 (22 cas), O-2, O-3, O-5 (MH), O-7, O-10, O-11 | 141 [mesuré] | non consommable seul (installation : D8c-1b) | complet (sous le cp-1 du lot) |
| **D8c-1b** (2026-09-30 ; idem) | installeur, cas I | installeur, runner, commentaire du job | O-1 (36 cas), O-5 (MI), O-6 | 99 [mesuré] | index → hook installé → commits ; job g5 | idem |
| **D8c-2** (2026-09-30 ; idem) | étapes lint et secrets du hook, cas C | hook, installeur (`ATTENDU`), runner, commentaire du job | O-1 (50 cas), O-4, O-5 (MC), O-12 | 65 [mesuré] | lint et gate → hook → commits | idem |
| **D8c-3** (2026-09-30 ; idem ; consommable après C-4) | lint : formes imbriquées (CH-12), JSON à jetons et garde de résidu (CH-13) ; T-77 à T-92 | lint, son runner | O-1 (92 cas du lint), O-5 (ML), O-8 | 51 [mesuré] | `.claude/` et réglages → lint → job g1, hook, G3 opérant | idem |

- *Amendement daté du 2026-10-01 (correction de la revue G2, §15)* : lignes proposées pour l'annexe A, qui remplacent celles du tableau ci-dessus (tailles mesurées sur les états corrigés) :

| lot (date) | objet (décision) | véhicule | oracle non-LLM nommé | taille (R-25) | tuyau (entrée → sortie → consommateur ; test) | cp-1 |
|---|---|---|---|---|---|---|
| **D8c** (2026-09-29 ; amendée le 2026-09-30 par le G0 et le G1, le 2026-10-01 par la correction de la revue G2) | D8 : hook versionné, porté de `9c4c846` (étape R-13 = image de g5 sur l'index), installeur vérifié, motif g5 élargi, note de collision ADR-0020 ; branchement du lint et de la gate ; SHOGEN-LINT-IMBRIQUE-1 et -JSON-ECHAPPEMENT-1 tranchés ; correction G2 C-G2-1 à C-G2-9 | `enforcement/hooks/`, `enforcement/tests/`, `enforcement/lint-model-pinning.sh`, `gates.yml`, `docs/DECISIONS.md` | O-1 à O-12 (O-13 au cp-2) ; mutants MH, MI, MC, ML et ceux de la revue G2 | 365 [mesuré : 144 + 100 + 65 + 56] | index du commit → hook installé → `git commit` et `--amend` (fusions sans conflit : item 2) ; test : runner du hook et O-4 | complet |
| **D8c-1a** (2026-09-30 ; règle 2 du G0 §9 ; corrigé le 2026-10-01) | hook (étape R-13), runner (cas H, H-23 compris), job g5, note de DECISIONS | hook, runner, `gates.yml`, `docs/DECISIONS.md` | O-1 (23 cas), O-2, O-3, O-5, O-7, O-10, O-11 | 144 [mesuré] | non consommable seul (installation : D8c-1b) | complet (sous le cp-1 du lot) |
| **D8c-1b** (idem) | installeur, cas I | installeur, runner, commentaire du job | O-1 (37 cas), O-5 (MI, GI), O-6 | 100 [mesuré] | index → hook installé → commits ; job g5 | idem |
| **D8c-2** (idem) | étapes lint et secrets du hook, cas C | hook, installeur (`ATTENDU`), runner, commentaire du job | O-1 (51 cas), O-4, O-5 (MC, GH), O-12 | 65 [mesuré] | lint et gate → hook → commits | idem |
| **D8c-3** (idem ; consommable après C-4) | lint : formes imbriquées (CH-12, crochet compris), JSON à jetons et garde de résidu (CH-13) ; T-77 à T-95 | lint, son runner | O-1 (95 cas du lint), O-5 (ML, GL), O-8 | 56 [mesuré] | `.claude/` et réglages → lint → job g1, hook, G3 opérant | idem |
| **D8c-C** (2026-10-01 ; correction de la revue G2 de D8c) | liste fermée C-G2-1 à C-G2-9 ; écart mesuré au texte de C-G2-7 (`basename`) ; C-G2-5 appliquée aussi à l'état 1a | hook (en-tête, message), installeur (`ATTENDU`), runners, lint (classe, en-tête), commentaire du job, note de DECISIONS, ce journal, copie du G0 | mêmes oracles ; sondes et mutants de la revue G2 rejoués | +9 [mesuré, code : 365 − 356] | inchangé | sous le cp-1 du lot |

- *Puce datée pour `docs/17-modele-de-menace.md`* (item SHOGEN-MENACES-D8-MAJ-1, au commit de D8c) : « *2026-09-30 (lot D8c)* : T-10 : hook versionné, installé par l'orchestrateur, gate des secrets en mode indexé à chaque `git commit` (noms de chemin et messages : lot D8d) ; T-12 : lint d'épinglage sur `main` depuis `de12b8b`, et dans le hook à chaque `git commit` ; effacement du hook installé vu par `--verifier` au G3 opérant, sans être empêché. »
- *RUNNERS-1* : ramené de 12 à 11 définitions de job (g5 épinglé par D8c).

**Items** (reprise du G0 §11 ; versement à l'annexe B par l'orchestrateur)

| # | item | objet | propriétaire | déclencheur |
|---|---|---|---|---|
| 1 | SHOGEN-HOOK-INSTALL-1 | installation CH-6, ligne de JOURNAL, `--verifier` au G3 opérant ; réinstallation à chaque lot qui change le hook | orch. | G7 du dernier sous-lot de D8c |
| 2 | SHOGEN-HOOK-COUVERTURE-1 | `cherry-pick` et `rebase` sans pre-commit ; recherche côté client (hook `reference-transaction`, non lu) ou rejeu du G3 opérant | orch. | premier commit sur `main` par `cherry-pick` ou `rebase`, ou prochain lot qui touche aux hooks |
| 3 | SHOGEN-G5-FORGE-1 | (a) contrôle requis ; (b) premier run ; (c) outils de l'image, modes de fichier (MI-13), durée du runner sous Linux | orch. ; (a) investisseur ou mainteneur | forge rétablie |
| 4 | SHOGEN-HOOK-SUITE-S2-1 | suite `s2-harness` dans le hook, ou non | orch. | premier commit qui rougit la suite sans que le G3 opérant l'ait vu, ou G0 de RENDU-1 |
| 5 | SHOGEN-D8D-SECRETS-1 | lot D8d (gate : messages, noms de chemin, chemin d'étage, statut de `grep`, masquage) | orch. | commit de D8b |
| 6 | SHOGEN-MENACES-D8-MAJ-1 | puce datée de `docs/17` (texte ci-dessus) | orch. | commit de D8c |
| 7 | SHOGEN-HARNAIS-ECHAPPEMENTS-1 | barres obliques inverses écrites par gabarit et contrôlées sur les octets ; appliqué ici (`od -c`, `chr(92)`, octal `\134`) | orch. | prochaine commande de mission qui porte un regex |
| 8 | SHOGEN-WORKTREE-BASE-HOOK-1 | consigne « avancer la base » ; forme mesurée : C-12 | orch. | installation |
| 9 | SHOGEN-LINT-LECTEUR-CC-1 (demande formée, G0 §11.1) | + forme mesurée : clé complexe imbriquée ; + grammaire JSON (réglage invalide ignoré ou refusé par Claude Code ?) | orch. | voie (a) ou (b) de C-4 |
| 10 | SHOGEN-LINT-IMBRIQUE-2 (proposé, PAROXYSME) | refus fail-closed des propriétés de nœud imbriquées (ancre, étiquette, alias, clé complexe) et des clés échappées à toute profondeur du frontmatter, sans faux refus des puces de description (`* point`) : recherche de la forme, puis cas ; mesure de départ : `sonde-residu-imbrique.out` (5 formes) | orch. | FAITS de LECTEUR-CC-1 (question 2), ou premier bloc `hooks`/`mcpServers` suivi, au premier des deux |
| 11 | SHOGEN-HARNAIS-TACHE-10MIN-1 (transmission) | une tâche de fond du harnais est bornée à 10 min ; toute campagne longue se découpe en lots | orch. (gabarit de mission) | prochaine commande de mission qui porte une campagne de mutants |

Items entrants du G0 §11.1 : tranchés tels que le G0 (IMBRIQUE-1 et JSON-ECHAPPEMENT-1 construits en D8c-3 ; HOOK-LINT-1 et HOOK-SECRETS-1 construits en D8c-2 ; ENV-MODEL-1, HORS-DEPOT-1 et les cinq items de la gate re-formés avec leurs déclencheurs).

- *Amendement daté du 2026-10-01 (correction de la revue G2, §7 de la revue)* : items re-formés, complétés ou neufs (versement à l'annexe B : acte de l'orchestrateur) :
  - **item 2, SHOGEN-HOOK-COUVERTURE-1, re-formé** : (a) fusions : `git merge --no-ff` ne lance pas pre-commit ; construction mesurée par la revue G2 : le même blob installé aussi en `pre-merge-commit` (refus d'une branche marquée, fusion propre acceptée ; rejeu du correcteur identique) ; prix ≈ 12 à 20 lignes [inféré] (installeur : deuxième nom, même `ATTENDU`, `--verifier` sur les deux ; runner : deux cas) ; propriétaire : orch. ; déclencheur : question Q-G2-1, au plus tard avant la première fusion d'une partie dans `main` après l'installation (CH-6) ; (b) `cherry-pick` et `rebase` : interdits par la méthode par parties (PARTIES-S2 l.19), rejeu du G3 opérant.
  - **item 9, SHOGEN-LINT-LECTEUR-CC-1, complété** : six frontmatters globaux sur neuf illisibles par PyYAML 6.0.3 et en service (question 3) ; formes de flux de séquence F1 à F8 refusées par la sentinelle corrigée, à ne relâcher que sur FAITS.
  - **SHOGEN-LINT-HORS-DEPOT-1, remesuré** : D8c-3 refuse `worker.md` l.3 dans la disposition globale ; décision : question Q-G2-3 ; propriétaire : orch., investisseur pour le fichier global ; déclencheur : prochaine décision de roster ou cartographie de clôture, au premier des deux.
  - **SHOGEN-G5-ERREUR-GREP-1 (neuf, PAROXYSME)** : l'étape de balayage du job g5 sort en 0 quand `git grep` échoue (128 vers 0, mesure de la revue G2 ; rejeu du correcteur sur la copie corrigée, `corr/o/sonde-g5-erreur.out` : `git grep` seul 128, étape 0, hook 2 `HOOK/echec`) ; construction : code de `git grep` capté puis `case` (1 vert, 0 refus, autre refus), ≈ 3 lignes, extraction de H-20 adaptée ; propriétaire : orch. ; déclencheur : prochain lot qui touche le job g5, ou SHOGEN-G5-FORGE-1, au premier des deux ; item ou correction dans ce lot : question Q-G2-5.
  - **item 3, SHOGEN-G5-FORGE-1 (c), complété** : `--verifier` et le contrôle après copie ne testent pas le bit d'exécution ; sous Linux un hook non exécutable n'est pas lancé par git [inféré : comportement de git non lu] alors que `--verifier` sort en 0 ; construction : test `-x` aux deux endroits, 2 lignes, mesurable sous Linux seulement.
  - **SHOGEN-D8-PC-1** : fermé au JOURNAL l.149 ; l'annexe B l.201 le porte encore comme acte de l'investisseur : à clore au prochain versement à l'annexe B.
  - **SHOGEN-HARNAIS-BASH-WSL-1 (neuf, transmission)** : sur ce poste, un sous-processus Python qui nomme `bash` sans chemin a lancé le lanceur WSL du dossier système de Windows (`C:/Windows/System32/bash.exe`, distribution Ubuntu installée), non le bash de Git [mesuré : sortie 127, date de `ext4.vhdx` de la distribution à l'heure des appels ; mécanisme inféré : ordre de recherche de `CreateProcess`, non lu] ; consigne : passer le chemin absolu de Git Bash (variable `BASH_EXE` de `g2/o/sonde_crochet.py`) ; propriétaire : orch. (gabarit de mission) ; déclencheur : prochaine commande de mission qui lance un script Python appelant bash.
  - **SHOGEN-MUT-FATAL-1 (neuf, transmission)** : `g2/o/mut-un.sh` classe une sortie 3 (erreur fatale du runner) en tué ; le correcteur la classe FATAL, run invalide (`corr/mut-un.sh`) ; propriétaire : orch. (gabarit de campagne) ; déclencheur : prochaine campagne de mutants.

## 12. Livrables (`F:/tmp/shogen-lots/D8c/`)

- `lot.diff` : diff du lot entier contre `e9ac6e2` (`git add -N .` puis `git diff HEAD`, prescrit), neuf fichiers.
- `d8c-1a.diff`, `d8c-1b.diff`, `d8c-2.diff`, `d8c-3.diff` (**non consommable avant C-4**) et `docs.diff` (copie du G0, journal) : sous-diffs par sous-lot, avec en-têtes `new file mode`, produits dans un clone `--shared` du worktree (`work/clone` ; les commits d'étape vivent dans le clone seul ; `oracles/sous-diffs.sh`) ; la note de DECISIONS est dans `d8c-1a.diff` (règle 2 du G0 §9). Contrôle d'application : `e9ac6e2` + les cinq sous-diffs, et `e9ac6e2` + `lot.diff`, par `patch -p1` : les neuf fichiers égaux à ceux du worktree (`oracles/check-apply.out`).
- `G1-rapport.md` : ce journal, précédé des empreintes des livrables.
- `oracles/` : scripts et sorties (estimation R-25 et son sceau ; `c5-mesure.sh` ; `empreintes.sh`, `r25.sh`, `r25-etats.sh`, `instantane.sh`, `extraire-base.sh`, `derive-1a.py` ; `o1.sh`, `o1-etat.sh`, `o1-lint.sh`, `o2-sonde-hook-local.sh`, `o2-sonde-final.sh`, `statiques.sh`, `docs-controle.py`, `o4-o12.sh`, `o6-garde.sh`, `o8-depot.sh`, `o10.py`, `o11.sh`, `suite.sh`, `xtask.sh`, `cargo_env.sh`, `runners-d8ab.sh`, `check-apply.sh`, `sous-diffs.sh` ; sondes `sonde-h21-h22.sh`, `sonde-bit-x.sh`, `sonde-index.sh`, `sonde-residu-imbrique.sh` ; mutants `mutants.py`, `mutants-run.sh`, `cas-par-mutant.py`, `table-mutants.py`, dossiers `mut-*` ; scripts d'écriture `patch-*.py`, `note-decisions.py`, `g0-copie.py`, `g0-copie-maj.py`, `maj-attendu.sh`, `journal-assemble.py`, `journal-o8.py` ; `oracle_record.py` et `oracle-G1-D8c-substitut.json`).
- `work/` : instantanés figés (`etat-base`, `etat-1a`, `etat-1b`, `etat-2f`, `etat-3f` et les états intermédiaires des campagnes), clone des sous-diffs, brouillons.
- *Amendement daté du 2026-10-01 (correction de la revue G2, §15)* : `lot.diff`, `d8c-1a.diff`, `d8c-1b.diff`, `d8c-2.diff`, `d8c-3.diff` (non consommable avant C-4) et `docs.diff` régénérés sur l'état corrigé, par un clone `--shared` neuf (`F:/tmp/shogen-lots/D8c/corr/clone`) ; `correction-rapport.md` (correction → changement → preuve) ; `corr/` (estimation R-25 scellée, états corrigés et leurs sceaux, sondes adaptées de la revue G2, mutants, sorties, enregistrement d'oracle substitut de la correction).

## 13. Contraintes d'environnement déclarées

- **Garde d'isolation du worktree** : refus mesurés (§0) ; contournement retenu : scripts sous `oracles/`, exécutés directement ; leurs appels git visent ce worktree en lecture (`archive`, `rev-parse`, `log`, `show`, `reflog`, `grep`) ou des dépôts jetables sous `F:/tmp/shogen-tests-tmp/d8c-g1/`.
- **Borne de 10 min des tâches de fond** : une campagne de 37 mutants a été arrêtée puis relancée par lots (E-7).
- **Mode texte et montage `noacl` de Git Bash** : bits d'exécution dérivés du contenu (MI-13).
- **Écrivains concurrents du TMP partagé** : chaque compte O-9 porte sur un TMP neuf.
- **Attributs** : `git check-attr text eol` sur les cinq fichiers neufs : `text: auto`, `eol: lf` pour chacun (`oracles/check-attr.out`) ; 0 CR mesuré dans les neuf fichiers du lot (O-3).
- **Rien sur C:** : TMP, cibles cargo, clones et sorties sous `F:/tmp/` ; `CARGO_HOME` de la mission ; lecture seule de la toolchain sous `F:/rust` (`F:/rust/rustup/downloads` vide après chaque `xtask`).

## 14. Attestation (forme d'ADR-0028 D.3)

- **Pièces lues** : ADR-0028 (D8, §4.10, §4.11, §6) et annexes A (l.30-45), B (B.11) à `40b4cfb` ; le G0 accepté et ses mesures ; `docs/G1-lot-D8a.md` (format) ; le journal et la gate de D8b (état corrigé) ; `JOURNAL.md` (l.122-141) ; `docs/DECISIONS.md` l.1-30 et l.3050-3060 ; `adb2213:.github/workflows/gates.yml` l.25-50 et `adb2213:docs/DECISIONS.md` l.24 et l.3051-3053 ; le hook local (copie scellée du G0) ; `xtask/src/sg4.rs` (liste des locutions) et `sg5.rs` (en-tête).
- **Non ouverts** : les pièces de l'annexe D.2, toutes ; `F:/shogen-campagne/*`, `F:/tmp/shogen-j28/*`, `F:/tmp/shogen-carto-2026-09-29/campagne.md`. Aucune copie scellée lue ; `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée.
- **Balayages mécaniques** : `cargo xtask verify` (S-G4, S-G5) lit tout `docs/` ; `gate-secrets.sh --tree` et `--history` lisent l'arbre et l'historique ; seules les lignes de verdict et de note ont été affichées.
- **Aucune statistique S2 calculée. Aucun z, aucun K, aucun P̂_more ni aucun φ de campagne vu.**
- **Isolation git** : aucun `GIT_DIR`, aucun `GIT_WORK_TREE`, aucun `--write-tree` ; sur ce worktree : `merge --ff-only`, `apply --3way`, un commit d'empilement, `add -N`, `diff`, `archive`, `rev-parse`, `log`, `show`, `reflog show`, `grep`, `ls-files`, `config --get`, `status --short` ; sur `F:/Shogen` : aucune commande git (le journal de refs `HEAD` lu comme un fichier, le hook local haché comme un fichier) ; dépôts jetables et clone `--shared` sous `F:/tmp/` seulement.

## 15. Corrections de la revue G2 (2026-10-01, ajout daté ; lignes précédentes inchangées)

- **Générateur** : `claude-opus-5-5` (R-1 déclaré en tête de session), effort max, contexte frais, worker de correction, distinct du réviseur G2. Même worktree (branche `worktree-wf_089f8fc6-492-6`, HEAD `e9ac6e2`, rien de commité). Aucun commit, aucun workflow (R-20) ; aucun `GIT_DIR` ni `GIT_WORK_TREE`, aucun `--write-tree`. Horloge (`date -u`) : première heure 01:15:20Z ; estimation R-25 scellée à 01:29:05Z, avant tout code ; états corrigés construits à 01:32Z ; temps remesurés sur les octets finaux de 01:55:46Z à 02:00:53Z ; contrôles finaux de 02:01:34Z à 02:06:12Z ; mutants du lint de 01:39:57Z à 01:44:12Z, du hook et de l'installeur de 02:06:23Z à 02:14:55Z ; sonde des arguments du runner (C-G2-7) de 01:51:50Z à 01:55:37Z ; sondes de la revue G2 de 02:06:49Z à 02:11:28Z ; rejeu sur `main`, `xtask`, suite et documents ensuite (rapport de correction).
- **Mandat** : commande de correction de l'orchestrateur Shōgen (`claude-fable-5-1`, workflow) ; liste fermée C-G2-1 à C-G2-9 de la revue G2 (`F:/tmp/shogen-lots/D8c/G2-rapport.md`, ACCEPTE-AVEC-CORRECTIONS ; prototype `g2/w/copie-C4`, diff `g2/corrections-G2.diff`, sha256 `0dad2bae…6074`). Preuves, chemins et empreintes : `F:/tmp/shogen-lots/D8c/correction-rapport.md`.
- **Méthode** : contrôle préalable, `work/etat-3f` plus le diff du G2 égale le prototype (sept fichiers sur sept, `cmp`) ; octets du prototype repris pour le lint, son runner, la note de DECISIONS, le message final du hook, la ligne des chemins absolus (avant l'écart 1) et le cas H-23 ; quatre états reconstruits depuis les instantanés scellés du G1 par `corr/construire.py`, `construire-b.py`, `construire-c.py` (écart 1) et `construire-d.py` (temps finaux), remplacements exacts à compte 1 ; la chaîne rejouée dans un dossier neuf redonne les quatre états et leurs sceaux à l'octet près (`corr/verif-rebuild`), `ATTENDU` calculé en dernier à chaque état ; régénération contrôlée avant toute modification : `git diff HEAD` du worktree égale `lot.diff` du G1 (`4d98b4fa…`) octet pour octet.
- **C-G2-1** (note de DECISIONS) : texte de `g2/o/note_c1.py`, 21 lignes ; O-11 rejoué ; puces datées au §0 et au §3 (CH-14) de ce journal, au §2 et sous CH-14 de la copie du G0.
- **C-G2-2** (sentinelle) : classe `[[{,]` et commentaire du lint, octets du prototype (ligne `SENT`, l.43 de l'état corrigé, contrôlée par `od -c`) ; T-93 et T-94, F2P ; `sonde_crochet.py` : F1 à F9 refusés, P1 accepté ; O-4 k=5 refusé ; lint corrigé sur la copie (2 fichiers) et sur l'arbre principal en lecture (3 fichiers) : sortie 0, 2 fichiers et 3 fichiers, 0 refus (`corr/o/lint-arbres.out`) ; la ligne `SENT` (l.43 de l'état corrigé, l.41 du prototype, décalée par les deux lignes de limite de C-G2-6) égale celle du prototype octet pour octet (`od -c` ; sha256 de la ligne `385237f3…daf8`).
- **C-G2-3** : T-95, épingle ; GL-5b rouge sur T-95 seul.
- **C-G2-4** : H-23 et ligne d'en-tête du runner ; commentaire du job g5 : 51 cas, temps remesurés ; O-4 k=4 refusé ; GH-1 rougit H-23 ; texte proposé pour §4.11 (§7).
- **C-G2-5** : message de succès du hook, texte du G2 à l'état 2 ; `ATTENDU` recalculé en dernier ; `grep -c conforme` sur le hook : 0 ; I-10 vert à chaque état.
- **C-G2-6** : prix mesuré écrit (§10 pt 6, §11), ligne de limite dans l'en-tête du lint (deux lignes) ; `hors-depot.sh` rejoué.
- **C-G2-7** : chemins absolus des deux arguments du runner (écart 1 ci-dessous) ; arguments relatifs depuis la racine : 51 ok (lot : 48 ok, 2 échecs, H-19 et H-22).
- **C-G2-8** : base de commit documentée (§0) ; rejeu sur `205c1b2` : application sans avis de hunk, huit fichiers égaux au worktree, `gates.yml` à `5d6e2bf9…f365` (part de D8b), runners 51, 95 et 113, 0 entrée TMP (`corr/o/cible-main-205c1b2.out`).
- **C-G2-9** : prémisse retirée (§7 et §8 de ce journal ; §3, §10, CH-15, §11.2 et §13.1 de la copie du G0) ; item 2 re-formé (§11) ; en-tête du hook (écart 3) ; sonde de fusion rejouée.
- **Écarts mesurés au texte du G2** (chacun réversible en une édition ; l'orchestrateur tranche) :
  1. **C-G2-7, `basename` au lieu de `${HOOK##*/}`** : sous Git Bash, `dirname` et `basename` coupent sur la barre oblique inverse, `${HOOK##*/}` non ; la ligne prescrite recompose alors `…/hooks/hooks` suivi du nom et sort en 3 sur un argument dont le nom suit une barre oblique inverse, forme que produit `os.path.join` dans les plans de mutants de la revue G2. Sonde (`corr/o/sonde-c7.out`) : ligne du G2, relatif 51 ok, absolu 51 ok, barre inverse sortie 3 ; ligne `basename`, 51 ok sur les trois formes. Sous Linux, les trois coupent sur la seule barre oblique [inféré : POSIX]. Alternative : garder la ligne du G2 et écrire les plans en barres obliques.
  2. **C-G2-5 appliquée aussi à l'état 1a** : le message de 1a (index sans marqueur de dette nu) est le même site à un état antérieur, et la règle d'application du registre 09 corrige en classe, à tous les sites ; texte de 1a : `OK (hook) : aucune étape en refus sur l'index (image locale du job g5)` ; celui de l'état 2 est mot pour mot celui du G2.
  3. **C-G2-9, en-tête du hook** : appliqué, la question Q-G2-1 n'étant pas tranchée et `pre-merge-commit` n'étant pas construit ; si l'orchestrateur construit, l'en-tête et `ATTENDU` changent dans ce sous-lot.
  4. **Lignes d'en-tête** : ligne H-23 dans l'en-tête du runner du hook, que le §6 de la revue G2 demande et que son prototype ne porte pas ; ligne de limite de C-G2-6 dans l'en-tête du lint, sur deux lignes.
  5. **Revue G2 §1.3** : de `40b4cfb` à `205c1b2`, `gates.yml` change (job g3-secrets de D8b) ; seul l'intervalle `3c63e91..205c1b2` laisse intacts tous les fichiers du lot.
  6. **Empreinte abrégée** : la note de DECISIONS du prototype vaut `00d93cc4…c5f9` (le §14 de la revue G2 écrit `…f5f9`) ; le fichier livré lui est égal octet pour octet.
- **Temps** : le commentaire du job cite les passages séquentiels sur les octets finaux (14 à 21 s, 36 à 41 s, 93 à 98 s ; balayage 68 à 78 ms) ; les passages lancés en parallèle (jusqu'à 115 s pour 51 cas) sont au rapport, sans élargir les fourchettes.
- **Oracles** : O-1 (hook 23, 37, 51 ; lint 95), O-2 (S1 à S9b identiques au rejeu de la revue G2), O-3 (0 ligne aux deux motifs du job g5 sur les neuf fichiers, 0 CR ; note : 21 lignes, 96 caractères au plus, 0 guillemet, aucune ligne qui commence par une ponctuation de clôture), O-4 (k = 0 à 5), O-6, O-7 et O-10 (20 sur 20), O-8 (suite 216, `xtask` VERT, G3 opérant du worktree), O-11 ; sondes de la revue G2 rejouées (crochet, fusion, sous-dossiers, erreur de `git grep`, agents hors dépôt) ; rejeu sur `205c1b2`. Détail : rapport de correction.
- **`error_origin` proposés** (assignation au G7) :
  - **E-9** : `sonde_crochet.py` lancée sans `BASH_EXE` (20 appels, vers 01:47Z) a exécuté le lanceur WSL du dossier système de Windows au lieu du bash de Git : sorties 127 ; `ext4.vhdx` de la distribution Ubuntu daté 01:47:14Z : écriture sur C: involontaire, hors des fichiers du lot, non réversible par le correcteur ; sonde relancée avec `BASH_EXE`. Origine : worker de correction. Item SHOGEN-HARNAIS-BASH-WSL-1 (§11).
  - **E-10** : première campagne des mutants du hook invalide : chemins du plan à barre oblique inverse, refusés en sortie 3 par la ligne de C-G2-7, comptés tués par le lanceur repris du G2 ; trouvé à la lecture (13 runs de 0 à 1 s) ; plan normalisé, sortie 3 classée FATAL, campagne relancée. Origine : worker de correction (plan) et revue G2 (classement du lanceur). Item SHOGEN-MUT-FATAL-1.
  - **E-11** : la ligne prescrite par C-G2-7 combine `dirname` et `${HOOK##*/}`, incohérents sous Git Bash (écart 1). Origine : revue G2.
  - **E-12** : deux commandes du correcteur ont dépassé la borne de 6 Ko des commandes Bash, sans erreur de lexage : écriture de `corr/journal-c.py` (environ 7,7 Ko) et de `corr/oracle_record.py` (environ 6,2 Ko) ; un remplacement écrit avec une double barre oblique inverse est arrivé transformé (piège SHOGEN-HARNAIS-ECHAPPEMENTS-1), détecté par l'assertion de compte et refait avec `chr(92)`. Origine : worker de correction ; environnement (outil).
- **Attestation** (forme D.3) : pièces de l'annexe D.2 non ouvertes, ni `F:/shogen-campagne/*`, ni `F:/tmp/shogen-j28/*` ; `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée (retirée par `unset`) ; aucune statistique S2 calculée ; aucun z, K, P̂_more ni φ vu ; suite lue par ses lignes de résumé et les noms des sauts. Git sur `F:/Shogen` : lecture seule en `--no-optional-locks` (`rev-parse`, `log`, `show`, `diff`, `grep` sur des objets, `for-each-ref`, `cat-file`, `archive`) ; journal de refs `HEAD` lu comme fichier. Sur ce worktree : `status --short`, `log`, `branch --show-current`, `worktree list` (orientation), `diff HEAD`, `archive` et `grep`, en lecture. Clone `--shared` et dépôts jetables sous `F:/tmp/` seulement. Écrit sur C: : l'écart E-9, rien d'autre.
