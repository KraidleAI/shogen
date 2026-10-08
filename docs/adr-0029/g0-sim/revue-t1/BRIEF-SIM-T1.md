# Brief — lot SIM-BIS, tranche 1 : sous-lots SB-0, SB-1, SB-2, SB-5

Worker `shogen-worker`, effort max. Dépôt `/home/user/shogen` (lecture seule ; **aucune opération git en écriture**). Lis `date -u`
avant toute date. Tu travailles dans `<scratchpad>/s2bis/sim1/` ;
`TMPDIR` dédié. Base : `git archive HEAD | tar -x …` (exclusions habituelles : `docs/rapports`, `docs/adr-0025`,
`docs/adr-0028/monark-m009a`, `docs/15-*`, `docs/16-*`, `docs/pocket-report`).

Contrat : **G0 `docs/adr-0029/g0-sim/G0-SIM-BIS.md`** — son contenu est `PROPOSITION.md` (même dossier) corrigée par `AVIS.md`, qui
prime ; ADR-0029 avec ses ajouts datés (dont celui du G0 SIM-BIS). Sous-lots de cette tranche (proposition §6.1) : **SB-0** (socle :
`parametres.json` et son schéma, `commun.py`), **SB-1** (`aleas.py` : flux SHA-256, tables de seuils exactes, tirages), **SB-2**
(`calibration.py` : lecture des sorties de PLAN-S2BIS en rationnels exacts), **SB-5** (`calendrier.py` : strates, compression, n_s,
T_max, runs ; test croisé avec `window`). Emplacement : celui que fixe la proposition (`scripts/sim-bis/` ou autre, tel qu'écrit).
Exigences E-S-nn concernées : celles que la proposition rattache à ces sous-lots ; tests du §6.2 (valeurs de référence écrites à la
main, indépendantes du code) ; identité bit à bit (E-S sur graines et flottants) ; aucune libm là où E-S-43 l'exclut.

Règles : tests d'abord (rouge avant, vert après) ; au moins dix mutants par sous-lot (contrat 0/1/3, copie fraîche par mutant) ;
bibliothèque standard seule ; **un diff par sous-lot, ≤ 200 lignes de code ajoutées, s'appliquant en série sur la tête** ; R-13 ; R-8 ;
aucune opération réseau ; aucune lecture de journal de campagne (seules les sorties versées de PLAN-S2BIS, `docs/adr-0029/plan-s2bis/`) ;
`SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée ; si un job CI est prévu par la proposition, l'écrire avec un plancher exact ;
`cargo --locked xtask verify` sur la copie (lignes de verdict seules ; S-G9 `docs/17:70` connu sur une copie). Journal G1 dans le
rapport ; SHA256SUMS ; questions ouvertes ; estimation révisée des sous-lots restants. Interdits : `docs/15-*`, `docs/16-*`,
`docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, `docs/adr-0028/execution/`, tout `*.jsonl`
réel, toute pièce de D.2 ; aucune recherche récursive sur `docs/`. Gate 0 (identifiant exact en tête). Rapport
`RAPPORT-WORKER-SIM-T1.md` (ou par message si le harnais refuse le fichier) ; résumé court en français.
