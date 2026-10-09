# Contre-contrôle de SB-11 (CONFORME après SB-11w) (transcrit)

> Transcription par l'orchestrateur le 2026-10-09 14:33:41 UTC du fichier g2/cc/RAPPORT-CC.md ; contrôle FM-1.1 des transcripts du générateur (deux reprises), du réviseur, du correcteur et du contre-contrôleur : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Contre-contrôle des corrections de la G2 de SB-11 (diff SB-11v)

**Gate 0** : modèle résolu `claude-opus-5-5` (identifiant exact de l'environnement de ce contre-contrôleur). Rôle :
contre-contrôleur neuf. Je n'ai écrit ni la série SB-11a … u, ni la G2, ni le diff SB-11v. Je n'ai rien corrigé.

**Verdict : CONFORME-AVEC-RÉSERVES.**

Les corrections C-1 à C-9 sont faites, aux lignes citées. Pour chacune, j'ai rejoué le mutant visé :
- le test neuf est rouge d'assertion sous ce mutant ;
- il est vert sans lui.

Le delta e11u → e11v ne touche que ce que la liste demande. Les preuves P-1 à P-9 passent, P-1 comprise. Les 12 vivants
non équivalents de la G2 sont tués, et toutes les gates sont aux planchers exacts.

Réserves (liste fermée) :
- **R-1** (O-CC-1) : `test_budget` affaibli contre le mutant « première mesure ».
- **R-2** (O-CC-2) : le cas « hors de l'ordre » de C-5 n'isole pas sa garde.
- **R-3** (O-CC-3) : le R de la cellule n'est pas couvert à deux sites : le calcul « avec » et `variante.tester`.
- **R-4** (O-CC-4) : le W de la cellule passé à `fond` n'est pas couvert.
- **R-5** (O-CC-6) : la ligne d'item NPRIME-NUL-1 est à préciser.

R-1 et R-2 viennent de la lettre même de la G2 (§5) et de l'adjudication, que le correcteur a suivies. R-3 et R-4 sont
des lacunes de la série, du même motif que C-4 et C-8, que ni la G2 ni SB-11v n'ont visées. Aucune réserve ne touche un
chiffre produit par le code de SB-11v.

Dossier : `<scratchpad>/s2bis/sb11/g2/cc/`, avec `NOTES.md` pour la reprise. Il contient :
- `outils/` : mes scripts ;
- `journal/` : les sorties des contrôles ;
- `mut/` : la campagne et la sortie de chaque mutant ;
- `SHA256SUMS`.

## 1. Pièces, base, copies, horloge

- **Horloge** : début à 08:25:00 UTC, rapport à 09:35:23 UTC, le 2026-10-09. Chaque heure a été lue par `date -u`.
- **Pièces**, contrôlées à 08:25:17 :
  - `sha256sum -c SHA256SUMS` : 1 376 OK, 0 échec ;
  - `g2/SHA256SUMS` : 57 OK, 0 échec.

  | pièce | sha256 |
  |---|---|
  | `SB-11v.diff` | `1508a268…` (égal au §15.2) |
  | `RAPPORT-GENERATEUR.md` | `73f291dc…` |
  | `ADJUDICATION-G2.md` | `635e8b91…` |
  | `g2/RAPPORT-G2.md` | `42b1a1b3…` |
  | `g2/preuves/test_preuves_g2.py` | `54cadf72…` |

  Les trois dernières sont égales à celles de leurs listes.
- **Base 5e386c4** : copie par `git --no-optional-locks archive`, avec les sept exclusions du brief, que j'ai vérifiées
  absentes (aucun `*.jsonl`).
  - `scripts/sim-bis` et `gates.yml` de la copie sont égaux à `etapes/base`.
  - SB-11a … u puis SB-11v s'appliquent avec `patch -p1`, sans rejet ni décalage (`journal/application-base.txt`).
  - Le résultat est égal à `etapes/e11v` (`diff -rq` et `cmp` vides).
  - `w` moins SB-11v (`patch -R`) donne une copie égale à `etapes/e11u`.
- **Tête** : `1a388e1`, relue à 08:25:27, 08:32 et 09:34:59. Elle descend de 5e386c4 et `status --porcelain` est vide.
- **Écritures** :
  - aucune écriture git au dépôt réel ;
  - `git init` avec alternates vers les objets du dépôt (lecture seule) dans mes copies seules, pour `oracle_r1` (E-CC-1).
- **Interdits tenus** :
  - `SHOGEN_S2_CAMPAGNE_CONTROL` n'a jamais été posée : elle est retirée de chaque environnement, et `isole.sh` la retire
    aussi ;
  - aucun `*.jsonl`, aucune pièce de D.2, aucun dossier interdit ouvert ;
  - aucune recherche récursive sur `docs/`, le dépôt ou le scratchpad ;
  - tout a tourné sous `unshare -n` ;
  - de `cargo xtask`, je n'ai lu que les lignes VERDICT.
- **Processus lourds**, un seul à la fois, en PAR=2 au plus. Chaque PID a été lu dans `/proc/PID/cmdline` :

  | processus | PID | début | fin |
  |---|---|---|---|
  | rouges ciblés | 26980 | 08:29:21 | 08:29:55 |
  | campagne 1 | 27742 | 08:30:44 | 09:08:25 |
  | campagne 2 | 10745 | 09:08:59 | 09:15:32 |
  | gates | 16052 | 09:17:04 | 09:34:51 |

  Les preuves (08:30, 12 s) et la reproduction de n′ = 0 (09:16, 5 s) ont tourné au premier plan, chacune seule.
- **Copies supprimées à la fin** : `w`, `wu`, `t`, `tn` et la cible cargo. Le TMPDIR `cc/tmp` a été vidé.

## 2. Le delta e11u → e11v : rien hors de la liste

SB-11v touche sept fichiers :
- `gates.yml` : plancher sim-bis 246 → 252 ;
- `executer.py` : la ligne `:190` et la docstring de `plan`, `:184-187`, et rien d'autre ;
- cinq fichiers de tests : `test_budget`, `test_executer`, `test_cellules`, `test_replication`, `test_pauses`.

Forme :
- 112 lignes ajoutées et 15 retirées, recomptées (≤ 200, R-25) ;
- 0 octet 92 dans le diff et dans `scripts/sim-bis` ;
- aucune ligne `.py` de plus de 120 caractères ;
- 0 marqueur `TODO`, `FIXME` ou `XXX`.

Chaque changement de test se rattache à un C-n :
- C-1 : `test_budget`, `test_plan_90_min` ;
- C-2 : `test_frequences_e_s_52` ;
- C-3 : `test_lot_forme` ;
- C-4 : `test_l_2_au_site_d_appel` ;
- C-5 : `test_schema_ferme_c_5` ;
- C-6 : `test_n_prime_aux_sites_d_appel` ;
- C-7 : `test_surcharges_jusqu_aux_sources` ;
- C-8 : `test_r_de_la_cellule` ;
- C-9 : `test_meme_c1_dans_les_deux_strates`.

Deux tests vont au-delà de la lettre de l'adjudication, sans en sortir :
- C-7 contrôle aussi `observateurs.Couche` (voir O-CC-5) ;
- C-8 nomme M-11V-04 et M-11V-05.

**Plancher** (`TestLoader.discover`, 0 erreur de chargement) :
- e11u : 246 ;
- e11v : **252** (6 méthodes neuves) ;
- tête + série : **268** = 210 + 58.

## 3. Corrections C-1 à C-9

- **Rouge ciblé** : le test seul, sous le mutant, par `python3 -B -m unittest -v`, isolé (`journal/rouges.txt`). Les 14
  paires sont FAIL d'assertion, sans aucune ERROR.
- **Vert** : les 10 tests sans mutant, Ran 10, OK.
- **Campagne** : la commande du job sur la suite entière (§4).
- **Lignes citées** : toutes relues à leur numéro. Elles tombent sur `def` ou sur la ligne de code annoncée.

| C | fait (fichier:ligne, e11v) | rouge rejoué (assertion) | vert | règle de fixture | écart |
|---|---|---|---|---|---|
| C-1 | `executer.py:190` `t = borne // ns * processus` ; tests `test_budget.py:24`, `test_executer.py:198` | ancienne formule : `test_budget` ((0, 5), (5, 10) contre (0, 4), (4, 8), (8, 10)) et `test_plan_90_min` ((0, 526)… (9994, 10000) contre (0, 524)… (9956, 10000)) ; G-22 : ns_max 5 contre 12 | oui | 41 s × 4 : 131 tours, 5 371 s, lots de 524, 20 lots, recomptés ; P-1 passe | **O-CC-1** : (12, 5) ne sépare plus la « première mesure » (M-CC-08 vivant sur e11v, tué sur e11u) |
| C-2 | `test_executer.py:71` | G-01 : (3, 2, 1) contre (4, 2, 1) | oui | combinaison mixte, de compte distinct | — |
| C-3 | `test_executer.py:159` | G-03 : None contre LOT/forme ; M-CC-06 (contrôle par `sorted`) tué aussi | oui | i permutés, empreinte recalculée | — |
| C-4 | `test_cellules.py:133` | G-06 : 8 contre 16 | oui | W = 16 et 2, contre ⌊(W + 1)/2⌋ = 8 et 1 | O-CC-4 : W non couvert à `fond` |
| C-5 | `test_cellules.py:140` | G-07, G-08, G-19 : None contre CELLULE/schema | oui | gardes : N1 et « parmi/faibles » avec unités faibles passent (None) | **O-CC-2** : [ETH, BTC] n'isole pas la garde d'ordre (M-CC-09 vivant) |
| C-6 | `test_replication.py:194` | G-09 : {12 000, 2 736} contre {11 838, 2 533} ; G-12 : [12 000, 12 000, 2 736, 2 736] contre [11 838, 11 838, 2 533, 2 533] | oui | n′ distinct de n_s dans les deux strates ; garde n′ de calme < 12 000 | — |
| C-7 | `test_replication.py:210` | G-10 : longues [60, 1 440, 4 320] contre [60] | oui | surcharge distincte de `PRM` ; garde `P99` intact | O-CC-5 (info) |
| C-8 | `test_replication.py:223` | G-11 : ([99, 99], …) contre ([999, 999], …) | oui | R = 999 contre 99 ; R_approche vaut aussi 999, mais M-CC-01 (`R_approche` passé) est tué par trois autres tests | **O-CC-3** : sites « avec » et `variante.tester` non couverts |
| C-9 | `test_pauses.py:104` | G-16 : strate de stress absente | oui | point partagé (1/10, 5, 60) contre (1/100, 5, 60) | attendu par appel de la même fonction (forme prescrite par l'adjudication) |

L'ancienne formule appliquée à e11v donne exactement le code de e11u avec les tests de v, puisque `plan` est le seul delta
de code. Son rouge est donc le rouge de C-1 sur la série.

## 4. Mutants

**Commande** : celle du job, `python3 -B enforcement/verdict-suite-s2.py scripts/sim-bis --aucun-saut --egal
--plancher 252`.
- Elle tourne dans un arbre par mutant : liens vers `w`, et `scripts/sim-bis` copié puis muté.
- Le tout tourne sous `isole.sh` et `timeout 300`, en PAR=2.
- Classement : sortie 1, tué ; sortie 0, vivant ; toute autre sortie, FATAL.
- Mes définitions G-xx (`outils/mutants_cc.py`) sont égales, chaîne pour chaîne, à `g2/outils/mutants_g2.py` (contrôle
  par script).

**Témoins** (VIVANT, Ran 252) : 148 s au début, 152 s à la fin. Sur e11u : 190 s, Ran 246. Le mutant le plus long a pris
213 s. Il n'y a eu aucun FATAL.

| id | mutation | issue | test(s) rouge(s) |
|---|---|---|---|
| G-01 | `any` → `all` | TUÉ | test_frequences_e_s_52 |
| G-03 | contrôle des i retiré | TUÉ | test_lot_forme |
| G-06 | (W + 1) // 2 à la couche | TUÉ | test_l_2_au_site_d_appel |
| G-07 | imposés « faibles » sans unité faible | TUÉ | test_schema_ferme_c_5 |
| G-08 | BTC en tête non exigé | TUÉ | test_schema_ferme_c_5 |
| G-09 | n_s aux retraits | TUÉ | test_n_prime_aux_sites_d_appel |
| G-10 | `Replication(prm, …)` | TUÉ | test_surcharges_jusqu_aux_sources |
| G-11 | R du prm à la règle | TUÉ | test_r_de_la_cellule |
| G-12 | n_s au critère | TUÉ | test_n_prime_aux_sites_d_appel |
| G-16 | première strate seule | TUÉ | test_meme_c1_dans_les_deux_strates |
| G-19 | f nul admis | TUÉ | test_schema_ferme_c_5 |
| G-22 | dernière durée | TUÉ | test_budget |
| ANCIENNE | `t = borne * processus // ns` | TUÉ | test_budget, test_plan_90_min |
| M-CC-01 | `R_approche` du prm à la règle | TUÉ | test_absorption_s_variante_evenements, test_chaine_a_la_main, test_premiere_apres_retrait |
| M-CC-02 | division par excès dans `plan` | TUÉ | test_budget, test_plan_90_min |
| M-CC-03 | R du prm au calcul « avec » (`_tester`) | **VIVANT** | — |
| M-CC-04 | R du prm à `variante.tester` (i ≥ 200) | **VIVANT** | — |
| M-CC-05 | `fond(p, cel, points, (W + 1) // 2)` | **VIVANT** | — |
| M-CC-06 | contrôle des i par `sorted` (permutation admise) | TUÉ | test_lot_forme |
| M-CC-07 | `(borne - 1) // ns` (lot égal à la borne refusé) | TUÉ | test_plan_90_min (assertion), test_lots_par_point_et_reprise (ERROR : pas nul) |
| M-CC-08 | `m = ns[0]` | **VIVANT** sur e11v ; **TUÉ** sur e11u (test_budget) | — |
| M-CC-09 | garde d'ordre des classes retirée | **VIVANT** | — |

Chaque tué l'est par au moins une AssertionError. La seule ERROR est celle de M-CC-07, à côté de son assertion.

**Bilan** :
- les 12 vivants non équivalents de la G2, et l'ancienne formule : 13 sur 13 tués ;
- mes 9 mutants neufs : 4 tués et 5 vivants.

Les 5 vivants ne sont pas équivalents :
- M-CC-03 et M-CC-04 : un R de 99 au lieu de 999 change le seuil et le nombre de rotations. Les champs C, C1 et r des
  enregistrements « avec » et « variante » changent alors [inféré du code, `regle.decider` et `regle.seuil`].
- M-CC-05 : la durée de dérive passe de W·tendance à ⌈W/2⌉·tendance. C'est la même chose à W = 1 seulement.
- M-CC-08 : le coût retenu n'est plus le maximum.
- M-CC-09 : une cellule à [BTC, USDT, ETH] est admise, ce qui casse le schéma fermé.

## 5. Preuves P-1 à P-9 du réviseur, sur l'état final

`g2/preuves/test_preuves_g2.py`, copié sans changement dans un arbre de `w`, donne Ran 9, OK, code 0
(`journal/preuves.txt`). **P-1 passe** : chaque lot tient sous la borne, ⌈(b − a)/p⌉·ns ≤ borne, et `ns_max` vaut 12.

## 6. Gates

Toutes ont tourné l'une après l'autre (`journal/gates.txt`).

| contrôle | copie | résultat |
|---|---|---|
| sim-bis `--plancher 252` | `w` = 5e386c4 + a … v | conforme, Ran = 252 (135 s), plus les témoins de campagne |
| runner `run-fixtures-verdict-suite-s2.py` | `t` = 1a388e1 + a … v résolue | code 0, 136 ok, 0 échec |
| sim-bis `--plancher 268` | `t` | conforme, Ran = 268 (140 s) |
| s2bis `--plancher 340` | `t` | conforme, Ran = 340 |
| S2 `--egal` | `t` | conforme, Ran = 415, deux sauts qui nomment la variable scellée |
| matrice `-X dev -W error`, `unittest discover` | `t/scripts/sim-bis` | 3.10.20 : 192 s ; 3.11.15 : 158 s ; 3.12.3 : 166 s ; 3.13.14 : 155 s. Code 0 et Ran 268 OK partout ; 0 « Exception ignored », 0 « Warning » |
| `cargo --locked xtask verify`, lignes VERDICT seules | `t` et `tn` = `git archive 1a388e1` neuve | 8 VERT, 1 ROUGE (1 violation), global ROUGE. Les **dix lignes sont identiques** (`diff` vide) : la violation précède la série |

**Application sur la tête** (`journal/application-tete.txt`) :
- **Seuls conflits** :
  - le plancher sim-bis de `gates.yml`, aux 22 diffs ;
  - la ligne du README voisine d'`oracle_recalc.py`, à 20 diffs (ni s ni v).
- `commun.py` s'applique avec un décalage de 6 lignes, et rien d'autre ne rejette.
- **Ma résolution, faite à neuf** :
  - le plancher passe à 268 ;
  - les lignes `executer.py` et `e1.py` de e11v sont insérées après celle d'`oracle_recalc.py`.
- **Comparaison avec `fusion/` du générateur** : les seules différences sont les six fichiers de SB-11v et les planchers
  (s2bis 340, de la tête ; sim-bis 268). C'est ce qu'affirme le §15.6.

## 7. Lignes d'items du §15.7 au regard du code

| item | avis | preuve |
|---|---|---|
| NPRIME-NUL-1 | **exacte sur le fond, à préciser (R-5)** | voir ci-dessous |
| BUDGET-SERRE-1 | exacte | recomptes ci-dessous |
| VALS-STRICT-1 | exacte | `e1.py:279-280` (`zip`) ; `:211` (`if s in pz`) ; `strict=` existe depuis 3.10 |
| MUT-EQUIV-FIXTURE-1 | exacte, portée à élargir | les survivants M-CC-03, M-CC-04, M-CC-05, M-CC-08 et M-CC-09 relèvent du même motif : y joindre la règle « une garde par cas » et « maximum ni premier ni dernier » |
| AGREGATS-SB12-1 | exacte | `agreger` (`executer.py:417-444`) ne calcule que les fréquences, les taux, le rejet familial et la séquence d'ETH ; `agreger_impressions` (`:529`) ne calcule que les impressions ; d'après le grep, `atteinte`, `retraits`, `C_S` et `evenements` ne sont écrits qu'aux enregistrements (`:395-401`) et jamais agrégés |
| P-L20-1 | plausible [lu en partie] | `sources.loi_longueurs` est empirique (EP) ; la loi géométrique ne sert qu'aux incidents |
| FAMILLES-1, TDET-ECHELLE-1 | reprises de la G2 [2nd] | — |
| E1-LANCEUR-1 | exacte | `lancer_e1(…, oracles: dict, …)`, `e1.py:329` |
| MUT-DUREE-1 | exacte, et mes mesures la confirment | suite seule 135-140 s ; témoins 148 à 190 s et mutants jusqu'à 213 s en PAR=2 sous une charge de 4 à 6 |
| PARTIEL-AVANT-1 | exacte | `commun.py:209-213` (SORTIE/partiel-present) ; README : « un « .partiel » resté se retire d'abord » |
| E1-PAIRE-1 | exacte | `e1.py:268-271` : JSON puis texte |
| O-10 sans ligne | raison écrite, admise par l'adjudication | — |

**NPRIME-NUL-1, en détail** :
- **Reproduit, en 5 s** (`outils/nprime.py`, `journal/nprime.txt`) :
  - fixture : `executer.replication(P99, EP, cel(couche__grille="large", couche__repli=True), POINTS, 1, 1)`, avec
    `P99`, `EP`, `POINTS` et `cel` de `tests/test_impressions.py` (cellule T-imp) ;
  - n′ de stress = 0 pour n_s = 2 736, et la réplication lève REGLE/entier (« n = 0 : entier ≥ 1 attendu ») ;
  - sans repli à i = 1, n′ vaut 2 543 ; avec repli, i = 0, 2 et 3 n'ont pas de n′ nul.

  Le constat de la ligne est donc exact, et le test demandé peut partir de cette recette.
- **À préciser** :
  - « à n′_s = 1 le moteur rend [unites, k_crit, runs, n_prime] », et la recommandation « celles de n′_s = 1 »,
    dépendent des séries. Mesuré par `regle.tester` à n = 1 : 10 unités à 1 donnent [runs, n_prime] ; 0 ou 1 unité
    donne [unites, k_crit, runs, n_prime]. La ligne doit écrire la liste explicite.
  - Celle que donne la garde à n′ = 0 est [unites, k_crit, runs, n_prime] : unites 0 < 2 ; C1 = 0 ≤ seuil ; runs 0 < 2 ;
    2·0 < n_s [inféré de `regle._valeur`, l.163-166].
  - « code dans `regle`, sous-lot SB-7 » préjuge du lieu du correctif. Le §11 du même rapport disait
    `executer.replication`. Le lieu est à laisser au G0 du correctif.

**BUDGET-SERRE-1, recomptes** :
- 13 cellules sur 18 avaient un lot de 5 401 à 5 418 s sous l'ancienne formule ;
- Σ des 17 coûts à i = 0 = 234,34 s, et 200 × 234,34 = 46 868 s ≈ 13,02 h ;
- `duree_ns` sous-estime le temps de mur de moins d'un coût. C'est exact sous C-1 : tous les lots sauf le dernier sont
  des multiples de `processus` ;
- 131, 5 371, 5 412, 524, 9 956, 526 et 4 ont été recomptés.

## 8. Constats neufs

- **O-CC-1, mineure (réserve R-1)** : le nouveau `test_budget` à (12, 5) ne tue plus « coût = première mesure »
  (M-CC-08). Ce mutant est vivant sur e11v et tué sur e11u, où les durées étaient (5, 12).
  - Le §15.2 dit « aucun test affaibli », ce qui est inexact au niveau des mutants.
  - Origine : la prescription « durées (12, 5) » de la G2 (C-1) et de l'adjudication. Avec deux mesures, le maximum est
    toujours premier ou dernier.
  - Remède : trois mesures, maximum au milieu (par exemple (5, 12, 7)), ou les deux ordres.
- **O-CC-2, mineure (R-2)** : dans C-5, le cas « hors de l'ordre » [ETH, BTC] est aussi refusé par « BTC en tête ». La
  garde d'ordre n'est donc pas isolée, et M-CC-09 vit.
  - Origine : la prescription du §5 de la G2.
  - Remède : [BTC, USDT, ETH] → CELLULE/schema.
- **O-CC-3, moyenne (R-3)** : le R de la cellule est passé à cinq sites, et C-8 en couvre trois. Les deux autres ne sont
  pas couverts :
  - le calcul « avec » du critère collectif (`executer.py`, `_tester`) : M-CC-03 vit, car C-8 tourne sans absorption ;
  - `variante.tester` à i ≥ 200 : M-CC-04 vit, car C-8 tourne à i = 0.

  C'est le motif de G-11. Remède : C-8 avec `absorption` et une réplication i ≥ 200, avec des espions sur
  `regle.oracle`, `regle.tester` et `variante.tester`.
- **O-CC-4, moyenne (R-4)** : le W de la cellule passé à `fond` n'est testé à aucun W ≠ 1. Il porte la durée de dérive,
  W·tendance_par_semaine (E-S-13). À W = 1, (W + 1) // 2 = W : la fixture est équivalente, et M-CC-05 vit.
  - C'est le motif de G-06, hors de L-2.
  - Remède : `cellule(…, W)["fond"]["derive"]["duree"]` = W·tendance, pour W = 16 et 2.
- **O-CC-5, info** : M-11V-02 (`observateurs.Couche` sur le prm du lot) est équivalent pour le comportement. En effet,
  `observateurs.py` ne lit ni `longues` ni `poids_longues` (grep : 0 occurrence). Il est tué par l'espion de C-7, qui
  contrôle l'argument et non un effet. Il faut le compter comme mutant de site d'appel, pas comme preuve de
  comportement.
- **O-CC-6, mineure (R-5)** : la ligne d'item NPRIME-NUL-1 est à préciser (§7). Il faut y écrire :
  - la liste explicite des causes ;
  - la recette de reproduction ;
  - le lieu du correctif laissé au G0.
- **O-CC-7, info** :
  - C-9 et C-6 prennent leur attendu dans le code sous test : l'appel de référence de `pauses_c1`, et le `n` de
    l'enregistrement. C'est la forme que prescrit l'adjudication.
  - Dans C-6, la garde « n′ de calme < 12 000 » protège contre un mutant qui changerait de concert le n et les appels.
  - Dans C-9, aucun attendu n'est écrit à la main : à signaler à la règle « valeurs de référence indépendantes du
    code ».

## 9. Écarts du contre-contrôleur

- **E-CC-1** : j'ai fait `git init` avec alternates vers `/home/user/shogen/.git/objects` dans mes copies `w`, `wu`, `t`
  et `tn` (pour `oracle_r1` et xtask), comme E-R5 et E-C6. Je n'ai fait aucun `git add`. Le dépôt réel n'a rien reçu.
  Les copies sont supprimées.
- **E-CC-2** : des barres obliques inverses ont été tapées dans des commandes, jamais pour écrire un fichier du lot :
  - `tr` pour afficher `/proc/PID/cmdline` ;
  - des sauts de ligne dans des chaînes Python de retouche de mes outils (`campagne_cc.py`, `nprime.py`).

  Les fichiers écrits ont été comptés par Python : 0 octet 92 dans tous mes outils.
- **E-CC-3** : le premier lancement de `outils/nprime.py` (09:16:14) a échoué sur l'import (`calendrier` hors de
  `sys.path`). Il n'avait rien calculé. J'ai corrigé l'outil par un `sys.path` sur le dossier courant, puis relancé à
  09:16:22. Seul ce second passage compte.
- **E-CC-4** : `campagne_cc.py` a été modifié entre la campagne 1 et la campagne 2, pour prendre la copie et le
  plancher en argument (`wu` est à 246). La campagne 1 a tourné sur la version d'origine (copie `w`, plancher 252
  figé). Les deux versions ont la même commande de job.
