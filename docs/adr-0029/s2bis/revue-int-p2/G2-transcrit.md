# Relecture G2 neuve de la série intégrée P2 (transcrit)

> Transcription par l'orchestrateur le 2026-10-17 22:35:44 UTC du fichier s2bis/int-p2/g2/RAPPORT-G2.md ; contrôle FM-1.1 du transcript du réviseur G2 par le fm11.py versé : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5 (327 occurrences, aucune autre). Texte ci-dessous avec 6 retouche(s) (E35, E38) : noms de marqueur de dette et locutions de la gate S-G4 cités en clair, mis en code, segments de code à doubles accents graves réécrits en segments simples, heures sans date dans les 25 caractères ou approchées mises en code ou entre guillemets français, sans autre changement (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# RAPPORT-G2 : relecture G2 neuve de la série intégrée P2 (INT-P2-01 à INT-P2-16)

**Gate 0 : `claude-opus-5-5`** (identifiant exact du modèle qui tourne ; effort `high`), worker `shogen-worker`,
réviseur G2 distinct des deux générateurs (P2C, P2D) et de l'intégrateur (INT-P2). Brief : `g2/BRIEF-G2.md`
(sha256 `2291296ae1671cfb1643329272920ae59beeeb966bcca46dc900f8fb82701962`), lu en entier.

