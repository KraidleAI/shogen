# Brief — corrections G2 de la tranche 1 du lot SIM-BIS (diff SB-5c, après SB-5b)

Worker `shogen-worker`, effort max. Dépôt `/home/user/shogen` (lecture seule ; **aucune opération git en écriture**). Lis `date -u`
avant toute date. Tu travailles dans `<scratchpad>/s2bis/sim1/corr/` ;
`TMPDIR` dédié. **Place disque comptée** : supprime tes copies et cibles cargo en fin de passe (garde diffs, preuves, SHA256SUMS).

Base : copie de la tête (`git archive HEAD | tar -x …`, exclusions : `docs/rapports`, `docs/adr-0025`, `docs/adr-0028/monark-m009a`,
`docs/15-*`, `docs/16-*`, `docs/pocket-report`) + les neuf diffs `…/sim1/diffs/` (SB-0A à SB-5B, ordre de `…/sim1/SHA256SUMS`).

Relecture G2 : `…/sim1/g2/G2-SIM-T1-transcrit.md` (liste fermée **C-1 à C-6**, à appliquer telle qu'écrite ; mutants du réviseur et
outils sous `…/sim1/g2/rev/`). Contrat : G0 `docs/adr-0029/g0-sim/G0-SIM-BIS.md`. C-6 : date du commit = date de ton `date -u` (le
commit suivra le jour même). Les observations O-1 et O-2 : corrige-les si cela tient dans le budget du diff, sinon laisse-les.

Règles : **rouge d'assertion consigné avant le code** (tests sur la base SB-5b : échec d'assertion, pas d'import), vert après ; rejoue
les mutants du réviseur (R-02, R-03, R-07, R-08, R-12, R-13, R-26, R-28, R-34 doivent mourir) et ceux du worker de la tranche 1, **par la
commande du job (suite entière, ligne de `gates.yml`), avec borne de temps** (dépassement = FATAL) ; un seul diff **SB-5c ≤ 200 lignes de
code ajoutées** (sinon SB-5c et SB-5d), plancher exact relevé ; bibliothèque standard seule ; R-13, R-8 ; aucune opération réseau (si tu
lances la suite s2bis sous `unshare -n`, `lo` y est éteinte : lance-la sans `unshare`, sous sa garde) ; `cargo --locked xtask verify` sur
la copie (lignes de verdict seules ; S-G9 `docs/17:70` connu). Interdits : `docs/15-*`, `docs/16-*`, `docs/pocket-report/`,
`docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, `docs/adr-0028/execution/`, tout `*.jsonl` réel, toute pièce de D.2 ;
aucune recherche récursive (grep -r, git grep, du, find large) sur `docs/`, le dépôt entier ou le scratchpad entier. Rapport par
message si le harnais refuse le fichier ; journal G1 ; SHA256SUMS. Gate 0 (identifiant exact en tête). Résumé court en français, C-n par C-n.
