# Brief — relecture G2 de la partie P1 du collecteur de S2-bis, tranche A (sous-lots CB-0, CB-1, CB-2 : diffs CB-0a à CB-2c)

Tu es **réviseur G2 neuf** (`shogen-worker`) : tu n'as rien écrit de ce lot. Dépôt `/home/user/shogen` (lecture seule ; **aucune
opération git en écriture**). Lis `date -u` avant toute date. Tu écris seulement dans
`<scratchpad>/s2bis/p1/g2/` (rapport `G2-P1A.md`).

Pièces : sept diffs `…/s2bis/p1/diffs/` (empreintes : `…/p1/SHA256SUMS`) ; arbre final et preuves du worker (`…/p1/journal/`, outils
de mutants) ; rapport du worker, avec son journal G1 et ses questions Q-1 à Q-8 : `…/p1/g2/RAPPORT-WORKER-P1A.md` ; brief du worker
`…/p1/BRIEF-P1-A.md`. Contrat : G0 `docs/adr-0029/g0-collecte/G0-COLLECTE-RECALC-DEPLOI.md` (la proposition `PROPOSITION.md` en est le
contenu, corrigée par `AVIS.md`) ; ADR-0029 (acceptée, avec ses ajouts datés).

Contrôles : (1) les diffs s'appliquent en série sur la tête actuelle, chacun ≤ 200 lignes de code ajoutées ; arbre obtenu = empreintes ;
(2) conformité exigence par exigence (E-C-01, E-C-02 partiel, E-C-16, E-C-18 à E-C-22, E-C-40, E-C-41 ; §1 pt 6 et §2.4 de la
proposition) ; (3) robustesse du journal chaîné : intégrité de la chaîne (seq, prec), durabilité (fsync), reprise sur chaque forme de
queue, verrou, trous, horloge reculée ; cherche les cas non testés ; (4) rouge avant / vert après rejoués sur au moins trois cas ; au
moins douze mutants à toi ; (5) la CI : le job `s2bis-unittest`, le vérificateur paramétré (comportement par défaut inchangé : rejoue
le runner et la suite S2), aucune gate affaiblie ; (6) les choix E-7 (a) à (f) du worker et ses questions Q-1 à Q-8 : avis motivé ;
(7) R-13, R-8 (bibliothèque standard seule), R-25 ; `cargo --locked xtask verify` sur une copie sans dossiers interdits (sortie redirigée,
lignes de verdict seules ; le rouge S-G9 `docs/17:70` d'une copie sans `docs/rapports` est connu) ; (8) items proposés I-1 à I-7.
Copies : `git archive HEAD | tar -x -C <dossier>/arbre --exclude=docs/rapports --exclude=docs/adr-0025 --exclude=docs/adr-0028/monark-m009a
--exclude='docs/15-*' --exclude='docs/16-*' --exclude=docs/pocket-report` ; `TMPDIR` et cible cargo dédiés. Aucune opération réseau hors
des cibles réservées de test. Interdits : ces dossiers, tout `*.jsonl` réel, toute pièce de D.2 ; aucune recherche récursive sur tout
`docs/`. Verdict : ACCEPTE, ACCEPTE-AVEC-CORRECTIONS (liste fermée) ou REFUSE. Gate 0 (identifiant exact). Résumé court en français.
