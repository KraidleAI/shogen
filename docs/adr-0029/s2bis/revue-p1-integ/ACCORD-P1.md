# Accord de fin de partie P1 (collecteur S2-bis, noyau) — avis d'advisor

- Gate 0 : modèle résolu `claude-fable-5-1`, effort `medium` (CLAUDE.md §7, amendement 2026-09-18 ; R-26).
- Date : 2026-10-05 d'après le contexte de session ; `date -u` non exécutable ici (aucun outil shell dans cet
  environnement), écart déclaré. Le bloc B.71 est daté 2026-10-05 23:30:28 UTC, l'avis est donc postérieur à cette heure.
- Rattachement : G0 `docs/adr-0029/g0-collecte/G0-COLLECTE-RECALC-DEPLOI.md`, point 5 et ajout du 2026-10-05 04:38:22 UTC
  (accord rendu par un advisor sur la pièce de clôture, au regard du but : standard institutionnel vendable, sans baisse
  de qualité ; dépense, calendrier et Pocket restent à l'investisseur).
- Pièces lues à la tête 2d30697 : `CLOTURE-P1.md`, `G2-P1-INTEG-transcrit.md`, `RAPPORT-CORRECTIONS-P1-INTEG-transcrit.md`,
  `CONTRE-CONTROLE-P1-INTEG-transcrit.md` (dossier `docs/adr-0029/s2bis/revue-p1-integ/`), annexe B bloc B.71 seul
  (`docs/adr-0028/ANNEXE-B-items.md` l.1143-1165), G0 l.21-23. Aucune pièce D.2, aucun dossier interdit, aucun `*.jsonl`.

## Verdict : ACCORD-AVEC-RÉSERVES

**Pourquoi l'accord.** La pièce de clôture demande cinq corrections avant l'accord (CLOTURE §3, C-1 à C-5). Les cinq sont
faites en huit diffs, avec preuves recomptées : banc à coupures 0 rupture et 0 somme fausse contre 128 et 131 avant ; plus
grande `sante` 3 823 224 octets sous LIMITE ; les cinq mutants d'interface tués, plus 96 mutants neufs tués ; runner qui
sort en 3 sur un vérificateur complaisant au chargement (RAPPORT-CORRECTIONS, résumé et tableau final). Le contre-contrôle
du même réviseur, indépendant des tranches, est CONFORME avec une liste vide, chiffres recomptés sans import du collecteur
(CONTRE-CONTROLE §1-§5). Les commits sont consignés (`3576bef` à `991d608`, B.71). Ce qui reste ouvert est formé en items
avec propriétaire et déclencheur (B.71, tableau et précisions), ce que le point 5 du G0 exige pour la pièce de clôture.
Les preuves de P1 (sonde du FORMAT à 0 écart sur 1 000 journaux, bout en bout réel, 30 minutes en plateau mémoire,
entrées hostiles closes ; CLOTURE §2) sont du niveau attendu d'un standard vendable.

**Ce qui pèse le plus sur le but du projet, en une phrase.** Ce qui reste ouvert de plus lourd est la confiance dans
l'outillage de preuve lui-même : l'enregistreur de rôle exécute encore le vérificateur du commit relu et peut être trompé
par un vérificateur complaisant, et le runner sort encore en 0 sur `os._exit(0)` (CLOTURE §5 ; CONTRE-CONTROLE §4 et
« À noter » ; B.71 items ENREG-VERIF-COMMIT-1 et RUNNER-SORTIE-1) — or un standard institutionnel se vend sur des preuves
qu'un tiers ne peut pas contourner, et tant que cela tient, la relecture humaine du vérificateur reste la seule garantie.

## Réserves (liste fermée)

| n° | réserve | déclencheur |
|---|---|---|
| R-1 | Les items SHOGEN-S2BIS-ENREG-VERIF-COMMIT-1 et SHOGEN-S2BIS-RUNNER-SORTIE-1 (B.71) sont fermés et contre-contrôlés avant que la G2 de P2 commence ; aucun accord de P2 ne peut être rendu sur des verdicts de CI qu'un vérificateur altéré trompe. D'ici là, chaque verdict de CI cité par une pièce de revue s'accompagne d'une lecture humaine du vérificateur (CLOTURE §5, dernier point). | avant la G2 de P2 (déclencheur déjà inscrit en B.71) |
| R-2 | `CLOTURE-P1.md` a été rédigée avant les corrections et son §3 dit encore « reste à faire » (CLOTURE l.43 ; B.71 : « versée telle que rendue »). Une note datée, posée par l'orchestrateur en tête du dossier `revue-p1-integ/` ou de la pièce, doit renvoyer §3 aux commits `3576bef`-`991d608` et au contre-contrôle CONFORME, pour qu'un lecteur extérieur ne croie pas la partie inachevée. | au versement du présent accord |
| R-3 | P1 mesure environ 2,4 fois l'estimation du G0 (CLOTURE §5 ; B.71, P1-ESTIMATION-1), et le calendrier annoncé en dépend. Ce n'est pas un motif de refus technique, mais c'est une question de valeur réservée à l'investisseur (G0, ajout du 2026-10-05) : il doit en être informé avec le chiffre avant le lancement de P2. | avant le brief de P2 |
| R-4 | La CLOTURE §5 note que la forge ne lance pas les jobs, et que la poignée TLS réelle et la tenue sur des semaines ne sont pas éprouvées. Les deux derniers ont leurs items (TLS-REUSSI-1 en B.63 cité par la G2 §8 ; rodage de 14 jours, Q-C-06). L'exécution réelle des jobs par la forge n'apparaît dans aucun item de B.71 : si aucun item existant ne la porte, en former un, car G3/G4/G6 bloquants (CLAUDE.md point 3) n'existent qu'une fois les jobs lancés par la forge. | avant le gel du collecteur |

## Risques acceptés avec cet accord

- Journal neuf rendu illisible si la toute première écriture est coupée (22 graines sur 300 sous coupures ; B.71 item
  PREMIERE-ECRITURE-1) : accepté parce que porté par une procédure d'intervention (DB-6, A-7) et une décision au gel.
- Aucune configuration de production scellée (E-C-11, E-C-27, E-C-28 ; G2 §1 « exigences sans test » ; B.71
  CONFIG-PRODUCTION-1) : accepté parce que les valeurs ne servent qu'au gel ; mais le gel ne doit pas être prononcé sans.
- Suite S2 rouge sous Python 3.10 (item PY310-1, G2 §6) : connu, hors P1.
- Après le gel, toute correction du chemin de lecture ou du journal refait le rodage de 14 jours (CLOTURE §5) : c'est
  la raison pour laquelle R-1 et R-4 doivent être tenues avant, pas après.
