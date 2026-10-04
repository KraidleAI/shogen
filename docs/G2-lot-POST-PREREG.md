# G2 — relecture du lot POST-PREREG (réviseur neuf)

- Ouverture : 2026-10-04 06:01:57 UTC (lue par `date -u`).
- Gate 0 : modèle `claude-opus-5-5` (Opus 5.5), effort `max` ; préfixe attendu conforme.
- Brief : `BRIEF-G2-POST-PREREG.md`, sha256 fb056b65172ef1d329e222a0e88a5dac0a38c6ac71b325573b9feb44da06b240 (vérifié).
- Dépôt : `/home/user/shogen`, branche `partie-4-execution`, tête 3e275a2b2466245375041612c6d83b9ef2aafc10.
- Réviseur ≠ générateur : je n'ai rien écrit de ce lot.

## Journal (au fil de l'eau)

- 06:01:57 : brief lu, sha256 vérifié égal.
- 06:02-06:03 : lus [lu] `docs/adr-0028/G0-lots-DETTES.md` (entier), `AVIS-SEUIL-FLUX-QUASI-MORT.md` (entier),
  `ANNEXE-B-items.md` l.98-103, l.224, l.547-558, l.643, l.684-686, `ANNEXE-D-preenregistrement.md` l.32-48 (liste D.2,
  sans ouvrir ses pièces) et l.124-211 ; brief du worker `BRIEF-POST-PREREG.md` (entier) ; journal G1 du worker (entier).
- 06:03:30 : copie `git archive HEAD | tar -x` (exclusions du brief) dans `G2-PP/arbre` à la tête 3e275a2.
  sha256 des 14 diffs recalculés : égaux au tableau §9 du G1.
- Contrôle (1) : `git apply --check` puis `git apply`, dans l'ordre 01 à 14, sur 3e275a2 : 14 OK.
- R-25 recompté (`grep -c '^+'` moins `+++`) : +144, +137, +157/−8, +89, +177, +42/−7, +129, +167/−2, +166/−3, +189,
  +144, +176, +75, +53 : tous ≤ 200 ; fichiers touchés : `scripts/post-s2/`, `docs/adr-0028/execution/post-prereg-2026-10-04/`,
  `docs/11-mesures-pilotes.md` seulement ; aucun fichier de `s2-harness`.
- Lus [lu] : `s2-harness/shogen_s2/r1.py` (entier), `records.py` (entier), `tools/rendu_unique.py` l.39-54 (portée J28 :
  t0 = 1787770800, n fixe = 38600, plage (1790273880, 1790435280), égale aux constantes de `commun.py` l.26),
  `r2.py` l.228-240, paquet l.112 (forme scellée = la règle, non le repli), bloc machine l.214-219.
- Rendu J28 : sha256 26877549…65c0 (recalculé) ; blocs repérés par `grep -n '^\[BLOC '` ; bloc 3 lu (l.435447-435538)
  seul ; blocs 1-2 (journal brut) non lus.
- 06:04:58 : `sha256sum -c` des trois journaux de la session contre le bloc machine (l.217-219) : control, journal, raw OK.
  Contenu jamais affiché.
- 06:06:16-06:14:51 : rejeu (script `G2-PP/rejeu.sh`, `env -u SHOGEN_S2_CAMPAGNE_CONTROL PYTHONDONTWRITEBYTECODE=1
  python3 -B`, trois à la fois ; sorties dans `G2-PP/rejeu/`, stdout et stderr en fichiers jamais affichés) : 9 codes 0,
  18 flux stdout/stderr de 0 octet. **Contrôle (3)** : `cmp` des neuf sorties contre celles des diffs 12-13 : 9
  IDENTIQUES ; `sha256sum -c SHA256SUMS` (livré) sur les sorties rejouées : 9 OK.
