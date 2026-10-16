# Adjudication de l'orchestrateur, lot GARDE-FOUS-ORCH

## Ajout daté du 2026-10-10 05:05:23 UTC (`date -u`) : conception et avis
Demande de l'investisseur (2026-10-10, mot pour mot) : « crérs des outils, des script ou je ne sais quoi pour toutes les erreurs que tu as faites. pour t empécher de commetre les mémes erreurs; un skill ou des skills. des erreurs qui ont couté de largent des tokens et du temps ».
Pièces : `ERREURS-ORCHESTRATEUR.md` (E1 à E21) ; inventaire de deux lecteurs `claude-sonnet-5-5` (workflow `wf_b66e9ccc-c99`) ; `PROPOSITION.md` (`eb4054d8…`, worker `claude-opus-5-5`) ; `AVIS.md` (`8335b4ce…`, advisor `claude-fable-5-1`). Gate 0 sur les quatre transcripts (modèles du roster) ; FM-1.1 : 0 pour chacun.
- **Avis adopté** : ordre (d) de l'avis ; phase 1 seule maintenant ; arrêt mesuré après elle.
- **Phase 1** (aucune configuration du harnais) :
  - **GF-0** : ajout daté au G0 des lots de dettes (`docs/adr-0028/G0-lots-DETTES.md`), rattachement du lot. L'item SHOGEN-GARDE-FOUS-ORCH-1 est formé par l'orchestrateur au bloc daté du versement.
  - **GF-1** : `garde_commun.py`, horloge et heures (tolérance 120 s ; une heure future refusée).
  - **GF-2** : `presg5.py` versé, contrat de sortie 0, 1, 3, tests dont une sortie dorée.
  - **GF-3** : citations, avec refus de la seule forme stricte `« … » (chemin:N)` ; les autres formes donnent un avertissement compté au journal (avis c.4).
  - **GF-4** : interdits (une seule source de vérité ; jamais les noms de D.2, lus par la liste déjà tenue par `fm11.py` si elle existe, sans affichage), racines, lignes ajoutées, disque. Seuils : refus sous 3 Go, avertissement sous 6 Go, `--lister` (avis Q-13).
  - **GF-5** : `avant_acte.py`, `sceller` et `commit` C1, C3. **C2 remplacé par `Source-Sha:`** (sha256 de la source dans le message, comparé au moment du commit ; avis c.2), avec un mutant : la source retouchée après l'écriture du message est refusée.
  - **GF-6** : `commit` C4 à C9, `lignes-citees.txt`, délégation YAML à `workflows-yaml.py`.
  - **GF-6b** (nouveau, avis b.2) : `avant_acte.py diff --fichier x.diff`, les mêmes contrôles (C4 heures, C5 citations stricte, C7 ajout en fin et non-décalage des lignes citées, presg5 sur les `.md`, C8 YAML), lancés à la réception d'un diff de worker, avant la G2.
  - **GF-7** : `verser`.
  - **GF-8** : `pousser`, `publier`, `existe`, `disque --lister`, `hors-distant.txt` (mandataire : écritures de réglages et de branches refusées, constatées le 2026-10-10).
  - **GF-9** : modèle de chaîne `gabarits/chaine.sh` avec `timeout`, sceau et `Source-Sha`.
  - **GF-9b** (nouveau, avis b.3) : ligne fixe `GROUPES :` au rapport des contre-contrôles (gabarit), et `avant_acte.py chaine --plan P --cc RAPPORT`, qui refuse un plan où un diff rouge seul est commité sans son groupe.
  - **GF-10** : les quatre skills (`.claude/skills/shogen-avant-lancer`, `-avant-committer`, `-avant-pousser`, `-avant-ecrire`), qui donnent les commandes, sans répéter les règles du bloc commun (avis c.6) ; `test_skills.py`.
  - **GF-20, avancé en phase 1** (avis d.3) : bloc commun des fiches, texte identique dans chaque fiche `shogen-*` (lint R-1 et ses cas verts), test d'identité. Il porte la règle de non-décalage (E21), la règle I-1 (E5), les messages d'outils en code (E9), `timeout` aussi pour les campagnes de mutants (avis b.4), et « avant de rendre ton diff, lance `avant_acte.py diff` ».
  - Journal des refus avec une colonne `contourne` (avis b.5).
- **Phase 2** (crochet `PreToolUse`, GF-11 à GF-16) : **non engagée**. Conditions :
  - le journal des refus de la phase 1 est lu ;
  - un témoin de dix lignes prouve d'abord que le crochet voit les outils des sous-agents (avis b.1, Q-19) ;
  - l'investisseur donne son accord (Q-2), car le crochet change la configuration du harnais.
  Phase 3 (`redos.py`, `brief`) : `redos.py` est réduit à une liste de motifs suspects sans exécution, ou retiré (avis c.1) ; décision après la phase 1.