- **E-CC-5** : `pgrep -n -f` sur le nom exact de chacun de mes scripts détachés, suivi de la lecture de
  `/proc/PID/cmdline`. Aucun motif large.

## 10. Journal de provenance (G1)

**Lu [lu]** :
- en entier : `ADJUDICATION-G2.md`, `g2/RAPPORT-G2.md`, `g2/preuves/test_preuves_g2.py`,
  `g2/outils/{mutants_g2,campagne,chaine,preuves,preuves2,xtask}`, `RAPPORT-GENERATEUR.md` §15, `BRIEF-SB11.md` et
  `diffs/SB-11v.diff` ;
- dans l'état e11v :
  - `executer.py` l.1-60, 60-100, 100-588 ;
  - `e1.py` : `pauses_c1`, `lignes_pauses`, `ecrire_e1`, `_vals` ;
  - `regle.py` l.99-136, 140-246, 329-337 ;
  - `calendrier.retenues` et `segments` ;
  - `commun.py` l.203-231 (par grep) ;
  - `oracle_r1.extraire` ;
  - les fixtures de `test_cellules`, `test_replication`, `test_pauses` et `test_impressions` (N5) ;
- `parametres.json` : `regle`, `e1`, `n_par_semaine`, `longues` ;
- le README de `sim-bis` (ligne `executer.py`) ;
- `gates.yml` : lignes des jobs.

