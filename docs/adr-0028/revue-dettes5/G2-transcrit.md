# Relecture G2 neuve de DETTES-T5 (transcrit)

> Transcription par l'orchestrateur le 2026-10-10 02:32:22 UTC du fichier g2/RAPPORT-G2.md ; contrôle FM-1.1 des transcripts du générateur-correcteur, du réviseur G2 et du contre-contrôleur, par le fm11.py versé et par celui de DT3-E : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte ci-dessous sans retouche, sauf : le chemin du scratchpad est abrégé en `<scratchpad>` ; Retouche déclarée (précédent : versement du G0 de CALIB-ACTIFS) : 2 message(s) d'outil cité(s) entre guillemets sont mis en code, sans autre changement (S-G5 lit les guillemets comme une citation bibliographique).

# Relecture G2 neuve du lot DETTES-T5 (volets code de la forge) : rapport

- **Modèle** : `claude-opus-5-5` (Gate 0 : identifiant exact donné par l'environnement ; préfixe conforme). Réviseur
  neuf : je n'ai rien écrit de ce lot. Effort demandé : high.
- Heures lues par `date -u` : début 2026-10-09 21:45:31 UTC ; rapport écrit à partir de 22:32 UTC (fin : « Clôture »).
- Brief : `BRIEF-G2.md`, sha256 `564d7d332f2ac94c886502411cebfb0dfcca62b1ea1ad2ffb344743768b21646`.
- Objet relu à 100 % : DT5-0 commis (`c1122de73ec0e07812fef30d41ddb4269a76a1c8`) ; DT5-1 à DT5-8 non commis
  (`../diffs/`), appliqués dans l'ordre sur `c1122de`. Empreinte de la série (sha256 de la concaténation DT5-1 … DT5-8),
  recalculée : **`0e31704d809627823e490f4332f3140a5513b147f9391f544378b49160cb5afe`**, égale à celle du brief ; les
  huit sha256 individuels égalent le `SHA256SUMS` du lot.
- Base : dépôt réel `/home/user/shogen` à `c1122de` au début (`status` vide). Pendant la relecture, sa tête est passée à
  `094fa5d3d5debe9dd466e37feee95200ca460dcf` (fusion de la PR n° 10, 22:13:20 UTC, parents `6356a94` et `c1122de`) :
  même arbre que `c1122de` (`f8c869cd…`, `git diff c1122de 094fa5d` vide) ; la série et les propositions s'y
  appliquent à l'identique.
- Copies : clones creux `git clone --no-hardlinks --no-checkout`, sparse non-cone sans `docs/15-*`, `docs/16-*`,
  `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`,
  `docs/adr-0028/execution/` ni `*.jsonl` (1131 fichiers suivis, 58 sautés, 0 `*.jsonl` extrait) : `copie/` (série),
  `tete/` (c1122de seule), `corr/` et `prop/` (série + corrections proposées).

## Verdict : **ACCEPTE-AVEC-CORRECTIONS** (liste fermée C-1 à C-8)

Le lot tient sur l'essentiel : chaque gate est verte sur la série, les rouges annoncés se rejouent, les comptes
(418, 33, 57) sont exacts, aucune gate n'est desserrée, aucune régression (VERDICT de `cargo xtask verify` identiques à
la tête). Huit constats corrigeables restent ; leur forme exacte est livrée en quatre diffs, à appliquer **dans cet
ordre après DT5-8** (vérifié sur une copie de la série : l'arbre obtenu égale `corr/`, où toutes les gates ont tourné) :

| diff proposé | corrections | lignes | sha256 |
|---|---|---|---|
| `propose/DT5-2-propose.diff` | C-6 | +7 −5 | `4b452944c8958e593d59527334ca34ef653ca5afdb6863b6356737ee3c969177` |
| `propose/DT5-5-propose.diff` | C-5 (en-tête, sim-bis) | +12 −10 | `1013068585c361f1126558b3569a99cb5ef702b594e588e26d7c9e3b4e9a5d7a` |
| `propose/DT5-7-propose.diff` | C-1, C-7 | +86 −26 | `172327f0f61e18500b1bdd8ca151cf5a26fdf97f39c62271d42b066e65c87461` |
| `propose/DT5-8-propose.diff` | C-2, C-3, C-4, C-5 (job g1), C-8 | +81 −14 | `f905744dd3de151c50b61446226018330d145bb625be8e3a28d42b4cb4da81c4` |

Concaténation des quatre, dans cet ordre : `440d4ec1d244765ce2c2e0c6dd94704ba134d8446b35fbcc58ff9bc878ea687b`.
Octets (consigne SHOGEN-HARNAIS-ECHAPPEMENTS-1) : 5 lignes ajoutées de DT5-7-propose portent des barres obliques
inverses (expressions brutes et guillemets échappés), contrôlées sur les octets écrits (`repr`) et par les tests et
mutants qui ont tourné sur ces octets ; les 3 autres diffs n'en ajoutent aucune ; aucun CR, aucun blanc final. Les
diffs s'appliquent tels quels (`git apply`), jamais retapés.
**R-25** : fondre DT5-7-propose dans DT5-7 (+166) ou DT5-8-propose dans DT5-8 (+193) passerait 200 lignes ajoutées ;
les quatre se versent comme diffs à part (chacun ≤ 200).

## Corrections (liste fermée)

### C-1 (DT5-7) : `runners-epingles.py` laisse passer des formes YAML valides qui portent un `-latest`

- **Constat** (outil `outils/sondes_runners.py`, sortie `sorties/sondes-runners-copie.txt`) : 14 workflows synthétiques
  valides où PyYAML lit un libellé `-latest` dans `runs-on` ou dans la matrice ; le contrôle de DT5-7 sort en **0 sur
  11** :
  - S-01, S-02 : suite de bloc écrite au retrait de la clé (`os:` puis `- windows-latest` au même retrait ; même forme
    sous `runs-on:`), style YAML courant ;
  - S-03, S-04 : scalaire de bloc (`runs-on: >-`, `os: |-`) ;
  - S-05, S-06 : clé JSON collée à sa valeur (`matrix: {"os":["ubuntu-24.04","windows-latest"]}`), alors que la
    docstring revendique le « mapping de flux », « entre guillemets », et « jamais un refus en moins sur ces formes » ;
  - S-07, S-08 : ancre ou étiquette seule sur la ligne de la clé (`runs-on: &r`, `runs-on: !!str`) ;
  - S-10 : casse (`Ubuntu-Latest` ; libellés insensibles à la casse sur la forge [inféré]) ;
  - S-11 : clé de matrice autre que `os` nommée par `runs-on: ${{ matrix.image }}` ; la limite écrite (« expression
    `${{ }}` autre que la matrice ») laisse croire la matrice couverte ;
  - S-12, S-13 : échappement dans un scalaire entre guillemets doubles, clé explicite `? runs-on` (voir C-8).
  
  De plus, six de mes mutants survivent aux 7 tests (`sorties/mutants-g2.json`) : MR-1 (dièse sans blanc devant lu
  comme commentaire), MR-2 (guillemets non suivis), MR-3 (doublons gardés), MR-4 (deux arguments admis), MR-6 (un seul
  jeton par ligne), MR-8 (accolade ouvrante non comptée).
- **Forme exacte** : `propose/DT5-7-propose.diff`.
  - Code (sha256 proposé `957e55835d18e6e11084294581c75a14297bc11bc90dd32529e2a0ed9b500ed1`) : clé lue sans exiger
    d'espace après « : » ; casse ignorée (libellé et clé) ; clés de matrice nommées par une valeur `runs-on`
    (`matrix.<clé>`, ligne et bloc) ; lignes suivantes lues après une clé sans valeur, une ancre ou une étiquette
    seule, un en-tête de scalaire de bloc ou un flux ouvert ; suite `-` au retrait de la clé après une clé sans
    valeur.
  - Docstring : formes lues et limites écrites (ancres et alias, `<<`, échappements, clé explicite, flux moins indenté
    que sa clé, expression autre que `matrix.<clé>`).
  - Tests : `test_formes_hors_ligne`, `test_casse_cle_de_matrice_et_jetons`, et le cas `(valide, valide)` dans
    `test_erreurs_sortie_3`. Plancher de `controle-unittest` 33 → **35** et commentaire du job.
- **Vérifié** : tests proposés **rouges** sur le contrôle de DT5-7 (2 FAIL, 0 ERROR), **verts** sur la forme proposée
  (9 OK) ; sondes S-01 à S-11 refusées, S-12 et S-13 admises (C-8 les ferme) ; arbre du dépôt « conforme (7
  workflow(s), 22 clé(s)) », tête `c1122de` refusée (3 `windows-latest`) ; **24 mutants sur 24 tués**
  (`sorties/mutants-propose-re.json` : MR-1 à MR-8, N-1 à N-8, R-1 à R-3 et R-5 à R-9 du générateur adaptés).

### C-2 (DT5-8) : l'étape `apt-get` du job g1 peut poursuivre avec une autre version de `python3-yaml`

- **Constat** (souches `dpkg-query`, `sudo`, `apt-get` en tête de `PATH`, étape extraite de `gates.yml`, `bash
  --noprofile --norc -eo pipefail` ; `sorties/sonde-etape-apt.txt`) : version exacte installée par `=6.0.1-2build2` et
  refus quand le paquet manque, **sauf** quand `apt-get update` échoue alors qu'une autre version est présente :
  h (6.0.2-1, retour arrière refusé) et i (6.0.1-2) sortent en **0**, et la suite lit alors cette autre version. Dans
  `A || { update && install; }`, l'échec de `update` (élément non final d'une liste `&&`) n'arrête pas `bash -e`, et
  rien ne relit la version. Le cas « absent, update en échec » ne sort en 1 que par la ligne `dpkg-query -W` qui
  suit. Le module importé n'est pas rattaché au paquet : un PyYAML installé par `pip` sous
  `/usr/local/lib/python3.12/dist-packages` ou dans le site de l'utilisateur passerait devant (motif réel : sur l'hôte
  cloud, `/usr/local/lib/python3.11/dist-packages` porte des paquets `pip`). Le commentaire de l'étape et la ligne R-8
  disent « s'il manque à l'image » ; la condition est « version différente ».
