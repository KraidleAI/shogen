# Relecture G2 neuve de SB-11x (transcrit)

> Transcription par l'orchestrateur le 2026-10-09 18:27:52 UTC du fichier g2/RAPPORT-G2.md ; contrôle FM-1.1 des transcripts de l'advisor (claude-fable-5-1), du générateur-correcteur, du réviseur et du contre-contrôleur (claude-opus-5-5), par le fm11.py versé et par celui de DETTES-T3 : fragments_l51_l14 = 0. Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# G2 neuve de SB-11x (SHOGEN-SIM-BIS-NPRIME-NUL-1) — rapport du réviseur, 2026-10-09, écrit à partir de 13:47 UTC

## 0. Gate 0
Modèle résolu : `claude-opus-5-5` (identifiant de l'environnement de l'agent), effort max, réviseur G2 neuf. Je n'ai écrit
ni l'AVIS, ni l'ADJUDICATION, ni SB-11a … w, ni SB-11x (réviseur ≠ générateur).

## 1. Verdict
**ACCEPTE-AVEC-CORRECTIONS.** Le code de SB-11x est conforme à l'adjudication (option (b)) : ma sonde, écrite avant la
lecture du diff, passe 237/237 sur l'arbre corrigé ; `regle.py`, `variante.py`, `calendrier.py`, `oracle_recalc.py`,
`test_regle.py` et `test_oracle_recalc.py` sont inchangés ; toutes les gates sont vertes. Les tests, en revanche, laissent
vivants 8 de mes 15 mutants. Ils les laissent passer parce que les paramètres sous étiquette n'ont pas, dans les
fixtures, de valeurs distinctes de leurs sources concurrentes : S vaut toujours absorption, le R de la cellule vaut le
R_approche du prm, n′ ne prend que 0 ou n_s, et l'égalité se fait en Python et non en octets JSON. Cette condition est
celle que pose le brief. Les corrections C-1 à C-6 forment une liste fermée. Je les ai démontrées : chacune a son test,
écrit et lancé (`propositions/test_nprime_g2.py`), et ses mutants, tués par la commande exacte du job.

### Corrections (liste fermée)
| id | correction | test | mutants tués (vivants avant) |
|---|---|---|---|
| C-1 | fixture à S et absorption opposés : (S vrai, absorption faux, variante [8]), puis (S faux, absorption vrai, variante [4]) | `test_etiquettes_croisees_et_octets` | G2-M04, G2-M05, G2-M06 |
| C-2 | R de la cellule égal tour à tour au R_approche (99) et au R (199) d'un prm où ils diffèrent ; C, r et C_S comparés | même test | G2-M08 |
| C-3 | source de « strate vide » : (a) 0 < n′_s < n_s/2 (T-imp, large, repli, W = 1, i = 65 : n′ de stress 650, suffisant faux) passe par la règle ; (b) n′ > 0 et `regle.premiere` rendue None (mock) : la règle est appelée dans les deux strates | `test_n_prime_partiel`, `test_premiere_absente` | G2-M01, G2-M03 |
| C-4 | égalité en octets JSON canoniques, `commun.json_canonique(executer.jsonable(·))`, entre l'enregistrement dégénéré et la référence `regle.tester`/`filtrer`/`variante.tester` sur séries vides à n = 1. L'égalité Python ne suffit pas : Fraction(0) == 0 | `test_etiquettes_croisees_et_octets` | G2-M12, G2-M13 |
| C-5 | plancher du job sim-bis relevé au compte réel (273 + tests ajoutés ; 276 avec mes trois tests), `--egal` ; voir la remarque R-25 ci-dessous | TEMOIN : conforme, Ran 276 | — |
| C-6 | RAPPORT-GENERATEUR §4 point 2 : retirer « toute valeur sous étiquette diffère de ses sources concurrentes ». La phrase est démentie par G2-M04/M05/M06/M08, vivants sous la suite livrée | — | — |

