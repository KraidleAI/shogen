# Brief — relecture G2 du lot SIM-BIS, tranche 2 (SB-3a à SB-4b, couche des sources)

Tu es **réviseur G2 neuf** (`shogen-worker`) : tu n'as rien écrit de ce lot. Dépôt `/home/user/shogen` (lecture seule ; **aucune
opération git en écriture**). Lis `date -u` avant toute date. Tu écris seulement dans
`<scratchpad>/s2bis/sim2/g2/` (rapport par message si le harnais refuse
le fichier). **Place disque comptée** : supprime tes copies et cibles en fin de passe.

Pièces : six diffs `…/sim2/diffs-784ebd2/` (empreintes `…/sim2/SHA256SUMS`) ; preuves `…/sim2/journal/`, outils `…/sim2/outils/` ;
rapport du worker transcrit `…/sim2/g2/RAPPORT-WORKER-SIM-T2-transcrit.md` ; brief `…/sim2/BRIEF-SIM-T2.md`. Contrat : G0
`docs/adr-0029/g0-sim/G0-SIM-BIS.md` avec ses ajouts datés (contenu `PROPOSITION.md` corrigé par `AVIS.md`) ; ADR-0029 ; sorties de
PLAN-S2BIS ; relecture de la tranche 1 `docs/adr-0029/g0-sim/revue-t1/` (modèle de forme). Un avis de l'advisor sur les douze questions
de conception Q-T2-1 à Q-T2-12 est demandé en parallèle : toi, juge la **fidélité au G0 et la justesse du code**.

Contrôles : (1) application en série sur la tête actuelle, ≤ 200 lignes de code par diff, arbre = empreintes, chaque état vert seul à
plancher exact ; (2) conformité exigence par exigence (E-S-07 à E-S-16, E-S-39 et toutes celles que la proposition rattache à SB-3 et
SB-4) ; (3) **justesse statistique, par des calculs indépendants du code** : loi résiduelle P(R=k)=P(L≥k)/E[L] et stationnarité du
renouvellement alterné (vérifie sur un petit cas, à la main ou en `Fraction`, que la probabilité d'être en épisode à un instant donné
vaut le taux marginal) ; taux marginal et κ du régime E ∪ (E′∩Z) exacts ; amincissement des dérives ; incidents (taux ρ·w/86 400, k
parmi sans remise) ; vérifie aussi par une simulation Monte Carlo indépendante, à graine fixe, que les taux empiriques produits par le
code s'accordent aux taux visés à quelques erreurs-types ; (4) identité bit à bit (graines, PYTHONHASHSEED, 3.10 à 3.13) ;
(5) rouge/vert rejoués sur au moins trois pas ; au moins quinze mutants à toi, **classés par la commande du job (runner d'abord, ligne
de `gates.yml`), borne de temps, dépassement = FATAL** ; (6) CI : aucune gate affaiblie ; nouveau `test_fitness_tirages.py` ;
(7) R-13, R-8 ; `cargo --locked xtask verify` sur une copie (lignes de verdict seules ; S-G9 `docs/17:70` connu) ; (8) écarts E-1 à
E-13 et items proposés : avis motivé. Copies : `git archive HEAD | tar -x -C <dossier> --exclude=docs/rapports --exclude=docs/adr-0025
--exclude=docs/adr-0028/monark-m009a --exclude='docs/15-*' --exclude='docs/16-*' --exclude=docs/pocket-report` ; `TMPDIR` dédié ;
la suite s2bis se lance sans `unshare` (sa garde suffit ; sous `unshare -n`, `lo` est éteinte). Interdits : ces dossiers,
`docs/adr-0028/execution/`, tout `*.jsonl` réel, toute pièce de D.2 ; **aucune recherche récursive (grep -r, git grep, du, find
large) sur `docs/`, le dépôt entier ou le scratchpad entier**. Verdict : ACCEPTE, ACCEPTE-AVEC-CORRECTIONS (liste fermée) ou REFUSE.
Gate 0 (identifiant exact). Résumé court en français.
