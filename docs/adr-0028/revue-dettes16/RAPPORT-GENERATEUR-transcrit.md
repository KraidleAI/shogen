# Rapport du générateur de DETTES-T16 (BIBLIO-API) (transcrit)

> Transcription par l'orchestrateur le 2026-10-15 13:39:21 UTC du fichier dettes16/RAPPORT-GENERATEUR.md ; contrôle FM-1.1 des transcripts du générateur et du réviseur G2, par le fm11.py versé et par celui de DT3-E : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# RAPPORT-GENERATEUR — lot de dettes DETTES-T16 (BIBLIO-API)

Gate 0 : modèle résolu `claude-opus-5-5` (générateur G1, effort `max`). Heures UTC lues par `date -u`. Dépôt
`/home/user/shogen` lu seulement (`git --no-optional-locks`), aucune écriture git ; `SHOGEN_S2_CAMPAGNE_CONTROL` jamais
posée (retirée de l'environnement des exécutions par `env -u`) ; aucun emplacement interdit ouvert ni listé ; aucune
pièce de D.2 ; aucune API de données appelée. Travail du 2026-10-10 (08:46 à 09:28), interrompu, repris le 2026-10-15 à
10:12 sur message du coordinateur.

## 1. Rattachement (G0) et base

- Brief : `BRIEF-DETTES-T16.md` (24 l., sha256 `6e54efbc544d43612466641ec453e861dc0e5755b86b9adb04bbe23a528bf34e`), lu en
  entier le 2026-10-10 à 08:46:04.
- ADR-0028, annexe B.85, `docs/adr-0028/ANNEXE-B-items.md` l.1361 : SHOGEN-CALIB-FORMES-API-1 (prix : une page citée datée
  ou une capture par place) [lu] ; item SHOGEN-BIBLIO-API-BOURSES-1, formé par l'orchestrateur au brief (absent de
  l'annexe) ; règle de `biblio/` (INDEX l.11-14) et forme de la section DETTES-T14 (INDEX l.388-437 ; annexe B.96,
  l.1627-1650) [lu].
- Base de départ : `87249c221fd408d1bd77d10d9e4303fdb288db27` (lue le 2026-10-10 à 08:46:33) ; le brief dit « contre la
  tête » sans nommer de commit. La tête a avancé pendant le lot : `73894cc5c78937ac9046521488668ec688eb4931` (2026-10-10
  09:25:42), puis, à la reprise, `41e69bdc23eb3c07b36009406770d3faf0e3539a` (lue le 2026-10-15 à 10:14:02 ; 8 commits
  depuis la précédente : DETTES-T2 DT2-c à DT2-h, GARDE-FAITS, PREAVIS-S2). Sur chaque intervalle, `biblio/INDEX.md`
  (sha256 `2e54fccdd134f82a09ff0faff273938e5b273eaebe90c9497cd61d3e2e9c2618`, 437 lignes, 196 artefacts déclarés),
  `xtask/`, `WISHLIST.md`, `enforcement/`, `.cargo/`, `Cargo.toml`, `Cargo.lock` et `.gitignore` sont inchangés
  (`git diff --quiet` sur ces chemins nommés) : DT16-a, régénéré sur la dernière tête, a les mêmes octets ; la preuve
  du §7 est faite sur la copie de `41e69bdc23eb3c07b36009406770d3faf0e3539a`. `biblio/` de la session : 252 fichiers
  (196 artefacts, 55 `*.sidecar`, INDEX), 113176322 octets.
