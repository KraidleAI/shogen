# Rapport du worker — corrections du recalcul, tranche 1 (transcrit)

> Transcription par l'orchestrateur le 2026-10-05 08:15:55 UTC du rapport rendu par message par le worker (agent a0b2da034f0768e69) ; contrôle FM-1.1 du transcript : fragments_l51_l14 = 0. Texte du worker ci-dessous, sans retouche.

# Rapport du worker : corrections G2 et avis de la tranche 1 du recalcul de S2-bis (diffs RB-1d à RB-1g)

**Gate 0** : modèle `claude-opus-5-5`, fiche `shogen-worker`, effort max.
Travail du 2026-10-05, de 06:41:06 à 08:14:04 UTC (`date -u`). Rapport rendu par message.
Dépôt en lecture seule : aucune opération git en écriture. La tête est restée `3164348` du début à la fin, et `git status` est vide.

## Résumé, point par point

- **Base** : copie de `3164348` par `git --no-optional-locks archive`, avec les exclusions du brief (vérifiées absentes). Les sept diffs sont appliqués en série, leurs empreintes contrôlées (`rb1/SHA256SUMS` : 112 OK). Témoin : Ran 144 conforme, runner 33 ok.
- **Livraison** : 4 diffs en série, `RB-1d` à `RB-1g`.
  - Lignes de code ajoutées : 76, 83, 31 et 37, soit 227. Chacun reste sous 200.
  - Plancher exact à chaque diff (`--egal`) : 150, 155, 155, 156.
  - La série complète (11 diffs) s'applique sur `3164348` et redonne l'état final à l'identique (`diff -r`). Elle s'applique aussi sur `122c670`, où seul le plancher de sim-bis diffère.
- **C-1** (RB-1e) : σ de l'oracle Chainlink au moins égal au plancher par actif.
  - BTC et ETH : 5 400 s, le plancher de classe d'ADR-0020, égal à la valeur d'ETH de l.188. USDC : 124 200 s. USDT : 129 600 s (l.188).
  - Refus `ANALYSE/sigma`. Le test admet le plancher et refuse le plancher − 1, pour BTC, USDC et USDT.
- **C-2** (RB-1d) : six cas nommés tuent G-13, G-14, G-15, G-16, G-19 et G-20.
  - Le rouge est montré sous chaque mutant (`preuves/rouges/`).
  - Sur l'état RB-1c, les six restent vivants. Sur RB-1d, chacun est tué par son cas.
- **C-3** (RB-1d) : METRIQUES corrigé, comptes relevés par `wc -l` sur les états rebâtis.
  - RB-0a : `test_fitness.py` fait 74 lignes. RB-1a : `test_lecteur.py` fait 76 lignes. RB-1b : 202 lignes.
  - Tous les autres comptes de METRIQUES ont été recomptés : ils sont justes.
- **C-4** (RB-1d) : la docstring de `_integre` dit ce que le lecteur calcule.
  - Valeur inchangée : `ws` d'un marqueur et `a` d'un trou, là où l'écrivain retient `ws + w` et `a + w`. Le lecteur n'en garde que le type.
  - L'état d'un marqueur est maintenant fixé par `test_lignes_integres_et_etat`. Le mutant M-1d-01 était vivant sur RB-1c ; il est tué sur RB-1d.
- **Q-RB-1** (RB-1g) : nouvelle fitness `test_copie_de_la_lecture_json_stricte`.
  - Elle lit les deux fichiers en octets, sans import, et compare par `ast` les segments de texte : `_objet`, `_entier`, et dans `charger` le `with`, le `try`/except et le `return`.
  - Seuls diffèrent les préfixes `CONFIG/`↔`ANALYSE/` et le nom d'exception.
  - La copie a été alignée sur l'original : docstring de `_entier`, variable `donnees`.
  - Rouge avant l'alignement : 1 échec. Le test tombe si l'une des copies change sans l'autre (M-1g-01 à M-1g-04 tués, dont un commentaire seul changé).
