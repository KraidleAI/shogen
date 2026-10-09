# Relecture G2 neuve de DETTES-T3 (transcrit)

> Transcription par l'orchestrateur le 2026-10-09 18:07:35 UTC du fichier g2/RAPPORT-G2.md ; contrôle FM-1.1 des transcripts du générateur-correcteur, du réviseur et du contre-contrôleur, par le fm11.py versé et par celui de DT3-E : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Relecture G2 neuve du lot DETTES-T3 (série DT3-A, DT3-E, DT3-B, DT3-C, DT3-D)

- **Modèle** : `claude-opus-5-5`
- Gate 0 : modèle résolu `claude-opus-5-5` (identifiant exact donné par l'environnement), effort `max` demandé par le
  brief (non observable de l'intérieur). Heures lues par `date -u` : début 2026-10-09 16:05:56Z ; rédaction 16:19:20Z.
- Réviseur neuf : je n'ai écrit aucun des diffs relus. Base : `/home/user/shogen` HEAD
  `0cfbe3ecaeac81cbb35f606b3c53ef3df856dff5`, égale à la tête du brief ; dépôt réel jamais modifié (lectures seules,
  `git status` vide à la fin, HEAD inchangé).
- Pièces relues (sha256, 16 premiers caractères) : `DT3-A.diff` `b018c1f1a7255502`, `DT3-E.diff` `2cbd3e1b0a61f883`,
  `DT3-B.diff` `1f0d78c7ed63d033`, `DT3-C.diff` `9239ceab0eb7c2c4`, `DT3-D.diff` `47dd12caaff7b7fa`,
  `ADJUDICATION-G1.md` `87818903a5990e6b`, `RAPPORT-GENERATEUR.md` `976c876e31365e23`.
- Rattachement (G0) : `docs/adr-0028/ANNEXE-B-items.md` (sha256 `16f6e5615c57…`, 1 518 lignes) l.520 (B.35), l.894
  (B.54), l.1014 (B.60), l.1367 (B.85), B.87 l.1390 et l.1507 ; `docs/adr-0028/G0-lot-D8a.md` l.190-198 (CH-4) et l.424.

## Verdict : ACCEPTE-AVEC-CORRECTIONS (C-1 à C-9, liste fermée)

La série s'applique dans l'ordre A, E, B, C, D sur la tête (`git apply --check` puis `git apply`, arbre égal à `st-D/`
du générateur, `diff -r` vide). Toutes les gates sont vertes sur la série. Les quatre dettes sont fermées au sens de
l'adjudication, avec une réserve sur la part « information de l'investisseur » de P1-ESTIMATION (O-1). Mais six
mutants neufs, plausibles, survivent à la suite du lot (N-1 à N-6). Les tests proposés en C-1 à C-3 les tuent tous,
mesure faite sur une copie corrigée. Une erreur interne de `journaux-modele.py` sort en 1 (refus) au lieu de 3 (C-4). Il
manque deux textes de procédure ou de garantie (C-5, C-9) et une précision d'usage dans la consigne G2 (C-7). Deux
citations ou dates sont à corriger (C-6, C-8). Toutes ces corrections tiennent dans le lot (règle « aucune dette »,
B.87). Aucun item n'est à former.

La forme de C-1 à C-7 est écrite et vérifiée dans `propositions/corrections-G2.diff` (sha256 `24f750e5fa2ece80…`) :
`git apply --check` vert sur la série. Sur la copie corrigée : `controle-unittest` à `--egal --plancher 18`, conforme,
Ran = 18 ; runner 137 ok ; lint R-1 OK ; `journaux-modele` conforme.

### Corrections (liste fermée)

- **C-1 (DT3-E, `scripts/controle/tests/test_fm11.py`)** : ajouter `Temoin.test_queue_aux_longueurs_limites`. Le test
  prend une ligne interdite de n caractères tous distincts (U+0100 et suivants), pour n = 39, 40, 41, 59, 60 et 61. Les
  extraits (début, fin, détecté) sont écrits à la main : 39 : (0,39,1), (1,39,0) ; 40 : (0,40,1), (1,40,0) ; 41 :
  (1,41,1), (0,40,1), (2,41,0) ; 59 : (19,59,1), (0,40,1), (10,50,0) ; 60 : (20,60,1), (21,60,0), (10,50,0) ; 61 :
  (21,61,1), (20,60,1), (22,61,0). Le test vérifie la liste des événements `FRAGMENT:carto_l51`. Plancher de
  `controle-unittest` : +1 dès E (8 → 9). Il tue N-1, N-2 et N-3. Sur le `fm11.py` de la tête, il est rouge par
  AssertionError, aux longueurs 41, 59, 60 et 61. Taille : +13 lignes, DT3-E passe à +46.
- **C-2 (DT3-B, `scripts/controle/tests/test_journaux_modele.py`)** : dans `test_formes_refusees`, ajouter trois lignes
  refusées : `claude-opus-5[1m]`, `opus[1m]` et `claude-opus-5-5[1m][1m]`. Dans `test_exempte_puis_modifie`, ajouter
  `self.assertEqual(controler(self.arbre({"G1-lot-NEUF.md": texte}))[0], 1)` : mêmes octets, nom neuf. Ces ajouts tuent
  N-4 (exemption par sha256 seul) et N-5 (tout suffixe `[1m]` admis). Taille : +3 lignes, DT3-B passe à +192.
- **C-3 (DT3-C, `scripts/controle/tests/test_fiche_worker.py`)** : ajouter `test_commande_passe_l_analyseur`. Le test
  lance la commande de la consigne, lue dans `COMMANDE` : marqueurs remplacés par des valeurs factices (`--commit` 40
  zéros, `--auteur claude-opus-5-5`, `--depot` et `--sortie` sous un dossier temporaire, dépôt absent), sans la
  variable interdite. Il exige qu'aucun `usage:` ne paraisse, puis la sortie 2 avec un stderr qui commence par
  `oracle_record : ` : l'analyseur réel admet la commande, et l'outil la refuse ensuite sur le dépôt absent. Le test
  actuel ne lit que l'aide, et N-6 (l'outil exige une option de plus à l'écriture) lui survit. Plancher : +1. Taille :
  +17 lignes.
- **C-4 (`enforcement/journaux-modele.py`, `main`)** : remplacer `except (OSError, ValueError) as e:` par
  `except Exception as e:`, pour que la sortie soit 3 et jamais 1. Mesure : un `oracle_record.py` sans `auteur_admis`,
  en erreur de syntaxe ou à import manquant fait sortir le script en **1**, la sortie d'un refus, avec une trace. Cela
  contredit le contrat de sa docstring (« 3 erreur ») et la règle SHOGEN-MUT-FATAL-1 : une erreur fatale ne se compte
  jamais comme un refus. Test : dans `test_racine_illisible`, un arbre temporaire qui porte une copie du script et un
  `s2-harness/tools/oracle_record.py` vide doit sortir en 3. Ce test est rouge (`AssertionError: 1 != 3`) sur le code
  du lot. Taille : ±1 ligne de code, +7 lignes de test.
- **C-5 (`enforcement/journaux-modele.py`, docstring)** : écrire la procédure de retouche d'un journal exempté. Forme
  proposée : « un journal exempté puis modifié ne l'est plus : le commit qui le modifie lui ajoute la ligne (ajout daté,
  identifiant de son auteur) ; G1-lot-DETTES-B2.md et G2-lot-DETTES-B2.md, qui portent déjà une ligne de cette tête hors
  forme, ne se modifient qu'avec leur sha256 changé ici, par un lot ». Taille : +2 lignes nettes. Fondement : O-3.
  **R-25** : C-2, C-4 et C-5 réunis porteraient DT3-B à +201. Je propose de mettre C-4 et C-5 dans un diff DT3-F
  appliqué après D (environ +12 −3), ou de resserrer la docstring d'une ligne.
- **C-6 (DT3-D)** : le rattachement « annexe B, B.55 et B.61 » est inexact. L'item SHOGEN-S2BIS-P1-ESTIMATION-1 est
  formé au bloc B.60 (en-tête l.992, item l.1014). Son volet CALIB-ACTIFS est au bloc B.85 (en-tête l.1352, volet
  l.1367) et sa portée est étendue en B.61. Forme : « (SHOGEN-S2BIS-P1-ESTIMATION-1, annexe B, B.60 ; volets B.61 et
  B.85) ».
- **C-7 (DT3-C, consigne de `shogen-worker.md`)** : ajouter à la fin de la consigne : « `<commit relu>` est le sha
  complet du commit qui porte la série, présent dans `<copie>` ; une relecture de diffs non commis n'en a pas : son
  rapport le dit, et l'orchestrateur fait enregistrer le rôle G2 sur son commit avant le cp-2. » Motif : `oracle_record`
  extrait `--commit` de `--depot` par `git archive`. Une G2 faite avant le commit de l'orchestrateur, comme celle-ci, n'a
  aucun commit à citer, et la règle 2 de la fiche lui interdit d'en créer un. La consigne serait alors inexécutable sans
  rien en dire. Cette précision reste soumise à l'adjudication de l'orchestrateur (procédure). Le test de C-3 n'en
  dépend pas.
- **C-8 (DT3-A et DT3-E, `scripts/controle/README.md`)** : les deux ajouts « *Ajout daté du 2026-10-09 (lot
  DETTES-T3, …)* » n'ont pas d'heure, alors que l'ajout précédent du même fichier en porte une (« 2026-10-03 01:43:15
  UTC »), comme DT3-C et DT3-D. Ajouter l'heure lue par `date -u` au moment de l'écriture.