- **Forme exacte** (`propose/DT5-8-propose.diff`), après `dpkg-query -W python3-yaml` :
  `[ "$(dpkg-query -W -f='${Version}' python3-yaml)" = "$V" ] || { echo "python3-yaml $V exigé" >&2; exit 1; }`,
  `M="$(/usr/bin/python3 -B -P -c 'import yaml; print(yaml.__file__)')"`, puis un `case` sur `dpkg -S "$M"` qui exige
  `python3-yaml: $M` (« PyYAML lu : $M » au journal, refus sinon) ; commentaire de l'étape et phrase de
  `docs/R-8-outillage.md` récrits.
- **Vérifié** (`sorties/sonde-etape-apt-corrigee.txt`) : a, b, c, g → 0 ; d → 100 ; e, h, i → 1 ; f → 100 ; j (module
  hors paquet) → 1. Sur l'hôte, l'étape corrigée imprime « PyYAML lu : /usr/lib/python3/dist-packages/yaml/__init__.py »
  et sort en 0.

### C-3 (DT5-8) : tests du chargeur sûr et du contrat « une erreur n'est jamais un refus »

- **Constat** : mes mutants MY-1 (`SafeLoader` → `UnsafeLoader` : une étiquette `!!python/object/apply` serait
  exécutée) et MY-2 (seule `ImportError` rendue en 3 : une clé non hachable sort en 1 par trace, comme un refus)
  survivent aux 11 cas.
