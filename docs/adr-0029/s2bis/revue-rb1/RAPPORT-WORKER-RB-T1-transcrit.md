# Rapport du worker — P3 du recalcul, tranche 1 (transcrit)

> Transcription par l'orchestrateur le 2026-10-05 05:42:46 UTC du rapport rendu par message par le worker (agent a01774b5f2895a7e9) ; contrôle FM-1.1 du transcript : fragments_l51_l14 = 0. Texte du worker ci-dessous, sans retouche.

# Rapport du worker : P3 du recalcul de S2-bis, tranche 1 (RB-0, RB-1, RB-6)

**Gate 0** : modèle `claude-opus-5-5`, effort max (fiche `shogen-worker`). Travail du 2026-10-05, de 04:04:35 à 05:40:47 UTC (`date -u`). Rapport rendu par message.

## Résumé

Les trois sous-lots sont livrés en **7 diffs en série**, chacun sous 200 lignes de code ajoutées, tests compris. Ils sont classés dans l'ordre RB-0a, RB-0b, RB-6a, RB-6b, RB-1a, RB-1b, RB-1c.

- **Suite `s2bis`** : de 114 à **144 tests**, sans saut. Le plancher du job `s2bis-unittest` est relevé à chaque diff, avec `--egal`.
- **Tests d'abord** : pour chaque diff, j'ai montré un rouge fait seulement d'échecs d'assertion (aucune erreur), puis le vert.
- **Mutants** : **122 nommés, 122 tués par leur test visé, 0 vivant, 0 FATAL** sur les passages valides. Ils sont classés par la commande du job : runner, puis ligne de `gates.yml`, borne de 300 s, réseau isolé.
- **Contrôles finaux** : 3.10 à 3.13 en `-X dev -W error` OK ; `s2-harness` à 405 tests, OK (skipped=2) ; hooks 54 ok ; gate des secrets OK ; R-13 : 0.
- **`xtask verify`** : mes lignes de verdict sont identiques à celles du témoin. S-G1 à S-G8 sont vertes ; S-G9 est rouge sur `docs/17:70`, cas connu sur les copies.
- Bibliothèque standard seule. Aucun journal réel lu ; seulement des journaux synthétiques écrits par l'écrivain de `collecte/journal.py`.

Il reste **15 questions Q-RB-n** à trancher et **8 items** que je propose de former (règle PAROXYSME).

## 1. Livraison

**Base** : `122c670`, relevée par `git --no-optional-locks rev-parse` ; égale à la tête au début du lot. La copie est faite par `git archive` avec les exclusions du brief.

**Tête à la fin** : `3164348`, soit 13 commits SIM-BIS et un ajout daté au G0 de COLLECTE sur l'accord des parties, sans effet technique ici. La série **s'applique aussi sur cette tête** (vérifié avec `git apply`). Sur la base, la série redonne l'arbre final à l'identique (vérifié avec `diff -r`).

Les diffs sont dans `<scratchpad>/s2bis/rb1/diffs/`.

| diff | objet | code ajouté | plancher | mutants |
|---|---|---|---|---|
| RB-0a | sous-paquet `recalc`, sa règle de frontière, `config_analyse.py` : lecture JSON stricte, blocs à fixer, schéma | 199 | 117 | 21/21 |
| RB-0b | τ (0,05 % ≤ τ < 2,85 %), planchers de σ, fractions, noms d'unité, cohérence, gabarit `s2bis/config/analyse.json` | 128 | 122 | 20/20 |
| RB-6a | `rotation.py` : o(r, u) (AVIS Q-R-02), refus nommés, `tourner` | 102 | 125 | 18/18 |
| RB-6b | `compter`, `resume`, `lois` : K, S, C, K_crit, moyennes exactes, rotations jointes par hôte | 140 | 130 | 17/17 |
| RB-1a | `lecteur.py` : ligne intègre au sens de l'écrivain, causes nommées, entier de plus de 640 chiffres, ordre des fichiers | 159 | 134 | 20/20 |
| RB-1b | lecture en flux, genèse, lien entre fichiers, ruptures et ancre, queue finale | 189 | 141 | 16/16 |
| RB-1c | déclaration exacte des queues par la `reprise`, mémoire bornée (`tracemalloc`) | 64 | 144 | 10/10 |

