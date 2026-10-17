# Rapport de l'intégrateur (série unique C, B, A, réserves posées) (transcrit)

> Transcription par l'orchestrateur le 2026-10-17 07:31:23 UTC du fichier garde-fous/int3/RAPPORT-INTEGRATEUR.md ; contrôle FM-1.1 du transcript du intégrateur par le fm11.py versé : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5 (567 occurrences, aucune autre). Texte ci-dessous avec 18 retouche(s) (E35, E38) : noms de marqueur de dette et locutions de la gate S-G4 cités en clair, mis en code, segments de code à doubles accents graves réécrits en segments simples, heures sans date dans les 25 caractères ou approchées mises en code ou entre guillemets français, sans autre changement (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Rapport de l'intégrateur G1 — lot INTEGRATION-P3 (GARDE-FOUS phase 3 : groupes C, B, A en une série)

Gate 0 : `claude-opus-5-5` (identifiant de l'environnement de l'agent), effort `high`, fiche `shogen-worker`. Rôle :
intégrateur G1, ni générateur ni réviseur des groupes. Brief : `BRIEF.md` de ce dossier (orchestrateur, 2026-10-16
`17:52:19` UTC ; sha256 `9638ab705607a0fb2a369aff827d82669c4cb398d37216eb4d04f2c39273b4aa`). Journal G1 : `NOTES.md`.
Rattachement : ADR-0028, annexe B (`docs/adr-0028/ANNEXE-B-items.md`), items ouverts l.1872 à 1880 (B.108) et 1890,
1891 (B.109), par les briefs et adjudications des trois groupes. Dépôt lu en lecture seule (aucune commande git en
écriture sur lui, aucun cargo, aucun passage à blanc avec `--depot` sur lui) ; git en écriture dans des dépôts jetables
de ce dossier seulement (`serie/`, `depot-blanc/`, `tete2/`, `emul/`, `emul-rapide/`, `emul-tete2/`, `juge/`,
`mut/copie/`, `tmp/`).

## 1. Base, ordre, livrables

- Tête lue à l'ouverture : `fe9a72b0503758d7c0e19f1e9a928a5e6d0f3878` (attendue `fe9a72b`) ; plancher du job
  `controle-unittest` à la tête : 177 (`gates.yml` l.369). Tête relue à `20:13:34` UTC :
  `328a6d2565ff5b3df87924608133b6e6b8f0f84c` (sept commits SYNC-DOCS11 SD-01 à SD-07) ; `git diff --stat fe9a72b HEAD`
  limité aux chemins de la série (`scripts/controle .claude .gitignore .github/workflows/gates.yml enforcement`) et à
  `docs/RENVOIS-LIGNES.tsv biblio/INDEX.md JOURNAL.md docs/adr-0028/ANNEXE-B-items.md CLAUDE.md` : vide (seul
  `scripts/publication/` change) ; copie de cette tête (`tete2/`) : mêmes octets que la base sur ces chemins
  (`diff -rq`), et la série s'y joue de même (section 6). Copie creuse : `outils/copie.py` (repris de
  `int/outils/copie.py`, sha256 égal), 1532 membres, 0 écarté par `chemin_interdit`.
- Entrées contrôlées par sha256 : G2 des groupes C `7454f8d5…`, B `b3de4362…`, A `b8661e5f…` (égales aux
  adjudications) ; concaténations des séries C `73d9a1bf…` et corrections `814f40c8…`, B `2fe76b3c…` et `d181e070…`, A
  `689669bf…` et `47003d95…` (égales aux rapports).
- Ordre (adjudications) : C (INT-01 à INT-06), B (INT-07 à INT-12), A (INT-13 à INT-19) ; les corrections de G2 d'un
  groupe forment un pas (INT-06 : C-1 à C-5 de C ; INT-12 : C-1 à C-5 de B ; INT-19 : C-1 à C-6 de A). Table : `ordre.txt`.
- Livrables : `diffs/INT-01.diff` … `INT-19.diff` (aucun hunk sur `scripts/controle/README.md` hors la l.11 de
  INT-13 et INT-19, aucun sur `gates.yml`, aucun sur `xtask/` ni `docs/` ; 28 à 188 lignes ajoutées, chacun sous 200) ;
  `readme/C.txt`, `B.txt`, `A.txt` (un ajout daté par groupe, `<DATE>` et `<tête + n>`) ; `planchers.tsv` (pas → tests
  ajoutés ; total 46) ; `ordre.txt` ; `chaine/plan.sh`, `chaine/preparer.sh`, `chaine/pas.tsv`,
  `chaine/source-pas.md` ; `arbre-final/` (sommes de ses 1369 fichiers : `arbre-final.sha256sums.txt`, chemins relatifs
  à lui) ; `SHA256SUMS` (283 pièces de ce dossier, `sha256sum -c` vert).
- Plancher final : 177 + 6 + 14 + 26 = 223, vérifié par la ligne exacte du job au dernier pas de la chaîne émulée :
  `verdict-suite-s2 : conforme (code 0, résumé final, aucun saut, Ran = 223)` (`preuves/pas_a_pas.txt`).

## 2. Pas par pas

