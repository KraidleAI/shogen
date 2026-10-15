# Relecture G2 neuve de DETTES-T16 (transcrit)

> Transcription par l'orchestrateur le 2026-10-15 13:39:21 UTC du fichier dettes16/g2/RAPPORT-G2.md ; contrôle FM-1.1 des transcripts du générateur et du réviseur G2, par le fm11.py versé et par celui de DT3-E : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# RAPPORT G2 — lot DETTES-T16 (BIBLIO-API), relecture neuve

Gate 0 : modèle résolu `claude-opus-5-5` (réviseur G2 neuf ; effort `max` demandé, non observable de l'intérieur). Je n'ai
ni écrit ni relu ce lot avant ce jour. Heures UTC lues par `date -u` (ouverture : 2026-10-15 10:46:38). Dépôt
`/home/user/shogen` lu seulement (`git --no-optional-locks`), aucune écriture git ; `SHOGEN_S2_CAMPAGNE_CONTROL` jamais
posée (retirée par `env -u`) ; aucun réseau (exécutions sous `isole.sh` : `unshare -n`, connexion d'essai refusée, code
101 ; variables de mandataire retirées par `env -u`) ; aucun emplacement interdit ouvert ni listé ; aucune pièce de D.2 ;
écritures dans `<scratchpad>/s2bis/dettes16/g2/` seulement. Brief : `g2/BRIEF-G2.md` ; décisions : `ADJUDICATION.md`.

## 0. Verdict

**ACCEPTE-AVEC-CORRECTIONS**, liste fermée :

- **C-1** (DT16-a, `biblio/INDEX.md` l.449, rangée `okx-docs-v5-en-api-guide-2026-10-10.html`, colonne « non citable ») :
  « (leur alignement sur UTC+8 est inféré) » devient « (leur découpage en UTC+8, qui ne s'y lit pas, est établi sur
  pièce : `scripts/calib-actifs/README.md`, DECISION de FORMES-API-1, ajout daté du 2026-10-09 19:51:45 UTC) ».
  Motif : `scripts/calib-actifs/README.md` (l.53-54 à la tête de ma copie, l.67 à la tête de fin) dit le découpage UTC+8 « établi sur pièce » ; la rangée,
  vraie sur la page, se lisait comme un état du savoir du projet et le contredisait. `corrections/C-1.diff` (+1 −1),
  s'applique après DT16-a ; INDEX final sha256 `f6a59ae2b6f8d8fbe0ec51494cf00f377db309cbf30840f0b8a0591a108d2df1`.
- **C-2** (outil du lot `outils/verser_biblio.py`) : la section est lue de son titre au titre de niveau 3 suivant, non
  jusqu'à la fin du fichier. Motif : SHOGEN-BIBLIO-COPIE-DURABLE-1, étendu aux 8 pièces, prévoit de rejouer ce script
  plus tard, quand une section postérieure existera ; le script d'origine en lirait les rangées et refuserait (refus
  fermé, mais versement impossible). `corrections/C-2.diff` (+4 −2) ; script corrigé sha256
  `88105cc6d36b61d63ddab2529374c1a3b05967508c7e794b1a83c4090f6ca5f2`. Échec montré avant correction : cas L de ma
  batterie, `REFUS : piece-posterieure.html introuvable …` sur l'origine, 12 cas sur 12 sur le corrigé.