Total : **981 lignes**. Documents hors compte :
- sections RB-0a à RB-1c de `METRIQUES-S2BIS.md`, avec le tableau des fonctions de fitness mis à jour ;
- nouveau `docs/adr-0029/s2bis/ROTATION-S2BIS.md` (voir Q-RB-12).

**Fichiers neufs à l'état final** :

| fichier | lignes |
|---|---|
| `s2bis/shogen_s2bis/recalc/__init__.py` | 1 |
| `s2bis/shogen_s2bis/recalc/config_analyse.py` | 143 |
| `s2bis/shogen_s2bis/recalc/rotation.py` | 107 |
| `s2bis/shogen_s2bis/recalc/lecteur.py` | 142 |
| `s2bis/config/analyse.json` | 12 |
| `s2bis/tests/test_config_analyse.py` | 151 |
| `s2bis/tests/test_rotation.py` | 133 |
| `s2bis/tests/test_lecteur.py` | 248 |

`test_fitness.py` gagne 9 lignes.

**SHA256SUMS** : `…/rb1/SHA256SUMS`, 112 lignes, sha256 `fe0e16b6…1431`, contrôlé par `sha256sum -c`. Empreintes des diffs :

| diff | sha256 |
|---|---|
| RB-0a | `f6d09637…5f63` |
| RB-0b | `da1e7446…eba6` |
| RB-6a | `15de17a0…6d73` |
| RB-6b | `89e4c806…6b83` |
| RB-1a | `7c26470d…8c58` |
| RB-1b | `c53ba709…8c58` |
| RB-1c | `33df1519…0145` |

Les preuves sont dans `…/rb1/preuves/` : rouge, vert, job, runner et mutants de chaque diff, plus les contrôles finaux. Les outils (lanceur de campagne, script des vecteurs, mesure de coût, diffs) sont dans `…/rb1/outils/`. Les sources, souches et mutants sont dans `…/rb1/travail/`.

Le plancher final est **144** ; la ligne à committer est `verdict-suite-s2.py s2bis --aucun-saut --egal --plancher 144`.

## 2. Contrat de RB-6 pour l'oracle croisé SB-13

Le contrat est écrit dans la docstring de `rotation.py` et dans `ROTATION-S2BIS.md`.

**Entrées** :
- graine : 64 caractères hexadécimaux minuscules, la forme imprimée ;
- strate : `calme` ou `stress` ;
- `n` : longueur de la suite retenue ;
- positions t = 0…n − 1, dans l'ordre chronologique ;
- masques : entiers, bit t = D(u, t), 0 ≤ m < 2^n ;
- unités : ASCII imprimable sans « : » ;
- `premiere` : une unité ou None ;
- R ≤ 9 999 et seuil, fournis par l'appelant depuis `analyse.json`.

**Calcul** :
- o(r, u) = SHA-256 des octets UTF-8 de `graine:strate:r:u`, lu en big-endian, mod n ;
- la valeur de la position t va en (t + o) mod n ;
- la classe n'entre jamais dans le décalage.

**Signature** : `lois(graine, strate, n, classes, premiere, R, seuil)`.

**Sortie** : `{classe: {K, C, K_crit, K_moyen, K_r, S, C_S, S_crit, S_moyen, S_r}}`, classes triées ; `K_r[r−1]` = K^(r) ; les moyennes sont des `Fraction` exactes.

**Vecteurs** : 6, calculés sans Python (`printf | sha256sum`, puis `bc`), dont o = 0 et o = n − 1, et un modulo n′ = n/2 (52 807).

**Coût mesuré** (machine partagée, charge ≈ 3 sur 4 cœurs) :

