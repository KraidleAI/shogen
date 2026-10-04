# Brief — étude de Hylo et des protocoles d'autres chaînes qui dépendent d'oracles (qualitatif)

Chercheur `shogen-lecteur`, effort high. Dépôt `/home/user/shogen` (lecture seule ; **aucune opération git en écriture**). Lis `date -u`
avant toute date. Tu écris seulement dans `<scratchpad>/s2bis/marche2/hylo/`.

Demande de l'investisseur (2026-10-04), qui cite `https://x.com/hylo_so`. Contexte : `docs/adr-0029/etude-marche/SYNTHESE-CROISEMENT.md`
(ce que Shōgen mesure : les racines communes des sources de prix ; ce que S2-bis couvre : BTC, ETH, USDC, USDT).

1. **Hylo** : lis sur place son site officiel, sa documentation et ses dépôts publics : ce que fait le protocole (chaîne, produits,
   mécanisme), **d'où vient son prix** (quel oracle, quelles places en amont, combien de sources, que se passe-t-il si une source s'arrête
   ou diverge), sa taille (DefiLlama), son équipe et ses canaux officiels publics, ses audits ; ce que Shōgen pourrait lui apporter,
   concrètement ; ses risques d'oracle déclarés.
2. **Cinq à huit protocoles comparables sur d'autres chaînes que l'EVM principal** (Solana d'abord, puis Sui, Aptos, Hyperliquid,
   Base) qui dépendent d'oracles pour des actifs volatils ou des stablecoins (stablecoins adossés, prêt, perps) : même grille, plus
   courte ; choisis-les par leur dépendance à un ou plusieurs oracles, toutes tailles.
3. Incidents d'oracle documentés sur ces chaînes (2023-2026), avec source lue : ce qu'ils montrent pour Shōgen.
Sortie : `HYLO-ET-AUTRES-CHAINES.md` (une fiche par protocole, sources lues avec date, niveaux [lu] / [inféré]) ; copies des pages lues
et SHA256SUMS. Citations web non versées entre “ ” (jamais « »). Aucune prise de contact. Interdits : `docs/15-*`, `docs/16-*`,
`docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, tout `*.jsonl`. Gate 0 (identifiant exact).
Résumé court en français.
