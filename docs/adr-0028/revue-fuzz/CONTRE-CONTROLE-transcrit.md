# Contre-contrôle du lot FUZZ (passes 1 et 2 ; clôture CONFORME) (transcrit)

> Transcription par l'orchestrateur le 2026-10-10 03:36:30 UTC du fichier g2/cc/RAPPORT-CC.md ; contrôle FM-1.1 des transcripts du générateur-correcteur, de l'advisor, du réviseur G2 et du contre-contrôleur, par le fm11.py versé et par celui de DT3-E : fragments_l51_l14 = 0 ; modèles résolus : claude-opus-5-5 (générateur, G2, contre-contrôle), claude-fable-5-1 (advisor). Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Contre-contrôle neuf du lot FUZZ (corrections de la G2 : FZ-g, FZ-h, G-4 ; règle Q-8)

- **Modèle** : `claude-opus-5-5`. **Gate 0** : modèle résolu `claude-opus-5-5` (identifiant exact donné par l'invite système
  du run) ; effort demandé par le brief : high. Contre-contrôleur neuf : je n'ai écrit ni relu aucune pièce de ce lot.
- Horloge (`date -u`) : ouverture 2026-10-10 00:58:34 UTC ; rédaction de ce rapport 2026-10-10 01:35:49 UTC.
- Brief : `BRIEF-CC.md`, sha256 `23e1ec150c883e95c0bfdbc2857d04927cc9ef32abc8b660cdf6272d2a8e0c89` (préfixe attendu conforme).
- Base : `git archive 094fa5d` (base du brief), copie creuse (sans `docs/15-*`, `docs/16-*`, `docs/pocket-report/`,
  `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, `docs/adr-0028/execution/`, `*.jsonl` ; les pièces de
  D.2 présentes au dépôt sont dans ces exclusions). Tête du dépôt relevée : `7026d01` (00:59) puis `4211d71` (DT5-10, 01:26) ;
  index de l'orchestrateur modifié (non lu). Aucune écriture git au dépôt, aucun commit, aucun push.
- Série a, b, c, d, f, e, x, g, h : empreinte de la concaténation recalculée
  `0fe1972a99b7b9ea33cd0cb9d10868cd5401b90d5c2793b647ff82b78c79621c` (= brief) ; a..x `24def280…` (= G2). Pièces versées avec
  FZ-f : `sha256sum -c` 4 OK ; archive `cbc2ab11…ba59dd` = épingle de FZ-h.
- `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée (`env -i` dans chaque lancement isolé, `unshare -n`). Enregistrement du rôle G2
  (`oracle_record.py`) : sans objet (lot postérieur à la clôture de S2, hors du dossier du cp-2 ; le brief ne le demande pas).

## 1. Verdict : **CONFORME-AVEC-RÉSERVES (R-1 à R-3)** ; R-1 bloque le versement

G-1 à G-4 sont faites, justes et testées (rouge puis vert rejoués) ; la réponse à la question de G-2 est non (§2). Mais la série
porte un **défaut neuf**, introduit par FZ-x et caché aux deux rejeux précédents par leur configuration : il rendrait rouge le
job `squelette` (ubuntu-24.04 et Windows) de la PR qui porte le lot. Corrigé par R-1 (5 lignes, diff fourni et éprouvé).

| R-n | constat | preuve | forme exacte |
|---|---|---|---|
| **R-1** (bloquante) | FZ-x pose l'arbre jouet de `xtask/tests/reproductible.rs` sous `CARGO_TARGET_TMPDIR` (`racine_du_cas` → `Arbre::nouveau`). Avec la cible cargo par défaut, celle de la forge (`squelette.yml` l.107 à `094fa5d`, l.116 à `4211d71` : `cargo test --locked --workspace -- --nocapture`, sans `CARGO_TARGET_DIR`), ce dossier est **dans** le workspace du dépôt : `cargo generate-lockfile` sur le jouet sort en « current package believes it's in a workspace when it's not », 4 tests rouges sur Linux (`mutant_base_…`, `mutant_construction_…`, `mutant_double_build_…`, `temoin_double_build_…`), 3 sur Windows où le témoin est exclu [inféré : même chemin sous la cible, non mesuré]. Le générateur et la G2 ont lancé leurs tests avec un `CARGO_TARGET_DIR` hors de la copie (`g2/outils/isole_g2.sh` ; NOTES du générateur l.32) : le défaut n'y paraît pas | `094fa5d` creuse, cible par défaut : reproductible 9/9 ; série, cible par défaut : `test -p xtask` reproductible 5 ok / 4 FAILED, rc 101 ; commande de la forge `--workspace` : rc 101, mêmes 4 ; série, cible hors copie : 9/9 (`journaux/test-final*.txt`, `squelette-tests-final.txt`) | `R-1.diff` (sha256 `54c7e8b7…cd51b4`, +5/−1, s'applique sur l'arbre final et sur `4211d71` + série) : table `[workspace]` vide dans le manifeste du jouet, et un commentaire qui en dit la raison. Éprouvée : cible par défaut, `test -p xtask` 3/7/81/9, commande `--workspace` de la forge rc 0, verify inchangé (S-G9 seul, artefact), fmt et clippy VERT ; le garde lexical d'`arbres.rs` a refusé mon premier jet (le commentaire nommait la variable de la cible) : commentaire réécrit. **Diff écrit par le contre-contrôleur : à relire par un autre que moi avant versement** |
| **R-2** | Le README du corpus ne dit pas la règle Q-8 : « jamais un seuil abaissé » et « la nouvelle épingle se pose par un lot qui redistille, jamais en même temps qu'un seuil plus bas » se lisent sur le nombre absolu, donc comme un plancher à 642, ce que Q-8 exclut (« le nombre absolu suit E », « aucun plancher absolu à 642 ») ; « lot revu (G2) », « l'ancien et le nouvel E », « le binaire mesuré », « la raison du changement » n'y sont pas | README l.52-60 de l'arbre final (§5) ; scénario N10 : une épingle nouvelle sur un dérivé plus petit donne E 623, seuil 372, VERT : seul un lot revu l'empêche, la règle doit donc être écrite | `R-2.diff` (sha256 `07a4fe25…263dbc`, +9/−7) : « **Règle** : ce qui ne baisse jamais est la fraction, 471/789 de E ; le nombre absolu suit E, sans plancher (642 n'en est pas un). […] jamais une fraction abaissée […]. Un dérivé remplacé, même avec le `SHA256SUMS` du dossier à jour, fait échouer le pas et ne peut plus abaisser le seuil. Une épingle nouvelle ne se pose que par un lot revu (G2), daté, qui écrit l'ancien et le nouvel E, le binaire mesuré et la raison du changement. » |
| **R-3** | Même ambiguïté dans la ligne de fermeture de FZ-e (`docs/13` l.195) : « seuil ⌈E × 471/789⌉ (642 au binaire de `c1122de`) ; redistiller, jamais abaisser le seuil » | lu à l'arbre final | `R-3.diff` (sha256 `ebfc4179…508ec4`, +1/−1) : « …(642 au binaire de `c1122de`), nombre qui suit E ; redistiller, jamais abaisser la fraction 471/789 ; épingle du dérivé changée par un lot revu (G2) seulement, qui écrit l'ancien et le nouvel E. » Composable avec G-5 (dates de fermeture posées au versement) : la ligne est retouchée de toute façon |