- **C-9 (DT3-E, ajout daté du README)** : écrire la garantie de détection, qui suit de la règle des fenêtres et que C-1
  vérifie. Forme : « tout extrait d'au moins 60 caractères consécutifs d'une ligne interdite contient un fragment et est
  détecté ; un extrait de 40 à 59 caractères ne l'est que s'il contient une fenêtre (pas de 20) ou la queue ».
  Démonstration : un extrait [s, s+60) contient la fenêtre qui commence au premier multiple de 20 au moins égal à s, ou
  bien la queue. Mesure : l'extrait (10, 50) n'est pas détecté aux longueurs 59, 60 et 61.

## Checklist G2

### (1) Fermeture des dettes

| dette | diff | fermeture |
|---|---|---|
| SHOGEN-FM11-VERIFIABLE-1 (B.35 l.520) | A, E | Fermée. Le témoin automatique est versé (`test_fm11.py`, 8 tests après E, 9 avec C-1), `SHA256SUMS` couvre 71 fichiers (`sha256sum -c` : 71 OK sur la série) et le test est câblé (job `controle-unittest`, K-04). L-1 (queue) est corrigé par E, comme l'adjudication le demande : `| {v[-40:]}`, nouveau sha256 `4a0b8abc…` épinglé au test, au README et aux sommes. À la tête, seule la ligne de `fm11.py` diffère des sommes de la série : les 28 sommes ajoutées attestent bien les octets de `0cfbe3e`. |
| SHOGEN-R1-FORME-RESOLUE-1 (G0-D8a l.424) | B | Fermée sur la portée adjugée (Q-B1). La ligne « Modèle » des journaux `docs/G1-*.md` et `docs/G2-*.md` nouveaux est contrôlée par égalité exacte (`auteur_admis`, aucun test de préfixe, CH-4). Le champ `auteur` de l'enregistrement est déjà contrôlé par `oracle_record.auteur_admis`, à l'écriture comme à la lecture. La liste figée est recalculée : 52 noms et sha256, identiques aux blobs de HEAD (`diff` vide). L'étape est câblée au job g1. Réserves : C-2, C-4, C-5. |
| SHOGEN-G2-ENREG-ROLE-1 (B.54 l.894) | C | Fermée sur la forme adjugée (Q-C1). La consigne datée est au bloc « Consignes de gabarit », avec la commande à la lettre de l'adjudication, et elle est contrôlée par `test_fiche_worker.py`. Réserves : C-3 et C-7. |
| SHOGEN-S2BIS-P1-ESTIMATION-1 (B.60 l.1014, volet B.85 l.1367) | D | Part « calendrier » fermée : ajout daté au point 4 du G0 adjugé, avec la règle ×2/×3, le jalon sur la borne haute et le rapport mesuré qui remplace le facteur. La part « information de l'investisseur » est un acte de l'orchestrateur (O-1). Réserve : C-6. |

