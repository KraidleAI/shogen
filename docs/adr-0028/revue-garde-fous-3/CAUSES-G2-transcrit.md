# Relecture G2 neuve du lot CAUSES (transcrit)

> Transcription par l'orchestrateur le 2026-10-17 07:31:23 UTC du fichier causes/g2/RAPPORT-G2.md ; contrôle FM-1.1 du transcript du réviseur G2 par le fm11.py versé : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5 (231 occurrences, aucune autre). Texte ci-dessous avec 8 retouche(s) (E35, E38) : noms de marqueur de dette et locutions de la gate S-G4 cités en clair, mis en code, segments de code à doubles accents graves réécrits en segments simples, heures sans date dans les 25 caractères ou approchées mises en code ou entre guillemets français, sans autre changement (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Relecture G2 neuve du lot CAUSES (E37, E39, E40 ; pas INT-20 à INT-22 de la chaîne INTEGRATION-P3)

Gate 0 : réviseur `claude-opus-5-5` (identifiant exact du modèle résolu), effort `high`, worker `shogen-worker`, distinct du
générateur (l'orchestrateur). Travail du 2026-10-17 00:28:22 au 01:46 UTC (`date -u`). Rattachement : ADR-0028, annexe B,
bloc B.108 ; registre des erreurs de l'orchestrateur, entrées E37, E39, E40 (lues en entier, l.68-82). Dépôt
`/home/user/shogen` lu seulement, tête `8024a184b91127ce63b84794efb1cea87a1c4010` ; aucune écriture git, aucun commit,
aucun cargo, aucune vraie chaîne ; `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée ; aucune pièce interdite ouverte. Notes de
reprise : `NOTES.md` du même dossier (suffit seul).

## Verdict : ACCEPTE-AVEC-CORRECTIONS (liste fermée C-1 à C-5)

C-1 est bloquante : sans elle, la chaîne INTEGRATION-P3 ne peut pas passer le lot (K8 rouge à son premier acte, verif
rouge au pas INT-22). Les quatre autres corrigent des faux refus et des fautes admises mesurés du crochet, et le texte
README. Avec C-1 à C-4 en série sur `../copie` : suite `scripts/controle` conforme (Ran = 231) dans l'environnement
normal, sous `DETACHE=1 DUREE_PAS=60 DELAI=2400 DISQUE_MIN_GO=0`, et sous ces variables plus une chaîne factice vivante ;
suite du crochet : 26 cas OK ; K8 à blanc avec une chaîne factice vivante : sortie 0.

## Verdict par point

1. **Série et suites : conforme, avec une réserve sur la commande du crochet.** J'ai cloné base-final (tête
   `ead5d5ed6c9ab2c31f29fe3f5abffd9ab9522e96`, `final`) ; `git apply` des trois diffs dans l'ordre passe ;
   `diff -r --exclude=.git` avec `../copie` est vide. Les sommes du générateur passent `sha256sum -c`, tout OK. La ligne
   du job, avec `--egal --plancher 231`, rend `conforme (code 0, résumé final, aucun saut, Ran = 231)` dans l'environnement
   normal comme sous les quatre variables (deux passages sur trois). Le troisième passage sous les variables, à `00:35:45`, a
   rougi : sept échecs, tous dans `test_mutants`, avec le message `campagne refusée`. Un processus de l'hôte répondait au
   motif (voir C-1). La commande du brief `python3 -I -B -m unittest discover -s .claude/hooks/tests -t .` ne se lance pas
   (`Start directory is not importable`). Celle qu'écrit l'en-tête du fichier,
   `python3 -I .claude/hooks/tests/test_garde_faits.py -v`, rend 26 cas OK. Base-final compte 225 cas sous une ligne de
   job à 223 : `refus : Ran 225 > plancher 223 (--egal)`. Elle porte le lot ISOLE-ENV (deux cas, `tests/test_aide_garde.py`),
   qui n'est ni à la tête ni dans aucun INT-xx.diff.
2. **Rouge avant, vert après : conforme.** Les tests seuls sur base-final, sans le code : les six cas rougissent.
   Avec la donnée `motif-chaine.txt` seule, chacun rougit par sa propre assertion. Avec le code : sept cas OK
   (`test_refus_lecteur` compris).
3. **Motif de chaîne : écarts mesurés, corrigés par C-2.**
   - Processus réels qui dorment, dans un espace de PID privé : la forme R-2 réelle, `nohup bash ./x/chaine_int3.sh`,
     `sh chaine.sh`, `bash -c 'bash chaine.sh'`, l'exécution par le nom, `/bin/bash` et `/usr/bin/env bash` sont vus.
   - Ne sont pas vus : `source`, `.`, `bash -l chaine.sh`, `bash -e chaine.sh`, un chemin à espace, `plan.sh`, et le
     modèle lancé en place (`bash scripts/controle/gabarits/chaine-modele.sh`, invisible à R13 (a), à mutants.py et à V7).
   - Le crochet refuse à tort : `grep chaine.sh`, `cat chaine_int3.sh`, `bash -c '. ./chaine.sh'` (le texte du `-c` est
     pris pour un chemin), et surtout `cp <modèle> …/chaine_int3.sh`. Ce `cp` est refusé par `script illisible` parce que
     la cible n'existe pas encore ; c'est pourtant le remède que le refus prescrit et la procédure de lancement de
     l'intégrateur.
   - `cd x && bash chaine_int3.sh` est résolu contre le cwd du crochet et non celui du `cd` : une copie égale dans le cwd
     couvre une chaîne écrite à la main dans `x/`.
   - Justes : `tail -f chaine_int3.log`, `chaine_x.sh.bak`, `machaine.sh`, le `pgrep` de surveillance.
4. **R13 (a) : écarts, corrigés par C-2.**
   - Pendant une chaîne factice, `cargo --version`, `cargo xtask verify`, `cargo --locked xtask verify` et
     `python3 scripts/controle/mutants.py …` sont refusés ; `git status`, `python3 -m unittest` et `cat Cargo.toml`
     passent.
   - Refusés à tort : `grep cargo x.txt`, `grep -n cargo README.md`, `echo cargo`, `ls target/debug/xtask`,
     `git log --grep xtask`. LOURD est cherché sur tous les mots, arguments compris.
   - Une seconde chaîne, copie à l'octet du modèle, est PERMISE pendant la chaîne factice, sous la forme R-2 comme en
     `bash <copie>` : l'exemption `not chaines_lancees` le permet, et aucun cas ne la teste (mutant G2-lourd-exemption
     vivant).
   - La chaîne du modèle elle-même n'est pas gênée par le crochet, ses cargo n'y passant pas ; elle est gênée par C-1.
5. **R13 (b) : conforme sur le fond, écarts de position corrigés par C-2.**
   - Forme R-2 sur une copie à l'octet : permise. Un octet changé, une copie absente, un dossier, un arbre sans modèle :
     refus.
   - Le sha256 lu est celui du modèle de l'arbre du crochet (`RACINE` tiré de `__file__`, l.146). Mesure : un arbre au
     modèle différent, sous `CLAUDE_PROJECT_DIR` = clone, refuse la copie du clone. En service, le crochet est
     `$CLAUDE_PROJECT_DIR/.claude/hooks/garde_faits.py` : c'est le même arbre.
   - `chmod 000` est permis, puisque root lit le fichier.
   - Le modèle lancé lui-même (`bash scripts/controle/gabarits/chaine-modele.sh`) est permis sans jugement, car son nom
     est hors de `CHAINE_SH`, et il est invisible au motif. Le permettre se défend, puisqu'il est sa propre copie à
     l'octet, mais il doit alors être vu comme une chaîne : C-2 l'ajoute au motif et à `CHAINE_SH`. Après C-2, il est
     jugé égal à lui-même, donc permis, et vu par `pgrep`.
6. **R13 (c) : écarts, corrigés par C-3.** Le vocabulaire `GATE_ROUGE` couvre `rougi`, `rougie`, `rougit`, `rougis`,
   `rouge`, `ROUGE`, `VIOLATION`, `violation` (sans casse), plus `refus`, `refusé` ou `refusée` suivi de `par` ou `à` et
   de la gate, une gate, `S-G<n>`, `R-13`, le job ou le crochet.
   - Permis justes : une ligne longue citée telle quelle, lue par Bash ou par Read, ou au milieu d'un résultat de 2 Mo.
   - Refusées à tort :
     - une ligne courte (moins de 60 caractères) suivie de texte, ou placée en fin de message (le JSON ajoute `"}`) ;
     - une ligne à guillemets droits, échappés en `\"` parce que le texte jugé est `json.dumps(inp)` ;
     - les consignes Agent `Rouge avant, vert après : …`, `aucune violation attendue`, `sa ligne ROUGE (trap ERR)`, et
       `Suite verte, aucun rouge`.
   - Admises à tort : `a échoué`, `a refusé le diff`, `failed`, `red`, `refused`, `bloquée par S-G4`, une ligne
     `REFUS K8 : …` inventée sans mot de rougeur, et une ligne vraie suivie d'une inventée (`any`).
   - Mesure sur un journal factice : `outils/mesure6.py`, `out/point6.txt`.
7. **K8 : conforme, avec C-1 et C-4.** J'ai fait un passage à blanc réel : avant_acte de l'état final, dépôt d'essai =
   base-final, plan des trois diffs, sous les quatre variables.
   - Avec le plancher 231 posé au dernier pas : sortie 0 en 73 s. Le coût est une suite, loin sous `BORNE_K8` (1800 s) et
     sous le `timeout 13680` du lancement.
   - Plan sans diff de plancher : `REFUS K8 … Ran 231 > plancher 223 (--egal)`. Plancher d'un rendu à tête 177 :
     `Ran 231 > plancher 229`. Copie sans `enforcement/verdict-suite-s2.py` : `REFUS K8 … can't open file`. K8 rougit
     bien sur un plancher faux.
   - Dans le cas réel, K8 est appelé par la l.21 du modèle pendant que la chaîne vit. Avec une chaîne factice vivante :
     REFUS K8 en 66 s, et la ligne citée est `résumé final absent`, sans nommer le cas rouge (C-4). Avec C-1 à C-4 : sortie
     0 en 79 s.
8. **Mutants : conformes ; deux vivants parmi les miens, couverts par C-2.** J'ai rejoué la campagne par la commande du
   job `controle-unittest`, avec l'outil `mutants.py` de l'arbre relu, sur la copie `mut` (clone, plancher 231), dans un
   espace de PID privé, de `01:05:48` à `01:33:41` UTC.
   - Le témoin est vivant. Les onze du générateur sont tous tués (sortie 1), chacun par le cas qu'il annonce. Le générateur
     les classait par un seul cas et non par la commande du job (consigne SHOGEN-S2BIS-MUT-COMMANDE-1) ; mon rejeu
     confirme ses classements.
   - Miens, tués : G2-motif-sans-ancre (dix ERROR d'import `NameError: name 'Erreur' is not defined`, défaut corrigé par
     C-4), G2-motif-jamais (par le seul `test_e28`), G2-csl-10, G2-csl-site, G2-k8-env.
   - Miens, VIVANTS : G2-motif-sans-sh (aucun cas ne lance `sh chaine.sh` ; C-2 l'ajoute) et G2-lourd-exemption (C-2
     retire l'exemption et la teste).
   - Relevé ps de fin : `aucun processus des 40 groupes de la campagne`. Après la campagne, `diff -r` entre la copie mutée
     et le clone ne montre que la ligne du plancher.
9. **Contrôles des pièces : conforme, sauf le plancher rendu (C-5).**
   - `avant_acte.py --lecture-seule --depot <clone> diff --fichier ../diffs/CAUSES-tous+readme.diff --rapport
     ../RAPPORT-GENERATEUR.md` : sortie 0, avec l'outil de base comme avec celui de l'état final.
   - R-13 du job g5 (motif lu à la l.78 de gates.yml) sur le rapport et D.txt : 0 ligne. presg5 : `0 fragment(s)
     introuvable(s)`.
   - D.txt : les fonctions publiques nommées existent ; les huit empreintes égalent `sha256sum` de `../copie` ; six cas,
     conforme.
   - Plancher : D.txt écrit `<tête + 52>`. Le rendu de `CAUSES-tous+readme.diff` dit 229 (tête 177) alors que la suite
     compte 231. Le juste est 231 = 179 + 52, tête 179 une fois ISOLE-ENV commis, ce que dit le rapport du générateur
     (225 → 231). K8 rougit sur 229.

## Corrections (diffs byte-exacts dans `diffs/` ; chacun s'applique seul sur `../copie`, et les cinq en série, `git apply`)

- **C-1** `diffs/C-1-test-mutants-isole-de-l-hote.diff` (sha256 `ca4ec251eae7c5b9…`).
  - `tests/test_mutants.py` : `lancer(…, chaine=False)` pose un faux `pgrep` en tête du PATH (sortie 0 si `chaine`, 1
    sinon) ; `test_e37` passe par `chaine=` et ajoute l'assertion d'un vrai `bash …/chaine_essai_<pid>.sh` vivant sur
    l'hôte : le témoin doit être joué.
  - Cause : `test_classement_par_la_commande_du_job` et `test_refus_avant_tout_mutant` lançaient `mutants.py` sur le vrai
    `pgrep`. Ils rougissent dès qu'une chaîne vit sur l'hôte (8 échecs, `out/suite-final-sous-chaine.out`), donc dans la
    verif de chaque pas (`unshare -n` seul, même espace de PID) et dans K8 que la chaîne joue à son premier acte (REFUS
    K8, `out/k8-231-sous-chaine.txt`). Base-final, sous la même chaîne factice : conforme, Ran = 225. C'est la régression
    du lot, de la famille d'E39.
  - Rouge avant : la correction mutée (faux pgrep posé seulement si `chaine`) fait rougir `test_e37` à la l.152, sur
    l'assertion de l'hôte.
- **C-2** `diffs/C-2-r13-ab-ce-que-l-acte-lance.diff` (`ed4f2a3455df8170…`).
  - Crochet : `lances()` (programme après enveloppes, script d'un shell, de `source` ou de `.`, arguments d'un `sh -c`,
    script d'un python) remplace l'examen de tous les mots, dans `processus_lourd` et `chaines_lancees`. Une chaîne lancée
    compte comme lot lourd (seconde chaîne refusée). Un relatif après un `cd` est refusé (`chemin relatif après un cd`).
    `CHAINE_SH` et `garde/motif-chaine.txt` admettent les options du shell et `chaine-*.sh` (le modèle en place est vu).
  - Cas complétés : `test_r13_processus_lourd_pendant_une_chaine`, `test_r13_chaine_lancee_hors_du_modele`,
    `test_motif_de_chaine_lu`, sans cas neuf.
  - Rouge avant : 3 échecs (`corr/rb2`) ; vert après.
- **C-3** `diffs/C-3-r13-c-citation-entiere.diff` (`858f4ad3b351b77c…`).
  - Crochet : texte jugé = valeurs brutes de l'entrée (`textes_de`), jamais son JSON. Une citation
    (`VIOLATION chemin:ligne` ou `REFUS <règle>`) doit être, entière, la fin d'une ligne d'un résultat d'outil. Toutes les
    citations sont jugées, même sans mot de rougeur. `GATE_ROUGE` exige un sujet de gate et un mot de rougeur, en français
    ou en anglais (échoué, échec, bloqué, `failed`, `red`, `refused`, `rejected`…).
  - Cas complété : `test_r13_cause_de_refus_sans_la_ligne_de_la_gate` (quatre justes, cinq fautes).
  - Rouge avant : 1 échec (`corr/rb3`) ; vert après. Re-mesure : `out/point6-corr.txt`, sept justes permis et neuf
    fautes refusées.
- **C-4** `diffs/C-4-k8-nomme-le-cas.diff` (`d2cbdee75fa3812b…`).
  - `avant_acte.py` : le refus K8 nomme le premier `FAIL:` ou `ERROR:`, puis la dernière ligne, et son conseil couvre
    variable, `pgrep` et plancher. `MOTIF_CHAINE = motif_chaine()` passe après `class Erreur`, sinon un motif faux lève
    `NameError` à l'import (mutant G2-motif-sans-ancre).
  - Fixture de `test_k8` complétée.
  - Rouge avant : 1 échec (`corr/rb4`) ; vert après.
- **C-5** `diffs/C-5-readme-rendu.diff` (`0c85e124a7408520…`).
  - Bloc README du lot rendu à l'état copie + C-1..C-4 : textes K8, motif, R13 (a)(b)(c) et mutants mis au jour,
    empreintes recalculées (`out/sha-all.txt`), plancher 231, date `2026-10-17 01:43:31 UTC`.
  - `readme/D.txt` de l'intégrateur doit porter le même texte (`<DATE>` et `<tête + 52>` gardés), et le rendu d'aperçu se
    fait à la tête 179.
  - presg5 et R-13 : 0.

Le lot reste à six cas ; le plancher reste 231 après C-1 à C-5.

## Items à former (règle PAROXYSME ; aucun n'est tu)

- I-1. R13 (b) et le motif tiennent au nom : une chaîne nommée autrement (`plan.sh`, `lot.sh`) échappe aux deux (réserve
  R-2 de l'intégrateur). `source` et `.` sont jugés par le crochet après C-2, mais restent invisibles à `pgrep`, comme un
  chemin à espace.
- I-2. Un programme porté par une variable (`C=cargo; $C test`) passe R13 (a).
- I-3. R13 (c), après C-3 : une consigne d'instruction qui unit un sujet de gate et un mot de rougeur (par exemple : si la
  gate rougit, cite la ligne) est refusée. Une citation tronquée ou aux espaces changés est refusée, par choix (ligne
  entière exigée).
- I-4. Deux suites sur un même hôte se gênent. `test_e28` lance un vrai `bash chaine_essai_<pid>.sh` : pendant ce temps,
  R13 (a) d'un autre agent et `mutants.py` voient une chaîne (refus transitoires). Le rouge de `00:35:45` en est un cas
  probable.
- I-5. `avant_acte.py --lecture-seule` écrit `garde/lecture-seule.tsv` dans l'arbre de ses outils, fichier non ignoré par
  `garde/.gitignore` ; ce comportement est antérieur au lot.
- I-6. L'en-tête de `gabarits/chaine.sh` documente toujours le lancement d'une copie de `chaine.sh`, que R13 (b) refuse
  désormais.
- I-7. La commande de la suite du crochet donnée par le brief ne se lance pas : à corriger dans le gabarit de brief.

## Écarts du réviseur

- E-1 (`00:50:27` UTC) : un premier passage de `outils/mesure3.py` a lancé le vrai `chaine-modele.sh` dans l'espace de PID
  privé. Il est sorti à sa l.12 (`PLAN=${PLAN:?…}`, PLAN non posé) avant tout acte : aucun avant_acte, aucun git, aucun
  cargo. J'ai jeté et refait ce passage avec une copie factice qui dort.
- E-2 : ma première chaîne factice (`00:41`:2x → `00:41:35` UTC) vivait dans l'espace de PID de l'hôte. Un passage de l'autre
  réviseur sur du code CAUSES dans cette fenêtre a pu voir une chaîne. Toutes les suivantes ont tourné dans un espace
  privé.
- E-3 : j'ai retiré de `g2/clone` deux artefacts à moi, `garde/lecture-seule.tsv` (I-5) et `.claude/hooks/__pycache__`
  (import du crochet par mesure3) ; `diff -r` le redonne égal à `../copie`. Je n'ai pas enregistré le rôle G2 par
  `oracle_record.py` : le lot est hors du chemin S2.

## Journal de provenance (G1)

- Lu [lu] : `BRIEF-G2.md` ; `../RAPPORT-GENERATEUR.md` ; `../diffs/CAUSES-1.diff`, `-2`, `-3`, `CAUSES-tous+readme.diff`
  (préfixe exact = `CAUSES-tous.diff`, concaténation des trois) ; `../mut-*.diff` et `.out` (onze) ; `../suite-env4*.out`,
  `../suite-normal-2.out` (les sorties `Ran 231`, et le rouge de `suite-env4-2.out`) ; `../SHA256SUMS-generateur.txt`
  (`-c` OK) ; `garde-fous/ERREURS-ORCHESTRATEUR.md` l.68-82 ; `garde-fous/int3/readme/D.txt` ;
  `garde-fous/int3/RAPPORT-INTEGRATEUR.md` §4 ; `garde-fous/int3/ordre.txt`, `planchers.tsv` ; dans `../copie` :
  `avant_acte.py`, `garde/motif-chaine.txt`, `garde_faits.py`, `acte_shell.py`, `mutants.py`, `gabarits/chaine.sh`,
  `chaine-modele.sh`, les quatre fichiers de cas, `gates.yml` (l.78, l.343-369), `verdict-suite-s2.py` (`--egal`).
- Interdits : je n'ai ouvert aucun `docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`,
  `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, `docs/adr-0028/execution/`, `*.jsonl` ni aucune pièce de D.2 ; je n'ai
  fait aucune recherche récursive ni aucune liste par motif sur `docs/`, le dépôt ou le scratchpad.
- Commandes et sorties : toutes consignées dans `NOTES.md`, et les sorties sous `out/` (`suite-*`, `hooks-*`, `rva-*`,
  `point3-*`, `point45*`, `point6*`, `k8-*`, `p9-*`, `corr-all-*`), `mutants/` (`campagne.txt`, `campagne.err`,
  `sortie/`). Mes outils sont sous `outils/` (`juge.py`, `mesure3.py`, `mesure45.py`, `mesure6.py`, `k8.sh`, `r13.py`,
  `sonde.py`), les fixtures sous `fx/`, les arbres de travail sous `corr/`.
- Chiffres recomptés par outil : 225, 231, 223 (Ran et lignes du job) ; 177 + 2 = 179, 179 + 52 = 231, 177 + 52 = 229
  (affichés à `01:45:30`) ; 26 cas du crochet ; 25 `def test_` dans `test_garde_acte.py` ; durées K8 de 73, 75, 70, 66, 79 s
  et 2 s ; 40 groupes au relevé de fin.
