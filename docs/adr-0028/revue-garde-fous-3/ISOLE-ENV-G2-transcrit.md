# Relecture G2 neuve du lot ISOLE-ENV (transcrit)

> Transcription par l'orchestrateur le 2026-10-17 07:31:23 UTC du fichier isole-env/g2/RAPPORT-G2.md ; contrôle FM-1.1 du transcript du réviseur G2 par le fm11.py versé : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5 (176 occurrences, aucune autre). Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Relecture G2 du lot ISOLE-ENV (erreur E39) : rapport

Réviseur : `shogen-worker`, Gate 0 : `claude-opus-5-5` (identifiant donné par le contexte système de la session), effort
`high` ; générateur : l'orchestrateur (réviseur distinct du générateur). Rédigé le 2026-10-17 00:38:47 UTC (`date -u`).
Rattachement : ADR-0028, annexe B, bloc B.108 ; registre des erreurs de l'orchestrateur, entrée E39 (lue en entier).
Base : tête du dépôt `8024a184b91127ce63b84794efb1cea87a1c4010` (attendue `8024a18` : conforme) ; Python 3.11.15.
Dépôt lu seulement (aucune écriture git, aucun cargo) ; copie par `git archive HEAD` hors interdits dans `g2/copie`.

## Verdict : ACCEPTE-AVEC-CORRECTIONS (quatre corrections, liste fermée C-1 à C-4)

Le correctif fait ce qu'il dit : E39 reproduite à la tête et à l'état final de la série, corrigée par le diff, rouge
avant et vert après, plancher juste. Mais le premier cas neuf a pour oracle la fonction qu'il teste : trois mutants
restent vivants sous la commande du job (C-1). Le point 3 trouve deux autres fuites qui font rougir la suite à l'état
final de la série (C-2, C-3), et C-4 corrige une faute de typographie du README.

| C | Base | Fichiers | Objet |
|---|------|----------|-------|
| C-1 | tête + ISOLE-ENV | `scripts/controle/tests/test_aide_garde.py` l.17 | référence indépendante des neuf variables (inclusion) |
| C-2 | `arbre-final` de la série (pas de fin de série) | `scripts/controle/tests/__init__.py` l.7, `.claude/hooks/tests/test_garde_faits.py` l.14, `scripts/controle/tests/test_garde_refus.py` (avant l.168) | `SHOGEN_GARDE_REFUS` posé d'office, plus jamais hérité ; un cas |
| C-3 | `arbre-final` + ISOLE-ENV + C-1 (pas de fin de série) | `scripts/controle/tests/test_gabarit_chaine.py` l.66-68, `scripts/controle/tests/test_aide_garde.py` l.27 | `ROUGE` (faux verif) jamais héritée |
| C-4 | tête + ISOLE-ENV | `scripts/controle/README.md` l.696, l.698 | apostrophes manquantes (`l orchestrateur`, `l environnement`) |

Diffs byte-exacts (étiquettes `a/` et `b/`, sans horodatage, `git apply` vérifié sur leur base) :
- `diffs/C-1.diff` sha256 `da1fc59f9e466dc664d372e81bc4827dcf88a32991e495807542ae272826ef01`
- `diffs/C-2.diff` sha256 `06d8f6a2852b42351d2d47329c50f748b56623ed827341025b98488679d41be6`
- `diffs/C-3.diff` sha256 `e8bf50664396c52717be60c6ca2b86f0075eb59425d3cd1f7a0b2fddfbf6a791`
- `diffs/C-4.diff` sha256 `836b5e93df1214ae0073aea1b56882f27a01aecc5f4922ed34037c29932277d7`

C-1 et C-4 se fondent dans ISOLE-ENV : aucun test de plus, le plancher reste 179. C-2 et C-3 ne peuvent pas entrer
dans ISOLE-ENV. La ligne `setdefault` de C-2 naît au pas INT-03 de la série. Le hunk `@@ -67,7 +68,7 @@` de INT-18
couvre la l.67 de `test_gabarit_chaine.py`, qu'une retouche à la tête ferait échouer. C-2 et C-3 se posent donc en un
pas après INT-19. C-2 y ajoute un test (`planchers.tsv` : une ligne de plus, 1 test), et le plancher final passe de 225
à 226. C-3 n'ajoute aucun test.

## Checklist

