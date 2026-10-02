# Journal G1 — partie 2 de S2, étape C, sous-lots C1 et C2

**Nature de ce journal** : journal de provenance du worker de la session cloud, travail du 2026-10-02 de 07:21 à 08:3x
UTC (horloge lue par `date -u` : 07:21:51 au départ, 08:27:42 avant la rédaction ; clôture au §9). Contrat :
`docs/adr-0028/G0-partie-2.md`, section « C — RENDU-1 » (l.106-145, sha256 du fichier `13417c8e…`), lue en entier avec
ses ajouts datés de l'étape B (l.147-168). Branche `partie-2-rendu`, base `01b8cb5` (HEAD inchangé pendant le travail).
Aucune opération git en écriture sur le dépôt ; seuls les dépôts jetables des tests et des sondes, sous des répertoires
temporaires ou le scratchpad, sont écrits. Livrables : `s2-harness/tools/rendu_unique.py` et
`s2-harness/tests/test_rendu_unique.py` (neufs, non suivis), coupés en cinq sous-lots C1a, C1b, C1c, C2a, C2b ; diffs
dans `…/scratchpad/lot-C1/` ; ce journal.

## 0. Gate 0

Modèle résolu sous lequel le worker a tourné : **`claude-opus-5-5`** (identifiant exact fourni par l'environnement de la
session ; préfixe attendu `claude-opus-5-5` : conforme). Effort : `max` (fiche du worker et brief).

## 1. Provenance commune

### 1.1 Sources lues (toutes [lu] ; aucune [abs] ni [2nd])

- `CLAUDE.md` (racine, rappelé par la session) ; `docs/PASSATION-CLOUD.md` l.1-273, en entier.
- `docs/adr-0028/G0-partie-2.md` l.1-168, en entier ; `docs/adr-0028/PLAN-PARTIE-2.md` : titres et §5 (l.55-70).
- `docs/adr-0028/ANNEXE-D-preenregistrement.md` (`5fc0cbc1…`) : l.30-42 (D.2, liste fermée, lue pour s'en garder),
  l.107-151 (D.4 a, b et c), et les lignes d'un `grep -n` sur `^#\|D\.4\|D\.2` (l.1, 3, 7, 24, 26, 28, 30, 44, 54,
  107, 126, 140, 143, 144, 152).
- `docs/adr-0028/ANNEXE-A-lots.md` l.37 (RENDU-1) ; `docs/adr-0028/ANNEXE-B-items.md` l.57 (SHOGEN-RENDU-UNIQUE-1),
  l.163 (EX-E1-1), l.270 (SHOGEN-HOOK-SUITE-S2-1).
- `scripts/sceau/verify.sh` (`cf55f897…`, 18 lignes) et `scripts/sceau/make-tsq.sh` (`f8b04b5a…`, 20 lignes), en entier.
- `docs/17-modele-de-menace.md` (`d95657c8…`) : lignes d'un `grep -n` sur `T-13\|T-16\|T-17` (l.82, 94, 97, 99, 104,
  107, 108).
- Méthode et format : `docs/G1-partie-2-etape-B-3.md` l.1-352, en entier ; `docs/G1-partie-2-etape-B-2.md`, les seules
  lignes d'un `grep -n` sur la coupe et les numstat de B4 (vingt-six lignes entre l.8 et l.322).
- Code : `s2-harness/tools/oracle_record.py` l.1-249 et `s2-harness/tests/test_oracle_record.py` l.1-314, en entier
  (conventions : `git` sans `GIT_*`, dépôts jetables, `importlib`) ; `s2-harness/tests/__init__.py` en entier ;
  `s2-harness/tests/test_exclusion.py`, lignes d'un `grep -n` (imports, `HARNESS` l.44).
- Dépôt : `.gitignore` l.1-40 ; `.gitattributes` l.1-20 ; `enforcement/hooks/pre-commit` l.15-30 (motif R-13, l.21) ;
  `enforcement/gate-secrets.sh`, lignes de deux `grep -n` (motifs VENDOR et GENERIC l.57-58, mode `--tree` l.110-111) ;
  `enforcement/lint-model-pinning.sh` l.28 (usage) ; `xtask/src/sg4.rs` l.36-100
  et l.130-160 (locutions de S-G4, citations exclues) ; `xtask/src/sg5.rs`, lignes d'un `grep -n` (extraction des
  « … » d'allure anglaise).