**Seconde main [2nd]** :
- `RAPPORT-GENERATEUR.md` §10 (E-14), §11 et §6 (M-11P-03, M-11U-05) ;
- `journal/budget.txt` et `journal/corr/plan-budget-c1.txt` (durées), lus comme des données ;
- `g2/journal/xtask-tete.txt` et `journal/corr/xtask-tete-v.txt`, pour comparaison.

**Commandes** :
- `sha256sum -c` ×2 ;
- `git archive` ×3 (5e386c4 ; 1a388e1 ×2) ;
- `patch -p1` (base et tête), `patch -R` ;
- `diff -rq` et `cmp` contre `etapes/` et `fusion/` ;
- les outils `rouges.py`, `preuves_cc.py`, `campagne_cc.py`, `chaine_cc.sh`, `chaine_cc2.sh`, `nprime.py` et
  `gates_cc.sh`, avec leurs sorties dans `journal/` et `mut/` ;
- `TestLoader` sur `w`, `wu` et `t` ;
- les comptes d'octets 92, de longueurs de ligne et de marqueurs R-13 (Python).

**Recomptés par moi** :
- 112 lignes ajoutées et 15 retirées ;
- les planchers 246, 252 et 268 ;
- les attendus de C-1 ;
- les chiffres de BUDGET-SERRE-1 ;
- 13 lots sur 18 au-delà de la borne ;
- le bilan des mutants (12 + 1 + 9 ; 17 tués, 5 vivants) ;
- les Ran de chaque job ;
- l'identité des dix lignes xtask.