- Code relu en entier [lu] : `commun.py`, `sens_pool.py`, `poolee_bloc.py`, `hote_horloge.py`, `censure.py`,
  `sigma_indep.py`, `influence.py`, `contenu.py`, les 8 fichiers de tests et `fixtures.py`. Attendus des tests recomptés à
  la main (tous exacts) : P̂_more = 2/9 ; K = 49 (QUASI-MORT, fenêtres 51-99) ; 9/√9 = 3 ; σ̂² = 20/32 = 0,625 = γ̂₀ + γ̂₁ ;
  IF = (1/6, 1/6, −1/3, 0, 0, 0), Σ IF² = 1/6, σ̂²_IF,bloc = 5/36 ; runs E = 17/16, V = 147/256 ; loi de m (2, 3, 1) ;
  Pearson ρ = 0,8, IF ±0,36, Var̂_0 = 0,0324, Var̂_bloc = 0,0243, N_eff = 25/3, N_eff,0 = 7 ; écarts a = 9, c = 6, d = 2.
- Dérivations refaites à la main (CENSURE-INFO-2) : z' décroît en P sur ]0 ; 1[ pour tout K' ∈ [0 ; n'] (signe de
  P(1 − 2x) + x > 0, x = K'/n') ; ∂P_more/∂p_i = P(exactement un écart parmi les autres) ≥ 0 ; ∂²P/∂p_i∂p_j =
  Π_{l≠i,j}(1 − p_l)·[1 − Σ_{k≠i,j} p_k/(1 − p_k)] : concavité le long des transferts sous la condition, qu'assure
  Σe + 3c + max e ≤ n' (borne (Σe + 2c)/(n' − max e − c)) ; argument de sommet par transferts successifs (une seule
  coordonnée fractionnaire impossible car Σa = 2c) ; borne basse : P ≤ P(e + c·1) + (s − c)/n' (gradient ≤ 1/n').
  Construction conforme à l'annexe B l.102.
- 06:16-06:17 : sorties rejouées lues (comptes et statistiques ; aucune ligne de journal). **Contrôle (4)** : lignes 7-8
  des neuf sorties, (n, K, P̂_more) recomptés = bloc 3 du J28, chaîne pour chaîne, « égaux » dans les deux strates ;
  QUASI-MORT : n_s − ok_windows = colonne « panne » du bloc 3 pour les 22 couples ; DEVIANT : écarts = colonne « écart » ;
  SIGMA-INDEP : 24585·11 = 270435 et 11397·11 = 125367 cellules ; loi de m_t : Σ observés = n, Σ_{m≥2} = K (154, 133).
- Recoupement HOST avec ADR-0028 l.58-60 : (1550 − 815)/(45030 − 5313) = 735/39717 = 1,85 % ; 815/5313 = 15,3 %.
- 06:17:03-06:17:38 : recalculs indépendants (`G2-PP/indep/recalc_publies.py`, mon code, Fraction et entiers, entrées =
  bloc 3 du rendu lu par numéros de ligne) : z_pool,bloc = 2.60187760189464807987550108417… égal à la sortie (1e-40) ;
  24 attendus n·PB(m ; p̂) égaux ; CENSURE : condition de concavité vraie pour tout c ≤ s dans les deux strates
  (maximum exact), maximum (c = 4507, binance-bitstamp ; c = 1914, coingecko-defillama), borne basse, témoin « tout en
  écart » = borne, z_s de W_A et de W_B, pas s//c (300 ; 49) : tous égaux.
- CONTENU recompté depuis la sortie seule : 55 lignes « ρ̂ égaux au bloc 5 : oui » ; 110 calculs N_eff < N et
  SE_F < SE_bloc ; rapport SE_bloc/SE_F de 1,5027 à 15,0315 ; bloc 5 du rendu : 55 ρ̂ imprimés à 50 chiffres
  (binance×coinbase égal).
- 06:19:34 : suite post-s2 de base sur ma copie : `Ran 29 tests in 8.645s`, `OK`. 06:19-06:20:47 : suite `s2-harness`
  sur ma copie patchée : `Ran 398 tests in 63.263s`, `OK (skipped=2)` (= base du worker : inchangée).
