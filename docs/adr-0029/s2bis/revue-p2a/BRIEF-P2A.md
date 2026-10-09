# Brief — partie P2 du collecteur de S2-bis, tranche A : CB-6 (décodeurs BTC), CB-12 (relevé ASN), CB-13 (processus secondaire)

Worker `shogen-worker`, effort max. Tu travailles dans `<scratchpad>/s2bis/p2a/` (scratchpad = `<scratchpad>`), avec `TMPDIR` et une cible cargo dédiés, `NOTES.md` tenu (reprise depuis lui, jamais depuis un `.jsonl`). Dépôt `/home/user/shogen` en lecture seule : **aucune opération git en écriture**. Lis `date -u` avant toute date. Base : copie de la tête **5cfe746** (`git archive`, exclusions : `docs/rapports`, `docs/adr-0025`, `docs/adr-0028/monark-m009a`, `docs/adr-0028/execution`, `docs/15-*`, `docs/16-*`, `docs/pocket-report`). La partie P1 y est commise et close (accord sous réserves, réserve R-1 tenue, outillage OUT-2 commis).

Contrat : le G0 `docs/adr-0029/g0-collecte/G0-COLLECTE-RECALC-DEPLOI.md` et ses ajouts datés, dont le contenu est `PROPOSITION.md` corrigé par `AVIS.md`, qui prime ; ADR-0029 et ses ajouts datés ; FORMAT `docs/adr-0029/s2bis/FORMAT-JOURNAUX-S2BIS.md` (le champ `valeurs` l.310 et ce qui s'y rattache) ; pièces de revue de P1 (`docs/adr-0029/s2bis/revue-p1a/`, `revue-p1b/`, `revue-p1c/`, `revue-p1-integ/`) pour la forme des diffs et des tests.
- **CB-6** (PROPOSITION l.214) : décodeurs BTC repris du harnais de S2 (`s2-harness/`, lis-les en entier), fixtures reprises, formes BTC, contrôle de finitude ; branchement dans la lecture de P1 sans flottant.
- **CB-12** (l.220) : relevé ASN (A propre, RIPEstat, Cymru), sur le client DNS filaire de CB-10 ; les items de déclencheur « G0 de CB-12 » (SHOGEN-S2BIS-DNS-TC-1, SHOGEN-S2BIS-DNS-ID-16BITS-1, et tout autre) sont fermés ici.
- **CB-13** (l.221) : processus secondaire (carte et ASN) : journal propre, isolement, budget de débit partagé.
- Lis aussi PROPOSITION §2.2 (exigences), §2.4 (tests et mutants obligatoires) et §2.6 (risques), et AVIS sur ces points.

Règles communes (identiques à la partie P1) :
- **tests d'abord** : un rouge d'assertion montré avant le code, puis le vert ;
- **mutants** : au moins dix par sous-lot, **classés par la commande du job** (runner d'abord, puis la ligne s2bis de `gates.yml`, suite entière, borne de 300 s ; dépassement = FATAL, jamais « tué » ; SHOGEN-S2BIS-MUT-COMMANDE-1) ; verse tous les mutants que tu cites ;
- **bibliothèque standard seule** (R-8) ; R-13 ; aucun flottant dans un journal (SHOGEN-S2BIS-ECRIVAIN-REFUS-ARRET-1 : lis-le) ;
- **diffs en série** : chacun ≤ 200 lignes de code ajoutées (R-25), plancher exact du job s2bis relevé à chaque diff (`--egal`), section METRIQUES (`docs/adr-0029/s2bis/METRIQUES-S2BIS.md`) par diff, dans la forme des diffs de P1 ;
- **aucune opération réseau** : `unshare -n` avec `lo` allumée (`<scratchpad>/s2bis/p1b/g2/travail/outils/isole.sh`, `env -u SHOGEN_S2_CAMPAGNE_CONTROL`) ; aucun appel réel à une API : fixtures seulement ;
- Python 3.10 à 3.13 en `-X dev -W error` (critère de vert : code 0, aucune ligne « Exception ignored » ni « Warning ») ; aucun `__pycache__` laissé dans une racine de suite (le vérificateur le refuse désormais) ;
- avant livraison : runner (136 cas), jobs s2bis, S2 (415) et sim-bis aux planchers exacts ; `cargo --locked xtask verify` sur la copie : lignes de verdict seules ; S-G9 `docs/17:70` est connu sur les copies ;
- journal G1 dans le rapport ([lu], [2nd], [abs]) ; SHA256SUMS couvrant ton rapport ; estimation révisée des sous-lots restants de P2 ;
- **nettoie tes copies lourdes à la fin** (disque partagé avec d'autres workers).

Items de l'annexe B : lis `docs/adr-0028/ANNEXE-B-items.md` par recherche **dans ce seul fichier** des noms de tes sous-lots dans la colonne « déclencheur » ; chaque item dont le déclencheur est l'un de tes sous-lots (ou « G0 de CB-x » pour l'un d'eux) est **fermé dans ton lot**, chacun avec un test nommé, ou rendu en question s'il demande une décision de valeur.

Interdits :
- `docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, `docs/adr-0028/execution/` ;
- tout `*.jsonl` réel ; toute pièce de D.2 ; ne jamais poser `SHOGEN_S2_CAMPAGNE_CONTROL` ;
- **aucune recherche ou énumération récursive (grep -r, git grep, git ls-tree -r, du, find large) sur `docs/`, sur le dépôt entier ni sur le scratchpad entier**, même sur tes copies ;
- aucun fichier sous un `.claude/` du dépôt réel ; rien sur Pocket.

Un autre worker travaille en parallèle sur une autre tranche de P2, et l'orchestrateur committe dans le dépôt pendant ton lot : ne prends pas de verrou git (`git --no-optional-locks`). Gate 0 : l'identifiant exact du modèle en tête. Rapport final par message (ta valeur de retour), court, en français ; écris-le aussi dans ton dossier (`RAPPORT-GENERATEUR.md`), couvert par ton SHA256SUMS.
