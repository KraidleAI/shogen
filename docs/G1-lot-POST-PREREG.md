# Journal G1 — lot POST-PREREG (analyses ajoutées après le pré-enregistrement, hors décision)

Worker G1 `shogen-worker`. Gate 0 : modèle `claude-opus-5-5` (identifiant exact déclaré par la session), effort `max`.
Brief : `scratchpad/dettes/BRIEF-POST-PREREG.md`, sha256 `d8457caa359ba581bd1b451a3fd9529ef5c2a4c9504ca5f5083c13e7691e01c5` (recalculé : égal).
Début : 2026-10-04 03:59:35 UTC (date -u). Dépôt `/home/user/shogen`, branche `partie-4-execution`, tête `5afbdd2` (git rev-parse, relu).
Copie de travail : `git archive HEAD | tar -x` avec les exclusions du brief, dans `POST-PREREG/arbre`.

## 0. Chronologie (heures date -u)

- 2026-10-04 03:59:35 UTC : brief lu et vérifié ; dossier créé ; copie extraite.
- 2026-10-04 03:59:43-03:59:58 UTC : sha256 des trois journaux de `scratchpad/execution/journaux/` calculés (`sha256sum`, contenu jamais affiché) et comparés au bloc machine `shogen-paquet-v1` du paquet (§13, l.217-219) : control.jsonl `351f51b2…66ff`, journal.jsonl `98c5793e…d595d74`, raw.jsonl `39ffb13f…c15d` — **égaux** aux trois lignes.
- 2026-10-04 04:18:36 UTC : lectures de cadrage faites (liste au §1) ; **section §2 « paramètres fixés avant l'exécution » écrite à cette heure**, avant toute ligne de code et avant toute exécution sur les journaux.

## 1. Lectures (niveau [lu] = lu sur place ; [abs] = non détenu ou non lu ; [inféré] = dérivé ici)

- Brief `BRIEF-POST-PREREG.md` [lu, entier ; sha256 recalculé égal].
- `docs/adr-0028/G0-lots-DETTES.md` [lu, entier] ; `ETAT-REGISTRE-2026-10-04.md` [lu : l.1-100 ; lignes des items l.217-218,
  247-252, 291, 365, 367, 381, 387, 389] ; `ANNEXE-B-items.md` [lu : l.85-105 (B.6), l.214-230 (B.13), l.540-562 (B.38-B.39),
  l.601-613 (B.43), l.630-646 (B.44), l.664-687 (B.46)] ; `AVIS-SEUIL-FLUX-QUASI-MORT.md` [lu, entier] ;
  `ANNEXE-D-preenregistrement.md` [lu : l.1-48 (D.1, D.2), l.124-200 (D.4, D.5)] ; `PAQUET-PREREG-S2.md` [lu : en-têtes,
  l.81-92, l.174-240 dont le bloc machine l.213-222] ; `ADR-0028-decisions-sortie-S2.md` [lu : l.18-140] ;
  `docs/11-mesures-pilotes.md` [lu : l.1-330, l.413-680, l.746-1011] ; `docs/09-vocabulaire.md` [lu, entier] ;
  `docs/adr-0029/ADR-0029-campagne-S2-bis.md` [lu : l.60-110] ; `docs/adr-0028/execution/README.md` [lu : l.1-10] ;
  `scripts/controle/README.md` [lu : l.1-60] ; `scripts/sim/sim_niveau_oracle_r1.py` [lu : l.1-40].
- Rendu J28 `…943.3-j28.out` (sha256 `26877549…65c0`) [lu : en-têtes de blocs par grep ; bloc 3 l.435447-435538 ; bloc 5
  l.435671-435700] ; ni le bloc 1 ni le bloc 2 (journal brut fenêtre × source) n'ont été lus ; leur format a été pris
  dans `report.py`.
- Harnais [lu] : `r1.py`, `records.py`, `rendu_unique.py`, `window.py`, `journal.py` (entiers) ; `model.py` l.1-70 ;
  `collector.py` l.55-252 ; `run_campaign.py` l.200-300 ; `r2.py` l.60-80, l.213-246, l.300-400, l.425-545, l.703-772,
  l.1025-1098 ; `report.py` l.73-81, l.205-222, l.284-296 et recherches ; `tools/oracle_record.py` (définitions par
  recherche) ; `tests/test_pool_analyse.py` l.1-120. xtask [lu] : `main.rs` l.1-120, `lib.rs`, en-têtes des gates,
  `sg5.rs` l.1-120.
- `biblio/INDEX.md` [lu : recherches ; l.330-338]. Künsch 1989, *Annals of Statistics* 17(3) (`biblio/kunsch1989-aos-17-3-1217.pdf`,
  sha256 recalculé `6d069c52…3a64`, égal à l'INDEX) [lu sur le scan : p. 1219, Ex. 2.2 et (A1)-(A4) ; p. 1222, (2.14) ;
  OCR l.100-200, 296-345, 626-700].
- [abs] : Kiefer & Vogelsang 2005 (P-05) ; Horowitz-Manski, Little-Rubin (P-08) ; AVIS-advisor-defi (hors dépôt). [inféré] :
  fonction d'influence de Pearson (dérivée au journal, §2 ; contrôlée par le test à la main de PP-h) ; argument des
  sommets de CENSURE-INFO-2 (énoncé dans la docstring de `censure.py`, contrôlé par énumération exhaustive en test).
- Relecture avant remise (2026-10-04 05:45-05:55 UTC) : `s2-harness/shogen_s2/r2.py` l.312-345 [lu] (résolveur réel de
  la sonde ASN : DoH, RIPEstat, Cymru ; toute erreur réseau donne `resolve_failed`) ; `docs/11-mesures-pilotes.md`
  l.868-1000 [lu] (§9.3 à §11) ; `docs/08-assumptions.md` l.31 [lu, par recherche] (A(loss-non-informative)) ;
  `PAQUET-PREREG-S2.md` l.65 et l.200 [lu, par recherche] (§12 pt 12, Fisher) ; `git log` et `git diff` en lecture
  seule de `5afbdd2..3e275a2` : `ANNEXE-B-items.md` (B.47) [lu] ; `biblio/INDEX.md` [recherche seule, sur le diff].
- Non ouverts : `docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`,
  `docs/adr-0028/monark-m009a/`, `JOURNAL.md`, `PASSATION-CLOUD.md`, tout journal `*.jsonl` (lus par programme
  seulement, jamais affichés). Écarts : §6.

## 2. Paramètres et constructions fixés AVANT toute exécution sur les journaux (écrits le 2026-10-04 04:18:36 UTC)

