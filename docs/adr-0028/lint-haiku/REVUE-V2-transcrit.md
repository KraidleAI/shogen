# Contre-contrôle et relecture G2 neuve — LINT-HAIKU, vague 2 (transcrit)

> Transcription par l'orchestrateur le 2026-10-08 14:56:51 UTC du rapport rendu par l'agent a36dac130fa3c2c3e (workflow wf_eabb8e95-e1a) ; contrôle FM-1.1 : fragments_l51_l14 = 0 ; modèle résolu au transcript : claude-opus-5-5. Texte de l'agent ci-dessous, sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

**Gate 0 : `claude-opus-5-5`.**
- C'est l'identifiant exact donné par le contexte système de la session, avec le préfixe attendu. L'effort `max` ne se voit pas de l'intérieur.
- Je suis réviseur neuf : je n'ai écrit ni les diffs relus, ni la relecture précédente.
- Horloge (`date -u`) : de 2026-10-08T13:15:55Z à 13:57Z.
- Base : e6657dcc3154bf2d35c69b84d9deae1385e702a7, tête de claude/compassionate-noether-szmdyj, égale à la base du brief.
- `<R>` = `<scratchpad>/lot-haiku/corr/revue`.

## Verdict : ACCEPTE-AVEC-CORRECTIONS (C-1 à C-3)

Le lint (partie lint de LH-1) et la fiche (LH-2) sont acceptés tels quels, sous réserve de Q-1 et Q-2, qui restent à adjuger. Les trois corrections portent sur le runner seul. Elles ajoutent des cas et n'en retirent ni n'en modifient aucun. Chacune répond à un mutant qui survit, qui n'est pas équivalent, et dont un témoin montre l'effet.

| C | fichier:ligne (runner final fa6b4cdf…) | preuve | remède |
|---|---|---|---|
| C-1 | `enforcement/tests/run-fixtures-model-pinning.sh:191-192` : `unset LC_ALL LC_CTYPE`, puis `casl`, qui ne fait varier que LANG ; commentaire l.184-185 | M-01 (`export LC_CTYPE=C`) et M-02 (`export LANG=C`) survivent avec 138 ok, sous P comme sous U. Sous LC_ALL=C.UTF-8, ils admettent `model: claude-opus-5-5 # décision` (sortie 0). Le lint final refuse cette forme partout (sortie 2). | `casl` lance aussi le lint sous `LC_ALL=C.UTF-8`. Les deux passages par LANG restent : ce sont eux qui tuent M-03 et N-06 (LC_ALL non exporté). |
| C-2 | même fichier, l.208-209 (T-125, seul cas du contrôle du commentaire) ; lint l.123 | M-11 ne voit que l'octet collé au `#` ; M-16 oublie la tabulation. Tous deux survivent et admettent `# x<0xFF>` et `<TAB>#<0xFF>`, que la base refusait sous C.UTF-8 et que le final refuse : c'est le desserrement que la compensation devait empêcher. M-10 (`[^[:print:]]`) survit aussi : il refuse `# a<TAB>b`, que la base et le final admettent. | Ajouter T-126 (`model: claude-haiku-5-5<TAB># x<0xFF>`, casl, attendu 2 R-1/hors-liste) et T-127 (`model: claude-haiku-5-5 # a<TAB>b`, casl, attendu 0 1). |
| C-3 | même fichier, l.207 (T-124 n'a qu'un blanc) ; lint l.169-170 (lignes réécrites, E-8) | M-14 (`)*` devient `)?`) admet `agent <U+3000>(` ; la base refusait cette forme sous C.UTF-8. M-15 (`*.cjs` retiré) admet un `wf.cjs` qui appelle `agent(` ; la base le refusait. | Ajouter T-128 (`await agent $U3(…)`, casl, attendu 2 R-1/workflow) et T-129 (`wf.cjs`, attendu 2 R-1/workflow). |

Le remède est éprouvé dans `<R>/tmp/proposition/C1-C3-runner.diff` (21671f83…) :
- **Taille** : +12 −3 lignes, dont 8 de code ; 111 caractères au plus ; octets 92 du runner de 72 à 73.
- **Application** : il s'applique en série après LH-1 et LH-2.
- **Résultat sur le lint final** : 161 ok, sortie 0, sans variable de locale, sous LC_ALL=C.UTF-8 et sous LANG=C.UTF-8.
- **Mutants** : il tue M-01 à M-16 (16 sur 16) ; les lints de base et du premier tour restent rouges.

## 1. Contre-contrôle de C-1 à C-3 (G2 précédente)

