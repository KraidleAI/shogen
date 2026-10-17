# Rapport de l'intégrateur de P2 (rebasage, corrections, CB-16, formes du témoin, capture) (transcrit)

> Transcription par l'orchestrateur le 2026-10-17 22:35:44 UTC du fichier s2bis/int-p2/RAPPORT-INTEGRATEUR.md ; contrôle FM-1.1 du transcript du intégrateur par le fm11.py versé : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5 (516 occurrences, aucune autre). Texte ci-dessous avec 13 retouche(s) (E35, E38) : noms de marqueur de dette et locutions de la gate S-G4 cités en clair, mis en code, segments de code à doubles accents graves réécrits en segments simples, heures sans date dans les 25 caractères ou approchées mises en code ou entre guillemets français, sans autre changement (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Rapport de l'intégrateur : lot INT-P2 (S2-bis, partie P2 du collecteur : tranches C et D, corrections, CB-16)

**Gate 0 : `claude-opus-5-5`** (effort `high`), identifiant exact du modèle qui tourne ; intégrateur neuf (ni
générateur de P2C, ni de P2D).

Dates (`date -u`) : ouverture 2026-10-17 12:07:38 UTC ; contrôles finals achevés à `15:50:14` UTC (16 pas : `16:46:25` UTC, §11). Base : extraction
`git archive` de **2a07ae6** (`2a07ae6f2baecc662b3eda9594fdeee50c296e6a`, égale au brief et à la tête du dépôt réel,
inchangée à la clôture, état propre sur les chemins touchés), exclusions du brief. Dépôt réel en lecture seule : aucune
écriture git, aucun verrou (`--no-optional-locks`). Je livre une série unique de 14 diffs à adjuger,
`diffs/INT-P2-01.diff` à `INT-P2-14.diff`, applicable dans l'ordre sur 2a07ae6.

## 1. Table des pas

