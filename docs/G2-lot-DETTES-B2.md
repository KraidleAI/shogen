# Relecture G2 du lot DETTES-B2 (gates : `xtask` S-G9, `enforcement/` secrets, `.github/workflows/`)

Réviseur G2 neuf (`shogen-worker`), qui n'a rien écrit de ce lot. Rapport écrit au fil de l'eau ; du 2026-10-04 06:45:50 UTC à 07:32 UTC (`date -u`).

## 0. Gate 0, pièces et base

- **Modèle** : identifiant exact `claude-opus-5-5` (préfixe attendu `claude-opus-5-5` : conforme). L'effort `max` est
  déclaré dans le message de lancement ; il ne se voit pas depuis l'instance.
- **Brief** : `BRIEF-G2-DETTES-B2.md`, sha256 recalculé `4027b2b22d6e3fadec21c3b4996be4054b76702f8094a0cacf57228810ed2cd5`,
  égal à celui du lancement.
- **Rapport du worker** : `RAPPORT-WORKER-B2.md`, sha256 `0c62263c1a7515d749a02ca6ef8a1ca4907e77f34b726b5b14a44bfb0f82faa6`.
- **Brief du worker** : sha256 recalculé `6985af88a3a652a2488d02b76bb9b87b86853340f8de882d6cb07a60887b776e` (égal au rapport).
- **Tête du dépôt au départ** : `3cc089231717737b44f59536ad4ef959df27092b` (branche `partie-4-execution`).
  Arbre de travail : `.github/workflows/gates.yml` modifié et non committé (sous-lot D8a-3 du lot DETTES-B1, job
  `s2-harness-unittest`), plus trois fichiers non suivis du même lot. Mes copies partent de `git archive 3cc0892`, sans
  ces modifications ; leur interaction avec les diffs 01 à 03 (seuls à toucher `gates.yml` ou la gate) est mesurée au §1.

## 1. Contrôle (1) : application, empreintes, tailles (06:46-06:52 UTC)

- **sha256** des 11 diffs recalculés, chacun retrouvé mot pour mot dans le rapport du worker (contrôle par script) :
  - `01-D8d-1.diff` : `0583e648a1d69de87fa1411fc53d431269195d1cf66580bc600a2b0ddc3b2e5b` (présent tel quel au rapport du worker)
  - `02-D8d-2.diff` : `52453abf1bde18ab266214ef2e1f0ceccab3b0e2e276cdfb1f4fc2b1229ad6fb` (présent tel quel au rapport du worker)
  - `03-G5.diff` : `33d770cc57b2e70c05c46e91d379368d082c73dca6ac0aa065f9e55a51a0a9dd` (présent tel quel au rapport du worker)
  - `04-RUNNERS.diff` : `57f4e69ceabf456a63655af60da036ccd288b8755c1e656f8c8787fb5ab6348d` (présent tel quel au rapport du worker)
  - `05-RUNNERS-WINDOWS-conditionnel.diff` : `8faf68f61303541c8460aa997c67845bae5d7d00e4c2488a7ba2c9f211445bda` (présent tel quel au rapport du worker)
  - `06-XR-1.diff` : `328aa459c5eff5ffa246d7e6ba2dcf58c46612d415d3b932826a5b12cd8a7dd7` (présent tel quel au rapport du worker)
  - `07-XR-2.diff` : `666950902a8258ec681430f9e3c010a621f9b52fbb91babd72fb64f0f3668038` (présent tel quel au rapport du worker)
  - `08-XR-3.diff` : `691ead290ac44d6f1cf6898394768c3c4b39154acd589b4b2bd9e57722537b4d` (présent tel quel au rapport du worker)
  - `09-XR-4.diff` : `07b4d66d6895dfa5e91d03e1982acfafbff8b18f39c92738fb6f6851ec069b89` (présent tel quel au rapport du worker)
  - `10-ACTES-PROPOSES-orchestrateur.diff` : `409a8537135f89b1c9c7a6f9524789ca111cb32ef396e50a5fc2d2377bb71768` (présent tel quel au rapport du worker)
  - `10b-ACTES-PROPOSES-orchestrateur-sur-52b9b4e.diff` : `c45923198926c9af4bebfdfae2ae3a30a760c540f255bd61e0b38fb0caa3d9cc` (présent tel quel au rapport du worker)
- **Ordre déclaré sur la tête `3cc0892`** (copie `git archive`, exclusions du brief) : 01, 02, 03, 04, 06, 07, 10b, 08, 09
  s'appliquent chacun par `git apply --check` puis `git apply`. 05 s'applique après 04 (pas seul). 10 ne s'applique plus
  (`ANNEXE-A-lots.md:130`, attendu : E-10) ; 10b s'applique. 02 ne s'applique pas sans 01 (attendu). 03, 04, 06 seuls : oui.
- **Interaction avec l'arbre non committé du lot B1** : 01, 02 et 03 s'appliquent aussi sur le `gates.yml` modifié de
  l'arbre de travail (sha256 `856ed884…dfd5a`) : aucun conflit attendu, quel que soit l'ordre des commits B1 et B2.
