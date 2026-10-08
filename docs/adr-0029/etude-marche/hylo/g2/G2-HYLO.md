# G2 — relecture de « Hylo et protocoles d'autres chaînes dépendant d'oracles »

- **Gate 0** : modèle qui m'exécute : `claude-opus-5-5` (identifiant exact ; worker `shogen-worker`, effort `max`). Conforme au roster du CLAUDE.md §7.
- **Rôle** : réviseur G2 neuf. Je n'ai écrit aucune ligne de la pièce, générée par un lecteur `claude-sonnet-5-5` (réviseur ≠ générateur).
- **Date** : `date -u` lu à 20:50 UTC puis 21:13 UTC, le 2026-10-04.
- **Pièce relue** : `marche2/hylo/HYLO-ET-AUTRES-CHAINES.md`, sha256 `a24e7cf2a7d1fc551cb85a5024c8492825cc1624ce73a8f81aee39e35fb94f65` (inchangée du début à la fin de la relecture). Avec : `BRIEF-HYLO-SOLANA.md`, `pages/`, `pages2/`, `quotes.txt`, `chk.py`, `SHA256SUMS`.
- **Brief** : `marche2/hylo/g2/BRIEF-G2-HYLO.md`. Contexte : `docs/adr-0029/etude-marche/SYNTHESE-CROISEMENT.md`.
- **Dépôt** : `/home/user/shogen` lu seulement. HEAD valait `86c07ffe5bc827d818e48d9e735fd63ccbadf070` au début de la relecture et `e6d3cff08c06700de14472e6fad23441c31385c2` à la fin : cinq commits d'un tiers ont ajouté `docs/adr-0029/etude-marche/carto/` et modifié `JOURNAL.md`. Les fichiers du dépôt sur lesquels je m'appuie sont inchangés (sha256 identiques avant et après) : `docs/09-vocabulaire.md` (`001b9606…`), `SYNTHESE-CROISEMENT.md` (`69f9ddbb…`) et `xtask/src/sg4.rs`, `sg5.rs`, hors du diff. Le brief ne donne pas de base à comparer ; je consigne les deux. Aucune opération git en écriture.
- **Réseau** : aucune requête (0 sur les 5 permises).

---

## 1. Verdict

**ACCEPTE-AVEC-CORRECTIONS**, selon la liste fermée du §3 (C1 à C8).

Le socle tient :
- les 201 empreintes sont bonnes ;
- 96 des 97 citations “ ” sont retrouvées mot pour mot dans la copie que le rapport désigne, et il n'y a aucune « » ;
- les faits techniques centraux sur Hylo sont exacts : un seul oracle (Pyth), USDC en contrôle de parité seulement, bornes 1–60 s et 5 %, épinglage `=1.2.0` `pro-compatible` ;
- tous les chiffres DefiLlama se recalculent à l'identique ;
- chaque incident porte une source lue et une date.

Les corrections portent sur quatre points :
- les **audits** : la sévérité CRITIQUE d'OtterSec ADV-01 est omise, et les décomptes ne concordent pas ;
- des **précisions techniques** ;
- les **incidents** : niveaux de confiance absents, dates présentes dans les copies mais déclarées absentes, portée et chronologie de Switchboard, POPCAT sans oracle dans sa source ;
- le **registre 09** et la **provenance** de deux copies.

Aucune ne demande de nouvelle collecte.

## 2. Résultats des contrôles du brief

