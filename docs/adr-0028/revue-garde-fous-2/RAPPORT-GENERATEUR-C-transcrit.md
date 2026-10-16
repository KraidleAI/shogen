# Rapport du générateur du groupe C (transcrit)

> Transcription par l'orchestrateur le 2026-10-16 12:03:37 UTC du fichier garde-fous/p2c/RAPPORT-GENERATEUR.md ; contrôle FM-1.1 des transcripts (générateurs des groupes A, B, C, réviseurs G2 des trois groupes, intégrateur, contre-contrôleur) par le fm11.py versé : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Rapport du générateur G1 — GARDE-FOUS-ORCH, phase 2, groupe C (limites de la phase 1)

Gate 0 : `claude-opus-5-5` (worker, générateur). Rattachement : ADR-0028 annexe B.102, items
SHOGEN-GARDE-LECTURE-SEULE-1, SHOGEN-GARDE-DATE-PASSEE-1, SHOGEN-GARDE-ATTRIBUTION-DIFF-1,
SHOGEN-GARDE-VERIF-VERSIONNEE-1, SHOGEN-GARDE-DISQUE-CHAINE-1, SHOGEN-GARDE-LIGNE-REMPLACEE-1,
SHOGEN-FM11-MOTIF-SESSION-1 ; pièces `docs/adr-0028/revue-garde-fous/` (L-1, L-3, L-4, L-12, L-13, LN-1, Q-3, Q-5).
Journal G1 : `NOTES.md` (sources, commandes, sorties, écarts). Aucune écriture dans le dépôt lu, aucune commande git
en écriture sur lui, aucun cargo.

## 1. Base et série

- Base de la série livrée : `413321bf7bd42ad9b1dc543c84149b087772e48f` (DETTES-T15 DT15-b, registre des renvois
  commis). Le travail a commencé sur `84993090d817…` ; la chaîne DETTES-T7 puis DETTES-T15 a avancé la tête pendant
  le lot : la série a été refaite sur `413321bf` (copie `copie3`, branche locale `serie3`). Elle s'applique aussi à
  `88da219e2bc0…` (DT15-b2, registre seul changé) : `avant_acte.py --lecture-seule diff` de la série entière sur le
  dépôt lu à cette tête : sortie 0.
- Anciens diffs (base `84993090`) : `diffs-ancienne-base/` (pour mémoire ; P2C-6 y lit un format de registre
  supposé, remplacé).

| diff | item | fichiers | +/− (numstat) | tests ajoutés | plancher |
|---|---|---|---|---|---|
| `diffs/P2C-1-fm11-motif.diff` | SHOGEN-FM11-MOTIF-SESSION-1 | fm11.py, SHA256SUMS, test_fm11, README, gates.yml | +27 −5 | 1 | 118 |
| `diffs/P2C-2-date-passee.diff` | SHOGEN-GARDE-DATE-PASSEE-1 | garde_commun.py, avant_acte.py, tests, README, gates.yml | +118 −7 | 3 | 121 |
| `diffs/P2C-3-attribution-diff.diff` | SHOGEN-GARDE-ATTRIBUTION-DIFF-1 | avant_acte.py, test, README, gates.yml | +95 −2 | 1 | 122 |
| `diffs/P2C-4-verif-versionnee.diff` | SHOGEN-GARDE-VERIF-VERSIONNEE-1 | avant_acte.py, gabarits/chaine.sh, tests, README, gates.yml | +106 −9 | 2 | 124 |
| `diffs/P2C-5-disque-chaine.diff` | SHOGEN-GARDE-DISQUE-CHAINE-1 | gabarits/chaine.sh, test, README, gates.yml | +27 −3 | 1 | 125 |
| `diffs/P2C-6-ligne-remplacee.diff` | SHOGEN-GARDE-LIGNE-REMPLACEE-1 | avant_acte.py, garde/lignes-citees.txt, test, README, gates.yml | +147 −5 | 3 | 128 |
| `diffs/P2C-7-lecture-seule.diff` | SHOGEN-GARDE-LECTURE-SEULE-1 | avant_acte.py, garde_commun.py, test, README, gates.yml | +111 −28 | 1 | 129 |

