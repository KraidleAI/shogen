# Relecture G2 neuve du groupe A (transcrit)

> Transcription par l'orchestrateur le 2026-10-17 07:31:23 UTC du fichier garde-fous/p3a/g2/RAPPORT-G2.md ; contrôle FM-1.1 du transcript du réviseur G2 par le fm11.py versé : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5 (319 occurrences, aucune autre). Texte ci-dessous avec 3 retouche(s) (E35, E38) : noms de marqueur de dette et locutions de la gate S-G4 cités en clair, mis en code, segments de code à doubles accents graves réécrits en segments simples, heures sans date dans les 25 caractères ou approchées mises en code ou entre guillemets français, sans autre changement (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# RAPPORT G2 — GARDE-FOUS phase 3, groupe A (relecture neuve, réviseur distinct du générateur)

Gate 0 : réviseur `claude-opus-5-5` (identifiant de l'environnement de l'agent). Brief : `BRIEF-G2.md` (orchestrateur,
2026-10-16 15:52:57 UTC). Rattachement : ADR-0028, annexe B l.1872, 1875, 1876, 1877. Journal G1 du réviseur : `NOTES.md`.

Base : dépôt à `fe9a72b0503758d7c0e19f1e9a928a5e6d0f3878` (lu, jamais écrit dans l'arbre ; écart E-1 plus bas pour
`.git/shogen-garde/journal.tsv`) ; copie `copie/` par `git archive HEAD` hors interdits (forme exacte de
`copie_creuse`, 1356 fichiers, 0 interdit au compte casse pliée et composant `.jsonl`, noms jamais affichés). Diffs
relus : `../diffs/` GF3A-1, GF3A-2, GF3A-3a, GF3A-3b, GF3A-4, GF3A-5 ; sha256 de leur concaténation dans cet ordre
`689669bf6d5c06bef95466f666c1802769db38bd732493b41638c34c361e0374` (égal à celui du générateur ; `sha256sum -c
../SHA256SUMS` : tout OK). Enregistrement `oracle_record.py` du rôle G2 : sans objet (lot d'outillage, hors du chemin S2).

## Verdict

**ACCEPTE-AVEC-CORRECTIONS**, liste fermée C-1 à C-6 (diffs byte-exacts dans `diffs/`, série à appliquer dans
l'ordre C-1 à C-6 sur la tête de la série du générateur, chacune vérifiée par `git apply --check` sur l'état qui
porte les précédentes, sur un clone neuf de la copie). Plancher du job `controle-unittest` après les corrections :
203 (196 + 7).

| C | diff du générateur | fichier:ligne (tête de la série, `3603b0e` de la copie) | constat | diff |
|---|---|---|---|---|
| C-1 | GF3A-1 | `scripts/controle/fm11.py:23` | regard avant `\S*?` non borné : temps quadratique | `diffs/C-1.diff` |
| C-2 | GF3A-3b | `scripts/controle/avant_acte.py:974-975`, `:979` | K4 : une apostrophe entre guillemets ou en commentaire cache un `$N` | `diffs/C-2.diff` |
| C-3 | GF3A-2 | `scripts/controle/avant_acte.py:345` | plage lue dans une liste sans virgule (`DT15-ba DT15-m`) : faux admis C3 | `diffs/C-3.diff` |
| C-4 | GF3A-5 | `scripts/controle/avant_acte.py:1002-1003` | K7 : un seul `acte commit` admet tout `git commit` nu | `diffs/C-4.diff` |
| C-5 | GF3A-4 | `scripts/controle/avant_acte.py:642-648` | borne de `verser --blanc` tenue par un tuyau : un descendant détaché la défait | `diffs/C-5.diff` |
| C-6 | GF3A-3a, GF3A-4 | `scripts/controle/avant_acte.py:880-882`, `scripts/controle/gabarits/versement.py:28-35`, `scripts/controle/garde_commun.py:529` | propriétés écrites sans cas (mutants du réviseur vivants) | `diffs/C-6.diff` |

## Checklist du brief, point par point

### 1. Application, lignes décalées, plancher — CONFORME

- Les six diffs s'appliquent dans l'ordre sur `fe9a72b` (`git apply --check` puis `--index`, commis pas à pas dans la
  copie : `1de9de0`, `896257b`, `ccf35cf`, `6987ccc`, `3610f48`, `3603b0e`). Aucun ne cesse de s'appliquer.
- README (`scripts/controle/README.md`, listé par `garde/lignes-citees.txt`) : la l.11 remplacée à nombre de lignes
  égal (empreinte de `fm11.py`), tout le reste en fin (`git diff -U0`, en-têtes `@@ -11 +11` puis `@@ -694,0 …` à
  `@@ -749,0 …`). gates.yml : la l.369 seule, remplacée. `fm11.py` l.4 (empreinte `3501489f246ba05c` de
  `lignes-citees.txt`) intacte : recalculée, égale. Les skills et `gabarits/chaine.sh` reçoivent des lignes au milieu,
  mais aucun n'est cité par numéro (ni `lignes-citees.txt` ni `docs/RENVOIS-LIGNES.tsv` ; les seuls renvois `fichier
  l.N` vers les fichiers touchés, dans le README, visent `fm11.py` l.4 et l.19, intactes).
- Plancher : tête 177 (gates.yml de `fe9a72b`) ; tests ajoutés recomptés sur la sortie de la suite : 2 (`test_fm11`)
  + 1 (`Attribution`) + 2 + 1 + 1 (`ChaineABlanc` : 3a, 3b, K7) + 2 (`VersementABlanc`) + 10 (`ChaineModele` : 9
  hérités de `Chaine`, dont 2 redéfinis, plus `test_modele_a_blanc_avant_tout_pas`) = 19 ; 177 + 19 = 196, égal au
  plancher final de GF3A-5. Suite du job à la tête de la série, disque revenu à 6,3 Gio : `verdict-suite-s2 :
  conforme (code 0, résumé final, aucun saut, Ran = 196)` (`preuves/suite-livree-sans-harnais.txt`) ; à la tête des
  corrections : `Ran = 203`, conforme (`preuves/suite-corrigee-sans-harnais.txt`) ; aucune ligne `Exception ignored`
  ni `Warning`.
- Empreintes du tableau du générateur (neuf fichiers) : toutes égales sur ma copie.

### 2. GF3A-1 (fm11) — CONFORME AVEC CORRECTION C-1

- Pied `Claude-Session:` : le regard arrière ne couvre que le texte qui précède immédiatement l'identifiant. Mesuré
  (`travail/fm11_sondes.py`) : pied seul 0 (avant 1) ; pied puis une vraie mention sur la même ligne 1 (avant 2) ;
  sur la ligne suivante 1 ; collée au pied 1 ; URL sans la clé 1 ; clé sans espace ou en minuscules 1 (sens sûr).
  Un vrai fragment placé après le pied reste compté.
- `..` qui ressort du scratchpad, cinq formes : `./../x` compté ; `a/../..` compté ; URL `file://…/scratchpad/../x`
  comptée ; variable (`S=…/scratchpad; cat $S/../x`) non comptée (limite écrite) ; `../x` relatif après un `cd` dans
  le scratchpad non compté, et `%2e%2e` non compté : deux limites non écrites, ajoutées au README par C-1.
- Régression : fm11 avant (`17caaa35…`) et après (`b78a19e9…`), sous la doublure, sur les 19 transcriptions
  synthétiques des 12 tests (`travail/fm11_regression.py`) : 4 écarts, tous attendus (les deux tests neufs ; une
  capture aux comptes égaux dont seule la clé du motif change). Les sorties versées `sorties-fm11/` ne se rejouent pas
  (transcriptions `*.jsonl`, interdites) ; la clé de motif change pour la session et le dossier de session, comme au
  changement Q-3.
- **C-1** : le regard avant `(?!\S*?/[.][.](?![\w.-]))` lit, pour chaque mention du dossier de session suivie de
  `/scratchpad`, toute la suite sans blanc : temps quadratique. Une ligne sans blanc de 4000 chemins du scratchpad
  (JSON compact, 350889 caractères) : 7,854 s, contre 0,001 s avant GF3A-1 ; 1000 chemins 0,438 s, 2000 chemins
  1,695 s (`travail/fm11_sondes.py`, `travail/borne.py`). Le détecteur RX du dépôt (`motifs_suspects`) ne voit que les
  formes exponentielles : il rend `[]` sur ce motif (forme polynomiale, non vue). Correction : `\S{0,4096}?` (PATH_MAX :
  un `..` plus loin n'est pas dans le même chemin) : 0,173 s à 4000 chemins, 0,695 s à 16000. Test
  `test_sortie_du_scratchpad_temps_borne` : rouge avant (7,24 s, `AssertionError: … not less than 3.0`), vert après.

### 3. GF3A-2 (plages en lettres) — CONFORME AVEC CORRECTION C-3

- `rang` (mesuré) : `j` (1, 1, j) ; `z` (1, 1, z) ; `aa` (1, 2, aa) ; `ab` (1, 2, ab) ; `b2` (1, 1, b) ; `10b` (0, 10) ;
  capitale ou vide : None. `DT7-z à DT7-aa` : plage (1, 1, z) à (1, 2, aa), juste ; `DT7-ab` rangé après `aa`.
- Bornes mêlées (`DT15-3 à DT15-c`) : aucune plage (filtre `rang(i)[0] == rang(j)[0]`), juste ; mais aucun test ne
  le gardait (mutant G-c vivant, point 6) : cas ajouté par C-3. Plage inversée (`DT15-m à DT15-a`) : rien couvert,
  refus, juste.
- **C-3, faux admis** : le séparateur se lisait sans blanc devant lui (` ?(?:à|a|au|…|[.]{2,3}) ?`) ; deux diffs
  nommés à la suite sans virgule dont le premier finit par `a` forment une plage : `nommes` rend, mesuré, pour
  `DT15-aa DT15-m` la plage (1, 1, a) à (1, 1, m), pour `Série DT15-ba DT15-m` la plage (1, 1, b) à (1, 1, m) ; un mot
  du message est alors admis pour `DT15-c`, que le passage ne nomme pas. La même lecture valait déjà pour les nombres
  (`GF-1a GF-5` : plage 1 à 5) ; les lettres la rendent fréquente (`aa`, `ba`, … `za`). Correction : séparateur en mot
  entre deux blancs, `…` et `..` inchangés. Test `test_plage_liste_et_bornes_melees` : rouge avant (`DT15-c` admis),
  vert après ; les plages des tests existants (`C-1 à C-3`, `GF-2 … GF-5b`, `C-1 à C-10`, `INT-01 à INT-25`) restent
  lues.

### 4. GF3A-3a, 3b, 4 (`chaine --blanc`, `verser --blanc`) — CONFORME AVEC CORRECTIONS C-2 ET C-5

- `chaine --blanc` sur les chaînes réelles (`preuves/blanc-chaines-reelles.txt`, six diffs de la série) :
  `chaine_int.sh`, `chaine_fus2.sh`, `chaine_cq.sh` : chacune `REFUS K2` (`set -euo` sans `-E` ; `chaine_fus2.sh` a
  bien un `trap … ERR` l.23, mais sans errtrace il ne vaut pas dans `verif`) et deux `REFUS K7` (verif écrite ; `git
  commit` sans `acte commit`) : refus justes (la `verif` recopiée de `chaine_int.sh` l.10 lit `xtask-d7.log` au lieu
  de `xtask-int.log` : la recopie est le défaut que K7 vise). Aucun K1, K3, K4 : justes (`un` protège `${4:-}` et
  `${5:-}` ; `readme` est appelée avec ses deux arguments). `chaine-modele.sh` : sortie 0. `gabarits/chaine.sh` lui-même :
  K2 et K7, comme son README l'écrit.
- K4 statique (`travail/sondes_k.py`, `preuves/sondes-k4-k7.txt`) : `${2}` sans `:-` : refusé, juste ; `"$@"` sans
  argument : admis, juste (bash 5.2.21 sous `set -u` : sortie 0) ; `shift` puis `$1` : admis (limite écrite ; bash :
  `$1: unbound variable`) ; `function f {` : non lu comme fonction, `$2` refusé comme hors de toute fonction (sens
  sûr). **C-2** : faux admis mesurés : `echo "l'arbre $2 n'est pas propre"`, une apostrophe entre guillemets sur deux
  lignes du corps, une apostrophe dans deux commentaires du corps : le motif `'[^']*'` ôte le texte entre deux
  apostrophes sans voir les guillemets ni les commentaires, et le `$2` disparaît ; `${2:0:1}`, `${#2}` et `${10}`
  (bash : `unbound variable`, mesuré) ne sont pas lus. Le cas E34 est un `$4` dans `un()`, et les messages de ces
  chaînes sont en français : les apostrophes y sont ordinaires. Correction : `litteraux_otes` (chaînes et commentaires
  lus comme bash) et `LIT_N`. Test `test_k4_apostrophes_et_formes` : rouge avant (`'' != 'REFUS K4 '`), vert après ;
  les six chaînes de la session ne prennent aucun K4 neuf (`preuves/c2-chaines-reelles.txt`).
- `verser --blanc` avec `SHOGEN_DEPOT` : `verser_cq.py` (sha256 `9c4ddf4d…`, il ne lit pas la variable), joué sous une
  vue en lecture seule du dépôt : `REFUS V8 : le script ne lit pas SHOGEN_DEPOT … (non lancé)` : refusé comme annoncé
  (`preuves/v8-verser-cq.txt`). Limite non écrite (observation O-3) : le contrat est lu sur les octets ; un script qui
  nomme la variable sans la lire (le cas `# SHOGEN_DEPOT ignoré` du test du générateur) est lancé et écrit dans le
  vrai dépôt, refusé après coup.
- **C-5, borne** : `p.communicate(timeout=BORNE_VERSER)` lit un tuyau jusqu'à sa fin : un descendant du script, dans
  sa propre session, qui garde la sortie retient l'outil. Mesuré (borne 2 s, descendant de 12 s,
  `preuves/sonde-borne-verser.txt`) : script sorti à 0 : `ERREUR … script au-delà de 2 s` en 12,1 s (faux) ; script
  qui boucle : 12,1 s. Correction : sortie dans un fichier du dossier temporaire, `p.wait(timeout=…)`. Test
  `test_borne_et_descendant_detache` : rouge avant (`Ran 1 test in 30.161s`, attendu `(0, True)`), vert après.
- V9 sur la vraie `biblio/INDEX.md` (trouvée par le skill `shogen-avant-committer`, point 5 ; la copie sert de dépôt) :
  rangée de 7 cellules : 0 ; gabarit à 8 : `REFUS V8 … REFUS biblio/INDEX.md:469 : 8 cellules, en-tête de 7` avant
  écriture ; script brut à 8 : `REFUS V9 : biblio/INDEX.md:469 : 8 cellules, en-tête de 7 (E32)`. L'INDEX finit sur
  son dernier tableau (en-tête l.466, 7 colonnes) ; `rangees_fautives` sur toutes ses lignes : 0 (pas de faux refus).
- Options retirées d'argparse : le code exige toujours `--plan` et `--cc` ensemble ou `--blanc` (sinon erreur 3 :
  `chaine --plan d1` mesuré par le test), `--pieces` ou `--blanc --script` ; le crochet GARDE-FAITS ne lit pas ces
  options (aucune mention de `chaine` ni `verser` dans `garde_faits.py`). `EXIGES` garde la présence de `--plan`,
  `--cc`, `--pieces` au texte des skills : suffisant, rien n'est desserré au skill. Seule voie neuve : `chaine --blanc
  --diffs` sans plan saute G1 à G4 ; voulue (chaîne sans plan), et le modèle passe toujours `--plan --cc --blanc`.

### 5. GF3A-5 (modèle, `source` de la `verif` scellée) — CONFORME AVEC CORRECTION C-4

- K7 : chaînes réelles refusées (point 4), modèle admis. **C-4** : la garde du commit lisait le texte entier : un
  seul `acte commit … && git commit` admet tout autre `git commit` nu ; `git --no-pager commit` et `git -c
  user.name="b c" commit` ne sont pas lus comme commits (mesuré : admis tous les trois). Correction : `commits_nus`,
  par ligne, mots lus par shlex, options globales sautées ; `git commit-tree` n'est pas un commit. Test
  `test_k7_chaque_commit_garde` : rouge avant (`REFUS K7` attendu, rien rendu), vert après. Reste vu, non corrigé
  (observation O-5) : `function verif {` (sans parenthèses) n'est pas lu comme une verif écrite ; C1 la refuse au
  sceau (empreinte autre).
- `unshare -n` sur l'hôte (`travail/unsh/joue.sh`) : root, `unshare -n true` 0, `lo` allumée et joignable ; `verif`
  tirée par `source` sur un dépôt factice : droits pleins 0 ; capacités ôtées (`setpriv --bounding-set -all`) :
  `unshare failed: Operation not permitted`, `verif` 1 ; `unshare` absent du PATH : `verif` 1. La chaîne s'arrête
  donc rouge (`vérification rouge avant …`), jamais verte sans isolement.
- Empreinte : `8fa5ee9f…` avant, `e0254878…` après, recalculées par `empreinte_verif` ; la `verif` tirée par le
  `source` du modèle a la même empreinte `e0254878…`.
- Procédure de resceau : écrite (README de GF3A-5 et rapport du générateur, une phrase), juste dans son principe,
  incomplète sur deux points mesurés (observation O-4, procédure complète plus bas) : la copie des outils doit être
  un arbre entier (gates.yml et `enforcement/docs-sha256sums.py` lus à `../..` de `OUTILS` : sinon `chaine --blanc`
  sort en 3, mesuré) ; et la chaîne doit être `chaine-modele.sh` de cette copie : une chaîne à `verif` écrite (forme de
  `chaine.sh` d'avant) scelle `8fa5ee9f…`, que l'outil d'après refuse à chaque pas.
- Portes Python de gates.yml jouées comme la `verif` neuve les joue (même `grep`, même `sed`, même enveloppe :
  variables de mandataire retirées, `unshare -n`, `lo` allumée par son ioctl ; cargo non lancé ;
  `travail/portes_isolees.sh`, `preuves/portes-isolees.txt`) sur la tête corrigée : 15 lignes, toutes à 0 sauf
  sim-bis, en échec faute d'historique dans la copie (`git archive f35a70c19ba8 : sortie 128`, artefact de ma
  mesure) ; rejouée sur la même copie portée par un clone partagé sans extraction du dépôt (historique présent) :
  `Ran 279`, `OK`, sortie 0, isolée comme sans `unshare` (`preuves/simbis-isolee.txt`). L'isolement de la `verif`
  ne rougit donc aucune porte.
- `chaine.sh` d'avant et ses copies en marche : `chaine --plan --cc` sans `--blanc` suit le même chemin qu'avant
  (G1 à G4 ; la classe `Chaine` passe, 9 tests) ; K7 n'est joué qu'à `--blanc`. Une copie en marche qui prend `OUTILS`
  dans le dépôt est refusée en C1 dès que GF3A-5 y est commis (`MODELE` change) : arrêt rouge, jamais un commit
  silencieux.

### 6. Mutants — voir la section Mutants

### 7. Écarts du générateur — CONFORME

- Les deux `git diff --cached` sans liste de chemins ont tourné dans la copie du générateur : son archive (branche
  `serie5` et `HEAD`, 1356 fichiers) porte 0 interdit (compte en mémoire, noms jamais affichés) ; aucun nom interdit
  n'a pu s'afficher. M1d (lot 1) : écarté et refait en M1d-bis, comptes des lots relus (lot 1 : 24 tués, lot 2 : 24
  tués et M5j vivant, lot 3 : M5j tué, lot 4 : 9 tués ; témoins vivants). Aucune pièce interdite ouverte dans les
  pièces du générateur que j'ai lues. Arbre du dépôt : `git status --porcelain` sur `scripts .github .claude
  enforcement JOURNAL.md docs/adr-0028/ANNEXE-B-items.md biblio s2bis s2-harness` : vide.

### 8. S-G5 et R-13 — voir la section Contrôles des pièces

### 9. Dépendances hors des lignes annoncées (groupes B et C)

Lu : noms des fichiers touchés par les diffs de `../../p3b/diffs/` et `../../p3c/diffs/` (lignes `diff --git`) et le
diff GF3C-2. Dans les diffs du groupe A, dépend d'autre chose que du plancher, du README, de `test_skills.py`, de
`motifs`/`refus`, de `disque`/`--lecture-seule` et de `.gitignore` :
- `motif_r13` lit l'unique ligne de gates.yml qui porte `git grep -nE '` (job g5) et ses exclusions `':!…'` : un
  changement de cette étape par B ou C change K6 ; deux lignes de cette forme font sortir `chaine --blanc` en 3.
- `copie_creuse` lit `INTERDITS` dans `enforcement/docs-sha256sums.py` (constante lue, non recopiée).
- `chaine-modele.sh` recopie la boucle de `chaine.sh` (`acte disque --min-go`, `acte sceller`, `acte commit`) : un
  changement de la boucle ou des options de `disque` (B-5) doit être porté aux deux fichiers.
- GF3A-5 change la `verif` scellée (`MODELE`) : tout diff de B ou C qui touche `gabarits/chaine.sh` entre `verif() {`
  et `# --- fin de verif` change encore l'empreinte (resceau).
- `motifs --arbre` (GF3C-2) jugera tous les motifs des `.py` de `scripts/controle/`, dont ceux du groupe A (fm11,
  `LIT_N`, `rang`, `nommes`, K7, `rangees_fautives`) : `motifs_suspects` rend `[]` sur chacun, mesuré ; il ne voit
  pas la forme quadratique de C-1.
- `garde_commun.py` : GF3A-4 et GF3C-2 ajoutent tous deux en fin, après `motifs_ajoutes` (contexte seul).
- `tests/__init__.py` touché par GF3C-3 : les classes de test neuves du groupe A tournent sous lui.

## Corrections (liste fermée)

Chaque correction : test écrit d'abord et vu rouge sur la tête de la série, puis code ; ajout daté en fin de
`scripts/controle/README.md` (`date -u`), plancher recalé par diff (`--egal`) ; diffs faits par `git diff --cached`
limité à `scripts .github .claude` dans `corr/` (dépôt local de la copie), saut de ligne final, chemins `a/` et `b/`
relatifs. Lignes ajoutées (lignes `+` hors en-têtes) : C-1 30, C-2 47, C-3 24, C-4 44, C-5 51, C-6 34 (R-25).

- **C-1** (`diffs/C-1.diff`, GF3A-1, `scripts/controle/fm11.py:23`) : `\S*?` devient `\S{0,4096}?` dans le regard
  avant du dossier de session (barres écrites par `chr(92)` et contrôlées sur les octets : trois par ligne, `\w`,
  `\S`, `\w`) ; sha256 de `fm11.py` `e9c80fa1d98e54c202a82badf445081ce33557a4f6dfd4498bd1c1e8543e7a2d` reporté à
  `SHA256SUMS`, `tests/test_fm11.py` (`SHA_FM11`) et README l.11 (remplacement à nombre de lignes égal ; `fm11.py` l.4
  intacte) ; test `test_sortie_du_scratchpad_temps_borne` (4000 chemins en moins de 3 s ; `..` à 5001 caractères non
  compté, à 4001 compté) ; plancher 197.
- **C-2** (`diffs/C-2.diff`, GF3A-3b, `scripts/controle/avant_acte.py:974-975` et `:979`) : `litteraux_otes` (chaînes
  entre apostrophes hors guillemets et commentaires ôtés, comme bash les lit) et `LIT_N` (`$N`, `${N}`, `${#N}`,
  `${N:…}` hors protection `-`, `?`, `+`, `=`, `${10}`) remplacent le motif `'[^']*'` et `[$][{]([1-9])[}]`, dans le
  corps des fonctions et hors fonction ; test `test_k4_apostrophes_et_formes` ; plancher 198.
- **C-3** (`diffs/C-3.diff`, GF3A-2, `scripts/controle/avant_acte.py:345`) : séparateur `(?: (?:à|a|au) | ?(?:…|[.]{2,3}) ?)` ;
  test `test_plage_liste_et_bornes_melees` (liste sans virgule refusée hors de ses diffs, bornes mêlées) ; plancher 199.
- **C-4** (`diffs/C-4.diff`, GF3A-5, `scripts/controle/avant_acte.py:1002-1003`) : `commits_nus` et `GIT_OPT2` ;
  test `test_k7_chaque_commit_garde` (second commit nu, `--no-pager`, `-c` à valeur entre guillemets, `acte commit ;
  git commit` refusés ; `git log`, `git commit-tree` et le commit gardé admis ; `verif` tirée par une ligne commentée
  ou par un `source` du fichier entier, sans `verif` : refusées, cas qui tuent G-g et G-i) ; plancher 200.
- **C-5** (`diffs/C-5.diff`, GF3A-4, `scripts/controle/avant_acte.py:642-648`) : sortie du script de versement dans
  `versement.log` du dossier temporaire (hors de la copie), `p.wait(timeout=BORNE_VERSER)`, `lire` ensuite ; test
  `test_borne_et_descendant_detache` (descendant détaché qui garde la sortie : script sorti à 0 rendu 0, script qui
  boucle rendu 3, chacun en moins de 10 s ; à la borne, l'enfant du même groupe est arrêté, ce qui tue G-f ;
  descendants arrêtés par le test) ; plancher 201.
- **C-6** (`diffs/C-6.diff`, GF3A-3a et GF3A-4) : deux tests de propriétés écrites que rien ne gardait (mutants du
  réviseur G-a, G-b, G-e, G-l, G-m vivants sur la série livrée) : `test_copie_creuse_exclut_les_interdits`
  (`docs/rapports/`, `docs/15-`, `*.jsonl` à la racine et en sous-dossier : absents de la copie creuse ; le reste
  présent) et `test_gabarit_refus_et_barre_echappee` (cible hors du dépôt, cible sans saut de ligne final : V8 avant
  écriture ; rangée à barre échappée : admise) ; plancher 203.

## Procédure de resceau pour la chaîne qui commet la série (observation O-4, à la charge de l'orchestrateur)

1. Arbre des outils d'après la série : `git archive HEAD` du dépôt (interdits exclus) dans un dossier neuf, puis les
   six diffs et C-1 à C-5 appliqués dans l'ordre ; `OUTILS=<arbre>/scripts/controle` (l'arbre entier : gates.yml et
   `enforcement/docs-sha256sums.py` y sont lus).
