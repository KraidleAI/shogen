# Relecture G2 neuve du groupe C (transcrit)

> Transcription par l'orchestrateur le 2026-10-16 12:03:37 UTC du fichier garde-fous/p2c/g2/RAPPORT-G2.md ; contrôle FM-1.1 des transcripts (générateurs des groupes A, B, C, réviseurs G2 des trois groupes, intégrateur, contre-contrôleur) par le fm11.py versé : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Relecture G2 neuve — GARDE-FOUS-ORCH, phase 2, groupe C (P2C-1 à P2C-7)

Gate 0 : `claude-opus-5-5` (worker, réviseur ; je n'ai pas généré le lot). Brief : `g2/BRIEF-G2.md` (orchestrateur,
2026-10-16 01:58:16 UTC). Journal G1 du réviseur : `g2/NOTES.md` (sources, commandes, sorties, écarts ; reprise
après le redémarrage du conteneur à 02:05:01 UTC). Dépôt lu en lecture seule, tête `520bb2afa8116ecd3229cda0e8685eb19a4e0e4f`
pour toute la relecture ; aucune écriture git sur lui, aucun cargo. À 02:33:43 UTC (`date -u`), la chaîne DETTES-T15
avait avancé la tête à `ccc29190` (DT15-k, DT15-l, DT15-n), sans toucher `scripts/controle`, `gates.yml`,
`enforcement` ni `docs/RENVOIS-LIGNES.tsv` (`git diff --stat` vide). Le registre est indexé, non commis, au moment du
relevé : s'il est commis, le relevé de C-3 et les cas du point 7 se refont au recalage. Copie : `git archive 520bb2af` hors interdits
(`g2/copie/`, commit local `300ed7ec`). Enregistrement `oracle_record.py --role G2` : sans objet (lot hors du
chemin S2, aucun dossier soumis au cp-2).

## Verdict : ACCEPTE-AVEC-CORRECTIONS (C-1 à C-4, liste fermée)

Le code, les tests et les mutants des sept diffs tiennent : la série recalée sur la tête passe le job
`controle-unittest` (runner `153 ok, 0 échec` ; Ran = 130, conforme, aussi après C-1 à C-4) et sa propre garde (`--lecture-seule diff` de chaque pas : sortie 0) ; les
19 mutants rejoués se classent comme au rapport du générateur. Les corrections portent sur le texte des ajouts du
README, que le recalage de Q-1 réécrit de toute façon :

- **C-1** (point 1) : les planchers écrits dans les sept ajouts du README (118, 121, 122, 124, 125, 128, 129) sont
  ceux de la base `413321bf` ; à la tête le job porte 118 (DT15-f), la série pose 119, 122, 123, 125, 126, 129, 130.
  Le texte de chaque ajout prend le plancher que son diff écrit dans `gates.yml` (règle à garder au recalage de la
  chaîne si la tête bouge encore).
- **C-2** (point 5) : l'ajout de P2C-4 dit qu'une chaîne copiée d'un modèle ancien ne commet plus. C'est faux pour
  toute copie d'un modèle antérieur à P2C-4 (elle scelle sans `--verif`, sceau non jugé) et pour une chaîne qui
  n'appelle pas `avant_acte.py` (`chaine_d7.sh`). Le texte corrigé borne la portée et écrit la forme `source` de Q-2.
- **C-3** (point 7) : l'ajout de P2C-6 ne donne le relevé du registre qu'à `413321bf` (99 répondent, 11 non) ; à la
  tête (DT15-b2) l'outil lit 110 répondent, 0 non, 23 hors de l'arbre. Le relevé de la tête est ajouté.
- **C-4** (point 5) : `OUTILS` est dans le dépôt par défaut, donc un diff qui verse une vérification au modèle (voie
  de Q-2) est refusé en C1 par une chaîne copiée du modèle d'avant (mesuré). Le README écrit la procédure :
  ce diff passe au premier pas d'une chaîne copiée du modèle d'après lui.

