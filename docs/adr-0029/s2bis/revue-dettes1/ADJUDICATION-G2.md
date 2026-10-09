# Adjudication de l'orchestrateur sur la G2 de DETTES-T1 (2026-10-09)

Pièce d'entrée : `g2/RAPPORT-G2.md` (réviseur neuf, `claude-opus-5-5`, ACCEPTE-AVEC-CORRECTIONS pour les deux dettes ; FM-1.1 : 0 fragment).

À corriger (liste fermée), sous les mêmes règles que la génération (réseau coupé, tests d'abord, rouge d'assertion sous le mutant visé, ≤ 200 lignes, plancher exact) :
- C-A1 : formes de casse mêlée pour chaque schéma dans le test de purge (`hTtP_pRoXy`, `hTtPs_PrOxY`, `aLl_pRoXy`) ; docstring corrigée ; preuve MA01 tué.
- C-A2 (O-6, décision de l'orchestrateur : aucune dette laissée) : `test_dns.test_drapeau_tc_garde_section_reponse_non_lue` ne doit plus dépendre d'un port UDP éphémère réutilisé en TCP (EADDRINUSE, 1 échec sur 33) ; port TCP pris par `bind(('127.0.0.1', 0))` puis lu, ou équivalent ; preuve : 100 lancements du test seul sans échec, et le test garde sa force (ses mutants tués).
- C-B1, C-B2, C-B3 : tels qu'au §« Corrections » du rapport (un seul refus dans la boucle ; premier refus sans valeur puis CA/borne ; ordre des actifs différent de l'ordre des valeurs) ; preuves MB03, MB01, MB10 tués.
- C-B4 (Q-DT-2 adoptée) : une ligne `descriptif hors refus (jamais décisif) : refus suivant : <refus>` par refus suivant sans valeur ; exceptions non nommées imprimées `CA/calcul (<type>)` ; refus écrit et JSON inchangés ; une passe de test et une phrase au README.
- C-B5 (O-7) : README de BM-1 : « le JSON ne porte que le refus ».

Questions Q-DT-1, Q-DT-3, Q-DT-4 : avis du réviseur adoptés. O-5, O-8, O-9 notés. Écarts E-DT-1 à E-DT-3 et E-G2-1 à E-G2-7 admis.

Rendu : diffs corrigés sous les mêmes noms (GM-1, BM-1, versions série et tête ; un diff neuf pour C-A2 si GM-1 dépasse 200 lignes), tableau des corrections, mutants, matrice, gates, `SHA256SUMS` recalculé, section datée à la fin de `RAPPORT-GENERATEUR.md`.

## Ajout daté du 2026-10-09 (après 13:37 UTC) : adjudication du contre-contrôle (CONFORME-AVEC-RÉSERVES, R-1 à R-3) ; règle « aucune dette »
- C-A3 (R-1) : le test TC vérifie que TCP et UDP partagent le port (`tcp.getsockname()[1] == port` dans la boucle) ; preuves NA2, NA3 tués.
- C-B6 (R-2) : passe « deux suivants » (ETH à 102, USDC en ZeroDivisionError, USDT en CA/population ; ordre des lignes figé) ; preuves NB2, NB3 tués.
- C-B7 (R-3) : passe « exception premier » (refus écrit et JSON figés quand le premier refus est une exception non nommée) ; preuve NB4 tué.
- C-B8 (O-CC-5, aucune dette) : les lignes « refus suivant » identiques ne sont imprimées qu'une fois (refus global aux paramètres) ; test et mutant.
La forme proposée par le contre-contrôleur (`g2/cc/travail/propose-R1-R3.diff`) est une donnée, pas le diff à livrer.

## Ajout daté du 2026-10-09 (passe 3 du contre-contrôle, CONFORME-AVEC-RÉSERVES, R-1 à R-3 levées, R-4 ouverte) ; consigné à 14:45 UTC
- C-B9 (R-4, O-CC-7) : passe « même motif » de `test_borne_plusieurs` (deux actifs au même refus, un troisième qui répète le motif d'un autre), pour distinguer le dédoublonnage par texte entier de ses variantes ; preuves ND1, ND2 tués. Transmise au correcteur par message avant 14:25 UTC ; consignée ici après coup (écart de forme, sans effet sur le contenu : la passe 4 du contre-contrôle cite R-4 et ND1, ND2).