2. Chaîne : `chaine-modele.sh` de cet arbre, copié tel quel (jamais une `verif` écrite ou recopiée) ; `DEPOT` le dépôt,
   `OUTILS` comme au point 1 ; la `verif` tirée par `source` y est `e0254878…`, égale au `MODELE` de cet `OUTILS` : C1
   admet chaque pas, GF3A-1 à GF3A-4 compris.
3. Avant le lancement : disque libre au moins 3 Gio (LN-1 ; 2,957 Gio mesurés à `16:0x` UTC : la chaîne serait arrêtée
   au premier pas) ; `unshare -n` exige les droits de l'hôte (root ici, mesuré).
4. Après la série : `OUTILS` peut revenir au dépôt (son `chaine.sh` porte la même `verif`).

## Observations hors liste (non bloquantes ; items proposés, règle PAROXYSME)

- **O-1, disque de l'hôte** : `shutil.disk_usage('/')` : 2,957 Gio libres (seuil de refus 3, `SEUILS_GIO`). La suite du
  job à la tête de la série (`preuves/suite-finale.txt`) : `Ran 196`, 13 échecs, tous des cas de chaîne
  (`ROUGE disque avant X-1 (LN-1)`) ; les mêmes cas échouent à la base `8e3cfa6` : environnement. Mesures vertes faites
  sous un harnais de disque (`mut/`, `mutc/` : lecture réelle + 8 Gio quand `disk_usage` est la fonction de `shutil`,
  lectures simulées des tests inchangées ; seule différence avec la tête, `diff` à l'appui dans `NOTES.md`). Toute
  chaîne de l'orchestrateur est refusée au premier pas tant que le disque reste sous 3 Gio. En fin de relecture, le
  disque est revenu à 6,3 Gio (place libérée, dont mes copies mutées) : les deux suites, sans harnais, sont conformes
  (point 1).
- **O-2, journal des actes** : `chaine --blanc` et `verser --blanc` écrivent une ligne au journal
  `.git/shogen-garde/journal.tsv` du dépôt passé par `--depot`, et `--lecture-seule` n'est admis que pour `diff` et
  `commit` : un passage à blanc d'un réviseur sur le vrai dépôt écrit dans `.git` (mon écart E-1). Proposé :
  SHOGEN-GARDE-BLANC-LECTURE-SEULE-1 (`--lecture-seule` admis pour `chaine --blanc` et `verser --blanc` ; à rapprocher
  de B-4 du groupe B).
- **O-3, contrat de `verser --blanc` lu sur les octets** : un script qui nomme `SHOGEN_DEPOT` sans le lire est lancé et
  écrit dans le vrai dépôt ; V8 le refuse après coup (le test `test_e33_e35_portes_et_contrat` le montre sur un dépôt
  de test : `?? z.md`) ; une écriture dans un chemin ignoré du dépôt n'est pas vue (`git status` sans `--ignored`).
  Proposé : SHOGEN-GARDE-VERSER-DEPOT-RO-1 (script lancé sous une vue en lecture seule du dépôt : `unshare -m`, montage
  lié `ro`, mesuré sur l'hôte : `touch` refusé, `Read-only file system`), à joindre à SHOGEN-GARDE-VERSER-HORS-COPIE-1
  du générateur.
- **O-4, resceau** : procédure complète ci-dessus ; la phrase du README de GF3A-5 suffit à l'orchestrateur s'il lit
  aussi cette procédure.
- **O-5, K7** : `function verif {` (sans parenthèses) n'est pas lu comme une `verif` écrite, ni par K4 comme une
  fonction ; un `source` d'un autre `OUTILS` que celui d'`acte` n'est pas vu (limite écrite). C1 reste la garde au
  sceau. Proposé : SHOGEN-GARDE-K7-FUNCTION-1.
- **O-6, détecteur RX** : `motifs_suspects` ne voit que les formes exponentielles ; la forme quadratique de GF3A-1
  (C-1) a passé `avant_acte.py diff` (RX). Proposé : SHOGEN-MOTIFS-POLYNOMIAL-1 (regard avant non borné après un
  préfixe répétable).
- **O-7, copie creuse** : les exclusions de `copie_creuse` sont sensibles à la casse (`:(exclude)docs/rapports`) alors
  que `interdit()` plie la casse ; à la tête `fe9a72b` aucun chemin n'est concerné (0, compte casse pliée sur l'archive) ;
  une pièce nommée en capitales serait extraite dans le dossier temporaire (jamais lue ni affichée par l'outil).
  Proposé : magie `icase` dans les exclusions (SHOGEN-GARDE-COPIE-ICASE-1).
- **O-8, borne de `verser --blanc` après C-5** : le descendant détaché survit à l'outil (écrit au README de C-5).
  Proposé : SHOGEN-GARDE-VERSER-ORPHELINS-1 (moissonneur, comme `mutants.py`).

## Mutants

Outil du dépôt `scripts/controle/mutants.py` (relu, lu seulement), job `controle-unittest` (commande lue dans gates.yml
de la copie mutée), borne 300 s, classement par la sortie (1 tué, 0 vivant, autre FATAL) ; copies mutées à part
(`mut/` = tête de la série, `mutc/` = tête des corrections, chacune avec le seul harnais de disque d'O-1) ; témoin
vivant à chaque lot ; relevé `ps` de fin vide à chaque lot (44, 22 et 40 groupes). Diff et sortie de chaque mutant :
`mutants/lot-<a|b|c>/<id>.diff|.out` ; tests en échec relus dans chaque sortie (`travail/attribuer.py`,
`preuves/mutants-lot-*-attribution.txt`). Aucun FATAL, aucun équivalent déclaré.

- Lot a, 21 mutants du générateur rejoués sur la série livrée (dont GF3A-4 : M5a, M5c, M5d, M5e, M5i, M5j ; GF3A-5 :
  M6a, M6b, M6c, M6h, M6k) : 21 tués, par les tests que le générateur nomme (relu mutant par mutant).
- Lot b, 10 mutants du réviseur sur la série livrée : **10 vivants** : G-a (exclusion `*.jsonl` de la copie creuse
  retirée), G-b (exclusions `INTERDITS` retirées), G-c (filtre des bornes mêlées retiré), G-d (motif `'[^']*'` retiré
  du corps des fonctions), G-e (barre échappée comptée), G-f (`os.killpg` remplacé par `p.kill()`), G-g (lignes
  commentées lues par K7), G-i (`verif` non exigée sur la ligne du `source`), G-l (garde du gabarit contre une
  cible hors du dépôt retirée), G-m (garde contre une cible sans saut de ligne final retirée). D'où C-3 (G-c), C-4 et C-5 serrées (G-g, G-i, G-f),
  C-6 (G-a, G-b, G-e, G-l, G-m) ; G-d n'a plus d'objet après C-2 (code remplacé, MC2c le reprend).
- Lot c, 19 mutants sur la série corrigée : 19 tués.

Ligne par test ajouté par les corrections (forme de D4 : nom du test et mutants tués sur la même ligne) :
- `test_sortie_du_scratchpad_temps_borne` : mutants tués MC1a (borne retirée), MC1b (borne 8192).
- `test_k4_apostrophes_et_formes` : mutants tués MC2a (motif `$N` d'avant), MC2b (commentaires non ôtés), MC2c (guillemets ignorés).
- `test_plage_liste_et_bornes_melees` : mutants tués MC3a (séparateur d'avant), MC3b (filtre des bornes mêlées retiré, G-c).
- `test_k7_chaque_commit_garde` : mutants tués MC4a (garde sans `&&`), MC4b (`-c` sans valeur), MC4c (options non sautées), G-g, G-i.
- `test_borne_et_descendant_detache` : mutants tués MC5a (tuyau d'avant C-5), MC5b (`p.kill()` au lieu du groupe, G-f).
- `test_copie_creuse_exclut_les_interdits` : mutants tués G-a, G-b.
- `test_gabarit_refus_et_barre_echappee` : mutants tués G-e, G-l, G-m.

Les mutants de `fm11.py` sont aussi tués par `Empreintes` (sha256 épinglé) ; l'attribution relue montre que le test de
comportement échoue aussi (MC1a, MC1b : `test_sortie_du_scratchpad_temps_borne` ; M1a, M1c, M1e du lot a : les deux
tests de GF3A-1).

## Contrôles des pièces (point 8 du brief)

- R-13 : motif de l'étape du job g5 lu dans gates.yml, joué sur les lignes ajoutées de chaque diff
  (`preuves/r13-diffs.txt`) : GF3A-1 à GF3A-5 et C-1 à C-6 : `grep` sortie 1 (aucun) ; aucun marqueur de dette dans
  `../RAPPORT-GENERATEUR.md`, `../NOTES.md`, ce rapport, `NOTES.md` (`grep -c` : 0).
- S-G5 : `presg5.py` sur `../RAPPORT-GENERATEUR.md`, `../NOTES.md`, ce rapport et `NOTES.md` : `0 fragment(s)
  introuvable(s)` chacun (`preuves/juger-diffs.txt` pour les deux derniers).
- `avant_acte.py diff --fichier <diff> --rapport <rapport>`, chaque diff sur l'état qui porte les précédents
  (`travail/juger.sh`, `preuves/juger-diffs.txt`) : les six diffs du générateur avec son rapport, puis C-1 à C-6 avec
  ce rapport : douze sorties 0 (D3 README, D4 mutant tué par test compris).

## Écarts du réviseur

- **E-1** : cinq passages de `chaine --blanc` sur les chaînes réelles ont pris `--depot /home/user/shogen` (`16:05:32` à
  `16:09:10` UTC) : l'outil a ajouté 12 lignes (K2, K7, une conforme) au journal `.git/shogen-garde/journal.tsv` du
  dépôt (hors de l'arbre, non suivi ; observation O-2). Rien d'autre n'est écrit au dépôt. Les lignes portent ces
  heures ; à retirer ou à garder comme passages G2, au choix de l'orchestrateur. Les passages suivants ont pris la
  copie pour dépôt, ou une vue `ro` du dépôt.
- **E-2** : `git checkout --detach`, `git reset --soft` et `git commit` ont tourné dans les dépôts locaux de mes
  copies (`corr/`, `copie/`), jamais dans le dépôt du projet ; un `git clone --shared --no-checkout` du dépôt
  (`tmp/hist`, supprimé en fin) a servi à rejouer sim-bis avec l'historique.
- **E-3** : premier lancement de la campagne a arrêté par l'outil (témoin mort : harnais de disque faux) ; sorties
  gardées dans `mutants/ecarte/`, aucune compte.

## Journal de provenance (résumé ; détail dans `NOTES.md`)

- [lu] `BRIEF-G2.md`, `../BRIEF.md`, `../RAPPORT-GENERATEUR.md`, `../NOTES.md`, `../SHA256SUMS`, les six diffs en
  entier, `../patches/mutants-lot1.json` à `mutants-lot4.json`, `../mutants/lot1.txt` à `lot4.txt` (comptes),
  `../preuves/juger-diffs.txt` ; `scripts/controle/avant_acte.py` (parties : en-tête, `garde`, `sceller`,
  `empreinte_verif`, `disque`, `chaine`, `copie_creuse` à `blanc`, `verser_blanc`, `journal`, `parseur`, `main`),
  `garde_commun.py` (`etat_disque`, `motifs_suspects`, `rangees_fautives`), `fm11.py`, `gabarits/chaine.sh`,
  `gabarits/chaine-modele.sh`, `gabarits/versement.py`, `tests/test_fm11.py`, `tests/test_skills.py`,
  `tests/test_gabarit_chaine.py` (parties), `tests/test_avant_acte.py` (parties), `garde/lignes-citees.txt`,
  `docs/RENVOIS-LIGNES.tsv` (lignes de gates.yml), les deux skills, `mutants.py` (docstring), `biblio/INDEX.md`
  (structure des tableaux), `scripts/sim-bis/oracle_r1.py` (`extraire`) ; `ERREURS-ORCHESTRATEUR.md` (E30 à E36) ;
  chaînes `chaine_int.sh`, `chaine_fus2.sh`, `chaine_cq.sh`, `verser_cq.py`, `isole.sh` du scratchpad ; noms des
  fichiers touchés par les diffs des groupes B et C, et le diff GF3C-2. Aucune source [abs] ni [2nd].
- Chiffres : tous affichés par un outil dans ce journal (suites, campagnes, sondes, `sha256sum`, `grep -c`, `awk`).
- Pièces interdites : aucune ouverte ; copies faites par `git archive` hors interdits, comptes en mémoire seulement.

sha256 de la concaténation de C-1 à C-6, dans cet ordre : `47003d959c3754a105ec181253f2d04379681c9a98aa54f24cd3f2a085f0e563` ; tête des corrections dans `corr/` : `8643b6c35466a72100d85b2b7e171103874309c5` (branche `serie-c`).
