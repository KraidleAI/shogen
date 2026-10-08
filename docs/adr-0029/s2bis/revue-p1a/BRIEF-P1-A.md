# Brief — partie P1 du collecteur de S2-bis, sous-lots CB-0, CB-1, CB-2

Worker `shogen-worker`, effort max. Dépôt `/home/user/shogen`, branche `claude/compassionate-noether-szmdyj` (lecture seule ;
**aucune opération git en écriture**). Lis `date -u` avant toute date. Tu travailles sur une copie (`git archive HEAD | tar -x -C
<dossier>/arbre --exclude=docs/rapports --exclude=docs/adr-0025 --exclude=docs/adr-0028/monark-m009a --exclude='docs/15-*'
--exclude='docs/16-*' --exclude=docs/pocket-report`) dans `<scratchpad>/s2bis/p1/` ;
`TMPDIR` dans ce dossier ; cible cargo dédiée si tu lances `xtask`.

Contrat : **G0 `docs/adr-0029/g0-collecte/G0-COLLECTE-RECALC-DEPLOI.md`** (lis-le), qui fait de la proposition
(`docs/adr-0029/g0-collecte/PROPOSITION.md`) le contenu du G0, corrigée par l'avis (`docs/adr-0029/g0-collecte/AVIS.md`, qui prime
question par question) ; ADR-0029 (acceptée, avec ses ajouts datés). Sous-lots de ce brief : **CB-0** (squelette du paquet `s2bis/`,
CI, plancher de tests, fonctions de fitness), **CB-1** (écrivain chaîné, fsync, verrou exclusif), **CB-2** (fichiers quotidiens,
reprise, trous) : périmètre, exigences numérotées, tests et mutants obligatoires tels qu'écrits à la proposition pour ces sous-lots.

Règles : tests d'abord (rouge avant, vert après) ; mutants (au moins dix par sous-lot, contrat du lanceur 0/1/3 : vivant/tué/FATAL) ;
bibliothèque standard Python seule, version fixée par la proposition (R-8 : aucune dépendance nouvelle sans vérification au registre
avant installation, et décision de l'orchestrateur) ; chaque diff ≤ 200 lignes ajoutées (R-25), s'appliquant en série sur la tête du
moment ; R-13 ; `s2-harness/` intouché ; si CB-0 touche `.github/workflows/` ou `enforcement/`, rien n'est affaibli ; journal G1
(lectures avec niveau, exigences couvertes ligne par ligne, rouge/vert, mutants, écarts, questions) ; SHA256SUMS.
Aucune lecture de journal de campagne, aucun réseau requis. Interdits : `docs/15-*`, `docs/16-*`, `docs/pocket-report/`,
`docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, tout `*.jsonl` réel, toute pièce de D.2 ; aucune recherche récursive
sur tout `docs/` ; sortie de `cargo xtask verify` redirigée, lignes de verdict seules. Gate 0 (identifiant exact). Résumé court en français.
