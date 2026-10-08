# Premier contre-contrôle de SIM-INTEG (NON-CONFORME, CC-1 et CC-2) (transcrit)

> Transcription par l'orchestrateur le 2026-10-08 20:46:23 UTC du texte écrit par l'agent a059fa5f14a203e0a dans `<scratchpad>/s2bis/sim5/g2/cc/RAPPORT-CC.md` (sha256 e4e2a04b…) ; contrôle FM-1.1 de son transcript : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte de l'agent ci-dessous, sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Contre-contrôle de SIM-INTEG : corrections C-1 à C-4 et relecture G2 du diff neuf SB-15G

**Gate 0 : modèle `claude-opus-5-5`** (réviseur de la G2 de ce lot, effort max ; je n'ai écrit aucune correction ni
aucun diff). Contre-contrôle du 2026-10-08, de 19:11:09 à 19:34 UTC (`date -u`).

## Verdict : NON-CONFORME (liste fermée CC-1, CC-2)

Ce qui est adjugé tient :
- C-1 à C-4 sont corrigées telles que je les ai écrites, sans aucune ligne de code de production changée de A à F ;
- la ligne 9 du README est coupée ;
- Q-SI-9 : les égalités n et K tiennent par construction, ce que j'ai vérifié dans le code de PLAN-S2BIS-2. Le refus
  `CALIB/croisement` est nommé, et ma sonde d'accord donne 600 accords sur 600 ;
- mes six survivants sont tués ; le plancher est exact à 194 ; la matrice, les portes et la forme sont vertes.

Deux survivants non équivalents restent pourtant, à corriger par des **tests seulement** :
- **CC-1** sur SB-15G : rien ne fige que le contrôle croisé ne peut pas être sauté ;
- **CC-2** : je retire mon avis d'équivalence de MR-18 au sens strict.

Aucune valeur et aucune ligne de production ne changent. Mes tests de faisabilité tuent les deux mutants
(`cc/outils/test_cc.py`, Ran 196).

## 1. Liste fermée

**CC-1 : le caractère « non contournable » du contrôle croisé n'est figé par aucun test** (SB-15G, Q-SI-9).
- **Où :** `scripts/sim-bis/calibration.py:183-189` (`charger_unites(prm, presentes, ep, lus=None, environ=None)` puis
  `croiser_unites`, l.188) ; `tests/test_calibration.py:194` (`test_croisement_q_si_9`).
- **Preuve :** MG-14 donne à `presentes` et `ep` la valeur par défaut `None` et saute le contrôle s'ils manquent. Il sort
  en 0 sous la commande du job (plancher 194) : il est VIVANT (`cc/journal/mg_e15g.txt`). C'est pourtant sur cette
  propriété que l'adjudication ferme Q-SI-9 (« la signature change, le contrôle ne peut pas être sauté »). Le code actuel
  la tient : un appel sans ces deux arguments lève `TypeError`, ce que mon test vérifie, vert sur l'état final.
