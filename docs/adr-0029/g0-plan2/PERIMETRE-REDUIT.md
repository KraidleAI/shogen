# PLAN-S2BIS-2 — périmètre réduit : sous-lots, tests et mutants, exigences, refus, lettre de Q-P2-08, items (sans code)

- **Statut** : pièce finale demandée par l'orchestrateur (message de 14:11 UTC, pièce 2) ; sans code ; matière du G0 du lot. Rien n'est décidé ici : l'adjudication revient à l'orchestrateur.
- **Gate 0** : `claude-opus-5-5`, effort max (worker, CLAUDE.md §7).
- **Date** : 2026-10-05, 14:46:51 UTC (`date -u`).
- **Base** : HEAD `4df58862fb77fff792a321515b938c9a34791b9c` à l'écriture. La base a avancé pendant la passe (commits COLLECTE-BIS de l'orchestrateur, de `5f99ab5` à `4df5886`) ; les pièces citées ici n'ont pas changé (`git diff --quiet 5f99ab5 HEAD`, code 0, §10).
- **Sources** : `AVIS-PLAN2.md` (`33ac8d31…`, « AV l.n »), adopté tel qu'écrit, §4.2 et §4.3 (AV l.134-158) ; `PROPOSITION-PLAN2.md`, version remise et lue par l'avis (`4b3107a7…`, « PP l.n ») ; `LETTRE-AJOUT-G0-SIM.md` (`01ce4551…`) ; code de PLAN-S2BIS au dépôt (« PS2 <fichier> l.n ») ; EP = `docs/adr-0029/plan-s2bis/episodes.txt` (`c0371ca5…`, « EP l.n »).
- **Conventions** : [lu] lu dans la pièce ; [calc] calcul du rédacteur ; [mesuré] commande lancée (§10) ; [inféré] estimation ou déduction.
- **Écarts à l'avis, signalés** : six sous-lots au lieu de cinq (AV l.156), et ≈ 980 lignes au lieu de ≈ 750 à 900 (§1) ; neuf précisions de lettre, lues dans le code de PLAN-S2BIS (§9), dont deux complètent la lettre de l'avis (P-3, P-6).

## 0. En bref

1. **Un seul estimateur** : `r1.block_long_run_variance` du harnais extrait de `f35a70c`, appelé par `episodes.courbe` épinglé (PS2 episodes.py l.59-70). Le lot n'écrit aucune formule de FIV, d'épisode, de pause, de quantile ni d'histogramme : il appelle `episodes.episodes`, `episodes.resume` et `regles.quantile` (par `resume`, PS2 episodes.py l.48), et ses tests appellent `tests/fixtures.py` de PLAN-S2BIS (AV l.29, l.132, l.144).
2. **Deux scripts** : `masque_fiv.py` écrit `masque_j28.txt` et `fiv_unites.txt` (AV l.150) ; `intervalles.py` écrit `intervalles.txt`. Contrôles (a) à (f) ; (g) disparaît (AV l.142).
3. **Six sous-lots**, chacun ≤ 200 lignes [inféré], tests et données compris : `masque_fiv.py` reste un seul script, mais avec ses tests il passe 200 lignes (≈ 130 de code, ≈ 125 de tests) ; il s'écrit en deux diffs. Le lanceur aussi, pour la même raison.
4. **Taille ≈ 980 lignes** [inféré] : le code (≈ 435) tient dans les chiffres de l'avis ; l'écart est dans les tests (≈ 500 contre ≈ 300). Ratio mesuré à PLAN-S2BIS : 813 lignes de tests pour 661 de code [mesuré].
5. **Exigences** : sur E-P2-01 à E-P2-29, 15 restent, 3 sont précisées, 10 modifiées, 1 tombe (E-P2-29). Deux refus tombent (P2/r1, P2/entree). Tests : cinq retirés (T-P2-FIV-1 à 4, T-P2-ORA-1), huit neufs. Mutants : cinq retirés, neuf neufs.
6. **Lettre de Q-P2-08** : celle de l'avis, citée mot pour mot au §7, avec sa mise en œuvre au lanceur.
7. **Items** : deux neufs (SHOGEN-PLAN-S2BIS-CI-1 ; SHOGEN-PLAN-S2BIS-EXCLUSIONS-1, constat de ce jour), un retiré (ORACLE-CALIB-1), neuf précisés (§8).

## 1. Fichiers, tailles, ordre

**Code** sous `scripts/plan-s2bis-2/` (E-P2-01 réécrite) : `README.md`, `parametres.json`, `socle.py`, `masque_fiv.py`, `intervalles.py`, `lancer.sh`, `SHA256SUMS`, `tests/__init__.py`, `tests/test_socle.py`, `tests/test_masque_fiv.py`, `tests/test_intervalles.py`, `tests/test_lancer.py`, `tests/test_identite.py`. Bibliothèque standard seule. Aucun module du lot ne s'appelle `commun`, `regles`, `episodes` ni `fixtures` (P-1).

**Sorties** sous `docs/adr-0029/plan-s2bis-2/` (versement, E-P2-24) : `masque_j28.txt`, `fiv_unites.txt`, `intervalles.txt`, `SHA256SUMS`, `README.md`, G1, G2.

**Réemplois par chemin, jamais modifiés**, sous huit épingles du `parametres.json` du lot :

| pièce de PLAN-S2BIS | sha256 [mesuré] | usage |
|---|---|---|
| `scripts/plan-s2bis/commun.py` | `14920e87…` | harnais, lecture, pools, classement, bloc 3, `dec` |
| `scripts/plan-s2bis/episodes.py` | `90c7842d…` | `episodes`, `resume`, `courbe` |
| `scripts/plan-s2bis/regles.py` | `a0140188…` | `quantile`, appelé par `resume` |
| `scripts/plan-s2bis/parametres.json` | `7e214864…` | sous-arbres lus (P-3) |
| `scripts/plan-s2bis/tests/fixtures.py` | `17ae3c13…` | journaux, paramètres et rendu de fixture (tests seuls) |
| `scripts/plan-s2bis/SHA256SUMS` | `65c26310…` | source des cinq épingles ci-dessus |
| `docs/adr-0029/plan-s2bis/episodes.txt` (EP) | `c0371ca5…` | contrôles (c), (e), (f) |
| `docs/adr-0029/plan-s2bis/SHA256SUMS` | `f21f9293…` | source de l'épingle d'EP |

