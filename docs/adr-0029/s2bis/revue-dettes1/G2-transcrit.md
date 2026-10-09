# Relecture G2 neuve de DETTES-T1 (transcrit)

> Transcription par l'orchestrateur le 2026-10-09 14:56:18 UTC du fichier g2/RAPPORT-G2.md ; contrôle FM-1.1 des transcripts du générateur-correcteur, du réviseur et du contre-contrôleur : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Relecture G2 neuve du lot DETTES-T1 (GM-1 : SHOGEN-TESTS-GARDE-MANDATAIRE-1 ; BM-1 : SHOGEN-CALIB-BORNE-MULTI-1)

Le 2026-10-09, de 11:57 à 12:36 UTC (`date -u`). Réviseur G2 neuf : je n'ai écrit aucun des diffs relus.

## Gate 0

- Modèle résolu : `claude-opus-5-5`, identifiant donné par l'environnement de la session. L'effort ne se vérifie pas
  depuis la session.
- Dépôt réel en lecture seule, toujours avec `--no-optional-locks` : aucune écriture git, aucun commit, aucun push.
- `SHOGEN_S2_CAMPAGNE_CONTROL` n'a jamais été posée ; la sonde le vérifie (`posee : False`).
- Aucune clé ni aucun secret lu. Rien sur Pocket. Aucune lecture interdite : `git archive` exclut les sept chemins.

## Verdicts

| dette | diff | verdict |
|---|---|---|
| A | `diffs/GM-1.diff` | **ACCEPTE-AVEC-CORRECTIONS** : C-A1 |
| B | `diffs/BM-1.diff` et `diffs-tete/BM-1.diff` | **ACCEPTE-AVEC-CORRECTIONS** : C-B1 à C-B4 |

Dans les deux dettes, le code est juste. Les corrections portent sur les **tests** : quatre de mes mutants y survivent
(MA01, MB01, MB03, MB10). La cinquième correction, C-B4, répond à Q-DT-2. Chaque correction donne le mutant qui la
prouvera. Pour C-A1, C-B1, C-B2 et C-B3, la forme proposée est **déjà vérifiée sur copie** : vert sur le code du lot,
rouge sur l'ancien, mutant visé tué (§4).

## 1. Contrat lu, puis sonde écrite avant le code

- **Dette A**, sources lues :
  - `calib3/ADJUDICATION-G2.md`, avec ses trois ajouts datés. Le dernier ajout reçoit O-CC-2 et le renvoie vers
    l'item SHOGEN-CALIB-BORNE-MULTI-1. L'item MANDATAIRE-1 est adopté dans le corps et dans l'ajout de 09:59.
  - `calib3/g2/RAPPORT-G2.md` §3.4, §5 (C-3) et §9.
  - La forme de C-3 dans `snap/CA-6e/scripts/calib-actifs/tests/`. `__init__.py` purge à l'import. Dans
    `test_pages.test_garde_reseau`, un sous-processus pose quatre variables fictives, importe `tests` et lit
    `getproxies()`.
- **Dette B**, sources lues : O-CC-2 et la ligne C-13 de `calib3/g2/cc/RAPPORT-CC.md` ; C-13 dans
  `calib3/RAPPORT-GENERATEUR.md` §11.
- **Sonde** `g2/outils/sonde.py`, écrite avant toute lecture de code. Lancée sous `g2/outils/run.sh` (copie de
  `dettes1/outils/run.sh` : `env -u` des huit variables, puis `isole.sh` et `TMPDIR=g2/tmp`) :
  - 1.1.1.1:443 et 8.8.8.8:53 : errno 101 ;
  - `getaddrinfo("example.com")` : gaierror ;
  - `urlopen` http et https : URLError ;
  - mandataire du harnais 127.0.0.1:36573 : errno 111.

  La sonde de fin (12:34) donne des résultats identiques (`travail/sonde-1.out`, `travail/sonde-fin.out`).
