# Rapport de l intégrateur (série unique C, B, A) (transcrit)

> Transcription par l'orchestrateur le 2026-10-16 12:03:37 UTC du fichier garde-fous/int/RAPPORT-INTEGRATEUR.md ; contrôle FM-1.1 des transcripts (générateurs des groupes A, B, C, réviseurs G2 des trois groupes, intégrateur, contre-contrôleur) par le fm11.py versé : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Rapport de l'intégrateur G1 — lot INTEGRATION-P2 (GARDE-FOUS-ORCH, phase 2 : groupes C, B, A en une série)

Gate 0 : `claude-opus-5-5` (identifiant de l'environnement de l'agent). Rôle : intégrateur G1, ni générateur ni
réviseur des groupes. Brief : `BRIEF.md` de ce dossier (orchestrateur, 2026-10-16 02:34:34 UTC). Journal G1 :
`NOTES.md`. Dépôt lu en lecture seule (aucune commande git en écriture sur lui, aucun cargo) ; tout git en écriture
dans des dépôts jetables de ce dossier (`serie/`, `chaine/`, `juge/`, `verif2/`).

## 1. Base, ordre, livrables

- Tête lue à l'ouverture : `ccc29190eb8c7639405cbc1e9423d914bc1153c8` (plancher du job `controle-unittest` : 118,
  `gates.yml` l.367). Relue à 03:41:13 UTC : `50823a12733a686d1fdd456e0ac90cc750266c5a` (DT15-o à DT15-v) ; entre les
  deux, `git diff --stat` limité aux chemins de la série (`scripts/controle .claude .github/workflows/gates.yml
  docs/RENVOIS-LIGNES.tsv enforcement xtask`) ne change que `xtask/` et le registre, qui n'a aucune rangée vers un
  fichier de la série hors `lignes` à `-` : la série s'applique sur l'une comme sur l'autre. Relue à 05:22:27 UTC :
  `571b2c5b3157bcb4a42ce9836d049370d582e59c` (DT15-m : `presg5.py`, `tests/test_presg5_lineaire.py`, plancher 121,
  ajout README daté du 2026-10-16 03:55:54 UTC, deux lignes de commentaire du job) : les 24 diffs s'y appliquent
  (`chaine2/`, plancher <tête + n> avec tête = 121, ajouts README redatés au moment) ; résultats au §6.
  Relue à 05:48:37 UTC : `6a9434fb5bdd61d0eaeda48cc89eb8c05fd786e3` (PRODUIT-R2 : plancher 126,
  `tests/test_gabarit_controle.py` neuf ; aucun fichier de la série touché) : les 24 diffs s'appliquent (`chaine3/`)
  et la ligne du job au dernier pas rend `conforme (… Ran = 174)` (126 + 48), runner `153 ok, 0 échec`.
- Ordre (adjudications) : C (INT-01 à INT-07), B (INT-08 à INT-16), A (INT-17 à INT-24) ; table complète :
  `ordre.txt`. Les corrections de G2 d'un groupe forment un pas (INT-16 : C-2 à C-8 de B ; INT-24 : C-1 à C-8 de A) ;
  les corrections de la G2 de C (C-1 à C-4) ne portaient que sur le README : elles sont dans `readme/C.txt`.
- Livrables : `diffs/INT-01.diff` … `INT-24.diff` (aucun hunk sur `scripts/controle/README.md` ni sur la ligne du
  plancher ; chacun ≤ 200 lignes ajoutées, 198 au plus, INT-08 ; R-13 : 0 ; `preuves/comptes-diffs.txt`) ;
  `readme/C.txt`, `readme/B.txt`, `readme/A.txt` (un ajout daté par groupe, `<DATE>` et `<tête + n>` à remplacer au
  pas) ; `readme/C-table.diff` (voir §4, point 1) ; `planchers.tsv` (pas → tests ajoutés ; total 48) ; `ordre.txt` ;
  `SHA256SUMS`.
