# Rapport du générateur de P2D (CB-9, témoin) (transcrit)

> Transcription par l'orchestrateur le 2026-10-17 22:35:44 UTC du fichier s2bis/p2d/RAPPORT-GENERATEUR.md ; contrôle FM-1.1 du transcript du générateur par le fm11.py versé : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5 (336 occurrences, aucune autre). Texte ci-dessous avec 11 retouche(s) (E35, E38) : noms de marqueur de dette et locutions de la gate S-G4 cités en clair, mis en code, segments de code à doubles accents graves réécrits en segments simples, heures sans date dans les 25 caractères ou approchées mises en code ou entre guillemets français, sans autre changement (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Rapport du générateur — lot P2D (partie P2 du collecteur de S2-bis, tranche D : CB-9, témoin)

**Gate 0 : `claude-opus-5-5`** (identifiant exact du modèle qui tourne), effort high, worker G1.

- Horloge (`date -u`) : ouverture 2026-10-17 08:13:47 UTC ; rapport écrit à `10:12:13` UTC.
- Brief : `<scratchpad>/s2bis/p2d/BRIEF-P2D.md`, sha256
  `9ce7afdd74c9854da004a742e5aa45588e61d9511804fe1a01a2c4ad04c75be9`.
- Base des diffs : `2a07ae6f2baecc662b3eda9594fdeee50c296e6a` (= 2a07ae6 du brief), tête du dépôt réel à
  l'ouverture et à `10:11:31` UTC (`git rev-parse HEAD` : inchangée ; `git status --short` limité à mes chemins : vide) ;
  copie par `git archive 2a07ae6` avec les sept exclusions du brief (absentes,
  `test -e`). Aucune opération git en écriture, aucun verrou (`--no-optional-locks`, `GIT_OPTIONAL_LOCKS=0`).
- Rattachement (G0) : G0 `docs/adr-0029/g0-collecte/G0-COLLECTE-RECALC-DEPLOI.md` (PROPOSITION corrigée par l'AVIS,
  qui prime) ; PROPOSITION l.217 (CB-9), l.167-168 (E-C-06, E-C-07), §2.4 (`Décodeurs` : prix Uniswap sous le
  contexte nommé) ; AVIS Q-C-14 (contexte complet, précision 50, `ROUND_HALF_EVEN`) ; ADR-0029 §2.5 l.174 ; G0 de
  CALIB-ACTIFS point 5 (Q-CA-09 : 3pool ; Q-CA-10 : `eth.drpc.org` pour Uniswap, `rpc.mevblocker.io` pour Curve) ;
  pièce `docs/adr-0029/g0-calib/PAIRES-ET-TEMOIN.md` §3.1, §3.2, §4.

## 1. Livrables

Dossier `<scratchpad>/s2bis/p2d/diffs/` : trois diffs à appliquer **dans l'ordre des numéros** sur 2a07ae6
(`git apply`), contrôlés en série par `outils/serie.sh` (extraction neuve des chemins touchés par `git archive 2a07ae6`,
`git apply --whitespace=error-all`, état comparé fichier par fichier au mini-arbre figé de chaque étape : 0 écart).

| # | diff | objet | code (R-25) | docs | retirées | plancher |
|---|---|---|---|---|---|---|
| 1 | `01-CB-9a.diff` | OKX `USDC-USDT`, Uniswap v3 `slot0`, corps `eth_call` construit | 186 | 23 | 3 | 380 |
| 2 | `02-CB-9b.diff` | Curve 3pool `get_dy(1, 2, 10^6)`, décimales distinctes | 58 | 22 | 3 | 384 |
| 3 | `03-CB-9c.diff` | règles `corps-du-decodeur`, `rpc-par-unite` ; FORMAT §9.1, §14.1 | 162 | 47 | 6 | 390 |

sha256 des diffs : `01-CB-9a.diff` `919a8ed1d78be161494804bc458a35642f75d39194d2f6c456b9e97ad6053889` ;
`02-CB-9b.diff` `a157039435dc17a8cbff685e88964d700057292c870f7c08cb6ad230e997367f` ;
`03-CB-9c.diff` `3ff08723074183b1b9e9cf32c0995a974d1218af6ba178ef86fae83f9f43ee78` (aussi dans SHA256SUMS).

