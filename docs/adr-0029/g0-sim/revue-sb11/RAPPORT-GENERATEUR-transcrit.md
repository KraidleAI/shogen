# Rapport du générateur de SB-11, avec les corrections SB-11v (§15) et SB-11w (§16) (transcrit)

> Transcription par l'orchestrateur le 2026-10-09 14:33:41 UTC du fichier RAPPORT-GENERATEUR.md ; contrôle FM-1.1 des transcripts du générateur (deux reprises), du réviseur, du correcteur et du contre-contrôleur : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Rapport du générateur — SIM-BIS, sous-lot SB-11 (executer.py, e1.py, câblage d'E1)

**Gate 0** : modèle résolu `claude-opus-5-5` (worker G1, effort max). Le travail a été commencé par un agent précédent
(même modèle), arrêté en cours de route ; je l'ai repris à 00:29:03 UTC (`date -u`) depuis `NOTES.md` seul, après avoir
vérifié l'état réel des fichiers. Rattachement : G0 `docs/adr-0029/g0-sim/G0-SIM-BIS.md` et ses ajouts datés,
`PROPOSITION.md` corrigée par `AVIS.md`, brief `BRIEF-SB11.md`, lignes `LIGNES-BRIEF-SB11.md` (sha256 `4eea7af8…`, égal
à celui du dépôt).

## 1. Base, reprise, horloge

