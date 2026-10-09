# Contre-contrôle de CALIB-ACTIFS (CONFORME après CA-6e) (transcrit)

> Transcription par l'orchestrateur le 2026-10-09 12:17:23 UTC du fichier g2/cc/RAPPORT-CC.md ; contrôle FM-1.1 des transcripts du générateur, du réviseur, du correcteur et du contre-contrôleur : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Contre-contrôle des corrections de la G2 de CALIB-ACTIFS (CA-0a … CA-6c, plus CA-6d)

- **Gate 0** : modèle résolu `claude-opus-5-5` (identifiant donné par l'environnement). Rôle : contre-contrôleur neuf.
  Je n'ai écrit ni la série, ni la G2, ni les corrections, et je n'ai rien corrigé. L'effort n'est pas vérifiable depuis
  la session.
- **Dates** (`date -u`) : début le 2026-10-09 à 09:59 UTC, contrôles de 09:59 à 10:17, rapport à 10:17 UTC.
- **Base** : `ebd1560` (ebd156071794…). **Tête du dépôt** : `1a388e1` (1a388e1c548b…), inchangée pendant tout le
  contrôle. Les deux viennent de `git --no-optional-locks archive` avec les sept exclusions du brief. Le dépôt réel a été
  lu seulement, sans aucune écriture git. Mes écritures sont toutes sous `g2/cc/`.
- **Réseau** : toute exécution est passée par `g2/cc/outils/run.sh`. C'est une copie de `g2/outils/run.sh` : `env -u`
  sur les huit variables de mandataire, `isole.sh` (`unshare -n`), puis TMPDIR `g2/cc/tmp`.
  Sonde préalable à 09:59, sous `run.sh` :
  - 1.1.1.1:443 et 8.8.8.8:53 injoignables (errno 101) ;
  - `urlopen` refusé (URLError) ;
  - mandataire 127.0.0.1:36573 injoignable (errno 111).

  Hors isolement, ce même mandataire répond, donc la sonde discrimine bien. Je n'ai fait aucune requête réseau.

## Verdict : **CONFORME-AVEC-RÉSERVES** (liste fermée R-1, R-2)

Les treize corrections sont faites comme la G2 et l'adjudication les demandent, et chacune est prouvée par son mutant :
- les 13 vivants visés sont tués, toujours par un FAIL d'assertion du test neuf ou changé ;
- G26 vit, ce qui est attendu (mutant équivalent) ;
- CA-6d ne touche que le périmètre de C-1 à C-13 ;
- CA-0a … CA-6c sont inchangés à l'octet ;
- toutes les gates sont vertes, au plancher exact.

Les réserves portent sur le rapport (lignes d'items) et sur un mutant neuf qui vit. Aucune ne porte sur une valeur
calculée.

- **R-1** (forme, lignes d'items du §11.4, G1) :
  - (a) Ne pas former **SHOGEN-S2BIS-RB2-SCHEMA-MODES-1**. Un item de RB-2 porte déjà le volet :
    **SHOGEN-S2BIS-CALIB-L189-1**, « précisé » à l'annexe B l.1267 (« E-CA-23 écrits, avec le champ de mode ; RB-2 et
    lot CA ») et listé l.1086. Le constat O-8 (clé `etiquette` retirée, `modes` au schéma) doit devenir un volet de
    CALIB-L189-1. C'est la condition même de l'ajout daté de l'adjudication (« si aucun item de RB-2 ne porte déjà le
    volet »). Le correcteur avait écrit « je ne l'ai pas cherché ».
  - (b) **SIGMA-ARRONDI-1** cite « `tau.py` l.134 » : c'est la numérotation de CA-6c. Dans l'état qui sera commis (après
    CA-6d), le contrôle (e) est à `tau.py` l.136. `sigma.py` l.64 est exact.
  - (c) **TESTS-GARDE-MANDATAIRE-1** écrit « à la tête (`4e692df`) ». Or `4e692df` est le dernier commit qui touche
    `s2bis/tests/__init__.py`, pas la tête (`1a388e1`). Le constat lui-même est juste : 0 mention de proxy dans ce
    fichier à `1a388e1`.
- **R-2** (faible, C-5) : mon mutant **X09** (« semaine de l'oracle commencée 10 minutes plus tôt » :
  `socle.minutes(dict(o, debut=o["debut"] - 600))` dans `bougies.oracle_sh`) **vit**.
  - Cause : la fixture de `test_series.test_oracle` ne porte des minutes actives hors de la semaine qu'après sa fin
    (minute 9).
  - Effet : au lancement, il échouerait fermé (CA/oracle-sh), comme G07 que la G2 a tout de même fait tuer.
  - Correction proposée : une minute active avant `T0` dans la série `binance`, avec pour preuve X09 tué.
  - Variante à l'arbitrage de l'orchestrateur : l'accepter en limite écrite, puisque la lettre de C-5 (sous-fenêtre
    stricte, minutes actives hors de la semaine, G07 tué) est tenue.