- **Chemins concernés depuis la base du worker** : de `5afbdd2` à `3cc0892`, seuls `ANNEXE-A-lots.md` (+1) et
  `ANNEXE-B-items.md` (+47, B.47 et B.48) changent ; docs/17, docs/08, `enforcement/`, `.github/`, `xtask/` inchangés.
- **R-25** (`git apply --numstat`) : 01 +65, 02 +93, 03 +23, 04 +13, 05 +4, 06 +197, 07 +125, 08 +187, 09 +185, 10/10b +10.
  Tous ≤ 200 ; 08 et 10b ensemble font 197.
- **R-8** : aucun diff ne touche un `Cargo.toml` ni `Cargo.lock` ; `xtask` n'a que des arêtes internes ; `--locked` passe.

## 2. Mesures de base, tête `3cc0892` contre tête + séquence (06:52-07:00 UTC)

| mesure | tête | tête + 01..09 + 10b |
|---|---|---|
| runner secrets | 113 ok, 0 échec | **146 ok**, 0 échec |
| runner hooks | 51 ok | **54 ok** |
| runner model-pinning | 95 ok | **95 ok** |
| `cargo --locked test -p xtask` (cible dédiée, construction neuve) | 31 + 9 | **73 + 9** (42 tests S-G9) |
| `cargo --locked xtask verify` (copie sans dossiers interdits) | VERDICT GLOBAL VERT | ROUGE : S-G9 seul, 1 violation `docs/17:70 → docs/rapports/cartographie-2026-09-29.md:21` (dossier exclu) ; fmt, clippy, no_std VERT |

Lecture YAML (PyYAML 6.0.1, déjà présent) de tous les workflows, tête contre patch : 12 feuilles changent, les 11
`runs-on`/matrice `ubuntu-latest` → `ubuntu-24.04` et l'étape g5. Aucune condition `if:` ne dépend de `matrix.os` (seul un
commentaire de `reproductibilite.yml` en parle) : le changement de valeur ne fait sauter aucune étape ; seuls les noms des
contrôles `compagnon (…)`, `squelette (…)`, `temoignage (…)` changent. `g5-dette` était déjà en `ubuntu-24.04` et checkout
`3d3c42e5…` à la tête : la description de B.4:80 (12 définitions) est bien périmée (11 restaient).

**Tête mobile (07:20 UTC)** : la tête est passée à `dad3bc6` (clôture de DETTES-B1 : `gates.yml` committé, sha256 `856ed884…`,
celui sur lequel 01-03 avaient été vérifiés ; annexe A +1 ligne DETTES-B1 ; annexe B.49), puis à `1ed64e3`, `519bd12` et
`b80b625` (lot POST-PREREG, `scripts/post-s2/` seul : aucun chemin du lot). Contrôles refaits sur `dad3bc6` :

| mesure à `dad3bc6` | tête | tête + séquence |
|---|---|---|
| application | — | 01, 02, 03, 04, 06, 07, 08, 09 : oui ; **10b : non** (`ANNEXE-A-lots.md:131`, ligne DETTES-B1) ; 05 après 04 : oui |
| runners secrets / hooks / model-pinning | 113 / 51 / 95 | **146 / 54 / 95** |
| `cargo --locked test -p xtask` | 31 + 9 | **73 + 9** |
| `verify`, copie sans dossiers interdits | — | ROUGE (S-G9 seul, docs/17:70) ; avec un substitut de 21 lignes vides au chemin exclu : **VERT** |
| `verify`, arbre complet (+ 10c, voir C-5) | — | **9 gates VERT, fmt, clippy, no_std VERT, VERDICT GLOBAL VERT, sortie 0** (lignes VERDICT seules, sortie brute jamais stockée, copie supprimée) |
| commandes B1 du G3 opérant | — | `run-fixtures-verdict-suite-s2.py` : 20 ok ; `verdict-suite-s2.py` : conforme, `Ran 405`, `OK (skipped=2)` |
| `s2-harness/`, `scripts/`, `enforcement/` hors fichiers du lot | — | identiques à l'octet entre tête et patch |

**Tête finale (07:30-07:32 UTC)** : `d97ce4ad1f3590f046b5ff8e1c96f84b4d6f6e7c` (deux commits POST-PREREG de plus, aucun chemin du
lot touché depuis `dad3bc6`). Sur sa copie : 01-04, 06, 07, 10c, 08, 09 s'appliquent, 05 reste applicable après 04 ;
runners 146 / 54 / 95 ; tests 73 + 9 ; `verify` avec le substitut de 21 lignes : 9 gates VERT, fmt, clippy, no_std VERT,
VERDICT GLOBAL VERT, sortie 0. **Les contrôles de ce rapport valent pour `d97ce4a`** (chemins du lot identiques à `dad3bc6`).