Hors de DT16-a, formes exactes demandées par le brief pour le versement de DETTES-T2 (actes de l'orchestrateur, §3, §4) :
F-1 (retouche déclarée du rapport du chercheur), F-2 (erratum daté, OKX), F-3 (bloc B de `verser_d2.py`), F-4 (phrases
de fermeture du §8 du générateur). Signaux : S-1 (docstring de `acquerir.py`), S-2 (ordre des actes du versement), S-3
(conditions d'usage, point 4).

## 1. Base, copies, méthode

- Tête à l'ouverture : `2b8fb5944d353e8c7867b85a1cb4b85ae95f6953` ; copie faite sur `29d945dd57a9b643b94e34053719dca09d4ff026`
  (lue à 10:48:01, DETTES-T2 DT2-n) : `git archive` avec exclusions par pathspecs (emplacements interdits, `*.jsonl`),
  1392 membres, 0 sous un emplacement interdit, 0 `.jsonl` (comptes seuls). `biblio/INDEX.md` de cette tête : sha256
  `2e54fccdd134f82a09ff0faff273938e5b273eaebe90c9497cd61d3e2e9c2618`, 437 lignes, inchangé depuis la base du générateur.
- DT16-a (`diffs/DT16-a.diff`, sha256 `4c73834def85cb37d72d11b0f23a47c68bdec73cc9e2577e849c6080edc52749`) :
  `git apply --check` puis `git apply` sur ma copie : passe ; état égal à l'octet à celui du générateur (`cmp`).
- `biblio/` de copie : les 252 fichiers de la session (196 artefacts, 55 `*.sidecar`, INDEX) copiés sans écraser
  l'INDEX de la série, puis les 8 pièces versées par `outils/verser_biblio.py` : 260 fichiers, 204 artefacts ;
  `sha256sum -c pieces/SHA256SUMS` dans la cible : 8 OK ; `SHA256SUMS` du lot : 41 OK.
- Copie finale = tête + DT16-a + C-1 + `biblio/` versé. Mes outils (dossier `outils/`, aucune barre oblique inverse
  dans leurs octets) : `g2sg5.py` (normalisation de S-G5 réécrite depuis `sg5.rs` et `documents.rs`, 6 tests à valeurs
  écrites à la main), `verif_index_g2.py`, `citations_rapport_g2.py`, `spans_piece_g2.py`, `section_okx.py`,
  `contexte.py`, `test_verser_g2.py`, `mutants_verser_g2.py`, `mutants_controleurs_g2.py`, `retouche_g2.py`,
  `sim_transcription_g2.py`, `filtre_verdicts.py`, `preuve_g2.sh`, `preuve_finale_g2.sh`. Sorties : `sorties/`.
- Tête à la fin (11:42:00) : `ffd338e4649618a38354d02bf121ad5def11ccb8` (DEPLOI-BIS DB1-b). Depuis la tête de ma
  copie, `biblio/INDEX.md`, `xtask/`, `enforcement/`, `.cargo/`, Cargo, `WISHLIST.md`, `.gitignore`, `s2-harness/` et les quatre
  fichiers de code lus de `scripts/calib-actifs/` sont inchangés (`git diff --quiet` sur ces chemins nommés) ; seul le README
  de ce dossier a changé (DT2-t ; le passage que cite C-1 y est à la l.67) ; `git apply --check` puis `git apply`
  de DT16-a puis de C-1 sur l'INDEX de cette tête (`git show`) : passent ; état égal à ma copie finale (`cmp`).

## 2. Point 1 — rangées de l'INDEX (DT16-a)

- **Lignes et compte** (`verif_index_g2.py`, `sorties/verif_index_g2.txt` et `.finale.txt`, sortie 0) : des 437 lignes
  de la tête, seule la l.3 change ; elle vaut le nouveau préfixe suivi de l'ancienne ligne à partir de « (+35 le »
  (historique gardé, forme de DT14-a) ; 15 lignes ajoutées (l.438 à 452) ; compte lu dans les 500 premiers octets
  (lecture de `compte_declare_en_tete`) : 196 à la tête, 204 dans la série = 196 + 8 rangées = 8 pièces ; S-G6 sur la
  copie versée : `compte déclaré 204, compte réel 204`.
- **Renvois** : `refs_index.py` du G2 de DETTES-T14 (sha256
  `4a46493bf7da4c334af90615181c9d54172be3ee525ef0b6ab7291b292562fdd`), liste `noms-g2-presents.txt` (117 noms, 0
  interdit) : 37 renvois vers l'INDEX, seule la l.3 diffère (`docs/G2-lot-CORR.md:355`, ligne du compte, réécrite à
  chaque versement) ; `refs_decalees.py` (sha256 `c15a0ace28a0846ebf91c8f3a8e6cc0f7facd811921f4c0efa05cadd02327a56`) :
  223 renvois, 0 décalé ; mes copies tête et série ne diffèrent que sous `biblio/` (`diff -rq`, sortie 0).
- **Rangées** : 8 rangées de 7 cellules, en bijection avec les 8 pièces ; taille et sha256 de la cellule 3 égaux aux
  octets (8 sur 8). URL et heures : journal de téléchargement du générateur (heure de fin = date de la rangée, 8 sur 8),
  recoupé par les en-têtes HTTP gardés (`date:` du serveur, `content-type: text/markdown; charset=utf-8` pour Coinbase,
  `last-modified: Thu, 08 Oct 2026 10:19:17 GMT` pour OKX, 302 vers `https://www.okx.com/en-us/help/okx-api-agreement`).
  Identité et version lues sur les octets : `GET /products/{product_id}/candles` et `version: '1.0'` ; balise de titre
  et `dateModified` 2026-10-03T00:38:58.916Z (types de Coinbase) ; « Bitstamp Public API », `v2`, ancre
  `#tag/Market-info/operation/GetOHLCData` ; `dateModified` 2026-02-23T10:03:42.000Z et
  `https://api-pub.bitfinex.com/v2/candles/{candle}/{section}` ; titres d'OKX, dates de publication et de mise à jour
  des deux pages de conditions. Conditions : Coinbase, Bitfinex et OKX (documentation) sans mention de droits
  (recherche de `©`, `opyright`, `ights reserved` : 0) ; pied de Bitstamp `All rights reserved © 2026 Bitstamp by
  Robinhood.` ; refus gardés : 403 et page `Just a moment...` (Cloudflare) pour Coinbase, 212 o (Incapsula) pour
  Bitstamp, titre seul et 0 occurrence de `agree` pour les conditions d'API de Bitfinex. Colonne
  « redistribuable » : non, partout, conforme à la règle en tête du registre.
- **Non citable** : vrai sur chaque pièce (Coinbase lu en entier : ni inclusion, ni format des bornes d'une requête, ni
  ordre ; Bitstamp, section OHLC rendue, octets 724223 à 737167 : `seconds` à `step` seul, aucun mot d'inclusion ni
  d'ordre ; Bitfinex : schéma de `sort` sans défaut ; OKX : voir §4). Seule la parenthèse de la rangée OKX reçoit C-1.
- **Citations** : 48 spans, tous EXACT dans la pièce de leur rangée (normalisation de S-G5), 19 mots au plus ; aucun span
  dans la provenance. Encadrés : 248 dans la page OKX, 2 dans la copie Firecrawl du chercheur (60 premiers caractères
  normalisés), les deux encadrés cités absents de la copie, présents dans la page. La copie `okx.md` du chercheur est
  celle de la documentation v5 : aucune copie de la page des données historiques (0 occurrence). Bloc B.85 de
  l'annexe B (l.1352) : il porte bien SHOGEN-CALIB-FORMES-API-1.

## 3. Point 2 — citations du rapport du chercheur

`citations_rapport_g2.py` (garde : sha256 du rapport
`0dff14fd0f1b473ae0e3f22c91c4e456f336f67f53a691e8dda47fdef0d1abd4`, sinon sortie 3), `sorties/citations_rapport_g2.txt` :
52 spans ; 7 hors page (`seconds` l.42 deux fois et l.106 ; expressions françaises l.98 deux fois, l.100, l.112) ;
45 citations de pages, cherchées dans la pièce visée par leur section du rapport : 42 EXACT (élision de la l.73
comprise : `dataDate ... (UTC+8)` dans la section `trading-account-rest-api-get-get-glp-today-performance` ; Bitstamp,
toutes dans la section OHLC ; OKX, l.66, 67 et 72 dans « Get historical market data », l.77 et 81 à 86 dans « GET /
Candlesticks history ») ; l.56 EXACT une fois l'échappement Markdown `\|` du tableau rendu (aucune retouche) ;
**l.40 confirmée** : forme compacte seulement ; le rapport écrit `integer[ 1 .. 1000 ]`, la page (octet 728740)
`<span …>integer</span><span> <span …> <!-- -->[ 1 .. 1000 ]`, soit « integer [ 1 .. 1000 ] » après débalisage ; la
copie Firecrawl porte `integer\[ 1 .. 1000 \]` : graphie de l'extraction, non changement de page ; **l.64 confirmée** :
introuvable ; la page porte `<h3 …>Candlestick</h3><p …>OHLC chart history from July 2023 onwards.</p>`, sans
deux-points : coquille du chercheur (jonction du titre et de la description), description mot pour mot.
Constat de plus, hors « » : la l.38 porte, en code, `integer[ 0 .. 253402297199 ]`, même graphie (page : deux
occurrences de `integer [ 0 .. 253402297199 ]` après débalisage) ; je la range dans la retouche (F-1).
S-G5 ne contrôle aucun de ces trois fragments (moins de deux mots-fonction, ou crochet court traité en insertion).

## 4. Point 3 — encadrés d'OKX, code de `scripts/calib-actifs/`

**Où la page détenue dit UTC+8 et « inclusive »** (`section_okx.py`, sections tranchées d'un `<h3 id='…'>` au titre
suivant de niveau 1 à 3) :

- Section `public-data-rest-api-get-historical-market-data` (« Get historical market data », octets 3883189 à
  3897782, 5 encadrés), point d'accès `GET /api/v5/public/market-data-history` (liste des fichiers à télécharger) :
  table des paramètres, `begin` et `end` « Unix timestamp format in milliseconds (inclusive) », `dateRangeStart` et
  `dateRangeEnd` « (inclusive) », module 2 « 1-minute candlestick » ; encadré 4 « Data query rules » : « Only the date
  portion (yyyy-mm-dd) of timestamps is used; time components are ignored », « Both begin and end timestamps are
  inclusive », « Data is returned in reverse chronological order (closer to end first) » ; encadré 5 « Timezone
  specifications for timestamp parsing » : « When converting Unix timestamps to dates, the following timezone
  conventions are applied to all timestamp fields (begin, end, dateRangeStart, dateRangeEnd, dataTs) », carnets
  (modules 4, 5, 6) UTC+0, « All other data modules (modules 1, 2, 3, 11): UTC+8 ».
- Section `order-book-trading-market-data-get-candlesticks-history` (« GET / Candlesticks history », octets 2790193 à
  2799726, 3 encadrés : forme du tableau, bougie d'une seconde, `adjust=forward`) : `after` « Pagination of data to
  return records earlier than the requested ts », `before` « … newer than the requested ts … » ; **ni « inclusive »,
  ni ordre, ni fuseau pour `after` et `before`** ; UTC+8 n'y vise que les barres longues de `bar` (« UTC+8 opening price
  k-line »).
- Donc : « inclusive » vise `begin` et `end` de la liste des fichiers, **au jour près** ; UTC+8 vise la conversion des
  horodatages en dates des modules 1, 2, 3 et 11 ; ni l'un ni l'autre ne vise `after`/`before` des bougies.

**Le code à la tête** (`29d945dd57a9b643b94e34053719dca09d4ff026`, ma copie) : `parametres.json` l.61-63, OKX
`"acces": "mensuel"`, `"voisins": 1`, URL statique `https://static.okx.com/cdn/okex/traderecords/candlesticks/monthly/…`
(seule mention d'`okx.com` du code ; 0 occurrence de `api/v5`, `market-data-history`, `history-candles` dans les `.py`,
`lancer.sh`, `README.md`) ; `acquerir.py` l.80-83 `mois()` et `socle.py` l.208-212 `rangs_mois` : mois UTC de la
fenêtre et un voisin de chaque côté ; `bougies.py` l.49-56 lit `open_time` en millisecondes depuis l'époque (aucun
fuseau) ; l.224-226 : minutes gardées dans la fenêtre, refus hors des mois acquis à ± 50400 s (14 h). Le code ne suppose
donc aucun fuseau : il est juste sous UTC et sous UTC+8 (fenêtre principale 2026-04-01 à 2026-07-01 UTC : en UTC+8,
le mensuel 2026-04 commence le 2026-03-31 16:00 UTC et les 8 dernières heures sont dans 2026-07, acquis comme voisin ;
garde respectée des deux côtés). Il n'appelle ni la liste des fichiers ni `history-candles` : les bornes « inclusive »
de la page ne le concernent pas ; pour les places paginées, `socle.pages` est construit « bornes incluses ou non »
(docstring l.227-228). Lecture exacte de l'adjudication : « le code lit déjà les mensuels en UTC+8 » se dit mieux
« le code lit les mensuels sous les deux découpages ; le README de la tête (l.53-54 ; l.67 à la tête de fin) dit le découpage
UTC+8 établi sur pièce » ; « les bornes inclusives sont celles que le code suppose » ne tient pas à la lettre : le code n'emploie pas ces
bornes et ne suppose aucune inclusion pour OKX.

**Phrases qui deviennent fausses** : dans le rapport du chercheur, l.71 (« NON DIT pour les fichiers mensuels de
bougies. Aucune phrase sur le fuseau des fichiers. », niveau [abs]), l.73 (« le découpage des FICHIERS mensuels n'est
pas dit »), l.100 (« jamais énoncé pour les mensuels ») et le premier point de la l.108 : erratum F-2. Dans le bloc B de
`verser_d2.py` (sha256 `d2812680b1be96d905a620e0443c684b48bd8802092fdea1453f8f96c56b8586`) : « les lectures des bornes
que les documentations laissent ouvertes [abs] (Coinbase, Bitstamp ; mensuels d'OKX) » : la documentation d'OKX ne
laisse plus ouvert le fuseau des mensuels : F-3. Le reste du bloc tient (code juste sous les deux découpages ; UTC+8
établi sur pièce). Les [abs] des l.81, 82 et 85 (inclusion de `after` et `before`, ordre de
`history-candles`) tiennent, comme la l.101 et les deux derniers points de la l.108.

## 5. Point 4 — conditions d'usage (signal pour l'investisseur, pas une décision)

Citations mot pour mot, contrôlées EXACT sur les pièces (`spans_piece_g2.py --code`, 25 mots au plus) :

- Accord d'API d'OKX, **version américaine détenue** (la version mondiale ne l'est pas) :
  §1.8 (définition) `or other market information made available through the API Services or through OKX's publicly accessible endpoints, whether accessed with or without authentication` ;
  §9.4 `Market Data — Non-Commercial Use and Redistribution Restrictions` ;
  `You may access and use Market Data solely for your own personal, non-commercial trading and account management purposes.` ;
  (a) `resell, redistribute, publish, display, or otherwise make Market Data available to any third party, whether for commercial gain or otherwise` ;
  (b) `use Market Data to build, operate, or contribute to any competing data product, market data service, financial data aggregator, price feed, or analytics platform` ;
  `The restrictions in this Section 9.4 apply equally to Market Data accessed through public endpoints as to Market Data accessed through authenticated endpoints.` ;
  `You must not use automated scripts, bots, web scrapers, or any other automated means to extract Market Data from OKX's public endpoints or website`
  `at a rate or scale that: (a) exceeds what is reasonably necessary for your personal trading use` ;
  `Any person accessing OKX Market Data through public endpoints without authentication is subject to the same Market Data restrictions`.
- Conditions américaines d'OKX : §8 `We grant you a limited, non-exclusive, non-transferable permit, subject to these Terms, to access and use the Services, solely for purposes approved by us.` ;
  §9.4 `You shall not utilize the Services to engage in or in connection with any commercial activities without our express written consent.`
  (ce §9.4 des conditions n'est pas dans la rangée d'INDEX, qui dit « reste non lu » : exact, rien à corriger).
- Bitstamp (page de l'API, section « Commercial Use of Bitstamp's Exchange Data ») :
  `Companies seeking to utilize Bitstamp's exchange data for their own commercial purposes are directed to contact` …
  `to receive and sign a commercial use Data License Agreement.` ; `Bitstamp allows the incorporation and redistribution of our exchange data for commercial purposes.` ;
  limites : `As standard, all clients can make 400 requests per second.` ; `There is a default limit threshold of 10,000 requests per 10` (minutes).

**Ce que fait CALIB-ACTIFS** (code à la tête) : pour OKX, téléchargement par script des mensuels de bougies d'une
minute à leur URL statique (mois des deux fenêtres et un voisin de chaque côté, paires ETH-USDT et USDT-USD), sans
compte ni clé, sans appel d'API ; pour Bitstamp, requêtes paginées au point d'accès public `/api/v2/ohlc/{s}/`
(`intervalle_ms` 200, soit 5 requêtes par seconde au plus) ; aucun octet d'historique n'entre au dépôt
(`acquerir.py` l.4) ; sortent des valeurs de calibration et des comptes de minutes.

**Où la clause s'applique** (lecture du réviseur, à soumettre) : OKX §9.4 vise par ses termes les données lues sans
compte aux points d'accès publics ; si les mensuels statiques en sont (fichiers listés par la page publique des données
historiques, dont le pied renvoie aux conditions), l'usage permis est « personal, non-commercial trading and account
management », que la calibration d'un projet n'est pas, qu'elle soit commerciale ou non ; (a) n'est pas touché pour les
octets bruts (jamais versés) ; la publication de valeurs dérivées et (b) « price feed, or analytics platform » dépendent
de ce qu'est Shōgen : question pour l'avocat (Q-A). Conditions américaines §8 et §9.4 : même question, version
américaine seule détenue. Bitstamp : l'usage commercial des données passe par un contrat de licence ; l'usage non
commercial n'y est pas traité ; débit du lot bien sous les limites écrites ; conditions générales non lues (défi
Incapsula). Coinbase, Bitfinex : conditions non lues (SHOGEN-BIBLIO-CONDITIONS-CAPTURE-1). Aucun acte avant la réponse
de l'investisseur (adjudication).

## 6. Point 5 — versement privé (`outils/verser_biblio.py`, sha256 `279db9006458a450ebc56fea12411600f2bd8de8cba0da0d7717626763b6374c`)

- Sur ma copie : 8 copiés, puis 8 déjà présents à l'identique (sortie 0 deux fois) ; 260 fichiers, 204 artefacts.
- Batterie `test_verser_g2.py` (contrat 0 / 1 / 3), un dossier neuf par cas : A nominal ; B idempotent (octets et dates
  inchangés au second passage) ; C source altérée d'un octet (3e rangée) : refus nommé, rien copié ; D cible présente
  avec d'autres octets : refus, fichier intact ; E INDEX sans la section : refus ; F copie faussée (copie2 ajoute un
  octet) : refus après copie ; G nom `../evasion.md` : refus avant toute copie, rien écrit hors de la cible ; H cible
  absente : refus ; I pièce manquante : refus, rien copié ; J deux sources ; K sha256 d'INDEX altéré : refus ; L
  section postérieure à celle de DT16 : ignorée (C-2). Origine : 11 cas sur 11 sans L, 11 sur 12 avec L (échec montré :
  L) ; corrigé C-2 : 12 sur 12.