Item à former (règle PAROXYSME, limite rencontrée, non une réserve de la série) : **I-1**, nom proposé
SHOGEN-HARNAIS-CIBLE-HORS-COPIE-1 : la consigne « cible cargo dédiée par copie » (SHOGEN-HARNAIS-CIBLE-PARTAGEE-1), appliquée
avec un `CARGO_TARGET_DIR` hors de la copie, place `CARGO_TARGET_TMPDIR` hors du workspace et masque tout défaut qui en dépend
(R-1 en est un). Forme proposée : tout rejeu de `cargo test` d'un lot comprend au moins une exécution cible par défaut (dans
la copie, configuration de la forge), ou une cible dédiée posée **dans** la copie.

## 2. Point 1 du brief : G-1 à G-4

- **G-1** (FZ-g, `distillation.rs` +12, à l'octet de `g2/C-G2.diff`) : fait, juste, testé. M5 de la G2 (E = |dérivé| − |base|)
  rejoué : tests d'avant FZ-g (FZ-g inversé) 6/6, **vivant** ; tests de FZ-g : **tué** par le seul test neuf, `left: (95, 57)`,
  `right: (100, 60)` ; sans mutant 7/7. Valeurs recomptées : E = 10..109 = 100, ⌈47 100/789⌉ = 60 ; 59 gagnées, ROUGE ; sous M5
  105 − 10 = 95, ⌈44 745/789⌉ = 57.
- **G-2** (FZ-h, `fuzz.yml` à l'octet de C-G2, README complété de 3 lignes) : fait. Épingle exacte, avant l'extraction, fatale ;
  `SHA256SUMS` gardé. Les 7 scénarios du générateur rejoués à l'identique (§3) ; 5 neufs. **Réponse** : un dérivé remplacé
  (altéré, substitué, absent, faible avec `SHA256SUMS` à jour) fait échouer le pas à l'épingle, avant toute carte : il ne peut
  ni abaisser le seuil ni passer au vert ; un `SHA256SUMS` faux sur la ligne de l'archive (périmée, absente, retirée, doublée,
  au marqueur `*`) fait échouer le pas ; faux sur une carte : le pas ne lit pas les cartes (VERT, sans effet sur le seuil) et
  `docs-sha256sums.py` (job `g1-model-pinning`) le refuse, rc 1. Seul un changement de l'épingle elle-même (changement de la
  gate) déplace E : N10, épingle de l'archive faible, E 623, seuil 372, VERT ; voulu par Q-8, d'où R-2.