Diffs byte-exacts (`g2/diffs/`) : `P2C-1-…-recale-g2.diff` à `P2C-7-…-recale-g2.diff`, la série recalée sur
`520bb2af` avec C-1 à C-4 (forme Q-1 : ajouts du README reposés en fin ; les dates de l'heure du générateur restent :
l'orchestrateur les redate au pas, `date -u`) ; `C-1-a-C-4-sur-serie-recalee.diff`, l'écart de ces corrections
au recalage mécanique (README seul, 12 lignes ôtées, 18 ajoutées, mesuré par `grep -c`). Le code, les tests,
`gates.yml` (hors valeur du plancher), `SHA256SUMS` et `garde/lignes-citees.txt` sont ceux du générateur, à l'octet.

## Checklist

### 1. Application, plancher, lignes décalées : CONFORME avec C-1
- `git apply --index` des sept diffs tels quels sur la tête : aucun ne s'applique. La cause est DT15-f (`284c200`) :
  plancher 118, commentaire de deux lignes au-dessus du job (le plancher passe de la l.365 à la l.367), ajout daté
  du 2026-10-16 00:56:42 UTC en fin du README. Le premier diff échoue sur ces deux points, les autres par cascade.
  Les hunks de code ne sont pas en cause.
- Recalage Q-1 (`g2/outils/recale.py` : hunks de fin du README reposés en fin, octets inchangés ; plancher courant +
  écart du diff ; reste par `git apply --index`) : 7 applications en sortie 0. Les planchers sont 119, 122, 123,
  125, 126, 129, 130.
- **Plancher final 130 = 118 + 12, et non + 11** : 12 tests ajoutés (1, 3, 1, 2, 1, 3, 1), recomptés par
  `def test_` au pas. Le runner des cas sort en 0 ; `verdict-suite-s2 : conforme (code 0, résumé final, aucun saut,
  Ran = 130)` sous Python 3.11.15.
- Lignes décalées : README, ajouts en fin et l.11 de la table changée en place ; `git grep -n 'README.md:11'` et
  `'README.md l.11'` sur `ANNEXE-B-items.md`, `JOURNAL.md` et `revue-garde-fous/` ne trouvent rien (rc 1). Le
  registre n'a aucune rangée vers `scripts/controle` ; ses rangées vers `gates.yml` ont toutes `lignes` à `-`.
  `fm11.py` change sa l.23 en place, et la l.4 citée ne bouge pas.
- Hors du README, `chaine.sh` bouge aussi : P2C-5 décale ses l.42-45 d'une ligne, nombre de lignes inchangé. Le
  seul renvoi trouvé, `chaine.sh` l.44 (G2 transcrite de la phase 1, l.59), visait déjà à la tête une autre ligne que
  la reprise qu'il cite (l.45). Après P2C-5, cette reprise est en l.44. C'est un renvoi d'histoire, hors registre.
- Ajouts recalés : chaque sha256 cité est celui du fichier au pas, et les comptes de tests cités sont égaux aux
  comptes du pas. Seuls les planchers sont faux (C-1).

### 2. P2C-1 (FM11-MOTIF) : CONFORME
`g2/outils/fm11_rejeu.py` rejoue `fm11.py` sous la DOUBLURE de `tests/test_fm11.py` : aucune pièce de D.2 n'est lue.
- Chemin du scratchpad (entrée et résultat) : 0 avec P2C-1, compté à la tête. Le faux positif est fermé.
- Fragment réel : un nom de transcription `<projet>/<session>.txt`, `<session>/subagents/…` et le préfixe seul sont
  détectés.
- `Claude-Session: …session_013dvmub…` sur un journal factice compte 1, avant et après P2C-1. Le faux positif est
  mesuré : l'item proposé SHOGEN-FM11-MOTIF-ATTRIBUTION-1 se forme.
- Limite non écrite au rapport du générateur : `<session>/scratchpad/../subagents/a.txt` n'est pas compté (faux
  négatif, le lookahead accepte un chemin qui ressort du scratchpad). C'est l'item 2 ci-dessous.

