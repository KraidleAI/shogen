# Contre-contrôle neuf de la série intégrée (R-1 à R-4) (transcrit)

> Transcription par l'orchestrateur le 2026-10-17 07:31:23 UTC du fichier garde-fous/int3/cc/RAPPORT-CC.md ; contrôle FM-1.1 du transcript du contre-contrôleur par le fm11.py versé : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5 (324 occurrences, aucune autre). Texte ci-dessous avec 7 retouche(s) (E35, E38) : noms de marqueur de dette et locutions de la gate S-G4 cités en clair, mis en code, segments de code à doubles accents graves réécrits en segments simples, heures sans date dans les 25 caractères ou approchées mises en code ou entre guillemets français, sans autre changement (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Contre-contrôle neuf — lot INTEGRATION-P3 (GARDE-FOUS phase 3, série unique C, B, A)

Gate 0 : `claude-opus-5-5` (identifiant de l'environnement de l'agent), effort `high`, fiche `shogen-worker`. Rôle :
contre-contrôleur neuf, ni intégrateur, ni générateur, ni réviseur des groupes A, B, C. Brief : `cc/BRIEF-CC.md`
(orchestrateur, 2026-10-16 20:19:18 UTC ; sha256 `60ee301b…`). Journal G1 : `cc/NOTES.md`. Rattachement : ADR-0028,
annexe B (`docs/adr-0028/ANNEXE-B-items.md`), items ouverts l.1872 à 1880 (B.108) et 1890, 1891 (B.109), lignes relues
à la tête (`git show HEAD:…`, l.1872 SHOGEN-GARDE-RECALAGE-CHECK-1 à l.1891 SHOGEN-GARDE-ERREUR-INTERNE-1).
Dépôt lu en lecture seule : aucune écriture git, aucun cargo, aucun `--depot` sur lui ; travail dans des dépôts
jetables de `cc/` (`base`, `serie`, `groupes/`, `juge`, `outil-final`, `blanc`, `emul-depot`, `pas`, `r1`, `r3`,
`r4`, `corr`, `corr-jeu`, `mut/copie`, `mut2/`, `tmp/`).

Tête du moment : `72c2381610c88a0be2f092ed0113fa16822787e4` (lue à `20:44:42` UTC, après la fin de la chaîne
SYNC-DOCS11 ; versement : `JOURNAL.md` et annexe B après la l.1895 seulement). Copie creuse faite de `bcaab82`
(`bcaab823a26c2ad4c5780fb847b0e9eca161e299`, tête lue à `20:35:15`) : `git diff --stat bcaab82 72c2381` et
`fb30775 bcaab82` limités à `scripts/controle .claude .gitignore .github enforcement CLAUDE.md` : vides ; `fe9a72b
HEAD` sur les mêmes chemins : vide. Tête relue à 22:22:25 UTC : `8024a184b91127ce63b84794efb1cea87a1c4010` (fusion de la PR 13, SYNC-DOCS11),
`git diff --stat 72c2381 HEAD` sur ces chemins : vide. Copie : `outils/copie.py` (le mien), 1532 membres, 0 écarté, 1356 fichiers
(`git ls-files`).

## Verdict : CONFORME-AVEC-RÉSERVES (R-1 à R-4)

La série s'applique dans l'ordre sur la tête du moment, chaque pas est vert à son plancher (177 + n, ligne exacte du
job `--egal`), le README et `gates.yml` ne changent qu'aux lignes prévues, le code est celui des groupes à l'octet hors
des sept zones déclarées, et les sept résolutions sont justes. Quatre réserves, aucune bloquante pour la sûreté de la
série, chacune un diff byte-exact dans `propose/` :

| R | objet | diff | effet |
|---|---|---|---|
| R-1 | résolution (1) : une lecture pure permise sous journal illisible est consignée `permis`, non `erreur` (le sous-agent du test passait déjà par là) | `propose/R-1-erreur-journal-illisible.diff` (crochet, une ligne ; `test_refus_journal_des_passages`) | le relevé et la lecture comptent l'acte permis sans contrôle |
| R-2 | lancement : `bash <int3>/chaine/plan.sh` n'est vu ni par V7 (`MOTIF_CHAINE`) ni par `pgrep -f '^bash /tmp.*chaine_'` (règle (2) d'E37) ; aucune trace de PID ni de sortie (règle (1) d'E37) | `propose/R-2-nom-de-la-chaine.diff` (ligne de lancement du rapport de l'intégrateur : copie `chaine_int3.sh`, mêmes octets ; enveloppe PID et code de sortie) | la chaîne de la série se voit comme chaîne active |
| R-3 | mutants CC-11 et CC-12 vivants : la marque `R0` n'a aucun cas dans le relevé ni dans la lecture | `propose/R-3-cas-r0-releve-lecteur.diff` (cas seuls, `test_garde_refus.py`) | CC-11, CC-12 tués |
| R-4 | mutants CC-24 (même ligne de `piece_porte`, R12) et CC-30 (`git` nommé par son chemin, K7) vivants | `propose/R-4-cas-trois-mutants-vivants.diff` (cas seuls : `test_garde_reponse.py`, `test_avant_acte.py`, `test_lecture_seule_journal.py`) | CC-24, CC-30, CC-31b tués |