## 11. Vérification de SB-11w (section datée du 2026-10-09, 10:36:05 à 11:14:19 UTC)

**Gate 0** : modèle résolu `claude-opus-5-5`. Je n'ai écrit ni SB-11w ni le §16 du rapport du générateur.

**Verdict final sur le sous-lot SB-11 (a … w) : CONFORME.** SB-11w lève les réserves R-1 à R-4 (C-10 à C-13 de
l'ajout daté d'`ADJUDICATION-G2.md`) :
- chacun des cinq mutants visés est tué par un FAIL d'assertion du test retouché ;
- aucun mutant que ces tests tuaient déjà ne survit ;
- les gates sont aux planchers exacts.

R-5 (ligne NPRIME-NUL-1) reste à l'orchestrateur, au versement, comme le prévoit l'adjudication.

### 11.1 Pièces et application
- **Pièces** :
  - `diffs/SB-11w.diff` a pour sha256 `5de3fd63040870a995957651f1dfd3b5817b14e41607e5e5a2789c564ab490c3`, comme
    demandé ;
  - `sha256sum -c SHA256SUMS` donne 1 510 OK et 0 échec ;
  - `ADJUDICATION-G2.md` a désormais pour sha256 `7330cc58…` (ajout daté) ;
  - le §16 de `RAPPORT-GENERATEUR.md` a été lu comme une donnée.