- **G-3** (FZ-g, `arbres.rs` +4/−1, à l'octet de C-G2) : fait, juste, testé. Fichier planté au nom fixe sous la cible :
  `arbres.rs` d'avant FZ-g FAILED (NotADirectory), celui de FZ-g 3/3. Concurrence sur une **même** cible (deux boucles
  parallèles de 10 passes des quatre binaires de test) : 0 échec sur 2 × 40, 0 dossier laissé.
- **G-4** (§11 du rapport du générateur) : fait, juste. `gate-secrets.sh --tree` lit l'index (l.165 `git ls-files`, l.18 étage
  0) : relu. Comptes recomptés : arbre de `094fa5d` 1131 fichiers, copie creuse 1073 (écart 58), série + pièces 117 ajouts,
  9 fichiers de garde exclus par contrat : 1131 + 117 − 9 = 1239 (générateur, clone complet), 1073 + 117 − 9 = 1181 (G2 et mon
  rejeu, index complet) ; l'explication « [inféré] » du §11 est confirmée.
- **Défaut neuf** : R-1 (FZ-x). G-1 à G-4 n'en introduisent aucun (mutants §4 ; jobs §3).

## 3. Point 2 du brief : rejeux (isolés, `unshare -n`, `env -i`, journaux sous `journaux/`)

