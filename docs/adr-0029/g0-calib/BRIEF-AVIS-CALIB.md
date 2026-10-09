# Brief — avis de l'advisor sur la proposition de G0 du lot CALIB-ACTIFS

Tu es l'advisor (`shogen-advisor`, R-26). Tu n'agis pas : écris seulement `<scratchpad>/s2bis/calib2/AVIS-CALIB.md` (scratchpad = `<scratchpad>`), et rends un résumé par message.

**But du projet** : faire de Shōgen un standard institutionnel vendable, sans baisse de qualité ; aucune durée ni aucun seuil ne doit reposer sur un artefact.

## Pièces
- La proposition `…/calib2/PROPOSITION-CALIB.md`, le relevé du lecteur `…/calib2/PAIRES-ET-TEMOIN.md`, les notes du rédacteur.
- ADR-0029 (§2.5, §2.6, §7 n° 5) ; `DECISIONS-ARCHITECTURE-S2BIS.md` (D-4) ; `docs/adr-0029/calib/SOURCES-HISTORIQUES.md` ; G0 de collecte (`docs/adr-0029/g0-collecte/`).

## Ce qui est demandé
1. Pour chaque question Q-CA-n : Adopté, Modifié ou Rejeté, avec un motif sourcé ; [G0] si elle touche la lettre de l'ADR ou d'un G0.
2. Les paires servies et les pools qui en découlent : justes, suffisants pour CB-7 et CB-8 ?
3. Les règles de calcul (τ, planchers, σ) : justes, et qu'est-ce qui doit être scellé avant le sceau ?
4. La condition des historiques (au moins 4 places par classe) et la licence : ce qui est technique (à toi) et ce qui revient à l'investisseur (calendrier : décalage du sceau ou seconde vague ; licence ; dépense), en langage clair.
5. Ce qui débloque CB-7, CB-8, CB-9 et RB-2 dès l'adjudication, et ce qui attend.
6. Trois risques au plus.

## Interdits
`docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, `docs/adr-0028/execution/` ; tout `*.jsonl` ; toute pièce de D.2 ; toute recherche récursive, y compris par Glob, sur `docs/`, le dépôt ou le scratchpad ; rien sur Pocket.

Gate 0 : l'identifiant exact du modèle et l'effort, en tête.
