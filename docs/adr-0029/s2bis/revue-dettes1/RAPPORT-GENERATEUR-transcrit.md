# Rapport du générateur de DETTES-T1, avec les sections datées des corrections (transcrit)

> Transcription par l'orchestrateur le 2026-10-09 14:56:18 UTC du fichier RAPPORT-GENERATEUR.md ; contrôle FM-1.1 des transcripts du générateur-correcteur, du réviseur et du contre-contrôleur : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Rapport du générateur : lot DETTES-T1 (SHOGEN-TESTS-GARDE-MANDATAIRE-1, SHOGEN-CALIB-BORNE-MULTI-1)

2026-10-09, de 11:32 à 11:55 UTC (`date -u`). Worker G1 (générateur). Une G2 neuve doit suivre : ce rapport n'est pas
une relecture.

## 0. Gate 0 et cadre

- Modèle résolu : `claude-opus-5-5`, identifiant donné par l'environnement. L'effort ne peut pas se vérifier depuis la
  session.
- Base de la dette A : la tête `81485661f479c9165a91d39b9d25cc43c78144e6`, extraite par `git --no-optional-locks
  archive`, avec les sept exclusions. La tête est passée à `9d5d592` (CA-5e) pendant la passe. `s2bis/` n'a pas bougé :
  `git diff 8148566 9d5d592 -- s2bis/` est vide. Le diff GM-1 s'applique sur `9d5d592` sans décalage
  (`patch --dry-run`).
- Base de la dette B : `calib3/travail/snap/CA-6e`, reconstruite de deux façons :
  - tête + `diffs-tete/` CA-5a à CA-6e : 10 diffs sur 10 appliqués, lot égal à `snap/CA-6e` (`diff -r` vide), plancher
    64 ;
  - `ebd1560` + `diffs/` CA-0a à CA-6e : 21 diffs sur 21 appliqués, lot égal à `snap/CA-6e`.

  Contrôle : `9d5d592` = base + `diffs-tete` CA-5a à CA-5e, pour le lot et pour `gates.yml`.
- Dépôt réel en lecture seule : aucune écriture git, ni commit, ni push. `SHOGEN_S2_CAMPAGNE_CONTROL` n'a jamais été
  posée. Aucune clé n'a été lue ni écrite. Rien sur Pocket.
- Réseau : tout est passé par `outils/run.sh`, copie de `calib3/g2/outils/run.sh` : `env -u` sur les huit variables,
  puis `p1b/.../isole.sh`, TMPDIR `dettes1/tmp`.
  - Sonde préalable à 11:34 (`travail/sonde-1.out`) : 1.1.1.1 et 8.8.8.8 en errno 101, `urlopen` refusé, mandataire
    127.0.0.1:36573 en errno 111. Hors isolement, ce mandataire est joint : la sonde discrimine.
  - Sonde de fin à 11:54 : résultats identiques.
  - `ps` de fin : vide.

## 1. Dette A : SHOGEN-TESTS-GARDE-MANDATAIRE-1 (`s2bis/tests/`)

| diff | base | lignes ajoutées / retirées | plancher | sha256 |
|---|---|---|---|---|
| `diffs/GM-1.diff` | tête `8148566` (applicable sur `9d5d592`) | +25 / −2 (gates.yml +1, `__init__.py` +7, `test_garde.py` +17) | s2bis 340 → **341** | `74686277e20e0d6851cd1a29de368998d09aff5fc2d64de470bdd3eb6350e6ad` |

- **Remède** (forme de C-3) : `import os`, puis, après `TENTATIVES = []`, la boucle
  `for _v in [k for k in os.environ if k.lower() in ("http_proxy", "https_proxy", "all_proxy")]: del os.environ[_v]`.
  La docstring est complétée. Le reste de la garde est inchangé, à l'octet.
- **Test neuf** `test_garde.Garde.test_mandataires_purges`, indépendant de l'environnement :
  - un sous-processus pose sept variables fictives (`http://127.0.0.1:9`) : `HTTP_PROXY`, `http_proxy`, `HTTPS_PROXY`,
    `https_proxy`, `ALL_PROXY`, `all_proxy` et `Https_Proxy` (casse mêlée, que `urllib` lit aussi) ;
  - il importe `tests`, puis imprime `{'http','https','all'} ∩ getproxies()` et les noms qui restent dans
    `os.environ` ;
  - le test exige `(0, "[] []" + chr(10))`.
- **Rouge** (11:34, `travail/A/rouge.out`) : FAIL d'assertion. Sortie obtenue :
  `['all', 'http', 'https'] ['ALL_PROXY', 'HTTPS_PROXY', 'HTTP_PROXY', 'Https_Proxy', 'all_proxy', 'http_proxy',
  'https_proxy']`.
- **Vert** : ligne du job, isolée : Ran 341, conforme (`travail/A/vert.out`). Avec deux mandataires fictifs posés dans
  l'environnement (isolé), `test_garde` passe aussi.