Chaque diff : ≤ 200 lignes ajoutées (R-25), aucun marqueur de dette nu (R-13 : 0), aucun chemin absolu du
scratchpad (0), un ajout daté en fin de `scripts/controle/README.md` (`date -u` au pas), plancher du job
`controle-unittest` recalé en place (`--egal`). Pas à pas (`mesures/pas_a_pas3.sh`) : à chaque pas, le runner du
job et la suite jugée par le vérificateur sont rejoués ; résultats au §9.

Aucun document cité par numéro n'a de ligne décalée (C-3) : README et `garde/lignes-citees.txt` reçoivent leurs
ajouts en fin ; la ligne 11 de la table du README et les lignes 24 et 50 de `gabarits/chaine.sh` sont changées en
place (nombre de lignes de `chaine.sh` inchangé, 54) ; `gates.yml` : seule la valeur du plancher change, en place
(les renvois du registre vers `gates.yml` sont tous hors de l'arbre, `lignes` à `-`). `fm11.py` : l.23 en place
(le README cite sa l.4, intacte).

## 2. SHOGEN-FM11-MOTIF-SESSION-1 (Q-3) — P2C-1

- Erreur visée : le motif de session de `fm11.py` comptait l'identifiant de session écrit comme composant du chemin
  du scratchpad, que porte toute transcription de sous-agent de la session (faux positif de FM-1.1).
- Ce qu'il refuse (compte) : la session nommée ailleurs que comme composant du scratchpad (transcription, dossier de
  la session, dossier voisin `scratchpad-copie`) ; il ne compte plus `…/<session>/scratchpad`.
