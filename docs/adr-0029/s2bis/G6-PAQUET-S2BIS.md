# Pièce G6 du paquet `s2bis/` (S2-bis) : composition et licences

- **Rattachement** : ADR-0029 §2.9 (R-8 : aucune dépendance Python neuve) ; G0 des lots COLLECTE-BIS, RECALC-BIS et
  DEPLOI-BIS (`docs/adr-0029/g0-collecte/`), question Q-G-06 de la proposition, adoptée par l'avis : pièce écrite à
  CB-0 (bibliothèque standard seule), complétée à DB-0 par le tableau R-8 des paquets système. Leçon de
  SHOGEN-G6-PIECE-RECALCUL-1 (annexe B d'ADR-0028, l.896).
- **Écrite** le 2026-10-04 (17:41 UTC, `date -u`), sous-lot CB-0a, par le worker `claude-opus-5-5` ; à relire en G2
  avec la partie P1.

## 1. Composition

| composant | origine | version | licence |
|---|---|---|---|
| `s2bis/` (paquet `shogen_s2bis` et ses tests) | ce dépôt | commit scellé du collecteur (paquet de S2-bis) | MIT OR Apache-2.0 (`LICENSE-MIT`, `LICENSE-APACHE`, `Cargo.toml` l.25) |
| interpréteur Python et sa bibliothèque standard | paquet `python3` de la distribution des observateurs ; image de la CI | 3.10 au moins (`sys.stdlib_module_names` dans les tests) ; suite passée sous 3.10.20, 3.11.15, 3.12.3 et 3.13.14 | licence de CPython (« PYTHON SOFTWARE FOUNDATION LICENSE VERSION 2 » et licences historiques, `LICENSE.txt` de l'interpréteur 3.12 lu sur l'hôte, l.73) ; l'interpréteur n'est pas redistribué par le paquet |
| fixtures BTC de `s2bis/tests/fixtures/btc/` (huit places, CB-6a ; CoinGecko, DefiLlama et Chainlink, CB-6b) | copies octet pour octet des fixtures de S2 (`s2-harness/tests/fixtures/`, commit `a6f3990` du 2026-08-05 : réponses d'API publiques gelées par `s2-harness/tests/capture.py`) ; sha256 comparés aux originaux par `tests/test_decodeurs.py` | instantané de S2 | données de tiers ; conditions de republication non établies sur pièce : SHOGEN-S2BIS-LICENCES-API-1 (ADR-0029 §8.1 ; pour le pool, avant le sceau) ; la copie n'ajoute rien aux octets déjà au dépôt sous `s2-harness/` |
| fixtures des actifs de `s2bis/tests/fixtures/actifs/` (CB-7 et CB-8) | écrites octet pour octet par le générateur du lot P2C depuis les formes de réponse de `docs/adr-0029/g0-calib/PAIRES-ET-TEMOIN.md` (tableau 1.2, §2), valeurs mesurées par le lecteur le 2026-10-08 (tableau 1.1, §2), champs élidés construits et déclarés au rapport du lot ; aucune capture (réseau interdit au lot) | pièce du 2026-10-08 | valeurs de tiers ; même réserve que la ligne précédente (SHOGEN-S2BIS-LICENCES-API-1) ; capture datée avant le gel : SHOGEN-S2BIS-FORMES-DOC-1 |
| fixtures du témoin de `s2bis/tests/fixtures/temoin/` (CB-9) | écrites octet pour octet par le générateur du lot P2D (`bc`, `printf`) : forme de réponse d'OKX de `docs/adr-0029/g0-calib/PAIRES-ET-TEMOIN.md` (tableau 1.2, champs lus seuls) et enveloppe JSON-RPC de la fixture BTC de Chainlink ; valeurs mesurées par le lecteur le 2026-10-08 (§3.1) ; mots de `slot0` non mesurés déclarés au rapport du lot (adjudication de la tranche D, Q-4) ; aucune capture (réseau interdit au lot) ; lot GEL-COLLECTEUR-1 (diff GEL-5) : Uniswap et Curve réécrits à la main en réponses groupées (trois réponses JSON-RPC, `eth_blockNumber` en id 1 et 3), mots inchangés ; blocs 26 149 791 (Uniswap, pièce l.90) et 26 149 796 (Curve, pièce l.94), puis 26 149 797 (un bloc de plus, valeur de test) ; Curve dans l'ordre 3, 1, 2 | pièce du 2026-10-08 | valeurs de tiers ; même réserve (SHOGEN-S2BIS-LICENCES-API-1) ; capture datée avant le gel : SHOGEN-S2BIS-FORMES-DOC-1 |

Aucune dépendance hors de la bibliothèque standard. Le contrôle est mécanique : `s2bis/tests/test_fitness.py` lit les
imports de chaque module par analyse syntaxique et refuse tout module hors de la bibliothèque standard et du
sous-paquet (frontière de la PROPOSITION §1 pt 2), ainsi que les imports dynamiques. Rien n'est installé : aucun
contrôle de registre R-8 n'est dû pour le paquet Python.

**Plate-forme : POSIX seulement** (C-6 (e) de la relecture G2 de la tranche A de P1, ajout du diff CB-2d,
2026-10-04). Le journal (`collecte/journal.py`) importe `fcntl` pour le verrou exclusif `flock` (E-C-16) ; ce module
de la bibliothèque standard n'existe pas sous Windows. Le paquet tourne sur Linux (observateurs Debian, image
`ubuntu-24.04` de la CI) et sur les systèmes POSIX qui fournissent `flock` ; sa suite de tests aussi.

## 2. À compléter à DB-0

Paquets système des observateurs (chrony, unbound pour O1, rsync, outil de pare-feu, python3) : tableau R-8 écrit
avant toute installation (SHOGEN-S2BIS-R8-PAQUETS-1 ; PROPOSITION E-D-04), versions relevées au descripteur
d'observateur (E-C-23).

## 3. Limite écrite

Aucune analyse statique de sécurité (SAST) ne tourne sur le paquet : un outil serait une dépendance nouvelle, soumise à
R-8 et à la décision de l'orchestrateur (Q-G-05 de l'avis, même forme que SHOGEN-SAST-PYTHON-RECALCUL-1, annexe B
l.916). En attendant : la présente limite, les fonctions de fitness (frontière d'imports, garde réseau des tests,
mêmes octets sous cinq graines de hachage) et la compilation de chaque module avec les avertissements en erreur.

