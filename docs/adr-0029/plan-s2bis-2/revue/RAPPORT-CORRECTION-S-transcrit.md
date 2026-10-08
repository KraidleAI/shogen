# Correction complémentaire de PLAN-S2BIS-2 : `python3 -S` (Q-CORR-5) (transcrit)

> Transcription par l'orchestrateur le 2026-10-08 15:12:11 UTC de la section 13 du rapport écrit par le worker de correction (agent a059a9ec1498192e1, reprise) dans `<scratchpad>/s2bis/plan2/corr/RAPPORT-CORRECTIONS.md` (sha256 0039aed2…) ; contrôle FM-1.1 : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte du worker ci-dessous, sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

## 13. Correction complémentaire du 2026-10-08 : `python3 -S` (adjudication de Q-CORR-5)

- **Gate 0** : modèle résolu `claude-opus-5-5` (même worker, effort max).
- **Horloge** (`date -u`) : message de l'orchestrateur reçu, passe ouverte le 2026-10-08 à 14:39:44 UTC ; close à
  15:09 UTC (§13.10).
- **Base** : tête `e6657dcc3154bf2d35c69b84d9deae1385e702a7`, `git status --short` vide, relevées à l'ouverture et à la
  clôture.
- **Demande** : message de l'orchestrateur (Q-CORR-5 adjugée : scripts lancés par `lancer.sh` en `python3 -S`), lu en
  entier ; mêmes règles et interdits durs que le brief corr.
- **Pièce lue [lu]** : `cc/CONTRE-CONTROLE-P2R-transcrit.md` (211 l., sha256 `dac5afca…d15b`), en entier : verdict
  CONFORME ; sous `env -i`, site utilisateur actif (`/root/.local/lib/python3.11/site-packages`, sans `.pth`) ; `.pth`
  système exécutés à chaque démarrage, `-s` seul ne les écarte pas ; en `python3 -S`, sorties identiques à l'octet.

### 13.1 Place, diffs touchés, épingle neuve

- **Place : P2R-6a** (le diff de C-1), +149 / −38 après correction, sous 200 : pas de P2R-6c.
- **Diffs touchés : P2R-6a et P2R-6b seulement** ; P2R-0a à P2R-5 identiques à l'octet (`cmp` contre les diffs
  d'avant cette passe).

| diff | avant (§2) | après | tests | sha256 après |
|---|---|---|---|---|
| P2R-6a | +132 / −37, `23ef1e17…15ed` | **+149 / −38** | 32 | `b320749440bbed37fb5c49e3e271d65faeffacb2a1f6b6f390757816145ca075` |
| P2R-6b | +184 / −40, `8b9660a9…d2f6` | **+184 / −40** | 35 | `72dbbfc579ea5cdbfb958f3287bd63952ff9bd68403d46e1edad141edc17847a` |

- P2R-6a (par fichier, `git apply --numstat`) : `lancer.sh` +24 / −13, `tests/test_lancer.py` +115 / −20, `README.md`
  +7 / −2, `SHA256SUMS` +3 / −3. Delta de cette passe : `-S` aux deux heredocs et à la ligne des scripts (ligne de P2R-5
  désormais modifiée), commentaire de tête (4 lignes au lieu de 3), README point 2 (5 lignes au lieu de 4), test LAN-14
  (14 lignes, ligne blanche comprise), sommes : +17 et −1 par rapport au §2.
- P2R-6b : parmi ses lignes + et −, seules changent les quatre lignes des deux heredocs (− et +, qui portent `-S`) et
  les six lignes de `SHA256SUMS` (`README.md`, `lancer.sh`, `tests/test_lancer.py`) ; le reste n'est que contexte.
