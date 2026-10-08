# Brief — partie P3 du recalcul de S2-bis, tranche 1 : sous-lots RB-0, RB-1 et RB-6

Worker `shogen-worker`, effort max. Tu travailles dans `<scratchpad>/s2bis/rb1/`, avec un `TMPDIR` dédié.
Dépôt `/home/user/shogen` en lecture seule : **aucune opération git en écriture**. Lis `date -u` avant toute date. Base : copie de la tête **122c670** (`git archive 122c670 | tar -x …`, exclusions : `docs/rapports`, `docs/adr-0025`, `docs/adr-0028/monark-m009a`, `docs/adr-0028/execution`, `docs/15-*`, `docs/16-*`, `docs/pocket-report`).

Contrat : le G0 `docs/adr-0029/g0-collecte/G0-COLLECTE-RECALC-DEPLOI.md`, dont le contenu est `PROPOSITION.md` corrigé par `AVIS.md`, qui prime ; ADR-0029 et ses ajouts datés.
- Sous-lots (PROPOSITION l.468, 469 et 474 ; exigences rattachées par la proposition : lis la section du recalcul et ses tableaux d'exigences) :
  - **RB-0** : `config_analyse.py` ;
  - **RB-1** : lecteur en flux du journal au FORMAT `docs/adr-0029/s2bis/FORMAT-JOURNAUX-S2BIS.md` ;
  - **RB-6** : rotation avec vecteurs indépendants.
- Emplacement du paquet, job CI, plancher et fitness : ceux que fixe la proposition. Si elle ne les fixe pas, pose une question Q-RB-n avec ta proposition, et prends le patron de `s2bis/` (job unittest jugé par `enforcement/verdict-suite-s2.py --aucun-saut --egal --plancher N`, cas du runner).
- Le recalcul de S2 (`s2-harness/shogen_s2/`) est la référence de continuité : lis ce que la proposition en cite, et reprends ou adapte avec la provenance écrite. RB-6 servira d'oracle croisé au lot SIM-BIS (SB-13) : écris son contrat d'entrée et de sortie explicitement.
- **Aucune lecture de journal de campagne réel** : jeux synthétiques seulement, écrits par l'écrivain de `s2bis/`.
- **Toute valeur que le G0 ne fixe pas devient une question numérotée Q-RB-n**, et non un choix silencieux.

Règles communes :
- **tests d'abord** : un rouge d'assertion montré avant le code, puis le vert ;
- **mutants** : au moins dix par sous-lot, **classés par la commande du job** (runner d'abord, puis la ligne de `gates.yml`, suite entière, borne de 300 s ; dépassement = FATAL, jamais « tué » ; SHOGEN-S2BIS-MUT-COMMANDE-1) ; verse tous les mutants que tu cites ;
- **bibliothèque standard seule** (R-8) ; R-13 ;
- **diffs en série** : chacun ≤ 200 lignes de code ajoutées (R-25), plancher exact du job relevé à chaque diff (`--egal`) ;
- **aucune opération réseau** : `unshare -n` avec `lo` allumée quand la suite l'exige (SHOGEN-HARNAIS-UNSHARE-LO-1 ; outils `lo_up.py` et `isole.sh` du réviseur dans `…/s2bis/p1b/g2/travail/`) ;
- Python 3.10 à 3.13 en `-X dev -W error` ;
- `cargo --locked xtask verify` sur la copie : lignes de verdict seules ; S-G9 `docs/17:70` est connu sur les copies ;
- journal G1 dans le rapport ([lu], [2nd], [abs]) ; SHA256SUMS ; estimation révisée des sous-lots restants ;
- **nettoie tes copies lourdes à la fin** (disque partagé avec deux autres workers).

Interdits :
- `docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, `docs/adr-0028/execution/` ;
- tout `*.jsonl` réel ; toute pièce de D.2 ;
- **aucune recherche récursive (grep -r, git grep, du, find large) sur `docs/`, sur le dépôt entier ni sur le scratchpad entier**, même sur tes copies.

Deux autres workers travaillent en parallèle sur d'autres dossiers, et l'orchestrateur committe dans le dépôt pendant ton lot : ne prends pas de verrou git sur le dépôt (`git --no-optional-locks` si tu lis son état). Rapport par message si le harnais refuse le fichier. Gate 0 : l'identifiant exact du modèle en tête. Résumé court en français.