| id | sujet | code ajouté (`.py`, `.yml`) | plancher s2bis | mutants (tués / joués) |
|---|---|---|---|---|
| INT-P2-01 | CB-7a (P2C, à l'octet) | 117 | 375 | du générateur, non rejoués |
| INT-P2-02 | CB-7b (P2C, à l'octet) | 108 | 379 | idem |
| INT-P2-03 | CB-7c (P2C, à l'octet) | 17 | 380 | idem |
| INT-P2-04 | CB-8a (P2C, à l'octet) | 120 | 386 | idem |
| INT-P2-05 | CB-8b (P2C, à l'octet) | 59 | 388 | idem |
| INT-P2-06 | CB-8c (P2C, à l'octet) | 115 | 394 | idem |
| INT-P2-07 | CB-9a rebasé | 189 | 400 | du générateur (sur 2a07ae6), non rejoués |
| INT-P2-08 | CB-9b rebasé | 59 | 404 | idem |
| INT-P2-09 | CB-9c rebasé | 163 | 410 | idem |
| INT-P2-10 | C-P2D-1, classe `temoin` | 54 | 413 | 14 / 14 |
| INT-P2-11 | C-P2D-2, limites de la lecture Curve | 30 | 415 | 12 / 12 |
| INT-P2-12 | C-P2C-1, `Bornes` sans temps réel | 50 | 416 | 10 / 10 |
| INT-P2-13 | CB-16a, smoke sans prix | 178 | 420 | 17 / 17 |
| INT-P2-14 | CB-16b, commande `smoke`, FORMAT §18 | 93 | 422 | 13 / 13 |

Compte de R-25 par `outils/compte.py` (lignes ajoutées des `.py` et `.yml`, docstrings comprises) : 17 à 189, toutes
sous 200. Hors compte : fixtures `.bin`, `formes-pool.json`, FORMAT, METRIQUES, G6. Chaque diff porte sa section de
METRIQUES et le hunk de son plancher (`--egal`). `pas.tsv` (`id`, `sujet`, `n_tests` = plancher) et `source-pas.md`
(ce que porte chaque pas, d'où il vient, sha256 des diffs d'origine) servent aux messages de la chaîne.

## 2. Pas 1 : P2C telle quelle

Les six diffs de `s2bis/p2c/diffs/` (sha256 égaux à leur `SHA256SUMS`) sont copiés à l'octet (`cmp`) en INT-P2-01 à
06 ; chacun s'applique (`git apply --whitespace=error-all`, code 0) sur l'état précédent. Aucun n'a été réécrit.

## 3. Pas 2 : P2D rebasée, conflits et résolution

Méthode : fusion à trois par fichier (`git merge-file`, hors dépôt ; `outils/rebase.sh`) : nôtre = arbre intégré,
base = état P2D d'avant le diff, leur = état P2D d'après (états P2D régénérés depuis ses diffs, égaux à ses mini-arbres
figés). Résolutions écrites par script (`outils/resoudre_9a.py`, `_9b`, `_9c`, `semantique_9a.py`, `_9b`) ; écart de
contenu contrôlé ligne à ligne contre les diffs de P2D (`preuves/compare-rebase-CB-9{a,b,c}.txt`) : seuls diffèrent
les hunks en conflit et les deux tests à listes fermées ci-dessous.

| pas | conflit | résolution |
|---|---|---|
| 07 (CB-9a) | `test_decodeurs.py` l.52 | même changement dans les deux séries : fusionné seul, absent du pas |
| 07 | docstring de `decodeurs.py` | docstring de P2C, puis la phrase de CB-9a (mêmes mots, recoupée à 120) |
| 07 | table `DECODEURS` | bloc du témoin de CB-9a (`D_USDC` à `CORPS`) avant `H, P`, `CG` et la table de P2C ; les deux entrées du témoin en fin de table |
| 07 | plancher | 394 + 6 = 400 |
| 07 | METRIQUES | section de CB-9a après celles de P2C ; comptes relevés, plancher 400, phrase du rebasage |
| 07 (sens) | `test_paires_absentes_sans_decodeur` (P2C) | il refusait tout décodeur OKX d'actif USDC ; OKX `USDC-USDT` (témoin) n'est pas la paire non servie USDC/USD : condition lue sur la paire `(USDC, USD)` |
| 07, 08 (sens) | `test_requete_btc_de_s2_gardee` (P2C) | liste fermée des décodeurs sans forme dans `formes-pool.json` : `okx_usdc_usdt`, `uniswap_usdc_usdt` (07), `curve_usdc_usdt` (08) ajoutés (question Q-1) |
| 08 (CB-9b) | docstring, `_curve` et CORPS | phrase de CB-9b après celle de CB-9a ; `_curve` et le CORPS à deux entrées avant `H, P` ; plancher 404 |
| 09 (CB-9c) | docstring | phrase de CB-9c après celle de CB-9b |
| 09 | FORMAT, puces de l'en-tête | puce « tranche D » après la puce « tranche C » |
| 09 | FORMAT §14.1 | règles `corps-du-decodeur` et `rpc-par-unite` après « §9.1). », puis la phrase des formes du pool de CB-8c |
| 09 | plancher, METRIQUES | 404 + 6 = 410 ; section relevée |

`entree.py`, `test_format.py` (test de CB-9c) et `test_temoin.py` fusionnent sans conflit ; le contenu de CB-9 hors
de ces hunks est celui de P2D. Rouges et mutants de CB-9 : ceux du générateur, sur 2a07ae6, non rejoués (brief).

## 4. Corrections posées

- **C-P2D-1** (INT-P2-10) : classe `temoin` pour les trois lectures du témoin (table `DECODEURS`, `CLASSES`) ; le
  recalcul la tient hors du vote : `config_analyse.TEMOIN`, refus nommé `ANALYSE/temoin` d'une classe `temoin` dans
  `tau_sigma` (avant le refus générique `ANALYSE/classe`), hors `PLANCHERS` et `SIGMA_BTC` ; test nommé
  `test_config_analyse.Temoin.test_classe_temoin_refusee_hors_du_vote` ; FORMAT §9.1 (liste des classes ; puce du
  témoin : la classe n'est plus « rendue en question ») ; `test_bout_en_bout` lit la liste des classes du FORMAT.
- **C-P2D-2** (INT-P2-11) : sens lu de `get_dy` et les trois limites, mot pour mot, dans la docstring de `_curve` et au
  FORMAT §9.1 : identité de la source `master` avec le bytecode déployé non vérifiée ; rattachement direct du pool NG
  à sa fabrique non lu ; absence du bogue d'oracle du pool NG non vérifiée sur chaîne (pool créé après la correction
  d'après l'API, inféré).
- **C-P2C-1** (INT-P2-12) : `test_decodeurs.Bornes` sans mesure de temps : `_entier` enveloppé, chaque valeur hors
  bornes doit donner la panne et une seule note, le refus de borne ; un décodeur qui convertirait sans `_entier` ne
  laisse aucune note. Test neuf `test_aucune_horloge_dans_la_classe` (AST de la classe : aucune horloge nommée).
  Preuves : l'ancien test échoue sous une horloge monotone truquée (+0,2 s par lecture, `outils/horloge_lente.py`) :
  6 FAIL ; le nouveau y passe ; le test neuf échoue sur l'ancien (1 FAIL) ; **rejoué dix fois pendant la campagne de
  mutants m12 (mutant M12-01 en cours, `mutants.py` PID 3662) : dix verts** (`preuves/bornes-final-dix.txt`). Charge
  réelle : l'ancien test rejoué dix fois pendant la campagne m10 est resté vert : la charge d'une campagne ne suffit
  pas à reproduire I-1, d'où la preuve par horloge truquée et par l'AST.

## 5. CB-16, smoke sans prix (INT-P2-13, INT-P2-14)

`collecte/smoke.py` (`jouer`, `role`, `ligne`, `CRYPTOCOMPARE`) et la commande
`python3 -m shogen_s2bis.collecte smoke --formes F [--carte C]` (`entree._smoke`) : `formes.json` (pool et témoin) et
`carte.json` contrôlés par leurs schémas, leurs règles et les règles croisées ; une lecture de chaque forme du pool et
du témoin (délai de `formes.json`), puis de la carte (délai de `carte.json`), en série, décodée par le décodeur de sa
forme ; une seconde avant une nouvelle lecture d'un hôte à `espace` vrai ; puis CryptoCompare (URL de S2), 401
re-confirmé. Ligne : `<rôle> <forme> <hôte> <statut> <code ou -> <sous-type ou -> <latence> ms décodable oui|non`,
rôle `temoin` par la classe `temoin` (C-P2D-1). Aucun prix, aucune valeur décodée, aucun octet du corps. Code 0 si et
seulement si toutes les formes du pool et du témoin décodent ; 1 sinon ; 2 refus de configuration. Lecture HTTP
(`lire`), pause et sortie injectables ; tests sur fixtures, `http.lire` remplacé, aucune opération réseau. FORMAT §18.
Le test `test_sortie_sans_aucun_prix_et_code_0_si_tout_decode` prend les 13 prix des fixtures par le décodeur seul et
exige qu'aucun ne figure dans la sortie : le mutant qui imprime le prix (M13-01, valeurs décodées dans la ligne) et
celui qui imprime les octets du corps (M13-02) sont tués.

## 6. Vérifications

Toutes hors du dépôt, réseau isolé (`unshare -n`, boucle locale allumée : `s2bis/p1b/g2/travail/outils/isole.sh`),
`SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée (ôtée de l'environnement), `TMPDIR` dédié sous ce dossier. Un seul
processus lourd à la fois (campagnes et contrôles finals lancés détachés, `setsid nohup`, fin constatée sur leur
journal) ; seuls des essais de modules de moins de 15 s ont tourné pendant une campagne.

- **Tests d'abord, rouges** (0 ERROR à chaque fois) : INT-P2-10 9 FAIL (`preuves/rouge-10.txt`) ; INT-P2-11 2 FAIL
  (`rouge-11.txt`) ; INT-P2-12 : ancien `Bornes` sous horloge truquée 6 FAIL (`horloge-lente-avant.txt`), test neuf sur
  l'ancien 1 FAIL (`rouge-12b.txt`) ; INT-P2-13 sur squelette d'interface 9 FAIL (`rouge-13.txt`) ; INT-P2-14 sur
  squelette 2 FAIL (`rouge-14.txt`).
- **Mutants** (`scripts/controle/mutants.py` d'une extraction de 2a07ae6, à part de la copie mutée, sha256
  `3e21878363ad7a106357abb666c3d8c5351f8ac94fcf3d95c4e64400abddad64` ; job `s2bis-unittest` : le runner puis la ligne
  s2bis de `gates.yml` telle qu'écrite ; borne 300 s ; tué = sortie 1 ; témoin vivant d'abord ; relevé `ps` de fin vide
  à chaque campagne) : m10 14/14, m11 12/12, m12 10/10, m13 17/17, m14 13/13, soit **66 mutants, 66 tués, tous par leur
  test visé, 0 vivant, 0 FATAL** (`mutants/<m>.txt`, `.bilan.txt`, diff et sortie de chaque mutant sous `mutants/<m>/`).
  Sites d'appel et étiquettes : décodeur de la forme et non son nom (M13-15 ; noms de forme ≠ décodeurs dans les
  tests), délais du pool et de la carte distincts (3 s et 7 s ; 0,3 s et 0,25 s : M13-09, M14-02), hôte lu deux fois
  sans `espace` pour séparer l'espacement (M13-08), sites d'appel de `_entier` dans chaque décodeur (M12-05 à 09).
- **Planchers par état** (`preuves/fin.log`, `job-final-s<k>.log`) : la commande du job est conforme à chacun des 14
  états, arbre neuf (extraction de 2a07ae6 et fichiers figés de l'état) : 375, 379, 380, 386, 388, 394, 400, 404, 410,
  413, 415, 416, 420, 422 ; runner 153 ok à chaque fois.
- **Série** rejouée depuis une extraction neuve de 2a07ae6 (`git apply --whitespace=error-all`) : code 0 aux 14 diffs,
  0 écart à chaque état ; `diff -r -q` de l'arbre de la série et de l'arbre final : vide (`preuves/diff-r-serie-travail.txt`,
  à `14:11` contre l'arbre de travail, à `15:39` contre l'arbre final reconstruit).
- **Arbre final** (`preuves/final-*.txt`) : runner `153 ok, 0 échec` ; s2bis `conforme … Ran = 422` ; S2 (`--egal`)
  `conforme (… sauts nommant SHOGEN_S2_CAMPAGNE_CONTROL, Ran = 423)` ; sim-bis `conforme … Ran = 279` (objets git du
  dépôt réel lus par `GIT_DIR`, sans verrou) ; aucun `__pycache__` sous `s2bis/`, `s2-harness/`, `scripts/sim-bis/`,
  `enforcement/` (`preuves/pycache-final.txt`).
- **Matrice 3.10 à 3.13** (`-I -B -X dev -W error`) : `Ran 422`, `OK`, 0 ligne `Warning`, 0 ligne `Exception ignored`
  sous chaque version ; la ligne du job est conforme sous chacune (`preuves/final-dev-python3.1x.txt`,
  `final-job-python3.1x.txt`).
- **`cargo --locked xtask verify`** (cible cargo par défaut de chaque arbre, aucun `CARGO_TARGET_DIR` ; lignes de
  verdict seules, `preuves/xtask-{final,temoin}-verdicts.txt`) : arbre final et témoin (extraction neuve de 2a07ae6)
  identiques (`cmp`) : S-G1 à S-G8, fmt, no_std, clippy VERT ; S-G9 ROUGE d'une violation des deux côtés (renvoi de
  `docs/17-modele-de-menace.md` l.70 vers `docs/rapports/`, exclu des copies : connu) ; sortie brute non lue.
- **Forme** (`outils/forme.py` sur les 14 diffs) : aucune ligne ajoutée de plus de 120 caractères (hors tableaux `.md`
  et données) ; 0 marqueur R-13 ; octet 92 : 88 dans `formes-pool.json` (P2C), 18 dans `test_temoin.py` (P2D : `\r\n`
  des octets HTTP attendus), 1 dans `test_smoke.py` (jointure des lignes par saut de ligne, octets contrôlés par
  `od -c`) ; bibliothèque standard seule (R-8) ; aucun flottant ajouté (prix et instants en Decimal et en entiers).
- Dépôt réel : HEAD `2a07ae6f2baecc662b3eda9594fdeee50c296e6a` à l'ouverture et à `15:50` UTC, `git status --short`
  vide sur les chemins touchés.

## 7. Questions rendues à l'orchestrateur

- **Q-1 (formes du témoin).** `s2bis/config/formes-pool.json` (P2C) n'a aucune forme du témoin ; deux tests de P2C à
  listes fermées l'ont révélé au rebasage, et je n'ai fait qu'y nommer les trois décodeurs du témoin. Le smoke ne joue
  que les formes qu'on lui donne : sans elles, le smoke du pool réel ne lit pas le témoin (E-C-37). Faut-il verser les
  trois formes (OKX `USDC-USDT` sur `www.okx.com` ; Uniswap sur `eth.drpc.org` et Curve sur `rpc.mevblocker.io`,
  Q-CA-10, corps de `decodeurs.CORPS`) dans `formes-pool.json` maintenant (un diff de données et de tests : 33 formes,
  OKX à cinq lectures, budget déjà compté par `test_lectures_par_hote_et_budget`), ou à la fusion dans `formes.json`
  au gel ?
- **Q-2 (CryptoCompare au smoke).** E-C-37 demande le 401 re-confirmé ; je l'imprime (`attendu 401 : OK|ÉCART`) sans
  changer le code de sortie, comme S2 (`s2-harness/shogen_s2/smoke.py`). Un écart doit-il faire échouer le smoke ?
- **Q-3 (tests de P2C ouverts au témoin).** `test_paires_absentes_sans_decodeur` admet désormais un décodeur OKX
  d'actif USDC coté en USDT (la condition vise la paire USDC/USD, celle de sa docstring) ; `test_bout_en_bout` admet la
  classe `temoin` (liste du FORMAT §9.1). À confirmer.
- **Q-4 (forme du smoke).** Lectures en série dans l'ordre des fichiers, une seconde avant toute nouvelle lecture d'un
  hôte à `espace` vrai, sans le plan de la boucle ; règles croisées appliquées si `--carte` est donnée ; `--carte`
  facultative. À confirmer.
- **Q-5 (commande de capture).** La capture des octets (AVIS Q-C-05 : commande séparée, qui n'imprime rien) n'est pas
  dans CB-16 ; elle est l'entrée de SHOGEN-S2BIS-FORMES-DOC-1, de SHOGEN-S2BIS-TEMOIN-BLOC-1 et de
  SHOGEN-S2BIS-OKX-CARNET-VIDE-1 (déclencheur « smoke CB-16 (capture) »). Sous-lot à former ?
- **Q-6 (planchers de la chaîne).** Pour satisfaire `preparer-p2.sh` (un hunk de plancher par diff), INT-P2-12 porte un
  test neuf (E-2). Si l'orchestrateur préfère un diff de test seul sans plancher, retirer ce test rend les planchers
  415, 419, 421 aux pas 12 à 14 et lève l'exigence du script pour ce pas.

## 8. Items de l'annexe B (recherche de `CB-16` et de `smoke` dans `docs/adr-0028/ANNEXE-B-items.md` seul)

- **SHOGEN-S2BIS-CURVE-DOC-1** : limites déclarées par INT-P2-11 (docstring et FORMAT) ; fermé avec elles au
  versement, selon l'adjudication de la tranche D.
- **SHOGEN-S2BIS-TLS-REUSSI-1** (l.1052, déclencheur « smoke CB-16 (poignée réelle) ») : **rendu, non fermé** : le
  smoke existe et lit par `http.lire` sous le contexte TLS réel (`http.CONTEXTE` par défaut), mais la poignée réelle
  demande le réseau, interdit au lot : à fermer au premier smoke réel d'un observateur.
- **SHOGEN-S2BIS-BINANCE-HOTE-1** (l.1273) et **SHOGEN-S2BIS-TEMOIN-RPC-1** (l.1274) : le smoke de chaque observateur
  en est l'outil ; inchangés (réseau).
- I-1 de P2C (test `Bornes` sensible à la charge) : levé par C-P2C-1 (pas d'item, adjudication de la tranche C).
- Aucune limite neuve hors des questions ci-dessus.

## 9. Écarts au brief et incidents

- **E-1 (lignes longues recoupées après campagne).** Mes remplacements ont écrit des lignes de plus de 120 caractères
  (FORMAT §9.1, `test_format`, `test_bout_en_bout` en INT-P2-10 ; docstring de `_curve` en INT-P2-11 ; docstring de
  `smoke.py` en INT-P2-13 ; import d'`entree.py` avant sa campagne). Recoupées après les campagnes m10, m11, m13
  (`outils/reformer.py`, `reformer_smoke.py`) ; équivalence aux blancs près contrôlée (AST aux chaînes ramenées à leurs
  mots pour les `.py`, mots pour les `.md` : `preuves/equivalence-forme.txt`, `equivalence-campagne-s13.txt`, 0 écart ;
  les tests du FORMAT et de la docstring comparent aux blancs près) ; copies d'avant : `etats-avant-forme/`.
- **E-2 (plancher de INT-P2-12, test ajouté après coup).** Le script de chaîne posé dans ce dossier par l'orchestrateur
  (`preparer-p2.sh`, lu seulement) exige un hunk de plancher dans chaque diff ; INT-P2-12 n'en portait pas. J'y ai
  ajouté un test neuf (`test_aucune_horloge_dans_la_classe`), d'où les planchers 416, 420, 422 aux pas 12 à 14 ; les
  campagnes m12, m13, m14 ont été rejouées sur ces octets (premières passes `mutants/m1x-v1*`, valides sur les octets
  d'avant, non comptées ; copies d'avant : `etats-avant-12b/`).
- **E-3 (relance de campagne invalide).** À `14:26:53`, la relance des trois campagnes a échoué (sortie 2 de l'outil :
  `mutants.py` absent, la copie de base qui le portait ayant été effacée à `14:22`) ; runs invalides gardés sous
  `mutants/invalides/`, non comptés ; outil ré-extrait (`outil/`, effacé à la fin) ; relance à `14:35:23`. Une boucle
  d'attente restée en fond a été tuée (PID 24567), comme une commande de contrôle mal formée à `13:03` (`faire_diff.sh`
  vers `/dev/stdout`, PID 19962 et 20016) et le premier `fin.sh` de `15:24:23` (il comparait la série à un arbre effacé).
- **E-4 (empreintes et heures écrites de mémoire).** Un premier jet de `source-pas.md` portait des sha256 abrégés écrits
  de mémoire, dont un faux (02-CB-7b) : remplacés par les sha256 complets recalculés ; une plage d'heures de NOTES
  écrite avant de lire l'horloge, corrigée à la lecture (`12:18:14`).
- **E-5 (premier jet de C-P2C-1).** Un espion du nom `int` du module des décodeurs cassait `type(c) is int` de
  `_champ` (témoins en panne) ; remplacé, avant toute campagne, par l'enveloppe de `_entier`.
- **E-6 (charge réelle insuffisante).** L'ancien `Bornes`, rejoué dix fois pendant la campagne m10, est resté vert :
  I-1 ne se reproduit pas sous la charge d'une seule campagne ; la dépendance au temps est montrée par l'horloge
  truquée et par le test neuf (AST).
- **E-7 (`diff -r`, `find`).** `diff -r -q` (demandé par le brief) compare récursivement deux copies, `docs/` compris :
  sortie vide, aucun nom imprimé. `find -name __pycache__` ne parcourt que `s2bis/`, `s2-harness/`, `scripts/sim-bis/`
  et `enforcement/` de mes copies. Aucune énumération de `docs/` ; les absences des exclusions se contrôlent par
  `test -e` sur les chemins nommés, `docs/15-*` et `docs/16-*` par le pathspec de l'archive seul.
- **E-8 (lignes des jobs).** Elles tournent telles qu'écrites dans `gates.yml` (`python3 -B …`, sans `-I`), sous
  `python3` 3.11.15 ; mes appels Python sont en `-I -B`.
- **E-9 (refus du crochet).** Le crochet `garde_faits` a refusé deux commandes (sleep d'avant-plan ; `pgrep -f` non
  ancré) avant toute exécution ; refaites dans les formes admises.

## 10. Journal G1 (provenance)

**Sources lues** (sha256 des octets lus ; base = extraction de 2a07ae6) :
- [lu] le brief, en entier (`BRIEF-INT-P2.md`, `423951f6…1ff62`) ;
- [lu] tranche C : `s2bis/p2c/RAPPORT-GENERATEUR.md` (`bc5fc99b…a37c9`), `ADJUDICATION.md` (`ef2d1465…45ade`), les six
  diffs (sha256 égaux à leur `SHA256SUMS`), outils `p2c/outils/*.sh`, `compte.py`, `bilan.py` (repris) ;
- [lu] tranche D : `s2bis/p2d/RAPPORT-GENERATEUR.md` (`b1efb433…787f2`), `ADJUDICATION.md` (`2fe61d21…1dae5`), les trois
  diffs en entier, outils `p2d/outils/*.sh` ;
- [lu] `s2bis/curve-doc/RAPPORT-LECTEUR.md` (`b4ac15c0…10140`), en entier ;
- [lu] G0 `docs/adr-0029/g0-collecte/G0-COLLECTE-RECALC-DEPLOI.md` (`08c1e6b0…8ec691d`), en entier ;
  PROPOSITION (`0cdf84c2…fbfd0`) l.120-135, l.160-230, l.270-285 (E-C-06 à E-C-41, CB-16 l.224, E-C-37 l.198, essai du
  smoke l.278) ; AVIS (`a919b307…16ce`) : lignes de Q-C-05 et de « smoke » (recherche dans ce seul fichier) ;
- [lu] ADR-0029 (`32a59893…aa2801`) l.78-82 (smoke de chaque observateur), l.166-176 (§2.5, témoin l.174), l.218-224
  (rodage, l.222) ;
- [lu] FORMAT (`799c8291…f5a6`, base ; puis l'état de travail) : en-tête (puces), §9.1, §14.1, §17 ;
- [lu] annexe B d'ADR-0028 (`ff6b4f47…4f9`), par recherche dans ce seul fichier (`CB-16`, `smoke`) : l.1052, l.1273,
  l.1274 ;
- [lu] code : `collecte/decodeurs.py`, `entree.py`, `lecture.py` (l.1-50), `http.py` (l.1-40, `lire` l.82-110),
  `__main__.py`, `recalc/config_analyse.py`, `recalc/rotation.py` (l.1-30, `lois`), `recalc/lecteur.py` et
  `oracle_indep.py` (docstrings) ; tests `test_decodeurs.py`, `test_decodeurs_actifs.py` (l.100-120),
  `test_formes_pool.py`, `test_temoin.py`, `test_format.py` (l.1-30, tests touchés), `test_config_analyse.py`
  (l.1-125), `test_bout_en_bout.py` (l.70-85), `test_entree.configurations`, `test_secondaire.carte` et `fichiers` ;
- [lu] S2 : `s2-harness/shogen_s2/smoke.py` (`779b6541…51757`, en entier), `sources.py` (`0c81fc33…dd4afe4`) l.288-290 ;
- [lu] outillage : `scripts/controle/mutants.py` (`3e218783…abddad64`) : docstring, `muter`, `main` ;
  `s2bis/p1b/g2/travail/outils/isole.sh` et `lo_up.py` ; `preparer-p2.sh` de l'orchestrateur (lu, non lancé) ;
- [2nd] valeurs mesurées des sources (prix, instants, adresses, sélecteurs) : celles des pièces et des fixtures des
  générateurs, que je n'ai pas re-mesurées ; documentation Curve : par la lecture du lecteur `claude-sonnet-5-5` ;
- [abs] tout essai réseau : smoke réel, poignée TLS réelle, captures (lot sans réseau).

**Commandes et sorties** : horodatées dans `NOTES.md` ; sorties sous `preuves/` (rouges, horloge truquée, rejeux de
`Bornes`, comparaisons du rebasage, équivalences, jobs par état, série, gates, matrice, xtask, `fin.log`) et sous
`mutants/` (une ligne JSON par run, diff et sortie de chaque mutant, bilans, journaux de campagne).

**Chiffres recomptés** : lignes ajoutées par diff par `outils/compte.py` ; tests par le `Ran` des suites et
`grep -c "    def test_"` ; lignes de fichiers par `wc -l` ; prix des fixtures pour la garde du smoke par le décodeur seul
(13) ; mutants par `outils/bilan.py` sur la sortie de chaque mutant (`FAIL:` et `ERROR:` relus).

**Outils** (`outils/`, hors dépôt) : `extraire.sh`, `geler.sh`, `regeler.sh`, `restaurer.sh`, `rebase.sh`,
`conflits.py`, `resoudre_9{a,b,c}.py`, `semantique_9{a,b}.py`, `metriques_*.py`, `tests_1*.py`, `code_1*.py`,
`squelette_14.py`, `stage/` (smoke, tests, squelette), `faire_diff.sh`, `serie.sh`, `arbre.sh`, `job.sh`, `essai.sh`,
`campagne.sh`, `suite_campagnes.sh`, `liste_mutants.py`, `m1{0..4}.py`, `bilan.py`, `compte.py`, `forme.py`,
`reformer.py`, `reformer_smoke.py`, `equivalence.py`, `egal_campagne.sh`, `horloge_lente.py`, `gates.sh`,
`matrice.sh`, `xtask.sh`, `fin.sh`, `fichiers.txt` (liste explicite des chemins touchés).

**Nettoyage** : copies lourdes effacées (base, travail, série, témoin, arbres de campagne, outil) ; restent les
mini-arbres figés par état (`etats/`, chemins explicites ; `etats-avant-forme/`, `etats-avant-12b/`), les diffs,
`mutants/`, `preuves/`, `outils/`, `NOTES.md`, ce rapport et `SHA256SUMS`. Aucun processus du lot ne tourne.

## 11. Ajout daté du 2026-10-17 16:47:34 UTC (`date -u`) : adjudication des questions, pas INT-P2-15 et INT-P2-16

L'orchestrateur a adjugé Q-1 à Q-6 après le rapport ci-dessus :
- Q-1 : les formes du témoin entrent maintenant dans `formes-pool.json` (pas 15).
- Q-2, Q-3, Q-4 : acceptés tels quels.
- Q-5 : la commande de capture se fait maintenant (pas 16).
- Q-6 : le test neuf du pas 12 est gardé.

Mêmes règles que pour les pas 10 à 14 : tests d'abord, mutants classés par la commande du job (même outil, borne de
300 s), plancher exact, une section METRIQUES par pas, R-25 respecté.

| id | sujet | code ajouté | plancher | mutants |
|---|---|---|---|---|
| INT-P2-15 | formes du témoin dans `formes-pool.json` (33 formes) ; smoke : les 33 formes lues et décodées | 59 (+ 4 lignes de données) | 425 | 12 / 12 |
| INT-P2-16 | commande `capture` (`capture.py`) : octets bruts et manifeste `captures.txt`, rien d'imprimé ; FORMAT §19 | 197 | 430 | 16 / 16 |

**INT-P2-15**
- Formes ajoutées : OKX `USDC-USDT` sur `www.okx.com` (espacée, cinq lectures d'OKX par fenêtre) ; Uniswap sur
  `eth.drpc.org` et Curve sur `rpc.mevblocker.io`, chacune en `POST` du corps de son décodeur.
- `test_formes_pool` contrôle aussi `corps-du-decodeur` et `rpc-par-unite`. Le budget d'OKX se lit sur le plan réel ; une
  sixième lecture d'OKX est refusée.
- La liste des décodeurs sans forme revient aux trois BTC regroupés.
- Test neuf : le smoke lit et décode les 33 formes, chacune servie par la fixture de son décodeur, rôle `temoin` pour les trois du témoin.
- Rouge : 7 FAIL, 0 ERROR.

**INT-P2-16**
- `capture --formes F [--carte C] --dossier D` fait les mêmes lectures que le smoke, sans décodage.
- Il écrit `<rôle>-<forme>.bin` et le manifeste `captures.txt` (fichier, sha256, statut, code, départ).
- Refus avant toute lecture : dossier absent, nom de forme non sûr, fichier déjà présent (jamais écrasé).
- Rien sur la sortie standard. Le test exige une sortie vide ; il vérifie aussi que les fichiers portent bien les prix.
  Les trois mutants « imprime » (octets lus, manifeste, commande) sont tués.
- Rouge sur squelette : 11 FAIL, 0 ERROR.

**Vérifications sur l'arbre final** (`preuves/fin2.log`) :
- Jobs de s15 et s16 conformes : 425 et 430.
- Série 01 à 16 rejouée depuis une extraction neuve de 2a07ae6 : 0 écart à chaque état. `diff -r -q` contre l'arbre
  final : vide. Contre l'arbre de travail réel, seule différence : le dossier `target/` que `xtask` crée dans la série.
- Runner 153 ok ; s2bis `Ran = 430` conforme ; S2 423 conforme ; sim-bis 279 conforme.
- Matrice 3.10 à 3.13 : 430 OK, 0 `Warning`, 0 `Exception ignored`, ligne du job conforme sous chaque version.
- `xtask` identique au témoin : seul S-G9 est ROUGE, déjà connu.
- 0 `__pycache__`. La HEAD du dépôt réel est inchangée.

**Écart E-10** : le premier lancement de m15 (`16:01:09`) a trouvé l'outil effacé. Il a été arrêté avant tout mutant,
l'outil ré-extrait (sha256 de `mutants.py` inchangé), et la campagne relancée à `16:01:24`. Ce premier lancement
n'est pas compté.

**Totaux de la série** : 16 diffs ; mutants des pas 10 à 16 : 94 joués, 94 tués par leur test visé, 0 vivant, 0 FATAL.

**Items** : la commande de capture existe désormais pour SHOGEN-S2BIS-FORMES-DOC-1, SHOGEN-S2BIS-TEMOIN-BLOC-1 et
SHOGEN-S2BIS-OKX-CARNET-VIDE-1. Leurs captures réelles demandent le réseau : ces items restent ouverts, à fermer au
premier smoke et à la première capture d'un observateur.
