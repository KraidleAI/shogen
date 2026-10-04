# Rapport du worker G1 : lot DETTES-B2 (gates : `xtask`, `enforcement/`, `.github/workflows/`)

Horloge (`date -u`) : travail du 2026-10-04 04:02 à 06:41 UTC. Aucune opération git en écriture sur le dépôt. `SHOGEN_S2_CAMPAGNE_CONTROL` n'a jamais été posée. Aucune pièce D.2 n'a été ouverte par moi. Rien n'a été installé.

## 0. Gate 0 et base
- **Modèle** : l'identifiant exact est `claude-opus-5-5`, conforme au préfixe attendu. L'effort ne se voit pas depuis l'instance : le `max` explicite est à constater dans la commande de lancement.
- **Brief** : `/tmp/claude-0/-home-user-shogen/7ba84933-ba6d-5813-9ef4-ca3ac4febd16/scratchpad/dettes/BRIEF-DETTES-B2.md`. Son sha256 recalculé, `6985af88…7b776e`, est égal à celui du brief.
- **Base de la copie** : `5afbdd2` (git archive), la même que celle du brief.
- **La tête du dépôt a bougé pendant le lot** : 5afbdd2, puis 3e275a2, 52b9b4e et 6b4b49c.
  - Aucun des 17 chemins touchés ne change sur cette période, sauf `docs/adr-0028/ANNEXE-A-lots.md`, qui reçoit la ligne DETTES-A à 52b9b4e.
  - C'est pourquoi le diff 10b existe.

## 1. Livrables

Dossier : `/tmp/claude-0/-home-user-shogen/7ba84933-ba6d-5813-9ef4-ca3ac4febd16/scratchpad/dettes/DETTES-B2/livrables/`. Les tailles viennent de `git apply --numstat`.

| diff | sha256 | lignes | contenu | s'applique sur |
|---|---|---|---|---|
| 01-D8d-1 | `0583e648a1d69de87fa1411fc53d431269195d1cf66580bc600a2b0ddc3b2e5b` | +65 −25 | gate et runner des secrets : étage 0, statut de grep, masquage, noms de chemin | 5afbdd2 |
| 02-D8d-2 | `52453abf1bde18ab266214ef2e1f0ceccab3b0e2e276cdfb1f4fc2b1229ad6fb` | +93 −17 | messages de commit et de tag annoté (tags imbriqués compris), objets des refs non-commit, `--hors-refs`, commentaire du job g3 | après 01 |
| 03-G5 | `33d770cc57b2e70c05c46e91d379368d082c73dca6ac0aa065f9e55a51a0a9dd` | +23 −9 | étape g5 (code de `git grep` capté), cas H-24a à H-24c, H-20 | 5afbdd2, seul |
| 04-RUNNERS | `57f4e69ceabf456a63655af60da036ccd288b8755c1e656f8c8787fb5ab6348d` | +13 −13 | 11 définitions `ubuntu-latest` passées en `ubuntu-24.04`, plus 2 commentaires | 5afbdd2 |
| 05-RUNNERS-WINDOWS-conditionnel | `8faf68f61303541c8460aa997c67845bae5d7d00e4c2488a7ba2c9f211445bda` | +4 −4 | `windows-latest` passé en `windows-2025` ; **libellé non lu** | après 04 |
| 06-XR-1 | `328aa459c5eff5ffa246d7e6ba2dcf58c46612d415d3b932826a5b12cd8a7dd7` | +197 −0 | S-G9 : infrastructure et contrôle (b) | 5afbdd2 |
| 07-XR-2 | `666950902a8258ec681430f9e3c010a621f9b52fbb91babd72fb64f0f3668038` | +125 −1 | S-G9 : contrôle (a) | après 06 |
| 08-XR-3 | `691ead290ac44d6f1cf6898394768c3c4b39154acd589b4b2bd9e57722537b4d` | +187 −1 | S-G9 : (c), (d) numérique, décimaux et IPv4 de (f) | après 07, **et la ligne D8d de l'annexe A (10 ou 10b) avant ou dans le même commit** |
| 09-XR-4 | `07b4d66d6895dfa5e91d03e1982acfafbff8b18f39c92738fb6f6851ec069b89` | +185 −4 | S-G9 : noms de mois de (d), (e), reste de (f) | après 08 |
| 10-ACTES-PROPOSES-orchestrateur | `409a8537135f89b1c9c7a6f9524789ca111cb32ef396e50a5fc2d2377bb71768` | +10 −0 | actes de l'orchestrateur : annexe A (D8d, DETTES-B2-a à h) et DEVOPS (ligne S-G9) | 5afbdd2 et 3e275a2 |
| 10b-ACTES-PROPOSES-orchestrateur-sur-52b9b4e | `c45923198926c9af4bebfdfae2ae3a30a760c540f255bd61e0b38fb0caa3d9cc` | +10 −0 | mêmes lignes, placées après la ligne DETTES-A | 52b9b4e et 6b4b49c |

