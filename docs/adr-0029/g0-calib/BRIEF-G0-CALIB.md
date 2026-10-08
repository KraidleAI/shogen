# Brief — proposition de G0 du lot CALIB-ACTIFS (ETH/USD, USDC/USD, USDT/USD : τ, planchers, σ, paires servies, historiques)

Tu es le rédacteur de la proposition de G0 (`shogen-worker`, effort max). Tu écris un document de conception, pas de code. Dépôt `/home/user/shogen` en lecture seule (`git --no-optional-locks`), aucune écriture git. `date -u` avant toute date. Tu écris seulement dans `<scratchpad>/s2bis/calib2/` (scratchpad = `<scratchpad>`) : `PROPOSITION-CALIB.md` et `NOTES.md`.

## Pourquoi
ADR-0029 (révision 3, §2.6, DÉC D-4, l.185-191 et le tableau l.63) prévoit le lot CALIB-ACTIFS avant le sceau : S2 n'a aucune donnée pour ETH et les stables ; règle de τ, planchers, σ = 1,5 × heartbeat ; décalage du sceau **sous condition** (si le G0 établit les historiques, au moins 4 places par classe), sinon seconde vague. Le collecteur attend ce G0 pour CB-7 (décodeurs ETH, USDC, USDT) et CB-8 (agrégateurs, Chainlink), et le recalcul pour RB-2 ; l'item SHOGEN-S2BIS-CALIB-L189-1 (annexe B l.1086) y renvoie.

## Pièces
- ADR-0029 (§2.5, §2.6, §7 n° 5, ajouts datés) ; `DECISIONS-ARCHITECTURE-S2BIS.md` (D-4) ; `AVIS-QUESTIONS-TECHNIQUES-V3.md` ; `ETUDE-POOL-BIS.md` ; `docs/adr-0029/calib/SOURCES-HISTORIQUES.md` et `SHA256SUMS-ECHANTILLONS.txt` ; `G0-lots-S2BIS.md`.
- Le relevé du lecteur de cette passe : `<scratchpad>/s2bis/calib2/PAIRES-ET-TEMOIN.md`.
- G0 de collecte `docs/adr-0029/g0-collecte/` (PROPOSITION l.204-232, §2.6 l.310-320, AVIS) pour ce que CB-7 à CB-9 attendent.
- Annexe B : la ligne de SHOGEN-S2BIS-CALIB-L189-1 et les blocs qui nomment CALIB-ACTIFS, par recherche dans ce seul fichier.
- La forme : `docs/adr-0029/g0-plan2/PROPOSITION.md` et `docs/adr-0029/g0-sim/PROPOSITION.md`.

## Ce que doit contenir la proposition (`PROPOSITION-CALIB.md`)
1. Objet et rattachements.
2. **Paires servies** par hôte et par classe (depuis le relevé du lecteur), et ce que cela fait aux pools d'ETH, d'USDC et d'USDT (unités = hôtes de la liste du paquet qui servent la paire, ADR l.173).
3. **Historiques** : la condition « au moins 4 places par classe » lue sur `SOURCES-HISTORIQUES.md`, sous ses deux lectures (disponibilité ; republication des octets bruts permise), sans trancher : c'est une **question à l'investisseur** si elle engage le calendrier ou une licence.
4. **Règles de calcul** proposées (τ, planchers des agrégateurs et des oracles, σ = 1,5 × heartbeat, grille de 0,05 %), avec ce qui se calcule avant le sceau et ce qui ne le peut pas ; aucun calcul sur un historique dans cette passe.
5. **Exigences numérotées E-CA-nn**, sous-lots éventuels (≤ 200 lignes chacun), tests et oracles.
6. **Questions techniques Q-CA-n** pour l'advisor ; **questions de valeur, de calendrier, de licence ou de dépense, à part, en langage clair, pour l'investisseur** (aucune n'est tranchée par toi).
7. Calendrier, risques, items.

## Interdits
`docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, `docs/adr-0028/execution/` ; tout `*.jsonl` ; toute pièce de D.2 ; toute recherche récursive (grep -r, git grep, du, find large, Glob large) sur `docs/`, le dépôt entier ou le scratchpad entier ; rien sur Pocket.

Gate 0 : l'identifiant exact du modèle en tête. Rapport final par message (ta valeur de retour), court, en français.
