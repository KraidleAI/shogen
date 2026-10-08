# Brief — corrections G2 et avis de la tranche 1 du recalcul de S2-bis (diffs RB-1d, RB-1e…, après RB-1c)

Worker `shogen-worker`, effort max. Le dépôt `/home/user/shogen` est en lecture seule : **aucune opération git en écriture**. Utilise `git --no-optional-locks` ; l'orchestrateur et d'autres workers y travaillent pendant ton lot. Lis `date -u` avant toute date. Tu travailles dans `<scratchpad>/s2bis/rb1/corr/`, avec un `TMPDIR` dédié.

**Base** :
- copie de la tête actuelle (`git archive` avec les exclusions habituelles : `docs/rapports`, `docs/adr-0025`, `docs/adr-0028/monark-m009a`, `docs/adr-0028/execution`, `docs/15-*`, `docs/16-*`, `docs/pocket-report`) ;
- puis les sept diffs `…/rb1/diffs/RB-0a.diff` … `RB-1c.diff`, appliqués en série, avec les sha256 de `…/rb1/SHA256SUMS`.

**Pièces** :
- relecture G2 : `…/rb1/g2/G2-RB-T1-transcrit.md` (ACCEPTE-AVEC-CORRECTIONS, liste fermée C-1 à C-4) ;
- outils, mutants G-1 à G-20 et preuves du réviseur : `…/rb1/g2/outils/` et `…/rb1/g2/preuves/` ;
- avis de l'advisor : `…/rb1/g2/AVIS-RB-T1.md` ;
- ton rapport précédent : `…/rb1/g2/RAPPORT-WORKER-RB-T1-transcrit.md`.

**Contrat** : le G0 `docs/adr-0029/g0-collecte/G0-COLLECTE-RECALC-DEPLOI.md` (PROPOSITION corrigée par l'AVIS), l'ADR-0029 et le FORMAT.

## Adjudications de l'orchestrateur (liste fermée de ce lot)

- **C-1** (σ des oracles par actif), **C-2** (six mutants vivants G-13 à G-20 à tuer, chacun par un cas, avec le rouge montré sous le mutant) et **C-3** (comptes de METRIQUES) : telles qu'écrites par le réviseur.
- **C-4** : corrige la docstring de `_integre` pour qu'elle dise exactement ce que le lecteur calcule. Ne change pas la valeur.
- **Q-RB-1** (avis, et O-4 du réviseur) : un test d'égalité du texte de la lecture JSON stricte copiée avec `collecte/config.py` l.20-46. Ce test échoue si l'une des deux copies change sans l'autre.
- **Q-RB-4** (avis modifié, et O-2 du réviseur), contrôles sourcés à l'ADR et refusés par nom :
  - planchers de τ des oracles poussés : ETH 0,75 %, stables 0,375 % (l.188) ;
  - grille de 0,05 % de τ de **BTC** seulement (l.181) ; la grille des autres actifs relève du G0 de CALIB-ACTIFS ;
  - σ(actif, classe) ≥ σ_BTC(classe) (l.189).
- **Q-RB-5** (avis modifié) : écris dans `ROTATION-S2BIS.md` la précision suivante : ordre strict des points de code sur les noms d'hôte de la configuration (précision de l.200) ; la première unité effective sera imprimée au rendu (item pour RB-15).
- **Q-RB-6** (avis modifié, et O-1 du réviseur) : R = 9 999 et seuil = 99 exacts au chargeur, avec la cohérence alpha gardée en seconde garde. Les tests à petit R passent par `lois()` directement.
- **Q-RB-12** (avis adopté) : écris dans `ROTATION-S2BIS.md` les six points de cohérence avec SIM-BIS, d'après l'AVIS §2 Q-RB-12 :
  - positions ;
  - identifiants des unités = noms d'hôte ;
  - première unité ;
  - R et seuil en paramètres ;
  - libellés de strate ;
  - masques ≤ 2^n.
- **Q-RB-13** (avis modifié, et O-3 du réviseur ; resserrement de la lettre, l'orchestrateur porte l'ajout daté au G0) : noms d'unité aux seuls caractères d'un nom d'hôte, en minuscules (lettres, chiffres, « - » et « . », au plus 253 caractères). Refus nommé.
- **Q-RB-14** : déclare, dans METRIQUES et dans la docstring des tests de rotation, le mutant dû « modulo n_s au lieu de n′_s » à RB-7.
- **O-6** : corrige le commentaire de `test_fitness.py` pour qu'il décrive la règle codée.
- **Restent en items, sans code dans ce lot** :
  - Q-RB-10 et N-2 (portée d'une rupture, monotonie de `ws` à travers les ruptures, fenêtre de `apres`) : RB-3 ;
  - Q-RB-15 (`LECTEUR/illisible`) : RB-2 ;
  - O-5 (causes de `queue_finale`) : RB-3 ;
  - I-4, I-5, I-6.
  - I-1 (borne de 640 chiffres à l'écriture) et N-1 (segment du jour) sont confiés au worker du collecteur.

## Règles

- **Tests d'abord**, avec le rouge montré avant le code pour chaque point.
- **Mutants** : rejoue par la commande du job (runner, puis ligne de `gates.yml`, borne de 300 s ; tout dépassement = FATAL) :
  - les 20 mutants du réviseur : tous tués ;
  - l'échantillon de 23 mutants du worker ;
  - au moins dix mutants neufs pour tes ajouts.
- **Assertions** : sur de grandes structures, elles doivent échouer vite (I-8).
- **Bibliothèque standard seule.**
- **Diffs** : en série, **chacun ≤ 200 lignes de code ajoutées**, plancher exact relevé à chaque diff.
- **Python** 3.10 à 3.13 en `-X dev -W error`. R-13 ; R-8 ; octets 92 contrôlés.
- **Réseau isolé** : `unshare -n`, avec `lo` allumée (`…/p1b/g2/travail/lo_up.py`, `isole.sh`).
- **xtask** : `cargo --locked xtask verify` sur la copie, lignes de verdict seules ; S-G9 `docs/17:70` est connu.
- **Livrables** : journal G1, SHA256SUMS.
- **Machine partagée** : ne tue que tes propres processus, et nettoie tes copies lourdes à la fin.

**Interdits** :
- `docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, `docs/adr-0028/execution/` ;
- tout `*.jsonl` réel ;
- toute pièce de D.2 ;
- **aucune recherche récursive (grep -r, git grep, du, find large) sur `docs/`, sur le dépôt entier ni sur le scratchpad entier**.

Rapport par message. Gate 0 : l'identifiant exact du modèle en tête. Résumé court en français, point par point.
