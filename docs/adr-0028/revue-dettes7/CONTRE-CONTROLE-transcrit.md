# Contre-contrôle neuf de DETTES-T7 (R-1 à R-7 ; clôture CONFORME) (transcrit)

> Transcription par l'orchestrateur le 2026-10-16 07:19:00 UTC du fichier dettes7/g2/cc/RAPPORT-CC.md ; contrôle FM-1.1 des transcripts du générateur, du réviseur G2 et du contre-contrôleur, par le fm11.py versé et par celui de DT3-E : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Contre-contrôle neuf du lot DETTES-T7 (série DT7-a à DT7-t)

- **Modèle** : `claude-opus-5-5` (Gate 0 : identifiant exact donné par l'environnement ; effort `max` déclaré par le
  lanceur, non observable de l'intérieur). Contre-contrôleur neuf : je n'ai ni écrit ni relu ce lot.
- Heures (`date -u`) : début 2026-10-15 12:09:18 UTC ; fin : section 9.
- Brief `g2/cc/BRIEF-CC.md` (`14e0aa67…`) lu en entier ; décisions de `ADJUDICATION.md` (`888775dd…`, avec ses trois
  ajouts) appliquées. Pièces lues en entier : `g2/RAPPORT-G2.md` (`f803c9db…`), `RAPPORT-GENERATEUR.md` (`1829a158…`,
  phases 1 à 3), `BRIEF-DETTES-T7.md` (`07c5c055…`), `ITEMS-ANNEXE-B.md` (`cb92193f…` ; ses 23 lignes égales, par
  script, aux lignes citées de `docs/adr-0028/ANNEXE-B-items.md` à la tête `a639ba8`).
- **Série** : 23 diffs dans l'ordre a, b, c1, c2, c3, c4, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t ; empreinte
  de la concaténation recalculée : `1f60b3315afc2be1edb6a367cdc0b92b640c874c020ade18d7b3c883a7f5b5d8` (égale au
  brief). DT7-l à DT7-s identiques à l'octet à `g2/corrections/C-1.diff` à `C-8.diff` (`cmp`, 8 sur 8 ; empreinte des
  corrections `1564adc9…`, égale à l'adjudication).
- **Têtes** : `5d4f2dd` (12:11:16, copie finale de la série), `0be8e9d` (12:45:16), `cb03207` (13:30:55), `a639ba8`
  (13:49:39). Depuis `87249c2` (base du générateur), le seul chemin de la série touché est `.github/workflows/gates.yml`
  (planchers de la tête : s2bis 358 puis 371, 373, 374 ; calib-actifs 65 puis 78), hors des hunks de DT7-f. **La série
  s'applique sur la tête du moment** : copie neuve de `a639ba8`, 23 sur 23 (`git apply --check` puis `git apply`),
  fichiers de la série égaux à la copie finale sauf `gates.yml` (planchers de la tête) ; réserves R-1 à R-7, 7 sur 7.
  Tête relue en fin de passe (13:55:53) : `3b5d484` (versement de DETTES-T2) ; `git diff --stat a639ba8 3b5d484` limité
  aux chemins de la série et des réserves : vide (préimages inchangées).
- **Constat d'entrée** : le dossier `cc/` portait une tentative antérieure de contre-contrôle (2026-10-10, 08:49 à
  09:32 UTC, sans rapport, interrompue). Déplacée à l'identique dans `tentative-1/` ; ses copies périmées supprimées
  (5158 puis 6040 Mo libres). Son `NOTES.md` a été lu au démarrage, et son `R-1.diff` après que mon R-1 a été écrit et
  éprouvé : signal seulement, rien n'en est repris sans mesure (les deux R-1 convergent).

## Verdict : CONFORME-AVEC-RÉSERVES (R-1 à R-7)

Les huit corrections sont celles de la G2 à l'octet, justes et testées (rouge puis vert rejoués) ; DT7-t tient ; toutes
les étapes `run:` de `gates.yml` (g3 `--tree` et `--history` exclus), la matrice, l'étape Tests du job `squelette` et
`xtask` sont verts sur la série (S-G9 rouge, copie creuse, attendu). Mais deux promesses du brief ne sont pas tenues en
entier : des processus d'une campagne survivent encore (descendant détaché, course, enfant d'une autre session après
une sortie normale) ; l'attente de l'enregistreur après le reliquat dépend encore de l'arrêt de l'arbre. La remarque
du générateur est un défaut. Trois de mes mutants survivent sans être équivalents. Sept réserves, chacune avec sa forme
exacte (`propose/R-n.diff`), son rouge et son vert, éprouvées ensemble sur la série entière.

