# Brief — lecteur : paires servies par hôte (SHOGEN-S2BIS-PAIRES-1) et pièces du témoin (CB-9), lues sur pièce

Lecteur `shogen-lecteur` (`claude-sonnet-5-5`, effort high). Tu écris seulement dans `<scratchpad>/s2bis/calib2/` (scratchpad = `<scratchpad>`) : `PAIRES-ET-TEMOIN.md` et `NOTES.md`. Dépôt `/home/user/shogen` en lecture seule, aucune écriture git. `date -u` avant toute date.

## Objet
Préparer, **sans rien décider**, les faits dont le G0 de CALIB-ACTIFS et les sous-lots CB-7 à CB-9 du collecteur ont besoin :
1. **Paires servies.** Pour chaque hôte du pool de BTC de S2-bis (liste à établir depuis ADR-0029 §2.5, `docs/adr-0029/ETUDE-POOL-BIS.md` et `docs/adr-0029/calib/SOURCES-HISTORIQUES.md`), dis si l'hôte sert en temps réel ETH/USD, USDC/USD et USDT/USD (ou la paire la plus proche qu'il publie : ETH-USDT, USDC-USDT…), par quel point d'accès public sans clé, dans quelle forme de réponse (champs, unités, horodatage), avec une citation de la documentation officielle. Pour les flux Chainlink ETH/USD, USDC/USD, USDT/USD : adresse du flux, réseau, seuil de déviation et heartbeat publiés, lus sur la page officielle (data.chain.link ou docs.chain.link).
2. **Témoin (CB-9).** OKX USDC-USDT (point d'accès public), pool Uniswap v3 USDC/USDT sur Ethereum (adresse, frais, lecture `slot0`), pool Curve des stables (adresse, méthode de lecture) : adresses lues sur pièce officielle, avec citation ; hôtes RPC publics sans clé qui permettent un `eth_call`, lus sur pièce.

## Méthode
- Sources officielles seulement (documentation de l'hôte, page du contrat, explorateur public pour confirmer une adresse) ; `curl` par le proxy de la session ; aucune clé, aucun compte, aucune dépense, aucune écriture vers un service.
- Une requête de lecture publique **sur un point d'accès documenté** est permise pour confirmer la forme d'une réponse ([mesuré]) ; pas plus de quelques requêtes par hôte.
- Niveaux : [lu] (URL et date), [mesuré] (requête réelle de cette passe), [abs] (introuvable), [inféré]. Citations de 25 mots au plus, entre “ ”, avec l'URL. Aucun chiffre de seconde main.
- Ce que tu ne trouves pas est rendu [abs], jamais comblé.

## Interdits
`docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, `docs/adr-0028/execution/` ; tout `*.jsonl` ; toute pièce de D.2 ; toute recherche récursive sur `docs/`, le dépôt ou le scratchpad entiers ; rien sur Pocket (ni ses points d'accès, ni sa documentation, ni ses portails).

## Rendu
`PAIRES-ET-TEMOIN.md` : un tableau hôte × paire (servie oui / non / [abs], point d'accès, forme, citation), un tableau des flux Chainlink, un tableau du témoin, la liste des limites. Rapport final par message (ta valeur de retour), Gate 0 en tête, court.