- 06:20:24-06:21:51 : mes dix mutants (`G2-PP/mut/mutants_g2.py`, copie fraîche, substitution unique vérifiée, suite
  post-s2 ENTIÈRE) : 3 TUÉS (R5, R6, R7), 7 VIVANTS (R1, R2, R3, R4, R8, R9, R10) ; détail au §3.
- Datation du critère HOST : `etats/PP-d/scripts/post-s2/hote_horloge.py` (mtime 04:36:07, avant la 1re exécution
  04:59:41), sha256 1d19f833… = sha imprimé en tête de `sorties/v1/hote-degrade.txt` (05:05:59) ; diff avec le final :
  seulement `entrelaces` et sa ligne (C-2) ; corps v1 = corps final à cette ligne près. `sens_pool.py` 3475aeac…
  inchangé depuis 04:31:56. Corrections d'après exécution (diff PP-h → livré) : C-1, C-3, C-4 de présentation ou
  d'arrondi, C-2 descriptive ; aucune ne touche un critère. Limite : horodatages de fichiers, indices et non preuves ;
  l'heure 04:18:36 du §2 du G1 n'est pas vérifiable (fichier réécrit ensuite).
- Prémisse du rattachement HOST relue [lu] : `run_campaign.run_segment` (l.215-270) appelle `r2.collect_asn` avant
  `collector.collect`, qui écrit run_params puis clock_check « startup » (`collector.py` l.224-227) : la sonde d'un chunk
  précède son run_params, comme le dit la docstring.