### (2) Tests : rouges, force réelle

Rouges reproduits par moi sur une copie, tous en AssertionError (contrat unittest, sortie 1) :
- E : avec le `fm11.py` de la tête, `test_fragment_en_queue` échoue (`{'resultats': 0, 'entrees': 0} != {'resultats':
  1, 'entrees': 1}`), ainsi que l'épingle et la somme (`886cc676… != 4a0b8abc…`) : 3 FAIL.
- A : avec le `SHA256SUMS` de la tête (ligne de `fm11.py` mise à jour), `test_sommes_couvrent_script_et_sorties` échoue
  sur `Lists differ` (28 chemins).
- B : sans le script, 13 FAIL sur 6 tests (sous-cas compris), chacun en AssertionError sur le code de sortie (2).
- C : avec la fiche de la tête, `test_consigne_au_bloc_de_gabarit` échoue sur `0 != 1`.
- K-04 : non rejoué sans le job (rouge du générateur, contrat du runner, sortie 1). Le runner de la série donne 137 ok
  et celui de la tête 136 ok.

Mutants (`outils/mutants_g2.py`) : une copie neuve par mutant, un remplacement exact (une occurrence exigée), un
lancement borné à 300 s avec `start_new_session` et `killpg`, et un classement selon le contrat (sortie 1 avec FAIL sans
ERROR : tué ; 0 : vivant ; autre : FATAL). La copie témoin non mutée est verte. Le relevé `ps` de fin montre 0 processus
`mutg2_` restant.

