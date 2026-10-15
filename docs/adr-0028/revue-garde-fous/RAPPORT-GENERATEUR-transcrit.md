# Rapport du générateur de GARDE-FOUS-ORCH phase 1 (GF-0 à GF-10b) (transcrit)

> Transcription par l'orchestrateur le 2026-10-15 20:10:04 UTC du fichier garde-fous/gf1/RAPPORT-GENERATEUR.md ; contrôle FM-1.1 des transcripts du générateur, du réviseur G2 et du contre-contrôleur, par le fm11.py versé et par celui de DT3-E : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Rapport du générateur G1, lot GARDE-FOUS-ORCH, phase 1

Écrit le 2026-10-10 07:38:24 UTC (heure lue par `date -u` au moment de l'écriture, par script). Worker `shogen-worker`, générateur G1.
**Gate 0 : modèle résolu `claude-opus-5-5`** (identifiant exact déclaré par l'environnement de l'agent), effort max.
Brief `BRIEF-GF1.md` (sha256 `12c3673e…52bc3cd`). Rattachement : adjudication de l'orchestrateur du 2026-10-10
(`ADJUDICATION.md`, sha256 `79c53696…`), avis adopté (`AVIS.md`, `8335b4ce…`), proposition (`PROPOSITION.md`,
`eb4054d8…`), liste des erreurs (`ERREURS-ORCHESTRATEUR.md`, `042f1507…` puis, après le message de l'orchestrateur de
06:51 UTC, `cb941153…`, E22 à E25). Base de départ `dda4bbcc2b0f480eb0c39d7891237e0e3d2b0918` ; la série s'applique aussi,
contrôlée, sur `85751864…` et sur la tête `2fcd30369e3c0bcdf2e3c80a197a4e09d713eb18` (07:30:58 UTC). Aucune écriture
dans le dépôt du projet ; aucun commit, aucune poussée, aucun réseau ; `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée.
GF-20 (bloc commun) : brouillon seul, `bloc-commun-brouillon.md`, en attente du signal.

## 1. Diffs, dans l'ordre de la chaîne

| diff | contenu | lignes ajoutées | tests (fichier : total) | plancher | mutants tués / équivalents | sha256 |
|---|---|---|---|---|---|---|
| GF-0 | ajout daté en fin de `docs/adr-0028/G0-lots-DETTES.md` : rattachement, phase 1, conditions de la phase 2 | 23 | — | 37 | — | `722c6d8f…` |
| GF-1 | `garde_commun.py` : horloge par `date -u`, heures futures et approchées | 108 | garde_commun : 6 | 43 | 14 / 0 | `d01ad1a9…` |
| GF-4 | interdits (liste lue, D.2 par `fm11.py`), racines, `analyser_diff`, disque | 171 | garde_commun : 11 | 48 | 15 / 0 | `2db1f861…` |
| GF-2 | `presg5.py` versé à l'octet, sortie dorée | 197 | presg5 : 1 | 49 | 12 / 0 | `55fda7f6…` |
| GF-2b | `presg5.py` outil : sorties 0, 1, 3, interdits jamais ouverts | 125 | presg5 : 5 | 53 | 10 / 0 | `b0e5c654…` |
| GF-3 | citations : forme stricte refusée si fausse, autres formes en avertissement | 121 | garde_commun : 14 | 56 | 15 / 0 | `4ba39e61…` |
| GF-4b | `lignes_ajoutees` de l'index (git), aide `tests/aide_garde.py` | 81 | garde_commun : 15 | 57 | 8 / 1 | `775f9f90…` |
| GF-5 | `avant_acte.py` : contrat 0/1/3, journal avec `contourne`, `sceller` | 198 | avant_acte : 3 | 60 | 13 / 1 | `d71b6dff…` |
| GF-5b | `commit` C1 (sceau), C2 (`Source-Sha:`), C3 (mots du message) | 140 | avant_acte : 6 | 63 | 13 / 0 | `e85a2e48…` |
| GF-6 | `commit` C4, C5, C6, C7 (`garde/lignes-citees.txt`), C9 | 192 | avant_acte : 10 | 67 | 14 / 0 | `8d5d3e0f…` |
| GF-6b | C8 (lecture YAML déléguée), `diff --fichier` (D1, D2, C4, C5, G5, C7, C8) | 135 | avant_acte : 13 | 70 | 12 / 0 | `b7f59e3b…` |
| GF-7 | `verser` (V0, V2, V3, V4, C4, C5, G5) | 120 | avant_acte : 15 | 72 | 11 / 0 | `59e6e163…` |
| GF-8 | `pousser` (P1, P2, C8, P4 `--acte`), `publier`, `garde/hors-distant.txt` | 134 | avant_acte : 18 | 75 | 12 / 0 | `eb2dc17f…` |
| GF-8b | `existe`, `disque [--min-go] [--lister]` | 99 | avant_acte : 20 | 77 | 11 / 0 | `c61be661…` |
| GF-9 | modèle `gabarits/chaine.sh` | 157 | gabarit_chaine : 5 | 82 | 10 / 0 | `9d736107…` |
| GF-9b | `chaine` (G1, G2 ligne `GROUPES :`, G3 durée, E25), `gabarits/rapport-cc.md` | 127 | avant_acte : 22 ; chaine : 7 | 86 | 14 / 0 | `695938b9…` |
| GF-10 | quatre skills `.claude/skills/shogen-avant-*`, `parseur()` | 158 | skills : 2 | 88 | 9 / 0 | `9069cf7f…` |
| GF-10b | toute exception en 3, jamais en 1 | 23 | avant_acte : 23 | 89 | 7 / 1 | `d6604137…` |

Total : 2 309 lignes ajoutées, 18 diffs, chacun sous 200 (R-25), vert seul (ligne exacte du job `controle-unittest`,
`--egal`, plancher recalé en place : aucune ligne de `gates.yml` déplacée), un ajout daté en fin de
`scripts/controle/README.md` par diff de code (sha256 de l'outil, heure de `date -u` lue par le script d'écriture).
Comptes de tests de chaque ajout daté recomptés contre les arbres (un écart trouvé et corrigé : E-15).

## 2. Ordre et découpes

Ordre : celui des dépendances, chaque diff vert seul ; G0 d'abord ; les interdits (GF-4) avant le premier outil qui
ouvre un fichier (`presg5.py`, citations) ; `avant_acte.py` avant ses sous-commandes ; le modèle de chaîne après
`sceller`, `commit`, `disque` ; les skills en dernier (ils citent des commandes qui existent). L'ordre (d) de l'avis
fixe le contenu de la phase 1 et l'arrêt après elle ; toute la phase part dans une seule chaîne. Découpes pour R-25,
chacune déclarée : GF-2 et GF-2b (versement à l'octet, puis outil) ; GF-4 et GF-4b (partie git des lignes ajoutées et
aide des tests, placée après GF-3 pour ne pas refaire GF-2 à GF-3) ; GF-5 et GF-5b ; GF-8 et GF-8b ; C8 passé de GF-6
à GF-6b, qui le partage avec `diff` ; GF-10b ajouté après relecture de mon code.

## 3. Erreur, contrôle, test rouge (cas réel reproduit)

| erreur (classe) | contrôle | test rouge tiré de l'erreur |
|---|---|---|
| E1 `gates.yml` illisible (K-8, K-13) | C8 : `enforcement/workflows-yaml.py` du dépôt sur les workflows de l'index (`commit`), de HEAD plus le diff (`diff`), de HEAD (`pousser`) | `test_e1_commit`, `test_e1_interdit_tete`, `test_la_n05_et_hors_distant` (lecteur factice en refus, absent : 3) |
| E2 commentaire public faux (K-14) | `publier` : parties vérifiables seulement (heures, citations, secrets, chemins) | `test_e14_publier` ; la cause fausse elle-même passe (L-10) |
| E3 chaîne tuée à 30 min (K-3) | modèle de chaîne : lancement détaché avec délai ; G3 | `test_e25_lancement_lie`, `test_e25_duree` |
| E4 disque presque plein (K-4) | `etat_disque` (refus sous 3 Gio, avertissement sous 6), `disque`, `disque --lister`, contrôle au départ de la chaîne | `test_e4_seuils` (222 Mio), `test_e4_disque`, `test_disque_et_arbre` |
| E5 cible cargo hors de la copie (K-13, K-1) | `verif` du modèle : `cargo --locked test -p xtask` à la cible par défaut ; ligne I-1 du bloc commun si DETTES-T7 ne la porte pas | `test_modele` (présence) ; règle |
| E8 « trois passes » (K-9) | C2 `Source-Sha:` (source retouchée après le message : refus) ; C3 (verdicts, passes, identifiants, sha courts) | `test_e8_source_sha`, `test_e8_mots_du_message`, `test_e8_message_perime` |
| E9 messages d'outils anglais entre guillemets (K-10) | `presg5.py` (0, 1, 3) ; G5 dans `diff` et `verser` | `test_e9_message_d_outil`, `test_e21_e14_e16_e9`, `test_e9_e10` |
| E10 adjudication versée en double (K-10) | `verser` V2 (même sha256 ; pièce de 500 caractères ou plus contenue dans une autre) | `test_e9_e10` |
| E11 chaîne au rouge sur FZ-x seul (K-6) | ligne fixe `GROUPES :` du rapport de contre-contrôle ; `chaine` G1, G2 ; appel par le modèle avant tout pas | `test_e11_groupe_coupe` (FZ-x+FZ-i), `test_e11_groupe` |
| E14 heures de mémoire (K-16) | `horodatages_fautifs` (tolérance 120 s), C4 au commit, au diff, au versement, à la publication | `test_e14_heures_futures` (04:18 et 04:22 écrits à 04:14), `test_e14_e16_lignes_ajoutees`, `test_e21_e14_e16_e9`, `test_e14_publier` |
| E15 absence affirmée (K-17) | `existe` | `test_e15_existe` (WISHLIST.md à la racine) |
| E16 citation inexacte du JOURNAL (K-17) | `citations` : forme stricte refusée ; forme de E16 `(JOURNAL l.143)` en avertissement compté (adjudication) | `test_e16_forme_stricte_refusee` |
| E17 écritures refusées par le mandataire (K-15) | `pousser --acte` (P4), lignes `acte` de `garde/hors-distant.txt` | `test_e17_actes_refuses` |
| E19 gestes hors du dossier, listes du dépôt (K-2) | interdits lus par tous les outils, jamais nommés ; `racine_dangereuse` ; bloc commun | `test_e19_copies_et_formes`, `test_racines` ; les commandes des agents : phase 2 |
| E21 renvois décalés (K-11) | C7 au `commit` et au `diff` (aucun bloc ne décale une ligne existante d'un fichier cité ; `Décalage admis : <chemin>` journalisé en contournement) | `test_e21_fichier_cite`, `test_e21_e14_e16_e9` |
| E24 noms d'interdits imprimés (K-2) | aucun outil n'affiche un chemin interdit (V0, D1, X1, `presg5`, `lignes_ajoutees`) ; règle au brouillon du bloc commun | `test_lignes_ajoutees_sans_interdit`, `test_e1_interdit_tete`, `test_sommes_chemins_heures`, `test_e15_existe` ; le brief : phase 3 |
| E25 chaîne de 126 min en tâche liée (K-3) | G3 de `chaine` (pas × durée mesurée, 6 min par défaut ; au-delà de 100 min, lancement lié refusé, lancement détaché donné) ; `DETACHE`, `DUREE_PAS` du modèle | `test_e25_duree` (23 commits : 138 min), `test_e25_lancement_lie` |
| LA-N01 poussée de ce qui ne part pas (K-14) | `pousser` P2 (ADR-0028 l.293 : docs 15/16) | `test_la_n05_et_hors_distant` |
| LA-N03 sha court faux (K-9) | C3 (sha absent des sources et inconnu de git) | `test_e8_mots_du_message` |
| LA-N04 index plus large que les diffs (K-6) | C6 | `test_la_n04_diffs_nommes` |
| LA-N05 commit ou poussée sans vert (K-8) | `sceller` après la vérification, C1, P1 ; le modèle scelle après `verif` | `test_la_n05_sceau_du_contenu_verifie`, `test_la_n05_commit_sans_sceau`, `test_rouge_au_second_pas` |
| LA-N08 lecture d'un interdit (K-2) | `chemin_interdit` ; citation d'un interdit refusée sans ouverture | `test_citations_fausses` (le chemin est un dossier : rien n'est ouvert) |

Sans contrôle mécanique en phase 1 : E6, E7, E12 (`redos.py` réduit ou retiré, phase 3), E13 (compte du README), E18,
E20, E22, E23 (L-10).

## 4. Mutants

17 diffs de code : 203 mutants, 200 tués par la ligne exacte du job `controle-unittest` (sortie 1 du vérificateur,
test en échec nommé au journal du banc), 3 équivalents déclarés : M4b-2 (`git diff --cached` compare déjà à HEAD),
M5-11 (témoin du banc : chemin inutile dans `sys.path`), M10b-7 (`BaseException` : aucune interruption dans les cas) ;
0 FATAL. Banc : `gf1/outils/mutants.py` (groupe de processus, `killpg` au délai, sans variables de mandataire, base
verte exigée avant le premier mutant, fichier restauré et relu par sha256, relevé des processus sous la copie). Mutants
d'abord vivants puis tués après renforcement du test : M2b-4, M4b-5, M5b-9, M7-1, M8-8, M9-1, M9-3, M9-9, M9b-1,
M10-2, M10-9, M10b-4. Journaux : `gf1/mutants/*.log`.

## 5. Vérifications

- Suite de `scripts/controle` sous 3.10, 3.11, 3.12, 3.13 en `-X dev -W error -B` : 89 tests OK ; aucun `.pyc`.
- Lignes exactes de `gates.yml`, sous `isole.sh`, sans mandataire : runner 137 ok ; S2 Ran = 419 ; s2bis Ran = 355 ;
  sim-bis Ran = 279 ; calib-actifs Ran = 65 ; controle Ran = 89 ; runners-epingles, cas et lecture YAML,
  journaux-modele, docs-sha256sums, cas du lint R-1 (227 ok), lint R-1 (11 fichiers), marqueurs de dette : tous
  conformes, sur `2fcd303` plus la série (et sur `8575186` plus 17 diffs, et sur `dda4bbc` plus 17 diffs, sauf sim-bis
  sans historique, refait avec l'historique en lecture seule).
- `cargo --locked xtask verify` (lignes VERDICT seules) : 8 portes VERT, S-G9 ROUGE (1 violation) ; même motif, aux
  mêmes numéros de ligne, sur la copie creuse de la base sans la série (`dda4bbc`, `8575186`) : rouge préexistant de la
  copie creuse (Q-12).
- Le lot sur lui-même : `avant_acte.py diff` sur chacun des 18 diffs, dans l'ordre, sur un dépôt jetable de la tête du
  moment : sortie 0 partout, aucun avertissement ; aucune heure écrite de mémoire (heures des ajouts datés lues par
  script) ; aucun ajout ne décale une ligne d'un fichier cité ; aucun message d'outil entre guillemets français dans
  les textes livrés.

## 6. Questions

| n° | question | recommandation |
|---|---|---|
| Q-1 | Découpes pour R-25 (GF-2b, GF-4b, GF-5b, GF-8b, GF-10b) et déplacements (partie git des lignes ajoutées, C8). | Les accepter : chaque diff est vert seul et sous 200 lignes. |
| Q-2 | Interdits lus dans `INTERDITS` de `enforcement/docs-sha256sums.py` et `motifs` de `fm11.py`, sans `garde/interdits.txt`. | Accepter (une seule source, déjà liée à `sg5.rs` par un cas) ; un fichier de données ferait une quatrième copie. |
| Q-3 | Un motif de D.2 paraît dans le composant de session du chemin du scratchpad ; les motifs sont jugés sous le dernier composant `scratchpad`. | Accepter ; revoir ce motif de `fm11.py` dans un lot à part. |
| Q-4 | Ligne source de la liste hors-distant : l.293 d'ADR-0028 à `dda4bbc` (la proposition écrivait l.291) ; entrée « suppression de branche » prise de E17 [2nd]. | Confirmer la transcription ; confirmer l'entrée sur la réponse du mandataire versée (`docs/adr-0028/forge-pr11/`). |
| Q-5 | `diff` et `commit` écrivent des objets git et le journal dans le dépôt lu : un sous-agent en lecture seule ne peut lancer `diff` sur le dépôt du projet. | Ligne du bloc commun : dépôt jetable dont la tête est la base du diff ; mode de lecture seule en phase 2. |
| Q-6 | GF-20 : deux lignes (I-1, messages d'outils en code) dépendent de ce que DETTES-T7 pose. | Les retirer du bloc si DETTES-T7 les porte ; poser le bloc sur la tête qui porte DETTES-T7. |
| Q-7 | Outil `Skill` dans la fiche orchestrateur (Q-21 de la proposition) : non touché. | Décider après DETTES-T7, et seulement si l'orchestrateur tourne sous cette fiche. |
| Q-8 | C4 ne juge que le message et les lignes ajoutées des `.md` (les `.py` d'essai portent des heures). | Accepter. |
| Q-9 | Le job sim-bis exige l'historique (`f35a70c`, `f458980`) : une copie par `git archive` échoue. | Écrire dans la procédure des copies G2 et CC : `objects/info/alternates` vers les objets du dépôt (lecture seule). |
| Q-10 | `garde/lignes-citees.txt` : `G0-lots-DETTES.md` et `.claude/agents/*.md` ajoutés à la liste de Q-10 ; `gates.yml` non inscrit faute de preuve. | Confirmer la liste. |
| Q-11 | E22, E23 et le volet brief de E24 (ajoutés après l'adjudication) sans contrôle en phase 1. | Former les items ; E24 dans le contrôle `brief` de la phase 3. |
| Q-12 | S-G9 ROUGE sur la copie creuse, avec et sans la série (sortie brute non lue). | Le confirmer VERT sur l'arbre complet à la vérification de la chaîne (verdict global seul). |
| Q-13 | Le journal `journal.tsv` est local à chaque copie. | Relever celui du dépôt de l'orchestrateur à chaque versement, pour la décision de phase 2 (avis b.5). |

## 7. Limites, à former en items (règle PAROXYSME)

- L-1 Une heure sans sa date, ou une heure passée fausse, n'est pas vue (SHOGEN-GARDE-DATE-PASSEE-1).
- L-2 Seule la forme stricte de citation est refusée ; la forme de E16 donne un avertissement ; une citation sans
  référence n'est pas vue.
- L-3 C3 contrôle la présence des mots dans les sources, pas leur attribution au bon diff (SHOGEN-GARDE-ATTRIBUTION-DIFF-1).
- L-4 Le sceau prouve que la vérification s'est terminée sans erreur, pas ce qu'elle contient (SHOGEN-GARDE-VERIF-VERSIONNEE-1).
- L-5 Les outils lisent en mémoire des noms de chemins (`git status`, `diff --name-only`, `ls-files`) sans jamais
  afficher un interdit ; les commandes des agents (E19, E24) ne se contrôlent qu'avec le crochet de la phase 2.
- L-6 `pousser` P2 compare à la référence distante locale, sans `fetch` (acte réseau de l'orchestrateur).
- L-7 `pousser --acte` lit des motifs sur le texte de la commande : une autre écriture de la même requête passe.
- L-8 `presg5.py` approche S-G5 (sans `WISHLIST.md` ni régime partiel) ; `xtask` reste le juge.
- L-9 `verif` du modèle de chaîne est générique, à relire par lot ; un arrêt laisse le pas appliqué à l'index.
- L-10 E2 (cause fausse), E6, E7, E12, E13, E18, E20, E22, E23 sans contrôle mécanique en phase 1.
- L-11 G3 dépend de la durée déclarée d'un pas (`--duree-pas`, 6 min par défaut) et de `DETACHE`.
- L-12 `diff` et `commit` écrivent dans le dépôt lu (objets git, journal) (Q-5).
- L-13 C7 ne voit que les décalages : un remplacement à nombre égal de lignes change une ligne citée sans refus.

## 8. Mesure contre l'estimation de la proposition

| proposition (§7) | estimé | mesuré |
|---|---|---|
| GF-1 | 160 | 108 |
| GF-2 | 195 | 322 (GF-2 + GF-2b) |
| GF-3 | 190 | 121 |
| GF-4 | 195 | 252 (GF-4 + GF-4b) |
| GF-5 | 200 | 338 (GF-5 + GF-5b) |
| GF-6 | 195 | 192 (sans C8) |
| GF-7 | 190 | 120 |
| GF-8 | 198 | 233 (GF-8 + GF-8b) |
| GF-9 | 140 | 157 |
| GF-10 | 195 | 158 |
| total comparable | 1 858 | 2 001 (×1,08) |
| hors estimation | — | GF-0 23, GF-6b 135 (C8 compris), GF-9b 127 (E25 compris), GF-10b 23 |
| total de la phase 1 | 1 858 | 2 309 (×1,24 ; borne haute de la proposition ×2 à ×3) |

Tests : 37 → 89 (+52 ; estimé +39). Mutants : 203 (prévus 45 pour ces outils). Diffs : 18 (prévus 10, plus GF-6b et
GF-9b ajoutés par l'adjudication).

## 9. Écarts

- E-1 `git archive HEAD | wc -c` lancé sans exclusions : le contenu des interdits a traversé un tube vers `wc`, sans
  affichage ; non refait.
- E-2, E-3, E-4, E-6, E-9 Découpes et déplacements pour R-25 (§2) ; GF-4b placé après GF-3 (E-14).
- E-5 Une campagne de mutants de GF-6 a tourné sur une base rouge : invalide, refaite ; le banc exige désormais une
  base verte.
- E-7 Dépôts jetables du scratchpad avec un commit de base puis un commit par diff (`gf1/verif`), pour donner une tête
  à `avant_acte.py diff` ; `objects/info/alternates` vers les objets du projet, en lecture, pour sim-bis ; jamais le
  dépôt du projet.
- E-8 Le mutant M8b-10 a parcouru `/` à profondeur 4 pendant sa campagne (noms et tailles seulement, rien d'ouvert,
  sortie captée) ; le test prend désormais des racines petites.
- E-10 Le modèle de chaîne a été écrit avant son test ; le rouge a été montré sur un modèle bouchon.
- E-11 Pour comprendre un faux refus, j'ai imprimé l'indice d'un motif de D.2 et la position du composant de chemin où
  il paraît (le composant de session), jamais le motif.
- E-12 Une commande qui rétablissait la base dans la copie a été arrêtée par le contrôle de sûreté du harnais (rien
  n'a été lancé) ; comparaison refaite sur une extraction neuve, sans suppression.
- E-13 Ordre des diffs : celui des dépendances, non le rang de rentabilité de l'avis (§2).
- E-15 Compte de tests de l'ajout daté de GF-10b écrit 25 au lieu de 23 (compte non mesuré, classe K-17) ; trouvé au
  recompte de tous les ajouts datés contre les arbres, corrigé.

## 10. Journal de provenance

Sources lues dans cette passe, niveau [lu] : `BRIEF-GF1.md` ; `ADJUDICATION.md` ; `AVIS.md` ; `PROPOSITION.md` ;
`ERREURS-ORCHESTRATEUR.md` (deux versions) ; `scripts/controle/README.md` ; liste de `scripts/controle/` et de ses
tests (noms) ; `scripts/controle/tests/test_fm11.py` ; `scripts/controle/fm11.py` (structure par `ast`, motifs jamais
affichés : longueurs et classes de caractères seulement) ; `.github/workflows/gates.yml` (360 lignes, `52b94cd3…`) ;
`enforcement/tests/run-fixtures-verdict-suite-s2.py` (cas K, l.560-660) ; `enforcement/verdict-suite-s2.py` (l.1-80) ;
`enforcement/workflows-yaml.py` (l.1-60) ; `enforcement/lint-model-pinning.sh` (entier) ; `enforcement/docs-sha256sums.py`
(entier) ; ligne `VENDOR=` de `enforcement/gate-secrets.sh` ; `xtask/src/lib.rs` l.57-70 ; en-têtes de `xtask/src/sg5.rs`
et `sg9.rs` ; `scripts/sim-bis/oracle_r1.py` (lignes de `git archive`) ; scratchpad : `outils/presg5.py`
(`60de4077…`), `chaine_fz2.sh` (`fc074c47…`), `verser_fz.py` (`047c0998…`), `verser_d5c.py` (`aea8d5e4…`),
`isole.sh` (`ebaa1c78…`), `lo_up.py` ; `.claude/agents/shogen-orchestrator.md` et `shogen-worker.md` ;
`docs/adr-0028/G0-lots-DETTES.md` (entier, `868f9fff…`) ; `docs/adr-0028/ADR-0028-decisions-sortie-S2.md` l.285-297
(`e0007859…`) ; `docs/adr-0028/ANNEXE-B-items.md` l.1611-1625 (B.95) ; noms de fichiers de `docs/adr-0028/` cités dans
`CLAUDE.md` et `docs/PASSATION-CLOUD.md` (recherche ciblée dans ces deux fichiers). Niveau [2nd] : coûts et contextes des
erreurs, repris de la liste de l'orchestrateur et de la proposition ; entrée « suppression de branche » (E17).
Aucun emplacement interdit ouvert, aucun `*.jsonl`, aucune pièce de D.2, aucune variable de clé lue, rien sur Pocket.
Commandes, heures et sorties : `gf1/NOTES.md` (journal de la passe) ; mutants : `gf1/mutants/*.log` ; scripts du
générateur : `gf1/outils/` (banc de mutants, lignes de gates, rejeu des diffs, sortie dorée) et `gf1/ecrire/`
(ajouts datés, plancher, versement de `presg5.py`). Chiffres de ce rapport recomptés par script : lignes ajoutées et
sha256 des diffs, comptes de tests par arbre, bilan des mutants.

## 11. Ajout daté du 2026-10-10 07:59:35 UTC : tête du moment

Après l'écriture de ce rapport, la tête du projet a avancé trois fois :
`6e673097f81d9a4bf6e869329482e07f65278939` (DT6-h), `157357abae32a2b0a19dc6be66d05dde54ccceba` (DT6-i, DT6-j),
puis `d42fcaa58b05a1af90103f6afb95726a47d35f30` (DT6-k). Changements amont dans les chemins touchés par la série
et dans les fichiers que lisent les outils et les gates (`git diff --stat` sur une liste explicite de chemins) :
`gates.yml` seul (plancher s2bis 355 → 356 → 358 ; quatre lignes de commentaire de DT6-j après la l.271, hors
des blocs de la série) ; l.293 d'ADR-0028 inchangée (même sha256 ; ajout en fin de fichier, avant `2fcd303`) ;
scripts de `enforcement/` lus par les gates et `xtask` inchangés depuis `2fcd303`.

- `6e67309` plus la série : les 18 diffs s'appliquent dans l'ordre, `avant_acte.py diff` sortie 0 sur chacun, sans
  avertissement ; 14 lignes de gates vertes : runner 137 ok ; S2 Ran = 419 ; s2bis Ran = 356 ;
  sim-bis Ran = 279 ; calib-actifs Ran = 65 ; controle Ran = 89 ; runners-epingles, cas (16 ok) et
  lecture YAML, journaux-modele, docs-sha256sums, cas du lint R-1 (227 ok), lint R-1 (11 fichiers),
  marqueurs de dette : conformes.
- `157357a` plus la série : les 18 diffs s'appliquent dans l'ordre, `avant_acte.py diff` sortie 0 sur chacun ;
  10 lignes de gates vertes, toutes sauf les quatre suites S2, s2bis, sim-bis, calib-actifs (aucun de leurs
  fichiers n'est touché par la série) : runner 137 ok ; controle Ran = 89 ; runners-epingles, cas (16 ok)
  et lecture YAML, marqueurs de dette, journaux-modele, docs-sha256sums, cas du lint R-1 (227 ok),
  lint R-1 (11 fichiers) : conformes (`gf1/outils/gates_partiel.sh`, `gf1/outils/gates_reste.sh`).
- `d42fcaa` (DT6-k ; aucun changement amont dans la même liste de chemins) plus la série : les 18 diffs
  s'appliquent dans l'ordre, `avant_acte.py diff` sortie 0 sur chacun (18 lignes de sortie, aucun avertissement) ;
  runner 137 ok ; controle Ran = 89 ; runners-epingles, cas (16 ok) et lecture YAML, marqueurs de dette : conformes.
- `cargo --locked xtask verify` non relancé après `2fcd303` (§5).
- Ajout du 2026-10-10 08:11:59 UTC. Écart E-16 (classe K-17, chiffres non recomptés) : le total des lignes
  ajoutées était écrit 2 286 (somme d'avant l'ajout de GF-10b) et le §4 comptait 18 diffs de code
  (GF-0 n'en est pas un : 17). Trouvés au recompte final : `git apply --numstat` sur les 18 diffs donne
  2 309 ; les journaux du banc donnent 17 groupes, 203 mutants distincts, 200 tués, 3 vivants
  déclarés équivalents. Corrigés en place aux l.36, 83 et 159 de ce rapport (même nombre de lignes, aucun
  décalage).
- Base verte des campagnes dont le journal ne porte pas de ligne `base` (GF-1 à GF-5b, banc d'avant E-5) :
  la ligne exacte du job `controle-unittest` passe sur l'arbre de chacun des 18 diffs, tel que commis
  dans le dépôt jetable (planchers 37 → 89, Ran égal au plancher, `gf1/outils/arbres_verts.sh`) ;
  dans ceux de ces journaux qui portent plus d'un mutant tué, aucun test n'échoue sous tous, sauf pour GF-2
  (un seul test, la sortie dorée, cible de chaque mutant) et GF-4b (des mutants vivants y montrent la base
  verte).