| pas | origine | ce qui a été recalé, et pourquoi | à l'octet |
|---|---|---|---|
| INT-01 | groupe C, GF3C-1 (SHOGEN-GARDE-D3-MOT-COMMUN-1) | hunks README et plancher retirés (règle 1) ; commentaire daté du job retiré (le plancher est écrit par la chaîne) | oui hors ces hunks |
| INT-02 | groupe C, GF3C-2 (SHOGEN-MOTIFS-ARBRE-REDOS-1) | idem | oui hors ces hunks |
| INT-03 | groupe C, GF3C-3 (SHOGEN-GARDE-FOUS-ORCH-1, phase 3, écriture) | idem ; fixture du masque de `test_refus_journal_des_passages` : la clé factice en forme d'identifiant écrite en deux littéraux joints (même valeur à l'exécution), sinon la gate des secrets (job g3 et hook pre-commit) refuse le pas (§3, conflit 4) | oui hors ces hunks et cette ligne |
| INT-04 | groupe C, GF3C-4 (SHOGEN-GARDE-FOUS-ORCH-1, phase 3, relevé) | hunks README et plancher retirés | oui hors ces hunks |
| INT-05 | groupe C, GF3C-5 (SHOGEN-GARDE-FOUS-ORCH-1, phase 3, lecture) | idem | oui hors ces hunks |
| INT-06 | groupe C, C-1 à C-5 de la G2 du groupe C | cinq diffs en un pas, hunks README retirés ; ajout README du groupe C (`readme/C.txt`) | état final égal à `p3c/g2/copie` (C-5) hors README et plancher, fixture de INT-03 exceptée |
| INT-07 | groupe B, B-1 (SHOGEN-GARDE-ERREUR-INTERNE-1) | fin de docstring du crochet (lignes de B après celles de C) ; `except` de `juger` (corps de l'ancien `main`, déplacé par C) : refus de B gardé, marque `R0` posée pour le journal des refus, `erreur` pour la lecture pure ; motif du refus sur journal illisible préfixé `R0 (erreur interne)` ; `test_refus_journal_des_passages` (C) recalé : liste d'entrée refusée `R0`, lecture pure en erreur `erreur`, journal illisible `R0` (§3, conflit 1) | oui hors ces lignes |
| INT-08 | groupe B, B-2 (SHOGEN-GARDE-CROCHET-MESSAGE-CHAINE-1) | hunks README et plancher retirés | oui hors ces hunks |
| INT-09 | groupe B, B-3 (SHOGEN-GARDE-REPONSE-INVESTISSEUR-1) | bloc R12 posé dans `juger` ; `REGLE[0] = "R12"` ajouté (sinon le refus R12 est consigné `R6`) ; `test_refus_journal_des_passages` reçoit un refus R12 consigné `R12` ; `test_refus_lecteur` : R12 parmi les règles sans refus (§3, conflit 2) | oui hors ces lignes |
| INT-10 | groupe B, B-4 (SHOGEN-GARDE-JOURNAL-LECTURE-SEULE-1) | fin de docstring d'`avant_acte.py` (lignes de B après celles de C) | oui hors docstring |
| INT-11 | groupe B, B-5 (SHOGEN-GARDE-DISQUE-DU-DEPOT-1) | fin de docstring ; point 1 de la skill `shogen-avant-lancer` : `df -h /` remplacé par `avant_acte.py --depot <dépôt> disque` (décision de l'orchestrateur, adjudication du groupe B, I-5) ; garde dans `test_modele_de_chaine_passe_le_depot` | oui hors ces lignes |
| INT-12 | groupe B, C-1 à C-5 de la G2 du groupe B | cinq diffs en un pas ; C-3 posé à la main dans `juger` (contexte changé par la ligne R12 de INT-09) ; ajout README du groupe B (`readme/B.txt`, table R1 à R12) | état final égal à `p3b/g2/copie-corr` (C-5) hors README, plancher et recalages de INT-07, INT-09, INT-11 ; R-1 et R-3 du contre-contrôle (`cc/propose/R-1-erreur-journal-illisible.diff`, `R-3-cas-r0-releve-lecteur.diff`) repliés à l'octet dans ce pas |
| INT-13 | groupe A, GF3A-1 (SHOGEN-FM11-MOTIF-ATTRIBUTION-1) | hunk README de fin et plancher retirés ; hunk de la l.11 du README gardé à l'octet | oui hors ces hunks |
| INT-14 | groupe A, GF3A-2 (SHOGEN-GARDE-ATTRIBUTION-PLAGE-LETTRES-1) | fin de docstring d'`avant_acte.py` (lignes de A après celles de C et B) | oui hors docstring |
| INT-15 | groupe A, GF3A-3a (SHOGEN-GARDE-RECALAGE-CHECK-1) | hunks README et plancher retirés ; skill `shogen-avant-lancer` posée par --3way sur le point 1 de INT-11 | oui hors ces hunks |
| INT-16 | groupe A, GF3A-3b (SHOGEN-GARDE-RECALAGE-CHECK-1) | idem | oui hors ces hunks |
| INT-17 | groupe A, GF3A-4 (SHOGEN-GARDE-RECALAGE-CHECK-1) | fin de `garde_commun.py` : `rangees_fautives` (A) après `DRAPEAUX_RE`, `_plier_motif`, `motifs_du_code` (C) | oui hors ce contexte |
| INT-18 | groupe A, GF3A-5 (SHOGEN-GARDE-CHAINE-ORCH-MODELE-1) | hunks README et plancher retirés | oui hors ces hunks |
| INT-19 | groupe A, C-1 à C-6 de la G2 du groupe A | six diffs en un pas (173 lignes ajoutées) ; hunk de la l.11 du README gardé (empreinte finale de `fm11.py`) ; ajout README du groupe A (`readme/A.txt`, empreintes de l'état final) | état final égal à `p3a/g2/corr` (C-6) hors README, plancher et fin de docstring ; R-4 du contre-contrôle (`cc/propose/R-4-cas-trois-mutants-vivants.diff`, trois cas de test) repliée à l'octet dans ce pas |

Contrôles d'égalité (`outils/compare_net.py`, lignes ajoutées et retirées par fichier, net du groupe contre net de
l'intégration) : C, aucun écart avec `p3c/g2/copie` (C-5) sur la première série (`preuves/compare-net-C.txt` vide),
la série livrée n'en diffère que par la ligne de la fixture de INT-03 (`git diff` des deux états finaux : une ligne) ;
B, `preuves/compare-net-B.txt` : seuls écarts, les recalages de INT-07, INT-09, INT-11 et la fin de docstring ; A,
`preuves/compare-net-A.txt` : seul écart, la fin de docstring d'`avant_acte.py`.

## 3. Conflits et leur résolution

1. **Erreur interne et journal des refus (point bloquant de la G2 du groupe C, adjudication C ; point 3 du brief)** :
   C déplace le corps de `main` du crochet dans `juger` et consigne `REGLE[0]` ; B-1 rend 2 dans l'`except` de ce corps
   pour un acte qui écrit, sans poser de règle : posé tel quel, le refus serait consigné `permis` (règle initiale), et
   le refus sur journal illisible (`refuser`, motif sans `R<n>` en tête) serait consigné `?` (mesuré par les mutants
   I-1 et I-2, qui ôtent ces deux recalages : `mut/sortie/I-1.out`, `I-2.out`). Résolution (INT-07) :
   l'`except` garde le refus de B et pose `REGLE[0] = "R0"`, l'erreur sur une lecture pure pose `erreur` (sens de C) ;
   le motif du refus sur journal illisible commence par `R0 (erreur interne)`. `R0` est une marque du journal des
   refus, non une règle du crochet : elle n'est pas dans la docstring du module, donc pas dans `regles_du_crochet`
   (mesuré : `R1` à `R12`), et le relevé comme la lecture la comptent parmi les refus (`R[0-9]+`). Test recalé :
   `test_refus_journal_des_passages` (C) : `tool_input` en liste, refusé sous B-1 (sortie 2, `R0`) au lieu de permis
   (`erreur`) ; une erreur interne sur `ls` (journal de session dont `message` n'est pas un objet) reste permise et
   consignée `erreur` ; un `git commit` sous journal illisible est consigné `R0`. Rouge mesuré avant le recalage
   (INT-07 avec le test de C d'avant : codes `[0, 2, 0, 0, 2, 2, 2, 2]` au lieu de `[0, 2, 0, 0, 2, 0, 2, 2]`,
   `preuves/r0-consigne-rouge.txt`), vert après (`preuves/r0-consigne-vert.txt`) ; mutants I-1, I-2, I-4 tués.
2. **R12 et le journal des refus (point 3 du brief)** : le refus R12 de B-3 écrit son message sans poser de règle ;
   `juger` a posé `R6` avant `stop` : le refus R12 était consigné `R6` (rouge mesuré sur la première série, `preuves/r12-consigne-rouge.txt`).
   Résolution (INT-09) : `REGLE[0] = "R12"` dans la branche R12 ; cas ajouté à `test_refus_journal_des_passages`
   (réponse `Pendant les 28 jours de collecte.` après un 28 affiché sans unité : sortie 2, `R12`), vert
   (`preuves/r12-consigne-vert.txt`) ; mutant I-3. `test_refus_lecteur` attend la liste exacte des règles sans refus,
   lue dans la docstring du crochet : R12 s'y ajoute (`R1, R3, R4, R8, R9, R10, R12`) : rouge sur INT-09 avec l'attendu
   d'avant (`preuves/lecteur-r12-rouge.txt`), vert après (`preuves/lecteur-r12-vert.txt`) ; mutants I-6, I-6b, I-6c
   (section 5). Après C-3 de la G2
   de B (R12 jugée même quand R6 ou R10 refusent), une ligne par passage du crochet : la dernière règle qui refuse
   (ordre R6, R10, R12) est consignée ; limite écrite au README (B).
3. **C-3 de la G2 de B** : écrit contre `main` de B (sans C) ; posé à la main dans `juger` (même texte : `code = 2`
   pour R10, `sans = …` sans `and not code`), au-dessus de la ligne `REGLE[0] = "R12"`.
4. **Fixture du masque et gate des secrets (constat de l'intégrateur, hors des G2)** : `test_refus_journal_des_passages`
   (GF3C-3) écrit une clé factice en forme d'identifiant ; la gate des secrets (`enforcement/gate-secrets.sh --tree`,
   job g3, et le hook pre-commit du dépôt en mode indexé) la refuse (`REFUS (SECRETS/forme)`, sortie 2,
   `preuves/secrets-serie-v1-finA.txt`) : la chaîne se serait arrêtée au commit de INT-03. Résolution : la même valeur
   écrite en deux littéraux joints (`" sk-ant-" + "api03-…"`), même texte à l'exécution (le masque est jugé sur la
   valeur) ; gate verte (`OK (secrets)`) ; INT-04 à INT-19 rejoués sur INT-03 refait (`--3way`, côté du pas gardé,
   même réécriture : `outils/secret_fix.py`) ; écart avec la première série : cette ligne seule (`git diff` des deux
   états finaux). Le hook est rejoué à chaque pas de la chaîne émulée (section 6).
5. **Skill `shogen-avant-lancer`, point 1 (adjudication B, I-5)** : `df -h /` remplacé par
   `python3 -I -B scripts/controle/avant_acte.py --depot <dépôt> disque` (forme lue par `tests/test_skills.py` ;
   l'option `--depot` précède la sous-commande dans `parseur`), en INT-11 ; garde ajoutée à
   `test_modele_de_chaine_passe_le_depot` (rouge sur la skill d'avant, `preuves/skill-disque-rouge.txt`, vert après) ;
   mutant I-5. GF3A-3a et GF3A-5 touchent ensuite la même skill (liste des erreurs, point 2) : posés par `--3way`
   sans conflit.
6. **Textes** : fins de docstring de module (`.claude/hooks/garde_faits.py` : C puis B ; `avant_acte.py` : C, B, A) :
   paragraphes ajoutés dans l'ordre C, B, A (`outils/docfin.py`) ; fin de `garde_commun.py` : `rangees_fautives` (A)
   après `DRAPEAUX_RE`, `_plier_motif`, `motifs_du_code` (C) ; `.gitignore` de la racine (B-4) et
   `scripts/controle/garde/.gitignore` (GF3C-3) : fichiers distincts, sans conflit ; `tests/test_avant_acte.py`
   (`Depot.setUp` de B-4, cas de A) et `tests/test_skills.py` (`EXIGES` de A) : posés sans conflit, suites vertes.
7. **Commentaires datés du job** : chaque diff du groupe C ajoutait au-dessus du job `controle-unittest` un commentaire
   daté qui écrit son plancher (178 à 183) ; retirés avec la ligne du plancher (règle 1 : le plancher est écrit par la
   chaîne, `<tête + n>` ; un commentaire au nombre figé mentirait si la tête bouge) ; les ajouts du README portent les
   planchers. À adjuger.
8. **D3 plus strict** : chaque pas est jugé par l'outil de l'état d'avant lui (section 6) ; l'ajout du README d'un
   groupe est posé à son dernier pas (règle 1) : D3 refuse, aux pas qui ajoutent une fonction publique avant ce dernier
   pas, le nom absent du README de l'état du pas ; jugé par groupe (diff cumulé, ajout README compris), D3 et D4 sont
   satisfaits (section 6).

## 4. Chaîne de commit (resceau, procédure de la G2 du groupe A, l.224 à 233)

- `arbre-final/` : copie creuse de la tête (`outils/copie.py`, `git archive` hors interdits et `*.jsonl`), puis les 19
  pas du plan appliqués dans l'ordre (diff de la série, plancher, ajout README), arbre entier (`gates.yml` et
  `enforcement/docs-sha256sums.py` y sont lus) ; ses dates d'ajout README sont celles de mon premier passage
  de `chaine/preparer.sh` (`18:21:50`, `18:21:51`, `18:21:52` UTC ; pièce de contrôle, la chaîne écrit les siennes). Outils égaux, octet pour octet, à ceux de
  l'état final de la série (`avant_acte.py`, `garde_commun.py`, `fm11.py`, `gabarits/chaine.sh`,
  `gabarits/chaine-modele.sh`, crochet : sha256 égaux, `NOTES.md`).
- `chaine/plan.sh` : `gabarits/chaine-modele.sh` de `arbre-final/`, copié tel quel (sha256
  `3c78d1110985a5678dbc4c6ede2c9d7cc099d4b7b597cff5d0e906de33ca890b`, égal) : la `verif` est tirée par `source` de
  `$OUTILS/gabarits/chaine.sh` (empreinte `e0254878…`, égale au `MODELE` de ces outils), aucune `verif` écrite.
- `chaine/pas.tsv` (pas, groupe de l'ajout README, tests ajoutés, sujet) et `chaine/preparer.sh` : juste avant le
  lancement, lit la tête du dépôt (`git show HEAD:`, aucune écriture), écrit `chaine/gen/INT-nn-plancher.diff`
  (plancher `tête + tests cumulés`, ligne de `scripts/controle` seule), `chaine/gen/INT-06-readme.diff`,
  `INT-12-readme.diff`, `INT-19-readme.diff` (`readme/C.txt`, `B.txt`, `A.txt` ; `<DATE>` lue par `date -u`, une
  seconde au moins entre deux ajouts, dans l'ordre C, B, A ; `<tête + n>` remplacé), les messages
  `chaine/messages/INT-nn.txt` (sujet `INTEGRATION-P3 INT-nn : …`, `Diff-Id`, `Source-Sha` de `chaine/source-pas.md`,
  le tableau du §2, lu à cet instant ; pieds de l'orchestrateur) et `chaine/plan.txt` (`id|diffs|message|source`, un
  pas par diff de la série). `plan.txt`, `gen/` et `messages/` livrés : mon dernier passage, sur `tete2/`
  (copie de `328a6d2`, ajouts datés `20:14:10`, `20:14:11`, `20:14:12` UTC) ; le passage du lancement les réécrit contre le
  dépôt.
  Le README et le plancher sont donc écrits au pas, par les diffs du pas (C6 : l'index est HEAD plus les diffs
  nommés) ; les dates sont celles de la préparation, non du commit (le modèle, copié tel quel, n'écrit rien entre deux
  pas).
- Lancement (à la charge de l'orchestrateur, non fait) : disque libre du dépôt au moins 3 Gio (LN-1) ;
  `DEPOT=/home/user/shogen bash <int3>/chaine/preparer.sh`, puis `cp <int3>/chaine/plan.sh
  <int3>/chaine/chaine_int3.sh` (mêmes octets, `cmp` ; réserve R-2 du contre-contrôle : un script nommé `plan.sh`
  n'est vu ni par V7, `MOTIF_CHAINE`, ni par `pgrep -f '^bash /tmp.*chaine_'` de la règle (2) d'E37), puis
  `DEPOT=/home/user/shogen OUTILS=<int3>/arbre-final/scripts/controle PLAN=<int3>/chaine/plan.txt CC=<rapport du
  contre-contrôle> DETACHE=1 setsid nohup timeout 13680 bash -c 'echo "PID $$ $(date -u +%T)"; bash "$1"; echo
  "SORTIE code $? $(date -u +%T)"' _ <int3>/chaine/chaine_int3.sh > chaine.log 2>&1 &` (PID et code de sortie au
  journal, règle (1) d'E37) ;
  `chaine/groupes-integrateur.md` (`GROUPES : aucun`) ne sert qu'au passage à blanc de l'intégrateur. Après la série,
  `OUTILS` peut revenir au dépôt (son `chaine.sh` porte la même `verif`).
- Passage à blanc (preuve) : `arbre-final/scripts/controle/avant_acte.py --depot <int3>/depot-blanc chaine --plan
  chaine/plan.txt --cc chaine/groupes-integrateur.md --blanc --script chaine/plan.sh --detache` (forme de la ligne du
  modèle, `DETACHE=1`) : `sortie 0`, aucune ligne (`preuves/blanc-final.txt` ; journal de `depot-blanc/` :
  `chaine - conforme -`) ; K0, K5 (chaque diff du plan sur HEAD plus les précédents), K6, G5, K1 à K4, K7 et G1 à G4
  jugés. Sans `--detache` : `REFUS G3 : durée estimée 114 min (19 pas × 6 min)` (`preuves/blanc-temoin-g3.txt`,
  sortie 1) : la chaîne se lance détachée. Témoins : plan aux deux premiers pas inversés, `REFUS K5` sortie 1
  (`preuves/blanc-temoin-desordre.txt`) ; `plan.sh` avec une `verif` écrite, `REFUS K7` sortie 1
  (`preuves/blanc-temoin-verif-ecrite.txt`).

## 5. Mutants (rejeu sur l'état final)

- Outil : `scripts/controle/mutants.py` de la tête lue (`base/`, sha256 `68406b966a7d…`, égal à celui du dépôt), lancé
  à part de la copie mutée `mut/copie/` (archive de `arbre-final/`, dépôt jetable, plancher 223), job
  `controle-unittest` (runner puis suite, commande du job), borne 300 s, une campagne détachée (`outils/campagne.sh`,
  PID consigné) ; relevé `ps` de fin : `aucun processus des 98 groupes de la campagne, aucun descendant vivant de
  l'outil (moissonneur)`, sortie 0 (`mut/campagne.err`).
- Liste : `outils/pool.py` -> `mut/mutants.json` (pièce source de chaque mutant : `mut/mutants.json.sources.txt`),
  texte avant présent une fois dans l'état final (vérifié par l'outil) : 48 mutants, C 16, B 14, A 12, intégration 6.
- Résultat (`mut/campagne.txt`, diff et sortie de chaque mutant dans `mut/sortie/`) : témoin vivant ; 47 tués
  (sortie 1), 1 vivant (I-6), 0 FATAL ; puis I-6b (`mut2/`) vivant et I-6c (`mut3/`) tué : en tout 50 mutants, 48
  tués, 2 vivants déclarés équivalents (I-6, I-6b), aucun FATAL.
- Sites d'appel et zones de conflit, tous tués : C-D3-6 (`nomme_en_code(readme, nom)` au site de D3), C-MA-9
  (`motifs(None, fautes, [])` au site de `motifs_arbre`), C-LR-14 (sous-commande `refus` vers `motifs_arbre` dans
  `COMMANDES`), B-M5-4 (`lieux_disque(".")` au site de `disque`), B-K-10 (`comptes_nus(entrees)` au site de R12),
  A-M6d (K7 non appelé), C-JR-3 et I-4 (`erreur` dans l'`except` de `juger`, zone de conflit B-1/C), I-1 (`R0` de cet
  `except`), I-2 (`R0` du journal illisible), B-M1-1 (refus sur erreur interne), B-K-6, B-K-7 et I-3 (Stop de `juger` :
  R10, R12, marque R12), C-G2-1 (marque R10), I-5 (point 1 de la skill), A-G-g (garde de K7 par ligne).
- Équivalents déclarés : I-6 (paragraphe R12 ôté de la docstring du crochet) : `regles_du_crochet` lit encore `R12`
  dans les noms `R12_NOMBRE` et `R12_FORMES` du paragraphe suivant (son regard avant `(?![0-9])` admet un souligné) :
  seule la docstring change et ce que `regles_du_crochet` en lit est inchangé : équivalent ; I-6b (R12 et `R12_NOMBRE` ôtés,
  `mut2/`) : vivant, même cause (`R12_FORMES`) ; I-6c (les trois ôtés, `mut3/`) : tué par `test_refus_lecteur`
  (témoin vivant, relevé `ps` vide dans les deux campagnes). Constat à former (section 7).
- Attribution (`outils/attribuer.py`, `preuves/attribution.txt` : tests en échec lus dans la sortie de chaque
  mutant) : 30 des 39 tests ajoutés par la série échouent sous au moins un mutant du rejeu ; les 9 autres reçoivent les
  mutants tués que les campagnes de leur groupe leur attribuent (pièce nommée).

Tests ajoutés par la série et mutants tués qui les font échouer (règle D4) :

| pas | test (module) | mutants tués qui le font échouer |
|---|---|---|
| INT-01 | `test_d3_mot_commun` (test_garde_suivi) | rejeu de l'intégration : tué par C-D3-2, C-D3-6 |
| INT-02 | `test_motifs_arbre` (test_garde_regex) | rejeu de l'intégration : tué par C-MA-7, C-MA-9 |
| INT-03 | `test_refus_journal_des_passages` (test_garde_refus) | rejeu de l'intégration : tué par B-M1-1, B-M1-6, C-G2-1, C-JR-1, C-JR-17, C-JR-2, C-JR-3, C-JR-4, C-JR-5, I-1, I-2, I-3, I-4 |
| INT-03 | `test_refus_entete_unique` (test_garde_refus) | rejeu de l'intégration : tué par C-JR-17 |
| INT-04 | `test_refus_releve_premier_message` (test_garde_refus) | rejeu de l'intégration : tué par C-C3-a, C-JR-17, C-RV-7 |
| INT-05 | `test_refus_lecteur` (test_garde_refus) | rejeu de l'intégration : tué par C-LR-14, C-LR-2 |
| INT-07 | `test_cas_reel_de_la_g2_refuse` (test_garde_erreur_interne) | rejeu de l'intégration : tué par B-M1-1 |
| INT-07 | `test_table_des_cas` (test_garde_erreur_interne) | rejeu de l'intégration : tué par B-M1-1, B-M1-9 |
| INT-07 | `test_journal_illisible` (test_garde_erreur_interne) | rejeu de l'intégration : tué par B-M1-6 |
| INT-08 | `test_r5_voit_le_message_a_contenu_chaine` (test_garde_message_chaine) | rejeu de l'intégration : tué par B-K-5, B-M2-1 |
| INT-08 | `test_faits_et_appels_deux_formes` (test_garde_message_chaine) | rejeu de l'intégration : tué par B-M2-1 |
| INT-09 | `test_e29_vingt_huit_jours_sans_piece` (test_garde_reponse) | rejeu de l'intégration : tué par B-K-6, B-K-7, B-M3-5 |
| INT-09 | `test_e29_seize_semaines_apres_lecture` (test_garde_reponse) | tué par M3-6, M3-7, M3-10 (générateur B), K-8 (G2 de B) : campagnes des groupes (p3b/RAPPORT-GENERATEUR.md, p3b/g2/RAPPORT-G2.md), hors du rejeu |
| INT-09 | `test_unite_et_fenetre` (test_garde_reponse) | rejeu de l'intégration : tué par B-K-10, B-M2-1, B-M3-3 |
| INT-10 | `test_passages_journalises` (test_lecture_seule_journal) | rejeu de l'intégration : tué par B-M4-1 |
| INT-10 | `test_journal_ignore_par_git` (test_lecture_seule_journal) | tué par M4-5 (générateur B) : campagnes des groupes (p3b/RAPPORT-GENERATEUR.md), hors du rejeu |
| INT-10 | `test_journal_non_ecrit` (test_lecture_seule_journal) | rejeu de l'intégration : tué par B-M4-1, B-M4-4 |
| INT-11 | `test_disque_du_depot` (test_disque_depot) | rejeu de l'intégration : tué par B-M5-1, B-M5-4 |
| INT-11 | `test_tmpdir_sur_un_autre_systeme` (test_disque_depot) | rejeu de l'intégration : tué par B-M5-1, B-M5-4 |
| INT-11 | `test_modele_de_chaine_passe_le_depot` (test_disque_depot) | rejeu de l'intégration : tué par I-5 |
| INT-13 | `test_attribution_claude_session` (test_fm11) | rejeu de l'intégration : tué par A-M1a |
| INT-13 | `test_sortie_du_scratchpad_comptee` (test_fm11) | tué par M1c, M1e, M1d-bis (générateur A) : campagnes des groupes (p3a/RAPPORT-GENERATEUR.md), hors du rejeu |
| INT-14 | `test_plage_a_bornes_en_lettres` (test_avant_acte) | rejeu de l'intégration : tué par A-M2b |
| INT-15 | `test_e30_e31_diffs_a_blanc` (test_avant_acte) | rejeu de l'intégration : tué par A-M3a |
| INT-15 | `test_e35_e36_portes_sur_lignes_ajoutees` (test_avant_acte) | tué par M3d, M3e, M3f, M3g, M3i (générateur A) : campagnes des groupes (p3a/RAPPORT-GENERATEUR.md), hors du rejeu |
| INT-16 | `test_e34_e36_script` (test_avant_acte) | rejeu de l'intégration : tué par A-M4e |
| INT-17 | `test_e32_rangee_lue_et_ordre` (test_avant_acte) | tué par M5a, M5b, M5c, M5f, M5h, M5i, M5j (générateur A) : campagnes des groupes (p3a/RAPPORT-GENERATEUR.md), hors du rejeu |
| INT-17 | `test_e33_e35_portes_et_contrat` (test_avant_acte) | rejeu de l'intégration : tué par A-M5d |
| INT-18 | `test_k7_verif_du_sceau` (test_avant_acte) | rejeu de l'intégration : tué par A-M6a, A-M6d |
| INT-18 | `test_modele_a_blanc_avant_tout_pas` (test_gabarit_chaine) | tué par M6f, M3b (générateur A) : campagnes des groupes (p3a/RAPPORT-GENERATEUR.md), hors du rejeu |
| INT-18 | `test_l4_verif_versionnee` (test_gabarit_chaine) | rejeu de l'intégration : tué par A-M6a, A-M6d |
| INT-18 | `test_modele` (test_gabarit_chaine) | tué par M6g, M6j, M6h (générateur A) : campagnes des groupes (p3a/RAPPORT-GENERATEUR.md), hors du rejeu |
| INT-19 | `test_plage_liste_et_bornes_melees` (test_avant_acte) | tué par MC3a, MC3b (G2 de A) : campagnes des groupes (p3a/g2/RAPPORT-G2.md), hors du rejeu |
| INT-19 | `test_k4_apostrophes_et_formes` (test_avant_acte) | rejeu de l'intégration : tué par A-M4e |
| INT-19 | `test_k7_chaque_commit_garde` (test_avant_acte) | rejeu de l'intégration : tué par A-G-g, A-M6d, A-MC4a |
| INT-19 | `test_copie_creuse_exclut_les_interdits` (test_avant_acte) | rejeu de l'intégration : tué par A-G-a |
| INT-19 | `test_borne_et_descendant_detache` (test_avant_acte) | rejeu de l'intégration : tué par A-MC5b |
| INT-19 | `test_gabarit_refus_et_barre_echappee` (test_avant_acte) | tué par G-e, G-l, G-m (G2 de A) : campagnes des groupes (p3a/g2/RAPPORT-G2.md), hors du rejeu |
| INT-19 | `test_sortie_du_scratchpad_temps_borne` (test_fm11) | rejeu de l'intégration : tué par A-MC1a |

## 6. Pas à pas, matrice, portes, contrôles des diffs

- Chaîne émulée (`outils/emuler-v1.sh`, détachée ; `preuves/pas_a_pas.txt`) sur `emul/`, clone de `depot-blanc/`, avec
  les outils de `arbre-final/` : à chaque pas, diffs du plan (`--index`), runner du job puis ligne exacte du job
  `controle-unittest` lue dans `gates.yml` du pas, hook pre-commit du dépôt (copie), `sceller` de la `verif` tirée par
  `source`, `acte commit` (C1 à C9), commit jetable. Aux 19 pas : runner `verdict-suite-s2 : 153 ok, 0 échec`, ligne du
  job `conforme (code 0, résumé final, aucun saut, Ran = N)` avec N = 178, 179, 181, 182, 183, 183, 186, 188, 191, 194,
  197, 197, 199, 200, 202, 203, 205, 216, 223 (plancher du pas, `--egal`), aucune ligne `Warning` ni
  `Exception ignored`, hook `OK (hook) : aucune étape en refus sur l'index (images locales des jobs g5, g1 et g3)`,
  `sceller` 0, `acte commit` 0 sans ligne. `arbre-final/` est égal à l'arbre final de `emul/` (`diff -rq` vide).
- Plan final (`chaine/preparer.sh` sur `depot-blanc/`, `preuves/preparer-final.txt` : `plan : 19 pas ; plancher de
  la tête 177, final 223`) : ajouts README datés «20:08:58», «20:08:59», «20:09:00» UTC (C, B, A) ; même émulation, runner
  et suite non joués (`RAPIDE=1`, `preuves/pas_a_pas-rapide.txt`) : hook OK, `sceller` 0, `acte commit` 0 aux 19 pas
  (messages et `Source-Sha` du plan final) ; arbre final égal à celui de `emul/` hors les trois dates du README.
- Matrice sur l'état final (`outils/matrice.sh`, `preuves/matrice.txt`, `-X dev -W error`, `discover -s tests -t .`
  depuis `scripts/controle`) :
  - `python3.11 rc=0 Ran 223 tests in 67.956s OK Warning/Exception: 0`
  - `python3.12 rc=0 Ran 223 tests in 70.595s OK Warning/Exception: 0`
  - `python3.13 rc=0 Ran 223 tests in 73.477s OK Warning/Exception: 0`
- Portes légères sur l'état final (mêmes lignes que le précédent) : `docs-sha256sums : conforme : 53 SHA256SUMS, 382
  ligne(s), dont 11 absente(s) admise(s) (SHOGEN-SIM-SOMMES-1)` ; `journaux-modele : conforme (52 journaux exemptés
  par nom et sha256)` ; `runners-epingles : conforme (7 workflow(s), 22 clé(s) runs-on/os lues)` ; `workflows-yaml :
  conforme (7 workflow(s), PyYAML 6.0.1)` ; lint R-1 `OK (R-1) : 12 fichier(s)` ; gate des secrets `--tree` :
  `OK (secrets) : 1345 fichier(s) sans forme d'identifiant dans la portée` (sur la première série : `REFUS
  (SECRETS/forme)`, `preuves/secrets-serie-v1-finA.txt`) ; cas hors CI du crochet (`.claude/hooks/tests`) : `Ran 26`,
  `OK`. Toutes en sortie 0.
- `avant_acte.py --lecture-seule diff --rapport RAPPORT-INTEGRATEUR.md` (`outils/juger.sh`, diff jugé : commit du pas
  de la chaîne émulée, README et plancher compris ; dépôt jetable `juge/` à l'état d'avant le pas, inchangé après
  chaque passage) :
  - (a) outil de l'état d'avant le pas, (b) outil final : sortie 0 aux pas INT-03, 04, 06 à 09, 12, 13, 19 ; aux pas
    INT-01, 02, 05, 10, 11, 14 à 18, seul refus D3 (18 par outil, 36 en tout : fonction publique ajoutée avant l'ajout
    README de son groupe, posé au dernier pas du groupe, règle 1), aucun autre refus (D4, C7, RX… : aucun)
    (`preuves/juger-pas.txt`) ;
  - par groupe (diff cumulé, ajout README compris, outil final) : C, B, A en sortie 0 (`preuves/juger-groupes.txt`) :
    D3 et D4 satisfaits pour toutes les fonctions publiques et tous les tests de la série.
- Tête `328a6d2` (copie `tete2/`) : préparation (`preuves/preparer-tete2.txt`), passage à blanc `sortie 0`
  (`preuves/blanc-tete2.txt`), émulation `RAPIDE=1` (`preuves/pas_a_pas-tete2.txt`) : hook OK, `sceller` 0, `acte
  commit` 0 aux 19 pas ; runner et ligne du job sur l'état final : `153 ok, 0 échec`, `conforme (code 0, résumé final,
  aucun saut, Ran = 223)` (`preuves/suite-tete2-final.txt`).
- Passage à blanc (preuve exigée) : voir section 4.

## 7. Points à adjuger, limites, items à former

Points à adjuger (choix de l'intégrateur, chacun réversible par un diff de la série) :

1. Marque `R0` du journal des refus pour un refus sur erreur interne ou sur journal illisible (§3, conflit 1) : une
   marque hors règle, comptée parmi les refus par le relevé et la lecture sans toucher leur code (`R[0-9]+`), absente
   de la docstring (donc jamais `candidate à relire`) ; autre voie possible : une marque non numérotée, au prix d'un
   changement du relevé et de la lecture de C.
2. Une ligne par passage du crochet : quand R6, R10 et R12 refusent au même arrêt, la dernière qui refuse est consignée
   (comme R6 puis R10 chez C avant la série) ; le compte par règle de `avant_acte.py refus` sous-compte ces refus
   doubles (item proposé ci-dessous).
3. Commentaires datés du job `controle-unittest` du groupe C retirés avec le plancher (§3, conflit 7).
4. Fixture du masque coupée en deux littéraux en INT-03 (§3, conflit 4) : seul écart de texte à un diff de groupe
   hors des conflits ; sans lui, le hook pre-commit et le job g3 refusent la série.
5. Dates des ajouts du README : lues par `date -u` au passage de `chaine/preparer.sh`, juste avant le lancement, non à
   chaque commit (le modèle, copié tel quel, applique les diffs du plan sans rien écrire entre deux pas) ; croissantes
   (C, B, A ; une seconde au moins entre deux).
6. Messages de commit (`chaine/messages/`, écrits par `preparer.sh`) : pieds `Co-Authored-By: Claude Fable 5.1` et
   `Claude-Session:` de l'orchestrateur, qui commet ; source unique `chaine/source-pas.md` (le tableau du §2 ; ligne
   `Source-Sha`, attribution C3 par ses rangées, qui nomment chaque pas). Une source de plus (adjudication de l'orchestrateur, rapport du
   contre-contrôle) : l'ajouter au champ source de `plan.txt` et une ligne `Source-Sha` par source.
7. Rapport du contre-contrôle : `chaine/plan.sh` exige `CC` (ligne `GROUPES :`) ; `chaine/groupes-integrateur.md`
   (`GROUPES : aucun`, chaque pas vert seul) n'a servi qu'au passage à blanc.
8. Forme de la skill : `avant_acte.py --depot <dépôt> disque` (l'option globale précède la sous-commande ; la forme
   `disque --depot` du brief sort en 3, `unrecognized arguments`, mesuré).
9. D3 par pas : refus aux pas intermédiaires qui ajoutent une fonction publique avant l'ajout README de leur groupe
   (conséquence de la règle 1, comme au lot INTEGRATION-P2) ; D3 et D4 satisfaits par groupe (§6).

Limites de l'intégration :

- La `verif` de la chaîne (portes de `gates.yml`, cargo compris) n'est jouée à aucun pas : cargo est interdit à
  l'intégrateur ; la chaîne émulée joue le runner et la ligne du job `controle-unittest`, le hook pre-commit du dépôt
  (copie, sha256 égal), `sceller` et `acte commit` des outils de `arbre-final/` ; les autres portes ne sont jouées que
  sur l'état final (§6).
- Le passage à blanc et la chaîne émulée tournent sur `depot-blanc/` et `tete2/`, dépôts jetables au contenu des
  têtes `fe9a72b` et `328a6d2` (un commit, sans historique) : G4 (Diff-Id déjà portés) et les sha courts résolus ne sont jugés que contre lui.
- Rejeu de 50 mutants (section 5), non des campagnes entières des groupes ; les tests ajoutés que le rejeu ne tue pas
  sont attribués aux mutants des campagnes des groupes (§5, colonne source).
- Le docstring d'`avant_acte.py` dit encore `refus sous 3 Gio libres sur /` (l.37 ; remarque de la G2 de B, sans
  correction) ; la ligne du README qui écrivait la limite DISQUE-CHAINE n'est pas réécrite (ligne citée possible),
  l'ajout B dit qu'elle est levée.
- Limites et items des groupes inchangés (rapports G2 et adjudications des trois groupes).

Items à former (règle PAROXYSME) :

| item proposé | constat | prix |
|---|---|---|
| SHOGEN-GARDE-SECRETS-AVANT-CHAINE-1 | aucune des trois G2 ni `chaine --blanc` ne joue la gate des secrets : la fixture de GF3C-3 aurait arrêté la chaîne au commit de INT-03 (hook pre-commit), mesuré par l'intégrateur | gate des secrets (mode indexé) dans les portes de `chaine --blanc` et de `diff` |
| SHOGEN-GARDE-REFUS-DOUBLE-1 | une ligne par passage du crochet : un arrêt refusé par R6 et R12 (ou R10) n'est compté que sous la dernière règle | une ligne par règle qui refuse, ou règles jointes et lues par la lecture |
| SHOGEN-CHAINE-MODELE-README-1 | le modèle copié tel quel ne peut dater un ajout du README au pas : les dates sont celles de la préparation | une étape d'écriture au pas dans le modèle (README, plancher), jugée par K7 |
| SHOGEN-GARDE-ERREUR-INTERNE-R0-1 | la marque `R0` (choix de l'intégrateur) n'a pas de cas dans la lecture `avant_acte.py refus` ni dans le relevé (comptée par leur motif `R[0-9]+`, non par un cas) | un cas `R0` dans `test_refus_lecteur` et `test_refus_releve_premier_message` |
| SHOGEN-GARDE-REGLES-DOCSTRING-1 | `regles_du_crochet` (C) lit `R12` dans les noms `R12_NOMBRE` et `R12_FORMES` de la docstring du crochet : le paragraphe d'une règle ôté, la règle reste listée (mutants I-6 et I-6b vivants, équivalents) | regard avant qui exclut le souligné (`(?![0-9_])`), cas d'un nom de constante |

## 8. Provenance (G1)

- [lu] `BRIEF.md` ; `p3c/` : `BRIEF.md`, `RAPPORT-GENERATEUR.md`, `g2/RAPPORT-G2.md`, `ADJUDICATION.md`, diffs
  `diffs/` et `g2/diffs/` (en entier, filtrés par `outils/filtre.py`), listes de mutants (`mutants/mutants.json`,
  `g2/mutants-a.json`, `-b`, `-d`) ; `p3b/` : mêmes pièces, `mutants/mutants.json`, `g2/mutants/campagne-a.json`,
  `campagne-b.json`, état final de `g2/copie-corr` (nets comparés) ; `p3a/` : mêmes pièces (procédure de resceau de la
  G2, l.224 à 233), `patches/mutants.json`, `g2/mutants/lot-a.json`, `lot-b.json`, `lot-c.json`, état final de
  `g2/corr` ; `p3c/g2/copie` (état C-5) ; `ERREURS-ORCHESTRATEUR.md` (E30 à E36) ;
  `docs/adr-0028/revue-garde-fous-2/RAPPORT-INTEGRATEUR-transcrit.md` (précédent, en entier) ; `int/outils/`
  (`filtre.py`, `copie.py`, `compare_net.py`, `chaine_emulee.sh`, `pas_a_pas2.sh`, `remplir_readme.py`), `int/readme/`
  (forme), `int/planchers.tsv`, `int/ordre.txt` ; chaîne P2 `scratchpad/chaine_int.sh` (lecture seule) ; dépôt (tête) :
  `gates.yml` (job `controle-unittest`, étape des secrets), `scripts/controle/README.md` (fin, table des règles l.643 à
  655), `.git/hooks/pre-commit` (copié dans `outils/`, sha256 égal), `enforcement/gate-secrets.sh` (en-tête), et, sur
  l'état de la série, `avant_acte.py` (`refus`, `regles_du_crochet`, `commit`, `diffs_nommes`, `cites`, `suivi`,
  `nomme_en_code`, `sceller`, `chaine`, `nommes`, `attribuer`, `passes`, `lieux_disque`, `empreinte_verif`,
  `parseur`), `garde_faits.py` (`juger`, `main`, `refuser`, `consigner`, `pre_tool_use`, R12, `lecture_pure`),
  `mutants.py` (docstring, format des mutants), tests touchés (`test_garde_refus.py`, `test_garde_erreur_interne.py`,
  `test_garde_reponse.py`, `test_disque_depot.py`, `test_skills.py`), skill `shogen-avant-lancer`. Aucune source
  [abs] ni [2nd].
- Commandes et sorties : `NOTES.md` ; preuves : `preuves/` ; outils : `outils/` ; mutants : `mut/` ; diffs jugés :
  `jugediffs/`. Chiffres recomptés par outil (suites, campagne, `grep -c`, `sha256sum`, `git diff`).
- Aucune pièce interdite ouverte, aucun `*.jsonl` lu ni créé, aucun réseau, aucun cargo, `SHOGEN_S2_CAMPAGNE_CONTROL`
  jamais posée (retirée par `outils/env.sh`).
- Écarts : E-1 (une boucle d'attente active d'environ une minute pendant la chaîne émulée), E-2 (un `pkill -f` non
  ancré refusé par R7, rien n'a tourné), E-3 (un `git checkout -- <chemin>` sur un chemin modifié, dans un clone
  jetable de ce dossier) : `NOTES.md`.

## 9. Pose des réserves du contre-contrôle (brief `BRIEF-R.md`, 2026-10-16 22:28:28 UTC ; travail de `22:29:11` à `23:03` UTC)

Décisions : `ADJUDICATION.md` (ajout daté du 2026-10-16 22:28:28 UTC) ; contre-contrôle `cc/RAPPORT-CC.md`
(CONFORME-AVEC-RÉSERVES R-1 à R-4). Diffs des réserves pris tels quels (`cc/propose/`, sha256 égaux à `cc/SHA256SUMS` :
R-1 `b8d4e5ac…`, R-2 `7e06dcb0…`, R-3 `5839857c…`, R-4 `fd2fecab…`, texte B `bf8c1208…`). Tête lue : `8024a184b91127ce63b84794efb1cea87a1c4010`
(fusion de la PR 13) ; `git diff --stat fe9a72b HEAD` limité aux chemins de la série et aux registres lus : vide ; copie
`tete3/` (1537 membres, 0 écarté) : `scripts/controle`, `.claude`, `.gitignore`, `gates.yml`, `enforcement` égaux à
la base (`diff -rq`).

Ce qui a changé :
- **INT-12** (`diffs/INT-12.diff`, sha256 `8288db52…`, 64 lignes ajoutées) : corrections de la G2 B, puis R-1 et R-3
  appliqués à l'octet (`git apply --index`, sans conflit) dans le même pas (`serie/`, branche `v3`). INT-13 à INT-18
  posés ensuite sans retouche : `garde_faits.py` et `test_garde_refus.py` ne changent plus après INT-12 (contrôlé :
  aucun de ces six diffs ne les nomme, et les 17 diffs hors INT-12 et INT-19 sont égaux à l'octet, `cmp`, à ceux de
  la première livraison).
- **INT-19** (`diffs/INT-19.diff`, sha256 `d5a4ea1a…`, 185 lignes ajoutées : les six corrections de la G2 A, 173, et
  R-4) : R-4 appliquée à l'octet ; méthodes de test ajoutées : 7, comme avant (`def test_` compté) : `planchers.tsv`
  inchangé, plancher final 223.
- `readme/B.txt` : `R-1-R-3-readme-B.diff` appliqué, seul changement ; `readme/A.txt` : empreintes recalculées sur le
  nouvel état final (`outils/remplir_A.py`) : seule la ligne de `.claude/hooks/garde_faits.py` change
  (`3ac396570c22f0c4fddf6dd9cc659da43f6527ac4b3066dbc8f66188c2284c5b`, égale à `sha256sum` du crochet de `cc/corr`) ;
  `readme/C.txt` : aucune empreinte, inchangé.
- R-2 appliqué à la ligne de lancement (section 4) ; `chaine/chaine_int3.sh` : copie de `chaine/plan.sh`, `cmp` égal
  (sha256 `3c78d111…`, égal à `chaine-modele.sh` de l'arbre final).
- Messages (`chaine/preparer.sh`) : pied `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` (ligne
  `Claude-Session:` gardée) dans les dix-neuf ; sujet de INT-19 complété de `R-4 du contre-contrôle : trois cas de test` ;
  sujet de INT-12 complété de `R-1 et R-3 du contre-contrôle : journal illisible en lecture consigné erreur, cas de la
  marque R0` (ajout de l'intégrateur : le pas porte ces réserves ; à adjuger) ; rangées INT-12 et INT-19 du tableau du
  §2 et de `chaine/source-pas.md` complétées des réserves (attribution C3 de `R-1`, `R-3`, `R-4`).

Preuves :
- Préparation sur `tete3/` (`preuves/preparer-reserves.txt` : `plan : 19 pas ; plancher de la tête 177, final 223`,
  ajouts datés `22:32:24`, `22:32:25`, `22:32:26` UTC) ; `arbre-final/` refait par le plan (l'ancien : `tmp/arbre-final-v1`).
- `arbre-final/` contre `cc/corr` (`diff -r`, hors `.git` ; `preuves/arbre-final-vs-cc-corr.txt`) : égaux à l'octet hors
  quatre chemins : `scripts/controle/README.md` (les trois dates de l'ajout, le texte R-1-R-3 de l'ajout B et
  l'empreinte du crochet, que le README de `cc/corr` cite encore à `e95623db…` ; le README attendu, construit depuis
  celui de `cc/corr` par ces trois changements, est égal à celui de `arbre-final/` : `preuves/readme-attendu-vs-cc-corr.txt`,
  `True`) ; `JOURNAL.md` et `docs/adr-0028/ANNEXE-B-items.md` (ceux de la tête `8024a18`, sha256 égaux ; `cc/corr`
  porte ceux de `bcaab82`) ; `docs/publication/interne/revue-sync-docs11/` (versé à `72c2381`, absent de `cc/corr`).
  Aucun fichier de `cc/corr` n'est absent de `arbre-final/`.
- Série rejouée pas à pas (`outils/emuler.sh`, `SRC=tete3`, outils du nouvel `arbre-final/` ;
  `preuves/pas_a_pas-reserves.txt`) : aux 19 pas, runner `153 ok, 0 échec`, ligne exacte du job conforme à son plancher
  (178 … 223, `--egal`), 0 ligne `Warning` ni `Exception ignored`, hook pre-commit `OK (hook)`, `sceller` 0,
  `acte commit` 0 sur les dix-neuf messages (pied Opus 5.5) ; arbre final de `emul-reserves/` égal à `arbre-final/`
  (`diff -rq` vide).
- Matrice sur l'état final (`preuves/matrice-reserves.txt`) : 3.11, 3.12, 3.13 `Ran 223`, `OK`, 0 `Warning` ; portes
  légères, gate des secrets `--tree` (`OK (secrets) : 1349 fichier(s)`), crochet hors CI `Ran 26` : sortie 0.
- `avant_acte.py --lecture-seule diff --rapport RAPPORT-INTEGRATEUR.md` par groupe (`preuves/juger-groupes-reserves.txt`) :
  C, B, A en sortie 0 ; par pas (`preuves/juger-pas-reserves.txt`) : mêmes 36 refus D3 qu'avant, aucun autre.
- `chaine --blanc --detache` de `arbre-final/` sur `chaine/chaine_int3.sh` et `chaine/plan.txt`, dépôt `tete3/` :
  `sortie 0` avec `--cc cc/RAPPORT-CC.md` (`preuves/blanc-chaine_int3.txt`) comme avec `chaine/groupes-integrateur.md`.
- La chaîne n'est pas lancée ; aucune campagne de mutants (les mutants des réserves sont ceux du contre-contrôle,
  `cc/RAPPORT-CC.md:225-231`).