Même mesure sur l'arbre complet à `3cc0892` + 01..09 + 10b : VERDICT GLOBAL VERT, sortie 0. Suite `s2-harness` à `3cc0892`
(tête et patch) : `Ran 405`, `OK (skipped=2)`, aucun `__pycache__`, arbres `s2-harness/` identiques à l'octet.
Ma sortie du runner des secrets patché (sha256 `7f9ef8ed…`) est identique à l'octet à la sortie `vert-imbrique` du worker.

**Ordre de commit** (copie cumulée à `3cc0892`, substitut de 21 lignes) : après 01-04, 31 tests, VERT ; après 06, 35, VERT ;
après 07, 47, VERT ; après 08 sans la ligne D8d, 60, **ROUGE** `docs/17:112 (c) lot absent de l'annexe A` ; avec 10b, 60, VERT ;
après 09, 73, VERT. Conforme au tableau du worker.

## 3. Contrôle (3) : rouge avant, vert après, mesurés par moi

Sondes indépendantes du runner (`sondes/`), dépôts jetables, gate de la tête (A) contre gate patchée (B). Les formes sont
fabriquées à l'exécution depuis `fixtures/secrets/sondes.tsv` ; la sortie ne compte que leurs occurrences en clair.

| item | cas | A (tête) | B (patch) |
|---|---|---|---|
| CHEMIN-ETAGE-1 | `0:x` porteur, `x` propre, mode indexé | 0, OK (manqué) | 2, SECRETS/forme |
| GREP-STATUT-1 | enveloppe `grep` qui sort en 2 sur `-anE`, forme indexée | **0, OK** (faux vert) | 2, SECRETS/echec |
| MASQUE-EXCLUSION-1 | entrée d'exclusion = forme, sans `ADR-` | 2, forme **en clair** (1 fuite) | 2, masquée (0 fuite) |
| noms de chemin (I-G2-3) | `<forme>.txt` au contenu propre | 0, OK (manqué) | 2, SECRETS/forme `(chemin)` |
| MESSAGES-1 | forme dans le corps d'un message de commit | 0, OK (manqué) | 2, SECRETS/historique |
| MESSAGES-1 | forme générique dans un tag annoté | 0, OK (manqué) | 2, SECRETS/historique |
| MESSAGES-1 | tag imbriqué, message intérieur porteur | 2, echec « blob ou arbre » | 2, SECRETS/historique |
| (relâchement) | tag imbriqué propre | **2, echec** (diagnostic faux) | **0, OK** |
| HORS-REFS-1 | blob orphelin porteur, `--hors-refs` | 2, argument inconnu | 2, SECRETS/hors-refs |
| HORS-REFS-1 | dépôt propre, `--hors-refs` | 2, argument inconnu | 0, OK (0 sur 3) |
| extension de l'item 5 | ref vers un blob propre | 2, echec | 0, OK (T-75c) |
| extension de l'item 5 | ref vers un blob porteur | 2, echec | 2, SECRETS/historique `refs/tags/tb:(objet)` |
| G5-ERREUR-GREP-1 | index vidé, étape lancée par `bash -e` et par `bash --noprofile --norc -eo pipefail` | **0, OK** (faux vert) | 1, `git grep a échoué (code 128)` |
| CI-RUNNERS-1 | feuilles YAML `ubuntu-latest` | 11 | 0 (restent 3 `windows-latest`, diff 05) |
| E1-XTASK-REFS-1 | cinq des six cas de B.7:143 ajoutés à docs/17 (vraie copie) : résidu en majuscules, apostrophes, décimal, pour-cent en lettres, `LISEZ-MOI.txt` nu | VERDICT GLOBAL VERT (manqués) | S-G9 ROUGE, le bon motif chacun |
| E1-XTASK-REFS-1 | sixième cas, la borne : « lot MONARK G9 » | VERT | VERT, listé `lots MONARK : [G7, G2, G1, G8, G9]` |

Dix-sept sondes de plus sur docs/17 (sondes/rv-sg9.sh). Treize ROUGE au bon motif : `INCIDENT-2026-09-26`, nom de mois,
JJ/MM/AAAA, chemin `./`, plage hors fichier, fichier absent, item inventé, lot inventé, guillemet droit, citation française
inventée, IPv4, statistique, adresse électronique. Référence `biblio/` pendante sans octets `biblio/` : listée en note (borne
voulue), VERT. `1.97.1` en prose : VERT (pas de faux positif). Deux faux positifs mesurés sur
des textes hypothétiques : `` `crate::documents` `` → « (f) adresse IP » ; `SHOGEN-CLOTURE-S2-1` → « (f) pièce de D.2 »
(voir O-2 ; l'item réel `SHOGEN-BUNDLE-CLOTURE-1` existe à l'annexe B).