## 1. Pièces

- `sha256sum -c SHA256SUMS` donne 247 OK et 1 FAILED, sur `ADJUDICATION-G2.md`. L'explication : le fichier a été
  modifié à 09:58:52, après `SHA256SUMS` (09:57:52), par l'ajout daté de l'orchestrateur (« après 09:59 UTC »). C'est
  attendu.
- `g2/SHA256SUMS` : 61/61 OK.
- Lus [lu] :
  - `ADJUDICATION-G2.md` en entier, ajout daté compris ;
  - `g2/RAPPORT-G2.md` en entier ;
  - `g2/NOTES.md` ;
  - `g2/outils/mutants_g2.py` ;
  - `RAPPORT-GENERATEUR.md` §1 et §11, comme une donnée ;
  - `BRIEF-CA.md` ;
  - `diffs/CA-6d.diff` en entier ;
  - à l'état final : `cadence.py`, `tau.py`, `sigma.py`, `socle.py` (Refus, regle, oracles), `bougies.oracle_sh`,
    `tests/__init__.py`, `tests/serveur.py` (en-tête), `test_tau.test_places` ;
  - ADR-0029 l.181-191, dont l'amendement (2) : « la valeur de la règle imprimée » ;
  - SOURCES-HISTORIQUES l.100-112 ;
  - annexe B l.1086 et l.1265-1272. J'ai aussi cherché des identifiants d'items par motif dans ce seul fichier.
- Non ouverts : `tau_sigma.txt`, tout `*.jsonl`, les dossiers interdits, les pièces de D.2. Je n'ai jamais lu la sortie
  brute de xtask.

## 2. Série et tête

- **Base + 20 diffs** (`outils/par_diff_cc.py`, `git apply`) :
  - 20/20 appliqués ;
  - **l'état après chaque diff est égal à l'octet à `travail/snap/<id>`** (dossier `scripts/calib-actifs` et
    `gates.yml`) ;
  - l'état final est égal à `travail/snap/CA-6d` ;
  - lignes ajoutées : 200, 192, 128, 198, 111, 126, 184, 190, 161, 182, 105, 125, 173, 110, 126, 186, 186, 179, 115,
    188. Ce qui fait 2 977 + 188 = **3 165**, au plus 200 par diff ;
  - forme : 0 octet 92, aucune ligne de plus de 120 caractères, aucun TODO, FIXME ni XXX, à chaque pas.
- **CA-0a … CA-6c inchangés**. Quatre preuves concordent :
  - les instantanés CA-0a … CA-6c datent au plus tard de 08:40, avant la G2 (08:48) ;
  - les 19 sha256 abrégés du tableau §1 (écrit avant la G2) sont égaux aux sha256 actuels ;
  - le sha256 complet de CA-5e cité par la G2 (`cf3baa70075f…983c7f7d`) est égal ;
  - `g2/travail/CA-0a-tete.diff`, ramené à `--plancher 194`, est égal à `diffs/CA-0a.diff`.
- **Tête `1a388e1` + `diffs-tete/`** :
  - `diffs/CA-0a.diff` tel quel échoue sur la tête (`gates.yml:245`) : le conflit est confirmé ;
  - `diffs-tete/` ne diffère de `diffs/` que par les lignes `index`, l'en-tête des hunks `gates.yml` (+2 lignes) et la
    seule ligne de contexte `--plancher 194` → `210` de CA-0a. Les hunks de code sont identiques ;
  - `git apply` et `patch -p1` donnent 20/20 chacun, sans fuzz ni décalage, avec des résultats égaux ;
  - **le lot est identique à l'octet à `snap/CA-6d`** ;
  - `gates.yml` est égal à celui de la tête plus le seul job neuf (`--plancher 64`). Le blob `index` final `b8fc2ee` est
    égal à `git hash-object` du résultat.
