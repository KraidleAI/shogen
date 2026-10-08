# Brief — avis de l'advisor sur les quinze questions de conception de la tranche 1 du recalcul de S2-bis (Q-RB-1 à Q-RB-15)

Tu es l'advisor du projet (`shogen-advisor`, R-26). Tu n'agis pas : tu ne lances aucune commande et tu ne modifies aucun fichier suivi.

Lis `date -u` si tu dates. Tu écris seulement `<scratchpad>/s2bis/rb1/g2/AVIS-RB-T1.md`. Rends aussi un résumé par message.

**But du projet**, à garder présent dans chaque recommandation : faire de Shōgen un standard institutionnel vendable, avec une ingénierie de pointe et sans baisse de qualité. Décision de l'investisseur du 2026-10-05 : les advisors rendent aussi l'accord de fin de partie.

## Pièces
- Le rapport du worker transcrit : `…/rb1/g2/RAPPORT-WORKER-RB-T1-transcrit.md`. Lis le §3 (les questions) et le §4 (les items).
- Les diffs : `…/rb1/diffs/`. Lis `rotation.py`, `config_analyse.py`, `lecteur.py` et le gabarit `analyse.json`, dans les diffs.
- Le G0 `docs/adr-0029/g0-collecte/G0-COLLECTE-RECALC-DEPLOI.md`, avec `PROPOSITION.md` et `AVIS.md`.
- ADR-0029.
- Le FORMAT `docs/adr-0029/s2bis/FORMAT-JOURNAUX-S2BIS.md`.
- Le G0 de SIM-BIS `docs/adr-0029/g0-sim/G0-SIM-BIS.md` : SB-13 sera l'oracle croisé de RB-6.
- L'annexe B : blocs B.60 à B.64 seulement.

## Ce qui est demandé
- **Pour chaque question** :
  - **Adopté**, **Modifié** ou **Rejeté** ;
  - un motif court, sourcé par fichier et ligne ;
  - la marque **[G0]** si la question touche la lettre du G0, **[E0]** si elle doit être tranchée avant le gel du collecteur ou avant l'exécution du recalcul.
- **Pour chaque item I-1 à I-8** : former ou non, avec le déclencheur et le propriétaire.
- **Trois risques au plus** pour la suite de P3 et de P4 (RB-2 à RB-20), au regard de l'estimation révisée (×1,85).

## Points d'attention
- **Q-RB-1** : copie ou frontière desserrée.
- **Q-RB-3** : noms des classes, à reprendre tels quels par CB-6 à CB-9.
- **Q-RB-5** : ordre des unités sur les identifiants DNS.
- **Q-RB-9** : borne de 640 chiffres, et I-1 côté écrivain.
- **Q-RB-10** : portée d'une rupture sans reprise.
- **Q-RB-12** : contrat de rotation partagé avec SIM-BIS. Cohérence avec `sources.indices_hotes` et l'ordre des unités de SIM-BIS.

## Interdits
- `docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, `docs/adr-0028/execution/` ;
- tout `*.jsonl` ;
- toute pièce de D.2 ;
- aucune recherche récursive sur `docs/`, sur le dépôt ou sur le scratchpad entiers.

Gate 0 : l'identifiant exact du modèle et l'effort, en tête de l'avis.
