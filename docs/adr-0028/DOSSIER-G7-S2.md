# Dossier de preuves G0 à G6 du chemin de recalcul de S2 (lot CP2-G7, préparation du G7 et du cp-2)

Lecteur `shogen-lecteur`. Brief : `scratchpad/cp2-g7/BRIEF-DOSSIER-G7.md`, sha256 recalculé
`336f5dfeed267bdb0d813d7e5621054b186b44a16bb423b2aa49fc01df6feef6` (égal à celui donné). `date -u` : 2026-10-04 09:00:59 UTC
au départ, 09:10:14 UTC avant la rédaction. Dépôt `/home/user/shogen`, branche `partie-4-execution`, tête
`b24ff8676d6fdfff4baad22f9163033a6f0e65a6` (`git status --short` vide au départ et à la fin).

**Ce dossier ne conclut pas le G7.** Il rassemble les preuves et signale les réserves ; le verdict est à l'orchestrateur.

## 0. Gate 0, attestation, commandes

- **Gate 0** : modèle résolu `claude-opus-5-5` (identifiant exact fourni par l'environnement de la session). Attendu par
  l'orchestrateur : `claude-opus-5-5` (lecture qui exige du jugement, roster CLAUDE.md §7) : conforme. Effort `high`
  demandé, non observable depuis la session.
- **Pièces non ouvertes** : aucune pièce de la liste D.2 ; rien sous `docs/15-*`, `docs/16-*`, `docs/pocket-report/`,
  `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/` ; aucun `*.jsonl` ; aucun journal de campagne. Toutes
  les recherches `grep -r` ont exclu ces dossiers à la source (`--exclude-dir`, `--exclude`). `cargo xtask verify` non lancé.
- **Expositions déclarées** (rien n'est recopié ici) :
  1. `JOURNAL.md` l.316 affichée (tronquée) : valeurs de résultat du J28 (z, K, n) déjà versées au dépôt ;
  2. `PAQUET-PREREG-S2.md` l.51 : comptes et deux taux de `resolve_failed` (classe M) ;
  3. 300 premiers octets de la sortie `…943.4-recalcul-tiers.out` : un fragment de borne de censure ; puis clés JSON seules ;
  4. sortie `…943.5-raw.out` lue en entier (443 o : verdict `raw`, cinq horodatages et noms de flux) ; fin de
     `…943.0-suite.out` et ses deux lignes de saut ;
  5. annexe B.50 et B.53 (valeurs exploratoires et synthétiques déjà versées).
  L'extraction en mémoire de `git archive 27b0e30` (contrôle de `tree.sha256`, §5) a fait passer tous les fichiers du commit,
  dossiers interdits compris, par un calcul de sha256, sans aucun affichage ni écriture.
- **Écritures** : ce fichier. Écart déclaré : le rejeu du §2 (G3) a écrit une sortie `scratchpad/cp2-g7/suite-head.out`
  (sha256 `eeb1705e7140dad608aae8233dd1dcf8acd73d9ca40e77fe49e73cf891c7f36a`) et les répertoires temporaires des tests sous
  `scratchpad/cp2-g7/tmp/` ; les deux ont été supprimés. Aucune opération git en écriture ; aucun fichier suivi modifié ;
  `PYTHONDONTWRITEBYTECODE=1` et `-B` partout ; `SHOGEN_S2_CAMPAGNE_CONTROL` retirée.
- **Commandes** (lecture) : `date -u` ; `git log`, `git show --stat`, `git diff --stat|--quiet`, `git merge-base
  --is-ancestor`, `git grep` (motif g5), `git archive` (en mémoire) ; `sha256sum` ; `grep`, `sed`, `awk` sur des fichiers
  nommés ; `python3 -B s2-harness/tools/oracle_record.py --verifier … --role rendu --commit 27b0e303…` (sans `--depot`) ;
  un script Python de lecture du JSON d'enregistrement ; `python3 -B enforcement/verdict-suite-s2.py` et
  `python3 -B enforcement/tests/run-fixtures-verdict-suite-s2.py`.

## 1. Objet et périmètre

- **Frontière** (ADR-0028 D6 (i), l.186-189) [lu] : `records` (hors `append_asn`), `window`, `r1`, `lm`, `r2` (hors
  `collect_asn`), `report`, points d'entrée `recompute_*`, et leurs tests ; le brief y ajoute `tools/rendu_unique.py`.
  L'inventaire du 2026-10-02 compte **neuf modules** (`INVENTAIRE-G2-RECALCUL.md` l.74) : `rendu_unique.py`,
  `oracle_record.py`, `report.py`, `lm.py`, `r1.py`, `r2.py`, `records.py`, `window.py`, `model.py` [lu].
- **G0 d'ADR-0028** : commit `ce63fed` (2026-09-29 20:59:49 +01:00) [lu].
- **État du chemin** : dernier commit qui touche `s2-harness/shogen_s2`, `tools` ou `tests` : `b6c1c95` (DETTES-B1, B1-7) ;
  `git diff --quiet b6c1c95 HEAD` sur ces trois chemins : vrai (seul `README.md` a bougé depuis, `dad3bc6`) [lu].
- **Deux arbres à ne pas confondre** [lu] :
  - arbre des rendus : commit d'analyse `f35a70c` (bloc machine du paquet, `PAQUET-PREREG-S2.md` l.215), tête gardée de
    l'exécution `27b0e30`, identique à `f35a70c` sur les chemins gardés (`git diff --quiet` vrai) ;
  - arbre de la tête : `shogen_s2` et `tools` diffèrent de `f35a70c` (+52 −26, quatre fichiers, lot DETTES-B1). La procédure
    le dit : « La procédure ne se rejoue donc qu'à `f35a70c`. » (`PROCEDURE-EXECUTION.md` l.85).
  Le G7 et le cp-2 doivent nommer le gel qu'ils jugent (voir §6, point 1).

## 2. Table G0 à G6

Définitions au dépôt : `docs/AUDIT-ENTREE.md` §1 (l.13-20) ; ADR-0028 D6 (ii) l.191-196, (iii) l.197 ; §4.11 l.291 et
amendements datés l.296-300. Le doc 02 du corpus est hors dépôt (poste local) : non lu [abs].

| gate | exigence (au dépôt) | preuves (fichier:ligne, commit) | état |
|---|---|---|---|
| **G0** | AUDIT l.13 : « Specs + ADRs + modèle de menace + exigences réglementaires ». D6 (ii) l.191 : « G0 = cette ADR, plus une ligne datée par lot (annexe A) ». Garde-fou D6 (i) l.189 : tout changement hors lots de l'annexe A exige un G0. | ADR-0028 `ce63fed` ; annexe A l.15-145 : chaque lot du §3 a sa ligne datée (CI-S2 l.15, B0 l.16-18, B-SEG l.19-27, B l.28-32, POOLEE l.33-36, RENDU l.37-38, DOCS-S2 l.60-63, B-DEP l.64-72, CRITERE l.73-78, D5-AMEND l.79-82, partie 2 l.87-117, partie 3 l.118-124, CORR l.130, DETTES-A l.133, DETTES-B1 l.134) ; G0 de partie : `G0-partie-2.md`, `G0-partie-3.md`, `G0-lot-CORR.md`, `G0-lots-DETTES.md` l.22 (DETTES-B1) et l.26 (CP2-G7). Les 81 commits `ce63fed..HEAD` qui touchent `s2-harness/` se rangent tous dans un lot de l'annexe A (rapprochement par sujet de commit et fichiers) [lu]. Modèle de menace : `docs/17-modele-de-menace.md`, « méthode et chemin S2 » (AUDIT l.52) [lu]. | **tenu** |
| **G1** | AUDIT l.14 : provenance des artefacts générés. D6 (ii) l.192 : « G1 = journal de provenance par lot ». | Journaux au dépôt : `docs/G1-lot-B0-pool-analyse.md`, `-B-SEG-1-segment`, `-B-SEG-2-bloc1`, `-DOCS-S2`, `-B-sensibilite`, `-POOLEE-strate-poolee`, `-B-DEP-1-blocs`, `-B-DEP-2-bloc3`, `-CRITERE-regle`, `-D5-AMEND-descriptifs`, `G1-partie-2-etape-A`, `-etape-B-1..3`, `-etape-C-1..3`, `-corrections-G2`, `G1-partie-3-P3`, `-P3g`, `G1-lot-CORR` (sha256 `1849053c…ac56`), `G1-lot-DETTES-B1` (`61c9b86d…89ef`) [lu]. Le journal central `docs/journal-provenance.md` s'arrête au 2026-09-28 (l.30) : les journaux par lot en tiennent lieu [inféré]. | **tenu avec réserve** : CI-S2 (`19db9d9`, `gates.yml`) n'a son G1 qu'au message de commit et au JOURNAL l.108 [2nd] ; DETTES-A (`23c1fc0`, README seul) n'a pas de journal G1 au dépôt [abs]. Aucun item ne porte ces deux réserves. |
| **G2** | AUDIT l.15 : revue 100 % + checklist ; « Adopter la checklist du corpus (templates/checklist-revue-G2.md) dès la prochaine PR de code. » D6 (ii) l.193 : « G2 = revue à 100 % par une instance séparée ». D6 (viii) l.207 : « Chaque réviseur le produit par ses propres commandes. Le cp-2 contrôle celui que cite le G2 ». | Au dépôt [lu] : `G2-partie-2.md` (`0b45a458…14d9`), `G2-partie-3.md` (`c6e3962a…c138`), rattrapages `G2-RATTRAPAGE-R-A.md` (`d2fdd8cc…3b77`, r1, records, window, model entiers à `41f087e`), `-R-B.md` (`894ed219…86a4`, r2, lm, report entiers), `-R-C.md` (`f06a69f0…4a97`, corrections de la partie 2), `G2-lot-CORR.md` (`96210705…680c`), `G2-lot-DETTES-B1.md` (`0e0acfe1…473f5c`). SHOGEN-G2-HISTO-RECALCUL-1 FERMÉ (registre TSV l.39 ; annexe B.40-B.44). Les changements du chemin après `41f087e` sont ceux de CORR et de DETTES-B1, chacun revu au dépôt. Lots de la partie 1 : rapports hors dépôt, cités [2nd] (§3). | **tenu avec réserve** : (1) les tests de Phase A (`test_r1`, `test_lm`, `test_r2`, `test_report`, `test_window`, cités par D6 (i)) n'ont pas de relecture G2 au dépôt : les rattrapages portaient sur les modules (INVENTAIRE l.60-74) [lu] ; (2) aucune relecture G2 au dépôt ne mentionne la checklist du corpus (`grep -il checklist` : 0) [abs] ; (3) aucune relecture G2 au dépôt ne cite un enregistrement de rôle G2 (recherche des noms `shogen-<sha>-G2-…json` : 0) [abs] : le contrôle « celui que cite le G2 » n'a pas d'objet au dépôt. Aucun item ne porte ces trois réserves. |
| **G3** | AUDIT l.16 : tests, SAST, dépendances. D6 (iii) l.197 : « Tant que la forge est morte (GC-01), le G3 opérant est l'oracle local, rejoué par l'orchestrateur, avec enregistrement d'oracle (viii) ». §4.11 l.291 : « G3 opérant = l'oracle local (`cargo --locked xtask verify` + suite `unittest` du harnais, rejoués par l'orchestrateur et consignés au JOURNAL à chaque lot) ». Amendements l.296-300 : `model-pinning : 95 ok` et lint ; `secrets : 147 ok`, `--tree`, `--history`, `--hors-refs` « consigné au JOURNAL à chaque G3 avec ses deux comptes » ; `hooks : 54 ok` et `install-pre-commit.sh --verifier` ; à partir de `30db124`, `verdict-suite-s2 : 20 ok` et `verdict-suite-s2.py` « conforme », `Ran 405`. | JOURNAL l.364 (DETTES-B1) : suite 405 OK (skipped=2), vérificateur conforme ; annexe A l.134 : `xtask verify` VERT à chaque commit ; `G2-lot-DETTES-B2.md` l.62-70 : runners 146/54/95, `verify` VERT, vérificateur conforme `Ran 405` (à `dad3bc6`/`d97ce4a`) ; annexe B.51 : `verify` VERT sur l'arbre réel. **Mon rejeu à `b24ff86`** (09:05 UTC, Python 3.11.15) : `verdict-suite-s2.py` sortie 0, `Ran 405 tests`, `OK (skipped=2)`, « conforme » ; lanceur `20 ok, 0 échec`, sortie 0. Dépendances : bibliothèque standard seule (README l.17 ; imports relus) [lu]. Contrôles de l'exécution : `Ran 398`, `OK (skipped=2)` sur l'arbre des rendus (§5). | **tenu avec réserve** : (1) le G3 opérant complet (toutes les commandes de §4.11) n'est consigné au JOURNAL pour aucune tête postérieure à DETTES-B2 ; les deux comptes de `--hors-refs` n'apparaissent dans aucune ligne du JOURNAL (`grep`) [abs] ; à rejouer au commit du G7, sortie de `verify` redirigée (SHOGEN-SG5-NOTES-INTERDITS-1) ; (2) forge morte : le job CI ne vaut pas preuve (SHOGEN-CI-S2-FORGE-1, SHOGEN-G3-FORGE-1, décisions de l'investisseur) ; (3) aucun SAST sur le code Python du chemin [abs] ; (4) SHOGEN-CI-S2-CABLAGE-1 (annexe B l.760). |
| **G4** | AUDIT l.17 : « Fitness functions + métriques + description d'architecture 42010 » ; « Baseline métrique à poser au premier code. » AUDIT l.37 : « À relever au premier commit de code produit (condition G3/G4 ci-dessus). » D6 (ii) l.195 : « G4 à G6 selon doc 02 ». | Description d'architecture partielle : frontière D6 (i) (graphe d'imports) et INVENTAIRE §1 (neuf modules, imports relus) [lu]. Contrôles qui jouent un rôle de fonction de fitness : plancher du vérificateur (`PLANCHER = 405`), règle `ea3a2d94…` et épingles contrôlées à chaque lot (annexe A l.130, l.134), mutants [lu]. **Métriques R-15** (duplication, churn, ratio refactoring/ajout) : aucune mesure au dépôt après le point zéro « s.o. » d'AUDIT l.31-35 (recherche `churn`, `42010`, `point zéro`, `R-15`, `fitness` : seul AUDIT répond) [abs]. Aucun item de l'annexe B ne porte le G4 du chemin [abs]. | **non tenu en l'état des preuves** : la baseline métrique exigée au premier code produit n'existe pas ; le reste est partiel. À trancher par l'orchestrateur (§6, point 2). |
| **G5** | AUDIT l.18 : TODO nus ; registre de dette. CLAUDE.md pt 6 : clôture, « section dettes vide ou en PR-x/recherches ». | Motif g5 de `gates.yml` l.69 lancé par `git grep` sur `s2-harness` et `enforcement/verdict-suite-s2.py` : aucune sortie (code 1) [lu]. Registre : annexe B (B.1 à B.53) ; état au 2026-10-04 03:46 UTC (`ETAT-REGISTRE-2026-10-04.md`, à `7cfa0df`) mis à jour ici par les blocs B.47 à B.53 (§4) [lu]. | **tenu avec réserve** : SHOGEN-ERRATA-ADR0028-1 a un déclencheur échu (« au commit de cette ADR », annexe B l.61 ; restent §8 pts 2, 5, 6 et actes 8, 13 à 16, B.48) ; trois actes sont dus à la clôture même et deux d'entre eux ne se font que sur le poste local (§4 a). Aucun état consolidé du registre après B.53 : la liste du §4 est ma reconstruction [inféré]. |
| **G6** | AUDIT l.19 : SBOM, licences, réglementaire ; « ne jamais rendre ce dépôt public sans purge de biblio/ ». | Aucune dépendance tierce : « Zéro dépendance hors bibliothèque standard Python (≥ 3.9) » (README l.17) [lu]. Licence du dépôt : `LICENSE-MIT`, `LICENSE-APACHE` ; ADR-0017 « MIT OR Apache-2.0 » (`docs/14-dossier-licence-adr-0014.md` l.3-5) [lu]. Aucune distribution : publication = G9, acte de l'investisseur (SHOGEN-DOCS11-PUBLIC-1, SHOGEN-PASSAGE-PUBLIC-EXPORT-1). Python de l'exécution consigné (`3.11.15`, enregistrement « rendu »). | **tenu avec réserve** : aucune pièce G6 écrite pour le chemin (SBOM, même vide ; revue réglementaire) [abs] ; purge de `biblio/` et réglementaire reportés à G9 et au passage public. Observation : `r2.py` l.62-65 importe `socket` et `urllib` (pour `collect_asn`, hors frontière) [lu]. |

Note sur l'ordre (sans effet sur ce dossier) : D6 (ii) l.196 dit « G7 = orchestrateur, puis cp-2 », alors qu'ADR-0028
l.224 et l'annexe A l.9 et l.11 écrivent « `docs/11` → cp-2 → G7 » [lu]. Le brief suit D6 (ii).

## 3. Lots qui ont touché le chemin depuis le G0 d'ADR-0028 (`ce63fed`)

Source : `git log ce63fed..HEAD -- s2-harness` (fichiers par commit), annexe A, journaux G1, JOURNAL. « AAC » =
ACCEPTE-AVEC-CORRECTIONS. Les lots SIM-NIVEAU, POST-PREREG et DETTES-SIM ne touchent pas `s2-harness/`
(`scripts/sim/`, `scripts/post-s2/`) ; DETTES-B2 non plus (`xtask`, `enforcement`, `gates.yml`).

| lot (commits) | G1 versé ? | G2 versé ? | verdict | corrections appliquées ? |
|---|---|---|---|---|
| CI-S2 (`19db9d9`, `gates.yml`, D6 iii) | non : message de commit et JOURNAL l.108 [2nd] | non : déclaré au message (« G2 worker distinct … 5 corr ») [2nd] | AAC | oui, au même commit (message) [2nd] |
| B0, B0-1, B0-2 (`0abc881`) | oui `docs/G1-lot-B0-pool-analyse.md` | non : `F:\tmp\shogen-lots\B0\G2-rapport.md`, sha tronqué `1c2d2b32…d892` (G1 l.218) [2nd] | AAC C-1..C-6 | oui, intégrées à `0abc881` |
| B-SEG-1 (`dc39cb8`, `83f86d8`, `05cff36`, `b72509b`) | oui | non : sha complet `cc8f2b50…9c5c` (G1 l.205) [2nd] | AAC C-1..C-6 | C-1..C-3 en `05cff36` (tests) |
| B-SEG-2 (`c385d52`, `8878200`, `5e0c09b`) | oui | non : `e778cef1…22de` (G1 l.257) [2nd] | AAC C-1..C-9 | C-1..C-5 en `5e0c09b` |
| DOCS-S2-a (`4d49757`) | oui `G1-lot-DOCS-S2.md` | non : rapport non nommé, aucun sha (JOURNAL l.135) [2nd] | C-1..C-10 | oui (coupe a1/a2, C-10) |
| B (`082d457`, `e47a425`, `cf2a1ba`, `b923a71`) | oui | non : `47307159…bef8` (G1 l.231) [2nd] | AAC C-1..C-10 | C-1..C-5 en `b923a71` |
| POOLEE (`57d1857`, `f70421b`, `de87b90`) | oui | non : `d5d87ca9…6ce7` (G1 l.224) [2nd] | AAC C-1..C-10 | C-1..C-3 en `de87b90` (tests) |
| B-DEP-1 (`6c524a5`, `09c1a50`, `d0b9663`) | oui | non : `5cd2ff40…f11e` (G1 l.286) [2nd] | AAC C-1..C-7 | C-1..C-4 en `d0b9663` |
| B-DEP-2 (`1775309`, `52ed450`) | oui | non : aucun sha cité (G1 l.16) [2nd] | C-1..C-4 | C-1..C-3 en `52ed450` (B-DEP-2c) |
| CRITERE (`d23706a`, `ca6011c`, `eb3453d`, `6c57039`, `3a51b7c`) | oui | non : JOURNAL l.191 seul, ni chemin ni sha [2nd] | AAC C-G2-1..6 | oui, `3a51b7c` |
| D5-AMEND (`8de4062`, `8b9ec48`, `b323f03`) | oui | non : `fd731fed…efdf0` (G1 l.181) [2nd] | C-1..C-3 | oui, dans les sous-lots (annexe A l.79-82) |
| Partie 2, étape A (`957525a`, `37db486` = DOCS-S2-b, `1ed1c29`) | oui `G1-partie-2-etape-A.md` | oui `G2-partie-2.md` [lu] | AAC C-1..C-11 | oui : G2a-G2f |
| Partie 2, étape B (`270d09a`, `1c35b49`, `fd498a0`, `5cb791e`, `0ad3655`, `cbd3f7d`, `ff4ce8c`, `24dd734`, `6fde16b`, `e5d989b`) | oui `-etape-B-1..3` | oui `G2-partie-2.md` | AAC | oui : G2a-G2f |
| Partie 2, étape C (`f939c05` … `eba5071`, onze commits) | oui `-etape-C-1..3` | oui `G2-partie-2.md` | AAC | oui : G2a-G2f |
| Corrections G2 de la partie 2, G2a-G2f (`3ef3b25`, `093c076`, `cfc67f5`, `81b8a87`, `04553a7`, `15d831e`) | oui `G1-partie-2-corrections-G2.md` | oui, en rattrapage `G2-RATTRAPAGE-R-C.md` | ACCEPTE-AVEC-CONSTATS (B-1, H-1, C-1..C-5) | oui : items RAW-CHEMIN-1, RENDU-MKDTEMP-1, TESTS-C8-SUITE-1 fermés par CORR (B.44) |
| Partie 3, P3a-P3g (`39f5cd2`, `b47ff24`, `a4e44d0`, `ced5cb6`, `a6a99d8`, `d69c914`, `cc37c8c`) | oui `G1-partie-3-P3.md`, `-P3g.md` | oui `G2-partie-3.md` (périmètre `0711cc1..86a8a5b`, les sept commits y sont) | AAC C-1..C-4 | C-1 en item, C-2..C-4 appliquées (B.35) |
| Rattrapages R-A, R-B (sans commit ; modules entiers à `41f087e`) | — | oui (§2) | CONSTAT-A chacun (A-1) | oui : SHOGEN-PRIX-NON-FINI-1 et SHOGEN-RECALCUL-JSON-COPIE-1 fermés par CORR |
| CORR (`02f9c00`, `4002239`, `35cd2e2`, `4c831b8`, `e4bc2f1`, `a5a9de9`, `f35a70c`) | oui `G1-lot-CORR.md` | oui `G2-lot-CORR.md` | AAC, K-1 et K-2 (tests) | oui, `f35a70c` |
| DETTES-A (`23c1fc0`, README seul, hors modules) | non [abs] | oui `G2-lot-DETTES-A.md` | AAC C-1..C-6 | oui (B.48) |
| DETTES-B1 (`0221a74`, `53cff2c`, `6b4b49c`, `0789d96`, `3cc0892`, `30db124`, `b6c1c95` ; README `dad3bc6`) | oui `G1-lot-DETTES-B1.md` | oui `G2-lot-DETTES-B1.md` | AAC C-1..C-5 | oui : C-1, C-2 au code (B1-1, B1-6) ; C-3..C-5 par l'orchestrateur (B.49) |

Lecture : tout lot a un G1 et un G2 déclarés. Pour la partie 1 (CI-S2 à D5-AMEND), les rapports G2 sont hors dépôt [2nd].
Les rattrapages R-A et R-B, au dépôt, relisent en entier l'état de `41f087e` des sept modules de calcul. Ils tiennent lieu
de ces rapports pour les modules, pas pour les tests (réserve G2 (1)).

## 4. Items ouverts de l'annexe B sur le chemin de recalcul ou sur S2

État de départ : `ETAT-REGISTRE-2026-10-04.md` (à `7cfa0df`) ; fermetures et formations ensuite : B.47 à B.53 [lu].
Les items fermés depuis l'état du registre ne sont pas repris (exemples : TEST-ENV-HERMETIQUE-1, CI-S2-SAUT-1,
KEFF-NOTE-1, POOLEE-BLOC-1, FLUX-QUASI-MORT-1 et -2, SIGMA-BLOC-INDEP-1, ENREG-VARIABLE-1).

### (a) Bloquants pour la clôture de S2, ou dus à la clôture même

| item (annexe B) | motif |
|---|---|
| **SHOGEN-INSTRUMENT-S2-1** (l.22) | C'est l'objet même : « D6 : frontière recalcul/collecte, G0-G7 sur le chemin de recalcul ». Restent le G7 et le cp-2 (ci-dessous). |
| **SHOGEN-CP2-RUNS-RENDU-1** (l.425) | Contrôle exigé au cp-2 (« au cp-2, contrôler que l'enregistrement de rôle « rendu » porte les runs exigés ») ; préparé au §5. |
| **SHOGEN-ERRATA-ADR0028-1** (l.61 ; B.48) | Déclencheur « au commit de cette ADR », échu depuis le 2026-09-29. Restent §8 pts 2 (amendement en tête d'ADR-0025), 5, 6 et actes 8, 13 à 16 de §1 bis.11. Une dette à déclencheur échu ne passe pas une clôture « zéro dette » : poser, ou re-dater par décision écrite. |
| **SHOGEN-D8-AMONT-ERRATUM-1** (l.200) | Reste « cartographie de clôture S2 à corriger » : acte dû à la clôture (cartographie sous `docs/rapports/`, que je n'ouvre pas). |
| **SHOGEN-PAROXYSME-REGISTRE-1** (l.50) | Mise à jour L-36..L-53 due à « cartographie de clôture S2 » ; fichier sur le poste local (classe G) : impossible en cloud. Re-dater ou déclarer à la clôture. |
| **SHOGEN-BUNDLE-CLOTURE-1** (l.23) | « chaque commit de clôture, tant que le push n'est pas complet » ; bundle sur `D:` du poste local (classe G). Le commit de clôture de S2 le déclenche. |
| **SHOGEN-E1-AVIS-FRAICHEUR-1** (l.140) — conditionnel | « avant tout vert d'avis cité au cp-2 de clôture S2 ». `cargo deny` absent de l'hôte cloud (registre §9). Le brief du cp-2 doit exclure toute citation d'un vert d'avis, ou l'acte doit être fait avant. Le chemin Python n'a aucune dépendance tierce. |
| Réserves sans item (§2) | G4 non tenu ; G2 (1) à (3) ; G3 (1) ; G1 (CI-S2, DETTES-A). Aucune n'a d'identifiant à l'annexe B : il faut les former ou les disposer par écrit avant le G7 [inféré]. |

### (b) Non bloquants, avec jalon futur

| jalon | items (annexe B, ligne) |
|---|---|
| **déclenché par le G7 lui-même** | SHOGEN-PASSAGE-PUBLIC-EXPORT-1 (l.29, déclencheur « clôture S2 (G7) » ; décision de l'investisseur) : devient dû au G7, sans le bloquer. |
| **G9 (publication) ou son G0** | SHOGEN-DOCS11-PUBLIC-1 (l.687) ; -REJEU-HOTE-1 (l.683 ; rejeu à `f35a70c` seulement, B.49) ; -LECTEUR-INDEP-1 (l.802 : les analyses et le rendu partagent `r1.parse_journal` ; touche la portée du mot « tiers » des `recompute_*`) ; -RT-ETIQUETTE-J14-1 (l.763) ; -PEARSON-IF-SOURCE-1 (l.799) ; -POOLEE-NIVEAU-1 (l.877) ; -EMD-PROFIL-1 (l.875) ; -FETCH-AVANT-PUB-1, -BIBLIO-PAGES-4-3-1, -DONG-CORPS-1, -S2-TUYAU-MONARK-1, -VITRINE-MONARK-1 (registre §7). |
| **prochain lot qui touche le fichier** | SHOGEN-PRIX-ARITH-RESIDU-1 (l.761, `r1.py`) ; -JSON-ENTIER-LONG-1 (l.762, `records.py`) ; -CI-S2-CABLAGE-1 (l.760, `gates.yml` ou forge) ; -CI-PLANCHER-SUIVI-1 (l.764, chaque lot qui ajoute des tests) ; -SG5-NOTES-INTERDITS-1 (l.828, `xtask`, priorité haute ; d'ici là, sortie de `verify` redirigée : consigne à mettre dans le brief du cp-2). |
| **analyses d'après le pré-enregistrement (hors décision)** | SHOGEN-ASN-PARTIELLE-S2-1 (l.759 ; déclencheur « lot d'après pré-enregistrement, ou limite déclarée au rapport » : POST-PREREG a eu lieu sans le traiter, et `docs/11` ne le cite pas (`grep` : 0) : une limite écrite suffirait) ; -DEP-FENETRES-2 (l.98, avant G10, P-05) ; -R1-PLUGIN-1 (l.99, test sourcé) ; -CENSURE-INFO-2 (l.102, P-08) ; -ZIF-NIVEAU-1 (l.796) ; -CENSURE-ZBLOC-1 (l.797) ; -GARDE-NIVEAU-ZSEUL-2 (l.876) ; -POSTPREREG-PARAMS-SCEAU-1 (l.800) ; -FICHE-WORKER-POSTEXEC-1 (l.801) ; -SIM-REGEN-1 (l.874). |
| **S2-bis (ADR-0029)** | SHOGEN-FLUX-ABSORPTION-COLLECTIVE-1 (l.872) ; -FLUX-SERIEL-1 (l.873) ; -ENTRELACEMENT-D5-1 (l.798) ; -SCEAU-OTS-1 (l.711, investisseur) ; -TASK-72H-1, -SCHED-MONITOR-1, -TORN-LINE-1, -UPS-1, -CENSURE-S2BIS-1 (registre §7). |
| **promotion de la collecte (D6 vi ; la collecte est arrêtée, JOURNAL l.322)** | SHOGEN-CLOSURE-CONTEXTE-1, -RAW-REDECODAGE-1, -COLLECTOR-FISHER-1 (registre §7). |
| **investisseur ou forge** | SHOGEN-CI-S2-FORGE-1 (l.78), -G3-FORGE-1, -G5-FORGE-1 ; -CI-RUNNERS-1 (l.80, partie Windows ; échéance « forge rétablie ou 2026-10-19 », non échue). |
| **poste local, sans échéance S2** | SHOGEN-COLLECT-PREVWS-1, -PERIMETRE-DISQUE-1, -POOLEE-SOURCE-1 (registre §9). |

### Ce qui reste à faire pour les deux items du lot CP2-G7

**SHOGEN-INSTRUMENT-S2-1** :
1. Le G7 de l'orchestrateur sur ce dossier. Il tranche les réserves du §2 (G4 surtout), forme ou dispose les réserves sans
   item, et nomme le gel jugé : `b6c1c95` (égal à la tête sur le chemin) ou `f35a70c` (arbre des rendus).
2. Le rejeu du G3 opérant complet (§4.11 et amendements) au commit du G7, consigné au JOURNAL avec les deux comptes de
   `--hors-refs` ; sortie de `xtask verify` redirigée, lignes de verdict seules.
3. Le cp-2 d'un validateur frais. Il produit **son propre** enregistrement de rôle `cp-2` par ses commandes (D6 viii l.207) :
   `tree.commit` égal au gel nommé, exit 0, `static_only` false, `served_from` conforme. L'enregistrement
   `execution/apres-execution/shogen-5afbdd2-cp-2-20261004T035926Z-20065.json` (sha256 `8567384f…ea82`) **n'est pas** ce
   cp-2 : il est de l'orchestrateur, sa sortie vaut 1 (un échec de test, depuis corrigé par DETTES-B1) et la variable y
   était posée (398 tests avec la variable). `--verifier` le refuserait au contrôle `exit` [lu]. Le cp-2 doit aussi dire
   quel enregistrement de G2 il contrôle, puisqu'aucun G2 au dépôt n'en cite un (réserve G2 (3)).
4. La fermeture de l'item (ligne datée à l'annexe B, JOURNAL), puis les actes dus à la clôture du §4 (a).

**SHOGEN-CP2-RUNS-RENDU-1** : le contrôle passe sur pièces (§5), mais un lecteur n'est pas le cp-2. Il reste que le
validateur du cp-2 le refasse par ses propres commandes, avec `--depot`, et le consigne :
`python3 -B s2-harness/tools/oracle_record.py --verifier docs/adr-0028/execution/rendu-2026-10-04/shogen-27b0e30-rendu-20261004T011129Z-943.json --role rendu --commit 27b0e303f196699959bddc2607db6a1d808ce0db --depot .`
(répertoire temporaire hors dépôt). Le vérificateur de la tête est celui de l'exécution : `oracle_record.py` est
identique entre `f35a70c` et la tête (`git diff --quiet` vrai) [lu].

## 5. CP2-RUNS-RENDU-1 : contrôle de l'enregistrement de rôle « rendu »

**Enregistrement** : `docs/adr-0028/execution/rendu-2026-10-04/shogen-27b0e30-rendu-20261004T011129Z-943.json`,
sha256 `355cf9bb43609c1c4b0f3ffebcd32d9d987e5e12e63277d9e4acbd467eb0fb5c`, égal au JOURNAL l.314 [lu].

**Liste exigée.** La suite d'abord, puis D.4 b (annexe D l.136) : « Elle produit, dans cet ordre : J14 principal (D4) ;
J14 second (coupe de 270) ; J28 (D2 pt 6) ; chaque sensibilité de la liste fermée (D2 pt 7) », puis l'oracle tiers sur
chaque sortie et l'enregistrement d'oracle. Le paquet scellé fixe le lieu des sensibilités : « plage incluse » = section
[SENSIBILITÉ] du J28 ; « seconde coupe J14 » = sortie J14 second (`PAQUET-PREREG-S2.md` l.84). Il fixe aussi l'ordre des
runs : suite, J14 principal, J14 second, J28, recalcul tiers, verdict du journal brut (l.106). Dans le code, c'est la liste
`["suite", *PRODUCTION]` exigée par `verifier` (`oracle_record.py` l.31, l.224-226).

| contrôle (comme `--verifier`) | attendu | constaté | résultat |
|---|---|---|---|
| champs, schéma | `shogen.oracle-record.v1`, champs complets | conformes | OK |
| rôle | `rendu` | `rendu` | OK |
| auteur | liste blanche du lint | `claude-opus-5-5` | OK |
| `tree.commit` | tête gardée de l'exécution | `27b0e303f196699959bddc2607db6a1d808ce0db` (JOURNAL l.314) | OK |
| `tree.sha256` (recalcul indépendant, `git archive` en mémoire) | égal par fichier | 436 fichiers sur 436, 0 écart | OK |
| `static_only` | false | false | OK |
| `exit` global et par run | 0 entier | 0 ; 0,0,0,0,0,0 | OK |
| sha256 de chaque sortie | égal au fichier | 6 sur 6 égaux, et égaux au JOURNAL l.314 | OK |
| `paquet.sha256` | sha du paquet scellé | `4d2a8276…f528` = sha du fichier à la tête et à `3be95be`, présent au JOURNAL (l.304) | OK |
| `sceau.genTime` | genTime du jeton | `2026-10-03T01:04:10Z` (JOURNAL l.306) | OK |
| **runs, dans l'ordre** | `suite`, `j14-principal`, `j14-second`, `j28`, `recalcul-tiers`, `raw` | identiques, dans cet ordre | **OK** |
| `served_from` | null ou conforme | null | OK |
| `tests_avec_variable` | vide (variable absente) | vide pour chaque run ; `env.SHOGEN_S2_CAMPAGNE_CONTROL` null | OK |
| compte de la suite (procédure l.77) | `Ran 398 tests`, `OK (skipped=2)` | `Ran 398 tests in 62.358s`, `OK (skipped=2)` ; deux sauts qui nomment la variable | OK |
| sensibilité « plage incluse » | section [SENSIBILITÉ] du J28 | présente (`[SENSIBILITÉ] PLAGE D'EXCLUSION INCLUSE`, l.435799 de la sortie J28) | OK |
| oracle tiers sur chaque sortie | `recompute_*` sur chaque rendu | clés `j14-principal`, `j14-second`, `j28`, `j28-incluse` (sous-clés `d5`, `lm`, `r1`, `r2`) | OK |
| code de l'exécution = code du paquet | `f35a70c` | `base` = `f35a70c…` ; `27b0e30` = `f35a70c` sur `shogen_s2` et `tools` ; sha256 de `rendu_unique.py` dans `tree.sha256` = `sha256_script` du paquet (`06d189cf…9050`, l.216) | OK |

**`--verifier` lancé** (code de la tête, identique à `f35a70c` pour `oracle_record.py`), sans `--depot` : sortie 0,
« conforme : … (rôle rendu, tree.commit 27b0e303… ; tree.sha256 non recalculé : --depot absent) ». Le recalcul de
`tree.sha256` a été fait à part, en mémoire, sans rien écrire (ligne du tableau).

**Résultat : CONFORME.** L'enregistrement porte les runs exigés, dans l'ordre, chacun avec une sortie 0. Ce contrôle est
celui d'un lecteur ; il prépare le cp-2 sans en tenir lieu.

**Note hors décision** : le run `raw` sort 0, mais son verdict est « refus » (cinq lectures de `raw.jsonl` absentes de
`journal.jsonl`). C'est voulu et écrit avant le sceau : « son verdict est imprimé sans fermer l'exécution »
(`docs/11-mesures-pilotes.md` l.830 ; paquet §12 pt 1). Ce verdict est rapporté dans `docs/11` (l.776-783).

## 6. Points que l'orchestrateur doit trancher (aucun n'est tranché ici)

1. **Gel jugé** par le G7 et le cp-2 : `b6c1c95` (= tête sur le chemin, code de qualité produit) ou `f35a70c` (arbre des
   rendus de décision). Les G2 au dépôt couvrent les deux (CORR jusqu'à `f35a70c`, DETTES-B1 au-delà).
2. **G4** : aucune baseline R-15 ni fonction de fitness nommée G4 pour le chemin. Choix possibles : relever les métriques,
   ou disposer par une décision écrite (avec item). Le doc 02 du corpus n'est pas au dépôt.
3. **Réserves G2** : tests de Phase A sans relecture au dépôt ; checklist du corpus non citée ; aucun enregistrement de
   rôle G2 cité, alors que le cp-2 doit en contrôler un (D6 viii l.207).
4. **G3 au commit du G7** : rejeu complet et consignation, `--hors-refs` compris.
5. **Dettes à déclencheur échu ou dues à la clôture** : ERRATA-ADR0028-1 ; D8-AMONT-ERRATUM-1, PAROXYSME-REGISTRE-1 et
   BUNDLE-CLOTURE-1 (les deux derniers seulement sur le poste local) ; condition E1-AVIS-FRAICHEUR-1 dans le brief du cp-2.
6. **Ordre G7 / cp-2** : D6 (ii) l.196 et ADR l.224 / annexe A l.9, l.11 ne disent pas la même chose.

## 7. Limites

- Rapports G2 de la partie 1 et de CI-S2 : hors dépôt (`F:\tmp\…`), non lus ; je ne cite que leur citation au dépôt [2nd].
- Doc 02 du corpus, `validateur-humain.md` (CA-12) : hors dépôt, non lus [abs].
- Signatures de commit : présentes, non vérifiables ici (`gpg.ssh.allowedSignersFile` absent) [abs].
- Je n'ai pas rejoué `xtask verify` (interdit par le brief), ni les gates des secrets, des hooks et de l'épinglage.
- La liste du §4 vient de l'état du registre de 03:46 UTC plus les blocs B.47 à B.53. Un item formé ailleurs qu'à
  l'annexe B depuis 03:46 UTC m'échapperait [inféré].