Texte du README (ajout B) pour R-1 et R-3 : `propose/R-1-R-3-readme-B.diff` (sur `readme/B.txt`). Aucune réserve
n'ajoute de méthode de test : planchers inchangés (223). R-1, R-3, R-4 s'appliquent sur l'état final et, pour R-1 et
R-3, juste après INT-12 (`git apply --check` vert ; `garde_faits.py` et `test_garde_refus.py` ne changent plus après
INT-12) : à replier dans INT-12 (README du groupe B au même pas ; empreinte de `garde_faits.py` de `readme/A.txt` à
recalculer) ou à poser en pas INT-20 (précédent : INT-25 de la phase 2, `CC R-3`), au choix de l'orchestrateur.
Copie corrigée (`cc/corr` = état final + R-1 + R-3 + R-4) : ligne du job `conforme (code 0, résumé final, aucun saut,
Ran = 223)`, matrice 3.11 à 3.13 `Ran 223`, `OK`, 0 ligne `Warning` ni `Exception ignored` (`preuves/corr-suite.txt`).

GROUPES : aucun

(Ligne lue par `chaine --cc` : chaque pas de la série est vert seul à son plancher, point 1.)

## 1. Application — CONFORME

- Chaîne émulée : `chaine/preparer.sh` de l'intégrateur copié tel quel (`cmp`) dans `cc/emu/` avec `diffs/`,
  `readme/`, `pas.tsv`, `source-pas.md`, lancé avec `DEPOT=cc/base` (jamais sur le dépôt) : `plan : 19 pas ; plancher
  de la tête 177, final 223` (`preuves/preparer-cc.txt`) ; diffs de plancher égaux à ceux de l'intégrateur, diffs du
  README égaux hors la date, messages égaux.
- Application (`outils/appliquer.sh`, `preuves/application.txt`) : 19 pas, `git apply --index --check` puis
  `--index`, commit avec le hook pre-commit du dépôt (copie, sha256 `00131872…` égal) : plancher lu au pas = attendu
  aux 19 pas (178, 179, 181, 182, 183, 183, 186, 188, 191, 194, 197, 197, 199, 200, 202, 203, 205, 216, 223) ; README :
  hunks `@@ -694,0 +695,51` (INT-06, `C.txt`), `@@ -745,0 +746,92` (INT-12, `B.txt`), `@@ -11 +11` (INT-13),
  `@@ -11 +11` et `@@ -837,0 +838,79` (INT-19, `A.txt`), aucun autre ; `gates.yml` : la ligne du plancher seule ; aucun
  chemin `xtask/` ni `docs/`. La l.11 de INT-13 et de INT-19 est celle de GF3A-1 et de C-1 de la G2 A (lignes `| fm11.py`
  comparées par sha256) ; l.11 finale : `e9c80fa1…`, égale à `sha256sum fm11.py`, à `SHA256SUMS` et à `SHA_FM11`.
- Chaîne émulée jusqu'au commit (`outils/emul-p3.sh` = `chaine/plan.sh` sans l'exécution de `verif`, seule ligne
  changée ; `verif` tirée par `source` et scellée par `sceller`, `acte commit`, hook) : 19 commits, 19 `OK (hook)`,
  `FIN`, sortie 0 (`preuves/chaine-emulee.txt`).
- Pas à pas (`outils/lourd.sh`, `preuves/pas_a_pas.txt`) : ligne exacte du job lue dans `gates.yml` de chaque pas,
  jouée sous `unshare -n`, `lo` allumée, variables de mandataire retirées (forme de la `verif`) : `conforme (code 0,
  résumé final, aucun saut, Ran = N)` à la tête (177) et aux 19 pas, 0 ligne `Warning` ni `Exception ignored` ; runner
  `verdict-suite-s2 : 153 ok, 0 échec` à la tête et au dernier pas.