**Constat C-1 (mesuré)** : copie où `biblio/` porte des octets (`biblio/factice-sonde.pdf` ajouté) : une référence
`biblio/inexistant-sonde.pdf.sidecar:3` est listée « biblio/ absente, non contrôlée(s) ici » et S-G9 reste **VERT** ; une
référence à un fichier `biblio/` présent avec une plage hors fichier est bien ROUGE. La borne est prise sur l'absence du
**fichier**, pas sur l'environnement (S-G6, `sg6.rs` l.68-84, ne la prend que si `biblio/` n'a aucun octet hors `INDEX.md` et sidecars).

## 4. Contrôle (4) : mes mutants (39, dont 35 tués, 4 survivants, 0 FATAL)

Outil : `mut/muter.py` (remplacement exact à occurrence unique, contrôlée avant lancement ; restauration à l'octet vérifiée
par sha256 ; tué = sortie 1 du runner ou 101 de `cargo test`, survivant = 0, autre = FATAL ; S-G9 : compilation d'abord,
échec de compilation = FATAL). Barres obliques inverses de la table écrites `\x5c`.

- **Gate des secrets** (`mut/table-secrets.tsv`, runner patché, copie dédiée) : 14 mutants, **13 tués**.
  RS-01 statut du grep VENDOR ignoré (T-82, T-102 à T-104) ; RS-02 statut du grep GENERIC (T-82b, T-83) ; RS-03 `":$f"`
  (T-81, T-81b) ; RS-04 noms non balayés (T-79, T-91, T-91b, T-82b) ; RS-05 `%B` → `%s` (T-96) ; RS-06 chaîne de tags coupée
  au premier niveau (T-105) ; RS-07 `comm -23` → `comm -12` (T-97, T-98b, T-99, T-102) ; RS-09 objet de ref jamais retenu
  (T-75, T-75d) ; RS-10 message « traversant » non masqué (T-85) ; RS-11 `--hors-refs` sans garde superficiel/greffé
  (T-101) ; RS-12 tags annotés non lus (T-95, T-105) ; RS-13 seuls les blobs de refs (T-75d) ; RS-14 `pipefail` retiré
  sur `git show` (T-90).
  **Survivant RS-08** : les noms d'entrée d'un arbre pointé par une ref ne sont plus imprimés dans le flux balayé ; aucun
  cas ne le voit, alors que le code et son commentaire l'annoncent (« arbre : noms et blobs réguliers ») → **C-3**.
