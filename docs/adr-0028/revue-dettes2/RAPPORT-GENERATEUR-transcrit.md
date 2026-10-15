# Rapport du générateur de DETTES-T2, avec ses sections datées de correction (§1 à §16) (transcrit)

> Transcription par l'orchestrateur le 2026-10-15 13:51:21 UTC du fichier dettes2/RAPPORT-GENERATEUR.md ; contrôle FM-1.1 des transcripts du générateur-correcteur, du réviseur G2 et des deux contre-contrôleurs, par le fm11.py versé et par celui de DT3-E : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# DETTES-T2 : rapport du générateur (G1) pour SHOGEN-CALIB-FORMES-API-1

**Gate 0** : modèle résolu `claude-opus-5-5` (worker générateur). Horloge relue par `date -u` : début 14:38Z, fin 15:28Z,
le 2026-10-09. Dossier : `<scratchpad>/s2bis/dettes2/` (NOTES.md tenu, TMPDIR `dettes2/tmp`).

## 0. Base, reprise, réseau

- Base d'origine : tête 3deeb70 plus `dettes1/diffs-tete/BM-1.diff` (sha256 a649c7b6…, patch propre).
- Reprise à 14:57Z, après le redémarrage du conteneur (message de l'orchestrateur) : aucun processus restant, `tmp/`
  vide, sonde refaite. DETTES-T1 est commis (798176f GM-1, 60fad53 BM-1). `travail/tete` = archive de 60fad53 (sept
  exclusions). Seuls `gates.yml` (ligne s2bis) et `s2bis/tests` diffèrent de base + BM-1 ; le lot calib est identique.
  Mon travail a été reporté sur cette base sans changement.
- À la fin, la tête est 0cfbe3e (versement de DETTES-T1 et fusions). `scripts/calib-actifs`, `gates.yml`, `s2bis` et
  `enforcement` n'ont pas changé depuis 60fad53. Les quatre diffs s'appliquent en série (`patch --dry-run` puis
  `patch`), sans décalage, et le résultat est égal à `travail/w`.
- Réseau : chaque exécution est passée par `outils/run.sh` (copie de `calib3/g2/outils/run.sh` : `env -u` des huit
  variables, puis `p1b/g2/travail/outils/isole.sh`, TMPDIR dédié).
  - Sondes à 14:39Z, 14:57Z et 15:26Z : 1.1.1.1 et 8.8.8.8 en errno 101, `urlopen` refusé, mandataire 127.0.0.1:36573
    en errno 111 sous isolement. Le même mandataire est joint hors isolement, ce qui montre que la sonde discrimine.
  - Aucune requête vers une vraie place. `ps` de fin vide.
- Dépôt réel : lecture seule (`--no-optional-locks`), aucune écriture git.

## 1. Diffs (série à appliquer sur la tête 0cfbe3e, = 60fad53 pour ces chemins)

| diff | objet | lignes ajoutées / retirées | octets 92 | plancher calib | sha256 |
|---|---|---|---|---|---|
| `diffs-tete/DT2-a.diff` | pages : découpage chevauchant, filtre à la page, doublons, découpage exact | +197 / −57 | 0 | 66 | 48e5326af1c4ed9163d7d1acb0a6c81f7007efc1412dff248c59eb2de1c020e2 |
| `diffs-tete/DT2-b.diff` | sémantiques simulées par le serveur local (test de caractérisation) | +102 / −6 | 0 | 67 | de01e92d3ed5fe90d613276a5f18040f15c11f56d4817b409fad801c40b1ba5c |
| `diffs-tete/DT2-c.diff` | OKX : mois voisins, filtre à la fenêtre | +108 / −35 | 0 | 68 | e39fcfe0045a0fc0f660705edfc8325433860f44d0ea386fccea7d244b669f53 |
| `diffs-tete/DT2-d.diff` | complétude : reçues / attendues par page dans `calib_actifs.txt` | +94 / −13 | 0 | 69 | 0197eecf541744721b05ad72fbf80646b9388faa1193cfc887dd70c92ff4198e |

- Chaque diff a moins de 200 lignes ajoutées (tests, données, SHA256SUMS et gates.yml compris).
- Aucune ligne de plus de 120 caractères dans les cinq états du lot.
- Aucun `TODO` ni `FIXME`. Bibliothèque standard seule (`bisect` ajouté).
- Le SHA256SUMS du lot est recalculé à chaque diff : `sha256sum -c` passe, et la liste couvre tous les fichiers. Le
  sha256 du SHA256SUMS final est f617bc9f4aa4e44c63370445d08382c6a3fc22e3c7e4764cd6a8749a2316290a.

**Contenu par diff :**

- **DT2-a**
  - Code :
    - `socle.pages` : découpage partagé entre l'acquisition et le chargement.
    - Clés `chevauchement` du schéma, avec un contrôle de cohérence : 0 ≤ chevauchement < pas pour une place
      paginée, 0 ailleurs.
    - `parametres.json` : `pas` lu comme le nombre maximal de bougies par requête (300, 1000, 10000, valeurs
      inchangées) ; chevauchement 1 pour Coinbase et Bitstamp, 0 pour Bitfinex.
    - `acquerir.pages` passe par le découpage.
    - `bougies.serie` reçoit `fenetres` : une bougie hors de [a ; b) ∩ fenêtre est écartée. Une minute servie
      identique par deux fichiers est gardée une fois. Une minute aux valeurs différentes donne le refus
      `CA/format : minute en double aux valeurs différentes`. Une minute en double dans un même fichier donne toujours
      `minute en double`.
    - `bougies.charger` : pour une place paginée, les fichiers doivent être exactement les pages du découpage, sinon
      refus `CA/format : pages différentes du découpage de la fenêtre`.
    - README.
  - Tests :
    - `tests/test_formes.py` (outils communs, test des doublons et du découpage).
    - `synthetiques.fichiers` : écrit des pages nommées.
    - Recalés : `test_pages` (URL du nouveau découpage), `test_series.test_charger` (noms de pages), `test_cli`
      (écriture par `sy.fichiers`), `test_socle` (deux cas de cohérence).
- **DT2-b** : crochet `fonction` du serveur local de test ; `tests/test_formes_pages.py`.
- **DT2-c** : `acquerir.mois(fen, voisins)`, `mensuels` (lecture de `voisins`), branche `voisins` de `charger`, clé
  `voisins` (OKX 1, les autres 0) avec son contrôle, `tests/test_formes_okx.py`, `test_okx_reprise` (cinq mois),
  `test_socle` (voisins négatifs), README.
- **DT2-d** : `bougies.comptes`, `tau.completude`, `septembre(…, comptes)` et `main`, `tests/test_comptes.py`, comptes
  par page ajoutés à `test_formes_pages`, README.

## 2. Tableau par place et par sémantique (série reconstruite contre la vérité de la fixture)

Sources : `travail/tableau.out` (code final) et `travail/tableau-tete.out` (code d'avant, mêmes cas).

**Paramètres de la fixture**, distincts d'une place à l'autre :

| place | pas | chevauchement |
|---|---|---|
| Coinbase | 5 | 1 |
| Bitstamp | 7 | 2 |
| Bitfinex | 4 | 0 |

OKX a voisins 1 et Binance voisins 0. Chaque cas est joué sur la fixture (14 minutes) et avec les paramètres du lot
(1 200 minutes).

| place | sémantique simulée | code final : manquantes / en trop / différentes | code d'avant |
|---|---|---|---|
| Coinbase | `end` inclus | 0 / 0 / 0 (4 et 5 pages) | 0 / 0 / 0 |
| Coinbase | `end` exclu | 0 / 0 / 0 | **2 et 3 minutes perdues en silence**, sans refus : [1775001840, 1775002380] ; [1775019540, 1775037540, 1775055540] |
| Coinbase | inclus + bougies qui précèdent `start` (altérées) | 0 / 0 / 0 | refus CA/format (temps hors fenêtre) |
| Coinbase | exclu + bougies qui précèdent `start` | 0 / 0 / 0 | refus CA/format |
| Bitstamp | `end` inclus, `end` prioritaire, `limit` ≤ pas | 0 / 0 / 0 (3 et 2 pages ; 14/14 et 1200/1200 reçues) | 0 / 0 / 0 |
| Bitstamp | `end` exclu | 0 / 0 / 0 | refus CA/format |
| Bitfinex | bornes incluses, tronqué à pas (`[lu]`) | 0 / 0 / 0 | 0 / 0 / 0 (déjà conforme) |
| OKX | mensuels UTC (début et fin de juin) | 0 / 0 / 0, mois 05, 06, 07 | refus CA/format |
| OKX | mensuels UTC+8 | 0 / 0 / 0 | refus CA/format |
| OKX | mensuels UTC−4 (le mois précédent est nécessaire) | 0 / 0 / 0 | refus CA/format |

**Fonctionnement de la simulation :**

- Coinbase :
  - Une requête au-delà de `pas` points est rejetée (404).
  - Sous la variante « avant », la place rend les `pas` bougies les plus récentes jusqu'à la fin ; les plus anciennes
    précèdent `start` et ont une clôture altérée.
  - Les minutes sans échange sont absentes, et les réponses arrivent dans l'ordre décroissant.
- Bitstamp : `limit` est compté à rebours depuis `end`, toutes les minutes sont rendues, une requête au-delà de `pas`
  est rejetée.
- Bitfinex : tronqué à `pas`.

**Doublons** (DT2-a, pages de Coinbase écrites à la main) :

- La minute de chevauchement, identique dans deux pages, est gardée une fois.
- Sont écartées : la minute 6 placée dans la page 0 (hors de sa page, altérée) et la minute 14 (hors de la fenêtre).
- La minute 8 à clôture différente, ou à volume différent, donne le refus nommé
  `REFUS CA/format : minute en double aux valeurs différentes ; actif ETH ; place coinbase`.
- Une minute en double dans une même page donne `minute en double`.
- Une page hors du découpage, ou une page absente, donne `pages différentes du découpage de la fenêtre`.

## 3. Rouges (tests neufs sur le code d'avant ; 0 ERROR, uniquement des FAIL d'assertion)

L'outil `outils/rouge.sh` prend le code d'un état et les tests de l'état suivant.

| test | code d'avant | résultat |
|---|---|---|
| DT2-a, `test_formes` | tête | 4 FAIL (cas 0, 1, 4 et 5 ; cas 3, double dans une page, déjà refusé) |
| DT2-b, `test_formes_pages` | tête | 12 FAIL, dont Coinbase « exclue » `(([1775001840, 1775002380], [], []), …)` : minutes perdues sans refus |
| DT2-b, `test_formes_pages` | état après DT2-a | vert : c'est un test de caractérisation, le correctif est dans DT2-a ; son rouge est montré sur la tête |
| DT2-c, `test_formes_okx` | état après DT2-b | 7 FAIL |
| DT2-d, `test_comptes` et `test_formes_pages` | état après DT2-c | 15 FAIL |
| les quatre ensemble | tête | 26 FAIL |

Sorties : `travail/rouge-{a,b,b-sur-a,c,d,tout}.out` ; premier rouge monobloc dans `travail/rouge-1.out`.

## 4. Mutants (`outils/mutants.py`)

**Méthode :**

- Ligne exacte du job `calib-actifs-unittest`, plancher 69, sous `run.sh` et `env -i`.
- Nouvelle session, borne 300 s par `killpg`, PAR = 2.
- Classement : sortie 1 = TUÉ, 0 = VIVANT, toute autre sortie = FATAL.
- PID 18289, campagne de 15:09:55Z à 15:16:36Z.

**Résultat : 33 TUÉS (M01 à M33), témoin M00 VIVANT, 0 FATAL, 0 INVALIDE.** Fichiers : `travail/mutants.{tsv,log}` et
`travail/mut/`.

**Chevauchement :**

- M01 : chevauchement ignoré dans le pas.
- M02 : borne de requête sans chevauchement.
- M03 : `n` faux.
- M04 : site d'appel, découpage de coinbase pris pour toute place.
- M05 : source, chevauchement lu à coinbase.

**Filtre :**

- M06 : filtre à la fenêtre entière.
- M07 : fenêtre de page non bornée à la fenêtre.
- M08 : filtre sans la minute de chevauchement.
- M09 : pages strictes.
- M10 : Binance et Kraken filtrés, non stricts.

**Doublons :**

- M11 : doublon identique refusé.
- M12 et M13 : doublon contradictoire admis, en gardant le dernier ou le premier.
- M14 : double dans un fichier admis.
- M15 : volume non comparé (tué par le cas « volume différent » seul).

**Découpage :**

- M16 : page absente admise.
- M17 : page hors découpage ignorée.

**Mois voisins :**

- M18 : site d'appel, voisins non passés.
- M19 : mois précédent non acquis.
- M20 : mois suivant non acquis.
- M21 : filtre d'OKX retiré.
- M22 : source, voisins lus à binance.
- M23 : source, voisins lus à okx au chargement.

**Compte :**

- M24 : attendues + 1.
- M25 : reçues avec la minute de fin.
- M26 : site d'appel, fenêtre descriptive à la place de la principale.
- M27 : complétude de septembre omise.
- M28 : détail par page omis.
- M29 : source, place paginée prise égale à coinbase.
- M33 : site d'appel, comptes sans découpage.

**Cohérence :**

- M30 : chevauchement non contrôlé.
- M31 : voisins non contrôlés.
- M32 : chevauchement égal au pas admis.

## 5. Matrice et gates (`travail/lourd.log`, PID 30380, de 15:17Z à 15:25Z)

- Matrice python 3.10, 3.11, 3.12 et 3.13 en `-X dev -W error` (PYTHONDEVMODE=1, PYTHONWARNINGS=error), ligne du job au
  plancher exact : `w` Ran 69, `s1` Ran 66, `s2` Ran 67, `s3` Ran 68.
  - 16 exécutions sur 16 en code 0, 0 « Exception ignored », 0 « Warning ».
  - `s1` à `s3` sont les états après DT2-a, b et c, reconstruits par `outils/scinde.py`.
- Batterie sur `w` :
  - calib-actifs : Ran 69, conforme.
  - runner `run-fixtures-verdict-suite-s2.py` : 136 ok, 0 échec.
  - s2bis : Ran 341, conforme.
  - S2 `--egal` : Ran 415, conforme.
  - Tous en code 0.
- xtask (`cargo --locked --offline xtask verify`, lignes VERDICT seules) sur la tête 60fad53 et sur `w` : les 10 lignes
  sont identiques ; la 9e est ROUGE, déjà connue sur copie (S-G9).
- Répétition à l'échelle (E-CA-26, synthétique, `outils/repetition.py`) sur `w` :
  - `tau.py` sort en code 0, en 90,2 s, avec une mémoire maximale de 875 492 Kio.
  - Coinbase d'ETH produit 439 pages, et la complétude de Bitstamp vaut 131040/131040.
  - Pour comparaison, calib3 mesurait 86,1 s et 838 600 Kio.

## 6. Écarts

- **E-1. E-CA-16, lettre « aucune bougie hors fenêtre ; minute en double : refus ».**
  - Pour les pages et pour OKX, la lettre est adoucie comme la DECISION l'ordonne (points 2 et 3) : une bougie hors
    de sa page ou de la fenêtre est écartée, et un doublon identique entre deux fichiers est admis.
  - Restent des refus : le doublon contradictoire, le double dans un fichier, et toute minute hors fenêtre chez
    Binance et Kraken.
  - La série gardée n'a toujours aucune minute hors fenêtre.
- **E-2. Propriété C-7 / G08 « aucune bougie demandée hors fenêtre ».**
  - Elle est renversée, comme le veut la DECISION au point 1 : la dernière page demande la minute qui suit la fenêtre
    (Bitstamp de septembre : `n=31 … end=1790812800`), puis l'écarte au chargement.
  - `test_pages.test_main` est recalé en conséquence.
- **E-3. Tests existants recalés.** Ce sont des valeurs neuves calculées à la main ; aucun test n'est affaibli ni
  sauté.
  - `test_pages_bornees` : URL, n = 701, noms de pages.
  - `test_main` : n = 31.
  - `test_okx_reprise` : cinq mois.
  - `test_charger` : noms du découpage. L'assertion « dans l'ordre des noms » de sa docstring est retirée, car elle
    n'était pas vérifiable sur un dictionnaire.
- **E-4. Fixture synthétique.** `synthetiques.fichiers` lit `chevauchement` par `.get(…, 0)`. L'absence de la clé
  donne le découpage d'avant, ce qui permet le rouge sur le code d'avant. Ce n'est le cas que dans la fixture : le
  schéma du lot exige la clé.

## 7. Questions (mon choix et sa raison)

- **Q-DT2-1 : `start` exclu non couvert** (item PAROXYSME à former).
  - La DECISION ne traite que l'inclusion de `end`, et j'en ai suivi la lettre : 299 minutes utiles.
  - Si Coinbase excluait `start`, deux cas se présenteraient. Avec `end` inclus, la première minute de la fenêtre
    serait perdue en silence ; avec `end` exclu, ce serait la première minute de chaque page. Seules les lignes de
    complétude le montreraient, et seulement pour une paire liquide.
  - La couverture complète demande un chevauchement des deux côtés, soit 298 minutes utiles et une requête de début −
    60 à borne. C'est à décider par l'orchestrateur ; je ne l'ai pas fait, puisque cela contredit le « 299 » écrit.
  - Bitstamp : la simulation suit `end` prioritaire, `[lu]`. Une lecture de `limit` en avant depuis `start` est
    couverte pour `start` inclus, pas pour `start` exclu.
- **Q-DT2-2 : mois d'octobre 2026 pour septembre.**
  - Les voisins de la fenêtre descriptive comprennent 2026-10. Ce mensuel n'est publié qu'après la fin d'octobre.
  - Avant cette date, l'acquisition sort en refus `CA/acquisition` (code 4) et le lancement aussi.
  - Choix : refus fermé, sans mois facultatif, parce qu'un mois facultatif ferait perdre en silence les 8 dernières
    heures de septembre sous UTC+8. Conséquence : aucun lancement avant novembre 2026, ce qui est à noter au
    calendrier. La fenêtre principale demande 2026-03 et 2026-07, qui existent.
- **Q-DT2-3 : découpage exact exigé au chargement.**
  - C'est un resserrement, avec un motif neuf sous le code CA/format existant.
  - Des bruts acquis par l'ancien code (pages de 300) seraient refusés et devraient être réacquis. Aucune acquisition
    réelle n'a eu lieu, il n'y a donc rien à migrer.
- **Q-DT2-4 : sens de « reçues ».**
  - Le compte retenu est celui des minutes présentes dans la série finale sur [début ; fin) propre à la page. Une
    minute fournie par le chevauchement de la page précédente compte.
  - « Attendues » est le nombre de minutes de l'intervalle.
  - Raison : avec ce compte, une page complète a reçues = attendues sous les deux lectures de `end` (Bitstamp 999/999),
    et une perte systématique ressort de l'écart.
  - Places sans pages : un seul total sur la fenêtre. Coinbase, Bitfinex et Kraken n'écrivent pas les minutes sans
    échange, donc reçues < attendues est normal chez eux.
- **Q-DT2-5 : paramètres nouveaux non nommés au G0.**
  - `chevauchement` est un entier en minutes et `voisins` un entier en mois. Leurs valeurs viennent de la DECISION
    (1, 1, 0 ; 1 pour OKX).
  - Je les ai généralisés, plutôt que de coder le nom des places en dur, pour que la fixture puisse donner une valeur
    distincte à chaque place, comme l'exige le brief.
- **Q-DT2-6 : découpe en quatre diffs.**
  - DT2-b est un test seul, puisque le correctif de pages est dans DT2-a pour tenir sous 200 lignes.
  - Son rouge est montré contre la tête, ce qui est le code d'avant du lot.

## 8. Journal de provenance (G1)

**Sources, niveau [lu] :**

- `formes-api/DECISION.md` et `formes-api/RAPPORT.md`, en entier.
- `calib3/BRIEF-CA.md`.
- PROPOSITION : §4.1, §4.2 et §5 (§5.7 compris).
- Code du lot à la tête : `acquerir.py`, `bougies.py`, `socle.py`, `tau.py`, `parametres.json`, `lancer.sh`, et les
  tests touchés.
- `dettes1/NOTES.md` et les outils de dettes1 réutilisés en copie.
- `calib3/RAPPORT-GENERATEUR.md` §5 : le chiffre de comparaison de la répétition.

**Repères du chiffre de chaque requête :**

- Horodatages des bornes de mois et de pages calculés par `date -u -d` : 1780272000, 1782842400, 1782864000,
  1777593600, 1785542400, 1775019540, 1775037480, 1775043600, 1790811000, 1790812800.
- Comptes à la main dans les docstrings.

**Lectures interdites :** aucune ouverte, ni docs/15-16, ni rapports, ni adr-0025, ni monark, ni execution, ni
`*.jsonl`, ni pièces D.2. `SHOGEN_S2_CAMPAGNE_CONTROL` n'a jamais été posée ; seul le test du lanceur existant la pose.

**Commandes et sorties :** `travail/` contient sonde-1, sonde-2, sonde-fin, rouge-*, suite-*, job-*, mutants.*,
lourd.log, matrice_*, batterie_*, xtask-*, repetition.out et tableau*.out.

**Outils** (`outils/`) : run.sh, sondes, fais_diff.sh, compte.py, longues.py, scinde.py, rouge.sh, mutants.py, matrice.sh,
batterie.sh, xtask.sh, lourd.sh, repetition.py et tableau.py.

**Copies lourdes supprimées :** s1 à s3, rouge, tmp, target et base (archive 3deeb70). Restent `travail/tete` (archive de 60fad53) et
`travail/w` (état final).

## 9. Ajout daté du 2026-10-09, 16:09Z (`date -u`) : passe Q1 (DECISION.md, ajout 15:29:27 UTC, Q-DT2-1)

**Ce qui change :**
- Chevauchement des deux côtés. `socle.pages` rend maintenant (début, fin, départ, borne).
- La page contient au plus `pas` − 2c minutes. La requête va de départ = début − 60c à borne = fin − 60 + 60c, ce qui
  fait `pas` bougies.
- Coinbase a donc 298 minutes utiles par page et Bitstamp 998. Bitfinex ne change pas (c = 0).
- Le filtre au chargement porte sur [départ ; borne + 60).
- Cohérence : 0 ≤ 2c < pas.
- Les versions d'avant la passe sont gardées sous `travail/avant-q1/` : quatre diffs, rapport, SHA256SUMS, `w`, outils
  et premier essai de campagne.

**Diffs** (mêmes noms ; ils s'appliquent en série sur la tête 0cfbe3e et donnent `w`) :

| diff | ajoutées / retirées | octets 92 | plancher | sha256 |
|---|---|---|---|---|
| DT2-a | +199 / −60 | 0 | 66 | 4a07b3680ba34bd1efc11b0efa4343ff097282b4c62723752ee6b95ba895d673 |
| DT2-b | +107 / −6 | 0 | 67 | 1cddb96cb2233c4282e61f3b3411db0db5750c6a920487c5a85e8b713f93a05f |
| DT2-c | +108 / −35 | 0 | 68 | 1cc25657f10f3b322f27851ba2b77903e129055efe3333a471fe15b1e7ceb16b |
| DT2-d | +94 / −13 | 0 | 69 | 9aef8d1b52b6952bddbb9b78f4321887c684b030205f17b758d3f246e43ef1ee |

- Le SHA256SUMS du lot final a pour sha256 e47a3c77975e6afc373e9d8e9a6113c8b12d9b2669808d624a198f97880798fe.
- Aucune ligne de plus de 120 caractères, aucun TODO.

**Tests :**
- Le simulateur est étendu :
  - Coinbase : `start` exclu seul, et `start` et `end` exclus ;
  - Bitstamp : `start` prioritaire avec `limit` compté en avant, `start` inclus ou exclu.
- Fixture : pas 5, 9 et 4 ; chevauchement 1, 2 et 0.
- Recalés à la main :
  - `test_pages_bornees` : 23:59-04:58, 04:57-09:56, 09:55-11:40 ; n = 702 ; début 1775001540 ;
  - `test_main` : n = 32, start 1790810940 ;
  - `test_charger` : pages T0, T0 + 17880, T0 + 35760 ;
  - doublons : pas 6, plus le cas « minute 3 contradictoire au chevauchement de début ».

**Tableau.** Nombre de minutes manquantes, sur la fixture de 14 minutes et sur 1 200 minutes avec les paramètres du lot :

| sémantique simulée | tête | avant Q1 | final |
|---|---|---|---|
| Coinbase, `start` exclu, `end` inclus | 3 et 4 | **1 et 1** (la minute 1775001600, en silence) | 0 et 0 |
| Coinbase, `start` et `end` exclus | 5 et 7 | **4 et 5** (la première minute de chaque page) | 0 et 0 |
| Bitstamp, `start` prioritaire, inclus | 0 | 0 | 0 |
| Bitstamp, `start` prioritaire, exclu | refus CA/format | **1 et 1** (1775001600) | 0 et 0 |

- Sources : `travail/tableau-q1.out`, `tableau-q1-tete.out` et `tableau-q1-avant.out`.
- Toutes les autres sémantiques (§2) restent égales à la vérité, et les comptes par page sont égaux aux valeurs à la
  main.

**Rouge par AssertionError avant le correctif** (`travail/rouge-q1-pages.out`) :
- Le test étendu, joué sur le code d'avant Q1, donne 20 FAIL et 0 ERROR.
- Parmi eux, les pertes silencieuses : `(([1775001600], [], []), …)` pour `start` exclu ; la première minute de
  chaque page pour `start` et `end` exclus ; `[1775001600]` pour Bitstamp `start` exclu.
- Les tests anciens recalés donnent sur ce code 2 ERROR (refus levé : URL absente du serveur, page hors découpage),
  dans `rouge-q1-anciens-recales.out`. Ce ne sont pas des tests neufs.
- Rouges par diff, sur l'état précédent, tous sans ERROR :
  - DT2-a (sur la tête) : 6 FAIL ;
  - DT2-b (sur la tête) : 20 FAIL ;
  - DT2-c : 7 FAIL ;
  - DT2-d : 23 FAIL.

**Mutants** (`travail/mutants-q1.{tsv,log}`, PID 18595, de 15:50:06Z à 15:59:16Z, même méthode que le §4) :
- Résultat : **43 TUÉS, M00 témoin VIVANT, 0 FATAL, 0 INVALIDE**.
- Les 33 mutants M01 à M33 sont rejoués ; leurs chaînes sont recalées sur le nouveau code.
- Mutants neufs sur Q1 :
  - Q01 : chevauchement de fin seul ;
  - Q02 : départ = début ;
  - Q03 : pas − c ;
  - Q04 : URL partant du début de page ;
  - Q05 : n compté depuis le début de page ;
  - Q06 : start ISO compté depuis le début de page ;
  - Q07 : filtre depuis le début de page ;
  - Q08 : départ = début − 120c ;
  - Q09 : cohérence en c < pas ;
  - Q11 : start de Bitstamp compté depuis le début de page.
- Premier essai (gardé sous `avant-q1/`) :
  - M03 était INVALIDE : sa chaîne avait changé ; corrigé.
  - Q07 a survécu : le cas « contradiction au chevauchement de début » a été ajouté au test des doublons, et Q07 est
    tué depuis.
  - Q10 (start en ms de Bitfinex) est retiré : il est équivalent, puisque c = 0 chez Bitfinex.

**Matrice et gates** (`travail/lourd-q1.log`, PID 4829, de 15:59Z à 16:07Z, sur t2 = archive 0cfbe3e + DT2-a à d) :
- Matrice python 3.10 à 3.13 en `-X dev -W error` : t2 Ran 69, s1 Ran 66, s2 Ran 67, s3 Ran 68. Les 16 exécutions
  sortent en code 0, sans « Exception ignored » ni « Warning ».
- Batterie : calib Ran 69 (plancher exact), runner 136 ok, s2bis Ran 341, S2 Ran 415.
- xtask : lignes VERDICT identiques à celles de la tête ; la 9e est ROUGE, déjà connue sur copie.

**Fin de passe :**
- Sondes à 15:30Z et 16:08Z : réseau coupé.
- `ps` vide.
- Dépôt réel non touché ; tête 0cfbe3e.
- Copies s1 à s3, t2 et target supprimées.
- Q-DT2-1 est fermée par cette passe. Q-DT2-2 à Q-DT2-6 sont adoptées par l'ajout daté de la DECISION.

## 10. Ajout daté du 2026-10-09, 17:20Z (`date -u`) : passe de correction de la G2 (DECISION.md, ajout 16:36:32 UTC)

Pièces lues : `g2/RAPPORT-G2.md` (C-1 à C-6, mutants N01 à N07), `g2/outils/propriete.py` (en lecture), ajout daté de
la DECISION (C-7). Versions d'avant la passe : `travail/avant-g2/` (diffs, rapport, SHA256SUMS, NOTES, w, outils).

**Corrections** (tests d'abord, rouge par AssertionError, 0 ERROR) :
- C-1 (DT2-c) : garde des mois acquis. `socle.rangs_mois` et `socle.debut_mois` sont partagés par l'acquisition et le
  chargement ; en mode `voisins`, une minute hors fenêtre n'est écartée que dans [début du premier mois − 14 h ; début
  du mois après le dernier + 14 h), sinon `CA/format : temps hors fenêtre ou hors minute`. Test : bornes 1777543200 et
  1785592740 admises, 1777543140, 1785592800, 2025-01-01 et un mensuel en microsecondes refusés (date -u -d).
- C-2 (DT2-c) : `REFUS CA/acquisition : mensuel 2026-10 non obtenu (téléchargement impossible (HTTPError)) ; un mensuel
  n'est publié qu'après la fin de son mois ; actif ETH ; place okx`, code 4 ; ligne au README.
- C-3 (DT2-c) : `voisins` = 0 hors des accès mensuels (cas `kraken voisins=1`).
- C-4, C-5 (DT2-e) : cas `chevauchement=-1` ; temps non rond W0 + 390 s hors de la page 0 (refus).
- C-6 : répétition refaite sur l'état final (0cfbe3e + DT2-a à e) : code 0, 98,4 s, 874 136 Kio, 440 pages de
  Coinbase d'ETH, Bitstamp 131040/131040, fragment ba896088… inchangé.
- C-7 (DT2-e) : refus `CA/format : réponse plafonnée ancrée avant le départ : fin de page tronquée` quand une page
  porte exactement `pas` bougies, dont une avant le départ, **et aucune à la dernière minute propre de la page ou
  après** (voir Q-DT2-7). Simulateur : variante « tronquee » (plafond ancré `pas` minutes avant start) : refus, là où le
  code d'avant perdait la fin de page en silence (rouge : `([1775001600, 1775001660, …], …)`). Variante « fin exclue,
  avant » de Coinbase : refus aussi (dernière minute propre sans échange : indiscernable d'une troncature).

**Diffs** (même noms ; DT2-e neuf ; série sur 0cfbe3e, égale à `w`) :

| diff | ajoutées / retirées | plancher | sha256 |
|---|---|---|---|
| DT2-a | +199 / −60 (inchangé) | 66 | 4a07b3680ba34bd1efc11b0efa4343ff097282b4c62723752ee6b95ba895d673 |
| DT2-b | +107 / −6 (inchangé) | 67 | 1cddb96cb2233c4282e61f3b3411db0db5750c6a920487c5a85e8b713f93a05f |
| DT2-c | +170 / −46 | 69 | f3d6733ef57c547ff3860ba9e37401f7f8246c7543d158ea8db42cfcb1247386 |
| DT2-d | +94 / −13 | 70 | ae440f30b7f64ef619b954768cccdaca7501248538af92a465fed4c03429c7e4 |
| DT2-e | +37 / −16 | 70 | 926012315138db01d1fd173beed3556a771201df58eb7c21891255c8b652090f |

0 octet 92, lignes ≤ 120, aucun TODO. SHA256SUMS du lot final : 9b9e3984ae4ac41969a68312904cfc3b58cdd95ad52a43e21aa77bdfbcb3efd7.

**Rouges** : C-1 et C-2 sur le code d'avant la passe, 5 FAIL (`rouge-g2-c1c2.out`) ; C-3, C-7, 3 FAIL
(`rouge-g2-c3c4c5c7.out` ; C-4 et C-5 verts sur le code, tests de mutants N01 et N07) ; par diff : DT2-c sur l'état
précédent 10 FAIL, DT2-e 4 FAIL (`rouge-g2-c.out`, `rouge-g2-e.out`).

**Mutants** (`mutants-g2c.{tsv,log}`, PID 3029, 16:48:44Z à 17:03:40Z ; plancher 70, borne 300 s, killpg, PAR 2) :
67 lancés, 64 TUÉS, M00 témoin vivant, 0 FATAL, 0 INVALIDE ; N01 et N07 de la G2 TUÉS (N04 recalé : année du début
pour le dernier mois, dans `socle.rangs_mois`) ; G01 à G16 pour C-1, C-2, C-3, C-7. G12 (compte de `pas` ignoré) a
survécu : cas ajouté (page sous le plafond, une bougie avant le départ, admise), rejeu 17:04:55Z : TUÉ
(`mutants-g2c-rejeu.tsv`). G15 (départ comparé au début de page) VIVANT, **équivalent** : les deux ne diffèrent qu'en
première page, où une réponse de `pas` bougies sans bougie avant le départ a forcément une bougie à la dernière minute
propre ou après (la requête n'en compte que `pas` − 1 avant elle) ; le critère ne peut donc pas changer. G14 (lettre de
C-7, sans la condition de fin) est TUÉ par Bitstamp « fin exclue » : voir Q-DT2-7.

**Matrice et gates** (`lourd-g2c.log`, PID 25216, 17:06Z à 17:19Z, sur 0cfbe3e + DT2-a à e) : python 3.10 à 3.13 en
`-X dev -W error`, t3 Ran 70 et états intermédiaires 66, 67, 69, 70 : 20/20 code 0, 0 « Exception ignored », 0
« Warning » ; calib Ran 70 (plancher exact), runner 136 ok, s2bis Ran 341, S2 Ran 415 ; xtask identique à la tête.

**Question Q-DT2-7 (C-7, mon choix et sa raison).** À la lettre (« exactement `pas` bougies dont au moins une précède
le départ »), C-7 refuserait toute page de Bitstamp sous la lecture « `end` exclu, `limit` compté depuis `end` » : la
réponse complète y porte toujours `pas` bougies dont la première précède le départ (mutant G14, tué par ce cas). Cela
contredirait le point 1 (correct sous les deux lectures). J'ai ajouté une condition : aucune bougie à la dernière
minute propre de la page (fin − 60) ou après. Une réponse plafonnée qui atteint cette minute couvre toute la page
(listes contiguës) ; une réponse qui ne l'atteint pas est refusée, troncature ou non. Conséquence à noter (item
PAROXYSME) : sous la lecture Coinbase « les 300 plus récentes jusqu'à `end` » avec `end` exclu, une page dont la
dernière minute propre n'a pas d'échange et qui a au moins une minute sans échange ailleurs est refusée : sur une paire
peu liquide (USDT-USD), l'acquisition peut échouer fermé ; seul un essai réel autorisé lèverait l'ambiguïté.

Fin de passe : sonde 17:19Z coupée ; `ps` filtré sur le dossier vide ; dépôt réel non touché (tête 0cfbe3e) ; copies
s1 à s4, t3, rep et target supprimées.

## 11. Ajout daté du 2026-10-09, 18:10Z (`date -u`) : passe C-8 (DECISION.md, ajout 17:21:10 UTC ; Q-DT2-7 adoptée)

**C-8, dans un diff neuf DT2-f** (DT2-a à DT2-e inchangés, mêmes sha256 qu'au §10) :
- `acquerir.pages` : après chaque page (et à la reprise, sur le fichier déjà acquis), `bougies.suspecte` (critère de
  C-7 adopté : au moins `pas` bougies, une avant le départ, aucune à la dernière minute propre) ; page suspecte
  redemandée en deux demi-pages au même débit (`requete`, même `Debit`), fichiers `page-<début>.1.json` et `.2.json`.
- `socle.demis` : cœurs [départ ; m] et [m + 60 ; borne] (m au milieu des n points de la page), élargis de c minutes de
  chaque côté (couverture sous toute inclusion des bornes) ; chaque demi doit atteindre m, la seconde fin − 60.
- `bougies.charger` : demi-pages présentes (les deux, sinon refus du découpage) : la page suspecte n'est plus contrôlée,
  chaque demi est filtrée à sa propre fenêtre ∩ celle de la page ; une demi-réponse elle-même plafonnée et tronquée :
  `REFUS CA/format : demi-page redemandée plafonnée et tronquée` ; page suspecte sans demi-pages : refus C-7 inchangé.
- Complétude : `pages redemandées k` par place paginée et par fenêtre.

**Tests** (serveur local ; `tests/test_demi_pages.py`, 2 tests ; plancher 70 → 72) : plafond ancré 4 minutes avant
start, pas 15 (pages et demi-pages à la main, `date -u -d`) : pages tronquées puis demi-pages, série égale à la vérité,
6 requêtes, aucune à la reprise, même débit (5 attentes de 0,34 s) ; minutes 11 et 12 sans échange : absentes, page
admise, complétude 24/26 et « pages redemandées 2 » ; demi-réponses tronquées (plafond ancré 15 minutes, ou la seule
seconde demi ancrée 10 minutes) : refus nommé ; demi-page effacée : refus du découpage ; deux effacées : refus C-7.
`test_formes_pages` : « fin exclue, avant » de Coinbase désormais admise (demi-pages de la page 0 de la fixture, de la
page 1192 du lot, à la main) ; « tronquee » : refus de la demi-page. `test_comptes` : « pages redemandées 0 ».
Rouge par AssertionError sur l'état d'avant DT2-f : 9 FAIL, 0 ERROR (`rouge-c8-f.out`).

**Diff** : DT2-f +183 / −36, 0 octet 92, lignes ≤ 120, aucun TODO, sha256
6b25dcccfc89d99c5754179db110166130c334ebcd0addf862c378a6ef66b69b ; plancher 72 ; SHA256SUMS du lot final
a37d6b844883de1a764461ce066939b9362d3fe92360a031506381cf29a00262.

**Mutants** (`mutants-c8.{tsv,log}`, PID 16818, 17:31:59Z à 17:50:17Z, plancher 72, borne 300 s, killpg, PAR 2) : 80
lancés (M, Q, N, G rejoués et recalés ; H01 à H13 neufs pour C-8) : 76 TUÉS, M00 témoin vivant, M07 et M27 INVALIDES
(chaînes changées), H13 VIVANT (seconde demi contrôlée jusqu'à m seulement). Cas ajouté (seconde demi seule tronquée)
et chaînes recalées ; rejeu 17:51:27Z : M07, M27, H13, H03, H11 TUÉS, M00 vivant (`mutants-c8-rejeu.tsv`). G15 a été
redéfini (plafond strict) et est tué ; l'ancien G15 équivalent n'existe plus.

**Matrice et gates** (`lourd-c8.log`, PID 9863, 17:53Z à 18:07Z, sur 0cfbe3e + DT2-a à f) : python 3.10 à 3.13 en
`-X dev -W error`, état final Ran 72 et états intermédiaires 66, 67, 69, 70, 70 : 24/24 code 0, aucun « Exception
ignored » ni « Warning » ; calib Ran 72 (plancher exact), runner 136 ok, s2bis Ran 341, S2 Ran 415 ; xtask identique à
la tête. Répétition à l'échelle : code 0, 84,3 s, 874 976 Kio, 440 pages, aucune redemandée, fragment ba896088…
inchangé.

**Écart de base (tête mobile).** Pendant la passe, la tête est passée de 0cfbe3e à 6f8bfd8 (DETTES-T3 : job
`controle-unittest` inséré après le job calib dans `gates.yml`, runner à 137 cas). Les diffs de `diffs-tete/` (base
0cfbe3e) n'y s'appliquent plus pour `gates.yml` (leur hunk du plancher était en fin de fichier). Jeu régénéré pour la
tête du moment : `diffs-tete-6f8bfd806eab183ef956e6ea2964473b16a512e4/` (seul `gates.yml` diffère ; DT2-e identique) : application en série propre,
lot égal à `w`, runner 137 ok, calib Ran 72 conforme. Sha256 : a bd86f83e…, b 2dbc193d…, c 105f7b2f…, d 0f385daa…,
e 92601231…, f 96ab3140….

**Limite rendue (PAROXYSME, sans item, pour décision)** : sous la lecture Coinbase « les 300 plus récentes jusqu'à
`end` », une demi-page est elle aussi plafonnée ; elle n'est refusée que si elle n'atteint pas sa minute (m, ou fin − 60
pour la seconde), soit deux minutes sans échange à des places précises ; la redemande réduit le cas résiduel, elle ne
l'annule pas sous cette lecture.

Fin de passe : sondes 17:24Z et 18:09Z coupées ; `ps` filtré sur le dossier vide ; dépôt réel non touché ; copies
s1 à s5, t4, tH, rep et target supprimées.

## 12. Ajout daté du 2026-10-09, 19:46Z (`date -u`) : passe C-9 à C-12 (DECISION.md, ajout 18:36:29 UTC ; RAPPORT-CC)

**Base.** Tête lue au début et à la fin : 6356a945c4faf667b9b4a432cd6cb9b2200432a6 (fusion de 963eba9, même arbre
7bb7ac53…). Anciennes versions sous `travail/avant-c9/`. Diffs : `diffs-tete-6356a945c4faf667b9b4a432cd6cb9b2200432a6/`.

**Ce qui change.**
- C-9 (`socle.pages`) : une page demande au plus ⌊pas/2⌋ créneaux, chevauchement compris ; minutes utiles
  u = ⌊pas/2⌋ − 2c (Coinbase 148, Bitstamp 498, Bitfinex 5000).
- C-9 (`bougies.serie`) : refus nommé `réponse de plus de bougies que de créneaux demandés`. Les bougies se comptent à
  partir du départ (Q-DT2-8 ci-dessous).
- C-7 et C-8 gardés. Une réponse suspecte n'est refusée que sur preuve : une bougie d'un fichier du lot dans
  ]dernière bougie ; dernière minute propre]. Sans cette règle, la lecture `recentes` est refusée sur des données
  complètes (rouge `rouge-c9-preuve.out`).
- C-10 : bloc « formes » du README récrit.
- C-11 : `test_reprise_page_suspecte` (X03 tué).
- C-12 (`socle.lire`) : 0 ≤ 2c < ⌊pas/2⌋ (pages), et demi-requête (⌈k/2⌉ + 2c créneaux) sous `pas`.

**Diffs** (0 octet 92, lignes ≤ 120, aucun TODO/FIXME ; DT2-a à f inchangés depuis la régénération pour 6356a94) :

| Diff | + / − | sha256 |
|---|---|---|
| a | 199 / 60 | 15cf93cb… |
| b | 107 / 6 | a3b713a3… |
| c | 170 / 46 | 85928390… |
| d | 94 / 13 | 00371e8f… |
| e | 37 / 16 | 92601231… |
| f | 183 / 36 | 419afa57… |
| g (C-9 à C-12) | 165 / 97 | 1aedd6c1441cde0207e5fe6d3b8f896db56583491b475dc8fa670276ca92b2e2 |

Plancher 74. SHA256SUMS du lot : 1ce0dea0f1a1b32d0e5dde90518aa2874eb88fb94c290f5733baca9b212cfad5.

**Preuve de C-9.** Outil `outils/propriete_c9.py` : copie de `g2/cc/outils/propriete_cc.py`, plus deux ajouts.
- Ajouts : u et c recalculés selon C-9 ; mode neuf `crenp-g`, le plafond compté en créneaux ancré g minutes avant
  start (bougies échangées de [s − g ; min(e, s − g + pas − 1)]).
- Tirages : graines 7, 11 et 12, 13 200 cas. Classement par prémisse : g ≤ pas − ⌊pas/2⌋ (`propriete-c9f-*.out`,
  bilan `propriete-c9f-bilan.out`).
- Dans la prémisse : `exact`, `recentes`, `cpt` et `crenp` sont JUSTE (redemandées comprises), 0 PERTE, 0 REFUS.
- Au-delà de la prémisse (plafond ancré plus d'une demi-page avant start) :
  - `cpt` : JUSTE ou REFUS, sauf 13 PERTE, toutes avec c = 0 ;
  - `crenp` : PERTE (919 cas) et REFUS.
- `cren` du contre-contrôle : fenêtre décalée [s − g ; e − g], quelle que soit la taille de la requête. PERTE dans
  toutes les plages. Ce mode n'est pas un plafond, donc C-9 ne l'atteint pas (L-C9-1 ci-dessous).
- Échelle du lot (`lot-c9.out`, Coinbase pas 300, c 1, 444 minutes) : `exact`, `recentes`, `cpt` jusqu'à g = 150 et
  `crenp` jusqu'à g = 150 sont JUSTE. Au-delà de 150 : `cpt` JUSTE ou REFUS, `crenp` avec des PERTE ; `cren` g = 1 ou 2
  : PERTE.

**Rouges** (AssertionError seulement) :
- `rouge-c9-g.out` : 35 FAIL, 0 ERROR (tests de w sur avant-c9) ;
- `rouge-c9-preuve.out` : 1 FAIL (`test_recentes_sans_preuve`) ;
- `rouge-c9-socle.out` : 1 FAIL (`test_parametres_coherence`).

**Mutants** (borne 300 s, killpg, PAR 2, plancher 74).
- Campagne `mutants-c9.{tsv,log}`, PID 24156, 18:57:16Z à 19:19:21Z : 91 lancés (M, Q, N, G, H rejoués ; I01 à I11
  et X03 neufs ; pas de I08). Résultat : 87 TUÉS, 4 VIVANTS, 0 FATAL, 0 INVALIDE.
- Deux vivants corrigés par des cas neufs :
  - I07 (preuve sans la dernière minute) : page 13 exacte, la minute 12 seule prouve la troncature de la page 0 ;
  - I11 (k = pas) : `pas` 1, aucun créneau.
- Rejeu `mutants-c9-rejeu.{tsv,log}`, PID 31655, 19:23:36Z à 19:26:42Z : 10 TUÉS, dont I07 et I11. M00 (témoin) et
  I10 restent vivants.
- I10 est équivalent. Pour une place paginée, 2c < k = ⌊pas/2⌋ donne ⌈k/2⌉ + 2c ≤ 2k − 1 < pas. Pour une autre
  place, k = 1 et c = 0, d'où 1 < max(pas, 2). La garde des demi-requêtes, exigée par C-12, est donc impliquée.

**Matrice et gates** (`lourd-c9.log`, 19:27:26Z à 19:44:58Z, tête + DT2-a à g).
- PID : j'ai consigné 6324, celui du `setsid`. Le processus réel est 6325, sondé jusqu'à sa fin.
- Matrice python 3.10 à 3.13 en `-X dev -W error` : 28/28 code 0 (Ran 66, 67, 69, 70, 70, 72, 74), aucun « Exception
  ignored » ni « Warning ». Lot appliqué = w.
- Gates sur la copie : calib Ran 74 (plancher exact), runner 137 ok, s2bis Ran 341, controle Ran 18, journaux-modele
  conforme, S2 Ran 415.
- Sur le clone : sim-bis Ran 279, calib Ran 74.
- xtask : lignes VERDICT identiques à la tête (9e ROUGE, connue).
- Répétition à l'échelle : code 0, 106 s. Durée de tau.py 83,7 s, 874 704 Kio. 886 pages Coinbase pour ETH (440
  avant C-9), 0 redemandée, fragment ba896088… inchangé. Coût calculé, non mesuré : au moins 886 × 0,34 s ≈ 5 min
  d'attente Coinbase par actif.

**Questions et limites (PAROXYSME, pour adjudication)**
- Q-DT2-8, mon choix : le refus C-9 compte les bougies à partir du départ. Raison : Coinbase écrit que des bougies
  peuvent précéder start. Les compter toutes refuserait la lecture `recentes`, documentée.
- Q-DT2-9, mon choix : la garde C-7/C-8 ne refuse que sur preuve. C'est un desserrement de C-7 sans preuve : il évite
  les refus sur données complètes demandés par la preuve de C-9 (L-2 fermée).
  - Avec le refus sans preuve (`propriete-c9-g{7,11,12}.out`, mêmes 13 200 cas), j'ai recompté 486 REFUS sous
    `recentes` (216, plus 270 avec c = 0), tous « demi-page redemandée plafonnée et tronquée ».
  - Une variante (« réponse entièrement avant le départ : refus ») a été essayée : elle supprimait les 13 PERTE
    au-delà de la prémisse et rendait des refus sous `recentes`. Je n'ai pas gardé sa sortie, donc je n'en cite pas
    de chiffre (écart E-C9-1). Rejetée.
- L-C9-1 : décalage inconditionnel (`cren` du contre-contrôle) : pertes silencieuses, que C-9 ne ferme pas. L-1 n'est
  fermée que pour un plafond, compté en bougies ou en créneaux. Écrit au README ; item proposé :
  SHOGEN-CALIB-FORMES-API-CRENEAUX-1.
- L-C9-2 : plafond ancré plus de pas − ⌊pas/2⌋ minutes avant start, hors de la prémisse de C-9.
  - Avec c ≥ 1 : REFUS ou JUSTE.
  - Avec c = 0 : 13 pertes sur ce sous-ensemble. Pour Bitfinex, le [lu] (MTS ≥ start) exclut ce cas.
  - Écrit au README.
- L-C9-3 (vu en relisant `socle.demis`, non testé) : une page d'un seul point avec c = 0 (dernière page d'une
  fenêtre) donne, si elle est suspecte, une seconde demi-requête vide (start > end). Atteignable seulement au-delà de
  la prémisse : il faut au moins `pas` bougies avant le départ. Item à former ou à admettre.

Écart E-C9-1 : la sortie de la variante essayée sur la garde n'a pas été gardée ; son chiffre est retiré du rapport.

Fin de passe :
- sonde de 19:45:26Z coupée ;
- `ps` filtré sur le dossier vide ;
- dépôt réel non touché : tête 6356a94, `status` vide ;
- copies A, C, tete-H, rep, tH, target, ws/tete et ws/w supprimées.

## 13. Ajout daté du 2026-10-09, 22:01Z (`date -u`) : passe C-13 et C-14 (DECISION.md, ajouts 19:48:33 et 19:51:45 UTC)

**Base.** Tête lue au début (6356a94), puis relue pendant la passe : 50ca52d (DETTES-T4, `gates.yml`), b837efe (docs),
c1122de (DETTES-T5 DT5-0, `gates.yml`). Tête finale : c1122de73ec0e07812fef30d41ddb4269a76a1c8, relue à 22:00:53Z.
`scripts/calib-actifs` et `s2bis` sont inchangés sur ces têtes ; seul le contexte de `gates.yml` change. Diffs pour
la tête finale : `diffs-tete-c1122de73ec0e07812fef30d41ddb4269a76a1c8/`. Jeu pour 6356a94, même contenu hors
`gates.yml` : `diffs-tete-6356a945c4faf667b9b4a432cd6cb9b2200432a6/` (a à g inchangés). Anciennes versions :
`travail/avant-c13/`.

**C-13 (couverture double), DT2-h** (+200 / −53) :
- paramètre `couverture` (2 pour Coinbase et Bitstamp, 1 ailleurs) ;
- cohérence : 1 ou 2 ; 2 seulement pour une place paginée d'au moins 2 minutes utiles ;
- `socle.doubles` : second découpage décalé d'une demi-page h = ⌊minutes utiles / 2⌋ (74 et 249 minutes), de
  début − h à fin + h au moins, pages non coupées à la fenêtre ;
- `acquerir.pages` : `double-<début>.json` après les pages, au même débit, avec C-8 ;
- `bougies` : plan de chargement à deux découpages et contrôle de chaque réponse sans modèle du plafond ;
- `tau.completude` : « seconde couverture n pages » ;
- tests : `test_couverture`, `test_formes` et `test_socle`.

Règle du contrôle : une bougie servie par n'importe quel fichier, prise dans [min(première bougie de la réponse,
début de sa page) ; dernière minute de sa page] et absente de la réponse, donne `REFUS CA/format : couverture double
discordante`. Une page du premier découpage suspecte au sens de C-7 garde « fin de page tronquée » ; une demi-page
garde son motif. Des valeurs différentes avec un fichier du second découpage donnent le même refus.

