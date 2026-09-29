# ADR-0028 — Décisions de sortie S2 et séquence PAROXYSME Shōgen → MONARK (délégation investisseur du 2026-09-29)

- **Statut** : **G0 proposé** (orchestrateur Shōgen `claude-fable-5-1`, 2026-09-29). Checkpoint-1 du validateur-humain (`claude-fable-5-1`) : **ACCEPTE-AVEC-CORRECTIONS**, liste fermée C-1..C-17 (`F:\tmp\cp1-adr0028\CP1-ADR-0028.md`, sha256 `a2d5bafb69c5a541ce1557a4eebd8833890a0db7cf3371f03f9af34ebb22a2b5`). C-1 : avis versés par l'orchestrateur. C-2..C-17 : appliquées le 2026-09-29 par un rédacteur à contexte frais ; table d'application `F:\tmp\cp1-adr0028\APPLICATION-C2-C17.md`. **À soumettre au cp-1 bis avant tout G0 de lot.** Aucun code dans cette ADR.
- **Mandat** : investisseur, 2026-09-29 : « pour les choix, consultes tes advisors, moi je suis investisseur, pas technicien. prenez des décision pour que SHOGEN SOIT UN PRODUIT DE GRANDE ENVERGURE ». Les décisions **techniques** ci-dessous sont prises par délégation. Les décisions de **valeur, d'argent, de message public et de droit** restent à l'investisseur (§4). Les décisions antérieures de l'investisseur que cette ADR amende sont soumises à son **veto jusqu'au scellement du paquet** (§4.10).
- **Rattachement** :
  - cartographie `docs/rapports/cartographie-2026-09-29.md` (constats SUP-01, SUP-02, F-DP-01, HS2-*, GC-*, CARTO-MK-*) ; revue G2 du lot A (`F:\tmp\shogen-g2-lotA\G2-lot-A-ADR-0025.md`) ; ADR-0020, 0022 pt 5, 0023, 0024, 0025 ; doc 10 ; RUNBOOK ;
  - avis de consultation (canal 2, 2026-09-29), textes intégraux versés **hors dépôt** et scellés (C-1 ; emplacement ci-dessous) :
    - Emplacement (2026-09-29, orchestrateur) : les trois avis sont conservés **hors dépôt**, verbatim et scellés, sous `F:/tmp/shogen-carto-2026-09-29/avis-adr0028/` (copie `D:/shogen-sauvegarde-2026-09-29/avis-adr0028/`, `SHA256SUMS.txt`) : leur texte cite des sources non versées à biblio/ (S-G5), et un avis ne se paraphrase pas. Les sha ci-dessous font foi.
    - `AVIS-advisor-defi-2026-09-29.md` — `advisor-defi`, modèle résolu `claude-fable-5-1` (l.5), Q1-Q5 et Q9 — sha256 `fac2117387785ea718672cfa65bcd1985ac931ade02b2f8e6eb8149a12a40d3b` ;
    - `AVIS-advisor-2026-09-29.md` — `advisor`, `claude-fable-5-1` (l.5), Q6-Q10 et Q2 — sha256 `87e044201821831c200b89cc5b80351ff0f47f9359fee36d0e8c0ed9ef6cc047` ;
    - `AVIS-advisor-marche-2026-09-29.md` — `advisor-marche`, `claude-fable-5-1` (l.3), Q9 et Q6 — sha256 `592258d3e2605b2707ed02c5c45bf332535dee7602aa37972fb3a71b03e7d8ff` ;
  - points où cette ADR ne suit pas un avis, ou le tranche autrement : **annexe E**.
- **Annexes** (même dossier) : A — table des lots (C-3) ; B — items formés (C-15) ; C — modes MAST (C-2) ; D — pré-enregistrement : inventaire des lectures, pièces interdites, attestations, définitions de contrôle, traitements (C-6, C-7, C-10, C-11, C-12, C-13) ; E — avis non suivis (C-1).
- **Provenance de la révision cp-1** : rédacteur `claude-opus-5-5` (effort max, R-1 déclaré), 2026-09-29, à partir de 19:00:35Z (`date -u`) ; entrées : avis du cp-1, trois avis, pièces autorisées (annexe D.3 f) ; réviseurs : orchestrateur (R-21), puis validateur-humain (cp-1 bis).

## 1. Décisions statistiques (sortie S2)

