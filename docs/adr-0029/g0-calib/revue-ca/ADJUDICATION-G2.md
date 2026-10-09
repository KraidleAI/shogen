# Adjudication de l'orchestrateur sur la G2 de CALIB-ACTIFS (2026-10-09, après 09:20:38 UTC)

Pièce d'entrée : `g2/RAPPORT-G2.md` (réviseur neuf, `claude-opus-5-5`, ACCEPTE-AVEC-CORRECTIONS ; contrôle FM-1.1 de son transcript : 0 fragment). À lire en entier, avec `g2/outils/` (sondes, mutants G01 à G30) et `g2/NOTES.md`. Le brief `BRIEF-CA.md` reste en vigueur ; aucune écriture git ; `date -u` avant toute heure ; NOTES.md tenu.

**Réseau : interdiction absolue.** Toute exécution (tests, mutants, répétition) passe par la recette du réviseur (`g2/outils/run.sh` : `env -u` sur les huit variables de mandataire, puis `isole.sh`). Sonde préalable qui échoue à joindre l'extérieur, consignée. Borne des mutants par `killpg` ; `ps` de fin sans processus restant.

Base : **ebd1560**, inchangée. Série corrigée sous les mêmes noms (CA-0a … CA-6c), un diff neuf seulement si nécessaire ; ≤ 200 lignes ajoutées par diff, tout compris (Q-CA3-1) ; plancher exact à chaque diff.

À corriger (liste fermée) :
- C-1 à C-12 : tels qu'écrits au §5 du rapport de G2, chacun prouvé par le mutant qu'il nomme (G01, G14, G11 et le mutant « garde de `cadence.main` retirée », C-4 sous le PATH simulé avec M-CA-23 toujours tué, G07, G29 et G30, G08, G23, G12 et G13, G28 et G10 avec le rouge du corps `[]`, G27) ; C-12 au rapport.
- C-13 (O-1, décision de l'orchestrateur) : le refus CA/borne imprime la valeur calculée sur une ligne à part de `calib_actifs.txt`, nommée et descriptive, pour qu'une décision au lancement unique n'exige pas un second lancement ; test et mutant.

Constats non corrigés ici, à rédiger en lignes d'items (constat, propriétaire, déclencheur, prix, origine) :
- O-2 : σ_BTC arrondi à la seconde supérieure ; RB-2 (e) exige que le σ de BTC versé dans `analyse.json` soit arrondi de même. Item **SHOGEN-S2BIS-CALIB-SIGMA-ARRONDI-1**, déclencheur : G0 de RB-2.
- O-7 et Q-CA3-8 : **SHOGEN-CALIB-FORMES-API-1** (formes d'API, sens de `end`), condition de l'épinglage.
- O-8 : `etiquette` retirée et `modes` entré au schéma de RB-2 : volet de l'item de RB-2 existant, ou item neuf si aucun ne le porte.
- O-6 et O-3 : limites à écrire au paquet ; une ligne d'item chacune, ou une raison écrite de ne pas en faire.
- Items proposés et adoptés : **SHOGEN-TESTS-GARDE-MANDATAIRE-1** (le défaut est aussi dans `s2bis/tests/__init__.py` : déclencheur, prochain lot qui touche `s2bis/tests/` et au plus tard le gel du collecteur), **SHOGEN-MUTANTS-ORPHELINS-1** (killpg et `ps` de fin aux gabarits de campagne), **SHOGEN-CI-CABLAGE-CALIB-1** (cas K du runner) ; volet de **SHOGEN-S2BIS-P1-ESTIMATION-1** (2 977 lignes mesurées).
- O-4, O-5, O-9 à O-13 : notés, sans item, sauf si ta correction les touche.

Questions : avis du réviseur adoptés sur Q-CA3-1 à Q-CA3-17. E-CA3-1 : le lot ne dépend pas des lignes kraken du manifeste ; ce fait ne sert de preuve à rien ; le contrôle CA/kraken du lancement unique fera foi. Écarts E-CA3-2 à E-CA3-7 et E-G2-1 admis.

Tête : la série corrigée doit s'appliquer sur la tête actuelle avec pour seul conflit le hunk de `gates.yml` de CA-0a, résolu comme dit au §3 du rapport (contexte `--plancher 210`) ; livre aussi cette version résolue (`diffs-tete/`), vérifiée verte sur une copie neuve de la tête (job neuf, runner, s2bis, S2, sim-bis).

Preuves : rouge d'assertion de chaque test neuf ; les 14 vivants du réviseur rejoués (13 tués, G26 équivalent) ; ≥ 2 mutants neufs par correction ; matrice 3.10 à 3.13 en `-X dev -W error` ; xtask (lignes de verdict seules).

Rendu (valeur de retour), Gate 0 en tête : diffs, tableau C-1 à C-13, mutants, matrice, lignes d'items, écarts ; aussi en section datée à la fin de `RAPPORT-GENERATEUR.md`, `SHA256SUMS` recalculé.

## Ajout daté du 2026-10-09 (après 09:59 UTC) : décisions sur le rendu du correcteur
- E-COR-2 : le diff neuf CA-6d est admis (réécrire dix diffs rendrait caduques leurs campagnes) ; la série commise sera CA-0a … CA-6d, dans sa version `diffs-tete/`.
- E-COR-3 : sim-bis n'est pas lancé par les agents du lot (interdit du brief) ; l'orchestrateur le lance avant chaque commit de la chaîne, comme pour tout lot.
- Lignes d'items du correcteur adoptées (SIGMA-ARRONDI-1, FORMES-API-1, RB2-SCHEMA-MODES-1 si aucun item de RB-2 ne porte déjà le volet, TESTS-GARDE-MANDATAIRE-1, MUTANTS-ORPHELINS-1, CI-CABLAGE-CALIB-1, volet de P1-ESTIMATION-1) ; O-3 et O-6 sans item, raisons admises ; O-13 noté.

## Ajout daté du 2026-10-09 (après 10:20 UTC) : adjudication du contre-contrôle (CONFORME-AVEC-RÉSERVES, R-1 et R-2)
- R-2 (O-CC-1, X09 vivant) : corrigée dans ce lot, aucune dette laissée : diff neuf **CA-6e** (une minute active avant `T0` dans la série `binance` de `test_oracle`, ou équivalent), preuve X09 tué par un FAIL d'assertion ; campagne d'au moins 5 mutants sur CA-6e ; plancher exact ; version `diffs-tete/` ; mêmes règles réseau.
- R-1 : les trois retouches de lignes d'items sont faites par l'orchestrateur au versement : O-8 devient un volet de SHOGEN-S2BIS-CALIB-L189-1 (pas d'item neuf RB2-SCHEMA-MODES-1) ; SIGMA-ARRONDI-1 cite `tau.py` l.136 ; TESTS-GARDE-MANDATAIRE-1 cite `4e692df` comme dernier commit qui touche `s2bis/tests/__init__.py`.
- O-CC-2 (seule la valeur du premier CA/borne s'imprime) : item **SHOGEN-CALIB-BORNE-MULTI-1**, déclencheur : avant l'épinglage (E-CA-27).
- O-CC-3 : renvois du §11.1 à corriger dans le rapport avec CA-6e. O-CC-4 : `SHA256SUMS` recalculé avec CA-6e.