- **Q-RB-4** (RB-1e), trois contrôles à refus nommé :
  - plancher de τ des oracles : ETH 0,75 %, stables 0,375 % (l.188), refus `ANALYSE/tau-plancher` ;
  - grille de 0,05 % pour τ de BTC seulement (l.181), refus `ANALYSE/tau-grille` ;
  - σ(actif, classe) ≥ σ_BTC(classe) (l.189), refus `ANALYSE/incoherent : sigma-btc`. **Portée restreinte aux places et aux agrégateurs, voir Q-RBc-1.**
- **Q-RB-5** (RB-1f) : `ROTATION-S2BIS.md` §1 pt 8 dit maintenant : ordre strict des points de code sur les noms d'hôte de la configuration (précision de l.200) ; la première unité effective sera imprimée au rendu (item pour RB-15).
- **Q-RB-6** (RB-1e) : le schéma exige R = 9 999 et seuil = 99 exactement (`ANALYSE/borne`).
  - La règle alpha reste en seconde garde ; elle est testée sur le prédicat lui-même, dans `test_regles`.
  - Les tests à petit R passent par `lois()`. C'est documenté au §1 pt 9 du contrat.
- **Q-RB-12** (RB-1f) : nouveau §8 de `ROTATION-S2BIS.md`, avec les six points de cohérence avec SIM-BIS : positions, identifiants = noms d'hôte, première unité, R et seuil en paramètres, libellés de strate, masques.
- **Q-RB-13** (RB-1f) : une seule règle `HOTE = [a-z0-9.-]{1,253}` (`fullmatch`), dans `rotation.py`, importée par `config_analyse._nom`.
  - Refus `ROTATION/unite` et `ANALYSE/unite`.
  - Rouge avant le code : 14 échecs dans 3 tests.
- **Q-RB-14** (RB-1f) : le mutant « modulo n_s au lieu de n′_s », dû à RB-7, est déclaré à trois endroits : docstring de `tests/test_rotation.py`, METRIQUES RB-1f et contrat §7.
- **O-6** (RB-1g) : le commentaire de `test_fitness.py` décrit la règle codée (ni collecte, décodeurs compris, ni S2). Un cas de refus des décodeurs est ajouté ; M-1g-06 est tué.
- **Mutants**, tous classés par la commande du job (runner, puis ligne de `gates.yml`, borne de 300 s), avec 0 vivant, 0 FATAL et chaque mutant tué par son test visé :
  - réviseur : 20 sur 20 sur l'état final. 19 sont rejoués tels qu'écrits. G-02, dont le texte n'existe plus depuis Q-RB-13, est tué sur l'état RB-1e et tué une seconde fois sous sa forme transposée, G-02′ ;
  - échantillon de 23 mutants du worker : 23 sur 23 sur l'état final ;
  - mutants neufs : 37 sur 37, tués sur l'état de leur diff, puis de nouveau sur l'état final ;
  - durée d'un passage : de 18,9 à 22,9 s.
- **Contrôles finaux** :
  - Python 3.10 à 3.13 en `-X dev -W error` : Ran 156, OK, 0 avertissement ;
  - ligne du job sous les quatre interpréteurs : conforme, Ran = 156 ; runner : 33 ok ;
  - `s2-harness` : Ran 405, OK (skipped=2) ; hooks : 54 ok ;
  - gate des secrets : OK sur les 10 fichiers touchés ; R-13 : 0 ; R-8 : bibliothèque standard seule ;
  - octets 92 : compte inchangé dans chacun des 10 fichiers ;
  - `xtask` : lignes de verdict identiques au témoin (S-G9 sur `docs/17:70`, cas connu).

## 1. Livraison