| sous-lot | objet | code et données | tests | autres | total [inféré] | dépend de |
|---|---|---|---|---|---|---|
| P2R-0 | socle I : épingles, variable, schéma, contrôles (c) et (d) | ≈ 85 | ≈ 75 | — | ≈ 160 | — |
| P2R-1 | socle II et `masque_fiv.py` I : CLI, en-tête, contrôle (a), masque | ≈ 100 | ≈ 80 | — | ≈ 180 | P2R-0 |
| P2R-2 | `masque_fiv.py` II : D_u, FIV_u, contrôle (f), sensibilité | ≈ 65 | ≈ 75 | — | ≈ 140 | P2R-1 |
| P2R-3 | `intervalles.py` : épisodes, pauses, contrôle (e) | ≈ 65 | ≈ 75 | — | ≈ 140 | P2R-1 |
| P2R-4 | `lancer.sh` I : contrôles avant tout lancement | ≈ 70 | ≈ 105 | — | ≈ 175 | P2R-0 |
| P2R-5 | `lancer.sh` II, identité, README | ≈ 50 | ≈ 90 | README ≈ 30 ; `SHA256SUMS` 12 | ≈ 185 | P2R-2, P2R-3, P2R-4 |
| total | | ≈ 435 | ≈ 500 | ≈ 42 | ≈ 980 | |

- Code contre l'avis (AV l.156) : socle ≈ 90 (avis ≈ 100) ; `masque_fiv.py` ≈ 130 (≈ 150) ; `intervalles.py` ≈ 65 (≈ 80) ; `lancer.sh` ≈ 120 (≈ 120) ; `parametres.json` et README ≈ 60 (≈ 60). Tests ≈ 500 (≈ 300) : le lanceur seul en demande ≈ 165, comme à PLAN-S2BIS (PS2 tests/test_lancer.py : 158 lignes pour 82 de lanceur [mesuré]).
- **Règle de coupe** : un diff qui passe 200 lignes à l'écriture se coupe à la frontière d'une fonction, chaque moitié avec ses tests, et la coupe est déclarée au G1 ; aucun test ne quitte le diff de son code.
- **Après P2R-5** : G2 neuve à 100 % du lot (réviseur ≠ générateur), dont le passage du propre estimateur du réviseur (celui de la tranche 4) sur les séries du lot (AV l.76, l.158) ; corrections ; répétition à l'échelle (E-P2-20) ; épinglage au JOURNAL, après l'ajout daté et son cp-1 (AV l.66) ; lancement unique ; versement. Ordre impératif : AV l.178.

## 2. Les sous-lots

### P2R-0 — socle I : épingles, variable, schéma, contrôles (c) et (d) (≈ 160 lignes)

