# Brief — réserve R-1 de l'accord de P1 : outillage de preuve non contournable (SHOGEN-S2BIS-RUNNER-SORTIE-1, SHOGEN-S2BIS-ENREG-VERIF-COMMIT-1)

Worker `shogen-worker`, effort max. Dépôt `/home/user/shogen` en lecture seule (`git --no-optional-locks`), aucune écriture git. `date -u` avant toute date. Dossier : `<scratchpad>/s2bis/outillage/` (scratchpad = `<scratchpad>`), TMPDIR dédié, NOTES.md tenu (reprise depuis lui, jamais depuis un `.jsonl`). **Budget de calcul presque épuisé : reste sobre, pas d'exploration large.**

## Base et contrat
- Tête **11b9d43** (`git archive`, exclusions habituelles : `docs/rapports`, `docs/adr-0025`, `docs/adr-0028/monark-m009a`, `docs/adr-0028/execution`, `docs/15-*`, `docs/16-*`, `docs/pocket-report`).
- Rattachement : G0 `docs/adr-0029/g0-collecte/G0-COLLECTE-RECALC-DEPLOI.md` ; annexe B, blocs B.71 et B.72 (fin de `docs/adr-0028/ANNEXE-B-items.md`) ; accord `docs/adr-0029/s2bis/revue-p1-integ/ACCORD-P1.md` (R-1) ; relecture `G2-P1-INTEG-transcrit.md` §6 et contre-contrôle du même dossier.
- Fichiers : `enforcement/tests/run-fixtures-verdict-suite-s2.py` (runner), `enforcement/verdict-suite-s2.py` (vérificateur), l'enregistreur de rôle `oracle_record.py` et ses tests (chemin à lire dans le dépôt), `.github/workflows/gates.yml` (lignes des jobs, à ne changer que si nécessaire).

## À faire (liste fermée)
1. **RUNNER-SORTIE-1.** Le runner ne doit plus pouvoir sortir en 0 sans avoir joué tous ses cas : ni par `os._exit(0)` au chargement du vérificateur, ni par `sys.exit(0)` levé pendant un cas. Choisis entre (a) le vérificateur chargé et chaque cas joué dans un sous-processus dont le runner exige un résumé final signé de son nombre de cas, et (b) toute autre construction qui donne la même garantie ; écris ton choix et sa raison (Q-n). Cas neufs : `os._exit(0)` au chargement, `sys.exit(0)` pendant un cas, résumé absent ou tronqué → sortie non nulle.
2. **ENREG-VERIF-COMMIT-1.** L'enregistreur ne doit plus exécuter un vérificateur altéré du commit relu sans le dire : sha256 du vérificateur du commit consigné et comparé à celui de l'outil (ou d'une épingle versée) ; écart = refus nommé ; `ligne_du_job` rattrape toute exception au chargement et la nomme. Leurre L2 de la G2 d'intégration (vérificateur complaisant dans le commit) : refusé.
3. Aucun cas existant du runner ni test de l'enregistreur retiré ou affaibli ; les leurres des réviseurs CB-18 (`<scratchpad>/s2bis/cb18/cc*/travail/outils/leurres_*.py`) et de la G2 d'intégration (`<scratchpad>/s2bis/p1-integ/outils/`) donnent les mêmes verdicts, sauf ceux que ce lot doit faire refuser.

## Règles
- Tests d'abord, rouge montré. Au moins 8 mutants par diff, classés par la commande du job (runner, puis ligne s2bis de `gates.yml`, borne 300 s, dépassement FATAL).
- Bibliothèque standard seule ; Python 3.10 à 3.13 en `-X dev -W error` (critère de vert : code 0 et aucune ligne « Exception ignored » ni « Warning »).
- Diffs en série **OUT-1a, OUT-1b…**, chacun ≤ 200 lignes de code ajoutées ; planchers exacts (`--egal`) ; METRIQUES par diff si la suite s2bis change.
- R-13, R-8, octets 92 comptés, ≤ 120 caractères. Isolement réseau (`<scratchpad>/s2bis/p1b/g2/travail/outils/isole.sh`). `cargo --locked xtask verify` : lignes de verdict seules.
- Livrables : diffs, SHA256SUMS, journal G1, tableau des cas et mutants. PID réels ; nettoyage final.

## Interdits
`docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, `docs/adr-0028/execution/` ; tout `*.jsonl` réel ; toute pièce de D.2 ; toute recherche récursive (grep -r, git grep, du, find large) sur `docs/`, le dépôt entier ou le scratchpad entier.

Rapport par message, court, en français, Gate 0 en tête.
