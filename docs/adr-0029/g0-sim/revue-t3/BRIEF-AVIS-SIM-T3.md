# Brief — avis de l'advisor sur les seize questions de conception de SIM-BIS, tranche 3 (Q-T3-1 à Q-T3-16)

Tu es l'advisor du projet (`shogen-advisor`, R-26). Tu n'agis pas : tu ne lances aucune commande et tu ne modifies aucun fichier suivi.
- Lis `date -u` si tu dates.
- Tu écris seulement `<scratchpad>/s2bis/sim3/g2/AVIS-SIM-T3.md`.
- Tu rends aussi un résumé par message.

**But du projet**, à garder dans chaque recommandation : faire de Shōgen un standard institutionnel vendable, avec une ingénierie de pointe, sans baisse de qualité.

## Pièces
- Rapport du worker transcrit : `…/sim3/g2/RAPPORT-WORKER-SIM-T3-transcrit.md`, en particulier §7 (contrat RB-6), §8 (questions) et §10 (items).
- Diffs : `…/sim3/diffs/`. Lis `observateurs.py`, `regle.py` et `parametres.json` dans les diffs.
- G0 `docs/adr-0029/g0-sim/G0-SIM-BIS.md`, avec `PROPOSITION.md` et `AVIS.md`.
- ADR-0029.
- Avis précédents :
  - `docs/adr-0029/g0-sim/revue-t2/AVIS-SIM-T2.md` ;
  - `…/s2bis/rb1/g2/AVIS-RB-T1.md` (contrat de rotation, Q-RB-5, Q-RB-12, Q-RB-13).
- Annexe B : blocs B.61 à B.64 seulement.

## Ce qui est demandé
- **Pour chaque question** :
  - Adopté, Modifié ou Rejeté ;
  - un motif court, sourcé par fichier et ligne ;
  - [G0] si la question touche la lettre du G0, [E0] si elle doit être tranchée avant E0 (exécution des simulations).
- **Pour chaque item P-1 à P-9** : former ou non, avec le déclencheur.
- **Cohérence avec le recalcul** : dis si les onze points du §7 du rapport suffisent pour que l'oracle croisé SB-13 garde son sens, en particulier l'identifiant haché (noms courts ou noms d'hôte), Q-T3-15 (première unité après les retraits) et l'égalité des seuils.
- **Trois risques au plus** pour SB-9 à SB-14.

## Interdits
- `docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, `docs/adr-0028/execution/` ;
- tout `*.jsonl` ;
- toute pièce de D.2 ;
- toute recherche récursive sur `docs/`, sur le dépôt ou sur le scratchpad entiers.

Gate 0 : l'identifiant exact du modèle et l'effort, en tête de l'avis.