| # | Contrôle | Résultat |
|---|---|---|
| 1 | Empreintes | `sha256sum -c SHA256SUMS` : 201 OK, aucun échec, code de sortie 0. Couverture : chaque fichier du dossier hors `g2/` est listé, aucun fichier listé ne manque. |
| 2 | Citations | Mon script (`g2/work/cites.py`) part d'une table « citation → copie désignée » que j'ai établie en lisant le contexte de chaque ligne du rapport, et non `quotes.txt`. Résultat : 97 citations, dont 91 en octets exacts et 4 aux espaces près (sauts de ligne de `pdftotext`). Deux seulement passent en normalisation large. **L76** ne diffère que par l'échappement markdown `\$` de la source : le texte rendu est identique, c'est acceptable. **L142** commence par “each vault” (minuscule) alors que la source porte “Each vault” : c'est la correction C1. Aucune citation ne dépasse 25 mots (24 au plus). Aucune « ». Le seul guillemet droit est un littéral de code (Cargo.toml). En revanche, `quotes.txt` vérifie 8 citations contre une autre copie que celle désignée, et contient une ligne vide. Le `chk.py` du lecteur compare sans tenir compte de la casse : c'est ainsi que “Dual-Token Stablecoin” passait sur l'audit Accretion au lieu de DefiLlama. Voir C2. |
| 3 | Faits techniques Hylo | Exacts : un seul fournisseur, Pyth (docs et 7 fichiers SDK) ; USDC en contrôle de parité seulement, l'écart absolu au pair devant rester sous la tolérance (`validate_spot`), elle-même comprise entre 0,00001 et 0,001 (`MIN 10_000`, `MAX 1_000_000` en N9) ; bornes `MIN_INTERVAL_SECS = 1`, `MAX_INTERVAL_SECS = 60`, `MAX_CONF_TOLERANCE = 50_000_000` (= 0,05) ; `ORACLE_DIVISOR = 4` ; niveau `Full` ; fourchette prix ± conf ; épinglage `pyth-solana-receiver-sdk = { version = "=1.2.0", features = ["pro-compatible"] }` (ligne 40), conforme à la consigne de `pyth-upg-solana.txt` (l. 51–54) ; `hylo-core` 2.6.2 publiée le 2026-09-30T19:08:17Z, `0xPlish` seul publieur des 43 versions ; identifiants de flux SOL, BTC, ETH et USDC identiques aux “Popular Feed IDs” de `pyth-core.txt`. **Écarts** : sévérité d'ADV-01 et décomptes d'audit (C3) ; fenêtre de publication unilatérale, « spot/EMA » sans appui, « écart fixe », ETH/USD, Pythnet, contradiction entre deux pages Pyth (C4). |
| 4 | DefiLlama | Tous les chiffres se recalculent à l'identique (détail au §6.3) : TVL 68 383 779 $ au 2026-10-04 17:14:35 UTC ; 66,72 / 49,94 / 33,47 M$ ; pic 107 588 628 $ le 2026-01-15 ; hyUSD 26,04 M$ crypto-backed ; composition ; levée ; tailles des comparables. |
| 5 | Incidents | Les 12 lignes portent une source lue et une date, à une exception près : MarginFi, dont la date est pourtant **dans la copie** (C5 b). Sont relus sur les copies : faits, montants et dates de Loopscale, Moonwell (×4), Drift, JELLY, POPCAT, Scallop, Switchboard, Virtue et Full Sail. **Écarts** : aucun niveau de confiance par incident hors Scallop ; étiquettes [tiers] et [2nd] incohérentes ; portée et chronologie de Switchboard ; date du 2026-09-25 tirée d'une seconde main mais étiquetée [lu] ; POPCAT absent de toute mention d'oracle dans sa source ; familles du §3.3 non conformes au tableau (C5). Les affirmations sur MarginFi (“mass liquidations”, seuil de 10–20 k$), sur Drift et sur Scallop (prudence « non confirmée ») sont conformes. |
| 6 | Niveaux et limites | Les niveaux sont dans l'ensemble justes et prudents : le [abs] est employé à bon escient, Scallop est en faible confiance, Tracxn n'est pas retenu. Trois écarts : un [lu] posé sur une seconde main (Switchboard 2026-09-25) ; des dates déclarées [abs] alors qu'elles sont dans les octets reçus ; trois anomalies de provenance non déclarées (C8). Les limites du §6 du rapport sont réelles et bien rendues ; elles se complètent par C8. |
| 7 | Prête à verser ? | Pas en l'état ; oui après C1 à C8 (voir §5). |

## 3. Liste fermée des corrections (C1 à C8)

Les références « L » renvoient aux lignes de la pièce (sha256 `a24e7cf2…`). Les citations proposées ont été contrôlées au mot près dans les copies (§6.2).

**C1 — Citation non verbatim (§2.2, L142).** Remplacer “each vault requires a specific set of Pyth oracle accounts” par “Each vault requires a specific set of Pyth oracle accounts”. Source : `pages2/jupusd.txt`, octets identiques dans `jupusd.raw`.

**C2 — Contrôle des citations et sa description (L6, L284, `quotes.txt`, `chk.py`).**
- (a) Aligner les 8 lignes de `quotes.txt` sur la copie que le rapport désigne :
  - L32 (×2) → `pages/hylodocs-introduction.md` ;
  - L34 → `pages/hylodocs-product-guide-xassets.md` ;
  - L44 → `pages/llama-protocols.json` ;
  - L62 → `pages/hylodocs-technical-addendum-hylo-equations.md` ;
  - L138 “permissioned” → `pages2/pyth-pro-how.txt` ;
  - L143 → `pages2/jup-dev-llms.txt` (voir C8) ;
  - L182 → `pages2/thala-oracles.txt`.

  Supprimer la première ligne, dont la citation est vide.