- Mutants (`mutants_verser_g2.py`, une mutation par mutant, base verte exigée ; classement SHOGEN-MUT-FATAL-1) :
  origine, batterie sans L : M1 à M10 **10 tués sur 10**, 0 vivant, 0 FATAL ; corrigé, batterie complète : M1 à M9,
  M10b, M11 **11 tués sur 11**, 0 vivant, 0 FATAL (M10 sans objet : motif absent). Mutants : contrôle du sha256 de la
  source ôté ; contrôle de la cible divergente ôté ; idempotence rompue ; validation du nom ôtée ; recontrôle après copie
  ôté ; refus rendu en sortie 0 ; titre de section trop large ; copie avant le plan complet ; contrôle de la cible absente
  ôté ; rangées lues dans tout l'INDEX ; borne de section ignorée.
- Mes contrôleurs éprouvés par entrées mutées (`mutants_controleurs_g2.py`) : citation d'INDEX altérée, citation de 26
  mots, taille fausse, ligne insérée avant la l.200, compte faux, pièce Bitfinex altérée : sortie 1 ; rapport changé :
  sortie 3 ; 7 tués sur 7.

## 7. Point 6 — gates (copies sous `isole.sh`, `env -u` des neuf variables du brief)

- `cargo --locked --offline xtask verify` (sortie brute jamais lue ; `filtre_verdicts.py` : VERDICT, `chemin:ligne`,
  comptes) sur la copie série, puis sur la copie finale (avec C-1), mêmes verdicts : S-G1 à S-G4 VERT ; **S-G5 VERT**,
  `347 fragment(s) de citation contrôlé(s)`, corpus `INDEX + 204 artefact(s) local(aux) sur 204 déclaré(s)` ; **S-G6
  VERT**, `compte déclaré 204, compte réel 204` ; S-G7a, S-G8 VERT ; S-G9 ROUGE, 1 violation,
  `docs/17-modele-de-menace.md:70` (copie creuse, attendue) ; `cargo fmt --check`, `no_std`, `cargo clippy -D warnings`
  VERT ; sortie 1 par S-G9 seul.