| C | état | preuve |
|---|---|---|
| C-1 | soldée | `docs/adr-0028/G0-lot-LINT-HAIKU.md` est cité au lint l.9 et au runner l.14 et l.158. Ce fichier est à verser dans le même commit (G0 §6). |
| C-2 | soldée | T-108 (l.180). R-04, porté sur le lint final, est tué par T-108 seul ; N-03 aussi. |
| C-3 | soldée | T-109 et T-110 (l.181-182), écrits en octal (l.165) ; décodés, ils donnent U+00A0 et U+200B. R-10 est tué par T-109 seul, R-11 par T-110 seul ; N-04 et N-05 aussi. |

## 2. E-LH-1 corrigé

**Code (lint l.45 et l.156-159).** Quand la clé n'est pas exactement `model` et que la valeur vaut exactement `claude-haiku-5-5`, le lint refuse avec `R-1/role`. L'en-tête est conforme au code. Les renvois à CLAUDE.md l.23-49 et l.35-42, et à B.76, sont exacts.

**Runner.** T-100 (l.172) est inversé, par décision écrite. C'est le seul cas existant qui change : depuis la base, 0 ligne retirée et les 96 lignes « cas T- » sont identiques.

**Mes formes hostiles** : 98 sur 98 conformes à des attendus écrits à la main, sous 8 environnements de locale.
- **JSON** : `advisorModel` en haiku est refusé `R-1/role` sous toutes les formes essayées, y compris compacte, sur plusieurs lignes, CRLF, imbriquée, clé répétée et casse de la clé. Les valeurs voisines sont refusées avec leur jeton.
- **YAML** : `advisorModel:` dans un frontmatter n'est pas lu. Haiku y passe, et même l'identifiant banni ou le tier nu, comme sur la base (I-R-2).
- **Hook** : un hook de type prompt en haiku passe (I-a).

## 3. E-LH-5

`export LC_ALL=C` est posé en l.41.

J'ai balayé 1 112 063 points de code, plus les 128 octets isolés :
- Sous C.UTF-8, bash, grep et sed prennent dans `[[:space:]]` les mêmes 15 blancs Unicode. Décodé, le motif BU donne exactement ces 15 points.
- Un octet isolé n'est pris ni par `.` ni par `[^#]` sous C.UTF-8.

Différentiel sur 98 formes à attendu écrit, sous 8 environnements, et 2 465 formes générées, sous 4 environnements. Ces environnements comprennent tr_TR.UTF-8, zh_CN.GB18030 et ja_JP.EUC-JP (compilées par localedef), et un LC_ALL invalide.
- **Indépendance de la locale** : la sortie du lint est identique d'un environnement à l'autre (0 instable).
- **Desserrement** : 0 forme admise de plus que la base, hors haiku.
- **Serrages** : 163, soit le prix E-4 : un blanc Unicode dans un frontmatter, ou un commentaire non ASCII sur une ligne model.
- Ce prix dépasse la compensation stricte : `# décision` était admis par la base sous les deux locales, il est désormais refusé.

**Runner** : 138 ok sous 15 environnements. T-112 est rouge quand la locale du témoin est absente.

## 4. Mutants

Classement par la sortie du runner : 1 tué, 0 vivant, toute autre sortie FATAL. Les résultats sont identiques sous P et sous U.

| campagne | tués | vivants | FATAL |
|---|---|---|---|
| témoin : lint final non muté | — | vivant (138 ok) | 0 |
| mes mutants M-01 à M-16, runner final | 9 | 7 (M-01, M-02, M-10, M-11, M-14, M-15, M-16) | 0 |
| M-01 à M-16, runner proposé | 16 | 0 | 0 |
| rejeu de R-01 à R-15 (G2) et GM-01 à GM-13 (générateur), portés sur le lint final | 28 | 0 | 0 |
| rejeu de N-01 à N-20 (correcteur) | 20 | 0 | 0 |

## 5. Autres contrôles

