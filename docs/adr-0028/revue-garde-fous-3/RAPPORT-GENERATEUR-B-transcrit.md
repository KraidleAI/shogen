# Rapport du générateur du groupe B (transcrit)

> Transcription par l'orchestrateur le 2026-10-17 07:31:23 UTC du fichier garde-fous/p3b/RAPPORT-GENERATEUR.md ; contrôle FM-1.1 du transcript du générateur par le fm11.py versé : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5 (238 occurrences, aucune autre). Texte ci-dessous avec 1 retouche(s) (E35, E38) : noms de marqueur de dette et locutions de la gate S-G4 cités en clair, mis en code, segments de code à doubles accents graves réécrits en segments simples, heures sans date dans les 25 caractères ou approchées mises en code ou entre guillemets français, sans autre changement (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Rapport du générateur G1 — GARDE-FOUS phase 3, groupe B (crochet GARDE-FAITS et `avant_acte.py`)

- **Gate 0** : modèle `claude-opus-5-5` (effort `high`), worker `shogen-worker`.
- Rédigé le 2026-10-16 14:39:16 UTC (`date -u`). Brief : `BRIEF.md` de ce dossier (orchestrateur, `13:32:40` UTC).
- Rattachement : ADR-0028, annexe B, B.108 (l.1873, 1878, 1879, 1880) et B.109 (l.1891) ; lignes relues à la tête
  `fe9a72b` : mêmes items aux mêmes numéros.
- Base de la copie : `fddedcfe6c64c43c5c25aa1477f1b8fe1d6f9933` (fusion de B.110). Le dépôt a avancé pendant le travail
  à `fe9a72b0503758d7c0e19f1e9a928a5e6d0f3878` (un commit, FORGE-PR12) : il ne touche aucun chemin des diffs
  (`git diff --stat` vide sur la liste explicite des chemins touchés) ; écart rendu à l'orchestrateur, base non avancée
  par le générateur.
