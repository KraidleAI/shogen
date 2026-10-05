# Brief — avis de l'advisor sur SIM-BIS, tranche 4 : questions Q-T4-1 à Q-T4-13, et constat sur la famille E1

Tu es l'advisor (`shogen-advisor`, R-26). Tu n'agis pas. Tu écris seulement `<scratchpad>/s2bis/sim4/g2/AVIS-SIM-T4.md`, et tu rends aussi un résumé par message.

**But du projet** : faire de Shōgen un standard institutionnel vendable, sans baisse de qualité. Une durée de campagne déclarée sur un artefact de simulation serait un défaut grave pour un tiers.

## Pièces

- Le rapport du worker transcrit : `…/sim4/g2/RAPPORT-WORKER-SIM-T4-transcrit.md`, en particulier :
  - le point 9 (constat) ;
  - le tableau des questions Q-T4 ;
  - l'écart E-4 (FIV de type E1 imprimées avant E0, pour fixer un seuil de test) ;
  - l'estimation révisée.
- Les diffs dans `…/sim4/diffs/`.
- Le G0 `docs/adr-0029/g0-sim/G0-SIM-BIS.md`, avec `PROPOSITION.md` et `AVIS.md`.
- L'ADR-0029.
- Les avis précédents : `docs/adr-0029/g0-sim/revue-t2/AVIS-SIM-T2.md` (risque 3) et `revue-t3/AVIS-SIM-T3.md`.
- L'annexe B, blocs B.61, B.62, B.64 et B.66 seulement. B.61 porte FIV-IDENTIF-1 : le déclencheur PLAN-S2BIS-2 passe avant tout acte A-2.

## Ce qui est demandé

1. **Pour chaque question Q-T4-1 à Q-T4-13** : Adopté, Modifié ou Rejeté. Donne un motif sourcé, et marque [G0] si la question touche la lettre du G0, [E0] si elle doit être tranchée avant E0.
2. **Constat du point 9.** La famille E1 culmine vers FIV(240) ≈ 2 contre 22,9 et 34,6 pour EP.
   - Que dit le G0 de ce cas ?
   - Faut-il déclencher PLAN-S2BIS-2 maintenant, sans attendre E1 complet ?
   - Faut-il élargir la grille d'E1 avant E0 ? Est-ce licite, et à quel prix ?
   - Quel est l'effet sur la durée déclarée et sur le calendrier ?
   - Qu'est-ce qui reste une question de valeur pour l'investisseur, et comment la lui poser simplement ?
3. **E-4** : le coup d'œil sur des FIV avant E0 est-il un écart au pré-enregistrement ? Que faut-il écrire ?
4. **Estimation** : le lot passerait de 6 500 à 7 200 lignes. Quelle conséquence pour le plan ?
5. **Trois risques au plus** pour SB-11 à SB-13.

## Interdits

- `docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, `docs/adr-0028/execution/` ;
- tout `*.jsonl` ;
- toute pièce de D.2 ;
- aucune recherche récursive, y compris par Glob, sur `docs/`, sur le dépôt ou sur le scratchpad.

Gate 0 : l'identifiant exact du modèle et l'effort, en tête.