- Sommes vérifiées :
  - `SHA256SUMS` du lot : 29/29 OK, sha256 `485a82fe…4ea6` ;
  - CA-6d : `00101674…8854` ;
  - `diffs-tete/CA-0a` : `5ecf4078…b372` ;
  - `diffs-tete/CA-6d` : `8a3b1c7a…82c2`.

  Tous ces sha256 sont égaux à ceux du §11.

## 3. Corrections une par une

Tous les mutants sont classés par la commande du job (plancher 64), sous `run.sh`. Le libellé « FAIL » désigne un rouge
d'assertion, jamais une ERROR.

| C | code et test lus | mutant visé, sous le test neuf | sans le mutant | règle de fixture | avis |
|---|---|---|---|---|---|
| C-1 | `test_tau.test_agregateurs_suite` (ph 0,0050 > sh 0,0045 → 0,0055 ; sous sh : 0,00588… → 0,0060) ; `synthetiques.BTC_PH` dans `test_planchers_seuls` (0,0200 contre 0,0225 sous sh). Valeurs recalculées à la main. | G01 TUE (FAIL `test_agregateurs_suite`, `test_planchers_seuls`) | vert | ph, sh et τ_agr_BTC 0,0265 distincts ; dénominateurs sh et max distincts | conforme |
| C-2 | `test_sigma.test_maximum_des_strates` : âges (0, 2) et (0, 7), P99 de rang 2, max 7, 3 × 7 × 60 = 1 260 s ; les deux ordres | G14 TUE (FAIL) ; X08 (moyenne) TUE | vert | P99 de calme ≠ P99 de stress, dans les deux ordres (sinon G14 vivrait sur la seconde moitié) | conforme |
| C-3 | `test_pages.test_garde_reseau` : sous-processus, quatre mandataires fictifs, `getproxies()` ∩ {http, https, all} = ∅ ; `test_cadence.test_cli_hors_lanceur` : paramètres locaux, les deux URL d'agrégateur sur `Serveur` (127.0.0.1), `essais` 1, `lectures` 1, `TENTATIVES` inchangé | G11 TUE sous `run.sh` **et sous `env -i`** (§4) ; KCAD (garde retirée) TUE ; X01 et X02 TUE | vert (aussi sous `env -i` et avec mandataire posé) | valeurs fictives sur la boucle locale | conforme |
| C-4 | `test_identite` : `sys.executable` plus chaque `python3.1x` présent, × graines 0 et 1 ; README | sous le PATH simulé (sans 3.10 à 3.13, `python3` → 3.12) : MCA23 TUE (FAIL `test_identite`), X14 TUE | sous le PATH simulé : vert, Ran 64 ; `test_identite` de CA-6c sous le même PATH : FAIL « None unexpectedly found in [None, None, None, None] » | — | conforme |
| C-5 | `test_series.test_oracle` : minute 9 active hors de la semaine ; `Refus` rendu en assertion | G07 TUE (FAIL) | vert | 4 actives contre 3 attendues : distinctes | conforme ; **X09 vit (R-2)** |
| C-6 | `test_comptes_de_sh` : tableau lu ligne à ligne, jeu de places par colonne (« ci-dessus », « sans »), comptes à ≥ 4, 3 et 2 places ; phrase des actives lue place par place. **Relu à la main contre SH l.103-111** : 5 concurrences et 5 comptes par place égaux à `parametres.json` | G29, G30 TUE (FAIL) | vert | comptes par place tous distincts (9 998, 1 098, 693, 9 551) | conforme ; O-13 inchangé (lecture par position) |
| C-7 | `test_pages.test_main` : seul fichier `page-1790811000.json` dans la descriptive, URL de fin 1790812740 (`date -u -d @1790812800` = 2026-10-01 00:00 ; −60 s) | G08 TUE (FAIL) | vert | bornes de la descriptive ≠ bornes de la principale | conforme |
| C-8 | `test_fragment.test_borne_basse_et_variante` : écarts nuls, règle 0, τ 0,0005 avec drapeau, τ_agr 0,0005 × 0,0265 / 0,0050 = 0,00265 → 0,0030 | G23 TUE (FAIL) | vert | règle 0 ≠ τ 0,0005, et sous G23 τ_agr 0,0005 ≠ 0,0030 | conforme |
| C-9 | `test_fenetre.test_oracles` : seuil relu à 0,003 (1,5 × 0,003 = 0,0045 ≠ 0,00375) ; `test_agregateurs_suite` : τ de BTC nul, classe par classe | G12, G13 TUE (FAIL) ; X06 (`<` au lieu de `!=`) TUE | vert | seuil fictif distinct du scellé | conforme |
| C-10 | `cadence.releve` capte `TypeError` ; `test_corps_hors_forme` : corps `[]` et `"x"`, BTC propre à chaque agrégateur (100 et 200, ETH 150 : oui et non) | G28a (AttributeError), G28b (état avant), G28c (tuple de la G2) et G10 TUE ; avec le code de CA-6c : FAIL `['TypeError', 'TypeError'] != [({}, 2), ({}, 2)]` | vert | médianes de BTC distinctes, verdicts opposés | conforme |
| C-11 | même test, lecture A-prime : USDC sur 3 places, N_min 3, 15 cellules par strate (5 minutes × 3 places) | G27 TUE (FAIL) ; X12 (lecture forcée à A) TUE | vert | N_min 3 (A-prime) ≠ 4 (A) | conforme |
| C-12 | §1 : CA-5e `cf3baa70…7f7d` = `sha256sum` ; §2 E-CA-04 `socle.py:19` = `ETIQUETTE` (`sed -n 19p`, ligne inchangée par CA-6d) | — | — | — | conforme |
| C-13 | `Refus(valeur=(nom, valeur))` hors du message ; `tau.main` écrit après le refus la ligne `descriptif hors refus (jamais décisif) : valeur calculée de la règle, <nom> : <v> ; <lieu>` ; JSON inchangé ; README. Conforme à l'amendement (2) d'ADR-0029 (« la valeur de la règle imprimée ») | avec le code de CA-6c : 4 FAIL (`test_borne_valeur`, `test_agregateurs_suite`, `test_places`, et C-10) ; X03 (ordre), X04 (valeur dans le message), X05 (autre dénominateur) TUE | vert | valeurs indépendantes : 0,0300 (`test_places`, 1,5 × 0,02) et 0,0530 (0,0100 × 0,0265 / 0,0050) ; `test_borne_valeur` compare au calcul direct (limite déclarée par le correcteur) | conforme ; O-CC-2 |