### 3. P2C-2 (DATE-PASSEE) : CONFORME (décision Q-3 respectée : refus dès maintenant)
`g2/outils/heures.py` :
- `heure-sans-date`, cas vrais refusés : `vers 04:18 UTC`, `(16:57:31 UTC)`, heure à plus de 25 caractères de sa
  date.
- `heure-sans-date`, cas faux admis : `Ajout daté du 2026-10-16 01:03:46 UTC`, heure en code, heure citée.
- Bords refusés hors code : `JOURNAL.md:12:34` et une durée `01:30`. Le geste affiché pour ces refus reste
  `lire date -u, puis récrire l'heure` (observation O-1).
- `heure-passee`, cas vrais refusés : ajout daté antérieur, titre daté de la veille, `Amendement daté du` antérieur.
- `heure-passee`, cas faux admis : ajout daté du moment, renvoi en minuscule (`l'ajout daté du …`), date seule du
  jour. Une date seule de la veille est refusée.
- Textes réels de la tête (`g2/outils/ajouts_reels.py`) :
  - README : 62 entrées datées, 0 hors d'ordre, 0 heure sans date ;
  - CLAUDE.md : 0 heure sans date ;
  - annexe B, de la l.1484 à la fin : 1 heure sans date (l.1539, `13:49:50 UTC` sans date, vrai positif) et 1 entrée
    hors d'ordre (l.312, B.19 du 2026-10-01 après une entrée du 2026-10-02). C'est de l'histoire : la règle ne juge
    que les ajouts.
- Les ajouts datés de la série recalée passent : leurs `diff` sortent en 0.

### 4. P2C-3 (ATTRIBUTION-DIFF) : CONFORME, avec une limite mesurée (item 3)
- Le refus d'un mot attribué à un autre diff du préfixe est couvert par `test_l3_attribution_au_diff` (7 refus,
  7 admis, `--id`, lignes ajoutées). Rejoué sur un message réel jugé sous un autre Diff-Id : `cb447f6` jugé `C-5`
  donne le refus `identifiant C-3`.
- Rejeu sur 10 des messages de la phase 1 (`g2/outils/attribution10.py`) : `61b1c3b`, `b4382af`, `0dc7b27`,
  `2726793`, `cb447f6`, `8c808e2`, `655dcf0`, `c08242a`, `001ffe4`, `04cb816`. Source : ADJUDICATION de la tête ;
  lignes ajoutées réelles. **0 refus**, et 0 encore sans les lignes ajoutées.
- La garde est faible sur des sources réelles : sur 5 messages jugés sous un autre Diff-Id, 1 seul refus. Un passage
  qui couvre plusieurs diffs les admet tous. C'est la limite déclarée.
- Faux refus mesuré : Diff-Id `DT15-j` et source `Série DT15-a à DT15-m : G2 neuve ACCEPTE-AVEC-CORRECTIONS, C-1 à
  C-10 reprises.` donnent 3 refus (verdict, C-1, C-10). Une plage à bornes en lettres n'est pas lue, et c'est la
  forme des familles DTn-x. Le refus ferme l'acte sans rien laisser passer ; item proposé
  SHOGEN-GARDE-ATTRIBUTION-PLAGE-LETTRES-1 (item 3), à traiter avant la prochaine chaîne qui passe par `acte commit`
  avec des identifiants à lettres.

### 5. P2C-4 (VERIF-VERSIONNEE) : CONFORME avec C-2 et C-4 (décision Q-2 respectée : aucun `--verif-admise`)
- Le sceau porte le sha256 de `declare -f verif` et `commit` refuse une vérification étrangère : tests rouges puis
  verts du générateur, et mutants M4-2 et M4-4 rejoués, tués.
- `<scratchpad>/chaine_d7.sh`, l.1-22 lues. Cette chaîne n'appelle pas `avant_acte.py` (`git commit` direct) : elle
  n'est **pas** refusée aujourd'hui, elle est hors de la garde.
- Si elle scellait sa fonction `verif` (l.9-22) par `--verif`, elle serait refusée (mesuré dans un dépôt jetable) :
  `REFUS C1 : sceau d'une vérification (f7d0b53b09b0…) autre que la fonction verif versionnée de gabarits/chaine.sh
  (L-4)`, commit en 1.