- Plancher final : 118 + 48 = 166, vérifié par la ligne exacte du job au dernier pas : `verdict-suite-s2 : conforme
  (code 0, résumé final, aucun saut, Ran = 166)` (`preuves/pas_a_pas2.txt`).

## 2. Pas par pas

| pas | origine | ce qui a été recalé, et pourquoi | à l'octet |
|---|---|---|---|
| INT-01 | C, P2C-1 (`p2c/g2/diffs/P2C-1-…-recale-g2.diff`) | hunks README et plancher retirés (règle 1) ; la ligne de la table (l.11) livrée à part, `readme/C-table.diff` | oui, hors README et plancher |
| INT-02 à INT-07 | C, P2C-2 à P2C-7 (série recalée de la G2 sur `520bb2a`) | hunks README et plancher retirés | oui (mêmes lignes + et −, `outils/memes_lignes.py`) |
| INT-08 | B, GFB-1 | aucun | oui |
| INT-09, INT-10 | B, GFB-2, GFB-2t | hunks README et plancher retirés | oui |
| INT-11 à INT-14 | B, GFB-3 à GFB-6 | idem | oui |
| INT-15 | B, GFB-7 | `avant_acte.py` : fin de docstring (lignes de B posées après celles de C) et constante `MOTIF_CHAINE` (après `PIECES_MAX`, constantes de C entre elles) : contextes changés par C | oui hors ces deux contextes |
| INT-16 | B, C-2 à C-8 de la G2 de B | hunks README et plancher retirés ; sept diffs en un pas (190 lignes ajoutées) | état final égal à `p2b/g2/corr` pour les huit fichiers de B |
| INT-17 | A, P2A-1 | R7 → R11 ; fins de docstring d'`avant_acte.py` et de `garde_commun.py` (lignes de A après celles de C et B) | oui hors docstrings et numéro |
| INT-18 | A, P2A-2 | R7 → R11 | oui hors numéro |
| INT-19 | A, P2A-3 | R7 → R11, `test_r7_crochet_agent` → `test_r11_crochet_agent` ; constantes `BRIEF_NOMME`, `OUTILS` après `RM` ; appel R11 après R4, avant R9 (§3, conflit 3) | mêmes lignes + et − que P2A-3 renuméroté |
| INT-20 | A, P2A-4 | `cibles` → `fc["ecrit"]` (point bloquant, §3, conflit 1) ; test `test_bash_juge_apres_la_serie` ajouté | oui hors cette ligne et le test |
| INT-21 | A, P2A-5 | aucun conflit | oui |
| INT-22 | A, P2A-6 | `lignes_ajoutees(depot, env=None, racine=None, plage=None)` (C y avait posé `racine`, A `plage`) ; `motifs(fichiers, fautes)` après les appels `workflows(…)` réécrits par C (commit et diff) | oui hors signature et docstring de `lignes_ajoutees` |
| INT-23 | A, P2A-7 | `suivi(…)` après `motifs(…)` dans `diff()` ; SKILL `shogen-avant-committer` : E12 ajouté à la liste qui porte E28 de B | oui hors cette ligne de la SKILL |
| INT-24 | A, C-1 à C-8 de la G2 de A | R7 → R11 ; `CONSIGNE_MAX` après `BRIEF_NOMME` (contexte changé par B) ; huit diffs en un pas (154 lignes ajoutées) | état final : seuls écarts au net du groupe, les résolutions ci-dessus |