| R-n | vise | objet | +/− (`.py`) | sha256 |
|---|---|---|---|---|
| R-1 | C-1, remarque du générateur | `mutants.py` : la première étape doit être le checkout épinglé du gabarit K (lignes brutes du job : `ETAPES[1]`, `with:`, `persist-credentials: false`, puis `fetch-depth: 0` admis) ; cas `tete-if`, `tete-action`, `tete-with`, `fetch-depth: 0` admis ; README daté | +35 −10 (28) | `9822749b…` |
| R-2 | C-1, MUTANTS-ORPHELINS-1 | `mutants.py` : sous Linux, moissonneur (`prctl(PR_SET_CHILD_SUBREAPER)` par `ctypes`) ; après chaque étape, à la borne comme à la sortie, `balayer` arrête tout descendant vivant jusqu'au dernier ; relevé de fin qui le dit ; hors Linux, limite de C-1 écrite ; cas M9, M10 ; README daté | +96 −6 (87) | `b4a428e0…` |
| R-3 | C-2, ENREG-DELAI-ARBRE-1 | `oracle_record.py`, `lancer` : `p.kill()` avant `p.wait()` après le reliquat ; cas de l'arrêt d'arbre échoué (simulé) ; README daté | +20 −4 (13) | `b18d7f7d…` |
| R-4 | même classe, vérificateur | `verdict-suite-s2.py`, docstring de `lancer` : limites mesurées (tuyaux gardés : attente sans borne propre ; descendant en session propre : survit, peut recréer le dossier du compte) | +5 −1 (5) | `b4678042…` |
| R-5 | C-1 (mutant CC7 vivant) | `test_mutants.py` : cas M11 (étapes illisibles sous un mutant de `gates.yml` : FATAL) ; README daté | +12 −3 (7) | `da891da2…` |
| R-6 | DT7-b (mutant CO4 vivant) | `test_oracle_record.py` : lien `docs/sous/vers-haut -> ../rapports/d.md` (cible normalisée) ; exclus 13 | +10 −7 (10) | `a0a12bfd…` |
| R-7 | DT7-c3 (mutant CR1 vivant) | runner : cas S-14, chaque fin de ligne autre que LF seule dans le nom du job (U+0085 compris), `CAS = 153` | +5 −1 (5) | `ab95e0d1…` |

Ordre d'application : après DT7-t, R-1 à R-7 (R-2 suit R-1 ; R-5 suit R-2 ; R-6 suit R-3). Empreinte de la
concaténation R-1 à R-7 : `77e83ecffb4f9884efb381bfc3e0ee18d32866e75b13dc0bea9359ae35745460`. Contrôle par script sur
les octets : aucune ligne ajoutée de plus de 120 caractères, aucune barre oblique inverse, aucun marqueur de dette ; R-25
tenu (au plus 87 lignes `.py` ajoutées) ; planchers : S2 423, controle 39 inchangés (tests étendus) ; runner 152
puis 153 (R-7, `CAS`, seule mention normative du compte).

## 1. Corrections C-1 à C-8 (DT7-l à DT7-s)

