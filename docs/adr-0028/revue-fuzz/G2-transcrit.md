# Relecture G2 neuve du lot FUZZ (transcrit)

> Transcription par l'orchestrateur le 2026-10-10 03:36:30 UTC du fichier g2/RAPPORT-G2.md ; contrôle FM-1.1 des transcripts du générateur-correcteur, de l'advisor, du réviseur G2 et du contre-contrôleur, par le fm11.py versé et par celui de DT3-E : fragments_l51_l14 = 0 ; modèles résolus : claude-opus-5-5 (générateur, G2, contre-contrôle), claude-fable-5-1 (advisor). Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Relecture G2 neuve du lot FUZZ (distillation du corpus de fuzz, gate, noms fixes de `xtask/tests`)

- **Modèle** : `claude-opus-5-5`
- **Gate 0** : modèle résolu `claude-opus-5-5` (identifiant exact de l'environnement du réviseur) ; effort demandé : high.
  Réviseur neuf : je n'ai écrit aucune pièce de ce lot.
- Horloge (`date -u`) : ouverture 2026-10-09 23:47:25 UTC ; rédaction de ce rapport 2026-10-10 00:25:09 UTC.
- Brief : `BRIEF-G2.md`, sha256 `2877e9d134e780d2c0038ac87d7b90ead54fc8eb6d1f75cc1cb5e81aba03d2b2` (préfixe attendu conforme).
- Base : dépôt `/home/user/shogen`, tête `094fa5d3d5debe9dd466e37feee95200ca460dcf` (= base du brief), propre au début et à la
  fin (`git status --short` vide) ; aucune écriture git au dépôt, aucun commit, aucun push.
- Série relue, dans l'ordre a, b, c, d, f, e, x : empreinte de la concaténation
  `24def280387b4caa21d7034369b02edd65ea4aaa10831dc47a82f52c54937dda` (recalculée, égale au brief). Pièces à verser avec FZ-f :
  `versement/docs/adr-0028/revue-fuzz/pieces/` (`sha256sum -c` : 4 OK).
- `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée (environnement vidé, `env -i`, et retirée par `isole.sh`). Aucune pièce de D.2 ni
  dossier interdit ouvert ; copies creuses (sans dossiers interdits ni `*.jsonl`).
- Enregistrement du rôle G2 (`oracle_record.py`, D6 (viii)) : **sans objet** — le lot FUZZ est postérieur à la clôture de S2 et
  hors du dossier du cp-2 (cp-2 rendu le 2026-10-04, `docs/adr-0028/CP2-S2.md`) ; le brief ne le demande pas.

## 1. Verdict : **ACCEPTE-AVEC-CORRECTIONS (C-1 à C-5)**, liste fermée

Le lot fait ce que l'annexe A l.59 et l'adjudication demandent : graines distillées nommées et régénérables (108), gate
`cargo xtask fuzz-distillation` à E recalculé (C-2, C-3 de l'adjudication), câblage au job `cargo-afl`, règle L-3 et O-1 écrites,
SHOGEN-XTASK-TMP-NOMS-FIXES-1 traité (C-1 de l'adjudication). Tous les chiffres de référence sont reproduits à l'identique ;
les rouges reconstruits (E-4) sont rejoués ; aucune gate existante n'est affaiblie. Cinq corrections, dont deux de fond
(C-1, C-2), avec leur forme ; le diff proposé `C-G2.diff` (sha256 `15a4ffeb…5c5ff7d2a`) porte C-1 à C-3 et s'applique sur
l'arbre final de la série.

| C-n | constat | preuve | forme de la correction |
|---|---|---|---|
| **C-1** | trou de test sur le recalcul de E : mon mutant **M5** (E compté comme card(dérivé) − card(base) au lieu de la différence d'ensembles) **survit** aux 6 tests de `distillation.rs` ; il n'est pas équivalent : sur les cartes réelles, 3 arêtes de la base sont hors du dérivé, la gate imprime alors E 1071 et **seuil 640** au lieu de 1074 et 642 (`journaux/M5-sur-final.txt`) | M5 : construction faite (`Compiling xtask`), 6/6 verts | test neuf `apport_compte_en_ensemble_quand_le_derive_manque_des_aretes_de_la_base` (dérivé 5 à 109 sans les arêtes 0 à 4 de la base : E 100, seuil 60, 59 gagnées ROUGE) ; `xtask/tests/distillation.rs` +12 ; vert sur la série, **rouge sur M5** (`left: (95, 57)`, `right: (100, 60)`) |
| **C-2** | le seuil se déplace sans toucher à la gate : le dérivé fixe E, donc le seuil, et son seul ancrage est le `SHA256SUMS` voisin. Scénario rejoué : corpus sans les 26 constats (vraie mesure 601 < 642, ROUGE) **et** archive substituée par les 82 autres graines distillées **avec `SHA256SUMS` mis à jour** → somme OK, E 623, seuil 372, **VERT** (`journaux/scen-serie-original-substituee-sommes-a-jour-sans-constats.txt`) ; contourne L-3 (« jamais un seuil abaissé ») par une simple mise à jour de pièce | 5 scénarios du pas tel qu'écrit | empreinte de l'archive **épinglée dans le pas** (`echo "cbc2ab11…ba59dd  ${PIECES}/corpus-derive-2026-10-09.tar.gz" \| sha256sum -c -`, avant le contrôle au `SHA256SUMS`, gardé) et commentaire du pas ; phrase au README du corpus (« le remplacer est un changement de la gate (nouvelle mesure de référence datée, adjugée), jamais la réponse à un rouge ») ; `fuzz.yml` +5/−1, README +3. Pas corrigé : les 5 scénarios rendent l'issue attendue, la substitution avec sommes à jour devient ROUGE (`journaux/scenarios-ci.tsv`, ligne `corrige`) |
| **C-3** | `arbre_sur_un_reste_le_vide_d_abord` (`arbres.rs`, exclu du balayage) compose à la main un nom **fixe** sous `CARGO_TARGET_TMPDIR` (`essai-reste-d-un-processus-tue`) : contredit « deux exécutions simultanées ne partagent aucun chemin » (`commun/mod.rs`) pour deux `cargo test` sur une même cible | fichier planté à ce nom sous `target/tmp` : test ROUGE sur la série, vert corrigé (`journaux/c3-*.txt`) | nom suffixé du processus (`format!("essai-reste-d-un-processus-tue-{}", std::process::id())`, forme rustfmt) ; `arbres.rs` +4/−1 |
| **C-4** | documents vrais (rapport du générateur §2.6 et §10.4) : « secrets de l'arbre OK (1232 / 1239 fichiers) » a été rejoué sur un clone où les fichiers neufs étaient en `git add -N` et, [inféré de la même phrase], les fichiers modifiés non indexés ; `gate-secrets.sh --tree` lit l'**index** (`git show :0:<f>`) : il a lu des blobs vides pour les neufs et la version de base pour les modifiés, donc **pas la série** (mesuré : `add -N` → `git show :0:` rend 0 octet) | rejeu G2 sur index complet (`git add -A`, sans commit) : « OK (secrets) : 1181 fichier(s) », série comprise | ajout daté au rapport du générateur (ou au bloc de versement) : la portée G3 `--tree` de la série est celle du rejeu G2 (index complet), non celle du §2.6 ; aucune modification de la série |
| **C-5** | FZ-e date la fermeture « FERMÉE le 2026-10-09 » et « fermée (2026-10-09) » ; l'item n'est fermé qu'au versement, après cette G2 (2026-10-10 à l'horloge) | `date -u` | les deux mentions de fermeture prennent la date du versement relevée par `date -u` ; les mentions de mesure et d'adjudication (2026-10-09) restent |

Ordre de versement inchangé : les pièces de `revue-fuzz/pieces/` au plus tard avec FZ-f (sinon le pas rougit, échec fermé :
scénario « archive absente » du générateur [2nd] ; `sha256sum -c` sur une archive absente sort en 1, mesuré) ; C-1 à C-3 après FZ-x (le diff vise l'arbre final).

## 2. Checklist G2

- **Exactitude** : code de la gate relu en entier (`seuil`, `lire_carte`, `Mesure::de`, `vert`, `juger`, sous-commande), tables
  des 108 graines, pas CI, `commun::Arbre` et ses quatre migrations ; chiffres reproduits à l'octet (§4). Aucune erreur de code
  trouvée ; deux faiblesses de garde (C-1, C-2) et un nom fixe résiduel (C-3).
- **Tests rouges puis verts** (E-4 : rouges reconstruits) **rejoués** (`outils/rouges.sh`, une copie, une cible, nombre de tests
  relevé à chaque pas) : R-a 1 FAILED (`le_corpus_committe_…`) puis 2/2 ; R-b 1 FAILED puis 2/2 ; R-c (bouchons, `rouge_c.py` du
  générateur) 4 FAILED puis 6/6 ; R-d extraction du pas rc 2 puis 0 ; R-f (`rouge-f-distillation.rs.txt`, sha256 `91e5c378…`)
  2 FAILED (`gate_compte_…`, `commande_rend_…`) puis 6/6 ; R-x : balayage FAILED avant migration, nom fixe planté → témoin S-G9
  FAILED avant FZ-x, vert après ; suite entière verte après x. Tous conformes au rapport. Mes corrections : C-1 rouge sur M5, vert
  sur la série ; C-3 rouge (fichier planté) puis vert ; C-2 : scénario de substitution VERT avant, ROUGE après.
- **Mutants** : 17 du réviseur (§3) ; tallies du générateur recoupés sur ses TSV (10, 11, 14, 6/9, 12, 9, 9, 8 ; témoins vivants).
- **R-13** : `git grep` du job g5 (pas extrait de `gates.yml` par PyYAML, octets contrôlés) : aucun marqueur, série et C-G2 comprises.
- **R-8** : aucune dépendance neuve (aucun `Cargo.toml` ni `Cargo.lock` touché ; `xtask` dépendait déjà de `shogen-core` et
  `shogen-verifier`) ; outils du pas : `cargo afl showmap` (cargo-afl 0.18.2, admis), `tar`, `sha256sum`, `grep` de l'image.
- **R-25** (numstat, graines à part) : a +162/−1, b +147/−3, c +196/−1, d +68/0, f +126/−66, e +1/−1, x +137/−19 : chaque diff
  ≤ 200 ; graines 29 + 79 = 108 (10 455 + 36 110 octets, toutes distinctes) ; pièces 275 684 + 12 387 + 22 762 + 19 251 + 394
  octets. C-G2.diff : +24/−2.
- **Aucune gate affaiblie** : gate neuve ; pas inséré avant la campagne, campagne et verdict d'AFL++ inchangés ; mesure comparée
  plus stricte après FZ-f (719 dans E, non 745). C-2 ferme la seule voie trouvée pour déplacer le seuil hors de la gate.
- **Documents vrais** : README du corpus, `fuzz/README.md`, DEVOPS §3, docs/13 (FZ-e) recoupés contre les mesures rejouées ;
  O-1 rejouée à l'instrument de libFuzzer (§4) ; `fuzz/.gitignore` dit bien ce que `fuzz/README.md` lui prête. Restent C-4, C-5.

## 3. Mutants du réviseur (estimateur propre)

Classement : construction en échec = non viable ; `cargo test` 101 = tué, 0 = vivant, autre = FATAL (aucun FATAL) ; pas CI :
tué si un scénario rend une autre issue que l'attendue (aucune 0 / sans-constats 1 / archive altérée 1 / archive substituée 1).

| id | zone | mutation | issue |
|---|---|---|---|
| M1 | seuil | `div_ceil(789 + 1)` | TUÉ (`seuil_471_sur_789_…`) |
| M2 | seuil | `vert` compare à `seuil(gagnees)` | TUÉ (2 tests) |
| M3 | seuil | tolérance d'une arête (`+ 1 >=`) | TUÉ (2 tests) |
| M4 | E | `derive.difference(corpus)` | TUÉ (2 tests) |
| **M5** | E | E par comptes, card(D) − card(B) | **VIVANT, non équivalent** (seuil réel 640) → **C-1** |
| M6 | E | `juger` lit le dérivé au chemin du corpus | TUÉ (`commande_rend_…`) |
| S4 | somme | contrôle au `SHA256SUMS` neutralisé (`\|\| echo`) | TUÉ (archive substituée) |
| S7 | somme | contrôle porté sur la ligne d'une carte | TUÉ (archive substituée) |
| SE1 | E (pas) | dérivé remplacé par le corpus | TUÉ (sans-constats VERT) |
| SE2 | E (pas) | dérivé versé dans la base | TUÉ (aucune ROUGE) |
| X1 | Arbre | rang figé (`load`) | TUÉ (`arbre_unique_…`) |
| X2, X3, X4 | Arbre | aides qui ne tiennent plus l'`Arbre` (fuite à nom unique sous `target/tmp`) | VIVANTS, équivalents d'issue pour l'objet de C-1 (aucune collision, aucun nom fixe) ; la fuite (65 dossiers) n'est vue que par le témoin |
| X5, X6 | Arbre | arbre effacé **avant** l'emploi (`arbre_copie`, `arbre_menace`) | TUÉS en masse (15 et 46 tests) : les tests ne passent pas à vide |
| X7 | Arbre | idem `arbre_documentaire` | NON VIABLE (types) |

Score : 16 viables, 12 tués avant correction ; avec C-1, 13 sur 13 non équivalents. Hors matrice, sonde de C-2 : substitution
avec sommes à jour, VERT sur la série, ROUGE sur le pas corrigé.

## 4. Rejeux (copie creuse de `094fa5d` + série + pièces, isolée : `unshare -n`, `env -i`)

- `cargo --locked xtask verify` : S-G1 à S-G8 VERT ; S-G9 ROUGE, une violation (docs/17 l.70, référence vers un dossier interdit
  absent de la copie creuse) ; fmt, no_std, clippy (`--all-targets`) VERT. **Même violation, seule, sur `094fa5d` creuse sans la
  série** : SHOGEN-SG9-COPIE-INTERDITS-1 (annexe B l.834), artefact de la copie, hors du lot. Idem sur la copie corrigée.
- `cargo --locked test -p xtask` : arbres 3, distillation 6, mutants 81, reproductible 9, tout vert (corrigé : distillation 7).
- Pas « Distillation » extrait de `fuzz.yml` (PyYAML 6.0.1) et lancé comme la forge, après le pas de construction, cargo-afl
  0.18.2 (« AFL++ version 4.40c ») : rc 0 ; cartes 1339 (15 fichiers), 2084 (123), 2410 (2353) ; E 1074, gagnées 745 dont 719 dans
  E, seuil 642, perdues 0, VERT. Cartes base et corpus **identiques à l'octet** aux cartes versées ; union base ∪ dérivé = carte
  versée. Gate directe sur les trois cartes versées : même mesure, VERT ; 2 arguments rc 64 ; base comme corpus ROUGE rc 1.
- Recompte indépendant (python) : E 1074, 745, 719, hors E 26, perdues 0, seuil `(1074·471 + 788) // 789` = 642, marge 77 ;
  642/1074 = 59,78 % ≥ 471/789 = 59,70 % ; seuil(789) = 471.
- Corpus régénéré depuis vide (`fuzz-corpus`) = corpus de la série à l'octet (124 `dirigee-*`).
- `cargo xtask fuzz --duree 60` (release) : VERT, 124 graines, 46 930 556 cas, graine 0x5000001100000007, aucun `panique-*`.
- Jobs de `gates.yml` (copie creuse indexée `git add -A`, sans commit) : hooks 54, TODO/FIXME aucun, lint 227, R-1 OK,
  journaux-modele conforme, docs-sha256sums 35 SHA256SUMS / 299 lignes, secrets 147, arbre 1181 fichiers OK, runner 137,
  s2-harness 415, s2bis 341, sim-bis 279 (avec `objects/info/alternates` en lecture seule vers les objets du dépôt : sans eux,
  3 erreurs `git archive` de commits historiques, artefact d'un dépôt neuf), calib-actifs 65, controle 26 ; mêmes résultats sur
  la copie corrigée. `--history` sans objet (série non commise ; son contenu est balayé par `--tree`).
- `enforcement/docs-sha256sums.py` : conforme (35 / 299 ; base 34 / 295). Lecture YAML : `fuzz.yml` 4 jobs, 11 pas au job
  `cargo-afl` (10 à la base) ; `gates.yml` 8 jobs ; `fuzz.yml` corrigé lisible.
- **Témoin C-1** (deux copies, cibles distinctes, même TMPDIR neuf, simultanés) : après la série, 3 essais sur 3 : deux exécutions
  vertes, **0 dossier laissé** ; à `094fa5d`, 2 essais sur 2 : une exécution rouge par essai (au premier :
  `mutant_couverture_fichier_neuf_dans_le_role`), 85 dossiers laissés.
- **O-1 rejouée** (nightly-2026-08-10 installée dans un RUSTUP_HOME du dossier G2, rustup partagé intact, supprimée après) :
  base 724, base + distillées 1218, base + dérivé 1575, fusion « 910 new files with 2035 new features added; 378 new coverage
  edges » ; 1596 − 1218 = 378 en `-runs=0` : chiffres du README confirmés, (851 − 378)/851 = 55,6 %.

## 5. Point 4 du brief

- Règle « redistiller, jamais abaisser le seuil » : écrite au README du corpus (« **Règle** : … appelle une nouvelle distillation,
  jamais un seuil abaissé ») et dans FZ-e (« redistiller, jamais abaisser le seuil ») ; C-2 l'étend au dérivé.
- O-1 : écrite au README du corpus (chiffres et motif : « Les deux instruments ne comptent pas les mêmes arêtes ; 13 §7 fixe
  afl-showmap, seul instrument de la gate ») et dans FZ-e (55,6 %, sans second seuil) ; chiffres confirmés (§4).
- Seuil non desserré par la transposition : ⌈E × 471/789⌉ arrondit au-dessus (642/1074 = 59,78 % ≥ 59,70 %) ; mesure comparée
  stricte (gagnées **dans** E) ; seuil ≥ top-20 du glouton pour les 32 départages essayés (615 à 624, §6). La seule voie de desserrage
  trouvée passe par la substitution du dérivé (C-2).

## 6. Observations (sans correction)

- O-a : top-20 du glouton dépendant du départage : 624 (départage par nom croissant, = rapport et avis), 616 (décroissant),
  615 à 624 sur 30 départages aléatoires ; 642 atteint au rang 23 ou 24. Le contrôle de cohérence de l'avis (642 ≥ top-20) tient pour les 32 départages essayés.
- O-b : l'annexe A l.59 inférait ≈ 60-120 lignes ; la série FUZZ en ajoute 700 hors graines (FZ-x à part), chaque diff sous 200
  (R-25 tenu) : écart d'estimation à consigner au versement.
- O-c : l'archive est binaire pour git (30 octets NUL dans les 8000 premiers) : aucune conversion sous `* text=auto eol=lf` ;
  avec C-2, toute altération rougit de toute façon.
- O-d : à consigner au versement (actes de l'orchestrateur, hors série) : fermeture de SHOGEN-FUZZ-DISTILLATION-1 et de
  SHOGEN-XTASK-TMP-NOMS-FIXES-1, rappel de Q-1 (SHOGEN-E1-XTASK-REFS-1 déjà fermé), substitution de la ratification C-10.

## 7. Écarts du réviseur

- E-1 : comptes récursifs sur ma copie creuse pour contrôler les exclusions (`find … | wc -l`, `find docs -maxdepth 1 -name …`),
  un `wc -l xtask/src/*.rs xtask/tests/*.rs` au dépôt, des `diff -r -q` entre mes copies, un `grep -l` sur les journaux nommés du
  générateur : sorties limitées à des comptes, des noms hors emplacements interdits ou à « aucune différence » ; aucun chemin
  interdit lu ni affiché. Contraire à la lettre « aucune liste par motif » : déclaré.
- E-2 : la première commande `isole_g2.sh … cargo afl --version` a tourné avec le dépôt pour répertoire courant ; aucune
  écriture (`git status` vide, relevé à la fin).
- E-3 : mes mutants X2 à X4, voulus « arbre effacé avant l'emploi », ont réalisé une fuite (l'`Arbre` lâché aussitôt) :
  reclassés comme tels ; X5 et X6 ajoutés pour l'effacement avant emploi.
- E-4 : nightly-2026-08-10 (admise par R-8) installée par le réseau, dans le dossier G2 seulement, pour rejouer O-1 ; supprimée.

## 8. Journal de provenance

[lu] : BRIEF-G2 et BRIEF-FUZZ (entiers) ; ADJUDICATION, avis/AVIS.md, RAPPORT-GENERATEUR, NOTES du générateur (entiers) ;
annexe A l.59 ; annexe B l.28, l.832, l.834, l.920-933 (noms trouvés par grep dans ANNEXE-B-items.md seul) ; docs/13 titres,
l.86-101, l.185-195 ; annexe D l.28-50 (liste D.2, pour l'appliquer) ; CP2-S2.md l.1-12 et l.30-40 ; docs/12 l.99-114 ; les sept
diffs en entier (code ; graines par numstat et par octets) ; fuzz.yml (en-tête, jobs pr et cargo-afl), gates.yml (l.1-120 et
commandes des jobs), fuzz/README.md, README du corpus, fuzz/.gitignore, fuzz/.gitattributes, .gitattributes, xtask/Cargo.toml,
rust-toolchain.toml, docs-sha256sums.py, gate-secrets.sh (l.1-60 par grep, l.160-202), oracle_r1.py et oracle_recalc.py
(fonctions `extraire`), xtask main.rs l.105-135, mutants.rs (aides), reproductible.rs l.170-200 et l.320-330, distillation.rs
final ; journaux du générateur lf-fusion.log, campagne-libfuzzer.log, résultats de mutants. [2nd] : aucun chiffre retenu sans
rejeu (les chiffres libFuzzer, d'abord [2nd], sont rejoués §4). [abs] : aucune.

Commandes (sorties dans `journaux/`, scripts dans `outils/`, sommes au `SHA256SUMS`) : `git archive 094fa5d` avec exclusions ;
`git apply` de la série ; `outils/verifier.sh` (verify, test) ; `outils/pas_ci_g2.py` + `outils/isole_ci.sh` (pas CI) ;
`outils/temoin.sh` ; `outils/rouges.sh` ; `outils/mutants_g2.py` ; `outils/scenarios_ci.py` ; `outils/jobs_gates.sh` ;
`cargo xtask fuzz --duree 60` ; `cargo fuzz build` et `eprouver -runs=0` / `-merge=1`. Chiffres recomptés : 1339, 2084, 2410,
1074, 745, 719, 26, 0, 642, 77 (python sur mes cartes) ; 108, 124, 10 455, 36 110 (`ls`, `wc -c`) ; numstat R-25 ; 724, 1218,
1575, 1596, 1229, 1607, 378 (libFuzzer rejoué) ; top-20 615 à 624 (glouton sur 2353 cartes par graine).

## 9. Fichiers rendus

`RAPPORT-G2.md` (ce fichier), `NOTES.md`, `C-G2.diff` (C-1 à C-3), `outils/` (scripts du réviseur), `journaux/` (sorties),
`BRIEF-G2.md`, `SHA256SUMS` du dossier (écrit en dernier). Copies et cibles cargo supprimées après usage.