**Périmètre de CA-6d.** Le diff touche 17 fichiers, chacun rattaché à une correction : `gates.yml` (plancher), README
(C-4, C-13), `SHA256SUMS`, `cadence.py` (C-10), `socle.py` (C-13), `tau.py` (C-13), `synthetiques.py` (C-1), et les
tests (C-1 à C-11, C-13). Rien n'est hors liste. Les 5 tests neufs font passer Ran de 59 à 64.

## 4. C-3 : indépendance de l'environnement

1. **Sans aucun mandataire posé** : le job a été lancé sous `run.sh env -i PATH=/usr/bin:/bin HOME=/root TMPDIR=…`.
   Une sonde dans le même environnement montre ce qu'il contient : variables `HOME`, `LC_CTYPE`, `PATH`, `TMPDIR`
   seulement ; aucune variable dont le nom contient « proxy » ; `getproxies()` vaut `{}`. Résultats :
   - **G11 TUE** : FAIL `(0, "['all', 'http', 'https']") != (0, '[]')`, car le sous-processus pose lui-même les quatre
     variables fictives ;
   - X01 TUE (`os.unsetenv` à la place de `del os.environ`) ;
   - témoin G00 vert.

   Sous `run.sh` seul, G11 est aussi tué. Il reste alors des variables étrangères au schéma (`GLOBAL_AGENT_HTTPS_PROXY`,
   etc.), mais le test ne regarde que http, https et all.