Exposition déclarée au moment de fixer ces paramètres : j'ai lu le bloc 3 du rendu J28 (l.435447-435538 : n, K, p̂ par flux,
P̂_more, z, z_bloc, décomposition de K, bornes de censure) et `docs/11-mesures-pilotes.md` en entier (valeurs publiées). Je n'ai lu
ni le bloc 1 ni le bloc 2 du rendu J28 (le bloc 2 est le journal brut fenêtre × source), ni aucun journal. Les seuils de
QUASI-MORT-1 (1/2) et de FLUX-DEVIANT-1 (1/2, AVIS V2/L2) viennent de l'avis d'un auteur sans exposition (B.39) ; les
constructions viennent de l'annexe B (B.6, B.13, B.39, B.44, B.46), écrites avant l'exécution ; mes choix propres sont
marqués [choix G1] et sont donc postérieurs à l'exposition ci-dessus (analyses exploratoires, hors décision).

Commun à tout le lot :
- Portée : segment J28 du rendu (`rendu_unique.SORTIES` « j28 ») : t0 = 1787770800, n fixe = 38 600, plage D5 fermée
  [1790273880 ; 1790435280] exclue ; lecture par `records.parse_control`, `records.effective_run_params`,
  `window.verify_markers_against_spec`, `records.filtre_lecture`, `r1.parse_journal`, `records.sigma_tau_from_params`
  (mêmes appels que `r1.recompute_from_journal`) ; pool D1 par `r1.analysis_pools`.
- ℓ = `r1.ELL_BLOC` = 240 ; garde de blocs 30·ℓ ; seuil 2,33 (`r1.SEUIL_Z`) ; précision Decimal 50 (`r1.contexte_decimal`).
- Étiquette en première ligne de chaque sortie, mot pour mot : « ajoutée après le pré-enregistrement, hors décision ; ne change
  pas le verdict de la règle scellée (« R1 discrimine » = FAUX, docs/11 §3) ».
- Contrôle de cohérence dans chaque sortie : n, K, P̂_more par strate recomptés (`r1.compute_r1`) égaux, chaîne pour chaîne,
  au bloc 3 du rendu J28 ; sinon la sortie le dit et n'imprime aucune valeur d'analyse (fail-closed).

FLUX-QUASI-MORT-1 (+ QUASI-MORT-PREDICAT-1, POOL-MIN-1) : seuil de l'avis B.39, recopié : f retiré du pool de la strate s si
2·ok(f, s) < n_s ; ok(f, s) = `ok_windows` de `r1.compute_r1` (prédicat statut ok ET prix non nul, lectures last-wins de la
liste de `r1.parse_journal`, fenêtres retenues), 0 pour un flux retiré par D1 ; égalité : le flux reste (imprimée) ; une passe,
par strate ; recalcul `r1.compute_r1(pool_by_strate=…)` puis `r1.regle_critere` (pts 1-8 ; drapeau 2 non recalculé). Garde
POOL-MIN-1 : strate dont le pool réduit compte moins de `r1.N_MIN_HORSENV` = 4 flux : refus nommé, aucun z calculé pour elle,
pas de « R1 discrimine » recalculé.

FLUX-DEVIANT-1 : f retiré du pool D1 de la strate s si 2·écart(f, s) > n_s (p̂_f > 1/2 strict, AVIS V2/L2), écart = panne +
staleness + hors-enveloppe de `r1.compute_r1` sur le pool D1 ; une passe sans itération ; égalité : reste ; même garde
POOL-MIN-1 ; étiquette ajoutée : « exploratoire, conditionnée sur une composante du résultat (p̂_f) ».

POOLEE-BLOC-1 (a) : forme de B.13 : z_pool,bloc = Σ_s (K_s − n_s·P̂_more,s) / √(Σ_s σ̂²_bloc,s) sur les sorties scellées du J28 ;
publiée si la strate poolée publie z_pool (≥ 2 strates, z_s publiée dans chacune) ET si chaque strate publie z_bloc (σ̂² > 0,
n_s ≥ 7 200) [choix G1 : condition de publication calquée sur `r1.strate_poolee` et `r1.bloc_strate`] ; sinon motif.
Étiquette ajoutée : « exploratoire, hors famille, hors décision ; niveau non mesuré (POOLEE-BLOC-1 (b), lot DETTES-SIM) ».

