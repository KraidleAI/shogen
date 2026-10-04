# Brief — cartographie des protocoles DeFi qui dépendent d'oracles, toutes chaînes, toutes tailles (source : DefiLlama)

Chercheur `shogen-lecteur`, effort high. Dépôt `/home/user/shogen` (lecture seule ; **aucune opération git en écriture**). Lis `date -u`
avant toute date. Tu écris seulement dans `<scratchpad>/s2bis/marche2/carto/`.

Demande de l'investisseur (2026-10-04) : « as tu étudié d'autres acteurs sur d'autres blockchain ? acteur DeFi. petits, moyens, gros. pas
que AAVE. il faudrait chercher sur defilama ? ». But : trouver les clients et partenaires possibles de Shōgen (mesure des racines communes
des sources de prix), au-delà d'Aave. Contexte : `docs/adr-0029/etude-marche/SYNTHESE-CROISEMENT.md` et `P1-DEFI-PRET.md` (déjà étudiés :
Aave, Spark, Morpho, Euler, Compound, Kamino, Venus) ; décisions de l'investisseur au JOURNAL (premier acheteur visé : un protocole DeFi).

Travail, **par l'API publique et gratuite de DefiLlama** (`https://api.llama.fi/protocols`, `https://api.llama.fi/oracles` ou
équivalents ; lis la documentation `https://api-docs.defillama.com/` d'abord ; aucune clé, aucun compte) :
1. Télécharge et garde (sha256) les réponses brutes ; date de lecture.
2. Retiens les protocoles **qui dépendent d'un prix externe** : catégories prêt, CDP et stablecoins adossés à des actifs volatils, dérivés
   et perps, options, actifs réels tokenisés, rendement à levier, et toute catégorie où le champ des oracles est renseigné.
3. Classe-les en **trois tailles** par valeur déposée (seuils écrits d'avance : par exemple > 1 Md$, 50 M$ à 1 Md$, 1 à 50 M$ ; dis
   lesquels tu retiens et pourquoi) et **par chaîne** (Ethereum, Solana, Base, Arbitrum, BNB Chain, Sui, Aptos, Avalanche, Hyperliquid,
   Tron, autres).
4. Pour chacun : catégorie, chaînes, valeur déposée, **oracles déclarés** (Chainlink, Pyth, RedStone, Chronicle, Switchboard, API3,
   internes…), nombre d'oracles (un seul oracle = dépendance unique ; plusieurs = question des racines communes, notre sujet).
5. Tableaux de synthèse : par chaîne × taille ; par oracle (valeur sécurisée, nombre de protocoles) ; **liste courte de 30 cibles**
   (10 grandes, 10 moyennes, 10 petites), réparties sur plusieurs chaînes, avec pour chacune pourquoi elle serait intéressée (dépendance à
   plusieurs oracles, incidents d'oracle connus si tu en trouves une source lue, actifs couverts par S2-bis : BTC, ETH, USDC, USDT).
6. Limites : ce que DefiLlama déclare n'est pas vérifié (le dire) ; niveaux [lu] / [inféré].
Sortie : `CARTO-DEFI-ORACLES.md` (tableaux, liste courte, méthode, limites) ; données brutes et script de traitement (rejouables) ;
SHA256SUMS. Citations web non versées entre “ ” (jamais « »). Aucune prise de contact. Interdits : `docs/15-*`, `docs/16-*`,
`docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, tout `*.jsonl`. Gate 0 (identifiant exact).
Résumé court en français.