| | calme, 1 classe | calme, 4 classes | stress, 1 classe | stress, 4 classes |
|---|---|---|---|---|
| Python 3.12.3 | 7,5 s | 17,2 s | 2,5 s | 6,1 s |
| Python 3.10.20 | 6,7 s | 15,7 s | 2,2 s | 5,7 s |

Les deux versions donnent les mêmes K, C et K_crit.

## 3. Questions Q-RB-n : valeurs non fixées par le G0 (proposition entre parenthèses, appliquée)

1. **Q-RB-1** : la frontière de `recalc` n'admet que `collecte.decodeurs` (PROPOSITION §1 pt 2). J'ai donc **recopié** la lecture JSON stricte de `collecte/config.py` (l.20-46, adaptée). Proposition : garder la copie. L'alternative, admettre `collecte.config`, desserre la frontière : c'est votre décision.
2. **Q-RB-2** : format d'`analyse.json`. Proposition :
   - blocs `degradation` (secondes entières ; `d4_echecs` de 1 à 3, `d5_echecs` de 1 à 2), `gardes`, `n_s` par strate, `t_max_s`, `rotations`, `tolerance_evenements`, `p_j`, `tau_sigma[actif][classe]`, `unites[classe]` ;
   - `t_max_s` en secondes, multiple de 60 ;
   - τ et P_j en fractions décimales écrites en chaîne, comme le τ de S2 (`run_campaign.py` l.120-129).
3. **Q-RB-3** : noms des classes de source. Proposition : `place_horodatee`, `sans_horodatage`, `agregateur`, `oracle_chainlink`, soit S2 sans `oracle_pyth`. Ces noms doivent être repris tels quels dans `formes.json` (CB-6 à CB-9, E-C-08).
4. **Q-RB-4** : contrôles de σ et de τ.
   - σ est null exigé pour les places sans horodatage, et n'a pas de borne haute.
   - Les planchers de τ des oracles poussés (0,75 % pour ETH, 0,375 % pour les stables, l.188) et la grille de 0,05 % ne sont **pas** contrôlés : E-R-09 ne fixe que la borne CAPO.
   - Proposition : resserrement possible, sur votre décision.
5. **Q-RB-5** : ordre des unités. Proposition : ordre strict des points de code, comme lecture exacte de « ordre alphabétique » (l.200) ; avec des noms DNS, `api-pub.` précède `api.` (recalculé : 0x2D < 0x2E). Les pools d'ETH, d'USDC et d'USDT sont inclus dans celui de BTC (l.173). `premiere` est calculée à RB-7.
6. **Q-RB-6** : R et seuil. J'ai mis une borne R ≤ 9 999 et la cohérence alpha (seuil + 1)·100 = R + 1, plutôt que des valeurs exactes. Le gabarit porte 9 999 et 99, contrôlés par test.
7. **Q-RB-7** : gardes. Proposition : `{unites, k_crit, runs, diviseur_n}`, entiers ≥ 1, et n′_s ≥ n_s/`diviseur_n`. Le gabarit porte 2, 2, 2, 2 (l.203).
8. **Q-RB-8** : gabarit. Les blocs fixés par les lots amont sont à null (`n_s`, `t_max_s`, `tau_sigma`, `tolerance_evenements`, `unites`), et le chargeur refuse alors avec `ANALYSE/a-fixer`. Qui les remplit :
   - SIM-PUISSANCE-BIS : n_s et T_max ;
   - SIM-BIS (Q-S-18) : la tolérance ;
   - TAU-SIGMA-S2BIS et CALIB-ACTIFS : τ et σ ;
   - CALIB-ACTIFS et `formes.json` : les unités.
