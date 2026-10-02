# Partie 2 de S2 — G0 courts par étape (orchestrateur de la session cloud)

Rattachement : `docs/adr-0028/PLAN-PARTIE-2.md` ; ADR-0028 annexes A, B, D ; méthode `docs/METHODE-PARTIES.md`
(un G0 court par lot : fichiers, tests, risques). Chaque section est datée ; une section écrite ne se réécrit pas.

## P0 — SHOGEN-ORACLE-PERIMETRE-1 (i) : S-G4 et S-G5 sur `s2-harness/**/*.md` (2026-10-02 02:5x UTC)

- **Source** : annexe B l.188 (item, échéance « (i) avant le G0 du lot RENDU-1 ») ; origine C-1 et C-9 b du G2 de
  DOCS-S2 (`docs/G1-lot-DOCS-S2.md` l.90 : S-G4/S-G5 ne lisent que `docs/**/*.md`) ; doctrine des gates ADR-0013
  (une gate imprime sa couverture ; aucun vert sans mutant semé) ; `.claude/agents/shogen-devops.md` §2.
- **Fichiers** : `xtask/src/sg4.rs`, `xtask/src/sg5.rs` (périmètre : `docs/**/*.md` puis `s2-harness/**/*.md`,
  couverture imprimée pour les deux) ; `xtask/tests/mutants.rs` (arbres de fixture, mutants neufs) ; au besoin
  `s2-harness/README.md` et `RUNBOOK-campagne.md` si la gate étendue y trouve une violation (correction du texte,
  jamais de la gate).
- **Tests** : (1) mutant S-G4 : locution interdite dans un `.md` de `s2-harness/` ⇒ S-G4 ROUGE ; (2) mutant S-G5 :
  citation anglaise hors corpus dans un `.md` de `s2-harness/` ⇒ S-G5 ROUGE ; (3) les témoins verts existants
  restent verts ; (4) `cargo --locked xtask verify` VERT sur l'arbre réel, couverture S-G4/S-G5 = fichiers de
  `docs/` + 2 fichiers de `s2-harness/`.
- **Risques** : (a) `fichiers_par_extension` refuse de conclure sur un répertoire absent ou vide : les arbres de
  fixture des mutants documentaires n'ont que `docs/` ; ils doivent recevoir un `s2-harness/` synthétique, sans
  affaiblir le refus ; (b) la recherche est récursive sur le disque, pas sur l'index git : un `.md` non suivi sous
  `s2-harness/` (environnement virtuel, cache) entrerait au périmètre, à constater et à déclarer, jamais à
  exclure par nom choisi par le fichier ; (c) S-G5 en régime partiel en session cloud (biblio absente) : les
  citations de `s2-harness/` sont listées « non contrôlées » ; le rejeu en corpus complet relève de (ii) ;
  (d) S-G4 exempte seulement `docs/09-vocabulaire.md` ; aucune exemption neuve.
- **Taille** : ≈ 15 lignes de code, ≈ 60 de tests [inféré]. Un commit (R-25).
- **G1** : worker `shogen-worker` (`claude-opus-5-5`, effort `max`). Gate 0 : modèle résolu déclaré par le worker.

## A — rendu du rapport : DOCS-S2-b et items de rendu (2026-10-02 03:1x UTC)