- Registre doc 09 (`docs/09-vocabulaire.md`, entier [lu]) : grep des termes sensibles sur les 53 lignes du §11.1 :
  « significatifs » (chiffres), « indépendant » (code, paires de Fisher), « établir » (« sans l'établir »),
  « indépendance des sources » (« rien n'est dit ») : aucun emploi interdit.
- §9.3 de docs/11 (l.868-907 [lu]) : limite 12, 2e moitié = « σ̂²_bloc,s n'est recompté par aucun code distinct » ;
  pt 11 = sorties hors décision au-delà du seuil (même tournure « franchissent … là où le J28 ne le franchit pas »).
- (5) : étiquette mot pour mot en ligne 1, une seule fois, dans les 9 sorties (script) ; R-13 : `grep -rn -i
  "TODO|FIXME|XXX"` sur le code, les sorties et le §11.1 : 0 ; R-8 : imports = bibliothèque standard, harnais, modules
  du lot ; tests : `control.jsonl`/`journal.jsonl` seulement dans des `mkdtemp` (fixtures).
- 06:25:32-06:25:43 : `CARGO_TARGET_DIR=<copie de target/> cargo --locked xtask verify` sur ma copie patchée : rc 0,
  S-G1 à S-G8 « VERDICT : VERT (0 violation(s)) », `cargo fmt --check` VERT, no_std VERT, `clippy -D warnings` VERT,
  `=== VERDICT GLOBAL : VERT ===` ; S-G4 : 118 fichiers `docs/**/*.md` examinés (§11.1 et README des sorties compris) ;
  S-G5 en régime « corpus incomplet » ; 1 mention `docs/15|16` dans le journal, comptée, jamais affichée.
- 06:23-06:27 : non-équivalence des survivants montrée sur fixtures (`G2-PP/mut/demo_survivants.py`) : R1 (0.1 →
  0.1000000000000000055511…), R2 (strate « stress » refusée au lieu de 5 flux gardés), R3 (max 2,4407… < max énuméré
  2,5310…, argmax (0, 2) manqué), R4 (« retenues 5 ; retirées 2 » au lieu de « 4 ; 1 »), R10 (médiane 0,7 au lieu de 0,45).
- 06:28-06:30 : suite post-s2 après chaque diff de code sur une copie neuve de 3e275a2 : 4, 6, 9, 12, 15, 16, 19, 21,
  23, 27, 29 tests, OK à chaque pas (égal au G1 §3).
- 06:32 : constat (lecture seule, `git log`, `git diff --stat`, `git diff`) : pendant la relecture, la tête est passée à
  52b9b4e (lot DETTES-A et étude de marché : aucun changement de `s2-harness/shogen_s2`, `tools`, docs/11, du dossier
  des sorties ni de `scripts/post-s2`) ; l'arbre de travail du dépôt porte une modification **non commitée** de
  `s2-harness/shogen_s2/r1.py` et de `tests/test_prix_non_fini.py` (DETTES-B1 : `parse_journal` refuse désormais, quel
  que soit le statut, un prix illisible ou hors contexte, `PrixIllisible`, `PrixHorsContexte`). Ce n'est pas mon fait
  (aucune écriture de ma part dans le dépôt). Sur une copie neuve de 52b9b4e : 14 diffs OK, fichiers du lot identiques
  à ma copie de 3e275a2, `git diff --quiet f35a70c 52b9b4e -- s2-harness/shogen_s2 s2-harness/tools` vrai : le rejeu
  vaut pour 52b9b4e.

## 1. Verdict

**ACCEPTE-AVEC-CORRECTIONS** (liste fermée au §5 : C-1 à C-6). Les neuf sorties sont reproduites à l'octet ; les
constructions sont celles de l'annexe B, avec des choix du worker déclarés et codés avant la première exécution (§4) ;
chaque nombre du §11.1 est égal à une sortie. Les corrections portent sur trois trous de test (mutants vivants qui
changeraient des sorties en silence), sur deux précisions de texte du §11.1 (provenance des critères ; décompte des
statistiques au-delà de 2,33) et sur la version du harnais à nommer au README des sorties. Aucune correction ne touche
le code d'analyse ni les sorties : le rejeu reste valable (tête 3e275a2 et tête 52b9b4e, harnais = commit d'analyse).

## 2. Contrôles du brief

| n° | contrôle | résultat |
|---|---|---|
| 1 | diffs dans l'ordre sur la tête actuelle | 14 OK sur 3e275a2 (tête au départ) et sur 52b9b4e (tête à 06:32, copie neuve) ; sha256 des diffs = G1 §9 |
| 2 | constructions = annexe B | conformes ; choix du worker listés au §4 (HOST-DEGRADED-2 : forme du critère, clock_check écarté contre la lettre de l.100, codé avant l'exécution, après exposition au bloc 3) |
| 3 | rejeu sur les journaux scellés | journaux = bloc machine (sha256 -c OK) ; 9 sorties identiques à l'octet (`cmp`, `sha256sum -c`), rc 0, stderr vides ; aucun journal affiché |
| 4 | n, K, P̂_more = bloc 3 du J28 | égaux, chaîne pour chaîne, dans les 9 sorties (l.7-8) ; recoupements par flux (pannes, écarts) égaux |
| 5 | étiquette, aucune valeur des rendus remplacée | étiquette mot pour mot en l.1 des 9 sorties ; nouveau dossier ; diff 14 : +53/−0, aucun texte existant changé ; rendus non touchés |
| 6 | §11.1 | chaque nombre du tableau et de la prose (valeurs « ≈ » à 3 chiffres significatifs, comptes exacts, [calc]) contrôlé contre la sortie et la ligne citées : tous égaux, arrondis justes, renvois de lignes justes ; registre doc 09 respecté ; aucune lecture ne fait d'une analyse exploratoire un verdict ; z_pool,bloc et z_IF,bloc et la lecture « non identifié » rapportés avec leurs réserves ; deux précisions requises (C-4, C-5) |
| 7 | ≥ 6 mutants à moi | 10 mutants (R1-R10) : 3 tués, 7 vivants dont 5 non équivalents démontrés (§3) |
| 8 | R-25, R-13, R-8, verify, s2-harness | ≤ 189 lignes ajoutées par diff ; 0 TODO/FIXME ; stdlib seule ; `cargo --locked xtask verify` VERT ; `s2-harness` 398 OK (skipped=2), aucun fichier touché |

## 3. Mutants du réviseur (suite post-s2 entière, copie fraîche par mutant ; `mut/mutants-g2.log`)

| id | mutation | verdict | portée |
|---|---|---|---|
| R1 | HORLOGE : `Decimal(repr(x))` → `Decimal(x)` | VIVANT | non équivalent (valeurs binaires longues) ; le test n'emploie que des flottants dyadiques → C-3 |
| R2 | QUASI-MORT/DEVIANT : critère contre le n du segment au lieu de n_s | VIVANT | non équivalent (stress refusé) ; fixtures à une seule strate ; AVIS §1 pt 5 « par strate » non épinglé → C-1 |
| R3 | CENSURE : sommets limités aux paires voisines | VIVANT | non équivalent (max sous le max énuméré) ; test à 3 flux où la paire optimale est voisine ; au J28 calme l'argmax (binance, bitstamp) n'est pas voisin → C-2 |
| R4 | HOST : n retenu sans dédoublonnage (ligne « retirées ») | VIVANT | non équivalent sur fixture ; sur le J28 la valeur imprimée (24585, 11397) est égale au bloc 3 → remarque |
| R5 | HOST : `any` → `all` (sonde) | TUÉ | 2 tests |
| R6 | RUNS : μ sans (1 − p) | TUÉ | `test_runs_a_la_main` |
| R7 | CONTENU : s_xx par N − 1 | TUÉ | `test_influence_de_pearson_a_la_main` |
| R8 | CENSURE : « non identifié » dès qu'un W_B existe | VIVANT | équivalent sur le J28 (W_A = FAUX) ; cas « W_A déjà VRAI » non testé → remarque |
| R9 | SIGMA-INDEP : staleness au début de fenêtre | VIVANT | aucune cellule de fixture dans la bande ; sur journaux réels l'écart se verrait en « désaccords » > 0 → remarque |
| R10 | HORLOGE : médiane haute | VIVANT | non équivalent (compte pair : 3 610 au J28) ; test à compte impair → C-3 |

## 4. Choix du worker non écrits à l'annexe B (contrôle 2), et datation

- **HOST-DEGRADED-2** (l.100 ne fixe que le principe) : démarrage = groupe ouvert par run_params (ou clock_check
  « startup » qui n'en suit pas un sans marqueur) ; relevés ASN rattachés au démarrage suivant (prémisse vérifiée dans le
  harnais) ; dégradé = au moins un `resolve_failed`, tout hôte ; fenêtre retirée si le démarrage de son dernier marqueur
  est dégradé ; D1 réappliqué ; **clock_check exclu** alors que l.100 le nomme : motif écrit (ses signaux dépendent des
  sources qui répondent, ce que la même ligne interdit), déclaré (E-3). Codé avant la première exécution
  (`etats/PP-d`, 04:36:07 ; sortie v1 produite par ce code, sha 1d19f833…), après exposition au bloc 3 et à docs/11.
  Le §11.1 ne dit pas que cette forme est un choix du worker → C-4.
- **FLUX-DEVIANT-1** (l.556 sans seuil) : p̂_f > 1/2 strict = valeur de la variante V2 de l'avis, appliquée par le
  worker ; égalité : reste ; une passe. Codé à 04:31:56 (inchangé depuis), après exposition au bloc 3, qui montre
  p̂ maximal ≈ 0,0198 : le « aucun retrait » était prévisible. Le §11.1 l'attribue à « l'avis d'un auteur sans
  exposition » → C-4.
- POOLEE-BLOC-1 (a) : condition de publication (z_pool publié et z_bloc publié dans chaque strate) ; « forme à fixer
  au G0 » : non fixée au G0 DETTES, forme de B.13 prise telle quelle.
- CENSURE-INFO-2 : algorithme exact (sommets « deux flux à c », borne par gradient), famille et placement des témoins
  W_B, lecture (« non identifié » par deux témoins ; jamais « identifié ») ; attribution « type Manski » [inféré].
  Validité vérifiée à la main et par recalcul indépendant.
- DEP-FENETRES-2 (c) : runs à tolérance 0 sous loi nulle iid à P̂_more. CONTENU-DEP-1 : IF de Pearson [inféré, forme
  classique], N_eff = 3 + (1 − ρ̂²)²/Var̂_bloc, SE de Fisher (1 − ρ̂²)/√(N − 3). SIGMA-BLOC-INDEP-1 : indépendance limitée
  à la classification et à la variance (lecteurs communs, déclaré). HORLOGE-ETENDUE-1 : étendue des `median_offset`,
  conforme au paquet §12 pt 17 (« écarts médians »).
- Datation : tous les fichiers de code de l'état PP-h (04:58:57) précèdent la première exécution (04:59:41) ; les seuls
  changements ultérieurs sont C-1 à C-4 du G1 (aucun critère). Indices par horodatage de fichiers, pas preuves.

## 5. Corrections requises (liste fermée)

- **C-1** (diff 03, test) : ajouter à `test_sens_pool.py` un cas à deux strates, par exemple 100 fenêtres calmes et 20
  de stress, e en panne dans 5 des 20 fenêtres de stress : attendu à la main, pools {calme : a-e, stress : a-e}, aucun
  refus (2·15 ≥ 20 ; avec le n du segment, 120, e serait retiré et la strate refusée). Le mutant R2 doit être tué.
- **C-2** (diff 07 ou 08, test) : ajouter à `test_censure.py` le cas `bornes(40, 1, [4, 1, 2], 2)`, maximum égal à celui
  de l'énumération exhaustive (2,5310041009605653…, sommet c = 2, paire (0, 2), non voisine). Le mutant R3 doit être tué.
- **C-3** (diff 05 ou 06, test) : ajouter à `test_hote_horloge.py` des offsets non dyadiques en nombre pair, par exemple
  0.1, 0.2, 0.7, 1.3 : attendus minimum 0.1, médiane 0.45, maximum 1.3, étendue 1.2 (Decimal exacts). Les mutants R1 et
  R10 doivent être tués.
- **C-4** (diff 14, texte du §11.1, 1er paragraphe) : remplacer « Les seuils de FLUX-QUASI-MORT-1 et de FLUX-DEVIANT-1
  viennent de l'avis d'un auteur sans exposition (annexe B.39) ; les constructions viennent de l'annexe B, écrite avant
  l'exécution ; les choix propres du worker sont nommés dans le journal G1. » par un texte de ce sens : « Le seuil de
  FLUX-QUASI-MORT-1 vient de l'avis d'un auteur sans exposition (annexe B.39) ; celui de FLUX-DEVIANT-1 (p̂_f > 1/2) est la
  valeur de la variante V2 du même avis, appliquée par le worker. Les constructions viennent de l'annexe B, écrite avant
  l'exécution, sauf la forme du critère de HOST-DEGRADED-2 (sonde ASN du démarrage, dernier marqueur, `clock_check` hors
  critère), choix du worker non écrit à l'annexe. Ces choix du worker sont fixés avant l'exécution, après l'exposition
  déclarée ci-dessus, et nommés dans le journal G1. »
- **C-5** (diff 14, texte du §11.1, « Ce qu'elles ne permettent pas de dire ») : « Deux statistiques exploratoires
  franchissent 2,33 là où la règle ne le fait pas » → « Deux statistiques exploratoires à erreur-type par blocs
  franchissent 2,33 là où z_bloc,s ne le fait pas ». Motif : z_s franchit 2,33 dans les deux strates (20,8 ; 28,5), et
  d'autres statistiques exploratoires du lot le franchissent aussi, sous des lois nulles sans dépendance sérielle
  (z_R ≈ 14,8 et 27,8, au tableau ; z_IF,0 ≈ 11,1 et 12,2) ; le décompte « deux » n'est juste qu'avec ce qualificatif.

- **C-6** (diff 12, README des sorties) : nommer la version du harnais que les scripts importent (commit d'analyse
  `f35a70c`, `s2-harness/shogen_s2` et `s2-harness/tools` identiques à 3e275a2 et à 52b9b4e) et dire qu'un rejeu se fait
  à cette version. Motif : les en-têtes des sorties portent le sha des scripts et de `commun.py`, pas celui des modules
  du harnais (`r1`, `records`, `window`, `r2`) dont dépendent toutes les valeurs ; le lot DETTES-B1, en cours
  d'application, modifie `r1.parse_journal`.

Après correction : rejouer la suite post-s2 et les mutants R1, R2, R3, R10 (tués) ; R-25 tenu (diffs 03 : 157, 05 : 177,
06 : 42, 07 : 129, 08 : 167, 12 : 176, 14 : 53 lignes ajoutées avant correction) ; aucune sortie à refaire (les en-têtes portent le
sha des scripts, pas des tests).

## 6. Actes de l'orchestrateur (hors corrections du lot)

- Q-1 du worker : la fermeture de SHOGEN-HOST-DEGRADED-2 dépend de l'adjudication du critère (la l.100 nomme
  `clock_check`). Si elle est adjugée, l'amendement daté de l'annexe B doit dire que la forme a été fixée par le worker
  avant l'exécution, après exposition au bloc 3 et à docs/11.
- Q-3 : je n'y vois pas de surclamation dans le §11.1 ; le signalement à l'investisseur relève de l'orchestrateur.
- Verser le journal G1 du worker et citer son chemin au §11.1 (le texte y renvoie ; il n'est pas au dépôt).
- Interaction avec DETTES-B1 (non commité à 06:32) : après son commit, `r1.parse_journal` refuse tout prix illisible
  ou hors contexte, quel que soit le statut ; un rejeu des scripts POST-PREREG à cette tête donnera les mêmes sorties
  si les journaux n'en portent aucun, sinon un refus nommé. Je ne l'ai pas mesuré (cela exige de lire les journaux
  hors des scripts du lot). À trancher par l'orchestrateur : rejouer les neuf sorties après le commit de B1, ou consigner
  que le rejeu se fait au commit d'analyse (C-6). Item à former si non tranché : SHOGEN-PP-REJEU-B1-1.

## 7. Remarques non bloquantes

- Mutants vivants R4, R8, R9 (§3) : sans effet possible sur les sorties livrées (R4 recoupé par l'égalité au bloc 3,
  R8 équivalent sur le J28, R9 visible en « désaccords ») ; tests à renforcer quand les fichiers seront rouverts.
- Tableau du §11.1, ligne SIGMA : « code indépendant de r1 » ; la prose dit plus juste « distinct de r1, lecteurs
  communs mis à part ».
- Énoncés du texte validé devenus datés par l'ajout (§2.7 l.219-220 : étendue « ni par ce rapport » ; §9.3 pt 12 :
  « recompté par aucun code distinct ») : un renvoi daté au §11.1 éviterait une lecture contradictoire, sans réécrire.
- G1 §2 annonce pour HORLOGE une lecture `parse_float=Decimal` ; le code lit `Decimal(repr(float))` après
  `parse_control` : identique pour des flottants écrits par `json` de Python (repr le plus court) ; C-3 épingle le geste.
- Affirmations du G1 issues d'outils non livrés (« 766 marqueurs tous dans la plage D5 », « la lecture alternative ne
  change aucune fenêtre retirée ») : non vérifiées par moi [2nd] ; la ligne livrée « 74 ; 0 » est vérifiée (rejeu).

