# Brief — corrections G2 de la tranche A du collecteur de S2-bis (diff CB-2d, après CB-2c)

Worker `shogen-worker`, effort max. Dépôt `/home/user/shogen` (lecture seule ; **aucune opération git en écriture**). Lis `date -u`
avant toute date. Tu travailles dans `<scratchpad>/s2bis/p1/corr/` ;
`TMPDIR` et cible cargo dédiés.

Base : copie de la tête (`git archive HEAD | tar -x …`, exclusions habituelles : `docs/rapports`, `docs/adr-0025`,
`docs/adr-0028/monark-m009a`, `docs/15-*`, `docs/16-*`, `docs/pocket-report`) + les sept diffs `…/s2bis/p1/diffs/CB-0a.diff` à
`CB-2c.diff` appliqués en série (`git apply`).

Relecture G2 : `…/s2bis/p1/g2/G2-P1A.md` (verdict ACCEPTE-AVEC-CORRECTIONS, liste fermée **C-1 à C-6**, §7) ; ses outils et preuves
dans `…/p1/g2/reprise/` (jeux de mutants `outils/mutants_g2.py`, `mutants_prec.py`). Contrat : G0
`docs/adr-0029/g0-collecte/G0-COLLECTE-RECALC-DEPLOI.md` (contenu `PROPOSITION.md`, corrigé par `AVIS.md`, qui prime) ; ADR-0029.

Adjudications de l'orchestrateur : C-1 telle que la G2 l'écrit (refus nommé de tout `window_start` inférieur ou égal à la dernière
fenêtre écrite, restaurée à la reprise ; `suivante = max(attendu, dernière + w, ws + w)`), et Q-4 : la fenêtre du redémarrage reste
refusée ; le test qui validait le cas contraire est corrigé, pas supprimé. C-2 : après toute `OSError`, l'écrivain passe en état
terminal et refuse tout par un refus nommé ; la reprise suivante déclare la queue. C-3 à C-6 telles qu'écrites. Q-2 : option `--egal`
réservée au job s2bis, si elle tient dans le budget ; sinon item.

Règles : tests d'abord (rouge avant sur la base, vert après) ; rejoue les deux jeux de mutants de la G2 : tout mutant vivant non
équivalent listé en C-5 doit mourir, équivalences motivées ; bibliothèque standard seule ; **un seul diff `CB-2d.diff`, ≤ 200 lignes de
code ajoutées** (sinon CB-2d et CB-2e, en série) ; R-13, R-8 ; aucune opération réseau (lance suites et mutants sous `unshare -n` si
possible) ; `cargo --locked xtask verify` sur la copie (sortie redirigée, lignes de verdict seules ; S-G9 `docs/17:70` connu) ; journal
G1 dans le rapport ; SHA256SUMS. Interdits : `docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`,
`docs/adr-0028/monark-m009a/`, tout `*.jsonl` réel, toute pièce de D.2 ; aucune recherche récursive (grep -r, git grep) sur `docs/`.
Sorties : `…/p1/corr/CB-2d.diff` (et `CB-2e.diff` si besoin), `RAPPORT-CORRECTIONS-P1A.md` (C-n → ce qui a changé, preuves),
SHA256SUMS. Gate 0 (identifiant exact du modèle en tête). Résumé court en français.
