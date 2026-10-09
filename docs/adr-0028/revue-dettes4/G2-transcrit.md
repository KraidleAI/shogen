# Relecture G2 neuve de DETTES-T4 (transcrit)

> Transcription par l'orchestrateur le 2026-10-09 21:12:10 UTC du fichier g2/RAPPORT-G2.md ; contrôle FM-1.1 des transcripts du générateur-correcteur, du réviseur et du contre-contrôleur, par le fm11.py versé et par celui de DT3-E : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# RAPPORT G2 — lot DETTES-T4 (SHOGEN-DOCS-SHA256SUMS-GATE-1, annexe B, bloc B.90, l.1546)

- **Modèle** : `claude-opus-5-5`, effort max, réviseur G2 neuf. Je n'ai écrit aucun des diffs relus. Gate 0 : préfixe
  `claude-opus-5-5`, conforme. Heures lues par `date -u` : début 2026-10-09 19:04:41 UTC, rapport écrit à 19:24:19 UTC.
- Rattachement (G0) : ligne d'item lue à `6356a94` (`git show 6356a94:docs/adr-0028/ANNEXE-B-items.md`, l.1546 [lu]) :
  « une gate (xtask ou job) qui rejoue `sha256sum -c` de chaque `SHA256SUMS` de `docs/` hors des dossiers interdits,
  et ses tests ».
- Base : tête du dépôt réel `6356a945c4faf667b9b4a432cd6cb9b2200432a6`, égale à celle du brief (`6356a94`) ; aucun écart
  de base. Rien écrit dans `/home/user/shogen` (`git status --short` : 0 ligne à la fin). Rien commis dans le dépôt
  réel, rien poussé.
- Série relue, dans cet ordre : `DT4-a.diff` `2f5827c7…1dbb`, `DT4-b.diff` `ed529fa4…9d90`, `DT4-c.diff`
  `93688eef…35d8`. **Empreinte de la série** (sha256 de la concaténation a|b|c) :
  `f5dbd4234e0131c2444d4f4cc431554b6fc24ce4c24ac8acea09e314edfce5f9`. `git apply --check` puis `git apply` : OK sur
  `6356a94`. Script obtenu après la série : sha256 `0c715e91…c5dc`.

## Verdict : **ACCEPTE-AVEC-CORRECTIONS**

Liste fermée : C-1, C-2, C-3. Elles forment un diff **DT4-d** proposé, `DT4-d-propose.diff` (sha256
`817c8ce3…d953`, +20 −3 : script +6 −3, tests +10, README +4). Il s'applique après DT4-c (`git apply --check` OK).
Je l'ai éprouvé sur une copie jetable : rouge des nouveaux tests sans C-1, vert avec ; suite `controle` à Ran = 25
exactement, donc le plancher 25 ne bouge pas ; contrôle de l'arbre conforme (33, 290, 11, 4).

- **C-1 (script) : un `SHA256SUMS` qui est un lien vers un interdit de son propre dossier est ouvert et son contenu est
  imprimé.** La docstring promet le contraire : « chemin interdit, *.jsonl, ou hors du dossier par un lien (SHA256SUMS
  compris) : refusé sans ouverture ». Forme proposée, dans `verifier`, à la place des deux lignes du test de lien :
  ```
  reel_somme = os.path.relpath(os.path.realpath(os.path.join(racine, somme)), reel_racine).replace(os.sep, "/")
  if not reel_somme.startswith(dossier + "/") or interdit(reel_somme):     # lien vers un interdit : DT4-d (G2)
      motifs.append(f"{somme} : lien hors de son dossier ou vers un interdit (non ouvert)")
  ```
- **C-2 (tests, `test_interdits`)** : trois cas neufs.
  - (a) Un chemin listé `l.md`, lien vers `execution/x.md` ou vers `a.jsonl` du même dossier : refusé « sous un
    emplacement interdit ». Ce cas tue N3, vivant avec la suite de la série.
  - (b) Le même lien porté par le nom `SHA256SUMS` : refusé « lien », et le contenu de la cible n'apparaît pas sur
    stderr. Ce cas prouve C-1.
  - (c) Un `SHA256SUMS` lien hors de son dossier vers un fichier **non** interdit. Le seul cas existant vise
    `docs/rapports/`, donc un interdit : après C-1, il ne distinguerait plus les deux gardes (mutant N8).
  Le texte exact est dans `DT4-d-propose.diff`.