- Preuve : rouge `test_q3_session_du_scratchpad` (le motif comptait l'entrée et le résultat) ; vert après ;
  identifiant formé en deux morceaux dans le test. `SHA256SUMS`, `SHA_FM11` et la ligne de table mis à jour.
- Mutants : M1-1 (motif d'origine), M1-2 (garde de fin de composant ôtée).
- Limite : le motif `session_013dvmub` peut se lire dans toute transcription par la ligne d'attribution
  `Claude-Session:` que le contexte des agents porte (non mesuré : item à former, SHOGEN-FM11-MOTIF-ATTRIBUTION-1
  proposé).
- Phrase de fermeture : SHOGEN-FM11-MOTIF-SESSION-1 fermé par P2C-1 : le motif de session de `fm11.py` ne compte
  plus l'identifiant de session écrit comme composant du chemin du scratchpad ; témoin `test_q3_session_du_scratchpad`.

## 3. SHOGEN-GARDE-DATE-PASSEE-1 (L-1) — P2C-2

- Erreur visée : E14 (heures écrites sans lire l'horloge) dans les formes que la phase 1 ne voyait pas : heure sans
  sa date, heure avant sa date ou plus de 25 caractères après elle, entrée datée antérieure à la dernière du fichier.
- Ce qu'il refuse : `heure-sans-date` (C4 : message, lignes ajoutées des .md du commit et du diff, `publier`,
  `verser`) ; `heure-passee` (C4, commit et diff : entrée datée ajoutée — ligne qui commence par date et heure, ou par
  un mot en capitale suivi de `daté du` — antérieure à la dernière entrée datée du fichier à HEAD ou à une entrée
  ajoutée avant elle). Code et guillemets français restent masqués ; une date seule du même jour n'est pas jugée.
- Preuve : rouges `test_l1_heure_sans_date`, `test_l1_entree_datee_anterieure` (garde_commun, fonction absente),
  `test_l1_entree_datee_anterieure` (avant_acte, diff et commit) ; vert après. Test existant modifié :
  `test_heure_approchee` (attendu étendu : 19:50 écrite sans date est maintenant vue).
- Mesure du coût (`mesures/rejeu_heures.py`, 120 commits, 1463 lignes ajoutées des .md suivis) : 24 heures sans date
  et une entrée hors d'ordre auraient été refusées (exemples : `depuis 09:32 UTC`, `vers 20:42 UTC`, une entrée
  04:09:04 écrite après une entrée 04:38:22 du même diff). C'est l'objet de la règle ; le prix est d'écrire la date
  devant chaque heure. Question Q-3 ci-dessous.
- Mutants : M2-1 à M2-11 (refus ôté, fenêtre 25 → 40, sens de comparaison, égalité, maximum courant ôté, préfixes des
  deux formes d'entrée, sites d'appel au commit et au diff, contenu d'avant ôté, heure ignorée).
- Limites : une heure passée fausse hors d'une entrée datée n'est pas vue ; les entrées sont comparées au fichier de
  HEAD (un fichier neuf n'a que l'ordre de ses propres entrées) ; .md seulement.
- Phrase de fermeture : SHOGEN-GARDE-DATE-PASSEE-1 fermé par P2C-2 : C4 refuse une heure écrite sans sa date et une
  entrée datée antérieure à la dernière entrée datée du fichier ; reste : heure passée fausse hors d'une entrée datée.

## 4. SHOGEN-GARDE-ATTRIBUTION-DIFF-1 (L-3) — P2C-3

- Erreur visée : E8 sous la forme de L-3 : un mot du message présent dans les sources, mais écrit pour un autre diff.
- Ce qu'il refuse (C3) : un verdict, nombre de passes, identifiant ou sha court du message que les sources n'écrivent
  que dans des passages (paragraphe ; rangée de tableau, point de liste ou titre à part ; ligne de continuation jointe)
  qui nomment d'autres diffs du même préfixe que le `Diff-Id` (ou `--id`), sans ce diff ni une plage qui le couvre
  (`C-1 à C-18`, `GF-0 … GF-10b`, bornes incluses), sauf si les lignes ajoutées du diff portent ce mot.
- Preuve : rouge `test_l3_attribution_au_diff` ; vert après. Rejeu (`mesures/rejeu_attribution.py`) sur les 45
  messages GARDE-FOUS de la phase 1 (Diff-Id pris au second mot du sujet ; ces messages ne portent pas de ligne
  `Diff-Id`) : premier jet 16 refus (plages à borne alphanumérique non lues), après correction 0 sur 45.
- Mutants : M3-1 à M3-10 (appel, lecture du Diff-Id, lignes ajoutées, plages, bornes basse et haute, rangées de
  tableau, lignes de continuation, juge des sha, passage qui nomme ce diff et un autre).
- Limites : `chaque mot` est lu comme les mots que C3 sait lire (verdicts, passes, identifiants, sha), non la prose ;
  l'attribution ne juge que la famille du `Diff-Id` (un identifiant d'une autre famille reste jugé sur sa seule
  présence) ; sans `Diff-Id` ni `--id`, non jugée ; le découpage en passages suit la forme Markdown des sources.
- Phrase de fermeture : SHOGEN-GARDE-ATTRIBUTION-DIFF-1 fermé par P2C-3 : C3 refuse un mot du message que les
  sources n'attribuent qu'à d'autres diffs du même préfixe ; reste : prose libre, familles d'identifiants autres que
  celle du Diff-Id.

## 5. SHOGEN-GARDE-VERIF-VERSIONNEE-1 (L-4) — P2C-4

- Erreur visée : LA-N05 sous la forme de L-4 : le sceau prouvait la fin de la vérification, pas son contenu (une
  chaîne copiée d'un modèle ancien, au défaut C-1, ou affaiblie, scellait et commettait).
- Ce qu'il refuse : `sceller --verif F` (texte de `declare -f verif`, `-` : entrée standard) écrit la ligne
  `verif <sha256>` au sceau ; `commit` (C1) refuse un sceau dont cette ligne n'est pas l'empreinte de la fonction
  `verif` de `gabarits/chaine.sh` des outils (extraite de `verif() {` à `# --- fin de verif`, passée par
  `declare -f` de bash). Le modèle scelle par `declare -f verif | acte sceller --verif -`.
- Preuve : rouges `test_l4_verif_versionnee` (chaîne à verif affaiblie commise) et `test_l4_sceau_de_la_verif`
  (option absente : sortie 3) ; vert après ; référence du test obtenue par `sed` puis bash, indépendante du code.
  Les cas du modèle tournent avec une copie des outils dont le modèle porte le faux `verif`.
- Mutants : M4-1 à M4-5 (contrôle ôté, ligne non écrite, chaîne sans empreinte, empreinte sans `declare -f`, entrée
  standard non lue).
- Limites : un sceau sans ligne `verif` (vérification hors du modèle : `<vérification> && sceller` des skills) n'est
  pas jugé ; une copie de chaîne modifiée pour ne plus passer `--verif` n'est pas vue ; une vérification propre à un
  lot doit être versée au modèle par un diff relu (Q-2).
- Phrase de fermeture : SHOGEN-GARDE-VERIF-VERSIONNEE-1 fermé par P2C-4 : le sceau du modèle porte le sha256 de
  `declare -f verif` et `commit` refuse une vérification autre que celle de `gabarits/chaine.sh` ; reste : sceaux posés
  hors du modèle.

## 6. SHOGEN-GARDE-DISQUE-CHAINE-1 (LN-1) — P2C-5

- Erreur visée : E4 et E28 (chaîne morte sans ligne lisible) sous la forme de LN-1 : disque contrôlé au départ seul.
- Ce qu'il refuse : à chaque pas, avant `git apply`, `acte disque --min-go "${DISQUE_MIN_GO:-0}"` (seuils lus par
  l'outil dans `garde_commun.py`) ; un refus imprime `ROUGE disque avant <id> (LN-1) : arrêt, rien appliqué`.
- Preuve : rouge `test_ln1_disque_a_chaque_pas` (outil réel, enveloppé pour serrer le seuil au second contrôle :
  les deux pas commis) ; vert après (X-1 seul commis, arbre propre, ligne ROUGE).
- Mutants : M5-1 à M5-3 (contrôle ôté, ligne sans ROUGE, contrôle après `git apply`).
- Limite : le disque peut se remplir pendant la vérification d'un pas (cargo) : vu au pas suivant seulement.
- Phrase de fermeture : SHOGEN-GARDE-DISQUE-CHAINE-1 fermé par P2C-5 : le modèle de chaîne contrôle le disque à
  chaque pas, avant `git apply`, et s'arrête sur une ligne ROUGE.

## 7. SHOGEN-GARDE-LIGNE-REMPLACEE-1 (L-13) — P2C-6

- Erreur visée : E21 sous la forme de L-13 : un remplacement à nombre de lignes égal change une ligne citée.
- Ce qu'il refuse (C7, commit et diff) : un renvoi dont les lignes répondaient à leur empreinte à HEAD et n'y
  répondent plus après le diff. Sources : registre `docs/RENVOIS-LIGNES.tsv` de DETTES-T15 lu dans l'état d'après
  (colonnes `cible`, `lignes`, `empreinte` ; `lignes` à `-` sauté ; lignes `#` sautées ; en-tête ou rangée illisible :
  erreur 3) et lignes `<chemin>:<a>[-<b>] <empreinte>` de `garde/lignes-citees.txt` (deux versées : ADR-0028 l.293,
  la ligne de `garde/hors-distant.txt`, et `fm11.py` l.4, que cite la table du README). Empreinte à la convention du
  registre : sha256 des lignes jointes par LF, sans LF final, comparé sur sa longueur. Admis : empreinte mise à jour
  dans le même diff ; avertissement : empreinte sans réponse avant ni après ; fichier déjà décalé (refusé, ou admis
  par `Décalage admis`) : non jugé une seconde fois.
- Preuve : rouges contre le code (`test_l13_ligne_citee_remplacee`, `test_l13_empreinte_de_la_garde`,
  `test_l13_empreintes_de_la_garde_a_jour`), puis rouges du P2C-6 refait contre l'ancien P2C-6 (format réel du
  registre : sortie 3) ; vert après. Relecture du registre réel par l'outil (`mesures/registre_outil.py`) : à
  `413321bf`, 99 renvois répondent, 11 non, 23 hors de l'arbre, égal au recalcul indépendant
  (`mesures/registre.py`) ; à `88da219e` (DT15-b2) : 110 répondent, 0 non, 23 hors de l'arbre.
- Mutants : M6-1 à M6-13 (appel, admission par mise à jour, avertissement, garde non lue, motif, fichiers décalés,
  registre lu à HEAD, site d'appel du diff, décalage non noté, rangée `-`, longueur de l'empreinte, fin de plage,
  lignes `#`).
- Limites : les empreintes de la garde sont lues dans l'arbre des outils (non dans l'état d'après) ; un renvoi dont le
  texte a bougé sans mise à jour du registre ne donne qu'un avertissement ; texte décodé en UTF-8 par git.
- Phrase de fermeture : SHOGEN-GARDE-LIGNE-REMPLACEE-1 fermé par P2C-6 : C7 lit les empreintes du registre de
  DETTES-T15 et de `garde/lignes-citees.txt` et refuse un renvoi changé à nombre de lignes égal, sauf empreinte mise à
  jour dans le même diff.

## 8. SHOGEN-GARDE-LECTURE-SEULE-1 (L-12, Q-5) — P2C-7

- Erreur visée : L-12 : `diff` et `commit` écrivaient dans le dépôt lu (objets, journal), ce qu'un agent en lecture
  seule ne peut pas faire.
- Ce qu'il fait : `--lecture-seule` (avant la sous-commande ; `diff` et `commit` seulement, autre sous-commande :
  erreur 3) : git tourne dans un dépôt jetable de TMPDIR (`git clone --shared --no-checkout`, HEAD du dépôt lu, son
  index copié pour `commit`) ; fichiers cités, lecteur YAML, sceaux et interdits (liens suivis compris) se lisent dans
  le dépôt lu ; le journal va au dépôt jetable.