## 4. Remplaçants écrits d'avance

*Ajout daté du 2026-10-17 (lot GEL-COLLECTEUR-1, diff GEL-2 ; Q-C-08 du G0 COLLECTE-RECALC-DEPLOI, PROPOSITION
l.347-351, adoptée par l'AVIS l.97 ; Q-7 de P2C ; avis de l'advisor du lot, Q-A)*. Liste fermée, par unité : un
remplaçant n'est lu que par le processus secondaire, hors du vote ; la bascule vers lui n'est possible qu'avant le
sceau, et refait le rodage selon Q-C-06 (7 jours, dont un week-end, AVIS l.95).

| unité ou rôle | en service au gel | remplaçant | même chemin et même décodeur | motif |
|---|---|---|---|---|
| binance (pool, quatre formes `binance_*`) | `data-api.binance.vision` | `api.binance.com` (hôte de S2) | oui : chemins `/api/v3/ticker/price?symbol=…` et décodeurs `binance_*` inchangés | `api.binance.com` rend le code 451 depuis le poste de mesure (`docs/adr-0029/g0-calib/PAIRES-ET-TEMOIN.md` l.37, l.131) ; la réponse de l'un et l'autre hôte depuis des hôtes européens n'est pas mesurée : à vérifier par `smoke` à DB-2, depuis chaque observateur. Limite : une restriction par la localisation de l'adresse source frapperait aussi le remplaçant, qui ne vaut que contre une panne propre à `data-api.binance.vision` (avis de l'advisor, Q-A) |
| nom témoin de D-5 (`sante.json`, `noms` : `www.kernel.org`, `www.arin.net`) | les deux noms | `www.cern.ch` | sans objet (sonde D-5, requête A au résolveur de l'observateur) | lecture des noms témoins du 2026-10-17 et son adjudication (lot GEL-COLLECTEUR-1) : TTL servi de 60 s, autorités et adresses hors des ASN du pool et distinctes de celles des deux témoins ; réserve : un seul opérateur (AS513) ; TTL d'origine et ASN à confirmer au rodage (ADR-0029 l.110) |

## 5. USDC : les deux mesures et leur écart (Q-C-07)

*Ajout daté du 2026-10-18 (lot GEL-COLLECTEUR-1, diff GEL-8 ; Q-C-07 du G0 COLLECTE-RECALC-DEPLOI, PROPOSITION
l.342-346, AVIS l.96 ; avis de l'advisor du lot, Q-C, adopté). Numéros de l'ADR-0029 au commit `e16956b`, convention
de `FORMAT-JOURNAUX-S2BIS.md`.* Réponse acceptée à la q. 10 : `USDC : les deux mesures, contre le dollar réel et telle
que la DeFi la consomme, avec leur écart` (JOURNAL l.382, texte recopié à la PROPOSITION l.343-344). Traduction
retenue, **aucune forme nouvelle** au gel de `s2bis/config/formes.json` :

- **contre le dollar réel** : la classe USDC/USD des places qui servent la paire (ADR-0029 l.171), formes
  `kraken_usdc`, `bitstamp_usdc`, `gemini_usdc`, `binance_usdc` et `bitfinex_groupe` (`tUDCUSD`), avec les
  agrégateurs `coingecko_groupe` et `defillama_groupe` (`usd-coin`) ;
- **telle que la DeFi la consomme** : `chainlink_usdc`, classe « borné » au recalcul, plafond de 1,05 porté en extra
  et jamais appliqué par le collecteur (FORMAT §9.1), et l'ensemble témoin sur chaîne et chez OKX, `okx_usdc_usdt`,
  `uniswap_usdc_usdt`, `curve_usdc_usdt`, de classe `temoin`, hors des classes USD et hors du vote (ADR-0029 l.172),
  porteur de P_j ;
- **leur écart** : un calcul sur ces relevés, non une lecture : il relève de RB-2 (Q-R-04 : écart au pair des médianes
  des classes USD ; P_j du témoin ; filtre de la classe `temoin` hors des classes USD et du vote,
  SHOGEN-S2BIS-TEMOIN-RECALC-1), daté pour le témoin par ses blocs (FORMAT §9.1, bloc du témoin, diff GEL-5).

Limite écrite, recopiée de l'ADR-0029 l.171 : trois places liquides seulement cotent USDC contre le dollar fiat
(Kraken, Bitstamp, Bitfinex ; Gemini liste la paire ; aucun marché USDC-USD chez Coinbase) ; la condition N ≥ 4
répondantes de la classe USDC/USD dépend donc des agrégateurs et de l'oracle.

## 6. Carte descriptive : date de coupure

*Ajout daté du 2026-10-18 (lot GEL-COLLECTEUR-1, diff GEL-8 ; Q-G-04 de l'AVIS du G0, l.72-78 : `fixer maintenant
la date de coupure de la carte égale au gel du collecteur` ; Q-C-09, AVIS l.98).* La date de coupure de la carte est
celle du gel du collecteur, c'est-à-dire du commit qui verse ce lot. Aucun lot CB-14 n'est prêt à cette date : aucune
source n'entre à la carte avant le rendu ; les sources passent après le rendu, hors paquet (AVIS l.77). Le processus
secondaire tourne alors avec une carte vide, que le schéma admet (`entree.CARTE`, `formes` : liste vide admise ; le
relevé ASN tourne sans carte, FORMAT §15).
