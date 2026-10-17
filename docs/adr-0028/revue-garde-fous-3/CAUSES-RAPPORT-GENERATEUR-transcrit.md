# Rapport du générateur du lot CAUSES (l'orchestrateur ; E37, E39, E40) (transcrit)

> Transcription par l'orchestrateur le 2026-10-17 07:31:23 UTC du fichier causes/RAPPORT-GENERATEUR.md ; générateur : l'orchestrateur lui-même, sans transcript d'agent. Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Rapport du générateur : lot CAUSES (erreurs E37, E39, E40 ; pas INT-20 à INT-22 de la chaîne INTEGRATION-P3)

Générateur : l'orchestrateur, 2026-10-17 00:23:32 UTC (`date -u`). Rattachement : ADR-0028, annexe B, bloc B.108 (GARDE-FOUS-ORCH phase 2 commise) et lot INTEGRATION-P3 en cours (pas INT-01 à INT-19 relus, série non commise) ; registre des erreurs de l'orchestrateur, entrées E37, E39 et E40 ; décision de l'investisseur du 2026-10-17 : les erreurs passées se suppriment par leurs causes, avec des outils, sans flux d'orchestration.

## Constat (une cause par erreur)
- E37 : une chaîne a disparu pendant sa vérification tandis qu'une campagne de mutants de l'intégrateur tournait sur le même hôte ; rien n'empêchait deux lots lourds à la fois.
- E39 : la chaîne INTEGRATION-P3 a rougi au premier pas parce que des cas de la suite héritaient des variables du lancement ; le passage à blanc (`chaine --blanc`) ne jouait pas la suite sous ces variables, la faute n'apparaissait qu'au lancement. Le lot ISOLE-ENV corrige la fuite ; ce lot ferme la cause de sa découverte tardive.
- E40 : une consigne à un worker a nommé de mémoire la cause d'un refus de gate (« garanti » au lieu du mot réellement relevé) ; rien n'exigeait de citer la ligne lue.

## Correctifs (trois diffs, appliqués en série sur l'état final de la série INT-01 à INT-19 ; la série rejouée est égale à la copie, `diff -r`)
- `CAUSES-1.diff` (`6c647ceea189a01e…`, trois fichiers, +77/−1) : `scripts/controle/garde/motif-chaine.txt` (une ligne, motif ancré par `^`, reconnaît `bash chaine.sh` et `bash chaine_x.sh` avec ou sans chemin) ; `avant_acte.py` : `motif_chaine()` lit ce fichier (une seule ligne ancrée exigée), `suite_k8()` joue la ligne exacte du job `controle-unittest` de `gates.yml` de la copie, dans la copie à l'état final du plan, sous l'environnement du lancement tel quel, borne `BORNE_K8` ; rouge, ligne absente ou double : refus K8 ; copie sans `gates.yml` : rien à jouer ; appelée par `blanc()` quand `--plan` est donné. Cas : `test_k8_suite_sous_les_variables_du_lancement`, `test_motif_de_chaine_lu` (`tests/test_avant_acte.py`, classe `ChaineABlanc`).
- `CAUSES-2.diff` (`319c63f9a6850dfb…`, trois fichiers, +140/−5) : crochet `.claude/hooks/garde_faits.py`, règle R13 : (a) une chaîne tourne (`pgrep -f` du motif partagé) : tout Bash qui lance `cargo`, `xtask` ou `mutants.py` est refusé ; (b) un Bash qui lance `chaine.sh` ou `chaine_*.sh`, aussi derrière `setsid nohup timeout bash -c`, doit lancer une copie à l'octet (sha256) de `gabarits/chaine-modele.sh` du dépôt ; modèle absent ou script illisible : refus ; (c) une consigne (Agent, Workflow, SendMessage) qui dit qu'une gate ou un contrôle a rougi doit citer une ligne `VIOLATION …` ou `REFUS …` présente dans un résultat d'outil du journal ; cause déduite sans ligne, ou ligne citée absente du journal : refus. Cas : `test_r13_processus_lourd_pendant_une_chaine`, `test_r13_chaine_lancee_hors_du_modele`, `test_r13_cause_de_refus_sans_la_ligne_de_la_gate` (`tests/test_garde_acte.py`, classe `Forge`) ; `tests/test_garde_refus.py` : la liste des règles du refus lecteur compte R13.
- `CAUSES-3.diff` (`96e4709ada280834…`, deux fichiers, +36/−0) : `mutants.py`, `chaine_en_cours()` par le même motif ; campagne refusée (sortie 3) quand une chaîne tourne ; motif absent ou `pgrep` en erreur : `ValueError`. Cas : `test_e37_campagne_refusee_pendant_une_chaine` (`tests/test_mutants.py`).
- Le lot ajoute six cas ; plancher du job `controle-unittest` 225 → 231 à l'état final de la série (porté par le pas INT-22 avec le README des contrôles, texte `readme/D.txt` de l'intégrateur). Aucun pas de la série INT-01 à INT-19 ne touche `motif-chaine.txt` ni `mutants.py` après INT-19 ; le crochet et `avant_acte.py` sont touchés par la série avant, d'où la pose en fin de plan.