| mutant | suite du lot (série) | suite corrigée (C-1 à C-4) | test neuf du réviseur |
|---|---|---|---|
| R-A3 `any` → `all` (rejeu) | tué | tué | — |
| R-A6 numérotation depuis 1 (rejeu) | tué | tué | — |
| R-E1 correction de la queue retirée (rejeu) | tué | tué | — |
| R-E3 queue de 41 (rejeu) | tué | tué | — |
| R-B1 exemption par nom seul (rejeu) | tué | tué | — |
| R-B6 texte collé admis (rejeu) | tué | tué | — |
| R-C2 rôle G1 dans la fiche (rejeu) | tué | tué | — |
| R-C4 rôle G2 retiré de l'outil (rejeu) | tué | tué | — |
| **N-1** `range(0, max(1,len(v)-41), 20)` (borne décalée d'un cran : fenêtre perdue quand n − 40 ≡ 1 mod 20) | **vivant** | tué | tué |
| **N-2** queue `v[len(v)-40:]` (ligne de moins de 40 : fragment d'un caractère) | **vivant** | tué | tué |
| **N-3** queue seulement si `len(v) > 61` | **vivant** | tué | tué |
| **N-4** exemption par sha256 seul, nom ignoré | **vivant** | tué | tué |
| **N-5** tout identifiant suivi de `[1m]` admis | **vivant** | tué | tué |
| **N-6** `oracle_record.py` : l'écriture exige aussi `--base` | **vivant** | tué | tué |

Pourquoi les mutants neufs survivent : la suite du lot n'essaie que des lignes interdites de 100 et 8 caractères (N-1 à
N-3 y sont équivalents), aucun journal exempté copié sous un nom neuf (N-4), aucun `[1m]` sur un identifiant hors liste
(N-5), et elle lit l'aide de l'outil sans faire analyser la commande (N-6). Échantillon rejoué : 8 mutants du
générateur, 8 tués. Recompte des journaux du générateur : A 12/12, E 5/5, B 7/7, C 4/4 tués ; un processus étranger
au lot reste dans le relevé de E, comme le générateur l'a déclaré.

### (3) Gates (tête seule et tête + série, clones creux locaux, réseau coupé, sans la variable interdite)

| gate | tête `0cfbe3e` | tête + série |
|---|---|---|
| runner `run-fixtures-verdict-suite-s2.py` | 136 ok, 0 échec | 137 ok, 0 échec |
| s2-harness `--egal` | conforme, Ran = 415 | conforme, Ran = 415 |
| s2bis `--plancher 341` | conforme, Ran = 341 | conforme, Ran = 341 |
| sim-bis `--plancher 268` (clone git) | conforme, Ran = 268 | conforme, Ran = 268 |
| calib-actifs `--plancher 65` | conforme, Ran = 65 | conforme, Ran = 65 |
| controle-unittest `--egal --plancher 16` | n/a | conforme, Ran = 16 (exact) |
| g1 : cas du lint, lint R-1, `journaux-modele.py .` | 227 ok ; OK 7 fichiers ; n/a | 227 ok ; OK 7 fichiers ; conforme, 52 exemptés |
| hooks (`run-fixtures-hooks.sh`) | 54 ok | 54 ok |
| G5, motif du job (octets contrôlés : `cmp` avec la ligne 72 de `gates.yml`) | `git grep` sortie 1, 0 marqueur | sortie 1, 0 marqueur (12 fichiers du lot indexés) |
| G3 secrets, mode indexé, et cas | n/a | OK, 11 fichiers ; cas 147 ok |
| xtask (lignes VERDICT seules) | 8 VERT, 1 ROUGE, global ROUGE | identiques (`cmp`) |

Les modes `--tree` et `--history` de G3 ne sont pas lancés : ils liraient les blobs exclus du clone. Pour G5, le
`git grep` exclut les chemins interdits par pathspec.

### (4) Forme

R-25 : `git apply --numstat` donne A +199 −4, E +33 −12, B +189 −1, C +38 −1, D +2 −0, tous sous 200. Avec les
corrections : E +46, B +192 (C-2), C +58 (C-3, C-7) ; C-4 et C-5 vont en DT3-F, voir C-5. Aucun `TODO` ni `FIXME`,
aucun octet 92 dans les lignes ajoutées. Longueur des lignes : voir O-4.

### (5) DT3-D

L'ajout est daté, avec 0 ligne retirée : aucune retouche du texte adjugé. Les chiffres sont recomptés. 3 168 =
somme `git show --numstat`, toutes voies, des 21 commits `1ed872c`…`19a0c7e` qui touchent `scripts/calib-actifs`
(22 avec `60fad53`, exclu ; 3 129 sous ce seul chemin). Ratios : 3168/1300 = 2,437 et 3168/1100 = 2,88. 998 et
« environ 560 » sont lus à `G2-P1A.md` l.389 (et l.83 pour le total de 998), soit 998/560 = 1,782. La règle n'en dépend
pas, comme l'adjudication le veut. Seule réserve : C-6.

### (6) Risques

- Contrôle des journaux sur un versement normal. Un journal nouveau versé sous `docs/G1-*.md` ou `docs/G2-*.md` doit
  porter exactement une ligne qui commence par la tête. J'ai essayé `RAPPORT-GENERATEUR.md` sous le nom
  `G1-lot-DETTES-T3.md` : conforme (1 ligne, sortie 0). Ce rapport porte aussi une seule ligne de cette tête. Les lots
  récents versent leurs pièces de revue sous `docs/adr-0029/…/revue-*/`, hors de la portée : aucun rouge. Le rouge à
  tort possible vient d'un ajout daté fait à un journal exempté : le journal perd son exemption. 34 journaux se
  réparent par l'ajout d'une ligne, 2 non (O-3), d'où C-5. Un journal qui citerait la ligne en début de ligne une
  seconde fois rougirait : c'est voulu (« une exigée »), et le message de refus le nomme.
- Sûreté de la consigne de `shogen-worker.md`. Elle ne pose jamais la variable : la commande commence par `env -u
  SHOGEN_S2_CAMPAGNE_CONTROL`, et l'outil consigne la variable sans jamais la poser (docstring l.5-6 ; `consigne` ne
  fait que lire `environ`). Elle renvoie à la règle d'usage de `s2-harness/tools/README.md`. Le lint R-1 est OK après C.
  Réserve d'exécutabilité : C-7.