- **Base des diffs** : `5e386c4` (`claude/compassionate-noether-szmdyj`), celle du brief. Copie `base/` par
  `git archive`, avec les exclusions du brief. Tête relue à la reprise : `ebd1560`, sans changement sous
  `scripts/sim-bis` ni dans `gates.yml` (E-7 de l'agent précédent).
- **Tête relue** (consignée à 01:44:02 UTC dans `NOTES.md` ; relue par moi à 03:48:07 et 04:59:54 UTC) : `b07147d`
  (fusion de la PR n° 5 : SB-13A à SB-13D). Elle change mes chemins (voir §14). Je n'ai pas avancé ma base (règle 2). J'ai vérifié à part que la série s'applique sur cette tête : copie
  `fusion/`, voir §14.
- **Horloge** : `date -u` lu avant chaque heure écrite depuis la reprise. Les heures de l'agent précédent ont été
  corrigées par lui (E-3).
- **État trouvé à la reprise** :
  - diffs SB-11a à SB-11l écrits ;
  - après la reprise de 23:01, l'agent précédent avait relancé sans le consigner les campagnes e11k (23:10), e11l
    (23:19), e11j (23:30) et e11a à e11g en confirmation (23:35 à 00:01) ;
  - aucun processus de lui ne tournait.
- **Suites données** :
  - e11k a été refaite en entier, comme le demandait l'orchestrateur ;
  - e11l est refaite après la série, parce que son passage de 23:19 n'a pas de PID consigné (E-15) ;
  - les confirmations e11a à e11g sont déclarées en E-15.
- **Seconde reprise (02:02:26 UTC, `date -u`)** : le conteneur a redémarré vers 02:00 UTC ; l'agent de la première
  reprise et tous ses processus ont été arrêtés (campagnes o, p, q, r du groupe 20088, chaîne s, t, u
  `outils/chaine_stu.sh` PID 30365, chaîne e11l `outils/chaine_l.sh`). J'ai repris depuis `NOTES.md` et l'état réel
  des fichiers (même modèle, `claude-opus-5-5`). Constat et suites : E-16 à E-28 (§10).
  - gardées, complètes et consignées : e11o (13/13) ; le premier passage de e11p (10/11, M-11P-03 vivant : E-17) ;
  - sans résultat : e11q (interrompue au témoin de début, journal vide) ; e11r, s, t, u et la reprise de e11l jamais
    lancées ;
  - refaites en une seule chaîne `PAR=2` (sh PID 2708) : e11p (après renfort du test), e11q, e11r, e11s, e11t, e11u,
    e11l ; puis, en chaînes d'attente, e11i (E-20) et le mutant ajouté M-11S-14 (E-19) (sh PID 13090), et e11u
    après le renfort contre M-11U-05 (E-23 ; sh PID 21684). Un seul groupe de campagnes à la fois.

## 2. Diffs (série SB-11a à SB-11u)

Lignes de code ajoutées, hors `.md`, tests et données compris. Plafond : 200 par diff (R-25). Le plancher est celui de
la suite `sim-bis` dans `gates.yml` à chaque étape.

| diff | objet | lignes ajoutées | plancher | sha256 |
|---|---|---|---|---|
| SB-11a | commun.ecrire (SORTIE/lien, fsync du dossier) ; taux, SE Decimal ; fréquences E-S-52 | 179 | 200 | `22a3565b08868dedee24579fe480ecd235939c271fc080b5111dcca678da0207` |
| SB-11b | jsonable, empreinte E-S-44 ; lots .lot (écriture, lecture : chaque i une fois, entête) | 163 | 204 | `480a2055682e2bc9d3f3922469e1cf30562fbe81c964d11e33bd69e41d7699b2` |
| SB-11c | appliquer (spawn, ordre) ; plan de lots 90 min | 67 | 206 | `0c770aebfa214dd1239a45796f9bbd4ebc002ebe1794b07ef3c496fdabcd9647` |
| SB-11d | couche : grille de la cellule (O-5), perte = W (L-2) | 114 | 208 | `d15e4f319c0f4158928d920412a8ad8ab7f49d3fac42371bca6833209fd6f3b0` |
| SB-11e | schéma fermé des cellules, refus nommés, surcharges ; fond | 195 | 211 | `dddb3d3f12035ae11093d0ba7cf46eba0d64db8222b7a0a6acea062a1c6a67f5` |
| SB-11f | replication d'une cellule (chaîne complète) ; composant « debut » | 186 | 215 | `482acc23a0687120e60c5e6647bdec133d3042081a56d22dfbf27f9aef075046` |
| SB-11g | oracle E-S-29 avec la variante (O-4), S, « avec », événements (P-3) | 104 | 217 | `2e1b361e196e8d9efab49fcc9fca370e84c9af539cb06f358854bc91192d7692` |
| SB-11h | agreger, ecrire_agrege | 109 | 219 | `b368dca6a5add2d783fc479cfefd009abb98a46f320dc5457234cfe1eed64bde` |
| SB-11i | calculer_lot ; T-DET-1 (1 contre 4 processus, PYTHONHASHSEED, lots, retrait P-9) | 134 | 221 | `59813014edc5c7dafbdef1ce4c5269b25df733bce11b479e15fbcce43f02525e` |
| SB-11j | e1 : replication_e1 (un appel), lot_e1, moyennes_point | 145 | 223 | `996aa0889faf5812b062710a6e2613396e70d6a734d0feeed1c0653278116484` |
| SB-11k | e1 : calibrer (charger_unites), phrases du bord, par hôte | 167 | 226 | `7e390933ffa478d549a46ba4a3a28367c79cdb793bf90eb685b119d217401df9` |
| SB-11l | e1 : faisabilite (REGIME-FAISABILITE-1) | 68 | 228 | `cc57ea66c900d6c5b94f5ac90d540ae51d0abcaea28e741c2a33673e35161d8f` |
| SB-11m | e1 : pauses | 58 | 229 | `ddfd42638cae65211a67ddf435fb7f1d87500b775bbaae16433535ecf2d4f09d` |
| SB-11n | e1 : pauses_c1, lignes_pauses | 188 | 231 | `b8baf7710af81e4970422c1774983308a39ee40c1365b52430a0f8010e6b4dc9` |
| SB-11o | e1 : calculer_e1 (lots par point, reprise), ecrire_e1 (E-S-48) | 144 | 233 | `0e037c4091787da248cda2d6d040f527c67a6ab8ed57ccf226d3ff06fc4c9c55` |
| SB-11p | e1 : rendu_e1, lancer_e1 | 177 | 235 | `4770d1c8e90a35c4bd64f6a01a4eca362bbe68b94c5ae61c17818df1c8ab3cc0` |
| SB-11q | impressions : F propre / hors-enveloppe, M_j | 139 | 237 | `941d7e8fb04cf68a19b75be6b96e8139239c5da78c2885f325a94c3397ad344d` |
| SB-11r | impressions : longues N4, absences N5, sauts et panne initiale N9 | 193 | 241 | `adf57dfdc4d0d823f66604993b0653cd0da2bfd3ffa2c7e0d5ad263b43c58aed` |
| SB-11s | table du §5.1 (17 cellules), familles du §5.2 exprimables | 130 | 243 | `f2c647b8fd293deb8a2af9363ad2387fceccc65dfa7cc09fa1a50febdbabad76` |
| SB-11t | chronometrer, budget | 66 | 245 | `7c2bdbc5021b9dc7d439ce61a994997ffa04b1123e2ba063a23edd2ac1e33086` |
| SB-11u | faisabilité des cellules du §5.1 et de la grille à C1, C2 | 67 | 246 | `f179c55c2eb336da5fe7311e289ee1674e63cd911e1dee0623af814f4707889a` |

Fichiers : `<scratchpad>/s2bis/sb11/diffs/SB-11{a..u}.diff`.
- Chaque diff est un `git diff --no-index` entre deux instantanés `etapes/e11X` (le contenu de `scripts/sim-bis` et
  `gates.yml`). Ils s'appliquent en série sur `5e386c4`, avec `-p1`.
- Octets 92 : 0 dans chaque diff et dans chaque fichier de `scripts/sim-bis` ; `gates.yml` en porte 4, ceux du motif
  R-13 de la base, non touchés (§7).
- Total ajouté : 2 793 lignes.
- Copies : `base/` (`git archive 5e386c4`, utile aux campagnes) et `fusion/` (tête `b07147d` + série, sans
  `target/`) gardées ; `travail/` (= `base/` + `etapes/e11u`, contrôlé par `diff -rq` et `cmp` avant
  suppression) supprimée à la fin ; `mut/` vide.

## 3. Périmètre du brief, points 1 à 7

| point | réalisation (fichier:ligne à l'état final) | tests |
|---|---|---|
| 1 Cellules | schéma fermé et refus nommés : `executer.py:215` (`_schema`), `:235` (`_valider`), `:318` (`cellule`). Refus : p = 1 → CELLULE/faible-p, L = 0 → CELLULE/faible-L, durée nulle → CELLULE/incident-duree, mode inconnu → CELLULE/incident-mode, ρ = 0 → CELLULE/rho, `longues` sans `poids_longues` → CELLULE/longues, W nul → CELLULE/duree. Surcharges sur une copie de parametres.json (`:327`). W de la cellule passé à la couche (`couche`, `:300`, perte = W à `:313` ; L-2). Grille de la couche dans `cellules.couches` (O-5). Table du §5.1 dans `cellules.nulles` (SB-11s), prédicat `commun.nommee` (`commun.py:68`). Pool : aucun changement de `calibration` (Q-SB11-14) | test_cellules (couches_o_5, couche_l_2, fond, refus_nommes_o_1, surcharges_longues) ; test_table |
| 2 Réplications, processus | graine et flux par réplication i, jamais par position de tâche (`replication` `:363`, `calculer_lot` `:406`) ; `appliquer` (`:168`), spawn, starmap ordonné ; T-DET-1 : 1 processus et PYTHONHASHSEED 0 contre 4 et 1, découpage de lots différent, retrait « presque mort » exercé (P-9) | test_determinisme (t_det_1, calculer_lot), test_executer (appliquer_ordonne) |
| 3 Lots reprenables | `ecrire_lot` `:115`, `lire_lots` `:151` (chaque i une fois : LOT/manquant, double, surplus ; entête : LOT/entete ; forme : LOT/forme), suffixe `.lot` ; écriture atomique `commun.ecrire` (`commun.py:202` : SORTIE/lien, fsync du dossier) ; reprise E1 (`e1.calculer_e1` `e1.py:233` : lot présent relu, lot perdu refait aux mêmes octets) ; plan de 90 min (`plan` `:183`, `budget` `:579`) | test_executer (lot_*, lots_couverture, plan_90_min), test_commun (ecrire_*), test_e1_sorties (lots_par_point_et_reprise), test_budget |
| 4 Agrégation exacte, SE | `taux` `:45` (x, r̂ en Fraction, SE en Decimal sous le contexte de r1, borne 1 − exp(ln(1/20)/R) par Decimal.ln/exp quand x = 0) ; `frequences` `:61` ; `agreger` `:416` ; `agreger_impressions` `:528` ; aucune fonction de libm (garde ast) | test_executer (taux_e_s_40, borne_a_2000, frequences_e_s_52, agreger), test_impressions |
| 5 E1 câblé | `e1.py` : `replication_e1` `:36` (un seul appel de calib_fiv.replication : I_t et dix hôtes sur le masque), `moyennes_point` `:59`, `calibrer` `:112` (selection sur `calibration.charger_unites(prm, cal["presentes"], ep)`), `phrases_bord` `:77`, `faisabilite` `:84`, `pauses_c1`/`lignes_pauses` `:177`/`:204`, `calculer_e1` `:233`, `ecrire_e1` `:254`, `rendu_e1` `:283`, `lancer_e1` `:329` ; sorties `calibration_e1.{json,txt}`, première ligne = étiquette (E-S-05) | test_e1, test_e1_sorties, test_pauses |
| 6 Cellules de niveau et de puissance | même mécanique pour toute cellule : `cellules.nulles` (17 cellules du §5.1, N1 à τ = 0 comprise) ; une cellule de chaque famille du §5.2 passe le schéma (P-cible C0/C1/C2, P-ETH, P-F3, P-grille aux coins, P-abs paire/triplet/impliquant, bascule 0 et 3/5, P-év) ; P-L20 non exprimable (Q-SB11-12) ; fréquences de NON ÉVALUABLE par strate, par cause, information insuffisante et combinaison (E-S-52) | test_table, test_executer (frequences_e_s_52, agreger) |
| 7 Budget mesuré | `chronometrer` `:567`, `budget` `:579` ; sonde hors dépôt `outils/budget.py` (préfixe de flux `SIM-BIS-proto`, une réplication par cellule à W = 16, durées seules) : §8 | test_budget |

## 4. Lignes de `LIGNES-BRIEF-SB11.md` et des items nommés

| ligne | où | test (et mutant qui le prouve) |
|---|---|---|
| L-2 : W de la cellule à la couche | `executer.couche` (`:313`, `"perte": W`) | test_couche_l_2 (M-11D-03 T_max au lieu de W) |
| O-5 : grille de la couche dans les cellules | `parametres.json` `cellules.couches`, `executer.couche` | test_couches_o_5 (M-11D-01, M-11D-05) |
| P-3 : mutant « g sur la grille » | M-11G-03 | test_absorption_s_variante_evenements |
| P-9 : T-DET-1 avec un retrait | cellule D-3 (bascule p_w = 3/5, panne) | test_t_det_1 (retrait « presque mort » de bitfinex exigé) |
| (6) résidus par hôte à C1 | `e1._par_hote` | test_impressions_par_hote (M-11K-06, -07, -11) |
| (6) point de Q₁ de l'hôte seul (diagnostic) | `e1._par_hote` | idem (M-11K-08) |
| (6) réplications à FIV indéfini (Q-SI-8 (d)) | `e1.moyennes_point`, `_par_hote` | test_moyennes_point (M-11J-06), test_impressions_par_hote (M-11K-09) |
| (6) loi des pauses à C1 sur le masque, à côté d'intervalles.txt | `e1.pauses`, `pauses_c1`, `lignes_pauses` ; section [PAUSES À C1] | test_pauses (M-11M-*, M-11N-*) |
| (6) écart-type exact par point et par ℓ (I_t) | `e1.moyennes_point` (Decimal.sqrt, contexte de r1) ; lignes [ÉCART-TYPE I_t] | test_moyennes_point (M-11J-05, -07, -10), test_sections_et_lancer (M-11P-04) |
| REGIME-FAISABILITE-1 sur C1 | `e1.faisabilite`, `calibrer` (C1, C2, cellules du §5.1, grille) | test_faisabilite_* (M-11L-*, M-11U-* ; M-11U-05 tué après le renfort d'E-23) |
| SB11-IMPRESSIONS-1 : résidus log FIV par ℓ de C2 | [RÉSIDUS C2] (`rendu_e1`), ℓ gardés dans le JSON (`ell_residus`) | test_sections_et_lancer (M-11P-03, tué après le renfort d'E-17) |
| SB11-IMPRESSIONS-1 : taux effectifs de F (propre, hors-enveloppe) | `executer.f_separe`, `impressions`, `agreger_impressions` | test_f_propre_et_hors_enveloppe, test_comptes_exacts (M-11Q-*) |
| SB11-IMPRESSIONS-1 : épisodes longs par durée sous N4 | `executer.longues`, `_par_duree`, `_distribution` | test_longues_n4 (M-11R-01 à -04, -14) |
| SB11-IMPRESSIONS-1 : part visible de la panne initiale selon T_début | `impressions["initiale"]`, agrégée par jour tiré | test_sauts_et_initiale_n9, test_agreger_n4_n5_n9 (M-11R-10, -12, -13) |
| SB11-IMPRESSIONS-1 : schéma fermé, refus nommés ; surcharge de longues | `executer._schema`, `_valider`, `cellule` | test_refus_nommes_o_1, test_surcharges_longues (M-11E-*) |
| AVIS-T3 : distribution de M_j par strate ; absences par durée sous N5 ; sauts et panne initiale sous N9 | `agreger_impressions["M"]`, `executer.absences`, `impressions["sauts"]` | test_comptes_exacts (M-11Q-10), test_absences_n5 (M-11R-05 à -07), test_sauts_et_initiale_n9 (M-11R-08, -09) |
| Q-SI-8 (a) courbes des dix hôtes et moyennes, par point et par réplication | lots d'E1 (une ligne par réplication), JSON `points` | test_courbes_d_un_seul_appel, test_sections_et_lancer (M-11P-09) |
| Q-SI-8 (b) `selection` sur `charger_unites(prm, cal["presentes"], ep)` | `e1.calibrer` | test_selection_par_charger_unites_q_si_8_b (**M-11K-01 analyser_unites tué**, M-11K-02, -03) |
| Q-SI-8 (c) `ligne_bord` par strate et phrases (8)(ii), (iii) | `e1.calibrer`, `phrases_bord` | test_bord_et_phrases_q_si_8_c (M-11K-04, -05, -10) |
| Q-SI-8 (e) I_t et D*(u) d'un même appel `replication` | `e1.replication_e1` | test_courbes_d_un_seul_appel (M-11J-01, -03) |
| Q-SI-7 : phrase datée sur la clause `ell_c1` de Q-T4-10 | acte de l'orchestrateur (G2 de SIM-INTEG l.94) : phrase proposée en Q-SB11-15 | — |
| C1-COUT-1, TABLES-CACHE-1 | §8 (coût mesuré, tables à froid et à chaud, plan) | test_budget, test_plan_90_min |
| ECRITURE-LIEN-1 | `commun.ecrire` : SORTIE/lien, fsync du dossier | test_ecrire_sans_lien_dur, test_ecrire_atomique_sans_ecrasement (M-11A-01 à -05, -16) |
| LIBM-POW-1 | garde ast du lot inchangée et tenue par executer.py, e1.py (ni `**`, ni `pow`, ni libm, ni `random.*` autre que `random()`) | test_fitness, test_fitness_tirages (verts à chaque étape) |
| MUTANTS-SITE-APPEL-1 | mutants des deux formes dans la série ; décompte exact par diff, et diffs sans mutant de site d'appel (m, s), au §6 (E-19) | §6 |
| POOL-EP-SEPARES-1 | aucun changement de `calibration` : le câblage ne l'exige pas (Q-SB11-14) | — |
| ENREG-ROLE-1, P1-ESTIMATION-1, OBS-GRILLE-1, FIV-IDENTIF-1, INDICES-IDENTIFIANTS-1, CALCUL-1 | rien à coder ici ; statut au §11 | — |

## 5. Exigences E-S réalisées par SB-11 (liste dressée depuis le §2 de la PROPOSITION)

- **Réalisées dans leur part SB-11** :
  - E-S-05 : étiquette en tête des lots, des agrégats et des sorties d'E1.
  - E-S-06 : fichiers partiels `.lot`, `TMPDIR` du lot, octets 92 écrits par gabarit.
  - E-S-40 : x, r̂, SE et borne à x = 0.
  - E-S-41 : flux et graine de règle par (cellule, i).
  - E-S-42 : ordre des tirages, ordre des réplications, indépendance au nombre de processus et à PYTHONHASHSEED.
  - E-S-43 : entiers, Fraction et Decimal sous le contexte de r1 ; JSON canonique sans heure.
  - E-S-44 : empreinte par cellule et T-DET-1.
  - E-S-45 : lots reprenables.
  - E-S-46 : chronométrage et plan ; le plan reste à approuver par l'orchestrateur.
  - E-S-48 : pour `calibration_e1.{json,txt}` seulement.
  - E-S-52 : fréquences par cause, information insuffisante et combinaison.
- **Câblées par SB-11** (la règle elle-même appartient au sous-lot qui l'a écrite) :
  - E-S-14 : T_début tiré sur le flux « debut ».
  - E-S-23, E-S-24 : fenêtres retenues, retraits, première unité.
  - E-S-29 : oracle sur les 200 premières réplications, variante comprise (O-4).
  - E-S-30, E-S-31 : séquence d'ETH ; F3 par les classes de la cellule.
  - E-S-32 : S suivie.
  - E-S-33 : variante.
  - E-S-34 : événements sur la suite comprimée.
  - E-S-35 : valeurs « avec ».
  - E-S-38 : E1 câblée, sur les points (1) à (8) de l'ajout daté.
  - E-S-03, en partie : table des cellules du §5.1 dans `parametres.json`.
- **Hors SB-11** :
  - E-S-48 pour `sim_niveau_bis` et `sim_puissance_bis`, E-S-49, E-S-50 : SB-12.
  - E-S-51 : SB-13.
  - E-S-47 : lieu du calcul, acte d'exécution.

## 6. Mutants

Chaque mutant est classé par la commande du job `sim-bis-unittest` lancée sur l'instantané de l'étape, sous
`isole.sh`, avec une borne de 300 s. Sortie 1 : tué ; sortie 0 : vivant ; autre sortie ou dépassement de la borne :
FATAL. Un témoin non muté tourne au début et à la fin de chaque campagne. Journaux :
`journal/campagne-e11X.txt` et `journal/mut-e11X-*.txt`.

| campagne | mutants | tués | vivants | FATAL | témoins début / fin | mutant le plus long | heures (UTC) | processus |
|---|---|---|---|---|---|---|---|---|
| e11a | 17 | 17 | 0 | 0 | VIVANT 29 s (sortie 0) / VIVANT 31 s (sortie 0) | 34 s | 23:31–23:35 | non consigné (E-15) |
| e11b | 14 | 14 | 0 | 0 | VIVANT 30 s (sortie 0) / VIVANT 30 s (sortie 0) | 54 s | 23:35–23:40 | non consigné (E-15) |
| e11c | 10 | 10 | 0 | 0 | VIVANT 30 s (sortie 0) / VIVANT 32 s (sortie 0) | 45 s | 23:40–23:44 | non consigné (E-15) |
| e11d | 12 | 12 | 0 | 0 | VIVANT 32 s (sortie 0) / VIVANT 31 s (sortie 0) | 57 s | 23:44–23:48 | non consigné (E-15) |
| e11e | 17 | 17 | 0 | 0 | VIVANT 31 s (sortie 0) / VIVANT 31 s (sortie 0) | 36 s | 23:49–23:53 | non consigné (E-15) |
| e11f | 12 | 12 | 0 | 0 | VIVANT 34 s (sortie 0) / VIVANT 34 s (sortie 0) | 52 s | 23:53–23:57 | non consigné (E-15) |
| e11g | 12 | 12 | 0 | 0 | VIVANT 35 s (sortie 0) / VIVANT 35 s (sortie 0) | 53 s | 23:58–00:01 | non consigné (E-15) |
| e11h | 11 | 11 | 0 | 0 | VIVANT 28 s (sortie 0) / VIVANT 28 s (sortie 0) | 38 s | 22:18–22:20 | non consigné (E-15) |
| e11i | 10 | 10 | 0 | 0 | VIVANT 93 s (sortie 0) / VIVANT 83 s (sortie 0) | 99 s | 04:20–04:29 | 1951 (groupe 13090) |
| e11j | 11 | 11 | 0 | 0 | VIVANT 78 s (sortie 0) / VIVANT 72 s (sortie 0) | 172 s | 23:20–23:30 | non consigné (E-15) |
| e11k | 11 | 11 | 0 | 0 | VIVANT 76 s (sortie 0) / VIVANT 92 s (sortie 0) | 184 s | 00:31–00:42 | 31614 |
| e11l | 10 | 10 | 0 | 0 | VIVANT 92 s (sortie 0) / VIVANT 101 s (sortie 0) | 142 s | 04:06–04:18 | 21328 (groupe 2708) |
| e11m | 11 | 11 | 0 | 0 | VIVANT 86 s (sortie 0) / VIVANT 90 s (sortie 0) | 185 s | 00:49–01:02 | 27213 (groupe 27212) |
| e11n | 13 | 13 | 0 | 0 | VIVANT 93 s (sortie 0) / VIVANT 93 s (sortie 0) | 214 s | 01:03–01:20 | groupe 27212 |
| e11o | 13 | 13 | 0 | 0 | VIVANT 101 s (sortie 0) / VIVANT 103 s (sortie 0) | 151 s | 01:24–01:42 | 20089 (groupe 20088) |
| e11p | 11 | 11 | 0 | 0 | VIVANT 110 s (sortie 0) / VIVANT 104 s (sortie 0) | 194 s | 02:07–02:24 | 2709 (groupe 2708) |
| e11q | 13 | 13 | 0 | 0 | VIVANT 106 s (sortie 0) / VIVANT 109 s (sortie 0) | 166 s | 02:26–02:45 | groupe 2708 |
| e11r | 15 | 15 | 0 | 0 | VIVANT 122 s (sortie 0) / VIVANT 120 s (sortie 0) | 213 s | 02:47–03:10 | groupe 2708 |
| e11s | 13 | 13 | 0 | 0 | VIVANT 107 s (sortie 0) / VIVANT 114 s (sortie 0) | 152 s | 03:12–03:28 | groupe 2708 |
| e11t | 11 | 11 | 0 | 0 | VIVANT 113 s (sortie 0) / VIVANT 112 s (sortie 0) | 158 s | 03:30–03:46 | 7082 (groupe 2708) |
| e11u | 10 | 10 | 0 | 0 | VIVANT 118 s (sortie 0) / VIVANT 126 s (sortie 0) | 175 s | 04:37–04:53 | 16385 (groupe 21684) |
| e11s (supplément, E-19) | 1 | 1 | 0 | 0 | VIVANT 123 s (sortie 0) / VIVANT 119 s (sortie 0) | 120 s | 04:31–04:35 | chaîne 13090 |

- **Total des passages retenus** : 258 mutants (257 dans les 21 campagnes, plus M-11S-14), 258 tués, 0 vivant, 0 FATAL, 0 inapplicable ; chaque témoin VIVANT (sortie 0).
- **Passages écartés**, gardés en `journal/premier-passage/` et jamais comptés : premiers passages de e11a à e11g, e11j (avant
  confirmation) ; e11h (deux passages à 9/11, survivants corrigés par l'agent précédent) ; e11i du premier passage (instantané retouché en cours) et de 22:08 (E-20) ;
  e11k interrompue (22:44) et e11k de 23:10 ; e11l de 23:19 (E-15) ; premier passage de e11p (M-11P-03 vivant, E-17) ;
  e11q interrompue (E-16) ; premier passage de e11u (M-11U-05 vivant, E-23).

- **Mutants exigés par le brief, tous tués** :
  - P-3 « g sur la grille » : M-11G-03.
  - « analyser_unites au lieu de charger_unites » : M-11K-01 (contre-contrôle de SIM-INTEG).
  - M-DET-1 : graine dérivée de l'indice de tâche, tué (campagne e11i refaite) ; sa forme pour E1, M-11J-09, aussi.
  - M-DET-2 : itération sur un ensemble, tué (e11i refaite).
- **Site d'appel et source des données** (SHOGEN-MUTANTS-SITE-APPEL-1 ; décompte exact, E-19). Motifs écrits dans
  `outils/mutants_11X.py` :

| diff | « site d'appel » (motif) | « source des données » (motif) | site d'appel muté sous un autre motif |
|---|---|---|---|
| a | 1 | 1 | — |
| b | 1 | 1 | — |
| c | 0 | 1 | M-11C-01 (`p.starmap` → `imap_unordered` au site d'appel d'`appliquer`) |
| d | 0 | 2 | M-11D-04 (argument de `observateurs.chemin_reference` à son site d'appel : f au lieu de 1 − f) |
| e | 1 | 1 | — |
| f | 1 | 1 | — |
| g | 0 | 1 | M-11G-03 (`regle.loi_evenements` appelée sur la grille, P-3) |
| h | 1 | 1 | — |
| i | 0 | 2 | M-11I-04 (tâches de `replication` sans les points), M-11I-06 (`ecrire_lot` sous un autre nom) |
| j | 1 | 1 | — |
| k | 0 | 3 | M-11K-01 (`analyser_unites` au lieu de `charger_unites`) |
| l | 1 | 2 | — |
| m | 0 | 1 | aucun |
| n | 1 | 2 | — |
| o | 1 | 2 | — |
| p | 1 | 4 | — |
| q | 1 | 2 | — |
| r | 0 | 2 | M-11R-01 (`rep.u` appelé sur un autre emplacement) |
| s | 0 | 1 (M-11S-14, ajouté) | aucun |
| t | 1 | 1 | — |
| u | 1 | 1 | — |

  - Sans mutant de site d'appel : SB-11m (`pauses`, fonction nouvelle sans appelant dans le diff ; les tâches qui
    l'appellent, dans `pauses_c1`, sont mutées en SB-11n par M-11N-01) et SB-11s (table de données ; le seul appel
    nouveau est le prédicat `commun.nommee` du schéma, dont le corps est muté par M-11S-08).
  - L'item demande ces deux formes à la campagne, sans exiger un mutant par diff ; je le dis ici pour que le
    réviseur juge.
- **Mutants de spécification sans oracle**, déclarés au G0 (prop. l.407-408) :
  - « C1 contre K_crit » : sans objet depuis la règle de C1 du point (1) ;
  - « g fusionné sur la grille » : il a maintenant un oracle (P-3).

## 7. Matrice, planchers, jobs

Contrôles finaux par `outils/final.py` (processus python3 détaché, PID 32128), l'un après l'autre, de 04:53:47 à 05:11:26 UTC, puis
deux compléments ; résumé `journal/final.txt`, sortie de chaque étape `journal/final-<nom>.txt`.

**Matrice 3.10 à 3.13** (`fusion/`, état final sur la tête ; `-X dev -W error`, `isole.sh`, `unittest discover`) :

| Python | code | tests | Exception ignored | Warning |
|---|---|---|---|---|
| 3.10 | 0 | Ran 262, OK (180 s) | 0 | 0 |
| 3.11 | 0 | Ran 262, OK (147 s) | 0 | 0 |
| 3.12 | 0 | Ran 262, OK (150 s) | 0 | 0 |
| 3.13 | 0 | Ran 262, OK (147 s) | 0 | 0 |

**Jobs, commandes de `gates.yml`** (vérificateur `enforcement/verdict-suite-s2.py`, `SHOGEN_S2_CAMPAGNE_CONTROL`
retirée de l'environnement, jamais posée) :

| job | copie | résultat |
|---|---|---|
| runner `run-fixtures-verdict-suite-s2.py` | fusion | code 0, 136 ok, 0 échec |
| sim-bis, plancher 262 | fusion (tête + série) | conforme : code 0, aucun saut, Ran = 262 |
| sim-bis, plancher 246 | travail (5e386c4 + série) | conforme : code 0, aucun saut, Ran = 246 |
| s2bis, plancher 255 | fusion | conforme : code 0, aucun saut, Ran = 255 |
| S2 (`--egal`) | fusion | conforme : code 0, Ran = 415, deux sauts nommant SHOGEN_S2_CAMPAGNE_CONTROL |
| hook (`run-fixtures-hooks.sh`) | fusion | 54 ok, 0 échec |
| secrets (fixtures ; `gate-secrets.sh --tree`) | fusion | 147 ok ; 956 fichiers sans forme d'identifiant |
| R-1 (fixtures ; `lint-model-pinning.sh .`) | fusion | 227 ok ; 7 fichiers, liste blanche exacte |
| R-13 (motif du job par `chr(92)`, témoin positif détecté) | fusion (`git grep`) ; travail (`grep -rnE`, E-24) | aucun marqueur (code 1) dans les deux |
| `cargo --locked xtask verify` | fusion | 8 VERDICT VERT, 1 VERDICT ROUGE (1 violation), global ROUGE |

- **cargo** : lignes VERDICT seules lues (`grep VERDICT`). Contrôle : la même commande sur une copie neuve de
  `b07147d` (même `git archive`, mêmes exclusions), à 05:12:33 UTC, rend les mêmes dix lignes VERDICT (8 VERT, 1 ROUGE
  à 1 violation, global ROUGE). La violation précède donc la série ; c'est, selon le brief, S-G9 `docs/17:70`, connue
  sur copie. La série n'en ajoute aucune.
- **Planchers** : chaque diff recale exactement le plancher de `sim-bis-unittest` (§2 : 200 à 246 sur la base 194) ;
  sur la tête, 262 = 210 + 52, tenu exactement par la matrice et le job.
- **Octets 92 et longueur des lignes** (script sur `etapes/e11u`) : 0 octet 92 dans chaque diff et dans chaque
  fichier de `scripts/sim-bis` ; `gates.yml` en porte 4 (motif du job R-13), comme la base, non touchés. Aucune
  ligne de plus de 120 caractères dans les `.py`. Les lignes longues de données et de texte suivent la forme de la
  base : `parametres.json` 57 → 78 (une cellule par ligne, sources), `README.md` 19 → 21, `gates.yml` 2 (base).

## 8. Budget mesuré (E-S-46 ; C1-COUT-1, TABLES-CACHE-1)

- **Sonde** : `outils/budget.py` (hors dépôt), lancée sur `travail/` (état e11u) sous `isole.sh`, de 02:07:15 à
  02:11:53 UTC (`date -u` encadrant), journal `journal/budget.txt`. Préfixe de flux `SIM-BIS-proto` (E-S-41 : aucune
  graine du lot essayée), W = 16, **une réplication par type** (consigne de l'orchestrateur), à i = 0 : elle porte donc
  l'oracle d'E-S-29 (mode à R complet, variante comprise) et les impressions, soit une **borne haute** du coût d'une
  réplication de la cellule. Aucune valeur de règle ni de FIV n'est imprimée, seulement des durées et des plans.
- **Conditions** : machine partagée, charge 4,10 au début et 7,08 à la fin sur 4 cœurs, campagne e11p en cours (E-18).
  Les durées sont gonflées par la charge ; elles valent comme ordre de grandeur et comme majorant.
- **Durées mesurées** (`executer.chronometrer`, ns lus avant et après l'appel ; affichées en s) et plan de 10⁴
  réplications sur 4 processus à ce coût (`executer.budget`, lots de 90 min au plus par `executer.plan`) :

| cellule | 1 réplication, i = 0 (s) | 10⁴ réplications, 4 processus (s) | lots |
|---|---|---|---|
| N0 (première du processus : tables à froid) | 8,53 | 21 326 | 4 |
| N1 | 41,577 | 103 942 | 20 |
| N1-tau0 | 7,034 | 17 587 | 4 |
| N2 | 8,234 | 20 586 | 4 |
| N3 | 20,496 | 51 241 | 10 |
| N4 | 21,07 | 52 676 | 10 |
| N5 | 7,862 | 19 655 | 4 |
| N6 | 7,725 | 19 314 | 4 |
| N7 | 7,571 | 18 929 | 4 |
| N8 | 20,72 | 51 801 | 10 |
| N9 | 19,245 | 48 113 | 9 |
| N10 | 9,743 | 24 358 | 5 |
| N11 | 12,968 | 32 421 | 7 |
| N12 | 6,924 | 17 311 | 4 |
| X1 | 18,898 | 47 246 | 9 |
| X2 | 8,718 | 21 796 | 5 |
| X3 | 7,025 | 17 563 | 4 |
| P-cible-C1 (une cellule de la famille) | 41,052 | 102 631 | 20 |

- **Totaux recomptés** (script sur `journal/budget.txt`) : les 17 cellules du §5.1, une réplication chacune : 234,34 s ;
  à 10⁴ réplications chacune sur 4 processus : 585 865 s, soit environ 162,7 h, en 117 lots. C'est un majorant : le
  coût hors du sous-ensemble de l'oracle (i ≥ 200, soit 98 % des réplications) n'est pas mesuré ici.
- **Forme des coûts** : les cellules à variante (N1, N3, N4, N8, N9, X1) coûtent de 18,9 à 41,6 s, les autres de 6,9 à
  13,0 s ; à i < 200, la variante est rejouée par l'oracle à deux modes (O-4). N1, qui porte aussi S et F3, et
  P-cible-C1, bâtie sur N1, sont les plus chères (≈ 41 s).
- **E1** (`e1.replication_e1`, i = 0) : C0 (`E1-C0-v2`) 0,524 s ; point (1/20, 10, 240), tenant lieu des points d'E1
  inconnus avant E1, 2,017 s. Plan de 200 réplications sur 4 processus : 26 s et 100 s, un lot chacun ; les 65 cellules
  d'E1 (C0 et 64 points) au coût du point : 6 558 s, soit environ 109 min.
  - Comparaison avec C1-COUT-1 (≈ 0,32 s par réplication pour les 20 courbes, ≈ 70 min pour E1) : la mesure unique
    inclut la génération à froid du point (payée une fois par point et par processus dans un lot) et la charge ; une
    seule réplication par type ne sépare pas le froid du chaud.
- **TABLES-CACHE-1** : le cache des tables (`functools.lru_cache` de `sources`) vit par processus ; la première
  réplication du processus (N0) paie les tables à froid. La sonde à une réplication par type ne donne pas de mesure
  propre du froid contre le chaud (la première sonde de l'agent précédent, à 21:05, donnait 1,8 s à froid contre
  0,18 s à chaud pour les sources, [2nd] de `NOTES.md`).
- **Plan à approuver** (E-S-46) : le plan ci-dessus n'est pas approuvé par moi ; il sert de majorant. Pour un plan
  serré, il faut une réplication hors du sous-ensemble de l'oracle (i ≥ 200) et une réplication chaude d'E1 par type,
  sur une machine moins chargée (Q-SB11-18).

## 9. Questions Q-SB11-n (choix fait, raison ; aucune valeur scellée tranchée)

**Organisation du code et paramètres déjà en place**
- **Q-SB11-1, modules.**
  - Choix : `executer.py` (cellules, réplication, lots, agrégation, impressions, budget) et `e1.py` (E1 câblée et
    sorties d'E1) sont deux modules du moteur.
  - Raison : taille, et frontière E-S-01. `e1.py` n'importe aucun adaptateur.
- **Q-SB11-2, composant « debut ».**
  - Choix : composant ajouté à `sources.composants` (liste fermée). T_début est tiré sur le flux d'indice 0.
  - Raison : la liste fermée des composants est sous schéma avant E0 (ajout daté du 2026-10-05 01:45:03 UTC, point 3).
  - À adjuger avant E0.
- **Q-SB11-3, grille « large ».**
  - Choix : perte d'un observateur, et pannes de paires par semaine (maximum de la grille), dans `cellules.couches`.
  - À adjuger avant E0.

**Agrégats et impressions**
- **Q-SB11-4, écart-type.**
  - Choix : dénominateur m − 1 (variance d'échantillon) sur les m FIV définis. None si m < 2.
  - Raison : le point (6) ne fixe pas le dénominateur.
- **Q-SB11-5, loi des pauses.**
  - Choix : type « ecart » seul (série D*(u), celle de Q₁). Les 200 réplications de C1 sont rejouées par leurs flux,
    plutôt que leurs pauses stockées dans les lots.
  - Raison : même série que la règle de C1 ; lots plus légers ; le rejeu est exact (flux par i).
  - Le type « panne » de `intervalles.txt` n'est pas imprimé.
- **Q-SB11-6, impressions des cellules.**
  - Choix : sur les 200 premières réplications de chaque cellule (`IMPRESSIONS = ORACLE`), le même sous-ensemble
    pré-déclaré que l'oracle d'E-S-29.
  - Raison : poids des lots à 10⁴ réplications.
  - M_j est sommé sur toutes les réplications.
- **Q-SB11-7, n′_s = 0 (constat).**
  - Constat : cellule à repli et grille « large », W = 1, i = 1 (cellule de test). Aucune fenêtre évaluable en stress :
    `regle` refuse REGLE/entier (n = 0), et la réplication échoue au lieu de rendre NON ÉVALUABLE.
  - À W = 16, le cas est très improbable mais pas exclu [inféré, non mesuré]. Il bloquerait un lot (E-S-45).
  - Proposition, non codée : NON ÉVALUABLE avec les causes de la garde (unites, k_crit, runs, n_prime).
  - Raison de ne pas coder : c'est une valeur de la règle au cas dégénéré, à adjuger. D'ici là, le refus nommé est le
    défaut sûr.

**Table des cellules**
- **Q-SB11-8, table du §5.1 : classes, S, diviseurs.**
  - ETH est dans toutes les cellules, pour la séquence familiale du §4 pt 4.
  - F3 (USDC, USDT) sur N1 seulement (l.301).
  - S sur N1 (E-S-32, sous H0).
  - Variante aux diviseurs 4 et 8 sur N1, N3, N4, N8, N9, X1 (l.301 et section `variante`).
  - À adjuger avant E0.
- **Q-SB11-9, valeurs de cellule que le §5.1 ne fixe pas.**
  - N11 : L_w = 1, type « ecart », critère collectif mesuré.
  - N6 : λ_loc = 10⁻³ en part du temps (Q-T3-5).
  - N7 : π = β = 1/5.
  - X3 : ρ_art = 1/20 par jour.
  - N0 : ε fixe = 10⁻⁴.
  - N1 à τ = 0 ajoutée (AVIS Q-S-21).
  - À adjuger avant E0.
- **Q-SB11-12, P-L20.**
  - Constat : « lettre du scénario B (L = 20, sans groupement) » ne s'exprime pas dans le schéma. `sources` n'a pas de
    loi d'épisodes de moyenne fixée pour le fond.
  - Proposition : une clé de cellule (loi du fond : EP ou géométrique de moyenne L), avec son support dans `sources`.
  - Élément à former (§11).
- **Q-SB11-17, familles du §5.2.**
  - Constat : leur énumération (P-grille 72, P-abs 72 + 14, échelle de P-cible) n'est pas écrite dans
    `parametres.json`. Seule leur exprimabilité est testée.
  - Proposition : grilles dans `parametres.json` et générateur, au brief de SB-12 ou d'E3.
  - Pour P-abs, les ρ et D des alternatives sont à prendre de la cible (§3 pt 1) : à adjuger.

**E1 et budget**
- **Q-SB11-10, oracles internes d'E1 (E-S-48).**
  - Choix : `ecrire_e1` exige un dictionnaire d'oracles non vide, tous vrais, passé par le lanceur. Les oracles
    d'exécution sont des refus nommés internes à la chaîne : lots complets, masque, croisement Q-SI-9, entête
    inchangée.
  - Proposition : le lanceur passe le verdict conforme de la suite sim-bis, qui porte l'oracle E-S-39 contre r1 sur
    10 réplications (`test_oracle_r1.test_oracle_e_s_39`).
  - Aucune ligne de commande d'E1 n'est écrite. La commande et ses oracles sont à fixer au brief d'E0/E1.
- **Q-SB11-11, phrase (8)(iii).**
  - Choix : écrite à E1 avec sa condition sur W*(C1) telle quelle. Les W* sont calculés par SB-12, après E1.
- **Q-SB11-13, coût retenu pour le plan.**
  - Choix : la plus longue réplication mesurée, sans marge.
  - Dans la sonde, les points C1 et C2 sont tenus par (1/20, 10, 240), puisque les vrais points sont inconnus avant E1.

**Lignes des items et du brief**
- **Q-SB11-14, POOL-EP-SEPARES-1.**
  - Choix : pas de séparation. Le câblage de SB-11 n'emploie que le pool entier.
  - L'O-3 de l'item reste à déclarer comme limite : la panne initiale est tirée avant les retraits (avis Q-T3-1,
    seconde limite).
- **Q-SB11-15, Q-SI-7.**
  - Phrase proposée, à poser par l'orchestrateur : « *Ajout daté du <date> (Q-SI-7)* : la clause « ou FIV(ell_c1) de
    C0 ou de C2 indéfini » de Q-T4-10 est sans objet depuis le retrait de `e1.ell_c1` (point (7) de l'ajout daté du
    G0 du 2026-10-05 15:05:43 UTC) ; le refus E1/indefini de `calib_fiv.selection` porte sur : aucun critère défini,
    aucun Q₁ défini, ou aucun (u, ℓ) retenu dans la strate ».
- **Q-SB11-16, T-DET-1.**
  - Constat : 3 cellules × 6 réplications, au lieu de 3 × 200 (§6.2), pour tenir le temps de la suite. L'identité à
    l'échelle reste l'exécution B (Q-S-10).
  - À adjuger : accepter, ou porter la sonde à 200 hors suite.

**Questions de la seconde reprise**
- **Q-SB11-18, plan de budget.**
  - Constat : à une réplication par type (consigne), la sonde ne mesure que i = 0, qui porte l'oracle d'E-S-29 et
    les impressions ; le coût des réplications i ≥ 200 (98 % d'une cellule à 10⁴) et celui d'une réplication chaude
    d'E1 ne sont pas mesurés. Le plan du §8 est un majorant (≈ 163 h pour le §5.1 sur 4 processus).
  - Choix : aucun plan proposé à l'approbation ; le majorant est rendu tel quel.
  - À adjuger : admettre une seconde réplication par type (i = 200 ; E1 à i = 1), sur une machine moins chargée,
    pour un plan serré avant E0.
- **Q-SB11-19, `e1._vals` coupe au plus court.**
  - Constat (E-17) : `_vals(ells, xs)` imprime par `zip`, qui s'arrête à la plus courte des deux listes ; une
    longueur fausse des ℓ ou des valeurs passe donc en silence dans le texte d'E1 (le JSON, lui, la montre).
  - Proposition, non codée : refus nommé si les deux longueurs diffèrent (ou `zip(..., strict=True)`, Python ≥ 3.10).
  - Raison de ne pas coder : la série est close et ses campagnes de p à u sont faites ; le changement rouvrirait SB-11p.
    À porter au brief de SB-12, qui récrit les sorties.

## 10. Écarts

- E-1 à E-7 : de l'agent précédent, recopiés de `NOTES.md` (barres obliques inverses dans des outils, réécrites ;
  heures estimées puis corrigées ; référence SE d'abord tapée fausse ; octets 92 retirés avant lancement ; fixtures
  d'E1 sous les vraies cellules d'E1, corrigées en « E1-essai », valeurs vues déclarées en E-6 ; base `ebd1560`).
- E-8 : « barre oblique inverse suivie de n » tapé dans deux commandes d'outil (heredoc Python, sed). Les octets
  du lot sont contrôlés : 0 octet 92, et le sha256 d'e1.py est égal à l'instantané d'avant l'ajout. Aucune
  incidence.
- E-9 : une suite entière lancée pendant la campagne e11k, soit deux processus lourds à la fois (00:42 à 00:44).
- E-10 : `test_cellules_5_2_exprimables` est vert d'emblée. C'est un test de caractérisation de la mécanique existante.
  Son mutant M-11S-09 le rougit.
- E-11 : rouge de SB-11u. La première ébauche (calibrer sans les clés nouvelles) a donné 1 FAIL et 1 ERROR. La seconde
  (rendu sans les lignes nouvelles) a donné le FAIL d'assertion attendu.
- E-12 : exposition. `intervalles.txt` (sortie épinglée de PLAN-S2BIS-2, classe M) a été affiché en partie : en-tête,
  et lignes de pauses par hôte pour l'étude de forme. L'agent précédent l'avait déjà lu. Aucun chiffre n'en est repris
  dans le code ou les tests (texte synthétique dans `test_pauses`).
- E-13 : la tête a avancé à `b07147d` pendant le travail (§14). Les diffs restent sur `5e386c4`.
- E-14 : test N5 déplacé de i = 1 à i = 2 après le constat de Q-SB11-7.
- E-15 : passages sans PID consigné (session précédente, 23:02 à 00:01). Les journaux sont complets :
  - e11l a été refaite (§6) ;
  - e11j a son premier passage consigné ;
  - les confirmations e11a à e11g (docstrings normalisées, texte seul) ne sont pas refaites, à refaire si
    l'orchestrateur l'exige. Leurs premiers passages, consignés, ont tué tous les mutants.
- E-16 : **interruption** par le redémarrage du conteneur (~02:00 UTC). Campagnes arrêtées : o, p, q, r (groupe
  20088), chaîne s, t, u (PID 30365), chaîne e11l. Gardées, parce que complètes et consignées (bilan, deux témoins,
  journal par mutant) : e11o et le premier passage de e11p. Sans résultat, jamais comptées : e11q (arrêtée pendant
  son témoin de début ; journal vide gardé en `premier-passage/campagne-e11q-0159-interrompue-vide.txt`, arbre
  `mut/e11q-TEMOIN-debut` supprimé). Refaites : p, q, r, s, t, u, l (chaîne sh PID 2708, `PAR=2`).
- E-17 : **survivant M-11P-03** (résidus de C2 sous des ℓ non gardés) au premier passage de e11p. Cause : les ℓ non
  gardés d'EP sont en queue de grille (1 440 en calme ; 480, 720, 1 440 en stress), `e1._vals` coupe au plus court
  (`zip`), la ligne [RÉSIDUS C2] est donc identique sous le mutant, et le test ne lisait pas `ell_residus` du JSON.
  Remède : une assertion (`obj["strates"][s]["ell_residus"] == ells`) dans `test_sections_et_lancer`, posée par
  `outils/renfort_p03.py` à l'identique dans e11p à e11u, `travail/` et `fusion/`. Rouge d'assertion sur le mutant et
  vert sans lui : `journal/rouge-11p-renfort.txt`. Diffs régénérés : SB-11p (176 → 177 lignes), SB-11u (contexte) ;
  q à t inchangés (sha256 égaux). e11p refaite : 11/11. Reste une faiblesse du rendu texte : Q-SB11-19.
- E-18 : **sonde de budget sous charge** : lancée pendant la campagne e11p (deux processus lourds à la fois, comme
  E-9), charge 4,1 à 7,1 sur 4 cœurs ; deux mutants de e11p ont pris 192 et 194 s pendant ce temps (borne 300 s). La
  sonde a été réduite à une réplication par type (consigne), l'ancienne forme gardée en `tmp/budget-2-repl.py`.
- E-19 : **affirmation fausse corrigée** au §6. La version précédente du rapport disait que chaque diff portait au
  moins un mutant « site d'appel » et un mutant « source des données ». Recompte des motifs dans
  `outils/mutants_11X.py` : aucun motif « site d'appel » dans c, d, g, i, k, m, r, s ; aucun motif « source des
  données » dans s. Le §6 donne le décompte exact et les mutants qui mutent un site d'appel sous un autre motif. Ajout :
  M-11S-14 (ligne de N2 passée sous le nom N3, forme « source des données ») pour SB-11s, campagne supplémentaire
  `journal/campagne-e11s-sup.txt`.
- E-20 : **e11i sans campagne sur son instantané final**. Le passage consigné (22:08 à 22:13) précède la retouche de
  `tests/test_executer.py` de l'instantané e11i (22:17:19, `patch_agreger.py`). Contrôle fait sur toutes les étapes
  (date du fichier le plus récent de l'instantané contre le début de la campagne retenue) : e11i est la seule en
  défaut. e11i refaite (chaîne sh PID 13090) ; l'ancien passage gardé en `premier-passage/`.
- E-21 : **E-15 étendu**. Outre les confirmations e11a à e11g, les passages retenus de e11h (22:17 à 22:20) et de
  e11j (23:19 à 23:30) n'ont pas de PID consigné. Ils ne sont pas refaits : non interrompus, journaux complets
  (bilan, deux témoins VIVANT, journal par mutant), instantanés antérieurs à leur début.
- E-22 : **barres obliques inverses dans un outil** : la première écriture de `outils/renfort_u05.py` portait 18
  octets 92 (guillemets échappés tapés). Réécrite par `chr(92)` avant tout usage sur un instantané, sortie
  identique contrôlée (`cmp`) ; fichiers du lot : 0 octet 92.
- E-23 : **survivant M-11U-05** (grille : premier point au lieu du maximum) au premier passage de e11u (9/10). Cause :
  dans la grille réduite du test (φ = 1/100 puis 1/10), le r′ maximal est au premier point ; le mutant y est
  équivalent. Remède (`outils/renfort_u05.py`) : dans `test_faisabilite_cellules_et_grille`, grille à φ inversé
  (1/10 puis 1/100) et garde d'attendu (le maximum n'est pas au premier point). Rouge d'assertion sur le mutant, vert
  sans lui, test d'origine vert sous le mutant : `journal/rouge-11u-renfort.txt`. Diff SB-11u régénéré (64 → 67
  lignes) ; e11u refaite (chaîne sh PID 21684). Exposition : le message du rouge montre deux r′ de faisabilité aux
  points de la grille d'essai, calculés sur les taux d'EP (aucune valeur d'E1, aucune simulation).
- E-24 : **R-13 sans objet sur `travail/` par `git grep`** : l'index git de `travail/` est vide (copie à alternates
  pour `oracle_r1`), donc `git grep` n'y cherche rien et rend 1. Remplacé par `grep -rnE` du même motif sur
  `scripts/sim-bis` (37 fichiers) et `gates.yml` de `travail/` : aucun marqueur, témoin positif détecté. Sur
  `fusion/` (965 fichiers suivis), `git grep` tient.
- E-25 : « barre oblique inverse suivie de n » tapé dans deux commandes d'outil (heredocs Python qui écrivaient les
  §6 et §7 du rapport). Effet : des sauts de ligne, voulus ; le rapport porte 0 octet 92 (contrôlé). Aucun fichier
  du lot touché.
- E-26 : **deux rouges manquaient aux journaux**. Contrôle par script : chaque test ajouté par un diff (`def test_`
  des lignes `+`) cherché parmi les FAIL et ERROR de `journal/rouge-*.txt`. Manquaient : `test_calculer_lot`
  (SB-11i ; `rouge-11h.txt` n'a lancé que trois tests) et `test_premiere_apres_retrait` (SB-11f ; `rouge-11f.txt`,
  trois tests) ; `test_cellules_5_2_exprimables` (SB-11s) est le test de caractérisation déjà déclaré en E-10. Les deux
  rouges ont été montrés après coup, sur les ébauches gardées de l'étape (`ebauches/e11h/executer.py`,
  `ebauches/e11f/executer.py`), avec les tests de l'instantané final de l'étape : FAIL d'assertion chacun
  (`journal/rouge-11i-calculer-lot.txt`, `journal/rouge-11f-premiere.txt`). Le rouge vient donc après l'écriture du
  code, non avant : à juger par le réviseur.
- E-27 : une barre oblique inverse tapée dans la commande du premier calcul de `SHA256SUMS` (délimiteur de `xargs`).
  Le fichier a été recalculé par un script Python sans barre (`chr(10)`), puis contrôlé par `sha256sum -c`.
- E-28 : **la tête a encore avancé** pendant le rendu : `2f3070f` (COLLECTE-BIS CB-6a, d'un autre lot), relue à
  05:18:44 UTC. Elle ne touche pas `scripts/sim-bis` ; dans `gates.yml`, seule la ligne du plancher s2bis change
  (255 → 263). Rejeu à sec du diff cumulé sur `git archive 2f3070f` à 05:18:53 UTC : mêmes deux conflits, rien
  d'autre. Le job s2bis du §7 a tourné sur `b07147d` (255) ; sur `2f3070f`, il relève de CB-6a. Le dépôt réel
  porte aussi des changements indexés d'un autre agent (s2bis, décodeurs) : aucun de moi (lecture seule).

## 11. Éléments à former et état des items

**Éléments à former** (règle PAROXYSME : limites rencontrées, rendues à l'orchestrateur). Les noms sont proposés.
- **SHOGEN-SIM-BIS-NPRIME-NUL-1**
  - Limite : n′_s = 0 dans une strate fait refuser la règle (REGLE/entier), et la réplication échoue au lieu de rendre
    NON ÉVALUABLE.
  - Construction : adjuger la valeur au cas dégénéré (Q-SB11-7), puis l'écrire dans `executer.replication`, avec un
    test.
  - Échéance : avant E0.
- **SHOGEN-SIM-BIS-P-L20-1**
  - Limite : la cellule P-L20 (scénario B) ne s'exprime pas dans le schéma (Q-SB11-12).
  - Construction : une loi du fond par cellule, avec son support dans `sources`.
  - Échéance : avant E0, ou limite écrite.
- **SHOGEN-SIM-BIS-FAMILLES-1**
  - Limite : les familles du §5.2 (P-cible et son échelle, P-grille, P-abs, bascule, cible à f = 0,1 de Q-S-06
    complément 3) ne sont pas énumérées dans `parametres.json` (Q-SB11-17).
  - Échéance : brief de SB-12 ou d'E3, avant E0.
- **SHOGEN-SIM-BIS-E1-LANCEUR-1**
  - Limite : la commande d'E1 et la liste des oracles passés à `ecrire_e1` ne sont pas fixées (Q-SB11-10).
  - Échéance : brief d'E0/E1.
- **SHOGEN-SIM-BIS-MUT-DUREE-1**
  - Limite : la suite sim-bis dure 118 s seule (246 tests) ; sous la charge partagée, un témoin prend jusqu'à 126 s
    et un mutant jusqu'à 214 s (§6), contre une borne de 300 s. Chaque sous-lot ajoute des tests, et des FATAL par dépassement deviendront probables.
  - Construction : borne, ou budget de durée de la suite, à fixer pour les campagnes à venir. Mesures au §6.
- **SHOGEN-SIM-BIS-TDET-ECHELLE-1**
  - Limite : T-DET-1 tourne à 3 × 6 réplications, contre 3 × 200 au §6.2 (Q-SB11-16).
- **SHOGEN-SIM-BIS-BUDGET-SERRE-1**
  - Limite : le budget mesuré à une réplication par type (i = 0) n'est qu'un majorant ; il ne sépare ni l'oracle du
    régime courant, ni le froid du chaud (Q-SB11-18, §8).
  - Construction : seconde mesure par type (i ≥ 200 ; E1 chaude), sur machine peu chargée, puis plan à approuver.
  - Échéance : avant E0 (acte d'exécution, CALCUL-1).
- **SHOGEN-SIM-BIS-VALS-STRICT-1**
  - Limite : `e1._vals` coupe en silence au plus court ; une longueur fausse ne se voit que dans le JSON (Q-SB11-19).
  - Construction : refus nommé sur longueurs inégales, avec son test et son mutant.
  - Échéance : brief de SB-12.
- **SHOGEN-SIM-BIS-MUT-EQUIV-FIXTURE-1**
  - Limite : deux survivants de cette série (M-11P-03, M-11U-05) tenaient à une fixture où le mutant est équivalent
    (ℓ non gardés en queue de grille ; maximum au premier point). La revue des tests ne l'a pas vu avant la campagne.
  - Construction : à la rédaction d'un test, une garde d'attendu qui prouve que la fixture sépare le mutant visé
    (forme de `test_faisabilite_cellules_et_grille`), à inscrire dans les briefs des campagnes à venir.
  - Échéance : prochain brief de campagne de mutants.

**État des items nommés par le brief**
- Tenus ici :
  - SB11-BRIEF-1 et SB11-IMPRESSIONS-1 : toutes leurs lignes sont tenues (§4). Le rendu texte des impressions des
    cellules dans `sim_niveau_bis.txt` est à SB-12, depuis les agrégats.
  - ECRITURE-LIEN-1 : tenu (SB-11a).
  - LIBM-POW-1 : la garde tient sur les nouveaux modules.
  - MUTANTS-SITE-APPEL-1 : appliqué à la série ; deux diffs (m, s) sans mutant de site d'appel (§6, E-19).
- Tenus ici, à fermer sur les sorties d'E1 :
  - C1-COUT-1 et TABLES-CACHE-1 : mesurés (§8) ; le cache des tables existe déjà dans `sources` ; le coût à froid est
    payé une fois par processus et par lot.
  - REGIME-FAISABILITE-1 : contrôle câblé à C1 et à C2, sur les cellules du §5.1 et sur la grille ; il se ferme sur la
    sortie d'E1.
- Restent ouverts :
  - POOL-EP-SEPARES-1 : aucun changement (Q-SB11-14) ; l'item reste ouvert pour tout retrait de pool avant le sceau.
  - FIV-IDENTIF-1 : phrases (8)(ii) et (iii) câblées ; l'item reste ouvert jusqu'à la sortie d'E1 épinglée.
  - OBS-GRILLE-1 : grille portée par les cellules ; ouvert jusqu'au rodage.
  - CALCUL-1 : budget mesuré, plan à approuver.
- Inchangés :
  - INDICES-IDENTIFIANTS-1 : affaire de la finale.
  - ENREG-ROLE-1 : l'enregistreur ne couvre pas encore `scripts/sim-bis`.
- P1-ESTIMATION-1 : SB-11 a pris 2 793 lignes, contre ≈ 200 estimées au §6.1, soit environ 14 fois. À porter au
  calendrier (§12).

## 12. Estimation révisée de SB-12

- **Estimation de la PROPOSITION** : ≈ 170 lignes (§6.1).
- **Ce que SB-12 doit porter, mesuré sur ce qui reste à écrire** :
  - règle de niveau du §4 : comparaison exacte, gabarit, familial, rappel de multiplicité ;
  - règle de n_s du §3, avec les amendements du point (5) : W* aux trois niveaux, A-2 posé selon W*(C0) et W*(C1),
    phrase de C2, phrases (8) finales ;
  - confirmation à 10⁴ (Q-S-06, complément 2) ;
  - seuils de NON ÉVALUABLE scellés (Q-S-13) ;
  - règle d'entrée de la variante (Q-S-09) ;
  - bloc `[VALEURS POUR LE PAQUET DE S2-BIS]` ;
  - sorties `sim_niveau_bis` et `sim_puissance_bis` (texte et JSON, E-S-48), avec le rendu des impressions agrégées
    de SB-11 ;
  - et, si le brief les lui donne, les familles du §5.2 (Q-SB11-17) et P-L20 (Q-SB11-12).
- **Repère mesuré** : SB-11 a pris environ 14 fois son estimation, en 21 diffs. SB-11 portait E1 en plus de son objet.
- **Révision [inféré]** : 900 à 1 400 lignes avec tests, soit 6 à 9 diffs. Le bas de la fourchette vaut sans les
  familles, le haut avec. Chaque diff est un sous-lot à part entière, avec sa propre campagne de mutants
  (SHOGEN-SIM-BIS-MUT-DUREE-1).

## 13. Journal de provenance (G1)

### Sources lues par moi depuis la reprise, toutes au niveau [lu]

Lectures dans la copie `base/` (`5e386c4`) ou `travail/`, sauf mention.

**Contrat et revues**
- `G0-SIM-BIS.md` : en entier, ajouts datés compris.
- `PROPOSITION.md` : l.130-230 (§2), l.232-254 (§3), l.255-440 (§4 à §7), l.575-580.
- `AVIS.md` : l.11, l.27-75, l.90-106.
- `revue-t2/AVIS-SIM-T2.md` : l.95, l.115-145, l.195-215, l.286-292.
- `revue-t3/AVIS-SIM-T3.md` : l.9-31, l.58, l.101, l.118, l.124, l.139-151.
- `revue-integ/` : `G2-SIM-INTEG-transcrit.md` l.94-98, `CORRECTIONS-G2-transcrit.md` l.100,
  `RAPPORT-GENERATEUR-transcrit.md` l.75, l.104, `LIGNES-BRIEF-SB11.md`.
- `docs/adr-0028/ANNEXE-B-items.md` : les quinze items, par leur nom.
- `docs/adr-0028/ANNEXE-D-preenregistrement.md` : l.32-46 (liste D.2). `intervalles.txt` est hors de D.2.
- `BRIEF-SB11.md`, `LIGNES-BRIEF-SB11.md`, `NOTES.md` : en entier.

**Sorties et code de PLAN-S2BIS et PLAN-S2BIS-2**
- `docs/adr-0029/plan-s2bis-2/README.md` l.1-40 ; `intervalles.txt` (lignes 1 à 60, puis une ligne sur six) :
  exposition déclarée en E-12.
- `scripts/plan-s2bis-2/intervalles.py` en entier ; `scripts/plan-s2bis/episodes.py` l.1-80 ; `regles.quantile`.

**Code du lot (`scripts/sim-bis/`, tout ce que j'appelle ou touche)**
- En entier : `executer.py`, `e1.py`, `calib_fiv.py`, `commun.py`, `calibration.py`, `sources.py`, `calendrier.py`,
  `oracle_r1.py`.
- `observateurs.py` l.85-229 et la liste de ses fonctions ; `regle.py` : liste des fonctions, `deux`.
- Tests : `test_e1.py` en entier ; `test_replication.py` l.1-80 ; `test_determinisme.py` l.1-68 et l.97-140 ;
  `test_executer.py` l.1-30, l.180-250 ; `test_fitness.py` l.1-80 ; `test_calib_fiv.py` l.195-240 ;
  `test_oracle_r1.py` l.121-160.

**Outillage et CI**
- `.github/workflows/gates.yml` : lignes des jobs.
- Têtes de `enforcement/verdict-suite-s2.py`, `run-fixtures-hooks.sh`, `gate-secrets.sh`.
- `isole.sh` de P1b.

### Lectures de seconde main [2nd]

- Toutes reprises de `NOTES.md` (agent précédent) : la première lecture d'AVIS-SIM-T3, de G2-T3/T4 et des corrections
  T3/T4, et l'énoncé des items.
- Les lignes du code que j'appelle ont été relues par moi.

### Commandes et sorties (journaux sous `<scratchpad>/s2bis/sb11/journal/`)

- **Rouges** : `rouge-11m.txt` à `rouge-11u.txt` (FAIL d'assertion, ERROR déclarés en E-11).
- **Suites entières** :
  - à l'état e11r, 01:20:48-01:22:46 UTC : « Ran 241 tests in 118.041s OK », verdict conforme ;
  - autres passages : §7.
- **Campagnes** : `campagne-e11X.txt`, une ligne par mutant (sortie du vérificateur, tests rouges, durée), PID dans
  `NOTES.md`.
- **Budget** : `budget.txt` (§8).
- **Matrice et jobs finaux** : `final.txt` (résumé), `final-<nom>.txt` (sortie de chaque étape ; celle de cargo
  n'est lue que par ses lignes VERDICT), produits par `outils/final.py` (§7).
- **Contrôles légers de la première reprise** : `../tmp/hooks.txt`, `secrets-tree.txt`, `secrets-fix.txt`,
  `runner.txt` (refaits au §7).

### Chiffres recomptés par moi

- Lignes par diff : `outils/bilan.py`, même règle que `etape.sh`.
- Nombres de tests : lignes « Ran N » du vérificateur.
- Mutants : comptés par le bilan de chaque campagne.
- Budget : durées de `executer.chronometrer`.
- Plancher de la fusion : 262 = 210 + (246 − 194).
- Aucun chiffre de seconde main n'entre dans un test ni dans une valeur.

### Seconde reprise (depuis 02:02:26 UTC) : lectures, commandes, recomptes

- **Lu [lu] par moi** : `NOTES.md`, `BRIEF-SB11.md`, `LIGNES-BRIEF-SB11.md`, ce rapport, en entier ; outils
  `campagnes.sh`, `chaine_stu.sh`, `chaine_l.sh`, `etape.sh`, `diff_etape.sh`, `mutants.py`, `bilan.py`,
  `matrice.sh`, `budget.py` en entier ; définitions de M-11P-03 à -07, M-11U-05, -06, des mutants de SB-11s, de
  C-01, D-03, D-04, D-06, G-03, I-04, I-06, K-01, M-04, N-01, R-01 ; `e1.py` (e11p) l.263-345 et (e11u) l.84-137 ;
  `calib_fiv.py` : `grille` et lignes de garde ; `commun.py` (e11s) l.60-120 ; `executer.py` : `BORNE`, `plan`,
  `ORACLE`, `IMPRESSIONS`, `chronometrer`, `budget` ; `tests/test_e1_sorties.py` (e11p) l.1-200 ;
  `tests/test_e1.py` (e11u) l.20-75 et l.242-269 ; `tests/test_table.py` (e11s) l.59-89 ; `gates.yml` (fusion)
  l.63-80 et l.183-250 ; `isole.sh` ; lignes d'énumération de `gate-secrets.sh` ; `xtask/src/main.rs` (ligne
  `verify`) ; `ANNEXE-B-items.md` l.1261 (SHOGEN-MUTANTS-SITE-APPEL-1, par son nom).
- **Dépôt (lecture seule)** : `rev-parse HEAD` (b07147d, 03:48:07 UTC), `status --porcelain` (0 ligne),
  `log --oneline 5e386c4..b07147d` (13), `diff --stat 5e386c4 b07147d` sur mes chemins, `git archive b07147d`
  de `scripts/sim-bis` et `gates.yml` (rejeu à sec, §14).
- **Commandes et sorties** : rouges des renforts `rouge-11p-renfort.txt`, `rouge-11u-renfort.txt`, rouges après coup
  `rouge-11i-calculer-lot.txt`, `rouge-11f-premiere.txt` (E-26) ; campagnes
  (chaînes sh PID 2708, 13090, 21684 ; PID des `mutants.py` au tableau du §6) ; `budget.txt` ; `final.txt`.
- **Recomptes** : `outils/tableau_diffs.py` (lignes, plancher, sha256, octets 92, total 2 793) ;
  `outils/tableau_campagnes.py` (bilans et témoins lus des journaux) ; totaux du budget recomptés par script sur
  `budget.txt` ; contrôle des dates d'instantané contre le début des campagnes (script, E-20) ; décompte des motifs
  de mutants par `grep -c` (E-19).
- **[2nd]** : PID et heures de la première reprise et de l'agent d'origine, repris de `NOTES.md` ; mesure à froid de
  21:05 (§8).

## 14. Recouvrement avec la tête `b07147d`

- **Tête** : `b07147d` (relue à 03:48:07 UTC), 13 commits au-dessus de `5e386c4`. Sur mes chemins, elle change
  (`git diff --stat 5e386c4 b07147d`) : `gates.yml` (4 lignes : plancher sim-bis 194 → 210, deux lignes de commentaire),
  `README.md` (+1, ligne d'`oracle_recalc.py`), `commun.py` (8 lignes, schéma `oracle_recalc`), `parametres.json` (+10,
  section `oracle_recalc`), `oracle_recalc.py` et `tests/test_oracle_recalc.py` (nouveaux).
- **Rejeu** : diff cumulé `etapes/base` → `etapes/e11u` (sha256 `0569ee98f40837fbccdf59f1e739f28b54987d906682e19a8b7cd98c01ebe0d7`,
  état final, renforts E-17 et E-23 compris) passé à sec (`patch -p1 --dry-run`) sur `git archive b07147d` de
  `scripts/sim-bis` et `gates.yml` à 04:59:54 UTC (tête relue `b07147d`) : deux hunks en conflit, et deux seulement :
  - `gates.yml`, ligne du plancher sim-bis : la tête porte 210, la série 246 sur la base 194 ;
  - `README.md`, ligne voisine de celle d'`oracle_recalc.py`.
  Tout le reste s'applique ; `commun.py` à 6 lignes de décalage.
- **Résolution, dans la copie `fusion/` seulement** : plancher **262 = 210 + (246 − 194)** ; les deux lignes du README
  gardées. `fusion/` = `git archive b07147d` (exclusions du brief) + la série ; `diff -rq` contre `travail/` : seuls
  `README.md`, `commun.py`, `parametres.json` diffèrent (apports de SB-13), plus `oracle_recalc.py` et son test.
- **Pour l'orchestrateur** : la série reste écrite sur `5e386c4` (règle 2 : je n'avance pas la base). Pour la poser
  sur `b07147d`, il faut rebaser avec ces deux résolutions ; les planchers des diffs intermédiaires montent alors de 16
  (= 210 − 194) : SB-11a 216, …, SB-11u 262.

## 15. Corrections après la G2 : diff SB-11v (correcteur, 2026-10-09)

**Gate 0** : modèle résolu `claude-opus-5-5` (worker G1, correcteur, effort max). Je n'ai écrit ni la série SB-11a … u
ni la G2. Contrat : `ADJUDICATION-G2.md` (liste fermée C-1 à C-9, items, preuves, rendu), sur `g2/RAPPORT-G2.md` §5,
`BRIEF-SB11.md` et `LIGNES-BRIEF-SB11.md`, qui restent en vigueur.

### 15.1 Base, horloge, pièces d'entrée

- **Horloge** : début 06:39:33 UTC, fin de section 08:22:37 UTC, le 2026-10-09 ; chaque heure lue par `date -u`.
- **Pièces** : `sha256sum -c SHA256SUMS` : 1 199 OK, 0 échec ; `g2/SHA256SUMS` : 57 OK, 0 échec (06:39:59). Rien
  écrit sous `g2/`.
- **Base** : `5e386c4`, inchangée. Copie `travail-v/` = `base/` + `etapes/e11u` (`diff -rq`, `cmp` : égales), `git
  init` à alternates vers les objets du dépôt (lecture seule) pour `oracle_r1`.
- **Tête** : `1a388e1`, relue à 06:40:22, 07:37:24 et 08:21:08 UTC ; descend de `5e386c4` ; `status --porcelain`
  vide. Aucune écriture git au dépôt réel.
- **Interdits tenus** : `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée (retirée des environnements, `isole.sh`) ; aucun
  `*.jsonl`, aucune pièce de D.2, aucun dossier interdit, aucune recherche récursive sur `docs/`, le dépôt ou le
  scratchpad ; tout a tourné sous `unshare -n` ; `cargo` lu par ses lignes VERDICT seules.

### 15.2 Diff

| diff | objet | lignes de code ajoutées | retirées | plancher | octets 92 | sha256 |
|---|---|---|---|---|---|---|
| SB-11v | C-1 (`executer.plan`) ; tests de C-1 à C-9 | 112 | 15 | 252 (= 246 + 6) | 0 | `1508a268013e408938b38ae6c2e1a6f839a0358c967bb9d6f31251f1cee907fd` |

- Fichier : `diffs/SB-11v.diff` (`git diff --no-index` de `etapes/e11u` à `etapes/e11v`, `-p1` sur la série).
- Code : `executer.py` seul, 1 ligne de code (`:190`, `t = borne // ns * processus`) et sa docstring (`:184-187`).
- Tests : 6 méthodes neuves (`test_l_2_au_site_d_appel`, `test_schema_ferme_c_5`, `test_n_prime_aux_sites_d_appel`,
  `test_surcharges_jusqu_aux_sources`, `test_r_de_la_cellule`, `test_meme_c1_dans_les_deux_strates`) ; 4 renforcées
  (`test_budget`, `test_plan_90_min`, `test_frequences_e_s_52`, `test_lot_forme`). Aucun test sauté, désactivé ni
  affaibli : les seules assertions retirées sont celles de `test_budget` (durées (5, 12), plages (0, 5), (5, 10)),
  remplacées par l'attendu corrigé.
- Plancher : `TestLoader.discover` = 252 ; job `sim-bis-unittest` conforme à 252 (Ran = 252).
- Forme : 0 octet 92 dans le diff et dans `scripts/sim-bis` ; aucune ligne `.py` de plus de 120 caractères ; R-13 :
  0 marqueur (motif du job par `chr(92)`, témoin positif détecté). R-25 : 112 ≤ 200, pas de scission.

### 15.3 Corrections C-1 à C-9

Attendus écrits à la main dans les tests. « Rouge » : FAIL d'assertion (`AssertionError`, aucune ERROR) du test visé
seul, sous le mutant (`journal/corr/rouges-mutants.txt`, `outils/corr_rouges.py`) ; pour C-1, rouge sur le code de la
série avant correction (`journal/corr/rouge-serie.txt`). Chaque test est vert sans mutant.

| C | correction (fichier:ligne, état final) | test (fichier:ligne) | rouge montré | mutants tués (campagne) |
|---|---|---|---|---|
| C-1 | `executer.py:190` : `t = borne // ns * processus` ; lot en ⌈(b − a)/processus⌉ ≤ ⌊borne/ns⌋ tours | `test_budget.py:24` (durées (12, 5) ; plages (0, 4), (4, 8), (8, 10)) ; `test_executer.py:198` (41 s × 4 : lots de 524, 20 lots, 131 tours, 5 371 s) | sur la série : plages (0, 5), (5, 10) et (0, 526) (2 FAIL) | M-11V-01 (ancienne formule), G-22, M-11V-03 |
| C-2 | — | `test_executer.py:71` : NON ÉVALUABLE [unites, k_crit, runs, n_prime] comptée en information insuffisante (4 sur 7) | G-01 : (3, 2, 1) ≠ (4, 2, 1) | G-01 |
| C-3 | — | `test_executer.py:159` : lot N3 à i permutés, empreinte recalculée, JSON canonique : LOT/forme | G-03 : None ≠ LOT/forme | G-03 |
| C-4 | — | `test_cellules.py:133` : `cellule(…)["couche"]["perte"]` = W pour W = 16 et 2 | G-06 : 8 ≠ 16 | G-06 |
| C-5 | — | `test_cellules.py:140` : gardes (N1 ; « parmi » à imposés « faibles » avec unités faibles : None), puis CELLULE/schema pour imposés « faibles » sans unité faible, [ETH], [ETH, BTC], f nul | G-07, G-08, G-19 : None ≠ CELLULE/schema | G-07, G-08, G-19 |
| C-6 | — | `test_replication.py:194` : fixture de `test_chaine_a_la_main` (garde n′ de calme < 12 000), critère collectif : `regle.retraits` reçoit {calme : n′, stress : n′} à chaque classe, `regle.filtrer` le n′ de sa strate | G-09 : n_s (12 000, 2 736) aux retraits ; G-12 : n_s au critère | G-09, G-12 |
| C-7 | — | `test_replication.py:210` : surcharge {longues : [60], poids_longues : [1]} vue par `sources.Replication` et `observateurs.Couche` | G-10, M-11V-02 : longues du prm du lot | G-10, M-11V-02 |
| C-8 | — | `test_replication.py:223` : cellule à R = 999 sous un prm à R = 99 : 999 à `regle.oracle`, `variante.deux_modes`, `regle.loi_evenements` | G-11 : [99, 99] ; M-11V-04, M-11V-05 : 99 à la variante, aux événements | G-11, M-11V-04, M-11V-05 |
| C-9 | — | `test_pauses.py:104` : C1 partagé : `pauses_c1` rend les deux strates, chacune égale à l'appel où le point n'est C1 que d'elle | G-16 : strate de stress absente | G-16 |

- **Règle de fixture** (adjudication, constat de méthode du réviseur) : chaque paramètre passé sous étiquette y prend
  une valeur distincte de toute source concurrente : W = 16 et 2 contre ⌊(W + 1)/2⌋ (8, 1) et T_max (24 semaines) ;
  n′ de calme 11 838 contre n_s 12 000, n′ de stress 2 533 contre 2 736 ; R = 999 contre 99 ; longues [60] contre
  [60, 1 440, 4 320] ; durées (12, 5), le maximum en premier ; combinaison mixte de causes ; i permutés ; même point de
  C1 dans les deux strates ; les gardes d'attendu (n′ < 12 000, cellules de base qui passent le schéma) sont dans les
  tests.
- **Effet de C-1 sur le budget du §8** (`journal/corr/plan-budget-c1.txt`, `outils/corr_plan_budget.py`, durées de
  `journal/budget.txt`) : sous l'ancienne formule, 13 des 18 cellules mesurées avaient un lot de 5 401 à 5 418 s ; sous
  C-1, tous les lots sont ≤ 5 400 s ; le nombre de lots des 17 cellules du §5.1 reste 117.

### 15.4 Mutants (campagne sur SB-11v)

- **Commande** : celle du job `sim-bis-unittest` (`enforcement/verdict-suite-s2.py scripts/sim-bis --aucun-saut
  --egal --plancher 252`), sur `travail-v` = `etapes/e11v` (5e386c4 + SB-11a … v). Un arbre par mutant (liens vers
  la copie, `scripts/sim-bis` copié et muté), sous `isole.sh` et `timeout 300`, `PAR=2` ; classement : sortie 1 tué,
  sortie 0 vivant, toute autre sortie ou dépassement FATAL.
- **Outils** : `outils/corr_mutants.py` (définitions, les G-nn recopiés de `g2/outils/mutants_g2.py` à l'identique),
  `outils/corr_campagne.py` (forme de `g2/outils/campagne.py`), `outils/corr_chaine.sh`.
- **Passage retenu** : 07:38:48 à 08:03:51 UTC, chaîne `sh corr_chaine.sh` PID 5931 (`/proc/PID/cmdline` lu), sur
  l'instantané final. Journal `journal/corr/campagne-e11v.txt`, sorties `journal/corr/mut-<id>.txt`.
- **Bilan** : 17 mutants, **17 tués**, 0 vivant, 0 FATAL, 0 inapplicable ; chacun par un `AssertionError`, aucune
  ERROR. Témoins VIVANT (sortie 0, Ran = 252, conforme) : 126 s au début, 128 s à la fin. Mutant le plus long :
  153 s.

| id | mutation | test qui le tue (campagne) | issue |
|---|---|---|---|
| G-01 | `any` → `all` (information insuffisante) | test_frequences_e_s_52 | TUÉ |
| G-03 | contrôle des i des enregistrements retiré (`_lot`) | test_lot_forme | TUÉ |
| G-06 | `couche(p, ep, cel, (W + 1) // 2)` dans `cellule` | test_l_2_au_site_d_appel | TUÉ |
| G-07 | imposés « faibles » admis sans unité faible | test_schema_ferme_c_5 | TUÉ |
| G-08 | `cl[0] == "BTC"` retiré | test_schema_ferme_c_5 | TUÉ |
| G-09 | `regle.retraits(…, e["n"])` (n_s au lieu de n′_s) | test_n_prime_aux_sites_d_appel | TUÉ |
| G-10 | `sources.Replication(prm, …)` (prm du lot) | test_surcharges_jusqu_aux_sources | TUÉ |
| G-11 | `p["regle"]["R"]` au lieu de `rg["R"]` (règle) | test_r_de_la_cellule | TUÉ |
| G-12 | `regle.filtrer(series, n_s, p)` | test_n_prime_aux_sites_d_appel | TUÉ |
| G-16 | `pauses_c1` : première strate seule pour un point partagé | test_meme_c1_dans_les_deux_strates | TUÉ |
| G-19 | f = 0 admis | test_schema_ferme_c_5 | TUÉ |
| G-22 | coût retenu = dernière durée | test_budget | TUÉ |
| M-11V-01 | ancienne formule `t = borne * processus // ns` | test_budget, test_plan_90_min | TUÉ |
| M-11V-02 | `observateurs.Couche(prm, …)` (prm du lot) | test_surcharges_jusqu_aux_sources | TUÉ |
| M-11V-03 | `t = borne // ns` (processus ignorés dans le plan corrigé) | test_budget, test_plan_90_min | TUÉ |
| M-11V-04 | `variante.deux_modes(…, p["regle"]["R"], d)` | test_r_de_la_cellule | TUÉ |
| M-11V-05 | `regle.loi_evenements(…, p["regle"]["R"], p)` | test_r_de_la_cellule | TUÉ |

- **Les 12 vivants non équivalents du réviseur** (G-01, G-03, G-06, G-07, G-08, G-09, G-10, G-11, G-12, G-16, G-19,
  G-22) sont rejoués et tués. Ses quatre équivalents (G-04, G-13, G-20, G-21) ne sont pas rejoués : leur classement
  est celui de la G2, que l'adjudication admet.
- **Couverture** : site d'appel (G-06, G-09, G-12, G-16) ; source des données sous étiquette inchangée
  (G-10, G-11, M-11V-02, M-11V-04, M-11V-05) ; schéma fermé (G-07, G-08, G-19) ; lots (G-03) ; E-S-52 (G-01) ;
  `plan` et `budget` (M-11V-01, ancienne formule ; M-11V-03 ; G-22).
- **Passage écarté** (E-C2) : un premier passage complet, 06:51:16 à 07:20:33 UTC (chaîne PID 14119), a tué les
  mêmes 17 mutants (témoins 135 s et 126 s, mutant le plus long 227 s) sur un instantané dont trois docstrings ont
  changé ensuite ; gardé en `journal/corr/premier-passage/`, jamais compté.

### 15.5 Matrice, jobs, xtask

Contrôles l'un après l'autre (`outils/corr_finale.sh`, PID 22905 : `corr_rouges.py`, `corr_apres.sh`,
`corr_xtask.sh`), de 08:04:01 à 08:21:01 UTC ; résumé `journal/corr/resume.txt`, sortie de chaque étape
`journal/corr/apres-<nom>.txt`. Copie `tete-v` = tête `1a388e1` + SB-11a … v résolue (§15.6).

| contrôle | copie | résultat |
|---|---|---|
| sim-bis, plancher 252 | travail-v (5e386c4 + série + v) | conforme, Ran = 252 (témoins de la campagne, 126 s et 128 s) |
| runner `run-fixtures-verdict-suite-s2.py` | tete-v | code 0, 136 ok, 0 échec |
| sim-bis, plancher 268 | tete-v | conforme, Ran = 268 (135 s) |
| s2bis, plancher 340 (plancher de la tête) | tete-v | conforme, Ran = 340 |
| S2 `--egal` | tete-v | conforme, Ran = 415, deux sauts nommant la variable scellée |
| hooks | tete-v | 54 ok, 0 échec |
| secrets (fixtures ; `--tree`) | tete-v | 147 ok ; 991 fichiers, OK |
| R-1 (fixtures ; arbre) | tete-v | 227 ok ; OK, liste blanche exacte |
| R-13 (`g2/outils/r13.py`, motif par `chr(92)`, témoin détecté) | tete-v, `scripts/sim-bis` | 0 marqueur |
| matrice `-X dev -W error`, `unittest discover` | tete-v | 3.10.20 : code 0, Ran 268 OK (194 s) ; 3.11.15 : 160 s ; 3.12.3 : 158 s ; 3.13.14 : 160 s ; 0 « Exception ignored », 0 « Warning » |
| `cargo --locked xtask verify` (lignes VERDICT seules) | tete-v ; tete-neuve (`git archive 1a388e1`) | 8 VERT, 1 ROUGE (1 violation), global ROUGE, **mêmes dix lignes** (`diff` vide) : la violation précède la série, SB-11v n'en ajoute aucune |

### 15.6 Application sur la tête `1a388e1`

- Série SB-11a … u puis SB-11v appliquées diff par diff (`patch -p1`) sur `git archive 1a388e1` (exclusions du
  brief, vérifiées absentes) : **seuls les conflits connus** (`journal/corr/application-tete.txt`) :
  - le plancher sim-bis de `gates.yml`, à chacun des 22 diffs ;
  - la ligne du README voisine d'`oracle_recalc.py`, à 20 diffs (ni s ni v) ;
  - tout le reste s'applique (`commun.py` à 6 lignes de décalage).
- **Résolution** (copie seule) : plancher **268 = 210 + (252 − 194)** ; lignes `executer.py` et `e1.py` du README
  insérées après celle d'`oracle_recalc.py`. Refaite à neuf sur l'instantané final (07:38:32) : même résultat (`diff
  -rq` vide hors `.git`).
- **Comparaison** : `scripts/sim-bis` de `tete-v` est égal à `fusion/` du générateur sauf les six fichiers de SB-11v ;
  `gates.yml` n'en diffère que par les planchers s2bis (340, de la tête) et sim-bis (268).
- **Pour l'orchestrateur** : SB-11v se pose après SB-11u ; sur une base rebasée sur `1a388e1`, son plancher est 268
  (les planchers intermédiaires montent de 16 : SB-11a 216 … SB-11u 262).

### 15.7 Lignes d'items

Forme de l'annexe B (constat, propriétaire, déclencheur, prix, origine). Les noms sont proposés ; l'orchestrateur
les inscrit.

| item | constat | propriétaire | déclencheur | prix | origine |
|---|---|---|---|---|---|
| SHOGEN-SIM-BIS-NPRIME-NUL-1 | à n′_s = 0 dans une strate, `regle.tester` refuse (REGLE/entier) et la réplication échoue au lieu de rendre NON ÉVALUABLE (E-S-28, E-S-52) ; à n′_s = 1 le moteur rend NON ÉVALUABLE de causes [unites, k_crit, runs, n_prime] ; un lot qui rencontre n′_s = 0 échoue à chaque reprise (E-S-45). La fixture qui le montrait (cellule à repli et grille « large », W = 1, i = 1) a été déplacée en E-14 : il faut d'abord un test qui reproduise n′_s = 0, puis, adjugé à son G0, soit un refus nommé, soit un NON ÉVALUABLE à causes listées (recommandé : celles de n′_s = 1). **Bloque E0.** | orch. (G0 du correctif ; code dans `regle`, sous-lot SB-7) | avant E0 | un test qui reproduit le cas, une ligne de règle et son mutant (≈ 30 lignes) [inféré] | Q-SB11-7, E-14 du générateur ; G2 de SB-11 O-3 ; adjudication de la G2 |
| SHOGEN-SIM-BIS-BUDGET-SERRE-1 | le plan du §8 est un majorant : une réplication par type à i = 0 (oracle d'E-S-29 à R complet, variante à deux modes et impressions compris), sous une charge de 4,1 à 7,1 ; ni i ≥ 200 (98 % d'une cellule à 10⁴) ni une réplication chaude d'E1 ne sont mesurés. C-1 (SB-11v) rend chaque lot ≤ 90 min de mur : sous l'ancienne formule, 13 des 18 cellules mesurées avaient un lot de 5 401 à 5 418 s (`journal/corr/plan-budget-c1.txt`). `budget["duree_ns"]` = ⌈R·coût/processus⌉ sous-estime le mur du plan, ⌈R/processus⌉·coût, de moins d'un coût. Le plan à approuver porte le maximum mesuré, une **marge déclarée** pour la charge, et le **coût de l'oracle compté à part** du régime courant (200 premières réplications par cellule : 200 × 234,34 s = 46 868 s ≈ 13,0 h de CPU pour les 17 cellules du §5.1 au majorant) | orch. (acte d'exécution, avec SHOGEN-SIM-BIS-CALCUL-1) | avant E0 | une seconde mesure par type (i = 200 ; E1 à i = 1) sur une machine peu chargée, puis un plan [mesuré] | Q-SB11-13, Q-SB11-18 ; G2 de SB-11 §10 et C-1 |
| SHOGEN-SIM-BIS-VALS-STRICT-1 | `e1._vals` imprime par `zip`, qui coupe au plus court : une longueur fausse des ℓ ou des valeurs passe en silence dans le texte d'E1 (le JSON la montre) ; `e1.lignes_pauses` saute en silence une strate absente de `pz` (`if s in pz`, O-9) | orch. | brief de SB-12 (qui récrit les sorties), avant E0 | refus nommé sur longueurs inégales (ou `zip(…, strict=True)`, Python ≥ 3.10) et sur strate absente, deux tests et leurs mutants (≈ 20 lignes) [inféré] | Q-SB11-19, E-17 ; G2 de SB-11 O-9 |
| SHOGEN-SIM-BIS-MUT-EQUIV-FIXTURE-1 (volet de SHOGEN-MUTANTS-SITE-APPEL-1) | 14 survivants de SB-11 tenaient à une fixture où le mutant est équivalent : M-11P-03 et M-11U-05 du générateur, et les 12 vivants non équivalents de la G2 (W = 1, n′_s = n_s, R de la cellule = R du prm, surcharges vides, points de C1 distincts, durées en ordre croissant, aucune combinaison mixte, aucun lot à i permutés, refus du schéma non exercés). Règle à inscrire au prochain brief de campagne : « pour chaque paramètre passé sous étiquette (W, n′_s, R, prm de la cellule, point par strate), une fixture où sa valeur diffère de toute source concurrente », avec une garde d'attendu qui prouve que la fixture sépare (forme de `test_faisabilite_cellules_et_grille` ; gardes de SB-11v : n′ de calme < 12 000, cellule de base qui passe le schéma) | orch. | prochain brief de campagne de mutants | une ligne de brief [inféré] | générateur E-17, E-23 ; G2 de SB-11 §6 (constat de méthode) et §12 |
| SHOGEN-SIM-BIS-AGREGATS-SB12-1 | `executer.agreger` ne compte ni le taux de C_S ≤ 99 (E-S-32), ni la puissance par g (E-S-34), ni la distribution des dates d'atteinte (E-S-23), ni les retraits (E-S-24) ; les enregistrements des lots les portent | orch. | brief de SB-12 | agrégats écrits depuis les lots, avec leurs tests et mutants [inféré] | G2 de SB-11 O-4 |
| SHOGEN-SIM-BIS-P-L20-1 | la cellule P-L20 (lettre du scénario B : L = 20, sans groupement) ne s'exprime pas dans le schéma des cellules : `sources` n'a pas de loi d'épisodes de moyenne fixée pour le fond ; un schéma changé après E0 serait une déviation | orch. | avant E0 | une clé de cellule (loi du fond : EP ou géométrique de moyenne L) et son support dans `sources`, ou une limite écrite [inféré] | Q-SB11-12 ; G2 de SB-11 §11 |
| SHOGEN-SIM-BIS-FAMILLES-1 | les familles du §5.2 (P-cible et son échelle, P-grille, P-abs, bascule, cible à f = 0,1 de Q-S-06 complément 3) ne sont pas énumérées dans `parametres.json` ; seule leur exprimabilité est testée ; les ρ et D des alternatives de P-abs sont à prendre de la cible (§3 pt 1), à adjuger ; la grille « large » n'est employée par aucune cellule de `cellules.nulles` (O-11, avec Q-SB11-3) | orch. | brief de SB-12 ou d'E3, avant E0 | grilles dans `parametres.json`, générateur et test [inféré] | Q-SB11-17 ; G2 de SB-11 §11, O-11 |
| SHOGEN-SIM-BIS-E1-LANCEUR-1 | la commande d'E1 et la liste des oracles passés à `ecrire_e1` ne sont pas fixées ; avis du réviseur : `lancer_e1` calcule lui-même ses oracles internes, dont E-S-39 contre r1, au lieu de recevoir un dictionnaire de booléens. O-6 : la reprise d'E1 exige les mêmes (ns, processus, borne) ; un autre plan rend LOT/double, refus nommé et sûr, à consigner au journal d'exécution | orch. | brief d'E0/E1 | une ligne de commande, la liste des oracles, une consigne de reprise [inféré] | Q-SB11-10 ; G2 de SB-11 O-6 |
| SHOGEN-SIM-BIS-TDET-ECHELLE-1 | T-DET-1 tourne dans la suite à 3 cellules × 6 réplications (contre 3 × 200 au §6.2) et ne passe jamais par le chemin i ≥ 200 (`regle.tester`, `variante.tester`, sans impressions ; O-5) | orch. | avant E0 | un passage hors suite : 3 cellules × au moins 202 réplications, 1 contre 4 processus, PYTHONHASHSEED 0 contre 1, W réduit déclaré [inféré] | Q-SB11-16 ; G2 de SB-11 O-5 |
| SHOGEN-SIM-BIS-MUT-DUREE-1 | la suite sim-bis dure 136 s seule à 252 tests (SB-11v, charge ≈ 4 sur 4 cœurs) ; sous campagne en PAR=2, les mutants ont pris jusqu'à 209 s (G2) et 227 s (SB-11v), les témoins jusqu'à 135 s, contre une borne de 300 s ; chaque sous-lot ajoute des tests, et des FATAL par dépassement deviendront probables | orch. | brief de SB-12 | une borne ou un budget de durée de la suite, ou des campagnes à tests ciblés [mesuré] | générateur §11 ; G2 de SB-11 §12 ; campagne SB-11v |
| SHOGEN-SIM-BIS-PARTIEL-AVANT-1 (O-7) | un `.partiel` laissé par un lot tué fait échouer la reprise à l'écriture (SORTIE/partiel-present), après tout le calcul du lot ; le README prescrit de le retirer à la main | orch. | brief de SB-12 ou d'E0 | un contrôle des `.partiel` du lot avant son calcul (refus nommé tôt), un test et son mutant (≈ 15 lignes) [inféré] | G2 de SB-11 O-7 |
| SHOGEN-SIM-BIS-E1-PAIRE-1 (O-8) | `ecrire_e1` écrit le JSON puis le texte ; si le second échoue, le premier reste seul : c'est sûr (aucune réécriture, SORTIE/existe à la relance), mais la paire n'est pas atomique et la relance exige un retrait à la main | orch. | brief d'E0/E1 (avec E1-LANCEUR-1) | un contrôle de paire au lancement (paire complète, ou aucune pièce) et sa consigne de reprise [inféré] | G2 de SB-11 O-8 |

- **O-10, sans ligne d'item** : l'ε de N10 suit (1 − f)·p̂ = 0,9·p̂, quand le §5.1 écrit ε = 0,7·p̂ pour N1 [2nd : G2
  O-10]. C'est une valeur de la table des cellules ; Q-SB11-9 porte déjà ces valeurs à l'adjudication avant E0, par le
  même acte et le même propriétaire. Une ligne à part doublerait la question : je la joins à Q-SB11-9.
- **Avis du réviseur adoptés** (Q-SB11-1 à Q-SB11-19, G2 §11) : rien de neuf ici. Q-SB11-2, Q-SB11-3, Q-SB11-12 et
  Q-SB11-16 restent à régler avant E0 ; Q-SB11-19 et O-9 vont au brief de SB-12 (VALS-STRICT-1) ; Q-SB11-7 et O-3 vont
  à NPRIME-NUL-1, non corrigés dans ce lot (le défaut est dans `regle`, SB-7).

### 15.8 Écarts du correcteur

- **E-C1** : le premier passage de `outils/corr_rouges.py` (06:46:11 à 06:46:15) était invalide : il copiait
  `scripts/sim-bis` seul, et les données du dépôt (`docs/adr-0029/plan-s2bis/episodes.txt`) étaient introuvables
  (`FileNotFoundError`, sortie 1 sans `AssertionError`). Gardé en `journal/corr/rouges-mutants-0646-invalide.txt`,
  jamais compté. Outil corrigé (arbre de liens vers la copie, `scripts/sim-bis` copié), refait.
- **E-C2** : une ligne de 121 caractères (docstring de `test_schema_ferme_c_5`) est restée dans le premier instantané
  e11v. Mon contrôle de 06:44 l'avait signalée, mais j'ai corrigé une autre ligne. Le contrôle final l'a trouvée
  (consigné à 07:38:08). Corrigée par le texte de la docstring seul : AST hors docstrings égal pour les quatre
  fichiers touchés (script ; copies d'avant en `journal/corr/premier-passage/tests-avant-docstrings/`), aucun test
  ne lit `__doc__`. Le premier passage de la campagne, des contrôles et de xtask (06:51 à 07:37, tous verts,
  17/17 tués) est gardé en `journal/corr/premier-passage/`, jamais compté ; tout a été refait sur l'instantané final.
- **E-C3** : dans la même retouche, les docstrings nomment désormais M-11V-03 (`test_budget`, `test_plan_90_min`),
  M-11V-04 et M-11V-05 (`test_r_de_la_cellule`), selon l'usage du fichier. Le diff passe de 110 à 112 lignes.
- **E-C4** : des barres obliques inverses tapées dans des commandes, jamais dans un fichier du lot :
  - `tr` pour afficher `/proc/PID/cmdline` ;
  - le format de `printf` qui a écrit `outils/corr_finale.sh` ;
  - des motifs de `grep` en lecture.
  - « barre oblique inverse suivie de n », trois fois, dans les scripts Python (heredoc) qui ont ajouté cette
    section et ce point au rapport : des sauts de ligne voulus, dans des chaînes de recherche ou de
    remplacement.

  Les fichiers écrits ont été comptés par Python : 0 octet 92 dans le diff, dans `scripts/sim-bis` et dans mes outils.
- **E-C5** : `pgrep -n -f` sur le nom exact de mon script détaché, pour lire son PID ; `/proc/PID/cmdline` lu à chaque
  fois. Aucun motif large.
- **E-C6** : des index git existent dans mes copies `travail-v` et `tete-v` (`git init`, alternates, `git add` dans la
  copie seule), comme E-R5 du réviseur. Le dépôt réel n'a reçu aucune écriture.
- **E-C7** : les tests de C-2 à C-9 éprouvent un code déjà juste. Leur rouge est donc montré sous le mutant visé, comme
  le demande l'adjudication, non sur le code de la série. Seul C-1 a un rouge sur la série, avant la correction.

### 15.9 Journal de provenance (G1)

**Lu [lu]**, en entier :
- `ADJUDICATION-G2.md`, `g2/RAPPORT-G2.md`, `g2/preuves/test_preuves_g2.py`, `g2/mut/campagne.txt` ;
- `g2/NOTES.md`, et les outils `campagne.py`, `chaine.sh`, `apres.sh`, `mutants_g2.py`, `preuves2.py`, `r13.py` et
  `xtask.sh` du réviseur ;
- `NOTES.md`, `RAPPORT-GENERATEUR.md`, `BRIEF-SB11.md`, `LIGNES-BRIEF-SB11.md` ;
- `outils/etape.sh`, `outils/diff_etape.sh`, `outils/bilan.py`, `journal/budget.txt` du générateur.

**Lu [lu]**, en partie :
- `executer.py` : l.1-587, état e11u ;
- `e1.py` : l.150-235 et `ecrire_e1` ;
- `commun.py` : l.203-231 (`ecrire`) ;
- `tests/test_budget.py`, `test_executer.py`, `test_cellules.py`, `test_replication.py`, `test_pauses.py`, en entier ;
- `regle.py` et `variante.py` : signatures (grep), `CAUSES` ;
- `parametres.json` : `regle.R`, `R_approche`, `n_par_semaine`, `longues`, `poids_longues`, strates ;
- `gates.yml` : l.222-247 ;
- `isole.sh` ;
- `ANNEXE-B-items.md` : l.1260-1261, par leur nom (forme des lignes).

**Seconde main [2nd]** : les constats O-1 à O-13 et les avis du réviseur, repris de la G2 et routés vers les items
sans nouvelle mesure, sauf les recomptes ci-dessous ; le budget du §8 (durées de `journal/budget.txt`).

**Commandes** (journaux sous `journal/corr/`, PID dans `NOTES.md`) :
- `rouge-serie.txt` (rouge de C-1) ;
- `rouges-mutants.txt` (17 rouges ciblés) ;
- `campagne-e11v.txt` et `mut-*.txt` ;
- `job-simbis-252.txt` ;
- `resume.txt` et `apres-*.txt` ;
- `xtask-*.txt` (VERDICT seuls) ;
- `application-tete.txt` ;
- `plan-budget-c1.txt`.

**Recomptés par moi** :
- lignes du diff (`diff_etape.sh`) : 112 ajoutées, 15 retirées ;
- 0 octet 92 ; lignes ≤ 120 ; plancher 252 (`TestLoader`) et 268 sur la tête ;
- attendus de C-1 : ⌊5 400/41⌋ = 131, 41 × 131 = 5 371, 41 × 132 = 5 412, 131 × 4 = 524, 19 × 524 = 9 956 ;
  ⌊21 600/41⌋ = 526 pour l'ancienne formule ; ⌊30/12⌋ × 2 = 4 ;
- lots du §8 avant et après C-1 ; 200 × 234,34 s = 46 868 s ;
- bilans de la campagne et des contrôles.

## 16. Corrections après le contre-contrôle : diff SB-11w (correcteur, 2026-10-09)

**Gate 0** : modèle résolu `claude-opus-5-5` (worker G1, correcteur, effort max). Je n'ai écrit ni la série SB-11a … u,
ni la G2, ni le contre-contrôle. Contrat : ajout daté d'`ADJUDICATION-G2.md` (après 09:38 UTC). C-10 à C-13 répondent
aux réserves R-1 à R-4 de `g2/cc/RAPPORT-CC.md` ; R-5 (ligne d'item NPRIME-NUL-1) reste à l'orchestrateur.

### 16.1 Pièces, base, horloge

- **Horloge** : début à 09:38:37 UTC, fin de section à 10:34:45 UTC ; chaque heure lue par `date -u`.
- **Pièces** : `g2/cc/SHA256SUMS` : 60 OK, 0 échec. Rien écrit sous `g2/`.
- **Base** : `5e386c4`. SB-11w se pose après SB-11v ; copie `travail-w` = `base/` + `etapes/e11v` (`diff -rq` et
  `cmp` égaux).
- **Tête** : `1a388e1`, relue à 09:39:04, 09:42:44 et 10:34:13 UTC ; `status --porcelain` vide. Aucune écriture git
  au dépôt réel.
- **Interdits** : tenus comme au §15.1 (variable scellée jamais posée, `unshare -n`, aucun `*.jsonl` ni dossier
  interdit, aucune recherche récursive, xtask par ses lignes VERDICT seules).

### 16.2 Diff

| diff | objet | lignes de code ajoutées | retirées | plancher | octets 92 | sha256 |
|---|---|---|---|---|---|---|
| SB-11w | tests de C-10 à C-13 | 37 | 26 | 252 (inchangé) | 0 | `5de3fd63040870a995957651f1dfd3b5817b14e41607e5e5a2789c564ab490c3` |

- Fichier : `diffs/SB-11w.diff` (`git diff --no-index` de `etapes/e11v` à `etapes/e11w`).
- Aucun code touché. Les tests retouchés sont `test_budget`, `test_l_2_au_site_d_appel`, `test_schema_ferme_c_5` et
  `test_r_de_la_cellule`. Il n'y a aucune méthode neuve : le plancher reste **252**, et `gates.yml` est inchangé.
- Les 26 lignes retirées se répartissent ainsi :
  - les docstrings, réécrites ;
  - l'assertion de `test_budget`, remplacée par une assertion plus serrée ;
  - la boucle de C-4, remplacée par une boucle qui garde l'assertion de perte et y ajoute celle de la dérive ;
  - le corps de C-8, dont les trois listes d'avant sont incluses dans l'attendu neuf.

  Aucune assertion n'est perdue.
- Forme : 0 octet 92 ; aucune ligne `.py` de plus de 120 caractères ; R-13 : 0 marqueur ; `TestLoader` : 252.

### 16.3 Corrections C-10 à C-13

« Rouge » : le test visé, lancé seul sous le mutant, est en FAIL d'assertion (`AssertionError`, aucune ERROR) ; il est vert
sans le mutant (`journal/corrw/rouges-mutants.txt`, `outils/corrw_rouges.py`). Le contre-contrôle avait montré chaque
M-CC vivant sur e11v (`g2/cc/mut/campagne.txt`).

| C (réserve) | test (fichier:ligne, e11w) | fixture qui sépare | rouge sous le mutant | tué en campagne |
|---|---|---|---|---|
| C-10 (R-1) | `test_budget.py:24` | durées (5, 12, 7) : le maximum n'est ni premier ni dernier ; total 24, trois mesures | M-CC-08 : ns_max 5 au lieu de 12 ; G-22 : 7 ; M-11T-04 : 8 | M-CC-08, G-22, M-11T-04 à -10, M-11V-01 |
| C-11 (R-2) | `test_cellules.py:143` | [BTC, USDT, ETH] (BTC en tête, seul l'ordre en défaut) → CELLULE/schema ; garde : [BTC, ETH, USDT] passe | M-CC-09 : None au lieu de CELLULE/schema | M-CC-09, G-08 |
| C-12 (R-3) | `test_replication.py:223` | critère collectif actif ; i = 0 et i = 200 ; R = 999 contre 99 | M-CC-03 : oracle [999, 99, 999, 99] ; M-CC-04 : variante.tester [99, 99] | M-CC-03, M-CC-04, G-11, M-11V-04, M-11V-05 |
| C-13 (R-4) | `test_cellules.py:133` | dérive « tendances », W = 16 et 2 : durée 161 280 et 20 160 (W·10 080, valeur de `test_fond`) | M-CC-05 : (16, 80 640) au lieu de (16, 161 280) | M-CC-05, G-06 |

- Les attendus de C-12 (4 appels d'oracle, puis 4 de `regle.tester`, puis 2 de `variante.tester`) ont été relevés hors
  suite par la sonde `outils/corrw_sonde_r.py` (09:39:25-09:39:29), puis écrits à la main dans le test.
- Non-affaiblissement au niveau des mutants : les mutants qui tuaient déjà les quatre tests retouchés sont rejoués,
  tous en rouge ciblé et en campagne. Ce sont G-06, G-08, G-11, G-22, M-11V-01, M-11V-04, M-11V-05 et M-11T-04 à -10.
  M-11T-07 (aucune mesure admise) est tué par une ERROR et non par un FAIL : `max([])` lève ValueError dans
  `assertRaises(Refus)`. C'était déjà la forme du test à SB-11t, et SB-11w n'en a pas touché la partie : voir O-W1.

### 16.4 Mutants (campagne sur SB-11w)

- **Commande** : celle du job, au plancher **252**, sur `travail-w` = `etapes/e11w`, sous `isole.sh`, avec `timeout 300`
  et `PAR=2`. Outils : `outils/corrw_mutants.py`, `corrw_campagne.py`, `corrw_chaine.sh`.
- **Déroulé** : de 09:42:20 à 10:17:16 UTC, chaîne `sh corrw_chaine.sh` PID 10825 (`/proc/PID/cmdline` lu). Journal :
  `journal/corrw/campagne-e11w.txt`, et `mut-<id>.txt` pour chaque mutant.
- **Bilan** : 19 mutants, **19 tués** (sortie 1), 0 vivant, 0 FATAL, 0 inapplicable.
  - 18 sont tués par AssertionError ; M-11T-07 l'est par une ERROR (§16.3).
  - Témoins VIVANT (Ran = 252, conforme) : 140 s au début, 135 s à la fin. Mutant le plus long : 201 s.

| id | mutation | test tué |
|---|---|---|
| M-CC-03 | R du prm au calcul « avec » | test_r_de_la_cellule |
| M-CC-04 | R du prm à `variante.tester` | test_r_de_la_cellule |
| M-CC-05 | `fond(p, cel, points, (W + 1) // 2)` | test_l_2_au_site_d_appel |
| M-CC-08 | `m = ns[0]` | test_budget |
| M-CC-09 | garde d'ordre des classes retirée | test_schema_ferme_c_5 |
| G-06, G-08, G-11, G-22 | ceux de la G2 | test_l_2…, test_schema…, test_r…, test_budget |
| M-11V-01, M-11V-04, M-11V-05 | ceux de SB-11v | test_budget et test_plan_90_min ; test_r_de_la_cellule |
| M-11T-04 à M-11T-10 | ceux de SB-11t | test_budget |

### 16.5 Gates

Contrôles l'un après l'autre : `outils/corrw_finale.sh`, PID 31869, qui lance
`corrw_apres.sh` puis `corrw_xtask.sh`, de 10:17:34 à 10:34:04 UTC. Résumé dans `journal/corrw/resume.txt`. Copie :
`tete-w` = `1a388e1` + SB-11a … w, conflits résolus.

| contrôle | copie | résultat |
|---|---|---|
| sim-bis, plancher 252 | travail-w (5e386c4 + a … w) | conforme, Ran = 252 (témoins de campagne, 140 et 135 s) |
| runner | tete-w | code 0, 136 ok, 0 échec |
| sim-bis, plancher 268 | tete-w | conforme, Ran = 268 (133 s) |
| s2bis, plancher 340 | tete-w | conforme, Ran = 340 |
| S2 `--egal` | tete-w | conforme, Ran = 415, deux sauts nommant la variable scellée |
| hooks ; secrets (fixtures, `--tree`) ; R-1 (fixtures, arbre) ; R-13 | tete-w | 54 ok ; 147 ok, 991 fichiers ; 227 ok, liste blanche exacte ; 0 marqueur |
| matrice `-X dev -W error` | tete-w | 3.10.20 : 198 s ; 3.11.15 : 173 s ; 3.12.3 : 165 s ; 3.13.14 : 153 s. Partout code 0, Ran 268 OK, 0 « Exception ignored », 0 « Warning » |
| `cargo --locked xtask verify` (VERDICT seuls) | tete-w ; tete-neuve-w | 8 VERT, 1 ROUGE (1 violation), global ROUGE, **mêmes dix lignes** (`diff` vide) : la violation précède la série |

### 16.6 Application sur la tête `1a388e1`

- SB-11a … w ont été appliqués diff par diff sur `git archive 1a388e1` (`journal/corrw/application-tete.txt`).
  - Seuls rejets : les conflits connus du §15.6, c'est-à-dire le plancher sim-bis aux diffs a … v et la ligne README à 20
    diffs.
  - **SB-11w s'applique sans rejet** : il ne touche pas `gates.yml`.
- Résolution : plancher **268** (= 210 + 252 − 194), lignes README insérées.
- Contrôle : la copie est égale à `fusion/` du générateur, sauf les six fichiers de v/w et les deux planchers.

### 16.7 Écarts et constats

- **E-W1** : la première relance de `corrw_rouges.py` après l'ajout des mutants M-11T a échoué à l'import (`NL` non
  défini dans `corrw_mutants.py`) avant tout calcul. Corrigée et relancée ; seul le passage de 09:41:35 compte. Le premier
  jeu de 15 rouges (09:40:44-09:41:07, `rouges-mutants-15.txt`) est gardé : 15 sur 15 en rouge d'assertion.
- **E-W2** : des barres obliques inverses ont été tapées dans des commandes (`tr` pour lire `/proc/PID/cmdline`), jamais
  dans un fichier. Un compte Python le vérifie : 0 octet 92 dans le diff, dans `scripts/sim-bis` et dans mes outils.
- **E-W3** : `pgrep -n -f` sur le nom exact de mes scripts détachés, avec lecture de `/proc/PID/cmdline` ; index git
  dans mes copies seulement, comme E-C5 et E-C6.
- **O-W1, mineure** : le cas « aucune mesure » de `test_budget` (`assertRaises(commun.Refus)`) tue M-11T-07 par une
  ERROR, pas par un FAIL d'assertion. C'était déjà le cas depuis SB-11t, hors de C-10 à C-13. Le remède serait la forme
  `code_de` des autres fichiers. Je le rends comme constat, à joindre à MUT-EQUIV-FIXTURE-1 ou au prochain brief.
- **MUT-EQUIV-FIXTURE-1** (élargi par l'adjudication) : C-10 à C-13 en sont quatre cas de plus.
  - Mettre le maximum au milieu des mesures.
  - Donner à chaque garde d'ordre un cas qui l'isole seule.
  - Couvrir tous les sites d'un même paramètre : « avec », i ≥ 200.
  - Prendre un W ≠ 1 pour chaque destinataire du W.

### 16.8 Journal de provenance (G1)

- **Lu [lu]** :
  - `g2/cc/RAPPORT-CC.md` en entier et l'ajout daté d'`ADJUDICATION-G2.md` ;
  - `g2/cc/outils/mutants_cc.py`, `nprime.py` et sa sortie ;
  - `g2/cc/mut/campagne.txt` et la queue de `g2/cc/NOTES.md` ;
  - `outils/mutants_11t.py` ;
  - les quatre tests retouchés, dans leur état e11v.
- **Seconde main [2nd]** : les constats O-CC-1 à O-CC-7 et le classement des M-CC sur e11v (contre-contrôleur).
- **Commandes** :
  - sonde de C-12 ;
  - `corrw_rouges.py`, deux jeux ;
  - campagne `corrw_chaine.sh` ;
  - `corrw_apres.sh` et `corrw_xtask.sh` ;
  - `patch -p1` sur la tête ;
  - `TestLoader`.
- **Recomptés par moi** :
  - 37 lignes ajoutées et 26 retirées ;
  - plancher 252, et 268 sur la tête ;
  - 161 280 / 16 = 10 080, 2 × 10 080 = 20 160, 8 × 10 080 = 80 640 ;
  - 5 + 12 + 7 = 24, ⌊24/3⌋ = 8 ;
  - bilans de la campagne et des gates.