- Réponses aux Q-n : celles de l'avis (§e), adoptées. Q-21 : la ligne du CLAUDE.md appartient au mainteneur, elle n'est pas touchée.
- Suite : générateur de la phase 1 (`BRIEF-GF1.md`), puis G2 neuve, contre-contrôle, chaîne (par le modèle GF-9 lui-même, une fois commis) et versement.

## Ajout daté du 2026-10-10 08:13:53 UTC (`date -u`) : rapport du générateur de la phase 1
Pièce : `gf1/RAPPORT-GENERATEUR.md` (`1c511b88…` ; générateur `claude-opus-5-5`, Gate 0 sur le transcript : 645 occurrences, aucun autre modèle ; FM-1.1 : 0, deux versions) ; `gf1/SHA256SUMS` (`f49f733b…`, 21 lignes, `sha256sum -c` relu). 18 diffs (GF-0 à GF-10b), 2 309 lignes ajoutées, chacun sous 200 ; suite `scripts/controle` 37 → 89 ; 203 mutants, 200 tués, 3 équivalents déclarés.
- **Q-1, Q-2, Q-8, Q-9, Q-12, Q-13 : recommandations adoptées.** Q-12 : la chaîne lance `xtask verify` sur l'arbre complet et exige VERDICT GLOBAL VERT (déjà sa règle).
- **Q-3 adoptée**, avec item formé au versement : le motif de `fm11.py` qui prend le nom de session du scratchpad est revu dans un lot de dettes (SHOGEN-FM11-MOTIF-SESSION-1).
- **Q-4** : la l.293 d'ADR-0028 à `dda4bbc` est confirmée par l'orchestrateur (§4.2, documents Pocket hors de GitHub ; la l.291 est §4.1). L'entrée « suppression de branche » de `hors-distant.txt` ne se fonde pas sur E17 [2nd] mais sur l'annexe B, B.92 (l.1568 : réponse 403 du mandataire à la suppression de la branche jetable `essai/analyseur-residus`) : correction à faire (source citée).
- **Q-5 adoptée** : ligne du bloc commun (GF-20) : un agent lance `avant_acte.py diff` dans un dépôt jetable dont la tête est la base du diff ; mode de lecture seule en phase 2 (item SHOGEN-GARDE-LECTURE-SEULE-1).
- **Q-6 adoptée** : DETTES-T7 porte I-1 et la règle des messages d'outils (DT7-a, bloc de gabarit de la fiche worker) ; GF-20 ne les répète pas et se pose sur la tête qui porte DETTES-T7, par un diff du générateur relu par la G2 du lot GF.
- **Q-7** : décidé après DETTES-T7 ; la fiche orchestrateur n'est pas touchée en phase 1.
- **Q-10** : liste soumise à la G2 (elle juge chaque entrée et dit ce qui manque, `gates.yml` compris).
- **Q-11 adoptée** : items formés au versement : E22 (référence exacte d'un constat relayé), E23 (faisabilité d'un acte vérifiée avant de l'écrire), volet brief de E24 (contrôle `brief`), déclencheur : phase 3 du lot GARDE-FOUS-ORCH, décidée après la lecture du journal des refus de la phase 1. L-1 à L-13 : items ou limites au versement, selon la G2.
- E-1 à E-16 admis. E-1 (archive du dépôt entier passée dans un tube vers `wc`, rien affiché), E-8 (un mutant a parcouru `/` à profondeur 4, noms et tailles seulement), E-11 (indice d'un motif de D.2 affiché, jamais le motif) : déclarés au bloc daté du versement.
- Suite : G2 neuve (`gf1/g2/BRIEF-G2.md`).

## Ajout daté du 2026-10-10 08:19:22 UTC (`date -u`) : ligne de plus pour GF-20
- Venue de la G2 de DETTES-T7 (L-G1) : les passes d'agents ne lancent ni g3 `--history` ni g3 `--tree` (ce dernier lit les blobs de tous les fichiers suivis, emplacements interdits compris, dans un temporaire) ; la CI de la forge les porte. À écrire au bloc commun GF-20 avec les lignes de E24 (commandes git limitées à une liste explicite de chemins) et de Q-5 (dépôt jetable).

## Ajout daté du 2026-10-10 14:09:16 UTC (`date -u`) : décision de l'investisseur, portée du lot

Décisions verbatim :
- sur la priorité : « ça sera la premiére chose a faire aprés la reprise » ;
- sur la portée : « toutes les erreurs passés doivent étre évités avec des outils et pas des écrits qui seront perdus dans un million de décisions et un million de documents. »

Conséquences :
1. Le lot GARDE-FOUS-ORCH est le premier travail à la reprise. L'ordre est le suivant :
   - fin de la G2 (agent `acb14b7565fdf6765`, à reprendre : il lui reste les gates finales et son rapport) ;
   - adjudication des corrections C-1 à C-17 ;
   - contre-contrôle neuf ;
   - commit.
2. Aucune erreur de la liste ne reste couverte par un écrit seul. Les erreurs sans contrôle mécanique en phase 1 entrent dans le lot, chacune avec son outil et son test rouge tiré du cas réel : E6, E7, E12, E13, E18, E20, E22 et E23, plus E26 et E27.
   - Une erreur qu'on ne peut pas mécaniser entièrement reçoit l'outil le plus proche.
   - Ce qui reste hors de l'outil est dit en une ligne de limite, jamais en règle seule.
3. **Les outils sont branchés pour se lancer seuls**, sans dépendre de la mémoire de l'orchestrateur. Le moyen : des hooks du harnais Claude Code (`.claude/settings.json` du projet).
   - PreToolUse sur `git commit` et `git push` : `avant_acte.py`, refus bloquant.
   - PreToolUse sur Agent et Workflow :
     - contrôle du brief (items cités, état relu à l'annexe B, E6 ; règles des interdits, E24) ;
     - seuil de coût (E27).
   - PreToolUse sur la création d'une PR : visibilité du dépôt et forge disponible (E20).
   - UserPromptSubmit : un message externe collé fait relever ses noms propres dans le JOURNAL et dans `docs/publication/`, et la réponse est injectée en contexte (E26).
   - Écriture d'une heure dans un fichier versé : contrôle des heures (E14).
   - Commande `sleep` d'avant-plan : refus (E18).
   - Le bloc commun GF-20 garde le reste. Le branchement passe par la skill `update-config` et par la G2 du lot.

## Ajout daté du 2026-10-15 10:57:57 UTC (`date -u`) : adjudication de la G2 neuve (phase 1)

Contrôles : Gate 0, 788 champs `model` du transcript, tous `claude-opus-5-5` (un `<synthetic>` de harnais) ; FM-1.1 : 0 (deux outils) ; `SHA256SUMS` du dossier conforme ; 18 diffs de correction présents.

Verdict de la G2 : ACCEPTE-AVEC-CORRECTIONS, C-1 à C-18. **Les dix-huit corrections sont adoptées telles quelles**, dont C-18 et le complément de C-13, venus après la liste « C-1 à C-17 » du 2026-10-10 : la liste fermée est maintenant C-1 à C-18. Ordre de la chaîne : GF-0 à GF-10b, puis C-1 à C-12, C-14 à C-18 ; C-13 se joint au diff GF-20 (bloc commun), posé après le lot DETTES-T7.

Points relevés :
- C-1 : le défaut le plus grave (chaîne qui scelle un pas rouge) confirme la décision de l'investisseur : les outils ne servent que validés et branchés. Le crochet GARDE-FAITS du dépôt (`a45f363`) couvre déjà, de son côté, commit et poussée sans lecture ; les deux se complètent.
- C-3 et C-16 : les faux refus sur DT14-a, DT14-b et DT6-d sont fermés ; les rejeux réels de la G2 font foi.
- Écarts E-10 (g3 `--tree` sur copies avec exclusions) et E-15 (`/dev/shm`) : acceptés ; la règle « pas de g3 `--tree` dans les passes d'agents » entre au bloc commun (C-13 la porte). Mutants K-28 à K-30 non joués (E-8) : le contre-contrôle les joue.

Suite : contre-contrôle neuf (brief `gf1/g2/cc/BRIEF-CC.md`), puis chaîne de commit (35 pas) après la fin de la chaîne DETTES-T2 (une seule chaîne à la fois dans l'arbre), puis phase 2 (E6, E7, E12, E13, E18, E20, E22, E23, E26, E27 : un outil chacun, branché en crochet).

## Ajout daté du 2026-10-15 12:07:52 UTC (`date -u`) : adjudication du contre-contrôle neuf

Contrôles : Gate 0, 402 champs `model`, tous `claude-opus-5-5` ; FM-1.1 : 0 (deux outils) ; `SHA256SUMS` conforme ; 10 diffs de réserve présents. Verdict CONFORME-AVEC-RÉSERVES, R-1 à R-10 : **toutes adoptées telles quelles**, posées après C-18 dans l'ordre R-1 à R-10 (45 pas au total : GF-0 … GF-10b, C-1 … C-12, C-14 … C-18, R-1 … R-10 ; C-13 reste joint au diff GF-20). Clôture sans passe 3 : les réserves sont des diffs écrits par le contre-contrôleur, copiés à l'octet. R-8 règle la contradiction entre le crochet GARDE-FAITS et les skills (lectures ajoutées en tête des commandes) ; LN-6 (le crochet juge le texte de la commande, pas l'acte) est formé en item au versement, à traiter en phase 2 avec la forme « lecture de l'acte réel ». LN-1 à LN-5, LN-7 : items formés au versement. Chaîne détachée (270 min estimées par l'outil), lancée après la fin de la chaîne DB-1 ; écarts acceptés.