- **Forme exacte** : W-12 (étiquette python refusée, sans effet : marqueur absent) et W-13 (clé non hachable : 3) dans
  le runner (`propose/DT5-8-propose.diff` ; `CAS` 11 → 14 avec W-14 de C-8).
- **Vérifié** : W-12 et W-13 verts sur DT5-8 et sur la forme proposée ; MY-1 et MY-2 tués.

### C-4 (DT5-8, adjudication Q-4) : limites à écrire

- **Jugement de Q-4 : juste.** Le crochet versionné ne porte que des étapes bash (R-13, lint R-1, gate des secrets) ;
  aucune étape Python du job g1 (`journaux-modele.py`, `docs-sha256sums.py`) n'y est ; y exiger PyYAML créerait une
  dépendance sur le poste local (R-8 de cette machine) et changerait `ATTENDU` (réinstallation). La chaîne de
  l'orchestrateur rejoue la lecture avant commit (`chaine_d5_0.sh` l.25 et l.29 : `yaml.safe_load` de `gates.yml`).
- **Limites absentes** : (a) le crochet ne lance pas ce contrôle ; avant commit, seule une procédure le rejoue ; (b)
  sur la forge, ce contrôle ne voit pas l'illisibilité de `gates.yml` lui-même : le workflow qui le porte ne démarre
  pas (PR n° 10 : « échoué sans job ») ; elle ne bloque la fusion que si les contrôles requis de `main` nomment des
  jobs de `gates.yml` [inféré].