- Crochet GARDE-FAITS de la tête lu (`.claude/hooks/garde_faits.py`, R1 à R6) : identifiants et nombres écrits seulement
  s'ils ont été affichés par un outil ; fichier lu avant d'y écrire par le shell ; empreintes sha256 écrites en entier
  (un préfixe tronqué n'est pas un identifiant affiché pour ce crochet).

## 2. Pièces (8, dossier `pieces/`, `pieces/SHA256SUMS`, `sha256sum -c` : 8 OK)

Téléchargées le 2026-10-10 par `outils/telecharger.sh` (un dossier neuf et vide par téléchargement, `curl -sS -L`,
HTTPS seul, mandataire de la session, vérification TLS active, agent utilisateur par défaut de `curl`), journal
`tmp/journal-telechargements.tsv` (heures avant et après, code, URL effective, redirections, type, taille, sha256), puis
copiées sous leur nom final.

| pièce | URL (demandée ; effective si redirigée) | fin UTC | HTTP | taille | sha256 |
|---|---|---|---|---|---|
| `coinbase-exchange-api-get-product-candles-2026-10-10.md` | https://docs.cdp.coinbase.com/api-reference/exchange-api/rest-api/products/get-product-candles.md (`text/markdown`) | 08:49:41 | 200 | 4994 | `ce66414274ecc32b6c5317d6a595f8e131f7db602596b9cad0bac485e987548f` |
| `coinbase-exchange-rest-api-types-2026-10-10.html` | https://docs.cdp.coinbase.com/exchange/rest-api/types | 08:49:58 | 200 | 798628 | `04001a41ac7eb236f4677ee87158f922cbcc4f7538de61189f3cd54be50ae501` |
| `bitstamp-api-v2-docs-2026-10-10.html` | https://www.bitstamp.net/api/ | 08:51:12 | 200 | 2010852 | `a987886bce0afa68616e86aed037c1df48a666685a6dee8d3bbf1f57c9fd3a9a` |
| `bitfinex-docs-rest-public-candles-2026-10-10.html` | https://docs.bitfinex.com/reference/rest-public-candles | 08:51:23 | 200 | 261505 | `e541fcc2813766c49393031746b015f44b9154fb55e0c744b55381553e732887` |
| `okx-docs-v5-en-api-guide-2026-10-10.html` | https://www.okx.com/docs-v5/en/ | 08:51:34 | 200 | 5247633 | `009d139c6386fad226e43a47a346d00be4cac2fe8412779078d65c2cc9e50f0d` |
| `okx-en-us-historical-data-2026-10-10.html` | https://www.okx.com/en-us/historical-data | 08:51:46 | 200 | 59999 | `0b10a2edac98a2910ad15ae8526e71f4ba45dd7869131246bf1b0944fe59efc2` |
| `okx-en-us-api-agreement-2026-10-10.html` | https://www.okx.com/help/okx-api-agreement ; 302 vers https://www.okx.com/en-us/help/okx-api-agreement | 08:53:09 | 200 | 117050 | `129a9087aa0dc043a4b86da3df501bb15d53302b7ff5faa5a7995e118c29975f` |
| `okx-en-us-terms-of-service-us-2026-10-10.html` | https://www.okx.com/en-us/help/terms-of-service-us | 08:53:09 | 200 | 158504 | `cbbf5cc0c927f107291e600edce70e62af038849346eeb435a12e4eb1cd1abcd` |

Les pages servies en HTML statique portent le texte cité : les copies Firecrawl du chercheur (`formes-api/bitstamp.md`,
`formes-api/okx.md`) ne servent qu'à la comparaison (§3, §4) ; aucune capture n'est demandée à l'orchestrateur pour les
citations.

Réponses non versées (gardées au dossier du lot, `tmp/dl/`, sha256 au journal) : la page des bougies de Coinbase en HTML
(892776 o ; le `.md` lui est préféré par le brief) ; les conditions de Coinbase liées au pied de page
(`https://www.coinbase.com/legal/developer-platform/terms-of-service` : 403, défi Cloudflare) ; les conditions générales
de Bitstamp liées au pied de page (`/legal/financial-services/general-terms-and-conditions/` : 200, 212 o, défi
Incapsula) ; `https://www.bitfinex.com/legal/terms` (404, URL devinée, écart E-3) ; la page des conditions de l'API de
Bitfinex liée au pied de page du site (`/legal/general/api-terms/` : 200, 113009 o, titre seul, texte rendu par script).
Aucun refus contourné.

## 3. Citations du rapport du chercheur (`formes-api/RAPPORT.md`, 113 l., sha256 `0dff14fd0f1b473ae0e3f22c91c4e456f336f67f53a691e8dda47fdef0d1abd4`)

`outils/verifier_citations.py` (avec `outils/sg5norm.py`, reprise en Python de la normalisation de `xtask/src/sg5.rs` et
`documents.rs`), sortie `outils/verifier_citations.sortie.tsv` (sortie 1 : un span de source introuvable) :

- 52 spans entre guillemets français (table de garde : ligne et empreinte de chaque span ; rapport changé : sortie 3).
- 45 citations de pages : **44 trouvées** dans la pièce et la section qu'elles visent (sections tranchées dans les
  pièces : OHLC de Bitstamp ; données historiques, historique des bougies et performances GLP d'OKX) : 42 à l'identique
  (élision de la l.73 comprise, morceaux dans l'ordre à moins de 400 caractères) ; l.56 (Bitfinex, `sort`) avec la barre
  verticale échappée du tableau Markdown rendue ; l.40 (Bitstamp, `limit`) en forme compacte seulement (second essai de
  S-G5) : le rapport écrit `integer[ 1 .. 1000 ]`, la page `integer [ 1 .. 1000 ]` (graphie de l'extraction Firecrawl,
  qui colle `integer` aux crochets échappés).
- **1 introuvable mot pour mot** : l.64, OKX, données historiques : le rapport écrit
  `Candlestick: OHLC chart history from July 2023 onwards.` ; la page détenue porte le titre de carte « Candlestick »
  (balise h3) puis la description « OHLC chart history from July 2023 onwards. » (balise p), sans deux-points. Forme du
  chercheur (jonction du titre et de la description), non changement de page établi : aucune copie du 2026-10-09 de cette
  page ; la description est mot pour mot la même. Hors contrôle de S-G5 (aucun mot-fonction de sa liste).
- 7 spans qui ne sont pas des citations de page : 3 mentions du mot `seconds` (l.42 deux fois, l.106 : le rapport dit
  son absence pour `start` et `end` ; contrôle : dans la section OHLC de Bitstamp, une seule occurrence, à `step`) et 4
  expressions françaises du chercheur (l.98 deux fois, l.100, l.112).
- Sans écart, à noter : l.40, la citation des erreurs de `limit` joint deux cellules de la table des erreurs (raison,
  action), contiguës après débalisage.
- Pré-contrôle avant le lot (`presg5.py` sur la tête, `biblio/` de la session) : 17 fragments introuvables
  (`tmp/presg5-avant.txt`), tous dans les pièces du lot.

## 4. Trouvaille hors citations (à adjuger) : encadrés de la page d'OKX

La section « Get historical market data » de la page OKX détenue porte cinq encadrés `<aside class="notice">`, dont
« Data query rules » (« Both begin and end timestamps are inclusive ») et « Timezone specifications for timestamp
parsing » : conversion des horodatages en dates, carnets d'ordres (modules 4, 5, 6) en UTC+0 et « All other data modules
(modules 1, 2, 3, 11): UTC+8 ». La copie Firecrawl du chercheur (2026-10-09, 1902588 o) ne porte que 2 des 248 encadrés
de la page (perte systématique de l'extraction ; le texte courant y est, par exemple 114 lignes de débit dans l'une et
l'autre) ; l'en-tête `last-modified` de la page est du 2026-10-08 10:19:17 GMT, antérieur à la lecture du chercheur
[inféré : les encadrés existaient le 2026-10-09]. Le rapport écrit pour OKX qu'aucune phrase ne dit le fuseau des
fichiers et classe le point en [abs] : la page détenue le contredit pour la conversion des dates (module 2 compris).
L'alignement du contenu d'un fichier mensuel sur UTC+8 reste une inférence (la page ne dit pas les minutes que contient
un fichier). Rien de neuf pour Bitstamp (section OHLC relue en entier : ni inclusion ni ordre), pour Bitfinex (`sort`
sans défaut au schéma) ni pour l'historique des bougies d'OKX (trois encadrés, rien sur `after`, `before` ni l'ordre).
Porté à la rangée d'INDEX de la page OKX (lu, non citable) ; à adjuger pour SHOGEN-CALIB-FORMES-API-1 (§8, §9).

## 5. Série : DT16-a

| diff | fichier | + / − | sha256 |
|---|---|---|---|
| `diffs/DT16-a.diff` | `biblio/INDEX.md` | +16 −1 | `4c73834def85cb37d72d11b0f23a47c68bdec73cc9e2577e849c6080edc52749` |

- Ligne 3 réécrite sur place : `**204 artefacts détenus**` (+8, lot DETTES-T16), l'historique du compte gardé à la suite
  (forme de DT14-a) ; compte dans les 500 premiers octets (S-G6).
- Section neuve en fin de registre (l.438-452) : titre, ajout daté (`date -u`, 2026-10-10 09:16:40), provenance et bilan
  des citations, table de 8 rangées dans la forme de la règle en tête (URL exacte, date UTC, taille, sha256, conditions
  lues ou aucune licence lue, redistribuable, lu et citations vérifiées, non citable).
- Généré par `outils/generer_diffs.py` depuis `copie-tete/` (`git archive` de la tête sans emplacements interdits ni
  `*.jsonl`, exclusion vérifiée par comptes seuls ; 1391 membres pour `41e69bdc23eb3c07b36009406770d3faf0e3539a`) et
  `blocs/bloc-dt16.md` (sha256 `e31aff810e23e8852c4d392806b6a0d44fb6d55d78a21ff67cf99106b246084f`), assertions : préfixe
  unique de la l.3, 196 + 8 rangées = 204, aucune autre ligne changée ; `git apply --check` puis `git apply` sur une copie
  neuve de chaque tête : état final égal à l'état généré (`cmp`). 16 lignes ajoutées (R-25 : au plus 200). Aucun octet de
  pièce au dépôt ; aucune marque de tâche nue (R-13).
- Citations de la section : `outils/verifier_index.py`, sortie `outils/verifier_index.sortie.txt` : 48 spans, chacun trouvé
  mot pour mot dans la pièce de sa rangée, aucun au-delà de 25 mots ; taille et sha256 de chaque rangée égaux aux octets ;
  chaque pièce a sa rangée ; 0 écart.
- Aucun décalage : `outils/lignes_conservees.py` (preuve sans motif) : CONFORME, l.3 seule réécrite, 15 lignes après la
  l.437. `refs_index.py` du réviseur G2 de DETTES-T14 (inchangé, sha256
  `4a46493bf7da4c334af90615181c9d54172be3ee525ef0b6ab7291b292562fdd`) sur les 117 fichiers nommés de sa liste
  (`noms-g2-presents.txt`, sha256 `a8de9af4f599171b5bf0c0f41b7fcfce5d79afac246949b3cccf720948783b87`) : 37 renvois vers
  l'INDEX, seule la l.3 diffère (`docs/G2-lot-CORR.md:355`, ligne du compte, réécrite à chaque versement) ;
  `refs_decalees.py` (inchangé, sha256 `c15a0ace28a0846ebf91c8f3a8e6cc0f7facd811921f4c0efa05cadd02327a56`) : 223 renvois,
  0 décalé. Mêmes résultats sur les trois têtes.
- Mutants des contrôleurs (`outils/mutants.sh`, sortie `outils/mutants.sortie.txt`) : 9 tués sur 9 (citations : pièce
  altérée, rapport altéré ; INDEX : citation altérée, citation de 26 mots, taille fausse ; versement : source altérée,
  cible divergente, INDEX sans la section ; lignes conservées : l.200 retouchée).

## 6. Versement privé

`outils/verser_biblio.py` (forme de celui de DETTES-T14) : lit les rangées de la section DETTES-T16 (nom, sha256), cherche
chaque pièce dans les sources, refuse avant toute copie si une pièce manque, si un sha256 diffère, ou si la cible existe
avec d'autres octets ; copie, puis recontrôle le sha256. Éprouvé sur `copie-serie/biblio/` (251 fichiers de la session
copiés) : 8 copiés, puis 8 déjà présents à l'identique ; 260 fichiers, 204 artefacts. Jamais lancé sur le `biblio/` du
dépôt (acte de l'orchestrateur) ; commande proposée :
`python3 -I <lot>/outils/verser_biblio.py biblio/INDEX.md biblio <lot>/pieces`.

## 7. Preuve

Copies de `41e69bdc23eb3c07b36009406770d3faf0e3539a` (`git archive`, sans emplacements interdits ni `*.jsonl`) :
`copie-tete/` (tête seule, 251 fichiers de la session ajoutés à `biblio/` : 196 artefacts) et `copie-serie/` (même tête,
DT16-a appliqué, mêmes octets plus les 8 pièces versées par `verser_biblio.py` : 260 fichiers, 204 artefacts). Lancement
détaché d'`outils/preuve_gates.sh` (2026-10-15, 10:15:22 à 10:26:52 ; `uptime` : charge 2.49 au départ ; `df` : 5.1G
libres), journaux filtrés en `journaux/` par `outils/filtrer_gates.py` (lignes VERDICT, notes de compte, emplacement
`chemin:ligne` des violations, jamais leur texte) ; sorties complètes hors livrables (`tmp/preuve/`).

- **`cargo --locked --offline xtask verify` sur `copie-serie/`** (`journaux/verify-serie.txt`, sortie 1) : S-G1 à S-G4
  VERT ; **S-G5 VERT** (347 fragments contrôlés, corpus INDEX + 204 artefacts sur 204 déclarés : régime complet) ;
  **S-G6 VERT** (compte déclaré 204, compte réel 204) ; S-G7a et S-G8 VERT ; S-G9 ROUGE, 1 violation,
  `docs/17-modele-de-menace.md:70` (copie creuse, attendue) ; `cargo fmt --check`, `no_std` du vérificateur,
  `cargo clippy -D warnings` VERT ; verdict global ROUGE par S-G9 seul.
- **Tête seule, `xtask gates` sur `copie-tete/`** (`journaux/gates-copie-tete.txt`) : mêmes verdicts (S-G5 : 347
  fragments, 196 sur 196 ; S-G6 : 196 = 196 ; S-G9 : la même violation, `docs/17-modele-de-menace.md:70`) : la violation de
  S-G9 précède le lot.
- **Échec montré avant correction (simulation du versement du rapport)** : le rapport du chercheur posé dans la copie sous
  un chemin de simulation (`docs/adr-0029/g0-calib/formes-api-simulation/RAPPORT.md`, chemin choisi pour l'essai, pas une
  décision de versement). Sans les pièces (`journaux/gates-sim-tete.txt`) : **S-G5 ROUGE, 17 violations**, aux lignes 18,
  19, 20 (deux), 21, 23, 24, 39, 40, 41, 53, 54, 55, 81, 82, 83 et 84 du rapport (les 17 fragments du pré-contrôle). Avec
  la série et les pièces (`journaux/gates-sim-serie.txt`) : **S-G5 VERT**, 364 fragments contrôlés (347 + 17), corpus 204
  sur 204 ; S-G4 VERT sur le rapport ; S-G9 inchangé.
- **`python3 -B enforcement/docs-sha256sums.py .`** sur `copie-serie/` (`journaux/docs-sha256sums-serie.txt`), dernière
  ligne : `docs-sha256sums : conforme : 42 SHA256SUMS, 324 ligne(s), dont 11 absente(s) admise(s) (SHOGEN-SIM-SOMMES-1) ;
  4 fichier(s) non listé(s), non refusés` ; sortie 0.
- **Suite `s2-harness`** sur `copie-serie/` (`python3 -B -m unittest discover -s tests -t .`,
  `SHOGEN_S2_CAMPAGNE_CONTROL` retirée) : `Ran 419 tests`, `OK (skipped=2)`, sortie 0 (`journaux/s2-harness-serie.txt`).
- **`presg5.py`** (outil de l'orchestrateur, sha256 `60de40770b2889b7dc449b863b42755df757789c7063ba445cbd982c81a87ef0`) sur
  `RAPPORT.md`, racine `copie-serie/`, détaché (2026-10-15, 10:27:18 à 10:43:45, journal
  `journaux/presg5-serie-2026-10-15.txt`) : `presg5 : 0 fragment(s) introuvable(s)`, sortie 0 (avant le lot, sur la
  tête : 17). Durée de 16 minutes, due au débalisage quadratique de l'outil sur la page OKX (§9, point 5).
- **Tête du moment, à la fin** : `2b8fb5944d353e8c7867b85a1cb4b85ae95f6953` (lue le 2026-10-15 à 10:43:57 ; 5 commits de
  DETTES-T2 depuis la tête de la preuve) ; `biblio/INDEX.md`, `xtask/`, `WISHLIST.md`, `enforcement/`, `.cargo/`, Cargo et
  `.gitignore` inchangés depuis `41e69bdc23eb3c07b36009406770d3faf0e3539a` ; `git apply --check` de DT16-a sur l'INDEX de
  cette tête (`git show`) : OK ; état appliqué égal à l'état généré (`cmp`).

## 8. Phrases de fermeture proposées (annexe B)

- **SHOGEN-BIBLIO-API-BOURSES-1** fermé (lot DETTES-T16, DT16-a) : les six pages de documentation que cite le rapport du
  chercheur de SHOGEN-CALIB-FORMES-API-1 (Coinbase Exchange : bougies en Markdown brut et types ; Bitstamp ; Bitfinex ;
  OKX : documentation v5 et données historiques) et deux pages de conditions d'OKX sont détenues (copies du 2026-10-10,
  08:49 à 08:53 UTC ; sha256, tailles et conditions à l'INDEX, 204 artefacts ; octets privés versés par
  `verser_biblio.py` du lot) ; les 52 spans du rapport contrôlés par script : 44 des 45 citations de pages trouvées dans
  la pièce et la section visées, `presg5.py` sans fragment introuvable, S-G5 et S-G6 VERT sur copie ; reste une citation
  qui n'est pas mot pour mot (rapport l.64 : deux-points ajouté entre le titre de carte et sa description), à corriger
  au versement du rapport (lot DETTES-T2).
- **SHOGEN-CALIB-FORMES-API-1**, volet pièces (l'item reste ouvert) : pages citées détenues et datées (DETTES-T16) ;
  Bitfinex établi sur pièce (bornes incluses, `>=` et `<=`) ; Coinbase (inclusion et format des bornes d'une requête) et
  Bitstamp (inclusion, articulation de `limit` avec `end`) restent non dits par leur page ; OKX : la page détenue dit le
  fuseau de conversion des horodatages en dates pour les fichiers historiques (UTC+8 pour le module 2, encadré absent de
  la copie du chercheur), l'alignement du contenu des fichiers mensuels restant inféré ; déclencheur inchangé
  (condition de l'épinglage, E-CA-27).

## 9. Limites, items à former (règle PAROXYSME)

1. **Citations du rapport à corriger au versement (lot DETTES-T2)** : l.64 (deux-points, §3) ; à titre de graphie, l.40
   (`integer[` contre `integer [` sur la page). Correction ou erratum daté au versement ; propriétaire : orchestrateur.
2. **Énoncé d'OKX absent de la copie du chercheur (§4)** : le rapport, tel qu'il sera versé, dit qu'aucune phrase de la
   documentation d'OKX ne donne le fuseau des fichiers ; la page détenue porte la convention de conversion (UTC+8 pour
   les modules 1, 2, 3, 11). Erratum à prévoir au versement du rapport (à adjuger) ; à peser pour l'épinglage (E-CA-27)
   par le propriétaire de SHOGEN-CALIB-FORMES-API-1 (DT2-c, à la tête, traite déjà les mois voisins d'OKX : son sujet
   seul est lu, son code non). Leçon de méthode : une copie Firecrawl de cette page perd 246 encadrés sur 248 ; un [abs]
   établi sur une telle copie n'est pas une absence.
3. **Conditions non lues** : Coinbase (403), Bitstamp (défi Incapsula), Bitfinex (texte rendu par script) ; OKX : seules
   les versions américaines sont détenues (le site redirige la session vers `/en-us/`), la version mondiale ou européenne
   de l'accord d'API et des conditions ne l'est pas. Sans effet sur ce lot (copies privées, redistribuable : non) ; une
   capture (connecteur Firecrawl de l'orchestrateur, ou session locale) si la question de redistribution se pose.
4. **Conditions d'usage des données de marché, lues en passant (signal, pas une décision)** : l'accord d'API d'OKX
   (version américaine, §9.4) limite les données de marché, y compris celles des points d'accès publics, à un usage
   personnel et non commercial et interdit de les publier ou de les redistribuer ; la page de Bitstamp renvoie l'usage
   commercial de ses données à un contrat de licence. Le lot CALIB-ACTIFS télécharge des historiques publics de ces
   places : question à porter à l'investisseur (et, le cas échéant, à la question posée à l'avocat, Q-A du procurement).
5. **Outil `presg5.py`** (dossier `outils/` du scratchpad, hors dépôt) : débalisage par tranches de chaînes Python,
   quadratique ; sur la copie de la série (page OKX de 5 Mo, 306899 balises ouvrantes), durée au §7 ; une version par
   positions d'octets (forme de `sg5norm.retirer_balises`) le rendrait linéaire.
6. **Durabilité** : les 8 pièces n'existeront, une fois versées, que dans le `biblio/` de la session cloud ;
   SHOGEN-BIBLIO-COPIE-DURABLE-1 s'étend à elles (un re-téléchargement par les URL de l'INDEX donnera d'autres octets :
   pages mutables).
7. **Restes [abs] de SHOGEN-CALIB-FORMES-API-1** : ce lot ne les lève pas (Coinbase, Bitstamp ; ordre et inclusion de
   l'historique des bougies d'OKX) ; ils demandent une capture d'horodatages (hors mandat de lecture).

## 10. Écarts

- **E-1 (consigne SHOGEN-HARNAIS-ECHAPPEMENTS-1)** : les séquences d'échappement unicode (barre oblique inverse, u,
  quatre chiffres) tapées dans les premières versions de `sg5norm.py` et `verifier_citations.py` sont arrivées converties
  en caractères (constaté sur les octets) ; équivalent pour Python, mais contraire à la consigne : les deux scripts ont
  été réécrits sans aucune barre oblique inverse (caractères produits par `chr()`) ; les scripts écrits ensuite en
  comptent 0 (`grep -c -F`). `telecharger.sh`, écrit et employé avant, porte 12 barres voulues (10 tabulations et 1 saut
  de ligne de format pour `curl -w` et `printf`, 1 continuation de ligne) : octets contrôlés un à un ; le journal TSV qu'il
  a écrit a 11 colonnes sur chacune de ses 13 lignes. Deux commandes de diagnostic ont porté une barre tapée, sans effet
  sur un livrable (le compte qu'en tirait la première est refait par S-G6 au §7).
- **E-2** : une citation de ma rangée d'INDEX (accord d'API d'OKX) n'était pas mot pour mot (la page porte `not:(a)` sans
  espace) ; attrapée par `verifier_index.py` avant la série, remplacée par un extrait exact.
- **E-3** : une URL de conditions de Bitfinex devinée (`/legal/terms`, 404) avant de lire le lien du pied de page du site
  dans la réponse (`/legal/general/api-terms/`) ; dans le périmètre du brief (pages de conditions de ces sites), mais non
  liée par une pièce.
- **E-4** : la page des bougies de Coinbase a aussi été téléchargée en HTML (le `.md` est versé, le HTML non).
- **E-5** : deux passages de `presg5.py` sans résultat : le premier, sur un état non final, arrêté par moi après 7
  minutes (sortie partielle vide supprimée) ; le second, détaché le 2026-10-10 à 09:17:03, perdu à l'interruption de la
  session (journal réduit à sa ligne de début). Aucun ne compte ; refait le 2026-10-15 (§7).
- **E-6 (listes)** : listes non récursives, sans motif, de dossiers nommés du scratchpad (`s2bis/formes-api/`, `outils/`,
  `s2bis/dettes14/` et ses dossiers `outils/`, `g2/`, `g2/outils/`, `g2/tmp/`, `phase2/`) pour trouver les outils voisins
  que nomme le brief ; listes de `biblio/` (dépôt et copies : un dossier plat, comptes, comme S-G6). Aucune liste de
  `docs/` ; aucun emplacement interdit ; les copies de la tête sont faites par `git archive` avec exclusions, sans liste.
- **E-7** : le premier passage de `outils/mutants.sh` lisait le code de sortie après une substitution de commande placée
  dans les arguments du verdict : trois verdicts VIVANT faux (versement, sortie réelle 2, vue 0) ; harnais corrigé (code
  capté avant), repassé : 9 tués sur 9.
- **E-8** : une mesure de la taille de la cible de compilation du lot (`tmp/target`) par parcours récursif (équivalent
  de `du`) sur mon propre dossier du scratchpad, contraire à la lettre du brief ; surveillance par `df` seul ensuite.

## 11. Journal de provenance (G1)

Sources lues (niveaux : [lu] lu sur la pièce ; [2nd] source secondaire ; [abs] cherché, absent) :

- [lu] `BRIEF-DETTES-T16.md` en entier ; `formes-api/RAPPORT.md` en entier ; `outils/presg5.py` en entier.
- [lu] `biblio/INDEX.md` à la tête, l.1-437 (les lignes longues de la fin sur leurs 1500 premiers caractères à
  l'affichage ; contrôles par script sur les lignes entières).
- [lu] `docs/adr-0028/ANNEXE-B-items.md` : l.261 (titre de B.16), l.1330-1362 (B.84, B.85), l.1627-1650 (B.96) ; recherche
  des noms d'items dans ce seul fichier.
- [lu] `xtask/src/sg5.rs` et `sg6.rs` en entier, `sg9.rs` l.1-80, `documents.rs` (`fichiers_du_repertoire`,
  `compte_declare_en_tete`, `normaliser_pour_recherche`), `rapport.rs` l.60-110, `lib.rs` l.60-110 et l.160-200,
  `main.rs` l.1-40, `sg4.rs` l.1-40, `.cargo/config.toml`, `.gitignore` ; `.claude/settings.json` et
  `.claude/hooks/garde_faits.py` en entier (reprise).
- [lu] outils du lot DETTES-T14 : `outils/verser_biblio.py`, `extraire.sh`, `executions_controle.sh`,
  `verifier_serie_c3.sh`, `lignes_conservees.py`, `decalages_anterieurs_index.py` ; `g2/outils/refs_decalees.py`,
  `refs_index.py` ; passages de `NOTES.md`, `RAPPORT-GENERATEUR.md` (l.14-30, l.280-295, l.510-530), `g2/NOTES.md`
  (lignes trouvées par recherche dans ce fichier) ; `phase2/decalages-anterieurs-ba5ea95-index.tsv` ;
  `g2/tmp/noms-g2-presents.txt` (117 noms, employé comme liste).
- [lu] les 8 pièces, aux passages cités par le rapport et par l'INDEX (Coinbase : le `.md` en entier ; Bitstamp : section
  OHLC en entier, section des limites de requêtes ; Bitfinex : paramètres et métadonnées ; OKX : sections des données
  historiques, de l'historique des bougies, des bougies, champ `dataDate`, avis de l'accord d'API ; données historiques :
  carte des bougies, titre, pied de page ; accord d'API : §1.9, §9 ; conditions américaines : §8, dates).
- [lu] réponses non versées : en-têtes et texte visible (403 de Coinbase, défi Incapsula, 404 et coquille de Bitfinex).
- [2nd] copies Firecrawl du chercheur `formes-api/bitstamp.md` (214569 o, sha256
  `53d1d385eca6d56fe978aa650487a9afd4c00dbf3535acdfb882c92f12e92f35`) et `formes-api/okx.md` (1902588 o, sha256
  `6ab70e78a4c7c2fdcf1e3ad77f01ec65c78717fba3c25d5c554b48eb56c999ef`), du 2026-10-09 vers 11:33 : comparaison seulement.

Commandes et sorties (fichiers au dossier du lot) : `git rev-parse HEAD` à 08:46:33, 09:25:42 et 10:14:02 (§1) ;
`git status --porcelain -- biblio/INDEX.md` : vide ; `presg5.py` avant : 17 fragments (`tmp/presg5-avant.txt`) ;
téléchargements : `tmp/journal-telechargements.tsv` ; `pieces/SHA256SUMS` ; `outils/*.sortie.*` (citations, INDEX,
lignes conservées, renvois, mutants, versement) ; `generer_diffs.py` : `DT16-a : +16 -1 ; rangées 8 ; compte 196 -> 204 ;
lignes 437 -> 452` ; preuve : §7 (journaux filtrés en `journaux/`).

Chiffres recomptés par moi, sur les octets : 52 spans, 45 citations de pages (44 trouvées, 1 non) ; 17 fragments du
pré-contrôle avant ; 196 + 8 = 204 artefacts, 252 + 8 = 260 fichiers ; 437 + 15 = 452 lignes ; 48 spans à l'INDEX ;
248 encadrés à la page OKX, 2 dans la copie du chercheur ; 306899 balises ouvrantes dans la page OKX ; 37 renvois par
numéro vers l'INDEX, 223 renvois vers les autres documents.