| rejeu | résultat |
|---|---|
| `cargo --locked xtask verify`, arbre final creux (cible par défaut) | S-G1..S-G8 VERT ; S-G9 ROUGE 1 (docs/17 l.70, référence vers `docs/rapports/`, absent de la copie creuse) ; fmt, no_std, clippy VERT. Même violation, seule, sur `094fa5d` creuse : artefact attendu. Idem avec R-1 seul et avec R-1..R-3 |
| `cargo --locked test -p xtask` | cible hors copie : arbres 3, distillation 7, mutants 81, reproductible 9 ; cible par défaut : reproductible 5/4 FAILED (R-1) ; avec R-1, puis avec R-1..R-3 : 3/7/81/9, 0 dossier laissé |
| `cargo xtask fuzz-distillation` sur les cartes versées | 1339, 2084, E 1074, 745 gagnées dont 719 dans E, seuil 642, perdues 0, VERT rc 0 ; deux cartes rc 64 ; base comme corpus ROUGE rc 1. Recompte python : identique, marge 77, 719/1074 = 66,95 % ≥ 59,70 % |
| pas « Construction » et « Distillation » extraits de `fuzz.yml` (PyYAML 6.0.1 ; sha256 du pas `079f035c…`, avant FZ-h `8552209a…`), lancés `bash --noprofile --norc -eo pipefail`, cargo-afl 0.18.2 « AFL++ version 4.40c » (outils du lot copiés) | aucune : 0, VERT (1339/2084/2410 ; E 1074 ; 745/719 ; 642). Cartes ≠ versées à l'octet, comptes identiques (binaire recompilé) ; base : 16 graines, 15 lues (`dirigee-cbor-vide.bin`, 0 octet) |
| 7 scénarios du générateur, avant → après FZ-h | sans constats 1 → 1 (601 < 642) ; archive altérée 1 → 1 ; substituée (20) 1 → 1 ; **faible + sommes à jour + sans constats 0 (E 623, seuil 372) → 1 (épingle)** ; absente 1 → 1 ; sommes périmées 1 → 1 (somme) : identiques au §12.4 |
| 5 scénarios neufs (avant → après), plus N10 | sans la ligne de l'archive 1 → 1 ; sans `SHA256SUMS` 1 → 1 ; ligne doublée (une fausse) 1 → 1 ; ligne au marqueur `*` 1 → 1 ; somme fausse d'une carte 0 → 0 au pas, refusée par `docs-sha256sums.py` (rc 1). N10, changement de la gate (épingle de l'archive faible, sommes à jour, sans constats) : 0, E 623, seuil 372 ; même épingle, scénario « aucune » : 1 |
| témoin de deux `cargo test -p xtask` simultanés (deux copies, même TMPDIR neuf) | série + R-1, cibles par défaut : 3 essais sur 3, deux sorties 0, 0 dossier laissé ; série, cibles hors copies : 2 sur 2 verts, 0 laissé ; série, cibles par défaut : deux sorties 101 (R-1, aucune collision), 0 laissé |
| jobs de `gates.yml` (pas `run` extraits par PyYAML, coquilles de la forge, dépôt jetable `git add -A` sans commit) | à `094fa5d`, série : 15 scripts rc 0 (hooks 54, TODO aucun, lint 227, R-1 OK, journaux-modele, docs-sha256sums 35/299, secrets 147, arbre 1181, vérificateur 137, s2-harness 415, s2bis 341, sim-bis 279, calib-actifs 65, controle 26) ; `--history` sans objet (série non commise). Même résultat avec R-1..R-3. À la tête `4211d71` + série + R-1..R-3, `gates.yml` de la tête : tous rc 0 (hooks 57, runners-epingles conforme, workflows-yaml 11 cas + conforme, arbre 1185, s2-harness 418, controle 33) |
| `enforcement/docs-sha256sums.py` | conforme, 35 `SHA256SUMS`, 299 lignes (dossier des pièces compris) |
| lecture YAML | les 7 workflows lisibles ; `fuzz.yml` 4 jobs, 11 pas au job `cargo-afl` ; `gates.yml` 8 jobs |

## 4. Point 3 du brief : mutants propres

Classement : construction de xtask en échec = non viable ; `cargo test -p xtask` 101 avec un test FAILED = tué ; 0 = vivant ;
autre = FATAL (aucun). Pas CI : tué si un scénario rend une issue autre que celle du pas de FZ-h. Témoin sans mutation vivant.

| id | zone | mutation | issue (tueur) |
|---|---|---|---|
| S1 | seuil | division entière au lieu de `div_ceil` | TUÉ (`seuil_471_sur_789_…`, `apport_compte_…`) |
| S2 | seuil | verdict sur `seuil(E + 1)` | TUÉ (`gate_compte_…`, `commande_rend_…`) |
| S3 | seuil | `>` au lieu de `>=` | TUÉ (mêmes) |
| E1 | E | E = carte du dérivé entière | TUÉ (3 tests) |
| E2 | E | gagnées filtrées par le dérivé au lieu de E | VIVANT, **équivalent prouvé** : gagnées ⊆ corpus ∖ base, donc a ∈ E ⇔ a ∈ dérivé |
| E3 | E | E restreint aux arêtes du corpus entier | TUÉ (3 tests) |
| E5 | E | `juger` permute corpus et dérivé | TUÉ (`commande_rend_…`) |
| E6 | E | garde `apport > 0` retirée | TUÉ (`gate_compte_…`, cas « apport nul ») |
| A1 | Arbre | `Drop` par `remove_dir` (non récursif) | TUÉ (`arbre_unique_…`) |
| A2 | Arbre | aucun effacement pendant une panique | TUÉ (`arbre_unique_…`) |
| A3 | Arbre | arbre sous `temp_dir()` | TUÉ (`arbre_unique_…`) |
| A4 | Arbre | `cas` omis du nom | VIVANT, **équivalent** : unicité par rang atomique et processus, `cas` lisible seulement |
| EP1 | épingle | épingle dans le sous-shell (chemin doublé) | TUÉ (aucune : 1) |
| EP2 | épingle | une espace au lieu de deux | VIVANT, **équivalent mesuré** : coreutils 9.4 accepte une ou deux espaces et `*` |
| EP3 | épingle | `set -uo pipefail` (sans `-e`) | VIVANT, **équivalent** : la forge lance `bash -eo pipefail` |
| EP3b | épingle | `set +e` | TUÉ (8 scénarios ; substituée-20 : E 292, seuil 175, VERT) |

16 mutants, 12 non équivalents, 12 tués. Rejeux hors matrice : M5 (G-1) et le nom fixe (G-3), §2.

## 5. Point 4 du brief : le README dit-il la règle Q-8 ?

Non, pas entièrement (texte de l'arbre final, l.52-60). Il dit le seuil comme formule (⌈E × 471/789⌉, « 642 pour E = 1074 »),
l'épingle et « jamais la réponse à un rouge ». Il ne dit pas que la fraction est ce qui ne baisse jamais ni que le nombre suit E,
et deux phrases se lisent comme un plancher à 642 : « jamais un seuil abaissé », « jamais en même temps qu'un seuil plus bas » ;
il ne dit pas « lot revu (G2) » ni « l'ancien et le nouvel E, le binaire mesuré et la raison du changement ». Le commentaire
du pas de FZ-h (« un changement de cette gate, jamais une mise à jour de pièce ») et la ligne de DEVOPS (FZ-f) sont conformes à
Q-8. Corrections : R-2 (README), R-3 (docs/13).

## 6. Observations (sans réserve)

- O-1 : E se déplace aussi si la base grossit (graines non distillées ajoutées) sans toucher l'épingle. La fraction de la
  doctrine tient : avec a arêtes de E₀ couvertes par les distillées hors de l'ajout X, x arêtes de E₀ couvertes par X, e = |E₀|,
  la gate exige a/(e − x) ≥ f, d'où (a + x)/e ≥ f + x(1 − f)/e ≥ f : un VERT de la gate implique la mesure de 13 §7 sur le
  corpus entier. Une graine `panique-*` qui ne serait pas une panique observée relève de la revue du corpus.
- O-2 : la troisième carte versée est base ∪ dérivé (2413), le pas calcule le dérivé seul (2410) : même E (1074). Sur les
  cartes versées, M5 est indétectable (|base ∪ dérivé| − |base| = |E|) ; le test de G-1 le tue sans dépendre des cartes.
- O-3 : G-5 n'est pas dans la série (FZ-e porte encore « FERMÉE le 2026-10-09 » et « fermée (2026-10-09) ») : conforme à
  l'adjudication de 00:28:49 (date posée au versement) ; Q-9 : DEVOPS l.91 garde sa date d'écriture.
- O-4 : R-25 : FZ-g +16/−1, FZ-h +11/−1 ; R-1 +5/−1, R-2 +9/−7, R-3 +1/−1 ; aucune dépendance neuve (R-8), aucun marqueur nu
  (job g5 rejoué sur la série corrigée).
- O-5 (consigne de versement) : `git apply` signale « space before tab in indent » à FZ-b l.853, contenu voulu de la graine
  `dirigee-distillee-registre-blanc.txt` (16 espaces, tabulation, saut de page) ; `--whitespace=error` refuse FZ-b (rc 128),
  le défaut `warn` l'applique (rc 0) ; le dépôt ne pose ni `apply.whitespace` ni `core.whitespace`. Appliquer la série sans
  `--whitespace=fix` ni `error` : `fix` changerait la graine et `le_corpus_committe_…` rougirait.
- O-6 : la tête a encore avancé pendant ce contre-contrôle (`2d233c8`, DT5-11 et DT5-12, relevé à 01:39) ; fichiers changés
  depuis `094fa5d` (commits, index, arbre) : 16, aucun dans la série ni dans `reproductible.rs` (cible de R-1).

## 7. Écarts du contre-contrôleur

- E-1 : contrôle de restauration de ma copie de mutants par `find xtask -name '*.rs' | xargs sha256sum` (deux copies du
  scratchpad) : liste par motif, contraire à la lettre du brief ; sortie limitée à « identiques ». Plus de `find` ensuite.
- E-2 : `git ls-tree -r --name-only 094fa5d | wc -l` (liste récursive du dépôt, compte seul, aucun nom affiché) pour G-4 ;
  et un `git ls-tree --name-only 094fa5d docs/adr-0028/` (non récursif) pour nommer l'annexe D : noms seuls, aucun contenu
  interdit ouvert.
- E-3 : premier passage des mutants écarté (mon classement prenait « could not compile `jouet` », source fautive voulue de
  reproductible.rs, pour un échec de construction) ; classement corrigé, tout relancé.
- E-4 : R-1 à R-3 sont écrits par moi : ils ne peuvent compter comme relus par moi (réviseur ≠ générateur) ; à faire relire.
- La sortie de S-G9 nomme le chemin d'un fichier de `docs/rapports/` (nom seul, dans le message de la gate).
- E-5 : pour O-5 et O-6, deux listes et un arbre d'essai (`xtask/src` de `094fa5d`) posés à la racine du scratchpad, hors de
  mon dossier, supprimés aussitôt.

## 8. Journal de provenance (G1)

[lu] : BRIEF-CC (entier) ; ADJUDICATION (entière) ; g2/RAPPORT-G2 et g2/NOTES (entiers) ; RAPPORT-GENERATEUR §11-§12
(l.340-533) ; BRIEF-FUZZ ; les neuf diffs (code en entier, graines par numstat) ; g2/C-G2.diff (comparé section par section) ;
annexe D l.1-60 à `094fa5d` (liste D.2, pour l'appliquer) ; à l'arbre final : fuzz.yml (déclencheurs, job cargo-afl), README du
corpus (l.1-80), xtask/src/distillation.rs (gate), xtask/tests/reproductible.rs (l.1-60, l.170-240, l.318-400),
xtask/src/reproductible.rs (l.470-535), squelette.yml (l.20-60, l.95-115), temoignage.yml (l.20-85), Cargo.toml (l.1-40),
.cargo/config.toml, docs-sha256sums.py (entier), gate-secrets.sh (l.18, l.160-170), gates.yml (pas `run`) ; à `4211d71` :
gates.yml (pas `run`), squelette.yml (diff depuis 094fa5d). [2nd] : aucun chiffre retenu sans rejeu. [abs] : aucune.

Commandes (scripts dans `outils/`, sorties dans `journaux/`) : `copie.sh` (git archive creux), `serie.sh` (git apply a..h et
pièces), `isole.sh`, `isole_ci.sh` + `lance_lo.sh` + `lo_up.py` (unshare -n, env -i, lo allumée), `cargo --locked xtask
verify`, `cargo --locked test -p xtask`, `cargo test --locked --workspace -- --nocapture`, `mutants_cc.py`, `pas_ci.py`,
`scenarios_cc.py`, `sommes_docs.py`, `gate_cartes_versees.sh`, `recompte.py`, `temoin.sh`, `concurrence.sh`,
`jobs_gates.py`. Chiffres recomptés : 1339, 2084, 2410, 2413, 1074, 745, 719, 26, 0, 642, 77, 1071, 3 (python sur cartes
versées et sur mes cartes) ; 108 et 26 graines (tables de distillation.rs) ; 623, 372, 292, 175, 601 (scénarios) ; 1131, 1073,
58, 117, 9, 1239, 1181, 1185 (G-4) ; numstat (O-4).

## 9. Fichiers rendus (sous `<scratchpad>/s2bis/fuzz/g2/cc/`)

`RAPPORT-CC.md` (ce fichier), `NOTES.md`, `BRIEF-CC.md`, `R-1.diff`, `R-2.diff`, `R-3.diff`, `outils/`, `journaux/`,
`SHA256SUMS` (écrit en dernier). Copies, cibles cargo et RUNNER_TEMP supprimés à la fin (reconstructibles : `git archive
094fa5d`, la série, les diffs R-n).

## 10. Passe 2 — ajout daté du 2026-10-10 02:10:00 UTC (`date -u`) : série a..k (FZ-i, FZ-j, FZ-k = R-1, R-2, R-3)

Pièces suivies : `ADJUDICATION.md` (ajout daté de 01:41:06 : R-1 à R-3 adoptées, I-1 versée comme règle au lot DETTES-T7,
O-5 tenue par `git apply --index --whitespace=nowarn` ; sha256 `11f3d7ce…`), `RAPPORT-GENERATEUR.md` §13 (l.535-678, sha256
`9642b27d…`), lus en entier. Gate 0 inchangé : `claude-opus-5-5`. Ouverture de la passe : 01:57:19 UTC.

- Entrées : `cmp` FZ-i = R-1, FZ-j = R-2, FZ-k = R-3, octet pour octet. Empreinte de la série a..k recalculée :
  `3003589dac9a42ff5af46cf1f13ebc2afe30f4fa8076536f65611b4afe73b6cf` (= message de l'orchestrateur) ; a..h inchangée
  (`0fe1972a…`). Base : `git archive 094fa5d`, copies creuses ; pièces 4 OK. Tête relevée `e8825318` puis `5f99b4c`
  (DT5-17, 02:01) : 16 fichiers changés depuis `094fa5d` (commits, index, arbre), aucun des 122 de la série.
- Toutes les courses : isolées (`unshare -n`, `env -i`, `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée), à la **cible cargo par
  défaut de chaque copie** (règle I-1) ; `df -h /` avant compilation : 8,2 G à 6,4 G libres.

### 10.1 Verdict de la passe 2 : **CONFORME** — R-1, R-2, R-3 levées ; aucun défaut neuf

| R-n | levée | preuve (journaux sous `journaux/passe2/`) |
|---|---|---|
| R-1 | **oui** | Avant FZ-i (a..h) : `cargo --locked test -p xtask` rc 101, reproductible 5 ok / 4 FAILED, 4 refus de workspace ; `cargo test --locked --workspace -- --nocapture` rc 101, mêmes 4. Après (a..k) : `test -p xtask` rc 0, arbres 3, distillation 7, mutants 81, reproductible 9, 0 dossier laissé ; `--workspace` rc 0, 28 bilans ok, 0 FAILED. Témoin de deux `test -p xtask` simultanés, deux copies de l'arbre final, cibles par défaut, même TMPDIR neuf : 3 essais sur 3, deux sorties 0, 0 dossier laissé |
| R-2 | **oui** | README du corpus l.52-62 de l'arbre final : la fraction 471/789 de E ne baisse jamais ; le nombre absolu suit E, sans plancher, « 642 n'en est pas un » ; épingle nouvelle par un lot revu (G2), daté, qui écrit l'ancien et le nouvel E, le binaire mesuré et la raison du changement ; « jamais un seuil abaissé », « jamais en même temps qu'un seuil plus bas » : 0 occurrence |
| R-3 | **oui** | `docs/13` l.195 : « nombre qui suit E ; redistiller, jamais abaisser la fraction 471/789 ; épingle du dérivé changée par un lot revu (G2) seulement, qui écrit l'ancien et le nouvel E » ; « jamais abaisser le seuil » : 0 occurrence. Les deux mentions de fermeture « 2026-10-09 » restent à dater au versement (G-5), comme adjugé |

### 10.2 Aucun défaut neuf : contrôles sur l'arbre final a..k

| contrôle | résultat |
|---|---|
| `cargo --locked xtask verify` | S-G1..S-G8 VERT ; S-G9 ROUGE 1, la seule violation connue (docs/17 l.70, artefact de la copie creuse, déjà à `094fa5d`) ; fmt, no_std, clippy VERT |
| pas « Distillation » et « Construction » extraits par PyYAML | octets identiques aux pas de FZ-h (`079f035c…`, `b780011e…`) ; binaire AFL `9101e309…`, celui de la passe 1 |
| mes 12 scénarios du pas, rejoués comme la forge | mêmes issues qu'en passe 1 : aucune 0, VERT (E 1074, 745 gagnées dont 719 dans E, seuil 642) ; sans constats 1 (601 < 642) ; archive altérée, substituée (20), faible avec `SHA256SUMS` à jour, absente : 1 à l'épingle ; sommes périmées, ligne retirée, `SHA256SUMS` absent, ligne doublée, marqueur `*` : 1 ; somme fausse d'une carte : 0 au pas, refusée par `docs-sha256sums.py` (rc 1). N10 (changement de l'épingle) : 0, E 623, seuil 372, la voie que la règle de FZ-j réserve à un lot revu |
| mutants propres et rejeux G-1, G-3, cible par défaut | 17 issues conformes, identiques à la passe 1 : témoin vivant ; M5 tué par le seul test de G-1 et vivant avant FZ-g ; nom fixe planté rouge avant FZ-g, vert après ; S1-S3, E1, E3, E5, E6, A1-A3 tués ; E2, A4 vivants, équivalents |
| `enforcement/docs-sha256sums.py` | conforme, 35 `SHA256SUMS`, 299 lignes |
| jobs de `gates.yml` à `094fa5d` (dépôt jetable, `git add -A` sans commit) | 15 scripts, tous rc 0 : hooks 54, TODO/FIXME aucun, lint 227, R-1 OK, journaux-modele, docs-sha256sums 35/299, secrets 147, arbre 1181, vérificateur 137, s2-harness 415, s2bis 341, sim-bis 279, calib-actifs 65, controle 26 ; `--history` sans objet ; aucun fichier non suivi créé |
| jobs de `gates.yml` de la tête `5f99b4c`, sur `5f99b4c` + a..k + pièces | tous rc 0 : hooks 57, environnement, runners-epingles conforme (7 workflows, 22 clés), workflows-yaml 16 cas + conforme (PyYAML 6.0.1), lint 227, R-1 OK, journaux-modele, docs-sha256sums 35/299, secrets 147, arbre 1185, vérificateur 137, s2-harness 418, s2bis 341, sim-bis 279, calib-actifs 65, controle 36 |

- Restes dans le `TMPDIR` après `cargo test --locked --workspace` (cible par défaut) : `094fa5d` 119, a..h 34, a..k 34. Les
  34 existent déjà à la base (119 = 85 de `xtask/tests`, fermés par FZ-x, + 34) : ils sont antérieurs au lot et ne viennent
  pas de la série. Le compte recoupe l'item proposé par le générateur au §13.7 (SHOGEN-VERIFIER-TESTS-TMP-RESTES-1,
  34 par course). Je n'ai pas lu la source de ces restes, je n'ai que le compte.
- Recoupements du §13 du générateur : FZ-i..k identiques aux R-n ; rouge à a..h, vert à a..k, cible par défaut, 28 bilans
  ok : identiques à mes mesures. Sa remarque sur FZ-j (« le corpus dérivé fixe E » vaut à base fixée) rejoint mon O-1 :
  sans correction. Son mutant I1 (table `[workspace]` retirée), tué à la seule cible par défaut, est l'état a..h mesuré ici.

### 10.3 Écarts et limites de la passe 2

- E-6 : un premier contrôle des phrases de FZ-j par `grep -E` a rendu deux faux zéros (parenthèses lues comme un groupe) ;
  refait en `grep -F` : présentes.
- E-7 : dernier relevé de tête après le rapport (`093a174`, DT5-18 et DT5-19, 02:11) : 16 fichiers changés depuis `094fa5d`,
  aucun dans la série ; deux listes posées pour ce croisement à la racine du scratchpad, hors de mon dossier, supprimées aussitôt.
- Limite : la jambe Windows de `squelette.yml` n'est pas mesurée (hôte Linux). FZ-i ne dépend pas du système [inféré].
- FZ-i à FZ-k sont de ma main (R-1 à R-3) ; cette passe établit leur effet, pas une relecture indépendante de leur
  texte. Celle-ci est au §13.2 du générateur.
- Fichiers de la passe : `journaux/passe2/` (tests, scénarios, mutants, gates, verify), `journaux/passe2-tests.txt`,
  `outils/serie_k.sh`, `outils/passe2_tests.sh`, `outils/scenarios_cc_p2.py`, `outils/mutants_cc_p2.py`. Copies, cibles
  cargo, outils AFL copiés et `RUNNER_TEMP` supprimés en fin de passe ; `SHA256SUMS` du dossier réécrit en dernier.