- (b) Rendre la comparaison de `chk.py` sensible à la casse, puis le relancer : 0 problème attendu après C1.
- (c) L284 : remplacer « citations vérifiées » par « citations contrôlées par `chk.py` » (registre 09, l. 12–14). L6 : remplacer « contre le fichier copié » par « contre la copie que le rapport désigne ».

**C3 — Audits (§0 point 4 L18, §1.4 L96–98, §5 L256).**
- (a) OS-HYL-ADV-01 est **CRITIQUE**, statut RESOLVED, PR #200. Sources : OtterSec, pages imprimées 4 (tableau des sévérités : deux constats critiques), 5 (tableau des vulnérabilités) et 8 (en-tête du constat ADV-01, sévérité critique). Ajouter cette sévérité au §1.4 et au §0 point 4.
- (b) §0 point 4 : « Trois constats touchent l'oracle » contredit le §1.4, qui en cite six. Écrire : « six constats touchent l'oracle : ADV-01 (critique), ACC-H1 (haute), ADV-03, ACC-L1, ACC-L7 et ACC-L20 (basses), tous corrigés ».
- (c) §1.4, ADV-03 : ajouter « corrigé (PR #200) » (page imprimée 5 : RESOLVED ; page imprimée 11 : “Resolved in PR #200”).
- (d) §1.4, A26HYL1 : remplacer « 44 corrigés, 6 acceptés ou reconnus » par « 44 FIXED et 7 ACKNOWLEDGED au tableau des constats (pp. 3–5) ; la couverture écrit 44 et 6, soit 50 pour 51 constats ». Mon recomptage : moyens 13 F / 3 A ; faibles 24 F / 1 A ; informatifs 7 F / 3 A.
- (e) §1.4 et §5 : retirer « écart de date ». Le PDF d'OtterSec date lui-même l'évaluation, “conducted between February 10th and February 27th, 2025”, avec un suivi du 2 au 30 avril 2025. La couverture est datée du 5 mai 2025. La mention “Feb 2025” de la doc Hylo est donc la période d'évaluation, pas un écart.

**C4 — Précisions techniques Hylo et Pyth (§0 points 2 et 9, §1.1, §1.3, §1.6, §1.7, §4, §5).**
- (a) §1.3 point 2 (L69) : le code (`pyth-oracle.rs`, l. 132) ne teste que `publish_time + interval >= clock_time`. Une heure de publication en avance sur l'horloge Solana est donc acceptée : c'est la remédiation d'OtterSec ADV-03 contre la dérive d'horloge, et ACC-L7 (p. 49) décrit le même test. L'intervalle fermé `[clock − interval, clock]` est celui du commentaire (l. 119–120), pas du code.
- (b) L83 : supprimer « ou entre spot et EMA (OtterSec, ci-dessous) ». Le code lu ne lit pas l'EMA : aucune occurrence de `ema` dans `pyth-oracle.rs`. ADV-01 a remplacé l'EMA par le spot. Le seul contrôle de dispersion du code lu est le rapport conf/prix.
- (c) L35 « corrigé d'un écart fixe » et L112 « l'écart appliqué est fixe » : écrire « écart en pourcentage qui varie avec le CR selon un barème fixe ». Source : `collateral-rebalancing.md`, “scales with how much the pool needs the flow” ; le “fixed schedule” de la page est le barème, pas l'écart.
- (d) ETH/USD. L118 « Hylo lit Pyth BTC/USD, ETH/USD (SDK) et USDC/USD ; S2-bis mesure déjà ces trois actifs » et L23 « BTC/ETH/USDC » : d'après les docs, Hylo lit BTC/USD et USDC/USD. ETH/USD n'est que défini dans le SDK, associé à WETH sous `#[cfg(feature = "offchain")]` (`feeds.rs`, l. 107–110). Son usage en production est [abs], et `tokensInUsd` ne contient aucun WETH. Ce traitement doit concorder avec le §1.1 (L37).
- (e) L16 : remplacer « (publié le 2026-09-30) » par « (crate `hylo-core` 2.6.2, publiée le 2026-09-30) ». Sinon, la date semble porter sur le récepteur Pyth.
- (f) L88 « Pythnet est supprimé » et L248 « Pythnet supprimé » : écrire « Pythnet est en cours d'arrêt » (“is being shut down”, `pyth-aggregation.txt`).
- (g) Compléter le §5 et qualifier le §1.3 (L90) et le §0 point 2 (L16). `pyth-upg-contracts.txt` écrit, pour le 2026-08-26, “You kept your address, and your feed IDs didn't change” (sauf Sui). À l'inverse, `pyth-upg-solana.txt` et la section Solana de la même page annoncent de nouveaux comptes push par flux. Les deux pages Pyth ne disent pas la même chose ; pour Hylo, la conséquence reste [abs]. La table des comptes est rendue en JavaScript et absente de la copie.

**C5 — Incidents (§0 points 6 et 8, §2.4, §2.7, §3.1, §3.2, §3.3, §4, §5, §6).**
- (a) §3.1 : donner un **niveau de confiance par ligne**, exigé par le brief, et énoncer l'échelle. Aligner aussi les étiquettes sur la légende de L8. Aujourd'hui, [tiers] (CoinDesk, The Crypto Times, SolanaFloor, Chainalysis, Nexus) et [2nd] (Solana Compass, Startup Fortune, Shattered) désignent la même catégorie (presse ou analyste).
- (b) MarginFi : la date est dans la copie. `inc-marginfi-refund.raw` porte `article:published_time` 2024-04-19T19:29:12Z (modifiée le 2024-05-21), et l'article situe la déclaration “3 days after the incident”. À corriger :
  - §3.1 L201 : « sans date sur la page », « date [abs] » ;
  - §3.2 L216 : « sauf MarginFi (sans date sur la copie) » ;
  - §6 point 7 L274 : « aucune page datée collectée ». MarginFi est un incident de 2024 daté.
- (c) Autres dates présentes dans les octets reçus :
  - post-mortem de Switchboard : `article:published_time` 2026-09-18T20:45:56Z, contre « année non affichée, déduite 2026 » en L209 ;
  - Shattered : `datePublished` 2026-09-10, contre « page non datée » en L260.
- (d) Portée de l'incident Switchboard. Selon le post-mortem, l'exploitation documentée porte sur le **déploiement IOTA** (les quatorze oracles de la file IOTA). Full Sail (Sui) signale une perte après une compromission qu'il qualifie lui-même de “suspected”. Les quatre déploiements Move ont été suspendus, y compris sur des chaînes sans incident signalé. À corriger :
  - L20 : « une attaque sur ses déploiements Move » ;
  - la colonne chaîne de L209 ;
  - L222 : « a touché trois chaînes à la fois (IOTA, Sui, ensuite l'arrêt de toutes) ».

  En §2.7 (L179), préciser qu'aucune copie ne rapporte d'incident chez Suilend, Thala, Echelon ou Aries.
- (e) Fermeture de Switchboard. La date du 2026-09-25 ne vient que de Solana Compass [2nd] (“all support services ending on September 25”). Le profil X ne montre que le titre et un extrait ; l'arrêt effectif n'est pas lu [abs]. À corriger :
  - L20 (étiquette [lu]) ;
  - L178 : « annoncé sa fermeture au 2026-09-25 » ;
  - L245 : « le service arrêté le 2026-09-25 ».

  Rapporter aussi que Solana Compass présente la fermeture comme “a separate decision from that incident”, et retirer de L222 l'enchaînement « et la fermeture du fournisseur a suivi ».
- (f) L22 : remplacer « clés compromises » par « clé compromise (Drift) ou défaut d'attestation (Switchboard : “No keys were extracted”) ».
- (g) POPCAT : la copie `inc-hl-popcat.txt` ne mentionne aucun oracle et parle de “what appeared to be a deliberate attempt”. En L204 et L158, marquer le lien avec l'oracle comme [inféré], ou sortir l'événement du tableau des incidents d'oracle, et garder la prudence de la source.
- (h) §3.3 point 1 (L220) : aligner les familles sur le tableau du §3.1 et sur les sources.
  - wrsETH n'est pas une « configuration » : c'est un flux qui a “erroneously reported” (Anthias).
  - Loopscale relève d'une validation de programme manquante.
  - MarginFi relève d'un changement de configuration d'oracle pendant la congestion, avec décrochage de LST ; la source ne décrit aucune divergence entre places.

  Revoir en conséquence la phrase « dont une seule … relève de ce que R1 mesure en principe ».

**C6 — Registre 09 (relecture ; ces formes sont hors de la liste mécanisée par S-G4).**
- (a) « témoin indépendant » (L23, L118) : écrire par exemple « série de comparaison sur des places hors Pyth (recouvrement avec les éditeurs de Pyth non mesuré) ». Registre 09, l. 21.
- (b) L119 « Cela décide si ajouter un second oracle apporterait une vraie redondance » : écrire « Cela dirait si un second oracle partage des amonts nommés avec Pyth (recouvrement constaté ou non sur l'axe des places) ; l'indépendance n'en serait pas établie ». Registre 09, l. 21 et 27.
- (c) L138 « la preuve d'indépendance des racines manque » : écrire « aucune mesure du recouvrement de leurs racines n'est publiée ». Registre 09, l. 21.
- (d) L249 « ne sont pas des racines indépendantes tant que… » : écrire « restent des redondances déclarées : sans la liste des places derrière chaque flux, aucun recouvrement n'est mesuré ». Registre 09, l. 21 et 29.
- (e) L121 « la profondeur des places derrière Pyth HYPE/USD est la vraie question » et L165 « la profondeur … est la même question » : la profondeur est hors du périmètre de Shōgen (registre 09, l. 30 ; ADR-0007). Écrire « les amonts nommés derrière Pyth HYPE/USD ; leur profondeur n'est pas mesurée par Shōgen ».
- (f) « citations vérifiées » : voir C2 (c).
- (g) Surclamation de capacité, L120 « et si c'est la même place qui tire Pyth » : les éditeurs de Pyth par flux sont [abs] (L86). Écrire « et si un écart de Pyth coïncide avec celui d'une place nommée (co-occurrence, sans attribution) ».

**C7 — Chiffre et traduction (§2.4).**
- (a) L159 « 3 sur 12, soit 25 % » : pour BTC, le spot Hyperliquid est exclu (“do not include Hyperliquid spot prices in the oracle”). Le poids de Binance est donc de 3 sur 11, soit environ 27 % ; 3 sur 12 (25 %) ne vaut que si le spot Hyperliquid est inclus.
- (b) L155 « exigible 183 jours » : écrire « maintenu au moins 183 jours après le déploiement du dex » (“maintained for a minimum of 183 days after the dex is deployed”).

**C8 — Provenance des copies et empreintes (§6, §7).**
- (a) Déclarer trois anomalies :
  - `pages2/jup-dev-llms.raw` est une page 404 du portail Jupiter (15 162 octets), alors que `pages2/jup-dev-llms.txt` est octet pour octet `pages2/jupx-742488.raw` (sha256 `f90a7559…`). Donner l'URL source de `jupx-742488.raw`, qui porte la citation L143. Le §7 affirme aujourd'hui que « les `.raw` sont les octets reçus, les `.txt` leur texte » ;
  - `pages2/kamino-llms.txt` n'a pas de `.raw` ;
  - les `pages/*.derived.txt` ont été produits sans script consigné. Leurs citations figurent bien dans le HTML reçu : je l'ai contrôlé.
- (b) Après correction, régénérer `SHA256SUMS` (le rapport et `quotes.txt` changent) et relancer `sha256sum -c`.

## 4. Observations hors liste (sans effet sur le verdict)

- **O1.** Aucun index copie → URL : 61 copies sur 117 n'ont pas d'URL récupérable dans leurs octets. Les pièces voisines P4 et P5 n'en tiennent pas non plus. Il serait utile si les copies restent hors dépôt (précédent : note de versement de P5).
- **O2.** Le nom d'une personne tiré d'un extrait de moteur (Tracxn, L106) est correctement étiqueté [2nd] et non retenu. Envisager de le retirer d'une pièce versée.
- **O3.** « TVL nul » (L150, L157) traduit une valeur `null` de DefiLlama : « sans valeur de TVL » serait plus exact.
- **O4.** Coquille L199 : « règlant » → « réglant ».
- **O5.** JELLY : CoinDesk relaie Lookonchain et écrit “allegedly manipulated”. « Selon CoinDesk (d'après Lookonchain) » serait plus précis.
- **O6.** « Anthias Labs (gestionnaire de risque du protocole) [lu] » (L171) : aucune copie n'énonce ce rôle. Il est appuyé par le fil 2068, où Anthias abaisse les plafonds du marché cbETH ; [inféré] serait plus exact.
- **O7.** L259 : le profil X montre le titre et environ 40 mots de l'article, pas seulement le titre.
- **O8.** L'audit v2 marque les builds “unverified” ; la v1.2 portait “Verified build matches on-chain”. C'est une information utile à l'investisseur, pas une correction.
- **O9.** Le test du SDK fige l'adresse push SOL/USD `7AviUf9n…`. Ancienne ou nouvelle adresse ? Les copies ne permettent pas de trancher, ce qui est cohérent avec le [abs] du rapport.

## 5. Prête à verser ?

**Pas en l'état ; oui après C1 à C8**, vers `docs/adr-0029/etude-marche/`, comme pièce de contexte commercial non normative, avec une note de versement : copies hors dépôt, référence à `SHA256SUMS`.

Pré-contrôles mécaniques sur la pièce actuelle :
- **S-G5** : aucune « », donc rien à contrôler ; les “ ” sont des zones marquées.
- **S-G4** : j'ai reproduit la liste `LOCUTIONS_INTERDITES` de `xtask/src/sg4.rs` sur la prose hors “ ”, « » et code : 0 occurrence. Les écarts au registre 09 relevés en C6 sont hors de la liste mécanisée.
- **R-13** : aucun marqueur de tâche nu dans la pièce (recherche des trois marqueurs usuels : 0 occurrence).

Contre-contrôle conseillé après correction :
- relancer `g2/work/cites.py`, avec les numéros de ligne mis à jour : attendu 97 sur 97, casse comprise ;
- relancer `sha256sum -c SHA256SUMS` ;
- lancer les vraies gates S-G4 et S-G5 au versement (voir §7, L1).

## 6. Journal de provenance (G1)

### 6.1 Sources lues

Tout ce qui suit est [lu] par moi sur les copies.
- **Briefs et pièce** : `BRIEF-G2-HYLO.md` ; `BRIEF-HYLO-SOLANA.md` ; la pièce, en entier ; `quotes.txt` ; `quotes-v1-premiere-passe.txt` (présence seulement) ; `chk.py` ; `fetch.sh`, `ddg.sh`, `bing.sh` ; `SHA256SUMS`.
- **SDK Hylo** :
  - lus en entier : `sdk-hylo-core-src-pyth-oracle.rs`, `-par_tolerance.rs`, `-pyth-feeds.rs`, `-lib.rs`, `-pyth-mod.rs`, `sdk-Cargo.toml`, `sdk-hylo-core-Cargo.toml` ;
  - lu en partie : `-error.rs` (variantes oracle, parité, `oracle_config`) ;
  - lus au début : `-solana_clock.rs` (l. 1–30) et `sdk-README.md` (licence).
- **Audits** :
  - OtterSec, texte comparé au PDF : pp. 1–5 et 8–11 (numéros imprimés) ;
  - Accretion de décembre 2025 : pp. 1–6, puis balayage oracle des 26 pages ;
  - Accretion de juillet 2026 : pp. 1–5 (tableau complet), détail d'ACC-L1, L7 et L20, puis balayage « oracle/pyth » des 94 pages.
- **Docs Hylo** : introduction, multi-asset, equations, value-at-risk, risk-management, additional-risk-management, collateral-rebalancing, security-audits, onchain-addresses, product-guide-xassets, developer-resources, `hylo-llms.txt`.
- **Pages tierces sur Hylo** : X de Hylo (`.html` et `.derived.txt`), SolanaFloor (`.html`, métadonnées), extrait Tracxn (`ddg-hylo-team.derived.txt`).
- **DefiLlama** : `llama-hylo.json`, `llama-protocols.json`, `llama-stablecoins.json`, avec les calculs du §6.3.
- **Pyth** : `pyth-core`, `-aggregation`, `-upg-how`, `-pro-how` lus en entier ; `-pro-data`, `-upg-solana` et `-upg-contracts` lus en partie.
- **Comparables** :
  - Kamino (oracles, priceprot) ; Jupiter (lend-oracles, jupusd, perps-custody, une ligne de `jup-dev-llms`) ;
  - Velocity (oracles en entier, migrate) ; `drift-llms` (en-tête) ;
  - Hyperliquid (oracle en entier, hip3 en partie) ;
  - Felix (risk, cdp) ; Moonwell (oev, oev-core) ; Suilend (risks, liq) ;
  - Thala, Echelon, Aries (oracles) ;
  - Bucket et NAVI (balayage par motifs).
- **Incidents** :
  - `inc-loopscale`, `inc-marginfi-refund` (`.raw` et `.txt`), `inc-hl-jelly-coindesk`, `inc-hl-popcat`, `inc-drift-chainalysis`, `inc-drift-nexus`, `inc-sui-scallop` ;
  - `inc-switchboard-postmortem` (en entier), `inc-switchboard-shutdown`, `inc-sui-shattered` ;
  - `x-virtue-incident-report` (TL;DR et résumé), `x-fullsail-2026-08-29`, `x-switchboardfdn-profile` ;
  - fils Moonwell 1983, 2017, 2068, 2084 et 2208 (premiers messages).
- **Dépôt** :
  - `docs/09-vocabulaire.md` (en entier, sha256 `001b9606…2f8831`) ;
  - `docs/adr-0029/etude-marche/SYNTHESE-CROISEMENT.md` : l. 115–126, 243–247 et 628, plus une recherche par motifs (sha256 `69f9ddbb…eea9b`) ;
  - `xtask/src/sg4.rs` (l. 1–140), `xtask/src/sg5.rs` (l. 1–100), `xtask/src/main.rs` (l. 1–60) ; `xtask/src/documents.rs` et `justfile` (recherche par motifs) ;
  - P4 et P5 de la même étude, par recherche de motifs seulement, pour comparer les pratiques de sources.
- **Non ouverts** : `docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`. Aucun `*.jsonl`, aucune recherche récursive sur tout `docs/`.

### 6.2 Commandes lancées et sorties

- `sha256sum -c SHA256SUMS` → 201 lignes OK, code 0. `comm` entre fichiers listés et présents → seul écart : `SHA256SUMS` lui-même.
- `g2/work/extract.py` → 98 paires “ ” : 97 citations plus la définition vide de L8. Aucune « » ; un guillemet droit, dans du code.
- `g2/work/cites.py` (sha256 `d377e113…5b`) → `citations 97 a examiner 2` ; EXACT 91, WS 4, LARGE 2 (L76 `\$` ; L142 casse). Sortie dans `g2/work/cites.out` (sha256 `04a2beb3…24f5524`).
- `g2/work/qalign.py` → 95 lignes dans `quotes.txt`, 94 citations distinctes toutes couvertes, 8 lignes sur une autre copie, 1 ligne vide (`g2/work/qalign.out`).
- `chk.py` du lecteur → `problemes: 0` (`g2/work/chk-lecteur.out`).
- Dérivation `.raw` → `.txt` de `fetch.sh` refaite sur `pages2/` → 67 identiques, 1 différente (`jup-dev-llms`). `kamino-llms.txt` n'a pas de `.raw`.
- `pdftotext -layout` sur les trois PDF → identique octet pour octet aux `.txt` copiés, 3 sur 3. `pdfinfo` : 18, 26 et 94 pages ; création le 2025-05-13, le 2025-12-08 et le 2026-07-08.
- Citations des `pages/*.derived.txt` recherchées dans le HTML reçu → présentes (X, docs-hylo, Tracxn ; SolanaFloor une fois les balises `<em><a>` retirées).
- Métadonnées de date dans les `.raw` :
  - MarginFi : 2024-04-19T19:29:12Z ;
  - post-mortem Switchboard : 2026-09-18T20:45:56Z ;
  - Shattered : 2026-09-10 ;
  - Chainalysis : 2026-04-09 ; Nexus : 2026-04-09 ;
  - CoinDesk : 2025-03-26 ; The Crypto Times : 2025-11-13 ; Startup Fortune : 2026-04-26 ;
  - Solana Compass : 2026-09-19 ; Virtue : 2026-08-30 ; Full Sail : 2026-08-29 ;
  - SolanaFloor (Hylo) : 2026-06-17.
- Horodatages des captures → de 18:30:11 à 18:42:59 UTC, dans l'intervalle annoncé de 18:29 à 18:43.
- S-G4 approché (Python) → 0 occurrence. R-13 → 0.
- Citations proposées en §3, contrôlées dans leurs copies → 13 en octets exacts, 1 aux espaces près (“is being shut down”).

### 6.3 Chiffres recomptés

- **Hylo** (`llama-hylo.json`) :
  - dernier point 1791134075 = 2026-10-04 17:14:35 UTC, soit 68 383 779 $ ;
  - 66 722 444 $ (2026-09-27), 49 935 069 $ (2026-09-04), 33 470 033 $ (2026-07-06) ;
  - pic 107 588 628 $ le 2026-01-15 ;
  - `tokensInUsd` : jitoSOL 34 557 724, SOL 24 389 995, cbBTC 3 864 707, hyloSOL 2 951 852, HYPE 2 619 502, USDC 0, soit SOL et LST à 90,52 % ;
  - levée Seed de 1,5 M$ le 2025-08-07.
- **Sous-protocoles** : Hylo Protocol 43 993 785 $ (« Dual-Token Stablecoin », 2 audits) ; Hylo LSTs 24 389 995 $ (0 audit).
- **Stablecoins** : hyUSD 26,04 M$ ; JupUSD 48,963 M$ ; feUSD 9,718 M$ ; BUCK 25,827 M$ ; MOD 0,032 M$, tous crypto-backed.
- **Comparables** :
  - Kamino Lend 1 397,2 M$ (emprunts 1 020,0 M$) ; Kamino Liquidity 75,98 M$ ;
  - Jupiter Lend 1 318,1 M$ (emprunts 988,3 M$) ; Jupiter Perpetual Exchange 820,4 M$ (emprunts 149,1 M$) ;
  - Drift Trade 0,643 M$ ; Velocity sans valeur de TVL ;
  - Hyperliquid Bridge 7 135,0 M$ ; HLP 181,6 M$ ; Spot Orderbook 178,6 M$ ; Perps sans valeur de TVL ;
  - Felix CDP 31,42 M$ ; Felix Vaults 43,41 M$ ;
  - Moonwell Lending 13,656 M$ (Base 11,736, Optimism 1,276, Ethereum 0,6446 ; emprunts 26,83 M$, dont Base 24,86) ; Moonwell Vaults 10,30 M$ ;
  - Suilend 174,07 M$ (emprunts 78,52 M$) ; Thala CDP 0,506 M$ ;
  - Echelon Market 8,138 M$ (Aptos 7,544 M$) ; Aries 0,076 M$ ; NAVI 188,97 M$.
- **Audits** :
  - OtterSec : 7 constats (2 critiques, 0 haut, 1 moyen, 2 faibles, 2 informatifs) ;
  - Accretion de décembre 2025 : 16 constats ;
  - Accretion de juillet 2026 : 51 constats (16 moyens, 25 faibles, 10 informatifs), dont 44 FIXED et 7 ACKNOWLEDGED au tableau.
- **SDK** : 50 000 000 / 10⁹ = 0,05 ; 10 000 / 10⁹ = 10⁻⁵ ; 1 000 000 / 10⁹ = 10⁻³. `lib.rs` déclare 22 modules ; le lecteur en a lu 4 hors `lib.rs`, il en reste 18 non lus.
- **Hyperliquid** : poids 3+2+2+1+1+1+1+1 = 12, et 11 sans le spot Hyperliquid ; 3/11 = 27,3 %.
- **Synthèse §4** : 11 piles à fournisseur externe ; Pyth dans 9, Chainlink dans 6, RedStone dans 2, Switchboard dans 4 (le « déprécié » de Velocity non compté), conforme au rapport.

### 6.4 Écrits

Uniquement dans `marche2/hylo/g2/` :
- `G2-HYLO.md` (ce rapport) ;
- `sha-check.out`, `listed.txt`, `present.txt` ;
- `work/extract.py`, `work/cites.py`, `work/qalign.py` et leurs sorties `.out` ;
- `work/chk-lecteur.out` ;
- `work/*.layout.txt` et `work/*.plain.txt` (sorties de `pdftotext`).

Rien d'écrit ailleurs ; aucune opération git en écriture.

## 7. Limites rencontrées, rendues à l'orchestrateur comme items à former

- **L1.** Les vraies gates S-G4 et S-G5 n'ont pas tourné sur la pièce. Le dépôt est en lecture seule, et `cargo xtask gates` lance toutes les gates sur le workspace. S-G4 est approché en Python ; S-G5 n'a rien à contrôler (aucune « »). Item : passer les vraies gates au versement.
- **L2.** La fidélité des copies aux pages en ligne n'est pas recontrôlée : il n'y a pas d'index des URL et je n'ai pas utilisé le réseau. Seule la cohérence interne est contrôlée : 67 dérivations `.raw` → `.txt` sur 68 identiques, et les 3 extractions PDF → texte identiques.
- **L3.** Je n'ai pas pu déterminer si le SDK Hylo dérive les anciens ou les nouveaux comptes push Pyth (O9, C4 g) : la table de Pyth est rendue en JavaScript et ne figure pas dans la copie.
- **L4.** Je ne fais qu'adjuger : les corrections C1 à C8 doivent être appliquées par un autre que moi, puis faire l'objet du contre-contrôle décrit au §5.