| diff | objet | code ajouté | plancher | mutants du diff | sha256 |
|---|---|---|---|---|---|
| RB-1d | C-2, C-3, C-4 (lecteur, comptes) | 76 | 150 | 9 sur 9 (G-13 à G-16, G-19, G-20 ; M-1d-01 à 03) | `67caf29e…09d0` |
| RB-1e | C-1, Q-RB-4, Q-RB-6 | 83 | 155 | 17 sur 17 | `41b0c317…1439` |
| RB-1f | Q-RB-13 ; contrat : Q-RB-5, 6, 12, 14 | 31 | 155 (aucun test neuf, tests des noms récrits) | 11 sur 11 | `8a0fa48d…0f66` |
| RB-1g | Q-RB-1, O-6 ; sous-section des rejeux finaux | 37 | 156 | 6 sur 6 | `ac3c1f6e…0fb6` |

État final :

| fichier | lignes | tests |
|---|---|---|
| `config_analyse.py` | 168 | — |
| `rotation.py` | 111 | — |
| `lecteur.py` | 147 | — |
| `test_config_analyse.py` | 204 | 13 |
| `test_rotation.py` | 141 | 8 |
| `test_lecteur.py` | 313 | 20 |
| `test_fitness.py` | 96 | 5 |

- METRIQUES reçoit une section par diff, la ligne de fitness neuve et une sous-section des rejeux sur l'état final.
- Ligne à committer : `verdict-suite-s2.py s2bis --aucun-saut --egal --plancher 156`.

## 2. Rouges (tests d'abord)

- **RB-1e** : 16 échecs dans 5 tests, 0 erreur (souche : code de RB-1d, tests de RB-1e).
- **RB-1f** : 14 échecs dans 3 tests, 0 erreur.
- **RB-1g** : 1 échec dans 1 test.
- **RB-1d** : le code était déjà juste. Le rouge est montré sous les 6 mutants de C-2 et sous M-1d-01 et M-1d-03 : sous mutant sortie 1, sans mutant sortie 0 (`preuves/rouges/`).
- Les rouges ont été rejoués sur les souches rebâties : mêmes échecs.
- **Sans test, par nature** : C-3, C-4 (docstring ; sa valeur est épinglée par un test), Q-RB-5, Q-RB-12 et Q-RB-14 (documents).

## 3. Écarts déclarés

- **E-1, correction de forme.** Ma relecture a trouvé deux défauts de lignes vides dans `test_config_analyse.py` (PEP 8) : une manquante avant `class Unites` à RB-1e, une de trop avant `test_R_et_seuil_exacts`.
  - Correction faite dans RB-1e et propagée ; les diffs ont été régénérés.
  - J'ai tout rejoué : rouges, verts, campagnes de RB-1e à RB-1g, rejeux finaux.
  - Les premières passes sont versées sans être comptées, dans `preuves/v1-avant-forme/`. Le premier rejeu final était à 20 sur 20 sur le jeu du réviseur quand je l'ai arrêté ; j'ai tué mon seul groupe de processus (8522).
- **E-2, test visé mal déclaré.** Au premier passage de RB-1f, M-1f-07 (nom vide admis) était tué par `test_refus_nommes`, alors que j'avais déclaré un autre test visé. Le test visé est corrigé ; les rejeux le montrent tué par celui-ci.
- **E-3, VALIDE modifié.** Le σ des places horodatées de BTC passe de 180 à 30 : sinon σ(ETH, place) = 30 violerait la règle sigma-btc.
  - Nouvel sha256 calculé hors du code (`sed`, `sha256sum`) : `c7597368…a15e`, 1 000 octets, versé dans `travail/VALIDE-c1.bin`.
- **E-4, G-02.** Son texte (`_nom` en ASCII imprimable) a disparu avec Q-RB-13, qui refuse l'espace par conception. Il est rejoué tel qu'écrit sur RB-1e (tué), et transposé sous la forme G-02′ (« espace admise dans HOTE », tué).
- **E-5, σ de l'oracle ETH.** Il n'a pas d'entrée dans `SIGMA_ORACLES`, car sa valeur (5 400 s) est égale au plancher de classe ; un commentaire le déclare. Ainsi G-01 garde son test visé. Sans ce choix, G-01 deviendrait équivalent.
- **E-6, git hors du dépôt.** La gate des secrets a tourné dans un index jetable de mon `TMPDIR` ; le runner des hooks crée ses propres dépôts dans `mktemp`. Sur `/home/user/shogen`, seulement `rev-parse`, `log`, `status` et `archive`, avec `--no-optional-locks`.
- **E-7, machine partagée.** Les campagnes `cb18` d'un autre worker tournaient en même temps. Je n'ai arrêté que mes propres processus.