- Format du fichier de sommes réel : un `grep -rn SHA256SUMS` sur le dépôt, fichiers exclus `JOURNAL.md`,
  `docs/rapports/cartographie-2026-09-29.md`, `docs/adr-0025/**`, `biblio/**`, `scratch/**` ; seule ligne retenue :
  `docs/G1-lot-adr0025-filtre.md` l.11 (`sha256sum -c SHA256SUMS-cloture-2026-09-28.txt` dans `campagne\`, cinq
  fichiers conformes) : format de `sha256sum`, cinq entrées, noms relatifs au dossier des journaux. Le même `grep` a
  affiché, sans autre lecture, des lignes de G1 et G0 antérieurs, d'ADR-0028 (l.9, 68, 241) et trois lignes de
  `docs/pocket-report/` (`G0-claims-register.md` l.13, `POCKET-DISCLOSURE-REPORT.md` l.405 et l.508), non touchées.
- Scratchpad : `regle_fixtures.py` (`5557fb56…`, imposé par le brief, utilisé tel quel) ; `lot-B3/outils/mutants.py`
  (`2f0dcc09…`) et `faire_diff.py` (`1d7e4b56…`), recopiés à l'identique dans `lot-C1/outils/` ;
  `lot-B3/outils/mutants_b6b.py` et `mutants_enf.py` (lus pour la forme des listes) ; mise en page de ce journal :
  `lot-B3/outils/rewrap_md_b3.py` (`d86a1ee6…`), recopié avec une garde des tableaux, et
  `lot-B2/outils/precheck_md.py` (`1b46b7cb…`), utilisé tel quel.
- Système : OpenSSL 3.0.13 (`openssl version -a`), git 2.43.0, Python 3.11.15, `sha256sum` de GNU coreutils 9.4.

### 1.2 Pré-enregistrement (annexe D)

- D.4 a : fixtures seulement (dépôts jetables, journaux synthétiques de trois lignes, autorité RFC 3161 de test produite
  par `openssl`) ; aucun journal de campagne, aucune copie scellée, aucun réseau ; FreeTSA jamais sollicitée.
- D.2 : aucune pièce ouverte. ADR-0025 n'a pas été ouverte ; la cartographie du 2026-09-29 n'a pas été ouverte (exclue
  de tout `grep`) ; `JOURNAL.md` n'a pas été ouvert (exclu de tout `grep` ; la copie du scratchpad non plus), l'outil ne
  l'a lu que dans des dépôts jetables.
- Exposition déclarée (D.3, FM-2.4) : la l.11 de `docs/G1-lot-adr0025-filtre.md` porte deux préfixes de sha256 de
  journaux scellés (`351f51b2…`, `98c5793e…`), admis par D.2 n° 7 (seuls les sha256) ; rien d'autre : aucun taux par
  source, aucun z, K, P̂ ni φ. Ces préfixes n'entrent dans aucun code ni test.
- `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée : `env | grep -c` rend 0 au départ et après chaque suite ; le moteur de
  mutants la retire de l'environnement de ses sous-processus.

### 1.3 Sondes (scratchpad `lot-C1/sondes/`, dépôts et dossiers jetables)

- git (`r/`) : `git show HEAD:<fichier>` rend le blob brut même sous un textconv configuré ; `git log -S` applique le
  textconv (aucun commit trouvé sous `tr a-z A-Z`) sauf avec `--no-textconv` ; le commit racine est compté ; `git diff
  --quiet` entre deux commits compare les objets.
- OpenSSL 3.0.13 (`tsa1/` à `tsa3/`) : `openssl ts -reply` exige la clé `digests` ; `req -x509` applique les extensions
  `v3_ca` de la configuration système (le certificat de TSA sortait `CA:TRUE`) : la fixture tourne sous une
  configuration minimale passée en `OPENSSL_CONF` ; CA de test et TSA (extension timeStamping critique), requête et
  réponse : 65 ms ; sortie `-text` : `Time stamp: Oct  2 07:46:13 2026 GMT`. La sonde `tsa2/`, sans `digests`, n'a
  produit aucune réponse : ses refus de vérification ne prouvent rien ; le refus d'une autre requête (nonce) et d'autres
  données est établi par les tests (§3.4) et par les mutants A4 et A5.
- `sha256sum -c` (`sommes/`) : accepte marque texte ou binaire, majuscules, CRLF, lignes vides ; une ligne mal formée ne
  donne qu'un avertissement, code 0.
- `datetime.fromisoformat` (3.11) : lit `Z`, `+00:00`, minutes seules, fraction ; refuse mois 13 et 30 février.
- Sceau (`sceau-scripts/`) : `make-tsq.sh` puis `verify.sh` dans un dépôt jetable : manifeste
  `<sha> *docs/adr-0028/PAQUET-PREREG-S2.md` (chemin relatif à la racine) ; l'étape (1) de `verify.sh`, lancée depuis le
  dossier de sceau, sort `MANIFESTE : ÉCART`, code 2 (limite L1, §7).
- Python (`pyc/`) : module importé une fois (bytecode écrit), source changée à taille et date égales, import sous `-B` :
  l'ancien bytecode s'exécute (`aaa` au lieu de `bbb`) : `-B` n'empêche que l'écriture (appui de E3).

### 1.4 Outils écrits (scratchpad `lot-C1/outils/`, sha256)

`mutants_c1a.py` `8bf93a90…` ; `mutants_c1b.py` `45511a82…` ; `mutants_c1c.py` `880345f2…` ; `mutants_c2a.py`
`78a0036c…` ; `mutants_c2b.py` `9c89f332…` ; `mutants_final.py` `6902a801…` (neutralisation canonique de chaque garde,
liste de C1b sans N1) ; `rewrap_md_c1.py` `49a8cac2…` (copie de `rewrap_md_b3.py` : tableaux laissés intacts,
ponctuation isolée collée au mot qui la précède). Moteur : `mutants.py` (copie de lot-B3) : copie de l'arbre, une
mutation textuelle dont l'ancien texte figure une fois exactement, `tests.test_rendu_unique` lancé, variable scellée
retirée.

### 1.5 État de départ (arbre `01b8cb5`, exporté par `git archive` dans `lot-C1/arbres/HEAD`, égal à l'arbre de travail)

- Suite : `Ran 343 tests in 35.232s`, `OK (skipped=2)` (`preuves/suite-depart.out` `4e809192…`).
- Règle scellée SHOGEN-CRITERE-R1-1 : `regle_fixtures.py` sur `HEAD`, sha256 du JSON `ea3a2d94…` (= référence).
- Préexistant, hors de mon fait : `s2-harness/tests/__pycache__/__init__.cpython-311.pyc` (04:36:57 UTC, ignoré par
  `.gitignore` l.33), laissé en place.

## 2. Construction (décisions du G0 §C appliquées)

- **Outil** `s2-harness/tools/rendu_unique.py`, bibliothèque standard seule ; `git` lancé par liste d'arguments, avec
  `--no-optional-locks` et sans variable `GIT_*` héritée ; `openssl` résolu par `shutil.which`, liste d'arguments ;
  jamais de shell. `verifier_gardes(depot, paquet, journaux, sommes, maintenant=None)` évalue toutes les gardes dans
  l'ordre `bloc`, (1) à (6), et rend la liste `[(nom, motif)]` des refus ; une exception pendant une garde est un refus
  (motif « non évaluée »). Ligne de commande : `--depot`, `--paquet`, `--journaux`, `--sommes`, `--sortie` (toutes
  exigées) ; refus : une ligne `rendu_unique : refus <nom> : <motif>` par garde sur stderr, code 2, rien d'écrit ;
  gardes levées : `gardes levées` sur stdout, code 0, rien d'écrit (sorties : C3). `--depot` est ramené à la racine du
  dépôt (`git rev-parse --show-toplevel`).
- **Bloc machine** (`lire_bloc`) : une seule ligne d'ouverture de bloc clôturé qui nomme `shogen-paquet-v1` (toute
  ouverture voisine, à tildes, indentée ou à plus de trois accents graves, compte), de forme exacte, fermée par la
  première ligne de trois accents graves ; une clé par ligne, champs séparés par une espace ; `commit_analyse` (40
  hexadécimaux), `sha256_script`, `sommes`, `cacert_sha256`, `tsa_crt_sha256` (64), une fois chacune ;
  `journal <nom> <sha256>` trois fois, noms distincts, nom en chemin relatif sans composante qui commence par un
  point ; minuscules. Clé absente, dupliquée (même de même valeur), inconnue ou malformée, ligne vide : refus `bloc`.