- **Contenu**
  - `parametres.json` (≈ 30) : clés exactes, aucun flottant, chaque valeur avec sa source. `plan_s2bis` : chemin et sha256 des huit pièces du §1. `masque` : calendrier hors D5 30 286 et 13 491 ; sautées hors D5 5 701 et 2 094 (ADR-0029 l.31 ; recompte de `calc_p2.py` et test de SB-10B l.148-161). `voisinage` : « sensibilité au voisinage des lacunes », d = 1, bords de la portée comptés comme lacunes, grille `fiv.ell` de PLAN-S2BIS, garde recalculée sur le n réduit (AV l.81), règle de lacune de P-4. `passes` : A, `PYTHONHASHSEED` 0 ; B, 1. `sous_arbres` : ligne de P-3.
  - `socle.py` I (≈ 55) : refus nommé (code, strate, hôte, ℓ ; ni ligne de journal ni valeur, E-P2-12) ; garde de la variable sur un environnement passé en argument ; chargement épinglé (sha256 avant l'import, `__file__` après) de `commun`, `regles`, `episodes`, dans cet ordre et sous ces noms (P-1), puis des autres pièces du §1 ; schéma du `parametres.json` du lot ; contrôle (d) : type « ecart » de PLAN-S2BIS = `r1.ECARTS` ; contrôle (c) : pool D1-bis de chaque strate = les dix flux de `pool_d1bis.unites`, aucun retrait, ligne « pool D1-bis » de l'en-tête = EP l.8, chaîne pour chaîne.
  - `tests/__init__.py` (≈ 15) : chargement épinglé pour les tests ; `tests/fixtures.py` de PLAN-S2BIS par chemin, sous son sha256, sous le nom `fixtures_ps2` ; `PLAN_S2BIS_HARNAIS` exigée (PS2 tests/fixtures.py l.11-13).
  - `tests/test_socle.py` (≈ 60).
- **Tests et mutants**
  - T-P2-SOC-1 épingles : sha256 des huit pièces par `sha256sum`, recopiés dans le test ; chaque épingle de fichier égale à sa ligne dans le `SHA256SUMS` correspondant ; copie altérée d'un octet de chaque pièce : P2/plan-s2bis. Mutant M-P2-01 : contrôle de sha256 retiré.
  - T-P2-SOC-2 variable : environnement passé avec la variable : P2/variable ; sans : aucun refus ; aucun test Python ne pose la variable. M-P2-02 : garde retirée.
  - T-P2-SOC-3 sous-arbres : t0 = 1787770800, n fixe 38 600, D5 [1790273880 ; 1790435280], 10 hôtes, 17 ℓ, recopiés à la main, égaux à ce que lit le socle. M-P2-03 : sous-arbre pris au `parametres.json` du lot.
  - T-P2-SOC-4 écarts (neuf) : paramètres de fixture dont le type « ecart » omet STALENESS : P2/ecarts. M-P2-36 : contrôle (d) retiré.
  - T-P2-SOC-5 schéma (neuf) : clé en trop, clé manquante, flottant : P2/parametres. M-P2-35 : contrôle de schéma retiré.
  - T-P2-POOL-1 pool (neuf) : hôte absent du pool d'une strate ; retrait non vide ; ligne « pool D1-bis » différente de celle d'EP : P2/pool. M-P2-37 : contrôle (c) retiré.
- **E-P2 portées** : 01, 03 (précisée), 04 (épingles), 05 (socle), 07, 11 (c) et (d), 12, 16, 19, 26 à 28.
- **Tombe ici** (P2-0, PP l.387) : la tolérance 10^-45 ; le réemploi de `commun.py` seul.
- **Refus** : P2/variable, P2/plan-s2bis, P2/parametres, P2/ecarts, P2/pool.

### P2R-1 — socle II et `masque_fiv.py` I : CLI, en-tête étendu, contrôle (a), masque (≈ 180 lignes)

- **Contenu**
  - `socle.py` II (≈ 35) : CLI `--journaux`, `--harnais`, `--sortie` (un dossier, P-2), `--parametres`, `--rendu` ; harnais par `commun.importer_harnais` (P2/harnais) ; contrôle (d) dès le harnais chargé ; lecture par `commun.charger`, donc par les seuls lecteurs du harnais extrait (E-P2-02) ; contrôle (a) par `commun.controle`, seul lecteur du rendu J28, qui n'en tire que le bloc 3 (E-P2-04 ; P2/coherence) ; contrôle (c) ; en-tête étendu (E-P2-06) : étiquette mot pour mot, objet, sha256 de chaque module chargé (du lot et de PLAN-S2BIS), des deux `parametres.json` et d'EP, ligne des sous-arbres (P-3), lignes de provenance dans la forme de PS2 commun.py l.184-194, lignes du bloc 3 ; chaque sortie écrite en `.partiel`, puis renommée ; en refus, chaque sortie du script porte l'en-tête et une ligne de refus, code 1 ; sinon 0.
  - `masque_fiv.py` I (≈ 65) : positions j = (ws − t0)/w de la portée (bornes de `commun.charger`) ; strate de chaque position par `window.strate_from_spec` sous le calendrier journalisé ; retenue = fenêtre de `d["ws"]` ; plage D5 = plages exclues ; chaîne c/s/- et son sha256 ; comptes par strate ; lacunes (suites maximales de positions non retenues, D5 comprise, composition par strate) ; contrôle (b) ; `masque_j28.txt` dans la forme de PP l.144-153.
  - `tests/test_masque_fiv.py` I (≈ 50) ; suite de `tests/test_socle.py` (≈ 30).
- **Tests et mutants**
  - T-P2-MAS-1 lacunes (redéfini : fenêtre courte au passage de strate ; la portée réelle est l'objet de MAS-2) : 20 positions de vendredi 23:50 à samedi 00:10 UTC (calme puis stress), une fenêtre absente, une plage exclue de trois positions : lacunes, comptes, chaîne c/s/- écrite à la main, sha256 par `printf`, puis `sha256sum`. M-P2-04 : borne haute de la plage exclue ; M-P2-05 : lacunes contiguës non fusionnées.
  - T-P2-MAS-2 portée réelle : sans journal, depuis les bornes d'EP l.6 et la plage D5 : 46 468 positions ; 32 068 et 14 400 ; 1 782 et 909 ; 30 286 et 13 491 (deux sources : `calc_p2.py` et le test de SB-10B l.148-161). M-P2-06 : jour pris en heure locale ; M-P2-07 : premier jour partiel ignoré.
  - T-P2-MAS-3 fail-closed : retenues différentes du n du bloc 3 dans une fixture : P2/masque, aucune valeur dans les deux sorties. M-P2-08 : contrôle (b) retiré.
  - T-P2-OUT-1 sortie : étiquette mot pour mot ; en-tête : sha256 de `socle.py`, `masque_fiv.py`, `commun.py`, `episodes.py`, `regles.py`, des deux `parametres.json` et d'EP ; ligne des sous-arbres ; trois lignes d'une fixture écrites à la main ; aucun `.partiel` restant. M-P2-19 : un module absent de l'en-tête.
  - T-P2-SOC-6 cohérence et harnais (neuf) : bloc 3 épinglé différent du recompte : P2/coherence ; épingle d'un module du harnais altérée : P2/harnais ; aucune valeur. M-P2-40 : contrôle (a) neutralisé ; M-P2-41 : harnais importé sans `commun.importer_harnais`.
- **E-P2 portées** : 02 (lecture par le harnais extrait), 04 (rendu), 05, 06 (modifiée), 07 (`.partiel`), 08, 11 (a) et (b), 12, 14, 16, 19, 26 à 28.
- **Tombe ici** (P2-0 et P2-1, PP l.387-388) : `masque.py` comme script distinct, avec sa CLI, son en-tête et ses contrôles propres (fusion, AV l.150).
- **Refus** : P2/harnais, P2/coherence, P2/masque.

### P2R-2 — `masque_fiv.py` II : séries D_u, FIV_u, contrôle (f), sensibilité au voisinage (≈ 140 lignes)

- **Contenu**
  - `masque_fiv.py` II (≈ 65) : D_u(t) = 1 si la cellule (t, u) est dans `r1.ECARTS`, par `commun.classer(d, d["pools_bis"])` (l'appel d'EP, PS2 episodes.py l.88), aux fenêtres retenues de la strate, positions réelles, jamais renumérotées ; FIV_u par `episodes.courbe(série, w, fiv.ell)` aux 17 ℓ ; contrôle (f) : (i) n et K de chaque D_u = n_s et cellules « ecart » d'EP l.13-92 (P-5) ; (ii) I_t = 1{Σ_u D_u ≥ 2} recalculée depuis les D_u, `episodes.courbe` aux 17 ℓ, lignes dans la forme de PS2 episodes.py l.118-120 (nom « D1-bis ») = EP l.128-161, chaîne pour chaîne ; `fiv_unites.txt` : 340 lignes (2 × 10 × 17), forme d'EP l.94, le nom du pool remplacé par la strate, le flux et l'hôte, comme aux lignes d'EP l.13 (P-6) ; section `[SENSIBILITÉ VOISINAGE]` : une ligne par strate (positions retirées ; par hôte, cellules d'écart voisines d'une lacune, K − K′ ; AV l.167), puis 340 lignes sur les séries réduites (P-4).
  - `tests/test_masque_fiv.py` II (≈ 75).
- **Tests et mutants**
  - T-P2-FIV-5 contre EP : journaux synthétiques dans la forme de PS2 tests/test_episodes.py l.57-66 (une cellule périmée : l'hôte a compte 5 cellules d'écart et 4 de panne [calc]) ; `episodes.main` épinglé produit dans le test la sortie de forme EP ; (c) et (f) égaux ; un chiffre altéré dans cette sortie : P2/ep. M-P2-13 : contrôle (f) neutralisé ; M-P2-32 : FIV_u sur le type panne (tué par le K de P-5).
  - T-P2-FIV-6 contre `episodes.courbe` (neuf, AV l.144) : lignes de `fiv_unites.txt` d'une fixture égales aux lignes construites dans le test par `episodes.courbe` épinglé sur des séries écrites à la main (positions réelles, fenêtre absente gardée) ; valeur à la main : positions 0, 1, 3, 4, D = 1, 1, ·, 0, 0 : FIV_série(2) = FIV_série(3) = 3/2 [calc, convention de PS2 tests/test_episodes.py l.36-44 ; égale à SB-10A l.128-134]. M-P2-10 : série comprimée (positions renumérotées).
  - T-P2-VOI-1 sensibilité (neuf) : série écrite à la main, une lacune et les deux bords de la portée : positions retirées, n′, K′, K − K′, garde recalculée. M-P2-33 : bords de la portée non comptés comme lacunes.
- **E-P2 portées** : 09 (modifiée), 11 (f), 12, 13 (modifiée), 14, 15 (modifiée), 16, 19, 26 à 28.
- **Tombe ici** (P2-2 et P2-4, PP l.389, l.391) : `estimateur.py` I (FIV exact, numérateur entier, `Fraction`), double calcul, contrôle (g), tolérance 10^-45 ; T-P2-FIV-1 à T-P2-FIV-4 ; M-P2-09, M-P2-11, M-P2-12 ; refus P2/r1 et P2/entree.
- **Refus** : P2/ep.

### P2R-3 — `intervalles.py` : épisodes, pauses, contrôle (e) (≈ 140 lignes)

- **Contenu**
  - `intervalles.py` (≈ 65) : par (strate, hôte, type), types `episodes.types` de PLAN-S2BIS (panne ; écart), série [(ws, classe)] aux positions réelles ; segments = `episodes.episodes(série, w, toujours vrai)` ; épisodes = `episodes.episodes(série, w, type)` ; pauses = `episodes.episodes(série, w, non type)` (AV l.40) ; pause complète : aucun drapeau ; pause de bord : un drapeau au moins ; segment sans épisode : deux drapeaux ; `episodes.resume` (quantiles `episodes.quantiles` de PLAN-S2BIS, par `regles.quantile`) sur les pauses complètes (compte imprimé en premier, AV l.39 ; moyenne, max, P50, P90, P99, histogramme), sur les pauses de bord (compte, histogramme des longueurs observées), sur les épisodes complets (histogramme, Q-P2-11 b) ; contrôle (e) : ligne d'épisodes régénérée dans la forme de PS2 episodes.py l.106-112 = EP l.13-92, chaîne pour chaîne ; 40 entrées (2 × 10 × 2).
  - `tests/test_intervalles.py` (≈ 75).
- **Tests et mutants**
  - T-P2-EPI-1 épisodes (redéfini : par la série du lot) : fixture, positions 0 à 9, la 5 absente, type vrai en 0, 1, 2, 4, 6, 7, 9 : (3, censuré à gauche), (1, à droite), (2, à gauche), (1, à droite) (PS2 tests/test_episodes.py l.19-24). M-P2-14 (redéfini) : positions renumérotées par le lot.
  - T-P2-EPI-2 contre EP : sortie de forme EP produite dans le test par `episodes.main` épinglé ; (e) égal ; un chiffre altéré : P2/ep. M-P2-15 (redéfini) : contrôle (e) neutralisé.
  - T-P2-EPI-3 complets (neuf) : un épisode censuré et deux complets : histogramme des complets sans le censuré. M-P2-34 : épisode censuré compté complet.
  - T-P2-INT-1 pauses : segment [0 ; 11] vrai en 2, 3 et 7 ; lacune en 12 ; segment [13 ; 16] sans épisode : pause complète 3 (positions 4 à 6) ; pauses de bord 2 (0-1), 4 (8-11), 4 (13-16), dont un segment sans épisode. M-P2-16 (redéfini) : pause de bord comptée complète.
  - T-P2-INT-2 résumé (redéfini) : pauses complètes 1, 2, 2, 7 et une pause de bord de 30 : compte 4, moyenne 3, P50 = 2, P90 = 7, P99 = 7, max 7 ; bord : 1, histogramme 30×1 [calc, rang ⌈num·N/den⌉]. M-P2-18 (redéfini) : statistiques sur toutes les pauses, bords compris (moyenne 42/5, max 30).
- **E-P2 portées** : 10 (précisée), 11 (e), 12, 14, 15 (modifiée), 16, 19, 26 à 28.
- **Tombe ici** (P2-3 et P2-5, PP l.390, l.392) : `estimateur.py` II (segments, épisodes, censure, pauses, quantiles, histogrammes) ; M-P2-17.
- **Refus** : P2/ep.

### P2R-4 — `lancer.sh` I : contrôles avant tout lancement (≈ 175 lignes)

- **Contenu**
  - `lancer.sh` I (≈ 70), forme de PS2 lancer.sh l.1-65 : usage `bash scripts/plan-s2bis-2/lancer.sh <journaux> <sortie> <travail> <sha256 du SHA256SUMS du code>` (code 2 sinon) ; variable ; dossier des journaux ; sortie absente ou vide ; épingle : sha256 du `SHA256SUMS` du lot égal à l'argument, puis `sha256sum -c` dans le dossier du lot ; `parametres.json` de PLAN-S2BIS contrôlé contre son épingle, puis paquet de S2 et commit d'analyse lus dans lui, jamais recopiés (E-P2-03) ; extraction déjà présente ; sha256 du paquet ; bloc machine (une ouverture, une clôture) ; chaque journal du bloc présent et de sha256 égal ; commit du bloc = commit d'analyse ; `control.jsonl` et `journal.jsonl` nommés ; codes 3 ; l'écran ne porte que des noms, des codes et des sha256.
  - `tests/test_lancer.py` I (≈ 105) : arborescence jetable dans la forme de PS2 tests/test_lancer.py l.1-76 (faux paquet, faux journaux, faux scripts qui écrivent leurs arguments, dépôt git temporaire, `git write-tree`), plus les fausses pièces épinglées de PLAN-S2BIS et le `SHA256SUMS` du lot.
- **Tests et mutants**
  - T-P2-LAN-3 épingle : argument différent ; fichier du lot altéré après l'épingle. M-P2-23.
  - T-P2-LAN-4 paquet et bloc : paquet non épinglé ; bloc double ou non fermé. M-P2-24 ; M-P2-25.
  - T-P2-LAN-5 journal : sha256 différent du bloc ; journal absent. M-P2-26.
  - T-P2-LAN-6 commit, variable, sortie, usage : commit du bloc différent ; variable posée à une valeur fictive dans le seul sous-processus du test (exception A-3, E-P2-05) ; sortie non vide ; trois arguments (code 2). M-P2-27 ; M-P2-21 ; M-P2-22.
- **E-P2 portées** : 02 (lanceur), 03 (paquet et commit pris à PLAN-S2BIS), 05 (lanceur), 07, 19, 21 (épingle en argument), 22 (écran), 26 à 28.
- **Tombe ici** (P2-6, PP l.393) : aucun contrôle ne tombe ; « trois scripts » devient deux.
- **Refus** : P2/usage, P2/variable, P2/sortie, P2/epingle, P2/plan-s2bis (`parametres.json` seul), P2/paquet, P2/journal, P2/commit.

### P2R-5 — `lancer.sh` II, identité, README (≈ 185 lignes)

- **Contenu**
  - `lancer.sh` II (≈ 50) : sept autres épingles de PLAN-S2BIS par `sha256sum` (P2/plan-s2bis, code 3) ; extraction de `f35a70c` par `git archive`, dossiers interdits exclus (forme de PS2 lancer.sh l.66-69, plus `docs/adr-0028/execution`, P-9 ; code 4) ; passes A et B et leur comparaison (§7) ; A = B : copie de A ; A ≠ B : P2/identite, code 5.
  - `tests/test_lancer.py` II (≈ 60) ; `tests/test_identite.py` (≈ 30) ; `README.md` (≈ 30 : objet ; frontière et exception écrite, journaux et rendu J28, AV l.199 ; réemplois et épingles ; variable et exception A-3 ; `PLAN_S2BIS_HARNAIS` pour les tests ; commande de lancement détachée ; codes ; lettre du §7) ; `SHA256SUMS` du code (12 lignes, produit).
- **Tests et mutants**
  - T-P2-LAN-1 lancement complet : code 0 ; écran fait de noms, de codes et de sha256 seuls ; sortie = passe A ; `--harnais` = l'extraction du dossier de travail. M-P2-38 : harnais pris au dépôt.
  - T-P2-LAN-2 dossiers interdits non extraits : les six témoins de PS2 tests/test_lancer.py l.17-18, plus un septième sous `docs/adr-0028/execution` (P-9). M-P2-28.
  - T-P2-LAN-7 extraction impossible (4) ; script en échec (5), passe B non commencée (P-7). M-P2-29.
  - T-P2-LAN-8 A ≠ B : faux script dont la sortie dépend de `PYTHONHASHSEED` : code 5, sortie vide, deux `SHA256SUMS` à l'écran. M-P2-30 : comparaison retirée.
  - T-P2-LAN-9 épingles de PLAN-S2BIS au lanceur (neuf) : copie altérée d'une pièce épinglée : code 3. M-P2-39.
  - T-P2-DET-1 identité : `masque_fiv.py` et `intervalles.py` sur fixture, `PYTHONHASHSEED` 0 et 1, sous python3.11, python3.12 et python3.13 (présents sur l'hôte [mesuré]) : sorties égales à l'octet. M-P2-20 : itération sur un ensemble.
- **E-P2 portées** : 02, 03 (épingles au lanceur), 16, 17, 18 (lettre réécrite), 19, 22, 23, 26 à 28 ; puis 20 (répétition à l'échelle, au G1 du worker).
- **Tombe ici** (P2-7, PP l.394) : `tests/vecteurs_fiv.json`, T-P2-ORA-1, M-P2-31 ; job CI (item SHOGEN-PLAN-S2BIS-CI-1) ; troisième script.
- **Refus** : P2/plan-s2bis (au lanceur), P2/identite ; code 4.

## 3. Exigences E-P2 : ce qui reste, ce qui change, ce qui tombe

| n° | état | lettre pour le lot réduit | sous-lots |
|---|---|---|---|
| E-P2-01 | modifiée | liste des fichiers du §1 (`estimateur.py`, `masque.py`, `fiv_unites.py` retirés) ; contrôle sur la liste des chemins de chaque diff | tous |
| E-P2-02 | modifiée | frontière inchangée ; l'exception écrite au G0 du lot nomme les journaux **et** le rendu J28 (AV l.199) | P2R-1, P2R-4, P2R-5 |
| E-P2-03 | précisée | réemploi épinglé étendu à `episodes.py`, `regles.py`, `tests/fixtures.py` (AV l.29) : huit épingles du §1 | P2R-0, P2R-4, P2R-5 |
| E-P2-04 | reste | | P2R-0, P2R-1 |
| E-P2-05 | reste | | P2R-0, P2R-4 |
| E-P2-06 | modifiée | en-tête : plus les sha256 d'`episodes.py`, de `regles.py` et d'EP, et la ligne des sous-arbres (AV l.198 ; P-3) | P2R-1 |
| E-P2-07 | reste | | tous |
| E-P2-08 | reste | `masque_j28.txt`, PP §2.2 tel quel (AV l.138) | P2R-1 |
| E-P2-09 | modifiée | `fiv_unites.txt` : 340 lignes, FIV_série de r1 seule, forme d'EP l.94 (P-6) ; section `[SENSIBILITÉ VOISINAGE]` ; ni N, ni FIV exact (AV l.139) | P2R-2 |
| E-P2-10 | précisée | 40 entrées ; compte des pauses complètes imprimé en premier (AV l.39) ; formes par `episodes`, `resume`, `regles.quantile` (AV l.40) | P2R-3 |
| E-P2-11 | modifiée | contrôles (a) à (f) ; (f) serré par n et K de chaque D_u (P-5) ; (g) tombe (AV l.142) | P2R-0 à P2R-3 |
| E-P2-12 | reste | | tous |
| E-P2-13 | modifiée | « sensibilité au voisinage des lacunes » : d = 1, bords comptés, même grille ℓ, garde recalculée sur le n réduit, pré-déclarée au `parametres.json` (AV l.81 ; P-4) | P2R-0, P2R-2 |
| E-P2-14 | reste | | P2R-1 à P2R-3 |
| E-P2-15 | modifiée | chaînes de r1 sous `r1.contexte_decimal()` seules ; moyennes et quantiles par `resume` ; ni `Fraction`, ni tolérance | P2R-2, P2R-3 |
| E-P2-16 | reste | | tous |
| E-P2-17 | reste | | P2R-5 |
| E-P2-18 | modifiée | lettre réécrite de Q-P2-08 (§7) | P2R-5 |
| E-P2-19 | modifiée | refus du §4 ; P2/r1 et P2/entree tombent | tous |
| E-P2-20 | reste | la répétition mesure la durée des deux passes (≈ 2 min de plus, AV l.71) | après P2R-5 |
| E-P2-21 | précisée | l'ajout daté au G0 de SIM-BIS est inscrit avant l'inscription au JOURNAL du sha256 du code du lot ; antériorité consignée par deux heures `date -u` ; cp-1 bref entre les deux (AV l.66) | épinglage |
| E-P2-22 | reste | | exécution |
| E-P2-23 | reste | appelée par la lettre du §7 | exécution |
| E-P2-24 | reste | | versement |
| E-P2-25 | reste | | versement |
| E-P2-26 | modifiée | références : à la main, `sha256sum`, `episodes.py` épinglé ; le comptage naïf des γ̂_k tombe avec le second estimateur | tous |
| E-P2-27 | reste | | tous |
| E-P2-28 | reste | suites du lot rejouées par l'orchestrateur à chaque sous-lot, faute de job (item CI-1) | tous |
| E-P2-29 | tombe | Q-P2-09 sans objet (AV l.74-76) ; devient une ligne du brief de G2 : passage du propre estimateur du réviseur sur les séries du lot | brief de G2 |

## 4. Refus nommés (E-P2-19 réduite)

| code | cause | où | sous-lot | test |
|---|---|---|---|---|
| P2/usage | arguments du lanceur (code 2) | lanceur | P2R-4 | LAN-6 |
| P2/variable | `SHOGEN_S2_CAMPAGNE_CONTROL` posée | lanceur ; socle | P2R-0, P2R-4 | SOC-2, LAN-6 |
| P2/sortie | dossier de sortie non vide ; extraction déjà présente | lanceur | P2R-4 | LAN-6 |
| P2/epingle | sha256 du `SHA256SUMS` du code différent de l'argument ; `sha256sum -c` en échec | lanceur | P2R-4 | LAN-3 |
| P2/plan-s2bis | une des huit pièces du §1 différente de son épingle ; module chargé hors de son chemin | socle ; lanceur | P2R-0, P2R-4, P2R-5 | SOC-1, LAN-9 |
| P2/paquet | sha256 du paquet de S2 différent ; bloc machine absent, multiple ou non fermé | lanceur | P2R-4 | LAN-4 |
| P2/journal | journal nommé absent ; sha256 différent du bloc ; ligne malformée | lanceur | P2R-4 | LAN-5 |
| P2/commit | commit du bloc différent du commit d'analyse | lanceur | P2R-4 | LAN-6 |
| P2/harnais | module du harnais hors épingles (`commun.importer_harnais`) | socle | P2R-1 | SOC-6 |
| P2/parametres | schéma du `parametres.json` du lot | socle | P2R-0 | SOC-5 |
| P2/coherence | contrôle (a) : bloc 3 recompté différent de l'épingle | socle | P2R-1 | SOC-6 |
| P2/masque | contrôle (b) | `masque_fiv.py` | P2R-1 | MAS-3 |
| P2/pool | contrôle (c) | socle | P2R-0 | POOL-1 |
| P2/ecarts | contrôle (d) | socle | P2R-0 | SOC-4 |
| P2/ep | contrôles (e) et (f) | `intervalles.py` ; `masque_fiv.py` | P2R-2, P2R-3 | FIV-5, EPI-2 |
| P2/identite | passes A et B différentes (code 5) | lanceur | P2R-5 | LAN-8 |

Tombent : P2/r1 (contrôle (g)) ; P2/entree (`estimateur.py`). Codes : lanceur 0 (deux scripts en 0 dans chaque passe, A = B), 2 usage, 3 refus avant tout lancement, 4 extraction impossible, 5 script hors 0 ou A ≠ B ; scripts 0 ou 1 (en-tête et une ligne de refus, aucune valeur).

## 5. Tests et mutants : bilan

| | tests | mutants |
|---|---|---|
| gardés | SOC-2, SOC-3, MAS-2, MAS-3, FIV-5, INT-1, OUT-1, DET-1, LAN-3 à LAN-6, LAN-8 | M-P2-01 à M-P2-08, M-P2-13, M-P2-19 à M-P2-30, M-P2-32 |
| étendus ou redéfinis | SOC-1 (huit pièces), MAS-1 (fixture courte), EPI-1 (série du lot), EPI-2 (cible : contrôle (e)), INT-2 (bords hors des statistiques), LAN-1 (harnais de l'extraction), LAN-2 (septième témoin), LAN-7 (passe B non commencée) | M-P2-10 (tué par FIV-6), M-P2-14, M-P2-15, M-P2-16, M-P2-18 |
| neufs | SOC-4, SOC-5, SOC-6, POOL-1, FIV-6, VOI-1, EPI-3 ; LAN-9, neuf par son objet (refus P2/plan-s2bis au lanceur, nommé à PP l.346 sans test) | M-P2-33 à M-P2-41 |
| retirés | FIV-1 à FIV-4, ORA-1 (AV l.151) | M-P2-09, M-P2-11, M-P2-12, M-P2-17, M-P2-31 |

- Les mutants s'appliquent au code du lot seul ; aucun ne touche `scripts/plan-s2bis/` (d'où les redéfinitions : la censure et le quantile sont ceux d'`episodes.py` et de `regles.py`, déjà tués par les tests de PLAN-S2BIS : PS2 tests/test_episodes.py l.19-33, tests/test_regles.py l.11-13).
- Classement par la sortie du runner : 0 vivant, 1 tué, 3 ou autre FATAL, campagne relancée après correction (E-P2-27).
- Mutant de spécification sans oracle propre (PP l.425-426) : sans objet ; les drapeaux de bord viennent d'`episodes.episodes`, et INT-1 tue le filtre du lot (M-P2-16).

## 6. Ce qui n'est pas perdu, ce qui l'est

Gardés : les trois sorties, le masque, la sensibilité au voisinage, l'histogramme des complets, tous les contrôles contre EP, l'identité bit à bit, le lanceur à deux passes (AV l.158). Perdu : un second auteur interne du FIV ; la G2 du lot le remplace par son propre estimateur (E-P2-29), et SHOGEN-LECTEUR-INDEP-1 porte la limite.

## 7. Lettre réécrite de Q-P2-08 (E-P2-18, au G0 du lot)

À écrire au G0 du lot, mot pour mot (AV l.72 ; Q-P2-08 (b) adoptée), **en remplacement** de la lecture « une fois » : brief l.29 (« Seuls les scripts du lot, épinglés, les lisent une fois, lancés par l'orchestrateur ») et B.58 l.961 (« exécutés une fois »). L'avis demande de remplacer la lettre, non de la réinterpréter (AV l.72) :

> « un seul lancement ; dans ce lancement, deux passes A et B (`PYTHONHASHSEED` 0 et 1) ; sha256 comparés ; A ≠ B est un refus (code 5), aucune sortie n'est versée ni ouverte par quiconque, les deux `SHA256SUMS` seuls sont consignés ; la cause est cherchée sur fixtures ; toute relance est une déviation déclarée (E-P2-23) »

Mise en œuvre au lanceur (P2R-5), sans rien ajouter à la lettre :

1. Un lancement = une commande `lancer.sh`, détachée, par l'orchestrateur, après l'épinglage au JOURNAL (E-P2-21, E-P2-22).
2. Passe A : `masque_fiv.py`, puis `intervalles.py`, `PYTHONHASHSEED=0`, sorties dans `<travail>/A` ; passe B : les mêmes, `PYTHONHASHSEED=1`, dans `<travail>/B` ; même code épinglé, même extraction, mêmes arguments.
3. Chaque passe écrit son `SHA256SUMS` (noms et sha256 de ses trois sorties) ; les deux fichiers sont comparés à l'octet.
4. A = B : les trois sorties de A et son `SHA256SUMS` sont copiés dans `<sortie>` ; code 0.
5. A ≠ B : refus P2/identite, code 5 ; rien dans `<sortie>` ; les deux `SHA256SUMS` affichés (noms et sha256 seuls), consignés par l'orchestrateur ; les fichiers des passes ne sont ni ouverts ni copiés (P-8).
6. Un script hors 0 : code 5, rien dans `<sortie>` ; la passe B ne commence pas si A a échoué (P-7).
7. Relance : déviation déclarée (E-P2-23 : motif, correctif relu en G2, nouvelles épingles au JOURNAL, mention à l'annexe B) ; un lancement coupé par une borne de temps se refait et ne se compte pas.

Tests : T-P2-LAN-1 (A = B), T-P2-LAN-7 (script en échec), T-P2-LAN-8 (A ≠ B) ; identité sur fixtures : T-P2-DET-1 (E-P2-17). Coût : ≈ 2 min de plus (AV l.71).

## 8. Items à former (règle PAROXYSME)

| item | état | constat | construction | prix [inféré] | déclencheur |
|---|---|---|---|---|---|
| SHOGEN-PLAN-S2BIS-CI-1 | neuf (AV l.89, l.153) | deux lots lisent les journaux scellés, PLAN-S2BIS et PLAN-S2BIS-2, et aucun job CI ne rejoue leurs tests ; seul l'orchestrateur les rejoue, à chaque sous-lot (E-P2-28) | un job commun aux deux lots : historique complet, harnais extrait de `f35a70c` par les tests eux-mêmes (forme d'`oracle_r1`, AV l.89), extension du cas K-02 du runner (SHOGEN-CI-S2-CABLAGE-1) ; une G2 | ≈ 40 lignes (AV l.89) | après E0, hors du chemin critique (AV l.89, l.174) |
| SHOGEN-PLAN-S2BIS-EXCLUSIONS-1 | neuf (constat de ce jour, P-9) | `docs/adr-0028/execution`, interdit aux agents par le brief de ce G0, existe à `f35a70c` [mesuré] et n'est pas dans les exclusions de PS2 lancer.sh l.66-67 ; l'extraction du lancement de PLAN-S2BIS (2026-10-04) l'a donc écrit dans son dossier de travail [inféré, PS2 lancer.sh l.66-69] ; rien n'indique qu'il ait été ouvert (le lanceur n'affiche que des noms, des codes et des sha256) | exclusion et septième témoin dans ce lot (P2R-5) ; pour PLAN-S2BIS, l'orchestrateur constate que ce dossier de travail est effacé, ou l'efface | 2 lignes et un témoin | P2R-5 ; constat de l'orchestrateur avant l'épinglage du lot |
| SHOGEN-PLAN-S2BIS-2-ORACLE-CALIB-1 | retiré (PP l.564 ; AV l.151) | Q-P2-09 sans objet : un seul estimateur, r1, auteur d'EP | — | — | — |
| SHOGEN-SIM-BIS-FIV-IDENTIF-1 (B.61 l.1022) | précisé | troisième constat : le filet ne joue plus si E1 n'encadre pas S2 (G2-T4 l.189) ; fermé dans la lettre par les points (5), (8) et (9) de `LETTRE-AJOUT-G0-SIM.md` | ce lot, puis le diff d'intégration de SIM-BIS (≈ 150 à 180 lignes, AV l.156) | ce lot | remplacé par « sortie d'E1 épinglée » ; limite écrite selon le point (8) (ii) si C1 est au bord |
| SHOGEN-SIM-BIS-SOURCES-LIMITES-1 (B.64 l.1070) | précisé | (i) C1 « borne haute du groupement propre » comme direction, non démontrée pour la durée (AV l.166) ; au bord, « borne basse de la mesure » (point (8) (ii)) ; (ii) en stress, 453 des 674 épisodes d'écart censurés (67 %), contre un plafond ≈ 37 % sous indépendance (2 × 2 094 / 11 397) ; en calme, 15 % sous ≈ 46 % (AV l.164, l.167) ; (iii) pauses complètes penchées vers les courtes ; en stress, bitfinex, chainlink, coingecko et kraken n'ont presque que des pauses de bord (AV l.39) | phrases au paquet (SB-12), chiffrées par les sorties du lot | aucun | phrases de limite (SB-12) |
| SHOGEN-SIM-BIS-SB11-IMPRESSIONS-1 (B.64 l.1069) | précisé | impressions du point (6) de la lettre : résidus de C1 par hôte et par ℓ, meilleur point par hôte, écart-type des 200 FIV par point et par ℓ, réplications à FIV indéfini par hôte ; ligne nommée du bord (point (8) (iv)) ; loi des pauses du modèle à C1 | impressions | ≈ 25 lignes (AV l.156) | brief de SB-11 |
| SHOGEN-SIM-BIS-SB11-BRIEF-1 (B.66 l.1097) | précisé | ordre impératif : ajout daté, cp-1 bref, épinglage du lot, lancement, versement, diff d'intégration commis, E0, E1 (AV l.178) ; aucune exécution provisoire avec l'ancienne C1 (AV l.188) | ligne de brief | aucun | brief de SB-11 |
| SHOGEN-SIM-BIS-REGIME-FAISABILITE-1 (B.64 l.1067) | précisé | s'applique au point C1 mesuré | un calcul | aucun | épinglage de C1 |
| SHOGEN-SIM-BIS-POOL-EP-SEPARES-1 (B.66 l.1096) | précisé | le lecteur des sorties lit la liste des dix hôtes du format, jamais le pool opérationnel ; un seul analyseur de ligne pour EP et `fiv_unites.txt` (P-6) | séparation des deux listes | compris dans le diff d'intégration | diff d'intégration |
| SHOGEN-SIM-BIS-STRESS-EPISODES-1 (B.61 l.1029) | précisé | limite chiffrée par l'histogramme des complets ; en stress, 2 à 8 complets pour quatre hôtes : histogramme vide d'information (AV l.85) | phrase | aucun | sortie d'E1 |
| SHOGEN-S2BIS-P1-ESTIMATION-1 (B.61 l.1018) | précisé | ≈ 150 lignes annoncées ; ≈ 980 estimées au périmètre réduit (≈ 750 à 900 à l'avis) | une ligne à la clôture | aucun | clôture du lot |
| SHOGEN-LECTEUR-INDEP-1 (G2-PS2 l.182) | précisé | un seul auteur interne de FIV_u (r1) et des épisodes (`episodes.py`) ; la G2 du lot passe son propre estimateur sur les séries du lot (AV l.158) | ligne du brief de G2 | aucun | brief de G2 du lot |

Consignes appliquées sans item neuf : SHOGEN-WORKER-TMPDIR-1, SHOGEN-PLAN-S2BIS-LOG-1, SHOGEN-PLAN-S2BIS-VARIABLE-TEST-1, SHOGEN-FICHE-WORKER-POSTEXEC-2 (l'exception écrite au G0 du lot nomme les journaux et le rendu J28, AV l.199). Non déclenché : SHOGEN-PLAN-S2BIS-GARDES-1 (B.58 l.970), `scripts/plan-s2bis/` n'étant pas touché.

## 9. Précisions de lettre à adjuger au G0 du lot (lues dans le code de PLAN-S2BIS)

- **P-1 Chargement** [lu] : `episodes.py` importe `commun` et `regles` par leur nom (PS2 episodes.py l.17-18) ; `regles.py` importe `commun` (PS2 regles.py l.9) ; `tests/fixtures.py` importe `commun` et exige `PLAN_S2BIS_HARNAIS` (PS2 tests/fixtures.py l.9-15). Les trois modules se chargent donc sous leurs noms, dans l'ordre `commun`, `regles`, `episodes` ; `fixtures.py` sous un nom distinct (`fixtures_ps2`).
- **P-2 Socle II** [lu] : `commun.executer` ne se réemploie pas tel quel : son en-tête ne liste que les modules du dossier de `commun.py` (PS2 commun.py l.178-183), ne lit qu'un `parametres.json` (l.173), et `--sortie` y est un fichier (l.196-198) ; le lot passe un dossier, `masque_fiv.py` écrivant deux sorties.
- **P-3 Ligne des sous-arbres** [lu] : la ligne de l'avis (AV l.198 : segment, strates, pool_d1bis, episodes, fiv) omet `classes`, lu par `commun.pool_d1bis` (PS2 commun.py l.96), et les épingles lues par le code réemployé (`commit_analyse`, `harnais_sha256`, `rendu_j28` : l.147, l.174-175, l.184 ; `paquet_s2` au lanceur, PS2 lancer.sh l.30-36). Lettre proposée : « sous-arbres lus dans scripts/plan-s2bis/parametres.json : segment, strates, pool_d1bis, classes, episodes, fiv ; épingles : commit_analyse, harnais_sha256, rendu_j28, paquet_s2 ».
- **P-4 Lacune de la sensibilité** [inféré] : position de grille non retenue dans la strate (absente, exclue, D5, de l'autre strate, hors portée), dual exact de la censure d'EP (PS2 episodes.py l.8, l.35 ; AV l.163) ; les bords de la portée y sont compris (AV l.81), les passages de strate aussi. d = 1 retire toute position retenue dont une voisine à distance 1 n'est pas retenue dans la strate.
- **P-5 Contrôle (f) par hôte** [calc] : n et K de chaque D_u = n_s et cellules « ecart » d'EP l.13-92 (forme de PP l.171). Sans cette ligne, M-P2-32 survit sur la fixture de PLAN-S2BIS : la courbe de I_t y est la même sous panne et sous écart (seule cellule périmée : fenêtre 1, un seul écart), alors que K de l'hôte a vaut 5 sous écart et 4 sous panne (PS2 tests/test_episodes.py l.57-66).
- **P-6 Forme des lignes de FIV_u** [inféré] : forme exacte d'EP l.94, « cv théorique » compris (rendu par `episodes.courbe`, l.67-69), pour qu'un seul analyseur de ligne lise EP et `fiv_unites.txt` côté SIM-BIS (AV l.156) ; la liste de l'avis (AV l.139) ne nomme pas cv.
- **P-7 Passe B après un échec de A** [inféré] : non commencée (une lecture de moins) ; l'avis ne le dit pas.
- **P-8 Fichiers des passes sur A ≠ B** [inféré] : restent dans le dossier de travail, jamais ouverts ni copiés ; l'orchestrateur efface ce dossier après avoir consigné les deux `SHA256SUMS` (AV l.72 : « aucune sortie n'est versée ni ouverte par quiconque »).
- **P-9 Exclusion de `docs/adr-0028/execution`** [mesuré] : présent à `f35a70c`, interdit aux agents par le brief de ce G0, absent des exclusions de PS2 lancer.sh l.66-67 : serrage dans ce lot (P2R-5), et item SHOGEN-PLAN-S2BIS-EXCLUSIONS-1.

## 10. Provenance (G1) et attestation

- **Lu ce tour** [lu] : `AVIS-PLAN2.md` l.1-95 et l.125-204 ; `PROPOSITION-PLAN2.md` l.72-231, l.286-445, l.478-602 ; `NOTES.md` l.330-420 ; au dépôt, `scripts/plan-s2bis/episodes.py` (en entier), `commun.py` (en entier), `regles.py` l.1-25, `tests/fixtures.py` (en entier), `tests/test_episodes.py` (en entier), `tests/test_lancer.py` l.1-60 et lignes des tests, `tests/test_regles.py` l.11-13, `lancer.sh` (en entier), les deux `SHA256SUMS` de PLAN-S2BIS ; EP : nombre de lignes et début des lignes 8, 12, 13, 92, 93, 94, 127, 128, 161 ; brief l.29 ; annexe B l.961 (« exécutés une fois »).
- **Commandes** [mesuré] : `date -u` (14:26:51, 14:37:48, 14:38:04, 14:41:31, 14:45:17, puis 14:46:51) ; `git rev-parse HEAD` (`dcbd9d05…` à 14:26:51, `af859b79…` à 14:41:31, `4df58862…` à 14:45:17, `4df5886` à l'écriture) ; `git diff --quiet 5f99ab5 HEAD` sur `docs/adr-0029/ADR-0029-campagne-S2-bis.md`, `docs/adr-0028/ANNEXE-B-items.md`, `docs/adr-0029/g0-sim`, `docs/adr-0029/plan-s2bis`, `scripts/plan-s2bis`, `docs/adr-0029/G0-lot-PLAN-S2BIS.md`, `docs/adr-0029/G0-lots-S2BIS.md` : code 0 (14:27, 14:45 et à l'écriture) ; `sha256sum` des pièces du §1 ; `wc -l` du code et des tests de PLAN-S2BIS ; `ls /usr/bin/python3*` (3.10 à 3.13 présents) ; `git ls-tree --name-only` à `f35a70c` et à HEAD sur `docs/adr-0028/` seul, un niveau, noms seuls (30 noms à `f35a70c` ; deux affichés : `execution`, `monark-m009a`).
- **Recomptes** [calc] : PLAN-S2BIS, code 661 lignes (`commun.py` 199, `episodes.py` 129, `okx.py` 77, `regles.py` 47, `tau_sigma.py` 127, `lancer.sh` 82), tests 813 (dont `fixtures.py` 103), total 1 474 ; tailles du §1 : 85 + 100 + 65 + 65 + 70 + 50 = 435 ; 75 + 80 + 75 + 75 + 105 + 90 = 500 ; 30 + 12 = 42 ; total 977 ; FIV_série à la main de T-P2-FIV-6 : γ̂₀ = 1, γ̂₁ = 1/2, γ̂₂ = −1/4, γ̂₃ = −1/2, FIV(2) = 1 + 2 × 1/2 × 1/2 = 3/2, FIV(3) = 1 + 2 × (2/3 × 1/2 − 1/3 × 1/4) = 3/2 ; T-P2-INT-2 : rangs ⌈50 × 4/100⌉ = 2, ⌈90 × 4/100⌉ = 4, ⌈99 × 4/100⌉ = 4 ; avec le bord : 42/5.
- **Écarts** : E-5 (ce tour) : listage d'un niveau de `docs/adr-0028/` à `f35a70c` et à HEAD, noms seuls, pour P-9 : aucun contenu de `execution/` ni de `monark-m009a/` listé ni ouvert. La base a avancé pendant la passe (commits de l'orchestrateur) ; l'index de l'orchestrateur n'est pas touché.
- **Attestation (forme D.3)** : aucune pièce de la liste D.2 ouverte ; aucun `*.jsonl` lu, listé ni haché ; rien de `docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, `docs/adr-0028/execution/` ; aucune opération git en écriture ; seul le dossier `…/s2bis/plan2/` est écrit. Exposition : valeurs de S2 post-rendu portées par EP et par l'avis ; aucune donnée de S2-bis n'existe.
