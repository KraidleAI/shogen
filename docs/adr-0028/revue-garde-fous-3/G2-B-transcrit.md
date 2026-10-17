# Relecture G2 neuve du groupe B (transcrit)

> Transcription par l'orchestrateur le 2026-10-17 07:31:23 UTC du fichier garde-fous/p3b/g2/RAPPORT-G2.md ; contrôle FM-1.1 du transcript du réviseur G2 par le fm11.py versé : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5 (278 occurrences, aucune autre). Texte ci-dessous avec 2 retouche(s) (E35, E38) : noms de marqueur de dette et locutions de la gate S-G4 cités en clair, mis en code, segments de code à doubles accents graves réécrits en segments simples, heures sans date dans les 25 caractères ou approchées mises en code ou entre guillemets français, sans autre changement (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Relecture G2 — GARDE-FOUS phase 3, groupe B (crochet GARDE-FAITS et `avant_acte.py`)

- **Gate 0** : modèle `claude-opus-5-5` (effort `high`), worker `shogen-worker`, réviseur distinct du générateur.
- Brief : `g2/BRIEF-G2.md` (orchestrateur, 2026-10-16 14:42:24 UTC). Relecture du 2026-10-16, de 14:42:34 à
  `15:32:20` UTC (`date -u`).
- Rattachement : ADR-0028, annexe B, B.108 (l.1873, 1878, 1879, 1880) et B.109 (l.1891), lignes relues à la tête.
- Tête du dépôt : `fe9a72b0503758d7c0e19f1e9a928a5e6d0f3878` ; base du générateur `fddedcf`. Le commit qui les
  sépare ne touche aucun chemin des diffs (`git diff --stat fddedcf fe9a72b -- <onze chemins>` vide).
- Série relue (empreintes contrôlées par `sha256sum -c ../SHA256SUMS`, 13 OK) : `B-1` à `B-5`, concaténation
  `2fe76b3cdaa8e076189bdedb1aa1e52a39f4477961f39973ce433195a8333294` (recalculée, égale à celle du générateur).

## Verdict : ACCEPTE-AVEC-CORRECTIONS (C-1 à C-5, liste fermée)

La série fait ce que les cinq items demandent, s'applique telle quelle sur la tête et garde la suite verte (Ran 191,
plancher de la tête 177 + 14). Elle a pourtant quatre défauts et deux mutants vivants (G-3, G-5), qui bloquent
l'acceptation en l'état. Les cinq corrections sont écrites en diffs byte-exacts, à appliquer après `B-5` dans l'ordre
C-1 à C-5. Chaque correction a son test rouge avant et vert après, ou son mutant tué quand c'est une garde. Aucune
correction n'ajoute de méthode de test : le plancher reste 191. La suite du job sur la copie corrigée rend
`conforme (code 0, résumé final, aucun saut, Ran = 191)` (`preuves/suite-corrigee.txt`).

| C | diff (`g2/diffs/`) | défaut corrigé | se rattache à | + / − | sha256 |
|---|---|---|---|---|---|
| C-1 | `C-1-lecture-pure.diff` | `lecture_pure` tient pour lectures trois actes qui écrivent ou exécutent ; arrêt sous erreur interne non testé (G-5 vivant) | B-1 | 25 / 7 | `c0df33f1986a698ee8dee759a81675cf496eb5178090cd974e2358201881af52` |
| C-2 | `C-2-marque-humain.diff` | un refus du crochet relayé dans un message `user` compte comme texte humain (R5, R6) | B-2 | 15 / 1 | `85dd3b452a22ac306495109196c4a4cee14f3ac7bdd09a06789233f883898273` |
| C-3 | `C-3-r12-apres-r6.diff` | R12 n'est jamais jugée quand R6 ou R10 refusent d'abord ; au second arrêt, tout passe | B-3 | 17 / 2 | `1bc7a5dc548e7e2d974ea541268d26cec44cfe64a68c19b5c98be5d6209f16cd` |
| C-4 | `C-4-r12-comptes.diff` | R12 refuse un compte lu par `wc -l` (faux refus, contraire à R5 C-6) | B-3 | 18 / 1 | `d5758a9c88cdbacce3ee82d1fdadbabd3d24d2c989430d4f0676bea6a668f492` |
| C-5 | `C-5-garde-piece-porte.diff` | regard avant du nombre de `piece_porte` gardé par aucun cas (G-3 vivant) | B-3 | 8 / 0 | `a4bf854a26256edfec6193ee1cd512ad0f496452681d78e8403ecb7bd31ab5f5` |