- Erreur interne de `journaux-modele.py` classée comme un refus : C-4.

### (7) Règle « aucune dette »

Chaque constat corrigeable est une correction du lot (C-1 à C-9). Aucun item n'est formé. Le seul acte extérieur est
l'information de l'investisseur (O-1) : il appartient déjà à l'item, avec son déclencheur.

## Constats (O-n)

- **O-1** : SHOGEN-S2BIS-P1-ESTIMATION-1 demande aussi « l'information de l'investisseur » (déclencheur : prochain
  point d'étape). C'est un acte extérieur au diff. L'amendement de clôture doit dire s'il est fait ou s'il reste ouvert
  pour cette seule part, avec son déclencheur.
- **O-2** : la liste figée vaut, au nom et au sha256 près, l'ensemble des 52 journaux de HEAD (recalculé, `diff` vide).
- **O-3** : sans exemption, 16 des 52 journaux sont déjà conformes, 34 n'ont aucune ligne de cette tête, et 2
  (`G1-lot-DETTES-B2.md`, `G2-lot-DETTES-B2.md`) en ont une hors forme. Ces deux-là ne peuvent pas être réparés par un
  simple ajout.
- **O-4** : longueur des lignes. La consigne porte une ligne de 204 caractères, alors que la fiche ne dépassait pas 103.
  Cette ligne est la commande littérale, sur une seule ligne, que le test exige ; aucune règle de longueur n'est
  trouvée, donc pas de correction. `gates.yml` reçoit des lignes de 121 caractères, et en comptait déjà 5 au-delà de
  120 à la tête.
- **O-5** : aucun cas K ne lit l'étape g1 `journaux-modele.py`. Le même contrôle est pourtant exécuté par
  `test_arbre_du_depot` dans `controle-unittest`, lu par K-04 : pas d'angle mort, pas d'item.
- **O-6** : xtask est ROUGE à l'identique sur la tête seule et sur la série (une gate, 1 violation, sous les exclusions
  du clone). La série ne change aucun VERDICT. Le xtask VERT avant commit reste celui de l'orchestrateur sur le dépôt
  entier.
