# Rapport du générateur du lot ISOLE-ENV (l'orchestrateur) (transcrit)

> Transcription par l'orchestrateur le 2026-10-17 07:31:23 UTC du fichier isole-env/RAPPORT-GENERATEUR.md ; générateur : l'orchestrateur lui-même, sans transcript d'agent. Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Rapport du générateur : lot ISOLE-ENV (erreur E39 ; préalable de la chaîne INTEGRATION-P3)

Générateur : l'orchestrateur, 2026-10-16 23:43:11 UTC. Rattachement : ADR-0028, annexe B, bloc B.108 (GARDE-FOUS-ORCH phase 2 commise) et lot INTEGRATION-P3 en cours ; registre des erreurs de l'orchestrateur, E39.

## Constat
- Chaîne INTEGRATION-P3, modèle scellé lancé avec `DETACHE=1` (lancement détaché, déclaration vraie) : vérification rouge avant INT-01 ; xtask et `cargo test` verts ; suite `scripts/controle` rouge.
- Rejeu porte par porte (`<scratchpad>/diag-int3/`) : quinze portes vertes seules ; sous les variables du lancement et une chaîne active, la porte `scripts/controle` rouge, un seul cas : `test_e25_lancement_lie`, `AssertionError: Tuples differ: (False, ['X-2', 'X-1']) != (True, [])`.
- Cause : `tests/aide_garde.env_git` recopie `os.environ` (hors `GIT_*` et `SHOGEN_S2_CAMPAGNE_CONTROL`) ; le cas hérite de `DETACHE=1` et admet le lancement lié qu'il doit refuser. `DEPOT`, `PLAN`, `CC`, `OUTILS`, `PYTHON` sont réécrits par `lancer()` : le vrai dépôt n'est pas visé.
- À l'état final de la série, sans correctif, sous les mêmes variables : deux échecs, `Chaine.test_e25_lancement_lie` et son jumeau `ChaineModele.test_e25_lancement_lie` (`final-sans-correctif.out`).

## Correctif (`ISOLE-ENV.diff`, `8809f015605086e5…`, quatre fichiers, +60/−3)
- `tests/aide_garde.py` : `variables_de_chaine()` lit les noms `${NOM:` des modèles `gabarits/*.sh` sur les fichiers (aucune liste recopiée : un modèle neuf est couvert) ; `env_git` les retire de l'environnement copié.
- `tests/test_aide_garde.py` (neuf) : deux cas. `test_e39_variables_de_chaine_retirees` : toutes les variables des modèles posées dans l'environnement ambiant, aucune dans `env_git`, une variable étrangère passe, `DETACHE` est bien lue. `test_e39_lancement_lie_sous_lancement_detache` : le cas réel, `test_e25_lancement_lie` rejoué sous `DETACHE=1` et `DUREE_PAS=60` ambiants, vert.
- Plancher du job `controle-unittest` 177 → 179 ; ajout daté en fin de README des contrôles.

## Preuves
- Rouge avant, vert après : sur l'aide de la tête, `ERROR` au premier cas (fonction absente) et `FAIL` au second (le cas réel) ; avec le correctif, `OK`.
- Suite `scripts/controle` à la tête plus le correctif : `conforme (code 0, résumé final, aucun saut, Ran = 179)`, dans l'environnement normal et sous `DETACHE=1 DUREE_PAS=60 DELAI=2400 DISQUE_MIN_GO=0`.
- Correctif posé sur l'état final de la série (`arbre-final` de l'intégrateur, hors `gates.yml` et README) : `conforme (… Ran = 225)` sous les mêmes variables.
- `git apply --check` du diff sur la tête : vert ; aucun pas de la série ne touche `tests/aide_garde.py` ni `gates.yml` ; le fichier de sommes des contrôles ne cite pas l'aide.

## Mutants (à la main, aide rendue à ses octets, `cmp`)
- M1 (`M1.diff`) : filtre `and k not in chaine` retiré : test_e39_variables_de_chaine_retirees et test_e39_lancement_lie_sous_lancement_detache rouges : mutant tué.
- M2 (`M2.diff`) : motif `${NOM:` changé en `${NOM}` : les deux cas rouges : mutant tué.
- M3 (`M3.diff`) : modèles `.sh` lus comme `.bash` : les deux cas rouges : mutant tué.

## Limites
- Les variables lues par un modèle sous une autre forme que `${NOM:` (par exemple `$NOM` nu) ne sont pas vues ; les deux modèles du dépôt n'en lisent aucune autre (relevé `grep` des deux fichiers).
- Item formé : SHOGEN-CHAINE-BLANC-ENV-LANCEMENT-1 : le passage à blanc d'une chaîne ne joue pas la suite `scripts/controle` sous les variables de son lancement.

## Ajout daté du 2026-10-17 00:46:50 UTC (`date -u`) : après la relecture G2
- Diff v2 `ISOLE-ENV.diff` (`ad59159c7593c66c…`, quatre fichiers, +53/−3) : le diff v1 (`ISOLE-ENV-v1.diff`) plus C-1 (référence `LUES` des neuf noms, vérifiée par inclusion) et C-4 (deux apostrophes du README) de la G2, repris à l'octet. C-2 et C-3 sont posées en fin de série (pas INT-23 de la chaîne INTEGRATION-P3), le hunk d'INT-18 interdisant la tête.