**Ordre de commit vérifié vert à chaque pas** : 01, 02, 03, 04, 06, 07, puis 10 ou 10b, puis 08, puis 09. On peut aussi committer 08 et 10 ensemble (197 lignes ajoutées).
- 08 sans la ligne D8d de l'annexe A rend S-G9 rouge : (c) « lot absent de l'annexe A : D8d », sur docs/17 l.112.
- 05 ne doit être appliqué qu'après lecture du libellé Windows.

## 2. Les items un par un

### SHOGEN-D8D-SECRETS-1 et ses quatre sous-items — construit
Fermable au commit de 01 et 02, avec l'acte de l'annexe A (10 ou 10b). Contrat [lu] : G0-lot-D8c l.480-489 et l.497, annexe B.15 l.236-258.

- **CHEMIN-ETAGE-1** : la gate lit `":0:$f"`.
  - Cas T-81 (index) et T-81b (arbre) : un fichier `0:x` porteur à côté d'un `x` propre est refusé.
  - Rouge avant mesuré sous Linux : la gate de 5afbdd2 lisait `x` et sortait en 0.
- **GREP-STATUT-1** : `formes()` capte le statut de chaque grep. Un statut de 2 ou plus est un échec fermé, sur six flux : contenu, noms, historique, messages, refs, hors refs.
  - Une enveloppe de PATH fait sortir grep en 2 : cas T-82, T-82b, T-83, T-102, T-103, T-104.
- **MASQUE-EXCLUSION-1** : tout chemin ou pathspec imprimé passe par le masque (exclusions, greffes, `git show`, avis). Cas T-84 à T-90.
- **Noms de chemin** : balayés en modes indexé et arbre, cas T-91, T-91b, T-92.
  - T-79 (lien symbolique dont le nom porte une forme) passait « ignoré » ; il est maintenant refusé. C'est un resserrement.
- **MESSAGES-1** : la gate balaie les messages de commit (`log --all`, lignes indentées) et de tag annoté.
  - Les tags couverts sont ceux de toute ref vers un objet tag, à chaque niveau d'un tag imbriqué.
  - Cas T-94, T-95, T-96 (faux en-tête « commit » dans un message), T-105 (tag imbriqué porteur) et T-105b (tag imbriqué propre).
- **Extension datée de l'item 5 (B.15, Q-C-2)** : les refs vers un blob ou un arbre sont balayées au lieu d'être refusées. Cas T-75, T-75c, T-75d, T-75e.

**Preuves** :
- Le runner passe de 113 à 129 cas (01), puis à 146 cas (02).
- Rouge avant : 16 échecs pour 01, 14 pour 02, puis 1 pour T-105.
- Mutants : 37, dont 35 tués et 2 équivalents déclarés (MD-08, ME-10).
- Dépôt de la session à 06:29 (lecture seule, `GIT_OPTIONAL_LOCKS=0`) : `--history` sort en 0 sur 351 commits ; `--hors-refs` sort en 0, avec 0 objet hors refs sur 2985 ; `find .git -newer` ne trouve aucun fichier modifié.

**Résidu** : il n'existe pas de hook `commit-msg` (G0 D8c l.484). Les messages ne sont donc vus que par `--history`, et pas au moment du commit (item I-4).

### SHOGEN-SECRETS-HORS-REFS-1 — construit, fermable au commit de 02
- Le mode `--hors-refs` prend `cat-file --batch-all-objects` moins `rev-list --objects --all` et balaie ce reste. Il ne rend que des comptes et refuse un dépôt superficiel ou greffé.
  - T-97 : blob orphelin.
  - T-98a et T-98b : un commit qui ne vit que dans les journaux de refs est invisible à `--history` et vu par `--hors-refs` (3 objets).
  - T-99 : dépôt propre. T-101 : dépôt superficiel. T-102 : grep en erreur.