Remarque R-25 : SB-11x fait 176 ajouts et 8 retraits (numstat). Mes trois tests en ajoutent 66. Le tout dépasserait la
borne de 200 lignes. Je recommande donc de verser C-1 à C-5 dans un sous-lot SB-11y, avant E0, et de garder SB-11x tel
quel ; la décision revient à l'orchestrateur.

## 2. Constats
- **O-1 (majeure, tests ; corrigée par C-1 à C-4)** : 8 mutants vivants sur 15 sous la suite livrée, tous en sortie 0 et
  Ran 273. Ce sont M01, « vide » pris sur `not suffisant`, et M03, sur `prem is None` ; M04, M05 et M06, S et absorption
  croisés ; M08, C pris sur R_approche ; M12, indice entier 0, écrit 0 en JSON ; M13, S écrit Fraction(0), soit « "0" ». Le
  code livré est correct (sonde, gates). Le défaut tient au pouvoir de détection des tests. Sous M01, une strate où n′ est
  à la fois non nul et inférieur à n_s/2 perdrait sa statistique sans qu'un test le voie (n′ = 650 existe, T-imp i = 65).
- **O-2 (mineure, rapport G1 ; corrigée par C-6)** : l'affirmation du §4 point 2 du rapport du générateur est inexacte
  (O-1).
- **O-3 (mineure, texte G0 proposé)** : « indice = 0 » est ambigu. Le code écrit Fraction(0), sérialisé « "0" » comme tout
  indice de `regle.filtrer`, et S vaut l'entier 0 (`regle.paires`). Il faut l'écrire ainsi dans l'ajout daté.
- **O-4 (information, forme)** : la rangée `executer.py` du README fait 4 606 caractères (4 240 avant). **Admissible** :
  - c'est le format préexistant (tableau GFM, une rangée par ligne ; 8 rangées font déjà plus de 120 caractères avant le
    diff) ;
  - aucune gate ne borne la longueur des lignes Markdown ;
  - la borne de 120 caractères est tenue dans le code (executer.py : 120 au plus ; test_nprime.py : 119 au plus).
  La rangée grossit à chaque sous-lot ; une refonte du tableau peut être formée en item, sans blocage.
- **O-5 (information)** : la recette de l'AVIS (T-imp, i = 1) est juste ; je l'ai mesurée (`sonde/trouver.py`). Pour T-imp,
  grille large et repli, n′_stress vaut 0 à i ∈ {1, 5, 56} sur i ∈ [0, 140]. Ma fixture T-1 le donne à i = 2. Le cas est
  rare : aucun i pour « G2-NP » sur [0, 40] ∪ [200, 240].
- **O-6 (information, I-3)** : l'agrégat ne compte pas à part les réplications à n′_s = 0. La combinaison
  « unites+k_crit+runs+n_prime » mêle n′ = 0 et les n′ > 0 à 0 ou 1 unité en écart. Le compte se lit dans les
  enregistrements (`strates[s]["n"] == 0`), mais n'est pas imprimé ; à former en item (voir §7).
- **O-7 (information)** : `_vide` place S en dernière clé, alors que `_court` la place avant runs. C'est sans effet :
  `json_canonique` trie les clés et l'égalité de dict ignore l'ordre.

## 3. Sonde indépendante (écrite avant lecture du diff)
`sonde/sonde.py` (sha256 05bbfd37…0cac265, voir SHA256SUMS). Fixture : T-1, grille large, repli, W = 1, i = 2. Le prm a
R = 99 et R_approche = 199 ; la cellule a R = 199, classes BTC, ETH et USDT (sans USDC), S, absorption, variante [8],
evenements 3. Une seconde fixture minimale a R = 99, S faux, sans absorption, sans variante, classes BTC et USDC. Elle
couvre :
- les champs de chaque classe en stress : égaux à un littéral écrit à la main et à `regle.tester({}, …, n = 1, n_s)` pour
  n_s ∈ {3, 4, 7, 2 736} ; « avec » égal à `regle.filtrer({}, 1)` suivi de `tester` (indice de type Fraction) ;
  `variante[8]` égal à `variante.tester` à n_s ∈ {3, 2 736} (N = 0, pas de S) ;