- **O-7** : la queue `v[-40:]` contiendrait un `\r` final si une ligne interdite finissait en CRLF. Ce n'est pas le
  cas : `.gitattributes` impose `* text=auto eol=lf`, et 610 fichiers des chemins permis sont `i/lf`. Le contrôle porte
  sur des fichiers permis seulement.
- **O-8** : le rouge de K-04 suit le contrat du runner (sortie 1), conformément à SHOGEN-MUT-FATAL-1. Les rouges de B
  passent par la sortie 2 de l'interpréteur (fichier absent), assertée par les tests : ce sont bien des AssertionError.

## Écarts du réviseur (E-G2-n)

- **E-G2-1** : pendant les gates de la série, `test_g2_limites.py` est resté une seconde environ dans
  `w/clone/scripts/controle/tests/`, puis a été retiré. Le run `controle-unittest`, lancé plus tard, donne Ran = 16 :
  aucun effet.
- **E-G2-2** : un fichier transitoire `/tmp/jm.<pid>`, hors de `g2/`, a été écrit puis retiré aussitôt. C'était une
  copie de `journaux-modele.py`, sans contenu de D.2.
- **E-G2-3** : les noms et sha256 d'EXEMPTES ont été lus par `eval` d'un littéral de dictionnaire du diff, sous
  `python3 -I` ; `ast.literal_eval` aurait suffi.