- Forme qui passe (mesurée, commit en 0) :
  `source <(sed -n '/^verif() {/,/^# --- fin de verif/p' "$OUTILS/gabarits/chaine.sh")` puis
  `verif "$id" && declare -f verif | acte sceller --verif - && acte commit … && git commit …`.
- Ce que cette forme demande à l'orchestrateur :
  - la fonction du modèle lit `PLAN`, `DEPOT` et `DELAI` ;
  - elle ne porte ni l'isolement `isole.sh` ni le retrait des variables de mandataire que `chaine_d7.sh` emploie. Les
    verser au modèle passe par un diff relu (Q-2), et ce diff tombe sous C-4.
- Mesuré dans un dépôt jetable (`OUTILS` dans le dépôt, défaut du modèle) : un diff qui change la fonction `verif`
  du modèle, scellé avec la fonction d'avant, est refusé `REFUS C1 … (8fa5ee9f55f6…)` (C-4 et item 4).
- `declare -f` dépend de la version de bash : la chaîne et l'outil tournent sur le même hôte (observation O-2).

### 6. P2C-5 (DISQUE-CHAINE) : CONFORME
- Le disque se contrôle dans la boucle, après l'arbre propre et avant `git apply`, avec la ligne
  `ROUGE disque avant <id> (LN-1) : arrêt, rien appliqué`. Test `test_ln1_disque_a_chaque_pas` ; mutants M5-1 et
  M5-3 rejoués, tués.
- Seuil lu dans `garde_commun.py` l.40, `SEUILS_GIO = (3, 6)` : refus sous max(3 Gio, `--min-go`), avertissement
  sous 6. `DISQUE_MIN_GO` vaut 0 par défaut dans le modèle.
- Le disque se mesure sur `/` (`etat_disque("/", …)`), non sur le système de fichiers de `DEPOT`. C'est antérieur au
  lot (observation O-3).

### 7. P2C-6 (LIGNE-REMPLACEE) : CONFORME avec C-3
- Le format réel du registre (DT15-b2) est lu : à la tête recalée, 112 empreintes (110 du registre, 2 de la garde),
  toutes répondent ; 23 rangées ont `-`.
- Cas, par `--lecture-seule diff` :
  - `verification.rs` l.300 remplacée à nombre de lignes égal (renvoi 294-308) : `REFUS C7 … renvoi 294-308 changé`
    ;
  - l.3, ligne non citée : sortie 0 ;
  - ADR-0028 l.293 : refus (garde) ;
  - `fm11.py` l.4 : refus (garde).
- Pourquoi ces deux empreintes : ce sont les deux renvois par numéro des outils que le registre ne couvre pas (il ne
  recense que les renvois des documents).
  - ADR-0028 l.293 est la source de `garde/hors-distant.txt` (l.2-3, sha d'époque `16e208a9…`, saut de ligne
    compris) et des messages de `pousser`.
  - `fm11.py` l.4 (`REPO = '/home/user/shogen'`) est citée par la table du README.
  - Les valeurs versées (`d4d626281fcd97a6`, `3501489f246ba05c`) sont recalculées par mon script à la convention du
    registre, sans saut de ligne final.
- **Ordre des diffs** : P2C-1 change la l.23 de `fm11.py`, non la l.4 ; la l.4 est identique avant et après P2C-1
  (relu). L'empreinte versée par P2C-6, appliqué après P2C-1, reste donc juste.
- Les rangées du registre en double (plusieurs documents citent la même plage) répètent le même refus : bruit sans
  effet sur le verdict (observation O-4).

### 8. P2C-7 (LECTURE-SEULE) : CONFORME
- Un clone `--shared --no-checkout` est fait dans un `TemporaryDirectory`.
- Empreinte de tous les fichiers de `copie/.git` (1824 entrées), égale avant et après `--lecture-seule diff`. Même
  égalité avant et après `--lecture-seule commit` (1830 entrées, sceau du dépôt lu exigé et lu, sortie 0). Le commit
  courant, lui, change l'empreinte (journal).