- Le bundle de custodie se clone, puis se balaie par `--history` (T-100).
- Je n'ai pas ajouté d'étape CI : un clone neuf de la forge n'a pas d'objet hors refs [inféré].
- Reste un acte local : lancer `--hors-refs` avant toute copie brute de `.git` en custodie, sur F:/Shogen.

### SHOGEN-G5-ERREUR-GREP-1 — construit, fermable au commit de 03
- L'étape devient `g=0; git grep … || g=$?` suivie d'un `case` :
  - code 1 : OK ;
  - code 0 : refus R-13 ;
  - tout autre code : `::error::git grep a échoué (code N)` et sortie 1.
- Cas H-24a (propre), H-24b (marqueur) et H-24c (index vidé). Le bloc est extrait de gates.yml et lancé par `bash -e`.
- Rouge avant : avec l'étape de 5afbdd2, H-24c sortait en 0 avec « OK ».
- 54 cas verts ensuite ; 4 mutants tués sur 4.

### SHOGEN-CI-RUNNERS-1 — **non fermé** (la part Linux est livrée)
- **Linux** : les 11 définitions flottantes restantes passent en `ubuntu-24.04`.
  - Lecture YAML avant et après (PyYAML 6.0.1, déjà présent) : seules ces 11 feuilles changent, plus celle de g5 (diff 03).
  - Avec 05, 15 feuilles changent en tout.
- **Déjà fait avant le lot** : g5-dette était épinglé et son checkout aligné sur v7.0.1 depuis `87b246a` (lot D8c-1a).
  - La ligne B.4:80 (12 définitions, 15 instances) est donc périmée : à 5afbdd2, il restait 11 définitions et 14 instances.
- **Windows (3 instances)** : le libellé n'a pas été lu, faute de réseau GitHub (brief).
  - `windows-2025` vient de ma mémoire, non vérifiée.
  - Le commentaire de temoignage.yml sur `core.autocrlf` doit être revérifié pour ce libellé.
- **Épinglage par digest** : impossible pour un runner hébergé, car `runs-on` ne prend qu'un libellé. B.4:78 le dit déjà. Je l'écris comme manque.
- **Résidu ajouté par B.47** : l'appartenance du SHA `3d3c42e5` au tag v7.0.1 n'est pas vérifiée. Non traité ici.
- **Effet de bord** : les noms des contrôles portent `matrix.os` et changent donc. Sans effet aujourd'hui, puisqu'il n'y a aucun `required_status_checks` (GC-09).

### SHOGEN-E1-XTASK-REFS-1 — construit sur le périmètre de verif_refs.py (docs/17)
Fermable au commit de 06 à 09 avec 10.

**La gate** : S-G9 `references`, dans `xtask/src/sg9.rs` (530 lignes), branchée dans `verify`. Elle porte les contrôles (a) à (f) :
- (a) références `chemin:ligne`, sha MONARK de 40 chiffres, cellule de contrôle des lignes T-xx ;
- (b) résidus au registre 08, casse comprise ;
- (c) items à l'annexe B et lots à l'annexe A ; PX et lots MONARK sont listés comme bornes, jamais résolus ;
- (d) dates ISO seules ;
- (e) guillemets droits, citations entre apostrophes, citations françaises cherchées dans le corpus ;
- (f) pièces D.2 (noms nus compris), pour-cent en signe et en lettres, décimaux, IPv4 et IPv6, adresses, statistiques.

**Les six cas nommés par B.7:143 ont chacun leur test** :
- `mutant_sg9_b_residu_en_majuscules`, `mutant_sg9_e_apostrophes`, `mutant_sg9_f_nombre_decimal` ;
- `mutant_sg9_f_pour_cent_en_lettres`, `mutant_sg9_f_nom_nu_de_d2_n8`, `temoin_sg9_bornes_monark_et_px_listees`.