HOST-DEGRADED-2 [choix G1 sur la forme ; principe de B.6 l.100] : démarrage = groupe ouvert par un `run_params` (ou par un
`clock_check` de phase « startup » qui n'en suit pas un), auquel se rattachent les relevés `asn_attribution` écrits depuis le
dernier marqueur du démarrage précédent (la sonde ASN de chaque chunk précède son `run_params`, `run_campaign.run_segment`) ;
un démarrage est « à diagnostic d'hôte dégradé » s'il porte au moins un `asn_attribution` de statut `resolve_failed` (tout
hôte). Une fenêtre retenue est retirée si le démarrage de son DERNIER marqueur (last-wins) est dégradé. Aucun paramètre
numérique. Le `clock_check` n'entre PAS au critère : ses seuls signaux de dégradation (« non évaluable », offset médian)
dépendent des sources du pool qui ont répondu à la sonde, donc d'un statut de source (exclu par B.6) ; écart au libellé
déclaré, ses comptes sont imprimés à côté. Recalcul : D1 (`r1.analysis_pools`) sur les fenêtres restantes, `compute_r1`,
`regle_critere`.

HORLOGE-ETENDUE-1 : relevés `clock_check` retenus par le filtre de lecture du J28 (segment, plage D5 sur `harness_ts`) ;
`median_offset` lu en Decimal exact (`records.read_jsonl_tolerant(parse_float=Decimal)`) ; imprimés : nombre (attendu 3 610),
non évaluables (médiane nulle), minimum, médiane (`r1._median`), maximum, étendue = max − min. Aucun seuil.

CENSURE-INFO-2 [construction B.6 l.102 ; algorithme choix G1] : par strate, pool D1 de N flux, n, K, écarts e_i (sealed
`compute_r1`), s = fenêtres sautées (`r1.fenetres_sautees`, comme le rendu). Imputation : chaque fenêtre censurée reçoit un vecteur
quelconque de {0,1}^N ; n' = n + s, e'_i = e_i + a_i, K' = K + c (c = fenêtres imputées à ≥ 2 écarts). z' calculé en entiers
exacts (P_more rationnel), Decimal 50 à la fin. (i) Maximum de z' : exact, sur c ∈ [0 ; s] et les 55 sommets « deux flux à c »
(argument : z' décroît en P̂ à K' fixé ; P_more croît en chaque a_i et est concave le long des transferts tant que
Σ_k x_k ≤ 1, x = p/(1−p), condition contrôlée pour chaque c ; sinon borne relâchée P ≥ P(e/n') et la sortie le dit).
(ii) Minimum : borne extérieure L = min_c f_c(P(e + c·1) + (s − c)/n') (gradient ∂P/∂a_i ≤ 1/n'), et témoin atteint
« toutes les fenêtres censurées avec les N flux en écart » ; égalité imprimée si la borne est serrée. (iii) Identification de la
valeur de la règle par témoins (z_bloc sur la série complétée aux positions censurées, `r1.block_long_run_variance`, puis
`r1.regle_critere`) : W_A = toutes les fenêtres censurées propres ; W_B = plus petit c ≥ 1 donnant REJETTE, c fenêtres
censurées imputées à deux écarts sur la paire qui minimise P̂_more à ce c, placées toutes les ⌊s/c⌋ positions censurées
(ordre du temps, à partir de la première) [choix G1]. Lecture : « non identifié sous censure arbitraire » si deux témoins
donnent des valeurs différentes ; « identifié » seulement si les bornes extérieures de z_s et de z_bloc sont du même côté
(z_bloc : aucune borne extérieure construite → jamais « identifié » par cette construction, limite déclarée). Attribution
« type Manski » [inféré : P-08 non versée].

SIGMA-BLOC-INDEP-1 [choix G1] : code indépendant de `r1` pour la classification (texte du rendu l.435448 : panne > staleness >
hors-enveloppe, σ et τ par classe, N ≥ 4 répondantes, médiane leave-one-out > 0, comparaison exacte |p − m| > τ·m) et pour la
variance (somme des carrés des sommes de blocs de c_t = n·I_t − K, série complétée par des 0 sur la grille, Σ_j B_j² / (ℓ·n²)) ;
lecture par `r1.parse_journal` et le filtre de lecture (lecteurs) ; comparaison chaîne pour chaîne à n, K, γ̂₀, σ̂²_bloc du rendu.

DEP-FENETRES-2 (b) = R1-PLUGIN-1 (a) : Künsch 1989 (2.14) p. 1222 avec IF empirique de f(Ī, p̂) = Ī − P_more(p̂) (Ex. 2.2 p. 1219) :
IF_t = (I_t − Ī) − Σ_i g_i (D_it − p̂_i), g_i = ∂P_more/∂p_i(p̂) ; σ̂²_IF,bloc = Σ_j B_j(IF)²/ℓ (Bartlett, ℓ = 240, grille, série
complétée par des 0, même échelle que σ̂²_bloc), σ̂²_IF,0 = Σ_t IF_t² ; z_IF = (K − n·P̂_more)/σ̂_IF ; entiers exacts puis
Decimal 50. Classification : `r1.classify_cells` par strate (pool D1).
DEP-FENETRES-2 (c) [choix G1, tolérance 0] : R = nombre de runs de I_t (définition de `r1.bloc_strate`), E[R] et Var[R] exacts
sous fenêtres iid de probabilité P̂_more (plug-in), z_R = (R − E R)/√Var R ; exploratoire.
DEP-FENETRES-2 (a) (fixed-b, Kiefer-Vogelsang, P-05) : non faite (source non détenue).
R1-PLUGIN-1 (b) : descriptif seulement, sans test ni p-valeur : comptes observés de m_t = 0..N contre n·PB(m ; p̂) exacts ;
le test (statistique et niveau à sourcer) reste une recherche.

CONTENU-DEP-1 [construction B.6 l.103] : pour chaque paire du pool R2 et pour ρ_raw et ρ_resid (séries de `r2.log_returns` et
des résidus leave-two-out de `r2.rho_resid`, recalculés et contrôlés égaux aux ρ du bloc 5), IF de Pearson
IF_t = x̃_t ỹ_t − (ρ/2)(x̃_t² + ỹ_t²) (dérivée ici de Ex. 2.2 [inféré]), Var̂_bloc(ρ̂) = Σ_j B_j(IF)²/(ℓ·N²) sur la grille
(ℓ = 240, Bartlett, complétée par des 0), SE de Fisher (1 − ρ̂²)/√(N − 3), N_eff = 3 + (1 − ρ̂²)²/Var̂_bloc(ρ̂) ;
imprimés par paire, plus le nombre de paires à N_eff < N_min = 300.
- 2026-10-04 04:19:36-04:20:48 UTC : bases de référence sur la copie non patchée : `cargo --locked xtask verify` (CARGO_TARGET_DIR
  copie de `target/` du dépôt) → `=== VERDICT GLOBAL : VERT ===`, exit 0 (S-G5 en régime « corpus incomplet » : `biblio/INDEX.md`
  seul copié, 0 artefact sur 155 déclarés, comme en CI) ; suite `s2-harness` (`env -u SHOGEN_S2_CAMPAGNE_CONTROL
  PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s tests -t .`) → `Ran 398 tests in 63.881s`, `OK (skipped=2)`.
- Contrôle git en lecture : `git diff --stat f35a70c..5afbdd2 -- s2-harness/shogen_s2 s2-harness/tools` vide : les lecteurs
  importés depuis la tête sont ceux du commit d'analyse du rendu.
- 2026-10-04 04:23-04:27 UTC, sous-lot **PP-a1** (commun, partie pure) : tests écrits d'abord ; rouge montré
  (`ModuleNotFoundError: No module named 'commun'`, 04:24:05) ; vert (4 tests) ; mutants (outil `outils/mut.py`, copie
  fraîche, une substitution) : M1 étiquette « §3 » → « §2 » ; M2 t0 + 60 ; M3 lecture « P̂_more » relâchée (ligne poolée
  lue) ; M4 contrôle qui ignore les écarts : 4/4 tués (ROUGE). Lecture du vrai bloc 3 du J28 par `lire_bloc3` : calme
  (24585, 154, `0.0013629504…903986`), stress (11397, 133, `0.0014663989…123928`), égaux au rendu.
- 2026-10-04 04:27-04:29 UTC, sous-lot **PP-a2** (commun : chargeur, CLI fail-closed, fixtures) : tests d'abord ; rouge
  (`AttributeError: module 'commun' has no attribute 'charger'` / `'executer'`, 04:28:04) ; vert (6 tests) ; mutants
  M5 segment oublié, M6 plage oubliée, M7 D1 oublié (pool complet), M8 écart non fermant, M9 étiquette hors tête :
  5/5 tués.
- 2026-10-04 04:29-04:32 UTC, sous-lot **PP-b** (QUASI-MORT-1, QUASI-MORT-PREDICAT-1, POOL-MIN-1, FLUX-DEVIANT-1) : fixtures
  étendues (source_ts, clés de run_params) ; tests d'abord ; rouge (`ModuleNotFoundError: No module named 'sens_pool'`,
  04:31:14) ; vert (9 tests) ; mutants B1 « ≤ » au seuil, B2 compte au statut seul (lecture ok sans prix comptée), B3 garde
  POOL-MIN à « ≤ », B4 règle non recalculée, B5 garde absente, B6 critère déviant lu sur ok, B7 « ≥ » au seuil déviant,
  B8 pool non réduit : 8/8 tués.
- 2026-10-04 04:32-04:33 UTC, sous-lot **PP-c** (POOLEE-BLOC-1 (a)) : tests d'abord (valeurs à la main : 9/√9 = 3) ; rouge
  (`No module named 'poolee_bloc'`, 04:32:45) ; vert (11 tests) ; mutants C1 racine oubliée, C2 une seule strate, C3 z_bloc
  non publié ignoré, C4 z_pool absent ignoré : 4/4 tués.
- 2026-10-04 04:33-04:37 UTC, sous-lot **PP-d** (HOST-DEGRADED-2, HORLOGE-ETENDUE-1) : tests d'abord ; rouge
  (`No module named 'hote_horloge'`, 04:34:18) ; vert (14 tests) ; fixture renforcée (e sans lecture ok hors des fenêtres
  retirées, pour que le mutant « D1 non réappliqué » soit visible) ; mutants D1 sonde rattachée au démarrage précédent,
  D2 premier marqueur, D3 clock_check qui ouvre un démarrage, D4 fenêtres non retirées, D5 D1 non réappliqué, D6 relevé
  hors segment compté, D7 médiane nulle comptée, D8 étendue = max : 8/8 tués.
- 2026-10-04 04:38-04:40 UTC, sous-lot **PP-e1** (CENSURE-INFO-2, bornes de z_s) : référence indépendante = énumération
  exhaustive des imputations (64 et 512 cas, `Fraction`, code du test) ; rouge (`No module named 'censure'`, 04:38:57) ;
  vert (16 tests) ; mutants E1 sommets à un seul flux, E2 c limité à 0, E3 terme de gradient omis (borne inférieure non
  extérieure), E4 borne relâchée non appliquée : 4/4 tués.
- 2026-10-04 04:40-04:46 UTC, sous-lot **PP-e2** (CENSURE-INFO-2, témoins et lecture) : tests d'abord ; rouge
  (`no attribute 'strates'` puis `'identification'`) ; une attente du test corrigée avant le code (la dernière position
  de la grille sautée tombe hors du segment à n fixe : grille modifiée, la dernière position est vue) ; vert (19 tests) ;
  mutants E5 positions sautées mal recomptées, E6 série complétée sans les positions sautées propres (d'abord VIVANT :
  masqué par la recherche W_B qui s'adapte et par K = 0 sous W_A ; tué après ajout d'une imputation fixe contrôlée par
  journal imputé écrit sur disque), E7 W_B à un seul écart, E8 lecture forcée, E9 contrôle des positions inopérant :
  5/5 tués. Temps de `bornes` sur des entrées synthétiques de la taille du J28 (n = 24 585, s = 5 701, N = 11) : 4,9 s.
- 2026-10-04 04:47-04:51 UTC, sous-lot **PP-f** (SIGMA-BLOC-INDEP-1) : fixtures étendues (prix par lecture) ; tests d'abord
  (variance à la main : Σ B² = 20, σ̂² = 0,625 ; écarts comptés à la main a = 9, c = 6, d = 2, recomptés après une
  première attente fausse c = 8 corrigée avant le code par recomptage ligne à ligne) ; rouge (`No module named
  'sigma_indep'`, 04:48:39) ; vert ; mutants F1 blocs de bord omis, F2 positions contiguës (fenêtre absente qui forme
  une paire), F3 division par ℓ·n, F4 prix nul non compté en panne (tué par exception), F5 staleness « ≥ », F6
  enveloppe « ≥ », F7 médiane qui inclut le flux, F8 n_min ignoré (après ajout d'un cas d à 200 avec la seule e) : 8/8
  tués. Mutant « précédence staleness avant panne » écarté comme équivalent (l'indicateur d'écart vaut 1 dans les deux
  cas), docstring corrigée.
- 2026-10-04 04:51-04:55 UTC, sous-lot **PP-g** (DEP-FENETRES-2 (b) et (c), R1-PLUGIN-1 (a) et (b)) : tests à la main
  d'abord (IF, Bartlett ℓ = 2, runs avec trou, loi de m_t) ; rouge (`No module named 'influence'`, 04:51:57) ; deux
  références de test corrigées (précision 28 du contexte par défaut, passées à 60 chiffres) ; série de test rendue
  asymétrique (p̂ = 1/2, 1/3) pour que les mutants « poids g_i = p̂_i » et « binomiale à p moyen » soient visibles ;
  fixture d'intégration renforcée (b seule en panne) après un mutant VIVANT G7 (cellules hors pool D1) ; mutants G1-G7 :
  7/7 tués (G4 par exception).
- 2026-10-04 04:56-04:59 UTC, sous-lot **PP-h** (CONTENU-DEP-1) : test à la main d'abord (x = 1..4, y = 1, 3, 2, 4 :
  ρ = 0,8, IF = ±0,36, Var̂_0 = 0,0324, Var̂_bloc = 0,0243, N_eff = 25/3, N_eff,0 = 7) ; rouge (`No module named
  'contenu'`, 04:56:16) ; référence N_eff passée à 60 chiffres ; fixture d'intégration passée à 7 flux (avec 5 flux,
  ρ_resid n'était jamais calculé : test trivial, corrigé avant tout mutant) ; mutants H1 facteur ρ/2 oublié, H2
  division par N, H3 blocs de bord, H4 1 − ρ au lieu de 1 − ρ², H5 résidus leave-one-out, H6 rendements qui enjambent
  le trou : 6/6 tués.

## 3. Exécution sur les journaux scellés

- 2026-10-04 04:59:32 UTC : **avant la première exécution sur les journaux** : paramètres et constructions inchangés depuis le §2
  (04:18:36 UTC). Ajouts **descriptifs** faits pendant le codage, avant toute exécution, sans effet sur les critères :
  POOLEE-BLOC-1 (a) imprime aussi z_pool (rendu) à côté ; DEP-FENETRES-2 (b) imprime les rapports Σ IF²/(n·P̂(1 − P̂))
  et σ̂²_IF,bloc/σ̂²_bloc ; DEP-FENETRES-2 (c) imprime l'histogramme des longueurs de runs ; CONTENU-DEP-1 imprime aussi
  N_eff,0 (variance d'influence au lag 0), les SE (Fisher et blocs) et les rapports N_eff/N (min, médiane, max), SE et
  N_eff à 6 chiffres significatifs (format « .6g » de Decimal) ; HOST-DEGRADED-2 imprime le compte des démarrages à
  clock_check non évaluable. Suite post-s2 : 26 tests verts ; journaux contrôlés par sha256 au §0.
- 2026-10-04 04:59:41-05:01:04 UTC : `sens_pool.py quasi-mort` sur les journaux (1 min 23 s, exit 0, stderr vide) ;
  contrôle de cohérence égal dans les deux strates ; aucun retrait (taux ok minimal 24 110/24 585 en calme, 11 171/11 397
  en stress), règle recalculée identique à la règle scellée, « R1 discrimine » recalculé FAUX. Recoupement : n_s − ok =
  pannes du bloc 3 pour chaque flux contrôlé (binance 372, bitstamp 475, gemini 65 en calme ; coingecko 127 en stress).
- 2026-10-04 05:01:22-05:06:00 UTC : `deviant`, `poolee_bloc`, `hote`, `horloge` en parallèle, exit 0 tous, stderr vides.
- **Constat C-1 (présentation, corrigé)** : la ligne par strate de `poolee_bloc.py` imprimait K_s − n_s·P̂_more,s calculé
  hors du contexte nommé (28 chiffres : `120.4918638555169987715770203`), alors que le numérateur sommé et z étaient au
  contexte 50. Test d'abord (cas 1 − 3·0,3…3 = 1E-50, rouge : « 0E-27 », 05:08:41), correction, vert, mutant C5 (terme
  hors contexte) tué ; sortie à refaire.
- **Constat C-2 (HOST-DEGRADED-2, structure du journal de contrôle)** : 4 172 démarrages pour 4 093 run_params ; 74
  démarrages sont ouverts par un clock_check qui suit un run_params sans clock_check avec des marqueurs entre les deux
  (motif compatible avec des écritures entrelacées de deux instances du harnais, non établi) ; le texte du §2 (« un
  clock_check qui n'en suit pas un ») admet deux lectures ; mesure en comptes seulement (outils non livrés
  `outils/demarrages_comptes.py`, `outils/hote_lecture_alt.py`) : les 766 marqueurs de ces 74 démarrages sont tous dans la
  plage D5, aucune fenêtre retenue au J28 n'y tombe : la lecture alternative ne change aucune fenêtre retirée. Compte
  ajouté à la sortie (fonction `entrelaces`, test d'abord : rouge `no attribute 'entrelaces'` 05:08:41, vert, mutant D9
  tué) ; sortie à refaire. Recoupement D5 : resolve_failed 1 550 sur 45 030 relevés rattachés ; la plage D5 en porte
  815 sur 5 313 (ADR-0028 D5) : hors plage 735/39 717 = 1,85 %, égal au taux hors plage de l'ADR.
- 2026-10-04 05:07:06-05:16:00 UTC : `censure`, `sigma_indep`, `influence`, `contenu` en parallèle, exit 0, stderr vides.
- **Constat C-3 (CENSURE-INFO-2, arrondi, corrigé)** : en stress, borne inférieure extérieure et témoin « tout en écart »
  égaux en droit (même P rationnel à c = s) imprimés différents au 50ᵉ chiffre (`…135593` contre `…135597`), d'où
  « borne non serrée » à tort : `z_de` calculait sur des représentations entières non réduites. Test d'abord (entrées
  publiées de la strate stress, docs/11 §3.5 et §2.6, aucun journal lu ; rouge 05:16:32), réduction de la fraction par
  pgcd, vert, mutant E10 tué. Effet : dernier chiffre du maximum de stress (`…104` → `…105`), « borne serrée ».
- 2026-10-04 05:17:32-05:21:40 UTC : sorties de `censure`, `poolee_bloc`, `hote`, `horloge` refaites avec le code final
  (premières versions gardées sous `sorties/v1/`) ; différences : poolee-bloc, termes par strate à 50 chiffres ;
  hote-degrade, une ligne ajoutée (74 ; 0), corps inchangé sinon ; horloge, corps identique ; censure, ligne de bornes
  de stress seule changée (C-3). Code gelé ensuite : les sha256 de script imprimés en tête des neuf sorties sont égaux
  aux fichiers finaux (contrôle par commande), commun.py `72948a51…` partout ; les neuf sorties ont l'étiquette en
  première ligne.
- **Constat C-4 (présentation, corrigé)** : relecture des sorties : les rapports Σ IF²/(n·P̂(1 − P̂)) et
  σ̂²_IF,bloc/σ̂²_bloc d'`influence.py` étaient divisés hors du contexte nommé (28 chiffres). Test d'abord (assertion sur
  la ligne imprimée, rouge 05:29:18), correction, vert, mutant G8 tué ; sortie refaite 05:29:43-05:30:53 (seuls ces
  deux rapports changent de longueur). Balayage par programme de toutes les sorties finales : aucune valeur à 26-29
  chiffres significatifs restante.
- 2026-10-04 05:31 UTC : états par sous-lot reconstruits (`outils/etats_finaux.py`, non livré) : les corrections C-1 à
  C-4 sont portées dans le sous-lot qui crée le fichier ; HOST-DEGRADED-2 et HORLOGE-ETENDUE-1 séparés en PP-d1 et PP-d2
  (PP-d dépassait 200 lignes ajoutées, lignes vides comprises : 212). Onze diffs de code, lignes ajoutées : 144, 137,
  157, 89, 177, 42, 129, 167, 166, 189, 144 ; chaque état intermédiaire passe ses propres tests (4, 6, 9, 12, 15, 16,
  19, 21, 23, 27, 29) ; le dernier état est égal, fichier pour fichier, à l'arbre qui a produit les sorties.
- 2026-10-04 05:33-05:36 UTC : section du §11 écrite (`SECTION-11.md`) ; nombres dérivés [calc] recomptés par programme
  depuis les sorties seules (`outils/calc_section.py`, non livré : taux ok minimal 24 110/24 585 = 0,980679 et
  11 171/11 397 = 0,980170 ; p̂ maximal 475/24 585 = 0,019321 et 226/11 397 = 0,019830 ; m ≥ 3 observé 49 contre
  0,424283 attendus en calme, 118 contre 0,223836 en stress ; fenêtres retirées 3 341/24 585 = 0,1359 et 720/11 397 =
  0,0632 ; K retirées 154 − 70 = 84 et 133 − 59 = 74, exact parce que le pool D1 est inchangé et que la classification
  d'une fenêtre ne dépend que de ses lectures). Sorties copiées sous `docs/adr-0028/execution/post-prereg-2026-10-04/`
  avec README et SHA256SUMS (`sha256sum -c` : OK) ; section insérée au §11 de la copie (§11.1, avant le §12).

## 4. Contrôles finaux (copie neuve de 5afbdd2, exclusions du brief, `biblio/INDEX.md` ajouté)

- 2026-10-04 05:35-05:36 UTC : les 14 diffs s'appliquent dans l'ordre par `git apply --check` puis `git apply` ; l'arbre
  obtenu est égal à la copie de travail (`diff -r` sur `scripts/post-s2` et `docs` : vide ; `diff -rq` global : vide).
- Suite post-s2 sur l'arbre patché : `Ran 29 tests in 22.061s`, `OK`. Suite `s2-harness` : `Ran 398 tests in 105.717s`,
  `OK (skipped=2)` (aucun fichier de `s2-harness` touché). `cargo --locked xtask verify` : `=== VERDICT GLOBAL : VERT ===`,
  exit 0 (S-G4 : 114 fichiers de `docs/` contre 113 avant, le README des sorties en plus ; S-G5 en régime « corpus
  incomplet », comme en CI).
- Campagne finale des mutants sur l'arbre final (`outils/campagne_mutants.py`, non livré ; sortie `mutants-final.log`,
  sha256 `475a2fd0…5c87`) : **63 tués sur 63**, aucun invalide (M1-M9, B1-B8, C1-C5, D1-D9, E1-E10, F1-F8, G1-G8, H1-H6).
  Mutants vivants rencontrés pendant le travail puis tués par un test renforcé : E6, G7 ; mutant écarté comme équivalent :
  précédence staleness/panne dans `sigma_indep.ecart` (l'indicateur vaut 1 dans les deux cas).
- R-13 : `grep TODO|FIXME` sur le code, les sorties et la section : 0. R-8 : bibliothèque standard seule (decimal,
  fractions, itertools, math, collections, argparse, hashlib, re), aucune installation. Style : 21 lignes de 121 à 123
  caractères (le dépôt n'a pas de gate de longueur ; `r2.py` en a jusqu'à 146).
- 2026-10-04 05:45-05:49 UTC, relecture de la section avant remise (E-11) : (i) « la sonde DNS du harnais a échoué »
  devient « la sonde ASN du harnais porte un `resolve_failed` » : `resolve_failed` couvre aussi une erreur réseau des
  requêtes RIPEstat et Cymru, pas seulement la résolution DoH (`r2.resolve_host_real`, l.315-342) ; (ii) la phrase
  H_perte cite les témoins W_B (19 et 42 fenêtres ; `censure.txt` l.13, l.17, l.19-20) au lieu de « pas sans elle » ;
  (iii) la phrase sur le SE de Fisher devient un constat de comptes : SE_F < SE_bloc pour les 110 calculs (55 paires,
  ρ_raw et ρ_resid), rapport SE_bloc/SE_F de 1,503 à 15,032, recompté par programme depuis `contenu.txt` seul [calc] ;
  (iv) une ligne de 171 caractères remise à la largeur du paragraphe. Diff 14 refait : +53 lignes, 0 retirée ; la méthode
  (`git diff --no-index --no-prefix a/… b/…` hors dépôt) reproduit à l'octet l'ancien diff 14 depuis l'ancien état
  (contrôle par `cmp`). Aucun code, aucune sortie, aucun nombre de sortie touchés.
- 2026-10-04 05:48 UTC : constat E-10 (§6) : le `biblio/INDEX.md` des copies venait de `4c46d9a`, pas de `5afbdd2`.
  Contrôles finaux refaits sur une copie neuve de `5afbdd2` (`verif2` : exclusions du brief, `biblio/INDEX.md` tiré de
  `5afbdd2` par `git show`) : 14 diffs `git apply --check` puis `git apply`, OK dans l'ordre ; `diff -rq` contre la
  copie de travail : seul `biblio/INDEX.md` diffère (version) ; suite post-s2 `Ran 29 tests in 17.346s`, `OK` ;
  `s2-harness` `Ran 398 tests in 133.874s`, `OK (skipped=2)` ; `cargo --locked xtask verify` (05:50:19-05:53:27 UTC) :
  huit gates S-G1 à S-G8 `VERDICT : VERT (0 violation(s))`, `cargo fmt --check`, `no_std`, `clippy -D warnings` VERTS,
  `=== VERDICT GLOBAL : VERT ===`, exit 0 ; résumé des gates égal, ligne pour ligne, à celui du premier passage (racine
  mise à part) ; la note S-G5 de l'écart E-2 y est encore (comptée, non affichée).
- 2026-10-04 05:53-05:55 UTC, informatif : la tête du dépôt est passée à `3e275a2` (sept commits depuis `5afbdd2`, de
  `a28dd9e` à `3e275a2`, lus par `git log` et `git diff --stat` seulement). Aucun ne touche `docs/11-mesures-pilotes.md`,
  `s2-harness/`, `scripts/` hors `scripts/controle/`, ni `docs/adr-0028/execution/post-prereg-2026-10-04/`. Sur une copie
  neuve de `3e275a2` (`verif3`, mêmes exclusions, son `biblio/INDEX.md`) : 14 diffs OK dans l'ordre ; suite post-s2
  `Ran 29 tests in 17.731s`, `OK` ; `cargo --locked xtask verify` VERT, exit 0. P-05 et P-08 ne figurent pas parmi les
  27 sources versées par `4c46d9a` (recherche sur le diff de l'INDEX) ; l'annexe B.47 ne touche aucun item du lot.

## 5. Items, un par un

| item | état proposé | preuve |
|---|---|---|
| SHOGEN-FLUX-QUASI-MORT-1 | **fermé** | seuil de l'avis B.39 appliqué tel quel ; sortie `quasi-mort.txt` (aucun retrait ; règle identique ; FAUX) ; sous-lot PP-b ; mutants B1-B4 |
| SHOGEN-QUASI-MORT-PREDICAT-1 | **fermé** | ok = `ok_windows` de `r1.compute_r1`, prédicat statut ok et prix non nul sur la liste de `r1.parse_journal` ; mutant B2 (compte au statut seul) tué ; recoupement n_s − ok = pannes du bloc 3 |
| SHOGEN-POOL-MIN-1 | **fermé** | garde `len(pool) < r1.N_MIN_HORSENV`, refus nommé, aucun z ni « R1 discrimine » ; test `test_pool_min_refus_nomme` ; mutants B3, B5 |
| SHOGEN-FLUX-DEVIANT-1 | **fermé** | sortie `deviant.txt` (aucun retrait ; FAUX), étiquette « exploratoire, conditionnée sur une composante du résultat » ; mutants B6-B8 |
| SHOGEN-POOLEE-BLOC-1 | **(a) fait, item ouvert pour (b)** | `poolee-bloc.txt` : z_pool,bloc ≈ 2,60, exploratoire, hors famille ; (b) appartient au lot DETTES-SIM |
| SHOGEN-HOST-DEGRADED-2 | **fermé, avec écart déclaré** | `hote-degrade.txt` ; critère fixé au §2 avant exécution ; clock_check hors critère (écart au libellé, motif écrit) ; constat C-2 mesuré sans effet ; question Q-1 |
| SHOGEN-HORLOGE-ETENDUE-1 | **fermé** | `horloge-etendue.txt` : 3 610 relevés, étendue ≈ 148 s |
| SHOGEN-CENSURE-INFO-2 | **fermé pour z_s et la lecture ; attribution en attente de P-08** | `censure.txt` : bornes de z_s exactes (maximum par sommets, minimum atteint) ; « non identifié sous censure arbitraire » établi par deux imputations témoins, contrôlées par journal imputé écrit sur disque en test ; aucune borne de z_bloc (item proposé) |
| SHOGEN-SIGMA-BLOC-INDEP-1 | **fermé** | `sigma-indep.txt` : 0 désaccord de classification, σ̂²_bloc et γ̂₀ égaux au bloc 3, chaîne pour chaîne |
| SHOGEN-DEP-FENETRES-2 | **non fermé** | (b) fait (`influence.txt`), (c) fait en tolérance 0 sous loi nulle iid (exploratoire) ; (a) fixed-b non faite : P-05 non détenue ; tolérance et loi nulle de (c) : recherche |
| SHOGEN-R1-PLUGIN-1 | **non fermé** | (a) fait (= DEP-FENETRES-2 (b)) ; (b) descriptif fait (loi de m_t) ; le test (statistique et niveau sourcés) reste une recherche |
| SHOGEN-CONTENU-DEP-1 | **fermé** | `contenu.txt` : N_eff des 55 paires, ρ̂ égaux au bloc 5 ; fonction d'influence de Pearson [inféré], contrôlée à la main en test |

## 6. Écarts déclarés

- E-1 : une recherche `grep -rn … -l` sur toute la copie (07ᵉ minute du travail) a parcouru par programme les octets de
  `docs/15-*`, `docs/16-*` et `docs/pocket-report/` (noms de fichiers seulement en sortie, filtrés avant affichage) ;
  aucun contenu affiché. Les recherches suivantes ont visé des fichiers nommés.
- E-2 : les journaux complets de `cargo xtask verify` (base et final, dans mon dossier) contiennent une note S-G5 qui cite
  un fichier `docs/15-*` (comptée par `grep -c`, jamais affichée) ; je ne les livre pas comme pièces ; le verdict est
  recopié au §4.
- E-3 : HOST-DEGRADED-2 : le `clock_check` n'entre pas au critère (fixé au §2, avant exécution) ; la forme du critère
  (sonde ASN du démarrage, dernier marqueur) est un choix du worker, l'item ne la fixant pas.
- E-4 : quatre corrections faites après une exécution sur les journaux (C-1 à C-4), chacune par test d'abord, mutant et
  sortie refaite ; aucune ne touche un critère ni un paramètre : présentation (C-1, C-4), compte descriptif ajouté (C-2),
  arrondi au 50ᵉ chiffre et drapeau « serrée » (C-3). Premières versions gardées sous `sorties/v1/`.
- E-5 : ajouts descriptifs aux sorties décidés pendant le codage, déclarés avant la première exécution (§3).
- E-6 : exposition avant de fixer les paramètres : bloc 3 du J28 et docs/11 (déclarée au §2).
- E-7 : la fiche du worker dit « fixtures seulement (D.4 a) » ; le G0 (ligne POST-PREREG : « lit les journaux scellés :
  oui ») et le brief autorisent ce lot à lire la copie de session ; les tests restent sur fixtures, les journaux ne sont
  lus que par les scripts d'analyse et jamais affichés.
- E-8 : le test `test_borne_serree_sans_ecart_d_arrondi` prend en entrée des agrégats publiés (docs/11 §3.5 et §2.6), pas
  un journal.
- E-9 : PP-d (212 lignes ajoutées, lignes vides comprises) coupé en PP-d1 et PP-d2 pour R-25.
- E-10 : `biblio/INDEX.md`, ajouté aux copies parce qu'une gate le lit (brief), a été copié à 04:18:56 UTC depuis le
  dépôt, dont la tête était déjà `4c46d9a` (commit de 04:16:35 UTC, lot DETTES-BIBLIO), et non tiré de `5afbdd2` ; les
  premiers contrôles finaux (05:35-05:36) ont tourné avec cette version (sha256 `0fb86390…` au lieu de `3399ba9e…`).
  Refaits sur `5afbdd2` pur (§4, 05:50-05:53) : mêmes verdicts. L'entrée Künsch 1989 est à la l.336 dans les deux
  versions ; aucun livrable ne cite une ligne de l'INDEX.
- E-11 : correction de rédaction de la section faite après les premiers contrôles finaux (§4, 05:45-05:49) ; aucun
  nombre de sortie ni critère touché ; un nombre dérivé ajouté [calc] (rapport SE_bloc/SE_F de 1,50 à 15,0, recompté
  depuis `contenu.txt`) ; diff 14 refait et tous les contrôles refaits.

## 7. Questions à l'orchestrateur

- Q-1 : le critère de HOST-DEGRADED-2 (sonde ASN en échec ⇒ fenêtres du démarrage retirées ; clock_check hors critère)
  est-il adjugé comme la forme de l'item, ou faut-il l'écrire à l'annexe B avant d'en citer le résultat ? Toute autre
  forme serait un second chemin d'analyse, postérieur aux résultats.
- Q-2 : « au registre de docs/09-vocabulaire.md » est lu comme « rédigé dans le registre de doc 09 » ; aucune entrée
  neuve n'est proposée au registre. Si une entrée est attendue (par exemple contre « z_IF,bloc rejette » ou « la
  sensibilité confirme »), le dire.
- Q-3 : deux statistiques exploratoires franchissent 2,33 (z_pool,bloc ≈ 2,60 ; z_IF,bloc ≈ 2,37 en calme) ; la section
  les étiquette comme les sorties hors décision du §9.3 pt 11 ; faut-il les signaler à part à l'investisseur ?
- Q-4 : l'annexe B est à l'orchestrateur : proposition de bloc au rapport (fermetures et items à former du §8).

## 8. Items à former (règle PAROXYSME), proposés

- SHOGEN-ZIF-NIVEAU-1 : niveau de z_IF,bloc et de z_IF,0 sous le modèle nul (simulation synthétique de SIM-NIVEAU), avant
  tout usage de ces statistiques ; déclencheur : avant toute proposition qui les cite.
- SHOGEN-CENSURE-ZBLOC-1 : borne extérieure de z_bloc sous censure arbitraire (le placement des fenêtres imputées compte) ;
  sans elle, aucune lecture « identifié » n'est possible ; déclencheur : avant toute lecture « identifié ».
- SHOGEN-ENTRELACEMENT-D5-1 : 74 démarrages ouverts par un clock_check après un run_params sans clock_check, marqueurs
  entre les deux, tous dans la plage D5 (766 marqueurs) : écritures possiblement entrelacées de deux instances du harnais
  pendant l'incident de la plage ; à qualifier pour S2-bis (ADR-0029) ; sans effet sur le J28.
- SHOGEN-HOST-CRITERE-1 (si Q-1 ne l'adjuge pas) : forme du critère de HOST-DEGRADED-2 à écrire d'avance pour S2-bis
  (ADR-0029 §2.3 la fixe déjà pour S2-bis, sur des témoins hors pool).
- SHOGEN-PEARSON-IF-SOURCE-1 : source détenue de la fonction d'influence de Pearson (passer de [inféré] à [lu]) ;
  procurement, sans code.
- Restent ouverts : SHOGEN-DEP-FENETRES-2 ((a) P-05 ; (c) tolérance et loi nulle), SHOGEN-R1-PLUGIN-1 ((b) test sourcé),
  SHOGEN-POOLEE-BLOC-1 (b) (lot DETTES-SIM), procurement P-08 (attribution de CENSURE-INFO-2).

## 9. Livrables (sha256 recalculés le 2026-10-04 à 05:56 UTC ; dossier `scratchpad/dettes/POST-PREREG/`)

Diffs, à appliquer dans l'ordre sur `5afbdd2` par `git apply` (contrôlé aussi sur `3e275a2`, §4) :

| diff | lignes | fichiers | sha256 |
|---|---|---|---|
| `diffs/01-PP-a1.diff` | +144 | `scripts/post-s2/` README, `commun.py`, `tests/__init__.py`, `tests/test_commun.py` | `779524344fd8d37c55e3fc0c0c5c87240eb9ec79deb3f8afa27ad94e216f43a8` |
| `diffs/02-PP-a2.diff` | +137 | `commun.py`, `tests/fixtures.py`, `tests/test_commun.py` | `d6af075800d107d51115786b0b4a3277004a1b6c552835f412b805255590d581` |
| `diffs/03-PP-b.diff` | +157 −8 | `sens_pool.py`, `tests/fixtures.py`, `tests/test_sens_pool.py` | `eb80274a30c1e771efef5ea8ce2081bdd77f55422428c277d82924c34d1544e3` |
| `diffs/04-PP-c.diff` | +89 | `poolee_bloc.py`, `tests/test_poolee_bloc.py` | `b8cdcb51114e9ae16d21bc92a368d8d5546138ae16c4a6ee91deec1c1cdedf41` |
| `diffs/05-PP-d1.diff` | +177 | `hote_horloge.py`, `tests/test_hote_horloge.py` | `b42c4ed9f301cec4c9b9274384426437bdde0c25e09299b20433994609c2954b` |
| `diffs/06-PP-d2.diff` | +42 −7 | `hote_horloge.py`, `tests/test_hote_horloge.py` | `2218a3fbd7400e8be4b49dfba6d888e6af472dee6ca424c79adc2db76dd8be0f` |
| `diffs/07-PP-e1.diff` | +129 | `censure.py`, `tests/test_censure.py` | `e8ce9bccf1a426e2f3545f3511af92b59cfdd97582c2ff887463a44cfcb48589` |
| `diffs/08-PP-e2.diff` | +167 −2 | `censure.py`, `tests/test_censure.py` | `74209ad2b7b6691b944ec307de04d75321f13f0fb559f278be8db71d87b63c1a` |
| `diffs/09-PP-f.diff` | +166 −3 | `sigma_indep.py`, `tests/fixtures.py`, `tests/test_sigma_indep.py` | `67a0549c7a3ca6220d90d411c2a50730aa577a5670bec6b1599c966cd392c75c` |
| `diffs/10-PP-g.diff` | +189 | `influence.py`, `tests/test_influence.py` | `67f9d038066bde4c6233fa29a859e69df3a168c8b634b8dc9fcf1abab4f5308b` |
| `diffs/11-PP-h.diff` | +144 | `contenu.py`, `tests/test_contenu.py` | `52e657f020cd0adc247fa34f878e9cf703f480030013102aed353a04aa126585` |
| `diffs/12-PP-i1.diff` | +176 | `docs/adr-0028/execution/post-prereg-2026-10-04/` README et huit sorties (toutes sauf `contenu.txt`) | `6daeca0b80e8d8a7ddcdfadc671c39de8a982aab8154f9a8c96d08e325dd84bc` |
| `diffs/13-PP-i2.diff` | +75 | même dossier : `contenu.txt`, `SHA256SUMS` | `9e2167df1373ae23d42a2601b3c4f5d0c1ad5bf22cf0fd560377a4f3fe749c5c` |
| `diffs/14-PP-j.diff` | +53 | `docs/11-mesures-pilotes.md` (§11.1, avant le §12) | `f1606f41f26c51888d4162c0bbd3178a0f3e9c901c9ee5ee37e1ce517cfac0bf` |

Autres pièces :
- `SECTION-11.md` (texte du §11.1, égal aux lignes ajoutées du diff 14, ligne vide finale mise à part) :
  `6f74b6a7ae3b8133470aa92639dee6b06f9b6b24d644a24c3f076ac5d8808347`.
- Sorties (versées par les diffs 12-13 ; sommes de `SHA256SUMS`, `sha256sum -c` : OK) : quasi-mort `9942c78a…7ad1`,
  deviant `ca87f2d4…8fd2`, poolee-bloc `1c32d45f…22f5`, hote-degrade `2636951e…e698`, horloge-etendue `2c4c25ac…8efc`,
  censure `b362aaba…b516`, sigma-indep `1756b0fd…c256`, influence `7ef530a7…ebc4`, contenu `9bbfa043…121a` ;
  README `e8dc467eae7199cb488eb56639b6bf5cb39d7e7463687417b6de832bca52495c` ; SHA256SUMS
  `bbcfc92e32277de1ab8729530c3c97c7e4f672979c76fe5e0a2119076d3be191`.
- Code final (`scripts/post-s2/`, égal aux sha256 imprimés en tête des sorties) : `commun.py` `72948a51…e7a1`,
  `sens_pool.py` `3475aeac…7309`, `poolee_bloc.py` `8d6b8cf2…1e34`, `hote_horloge.py` `145241f1…d653`, `censure.py`
  `cb19845b…603f`, `sigma_indep.py` `0f1ce347…fc06`, `influence.py` `db6b76f0…254c`, `contenu.py` `f6f69d43…dda9`.
- `mutants-final.log` (63 tués sur 63) : `475a2fd04af25fcdd5225c68029c7db4d7194d62b673ed81abce3dadf9705c87`.
- Non livrés (outils de travail, dans `outils/`) : `mut.py`, `campagne_mutants.py`, `demarrages_comptes.py`,
  `hote_lecture_alt.py`, `etats_finaux.py`, `calc_section.py` ; journaux complets de `cargo xtask verify` (écart E-2).
- Ce journal : sha256 donné dans le rapport de remise (il ne peut pas se contenir).
