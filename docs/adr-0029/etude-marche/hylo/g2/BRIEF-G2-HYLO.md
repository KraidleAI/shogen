# Brief — relecture G2 de l'étude « Hylo et protocoles d'autres chaînes dépendant d'oracles »

Tu es **réviseur G2 neuf** (`shogen-worker`) : tu n'as rien écrit de cette pièce. Dépôt `/home/user/shogen` (lecture seule ; **aucune
opération git en écriture**). Lis `date -u` avant toute date. Tu écris seulement dans
`<scratchpad>/s2bis/marche2/hylo/g2/` (rapport `G2-HYLO.md`).

Pièce : `…/marche2/hylo/HYLO-ET-AUTRES-CHAINES.md` (lecteur `claude-sonnet-5-5`), son brief `BRIEF-HYLO-SOLANA.md`, ses copies
(`pages/`, `pages2/`), `quotes.txt`, `chk.py`, `SHA256SUMS`. Contexte : `docs/adr-0029/etude-marche/SYNTHESE-CROISEMENT.md`.
Destination prévue après relecture : `docs/adr-0029/etude-marche/` (pièce de contexte commercial, non normative).

Contrôles : (1) empreintes (`sha256sum -c`) ; (2) **citations** : par ton propre script, chaque citation “ ” du rapport retrouvée
verbatim dans la copie qu'il désigne ; aucune « » pour du texte web ; (3) **faits techniques sur Hylo** (un seul oracle Pyth ; USDC
en contrôle de parité ; bornes 1–60 s et 5 % ; épinglage du crate Pyth ; constats d'audit touchant l'oracle et leur statut) : vérifie
chacun dans le code SDK et les audits copiés ; (4) chiffres DefiLlama (TVL, hyUSD, pic) recalculés depuis `llama-*.json` ;
(5) **incidents** : chaque incident attribué à un acteur nommé porte une source lue, une date et un niveau de confiance ; aucune
défaillance présentée comme établie au-delà de ce que dit la source ; vocabulaire du registre 09 (lis `docs/09-vocabulaire.md`) ;
attention particulière aux affirmations sur Switchboard, Moonwell, Drift, Hyperliquid, MarginFi, Scallop ; (6) niveaux [lu]/[inféré]
cohérents ; limites déclarées suffisantes ; (7) prête à verser ? Liste fermée des corrections. Aucune opération réseau sauf sondage
(≤ 5 requêtes) pour lever un doute précis. Interdits : `docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`,
`docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, tout `*.jsonl` ; aucune recherche récursive sur tout `docs/`. Verdict : ACCEPTE,
ACCEPTE-AVEC-CORRECTIONS (liste fermée) ou REFUSE. Gate 0 (identifiant exact du modèle en tête). Résumé court en français.