Concaténation C-1 à C-5 : sha256 `d181e070196bd3938c774afbc1695e20e6741993ec417c48df5f89ae57bd11cb`. Les cinq diffs
appliqués par `git apply` sur l'état `B-5` donnent l'arbre de la copie corrigée (`git diff --stat` vide). Chacun passe
`avant_acte.py diff` à sortie 0 (`preuves/avant-acte-diff-c.txt`). Le motif R-13 du job g5 trouve 0 ligne ajoutée.
`presg5` trouve 0 fragment dans le README corrigé.

## Checklist

### 1. Application sur la tête, lignes, plancher : conforme
Les cinq diffs s'appliquent dans l'ordre sur la tête `fe9a72b` (`git apply --check`, puis `git apply`, un commit
jetable par pas ; `g2/copie`). Aucun ne s'applique mal. Les insertions au milieu d'un fichier touchent
`garde_faits.py`, `avant_acte.py`, `test_avant_acte.py` et `.gitignore`. Aucun de ces fichiers n'est cité par numéro
de ligne (`garde/lignes-citees.txt`). Le README n'est touché qu'en fin de fichier : `avant_acte.py diff` passe à
sortie 0 sur chaque pas à la tête, C7 compris (`preuves/avant-acte-diff.txt`). Plancher : 177 à la tête,
191 après `B-5`, soit 177 + 14. La ligne exacte du job `controle-unittest` sur la copie finale rend
`conforme (code 0, résumé final, aucun saut, Ran = 191)`, sans aucune ligne `Exception ignored` ni `Warning`
(`preuves/suite-serie.txt`).