| contrôle | résultat |
|---|---|
| SHA256SUMS du correcteur | 365 lignes, `-c` OK ; empreinte 1ad073ce… |
| diffs | conformes à SHA256SUMS : LH-1 a987effc…, LH-2 e76eac74… |
| archive de base | c1f09c21… |
| application | `patch -p1` et `git apply --check` passent en série ; lint f2983fb1…, runner fa6b4cdf…, fiche 1974e9f9… |
| forme | 54 lignes de code ajoutées ; 0 ligne de plus de 120 caractères ; 0 TODO/FIXME, CR, tabulation, blanc final ou littéral banni ; octets 92 : lint 43 → 60, runner 48 → 72 ; `bash -n` passe |
| E-LH-3 | runner de base contre le lint final : 95 ok ; fixtures identiques |
| lint de l'arbre | `OK (R-1) : 7 fichier(s)` sous 5 environnements |
| hooks | 54 ok |
| gate des secrets `--tree` | OK |
| s2-harness (`verdict-suite-s2 --egal`) | conforme, 407 tests OK (skipped=2) |
| verify (lignes de verdict seules) | S-G1 à S-G6, S-G7a et S-G8 VERT ; S-G9 ROUGE (1) ; fmt, no_std, clippy VERT ; global ROUGE |
| verify sur la base | mêmes verdicts ; section S-G9 identique, comparée par empreinte sans affichage |

## 6. Confrontation avec le rapport du correcteur

Tous ses chiffres concordent avec mes recomptes. La revue apporte en plus :
- le trou des variables LC_* autres que LANG (C-1) ;
- T-124 et T-125, trop étroits, et le `.cjs` absent (C-2, C-3) ;
- le prix du commentaire, qui dépasse la compensation stricte.

## Écarts

- **Écarts de ma revue** :
  - **ECART-REV-1** : 38 runs FATAL, le runner proposé ayant été lancé hors de son dossier. Campagne invalide, non comptée, relancée.
  - **ECART-REV-2** : un bug de mon harnais a fait marquer toutes les formes instables. Corrigé et relancé.
  - **ECART-REV-3** : des codes de sortie mal lus par `$?` dans un témoin. Témoin refait.
  - **ECART-REV-4** : des barres obliques inverses tapées dans des commandes. Les octets ont été contrôlés (`od -c`, diff, comportement).
  - **ECART-REV-5** : `localedef` (outil du système) a compilé des locales sous `<R>/tmp`, et seulement là.
  - **ECART-REV-6** : je n'ai pas contrôlé l'arbre complet (dossiers exclus compris). Il reste au hook et au job, au commit.
- **Écarts du correcteur** :
  - son E-9, une énumération du dépôt entier, est à juger par l'orchestrateur ;
  - RAPPORT-CORRECTIONS.md n'est pas couvert par son SHA256SUMS ;
  - l'heure de fin diffère entre son rapport (13:12:35Z) et son message (13:14:28Z).
- **Dépôt réel** : HEAD e6657dc, status vide, 6 fiches. Aucune écriture git ; je n'ai ouvert ni pièce de D.2, ni `*.jsonl`, ni dossier interdit.

## Items à former

- **I-R-1** : `"model": "claude-haiku-5-5"` dans les réglages JSON fixe le modèle de la session principale, donc de l'orchestrateur, qui décide. La lettre de E-LH-1 l'admet, mais c'est contraire au roster (CLAUDE.md l.41-42). À porter au G0 de Q-3.
- **I-R-2** : `advisorModel:` n'est pas lu dans un frontmatter, et même le banni y passe.
- **I-R-3** : le lint ne voit pas un appel `agent(` séparé par U+00A0, U+2007, U+202F ou U+FEFF, qui sont pourtant des blancs pour JS.
- **I-R-4** : une variante du contrôle du commentaire qui refuse seulement l'UTF-8 invalide compenserait sans refuser `# décision`.
- **Toujours ouverts** : I-a, I-c, I-e et I-f du correcteur ; I-2, I-3, I-4 et I-5 de la G2.

## Avis sur les questions

- **Q-1** : garder le refus des blancs Unicode. Pour le commentaire, garder la règle actuelle ou la restreindre à l'UTF-8 invalide (I-R-4) ; dans les deux cas, figer les deux bornes (C-2).
- **Q-2** : garder.
- **Q-3** : oui, ouvrir un G0 : hook de type prompt, `model` des réglages JSON, fiches de rôle G2.
- **Q-4** : garder T-112.

## Fichiers

Tous sous `<R>` :
- `RAPPORT-REVUE.md` : sha256 2b2d399cfe45411aaac0efc7d6e6ba2c31958b20a5a1d34da1ac79e923ad04ee.
- `SHA256SUMS` : 187 lignes, `sha256sum -c` OK, empreinte 602ccc326e9047797bb4eb43f2045e09cb0c554609f325f286765906c31c5605. Il couvre tout sauf lui-même et le rapport.
- `NOTES.md`, journal de provenance compris.
- `tmp/proposition/C1-C3-runner.diff` et `tmp/proposition/run-fixtures-model-pinning.sh` (e678f152…) : le remède.
- `logs/` : campagnes, formes hostiles, témoins, verify.
- `scripts/` et `mutants/` : mes outils et mes mutants.