Le contrôle généralise la règle de preuve de Q-DT2-9 à toutes les réponses. Il ne refuse jamais sous `exact` ni sous
`recentes`. Sous `exact`, une réponse non vide commence au plus tôt au départ. Sous `recentes`, la réponse est la
suite des `pas` dernières bougies jusqu'à `end` ; elle contient donc toute bougie connue entre sa première et la
dernière minute propre.

**C-14 et réglage des vraies places, DT2-i** (+93 / −63) :
- `socle.demis` rend [] pour une page d'un seul point : aucune demi-requête vide ;
- vraies places en couverture 2 ;
- recalage par le second découpage à la main : `test_pages`, `test_series`, `test_comptes`, `test_formes_pages` et
  synthétiques ;
- `test_demi_pages` en couverture simple (C-8 seul) ;
- README.

L'état intermédiaire après DT2-h (`outils/mk_s8.sh`) a la couverture 1 partout ; sa suite est verte.

**README** : bloc des formes récrit.
- Fermé : la couverture double et son contrôle, la garde C-7/C-8/C-14.
- Restant : la limite L-C13-1 ci-dessous.
- OKX : l'alignement UTC+8 est écrit comme établi, avec la référence de l'ajout 19:51:45 UTC ; `voisins` inchangé.

**Totaux** : 0 octet 92, lignes ≤ 120, aucun TODO/FIXME, plancher 76. SHA256SUMS du lot :
aedc2ba81b14f4e263316581d76979e9efb56ba7cfb69abbcca81adf4d6d9f6a.