## Preuves
- Suite `scripts/controle` à l'état final du lot : `conforme (code 0, résumé final, aucun saut, Ran = 231)` dans l'environnement normal et sous `DETACHE=1 DUREE_PAS=60 DELAI=2400 DISQUE_MIN_GO=0` (`suite-env4.out`, `suite-env4-1.out`). Un passage rouge (`suite-env4-2.out`, un échec, `test_r13_chaine_lancee_hors_du_modele`) a couru sur une version antérieure du cas, dont l'ordre des assertions dépendait d'un dossier partagé (modèle retiré avant la comparaison « script différent ») ; le cas a été réordonné avant la version commise, le passage rejoué est `suite-env4-3.out`.
- Chaque cas rouge sans son correctif : les onze mutants ci-dessous le montrent, chacun tué par un seul cas.
- `.claude/hooks/tests` : la suite du crochet verte à l'état final (`test_garde_acte`, vingt-cinq cas ; `test_garde_refus`).

## Mutants (à la main, copie `mut/` rendue à ses octets après chaque mutant, `cmp`)
- K8a (`suite_k8` jamais appelée), K8b (tous les `if p.returncode` d'`avant_acte.py` neutralisés), K8c (ligne double admise) : `test_k8_suite_sous_les_variables_du_lancement` rouge : tués.
- MCa (contrôle « une ligne ancrée » retiré) : `test_motif_de_chaine_lu` rouge : tué.
- R13a (`cargo` retiré du motif des processus lourds) : `test_r13_processus_lourd_pendant_une_chaine` rouge : tué.
- R13b (script différent admis), R13b2 (modèle absent admis) : `test_r13_chaine_lancee_hors_du_modele` rouge : tués.
- R13c (toute cause admise), R13c2 (mot de rougeur inversé) : `test_r13_cause_de_refus_sans_la_ligne_de_la_gate` rouge : tués.
- E37a (refus de campagne retiré), E37b (`pgrep` lu à l'envers) : `test_e37_campagne_refusee_pendant_une_chaine` rouge : tués.

## Limites
- Le motif reconnaît un lancement par `bash` ou `sh` ; une chaîne lancée par `source` ou `.` n'est pas vue (aucun modèle du dépôt ne se lance ainsi).
- R13 (c) juge les consignes qui portent un mot de rougeur (`GATE_ROUGE`) ; une cause déduite dite sans ce vocabulaire passe. Le relevé d'un lancement passe par `pgrep -f` : un hôte sans `pgrep` fait échouer `mutants.py` par `ValueError` (jamais une campagne à l'aveugle).
- K8 joue la suite une fois, à l'état final du plan ; un pas intermédiaire rouge sous les variables du lancement n'est vu qu'au lancement (chaque pas joue déjà la vérification complète).

## Ajout daté du 2026-10-17 01:53:36 UTC (`date -u`) : après la relecture G2
Corrections C-1 à C-4 du réviseur reprises à l'octet et repliées par fichier dans les pas de la chaîne : INT-20 porte CAUSES-1, C-4 et la part de C-2 sur `garde/motif-chaine.txt` et `tests/test_avant_acte.py` ; INT-21 porte CAUSES-2, la part de C-2 sur le crochet et ses cas, et C-3 ; INT-22 porte CAUSES-3 et C-1. La série repliée rejouée depuis l'état final de INT-19 est égale à l'octet (`diff -r`) à la copie plus C-1 à C-4 en série, l'état que le réviseur a prouvé. C-5 (README rendu) : les empreintes des huit fichiers de `readme/D.txt` recalculées sur cet état, plancher écrit par la chaîne (tête 179 : 231 après INT-22).
