# Brief — corrections G2 de la tranche C de P1 du collecteur (diffs CB-18g, CB-18h…, après ENTIER-ECRIVAIN)

Worker `shogen-worker`, effort max.

- Dépôt `/home/user/shogen` en lecture seule : **aucune opération git en écriture**. L'orchestrateur y committe pendant ton lot : lis avec `git --no-optional-locks`.
- Lis `date -u` avant toute date.
- Tu travailles dans `<scratchpad>/s2bis/cb18/corr/`, avec un `TMPDIR` dédié.

**Base** : copie de **3164348** par `git archive` (exclusions habituelles : `docs/rapports`, `docs/adr-0025`, `docs/adr-0028/monark-m009a`, `docs/adr-0028/execution`, `docs/15-*`, `docs/16-*`, `docs/pocket-report`). Puis les neuf diffs `…/cb18/diffs/`, en série, contrôlés par `…/cb18/SHA256SUMS` : CB-18a à CB-18f, ENREG-ROLE, SEGMENT-JOUR, ENTIER-ECRIVAIN.

L'orchestrateur committe en ce moment la tranche 1 du recalcul (`recalc/`, plancher s2bis à 156). Il recalera tes diffs sur le plancher en les commitant. Toi, travaille sur 3164348.

**Pièces** :
- relecture G2 : `…/cb18/g2/G2-CB18-transcrit.md` (ACCEPTE-AVEC-CORRECTIONS, liste fermée C-1 à C-4) ;
- outils, mutants MR-01 à MR-26, sondes (`sonde_budget.py`, `contournement_role.py`, `scenarios_jour.py`…) et preuves du réviseur : `…/cb18/g2/travail/` ;
- ton rapport précédent : `…/cb18/g2/RAPPORT-WORKER-CB18-transcrit.md`.

**Contrat** : G0 `docs/adr-0029/g0-collecte/G0-COLLECTE-RECALC-DEPLOI.md`, ADR-0029, FORMAT.

## Adjudications de l'orchestrateur (liste fermée de ce lot)

- **C-1 (budget)** : la forme proposée par le réviseur est adoptée.
  - Champ scellé `tolerance` (µs) dans `formes.json` : 5 s en production, porté par `run_params`.
  - Règle : `tolerance + plus grand décalage + délai + marge ≤ delta`.
  - FORMAT §14.1 et §14.4 mis à jour.
  - Test à la borne : égalité admise, 1 µs de plus refusée (tue MR-17). Rejoue `sonde_budget.py`.
- **C-2 (ENREG-ROLE)** : cas où la ligne du vérificateur de s2bis ne figure que dans un job suivant. Refus avant toute écriture. Rouge montré avec MR-24.
- **C-3 (METRIQUES)** : `boucle.py` fait 132 lignes, recompte toi-même. C-4 (biblio) revient à l'orchestrateur.
- **SHOGEN-S2BIS-LIGNE-JOB-LEURRE-1, fermé dans ce lot.**
  - Un seul analyseur lit la ligne d'un job dans les seuls blocs `run:` des étapes, en excluant les étapes `if:` et `continue-on-error`.
  - Il est partagé par K-01 à K-03 du runner (`enforcement/tests/run-fixtures-verdict-suite-s2.py` et ce qu'il appelle) et par `ligne_du_job` de `oracle_record`.
  - Les leurres C1 (`name: >`) et C4 (`if: false`) du réviseur doivent être refusés par les deux. Rejoue `contournement_role.py`.
  - C'est un serrage de gate : aucun cas existant du runner ne doit être affaibli, et le compte des cas monte.
- **`--egal` pour le job S2** : adopté, si c'est tenable.
  - Étends `--egal` à la ligne du job `s2-harness-unittest`, plancher exact 406.
  - Retouche la regex de K-01.
  - Vérifie le couplage avec le test de comptes de B-SEG-1 (raison de l'adjudication Q-2 de B.60 ; G2-P1A l.296-306). Si le couplage rend `--egal` intenable, ne le fais pas : écris pourquoi, ce sera un item.
  - Tue MR-25.
- **SHOGEN-S2BIS-TEST-DISQUE-INSTABLE-1** : injecte `statvfs` dans le test, ou ne compare que `total`. Le test doit devenir déterministe.
- **SHOGEN-S2BIS-CONFIG-REGLES-1** :
  - `places` ≥ nombre de formes ;
  - forme de `hote` : même règle `[a-z0-9.-]{1,253}` que le recalcul (Q-RB-13) ;
  - forme de `chemin` ;
  - commit hexadécimal en minuscules (tue MR-22) ;
  - test à la borne du délai des sondes (tue MR-18).
- **SHOGEN-S2BIS-SEGMENTS-10-1** : un test à 10 segments ou plus d'un même jour, qui tue MR-26. Le format des noms ne change pas dans ce lot : un nom sur 3 chiffres sera tranché avant le gel, comme item.
- **MR-09** : ajoute un cas tuple au test des 640 chiffres.
- **CITATIONS-ADR-DECALEES-1** : écris dans l'en-tête du FORMAT la convention des citations « ADR-0029 l.N ». Elles suivent l'ADR au commit e16956b, convention du G0. Corrige toute citation qui ne la suit pas.
- **FORMAT §11.5** : place `run_params` dans l'ordre de la première fenêtre d'une exécution.

**Restent en items, sans code dans ce lot** :
- RUNPARAMS-CALENDRIER-1 (gel) ;
- ECRIVAIN-REFUS-ARRET-1 (G0 de CB-6) ;
- SIGTERM sans `finally` (DB-3) ;
- PY310-1 (Python minimal de s2-harness et du recalcul, au G0 de RB-2) ;
- LIRE-BOOLEENS (avant le gel, des deux côtés) ;
- nom de segment sur 3 chiffres (avant le gel).

## Règles

- **Tests d'abord**, avec le rouge montré avant le code.
- **Mutants**, rejoués par la commande du job (runner, puis ligne de `gates.yml`, borne de 300 s ; dépassement = FATAL) :
  - les 26 mutants du réviseur : tout vivant meurt, sauf MR-09 si le tuple reste hors du domaine, à justifier ;
  - un échantillon de 20 de tes mutants ;
  - au moins dix mutants neufs, dont des leurres neufs contre l'analyseur.
- **Bibliothèque standard seule.**
- **Diffs en série**, **chacun ≤ 200 lignes de code ajoutées**, plancher exact relevé à chaque diff.
- **Python** 3.10 à 3.13 en `-X dev -W error` (s2bis).
- R-13, R-8, octets 92 comptés.
- **Isolement réseau** : `unshare -n` avec `lo` allumée (`…/p1b/g2/travail/outils/isole.sh`).
- **xtask** : `cargo --locked xtask verify` sur la copie, lignes de verdict seules ; S-G9 `docs/17:70` est connu.
- **Livrables** : journal G1 et SHA256SUMS.
- **Machine partagée** : consigne le PID réel ; pas de `pgrep -f` sur un motif large ; nettoie tes copies lourdes à la fin.
- **Après un compactage** : reprends depuis un fichier de notes tenu dans ton dossier, jamais depuis un `.jsonl`.

## Interdits

- `docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, `docs/adr-0028/execution/` ;
- tout `*.jsonl` ;
- toute pièce de D.2 ;
- **toute recherche récursive (grep -r, git grep, du, find large) sur `docs/`, sur le dépôt entier ou sur le scratchpad entier**.

Rapport par message. Gate 0 : l'identifiant exact du modèle en tête. Résumé court en français, point par point.