- les clés : celles du calme, sans « evenements » ;
- les appels : aucun appel de regle ni de variante sur stress (espions sur tester, oracle, deux_modes, loi_evenements,
  filtrer), y compris sur le chemin i ≥ ORACLE (ORACLE ramené à 1) ;
- le calme : égal à `regle`/`variante` appelés à la main sur les séries recomposées ;
- les comptes de `frequences` et d'`agreger` : sur [rec]*3 (NON ÉVALUABLE 3, insuffisante 3, chaque cause 3, combinaison
  unique 3), en blocs sans, avec et variante ; et sur un mélange normal + dégénéré, dans les deux ordres ;
- le déterminisme : deux appels ; `ecrire_lot` deux fois ; `calculer_lot` en 1 contre 2 processus ; PYTHONHASHSEED 0
  contre 1 ;
- le contrat de regle : à n = 0, REGLE/entier pour tester, oracle, loi_evenements, filtrer et variante.tester.

Résultats :
- arbre d'avant : sortie 3, REGLE/entier ; refus reproduit (journal/sonde-avant.txt) ;
- arbre d'après : 237/237, sortie 0, empreinte f7599cb5…958f0 (journal/sonde-apres.txt).

Ma sonde avait les mêmes angles morts sur S/absorption, n′ partiel et le type de S (§5, colonne « sonde »). C-1 à C-4 sont
écrits pour les fermer.

## 4. Diff relu en entier (246 lignes, sha256 c86a4d9b…a73a1, SHA256SUMS du générateur : 51/51 OK)
- `executer._vide(p, rg)` rend les champs exigés par l'adjudication (pt 2) un à un : valeur VALEURS[2], causes
  `list(regle.CAUSES)`, C = r = R de la cellule, C1 = 0, C_S = R si S est suivie (sinon None), K = runs = unites = 0, S = 0
  ou None ; « avec » avec `retirees = []` et `indice = Fraction(0)` ; `variante[d]` sans S, avec C_S None et
  N = `variante.demi(0, d, p)` = 0.
- `replication` : `vide = n[s] == 0` par strate ; `_vide` remplace `_tester` ; la branche des événements est sautée.
  `regle.strate`, `retraits`, `premiere` (None) et `M` sont inchangés.
- `test_nprime.py` : 5 tests. Sous le code d'avant, 4 FAIL d'assertion (« refus REGLE/entier »), 0 ERROR ;
  `test_contrat_regle_inchange` est vert, comme attendu (journal/rouge-avant.txt).
- README, une rangée ; gates.yml, plancher 268 → 273.
- Les 24 diffs (SB-11e … w, puis x) s'appliquent sans rejet ; `git apply --whitespace=error-all` passe.

## 5. Mutants
Commande exacte du job : `python3 -B enforcement/verdict-suite-s2.py scripts/sim-bis --aucun-saut --egal --plancher
273`, réseau isolé (`isole.sh`), mandataires retirés, borne 300 s, `os.killpg` de la session, PAR = 2. Classement : sortie 1
= tué, 0 = vivant, toute autre sortie = FATAL. Copies `cp -al` de g2/apres, fichier muté réécrit par unlink. Pièces :
mut/campagne.txt, mut/campagne.out, mut/apres-*.txt.