- R-25 : lignes ajoutées par diff (`git apply --numstat`, `preuves/numstat.txt`) : 28 à 188 (INT-17), toutes sous 200.
  Commits entiers (diff, plancher, README) : INT-06 +119, INT-12 +137, INT-19 +253 ; précédent de la phase 2 :
  `70e3964` +239, `3b15947` +238 (même règle 1). Marqueurs de dette (motif du hook) : 0 dans `diffs/` et `readme/`.
- Plancher final recalculé : 177 + somme de `planchers.tsv` (6 + 14 + 26 = 46) = 223, égal à la ligne du job au dernier
  pas. Empreintes du tableau de `readme/A.txt` : 13 sur 13 égales sur l'état final ; `empreinte_verif()` de l'outil
  final : `e0254878d0c18fadd8ac53269891ede6a982e67fd9fb85ad9989d90f3068e976`, égale au README.

## 2. Fidélité aux sources — CONFORME

- Entrées : concaténations recalculées égales aux rapports et adjudications (C `73d9a1bf…` et `814f40c8…`, B
  `2fe76b3c…` et `d181e070…`, A `689669bf…` et `47003d95…`) ; `sha256sum -c ../SHA256SUMS` : 272 OK ;
  `arbre-final.sha256sums.txt` : 0 écart sur 1365.
- Union naïve (`outils/groupe.sh`, `outils/union.py`, `preuves/union-naive.txt`) : chaque groupe rejoué seul sur la
  copie (diffs du générateur puis de la G2) ; fichier d'un seul groupe : égal à l'octet à l'état final (21 fichiers),
  sauf `shogen-avant-lancer/SKILL.md` (point 1 de la skill, résolution 5), `test_disque_depot.py` (garde de la
  résolution 5), `test_garde_refus.py` (fixture, résolution 4 ; R0 et R12, résolutions 1 et 2) ; fichiers de plusieurs
  groupes (`git merge-file`, C puis B puis A) : `garde_faits.py` (fin de docstring, R0 du journal illisible, `REGLE[0] =
  "R12"`, `except` de `juger`), `avant_acte.py` (fin de docstring), `garde_commun.py` (fin de fichier) ;
  `test_avant_acte.py` : union égale au final. Aucun écart hors des zones déclarées : pas de résolution non déclarée.
- `arbre-final/` de l'intégrateur : égal à mon état final sur les chemins de la série, hors les trois dates du README.
- Corrections des G2 dans l'état final (`preuves/corrections-presentes.txt`) : toutes leurs lignes ajoutées présentes,
  sauf cinq lignes de C-4 du groupe C dans `test_refus_journal_des_passages` (docstring et listes recalées en INT-07 et
  INT-09 ; les cas R11 et R10 de C-4 y sont).

## 3. Les sept résolutions

1. **`R0` et `erreur` (INT-07)** — juste, avec R-1. Au regard de B-1 : la sortie est celle de B (refus, sortie 2, d'un
   acte qui écrit ; lecture pure permise) ; `R0` n'est qu'une marque du journal des refus (`garde_faits.py`, l.1123 et
   motif du journal illisible, l.742), absente de la docstring, donc des règles de `regles_du_crochet`. La table des cas
   de `readme/B.txt` (l.11 à 18) ne dit pas `R0` : elle décrit la sortie du crochet (`refus`, `permis, erreur écrite`),
   non le journal ; la marque est écrite au paragraphe l.66 à 72. Mesuré sur le crochet réel (`preuves/sonde-crochet.txt`) :
   journal illisible et `git commit` : sortie 2, `R0` ; `tool_input` en liste : 2, `R0` ; erreur interne sur `git
   commit` : 2, `R0` ; erreur interne sur `ls` : 0, `erreur`. Défaut : journal illisible et `ls` : 0, consigné
   `permis` (cas E2), alors que B-1 et son README disent `même règle` et que la lecture compte `erreur(s) interne(s),
   acte permis sans contrôle` : R-1 (le cas sous-agent `a1` du test passait déjà par ce chemin, sans journal).
2. **`REGLE[0] = "R12"` et `test_refus_lecteur` (INT-09)** — juste : sans elle, le refus R12 est consigné `R6` (mutant
   CC-04 tué) ; `R12` parmi les règles sans refus du test, lue dans la docstring.
