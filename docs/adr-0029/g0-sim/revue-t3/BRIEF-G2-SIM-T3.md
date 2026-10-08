# Brief — relecture G2 du lot SIM-BIS, tranche 3 (SB-4I, SB-6A à SB-8C : observateurs et règle)

Tu es **réviseur G2 neuf** (`shogen-worker`) : tu n'as rien écrit de ce lot.

Cadre :
- le dépôt `/home/user/shogen` est en lecture seule, **aucune opération git en écriture** ; utilise `git --no-optional-locks`, car d'autres agents y travaillent ;
- lis `date -u` avant toute date ;
- tu écris seulement dans `<scratchpad>/s2bis/sim3/g2/`, rapport par message ;
- **place disque comptée** : supprime tes copies et tes cibles à la fin.

## Pièces
- Neuf diffs, dans l'ordre : `…/sim3/diffs/SB-4I.diff`, SB-6A, SB-6B, SB-6C, SB-7A, SB-7B, SB-8A, SB-8B, SB-8C (empreintes `…/sim3/SHA256SUMS`).
- Rapport du worker transcrit : `…/sim3/g2/RAPPORT-WORKER-SIM-T3-transcrit.md`.
- Brief du worker : `…/sim3/BRIEF-SIM-T3.md`, et les deux ajouts décrits dans le rapport.
- Outils et preuves : `…/sim3/outils/`, `…/sim3/journal/`.

Base : la tête du dépôt (3164348, où la tranche 2 est commise), puis les neuf diffs. Le worker affirme qu'ils s'y appliquent : vérifie-le.

## Contrat
- G0 `docs/adr-0029/g0-sim/G0-SIM-BIS.md` avec son ajout daté ; son contenu est `PROPOSITION.md`, corrigé par `AVIS.md`.
- ADR-0029.
- Pièces de revue : `docs/adr-0029/g0-sim/revue-t1/` et `revue-t2/`.
- Contrat de rotation du recalcul, non commis et en correction G2 : diffs `…/s2bis/rb1/diffs/RB-6a.diff` et `RB-6b.diff` (`ROTATION-S2BIS.md`).

Un avis de l'advisor sur les seize questions Q-T3-1 à Q-T3-16 est demandé en parallèle. Toi, juge **la fidélité au G0 et la justesse du code**.

## Contrôles
1. **Série**
   - Application sur la tête, chaque diff à au plus 200 lignes de code ajoutées.
   - Chaque état vert seul, à son plancher exact, par la commande du job : runner d'abord, puis la ligne de `gates.yml`.
2. **Conformité, exigence par exigence** : toutes celles que la proposition rattache à SB-6, SB-7 et SB-8, plus O-A et O-B de la tranche 2 pour SB-4I.
3. **Justesse, par des calculs indépendants du code**
   - Consolidation et quorum q_j recalculés à la main sur de petits cas.
   - Rotation, K, S, C, K_crit et seuil recalculés sans importer le code, les six vecteurs de RB-6 compris.
   - Arrêt anticipé contre R complet, par ton propre oracle sur des instances aléatoires.
   - Séquence d'ETH, F3, compte d'événements et critère d'absorption sur des cas construits.
   - Monte Carlo indépendant à graine fixe : les taux des processus des observateurs (absences, dégradations, défauts locaux, pannes de paires, artefacts, pannes régionales) s'accordent à leurs paramètres à quelques erreurs-types.
4. **Identité bit à bit** : graines, PYTHONHASHSEED, Python 3.10 à 3.13. Reproduis les empreintes déclarées, dont la nouvelle empreinte de la tranche 2 après SB-4I. Pour SB-4I : stabilité de l'état des autres hôtes quand le pool est réordonné ou réduit, avec dérives.
5. **Mutants**
   - Rouge et vert rejoués sur au moins trois pas.
   - Au moins quinze mutants à toi, classés par la commande du job, avec une borne de temps ; un dépassement est FATAL.
   - Rejoue un échantillon d'au moins vingt mutants du worker.
6. **CI** : aucune gate affaiblie.
7. **Règles et vérification** : R-13, R-8, octets 92, garde `ast` (LIBM-POW-1) appliquée aux nouveaux modules ; `cargo --locked xtask verify` sur une copie (lignes de verdict seules ; S-G9 `docs/17:70` est connu).
8. **Écarts E-1 à E-9 et items P-1 à P-9** : avis motivé. **E-6** : le worker a lu son propre journal de session `.jsonl`. Dis si cela a pu exposer une pièce interdite, au vu de ce qu'il en a extrait.

## Exécution
- Copies : `git archive` avec les exclusions `docs/rapports`, `docs/adr-0025`, `docs/adr-0028/monark-m009a`, `docs/adr-0028/execution`, `docs/15-*`, `docs/16-*` et `docs/pocket-report`.
- `TMPDIR` dédié.
- Réseau isolé : `unshare -n`, avec `lo` allumée par `…/s2bis/p1b/g2/travail/lo_up.py` et `isole.sh`.
- D'autres agents tournent sur la machine : ne tue que tes propres processus.

## Interdits
- les dossiers exclus des copies ;
- tout `*.jsonl` ;
- toute pièce de D.2 ;
- **toute recherche récursive (grep -r, git grep, du, find large) sur `docs/`, sur le dépôt entier ou sur le scratchpad entier**.

Verdict : ACCEPTE, ACCEPTE-AVEC-CORRECTIONS (liste fermée) ou REFUSE.
Gate 0 : l'identifiant exact du modèle en tête du rapport. Résumé court en français.