- **Forme exacte** : docstring de `enforcement/workflows-yaml.py` (L-5 gardée, ces deux limites ajoutées) et
  commentaire de l'étape (`propose/DT5-8-propose.diff`).

### C-5 (DT5-5 ; commentaire du job g1 de DT5-4, DT5-7, DT5-8) : commentaires de `gates.yml` périmés

- **Constat** : l'en-tête dit « La forge exécute de nouveau les jobs depuis le 2026-10-09 » et le commentaire du job
  sim-bis « la forge exécute aussi le job depuis le 2026-10-09 » ; l'adjudication de 21:28:17 UTC constate sur la PR
  n° 10 des workflows « sans machine (dépôt privé : acte de l'investisseur) » [2nd]. « Requis à la fusion : » se lit
  comme une affirmation. Le commentaire du job g1 dit « Étape 1 (après l'environnement…) » alors que DT5-7 et DT5-8
  placent deux étapes entre l'environnement et les cas du lint.
- **Forme exacte** : `propose/DT5-5-propose.diff` (en-tête et sim-bis au passé daté : exécution du 2026-10-09, dépôt
  alors public ; dépôt privé ensuite, constat de la PR n° 10 ; « Contrôles requis à la fusion : … n'en avait pas ») et
  `propose/DT5-8-propose.diff` (job g1).

### C-6 (DT5-2) : la docstring de la garde dit « un envoi … lève ReseauInterdit », faux pour `sendmsg`

- **Constat** (copie, réseau coupé) : `u.sendmsg([b"x"], [], 0, ("192.0.2.1", 53))` sous la garde lève une
  `OSError` du noyau, pas `ReseauInterdit`, et `TENTATIVES` reste vide : un envoi par `sendmsg` vers une adresse n'est
  pas gardé. Le code est celui de `s2bis/tests/__init__.py`, octet pour octet (forme adjugée, E-1) : aucun code de
  la suite n'emploie `sendmsg` ; la correction est documentaire.
- **Forme exacte** : `propose/DT5-2-propose.diff` (appels gardés nommés ; limite `sendmsg` ; commentaire du job
  s2-harness).

### C-7 (DT5-7) : README de `scripts/controle`

- **Constat** : chaque fichier de tests du dossier y a son ajout daté (DT3-A, DT4-c) ; `tests/test_runners_epingles.py`
  n'y est pas.
- **Forme exacte** : paragraphe daté (`date -u` 22:24:59 UTC) dans `propose/DT5-7-propose.diff`.

### C-8 (Q-2 : formes que le lecteur par lignes ne peut pas voir)

- **Constat** : après C-1 restent S-12 (échappement hexadécimal entre guillemets doubles), S-13 (clé explicite) et
  l'alias d'une ancre posée hors d'une clé `runs-on` ou `os` (`env: {R: &r ubuntu-latest}` puis `runs-on: *r`, forme
  de factorisation plausible [inféré : lecture des ancres par la forge]). Le job g1 charge déjà chaque workflow avec
  PyYAML (DT5-8) : la valeur lue y est disponible.
- **Forme exacte** (`propose/DT5-8-propose.diff`) : `workflows-yaml.py` refuse aussi tout libellé `-latest` (casse
  ignorée) dans les valeurs lues de `runs-on` et de `strategy.matrix` de chaque job ; cas W-14 (alias, échappement,
  clé explicite, matrice en capitales).
- **Vérifié** : runner proposé sur le contrôle de DT5-8 : W-14 en ÉCHEC, 13 ok, sortie 1 ; sur la forme proposée
  (sha256 `05c8d3a2e9b13c5e4ca57e0e9ed37f41c13e50424528d49df0fa1d4286554e40`) : 14 ok ; W-01 (arbre) conforme ;
  **20 mutants sur 20 tués** (`sorties/mutants-propose-wy.json` : MY-1 à MY-6, Y-1 à Y-8 du générateur, Z-1 à Z-6).

## Constats (O-n), sans correction

- **O-1 (DT5-0)** : juste. `gates.yml` de `b837efe` : `mapping values are not allowed here`, l.112 col. 94 ; celui de
  `c1122de` se lit. Le nom d'étape changé n'est lu par rien : greps fichier par fichier (un niveau) de `.claude/agents`,
  `.github/workflows`, `enforcement{,/hooks,/tests}`, `xtask/{src,tests}`, `s2-harness/{tools,tests}`, `s2bis/tests`,
  `scripts/{controle,controle/tests,calib-actifs/tests,sim-bis,sim-bis/tests,sceau,post-s2/tests,plan-s2bis/tests,`
  `plan-s2bis-2/tests,publication/en/tests}` : seul `gates.yml` porte ce nom ; les lecteurs de `gates.yml`
  (`etapes()`, cas K, `run-fixtures-hooks.sh`, `oracle_record.py`) ne lisent que les jobs unittest et g5.
- **O-2 (DT5-6)** : `windows-2025` remplace chaque `windows-latest` (3 matrices et le commentaire de `temoignage.yml`) ;
  aucun `-latest` hors commentaire dans les 7 workflows ; 22 clés lues (2+4+8+3+1+2+2) ; le contrôle refuse la tête.
- **O-3 (L-5)** : écrite dans la docstring de `workflows-yaml.py` (« un fichier admis ici peut encore être refusé par
  elle ») ; C-4 la complète.
- **O-4 (étape apt)** : épinglage exact (`python3-yaml=6.0.1-2build2`) ; aucune autre version de `python3-yaml` ne
  peut être installée par cette commande ; refus si absent (d, e). Dépendances non épinglées (`libyaml-0-2`) : sans
  effet sur le contrôle (`SafeLoader` pur Python). Seul défaut : C-2.
- **O-5 (DT5-2)** : garde identique à celle de s2bis (1002 octets dès `TENTATIVES = []`) ; suite entière sous la garde :
  `Ran 418`, `TENTATIVES` = 8, exactement les 8 appels du test neuf ; rouge rejoué (2 FAIL, 0 ERROR). La même phrase
  « un envoi » est dans `s2bis/tests/__init__.py`, hors des diffs relus : la phrase de C-6 y est à reporter par
  l'orchestrateur (même lot s'il l'admet, sinon au prochain lot qui touche s2bis).
- **O-6 (DT5-3)** : prémisse mesurée : git 2.43.0 ignore un `pre-commit` en 644 (`hint: The '.git/hooks/pre-commit'
  hook was ignored because it's not set as executable.`, commit en 0) et le lance en 755 (commit en 1) ; l'annexe B
  l.285 la disait inférée. Rouge rejoué (runner neuf, installeur de la tête) : I-15, I-16, I-17 en ÉCHEC, 54 ok.
- **O-7 (DT5-4, E-3)** : justifié : le gabarit K-01 exige trois étapes exactes dans `s2-harness-unittest`.
- **O-8 (R-8)** : champs conformes à `apt-cache show python3-yaml` (version, priorité, source, mainteneurs, fichier,
  SHA256 `315e5950…ec23`, amont) et au fichier `copyright` (MIT) ; listes apt locales du 2026-07-23 : seule
  6.0.1-2build2 pour noble, `noble-updates` comprise.
- **O-9** : SHOGEN-G1-FORGE-1 n'a aucune ligne dans l'annexe B (`docs/adr-0028/G0-lot-D8a.md` l.431 seul) : acte n° 7.
- **O-10** : le rapport du générateur cite l'annexe B à `377283b3…` ; elle est à `709e146c…` (B.91 ajouté) ; les numéros
  de ligne cités restent vrais.
- **O-11 [abs]** : aucun des deux contrôles ne lit un workflow caché (`.x.yml`) ni une extension en capitales ; la
  lecture de la forge n'est pas établie (acte de lecture, à joindre à l'acte extérieur n° 3) ; si elle les lit, la
  forme est une liste `os.listdir` filtrée par extension, sans casse.
- **O-12 (hors lot, PAROXYSME)** : `cargo test -p xtask` laisse 85 dossiers `shogen-*` à noms fixes dans `TMPDIR`
  (mesuré : mtime 21:55:10, pendant mon run) : deux runs simultanés peuvent se heurter. Item à former (lot xtask).
- **O-13** : la tête du dépôt réel a bougé pendant la relecture (`094fa5d`, même arbre que `c1122de`).

## Enregistrement de rôle G2 (consigne DT3-C)

- Commande (22:07:15 UTC), depuis ma copie `copie/` (`c1122de` + DT5-1..8 ; vérificateur de l'outil
  `enforcement/verdict-suite-s2.py` sha256 `bd5955e3c85526acffeb407a4d20c6c2630811afb7c16ad188beefd5639e0420`, relu ici :
  DT5-2 n'y change que `PLANCHER`), sous `isole.sh` :
  `env -u SHOGEN_S2_CAMPAGNE_CONTROL PYTHONDONTWRITEBYTECODE=1 python3 -B s2-harness/tools/oracle_record.py --role G2
  --commit c1122de73ec0e07812fef30d41ddb4269a76a1c8 --auteur claude-opus-5-5 --depot <g2>/copie --sortie <g2>` → exit 0.
- Enregistrement : `shogen-c1122de-G2-20261009T220715Z-28656.json`, sha256
  **`4595fc5e31f392fb9844834491597de6bbd3b58af5f23a8ee3591793def73d76`** ; sortie du run
  `shogen-c1122de-G2-20261009T220715Z-28656.0-suite.out`, sha256
  `d9cd58422e474f754e9168ced05aa1a7d9d4e1c82f68c3072807592aada54921` (`Ran 415`, `OK (skipped=2)`, exit 0) ;
  `tree.commit` `c1122de…`, 1131 fichiers ; `verdict-suite-s2.py` du commit `de48c6bf…` ; variable scellée absente.
- Lecture `--verifier … --depot <g2>/copie` (22:09:50 UTC) : « conforme », exit 0.
- Il atteste la base `c1122de` et la suite lancée sur elle, non les diffs ; ce rapport le relie à l'empreinte des
  diffs relus : `0e31704d809627823e490f4332f3140a5513b147f9391f544378b49160cb5afe`.

## Mutants (estimateur propre)

| campagne | cible | mutants | tués | vivants | FATAL |
|---|---|---|---|---|---|
| `mutants_g2.py` (série) | runners-epingles (MR-1 à MR-8), workflows-yaml (MY-1 à MY-6) | 14 | 6 | 8 (MR-1, 2, 3, 4, 6, 8 ; MY-1, 2) | 0 |
| `mutants_propose.py re` | runners-epingles proposé, tests proposés | 24 | 24 | 0 | 0 |
| `mutants_propose.py wy` | workflows-yaml proposé, runner proposé | 20 | 20 | 0 | 0 |

Classement SHOGEN-MUT-FATAL-1 : unittest tué = sortie 1 et `FAILED (failures=…)` sans `errors` ; runner tué = sortie
1 ; autre sortie = FATAL. Fichiers restaurés, sha256 contrôlés après chaque campagne.

## Gates rejouées (réseau coupé, mandataires retirés, variable scellée jamais posée)

Outil propre `outils/jobs_g2.py` : chaque étape `run:` de `gates.yml` de l'arbre, `bash --noprofile --norc -eo
pipefail` ; g5 (balayage) et g3 `--tree` sur un dépôt jetable des fichiers présents ; g3 `--history` non lancé.

| gate | `c1122de` | série | série + propositions |
|---|---|---|---|
| g5 : cas du hook / balayage R-13 | 54 ok / vert | 57 ok / vert | 57 ok / vert |
| g1 : environnement / runners-epingles / workflows-yaml | — / — / — | 0 / conforme (7, 22) / 11 ok, conforme | 0 / conforme (7, 22) / 14 ok, conforme |
| g1 : lint (cas) / R-1 / journaux-modele / docs-sha256sums | 227 / OK / conforme / 34, 295 | idem | idem |
| g3 : cas / `--tree` | 147 / 0 | 147 / 0 | 147 / 0 |
| runner du vérificateur (5 jobs) | 137 ok ×5 | 137 ok ×5 | 137 ok ×5 |
| s2-harness `--egal` / s2bis / sim-bis / calib-actifs | 415 / 341 / 279 / 65 | 418 / 341 / 279 / 65 | 418 / 341 / 279 / 65 |
| controle `--egal` | 26 | 33 | 35 |
| `cargo test -p xtask` (`test result`) | 81 et 9 passés | identiques | non relancé (aucun Rust touché) |
| `cargo --locked xtask verify` (VERDICT) | 8 VERT, 1 ROUGE | identiques | identiques |

Le ROUGE de `cargo xtask verify` est celui de la tête, inchangé par la série et par les propositions.

## Écarts

- **E-1** : l'enregistrement de rôle extrait le commit entier (`git archive`) : les 58 fichiers absents de ma copie
  creuse (dossiers interdits, `*.jsonl`) ont été écrits dans mon `TMPDIR` et hachés par l'outil, jamais affichés,
  puis retirés par lui (0 dossier `oracle_*` restant) ; même constat que l'O-10 de la G2 de DETTES-T4.
- **E-2** : deux entrées de mes NOTES ont d'abord porté une heure écrite avant lecture de l'horloge ; corrigées en
  place, avec mention.
- **E-3** : PyYAML de l'hôte (6.0.1, paquet `python3-yaml`) a servi d'outil de mesure (extraction des étapes, sondes),
  comme l'E-12 du générateur.
- **E-4** : écritures git dans mes seuls clones jetables (`checkout -b`, `apply`, `add -A`), jamais de commit ; dépôt
  réel lu seulement (`--no-optional-locks`), `status` vide à la fin.
- **E-5** : `gate-secrets.sh --history` non lancé (il lirait l'historique des pièces interdites).
- **E-6** : la liste des fichiers sommés a transité par un fichier temporaire hors de mon dossier
  (`dettes5/g2-liste.txt`), retiré dans la même commande.

## Journal de provenance (G1)

- [lu] `BRIEF-G2.md` ; `../ADJUDICATION.md` (Q-1 à Q-4, C-1, C-2) ; `../RAPPORT-GENERATEUR.md` en entier ; `../NOTES.md`
  du générateur ; les 8 diffs et `c1122de` en entier ; `.claude/agents/shogen-worker.md` l.75-87 ;
  `docs/adr-0028/ANNEXE-B-items.md` (sha256 `709e146c…55fa`) l.78, 80, 242, 269, 285, 820-826, 1173, 1250, 1390-1396 ;
  `docs/adr-0028/G0-lot-D8a.md` (`a5d70848…81e7`) l.427-435 ; `docs/adr-0028/ANNEXE-D-preenregistrement.md` l.32-48
  (liste D.2) ; `docs/adr-0028/revue-dettes4/G2-transcrit.md` l.100-110 et `revue-dettes3/ADJUDICATION.md` l.17-22 ;
  dans la copie : `gates.yml`, `squelette.yml` l.1-30, `enforcement/hooks/pre-commit`, `install-pre-commit.sh`,
  `run-fixtures-hooks.sh` l.1-135, `run-fixtures-verdict-suite-s2.py` l.540-640, `oracle_record.py` l.1-75, 205-240,
  300-340, 405-443, `s2-harness/tools/README.md`, `s2bis/tests/__init__.py` et `test_garde.py`, `scripts/controle/README.md`
  et `SHA256SUMS`, `docs/adr-0028/CP2-S2.md` l.25-45 ; `../../../haiku/FAITS-FORGE.md` (`90a40fc1…d786`) ;
  `../../../chaine_d5_0.sh` (greps l.8-29).
- [2nd] faits de forge (check runs des PR #7 à #9, journaux de jobs, PR n° 10, dépôt privé) : FAITS-FORGE et
  adjudication de l'orchestrateur ; libellés Windows (`windows-2025`) : adjudication.
- [abs] lecture par la forge des workflows cachés ou d'extension en capitales (O-11) ; casse des libellés sur la forge
  et lecture des ancres (marquées [inféré]).
- Commandes (sorties sous `sorties/`) : `cat … | sha256sum` (empreinte) ; `git apply --check`/`--numstat` ;
  `outils/cargo.sh` (cargo verify et test, VERDICT et `test result` seuls) ; `outils/jobs_g2.py` ×3 (copie, tête,
  corr) ; sondes `outils/sondes_runners.py`, `sondes/apt/` ; `outils/mutants_g2.py`, `outils/mutants_propose.py` ;
  `oracle_record.py` (écriture et lecture) ; `apt-cache show`/`policy python3-yaml` ; mesure git du hook en 644.
- Chiffres recomptés : comptes de tests et de cas par les sorties des runs ; mutants par les JSON ; lignes des diffs
  par `git apply --numstat` ; 22 clés par le contrôle ; 1131 et 58 fichiers par `git ls-files -t`.

## Clôture

Fin à 2026-10-09 22:35:33 UTC (`date -u`). Dépôt réel à `094fa5d` (arbre de `c1122de`), `status` vide, jamais
écrit. 0 processus restant. Clones, copies, dépôts jetables, arbres de sondes et `tmp/` supprimés (régénérables : clone
creux à `c1122de`, puis les diffs) ; gardés : `NOTES.md`, ce rapport, l'enregistrement G2 et sa sortie, `outils/`,
`propose/`, `sondes/apt/`, `sorties/`, sommés dans `SHA256SUMS` (chemins relatifs, sans `./`). Aucun commit, aucune
poussée ; `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée ; aucun accès réseau (tout sous `isole.sh`) ; aucune pièce de D.2
ouverte (E-1).