- **Sources** : annexe A l.63 (DOCS-S2-b) ; annexe B l.47 et l.107 (REPORT-FISHER-1), l.307 (GARDE-LIBELLE-1),
  l.212 (BLOC3-RENVOI-TAU-1), l.297 (RENDU-ZERO-1), l.306 (AXES-ENONCE-1), l.325 (SENS-PERTES-2), l.232
  (DECIMAL-ARRONDI-1, portée étendue à l'EMD), l.298 (PMORE-RESIDU-1), l.175 (BLOC1-RUNPARAMS-1), l.213
  (SENS-PLAGES-1), l.173 (ASN-STATUT-1) ; forme de la ligne Fisher : `docs/G1-lot-DOCS-S2.md` §2, « DOCS-S2-b
  (provisoire) » (l.76-78) ; méthode de re-capture : même section (l.79-83).
- **Décisions de l'orchestrateur (constructions)** :
  - REPORT-FISHER-1 : la ligne imprimée prend la forme finale du G1 de DOCS-S2 (l.77), `{content['n_min']}`
    dynamique, ni « 300 » ni « 0,058 », SE numérique omise ; test `test_v_ligne_nmin_suit_le_journal` refait.
  - GARDE-LIBELLE-1 : imprimer le seuil appliqué (`seuil_historique` du bloc), aux trois sites ; pas de refus.
  - BLOC3-RENVOI-TAU-1 : renvoi complété par « τ relatif : ADR-0020 déc. 2, ADR-0022 ».
  - RENDU-ZERO-1 : forme unique « 0 » pour un `Decimal` nul dans `_fmt_dec` ; test sur trois fixtures.
  - AXES-ENONCE-1 : construction (b) (décidée au B.18) : axes évaluables de la strate imprimés, résidu nommé.
  - SENS-PLAGES-1 : titre de la variante « incluse » accordé au nombre de plages réintégrées (pas de règle
    « une seule plage » : la sortie reste juste si la liste change).
  - DECIMAL-ARRONDI-1 : `ctx.rounding = ROUND_HALF_EVEN` dans chaque `localcontext` de `r1.py` (15 sites mesurés
    à 03:14 UTC, EMD de `regle_critere` compris) ; test sous `ROUND_DOWN` ambiant.
  - PMORE-RESIDU-1 : P_more sans annulation (entiers, une division `Decimal` finale) ; test p̂ = (0, 1/28, 0) ⇒ 0
    exact.
  - BLOC1-RUNPARAMS-1 : nombre de valeurs distinctes par clé non porteuse sur les démarrages, une ligne au bloc 1.
  - ASN-STATUT-1 : ventilation par statut des `asn_attribution` retirées, sur l'assiette de chaque ligne.
  - SENS-PERTES-2 : construction de l'item (fenêtres sautées par plage et par strate, lectures absentes).
- **Coupe R-25 (trois sous-lots, appliqués dans l'ordre, chacun ≤ 200 lignes de code et tests)** : **A1** calcul
  (`r1.py` : DECIMAL-ARRONDI-1, PMORE-RESIDU-1) ; **A2** rendu des blocs 3 et 6 (`report.py` : REPORT-FISHER-1,
  GARDE-LIBELLE-1, BLOC3-RENVOI-TAU-1, RENDU-ZERO-1, AXES-ENONCE-1, SENS-PLAGES-1) ; **A3** bloc 1 et
  [SENSIBILITÉ] (`report.py` : BLOC1-RUNPARAMS-1, ASN-STATUT-1, SENS-PERTES-2). Si un sous-lot dépasse 200, il se
  coupe encore ; jamais de fusion de sous-lots.
- **Tests** : D.4 a (fixtures seulement) ; tests d'abord, échec montré, une mutation par test ; à chaque sous-lot
  qui change le rendu, re-capture de `SHA_BASE_SANS_OPTION` (`tests/test_exclusion.py`) et de
  `SHA_BASE_AVEC_OPTION` (`tests/test_pool_analyse.py`) justifiée par le diff textuel du rendu avant et après
  (ligne par ligne, rien d'autre) ; les rendus « avant » doivent égaler les épingles en vigueur.
- **Risques** : (a) un changement de calcul (A1) qui bouge un rendu épinglé : à montrer dans le diff textuel ;
  (b) BLOC1-RUNPARAMS-1 et SENS-PERTES-2 ne lisent aucun journal de campagne avant le scellement (D.4 a) : calcul
  au rendu, testé sur fixture ; (c) la règle scellée SHOGEN-CRITERE-R1-1 (seuil 2,33, ℓ = 240, trois valeurs) ne
  change pas : test de non-régression des valeurs de la règle sur les fixtures de `test_critere`.

## B — RENDU-2 : lecteur de journal, recalcul tiers et enregistreur d'oracle (2026-10-02 03:2x UTC)

- **Sources** : annexe A l.38 (RENDU-2) ; annexe B l.43 (TORN-LINE-UTF8-1), l.45 (RAW-LECTEUR-1), l.52 et l.108
  (ORACLE-ENREG-1), l.214 (BLOC6-TS-1), l.318 (D5-RECALCUL-TIERS-1), l.319 (CENSURE-CAUSES-1) ; ADR-0028 D6 (viii)
  (champs du schéma `shogen.oracle-record.v1`) et §1 bis.6 (A-12 : `paquet.sha256`, `sceau.genTime`) ; code lu à
  03:2x UTC : `records.read_jsonl_tolerant` (l.72-101 : `open(..., encoding="utf-8")` puis `readlines()`, d'où
  l'erreur de décodage avant le contrôle de dernière ligne), `journal.raw_entry` (l.50-57 : `sha256_raw`,
  `raw_b64`), `r1.recompute_from_journal` (l.760).
- **Décisions de l'orchestrateur (constructions)** :
  - TORN-LINE-UTF8-1 : lecture en octets, décodage ligne par ligne ; dernière ligne non décodable traitée comme
    dernière ligne tronquée (consignée, ignorée) ; ligne non décodable **non finale** : `ValueError` (le refus
    actuel est gardé, jamais affaibli).
  - RAW-LECTEUR-1 : **lecteur et oracle construits** (pas de limite déclarée) : relecture de `raw.jsonl` par le
    même lecteur tolérant, décodage de `raw_b64`, sha256 recalculé égal à `sha256_raw` de la ligne et à celui de
    la lecture correspondante de `journal.jsonl` ; tout écart = refus nommé.
  - BLOC6-TS-1 : relevé `asn_attribution` sans `ts` compté à part au bloc 6 (ligne imprimée), jamais `KeyError`.
  - D5-RECALCUL-TIERS-1 : fonction sœur `recompute_d5_from_journal(control, journal, exclude_ranges, segment)`
    selon la construction de l'item ; test d'égalité avec le bloc 3 du rendu (même journal, mêmes options).
  - CENSURE-CAUSES-1 : le sous-lot commence par établir, sur les sources du dépôt (HS2-04, journaux G1 de B-SEG
    et de D5-AMEND, notes de réparation versionnées), quelles signatures sont lisibles dans un journal **réparé et
    scellé** ; ventilation par cause codée seulement sur ces signatures ; la cause « limite d'exécution de tâche »
    n'a pas de signature dans le journal : source hors journal nommée (journal d'événements de l'ordonnanceur du
    poste local), cause imprimée « arrêt du harnais, cause non attribuée par le journal » ; si les signatures ne
    suffisent pas, le sous-lot rend la question au lieu de coder.
  - ORACLE-ENREG-1 : enregistreur `s2-harness/tools/oracle_record.py` (bibliothèque standard) : lance les
    commandes nommées, écrit un enregistrement `shogen.oracle-record.v1` (tous les champs de D6 viii, plus
    `paquet.sha256` et `sceau.genTime`, nuls hors du rôle « rendu ») dans un répertoire passé en argument, nom
    `shogen-<sha court>-<role>-<date>-<pid>.json` ; mode `--verifier` qui relit un enregistrement et contrôle
    rôle attendu, `tree.commit`, `exit` 0, `static_only` false, `served_from` conforme (refus nommé sinon) ; le
    rôle « rendu » exige `paquet.sha256` et le sha256 de chaque sortie.
- **Coupe R-25 (dans l'ordre, chacun ≤ 200)** : **B1** lecteur (TORN-LINE-UTF8-1, BLOC6-TS-1) ; **B2**
  RAW-LECTEUR-1 ; **B3** D5-RECALCUL-TIERS-1 ; **B4** ORACLE-ENREG-1 ; **B5** CENSURE-CAUSES-1 (le plus incertain,
  en dernier).
- **Tests** : D.4 a (fixtures seulement) ; fixture « dernière ligne coupée dans un caractère multi-octets »
  (HS2-03) ; enregistrement produit sur fixture puis relu par `--verifier` (champs, sha, exit), avec un mutant par
  contrôle ; épingles re-capturées seulement si un rendu change (BLOC6-TS-1), par diff textuel.
- **Risques** : (a) le lecteur est sur le chemin de recalcul (D6 i) : toute tolérance neuve est un desserrage,
  interdite hors dernière ligne ; (b) l'enregistreur lance des commandes : liste fermée, jamais de shell
  interprété ; (c) `SHOGEN_S2_CAMPAGNE_CONTROL` : l'enregistreur la consigne (posée ou non), ne la pose jamais.