- Preuve : rouge `test_l12_rien_n_est_ecrit` (option inconnue : 3) ; vert : octets du dépôt lu, `.git` compris, égaux
  avant et après ; mêmes verdicts qu'en mode courant (C7, C5, C8 du diff ; C1 puis admis au commit ; avertissement
  d'un interdit vu par un lien). Sur le dépôt lu réel (`88da219e`) : série entière jugée conforme, blob neuf de
  `avant_acte.py` absent des objets du dépôt avant et après, aucun journal créé.
- Mutants : M7-1 à M7-8 (clone, index, lieu du sceau, racine des citations, lecteur YAML, refus des autres
  sous-commandes, HEAD du clone, racine des interdits).
- Limites : les passages en lecture seule ne sont pas journalisés (journal perdu avec le clone) ; un index scindé
  (`split-index`) n'est pas copié en entier ; le clone lit toutes les références du dépôt.
- Phrase de fermeture : SHOGEN-GARDE-LECTURE-SEULE-1 fermé par P2C-7 : `--lecture-seule` fait tourner `diff` et
  `commit` dans un clone jetable, sans rien écrire dans le dépôt lu ; reste : journal des passages en lecture seule.

## 9. Pas à pas et mutants

- Pas à pas de la série finale (`mesures/pas_a_pas3.txt`) : à chaque pas, runner du job 153 ok, 0 échec ; suite
  jugée par le vérificateur, conforme à Ran = 118, 121, 122, 124, 125, 128, 129 (plancher du pas, `--egal`).