| C-n | rouge rejoué (code d'avant, tests de la correction) | vert (`-X dev -W error`) | jugement |
|---|---|---|---|
| C-1 | 2 FAIL en 95,6 s : durée de la campagne non < 40 s (M7), M8 `vivant` à 2 étapes au lieu de `tué` à 1, refus `tete` absent `(0, ['M1'], False)` (`sorties/c1-rouge.txt`) | 2 OK, 11,5 s, 0 ligne `Exception ignored`/`Warning` | juste pour ce qu'il vise ; défauts restants : R-1, R-2, R-5 |
| C-2 | 1 FAIL : `duree3 < 30` faux, 95,4 s (`sorties/c2-rouge.txt`) | OK (avec C-3 : 2 OK, 11,5 s) | juste sous POSIX ; R-3 |
| C-3 | 1 ERROR `FileNotFoundError` (lien `docs/vers-dossier` pendant) (`sorties/c3-rouge.txt`) | OK | juste ; R-6 (site de normalisation, DT7-b) |
| C-4 | texte | — | juste : Q-3 et Q-5 adjugées, ordre `champs` puis `ancien outil` conforme au code (`verifier`) |
| C-5 | texte | — | juste : lint l.8 `l.23-55`, 113 caractères avant et après, 212 lignes ; CLAUDE.md l.23 ouvre le point 7, l.55 le clôt |
| C-6 | texte | — | juste : l'exception a la forme des l.18-22 du G0 de PLAN-S2BIS (lu : l.22 achève l'épinglage) ; trois causes sous 3.10 rejouées (section 6) |
| C-7 | texte | — | juste : ajout daté en fin d'ADR-0028 (337 puis 345 lignes), schéma gardé v1 comme adjugé |
| C-8 | texte | — | juste : les 34 lignes de la tête de `shogen-extracteur.md` retrouvées dans l'ordre, à l'octet ; ajouts l.11-13 et l.38-47, datés après 06:24:31 |

Rouges faits sur une copie `tête + a..k` où seuls les hunks de test de la correction sont posés (`git apply --include`).

### Processus d'une campagne à la borne (C-1) : mesure `outils/exp_survie.py`

Outil de la série, borne 3 s, un mutant par cas, marque posée quelques secondes après par un enfant `sh` (stdio coupés) :

| cas | outil de la série | outil R-2 |
|---|---|---|
| S1 enfant en session neuve, parent vivant à la borne | arrêté (0 marque) | arrêté |
| S2 descendant détaché (setsid, parent sorti) à la borne | **survit** (1 marque) : limite écrite par C-1 | arrêté |
| S3 enfant en session neuve, étape sortie en 0 | **survit** (1) ; mutant `vivant` | arrêté |
| S4 idem, étape sortie en 1 | **survit** (1) ; mutant `tué` | arrêté |
| S5 course : enfants en session neuve toutes les 20 ms, borne | **survit** sur 2 runs de 3 (1, 0, 1 marque) | 0, 0, 0 |

Relevé de fin de l'outil de la série : `aucun processus des 147 groupes de la campagne`, alors que 3 processus du cas
vivaient à la fin : le relevé ne voit que les groupes qu'il a consignés. S3, S4 et la course ne sont écrits nulle part.
Avec R-2 : `aucun processus des 153 groupes de la campagne, aucun descendant vivant de l'outil (moissonneur)`, 0
marque, 0 processus du cas (`sorties/exp-survie-r2.txt`, `exp-course-r2.txt`).

### Même classe : sites relevés dans les trois outils

| site | attente ou groupe | jugement |
|---|---|---|
| `mutants.py`, `jouer`, borne et sortie | descendants détachés, course, autres sessions après la sortie | **R-2** |
| `mutants.py`, `p.wait()` après le reliquat | groupe de l'enfant direct (session neuve) tué avant : bornée | sans réserve |
| `oracle_record.py`, `lancer`, `p.wait()` après le reliquat | non bornée si l'arrêt de l'arbre a échoué (Windows : `taskkill` refusé) ; simulée (`groupes` vide) : test en 31,4 s contre 17,3 s avec R-3 | **R-3** |
| `oracle_record.py`, sortie normale | descendant d'un autre groupe non suivi | limite déjà écrite (README des outils, l.62) |
| `verdict-suite-s2.py`, `lancer`, `communicate()` sans borne | V1 : descendant setsid qui garde les tuyaux 8 s : vérificateur 8,1 s ; V2 : fork setsid du leurre LE-05 : dossier du compte recréé après effacement (`sorties/exp-verif-serie.txt`) ; bornée par l'appelant (timeout-minutes, borne, délai), échec fermé | **R-4** (limites écrites) |
| `git()` (archive, rev-parse), `ps`, `taskkill` lancés par `subprocess.run` sans délai | outils système, aucun code sous test ne tient leurs tuyaux | hors classe, sans réserve (O-4) |

## 2. Remarque du générateur sur C-1 : défaut, R-1