- `python3 -B enforcement/docs-sha256sums.py .` (copie série et finale) : `docs-sha256sums : conforme : 42 SHA256SUMS,
  324 ligne(s), dont 11 absente(s) admise(s) (SHOGEN-SIM-SOMMES-1) ; 4 fichier(s) non listé(s), non refusés`, sortie 0.
- `presg5.py` (sha256 `60de40770b2889b7dc449b863b42755df757789c7063ba445cbd982c81a87ef0`) sur `RAPPORT.md`, racine =
  copie série : `presg5 : 0 fragment(s) introuvable(s)`, sortie 0 (10:56:47 à 11:13:31).
- `presg5.py` sur la copie finale, quatre fichiers (rapport d'origine, rapport retouché F-1, erratum F-2,
  transcription simulée) : `presg5 : 0 fragment(s) introuvable(s)`, sortie 0 (11:24:06 à 11:40:42).
- Suite `s2-harness` sur la copie finale (`python3 -B -m unittest discover -s tests -t .`, sous `isole.sh`) :
  `Ran 419 tests in 51.451s`, `OK (skipped=2)`, sortie 0.
- Simulation du versement réel (`xtask gates`) : la transcription composée selon F-1 et F-2
  (`sim_transcription_g2.py`) posée à `docs/adr-0028/revue-dettes2/RAPPORT-CHERCHEUR-transcrit.md` ; sur la tête seule
  avec les 196 artefacts de la session : **S-G5 ROUGE, 19 violations** (les 17 lignes du rapport, décalées de 4 par
  l'en-tête, et 2 sur la ligne de l'erratum) ; sur la copie finale : **S-G5 VERT**, 366 fragments contrôlés, 204 sur
  204 ; S-G4 VERT ; S-G9 inchangé.