9. **Q-RB-9** : entier JSON trop long. La borne est **640 chiffres**, la plus petite valeur non nulle d'`int_max_str_digits` ; le lecteur ne dépend donc pas du réglage de l'interpréteur (testé à 0, 640 et 4 300). J'ai lu le « refus nommé » d'E-R-01 comme une **cause nommée de non-intégrité de la ligne** (queue, ou rupture si quelque chose suit), et non comme l'arrêt de toute la lecture.
10. **Q-RB-10** : portée d'une rupture qui n'est pas suivie d'une `reprise` (altération puis bascule normale). Le lecteur prend comme ancre le premier enregistrement du fichier suivant. L'AVIS (Q-R-03) ne vise que le segment de reprise. Proposition pour RB-3 : la portée va jusqu'au premier marqueur qui suit l'ancre.
11. **Q-RB-11** : S_crit est défini comme K_crit ; l.212 le nomme sans le définir.
12. **Q-RB-12** : le contrat de rotation (bit t = position t, R et seuil en paramètres) est à transmettre à SIM-BIS. J'ai créé le document `ROTATION-S2BIS.md`, qui porte aussi les vecteurs au paquet (AVIS Q-R-02).
13. **Q-RB-13** : noms d'unité. La lettre de l'AVIS (ASCII imprimable sans « : ») admet l'espace. Faut-il resserrer aux caractères d'un nom d'hôte ?
14. **Q-RB-14** : mutants obligatoires de la rotation (§3.4).
    - Le mutant « modulo n_s au lieu de n′_s » ne peut pas s'écrire dans RB-6, qui ne reçoit que n. Je l'ai rejoué sous la forme « modulo autre que la longueur » (M-6a-05) ; la forme exacte est à refaire à RB-7.
    - « Classe dans l'entrée du hachage » est tué par l'API à classes jointes (M-6b-01).
    - « R = 9 998 » est tué deux fois (M-0b-18, M-6b-03).
15. **Q-RB-15** : une `OSError` du lecteur (fichier illisible) remonte telle quelle, sans refus nommé. Faut-il la laisser ainsi, ou la nommer `LECTEUR/illisible` à RB-2 ?

## 4. Items proposés (règle PAROXYSME)

- **I-1 SHOGEN-S2BIS-ENTIER-ECRIVAIN-1** : l'écrivain (`canonique`) écrit des entiers jusqu'à la limite de l'interpréteur (4 300 chiffres par défaut, et ce réglage peut changer). Une ligne de 641 à 4 300 chiffres est donc intègre pour l'écrivain mais forme une queue pour le lecteur. Remède : borne de 640 chiffres à l'écriture (une ligne), avant le gel du collecteur.
- **I-2 SHOGEN-S2BIS-FORMAT-INTEGRE-1** : FORMAT §7.1 ne dit pas les contrôles de type que fait `_lire` (`suivante`, `ws`, `a`, dernière fenêtre). Le lecteur les reprend. À écrire au FORMAT.
- **I-3 SHOGEN-S2BIS-ANCRE-RUPTURE-1** : l'ancre qui suit une rupture n'est vérifiée par rien d'extérieur au journal. Il faut la recouper avec les sommes (garde (3), RB-19) et avec les têtes horodatées (E-C-35, E-C-36).
- **I-4 SHOGEN-S2BIS-CONFIG-CROISEE-1** : rien ne contrôle la cohérence entre `analyse.json`, `formes.json` (unités, classes) et `sante.json` (nombre de témoins et de noms). À traiter à RB-2 ou à CB-18.
- **I-5 SHOGEN-S2BIS-ROTATION-COUT-1** : le coût n'est mesuré que sur des masques synthétiques. Il faut le re-mesurer à RB-11 et RB-12 (sensibilités, analyse conditionnelle).
- **I-6 SHOGEN-S2BIS-FRONTIERE-S2-1** : le mécanisme d'import de `shogen_s2` (chemin de `s2-harness`) et la granularité de sa liste fermée restent à fixer, la fitness lisant des modules et non des fonctions. Concerne RB-2, RB-4 et RB-9.
- **I-7 SHOGEN-S2BIS-P3-ESTIMATION-1** : sur cette tranche, la taille mesurée vaut ×1,85 l'estimation du G0. Détail au §7.
- **I-8 SHOGEN-S2BIS-ASSERT-DIFF-1** : `assertEqual` sur des structures de milliers d'éléments fait calculer à `unittest` un diff `difflib` qui pend jusqu'à la borne. Consigne proposée : ces assertions doivent échouer vite.