- **D1 — Pool d'analyse (accepte ADR-0023, pt 5 amendé ; veto §4.10 a).** Règle générale, écrite avant tout rendu. **Forme choisie après observation de la disponibilité** des flux, jamais d'un z, d'un K ou d'un φ.
  - *Forme formelle (C-10 i)*. Soit S un segment analysé (J14 principal, J14 second, J28), de strates s ∈ {calme, stress}. Pour tout flux f de `run_params.pool` (12 flux), soit ok(f, s) le nombre de lectures `ok` de f dans la strate s de S.
    - (a) Si ok(f, s) = 0 pour toute strate s de S, f est retiré du pool d'analyse de S (R1, L&M, R2).
    - (b) *Flux mort dans une seule strate* : si ok(f, s) = 0 pour une strate s seulement, f est retiré du pool de cette strate seulement, pour R1 et L&M (même motif : un flux sans lecture est en écart dans chaque fenêtre de la strate, SUP-01), et reste au pool de l'autre strate. L&M prend N = taille du pool de la strate. R2 n'applique que le cas (a). La forme stratifiée de la strate poolée (D2 pt 4) somme des strates à pools distincts. Si le cas (b) s'applique sur un segment, k nominal diffère d'une strate à l'autre : il est imprimé par strate au bloc 1, et la mention « 10 sources / 11 flux » ne vaut que pour les strates où Pyth seul est retiré. Cas (b) = proposition du rédacteur, **à ratifier** (annexe E, ligne E-D1b).
    - (c) Tout retrait est nommé au bloc 1, avec ses comptes, par strate.
  - Mesurée par comptes sur le journal entier, la règle ne retient que Pyth : 0 `ok` sur 40 804 lectures, HTTP 401 dès 2026-08-26T19:00Z ; tous les autres flux ont des lectures `ok` dans les deux strates (AVIS-advisor-defi l.11, l.143). Les segments filtrés ne sont pas mesurés : le script de rendu applique la règle et l'imprime.
  - R1, L&M et R2 portent sur 11 flux ; k nominal = 10 sources / 11 flux, dans tout texte. Écart au `run_params` ex ante déclaré, avec sa cause (Hermes gaté par clé) ; le z à 12 flux n'est jamais imprimé comme un z.
  - Motif (advisor-defi, AVIS Q1 l.20-26) : avec un flux toujours en écart, une co-défaillance positive pousse z vers le négatif (K − n·P̂ ≈ −n·Cov pour deux sources vivantes) ; L&M a N fixé à 12 (`lm.py:15,130`).
  - Erratum : ADR-0023 l.11 « 20:00 UTC » → 19:00Z (acte d'écriture §8). Véhicule : **lot B0** (annexe A).
- **D2 — Paquet de pré-enregistrement (oui), scellé par sha au JOURNAL avant tout rendu sur journaux réels.**
  - Rédigé et validé par des agents à contexte frais, **sans accès à aucune pièce de la liste fermée de l'annexe D.2** (C-7), avec attestation écrite. Contrôle a posteriori non-LLM : recherche des chemins de D.2 dans les appels d'outils de leurs transcriptions (annexe C, FM-1.1).
  - Contenu :
    1. Mesures et commits : collecte `ed479c5` ; analyse lot A `742f1fc` + `7f8b5cc`, puis les lots B0, B-SEG, B, POOLEE et RENDU de l'annexe A (commits écrits au paquet).
    2. D1, sous sa forme formelle.
    3. D5.
    4. **Strate poolée en forme stratifiée** (type Mantel-Haenszel) : z_pool = Σ_s (K_s − n_s P̂_s) / √Σ_s n_s P̂_s (1−P̂_s). **Pas** l'union brute de la décision 273, qui crée une association artificielle si les taux diffèrent entre strates (Simpson). **Étiquetée exploratoire** : décidée après la lecture intermédiaire du 28/09. Calme et stress restent confirmatoires, sous deux conditions : l'inventaire de l'annexe D.1 est déclaré, et les décideurs attestent n'avoir vu ni z, ni K, ni P̂_more, ni φ (annexe D.3). **Famille de Bonferroni (C-10 iii)** : m = 2 tests confirmatoires (calme, stress), chacun unilatéral au seuil 2,33, « le point à 99 % de la normale standard » (doc 10 l.379-380, l.386). Borne : P(au moins un rejet à tort) ≤ 2 × 0,01 = 0,02. La strate poolée est hors famille. Le « ~3 % » sur trois tests (RUNBOOK l.140) est supplanté. Veto §4.10 a (273).
    5. D3.
    6. D4 et le **segment J28 (C-10 ii)**, même logique que D4 : [2026-08-26T19:00:00Z ; T_fin), semi-ouvert, appliqué par horodatage à tous les types d'enregistrements (`window_start`, `ts`, `harness_ts`). T_fin = `window_start` de la 38 600ᵉ fenêtre distincte + 60 s (w = 60 s, ADR-0024 déc. 2). C'est la règle d'arrêt à n fixe d'ADR-0024 (déc. 1 et 4), pas une date choisie ce jour. La fin de campagne est le 2026-09-28 vers 01:27Z (cartographie l.52). T_fin est lu du journal scellé par le script de rendu et imprimé au bloc 1 (epoch et ISO). L'exclusion ADR-0025 s'applique dans ce segment : n = 35 982.
    7. **Liste fermée des sensibilités** : plage ADR-0025 exclue ou incluse ; seconde coupe J14 (270) ; dépendance entre fenêtres par blocs, taille de bloc fixée à l'aveugle dans le paquet (SHOGEN-DEP-FENETRES-1). Toute autre analyse est exploratoire. **Traitements pré-enregistrés (C-10 v)** : SHOGEN-TAU-REDERIV-1, -HOST-DEGRADED-1, -CENSURE-INFO-1, -DP-JOURNAL-LOSS-1 et le bloc 6 (ADR-0026) sont « descriptif seulement ». Aucun n'entre dans la liste des sensibilités (annexe D.5).
    8. **Inventaire complet des lectures faites sur les données de campagne (C-6)** : annexe D.1. Chaque lecture est classée « marginale/opérationnelle » ou « résultat (z, K, P̂_more, φ) ». Les attestations de l'auteur de cette ADR, des trois advisors et du validateur sont en annexe D.3. Une lecture découverte après le scellement est une déviation déclarée.
    9. **Le contrôle de processus devient un contrôle système** : les G1/G2 des lots B0, B-SEG, B, POOLEE et RENDU travaillent sur fixtures, au sens défini à l'annexe D.4 a (C-11). « Un seul rendu » = une exécution unique d'un script scellé, fail-closed (C-12, annexe D.4 b).
    10. Règle opérationnelle « R1 discrimine » (SHOGEN-CRITERE-R1-1, C-10 vi), écrite au paquet avant scellement, jamais après le rendu. Renvois : critère binaire de sortie S2 (doc 10 l.567-572 ; 05-roadmap l.123-127 ; question d'origine `s2-harness/README.md` l.5-7). Ce critère fixe le livrable (n, K, z, partition R2, k_eff contre k nominal) et la règle « résultat négatif = résultat ». Il ne définit pas la règle de décision. Candidats à trancher au paquet : le rejet du modèle d'indépendance du pool, « z au-delà du seuil 2,33 » (doc 10 l.386-388), et le drapeau 2, « z ≥ 2,33 avec partition sans recouvrement » (doc 10 l.535-537). D6 (vi) et D9 y renvoient.
    11. Sceau : ancre d'horodatage externe du sha du paquet, ou, à défaut, limite « sceau privé » déclarée (C-13, annexe D.4 c ; décision investisseur §4.10 b).
- **D3 — Estimateur de co-défaillance.**
  - **Structure à deux étages de doc 10 l.519-522 conservée (C-10 iv).**
    - Entre clusters R2 à au moins deux membres : la corrélation des séries (Θ̂_A,j, Θ̂_B,j), analogue de l'éq. 35 de L&M, reste l'estimateur principal.
    - Entre singletons : φ des indicatrices d'écart reste principal (pré-enregistré, doc 10 l.521-522).
  - Pour les paires de singletons (tables 2×2) : lift (membre gauche de l'éq. 28 de L&M) en secondaire déclaré ; odds ratio conditionnel en exploratoire, en attendant PXP-30 (§4.9).
  - Aucune significativité par paire : c'est du descriptif.
  - Publier l'identité φ = (lift−1)·√(p_A p_B / ((1−p_A)(1−p_B))), qui rend exacte la mention « proxy bruité ». Les quatre comptes par paire restent publiés (recalculables par tous).
  - `report.py:280` imprime « N_min = … (Fisher) » sans source détenue (F-DP-14, dette 10.7) : SHOGEN-REPORT-FISHER-1, avant le rendu.
- **D4 — Coupe du J14 rétroactif (C-9).**
  - **Principal** : [2026-08-26T19:00Z ; 2026-09-09T19:00Z), semi-ouvert (17 314 fenêtres). C'est la règle ex ante d'ADR-0022 pt 5 (« J14/J28 ré-ancrés à la date de lancement réelle »), introduite au commit `ed479c5` le 2026-08-26T18:58:57Z, une minute avant la 1ʳᵉ fenêtre (vérifié : cp-1 §2 ; `git log -S` du rédacteur).
  - **Décision 270** : la coupe transcrite avec 270 (≤ 2026-09-04T00:00Z) vient de l'orchestrateur MONARK, d'après RUNBOOK l.135, dont le J0 (21/08) est antérieur à ADR-0022 pt 5. **Elle est remplacée par la règle ex ante d'ADR-0022 pt 5. La décision de l'investisseur (270 : « il faut produire le J14 ») est exécutée.** La coupe du 04/09 (≤, 9 261 fenêtres) est rendue en second rendu, déclaré d'avance.
  - La troncature coupe **tous** les types d'enregistrements par horodatage (HS2-08).
  - Le J14 est non confirmatoire. Sa publication est une décision de l'investisseur (270 : « non publié sans décision investisseur » ; §4.4).
  - Erratum à poser (§8) : ADR-0023, conséquence 2, « J14 (~4 sept) / J28 (18 sept) » devient « J14 = [2026-08-26T19:00Z ; 2026-09-09T19:00Z) (ADR-0028 D4) ; J28 = segment d'ADR-0028 D2 pt 6 ».
- **D5 — Amendement d'ADR-0025 déc. 1 (veto §4.10 a : 269/272).**
  - L'exclusion s'étend à **tout enregistrement horodaté dans la plage** : `window_start` (fenêtres), `ts` (`asn_attribution`, 5 313 dont 815 `resolve_failed`), `harness_ts` (`clock_check`, 483). Les comptes sont déclarés au bloc 1.
  - *Bornes par type (FM-1.5)* : sur `window_start`, la plage fermée ratifiée [1790273880 ; 1790435280] (2026-09-24T18:18:00Z ; 2026-09-26T15:08:00Z). Sur `ts` et `harness_ts`, la même plage étendue à la durée de sa dernière fenêtre, soit [1790273880 ; 1790435340). C'est l'intervalle des comptes ci-dessus (AVIS-advisor-defi l.138 ; G2 du lot A §5, « [A ; B8+60) »).
  - Motif : `resolve_failed` 15,3 % dans la plage contre 1,85 % hors plage (santé du harnais DNS, pas une statistique de source ; causalité non établie). La partition R2 n'en dépend pas (11 hôtes, au moins 205 relevés après la plage). Une seule règle pour tous les types.
  - Plus, au lot B-SEG : SHOGEN-EXCL-COMPTE-1 (fenêtres retirées par plage et par strate au bloc 1) et refus des epochs négatifs (rc 2, Q-G2-5).
  - La sensibilité « plage incluse » reste au paquet. Texte d'amendement daté à poser en tête d'ADR-0025 (§8).

## 2. Décisions d'ingénierie

- **D6 — Statut du harnais S2 : le chemin de recalcul est de qualité produit, sous G0-G7 complets ; la collecte reste en quarantaine (réécrit selon cp-1 §4 pt 4 et C-5 ; R-22).**
  - R-22 (doc 02 l.111) interdit de promouvoir un prototype sans repasser G0-G7. Le chemin qui produit, recalcule et publie la sortie S2 repasse donc G0-G7. La position rejoint l'avis advisor-marché Q6 (« promouvoir le chemin de lecture et de recalcul, pas nécessairement tout le harnais », AVIS l.85-89), et non l'option C de l'avis advisor Q6 (annexe E).
  - **(i) Frontière**, tirée du graphe d'imports mesuré (`F:\tmp\shogen-carto-2026-09-29\harnais-s2.md` §1.1-1.3 ; frontière [inféré] de ce graphe) :
    - *Chemin de recalcul (produit)* : `records` (hors `append_asn`) avec son lecteur unique `read_jsonl_tolerant`, `window`, `r1`, `lm`, `r2` (hors `collect_asn`) et `report` ; les points d'entrée `recompute_*`, oracle tiers d'ADR-0003 ; leurs tests : `test_r1`, `test_lm`, `test_r2`, `test_report`, `test_exclusion`, `test_g2_adversarial`, `test_window`.
    - *Collecte (quarantaine, campagne scellée)* : `collector`, `sources`, `run_campaign`, `closure`, `smoke`, `journal` (écrivain unique `append_jsonl`), `model`, `r2.collect_asn` et `records.append_asn` ; leurs tests : `test_collector`, `test_sources`, `test_run_campaign`, `test_closure`.
    - Garde-fou (avis advisor Q6, l.48) : tout changement du harnais hors des lots de l'annexe A exige un G0.
  - **(ii) G0-G7 sur le chemin de recalcul** :
    - G0 = cette ADR, plus une ligne datée par lot (annexe A) ;
    - G1 = journal de provenance par lot ;
    - G2 = revue à 100 % par une instance séparée. La couverture G2 historique est établie par références : JOURNAL l.41 (incréments M1b à M2, « adjugé par oracle de recalcul + G2 à contexte frais », rapports non localisés dans le dépôt) ; JOURNAL l.42 (ADR-0021) ; `docs/adr-0022/G2-review.md` ; revue G2 du lot A. Les rapports du 2026-08-20 ne sont pas localisés : SHOGEN-G2-HISTO-RECALCUL-1, déclencheur « avant le rendu » ;
    - G3 : voir (iii) ;
    - G4 à G6 selon doc 02 ;
    - G7 = orchestrateur, puis cp-2.
  - **(iii) Job CI et G3.** Le job `s2-harness-unittest` (unittest de la bibliothèque standard, sans réseau, variable `SHOGEN_S2_CAMPAGNE_CONTROL` non posée) est ajouté à `gates.yml` au lot CI-S2, premier lot sous cette ADR. L'en-tête de `gates.yml` (l.3-6, « s2-harness est JETABLE ») est corrigé : « jetable » ne vaut plus que pour la collecte en quarantaine. Tant que la forge est morte (GC-01), le G3 opérant est l'oracle local, rejoué par l'orchestrateur, avec enregistrement d'oracle (viii).
  - **(iv) Défauts du rapport soldés avant le rendu** : HS2-05 (bloc 1 : dates de campagne) au lot B-SEG ; HS2-06 (bloc 3 : définition d'écart) et HS2-07 (bloc 6 : date de partition) au lot B ; HS2-11 (README, RUNBOOK) au lot DOCS-S2. Le bloc 6 est rendu avec la date de partition, en descriptif seulement (C-10 v). G10 (k_eff servi) reste après J28 (D9).
  - **(v) Sortie branchée** : `docs/11-mesures-pilotes.md`, consommé par MONARK comme fichier publié (arête G9). État aujourd'hui : **absent** (§3, C-17).
  - **(vi) Clause datée après J28 : décision de l'investisseur** (§4.10 b), sur la règle écrite au paquet (SHOGEN-CRITERE-R1-1). Si R1 discrimine : lot « benchmark continu » par un G0 neuf (réimplémentation dans le cœur, ou promotion G0-G7 de la collecte). Sinon, la collecte meurt comme prévu.
  - **(vii) Item PAROXYSME « mesure S2 hors produit »** (collecte en quarantaine), avec (vi) pour déclencheur. La quarantaine suppose que le format des journaux lus par le chemin de recalcul soit spécifié et scellé (condition de l'avis advisor-marché, AVIS l.88) : SHOGEN-FORMAT-JOURNAUX-1.
  - **(viii) Enregistrement d'oracle Shōgen, équivalent de CA-12 (C-4, Q-G2-4) — à ratifier.**
    - `scripts/oracle/run.mjs` (MONARK) est structurellement inapplicable : il lit `.github/workflows/ci.yml`, absent de Shōgen (G2 lot A §1).
    - Schéma retenu : `shogen.oracle-record.v1`, formalisation de la substitution du G2 du lot A (`F:\tmp\shogen-g2-lotA\sorties\oracle-G2-substitution.json`, schéma `shogen.g2.oracle-substitut.v1`, sha256 `c0ab619e2e17ef516685daa24f2e7b50f2dbf13673474c323446ddef66c9c434`).
    - Champs : `schema`, `role` (G1, G2, cp-2 ou rendu), `auteur` (modèle résolu), `tree.commit`, `tree.extraction`, `tree.sha256` par fichier, `base`, `static_only` (false exigé), `served_from` (null, ou chemin et sha d'un enregistrement conforme), `python`, `env` (dont la variable scellée, posée ou non), `runs` (nom, arbre, commande, chemin et sha256 de la sortie, exit, tests lancés avec la variable), `exit` (0 exigé), `ecrit` (ISO UTC).
    - Chemin : `F:/tmp/oracle-results/shogen-<sha court>-<role>-<date>-<pid>.json`.
    - Chaque réviseur le produit par ses propres commandes. Le cp-2 contrôle celui que cite le G2, comme en CA-12 (`validateur-humain.md` l.161-162) : rôle attendu, `tree.commit` égal au gel revu, exit 0, `static_only` false, `served_from` conforme.
    - Item SHOGEN-ORACLE-ENREG-1 : un enregistreur Python de la bibliothèque standard produit ce fichier en lançant la suite ; déclencheur : G0 du lot RENDU (sous-lot RENDU-2).
- **D7 — Custodie et push.**
  - Le bundle hors ligne est fait (`D:\shogen-sauvegarde-2026-09-29\`, sha 101d2385…). Il est à refaire à chaque commit de clôture tant que le push n'est pas complet.
  - Le préfixe `5b6469a…fa0ce5b` (7 commits, 0 fichier des docs 15/16) est poussable en avance rapide. L'acte a été refusé à l'orchestrateur par le contrôle d'autorisation le 2026-09-29 ; il est laissé à l'investisseur (§4.3). Le reste suit sa réponse sur le périmètre (§4.2).
  - Aucune réécriture d'historique (hash cités, main protégée).
- **D8 — Branche orpheline `roster-ban-alignment-2026-08-20`.**
  - Lots neufs D8a, D8b et D8c (annexe A ; le port mesuré dépasse le seuil R-25 en un seul lot). Ils portent `enforcement/` (lint de pinning et de bannissement, gate secrets), les jobs g1/g3, le motif g5 élargi et une **copie versionnée du hook pre-commit**. Pas les fichiers d'agents supplantés.
  - **Source canonique** : faute d'une amont retrouvée (`F:/VibeGates` absent, git-ci §2.b), la source devient le blob de `adb2213`. Sha cités : `enforcement/lint-model-pinning.sh` `457565f`, `enforcement/gate-secrets.sh` `6789a30`, `gates.yml` `493ae8c` ; hook `.git/hooks/pre-commit` sha256 `1da91c72…` (avis advisor Q8 pt 2, l.97).
  - **G1 du lot D8a (C-14)** :
    - acceptés : `claude-opus-5-5`, `claude-sonnet-5-5`, `claude-fable-5-1` ;
    - refusés : les tiers nus `opus`, `fable` et `sonnet` ; `claude-opus-5` ; `claude-opus-5[1m]` (suffixe de contexte entre crochets, forme mesurée le 2026-08-05) ; `claude-opus-5` suivi de tout autre chose que `-5` (collision de préfixe avec `claude-opus-5-5`, qui doit rester accepté) ;
    - cas limites, tranchés et testés au G0 de D8a (formés, non décidés ici) : `claude-opus-5-5[1m]`, forme résolue du G1 du lot A (JOURNAL l.86) ; `claude-sonnet-5`, retiré de l'usage mais non banni (décision 280).
  - Collision ADR-0020 consignée à DECISIONS (cause : sessions concurrentes du 2026-08-20 ; error_origin orchestrateur).
  - Un tag annoté signé `archive/roster-ban-2026-08-20` est posé sur `adb2213` et inclus au bundle, **puis** la branche est supprimée. Confirmation préalable de la décision du 2026-08-20 : §4.10 a.
- **D9 — Séquence PAROXYSME vers MONARK** (table G1-G16 de la cartographie §4) :
  - **T0 (MONARK, transmis)** : la correction de la vitrine publique Shōgen (claims sans support, vocabulaire 09) est **suspendue** jusqu'à la réponse de l'investisseur à l'escalade du cp-1 bis (§4.11) ; restent transmis les deux défauts du chemin servi : le recalcul de `sha256(utterance.bytes)`, et un `gate` qui ne lie que ce qui est vérifié (l'hôte). Garde G15 et glossaire G8. Propriétaire : orchestrateur MONARK.
  - **Voie A (dépend de S2)** : lot A (fait) → CI-S2 → B0 → B-SEG → B → POOLEE → RENDU (construction) → paquet scellé → **exécution unique** (J14 principal, J14 second, J28, sensibilités, oracle) → `docs/11` → cp-2 → G7 → clôture S2 → **G9**. La publication est un acte de l'investisseur, avec préavis privé à des acteurs nommés. L'exécution unique produit J14 puis J28, dans l'ordre de 270.
  - **Voie B (indépendante de S2, en parallèle)** :
    - G5 : liaison chemin + requête. Les options (a)/(b) sont **rendues au mainteneur** (DECISIONS l.1887-1904, « deux évolutions de forme ratifiée qui appartiennent au mainteneur » ; §4.10 a). Le lot suit sa décision.
    - G2 : vérificateur exécuté côté MONARK ; mesure de faisabilité wasm32 d'abord.
    - G8.
    - **Recherche G4** (notaire tiers, clé du notaire — PX-Shogen-3, F-DP-35) dès maintenant.
  - **Après J28 : bifurcation = décision de l'investisseur** (§4.10 b), sur cette proposition :
    - G10 (k_eff avec sa partition datée), puis S4 (G12-G14), si deux conditions tiennent : (i) R1 discrimine selon la règle du paquet (SHOGEN-CRITERE-R1-1) ; **et** (ii) un signal de demande est observé. Critère falsifiable de l'avis advisor-marché (§5, l.91-97) : dans les 90 jours après G9, au moins un acteur nommé et hors de l'équipe demande la méthodologie ou un certificat sur son propre pool, recalcule publiquement le chiffre, ou l'invoque au titre de DORA art. 29 (CASP MiCA).
    - Si (i) est faux : priorité à G4 et révision de 04 (doc 10 l.35-36 ; 05-roadmap l.126-127).
    - Si (i) est vrai et (ii) faux à 90 jours : question à l'investisseur (gap de packaging, AVIS-advisor-marche l.96).
- **D10 — Fin de S3.**
  - Maintenant, en parallèle : **E1 threat model** (Shōgen est déjà exposé via MONARK) et **distillation du corpus fuzz** (échue), lots E1 et FUZZ (annexe A).
  - Après la clôture S2 : Build L2, DEVOPS v2, audit de phase E (ils demandent une forge vivante).
  - **Passage public : décision de l'investisseur** (§4.10 b). Mécanisme proposé : export filtré (ADR dédiée ; le dépôt privé reste l'archive de preuve ; biblio/ exclu). L'alternative, la bascule de visibilité, publierait les docs 15/16 de l'historique (avis advisor Q7, Q10).

## 3. Tuyaux (règle Branchement ; CA-11 durci ; C-17)

- Entrée : journaux scellés `F:\shogen-campagne\campagne\` (sha `SHA256SUMS-cloture-2026-09-28.txt`).
- Sortie : `docs/11-mesures-pilotes.md`, consommé par MONARK (G9 : panneau ou page docs).
- État : sha des journaux, du paquet et du script de rendu au JOURNAL ; ancre externe du sceau ou limite « sceau privé » (D2 pt 11).
- Test de composition : **SHOGEN-S2-TUYAU-MONARK-1**, `shogen_s2_report_offline_recompute_matches_published` (nom proposé par la dimension MONARK de la cartographie, `monark.md` l.126, l.204).
  - Dépôt propriétaire : **MONARK**, là où vit le chemin servi. Shōgen fournit `docs/11` et les sha.
  - Déclencheur : **G0 du lot G9**.
  - Entrée : les journaux scellés, par sha, et `docs/11` commité. **Jamais un échantillon construit à la main.**
  - Dépendance déclarée : la publication des journaux (§4.4). Sans elle, la composition ne peut pas s'exécuter côté MONARK.
- **État du tuyau : absent.** `docs/11` n'existe pas, et le test n'est pas construit. S2 reste « upcoming » dans tout registre public (cohérent avec T0). L'oracle `recompute_*`, rejoué dans l'exécution unique, est un contrôle interne : ce n'est pas le test de composition.

## 4. Restent à l'investisseur (non techniques)

1. Facturation GitHub Actions (budget org à 0 $, cause non établie) : lire Billing & plans, décider la dépense.
2. Périmètre du « dépôt privé » : les docs 15/16 (vulnérabilité de tiers non divulguée) peuvent-ils aller sur le remote GitHub privé ? Sinon le bundle reste la custodie.
3. Push du préfixe sûr (commande fournie à l'investisseur). Conditions de l'avis advisor Q7 (d.2, l.72) : l'orchestrateur relit les 7 diffs (R-21) avant le push ; `.claude/launch.json` (JSON invalide, GC-13) part avec le préfixe.
4. Publication J14/J28 et G9, et contacts de préavis. Question ouverte : un contact **avant** les n/K/z est-il licite sous D8 ? La publication des journaux conditionne le test de composition (§3).
5. **Message public MONARK (règle Branchement, non discrétionnaire)** : ce qui n'est servi que comme fixture ou démo reste « upcoming » dans tout registre public. MONARK sert aujourd'hui une fixture S3 figée, sans exécuter le vérificateur (cartographie §4, l.56). La pièce Shōgen (capteur, vérificateur, mesures) est donc « upcoming » tant qu'aucune de ses sorties n'est consommée par un chemin servi couvert par un test d'intégration non-LLM. Au plus tôt : G2 (vérificateur exécuté) ou G9. L'outil MONARK `attest`, qui projette une fixture, ne vaut pas « Shōgen built ». La décision de l'investisseur porte sur la formulation publique de cet état et sur le calendrier de T0, pas sur le statut : la règle le fixe.
6. G4 : accord et dépense si un notaire commercial est requis.
7. Mesure de l'envergure : position institutionnelle (citations, recalculs) ou revenu. Les trajectoires diffèrent.
8. Canal 1 (cabinets de risque) : la reprise d'Aave par LlamaRisk sur Chainlink CRE aggrave le conflit. Réouverture éventuelle de D3 (ADR-0019).
9. Procurements :
   - **PXP-30** : Agresti, A., *Categorical Data Analysis*, 3ᵉ éd., Wiley (2013), ISBN 978-0-470-46363-5, 752 p. Aucun DOI enregistré à Crossref (`F:\tmp\shogen-carto-2026-09-29\FAITS-PXP-30-agresti-3e-2026-09-29.md`).
     - Parties visées (C-16). Numérotation relevée dans les transparents Agresti 2016 [lu] (`scratch/biblio-a-verser/2026-09-29/agresti-2016-short-course-cda-slides.txt`, sha256 `adf7d975…`) ; ces lignes n'indiquent pas l'édition, à confirmer à réception :
       - pp. 267-268 : estimateur « conditional ML » de l'odds ratio (transparents l.850) ;
       - §16.5-16.6 : intervalles « exacts » pour l'odds ratio (l.919) ;
       - en contexte : §3.1, inférence sur l'odds ratio (l.183) ; §3.5, test exact de Fisher, dont §3.5.6 (l.762, l.917).
     - **Usage exact** : fixer la méthode de l'estimateur exploratoire de D3, soit l'odds ratio conditionnel et son intervalle exact par paire de singletons. S'il est rendu après le scellement, il est déclaré « ajouté après le pré-enregistrement ». Non bloquant.
     - Tentatives : FAITS-PXP-30 (page éditeur lue ; Wiley Online Library : vérification Cloudflare non contournée ; Crossref : 0 DOI pour les 4 ISBN).
   - **PXP-20** : livré (Lopez Bernal 2016, sha `414cf7f3…`, JOURNAL l.92).
   - **P-M1..P-M5** : advisor-marché (AVIS l.106-111).
10. **Veto de l'investisseur, ouvert jusqu'au scellement du paquet (C-8).** Le scellement a lieu quand le sha du paquet est écrit au JOURNAL. L'orchestrateur porte cette rubrique au prochain point d'étape. Un veto avant le scellement rouvre la décision visée. Une décision changée après le scellement est une déviation déclarée au rapport.
    - **(a) Décisions de l'investisseur antérieures, amendées par délégation** :
      - **273** (forme et statut de la strate poolée ; famille de trois tests ramenée à deux confirmatoires) : D2 pt 4 ;
      - **269/272** (ADR-0025 déc. 1, étendue par D5 à tout type d'enregistrement horodaté) ;
      - **ADR-0023** : son statut (l.3) réserve l'acceptation à l'investisseur. D1 l'accepte, avec le pt 5 amendé ;
      - **options G5 (a)/(b)**, réservées au mainteneur (DECISIONS l.1887-1904) : **rendues** au mainteneur, non tranchées ici ;
      - **choix que les avis réservaient à l'investisseur et que cette ADR tranche par délégation** (annexe E) :
        - blocs de dépendance plutôt que résidu déclaré (AVIS-advisor-defi Q2 pt 9, l.61, l.70) ;
        - publication d'un résultat poolé comme exploratoire, décision de message (AVIS-advisor Q2, l.202) ;
        - confirmation que la décision du 2026-08-20 (« full opérationnel, zéro résidu ») tient dans sa forme g1/g3/g5, préalable de D8 ; sinon D8 devient un ADR de retrait motivé (AVIS-advisor Q8, l.105).
    - **(b) Décisions nouvelles de l'investisseur, avec leur déclencheur** :
      - **passage public** (D10) : mécanisme (export filtré ou bascule de visibilité) et divulgation des docs 15/16. Déclencheur : clôture S2 (G7) ;
      - **lot « benchmark continu »** (D6 vi) : déclencheur, le J28 rendu et la règle SHOGEN-CRITERE-R1-1 évaluée ;
      - **bifurcation après J28** (S4, G4, révision de 04 ; D9) : déclencheur, le J28 rendu ; puis, si R1 discrimine, la fin des 90 jours qui suivent G9 ;
      - **ancrage externe du sceau du paquet** (C-13) : déclencheur, la rédaction du paquet achevée, avant son scellement. Le mainteneur est concerné : ADR-0006 pt 3 réserve l'ancrage « dès l'existence du benchmark public (S2) » (DECISIONS l.311-314).

### 4.11 Réponses de l'investisseur (2026-09-29)

Questions posées par l'orchestrateur (message du 2026-09-29, verbatim, extraits) et réponse verbatim de l'investisseur : « on maisse comme ça sur le site monark, on continue de build shogen. vérifies en local et ok pour pocket. »

- **Forge (§4.1)** — question : « GitHub Actions ne tourne plus parce que le budget du compte est à 0 $. → Reco : dans les réglages GitHub (Billing), mets un petit budget. Sinon on continue à vérifier en local, et ça marche aussi. » Réponse : « vérifies en local » — l'investisseur retient la seconde branche offerte. **G3 opérant = l'oracle local** (`cargo --locked xtask verify` + suite `unittest` du harnais, rejoués par l'orchestrateur et consignés au JOURNAL à chaque lot) ; le job CI du lot CI-S2 est écrit mais ne sert de preuve qu'une fois la forge vivante. L'absence de budget est la conséquence de ce choix, pas une réponse explicite.
- **Pocket (§4.2)** — question : « Les documents Pocket (la faille trouvée chez Pocket, pas encore divulguée) : peuvent-ils être stockés sur GitHub, même en privé ? → Reco : non tant que l'accord avec Pocket ne le dit pas. Ils restent sauvegardés sur ton disque D:. » Réponse : « ok pour pocket » — accord avec la recommandation, donc **non** : les docs 15/16 ne vont pas sur le remote GitHub, même privé, tant que l'accord avec la Pocket Foundation ne l'autorise pas ; custodie = bundle hors ligne (`D:/shogen-sauvegarde-2026-09-29/`), refait à chaque clôture (SHOGEN-BUNDLE-CLOTURE-1) ; le push éventuel se limite aux préfixes sans ces fichiers.
- **Vitrine MONARK (§4.5)** — question : « Le site MONARK présente Shōgen comme « terminé » (« built »). En réalité, ce qu'il montre n'est qu'une démonstration. → Reco : afficher « en démonstration » jusqu'à la publication des premiers chiffres. » Réponse : « on maisse comme ça sur le site monark ». **Non enregistrée comme décision ni comme limite PAROXYSME** tant que l'investisseur n'a pas répondu à l'escalade du cp-1 bis : cette réponse vaut-elle dérogation datée à la règle Branchement du 2026-09-19 (« upcoming » tant qu'aucune sortie n'est consommée par un chemin servi testé) pour Shōgen sur le site MONARK, jusqu'à G2 ou G9 ? Item SHOGEN-VITRINE-MONARK-1 (annexe B).
- **Build (§4)** — « on continue de build shogen » : confirmation du plan (voies A et B de D9).

### 4.12 Décisions de l'orchestrateur (non investisseur)

- **CONS-1 (consultation du rédacteur, 2026-09-29)** : option (i) retenue — l'attestation de l'auteur (annexe D.3 a) reste masquée sur ses deux valeurs chiffrées, pour que l'ADR demeure lisible par les rédacteurs frais du paquet (C-7).
- **CB-6** : la version soumise au cp-1 est conservée — reconstituée par l'orchestrateur à partir de son texte d'écriture, sha256 `6060a0bfb25f6526afe45454d70aaea0044fc2b2a00cdc97370e87420fff78b6`, identique au sha relevé par le cp-1 : `F:/tmp/cp1-adr0028/ADR-0028-version-soumise-cp1.md`.
- **Rustup (cp-1 bis, AM-1)** : la cible `thumbv7em-none-eabi` installée par erreur par le validateur sous `F:/rust/rustup` (2026-09-29 19:40:18Z) a été retirée par l'orchestrateur (`rustup target remove`, 2026-09-29) ; état antérieur rétabli.

## 5. Items formés

La table complète est en **annexe B**. Chaque item y a un propriétaire, un déclencheur et une origine. Les quatre items sans déclencheur relevés par le cp-1 en ont maintenant un : SHOGEN-TASK-72H-1, -SCHED-MONITOR-1, -TAU-REDERIV-1 et -TESTS-TMP-1. Les items que demande C-15 sont ajoutés.

## 6. Lots (C-3)

La table des lots est en **annexe A** : véhicule, oracle non-LLM nommé, taille estimée (R-25), tuyau, type de cp-1, ordre. Sous cette ADR, **un cp-1 bref n'est recevable que pour un lot qui a sa ligne datée à l'annexe A** et qui est marqué « bref » (amendement « cp-1 BREF », `validateur-humain.md` l.169-170). Les lots marqués « complet » passent un cp-1 complet. Toute coupe R-25 ajoute une ligne datée, par amendement daté de l'annexe.

## 7. Risque résiduel MAST (C-2)

Les modes MAST et leurs contre-mesures sont en **annexe C** : FM-1.1, FM-2.4, FM-3.2, FM-3.3, FM-1.5, plus FM-2.3. Les 14 modes restent la checklist de revue de sprint (corpus doc 06 l.269).

## 8. Actes d'écriture hors de ce dossier, à poser par l'orchestrateur au commit de cette ADR

Le rédacteur n'écrit que dans `docs/adr-0028/`. Aucun des actes ci-dessous n'est posé. Item SHOGEN-ERRATA-ADR0028-1 (annexe B) :

1. erratum en tête d'ADR-0023 : l.11, « 20:00 UTC » devient 19:00Z (D1) ; conséquence 2, J14/J28 (D4) ;
2. amendement daté en tête d'ADR-0025 déc. 1 (D5) ;
3. JOURNAL : décision 273 (arête E48 absente), ADR-0028 et ouverture du veto (§4.10) ;
4. index DECISIONS : ADR-0024 à ADR-0028 (REG-02 ; l'index s'arrête à ADR-0023, l.27) ;
5. registre PAROXYSME-Shogen référencé par sha (`a655c401…`) dans le dépôt (SHOGEN-PAROXYSME-REGISTRE-1) ;
6. transmission à l'orchestrateur MONARK de MONARK-S2-M009A-EXPOSITION-1, de SHOGEN-S2-TUYAU-MONARK-1 et de SHOGEN-VITRINE-MONARK-1 (CB-4).