| id | mutation | suite livrée (273) | avec C-1 à C-4 (276) | sonde |
|---|---|---|---|---|
| TEMOIN (début, fin) | aucune | VIVANT, Ran 273 (148 s, 172 s) | VIVANT, Ran 276 (160 s) | 235/235 |
| G2-M01 | vide = `not ret[s]["suffisant"]` (source) | **VIVANT** | TUÉ (test_n_prime_partiel) | vivant |
| G2-M02 | vide = `ret[s]["atteinte"] is None` (source) | TUÉ (test_replication ×2) | — | vivant |
| G2-M03 | vide = `prem is None` (source) | **VIVANT** | TUÉ (test_premiere_absente) | vivant |
| G2-M04 | « avec » sous `rg["S"]` (étiquette) | **VIVANT** | TUÉ | vivant |
| G2-M05 | S suivie lue sur absorption (étiquette) | **VIVANT** | TUÉ | vivant |
| G2-M06 | C_S de « avec » sous absorption (étiquette) | **VIVANT** | TUÉ | vivant |
| G2-M07 | diviseur du prm au lieu de ceux de la cellule (source) | TUÉ (forme, équivalence) | — | FATAL (non compté) |
| G2-M08 | C = R_approche du prm (un R pour l'autre) | **VIVANT** | TUÉ | tué |
| G2-M09 | r = R du prm (un R pour l'autre) | TUÉ | — | tué |
| G2-M10 | vide dès qu'une strate a n′ = 0 (une strate pour l'autre) | TUÉ (forme) | — | FATAL |
| G2-M11 | tout écrit sous la première classe à n′ = 0 (une classe pour l'autre) | TUÉ (forme, équivalence ; 2 ERROR) | — | FATAL |
| G2-M12 | indice entier 0 (JSON 0) | **VIVANT** | TUÉ | tué |
| G2-M13 | S = Fraction(0) (JSON « "0" ») | **VIVANT** | TUÉ | vivant |
| G2-M14 | retirees tuple | TUÉ | — | tué |
| G2-M15 | C_S de la variante sous S de la cellule | TUÉ | — | tué |

Bilan :
- suite livrée : 7 mutants tués sur 15, 8 vivants, 0 FATAL, durées de 156 à 178 s ;
- suite munie de C-1 à C-4 : les 8 vivants sont tués, par AssertionError seule (0 ERROR, 0 FATAL), et le témoin passe,
  Ran 276 (mut/campagne-c.txt) ;
- équivalents non comptés : N littéral 0 (`demi(0, d)` vaut 0 pour tout diviseur admis) ; échange de deux champs nuls ;
  `not segs` ou `not ret[s]["masque"]`, équivalents à n′ = 0 ;
- la campagne du générateur (M-NP-01 à M-NP-15, 15/15) n'est pas recomptée ici. Ses mutants recoupent les miens sur C = 0,
  n′ de stress/calme, R du prm, avec/variante omis.

## 6. Gates (copie g2/apres = tête aec672e + SB-11e … w + SB-11x ; journal/gates.txt, pid 1264)
| étape | résultat |
|---|---|
| runner `run-fixtures-verdict-suite-s2.py` | 136 ok, 0 échec (7 s) |
| sim-bis (plancher 273, `--egal`) | conforme, Ran 273 (151 s) |
| s2bis (plancher 340) | conforme, Ran 340 (35 s) |
| S2 (`--egal`, 415) | conforme, Ran 415, 2 sauts nommant la variable (61 s) |
| matrice `-X dev -W error` 3.10 / 3.11 / 3.12 / 3.13 | code 0, Ran 273, OK (198 / 166 / 157 / 157 s) ; 0 « Exception ignored », 0 « Warning » |
| xtask verify, après et avant | code 0 ; 10 lignes VERDICT identiques (9 VERT + global VERT) ; seules les lignes VERDICT gardées |

Forme :
- R-25 : 176 ajouts et 8 retraits, sous 200 ;
- R-13 : 0 TODO ni FIXME ;
- octets 92 : 0 dans le diff, 0 dans executer.py, test_nprime.py et README ; les 4 de gates.yml préexistent, non touchés ;
- lignes Python de 120 caractères au plus ; README : voir O-4.

Fichiers inchangés, sha256 recomptés : regle.py 5875ccbd, variante.py 3906f1f6, calendrier.py 9fecdca0, oracle_recalc.py
a5805ffa, test_regle.py 3cf99c66, test_oracle_recalc.py 48732980, parametres.json et test_commun.py (cmp avant/après).
Ces valeurs sont égales à celles du rapport du générateur.

## 7. Avis sur les items du générateur
- **I-1 (empreinte du G0) — d'accord, procédure exacte proposée** (`outils/epingles_g0.py`, démontrée sur une copie
  jetable) :
  1. Figer l'ajout daté dans `docs/adr-0029/g0-sim/G0-SIM-BIS.md`, `date -u` lue, puis mesurer `sha256sum` : c'est
     NEUVE.
  2. Dans `scripts/sim-bis/parametres.json`, remplacer en texte, à une seule occurrence et sans `json.dump`, qui réécrirait
     tout le fichier, la tête « (sha256 a216a953…, mesurée par sha256sum sur la version figée par l'orchestrateur, ajout
     daté PLAN-S2BIS-2 du 2026-10-05 15:05:43 UTC compris : » par « (sha256 NEUVE, mesurée par sha256sum sur la version
     figée par l'orchestrateur, ajout daté NPRIME-NUL-1 du 2026-10-09 HH:MM:SS UTC compris (strate à n′_s = 0,
     SHOGEN-SIM-BIS-NPRIME-NUL-1) ; avant l'ajout daté NPRIME-NUL-1 du 2026-10-09 HH:MM:SS UTC :
     a216a953ba2be088868967e8b11a89c17e3882cee9da581700f88d3b70d0e11e, ajout daté PLAN-S2BIS-2 du 2026-10-05 15:05:43 UTC
     compris : ». La suite de la chaîne reste intacte : « avant l'ajout daté PLAN-S2BIS-2 … : d9cffc0a… », puis « avant
     cet ajout : eeaceb6b… ». Le diff de parametres.json est d'une seule ligne (l.4), et le JSON est relu sans erreur.
  3. Dans `scripts/sim-bis/tests/test_commun.py`, `test_provenance_c_5` :
     - l.61-62 : `g0` reçoit NEUVE ;
     - ajouter en tête de la liste des maillons « avant l'ajout daté NPRIME-NUL-1 du 2026-10-09 HH:MM:SS UTC : »
       suivi de « a216a953… », sur deux littéraux pour tenir 120 caractères ;
     - `[True, True]` devient `[True, True, True]` ;
     - la docstring nomme le mutant « ancienne épingle remise ».
     Aucun test n'est ajouté : le plancher reste celui du job (273, ou 276 avec C-1 à C-4).
  4. G0, parametres.json et test_commun.py vont dans **un seul commit** : `test_g0_mesure`, le fil d'alarme de SB-14H,
     rougit si G0 et épingle sont commités séparément. Il peut s'agir du commit de SB-11x lui-même. Contrôles mesurés sur
     la copie : test_commun vert (22 tests) ; ancienne épingle remise : 2 FAIL (test_g0_mesure, test_provenance_c_5) ; G0
     augmenté d'un octet : 1 FAIL (test_g0_mesure).
  5. Le sha256 de parametres.json change, mais aucune épingle de ce fichier n'existe dans scripts/, s2bis/,
     enforcement/, .github/, s2-harness/ ni xtask/ (grep du sha et de son préfixe) : test_parametres_du_lot le mesure
     lui-même. Limite : docs/ n'a pas été fouillé, la recherche récursive y est interdite ; c'est à l'orchestrateur de le
     confirmer. Aucun lot n'existe avant E0, donc aucune entête de lot n'est touchée.
- **I-2 (oracle d'E-S-29) — d'accord.** À écrire au G0 : le sous-ensemble pré-déclaré reste les 200 premières
  réplications, et le nombre de comparaisons effectives est 200 × strates moins les strates à n′ = 0. Je suggère de
  l'imprimer au paquet par cellule ; c'est déductible des enregistrements.
- **I-3 (taux d'information insuffisante) — d'accord, avec un complément (O-6).** Imprimer au paquet, par cellule et par
  strate, le nombre de réplications à n′_s = 0, à côté de la combinaison « unites+k_crit+runs+n_prime », qui mêle n′ = 0
  et n′ > 0 avec 0 ou 1 unité. C'est un item à former (proposition : SHOGEN-SIM-BIS-NPRIME-NUL-COMPTE-1), hors de
  l'adjudication de ce lot.

Texte G0 proposé par le générateur (§9) : je n'ai pas d'objection de fond, seulement O-3 (« indice = Fraction 0, écrit
"0" ; S entier 0 »).

## 8. Écarts du réviseur
- **E-1** : j'ai fait `git init` avec alternates vers /home/user/shogen/.git/objects, en lecture, dans mes copies seulement
  (g2/avant, g2/apres, les copies `cp -al` des mutants, la copie jetable i1). oracle_r1 et oracle_recalc en ont besoin,
  parce qu'ils lisent par `git archive`. Le dépôt réel n'a reçu aucune écriture, et toutes mes commandes git sur lui
  portaient `--no-optional-locks`.
- **E-2** : sur la copie i1, les contrôles de mutation de test_commun ont tourné hors `isole.sh`. Ces tests n'ouvrent aucun
  réseau ; le premier passage, lui, était sous `unshare -n`.
- **E-3** : un premier passage de la sonde sur les mutants, dans une copie hors arbre, est INVALIDE : RACINE était
  introuvable, et l'exit 1 d'import avait été compté « tué ». Il est conservé (journal/sonde-mutants-INVALIDE.txt) et
  non compté. Je l'ai refait dans l'arbre, la ligne BILAN étant exigée pour classer un run.
- **E-4** : le PID du maître de la seconde campagne a d'abord été mal relevé (13253, le pgrep lui-même). Le vrai est 13234 ;
  la correction est consignée dans NOTES.md.
- **E-5** : le journal du premier TEMOIN a été écrasé par celui du TEMOIN de fin. Les deux résultats restent dans
  mut/campagne.txt et mut/campagne.out.
- **E-6** : la tête du dépôt est passée de aec672e (SB-11d) à a75588d (SB-11o) pendant la revue. J'ai contrôlé que a75588d
  égale aec672e + SB-11e … o (diff -r vide), et que seuls scripts/sim-bis et gates.yml diffèrent. Ma base reste valide
  pour SB-11x.
- **E-7** : la machine était partagée avec la chaîne de commits et un autre agent. Toutes les durées sont restées sous la
  borne, et un seul processus lourd a tourné à la fois de mon côté : une campagne PAR = 2 compte pour un.

## 9. Journal de provenance (G1)
- Lu [lu] : ADJUDICATION.md (28ff0c90), AVIS.md (2024f275), PROPOSITION.md l.182, l.209, l.221 (0e78afab…),
  regle.py, variante.py, executer.py (arbre d'avant), test_replication.py (tête de fichier), test_impressions.py (CEL),
  test_commun.py l.30-81, verdict-suite-s2.py (en-tête), gates.yml (lignes des jobs), RAPPORT-GENERATEUR.md (comme
  donnée), SB-11x.diff en entier.
- Commandes et sorties : voir NOTES.md, horodatées. Pièces : journal/ (sonde-avant, sonde-apres, sonde-mutants,
  rouge-avant, gates.txt, g-*.txt, xtask-apres/avant) et mut/ (campagne.txt, campagne-c.txt, *.out, journaux par
  mutant).
- Chiffres recomptés par moi : Ran 273/276/340/415, 136, comptes de mutants, sha256 des fichiers inchangés, numstat,
  octets 92, longueurs de lignes, n′ par i (trouver.py).
- Aucune pièce D.2 ni lecture interdite ouverte ; SHOGEN_S2_CAMPAGNE_CONTROL jamais posée ; aucune clé ni secret.