3. **C-3 de la G2 B dans `juger` (INT-12)** — juste, à l'octet de `p3b` (union) : au premier arrêt, R6 et R12 refusent
   ensemble (sortie 2, deux lignes `REFUS`), R10 et R12 de même ; au second arrêt du même tour, passage
   (`PASSAGE R12 au second arrêt`) : le contournement des deux arrêts est fermé au premier arrêt, et la boucle reste
   bornée (`preuves/sonde-crochet.txt`, C3a à C3d). Mutants CC-05, CC-06, CC-34 tués.
4. **Fixture `sk-ant-…` en deux littéraux (INT-03)** — juste. Gate des secrets `--tree` sur l'état final : `OK
   (secrets) : 1345 fichier(s)` (`preuves/secrets-tree.txt`) ; `--history` sur ma série : `OK (secrets) : historique, 20 commit(s) (--all)`
   (`preuves/secrets-history.txt`) ; hook pre-commit rejoué sur l'index d'une copie : `OK (hook)` ; un vrai secret en
   clair indexé : `REFUS (SECRETS/forme)`, sortie 2 ; la fixture d'avant (un littéral) remise : `REFUS (SECRETS/forme)`
   sur `test_garde_refus.py:64` (`preuves/secrets-hook.txt`). Le masque reste jugé sur la valeur (mutant CC-27, masque du jeton ôté : tué). Le remède
   est celui que le hook affiche (`valeur factice : la sortir de la forme d'identifiant`). Limite de la gate, non de la
   série : un secret coupé en deux littéraux passe.
5. **Skill `shogen-avant-lancer`, point 1 (INT-11)** — juste : `--depot <dépôt> disque` (mesuré : `disque --depot .`
   sort en 3, `unrecognized arguments`) ; mutant CC-13 tué par `test_modele_de_chaine_passe_le_depot`.
6. **Fins de docstring** — justes : paragraphes dans l'ordre C, B, A (`garde_faits.py` : C, B ; `avant_acte.py` : C, B,
   A) ; fin de `garde_commun.py` : `rangees_fautives` après `motifs_du_code` (union).
7. **Commentaires datés retirés** — juste : `gates.yml` ne change qu'à la ligne du plancher ; même forme que la phase 2
   (aucun commentaire ajouté au job depuis le plancher 121) ; les planchers sont dans les ajouts du README.

## 4. Règles R1 à R12 — CONFORME

- Table de `readme/B.txt` (l.51 à 64) : crochets et actes relus contre le code (`pre_tool_use`, `juger`). Chaque règle a
  au moins un cas qui la joue (`ast` des tests : R1 6, R2 4, R3 9, R4 2, R5 9, R6 6, R7 6, R8 2, R9 4, R10 4, R11 3, R12 4
  fonctions ; R0 : 1) ; les 61 noms de tests cités au README depuis la l.655 existent tous. La table P3 ne répète pas la
  ligne `Cas de chaque règle` de la phase 2 : R1 à R11 y restent nommés (l.657 et suivantes), R12 dans son paragraphe.
- Ordre d'appel : Agent, Workflow : R4, R11 (`controler_briefs`), R9 ; Stop : R6, R10, puis R12 (l.1099 à 1110).
- Crochet réel, dix commandes (`preuves/sonde-crochet.txt`) : refusées `sleep 30` (R7), `pkill -f chaine_x` (R7),
  `git commit` sans lecture (R3), `rm -rf` d'un clone sans status (R1), `echo y > existant.txt` sans lecture (R2) ;
  permises `ls`, `git status`, `git commit` après `git diff --cached`, `until … sleep 2`, `pgrep -f '^bash
  chaine_x.sh'`. Chaque passage consigné sous sa règle ou `permis`.
- Trois réponses au Stop : `Pendant les 28 jours de collecte.` sans pièce : sortie 2, R6 et R12, consigné `R12` ;
  `La campagne S2-bis dure 16 semaines.` après le `grep -n` qui affiche la l.158 de l'ADR-0029 : 0 ; réponse de
  l'orchestrateur `La série est commise : 19 commits, plancher du job controle-unittest 223 (ligne 369 de gates.yml).`
  après lecture du plancher et du `wc -l` des commits : 0. Premier passage refait : un `uuid` commun aux réponses
  faisait passer la deuxième pour un second arrêt (`garde-faits.etat`) ; refait avec un `uuid` par réponse.

## 5. Décisions des adjudications — CONFORME

- C-1 à C-5 de C, C-1 à C-5 de B, C-1 à C-6 de A : présentes (point 2, union et lignes ajoutées).
- `.gitignore` : `scripts/controle/garde/.gitignore` l.2 (`refus.tsv`), l.3 (`refus.tsv.*.tmp`) ; `.gitignore` l.42
  (`scripts/controle/garde/lecture-seule.tsv`) : `git check-ignore -v` sur les trois, `git status` vide.