- Suite finale sous `-X dev -W error` (Python 3.11) : Ran 129, OK, aucune ligne `Exception ignored` ni `Warning` ;
  sous Python 3.12 et 3.13 : Ran 129, OK.
- Portes légères sur l'arbre final : `lint-model-pinning.sh` 0, `runners-epingles.py` 0, `workflows-yaml.py` 0
  (PyYAML du système), `journaux-modele.py` 0, `docs-sha256sums.py` 0.
- Mutants : `scripts/controle/mutants.py` du dépôt lu, figé à la tête `3660713891ff` dans `outils-mut/` (sha256
  `68406b966a7d…`, vérificateur `18430f2a007c…`), lancé à part de la copie mutée `copie4/` (archive de la série
  finale), job `controle-unittest`, borne 300 s. Liste : `mutants/genere3.py` → `mutants/mutants3.json` (52 mutants,
  texte avant présent une fois, contrôlé). Campagne finale (`mutants/campagne-finale.txt`, diffs et sorties dans
  `mutants/sortie-finale/`) : témoin vivant ; 50 tués (sortie 1), 2 vivants, 0 FATAL ; relevé `ps` de fin : aucun
  processus des 106 groupes, aucun descendant vivant.
- Vivants, déclarés équivalents : M6-5 (la ligne d'empreinte gardée parmi les motifs fnmatch ne répond qu'à un
  chemin écrit `<chemin>:<a> <empreinte>`, espace compris) ; M7-7 (`update-ref` de la HEAD du clone : `git clone`
  suit déjà la HEAD du dépôt lu, détachée ou sur une autre branche, mesuré dans un dépôt temporaire ; garde
  défensive).
