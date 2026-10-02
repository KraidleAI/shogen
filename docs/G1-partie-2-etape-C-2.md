# Journal G1 — partie 2 de S2, étape C, sous-lot C3

**Nature de ce journal** : journal de provenance du worker de la session cloud, travail du 2026-10-02 de 08:46 à 09:1x
UTC (horloge lue par `date -u` : 08:46:10 au départ, 09:00:46 avant la rédaction ; clôture au §10). Contrat :
`docs/adr-0028/G0-partie-2.md` (sha256 `b6c1dfa9…`), section « C — RENDU-1 » (l.106-145) et son ajout daté du
2026-10-02 08:44 UTC (l.170-172), lus en entier avec les ajouts de l'étape B (l.147-168). Branche `partie-2-rendu`,
HEAD `1bc1142` (inchangé pendant le travail). **Issue : arrêt avant tout code.** Le brief impose d'écrire d'abord la
table des sorties de D.4 b, puis, si une définition est introuvable ou ambiguë, de ne pas l'inventer et de rendre la
question : la table (§2) porte quatre points de définition ouverts (§3, Q1 à Q4) et quatre choix de construction qui
en dépendent (§4, Q5 à Q8). Aucun fichier du dépôt n'est modifié ; seul ce journal est neuf. Aucune opération git en
écriture. Preuves et sonde : `…/scratchpad/lot-C3/`.

## 0. Gate 0

Modèle résolu sous lequel le worker a tourné : **`claude-opus-5-5`** (identifiant exact fourni par l'environnement de la
session ; préfixe attendu `claude-opus-5-5` : conforme). Effort : `max` (fiche du worker et brief).

## 1. Provenance

### 1.1 Sources lues (toutes [lu] ; aucune [abs] ni [2nd])

- `CLAUDE.md` (racine, rappelé par la session) ; `docs/PASSATION-CLOUD.md` l.1-273, en entier (`f728657f…`), après un
  `grep -n` de contrôle des mentions de D.2 (seules l.126-128 répondent, texte de règle).
- `docs/adr-0028/G0-partie-2.md` l.1-172, en entier.
- `docs/adr-0028/ANNEXE-D-preenregistrement.md` (`5fc0cbc1…`) : l.107-151 (D.4 a, b, c), l.28-45 (fin de D.1, D.2 liste
  fermée, lue pour s'en garder), et les titres d'un `grep -n` (l.7, 30, 44, 107, 126, 140, 143, 144, 152) ; l.152-173
  (D.5).
- `docs/adr-0028/ADR-0028-decisions-sortie-S2.md` (`bc146415…`) : l.1-248 (§1, §1 bis entier, §2 D6 à D10, §3) ; les
  l.249-327 (§4 à §8) ne sont pas lues.
- `docs/adr-0028/ANNEXE-B-items.md` (`b227fede…`) : l.347-397 (blocs B.22 à B.25, en entier), et les lignes d'un
  `grep -n` (l.16, 17, 52, 57, 89, 100, 101, 108, 163, 173, 213, 310, 325, 343).
- `docs/adr-0028/ANNEXE-A-lots.md` (`35922ca0…`) : l.36-38 (RENDU-1, RENDU-2) et les lignes d'un `grep -n` (l.19, 21,
  28-32, 89, 90) ; `docs/adr-0028/PLAN-PARTIE-2.md` l.1-70 et `docs/adr-0028/PARTIES-S2.md` l.1-22, en entier.
- `docs/G1-partie-2-etape-C-1.md` l.1-402 (`cc4f63cd…`), `docs/G1-partie-2-etape-B-2.md` l.1-381 (`60754608…`, dont §3)
  et `docs/G1-partie-2-etape-B-3.md` l.1-352 (`a9a5b02e…`, dont §3), en entier.
- `docs/G1-lot-B-SEG-1-segment.md` (`49ccdc79…`) l.55-75 et les lignes d'un `grep -n` (l.5, 42, 152, 163, 171, 174) ;
  `docs/G1-lot-B-sensibilite.md` (`8762dff1…`), lignes d'un `grep -n` (l.31, 40, 66, 78, 85, 86, 88, 180, 190, 217,
  218, 219, 231, 246, 249, 251) ; `docs/17-modele-de-menace.md`, lignes d'un `grep -n` sur `T-13\|T-16\|T-17`
  (l.82, 94, 97, 99, 104, 107, 108) ; `s2-harness/RUNBOOK-campagne.md` (`8d68ee97…`) l.225-260 et les lignes d'un
  `grep -n` (l.17, 135, 136, 138, 144, 180).