## 8. Limites et items à former (règle PAROXYSME)

- SHOGEN-POSTPREREG-PARAMS-SCEAU-1 (proposé) : les paramètres « fixés avant l'exécution » ne sont attestés que par des
  horodatages de fichiers et un journal réécrit ; pour tout lot d'après pré-enregistrement, épingler le sha256 des
  paramètres (ou du code) au JOURNAL avant de lancer sur les journaux.
- SHOGEN-FICHE-WORKER-POSTEXEC-1 (proposé) : la fiche `shogen-worker` dit « fixtures seulement (D.4 a) » sans
  l'exception d'après exécution que le G0 DETTES accorde à POST-PREREG ; le worker (E-7) et moi l'avons rencontrée.
- Lecteurs communs (première moitié de la limite 12 du §9.3) : à former s'il n'existe pas déjà un item d'un lecteur
  indépendant de `parse_journal` et `filtre_lecture`.
- Items proposés par le worker (G1 §8) : pertinents, je les appuie (ZIF-NIVEAU-1, CENSURE-ZBLOC-1, ENTRELACEMENT-D5-1,
  HOST-CRITERE-1 selon Q-1, PEARSON-IF-SOURCE-1).

## 9. Provenance (G1 du réviseur)

- Sources [lu] : G0 DETTES (entier) ; AVIS-SEUIL (entier) ; annexe B l.98-103, 224, 547-558, 643, 684-686 ; annexe D
  l.32-48 et 124-211 ; paquet l.112, 187, 205, 214-219 ; ADR-0028 l.58-60 ; docs/11 l.210-226, 868-907, 976-1050 (copie
  patchée) ; docs/09 (entier) ; r1.py, records.py (entiers) ; r2.py l.228-240, 433-545, 709-775, 1063-1100 ;
  window.py l.80-118 ; rendu_unique.py l.39-54 ; run_campaign.py l.215-270 ; collector.py (recherche) ; rendu J28
  bloc 3 (l.435447-435538) et une ligne du bloc 5 ; code et tests du lot (entiers) ; sorties rejouées (entières) ;
  G1, SECTION-11.md, mutants-final.log, brief du worker (entiers) ; états `etats/PP-d`, `PP-h` et `sorties/v1`
  (diffs et en-têtes). [abs] : P-05, P-08 (non versées) ; transcriptions ; pièces de D.2 (non ouvertes).
