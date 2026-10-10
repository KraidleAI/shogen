# Contre-contrôle de DETTES-T5 (passes 1 et 2 ; clôture CONFORME) (transcrit)

> Transcription par l'orchestrateur le 2026-10-10 02:32:22 UTC du fichier g2/cc/RAPPORT-CC.md ; contrôle FM-1.1 des transcripts du générateur-correcteur, du réviseur G2 et du contre-contrôleur, par le fm11.py versé et par celui de DT3-E : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte ci-dessous sans retouche, sauf : le chemin du scratchpad est abrégé en `<scratchpad>` ; Retouche déclarée (précédent : versement du G0 de CALIB-ACTIFS) : 1 message(s) d'outil cité(s) entre guillemets sont mis en code, sans autre changement (S-G5 lit les guillemets comme une citation bibliographique).

# Contre-contrôle neuf du lot DETTES-T5 (corrections de la G2) : rapport

- **Modèle** : `claude-opus-5-5` (Gate 0 : identifiant exact donné par l'environnement ; préfixe conforme). Contre-contrôleur
  neuf : je n'ai ni écrit ni relu ce lot. Effort demandé : high.
- Heures lues par `date -u` : ouverture 2026-10-09 22:54:11 UTC ; redémarrage du conteneur vers 22:55 UTC (message de
  l'orchestrateur), reprise à 22:56:18 UTC ; rapport écrit à partir de 23:35:20 UTC (fin : « Clôture »).
- Brief : `BRIEF-CC.md`, sha256 `b1c1168414eeb2c5668d40918a71e67e4d172bb9ee37e6225d17c0628e837ac3` (préfixe attendu conforme).
- **Objet relu** (cité à la place d'un enregistrement de rôle, brief point 3) : tête
  **`094fa5d3d5debe9dd466e37feee95200ca460dcf`** (`git rev-parse`, `status` vide, au début et à la fin) ; série DT5-1 … DT5-14
  (`../../diffs/`), empreinte recalculée (sha256 de la concaténation dans l'ordre) :
  **`28da581e790aec5bab673d093431649ec1d2b6ecf4c9b742befe635640c43e4c`**, égale à celle du brief. DT5-9 à DT5-12 sont égaux
  octet pour octet aux propositions de la G2 (`cmp` avec `g2/propose/DT5-{2,5,7,8}-propose.diff`).
- Copies (outil `outils/copie.sh`) : clones `--no-hardlinks --no-checkout`, sparse non-cone sans `docs/15-*`, `docs/16-*`,
  `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, `docs/adr-0028/execution/` ni
  `*.jsonl` (1073 fichiers extraits, 58 sautés, 0 `*.jsonl`) ; checkout détaché de `094fa5d`, puis `git apply --check` et
  `git apply` : `copie` (DT5-1..14), `avant` (DT5-1..8), `s11`, `s12`, `s13` (états intermédiaires), `tete` (094fa5d seule).
- Pas d'enregistrement de rôle par `oracle_record.py` (brief point 3 : l'outil extrait des emplacements interdits).

## Verdict : **CONFORME-AVEC-RÉSERVES** (R-1 à R-6)

Les dix corrections sont faites et justes sur ce qu'elles visent. Chaque test neuf est rouge sur l'état antérieur et vert
sur la série. Toutes les gates sont vertes, aucun compte ne baisse. Les `VERDICT` de `cargo xtask verify` sont identiques à
la tête. Aucune gate n'est desserrée et je n'ai trouvé aucun défaut neuf qui vienne d'une correction.

Restent six constats corrigeables, dont deux de fond :

- **R-1** : une étiquette YAML explicite fait passer un libellé `-latest` aux deux contrôles à la fois.
- **R-2** : mon estimateur laisse 10 mutants vivants sur 11.

Les quatre autres sont documentaires. Leur forme exacte est livrée en six diffs, à appliquer **dans cet ordre après
DT5-14**. Je les ai vérifiés sur une copie de la série : l'arbre obtenu égale `tmp/prop`, où les gates ont tourné.

| diff proposé | réserve | lignes | sha256 |
|---|---|---|---|
| `propose/R-1-propose.diff` | R-1 (code de `workflows-yaml.py`, W-16, CAS 16, docstrings) | +35 −5 | `a6092c6d68bc353a04dbefa7c4b605c69fe08409abaef46d1170bfee13b630c3` |
| `propose/R-2-propose.diff` | R-2 (tests : 3 tests de RE étendus, W-14 étendu) | +29 −12 | `ae6115eed786d53394bc997200f45f0428d73f227285012772270be81f0c835a` |
| `propose/R-3-propose.diff` | R-3 (limites des deux gardes réseau, commentaire du job) | +7 −3 | `61fabf17a1eae8ee6878e0272b4b9c76f2205b1cbcf316fec70746e4451c4738` |
| `propose/R-4-propose.diff` | R-4 (limites de RE et de WY) | +6 −3 | `a790c2752c4e210f8f253d24e21ceb26ff92507f9447037f83cf60467d34f98a` |
| `propose/R-5-propose.diff` | R-5 (en-tête de `gates.yml`) | +3 −2 | `32f7c1af2c31e43ff9e63be9e67df7c8a63458156a56a981ba69c1c97518b45a` |
| `propose/R-6-propose.diff` | R-6 (datation du paragraphe C-7 du README) | +2 −1 | `a3737577954a5271b40dce68d18dd7246dae49858375cf84c4bce14fd52f5454` |

Concaténation des six, dans cet ordre : `a3ab1b62442df5c322e7eea77ca6cf427d56a5ec0aae355b99c5f74049a906d2`.

Contrôle des octets (consigne SHOGEN-HARNAIS-ECHAPPEMENTS-1) :
- aucune barre oblique inverse ni tabulation dans les textes écrits ; le code produit les forme par `chr(92)` et `chr(9)` ;
- le nombre d'octets 0x5c de chaque fichier modifié est inchangé (compté avant et après) ;
- toutes les lignes ajoutées font 120 colonnes au plus.

R-25 : six diffs, chacun bien sous 200 lignes ajoutées. Les comptes ne changent pas, sauf CAS du runner (15 → 16, R-1). Le
plancher de `controle-unittest` reste 36 (R-2 étend des tests existants).

## Les dix corrections

| corr. | diff | faite | juste | testée (rouge puis vert) | défaut neuf | suite |
|---|---|---|---|---|---|---|
| C-1 | DT5-11 | oui | oui | 2 FAIL sur le RE de DT5-7 (`cf756504…`), 9 OK sur l'état 11 | aucun | R-2, R-4 |
| C-2 | DT5-12 | oui | oui | souches : A, B et C' en 0 sur DT5-8, en 1 sur la série | aucun | — |
| C-3 | DT5-12 | oui | oui | W-12 et W-13 tuent MY-1 et MY-2 (rejeu de la campagne G2 sur la série) | aucun | — |
| C-4 | DT5-12 | oui | oui | documentaire | aucun | R-1 (clé de fusion non écrite) |
| C-5 | DT5-10, DT5-12 | oui | presque | documentaire | aucun | R-5 |
| C-6 | DT5-9 | oui | juste pour `sendmsg` ; incomplète | sonde : `sendmsg` → OSError, TENTATIVES +0 | aucun | R-3 |
| C-7 | DT5-11 | oui | oui | documentaire | aucun | R-6 (retouche de DT5-14 non datée) |
| C-8 | DT5-12 | oui | oui sur ses formes | ÉCHEC W-14 seul sur le WY de DT5-8 (`256060c8…`), 14 ok sur l'état 12 | aucun | R-1, R-2 |
| C-9 | DT5-13 | oui | même incomplétude que C-6 | documentaire ; aucune liste de sommes ne nomme ce fichier | aucun | R-3 |
| C-10 | DT5-14 | oui | oui | voir le détail ci-dessous | aucun | — |

Détail du rouge puis vert de C-10 :
- sur l'état 13 : 2 FAIL (`test_admis`, test neuf), et ÉCHEC W-10 et W-15 au runner (W-15 en `IsADirectoryError`, sortie 3 de
  WY sur le dossier `sous.yml`) ;
- sur la série : 10 OK et 15 ok.

Précisions :

- **C-2.** L'étape relit maintenant la version, et rattache le module au paquet par `dpkg -S`. Sondes faites avec des
  souches `dpkg-query`, `apt-get` et `sudo` en tête de `PATH`, étape extraite de `gates.yml` et lancée par
  `bash --noprofile --norc -eo pipefail` (`sorties/sonde-etape-yaml.txt`) :
  - A (6.0.2-1, `install` et `update` en échec) et B (6.0.1-2, idem) : sortie 0 sur DT5-8 ; sur la série, sortie 1
    « python3-yaml 6.0.1-2build2 exigé ».
  - C' (copie de PyYAML par `PYTHONPATH`) : sortie 0 et « PyYAML COPIE » sur DT5-8 ; sur la série, sortie 1 « PyYAML lu
    hors du paquet ».
  - D' (copie de PyYAML posée dans `enforcement/`) : W-11 la refuse déjà ([3, 3, 3, 0]), car le dossier du script passe
    devant `PYTHONPATH`. Pas de trou de ce côté.
- **C-10.** Aucune des 36 listes de sommes de `s2bis/`, `s2-harness/`, `scripts/` et `docs/adr-0029/` ne nomme les deux
  `tests/__init__.py` touchés (listes énumérées par `git ls-files`, lues une à une). Les trois listes qui nomment un
  `tests/__init__.py` (calib-actifs, plan-s2bis, plan-s2bis-2) nomment le leur, inchangé : `sha256sum -c` OK.
- **C-10, E-14 du générateur.** E-14 dit la classe des trois mutants FATAL de la G2 « couverte par les 8 mutants de C-10 ».
  C'est inexact pour « `.yaml` non lu » (R-7, Y-4) et pour « sous-dossiers lus » (MY-6). Je les ai rejoués, adaptés à
  `entrees()` (`outils/mutants_fatal_cc.py`) : 4 TUÉS sur 4. La campagne est donc complète ; pas de réserve.

## Réserves (liste fermée)

### R-1 (C-8, `workflows-yaml.py`) : une étiquette explicite efface le libellé, et les deux contrôles admettent alors un `-latest`

**Constat** (outil `outils/sondes_cc.py`, sortie `sorties/sondes-cc.json`) : quatre étiquettes font perdre le texte du
scalaire à la valeur construite par `SafeLoader` :

| étiquette | valeur construite |
|---|---|
| `!!null` | `None` |
| `!!binary` | octets |
| `!!set` | ensemble |
| `!!pairs` | tuples |

`chaines()` ne lit que `str`, `dict` et `list`. Si l'alias se trouve sur une ligne que RE ne lit pas, les deux contrôles
sortent en 0. Exemples :
- P-01 : `cfg: [&x !!null ubuntu-latest]` dans la matrice, puis `runs-on: *x` ;
- P-02 : la même forme avec `!!binary` ;
- P-19 : `env: {X: &x !!null ubuntu-latest}`, puis `runs-on: *x` ;
- P-03 et P-04 : `!!set {windows-latest}` et `!!pairs [{k: windows-latest}]` dans la matrice, admis alors que C-8 annonce
  « tout libellé -latest dans strategy.matrix ».

La phrase du README de C-7 (« les formes qu'il ne lit pas (alias, …) sont refusées … par `workflows-yaml.py` ») est fausse
pour ces formes.

La lecture de ces étiquettes par la forge n'est pas établie [abs]. Elle refuse probablement une étiquette inattendue
[inféré], mais la fermeture ne doit pas en dépendre.

**Forme exacte** : `propose/R-1-propose.diff`.
- Le `Lecteur` refuse, à la composition et avant toute construction, toute étiquette explicite qui perd le texte :
  `PERTE` = null, bool, int, float, binary, timestamp, set, omap, pairs.
- Message : « étiquette explicite refusée « tag:… » », avec ligne et colonne ; sortie 1.
- `!!str`, `!!seq` et `!!map` restent admis.
- Les étiquettes inconnues, `python/*` comprises, vont toujours au constructeur sûr, qui les refuse. W-12 garde donc son
  sens et tue toujours MY-1.
- Docstring : ce refus, plus celui des clés de fusion `<<`, constaté (P-14, P-20 : `could not determine a constructor for
  the tag 'tag:yaml.org,2002:merge'`) et nulle part écrit : `construct_mapping` construit chaque clé avant la fusion.
- Runner : cas W-16 (t1 `!!null`, t2 `!!binary`, t3 `!!set`, t4 `!!pairs` refusés ; t5 `!!str` admis), CAS 15 → 16,
  docstring (W-15 et W-16 nommés).

Aucun workflow du dépôt ne porte d'étiquette, d'ancre ni d'alias : lecture des événements PyYAML des 7 fichiers.

**Vérifié** :
- Rouge : runner de R-1 contre le WY de la série, ÉCHEC W-16 seul, 15 ok, sortie 1.
- Vert : 16 ok, et WY « conforme (7 workflow(s)) ».
- Sondes rejouées sur la série + R-1 (`sorties/sondes-cc-sur-R1.json`) : P-01, P-02, P-03, P-04 et P-19 refusés.
- Mutants : MC-12 (`PERTE` neutralisé) tué par W-16 ; MY-1 tué par W-12.

### R-2 (C-1, C-8) : formes documentées ou réelles que les tests ne fixent pas

**Constat** (estimateur propre : `outils/mutants_cc.py`, `sorties/mutants-cc.json`) : 11 mutants, 1 tué, 10 vivants. Deux
vivants sont sans conséquence (voir « Mutants »). Les huit autres portent sur des formes écrites dans les docstrings ou
courantes dans les workflows.

Sur RE :

| mutant | forme qu'aucun test ne fixe |
|---|---|
| MC-1 | en-tête de bloc à indicateur d'indentation (`runs-on: \|2-`) |
| MC-2 | ancre et étiquette ensemble (`runs-on: &a !!str`) |
| MC-3 | clé de matrice à trait d'union (`${{ matrix.runner-os }}`), forme courante |
| MC-4 | paire dans une suite de flux (`include: [os: …]`) |
| MC-5 | tabulation avant `#` |

Sur WY :

| mutant | forme qu'aucun test ne fixe |
|---|---|
| MC-6 | suffixe après `-latest` (`macos-latest-xlarge` par alias) |
| MC-7 | libellé dans un second job |
| MC-8 | libellé dans la seconde clé d'une matrice |
| MC-11 | `runs-on` en mapping (`{group, labels}`) |

Sur WY, chacun de ces mutants rendrait le job aveugle à un alias ou à un échappement que RE ne lit pas : la gate entière
admettrait alors le libellé.

**Forme exacte** : `propose/R-2-propose.diff`.
- `test_formes_hors_ligne` : 5 lignes ajoutées en fin d'arbre, refus attendus « 20 : ubuntu-latest », « 22 :
  windows-latest », « 23 : macos-latest ».
- `test_casse_cle_de_matrice_et_jetons` : `runner-os`, refus attendu « 13 : windows-latest ».
- `test_admis` : une ligne avec tabulation avant `#` (`chr(9)`) ; le compte de clés passe de 3 à 4.
- W-14 : 4 fichiers ajoutés (j second job, g mapping, s suffixe, k seconde clé avec échappement), un seul libellé par
  fichier et une seule voie de lecture.
- Aucun compte ne change : le plancher reste 36 et CAS reste celui de R-1.

**Vérifié** :
- Vert sur la série seule (10 OK, 15 ok) et sur la série + R-1 (10 OK, 16 ok).
- Mutants rejoués sur la série + R-1 + R-2 (`outils/mutants_cc2.py`, `sorties/mutants-cc-sur-R1R2.json`) : 12 tués sur 13 ;
  reste MC-10, équivalent.

### R-3 (C-6, C-9) : deux résolutions non gardées, absentes des limites corrigées

**Constat** (`outils/sonde_garde.py`, `sorties/sonde-garde.txt`) : sous la garde de `s2-harness/tests` et de
`s2bis/tests`, réseau coupé, deux appels échappent à la garde :
- `socket.getaddrinfo(host="example.com", port=80)` : la lambda ne lit que les arguments positionnels ;
- `socket.getnameinfo(("192.0.2.1", 80), 0)` : appel non gardé.

Dans les deux cas, l'appel atteint le résolveur réel (`gaierror`) et `TENTATIVES` reste à +0. Les docstrings corrigées
disent « une résolution (getaddrinfo, …) … lève ReseauInterdit » et ne listent en limites que `_socket` et `sendmsg`. Les
témoins se comportent comme attendu : `sendto` et `getaddrinfo` positionnel lèvent ReseauInterdit (+1).

**Forme exacte** : `propose/R-3-propose.diff` (documentaire, comme C-6 et C-9 ; le code reste identique dans les deux
paquets) : une limite ajoutée aux deux docstrings et au commentaire du job `s2-harness-unittest`. Variante, si
l'orchestrateur préfère fermer ces appels : garder `getnameinfo` et lire `k.get("host")`. Cela demande alors des tests dans
les deux suites et des planchers neufs.

### R-4 (C-1, C-8) : limites écrites incomplètes

**Constat** : la docstring de RE dit « jamais un refus en moins sur ces formes ». P-12 la contredit : un flux dont la ligne
de clé porte un `]` entre guillemets fausse le décompte `ouvert` (WY le refuse). Restent admis par les deux contrôles des
libellés posés par une entrée ou par une matrice que pose une expression :

| sonde | forme |
|---|---|
| P-06 | `matrix: ${{ fromJSON(needs….outputs.m) }}` |
| P-17 | `include: ${{ fromJSON('…l…') }}` |
| P-08 | `with: {runner: ubuntu-latest}` d'un workflow réutilisable |
| P-18 | entrée `workflow_dispatch` nommée `runner` |

RE n'écrit que « expression autre que `matrix.<clé>` », ce qui laisse croire la matrice couverte même quand une expression
la pose. WY n'écrit pas les entrées.

**Forme exacte** : `propose/R-4-propose.diff` (docstrings de RE et de WY).

### R-5 (C-5, en-tête de `gates.yml`) : « les workflows y échouent sans machine » cite un constat qui dit autre chose pour `gates`

**Constat** : l'adjudication de 21:28:17 UTC [2nd] dit : « le run du workflow `gates` a échoué sans job (cohérent) ; les
autres workflows échouent sans machine ». L'en-tête corrigé attribue « sans machine » à tous les workflows.

**Forme exacte** : `propose/R-5-propose.diff`. Nouveau texte : « sur la PR n° 10, le workflow gates a échoué sans job
(cohérent avec son YAML alors illisible, corrigé par DT5-0) et les autres sans machine ». La causalité n'est pas
affirmée : la forme suit le « cohérent » de l'adjudication.

### R-6 (C-7, `scripts/controle/README.md`) : paragraphe daté retouché sans date

**Constat** : le paragraphe « Ajout daté du 2026-10-09 22:24:59 UTC » parle maintenant de « l'adjudication C-10 » et de
« 10 tests … 36 ». DT5-14 l'a retouché sans date. Or C-10 a été adjugé à 22:37:10 UTC : le texte est postérieur à sa date.
La convention du README est d'écrire chaque ajout daté.

**Forme exacte** : `propose/R-6-propose.diff`. L'en-tête du paragraphe nomme la retouche (DT5-14, adjudication C-10 du
2026-10-09 22:37:10 UTC). Aucune liste de sommes ne nomme ce README (la liste de `scripts/controle` couvre fm11, regle et
render, et `sorties-fm11`).

**Vérification commune de R-1 à R-6.** Les six diffs s'appliquent dans l'ordre sur la série (`git apply --check`). L'arbre
obtenu (`tmp/pall`) égale le clone où ils ont été écrits. Jobs de `gates.yml` sur cet arbre (`sorties/j-pall-*` puis
`j-pall2-*` après la dernière rédaction de R-5) : toutes les étapes en 0, avec les mêmes comptes que la série, sauf le
runner YAML (16). La lecture YAML des 7 workflows est OK et aucun `TODO`/`FIXME` n'est ajouté.

## Recherche active de formes `-latest` encore admises (`sorties/sondes-cc.json`, puis `sondes-cc-sur-R1.json`)

Les formes sont écrites ici. Elles sont absentes des tests du lot et des sondes S-01 à S-14 de la G2. RE et WY sont lancés
sur un arbre jetable. Une « lecture brute » (PyYAML `compose`, étiquettes ignorées, alias suivis) dit si le texte d'un
scalaire sous `runs-on` ou `strategy.matrix` porte un `-latest`.

| sondes | RE | WY (série) | WY (+ R-1) | lecture |
|---|---|---|---|---|
| P-01, P-02, P-19 (alias vers `!!null`, `!!binary`) ; P-03, P-04 (`!!set`, `!!pairs` en matrice) | 0 | **0** | 1 | trou fermé par R-1 |
| P-05 (`!!null` sur la ligne de `runs-on`) | 1 | 0 | 1 | refusé par RE |
| P-09 `matrix['image']`, P-10 clé par alias, P-11 fin de ligne échappée, P-12 `]` entre guillemets, P-15 clé échappée | 0 | 1 | 1 | refusé par WY (P-12 : R-4) |
| P-13 scalaire simple sur deux lignes | 0 | 1 | 1 | libellé « self-hosted ubuntu-latest », pas une image flottante ; refus en plus |
| P-14, P-20 clé de fusion `<<` | 0 | 1 | 1 | refus de WY, même sans `-latest` (R-1 l'écrit) |
| P-16 `exclude` en `-latest` | 1 | 1 | 1 | refus en plus (serre) |
| P-06, P-07, P-08, P-17, P-18 (expression, entrée, variable) | 0 | 0 | 0 | limite écrite ; précisée par R-4 |

## Mutants

| campagne | cible | mutants | tués | vivants | FATAL |
|---|---|---|---|---|---|
| `mutants_cc.py`, sur la série (formes qu'aucun test n'a vues) | RE : MC-1 à 5, MC-10 ; WY : MC-6 à 9, MC-11 | 11 | 1 (MC-9) | 10 | 0 |
| `mutants_cc2.py`, série + R-1 + R-2 | les mêmes, plus MC-12 et MY-1 de la G2 | 13 | 12 | 1 (MC-10, équivalent) | 0 |
| `mutants_propose.py` de la G2, rejoué sur la série | RE (24) ; WY (20) | 44 | 41 | 0 | 3 (glob retirés par C-10) |
| `mutants_fatal_cc.py`, les 3 FATAL adaptés à `entrees()` (et MY-6 côté RE) | RE, WY | 4 | 4 | 0 | 0 |

Classement selon SHOGEN-MUT-FATAL-1 :
- RE (unittest) : TUÉ si la sortie vaut 1 avec « FAILED (failures=…) » sans `errors` ;
- WY (runner 0/1/3) : TUÉ si la sortie vaut 1 ;
- 0 = VIVANT ; toute autre issue, ou un remplacement qui ne trouve pas exactement une occurrence, = FATAL.

Fichiers restaurés, sha256 contrôlés après chaque campagne.

Vivants sans conséquence :
- MC-10 (suite `-` lue aussi après un bloc ou un flux) est équivalent sur du YAML valide : une ligne `-` au retrait d'une
  clé de bloc ou de flux est soit invalide, soit une clé déjà lue.
- MC-5 ne fait que refuser en plus : la docstring dit « `#` … après une espace ». R-2 le fixe quand même par `test_admis`.

## Gates rejouées

Conditions : réseau coupé (`isole.sh` du brief : `unshare -n`, lo seule) ; variables dont le nom contient « proxy » et
jetons retirés ; `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée.

Outil propre `outils/jobs_cc.py` : chaque étape `run:` de `gates.yml` de l'arbre tourne avec le shell de la forge :
- `shell: bash` → `bash --noprofile --norc -eo pipefail` ;
- sans `shell` → `bash -e`.

Exceptions :
- g5 (balayage `git grep`) et g3 `--tree` tournent sur un dépôt jetable des seuls fichiers présents (index, sans commit) ;
- g3 `--history` n'est pas lancé (il lirait l'historique des pièces interdites).

| gate | tête `094fa5d` | série DT5-1..14 | série + R-1..R-6 |
|---|---|---|---|
| g5 : cas du hook / R-13 | 54 ok / vert | 57 ok / vert | 57 ok / vert |
| g1 : environnement / runners-epingles | — / — | 0 / conforme (7 workflows, 22 clés) | 0 / conforme (7, 22) |
| g1 : workflows-yaml | — | python3-yaml 6.0.1-2build2, « PyYAML lu : /usr/lib/python3/dist-packages/yaml/__init__.py », 15 ok, conforme | idem, 16 ok |
| g1 : lint / R-1 / journaux-modele / docs-sha256sums | 227 / OK / conforme / 34, 295 | idem | idem |
| g3 : cas / `--tree` | 147 / 1064 fichiers | 147 / 1068 fichiers | 147 / 1068 fichiers |
| runner du vérificateur (5 jobs) | 137 ok ×5 | 137 ok ×5 | 137 ok ×5 |
| s2-harness `--egal` / s2bis / sim-bis / calib-actifs | 415 / 341 / 279 / 65 | 418 / 341 / 279 / 65 | 418 / 341 / 279 / 65 |
| controle `--egal` | 26 | 36 | 36 |
| `cargo test -p xtask` (`test result`) | 81 et 9 passés | identiques | non relancé (aucun Rust touché) |
| `cargo --locked xtask verify` (VERDICT) | 8 VERT, 1 ROUGE (sortie 1) | identiques | non relancé (aucun Rust touché) |

Lecture YAML de chaque workflow de la série (PyYAML 6.0.1, paquet `python3-yaml`) : 7 lus. Les `runs-on` valent
`ubuntu-24.04` ou `${{ matrix.os }}`, et les matrices `[ubuntu-24.04, windows-2025]` (`sorties/lecture-yaml-copie.txt`).
Le ROUGE de `cargo xtask verify` est celui de la tête, inchangé ; j'ai lu les lignes VERDICT seulement, comme le demande le
brief.

## Constats sans réserve (O-n)

- **O-1 (C-2).** Une souche qui se remplace par le module du paquet (`__file__` du paquet) passe le contrôle `dpkg -S`
  (ligne C de `sonde-etape-yaml.txt`). Ce cas est hors modèle de menace : qui pose `PYTHONPATH` sur la machine du job
  tient déjà le job. Ce n'est pas un défaut de la correction.
- **O-2.** Les refus en plus de WY servent la règle « serrer » : `exclude` en `-latest`, clé de fusion `<<` (désormais
  écrite par R-1), scalaire continué.
- **O-3.** Des processus étrangers ont tourné dans le conteneur, hors de mes dossiers : un `cargo test -p xtask` vers
  23:07, des `python3.12` vers 23:34. Je n'ai jamais eu plus de deux processus lourds à la fois.

## Écarts

- **E-1** : le conteneur a redémarré vers 22:55 UTC. Rien n'était perdu (lecture des pièces seulement, aucune copie ni
  processus) ; reprise consignée dans les NOTES à 22:56:18 UTC.
- **E-2** : PyYAML de l'hôte (6.0.1, paquet `python3-yaml`) a servi d'outil de mesure : extraction des étapes, sondes,
  lecture brute, lecture des événements. C'est le même écart que l'E-3 de la G2.
- **E-3** : écritures git dans mes seuls clones jetables, jamais de commit ; dépôt réel lu seulement, `status` vide à la
  fin. Gestes employés : `clone`, `sparse-checkout`, `checkout` détaché, `apply`, `add -A` (dans `prop` pour écrire les
  diffs, et dans les dépôts jetables de `git grep` et `--tree`).
- **E-4** : `gate-secrets.sh --history` n'a pas été lancé.
- **E-5** : `CARGO_NET_OFFLINE=true` ajouté aux deux commandes cargo ; le réseau est coupé de toute façon.
- **E-6** : `iso.sh` retire plus que les variables de mandataire du brief : tout nom en `*proxy*` ou `*TOKEN*`, `AWS_*`,
  `JAVA_TOOL_OPTIONS`, `SHOGEN_*`.
- **E-7** : la ligne PID de mes NOTES (23:07:15) a d'abord porté le PID du lanceur `setsid` ; corrigée en place, avec
  mention.
- **E-8** : j'ai lu les outils de la G2 et du générateur (listes de mutants, sondes) pour ne pas refaire leurs formes, et
  relancé tel quel `g2/outils/mutants_propose.py` (sha256 `ba145e5c…`) sous mon `iso.sh`.
- **E-9** : `sondes_cc.py` a été corrigé une fois avant les sorties gardées (P-17 ne portait pas de `-latest` ; P-19 et
  P-20 ajoutés). `mutants_cc.py` a été dérivé en `mutants_cc2.py` et `mutants_fatal_cc.py`. `propose_cc.py` a été retouché
  trois fois (lignes de plus de 120 colonnes, R-4, R-5) ; les diffs finaux sont régénérés et vérifiés.
- **E-10** : la souche « faux » des lignes C et D de `sonde-etape-yaml.txt` usurpe `__file__`. Ces lignes sont refaites en
  C' et D' avec une copie honnête, et annotées dans le fichier. La piste `PYTHONSAFEPATH` (lignes D à G) a été abandonnée
  quand D' a montré que W-11 la couvre déjà.
- **E-11** : listes de noms par `git ls-files` dans ma copie creuse (noms seulement, jamais de contenu ; les motifs ne
  touchent aucun emplacement interdit) :
  - pathspecs bornés à `s2bis/`, `s2-harness/`, `scripts/` et `docs/adr-0029/` pour trouver les listes de sommes ;
  - `ls-files -t` pour compter les fichiers extraits ou sautés, passé à `grep -c` et jamais affiché.
  
  Ce sont des listes sur l'index, pas une recherche de contenu ; je les déclare pour la règle « aucune recherche
  récursive ». Les suites rejouées extraient elles-mêmes, par `git archive`, une liste épinglée de fichiers des paquets
  `shogen_s2` et `s2bis` (`scripts/sim-bis/oracle_r1.py` l.44-47, `oracle_recalc.py` l.46-49, lus). D'après
  `scripts/sim-bis/parametres.json` (lu), la liste est : 5 fichiers de `s2-harness/shogen_s2/` à `f35a70c`, et 6 fichiers
  de `s2bis/` (`config/analyse.json`, `shogen_s2bis/…`, `tests/test_rotation.py`) à `f4589804`. Aucun emplacement
  interdit ni aucun `*.jsonl` n'en fait partie.

## Journal de provenance (G1)

**[lu]** :
- pièces du lot : `BRIEF-CC.md` ; `../../ADJUDICATION.md` (entier) ; `../RAPPORT-G2.md` (entier) ; `../../RAPPORT-GENERATEUR.md`
  l.1-60 et l.248-592, dont la section de 22:52:44 UTC en entière ;
- diffs : DT5-9 à DT5-14 en entier. DT5-1 à DT5-8 ne sont pas relus ligne à ligne (relus par la G2) ; je les ai lus par
  leur effet dans les fichiers ci-dessous ;
- dans la copie, en entier : `enforcement/runners-epingles.py`, `enforcement/workflows-yaml.py`,
  `enforcement/tests/run-fixtures-workflows-yaml.py`, `scripts/controle/tests/test_runners_epingles.py`,
  `s2-harness/tests/__init__.py` et `s2bis/tests/__init__.py` ;
- dans la copie, par plages : `.github/workflows/gates.yml` (l.1-40, 75-175, 196-215, et la liste des étapes par
  PyYAML) ; `scripts/controle/README.md` l.57-67 ; `scripts/controle/SHA256SUMS` (noms seulement) ;
  `enforcement/gate-secrets.sh` (lignes `--tree`, `ls-files`) ; `scripts/sim-bis/oracle_r1.py` l.40-52 ;
  `scripts/sim-bis/oracle_recalc.py` l.42-54 ; `scripts/sim-bis/parametres.json` (clés `oracle_r1` et `oracle_recalc`) ;
- `docs/adr-0028/ANNEXE-D-preenregistrement.md` l.28-52 (liste D.2) ;
- outils d'isolement : `isole.sh`, `lo_up.py` ;
- outils de la G2 : `mutants_propose.py`, `sondes_runners.py`, `cargo.sh`, `iso.sh`, `jobs_g2.py` ;
- outils du générateur : `mutants_c10.py`, et les listes de `mutants_re.py`, `mutants_yaml.py`, `mutants_g2.py`.

**[2nd]** : faits de forge (PR n° 10 : `gates` sans job, autres workflows sans machine, dépôt privé) : adjudication de
21:28:17 UTC.

**[abs]** :
- lecture par la forge des étiquettes explicites (R-1, d'où une fermeture côté contrôle) ;
- lecture par la forge des fichiers cachés et des extensions en capitales (décision C-10).

**Commandes**, sorties sous `sorties/` :
- empreinte de la série : `cat … | sha256sum` ; `cmp` avec les propositions de la G2 ;
- `outils/copie.sh` ;
- jobs : `outils/jobs_cc.py` ×4 (copie, tête, pall, pall2) ;
- cargo : `outils/cargo_cc.sh` ;
- rouges et verts : `outils/rouge_vert_cc.sh` ;
- sondes : `outils/sondes_cc.py` (×3), `outils/sonde_garde.py`, étape YAML (souches sous `sondes/etape-yaml/`) ;
- mutants : `outils/mutants_cc.py`, `mutants_cc2.py`, `mutants_fatal_cc.py`, et le rejeu de `mutants_propose.py` ;
- réserves : `outils/propose_cc.py`, `git apply --check`/`--numstat`, `dpkg -S`, `dpkg-query`.

**Chiffres recomptés** :
- comptes de tests et de cas : par les sorties des runs ;
- mutants : par les JSON ;
- lignes des diffs : par `git apply --numstat` ;
- 22 clés : par le contrôle, et à la main (2+4+8+3+1+2+2) ;
- 1073 et 58 fichiers : par `git ls-files -t` ;
- 36 listes de sommes : par `git ls-files`.

## Clôture

Fin à 2026-10-09 23:38:56 UTC (`date -u`), dernière entrée de `NOTES.md`. Dépôt réel à `094fa5d`, `status` vide, jamais
écrit ; aucun processus à moi ne tourne encore. Aucun commit, aucune
poussée, aucun accès réseau (tout sous `isole.sh`), `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée, aucune pièce de D.2 ouverte,
aucune recherche récursive sur `docs/`, le dépôt ou le scratchpad. Copies et dépôts jetables de `tmp/` supprimés à la fin ;
ils se régénèrent par `outils/copie.sh`, puis les diffs. Gardés et sommés dans `SHA256SUMS` (chemins relatifs, sans `./`) :
`BRIEF-CC.md`, `NOTES.md`, ce rapport, `outils/`, `propose/`, `sondes/` et `sorties/`.

## Ajout daté du 2026-10-10 00:20:11 UTC (`date -u`) : passe 2 (R-1 à R-6 adoptées, C-11)

- **Modèle** : `claude-opus-5-5` (Gate 0 : identifiant exact donné par l'environnement), même contre-contrôleur, passe 2
  demandée par l'orchestrateur. Ouverture à 2026-10-09 23:57:34 UTC (`date -u`).
- **Objet relu** : tête **`094fa5d3d5debe9dd466e37feee95200ca460dcf`** (`git log -1`, `status` vide, au début et à la fin).
  Série DT5-1 … DT5-21, empreinte recalculée **`8462701f7a24dd0fba5d0f6728aca17aa5136534185d88266b8acc1d37c21f72`**,
  égale au message de l'orchestrateur.
  - DT5-1 à DT5-14 sont inchangés : leur concaténation donne toujours `28da581e…`.
  - DT5-15 à DT5-20 égalent mes `propose/R-1` à `R-6-propose.diff` octet pour octet (`cmp`).
  - DT5-21 : sha256 `e917ebaf773e5f33cbb2c4b16cd22c8837f69a93614ec66bbf09196a1528fa1a`, +67 −28, 6 fichiers.
- Pièces lues :
  - `../../ADJUDICATION.md`, ajout de 23:39:53 UTC (l.36-41) ;
  - `../../RAPPORT-GENERATEUR.md`, section de 23:56:25 UTC (l.594-fin) ;
  - DT5-21 en entier ;
  - dans la copie de la série : les deux gardes et leurs deux modules de test, en entier ;
    `scripts/calib-actifs/tests/__init__.py` en entier ; `scripts/calib-actifs/SHA256SUMS` ; `README.md` (l.11-43) ;
    `tests/test_pages.py` (l.1-20 et 90-125).
- Copies (`outils/copie.sh`) : `copie2` (DT5-1..21) et `av21` (DT5-1..20), 91 M chacune. Elles ont été supprimées à la
  fin, avec tous les clones jetables. `df -h /` avant la compilation : 6,8 G libres.

### Verdict de la passe 2 : **CONFORME-AVEC-RÉSERVES** (R-7, R-8)

R-1 à R-6 sont levées. C-11 est fait et juste sur son objet : `host=` et `getnameinfo` sont gardés, les deux blocs sont
égaux octet pour octet, les planchers 419 et 342 sont exacts. J'ai mesuré qu'aucune suite ne dépend d'une résolution non
locale. Toutes les gates sont vertes, aucun compte ne baisse. Les `VERDICT` de `cargo xtask verify` sont identiques à la
tête.

Restent deux constats corrigeables, liés à C-11 :
- **R-7** : défaut neuf mineur. C-11 lit `host=` et `sockaddr=` comme si les fonctions C acceptaient des mots-clés : un
  appel invalide devient `ReseauInterdit` et s'inscrit dans `TENTATIVES`. En plus, une forme réelle n'est fixée par aucun
  test.
- **R-8** : C-11 laisse de côté une troisième copie de la garde, `scripts/calib-actifs`. Son bloc était égal à celui de
  s2bis et ne l'est plus. Le fichier appartient à un lot épinglé.

| diff proposé | réserve | lignes | sha256 |
|---|---|---|---|
| `propose/R-7-propose.diff` | R-7 : lecture de l'hôte des seules formes valides ; tests (2 suites) | +50 −16 | `6586e5a20048f27925f1712056b9002e56b18a020f5147d9703f04f727045019` |
| `propose/R-8-propose.diff` | R-8 : garde de calib-actifs alignée ; test ; 2 lignes du `SHA256SUMS` du lot | +36 −11 | `7db1663f7c725757cb6ac56c1a00ecc0487511c4779a371231f7bec8cc0c6902` |

Les deux s'appliquent dans cet ordre après DT5-21 (`git apply --check`). Concaténation des deux :
`84ee75d17595f6d11e4b57626633639d6c78b76eeeb2220319c5334666f93538`. Les textes écrits ne portent aucune barre oblique
inverse ni tabulation, et toutes les lignes ajoutées font 120 colonnes au plus. Les comptes des suites ne changent pas :
R-7 et R-8 étendent des tests existants.

### R-1 à R-6 : levées

| réserve | preuve sur la série DT5-1..21 |
|---|---|
| R-1 | Sondes rejouées (`sorties/sondes-cc-passe2.json`, octets égaux à `sondes-cc-sur-R1.json` de la passe 1) : P-01 à P-04 et P-19 sont refusés par WY. W-16 au vert. |
| R-2 | Mutants rejoués (`sorties/mutants-cc-passe2.json`) : 12 tués sur 13 ; seul MC-10, équivalent, reste vivant. Tests de RE : 10 OK. |
| R-3 | Remplacée par C-11 (E-16 du générateur) : les limites écrites par DT5-17 sont retirées par DT5-21, ce qui est juste puisque ces appels sont maintenant gardés. |
| R-4, R-5, R-6 | Textes présents dans l'arbre : RE et WY (limites), en-tête de `gates.yml` (PR n° 10), README (retouche datée). |

### C-11 (DT5-21) : contrôle

- **Rouge puis vert** (`outils/rouge_c11_cc.sh`, `sorties/rouge-vert-c11-cc.txt`) : avec les gardes de l'état 20 et les
  tests de l'état 21, FAILED (failures=1) dans chaque suite (`['gaierror'] ×3` au lieu de `ReseauInterdit ×3`) ; à l'état
  21, OK (4 tests par module).
- **Blocs** : de « `TENTATIVES = []` » à la fin, `s2-harness` et `s2bis` sont égaux octet pour octet (1280 octets).
- **Planchers** : 419 (`PLANCHER`, `verdict-suite-s2.py` l.58) et 342 (`gates.yml` l.287). Ce sont les seuls endroits du
  code et des workflows qui portent ces nombres (grep fichier par fichier, un niveau).
- **Mesure propre de la dépendance au réseau** (`outils/tentatives_cc.py`, suite entière dans un seul processus, sous la
  garde ; `sorties/tentatives-passe2.txt`) :
  - s2-harness : Ran 419, OK (skipped=2), `TENTATIVES` = 11 ;
  - s2bis : Ran 342, OK, `TENTATIVES` = 9 ;
  - ce sont exactement les appels des tests de garde, et les suites passent réseau coupé.
- **Sondes** : `sorties/sonde-garde-passe2.txt`, puis `sonde-garde2-passe2.txt` pour les formes que les tests ne montrent
  pas.
  - Refusés (+1) : `getaddrinfo(host=…)`, `getnameinfo` hors boucle, hôte positionnel avec `type=`, `host=` en octets, nom
    dans un sockaddr, `NI_NUMERICHOST` hors boucle, `asyncio` (`loop.getaddrinfo`), `getfqdn`.
  - Admis (+0) : `None`, `localhost`, `getnameinfo` local, sockaddr vide (TypeError de l'appel d'origine).
  - `sendmsg` reste une limite écrite.
- **Mutants propres** (`outils/mutants_c11_cc.py`, `sorties/mutants-c11-cc.json`) : 10, soit 5 formes par paquet ; 6 tués
  et 4 vivants :
  - K11-1 (deux fois) : hôte positionnel ignoré quand des mots-clés sont présents. C'est une forme réelle
    (`getaddrinfo("x", 443, type=…)`) qu'aucun test ne fixe : voir R-7.
  - K11-3 (deux fois) : `NI_NUMERICHOST` admis hors boucle, équivalent en sûreté. R-7 le fixe quand même, comme le veut la
    règle adjugée (« tout hôte non local »).

### R-7 (C-11) : faux positifs sur des appels invalides, et une forme réelle non fixée

**Constat.** Sonde : `sorties/sonde-garde2-passe2.txt`. Témoin sans garde : le même appel sous `python3` nu lève TypeError,
sous 3.11 et sous `python3.12`.

| appel invalide | sans garde | sous la garde de C-11 |
|---|---|---|
| `getnameinfo("192.0.2.1", 0)` | TypeError « must be a tuple » | ReseauInterdit vers **`'1'`**, inscrit (`tuple("192.0.2.1")[0]`) |
| `getnameinfo([…], 0)` | TypeError « must be a tuple » | ReseauInterdit, inscrit |
| `getnameinfo(sockaddr=…, flags=…)` | TypeError « takes no keyword arguments » | ReseauInterdit, inscrit |
| `gethostbyname(host=…)` et `gethostbyaddr(host=…)` | TypeError « takes no keyword arguments » | ReseauInterdit, inscrit |

Ces fonctions sont des fonctions C sans mots-clés. La garde change donc une `TypeError`, qui sort sans aucun réseau, en une
`BaseException`. Celle-ci échappe à `assertRaises(TypeError)` et ajoute une entrée fausse à `TENTATIVES`, qui sert de
mesure. Le commentaire de C-11 (« vide : l'appel d'origine juge ») ne vaut que pour le tuple vide. Enfin, la forme hôte
positionnel avec mots-clés n'est fixée par aucun test (K11-1 vivant).

**Forme exacte** : `propose/R-7-propose.diff`. Le bloc reste égal dans les deux paquets.
- Code :
  - `host=` n'est lu que pour `getaddrinfo` ;
  - `getnameinfo` ne lit que l'hôte d'un sockaddr en tuple non vide, sans mot-clé ;
  - toute autre forme est laissée à l'appel d'origine (TypeError) et rien n'est inscrit.
- Commentaire et docstrings des deux gardes.
- Tests de C-11 étendus dans les deux suites :
  - nouveaux refus : hôte positionnel avec `type=` ; `getnameinfo` numérique hors boucle ;
  - cinq formes invalides attendues en TypeError ;
  - `len(TENTATIVES) == n + 5`.
- Aucun test ajouté : les planchers restent 419 et 342.

**Vérifié** :
- Rouge : tests de R-7 contre les gardes de C-11, FAILED (failures=1) dans chaque suite (`sorties/rouge-vert-r7-cc.txt`).
- Vert : OK.
- Mutants adaptés (`outils/mutants_r7_cc.py`, `sorties/mutants-r7-cc.json`) : 16 tués sur 16, dont K7-1 (forme de K11-1) et
  K7-f (forme de K11-3).
- Sondes (`sorties/sonde-garde-r7-passe2.txt`) : formes invalides → TypeError, +0 ; formes valides inchangées.
- Mesure (`sorties/tentatives-r7-passe2.txt`) : 419 avec 13 entrées, 342 avec 11 entrées, toujours les seuls appels des
  tests de garde.

### R-8 (portée de C-11) : la troisième garde, `scripts/calib-actifs/tests/__init__.py`, reste à l'ancienne forme

**Constat.**
- Ce fichier porte la même garde (« forme de s2bis/tests/__init__.py »). Son bloc était égal octet pour octet à celui de
  s2bis à la tête et à l'état 20 (`cmp`), et il en diffère depuis DT5-21.
- `getaddrinfo(host=…)` et `getnameinfo` n'y sont pas gardés : la sonde donne `gaierror` du résolveur réel, +0.
- Sa docstring dit « une connexion, un envoi ou une résolution hors de la boucle locale lève ReseauInterdit », et n'écrit
  pas la limite `sendmsg`.
- L'ajout de 23:39:53 UTC parle de « deux gardes » et nomme `scripts/controle/tests/`, qui n'en porte aucune.
- Le fichier est épinglé par `scripts/calib-actifs/SHA256SUMS` (ligne 10). Le sha256 de ce `SHA256SUMS`, `1d0cae17…`, est
  épinglé au JOURNAL (README du lot l.34-37, E-CA-27, E-CA-28 ; `lancer.sh` refuse un dossier qui ne lui correspond pas).

**Forme exacte** : `propose/R-8-propose.diff`, appliqué après R-7.
- Bloc de garde de calib-actifs remplacé par celui de s2bis, de « `TENTATIVES = []` » à la fin : les trois blocs
  redeviennent égaux octet pour octet (`cmp`).
- Docstring : appels gardés, limites, alignement.
- `test_garde_reseau` de `tests/test_pages.py` étendu : `host=` et `getnameinfo` refusés et inscrits ; la mutation qui le
  rougit est nommée. Aucun test ajouté : le plancher reste 65.
- Les deux lignes du `SHA256SUMS` du lot sont recalculées (`sha256sum -c` OK). Le sha256 du `SHA256SUMS` passe de
  `1d0cae179ee000701fa4d8e47a8eaea22f9b9d825161d341fe05119357c52d4e` à
  **`a4a34b143c1973ffa84330af6c61a679f1d772b5ae924c4cb83f1bff2376a709`**.

**Décision à prendre par l'orchestrateur** : re-dater l'épingle du lot CALIB-ACTIFS au JOURNAL. Si R-7 n'est pas adoptée,
le bloc à recopier est celui de C-11, et la forme est à refaire.

**Vérifié** :
- Rouge : test de R-8 contre la garde de l'état 21, FAILED (failures=1), `['gaierror'] ×2`, 0 ERROR
  (`sorties/rouge-vert-r8-cc.txt`).
- Vert : OK, et la suite calib-actifs entière donne 65 OK.
- Sonde (`sorties/sonde-garde-r8-passe2.txt`) : `host=` et `getnameinfo` refusés, +1.
- Mutants K8-1 (`getnameinfo` non gardé) et K8-2 (`host=` ignoré) : tués (`outils/mutants_r8_cc.py`,
  `sorties/mutants-r8-cc.json`).

### Gates de la passe 2

Même outillage que la passe 1 : `jobs_cc.py` sous `isole.sh`, `--history` non lancé.

| gate | tête `094fa5d` (passe 1) | série DT5-1..21 | série + R-7 + R-8 |
|---|---|---|---|
| g5 : cas du hook / R-13 | 54 / vert | 57 / vert | 57 / vert |
| g1 : runners-epingles / workflows-yaml | — / — | conforme (7, 22) / 16 ok, conforme | idem |
| g1 : lint / R-1 / journaux-modele / docs-sha256sums | 227 / OK / conforme / 34, 295 | idem | idem |
| g3 : cas / `--tree` | 147 / 1064 | 147 / 1068 | 147 / 1068 |
| runner du vérificateur (5 jobs) | 137 ok ×5 | 137 ok ×5 | 137 ok ×5 |
| s2-harness / s2bis / sim-bis / calib-actifs / controle (`--egal`) | 415 / 341 / 279 / 65 / 26 | **419 / 342** / 279 / 65 / 36 | 419 / 342 / 279 / 65 / 36 |
| `cargo xtask verify` (VERDICT) / `cargo test -p xtask` | 8 VERT, 1 ROUGE / 81 et 9 | identiques (sortie 1 / 0) | non relancé (aucun Rust touché) |

Toutes les étapes lancées sortent en 0 (21 sur 21 dans les deux colonnes de droite, `sorties/j-copie2-*`, `j-prop2b-*`).

### Constats sans réserve (passe 2)

- **O-4.** L'ajout de 23:39:53 UTC nomme `scripts/controle/tests/` parmi les gardes. C'est un lapsus sans effet : DT5-21
  porte sur `s2-harness` et `s2bis`, comme le dit le message de l'orchestrateur. R-8 traite la troisième garde réelle.
- **O-5.** Une résolution vers la boucle locale est admise par construction : `getnameinfo(("127.0.0.1", 80), 0)` donne
  `('localhost', 'http')` par `/etc/hosts`. Sur une machine sans cette entrée, le résolveur pourrait interroger le DNS.
  Cela dépend de l'environnement, pas du code ; les tests emploient `NI_NUMERICHOST`.
- **O-6.** E-16 du générateur : DT5-17 écrit des limites que DT5-21 retire. L'état final est juste ; les fondre est au
  choix de l'orchestrateur.

### Écarts de la passe 2

- **E-12** : l'horloge a passé minuit pendant la passe ; les heures sont lues par `date -u`, en 2026-10-10 après 00:00.
- **E-13** : R-7 et R-8 ont été régénérés plusieurs fois avant leur forme finale. Les diffs versés sont régénérés et
  vérifiés, et leurs sha256 sont ceux de ce rapport. Raisons :
  - lignes de plus de 120 colonnes ;
  - fixation de K11-3 ;
  - rouge de R-8 d'abord en ERROR par `assertRaises`, ramené en FAIL par `AssertionError`.
- **E-14** : les mutants de R-8 ont d'abord tourné dans un script en ligne. Ce script est versé dans
  `outils/mutants_r8_cc.py` avec une docstring en tête ; le corps est identique.
- **E-15** : lecture de `scripts/calib-actifs` (README, `SHA256SUMS`, `lancer.sh` par grep, tests), hors de la série. C'est
  ce qui a fait trouver la troisième garde. J'ai cherché fichier par fichier, sur un niveau ; je n'ai fait aucune recherche
  récursive.

### Journal de provenance (passe 2)

**[lu]** : les pièces et fichiers listés ci-dessus.

**[2nd]** : l'épingle du lot CALIB-ACTIFS au JOURNAL, par le README du lot. Je n'ai lu ni la ligne du JOURNAL ni sa
valeur, seulement le sha256 actuel du `SHA256SUMS`.

**Commandes**, sorties sous `sorties/` :
- empreinte de la série et `cmp` ;
- copies : `copie.sh` ×2 ;
- rouges et verts : `rouge_c11_cc.sh`, `rouge_r7_cc.sh`, et le rouge de R-8 (dans `sorties/rouge-vert-r8-cc.txt`) ;
- sondes : `sonde_garde.py`, `sonde_garde2.py`, `sondes_cc.py` ;
- mesure : `tentatives_cc.py` ;
- mutants : `mutants_c11_cc.py`, `mutants_r7_cc.py`, `mutants_r8_cc.py`, `mutants_cc2.py` ;
- jobs : `jobs_cc.py` ×3 (`copie2`, `prop2` partiel, `prop2b`) ;
- cargo : `cargo_cc.sh copie2` ;
- réserves : `propose_c11_cc.py`, `propose_r8_cc.py`.

**Chiffres recomptés** : par les sorties (Ran, `TENTATIVES`, tués et vivants, sha256).

### Clôture de la passe 2

Fin à 2026-10-10 00:20:11 UTC (`date -u`), heure de cet ajout ; `NOTES.md` porte la dernière entrée. Dépôt réel à
`094fa5d`, `status` vide, jamais écrit ; 0 processus à moi ; `tmp/` et les dépôts jetables supprimés (`df` : 6,8 G
libres). Aucun commit, aucune poussée, aucun accès réseau, `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée, aucune pièce de D.2
ouverte. `SHA256SUMS` du dossier recalculé.