- **E-G2-4** : lectures ciblées hors des pièces du brief, toutes dans des chemins permis : `docs/adr-0028/CP2-S2.md`
  l.28-42 ; `s2-harness/tools/README.md` ; `G2-P1A.md` l.83 et l.389 ; `grep -l oracle_record` sur
  `docs/adr-0029/s2bis/revue-*/BRIEF*` (glob non récursif), puis les 2 lignes trouvées dans deux briefs G2 ;
  `git ls-files --eol` sur des chemins permis seulement. Aucune pièce de D.2 ouverte, aucun `*.jsonl` lu.

## Journal de provenance (G1)

Sources [lu] : `CLAUDE.md` ; `ADJUDICATION-G1.md` et `RAPPORT-GENERATEUR.md` en entier ; les 5 diffs en entier ;
`ANNEXE-B-items.md` l.515-525, 890-898, 1010-1018, 1362-1372, 1385-1395, 1490-1518 et les en-têtes de blocs ;
`G0-lot-D8a.md` l.186-200 et 418-428 ; `fm11.py` (tête) en entier ; `oracle_record.py` l.1-80, 100-135, 405-445 et ses
lignes de premier niveau ; `run-fixtures-verdict-suite-s2.py` l.548-625 ; `gates.yml` (jobs, lignes `run`, l.64-78) ;
`gate-secrets.sh` (en-tête) ; `CP2-S2.md` l.28-42 ; `s2-harness/tools/README.md` ; `G2-P1A.md` l.83 et l.389 ;
`.gitattributes` ; outils du générateur (`iso.sh`, `gates.sh`, `gates2.sh`, `mutants2.py`, `faire_diff.sh`,
`diff_etapes.sh`, `xtask*.sh`) ; journaux de mutants du générateur (verdicts recomptés). [abs] : aucune précédence
d'enregistrement de rôle G2 sur des diffs non commis (2 briefs G2 S2-bis citent `oracle_record` comme objet, non comme
commande).

Commandes (sorties sous `g2/sorties/`) :
- clone creux local `git clone --no-checkout` et `sparse-checkout` (exclusions du brief : 58 entrées sautées, 0
  `*.jsonl`), copie `tete`, puis la série appliquée sur `clone` ;
- `outils/gates.sh` sur les deux arbres (`serie-*.txt`, `tete-*.txt`, `*-codes.txt` : toutes les sorties à 0) ;
- `outils/xtask.sh` (`xtask-serie-VERDICT.txt`, `xtask-tete-VERDICT.txt`, `cmp` identiques ; sorties brutes non
  lues hors VERDICT) ;
- mutants : `mutants-g2.json` et `.txt` (série), `mutants-g2-corr.json` et `.txt` (copie corrigée) ;
- G5 (`g5-clone.txt`, `g5-tete.txt`, vides) et G3 (`g3-serie.txt`, `g3-cas-serie.txt`) ;
- rouges, copie corrigée et recomptes : commandes au fil de NOTES.md.

Chiffres recomptés : 52 journaux (noms et sha256) ; 16, 34 et 2 ; 71 sommes, 68 sorties, 71 OK ; 3 168, 3 129, 21 et
22 commits ; 2,437, 2,88 et 1,782 ; +199, +33, +189, +38 et +2 ; plancher 16, et 18 avec corrections ; mutants 8/8
rejoués, 6/6 neufs vivants contre la suite du lot et tués après corrections.

Outils du réviseur : `outils/iso.sh`, `gates.sh`, `xtask.sh`, `mutants_g2.py`, `corrections.py`, `motif-g5.txt`,
`tests_g2/test_g2_limites.py`. Ces fichiers sont dans `g2/` et ne sont pas à verser.