- **Forme de SB-11w** : tests seuls, sur `test_budget`, `test_cellules` (C-4/C-13, C-5/C-11) et `test_replication`
  (C-8/C-12).
  - 37 lignes ajoutées et 26 retirées, recomptées ;
  - 0 octet 92 dans le diff et dans `scripts/sim-bis` ;
  - aucune ligne `.py` de plus de 120 caractères ;
  - aucune méthode neuve : `TestLoader` donne 252, et `gates.yml` n'est pas touché.
- **Base + a … w** :
  - 5e386c4 par `git archive` (exclusions du brief), puis les 23 diffs en `-p1`, sans rejet ;
  - le résultat est égal à `etapes/e11w` (`diff -rq` et `cmp` vides) ;
  - job sim-bis `--plancher 252` : conforme, Ran = 252 (132 s).
- **Assertions retirées par w** : elles sont toutes remplacées par des assertions plus serrées.
  - `test_budget` passe à (5, 12, 7), et l'attendu est complet.
  - C-4 garde la perte et ajoute la durée de dérive.
  - C-8 garde ses trois listes, dans l'attendu à i = 0.

### 11.2 Corrections C-10 à C-13 : rouges rejoués

Chaque rouge est le test seul sous le mutant, et c'est un FAIL d'assertion sans aucune ERROR (`journal/rouges-w.txt`).
Sans mutant, les quatre tests retouchés donnent Ran 4, OK.

