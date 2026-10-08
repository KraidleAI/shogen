# Journal G1 — partie 2 de S2, étape B, sous-lots B0 à B2

**Nature de ce journal** : journal de provenance du worker `shogen-worker` (session cloud), travail du
2026-10-02 de 04:04 à 04:47 UTC (horloge lue par `date -u` : 04:04:52 au départ, 04:46:01 au dernier passage de la
suite). Contrat :
`docs/adr-0028/G0-partie-2.md`, section « B — RENDU-2 » (03:2x UTC) et son ajout daté du 2026-10-02 04:0x UTC
(sous-lot B0). Branche `partie-2-rendu`, base `34e096f`. Pendant le travail, l'orchestrateur a commis `4e8ec65`
et `3509ca0` (JOURNAL.md, `docs/G1-partie-2-P0.md`, `docs/PASSATION-CLOUD.md` seulement) :
`git diff --quiet 34e096f 3509ca0 -- s2-harness` sort 0, les trois diffs valent donc pour l'une et l'autre base.
Aucune opération git en écriture ; aucun commit. Livrables : arbre de travail portant B0 + B1 + B2, diffs
`B0.diff`, `B1.diff`, `B2.diff` dans le scratchpad de la session (`…/scratchpad/lot-B/`), ce journal.

## 0. Gate 0

Modèle résolu sous lequel le worker a tourné : **`claude-opus-5-5`** (identifiant exact fourni par l'environnement
de la session ; préfixe attendu `claude-opus-5-5` : conforme). Effort : `max` (fiche `.claude/agents/shogen-worker.md`
et brief).

## 1. Provenance commune

### 1.1 Sources lues (toutes [lu] ; aucune [abs] ni [2nd])