- Aucun clone ne reste dans `TMPDIR`.
- La journalisation absente est acceptable : elle est déclarée, et l'item proposé
  SHOGEN-GARDE-JOURNAL-LECTURE-SEULE-1 se forme.

### 9. Mutants : CONFORME
- Campagne G2 : `scripts/controle/mutants.py` de la tête (sha256 `68406b96…`, égal au figé du générateur), lancé à
  part de la copie mutée (`g2/copie/`, série recalée), job `controle-unittest`, borne 300 s.
- 19 mutants de `mutants3.json` (texte « avant » présent une fois, contrôlé) : M1-2, M2-2, M2-6, M2-10, M3-3, M3-5,
  M3-10, M4-2, M4-4, M5-1, M5-3, M6-1, M6-5, M6-7, M6-11, M7-1, M7-4, M7-7, M7-8.
- Résultat (`g2/mutants/campagne-g2.txt`, sorties dans `g2/mutants/sortie/`) : témoin vivant ; **17 tués**
  (sortie 1), 2 vivants (M6-5, M7-7), 0 FATAL ; `campagne-g2.err` : `aucun processus des 40 groupes de la
  campagne, aucun descendant vivant de l'outil`. Mêmes classements que la campagne finale du générateur.
- Équivalents déclarés, jugés :
  - **M6-5 équivalent** : la ligne d'empreinte gardée parmi les motifs fnmatch ne répond qu'à un chemin écrit
    littéralement `<chemin>:<a> <empreinte>` (ni `*`, ni `?`, ni `[` dans les deux lignes versées).
  - **M7-7 équivalent** : mesuré dans un dépôt temporaire, `git clone --shared --no-checkout` suit la HEAD du dépôt
    lu, détachée (source et clone en `4a925c7`) comme dans un worktree lié sur une autre branche (`75328a7`). La
    ligne `update-ref` est défensive.

### 10. Écarts E-1, E-2, E-4 : CONFORME
- E-1 : des noms de dossiers seulement, aucun contenu.
- E-2 : recherche dans les copies du générateur, bâties sans les interdits.
- E-4 : campagne interrompue sans résultat, non comptée.
- Contrôles :
  - `test -e` (sans liste) sur `docs/rapports`, `docs/adr-0025`, `docs/pocket-report`, `docs/adr-0028/execution`
    et `docs/adr-0028/monark-m009a`, dans `copie`, `copie2`, `copie3` et `copie4` : tous absents ;
  - `grep` des scripts du générateur (`mesures/`, `amend/`, `genere3.py`) sur les noms d'interdits : aucun (rc 1).
- Aucune pièce interdite n'a été ouverte d'après le rapport, les NOTES et ces contrôles.

### 11. Conflits avec les groupes A et B
Lu : en-têtes des hunks de `p2a/diffs/P2A-1..7` et de `p2b/diffs/GFB-*`, corps de P2A-6 et P2A-7.

**Recouvrements de texte au-delà du plancher et du README :**
- `avant_acte.py` :
  - fin de docstring : les trois groupes y ajoutent une ligne `Phase 2` ;
  - `commit()` : P2A-6 ajoute `motifs(…)` après `workflows(…)`, que P2C-7 réécrit avec `racine=` ;
  - `diff()` : P2A-6 et P2A-7 ajoutent `motifs` et `suivi` après `workflows(…)`, que P2C-6 et P2C-7 réécrivent ;
  - zone entre `workflows()` et `presg5()` : P2C-6 insère avant, P2A-6 insère `motifs()` après ;
  - `parseur()` : P2A-1 et P2A-7 y ajoutent des options, P2C-4 et P2C-7 aussi ;
  - `main()`, entièrement réindenté par P2C-7 (ExitStack) : toute retouche de `main()` par A ou B entre en conflit.
- `garde_commun.py` : fin de docstring.
- `tests/test_avant_acte.py` : GFB-7 touche sa docstring et ses imports, et C y ajoute 7 tests. Ce fichier est hors
  de la liste du brief.