- `SHOGEN_GARDE_REFUS` : posé seulement par les tests (`tests/__init__.py` l.7, `.claude/hooks/tests/test_garde_faits.py`
  l.14, `test_garde_refus.py`) ; lu par `chemin_refus` ; absent de `.claude/settings.json` et des gabarits.
- Skill, point 1 : décision I-5 de B appliquée (résolution 5).
- `chaine-modele.sh` : `chaine/plan.sh` lui est égal (`cmp`) ; `verif` tirée par `source` de `$OUTILS/gabarits/chaine.sh`
  (l.18), aucune écrite ; K7 : `sceau_de_chaine` appelé par `blanc` ; témoin `git commit --amend` nu : `REFUS K7`,
  sortie 1. `unshare -n` : hôte root (`id -u` 0), `unshare -n true` 0 ; `lo` éteinte, allumée par l'ioctl de la
  `verif`, joignable ; réseau externe coupé (`OSError`). `chaine --blanc` de l'outil final sur `../chaine/plan.sh` et le
  plan livré, dépôt jetable de la tête : sortie 0 (et sur mon plan émulé) ; sans `--detache` : `REFUS G3 : durée
  estimée 114 min (19 pas × 6 min)` (`preuves/blanc.txt`).

## 6. D3 et D4 — CONFORME (limite écrite)

