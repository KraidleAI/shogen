# G0 du lot SIM-BIS (SIM-NIVEAU-BIS ‖ SIM-PUISSANCE-BIS, S2-bis)

Adjugé par l'orchestrateur le 2026-10-04 23:02:56 UTC (heure produite par le script). Rattachement : ADR-0029 révision 3, acceptée (§2.4, §2.7, §6
lot 4, §8 ; ajout daté après l.141 sur les sources de la méthode des rotations) ; G0 de vague `docs/adr-0029/G0-lots-S2BIS.md` ;
sorties du lot PLAN-S2BIS (`docs/adr-0029/plan-s2bis/`). Pièces : proposition du rédacteur (`PROPOSITION.md`, worker
`claude-opus-5-5`, sha256 `0e78afab…`, 55 exigences E-S-01 à E-S-55, 22 questions Q-S-01 à Q-S-22) ; avis de l'advisor (`AVIS.md`,
`claude-fable-5-1` effort medium, sha256 `aaf70a4f…` : 15 recommandations adoptées, 7 modifiées, aucune rejetée).

## Adjudications
1. **La proposition est le contenu de ce G0** (périmètre, exigences, règle de n_s et T_max, règle de niveau, cellules, sous-lots,
   tests, critères de sortie, actes de l'investisseur), **corrigée par l'avis** : pour chacune des 22 questions, la recommandation de
   l'avis s'applique telle qu'écrite, y compris ses sept modifications (Q-S-03, Q-S-04, Q-S-06, Q-S-09, Q-S-11, Q-S-13, Q-S-21).
2. **Q-S-03** : l'échelle des durées tourne aux trois niveaux de calibration C0, C1, C2 ; la durée déclarée est celle de C2 ; si
   W*(C2) > 16 semaines ≥ W*(C0), le lot PLAN-S2BIS-2 (identification du groupement par source) passe **avant** toute question de durée
   à l'investisseur (acte A-2) : aucun allongement n'est demandé sur un artefact de calibration.
3. **Les sept écarts à la lettre de l'ADR** (§11 de la proposition, §4 de l'avis) sont adoptés et portés par l'ajout daté du même jour
   à l'ADR-0029 (après l'ajout du G0 de COLLECTE-BIS) ; SHOGEN-S2BIS-SIM-1 n'est pas fermé : sa portée est réduite et re-datée.
4. **Items** : les huit items du §12 sont formés (annexe B.61), avec les précisions de l'avis ; la portée de SHOGEN-S2BIS-ENREG-ROLE-1
   s'étend à `scripts/sim-bis` et SHOGEN-S2BIS-P1-ESTIMATION-1 s'applique à l'estimation du §6.1.
5. **Décisions réservées à l'investisseur** [INV] : durée au-delà de 16 semaines (A-2) ; serveur de calcul au-delà de 72 h de mur
   (A-3) ; information, dans A-2, que 20 % de NON ÉVALUABLE sous H0 est la probabilité acceptée qu'une campagne sans incident ne
   tranche pas. Aucune dépense sans acte écrit.
6. **Lieu du calcul** : hôte de session, lots détachés de 90 min au plus, versement par phase, graines par réplication ; bibliothèque
   standard seule (R-8 sans objet tant qu'aucune dépendance n'est proposée).
7. **Écarts du rédacteur** E-1 à E-6 (§14 de la proposition) : acceptés ; E-2 (sondes de temps hors dépôt, aucun taux de rejet
   imprimé) et E-6 (barres obliques inverses dans des heredocs, contrôlées) déclarés.

## Suite
Sous-lots SB-1 à SB-15 (§6 de la proposition) par un worker `claude-opus-5-5` effort max, tranche par tranche, G2 neuve à 100 %,
chaque diff ≤ 200 lignes de code ; exécution provisoire sur le pool de l'ADR pour clore la conception et débloquer RB-7 ; exécution
finale épinglée après le gel des pools.

*Ajout daté du 2026-10-05 01:45:03 UTC (relecture G2 de la tranche 1, `revue-t1/`)* : (1) **numérotation** : les sous-lots sont **SB-0 à SB-14** (proposition §6.1) ; « SB-1 à SB-15 » au § Suite ci-dessus est une erreur de compte de l'orchestrateur. (2) **E-S-10** n'est pas réalisable à la lettre : l'histogramme des épisodes d'EP compte tous les épisodes, censurés compris (`scripts/plan-s2bis/episodes.py` l.47-50 ; EP l.13-14 : 332 épisodes dont 51 censurés) ; SB-3 emploie la loi « tous épisodes » d'EP avec une limite écrite (écart des moyennes complets / tous : −0,035 à +0,134 fenêtre en calme, −0,023 à +0,015 en stress, mesuré par le réviseur) ; recours : PLAN-S2BIS-2, selon l'adjudication 2. (3) Questions de la tranche 1 adjugées : `Fraction(cellules, n_s)` ; indice de réplication à 0 ; composants des flux en liste fermée sous schéma avant E0 ; `math.nextafter` admis au sens d'E-S-43 (nextUp IEEE 754, vérifié par le réviseur) ; pas de garde réseau dans les tests ; lundi de référence, table géométrique de 4 096 rangs et garde de 128 bits scellés tels quels à E0.