Oui : `pas[0] is not None` reconnaît toute première étape non admise. Mesuré (`sorties/r1-rouge.txt`) : l'outil de la
série joue la campagne (sortie 0, M1 joué) quand la première étape est une étape `if: always()` / `run: exit 1` qui
ferait échouer le job sur la forge (`tete-if`), une autre action sans aucun checkout (`tete-action`), ou le checkout
avec `path: sous` (`tete-with`). R-1 exige les lignes brutes du checkout du gabarit K (`job` et `ETAPES[1]` du
vérificateur, jamais recopiés) ; vert 2 OK en 12,0 s ; sur le `gates.yml` réel, 7 jobs admis comme avant (g3 et
sim-bis avec `fetch-depth: 0`), `g5-dette` refusé comme avec la série (étape sans `shell`).

## 3. DT7-t

- Exception de la règle 3 rendue à l'octet en fin de fiche (l.168-175) : lignes ajoutées par DT7-a = retirées par
  DT7-t = ajoutées par DT7-t = fin de fiche (script ; sha256 du bloc `2ab3b6d4…`) ; titre daté l.162 (08:31:02 UTC).
- l.1 à 87 de la fiche finale égales à la tête (`cmp` ; sha256 `2c3bcdf5…`) ; fiche de 175 lignes.
- Renvois des pièces scellées : la fiche n'a pas changé depuis `c4fd0a3` (2026-10-09 17:55), antérieur aux deux pièces
  (`ba5ea95`, `0e03a9f`) ; `revue-dettes5/G2-transcrit.md` l.264 (`l.75-87`) tombe juste ;
  `revue-dettes5-codeql/G2-transcrit.md` l.625 (`l.78-89`) vise la règle d'enregistrement du rôle G2, entière aux
  l.78-87, inchangées (O-1).
- `git grep -n -I -F --untracked` sur la copie finale, pathspecs d'exclusion (casse pliée) des sept emplacements
  interdits, de `*.jsonl` et `*.jsonl/*` : `shogen-worker` 170 lignes dans 123 fichiers, `shogen-extracteur` 11 lignes
  dans 7 fichiers ; seuls renvois par numéro à une fiche : les deux pièces ci-dessus.

## 4. Items : phrases de fermeture (rapport du générateur, retouches des phases 2 et 3)