### 2. B-1, erreur interne : trois actes échappent ; limite d'entrée non exploitable → C-1
Les quatre familles que nomme le brief sont bien refusées sous erreur interne : redirection (`cat a > b`, `cat <>b`),
`tee`, `python3 -c "open('b','w')"` et outil MCP qui écrit (`mcp__github__create_or_update_file`)
(`preuves/sonde-lecture-pure.txt`). Trois autres actes passent pour des lectures pures, mesurés par
`acte_qui_ecrit` sur le crochet de la série :
- `echo x >&1b` et `cat secret >&2copie` : le motif `[0-9]?>&[0-9]` (`garde_faits.py:917` à l'état `B-5`) ôte `>&1`
  sans regarder la suite. Or bash lit `>&1b` comme une redirection vers le fichier `1b` : mesuré, `echo x >&1b` crée
  `1b` (sortie 0, `g2/tmp/bac`).
- `./cat NOTES.md`, `/tmp/x/git status`, `cd /tmp/x && ./ls` : `os.path.basename(mots[0])` (`:924`, `:931`) admet
  tout programme dont le nom de base est une lecture, même un script posé par l'agent.
- `printf -v PATH /tmp/x ; cat a` (et `printf -v HOME … ; git log`) : `printf -v` affecte une variable que les
  commandes suivantes lisent. `cat` et `git` résolus par un `PATH` choisi exécutent n'importe quoi.

Rejeu sur le crochet entier, en processus neuf, sous journal illisible (`preuves/rejeu-crochet-serie.txt`) : ces trois
commandes sortent 0, alors que `git commit -m essai` sort 2. Ce n'est pas une régression : à la tête, toute commande
sortait 0 sous journal illisible (`preuves/rejeu-crochet-tete.txt`). B-1 ne ferme donc pas l'item en entier.

Cas réel de la G2 CQ-1, rejoué sur le crochet entier. La `ValueError` est rétablie dans `hote_forge` (l'erreur
d'avant CQ-1, réelle et non un double). À la tête, `curl 'http://[' ; git commit -m essai` sort 0 avec
`erreur interne (ValueError('Invalid IPv6 URL')) ; acte permis sans contrôle.` Avec la série, il sort 2 avec
`REFUS. erreur interne (ValueError('Invalid IPv6 URL')) pendant le jugement d'un acte qui écrit…`. Le cas est fermé.

Limite `entrée JSON non objet sort 1` : mesurée (`preuves/entree-non-objet.txt`). `[]`, `null` et `5` sortent 1, une
entrée non JSON sort 0. Un objet dont `transcript_path` est un entier sort 1 aussi, même pour un `git commit`
(`TypeError` levée avant le `try`). Ce n'est pas un trou exploitable : l'entrée du crochet est écrite par Claude Code,
non par l'agent, qui ne choisit que `tool_input` (une valeur non objet y est gérée : `acte_qui_ecrit` rend vrai).
Item à former (I-1) : calculer `ev` et `dossier` dans le `try`.

Les journaux des sous-agents sont bien trouvés. B-1 refuse désormais tout acte qui écrit quand le journal est
illisible : un chemin faux pour les sous-agents les bloquerait tous. Or `pre_tool_use` rend 0 avant toute règle quand
le journal est illisible. Les refus R7 et R5 reçus par le générateur, un sous-agent (ses écarts E-4 et E-6), montrent
donc que son journal était lu.

### 3. B-2, message à contenu chaîne, effet sur R6 : pas de régression d'E29 dans la série ; défaut voisin → C-2
Mesure du crochet entier au Stop (`preuves/sonde-stop.txt`), à la tête, après B-2 seul, puis sur la série :
- `28 jours` sans pièce ni 28 affiché : R6 refuse dans les trois états.
- l'humain a tapé `J28`, la réponse dit `28 jours` : la tête refuse (R6), B-2 seul permet (R6 couvre 28 par `J28`), la
  série refuse (R12). R6 recule donc d'un cran : un nombre tapé par l'humain couvre le même nombre de la réponse. Ce
  desserrage est celui que R6 écrit (`faits + humain`) et celui de la forme liste, déjà en vigueur. E29 reste tenu par
  R12 (l'unité doit être sur la ligne de la pièce).
- l'humain a tapé `16 semaines ?` : la tête refuse (R6), B-2 et la série permettent (attendu).
- l'humain a tapé `2026-10-07`, la réponse dit `7 jours` : la tête permet (le chiffre 7 isolé par le découpage), B-2
  et la série refusent : c'est le serrage qu'annonce le générateur.

Le README de B-2 n'écrit que le serrage, et sa formule (`un chiffre isolé`) se lit à l'envers. C-2 écrit les deux
effets mesurés.

Défaut voisin, mesuré (`preuves/sonde-marque.txt`) : la docstring de R5 dit `les refus de ce crochet ne comptent pas`.
Mais `faits_et_appels` (`garde_faits.py:203-204`) range dans `humain` tout texte d'un message `user`, sans écarter la
marque `GARDE-FAITS`. Prenons un message `user` qui relaie `GARDE-FAITS : REFUS. R5 : 4f3e2d1 …`, puis un Write de
`BRIEF-x.md` qui écrit `4f3e2d1`. La tête refuse ce Write sous la forme chaîne, mais le permet sous la forme liste.
Après B-2, il passe sous les deux formes : B-2 étend à la forme chaîne un défaut de la forme liste. C-2 écarte la
marque dans les deux formes (serrage).

### 4. B-3, R12 : deux défauts → C-3 et C-4 ; une limite à former
Cinq réponses réalistes, et quelques autres, jouées sur le crochet entier (`preuves/sonde-stop.txt`, puis
`preuves/sonde-stop-corrige.txt`) :

| réponse | pièce du tour | série | corrigé |
|---|---|---|---|
| `La série compte 5 commits.` | `git log --oneline … \| wc -l` affiche `5` | refus R12 (faux) | permis (C-4) |
| `Plancher : 191 tests, tous verts.` | `Ran 191 tests …` | permis | permis |
| `3 items sur 5 fermés, soit 60 % d'avancement.` | `grep -c` affiche `2` | refus R6 (3) | refus R6 et R12 (60 %) |
| `Les 5 diffs touchent 11 fichiers.` | `11 files changed, …` | refus R6 (5 diffs) | refus R6 |
| `La suite compte 1 715 tests.` | `Ran 1715 tests` | refus R12 de `715 tests` (faux) | inchangé (I-2) |
| `La G2 a duré 25 minutes.` | `date -u` | refus R6 | refus R6 et R12 |

Le compte lu par `wc -l` est un faux refus, contraire à la règle que R5 tient depuis la G2 du groupe A, C-6 : un compte
affiché seul par une commande de comptage est un compte lu. L'item écrit aussi `avec son unité ou son contexte` :
le contexte d'un compte est sa commande. C-4 admet ces comptes pour les commits, les tests et les fichiers, jamais pour
une durée ni un pourcentage. Les nombres dérivés (60 %, 25 minutes) restent refusés : c'est la règle voulue, rien de
mémoire. Les milliers (`1 715 tests`, refusé sous le nom `715 tests`) sont un faux refus, donc dans le sens sûr :
item I-2.

Fenêtre `depuis le dernier message humain` : adaptée. Elle exige une relecture à chaque tour, ce que veut E29 (rien de
mémoire). Elle est bornée par `tour_humain`, qui écarte les refus du crochet et les rappels du système, et qui suit les
messages mis en file. Une réserve n'est pas mesurable ici : une notification du harnais enregistrée comme message
`user` à contenu chaîne, sans `isMeta`, ouvrirait un tour neuf. Le vérifier demanderait de lire un journal `*.jsonl`,
ce qui est interdit (item I-3).

`Au second arrêt du tour, passage consigné` : deux arrêts font bien passer, comme pour R6 et R10. Pris seul, ce n'est
pas un contournement propre à R12 : le premier arrêt est refusé avec la demande de lecture, et le second est consigné
(`PASSAGE R12` au journal des décisions). C'est la garde contre une boucle d'arrêts refusés. Le contournement réel est
ailleurs. Dans `main` (`garde_faits.py:968-969`), R12 ne se juge que si R6 et R10 laissent passer. Une réponse qui
porte un nombre non affiché (R6) et une durée sans pièce (R12) reçoit donc le refus R6 au premier arrêt, puis passe au
second : la demande de R12 n'est jamais faite. Mesuré : `Il reste 28 jours ; 123 cas.` avec `28` affiché sans unité,
puis `Pour Pocket, il reste 28 jours.` après un message qui nomme CoinGecko (R10). C-3 juge R12 au premier arrêt dans
tous les cas et ajoute les refus. Item I-4 : rendre le passage du second arrêt visible à l'humain (message du crochet
au Stop), à vérifier contre la documentation de Claude Code (aucun réseau ici).

### 5. B-4, journal de lecture seule : conforme
L'écriture est un ajout (`open(…, "a")`), une ligne par appel, en un seul `write` court. Ce n'est pas un écrit
atomique par renommage, et il n'en faut pas pour un journal en ajout. Le fichier n'est jamais versionné : il est ignoré
par la ligne ajoutée au `.gitignore` de la racine. Il est absent du dépôt (`test -e` : absent). `git status
--porcelain`, que lisent `avant_acte.py:215` et `gabarits/chaine.sh:45`, ne le voit pas : aucun des deux ne passe
`--ignored`. Le test `test_journal_ignore_par_git` lit le vrai `.gitignore`, et le mutant M4-5 est tué.
La sortie 3 quand le journal n'est pas écrit suit le contrat 0, 1, 3 : c'est une erreur de l'outil, jamais 0. Elle
peut masquer un refus (1 → 3), mais une chaîne s'arrête sur l'un comme sur l'autre.
Remarque sans correction : dans `test_passages_journalises`, la première affectation `avant = self.etat()` n'est
jamais lue. L'intégrité du dépôt lu n'est vérifiée qu'après le refus et `sceller`.

### 6. B-5, disque du dépôt : conforme ; la skill est un item à former
`lieux_disque` mesure `realpath(--depot)`, puis TMPDIR si `st_dev` diffère. `GC.etat_disque` lit
`shutil.disk_usage`, qui appelle `os.statvfs` au moment de l'appel : le double des tests est donc bien vu. Le modèle de
chaîne appelle `acte disque`, et `acte()` passe `--depot "$DEPOT"` (lu dans `gabarits/chaine.sh`). Aucun autre appel ne
mesure `/` : `etat_disque` n'a pas d'autre appelant que `disque` (recherche dans `.claude`, `scripts`,
`enforcement`). Les cas existants de `test_e4_disque` comparent un préfixe de la sortie : ils restent justes si TMPDIR
est sur un autre système de fichiers.
Skill `shogen-avant-lancer`, point 1 (`df -h /`, puis `avant_acte.py disque`) : le contrôle qui décide est la
sous-commande `disque`, désormais juste. `df -h /` n'est qu'un affichage, et la consigne vient d'E4, reprise dans les
briefs : la changer touche la règle des briefs, hors des diffs. C'est donc un item à former (I-5), non une correction.
Remarque : la docstring d'`avant_acte.py` dit encore `refus sous 3 Gio libres sur /` (l.37). Le paragraphe ajouté en
fin de docstring la contredit, ce qui suffit pour un fichier non cité par numéro.

### 7. Mutants : 15 du générateur tués ; 2 des 5 du réviseur vivants → C-1 (cas Stop) et C-5
Campagne A, sur la série (`g2/copie-mut`, outil `g2/tete/scripts/controle/mutants.py`, job `controle-unittest`, borne
300 s, groupes neufs, lancée détachée) : témoin vivant. Les 15 mutants repris du générateur sont tous tués (sortie 1) :
M1-1, M1-2, M1-3, M1-6, M1-9, M1-10, M2-1, M3-1, M3-3, M3-5, M3-7, M4-1, M4-4, M5-1 et M5-4 (B-1 et B-3 compris). Le
réviseur en ajoute cinq, G-1 à G-5 : trois sont tués (G-1, G-2, G-4) et deux vivent. Aucun FATAL. Relevé de fin :
aucun processus des 42 groupes.
- G-3 vit : le regard avant de `piece_porte`, retiré, laisse `280 jours` ou `28,5 jours` couvrir `28 jours` sans
  qu'aucun cas ne rougisse. C-5 ajoute ce cas.
- G-5 vit : sans la condition `ev == "PreToolUse"`, une erreur interne au Stop devient un refus. La table de B-1 le
  permet, mais aucun cas ne le jouait. C-1 ajoute ce cas.
Campagne B, sur la copie corrigée (`g2/copie-mut-b`) : K-1 à K-12, mutants des corrections, sites d'appel compris ;
K-11 et K-12 sont G-5 et G-3 rejoués sur la copie corrigée. Témoin vivant, 12 tués sur 12 (sortie 1), aucun vivant,
aucun FATAL ; relevé de fin : aucun processus des 26 groupes.

### 8. Écarts du générateur : conformes
- Pièces interdites : les copies du générateur sont faites par `git archive` sur une liste explicite, qui n'a aucun
  interdit (`../NOTES.md`). Les fichiers suivis sous les cinq dossiers interdits nommés sont au nombre de 0 dans
  `verif/` et dans `copie/` (`git ls-files -- <chemins explicites> | wc -l`). Aucun `*.jsonl` n'est ouvert.
- Espaces insécables (E-1) : 0 U+00A0 et 0 U+202F dans les lignes ajoutées des cinq diffs, recompté par script. `BLANC`
  est écrit par `chr()`.
- `sed -i` sur `/dev/null` (E-3), refus R7 (E-4), refus R5 (E-6) : sans effet sur l'arbre.
- Arbre du dépôt : `git status --porcelain --ignored -- <liste explicite>` ne montre que
  `!! enforcement/__pycache__/`, daté du 2026-10-10 (`stat`), donc antérieur au lot. `lecture-seule.tsv` est absent.

### 9. S-G5 et R-13 : conformes
Le motif R-13 est extrait de `gates.yml` par script. Son sha256
`a1a6e6842def9f47f6715203dfae6347c7d51fec08da5db7c2474712527bba71` est égal à celui du générateur. Il trouve 0 ligne
ajoutée dans B-1 à B-5 et dans C-1 à C-5, ainsi que 0 ligne dans ce rapport et dans `NOTES.md`. `presg5` trouve 0
fragment dans le README de la tête et dans le README corrigé. Aucun texte anglais entre « » dans les diffs ni dans ce
rapport : les messages d'outil sont en code.

### 10. Conflits avec les groupes A et C : ce qui dépend d'autre chose que les lignes annoncées
- `avant_acte.py`, `main` : B-4 la scinde en `main` et `_jouer`. Tout diff d'un autre groupe qui touche le corps de
  `main` (fautes, `journal`, `ExitStack`) entre en conflit au-delà du plancher et du README.
- `avant_acte.py`, `disque` (B-5) et fin de la docstring du module (B-4, B-5) : conflit textuel si un autre groupe
  ajoute un paragraphe en fin de docstring.
- `garde_faits.py` : fin de la docstring du module (B-1, B-3), `main` (B-1, B-3, C-3), `faits_et_appels` (B-2, C-2),
  bloc ajouté avant `main` (`BLANC` à `acte_qui_ecrit`).
- Tests : `test_lecture_seule_journal.py` dépend de `ta.Source`, de `ta.DiffDeWorker.diff_de` et `.etat`, de
  `ta.LECTEUR`, d'`indexer` et d'`horloge`. `test_disque_depot.py` dépend de l'API de `ta.Depot` (`lancer`, `d`,
  `tmp`) et de l'environnement vidé par `setUp`. Un changement de ces aides par A ou C les casse sans toucher
  `Depot.setUp`.

## Corrections (texte exact : les diffs ; résumé)

**C-1 — `.claude/hooks/garde_faits.py:907, 917, 924, 931` (état `B-5`), README (table de B-1), test.**
Les trois changements :
- `>&N` n'est ôté que suivi d'un blanc ou d'un séparateur : `[0-9]?>&[0-9]+(?![^\s;&|])` ;
- le programme se lit nommé sans chemin : `mots[0] == "git"`, `mots[0] not in LECTURE` ;
- `printf` sort de `LECTURE`.

La docstring de `lecture_pure` et la table du README sont mises à jour, à nombre de lignes égal, et un ajout daté est
posé en fin de README. Le test `test_table_des_cas` reçoit cinq refus de plus : `echo x >&1b`, `cat a >&2copie`,
`./cat a`, `/tmp/x/git status`, `printf -v PATH /tmp/x ; cat a`.
Rouge sur la série : `(0, True) != (2, True)` sur `echo x >&1b` (`preuves/c1-rouge.txt`). Vert après
(`preuves/c1-vert.txt`). Sonde après correction : les sept actes sont refusés, les lectures restent permises
(`preuves/sonde-lecture-pure-corrige.txt`). Le même test joue aussi la ligne Stop de la table : un Stop sous erreur
interne est permis et l'erreur est écrite. C'est une garde : elle est verte sur la série et tue G-5, rejoué en K-11.
Mutants : K-1 à K-4, K-11.

**C-2 — `.claude/hooks/garde_faits.py:203` (état `B-5`), README, tests.**
`else:` devient `elif MARQUE not in contenus(b):`. Un message `user` qui porte la marque du crochet n'est plus du texte
humain, sous les deux formes. Dans `test_r5_voit_le_message_a_contenu_chaine`, le refus relayé, sous forme chaîne puis
sous forme liste, ne couvre plus `4f3e2d1` : rouge `0 != 2` (`preuves/c2-rouge.txt`), vert après
(`preuves/c2-vert.txt`). Dans `test_unite_et_fenetre`, une garde fixe l'effet de B-2 mesuré au point 3 : `J28` tapé
puis `28 jours` donne un refus R12. L'ajout daté du README écrit les deux effets de B-2 sur R6. Mutant : K-5.

**C-3 — `.claude/hooks/garde_faits.py:968-969` (état `B-5`), README, test.**
Le refus R10 ne rend plus 2 tout de suite : il pose `code = 2`. R12 se juge au Stop quel que soit `code`, et les refus
s'ajoutent. Dans `test_e29_vingt_huit_jours_sans_piece`, R6 et R12 au même arrêt : rouge
`(2, True, False, False) != (2, True, True, True)` (`preuves/c3-rouge.txt`). R10 et R12 au même arrêt : vert après
(`preuves/c3-vert.txt`). Mutants : K-6 (R10 rend 2 avant R12) et K-7 (`and not code` rétabli).

**C-4 — `.claude/hooks/garde_faits.py:898-899` (état `B-5`), README, tests.**
`nus = comptes_nus(<fenêtre du tour>)`. Un nombre suivi de commits, tests ou fichiers, en chiffres, que `nus` porte,
n'est pas manquant. Rouge `(2, …R12…) != (0, '')` sur `Elle compte 5 commits.` après `wc -l` (`preuves/c4-rouge.txt`),
vert après (`preuves/c4-vert.txt`). Deux gardes : un compte lu par `grep -c` ne couvre pas `28 jours`, et un compte
d'un tour antérieur ne couvre pas. Mutants : K-8 (clause retirée), K-9 (restriction d'unité retirée), K-10 (site
d'appel : `comptes_nus(entrees)`, tout le journal).

**C-5 — `scripts/controle/tests/test_garde_reponse.py` (`test_unite_et_fenetre`), README.**
C'est une garde du regard avant `(?![\d]|[.,]\d)` de `piece_porte` (B-3). Une pièce `280 jours ; 28,5 jours` ne porte
pas `28 jours` : refus R12 attendu. Elle est verte sur la série et tue G-3, rejoué en K-12.

## Mutants (pièces : `g2/mutants/`)

Campagne A (série ; `campagne-a.json`, `campagne-a.txt`, `sortie-a/<id>.diff` et `.out`) :

| id | substitution (avant → après) | classement | tests rouges |
|---|---|---|---|
| témoin | — | vivant (toutes les étapes à 0) | — |
| M1-1 | `if ev == "PreToolUse" and acte_qui_ecrit(entree):` → `if False:` | tué (sortie 1) | `test_cas_reel_de_la_g2_refuse`, `test_table_des_cas` |
| M1-2 | `return nom != "Bash" or not lecture_pure(` → `return nom != "Bash" and not lecture_pure(` | tué (sortie 1) | `test_cas_reel_de_la_g2_refuse`, `test_journal_illisible`, `test_table_des_cas` |
| M1-3 | `if re.search(r"[>\x60]\|\$\(\|<\(", reste):` → `if False:` | tué (sortie 1) | `test_table_des_cas` |
| M1-6 | `if acte_qui_ecrit(entree):          # SHOGEN-GARDE-ERREUR-INTERNE-1 : ` → `if False:` | tué (sortie 1) | `test_journal_illisible` |
| M1-9 | `for seg in re.split(r"&&\|\\|\\|\|[;&\|\n]", reste):` → `for seg in [reste]:` | tué (sortie 1) | `test_table_des_cas` |
| M1-10 | `reste = re.sub(r"[0-9]?>&[0-9]\|[0-9]?>[ ]*/dev/null(?![^\s;&\|])", "", ` → `reste = c` | tué (sortie 1) | `test_table_des_cas` |
| M2-1 | `for b in [c] if isinstance(c, str) else c or []:` → `for b in c or []:` | tué (sortie 1) | `test_faits_et_appels_deux_formes`, `test_r5_voit_le_message_a_contenu_chaine`, `test_unite_et_fenetre` |
| M3-1 | `sans = nombres_sans_piece(entree) if ev == "Stop" and not code else []` → `sans = []` | tué (sortie 1) | `test_e29_vingt_huit_jours_sans_piece`, `test_unite_et_fenetre` |
| M3-3 | `for e in entrees[i + 1:] if i is not None else entrees:` → `for e in entrees:` | tué (sortie 1) | `test_unite_et_fenetre` |
| M3-5 | `if manque and entree.get("stop_hook_active"):` → `if False:` | tué (sortie 1) | `test_e29_vingt_huit_jours_sans_piece` |
| M3-7 | `reponse = []` → `pass` | tué (sortie 1) | `test_e29_seize_semaines_apres_lecture` |
| M4-1 | `if a.lecture_seule:` → `if False:` | tué (sortie 1) | `test_journal_non_ecrit`, `test_passages_journalises` |
| M4-4 | `return 3` → `return code` | tué (sortie 1) | `test_journal_non_ecrit` |
| M5-1 | `lieux = [os.path.realpath(depot)]` → `lieux = ["/"]` | tué (sortie 1) | `test_disque_du_depot`, `test_tmpdir_sur_un_autre_systeme` |
| M5-4 | `for lieu in lieux_disque(a.depot):` → `for lieu in lieux_disque("."):` | tué (sortie 1) | `test_disque_du_depot`, `test_tmpdir_sur_un_autre_systeme` |
| G-1 | `with open(JOURNAL_LS, "a", encoding="utf-8") as f:` → `with open(JOURNAL_LS, "w", encoding="utf-8") as f:` | tué (sortie 1) | `test_passages_journalises` |
| G-2 | `k += 2 if mots[k] == "-C" else 1` → `k += 1` | tué (sortie 1) | `test_table_des_cas` |
| G-3 | `r")(?![\d]\|[.,]\d)")` → `r")")` | vivant (toutes les étapes à 0) | — |
| G-4 | `journaliser(dossier, f"REFUS {ev} {entree.get('tool_name', '')} erreur` → (retiré) | tué (sortie 1) | `test_cas_reel_de_la_g2_refuse` |
| G-5 | `if ev == "PreToolUse" and acte_qui_ecrit(entree):` → `if acte_qui_ecrit(entree):` | vivant (toutes les étapes à 0) | — |

Campagne B (copie corrigée ; `campagne-b.json`, `campagne-b.txt`, `sortie-b/`) :

| id | substitution (avant → après) | classement | tests rouges |
|---|---|---|---|
| témoin | — | vivant (toutes les étapes à 0) | — |
| K-1 | `[0-9]?>&[0-9]+(?![^\s;&\|])\|` → `[0-9]?>&[0-9]\|` | tué (sortie 1) | `test_table_des_cas` |
| K-2 | `elif mots and mots[0] not in LECTURE:` → `elif mots and os.path.basename(mots[0]) not in LECTURE:` | tué (sortie 1) | `test_table_des_cas` |
| K-3 | `if mots and mots[0] == "git":` → `if mots and os.path.basename(mots[0]) == "git":` | tué (sortie 1) | `test_table_des_cas` |
| K-4 | `"pwd", "echo",` → `"pwd", "echo", "printf",` | tué (sortie 1) | `test_table_des_cas` |
| K-5 | `elif MARQUE not in contenus(b):      # refus du crochet` → `else:      # refus du crochet` | tué (sortie 1) | `test_r5_voit_le_message_a_contenu_chaine` |
| K-6 | `code = 2` → `return 2` | tué (sortie 1) | `test_e29_vingt_huit_jours_sans_piece` |
| K-7 | `sans = nombres_sans_piece(entree) if ev == "Stop" else []` → `sans = nombres_sans_piece(entree) if ev == "Stop" and not code else []` | tué (sortie 1) | `test_e29_vingt_huit_jours_sans_piece` |
| K-8 | `and int(m[1]) in nus)))` → `and False)))` | tué (sortie 1) | `test_e29_seize_semaines_apres_lecture` |
| K-9 | `unite(m[2].lower()) in ("commit", "test", "fichier") and m[1].isdigit(` → `m[1].isdigit()` | tué (sortie 1) | `test_unite_et_fenetre` |
| K-10 | `nus = comptes_nus(entrees[i + 1:] if i is not None else entrees)` → `nus = comptes_nus(entrees)` | tué (sortie 1) | `test_unite_et_fenetre` |
| K-11 | `if ev == "PreToolUse" and acte_qui_ecrit(entree):` → `if acte_qui_ecrit(entree):` | tué (sortie 1) | `test_table_des_cas` |
| K-12 | `r")(?![\d]\|[.,]\d)")` → `r")")` | tué (sortie 1) | `test_unite_et_fenetre` |

## Items à former (règle PAROXYSME)

- I-1 : entrée du crochet GARDE-FAITS qui n'est pas un objet, ou dont `transcript_path` n'est pas une chaîne : sortie
  1 hors du `try`, même pour un acte qui écrit. Ce n'est pas exploitable par l'agent (entrée écrite par Claude Code).
  Remède : calculer `ev` et `dossier` dans le `try`.
- I-2 : R12 et les milliers. `1 715 tests` est refusé sous le nom `715 tests` alors que `Ran 1715 tests` est affiché
  (faux refus, dans le sens sûr). Remède : lire le groupe de milliers comme `formes_nombre` de R6.
- I-3 : fenêtre de R12. Si une notification du harnais est enregistrée comme message `user` à contenu chaîne, sans
  `isMeta`, elle ouvre un tour neuf. Ce n'est pas mesurable sans lire un journal `*.jsonl` (interdit) ; à mesurer par
  qui en a le droit.
- I-4 : passage du second arrêt (R6, R10, R12) consigné au journal des décisions mais invisible à l'humain. Remède à
  vérifier contre la documentation des crochets Stop de Claude Code.
- I-5 : skill `shogen-avant-lancer`, point 1 : `df -h /` à remplacer par l'affichage du système de fichiers du dépôt
  (règle E4 des briefs comprise).
- I-6 (limite de B-3, écrite au README) : le texte de l'agent écrit avant son dernier appel d'outil n'est pas jugé par
  R12, alors que l'humain le lit aussi. Le juger ajouterait des faux refus (récits d'étape) : décision à prendre.

