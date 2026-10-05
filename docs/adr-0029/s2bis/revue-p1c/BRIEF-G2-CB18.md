# Brief — relecture G2 de la partie P1 du collecteur de S2-bis, tranche C (CB-18a à CB-18f, ENREG-ROLE, SEGMENT-JOUR, ENTIER-ECRIVAIN)

Tu es **réviseur G2 neuf** (`shogen-worker`) : tu n'as rien écrit de ce lot. Le dépôt `/home/user/shogen` est en lecture seule : **aucune opération git en écriture** (`git --no-optional-locks`). Lis `date -u` avant toute date. Tu écris seulement dans `<scratchpad>/s2bis/cb18/g2/`, et tu rends ton rapport par message. **Place disque comptée** : supprime tes copies et tes cibles à la fin.

## Pièces

- Neuf diffs, à appliquer dans cet ordre : `…/cb18/diffs/` CB-18a, CB-18b, CB-18c, CB-18d, CB-18e, CB-18f, ENREG-ROLE, SEGMENT-JOUR, ENTIER-ECRIVAIN. Leurs empreintes sont dans `…/cb18/SHA256SUMS`.
- Le rapport du worker transcrit : `…/cb18/g2/RAPPORT-WORKER-CB18-transcrit.md`.
- Le brief du worker : `…/cb18/BRIEF-CB18.md`. L'ajout N-1, I-1, I-2 est décrit dans le rapport.
- Les outils, mutants et preuves du worker : `…/cb18/`.

**Base** : la tête 3164348, puis les neuf diffs. Les tranches A et B de P1 sont commises dans la tête.

## Contrat

- Le G0 `docs/adr-0029/g0-collecte/G0-COLLECTE-RECALC-DEPLOI.md`, dont le contenu est `PROPOSITION.md` corrigée par `AVIS.md`.
- L'ADR-0029.
- Le FORMAT `docs/adr-0029/s2bis/FORMAT-JOURNAUX-S2BIS.md`.
- Les items de l'annexe B fermés par ce lot (blocs B.60 et B.63 seulement).
- Les pièces de revue `docs/adr-0029/s2bis/revue-p1a/` et `revue-p1b/`.
- Pour N-1 et I-1, le banc du réviseur du recalcul : `…/s2bis/rb1/g2/outils/banc_lecteur.py` et ses preuves.

## Contrôles

1. **Série.** Application sur la tête. Chaque diff ajoute au plus 200 lignes de code. Chaque état est vert seul, à son plancher exact, par la commande du job : runner d'abord, puis la ligne de `gates.yml`. Vérifie aussi le job S2 pour ENREG-ROLE.
2. **Fermeture des items.** Chaque item que le lot dit fermer l'est-il vraiment, par un test qui échoue sans le correctif ? Items : ECRIVAIN-USAGE-1, PLAN-CABLAGE-1, SONDES-ECHEANCE-1, SOMMEIL-MURAL-1, FORMAT-RETOUCHES-1 (avec I-2), SEGMENT-JOUR-1, ENTIER-ECRIVAIN-1, ENREG-ROLE-1. Rejoue les sondes de mesure (sommeil mural du worker et du réviseur de P1-B, dans `…/p1b/`).
3. **Conformité de CB-18 aux exigences de la proposition** : points d'entrée, descripteur, `run_params`, configurations scellées, bout en bout conforme au FORMAT.
4. **Écrivain après N-1 et I-1.**
   - Rejoue le banc du réviseur RB sur l'état final. Ni collision ni ordre faux ne doivent survenir.
   - Construis toi-même des scénarios de jour et de segment : jour futur, plus de 10 segments, redémarrages répétés, horloge reculée de plusieurs jours.
   - Vérifie que la borne de 640 chiffres ne dépend pas du réglage de l'interpréteur.
5. **ENREG-ROLE.**
   - `oracle_record` garde-t-il tous ses refus ?
   - La ligne du job est-elle lue au `gates.yml` du commit ?
   - Fais au moins un essai de contournement.
6. **Rouge et vert** rejoués sur au moins trois pas.
7. **Mutants.**
   - Au moins quinze à toi, classés par la commande du job, avec une borne de temps. Un dépassement est FATAL.
   - Rejoue un échantillon d'au moins vingt mutants du worker.
8. **CI** : aucune gate ne doit être affaiblie. Le job S2 n'a pas `--egal` : donne ton avis.
9. **Interpréteurs et contrôles statiques.**
   - Python 3.10 à 3.13 en `-X dev -W error`.
   - R-13, R-8, octets 92.
   - `cargo --locked xtask verify` sur une copie (lignes de verdict seules ; S-G9 `docs/17:70` connu).
10. **Écarts 1 à 5 et items 1 à 8 du worker.** Donne un avis motivé, en particulier sur :
    - SHOGEN-S2-PY310-1 (s2-harness rouge sous Python 3.10) ;
    - CITATIONS-ADR-DECALEES-1 (citations « ADR-0029 l.N » décalées par les ajouts datés).

## Exécution

- Copies faites par `git archive`, avec les exclusions `docs/rapports`, `docs/adr-0025`, `docs/adr-0028/monark-m009a`, `docs/adr-0028/execution`, `docs/15-*`, `docs/16-*` et `docs/pocket-report`. `TMPDIR` dédié.
- Réseau isolé : `unshare -n`, avec `lo` allumée par `…/s2bis/p1b/g2/travail/` (`lo_up.py`, `isole.sh`).
- D'autres agents tournent sur la même machine : ne tue que tes propres processus, consigne leur PID réel, et pas de `pgrep -f` sur un motif large.
- Après un compactage, reprends depuis un fichier de notes tenu dans ton dossier, jamais depuis un `.jsonl`.

## Interdits

- Les dossiers exclus des copies.
- Tout `*.jsonl`.
- Toute pièce de D.2.
- **Toute recherche récursive (grep -r, git grep, du, find large) sur `docs/`, sur le dépôt entier ou sur le scratchpad entier.**

## Rendu

Verdict : ACCEPTE, ACCEPTE-AVEC-CORRECTIONS (liste fermée) ou REFUSE. Gate 0 : l'identifiant exact du modèle en tête. Résumé court en français.