## 4. Questions et items (règle PAROXYSME)

- **Q-RBc-1, portée de σ ≥ σ_BTC (à décider).**
  - J'applique la règle aux places et aux agrégateurs seulement. C'est le texte de l.189 : « le σ des places et des agrégateurs sur ces actifs ».
  - Les oracles d'ETH et des stables ont des « planchers seuls » (l.189), aux valeurs de l.188. Or ETH = 5 400 s peut être sous σ_BTC(oracle) ; S2 avait 10 695 s (l.182).
  - Appliquer la règle aux oracles refuserait donc la valeur de l'ADR elle-même. Le test l'établit, et M-1e-12 montre que l'autre lecture est détectée.
  - Si l'orchestrateur voulait toutes les classes, il faut amender l'ADR.
- **Q-RBc-2, classe absente de BTC.** Une classe présente pour un actif et absente de BTC est refusée (`sigma-btc`). C'est [inféré] : l.189 exige σ_BTC(classe), et les pools sont pris parmi les hôtes de BTC (l.173). À confirmer.
- **Q-RBc-3, forme des noms d'hôte.**
  - La règle suit la lettre du brief : jeu de caractères et longueur seulement.
  - La structure en étiquettes de RFC 1123 (étiquettes non vides de 63 caractères au plus, ni « - » en tête ou en queue) n'est pas appliquée. Des noms comme `-`, `.` ou `a..b` sont donc admis.
  - Source primaire non lue ([abs]) ; l'expression de l'AVIS était [2nd]. Resserrer ou non relève de l'orchestrateur, avec l'ajout daté au G0.
- **Q-RBc-4, contrôles de l.189 hors liste fermée, non faits.**
  - Plancher de τ des agrégateurs des autres actifs : τ_agr(actif) = grid-ceil(τ_places(actif) × τ_agr_BTC/τ_places_BTC, 0,05 %), CAPO comprise.
  - Les autres termes de la formule de σ.
  - À porter à CALIB-ACTIFS ou au paquet.
- **Q-RBc-5, rédaction de la règle des masques.** Le brief dit « masques ≤ 2^n ». Le contrat écrit la règle exacte du code, 0 ≤ masque < 2^n (2^n est refusé). À confirmer.
- **Information** : SIM-BIS n'importe aujourd'hui ni `rotation` ni `shogen_s2bis` (recherche ciblée dans `scripts/sim-bis/`). Le resserrement des noms ne casse donc aucun consommateur ; SB-13 devra suivre le §8 du contrat.
- **Restent en items, non touchés** : Q-RB-10 et N-2, Q-RB-15, O-5, I-4, I-5, I-6, I-1 et N-1.

## 5. Journal G1 (provenance)

**[lu]** (préfixe du sha256 ; plage lue) :
- **Pièces du lot** :
  - brief `c33bfcdb`, en entier ;
  - G2 transcrit `03989bb1`, en entier ;
  - AVIS-RB-T1 `2e542f5f`, en entier ;
  - mon rapport précédent `b0977f09`, en entier ;
  - brief précédent `29d75bd2`, en entier.
- **G0 et ADR** :
  - G0 `fe57eeb1`, en entier ;
  - PROPOSITION `0cdf84c2` : l.1-130 et l.374-613 ;
  - AVIS du G0 `a919b307` : l.48-65 (Q-R-01, Q-R-02) et les titres ;
  - ADR-0029 `b908842d` : l.160-219 (l.181-189, 200, 202, 212) ;
  - FORMAT `08c6b20e` : §7 (l.101-132) et les titres.