| item | sur le code de la série | phrase si les réserves sont adoptées |
|---|---|---|
| HARNAIS-CIBLE-PARTAGEE-1, règle I-1 | vraie (fiche l.94-97 ; appliquée ici : cible par défaut) | — |
| FICHE-WORKER-POSTEXEC-2 | vraie (DT7-a, C-6, DT7-t ; G0 l.18-22 relu) | — |
| WORKER-TMPDIR-1, COMPACTION-TRANSCRIPT-1, UNSHARE-LO-1 (`ip` absente de l'hôte, relu), WERROR-IGNORE-1, GARDE-EN-TETE-1, citations | vraies (fiche l.98-112, l.132-134) | — |
| PLAN-S2BIS-2-PY310-1 | vraie (fiche l.113-115 ; `scripts/plan-s2bis-2/README.md` l.32) | — |
| MUTANTS-SITE-APPEL-1 et volet | vraie (fiche l.120-124) | — |
| S2BIS-MUT-COMMANDE-1 | vraie pour la consigne ; pour l'outil, vraie sur les jobs de `gates.yml` mais fausse en général (première étape), et le classement FATAL des étapes illisibles n'a pas de cas | fermé par DT7-a, DT7-f, C-1, R-1 et R-5 |
| MUTANTS-ORPHELINS-1 | vraie à la lettre (l'outil applique `start_new_session`, `killpg`, relevé) ; fausse sur le fond (S2 à S5) | fermé par DT7-a, DT7-f, C-1 et R-2 (Linux : aucun descendant ne survit ; ailleurs, limite écrite) |
| HAIKU-ROLE-SOURCES-1 | vraie (règle 7, CLAUDE.md l.50-55, lint l.8) | — |
| ENREG-EXTRACTION-INTERDITS-1 | vraie (C-3 vert ; ADR fin ; limite à deux sauts écrite) | fermé par DT7-b, C-3, C-7 et R-6 (cible normalisée, cas `..`) |
| S2BIS-ANALYSEUR-RESIDUS-1 | vraie (`SHA256SUMS` des sondes 8 OK ; `residus` des sondes égal aux attendus S-01 à S-08) | phrase inchangée, plus : R-7, chaque fin de ligne autre que LF a son cas (S-14) |
| ENREG-DELAI-ARBRE-1 | vraie sous POSIX tant que l'arrêt de l'arbre réussit | fermé sous POSIX par DT7-d, C-2 et R-3 ; branche Windows : L-1 |
| S2BIS-LEURRE-FORK-TMP-1 | vraie pour LE-05 (F-16) ; variante setsid : dossier restant (V2) | fermé par DT7-d ; limite écrite par R-4 |
| ENREG-ANCIEN-OUTIL-1, COMPILE-LIMITES-1, DRAPEAUX-LIMITES-1, TOOLS-README-SUITE-1 | vraies (code `vieux` ; README des outils l.46, 51, 76-98) | — |
| LINT-ENVIRONNEMENTS-1, volet Git Bash | vraie (étape l.68-76 de `squelette.yml`, `defaults.run.shell: bash` l.45-47) ; fermeture à la lecture du premier run (L-2) | — |
| VERIFIER-TESTS-TMP-RESTES-1 | vraie (section 6 : 0 reste) | — |
| S2-SUITE-PY310-1 | vraie (section 6 : errata rejoué) | — |

## 5. Mutants du contre-contrôle (outil de la série, commande du job, borne 300 s)

Outil `scripts/controle/mutants.py` de la série (sha256 `3349b771…`), copie mutée `0be8e9d + a..t` ; définitions
`mutants/cc-controle.json`, `cc-s2.json` ; diffs et sorties `mutants/controle/`, `mutants/s2/` ; témoin vivant
d'abord ; relevés `aucun processus des 16 groupes` et `des 17 groupes` ; aucun reste (`ps`), `TMPDIR` vide.

| mutant | job | classement | par |
|---|---|---|---|
| CC1 descendants retirés à la borne | controle-unittest | tué | suite (M6 : `petit-enfant d'une autre session vivant après la borne`) |
| CC2 parenté sur un seul niveau | idem | tué | suite (M6, même message) |
| CC3 reliquat 120 s | idem | tué | suite (durée de la campagne ; étape en 98,9 s) |
| CC4 seconde lecture sans borne | idem | tué | suite (durée de la campagne ; étape en 98,5 s) |
| CC5 checkout en tête non exigé | idem | tué | suite (`tete`) |
| CC6 groupes des descendants non comptés au relevé | idem | vivant : **équivalent en pratique, déclaré** (chaque groupe relevé est tué par `SIGKILL` ; forme de F8) | — |
| CC7 étapes illisibles sous un mutant classées tuées | idem | **vivant, non équivalent** : R-5 | — |
| CO1 seconde lecture de `lancer` sans borne | s2-harness-unittest | tué | suite (150,3 s) |
| CO2 reliquat 40 s | idem | tué | suite (105,0 s) |
| CO3 C-3 retiré | idem | tué | suite |
| CO4 cible de lien non normalisée | idem | **vivant, non équivalent** : R-6 | — |
| CE1 `-I` exigé des seules commandes de JOBS | idem | tué | suite (`sans-I`) |
| CR1 NEL retiré de `SEPARATEURS` | idem | **vivant, non équivalent** : R-7 | — |
| CR2 alias non vu par LC-13 | idem | tué | runner (S-07, S-08, R-09) |
| CR3 clé de job répétée non refusée | idem | tué | suite (`test_ligne_du_job_forme_k_et_residus_nommes`, forme `N-12 répété`) |

Bilan : 15 mutants, 11 tués, 1 équivalent déclaré, 3 vivants. Rejoués par la commande du job sur `cb03207 + a..t +
R-1..R-7` (`mutants/survivants-*.txt`) : CC7 tué (suite), CO4 tué (suite), CR1 tué (runner). Rouges des tests des
réserves sous ces mutants : R-5 `('M11', 'tué', 0)` au lieu de FATAL ; R-6 `FileNotFoundError` ; R-7 `151 ok, 2
échec` (S-14 `U+0085 admis`, et R-09 qui rejoue le runner). Sites d'appel et étiquettes : CC2, CE1, CR1.

## 6. Rejeu sur l'état final (`5d4f2dd + a..t`, sous `isole.sh` et `env -u …`)

- **gates.yml**, chaque étape `run:` telle qu'écrite (`outils/etapes_gates.py`), g3 `--tree` et `--history` exclus :
  0 étape en échec (`sorties/gates-final.txt`) : hooks `57 ok` ; `OK: aucun marqueur de dette nu.` ;
  `runners-epingles : conforme (7 workflow(s), 22 clé(s) runs-on/os lues)` ; `workflows-yaml : conforme (7
  workflow(s), PyYAML 6.0.1)` ; `model-pinning : 227 ok, 0 échec` ; `OK (R-1) : 8 fichier(s)` ; `journaux-modele :
  conforme` ; `docs-sha256sums : conforme : 42 SHA256SUMS, 324 ligne(s)` ; secrets `147 ok` ; runner `152 ok, 0
  échec` (cinq fois) ; S2 `Ran = 423`, s2bis 371, sim-bis 279, calib-actifs 78, controle 39, tous en `--egal` ; 0
  ligne `Exception ignored` ni `Warning` ; `TMPDIR` vide.
- **Matrice** (`-X dev -W error`, `PYTHONDEVMODE=1 PYTHONWARNINGS=error`) : runner et ligne du job controle sous
  3.10.20, 3.11.15, 3.12.3, 3.13.14 ; suite S2 sous 3.11 à 3.13 : 11 codes 0, 0 ligne (`sorties/matrice-serie.txt`).
- **Errata DT7-k rejoué sous 3.10.20** : `oracle_record.py --help` 0 ; `test_oracle_record` 25 tests, 1 FAIL
  (`test_enregistrement_champs_et_sha`) ; suite S2 `Ran 423`, `FAILED (failures=77, errors=3, skipped=2)`.
- **Job `squelette`, étape Tests**, une fois, cible par défaut de la copie (aucun `CARGO_TARGET_DIR`), après
  `cargo build --locked --workspace --all-targets` (0) : sortie 0, 29 lignes `test result: ok.`, 272 passés, 0 échec ;
  `TMPDIR` 0 entrée (0 `shogen-*`), `target/tmp` 0 entrée.
- **`cargo --locked xtask verify`** (lignes VERDICT seules, `sorties/xtask-verdicts.txt`) : S-G1 à S-G8 (S-G7a) `VERT
  (0 violation(s))` ; S-G9 `ROUGE (1 violation(s))`, `docs/17-modele-de-menace.md:70` (copie creuse, attendu) ;
  `cargo fmt --check`, no_std, `cargo clippy -D warnings` : VERT ; verdict global ROUGE (attendu).
- **Série + R-1..R-7** (`cb03207`, `sorties/gates-val2.txt`, `matrice-val2.txt`) : toutes les étapes à 0, runner
  `153 ok` (cinq fois), S2 423, s2bis 374, sim-bis 279, calib 78, controle 39 ; matrice : 11 codes 0, 0 ligne. Même
  rejeu avec R-1..R-4 sur `0be8e9d` : vert.

## 7. Observations (sans réserve)

- **O-1** : `revue-dettes5-codeql/G2-transcrit.md` l.625 cite `l.78-89` d'une fiche de 87 lignes à sa date (deux
  lignes au-delà de la fin) ; avec la série, l.88-89 sont une ligne vide et le titre du bloc de DT7-a. La règle citée
  reste entière aux l.78-87 ; la pièce est scellée, et aucune forme ne garde inexistantes des lignes qu'un ajout crée.
- **O-2** : la règle 3 (l.26-28) ne renvoie pas à l'exception, désormais en fin de fiche sous un titre explicite. Un
  renvoi tiendrait en place sur la l.28, mais romprait l'égalité des l.1-87 que la forme adoptée de DT7-t garantit ; le
  lecteur qui ne voit que la règle 3 applique la règle la plus stricte.
- **O-3** : la garde de `mutants.py` retire son dossier de `sys.path` après `import os`, `import sys` (même forme que
  le vérificateur) ; la variable scellée n'est pas refusée mais jamais passée aux étapes (`ENV`) : conforme à la règle 3.
- **O-4** : `subprocess.run` sans délai pour `git`, `ps`, `taskkill` : outils système, hors de la classe visée.

## 8. Écarts

- **E-1** (12:12:44) : `git ls-files -v -- '*.jsonl'` sur la copie creuse (comptes par lettre seuls, sortie vide) :
  liste par motif, contraire à la lettre ; aucun nom affiché ; le contrôle retenu ensuite est `git sparse-checkout list`.
- **E-2** : tentative antérieure trouvée dans le dossier, déplacée dans `tentative-1/`, copies supprimées (constat
  d'entrée) ; ses notes et son `R-1.diff` lus comme signal.
- **E-3** : `SHA256SUMS` de ce dossier calculé par un parcours de ce seul dossier (exigé par le brief).
- Gates rejouées sur `5d4f2dd` (série) et `cb03207` (série et réserves), non sur `a639ba8` : aucun chemin de la série
  ni des réserves n'a changé entre `cb03207` et `a639ba8` (`git diff --stat` limité à ces chemins : vide).

## 9. Journal de provenance (G1)

- **Sources [lu]** : pièces du lot en tête ; annexe B d'ADR-0028 aux 23 lignes de l'extrait (tête `a639ba8`, script ;
  annexe de 1705 lignes) ; code et textes de la série dans la copie finale (`mutants.py` et `test_mutants.py` en
  entier, `oracle_record.py` en entier, `verdict-suite-s2.py` en entier, `gates.yml` en entier, `squelette.yml` l.45-76
  et l.122-128, fiche `shogen-worker` l.72-175, fiche `shogen-extracteur` en entier, CLAUDE.md l.22-24 et l.44-57,
  `scripts/controle/README.md` l.60-97, `s2-harness/tools/README.md` l.46-116, `s2-harness/README.md` l.12-22 et
  l'errata, fin d'ADR-0028, runner l.201, l.372-383 et l.678-702) ; `docs/adr-0029/G0-lot-PLAN-S2BIS.md` l.15-24 ;
  `scripts/plan-s2bis-2/README.md` l.28-34 ; `revue-dettes5/G2-transcrit.md` autour de l.264 ;
  `revue-dettes5-codeql/G2-transcrit.md` autour de l.625 ; `enforcement/docs-sha256sums.py` l.23-33 ; xtask
  `rapport.rs` l.85-100 et `lib.rs` l.100-103 (forme des verdicts). Doc 03 du corpus : [2nd] (par CLAUDE.md). Aucune
  source [abs] ; aucun chiffre de seconde main : chaque compte ci-dessus est lu dans une sortie de ce dossier.
- **Outils** (`outils/`) : `iso.sh`, `copie.sh`, `etapes_gates.py`, `matrice.sh`, `val2.sh`, `cargo.sh`,
  `xtask_verdicts.py`, `exp_survie.py`, `exp_verif.py`, `diff_etats.py`, `definir_mutants.py`, `poser_r1.py`,
  `poser_r2.py`, `poser_r2_tests.py`, `poser_r3.py` ; aucune barre oblique inverse dans les fichiers écrits (contrôle
  sur les octets), hors les continuations de ligne de `iso.sh` et `copie.sh`.
- **Sorties** (`sorties/`, `mutants/`) : gates (`gates-final`, `gates-val`, `gates-val2`), matrices, rouges et verts
  (`c1-*`, `c2-*`, `c3-*`, `c23-vert`, `r1-*` à `r7-*`), mesures (`exp-*`, `py310-*`), cargo (`cargo-*`), xtask
  (`xtask-verdicts.txt` ; brut `tmp/xtask-brut.txt` jamais lu), grep (`grep-shogen-*`), classements de mutants.
- **Processus** : un seul processus lourd à la fois (gates, matrices, campagnes, cargo détachés, PID consignés dans
  `NOTES.md`, fin constatée sur la sortie) ; charge sous 5 à chaque lancement (1,05 à 4,32).

Fin de la passe : voir la dernière ligne de `NOTES.md`. Aucun commit, aucun push, aucune écriture git dans le dépôt,
aucun réseau ; `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée ; copies et cible cargo supprimées ; `SHA256SUMS` écrit en
dernier.
