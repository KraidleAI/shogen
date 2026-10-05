# Brief — lot SIM-BIS, tranche 3 : sous-lots SB-6 (observateurs), SB-7 et SB-8 (règle)

Worker `shogen-worker`, effort max. Tu travailles dans `<scratchpad>/s2bis/sim3/`, avec un `TMPDIR` dédié.
Dépôt `/home/user/shogen` en lecture seule : **aucune opération git en écriture**. Lis `date -u` avant toute date. Base : copie de la tête **122c670** (`git archive 122c670 | tar -x …`, exclusions : `docs/rapports`, `docs/adr-0025`, `docs/adr-0028/monark-m009a`, `docs/adr-0028/execution`, `docs/15-*`, `docs/16-*`, `docs/pocket-report`), **plus la tranche 2, non encore commise et en contre-contrôle**. Applique en série les six diffs `…/s2bis/sim2/diffs-784ebd2/SB-3A.diff` à `SB-4B.diff`, puis les six `…/s2bis/sim2/corr/diffs/SB-4C.diff` à `SB-4H.diff`, avec les sha256 de `…/sim2/SHA256SUMS` et `…/sim2/corr/SHA256SUMS`. Si le contre-contrôle change la tranche 2, je te ferai rejouer tes diffs après les siens.

Contrat : le G0 `docs/adr-0029/g0-sim/G0-SIM-BIS.md`, avec son ajout daté ; son contenu est `PROPOSITION.md`, corrigé par `AVIS.md`, qui prime ; ADR-0029. La numérotation SB-0 à SB-14 fait foi. Sous-lots (PROPOSITION l.359 à 361 ; exigences E-S-nn rattachées par la proposition ; tests du §6.2) :
- **SB-6** : `observateurs.py` ;
- **SB-7** : `regle.py` I ;
- **SB-8** : `regle.py` II.

Pièces de revue à lire :
- tranche 1 : `docs/adr-0029/g0-sim/revue-t1/` ;
- tranche 2 : `…/sim2/g2/` (`G2-SIM-T2-transcrit.md` et `AVIS-SIM-T2.md`) et `…/sim2/corr/RAPPORT-CORRECTIONS-SIM-T2-transcrit.md`.

Règles propres à la tranche, qui s'ajoutent aux règles communes plus bas :
- **identité bit à bit** : graines, PYTHONHASHSEED, Python 3.10 à 3.13 ;
- **indices des flux** pris dans `sources.indices_hotes` (Q-T2-11) ; composants des flux en liste fermée dans `parametres.json` ;
- **garde `ast`** des puissances et du hasard (LIBM-POW-1) appliquée à tes modules ;
- **aucune lecture de journal de campagne** ;
- **oracles exacts** là où la proposition le dit (arrêt anticipé contre R complet, SB-8) ;
- **toute valeur que le G0 ne fixe pas devient une question numérotée Q-T3-n**, et non un choix silencieux.

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