- **Mutants** (`outils/mutants.py A`) :
  - méthode : ligne exacte du job (`--aucun-saut --egal --plancher 341`) depuis une racine jetable, sous `run.sh`, donc
    **sans aucun mandataire dans l'environnement**. Borne 300 s, `killpg`, PAR 2. Sortie 1 = tué, 0 = vivant, toute
    autre sortie = FATAL ;
  - résultat : **11 TUÉS, 0 FATAL, 0 INVALIDE**. A00, témoin sans changement, VIVANT ;
  - chaque mutant est tué par un FAIL de `test_mandataires_purges` : A01 purge retirée ; A02 `all_proxy` oubliée ;
    A03 `https_proxy` oubliée ; A04 `http_proxy` oubliée ; A05 minuscules oubliées ; A06 majuscules oubliées ; A07
    `os.unsetenv` au lieu de `del os.environ` ; A08 purge d'une copie ; A09 première variable seule ; A10 six noms
    écrits, casse mêlée oubliée ; A11 variable vidée au lieu de retirée.
- **Matrice** 3.10 à 3.13 en `-X dev -W error`, `PYTHONDEVMODE=1`, `PYTHONWARNINGS=error` : 4 fois code 0, Ran 341, 0
  « Exception ignored », 0 « Warning ».

## 2. Dette B : SHOGEN-CALIB-BORNE-MULTI-1 (`scripts/calib-actifs/`)

| diff | base | lignes ajoutées / retirées | plancher | sha256 |
|---|---|---|---|---|
| `diffs/BM-1.diff` | `ebd1560` + série CA-0a à CA-6e | +60 / −16 | calib 64 → **65** | `f3b409aa15e4d14d48fd1046daa2e518a21023e82888c567f8d84bc4bf492e92` |
| `diffs-tete/BM-1.diff` | tête + CA-5a à CA-6e (`diffs-tete/`) | +60 / −16 | calib 64 → **65** | `eaaff515f7640f3e6a3ebae6e6f47085a478354ef4be87400bad68c7a95fb3f7` |

- Répartition des lignes : gates.yml +1 ; README +2 ; `SHA256SUMS` du lot +3/−3, recalculé ; `tau.py` +14/−6 ;
  `tests/test_cli.py` +40/−6.
- Les deux versions ne diffèrent que par la ligne `index` et le `@@` de `gates.yml` (−264 contre −266). Les deux
  s'appliquent sans fuzz, et le lot qui en résulte est identique à l'octet (`cmp`).
- **Remède** (`tau.main`) :
  - le calcul passe sur chaque actif dans une boucle, avec `except Exception` par actif pour aller au bout ;
  - ensuite, `raise refus[0]` : le refus écrit est le premier dans l'ordre des actifs, soit celui qu'écrivait l'arrêt
    au premier ;
  - puis une ligne `descriptif hors refus (jamais décisif) : valeur calculée de la règle, <nom> : <v> ; <lieu>` est
    écrite pour chaque refus qui porte une valeur (CA/borne), dans l'ordre des actifs ;
  - le JSON reste `{"etiquette", "refus"}` : aucun fragment n'est écrit (voir Q-DT-1). Code 1.