| C (réserve) | mutant | rouge d'assertion | règle de fixture |
|---|---|---|---|
| C-10 (R-1) | M-CC-08 `m = ns[0]` | ns_max 5 au lieu de 12 | durées (5, 12, 7) : le maximum n'est ni premier ni dernier |
| C-11 (R-2) | M-CC-09 garde d'ordre retirée | None au lieu de CELLULE/schema pour [BTC, USDT, ETH] | BTC en tête, seul l'ordre est en défaut ; garde : [BTC, ETH, USDT] passe |
| C-12 (R-3) | M-CC-03 R du prm au calcul « avec » | oracle [999, 99, 999, 99] au lieu de [999]×4 | absorption active, R 999 contre 99 |
| C-12 (R-3) | M-CC-04 R du prm à `variante.tester` | i = 200 : [99, 99] au lieu de [999, 999] | réplication i = 200 |
| C-13 (R-4) | M-CC-05 `fond(…, (W + 1) // 2)` | (16, 80 640) au lieu de (16, 161 280) | W = 16 et 2 |

Attendus de C-13 : 16·10 080 = 161 280 et 2·10 080 = 20 160, où 10 080 est `sources.derive.tendance_par_semaine`, lu
dans `parametres.json`.

### 11.3 Mutants, commande du job