- Campagnes antérieures (anciens diffs) : la première a laissé vivants M2-6, M3-10 et M7-8, tués après renforcement
  des tests (am2, am3b, am7b) ; la troisième a été arrêtée sans résultat (série remplacée).

## 10. Écarts, observations, questions

- E-1 `ls docs/adr-0028/` lancé une fois (liste sans motif d'un dossier de `docs/`) : noms de dossiers `execution` et
  `monark-m009a` affichés, aucun contenu. Contraire à la consigne des listes sous `docs/` du bloc de gabarit.
- E-2 Recherches récursives (`grep -rn`, `git grep`) dans mes copies (bâties sans les interdits) pour vérifier les
  renvois par numéro avant de changer une ligne en place ; jamais sur le dépôt lu ni sur le scratchpad entier.
- E-3 La série a été refaite deux fois : tests renforcés après une première campagne (mutants vivants M2-6, M3-10,
  M7-8), puis rebasage sur la tête où DETTES-T15 a commis le registre (P2C-6 refait sur son format).
- E-4 Campagne 3 (anciens diffs) arrêtée par SIGINT, sans résultat (série remplacée) ; aucun processus resté.
- O-1 `diff` sort en 3 (FileNotFoundError de presg5 sur `biblio/INDEX.md`) dans un dépôt sans ce fichier :
  comportement antérieur au lot (vu en écrivant un test) ; item proposé SHOGEN-GARDE-DIFF-SANS-INDEX-1.
- O-2 Les planchers (118 à 129) valent pour cette série seule ; fusionnée avec les séries des groupes A et B, la
  valeur se recale au compte mesuré.
- Q-1 Recalage : à la chaîne, les ajouts du README se replacent en fin, datés du moment (la règle de P2C-2 refuse
  une entrée datée antérieure à la dernière du fichier).
- Q-2 `gabarits/chaine.sh` dit sa vérification `à relire par lot` ; avec P2C-4, une vérification propre à un lot se
  verse au modèle par un diff relu : à adjuger (ou un `--verif-admise` à poser).
- Q-3 `heure-sans-date` refuse 24 heures sur 120 commits mesurés : refus dès la phase 2 (forme du brief) ou
  avertissement compté d'abord (forme de C5) ?
- Items à former : SHOGEN-FM11-MOTIF-ATTRIBUTION-1 (motif de session et ligne `Claude-Session:`),
  SHOGEN-GARDE-DIFF-SANS-INDEX-1 (O-1), SHOGEN-GARDE-JOURNAL-LECTURE-SEULE-1 (journal des passages en lecture seule).