## Journal de provenance (G1 du réviseur)

Sources lues [lu] : `g2/BRIEF-G2.md`, `../BRIEF.md`, `../RAPPORT-GENERATEUR.md`, `../NOTES.md`, `../SHA256SUMS` (en
entier) ; les cinq diffs `B-1` à `B-5` (en entier) ; `../../ERREURS-ORCHESTRATEUR.md` (index des lignes, E29 à E36 en
entier) ; `docs/adr-0028/revue-codeql-pr12/G2-transcrit.md` l.15-60 et l.115-135 (C-1) ;
`docs/adr-0028/ANNEXE-B-items.md` l.1873, 1878-1880, 1891 ; `docs/adr-0028/ANNEXE-D-preenregistrement.md` l.32-48
(liste D.2, pour ne rien en ouvrir) ; `.claude/hooks/garde_faits.py` de la série (docstring l.15-40, `contenus`,
`faits_et_appels`, `tour_humain`, `lire_queue`, `journal_de_l_agent`, `refuser`, `journaliser`, `hote_forge`,
`comptes`, `comptes_nus`, `stop`, R12, `lecture_pure`, `acte_qui_ecrit`, `main`, `dossiers`,
`dossiers_sans_releve`, `noms_propres`) ; `.claude/settings.json` ; `scripts/controle/avant_acte.py` (`diff`,
`suivi`, `_jouer`, `sortir`, l.30-60 de la docstring, `parseur` par `grep`) ; `garde_commun.py` (`maintenant`,
`etat_disque`) ; `mutants.py` (docstring, `main`) ; `presg5.py` (docstring) ; `tests/test_avant_acte.py` l.30-66 et
l.895-945 ; `gabarits/chaine.sh` l.45-46 ; `.claude/skills/shogen-avant-lancer/SKILL.md` ; `garde/lignes-citees.txt`,
`garde/dossiers.txt` (tête) ; `docs/adr-0029/ADR-0029-campagne-S2-bis.md` l.158 par `grep` (extrait du test
contrôlé). Aucune pièce de D.2, aucun emplacement interdit, aucun `*.jsonl` ouvert ; aucune liste par motif sur
`docs/`.

Commandes et sorties : voir `NOTES.md` et `preuves/` (sondes, rejeux, rouges et verts, suites, `avant_acte.py diff`,
entrée non objet). Chiffres recomptés : plancher 177 → 191 (`grep` de gates.yml, `Ran = 191`) ; lignes ajoutées et
retirées des diffs C (`grep -c`) ; empreintes (`sha256sum`) ; espaces spéciales (script) ; motif R-13 (`grep -cE`).

Écarts du réviseur, consignés dans `NOTES.md` :
- E-1 (règle git) : une commande `git diff --stat` a tourné sur le dépôt avec une liste de chemins vide. Elle a
  imprimé quatre chemins hors interdits, sans contenu. Remède : liste contrôlée non vide avant chaque commande git.
- E-2 : un `sleep 0` tapé par erreur a été refusé par R7 ; rien n'a tourné.
- E-3 (listes) : des globs et parcours ont tourné sur les seuls dossiers de travail du lot (`p3b/`, `p3b/g2/`), sans
  pièce interdite. Les sommes finales (`SHA256SUMS`) nomment chaque fichier un à un.