Commande : `verdict-suite-s2.py scripts/sim-bis --aucun-saut --egal --plancher 252`, sur base + a … w, avec un arbre par
mutant, sous `isole.sh` et `timeout 300`, en PAR=2.
- Chaîne `sh outils/chaine_cc3.sh`, PID 24569, de 10:37:44 à 11:07:32 UTC.
- Témoins VIVANT (Ran 252) : 138 s et 129 s.
- **14 sur 14 tués**, chacun par AssertionError. Aucune ERROR, aucun FATAL. Le plus long a pris 227 s.

| groupe | mutants | tué par |
|---|---|---|
| réserves | M-CC-03, M-CC-04 | test_r_de_la_cellule |
| réserves | M-CC-05 | test_l_2_au_site_d_appel |
| réserves | M-CC-08 | test_budget |
| réserves | M-CC-09 | test_schema_ferme_c_5 |
| non-affaiblissement | G-06 | test_l_2_au_site_d_appel |
| non-affaiblissement | G-08 | test_schema_ferme_c_5 |
| non-affaiblissement | G-11 | test_r_de_la_cellule |
| non-affaiblissement | G-22 | test_budget |
| non-affaiblissement | ANCIENNE (= M-11V-01) | test_budget, test_plan_90_min |
| neufs, sur les tests de w | M-CC-10 : durée de dérive à W fixe 16 | test_l_2_au_site_d_appel (W = 2 : 161 280 au lieu de 20 160) |
| neufs, sur les tests de w | M-CC-11 : « avec » par `regle.tester`, sans l'oracle d'E-S-29 | test_r_de_la_cellule |
| neufs, sur les tests de w | M-CC-12 : garde d'ordre seulement jusqu'à deux classes | test_schema_ferme_c_5 |
| neufs, sur les tests de w | M-CC-13 : coût = médiane | test_budget (7 au lieu de 12) |

