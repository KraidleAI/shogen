# Brief — partie P1 du collecteur de S2-bis, tranche C : sous-lot CB-18 (points d'entrée), puis l'enregistreur de rôle

Worker `shogen-worker`, effort max. Tu travailles dans `<scratchpad>/s2bis/cb18/`, avec `TMPDIR` et une cible cargo dédiés.
Dépôt `/home/user/shogen` en lecture seule : **aucune opération git en écriture**. Lis `date -u` avant toute date. Base : copie de la tête **122c670** (`git archive 122c670 | tar -x …`, exclusions : `docs/rapports`, `docs/adr-0025`, `docs/adr-0028/monark-m009a`, `docs/adr-0028/execution`, `docs/15-*`, `docs/16-*`, `docs/pocket-report`). Les tranches A et B de P1 y sont commises.

Contrat : le G0 `docs/adr-0029/g0-collecte/G0-COLLECTE-RECALC-DEPLOI.md`, dont le contenu est `PROPOSITION.md` corrigé par `AVIS.md`, qui prime ; ADR-0029 et ses ajouts datés.
- **CB-18** (PROPOSITION l.226) : points d'entrée, descripteur, `run_params`, test de bout en bout (collecteur, journal, conformité au FORMAT `docs/adr-0029/s2bis/FORMAT-JOURNAUX-S2BIS.md`).
- Pièces de revue des tranches : `docs/adr-0029/s2bis/revue-p1a/` et `revue-p1b/`.
- Items de l'annexe B (`docs/adr-0028/ANNEXE-B-items.md`, B.60 et B.63, lis ces blocs seuls) dont le déclencheur est CB-18. **Adjudication de l'orchestrateur : tous sont fermés dans ce lot**, chacun avec un test nommé :
  - SHOGEN-S2BIS-ECRIVAIN-USAGE-1 : garde d'un seul fil, refus nommés, `_terminal` sur toute méthode publique d'écriture, la boucle ferme et sort sur `OSError` ou `JOURNAL/casse`, fermeture au point d'entrée ;
  - SHOGEN-S2BIS-PLAN-CABLAGE-1 : refus à la construction d'un nom du plan sans lecture ; câblage des sondes contrôlé ;
  - SHOGEN-S2BIS-SONDES-ECHEANCE-1 : règle `fin` > E appliquée aux sondes, sur l'horloge monotone ;
  - SHOGEN-S2BIS-SOMMEIL-MURAL-1 : dormir jusqu'à l'instant mural en boucle ; départ monotone porté dans `suivi` (limite E-4) ; mesures du worker et du réviseur rejouées ;
  - SHOGEN-S2BIS-FORMAT-RETOUCHES-1 : FORMAT §12, citer RFC 1035 §7.3 et marquer la règle de source comme choix du lot ; ajouter CB-11h à l'en-tête « Corrections ». Le texte de la RFC est dans `biblio/rfc-1035-dns-implementation-2026-10-05.txt`.
- **Puis un diff distinct, SHOGEN-S2BIS-ENREG-ROLE-1**, à faire avant la G2 complète de P1 : étendre `s2-harness/tools/oracle_record.py` (liste fermée de commandes, commit exigé) aux suites `s2bis` et `scripts/sim-bis`, avec ses tests, sans affaiblir ses refus. Lis l'outil et ses tests avant d'écrire.

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