| Diff (tête c1122de) | + / − | sha256 |
|---|---|---|
| a | 199 / 60 | 3db9fb4a… |
| b | 107 / 6 | 40bc2295… |
| c | 170 / 46 | d1068e44… |
| d | 94 / 13 | c110a602… |
| e | 37 / 16 | 92601231… |
| f | 183 / 36 | 17b3de50… |
| g | 165 / 97 | 66f5b5ca… |
| h (C-13) | 200 / 53 | e2d8d925135a18dc871097497996347d2c23ce7f55cbcc04a02381be0ed06a09 |
| i (C-14, places, recalages) | 93 / 63 | da04fc2259895e4e7b59be821abcb6992fb1c3bb4cc6a8f83f83f5c106276315 |

**Preuve** (`outils/propriete_c13.py`, copie étendue de `propriete_c9.py`, toujours en boîte noire).
- Ce qui change dans l'outil :
  - couverture 2 ;
  - g ∈ {1, 2, 4, 9, 30, 100, 1000} ou variable par requête jusqu'à 1000 minutes, pour `cpt`, `cren` et `crenp` ;
  - historique du marché commencé avant s − g de toute requête ;
  - modes « hist » : historique commencé à −3 pas − 40, donc plafond ancré avant le début de l'historique ;
  - minutes sans échange : au hasard, plus les bords des deux découpages.