## 5. Écarts déclarés

- **E-1, découpage** : RB-0 en 2 diffs (le premier essai en un diff faisait 270 lignes), RB-6 en 2, RB-1 en 3.
- **E-2, passage invalide** : le premier passage de RB-6b est **invalide**. M-6b-01 a atteint la borne de 300 s (FATAL, non compté), à cause du diff de listes de 9 999 valeurs (voir I-8). J'ai arrêté **mes seuls processus** (PID 23584, groupe 27586) : un autre worker (`cb18`) tournait en même temps. J'ai ensuite corrigé l'assertion, refait le rouge et le vert, et relancé toute la campagne : 17/17. Le journal du passage invalide est conservé.
- **E-3, artefacts de souche** : deux rouges (RB-6b, RB-1a) comptaient d'abord une erreur due à la souche elle-même. J'ai corrigé les souches et refait ces rouges : seulement des échecs d'assertion.
- **E-4, ligne vide finale** : les états intermédiaires de `test_lecteur.py` (RB-1a, RB-1b) avaient une ligne vide en fin de fichier pendant leurs campagnes. Je l'ai retirée après, sans effet sur ce qui est testé, puis j'ai régénéré les diffs et refait la vérification en série.
- **E-5, git hors du dépôt du projet** :
  - la gate des secrets a tourné en mode `--tree` dans un index **jetable** du scratchpad (`git init` et `git add` des 13 fichiers touchés, aucun commit) ;
  - le runner des hooks crée ses propres dépôts sous `mktemp`, par conception ;
  - sur `/home/user/shogen`, seulement de la lecture : `rev-parse`, `log`, `archive`, `diff`.
- **E-6, contrainte partagée** : la machine était partagée avec deux autres workers ; les durées en portent la trace.

## 6. Contrôles finaux

Toutes les preuves sont dans `…/rb1/preuves/final*`.

- **Interpréteurs** : Python 3.10.20, 3.11.15, 3.12.3 et 3.13.14 en `-X dev -W error` : 144 tests, OK, aucun avertissement imprimé.
- **Ligne du job** sous les quatre interpréteurs : « conforme (… aucun saut, Ran = 144) ».
- **Runner** : 33 ok.
- **`s2-harness`** : « Ran 405 tests … OK (skipped=2) », inchangé.
- **Hooks** : 54 ok.
- **Gate des secrets** : « OK (secrets) : 12 fichier(s) ».
- **R-13** : 0.
- **`cargo --locked xtask verify`**, hors réseau : lignes de verdict identiques au témoin, avec S-G9 rouge sur `docs/17-modele-de-menace.md:70` (référence vers `docs/rapports/`, exclu des copies).

## 7. Estimation révisée

| sous-lot | estimation du G0 | mesuré |
|---|---|---|
| RB-0 | ≈ 150 | 327 (×2,2) |
| RB-1 | ≈ 190 | 412 (×2,2) |
| RB-6 | ≈ 190 | 242 (×1,3) |
| total | ≈ 530 | 981 (×1,85) |

Sous-lots restants, au même rapport :
- **P3** (RB-2 à RB-5, RB-7, RB-8) : ≈ 1 110 → **≈ 2 050 lignes**, soit P3 complète ≈ 3 030 au lieu de ≈ 1 640 ;
- **P4** (RB-9 à RB-20) : ≈ 2 160 → **≈ 4 000 lignes** ;
- au total, ≈ 6 050 lignes, soit 31 à 35 diffs.

RB-7 attend toujours la clôture de conception de SIM-NIVEAU-BIS (adjudication pt 3). SB-13 (oracle croisé avec RB-6) peut commencer.

## 8. Journal G1 (provenance)

