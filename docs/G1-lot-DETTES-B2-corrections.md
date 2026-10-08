# Corrections de la relecture G2 du lot DETTES-B2 (C-1 à C-5) : note du worker

Worker `claude-opus-5-5` ; Gate 0 : identifiant exact `claude-opus-5-5` (effort `max` déclaré au lancement, non observable
depuis l'instance). Travail du 2026-10-04, de 07:33 à 08:05 UTC (`date -u`). Aucune opération git en écriture sur le dépôt ;
`SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée ; aucune pièce D.2 ouverte ; sortie brute de `xtask verify` jamais lue ni stockée
(filtrée à la source : en-têtes de section, lignes VERDICT, lignes VIOLATION de la seule section S-G9).

Rattachement : rapport G2 `G2-B2/G2-DETTES-B2.md` (sha256 `e0612252db5963e48f001cbc602074f66a7f6f8f9e9306ebcd7f394026a386a7`,
recalculé, égal ; lu en entier), liste fermée C-1 à C-5 ; décisions de l'orchestrateur Q-1 à Q-6 (message du 2026-10-04).

## 1. Base et application

- Tête du moment : `99d2aa47ec6f116da6ceff06188f637da5eb086c` (`git log -1` à 07:55 et à 08:01 UTC). Les diffs 01 à 09 sont
  régénérés sur l'état de la tête (chemins du lot lus par `git show`), les livrés de la v1 appliqués un à un, puis les
  corrections posées en remplacements exacts à ancre unique (`v2/corrections.py`) ; 10c reposé sur la tête (`v2/faire_10c.py`).
- Série vérifiée sur une extraction neuve de la tête (sans dossiers interdits, matière Pocket ni `apres-execution`) :
  01, 02, 03, 04, 06, 07, 10c, 08, 09, chacun par `git apply --check` puis `git apply` ; 05 reste applicable sur l'état
  final (non appliqué, décision Q-2). La tête a bougé pendant le travail (`cb44084`, `5c8b5b9`, puis `99d2aa4`) ; aucun
  chemin du lot n'a changé, sauf l'annexe A (ligne POST-PREREG), d'où 10c reposé sur `99d2aa4`.

| diff | sha256 | lignes | changement par rapport à la v1 |
|---|---|---|---|
| 01-D8d-1 | `0583e648a1d69de87fa1411fc53d431269195d1cf66580bc600a2b0ddc3b2e5b` | +65 −25 | aucun (octets identiques) |
| 02-D8d-2 | `7d49a419ac0cdca25220569814540538adb1de5929a63dc0f17736b4f349d4f4` | +96 −17 | C-3 : cas T-75f (+3) |
| 03-G5 | `6b4a0eb330f9b2b69dd756ed34571d33ab8515ff03072b79135e30b337d808b3` | +23 −9 | contexte seul (`gates.yml` de la tête, job `s2-harness-unittest` de DETTES-B1) |
| 04-RUNNERS | `57f4e69ceabf456a63655af60da036ccd288b8755c1e656f8c8787fb5ab6348d` | +13 −13 | aucun |
| 05-RUNNERS-WINDOWS-conditionnel | `8faf68f61303541c8460aa997c67845bae5d7d00e4c2488a7ba2c9f211445bda` | +4 −4 | aucun ; non appliqué (Q-2) |
| 06-XR-1 | `328aa459c5eff5ffa246d7e6ba2dcf58c46612d415d3b932826a5b12cd8a7dd7` | +197 −0 | aucun |
| 07-XR-2 | `4b934e84c8c693dd9b7b78ed2867a2ca2c62d9ce9b563ffeffd2c772dc4adeb1` | +192 −11 | C-1 (code, `sg6.rs`, trois tests), C-2 (un cas) |
| 08-XR-3 | `30daa901f3084b1e451e781a46a9d4562ff70c8733190b01f5530aa641d174f8` | +187 −1 | contexte seul (lignes ajoutées et retirées identiques) |
| 09-XR-4 | `bcddcca4f138189c0779acfd43dfcbca7d24e330c1d4d151c46d99342fecec19` | +195 −8 | C-4 (note, en-tête, test) |
| 10c-ACTES-PROPOSES-orchestrateur | `51e41b4492c00a6a08b7e413eea028967c2a331a69ec60ce09bcd1c7064712f1` | +10 −0 | C-5 : reposé sur `99d2aa4`, comptes mis à jour |

R-25 : tous ≤ 200 lignes ajoutées (07 : 192, 09 : 195). R-8 : aucun `Cargo.toml` ni `Cargo.lock` touché, `--locked` partout.
R-13 : étape g5 extraite de `gates.yml`, lancée sur un dépôt jetable de l'arbre final : « OK: aucun marqueur de dette nu. ».

## 2. Corrections, une par une (rouge avant, vert après, mutants)

Rouge avant : code livré (v1 sur la tête) plus les seuls tests neufs (`v2/tests-seuls`) ; vert après : plus le code (`v2/corrige`).

### C-1 : borne `biblio/` de S-G9 au prédicat de S-G6 (diff 07)

- Code : la borne ne se pose que si `biblio/` est sans octets, prédicat de S-G6 désormais partagé (`sg6::octet_verse` :
  tout fichier hors `INDEX.md` et `*.sidecar`, casse ASCII ignorée ; réécriture du filtre de S-G6 à l'identique) ; dossier
  absent = sans octets. `biblio/` peuplée : un fichier absent est « fichier introuvable », une plage hors du fichier est
  refusée. Note et en-tête : « biblio/ sans octets » (ou « biblio/ peuplée, contrôle plein »).
- Tests : `mutant_sg9_a_biblio_peuplee_reference_pendante` (ROUGE « fichier introuvable » exigé) ;
  `mutant_sg9_a_biblio_peuplee_plage_hors_du_fichier` (ROUGE « plage hors du fichier ») ; `temoin_sg9_biblio_sidecars_seuls_sans_octets`
  (INDEX et sidecar seuls, extension en majuscules : VERT et borne dite) ; libellé du témoin de l'arbre (« biblio/ sans octets »).
- Rouge avant, mesuré (77 tests, 4 échecs) : la référence pendante, le témoin de l'arbre (libellé), le témoin des sidecars
  (libellé) et le témoin des bornes (C-4). La plage hors fichier **passe** sur le code livré : le code livré contrôlait
  déjà un fichier `biblio/` présent ; ce test ne peut pas rougir avant, il tue MX-06 (écart E-1 à la lettre de la consigne).
- Vert après : 77 sur 77 (`cargo --locked test -p xtask --test mutants`), plus 9 tests de `reproductible`.
- Mutants tués : MX-06 de la revue réancré sur le code corrigé (MX-06′, toute référence `biblio/` sautée) par les deux
  tests `biblio_peuplee` ; MX-19′ réancré par les témoins ; les miens XA-11, XA-13 à XA-17 (prédicat forcé à vrai ou faux,
  dossier absent, négation, libellé) et XS-01 à XS-04 sur `sg6.rs` (sidecars comptés, `INDEX.md` compté, casse, filtre retiré).

### C-2 : `[aucun contrôle]` sans motif (diff 07)

- Cas `mutant_sg9_a_aucun_controle_sans_motif` (texte du rapport G2, mot pour mot) : passe sur le code livré (le code
  refusait déjà) ; tue MX-07 (mon XA-12, `motif.is_some()`).

### C-3 : ref vers un arbre dont une entrée porte un nom en forme d'identifiant (diff 02)

- Cas T-75f : arbre d'une entrée `<forme>.txt` au contenu propre, ref `refs/arbres/n` ; refus attendu
  `SECRETS/historique` sur `^refs/arbres/n:\(objet\)$`, forme jamais en clair (`QQQQ` interdit en sortie).
- Passe sur la gate livrée (147 ok) ; tue RS-08 de la revue (seul tueur, T-75f). Barres obliques écrites par `chr(92)` et
  contrôlées sur les octets écrits (`\n`, `\t`, `\n`, `\(`, `\)` : barres simples).

### C-4 : (g) et (h) de `verif_refs.py` déclarés non mécanisés (diff 09)

- Note de S-G9 : « … contenu de docs/16, (g) formes proscrites et (h) structure des tables S et T de verif_refs.py ; résidu … ».
- En-tête de `sg9.rs` : (g) deux formes proscrites et (h) structure des tables S et T (ligne T retirée, S sans menace ni
  motif, cellule de résidu vide, jeton de chemin servi absent, marqueur entre guillemets au lieu du jeton), d'après
  `docs/G1-lot-E1-modele-de-menace.md` l.113 [lu] ; (i) et (j), propres au lot E1, sans objet. Le G0 d'E1 (§10.3, hors
  dépôt, `F:/tmp/shogen-lots/E1/G0-lot-E1.md`) n'est pas lisible ici [abs].
- Test : le témoin des bornes exige la déclaration ; rouge avant (code livré), vert après ; mutant XN-01 (déclaration
  retirée) tué par ce témoin.

### C-5 : actes 10c (diff 10c)

- Parti de `G2-B2/actes/10c.diff` (sha256 `9f7e864a…`, lignes ajoutées identiques à celles de 10b), reposé sur `99d2aa4`.
- Comptes : runner 147 cas, D8d +161 −42 ; DETTES-B2-b 147 cas, +96 −17 ; DETTES-B2-f : C-1 et C-2, `sg6.rs`, 51 tests,
  +192 −11 ; DETTES-B2-g : 64 tests ; DETTES-B2-h : (g) et (h) déclarés, 77 tests, 54 mutants de S-G9 et 4 de S-G6 tués,
  revue G2 19 sur 20 (MX-12, observation O-3) ; DETTES-B2-d : 05 non appliqué (Q-2), l'item reste ouvert.
- DEVOPS : « (a) à (f) mécanisés ; (g), (h) non, déclarés en note » et « `biblio/` sans octets ».
- Contrat du runner déclaré dans la ligne D8d : T-79 resserré, T-75 relâché (B.15, Q-C-2), T-105b relâché (tag imbriqué
  propre, refusé à tort avant), actés (Q-3).

## 3. Campagnes de mutants (après corrections)

| campagne | outil | résultat |
|---|---|---|
| S-G9, ma table v2 (46 de la v1, XA-05 réancré, plus XA-11 à XA-17 et XN-01) | `mut/mutants_cargo.py`, `v2/table_sg9_v2.py` | 54 tués sur 54 (témoin vert) |
| S-G6, prédicat partagé (XS-01 à XS-04) | même outil, `v2/table_sg6_v2.py` | 4 tués sur 4 ; XS-04 : prédiction incomplète (tué par les tests de S-G6, pas par le témoin S-G9, qui appelle la fonction et non le filtre) |
| revue G2, secrets (RS-01 à RS-14) | `G2-B2/mut/muter.py`, table du réviseur | 14 tués sur 14 (RS-08 par T-75f) |
| revue G2, S-G9 (MX-01 à MX-20) | même outil ; MX-06 et MX-19 réancrés | 19 tués, MX-12 survivant (observation O-3, hors liste) |
| revue G2, étape g5 (MG-01 à MG-05) | même outil, `gates.yml` de la tête | 5 tués sur 5 |

## 4. États cumulés sur la tête `99d2aa4` (`v2/cumul_v2.sh`, cible cargo dédiée par état)

| après | runners | tests `xtask` | `verify` (substitut de 21 lignes vides au seul chemin exclu, original jamais lu) |
|---|---|---|---|
| 01 | secrets 129, hooks 51 | — | — |
| 02 | secrets 147, hooks 51 | — | — |
| 03 | hooks 54 | — | — |
| 04 | model-pinning 95 ; YAML : 11 feuilles `runs-on` | — | — |
| 06 | — | 35 + 9 | 9 gates VERT, VERDICT GLOBAL VERT |
| 07 | — | 51 + 9 | VERT |
| 08 sans 10c | — | — | ROUGE : S-G9 seul, `docs/17:112` (c) lot absent de l'annexe A (D8d) |
| 10c puis 08 | — | 64 + 9 | VERT |
| 09 | secrets 147, hooks 54, model-pinning 95 ; s2-harness `Ran 405`, OK (skipped=2), 0 `__pycache__` | 77 + 9 | VERT |

Arbre final dans un dépôt jetable : gate `--tree` (551 fichiers), `--history`, `--hors-refs` : sortie 0 ; étape g5 : OK ;
lint d'épinglage : 6 fichiers, OK. Lecture YAML tête contre arbre final : 12 feuilles changent (11 `runs-on`, étape g5).

## 5. Actes rédigés, non appliqués (Q-4, Q-6)

- `actes/AMENDEMENT-4-11.md` : puce datée pour ADR-0028 §4.11 après la ligne 299 (forme A, recommandée) ; forme B
  (retrait en place dans la ligne 297) fournie.
- `actes/PUCE-DOCS17.md` : puce datée de docs/17 (T-09, T-10, T-14, T-04). Contrôle mesuré sur l'arbre final + puce,
  lignes de verdict seules : sans l'item SHOGEN-SECRETS-COMMIT-MSG-1 à l'annexe B, S-G9 ROUGE, seul motif
  « (c) item non défini » (`docs/17:113`) ; avec la variante sans identifiant : VERDICT GLOBAL VERT ; avec l'item simulé
  à l'annexe B (copie jetable, restaurée) : VERDICT GLOBAL VERT.

## 6. Décisions appliquées et items à former

- Q-1 : 10c, avant 08 ou dans le même commit (08 + 10c : 197 lignes) ; mesuré : 08 sans 10c rouge, avec 10c vert.
- Q-2 : 05 livré tel quel, non appliqué ; CI-RUNNERS-1 ouvert (ligne DETTES-B2-d de 10c).
- Q-3 : T-75, T-79 et T-105b déclarés dans la ligne D8d de 10c.
- Q-4, Q-6 : textes au §5. Q-5 : item (I-3).
- Items à former (texte du rapport G2 §11, que je ne reformule pas) : I-1 SHOGEN-SG5-NOTES-INTERDITS-1 (priorité haute),
  I-2 SHOGEN-SG9-PERIMETRE-1, I-3 SHOGEN-SG9-CORPUS-1, I-4 SHOGEN-SECRETS-COMMIT-MSG-1, I-6 SHOGEN-XTASK-TMP-NOMS-FIXES-1,
  N-1 SHOGEN-SECRETS-NOMS-REFS-1, N-2 SHOGEN-SG9-COPIE-INTERDITS-1, N-3 SHOGEN-SG9-STRUCTURE-1. La puce de docs/17 cite I-4 :
  la former avant d'appliquer la puce, ou prendre la variante.

## 7. Écarts

- E-1 : la consigne demandait que chaque test de C-1 soit rouge sur le code livré ; le test de plage hors fichier ne peut
  pas l'être (le code livré contrôle déjà un fichier présent) ; il tue MX-06′, comme le rapport G2 l'annonce (« tue MX-06 »).
  Le test de référence pendante, lui, rougit avant.
- E-2 : C-1 touche `xtask/src/sg6.rs` (prédicat partagé, filtre réécrit à l'identique) : un fichier de plus dans 07 ; tests de
  S-G6 verts, quatre mutants tués.
- E-3 : un témoin de plus que la liste (`temoin_sg9_biblio_sidecars_seuls_sans_octets`) : sans lui, XS-01 et XS-03
  (sidecars comptés comme octets, casse) survivaient, aucun test de S-G6 ne portant de sidecar.
- E-4 : MX-06 et MX-19 de la revue ancrés sur la ligne que C-1 réécrit : réancrés (MX-06′, MX-19′), même mutation.
- E-5 : la tête a bougé trois fois pendant la correction ; 10c est reposé sur `99d2aa4` et devra l'être de nouveau si
  l'annexe A bouge avant le commit (`v2/faire_10c.py <sha>`).
- E-6 : appels `python3` du worker : préfixe `env -u SHOGEN_S2_CAMPAGNE_CONTROL PYTHONDONTWRITEBYTECODE=1` posé partout dans
  cette passe ; 0 `__pycache__`.
- E-7 : copies et cibles anciennes de la v1 supprimées du scratchpad (3,6 Go) ; sorties et diffs de la v1 gardés
  (`DETTES-B2/o/`, `DETTES-B2/livrables-v1/`).

## 8. Provenance (sha256, 16 premiers caractères)

Lu [lu] : rapport G2 en entier ; `G2-B2/actes/10c.diff`, `G2-B2/sondes/c3.sh`, `G2-B2/mut/{muter.py, table-*.tsv, test-sg9.sh}` ;
à la tête : `xtask/src/sg6.rs` l.1-100, `docs/G1-lot-E1-modele-de-menace.md` l.80-118, ADR-0028 §4.11 l.287-301,
`docs/17-modele-de-menace.md` l.106-112, `docs/adr-0028/ANNEXE-B-items.md` l.147, annexe A (fin de table), DEVOPS (ligne S-G7).
Non lu : dossiers interdits, matière Pocket, `apres-execution`, pièces D.2, tout `*.jsonl`.

Scripts (`DETTES-B2/v2/`) : `corrections.py` 38c6fde1… ; `faire_diffs_v2.py` 8570a54b… ; `faire_10c.py` e1647d11… ;
`cumul_v2.sh` cf1e8820… ; `table_sg9_v2.py` 5ed33638… ; `table_sg6_v2.py` 013b8461… ; `g2-table-sg9-reancree.tsv`
a145f755… ; `g2-table-mx19.tsv` 2f31f985… ; `g2-test-sg9.sh` 409059ba….

Sorties (`DETTES-B2/v2/o/`) : rouge avant `tests-seuls-mutants.out` eafb3252…, `rouge-secrets-c3.out` fabc9131… ; vert après
`corrige-mutants.out` a1ffeaf8…, `vert-xtask-tests.out` a4023f3f…, `vert-secrets.out` fabc9131…, `vert-hooks.out`
dcefd2a5… ; mutants `mut-sg9-v2.out` 2e06aa38…, `mut-sg6-v2.out` 6c9155ff…, `g2-mut-secrets-v2.out` 7ec68dfa…,
`g2-mut-sg9-v2.out` 75f81fc9…, `g2-mut-mx19-v2.out` 8a5a80e1…, `g2-mut-g5-v2.out` d5404147… ; états cumulés
`cumul-v2.out` 2aeb8e23… (détail dans `o/cumul/`) ; puce `puce-A-sans-item.out` da7d80a3…, `puce-B-variante.out` et
`puce-A-avec-item.out` f16a33c8….