`avant_acte.py --lecture-seule diff --rapport RAPPORT-INTEGRATEUR.md` (`outils/juger.sh`) : par groupe, diff cumulé,
README et plancher compris, outil final : C, B, A en sortie 0 (`preuves/juger-groupes.txt`). Par pas : sortie 0 aux pas
INT-03, 04, 06 à 09, 12, 13, 19 ; ailleurs, seuls des `REFUS D3` (18 par outil, outil d'avant et outil final : fonction
publique ajoutée avant l'ajout README de son groupe, règle 1) ; dépôt jetable inchangé après chaque passage
(`preuves/juger-pas.txt`).

## 7. Matrice, `motifs --arbre`, lecteur — CONFORME

- État final, `-X dev -W error`, `discover -s tests -t .` (`preuves/matrice.txt`) : 3.11 `Ran 223 tests in 89.895s`, 3.12
  `72.931s`, 3.13 `71.554s`, `OK`, 0 ligne `Warning` ni `Exception ignored` ; crochet hors CI `Ran 26`, `OK`.
- `motifs --arbre` : `161 motif(s) lu(s), 25 non lu(s)`, un suspect, `scripts/controle/tests/test_garde_codeql.py:23`
  (l'ancien motif gardé exprès), sortie 1 (`preuves/motifs-arbre.txt`).
- `refus --journal` sur le journal écrit par la sonde du crochet (`preuves/refus-lecteur.txt`) : `22 ligne(s) lue(s), 0
  illisible(s) ; depuis le début : 11 refus`, R0, R1, R2, R3, R7, R12 par jour, actes, passages `11 (dont 1 erreur(s)
  interne(s)…)`. Mesure de la limite déclarée (point à adjuger 2 de l'intégrateur) : R6 et R10, qui ont refusé dans la
  sonde mais sont consignés `R12` (une ligne par passage), figurent parmi les `règles sans refus depuis trente jours
  (… candidates à relire) : R4, R5, R6, R8, R9, R10, R11` : la liste invite à relire deux règles actives.

## 8. Mutants — 35 à moi sur l'état final, 26 en zone de conflit ou site d'appel ; vivants non équivalents : R-3, R-4

Outil `scripts/controle/mutants.py` de la tête (`cc/base`, sha256 `68406b96…`, égal au dépôt), lancé à part de la copie
mutée (`cc/mut/copie`), job `controle-unittest`, borne 300 s, après la fin de la chaîne (`pgrep` vide, lancement
conditionné dans la même commande). Liste écrite par moi (`outils/liste_mutants.py`, texte avant présent une fois,
`mut/mutants.json`) ; diff et sortie de chaque mutant : `mut/sortie/` ; bilan : `preuves/mutants-bilan.txt`.
Témoin vivant ; 29 tués (sortie 1) ; 5 vivants ; 0 FATAL ; relevé de fin : `aucun processus des 70 groupes de la
campagne, aucun descendant vivant de l'outil (moissonneur)`.

| mutant | zone | mutation | classement | tests rouges |
|---|---|---|---|---|
| CC-01 | Z | `except` de `juger` : `R0` → `erreur` | tué | `test_refus_journal_des_passages` |
| CC-02 | Z | `except` : `REGLE[0] = "erreur"` ôté | tué | idem |
| CC-03 | Z | motif du journal illisible sans `R0` en tête | tué | idem |
| CC-04 | Z | `REGLE[0] = "R12"` ôté | tué | idem |
| CC-05 | Z | R10 : `code = 2` → `code = code` | tué | `test_e26_*` (3), idem |
| CC-06 | Z | R12 jugée si `code == 0` seulement (C-3 défait) | tué | `test_e29_vingt_huit_jours_sans_piece` |
| CC-07 | Z | site d'appel `acte_qui_ecrit({})` dans l'`except` | tué | `test_refus_journal_des_passages`, `test_table_des_cas` |
| CC-08 | Z | `main` : `erreur` consignée `permis` | tué | `test_refus_journal_des_passages` |
| CC-09 | Z | `main` : refus par `SystemExit` consigné `permis` | tué | idem |
| CC-10 | Z | `refuser` : `R[0-9]+` → `R[1-9][0-9]*` (R0 lu `?`) | tué | idem |
| CC-11 | Z | relevé : `R0` non compté | **vivant** | — (R-3) |
| CC-12 | Z | lecture `refus` : `R0` non compté | **vivant** | — (R-3) |
| CC-13 | Z | skill : `disque --depot <dépôt>` | tué | `test_modele_de_chaine_passe_le_depot` |
| CC-14 | Z | `chaine-modele.sh` : `acte` sans `--depot` | tué | `test_e25_lancement_lie`, `test_l4_verif_versionnee`, … |
| CC-15 | Z | `chaine-modele.sh` : contrôle du disque ôté | tué | `test_disque_et_arbre`, `test_ln1_disque_a_chaque_pas` |
| CC-16 | Z | site D3 : `nomme_en_code(nom, nom)` | tué | `test_d3_mot_commun`, `test_e13_readme_des_controles` |
| CC-17 | G | signature `nom(` → `nom( ` admise | tué | `test_d3_mot_commun` |
| CC-18 | Z | site `motifs_du_code("")` | tué | `test_motifs_arbre` |
| CC-19 | Z | site `rangees_fautives(lignes, [])` (V9) | tué | `test_e32_rangee_lue_et_ordre` |
| CC-20 | G | `rangees_fautives` ne rend rien | tué | idem |
| CC-21 | Z | `blanc` : `script(…)` non appelé (K1 à K4) | tué | `test_e34_e36_script`, `test_k4_apostrophes_et_formes` |
| CC-22 | Z | site `journal_lecture_seule` : refus écrit `conforme` | tué | `test_passages_journalises` |
| CC-23 | Z | site `regles_du_crochet(GC.__file__)` | tué | `test_refus_lecteur` |
| CC-24 | G | `piece_porte(…, pieces)` : nombre et unité sur deux lignes | **vivant** | — (R-4) |
| CC-25 | G | R12 : un refus du crochet relayé compte comme pièce | tué | `test_unite_et_fenetre` |
| CC-26 | G | `lecture_pure` : `sh` admis | tué | `test_table_des_cas` |
| CC-27 | Z | masque du jeton ôté (fixture de la résolution 4) | tué | `test_refus_journal_des_passages` |
| CC-28 | G | K4 hors fonction sans `litteraux_otes` | tué | `test_k4_apostrophes_et_formes` |
| CC-29 | G | `rang` : une lettre seule | tué | `test_plage_a_bornes_en_lettres` |
| CC-30 | G | K7 : `/usr/bin/git commit` non compté | **vivant** | — (R-4) |
| CC-31 | Z | `garde/.gitignore` : `refus.tsv.*.tmp` → `refus.tsv.tmp` | vivant, **équivalent** | `*.tmp` de `.gitignore` l.28 l'ignore déjà (`git check-ignore -v`) |
| CC-32 | G | `lieux_disque` : TMPDIR ajouté s'il est du même système | tué | `test_disque_du_depot`, `test_tmpdir_sur_un_autre_systeme` |
| CC-33 | Z | R12 jugée au SubagentStop | tué | `test_unite_et_fenetre` |
| CC-34 | Z | Stop : `REGLE[0] = "R10"` au lieu de `R6` | tué | `test_refus_journal_des_passages` |
| CC-31b | Z | `garde/.gitignore` : ligne `refus.tsv` ôtée (campagne à part, `mut2/campagne-finale.txt`) | **vivant** | — (R-4) |

Mutant de plus sur l'état final (`mut2/campagne-finale.txt`, `preuves/mutants-final2-bilan.txt`) : CC-31b (ligne
`refus.tsv` ôtée de `garde/.gitignore`) : témoin vivant, CC-31b **vivant** (R-4) ; relevé de fin vide (4 groupes). En
tout 35 mutants sur l'état final : 29 tués, 1 vivant équivalent (CC-31), 5 vivants non équivalents (CC-11, CC-12, CC-24,
CC-30, CC-31b), tous couverts par R-3 et R-4.

Copie corrigée (`cc/corr` = état final + R-1 + R-3 + R-4 ; mêmes outil, job et borne ; `mut2/`,
`preuves/mutants-corr-bilan.txt`) : témoin vivant ; CC-11 et CC-12 tués (`test_refus_releve_premier_message`,
`test_refus_lecteur`), CC-R1 (ligne de R-1 ôtée) tué (`test_refus_journal_des_passages`), CC-24 tué
(`test_unite_et_fenetre`), CC-30 tué (`test_k7_chaque_commit_garde`), CC-31b tué (`test_journal_ignore_par_git`) ;
0 FATAL ; relevé de fin : `aucun processus des 14 groupes de la campagne, aucun descendant vivant de l'outil
(moissonneur)`. `avant_acte.py --lecture-seule diff --rapport RAPPORT-CC.md` des diffs R-1, R-3, R-4 sur l'état
final : sortie 0 chacun (`preuves/juger-reserves.txt`).

## 9. Écarts de l'intégrateur — CONFORME (limites)

- E-1 (attente active d'environ une minute, `kill` du PID de sa propre boucle), E-2 (`pkill -f` non ancré refusé par
  R7), E-3 (`git checkout -- <chemin>` dans un clone jetable) : consignés dans `../NOTES.md`, sans effet sur le dépôt.
  Dépôt : `git status --porcelain` limité à `scripts .claude enforcement .github .gitignore CLAUDE.md JOURNAL.md` :
  vide ; `.git/shogen-garde/journal.tsv` du dépôt entre `17:52` et `20:19` UTC : six lignes `brief` (crochet R11 des
  lancements de l'orchestrateur), aucune `chaine` ni `diff` : aucun passage `--depot` de l'intégrateur sur le dépôt.
- Pièces interdites : `arbre-final.sha256sums.txt` (1365 chemins) : 0 chemin sous un préfixe interdit, 0 `*.jsonl` ;
  `SHA256SUMS` : 0 `jsonl` ; copies faites par `git archive` à pathspec d'exclusion (`outils/copie.py`, 0 écarté). Ce
  qu'il a ouvert ne se vérifie que par son journal (limite).
- E37 : la campagne de l'intégrateur (`18:46` à `19:56` UTC, `../NOTES.md`) a tourné pendant la chaîne SYNC-DOCS11 ; la
  règle (2) d'E37 (aucune campagne pendant une chaîne) est datée de `19:55:54`, postérieure à son brief ; la cause de la
  disparition de la chaîne n'est pas établie (E37) ; son `kill` visait le PID de sa propre boucle (`../NOTES.md`).

## Points à adjuger de l'intégrateur (section 7), avis

1. Marque `R0` : juste ; avec R-1 (journal illisible et lecture : `erreur`) et R-3 (cas du relevé et de la lecture).
2. Une ligne par passage : limite vraie et mesurée (point 7 : R6 et R10 listées sans refus) ; item
   SHOGEN-GARDE-REFUS-DOUBLE-1 à former, sa lecture trompe la relecture des règles.
3. Commentaires datés retirés : juste (précédent de la phase 2).
4. Fixture en deux littéraux : juste (point 3, résolution 4).
5. Dates du README à la préparation : admissible ; item SHOGEN-CHAINE-MODELE-README-1 juste.
6. Messages : formes vérifiées par `acte commit` à chaque pas (chaîne émulée, sortie 0).
7. Rapport du contre-contrôle : ce rapport porte la ligne `GROUPES : aucun` ; `CC=<int3>/cc/RAPPORT-CC.md`.
8. Forme `--depot <dépôt> disque` : juste (mesurée).
9. D3 par pas : limite de la règle 1 ; D3 et D4 satisfaits par groupe.

## Observations et items à former (règle PAROXYSME)

| item proposé | constat | prix |
|---|---|---|
| SHOGEN-GARDE-R12-ERREUR-APRES-REFUS-1 | depuis C-3 de la G2 B, R12 est jugée après un refus R6 ou R10 ; une erreur interne de R12 lève alors ce refus : mesuré par un double de `nombres_sans_piece`, R6 sur `123` : sortie 2 seule, 0 avec l'erreur (`preuves/sonde-r12-erreur-apres-r6.txt`) | garder le refus déjà posé quand R12 lève (sens sûr), un cas |
| SHOGEN-CHAINE-MODELE-TRAP-EXIT-1 | `chaine-modele.sh` n'écrit ni son PID ni une ligne `trap EXIT` (règle (1) d'E37) ; R-2 l'enveloppe au lancement pour cette série seulement | ligne PID et `trap … EXIT` au modèle, jugées par `chaine --blanc` |
| SHOGEN-GARDE-JOURNAL-ILLISIBLE-DECISIONS-1 | journal illisible et lecture pure : rien au journal des décisions (`garde-faits.log`), alors que l'ajout B écrit `l'erreur écrite sur stderr et au journal` | une ligne `ERREUR` au journal des décisions, comme l'erreur interne |
| SHOGEN-CHAINE-NOM-1 | aucun outil n'exige qu'une chaîne porte un nom que V7 et la règle (2) d'E37 reconnaissent (R-2) | `chaine --blanc` refuse un `--script` hors de `MOTIF_CHAINE` |

Observations sans item : la skill dit `jamais /` (le dépôt peut être sur `/`, il est alors mesuré) ; `readme/C.txt`
dit encore `R1` à `R11` (l.21), corrigé par l'ajout B ; la borne `timeout 13680` du lancement vaut 12 min par pas pour 19
pas (un pas INT-20 la porterait à 20 pas).

## Provenance (G1)

- [lu] en entier : `cc/BRIEF-CC.md`, `../BRIEF.md`, `../RAPPORT-INTEGRATEUR.md`, `../NOTES.md`, `../ordre.txt`,
  `../planchers.tsv`, `../readme/C.txt`, `B.txt`, `A.txt`, `../chaine/preparer.sh`, `pas.tsv`, `plan.txt`,
  `groupes-integrateur.md`, `plan.sh` (= `chaine-modele.sh`), un message ; `../diffs/INT-07.diff` en entier, les autres
  par leurs hunks, leur `numstat` et la comparaison à l'octet aux sources (point 2) ; `../SHA256SUMS` (contrôlé) ;
  adjudications `p3a`, `p3b`, `p3c` ; rapports G2 des trois groupes ; `ERREURS-ORCHESTRATEUR.md` E29 à E37 ; annexe B
  l.1872 à 1880, 1890, 1891 (`git show HEAD:`). Sur l'état final : `garde_faits.py` (docstring, `refuser`, `consigner`,
  `releve_refus`, `pre_tool_use`, `stop`, R12, `lecture_pure`, `acte_qui_ecrit`, `main`, `juger`, `soumission`),
  `avant_acte.py` (`regles_du_crochet`, `refus`, `nomme_en_code`, `suivi`, `rang`, `nommes`, `lieux_disque`, `disque`,
  `litteraux_otes`, `commits_nus`, `sceau_de_chaine`, `blanc`, `chaine`, `journal_lecture_seule`, `main`), `chaine.sh`
  (`verif`), `chaine-modele.sh`, skill `shogen-avant-lancer`, tests touchés, `mutants.py` (docstring), hook
  pre-commit du dépôt. Aucune source [abs] ni [2nd].
- Commandes et sorties : `cc/NOTES.md` ; outils : `cc/outils/` ; preuves : `cc/preuves/` ; mutants : `cc/mut/`,
  `cc/mut2/`. Chiffres recomptés par outil (`sha256sum`, `git apply --numstat`, suites, campagnes, `grep -c`).
- Aucune pièce interdite ouverte, aucun `*.jsonl` lu ni créé, aucun réseau, aucun cargo, `SHOGEN_S2_CAMPAGNE_CONTROL`
  jamais posée (`outils/env.sh` la retire) ; aucune écriture dans le dépôt ni dans les livrables de l'intégrateur.
- Écarts (détail dans `cc/NOTES.md`) : E-1 `grep -rn` sur ma copie entière (`docs/` de la copie compris, interdits
  absents) ; E-2 `sleep 1` d'avant-plan refusé par R7, rien n'a tourné ; E-3 `lourd.sh` lancé pendant une chaîne
  redémarrée, sorti en erreur à sa l.13 avant tout travail lourd ; E-4 `pgrep -f` non ancré refusé par R7 ; E-5 `git
  checkout --` d'un chemin modifié dans ma copie jetable `cc/serie`.