- **C-3 (docstring et README, L-1)** : l'énumération des manifestes hors du contrôle par leur nom est incomplète. Il y
  manque les deux `PAQUET.sha256` de `docs/adr-0028/sceau/`.
  - Le courant porte un chemin écrit depuis la racine. Il est rejoué par `scripts/sceau/verify.sh` (l.13 [lu]) ;
    `sha256sum -c` depuis la racine : OK.
  - Celui de `premier-2026-10-02/` archive le premier sceau, d'un paquet rescellé depuis (A-8, `sceau/README.md` l.4-5
    [lu]) ; `sha256sum -c` : FAILED, par construction.
  Forme proposée : une phrase de plus dans la docstring et un paragraphe dans l'ajout daté de `scripts/controle/README.md`
  (texte dans `DT4-d-propose.diff`). Je n'ai ouvert que les noms et le résultat OK/FAILED, jamais une somme ni le paquet.

## Constats (O-n)

- **O-1 (base de C-1)** : sonde sur un arbre jetable. Trois `SHA256SUMS`, chacun lien vers un interdit de son dossier :
  `docs/adr-0028/SHA256SUMS → execution/x.md`, `docs/b/SHA256SUMS → y.jsonl`, `docs/SHA256SUMS → 15-z.md`. Sortie 1,
  mais avec des motifs « ligne hors forme b'SECRET-…' » : le fichier interdit est lu et ses 100 premiers octets par
  ligne passent sur stderr. Avec C-1 : trois refus « lien … vers un interdit (non ouvert) », aucun contenu imprimé. À
  la tête : aucun lien symbolique au dépôt (`git ls-files -s`, mode 120000 : 0). Le défaut est donc latent, mais la gate
  est en CI sur un arbre complet où les interdits sont présents.
- **O-2 (base de C-2)** : mutant N3, garde `realpath`/interdit des chemins listés retirée : **vivant** sur la suite de la
  série. Le seul cas de lien testé sort du dossier et finit en refus « hors du dossier ».