- Code, en entier : `s2-harness/tools/rendu_unique.py` (l.1-273), `tools/oracle_record.py` (l.1-250),
  `shogen_s2/report.py` (l.1-785), `shogen_s2/records.py` (l.1-414) ; en partie : `shogen_s2/r1.py` l.690-827,
  `shogen_s2/lm.py` l.204-239, `shogen_s2/r2.py` l.1057-1092, et les définitions d'un `grep -n` sur ces modules.
- Tests : `tests/test_rendu_unique.py` l.1-376 et `tests/test_oracle_record.py` l.1-315, en entier ;
  `tests/test_sensibilite.py` l.1-215 ; lignes d'un `grep -n` des définitions de `test_exclusion.py` et
  `test_d5_amend.py`.
- Gates : `enforcement/hooks/pre-commit` l.15-30 (motif R-13, l.21) ; `enforcement/gate-secrets.sh`, lignes d'un
  `grep -n` (motifs VENDOR et GENERIC, l.57-58) ; `xtask/src/sg4.rs`, lignes d'un `grep -n` (liste des locutions,
  l.31-163).
- Scratchpad : `regle_fixtures.py` (`5557fb56…`, imposé par le brief, utilisé tel quel) ;
  `lot-B2/outils/precheck_md.py` (`1b46b7cb…`, utilisé tel quel pour ce journal) ; `lot-C1/` (liste des fichiers).
- Système : Python 3.11 (`python3`), git de l'hôte ; `date -u`.

### 1.2 Pré-enregistrement (annexe D)

- D.4 a : fixtures seulement. Hors de la suite, le code d'analyse n'a tourné que par `regle_fixtures.py` (fixtures de
  `test_critere`) et par la sonde du §1.4 (fixture de `tests/test_sensibilite.py` : collecteur réel, w = 3 600 s,
  statuts scriptés) ; aucun journal de campagne, aucune copie scellée, aucun réseau.
- D.2 : aucune pièce ouverte. ADR-0025 et `docs/rapports/cartographie-2026-09-29.md` n'ont pas été ouvertes et sont
  exclues de tout `grep` (`--exclude-dir=adr-0025`, `--exclude=cartographie-2026-09-29.md`) ; par prudence,
  `JOURNAL.md` et `docs/pocket-report/` aussi ; la copie de `JOURNAL.md` du scratchpad n'a pas été ouverte.
- Exposition déclarée (D.3, FM-2.4) : comptes de fenêtres et bornes de segment et de plage écrits dans ADR-0028 (D2
  pt 6, D4, D5 ; non interdits par D.2) ; le préfixe `351f51b2…` de `PASSATION-CLOUD.md` l.141 et l'épingle
  `SHA_CONTROL_SCELLE` de `tests/test_exclusion.py` l.43, affichée par un `grep -n` (sha256 seuls, admis par D.2 n° 7) ;
  des lignes affichées par des `grep` larges, sans autre lecture : `docs/15-etude-pocket-network-2026-09-25.md` l.75,
  l.281, l.284, `docs/DECISIONS.md` l.2645, `docs/rapports/r1-sweep-2026-07-30.json` l.48, `docs/adr-0023/ADR-0023.md`
  l.39, `docs/G1-lot-POOLEE-strate-poolee.md` l.8 et l.216, et des lignes de G1 de lots antérieurs. Aucun taux par
  source, aucun z, K, P̂ ni φ de campagne. Rien de cela n'entre dans un code ou un test.