- Tirage : graines 7, 11 et 12, 20 000 cas chacune, soit 60 000 cas (`propriete-c13-g*.out`, bilan
  `propriete-c13-bilan.out`, PID 24194, de 20:06Z à 20:18Z). Comptes recomptés par script ; « dont redemandées » est
  compris dans JUSTE :

| Mode | JUSTE | REFUS | PERTE |
|---|---|---|---|
| exact | 2 145 | 0 | 0 |
| recentes | 2 145 (dont 1 677 redemandées) | 0 | 0 |
| cpt, dans la prémisse de C-9 | 5 913 | 0 | 0 |
| cpt, au-delà | 1 745 | 9 496 | 0 |
| crenp, dans la prémisse | 5 951 | 0 | 0 |
| crenp, au-delà | 687 | 10 496 | 2 |
| cren (décalage), g ≤ pas − ⌊pas/2⌋ | 1 092 | 4 810 | 10 |
| cren, au-delà | 13 | 11 191 | 20 |
| cpt hist | 141 | 0 | 2 001 |
| crenp hist | 125 | 0 | 2 017 |

- Refus sur données complètes :
  - 0 sous `exact`, sous `recentes`, et sous `cpt` et `crenp` dans la prémisse ;
  - les autres refus ont tous lieu dans des modes où une réponse manque réellement d'une bougie servie ailleurs. La
    règle ne refuse que sur une bougie servie et absente d'une réponse qui la couvre.
