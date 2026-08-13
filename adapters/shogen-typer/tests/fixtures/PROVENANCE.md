# Provenance des fixtures du typeur

Chaque fixture est une **réponse réelle** d'un endpoint du pool S2
(`docs/10-mesures-pilotes-design.md` §3.1), conservée telle qu'elle est arrivée
— aucun octet réécrit, aucune indentation ajoutée. Les sha256 ci-dessous sont
mesurés (`sha256sum`), pas recopiés.

## Les deux captures Coinbase (cas acceptés)

| fichier | octets | sha256 | provenance |
|---|---|---|---|
| `coinbase-btc-usd-ticker-2026-08-05.json` | 186 | `3460af70ebae8008c4e7fd3a50a15aad38032cb106a9761aed3bff096ed0ba28` | **copie octet pour octet** de `s2-harness/tests/fixtures/coinbase.bin`, gelée par la campagne S2 du 2026-08-05 (`python -m tests.capture`) ; le sha256 des deux fichiers est **identique**, mesuré côte à côte |
| `coinbase-btc-usd-ticker-2026-08-13.json` | 180 | `e070427dbdcbd1cdd8d16bd8758be873fb30fae5c06aa874f73f4b1c7949d72f` | **capture propre à cette passe**, prise le 2026-08-13 à 04:08:53Z depuis `https://api.exchange.coinbase.com/products/BTC-USD/ticker` (`curl`, HTTP 200, 180 octets, `Accept: application/json`, aucune clé, aucun cookie — régime « strictement sans clé » de 10 §9.3) |

Les deux ne sont pas redondantes : celle du 2026-08-05 porte un prix à
**décimales** (`"64475.75"`, exposant −2), celle du 2026-08-13 un prix
**entier** (`"63577"`, exposant 0). Les deux chemins d'exposant sont donc
exercés sur du réel, pas sur du construit.

## Les douze autres flux du pool (cas de refus réels)

Copies octet pour octet des fixtures gelées de la campagne S2 du 2026-08-05
(`s2-harness/tests/fixtures/*.bin`). Elles servent de **cas de refus réels** :
ce sont de vraies réponses de vraies sources, mais d'endpoints que ce typeur
n'est pas — le refus attendu est nommé cas par cas dans `tests/commun/mod.rs`.

| fichier | octets | sha256 |
|---|---|---|
| `pool-binance-2026-08-05.json` | 45 | `880903276bc688eecfb02e8b5e30f60c6a195dda6c372bce445063f8621f61f5` |
| `pool-bitfinex-2026-08-05.json` | 95 | `42b787935cf66a065e0fadeb6042c529fecaae965180bfe14406a7da8e7bf27e` |
| `pool-bitstamp-2026-08-05.json` | 255 | `5b4ce336f72aba4775b339f676fc8b999ee068cd48c59adaf54f2509f0768c4c` |
| `pool-chainlink-2026-08-05.json` | 359 | `ab9a5a5e904fe3d6c64a6ecfa2a3341aac27c3b182e533434d4aa6eb8e2f8251` |
| `pool-coingecko-2026-08-05.json` | 54 | `80cec73dd3aa998f200a559fa0cbcc60890a6d0350c46bef175084e789c152da` |
| `pool-cryptocompare-401-2026-08-05.json` | 273 | `e54a34359ebeb4245031b742ee300e3fdd72ccf608d481d57caca1fc16147f17` |
| `pool-defillama-2026-08-05.json` | 116 | `8427d17ec5372179e39b0d69a25b188b64283669e657900e6f79829ba806e9d9` |
| `pool-gemini-2026-08-05.json` | 148 | `26b55ae19f60f415179dc3a20c8a1fd5ef5420a4683bb2a31dabcd2242daef65` |
| `pool-kraken-2026-08-05.json` | 308 | `c88fd8924700861f6d2e62c0250abe87bda8c17d7e96dd248d23f946d518f9ab` |
| `pool-okx-index-2026-08-05.json` | 189 | `f73ba748ed43eabf26766463a03731218b7a2b9c80e5e8f5514652bff1b86d9a` |
| `pool-okx-ticker-2026-08-05.json` | 365 | `fdf2d5be0c1d65a98ff2686bb0a3cba89ff6bb1ed455c741925f015c4e4fcb45` |
| `pool-pyth-2026-08-05.json` | 3027 | `ff2c769031ea556979768a53df430df791203116b736f2779ebe8323265359bb` |

## Ce qui n'est PAS ici

Les dires **construits** (JSON malformé, clé dupliquée, notation scientifique,
mantisse de quarante chiffres, substitut UTF-16 orphelin…) ne sont pas des
fixtures : ils vivent en clair dans `tests/commun/mod.rs`, étiquetés
`Origine::Construit`. Un dire construit ne doit jamais pouvoir se confondre
avec une réponse réelle rangée au même endroit.