- **Bibliothèque standard** : j'ai lu `getproxies_environment` dans `/usr/lib/python3.1{0,1,2,3}/urllib/request.py`
  (3.10.20, 3.11.15, 3.12.3, 3.13.14). Sur Linux, `getproxies` est `getproxies_environment`.
  - Un nom est retenu si `name[-6] == "_"` et `name[-5:].lower() == "proxy"` (3.10, 3.12, 3.13), ou si
    `name.lower()[-6:] == "_proxy"` (3.11).
  - La clé est le préfixe mis en minuscules. **Le préfixe et le suffixe peuvent donc avoir n'importe quelle casse.**
  - Le reste n'agit pas ici : `REQUEST_METHOD` retire `http`, une valeur vide est ignorée, et la seconde boucle retire
    les clés vides.

## 2. Pièces du générateur

- `sha256sum -c SHA256SUMS` du dossier : **57 OK, 0 échec**.
- Les sha256 des diffs sont recomptés et égaux au rapport :
  - GM-1 `74686277…e6ad` ;
  - BM-1 série `f3b409aa…2e92` ;
  - BM-1 tête `eaaff515…b3f7`.
- `RAPPORT-GENERATEUR.md` a été lu comme une donnée. Ses chiffres repris ici sont tous recomptés.

## 3. Bases (consignées)

- **Tête du dépôt** : `9d5d592` (CA-5e). L'index du dépôt n'est pas vide, car la chaîne de commits est en cours : il
  est ignoré, seul `HEAD` est archivé.
- **`travail/tete`** : `git archive HEAD`, avec les sept exclusions (`docs/rapports`, `docs/adr-0025`,
  `docs/adr-0028/monark-m009a`, `docs/adr-0028/execution`, `docs/15-*`, `docs/16-*`, `docs/pocket-report`). Leur
  absence a été contrôlée.
- **A = tête + GM-1** : `patch` propre.
- **Bt** (version de tête) :
  - tête + `calib3/diffs-tete` CA-6a à CA-6e : 5 diffs sur 5. Le lot est égal à `snap/CA-6e` (`diff -r` vide), avec le
    plancher 64 ;
  - puis `diffs-tete/BM-1` : propre. `SHA256SUMS` du lot : 29 sur 29 OK, et sa liste est égale aux fichiers du lot.
- **Bs** (version de série) :
  - `git archive ebd1560`, avec les mêmes exclusions, + `calib3/diffs` CA-0a à CA-6e : 21 diffs sur 21, égal à
    `snap/CA-6e` ;
  - puis `diffs/BM-1` : propre. Le lot de Bs est égal à celui de Bt (`diff -r` vide).
  - Ligne du job : conforme, Ran 65.
  - Les deux BM-1 ne diffèrent que par la ligne `index` et le `@@` de `gates.yml`.
- **AB = Bt + GM-1** : propre. Les hunks de `gates.yml` sont disjoints (l.220 pour s2bis, l.269 pour calib).
- J'ai relu les trois diffs en entier, ainsi que les fichiers touchés après application (`tau.py` en entier, et
  `socle.regle`, `quantile`, `Refus`).

## 4. Contrôles

### 4.1 Rouge d'assertion des tests neufs (sous `env -i`, isolé)