## 8. Formes exactes pour le versement de DETTES-T2 (demandées par le brief ; actes de l'orchestrateur)

**F-1, retouche déclarée** (rapport du chercheur ; éprouvée par `retouche_g2.py` : chaque motif une fois, sur sa ligne ;
seules les l.38, 40 et 64 changent ; texte retouché sha256
`a9d1738055494fd0fd457dec2d576ff3339cdb6f78c12e90ae4e5065d1001139`, 53 spans, 46 citations de pages, toutes EXACT, la
l.56 dans sa forme rendue) :

- l.38 : le span de code `integer[ 0 .. 253402297199 ]` devient `integer [ 0 .. 253402297199 ]` ;
- l.40 : « integer[ 1 .. 1000 ] ... Limit OHLC results. » devient « integer [ 1 .. 1000 ] ... Limit OHLC results. » ;
- l.64 : « Candlestick: OHLC chart history from July 2023 onwards. » devient « Candlestick » : « OHLC chart history from
  July 2023 onwards. » ;
- en-tête de `RAPPORT-CHERCHEUR-transcrit.md` (la phrase fixe d'`entete()`, « Texte ci-dessous sans retouche … », ne
  vaut plus pour cette pièce), forme de `revue-dettes14/PROCUREMENT-AVIS-transcrit.md` l.3 (citation de Fisher) :
  « Texte ci-dessous avec trois retouches, déclarées : l. 38 et l. 40 de l'original, une espace rétablie entre `integer`
  et le crochet ouvrant des domaines de `start` et de `limit` de Bitstamp, forme de la page détenue
  `bitstamp-api-v2-docs-2026-10-10.html` (la graphie collée venait de la copie Firecrawl) ; l. 64 de l'original, le
  guillemet fermant de la citation de la carte d'OKX est placé après « Candlestick » et le deux-points mis hors des
  guillemets, forme de `biblio/INDEX.md` : la page détenue `okx-en-us-historical-data-2026-10-10.html` porte le titre de
  la carte et sa description sans deux-points ; un erratum daté suit le texte (fuseau des mensuels d'OKX) ; le chemin du
  scratchpad est abrégé en `<scratchpad>`. »

**F-2, erratum daté** (à la suite du texte transcrit ; `{H}` = heure `date -u` du versement, `{N16}` = numéro du bloc
de DETTES-T16 ; 8 citations, toutes EXACT dans la page OKX ; S-G5 VERT avec les pièces, ROUGE sans ; copie dans
`sorties/F-2-erratum.md`) :

> **Erratum daté du {H} UTC (heure produite par `date -u`) : fuseau des mensuels d'OKX (§4a)**, porté par l'orchestrateur au versement (lot DETTES-T16, B.{N16}, relecture G2). Les l. 71, 73 et 100 de l'original et le premier point de sa l. 108 disent qu'aucune phrase de la documentation d'OKX ne donne le fuseau des fichiers mensuels, niveau [abs] : ce [abs] vient d'une copie de la page (extraction Firecrawl du 2026-10-09) qui ne porte que 2 des 248 encadrés de la page ; un [abs] établi sur une telle copie n'est pas une absence. La page détenue (`okx-docs-v5-en-api-guide-2026-10-10.html`), section « Get historical market data », porte l'encadré « Timezone specifications for timestamp parsing » : « When converting Unix timestamps to dates, the following timezone conventions are applied to all timestamp fields (begin, end, dateRangeStart, dateRangeEnd, dataTs) » ; « All other data modules (modules 1, 2, 3, 11): UTC+8 » (module 2 : « 1-minute candlestick ») ; et l'encadré « Data query rules » : « Only the date portion (yyyy-mm-dd) of timestamps is used; time components are ignored » ; « Both begin and end timestamps are inclusive ». Le fuseau des dates des fichiers de bougies est donc écrit : UTC+8 [lu] ; les minutes que contient un mensuel ne sont pas dites par la page, elles sont établies sur pièce par la DECISION (ajout daté du 2026-10-09 19:51:45 UTC). Les bornes inclusives visent `begin` et `end` de `GET /api/v5/public/market-data-history`, au jour près ; elles ne disent rien de `after` ni de `before` de `GET /api/v5/market/history-candles`, dont l'inclusion et l'ordre restent [abs]. Le code de `scripts/calib-actifs/` n'appelle aucun de ces deux points d'accès : il lit les mensuels à leur URL statique, mois voisins compris.

**F-3, bloc B de `verser_d2.py`** (deux remplacements dans la puce SHOGEN-CALIB-FORMES-API-1 ; ancres présentes une
fois ; script compilable ensuite) :
- « laissent ouvertes [abs] (Coinbase, Bitstamp ; mensuels d'OKX), sans essai sur données réelles » devient « laissent
  ouvertes [abs] (Coinbase, Bitstamp), et sous les deux découpages des mensuels d'OKX, sans essai sur données réelles » ;
- « première minute 2026-08-31 16:00 UTC) ; » devient « première minute 2026-08-31 16:00 UTC ; la page de documentation
  d'OKX détenue écrit ce fuseau pour la conversion des dates des modules 1, 2, 3 et 11, dans un encadré absent de la
  copie du chercheur, B.{b16[0]}) ; ».