- **Annexes d'ADR-0028** : annexe B `4633f7b9` (l.1042 et l.1068) ; annexe D `deb64179` (l.32-45, liste D.2, pour l'éviter).
- **Paquet `s2bis`** :
  - `journal.py` `958f5a8d` : l.114-125 et l.185-262 ;
  - `config.py` `77f909e5` : l.1-70 ;
  - `test_journal.py` `87804f34` (l.1-80), `test_reprise.py` `4c80609f` (l.1-60), `test_fichiers.py` `1c314a8d` (l.1-40) ;
  - les fichiers RB de l'état RB-1c, en entier ;
  - METRIQUES : l.1-20 et 228-454.
- **SIM-BIS** :
  - `parametres.json` `93982c86` : l.1-22 (`calibration.strates` = calme, stress), plus une recherche ciblée ;
  - `calendrier.py` `9fecdca0` : l.70-82 ;
  - `sources.py` `32e9b9f0` : l.165-194.
- **Outils** :
  - du réviseur : `job.py` `39084987`, `campagne_g2.py` `927a7475`, `mutants_g2.py` `08a26c15`, `echantillon_worker.py` `11e5517e`, `vise.py` `1cc5bb96` ; sa sortie des survivants non équivalents ;
  - d'isolement : `isole.sh` `ebaa1c78`, `lo_up.py` `b532be4b` ;
  - les miens du lot précédent, et les 7 fichiers `mutants_rb*.py` ;
  - `gate-secrets.sh` `f89abf0f` (l.1-60) ; runner des hooks `43411afb` (l.1-30) ; `gates.yml` (l.195-245).

**[abs]** :
- valeurs re-dérivées de σ_BTC (TAU-SIGMA-S2BIS pas encore produit) ;
- source primaire de la syntaxe des noms d'hôte ;
- `formes.json`.

**[2nd]** : le σ de S2 pour Chainlink (10 695 s), cité par l'ADR (l.182).

**Non ouverts** : aucune pièce de D.2, aucun `*.jsonl`, aucun dossier interdit. Aucune recherche récursive sur `docs/`, le dépôt ou le scratchpad. `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée.

**Chiffres recomptés** :
- `wc -l` des 8 états de la série ;
- VALIDE neuf : 1 000 octets, `c7597368…` ;
- lignes ajoutées par diff : 76, 83, 31, 37 ;
- rouges : 16, 14 et 1 ;
- bilans des campagnes (`preuves/*mutants*.txt`) ;
- octets 92 par fichier, avant et après (`preuves/octets92.txt`). Une seule ligne ajoutée en porte : la ligne déplacée de `test_config_analyse.py`, octets identiques à l'original (contrôlé par `od -c`) ;
- outils : barres écrites par `chr(92)` ; `\n` et `tr '\n'` voulus.

## 6. Fichiers

Dossier du lot : `<scratchpad>/s2bis/rb1/corr/`

- **diffs** : `…/corr/diffs/RB-1d.diff`, `RB-1e.diff`, `RB-1f.diff`, `RB-1g.diff`.
- **Empreintes** : `…/corr/SHA256SUMS`, 110 lignes, contrôlé par `sha256sum -c`, sha256 `d2705164…63cd3`.
- **outils/** :
  - mutants : `mutants_rb1d.py`, `mutants_rb1e.py`, `mutants_rb1f.py`, `mutants_rb1g.py`, `mutants_final.py` ;
  - lanceurs (`campagne_g2.py` et `job.py` sont des copies identiques à celles du réviseur) ;
  - `etats_corr.sh` rebâtit tous les états depuis la tête dans `corr/etats` ; le résultat a été vérifié égal à mes états ;
  - `verif_serie.sh`, `final_controles.sh`, `rouge_mutant.py`, `xtask.sh`.
- **preuves/** : rouges, verts, campagnes par diff et rejeux finaux, contrôles finaux, xtask, vérification de la série ; `v1-avant-forme/` (versé, non compté).
- **travail/** : `VALIDE-c1.bin` et les fichiers de tests des souches.
- **Nettoyage** : arbre complet, instantanés, cible cargo (137 Mo), copies de série et temporaires supprimés. Le dossier fait 1,1 Mo. Aucun processus à moi ne reste.

