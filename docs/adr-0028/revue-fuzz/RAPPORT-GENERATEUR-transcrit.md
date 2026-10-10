# Rapport du générateur du lot FUZZ, avec ses sections datées de correction (transcrit)

> Transcription par l'orchestrateur le 2026-10-10 03:36:30 UTC du fichier RAPPORT-GENERATEUR.md ; contrôle FM-1.1 des transcripts du générateur-correcteur, de l'advisor, du réviseur G2 et du contre-contrôleur, par le fm11.py versé et par celui de DT3-E : fragments_l51_l14 = 0 ; modèles résolus : claude-opus-5-5 (générateur, G2, contre-contrôle), claude-fable-5-1 (advisor). Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Rapport du générateur G1 — lot FUZZ (ADR-0028 annexe A l.59) et SHOGEN-E1-XTASK-REFS-1

- **Modèle** : `claude-opus-5-5`
- Gate 0 : identifiant résolu de la session worker `claude-opus-5-5` ; effort demandé par le brief : high.
- Horloge : départ `Fri Oct  9 22:03:18 UTC 2026` ; rédaction de ce rapport à partir de 23:14:49 UTC (relevés `date -u`).
- Brief : `BRIEF-FUZZ.md`, sha256 `199647f1e90c9147dc175f648672e4e766ac3b2a893183bfa6fa4d84345deb9f` (préfixe attendu conforme).
- Base : copie `git archive` de `c1122de` ; après le redémarrage du conteneur (vers 22:55 UTC), tête du dépôt `094fa5d`
  (fusion de la PR #10, parents `6356a94` et `c1122de`), **arbre identique** (`f8c869cd…` des deux côtés, `git diff --quiet`
  vrai) : la série s'applique telle quelle sur `094fa5d` (contrôlé, §2.6).
