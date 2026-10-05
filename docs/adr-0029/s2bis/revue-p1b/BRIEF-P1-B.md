# Brief — partie P1 du collecteur de S2-bis, tranche B : sous-lots CB-3, CB-4, CB-5, CB-10, CB-11

Worker `shogen-worker`, effort max. Dépôt `/home/user/shogen` (lecture seule ; **aucune opération git en écriture**). Lis `date -u`
avant toute date. Tu travailles dans `<scratchpad>/s2bis/p1b/` ;
`TMPDIR` et cible cargo dédiés.

**Base** : copie de la tête (`git archive HEAD | tar -x …` avec les exclusions habituelles : `docs/rapports`, `docs/adr-0025`,
`docs/adr-0028/monark-m009a`, `docs/15-*`, `docs/16-*`, `docs/pocket-report`), **plus** la tranche A non encore commise : les sept
diffs `…/s2bis/p1/diffs/CB-0a.diff` à `CB-2c.diff`, appliqués en série (`git apply`). La tranche A est en relecture G2 : si elle
change, tu reporteras ; tes diffs s'appliquent après les siens.

Contrat : G0 `docs/adr-0029/g0-collecte/G0-COLLECTE-RECALC-DEPLOI.md` (contenu : `PROPOSITION.md`, corrigée par `AVIS.md`, qui prime) ;
ADR-0029 (acceptée, avec ses ajouts datés, dont D-2 reformulée « plus de 5 s après son instant planifié »). Sous-lots : **CB-3** (client
HTTPS par phases, sous-types de panne), **CB-4** (boucle à échéance dure), **CB-5** (tests « lecture pendue » et leurs mutants),
**CB-10** (client DNS filaire), **CB-11** (santé D-2 à D-5). Contraintes connues de la tranche A : l'écrivain ne se partage pas entre fils
(format §5) ; garde réseau `ReseauInterdit` (boucle locale permise pour les serveurs factices) ; limites mesurées de la collecte de S2
(`read()` qui lève `ConnectionResetError` ; délai d'`urllib` qui ne borne pas la résolution DNS) : à fermer par construction.

Règles : tests d'abord (rouge avant, vert après) ; mutants (au moins dix par sous-lot, contrat 0/1/3) ; bibliothèque standard seule ;
chaque diff ≤ 200 lignes de code ajoutées, s'appliquant en série après la tranche A ; plancher du job `s2bis-unittest` relevé ; R-13,
R-8 ; aucune opération réseau hors boucle locale et cibles réservées de test ; journal G1 dans le rapport ; SHA256SUMS ; estimation
révisée des sous-lots restants de P1 (CB-18). Interdits : `docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`,
`docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, tout `*.jsonl` réel, toute pièce de D.2 ; aucune recherche récursive sur tout `docs/`.
Gate 0 (identifiant exact). Résumé court en français.
