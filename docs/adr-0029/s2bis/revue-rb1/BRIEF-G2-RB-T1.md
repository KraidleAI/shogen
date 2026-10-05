# Brief — relecture G2 de la partie P3 du recalcul de S2-bis, tranche 1 (RB-0a à RB-1c)

Tu es **réviseur G2 neuf** (`shogen-worker`) : tu n'as rien écrit de ce lot. Dépôt `/home/user/shogen` en lecture seule : **aucune opération git en écriture** (`git --no-optional-locks` pour lire son état ; l'orchestrateur y committe pendant ta passe). Lis `date -u` avant toute date. Tu écris seulement dans `<scratchpad>/s2bis/rb1/g2/` ; rapport par message si le harnais refuse le fichier. **Place disque comptée** : supprime tes copies et tes cibles en fin de passe.

## Pièces
- Les sept diffs `…/rb1/diffs/` : RB-0a, RB-0b, RB-6a, RB-6b, RB-1a, RB-1b, RB-1c, dans cet ordre. Leurs empreintes sont dans `…/rb1/SHA256SUMS`.
- Les preuves (`…/rb1/preuves/`), les outils (`…/rb1/outils/`), les sources, souches et mutants (`…/rb1/travail/`).
- Le rapport du worker transcrit : `…/rb1/g2/RAPPORT-WORKER-RB-T1-transcrit.md`.
- Le brief du worker : `…/rb1/BRIEF-RB-T1.md`.

## Contrat
- Le G0 `docs/adr-0029/g0-collecte/G0-COLLECTE-RECALC-DEPLOI.md`. Son contenu est `PROPOSITION.md`, corrigé par `AVIS.md`, qui prime. Lis la section du recalcul et ses exigences E-R-nn.
- ADR-0029 et ses ajouts datés.
- Le FORMAT `docs/adr-0029/s2bis/FORMAT-JOURNAUX-S2BIS.md`.
- Le recalcul de S2 (`s2-harness/shogen_s2/`), référence de continuité.

Un avis de l'advisor sur les quinze questions Q-RB-1 à Q-RB-15 est demandé en parallèle. Toi, juge la **fidélité au G0 et la justesse du code**.

## Contrôles
1. **Série** :
   - application en série sur 122c670 **et** sur la tête actuelle ;
   - au plus 200 lignes de code par diff ;
   - chaque état vert seul à son plancher exact, par la commande du job : runner d'abord, puis la ligne de `gates.yml`.
2. **Conformité, exigence par exigence**, pour toutes celles que la proposition rattache à RB-0, RB-1 et RB-6.
3. **Justesse du lecteur, contre le FORMAT et l'écrivain réel** :
   - journaux synthétiques écrits par `s2bis/shogen_s2bis/collecte/journal.py`, puis altérés à la main : queue tronquée, ligne coupée, rupture sans reprise, reprise, entiers longs, fichiers manquants ou désordonnés ;
   - le lecteur doit classer chaque cas comme le FORMAT le dit ;
   - mémoire bornée, mesurée par toi.
4. **Justesse de la rotation, par un calcul indépendant** :
   - recalcule toi-même les décalages o(r, u) et K, C, K_crit, S, sur au moins deux petits cas, à la main ou par un script à toi qui n'importe pas le code relu ;
   - recalcule les six vecteurs du worker par `sha256sum` et `bc` ;
   - comparaison au r1 de S2 (`s2-harness/shogen_s2/r1.py`) : écarts voulus (AVIS Q-R-02) contre écarts fortuits.
5. **Config** :
   - schéma, bornes, refus nommés ;
   - τ et σ contre E-R-09 et l'ADR ;
   - gabarit à null refusé tant que les lots amont ne l'ont pas rempli.
6. **Rouge et vert** rejoués sur au moins trois pas.
7. **Mutants** :
   - au moins quinze à toi, classés par la commande du job, avec une borne de temps ; un dépassement de la borne est FATAL ;
   - rejeu d'un échantillon d'au moins vingt mutants du worker.
8. **CI** :
   - aucune gate affaiblie ;
   - frontière de `recalc` dans `test_fitness.py`.
9. **Règles et xtask** :
   - R-13, R-8, octets 92 ;
   - Python 3.10 à 3.13 en `-X dev -W error` ;
   - `cargo --locked xtask verify` sur une copie : lignes de verdict seules ; S-G9 `docs/17:70` est connu.
10. **Écarts E-1 à E-6 et items I-1 à I-8** : avis motivé.

## Exécution
Copies : `git archive <tête> | tar -x -C <dossier>` avec les exclusions `docs/rapports`, `docs/adr-0025`, `docs/adr-0028/monark-m009a`, `docs/adr-0028/execution`, `docs/15-*`, `docs/16-*` et `docs/pocket-report`. Un `TMPDIR` dédié.

Réseau isolé : `unshare -n`, avec `lo` allumée par `…/s2bis/p1b/g2/travail/` (`lo_up.py`, `isole.sh`).

Deux autres workers tournent sur la même machine. Ne tue que tes propres processus.

## Interdits
- les dossiers exclus des copies, plus `docs/adr-0028/execution/` ;
- tout `*.jsonl` réel ;
- toute pièce de D.2 ;
- **aucune recherche récursive (grep -r, git grep, du, find large) sur `docs/`, sur le dépôt entier ni sur le scratchpad entier**.

## Rendu
Verdict : ACCEPTE, ACCEPTE-AVEC-CORRECTIONS (liste fermée) ou REFUSE.

Gate 0 : l'identifiant exact du modèle en tête. Résumé court en français.