- Aucune écriture git au dépôt, aucun commit, aucun push. `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée (environnement vidé par
  `env -i` dans tous les contrôles isolés). Aucune pièce de D.2 ni dossier interdit ouvert.

## 0. Résumé

| item | état proposé | pièces |
|---|---|---|
| SHOGEN-FUZZ-DISTILLATION-1 (13 §7 dette 3) | **fermeture proposée** : corpus dérivé distillé en 108 graines nommées régénérables, 719 des 1074 arêtes du dérivé (66,95 % ≥ 471/789 = 59,70 %), gate `cargo xtask fuzz-distillation` (seuil 642), câblée au job `cargo-afl` | FZ-a, FZ-b, FZ-c, FZ-d (+ FZ-e facultatif : docs/13) |
| SHOGEN-E1-XTASK-REFS-1 | **déjà fermé** en B.51 (lot DETTES-B2, commits XR-1 à XR-4) : aucun diff ; cas nommés vérifiés vivants à `094fa5d` (8 neutralisations, 8 tuées par leur test nommé) | §3, Q-1 |
| SHOGEN-XTASK-TMP-NOMS-FIXES-1 | déclencheur atteint par ce lot (FZ-a ajoute `xtask/tests/distillation.rs`) : **fermeture proposée**, diff séparé | FZ-x (facultatif), Q-4 |

## 1. Rattachement (G0), lu avant d'écrire

- Annexe A l.59 (lot FUZZ) : distillation du corpus dérivé (13 §7.3 : au moins 471/789 arêtes) et gate de distillation
  (M-13 : aucune aujourd'hui) ; corpus + `xtask` ; gate de couverture rouge sous le seuil (mutant semé) ; `cargo xtask fuzz` ;
  ≈ 60-120 [inféré, hors octets du corpus] ; corpus dérivé → corpus distillé → CI fuzz ; cp-1 bref.
- ADR-0028 l.236 : distillation du corpus fuzz (échue), lots E1 et FUZZ.
- Annexe B l.28 : SHOGEN-FUZZ-DISTILLATION-1, déclencheur « maintenant (lot FUZZ) », origine F-DP-09 ; 13 §7.3.
- Annexe B l.143 : SHOGEN-E1-XTASK-REFS-1, déclencheur « G0 du prochain lot qui modifie `xtask` (lot FUZZ) ».
- docs/13 l.195 (§7, dette 3) : 789 arêtes hors corpus committé (1055 → 1844 sur 3024) ; top-20 = 471/789 ; nommer les
  formes, étendre `fuzz-corpus` en `dirigee-*` régénérables ; gate d'acceptation ≥ 471 des 789 au même outillage de mesure ;
  repli `derivee-*` par amendement d'ADR-0011 pour l'innommable.
- JOURNAL l.122 (2026-09-30) : première tentative bloquée (instrument afl-showmap AFL++ 4.40c sous WSL2, binaire de
  `20e1084`, non rejouable : `crates/` changé à `58dc96e`) ; Q-FUZZ-1 au mainteneur (nouvelle base sur le binaire courant
  sous Linux, distillation sans afl, ou report) ; seuil 471/789 candidat, ratification due (C-10). JOURNAL l.143 : Q-FUZZ-1
  routée. Aucune réponse trouvée aux pièces lisibles (Q-2).

## 2. SHOGEN-FUZZ-DISTILLATION-1

### 2.1 Fermeture proposée

Option 1 de Q-FUZZ-1 appliquée (l'hôte cloud est un Linux) : **nouvelle base sur le binaire courant, au même outil**
(`afl-showmap -C` d'AFL++ 4.40c), campagnes refaites au protocole de `fuzz/README.md` (660 s par moteur), corpus dérivé
neuf, puis distillation par la méthode de 13 §7 dette 3 : analyse du dérivé (glouton sur les arêtes, oracle de classement
non-LLM : le vérificateur lui-même), formes **nommées**, générateur étendu, graines `dirigee-*` régénérables. Aucune
graine innommable n'a été nécessaire : **aucun repli `derivee-*`, donc aucun amendement d'ADR-0011**.

Le seuil écrit (fraction 471/789) est appliqué à la mesure neuve : ⌈1074 × 471/789⌉ = **642** arêtes
(789 × 641 = 505 749 < 1074 × 471 = 505 854 ≤ 789 × 642 = 506 538). La transposition est une décision (Q-2).

La famille distillée (`xtask/src/distillation.rs`), 108 graines, chacune avec le fragment de classement que le vérificateur
doit en rendre : 29 `subject` (une règle d'ADR-0016 par graine, plus trois formes acceptées riches), 15 altérations de champ
du lot canonique, 18 substitutions d'en-tête ou de clé (une par carte : clé inconnue, clés non triées, clé double, tailles,
types), 12 troncatures juste après chaque clé, 26 constats (un refus nommé d'ADR-0015 pt 13 par graine), 6 bords CBOR,
2 registres (texte Unicode riche, texte blanc).

### 2.2 Mesures (outil, version, nombre d'arêtes)

Outils, tous admis par R-8 (`docs/R-8-outillage.md`) : cargo-afl 0.18.2 (`--locked`), « cargo-afl 0.18.2 (AFL++ version
4.40c) », rustc 1.97.1 (8bab26f4f 2026-07-14) ; cargo-fuzz 0.13.2 (`--locked`) sur nightly-2026-08-10, servie
« rustc 1.99.0-nightly (969b803cb 2026-08-09) » (= épinglée) ; `fuzz/Cargo.lock` inchangé par `cargo fuzz build`.

| mesure (afl-showmap -C, binaire de `c1122de`, 3904 arêtes existantes, map size 3850) | arêtes |
|---|---|
| corpus dirigé d'origine B (16 graines, l'entrée vide sautée : 15 fichiers) | 1339 (34,30 %), 3 mesures identiques |
| B + dérivé (2353 entrées) = F | 2413 ; **E = F − B = 1074** ; B ⊆ F |
| glouton sur le dérivé : top-20 | 624/1074 (58,1 %) ; 642 atteint au rang 23 (648) |
| B + 108 graines distillées = C (124 graines) | 2084 ; **gagnées 745** ; **dans E : 719 (66,95 %)** ; hors E : 26 ; base perdue : 0 |
| après FZ-a seul (29 graines `subject`, 45 au corpus) | 1511 ; gagnées 172 (dans E 171, 15,92 %) → sous le seuil |
| après FZ-b (108 graines, 124 au corpus) ; FZ-c et FZ-d ne changent aucune graine | 2084 ; carte identique à l'octet à la ligne ci-dessus |
| prototype sans constats, CBOR ni registres (74 graines du lot canonique) | 1862 ; gagnées 523 (dans E 501) → sous le seuil |
| mutant semé : corpus sans les 26 constats | gagnées 623 < 642 → **ROUGE** |

Campagnes (dérivé) : AFL++ `-V 660`, run_time 660 s, execs_done 12 435 382, corpus_count 1123 (1108 trouvés), bitmap_cvg
61,51 %, edges_found 2368/3850, 0 plantage, 0 blocage ; libFuzzer `-max_total_time=660 -seed=20261009`, « Done 38234147 runs
in 661 second(s) », cov final 1534, 1250 entrées, aucun artefact. Union dédoublonnée par sha256 (base et vide exclues) :
2353 entrées.

Contre-mesure à un second instrument (libFuzzer, compteurs 8 bits, binaire nightly) : base cov 724 ; base + distillées 1218 ;
base + dérivé 1575 ; fusion `-merge=1` (base + distillées, puis dérivé) : 378 arêtes neuves du dérivé. Part couverte à cet
instrument ≈ (851 − 378)/851 = 55,6 % : le seuil tient à l'outil de référence, pas à celui-ci (O-1).

### 2.3 Diffs (série, base `094fa5d` = arbre de `c1122de`)

| diff | contenu | lignes ajoutées / retirées (hors graines) | graines | sha256 |
|---|---|---|---|---|
| FZ-a | `xtask/src/distillation.rs` (module, famille `subject`), crochet de `fuzz.rs` (`ecrire_corpus_dirige`), `lib.rs`, `xtask/tests/distillation.rs` (classement de chaque graine ; corpus committé = corpus régénéré, graines distinctes) | +162 / −1 | 29 (10 455 octets) | voir `SHA256SUMS` |
| FZ-b | familles 2 à 6 (altérations, substitutions, troncatures, constats, CBOR, registres) | +147 / −3 | 79 (36 110 octets) | idem |
| FZ-c | gate : `seuil`, `lire_carte`, `Mesure`, `juger` ; sous-commande `fuzz-distillation` (codes 0 vert, 1 rouge ou carte illisible, 64 usage) ; 4 tests | +196 / −1 | 0 | idem |
| FZ-d | pas « Distillation » du job `cargo-afl` de `fuzz.yml` (avant la campagne) ; README du corpus (famille, mesure, gate) ; `fuzz/README.md` (rejeu) ; ligne datée de DEVOPS §3 | +68 / 0 | 0 | idem |
| FZ-e (facultatif) | docs/13 §7 dette 3 : barrée, FERMÉE le 2026-10-09, mesures ; échéance « fermée » | +1 / −1 | 0 | idem |
| FZ-x (facultatif) | SHOGEN-XTASK-TMP-NOMS-FIXES-1 : `temp_dir()` → `CARGO_TARGET_TMPDIR` aux quatre sites des tests de `xtask` | +9 / −4 | 0 | idem |

Ordre d'application : a, b, c, d, puis e et x dans l'ordre voulu (x s'applique aussi directement après d). `git apply` avertit
« space before tab » sur FZ-b : c'est le contenu voulu de la graine `registre-blanc` (texte tout blanc) ; aucune gate du dépôt
ne contrôle les blancs.

### 2.4 Tests, rouges puis verts

- R-a (FZ-a) : code de l'étape, corpus sans ses graines distillées → `le_corpus_committe_est_ce_que_le_generateur_ecrit_graines_distinctes`
  FAILED (« corpus committé ≠ corpus régénéré ») ; corpus régénéré → 2/2 verts.
- R-b (FZ-b) : code de l'étape b, corpus de l'étape a → même test FAILED ; corpus régénéré → 2/2.
- Rouge réel en développement : la graine constat `cle-non-triee` d'abord mal construite (rendu `CleManquante`) a été vue par
  `chaque_graine_distillee_rend_le_classement_que_son_nom_annonce`, puis corrigée (`CleNonTriee`).
- R-c (FZ-c) : gate en bouchons de même signature (`scripts/rouge_c.py`) → les 4 tests de gate FAILED ; code réel → 6/6.
- R-d (FZ-d) : rejeu local du pas tel qu'écrit (`scripts/pas_ci.py`, lecture YAML du workflow) avant l'ajout → code 2 (pas
  introuvable) ; après : corpus complet code 0 (VERT, 745), sans les constats code 1 (ROUGE, 623), graines renommées code 1
  (`rm` sans correspondance), sans graines distillées code 1.
- Écart de méthode déclaré (E-4) : prototype écrit avant les tests ; les rouges ci-dessus sont reconstruits (bouchons, corpus
  échangés), sauf le rouge réel cité.

### 2.5 Mutants (au moins 8 par diff de code ; classement : construction en échec = non viable, sortie 101 = tué, 0 = vivant, autre = FATAL)

- FZ-a : **10/10 tués** (A1 crochet retiré, A2 préfixe, A3 subject non posé, A4 port 443 → 8443, A5 hôte vide, A6 `./` →
  `../`, A7 instant de l'exemple, A8 extension, A9 attendu, A10 triplet `%2B` → `%2b`).
- FZ-b : **11/11 tués** (B1 remplacement neutralisé, B2 queue gardée, B3 position jamais trouvée, B4 troncature avant la clé,
  B5 en-tête 0x40, B6 altération déplacée, B7 version inchangée, B8 octet CBOR, B9 ligne de registre, B10 clé du constat,
  B11 `replacen(…, 0)`). B5 n'était tué que par le test du corpus : attendu des troncatures resserré en
  `Refuse(FinPrematuree` (une graine vide passait par la surface constat).
- FZ-c : **14/14 tués** (C1 `>` au lieu de `>=`, C2 garde des arêtes perdues retirée, C3 division entière, C4 471 → 472,
  C5 1074 → 1073, C6 compte nul accepté, C7 arête répétée acceptée, C8 carte vide acceptée, C9 ligne fautive sautée — tué
  après durcissement du test : chaque faute suit une ligne valide —, C10 différence inversée, C11 cartes échangées, C12 codes
  inversés, C13 erreur rendue 0, C14 usage rendu 1).
- FZ-d (pas CI, `scripts/mutants_ci.py`, quatre corpus par mutant) : **6/9 tués** (D1 base non retranchée, D2 cartes
  échangées, D3 sans `-C`, D4 copie partielle, D7 juge remplacé par `true`, D8 base mesurée sur le corpus) ; **3 vivants,
  équivalents d'issue** : D5 `rm -f` (la gate rougit quand même, 0 arête gagnée), D6 sans `set -euo pipefail` (une carte
  manquante rend la gate rouge), D9 README gardé (il entre aux deux cartes, la différence ne bouge pas).

### 2.6 Contrôles

- Application : série a..x appliquée par `git apply` sur `git archive 094fa5d` = arbre final à l'octet ; a..d = arbre de
  FZ-d ; FZ-x s'applique directement après FZ-d.
- `cargo --locked xtask verify` (réseau coupé, `env -i`), à chaque étape (a, b, c, d, e, x) : VERDICT GLOBAL VERT (S-G1 à S-G9,
  fmt, no_std, clippy -D warnings), lignes de verdict seules relevées.
- `cargo --locked test -p xtask`, à chaque étape : distillation 2/2/6/6/6/6, mutants 81, reproductible 9, aucun échec.
- `cargo xtask fuzz` (arbre de FZ-d, release, isolé) : `--duree 30` VERT, 124 graines, 19 671 420 cas ; **budget par défaut
  900 s** (23:04:01-23:19:07 UTC) : VERT, « zéro panique sur 698072444 cas, graine 0x5000001100000007 », dont 4 431 950 en
  forme canonique des sept champs ; aucun `panique-*` écrit.
- Jobs de `gates.yml` rejoués sur un clone local du dépôt, série appliquée sans commit (nouveaux fichiers en `add -N` dans le
  clone), chacun isolé : hooks 54 ok ; motif TODO/FIXME : aucun (code 1) ; cas du lint 227 ok ; lint de l'arbre OK ; ligne
  Modèle conforme ; `docs-sha256sums.py` conforme (34 SHA256SUMS, 295 lignes) ; cas des secrets 147 ok ; secrets de l'arbre
  OK (1232 fichiers) ; historique OK (738 commits) ; runner `run-fixtures-verdict-suite-s2.py` 137 ok ; suites s2-harness
  Ran 415 (sauts nommant la variable scellée), s2bis 341, sim-bis 279, calib-actifs 65, controle 26, toutes conformes.
- Lecture YAML (`python3 -c`, PyYAML de l'environnement) de `fuzz.yml` : lisible, 4 jobs, 11 pas au job `cargo-afl`.
- Attributs : les graines neuves héritent de `crates/shogen-verifier/fuzz-corpus/** -text` (`git check-attr` : text unset).

## 3. SHOGEN-E1-XTASK-REFS-1 : déjà fermé, rien à mécaniser

Annexe B l.819-822 (B.51, 2026-10-04) : item fermé par les commits XR-1 `1c2f0f2`, XR-2 `ef657b9`, XR-3 `7c4861a`, XR-4
`c278b48` (gate S-G9 sur `docs/17`, contrôles (a) à (f) ; (g) et (h) déclarés non mécanisés, reportés à
SHOGEN-SG9-STRUCTURE-1). Les cas nommés par l'item sont des tests de `xtask/tests/mutants.rs` : résidu en majuscules (b),
apostrophes (e), décimal, pour-cent en lettres, nom nu de D.2 n° 8 (f), borne des lots MONARK de (c) (témoin), mut1
(JJ/MM/AAAA) et mut5 (guillemets droits). Preuve rejouée à `094fa5d` (= `c1122de`) : 8 neutralisations de `sg9.rs`, **8 tuées
par leur test nommé** (`mutant_sg9_b_residu_en_majuscules`, `mutant_sg9_e_apostrophes`, `mutant_sg9_f_nombre_decimal`,
`mutant_sg9_f_pour_cent_en_lettres`, `mutant_sg9_f_nom_nu_de_d2_n8`, témoins `temoin_sg9_bornes_monark_et_px_listees` et
voisins, `mutant_sg9_d_jj_mm_aaaa` et voisins, `mutant_sg9_e_guillemets_droits`). `verif_refs.py` n'est pas au dépôt
(`git ls-files` : aucun). Le lot FUZZ ne touche pas S-G9 : les déclencheurs des résidus (SG9-COPIE-INTERDITS-1 « prochain lot
qui touche S-G9 », SG9-PERIMETRE-1, SG9-CORPUS-1, SG9-STRUCTURE-1) ne sont pas atteints.

## 4. SHOGEN-XTASK-TMP-NOMS-FIXES-1 (déclenché par ce lot) : FZ-x

FZ-a ajoute un fichier à `xtask/tests` : le déclencheur (« prochain lot qui touche `xtask/tests` », reporté en B.56 ; DETTES-T4
a touché `xtask/tests` sans le traiter, B.91) est atteint. FZ-x place les arbres temporaires des tests sous
`CARGO_TARGET_TMPDIR` (propre à la cible cargo de chaque copie) au lieu du `temp_dir()` commun. Rouge puis vert : un fichier
planté au nom fixe `shogen-mutant-sg9-temoin` dans le `TMPDIR` commun (comme le laisserait une autre session) fait échouer
`temoin_sg9_arbre_menace_intact_est_vert` sur la base (panique `mutants.rs:92`), et le laisse vert avec FZ-x. Constat annexe :
85 répertoires `shogen-*` laissés par les exécutions précédentes dans le `TMPDIR` du lot. Les nouveaux tests de FZ-a et FZ-c
écrivent déjà sous `CARGO_TARGET_TMPDIR`.

## 5. Questions à l'orchestrateur

- **Q-1** : le point 2 du brief vise un item fermé en B.51 (l'ETAT-REGISTRE du 2026-10-04, 03:53Z, est antérieur à XR-4,
  08:24Z). Confirmer « rien à faire » (aucun diff ; preuve §3).
- **Q-2** : Q-FUZZ-1 (mainteneur) reste sans réponse écrite lisible ; le lot applique l'option « nouvelle base sur le binaire
  courant sous Linux ». La fraction 471/789 est transposée à E = 1074 (seuil 642) ; 13 §7 la disait candidate, ratification
  du mainteneur due (JOURNAL l.122, C-10). Adjuger la transposition et la forme du seuil (fraction appliquée à une mesure datée
  du binaire de `c1122de`).
- **Q-3** : FZ-e (fermeture écrite dans docs/13 §7) est à appliquer à l'adjudication seulement.
- **Q-4** : FZ-x ferme SHOGEN-XTASK-TMP-NOMS-FIXES-1, déclenché par ce lot ; diff séparé (R-25) ; à prendre ou à reporter
  par décision écrite.
- **Q-5** : « M-13 » (annexe A l.59) n'est défini dans aucune pièce lisible (docs/12, docs/13, DEVOPS, DECISIONS,
  AUDIT-ENTREE, ADR-0028 et annexes, PASSATION, R-8) ; ADR-0028 l.165 renvoie les M-n à « la critique v1 », non localisée.
  Lu comme « aucune gate de distillation aujourd'hui », ce que FZ-c et FZ-d créent. Confirmer la source.
- **Q-6** : où verser les pièces hors dépôt de la mesure (`pieces/` : corpus dérivé 2353 entrées en tar.gz de 275 684 octets,
  trois cartes afl-showmap, glouton top-60, `SHA256SUMS`) ; 13 §7 voulait ces pièces durables.

## 6. Limites (chacune liée à un lot futur nommé ou à un acte extérieur)

- **L-1** (acte extérieur : forge) : le pas CI n'a tourné qu'en local (rejoué tel qu'écrit) ; la forge ne démarre pas les
  jobs (GC-01). La première exécution sur un runner, et l'égalité attendue des comptes d'arêtes sur un binaire construit
  ailleurs (mesurée ici entre deux constructions locales de chemins différents : sha256 différents, 1339 et 2084 arêtes
  identiques), relèvent du premier run des jobs fuzz sur la forge.
- **L-2** (inhérente, écrite au README du corpus) : la gate CI compte les arêtes gagnées par les graines distillées (745) sans
  pouvoir les intersecter avec E, le dérivé n'étant pas versé ; la mesure stricte (719 dans E) a été faite une fois, ici.
- **L-3** (lot futur : toute modification du vérificateur ou du cœur) : la mesure de référence date du binaire de `c1122de` ;
  un changement qui fait passer la gate sous 642 appelle une nouvelle distillation, jamais un seuil abaissé (écrit au README).

### Observation (sans item : 13 §7 dette 3 fixe l'outil de mesure)

- **O-1** : à l'instrument de libFuzzer (compteurs 8 bits du binaire nightly, assertions de débogage comprises), la famille
  couvre ≈ 55,6 % de l'apport du dérivé, sous 471/789 ; à l'outil de référence (afl-showmap), 66,95 %. La gate et
  l'acceptation sont au même outillage que la mesure de 13 §7, comme écrit. Un critère tenu aux deux instruments serait une
  exigence nouvelle (Q-7).
- **Q-7** : exiger aussi la fraction à l'instrument de libFuzzer ? Si oui, c'est un lot de distillation complémentaire
  (fusion `-merge=1` déjà outillée : 910 entrées du dérivé apportent 378 arêtes à cet instrument).

## 7. Écarts

- **E-1** : boucles d'attente `pgrep -f 'afl-fuzz'` qui se trouvaient elles-mêmes ; tuées à la main, sans effet sur les
  campagnes ; attente par PID ensuite.
- **E-2** : une passe d'étapes a partagé `CARGO_TARGET_DIR` ; cargo a servi le code de l'étape 1 aux étapes 2 et 3 sans
  recompiler (SHOGEN-HARNAIS-CIBLE-PARTAGEE-1 reproduit) ; rejoué avec une cible par copie.
- **E-3** : deux titres des NOTES portaient des heures estimées, fausses ; corrigés sur les heures relevées à la reprise.
- **E-4** : tests écrits avec le prototype, pas avant ; rouges reconstruits (§2.4).
- **E-5** : la nightly-2026-08-10 a été installée dans le rustup partagé de l'hôte (hors scratchpad), puis désinstallée après
  les mesures libFuzzer ; cargo-afl, cargo-fuzz et AFL++ sont restés sous le dossier du lot.
- **E-6** : redémarrage du conteneur vers 22:55 UTC ; aucun processus du lot en vol ; reprise consignée aux NOTES.

## 8. Journal de provenance (G1)

### 8.1 Sources

[lu] : BRIEF-FUZZ.md (entier) ; annexe A l.55-62 ; ADR-0028 l.225-242 ; annexe B l.28, l.143, l.798-835 (B.51), l.920-933
(B.56), l.1390-1400 et l.1475-1509 (B.87), l.1548-1560 (B.91), recherches des noms d'items ; docs/13 titres, l.180-215,
l.195 entière ; JOURNAL l.122 et l.143 (passages FUZZ) et recherche « fuzz » ; ETAT-REGISTRE-2026-10-04 l.1-12 et lignes
« fuzz » ; PASSATION-CLOUD l.145-160, l.255-265 ; DEVOPS l.70-100 ; R-8-outillage l.20-30, l.61-80, l.145-175 ; G1 d'E1
l.105-125 ; fuzz/README.md, README du corpus, fuzz.yml, fuzz/Cargo.toml, fuzz/.gitignore, fuzz/.gitattributes, cibles afl et
libFuzzer (entiers) ; `.gitattributes` (corpus) ; xtask : main.rs, fuzz.rs, lib.rs, rapport.rs (entiers), sg9.rs (l.1-80,
196-300, 340-420, 486-512), mutation.rs (l.1-60), tests/mutants.rs (l.1-80, 921-1104), reproductible.rs (l.318-330) ;
vérificateur lib.rs l.1-240, constat.rs l.355-758 ; cœur : erreur.rs, subject.rs l.180-641, temoignage_canonique.rs
l.120-215, lot.rs, verification.rs l.281-341 ; enforcement/journaux-modele.py l.1-60 ; gates.yml l.1-120 et commandes des jobs.
[abs] : aucune. [2nd] : aucune ; la lecture de « M-13 » est [inféré] (Q-5).

### 8.2 Commandes (sorties principales ; journaux complets dans `journaux/`)

`cargo install cargo-afl --version =0.18.2 --locked --root $S/outils` ; `cargo afl config --build` ; `cargo afl build
--release --locked --manifest-path fuzz/afl/Cargo.toml` ; `rustup toolchain install nightly-2026-08-10 --profile minimal` ;
`cargo install cargo-fuzz --version =0.13.2 --locked` ; `cargo +nightly-2026-08-10 metadata --locked` puis `fuzz build` ;
campagnes `cargo afl fuzz -V 660` et `cargo fuzz run … -max_total_time=660 -seed=20261009 -print_final_stats=1` (détachées,
PID 13385 et 16572) ; `cargo afl showmap -C` (cartes) et `-i … -o <dossier>` (cartes par graine) ; scripts du lot (sha256 au
`SHA256SUMS`) ; `cargo --locked xtask verify`, `cargo --locked test -p xtask`, jobs de `gates.yml`, sous
`scripts/isole_propre.sh` (unshare -n, env -i).

### 8.3 Chiffres recomptés

1339, 2413, 2084 : lignes des cartes (`wc -l`) = « Captured N tuples » d'afl-showmap ; 1074, 745, 719, 26, 0 : recomptés par
`scripts/comparer.py` et par la gate elle-même (745, perdues 0) ; 642 : calcul à la main (§2.1) et test
`seuil_de_la_gate_642_aretes` ; 108 graines = 29 + 15 + 18 + 12 + 26 + 6 + 2 ; 124 = 16 + 108 ; octets des graines par
`wc -c`.

## 9. Fichiers rendus

`diffs/FZ-a.diff` à `FZ-d.diff`, `FZ-e.diff`, `FZ-x.diff` ; `SHA256SUMS` ; `NOTES.md` ; ce rapport ; `pieces/` (hors dépôt,
avec son `SHA256SUMS`) ; `journaux/`, `mutants/` (résultats), `scripts/`.

## 10. Ajout daté du 2026-10-09 23:42:31 UTC (`date -u`) — phase 2 : C-1, C-2, C-3, L-3, FZ-e

Pièce suivie : `ADJUDICATION.md` (adjudication de 23:22:28 et ajout daté de 23:26:57, sha256 `c4b75ed7…` relevé à 23:27:18).
Base relue par `git log -1` au début (23:22:41) et à la fin (23:42:11) : `094fa5d3d5debe9dd466e37feee95200ca460dcf`, dépôt
propre. Le seuil n'a pas changé de règle : fraction 471/789 de E, 642 pour E = 1074 au binaire de `c1122de` (Q-2 adjugé).

### 10.1 Série finale et ordre d'application

| diff | contenu | lignes (hors graines) | sha256 |
|---|---|---|---|
| FZ-a, FZ-b, FZ-c, FZ-d | inchangés (§2.3) | +162/−1, +147/−3, +196/−1, +68/0 | `b596b015…`, `6fe46fcd…`, `221a8921…`, `ed7eba72…` |
| **FZ-f** (neuf) | gate à E recalculé : `seuil(E)`, mesure comparée = arêtes gagnées dans E, E vide ROUGE, trois cartes ; sous-commande à trois arguments ; tests ; pas CI (contrôle sha256 de l'archive versée, extraction, trois cartes) ; README du corpus (mesure comparée, règle L-3, O-1) ; `fuzz/README.md` (rejeu) ; ligne de DEVOPS §3 | +126/−66 | `c968fb3a…` |
| **FZ-e** (révisé, après FZ-f) | docs/13 §7 dette 3 fermée : E recalculé depuis le dérivé versé, seuil ⌈E × 471/789⌉, redistiller sans abaisser, O-1 | +1/−1 | `164f5919…` |
| **FZ-x** (révisé, C-1) | `xtask/tests/commun/mod.rs` (arbre temporaire unique, effacé au `Drop`) ; aides de `mutants.rs`, `reproductible.rs`, `distillation.rs` migrées ; `xtask/tests/arbres.rs` (3 tests) | +137/−19 | `42abcf13…` |

Ordre : a, b, c, d, f, e, x (contrôlé : série appliquée par `git apply` sur `git archive 094fa5d` = arbre final à l'octet).
Les premières versions de FZ-e et de FZ-x sont remplacées (`diffs/remplaces/FZ-e-v1.diff`, `FZ-x-v1.diff`). **Ordre de
versement** : les pièces de §10.2 doivent être au dépôt au plus tard avec FZ-f, sinon le pas CI rougit (échec fermé : archive
absente, code 1).

### 10.2 C-2 : versement préparé (rien écrit au dépôt) et E recalculé en CI

Dossier préparé : `<scratchpad>/s2bis/fuzz/versement/docs/adr-0028/revue-fuzz/pieces/`, forme de B.91 (`SHA256SUMS` du dossier
régénéré sur les pièces seules, LF, deux espaces, sans `./`) :

| fichier | octets | lignes | sha256 |
|---|---|---|---|
| `corpus-derive-2026-10-09.tar.gz` (2353 graines `derive/<16 hex>.bin` et `derive.MANIFESTE.tsv`) | 275 684 | binaire | `cbc2ab113d1ab5965cbe60f28caa24944d561d483294457318760c1ea9ba59dd` |
| `carte-base-c1122de.carte` | 12 387 | 1339 | `f07880331dd56a7ba06cd0056068aa92ec521016c8a684b0a2dd7dc18a9892ca` |
| `carte-base-plus-derive-c1122de.carte` | 22 762 | 2413 | `ed22484981abe26eb255101bad985050ecc1754b8d4e473e0b924ec744741e54` |
| `carte-corpus-distille-c1122de.carte` | 19 251 | 2084 | `1cd865f8da1a9bd0c9cbe561084266d7f72103ea04afc1683feab39df48eb889` |
| `SHA256SUMS` (les quatre lignes ci-dessus) | 394 | 4 | voir `SHA256SUMS` du lot |

Budget mesuré : `afl-showmap -C` sur le dérivé, 2,47 / 2,42 / 2,39 s (carte identique aux trois essais, 2410 arêtes) ;
extraction 0,10 s : **C-2 tenu**, d'où **C-3** : la gate dérive le seuil de l'E mesuré. Le job `cargo-afl` contrôle la somme de
l'archive contre le `SHA256SUMS` versé, l'extrait, mesure trois cartes sur le binaire du job et appelle
`cargo xtask fuzz-distillation <sans distillées> <corpus> <dérivé>`.

- Tests d'abord, rouge puis vert : étape intermédiaire « signatures neuves, logique ancienne » (E figé à 1074, toutes les
  arêtes gagnées comptées ; `journaux/rouge-f-distillation.rs.txt`) → 2 tests FAILED (gate, commande) ; code réel → 6/6.
- Rejeu local du pas tel qu'écrit, pièces posées au chemin du versement : le pas de FZ-d sur le code de FZ-f rend 64 (rouge
  d'avant) ; avec FZ-f : corpus complet **VERT** (« E, apport du corpus dérivé : 1074 » ; « arêtes gagnées : 745, dont dans E :
  719 ; seuil 642 = ⌈1074 × 471/789⌉ ») ; sans les 26 constats ROUGE (601 < 642) ; graines renommées, sans graines distillées,
  archive absente, archive altérée, archive substituée (valide, 20 graines) : code 1.
- Mutants : code 12/12 tués (F1 à F12 : division entière, garde de E vide, gains hors E comptés, E pris pour tout le dérivé,
  base perdue ignorée, `>`, cartes permutées, dérivé ignoré, argument en trop accepté, usage rendu 1, filtre inversé) ; pas CI
  9/9 tués (G1 à G9) ; G1 (contrôle de somme retiré) et G7 (`|| true`) ne sont tués que par l'archive substituée, qui sans
  contrôle donnait un **faux VERT** : le contrôle de somme porte la gate.
- L-2 disparaît (la gate compare désormais les arêtes gagnées **dans E**) ; L-1 est périmée (adjudication) ; L-3 est écrite au
  README du corpus (« redistiller, jamais abaisser le seuil »), qui nomme aussi la mesure comparée et porte O-1 (chiffres et
  motif, sans second seuil, Q-7 : aucun item).

### 10.3 C-1 : SHOGEN-XTASK-TMP-NOMS-FIXES-1 (FZ-x révisé)

Tous les noms fixes des tests de `xtask` sont repris : `shogen-mutant-*`, `shogen-mutant-doc-*`, `shogen-mutant-sg9-*`
(`mutants.rs`), `shogen-d6-*` (`reproductible.rs`), `distillation-corpus` et `distillation-cartes` (`distillation.rs`, ajoutés
par FZ-a et FZ-c). Un `Arbre` porte un nom `<préfixe>-<cas>-<processus>-<rang>` sous `CARGO_TARGET_TMPDIR`, s'efface au `Drop`
(panique comprise), et vide d'abord un reste laissé par un processus tué.

- Rouge puis vert : `aucun_test_ne_compose_de_chemin_temporaire_a_la_main` (balayage de `xtask/tests/*.rs`) FAILED avant la
  migration (`mutants.rs : temp_dir() hors de commun::Arbre`), vert après.
- **Témoin** (`scripts/temoin_simultane.sh`) : deux `cargo --locked test -p xtask` simultanés sur deux copies (cibles distinctes,
  même `TMPDIR`), réseau coupé. Avant FZ-x, 3 essais sur 3 avec collision (une exécution rouge à chaque essai : 2, 11, puis 2 et
  10 lignes FAILED) et 81 à 85 dossiers laissés dans le `TMPDIR` commun, plus 4 sous les cibles. Après FZ-x, 3 essais sur 3 :
  deux exécutions vertes (7 résultats chacune), **0 dossier laissé** dans le `TMPDIR` commun comme sous les cibles.
- Mutants : 9/9 tués sur la suite entière (X1 `Drop` vide, X2 rang retiré, X3 processus retiré, X4 racine `temp_dir()`, X5 reste
  gardé, X6 effacement non récursif, X7 à X9 chemins composés à la main dans `mutants.rs`, `distillation.rs`, `reproductible.rs`).

### 10.4 Contrôles de la série finale

- `cargo --locked xtask verify` (isolé) : VERDICT GLOBAL VERT après FZ-f, FZ-e et FZ-x ; `cargo --locked test -p xtask` : vert
  (après FZ-x : arbres 3, distillation 6, mutants 81, reproductible 9).
- Jobs de `gates.yml` sur clone patché (série et pièces posées, sans commit) : hooks 54, lint 227, secrets 147, arbre 1239
  fichiers, historique 738 commits, runner 137, suites 415, 341, 279, 65, 26 : verts ; `docs-sha256sums.py` conforme (35
  `SHA256SUMS`, 299 lignes, le dossier de pièces compris) ; ligne Modèle et lint conformes ; aucun TODO/FIXME ; `fuzz.yml`
  lisible en YAML (11 pas au job `cargo-afl`).
- `cargo xtask fuzz` : non rejoué, ni le générateur ni le corpus ni le harnais n'ayant changé depuis la course de 900 s (§2.6).

### 10.5 Écarts de la phase 2

- **E-7** : le rouge de FZ-f est pris sur une étape intermédiaire construite pour lui (signatures neuves, logique ancienne),
  jamais livrée.
- **E-8** : disque de l'hôte à 98 % pendant la phase (993 Mo libres à 23:33) : copies et cibles reconstructibles supprimées au
  fil de l'eau ; les arbres d'étape gardés sont `travail/fz`, `etape-f`, `etape-e2`, `etape-x2`.

## 11. Ajout daté du 2026-10-10 00:51:55 UTC (`date -u`) — G-4 : portée du contrôle des secrets de l'arbre (corrige §2.6 et §10.4)

Ce que disaient §2.6 (« secrets de l'arbre OK (1232 fichiers) ») et §10.4 (« arbre 1239 fichiers ») a été obtenu sur un
clone où les fichiers neufs de la série étaient posés en `git add -N` et les fichiers modifiés laissés hors de l'index. Or
`enforcement/gate-secrets.sh --tree` balaie l'**index** : liste par `git ls-files` (l.165), entrée lue à l'étage 0
(`:0:<chemin>`, l.18 de l'en-tête) [lu, dans le clone]. Une entrée `add -N` y est un blob vide (mesure du réviseur,
`g2/NOTES.md`, « `git show :0:<f>` rend 0 octet ») et un fichier modifié non indexé y garde sa version de `094fa5d`. Les
comptes étaient justes ; le **contenu** balayé était celui de la base, non celui de la série. Ces deux lignes n'attestaient
donc pas l'absence de forme d'identifiant dans les fichiers de la série.

Rejeu, index complet : clone de `094fa5d` (détaché), série a, b, c, d, f, e, x, g, h et pièces versées posées, **`git add -A`**
sans commit (117 ajouts, 10 modifications à l'index), pas « secrets des fichiers suivis » de `gates.yml` extrait et lancé tel
qu'écrit, isolé (00:46:53-00:47:13 UTC) : « OK (secrets) : 1239 fichier(s) sans forme d'identifiant dans la portée. » ;
historique : « OK (secrets) : historique, 740 commit(s) (--all) ». Même pas sur la tête du moment (`d78e51d`, §12.1) avec la
même série et les mêmes pièces (00:51:10-00:51:30) : 1240 fichiers, OK (le fichier de plus est
`s2-harness/tests/test_garde_reseau.py`, ajouté par DT5-2).

Écart de compte avec le réviseur (1 181) : sa copie est creuse, sans les dossiers interdits ni `*.jsonl` (`g2/NOTES.md` l.20,
[lu]) ; mes clones sont complets, comme l'extraction de la forge. L'écart de 58 tient à ces exclusions [inféré de sa note : je
ne recompte pas par motif les chemins interdits]. Les gates lisent ces fichiers sans rien en afficher (secrets : comptes
seuls ; `docs-sha256sums.py` : hors interdits par construction) ; je n'en ai ouvert aucun.

## 12. Ajout daté du 2026-10-10 00:54:16 UTC (`date -u`) — phase 3 : corrections de la G2 (FZ-g, FZ-h, G-5)

Pièces suivies : `ADJUDICATION.md` (ajout daté de 00:28:49, sha256 `770f4a2d…` relevé à 00:28:55), `g2/RAPPORT-G2.md`
(`a53ea545…`), `g2/C-G2.diff` (`15a4ffeb…`, 4 254 octets, relu en entier). Gate 0 inchangé : `claude-opus-5-5`.

### 12.1 Base, et tête avancée pendant la phase (écart E-9)

- `git log -1` à 00:31:34 : `094fa5d3d5debe9dd466e37feee95200ca460dcf`, `git status` vide. Pendant la phase, l'orchestrateur a
  committé DETTES-T5 : DT5-1 `3461ba8` (00:39:17 UTC), DT5-2 `d78e51d` (00:44:00), DT5-3 `30e1b9f` (00:48:52). Relevé à
  00:52:53 : tête `30e1b9f`, et `.github/workflows/gates.yml` indexé modifié dans le dépôt (travail en cours, non lu).
- Mes arbres d'étape restent bâtis sur `git archive 094fa5d` (base du brief) ; je n'ai avancé aucune base. Les trois commits
  DT5 ne touchent aucun des 122 fichiers de la série (`git diff --name-only 094fa5d 30e1b9f` croisé avec la liste des numstat) ;
  la série a..h s'applique sans échec sur `d78e51d` (clone) et sur `30e1b9f` (`git archive`). Les pas de `gates.yml` sont
  rejoués sur `094fa5d` et sur `d78e51d` (§12.6), pas sur `30e1b9f` (DT5-3 ne touche que l'installeur du crochet et ses cas).

### 12.2 Réponse sur `g2/C-G2.diff`

Lu en entier : quatre fichiers, corrections C-1 à C-3 de la G2 (G-1 à G-3), +24/−2. Les deux hunks de G-2 (`fuzz.yml`,
README) y figurent aussi : FZ-g prend les deux hunks de tests, FZ-h les deux autres.

| fichier | correction | repris dans | vérification |
|---|---|---|---|
| `xtask/tests/distillation.rs` (+12) | G-1 | FZ-g, à l'identique | Valeurs recomptées : `carte(5, 105)` = arêtes 5 à 109 ; E = 10 à 109, 100 arêtes ; seuil(100) = ⌈47 100/789⌉ = 60 ; gagnées dans E = 10 à 68, 59 : ROUGE attendu. Sous M5, 105 − 10 = 95 et ⌈44 745/789⌉ = 57, d'où `(95, 57)`. « mesure réelle : 3 arêtes de la base hors du dérivé » recompté sur les cartes d'un rejeu du pas (§12.4) : base ∖ dérivé = 3. Remarque de forme, sans correction (identité demandée) : « \|dérivé\| − \|base\| donnerait 57 » abrège « le seuil tiré de \|dérivé\| − \|base\| = 95 serait 57 ». |
| `xtask/tests/arbres.rs` (+4/−1) | G-3 | FZ-g, à l'identique | Le nom porte le processus : un occupant du nom fixe ne gêne plus (rouge puis vert, §12.3). Contrepartie, sans défaut : le reste laissé par un processus tué (`essai-reste-d-un-processus-tue-<pid>`) n'est plus vidé par l'exécution suivante ; même propriété que les arbres d'`Arbre::nouveau`, sous la cible cargo. |
| `.github/workflows/fuzz.yml` (+5/−1) | G-2 | FZ-h, à l'identique | Épingle = sha256 de l'archive versée (§10.2), une occurrence ; deux espaces ; chemin relatif à la racine comme `PIECES` ; `set -euo pipefail` rend l'échec fatal ; l'épingle précède l'extraction (contrôle avant emploi). Conséquence relevée : avec l'épingle, le contrôle par `SHA256SUMS` du pas ne départage plus aucun des 5 scénarios du réviseur (ses mutants S4 et S7 y survivent) ; un scénario ajouté, « sommes périmées » (archive intacte, ligne de `SHA256SUMS` fausse), les tue (§12.4). Contrôle gardé : il tient la cohérence des pièces versées, et une gate ne se desserre pas. |
| `crates/shogen-verifier/fuzz-corpus/README.md` (+3) | G-2 | FZ-h, **complété** (+6) | Les trois lignes de C-G2 reprises à l'identique ; la clause adjugée n'y figurait pas (« un dérivé remplacé ne peut plus abaisser le seuil ; la nouvelle épingle se pose par un lot qui redistille, jamais en même temps qu'un seuil plus bas ») : trois lignes ajoutées. |

Texte posé au README du corpus, après la règle L-3 :

> Le corpus dérivé fixe E, donc le seuil : son empreinte est épinglée dans le pas CI ; le remplacer est un changement de la
> gate (nouvelle mesure de référence datée, adjugée), jamais la réponse à un rouge. Un dérivé remplacé, même avec le
> `SHA256SUMS` du dossier à jour, fait échouer le pas et ne peut plus abaisser le seuil ; la nouvelle épingle se pose par un
> lot qui redistille, jamais en même temps qu'un seuil plus bas.

### 12.3 FZ-g (G-1, G-3) : rouges puis verts, mutants

- FZ-g = sections `arbres.rs` et `distillation.rs` de `C-G2.diff` **à l'octet**, lignes d'index comprises (`d6843d4..306c399`,
  `ca02b16..e900ebb`) ; +16/−1.
- G-3, rouge puis vert (`scripts/rouges_g.py`, copie dédiée, isolée, journaux `journaux/rouges-g/`) : fichier planté au nom
  fixe `essai-reste-d-un-processus-tue` sous `CARGO_TARGET_TMPDIR`. `arbres.rs` d'avant FZ-g : `arbre_sur_un_reste_le_vide_d_abord`
  FAILED (« reste posé: Os { code: 20, kind: NotADirectory, … } ») ; `arbres.rs` de FZ-g, fichier toujours planté : 3/3 ;
  sans fichier : 3/3.
- G-1, rouge puis vert : mutant M5 du réviseur (E par comptes) ; tests d'avant FZ-g : 6/6 (M5 vivant) ; tests de FZ-g :
  `apport_compte_en_ensemble_quand_le_derive_manque_des_aretes_de_la_base` FAILED, `left: (95, 57)`, `right: (100, 60)` ;
  sans mutant : 7/7. Copie restaurée et contrôlée à l'octet.
- Mutants (`scripts/mutants_g.py`, forme de `g2/outils/mutants_g2.py` ; témoin sans mutation vivant aux deux variantes ;
  construction en échec = non viable, 101 tué, 0 vivant, autre FATAL ; `mutants/resultats-g.tsv`) :

| mutant | après FZ-g | avant FZ-g (tests de x) | tué, après, par |
|---|---|---|---|
| M1 dénominateur + 1 (réviseur) | tué | tué | `seuil_471_sur_789_de_l_apport_du_derive` |
| M2 seuil des gagnées (réviseur) | tué | tué | test neuf, `gate_compte…`, `commande_rend…` |
| M3 tolérance d'une arête (réviseur) | tué | tué | test neuf, `gate_compte…`, `commande_rend…` |
| M4 E hors du corpus (réviseur) | tué | tué | test neuf, `gate_compte…`, `commande_rend…` |
| M5 E par comptes (réviseur) | **tué** | vivant | test neuf seul |
| M6 dérivé lu du corpus (réviseur) | tué | tué | `commande_rend…` |
| M7 E par différence symétrique (ajout) | **tué** | vivant | test neuf seul |
| M8 E plus les arêtes de la base hors du dérivé (ajout) | **tué** | vivant | test neuf seul |
| X1 rang figé (réviseur) | tué | tué | `arbre_unique…` |
| X8 `sur` sans vidage (ajout) | tué | tué | `arbre_sur_un_reste_le_vide_d_abord` |
| X9 nom sans processus (ajout) | tué | tué | `arbre_unique…` |
| X10 `Drop` sans effacement (ajout) | tué | tué | `arbre_unique…` |

Après FZ-g : 12/12 tués ; le test neuf tue seul M5, M7 et M8, que la suite d'avant laissait vivre.

### 12.4 FZ-h (G-2) : les 5 scénarios du réviseur rejoués, mutants du pas

- Pas « Distillation » extraits par PyYAML (`scripts/pas_ci_h.py` = `g2/outils/pas_ci_g2.py` à l'octet) : celui de FZ-g est le
  pas « final » du réviseur à l'octet (sha256 `8552209a…`), celui de FZ-h son pas « corrigé » à l'octet (`079f035c…`).
- Rejeu (`scripts/scenarios_ci_h.py` : scénarios du réviseur repris à l'identique, chemins adaptés, deux scénarios ajoutés et
  comptés à part ; pas lancé comme la forge, `bash --noprofile --norc -eo pipefail`, isolé ; binaire AFL construit dans la copie
  par la commande du pas « Construction ») ; code de sortie et cause relevée dans la sortie :

| scénario | avant (pas de FZ-g) | après (pas de FZ-h) |
|---|---|---|
| aucune | 0, VERT (E 1074, 745 gagnées dont 719 dans E, seuil 642) | 0, VERT (mêmes chiffres) |
| sans les 26 constats | 1, ROUGE (601 < 642) | 1, ROUGE |
| archive altérée (un octet) | 1 (somme) | 1 (épingle) |
| archive substituée (20 entrées du dérivé, sommes non mises à jour) | 1 (somme) | 1 (épingle) |
| **archive faible (les 82 autres graines distillées) + `SHA256SUMS` à jour + sans constats** | **0, VERT** (E 623, 623 dans E, seuil 372) | **1 (épingle)** : « docs/adr-0028/revue-fuzz/pieces/corpus-derive-2026-10-09.tar.gz: FAILED », avant toute carte |
| archive absente (ajout) | 1 (somme) | 1 (épingle) |
| sommes périmées (ajout) | 1 (somme) | 1 (somme) |

Le faux VERT relevé par la G2 est reproduit avant FZ-h et fermé après ; le pas échoue à l'épingle (code 1), la gate n'est pas
appelée.

- Mutants du pas de FZ-h (tué si un scénario rend une issue autre que l'attendue ; `mutants/resultats-ci-h.tsv`) :

| mutant | classement | départagé par |
|---|---|---|
| S4 somme neutralisée (réviseur) | tué par l'ajout seul | sommes périmées (0 au lieu de 1) |
| S7 somme d'un autre fichier (réviseur) | tué par l'ajout seul | sommes périmées (0) |
| SE1 dérivé remplacé par le corpus (réviseur) | tué | sans constats (0) |
| SE2 dérivé versé dans la base (réviseur) | tué | aucune (1) |
| H1 épingle retirée | tué | archive faible + sommes à jour (0) |
| H2 épingle neutralisée (`\|\| echo`) | tué | archive faible + sommes à jour (0) |
| H3 empreinte altérée d'un chiffre | tué | aucune (1) |
| H4 épingle portée sur une autre pièce (carte de base) | tué | archive faible + sommes à jour (0) |
| H5 épingle après l'extraction | vivant, **équivalent d'issue** : l'échec tombe avant les cartes, l'ordre n'est pas observable à l'issue ; l'épingle reste avant l'extraction (contrôle avant emploi) | — |
| H6 `--ignore-missing` | vivant, **équivalent d'issue** : archive présente et différente, échec identique ; absente, « no file was verified », code 1 | — |

8 tués (dont S4 et S7 par l'ajout seul), 2 équivalents d'issue justifiés.

- Recompte sur un rejeu du pas de FZ-h (cartes gardées : `journaux/cartes-rejeu-h/`) : base 1339 arêtes, corpus 2084, dérivé
  2410 ; E = dérivé ∖ base = 1074 ; base ∖ dérivé = 3 ; dérivé − base en comptes = 1071 (M5 y donnerait E 1071, seuil 640) ;
  745 gagnées dont 719 dans E ; 0 perdue ; VERT. Ces cartes diffèrent à l'octet des cartes versées (binaire recompilé :
  identifiants d'arêtes d'AFL différents) ; les comptes sont identiques. La gate juge sur le binaire du jour, comme prévu.

### 12.5 G-5 : la ligne à dater au versement (rien changé)

`docs/13-temoignage-e2e-design.md`, **ligne 195** de l'arbre final (l'unique ligne ajoutée par FZ-e ; tableau « # | dette |
propriétaire | échéance | verrous anti-perpétuel »), deux mentions :

1. colonne « dette », en tête : « **FERMÉE le 2026-10-09 (lot FUZZ, SHOGEN-FUZZ-DISTILLATION-1)** » ;
2. colonne « échéance » : « fermée (2026-10-09) ».

La troisième date de la ligne, « (adjudication du 2026-10-09) », est celle de l'adjudication de Q-2 (ajout daté de 23:26:57) :
elle reste. Les autres dates de la série sont des dates de mesure ou de lot, ou le nom de l'archive épinglée
(`corpus-derive-2026-10-09.tar.gz` : l'épingle, le `SHA256SUMS` et le pas en dépendent, il ne change pas).

### 12.6 Série finale et contrôles

| diff | contenu | lignes | sha256 |
|---|---|---|---|
| FZ-a, FZ-b, FZ-c, FZ-d, FZ-f, FZ-e, FZ-x | inchangés (§10.1) | — | `b596b015…`, `6fe46fcd…`, `221a8921…`, `ed7eba72…`, `c968fb3a…`, `164f5919…`, `42abcf13…` |
| **FZ-g** (G-1, G-3) | `xtask/tests/distillation.rs` (+12), `xtask/tests/arbres.rs` (+4/−1), à l'identique de `C-G2.diff` | +16/−1 | `d5ef74568242a07a280127d80530e74c80a091c981f1fe17a3bef7b8947aaf74` |
| **FZ-h** (G-2) | `.github/workflows/fuzz.yml` (+5/−1, à l'identique de `C-G2.diff`), README du corpus (+6) | +11/−1 | `40c00c69ebb50fb7d1fbcdb3ce4ceeabaad11a30a535e80daa2480b3f148a3fe` |

- Ordre : **a, b, c, d, f, e, x, g, h**. Série appliquée par `git apply` sur `git archive 094fa5d` = arbre final (etape-h) à
  l'octet. Empreinte de la série (concaténation dans l'ordre) : `0fe1972a99b7b9ea33cd0cb9d10868cd5401b90d5c2793b647ff82b78c79621c`
  (a..x inchangée : `24def280…`). FZ-g et FZ-h touchent des fichiers disjoints.
- `df -h /` avant compilation : 8,2 G libres (00:38:15), 7,4 G (00:44:25), 6,9 G (00:46:25).
- `cargo --locked xtask verify` (isolé, une cible par copie) : VERDICT GLOBAL VERT après FZ-g et après FZ-h (S-G1 à S-G9, fmt,
  no_std, clippy -D warnings ; copies complètes : la violation S-G9 de la G2 tenait à sa copie creuse). `cargo --locked test -p
  xtask` : arbres 3, distillation 7, mutants 81, reproductible 9, aux deux étapes.
- Pas `run` de `gates.yml` extraits par PyYAML et lancés tels qu'écrits (`scripts/jobs_gates_h.py`, coquilles de GitHub,
  isolés), sur un clone indexé `git add -A` sans commit : **base `094fa5d`** + série + pièces (00:46:25-00:50:41) et **tête
  `d78e51d`** + série + pièces (00:50:41-00:54:58). 15 scripts distincts par base, 30 lancements, tous code 0 : hooks 54 ;
  TODO/FIXME aucun ; cas du lint 227 ; R-1 OK (7 fichiers) ; ligne Modèle conforme ; `docs-sha256sums.py` conforme (35
  `SHA256SUMS`, 299 lignes, le dossier de pièces compris) ; cas des secrets 147 ; secrets de l'arbre 1239 (base) et 1240 (tête)
  fichiers OK ; historique 740 commits OK ; runner 137 ; s2-harness Ran 415 (base) et 418 (tête, plancher de DT5-2) ; s2bis
  341 ; sim-bis 279 ; calib-actifs 65 ; controle 26.
- `fuzz.yml` lisible en YAML (PyYAML) : 4 jobs, 11 pas au job `cargo-afl`.
- `cargo xtask fuzz` non rejoué : générateur, graines et harnais inchangés depuis la course de 900 s (§2.6) ; le README du
  corpus n'est pas une graine (`charger_corpus` saute les `*.md`, `xtask/src/fuzz.rs` l.585).

### 12.7 Écarts et questions de la phase 3

- **E-9** (base) : la tête a avancé pendant la phase (DETTES-T5 en cours) ; relevé à 00:55:33 : `22612507` (DT5-4, 00:53:42,
  `gates.yml` seul), et `gates.yml` de nouveau indexé modifié dans le dépôt. La série ne touche aucun fichier de DT5-1 à DT5-4 et
  s'applique sans échec sur `22612507` (`git archive`). Rendu à l'orchestrateur ; aucune base avancée.
- **E-10** (outil) : un premier lancement (copie de l'arbre de scénarios et construction AFL par un script `bash -c`) a été
  refusé par la garde de suppression du harnais (script `-c` jugé invérifiable ; il ne supprimait rien) ; rien n'a tourné. Relancé
  par un fichier de script d'une ligne (`scripts/construction_ci.sh`, la commande du pas « Construction »).
- **Q-8** : la clause du README reprend les mots de l'adjudication, « jamais en même temps qu'un seuil plus bas ». Le seuil
  absolu suit E (⌈E × 471/789⌉) : un lot qui redistille sur un dérivé plus petit l'abaisse mécaniquement. Je lis « seuil plus
  bas » comme la règle (fraction sous 471/789, ou nombre figé sous elle) ; si l'adjudication vise aussi le nombre (jamais sous
  642), la phrase est à serrer.
- **Q-9** : `docs/DEVOPS.md` l.91 (FZ-f) écrit « ajout daté du 2026-10-09 » : même règle que G-5 (date du versement) ou date
  d'écriture ?

### 12.8 Fichiers rendus (phase 3, sous `<scratchpad>/s2bis/fuzz/`)

- `diffs/FZ-g.diff`, `diffs/FZ-h.diff` (et `serie/FZ-g.numstat`, `serie/FZ-h.numstat`) ; résultats : `mutants/resultats-g.tsv`,
  `mutants/resultats-ci-h.tsv`.
- Scripts : `scripts/readme_h.py`, `rouges_g.py`, `mutants_g.py`, `mutants_g.sh`, `scenarios_ci_h.py`, `scenarios_h.sh`,
  `pas_ci_h.py`, `isole_ci_h.sh`, `construction_ci.sh`, `jobs_gates_h.py`, `jobs_gates_h.sh`.
- Journaux : `journaux/rouges-g/`, `journaux/mut-g/`, `journaux/scen-h/` (84 sorties), `journaux/scenarios-ci-h.tsv`,
  `journaux/gates-h-base/`, `journaux/gates-h-tete/`, `journaux/jobs-gates-h.txt`, `journaux/cartes-rejeu-h/`,
  `journaux/pas-distillation-g.sh`, `journaux/pas-distillation-h.sh`, `journaux/verify-etape-g.txt`, `journaux/test-etape-g.txt`,
  `journaux/verify-etape-h.txt`, `journaux/test-etape-h.txt`, `journaux/verifications-etapes.txt`.
- Copies supprimées en fin de phase (reconstructibles par `git archive 094fa5d` et la série) : voir `NOTES.md`.

## 13. Ajout daté du 2026-10-10 01:51:29 UTC (`date -u`) — phase 4 : R-1 à R-3 du contre-contrôle (FZ-i, FZ-j, FZ-k)

Pièces suivies : `ADJUDICATION.md` (ajouts datés de 00:58:24 et 01:41:06, sha256 `11f3d7ce…` relevé à 01:41:11),
`g2/cc/RAPPORT-CC.md` (`d1400fa2…`, lu en entier), `g2/cc/R-1.diff` (`54c7e8b7…`), `R-2.diff` (`07a4fe25…`), `R-3.diff`
(`ebfc4179…`), lus en entier. Gate 0 inchangé : `claude-opus-5-5`.

### 13.1 Base et tête

- `git log -1` : `d7e88045` (DT5-13) à 01:41:11, `ae7ffe33` (DT5-14) à 01:47:43, `87257b6` (DT5-15) à 01:51:29 ; index du
  dépôt modifié par l'orchestrateur (non lu). Mes arbres partent de `git archive 094fa5d` (base du brief) ; aucune base avancée.
  Les 14 commits DT5 jusqu'à `ae7ffe33` changent 16 fichiers, aucun des 122 de la série ; la série a..k s'applique sans échec
  sur `ae7ffe33` (clone, §13.4).

### 13.2 FZ-i, FZ-j, FZ-k : repris à l'identique ; ce que j'en réponds

FZ-i, FZ-j, FZ-k sont les copies à l'octet de R-1, R-2, R-3 (mêmes sha256). Ils s'appliquent dans l'ordre après FZ-h
(« Applied patch … cleanly » ×3), et les diffs régénérés depuis mes arbres (h → i → j → k) leur sont identiques à l'octet.

| diff | fichier, lignes | réponse |
|---|---|---|
| **FZ-i** = R-1 | `xtask/tests/reproductible.rs`, +5/−1 | **Juste, et nécessaire** : le défaut vient de mon FZ-x. `racine_du_cas` pose l'arbre jouet sous `CARGO_TARGET_TMPDIR` ; avec la cible par défaut, c'est `<dépôt>/target/tmp`, donc sous la racine du workspace du dépôt. `generer_lockfile` lance `cargo generate-lockfile --offline` dans le jouet ; cargo remonte, trouve le `[workspace]` du dépôt, dont le jouet n'est pas membre, et refuse (« current package believes it's in a workspace when it's not », mesuré). Avant FZ-x, le jouet vivait sous `temp_dir()`, hors du dépôt. Mes rejeux (phases 1 à 3) posaient `CARGO_TARGET_DIR` hors de la copie : le défaut n'y paraissait pas (§13.3). La table `[workspace]` vide fait du jouet sa propre racine, où que soit la cible ; c'est plus local qu'un `exclude` au manifeste du dépôt. Le commentaire est exact et ne nomme pas la variable de la cible (le garde lexical d'`arbres.rs` reste vert). Limite : la jambe Windows de `squelette.yml` n'est pas mesurée ici (hôte Linux) ; la correction ne dépend pas du système [inféré]. |
| **FZ-j** = R-2 | README du corpus, +9/−7 | **Juste** : dit Q-8 sans ambiguïté (la fraction ne baisse jamais ; le nombre suit E, sans plancher, 642 n'en est pas un ; épingle nouvelle par un lot revu (G2), daté, qui écrit l'ancien et le nouvel E, le binaire mesuré et la raison). Il retire les deux phrases qui se lisaient comme un plancher, dont la mienne (« jamais en même temps qu'un seuil plus bas »). Remarque, sans correction : « Le corpus dérivé fixe E » est vrai à base fixée ; E = dérivé ∖ base bouge aussi si la base grossit, sans faille (O-1 du contre-contrôle). |
| **FZ-k** = R-3 | `docs/13` l.195, +1/−1 | **Juste** : « nombre qui suit E ; redistiller, jamais abaisser la fraction 471/789 ; épingle du dérivé changée par un lot revu (G2) seulement, qui écrit l'ancien et le nouvel E ». Plus bref que le README (binaire et raison n'y sont pas) : le README porte la règle entière. Compatible avec G-5 (§13.5). |

### 13.3 R-1 rejoué : cible cargo par défaut de la copie, sans `CARGO_TARGET_DIR`, avant et après FZ-i

Copie `git archive 094fa5d` + série, isolée (`unshare -n`, `env -i`) ; `scripts/rejeu_r1.sh`, journaux `journaux/r1/`. Les
deux commandes : `cargo --locked test -p xtask`, puis celle du pas « Tests » de `squelette.yml`,
`cargo test --locked --workspace -- --nocapture`.

| état | cible | `test -p xtask` | `test --workspace` (forge) |
|---|---|---|---|
| après FZ-h | **par défaut** (`<copie>/target`) | **rc 101** : reproductible 5 passed, **4 FAILED** | **rc 101**, mêmes 4 |
| après FZ-h | hors de la copie (configuration de mes rejeux antérieurs) | rc 0, reproductible 9/9 | rc 0, 9/9 |
| après FZ-i | par défaut | **rc 0**, reproductible 9/9 | **rc 0**, 28 bilans ok |
| après FZ-k (final) | par défaut | rc 0 : arbres 3, distillation 7, mutants 81, reproductible 9 | rc 0, 28 bilans ok |

Les 4 tests rouges : `mutant_construction_en_echec_ne_rend_aucun_verdict`,
`mutant_base_dans_l_arbre_source_est_refusee_avant_toute_suppression`, `temoin_double_build_sans_injection_reste_identique`,
`mutant_double_build_attrape_un_horodatage_incorpore` ; motif : « error: current package believes it's in a workspace when it's
not ». Aucun dossier laissé sous `<copie>/target/tmp` après les courses.

Mutants du manifeste du jouet (`scripts/mutants_i.py`, `mutants/resultats-i.tsv`), jugés aux deux cibles ; témoin vivant aux
deux :

| mutant | cible par défaut | cible hors copie |
|---|---|---|
| I1 table `[workspace]` retirée (état d'avant FZ-i) | tué (4 FAILED) | vivant |
| I2 `[workspaces]` (faute de nom) | tué (4) | vivant |
| I3 `[package.metadata.workspace]` | tué (4) | vivant |
| I4 autre table vide (`[patch.crates-io]`) | tué (4) | vivant |
| I5 `members = ["."]` | vivant, équivalent : une table workspace reste | vivant |
| I6 `exclude = []` | vivant, équivalent | vivant |
| I7 `[workspace.metadata]` (crée la table workspace) | vivant, équivalent | vivant |
| I8 `resolver = "2"` | vivant, équivalent | vivant |

Les 4 mutants qui ôtent la racine propre du jouet ne meurent qu'à la cible par défaut. Cela confirme la règle adoptée avec
I-1 : un rejeu de `cargo test` comprend au moins une course à la cible par défaut de la copie.

### 13.4 Gates complètes de la série a..k

Toutes les courses sont isolées (`unshare -n`, `env -i`, `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée) et à la **cible cargo par
défaut** de la copie. `df -h /` avant compilation : 7,7 G libres (01:44:02), 6,7 G (01:45:43), 6,3 G (01:48:07), 5,6 G
(01:49:19), 5,4 G (01:49:49).

- `cargo --locked xtask verify`, arbre final : VERDICT GLOBAL VERT (S-G1 à S-G9, fmt, no_std, clippy -D warnings).
- Job `squelette` de `squelette.yml` (jambe Linux ; pas `run` extraits par PyYAML et lancés tels qu'écrits,
  `scripts/squelette_h.py`), sur deux clones indexés `git add -A` sans commit, série a..k et pièces posées : **base `094fa5d`**
  et **tête `ae7ffe33`**.
  - Pas lancés et rendus à 0 aux deux bases : lockfile intact ; `cargo build --locked --workspace --all-targets` ;
    vérificateur sans features ; **`cargo test --locked --workspace -- --nocapture`** (25 binaires, 28 bilans ok,
    reproductible 9/9, 0 FAILED) ; `cargo run … verify` (VERT) ; squelette bout-en-bout (« lot muté refusé, fail-closed
    tenu ») ; `cargo deny --locked --offline check` (« advisories ok, bans ok, licenses ok, sources ok », 4 avertissements
    `license-not-encountered`).
  - Pas sautés (réseau) : « Toolchain épinglée » (rustup ; la chaîne 1.97.1 est installée) et « Outil S-G7 »
    (`cargo install` ; cargo-deny 0.20.2 installé). Le pas S-G7 tourne en variante `--offline`, sur la base d'avis locale,
    non rafraîchie : écart de forme, écrit.
- Pas `run` de `gates.yml`, sur les mêmes clones (`scripts/jobs_gates_h.py`) :
  - **base**, 15 scripts distincts, tous code 0 (01:48:07-01:52:37) : hooks 54, TODO/FIXME aucun, cas du lint 227, R-1 OK, ligne Modèle
    conforme, `docs-sha256sums.py` conforme (35 `SHA256SUMS`, 299 lignes), cas des secrets 147, arbre 1239 fichiers,
    historique 752 commits (`--all`), runner 137, s2-harness 415, s2bis 341, sim-bis 279, calib-actifs 65, controle 26.
  - **tête**, 18 scripts distincts : hooks 57, environnement de l'image, runners-epingles conforme (7 workflows),
    workflows-yaml conforme (7 workflows), cas du lint 227, R-1 OK, ligne Modèle, `docs-sha256sums.py` 35/299, secrets 147,
    arbre 1243, historique 752, runner 137, s2-harness 418, s2bis 341, sim-bis 279, calib-actifs 65, controle 36 : les 18
    rendus à 0 (01:50:30-01:55:01).
- Pas « Distillation » de `fuzz.yml` à l'arbre final (pas identique à l'octet à celui de FZ-h, `079f035c…`), binaire AFL construit
  par le pas « Construction » dans la copie, 7 scénarios (`scripts/scenarios_ci_h.py`) : témoin conforme. Aucune
  altération : VERT (E 1074, 745 gagnées dont 719 dans E, seuil 642). Sans constats : ROUGE (601). Archive faible avec
  `SHA256SUMS` à jour : échec à l'épingle. Les quatre autres : code 1.
- `cargo xtask fuzz` non rejoué : générateur, graines et harnais inchangés ; FZ-j ne touche que le README, qui n'est pas une
  graine (`charger_corpus` saute les `*.md`).

### 13.5 G-5 après FZ-k

`docs/13-temoignage-e2e-design.md` : toujours la **ligne 195**, deux mentions à dater au versement : « **FERMÉE le 2026-10-09
(lot FUZZ, SHOGEN-FUZZ-DISTILLATION-1)** » (colonne « dette ») et « fermée (2026-10-09) » (colonne « échéance »). La troisième
date, « (adjudication du 2026-10-09) », reste. FZ-k touche la même ligne, sans toucher ces mentions.

### 13.6 Série finale

| diff | contenu | lignes | sha256 |
|---|---|---|---|
| FZ-a à FZ-h | inchangés (§10.1, §12.6) | — | `b596b015…`, `6fe46fcd…`, `221a8921…`, `ed7eba72…`, `c968fb3a…`, `164f5919…`, `42abcf13…`, `d5ef7456…`, `40c00c69…` |
| **FZ-i** (R-1) | `[workspace]` vide au manifeste du jouet, et un commentaire | +5/−1 | `54c7e8b709323200bedc735620fae1b89b1884913843b3f21ad5fefc07cd51b4` |
| **FZ-j** (R-2) | README du corpus : règle Q-8 | +9/−7 | `07a4fe25be0ca3cec78733216d03cb3aec7cb59ad546536797905d1544263dbc` |
| **FZ-k** (R-3) | `docs/13` l.195 : règle Q-8 | +1/−1 | `ebfc4179106bcd087092d16f9fc2f7ba9f17c030c5a0eb1b903dbd0f6a508ec4` |

- Ordre : **a, b, c, d, f, e, x, g, h, i, j, k**. Empreinte de la série (concaténation dans l'ordre) :
  `3003589dac9a42ff5af46cf1f13ebc2afe30f4fa8076536f65611b4afe73b6cf` ; a..h inchangée (`0fe1972a…`). Appliquée sur
  `git archive 094fa5d`, elle redonne l'arbre final à l'octet. Elle s'applique aussi sans échec sur `ae7ffe33` (clone) et sur
  `e8825318` (DT5-16, tête à 01:55:20, `git archive`) ; de `094fa5d` à `e8825318`, 16 fichiers changent, aucun dans la série.
- R-25 : FZ-i +5/−1, FZ-j +9/−7, FZ-k +1/−1 ; aucune dépendance neuve (R-8) ; aucun marqueur nu (job g5 aux deux bases).

### 13.7 Écarts, item à former

- **E-11** (consigne) : pour nommer la source de restes dans le `TMPDIR`, j'ai lancé
  `grep -rn 'shogen-canonique' <copie>/crates --include=*.rs`, une recherche récursive sur une copie du dépôt dans le scratchpad.
  C'est contraire à la lettre de la consigne. Portée : `*.rs` de `crates/`, où ne vit aucune pièce de D.2 ; sortie limitée à 5
  lignes ; pas répété.
- **E-12** (outil) : première variante hors réseau du pas S-G7 en `--disable-fetch`, refusée par cargo-deny 0.20.2 (code 2,
  « unexpected argument ») ; relancée en `--offline`. Premier essai gardé : `journaux/squelette-k-base-essai1*`.
- **E-13** (outil) : le PID de `setsid nohup … &`, sondé par `kill -0`, s'est dit fini alors que la course continuait. Les
  résultats ont été lus après le bilan écrit en fin de course, aucun ne s'en trouve faussé. Depuis, je sonde une ligne de fin
  dans le journal (`scripts/gates_k.sh`).
- **Item à former** (règle PAROXYSME ; nom proposé **SHOGEN-VERIFIER-TESTS-TMP-RESTES-1**) : chaque
  `cargo test --workspace` laisse 34 dossiers `shogen-{canonique,coquille,e2e,reel}-*-<pid>` dans le `TMPDIR`. Ils viennent
  des tests d'intégration de `shogen-verifier`, qui posent leurs arbres sous `temp_dir()` sans les effacer (source lue pour
  `canonique` : `crates/shogen-verifier/tests/temoignage_canonique.rs` l.181 ; les trois autres préfixes [inférés des noms des
  binaires]). Mesuré : 238 dossiers après 7 courses = 34 × 7. Le défaut est préexistant et hors de la série (FZ-x ne couvrait
  que `xtask/tests`) ; le nom porte le processus, donc pas de collision, mais les restes s'accumulent hors de la forge.
  Remède de même forme que FZ-x (arbre unique effacé au `Drop`), par un lot.
- Limites : jambe Windows de `squelette.yml` non mesurée (hôte Linux) ; avis de cargo-deny lus dans la base locale, sans
  rafraîchissement (pas de réseau).

### 13.8 Fichiers rendus (phase 4, sous `<scratchpad>/s2bis/fuzz/`)

- `diffs/FZ-i.diff`, `diffs/FZ-j.diff`, `diffs/FZ-k.diff` (et `serie/FZ-i.numstat`, `FZ-j.numstat`, `FZ-k.numstat`) ;
  `mutants/resultats-i.tsv`.
- Scripts : `scripts/rejeu_r1.sh`, `mutants_i.py`, `squelette_h.py`, `gates_k.sh`.
- Journaux : `journaux/r1/` (bilan et sorties), `journaux/mut-i/`, `journaux/squelette-k-base/`, `journaux/squelette-k-tete/`,
  `journaux/gates-h-k-base/`, `journaux/gates-h-k-tete/`, `journaux/jobs-gates-k-base.txt`, `journaux/jobs-gates-k-tete.txt`,
  `journaux/verify-k-defaut.txt`, `journaux/scen-h/final-*`, `journaux/fichiers-serie.txt`.
- Copies, cibles cargo et `RUNNER_TEMP` supprimés en fin de phase (reconstructibles par `git archive 094fa5d` et la série).