- `CLAUDE.md` (racine, en entier, rappelé par la session).
- `docs/adr-0028/G0-partie-2.md` l.1-154, en entier (sections P0, A, B, C et l'ajout daté B0, l.147-154).
- `docs/adr-0028/ANNEXE-B-items.md` : l.43 (SHOGEN-TORN-LINE-UTF8-1), l.45 (SHOGEN-RAW-LECTEUR-1), l.214
  (SHOGEN-BLOC6-TS-1), l.335-345 (bloc B.21 : SHOGEN-DECIMAL-ARRONDI-2, SHOGEN-DECIMAL-CONTEXTE-1 et les trois autres
  items, réponses Q1 et Q3) ; liste des titres (`grep -n "^#"`).
- `docs/adr-0028/ADR-0028-decisions-sortie-S2.md` l.184-200 (D6 (i) à (vi)), repérées par `grep -n "D6"` sur ce seul
  fichier.
- `docs/adr-0028/ANNEXE-D-preenregistrement.md` l.30-43 (D.2, liste fermée) et la liste des titres.
- `docs/G1-partie-2-etape-A.md` l.1-83, en entier ; `docs/adr-0028/PLAN-PARTIE-2.md` l.1-70, en entier.
- Diffs des commits `4e8ec65` et `3509ca0` sur `JOURNAL.md` et `docs/PASSATION-CLOUD.md` (lus pour savoir si une
  consigne nouvelle me concernait : non ; biblio recopiée, S-G5 en corpus complet).
- Code : `s2-harness/shogen_s2/r1.py` l.1-808 (en entier), `report.py` l.1-768 (en entier), `records.py` l.1-362
  (en entier), `journal.py` l.1-63, `lm.py` l.30-242, `r2.py` l.55-80, 420-830 et 905-1101, `collector.py`
  l.95-252, `__init__.py`.
- Tests : `test_arrondi.py` (en entier), `test_critere.py` (en entier), `test_bloc3_bloc6.py` (en entier),
  `test_exclusion.py` l.1-120, `test_pool_analyse.py` l.25-40, `test_collector.py` l.405-470, `test_r1.py` l.36-90,
  `test_lm.py` l.30-60, `test_r2.py` l.30-60, `test_rendu_blocs.py` l.20-90, `capture.py` (tête), `expected.json`
  (tête).
- Gates : `xtask/src/sg4.rs` l.1-130 (locutions interdites, périmètre), `xtask/src/sg5.rs` (lignes repérées par
  `grep`), `xtask/src/main.rs` l.32-62 ; `.github/workflows/gates.yml` (lignes repérées par `grep` : aucun linter
  Python en CI).
- Bibliothèque standard : `/usr/lib/python3.11/_pydecimal.py` l.6088-6096 (`DefaultContext` : prec 28,
  ROUND_HALF_EVEN, traps DivisionByZero, Overflow, InvalidOperation, flags vides, Emax 999999, Emin −999999,
  capitals 1, clamp 0), recoupé par `print(decimal.DefaultContext)` à l'exécution (Python 3.11.15).
- Scratchpad de l'étape A : `render_fixture.py` (sha256 `4084c42b…`, imposé par le brief, utilisé tel quel),
  `regle_fixtures.py` (`5557fb56…`, lu, réécrit à l'identique de logique dans `regle_b.py`), `faire_diff.py`
  (`e03caf95…`, lu, réécrit dans `faire_diff_b.py`).

### 1.2 Pré-enregistrement (annexe D)

- D.4 a : fixtures seulement (collecteur réel sur horloge factice, fichiers synthétiques) ; aucun journal de
  campagne lu.
- D.2 : aucune pièce ouverte ; la cartographie du 2026-09-29 et ADR-0025 n'ont pas été ouvertes ; aucun `grep` large
  sur `docs/` (recherches limitées aux fichiers nommés ci-dessus). Une copie de `JOURNAL.md` présente dans le
  scratchpad n'a pas été ouverte.
- `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée (`env | grep -c` : 0 au départ et à la fin).

### 1.3 Outils écrits (scratchpad `lot-B/outils/`, sha256)

`oracle_b0.py` `48f6f48d…` (oracle sans le module decimal : fractions et entiers, arrondi pair à 50 chiffres, racine
correctement arrondie par `math.isqrt`) ; `sonde_b0.py` `261a346b…` (sites `localcontext` atteints par le rendu J2,
appels inexacts par site) ; `cherche_plage.py` `2fe3c08a…` ; `temoins_b0.py` `55a25051…` ; `sonde_ambiant_b0.py`
`c4f7a4f1…` ; `applique_b0.py` `650daced…` (remplacement contrôlé des 28 sites) ; `regle_b.py` `b5dfa01c…` ;
`equivalence_lecteur.py` `3e0b9d32…` ; `faire_diff_b.py` `1d7e4b56…` ; `mutants.py` `0916dbe1…` (moteur commun :
copie de l'arbre, mutation textuelle, tests nommés) ; `mutants_b0.py` `d38e7e66…`, `mutants_b1.py` `794e01e2…`,
`mutants_b2.py` `649765d8…`.

### 1.4 État de départ (arbre `34e096f`, exporté par `git archive` dans `lot-B/arbres/HEAD`, égal à l'arbre de travail)

- Suite : `Ran 318 tests in 27.190s`, `OK (skipped=2)`.
- `cargo --locked xtask verify` : `=== VERDICT GLOBAL : VERT ===`, rc 0 (`preuves/verify-depart.out`).
- Règle scellée : JSON des sorties de `regle_critere` sur les fixtures de `tests/test_critere.py` (16 entrées : U1 à
  U8, J1, J1 à ℓ = 1, J2, J3 à ℓ = 1, J5 = `deux(50, 40)`, J4, `seuil`, `ell`), sha256 `ea3a2d94…` (= étape A).
- Rendus épinglés (`render_fixture.py`) : sans option `c4f45f47…`, avec option `d0f785eb…` (= épingles en vigueur).

## 2. B0 — contexte Decimal nommé complet (SHOGEN-DECIMAL-CONTEXTE-1, SHOGEN-DECIMAL-ARRONDI-2)

### 2.1 Mesure avant construction

- Sites `localcontext` du paquet (`grep -n "with localcontext"`) : `r1.py` 14, `lm.py` 3, `r2.py` 10, `report.py` 1,
  `closure.py` 1 ; total du chemin de recalcul : 14 + 3 + 10 + 1 = 28 (recompté).
- Sonde `sonde_b0.py` sur J2 (`journal(200, 200, deux(50, 37))`, sans option puis avec une plage) : sites atteints
  avec opération inexacte : lm l.73, 91, 155 ; r1 l.217, 249, 263, 314, 356, 383, 610, 708 ; r2 l.475 ; sites
  atteints sans opération inexacte : r1 l.94, 169, 760, r2 l.491, 524, 584, 604, 645, 668, report l.701 ; non
  atteints : r1 l.227, 291, 652, r2 l.434, 548, 937. Conséquence : le seul rendu J2 ne suffit pas à tuer chaque
  mutant de site ; une table par site est ajoutée (2.3).
- `cherche_plage.py` : sur J2, la plage `[SAM + 6000 ; SAM + 11940]` (100 dernières fenêtres stress) rend l'écart de z
  de [SENSIBILITÉ] inexact (z exclue −2,77…, z incluse 0,146…) ; les plages en calme laissent la strate sous la
  garde ou gardent l'exposant (écart exact).
- Témoins attribut par attribut (`temoins_b0.py`, arbre `34e096f`) : rendu J2 sous ROUND_DOWN seul, 4 lignes du
  bloc 4 changent (Ê(Θ) …667 → …666 et Var̂(Θ) …779 → …775 en calme, …114 → …110 en stress : le constat L1 de
  l'étape A, recompté) ; sous Emin −20 seul, 0 ligne sur J2, mais `_median([1E-75, 3E-75])` rend `0E-69` ; sous le
  piège Inexact seul, rendu interrompu (`Inexact`).

### 2.2 Construction (décision du G0 appliquée)

- `r1.py` : `CONTEXTE_DECIMAL = Context(prec=DECIMAL_PREC, rounding=ROUND_HALF_EVEN, Emin=-999999, Emax=999999,
  capitals=1, clamp=0, flags=[], traps=[InvalidOperation, DivisionByZero, Overflow])`, défini une fois, à côté de
  `DECIMAL_PREC` (valeurs du `DefaultContext` de la bibliothèque standard, précision mise à part : sous le contexte
  par défaut, aucun calcul ne change, par construction).
- Les 28 sites de `r1.py`, `lm.py`, `r2.py`, `report.py` deviennent `with localcontext(CONTEXTE_DECIMAL):` (copie du
  contexte nommé ; les lignes `ctx.prec = …` et `ctx.rounding = …` disparaissent) ; `applique_b0.py` contrôle le
  compte par fichier (14, 3, 10, 1) et l'absence résiduelle de `localcontext()` dans ces quatre fichiers.
- Imports : `lm.py` et `report.py` prennent `CONTEXTE_DECIMAL` au lieu de `DECIMAL_PREC` (plus utilisé) ; `r2.py`
  garde `DECIMAL_PREC` (lu par `tests/test_r2.py` : `PREC = r2.DECIMAL_PREC`) et ajoute `CONTEXTE_DECIMAL`.
- `closure.py` (quarantaine, D6 (i) et (vi)) : non touché (`git diff --quiet 34e096f -- …/closure.py` : 0) ; limite
  déclarée au §7.

### 2.3 Tests (`tests/test_contexte_decimal.py`, neuf)

Contexte ambiant hostile du G0 : `rounding = ROUND_DOWN`, `Emin = −20`, `traps[Inexact] = True`.

1. `test_contexte_nomme_complet` : attributs du contexte nommé (prec 50, ROUND_HALF_EVEN, Emin −999999, Emax 999999,
   capitals 1, clamp 0, pièges exactement {InvalidOperation, DivisionByZero, Overflow}, aucun drapeau levé) ;
   valeurs de référence : `_pydecimal.py` l.6088-6096.
2. `test_sites_sous_contexte_hostile` (24 sous-tests) : les 13 sites calculants de r1 par la table `CAS` de
   `test_arrondi` (attendus de l'oracle de l'étape A) ; 10 sites de lm et r2 non exercés en inexact par J2 (table
   `X`) ; l'exemple de DECIMAL-CONTEXTE-1 (`_median([1E-75, 3E-75])` = `2E-75`). Chaque cas : attendu au contexte
   par défaut, puis sous le contexte hostile (valeur et chaîne). Attendus de la table `X`, de `oracle_b0.py`
   (`preuves/oracle_b0.out`) : `pairwise_second_moment(2, 4)` = 1/6 arrondi = `0.1666…667` ; `pearson` sur
   (0, 1, 2) et (0, 0, 3) = 3/rac50(12) = `0.86602540378443864676372317075293618347140262690518` (deux arrondis ;
   √3/2 arrondi une fois finirait en …519) ; `log_returns` sur un ln à 51 chiffres = `1.000…02` ; `_quantize(1.015,
   0.01)` = `1.02` (au pair) ; `tick_identity` T = 2/3 = `0.666…67` ; `coaberrance_kz` p_co = r50(r50(2/3)²) =
   `0.444…45` ; quatre cas « piège » (rho_resid, _aberrance_by_window, _jumps, cluster_lm_correlations) dont la
   sortie ne dépend pas du dernier chiffre : attendus écrits à la main (1, {}, {60: 0, 120: 0, 180: 1}, None).
3. `test_rendu_j2_et_regle_sous_contexte_hostile` : rendu J2 sans option, sorties de la règle (`regle` de
   `test_critere` : `recompute_from_journal` puis `regle_critere`), rendu J2 avec la plage du §2.1 ; sous le contexte
   hostile, égaux au contexte par défaut ; la ligne « écart de z » de la strate stress est présente.

Échec avant (code de `34e096f`, tests B0 ajoutés : `preuves/B0-avant.out`) : `FAILED (errors=26)` —
`AttributeError: module 'shogen_s2.r1' has no attribute 'CONTEXTE_DECIMAL'` (test 1) ; `decimal.Inexact` pour J2
(test 3) et pour les 24 sous-tests (test 2 ; la première assertion, au contexte par défaut, passe dans chaque cas :
les attendus de l'oracle égalent le code au contexte par défaut). Succès après : `Ran 3 tests … OK`.

Témoins après (`temoins_b0.py`, arbre final) : ROUND_DOWN seul 0 ligne, Emin −20 seul 0 ligne, piège Inexact seul
0 ligne ; `_median([1E-75, 3E-75])` sous Emin −20 = `2E-75`.

### 2.4 Mutants (`mutants_b0.py`, `preuves/B0-mutants.out`) : 35 tués sur 36

- Chaque site ramené à `with localcontext():` (28 mutants) : 27 tués (test 2 seul pour r1 l.98, 171, 217, 225, 245,
  283, 594, 738, lm l.73, r2 l.435, 490, 522, 545, 580, 639, 661, 929 ; test 3 seul pour lm l.90, 153, r2 l.475,
  report l.701 ; les deux pour r1 l.257, 304, 344, 369, 688, r2 l.599). Numéros de ligne de l'arbre B0.
- Mutant vivant, **équivalent, déclaré** : r1 l.634 (`compute_r1`, `degenere = (n == 0) or (p_more == Decimal(0)) or
  (p_more == Decimal(1))`) : comparaisons d'égalité seules, exactes quel que soit le contexte (même constat qu'à
  l'étape A).
- Premier passage : lm l.73 vivant (`pairwise_second_moment` n'est appelé par J2 qu'à l'intérieur du contexte nommé
  de `compute_lm`, dont la copie ambiante est alors le contexte nommé) ; cas direct ajouté à la table `X`, puis tué.
- Attribut changé (8 mutants : prec − 1, ROUND_HALF_UP, Emin −20, Emax 99, capitals 0, clamp 1, drapeau levé, piège
  Overflow retiré) : 8 tués (test 1 ; prec et Emin aussi par le test 2).

### 2.5 Règle scellée, rendus, suite, taille

- Règle : `regle_b.py` sur l'arbre B0 : 16 entrées, sha256 `ea3a2d94…`, `cmp` identique à l'octet au JSON de
  `34e096f`.
- Rendus épinglés : sans option `c4f45f47…`, avec option `d0f785eb…`, identiques à l'octet à ceux de `34e096f` :
  aucune re-capture.
- Suite : `Ran 321 tests in 26.783s`, `OK (skipped=2)` (318 + 3).
- Numstat (`faire_diff_b.py`, `preuves/B0-numstat.out`) : lm.py +4 −7 ; r1.py +21 −45 ; r2.py +11 −20 ; report.py
  +2 −3 ; tests/test_contexte_decimal.py +87 −0 ; total +125 −75 = **200 lignes** (plafond atteint après
  compactage des docstrings du test ; aucune coupe nécessaire).

## 3. B1 — lecteur en octets (SHOGEN-TORN-LINE-UTF8-1) et relevé sans ts au bloc 6 (SHOGEN-BLOC6-TS-1)

### 3.1 Construction

- `records.read_jsonl_tolerant` : lecture en octets, découpe `bytes.splitlines()` (fins de ligne universelles LF,
  CRLF, CR, comme le mode texte ; contrôlé : ni `\x0b`, `\x0c`, `\x1c`-`\x1e`, `\x85` ni U+2028 ne coupent, ni en
  mode texte ni ici), décodage UTF-8 ligne par ligne ; ligne blanche jugée sur le texte décodé (décodage avec
  remplacement : même jugement qu'avant pour les lignes décodables) ; dernière ligne non vide illisible (JSON, ou
  UTF-8 non décodable) : consignée sur stderr (`(ligne N, non décodable en UTF-8)`), ignorée ; ligne illisible non
  finale : `ValueError` nommée (`ligne non décodable en UTF-8 NON finale dans … (ligne N)` ; le message JSON
  d'avant est gardé à l'identique).
- `report.py`, bloc 6 : hôtes du pool dont le relevé retenu n'a pas de `ts` (ou `ts` nul) mis à part ; la date de
  la partition porte sur les relevés datés (`{len(ts)} / {len(hosts)}`) ; ligne neuve, toujours imprimée, sous la
  date : `relevés asn_attribution retenus sans ts (hôtes du pool, entrée malformée) = k [: hôtes] — comptés à part,
  hors date de la partition (SHOGEN-BLOC6-TS-1)` ; si aucun relevé retenu n'est daté alors que des hôtes en ont un,
  « non mesurée (… retenu daté) » au lieu d'un énoncé faux.
- `records.filtre_horodatage` : sous un filtre (plage ou segment), un enregistrement sans son champ d'horodatage
  lève `ValueError` nommée (`asn_attribution sans ts : placement dans le segment ou la plage indécidable —
  fail-closed`) au lieu de `KeyError` (écart E4, §6).

### 3.2 Tests (`tests/test_lecteur.py`, neuf : classes `TestLecteurOctets`, `TestBloc6SansTs`)

1. Fixture HS2-03 : `{"a": 1}` CR, ligne d'espace insécable LF, `{"b": "é"}` CRLF, puis `{"c": "` et l'octet 0xC3
   seul (coupure dans « é ») : `[{"a": 1}, {"b": "é"}]`, stderr « dernière ligne tronquée ignorée » et
   `(ligne 4, non décodable en UTF-8)`.
2. Ligne 2 non décodable suivie d'une ligne valide : `ValueError` dont le message commence par `ligne non décodable
   en UTF-8 NON finale` et nomme `(ligne 2)`.
3. Chemin de recalcul : `control.jsonl` (fixture J de 20 fenêtres) terminé par une copie de `run_params` coupée
   après le premier octet de « é » : rendu égal au rendu sans cette ligne.
4. Bloc 6 : fixture d'exclusion, sondes datées A = `PLAGE[0]` (trois hôtes), puis relevé de l'hôte de coinbase sans
   `ts` (dernier de son hôte) : date min = max = A, « 2 / 3 hôtes du pool », ligne « sans ts » = 1 et l'hôte ; avant
   l'entrée malformée, la ligne dit 0 ; les trois hôtes sans `ts` : date « non mesurée (… retenu daté) », ligne = 3
   et les trois hôtes triés.
5. Même fixture avec la plage `PLAGE` : refus nommé (`ValueError`, motif `asn_attribution sans ts : placement …
   indécidable`), jamais `KeyError`.

Échec avant (code B0, tests B1 ajoutés : `preuves/B1-avant.out`) : `FAILED (failures=1, errors=4)` — tests 4 et 5
`KeyError: 'ts'` ; tests 1 et 3 `UnicodeDecodeError` (0xC3, unexpected end of data) ; test 2 : le refus actuel est
une `UnicodeDecodeError` anonyme, le motif nommé n'y est pas. Succès après : `Ran 5 tests … OK`.

Équivalence du lecteur (`equivalence_lecteur.py`, `preuves/B1-equivalence-lecteur.out`) : sur 3 066 fichiers
entièrement décodables (banc construit : séparateurs LF, CRLF, CR, lignes blanches ASCII et Unicode, BOM, ligne
tronquée finale, ligne corrompue au milieu ; plus 3 000 tirages à graine fixe), lecteur de `34e096f` et lecteur B1
rendent les mêmes objets, le même texte sur stderr et la même exception (type et message) : **0 écart**. La seule
différence de comportement porte donc sur les lignes non décodables (décision du G0).

### 3.3 Mutants (`mutants_b1.py`, `preuves/B1-mutants.out`) : 12 tués sur 12

M1 fichier décodé d'un bloc (tests 1, 2, 3) ; M2 ligne finale non décodable refusée (1, 3) ; M3 non décodable tolérée
hors fin (2) ; M4 découpe sur LF seul (1) ; M5 ligne blanche jugée sur les octets (1) ; M6 refus non décodable sous le
message JSON (2) ; M7 `ts` indexé au bloc 6 (4) ; M8 relevés sans `ts` comptés dans la date (4) ; M9 compte « sans
ts » = tous les retenus (4) ; M10 « daté » omis (4) ; M11 garde de `filtre_horodatage` retirée (5) ; M12 ligne non
imprimée (4 et les deux épingles). Un premier M9 (`len(hs) − len(ts)`) était équivalent par construction ; remplacé.

### 3.4 Rendus, épingles, règle, suite, taille

- Re-capture (la ligne neuve est imprimée dans tout rendu) : rendus « avant » de l'arbre B0 = épingles en vigueur
  (`c4f45f47…`, `d0f785eb…`) ; diff textuel complet avant/après (`rendus/rendu-B1-sans_option.diff` `181a5771…`,
  `rendus/rendu-B1-avec_option.diff` `d6e1b416…`) : **une ligne insérée, aucune retirée**, dans chaque rendu, au
  bloc 6, après la ligne de date :
  `  relevés asn_attribution retenus sans ts (hôtes du pool, entrée malformée) = 0 — comptés à part, hors date de la
  partition (SHOGEN-BLOC6-TS-1)`.
  Nouvelles épingles : `SHA_BASE_SANS_OPTION` = `37dfcacba647c8c1184ba3897787cdb1b4a6f0678c96d9b3adc9ca38f0c00a96`
  (`tests/test_exclusion.py`), `SHA_BASE_AVEC_OPTION` =
  `7b6059f577e35c92813bdddfc1565730c026f29b62d606e3b78f9e49ae0dbf90` (`tests/test_pool_analyse.py`), historiques de
  commentaire complétés (« avant c4f45f47…6a5d144 », « avant d0f785eb…fe5eeb0 »). Avant re-capture, la suite
  échouait sur ces deux tests seulement (`FAILED (failures=2, skipped=2)`, 326 tests).
- Règle : 16 entrées, `ea3a2d94…`, identique à l'octet.
- Suite : `Ran 326 tests in 26.301s`, `OK (skipped=2)` (321 + 5).
- Numstat : records.py +17 −12 ; report.py +8 −4 ; tests/test_exclusion.py +3 −2 ; tests/test_lecteur.py +101 −0 ;
  tests/test_pool_analyse.py +3 −2 ; total +132 −20 = **152 lignes**.

## 4. B2 — lecteur et oracle de `raw.jsonl` (SHOGEN-RAW-LECTEUR-1)

### 4.1 Construction

`records.verifier_raw(raw_path, journal_path)` : relecture de `raw.jsonl` par `read_jsonl_tolerant` (`parse_float =
Decimal`, comme `parse_journal`) ; `raw_b64` décodé en base64 strict (`validate=True`) ; sha256 recalculé égal à
`sha256_raw` de la ligne, sinon refus ; correspondance avec `journal.jsonl` (même lecteur) par la clé
(`window_start`, `flux_id`, `fetch_ts`) et le sha, multiplicités comprises (`Counter`) ; écarts nommés dans cet
ordre : sha des octets ≠ `sha256_raw` de `journal.jsonl`, lecture(s) de `raw.jsonl` absente(s) de `journal.jsonl`,
lecture(s) de `journal.jsonl` absente(s) de `raw.jsonl` (cinq clés au plus dans le message) ; tout écart lève
`ValueError` marquée SHOGEN-RAW-LECTEUR-1. Rend `{"lectures": n, "avec_octets": m}`. Bibliothèque standard seule
(`base64`, `hashlib`, `collections.Counter`) ; aucune dépendance neuve.

### 4.2 Tests (`tests/test_lecteur.py`, classe `TestRawLecteur`)

Fixture : `build_fixture` de `test_exclusion` (campagne w0-w5 puis reprise w1-w3, 3 flux, octets gelés), soit
(6 + 3) × 3 = 27 lectures, toutes à octets (recompté : 27 lignes dans chaque fichier, aucun `raw_b64` nul ; les 27
lignes des deux fichiers ont mêmes clé et sha, rang à rang ; la reprise duplique clé et sha de trois lectures,
même `fetch_ts`, d'où l'intérêt des multiplicités).

1. `test_conforme` : `{"lectures": 27, "avec_octets": 27}`.
2. `test_ecarts_refus_nommes`, sept cas sur copie réécrite objet par objet, première lecture altérée : b64 valide
   mais autres octets ; b64 invalide (« ! » ajouté) ; `sha256_raw` de la ligne mis à 64 zéros ; `sha256_raw` de
   `journal.jsonl` mis à 64 zéros ; lecture retirée de `raw.jsonl` ; lecture retirée de `journal.jsonl` ;
   `fetch_ts` + 1 dans `raw.jsonl`. Messages obtenus (`preuves/B2-messages.out`) : `sha256 recalculé 5ee7724e… ≠
   sha256_raw de la ligne 3460af70…` ; `raw_b64 non décodable (base64 strict)` ; `sha256 recalculé 3460af70… ≠
   sha256_raw de la ligne 000…` ; `sha256 des octets ≠ sha256_raw de journal.jsonl` ; `lecture(s) de journal.jsonl
   absente(s) de raw.jsonl` ; `lecture(s) de raw.jsonl absente(s) de journal.jsonl` (deux fois), chacun avec la clé.

Échec avant (code B1, tests B2 ajoutés : `preuves/B2-avant.out`) : `FAILED (errors=8)`, `AttributeError: module
'shogen_s2.records' has no attribute 'verifier_raw'` (le lecteur n'existait pas). Succès après : `Ran 2 tests … OK`.

### 4.3 Mutants (`mutants_b2.py`, `preuves/B2-mutants.out`) : 9 tués sur 9

N1 base64 non strict ; N2 sha de la ligne non contrôlé ; N3 correspondance avec `journal.jsonl` retirée ; N4 clé
sans `fetch_ts` ; N5 côtés d'absence inversés ; N6 sha pris sur le texte base64 (tue aussi le cas conforme) ; N7
écart de sha nommé absence ; N8 compte `avec_octets` faux ; N9 multiplicités ignorées (tué par le cas conforme :
reprise dupliquée).

### 4.4 Règle, rendus, suite, taille

- Règle : `ea3a2d94…`, identique à l'octet ; rendus épinglés égaux à ceux de B1 (`37dfcacb…`, `7b6059f5…`).
- Suite : `Ran 328 tests in 25.892s`, `OK (skipped=2)` (326 + 2).
- Numstat : records.py +32 −0 ; tests/test_lecteur.py +51 −1 ; total +83 −1 = **84 lignes**.

## 5. Empreintes

- Diffs (étiquettes `a/s2-harness/…`, `b/s2-harness/…`, sans opération git) : `B0.diff`
  `d1223ed26b6a72db936983e4eb9ffba1da7f586e77bc61c9224d3ba717f322eb` (par rapport à `34e096f`) ; `B1.diff`
  `f07d845bbbc380b5ddfb8623b57e59bd7c3129c7a28f8759eff137b762c47cb1` (par rapport à l'arbre B0) ; `B2.diff`
  `c577a3f55f410db7479f80d10f1c8320df53285f1f3e96b52dfcc478aa2638de` (par rapport à l'arbre B1). Contrôle : export de
  `34e096f` par `git archive`, `patch -p1` de B0 puis B1 puis B2, `diff -r` avec l'arbre de travail : identique.
- Fichiers finaux : `shogen_s2/r1.py` `5ac7819f…` ; `lm.py` `1a815ede…` ; `r2.py` `316337c0…` ; `report.py`
  `da4d2b24…` ; `records.py` `ef457e41…` ; `tests/test_contexte_decimal.py` `bbe821c3…` ; `tests/test_lecteur.py`
  `0682dda0…` ; `tests/test_exclusion.py` `3e42b797…` ; `tests/test_pool_analyse.py` `e326fe48…`.
- Preuves (`lot-B/preuves/`) : `B0-avant.out` `6b3f4e3d…`, `B0-mutants.out` `20096530…`, `B0-temoins.out`
  `f1b56be1…`, `B0-sonde-ambiant.out` `9168955e…`, `oracle_b0.out` `e2d6167e…`, `B1-avant.out` `c505e02d…`,
  `B1-mutants.out` `a6c4fd45…`, `B1-equivalence-lecteur.out` `d1b24456…`, `B2-avant.out` `e54dee95…`,
  `B2-mutants.out` `c93f90bb…`, `B2-messages.out` `2a1ed662…` ; JSON de la règle (`regle/HEAD.json`, `B0`, `B1`,
  `B2`) : tous `ea3a2d94…`.
- `git status` final : modifiés r1, lm, r2, records, report, test_exclusion, test_pool_analyse ; neufs
  test_contexte_decimal, test_lecteur, et ce journal.
- Fin de travail : suite `Ran 328 tests in 26.514s`, `OK (skipped=2)` ; `cargo --locked xtask verify` avec ce journal
  dans `docs/` : `=== VERDICT GLOBAL : VERT ===`, rc 0 (S-G4 : 74 fichiers examinés sur 74 ; S-G5 : 75 sur 75, corpus
  complet, 125 artefacts sur 125, 252 fragments contrôlés, 0 violation ; `preuves/verify-final.out`).

## 6. Écarts au G0

- **E1 (B0, lieu)** : le contexte nommé vit dans `r1.py` (`r1.CONTEXTE_DECIMAL`, à côté de `DECIMAL_PREC`), pas dans
  un module neuf : la frontière D6 (i) reste celle des modules déjà nommés.
- **E2 (B0, serrage)** : outre prec, rounding, Emin, Emax, traps et clamp, `capitals = 1` et `flags = []` sont aussi
  fixés : sans eux, `Context()` les copierait du `DefaultContext` (mutable).
- **E3 (B0, serrage)** : tests au-delà du « rendu J2 et sorties de la règle » : rendu J2 avec une plage (seul chemin
  du site de `report.py`) et 24 cas par site (le rendu J2 seul laisse 16 mutants de site vivants, §2.1).
- **E4 (B1, extension de « jamais KeyError »)** : le G0 nomme le bloc 6 ; sous un filtre, la `KeyError` venait de
  `filtre_horodatage` (sonde P4 du lot B). Elle devient un refus nommé (`ValueError`, fail-closed) : un relevé sans
  horodatage ne se place ni dans ni hors d'une plage. Ni tolérance neuve ni affaiblissement : le refus existait, il
  est nommé (question Q2).
- **E5 (B1)** : libellé « non mesurée (… retenu daté) » quand tous les relevés retenus du pool sont sans `ts`, pour ne
  pas imprimer un énoncé faux ; inchangé sinon (rendus épinglés : seule l'insertion de la ligne neuve).
- **E6 (B2)** : la correspondance est faite par clé (`window_start`, `flux_id`, `fetch_ts`) et multiplicité, non par
  rang de ligne ; le premier type d'écart rencontré est nommé, avec au plus cinq clés.
- **E7 (taille)** : B0 atteint exactement 200 lignes (code et tests) après compactage des docstrings de son test ;
  pas de coupe en B0a et B0b.

## 7. Limites rencontrées (items à former, règle PAROXYSME)

- **L1 — écriture d'un Decimal hors contexte nommé (`capitals`)** : `str()` et `_fmt_dec` suivent le `capitals` du
  contexte ambiant ; `_fmt_dec(Decimal("2E-75"))` rend `2e-75` sous `capitals = 0` (`preuves/B0-sonde-ambiant.out`).
  Aucun rendu testé ne change (J2 et les fixtures épinglées n'impriment aucune notation exponentielle, sonde §2.1),
  mais le texte rendu reste dépendant du contexte de l'appelant pour toute valeur en notation exponentielle.
  Construction proposée : `_fmt_dec` écrit sous `CONTEXTE_DECIMAL` (≈ 3 lignes et un test, avec re-capture si un
  rendu change) [inféré]. Non fait ici : B0 était au plafond de 200 lignes, et la décision du G0 ne vise que les
  `localcontext`.
- **L2 — `closure.py`** (quarantaine, D6 (i) et (vi)) : son `localcontext()` copie toujours le contexte de
  l'appelant (précision seule fixée). Hors du chemin de recalcul ; déclencheur naturel : tout G0 qui promeut la
  collecte.
- **L3 — mutant équivalent** : le `localcontext` de `compute_r1` autour de `degenere` ne contient que des égalités ;
  le contexte nommé y est sans effet (site gardé par la décision « tous les localcontext »).
- **L4 — assiette de la ligne « sans ts »** : relevés retenus (dernier par hôte, après filtre) des hôtes du pool ; un
  relevé sans `ts` d'un hôte hors pool, ou remplacé par un relevé daté plus récent, n'est pas compté. Un `ts` présent
  mais non numérique n'est pas traité (autre malformation, hors item).
- **L5 — sévérité de l'oracle raw face au lecteur tolérant** : une dernière ligne de `raw.jsonl` tronquée (ignorée par
  le lecteur) ou un arrêt entre les deux `append_jsonl` du collecteur (lecture écrite au journal, pas à raw) donnent
  le refus « lecture(s) de journal.jsonl absente(s) de raw.jsonl ». Conforme à « tout écart = refus nommé » ; le
  verdict sur les journaux scellés n'est pas connu (D.4 a, D.2) : un refus à l'exécution unique serait une déviation
  à déclarer (question Q3).
- **L6 — décodage des prix depuis les octets** : l'oracle recalcule le sha256 des octets ; il ne redécode pas le prix
  à partir des octets (parseurs de `sources`, en quarantaine). La promesse de `journal.py` (« le DÉCODAGE lui-même
  est recalculable ») n'est tenue que pour l'intégrité des octets (question Q4).
- **L7 — branchement** : `verifier_raw` n'a pas encore d'appelant hors de ses tests (ni rendu, ni outil) ; son
  consommateur (enregistreur d'oracle B4, exécution unique C) reste à fixer (question Q5).
- **L8 — mémoire** : le lecteur charge le fichier entier (comme avant B1) ; sur un `raw.jsonl` de campagne (octets
  base64 de chaque lecture), la mémoire croît avec la taille du fichier, non mesurée (D.4 a) [inféré].
- **L9 — contexte nommé mutable** : `r1.CONTEXTE_DECIMAL` est un objet `Context` modifiable ; une affectation à l'un de
  ses attributs toucherait les 28 sites. Aucun code ne le modifie ; le test 1 du §2.3 fige ses valeurs.

Constat sans dette : avec un contexte ambiant où InvalidOperation n'est pas piégé, l'arbre `34e096f` rendait un
journal dont un prix vaut `abc` (le NaN circulait en silence) ; après B0, le rendu refuse (`InvalidOperation`
levée dans le contexte nommé), `preuves/B0-sonde-ambiant.out`.

## 8. Questions ouvertes

- **Q1** (L1) : l'écriture des Decimal sous le contexte nommé (`capitals`) entre-t-elle dans un sous-lot de l'étape
  B, ou en item daté ?
- **Q2** (E4) : le refus nommé sous filtre d'un enregistrement sans horodatage est-il la conduite voulue, plutôt qu'un
  compte à part qui le laisserait hors segment ?
- **Q3** (L5) : l'oracle raw reste-t-il strict sur une lecture finale sans contrepartie (arrêt entre les deux
  écritures, dernière ligne tronquée), ou faut-il une tolérance déclarée pour la seule lecture finale orpheline (un
  desserrage, donc une décision) ?
- **Q4** (L6) : la clôture de SHOGEN-RAW-LECTEUR-1 exige-t-elle aussi le redécodage des prix depuis les octets
  (parseurs de `sources`, en quarantaine), ou l'oracle sha256 suffit-il ?
- **Q5** (L7) : qui appelle `verifier_raw` : l'enregistreur d'oracle (B4), le script d'exécution unique (C), une ligne
  du bloc 1 ?
