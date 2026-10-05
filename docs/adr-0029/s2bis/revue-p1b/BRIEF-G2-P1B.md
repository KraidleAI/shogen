# Brief — relecture G2 de la partie P1 du collecteur de S2-bis, tranche B (CB-3a à CB-11b)

Tu es **réviseur G2 neuf** (`shogen-worker`) : tu n'as rien écrit de ce lot. Dépôt `/home/user/shogen` (lecture seule ; **aucune
opération git en écriture**). Lis `date -u` avant toute date. Tu écris seulement dans
`<scratchpad>/s2bis/p1b/g2/` (rapport `G2-P1B.md` ; si le harnais
refuse le fichier, rends-le par message).

Pièces : huit diffs `…/s2bis/p1b/diffs/CB-3a.diff` à `CB-11b.diff` (empreintes : `…/p1b/SHA256SUMS`) ; preuves du worker
`…/p1b/journal-d/`, outils de mutants `…/p1b/mutants-*.py`, `campagne.py` ; rapport du worker transcrit :
`…/p1b/g2/RAPPORT-WORKER-P1B-transcrit.md` ; brief du worker `…/p1b/BRIEF-P1-B.md`. Contrat : G0
`docs/adr-0029/g0-collecte/G0-COLLECTE-RECALC-DEPLOI.md` (contenu `PROPOSITION.md`, corrigé par `AVIS.md`, qui prime) ; ADR-0029 avec
ses ajouts datés ; annexe B.60 (`docs/adr-0028/ANNEXE-B-items.md`, cherche par `grep -n` dans ce fichier seul). La tranche A est
commise (tête actuelle) ; ses relectures sont dans `docs/adr-0029/s2bis/revue-p1a/` (modèle de forme et de rigueur).

Contrôles : (1) les diffs s'appliquent en série sur la tête actuelle, ≤ 200 lignes de code ajoutées chacun, arbre = empreintes, chaque
état vert seul, plancher exact (`--egal`) ; (2) conformité exigence par exigence (E-C-03 à E-C-05, E-C-09, E-C-11 à E-C-15, E-C-17
partiel, E-C-25 à E-C-29, CB-5, CB-10) ; (3) robustesse : lecture pendue à chaque phase (DNS, connexion, TLS, en-têtes, corps lent,
coupure), échéance dure tenue quel que soit l'état des fils, fils abandonnés bornés, résultats tardifs jamais écrits, horloge reculée,
DNS (réponse forgée, identifiant, source, pointeurs, troncature) ; cherche les cas non testés ; (4) rouge avant / vert après rejoués sur
au moins trois cas ; au moins quinze mutants à toi ; (5) CI : job s2bis, plancher exact, aucune gate affaiblie ; (6) écarts E-1 à E-5
et questions 1 à 6 du worker : avis motivé, en particulier E-3 (a) ThreadPoolExecutor, E-3 (e) D-3 brut, E-3 (f) aucune redirection
(compare au comportement de S2 sur les mêmes points d'accès : cherche dans `s2-harness/` si un hôte du pool redirigeait), E-3 (i) TC ;
(7) R-13, R-8 (bibliothèque standard seule ; Node n'est qu'un contre-contrôle hors dépôt) ; `cargo --locked xtask verify` sur une
copie (lignes de verdict seules ; S-G9 `docs/17:70` connu sur une copie) ; (8) items I-B1 à I-B5 et effets sur B.60. Copies :
`git archive HEAD | tar -x -C <dossier> --exclude=docs/rapports --exclude=docs/adr-0025 --exclude=docs/adr-0028/monark-m009a
--exclude='docs/15-*' --exclude='docs/16-*' --exclude=docs/pocket-report` ; `TMPDIR` et cible cargo dédiés ; suites et mutants sous
`unshare -n` si possible. Interdits : ces dossiers, `docs/adr-0028/execution/`, tout `*.jsonl` réel, toute pièce de D.2 ; **aucune
recherche récursive (grep -r, git grep, du) sur `docs/` ni sur le scratchpad entier**. Verdict : ACCEPTE, ACCEPTE-AVEC-CORRECTIONS (liste
fermée) ou REFUSE. Gate 0 (identifiant exact). Résumé court en français.