- Série, dans cet ordre (chaque diff s'applique sur la base plus les précédents ; `git apply --check` vert pas à pas) :

| diff | item | lignes ajoutées | sha256 |
|---|---|---|---|
| `diffs/B-1-erreur-interne.diff` | SHOGEN-GARDE-ERREUR-INTERNE-1 | 181 | `d17157ad2b4b6b79624ce753e9e8ab9cfd5e98ffa6d1a74aac75a0a038f35f3c` |
| `diffs/B-2-message-chaine.diff` | SHOGEN-GARDE-CROCHET-MESSAGE-CHAINE-1 | 80 | `7e7dcb3574209f38fe21430e5b808eb854b97e5fa531dc8cc1568a97aeae5927` |
| `diffs/B-3-reponse-investisseur.diff` | SHOGEN-GARDE-REPONSE-INVESTISSEUR-1 | 182 | `3ce9daf859ecee95946388233a9bec6116eba1ea94da6388bb9f995ff54f6d8b` |
| `diffs/B-4-journal-lecture-seule.diff` | SHOGEN-GARDE-JOURNAL-LECTURE-SEULE-1 | 120 | `84d3b4c30199c541fc2fc8a8e06a59af7f4c438fc1240a90d41a84f7674c602e` |
| `diffs/B-5-disque-du-depot.diff` | SHOGEN-GARDE-DISQUE-DU-DEPOT-1 | 102 | `eeb580d9015970b42cad7eeb67e55de5be7390990191b3b7b7472f9440a97070` |

Concaténation dans l'ordre de la série : sha256 `2fe76b3cdaa8e076189bdedb1aa1e52a39f4477961f39973ce433195a8333294`.

Contrôles faits sur la copie (jamais le dépôt) : ligne du job `controle-unittest` après chaque diff, verdict conforme,
`Ran` 180, 182, 185, 188, 191 (plancher recalé à chaque diff, `--egal`) ; `avant_acte.py diff --fichier <diff>
--rapport RAPPORT-GENERATEUR.md` sur chaque pas (outil de la tête, dépôt jetable `verif/` qui porte aussi
`biblio/INDEX.md` et `docs/RENVOIS-LIGNES.tsv` de la tête) : voir NOTES ; motif R-13 du job g5 (extrait de `gates.yml`
à l'octet) sur les lignes ajoutées : 0 par diff ; aucun cargo.

Campagne de mutants : `scripts/controle/mutants.py` de l'arbre de la tête (`orig/`), sur la copie à l'état final, job
`controle-unittest`, borne 300 s, groupes de processus neufs ; témoin vivant ; 34 mutants, 34 tués (sortie 1), aucun
vivant, aucun FATAL ; relevé `ps` de fin : aucun processus des 70 groupes. Pièces : `mutants/mutants.json` (sha256
`5aea3f5fc65533402637fdd52fcc409807643b2b5899e7b1a9e4916f7dc3448f`), `mutants/campagne.txt` (une ligne JSON par run,
sha256 `d0f95c6bdb6f0ad7f97023bd79c1e6923ed2da41df8936f838d129f45449d20f`), `mutants/sortie/<id>.diff` et `<id>.out`,
`mutants/generer.py` (substitutions, chacune unique dans son fichier).

## B-1 — SHOGEN-GARDE-ERREUR-INTERNE-1 (B.109, l.1891)

**Ce qu'il refuse** : une exception levée pendant le jugement d'un PreToolUse dont l'acte écrit, commet, pousse,
supprime, lance un agent ou crée une PR (R1 à R3, R5, R8) ; même règle au journal illisible (`pre_tool_use`, ancienne
l.610). Lecture pure (`lecture_pure` : programmes de lecture nommés, git en lecture sans `--output` ni `$`, aucune
redirection d'écriture, substitution ni affectation ; `mcp__github__` `get_`, `list_`, `search_`) : permise, erreur
écrite sur stderr et au journal des décisions. Stop, SubagentStop, UserPromptSubmit : permis, erreur écrite. Table
des cas dans l'ajout daté du README.

**Preuve** : `tmp/ei-rouge.txt` (3 échecs, dont le cas réel de la G2 : `(0, False, True) != (2, True, True)`) ;
`tmp/ei-vert.txt` (OK).

**Mutants tués, par test** :
- `test_cas_reel_de_la_g2_refuse` : M1-1 tué (bloc de refus de `main` retiré : retour à `acte permis sans contrôle`),
  M1-2 tué.
- `test_table_des_cas` : M1-2, M1-3, M1-4, M1-5, M1-7, M1-8, M1-9, M1-10, M1-11, M1-12 tués (Bash jugé lecture,
  redirections non lues, `$` sur git admis, `--output` admis, mcp tout permis, affectation en tête admise, séparateurs
  non découpés, `2>/dev/null` non retiré, exception du classement tenue pour lecture, `sed` ajouté aux lectures).
- `test_journal_illisible` : M1-6 tué (refus du journal illisible retiré), M1-2 tué.

**Limites** : une entrée qui n'est pas du JSON sort 0 (aucun acte nommé) ; une entrée JSON qui n'est pas un objet lève
avant le `try` (sortie 1 de Python, que Claude Code ne tient pas pour un refus) ; la liste des lectures est étroite
(une lecture hors liste, ou un séparateur entre guillemets, est refusée en cas d'erreur : sens sûr, coût possible d'un
faux refus pendant une panne du crochet).

**Phrase de fermeture proposée** : SHOGEN-GARDE-ERREUR-INTERNE-1 fermé par B-1 : une erreur interne ou un journal
illisible pendant le jugement d'un acte qui écrit, commet, pousse, supprime ou crée une PR est un refus qui nomme
l'erreur ; une lecture pure reste permise, l'erreur écrite ; cas réel de la G2 refusé ; 3 tests, mutants M1-1 à M1-12
tués.

## B-2 — SHOGEN-GARDE-CROCHET-MESSAGE-CHAINE-1 (B.108, l.1880)

**Ce qu'il change** : `faits_et_appels` lit un message humain à `content` chaîne comme un texte entier (et non
caractère par caractère) ; la forme liste de blocs est inchangée. R5 voit l'identifiant et le compte qu'un tel message
porte.

**Preuve** : `tmp/mc-rouge.txt` (2 échecs : R5 refusait `4f3e2d1`, et `faits_et_appels` rendait un caractère par
entrée) ; `tmp/mc-vert.txt` (OK).

**Mutants tués, par test** :
- `test_r5_voit_le_message_a_contenu_chaine` : M2-1 tué (boucle d'avant rétablie).
- `test_faits_et_appels_deux_formes` : M2-1 tué.

**Limites** : effet sur R6, dont le code n'est pas touché : son corpus reçoit le texte humain entier ; un chiffre
isolé d'un message humain ne couvre plus un nombre d'un chiffre suivi d'une unité (serrage), un nombre que l'humain a
tapé couvre ce nombre (comme R6 l'écrit : `faits + humain`). Les messages de l'agent à contenu chaîne ne sont pas lus
(hors du constat).

**Phrase de fermeture proposée** : SHOGEN-GARDE-CROCHET-MESSAGE-CHAINE-1 fermé par B-2 : `faits_et_appels` lit les
deux formes du message humain ; R5 voit identifiant et compte d'un message à contenu chaîne ; 2 tests, mutant M2-1
tué.

## B-3 — SHOGEN-GARDE-REPONSE-INVESTISSEUR-1 (B.108, l.1873 ; E29)

**Ce qu'il refuse** : règle neuve R12 (R6 non modifiée), au Stop seul : un nombre à unité de la réponse (texte de
l'agent après son dernier appel d'outil ; jours, semaines, mois, heures, minutes, ans, %, commits, tests, fichiers)
qu'aucun résultat d'outil ni pièce jointe du tour ne porte avec une forme de son unité sur la même ligne (ou le message
de l'humain qui ouvre le tour). Fenêtre écrite : le tour, depuis le dernier message de l'humain. Refus qui nomme le
nombre et demande la lecture de la pièce ; passage consigné au second arrêt du tour.

**Preuve** : `tmp/r12-rouge.txt` (2 échecs : `Pendant les 28 jours de collecte` passait, un 28 étant affiché sans
unité) ; `tmp/r12-vert.txt` (OK). Mesure sur le cas réel : refus sans pièce lue ; `16 semaines` permis après lecture
de l'ADR-0029 §2.4 (e), l.158 (extrait recopié tel que `grep -n` l'a affiché).

**Mutants tués, par test** :
- `test_e29_vingt_huit_jours_sans_piece` : M3-1 tué (R12 non appelée), M3-4 tué (unité non exigée), M3-5 tué (pas de
  passage au second arrêt), M3-10 tué.
- `test_e29_seize_semaines_apres_lecture` : M3-6 tué (forme anglaise de l'unité retirée), M3-7 tué (texte d'avant le
  dernier appel d'outil compté dans la réponse), M3-10 tué.
- `test_unite_et_fenetre` : M3-2 tué (R12 au SubagentStop), M3-3 tué (fenêtre étendue à tout le journal), M3-8 tué
  (message de l'humain du tour ignoré), M3-9 tué (refus du crochet compté comme pièce), M3-1 et M3-4 tués.

**Limites** : nombres en lettres non lus ; unités hors liste jugées par R6 seule ; une ligne qui porte le nombre et son
unité pour un autre objet suffit (le sens n'est pas lu) ; R12 ne juge pas le SubagentStop (rapports des agents : R6
seule) ; une pièce lue dans un tour antérieur se relit (coût voulu : rien de mémoire).

**Phrase de fermeture proposée** : SHOGEN-GARDE-REPONSE-INVESTISSEUR-1 fermé par B-3 : règle R12 au Stop, chaque nombre
à unité de la réponse porté avec son unité par une pièce du tour, sinon refus qui le nomme ; cas réel E29 refusé,
16 semaines permis après lecture de l'ADR-0029 §2.4 (e) ; 3 tests, mutants M3-1 à M3-10 tués.

## B-4 — SHOGEN-GARDE-JOURNAL-LECTURE-SEULE-1 (B.108, l.1878)

**Ce qu'il change** : chaque passage de `avant_acte.py --lecture-seule` ajoute une ligne à
`scripts/controle/garde/lecture-seule.tsv` des outils (`JOURNAL_LS`) : heure lue par `date -u`, sous-commande, tête du
dépôt lu, verdict (`conforme`, `refus`, `erreur`) ; journal non écrit : sortie 3. Le fichier est ignoré par git
(`.gitignore` de la racine) ; les cas détournent `JOURNAL_LS` (`Depot.setUp`), la suite n'écrit jamais celui de
l'arbre (constaté : aucun `lecture-seule.tsv` dans `garde/` après la suite entière).

**Preuve** : `tmp/ls-rouge.txt` (2 échecs : aucune ligne écrite, sortie 0 au lieu de 3) ; `tmp/ls-vert.txt` (OK) ; le
3e test, rouge sans la ligne du `.gitignore` (`?? scripts/controle/garde/lecture-seule.tsv`), vert avec.

**Mutants tués, par test** :
- `test_passages_journalises` : M4-1 tué (journal retiré), M4-2 tué (refus écrit `erreur`), M4-3 tué (tête lue au
  dépôt jetable effacé).
- `test_journal_non_ecrit` : M4-4 tué (échec d'écriture rendu en code de la sous-commande), M4-1 tué.
- `test_journal_ignore_par_git` : M4-5 tué (ligne du `.gitignore` retirée).

**Limites** : une ligne de commande illisible (sortie 3 d'argparse) n'est pas journalisée ; le journal reste local
(jamais versé) ; il est écrit dans l'arbre des outils lancés (un arbre relu hors du dépôt garde son propre journal).

**Phrase de fermeture proposée** : SHOGEN-GARDE-JOURNAL-LECTURE-SEULE-1 fermé par B-4 : chaque passage en
`--lecture-seule` écrit heure, sous-commande, tête et verdict à `garde/lecture-seule.tsv`, ignoré par git ; 3 tests,
mutants M4-1 à M4-5 tués.

## B-5 — SHOGEN-GARDE-DISQUE-DU-DEPOT-1 (B.108, l.1879)

**Ce qu'il change** : `disque` mesure le système de fichiers du dépôt (`--depot`), et celui de TMPDIR s'il en diffère
(`st_dev`), non `/` (`lieux_disque` ; mesure par `GC.etat_disque`, `shutil.disk_usage`, qui lit `os.statvfs`) ; chaque
DQ nomme son chemin. Le contrôle de disque du modèle de chaîne passe `--depot "$DEPOT"` : il mesure le dépôt.

**Preuve** : `tmp/dq-rouge.txt` (2 échecs : dépôt à 2,9 Gio et `/` à 100 sous le double : conforme ; TMPDIR sur un
autre système à 2,9 : conforme) ; `tmp/dq-vert.txt` (OK).

**Mutants tués, par test** :
- `test_disque_du_depot` : M5-1 tué (mesure de `/` rétablie), M5-2, M5-3 (message `sur /`) et M5-4 (site d'appel :
  `lieux_disque(".")`) tués.
- `test_tmpdir_sur_un_autre_systeme` : M5-5 tué (source de TMPDIR : `tempfile.gettempdir()` seul), M5-1 à M5-4 tués.
- `test_modele_de_chaine_passe_le_depot` : M5-6 tué (`--depot` retiré d'`acte` dans `gabarits/chaine.sh` ; sept cas
  de `test_gabarit_chaine.py` le voient aussi).

**Limites** : la cible cargo d'une copie hors du dépôt et hors de TMPDIR n'est pas mesurée ; le point 1 de la skill
`shogen-avant-lancer` (`df -h /`) n'est pas changé (hors du brief) ; la ligne de README qui écrivait la limite
(DISQUE-CHAINE) n'est pas réécrite (ligne citée possible) : l'ajout daté dit qu'elle est levée.

**Phrase de fermeture proposée** : SHOGEN-GARDE-DISQUE-DU-DEPOT-1 fermé par B-5 : `disque` et le contrôle de disque du
modèle de chaîne mesurent le système de fichiers du dépôt, et celui de TMPDIR s'il diffère ; 3 tests (doubles de
`os.statvfs` et `os.stat`), mutants M5-1 à M5-6 tués.

## Items à former (règle PAROXYSME)

- Entrée non objet du crochet GARDE-FAITS : une entrée JSON qui n'est pas un objet sort 1 hors du `try` (non refus) ;
  une entrée non JSON sort 0 (limite de B-1).
- Skill `shogen-avant-lancer`, point 1 : `df -h /` à remplacer par la mesure du dépôt (limite de B-5).