- Série : 1 812 lignes ajoutées, 95 retirées ; lot final de 1 717 lignes (13 fichiers ; `wc -l` = 1 717).
- **Épingle neuve** : sha256 de `scripts/plan-s2bis-2/SHA256SUMS` =
  **`ffe6e5aaf683a782200d65c4ba1541556917fe788afce000d8c9ec5332a4d005`** (12 lignes, `sha256sum --strict -c` 12/12 sur
  l'arbre de la série rejouée depuis une base neuve). Elle **remplace `fe46ebd6…f36f`** (§1, §6), caduque. Épingle
  intermédiaire après P2R-6a : `0d8750bd…64db` (au lieu de `c2b121b3…d83e`) ; après P2R-5 : inchangée (`893024ab…eb17`).
- Fichiers changés dans le lot : `README.md` `b9ba5a5f…` (était `d77a28a0…`), `lancer.sh` `586f93f3…` (était
  `0293fdeb…`), `tests/test_lancer.py` `115d4eed…` (était `d92c6526…`) ; les neuf autres inchangés.

### 13.2 Mesure : `-S` et les autres drapeaux, sous 3.11, 3.12, 3.13

`outils/drapeaux_S.py`, `journal/drapeaux-S.json`. Chaque interpréteur tourne sous l'environnement du lanceur (`env -i`,
PATH, LC_ALL=C, PYTHONDONTWRITEBYTECODE=1, PYTHONPYCACHEPREFIX vers un dossier neuf, PYTHONHASHSEED) ; un venv jetable
sous `corr/tmp`, dont le `bin` passe en tête du PATH, porte un `.pth` hostile qui écrit une marque.

| forme | module `site` | site-packages dans `sys.path` | `.pth` hostile | `-X dev`, `-W error` | `hash('abc')` | `sys.pycache_prefix` |
|---|---|---|---|---|---|---|
| `-B` (système) | chargé | 3 / 2 / 1 (3.11 / 3.12 / 3.13 ; en 3.11 le site utilisateur `/root/.local/…` compris) | — | — | graine 0 : H0 | posé |
| `-S -B` | non chargé | 0 | — | — | graine 0 : H0 | posé |
| `-S -B`, graine 1 | non chargé | 0 | — | — | graine 1 : H1 | posé |
| `-S -B -X dev -W error` | non chargé | 0 | — | `dev_mode` vrai ; `warnoptions` = `default, error` ; premier filtre `error` | graine 0 : H0 | posé |
| venv, `-B` | chargé | 1 (venv) | **exécuté 2 fois** | — | graine 0 : H0 | posé |
| venv, `-I -B` (heredocs de C-1) | chargé, sans site utilisateur | 1 (venv) | **exécuté 2 fois** | — | aléatoire (graine ignorée sous `-I`) | non (ignoré sous `-I`) |
| venv, `-S -B` | non chargé | 0 | non | — | graine 0 : H0 | posé |
| venv, `-I -S -B` | non chargé | 0 | non | — | aléatoire (sous `-I`) | non (sous `-I`) |

H0 = −4594863902769663758 ; H1 = −4667308735975688587 ; `-B` (`dont_write_bytecode` = 1) partout ; code 0 partout.

- **Combinaison.** `-S` ne retire que le module `site` et ce qu'il charge : site-packages système et utilisateur,
  fichiers `.pth`, et le `sitecustomize` de la distribution (importé en `-B`, plus en `-S -B` : mesure complémentaire de
  15:05, 3.11 à 3.13 ; aucun `usercustomize` présent). Sous `-S`, `-B`, `-X dev` et `-W error` restent en effet ;
  `PYTHONHASHSEED` aussi (même hachage avec et sans `-S` pour une même graine, graines 0 et 1 distinctes), comme
  `PYTHONPYCACHEPREFIX` (`sys.pycache_prefix` posé). Les huit formes donnent les mêmes valeurs sous 3.11, 3.12 et
  3.13, à deux exceptions près : le nombre de site-packages sans `-S` (3, 2, 1) et le hachage aléatoire des formes en
  `-I`.