### 1. Application, plancher, suite : CONFORME
- `git apply --check` du diff sur la tête : code 0 (`NOTES.md` ; dépôt laissé propre, `git status --porcelain`
  limité à `scripts .github .claude` : vide). Diff : quatre fichiers, 60 lignes ajoutées, 3 retirées (recompté).
  `SHA256SUMS-generateur.txt` contrôlé : toutes les sommes OK.
- Plancher 177 → 179 à la l.369 de `gates.yml` : lu.
- Ligne exacte du job, `--egal`, depuis la racine de la copie (TMPDIR dédié) :
  - environnement normal : `conforme (code 0, résumé final, aucun saut, Ran = 179)` (`preuves/p1-tete-correctif-normal.out`) ;
  - sous `DETACHE=1 DUREE_PAS=60 DELAI=2400 DISQUE_MIN_GO=0` : même ligne (`preuves/p1-tete-correctif-lancement.out`) ;
  - tête seule sous ces variables (plancher 177) : `FAIL: test_e25_lancement_lie (… Chaine …)`, E39 reproduite
    (`preuves/p1-tete-sans-correctif-lancement.out`).
- État final de la série (`arbre-final` copié hors interdits ; correctif posé par `git apply --exclude` de `gates.yml`
  et du README) : `conforme (… Ran = 225)` sous les mêmes variables (`preuves/p1-final-correctif-lancement.out`).
  Sans correctif (plancher 223) : deux échecs, `Chaine.test_e25_lancement_lie` et `ChaineModele.test_e25_lancement_lie`,
  même `AssertionError: Tuples differ: (False, ['X-2', 'X-1']) != (True, [])` que `final-sans-correctif.out` du
  générateur (`preuves/p1-final-sans-correctif-lancement.out`).
- J'ai aussi joué la suite comme le verif réel (`unshare -n`, `lo` allumée par le code `lo` du modèle, variables de
  mandataire retirées), à l'état final avec C-1 à C-3 : `conforme (… Ran = 226)` (`preuves/c-final-C123-unshare.out`).
- Aucune ligne `Exception ignored` ni `Warning` dans les sorties (comptées : 0).

### 2. Rouge avant, vert après : CONFORME
`test_aide_garde.py` posé sur l'aide de la tête (octets égaux à ceux du dépôt, `cmp`) : `ERROR` au premier cas
(`AttributeError: module 'tests.aide_garde' has no attribute 'variables_de_chaine'`) et `FAIL` au second
(`preuves/p2-rouge-avant.out`, code 1) ; avec l'aide du correctif : `OK`, 2 tests (`preuves/p2-vert-apres.out`).

