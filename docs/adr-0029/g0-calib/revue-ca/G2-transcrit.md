# Relecture G2 neuve de CALIB-ACTIFS (transcrit)

> Transcription par l'orchestrateur le 2026-10-09 12:17:23 UTC du fichier g2/RAPPORT-G2.md ; contrôle FM-1.1 des transcripts du générateur, du réviseur, du correcteur et du contre-contrôleur : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Relecture G2 neuve du lot CALIB-ACTIFS, série CA-0a à CA-6c (`scripts/calib-actifs/`, job `calib-actifs-unittest`)

- **Gate 0** : modèle résolu `claude-opus-5-5` (identifiant donné par l'environnement), rôle réviseur G2 neuf ; je n'ai
  écrit aucun des 19 diffs relus. Effort non vérifiable depuis la session.
- **Dates** (`date -u`) : début 2026-10-09 08:48 UTC ; contrôles de 08:49 à 09:15 ; rapport à 09:16 UTC.
- **Base** : `ebd1560` (ebd156071794…), extraite par `git --no-optional-locks archive` avec les sept exclusions du brief ;
  tête du dépôt au départ : `1a388e1` (1a388e1c548b…). Dépôt réel lu seulement ; aucune écriture git, nulle part.
- **Réseau** : toute exécution sous `g2/outils/run.sh` = `env -u HTTPS_PROXY -u HTTP_PROXY -u https_proxy -u http_proxy
  -u ALL_PROXY -u all_proxy -u NO_PROXY -u no_proxy` puis `isole.sh` (`unshare -n`). Sonde préalable (08:49) : 1.1.1.1:443
  et 8.8.8.8:53 injoignables (errno 101), `urlopen("https://example.com/")` refusé, mandataire 127.0.0.1:36573 injoignable
  dans l'espace neuf (errno 111). Aucune requête réseau de ma part.

## Verdict : **ACCEPTE-AVEC-CORRECTIONS** (liste fermée C-1 à C-12 ci-dessous)

Le code est juste sur tout ce que j'ai pu confronter à une référence indépendante (sonde écrite d'après le contrat avant
toute lecture du code : 0 écart ; croisement de Q-CA-13 : 44 153 comparaisons, 0 écart) ; les 19 diffs sont verts au
plancher exact, la matrice 3.10 à 3.13 en `-X dev -W error` est verte, runner, s2bis et S2 sont verts, `xtask` ne change
aucun verdict. Les corrections portent sur la **force des tests** (14 de mes 30 mutants vivent, dont des mutants de
source et de site d'appel sur des règles scellées : dénominateur de τ_agr, maximum des strates du troisième terme), sur
la **garde mandataire** (le test qui vérifie le remède d'E-CA3-1 ne tue son mutant que si l'environnement porte un
mandataire), sur la **portabilité du job CI** (test d'identité qui exige quatre interpréteurs absents de l'image
déclarée) et sur le relevé de cadence (exception non captée).

## 1. Contrat lu, puis sonde écrite avant le code

Lu [lu] : `BRIEF-CA.md` (en entier) ; `G0-CALIB-ACTIFS.md` et son ajout daté (22:42:53, INV-1 = A) ; `PROPOSITION.md`
l.1-830 ; `AVIS.md` (en entier, prime : Q-CA-11 et Q-CA-15 modifiées, précisions Q-CA-02, -04, -06, -07, -13) ;
`PAIRES-ET-TEMOIN.md` (en entier) ; `SOURCES-HISTORIQUES.md` (en entier) ; ADR-0029 l.177-192, l.212, l.403 et l.405
(ajouts datés du 2026-10-08) ; `s2-harness/shogen_s2/r1.py` l.100-112 (médiane : moyenne des deux du milieu) ;
`scripts/plan-s2bis/regles.py` l.1-40, `tau_sigma.py` l.55-130, `commun.py` l.1-57 et l.163-199 (forme du bloc machine) ;
`s2bis/tests/__init__.py` à la tête. Non ouverts : `tau_sigma.txt`, tout `*.jsonl`, les dossiers interdits, les pièces de
D.2 ; sortie brute de `xtask` jamais lue (lignes VERDICT et un compte de motif).

Sonde `g2/outils/sonde_ref.py` (écrite à 08:49, avant toute lecture du code ; auto-test vert) : grid-ceil en Fraction
(pas 0,0005, borne basse 0,0005 avec drapeau, borne haute 0,0285 exclue en refus) ; rang ⌈num·N/den⌉ ; τ_agr au
**maximum** des deux classes de places de BTC ; troisième terme = P99 des **âges par cellule**, × 3 × 60 s, grid-ceil
60 s, maximum des strates ; médiane leave-one-out (paire : moyenne des deux du milieu) ; exclusion stricte 60·âge > σ ;
fenêtre (131 040 minutes ; 37 440 / 93 600) ; vecteurs de Q-CA-13 dont les deux de l'avis : 1,5 × 1/3000 = 0,0005 sans
drapeau ; 1/3 % donne 0,0050 sous le facteur 1,5 et 0,0035 sous le facteur 1. Liaison au lot (`sonde_lot.py`, fixture où
chaque paramètre de BTC sous étiquette diffère de toute source concurrente : τ_ph 0,0060 > τ_sh 0,0040, τ_agr 0,0265 ≠
τ_oracle 0,0270, σ_agr 450,2 et σ_ph 75,5 non entiers) : 3 010 règles, 1 500 quantiles, τ_agr dans les deux sens
(ph > sh, ph < sh, égalité) avec CA/borne, 200 grilles aléatoires de population (N_min, exclusion, médiane), 100
troisièmes termes aléatoires, strates heure par heure sur la fenêtre ± 3 jours, dernier prix et âges, σ par classe, mode
`planchers_seuls`, refus CA/variable, CA/mediane, CA/population, CA/borne (0,0285 refusé, 0,0280 admis), CA/format
(double, borne haute), bloc machine écrit avec les f-strings de `tau_sigma.py` : **SONDE-LOT OK**. La même sonde tue
mes mutants G01 (5 écarts) et G14 (42 écarts), que la suite du lot laisse vivre.

## 2. Pièces du générateur

`sha256sum -c SHA256SUMS` du dossier : **129/129 OK** (couvre BRIEF, NOTES, RAPPORT-GENERATEUR, 19 diffs, outils,
travail). `RAPPORT-GENERATEUR.md` lu comme une donnée. Série appliquée dans l'ordre du rapport sur `ebd1560` (`git
apply`) : 19/19, **2 977 lignes ajoutées** (recompté par `--numstat`), au plus 200 par diff (CA-0a : 200 exactement) ;
chemins : `scripts/calib-actifs/**` et `.github/workflows/gates.yml` seuls ; état final égal à l'octet à
`travail/snap/CA-6c` ; `SHA256SUMS` du lot : 29 entrées, `sha256sum --strict -c` sans écart, liste = fichiers du
dossier, sha256 `a9967de0…b778`. sha256 des diffs recalculés : égaux au `SHA256SUMS` ; **le tableau du rapport porte
une coquille** pour CA-5e (`…7c7d` écrit, `…7f7d` réel : `cf3baa70075f…983c7f7d`).

Relu en entier : les 30 fichiers de l'état final (1 371 lignes hors tests, 1 606 de tests) et les lignes
intermédiaires de chaque diff (lignes ajoutées puis retirées, listées par `g2/outils/intermediaires.py` : docstrings,
schéma, `lire_url`, serveur de test, intervalles de Binance et d'OKX, en-tête du lanceur sans TMPDIR) : rien qui ne soit
repris ou corrigé plus loin.

## 3. Contrôles

### 3.1 Vert et plancher à chaque diff (`g2/outils/par_diff.sh`, ligne du job telle qu'écrite, isolée)

| diff | plancher | Ran | code | | diff | plancher | Ran | code |
|---|---|---|---|---|---|---|---|---|
| CA-0a | 3 | 3 | 0 | | CA-4b | 37 | 37 | 0 |
| CA-0b | 6 | 6 | 0 | | CA-5a | 40 | 40 | 0 |
| CA-0c | 9 | 9 | 0 | | CA-5b | 44 | 44 | 0 |
| CA-1a | 11 | 11 | 0 | | CA-5c | 47 | 47 | 0 |
| CA-1b | 14 | 14 | 0 | | CA-5d | 49 | 49 | 0 |
| CA-1c | 16 | 16 | 0 | | CA-5e | 52 | 52 | 0 |
| CA-2a | 20 | 20 | 0 | | CA-6a | 56 | 56 | 0 |
| CA-3a | 24 | 24 | 0 | | CA-6b | 58 | 58 | 0 |
| CA-3b | 28 | 28 | 0 | | CA-6c | 59 | 59 | 0 |
| CA-4a | 33 | 33 | 0 | | | | | |

### 3.2 Matrice et batteries (état final, isolé)

| contrôle | base + série | tête `1a388e1` + série résolue |
|---|---|---|
| job `calib-actifs-unittest` sous python3.10, 3.11, 3.12, 3.13, `-X dev -W error`, `PYTHONDEVMODE=1`, `PYTHONWARNINGS=error` | 4 × code 0, Ran = 59, 0 « Exception ignored », 0 « Warning » | idem (4 × Ran = 59) |
| runner `enforcement/tests/run-fixtures-verdict-suite-s2.py` | 136 ok, 0 échec | 136 ok, 0 échec |
| job s2bis | conforme, Ran = 255 | conforme, Ran = 340 |
| job S2 (`verdict-suite-s2.py --egal`) | conforme, Ran = 415, sauts nommant la variable | idem |
| `cargo --locked --offline xtask verify` (lignes VERDICT seules) | 10 lignes **identiques à la base** ; 1 ROUGE, la 9e (S-G9 par l'ordre), motif `docs/17-modele-de-menace.md:70` une fois dans chaque sortie (connu sur copie) ; la 5e (S-G5) VERTE | identiques |
| sim-bis, plan-s2bis | non lancés (extraction de `f35a70c`) ; aucun de leurs fichiers ni de leurs entrées touché (chemins des 19 diffs) | — |

Forme : 0 octet 92 dans les 30 fichiers ; aucune ligne de plus de 120 caractères ; aucun `TODO`, `FIXME`, `XXX` (R-13) ;
R-25 tenu (≤ 200 lignes ajoutées par diff, tout compris). Entrées du lot inchangées de `ebd1560` à `1a388e1`
(`config_analyse.py`, `analyse.json`, `scripts/plan-s2bis`, `tau_sigma.txt`, SH, vérificateur, runner : `git diff
--stat` vide).

Répétition (E-CA-26), refaite avec l'outil du générateur sur le code final : bruts synthétiques 102 227 907 octets ;
`tau.py` code 0, **80,7 s murales, 838 468 Kio** (générateur : 86,1 s, 838 600 Kio) ; `fragment_analyse.json`
`ba896086…3ccc`, égal à celui du générateur ; `calib_actifs.txt` diffère par sa ligne d'en-tête de sha256 (chemins du
dossier de travail dans le `parametres.json` de l'outil [inféré]). Bruts supprimés.

### 3.3 Application sur la tête actuelle (`1a388e1`)

Conflit confirmé, **un seul hunk** : `gates.yml` de CA-0a, dont la ligne de contexte est la dernière ligne du job
`sim-bis-unittest` (`--plancher 194` à `ebd1560`, `--plancher 210` à la tête ; la tête a aussi deux lignes de
commentaire SB-13 et `s2bis` à 340). **Résolution exacte** : dans le hunk `gates.yml` de CA-0a, remplacer la seule ligne
de contexte

`           python3 -B enforcement/verdict-suite-s2.py scripts/sim-bis --aucun-saut --egal --plancher 194`

par la même ligne en `--plancher 210` (fichier `g2/travail/CA-0a-tete.diff`, une ligne changée) ; tout le reste de la
série s'applique alors sans retouche (hunks `gates.yml` de CA-0a à CA-6c : décalage de 2 lignes, à 247 puis 266). État
obtenu : lot égal à l'octet à la série sur `ebd1560` ; `gates.yml` égal à celui de la tête plus le job neuf
(`--plancher 59`). Batteries de la tête : tableau 3.2.

### 3.4 Garde réseau (remède d'E-CA3-1)

`tests/__init__.py` retire à l'import `http_proxy`, `https_proxy`, `all_proxy` (toutes casses) de `os.environ`, donc
des sous-processus, puis pose la garde (boucle locale seule). Exactitude : `urllib` ne lit que les variables
`<schéma>_proxy` ; pour des URL http et https, les seules qui comptent sont retirées ; les autres variables de
l'environnement (`GLOBAL_AGENT_HTTPS_PROXY`, `npm_config_https_proxy`…) donnent des schémas sans effet. La garde est
juste. **Mais** `test_garde_reseau` vérifie la purge en lisant l'environnement courant : sans mandataire (CI, ou sous
`env -u` comme l'impose ce brief), le mutant « purge retirée » (G11) **vit** ; il n'est tué qu'avec un `HTTPS_PROXY`
fictif posé (rejoué dans l'espace isolé : TUE). Le test du remède dépend donc de l'environnement : C-3. Autre reste :
`test_cadence.test_cli_hors_lanceur` passe la variable avec les **vrais** paramètres (sans `--parametres`) ; sous un
mutant qui retire la garde de `cadence.main`, seule la garde réseau en processus empêche un appel réel (même forme que
la cause d'E-CA3-1) : C-3.

### 3.5 Tableau E-CA-01 à E-CA-33 du générateur, vérifié ligne à ligne

Conforme, renvois `fichier:ligne` exacts, sauf : **E-CA-04** `socle.py:17` (ETIQUETTE est l.19 ; l.17 = PARAMETRES) ;
**E-CA-12** « source citée par bloc » : la pièce de SH est citée par bloc (`series.source`), non par (place, paire)
comme l'écrit E-CA-12 (O-11) ; **E-CA-15** tenue mais son test d'attache aux comptes de SH ne lie pas compte et place
(G29, G30 vivants : C-6) ; **E-CA-19** « nul » annoncé par la docstring de `agregateurs` non testé (G13 : C-9) ;
**E-CA-21** tenue sur cet hôte, non portable à l'image du job (C-4) ; **E-CA-26** remesurée (§3.2) ; **E-CA-33**
plan-s2bis et sim-bis non lancés, inchangés par construction (chemins). T-CA-* du §6.2 : tous présents (SOC-1, SOC-2,
FEN-1, FMT-1 à 3, SER-1, TAU-1 à 3, Q-1, G-1 avec les deux vecteurs de l'avis, AGR-1, ORA-1, SIG-1 à 3, ORX-1, KRA-1,
FRG-1 côté lot, DET-1, LAN-1 à 6). M-CA-01 à M-CA-29 : 31 lignes TUE dans les tsv du générateur (253 mutants, 251 TUE,
2 VIVANT déclarés équivalents : CA6b-02, CA6c-05, avis : équivalents admis). Rouge : par squelette (E-CA3-5) ; sur les 19
rouges, une part d'ERROR (TypeError sur `None`) plutôt que d'assertion (ex. CA-5a : 8 FAIL, 29 ERROR) (O-12).

## 4. Mutants du réviseur (30, `g2/outils/mutants_g2.py`)

Classement par la commande exacte du job (`python3 -B enforcement/verdict-suite-s2.py scripts/calib-actifs --aucun-saut
--egal --plancher 59`, racine jetable), borne 300 s, PAR = 2, groupe de processus tué au dépassement, sous `run.sh`.
Sortie 1 TUE, 0 VIVANT, autre FATAL. Témoin G00 (aucun changement) : VIVANT. Motifs contrôlés sur les octets (compte = 1,
sinon INVALIDE : G30 relancé une fois après un motif à 0). **Bilan : 16 TUE, 14 VIVANT, 0 FATAL.**

| id | objet (SITE = site d'appel, SOURCE = source sous étiquette inchangée) | état | tué par |
|---|---|---|---|
| G01 | SOURCE dénominateur de τ_agr = classe sans_horodatage de BTC | **VIVANT** | — (C-1) |
| G02 | SOURCE dénominateur = classe horodatée | TUE | test_agregateurs, test_planchers_seuls |
| G03 | SOURCE σ_BTC lu sous la classe agregateur | TUE | test_classe_sans_derniere_transaction |
| G04 | SITE population du 3e terme = places horodatées (Q-CA-07 a) | TUE | test_corps_et_septembre |
| G05 | SITE mode ignoré au calcul | TUE | test_planchers_seuls, test_affiche_et_planchers_seuls |
| G06 | SOURCE exclusion au σ des agrégateurs | TUE | test_site_exclusion |
| G07 | SOURCE semaine de l'oracle de SH = fenêtre principale | **VIVANT** | — (C-5) |
| G08 | SOURCE fenêtre descriptive acquise sur les bornes de la principale | **VIVANT** | — (C-7) |
| G09 | SOURCE volume d'OKX lu dans `vol_ccy` | TUE | test_colonnes, test_aller_retour, test_succes |
| G10 | SOURCE médiane de BTC de l'autre agrégateur (cadence) | **VIVANT** | — (C-10) |
| G11 | purge des variables de mandataire retirée | **VIVANT** (TUE avec HTTPS_PROXY fictif) | — (C-3) |
| G12 | CA/chainlink : contrôle du seuil retiré | **VIVANT** | — (C-9) |
| G13 | CA/btc : τ de BTC nul admis | **VIVANT** | — (C-9) |
| G14 | 3e terme : première strate au lieu du maximum des strates | **VIVANT** | — (C-2) |
| G15 | τ des places : strate calme seule | TUE | test_places |
| G16 | τ des places : strate de stress seule | TUE | test_places |
| G17 | SOURCE strates de la fenêtre principale pour toute fenêtre | TUE | 6 tests (ERROR) |
| G18 | exclusion à l'égalité (≥) | TUE | test_exclusion |
| G19 | N_min décalé | TUE | test_n_min et 3 autres |
| G20 | SOURCE plancher de 30 s pour les agrégateurs | TUE | test_classes |
| G21 | oracle de SH : compte à 2 places non contrôlé | TUE | test_oracle |
| G22 | passe B sous la graine de A (lanceur) | TUE | test_acquisition_et_identite |
| G23 | SITE τ_agr calculé sur la valeur de la règle (avant borne basse) | **VIVANT** | — (C-8) |
| G24 | reprise : manifeste existant ignoré | TUE | 5 tests d'acquisition |
| G25 | SITE épingle de tau_sigma non appelée au calcul | TUE | test_refus |
| G26 | SOURCE strates codées en dur (5, 6) | **VIVANT** (équivalent sous les paramètres scellés) | — (O-10) |
| G27 | SOURCE N_min codé en dur (4) | **VIVANT** (équivalent sous la lecture A) | — (C-11) |
| G28 | cadence : AttributeError non comptée | **VIVANT** | — (C-10) |
| G29 | SOURCE comptes de SH §4 permutés entre places dans parametres.json | **VIVANT** | — (C-6) |
| G30 | SOURCE compte de kraken remplacé par celui de binance | **VIVANT** | — (C-6) |

Les vivants n'invalident aucune valeur sous la lecture A et les paramètres actuels (sonde : 0 écart) ; G07, G29, G30
échoueraient fermés au lancement (CA/oracle-sh) ; G01, G14, G23 changeraient une valeur scellée sans qu'aucun test ne
rougisse.

## 5. Corrections (liste fermée ; chacune avec la preuve qui la fermera)

- **C-1** (moyenne ; Q-CA-06, ajout daté l.403 (2)) : vecteur de T-CA-AGR-1 avec τ_ph > τ_sh (par ex. 0,0050 et 0,0045 :
  dénominateur 0,0050, produit 0,0053, τ_agr 0,0055 ; sous la seule classe sans horodatage : 0,005888…, 0,0060), et une
  fixture de pipeline (`synthetiques.BTC` ou `banc`) où τ_ph > τ_sh. Preuve : G01 TUE, G02 et M-CA-15 toujours TUE.
- **C-2** (moyenne ; l.189 « maximum sur les deux strates ») : test du troisième terme avec les deux strates non vides,
  P99 de stress > P99 de calme (et l'inverse). Preuve : G14 TUE.
- **C-3** (moyenne ; remède d'E-CA3-1) : test de la purge indépendant de l'environnement (sous-processus qui pose
  `HTTPS_PROXY`, `https_proxy`, `HTTP_PROXY`, `ALL_PROXY` à une valeur fictive sur la boucle locale, importe `tests`
  et exige `urllib.request.getproxies()` sans clé http, https ni all) ; et cas « variable posée » de
  `test_cadence.test_cli_hors_lanceur` avec des paramètres locaux, comme `test_pages.test_main`. Preuve : G11 TUE sous
  `env -u …` (sans mandataire), et un mutant « garde de `cadence.main` retirée » TUE sans tentative vers un hôte réel
  (`tests.TENTATIVES` vide).
- **C-4** (moyenne ; job CI) : `test_identite` exige `python3.10` à `python3.13` sur PATH ; le job tourne sur
  `ubuntu-24.04`, « interpréteur de l'image, sans setup-python » ; sous un PATH sans ces interpréteurs, la suite rougit
  (mesuré : `AssertionError: None unexpectedly found in [None, None, None, None]`, verdict « code de sortie 1 ») ; que
  l'image n'en porte qu'un est [inféré]. Correction : identité sous `sys.executable` × {0, 1}, plus chaque `python3.1x`
  présent ; la matrice 3.10 à 3.13 reste une étape écrite du G3 opérant et de la G2. Preuve : suite verte sous le PATH
  simulé (liens vers `/usr/local/bin`, `/usr/bin`, `/bin` sans `python3.10` à `python3.13`, `python3` vers 3.12 ;
  recette dans `g2/NOTES.md`), M-CA-23 toujours TUE.
- **C-5** (faible ; E-CA-15) : test où la semaine de l'oracle est une sous-fenêtre stricte de la fenêtre principale, avec
  des minutes actives hors de la semaine. Preuve : G07 TUE.
- **C-6** (faible ; E-CA-15) : `test_comptes_de_sh` lie chaque compte de `oracle_sh` à sa place et à sa colonne (ligne
  du tableau de SH §4 et phrase « Minutes actives par place »), non à sa seule présence sur l.103-111. Preuve : G29, G30
  TUE.
- **C-7** (faible ; E-CA-13) : `test_pages.test_main` vérifie les bornes des pages de la fenêtre descriptive (URL ou
  noms `page-<début>`). Preuve : G08 TUE.
- **C-8** (faible ; §4.4 : τ_agr sur τ_places) : test de `calcul_actif` où τ des places tombe sous la borne basse
  (drapeau) : τ_agr calculé sur 0,0005, non sur la valeur de la règle. Preuve : G23 TUE.
- **C-9** (faible ; E-CA-10, E-CA-19) : tests d'un seuil Chainlink différent (CA/chainlink) et d'un τ de BTC nul
  (CA/btc, comme l'annonce la docstring). Preuve : G12 et G13 TUE.
- **C-10** (faible ; Q-CA-11) : `cadence.releve` ne capte pas `TypeError` : un corps DefiLlama `[]` ou `"x"` lève une
  trace et perd le relevé de deux heures (mesuré : `TypeError NON CAPTEE` ; `{"coins": []}` est capté) ; capter
  `TypeError`, tester des corps `[]` pour les deux agrégateurs, et une fixture où BTC diffère d'un agrégateur à l'autre.
  Preuve : test rouge avant (TypeError), vert après ; G28 et G10 TUE.
- **C-11** (faible ; Q-CA-15, variante A-prime) : un test de `calcul_actif` sous `lecture = "A-prime"` (N_min 3 pour
  USDC). Preuve : G27 TUE.
- **C-12** (forme, rapport du générateur, G1) : sha256 abrégé de CA-5e (`…7f7d`) et renvoi `socle.py:19` pour
  l'étiquette. Preuve : `sha256sum diffs/CA-5e.diff` ; `sed -n 19p socle.py`.

Chaque correction se fait dans un diff de la série (ou un diff CA-6d), plancher recalé, campagne relancée sur les
mutants nommés.

## 6. Constats O-n (hors liste ; décision ou mémoire de l'orchestrateur)

- **O-1** (moyenne, décision) Q-CA3-5 : sous CA/borne, aucune valeur n'est imprimée ; or la décision attendue (l.183 ;
  PROPOSITION §4.3 pt 3 renvoie à `regles.py`, qui la porte) en a besoin : un CA/borne au lancement unique forcerait un
  second lancement (déviation déclarée) pour la connaître. Avis : imprimer la valeur de la règle sur une ligne de
  `calib_actifs.txt` (le refus lui-même restant sans valeur, §5.7), à trancher avant l'épinglage.
- **O-2** (moyenne, à écrire pour RB-2 et le paquet) Q-CA3-4 : σ_BTC arrondi à la seconde supérieure ; E-CA-23 (e)
  exige σ_agr(actif) = σ_agr(BTC) : le σ de BTC versé dans `analyse.json` doit être arrondi de même, sinon (e) refuse.
- **O-3** (faible) Q-CA3-13 : la lettre de §4.3 pt 1 (« 3 pour F3 quand la classe n'a que 3 places ») vaut aussi pour
  USDC en septembre sans kraken : N_min = 3 y donnerait une valeur descriptive au lieu d'un refus ; sans effet décisif.
- **O-4** (faible) en mode `planchers_seuls`, `corps` imprime « troisième terme N s » alors que σ l'écarte : ajouter
  « (écarté) ».
- **O-5** (faible) `lancer.sh` rend toute sortie non nulle d'`acquerir.py` en « CA/acquisition », code 4, y compris
  CA/parametres et CA/variable (code 3 d'`acquerir`) ; le nom exact reste dans `lancer.log`.
- **O-6** (faible) `calib_actifs.txt` porte le sha256 de `manifeste.tsv`, daté : un tiers qui retélécharge obtient une
  autre ligne d'en-tête ; un condensé des seules colonnes URL, taille, sha256 serait recalculable.
- **O-7** (faible, garde E-CA3-1) Q-CA3-8 : sens inclus ou exclu de `end` (Coinbase, Bitstamp, Bitfinex) non établi ; une
  fin exclue perdrait une minute par page, lue « sans échange », sans refus (pour Coinbase, 1 sur 300) ; l'oracle de SH
  le verrait probablement pour ETH et USDT (Coinbase dans les concurrences), pas sûrement pour Bitfinex. Mensuels d'OKX en
  UTC+8 : échec fermé (CA/format, temps hors fenêtre).
- **O-8** (faible) Q-CA3-2 et Q-CA3-3 : au paquet, la clé `etiquette` est retirée et `modes` entre au schéma de RB-2
  (E-CA-23 b), qui ne le connaît pas encore.
- **O-9** (forme) états intermédiaires CA-2a à CA-6b : `acquerir.py`, `bougies.py`, `socle.py`, `tau.py`,
  `tests/synthetiques.py` finissent par une ligne vide (git : « new blank line at EOF »), corrigé en CA-6c ; le hook n'a
  pas de règle d'espaces : sans effet bloquant.
- **O-10** (faible) G26 : strates codées en dur équivalentes aux paramètres scellés (calendrier de S2) ; mutant
  équivalent admis.
- **O-11** (faible) E-CA-12 : pièce de SH citée par bloc de `series`, non par (place, paire).
- **O-12** (forme) rouge par squelette (E-CA3-5) : rouge montré, en partie par ERROR et non par assertion.
- **O-13** (faible) Q-CA3-16 : `test_comptes_de_sh` lit les lignes 103 à 111 de SH par position : un ajout au-dessus
  casse le test (fragile, fermé).

## 7. Avis sur les questions Q-CA3-1 à Q-CA3-17

1. **Taille** : lecture stricte (200 lignes tout compris) conforme à R-25 et au §6.1 ; 19 diffs admis.
2. **Champ de mode** : clé `modes` au premier niveau, conforme à Q-CA-15 modifiée ; à porter au schéma de RB-2 (O-8).
3. **Étiquette JSON** : clé `etiquette`, première des clés triées (aussi dans le cas de refus) : admis (O-8).
4. **σ_BTC non entier** : arrondi supérieur admis (σ ≥ σ_BTC, Q-RBc-1) ; condition pour (e) de RB-2 (O-2).
5. **CA/borne sans valeur** : à trancher ; avis : imprimer la valeur hors de la ligne de refus (O-1).
6. **Refus ajoutés** : serrage admis (CA/parametres, CA/fragment, CA/calcul, CA/usage des scripts) ; nom perdu à
   l'écran du lanceur (O-5).
7. **CA/chainlink** : admis comme contrôle de cohérence ; sa moitié τ n'est pas testée (C-9) ; la relecture datée reste
   au paquet (E-CA-10).
8. **Formes d'API** : constat juste ; à établir avant l'épinglage, condition de l'épinglage (O-7, item ci-dessous).
9. **Kraken par nom de base, unique** : admis ; échec fermé dans les deux sens ; ne dépend pas de l'écart E-CA3-1.
10. **Réseau du lanceur** : admis ; testé (`test_succes`) ; `SSL_CERT_FILE` présent sur l'hôte de session, donc gardé.
11. **CI** : patron appliqué (vérificateur, `--plancher` exact, aucun saut) ; **une exception** : interpréteurs de
   `test_identite` (C-4) ; aucun cas K ne lit le job (item CI-CABLAGE-CALIB-1) ; sim-bis et plan-s2bis inchangés par
   construction.
12. **Exclusion de Q-CA-04** : constat juste (σ ≥ 3 × 60 × P99 des âges de la population, donc seules des cellules d'âge
   > 3 × P99 sortent) ; limite à écrire au paquet.
13. **Septembre** : refus imprimé admis (descriptif) ; la lettre permettrait N_min = 3 (O-3).
14. **Strate d'une suite** : admis (descriptif).
15. **Réimplémentation dans `socle.py`** : admise ; croisée par moi contre `regles.py` (§1, 0 écart, contexte de r1
   sans effet).
16. **Dépendance des tests à SH et `config_analyse`** : admise (lecture seule) ; fragilité de position (O-13).
17. **README des sorties au versement ; manifeste daté** : admis (E-CA-13 exige la date) ; O-6.

## 8. Écarts du générateur

- **E-CA3-1 (grave)** : faits [2nd, rapport] : téléchargements réels (1 057 lignes de manifeste dont 12 locales, 118 905 568 octets : sommes recomptées sur les chiffres du rapport) avant tout
  épinglage, par un mutant, plus un orphelin jusqu'à 07:29 ; aucun fichier ouvert, aucune statistique (E-CA-25 non
  atteint d'après le rapport). Contrôlé par moi : aucun reste `ca_acq_*` dans `calib3/tmp` ni dans `/tmp`, aucun
  processus survivant. **Les deux lignes kraken du manifeste** : le lot **n'en dépend pas** : `kraken_sha256` vient de
  SH l.156-158, relu par `test_kraken_sommes_de_sh` ; CA/kraken échoue fermé au lancement ; Q-CA3-9 ne s'appuie sur
  aucune structure observée ; aucun fichier du lot ne cite l'observation. Elle ne doit servir de preuve à rien (ni de
  la stabilité de l'archive, ni de l'égalité des sommes) ; seul le contrôle CA/kraken du lancement unique fera foi ; à
  ne verser dans aucune pièce comme constat. Le remède est juste mais son test est incomplet (C-3). Les requêtes non
  bornées vers Coinbase depuis l'adresse de session restent un fait à consigner (limites lues : 3 par seconde).
- **E-CA3-2** (barres obliques tapées) : 0 octet 92 recompté dans les 30 fichiers ; motifs des mutants contrôlés par
  compte : admis.
- **E-CA3-3** (`git init`, `git add` dans des copies jetables) : hors dépôt réel ; admis, déclaré. Je n'en ai pas eu
  besoin (`xtask` ne lit pas git).
- **E-CA3-4** (premières campagnes non isolées) : plausible, aucune URL réelle n'est atteignable par les tests avant
  CA-2a (`local()` remplace les URL de Binance, d'OKX et de Kraken) ; admis.
- **E-CA3-5** (rouge par squelette) : admis (O-12).
- **E-CA3-6** (retouches sans relance) : couvert par mon rejeu vert à chaque diff et mes mutants sur l'état final.
- **E-CA3-7** (sim-bis, plan-s2bis non lancés) : admis par l'argument des chemins.

## 9. Items proposés

- **SHOGEN-TESTS-GARDE-MANDATAIRE-1** : à former ; constaté aussi à la tête dans `s2bis/tests/__init__.py` (garde sans
  purge) ; construction élargie : purge **et** test indépendant de l'environnement (forme de C-3) ; déclencheur : prochain
  lot touchant `s2bis/tests`, et tout paquet de tests à garde réseau.
- **SHOGEN-MUTANTS-ORPHELINS-1** : à former ; construction : `start_new_session` et `killpg` (fait dans mon outil et
  dans celui du générateur) ; ajouter un relevé `ps` de fin de campagne aux gabarits.
- **SHOGEN-CALIB-FORMES-API-1** : à former, **condition de l'épinglage** (E-CA-27) : sens de `end` et de `limit` par page
  citée ou capture (horodatages seuls), alignement des mensuels d'OKX ; O-7.
- **SHOGEN-CI-CABLAGE-CALIB-1** : à former ; cas K du runner pour le job neuf, et interpréteurs de l'image (C-4 s'il
  n'est pas corrigé dans la série).
- **SHOGEN-S2BIS-P1-ESTIMATION-1** : chiffre mesuré confirmé : 2 977 lignes ajoutées (recompté).

## 10. Provenance (G1)

Commandes et sorties : `g2/NOTES.md` (journal horodaté) ; `g2/travail/par_diff.log` et `par_diff_*.out` ;
`matrice.log` et `matrice_*` ; `batterie.log` et `batterie_*` ; `mutants_g2*.tsv` et `.log` ; `path_runner.out` ;
`xtask.log`, `xtask-*-verdicts.txt` ; `repetition_g2.out` ; `CA-0a-tete.diff`. Outils : `g2/outils/` (run.sh,
sonde_reseau.py, sonde_ref.py, sonde_lot.py, croise_g2.py, intermediaires.py, par_diff.sh, matrice.sh, batterie.sh,
mutants_g2.py, xtask.sh). Processus lourds, un à la fois, PID consignés dans NOTES (23838 rejeu, 26055 mutants, 482
matrice, 6821 batteries, 14494 xtask, 15708 répétition) ; fin constatée ; aucun processus de moi ne reste (`ps` à la
fin). Copies (base, série, tête, rejeu) et TMPDIR (`g2/tmp` : cible cargo, PATH simulé, sorties brutes de xtask)
supprimés à la fin. **Écart E-G2-1** (B.16, barres obliques inverses) : j'en ai tapé dans quelques commandes et
gabarits : continuations de ligne de `run.sh` (2 octets 92) et de `matrice.sh` (1), `$` échappés des boucles d'attente,
un motif `grep` d'un contrôle de fin de fichier (sortie non retenue, contrôle refait en Python par `bytes([10, 10])`) ;
contrôle sur les effets : `run.sh` retire bien le mandataire (sonde), la matrice a tourné en `-X dev -W error` (4 × 2
sorties), les attentes ont rendu. `mutants_g2.py` porte 150 octets 92 (guillemets échappés en Python, écrits par
l'outil d'écriture) : chaque motif est contrôlé par compte exact sur les octets du fichier cible (compte = 1). `SHOGEN_S2_CAMPAGNE_CONTROL`
jamais posée. Aucune clé, aucun secret. Rien sur Pocket.