**Tests** : 42 tests S-G9 (2 témoins, 39 mutants d'arbre, 1 de couverture).
- Rouge avant : une ébauche vide donnait 37 échecs sur 68 tests.
- Mutants de code : 45 tués sur 46 à la première campagne. XC-02 survivait, j'ai ajouté le test `mutant_sg9_c_item_en_troisieme_cellule`, puis 46 sur 46.

**Non mécanisé, imprimé en note** : les lignes de D.2 par sha256 (outil FM-1.1), la graine et la clé du constat, le contenu de docs/16, la fidélité des lignes citées (lecture G2).

## 3. Vérifications faites après la dernière modification (06:25-06:40)
- **Tête 52b9b4e plus 01 à 09 plus 10b** (extraction sans dossiers interdits, sans matière Pocket, sans `docs/adr-0028/execution/apres-execution/`) :
  - secrets 146 ok, hooks 54 ok, model-pinning 95 ok ;
  - `cargo --locked test -p xtask` : 73 et 9 tests ok ;
  - `cargo --locked xtask verify` : 8 gates VERT, et S-G9 avec 1 violation, `docs/17:70 → docs/rapports/cartographie-2026-09-29.md:21` (dossier exclu par le brief ; le fichier existe, même blob `d00d8011…` de 5afbdd2 à 52b9b4e, 112 lignes) ;
  - avec un substitut de 112 lignes vides pour ce fichier : VERDICT GLOBAL VERT ;
  - avec en plus les octets locaux de `biblio/` : VERT, S-G9 résout 78 références et S-G6 fait son contrôle plein ;
  - s2-harness : 398 tests OK (skipped=2), aucun `__pycache__`.
- **Sur 5afbdd2** : la séquence 01-04 puis 06-09 donne exactement la copie de travail. 01, 03, 04 et 06 s'appliquent seuls ; 02 sur 01 ; 05 sur 04 ; 10 sur la séquence.
- **États cumulés, dans l'ordre de commit** :

| après | runners | `cargo test -p xtask` | `cargo xtask verify` |
|---|---|---|---|
| 01 | secrets 129, hooks 51 | — | — |
| 02 | secrets 146, hooks 51 | — | — |
| 03 | hooks 54 | — | — |
| 04 | pinning 95 | — | — |
| 06 | — | 35 | VERT |
| 07 | — | 47 | VERT |
| 08 | — | 60 | ROUGE (D8d) seul ; VERT avec 10 |
| 09 et 10 | — | 73 | VERT |

- **Dépôt jetable bâti sur l'arbre final** : la gate sans argument, `--tree` (470 fichiers), `--history` et `--hors-refs` sortent en 0 ; l'étape g5 et le lint d'épinglage passent.

## 4. Journal de provenance (G1)
**Lu [lu]**, à 5afbdd2 sauf mention :
- brief ; G0-lots-DETTES (en entier) ; ETAT-REGISTRE ;
- annexe B : B.4 l.74-80, B.7 l.143, B.15 l.236-258, et B.47 l.690-705 à 3e275a2 ;
- G0-lot-D8c l.478-512 ; annexe A ; G1-lot-D8b ; G1-lot-E1 ;
- docs/17 (en entier), docs/08, DEVOPS, PASSATION-CLOUD ;
- les 7 workflows, `enforcement/*`, les sources de `xtask`, Cargo, `biblio/INDEX.md` ;
- la fiche `.claude/agents/shogen-worker.md`, diff de 5afbdd2 à 52b9b4e, lue après coup.

**Seconde main [2nd]** : le sens gitrevisions de `<0-3>:<chemin>`, cité par B.15. Ma mesure le confirme : T-81 est rouge sur la base.

**Mémoire, non vérifiée** : le shell `bash -e {0}` d'une étape sans `shell:` ; le libellé `windows-2025`.

**Non lu** : docs/15-*, docs/16-*, docs/pocket-report, docs/rapports (sauf un compte de lignes, voir E-2), docs/adr-0025, monark-m009a, les pièces D.2, `apres-execution`, les pages GitHub.

**Sorties** dans `/tmp/claude-0/-home-user-shogen/7ba84933-ba6d-5813-9ef4-ca3ac4febd16/scratchpad/dettes/DETTES-B2/o/` (16 premiers caractères du sha256) :

| fichier | sha256 |
|---|---|
| mut-d8d1 | c7d87c3f… |
| mut-d8d2 | 20ad2a5d… |
| mut-MN-01 | 1eede411… |
| mut-MN-02 | 331d935e… |
| mut-g5 | 8448db0f… |
| mut-sg9-campagne1 | ad2cf740… |
| mut-sg9-final | 4f317530… |
| rouge-imbrique | 1eede411… |
| vert-imbrique | 7f9ef8ed… |
| tete2-verify-substitut | c2bb76ec… |
| tete2-verify | 5c427879… |
| tete2-verify-biblio | 74d61073… |
| tete2-test | 62ec71a7… |
| tete2-s2 | 0c7a7234… |
| reel3-history | 2c8ba54a… |
| reel3-hors-refs | e2688ac5… |
| cumul (`sondes/cumul/resume.out`) | 3c6c3133… |
| 08 + 10 (`sondes/cumul/08+10-verify.out`) | ab3c63cc… |

**Scripts** : `run.sh` (9d79278c…), `cargo.sh` (5c3b94cc…), `mut/mutants.py` (b6993b61…), `mut/mutants_cargo.py` (cad3fcf3…), `sondes/faire_diffs.py` (57b06e2d…), `sondes/cumul/cumul.sh` (30e15042…).

**Équivalents déclarés** :
- **MD-08** : le refus « pathspec global » ne vaut que pour `.`, `*`, `**` ou vide, qui ne peuvent porter aucune forme. Le masque y est donc sans effet.
- **ME-10** : élargir le filtre aux tags qui pointent vers un commit fait balayer des arbres que le flux d'historique couvre déjà ligne à ligne. Le verdict est le même.

**Erreur de prédiction** : ME-03 est tué par T-94 et T-96, mais pas par T-104 comme prévu.

**Classement des mutants** : par la sortie du runner (conforme à MUT-FATAL-1). Aucun FATAL.

Transcription pour FM-1.1 : `/root/.claude/projects/-home-user-shogen/7ba84933-ba6d-5813-9ef4-ca3ac4febd16/subagents/agent-a337a77a2b9c7eeb2.jsonl`.

## 5. Écarts
- **E-1** : `verify` est rouge sur ma copie, seulement à cause du fichier exclu. Voir §3.
- **E-2** : accès à de la matière interdite, sans aucun affichage.
  - J'ai compté les lignes d'un fichier interdit : `git cat-file -p 5afbdd2:docs/rapports/cartographie-2026-09-29.md | wc -l`.
  - La gate des secrets, lancée sur le dépôt de la session, lit tous les objets, y compris les pièces D.2 et la matière Pocket. Elle n'imprime que des verdicts.
  - La recette de copie du brief n'excluait pas docs/15-*, docs/16-* et docs/pocket-report. Ils étaient donc dans mes premières copies, jamais affichés ni sondés.
  - Mais S-G5 a écrit, dans 4 de mes fichiers de sortie, une note qui cite docs/15-…:292. Je ne l'ai jamais affichée. J'ai retiré cette ligne et consigné les sha256 avant et après :
    - verify-base : 6b73cd3b… devient 0c41c562… ;
    - verify-final-actes : 47c81a1c… devient 69c06125… ;
    - gates-1 : d5328d08… devient 9daf0f51… ;
    - gates-2 : 898f3ddf… devient 67fb91b8….
- **E-3** : 44 appels à python3 sur 58 n'avaient pas le préfixe `env -u … PYTHONDONTWRITEBYTECODE=1`.
  - J'ai contrôlé que la variable est absente de mon environnement (présence seulement, valeur jamais lue).
  - `-B` était toujours mis, et aucun `__pycache__` n'a été créé.
- **E-4** : deux cas du runner changent de contrat.
  - T-79 : resserrement.
  - T-75 : un refus fermé est relâché. Une ref vers un blob ou un arbre propre est maintenant acceptée (T-75c, T-75e). C'est ordonné par l'extension datée de l'item 5 en B.15 ; à acter (Q-3).
- **E-5** : tailles. E1-XTASK-REFS-1 était estimé à environ 150-250 lignes ; mesuré +694 −6. D8d mesure +158 −42.
- **E-6** : la description du registre pour RUNNERS est périmée (voir l'item).
- **E-7** : incidents du harnais.
  - Une cible cargo partagée entre copies déplacées a produit une vérification faussement verte. Je l'ai refaite avec des cibles dédiées ; seules celles-ci font foi.
  - Les dates conservées par la copie ont laissé un artefact périmé ; j'ai relancé avec des copies sans dates.
  - J'ai retiré les dossiers `/tmp/shogen-mutant-sg9-*` et laissé ceux d'autres noms, partagés avec d'autres sessions.
- **E-8** : les temps ont été mesurés sous une charge moyenne de 15-17 sur 4 cœurs, puis de 1 à 3.
- **E-9** : modification tardive. En relisant mon propre code après la vérification de 06:03, j'ai vu que les messages des tags imbriqués n'étaient pas balayés.
  - Diff 02 révisé : cas T-105 et T-105b, mutants MN-01 et MN-02, rouge avant puis vert après.
  - Toutes les vérifications ont été refaites, et 10 a été mis à jour.
- **E-10** : 10 ne s'applique plus à partir de 52b9b4e, d'où 10b.
- **E-11** : j'ai lu les consignes de gabarit de la fiche worker après coup.
  - Barres obliques des lignes neuves contrôlées par `od -c`. La seule double barre, `'\\'` dans `canonique`, est voulue.
  - Aucune tâche longue n'a été interrompue.

## 6. Items à former (PAROXYSME)
- **I-1 SHOGEN-SG5-NOTES-INTERDITS-1** : S-G5 imprime le texte des citations de tout `docs/**/*.md`.
  - Mesuré : une note Pocket sur une copie de 5afbdd2.
  - Sur l'arbre réel, cela concerne probablement aussi rapports, adr-0025 et monark-m009a (non mesuré).
  - Conséquence : un `verify` lancé par un worker sur l'arbre réel lui affiche de la matière interdite.
  - Construction proposée : exclure ces dossiers, ou n'imprimer que `chemin:ligne`.
- **I-2 SHOGEN-SG9-PERIMETRE-1** : étendre S-G9 aux autres docs (préambule de B.7:143). 157 références courtes ne se résolvent pas sans une convention.
- **I-3 SHOGEN-SG9-CORPUS-1** : le corpus de (e) contient, sur l'arbre réel, des dossiers interdits et des pièces D.2.
  - Je propose de les exclure (resserrement).
  - Aujourd'hui sans effet : docs/17 ne porte aucune citation française.
- **I-4 SHOGEN-SECRETS-COMMIT-MSG-1** : hook `commit-msg`. La puce de docs/17 l.112 attend « noms et messages » du hook ; les noms sont faits, les messages non.
- **I-5 SHOGEN-CI-RUNNERS-1** reste ouvert : libellé Windows, décision sur le « digest », résidu B.47, noms des contrôles.
- **I-6 SHOGEN-XTASK-TMP-NOMS-FIXES-1** : les tests de `xtask` écrivent sous `temp_dir()` à des noms fixes. Deux sessions sur le même hôte entrent en collision.
- **I-7, docs/17 (hors périmètre du lot)** :
  - T-09 l.67 : « images flottantes (gates.yml:35) » ;
  - T-14 l.105 : `gates.yml:54-92` est périmé ;
  - T-10 l.112 : voir I-4 ;
  - T-04 l.62 : FIXTURE-MANIFESTE-1 est rattaché au « G0 du lot MONARK G1 », alors que l'annexe B l.147 dit « clôture S3 et passage public ».

## 7. Questions à l'orchestrateur
- **Q-1** : appliquer 10, ou 10b sur la tête ? La ligne D8d doit venir avant 08 ou avec lui.
- **Q-2** : 05 attend la lecture du libellé Windows et de la valeur par défaut de `core.autocrlf` sur cette image.
- **Q-3** : actez-vous le changement de T-75, ordonné par B.15 ?
- **Q-4** : ADR-0028 §4.11 (G3 opérant). Il faudrait passer les comptes à secrets 146 et hooks 54, et ajouter `--hors-refs` ainsi que le balayage du bundle par clone et `--history` avant toute custodie sur F:/Shogen.
- **Q-5** : le resserrement I-3 ?
- **Q-6** : faut-il une puce datée sur docs/17 (I-7) ?

## Résumé
Sur les cinq items, quatre sont construits et testés :
- D8D-SECRETS-1, avec ses quatre sous-items et les tags imbriqués ;
- SECRETS-HORS-REFS-1 ;
- G5-ERREUR-GREP-1 ;
- E1-XTASK-REFS-1, avec la nouvelle gate S-G9 sur docs/17.

Ils sont livrés en 9 diffs de moins de 200 lignes chacun, plus les actes proposés (10, et 10b pour la tête actuelle). Tous les tests sont verts à chaque pas de l'ordre proposé.

SHOGEN-CI-RUNNERS-1 reste ouvert. La part Linux est livrée ; la part Windows attend la lecture du libellé (05 est conditionnel). L'épinglage par digest est impossible sur un runner hébergé.

Sur ma copie, `verify` n'est rouge qu'à cause du fichier exclu. Avec un substitut de 112 lignes, il est globalement vert sur la tête 52b9b4e.

Sept items sont proposés et six questions posées. La plus urgente est I-1 : un `verify` lancé sur l'arbre réel affiche de la matière interdite aux workers.