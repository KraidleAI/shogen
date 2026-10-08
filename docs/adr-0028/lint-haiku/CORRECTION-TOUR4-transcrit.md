# Corrections du tour 4 du lot LINT-HAIKU (transcrit)

> Transcription par l'orchestrateur le 2026-10-08 18:42:05 UTC du texte écrit par l'agent a7b8f730edf0a532e dans `<scratchpad>/lot-haiku/corr3/RAPPORT-CORRECTIONS.md` (sha256 d18d5ee7…) ; contrôle FM-1.1 de son transcript : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte de l'agent ci-dessous, sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Tour 4 — corrections après la revue du tour 3 (2026-10-08, de 17:40:03Z à 17:58Z, `date -u`)

**Gate 0 : `claude-opus-5-5`.** C'est l'identifiant exact donné par le contexte système de la session ; l'effort `max` ne se voit pas de l'intérieur.

- Base des diffs : e6657dc. Tête nommée : b46672b0, qui est aussi HEAD du dépôt réel à 17:43Z et à 17:56Z (status vide, 6 fiches, pas de fiche extracteur).
- e6657dc est l'ancêtre de b46672b0 ; aucun fichier n'a changé sous `enforcement/`, `.claude/`, `.github/` ni `CLAUDE.md`.
- Aucune écriture git, aucun `.claude/` créé, ni pièce de D.2, ni `*.jsonl`, ni Pocket ; `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée.

## C-1 à C-3 : soldées, selon l'adjudication

| C | correction | rouge montré |
|---|---|---|
| C-1 (remède R1) | QS, FB et FLS sont retirés. FL passe à 1 dès qu'une ligne précédente du même frontmatter porte `[` ou `{` (FO, à toute place), et n'est jamais remis à 0 dans le fichier ; il est posé après le jugement de la ligne. `RX` revient à sa place de la base. L'en-tête dit ce que fait le lint, PyYAML 6.0.1 restant la référence écrite. T-152 est inversé (décision écrite) ; T-156, T-157, T-160 et T-161 sont ajoutés. | contre le lint du tour 3 : T-152, T-156, T-157, T-160, T-161 |
| C-2 | SIGX lit l'échappement `u00` de la minuscule ou de la majuscule (`${c^^}`) ; T-158 (`CL<u0041>UDE-H<u0041>I<u004B>U-5-5` sous `env`, décodé `CLAUDE-HAIKU-5-5` par json.load). | contre le lint du tour 3 ; seul tueur de PV-05 |
| C-3 | T-159 (`model: claude-opus-5-5 # x<FF> # y`, casl, 2 R-1/hors-liste). | seul tueur de V-20 (×4 locales) ; base sous POSIX |

**Cas que j'ajoute (serrage).** Chacun est rouge contre un mutant neuf qu'il tue seul :
- T-162 : `model: claude-haiku-5-5 # cf. [B.76]` est admis, car la ligne `model` ne se juge pas sous ses propres crochets (N4-01) ;
- T-163 : un ouvrant après un dièse qui n'ouvre pas de commentaire (`  a#b: [`), refusé `R-1/role` (N4-02) ;
- T-164 : `# a # x<FF>` est refusé hors-liste : le commentaire se lit jusqu'à la fin de la ligne (N4-05).

**Lectures PyYAML 6.0.1** (mesure seulement) : T-156, T-157, T-160, T-161 et T-163 sont lus imbriqués ; T-152 et T-162 au premier niveau.

## Diffs, à appliquer en série sur e6657dc (et sur b46672b : fichiers identiques)

| pièce | sha256 | lignes | code ajouté | octets 92 |
|---|---|---|---|---|
| `diffs/LH-1.diff` | 3a3ea99c465a6452681a34ab2de3926b8395449ce1a4ac44d054660fb257c546 | +180 −9 (lint +61 −9, runner +119 −0) | 31 + 89 = 120 (≤ 200) | lint 43 → 98, runner 48 → 146 |
| `diffs/LH-2.diff` | e76eac740293e9eaa0958aefc84208bac6cb3799c53631a8dc86c2317d68d6ec | +34 (inchangé) | texte | 0 |

- **Fichiers obtenus** : lint 5373b681…, runner ea390e12…, fiche 1974e9f9….
- **Forme** : 119 caractères au plus ; aucun TODO/FIXME, CR, tabulation, blanc final ni littéral banni ; `bash -n` passe ; `patch -p1` et `git apply` en série hors dépôt donnent des fichiers identiques.
- **Écriture** : constructeurs sans octet 92. Les octets écrits ont été contrôlés : SIGX affiché par le lint lui-même, U8 inchangé (`cmp`), JSON de T-158 vu par `od -c`.
- **Archive** : le LH-1 du tour 3 est gardé dans `logs/tour3-LH-1.diff` (fdedb729…).

## Résultats

| contrôle | résultat |
|---|---|
| runner livré | 227 ok, sortie 0, sous les 19 environnements de la revue et sous LC_ALL=POSIX et C.UTF-8 |
| rouge | contre le lint du tour 3 : 6 échecs d'assertion ; contre la base : 68 ; T-152 et T-156 à T-164 ont chacun un rouge (`logs/t4-table-rouges.txt`) |
| mutants (P et U) | 56 sur 56 tués, 0 FATAL, témoin vivant : les 33 de la revue portés (dont V-20, tué par T-159 seul, et PV-05, par T-158 seul), 18 du tour 3, 5 neufs (N4-01 à N4-05) |
| mutants sans objet | V-09 à V-12, V-23 et V-27 (QS, FB et FLS retirés) |
| lint de l'arbre | `OK (R-1) : 7 fichier(s)` sur e6657dc et sur b46672b, sous 5 environnements |
| prix de R1 sur les fiches | 0 sur 7, sur les deux arbres : aucune ligne de frontmatter ne porte `[` ou `{` ; un témoin `argument-hint: [x]` est bien compté |
| fuzz à oracle PyYAML (3 000 formes, graine 4) | lint du tour 3 : 5 formes imbriquées admises ; tour 4 : 0 sur 21 ; prix : 76 premiers niveaux refusés sur 181 |
| E-LH-3 | 95 ok ; fixtures et cas T-01 à T-95 identiques ; 0 ligne retirée du runner |
| hooks | 54 ok |
| s2-harness | Ran 407, OK (skipped=2) ; `--egal` conforme |
| verify | identique à la base (S-G9 ROUGE, même empreinte) |

**Mutants neufs.**

| id | mutation | tué par |
|---|---|---|
| N4-01 | la ligne `model` se juge sous ses propres crochets | T-162 seul |
| N4-02 | ouvrants après un dièse ignorés (`${x%%#*}`) | T-163 seul |
| N4-03 | FL remis à 0 par une ligne dont le dernier crochet est un fermant | T-149 à T-151, T-156, T-157, T-161 |
| N4-04 | FO élargi aux parenthèses | T-96, T-153, T-162 |
| N4-05 | commentaire lu jusqu'au dièse suivant | T-164 seul |

## Écarts

- **E-14** : T-162 à T-164 vont au-delà de la liste de l'adjudication. Ce sont des serrages motivés par des mutants.
- **E-15** : mon code de SIGX et de FO coïncide presque mot pour mot avec R1. C'est la forme directe de la règle adoptée. Je l'ai écrit par mes constructeurs et prouvé par mes cas et mes mutants.
- **E-16** : les tâches détachées ont été lancées par `setsid -f`. Leur fin est constatée par les fichiers `.fin`, mais leur PID n'est pas relevé : le `pgrep` attrapait aussi mon propre shell.
- **E-17** : un recompte a d'abord été lancé avec `-W error`, qui a émis du bruit (ResourceWarning). Le journal a été réécrit sans cette option.
- **E-18** : le fuzz donne 2 651 formes invalides sur 3 000. C'est un complément, pas la preuve principale (la revue en couvrait 1 101 imbriquées).
- **E-19** : `reconstruire4.sh` est dérivé de `reconstruire.sh` par sed ; ce dernier porte des barres de continuation tapées. Contrôle : `bash -n` et sorties vérifiées.
- **E-20** : un `grep` d'octets 92 sur `envs4.sh` a échoué (« Trailing backslash »). Le compte fait par Python donne 0.

## Items à former

- **I-R3-1** : quel lecteur fait référence, PyYAML ou celui de Claude Code ?
- **I-R3-3** : prix de R1. Aucune fiche n'est touchée à b46672b ; une commande dont `argument-hint: [x]` précède `model:` serait refusée.
- **I-R3-4, L-1, I-R-2, I-2, I-c, I-d, I-R-3, I-e, I-f, I-3, I-4, I-5** : toujours ouverts.

## Provenance (G1)

**[lu] en entier :**
- `corr3/REVUE-transcrit.md` ;
- `corr3/revue/RAPPORT-REVUE.md`.

**[lu], données :**
- `revue/proposition/R1/C1-C3.diff` ;
- les diffs des mutants de la revue (`revue/mutants/`, `revue/mutants-prop/`) ;
- `revue/logs/mutants3-liste.tsv`, `revue/scripts/envs.sh`, `revue/logs/runner-prop-envs.tsv`.

**[abs] :** le lecteur de Claude Code, Git Bash, la locale du job.

Les commandes et leurs sorties sont horodatées dans `NOTES.md` (section « Tour 4 ») et dans `logs/t4-*`, `logs/campagne4*`. Tous les chiffres sont recomptés par mes scripts (`scripts/*4*.py`, `scripts/*4.sh`, `scripts/sonde_tour4.py`, `scripts/fuzz4.py`, `scripts/prix_fiches.py`, `scripts/table_rouges4.py`).

## Fichiers (sous `corr3/`)

- `diffs/LH-1.diff`, `diffs/LH-2.diff` ;
- `mutants4/` (56 `.sh` et `.diff`, `INDEX.tsv`) ;
- `tmp/final4` (e6657dc + diffs), `tmp/tete4` (b46672b + diffs) ;
- `SHA256SUMS`, recalculé après ce rendu : il couvre ce rapport, `NOTES.md`, `diffs/`, `scripts/`, `logs/`, `mutants/`, `mutants4/`, les deux transcriptions, `revue/SHA256SUMS`, les deux archives et les fichiers de `tmp/final4`. Son empreinte est dans le message de retour.