2. **Avec mandataire posé** (`HTTPS_PROXY`, `https_proxy`, `ALL_PROXY` fictifs, `127.0.0.1:9`) : G11 est TUE et le
   témoin reste vert. La purge en processus marche avec une variable posée.
3. **Cas « variable posée » de la cadence** :
   - les deux URL de `cadence.AGREGATEURS` sont remplacées par `Serveur.base` (`http://127.0.0.1:<port>`) ;
   - `parametres.json` → `reseau` ne porte aucune URL ;
   - sous KCAD (garde retirée) et sous X02 (garde sur un environnement vide), le relevé part vers le serveur local et
     le test échoue sur les codes : `([0, 2], …) != ([3, 2], …)` ;
   - l'assertion `tests.TENTATIVES == avant`, placée avant, passe, donc aucune tentative n'a visé un hôte hors de la
     boucle locale ;
   - l'exécution était en plus isolée (`unshare -n`).

## 5. Mutants (`outils/mutants_cc.py`)

Méthode :
- commande exacte du job (`python3 -B enforcement/verdict-suite-s2.py scripts/calib-actifs --aucun-saut --egal
  --plancher 64`), depuis une racine jetable (tête + `diffs-tete/`) ;
- borne de 300 s, PAR = 2, `start_new_session` et `killpg` ;
- classement : sortie 1 TUE, sortie 0 VIVANT, autre sortie FATAL ;
- chaque motif est compté sur les octets et doit apparaître exactement 1 fois ; les 29 motifs ont été comptés avant le
  lancement.

| campagne | PID | mutants | bilan |
|---|---|---|---|
| principale (10:06-10:09) | 12007 | G00, 14 vivants de la G2 (G28 en 3 formes), KCAD, 9 neufs | 24 TUE, 3 VIVANT (G00 témoin, G26, X09), 0 FATAL, 0 INVALIDE |
| PATH simulé | premier plan | G00, MCA23, X14 | 2 TUE, G00 vert |
| `env -i` | premier plan | G00, G11, X01 | 2 TUE, G00 vert |
| mandataire fictif posé | premier plan | G00, G11 | 1 TUE, G00 vert |

**Les 14 vivants de la G2** : G01, G07, G08, G10, G11, G12, G13, G14, G23, G27, G28 (a, b, c), G29 et G30 sont tués,
soit **13 tués**. **G26 vit**, mutant équivalent sous les paramètres scellés (O-10 admis).

**Mes 10 mutants neufs sur CA-6d** :

| id | objet | état | tué par |
|---|---|---|---|
| X01 | C-3 : purge par `os.unsetenv` (environnement C seul) | TUE | `test_garde_reseau` |
| X02 | C-3 : garde de `cadence.main` sur un environnement vide | TUE | `test_cli_hors_lanceur` |
| X03 | C-13 : ligne descriptive avant le refus | TUE | `test_borne_valeur` |
| X04 | C-13 : valeur dans le message du refus | TUE | `test_agregateurs_suite`, `test_borne_valeur` |
| X05 | C-13 : valeur des agrégateurs sous le dénominateur minimum | TUE | `test_agregateurs_suite` |
| X06 | C-9 : seuil comparé dans un seul sens (`<`) | TUE | `test_oracles` |
| X08 | C-2 : moyenne des strates | TUE | `test_maximum_des_strates` |
| X09 | C-5 : semaine commencée 10 minutes plus tôt | **VIVANT** | — (R-2) |
| X12 | C-11 : lecture forcée à A au calcul | TUE | `test_borne_basse_et_variante` |
| X14 | C-4 : ensemble dans les lignes de septembre (PATH simulé) | TUE | `test_identite`, `test_succes`, `test_corps_et_septembre` |

Tous les rouges sont des FAIL d'assertion, aucun n'est une ERROR. La campagne du correcteur, d'après son tsv final, fait
42 mutants : 41 TUE et 1 VIVANT (G26), comme il l'écrit.

## 6. Gates

Le détail est dans `travail/par_diff_base.log`, `batterie_tete.log`, `batterie/`, `xtask.log` et `xtask-*-verdicts.txt`.