- **Remède :** dans `test_croisement_q_si_9`, affirmer que `charger_unites(PRM, environ={})` lève `TypeError` (ou que
  `presentes` et `ep` n'ont pas de valeur par défaut). Le plancher ne change pas si le cas est ajouté au test existant.

**CC-2 : la règle « FIV « - » si et seulement si γ̂₀ = 0 » n'est pas figée** (SB-15D, mon avis MR-18 révisé).
- **Où :** le code, `calibration.py:73` (`_point`, l.67) ; le test, `tests/test_calibration.py:167` (`test_fiv_unites_indefini`).
  Sa docstring annonce « « - » à K = 3 (γ̂₀ ≠ 0) : CALIB/coherence », mais la fixture `indefinie(1, k="3")` (l.27) écrit
  γ̂₀ = 0. Le refus vient donc du contrôle de γ̂₀, pas de la règle du « - ».
- **Preuve :** prenons une ligne fabriquée de forme valide : FIV « - », σ̂²_bloc = 0, n = 24 585, K = 372, γ̂₀ et cv
  cohérents.
  - L'original la refuse : `CALIB/coherence`.
  - MR-18 la lit comme un F_u indéfini (`cc/journal/mr18_distingue.out`, recopié au §4), et il survit sur l'état final
    (`cc/journal/mr_e15g.txt`).
  - MR-18 reste sans effet sur toute sortie possible du producteur : σ̂²_bloc > 0 dès que 0 < K < n, et le fichier
    épinglé n'a aucune ligne « - ». Mais le lecteur a pour rôle de refuser les lignes incohérentes, ce que la double
    épingle ne remplace pas dans les tests. Mon avis « équivalent » de la G2 était donc trop large.
- **Remède :** ajouter ce cas à `test_fiv_unites_indefini`, refus attendu `CALIB/coherence` ; plancher inchangé.

**Faisabilité, non versée :** les deux tests de `cc/outils/test_cc.py`, ajoutés à une copie de l'état final, donnent une
suite de 196 tests, conforme, témoins verts au début et à la fin. MG-14 et MR-18 y sont TUÉS (`cc/journal/remede_cc.txt`).

## 2. Contrôles demandés

| contrôle | résultat |
|---|---|
| SHA256SUMS de sim5 | ec194dd5… = le message ; 609 lignes ; `sha256sum -c` 609 OK ; aucun `jsonl` ; mon `g2/SHA256SUMS` 0 non-OK (mes fichiers intacts) |
| diffs | A 483b6963…, B 15209f3e…, C 652a5c8f…, D 35eeb496…, E e59aeb80…, F 89b8ae90…, G 563ba755… ; `avant-g2/` = les diffs de ma G2 |
| série sur b46672b | `git apply --check` puis `git apply` 7/7 ; instantanés égaux aux `etapes/e15a…e15g` du générateur |
| série sur 5cfe746 (HEAD) | 7/7 ; `scripts/sim-bis`, `gates.yml`, `scripts/plan-s2bis(-2)` et `docs/adr-0029/plan-s2bis(-2)` inchangés entre b46672b et 5cfe746 ; état final identique sur les deux bases |
| production A à F | ancienne série contre nouvelle, étape par étape : 0 fichier de production différent ; seuls changent le README (A à F) et `tests/test_calib_fiv.py` (E, F) |
| C-1 | `test_c1_egalites_grille_scellee` : grille scellée de 64 points, trois paires (κ, puis τ_D, puis φ) |
| C-2 | `test_q1_dernier_hote_du_format` (okx, puis le premier hôte ; Q₁ = 16·(ln 2)²) et `test_bord_derniers_hotes_du_format` |
| C-3 | `test_bord_selection_grille_scellee` : C1 = (1/50, 10, 240), C2 = (1/10, 5, 60), 6 hôtes, au bord |
| C-4 | docstring de `test_bord_sans_vacuite` : Q-SI-1 pour la vacuité, Q-SI-2 pour l'hôte indéfini |
| README l.9 | 114 + 45 caractères |
| survivants de la G2 | MR-03, -04, -05, -06 TUÉS à e15e (plancher 185) ; MR-10, -26 TUÉS à e15f (193) ; les six TUÉS à e15g (194) |
| mes 26 mutants à e15g | 25 TUÉS, 1 VIVANT (MR-18), 0 FATAL ; témoins verts |
| rouges rejoués (ébauches du générateur) | E : 6 FAIL / 0 ERROR (185) ; F : 7 FAIL / 0 ERROR (193) ; G : 1 FAIL / 0 ERROR (194) |
| jobs à chaque étape (`isole.sh`) | 174, 177, 179, 181, 185, 193, 194 : tous conformes ; le témoin `--egal` à 193 sur l'état final est refusé (Ran 194 > 193) |
| matrice stricte | 3.10.20, 3.11.15, 3.12.3, 3.13.14 × `PYTHONHASHSEED` 2 et 977 : 8/8, Ran 194, OK, 0 « Exception ignored », 0 « Warning » |
| forme | code ajouté : A 66, B 152, C 68, D 144, E 187, F 149, G 59 (au plus 200) ; 0 octet 92 ; R-13 0 ; imports du lot ou de la bibliothèque standard (R-8) ; Python : 0 ligne de plus de 120 caractères |

**Portes :**

| porte | état final, série sur b46672b | état final, série sur 5cfe746 |
|---|---|---|
| runner | 97 ok | 136 ok |
| sim-bis | 194 conforme | 194 conforme |
| s2bis | 255 conforme | 255 conforme |
| s2-harness | 407 conforme | 415 conforme |
| hooks / model-pinning / lint R-1 / secrets | 54 / 95 / OK / 147 | non relancé |
| R-13 (motif lu dans `gates.yml`) | 0 constat | non relancé |
| `gate-secrets --tree` | OK (26 fichiers) | non relancé |
| `cargo --locked xtask verify` (`unshare -n`) | verdicts égaux à ceux de la base : S-G1 à S-G8, fmt, no_std et clippy VERT ; S-G9 ROUGE, 1 violation (`docs/17-modele-de-menace.md:70`, connue) ; section S-G9 identique | non relancé |

## 3. Relecture G2 de SB-15G (à 100 %)

- **Contenu :**
  - `croiser_unites(unites, presentes, ep)`, `calibration.py:167-180` (refus l.179) : pour chaque strate, chaque hôte et chaque ligne,
    (n, n, K) = (positions présentes du masque, n_s d'EP, cellules « ecart » d'EP) ;
  - une strate absente ou un hôte absent donnent `CALIB/croisement`, jamais `KeyError` ni `AttributeError` (MG-01 et
    MG-02 tués) ;
  - `charger_unites` analyse, puis croise ;
  - `test_croisement_q_si_9`, 7 retouches ;
  - plancher 194.
- **Égalités par construction**, vérifiées contre le code et le contrat de PLAN-S2BIS-2 :
  - `classer` (`scripts/plan-s2bis/commun.py` l.113-123) range chaque fenêtre de `d["ws"]` sous sa strate journalisée ;
  - D_u est construite sur ce rangement (`masque_fiv.py` l.99), donc n(D_u) est le nombre de fenêtres retenues de la
    strate ;
  - le masque compte les mêmes fenêtres de `d["ws"]` par strate du calendrier (l.25-35) ;
  - `controle_b` exige, fenêtre par fenêtre, que la strate journalisée soit celle du calendrier, et que les retenues
    égalent le n du bloc 3 (l.37-52). Les deux comptes coïncident donc strate par strate ;
  - le contrôle (f), P-5, exige par hôte le préfixe d'EP « ecart : n_s = len(s) ; cellules = K », sinon `P2/ep`
    (l.101-103) ;
  - côté SIM-BIS, `masque_j28` réécrit la section et en contrôle les comptes et l'empreinte. Le nombre de présentes est
    donc le compte du producteur.

  La démonstration du générateur est exacte. Q-SI-9 se ferme dans ce lot comme l'a adjugé l'orchestrateur, sous réserve
  de CC-1.
- **Refus nommé :** oui. Seize mutants : quinze tués, dont strate absente, hôte absent, masque non comparé, K non comparé,
  n_s non comparé, `any` remplacé par `all`, première ligne seule, dernier hôte, dernière strate, panne au lieu d'écart,
  ℓ = 1 440 non contrôlé, `charger_unites` sans le contrôle, code de refus changé. Seul MG-14 vit (CC-1).
- **Contournement :** il est impossible par `charger_unites`, dont les arguments sont obligatoires (vérifié). Il reste
  possible en appelant `analyser_unites` directement, qui est l'analyseur public : la ligne (b) de Q-SI-8 au brief de
  SB-11 doit nommer `charger_unites(prm, cal["presentes"], ep)`, ce que propose le générateur.
- **Sonde d'accord** (`cc/outils/sonde_croisement.py`) : n et K lus par mon analyseur, comptes du masque par mon oracle,
  n_s et cellules d'EP par mon découpage.
  - Les représentations sont égales à celles du lot.
  - Sur les données versées : 20 couples (strate, hôte), 340/340 lignes égales ; ma décision et celle du lot acceptent
    toutes deux.
  - Sur 600 perturbations (n, K, comptes du masque, n_s, cellules, strate ou hôte absents, déplacements cohérents) :
    600 accords, 128 acceptées et 472 refusées par les deux.

## 4. Avis sur MR-18 (question de l'orchestrateur)

**Je ne maintiens pas mon avis d'équivalence au sens strict.**
- MR-18 est équivalent sur toute ligne que le producteur peut écrire. J'ai vérifié l'identité : numérateur =
  n²·Σ (sommes glissantes des écarts)², d'où σ̂²_bloc > 0 dès que 0 < K < n, sur 819 cas en G2.
- Il est sans effet sur le fichier épinglé, qui n'a aucune ligne « - ».
- Mais une ligne fabriquée, de forme valide, le distingue. Sortie de `cc/outils/mr18_distingue.py` :
  - FIV « - », σ̂²_bloc = 0, n = 24 585, K = 372 : original `CALIB/coherence`, MR-18 « lu, fiv None » ;
  - K = 0 ou K = n : les deux lisent un FIV indéfini.
- J'en fais CC-2.

## 5. Observations, sans correction

- **O-1.** Dans mon dossier `g2/`, le fichier `G2-SIM-INTEG-transcrit.md` (8ded2580…) est la transcription de mon rapport
  par l'orchestrateur ; il n'est pas de ma main. Mon `g2/SHA256SUMS` ne le couvre pas.
- **O-2.** E-12 du générateur : il a lu et exécuté mon `g2/outils/mutants_g2.py`, empreinte 6903583c…, égale à celle de
  ce fichier. Les tests des corrections sont de sa main : leurs noms, fixtures et valeurs diffèrent de ceux de mon
  `test_revue_g2.py`.
- **O-3.** La section S-G9 de xtask nomme aussi un chemin sous `docs/rapports/`. Je n'en ai vu que le chemin : le fichier
  est absent de la copie et n'a pas été ouvert. C'est le même constat qu'en G2.

## 6. Avis sur les items, et items à former

- **Q-SI-8 :** la ligne (b) devient `calibration.charger_unites(prm, cal["presentes"], ep)`. Le test de câblage de SB-11
  doit tuer le mutant « `analyser_unites` au lieu de `charger_unites` ». À verser à SHOGEN-SIM-BIS-SB11-BRIEF-1 avec la
  ligne (e).
- **I-CC-1 :** aucun item neuf si CC-1 et CC-2 sont faits ; sinon, les deux cas de test à porter à SB-11.

## 7. Écarts

- **E-CC1 :** une suppression récursive écrite avec des variables non gardées a été refusée par le contrôle de sûreté du
  harnais. Rien n'a été supprimé ; elle a été réécrite avec des chemins gardés (`"${T:?}"`).
- **E-CC2 :** pour l'adaptateur `oracle_r1`, un clone nu en lecture seule (`git clone --bare --no-hardlinks`) a été fait
  dans `cc/tmp`, puis supprimé. Aucune écriture git dans `/home/user/shogen` (`git status` vide, HEAD 5cfe746).
- **E-CC3 :** mes outils `jobs_cc.sh` (1 octet 92, la séquence de saut de ligne du `printf` qui écrit le fichier `gitdir`) et les outils de la G2 qu'ils
  réemploient portent des octets 92 voulus. Ce rapport et NOTES en ont 0.
- **Interdits :** aucun journal, aucun `*.jsonl`, aucune pièce de D.2. `SHOGEN_S2_CAMPAGNE_CONTROL` n'a jamais été
  posée. Aucune énumération récursive de `docs/`, du dépôt ou du scratchpad. Les copies lourdes sont supprimées.

## 8. Journal de provenance (G1)

**[lu] :** §12 de `RAPPORT-GENERATEUR.md` (l.202-297) ; les 7 diffs, dont SB-15G en entier ; `masque_fiv.py` l.25-60 et
95-140 ; `plan-s2bis/commun.py` l.105-123 ; les ébauches E, F et G du générateur.

**Commandes et sorties**, dans `cc/journal/` :
- `sonde_croisement.out`, `mg_e15g.txt`, `mr_e15g.txt`, `mr_e15e.txt`, `mr_e15f.txt`, `remede_cc.txt` ;
- `rouge_cc.out`, `jobs_cc.out`, `strict_cc.out`, `portes_cc.txt`, `xtask-verdicts-*.txt`.

Les tâches longues ont été lancées détachées (`setsid nohup`), leur fin constatée.