**F-4, phrases de fermeture du §8 du générateur** : SHOGEN-BIBLIO-API-BOURSES-1 nomme la seule l.64 ; il faut « deux
citations qui ne sont pas mot pour mot (l.64 : deux-points ajouté ; l.40 : une espace, et la même graphie en code à la
l.38), retouchées au versement du rapport ». SHOGEN-CALIB-FORMES-API-1 : « l'alignement du contenu des fichiers
mensuels restant inféré » est faux à la date du versement : il est établi sur pièce (DECISION, ajout daté du
2026-10-09 19:51:45 UTC) ; écrire « le découpage des fichiers mensuels, que la page ne dit pas, établi sur pièce par la
DECISION ».

## 9. Signaux et items rendus à l'orchestrateur (règle PAROXYSME)

- **S-1 (hors lot, code de DETTES-T2)** : `scripts/calib-actifs/acquerir.py` l.81-82 (docstring de `mois`, inchangée jusqu'à la tête de
  fin `ffd338e4649618a38354d02bf121ad5def11ccb8`) dit « alignement des mensuels en UTC ou UTC+8 non écrit » ; la page
  détenue écrit le fuseau des dates (UTC+8, modules 1, 2, 3, 11) et le découpage est établi sur pièce. Forme proposée :
  « (OKX : mensuels découpés en UTC+8, établi sur pièce, fuseau des dates écrit par la documentation détenue ; voisins
  gardés, DECISION de FORMES-API-1 pt 4) ». Le fichier est sous `SHA256SUMS` de `scripts/calib-actifs/` et la chaîne
  DETTES-T2 vient d'y commettre : je ne livre pas de diff sur une base mouvante ; à porter par l'orchestrateur avec le
  versement de DETTES-T2 ou au prochain lot qui touche ce fichier.