Contrôles d'égalité : C, état final égal à `p2c/g2/copie` hors README (`diff -rq`) ; B, `outils/compare_net.py`
(net de `p2b/g2/tete` à `p2b/g2/corr` contre net de l'intégration) : seul écart, la ligne de fin de docstring ; A, même
outil contre le net de la base `7d9dabe` à `p2a/g2/corr`, renuméroté : seuls écarts, les résolutions du tableau.

## 3. Conflits et leur résolution

1. **P2A-4 et `cibles` (point bloquant, adjudication de B, point 3)** : GFB-2 retire la variable `cibles` de la branche
   Bash du crochet (écritures lues sur l'acte : `fc["ecrit"]`). P2A-4 posé tel quel lève `NameError`, rattrapée par
   le crochet : toute commande Bash passe sans contrôle. Recalage : `for x in fc["ecrit"]` (mêmes fichiers écrits que
   l'ancienne `cibles`, lus sur l'acte, motifs d'avant si shlex ne lit pas la commande). Test exigé :
   `test_bash_juge_apres_la_serie` (`tests/test_garde_acte.py`, classe `Serie`) : `git commit -q -m x` refusé (R3),
   `printf '5 mutants' > BRIEF-x.md` refusé (E7) puis permis quand le compte est affiché, `ls` permis sans sortie
   d'erreur. Rouge sur le crochet sans recalage : `erreur interne (NameError("name 'cibles' is not defined"))`
   (`preuves/serie-rouge-cibles.txt`), vert après (`preuves/serie-vert.txt`).
2. **Deux règles R7** : la règle « brief » du groupe A devient R11 (`outils/renum.py` sur les diffs de A : tout `R7`
   d'un diff de A désigne cette règle, A étant posé sur une base sans les règles de B) ; ses messages, sa docstring, son
   commentaire, ses tests (`test_r11_crochet_agent`) et les textes du README suivent ; table R1 à R11 dans `readme/A.txt`.
3. **Ordre R11 / R9 (conflit de sens non relevé par les G2)** : posé d'abord après R9, l'appel R11 laissait R9
   refuser le cas C-8 de la G2 de A (Workflow dont le brief est nommé hors de `prompt` : nombre d'agents illisible)
   avant que R11 juge le brief : `test_r11_crochet_agent` rouge au pas INT-24 (`preuves/pas_a_pas-v1.txt` :
   `résumé final absent`). Remis à la place du diff P2A-3 (après R4, avant R9) : vert à chaque pas.
4. **LECTURE-SEULE et `lignes_ajoutees`** : signature unique `(depot, env=None, racine=None, plage=None)` ; l'appel
   positionnel du diff (`lignes_ajoutees(a.depot, env, a.racine)`) et l'appel nommé de `pousser`
   (`plage=(base, "HEAD")`) gardent leur sens ; mutant I-4 (paramètres permutés) au §5.
5. **Textes** : fins de docstring de module (`avant_acte.py`, `garde_commun.py`) : lignes ajoutées dans l'ordre C, B, A ;
   `main()` réindenté par P2C-7 : ni B ni A ne le touchent ; `parseur()` : options de A posées sans conflit après celles
   de C ; `test_avant_acte.py` : fusion à trois (`git merge-file`) égale à l'état intégré ; SKILL
   `shogen-avant-committer` : liste des erreurs E1 … E12, E13 … E21, E28, LA-N04, LA-N05.
6. **DATE-PASSEE de C** : les trois ajouts du README se posent en fin, datés au pas (`<DATE>`), C, puis B, puis A ;
   leurs textes ne portent aucune autre heure ni aucune autre entrée datée.
7. **D3 et D4 de A** : `readme/A.txt` nomme toutes les fonctions publiques ajoutées par C, B et A ; §5, table des tests.

## 4. Points à adjuger et limites

1. `readme/C-table.diff` : P2C-1 changeait la ligne de `fm11.py` de la table de tête du README (l.11, sha256 de
   l'outil). La règle 1 du brief exclut tout hunk de README des diffs : ce hunk est livré à part (contexte l.8-14,
   indépendant de la fin du fichier), à poser avec INT-01 ; `readme/C.txt` dit la ligne mise à jour. Sans lui, la table
   garde l'ancienne empreinte de `fm11.py` (le test `test_fm11` lit sa constante, pas la table).
2. Les empreintes de `readme/C.txt` et `readme/B.txt` sont celles du dernier pas de leur groupe (INT-07, INT-16) : un
   ajout cite l'état où il est commis ; `readme/A.txt` (dernier pas) donne la table des empreintes de l'état final.
3. Les planchers sont écrits `<tête + n>` : la chaîne lit le plancher de la tête au lancement (118 à `ccc29190`).
4. Contrôle `avant_acte.py diff` sur chaque pas (diff jugé : commit du pas de la chaîne émulée, README et plancher
   compris ; dépôt jetable `juge/` à l'état d'avant le pas ; `preuves/controle_diffs.txt`, `controle_diffs-rapport.txt`) :
   (a) outil de l'état d'avant (`--lecture-seule` dès INT-08, où il existe) : sortie 0 aux 24 pas, arbre jetable
   inchangé ; (b) outil final, `--lecture-seule --rapport RAPPORT-INTEGRATEUR.md` : sortie 0 à 15 pas ; aux pas INT-02,
   03, 04, 06, 15, 17, 18, 21 et 22, seul refus D3 (fonction publique nommée par l'ajout README de son groupe, posé au
   dernier pas du groupe : conséquence de la règle 1) ; D4 : aucun refus. Par groupe (diff cumulé, ajout README
   compris, outil final, `--rapport`) : sortie 0 pour C, B et A (`preuves/controle_groupes.txt`) : D3 et D4 satisfaits
   pour toutes les fonctions publiques et tous les tests de la série. Un `diff` de l'orchestrateur sur un pas isolé,
   avec l'outil d'après INT-23, rendra ces D3 : à juger par groupe.
5. `readme/*.txt.final` sont des pièces de contrôle (dates lues à mes passages, planchers sur la tête 121) : la chaîne
   part de `readme/C.txt`, `B.txt`, `A.txt` et remplace `<DATE>` (`date -u` au pas) et `<tête + n>`.
6. Limites des groupes (items à former au versement, sans changement) : celles des rapports G2 (C : items 1 à 6 ; B :
   L-G1 à L-G8 ; A : la table des items) et des adjudications.

## 5. Mutants (rejeu sur l'état final)

- Outil : `scripts/controle/mutants.py` de la tête lue (`tete/`, sha256 `68406b966a7d…`, celui que la G2 de C a relevé),
  lancé à part de la copie mutée `mut/copie/` (archive de l'état final de `serie/`, plancher 166), job
  `controle-unittest` (runner puis suite, commande du job), borne 300 s, cinq lots détachés (`outils/campagne.sh`).
- Mutants : 94 (C : 25, B : 34, A : 29, intégration : 6), pris dans les listes des
  campagnes des trois groupes (texte avant présent une fois dans l'état final, `outils/pool.py`, R7 → R11 pour A) et
  six de l'intégration (I-1 à I-6). Résultat : témoin vivant à chaque lot (5) ; 94 tués (sortie 1), 0 vivant, 0 FATAL ;
  relevé `ps` de fin de chaque lot : aucun processus des groupes de la campagne, aucun descendant vivant
  (`mut/campagne-lot1.err` … `lot5.err`). Diffs et sorties : `mut/sortie-lot1/` … `lot5/` ; bilan : `mut/bilan.txt`.
- Sites d'appel et zones de conflit, tous tués : C-M2-8 et C-M2-9 (C4 au commit et au diff), C-M6-8 (C7 au diff),
  C-M7-5 (`workflows`, `racine`), C-M7-8 (`lignes_ajoutees`, `racine`), A-M47 (`lignes_ajoutees`, `plage`), A-M42 et
  A-M43 (`motifs` au diff et au commit), A-M52 (`suivi` au diff), A-M22 (appel R11), B-A09 et B-C05 (`biblio` dans
  `verser`), B-H31 (arrière-plan passé à l'acte), B-C02, B-C06, B-C09 ; intégration : I-1 (`fc["ecrit"]` vidé :
  `test_bash_juge_apres_la_serie` et `test_e7_comptes_du_brief`), I-2 (message R11 rendu R7), I-3 (appel R11 ôté),
  I-4 (paramètres `racine` et `plage` permutés), I-5 (actes toujours jugés par les motifs d'avant : sonde de LN-6),
  I-6 (empreinte de `garde/lignes-citees.txt` fausse).
- Équivalents déclarés : aucun dans ce rejeu (M6-5 et M7-7 de C, K16 et K19 de A, admis par les adjudications, n'y sont
  pas : textes absents de l'état final ou non choisis).

Tests ajoutés par la série et mutants tués qui les font échouer (rejeu ; règle D4) :

| pas | test | mutants tués qui le font échouer |
|---|---|---|
| INT-01 | `test_q3_session_du_scratchpad` (test_fm11) | tué par C-M1-2 |
| INT-02 | `test_l1_entree_datee_anterieure` (test_avant_acte) | tué par C-M2-9, C-M2-10, I-4, C-M2-8 |
| INT-02 | `test_l1_heure_sans_date` (test_garde_commun) | tué par C-M2-2, C-M2-1 |
| INT-02 | `test_l1_entree_datee_anterieure` (test_garde_commun) | tué par C-M2-3 |
| INT-03 | `test_l3_attribution_au_diff` (test_avant_acte) | tué par C-M3-3, C-M3-10, C-M3-1 |
| INT-04 | `test_l4_sceau_de_la_verif` (test_avant_acte) | tué par C-M4-4, C-M4-1, C-M4-2 |
| INT-04 | `test_l4_verif_versionnee` (test_gabarit_chaine) | tué par C-M4-4, C-M4-1, C-M4-2 |
| INT-05 | `test_ln1_disque_a_chaque_pas` (test_gabarit_chaine) | tué par C-M4-4, C-M5-1, C-M5-3 |
| INT-06 | `test_l13_empreintes_de_la_garde_a_jour` (test_avant_acte) | tué par I-6 |
| INT-06 | `test_l13_ligne_citee_remplacee` (test_avant_acte) | tué par C-M6-1, C-M6-8, I-4, C-M6-13 |
| INT-06 | `test_l13_empreinte_de_la_garde` (test_avant_acte) | tué par C-M6-1, C-M6-11, C-M6-4 |
| INT-07 | `test_l12_rien_n_est_ecrit` (test_avant_acte) | tué par C-M7-1, C-M7-6, C-M7-4, C-M7-8, I-4, C-M7-5 |
| INT-10 | `test_ln6_sonde_du_contre_controle` (test_garde_acte) | tué par B-H01, I-5 |
| INT-10 | `test_ln6_controle_d_une_poussee` (test_garde_acte) | tué par B-H01, I-5 |
| INT-10 | `test_vrais_refus_restent` (test_garde_acte) | tué par B-H07, B-S07, B-H35 |
| INT-10 | `test_r5_lit_le_message_et_le_fichier_de_f` (test_garde_acte) | tué par B-H07, B-G12, B-C02, B-H06, B-H01 |
| INT-10 | `test_r2_ecriture_lue_sur_l_acte` (test_garde_acte) | tué par B-H02, B-H34, B-H01, I-5 |
| INT-10 | `test_r1_effacement_lu_sur_l_acte` (test_garde_acte) | tué par B-H33, B-H01, I-5 |
| INT-10 | `test_commande_illisible_motifs` (test_garde_acte) | tué par B-H07, B-H01, I-5 |
| INT-11 | `test_e18_sleep_d_avant_plan` (test_garde_acte) | tué par B-H08, B-H31, B-K04, B-S03, B-H01 |
| INT-11 | `test_e28_motif_non_ancre_se_reconnait` (test_garde_acte) | tué par B-H10 |
| INT-12 | `test_e20_forge_sans_job` (test_garde_acte) | tué par B-H16, B-H13 |
| INT-12 | `test_e20_marqueur_du_jour` (test_garde_acte) | tué par B-H16, B-K06, B-H13 |
| INT-13 | `test_e27_workflow_de_dix_agents` (test_garde_acte) | tué par B-H21, B-H17 |
| INT-13 | `test_e27_jeton_lu_au_journal_de_la_session` (test_garde_acte) | tué par B-C06 |
| INT-13 | `test_e27_agents_vivants` (test_garde_acte) | tué par B-H18 |
| INT-14 | `test_e26_courriel_rattache_sans_releve` (test_garde_acte) | tué par B-H28, B-C09 |
| INT-14 | `test_e26_releve_puis_rattachement` (test_garde_acte) | tué par B-H26 |
| INT-14 | `test_e26_crochet_branche` (test_garde_acte) | tué par B-J01 |
| INT-15 | `test_e28_biblio_sans_rangee` (test_avant_acte) | tué par B-C05, B-A09, B-A01 |
| INT-15 | `test_e28_versement_pendant_une_chaine` (test_avant_acte) | tué par B-A06, B-A07 |
| INT-16 | `test_ln6_actes_non_litteraux` (test_garde_acte) | tué par B-H07, B-K01, B-H35, B-H01, I-5 |
| INT-16 | `test_e18_boucle_a_condition_de_sortie` (test_garde_acte) | tué par B-H08, B-H10, B-K04, B-H01 |
| INT-16 | `test_e27_fan_out_dans_une_phrase_niee` (test_garde_acte) | tué par B-H21, B-K09 |
| INT-16 | `test_e26_dossiers_lus_au_fichier` (test_garde_acte) | tué par B-K08 |
| INT-17 | `test_e6_etat_des_items` (test_garde_brief) | tué par A-M01 |
| INT-17 | `test_e6_item_ferme_cite_ouvert` (test_garde_brief) | tué par A-M07 |
| INT-17 | `test_e24_git_sans_regle` (test_garde_brief) | tué par A-M12 |
| INT-18 | `test_e22_constat_relaye_sans_reference` (test_garde_brief) | tué par A-M13, A-M16 |
| INT-18 | `test_e23_faisabilite` (test_garde_brief) | tué par A-M16 |
| INT-19 | `test_r11_crochet_agent` (test_garde_brief) | tué par A-M23, A-G02, I-3, A-M25, A-G03, A-K11, A-M22, I-2 |
| INT-20 | `test_bash_juge_apres_la_serie` (test_garde_acte) | tué par B-H07, A-M28, I-1, B-H02 |
| INT-20 | `test_e7_comptes_du_brief` (test_garde_brief) | tué par A-M28, A-M29, I-1, B-H02, A-M27, A-G04, A-K13 |
| INT-21 | `test_e12_motifs_de_dt5` (test_garde_regex) | tué par A-M34 |
| INT-21 | `test_e12_formes` (test_garde_regex) | tué par A-K17, A-M31 |
| INT-22 | `test_e12_rx_diff_commit_pousser` (test_garde_regex) | tué par A-M42, A-M47, A-M43, I-4, A-M44, A-M34 |
| INT-23 | `test_e13_readme_des_controles` (test_garde_suivi) | tué par A-G05, A-M48, I-4, A-M49, A-M52 |
| INT-23 | `test_e13_test_sans_mutant_tue` (test_garde_suivi) | tué par A-M50, A-M51, I-4, A-M52 |

## 6. Matrice et portes

- Pas à pas (`preuves/pas_a_pas2.txt`, chaîne émulée : diff, README et plancher de chaque pas) : runner du job
  `153 ok, 0 échec` et ligne exacte du job `conforme` aux 24 pas, Ran = 119, 122, 123, 125, 126, 129, 130, 130, 130,
  137, 139, 141, 144, 147, 149, 153, 156, 158, 159, 161, 163, 164, 166, 166 ; aucune ligne Warning ni Exception.
- Matrice sur l'état final (`final/`, `-X dev -W error`, `discover -s tests -t .` depuis `scripts/controle`) :
  - `python3.11 rc=0 Ran 166 tests in 46.978s OK Warning/Exception: 0`
  - `python3.12 rc=0 Ran 166 tests in 50.024s OK Warning/Exception: 0`
  - `python3.13 rc=0 Ran 166 tests in 50.626s OK Warning/Exception: 0`
- Portes légères sur l'état final (lignes de `gates.yml` et lint R-1) :
  - `python3 -B enforcement/docs-sha256sums.py . : sortie 0 : docs-sha256sums : conforme : 46 SHA256SUMS, 344 ligne(s), dont 11 absente(s) admise(s) (SHOGEN-SIM-SOMMES-1) ; 4 fichier`
  - `python3 -B enforcement/journaux-modele.py . : sortie 0 : journaux-modele : conforme (52 journaux exemptés par nom et sha256)`
  - `python3 -B enforcement/runners-epingles.py . : sortie 0 : runners-epingles : conforme (7 workflow(s), 22 clé(s) runs-on/os lues)`
  - `python3 -B enforcement/workflows-yaml.py . : sortie 0 : workflows-yaml : conforme (7 workflow(s), PyYAML 6.0.1)`
  - `bash enforcement/lint-model-pinning.sh . : sortie 0 : OK (R-1) : 12 fichier(s) ; liste blanche : claude-opus-5-5 claude-sonnet-5-5 claude-fable-5-1 claude-haiku-5-5`
- Cas hors CI du crochet (`.claude/hooks/tests/test_garde_faits.py`, TMPDIR du lot) : `Ran 26`, OK.
- Sur la tête `571b2c5b` (`chaine2/`, plancher 121 + 48 = 169) : pas à pas (`preuves/pas_a_pas2-tete571b2c5.txt`) :
  runner `153 ok, 0 échec` et ligne du job `conforme` aux 24 pas, Ran = 122 … 169, aucune ligne Warning ni
  Exception ; `avant_acte.py diff` par pas (`preuves/controle_diffs-tete571b2c5.txt`) : (a) sortie 0 aux 24 pas ; (b)
  sortie 0 à 15 pas, D3 seul aux neuf mêmes pas ; par groupe (`preuves/controle_groupes-tete571b2c5.txt`) : C, B, A
  en sortie 0 ; matrice `-X dev -W error` :
  - `python3.11 rc=0 Ran 169 tests in 48.012s OK Warning/Exception: 0`
  - `python3.12 rc=0 Ran 169 tests in 51.908s OK Warning/Exception: 0`
  - `python3.13 rc=0 Ran 169 tests in 50.140s OK Warning/Exception: 0`

## 7. Provenance

- [lu] `BRIEF.md` ; `p2c/` : `BRIEF.md`, `RAPPORT-GENERATEUR.md`, `g2/RAPPORT-G2.md`, `ADJUDICATION.md`, diffs
  `g2/diffs/` ; `p2b/` : `BRIEF.md`, `RAPPORT-GENERATEUR.md`, `g2/RAPPORT-G2.md`, `ADJUDICATION.md`, `diffs/`,
  `g2/diffs/`, `g2/corr/` (fichiers de B) ; `p2a/` : `BRIEF.md`, `RAPPORT-GENERATEUR.md`, `g2/RAPPORT-G2.md`,
  `ADJUDICATION.md`, `diffs/`, `g2/diffs/`, `g2/corr/` (fichiers de A) ; listes de mutants des campagnes des trois
  groupes (`outils/pool.py`, sources nommées dans le script) ; dépôt : `gates.yml`, `scripts/controle/` (README,
  `avant_acte.py`, `garde_commun.py`, `gabarits/chaine.sh`, `mutants.py`), `.claude/hooks/garde_faits.py`,
  `docs/RENVOIS-LIGNES.tsv` (en-tête et colonnes `cible`, `lignes`).
- Commandes et sorties : `NOTES.md` ; preuves : `preuves/` ; outils : `outils/` ; mutants : `mut/`.
- Écarts : E-1 (P2A-7 committé une fois avec des rejets dans la copie jetable, repris), E-2 (une recherche récursive
  dans des copies du scratchpad du groupe B, noms de fichiers seuls), E-3 (un `sleep 1` d'avant-plan) : `NOTES.md`.
