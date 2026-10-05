# Brief — relecture G2 du lot SIM-BIS, tranche 1 (SB-0a à SB-5b)

Tu es **réviseur G2 neuf** (`shogen-worker`) : tu n'as rien écrit de ce lot. Dépôt `/home/user/shogen` (lecture seule ; **aucune
opération git en écriture**). Lis `date -u` avant toute date. Tu écris seulement dans
`<scratchpad>/s2bis/sim1/g2/` (rapport `G2-SIM-T1.md` ; si le harnais
refuse le fichier, rends-le par message).

Pièces : neuf diffs `…/sim1/diffs/` (empreintes `…/sim1/SHA256SUMS`) ; preuves `…/sim1/journal/`, outils `…/sim1/outils/` ; rapport du
worker transcrit `…/sim1/g2/RAPPORT-WORKER-SIM-T1-transcrit.md` ; brief du worker `…/sim1/BRIEF-SIM-T1.md`. Contrat : G0
`docs/adr-0029/g0-sim/G0-SIM-BIS.md` (contenu `PROPOSITION.md` corrigé par `AVIS.md`, qui prime) ; ADR-0029 et ses ajouts datés ;
sorties de PLAN-S2BIS `docs/adr-0029/plan-s2bis/`. Note de l'orchestrateur : la numérotation des sous-lots qui fait foi est celle de
la proposition (SB-0 à SB-14) ; « SB-1 à SB-15 » du G0 et du JOURNAL est une erreur de compte de l'orchestrateur, à corriger par ajout daté.

Contrôles : (1) application en série sur la tête actuelle, ≤ 200 lignes de code par diff, arbre = empreintes, chaque état vert seul
à plancher exact (`--egal`) ; (2) conformité exigence par exigence (E-S-01, 02, 03, 05, 06, 14, 23, 25, 28 partiel, 37, 41, 42, 43, 48
partiel) ; (3) **exactitude des tirages** : vérifie toi-même, par un calcul indépendant en `Fraction` (et non par le code du lot), que
`seuil` rend le plus petit flottant ≥ x pour des x difficiles (dénominateurs premiers, x proche d'un flottant, x = k/7), que la
comparaison u < seuil(x) ⇔ u < x tient, et que les seuils géométriques et la garde de 128 bits sont justes à quelques rangs ;
`math.nextafter` est-il exact au sens d'E-S-43 ? (4) **identité bit à bit** : mêmes graines → mêmes sorties sous 3.10 à 3.13 et
PYTHONHASHSEED différents ; (5) calibration : relis quelques lignes d'`episodes.txt` et refais à la main deux quotients et un FIV ;
(6) calendrier : vérifie la compression et les runs sur un petit exemple fait à la main ; le test croisé avec `window.py` ;
(7) rouge avant / vert après rejoués sur au moins trois cas ; au moins quinze mutants à toi, classés **par la commande du job (suite
entière) avec borne de temps** (item SHOGEN-S2BIS-MUT-COMMANDE-1) ; (8) CI : job `sim-bis-unittest`, K-03, aucune gate affaiblie ;
(9) R-13, R-8 ; `cargo --locked xtask verify` sur une copie (lignes de verdict seules ; S-G9 `docs/17:70` connu) ; (10) écarts E-1 à
E-10, questions Q-1 à Q-8 et items I-1 à I-6 : avis motivé. Copies : `git archive HEAD | tar -x -C <dossier> --exclude=docs/rapports
--exclude=docs/adr-0025 --exclude=docs/adr-0028/monark-m009a --exclude='docs/15-*' --exclude='docs/16-*' --exclude=docs/pocket-report` ;
`TMPDIR` et cible cargo dédiés ; `unshare -n` si possible. Interdits : ces dossiers, `docs/adr-0028/execution/`, tout `*.jsonl` réel,
toute pièce de D.2 ; **aucune recherche récursive (grep -r, git grep, du, find large) sur `docs/`, sur le dépôt entier ni sur le
scratchpad entier**. Verdict : ACCEPTE, ACCEPTE-AVEC-CORRECTIONS (liste fermée) ou REFUSE. Gate 0 (identifiant exact). Résumé court en français.