- **(1)** : sha256 des octets du paquet présent dans `git show HEAD:JOURNAL.md`, en entier (ni chiffre hexadécimal avant
  ni après : un préfixe ou une sous-chaîne ne suffit pas).
- **(2)** :
  `git diff --quiet --no-ext-diff --no-textconv <commit_analyse> HEAD -- s2-harness/shogen_s2 s2-harness/tools` sort 0
  (tout autre code, dont 128 pour un commit absent, refuse), et
  `git status --porcelain --untracked-files=all --ignored` sur ces chemins est vide.
- **(3) et EX-E1-1** : sha256 du fichier de sommes égal à `sommes` du bloc ; pour chaque `journal`, sha256 du fichier
  `<--journaux>/<nom>` égal au sha du bloc **et** à celui du fichier de sommes. Lecteur des sommes : grammaire de
  `sha256sum` (marque texte ou binaire, LF ou CRLF, hexadécimal des deux casses, lignes vides) ; ligne non conforme ou
  nom répété : refus.
- **(4)** : sha256 du fichier de l'outil qui s'exécute égal à `sha256_script`.
- **(6) voie (a)** : dans `docs/adr-0028/sceau/`, sha256 de `chain/cacert.pem` et `chain/tsa.crt` égaux au bloc, valeurs
  du bloc aux préfixes de D.4 c (`2151b611`, `8bfb0305`, constante `PREFIXES`) ; `openssl ts -verify -in paquet.tsr
  -queryfile paquet.tsq -CAfile chain/cacert.pem -untrusted chain/tsa.crt` (arguments de `verify.sh`) sort 0 ; serrage
  (E2) : `openssl ts -verify … -data PAQUET.sha256` sort 0 et le manifeste porte une ligne au sha256 du paquet. T0 =
  genTime lu dans `openssl ts -reply -in paquet.tsr -text` (une seule ligne `Time stamp:` ; forme d'OpenSSL ou ISO
  8601 ; fraction de seconde portée à la seconde suivante).
- **(6) voie (b)** : `docs/adr-0028/sceau/GO-sans-ancre.txt`, UTF-8 strict sans BOM, LF, exactement les trois lignes
  `date: <ISO 8601 UTC>` (secondes et fraction facultatives, `Z` ou `+00:00`, date du calendrier), `ordre: exécuter sans
  ancre`, `signataire: investisseur`, LF final ; première ligne de `JOURNAL.md` à HEAD qui porte son sha256 strictement
  après la première qui porte le sha du paquet. T0 = date de commit (`%ct`) du premier commit de `git log --no-textconv
  --reverse -S<sha> HEAD -- JOURNAL.md`.
- **(5)** : T_now ≥ T0 + 24 h, T0 = le plus tardif des T0 des voies établies ; sans voie établie, T0 indéterminé :
  refus. **(6)** : refus si aucune voie ne s'établit. L'horloge seule n'ouvre jamais : sans preuve, (5) et (6)
  refusent, même en 2100. T_now : `datetime.now(timezone.utc)` ; l'horloge n'est injectable qu'en processus (argument
  `maintenant` de `verifier_gardes` et de `main`), jamais par une option ni une variable d'environnement.

## 3. Sous-lots

Coupe R-25 : C1 coupé en C1a (lecteur du bloc), C1b (squelette, ligne de commande, gardes (1) et (4)), C1c (gardes (2)
et (3), EX-E1-1) ; C2 en C2a (voie (a), garde (5), lecture de genTime) et C2b (voie (b)). Chaque arbre intermédiaire
refuse par défaut : une garde non encore construite refuse (`garde construite au sous-lot … : refus`). Mesure :
`faire_diff.py` (ajouts et retraits, numstat), chaque diff contre l'arbre précédent. Tests d'abord à chaque pas : tests
ajoutés à l'arbre précédent, échec montré, puis code.