Code (R-25) : ajouts des `.py` et `.yml` (`git diff --no-index --numstat`, fichier par fichier, `outils/compte.sh`) ;
docs : `.md` ; hors compte aussi les trois fixtures (`.bin`, 733 octets, une ligne chacune, au diff 1). Total code :
406 lignes, dont 297 de tests (73 %) et 109 de code (decodeurs 91, entree 15, gates 3).

Fichiers : `s2bis/shogen_s2bis/collecte/decodeurs.py`, `s2bis/shogen_s2bis/collecte/entree.py`,
`s2bis/tests/test_temoin.py` (neuf), `s2bis/tests/test_decodeurs.py` (l.52), `s2bis/tests/test_format.py`,
`s2bis/tests/fixtures/temoin/{okx,uniswap,curve}_usdc_usdt.bin` (neufs), `.github/workflows/gates.yml` (plancher),
`docs/adr-0029/s2bis/FORMAT-JOURNAUX-S2BIS.md`, `docs/adr-0029/s2bis/METRIQUES-S2BIS.md` (une section par diff).

Ce que fait le code :
- `okx_usdc_usdt` : `last` (prix), `ts` en ms (instant de génération du ticker), `askPx` et `bidPx` en extra (finis,
  > 0, bornes d'exposant de CONTEXTE ; aucun ordre exigé : la documentation d'OKX admet ask < bid avant l'ouverture),
  instrument `USDC-USDT` contrôlé ; classe `place_horodatee`.
- `uniswap_usdc_usdt` : sept mots de `slot0`, sqrtPriceX96 (Q64.96 : de 1 à 2^160 exclu), prix token1/token0 =
  sqrtPriceX96² / 2^192 · 10^(6 − 6), **une seule division**, sous une copie de `CONTEXTE` (`_quotient`), jamais le
  contexte du fil ; `tick` signé en extra ; classe `sans_horodatage`.
- `curve_usdc_usdt` : un mot, dy de `get_dy(1, 2, 10^6)`, prix dy · 10^6 / (10^6 · 10^6), même division ; `dy` en
  extra ; classe `sans_horodatage`.
- `eth_call(adresse, sélecteur, *arguments)` : corps JSON-RPC au bloc `latest`, forme du corps de Chainlink en S2
  (`sources.py` l.278-282) ; `CORPS` lie chaque décodeur sur chaîne au corps exact de sa requête. **Rien n'est
  envoyé** : les tests remplacent `http.lire` ; l'hôte RPC est celui de la forme (`formes.json`).
- Règles de `formes.json` (et de `carte.json`, par COHERENCE_CARTE) : `corps-du-decodeur` ; `rpc-par-unite` (unités
  et hôtes en bijection parmi les formes lues sur chaîne ; toute forme de la classe `oracle_chainlink` est l'unité
  `chainlink`, pour que les flux ETH, USDC et USDT de CB-8 y entrent sans liste à tenir).
- Aucun flottant : `parse_float=Decimal` et `parse_int=Decimal` (chemin `decoder` existant) ; les valeurs passent
  `_releve` et la garde de l'écrivain (SHOGEN-S2BIS-ECRIVAIN-REFUS-ARRET-1).

Fixtures, rattachées à leur ligne de la pièce (construites par `outils/fixtures.sh`, `bc` et `printf`) :

| fixture | octets | ligne de la pièce | valeurs |
|---|---|---|---|
| `okx_usdc_usdt.bin` | 145 | l.87 (valeurs), l.47 (forme et ordre des champs) | last 1.00062, askPx 1.00063, bidPx 1.00062, ts 1791487760439 |
| `uniswap_usdc_usdt.bin` | 486 | l.90 ; enveloppe de `fixtures/btc/chainlink.bin` | sqrtPriceX96 79254659562179534821884273396, tick 6, observationCardinality 180 ; quatre mots non mesurés (Q-4) |
| `curve_usdc_usdt.bin` | 102 | l.94 ; même enveloppe | dy 1000393 |

## 2. Tests d'abord, mutants, gates

**Rouges** (rejoués avec les tests finaux : `outils/rouges.sh`, `preuves/rouges.txt`) : code de l'état précédent
plus un squelette d'interface, python3.12 `-X dev -W error`, réseau isolé :
- CB-9a : 6 tests neufs, 6 FAIL, 0 ERROR (premier passage : 1 ERROR, corrigé dans le test par une garde) ;
- CB-9b : 4 FAIL, 0 ERROR ;
- CB-9c : 3 tests en FAIL (9 sous-cas) et le test du FORMAT en FAIL, 0 ERROR ; deux tests neufs sont verts avant le
  code (caractérisation : câblage des requêtes avec l'hôte de la configuration ; aucun hôte dans le code).

**Références hors du code** : prix d'Uniswap par `bc` (s²/2^192 exact à 220 décimales, arrondi à la main à 50 et à
28 chiffres), (2^160 − 1)²/2^192 et (2^256 − 1)/10^6 par `bc` ; mots et fixtures par `bc` (`obase=16`) et `printf` ;
corps des requêtes écrits à la main ; `ts` d'OKX par `date -u -d`. Contexte nommé (E-C-07) : sous un contexte du fil
altéré (3 chiffres, troncature), Uniswap et Curve rendent les 50 chiffres, par `decoder` et par le décodeur appelé
seul ; garde d'attendu : le contexte par défaut rend les 28 chiffres de `bc`, la fixture sépare donc les contextes.

**Mutants** : `scripts/controle/mutants.py` du dépôt réel (arbre relu, lu seulement, `python3 -I -B`), job
`s2bis-unittest` (runner puis ligne s2bis de `gates.yml`, suite entière), borne 300 s, réseau isolé, témoin vivant
d'abord ; listes `mutants/m9{a,b,c}.py` (et `.json`), diff et sortie de chaque mutant sous `mutants/sortie-*/` ;
bilan par `outils/bilan.py` (test visé lu dans les lignes `FAIL:`/`ERROR:` de la sortie).

| sous-lot | mutants | tués | par le test visé | par la ligne du job | vivants | FATAL | sortie de l'outil |
|---|---|---|---|---|---|---|---|
| CB-9a (passe m9a2) | 20 | 20 | 19 | 1 | 0 | 0 | 0 |
| CB-9b | 13 | 13 | 12 | 1 | 0 | 0 | 0 |
| CB-9c | 14 | 14 | 13 | 1 | 0 | 0 | 0 |

La première passe de CB-9a (m9a) a classé les 20 mutants tués, puis l'outil est sorti en 3 au relevé `ps` de fin
(écart E-4, §6) : elle ne compte pas ; m9a2 la rejoue en entier. Sites d'appel et étiquettes
(SHOGEN-MUTANTS-SITE-APPEL-1) : `_quotient` (arguments permutés, deux sites), `_fini` (bid et ask permutés sous leurs
étiquettes : fixture où ils diffèrent, 1,00062 et 1,00063), `_okx` (bid lu pour le prix : séparé par le cas ask < bid,
la fixture ayant bid = last), D_USDC et D_USDT (permutées : équivalentes à 6 et 6, séparées par un test qui pose
USDT à 18), nom de la forme au lieu de son décodeur (noms de forme ≠ décodeurs dans les configurations de test),
corps d'une autre pièce. Mutant écarté avant campagne, équivalent : la méthode `POST` non contrôlée par
`corps-du-decodeur` (`methode-corps` fait d'un corps non vide un POST ; la règle ne contrôle plus que le corps).

**Gates de l'arbre final** (copie complète : base, plus les trois diffs ; `preuves/final-*.txt`) : python3 (3.11),
réseau isolé, de `09:58:40` à `10:02:21` UTC : runner `verdict-suite-s2 : 153 ok, 0 échec` ;
s2bis, ligne du job `--plancher 390` : `conforme (code 0, résumé final, aucun saut, Ran = 390)` ; S2 (`--egal`) :
`conforme (… sauts nommant SHOGEN_S2_CAMPAGNE_CONTROL, Ran = 423)` ; sim-bis, ligne du job `--plancher 279` (GIT_DIR du
dépôt réel en lecture seule, verrous optionnels coupés) : `conforme (… aucun saut, Ran = 279)`. Aucun `__pycache__`
laissé dans une racine de suite. Base t0 : 153, 374, 423, 279 (mêmes commandes).

**Matrice** (suite `s2bis`, 3.10 à 3.13, `-X dev -W error`) : `unittest discover` sous python3.10, 3.11, 3.12 et 3.13
(`10:02:47` à `10:08:42` UTC) :
`Ran 390`, `OK`, 0 ligne `Exception ignored`, 0 ligne `Warning` sous chacune ; la ligne du job
(`--plancher 390`) est `conforme` sous chacune (`preuves/matrice-*.txt`).

**xtask** : `cargo --locked xtask verify`, cible cargo par défaut de chaque arbre (aucun `CARGO_TARGET_DIR`), réseau
isolé, sur l'arbre final et sur une extraction neuve de la base (témoin) : lignes de verdict identiques
(`preuves/xtask-final-verdicts.txt`, `preuves/xtask-t0-verdicts.txt`) ; S-G1 à S-G8 `VERT`, `cargo fmt --check`,
`no_std`, `cargo clippy -D warnings` `VERT` ; S-G9 `ROUGE (1 violation(s))` dans les deux arbres :
`docs/17-modele-de-menace.md:70`, référence vers `docs/rapports/`, dossier exclu de mes copies par le brief (artefact
de l'exclusion ; les NOTES du lot P2B consignent la même ligne [2nd]) ; `VERDICT GLOBAL : ROUGE` dans les deux, pour
cette seule raison.

## 3. Items de l'annexe B (recherche de `CB-9` dans `docs/adr-0028/ANNEXE-B-items.md` seul)

Deux lignes nomment CB-9 : l.1265 (en-tête du bloc B.81, `Débloqués : CB-7, CB-8, CB-9`) et l.1275 :
- **SHOGEN-S2BIS-CURVE-DOC-1** (déclencheur `G2 de CB-9`, prix `une lecture`) : **non fermé, rendu**. La
  documentation de `get_dy` du 3pool, le rattachement du pool NG à sa fabrique et le sens de `price_oracle` demandent
  une lecture de pages en ligne ; le registre `biblio/INDEX.md` n'en détient aucune (recherche `curve` dans ce seul
  fichier : aucune ligne) et le brief interdit toute opération réseau. Le G0 de CALIB-ACTIFS (point 5) en fait une
  condition de la G2 de CB-9 : à lever avant elle (lecteur `claude-sonnet-5-5`, ou une copie versée au registre). Le
  code retient `get_dy` (Q-CA-09) et écrit la limite dans la docstring de `_curve`.
- **SHOGEN-S2BIS-TEMOIN-RPC-1** (B.81, déclencheur `avant le sceau`) : hors de mes sous-lots, **précisé** : la règle
  `une unité on-chain = un hôte RPC` est tenue par le code (`rpc-par-unite`), les deux hôtes retenus n'existent
  qu'en configuration (tests `test_une_unite_sur_chaine_un_hote_rpc`, `test_aucun_hote_en_dur_dans_les_decodeurs`) ;
  restent ouverts la lecture des conditions et le smoke (CB-16 et observateurs).

Aucun autre item n'a CB-9 pour déclencheur.

## 4. Questions rendues

- **Q-1 Classe de source du témoin** (non nommée : ni l'ADR-0029 §2.5 l.174 ni la PROPOSITION n'en donnent ; FORMAT
  §9.1 et `test_bout_en_bout` l.79 ferment la liste à quatre classes). Candidats : (a) **retenu, provisoire** : OKX
  `place_horodatee`, Uniswap et Curve `sans_horodatage` (liste fermée inchangée ; le témoin est isolé par `actif`
  USDC et `devise` USDT, et par le nom de la forme) ; (b) une classe neuve `temoin` pour les trois : change le FORMAT
  §9.1, `PLANCHERS` de `recalc/config_analyse.py` (classes connues) et `test_bout_en_bout` ; (c) une classe
  `sur_chaine` pour Uniswap et Curve seuls, OKX en `place_horodatee`. Le recalcul (RB-2, P_j) lira le témoin : la
  décision le concerne autant que le collecteur.
- **Q-2 Règle `un hôte par unité` entre le pool et la carte** : tenue dans chaque fichier, non entre les deux. Une
  source de la carte lue sur chaîne (ADR-0029 l.170 : Uniswap WBTC, RedStone) pourrait partager l'hôte d'une unité du
  pool. Candidats : (a) laisser ; (b) une règle croisée `rpc-partage` dans `entree.CROISEES` (une ligne, un test, une
  phrase au §15.2, le compte de `test_paragraphe_15_processus_secondaire` à relever).
- **Q-3 Recouvrement avec P2C (CB-7, CB-8)**, menée en parallèle sur la même base : mêmes fichiers (`decodeurs.py` :
  fin de `DECODEURS` et docstring ; `test_decodeurs.py` l.52, changement identique dans les deux séries ; en-tête du
  FORMAT ; fin de METRIQUES ; plancher de `gates.yml`, 374 → 380 dans les deux). Les deux séries ne s'appliquent pas
  l'une sur l'autre telles quelles. Je propose de rebaser la série CB-9 sur P2C une fois P2C adjugée (planchers
  relevés de l'écart, hunk de l.52 retiré) ; aucune variante n'est faite avant ce message.
- **Q-4 Fixture de `slot0`** : quatre mots ne sont pas mesurés par la pièce (observationIndex 0,
  observationCardinalityNext 180, feeProtocol 0, unlocked 1, déclarés dans `outils/fixtures.sh`) ; le décodeur ne
  lit que les mots 1 et 2, mesurés (l.90). Une capture réelle d'une réponse complète (smoke, CB-16) les remplacerait.

## 5. Limites rendues (items à former, règle PAROXYSME)

| item proposé | constat | déclencheur proposé |
|---|---|---|
| SHOGEN-MUTANTS-PID-REEMPLOI-1 | le relevé `ps` de fin de `scripts/controle/mutants.py` compte comme reste de la campagne tout processus dont le groupe porte un numéro relevé plus tôt ; sous lots concurrents, un PID réemployé (pid_max = 32 768) fait sortir l'outil en 3 (E-4 : groupe 27390, `campagnes.sh` de P2C lancé à `09:05:40`) | prochain lot qui touche l'outil commun |
| SHOGEN-S2BIS-DNS-DELAI-CHARGE-1 | `test_dns.Interroger.test_delai_reseau_forme_et_identifiant_aleatoire` borne chaque délai sous 300 ms ; sous la charge de deux lots, un délai a mesuré 316 ms (sortie du mutant M9b-05, tué par ailleurs) : faux rouge possible d'un témoin de campagne | prochain lot de dettes de la suite s2bis |
| SHOGEN-S2BIS-TEMOIN-BLOC-1 | une lecture `eth_call` `latest` ne rend pas le bloc lu : Uniswap et Curve n'ont aucun instant de source (`ts_source` null) ; un lot JSON-RPC avec `eth_blockNumber` le donnerait, hors des formes lues sur pièce | G0 de RB-2 (lecture de P_j) ou smoke CB-16 |
| SHOGEN-S2BIS-OKX-CARNET-VIDE-1 | `bidPx` ou `askPx` vide ou absent rend la lecture d'OKX `panne_decode` (choix du lot) ; la documentation lue ne dit pas si un carnet vide rend `""` | smoke CB-16 (capture) |

## 6. Écarts

- **E-1** : contrôle d'absence de `docs/15-*` et `docs/16-*` par `ls -d` avec un glob sur `docs/` de ma copie
  (consigne `Listes sous docs/`) ; sortie : deux `No such file`, aucun nom listé.
- **E-2** : deux heures écrites dans NOTES sans lire `date -u` ; corrigées à `08:36:37` en `avant 08:36, heure non lue`.
- **E-3** : `ls -R` de mes mini-arbres figés (`travail/f`), dont leurs sous-dossiers `docs/`, sortie tronquée à cinq
  lignes (noms des quatre mini-arbres) : énumération récursive sous une copie de `docs/`. Plus aucune ensuite.
- **E-4** : campagne m9a sortie en 3 au relevé `ps` de fin, faux positif par réemploi de PID
  (`preuves/E4-ps-27390.txt`) ; campagne rejouée (m9a2), la première passe n'est pas comptée.
- **E-5** : deux lots lourds ont tourné en même temps sur l'hôte (mes campagnes et celles de P2C, comme le brief
  l'annonçait) ; chez moi, un seul processus lourd à la fois, les essais de modules (moins de 10 s) mis à part.
- **E-6** : un premier jet de ce rapport, écrit par bash, portait un sha256 écrit de mémoire et faux (celui du G0 de
  CALIB-ACTIFS) ; relevé à la relecture, remplacé par la valeur recalculée ; toutes les empreintes de ce rapport sont
  recopiées depuis une sortie d'outil de cette session.

## 7. Estimation révisée des sous-lots restants de P2

Mesuré ici [mesuré, `outils/compte.sh`] : CB-9, chiffré ≈ 180 lignes au G0 (PROPOSITION l.217), fait 406 lignes
ajoutées de code et de tests en trois diffs, soit ×2,26 (tests : 73 %). Restent dans P2, hors des tranches A à D :
CB-14.k (≈ 175 chacun ; k = 0 à 2 selon l'AVIS Q-G-04, carte coupée au gel), CB-16 (smoke sans prix, ≈ 140) et
CB-19 en option (≈ 160, ou au lot RODAGE, Q-C-13). Avec la règle d'estimation (×2 à ×3, jalon sur la borne haute ;
×2,26 mesuré ici pour des décodeurs) : CB-16 ≈ 280 à 420 lignes (2 à 3 diffs) ; CB-14.k ≈ 350 à 525 par lot (2 à 3
diffs chacun), soit 0 à 1 050 ; CB-19 ≈ 320 à 480 s'il reste dans P2 ; plus le rebasage de CB-9 sur P2C (Q-3, ≈ 1
diff) et les corrections de la G2 de la partie P2 (non chiffrées) [inféré]. **Total P2 restant : ≈ 280 à 1 950
lignes, ≈ 3 à 13 diffs.**

## 8. Journal de provenance (G1)

Sources lues ; sha256 à 2a07ae6 (`git show 2a07ae6:<chemin> | sha256sum`) :
- [lu] `docs/adr-0029/g0-collecte/G0-COLLECTE-RECALC-DEPLOI.md`, entier, 100 l.
  (`08c1e6b0d307e11509798bd9409c6947e11df381602e22ad20f10a32c8ec691d`).
- [lu] `docs/adr-0029/g0-collecte/PROPOSITION.md` l.100-135, l.160-330, l.350-370, l.790-805
  (`0cdf84c25092101a9f2d8075fc90f59a5af7b689458b025635d42adb865fbfd0`, celui que cite le G0).
- [lu] `docs/adr-0029/g0-collecte/AVIS.md` l.1-80, lignes de Q-C-10 et Q-C-14
  (`a919b307e80f860733f9e114504c0ec93e30a87fabb0970b9384a854421616ce`).
- [lu] `docs/adr-0029/ADR-0029-campagne-S2-bis.md` §2.5 l.166-175, ajouts datés l.397-405, titres
  (`32a598931dd35c91afbc7e61fec532a1a18de2e4c69e188b2d22b97aadaa2801`).
- [lu] `docs/adr-0029/s2bis/FORMAT-JOURNAUX-S2BIS.md` en-tête l.1-61, §9 l.331-378, §14 l.583-636
  (`799c829100658910836d2ff5f28171c68e202972b4cfd9e4bde709e2bf38f5a6`).
- [lu] `docs/adr-0029/g0-calib/PAIRES-ET-TEMOIN.md`, entier, 139 l.
  (`75535ad5a43c3d1b0fc7eaaaed52f260bc9c8c51f1dfbc45feb4dcddddc1258b`) : l.47 (forme d'OKX), l.53, l.87 (OKX
  USDC-USDT), l.89 (jetons, décimales 6), l.90 (pool 0,01 %, `slot0`, sqrtPriceX96, tick 6, cardinalité 180), l.94
  (3pool, `get_dy(1, 2, 10^6)` = 1 000 393), §3.2 (hôtes), §4 (limites, point 8).
- [lu] `docs/adr-0029/g0-calib/G0-CALIB-ACTIFS.md` l.30-40
  (`914f2dd1ac8df232e472d80302079f981eb905420fd773a371af93070f14d700`) ; `AVIS.md` Q-CA-09, Q-CA-10, §5
  (`6deaf8cd9a5c7d24157b8957959861258809ea6280c0de1bdb74bb380660f1b8`) ; `PROPOSITION.md` §2.5, §2.6, §5.2, Q-CA-08
  à Q-CA-10 (`4514370faea93c4bbf91942a5b2b8120462c002cb823a8cdade6bbbb45a8f226`).
- [lu] `docs/adr-0028/ANNEXE-B-items.md`, par recherche dans ce seul fichier (`TEMOIN-RPC-1`, `CB-9`),
  l.1255-1280 (`ff6b4f4761ab2690d15466cb9371557b1aa64e8b3cb2257cd5431589d383f4f9`).
- [lu] `biblio/okx-docs-v5-en-api-guide-2026-10-10.html` du dépôt réel (hors suivi git ; sha256
  `009d139c6386fad226e43a47a346d00be4cac2fe8412779078d65c2cc9e50f0d`, égal à `biblio/INDEX.md` l.449) : section
  `GET / Ticker` (champs `last`, `askPx`, `bidPx`, `ts`, tous `String` ; « Best ask price may be lower than the
  best bid price during the pre-open period ») ; `biblio/INDEX.md` par recherche (curve, uniswap, okx, drpc).
- [lu] `s2-harness/shogen_s2/sources.py` l.1-30, l.270-300 (corps `eth_call` de S2 ;
  `0c81fc33425c66ba7c0684d65245048a9748331043a0b425329191c66dd4afe4`) ; fixture
  `s2bis/tests/fixtures/btc/chainlink.bin` (enveloppe JSON-RPC).
- [lu] code : `s2bis/shogen_s2bis/collecte/decodeurs.py`, `entree.py` l.1-200, `http.py` l.15-45 ; tests
  `test_decodeurs.py`, `test_entree.py` l.1-202, `test_secondaire.py` l.25-160, `test_format.py` l.1-40 et
  l.182-224 ; `scripts/controle/mutants.py`, entier
  (`3e21878363ad7a106357abb666c3d8c5351f8ac94fcf3d95c4e64400abddad64`) ; `.github/workflows/gates.yml` l.245-330.
- [lu] diffs de P2C (`<scratchpad>/s2bis/p2c/diffs/`), lignes de plancher et de `test_decodeurs` seules (Q-3).
- [2nd] aucun : adresses, sélecteurs, décimales et valeurs viennent de la pièce [lu], qui les tient pour [mesuré]
  (lecteur `claude-sonnet-5-5`, 2026-10-08) ; je ne les ai pas re-mesurés (réseau interdit).
- [abs] documentation de `get_dy` du 3pool, sens de `price_oracle` (SHOGEN-S2BIS-CURVE-DOC-1) ; conditions des hôtes
  RPC (SHOGEN-S2BIS-TEMOIN-RPC-1) ; sémantique d'un carnet vide chez OKX.

Commandes et sorties (preuves sous `preuves/`) :
- base t0 (`08:22`-`08:26`) : runner 153 ok ; s2bis 374 conforme ; S2 423 conforme (skipped=2) ; sim-bis 279 conforme
  (`preuves/t0-*.txt`).
- rouges et verts : `preuves/rouge-*.txt`, `preuves/rouges.txt`, `preuves/vert-*.txt`.
- campagnes : `mutants/campagne-m9{a,a2,b,c}.{txt,log}`.
- chiffres recomptés : lignes ajoutées par `git diff --no-index --numstat` (`outils/compte.sh`) ; tests par le `Ran`
  de chaque suite ; octets des fixtures par `wc -c` (102, 145, 486).

Outils (tous dans `outils/`, hors dépôt) : `gates.sh`, `essai.sh`, `fixtures.sh`, `campagne.sh`,
`suite_campagnes.sh`, `suite2.sh`, `bilan.py`, `geler.sh`, `chemins.txt`, `compte.sh`, `faire_diff.sh`, `serie.sh`,
`decouper.py`, `rouges.sh` ; listes de mutants dans `mutants/`.

## 9. Nettoyage

`10:11:42` UTC : copies lourdes effacées (`copie/` et sa cible cargo, `t0-complet/` et sa cible,
`etats/`, `rouge/`, contenu de `tmp/`), après contrôle qu'aucun de mes processus ne tournait (`pgrep -f` ancré : rien).
Restent (9,1 Mo) : `diffs/`, `mutants/` (listes, diff et sortie de chaque mutant), `preuves/`, `outils/`,
`travail/f/` (mini-arbres figés, liste explicite : la série se rejoue par `outils/serie.sh 2a07ae6`), `travail/edits/`,
`travail/t0/`, sorties brutes de xtask (`travail/xtask-*-brut.txt`, hors rapport), NOTES, ce rapport, SHA256SUMS.