- **S-2 (ordre des actes du versement)** : le script lit la section dans l'INDEX qu'on lui passe : appliquer DT16-a et
  C-1 à l'arbre de travail avant de le lancer (sinon `REFUS : section absente …`, rien copié : sûr) ; puis xtask, puis
  le commit, d'un seul tenant : entre les deux états, S-G6 rougit (8 artefacts sans mention, 204 contre 196), et le
  crochet local de pré-commit ne lance pas xtask (R-13, épinglage, secrets seulement). Commande, avec C-2 :
  `python3 -I <lot>/outils/verser_biblio.py biblio/INDEX.md biblio <lot>/pieces`.
- **S-3 (point 4)** : la question de valeur des conditions d'usage (§5) est un signal pour l'investisseur et l'avocat.
- **Enregistrement du rôle G2** (consigne B.16, DT3-C) : sans objet ; DETTES-T16 n'est pas un lot du chemin S2 (dossier
  soumis au cp-2) : registre `biblio/` et pièces de CALIB-FORMES-API-1 (S2-bis).
- Aucun item neuf à former par moi : C-1 et C-2 sont des corrections ; F-1 à F-4 et S-1 relèvent des actes déjà
  adjugés (versement de DETTES-T2).

## 10. Écarts

- **E-1 (SHOGEN-HARNAIS-ECHAPPEMENTS-1)** : des commandes d'édition ont porté des séquences tapées (saut de ligne et
  guillemet échappés dans des `python3 -c`, séquence octale d'un `printf`) ; les octets écrits sont contrôlés : 0 barre oblique
  inverse dans mes outils et dans `C-1.diff` et `C-2.diff`, sauts de ligne des en-têtes de diff vus par `od -c` ; le
  premier en-tête de C-2 avait perdu son saut de ligne (substitution de commande) : réécrit par Python, recontrôlé. Le
  présent rapport porte 3 barres voulues (citations de l'échappement Markdown et de la copie Firecrawl), comptées.
- **E-2 (harnais)** : défauts de mes outils trouvés et corrigés avant tout verdict : attente fausse d'un test de
  `g2sg5.py` (le Rust rogne la fin de ligne avant de chercher le saut de page) ; mise en place du cas G ; cas B dépendant
  de A, d'où 2 runs FATAL (M7, M10) au premier passage de la campagne, non comptés, campagne refaite ; recherche
  ordonnée limitée à la première occurrence (l.73 vue COMPACT au premier passage), corrigée dans mes deux contrôleurs.
- **E-3 (un processus lourd)** : mon `xtask gates` de simulation (lancé à 11:18:35, charge 1,27 au départ de la preuve)
  a chevauché un `xtask` de la chaîne DETTES-T2 pendant environ une minute et demie ; `presg5.py` (16 minutes) a tourné
  pendant d'autres runs de la chaîne. Rien d'autre de lourd lancé pendant ces chevauchements.
- **E-4 (listes)** : listes non récursives de dossiers nommés (mon dossier, ceux du lot, `formes-api/`, outils de
  `p1b/g2/travail/` et du G2 de DETTES-T14 par leurs noms, `tmp/dl/`, et dans ma copie `scripts/calib-actifs/`,
  `xtask/src/`, `enforcement/`) ; `.git/hooks/` en lecture ; **une liste par motif sous `docs/`** : `ls` puis boucle
  `*.md` sur `docs/adr-0028/revue-dettes14/` de ma copie, pour trouver la forme de la retouche de Fisher ; contraire à la
  lettre du brief, aucun emplacement interdit en cause.
- **E-5** : `python3 -m py_compile` a écrit des `__pycache__` dans mes dossiers ; effacés.

## 11. Journal de provenance (G1)

Niveaux : [lu] lu sur la pièce ou le fichier ; [2nd] source secondaire ; [abs] cherché sur les octets détenus, absent.

- [lu] en entier : `g2/BRIEF-G2.md`, `ADJUDICATION.md`, `BRIEF-DETTES-T16.md`, `RAPPORT-GENERATEUR.md`, `NOTES.md` du lot,
  `diffs/DT16-a.diff`, `formes-api/RAPPORT.md`, `<scratchpad>/verser_d2.py`, la pièce Markdown de Coinbase,
  `<scratchpad>/outils/presg5.py`, `isole.sh` et `lo_up.py`, les outils du générateur (`verser_biblio.py`,
  `generer_diffs.py`, `filtrer_gates.py`, `preuve_gates.sh`, `mutants.sh`, `telecharger.sh`), `xtask/src/sg5.rs`, et
  dans ma copie `scripts/calib-actifs/acquerir.py`, `socle.py`, `bougies.py`, `parametres.json`.
- [lu] par passages : `formes-api/DECISION.md` (l.5, 11, 49-53) ; `documents.rs` (trois fonctions), `sg6.rs`
  (l.1-40, 70-143), `sg9.rs` (l.1-45), `rapport.rs` (l.60-110), `lib.rs` (l.60-110, 160-200), `main.rs` (usage),
  `.cargo/config.toml` ; `scripts/calib-actifs/README.md` (l.45-62, et l.67 à la tête `b075e5731808c760f618952725aadf70314179c3`) ;
  `docs/adr-0028/ANNEXE-B-items.md` (recherches « retouch » et « Fisher », l.1352, le bloc B.96) ; `docs/adr-0028/CP2-S2.md`
  (l.1-60) ; `docs/adr-0028/revue-dettes14/` (l.1-6 de quatre transcriptions et leurs lignes « retouch ») ;
  `biblio/INDEX.md` (l.1-20, section neuve entière, fichier entier par script) ; outils du G2 de DETTES-T14
  (`refs_index.py` l.1-30, `refs_decalees.py` l.1-40) ; `.git/hooks/pre-commit` (recherche) ; les 7 autres pièces aux
  passages des §2, §4, §5 ; journal TSV du générateur (13 lignes) et en-têtes HTTP gardés (8 pièces, 3 refus).
- [2nd] copies Firecrawl du chercheur `formes-api/okx.md` (sha256
  `6ab70e78a4c7c2fdcf1e3ad77f01ec65c78717fba3c25d5c554b48eb56c999ef`) et `bitstamp.md` (sha256
  `53d1d385eca6d56fe978aa650487a9afd4c00dbf3535acdfb882c92f12e92f35`) : comparaison seulement.
- [abs] : mention de droits sur les pages de types de Coinbase, de Bitfinex et de documentation d'OKX ; « inclusive »,
  ordre et fuseau pour `after`/`before` dans la section des bougies historiques d'OKX ; défaut de `sort` au schéma de
  Bitfinex ; `api/v5`, `market-data-history`, `history-candles` dans le code de CALIB-ACTIFS.

Commandes et sorties : `sorties/` (contrôleurs, batterie, campagnes, filtres de gates), `tmp/preuve/` et
`tmp/preuve-finale/` (sorties brutes, celles de xtask lues par `filtre_verdicts.py` seul), `NOTES.md`.
Chiffres recomptés par moi, sur les octets : 52 spans, 45 citations de pages (42 EXACT, l.56 rendue, l.40 compacte,
l.64 absente) ; 48 spans de la section d'INDEX ; 437 lignes de tête, 452 en série, 15 ajoutées, l.3 seule réécrite ;
196 puis 204 ; 252 puis 260 fichiers ; 248 encadrés, 2 dans la copie Firecrawl ; 37 renvois vers l'INDEX, 223 vers les
autres documents ; 1392 membres d'archive ; 11 et 12 cas ; 10 et 11 mutants tués ; 7 entrées mutées tuées.

## 12. Fichiers rendus (dossier `<scratchpad>/s2bis/dettes16/g2/`)

- `RAPPORT-G2.md` (ce rapport), `NOTES.md`, `SHA256SUMS` (tous les fichiers rendus ; `tmp/` et les copies exclus).
- `corrections/C-1.diff` sha256 `120b0f0f6edd1e25b4b9417905e8a52adb4dd4eb99dd489e010f968800362a2c` ;
  `corrections/C-2.diff` sha256 `2be6efb59638bc9f138560ca87b89c2661cbd54eafe12fe48f82e3cf85a33b2b` ;
  `corrections/verser_biblio.C-2.py` (script corrigé) sha256 `88105cc6d36b61d63ddab2529374c1a3b05967508c7e794b1a83c4090f6ca5f2`.
- `sorties/F-2-erratum.md` sha256 `3e5abb48c654d98eddfbc0998c745058d82f2b7019b46b8b27b8d33c2eabe174` ;
  `sorties/RAPPORT-retouche-essai.md` (F-1 appliquée, essai) sha256 `a9d1738055494fd0fd457dec2d576ff3339cdb6f78c12e90ae4e5065d1001139` ;
  `sorties/RAPPORT-CHERCHEUR-transcrit-simulation.md` (simulation F-1 et F-2, jamais versée) sha256
  `e882de13b40c1fd7cc9100d2f99fe826a52a1fd478ef44a084e330f93740414c`.
- `outils/` (16 fichiers) et `sorties/` : sommes dans `SHA256SUMS`.
