# Rapport du worker — réserve R-1 de l'accord de P1 : OUT-1a, OUT-1b (transcrit)

> Transcription par l'orchestrateur le 2026-10-06 02:01:37 UTC du rapport rendu par message par le worker (agent acdbc4cdaa458d077) ; contrôle FM-1.1 : fragments_l51_l14 = 0. Texte du worker ci-dessous, sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

## Rapport du lot R-1 : réserve R-1 de l'accord de P1 (OUT-1a, OUT-1b)

**Gate 0.** Le modèle résolu est `claude-opus-5-5` (préfixe conforme), lu dans le contexte système de la session. L'effort `max` vient de la fiche ; je ne peux pas le mesurer de l'intérieur.
**Horloge.** Début à 01:30:06 UTC, fin à 02:00:15 UTC le 2026-10-06 (`date -u`).
**Base.** `git rev-parse HEAD` donne 11b9d4375a411020f55feaf814efdc51b089913e, la base du brief. Les quatre fichiers de base extraits par `git archive` ont le même sha256 que les blobs de `git show 11b9d43:…`.

### Verdict

Les deux items sont fermés côté code. La sortie est verte sur 3.10 à 3.13 en `-X dev -W error`, sauf la suite S2 sous 3.10, rouge connu. Le contre-contrôle exigé par R-1 reste à faire par un réviseur tiers.

### Décisions (Q-n)

- **Q-1 (RUNNER-SORTIE-1) : j'ai choisi (b).**
  - Le runner ne charge plus jamais le vérificateur. Un sous-processus (`--serveur`, même fichier) le charge, écrit « pret », puis répond par une ligne JSON entière à chaque attribut ou appel. Le runner garde ses fonctions et ses cas ; seul `v` devient un mandataire.
  - Cas d'échec :
    - sortie au chargement (dont `os._exit(0)`) : sortie 3, « vérificateur illisible » ;
    - réponse absente (`sys.exit(0)` ou `os._exit(0)` pendant un cas), tronquée, illisible, ou exception levée : `Rompu`, sortie 1, message « ÉCHEC vérificateur rompu : … ».
  - Pourquoi pas (a) : avec un résumé signé par l'enfant, le comptage et le jugement restent dans le processus qui exécute le vérificateur, et ce code peut lire le protocole et forger le résumé. Avec (b), le vérificateur ne fournit que des valeurs, et le runner compte et juge seul.
  - L'enfant reçoit les options `-X dev` et `-W` du parent.
  - Rien n'est passé par `pass_fds` (POSIX seul) : le canal passe par les pipes texte.
- **Q-2 : compte exact `CAS = 97`**, sur le modèle de `--egal`. La sortie finale est `1 if KO else bilan(OK_, KO, CAS)`. Ce choix vient du mutant A8 : avec `sys.exit(bilan(…))` seul, un `bilan` faux masquait l'échec de son propre cas.
- **Q-3 (ENREG-VERIF-COMMIT-1)** :
  - Le vérificateur du commit est comparé au fichier de l'outil (`VERIF`), pas à une épingle. `verdict-suite-s2.py` change à chaque relèvement de PLANCHER, et une épingle vivrait dans le même arbre que `VERIF` sans rien ajouter à la confiance.
  - La consignation se fait par l'entrée `enforcement/verdict-suite-s2.py` de `tree.sha256`. Le schéma v1 est inchangé.
  - La comparaison a lieu à l'écriture (refus nommé avant tout run) et à la lecture (`refus (vérificateur)`, seulement si une commande de JOBS a été lancée).
  - `.gitattributes` impose `eol=lf` : les octets de l'arbre de travail égalent le blob, y compris sous Windows.
  - Conséquence : un enregistrement ancien relu par un outil dont le vérificateur a changé est refusé et nommé. Il faut alors le relire avec l'outil de son commit.