- **A**, `travail/rougeA.out` : GM-1 sans la purge (l'`__init__.py` de la tête). On obtient un FAIL d'assertion de
  `test_mandataires_purges`, sortie `['all', 'http', 'https'] [7 noms]`. Les deux autres tests de `test_garde` sont ok.
- **B**, `travail/rougeB.out` : BM-1 avec le `tau.py` de CA-6e. On obtient 2 FAIL d'assertion, 0 ERROR :
  - `test_borne_plusieurs` : la ligne USDT manque ;
  - `test_borne_valeur` : les lignes USDC et USDT manquent.

### 4.2 Dette A : indépendance de l'environnement et formes de nom

- **Sous `env -i PATH=/usr/bin:/bin HOME=/root TMPDIR=…`** (isolé), l'environnement ne contient que `HOME`, `PATH`,
  `PWD` et `TMPDIR`. Aucun mandataire n'y est posé.
  - Rouge : FAIL d'assertion (§4.1).
  - Vert : ligne du job conforme, Ran 341 (`travail/vertA-envi.out`).
  - Toute ma campagne A (§5) tourne sous `env -i`. Le test du remède ne dépend donc pas de l'environnement.
- **Formes de nom** (`g2/outils/formes.py`, sous 3.10 à 3.13, `env -i`, isolé ; `travail/formes.out`) :
  - les **512** casses de `http_proxy` (neuf lettres) sont toutes lues par `getproxies` ;
  - l'échantillon https et all est lu 10 fois sur 10 (majuscules, minuscules, titre, alternées, suffixe seul) ;
  - `http_proxyx`, `http-proxy` et `httpproxy` ne sont pas lus ;
  - après `import tests` (GM-1, et C-A1), aucune clé ne reste et aucun nom ne reste.

  **La purge couvre toutes les formes lues.**
- **Le test, lui, ne couvre pas toutes les formes.** Ses sept noms sont les majuscules, les minuscules et
  `Https_Proxy`. La casse mêlée n'y figure que pour https, et seulement sous la forme titre.
  - Mon mutant MA01 (purge par liste des formes majuscules, minuscules et `str.title`) **VIT**. Avec lui, `hTtP_pRoXy`
    reste lu par `urllib`.
  - Correction : C-A1.

### 4.3 Dette B : valeurs à la main, et refus écrit inchangé

**Valeurs à la main de `test_borne_plusieurs`.** Les sources sont `socle.regle`, `socle.quantile`, `tau.ecarts` et
`places`, ainsi que `parametres.json` et `synthetiques.FEN`.

- La fenêtre fait 1775260500 à 1775261100, soit 600 s ou 10 minutes : 5 minutes le vendredi (strate calme), puis 5 le
  samedi (stress).
- Les deux actifs ont six places et `n_min` 4.
- N = 6 × 5 = 30 par strate. Le rang vaut ⌈999·30/1000⌉ = 30, c'est-à-dire le maximum.
- Écarts : okx a e = |102 − 100| / 100 = 2/100 (ETH) ou 3/100 (USDT). Les autres places ont une médiane
  leave-one-out de 100 sur cinq valeurs, d'où e = 0.
- k = ⌈1,5 × e / 0,0005⌉ = 60 et 90. On a k_haut = ⌈0,0285 / 0,0005⌉ − 1 = 56, donc refus.
- Valeur = `Decimal(k) × Decimal("0.0005")`, soit **`0.0300`** et **`0.0450`**. C'est égal au test.
- Valeurs de ma proposition C-B3 : okx à 103 donne 0.0450. Six places à 100 donnent k = 0 < k_bas = 1 : borne basse,
  aucun refus. Le τ des agrégateurs vaut alors ⌈0,0005 × 0,0265 / 0,0050⌉ à la grille = 0,0030 < 0,0285, aucun refus.

**Refus écrit = celui de l'ancien arrêt au premier.** Je l'ai vérifié avec un différentiel
(`g2/outils/differentiel.py`, `travail/differentiel.out`) :

- il oppose `tau.main` de CA-6e à celui de BM-1 ;
- il couvre **64 combinaisons** d'issues par actif (ok, CA/borne à valeur, CA/population, `ZeroDivisionError`),
  injectées dans `calcul_actif` ;
- il exige le même code, la même ligne de refus et le même JSON ; les lignes hors de BM-1, une par refus à valeur et
  dans l'ordre des actifs ; et la ligne hors de CA-6e égale à la première de BM-1 quand le premier refus porte une
  valeur.

Résultat : **0 écart**. Le témoin (`tau` = CA-6e) donne **24 écarts** (`travail/differentiel-temoin.out`) : le script
discrimine. Une réserve, que traite C-B1 : la suite du lot ne fige pas ce fait pour un refus unique (MB03 vit).

**Q-DT-4 vérifié.** Une valeur ne naît que dans `places` (l.66) et `agregateurs` (l.86).

- Les appels hors de la boucle sont :
  - `controle_fragment` l.135 : il rejoue `agregateurs` sur un τ déjà admis, avec la même valeur (Decimal de sa chaîne)
    et les mêmes entrées ;
  - `descriptifs` l.189 et `septembre` : ils captent `socle.Refus`.
- Le repli `refus or [r]` était donc mort.

### 4.4 Matrice (AB, `-X dev -W error`, `PYTHONDEVMODE=1`, `PYTHONWARNINGS=error`, sous `env -i`, isolé)

| python | s2bis (plancher 341) | calib-actifs (plancher 65) |
|---|---|---|
| 3.10.20 | code 0, Ran 341, 0 « Exception ignored », 0 « Warning » | code 0, Ran 65, 0, 0 |
| 3.11.15 | code 0, Ran 341, 0, 0 | code 0, Ran 65, 0, 0 |
| 3.12.3 | code 0, Ran 341, 0, 0 | code 0, Ran 65, 0, 0 |
| 3.13.14 | code 0, Ran 341, 0, 0 | code 0, Ran 65, 0, 0 |

### 4.5 Batteries (AB, une suite à la fois, sous `env -i`, isolé ; `travail/lot_lourd.log`)

- **calib-actifs** : conforme, Ran 65.
- **runner** : 136 ok, 0 échec.
- **S2** (`--egal`) : conforme, Ran 415, sauts nommant la variable.
- **s2bis** :
  - premier passage : **REFUS**, 1 ERROR dans `test_dns.test_drapeau_tc_garde_section_reponse_non_lue`
    (`OSError` 98 `EADDRINUSE` au bind TCP du numéro de port UDP) ;
  - rejeu : conforme, Ran 341 (`travail/batterie_s2bis-2.out`) ;
  - ce test n'est pas touché par le lot : O-6.
- **Bs** (série, plancher 65) : conforme, Ran 65.

### 4.6 xtask (lignes VERDICT seules ; sortie brute dans `g2/tmp`, jamais lue, effacée)

- Tête et AB donnent 10 lignes **identiques** (`diff` vide) : 8 VERT, la 9e ROUGE (1 violation) et le global ROUGE.
- La 9e ligne est identique sur la tête, donc préexistante.
- AB est aussi identique, au `cmp`, au fichier `xtask-AB-verdicts.txt` du générateur.

### 4.7 Forme

| contrôle | GM-1 | BM-1 (série et tête) |
|---|---|---|
| lignes (recomptées) | +25 / −2 | +60 / −16 |
| octets 92 (diffs et fichiers touchés) | 0 | 0 |
| plus longue ligne | 120 (≤ 120) | 120 (≤ 120) |
| `TODO` / `FIXME` | 0 | 0 |
| tabulations | 0 | 0 |
| fin de fichier | LF | LF |

- R-25 : deux diffs petits et unitaires, un par item.
- Les sauts et `expectedFailure` neufs sont absents, et le lot n'ajoute aucune dépendance.
- `SHA256SUMS` du lot calib : recalculé juste.

## 5. Mutants du réviseur

Méthode (`g2/outils/mutants_g2.py`) :

- chaque mutant tourne sur une copie jetable de la racine entière ;
- la substitution est exacte, avec une seule occurrence ; sinon le mutant est INVALIDE ;
- la commande est la ligne exacte du job (`--aucun-saut --egal --plancher 341`, ou `65`), sous `run.sh env -i`, dans
  une nouvelle session ;
- borne 300 s par `killpg`, PAR = 2 ;
- classement : sortie 1 = TUÉ, 0 = VIVANT, toute autre sortie ou la borne = FATAL ;
- `ps` de fin vide.

**Dette A** (racine A ; campagne n.2, PID 16863, de 12:17 à 12:21 ; la campagne n.1 est invalide, voir E-G2-3) :
**11 TUÉS, 1 VIVANT, 0 FATAL, 0 INVALIDE**. Le témoin MA00 est VIVANT (Ran 341).

| id | mutation | classe | par |
|---|---|---|---|
| MA01 | purge par liste : majuscules, minuscules, `str.title` | **VIVANT** | → C-A1 |
| MA02 | `os.putenv(_v, '')` au lieu de `del os.environ` | TUÉ | FAIL `test_mandataires_purges` |
| MA03 | majuscules seules (`k.isupper()`) | TUÉ | idem |
| MA04 | liste exacte en minuscules et majuscules | TUÉ | idem |
| MA05 | `os.environ.pop(_v.lower(), None)` : formes minuscules seules retirées | TUÉ | idem |
| MA06 | suffixe `_proxy` ou `_PROXY` seulement | TUÉ | idem |
| MA07 | purge dans une fonction jamais appelée | TUÉ | idem |
| MA08 | `all-proxy` au lieu de `all_proxy` | TUÉ | idem |
| MA09 | arrêt après la première variable | TUÉ | idem |
| MA10 | casse de titre exclue | TUÉ | idem |
| MA11 | minuscules seules (`k.islower()`) | TUÉ | idem |
| MA12 | `https_proxy` seul | TUÉ | idem |

**Dette B** (racine Bt ; PID 23385, 12:21 à 12:23) : **9 TUÉS, 3 VIVANTS, 0 FATAL, 0 INVALIDE**. Le témoin MB00 est
VIVANT (Ran 65).

| id | mutation | classe | par |
|---|---|---|---|
| MB01 | lignes hors seulement si le refus écrit porte une valeur | **VIVANT** | → C-B2 |
| MB02 | refus écrit = minimum des refus par texte | TUÉ | FAIL `test_borne_plusieurs` |
| MB03 | refus unique non levé (`if len(refus) > 1`) | **VIVANT** | → C-B1 |
| MB04 | une ligne par valeur distincte | TUÉ | FAIL `test_borne_valeur` |
| MB05 | USDT jamais calculé | TUÉ | 4 FAIL |
| MB06 | actifs parcourus à l'envers | TUÉ | 3 FAIL |
| MB07 | valeur imprimée en flottant | TUÉ | FAIL `test_borne_plusieurs` |
| MB08 | lieu du refus écrit sur chaque ligne | TUÉ | 2 FAIL |
| MB09 | calcul arrêté au deuxième refus | TUÉ | 2 FAIL |
| MB10 | lignes triées par valeur croissante | **VIVANT** | → C-B3 |
| MB11 | valeurs versées au JSON | TUÉ | FAIL `test_borne_plusieurs` |
| MB12 | lignes hors avant le refus | TUÉ | 2 FAIL |

**Effet de MB03.** Je l'ai rejoué avec un seul actif refusé, USDT à la borne (`travail/mb03.out`). Le refus écrit
devient `REFUS CA/calcul : calcul en échec (KeyError)` au lieu de `REFUS CA/borne … ; actif USDT`. C'est le cas le plus
courant au lancement, et rien ne le fige dans la suite.

**Preuve des corrections, sur copie** (`g2/outils/test_propose_B.py`). Ce fichier remplace le corps de
`test_borne_plusieurs` par cinq passes ; Ran reste 65.

- Résultat sur BM-1 : vert.
- Résultat sur le `tau.py` de CA-6e : 2 FAIL.
- J'ai rejoué toute la campagne B sur cette copie (PID 675) : **12 TUÉS sur 12**, MB01, MB03 et MB10 compris, et MB00
  VIVANT (`travail/mutants_B_propose.*`).
- Pour C-A1, avec trois noms ajoutés :
  - vert sur GM-1 ;
  - MA01 TUÉ (FAIL : `aLl_pRoXy`, `hTtP_pRoXy`, `hTtPs_PrOxY` restent) ;
  - rouge sur l'`__init__.py` de la tête (`travail/propose_A_*.out`).

## 6. Corrections (liste fermée)

- **C-A1** (faible) : ajouter aux noms de `test_mandataires_purges` des formes de casse mêlée pour **chacun** des trois
  schémas, hors forme titre (par exemple `hTtP_pRoXy`, `hTtPs_PrOxY`, `aLl_pRoXy`). Il faut ajuster la docstring
  (« sept variables ») et rester à 120 colonnes au plus.
  - Preuve : MA01 TUÉ par FAIL ; MA02 à MA12 toujours TUÉS ; vert à Ran 341 sous `env -i`.
- **C-B1** (moyenne) : figer le cas d'un **seul** actif refusé dans la boucle. Exemple : ETH à 100 sur six places,
  USDT avec okx à 103. Attendu : refus `REFUS CA/borne … ; actif USDT`, une seule ligne `0.0450 ; actif USDT`, JSON
  `{"etiquette", "refus"}`, code 1.
  - Preuve : MB03 TUÉ par FAIL.
- **C-B2** (faible) : figer le cas d'un premier refus **sans valeur** suivi d'un CA/borne. Exemple : ETH en
  CA/population, par injection ou par données, et USDT avec okx à 103. Attendu : le refus d'ETH écrit, puis la seule
  ligne `0.0450 ; actif USDT`.
  - Preuve : MB01 TUÉ par FAIL.
- **C-B3** (faible) : l'ordre des lignes doit être distingué de l'ordre des valeurs. Il faut une passe où l'actif
  premier a la plus grande valeur, par exemple ETH à 103 et USDT à 102, soit ETH 0.0450 puis USDT 0.0300. La passe
  existante, ETH 0.0300 puis USDT 0.0450, tue déjà le tri décroissant.
  - Preuve : MB10 (tri croissant) TUÉ par FAIL.
- **C-B4** (faible ; suit mon avis sur Q-DT-2, et l'orchestrateur peut la rayer en le refusant) : après les lignes de
  valeur, une ligne descriptive par refus **suivant** qui ne porte pas de valeur (`refus[1:]` sans `valeur`). Forme
  proposée : `descriptif hors refus (jamais décisif) : refus suivant : <texte du refus>`.
  - Le texte est nommé, sans valeur (§5.7). Une exception non nommée devient `CA/calcul : calcul en échec (<type>)`,
    jamais une trace.
  - Le refus écrit et le JSON restent inchangés.
  - Il faut ajouter une passe au test (ETH à la borne, USDT en CA/population) et une phrase au README.
  - Preuve : le mutant « refus suivants non imprimés » (= BM-1 actuel) est TUÉ ; le mutant « refus suivant imprimé
    avec le premier refus » est TUÉ ; MB02 et MB09 restent TUÉS.

À l'issue des corrections, il faut :

- recalculer `SHA256SUMS` du lot calib ;
- tenir un plancher exact : 65 si les passes entrent dans `test_borne_plusieurs`, 66 pour un test neuf ;
- produire les deux versions de BM-1 (série et tête) ;
- montrer le rouge de chaque passe neuve sur le `tau.py` de CA-6e, sauf C-B4, dont le rouge se montre sur BM-1.

## 7. Constats O-n

- **O-1** (moyenne) : MB03 vivant. Correction : C-B1.
- **O-2** (faible) : MB01 vivant. Correction : C-B2.
- **O-3** (faible) : MB10 vivant. Correction : C-B3.
- **O-4** (faible) : MA01 vivant. Le test ne couvre pas les formes de casse mêlée qu'`urllib` lit (§4.2). Correction :
  C-A1.
- **O-5** (information) : le code de `s2bis/shogen_s2bis` n'emploie pas `urllib`. Il passe par `http.client`
  directement (`collecte/http.py`, `collecte/tetes.py`), qui ne lit aucun mandataire. Le défaut corrigé par GM-1 était
  donc latent dans s2bis (défense en profondeur). La docstring (« ferait sortir urllib ») est exacte. Aucune action.
- **O-6** (faible, hors lot) : `s2bis/tests/test_dns.py`, `test_drapeau_tc_garde_section_reponse_non_lue` (l.237-238).
  - Le test lie en TCP le numéro d'un port UDP éphémère. Ce bind échoue en `EADDRINUSE` si une socket TCP de l'espace
    tient ce port.
  - Mesure : 1 échec sur 33 lancements complets de s2bis dans cette session, dans un espace réseau neuf.
  - Risque : un faux rouge de CI, et dans une campagne un faux « TUÉ ». Aucun de mes mutants n'en est touché : chaque
    mutant tué l'est par `test_mandataires_purges`, et seulement par lui.
  - Ligne d'item, à former si aucun item ne la porte : **SHOGEN-S2BIS-TEST-DNS-PORT-1**.
    - Constat : bind TCP sur un port UDP éphémère, flaky.
    - Propriétaire : orchestrateur, lot s2bis.
    - Déclencheur : prochain lot qui touche `s2bis/tests/`, au plus tard le gel du collecteur.
    - Prix : environ 5 lignes, avec un réessai sur un port libre dans les deux protocoles.
    - Origine : ce G2, §4.5.
- **O-7** (forme, faible) : le README de BM-1 dit « aucun fragment n'est écrit ». Or `fragment_analyse.json` est
  écrit, sous la forme `{"etiquette", "refus"}`. La phrase est juste au sens du fragment de valeurs, mais un lecteur du
  lanceur peut la prendre à la lettre. Forme suggérée, à faire si C-B4 retouche le README : « le JSON ne porte que le
  refus ».
- **O-8** (information) : après un premier refus, une `BaseException` (`KeyboardInterrupt`, `SystemExit`) levée sur un
  actif suivant sort désormais de `main` avec une trace. Avant, le calcul s'arrêtait au premier refus. Ce cas ne se
  produit que sous interruption. Aucune action.
- **O-9** (information) : la ligne de valeur d'un refus suppose que tout refus à valeur naisse dans la boucle (Q-DT-4,
  vérifié au §4.3). Un changement futur qui lèverait CA/borne hors de la boucle perdrait sa ligne sans bruit. À garder
  en mémoire pour le prochain lot qui touche `tau.main`.

## 8. Avis sur Q-DT-1 à Q-DT-4

- **Q-DT-1** (JSON de refus écrit) : **d'accord**.
  - §5.7 et `test_refus` veulent le même refus dans les deux sorties, et `lancer.sh` hache les deux fichiers.
    Supprimer le fichier changerait le contrat du lanceur, hors de l'item.
  - Le différentiel le confirme : le JSON est identique à celui de CA-6e sur les 64 combinaisons.
  - La lettre « le JSON n'est pas écrit » doit s'entendre « aucun fragment de valeurs ». Voir O-7 pour le README.
- **Q-DT-2** (refus suivant d'une autre famille) : **oui, une ligne « refus suivant » doit entrer dans ce lot** (C-B4).
  - Le but adjugé de C-13 et d'O-CC-2 est qu'une décision au lancement unique n'exige pas un second lancement. Un
    CA/population, CA/mediane ou CA/btc sur un actif suivant le contrarie exactement comme un second CA/borne. Après la
    décision, la relance le découvrirait, et il faudrait un troisième lancement.
  - BM-1 calcule déjà ces refus et les jette. Les imprimer coûte environ trois lignes et une passe de test.
  - Le texte d'un refus ne porte jamais de valeur : c'est compatible avec §5.7 et E-CA-25.
  - Le déclencheur est le même que celui de BORNE-MULTI-1 (avant l'épinglage). Le renvoyer à un item ouvrirait un
    cycle G2 de plus pour le même délai.
  - Si l'orchestrateur ne le veut pas dans ce lot, C-B4 est rayée et il faut former une ligne d'item : constat Q-DT-2 ;
    déclencheur : avant l'épinglage (E-CA-27) ; prix : environ 3 lignes et un test.
- **Q-DT-3** (`except Exception` par actif) : **d'accord**.
  - C'est la seule forme qui garde le refus écrit de l'arrêt au premier quand une exception non nommée survient sur un
    actif suivant.
  - Preuves : le différentiel (0 écart, avec `ZeroDivisionError` sur chaque actif) et le mutant B03 du générateur.
  - Limite : O-8.
- **Q-DT-4** (repli `refus or [r]` retiré) : **d'accord**. Le repli était mort (§4.3) : le remettre ferait un mutant
  équivalent. Aucune défense à rétablir ; O-9 garde la mémoire de l'invariant.

## 9. Écarts

**Écarts du générateur.**

- E-DT-1 (une barre oblique inverse, dans un outil) : admis.
- E-DT-2 (commande refusée, relancée par fichiers) : admis.
- E-DT-3 (la tête a avancé) : admis. J'ai vérifié que GM-1 s'applique sur `9d5d592`, et que la tête plus CA-6a à CA-6e
  plus BM-1 est propre.
- Sim-bis, hook et gate des secrets non lancés : admis, conformément à E-COR-3 (l'orchestrateur lance sim-bis avant le
  commit).

**Écarts du réviseur.**

- **E-G2-1** : une liste de fichiers a été écrite puis effacée dans `/tmp`, hors de `g2/`, par une commande de
  contrôle à 12:00.
- **E-G2-2** : une boucle d'attente `pgrep -f` se reconnaissait elle-même, et l'attente ne finissait pas. J'ai tué ces
  boucles. Le `kill` a aussi tué le shell de la commande (sortie 144), sans aucun effet sur le lot. Depuis, j'attends
  par `kill -0 <PID>`.
- **E-G2-3** : la campagne A n.1 (PID 31301) est invalide. Le témoin MA00 a été TUÉ par 16 ERROR `FileNotFoundError` :
  la copie jetable ne contenait ni `docs/adr-0029` ni `s2-harness`. Elle n'est pas comptée ; ses sorties sont sous
  `travail/invalide-1/`. L'outil est corrigé (racine entière copiée) et la campagne n.2 est complète.
- **E-G2-4** : le PID consigné pour le lot lourd (4547) était celui de `setsid`, qui a fourché. Le script tournait sous
  le PID 4548, que j'ai attendu.
- **E-G2-5** : le rejeu de la campagne B sur la copie corrigée a écrasé les `mut_MB*.out` de la première campagne B.
  Les `mutants_B.tsv` et `.log` de la première campagne restent.
- **E-G2-6** : au premier passage du différentiel, le succès comparait la ligne sha256, qui nomme le fichier et le
  `p.json` temporaire : c'était un artefact. Le script a été corrigé et rejoué : 0 écart. Le témoin a été lancé après.
- **E-G2-7** : une première extraction partielle de Bs (sans `docs/`) a fait refuser le job calib. Je l'ai refaite par
  `git archive` complet avec les exclusions : conforme, Ran 65.
- PID des processus lourds, un seul à la fois :

  | processus | PID |
  |---|---|
  | campagne A n.1 | 31301 |
  | campagne A n.2 | 16863 |
  | campagne B | 23385 |
  | campagne B proposée | 675 |
  | lot lourd | 4548 |
  | xtask | 18243 |

  `ps` de fin : vide. Copies lourdes et `g2/tmp` effacées.

## 10. Provenance (G1)

**Lus [lu] :**

- `calib3/ADJUDICATION-G2.md`, en entier ;
- `calib3/g2/RAPPORT-G2.md` §3.4, §5 (C-3) et §9 ;
- `calib3/g2/cc/RAPPORT-CC.md`, O-CC-2 et la ligne C-13 ;
- `calib3/RAPPORT-GENERATEUR.md` §11, la ligne C-13 et la ligne d'item MANDATAIRE-1 ;
- dans `snap/CA-6e` : `tests/__init__.py` et `test_pages.test_garde_reseau` ;
- `dettes1/RAPPORT-GENERATEUR.md`, `NOTES.md`, `outils/run.sh`, `batterie.sh`, `matrice.sh`, `xtask.sh` et les trois
  diffs ;
- `urllib/request.py` (`getproxies_environment`) de 3.10 à 3.13 ;
- `tau.py` en entier ; dans `socle.py`, `Refus`, `regle`, `quantile`, `strate`, `minutes` et `lecture` ;
  `parametres.json` ; `tests/synthetiques.py` l.1-20 ; `tests/test_cli.py` (`banc`, `lire`, et les tests touchés) ;
  README §3 ;
- `docs/adr-0029/g0-calib/PROPOSITION.md` §5.7 à §5.9 ;
- de la tête : `s2bis/tests/__init__.py`, `test_garde.py` et `test_dns.py` l.225-245 ;
- le résultat d'un `grep` ciblé de `proxy`, `environ` et `urllib` dans `s2bis/`.

**Seconde main [2nd] :** la sonde du générateur montre que le mandataire est joint hors isolement. Je ne m'en sers
comme preuve de rien.

**Commandes et sorties** : `g2/NOTES.md`, journal horodaté, et `g2/travail/`.

| contrôle | sorties |
|---|---|
| sondes | `sonde-1.out`, `sonde-fin.out` |
| rouges | `rougeA.out`, `rougeB.out` |
| verts | `vertA-envi.out`, `vertBs.out` |
| formes de nom | `formes.out` |
| différentiel | `differentiel.out`, `differentiel-temoin.out` |
| mutants | `mutants_{A,B,B_propose}.{tsv,log}`, `mut_*.out`, `invalide-1/` |
| corrections proposées | `propose_{A,B}_*.out`, `mb03.out` |
| matrice et batteries | `matrice_*.out`, `batterie_*.out`, `lot_lourd.log` |
| xtask | `xtask-{tete,AB}-verdicts.txt`, `xtask.log` |
| référence | `tau.py.ca6e` (le `tau.py` de CA-6e) |

**Outils** (`g2/outils/`) : `run.sh`, `sonde.py`, `formes.py`, `differentiel.py`, `mutants_g2.py`, `test_propose_B.py`,
`lot_lourd.sh` et `xtask.sh`. Je les ai contrôlés sur les octets : les seuls octets 92 sont les 30 séquences
d'échappement voulues (fin de ligne et tabulation) de `mutants_g2.py`. Les autres outils et ce rapport n'en
portent aucun.

**Recomptés par script** : sha256 des diffs, lignes ajoutées et retirées, octets 92, longueurs de ligne, `TODO` et
`FIXME`, `SHA256SUMS` du lot et du dossier, et les valeurs du §4.3.
