# Briefs de CB-18v, CB-18w et CB-18x, et des contre-contrôles cc4 et cc5 (P1 tranche C, fetch-depth du job sim-bis)

> Réunis par l'orchestrateur. Les quatre briefs ont été donnés par message. Le premier est reproduit tel que le worker l'a consigné dans ses notes (`corr4/NOTES.md`, lignes 2 à 4) ; les trois suivants sont le texte des messages de l'orchestrateur.

## 1. CB-18v et CB-18w (worker ; consigné dans ses notes)

- 15:38:22 UTC (date -u) : message du coordinateur. Besoin : le job sim-bis-unittest extrait f35a70c (adaptateur r1) ; SB-14A ajoute `fetch-depth: 0` sous le with: du checkout de ce job (Q-T4-11, adjugée) ; le gabarit de K-03 le refuse (tête + série SIM-T4 : 76 ok, 1 échec). O-2 du relecteur de SIM-T4 : K-03 doit exiger la ligne dans ce job. Base : tête poussée 98c8537 (P1 complète). Dossier corr4, TMPDIR dédié. Série SIM-T4 : sim4/diffs (SB-9A à SB-14B), puis sim4/corr/diffs (SB-14C à SB-14H) ; gates.yml final : sim4/corr/etapes/e14h.
- Adjudication : CB-18v (avant SIM-T4) : le gabarit admet, pour le seul job sim-bis-unittest, `fetch-depth: 0` (valeur exacte) sous le with: du checkout, en plus de `persist-credentials: false` ; s2bis et S2 inchangés ; cas L : fetch-depth: 1 refusé, fetch-depth: 0 sur s2bis refusé, autre clé du with: refusée ; montrer tête >= 77 ok et tête + SIM-T4 complète verte au runner. CB-18w (après SIM-T4) : le gabarit exige `fetch-depth: 0` dans le job sim-bis (ferme O-2) ; cas L : ligne absente refusée ; montrer sur tête + SIM-T4 + CB-18v.
- Règles : tests d'abord (rouge montré) ; mutants par la commande du job ; aucun cas existant affaibli ; <= 200 lignes par diff ; Python 3.10 à 3.13 ; xtask ; SHA256SUMS ; nettoyage ; rapport par message. Dépôt en lecture seule (git --no-optional-locks) ; interdits inchangés.

## 2. Contre-contrôle cc4 (réviseur)

Contre-contrôle bref (cc4) de CB-18v et CB-18w (P1 tranche C, gabarit K-03 et fetch-depth du job sim-bis) : verdict CONFORME ou NON-CONFORME avec liste fermée. Pièces : rapport transcrit du worker `corr4/RAPPORT-CB18VW-transcrit.md` ; diffs CB-18v (8db2bfc9…) et CB-18w (15ec5079…), SHA256SUMS e64ebccd ; série SIM-T4 ; leurres du réviseur. Base : tête 98c8537. Adjudications : E-1 (L-41, ordre exact de la ligne) accepté, serrage ; E-2 (M-18r-04 réécrit) noté, à vérifier ; E-3, E-4 notés ; I-1 attendu, le G0 figé et SB-14H commis ensemble ; ordre de commit : CB-18v, série SIM-T4, versement, G0 figé + SB-14H, CB-18w. À contrôler : application et arbres ; runner 82 puis 83 ok, L-37 à L-42 rouges sous leur mutant, aucun cas retiré ni affaibli ; gabarit limité au job sim-bis-unittest, place et égalité exactes, jobs s2bis et S2 inchangés, leurres aux mêmes verdicts ; au moins deux mutants neufs du réviseur par la commande du job s2bis (300 s, FATAL) ; octets 92, R-13, 120 caractères, 200 lignes ; xtask ; isolement réseau. Interdits habituels.

## 3. CC4-1 (worker)

Adjudication : les cas sont ajoutés, et non relégués au résidu de validité. Diff CB-18x posé après CB-18w, CB-18v et CB-18w inchangés. L-43 (fetch-depth: 0 à l'indentation 8, refusé) et L-44 (la ligne après le nom de l'étape du runner, refusée ; libellé sous 120 caractères), écrits par le worker, le POC du réviseur servant de référence. Preuves : runner à 85 ok ; sous MV-02 seul L-43 échoue, sous MV-01 seul L-44 ; rouge : w plus chacun des deux mutants donne 83 ok sans les cas. Au moins deux mutants neufs du worker ; leurres aux mêmes verdicts ; octets 92, R-13, 120 caractères, METRIQUES ; xtask et runner sous 3.10 à 3.13 ; job s2bis Ran 184. Livrables : `corr4/diffs/CB-18x.diff`, SHA256SUMS, preuve d'arbre.

## 4. Contre-contrôle cc5 (réviseur)

Contre-contrôle bref de CB-18x (27310410…, SHA256SUMS de corr4 033561ff…) : application sur w sans décalage, arbres cd873376 et fe319805 ; runner 85 ok, MV-02 tué par L-43 seul et MV-01 par L-44 seul, aucune ligne de code du gabarit changée, aucun cas retiré ni affaibli ; M-18x-01 et M-18x-02 tués par le cas annoncé, leurres aux mêmes verdicts ; octets 92, R-13, 120 caractères, METRIQUES, xtask ; job s2bis Ran 184 sous isolement.
