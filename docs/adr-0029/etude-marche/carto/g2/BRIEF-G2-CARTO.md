# Brief — relecture G2 de la cartographie DefiLlama des protocoles DeFi dépendant d'oracles

Tu es **réviseur G2 neuf** (`shogen-worker`) : tu n'as rien écrit de cette pièce. Dépôt `/home/user/shogen` (lecture seule ; **aucune
opération git en écriture**). Lis `date -u` avant toute date. Tu écris seulement dans
`<scratchpad>/s2bis/marche2/carto/g2/` (rapport `G2-CARTO.md`).

Pièce : `…/marche2/carto/CARTO-DEFI-ORACLES.md` (lecteur `claude-sonnet-5-5`), son brief `BRIEF-CARTO-DEFI.md`, ses scripts
(`traite.py`, `enrichit.py`, `assemble.py`, `cibles.json`, `pourquoi.json`), ses réponses brutes (`raw/`, `out/`) et `SHA256SUMS`.
Contexte : `docs/adr-0029/etude-marche/` (étude de marché déjà versée ; ce que Shōgen mesure). Destination prévue après relecture :
`docs/adr-0029/etude-marche/` (pièce de contexte commercial, non normative).

Contrôles : (1) empreintes (`sha256sum -c`) ; (2) **recalcul indépendant** à partir de `raw/protocols.json` par ton propre script (pas
celui du lecteur) : périmètre A/B (424), avec oracle déclaré (246), mono-oracle (170) / multi (76), comptes Chainlink/Pyth/RedStone,
tableaux T0 et T1a au moins ; tout écart chiffré ; (3) la méthode : catégories et seuils écrits d'avance et appliqués tels quels,
règles d'exclusion, traitement des dates d'oracle, chaîne principale ; biais et surcomptages déclarés ; (4) les 30 cibles : chacune
conforme à la règle de `cibles.json` ou écart motivé ; doublons d'organisation ; familles déjà étudiées bien exclues ; (5) toute
affirmation hors DefiLlama porte un niveau ([lu]/[inféré]) et une source ; aucune affirmation de défaillance d'un protocole nommé
présentée comme établie ; vocabulaire du registre 09 (lis `docs/09-vocabulaire.md`) ; citations web entre “ ” jamais « » ;
(6) prête à verser ? Liste fermée des corrections. Aucune opération réseau sauf pour vérifier par sondage (≤ 5 requêtes) l'API
publique `https://api.llama.fi`. Interdits : `docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`,
`docs/adr-0028/monark-m009a/`, tout `*.jsonl` ; aucune recherche récursive sur tout `docs/`. Verdict : ACCEPTE,
ACCEPTE-AVEC-CORRECTIONS (liste fermée) ou REFUSE. Gate 0 (identifiant exact du modèle en tête). Résumé court en français.