- Pertes hors « hist » : 32. Les 28 exemples imprimés ont tous une fenêtre de 1 à 10 minutes. La minute perdue est
  la dernière échangée de la fenêtre, après la dernière bougie que toute réponse décalée atteint. Les
  bandes de fin de page qui auraient montré le décalage sont toutes sans échange. Voir L-C13-2.
- Échelle du lot (`lot-c13.out` : Coinbase pas 300, c 1, couverture 2, 444 minutes ; minutes sans échange : aucune,
  ciblées, 5 % ou bande muette de 145 minutes) : aucune PERTE.
  - JUSTE : `exact` ; `recentes` ; `cpt` et `crenp` jusqu'à g = 151 ; `cren` 1 dans 10 cas sur 16.
  - REFUS : `cpt` et `crenp` à g = 300 et 1000 ; `cren` 2 (14 cas sur 16), et `cren` 74, 75, 150 et 1000.

**Rouges** (AssertionError seulement) :
- `rouge-c13.out` : `test_couverture` sur le code d'avant, 6 FAIL. Dont la perte silencieuse de la minute 39 sous
  décalage de 2 minutes.
- `rouge-c13-final.out` : `test_couverture`, `test_formes` et `test_socle` sur avant-c13, 8 FAIL, 0 ERROR.