**Pièces lues [lu]** (préfixe du sha256 à `122c670`, puis lignes lues) :
- brief `29d75bd2` ;
- G0 `56f9ca73`, en entier ;
- PROPOSITION `0cdf84c2`, en entier ;
- AVIS `a919b307`, en entier ;
- ADR-0029 `b908842d` : l.1-262 et l.377-401 ; ajouts datés repérés par recherche dans ce seul fichier ;
- FORMAT `08c6b20e`, en entier ;
- G6-PAQUET `2e690eb1` ;
- METRIQUES `4c972ca3` ;
- G0-SIM-BIS `d9cffc0a`, en entier ;
- PROPOSITION SIM-BIS `0e78afab`, par extraits : l.40-60, 150-230, 360-380, 450-520 ;
- AVIS SIM-BIS `aaf70a4f`, l.60-80 ;
- annexe B `245f0b40`, l.42-43, 45, 55, 354-355, 762, 802, 1014, 1042-1043 ;
- revue P1-B : brief `0ee2c928` et rapport `b9920e41` ;
- `s2bis` : `journal.py` `958f5a8d`, `config.py` `77f909e5` ; tests `__init__` `9be14d84`, `test_fitness` `93e1aaf6`, `test_garde` `96b65812`, `test_config` `65f1fc93`, `test_reprise` `4c80609f`, `test_journal` `87804f34`, `test_fichiers` `1c314a8d` ;
- `s2-harness` : `r1.py` `c5666e8d` (l.1-215), `sources.py` `0c81fc33` (l.320-345), `run_campaign.py` `12db6c84` (l.82-200), `records.py` `a2e9a774` (`read_jsonl_tolerant`) ;
- `verdict-suite-s2.py` `83271f84`, runner `2778270f`, `gates.yml` `2f9f9c43` ;
- en-têtes de `sg4.rs` `b0f7f125`, `sg5.rs` `e2629451`, de `gate-secrets.sh` et de `run-fixtures-hooks.sh` ;
- outils du réviseur : `lo_up.py` `b532be4b`, `isole.sh` `ebaa1c78`, `campagne_job_g2.py`, `versions.sh`.

**[2nd]** : rien n'est fondé au second degré. **[abs]** :
- définition de S_crit ;
- format d'`analyse.json` ;
- noms des classes de source au collecteur (`formes.json` absent) ;
- portée d'une rupture sans reprise.

**Exposition** :
- aucune pièce de D.2 ouverte, aucun `*.jsonl`, aucun dossier interdit ;
- `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée (`isole.sh` la retire) ;
- aucune recherche récursive sur `docs/`, sur le dépôt ou sur le scratchpad ; recherches ciblées sur des fichiers nommés seulement.

**Commandes et sorties clés** :
- base : `Ran 114 … OK`, runner 33 ok ;
- `printf '%s' SHOGEN-RB6-VECTEURS | sha256sum` → `6fce4df7…9688` ;
- contrôle de `bc` : FF mod 7 = 3 ; (2^256 − 1) mod 109 440 = 13 695 par les deux voies ;
- vecteurs : 107 527, 24 225, 39 743, 0 (r = 1), 6 (r = 7), 52 807 ;
- `sha256sum` de VALIDE = `fcf18be5…cd14` (1 001 octets) ;
- consigne B.16 : octets contrôlés par `od -c` (une seule barre dans `r"0\.[0-9]{1,20}"`) ; mutants écrits avec `chr(92)` et `chr(127)`, aucune barre tapée dans les textes de remplacement.

**Chiffres recalculés** :
- 24 semaines = 14 515 200 s ; n_calme = 109 440 et n_stress = 43 776 (l.158) ;
- pics de `tracemalloc` : environ 24 Ko pour 500 enregistrements (167 Ko), 11 à 14 Ko pour 2 000 (670 Ko), sous 3.10 et 3.13 ;
- coûts du §2.

**Nettoyage** : copie, arbre, instantanés, cible cargo, copies d'essai et de rouge, et temporaires sont supprimés ; restent diffs, preuves, outils, travail, brief et SHA256SUMS.

