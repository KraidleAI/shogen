# Brief — corrections G2 de la tranche B du collecteur de S2-bis (diffs CB-11c, CB-11d…, après CB-11b)

Worker `shogen-worker`, effort max. Dépôt `/home/user/shogen` (lecture seule ; **aucune opération git en écriture**). Lis `date -u`
avant toute date. Tu travailles dans `<scratchpad>/s2bis/p1b/corr/` ;
`TMPDIR` et cible cargo dédiés.

Base : copie de la tête (`git archive HEAD | tar -x …`, exclusions : `docs/rapports`, `docs/adr-0025`, `docs/adr-0028/monark-m009a`,
`docs/15-*`, `docs/16-*`, `docs/pocket-report`) + les huit diffs `…/p1b/diffs/CB-3a.diff` … `CB-11b.diff` appliqués en série.

Relecture G2 : `…/p1b/g2/G2-P1B-transcrit.md` (ACCEPTE-AVEC-CORRECTIONS, liste fermée **C-1 à C-7**) ; pièces et outils du réviseur
dans `…/p1b/g2/travail/` (sondes `outils/` ou `sondes_*.py`, mutants `mutants_g2.py`, `mutants_g2_b.py`, lanceur `campagne_g2.py`,
`mutants_lp_rejoues.py` ; repère-les par leur nom, sans recherche récursive large). Rapport du worker : `…/p1b/g2/RAPPORT-WORKER-P1B-transcrit.md`.
Contrat : G0 `docs/adr-0029/g0-collecte/G0-COLLECTE-RECALC-DEPLOI.md` (contenu `PROPOSITION.md`, corrigé par `AVIS.md`) ; ADR-0029.

Adjudications de l'orchestrateur : **C-1** : pour une lecture non finie à l'échéance, `fin` = E (FORMAT §11.4 aligné), état relevé une
seule fois à E avant toute écriture. **C-3 (a)** : armer `CONTEXTE` comme le contexte d'urllib (ALPN `http/1.1`, `post_handshake_auth`),
continuité avec S2 ; mesurer la ClientHello avant/après comme le réviseur. **C-6** et item neuf SHOGEN-S2BIS-MUT-COMMANDE-1 : toutes tes
campagnes de mutants se classent par la **commande du job** (suite entière, ligne de `gates.yml`), avec une borne de temps ; un dépassement
de borne est FATAL, jamais « tué ». C-2, C-4, C-5, C-7 telles qu'écrites. Observations O-5 et O-7 : à corriger si cela tient dans le
budget, sinon item. Questions du worker : réponses du réviseur adoptées (Q2 : motif de l'écart ThreadPoolExecutor consigné au JOURNAL).

Règles : tests d'abord (rouge sur la base, vert après) ; rejoue les deux jeux de mutants du réviseur et les M-LP du worker par la commande
du job : tout vivant non équivalent listé en C-7 meurt, M-LP-3 sort tué en temps borné ; bibliothèque standard seule ; diffs en série,
**chacun ≤ 200 lignes de code ajoutées**, plancher exact relevé à chaque diff ; R-13, R-8 ; aucune opération réseau (`unshare -n`) ;
`cargo --locked xtask verify` sur la copie (lignes de verdict seules ; S-G9 `docs/17:70` connu) ; journal G1 dans le rapport ;
SHA256SUMS. Interdits : `docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`,
`docs/adr-0028/monark-m009a/`, `docs/adr-0028/execution/`, tout `*.jsonl` réel, toute pièce de D.2 ; **aucune recherche récursive
(grep -r, git grep, du, find large) sur `docs/`, sur le dépôt entier ni sur le scratchpad entier**. Rapport par message si le harnais
refuse le fichier. Gate 0 (identifiant exact en tête). Résumé court en français, C-n par C-n.
