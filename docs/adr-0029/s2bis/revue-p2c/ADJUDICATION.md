# Adjudication de la tranche P2C (CB-7, CB-8) — orchestrateur, 2026-10-17 12:06:32 UTC (`date -u`)

- Générateur `shogen-worker`, Gate 0 `claude-opus-5-5` (456 occurrences, aucune autre), FM-1.1 : 0 ; `SHA256SUMS` : 452 lignes, toutes justes. Six diffs (CB-7a, 7b, 7c, 8a, 8b, 8c), plancher s2bis 374 → 394, 61 mutants tués, matrice Python 3.10 à 3.13 verte, S-G9 `docs/17:70` connu.
- **Q-1** (agrégateurs regroupés à quatre actifs, BTC compris, Bitfinex regroupé) : **accepté** : le G0 prime sur le brief (E-C-09, PROPOSITION l.170).
- **Q-2** (CB-7c : ETH coté en USDT chez binance et okx) : **gardé** : décision Q-CA-01 (a) adoptée au G0 de CALIB-ACTIFS (`g0-calib/AVIS.md` l.41) ; le diff reste isolé et retirable.
- **Q-3** (paires absentes : coinbase USDC/USD, okx USDC/USD et ETH/USD) : **aucun décodeur de substitution** ; OKX USDC-USDT est le témoin (CB-9), ETH-USDT d'OKX est déjà couvert par Q-CA-01 (a).
- **Q-4** (plafond Chainlink des stables porté dans l'extra du relevé) : **accepté** ; le recalc le lira dans l'extra (RB à venir).
- **Q-5** (`formes-pool.json` à part, fondu dans `formes.json` au gel ; `espace` vrai pour tout hôte à deux formes ou plus) : **accepté** ; fusion au gel.
- **Q-6** (un actif manquant met toute la lecture regroupée en panne) : **accepté** (ADR l.234 admet et déclare les pannes identiques entre actifs d'un même hôte).
- **Q-7** (nom de l'unité Binance : `api.binance.com` du harnais ou `data-api.binance.vision` de la mesure) : **décision au gel**, dans la configuration des hôtes, après la lecture des conditions (item FORMES-DOC-1) ; le code ne dépend pas de l'hôte.
- **Q-C-10** (budget OKX) : **pas de regroupement** ; cinq lectures séparées, budget tenu.
- **Items** : fermés SHOGEN-S2BIS-DECODEURS-TYPES-1 et SHOGEN-S2BIS-FORMES-BTC-1 (tests nommés) ; rendus faute de réseau : SHOGEN-S2BIS-HORODATAGE-SENS-1 et SHOGEN-S2BIS-FORMES-DOC-1 : lecture par un lecteur avant le gel (lot de lecture daté au gel du collecteur) ; I-1 (test `Bornes` sensible à la charge) : **correction C-P2C-1 à l'intégration** (test rendu indépendant de la charge), pas d'item.
- **Écarts E-1 à E-8** : admis ; E-1 et E-7 (énumérations récursives sur ses copies) et E-4 (essais pendant une campagne) notés, sans effet sur les verdicts ni sur le dépôt.
- **Suite** : intégrateur neuf (`s2bis/int-p2/`) : série P2C puis CB-9 rebasée, C-P2D-1 (classe `temoin`), C-P2D-2 (limites Curve), C-P2C-1, CB-16 ; puis G2 neuve sur la série intégrée ; puis chaîne par le modèle scellé.
