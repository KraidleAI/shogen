# Brief — proposition de G0 pour le lot SIM-BIS (SIM-NIVEAU-BIS ‖ SIM-PUISSANCE-BIS), sans code

Rédacteur `shogen-worker`, effort max. Dépôt `/home/user/shogen` (lecture seule ; **aucune opération git en écriture** ; aucun code).
Lis `date -u` avant toute date. Tu écris seulement dans
`<scratchpad>/s2bis/sim-g0/` (sortie `PROPOSITION-G0-SIM-BIS.md`).

Modèle à suivre (forme, rigueur, numérotation des exigences, questions techniques) : `docs/adr-0029/g0-collecte/PROPOSITION.md`,
`AVIS.md` et `G0-COLLECTE-RECALC-DEPLOI.md`. Rattachements à lire : ADR-0029 (révision 3, acceptée, avec ses ajouts datés) — §2.2 à
§2.7 (en particulier §2.4 points (d), (e), (g), (h) ; §2.7 points 2, 5 à 9), §6 lot 4 (l. ~382), §8 (items SHOGEN-S2BIS-SIM-1,
SHOGEN-S2BIS-ROTATION-SOURCE-1) ; `docs/adr-0029/G0-lots-S2BIS.md` (ligne SIM-BIS) ; sorties du lot PLAN-S2BIS
`docs/adr-0029/plan-s2bis/` (README, `tau_sigma.txt`, `episodes.txt` : épisodes et FIV_série(ℓ) destinés à SIM-BIS, `okx.txt`) et
`scripts/plan-s2bis/` ; `docs/adr-0029/AVIS-STATS.md`, `AVIS-QUESTIONS-TECHNIQUES-V3.md`, `DECISIONS-ARCHITECTURE-S2BIS.md`,
`CONTRE-EXPERTISE-DECISIONS.md` ; `docs/adr-0029/etude-marche/P6-MESURE.md` (§3.4, §3.6) ; items SHOGEN-FLUX-ABSORPTION-COLLECTIVE-1 et
SHOGEN-FLUX-SERIEL-1 dans `docs/adr-0028/ANNEXE-B-items.md` (cherche par `grep -n` dans ce fichier seul).

À produire : périmètre exact ; exigences numérotées (E-S-nn) : modèle génératif (couche d'observateurs, quorum 2/2-2/3-3/4, M_j
variable, défauts locaux non attrapés par D-2 à D-5, censure, épisodes hétérogènes jusqu'à plusieurs jours, séries à dérive),
calibration sur les sorties de PLAN-S2BIS (sans relire aucun journal de campagne), statistique K≥2 et S en sensibilité, rotation
enroulée et variante non enroulée de Harris, séquence d'ETH sous la loi jointe par hôte, fréquence de NON ÉVALUABLE (H0, cible, F3),
≥ 10⁴ réplications avec erreur-type, identité bit à bit de deux exécutions (graines, ordre, flottants), budget de calcul mesuré ;
ce qui fixe n_s et T_max et comment cela s'écrit au paquet ; règle pré-déclarée « niveau > 0,01 à deux erreurs-types → limite écrite,
rien ne change » ; sous-lots ≤ 200 lignes de code chacun, tests attendus (dont tests à valeurs écrites à la main et mutants),
bibliothèque standard seule ou dépendance justifiée (R-8 : vérification registre avant toute installation, dite, pas faite) ; où tourne
le calcul (aucune dépense sans acte de l'investisseur) ; dépendance aux sources de la méthode (item ROTATION-SOURCE, procuration en
cours en parallèle) ; critères de sortie ; questions techniques numérotées pour l'advisor, chacune avec options et recommandation.
Interdits : `docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`,
`docs/adr-0028/execution/`, tout `*.jsonl`, toute pièce de D.2 ; aucune recherche récursive (grep -r, git grep) sur `docs/`.
Gate 0 (identifiant exact en tête). Résumé court en français.