- **Q-4 : ligne du job lancée en `-I`.** C'est mesuré sous 3.10 et 3.13 : un `subprocess.py` posé à côté du vérificateur est importé à la place de la bibliothèque standard. Avec des octets égaux, la seule comparaison des sha256 ne suffisait donc pas. La commande consignée devient `[python, "-I", "-B", …]`, et l'attendu du test existant suit (resserré, pas affaibli).
- **Q-5 : `ligne_du_job` rattrape `BaseException` au chargement** et la nomme par `repr`. La comparaison des sha256 est dans `enregistrer`, pas dans `ligne_du_job`, pour que les leurres CB-18 (arbre factice qui n'a que `gates.yml`) gardent leurs verdicts.

### Diffs (série, base 11b9d43, `patch -p1` vérifié : les quatre fichiers obtenus sont égaux à ceux de la copie)

| Diff | Contenu | Lignes | sha256 |
|---|---|---|---|
| OUT-1a | runner seul | +151 / −17 | 6c5c43c4…c0e5 |
| OUT-1b | `oracle_record.py` +20, `test_oracle_record.py` +55, `verdict-suite-s2.py` +1 (PLANCHER 406 → 407) | +76 / −12 | b9235596…6451 |

- `gates.yml` est inchangé : ce n'était pas nécessaire.
- La suite s2bis est inchangée (255 tests), donc pas de METRIQUES. La suite S2 passe de 406 à 407 tests ; le runner de 87 à 97 cas.

### Tests et rouge montré

- Les 87 noms de cas du runner sont gardés à l'identique, et aucun test de l'enregistreur n'est retiré. Seule modification d'un test existant : l'attendu `-I` du test `test_suites_s2bis_et_sim_bis_par_la_ligne_du_job`, plus strict qu'avant.
- **Runner, cas neufs** :
  - R-03 : `os._exit(0)` au chargement, sortie 3 ;
  - R-04 : `sys.exit(0)` pendant un cas, réponse absente, sortie 1 ;
  - R-05 : `os._exit(0)` pendant un cas, réponse absente, sortie 1 ;
  - R-06 : réponse sans fin de ligne, réponse tronquée, sortie 1 ;
  - R-07 : exception pendant un cas, « a levé », sortie 1 ;
  - R-08 : copie du runner avec le vérificateur réel et CAS + 1, sortie 1. Les copies, lancées avec `--copie`, ne refont aucune copie.
  - B-01 à B-04 testent `bilan`.
  - **Rouge** sur le mécanisme de base : R-03 à R-06 sortent en 0 (le trou lui-même), R-07 sort en 1 sans nommer l'exception, R-08 lève `NameError` (CAS absent).
- **Enregistreur, test neuf** `test_verificateur_du_commit_egal_a_celui_de_l_outil` :
  - témoin honnête conforme ;
  - L2 refusé avant toute écriture ;
  - leurre `subprocess.py` : exit 1 consigné, commande en `-I` ;
  - `refus (vérificateur)` à la lecture ;
  - RuntimeError, SystemExit et gates.yml non UTF-8 au chargement : refus nommés.
  - **Rouge** sur la base : 2 FAIL, dont « ValueError not raised » à l'étape L2.

### Mutants (classés par la sortie : 1 tué, 0 étape suivante, autre sortie ou plus de 300 s FATAL ; réseau isolé)

**OUT-1a**, classés par le runner puis la ligne s2bis :

| Mutant | Tué par |
|---|---|
| A1 « pret » : fin de flux admise | R-01 à R-03 |
| A2 réponse absente lue comme None | R-04 |
| A3 réponse sans fin de ligne admise | R-06 |
| A4 exception lue comme None | R-07 |
| A5 SystemExit rattrapée dans l'enfant | R-04 |
| A6 sorties du vérificateur sur le canal | le run normal (réponse illisible) |
| A7 `bilan` sans le compte | B-02, B-03 |
| A8 `bilan` sans les échecs | vivant à la campagne 1 ; tué par B-04 après correction |
| A9 sortie finale sans `bilan` | R-08 |

Campagne 2 : **9 tués sur 9, 0 FATAL.**

**OUT-1b**, classés par le runner puis la ligne S2 (`--egal`) : **10 tués sur 10, 0 FATAL.** Le runner sort en 0 pour tous ; la ligne S2 tue.

| Mutant | Test qui le tue |
|---|---|
| B1 comparaison jamais faite | `test_verificateur…` seul |
| B2 comparaison sur gates.yml | `test_suites…`, `test_verificateur…` |
| B3 comparaison au fichier du commit | `test_verificateur…` |
| B4 chargement : `except (OSError, SyntaxError)` | `test_verificateur…` |
| B5 chargement : `except Exception` | `test_verificateur…` |
| B6 `-I` retiré | `test_suites…`, `test_verificateur…` |
| B7 lecture sans contrôle | `test_verificateur…` |
| B8 lecture sur les runs `suite` seuls | `test_verificateur…` et 6 autres |
| B9 exception non nommée | `test_verificateur…` |
| B10 PLANCHER non relevé | ligne S2 : « Ran 407 > plancher 406 » |

Ma première formulation de B1 tuait large ; je l'ai rejouée en forme précise (`and False`).

### Leurres

- **CB-18** (`leurres_cc.py`, `leurres_cc2.py`, `leurres_fetch.py`, copie cc5 ; cc à cc5 ont les mêmes sha256) : sorties identiques entre base et copie.
- **G2 d'intégration** (`leurres_enregistreur.py`) : seul L2 change. Il passe de « exit 0 ; conforme » à « vérificateur du commit enforcement/verdict-suite-s2.py (sha256 9f643924…) autre que celui de l'outil … — refus ». L0, L0b, L1 et L3 sont inchangés.

### Matrice (`-X dev -W error`, réseau isolé)

| Python | runner | s2bis | S2 |
|---|---|---|---|
| 3.10 | 97 ok | Ran = 255, conforme | rouge connu PY310-1 : 77 FAIL, 3 ERROR, comme la base mesurée sous 3.10 à 406 tests ; le test neuf passe |
| 3.11 à 3.13 | 97 ok | Ran = 255, conforme | Ran = 407, conforme |

Aucune ligne « Exception ignored » ni « Warning: » dans les sorties. Les copies R-03 à R-07 lancées à la main rendent une seule ligne nommée sur stderr.

### xtask

`cargo --locked xtask verify` sur la copie, cible dédiée, réseau isolé, 41 s :
- S-G1 à S-G8 VERT (S-G7a compris) ; fmt, no_std et clippy VERT ;
- S-G9 ROUGE, seule violation `docs/17-modele-de-menace.md:70`. Elle pointe vers un fichier de `docs/rapports/`, exclu de la copie par le brief, comme à la G2 d'intégration §6 ;
- verdict global ROUGE.

### Forme

- Aucune ligne ajoutée de plus de 120 caractères.
- Octets 92 : 0 dans OUT-1a ; 2 dans OUT-1b. Ce sont les deux échappements de `r"^refus \(vérificateur\) : "`, écrits par gabarit et contrôlés au compte (64 → 66 dans le fichier de test).
- R-13 : 0 marqueur ; contrôle positif : 1.
- R-8 : bibliothèque standard seule (`atexit` et `json` ajoutés).

### Items à former (PAROXYSME)

1. **SHOGEN-S2BIS-SUITE-MASQUE-UNITTEST-1** (nom proposé). C'est mesuré sous 3.10 et 3.13 : un `unittest.py` à la racine du dossier de la suite masque le module `unittest` de la bibliothèque standard pour `-m unittest`. La suite relue peut alors imprimer un résumé conforme, sans que le vérificateur, l'enregistreur ni le job de CI le voient. Hors de la liste fermée. Déclencheur proposé : avant la G2 de P2. Prix [inféré] : refus d'un `unittest*` à la racine de la suite, ou lancement de la suite qui l'exclut.
2. **Limites écrites, sans correction.** [inféré] pour les trois premières :
   - un vérificateur qui reconnaît les entrées des cas peut rendre les valeurs attendues : c'est une limite inhérente aux tests, et la lecture du diff du vérificateur reste nécessaire ;
   - le chemin Windows n'est pas éprouvé ;
   - un `os._exit(0)` dans le `VERIF` de l'outil arrête l'enregistreur en 0 sans rien écrire. Ce n'est pas une fausse preuve, puisqu'il n'y a rien à vérifier, mais le code 0 de la CLI trompe ;
   - un appel du vérificateur qui ne rend jamais la main bloque le runner jusqu'au `timeout-minutes` du job, comme avant le lot.

### Écarts

- **E-1** : mon premier `git status --short` a été lancé sans `--no-optional-locks`. C'était en lecture seule, mais l'index a pu être rafraîchi.
- **E-2** : deux essais lancés hors `isole.sh`, sans usage du réseau : l'expérience du masquage et les copies R-03 à R-07 lancées à la main.
- **E-3** : les mutants OUT-1b sont classés par le runner puis la ligne S2, et non par la ligne s2bis, parce que les tests de l'enregistreur sont dans la suite S2. C'est le précédent du worker des corrections de P1.
- **E-4** : A8 était vivant à la campagne 1. Le code a été corrigé puis la campagne entière rejouée ; les deux campagnes sont versées.
- **E-5** : pour la matrice, `$!` a rendu 7508 à 7515 alors que les vrais PID étaient 7512 à 7515, relevés par `ps`.
- **E-6** : une commande de nettoyage par `sh -c` a été refusée par le contrôle de sécurité. Je l'ai refaite par un script et des chemins littéraux, sans contourner le contrôle.

**PID :**
- 740 et 4279 (S2 base et S2 copie sous 3.12, valeurs rendues par `$!`) ;
- 7150 et 7832 (campagnes OUT-1a) ; 8242 (campagne OUT-1b) ;
- 7512 à 7515 (matrice) ;
- 18950 (xtask) ; 18960 (S2 de base sous 3.10).

Nettoyage fait : copies `base/` et `neuf/`, `mut/`, `tmp/`, cible cargo, liens `copie`.

### Journal G1

**Sources lues [lu]** :
- BRIEF-R1.md ;
- `docs/adr-0029/g0-collecte/G0-COLLECTE-RECALC-DEPLOI.md`, en entier ;
- ANNEXE-B l.1143-1173 (B.71, B.72) ;
- ACCORD-P1.md l.1-60 ;
- G2-P1-INTEG-transcrit.md §6 (l.183-211), plus les lignes « L2 » repérées par grep ;
- CONTRE-CONTROLE l.55-110 ;
- RAPPORT-CORRECTIONS l.56-57, 84, 87, 100, 106, par grep ;
- en entier : runner, vérificateur, `oracle_record.py`, `test_oracle_record.py`, `leurres_enregistreur.py` ;
- en partie : `leurres_cc.py`, `leurres_cc2.py`, `leurres_fetch.py`, `gates.yml` (grep), `.gitattributes`, `rust-toolchain.toml`, `.cargo/config.toml`, `isole.sh`.

Aucune pièce de D.2, aucun dossier interdit, aucun `*.jsonl` lu. Aucune recherche récursive sur `docs/`, le dépôt ou le scratchpad.

**Commandes et sorties** : elles sont dans `preuves/` (voir ci-dessous). Les chiffres cités ici (97, 87, 407, 255, 77/3, mutants) sont recomptés sur ces sorties.

### Fichiers

Dossier : `<scratchpad>/s2bis/outillage/`
- `livrables/` : OUT-1a.diff, OUT-1b.diff, fichiers-finaux.sha256, fichiers-base-11b9d43.sha256
- `SHA256SUMS` : 46 entrées OK, sha256 `f17ae9c0…dffdc`
- `NOTES.md`
- `preuves/` : rouge-*, matrice/*, leurres/*, mutants-*, copies-R03-R07.txt, xtask-verdicts.txt
- `outils/` : mutants.py, mutants_tests.py, mutant_un.py, forme.py, matrice.sh, chrono.sh