- **Étape g5** (`mut/table-g5.tsv`, runner des hooks) : 5 mutants, **5 tués** (H-24a, H-24b, H-24c, H-20).
- **S-G9** (`mut/table-sg9.tsv`, `cargo test --test mutants`, témoin vert 73) : 20 mutants, **17 tués**.
  Survivants : **MX-06** (toute référence `biblio/` sautée, fichier présent ou non : aucun cas avec `biblio/` peuplé) →
  couvert par C-1 ; **MX-07** (`[aucun contrôle]` sans motif accepté : la règle du motif, docs/17 l.9 et contrôle (a) de
  l'oracle, n'a aucun cas qui échoue) → **C-2** ; **MX-12** (condition d'élision de la fermante retirée) : condition de
  précision, sans effet sur le verdict du vrai docs/17 (mesuré : VERT) → observation O-3.
  Le test proposé en C-2 passe sur le code livré et tombe sous MX-07 ; le cas proposé en C-3 refuse
  `refs/arbres/n:(objet)` avec la gate patchée et sort en 0 sous RS-08 ; l'esquisse jetable de C-1 (+3 −1 lignes dans
  `controle_a`) passe les 73 tests et le test neuf, que le code livré échoue (« S-G9 devait être ROUGE et ne l'est pas »).

## 5. Contrôle (2) : conformité item par item

- **SHOGEN-D8D-SECRETS-1** et ses quatre composants : conformes à B.15 (I-G2-1 à I-G2-4, item 8) et à G0-lot-D8c l.484-488 et
  l.504 (G0 : `G0-lots-DETTES.md` ; ligne datée à l'annexe A : 10b, à reposer, C-5). Rien de plus, sauf un relâchement non
  déclaré (ci-dessous). Résidu juste : pas de `commit-msg` (I-4).
- **SHOGEN-SECRETS-HORS-REFS-1** : conforme (inatteignables et journaux de refs par `--hors-refs`, bundle par clone et
  `--history`, comptes seuls, refus superficiel ou greffé ; extension de l'item 5 construite). Acte local restant au
  déclencheur (custodie sur F:/Shogen).
- **SHOGEN-G5-ERREUR-GREP-1** : conforme (B.16 l.284 : code capté, `case` 1/0/autre ; H-20 adapté ; H-24a à H-24c).
- **SHOGEN-CI-RUNNERS-1** : part Linux conforme ; non fermé, à juste titre (Windows, « digest », résidu B.47).
- **SHOGEN-E1-XTASK-REFS-1** : les six cas de B.7:143 ont leur test et sont mesurés (§3). Deux écarts : **C-1** (borne
  `biblio/` ouverte en environnement peuplé) et **C-4** : l'oracle `verif_refs.py` porte aussi les contrôles (g) « deux
  formes proscrites » et (h) structure des tables (« ligne T retirée, S sans menace ni motif, cellule de résidu vide, jeton
  de chemin servi absent, marqueur entre guillemets au lieu du jeton », `docs/G1-lot-E1-modele-de-menace.md` l.113), ni
  mécanisés ni déclarés nulle part (rapport, code, tests, actes : 0 occurrence). Ce sont des limites tues (règle PAROXYSME).
- **Resserrement T-79** (lien symbolique dont le nom porte une forme : ignoré → refusé) : juste, c'est I-G2-3 (noms de toute
  entrée) ; le contenu du lien reste hors portée, déclaré.
- **Relâchement T-75** (ref vers un blob ou un arbre : refus fermé → balayage) : juste, ordonné par l'extension datée de
  l'item 5 (B.15 l.258, Q-C-2, rr1) ; l'objet est balayé par les mêmes motifs (blob ; arbre : noms et blobs réguliers, sous
  les exclusions du contrat, comme les autres modes).
- **Relâchement non déclaré** : un tag imbriqué propre était refusé à la tête (`%(*objecttype)` ne pèle qu'un niveau sous git
  2.43.0, mesuré : `tag tag`, d'où « 1 ref(s) vers un blob ou un arbre », diagnostic faux) ; il est accepté après (T-105b),
  chaque niveau de message et l'objet final étant balayés. Juste sur le fond ; absent de l'E-4 du worker → à acter avec T-75
  (C-5, Q-3).

## 6. Contrôle (5) : S-G9 sur docs/17 et sur l'arbre réel

- **Juste sur docs/17** pour les familles (a) à (f) : six cas de B.7 et dix-sept sondes au bon motif (§3), à C-1 près.
  Non exhaustive : (g) et (h) (C-4).
- **Aucun faux positif sur l'arbre réel** : arbre complet à `3cc0892` et à `dad3bc6`, plus la séquence : S-G9 0 violation,
  verdict global VERT. La violation `docs/17:70` n'existe que sur les copies sans `docs/rapports/`.
- **Faux positifs latents** (textes hypothétiques, la gate échoue fermée) : O-2.
- **Fichier exclu de la copie (question du brief)** : la gate ne doit pas excuser une absence de fichier (leçon de C-1). Je
  propose de former l'item N-2 avec cette convention : une référence dont le **dossier entier** appartient à la liste fermée
  des interdits (G0-lots-DETTES l.14) et manque de la copie est listée en note (« dossier interdit absent de la copie, non
  contrôlée ici ») ; si le dossier existe, contrôle plein. En attendant, une consigne suffit, mesurée : un substitut de N
  lignes vides au chemin exclu, N ≥ la plus grande ligne citée (ici 21), créé **sans lire** l'original ; `verify` est alors
  VERT. Le compte exact de 112 lignes (E-2 du worker, lecture d'un fichier interdit) n'était pas nécessaire.

## 7. Contrôle (6) : diff 05 (Windows)

**Recommandation : ne pas appliquer 05** tant que l'orchestrateur n'a pas lu sur la source primaire (README des images de
runner pour Windows 2025) l'existence du libellé `windows-2025` **et** la valeur par défaut de `core.autocrlf` sur cette
image. Motifs : (1) 05 ne change pas qu'un libellé : il réécrit en fait affirmé le commentaire de `temoignage.yml`
(« sur `windows-2025`, `core.autocrlf` vaut `true` par défaut »), dont dépend ce que le job éprouve (la règle `-text`) ;
sans lecture, c'est une affirmation de mémoire versée au dépôt (G1) ; (2) un libellé inexistant laisserait les trois jobs
Windows en attente sans runner, donc la seule vérification Windows du témoignage muette ; (3) aucune urgence : la forge
est arrêtée (ADR-0028 §4.11) et l'échéance du 2026-10-19 vise `ubuntu-latest` (commentaire de `gates.yml`), couverte par 04.

## 8. Contrôle (7) : règles

R-25 : tous les diffs ≤ 200 lignes ajoutées (06 : 197, marge de 3). R-13 : 0 ligne ajoutée au motif g5 sur les 11 diffs.
R-8 : aucun `Cargo.toml` ni `Cargo.lock` touché, `--locked` passe partout. `verify` VERT sur l'arbre complet + séquence
(`3cc0892` et `dad3bc6`). Runners 146 / 54 / 95. Suite `s2-harness` inchangée (arbre identique, 405 OK, skipped=2).
Gate patchée sur le dépôt réel (lecture seule, `GIT_OPTIONAL_LOCKS=0`, tête `519bd12`) : indexé, `--tree` (537 fichiers),
`--history` (364 commits) et `--hors-refs` (0 objet hors refs sur 3099) sortent en 0 ; les 8 objets apparus dans `.git`
pendant la mesure appartiennent aux commits concurrents `519bd12` et `b80b625` (contrôlé par `rev-list`).

## 9. Verdict et corrections

**Verdict : ACCEPTE-AVEC-CORRECTIONS**, liste fermée C-1 à C-5.

- **C-1 (S-G9, contrôle (a), borne `biblio/`)** : ne poser la borne que si l'environnement n'a pas d'octets `biblio/`
  (prédicat de S-G6, ou plus strict : aucun fichier hors `INDEX.md`) ; sinon un fichier `biblio/` absent est « fichier
  introuvable ». Deux tests : `biblio/` peuplé et référence pendante → ROUGE « fichier introuvable » ; `biblio/` peuplé,
  fichier présent, plage hors fichier → ROUGE « plage hors du fichier » (tue MX-06). Libellé de la note et de la ligne
  DEVOPS : « biblio/ sans octets ». Place : diff 07 (≈ +20 lignes, reste < 200).
- **C-2 (S-G9, cellule de contrôle)** : ajouter le cas `mutant_sg9_a_aucun_controle_sans_motif`
  (`"| T-03 x | a | b | c | [aucun contrôle] | r | i |\n" => "cellule de contrôle"`) ; vérifié : passe sur le code livré,
  tue MX-07. Diff 07, +1 ligne.
- **C-3 (runner des secrets)** : ajouter un cas « ref vers un arbre dont une entrée porte un nom en forme d'identifiant,
  contenu propre » → `2 SECRETS/historique '^refs/…:\(objet\)$'` ; vérifié : tue RS-08. Diff 02, +1 à 2 lignes (147 cas).
- **C-4 (S-G9, limites tues)** : déclarer dans la note « non mécanisés » de S-G9, dans l'en-tête de `sg9.rs` et au rapport
  du worker que (g) formes proscrites et (h) structure des tables S et T de `verif_refs.py` ne sont pas mécanisés ((i) et
  (j), propres au lot E1, sans objet), et former l'item correspondant (N-3). R-25 : 06 n'a que 3 lignes de marge ; placer
  la note dans 09 (qui touche déjà `executer`) ou dans les lignes existantes.
- **C-5 (actes proposés et comptes)** : 10b ne s'applique plus depuis `dad3bc6` (annexe A, ligne DETTES-B1) : le reposer
  (ma reconstruction de mesure, `actes/10c.diff`, sha256
  `9f7e864a1fa58a5a40150f913eff9ac89b6765ed17ba854daed09df5d43bd910`, s'applique sur `dad3bc6`, à refaire si l'annexe A
  bouge encore) ; mettre à jour après C-1 à C-4 les comptes des lignes D8d, DETTES-B2-b, -f, -h (cas, tests, mutants),
  écrire « (a) à (f) mécanisés ; (g), (h) non » et « biblio/ sans octets » dans la ligne DEVOPS ; déclarer le relâchement
  des tags imbriqués propres avec celui de T-75 (E-4 du worker, Q-3).

## 10. Réponses aux questions du worker (une ligne chacune)

- **Q-1** : ni 10 ni 10b sur la tête actuelle : depuis `dad3bc6`, les deux échouent (annexe A, ligne DETTES-B1). Reposer les
  actes (10c, C-5) avant 08 ou dans le même commit (08 + actes = 197 lignes), comptes mis à jour.
- **Q-2** : ne pas appliquer 05 avant la lecture sur place du libellé `windows-2025` et du `core.autocrlf` par défaut de
  l'image (§7).
- **Q-3** : oui, acter T-75 (ordonné par B.15 l.258), et dans le même acte le relâchement des tags imbriqués propres (T-105b,
  non déclaré) et le resserrement T-79.
- **Q-4** : oui, amendement daté de §4.11 : secrets 146 plus les cas de C-3 (147 si un seul), hooks 54 ; retirer la phrase de l.297 sur
  `SECRETS/echec` « ref vers un blob ou un arbre » (ces refs sont désormais balayées) ; `--hors-refs` consigné à chaque G3,
  bloquant avant toute copie brute de `.git` en custodie et avant l'acte de publication, avec le bundle cloné puis balayé
  par `--history` ; un refus sur F:/Shogen appelle `reflog expire` et `gc --prune`, actes destructifs à décider.
- **Q-5** : oui sur le principe (un document interdit ne doit pas valider une citation, et le verdict ne doit pas dépendre
  de la copie), mais comme item, joint à N-2 et I-2 : sans effet aujourd'hui (docs/17 : 0 citation française contrôlée).
- **Q-6** : oui, une puce datée de l'orchestrateur en fin de docs/17 (hors périmètre du lot), comme SHOGEN-MENACES-D8-MAJ-1 :
  T-09, T-10 (noms couverts par le hook, messages non : I-4), T-14, T-04 ; S-G9 la contrôlera elle-même.

## 11. Avis sur les items I-1 à I-7, items neufs, observations

- **I-1 SHOGEN-SG5-NOTES-INTERDITS-1** : **former**, priorité haute (antérieur au lot) ; tout `verify` d'un worker sur
  l'arbre réel affiche de la matière interdite ; n'imprimer que `chemin:ligne`.
- **I-2 SHOGEN-SG9-PERIMETRE-1** : **former**, priorité basse ; exige une convention de référence ; avec O-2 et Q-5.
- **I-3 SHOGEN-SG9-CORPUS-1** : **former**, joint à I-2 et N-2 (Q-5).
- **I-4 SHOGEN-SECRETS-COMMIT-MSG-1** : **former** ; docs/17 l.112 promet « noms de chemin et messages » au hook, les messages
  ne sont vus que par `--history`.
- **I-5 SHOGEN-CI-RUNNERS-1** : **garder ouvert** (pas d'item neuf) : libellé et `core.autocrlf` Windows lus sur place ;
  « digest » écrit comme limite (un runner hébergé ne prend qu'un libellé) ; résidu B.47 ; noms des contrôles avant tout
  `required_status_checks`.
- **I-6 SHOGEN-XTASK-TMP-NOMS-FIXES-1** : **former** (collision mesurée, E-7 du worker) ; consigne d'ici là : `TMPDIR` dédié
  par copie (appliquée dans cette relecture).
- **I-7 (docs/17)** : **pas d'item** : acte de l'orchestrateur, puce datée (Q-6).
- **N-1 SHOGEN-SECRETS-NOMS-REFS-1 (neuf, à former)** : aucun mode ne balaie les noms de refs (branches, tags, notes) ni les
  champs d'identité ; et la sortie d'erreur de git n'est pas masquée : une ref cassée dont le nom porte une forme est
  imprimée en clair par git (mesuré : `--history`, déjà à la tête ; `--hors-refs`, neuf). Construction : balayer
  `for-each-ref --format='%(refname)'` par les mêmes motifs, sortie masquée ; stderr de git passé par `masque`.
  Déclencheur : avant l'acte de publication, ou prochain lot qui touche la gate.
- **N-2 SHOGEN-SG9-COPIE-INTERDITS-1 (neuf, à former)** : convention du §6 (dossier interdit entier absent → borne listée ;
  présent → contrôle plein) ; consigne immédiate : substitut vide de N ≥ 21 lignes, original jamais lu.
- **N-3 SHOGEN-SG9-STRUCTURE-1 (neuf, issu de C-4)** : mécaniser (g) et (h) de `verif_refs.py` sur docs/17.
- **O-2 (observation)** : heuristiques de (f) qui refusent à tort, en échec fermé : `::` collé à un chiffre hexadécimal
  (`crate::x`, `sg5::y`) ; préfixes de D.2 (`CLOTURE-`, `INCIDENT-`, `REPAIR-`) dans un identifiant
  (`SHOGEN-BUNDLE-CLOTURE-1` existe). À corriger avant la première citation de ce genre dans docs/17, ou avec I-2.
- **O-3 (observation)** : MX-12 survit (condition d'élision non testée, sans effet sur docs/17 aujourd'hui).
- **O-4 (observation)** : la liste des noms de D.2 de S-G9 ne couvre, par construction, que des noms de fichiers ou dossiers :
  D.2 n° 7 (`*.jsonl`) et n° 11 (identifiant de session) restent au seul contrôle FM-1.1.

## 12. Écarts du réviseur

- **ER-1** : la sonde de masquage (§3) a affiché 13 caractères de la forme factice V-01 des fixtures du dépôt, imprimée en
  clair par la gate de la tête (le défaut mesuré). Valeur synthétique ; ni secret, ni matière interdite.
- **ER-2** : deux copies complètes (avec dossiers interdits) ont servi au `verify` sur l'arbre complet. Sortie brute jamais
  stockée (filtrée par grep des lignes VERDICT à la source), copies supprimées aussitôt (07:09 et vers 07:23 UTC).
- **ER-3** : substitut de 21 lignes vides au chemin `docs/rapports/cartographie-2026-09-29.md` dans mes copies. Original jamais
  lu ni compté.
- **ER-4** : la gate des secrets lancée sur le dépôt réel lit tous les objets, matière interdite et pièces D.2 de
  l'historique comprises ; elle n'imprime que des verdicts (admis par le brief).
- **ER-5** : plusieurs appels `python3` (édition de ce rapport, tables, aides de sondes) sans le préfixe
  `env -u … PYTHONDONTWRITEBYTECODE=1`. La variable était absente de mon environnement (présence contrôlée une fois, valeur
  jamais lue) ; scripts par l'entrée standard ; 0 `__pycache__` dans les copies.
- **ER-6** : tête mobile (§2). Contrôles faits à `3cc0892`, refaits à `dad3bc6`, puis vérifiés à `d97ce4a` ; de `dad3bc6`
  à `d97ce4a`, aucun chemin du lot ne change.
- Aucune opération git en écriture ; rien installé ; `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée ; aucune pièce D.2 ouverte ;
  aucun `*.jsonl` ouvert (la transcription du worker n'a pas été lue).

## 13. Journal de provenance (G1)

**Lu [lu]** (tête `3cc0892`, sauf mention) :
- brief G2 (sha256 `4027b2b2…cd5`), rapport du worker (`0c62263c…faa6`), brief du worker (`6985af88…776e`) ;
- `docs/adr-0028/G0-lots-DETTES.md` en entier ; `ETAT-REGISTRE-2026-10-04.md`, lignes des neuf items ;
- `ANNEXE-B-items.md` : B.4 l.70-80, B.7 l.138-149, B.15 l.234-258, B.16 l.261-290, B.47 et B.48 l.689-734 ;
- `G0-lot-D8c.md` l.470-520 ; `ANNEXE-D-preenregistrement.md` l.32-47 (liste D.2 seule) ;
- `docs/17-modele-de-menace.md` en entier ; `docs/G1-lot-E1-modele-de-menace.md` l.80-118 ; ADR-0028 §4.11 l.287-299
  (arbre de travail, l.299 venue de `3226dd2`) ; `docs/DEVOPS.md` (lignes `biblio`) ; `.gitignore` (lignes `biblio`) ;
- les onze diffs en entier ; `gate-secrets.sh` patché en entier ; `run-fixtures-secrets.sh` patché l.1-180 ; `sg9.rs` final
  en entier ; `sg6.rs` l.55-95 ; `sg8.rs` l.1-40 ; `source.rs` l.220-268 ; `lib.rs` l.40-110 ; `main.rs` l.10-40 ;
  `xtask/Cargo.toml` ; `.cargo/config.toml` ; `rust-toolchain.toml` ; tests S-G9 de `mutants.rs`.

**Mémoire, non lu** : shell d'une étape sans `shell:` (`bash -e {0}`) : g5 mesuré sous les deux shells ; existence de
`windows-2025` : non vérifiée. **Mesuré** : `%(*objecttype)` d'un tag imbriqué = `tag` sous git 2.43.0.

**Non lu** : `docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`, `monark-m009a/`,
`apres-execution/`, pièces D.2, tout `*.jsonl`, pages GitHub, `PASSATION-CLOUD.md`, fiche `shogen-worker`.

**Outils** (sha256, 16 premiers caractères) : `run.sh` 869fed35… ; `cargo.sh` 5bcbed69… ; `yamldiff.py` 407b4555… ;
`sondes/rv-secrets.sh` b5fb17fc… ; `sondes/rv-g5.sh` 2f87d60c… ; `sondes/rv-sg9.sh` f7433b0c… ; `sondes/fuite-ref.sh`
893becc9… ; `sondes/c3.sh` 97e5024b… ; `mut/muter.py` af46863a… ; `mut/test-sg9.sh` cae1ca41… ; tables : secrets
fd6fc5ec…, g5 92a0fc48…, sg9 35a2d6e0… ; `actes/10c.diff` 9f7e864a….

**Sorties** (`o/`, sha256 16 caractères) : rv-secrets 14484a98… ; rv-g5 4163a1f1… ; rv-sg9 057c6b16… ; fuite-ref
9ee01127… ; mut-secrets f773df4d… ; mut-g5 44175183… ; mut-sg9 ca9d8356… (témoin ce38295a…) ; verify arbre complet
(VERDICT seuls) 0d1a01fa… aux deux têtes ; runners tête 48ca3737… / 1b923027… / 44cd6951…, patch 7f9ef8ed… / dcefd2a5… /
44cd6951… ; tests `xtask` ad18564… / 4c2e4e90… ; `s2-harness` b03c4458… / 12b7fca2… ; à `dad3bc6` : test 151b4844…,
verify avec substitut 4b2117b8…, vérificateur B1 699e3349… (cas 46132101…).

**Chiffres recomptés par moi** : 113 → 146 cas ; 51 → 54 ; 95 ; 31 → 35 → 47 → 60 → 73 tests (+9) ; 11 feuilles YAML ;
12 feuilles changées ; 405 tests `s2-harness` ; 537 fichiers, 364 commits, 3099 objets (dépôt réel) ; 39 mutants.

## Résumé

Le lot fait ce qu'il annonce : la gate des secrets ferme ses quatre défauts et ajoute les messages, les refs non-commit
et les objets hors refs ; l'étape g5 n'accepte plus un `git grep` en erreur ; les images Linux sont épinglées ; S-G9
mécanise sur docs/17 les contrôles (a) à (f). Tout est mesuré rouge avant et vert après. L'arbre complet patché est vert à
deux têtes, et aucune dépendance n'est ajoutée. Cinq corrections restent avant commit : la borne `biblio/` de S-G9 laisse
passer une référence pendante quand `biblio/` est peuplé (C-1) ; deux règles n'ont aucun cas qui échoue (C-2, C-3) ; deux
contrôles de l'oracle sont omis sans être déclarés (C-4) ; les actes sont à reposer sur la tête, avec un relâchement
(tags imbriqués) à acter (C-5). Le diff Windows (05) attend une lecture sur place.