**Mutants** (borne 300 s, killpg, PAR 2, plancher 76).
- Campagne `mutants-c13.{tsv,log}`, PID 8829, de 20:19:47Z à 20:50:21Z : 106 lancés (tous rejoués ; J01 à J13, J15
  et J17 neufs). Résultat : 97 TUÉS, 5 VIVANTS, 0 FATAL, 4 INVALIDES.
  - INVALIDES (chaînes changées) : M02, M07, H02, H10.
  - VIVANTS : M00 (témoin), M32, Q09, I10, J10.
- Corrections :
  - chaînes recalées et J16 ajouté ;
  - cas Bitfinex à chevauchement 2500 (2c = k en couverture simple) : M32 et Q09 étaient masqués par la garde C-13
    de Coinbase et de Bitstamp.
- Rejeux :
  - `mutants-c13-rejeu` : 7 TUÉS ;
  - `-rejeu2`, après que les cas C-13 de `test_socle` ne dépendent plus du paramètre réel : 10 TUÉS ;
  - `-rejeu3`, après le resserrement final : 13 TUÉS.
- Restent vivants : M00 (témoin), I10 (équivalent, §12) et J10. J10 est équivalent : hors pages, k = 1, donc
  k − 2c ≥ 2 est faux et la clause « pages » est impliquée.

**Matrice et gates** (`lourd-c13-final.log`, PID 30924, de 21:37:42Z à 22:00:33Z, tête c1122de + DT2-a à i).
- Matrice python 3.10 à 3.13 en `-X dev -W error` : 36/36 code 0 (Ran 66, 67, 69, 70, 70, 72, 74, 76, 76), aucun
  « Exception ignored » ni « Warning ». Lot appliqué = w.
- Gates sur la copie :

| Suite | Résultat |
|---|---|
| calib | Ran 76, plancher exact |
| runner | 137 ok |
| s2bis | Ran 341 |
| controle | Ran 26 (plancher de la tête) |
| journaux-modele | conforme |
| docs-sha256sums | conforme : 34 SHA256SUMS, 295 lignes |
| S2 | Ran 415 |
| sim-bis (sur clone) | Ran 279 |
| calib (sur clone) | Ran 76 |

- xtask : lignes VERDICT identiques à celles de la tête (9e ROUGE, connue).
- Le run complet sur 50ca52d (PID 26714) était aussi vert ; il est caduc (retouches de tests, tête mobile).

**Échelle.**
- Mesuré (répétition) : code 0 en 140 s ; tau.py 96,2 s et 873 376 Kio. Fichiers Coinbase d'ETH : 1 773 (886 + 887).
  Bruts : 144,7 Mo (102,2 Mo avant). Fragment ba896088… inchangé. Ligne de complétude : « seconde couverture 265
  pages » pour Bitstamp.
- Calculé par `socle` sur les paramètres réels (non mesuré) :
  - Coinbase : 4 716 requêtes, contre 2 356 avant C-13, soit 1 603 s d'attente à 340 ms ;
  - Bitstamp : 2 112 requêtes, contre 1 053, soit 422 s à 200 ms ;
  - Bitfinex : 108 requêtes, 227 s ;
  - au moins 37,5 min de débit pour l'acquisition unique, contre 20,6 min avant C-13.

**Limites (PAROXYSME)**
- **L-C13-1, ouverte, écrite au README.** Cas : plafond ancré avant le début de l'historique de la paire. Toute requête
  reçoit alors les mêmes premières bougies de l'historique. Aucun plan de requêtes ne distingue ce monde d'un marché
  muet lu « les `pas` plus récentes » : pertes sans refus (« hist » : 4 018 cas). La complétude le montre (fenêtre
  vide ou presque). La seule règle qui la fermerait refuserait un silence réel d'une page entière sous `recentes`,
  c'est-à-dire des refus sur données complètes. Item proposé : SHOGEN-CALIB-FORMES-API-HISTORIQUE-1, ou une limite
  admise.
- **L-C13-2, résiduelle, mesurée et raisonnée.** Cas : décalage ou retard g plus grand que l'avance du second
  découpage au-delà de la fin (au moins h). Il faut en plus que toutes les bandes ]dernière bougie ; dernière minute]
  de toutes les pages des deux découpages soient sans échange.
  - Le décalage est vu dès qu'une seule de ces bandes porte un échange : toute minute antérieure à la dernière
    atteinte est servie par une requête plus tardive.
  - Le cas reste atteignable pour une fenêtre de quelques minutes (32 cas sur 60 000 ; les 28 exemples imprimés ont
    des fenêtres de 1 à 10 minutes).
  - Il ne l'est pas pour les fenêtres du lot (87 pages ou plus par découpage), sauf silence de plus d'une
    demi-page (74 minutes pour Coinbase, 249 pour Bitstamp) à chacune des fins de page. Sans item ; à adjuger.
- **Q-DT2-10.** La complétude dit « seconde couverture n pages », sans compte de discordances : toute discordance est
  un refus avant la complétude, donc le compte vaudrait toujours 0. À confirmer.

**Écarts**
- E-C13-1 : le PID consigné pour les lancements détachés était d'abord celui du `setsid` (24185, 6324…). Les PID réels
  (24194, 26714, 30924) sont consignés et ont été sondés.
- E-C13-2 : deux lancements, lourd-c13b et le premier lourd-c13 sur c1122de, arrêtés par killpg avant tout résultat
  (tête mobile, diffs absents). Ils ne comptent pas.
- E-C13-3 : une attente qui sondait par `pgrep -f` se reconnaissait elle-même ; arrêtée par la borne de 30 min, sans
  effet sur les résultats.

Fin de passe :
- sonde de 22:00:53Z coupée ;
- `ps` filtré sur le dossier vide ;
- dépôt réel non touché : tête c1122de, `status` vide ;
- copies A, C, tete-H, rep, tH, target, dbg et ws/s8 supprimées.

## 14. Ajout daté du 2026-10-10, 04:26Z (`date -u`) : passe C-15 (DECISION.md, ajout 22:03:39 UTC, sha256 e00ea36d…)

**Base.**
- Tête au début : 093a17435a40976722381cc4074adced5cddcf06 (02:12:48Z). DT2-a à i (jeu c1122de) s'y appliquent en
  série, à sec puis pour de bon, sans échec ; le lot obtenu est identique à w.
- La tête a avancé pendant la passe : 0e03a9f à 03:52Z, puis dda4bbc5… (dda4bbcc2b0f480eb0c39d7891237e0e3d2b0918) à
  04:25Z. Le commit 14597a6 (DETTES-T5 DT5-23) change trois fichiers du lot : `tests/__init__.py` (garde réseau),
  `tests/test_pages.py` (test de la garde) et `SHA256SUMS`.
- Rebase (`outils/rebase_tete.py`) : chaque état du lot est fusionné à trois voies par `git merge-file` (mien = état,
  base = 093a174, leur = nouvelle tête), sans conflit, et `SHA256SUMS` est recalculé. Les zones modifiées sont
  disjointes des miennes.
- Diffs neufs pour la tête finale : `diffs-tete-dda4bbcc2b0f480eb0c39d7891237e0e3d2b0918/` (identiques octet pour octet
  au jeu 0e03a9f). Entre 0e03a9f et dda4bbc, aucun changement sous `scripts/calib-actifs`, `s2bis`, `.github` ni
  `enforcement`.
- Ce qui change dans DT2-a à i : les lignes de `SHA256SUMS` du lot et le contexte de `test_pages.py`. Les comptes de
  lignes sont inchangés. Anciennes versions : `travail/avant-c15/` ; w d'avant le rebase : `travail/w-avant-rebase/`.

**C-15 : étudié, codé, et le cas est fermé dans la propriété**
- La sonde telle qu'écrite (« une requête ancrée au plus tôt ») ne rend rien en lecture exacte : la requête finit
  avant l'historique et revient vide. Il faut donc chercher la première bougie.
- **Recherche** (`socle.sonde`) :
  - sondes de ⌊pas/2⌋ créneaux ;
  - recul depuis fin − ⌊pas/2⌋ minutes, en haut − k (2^j − 1), borné à `historique.debut` (2009-01-03, avant toute
    cotation), jusqu'à une sonde non vide ;
  - puis dichotomie jusqu'au premier x non vide ;
  - T0 = première bougie de cette sonde ;
  - fichiers `sonde-<x>.json` (couverture double seulement), recherche rejouée au chargement : fichiers exactement
    ceux de la recherche, sinon refus nommé.