### 3. Autres fuites : deux fuites rougissent, C-2 et C-3
Relevé des appels de `subprocess` (46 lignes trouvées par `grep -n` dans `scripts/controle/tests/` et
`.claude/hooks/tests/` de `arbre-final`) qui lancent un modèle, `avant_acte.py` ou le crochet :
- Modèle de chaîne : `test_gabarit_chaine.py` l.70 (`lancer`, `self.env` vient de `ag.depot`, donc d'`env_git`), l.210
  (`VerifDuModele`, `dict(env, …)` sur `env_git`). Les appels l.146 et l.158/257 (`declare -f`, `bash -n`) et
  `test_avant_acte.py` l.231 n'exécutent pas le modèle.
- `avant_acte.py` : `test_avant_acte.py` l.121, 165, 171, 183, 189, 1058 passent `self.env`, qui vient de `ag.depot`
  (l.59). Le seul appel qui hérite, l.787, lance un `sleep` et non l'outil.
- Crochet : `test_garde_acte.py` l.70 et 355, `test_garde_brief.py` l.161 et 208, `test_skills.py` l.42,
  `test_garde_refus.py` l.46 et `.claude/hooks/tests/test_garde_faits.py` l.57 héritent tous de `os.environ` (pas
  d'`env_git`). Le crochet lit `SHOGEN_GARDE_REFUS` (`garde_faits.py` l.337) et `CLAUDE_PROJECT_DIR`.

Mesure : la suite rejouée sous des valeurs hostiles des neuf variables, de `SHOGEN_GARDE_REFUS` et de `SHOGEN_DEPOT`
(`preuves/hostile.env` : `DEPOT`, `SHOGEN_DEPOT` sur un dépôt leurre, `PYTHON=/bin/false`, `DELAI=1`,
`DISQUE_MIN_GO=1000000`, …). Le dépôt leurre est resté à sa tête `5cd5ec43…` après chaque rejeu.
- tête + ISOLE-ENV : `conforme (… Ran = 179)`, et aucune écriture au journal ambiant (le crochet de la tête ne lit
  pas cette variable) ;
- état final + ISOLE-ENV : `FAIL: test_e26_releve_puis_rattachement (tests.test_garde_acte.Releve…)`, et 232 lignes
  écrites dans le journal ambiant (`preuves/p3-hostile-final-correctif.out`). J'ai isolé la cause en posant
  **`SHOGEN_GARDE_REFUS` seul** : même échec, mêmes 232 lignes (`preuves/p3-refus-seul.out`). Avec `SHOGEN_DEPOT` seul,
  la suite reste verte (`preuves/p3-shogen-depot-seul.out`), comme avec `CLAUDE_PROJECT_DIR` posé sur le leurre
  (`preuves/p3-claude-project-dir.out`).
  Cause : `tests/__init__.py` l.7 et `test_garde_faits.py` l.14 font `os.environ.setdefault(…)`, si bien qu'une
  valeur ambiante gagne. Les cas écrivent alors leurs refus dans le journal ambiant, et le relevé de `test_e26` y voit
  un refus de trop (`test_garde_acte.py` l.395). Le commentaire de l.6 dit pourtant `n'écrit jamais au journal des refus du
  dépôt`. **C-2** : affectation d'office et un cas `test_c2_valeur_ambiante_ecartee` (l'import du paquet `tests` sous
  une valeur ambiante rend `os.devnull`). Le cas rougit sur `__init__.py` de la série (`preuves/c2-rouge-avant.out`)
  et passe au vert avec C-2 (`preuves/c2-vert-apres.out`). Les tests du crochet sous valeur ambiante n'écrivent plus
  rien (avant : 28 lignes, `preuves/p3-crochet-refus.out` ; après : `preuves/c2-crochet-apres.out`).
- Variable propre aux cas, hors des onze du brief : `ROUGE`, que lit le faux verif (`test_gabarit_chaine.py` l.25,
  `${ROUGE:-}`). Avec `ROUGE=X-1` ambiant, la suite finale avec ISOLE-ENV, C-1 et C-2 rougit sur onze cas
  (`preuves/p3-rouge-interne.out`). **C-3** : `lancer` pose `ROUGE=""` (une demande explicite la remplace) et le cas
  E39 du lot rejoue aussi sous `ROUGE=X-1`. Ce cas rougit sans le correctif de `lancer` (`preuves/c3-rouge-avant.out`)
  et passe au vert avec C-3 (`preuves/c3-vert-apres.out`).
- État final avec ISOLE-ENV et C-1 à C-3 : `conforme (… Ran = 226)` sous `ROUGE=X-1`, sous les valeurs hostiles avec
  `ROUGE=X-1` (aucun journal ambiant écrit) et dans l'environnement normal (`preuves/c3-final-C123-*.out`). Même
  verdict sous les variables de lancement (`preuves/c2-final-C1C2-lancement.out`).

### 4. Formes de lecture des variables : CONFORME, limite consignée
Relevé par `preuves/formes.py` (`preuves/formes.out`) sur `chaine.sh` de la tête et sur `chaine.sh` et
`chaine-modele.sh` de `arbre-final`. Aucun nom n'est lu sous la forme `${NOM}`, ni `${NOM-…}` (sans deux-points). Les
`$NOM` nus en majuscules (`DEPOT`, `PLAN`, `CC`, `OUTILS`, `PYTHON`, `DELAI`, `DUREE_PAS`) sont tous aussi lus sous
la forme `${NOM:`. Les seuls noms en majuscules hors du motif sont `LINENO` et `BASH_COMMAND` (`chaine-modele.sh`,
trap ERR), deux variables internes de bash. `variables_de_chaine` ne manque donc rien aujourd'hui. Sous `set -u`, une
variable facultative doit d'ailleurs s'écrire `${NOM:-…}` ou `${NOM:+…}`. La limite que le générateur déclare tient :
un nom neuf lu seulement en `$NOM`, ou en `${NOM-…}`, échapperait à la fonction. C-1 rend visible au moins la perte
d'un nom connu.

### 5. Cas qui en lance un autre : CONFORME (avec C-1 et C-3)
- Effets de bord : `cas.run(resultat)` passe par le `setUp` de `Chaine`, dont le `TemporaryDirectory` est rangé par
  `addCleanup` (`Chaine` n'a pas de `tearDown`). J'ai compté les dossiers laissés sous chaque TMPDIR des rejeux : 0
  partout (`preuves/tmpdirs-restes.txt` ; `aa` ne porte que le diff concaténé que j'y ai écrit).
- Coût : le module entier tourne en 0,9 à 1,1 s (`Ran 2 tests in 0.928s`, `1.059s`).
- Compte : l'issue du cas interne va dans un `TestResult` à part, que le lanceur ne compte pas. On lit `Ran = 179`
  (177 + 2) et `Ran = 225` (223 + 2) : deux tests, pas trois. `tgc` est un module, donc la découverte ne recueille
  pas `Chaine` une seconde fois.
- Jumeau `ChaineModele` : il hérite de `setUp` et de `lancer`, donc de `ag.depot` et d'`env_git`, et
  `chaine-modele.sh` lit les mêmes neuf noms (point 4). Il est couvert par construction, sans cas de plus, à condition
  que l'oracle du premier cas tienne aux neuf noms (C-1).
- Lisibilité : quand le cas interne échoue, la comparaison du tuple tronque sa trace (`[478 chars]`). C'est une
  observation, pas une correction.

### 6. Mutants : C-1 requis
Tous les mutants ont été classés par la commande du job `controle-unittest`, suite entière, avec
`scripts/controle/mutants.py` lancé depuis le dépôt relu, à part de la copie mutée, borne 300 s, groupes de processus
neufs. Le témoin est vivant d'abord, la copie a été rendue à ses octets (`diff -r` vide) et le relevé `ps` de fin
était vide (`aucun processus des 16 groupes de la campagne`). Diffs et sorties de chaque mutant sont dans
`mutants/sortie-*`.
- Avant C-1 (`mutants/campagne-avant-C1.txt`) : M1, M2 et M3 (ceux du générateur, rejoués) sont tués, sortie 1.
  J'ai ajouté quatre mutants :
  - M6 (site d'appel : `depot()` rend `dict(os.environ, **env_git(dossier))`) : tué ;
  - **M4** (motif `${([A-Z]+):`, qui perd `DUREE_PAS` et `DISQUE_MIN_GO`) : **vivant** ;
  - **M9** (motif `…:[-+]`, qui perd `PLAN` et `CC`) : **vivant** ;
  - **M10** (`return frozenset({"DETACHE"})`) : **vivant**.
  La cause : l'oracle du premier cas est `ag.variables_de_chaine()` lui-même, et seul `DETACHE` y est vérifié de
  façon indépendante. M4 rejoué sous `DISQUE_MIN_GO=1000000` ambiant donne 8 `FAIL` (`preuves/p6-M4-sous-DISQUE_MIN_GO.out`) :
  c'est une fuite de la classe E39 que le lot laisse passer.
- **C-1** : référence `LUES`, les neuf noms recopiés du relevé du point 4 (règle 4), vérifiée par inclusion, si bien
  qu'un modèle neuf peut en ajouter. Après C-1 (`mutants/campagne-apres-C1.txt`), les sept mutants (M1, M2, M3, M4, M6,
  M9, M10) sont tués. Tête avec ISOLE-ENV et C-1 sous les valeurs hostiles : `conforme (… Ran = 179)`
  (`preuves/p6-tete-C1-hostile.out`).
- Écart de méthode chez le générateur : ses M1 à M3 ont été classés sur le seul module (`Ran 2 tests`), et non par la
  commande du job (SHOGEN-S2BIS-MUT-COMMANDE-1). Rejoués par la commande du job, ils restent tués.

### 7. Contrôles avant acte : CONFORME
- `avant_acte.py --depot /home/user/shogen --lecture-seule diff --fichier ../isole-env/ISOLE-ENV.diff --rapport
  ../isole-env/RAPPORT-GENERATEUR.md` : code 0, sortie vide (`preuves/p7-avant-acte-ISOLE-ENV.out`). Sur la
  concaténation ISOLE-ENV + C-1 + C-4 avec le même rapport : code 0 (`preuves/p7-avant-acte-ISOLE-ENV+C-1+C-4.out`).
  C-2 et C-3 ont pour base `arbre-final`, qui n'est pas un dépôt git : la série les jugera à leur pas.
- R-13 du job g5 : motif lu dans `gates.yml`, jamais recopié (`preuves/r13.py`), appliqué par `grep -nE` aux fichiers
  touchés par ISOLE-ENV et C-1 à C-4 : aucune ligne (code 1). Le témoin (`tmp/temoin-r13.txt`, une ligne de commentaire au marqueur interdit) est trouvé (code 0) (`preuves/p7-r13.out`).
- S-G5 (`presg5.py`) sur `RAPPORT-GENERATEUR.md` : `0 fragment(s) introuvable(s)`, code 0. Même contrôle sur ce rapport
  et sur `NOTES.md` : `preuves/p7-presg5-g2.out`.

## Affirmations du générateur recontrôlées
- Les pas INT-01 à INT-19 ne touchent ni `tests/aide_garde.py` ni `gates.yml` : vrai, vérifié par lecture des en-têtes
  `+++ b/` des dix-neuf diffs. Les diffs du plancher sont écrits au lancement par `chaine/preparer.sh` depuis `HEAD`
  (l.19-34, plancher = tête + cumul), et ISOLE-ENV ne les gêne donc pas. `test_garde_refus.py`, `__init__.py` et
  `test_garde_faits.py` sont touchés par la série (INT-03 et suivants), d'où la base de C-2.
- Le fichier de sommes des contrôles ne cite pas l'aide : `grep -c aide_garde` sur `scripts/controle/SHA256SUMS` donne 0.

## Items à former (règle PAROXYSME)
- `ISOLE`, variable propre aux cas de `VerifDuModele` (`arbre-final`), que la porte factice lit. Ambiante à `1`, elle
  ferait croire la porte isolée. Je n'ai pas montré que cela fait passer à tort : le contrôle textuel de
  `test_modele` (`unshare -n bash`) tue le mutant évident. À poser vide comme `ROUGE`, si le lot qui porte
  CHAINE-ORCH-MODELE le juge utile.
- Les tests du crochet (`.claude/hooks/tests/test_garde_faits.py`) ne sont lancés par aucun job de `gates.yml` (`grep`
  de `garde_faits` et de `.claude/hooks` sur `gates.yml` : rien).
- `variables_de_chaine` retire aussi `CC` et `PYTHON`, deux noms génériques, de tout environnement des cas. C'est sans
  effet aujourd'hui (aucun cas n'en dépend). À savoir si un cas doit un jour compiler.
- Variables de démarrage de bash (`BASH_ENV`, `SHELLOPTS`) héritées par le lancement du modèle : hors du périmètre du
  lot, non mesuré.
- Je soutiens l'item du générateur SHOGEN-CHAINE-BLANC-ENV-LANCEMENT-1. Les mesures du point 3 montrent que la suite
  doit être jouée sous les variables du lancement, et aussi sous celles des sessions (`SHOGEN_GARDE_REFUS`).
- Enregistrement du rôle G2 (`oracle_record.py`) : non fait. Le lot ne touche pas le chemin S2 (il ne touche que
  `scripts/controle`, `gates.yml` et le README des contrôles), et le brief ne le demande pas.

## Journal de provenance (G1)
Sources lues [lu] : `BRIEF-G2.md` ; registre des erreurs, entrée E39 ; `RAPPORT-GENERATEUR.md`, `ISOLE-ENV.diff`,
`M1.diff` à `M3.diff` et leurs sorties, `final-sans-correctif.out` (lignes `FAIL`/`AssertionError`/`Ran`) ;
`aide_garde.py`, `test_gabarit_chaine.py` et `chaine.sh` (tête) ; `chaine-modele.sh`, `chaine.sh` et
`test_gabarit_chaine.py` de `arbre-final` ; `diag-int3/diag2.sh` et `porte2-15.out` (lignes d'échec : le même cas à
`Ran 178`) ; `int3/ordre.txt`, `planchers.tsv` et `chaine/preparer.sh` (lignes du plancher et du README) ;
`mutants.py` (docstring et `main`) ; extraits de `avant_acte.py`, `garde_faits.py`, `test_garde_refus.py`,
`test_garde_acte.py`, `test_garde_brief.py`, `test_skills.py`, `test_avant_acte.py`, `tests/__init__.py`. Aucune pièce
interdite ouverte, aucune liste sur `docs/`, aucun `*.jsonl`, aucun réseau, `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posé
(retiré par `env -u` à chaque rejeu).
Commandes et sorties : `NOTES.md`, puis `preuves/`, `mutants/` et `diffs/`. Un seul processus lourd à la fois : rejeux
de suite et campagnes l'un après l'autre, campagnes détachées, fin constatée par `tail --pid`. Toutes les sommes sont
dans `SHA256SUMS`.
