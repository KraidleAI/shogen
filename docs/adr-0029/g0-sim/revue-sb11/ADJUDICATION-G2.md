# Adjudication de l'orchestrateur sur la G2 de SB-11 (2026-10-09, après 06:39:05 UTC)

Pièce d'entrée : `g2/RAPPORT-G2.md` (réviseur neuf, `claude-opus-5-5`, ACCEPTE-AVEC-CORRECTIONS ; contrôle FM-1.1 de son transcript : 0 fragment). À lire en entier, avec `g2/preuves/test_preuves_g2.py` (preuves P-1 à P-9) et `g2/mut/campagne.txt`. Le brief `BRIEF-SB11.md` et `LIGNES-BRIEF-SB11.md` restent en vigueur ; aucune écriture git ; `date -u` avant toute heure ; NOTES.md tenu.

Base : **5e386c4**, inchangée. La série SB-11a … SB-11u reste telle quelle ; les corrections forment **un diff neuf SB-11v** (≤ 200 lignes de code ajoutées, tests compris ; scinder en SB-11v et SB-11w s'il le faut), plancher sim-bis recalé exactement (246 + n).

À corriger (liste fermée, celle du réviseur, §5) :
- C-1 (code) : `executer.plan`, `t = borne // ns * processus` ; `test_budget` aux durées (12, 5) ; `test_plan_90_min` au cas 41 s × 4 processus (lots de 524, 131 tours, 5 371 s) ; mutants : l'ancienne formule et G-22.
- C-2 à C-9 (tests de site d'appel et de source des données) : chacun tel que décrit au §5 du rapport, chacun tuant son mutant nommé (G-01, G-03, G-06, G-07, G-08, G-19, G-09, G-12, G-10, G-11, G-16). Règle de fixture pour ces tests : pour chaque paramètre passé sous étiquette, une valeur qui diffère de toute source concurrente (constat de méthode du réviseur).

Questions et constats :
- Q-SB11-7 et O-3 : non corrigés dans ce lot (le défaut est dans `regle`, SB-7) ; item **SHOGEN-SIM-BIS-NPRIME-NUL-1**, qui **bloque E0** : un test qui reproduit n′_s = 0 (la fixture d'E-14 ayant été déplacée) et un refus nommé ou un NON ÉVALUABLE à causes listées (celles de n′ = 1), à adjuger à son G0. Rédige sa ligne.
- Avis du réviseur adoptés sur Q-SB11-1 à Q-SB11-19 (§11). Q-SB11-2, Q-SB11-3, Q-SB11-12 et Q-SB11-16 sont à régler avant E0 ; Q-SB11-19 et O-9 au brief de SB-12.
- Items à rédiger (constat, propriétaire, déclencheur, prix, origine) : BUDGET-SERRE-1 (avec C-1, une marge déclarée et le coût de l'oracle compté à part), VALS-STRICT-1 (avec O-9), MUT-EQUIV-FIXTURE-1 (portée élargie, règle de brief citée ci-dessus, à joindre comme volet de SHOGEN-MUTANTS-SITE-APPEL-1), NPRIME-NUL-1, AGREGATS-SB12-1 (O-4), et, s'ils ne sont pas déjà rédigés à ton rapport, P-L20-1, FAMILLES-1, E1-LANCEUR-1 (avec O-6), TDET-ECHELLE-1 (i ≥ 200), MUT-DUREE-1. O-7, O-8 et O-10 : une ligne d'item chacun, ou une raison écrite de ne pas en faire.
- Écarts E-16 à E-28 du générateur et E-R1 à E-R5 du réviseur admis.

Preuves : rouge d'assertion de chaque test neuf (les preuves P-1 à P-9 du réviseur sont des données, pas ton test : écris les tiens dans la suite) ; campagne d'au moins 10 mutants sur SB-11v (les mutants nommés ci-dessus compris), classée par la commande du job sim-bis, PAR=2, borne 300 s ; les 12 vivants non équivalents du réviseur rejoués et tués ; matrice 3.10 à 3.13 en `-X dev -W error` ; runner, jobs s2bis, S2, sim-bis ; xtask (lignes de verdict seules) ; application sur la tête actuelle (`1a388e1`) avec les seuls conflits connus (plancher sim-bis de `gates.yml`, ligne du README).

Rendu (valeur de retour), Gate 0 en tête : diff(s), tableau C-1 à C-9, mutants, matrice, lignes d'items, écarts ; aussi en section datée à la fin de `RAPPORT-GENERATEUR.md`, `SHA256SUMS` recalculé.

## Ajout daté du 2026-10-09 (après 09:38 UTC) : adjudication du contre-contrôle (CONFORME-AVEC-RÉSERVES, R-1 à R-5)

Pièce d'entrée : `g2/cc/RAPPORT-CC.md` (contre-contrôleur neuf, `claude-opus-5-5` ; FM-1.1 : 0 fragment). Les réserves R-1 à R-4 sont corrigées dans ce lot (aucune dette laissée) par un diff neuf **SB-11w**, après SB-11v, sous les mêmes règles (≤ 200 lignes, plancher exact, rouge d'assertion sous le mutant visé, campagne ≥ 10 mutants) :
- C-10 (R-1, O-CC-1) : `test_budget` tue de nouveau « coût = première mesure » (M-CC-08) : durées (5, 12, 7), ou les deux ordres ; aucun test affaibli au niveau des mutants.
- C-11 (R-2, O-CC-2) : cas d'ordre des classes isolé, [BTC, USDT, ETH] (M-CC-09).
- C-12 (R-3, O-CC-3) : C-8 avec absorption et une réplication à i ≥ 200 ; le R de la cellule atteint le calcul « avec » et `variante.tester` (M-CC-03, M-CC-04).
- C-13 (R-4, O-CC-4) : durée de dérive = W·tendance à W = 16 et W = 2 (M-CC-05).
- R-5 (O-CC-6) : la ligne d'item NPRIME-NUL-1 est réécrite au versement par l'orchestrateur (listes de causes mesurées, lieu du correctif laissé au G0).
- MUT-EQUIV-FIXTURE-1 : élargi aux constats O-CC-1 à O-CC-4. O-CC-5 et O-CC-7 : notés.
