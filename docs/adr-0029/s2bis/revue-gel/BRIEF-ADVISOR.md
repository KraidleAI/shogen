# Brief advisor — lot GEL-COLLECTEUR-1 (gel du collecteur de S2-bis, Q-C-06)

Dépôt : /home/user/shogen. Trois choix techniques réels ; réponse courte et motivée par question (options, recommandation, risques). Ne modifie rien dans le dépôt ; écris l'avis dans <scratchpad>/s2bis/gel/AVIS-ADVISOR.md.

Interdits : docs/15-*, docs/16-*, docs/pocket-report/, docs/rapports/, docs/adr-0025/, docs/adr-0028/monark-m009a/, docs/adr-0028/execution/, tout fichier *.jsonl ; aucune recherche récursive sur docs/ (lis les fichiers nommés ci-dessous, aux lignes indiquées). Règle : toute commande git qui liste ou compare des chemins est limitée à une liste explicite de chemins ; ici tu n'as besoin d'aucune commande git.

## Sources à lire
- docs/adr-0029/g0-calib/PAIRES-ET-TEMOIN.md:11, docs/adr-0029/g0-calib/PAIRES-ET-TEMOIN.md:37, docs/adr-0029/g0-calib/PAIRES-ET-TEMOIN.md:44, docs/adr-0029/g0-calib/PAIRES-ET-TEMOIN.md:131 (Binance : l'hôte du harnais rend un code 451 depuis le poste de mesure ; l'hôte « données de marché seulement » est documenté par Binance).
- docs/adr-0029/g0-collecte/PROPOSITION.md:343 à docs/adr-0029/g0-collecte/PROPOSITION.md:351 (Q-C-07, Q-C-08) ; docs/adr-0029/g0-collecte/AVIS.md:95 à docs/adr-0029/g0-collecte/AVIS.md:98.
- docs/adr-0029/ADR-0029-campagne-S2-bis.md:166 à docs/adr-0029/ADR-0029-campagne-S2-bis.md:175 ; docs/adr-0029/ADR-0029-campagne-S2-bis.md:220 à docs/adr-0029/ADR-0029-campagne-S2-bis.md:224 ; docs/adr-0029/ADR-0029-campagne-S2-bis.md:234.
- docs/adr-0028/ANNEXE-B-items.md:1980 (item SHOGEN-S2BIS-TEMOIN-BLOC-1, ouvert) ; docs/adr-0028/ANNEXE-B-items.md:1983 (SHOGEN-S2BIS-NOM-FORME-1, ouvert).
- Code : s2bis/shogen_s2bis/collecte/decodeurs.py (décodeurs Uniswap v3 et Curve par `eth_call`, l.193 à l.262), s2bis/config/formes-pool.json, s2bis/shogen_s2bis/collecte/http.py.

## Questions
Q-A. Nom de l'hôte de l'unité « binance » au gel : `data-api.binance.vision` (documenté par Binance pour les données publiques, sans clé, répond depuis le poste de mesure) ou `api.binance.com` (hôte du harnais S2, code 451 depuis le poste de mesure). Les observateurs seront déployés sur des hôtes européens. Quel hôte inscrire dans la configuration des formes, et faut-il un remplaçant écrit d'avance (Q-C-08) ?

Q-B. SHOGEN-S2BIS-TEMOIN-BLOC-1 : comment dater une lecture on-chain du témoin (Uniswap v3 `slot0`, Curve `get_dy`, par `eth_call`) ? Options : (1) `eth_blockNumber`, puis `eth_call` épinglé à ce bloc, puis `eth_getBlockByNumber` pour l'horodatage du bloc ; (2) requête JSON-RPC groupée [`eth_blockNumber`, `eth_call` latest] en un aller, sans atomicité garantie ; (3) `eth_call` sur « latest » et bloc lu par un `eth_blockNumber` séparé. Le relevé doit porter un champ bloc dans son extra ; le recalc (RB-2) datera la mesure. Budget des RPC publics à respecter.

Q-C. Q-C-07 (« USDC : les deux mesures, contre le dollar réel et telle que la DeFi la consomme, avec leur écart ») : confirmes-tu la lecture de docs/adr-0029/g0-collecte/AVIS.md:96, qu'aucune forme nouvelle n'est nécessaire au gel de `formes.json` (classe USDC/USD des places fiat, Chainlink USDC/USD borné, ensemble témoin ; écart calculé au recalc, Q-R-04) ? Si une forme manque, nomme-la.

## Format
Trois sections Q-A, Q-B, Q-C ; chaque fait cité avec fichier:ligne ; conclure par « Recommandation » en une ligne par question.