### 3.1 C1a — lecteur du bloc machine

- Tests : `test_bloc_absent_duplique_malforme` (lecteur seul) : forme nominale lue à l'identique (attendu écrit à la
  main : sha256 des octets de l'outil et des journaux de fixture) ; 14 variantes de lignes (clé absente, journal absent,
  quatrième journal, clé dupliquée de même valeur, journal dupliqué à quatre lignes, majuscules, sha tronqué, commit
  court, champ en trop, clé inconnue, tabulation, ligne vide, retour chariot, nom `../c`) et 5 variantes de texte (aucun
  bloc, deux blocs, non fermé, ouverture voisine à tildes, ouverture à tildes) : refus, motif `ouverture` pour les
  secondes.
- Échec avant (tests sur l'arbre `HEAD`, outil absent ; `preuves/C1a-avant.out` `b4f96e9c…`) : `FileNotFoundError`.
  Après : `Ran 1 test … OK`.
- Mutants (`preuves/C1a-mutants.out` `f3275530…`) : **13 tués sur 13** — B1 clé dupliquée admise, B2 journal dupliqué
  admis, B3 clé absente admise, B4 nombre de journaux non contrôlé, B5 majuscules, B6 sha tronqué, B7 champ en trop, B8
  ligne inconnue ignorée, B9 nom hors forme, B10 second bloc ignoré, B11 ouverture voisine ignorée, B12 fermeture non
  exigée, B13 commit tronqué.
- Suite : `Ran 344 tests in 35.560s`, `OK (skipped=2)` (`a8224d06…`). Règle : `ea3a2d94…`, identique à l'octet.
- Numstat : outil +37 ; tests +65 ; total **102 lignes**.

### 3.2 C1b — squelette, ligne de commande, gardes (1) et (4)

- Tests : fixture `monter` (dépôt jetable, `core.autocrlf=false`, commit c1 du code d'analyse, puis paquet et
  `JOURNAL.md` ; journaux et fichier de sommes à cinq entrées hors dépôt) ; `lancer` (main en processus : code, gardes
  refusées lues sur stderr, dossier parent inchangé, répertoire de sortie absent, refus ⇔ code ≠ 0 ⇔ stdout vide) ;
  `test_nominal_et_cli` (en processus et par la ligne de commande : code 2, seules les gardes non construites
  refusent) ; paquet sans bloc : refus `bloc` et (4) non évaluée ; `test_garde_1_sha_du_paquet_a_head` (préfixe de huit
  chiffres, sha suivi ou précédé d'un chiffre hexadécimal, absent, présent sur le disque seulement) ;
  `test_garde_4_sha_du_script` (dernier chiffre changé).
- Échec avant (tests sur l'outil C1a ; `preuves/C1b-avant.out` `ad92789a…`) : `FAILED (errors=8)`,
  `AttributeError: module 'rendu_unique' has no attribute 'main'`. Après : `Ran 4 tests … OK`.
- Mutants (`preuves/C1b-mutants.out` `865237b4…`) : **11 tués sur 11** — B0 bloc jamais lu, G1a `JOURNAL.md` lu sur le
  disque, G1b sous-chaîne admise, G1c préfixe admis, G1d (1) neutralisée, G4a (4) neutralisée, G4b autre fichier haché,
  R1 exception avalée, N1 gardes non construites levées, X1 code de refus perdu, X2 refus non imprimé. C1a rejoués sur
  C1b : 13 sur 13 (même sha256 de sortie `f3275530…`).
- Suite : `Ran 347 tests in 34.422s`, `OK (skipped=2)` (`61b14985…`). Règle : identique.
- Numstat : outil +103 ; tests +91 −5 ; total **199 lignes** (202 avant le passage de `sha256_fichier` à
  `hashlib.file_digest`, E13).

### 3.3 C1c — gardes (2) et (3), EX-E1-1

- Tests : `test_garde_2_code_d_analyse` — commit qui change `tools`, fichier suivi modifié, indexé, fichier non suivi,
  fichier ignoré (`tools/__pycache__/t.pyc`), chacun aussi avec `--depot` sur le sous-dossier `s2-harness` ; commit du
  bloc absent du dépôt ; témoin : commit hors des chemins, (2) levée. `test_garde_3_journaux_bloc_et_sommes` — sommes
  qui diffèrent du fichier et du bloc (sha des sommes au bloc mis à jour), bloc qui diffère du fichier et des sommes,
  journal absent des sommes, nom répété, ligne non conforme, journal modifié, sommes modifiées hors de leurs entrées
  (ligne vide ajoutée), journal absent du dossier ; témoin : sommes en CRLF, marque binaire, majuscules, (3) levée.
- Échec avant (tests finaux sur l'outil C1b ; `preuves/C1c-avant.out` `e14ee6dd…`) : `FAILED (failures=22)`. Une
  première passe, faite avant la correction de l'attendu du paquet sans bloc (E11), donnait `failures=23` (`04a09b1b…`,
  fichier remplacé).
- Mutants (`preuves/C1c-mutants.out` `c4256abc…`) : **17 tués sur 17** — D1 `git diff` retiré, D2 erreur de `git diff`
  admise (code 1 seul), D3 `git status` retiré, D4 ignorés admis, D5 non suivis admis, D6 racine non résolue ; S1
  comparaison au bloc retirée, S2 comparaison aux sommes retirée, S3 sha du fichier de sommes non contrôlé, S4 CRLF
  refusé, S5 marque binaire refusée, S6 majuscules refusées, S7 nom répété admis, S8 ligne non conforme ignorée, S9
  hexadécimal non ramené en minuscules ; G2 et G3 gardes neutralisées. C1a et C1b rejoués sur C1c : 24 sur 24
  (`df363d05…`).
- Suite : `Ran 349 tests in 34.614s`, `OK (skipped=2)` (`184b7b5e…`). Règle : identique.
- Numstat : outil +42 −3 ; tests +60 −10 ; total **115 lignes**.

### 3.4 C2a — voie (a), garde (5), lecture de genTime

- Tests : autorité RFC 3161 de test produite par `openssl` dans le test (CA de test `CA:TRUE` critique, certificat de
  TSA signé par elle, extension timeStamping critique, requête `-sha256 -cert` comme `make-tsq.sh`, réponse
  `ts -reply`), sous `OPENSSL_CONF` minimal ; `openssl` absent : `assertTrue` échoue, jamais de saut.
  `test_voie_a_jeton_verifie_et_garde_5` : préfixes de D.4 c remplacés par ceux de la chaîne de test (`mock`) ;
  horloge à genTime + 24 h, borne haute (horloge lue après la réponse, plus une seconde) : code 0, `gardes levées`,
  rien d'écrit ; une seconde avant la borne basse + 24 h (horloge lue avant la requête) : refus (5) seul ; préfixes
  réels : refus (5) et (6). `test_voie_a_refus` (horloge à genTime + 48 h) : bloc d'une autre chaîne que `cacert.pem`
  puis que `tsa.crt` (même préfixe), requête d'un autre nonce, jeton sur d'autres octets que `PAQUET.sha256`,
  manifeste qui ne liste pas le paquet (jeton sur ce manifeste), jeton d'une autre autorité : refus (5) et (6).
  `test_ni_jeton_ni_go_horloge_seule` : sans dossier de sceau puis dossier vide, horloge en 2100 : refus (5) et (6) ;
  ligne de commande : même refus, et `--maintenant` y est refusé (`unrecognized arguments`). `test_gentime_formes` :
  forme d'OpenSSL, CRLF avec fraction (`Dec 31 23:59:59.5 2026 GMT` → 2027-01-01 00:00:00), ISO 8601 à fraction
  nulle ; vide, deux lignes, décalage `+01:00` : refus. Docstring du test nominal, désormais : « Fixture sans jeton ni
  go : seules refusent (5) et (6) ».
- Échec avant (tests sur l'outil C1c ; `preuves/C2a-avant.out` `ba939072…`) : `FAILED (errors=8)` — 7 fois
  `module 'rendu_unique' has no attribute 'PREFIXES'`, une fois `… 'gentime'` ; `test_ni_jeton_ni_go_horloge_seule`
  vert dès C1c (les gardes non construites refusent, E14). Après : `Ran 10 tests … OK`.
- Mutants (`preuves/C2a-mutants.out` `5c91880e…`) : **16 tués sur 16** — A1 sha de la chaîne non comparé, A2 préfixes de
  D.4 c non contrôlés, A3 `tsa.crt` non contrôlé, A4 `-queryfile` retiré, A5 `-data` retiré, A6 manifeste non lu, A7
  code d'`openssl` ignoré, A8 fraction tronquée, A9 CRLF non retiré, A10 forme ISO non lue, A11 première de plusieurs
  lignes lue ; T1 délai retiré, T2 T0 indéterminé admis, T3 délai de 23 h, T4 (6) neutralisée, T5 voie en échec tenue
  pour établie. Rejeu des listes de C1 sur C2a (`3e2e8299…`) : C1a 13 sur 13, C1c 17 sur 17 ; C1b arrêtée au mutant N1,
  dont l'ancre `non_construite` disparaît à C2a (toutes les gardes sont construites) : 8 rejoués, 8 tués ; X1 et X2
  rejoués sur l'arbre final (§3.6).
- Suite : `Ran 353 tests in 38.255s`, `OK (skipped=2)` (`e5992b04…`). Règle : identique.
- Numstat : outil +76 −4 ; tests +112 −5 ; total **197 lignes** (201 avec un bouche-trou `voie_b` ; remplacé par
  `VOIES` réduit à la voie (a), même effet).

### 3.5 C2b — voie (b), fichier de go

- Tests : `epingler` (go posé, ligne de `JOURNAL.md` qui porte son sha, commit daté par `GIT_COMMITTER_DATE`).
  `test_voie_b_go_epingle_et_garde_5` : textconv hostile posé sur `JOURNAL.md` (`.git/info/attributes`,
  `tr a-f A-F`) ; go épinglé le 2026-09-01 00:00:00Z puis cité de nouveau le 2026-09-11 : horloge à T0 + 24 h
  exactement : code 0 ; une seconde avant : refus (5) seul ; ligne de commande, heure système : go épinglé trois jours
  plus tôt, code 0 et `gardes levées` ; go épinglé à l'instant : refus (5). `test_voie_b_refus` (horloge en 2100) :
  BOM, CRLF, sans LF final, ligne de plus, sans accent, Latin-1, date hors ISO, mois 13, sans fuseau ; sha absent de
  `JOURNAL.md`, en préfixe, sur le disque seulement, avant la ligne du scellement, sur cette même ligne : refus (5) et
  (6). `test_deux_voies_t0_le_plus_tardif` : go épinglé trois jours avant le jeton ; horloge à T0 du go + 25 h : refus
  (5) ; à genTime + 24 h (borne haute) : levées.
- Échec avant (tests sur l'outil C2a ; `preuves/C2b-avant.out` `faed31e0…`) : `FAILED (failures=1)` (nominal de la
  voie (b)) ; les tests de refus de la voie (b) et des deux voies passent dès C2a, la voie (b) n'y existant pas (E14).
  Après : `Ran 13 tests … OK`.
- Mutants (sur les octets finaux, `preuves/final-mutants.out` §3.6) : **16 tués sur 16** — V1 BOM admis, V2 ligne de
  plus admise, V3 CRLF admis, V4 Latin-1 admis, V5 date hors calendrier, V6 date sans fuseau, V7 ordre sans accent, V8
  sha du go non cherché, V9 postériorité non contrôlée, V10 même ligne admise, V11 textconv appliqué, V12 dernier
  commit pris pour T0, V13 voie (b) absente, V14 T0 le plus ancien, V15 borne T0 + 24 h exclue, V16 date d'auteur au
  lieu de la date de commit.
- Suite : `Ran 356 tests in 37.879s`, `OK (skipped=2)` (`66f8373e…`). Règle : identique.
- Numstat : outil +23 −2 ; tests +68 −1 ; total **94 lignes** (la ligne d'en-tête de l'outil y perd la mention des
  gardes non construites, périmée à l'état final).

### 3.6 Rejeu sur les octets finaux et démonstration sans `openssl`

- `preuves/final-mutants.out` (`73bbd979…`) : C2b 16 sur 16 ; `mutants_final.py` 17 sur 17 (7 neutralisations
  canoniques, §4, et la liste de C1b sans N1 : B0, G1a à G1d, G4a, G4b, R1, X1, X2) ; C1a 13 sur 13 ; C1c 17 sur 17 ;
  C2a 16 sur 16 : **79 tués sur 79**, aucun vivant, aucun équivalent déclaré.
- `openssl` retiré du PATH (dossier de liens vers `git`, `tr`, `sh` seulement ; `preuves/sans-openssl.out`
  `ffb068f5…`) : `FAILED (failures=3)`, les trois tests de la voie (a) avec le motif
  `openssl absent : le test échoue, il ne saute pas`, 0 saut ; les autres verts.

## 4. Une garde, sa fixture, son mutant

| garde | fixture qui la déclenche (code 2, rien d'écrit) | test | neutralisation (`GARDES` : garde qui ne refuse jamais) |
|---|---|---|---|
| bloc | paquet sans bloc | `test_bloc_absent_duplique_malforme` | Nbloc tué (+ B0 à B13) |
| (1) | sha du paquet absent de `JOURNAL.md` à HEAD (5 variantes) | `test_garde_1_sha_du_paquet_a_head` | N(1) tué (+ G1a à G1d) |
| (2) | code différent, arbre modifié, commit absent (11 cas) | `test_garde_2_code_d_analyse` | N(2) tué (+ D1 à D6) |
| (3) | journaux, bloc et sommes en désaccord (8 variantes) | `test_garde_3_journaux_bloc_et_sommes` | N(3) tué (+ S1 à S9) |
| (4) | `sha256_script` faux | `test_garde_4_sha_du_script` | N(4) tué (+ G4a, G4b) |
| (5) | une seconde avant T0 + 24 h (voies a et b) ; deux voies ; T0 indéterminé | quatre tests de (5) et (6) | N(5) tué (+ T1 à T3, V14 à V16) |
| (6) | ni jeton ni go, horloge en 2100 ; voie (a) refusée (6) ; voie (b) refusée (14) | `test_ni_jeton_ni_go_horloge_seule`, `test_voie_a_refus`, `test_voie_b_refus` | N(6) tué (+ T4, T5, A1 à A11, V1 à V13) |

Cas nominal : voie (a) en processus (code 0, `gardes levées`) ; voie (b) en processus et par la ligne de commande
(code 0). Le refus « rien d'écrit » est contrôlé à chaque appel de `lancer` (dossier parent inchangé, répertoire de
sortie absent) et, par la ligne de commande, par stdout vide et code 2.

## 5. Empreintes

- Diffs (étiquettes `a/s2-harness/…`, `b/s2-harness/…`, sans opération git), chacun contre l'arbre précédent :
  `C1a.diff` `6b4807eb6ae3b1943608d5f11ddeacf7957d0d0959e105bef28a7c49e7381238` (contre `01b8cb5`) ; `C1b.diff`
  `416905091f06bef29d304c1ff616f562ac3984d7f7a403acda3272aef56be749` ; `C1c.diff`
  `dbf09a1aee419a685a4c84b37b57971cdddd0f89f29827cdb0bee6587cfdb7a7` ; `C2a.diff`
  `ce535edb686b4dc8b26235cbad159ec7d2d168c2d9bda2b0d73348fff8bf063e` ; `C2b.diff`
  `e729c882012a19533ee74ac847a29fefffe32b46ce00bbb1fed56050b335377a`. Contrôle par `patch -p1` sur l'export de
  `01b8cb5` : chaque diff donne l'instantané de son sous-lot, et la fin de chaîne égale l'arbre de travail (`diff -r`
  vide).
- Fichiers finaux (sha256) : `s2-harness/tools/rendu_unique.py`
  `7b0212fd72e4fa3413c664ec29fa2b9f6fa93ae7ed460098b337ded6a7d25e64` (272 lignes) ;
  `s2-harness/tests/test_rendu_unique.py` `ea5a0a39e1ce834ebbcb7e8cef07c39cb53c56e6291782d311145d16ef8e1320` (375
  lignes).
- Suites recomptées : 343 (départ) → 344 (C1a) → 347 (C1b) → 349 (C1c) → 353 (C2a) → 356 (C2b), deux sauts à chaque pas
  (les deux tests de la variable scellée). Règle scellée : `ea3a2d94…` sur les six arbres, `cmp` identique au JSON de
  `HEAD`.
- R-13 et secrets : motif R-13 du hook et motifs VENDOR et GENERIC de la gate des secrets rejoués par `grep` sur les
  trois fichiers neufs (outil, tests, ce journal) : 0 occurrence. Aucune dépendance neuve (`shutil`, `datetime`,
  `hashlib.file_digest` : bibliothèque standard ; `openssl` et `git` : programmes déjà requis par le G0 et par
  `oracle_record`).
- Brouillons mis à part, non cités comme preuves : premier jet (322 lignes d'un tenant,
  `brouillons/arbre-C1a-premier-jet`) et second jet (226 lignes, `brouillons/arbre-C1a-second-jet-226`), retirés de
  l'arbre avant la reprise tests d'abord ; preuves antérieures à la correction de l'en-tête (C2b) :
  `preuves/anterieur/avant-entete/` ; tout a été rejoué ensuite.

## 6. Écarts

- **E1 (coupe)** : C1 et C2 coupés en cinq sous-lots (C1a, C1b, C1c, C2a, C2b), chacun sous 200 lignes ; deux premiers
  jets trop grands (322, puis 226 lignes) mis de côté, refaits tests d'abord.
- **E2 (serrage, voie (a))** : au-delà des arguments de `verify.sh`, le jeton doit porter sur les octets de
  `PAQUET.sha256` (`-data`) et ce manifeste doit lister le sha256 du paquet. Sans ce lien, un jeton valide sur un autre
  manifeste (paquet antérieur à un veto A-8, par exemple) ouvrirait (6) et fixerait T0 (T-16). Les préfixes de D.4 c,
  présents au G0 et absents du brief, sont contrôlés sur les valeurs du bloc.
- **E3 (serrage, (2))** : les fichiers ignorés (`__pycache__`) comptent comme modification de l'arbre (un `.pyc`
  périmé se charge même sous `-B` : sonde `pyc/`, §1.3) ; `--no-ext-diff --no-textconv` ajoutés à `git diff` ;
  `--depot` ramené à la racine.
- **E4 (serrage, voie (b))** : c'est la **première** occurrence du sha du go qui doit suivre la première ligne du sha du
  paquet : un go cité avant le scellement puis de nouveau après est refusé ; la même ligne est refusée.
- **E5 (lecture de (5))** : deux voies établies : T0 = le plus tardif ; aucune : (5) refuse aussi (T0 indéterminé).
- **E6 (lecteur des sommes)** : grammaire de `sha256sum`, mais une ligne mal formée refuse (`sha256sum -c` sans
  `--strict` n'avertit que).
- **E7 (`git log -S --no-textconv`)** : ajouté après la sonde (le pickaxe applique le textconv).
- **E8 (horloge)** : injectable en processus seulement (argument `maintenant`), jamais par option ni variable
  d'environnement (le brief admettait les deux).
- **E9 (`--sortie`)** : exigée et inutilisée en C1 et C2 (rien n'est écrit) ; sa sémantique est celle de C3.
- **E10 (genTime)** : deux formes lues : celle de la sortie d'OpenSSL 3.0.13 (sonde) et une forme ISO 8601 que je
  prête, de mémoire et sans l'avoir lue, aux options de date des versions récentes d'OpenSSL [inféré] ; CRLF toléré
  (sortie d'un `openssl.exe` en mode texte), fraction portée à la seconde suivante.
- **E11 (attendu corrigé)** : à C1c, l'attendu du paquet sans bloc passe de `bloc, (4)` à `bloc, (2), (3), (4)` : les
  gardes (2) et (3), désormais construites, ne s'évaluent pas sans bloc ; correction du test, non du code.
- **E12 (aides de test partagées)** : `HARNESS`, `g` et `GIT_ENV` importés de `tests.test_oracle_record`, comme ce
  module importe `HARNESS` de `tests.test_exclusion`.
- **E13 (Python ≥ 3.11)** : `hashlib.file_digest`, même exigence de version que l'extraction filtrée d'`oracle_record`.
- **E14 (tests verts avant leur sous-lot)** : `test_ni_jeton_ni_go_horloge_seule` (dès C1c) et les tests de refus de la
  voie (b) et des deux voies (dès C2a) passent avant leur code, parce que l'état antérieur refuse par défaut ; leur
  pouvoir de discrimination est montré par T2, T4, V1 à V10 et V14.
- **Hors périmètre, à porter en C3** : l'appel à `records.verifier_raw` (G0 §B, second ajout : SHOGEN-RAW-FIN-1),
  l'écriture des sorties, l'enregistrement d'oracle, SHOGEN-RECALCUL-TIERS-CLI-1, SHOGEN-CENSURE-CAUSES-TIERS-1,
  SHOGEN-ENREG-AUTEUR-ECRITURE-1 : non touchés.

## 7. Limites rencontrées (items à former, règle PAROXYSME)

- **L1 — SHOGEN-SCEAU-VERIFY-CHEMINS-1** : `make-tsq.sh` écrit le manifeste avec des chemins relatifs à la racine du
  dépôt ; l'étape (1) de `verify.sh` le relit depuis le dossier de sceau : `MANIFESTE : ÉCART`, code 2, avant la
  vérification du jeton (sonde §1.3). `rendu_unique` n'en dépend pas (lien manifeste-paquet par le sha, E2).
  Construction : dans `verify.sh`, `sha256sum -c "$D/PAQUET.sha256"` depuis la racine ; sonde en dépôt jetable comme
  test. Déclencheur : lot PAQUET (partie 3), avant l'acte d'ancrage. Prix : une ligne et une sonde [inféré].
  `scripts/sceau/` est hors de mon périmètre.
- **L2 — SHOGEN-RENDU-OPENSSL-HOTE-1** : OpenSSL 3.5.7 de l'hôte non éprouvé ici : forme de la ligne `Time stamp:`
  (deux formes lues), commandes de la fixture (`req -x509 -CA`, `-addext`, `ts -reply` sous `OPENSSL_CONF`) ; sous
  Windows, `openssl` doit être dans le PATH de la suite (sinon trois tests échouent, par construction, et
  l'enregistrement d'oracle du rendu, qui lance la suite, porterait un échec). Construction : rejouer la suite sur
  l'hôte ; capturer la sortie `-text` du jeton FreeTSA réel dès qu'il existe. Déclencheur : revue de partie 2 ou
  première suite sur le poste Windows. Prix : une commande [inféré].
- **L3 — SHOGEN-SOMMES-FORMAT-1** : le fichier de sommes réel n'est pas lisible en session cloud (poste local) ; le
  lecteur suit la grammaire de `sha256sum` et compare les noms à l'identique (`<nom>` du bloc, relatif à `--journaux`).
  Une forme `SHA256 (nom) = …` ou des noms préfixés `./` refuseraient (3). Construction : lancer l'outil en refus sur le
  poste local avant le scellement ((3) ne doit pas paraître) ; étendre le lecteur sur fixture si besoin. Déclencheur :
  lot PAQUET (remplissage du bloc). Prix : une exécution [inféré].
- **L4 — SHOGEN-GO-ORDRE-COMMITS-1** : l'ordre des lignes de `JOURNAL.md` tient lieu d'ordre dans le temps (journal
  ajouté en fin seulement) ; un commit qui insérerait la ligne de scellement au-dessus d'un go antérieur satisferait
  le critère de ligne. Construction : exiger que le commit qui introduit le sha du go descende de celui qui introduit
  le sha du paquet (`git merge-base --is-ancestor`), fixture à lignes réordonnées. Déclencheur : décision de
  l'orchestrateur (Q2). Prix ≈ 4 lignes et 10 de tests [inféré].
- **L5 — SHOGEN-GO-DATE-1** : la date portée par le fichier de go n'est contrôlée qu'en forme ; ni comparée au commit
  qui l'épingle, ni à T_now. Construction : refuser un go daté après son commit, ou prendre T0 = max(commit, date du
  go). Déclencheur : Q3. Prix ≈ 2 lignes et 4 de tests [inféré].
- **L6 — SHOGEN-RENDU-T0-SORTIE-1** : `verifier_gardes` ne rend que les refus ; C3 a besoin de la voie retenue, de T0 et
  de genTime (`sceau.genTime` de l'enregistrement d'oracle). Construction : rendre aussi les preuves (voie, T0).
  Déclencheur : C3. Prix ≈ 3 lignes [inféré].
- **L7 — SHOGEN-RENDU-PYCACHE-1** : par E3, un `__pycache__` sous `s2-harness/shogen_s2` ou `s2-harness/tools` fait
  refuser (2) ; toute commande Python sur ces chemins doit tourner sous `-B` avant l'exécution unique (refus sans
  écriture, relançable). Construction : consigne au RUNBOOK ou au paquet, ou extraction par `git archive` en C3 (comme
  `oracle_record`). Déclencheur : C3 ou lot PAQUET. Prix : deux lignes de texte [inféré].

## 8. Questions ouvertes

- **Q1** (E2) : le serrage de la voie (a) (jeton sur les octets de `PAQUET.sha256`, manifeste qui liste le paquet)
  est-il retenu, ou la voie (a) s'en tient-elle aux seuls arguments de `verify.sh` ?
- **Q2** (L4) : l'ordre des commits (go descendant du scellement) entre-t-il à la voie (b) ?
- **Q3** (L5) : la date du fichier de go est-elle confrontée au commit qui l'épingle ?
- **Q4** (L1) : qui corrige `verify.sh` (lot PAQUET, ou un lot de l'étape C) ?
- **Q5** (E9) : `--sortie` exigée dès C1 et C2, sans effet, convient-elle comme interface de C3 ?

## 9. Clôture

- Suite finale (arbre de travail) : `Ran 356 tests in 37.879s`, `OK (skipped=2)` (`preuves/C2b-suite.out`) ;
  `SHOGEN_S2_CAMPAGNE_CONTROL` absente (`env | grep -c` : 0).
- `cargo --locked xtask verify` : avant la rédaction (08:1x UTC), `=== VERDICT GLOBAL : VERT ===`, rc 0 (S-G4 76
  fichiers sur 76, S-G5 77 sur 77, corpus complet 125 artefacts sur 125, 252 fragments contrôlés, 2 852 écartés sous
  seuil ; `preuves/xtask-avant-journal.out` `18df09a6…`). Relance avec ce journal en place : verdict et sha256 de ce
  fichier dans le rapport de remise à l'orchestrateur (un fichier ne porte pas son propre sha).
- `git status` final : neufs `s2-harness/tools/rendu_unique.py`, `s2-harness/tests/test_rendu_unique.py` et ce journal ;
  rien de modifié.