- **Heredocs.** Ils restent en `-I` : `PYTHONHASHSEED` et `PYTHONPYCACHEPREFIX` y sont ignorés (mesuré : hachage
  aléatoire, `sys.pycache_prefix` non posé), comme depuis C-1, sans effet sur leurs sorties (clés triées, accès
  directs, aucune itération d'ensemble). `-I` n'arrête pas le `.pth` (le contre-contrôle l'avait vu pour `-s`) : d'où
  `-S` aussi aux heredocs (Q-CORR-6).
- **Deux exécutions par démarrage** (vérifié par la pile, `.pth` jetable imprimant `traceback.extract_stack`, 3.11 à
  3.13) : `site.main` parcourt le site-packages du venv deux fois, par `venv()` puis par `main()`, et `addsitedir` relit
  les `.pth` d'un dossier déjà connu. Ma note de 14:40 l'attribuait à tort au lien `lib64` (rectifiée au NOTES).
- Un `sitecustomize` hostile posé dans le venv reste sans effet : celui de la distribution, dans la bibliothèque
  standard, passe avant les site-packages ; le test porte donc sur un `.pth` (E-12).

### 13.3 Code et règle

- `lancer.sh` : les deux lectures de `parametres.json` en `python3 -I -S -B -` ; les scripts en `"${PY[@]}"
  PYTHONHASHSEED="$graine" python3 -S -B` (liste fermée de C-1 inchangée) ; commentaire de tête (Q-CORR-5).
- README, Lancement, point 2 (règle du code exécuté), ajout : « Les `parametres.json` sont lus par `python3 -I -S` ; les
  scripts tournent en `python3 -S -B` sous `env -i` […] : ni site-packages (système ou utilisateur), ni fichier `.pth`,
  ni bytecode voisin ne sont lus. »

### 13.4 Test T-P2-LAN-14 et rouge

- `tests/test_lancer.py`, `test_site_hostile` (P2R-6a) : venv jetable (`python3 -I -m venv --without-pip`) dans le
  dossier temporaire du test, sous TMPDIR ; un `zz_hostile.pth` dans son site-packages écrit une marque ; le `bin` du
  venv passe en tête du PATH donné au lanceur. Attendu : code 0, marque absente, quatre sorties. Bibliothèque standard
  seule (aucune dépendance neuve, R-8 sans objet), aucun réseau, rien hors du dossier du test.
- **Préfixe plutôt que HOME** : sous `env -i`, ni HOME ni PYTHONUSERBASE n'atteignent les scripts et Python retrouve le
  HOME par `pwd` ; un site utilisateur hostile ne s'éprouverait qu'en écrivant dans le HOME réel, ce qui est exclu. Le
  site utilisateur passe par le même module `site` que le `.pth` ; son retrait par `-S` est mesuré (§13.2, 3.11 : présent
  en `-B`, absent en `-S -B`) sans rien écrire.
- **Rouge** (`journal/rouge-S-LAN-14.txt`) : LAN-14 ajouté à P2R-6a avant le code `-S` : `AssertionError: Tuples
  differ: (0, True, 4) != (0, False, 4)` ; Ran 32, FAILED (failures=1). Vert après le code : 6a 32 tests, 6b 35 tests.

### 13.5 Mutants

| mutant | substitution dans `lancer.sh` | test qui le tue | à l'état de P2R-6a | état final |
|---|---|---|---|---|
| M-P2R6-18 | scripts sans `-S` | LAN-14 | TUÉ (sortie 1) | TUÉ |
| M-P2R6-19 | premier heredoc sans `-S` | LAN-14 | TUÉ (sortie 1) | TUÉ |
| M-P2R6-20 | second heredoc sans `-S` | LAN-14 | TUÉ (sortie 1) | TUÉ |

- À l'état de P2R-6a (`journal/rouge-S-P2R-6a.txt`) : chacun `(0, True, 4) != (0, False, 4)` ; témoin non muté : sortie
  0, 32 OK.
- **Adaptations déclarées** (motif réécrit sur la forme à `-S`, même sens) : M-P2R6-4 et M-P2R6-5 (heredocs sans `-I`),
  M-P2R6-10 (stderr du premier heredoc rendu à l'écran) ; M-P2R4-6 du générateur, comme au §5.

Campagnes sur l'état final (`snap/P2R-6b`, `outils/mutants.py`, borne 300 s par mutant, classement par la sortie du
runner : 0 VIVANT, 1 TUÉ, autre FATAL ; témoins de 35 tests verts au début et à la fin ; restauration contrôlée par
sha256) :

| campagne | mutants | tués | vivants | FATAL | PID | heures (UTC) | journal |
|---|---|---|---|---|---|---|---|
| G2 rejouée (G-14 adapté) | 27 | 26 | 1 : G-05, équivalent (§5) | 0 | 22682 | 14:45:50–14:50:17 | `mutants-final-S-g2.json` |
| corrections (36 + 3 neufs) | 39 | 39 | 0 | 0 | 28778 | 14:50:17–14:56:00 | `mutants-final-S-corr.json` |
| générateur (M-P2R4-6 adapté) | 71 | 71 | 0 | 0 | 2552 | 14:56:00–15:06:04 | `mutants-final-S-gen.json` |
| **total** | **137** | **136** | **1 (G-05, équivalent)** | **0** | | | |

Enveloppe `sh` 22681 (`setsid` 22680) ; fins constatées en sondant les PID. Codes du runner : 1 pour chaque tué, 0
pour G-05, aucun autre ; copie de campagne restaurée égale à `snap/P2R-6b` (diff -r vide).

### 13.6 Suite, DET-1, bout en bout, xtask, forme

- **Suite du lot** (`outils/suite.sh`, réseau coupé) : 35 tests verts sous 3.11, 3.12, 3.13 × `PYTHONHASHSEED` 0 et 1,
  en `-X dev -W error`, 0 ligne d'avertissement (`journal/suite-finale-S.txt`) ; 3.10 : échec d'import connu
  (`hashlib.file_digest`, PY310-1 ; `journal/suite-py310-S.txt`).
- **DET-1** seul, verbeux, mêmes 6 combinaisons : 6 × « Ran 1 test, OK » (`journal/det1-S.txt`).
- **Instantanés** : P2R-6a (32 tests) et P2R-6b (35 tests) verts ; les neuf autres inchangés.
- **Série** rejouée depuis une base e6657dc neuve : 11 diffs sans retouche (`--check`, `--whitespace=error-all`), chaque
  état égal à `snap/P2R-x` (diff -r), `sha256sum -c` 12/12.
- **s2-harness** (copie du dépôt à e6657dc, réseau coupé, au premier plan, commande de la fiche) : Ran 407, OK
  (skipped=2), sortie 0, 15:06:53–15:07:49 ; le lot ne touche aucun de ses fichiers.
- **Bout en bout sur fixtures** (`outils/e2e.py`, dépôt jetable, vrais scripts ; `journal/e2e-S-avant.json`,
  `journal/e2e-S-apres.json`) :

| scénario | avant `-S` (état P2R-6b du §4) | après |
|---|---|---|
| S0 nominal | 0 ; sorties `SHA256SUMS` `6b70a712…`, `fiv_unites.txt` `58d23c28…`, `intervalles.txt` `b6244d02…`, `masque_j28.txt` `c9e65300…` ; égales au lancement direct | 0 ; **mêmes quatre sha256, à l'octet** ; égales au lancement direct |
| S24 `.pth` hostile, venv en tête du PATH | 0, **12 exécutions** : 4 dans les heredocs (2 × 2), 8 dans les scripts (2 scripts × 2 passes × 2) | 0, **aucune** |
| S8, S9, S22 (lot et PLAN-S2BIS), S19, L1 | comme au §4 | inchangés |

- **xtask** (copie de e6657dc et lot final) : S-G1 à S-G8 VERT ; S-G9 ROUGE, 1 violation (`docs/17-modele-de-menace.md:70`,
  connue) ; fmt, no_std, clippy VERT ; global ROUGE par S-G9 seule, comme au §1 (`journal/xtask-verdicts-S.txt`, lignes
  de verdict seules).
- **Forme** (`outils/forme.py`) : 13 fichiers du lot et 11 diffs : 0 octet 92, 0 tabulation, 0 retour chariot, 0 ligne
  de plus de 120 caractères, 0 TODO ni FIXME.

### 13.7 Questions, items, écarts

- **Q-CORR-5 : close par l'adjudication** ; la réserve du §7 (« `-s` non posé aux scripts ») tombe : `-S` retire aussi le
  site utilisateur.
- **Q-CORR-6 (serrage au-delà de la lettre).** La décision vise « les scripts lancés par `lancer.sh` » ; la mesure montre
  que les heredocs en `-I -B` exécutent aussi le `.pth` hostile (4 des 12 exécutions de S24). J'ai posé `-S` aussi aux
  deux heredocs : même vecteur, même diff, un mutant chacun (M-P2R6-19, M-P2R6-20). C'est un serrage ; s'il est jugé hors
  périmètre, il se retire avec ces deux mutants, sans toucher le reste.
- **SHOGEN-PLAN-S2BIS-2-EPINGLE-INTERPRETE-1 (précisé).** `-S` ferme site-packages (système et utilisateur) et `.pth`.
  Reste hors épingle le `python3` trouvé dans PATH lui-même : binaire et bibliothèque standard de son préfixe. LAN-14 le
  montre : le `python3` du venv placé en tête du PATH est bien celui qui tourne, seul son site est neutralisé. Restent
  aussi `git`, `tar`, `sha256sum`. Construction : consigner au JOURNAL, à l'épinglage, le chemin, la version et le sha256
  de `python3` et la version de `git`, ou faire appeler par le lanceur un interpréteur à chemin absolu épinglé. Prix :
  deux lignes de procédure ou une ligne de lanceur avec son test. Déclencheur : épinglage au JOURNAL.
- **E-11.** Suite en échec à l'import à 14:43 : la copie de e6657dc et l'extraction de `f35a70c` avaient été retirées
  à la clôture précédente ; ré-extraites (7 exclusions, absences contrôlées) ; ce passage n'est pas compté comme rouge.
- **E-12.** Premier dessin du test avec un `sitecustomize` hostile : sans effet (§13.2) ; remplacé par un `.pth` avant
  tout rouge compté.
- **E-13. Barres obliques inverses tapées** (comme E-1) : une séquence octale (barre suivie de 012) dans un `printf`
  mort d'une commande de vérification, dont la sortie allait vers `/dev/null` (aucun fichier écrit par elle ; la même
  commande a affiché un `sys.path` déformé par un `replace` de `sys.argv[0]`, qui valait `-c`) ; neuf séquences de saut
  de ligne dans les littéraux Python d'une commande d'édition du brouillon de cette section, arrivées intactes (chaque
  motif trouvé exactement une fois, sinon la commande s'arrêtait). Contrôle sur les octets écrits : 0 octet 92 dans le
  lot, les diffs, mes outils, NOTES.md et ce rapport. Les éditions suivantes passent par l'outil d'édition, sans
  commande.
- **E-14.** Cause des deux exécutions du `.pth` mal attribuée dans ma note de 14:40 (lien `lib64`) ; rectifiée par la
  pile (§13.2) et au NOTES ; les comptes mesurés ne changent pas.

### 13.8 Journal de provenance (G1) de cette passe

**Lu [lu]** : message de l'orchestrateur ; `cc/CONTRE-CONTROLE-P2R-transcrit.md` (211 l.) ; `lancer.sh`, `README.md`,
`tests/test_lancer.py` de `snap/P2R-6a` et `snap/P2R-6b` ; mes outils et journaux. **Mesuré [calc]** (et non tiré d'une
documentation) : tout le comportement de `-S`, `-I`, `-B`, `-X dev`, `-W error`, `PYTHONHASHSEED`,
`PYTHONPYCACHEPREFIX`, `site` et `sitecustomize` décrit au §13.2, et la double lecture des `.pth` (pile). **Non lu
[abs]** : comme au §10 ; aucune pièce neuve ouverte.

**Commandes et sorties** (heures `date -u`) : 14:39:44 relevé de base ; 14:40 mesure des drapeaux (24 lancements) ; 14:42
rouge LAN-14 ; 14:43 E-11, ré-extraction ; 14:44 suite 3.11 à 3.13 × 0/1 et 3.10, M-P2R6-18 à 20 à l'état de 6a ; 14:45
diffs régénérés (`outils/diffs.sh`, dépôt git jetable, `write-tree` et `diff-tree`, aucun commit) ; 14:46 listes des
campagnes (`outils/listes.py`), bout en bout avant et après ; 14:47 xtask ; 14:48 série depuis une base neuve ; 14:49
forme ; 14:45:50 à 15:06:04 campagnes ; 15:00 DET-1 ; 15:03 pile du `.pth` ; 15:05 `site` et `sitecustomize` ;
15:06:53 à 15:07:49 suite s2-harness.

**Recomptes [calc]** : lignes par `git apply --numstat` (1 812 − 95 = 1 717 = `wc -l` des 13 fichiers) ; sha256 par
`sha256sum` ; classements des campagnes par script ; octets par `outils/forme.py`.

### 13.9 Attestation (forme D.3), pour cette passe

- Aucune pièce de la liste D.2 ouverte ; aucun journal réel de S2 ni de S2-bis lu, listé, cherché ni copié ; les seuls
  `*.jsonl` sont les synthétiques des tests et de l'e2e, sous TMPDIR, retirés, jamais affichés.
- `lancer.sh` n'a tourné que dans des dépôts jetables de fixtures (suite, e2e, campagnes).
- `SHOGEN_S2_CAMPAGNE_CONTROL` : jamais posée par moi ; seulement par la suite du lot (LAN-6, exception A-3).
- Rien d'ouvert des dossiers exclus par le brief ; aucune recherche récursive sur `docs/`, le dépôt ou le scratchpad
  entier ; aucune écriture git sur le dépôt ; rien sur Pocket.
- Rien de hostile ni de test posé dans le HOME réel : venvs, `.pth` et marques sous `corr/tmp` (retirés) ; le site
  utilisateur n'a été vu que comme entrée de `sys.path` (nom de dossier), jamais ouvert.

### 13.10 Fichiers et clôture

- Remplacés : `diffs/P2R-6a.diff`, `diffs/P2R-6b.diff`, `snap/P2R-6a/`, `snap/P2R-6b/` ; les neuf autres diffs et
  instantanés inchangés.
- Neufs dans `journal/` : `drapeaux-S.json`, `rouge-S-LAN-14.txt`, `rouge-S-P2R-6a.txt`, `suite-finale-S.txt`,
  `suite-py310-S.txt`, `det1-S.txt`, `s2harness-S.txt`, `e2e-S-avant.json`, `e2e-S-apres.json`,
  `xtask-verdicts-S.txt`, `mutants-corr-S.json`, `mutants-final-S-{g2,corr,gen}.json` ; réécrits sur l'état final :
  `liste-finale-{g2,corr,gen}.json`, `forme.json`. Les autres journaux du §5 décrivent l'état d'avant `-S`.
- Outils : neufs `ajout_S.py`, `drapeaux_S.py` ; modifiés `listes.py` (motifs réécrits sur la forme à `-S`, mutants
  M-P2R6-18 à 20), `e2e.py` (scénario S24, sha256 des sorties de S0) et `diffs.sh` (source `snap/`).
- Clôture à 15:09 UTC : copies lourdes retirées (copie de e6657dc, extraction de `f35a70c`, cible cargo, arbres de
  travail, `etats3/`, dépôt git jetable) ; `tmp/` vidé puis retiré ; 0 `*.jsonl` et 0 `__pycache__` dans `corr/` ;
  dépôt intact (HEAD e6657dc, `git status` vide, relevé à 15:09:12) ; `SHA256SUMS` du dossier recalculé après ce
  paragraphe : il couvre ce rapport et tout le dossier sauf lui-même et `RAPPORT-CORRECTIONS-transcrit.md`, pièce de
  l'orchestrateur (14:15:22 UTC), que je n'ai pas modifiée (sha256 relevé `62a8a4ef…42ff`) ; son sha256 est donné dans
  le message de rendu.