- `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée : `env | grep -c` rend 0 au départ ; la suite, la règle et la sonde tournent
  sous `env -u SHOGEN_S2_CAMPAGNE_CONTROL`.

### 1.3 Commandes lancées et sorties (scratchpad `lot-C3/`)

- `git rev-parse --abbrev-ref HEAD`, `git rev-parse HEAD` : `partie-2-rendu`, `1bc114285b1bc060aa069feee0ae7cf99a84fc89`
  (commit du 2026-10-02 08:45:41 UTC) ; `git status --porcelain --untracked-files=all` : vide.
- `git archive --format=tar HEAD | tar -x -C lot-C3/arbres/HEAD` ; `diff -rq --exclude=__pycache__` de
  `arbres/HEAD/s2-harness` et de l'arbre de travail : identiques.
- Suite (arbre de travail) : `Ran 356 tests in 37.801s`, `OK (skipped=2)` (`preuves/suite-depart.out` `64aad2c3…`).
- Règle scellée : `regle_fixtures.py` sur l'export de `HEAD` et sur l'arbre de travail : sha256 du JSON
  `ea3a2d94ef1075603e8f7cfc53c68b26e51729b61714028e3fb03dc32f79cb29` dans les deux cas (`cmp` : identiques) ; égal à la
  référence du brief.
- Epochs des bornes, calculés par `datetime(…, tzinfo=timezone.utc).timestamp()` : 2026-08-26T19:00:00Z = 1787770800 ;
  2026-09-09T19:00:00Z = 1788980400 ; 2026-09-04T00:00:00Z = 1788480000, plus w = 60 s : 1788480060. Contrôle inverse
  des bornes de D5 (ADR l.59) : 1790273880 = 2026-09-24T18:18:00Z ; 1790435280 = 2026-09-26T15:08:00Z ; 1790435340 =
  2026-09-26T15:09:00Z (conformes au texte).
- Sonde (§1.4) : `preuves/sonde-sorties.out` (`4af5421a…`) ; rendus dans `sondes/` ; comptes de lignes et d'étiquettes
  par `grep -c` (§3).

### 1.4 Outil écrit (scratchpad `lot-C3/outils/`)

`sonde_sorties.py` (`e51f9a81…`) : sur la fixture de `test_sensibilite`, quatre appels de `report.render_report` de
`HEAD` (forme J14 : segment qui finit avant la plage, sans puis avec la plage ; forme J28 : segment à n fixe, avec puis
sans la plage), diff ligne par ligne, et relevé des lignes d'étiquette et de la règle. Ce n'est pas un livrable : il
mesure la conséquence, en octets, des options des questions Q1, Q2 et Q4.

## 2. Table des sorties de D.4 b (écrite avant tout code)

Ordre et liste : annexe D l.119 (« Elle produit, dans cet ordre : J14 principal (D4) ; J14 second (coupe de 270) ; J28
(D2 pt 6) ; chaque sensibilité de la liste fermée (D2 pt 7) ; l'oracle tiers `recompute_*` sur chaque sortie ;
l'enregistrement d'oracle (D6 viii), avec le sha de chaque sortie »). Fonction de rendu commune :
`report.render_report(control_path, journal_path, exclude_ranges=(), segment=None)` (report.py l.140), même calcul que
la CLI `python -m shogen_s2.report <dossier> [--segment-from T0 (--segment-to T_FIN | --segment-n-fixe N)]
[--exclude-window-start-range A B]` (report.py l.753-781 ; RUNBOOK §9 e, l.239-257). ℓ n'est pas une option :
`r1.ELL_BLOC = 240` (r1.py l.66), constante unique pour tous les segments et toutes les strates (ADR l.121).

| # | sortie | définition lue | fonction existante | options exactes | état |
|---|---|---|---|---|---|
| 1 | J14 principal | ADR D4 l.52 : [2026-08-26T19:00Z ; 2026-09-09T19:00Z), semi-ouvert ; l.54 : troncature de tous les types (HS2-08) ; l.55 : non confirmatoire ; §1 bis.1 pt 9 l.108 : hors décision, imprimé et étiqueté | `render_report` | `segment={"t0": 1787770800, "t_fin": 1788980400}` ; `exclude_ranges` : **Q2** ; étiquette du pt 9 : **Q4** | segment déterminé ; plages et étiquette ouvertes |
| 2 | J14 second (coupe de 270) | ADR D4 l.53 : coupe « ≤ 2026-09-04T00:00Z », second rendu déclaré d'avance ; même objet que la « seconde coupe J14 (270) » de la liste fermée (§1 bis.2 l.118) ; G1 de B-SEG-1 l.62 : `--segment-to` = 2026-09-04T00:00:00Z + w | `render_report` | `segment={"t0": ?, "t_fin": 1788480060}` : début **introuvable (Q3)**, lecture proposée 1787770800 ; `exclude_ranges` : **Q2** ; étiquette : **Q4** | fin déterminée ; début, plages et étiquette ouverts |
| 3 | J28 | ADR D2 pt 6 l.37 : [2026-08-26T19:00:00Z ; T_fin), T_fin = `window_start` de la 38 600ᵉ fenêtre distincte + 60 s, exclusion ADR-0025 dans le segment ; D5 l.59 : plage fermée [1790273880 ; 1790435280] sur `window_start`, [1790273880 ; 1790435340) sur `ts` et `harness_ts` ; §1 bis.1 pt 1 l.93 : segment de la règle | `render_report` ; T_fin par `records.t_fin_n_fixe` (records.py l.378) dans `records.filtre_lecture` (l.388) ; extension + w par `records.filtre_horodatage` (l.350), w de `run_params` | `segment={"t0": 1787770800, "n_fixe": 38600}` ; `exclude_ranges=[(1790273880, 1790435280)]` | déterminé (étiquette : Q4) |
| 4 | chaque sensibilité de la liste fermée | §1 bis.2 l.118 : liste amendée = plage ADR-0025 exclue ou incluse ; seconde coupe J14 (270) ; pt 9 l.108 ; D5 l.62 ; annexe D.5 l.159, l.171 ; annexe B l.213 (SENS-PLAGES-1) ; G1 du lot B l.219 | « plage incluse » : section `[SENSIBILITÉ]` de `render_report`, imprimée dès qu'une plage est passée (report.py l.682-748, R1 seul par variante) ; « seconde coupe » : la sortie 2 | **Q1** : nombre et forme des sorties | ambigu |
| 5 | oracle tiers `recompute_*` sur chaque sortie | D.4 b l.119 ; D6 (i) l.187 ; SHOGEN-RECALCUL-TIERS-CLI-1 (annexe B l.365) ; SHOGEN-CENSURE-CAUSES-TIERS-1 (l.378) ; brief | `r1.recompute_from_journal` (r1.py l.771), `r1.recompute_d5_from_journal` (l.813) ; ventilation : `r1.fenetres_sautees_vivant` (l.734) sur `records.demarrages` (records.py l.316) ; hors brief : `lm.recompute_lm_from_journal` (lm.py l.204), `r2.recompute_r2_from_journal` (r2.py l.1057) | options de chaque sortie 1 à 4 | construction de l'item ; portée : **Q6** ; liste : Q1 |
| 6 | enregistrement d'oracle avec le sha de chaque sortie | D.4 b l.119 ; ADR D6 (viii) l.205 (champs) ; §1 bis.6 l.143 ; G0 §C l.130-133 ; SHOGEN-RENDU-T0-1 (annexe B l.394) | `oracle_record.enregistrer` (tools/oracle_record.py l.104), relu par `verifier` (l.163) | rôle `rendu`, `paquet.sha256`, `sceau.genTime` (voie (a)) ; sha de chaque sortie : seulement par `runs[].sortie.sha256` (schéma fermé) : **Q5** | construction : Q5 |

Hors de la liste de D.4 b, au même brief : verdict de `records.verifier_raw(raw_path, journal_path)` (records.py l.109 ;
SHOGEN-RAW-FIN-1, annexe B l.354 ; G0 l.158), imprimé et enregistré sans fermer l'exécution : place et support, **Q7**.

## 3. Pourquoi l'arrêt : définitions ambiguës ou introuvables (questions bloquantes)

Constats de la sonde (fixture de `test_sensibilite`, code de `HEAD`) : forme J14 sans plage 366 lignes, avec une plage
hors du segment 389 lignes ; forme J28 avec la plage 399 lignes, sans la plage 392 lignes. Dans les quatre rendus :
0 occurrence de « J14 », de « J28 » et de « non confirmatoire » ; 1 ligne de la règle
`« R1 discrimine » (§1 bis.1 pt 6 ; déclencheur de D6 (vi) et D9) = …`.

- **Q1 (sensibilités : quelles sorties, sous quelle forme).** La liste amendée (ADR l.118) compte deux sensibilités. La
  « seconde coupe J14 (270) » est la sortie 2, que D.4 b nomme déjà à son rang. La « plage incluse » est produite par
  `render_report` lui-même, section `[SENSIBILITÉ]`, dès qu'une plage est passée : le lot B l'a construite pour RENDU
  (G1 de B l.219), SENS-PLAGES-1 la place « au rendu J28 » (annexe B l.213), D.5 y met les pertes (l.171). D.4 b
  la range pourtant comme une étape propre, après J28. Trois lectures :
  - (a) aucune sortie de plus : la sensibilité « plage incluse » est la section `[SENSIBILITÉ]` de la sortie 3, qui suit
    ses blocs 1 à 6 dans le même fichier (l'ordre de D.4 b tient dans le fichier) ; la seconde coupe est la sortie 2 ;
    trois rendus en tout ;
  - (b) une sortie 4 = `render_report(c, j, exclude_ranges=(), segment={"t0": 1787770800, "n_fixe": 38600})`, rendu
    complet de la variante incluse : la sonde montre que ce rendu imprime la règle et sa ligne « R1 discrimine » sans
    étiquette de sensibilité, et recalcule L&M et R2 sur la variante (forme J28 sans plage contre avec plage : +75 −82
    lignes, blocs 1 à 6 recalculés, section absente), alors que le lot B s'en tient à « R1 seul par variante » ;
  - (c) une sortie 4 qui ne porte que la section `[SENSIBILITÉ]` du J28 : aucune fonction existante ne la produit seule
    (code neuf dans `report.py`, ou découpe de la sortie 3).

  Lecture du worker, non appliquée faute de décision : (a).
- **Q2 (plage D5 aux deux J14).** D4 (l.51-56) ne nomme pas la plage ; D5 (l.57-62) exclut tout enregistrement horodaté
  dans la plage ; le pt 1 de la règle (l.93) ne la nomme que pour le J28. La plage tombe après les deux fins de J14
  (1788980400 et 1788480060 < 1790273880) : les valeurs des blocs 3 à 6 ne changent pas, les octets si. Sonde, forme
  J14 : avec la plage, +23 lignes, 0 retirée (quatre lignes `exclusion_*` au bloc 1, puis une section `[SENSIBILITÉ]` de
  19 lignes, ligne vide comprise, à variantes égales, écart de z 0). Options : (a) J14 sans plage ; (b) plage passée à
  toutes les sorties (règle uniforme).
- **Q3 (début du J14 second).** D4 l.53 ne donne que la coupe ; le G1 de B-SEG-1 l.62 fixe `--segment-to` =
  1788480060 et pas `--segment-from`, que l'API exige (`records.filtre_lecture`, l.396-399). Lecture proposée : t0 =
  1787770800, début du J14 principal (D4 l.52, qui cite ADR-0022 pt 5 : J14 ré-ancré au lancement réel). Les
  enregistrements de démarrage datés avant t0 sont hors segment, comme aux sorties 1 et 3 (SHOGEN-SEG-DEMARRAGE-1,
  annexe B l.89). À confirmer.
- **Q4 (étiquette des J14 : pt 9, texte scellé).** Le pt 9 (l.108) veut les J14 principal et second « imprimés et
  étiquetés », hors décision (D4 l.55 : non confirmatoires). `render_report` imprime la section de la règle et la ligne
  « R1 discrimine » sur tout segment, sans étiquette de segment (sonde ; `grep` de `report.py` : aucune occurrence de
  « J14 », « J28 » ni « non confirmatoire »). Sur les J14, la strate stress tombe sous la garde de blocs par
  construction (ADR l.122) : une valeur NON ÉVALUABLE peut s'imprimer sans étiquette. Options : (a) en-tête posé par le
  script en tête de chaque sortie (texte à fixer par l'orchestrateur ; sous Q5 (a), l'en-tête doit être imprimé par la
  commande nommée elle-même, sinon le sha consigné ne serait plus celui du fichier) ; (b) option d'étiquette du rendu
  (`report.py`, défaut sans étiquette : épingles inchangées) ; (c) aucune étiquette, limite déclarée (contraire à la
  lettre du pt 9). Sous-question : le J28 porte-t-il aussi une étiquette (segment de la règle, pt 1) ?

## 4. Constructions à fixer avec les réponses (proposées, non codées)

- **Q5 (sha de chaque sortie dans l'enregistrement).** Le schéma est fermé (ADR l.205, ratifié A-12 ; G1 B-3 L4 : une
  clé de plus amenderait le schéma) : une sortie n'y entre que comme `runs[].sortie` {chemin, sha256}. (a) Chaque
  sortie est un run : commandes nommées de la liste fermée, lancées par l'enregistreur sur l'extraction de HEAD, dans
  l'ordre de D.4 b, chacune la ligne de commande du rendu avec les options de la table, puis `recalcul-tiers` ; la suite
  y entre aussi (HOOK-SUITE-S2-1, G0 l.134-135) ; `--verifier` (rôle rendu) recalcule alors le sha de chaque sortie
  (contrôle « sortie » existant). Prix : un paramètre substitué dans les commandes nommées (dossier des journaux ; liste
  fermée, jamais un shell). (b) Rendus écrits en processus par le script ; leurs sha n'entrent dans l'enregistrement
  qu'à travers la sortie d'un run (le JSON de `recalcul-tiers`, par exemple), et `--verifier` ne les recalcule pas.
  Recommandation : (a). Ordre proposé des runs : suite d'abord (voir Q8), puis sorties 1 à 4, `recalcul-tiers`, verdict
  `raw`.
- **Q6 (portée de `recalcul-tiers`).** D.4 b dit `recompute_*` ; D6 (i) (l.187) range au chemin de recalcul les
  points d'entrée `recompute_*`, qui existent dans r1, lm et r2 ; l'item (annexe B l.365) et le brief :
  `recompute_from_journal` et `recompute_d5_from_journal`, avec la ventilation de B5. `recompute_lm_from_journal` et
  `recompute_r2_from_journal` restent-ils hors de la commande (blocs 4 à 6 sans JSON tiers dans l'enregistrement) ? Sous
  Q1 (a), le JSON couvre-t-il aussi la variante incluse du J28 (`exclude_ranges=()`), source des lignes « incluse » de
  la section ?
- **Q7 (verdict de `records.verifier_raw`).** Annexe B l.354 : imprimé et enregistré, sans fermer l'exécution.
  (a) Commande nommée `raw` dont la sortie porte le verdict (conforme et comptes, ou refus et motif) et dont l'exit
  est 0 dans les deux cas (non nul seulement si elle ne peut pas s'exécuter) : l'enregistrement reste conforme au
  `--verifier` ; (b) fichier écrit par le script dans le répertoire de sortie, hors enregistrement. Recommandation :
  (a), après `recalcul-tiers`, hors de l'ordre de D.4 b.
- **Q8 (échec après les rendus).** Le brief veut, à tout échec, une sortie non nulle et aucun répertoire de sortie. Un
  échec postérieur aux rendus (suite rouge, écriture de l'enregistrement) efface des sorties déjà calculées sur les
  journaux scellés. La relance est-elle une seconde exécution, donc une déviation déclarée (D.4 b l.127), ou une
  exécution qui n'a pas eu lieu ? Construction proposée : suite lancée avant tout rendu et arrêt au premier échec, pour
  que l'échec le plus probable précède toute lecture des journaux ; la qualification de la relance reste à décider.

Constructions sans question, que le sous-lot fixera et déclarera : nom du répertoire de déviation (suffixe numéroté),
fichier du motif dans ce répertoire, refus de `--deviation` sans première exécution, `tree.commit` = HEAD et `base` =
`commit_analyse`, `sceau.genTime` en ISO 8601 UTC (voie (a)) ou nul (voie (b) seule), `--auteur` exigé, sha256 de
chaque sortie imprimé pour la ligne du JOURNAL (D.4 b l.118), refus de `--sortie` présent avant toute garde.

Coupe proposée après réponse (prix [inféré]) : **C3a** (≈ 110) `oracle_record.py` : SHOGEN-ENREG-AUTEUR-ECRITURE-1
(refus avant toute commande), commandes nommées paramétrées, arrêt au premier échec (si Q8 le retient) ; **C3b**
(≈ 150) `r1.py` (et `records.py` au besoin) : clé de ventilation dans `recompute_d5_from_journal`
(SHOGEN-CENSURE-CAUSES-TIERS-1), entrée `recalcul-tiers` (JSON par sortie, `Decimal` en chaîne), commande `raw`, tests
d'égalité avec le rendu (forme du B3) ; **C3c** (≈ 190) `rendu_unique.py` : table des sorties et étiquettes,
SHOGEN-RENDU-T0-1, production par l'enregistreur dans un répertoire temporaire voisin, renommage, `--deviation`,
nettoyage à tout échec ; test nominal sur un dépôt jetable qui porte une copie de `shogen_s2/` et `tools/` (commandes
lancées sur l'extraction), une suite de fixture triviale (pas de récursion de la vraie suite), des journaux du
collecteur réel et une table des sorties injectée en processus (comme `PREFIXES` en C2a) ; nouvelle coupe si un
sous-lot dépasse 200 lignes.

## 5. Sous-lots

Aucun : arrêt avant code (§3). Numstat : 0 ligne ; aucun diff dans `lot-C3/` ; aucun mutant (aucun test neuf). Suite
au départ et à la fin : 356 tests, `OK (skipped=2)` (§10). Règle scellée : `ea3a2d94…`, inchangée. Épingles
`SHA_BASE_SANS_OPTION` et `SHA_BASE_AVEC_OPTION` : inchangées (aucun rendu modifié, aucune re-capture).

## 6. Empreintes

- Fichiers que C3 touchera, inchangés à `1bc1142` (sha256) : `s2-harness/tools/rendu_unique.py`
  `7b0212fd72e4fa3413c664ec29fa2b9f6fa93ae7ed460098b337ded6a7d25e64` ; `s2-harness/tools/oracle_record.py`
  `9d8553f33d1f44721072b65d225f1d1db1a649d49b9f1f35eda58c20cb4ee509` ; `s2-harness/shogen_s2/r1.py`
  `27a6e3d4e2258c5b9150017881b534a52dde343b617f4b2d5c6b4244bf7dfc57` ; `s2-harness/shogen_s2/records.py`
  `22924dfaa55f2072b6e964bc2ba576e6c10eed5bd7b5e5b924c05a5497cae503` ; `s2-harness/shogen_s2/report.py`
  `52bbae680c6e38115b8effc7bac616def99edb8b74f1dc0a23074cb7477ab338` ; `s2-harness/tests/test_rendu_unique.py`
  `ea5a0a39e1ce834ebbcb7e8cef07c39cb53c56e6291782d311145d16ef8e1320` ; `s2-harness/tests/test_oracle_record.py`
  `5fbd5cd882f1d364fa1ce5109d642fb32478536737f78a9d1fdd871e09e54b0a`.
- Preuves (scratchpad `lot-C3/`) : `preuves/suite-depart.out` `64aad2c3…` ; `regle/HEAD.json` et `regle/travail.json`
  `ea3a2d94…` ; `outils/sonde_sorties.py` `e51f9a81…` ; `preuves/sonde-sorties.out` `4af5421a…` ; rendus de la sonde
  `sondes/j14_sans_plage.txt` `ef4a714a…`, `j14_avec_plage.txt` `3e661eec…`, `j28_avec_plage.txt` `616bbf9d…`,
  `j28_sans_plage.txt` `8c8c3d17…`.
- Ce journal : sha256 dans le rapport de remise (un fichier ne porte pas son propre sha).

## 7. Écarts

- **E1 (issue)** : arrêt avant tout code, sur la consigne du brief ; aucun des cinq points du « À FAIRE » n'est livré ;
  la table des sorties et les questions tiennent lieu de livrable.
- **E2 (sonde)** : une sonde a été écrite et lancée dans le scratchpad (fixture, code de `HEAD`), pour chiffrer en
  octets les options de Q1, Q2 et Q4 ; elle ne touche pas le dépôt et n'est pas un livrable.
- **E3 (prudence de lecture)** : `JOURNAL.md` et `docs/pocket-report/` exclus des `grep`, en plus des exclusions du
  brief (précédent du G1 de C1 et C2).

## 8. Limites rencontrées (items à former, règle PAROXYSME)

- **L1 — SHOGEN-RENDU-ETIQUETTE-1** : le rendu n'imprime aucune étiquette de segment ; le pt 9 (texte scellé) exige que
  les J14 soient imprimés et étiquetés hors décision. Construction : Q4. Déclencheur : décision de l'orchestrateur, puis
  sous-lot C3. Prix ≈ 10 lignes et un test [inféré] (davantage sous Q4 (b) : option et épingles).
- **L2 — SHOGEN-RECALCUL-TIERS-PORTEE-1** : sous la construction de l'item, les blocs 4 à 6 (L&M, R2, drapeaux) n'ont
  pas de JSON tiers dans l'enregistrement du rendu, alors que D.4 b dit `recompute_*`. Construction : étendre
  `recalcul-tiers` à `recompute_lm_from_journal` et `recompute_r2_from_journal`, ou limite écrite au PAQUET.
  Déclencheur : Q6. Prix ≈ 10 lignes et un test d'égalité [inféré].
- **L3 — SHOGEN-RENDU-NOMS-JOURNAUX-1** : le rendu lit `control.jsonl` et `journal.jsonl` dans le dossier des journaux,
  `verifier_raw` lit `raw.jsonl` et `journal.jsonl` ; le bloc machine (G0 l.116-118) porte trois lignes `journal <nom>
  <sha256>` sans en fixer les noms : un bloc à d'autres noms passerait la garde (3) puis ferait échouer la production.
  Construction : la production exige ces trois noms au bloc (refus avant tout rendu), ou le G0 du PAQUET les fixe.
  Déclencheur : sous-lot C3 ou G0 du PAQUET. Prix ≈ 3 lignes et un test [inféré].
- **L4 — SHOGEN-RENDU-TABLE-REELLE-1** (anticipée) : la table réelle des sorties (bornes de D4, n fixe 38 600, plage de
  D5) ne peut pas tourner de bout en bout sur fixture sans un journal synthétique de plus de 38 600 fenêtres ; le test
  nominal injectera une table de fixture, et la table réelle ne sera contrôlée que contre des constantes écrites à la
  main depuis l'ADR. Première exécution de bout en bout : l'exécution unique (partie 4). Construction : test des
  constantes (attendus indépendants), plus une mesure sur journal synthétique si son coût est tenable. Déclencheur :
  sous-lot C3. Prix ≈ 10 lignes de test [inféré].
- **L5 — SHOGEN-RENDU-ECHEC-TARDIF-1** : voir Q8 ; un échec après les rendus efface des sorties calculées sur les
  journaux scellés, et la nature de la relance n'est pas écrite. Déclencheur : décision de l'orchestrateur avant C3 ;
  texte au PAQUET. Prix : deux lignes de texte et l'ordre des runs [inféré].

## 9. Questions ouvertes

- **Q1** : sensibilités de la liste fermée : (a) section `[SENSIBILITÉ]` du J28, aucune sortie de plus ; (b) rendu
  complet du J28 sans plage ; (c) section seule en sortie distincte ?
- **Q2** : plage D5 passée aux deux J14, ou non ?
- **Q3** : début du J14 second = 1787770800 (2026-08-26T19:00:00Z) ?
- **Q4** : étiquette du pt 9 : par qui (script, commande nommée ou option du rendu), avec quel texte ; le J28 en
  porte-t-il une ?
- **Q5** : sorties comme runs de l'enregistreur (a), ou rendus en processus (b) ?
- **Q6** : `recalcul-tiers` limité à r1 et d5 (avec ventilation) ; variante incluse du J28 comprise ?
- **Q7** : verdict `raw` par commande nommée à exit 0, ou par fichier hors enregistrement ?
- **Q8** : relance après un échec tardif : seconde exécution (déviation déclarée) ou non ; suite avant tout rendu ?

## 10. Clôture

- Suite finale (arbre de travail, inchangé, 09:03 UTC) : `Ran 356 tests in 39.214s`, `OK (skipped=2)`
  (`preuves/suite-fin.out` `4eea6d91…`) ; `SHOGEN_S2_CAMPAGNE_CONTROL` absente (`env | grep -c` : 0).
- `cargo --locked xtask verify` à 09:04 UTC, avec une version de ce journal dans `docs/` qui précède ce paragraphe :
  `=== VERDICT GLOBAL : VERT ===`, rc 0 (`preuves/xtask-1.out` `7d47963a…`) ; S-G4 78 fichiers sur 78 (76 de `docs/`, 2
  de `s2-harness/`), S-G5 79 sur 79, 252 fragments contrôlés, 2 885 écartés sous seuil, corpus complet (125 artefacts
  sur 125), 0 violation. Relance sur la version finale : verdict et sha256 de ce fichier dans le rapport de remise.
- `git status` final : ce journal seul, neuf ; rien de modifié.