M-CC-11 ne change pas les valeurs : il retire le contrôle d'oracle sur « avec ». Il est tué par le compte d'appels.
M-CC-13 aurait survécu à la fixture (12, 5) de v, où la médiane vaut 12 : c'est la (5, 12, 7) de w qui le sépare.

### 11.4 Gates
Toutes l'une après l'autre (`outils/gates_cc_w.sh`, PID 15765, de 11:07:44 à 11:13:52 UTC), sur `t2` = `git archive
1a388e1` + a … w résolue :

| contrôle | résultat |
|---|---|
| runner | 136 ok, 0 échec |
| sim-bis `--plancher 268` | conforme, Ran = 268 |
| s2bis `--plancher 340` | conforme, Ran = 340 |
| S2 `--egal` | conforme, Ran = 415, deux sauts qui nomment la variable scellée |

**Application sur `1a388e1`** :
- rejets connus seulement : le plancher sim-bis à a … v, et la ligne README à 20 diffs (ni s, ni v, ni w) ;
- **SB-11w s'applique sans rejet** ;
- résolution à neuf : plancher 268, et les deux lignes README après `oracle_recalc.py` ;
- `t2` ne diffère de `fusion/` que par les six fichiers de v/w et les planchers ;
- `TestLoader` donne 268.

### 11.5 Avis sur O-W1
Le constat est juste, mineur, et ne bloque pas.
- M-11T-07 retire le refus EXEC/budget. `max([])` lève alors ValueError dans `assertRaises(commun.Refus)` : le test
  finit en ERROR, pas en FAIL.
- La forme existe depuis SB-11t (`etapes/e11t/…/test_budget.py:32`). SB-11w n'y touche pas : c'est hors de C-10 à C-13.
- Le mutant est bien détecté : sortie 1, que le contrat MUT-FATAL classe « tué ». Mais il ne l'est pas par un rouge
  d'assertion, et une autre exception y ferait la même ERROR.
- Remède : la forme `code_de` des autres fichiers (`assertEqual(code_de(executer.budget, [], 10, 2, 30), "EXEC/budget")`).
  Je recommande de la joindre à MUT-EQUIV-FIXTURE-1 ou au brief de SB-12, comme le propose le correcteur.

### 11.6 Écarts de cette vérification
- **E-CC-6 : la tête a changé pendant le contrôle.** Relue à 11:14:01, elle valait `c961382` (six commits CALIB-ACTIFS
  CA-0a à CA-1c) au lieu de `1a388e1`, et `status --porcelain` comptait 6 entrées, d'un autre agent ; je ne les ai pas
  lues.
  - Sur les chemins de la série, seul `gates.yml` a changé : 20 lignes ajoutées, un job calib-actifs. `scripts/sim-bis`
    est inchangé.
  - Rejeu de l'application sur `gates.yml` + `scripts/sim-bis` de `c961382` (`journal/application-c961382.txt`) : mêmes
    rejets, w sans rejet. Les planchers de la tête sont inchangés (sim-bis 210, s2bis 340) : la résolution à 268 vaut
    toujours.
  - Les gates de §11.4 ont tourné sur `1a388e1`, pas sur `c961382`.
- **E-CC-7** : `git init` avec alternates dans les copies `w2` et `t2` seules, sans `git add`. Ces copies sont
  supprimées.
- **E-CC-8** : des barres obliques inverses tapées pour `tr` (affichage de `/proc/PID/cmdline`). Les fichiers écrits
  contiennent 0 octet 92 (compte Python).
- **E-CC-9** : `rouges_w.py` est dérivé de `rouges.py` par un script Python, et `mutants_cc.py` a reçu M-CC-10 à 13.
  Les G-xx, M-CC-03, 04, 05, 08 et 09 sont inchangés.

### 11.7 Provenance (G1)
- **Lu [lu]** :
  - `diffs/SB-11w.diff` en entier ;
  - `RAPPORT-GENERATEUR.md` §16 ;
  - l'ajout daté d'`ADJUDICATION-G2.md` ;
  - `test_budget.py` l.33-37 (e11w) ;
  - `executer.py` l.290 et 352 ;
  - `parametres.json` (`tendance_par_semaine`) et `sources.GENRES`.
- **Seconde main [2nd]** : le §16 du générateur (campagne, sonde de C-12, gates hooks, secrets, R-1 et matrice), que je
  n'ai pas rejoués.
- **Commandes** :
  - `sha256sum -c` ;
  - `git archive` de 5e386c4, 1a388e1, et `c961382` limité à `gates.yml` + `sim-bis` ;
  - `patch -p1` ;
  - `diff -rq`, `cmp` ;
  - `rouges_w.py`, `chaine_cc3.sh` et `gates_cc_w.sh` ;
  - `TestLoader` ;
  - les comptes d'octets 92 et de longueurs de ligne.
- **Recomptés par moi** : 37 et 26 lignes ; 252 et 268 ; 161 280 et 20 160 ; le bilan des 14 mutants ; le Ran de chaque
  job.