- Non ouverts : `docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`,
  `docs/adr-0028/monark-m009a/`, `JOURNAL.md`, blocs 1-2 du rendu, tout `*.jsonl` (lus par les scripts du lot seulement).
- Pièces du réviseur (`G2-PP/`, sha256) : `rejeu.sh` e95ee8cf…a6 ; `indep/recalc_publies.py` 3612edbf…53 ;
  `mut/mutants_g2.py` ce0aa223…cd ; `mut/mutants-g2.log` c37cc79b…65 ; `mut/demo_survivants.py` 20d1fa61…d9 ;
  sorties rejouées `rejeu/*.txt` (= SHA256SUMS livré).
- Pièces relues (sha256 recalculés) : brief G2 fb056b65…40 ; 14 diffs (= G1 §9) ; `SECTION-11.md` 6f74b6a7…47 ;
  `mutants-final.log` 475a2fd0…87 ; rendu J28 26877549…c0 ; journaux 351f51b2…ff, 98c5793e…74, 39ffb13f…5d.

## 10. Déviations et exposition du réviseur

- Règle 3 de ma fiche (« fixtures seulement ») contre le brief et le G0 DETTES (POST-PREREG : « lit les journaux
  scellés : oui ») : j'ai laissé les seuls scripts du lot lire la copie de session, sans `SHOGEN_S2_CAMPAGNE_CONTROL`,
  sans afficher aucun journal ; mes recalculs indépendants n'utilisent que des agrégats publiés (bloc 3) ; mes mutants
  et démonstrations ne tournent que sur fixtures.
- Exposition : j'ai lu le bloc 3 et une ligne du bloc 5 du J28, les sorties du lot et le §11 de docs/11 (valeurs de
  campagne publiées, après l'exécution) ; je n'ai fixé aucun paramètre d'analyse.
- Git : aucune écriture dans le dépôt (lectures seules : `status`, `log`, `diff`, `rev-parse`, `archive`) ; à 06:03, un
  `git init` dans ma copie `G2-PP/arbre` (hors dépôt), supprimé aussitôt (`rm -rf .git`) avant tout `git apply`.
- Clôture : 2026-10-04 06:33:50 UTC (`date -u`).
