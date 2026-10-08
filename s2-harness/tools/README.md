# s2-harness/tools : règle d'usage de l'enregistreur d'oracle (`oracle_record.py`)

Rattachement : item SHOGEN-S2BIS-ENREG-ANCRE-1 (ADR-0028, annexe B, bloc B.73 ; observation O-2 du contre-contrôle de
la réserve R-1, `docs/adr-0029/s2bis/revue-r1/`), sous le G0 `docs/adr-0029/g0-collecte/G0-COLLECTE-RECALC-DEPLOI.md` ;
lot OUT-2, diff OUT-2c (2026-10-08). Ce fichier ne couvre que l'enregistreur ; `rendu_unique.py` a sa docstring.

## L'ancre de confiance est l'arbre de l'outil

Pour `suite-s2bis` et `suite-sim-bis`, l'enregistreur lance la ligne du vérificateur écrite dans le `gates.yml` du
commit, avec le vérificateur de ce commit (`enforcement/verdict-suite-s2.py` de l'extraction). Il exige que ce
vérificateur soit égal, octet pour octet (sha256), à celui de l'arbre d'où l'outil tourne (`VERIF`), à l'écriture
comme à la lecture (SHOGEN-S2BIS-ENREG-VERIF-COMMIT-1, lot R-1). La comparaison ne dit donc rien du vérificateur du
commit par elle-même : elle le ramène à celui de l'arbre de l'outil, qui seul porte la confiance.

## Règle d'usage

1. L'outil tourne depuis un arbre dont le vérificateur a été relu (lecture humaine de son diff, consignée par une
   revue), extrait à part du commit à enregistrer : la comparaison ne vaut qu'à cette condition.
2. Lancé depuis l'arbre du commit enregistré lui-même, l'outil compare ce vérificateur à lui-même : la comparaison
   est triviale, et un vérificateur complaisant passe. Un tel enregistrement ne prouve rien de plus que le code de
   sortie de la ligne du job.
3. La lecture (`--verifier`) suit la même règle : elle compare `tree.sha256` au vérificateur de l'arbre du lecteur.
4. Qui cite un enregistrement nomme l'arbre d'où l'outil a tourné (commit, et sha256 de son
   `enforcement/verdict-suite-s2.py`) et la revue qui a relu ce vérificateur. À défaut, la lecture humaine du
   vérificateur reste nécessaire à chaque verdict cité (réserve R-1 de l'accord de P1).

## Limite

Le schéma `shogen.oracle-record.v1` ne consigne pas l'arbre de l'outil : cette règle est une règle d'usage, aucun
contrôle ne l'impose. Consigner cet arbre (commit, sha256 de `VERIF`, état propre ou non) demanderait un schéma v2 et
une décision.