- **Tests** :
  - `test_cli.test_borne_plusieurs` (neuf), sous la borne scellée de 0,0285 :
    - ETH et USDT : prix 100 sur cinq places, et 102 (ETH) ou 103 (USDT) sur okx, toutes les minutes actives ;
    - seule okx s'écarte de la médiane leave-one-out, qui vaut 100 : écart 0,02 ou 0,03, et P99,9 = maximum (rang 30
      sur 30) ;
    - valeurs de la règle, calculées à la main : 1,5 × 0,02 = 0,0300 et 1,5 × 0,03 = 0,0450. Elles sont au-delà de
      0,0285, puisque k = 60 et 90 dépassent k_haut = 56 ;
    - USDC (séries synthétiques) passe au premier passage. Au second, il lève une `ZeroDivisionError` (substitution
      de `calcul_actif`) ;
    - attendu dans les deux cas : le texte complet (refus d'ETH, ligne ETH 0.0300, ligne USDT 0.0450) et le JSON
      exact.
  - `test_borne_valeur` (C-13), borne abaissée à 0,0015 :
    - les trois actifs y touchent la borne. Le test exige maintenant les trois lignes, chacune égale à la règle du
      calcul direct ;
    - c'est un resserrement, pas un affaiblissement. L'ancienne attente d'une ligne unique est exactement le
      comportement d'un arrêt au premier.
- **Rouge** sur le `tau.py` de CA-6e (11:41, `travail/B/rouge2.out`) : 2 FAIL d'assertion.
  - `test_borne_plusieurs` : la ligne `0.0450 ; actif USDT` manque. La ligne `0.0300 ; actif ETH`, valeur faite à la
    main, est déjà tenue par CA-6e : la valeur indépendante est donc confirmée.
  - `test_borne_valeur` : les lignes USDC et USDT manquent.
- **Vert** : ligne du job, Ran 65, conforme, sur la tête et sur la série.
- **Mutants** (`outils/mutants.py B`, mêmes règles, plancher 65) : **11 TUÉS, 0 FATAL, 0 INVALIDE**. B00, témoin,
  VIVANT.
  - B01 « arrêt au premier » (un `break` après le premier refus, soit la forme de CA-6e) : TUÉ par FAIL de
    `test_borne_plusieurs` et de `test_borne_valeur`.
  - B02 refus écrit pris au dernier actif ; B03 `except socle.Refus` (une exception non nommée arrête le calcul) ; B04
    ligne du premier seule ; B05 ordre inverse ; B06 lieu du refus écrit ; B07 valeur du refus écrit ; B08 refus non
    relevé (fragment partiel) ; B10 refus pris au second ; B11 refus empilés à l'envers : tous tués par FAIL.
  - B09 (filtre des refus sans valeur retiré) est tué par ERROR, une `AttributeError` dans le gestionnaire.
  - Rejeu des mutants C-13 du correcteur, N18 à N21 : 4 TUÉS.
- **Matrice** 3.10 à 3.13 en `-X dev -W error`, sur la tête et sur la série : 8 fois code 0, Ran 65, 0 « Exception
  ignored », 0 « Warning ».

## 3. Gates (copies, sous `run.sh`, une suite à la fois)

| copie | calib-actifs | runner | s2bis | S2 |
|---|---|---|---|---|
| A : tête `8148566` + GM-1 | Ran 37 conforme (plancher de la tête) | 136 ok, 0 échec | Ran 341 conforme | Ran 415 conforme (sauts nommant la variable) |
| AB : tête + CA-5a à CA-6e + BM-1 + GM-1 | Ran 65 conforme | 136 ok, 0 échec | Ran 341 conforme | Ran 415 conforme |

- **sim-bis non lancé** : ses tests extraient `f35a70c` par git, ce qui est interdit (même motif qu'E-COR-3). Aucun de
  ses fichiers n'est touché, et les hunks de `gates.yml` portent sur les lignes s2bis et calib seules.
- Hook et gate des secrets : non lancés. Ils demandent une copie indexée par `git init` (forme d'E-CA3-3) et ne
  figuraient pas dans la liste du brief.
- `xtask` (lignes VERDICT seules ; sortie brute jamais lue) :
  - copies base, A et AB : 10 lignes identiques entre elles et identiques à `calib3/.../xtask-tete6e-verdicts.txt`
    (`cmp`) ;
  - 8 VERT, puis la 9e ROUGE (1 violation) et le global ROUGE ;
  - cette 9e ligne est la même sur la base : elle préexiste et n'est pas introduite ici (connue sur copie).
- Forme : 0 octet 92 dans les deux diffs et dans les fichiers touchés ; aucune ligne de plus de 120 caractères ; aucun
  `TODO` ni `FIXME` ; bibliothèque standard seule ; aucun test sauté ni désactivé.

## 4. Questions (mon choix, et sa raison)

- **Q-DT-1** : la lettre du brief dit « le JSON n'est pas écrit en cas de refus ».
  - Mon choix : le fichier `fragment_analyse.json` reste écrit sous sa forme de refus, `{"etiquette", "refus"}`, sans
    aucune valeur ; le test l'exige mot pour mot. Le cas « aucun fragment » est tenu.
  - Raison : le §5.7 et `test_refus` veulent « le même refus dans les deux sorties », et `lancer.sh` hache les deux
    fichiers de chaque passe. Supprimer le fichier changerait le contrat du lanceur, hors du périmètre de l'item.
- **Q-DT-2** : un refus non-borne d'un actif suivant (CA/population, CA/mediane, CA/btc) est calculé mais n'est pas
  imprimé, comme avant.
  - Mon choix : ne l'imprimer que s'il porte une valeur, ce qui veut dire CA/borne seulement.
  - Raison : le périmètre de l'item, et §5.7 (« jamais une valeur » au refus).
  - Limite : si un autre refus suit, sa découverte demanderait encore un second lancement. À former si l'orchestrateur
    veut une ligne « refus suivant » (environ 3 lignes et un test).
- **Q-DT-3** : `except Exception` par actif, et non `except socle.Refus`.
  - Raison : garder le refus écrit identique à celui d'un arrêt au premier dans tous les cas, y compris quand une
    exception non nommée survient sur un actif suivant (mutant B03).
- **Q-DT-4** : le repli `refus or [r]` a été retiré des lignes descriptives.
  - Raison : une valeur ne naît que dans `places` et `agregateurs`, qui sont appelés dans la boucle. `septembre` et
    `descriptifs` captent leurs propres refus, et `controle_fragment` rejoue des entrées déjà admises. Ce repli était
    du code mort, et il aurait laissé un mutant équivalent.
  - Si la G2 juge la défense utile, la remettre coûte une ligne.

## 5. Écarts

- **E-DT-1** (B.16) : aucune barre oblique inverse tapée dans du code du lot. Une seule est écrite, volontairement,
  dans `outils/fais_diff.sh` (`tr -cd` en octal 134, pour compter les octets 92), contrôlée sur les octets (= 1).
- **E-DT-2** : une commande composée (`setsid nohup sh -c` vers un script qui contient `rm`) a été refusée par la garde
  de l'outil. Rien n'a été exécuté. Elle a été relancée sous forme de fichiers (`outils/batterie.sh`,
  `outils/batteries.sh`).
- **E-DT-3** : la tête a avancé pendant la passe (CA-5a à CA-5e commis). Effet contrôlé au §0 : aucun.
- PID des processus lourds : campagne A 14450, campagne B 24604, batteries 7573, xtask 18728 ; un seul à la fois.

## 6. Provenance (G1)

- Lus [lu] :
  - `calib3/ADJUDICATION-G2.md`, avec tous ses ajouts datés ;
  - `calib3/BRIEF-CA.md` ;
  - `calib3/g2/RAPPORT-G2.md` §3.4 et §9 ;
  - `calib3/RAPPORT-GENERATEUR.md` §11 et §12 ;
  - `calib3/g2/cc/RAPPORT-CC.md` (O-CC-2, C-13) ;
  - `calib3/outils/` (`run_corr.sh`, `mutants_corr.py`, `matrice_corr.sh`, `batterie_corr.sh`, `xtask_corr.sh`,
    `serie_tete.py`) ;
  - le `tests/__init__.py` et le `test_pages.test_garde_reseau` de `snap/CA-6e` ;
  - `snap/CA-6e` : `tau.py`, `socle.py`, `tests/test_cli.py`, `tests/synthetiques.py`, `tests/test_fragment.py`,
    `README.md` §3, `lancer.sh` l.45-70 ;
  - `docs/adr-0029/g0-calib/PROPOSITION.md` §5.7 à §5.9 ;
  - `s2bis/tests/__init__.py`, `s2bis/tests/test_garde.py` et `.github/workflows/gates.yml` (l.198-269) de la base.
- Commandes et sorties : `NOTES.md` (journal horodaté) et `travail/` :
  - `sonde-*.out`, `A/{rouge,vert,mutants}.*`, `B/{rouge,rouge2,vert,vert-cli,mutants,mutants-rejeu}.*` ;
  - `matrice_*`, `batterie_*`, `xtask-*-verdicts.txt`.
- Outils : `outils/` (`run.sh`, `sonde_reseau.py`, `sonde_mandataire.py`, `mutants.py`, `matrice.sh`, `batterie.sh`,
  `batteries.sh`, `xtask.sh`, `fais_diff.sh`, `compte.py`, `sommes.py`).
- Chiffres recomptés par script : lignes des diffs (`compte.py`), octets 92, longueurs de ligne, sha256 (`sha256sum`).

## 7. Passe de correction après la G2 (2026-10-09, de 12:39 à 13:01 UTC, `date -u`)

- **Gate 0** : modèle résolu `claude-opus-5-5` ; correcteur (worker G1). Le réviseur G2 est distinct.
- **Lu** :
  - `ADJUDICATION-G2.md` : liste fermée C-A1, C-A2, C-B1 à C-B5 ;
  - `g2/RAPPORT-G2.md`, `g2/NOTES.md` et `g2/outils/`. `test_propose_B.py` est lu comme une donnée.
- `g2/SHA256SUMS` : 90 sur 90 OK. Rien n'a été écrit sous `g2/`.
- **Base** : tête `aec672e`, qui contient CA-6e. Son lot calib est égal à `snap/CA-6e`, et son `s2bis/` est égal à
  celui de `8148566`. À 12:59, la tête est `07d3979` (SB) : `s2bis/` et `scripts/calib-actifs/` sont inchangés, et
  seule la ligne sim-bis de `gates.yml` a changé. GM-1 et BM-1 (version tête) s'y appliquent sans décalage, et les
  fichiers obtenus sont égaux à la copie de travail.
- **Réseau** : `outils/run.sh`. Sondes à 12:40 et à 13:00 : errno 101, `urlopen` refusé, mandataire errno 111. `ps` de
  fin vide.

### 7.1 Diffs corrigés (mêmes noms ; versions d'avant la correction gardées sous `travail/corr/diffs*-avant-corr`)

| diff | base | lignes | plancher | sha256 |
|---|---|---|---|---|
| `diffs/GM-1.diff` (A, C-A1, C-A2) | tête `aec672e` | +56 / −8 : gates +1, `__init__.py` +7, `test_garde.py` +19, `test_dns.py` +29/−6 | s2bis **341** | `2d825e9aba5ee2ce8f84d7001f31f33f366851d41559d27a66933fb17fb6f010` |
| `diffs-tete/BM-1.diff` (B) | tête `aec672e` | +86 / −16 : gates +1, README +4, SHA256SUMS +3/−3, `tau.py` +18/−6, `test_cli.py` +60/−6 | calib **65** | `d8d500e74b3ea5ebc2eb75feeb34c1cd1b12d8f5fd610a64efd9e73810f28f42` |
| `diffs/BM-1.diff` (B) | `ebd1560` + CA-0a à CA-6e | le même ; seuls changent l'`index` et le `@@` de gates.yml | calib **65** | `d9e6d7cb255a88abb945bdffce5a2a59b5353462a0c44b1ef77eaf33e2542c89` |

- C-A2 est entré dans GM-1 : 56 lignes, sous la limite de 200, donc pas de diff neuf.
- Forme : 0 octet 92, au plus 120 colonnes, aucun `TODO` ni `FIXME`, aucune tabulation.

### 7.2 Corrections

| C | fait | preuve |
|---|---|---|
| C-A1 | `test_mandataires_purges` : dix noms, `hTtP_pRoXy`, `hTtPs_PrOxY` et `aLl_pRoXy` ajoutés ; docstring corrigée | MA01 TUÉ (FAIL du test), alors qu'il vivait sous GM-1 (G2) ; MA02 à MA12 TUÉS ; MA00 VIVANT |
| C-A2 | `test_dns` : `udp(comportement, port=0)` ferme sa socket si le bind échoue ; `tcp_et_udp` prend le port libre en TCP (`create_server` sur le port 0), puis le lie en UDP ; si le numéro est déjà tenu en UDP, un port neuf est repris (50 essais au plus) ; le test TC l'emploie | voir sous le tableau |
| C-B1 | passe `seul` de `test_borne_plusieurs` (ETH à 100 sur six places, USDT okx 103) : refus USDT, ligne 0.0450 USDT seule, code 1, JSON exact | MB03 TUÉ par FAIL `[seul]` ; la passe est verte sur CA-6e (un seul refus) |
| C-B2 | passe `sans valeur` : CA/population injecté sur ETH, puis USDT à 0.0450 | MB01 TUÉ par FAIL `[sans valeur]` ; rouge sur CA-6e |
| C-B3 | passe `ordre` (ETH 103, USDT 102) : 0.0450 ETH, puis 0.0300 USDT | MB10 TUÉ par FAIL `[ordre]` ; rouge sur CA-6e |
| C-B4 | `tau.main` : `refus` en couples (actif, exception) ; après les lignes de valeur, une ligne `descriptif hors refus (jamais décisif) : refus suivant : <refus>` par refus suivant sans valeur (exception non nommée : `REFUS CA/calcul : calcul en échec (<type>) ; actif <a>`) ; refus écrit et JSON inchangés ; passes `exception` (ZeroDivisionError sur USDC) et `suivant` (ETH à la borne, puis CA/population sur USDT) ; phrase au README | voir sous le tableau |
| C-B5 | README : « le JSON ne porte que le refus » | relu |

**Preuves de C-A2.** `outils/port_etroit.py` réduit la plage éphémère de l'espace isolé à 40000-40001 et tient le
port 40000 en TCP.

- Test de la tête : 20 lancements, **18 ERROR `EADDRINUSE`** (le défaut d'O-6, rendu fréquent).
- Test corrigé : **100 sur 100 OK** dans la même condition, et **100 sur 100 OK** sur la plage libre.
- Sa force tient. MD01 (repli en TCP sur le même port après TC) est TUÉ par le seul FAIL du test TC : l'écoute TCP est
  bien sur le port de l'UDP. MD02 (TC ignoré) et MD03 (`tc` rendu faux) sont TUÉS.

**Preuves de C-B4.**

- Rouge sur BM-1 : FAIL des passes `[exception]` et `[suivant]`.
- MC01 (refus suivants non imprimés, soit BM-1) : TUÉ par `[exception]` et `[suivant]`.
- MC02 (refus suivant imprimé avec le premier) : TUÉ par `[sans valeur]`.
- MC03 (`repr` au lieu du type), MC04 (actif omis), MC05 (refus à valeur repris en refus suivant) et MC06 (lignes de
  refus suivant avant les lignes de valeur) : TUÉS.

`test_borne_plusieurs` porte six passes sous `subTest`, si bien que chaque passe rougit à part. Ran reste 65 : le
plancher est inchangé et exact.

- **Rouge sur le `tau.py` de CA-6e** (`travail/corr/rougeB_ca6e.out`) : 6 FAIL d'assertion, soit `[deux]`,
  `[exception]`, `[ordre]`, `[sans valeur]`, `[suivant]` et `test_borne_valeur`.
- **Rouge sur le `tau.py` de BM-1** (`rougeB_bm1.out`) : 2 FAIL, `[exception]` et `[suivant]`.

### 7.3 Mutants

`outils/mutants_corr.py` est une copie de `g2/outils/mutants_g2.py`, avec la même méthode : racine entière copiée,
`env -i` sous `run.sh`, ligne exacte du job, borne 300 s, `killpg`, PAR 2. Les motifs B y sont suivis sur le code
corrigé, avec les mêmes mutations. Les octets 92 du fichier sont 38 séquences `\n` voulues dans des chaînes Python.

- **A** (PID 31726, de 12:45 à 12:50) : **15 TUÉS** (MA01 à MA12, MD01 à MD03, tous par FAIL), MA00 VIVANT, 0 FATAL, 0
  INVALIDE.
- **B** (PID 10002, de 12:50 à 12:52) : **18 TUÉS** (MB01 à MB12, MC01 à MC06), MB00 VIVANT, 0 FATAL, 0 INVALIDE.
  - Tous sont tués par FAIL, sauf MB04 : ERROR de `test_borne_plusieurs`, avec un FAIL de `test_borne_valeur`.
- `ps` de fin vide.

### 7.4 Matrice, gates, xtask

- **Matrice** 3.10 à 3.13, `-X dev -W error`, `PYTHONDEVMODE=1`, `PYTHONWARNINGS=error` : 12 fois code 0, 0
  « Exception ignored », 0 « Warning ». Soit calib en tête Ran 65, calib en série Ran 65, et s2bis Ran 341.
- **Batterie** sur tête + GM-1 + BM-1 (PID 25329) : calib Ran 65, runner 136 ok, s2bis Ran 341, S2 Ran 415
  (conformes, code 0). sim-bis n'est pas lancé (interdit de l'extraction git).
- **xtask** (lignes VERDICT seules) sur la tête `aec672e` et sur AB : 10 lignes identiques, égales à celles de la
  première passe. La 9e est ROUGE et préexiste.

### 7.5 Écarts

- **E-COR-DT-1** : C-B1 n'a pas de rouge sur CA-6e. L'ancien arrêt au premier écrit juste un refus unique ; son rouge
  est montré sous MB03.
- **E-COR-DT-2** : le rouge de C-A2 est une ERROR (`EADDRINUSE`, le défaut lui-même), pas un FAIL d'assertion. Le test
  garde sa force par des FAIL d'assertion (MD01 à MD03).
- **E-COR-DT-3** : MB04 est tué par une ERROR dans `test_borne_plusieurs`. Le `getattr(…, (0, None))[1]` du mutant
  bute sur un refus de valeur None. Il est aussi tué par FAIL dans `test_borne_valeur`.

**Provenance** : `NOTES.md`, passe de correction, et `travail/corr/`.

| contrôle | sorties |
|---|---|
| sondes | `sonde-*.out` |
| C-A2 | `ca2_*.out` |
| rouges | `rougeB_*.out` |
| verts | `vert*.out` |
| mutants | `mutants_{A,B}.{tsv,log}`, `mut/` |
| batterie et xtask | `lourd.log`, `../xtask-corr-*-verdicts.txt` |
| références | `tau.py.{ca6e,bm1}`, `test_dns.py.tete` |

Outils neufs : `outils/port_etroit.py`, `mutants_corr.py` et `lourd_corr.sh`.

## 8. Passe 3 après le contre-contrôle (2026-10-09, de 13:41 à 14:03 UTC, `date -u`)

- **Gate 0** : modèle résolu `claude-opus-5-5` ; correcteur (worker G1).
- **Lu** :
  - `g2/cc/RAPPORT-CC.md` (CONFORME-AVEC-RÉSERVES, R-1 à R-3, O-CC-5) ;
  - le dernier ajout daté d'`ADJUDICATION-G2.md` (C-A3, C-B6, C-B7, C-B8 ; règle « aucune dette ») ;
  - `g2/cc/outils/mut_cc.py` et `chainlink_cc.py`. `propose-R1-R3.diff` n'a pas été ouvert ; ce n'est pas mon diff.
- `g2/cc/SHA256SUMS` : tout OK. Rien n'a été écrit sous `g2/`.
- **Base** : tête `a75588d`. À 14:02, la tête est `bb285d8`. Depuis `aec672e`, `s2bis/` et `scripts/calib-actifs/` sont
  inchangés, et seule la ligne sim-bis de `gates.yml` a bougé. GM-1 et BM-1 (version tête) s'appliquent sur `bb285d8`
  sans décalage, et les fichiers obtenus sont égaux à la copie de travail.
- **Réseau** : `outils/run.sh`. Sondes à 13:42 et 14:02 : coupé. `ps` de fin vide.

### 8.1 Diffs (mêmes noms ; anciennes versions sous `travail/cc2/avant/`)

| diff | base | lignes | plancher | sha256 |
|---|---|---|---|---|
| `diffs/GM-1.diff` | tête | +57 / −8 | s2bis 341 | `e704fef1ab63c2c8db0c1c294aa77edbe9549759b7321e547af4ec7c1676626b` |
| `diffs-tete/BM-1.diff` | tête | +115 / −16 | calib 65 | `d7d49935ef9a6b4ee88e278f77e724bad9d88a6964020899cf642d85c2a98d01` |
| `diffs/BM-1.diff` | `ebd1560` + CA-0a à CA-6e | +115 / −16 | calib 65 | `ec50a9b7a87e7a9add3e997d7ca0b179ad808ae81562cd6c8d0199d2626bd783` |

- Forme : 0 octet 92 ; au plus 120 colonnes ; aucun `TODO` ni `FIXME` ; aucune tabulation.
- Ran reste à 341 et 65 : les passes neuves sont des `subTest` de `test_borne_plusieurs`, et C-A3 est une assertion de
  plus. Planchers exacts.

### 8.2 Corrections

| C | fait | rouge, puis vert |
|---|---|---|
| C-A3 | Le test TC affirme `tcp.getsockname()[1] == port` dans sa boucle, avant `setblocking` | NA2 et NA3 TUÉS par cette assertion (`AssertionError: 41491 != 40527`) ; ils vivaient au contre-contrôle. Vert : Ran 341. C-A2 rejoué : 100 sur 100 OK en plage étroite, 100 sur 100 sur la plage libre |
| C-B6 | Passe `deux suivants` : ETH à 102, USDC en `ZeroDivisionError`, USDT en CA/population, via `injecte(..., suite)` composable. Lignes figées : ETH 0.0300, refus suivant CA/calcul d'USDC, refus suivant CA/population d'USDT | NB2 et NB3 TUÉS par FAIL `[deux suivants]` ; vert |
| C-B7 | Passe `exception premier` : ETH en `ZeroDivisionError`, USDT à 103. Refus écrit et JSON figés : `REFUS CA/calcul : calcul en échec (ZeroDivisionError)`, sans actif ; ligne 0.0450 USDT | NB4 TUÉ par FAIL `[exception premier]` ; vert |
| C-B8 | `tau.main` : `vus = [str(r)]` ; une ligne « refus suivant » par texte, et jamais celle du refus écrit. Passes `doublon` (ETH à la borne, refus identique injecté sur USDC et USDT : une seule ligne) et `global` (plancher d'oracle d'USDT faux : CA/chainlink, levé dans `sigma.sigmas` pour chaque actif ; refus écrit seul, aucune ligne). Docstring et README | Rouge sur le code d'avant : FAIL `[doublon]` et `[global]` (`travail/cc2/rougeB_corr2.out`). Mutants à moi : NC01 (aucun dédoublonnage), NC02 (refus écrit hors du dédoublonnage), NC03 (dédoublonnage contre le seul refus écrit), tous TUÉS par FAIL. Vert |

### 8.3 Campagne (`outils/mutants_cc2.py`, PID 30381, de 13:46 à 13:54)

Méthode : racine entière, `env -i` sous `run.sh`, ligne exacte du job, borne 300 s, `killpg`, PAR 2.

- **Bilan** : **47 TUÉS**, MA00 et MB00 (témoins) VIVANTS, 0 FATAL, 0 INVALIDE.
- **Anciens** :
  - MA01 à MA12, MD01 à MD03 ;
  - MB01 à MB12 ; MB04 est tué par une ERROR de `[sans valeur]` et par un FAIL de `test_borne_valeur` ;
  - MC01 à MC06 ;
  - NA1 à NA4 et NB1 à NB7 du contre-contrôle.
- **Neufs** : NC01 à NC03.
- Les motifs anciens sont suivis sur le code de cette passe, avec les mêmes mutations. Aucun mutant ancien n'est
  retiré, et aucun test n'est affaibli.

### 8.4 Matrice, gates, xtask (PID 22894)

- **Matrice** 3.10 à 3.13 en `-X dev -W error` : 12 fois code 0, 0 « Exception ignored », 0 « Warning ». Soit calib en
  tête Ran 65, calib en série Ran 65 et s2bis Ran 341.
- **Batterie** tête + GM-1 + BM-1 : calib Ran 65, runner 136 ok, s2bis Ran 341, S2 Ran 415 ; toutes conformes. sim-bis
  n'est pas lancé (interdit de l'extraction git).
- **xtask** (lignes VERDICT seules) sur la tête et sur AB : 10 lignes identiques à la passe 2. La 9e est ROUGE et
  préexiste.

### 8.5 Question et écarts

- **Q-DT-5** (C-B8) : la lettre dit que les lignes « refus suivant » identiques ne s'impriment qu'une fois.
  - Mon choix : je dédoublonne aussi contre le **refus écrit**. Dans le cas global, on obtient donc le refus seul, sans
    aucune ligne.
  - Raison : la ligne de refus suivant sert à montrer un refus que la ligne décisive ne montre pas. Une ligne qui répète
    le refus écrit, ici CA/chainlink d'USDT levé pour chaque actif, n'apprend rien.
  - Si l'orchestrateur veut la lecture littérale (une ligne même égale au refus écrit), cela revient au mutant NC02 : une
    ligne de code et une attente de test à changer.
- **E-DT-4** (B.16) : `outils/mutants_cc2.py` porte une barre oblique inverse de continuation de ligne, tapée dans
  l'outil, hors du lot ; elle est comptée (= 1). Les diffs, le lot et ce rapport n'en ajoutent aucune.
- **E-DT-5** : le premier jet de la passe `doublon` (plancher faux d'USDT, ETH à 102) n'exprimait pas le cas voulu.
  CA/chainlink est levé dans `sigma.sigmas`, avant le τ des places : le refus écrit devenait CA/chainlink. La passe
  injecte désormais le même refus sur USDC et USDT, et le cas du plancher faux est devenu la passe `global`.
- **E-DT-6** : les copies de la passe 2 (`travail/corr/base2`, `w`) ont été supprimées. Elles étaient hors de
  `SHA256SUMS` et se reconstruisent par `git archive` plus les diffs.

**Provenance** : `NOTES.md` (passe 3) et `travail/cc2/`.

| contrôle | sorties |
|---|---|
| sondes | `sonde-*.out` |
| rouge | `rougeB_corr2.out` |
| verts | `vert*.out` |
| C-A2 | `ca2_*.out` |
| mutants | `mutants.{tsv,log}`, `mut/` |
| lot lourd | `lourd.log` |
| xtask | `../xtask-cc2-*-verdicts.txt` |
| base | `BASE` |

Outils : `outils/mutants_cc2.py` et `lourd_cc2.sh`.

## 9. Passe 4 : C-B9 (R-4 du contre-contrôle ; 2026-10-09, de 14:25 à 14:37 UTC, `date -u`)

- **Gate 0** : modèle résolu `claude-opus-5-5` ; correcteur (worker G1).
- **Lu** :
  - `g2/cc/RAPPORT-CC.md` §9 (R-1 à R-3 levées ; R-4 ; ND1 et ND2 vivants) ;
  - `g2/cc/outils/mut_cc3.py` (motifs de ND1 et ND2). `propose-R4.diff` n'a pas été ouvert.
- `g2/cc/SHA256SUMS` : tout OK. Rien n'a été écrit sous `g2/`, et rien en git.
- **Base** : tête `583135a`. À 14:35, la tête est `2229e15`. Depuis `a75588d`, `s2bis/` et `scripts/calib-actifs/` sont
  inchangés, et seule la ligne sim-bis de `gates.yml` a bougé. GM-1 et BM-1 (version tête) s'appliquent sur `2229e15`
  sans décalage, et les fichiers obtenus sont égaux à la copie de travail.
- **Réseau** : `outils/run.sh`. Sondes à 14:25 et 14:35 : coupé. `ps` de fin vide.

| diff | lignes | plancher | sha256 |
|---|---|---|---|
| `diffs/GM-1.diff` (inchangé depuis la passe 3) | +57 / −8 | s2bis 341 | `e704fef1ab63c2c8db0c1c294aa77edbe9549759b7321e547af4ec7c1676626b` |
| `diffs-tete/BM-1.diff` | +123 / −16 | calib 65 | `a649c7b655f831095d8c1c45ab9da487675f0c960175e2efd28e2a261b77002b` |
| `diffs/BM-1.diff` (série `ebd1560` + CA-0a à CA-6e) | +123 / −16 | calib 65 | `050c979828bf44deca6efc3f456bf5ad248f8831c32012353d15f59819bae561` |

- Les versions de la passe 3 sont gardées sous `travail/cc3/avant/`. Les deux BM-1 ne diffèrent que par `index` et
  `@@`.
- Forme : 0 octet 92, au plus 120 colonnes, aucun `TODO` ni `FIXME`, aucune tabulation.
- Ran reste à 65 : la passe est un `subTest`. Le plancher est exact.
- **C-B9** : passe `même motif` de `test_borne_plusieurs`.
  - Situation : ETH et USDC lèvent chacun leur CA/population en strate calme, par `pop_de(actif)`, injectés. USDT lève
    à l'identique le refus d'ETH.
  - Attendu : le refus d'ETH est écrit, puis une seule ligne, `refus suivant : REFUS CA/population : … ; actif USDC ;
    strate calme`, et le JSON exact.
  - La docstring nomme ND1 et ND2. Elle est aussi remise en forme, sans changer son texte. `tau.py` est inchangé : le
    code était juste, la preuve manquait.
- **Rouge et vert** :
  - ND1 (dédoublonnage par code et motif, actif ignoré) : **TUÉ** par FAIL `[même motif]` ;
  - ND2 (dédoublonnage contre le dernier texte seul) : **TUÉ** par FAIL `[même motif]` ;
  - sans mutant : vert, Ran 65.
- **Campagne** (`outils/mutants_cc3.py`, PID 771, de 14:26 à 14:29) :
  - **30 TUÉS** : ND1, ND2, NC01 à NC03, NB1 à NB7, MB01 à MB12 et MC01 à MC06 ;
  - MA00 et MB00 (témoins) VIVANTS ; 0 FATAL, 0 INVALIDE ;
  - aucun ancien n'est affaibli. MB04 est tué par une ERROR `[sans valeur]` et par un FAIL de `test_borne_valeur`.
- **Matrice** 3.10 à 3.13 en `-X dev -W error` (PID 10258) : 12 fois code 0, 0 « Exception ignored », 0 « Warning ».
  Soit calib en tête Ran 65, calib en série Ran 65 et s2bis Ran 341.
- **Batterie** tête + GM-1 + BM-1 : calib Ran 65, runner 136 ok, s2bis Ran 341, S2 Ran 415 ; toutes conformes.
  - xtask n'est pas relancé : il n'est pas demandé, et aucun `.rs` n'est touché.
  - sim-bis n'est pas lancé (interdit de l'extraction git).
- **Écart E-DT-7** (B.16) : un motif d'expression régulière avec des barres obliques inverses a été tapé dans une
  commande d'aide qui listait les identifiants des mutants. Effet contrôlé : la liste imprimée est juste (32
  identifiants). `outils/mutants_cc3.py` porte la même barre de continuation que `mutants_cc2.py` (= 1) ; les diffs,
  le lot et ce rapport n'en ajoutent aucune.
- **Provenance** : `NOTES.md` (passe 4) et `travail/cc3/`.

  | contrôle | sorties |
  |---|---|
  | sondes | `sonde-*.out` |
  | vert | `vertB.out` |
  | mutants | `mutants.{tsv,log}`, `mut/` |
  | lot lourd | `lourd.log` |

  Outils : `outils/mutants_cc3.py` et `lourd_cc3.sh`.