Dates (`date -u`) : ouverture 2026-10-17 16:49:50 UTC ; rédaction commencée `18:05:47` UTC ; clôture `18:40:16` UTC.
Dépôt `/home/user/shogen` en lecture seule : tête `2a07ae6f2baecc662b3eda9594fdeee50c296e6a` (attendue `2a07ae6`),
aucune écriture git, `git --no-optional-locks`, commandes git limitées à des chemins nommés. Copies : extractions
`git archive 2a07ae6` (exclusions du brief, plus tout `*.jsonl`) sous `g2/travail/`. Réseau isolé partout
(`unshare -n`, `isole.sh` de `p1b/g2`), `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée, `TMPDIR` = `g2/tmp`, tout Python de
la relecture en `python3 -I -B` (les lignes des jobs tournent telles qu'écrites dans `gates.yml`).

## Verdict : ACCEPTE-AVEC-CORRECTIONS (C-1, C-2, C-3)

| C-n | objet | pas visé | diff (contre l'arbre final de la série) |
|---|---|---|---|
| C-1 | `capture` : l'ouverture exclusive (`xb`, `x`) n'est fixée par aucun test ; mutants `wb` et `w` vivants | pas neuf **INT-P2-17**, après INT-P2-16 (le replier dans INT-P2-16 donnerait 197 + 17 = 214 lignes, au-delà de R-25) | `diffs/C-1.diff` |
| C-2 | `smoke` et `capture` : port de la forme et contexte TLS de `capture` jamais relevés par les tests ; mutants port 443 en dur (smoke, capture) et `tls=None` (capture) vivants | même pas neuf **INT-P2-17** (vise les tests de INT-P2-13 et INT-P2-16) | `diffs/C-2.diff` |
| C-3 | pièce G6 : aucune ligne pour les fixtures du témoin `s2bis/tests/fixtures/temoin/` | **INT-P2-07** (CB-9a, qui crée ces fixtures ; G6 de l'arbre final égal à celui de l'état 07) | `diffs/C-3.diff` |

`diffs/INT-P2-17.diff` porte C-1 et C-2 ensemble (une section METRIQUES, plancher 431), prêt pour la chaîne ; C-1 et
C-2 s'appliquent aussi chacun seul sur l'arbre final (chacun avec sa propre section METRIQUES : ne pas les enchaîner,
poser INT-P2-17). Chaque diff a été appliqué par `git apply --whitespace=error-all` sur une copie de l'arbre final
(code 0) et comparé à l'octet à l'arbre corrigé (`cmp`). Ligne à ajouter à `pas.tsv` si INT-P2-17 est adopté :
`INT-P2-17`, sujet `C-1 et C-2 de la G2 : capture jamais écrasante, port et TLS du smoke et de la capture figés par les
tests`, `n_tests` 431 ; `source-pas.md` : `relecture G2 neuve de la série, g2/RAPPORT-G2.md ; écrit par le réviseur`.

## 1. Série, planchers, gates (point 1) : CONFORME

- Les seize diffs (sha256 égaux à `SHA256SUMS` de l'intégrateur ; 01 à 06 égaux à l'octet, `cmp`, aux six diffs de
  P2C) s'appliquent dans l'ordre sur une extraction neuve de 2a07ae6 : `git apply --whitespace=error-all`, code 0 à
  chacun (`preuves/serie.txt`). `outils/fichiers.txt` de l'intégrateur = les 44 chemins des diffs.
- À chaque état, sur une extraction neuve et les fichiers figés de l'état, la commande du job (runner, puis la ligne
  s2bis de `gates.yml` telle qu'écrite, `--egal`) : 16 fois code 0, runner `153 ok, 0 échec`, `Ran =` 375, 379, 380,
  386, 388, 394, 400, 404, 410, 413, 415, 416, 420, 422, 425, 430, égal au plancher écrit de chaque état
  (`preuves/etats-job.log`) ; base 374 (`git show 2a07ae6:.github/workflows/gates.yml`, l.291).
- Arbre final : voir §10 (runner, S2, sim-bis, matrice, xtask, `__pycache__`).

## 2. Fidélité des fixtures (point 2) : CONFORME, SAUF LA PIÈCE G6 (C-3 ; observations O-1, O-2)

Chaque fixture rattachée à sa ligne de `PAIRES-ET-TEMOIN.md` (relue en entier) :
- ETH, USDC, USDT des places : formes du tableau 1.2 (Binance objet à un symbole, prix à 8 décimales ; Coinbase,
  Kraken `a` à `o` sous les clés rendues `XETHZUSD`, `USDCUSD`, `USDTZUSD` ; OKX `code`, `data` à seize champs, `ts`
  en ms ; Bitstamp treize champs dans l'ordre de la pièce ; Gemini v1 `volume.timestamp` en ms) ; valeurs du
  tableau 1.1 (2455,94 ; 0,99996 ; 0,99933 ; 2454,47 ; 0,9992 ; 2454,74 ; 0,9999 ; 0,99921 ; 0,99939 ; 2455,7 ; 2455,08 ;
  0,99976 ; 0,99919 ; 2454,44 ; 0,99982 ; 0,99918) ; champs élidés construits et déclarés (rapport de P2C §7).
- Agrégateurs : CoinGecko et DefiLlama à quatre identifiants, Bitfinex `v2/tickers` (symbole, puis onze champs,
  dernier prix à l'indice 7, codes `UDC` et `UST`) ; valeurs de la pièce (l.29, l.31, l.51, l.52).
- Chainlink : cinq mots décodés hors du code (Python, Decimal à 60 chiffres) : ETH 2457,46 à 2026-10-08 19:26:47,
  USDC 0,99986 à `15:38:23`, USDT 0,99928672 à `14:38:23`, phases et tours 7/34445, 4/26, 4/25 : égaux à la pièce §2 ;
  plafond `1.05000000` (`maxSubmissionValue` 105000000, l.72) en extra d'USDC et d'USDT seuls.
- Témoin : OKX last 1,00062, bid 1,00062, ask 1,00063, `ts` 1791487760439 (l.87) ; Uniswap sqrtPriceX96
  79254659562179534821884273396, tick 6, cardinalité 180 (l.90), prix recalculé 1,000668991… (1,000669 de la pièce) ;
  Curve dy `0xf43c9` = 1000393 (l.94). Décimales 6 et 6 (l.89).
- Adresses et sélecteurs (pièce §2 et §3) : pool `0x3416cF6C…27C6`, 3pool `0xbEbc4478…FF1C7`, proxys
  `0xF4030086…E88c`, `0x5f4eC3Df…8419`, `0x8fFfFfd4…18f6`, `0x3E7d1eAB…e32D` ; sélecteurs recalculés hors du code par un
  Keccak-256 écrit pour cette relecture (garde : haché du texte vide) : `latestRoundData()` `0xfeaf968c`, `slot0()`
  `0x3850c7bd`, `get_dy(int128,int128,uint256)` `0x5e0d443f`, `getPool(address,address,uint24)` `0x1698ee82` ; sommes
  EIP-55 des six adresses conformes (`preuves/selecteurs.txt`).
- Aucun flottant : `json.loads(…, parse_float=Decimal, parse_int=Decimal)` seul chemin ; une constante `NaN` ou
  `Infinity` (flottant de `parse_constant`) est refusée par `_releve` (type) : vérifié au §7.
- sha256 des cinq fixtures écrits à la main dans `test_capture` recalculés par `sha256sum` : égaux.
- Pièce G6 (`docs/adr-0029/s2bis/G6-PAQUET-S2BIS.md`) : une ligne pour les fixtures BTC, une pour les actifs
  (INT-P2-02), aucune pour `s2bis/tests/fixtures/temoin/` (la tranche D n'y a pas touché) : C-3.

## 3. Conformité au contrat (point 3) : CONFORME

- Tableau 1.1 : un décodeur par paire servie ; aucun pour Coinbase USDC/USD, OKX ETH/USD et USDC/USD (sans
  substitut ; OKX `USDC-USDT` est de classe `temoin`) ; CB-7c : binance `ETHUSDT`, okx `ETH-USDT`, cotés en USDT
  (Q-CA-01 (a), AVIS de CALIB-ACTIFS l.41). Lectures de vote par actif dans `formes-pool.json` (script) : BTC 11 (dont `okx_index`), ETH 10, USDC 8, USDT 10 ; témoin 3.
- E-C-09 : CoinGecko, DefiLlama et Bitfinex regroupés à quatre actifs, un relevé par actif, pannes identiques
  (ADR-0029 l.236) ; OKX : cinq lectures séparées avec le témoin, budget 5 + 4 + 10 + 1 = 20 s, sixième refusée
  (Q-C-10). Plafond Chainlink porté en extra, jamais appliqué (E-C-10).
- Classe `temoin` (C-P2D-1) : trois décodeurs du témoin seuls, hors `PLANCHERS` et `SIGMA_BTC`, refus nommé
  `ANALYSE/temoin` dans `tau_sigma` ; le recalcul ne lit pas encore les `valeurs` (RB-2) : voir l'item I-3 (§8).
- Contexte nommé (E-C-07, Q-C-14) : `decoder` sous `localcontext(CONTEXTE)`, `_quotient` sous une copie de CONTEXTE ;
  aucun calcul Decimal dans `smoke` ni `capture`.
- Smoke (E-C-37, ADR l.222) : lignes de métadonnées seules, comparées en entier par les tests. Mutants construits par
  moi et tués : G2-20 (prix imprimé sur la sortie standard hors de `sortie`), G2-21 (octets du corps sur l'erreur
  standard), G2-22 (fourchette et extra dans la ligne) ; rejoués : M13-01 (prix), M13-02 (octets).
- Capture (Q-C-05) : rien sur la sortie standard (tests et mutants M16-01, M16-03) ; aucun écrasement : contrôle des
  noms avant toute lecture (M16-04 tué) mais ouverture exclusive non testée (C-1).
- Hôtes : aucun dans `decodeurs.py` (recherche de noms d'hôte dans `decodeurs.py`, `smoke.py`, `capture.py`,
  `entree.py` : un seul, `min-api.cryptocompare.com` de `smoke.py`, URL de S2 pour la re-confirmation du 401, écrite au
  FORMAT §18 : O-4).

## 4. Rebasage de CB-9 (point 4) : CONFORME

Comparaison des multiensembles de lignes ôtées et ajoutées par fichier entre `p2d/diffs/0{1,2,3}-CB-9*.diff` et
INT-P2-07 à 09 (`outils/compare_hunks.py`, `preuves/compare-rebase.txt`). Seuls écarts : planchers ; METRIQUES (comptes
de lignes relevés, phrase du rebasage ; comptes recontrôlés par `wc -l` : 324, 338, 349 ; 248 ; 101 ; 308) ; docstring
de `decodeurs.py` recoupée (mêmes mots) ; l.52 de `test_decodeurs.py` absente (changement identique déjà porté par
P2C, vérifié sur l'état 06) ; `test_paires_absentes_sans_decodeur` et `test_requete_btc_de_s2_gardee` (conflits de sens
déclarés, confirmés par l'adjudication). FORMAT, `entree.py`, `test_temoin.py`, `test_format.py` et fixtures : lignes
identiques. Aucun écart hors des conflits déclarés.

## 5. Tests d'abord (point 5) : CONFORME

Rejoués pour les pas 10 à 16 (`outils/rouge.sh` : état précédent, puis les seuls fichiers de test du pas ; puis
l'état du pas ; `preuves/rouge-10-11.txt`, `rouge-12-16.txt`) : 10 : 9 FAIL, 0 ERROR, puis OK ; 11 : 2 FAIL, puis OK ;
13 : 1 ERROR d'import (module `smoke` absent ; l'intégrateur a montré 9 FAIL sur squelette), puis OK ; 14 : 1 FAIL et
1 ERROR (sous-commande absente), puis OK ; 15 : 7 FAIL, puis OK ; 16 : 1 FAIL et 1 ERROR d'import, puis OK.
Pas 12 (tests seuls, verts sur l'état 11, déclarés `par des tests seuls` au FORMAT) : AST de `Bornes` relu par un
script indépendant (`outils/ast_bornes.py`) : module sans `import time`, aucun nom lié au temps dans la classe ni dans
`prix` ; sur l'état 11, `monotonic` et `time` nommés ; sous une horloge monotone truquée (+0,2 s par lecture), l'ancien
`Bornes` 6 FAIL, le nouveau `Ran 7`, OK (`preuves/ast-bornes-avant-apres.txt`) ; rejoué dix fois pendant la campagne
g2 : dix `OK` (`preuves/bornes-dix.txt`). Caractérisation déclarée : CB-9c (deux tests verts avant le code, METRIQUES).

## 6. Mutants (point 6) : CINQ VIVANTS (FAUTES), TOUS TUÉS APRÈS C-1 ET C-2

Outil `scripts/controle/mutants.py` d'une extraction de 2a07ae6 (sha256 `3e218783…abddad64`, à part de la copie
mutée), job `s2bis-unittest`, borne 300 s, tué = sortie 1, témoin vivant d'abord.
- Campagne g2 (arbre final, 51 mutants ; `mutants/g2.bilan.txt`) : 25 mutants de l'intégrateur rejoués (pas 10 à 16 :
  M10-02, 05, 06, 09 ; M11-01, 07 ; M12-02, 05, 07, 10 ; M13-01, 02, 05, 08, 15 ; M14-01, 03, 09 ; M15-01, 06, 07 ;
  M16-01, 04, 11, 12) : 25 tués par leur test visé. 26 mutants neufs (G2-01 à G2-26) : Uniswap inversion
  token0/token1, borne 2^160, signe du tick, décimales permutées, pool 0,05 % ; Curve décimales, i et j inversés ;
  décimales de USDT à 18 ; Chainlink plafond perdu (USDT), porté à tort (ETH), écrit sans ses 8 décimales ; Binance
  symbole et Kraken clé non contrôlés ; OKX bid lu pour le prix ; témoin OKX bid sous l'étiquette de l'ask, ask nul
  admis ; Bitfinex indice 6, UDC et UST permutés ; CoinGecko USDC et USDT permutés ; devise USDT pour Coinbase ETH,
  Bitstamp et Gemini ; smoke : prix, octets, fourchette imprimés ; capture : `wb`, `w`. Résultat : 24 tués par leur
  test visé, **2 vivants (G2-23, G2-24)**, 0 FATAL ; relevé `ps` de fin vide (104 groupes).
- Campagne g2b (arbre final ; mutants repérés à la lecture des tests, aucun test ne relevant le port des requêtes
  de `smoke` et `capture` ni le contexte TLS de `capture` ; `mutants/g2b.bilan.txt`) : G2-27 (smoke, port 443 en dur),
  G2-28 (capture, port 443 en dur), G2-29 (capture, `tls=None`) : **3 vivants** ; relevé `ps` vide (8 groupes).
- Campagne g2c (arbre final + INT-P2-17 ; `mutants/g2c.bilan.txt`) : G2-23, G2-24, G2-27, G2-28, G2-29 : **5 tués par
  leur test visé** (1 FAIL, 0 ERROR chacun) ; relevé `ps` vide (12 groupes). C-2 seul (sans C-1), en essai de modules :
  G2-27 à G2-29 tués (`preuves/rouge-c2-seul.txt`) ; C-1 seul : G2-23 et G2-24 tués (`preuves/rouge-c1.txt`).
- Total cité : 59 runs de mutants classés par la commande du job (51 + 3 + 5), diff, sortie et classement de chacun
  sous `mutants/g2/`, `g2b/`, `g2c/` (`<id>.diff`, `<id>.out`, une ligne JSON par run dans `<campagne>.txt`).

## 7. Sécurité et robustesse (point 7) : CONFORME AVEC C-1

`outils/hostile.py` (`preuves/hostile.txt`) : 10050 corps hostiles sur les 36 décodeurs de la table (profondeur 10^5, nombres
géants, `NaN`, `Infinity`, octets non UTF-8, chaînes de 10^6 chiffres, chaque feuille de chaque fixture remplacée par
une valeur hostile) : 0 exception sortie de `decoder`, 0 décodage de plus d'une seconde, aucun prix autre que celui
d'origine ou la valeur injectée. Seul relevé hors attente : `binance_btc` rend `ok` un prix de 10^6 chiffres que le
corps porte (fini, dans les bornes de CONTEXTE, sous VALEURS) : pas un prix faux. `capture` : nom
`[a-z0-9_][a-z0-9_.-]{0,63}` préfixé du rôle, aucune barre ni traversée possible (`../x`, `.x` refusés, testés) ; écrasement après le
contrôle : C-1. Aucune adresse d'hôte dans les décodeurs (test `test_aucun_hote_en_dur_dans_les_decodeurs` et
recherche du §3).

## 8. Items de l'annexe B (point 8)

Fermés, test nommé présent dans la série : SHOGEN-S2BIS-DECODEURS-TYPES-1
(`test_decodeurs_actifs.Types.test_conteneur_remplace_jamais_une_autre_valeur`, INT-P2-01) ; SHOGEN-S2BIS-FORMES-BTC-1
(`test_formes_pool.Formes.test_requete_btc_de_s2_gardee`, INT-P2-06) ; SHOGEN-S2BIS-CURVE-DOC-1, fermé avec limites
(`test_temoin.Curve.test_limites_de_la_lecture_declarees`, `test_format.Format.test_paragraphe_9_limites_de_la_lecture_curve`,
INT-P2-11) ; I-1 de P2C (pas d'item) : `test_decodeurs.Bornes.test_aucune_horloge_dans_la_classe` (INT-P2-12).

Items à former ou à mettre à jour au versement (règle PAROXYSME ; recherche dans `ANNEXE-B-items.md` seul) :
- I-1 **SHOGEN-S2BIS-TEMOIN-BLOC-1** et I-2 **SHOGEN-S2BIS-OKX-CARNET-VIDE-1** : absents de l'annexe B (aucune ligne) ;
  l'adjudication de la tranche D les fait former au versement de P2, celle de l'intégration date leur fermeture à la
  première capture réelle d'un observateur (DEPLOI DB-2) : à écrire avec ce déclencheur.
- Mises à jour : SHOGEN-S2BIS-TLS-REUSSI-1 (l.1052, déclencheur encore `smoke CB-16 (poignée réelle)`) et
  SHOGEN-S2BIS-FORMES-DOC-1 (l.1271, `gel de formes.json`) : re-datés à DB-2 par l'adjudication, l'annexe ne le dit
  pas encore ; SHOGEN-S2BIS-HORODATAGE-SENS-1 (l.1272) : la lecture du 2026-10-17 (`s2bis/formes-doc/`) en donne le
  matériau, état à adjuger hors de cette série.
- Proposés par cette relecture :
  - I-3 SHOGEN-S2BIS-TEMOIN-RECALC-1 : le refus `ANALYSE/temoin` ne vaut que pour `analyse.json` ; les relevés du
    témoin portent `actif` `USDC` : la fusion et le re-décodage de RB-2 doivent les tenir hors de la classe USDC/USD
    (filtre sur `classe`, test nommé) ; déclencheur : G0 de RB-2.
  - I-4 SHOGEN-S2BIS-NOM-FORME-1 : `capture` refuse un nom hors de `[a-z0-9_][a-z0-9_.-]{0,63}`, `formes.json` et
    `carte.json` l'admettent (`nom` : texte de 1 à 64 caractères) ; le smoke imprime le nom tel quel (un saut de ligne
    y fausserait la sortie) ; règle de forme `nom-forme` à poser au gel ; déclencheur : gel du collecteur
    (SHOGEN-S2BIS-CONFIG-PRODUCTION-1).
  - I-5 SHOGEN-S2BIS-CAPTURE-PARTIELLE-1 : une erreur d'écriture au milieu d'une capture laisse des fichiers sans
    manifeste, et la relance est refusée (`fichier`) ; à déclarer ou à reprendre avant la première capture réelle ;
    déclencheur : DB-2.
  - I-6 SHOGEN-S2BIS-ENREG-ROLE-1 (existant, rappel) : cette relecture n'enregistre pas son rôle par
    `oracle_record.py`, qui ne couvre pas s2bis ; le brief ne le demande pas.

## 9. Observations (non bloquantes)

- O-1 : `okx_usdc_usdt.bin` ne porte que les champs lus (instType, instId, last, askPx, bidPx, ts) de la forme de l.47,
  toutes valeurs mesurées (l.87) ; les autres fixtures OKX portent la forme entière avec des valeurs construites.
  Choix défendable (aucune valeur inventée) ; la forme entière viendra de la capture (FORMES-DOC-1).
- O-2 : capture réelle Gemini v1 `usdtusd` du lecteur formes-doc : clés `USD`, `USDT`, `timestamp` ; fixture
  `gemini_usdt` : mêmes clés, autre ordre (sans effet sur le décodeur).
- O-3 : octet 92 non déclaré au rapport de l'intégrateur pour INT-P2-15 (66, échappements JSON des corps du témoin dans
  `formes-pool.json`) et INT-P2-16 (1, `\n` du manifeste, octets `\` `n` contrôlés par `od -c`) ; octets justes.
- O-4 : `smoke.CRYPTOCOMPARE` nomme un hôte dans le code (URL de S2, FORMAT §18) : hors des décodeurs, admis.
- O-5 : l'adjudication de la tranche D (Q-4) dit `les autres mots valent zéro` ; la fixture `slot0` porte 0, 180, 0
  et 1 (rapport de P2D, Q-4) : paraphrase inexacte de l'adjudication, sans effet.
- O-6 : `test_decodeurs_actifs.Places` a deux lignes vides entre deux méthodes (forme).

## 10. Contrôles de l'arbre final et des corrections

Chaîne `outils/fin.sh` (`preuves/fin.log`), arbre final = extraction neuve de 2a07ae6 + les seize diffs :
- runner `verdict-suite-s2 : 153 ok, 0 échec` ; S2 (`--egal`) `conforme (code 0, résumé final, sauts nommant
  SHOGEN_S2_CAMPAGNE_CONTROL, Ran = 423)` ; sim-bis (objets git du dépôt réel par `GIT_DIR`, sans verrou) `conforme
  (code 0, résumé final, aucun saut, Ran = 279)` ; s2bis : `Ran = 430` conforme (§1).
- Matrice `-I -B -X dev -W error` sous python3.10, 3.11, 3.12, 3.13 : `Ran 430`, `OK`, 0 ligne `Warning`, 0 ligne
  `Exception ignored`, code 0 ; la ligne du job conforme sous chacune (`preuves/matrice-final-*.txt`,
  `matrice-job-final-*.txt`). Même matrice sur l'arbre corrigé par INT-P2-17 : `Ran 431`, mêmes critères
  (`matrice-corr12-*.txt`).
- `__pycache__` : 0 (contrôle `test -e` sur les 25 dossiers de code de 2a07ae6, liste `git ls-tree -d` limitée à
  `s2bis`, `s2-harness`, `scripts/sim-bis`, `enforcement`, et sur les deux dossiers de fixtures neufs ; aucune recherche
  récursive), sur l'arbre final et sur l'arbre corrigé.
- `cargo --locked xtask verify` (cible cargo par défaut de chaque arbre, aucun `CARGO_TARGET_DIR`, réseau isolé ;
  lignes de verdict seules, sortie brute non lue et effacée) : arbre final, témoin (extraction neuve de 2a07ae6) et
  arbre corrigé (final + INT-P2-17 + C-3) : verdicts identiques (`cmp`) : S-G1 à S-G8, `cargo fmt --check`, `no_std`,
  `cargo clippy -D warnings` VERT ; S-G9 ROUGE d'une violation dans les trois (déjà sur 2a07ae6 : le cas connu des
  copies) ; les textes des corrections n'ajoutent aucune violation (S-G4, S-G5 verts).
- Arbre corrigé (final + INT-P2-17 + C-3) : job `Ran = 431` conforme (`preuves/job-corr123.txt`).
- Dépôt réel : tête `2a07ae6f2baecc662b3eda9594fdeee50c296e6a` à l'ouverture et à `18:36:25` UTC ; `git status --short`
  vide sur `.github/workflows/gates.yml`, `docs/adr-0029/s2bis`, `s2bis`.

## 11. Journal G1 (provenance)

**Sources lues** (sha256 des octets lus ; dépôt à 2a07ae6 ; `s2bis/` = `<scratchpad>/s2bis/`) :
- [lu] en entier : brief (`2291296a…701962`) ; `int-p2/RAPPORT-INTEGRATEUR.md` (`d0a5c484…757765`), `pas.tsv`
  (`cbf3d67b…b93a4`), `source-pas.md` (`bf885f51…a2416`), `ADJUDICATION.md` (`95973e23…a7a15`) ; rapports des
  générateurs `p2c/RAPPORT-GENERATEUR.md` (`bc5fc99b…5a37c9`), `p2d/RAPPORT-GENERATEUR.md` (`b1efb433…ef787f2`) et leurs
  adjudications (`ef2d1465…c45ade`, `2fe61d21…01dae5`) ; lectures `curve-doc/RAPPORT-LECTEUR.md` (`b4ac15c0…510140`),
  `formes-doc/RAPPORT-LECTEUR.md` (`820ee7ad…b05834`) ; les seize diffs (sha256 au §1) et le code et les tests finals
  touchés (`decodeurs.py`, `smoke.py`, `capture.py`, `entree.py`, `lecture.py`, `http.py`, `test_decodeurs_actifs.py`,
  `test_temoin.py`, `test_formes_pool.py`, `test_smoke.py`, `test_capture.py`), `formes-pool.json`, les fixtures neuves ;
  G0 `docs/adr-0029/g0-collecte/G0-COLLECTE-RECALC-DEPLOI.md` (`08c1e6b0…8ec691d`) ; pièce
  `docs/adr-0029/g0-calib/PAIRES-ET-TEMOIN.md` (`75535ad5…dc1258b`).
- [lu] en partie : PROPOSITION du G0 de collecte (`0cdf84c2…5fbfd0`) l.160-172, l.194-202, l.215-224, l.255-285,
  l.330-370 ; AVIS (`a919b307…1616ce`) lignes de Q-C-05, Q-C-10, Q-C-14 et du smoke (recherche dans ce seul fichier) ;
  ADR-0029 (`32a59893…aa2801`) l.81, l.98, l.166-175, l.222-225, l.234, l.236 ; AVIS de CALIB-ACTIFS (`6deaf8cd…60f1b8`)
  lignes de Q-CA-01, Q-CA-07, Q-CA-09, Q-CA-10 ; FORMAT final (base `799c8291…f5a6`) en-tête l.50-81, §9.1, §14.1,
  §18, §19 ; annexe B d'ADR-0028 (`ff6b4f47…d383f4f9`) par recherche dans ce seul fichier (l.1052, l.1271-1275, l.1306,
  l.1313) ; `config_analyse.py` (diff INT-P2-10) ; `scripts/controle/mutants.py` (`3e218783…abddad64`) docstring ;
  `p1b/g2/travail/outils/isole.sh` ; outils de l'intégrateur (`extraire.sh`, `serie.sh`, `job.sh`, `essai.sh`,
  `matrice.sh`, `gates.sh`, `xtask.sh`, `campagne.sh`, `bilan.py`, `m16.py`) ; captures `formes-doc/captures/R1-gemini-v1-
  {usdtusd,btcusd}.json` (clés seules).
- [2nd] valeurs mesurées des sources (prix, instants, adresses) : celles de la pièce (lecteur `claude-sonnet-5-5`),
  non re-mesurées ; documentation Curve : par le rapport du lecteur.
- [abs] tout essai réseau (smoke réel, poignée TLS, capture réelle) : interdit.

**Commandes et sorties** (horodatées dans `NOTES.md`) : série et planchers (`preuves/serie.txt`, `etats-job.log`) ;
rebasage (`compare-rebase.txt`) ; rouges (`rouge-10-11.txt`, `rouge-12-16.txt`, `rouge-c1.txt`, `rouge-c2-seul.txt`) ;
Bornes (`ast-bornes.txt`, `ast-bornes-avant-apres.txt`, `bornes-dix.txt`) ; corps hostiles (`hostile.txt`) ;
sélecteurs et EIP-55 (`selecteurs.txt`) ; forme des diffs (`forme-diffs.txt`) ; METRIQUES (`metriques-lignes.txt`) ;
campagnes (`mutants/g2*.txt`, `.bilan.txt`, `.log`, `.err`, dossiers) ; gates, matrice, xtask (`fin.log`, `final-*.txt`,
`matrice-*.txt`, `xtask-*-verdicts.txt`, `job-corr12.txt`, `job-corr123.txt`).

**Chiffres recomptés** : planchers par la sortie `Ran =` du vérificateur ; lignes de code ajoutées par diff (lignes `+`
des `.py` et `.yml`, script du réviseur) ; lignes et tests de METRIQUES par `wc -l` et `    def test_` sur chaque état
(`metriques-lignes.txt`, 0 écart) ; mots de Chainlink et d'Uniswap par Python (Decimal, 60 chiffres) ; sélecteurs par
Keccak-256 écrit pour la relecture ; sha256 des fixtures par `sha256sum` ; décodeurs (36) et lectures par actif par
script sur la table et `formes-pool.json`.

**Outils du réviseur** (`g2/outils/`, hors dépôt) : `extraire.sh`, `serie.sh`, `job.sh`, `etats.sh`, `essai.sh`,
`rouge.sh`, `compare_hunks.py`, `ast_bornes.py`, `horloge_lente.py`, `hostile.py`, `keccak.py`, `liste_g2.py`,
`campagne.sh`, `bilan.py`, `fin.sh`, `faire_diff.sh`, `poser_c1.py`, `poser_c2.py`, `poser_17.py`, `poser_c3.py`.

**Écarts** : E-1, commande refusée par le crochet `garde_faits` avant exécution (attente d'avant-plan ; puis un `pgrep`
non ancré), refaite dans la forme admise ; E-2, une plage horaire de NOTES écrite avant la lecture de l'horloge,
corrigée ; E-3, des noms de mutants entre guillemets français dans mes sections METRIQUES, retirés avant remise (diffs régénérés et
re-vérifiés) ; E-4, liste des dossiers de code par `git ls-tree -d` limité à quatre chemins nommés (pour le contrôle
`__pycache__` sans recherche récursive) ; E-5, essais de modules (moins de 15 s chacun : rouges, Bornes, C-1, C-2) lancés
pendant les campagnes, comme l'intégrateur ; une seule campagne ou suite lourde à la fois.

**Nettoyage** : copies lourdes effacées (`g2/travail/`, extraction de l'outil, cibles cargo) ; aucun processus du
réviseur ne tourne (relevé `ps` à `18:36:25` UTC) ; restent `NOTES.md`, ce rapport, `diffs/`, `mutants/`, `preuves/`,
`outils/`, `SHA256SUMS`.