**Dépendances sémantiques :**
- `suivi` (D3 de P2A-7, au `diff`) exige que chaque fonction publique ajoutée dans `scripts/controle/` soit nommée au
  README. Si A passe avant C, le `diff` de C est refusé pour `passees`, `entree_datee`, `unites`, `nommes`,
  `attribuer`, `empreinte_verif` et `remplacees`, absentes des ajouts.
- D4 exige aussi `--rapport` avec un mutant `tué` par test ajouté, ligne par ligne. Le `commit` de la chaîne n'est
  pas touché : `suivi` n'est appelé que par `diff`.
- `--lecture-seule` (P2C-7) : `a.depot` devient un clone sans arbre de travail. Toute fonction de A ou de B qui lit
  un fichier de l'arbre par `a.depot` dans `diff` ou `commit` doit passer à `a.racine`.
  - `suivi` lit le README par `git cat-file` dans l'index temporaire : sans effet.
  - Le lecteur `motifs` ne lit que les lignes ajoutées : sans effet.
- C4 de P2C-2 juge les messages et les ajouts `.md` de A et de B : une heure sans sa date, ou un ajout daté antérieur
  au dernier du fichier, est refusé. Les ajouts des trois groupes se redatent donc tous au pas (Q-1).
- RX de P2A-6 (`motifs_suspects` de l'étape 3-G de A) sur les diffs recalés de C : 7 motifs lus, 0 suspect.
- P2C-4 : A et B ne touchent pas `gabarits/chaine.sh` ; la fonction `verif` du modèle reste celle que la série C
  laisse (les lignes changées par C sont hors de la fonction).

## Observations (non bloquantes)
- O-1 Le geste de `heure-sans-date` (`lire date -u, puis récrire l'heure`) ne dit pas d'écrire la date devant l'heure,
  ni de mettre en code ce qui n'est pas une heure (`chemin:12:34`).
- O-2 `declare -f` : texte formé par bash ; un écart de version de bash entre la chaîne et l'outil changerait
  l'empreinte (même hôte aujourd'hui).
- O-3 `disque` mesure `/`, non le système de fichiers du dépôt (antérieur).
- O-4 Refus C7 répétés pour les rangées du registre en double.
- O-5 `remplacees` : une citation de la dernière ligne d'un fichier sans saut de ligne final ne répond jamais
  (`b < len(t)`) ; elle ne donne qu'un avertissement.

## Items à former (règle PAROXYSME)
1. SHOGEN-FM11-MOTIF-ATTRIBUTION-1 (générateur ; faux positif mesuré ici : 1 compte par ligne `Claude-Session:`).
2. SHOGEN-FM11-MOTIF-SORTIE-SCRATCHPAD-1 (proposé) : `<session>/scratchpad/../…` non compté.
3. SHOGEN-GARDE-ATTRIBUTION-PLAGE-LETTRES-1 (proposé) : plage `DT15-a à DT15-m` non lue ; faux refus mesuré.
4. SHOGEN-GARDE-VERIF-MODELE-CHANGE-1 (proposé) : diff qui change la fonction `verif` du modèle, refusé en C1 par une
   chaîne copiée du modèle d'avant ; C-4 écrit la procédure, un outil pourrait la porter.
5. SHOGEN-GARDE-CHAINE-ORCH-MODELE-1 (proposé) : les chaînes de l'orchestrateur (forme de `chaine_d7.sh`) n'appellent
   pas `avant_acte.py`. P2C-4 et P2C-5 ne les protègent qu'une fois réécrites depuis le modèle.
6. SHOGEN-GARDE-DIFF-SANS-INDEX-1 et SHOGEN-GARDE-JOURNAL-LECTURE-SEULE-1 (générateur), confirmés.

## Pièces
`g2/NOTES.md`, `g2/RAPPORT-G2.md`, `g2/diffs/`, `g2/outils/` (recale.py, corrige.py, fm11_rejeu.py, heures.py,
ajouts_reels.py, attribution10.py), `g2/mutants/` (selection.json, campagne-g2.txt, campagne-g2.err, sortie/),
`g2/SHA256SUMS`.
