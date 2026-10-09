# Contre-contrôle de DETTES-T1 (CONFORME après C-B9) (transcrit)

> Transcription par l'orchestrateur le 2026-10-09 14:56:18 UTC du fichier g2/cc/RAPPORT-CC.md ; contrôle FM-1.1 des transcripts du générateur-correcteur, du réviseur et du contre-contrôleur : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Contre-contrôle CC des corrections de la G2 du lot DETTES-T1 (GM-1, BM-1)

Le 2026-10-09, de 13:01 à 13:38 UTC (`date -u`). Contre-contrôleur neuf : je n'ai écrit ni les diffs, ni la G2, ni
les corrections. Je n'ai rien corrigé dans les pièces livrées.

## Gate 0

- Modèle résolu : `claude-opus-5-5` (identifiant donné par l'environnement de la session). L'effort ne se vérifie pas
  depuis la session.
- Dépôt réel en lecture seule (`--no-optional-locks`) : aucune écriture git, aucun commit, aucun push.
- `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée (`isole.sh` la retire). Aucune clé, aucun secret, rien sur Pocket.
- Réseau : tout passe par `cc/outils/run.sh` (copie de `dettes1/outils/run.sh` : `env -u` des huit variables, puis
  `isole.sh`, `TMPDIR=cc/tmp`). Sonde préalable (13:03) et sonde de fin (13:36) identiques : 1.1.1.1:443 et 8.8.8.8:53
  errno 101, `urlopen` URLError, mandataire 127.0.0.1:36573 errno 111.

## Verdict : **CONFORME-AVEC-RÉSERVES**

Les sept corrections C-A1, C-A2, C-B1 à C-B5 sont faites, et rien n'a été fait hors de la liste. Les quatre vivants de
la G2 (MA01, MB01, MB03, MB10) sont tués par un FAIL du test neuf. Le code est juste : mon différentiel donne 0 écart
sur 343 combinaisons.

Trois de mes onze mutants neufs vivent, d'où trois réserves sur la force des tests. Liste fermée, toutes de gravité
faible, toutes déjà prouvées sur une copie (§4) :

- **R-1 (C-A2)** : le test TC ne fige pas sa prémisse « même port ». Il faut ajouter
  `self.assertEqual(tcp.getsockname()[1], port)` dans la boucle de `test_drapeau_tc_garde_section_reponse_non_lue`,
  avant `tcp.setblocking(False)` (+1 ligne). Preuve : NA2 et NA3 TUÉS.
- **R-2 (C-B4)** : il faut une passe à **deux** refus suivants sans valeur, nommée « deux suivants » : ETH à 102 (borne),
  USDC en `ZeroDivisionError`, USDT en CA/population injecté. Lignes attendues, dans l'ordre : la valeur 0.0300 d'ETH,
  le refus suivant CA/calcul d'USDC, puis le refus suivant CA/population d'USDT. `injecte` devient composable
  (`suite=None`). Preuve : NB2 et NB3 TUÉS.
- **R-3 (C-B4)** : il faut une passe dont le **premier** refus de la boucle est une exception non nommée, nommée
  « exception premier » : ETH en `ZeroDivisionError`, USDT à 103. Refus attendu, sans actif :
  `REFUS CA/calcul : calcul en échec (ZeroDivisionError)`, dans le texte comme dans le JSON, puis la seule ligne 0.0450
  d'USDT. Preuve : NB4 TUÉ.

Forme de R-1 à R-3 sur copie : `cc/travail/propose-R1-R3.diff`, 52 lignes, avec la ligne `test_cli.py` de
`SHA256SUMS` recalculée. Ran reste à 341 et 65, donc les planchers ne changent pas. Contrôles : 0 octet 92, 120
colonnes au plus. Cette proposition n'est pas un diff livré : l'orchestrateur adjuge.

## 1. Pièces d'entrée

- J'ai lu en entier `ADJUDICATION-G2.md`, `g2/RAPPORT-G2.md` et la section 7 de `RAPPORT-GENERATEUR.md`. Cette
  section est lue comme une donnée : ses chiffres repris ici sont tous recomptés.
- `sha256sum -c` :
  - `dettes1/SHA256SUMS` : 143 sur 143 OK ;
  - `g2/SHA256SUMS` : 90 sur 90 OK.
- Les sha256 des trois diffs sont égaux au §7.1 du générateur :
  - `diffs/GM-1.diff` : `2d825e9a…f010` ;
  - `diffs-tete/BM-1.diff` : `d8d500e7…8f42` ;
  - `diffs/BM-1.diff` : `d9e6d7cb…2c89`.

## 2. Bases (consignées)

- **Tête** : `07d3979` (SB-11h). `travail/tete` vient de `git archive HEAD`, avec sept exclusions : `docs/rapports`,
  `docs/adr-0025`, `docs/adr-0028/monark-m009a`, `docs/adr-0028/execution`, `docs/15-*`, `docs/16-*` et
  `docs/pocket-report`. Leur absence a été contrôlée.
- **AB** = tête + `diffs/GM-1` + `diffs-tete/BM-1` :
  - les deux `patch` s'appliquent proprement, sans décalage ;
  - `SHA256SUMS` du lot calib : 29 sur 29, et sa liste est égale aux fichiers du lot ;
  - `diff -rq tete AB` donne 8 fichiers :
    - `gates.yml`, avec deux lignes seulement (plancher s2bis 340 → 341, calib 64 → 65) ;
    - dans `s2bis/tests` : `__init__.py`, `test_dns.py` et `test_garde.py` ;
    - dans `scripts/calib-actifs` : `README.md`, `SHA256SUMS`, `tau.py` et `tests/test_cli.py`.
- **Bs** = `git archive ebd1560` (mêmes exclusions) + `calib3/diffs` CA-0a à CA-6e (21 diffs sur 21) +
  `diffs/BM-1` :
  - le lot calib de Bs est égal à celui d'AB (`diff -r` vide) ;
  - la ligne du job a le plancher 65 ;
  - les deux BM-1 ne diffèrent que par la ligne `index` et le `@@` de `gates.yml`.
- **Arbre de travail du dépôt** (une copie de `gates.yml` seul, lue) : `gates.yml` y est modifié et indexé, par la
  chaîne de l'orchestrateur. Les hunks `gates.yml` de GM-1 et de BM-1 s'y appliquent (dry-run).
- **Rien hors de la liste.** J'ai rejoué les diffs d'avant la correction (`travail/corr/diffs*-avant-corr`) et comparé
  les fichiers. Les corrections ne touchent que :
  - pour C-A1, les noms de `test_garde` et sa docstring ;
  - pour C-A2, `test_dns`, inchangé avant la correction et neuf depuis ;
  - pour C-B4, les couples (actif, exception) de `tau.py`, la ligne de refus suivant et la docstring ;
  - pour C-B1 à C-B4, les six passes de `test_cli` ;
  - pour C-B4 et C-B5, la phrase du README.

  `gates.yml` et `__init__.py` sont inchangés par la passe de correction.

## 3. Corrections

Chaque mutant est rejoué par mon outil (`cc/outils/mut_cc.py`), avec la ligne exacte du job sous `env -i`.

| C | fait | mutant visé : rouge sous lui | vert sans lui | verdict |
|---|---|---|---|---|
| C-A1 | dix noms dans `test_mandataires_purges`, dont `hTtP_pRoXy`, `hTtPs_PrOxY` et `aLl_pRoXy` ; docstring « dix variables » | MA01 TUÉ, FAIL `test_mandataires_purges` ; FAIL aussi sous l'`__init__.py` de la tête | Ran 341 conforme | conforme |
| C-A2 | `tcp_et_udp` : port pris libre en TCP (`create_server` sur 0), puis lié en UDP ; reprise sur EADDRINUSE, 50 essais au plus | défaut d'O-6 : ancien test, plage étroite, 15 ERROR EADDRINUSE sur 20 | neuf, plage étroite : 100 sur 100 OK ; libre : 100 sur 100 OK | conforme, réserve R-1 |
| C-B1 | passe `seul` | MB03 TUÉ, FAIL `[seul]` | Ran 65 conforme | conforme |
| C-B2 | passe `sans valeur` | MB01 TUÉ, FAIL `[sans valeur]` | idem | conforme |
| C-B3 | passe `ordre` (ETH 103, USDT 102) | MB10 TUÉ, FAIL `[ordre]` | idem | conforme |
| C-B4 | lignes `descriptif hors refus (jamais décisif) : refus suivant : <refus>` ; exception non nommée en `REFUS CA/calcul : calcul en échec (<type>) ; actif <a>` ; passes `exception` et `suivant` | MC01 (= BM-1 d'avant) TUÉ, FAIL `[exception]` et `[suivant]` ; MC02 TUÉ, FAIL `[sans valeur]` | idem ; différentiel à 0 écart (§3.2) | conforme, réserves R-2 et R-3 |
| C-B5 | README : « le JSON ne porte que le refus » | (relu) | `SHA256SUMS` OK | conforme |

Rouges de `test_cli` seul :

- sous le `tau.py` de CA-6e : 6 FAIL d'assertion, soit `[deux]`, `[exception]`, `[ordre]`, `[sans valeur]`,
  `[suivant]` et `test_borne_valeur` ;
- sous le `tau.py` de BM-1 d'avant la correction : 2 FAIL, `[exception]` et `[suivant]` ;
- sous le `tau.py` corrigé : OK.

Ces trois résultats sont égaux à ceux du §7.2 du générateur.

**Valeurs de `[seul]` et `[ordre]` recomptées à la main.**

- e = 3/100 : k = ⌈1,5 × 0,03 / 0,0005⌉ = 90, soit 90 × 0,0005 = `0.0450`.
- e = 2/100 : k = 60, soit `0.0300`.
- Six places à 100 : e = 0 et k = 0 < k_bas, donc borne basse et aucun refus.

### 3.1 C-A2 : déterminisme et repli à 50 essais

Outils : `cc/outils/port_cc.py`, `reprise_cc.py` et `bind0_cc.py`. Tout tourne dans l'espace réseau isolé, où la plage
éphémère n'est écrite que pour cet espace.

| condition | test | résultat |
|---|---|---|
| plage 40000-40001, 40000 tenu en TCP | ancien (tête) | 15 ERROR EADDRINUSE, 5 OK, sur 20 |
| idem | neuf | **100 OK sur 100** |
| plage du noyau (32768-60999) | neuf | **100 OK sur 100** |
| 40000-40002, puis 40000-40006 ; 40000 tenu en TCP, 40001 en UDP | neuf | 100 sur 100 et 10 sur 10 FAIL, `AssertionError: aucun port libre en TCP et en UDP en 50 essais` |
| reprise forcée : premier `create_server` sur 40001 tenu en UDP, puis le noyau (`-X dev -W error`) | `tcp_et_udp` seul | 100 appels sur 100 à 2 essais, port TCP = port UDP 100 fois sur 100, 100 ports distincts, aucun avertissement |

**Le repli à 50 essais ne peut pas masquer un vrai défaut :**

- il ne porte que sur la mise en place du banc (bind TCP, puis bind UDP), avant tout appel au code testé.
  `dns.interroger` tourne une seule fois par message, hors de la boucle ;
- seul EADDRINUSE est repris ; toute autre `OSError` est relevée ;
- l'épuisement lève `AssertionError`, donc le test est rouge et jamais vert. Je l'ai mesuré en plage saturée (100 sur
  100 et 10 sur 10). Mon mutant NA4 (`essais=0`) est TUÉ par FAIL ;
- la force du test tient : MD01, MD02, MD03 et mon NA1 (repli TCP silencieux, `OSError` avalée) sont TUÉS par FAIL du
  test TC.

Ce que le repli peut produire, c'est un faux **rouge** : voir O-CC-4. La seule faiblesse trouvée est la prémisse non
figée (O-CC-1, R-1). Si `udp()` cessait d'honorer le port demandé (NA2), le banc perdrait sans bruit le « même port en
TCP ». Le repli TCP silencieux NA1 ne serait alors plus vu (NA3 vit). Avant C-A2, le banc tenait cette prémisse par
construction (bind TCP sur le port de l'UDP).

### 3.2 C-B4 : refus écrit et JSON, différentiel sur des issues injectées

Outil : `cc/outils/diff_cc.py`, écrit ici et indépendant de celui de la G2.

- Il oppose `tau.main` de CA-6e (l'arrêt au premier) à `tau.main` corrigé.
- Il couvre 7³ = **343** combinaisons d'issues par actif, injectées dans `calcul_actif` : ok, borne des places (avec
  valeur), borne des agrégateurs (avec valeur et classe), CA/population, CA/btc, `ZeroDivisionError` et `KeyError`.
- Il exige, pour les deux versions :
  - même code et même JSON ;
  - même refus écrit, à la ligne 2 ;
  - en succès, même texte hors de la ligne sha256.
- Il exige aussi, pour la version corrigée, les lignes hors refus attendues. Je les ai écrites depuis l'adjudication :
  - une ligne de valeur par refus à valeur, dans l'ordre des actifs ;
  - puis une ligne par refus suivant sans valeur, avec l'exception non nommée en `CA/calcul (<type>) ; actif <a>`.

Résultats :

| `tau` comparé à CA-6e | combinaisons | refus | écarts |
|---|---|---|---|
| corrigé | 343 | 342 | **0** |
| témoin : BM-1 d'avant la correction | 343 | 342 | 264, tous sur les lignes hors refus (0 sur le refus et le JSON) |
| témoin : NB4 (actif ajouté au refus écrit CA/calcul) | 343 | 342 | 228, dont des écarts sur le refus et le JSON |

**Le refus écrit et le JSON restent ceux de l'arrêt au premier.** La suite, elle, ne le fige pas pour un premier refus
non nommé dans la boucle : NB4 vit (R-3).

## 4. Mutants

**Méthode** (`cc/outils/mut_cc.py`) :

- copie jetable de la racine AB entière ;
- substitutions exactes, chacune d'une seule occurrence ; sinon le mutant est INVALIDE ;
- ligne exacte du job, sous `run.sh env -i` (`PATH`, `HOME`, `TMPDIR` seules), dans une nouvelle session ;
  - s2bis : `python3 -B enforcement/verdict-suite-s2.py s2bis --aucun-saut --egal --plancher 341` ;
  - calib-actifs : `python3 -B enforcement/verdict-suite-s2.py scripts/calib-actifs --aucun-saut --egal --plancher 65` ;
- borne 300 s par `killpg`, un mutant à la fois ;
- classement : sortie 1 = TUÉ, 0 = VIVANT, 3, toute autre sortie ou la borne = FATAL.

Bilan : **0 FATAL, 0 INVALIDE**. Toute mise à mort vient d'un FAIL d'assertion, jamais d'une ERROR. Chaque run porte
Ran 341 ou Ran 65.

**Campagne sur AB** (PID 14053, de 13:15 à 13:23) :

| id | mutation | classe | par |
|---|---|---|---|
| MA00 | témoin A | VIVANT | Ran 341 |
| **MA01** | (G2) purge par liste : majuscules, minuscules, `str.title` | **TUÉ** | `test_mandataires_purges` |
| MD01 | (générateur) repli TCP après TC | TUÉ | test TC |
| MD02 | (générateur) TC ignoré | TUÉ | test TC, `test_asn` `(cas='tc')` |
| MD03 | (générateur) `tc` faux | TUÉ | test TC, `test_analyse_a_soa_txt_nxdomain` |
| NA1 | (CC, C-A2) repli TCP silencieux, `OSError` avalée | TUÉ | test TC |
| NA2 | (CC, C-A2) `udp()` ignore le port demandé | **VIVANT** | → R-1 |
| NA3 | (CC, C-A2) NA1 + NA2, ordre supérieur | **VIVANT** | → R-1 |
| NA4 | (CC, C-A2) `essais=0` | TUÉ | test TC (`AssertionError` d'épuisement) |
| MB00 | témoin B | VIVANT | Ran 65 |
| **MB01** | (G2) lignes de valeur seulement si le refus écrit porte une valeur | **TUÉ** | `[sans valeur]` |
| **MB03** | (G2) refus unique non levé | **TUÉ** | `[seul]` |
| **MB10** | (G2) lignes de valeur triées par valeur croissante | **TUÉ** | `[ordre]` |
| MC01 | (générateur) refus suivants non imprimés | TUÉ | `[exception]`, `[suivant]` |
| MC02 | (générateur) refus suivants imprimés avec le premier | TUÉ | `[sans valeur]` |
| NB1 | (CC, C-B4) la boucle ne capte que `socle.Refus` | TUÉ | `[exception]` |
| NB2 | (CC, C-B4) seul le premier refus suivant est imprimé (`refus[1:2]`) | **VIVANT** | → R-2 |
| NB3 | (CC, C-B4) refus suivants en ordre inverse | **VIVANT** | → R-2 |
| NB4 | (CC, C-B4) le refus écrit CA/calcul nomme l'actif du premier refus | **VIVANT** | → R-3 |
| NB5 | (CC, C-B4) exception suivante nommée par l'actif du premier refus | TUÉ | `[exception]` |
| NB6 | (CC, C-B4) refus suivant réduit à son code | TUÉ | `[suivant]` |
| NB7 | (CC, C-B4) filtre des refus suivants sur la valeur du refus écrit | TUÉ | `[exception]`, `[sans valeur]`, `[suivant]` |

- Les quatre vivants de la G2 sont tous tués.
- Mutants neufs : onze (quatre sur C-A2, sept sur C-B4). Huit sont tués et trois vivent : NA2, NA3, puis NB2, NB3 et
  NB4 (les cinq vivants comptent NA3, mutant d'ordre supérieur).

**Campagne sur la copie des réserves** (`propose`, PID 28281, de 13:24 à 13:29) :

- MA00 et MB00 restent VIVANTS (Ran 341, Ran 65) ;
- NA2, NA3, NA1 et MD01 sont TUÉS (test TC) ;
- NB2 et NB3 sont TUÉS par `[deux suivants]`, et NB4 par `[exception premier]` ;
- MB01, MB03, MB10, MC01 et MC02 restent TUÉS.

## 5. Gates

**Matrice** : la ligne du job sous `-X dev -W error`, `PYTHONDEVMODE=1` et `PYTHONWARNINGS=error`, sous `env -i`,
isolée. Résultat : 12 fois code 0, 0 « Exception ignored », 0 « Warning ».

| python | AB s2bis 341 | AB calib 65 | Bs calib 65 |
|---|---|---|---|
| 3.10.20 | conforme, Ran 341 | conforme, Ran 65 | conforme, Ran 65 |
| 3.11.15 | conforme, Ran 341 | conforme, Ran 65 | conforme, Ran 65 |
| 3.12.3 | conforme, Ran 341 | conforme, Ran 65 | conforme, Ran 65 |
| 3.13.14 | conforme, Ran 341 | conforme, Ran 65 | conforme, Ran 65 |

**Batterie AB** (lignes lues dans le `gates.yml` de la copie ; une suite à la fois ; PID 4308) :

| suite | résultat |
|---|---|
| calib | conforme, Ran 65 |
| runner | 136 ok, 0 échec |
| s2bis | conforme, Ran 341 |
| S2 (`--egal`) | conforme, Ran 415, sauts nommant la variable |

Tout a rendu le code 0.

**xtask** (lignes VERDICT seules ; la sortie brute, jamais lue, est effacée) : la tête et AB donnent 10 lignes
**identiques**.

- Ce sont 8 VERT, la 9e ROUGE (1 violation) et le verdict global ROUGE.
- Le rouge préexiste sur la tête.
- AB est égal, au `cmp`, à `xtask-corr-AB-verdicts.txt` du générateur.

**Forme**, recomptée par script :

| contrôle | GM-1 | BM-1 (série et tête) |
|---|---|---|
| lignes | +56 / −8 | +86 / −16 |
| octets 92 | 0 | 0 |
| plus longue ligne ajoutée | 119 | 119 |
| `TODO` / `FIXME` ajoutés | 0 | 0 |
| tabulations | 0 | 0 |
| fin de fichier | LF | LF |

- Fichiers touchés : 0 octet 92 et au plus 120 colonnes.
- `gates.yml` porte déjà 4 octets 92, 2 lignes de plus de 120 colonnes et 3 mentions `TODO`/`FIXME` (le gate R-13
  lui-même). Ces comptes sont identiques sur la tête : rien n'est ajouté.
- R-25 : deux diffs unitaires, un par item. GM-1 compte 64 lignes de diff modifiées, sous 200 : aucun diff neuf n'est
  requis pour C-A2.
- R-13 : aucun `TODO` ni `FIXME` nu ajouté.

## 6. Constats

- **O-CC-1** (faible → R-1) : la prémisse « même port en TCP » du test TC n'est plus tenue par construction. NA2 et NA3
  vivent (§3.1).
- **O-CC-2** (faible → R-2) : aucune passe ne porte deux refus suivants sans valeur. Le pluriel (« une ligne par refus
  suivant ») et l'ordre ne sont pas figés : NB2 et NB3 vivent.
- **O-CC-3** (faible → R-3) : le refus écrit d'un premier refus non nommé **dans la boucle** n'est pas figé.
  - `test_refus` injecte l'exception hors de la boucle, dans `oracle_sh`, alors que `refus` est vide.
  - Les couples (actif, exception) de C-B4 rendent ce mutant exprimable : NB4 vit.
  - Mon différentiel le tue (228 écarts).
- **O-CC-4** (information) : faux rouge possible du banc de C-A2.
  - Sur une plage éphémère étroite, `create_server`, qui pose `SO_REUSEADDR`, reçoit du noyau toujours le même port
    pour `bind(0)`. Mesure : 30 fois sur 30 le port 40001 en 40000-40006, alors qu'un `bind` nu varie entre 40001,
    40003 et 40005.
  - La reprise n'y progresse donc pas : épuisement, puis FAIL d'assertion.
  - Dans une campagne de mutants, ce rouge d'environnement compterait comme TUÉ (sortie 1), comme l'ancien
    EADDRINUSE. Il ne survient qu'en plage étroite avec un port impair tenu en UDP ; sur la plage du noyau, j'ai obtenu
    30 ports distincts sur 30.
  - Aucune action requise.
- **O-CC-5** (information, `cc/travail/chainlink.out`) : refus global aux paramètres.
  - Un refus global aux paramètres, comme CA/chainlink levé par `socle.oracles` pour chaque actif, se répète. Le corrigé
    imprime deux lignes « refus suivant » identiques, et elles nomment l'actif du plancher faux (USDT), non celui du
    calcul.
  - Le refus écrit et le JSON sont égaux à ceux de CA-6e. Ces lignes ne sont jamais décisives.
  - Piste : dédoublonner les refus suivants par texte, au prochain lot qui touche `tau.main`, avec le même déclencheur
    qu'O-9 de la G2.
- **O-CC-6** (information) : l'arbre de travail du dépôt porte un `gates.yml` modifié et indexé (chaîne en cours).
  GM-1 et BM-1 s'y appliquent en dry-run. Si la tête avance encore, il faudra rejouer l'application avant le commit.

## 7. Écarts

- **E-CC-1** : le PID consigné au lancement de la campagne sur AB (14052) était celui de `setsid`, qui a fourché. Le
  script tournait sous le PID 14053, que j'ai attendu par `kill -0`. Les PID suivants (28281, 4308) sont relevés par
  `ps`.
- **E-CC-2** : le mode « reprise » de `port_cc.py`, dans sa forme première (plage 40000-40002, puis 40000-40006),
  n'exerce pas la reprise. Le banc y est saturé, à cause d'O-CC-4. Les sorties sont gardées
  (`ca2_neuf_sature-mesure-1.out`, `ca2_neuf_reprise.out`, `ca2_reprise_direct-plage-etroite.out`) et comptées comme
  mesures de saturation. La reprise est prouvée par injection (`reprise_cc.py`).
- **E-CC-3** : un `rm` groupé, précédé d'un `cd`, a été refusé par le contrôle de sécurité. Je l'ai refait en chemins
  absolus, sous `cc/` seulement.
- **E-CC-4** : un `grep` des lignes de job a été lancé une fois dans le dossier courant par défaut, `/home/user/shogen`.
  Il a lu le `gates.yml` de l'arbre de travail, sans écriture. Ce fichier n'est pas une lecture interdite.
- **E-CC-5** : les exclusions de l'archive sont les sept chemins ; les fichiers `*.jsonl` ne sont pas exclus. Ils sont
  écrits dans les copies et peuvent être lus par les suites, mais je n'en ai ouvert aucun. C'est la même pratique que
  la G2.
- **E-CC-6** : au `ps` de fin, aucun processus du CC ne reste. Un processus étranger y figure : PID 23115, dossier
  `/home/user/shogen`, job sim-bis plancher 249. Il n'a pas été lancé par ce contrôle.
- sim-bis, hooks et gate des secrets n'ont pas été lancés : ils sont hors de la demande.

## 8. Provenance (G1)

**Lus [lu] :**

- `ADJUDICATION-G2.md` ;
- `g2/RAPPORT-G2.md` ;
- `RAPPORT-GENERATEUR.md` §7 ;
- les trois diffs ;
- `dettes1/outils/` : `run.sh`, `mutants_corr.py`, `port_etroit.py`, `xtask.sh`, `matrice.sh`, `batterie.sh` et
  `lourd_corr.sh` ;
- `g2/outils/differentiel.py` et l'extrait de `mutants_g2.py` (MA01, MB01, MB03, MB10) ;
- dans AB :
  - `tau.py` `main` et l. 40-111 ;
  - `socle.Refus` et `socle.oracles` ;
  - `sigma.py` l. 60-64 ;
  - `dns.interroger` ;
  - `test_dns.py` l. 38-75 et l. 240-268 ;
  - `test_cli.py` l. 1-60 et l. 76-172 ;
- l'en-tête et les codes de sortie de `enforcement/verdict-suite-s2.py`.

**[2nd]** : aucun chiffre repris sans recomptage.

**Journal et sorties** : `cc/NOTES.md` est le journal horodaté. Les sorties sont sous `cc/travail/` :

| contrôle | sorties |
|---|---|
| verts | `vert_*.out` |
| rouges | `rouge*.out` |
| C-A2 | `ca2_*.out` |
| différentiel | `diff_cc*.out` |
| mutants | `mutants_*.{tsv,log}`, `mut-ab/`, `mut/` |
| matrice | `matrice_*.out` |
| batterie | `batterie_AB_*.out` |
| xtask | `xtask-*-verdicts.txt` |
| lot lourd | `lourd.log` |
| sondes | `sonde-fin.out` |
| information | `chainlink*.out` |
| sha256 des fichiers touchés d'AB | `sha256-AB.txt` |
| proposition | `propose-R1-R3.diff` |

**Outils** (`cc/outils/`) : `run.sh`, `sonde_reseau.py`, `sonde_mandataire.py`, `diff_cc.py`, `port_cc.py`,
`reprise_cc.py`, `bind0_cc.py`, `mut_cc.py`, `campagne*.sh`, `propose.py`, `chainlink_cc.py`, `matrice_cc.sh`,
`batterie_cc.sh`, `xtask_cc.sh` et `lourd_cc.sh`. Tous portent 0 octet 92 (contrôlé sur les octets).

`cc/tmp` est vidé et les copies lourdes sont effacées.

## 9. Passe 3 : vérification courte (2026-10-09, de 14:04 à 14:24 UTC, `date -u`)

### Gate 0

- Modèle résolu : `claude-opus-5-5`. Contre-contrôleur neuf : je n'ai écrit ni la passe 3, ni son diff.
- Dépôt en lecture seule (`--no-optional-locks`) : aucune écriture git, aucun commit, aucun push.
- `SHOGEN_S2_CAMPAGNE_CONTROL` n'a jamais été posée. Aucune clé, aucun secret.
- Réseau : `cc/outils/run.sh`. Sonde à 14:04 et à 14:23 : errno 101, URLError, mandataire errno 111.

### Verdict final : **CONFORME-AVEC-RÉSERVES**

- **R-1 à R-3 sont levées.** C-A3, C-B6 et C-B7 tuent NA2, NA3, NB2, NB3 et NB4, chacun par un FAIL d'assertion, et
  la suite reste verte.
- **C-B8 est juste dans le code.** Mon différentiel donne 0 écart sur 512 combinaisons, avec le dédoublonnage de
  Q-DT-5 écrit de mon côté.
- **Sa preuve dans la suite est incomplète.** Deux mutants neufs à moi survivent, ND1 et ND2. D'où une seule réserve
  (liste fermée) :
  - **R-4** (C-B8, gravité faible) : ajouter à `test_borne_plusieurs` la passe « même motif ».
    - ETH et USDC lèvent chacun leur CA/population (strate calme), et USDT lève à l'identique le refus d'ETH.
    - Attendu : le refus d'ETH est écrit, puis une seule ligne `refus suivant`, celle d'USDC.
    - Forme : `cc/travail/p3/propose-R4.diff`, 33 lignes avec la ligne `SHA256SUMS`. +4 lignes de test, Ran reste
      65, au plus 120 colonnes, 0 octet 92.
    - Vérifiée sur copie : ND1 et ND2 TUÉS par FAIL `[même motif]` ; NC01 à NC03, NB2 et NB4 restent TUÉS ; MB00
      VIVANT, Ran 65.
- Ce qui est en jeu :
  - **ND1** dédoublonne par code et motif, sans l'actif. Il supprime le refus d'un second actif de même motif : deux
    actifs sous N_min, ou un CA/population qui suit celui du refus écrit. C'est la perte même que C-B4 devait
    empêcher (88 écarts au différentiel).
  - **ND2** ne dédoublonne que contre le dernier texte. Il répète le refus écrit dans une suite (G, X, G) (4 écarts).

### Pièces

- `dettes1/SHA256SUMS` : 236 sur 236 OK.
- Les sha256 des diffs sont égaux au brief : GM-1 `e704fef1…626b`, BM-1 tête `d7d49935…8d01`, BM-1 série
  `ec50a9b7…d783`.
- Lus : `RAPPORT-GENERATEUR.md` §8, `NOTES.md` « Passe 3 » et l'ajout daté d'`ADJUDICATION-G2.md`, tous comme des
  données.

### Bases

- **Tête** : `ca77062`. Depuis `07d3979`, seule la ligne sim-bis de `gates.yml` a changé.
- **AB** = tête + GM-1 + BM-1 tête :
  - les deux diffs s'appliquent proprement ;
  - `SHA256SUMS` du lot est OK, et sa liste est égale aux fichiers du lot.
- **Bs** = `ebd1560` + CA-0a à CA-6e + `diffs/BM-1` : son lot est **égal** à celui d'AB (`diff -r` vide). Les deux BM-1
  ne diffèrent que par `index` et `@@`.
- **Rien hors de la liste.** J'ai rebâti la passe 2 depuis `travail/cc2/avant`, dont les sha sont ceux que j'ai
  vérifiés. De la passe 2 à la passe 3, seuls changent :
  - C-A3 : une ligne de `test_dns` ;
  - C-B8 : dans `tau.py`, le `vus` et la docstring ; une phrase au README ;
  - C-B6 à C-B8 : dans `test_cli`, `injecte` devient composable, plus quatre passes et la docstring.

### Corrections

| C | Fait | Preuve rejouée |
|---|---|---|
| C-A3 (R-1) | `assertEqual(tcp.getsockname()[1], port)` dans la boucle du test TC | NA2 et NA3 TUÉS (FAIL du test TC). C-A2 rejoué : 100 sur 100 en plage étroite, 100 sur 100 en plage libre |
| C-B6 (R-2) | passe `deux suivants` | NB2 et NB3 TUÉS, FAIL `[deux suivants]` |
| C-B7 (R-3) | passe `exception premier` | NB4 TUÉ, FAIL `[exception premier]` |
| C-B8 | `vus = [str(r)]` ; un texte une fois, jamais celui du refus écrit (Q-DT-5) ; passes `doublon` et `global` ; README | rouge sur le `tau.py` de la passe 2 : FAIL `[doublon]` et `[global]` ; NC01 TUÉ par `[doublon]` et `[global]`, NC02 par `[global]`, NC03 par `[doublon]` ; ND1 et ND2 VIVANTS, d'où R-4 |

### Différentiel C-B4 et C-B8 (`cc/outils/diff_cc3.py`)

- Il couvre 8³ = **512** combinaisons. Aux sept issues de la passe 2 s'ajoute un refus global identique à chaque actif
  (CA/chainlink nommant USDT).
- Il exige, pour la version corrigée, le même code, le même refus écrit et le même JSON que CA-6e, qui s'arrête au
  premier refus.
- Le refus écrit est aussi comparé à mon propre texte attendu.
- Les lignes hors refus attendues sont les lignes de valeur, puis les refus suivants dédoublonnés, refus écrit compris.

| `tau` comparé | écarts |
|---|---|
| corrigé | **0** (511 refus, 572 lignes « refus suivant ») |
| NC01 | 22 |
| NC02 | 16 |
| ND1 | 88 |
| ND2 | 4 |
| NB4 | 292 |

### Mutants

Mêmes règles qu'au §4 (`cc/outils/mut_cc3.py`) : la ligne exacte du job sous `env -i`, un mutant à la fois, `killpg`
à 300 s. Bilan : 0 FATAL, 0 INVALIDE.

| id | origine | classe | par |
|---|---|---|---|
| MA00 | témoin | VIVANT | Ran 341 |
| MB00 | témoin | VIVANT | Ran 65 |
| NA2 | CC | TUÉ | test TC |
| NA3 | CC | TUÉ | test TC |
| NB2 | CC | TUÉ | `[deux suivants]` |
| NB3 | CC | TUÉ | `[deux suivants]` |
| NB4 | CC | TUÉ | `[exception premier]` |
| NC01 | correcteur | TUÉ | `[doublon]`, `[global]` |
| NC02 | correcteur | TUÉ | `[global]` |
| NC03 | correcteur | TUÉ | `[doublon]` |
| ND1 | CC, neuf : dédoublonnage par code et motif, actif ignoré | **VIVANT** | → R-4 |
| ND2 | CC, neuf : dédoublonnage contre le dernier texte seulement | **VIVANT** | → R-4 |

### Gates (lot lourd, PID 19478, de 14:16 à 14:23)

- **Matrice** 3.10.20 à 3.13.14, en `-X dev -W error`, `PYTHONDEVMODE=1`, `PYTHONWARNINGS=error` : 12 fois code 0,
  avec 0 « Exception ignored » et 0 « Warning ». Elle couvre :
  - AB s2bis : Ran 341 ;
  - AB calib : Ran 65 ;
  - Bs calib : Ran 65.
- **Batterie** sur tête + GM-1 + BM-1 :
  - calib : conforme, Ran 65 ;
  - runner : 136 ok, 0 échec ;
  - s2bis : conforme, Ran 341 ;
  - S2 (`--egal`) : conforme, Ran 415, sauts nommant la variable.
- **Forme** :

  | diff | lignes | octets 92 | plus longue ligne | `TODO`/`FIXME` | tabulations |
  |---|---|---|---|---|---|
  | GM-1 | +57 / −8 | 0 | 119 | 0 | 0 |
  | BM-1 (série et tête) | +115 / −16 | 0 | 119 | 0 | 0 |

  Fichiers touchés : 0 ligne de plus de 120 colonnes. R-25 tenu : chaque diff reste sous 200 lignes.
- xtask n'est pas relancé : il n'est pas demandé à cette passe, et `.rs` comme `xtask` sont inchangés.

### Constat

- **O-CC-7** (faible → R-4) : C-B8 est juste, mais la suite ne distingue pas le dédoublonnage par texte entier d'un
  dédoublonnage par motif (ND1), ni d'un dédoublonnage contre le seul dernier texte (ND2).

### Écarts

- **E-CC-7** : une commande portait un `sed -i` sur `/dev/null`, refusé par sed et sans effet.
- **E-CC-8** : la course des témoins du différentiel a dépassé 120 s. L'outil l'a passée en tâche de fond ; je l'ai
  attendue jusqu'à sa fin (code 0).
- **E-CC-9** : au `ps` de fin, aucun processus du CC. Des processus étrangers tournent (campagne `nprime`, job S2 du
  dépôt réel), lancés hors de ce contrôle.

### Fichiers

- Notes : `cc/NOTES.md`, section « Passe 3 ».
- Sorties, sous `cc/travail/p3/` :
  - `mutants_{A,B,propose}.{tsv,log}`, `mut-ab/` et `mut/` ;
  - `diff_cc3*.out` ;
  - `lourd.log`, `matrice_*`, `batterie_AB_*` et `ca2_*.out` ;
  - `rougeB_p2.out` ;
  - `sonde-fin.out` ;
  - `sha256-AB.txt` ;
  - `propose-R4.diff`.
- Outils, sous `cc/outils/` : `mut_cc3.py`, `mut_cc3_defs.py`, `temoin3.py`, `diff_cc3.py`, `propose3.py`,
  `campagne3.sh`, `lourd_cc3.sh`, `matrice_cc3.sh` et `batterie_cc3.sh`. Ils portent 0 octet 92.
- Copies lourdes effacées ; `cc/tmp` vide.

## 10. Passe 4 : vérification courte de C-B9 (2026-10-09, de 14:38 à 14:42 UTC, `date -u`)

### Gate 0

- Modèle résolu : `claude-opus-5-5`. Contre-contrôleur neuf : je n'ai écrit ni C-B9, ni son diff.
- Dépôt en lecture seule (`--no-optional-locks`) : aucune écriture git.
- `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée.
- Réseau : sonde à 14:38 et à 14:41 : errno 101, URLError, mandataire errno 111.

### Verdict final : **CONFORME**

R-4 est levée, et R-1 à R-3 restent levées. Aucune réserve ne reste ouverte.

### Preuves

- **Pièces.**
  - `dettes1/SHA256SUMS` : 298 sur 298 OK.
  - Les sha256 sont égaux au brief :
    - `diffs-tete/BM-1.diff` : `a649c7b6…002b` ;
    - `diffs/BM-1.diff` : `050c9798…e561` ;
    - `diffs/GM-1.diff` : `e704fef1…626b`, inchangé.
  - Le §9 de `RAPPORT-GENERATEUR.md` est lu comme une donnée.
- **Bases.**
  - Tête : `3deeb70`. Depuis `ca77062`, seule la ligne sim-bis de `gates.yml` a changé.
  - Tête + GM-1 + BM-1 tête : propre et sans décalage ; `SHA256SUMS` du lot OK, et sa liste est égale aux fichiers.
  - `ebd1560` + CA-0a à CA-6e + `diffs/BM-1` : le lot est **égal** à celui de la tête. Les deux BM-1 ne diffèrent que
    par `index` et `@@`.
- **Rien hors de C-B9.** De la passe 3 (`travail/cc3/avant`, sha égaux à ceux de la passe 3) à la passe 4, seuls
  changent `tests/test_cli.py` et `SHA256SUMS` :
  - dans `test_cli.py` : `pop_de`, la passe « même motif » et la docstring ;
  - `tau.py` est inchangé.
- **Mutants** (`cc/outils/mut_cc4.py` : ligne exacte du job calib au plancher 65, sous `env -i`, un à la fois,
  `killpg`). Bilan : 0 FATAL, 0 INVALIDE.

  | id | classe | par |
  |---|---|---|
  | MB00 (témoin) | VIVANT | Ran 65 : vert sans mutant |
  | **ND1** | **TUÉ** | FAIL `[même motif]` |
  | **ND2** | **TUÉ** | FAIL `[même motif]` |
  | NB2 | TUÉ | FAIL `[deux suivants]` |
  | NB4 | TUÉ | FAIL `[exception premier]` |
  | NC01 | TUÉ | FAIL `[doublon]`, `[global]`, `[même motif]` |
  | NC02 | TUÉ | FAIL `[global]`, `[même motif]` |
  | NC03 | TUÉ | FAIL `[doublon]` |
  | MB03 | TUÉ | FAIL `[seul]` |

- **Différentiel** (`diff_cc3.py`, 512 combinaisons) : **0 écart**. Il compte 511 refus et 572 lignes « refus
  suivant ». Le refus écrit et le JSON sont égaux à ceux de l'arrêt au premier.
- **calib-actifs au plancher 65** : conforme, Ran 65, sur la tête et sur la version série.
- **Forme** des deux BM-1 : +123 / −16, 0 octet 92, 119 colonnes au plus, aucun `TODO`/`FIXME`, aucune tabulation.
  `test_cli.py` n'a aucune ligne de plus de 120 colonnes. R-25 tient (139 lignes, sous 200).
- Hors du périmètre de cette passe courte, et non relancés : la matrice, s2bis, S2, le runner et xtask. Ni le code ni
  `s2bis/` n'ont changé depuis la passe 3, où ces contrôles étaient verts (§9).

### Écarts

Aucun nouvel écart.

- `ps` de fin : aucun processus du CC.
- Copies `p4` effacées et `cc/tmp` vide.
- Sorties : `cc/travail/p4/` ; journal : `cc/NOTES.md`, section « Passe 4 ».
- Outils `mut_cc4.py` et `lourd_cc4.sh` : 0 octet 92.