- **Plancher exact à chaque diff** (base + série, PID 9758) : les 20 diffs donnent code 0 avec Ran égal au plancher
  (3, 6, 9, 11, 14, 16, 20, 24, 28, 33, 37, 40, 44, 47, 49, 52, 56, 58, 59, 64), verdict conforme. CA-6d n'a ni
  « Exception ignored » ni « Warning ».
- **Matrice** python3.10, 3.11, 3.12 et 3.13, en `-X dev -W error` avec `PYTHONDEVMODE=1` et `PYTHONWARNINGS=error` :
  - tête + série : 4 fois code 0, Ran 64, 0 « Exception ignored », 0 « Warning » ;
  - base + série : même résultat.
- **Tête + `diffs-tete/`** (PID 24496) :

  | suite | résultat |
  |---|---|
  | job neuf | conforme, Ran 64 |
  | runner | 136 ok, 0 échec |
  | s2bis | conforme, Ran 340 |
  | S2 | conforme, Ran 415, sauts nommant `SHOGEN_S2_CAMPAGNE_CONTROL` (jamais posée) |

- **xtask** (`cargo --locked --offline xtask verify`, PID 30633, lignes VERDICT seules) : la tête neuve et la tête +
  `diffs-tete/` donnent **10 lignes identiques** :
  - 8 VERT, puis la 9e ROUGE (1 violation) ;
  - verdict global ROUGE, comme sur la tête neuve ;
  - ces lignes sont égales aux verdicts du correcteur.

  La série ne change aucun verdict. Je n'ai pas vu le motif de la violation, puisque je n'ai lu que les lignes VERDICT.
- **sim-bis** : non lancé, par consigne. L'orchestrateur le lance à la chaîne.

## 7. Lignes d'items du §11.4

| item | avis |
|---|---|
| SIGMA-ARRONDI-1 | Exact sur le fond. `sigma.py` l.64 est exact ; pour `tau.py`, lire l.136 à l'état commis (R-1 b). |
| FORMES-API-1 | Fidèle à O-7 et Q-CA3-8 ; c'est bien une condition de l'épinglage. |
| RB2-SCHEMA-MODES-1 | **À ne pas former** : volet de SHOGEN-S2BIS-CALIB-L189-1 (R-1 a). |
| O-6, O-3 sans item | Raisons cohérentes avec le code : en-tête sha256 du manifeste, `septembre` descriptif. |
| TESTS-GARDE-MANDATAIRE-1 | Constat exact (0 mention de proxy à `1a388e1`) ; libellé du commit à corriger (R-1 c). |
| MUTANTS-ORPHELINS-1 | Exact. |
| CI-CABLAGE-CALIB-1 | Exact : 0 mention de `calib` dans `run-fixtures-verdict-suite-s2.py` à la tête. |
| P1-ESTIMATION-1 (volet) | 3 165 = 2 977 + 188, recompté. |

## 8. Constats neufs

- **O-CC-1** (faible) : X09 vivant (R-2).
- **O-CC-2** (faible, limite de C-13) : seule la valeur du **premier** CA/borne s'imprime, car le calcul s'arrête au
  premier refus. Si deux actifs touchent la borne, la valeur du second reste inconnue et sa décision demanderait un
  second lancement. La lettre de C-13 est tenue ; le but « décision au lancement unique » ne l'est que pour un seul
  actif à la borne. À adjuger : limite écrite au README ou au paquet, ou item.
- **O-CC-3** (forme) : les renvois de décalage du §11.1 sont approximatifs.
  - `socle.py` : la ligne insérée suit l'ancienne l.39, et le texte dit « au-delà de la l.37 » ;
  - `tau.py` : le troisième hunk ajoute encore 2 lignes au-delà de l'ancienne l.266, soit +4 au total, ce qui n'est
    pas dit.

  Aucun renvoi du §2 ne tombe à mon avis dans l'intervalle, mais je ne l'ai pas vérifié ligne à ligne.
- **O-CC-4** (information) : l'échec de `ADJUDICATION-G2.md` dans `SHA256SUMS` vient de l'ajout daté postérieur. Un
  nouveau `SHA256SUMS` sera à recalculer à la clôture.

## 9. Écarts du contre-contrôleur