- **Refus CA/avant-historique** (`bougies._sonde`, `serie`) :
  - (a) une requête de la fenêtre part moins de pas − ⌊pas/2⌋ + 1 minutes après T0 (« fenêtre commencée moins d'une
    page après la première bougie servie ») ;
  - (c) une réponse de la fenêtre porte une bougie au plus tard en T0 (« réponse portant la première bougie de
    l'historique ») ;
  - (d) aucune bougie servie, et aucune sonde non vide (« aucune bougie servie »).
- **Choix de seuil** : pas − ⌊pas/2⌋ + 1 minutes à partir du départ le plus précoce, second découpage compris, plutôt
  qu'« une page » à partir du début de la fenêtre. C'est la plus petite marge qui garde (c) sans refus sous `cpt` et
  `crenp` dans la prémisse de C-9.
- **Première version écartée** (sans recul, avec (d) sans condition ; `travail/c15-v1/`) : elle refusait 20 fenêtres
  muettes en lecture exacte, soit des refus sur données complètes. D'où le recul et la règle (d) restreinte.

**Diffs** (tête dda4bbc ; 0 octet 92, lignes ≤ 120, aucun TODO/FIXME) :

| Diff | + / − | sha256 |
|---|---|---|
| a | 199 / 60 | 981a7b96… |
| b | 107 / 6 | 8abdc1db… |
| c | 170 / 46 | 5bf5aae3… |
| d | 94 / 13 | 39d399ad… |
| e | 37 / 16 | 699aeada… |
| f | 183 / 36 | c23f8a31… |
| g | 165 / 97 | da5bc50a… |
| h | 200 / 53 | 780252af… |
| i | 93 / 63 | d041a67a… |
| j (C-15, socle) | 35 / 8 | a9fa3607079ccc6e4bb7962f0058f1bf92f10517e86389971584220efee21649 |
| k (C-15, acquisition, chargement, tests, README) | 190 / 44 | 7ef18354142a57d5b992973143d68b68c5e3bc590e2433eb6442591507b53f49 |

- Contenu de j : paramètre `historique`, sa cohérence, `socle.sonde` (sans appelant dans cet état), cas de
  `test_socle`.
- Plancher : 76 jusqu'à j, 77 après k. SHA256SUMS du lot final : 3749accc….

**README** : sonde et refus CA/avant-historique écrits. L-C13-2 est écrite avec sa borne mesurée : 32 cas sur 60 000,
fenêtres de 1 à 10 minutes ; une fenêtre du lot le verrait dès un seul échange dans une fin de page.

**Preuve** (`outils/propriete_c15.py` : copie de `propriete_c13.py`, avec `historique.debut` 2000 minutes avant
l'historique du marché et les sondes servies par le même serveur).
- Tirage : graines 7, 11 et 12, 20 000 cas chacune (PID 28531, de 02:46Z à 03:03Z ; `propriete-c15-g*.out`, bilan
  `propriete-c15-bilan.out`, recompté par script).
- **Mode « hist »** (`cpt` et `crenp` ancrés 1000 minutes avant le début de l'historique) : 4 284 REFUS
  CA/avant-historique, **0 PERTE**, contre 4 018 PERTE en C-13.
  - `cpt-hist` : 2 142 refus « réponse portant la première bougie de l'historique » ;
  - `crenp-hist` : 2 142 refus « aucune bougie servie ».
- **Aucun refus CA/avant-historique** sous `exact` et `recentes`, ni sous `cpt`, `crenp` et `cren` dans la prémisse de
  C-9. Le nombre de JUSTE est identique à C-13 : 2 145, 2 145, 5 913, 5 951 et 1 092.
- **Au-delà de la prémisse** :
  - 2 031 refus CA/avant-historique (`cren` 1 000, `crenp` 1 031) ;
  - 12 cas JUSTE en C-13 sont devenus des refus (`cren` 13 → 11 JUSTE, `crenp` 687 → 677). Ce sont des retards variables
    par requête (g « var ») : la sonde, servie avec un autre retard que les pages, situe T0 plus tard que le vrai.
  - Les pertes L-C13-2 sont inchangées (`cren` 30, `crenp` 2).
- Critère de l'ajout (0 perte en « hist », aucun refus sur fenêtre postérieure à T0 + une page) : tenu en « hist » et
  dans tous les modes de la prémisse. Hors prémisse, il reste les 12 cas ci-dessus (L-C15-1).

**Rouges** (AssertionError seulement) :
- `rouge-c15.out` : `test_sonde` et `test_couverture` sur le code de C-13, 6 FAIL, 0 ERROR. Dont la perte silencieuse
  des 40 minutes de la fenêtre sous les deux plafonds ancrés avant l'historique.

**Mutants** (`mutants-c15.{tsv,log}`, PID 3167, de 03:05:46Z à 03:49:47Z, plancher 77, borne 300 s, killpg, PAR 2).
- 125 lancés (tous rejoués ; K01 à K18 neufs) : 120 TUÉS, 3 VIVANTS, 2 INVALIDES (G05, K04 : chaînes), 0 FATAL.
- VIVANTS : M00 (témoin), I10 et J10 (équivalents, §12 et §13).
- Rejeu `mutants-c15-rejeu` : G05 et K04 TUÉS.
- Échantillon sur l'arbre rebasé (`mutants-c15-rb`) : 7 TUÉS, M00 vivant.
- K01 à K18 sont tous tués : sonde omise, ignorée ou mal dimensionnée, refus (a), (c) et (d) retirés, seuil d'une
  page, strict ou sur le seul premier découpage, T0 pris au départ de la sonde, dichotomie inversée ou absente, recul
  linéaire, cohérence de `historique`.

**Matrice et gates** (`lourd-c15.log`, PID 9138, de 03:57:13Z à 04:25:02Z, tête 0e03a9f + DT2-a à k ; même contenu
que dda4bbc pour ces chemins).
- Matrice python 3.10 à 3.13 en `-X dev -W error` : 44/44 code 0 (Ran 66, 67, 69, 70, 70, 72, 74, 76, 76, 76, 77),
  aucun « Exception ignored » ni « Warning ». Lot appliqué = w.
- Gates sur la copie :

| Suite | Résultat |
|---|---|
| calib | Ran 77, plancher exact |
| runner | 137 ok |
| s2bis | Ran 342 |
| controle | Ran 37 |
| journaux-modele | conforme |
| docs-sha256sums | conforme : 38 SHA256SUMS |
| S2 | Ran 419 |
| sim-bis (sur clone) | Ran 279 |
| calib (sur clone) | Ran 77 |

- I-1 : `cargo --locked --offline xtask verify` avec la cible cargo par défaut de chaque copie, sans
  CARGO_TARGET_DIR (`outils/xtask-defaut.sh`). Cible dans `travail/A/target` et dans `travail/tete-<sha>/target`.
  Lignes VERDICT identiques à la tête (9e ROUGE, connue). `df -h /` avant chaque build : 6,7 à 8,2 Go libres.

**Échelle.**
- Mesuré (répétition) : code 0 en 106 s ; tau.py 70,9 s et 868 240 Kio. Fichiers Coinbase d'ETH : 1 797, dont 24
  sondes. Fragment ba896088… inchangé.
- Calculé, non mesuré : environ 25 sondes par paire et par fenêtre sur les vraies fenêtres (recul nul, puis 24 pas
  de dichotomie depuis 2009), soit environ 250 requêtes en plus. Attente : environ 34 s pour Coinbase et 30 s pour
  Bitstamp.

**Limites et écarts**
- **L-C15-1** : sous un retard variable d'une requête à l'autre et au-delà de la prémisse de C-9, la sonde peut situer
  T0 trop tard ; 12 refus sur 60 000 cas, jamais une perte. C'est un refus nommé, non une dette de perte. Item proposé
  si l'orchestrateur le veut : SHOGEN-CALIB-FORMES-API-HISTORIQUE-1, déclencheur : un refus CA/avant-historique à la
  première acquisition réelle.
- **E-C15-1** : la tête a avancé deux fois pendant la passe. Rebase par fusion à trois voies, sans conflit.
  - Propriété et campagne de mutants : jouées sur l'arbre d'avant le rebase, dont le code (`acquerir`, `bougies`,
    `socle`) est identique ; le rebase ne touche que la garde réseau des tests.
  - Échantillon de mutants rejoué sur l'arbre rebasé. Matrice et gates : sur la tête rebasée.
- **E-C15-2** : j'ai lu cinq lignes de la sortie brute de xtask, dont mon outil dit qu'elle n'est « jamais lue ». Ce
  sont des citations de `docs/DECISIONS.md` et de `docs/adr-0028`, hors des chemins interdits.

Fin de passe :
- sonde de 04:25:44Z coupée ;
- `ps` filtré sur le dossier vide ;
- dépôt réel non touché : tête dda4bbc, `status` vide ;
- copies A, C, tete-H, rep, tH, target et les deux archives de base supprimées.

## 15. Ajout daté du 2026-10-10, 06:59Z (`date -u`) : R-1 à R-5 du contre-contrôle cc2 et Q-DT2-11 (DECISION.md, ajout 06:25:41 UTC, sha256 aaab0211…)

**Base.**
- Tête au début : e5bf085 (06:26:02Z). Entre dda4bbc et e5bf085, aucun changement sur `scripts/calib-actifs`,
  `gates.yml`, `s2bis`, `enforcement` ni `scripts/controle` (`git diff --stat` limité à ces chemins). La série complète
  le dossier `diffs-tete-dda4bbcc…/`.
- Tête relue à 06:57Z : 01d74bd (DETTES-T6). Seule la ligne s2bis de `gates.yml` change (plancher 342 → 344). DT2-a
  à p s'y appliquent sans décalage ni flou (`patch -F0`), et le lot obtenu est égal à l'état final. Dossier
  `diffs-tete-01d74bdab065411f3ccf61d9e4b1147ab391954e/` : copies octet pour octet de la série (`cmp`).
- À 06:58Z, l'index du dépôt réel porte une modification de `gates.yml` posée par un autre acteur (s2bis 344 → 345,
  fichier écrit à 06:56Z). Je n'ai fait aucune écriture git ; ma série ne touche pas cette ligne.
- `uptime` : charge sur 1 min entre 1,7 et 3,6 avant chaque campagne. `df -h /` : 7,1 à 8,0 Go libres.

**1. DT2-l, DT2-m, DT2-n.** Copies à l'identique de `g2/cc2/propose/R-1.diff`, `R-2.diff` et `R-5.diff` (`cmp` :
identiques). sha256 : l eea88358…, m b8d5368d…, n 03ab4d2a… (égaux à l'adjudication). Lignes : l +33/−17, m +23/−9,
n +16/−2 ; 0 octet 92, lignes ≤ 120.
- **DT2-l (R-1 + R-4) : juste.** La condition `t0[1] or tous and tous[0] <= t0[0]` refuse dès qu'aucune sonde n'est
  non vide. Le court-circuit protège la comparaison quand T0 vaut None. Coût : refus fermés, jamais une perte. Le cas
  −22 épingle le seuil (a).
- **DT2-m (R-2) : juste.** Refuse une réponse dont toutes les bougies suivent borne + c. C'est impossible sous exact,
  récentes, cpt et crenp, toutes bornées par la fin. Le minimum, et non le maximum, laisse écartée la bougie isolée
  du pt 2. Une lecture qui servirait au-delà de la fin sur une requête muette donnerait un refus, pas une perte.
  Observation : la marge + c n'était pas épinglée (mutant M02b, « borne sans le chevauchement », vivant sur la série
  a à n). Je l'épingle en DT2-p, cas « avant-1 ».
- **DT2-n (R-5) : juste.** Le dossier écrit à la main épingle le compte « seconde couverture » : `count('.') == 1`
  exclut les demi-pages.
- **Rouges rejoués sur la série** (AssertionError seulement) :
  - `rouge-dt2-l.out` : tests de l sur le code de k, 2 FAIL (cas R-1 cren et crenp), 0 ERROR ;
  - `rouge-dt2-m.out` : tests de m sur le code de l, 1 FAIL (« avant-100 »), 0 ERROR.
  - Les rouges de R-4 et R-5 sont des mutants (`mutants-lmn.log`) : X07 et X14 vivants sur la série a à k, tués sur la
    série a à n ; L01 (logique d'avant R-1) et M01 (R-2 retiré) tués.
  - `rouge-dt2-n.out` : vert sur le code de m, comme attendu pour un test qui épingle.

**2. DT2-o (R-3, README).**
- Mesure des renvois : aucun renvoi par numéro de ligne au README du lot dans les pièces lues (DECISION.md,
  RAPPORT.md de formes-api, RAPPORT-CC.md de cc et de cc2, RAPPORT-G2.md, mon rapport, BRIEF-CA.md, G0, AVIS et
  PROPOSITION de `docs/adr-0029/g0-calib`). `git grep` de `calib-actifs/README.md` suivi d'un numéro, limité à
  `docs/adr-0029`, `docs/JOURNAL.md`, `scripts/calib-actifs` et `gates.yml` : rien. Les points sont donc écrits en
  place.
- Les cinq points :
  - (i) recul des sondes : écrit par DT2-l ;
  - (ii) condition « ni sondée » : écrite par DT2-l ;
  - (iii) L-C13-2 « dans la propriété du générateur », 23 des 32 cas à chevauchement 0, configuration absente des
    places du lot (c = 1) : DT2-o ;
  - (iv) pertes de queue de la propriété cc2 (11, fenêtres jusqu'à 27 minutes ; 29 en marché mince, jusqu'à 95) :
    DT2-o ;
  - (v) miroir avant : écrit par DT2-m ; résidu de R-1 + R-2 (66) : DT2-o.
- DT2-o : +13/−5, sha256 fdf89c675bdb06d321f8bf289fcd1ac9852c9942b9a501c0a93885502b8f5fe9.

**3. Q-DT2-11 : oui, une fenêtre admise vide peut atteindre le calcul sans être vue.** Mesure :
`outils/q11_mesure.py`, `q11-mesure.out` (banc synthétique du lot, une série vidée à la fois, puis `tau.calcul_actif`).
- Chemin : `bougies.charger` admet une fenêtre où rien n'est servi (indiscernable d'une fenêtre muette). La série
  vide passe par `tau.main` → `bougies.oracle_sh` → `tau.calcul_actif` → `bougies.derniers` (clôtures toutes None) →
  `tau.ecarts` (la place n'est jamais « définie ») et `sigma.troisieme_terme` (aucune cellule). Il n'y a aucun refus si
  N_min tient sans la place.
- Mesuré : ETH et USDT admis pour toute place vidée. Le σ des places horodatées passe de 180 à 90 s quand Coinbase
  est vide (seule place à horodatage de dernière transaction d'ETH et d'USDT). USDC est refusé par N_min.
- En aval, sur la fenêtre principale, l'oracle de SH §4 couvre avec certitude :
  - Bitstamp USDC et USDT (comptes « actives » 693 et 1 542 → 0) ;
  - Bitstamp et Coinbase pour ETH (concurrence de 4 places au niveau 4 : 9 799 → 0).
- Il ne couvre **pas** Coinbase USDT, contrôlé seulement par des concurrences de 5 et 6 places, ce qui dépend des
  données. Il ne couvre pas non plus la fenêtre descriptive. La ligne de complétude (« total 0/N ») n'est jamais
  décisive.
- **Garde (DT2-p, recommandée et codée)** : dans `tau.calcul_actif`, une place de la lecture sans minute active dans
  la fenêtre donne `CA/population : place sans minute active dans la fenêtre`, avant tout calcul. Elle couvre toutes
  les places, les deux fenêtres (septembre imprime le refus) et les séries entièrement sans échange.
- **Seconde forme, non retenue** : dans `bougies.charger`, refuser une série vide pour les places en couverture
  double. Elle est plus étroite : ni Binance, ni Kraken, ni OKX, ni une série toute à volume nul.
- **Cas « marché mince » du résidu** (graine 14, cas 3890 de `prop-R12` : Coinbase pas 14, c 1, fenêtre de 28
  minutes, densité 0,1, décalage avant de 58 minutes). Le décalage dépasse la fenêtre sans atteindre la fin des
  données. R-2 refuserait toute réponse non vide, puisqu'elle serait entièrement après sa borne + c ; aucune ne l'a
  été, donc toutes étaient vides : les minutes décalées tombent sur des minutes sans échange. Rien n'est servi pour la
  fenêtre : c'est le même mécanisme que les 64, écrit au README et couvert par la garde.
- L'autre cas (graine 14, cas 3654 : fenêtre d'une minute, décalage de 3) est le miroir de L-C13-2. Les 64 restants
  ont toutes leurs requêtes décalées au-delà de la fin des données du marché (décalage > L + h + u + 2 pas + 5,
  recompté par script).
- **DT2-p** (+34/−8, sha256 00df0abdc526499bd4addcf2aa2c94665d4353994184b5baa6498e1f6863295d ; plancher 76 → … → 78 :
  77 → 78) :
  - `tau.py` (garde), `test_tau.test_place_vide`, README (ligne de `tau.py`) ;
  - cas « avant-1 » de `test_couverture`, qui épingle la marge + c de R-2 ;
  - `gates.yml` (plancher 78), `SHA256SUMS`.
- Rouges et mutants de DT2-p :
  - rouge (`rouge-dt2-p.out`) : `test_place_vide` sur le code de o, 5 FAIL, 0 ERROR ; « avant-1 » est vert sur o
    (épinglage) ;
  - mutants par la commande du job, plancher 78 (`mutants-Wp.log`, `mutants-Wp2.log`) : X07, X14, L01, M01, M02b et
    P01 (garde retirée) tués ;
  - P02 (refus dès une minute indéfinie) vivant, puis tué après l'ajout du cas « première minute sans échange :
    admise » ; M00 vivant.

**4. Série complète (tête e5bf085 + DT2-a à p ; `lourd-lp.log`, PID 21498, de 06:41:28Z à 06:57:23Z).**
- Matrice python 3.10 à 3.13 en `-X dev -W error` aux états l à p : 20/20 code 0 (Ran 77, 77, 77, 77, 78), aucun
  « Exception ignored » ni « Warning ».
- Sur l'état p :

| Suite | Résultat |
|---|---|
| job calib-actifs, au texte de `gates.yml` | Ran 78, plancher exact |
| runner | 137 ok |
| controle | Ran 37 |
| docs-sha256sums | conforme : 39 SHA256SUMS, 314 lignes |
| `cargo --locked --offline test`, cible par défaut (`Wp/target`, sans CARGO_TARGET_DIR) | code 0, 28 lignes « test result » toutes ok, 269 passés, 0 échec, 0 ignoré |

- La série a à p, appliquée en série sur l'archive de e5bf085, donne un lot égal à l'état p.
- Empreinte de la concaténation DT2-a à p dans l'ordre : a842a4341f43551fa5544a1259708990629642525235de6a93477f8faaf061bf.

**Écarts.**
- E-LP-1 : DT2-p porte aussi un cas qui épingle la marge de DT2-m (mutant M02b), hors du libellé « Q-DT2-11 ».
- E-LP-2 : l'index du dépôt réel a été modifié par un autre acteur pendant la passe (voir la base).

Fin de passe :
- sonde de 06:58:13Z coupée ;
- `ps` filtré sur le dossier vide ;
- copies Wk à Wp (et `Wp/target`) supprimées.

## 16. Ajout daté du 2026-10-10, 08:34Z (`date -u`) : R-6 à R-9 du contre-contrôle cc2 (DECISION.md, ajout 08:06:21 UTC, sha256 78c413ac…)

**Base.**
- Tête au début : 9a9bb23c74ac995ac942d55dab14a148aade059c (08:12:17Z).
- Depuis 01d74bd, `gates.yml` a bougé : quatre lignes de commentaire insérées avant le job calib, et le plancher s2bis.
  Les hunks `gates.yml` de DT2-a, b, c, d, f, g, h, k et p sont donc **recalés** : seuls leurs en-têtes `@@` changent
  (+4 lignes), le corps est identique, vérifié hors en-têtes.
- DT2-e, i, j, l, m, n et o sont copiés octet pour octet ; ils s'appliquent sans décalage ni flou.
- Rien d'autre n'a bougé sous `scripts/calib-actifs`.
- Dossier : `diffs-tete-9a9bb23c74ac995ac942d55dab14a148aade059c/`, DT2-a à DT2-t. La série s'y applique avec
  `patch -F0`, sans décalage ni flou. Lot obtenu : `SHA256SUMS` ef7f1063…, README 57ee4f91… (égaux à l'arbre T9 du
  contre-contrôleur).
- Tête relue à 08:34Z : 42d23d3 (aucun changement sous `scripts/calib-actifs` ni dans `gates.yml`). Copie octet pour
  octet en `diffs-tete-42d23d3aace474eb2287ae68e2d01e60a3bda799/` (`cmp`).
- **Empreinte de la série a à t** (concaténation dans l'ordre) :
  f85b61e9c48018937cc38751cec40aba8aa551f2a6bb7c38619103616c2dccfe.
- Charge sur 1 min entre 1,9 et 3,3 ; 6,8 Go libres.

**Identités** (`cmp`) : `propose/R-6.diff` = DT2-q (a4ca9f69…), R-7 = DT2-r (afd84c80…), R-8 = DT2-s (1a638e23…),
R-9 = DT2-t (2f678f38…).

**Relecture, une ligne chacun.**
- **DT2-q (R-6) : juste.**
  - Une seule minute active, la dernière (clôture 100), est le vrai bord : toutes les clôtures valent None sauf la
    dernière. Il est admis.
  - okx, dernière place de l'ordre trié, est contrôlée ; deux places vides donnent un refus nommé par la première.
  - BTC absents : `calcul_actif(…, {})` est refusé par la garde avant `sigma.sigmas`. Sans place vide, ce serait
    CA/btc.
- **DT2-r (R-7) : juste.** Recompté sur `bilan-R12.out` (AUTRE : 29 ; densités 0,03 : 14, 0,1 : 12, 0,3 : 2, 1 : 1) :
  - 28 cas à densité 0,3 ou moins ;
  - 1 à densité 1 : graine 12, cas 3436 de `rejeu-cas-p2.out`, fenêtre de 15 minutes, 5 échangées, dernière minute
    de cœur muette pour chacune des 11 requêtes ;
  - la fenêtre maximale de 95 minutes appartient aux 28.
- **DT2-s (R-8) : juste.** Configuration de Bitfinex (c = 0, une page de 15 minutes, décalage d'une minute vers
  l'avant). La page 0 ne sert que la minute 15 ; 15 > 14 + 0, donc APRES. Sous P13 (marge fixée à une minute),
  15 > 15 est faux : la réponse est admise puis écartée par le filtre, et le test attend APRES.
- **DT2-t (R-9) : juste, chaque chiffre vérifié sur les sorties du contre-contrôleur.**
  - 66 pertes et 38 des 40 (10 de queue sur 11, 28 sur 29) : `bilan-p2-transitions.out` (66 cren-avant, 8 cpt, 15
    cren, 9 crenp, 6 var → REFUS garde).
  - Restent 2 pertes partielles, graine 13, densité 0,3 (`rejeu-cas-p2.out`) :
    - cas 5479 : de queue (L-C13-2, var-cren), fenêtre de 11 minutes, 1 perdue sur 4 ;
    - cas 4093 : AUTRE, cpt, fenêtre de 20 minutes, 4 perdues sur 7 ;
    - chacune garde 3 minutes actives (7 − 4, 4 − 1).
  - Coût : 1 351 cas justes de la prémisse ; refus sur données complètes de 3 791 à 5 142 sur 7 947 (`bilan-R12.out`,
    `bilan-p2.out`).
  - Ventilation recomptée par script : fenêtre muette 477, densité ≤ 0,3 = 188 + 134 + 131 = 453, densité 0,6 à 1 =
    85 + 79 + 257 = 421.
  - « Sauf 7 » : 7 cas de la prémisse refusés par la garde, à densité 0,6 et sans bande muette, fenêtres de 1 à 3
    minutes (recompté sur `prop-p2-g*.tsv`).
  - « 87 pages ou plus pour Coinbase et Bitstamp » : vrai par `socle` (Bitstamp 87 et 88 sur 30 jours ; Coinbase 292
    ou plus).
  - Fenêtres de 91 et 30 jours : 131 040 et 43 200 minutes.
  - « Refus fermé et nommé, jamais une perte » : vrai sur le code (`tau.calcul_actif` lève CA/population).

**Rouges de R-6 et R-8** (mutants par la commande du job, plancher 78 ; `mutants-qt.log`) :
- sur a à p : P08, P09, P11, P12 et P13 tous VIVANTS ;
- sur a à t : P08, P09, P11 et P12 tués par `test_place_vide`, P13 par `test_double_couverture` ; P01 et P02 restent
  tués ; M00 vivant.

**Série a à t sur la tête** (`lourd-qt.log`, PID 23985, de 08:20:43Z à 08:33:43Z) :
- matrice python 3.10 à 3.13 en `-X dev -W error` aux états q, r, s et t : 16/16 code 0, Ran 78, aucun « Exception
  ignored » ni « Warning » ;
- job calib-actifs au texte de `gates.yml` : Ran 78 = plancher ;
- runner : 137 ok ;
- controle : Ran 37 ;
- docs-sha256sums : conforme, 40 SHA256SUMS, 319 lignes ;
- `cargo test` : **sans objet**. Aucun fichier Rust dans la série a à t (0 `.rs` dans les diffs), et aucun changement
  sous `xtask`, `crates` ni dans `Cargo.toml` et `Cargo.lock` entre 01d74bd et 9a9bb23 (`git diff --stat` limité à
  ces chemins).

Fin de passe :
- sonde de 08:34:02Z coupée ;
- `ps` filtré sur le dossier vide ;
- copies Tp à Tt supprimées ;
- dépôt réel : aucune écriture, aucune modification sous les chemins du lot.
