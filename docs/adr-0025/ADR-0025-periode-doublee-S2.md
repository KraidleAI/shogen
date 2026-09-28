# ADR-0025 — Période à double pilote de la campagne S2 (24/09 18:18Z → 26/09 15:07Z) : exclusion de n, sensibilité publiée, déclencheur de prolongation

- **Statut** : **G0 proposé** (rédigé par l'orchestrateur MONARK `claude-fable-5-1` sur go investisseur « règle tout ça », 2026-09-26 15:3x UTC, avis `advisor` Q6 du même jour — conseil suivi) ; à accepter par le validateur-humain / `shogen-orchestrator` **avant tout calcul de z**. Aucune implémentation dans ce commit.
- **Rattachement** : RUNBOOK-campagne §6 (« harnais-down ≠ source-en-panne »), §8 (« ne publie rien ; D6 = publiable »), critère strate stress 6,95 j = 166,8 h ; ADR-0020 (fail-closed) ; ADR-0024 (38 600 fenêtres, fin ≈ 28/09) ; 04 §5 (« fenêtre de complaisance ») ; incident `F:\shogen-campagne\INCIDENT-2026-09-26-double-pilote.md` ; archive chercheur `F:\PRODUITS\etude-2026-09-25-pocket\chercheurs\shogen-interne\ARCHIVE-shogen-interne.md` §10.2, §15.1, §15.2 (C-SI-2).

## Faits mesurés (journal `campagne/control.jsonl`, recompte orchestrateur 2026-09-26 15:24 UTC)

- Deux pilotes `run_campaign` ont écrit le même journal du **2026-09-24 18:18Z au 2026-09-26 15:07Z** (`window_start` de la première et de la dernière fenêtre à deux `window_close`) ; chaîne B (Startup → `run-onboot.bat` → boucle) arrêtée 15:08:53Z ; chaîne A conservée ; garde durcie (INCIDENT).
- Fenêtres distinctes : **36 557** ; écrites deux fois : **2 207** ; dans la plage [18:18Z ; 15:07Z], **410** fenêtres n'ont qu'une écriture (doublement non contigu) ⇒ la plage entière compte **2 617** fenêtres.
- Strates (week-end UTC = stress) : stress 10 351 fenêtres = 172,5 h dont **908 (15,1 h) dans la plage** ; calme 26 206 = 436,8 h dont **1 709 (28,5 h) dans la plage**. Après exclusion de la plage : **stress 157,4 h** (< 166,8 h aujourd'hui), calme 408,3 h.
- Projection à collecte continue (1 fenêtre/min) : 38 600ᵉ fenêtre ≈ **28/09 01:27Z** ; 1 955 fenêtres de week-end restantes ⇒ **stress ≈ 190,0 h après exclusion** (critère atteint si le reste du week-end est propre).
- Pendant la plage, deux relevés HTTP par flux et par fenêtre (octets différents) et pannes de transport en hausse (binance 0,3 % → 18,3 % sur toutes les lectures ; effet sur l'ensemble last-wins **inconnu avant calcul**) ; causalité **non établie** (aucune expérience contrôlée, charge machine concomitante). `error_origin` : harnais (garde de relance), pas les sources.

## Décision (proposée)

1. **Exclusion de la plage entière** [2026-09-24T18:18:00Z ; 2026-09-26T15:07:00Z], par `window_start`, de **n, K et P̂_more, dans les trois strates** (calme, stress, poolée), comme période « harnais-dégradé » (RUNBOOK §6). Motif : `r1.py` compte tout `status ≠ ok` comme panne ; des pannes induites par le harnais seraient inscrites comme co-défaillances de sources.
2. **Jamais une excision du journal** : filtre paramétré du lecteur d'analyse (`--exclude-window-start-range <from> <to>`, valeurs de cet ADR), couvert par l'oracle non-LLM (test : n avant/après = 2 617 fenêtres exactement sur le journal réel).
3. **Rejeté** : « retenir la lecture ok si l'une des deux l'est » — sélection dépendante des données (« fenêtre de complaisance », 04 §5) ; « inclure tel quel » sans sensibilité.
4. **Sensibilité obligatoire** dans le rapport final : table des trois z × {plage exclue, plage incluse}, couverture par week-end (29/08 19,0 h ; 05/09 46,7 h ; 12/09 43,5 h ; 19/09 47,9 h ; 26/09 en cours), et la mention « causalité non établie ».
5. **Déclencheur conditionnel, pas une décision** : si, à la 38 600ᵉ fenêtre, la strate stress après exclusion est < 166,8 h (coupure ce week-end), prolongation d'UN week-end par ADR séparée (`--duration` seul, comme ADR-0024).
6. Fin de campagne inchangée (date fixe, 38 600 fenêtres) ; publication du z = décision investisseur (RUNBOOK §8, D8).

## Conséquences

- Rapport final : n analysé ≈ 38 600 − 2 617 ; prolongation ADR-0024 et cet incident déclarés avec leur motif.
- Item **SHOGEN-LOOP-GUARD-1** : porter la garde durcie dans la boucle `run-campagne.bat` après la fin de campagne (fichier lu par position par le cmd vivant : pas d'édition à chaud). Item **SHOGEN-UPS-1** inchangé.
- Le compteur du watchdog (`J0-STATUS.txt`) compte les occurrences brutes : ne jamais lire « campagne terminée » sur ce chiffre.

## Alternatives écartées

- Exclure seulement les fenêtres à double écriture (2 207) : laisserait 410 fenêtres de la même période dégradée ; la plage est l'unité honnête.
- Prolonger d'emblée d'un week-end : décision de valeur sans besoin démontré aujourd'hui (190 h projetées) ; gardée en déclencheur.

## Provenance

Recompte : script de session (lecture seule de `control.jsonl`, 15:24Z) ; avis advisor archivé `F:\PRODUITS\etude-2026-09-25-pocket\AVIS-advisor-2026-09-26.md` (Q6) ; CHANTIERS MONARK 2026-09-26 15:1x / 15:3x UTC. Aucune ligne de journal modifiée ; aucun processus autre que la chaîne B touché.

## Statut — 2026-09-28 03:00 UTC : ACCEPTÉE (investisseur, décision MONARK 269 : « go pour ADR-0025, exclusion de la plage entière »)
Décision 1 retenue telle quelle (plage entière 2026-09-24T18:18:00Z → 2026-09-26T15:07:00Z exclue de n, K, P̂_more, trois strates) ; point 2 (filtre paramétré, jamais d excision) = lot « filtre d exclusion » (cp-1 bref → G1 → G2), mission `F:/tmp/shogen-j28/mission-adr0025-filtre.md` ; point 5 = fait à mesurer après la clôture (campagne close le 2026-09-28 01:27Z, journaux scellés). Publication du z inchangée : décision investisseur.

## Amendement — 2026-09-28 03:39 UTC (orchestrateur, Q-G1-2 du lot filtre) — **RATIFIÉ par l investisseur le 2026-09-28 03:44 UTC (décision MONARK 272)**
Borne haute de la plage : la chaîne B a été arrêtée à 15:08:53Z, en pleine fenêtre ; la fenêtre `window_start` 2026-09-26T15:08Z (strate stress) porte 6 flux à lectures doublées et un seul marqueur — seule fenêtre à lectures doublées hors plage. La plage exclue devient **[2026-09-24T18:18:00Z ; 2026-09-26T15:08:00Z]** (bornes incluses, sur `window_start`) : 2 618 fenêtres (calme 1 709, stress 909), n = 35 982 ; stress après exclusion 11 397 fenêtres = 189,95 h ≥ 166,8 h (déclencheur point 5 non atteint). Valeurs passées en ligne de commande au rapport (point 2), jamais codées. Écart préexistant relevé par le cp-1 (Q-1) : la « strate poolée » promise par RUNBOOK §5 et par la décision 1 n existe pas dans le harnais — construction à trancher par l investisseur avant J14/J28 (item SHOGEN-STRATE-POOLEE-1).