- **E-CC-1** (B.16) : j'ai tapé des barres obliques inverses trois fois.
  - Un motif `grep` après `od -c` (09:59) : sortie non retenue, contrôle refait en Python par le compte de l'octet 92.
  - Un regex dans un heredoc Python, pour croiser les sha256 du §1 (10:01) : le regex a trouvé les 19 lignes attendues
    et chaque sha256 vient d'un `sha256sum` séparé.
  - Des guillemets échappés dans un `awk` (10:15) : la commande a échoué, aucun résultat retenu, refaite en Python.

  Mes quatre outils ont 0 octet 92 (compté).
- **E-CC-2** : `setsid` a fourché : le PID consigné d'abord (9756) était celui du parent ; le PID réel, 9758, est
  consigné. Les autres PID ont été relevés par `ps`.
- **E-CC-3** : j'ai fait un `ls` non récursif de `docs/adr-0029/` (pour trouver le fichier de l'ADR) et des `grep` sur
  le seul fichier `docs/adr-0028/ANNEXE-B-items.md` (identifiants d'items, l.1086 et l.1265-1272). Je n'ai fait aucune
  recherche récursive.
- Fin : copies (archives, séries) et `g2/cc/tmp` supprimées (cible cargo, PATH simulé, sorties brutes de xtask non
  lues) ; `ps` ne montre plus aucun processus à moi. `SHOGEN_S2_CAMPAGNE_CONTROL` n'a jamais été posée. Aucune clé ni
  aucun secret n'a été affiché ou écrit. Rien sur Pocket.

## 10. Provenance

- Journal : `g2/cc/NOTES.md`.
- Outils (`g2/cc/outils/`) : `run.sh`, `sonde_reseau.py`, `sonde_mandataire.py` (copies), `par_diff_cc.py`,
  `mutants_cc.py`, `batterie_cc.py`, `xtask_cc.py`.
- Sorties (`g2/cc/travail/`) :
  - `par_diff_base.log`, `job_base_*.out` ;
  - `mutants_*.tsv`, `mutants_principal.log`, `mut/*.out` ;
  - `c4_avant_pathsim.out`, `code_avant_ca6d.out` ;
  - `batterie_tete.log`, `batterie/` ;
  - `xtask.log`, `xtask-*-verdicts.txt`.
- Les sommes de `g2/cc/` sont dans `g2/cc/SHA256SUMS`.

## 11. Section datée du 2026-10-09, 10:32 à 10:39 UTC (`date -u`) : contrôle de CA-6e (R-2) et verdict final

- **Gate 0** : modèle résolu `claude-opus-5-5` ; même contre-contrôleur. Je n'ai écrit ni CA-6e ni le §12.
- **Réseau** : sonde de 10:32 sous `run.sh`. 1.1.1.1 et 8.8.8.8 : errno 101 ; `urlopen` refusé ; mandataire
  127.0.0.1:36573 : errno 111. Hors isolement, le mandataire répond. Aucune requête réseau.

### Verdict final : **CONFORME**

R-2 est levée. R-1, sur les lignes d'items, est traitée par l'orchestrateur au versement, comme le dit la consigne.

### Preuves

- **Pièces**
  - `sha256sum -c SHA256SUMS` : 306/306 OK.
  - `diffs/CA-6e.diff` et `diffs-tete/CA-6e.diff` sont identiques, sha256 `21413440ace3…15120636`.
  - CA-6e ajoute 3 lignes : celle de `test_series.py` dans le `SHA256SUMS` du lot, la série `binance` avec la minute
    −1, et un commentaire. Il ne touche ni le code ni `gates.yml`. Le plancher reste 64.
  - `SHA256SUMS` du lot : 29/29 OK. `test_series.py` vaut `aa30da9b…`.
- **§11.1 corrigé** : les décalages ont été recalculés par `difflib` entre `snap/CA-6c` et `snap/CA-6d`. Ils sont
  exacts :
  - `socle.py` : +1 à partir de l'ancienne l.40 ;
  - `tau.py` : +1 pour les anciennes l.67 à 85, +2 pour les l.86 à 266, +4 à partir de la l.267.

  Cela clôt O-CC-3. Le §12 relève aussi l'item SHOGEN-CALIB-BORNE-MULTI-1 pour O-CC-2.
- **Mutants**
  - Classement par la commande du job, plancher 64, PAR 2, `killpg`. Motifs comptés : une fois chacun.
  - Sur CA-6e :
    - **X09 TUE**, par un FAIL d'assertion de `test_oracle` : « REFUS CA/oracle-sh : minutes actives différentes de
      SH §4 ; actif USDC ; place binance ». C'est un rouge d'assertion, pas une ERROR ;
    - **G07 toujours TUE**, par la minute 9 ;
    - mon mutant neuf **Z01** est **TUE** (FAIL `test_oracle`). Z01 ignore la borne basse de la semaine : `{t for t in
      series[a, p] if t < o["fin"] and …}` ;
    - témoin G00 vert (Ran 64).
  - Sur le lot de CA-6d, dans les mêmes conditions : X09 et Z01 sont **VIVANTS**. C'est donc bien la minute −1 de CA-6e
    qui les tue.
- **Base + 21 diffs** (PID 17623) : 21/21 en code 0, avec Ran égal au plancher (3 … 59, 64, 64). L'état est égal à
  l'octet à `snap/<id>` à chaque pas, et l'état final à `snap/CA-6e`. Lignes ajoutées : 3 168. Forme : 0 octet 92,
  aucune ligne de plus de 120 caractères, aucun TODO ni FIXME.
- **Tête `1a388e1` + `diffs-tete/`**
  - 21/21 appliqués ; `git apply` et `patch -p1` donnent le même état.
  - Les 121 lignes `index` des 21 diffs sont égales au `git hash-object` des fichiers après chaque pas.
  - Le lot est égal à l'octet à `snap/CA-6e`, et `gates.yml` est celui de la tête plus les 20 lignes du job neuf.
- **Les 20 autres `diffs-tete/` sont inchangés.** Leur date de fichier a été réécrite à 10:24:50, mais leur contenu
  est le même.
  - Seules les différences déjà relevées à 10:02 les séparent de `diffs/` : lignes `index`, en-têtes de hunk de
    `gates.yml`, et contexte `--plancher 194` → `210` de CA-0a.
  - `diffs-tete/CA-0a` et `diffs-tete/CA-6d` gardent les sha256 de mon §2 (`5ecf4078…b372`, `8a3b1c7a…82c2`).
  - `diffs/CA-0a` … `CA-6d` : dates ≤ 09:42:53, tableau §1 19/19, CA-6d `00101674…8854`.
- **Batterie sur la tête + 21 diffs** (PID 22713) :
  - matrice 3.10 à 3.13 en `-X dev -W error` : 4 fois code 0, Ran 64, 0 « Exception ignored », 0 « Warning » ;
  - job neuf : conforme, Ran 64 ;
  - runner : 136 ok, 0 échec ;
  - s2bis : conforme, Ran 340 ;
  - S2 : conforme, Ran 415, sauts nommant la variable, jamais posée.
- **Non relancés par moi** : sim-bis (consigne) et xtask. CA-6e ne touche qu'un test et `SHA256SUMS` sous
  `scripts/calib-actifs`. Je n'ai pas vérifié l'affirmation du §12 selon laquelle les verdicts xtask sont inchangés.

### Écarts

- **E-CC-4** (B.16) : en ajoutant Z01 à mon outil, j'ai tapé des barres obliques inverses : des guillemets échappés
  dans un heredoc Python. Effet contrôlé : 0 octet 92 dans `mutants_cc.py`, la ligne a été relue, et le motif compté
  vaut 1 au lancement.
- **Fin** : archives et copies supprimées, `g2/cc/tmp` vide, `ps` sans aucun processus à moi. `SHOGEN_S2_CAMPAGNE_CONTROL`
  n'a jamais été posée. Aucune écriture git, aucun secret, rien sur Pocket.
- **Provenance** (dans `travail/`) :
  - `par_diff_base6e.log` ;
  - `job_base6e_*.out` ;
  - `mutants_ca6e.tsv`, `mutants_ca6d_avant.tsv`, `mut/ca6e_*.out`, `mut/ca6d_avant_*.out` ;
  - `batterie_tete6e.log`, `batterie/tete6e_*`.
