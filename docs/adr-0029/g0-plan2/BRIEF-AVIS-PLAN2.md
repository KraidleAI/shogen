# Brief — avis de l'advisor sur la proposition de G0 du lot PLAN-S2BIS-2

Tu es l'advisor (`shogen-advisor`, R-26). Tu n'agis pas : écris seulement `<scratchpad>/s2bis/plan2/AVIS-PLAN2.md`, et rends aussi un résumé par message.

**But du projet** : faire de Shōgen un standard institutionnel vendable, sans baisse de qualité. La durée déclarée de S2-bis ne doit jamais reposer sur un artefact de simulation.

## Pièces
- Proposition : `…/plan2/PROPOSITION-PLAN2.md` (660 lignes) ; son calcul de support `…/plan2/calc/` ; les notes du rédacteur `…/plan2/NOTES.md`.
- Ton avis précédent : `…/s2bis/sim4/g2/AVIS-SIM-T4.md`, §2 (option B).
- La G2 de la tranche 4 de SIM-BIS : `…/s2bis/sim4/g2/G2-SIM-T4-transcrit.md`, § « Constat du point 9, recompté ». Son point 4 dit : si la famille E1 n'encadre pas S2, W*(C0) = W*(C2) devient vraisemblable et le filet du G0 ne joue plus.
- G0 de SIM-BIS : `docs/adr-0029/g0-sim/` (G0, PROPOSITION, AVIS).
- ADR-0029.
- Lot PLAN-S2BIS : `docs/adr-0029/plan-s2bis/`, `scripts/plan-s2bis/`.
- Annexe B : blocs B.58, B.61, B.64 et B.66 seulement.

## Ce qui est demandé
1. **Questions Q-P2-01 à Q-P2-13.** Pour chacune : Adopté, Modifié ou Rejeté, avec un motif sourcé. Marque [G0] si la question touche la lettre d'un G0 (SIM-BIS ou ADR) et [E0] si elle se tranche avant E0. Points précis :
   - **Q-P2-06** : la durée soumise à A-2 se lit-elle à C1 ? C'est un changement de la lettre du G0.
   - **Q-P2-07** : l'ajout daté doit-il passer avant l'exécution du lot ?
   - **Q-P2-08** : deux passes A et B dans un seul lancement, alors que la lettre dit « lisent une fois ».
2. **Lettre de l'ajout daté au G0 de SIM-BIS** (§3 de la proposition). Est-elle juste ? Ferme-t-elle entièrement le cas « l'encadrement n'encadre pas » (point 4 de la G2) ? Sinon, donne la lettre exacte.
3. **Taille.** La proposition estime 1 100 à 1 400 lignes, contre ≈ 150 dans l'item B.61, plus 180 à 250 lignes d'intégration. Faut-il réduire le périmètre (sorties indispensables, sous-lots fusionnables) sans perdre l'identification ? Rends une liste exacte de ce qu'on garde.
4. **Censure en stress** : 453 épisodes censurés sur 674. Quelle conséquence pour C1 ? La proposition la déclare « borne haute ». Est-ce juste ?
5. **Calendrier** : ce qui bloque E0, et ce qui ne le bloque pas.
6. **Investisseur** : qu'y a-t-il éventuellement à lui dire, en langage clair ?
7. **Trois risques au plus.**

## Interdits
- `docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, `docs/adr-0028/execution/` ;
- tout `*.jsonl` ;
- toute pièce de D.2 ;
- toute recherche récursive, y compris par Glob, sur `docs/`, sur le dépôt ou sur le scratchpad.

Gate 0 : l'identifiant exact du modèle et l'effort, en tête.