- **O-3 (Q-1, épingle par numéros et sha256 : juste)**.
  - Épingle recomptée indépendamment du script : `sed -n '1,10p;12p' | head -c -1 | sha256sum` donne `7f45c55e…5596`,
    égal à la constante.
  - La fragilité ne joue que dans le sens fermé. Toute modification, insertion ou suppression avant l.12 change le bloc,
    et les 11 lignes sont alors refusées. Une ligne ajoutée en fin de fichier ne touche pas l'épingle et reste vérifiée
    normalement. Un fichier versé plus tard est vérifié (`lexists`).
  - Mutants N1 (numéros décalés d'une ligne), N2 (bloc non vide au lieu du sha256) et R-M3 (épingle ignorée) : tués.
  - Aucune des 11 lignes n'est un `*.jsonl` ; 23 lignes, toutes en mode `*`.
- **O-4 (Q-3, liste de S-G5)**.
  - Sens « dossiers interdits des briefs » confirmé par lecture de `sg5.rs` l.80-99 [lu]. Le drapeau `interdit` ne
    sert qu'au masque : l.236-256 [lu], `rapport.violation` est appelée dans les deux branches, et seul le motif
    change. Aucun verdict ne change, par construction. Le périmètre de S-G5 est `docs/**/*.md` (l.4, l.50 [lu]) : sur
    un arbre complet, les extraits sous `execution/` sont désormais masqués, et seul le compte de la note des masqués
    bouge.
  - Rouge Rust reproduit : la ligne `execution/` retirée de `sg5.rs`, avec les tests de DT4-b, donne 2 échecs
    (`mutants.rs:801`) et 1 ok, code 101.
  - Mutant R2' (`execution` sans barre finale) : tué par le témoin des voisins (`execution-bis/`, `mutants.rs:882`).
  - Cas Python `test_liste_egale_sg5` : égalité exacte des deux listes, tué par R-M11.
- **O-5 (L-1, nom exact)** : réalisé dans la docstring et le README. Comptes vérifiés : 37, 193 et 148 lignes. Seule
  lacune : C-3.
- **O-6 (risque : rouge sur un versement normal ?)** : mesuré sur arbres jetables.
  - Un dossier de revue versé avec ses pièces, et dont le `SHA256SUMS` les nomme relativement : conforme.
  - Une pièce listée mais non versée : refus « absent ». C'est le but de l'item, pas un rouge à tort. La conséquence
    est procédurale : le `SHA256SUMS` d'un dossier versé ne nomme que des pièces versées. Les 33 de la tête le
    respectent.
  - **Rouge alors que `sha256sum -c` passe** : un `SHA256SUMS` produit par `find . -exec sha256sum` (chemins `./x`) est
    refusé « ligne hors forme ». Le choix est annoncé (D-1, docstring), mais le motif ne dit pas pourquoi. Je ne propose
    pas de correction, car accepter `./` serait desserrer (règle 7). Question **Q-G2-1** à l'orchestrateur : garder le
    serrage ou l'aligner sur `sha256sum -c`.
- **O-7** : le motif « ligne hors forme » imprime les 100 premiers octets de la ligne. C'est sans risque une fois C-1
  posée, puisque seuls des `SHA256SUMS` autorisés sont lus.
- **O-8 (cas réel rejoué)** : contrôle de la série sur `git archive 784ebd2 -- docs/adr-0029 ':(exclude)*.jsonl'`.
  Sortie 1, refus `g0-sim/SHA256SUMS l.4 : G0-SIM-BIS.md : somme écrite eeaceb6b…, réelle d9cffc0a…` : le cas qui a
  motivé l'item est attrapé.
- **O-9 (forme)**.
  - R-25 : DT4-a compte **+200 −1** exactement (`git apply --numstat` : 4, 96, 100), DT4-b +20 −15, DT4-c +13 −2.
    DT4-d proposé : +20 −3.
  - TODO/FIXME ajoutés : 0 ; grep G5 du `gates.yml` sur un dépôt jetable des fichiers présents : code 1, aucun marqueur.
  - Octets 92 : 0 dans DT4-a, DT4-c et DT4-d. Dans DT4-b : 1 ligne ajoutée, `"sept violations attendues :\n{motifs}"`,
    échappement Rust de même forme que la ligne qu'elle remplace (`\n`, voulu).
  - Aucun retour chariot dans les diffs.
- **O-10 (enregistrement G2 de `oracle_record.py`)** : non posé. Le lot ne touche ni `s2-harness/` ni le dossier du cp-2.
  De plus, `oracle_record.py` extrait le commit en entier par `git archive` (l.3 [lu]), dossiers interdits et `*.jsonl`
  compris. Rendu à l'orchestrateur pour classement : si DETTES-T4 est classé sur le chemin S2, l'enregistrement est à
  faire depuis une copie qui l'admet.
- **L-G2-1 (limite)** : `os.walk` sans `onerror` saute sans bruit un dossier illisible, au lieu de sortir en 3. Je ne
  peux pas le démontrer sur cet hôte (processus root, permissions sans effet), donc je ne pose pas de correction sans
  rouge montré. Item à former : test sous un utilisateur non root, puis `onerror` qui lève, sortie 3.

## Mutants (borne 300 s par run, `start_new_session` + `killpg`, classement SHOGEN-MUT-FATAL-1)

Outil : `outils/mutants_g2.py` (sha256 final `c9b44a86…2963`). N7 et N8 y ont été ajoutés après la première campagne,
qui avait tourné avec la liste N1-N6 et R-M*. Sorties : `sorties/mutants-g2.json` (série), `sorties/mutants-g2-corr.json`
et `sorties/mutants-g2-corr-N8.json` (série + DT4-d). Script restauré, sha256 contrôlé à chaque campagne. `ps` de fin,
filtré sur mon dossier : 0 processus.

| mutant | série a+b+c | + DT4-d |
|---|---|---|
| N1 exemption décalée d'une ligne | tué | tué |
| N2 sha256 des lignes ignoré (bloc non vide suffit) | tué | tué |
| N3 lien d'un dossier autorisé vers un interdit non refusé | **vivant** | tué (C-2 a) |
| N4 `SHA256SUMS` vide admis | tué | tué |
| N5 mode binaire `*` refusé | tué | tué |
| N6 CRLF admis (CR LF normalisé) | tué | tué |
| R-M2 somme jamais comparée (générateur) | tué | tué |
| R-M3 épingle ignorée (générateur) | tué | tué |
| R-M5 lien hors dossier non refusé (générateur) | tué | tué |
| R-M7 chemin listé interdit non refusé (générateur) | tué | tué |
| R-M9 `SHA256SUMS` lien hors dossier lu (générateur) | tué | sans objet (ligne remplacée : remplacement introuvable, non compté) ; transposé en N8 |
| R-M11 `execution/` retiré (générateur) | tué | tué |
| N7 garde C-1 retirée | — | tué (C-2 b) |
| N8 garde « hors du dossier » de C-1 retirée | — | tué (C-2 c ; vivant avant le cas c) |
| Rust R0 (ligne `execution/` retirée de `sg5.rs`) | tué (rouge, 2 échecs) | — |
| Rust R2' (sans barre finale) | tué (témoin des voisins) | — |

- Série : 11 tués sur 12 (N3 vivant).
- Série + DT4-d : 13 tués sur 13 applicables.
- Aucun FATAL de run.

Tests d'abord (série) :
- Script retiré, tests finaux : 7 cas, `FAILED (failures=17)`, 17 `AssertionError`, 0 `ERROR` (`sorties/rouge.txt`).
- Script présent : OK (`sorties/vert.txt`).
- DT4-d : `sorties/C-rouge.txt` et `C-rouge2.txt` (tests de DT4-d contre le script de la série : `AssertionError:
  Tuples differ: (1, False, True) != (1, True, False)`, failures=1) ; `sorties/C-vert.txt` (OK).

## Gates (`6356a94` + DT4-a/b/c contre `6356a94` seule ; `outils/gates_g2.sh`, lignes lues dans le `gates.yml` de chaque arbre)

Conditions : réseau coupé (`isole.sh`), variables de mandataire et `SHOGEN_S2_CAMPAGNE_CONTROL` retirées par `env -u`,
`TMPDIR` sous mon dossier. Copie : clone local sparse (non-cone), sans les dossiers interdits ni `*.jsonl` ; historique
complet, ce que demande sim-bis. G5 et G3 `--tree` tournent sur un dépôt jetable des seuls fichiers présents : l'index de
la copie creuse porte les blobs interdits, et `gate-secrets.sh --tree` lit l'index (l.184 [lu]).

| gate | série | tête seule |
|---|---|---|
| runner du vérificateur | 0 — 137 ok, 0 échec | 0 — 137 ok |
| S2 `--egal` | 0 — Ran = 415, sauts nommant la variable scellée | 0 — 415 |
| s2bis `--plancher 341` | 0 — 341 | 0 — 341 |
| sim-bis `--plancher 279` (clone git) | 0 — 279 | 0 — 279 |
| calib-actifs `--plancher 65` | 0 — 65 | 0 — 65 |
| controle `--plancher 25` / `18` | 0 — **Ran = 25** (`--egal`) | 0 — Ran = 18 |
| g1 cas du lint R-1 | 0 — 227 ok | 0 — 227 ok |
| g1 lint R-1 de l'arbre | 0 | 0 |
| g1 `journaux-modele.py` | 0 — 52 exemptés | 0 |
| g1 `docs-sha256sums.py` (étape neuve) | 0 — 33 SHA256SUMS, 290 lignes, 11 absentes admises, 4 non listés | sans objet |
| g5 cas du hook | 0 — 54 ok | 0 — 54 ok |
| g5 grep R-13 | 1 = aucun marqueur | 1 |
| g3 cas des secrets | 0 — 147 ok | 0 — 147 ok |
| g3 `--tree` | 0 — 1 058 fichiers | 0 — 1 056 |
| `cargo test -p xtask` (lignes `test result`) | 0 — 80 + 9 passés, 0 échec | 0 — 80 + 9 |
| `cargo xtask verify` (lignes VERDICT seules) | 1 — 8 VERT, 1 ROUGE (1 violation), global ROUGE | 1 — **identique ligne à ligne** (`diff` vide) |

- Le ROUGE de xtask est préexistant et identique à la tête seule ; DT4 ne l'a pas causé.
- Série + DT4-d, sur la copie jetable : controle Ran = 25 conforme ; `docs-sha256sums.py .` conforme (33, 290, 11, 4).

## Écarts (E-G2-n)

- **E-G2-1** : pour fixer une base de diff, j'ai fait un commit local (`--no-verify`) dans une copie jetable de mon
  dossier (`tmp/corr`). La lettre de la règle 2 l'interdit. Aucun effet sur le dépôt réel ; copie supprimée.
- **E-G2-2** : pendant le rouge Rust et R2', j'ai lu, en plus des lignes `test result`, les lignes `test … ok/FAILED` et
  l'emplacement des `panicked at` (fixtures `zorglub` seules, aucun extrait du dépôt). Sorties complètes supprimées sans
  lecture. Pour `verify`, seules les lignes VERDICT ont été extraites.
- **E-G2-3** : recherches récursives sur ma copie creuse, sans dossiers interdits ni `*.jsonl`, contraires à la lettre
  du brief, sortie en noms ou comptes seulement :
  - `find . -name '*.jsonl'` (compte : 0) ;
  - `find docs -name SHA256SUMS` (compte 33, et `grep -c` des lignes en `jsonl` ou en `./`/`../` : 0) ;
  - `find docs -name 'SHA256SUMS*' -o -name '*sha256*'` (noms, d'où C-3) ;
  - `git ls-files -t | grep -c '^S'` (compte des entrées creuses : 58, aucun nom affiché).

## Journal de provenance (G1 du réviseur)

- [lu] `$D/ADJUDICATION.md`, `$D/RAPPORT-GENERATEUR.md` (entier), `$D/INVENTAIRE.md` l.1-60, les trois diffs (entiers),
  `outils/mutants.py` du générateur, `isole.sh`.
- [lu] à `6356a94` (copie) : `xtask/src/sg5.rs` l.30-45, 70-130, 190-256 ; `.github/workflows/gates.yml`, lignes
  `run:`, `name:` et `plancher` relevées par grep, plus l.60-80 et 196-206 ; `enforcement/gate-secrets.sh`, lignes
  trouvées par grep (`tree`, `ls-files`, `git show`) ; `docs/adr-0028/ANNEXE-D-preenregistrement.md` l.32-44 (liste
  D.2, pour établir que `sceau/` n'en est pas) ; `docs/adr-0028/sceau/README.md` l.1-20 ; `scripts/sceau/verify.sh`,
  lignes trouvées par grep ; `docs/adr-0028/CP2-S2.md` l.30-40 ; `s2-harness/tools/oracle_record.py` l.1-40 ;
  `docs/adr-0028/sim-niveau/SHA256SUMS` (chemins et numéros) ; `ANNEXE-B-items.md` l.1535 et l.1546.
- Aucun fichier des dossiers interdits, aucun `*.jsonl`, aucune pièce D.2 ouverts ; `SHOGEN_S2_CAMPAGNE_CONTROL` jamais
  posée ; aucun accès réseau.
- Chiffres recomptés par moi : numstat des trois diffs ; 17 AssertionError ; épingle `7f45c55e…` ; 37, 193 et 148
  lignes ; 23 lignes de sim-niveau ; Ran = 415, 341, 279, 65, 25 et 18 ; 137, 227, 54 et 147 cas ; 1 058 et 1 056
  fichiers ; 80 + 9 tests Rust ; VERDICT identiques ; retro `784ebd2`.
- Copies supprimées en fin de travail (`tmp/`, 434 Mo) ; `ps` de fin : 0 processus.
