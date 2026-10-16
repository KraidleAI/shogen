# Relecture G2 neuve de DETTES-T7 (C-1 à C-8) (transcrit)

> Transcription par l'orchestrateur le 2026-10-16 07:19:00 UTC du fichier dettes7/g2/RAPPORT-G2.md ; contrôle FM-1.1 des transcripts du générateur, du réviseur G2 et du contre-contrôleur, par le fm11.py versé et par celui de DT3-E : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Relecture G2 neuve du lot DETTES-T7 (série DT7-a à DT7-k)

- **Modèle** : `claude-opus-5-5` (Gate 0 : identifiant exact donné par l'environnement ; effort `max` demandé par le
  brief, non observable de l'intérieur). Réviseur neuf : je n'ai ni écrit ni relu ce lot.
- Heures (`date -u`) : début 2026-10-10 06:45:10 UTC ; rédaction de ce rapport 08:10:14 UTC ; fin : section 10.
- Brief : `g2/BRIEF-G2.md`, lu en entier ; pièces lues en entier : `ADJUDICATION.md` (avec l'ajout de 06:44:18),
  `RAPPORT-GENERATEUR.md` (phases 1 et 2), `BRIEF-DETTES-T7.md`, `ITEMS-ANNEXE-B.md`.
- Série : 14 diffs dans l'ordre a, b, c1, c2, c3, c4, d, e, f, g, h, i, j, k ; empreinte de la concaténation
  `687d68e0a21f5bad5058ace8ce3c22bcd1d2cdd7cbae2448a0a9f2d0a4617704` (recalculée : égale au préfixe du brief).
- Base relue : `622eede75f54f1b51c9218d04ec50668232c950d` (tête de `claude/compassionate-noether-szmdyj` à 06:45) ;
  copie neuve `g2/tmp/copie` (clone sans liens durs, sparse non-cone sans les emplacements interdits ni `*.jsonl`,
  `git sparse-checkout list` relu), série appliquée 14 sur 14 (`git apply --check` puis `git apply`). Tête relue en
  fin de passe : voir section 10.

## Verdict : ACCEPTE-AVEC-CORRECTIONS, liste fermée C-1 à C-8

Le lot tient l'essentiel de ce qu'il annonce : toutes les étapes `run:` de `gates.yml` (g3 `--history` excepté), la
matrice, `cargo test` et `xtask` sont verts sur la série ; 25 mutants du réviseur sur 25 sont tués par la commande
du job ; les sondes versées sont les octets de la forge. Mais quatre phrases de fermeture sont fausses sur le code
pour des cas mesurés (MUTANTS-ORPHELINS-1 ; S2BIS-MUT-COMMANDE-1 pour l'outil ; ENREG-DELAI-ARBRE-1 ;
ENREG-EXTRACTION-INTERDITS-1 pour un lien), et des textes du lot sont inexacts ou réécrits sans date. Les huit corrections sont éprouvées sur la série (fichiers `corrections/C-n.diff`, appliqués dans
l'ordre après DT7-k, sur `622eede`, `d3d897b` et la tête de fin `1b8a44d`).

| C-n | diff visé | objet | +/− (dont `.py`) | sha256 |
|---|---|---|---|---|
| C-1 | DT7-f (et DT7-a) | `mutants.py` : à la borne, groupes de tous les descendants (relevé `ps` par parenté) arrêtés et comptés au relevé ; sortie lue `RELIQUAT` s ; checkout exigé en tête ; étapes relues sur la copie mutée ; tests M6, M7, M8, `tete` ; README ; puce datée de la fiche | +97 −17 (81) | `4cb0458f…ce8f` |
| C-2 | DT7-d | `lancer` de l'enregistreur : après l'arrêt de l'arbre au délai, sortie lue `RELIQUAT` s au plus ; test étendu (descendant détaché) ; README | +39 −8 (32) | `9c2c7e1c…2cbf` |
| C-3 | DT7-b | `extraire` : lien vers le dossier interdit lui-même exclu ; test étendu ; README (limite à deux sauts) | +19 −8 (13) | `a638444e…bfb5` |
| C-4 | DT7-e | README de l'outil : Q-3 et Q-5 adjugées ; ordre `champs` puis `ancien outil` | +5 −0 | `3a1e0ce5…eb1b` |
| C-5 | point ouvert | `enforcement/lint-model-pinning.sh` l.8 : `l.23-49` devient `l.23-55`, même longueur | +1 −1 | `78934920…56bc` |
| C-6 | DT7-a | puce d'errata datée : renvoi au G0 de PLAN-S2BIS l.18-22 ; trois causes sous 3.10 | +5 −0 | `a38b82e0…ddfd` |
| C-7 | DT7-b | ADR-0028, ajout daté en fin de document : `tree.exclus` au schéma v1 ratifié | +8 −0 | `aed93cce…8a1d` |
| C-8 | DT7-i | fiche `shogen-extracteur` : description et règle 6 rendues à leur texte validé, rôle ajouté par phrases datées ; règle 7 datée après l'adjudication | +19 −17 | `3407279d…8912` |

Sommes complètes : `SHA256SUMS` de ce dossier. Aucune ligne ajoutée de plus de 120 caractères, aucune barre oblique
inverse ajoutée, aucun `TODO`/`FIXME` (contrôle par script sur les octets des diffs). Planchers inchangés (S2 423,
runner 152, controle 39) : les tests neufs étendent des tests existants.

## 1. Items : phrases de fermeture proposées par le générateur

| item | verdict sur la phrase | phrase à retenir si elle change |
|---|---|---|
| HARNAIS-CIBLE-PARTAGEE-1 ; règle I-1 | vraie (DT7-a ; appliquée ici : `cargo test` à la cible par défaut de la copie) | — |
| FICHE-WORKER-POSTEXEC-2 | vraie sur le fond ; renvoi inexact (`l.18-21` : l'épinglage finit l.22 du G0 `docs/adr-0029/G0-lot-PLAN-S2BIS.md`) | fermé par DT7-a et C-6 |
| WORKER-TMPDIR-1, COMPACTION-TRANSCRIPT-1, WERROR-IGNORE-1, GARDE-EN-TETE-1, MUTANTS-SITE-APPEL-1 (et volet), règle de citation | vraies (DT7-a) | — |
| HARNAIS-UNSHARE-LO-1 | vraie (commande `ip` absente de l'hôte, mesuré ; garde de `s2bis/tests/__init__.py` présente) | — |
| PLAN-S2BIS-2-PY310-1 | vraie (`scripts/plan-s2bis-2/README.md` l.32 ; `hashlib.file_digest` en l.30 de `commun.py`) | — |
| S2BIS-MUT-COMMANDE-1 | **fausse en l'état** pour l'outil : un mutant de `gates.yml` est joué avec la ligne d'origine, classé vivant à tort (M-F2) ; un job sans checkout en tête perd sa première étape | fermé par DT7-a, DT7-f et C-1 (étapes relues sur la copie mutée, checkout exigé) |
| MUTANTS-ORPHELINS-1 | **fausse** : depuis DT7-d, la suite que lance le vérificateur a sa propre session ; à la borne, `mutants.py` n'arrête que le groupe de l'étape, la suite survit et le relevé `ps` ne la voit pas (M-F1) | fermé par DT7-a, DT7-f et C-1 (groupes de tous les descendants, relevés par parenté, arrêtés et comptés au relevé ; puce datée de la fiche) |
| HAIKU-ROLE-SOURCES-1 | vraie sur le fond (signal seul, rien n'y décide) ; forme : C-8 | fermé sur adjudication de Q-4 par DT7-i, DT7-j et C-8 |
| ENREG-EXTRACTION-INTERDITS-1 | vraie pour les fichiers ; `ni un lien qui y mène` fausse pour un lien vers le dossier interdit lui-même (M-B1) ; schéma ratifié sans trace (C-7) | fermé par DT7-b, C-3 et C-7 ; limite écrite : lien à deux sauts (M-B2) |
| S2BIS-ANALYSEUR-RESIDUS-1 | vraie : forme K exigée, résidus nommés, huit sondes en fixtures, octets égaux aux sondes poussées (8/8, sha256), runs et conclusions conformes aux preuves (`SHA256SUMS-runs` 30/30) | — |
| ENREG-DELAI-ARBRE-1 | vraie pour l'arbre suivi ; **régression** : le second `communicate()` sans borne attend un descendant détaché qui garde le tuyau (M-D1 : 6 s pour 6 s, 90 s pour 90 s ; avant DT7-d, 1 s) | fermé sous POSIX par DT7-d et C-2 ; branche Windows : L-1 du générateur (acte extérieur) |
| S2BIS-LEURRE-FORK-TMP-1 | vraie (F-16 ; mutant GD3 tué au runner) | — |
| S2BIS-ENREG-ANCIEN-OUTIL-1 | vraie au code ; un enregistrement réel d'un outil antérieur est refusé d'abord par `champs` (il précède DETTES-T7) ; README dit Q-3 à adjuger | fermé par DT7-e et C-4 |
| S2BIS-COMPILE-LIMITES-1, S2BIS-TOOLS-README-SUITE-1 | vraies | — |
| S2BIS-DRAPEAUX-LIMITES-1 | vraie (mesuré 3.10 à 3.13 : sous `-I`, `utf8_mode 0`, `optimize 0`, `hash_randomization 1` ; appliquées sans `-I`) ; README dit Q-5 proposée | fermé par DT7-e et C-4 |
| LINT-ENVIRONNEMENTS-1, volet Git Bash | vraie à la lettre : fermeture à la lecture du premier run (acte de forge, L-2) | — |
| VERIFIER-TESTS-TMP-RESTES-1 | vraie : 34 dossiers `shogen-*` par course à `622eede`, 0 avec la série, `target/tmp` vide (mesuré) | — |
| S2-SUITE-PY310-1 (DT7-k) | vraie (mesuré sous 3.10.20 : 77 FAIL, 3 ERROR ; un seul échec dans `test_oracle_record.py`, 25 tests ; `--help` en 0 ; runner et controle verts) ; la puce Matrice de DT7-a dit un test et une cause de moins | errata C-6 |

## 2. Enregistreur et vérificateur (DT7-b à DT7-e), code lu en entier

- **DT7-b.** Aucun fichier d'un emplacement interdit n'est écrit ni haché (prédicat `interdit` exécuté depuis
  `enforcement/docs-sha256sums.py`, garde `__main__` présente) ; aucun nom n'est imprimé (refus `exclus` par compte,
  `ecarts_arbre` atteint après le refus `exclus`) ; `tree.exclus` = nombre et sha256 de la liste triée ; un
  enregistrement sans ce champ est refusé (`champs`). Mon enregistrement de rôle en donne la mesure réelle : 58
  chemins exclus, 1 214 fichiers hachés. Constats : **K-B1** (C-3) un lien vers le dossier interdit lui-même
  (`docs/x -> rapports`, cible normalisée sans barre finale) est gardé, écrit pendant, puis le hachage lève
  `FileNotFoundError` (sortie 2, refus non nommé ; M-B1, `outils/exp_lien.py`) ; à deux sauts (`a -> b/d.md`,
  `b -> rapports`), même échec avec C-3 (M-B2) : limite écrite par C-3, aucun fichier interdit écrit dans les deux
  cas. **K-B2** (C-7) `tree.exclus` s'ajoute au schéma `shogen.oracle-record.v1`, dont la liste de champs est
  ratifiée à l'ADR-0028 (D6 (viii), §1 bis.6 ; même la note préexistante du README parlait de schéma v2 pour tout
  champ neuf) : l'adjudication Q-2 le décide sous la délégation A-12, mais l'ADR n'en porte pas trace ; C-7 l'écrit
  en fin d'ADR, sans décaler de ligne (garder le nom v1 ou passer en v2 reste à l'orchestrateur ; C-7 code le v1
  adjugé).
- **DT7-c1 à c4.** `residus` rend `[]` sur `gates.yml` et `gabarit` est vrai pour les cinq jobs unittest (à `622eede`
  et à `d3d897b`) ; l'enregistreur refuse avant toute écriture toute forme hors K et nomme N-12, N-14, LC-02, LC-13 ;
  AN1 refusé (Q-1 a). Mesure M-C1 (`outils/exp_tab.py`) : les formes à tabulation (alias, ancre, bloc) ne sont pas
  nommées par `residus`, mais PyYAML 6.0.1 (job g1) les refuse : couvert par la limite L-3 écrite, pas de constat.
- **DT7-d.** `groupes` suit les descendants par parenté (M-D1, scénario a : enfant direct vivant au délai, rendu en
  1,0 s ; que le fils intermédiaire, zombie, y garde le lien de groupe du descendant détaché est [inféré]).
  **K-D1** (C-2) : quand l'enfant direct est sorti et qu'un descendant détaché (double fork, `setsid`) garde le
  tuyau, l'outil l'attend sans borne (M-D1, `outils/exp_lancer.py`) ; la forme d'avant rendait la main au délai. Le délai est la garde de blocage de l'outil (`DELAI_DEFAUT`) : C-2 borne la lecture à `RELIQUAT` s et le
  README l'écrit. Côté vérificateur, la suite dans un groupe neuf arrêté avant l'effacement du dossier du compte
  ferme LE-05 (F-16) ; un descendant qui ouvrirait sa propre session n'est pas suivi (le verdict n'en dépend pas).
- **DT7-e.** Refus `ancien outil` exact au code ; voir C-4 pour l'ordre des refus. Le test neuf ne fixe pas la
  position de `-I` (mon mutant GE2, contrôle déplacé en position 2, survit à ce test et meurt par quatre autres).

## 3. Outil des mutants (DT7-f) et F8

- Classement par la commande du job : étapes `run:` lues par `etapes` du vérificateur de l'arbre de l'outil, runner
  d'abord, `bash --noprofile --norc -eo pipefail`, borne pour le job, sortie 1 tuée, 0 vivante, autre FATAL : exact.
- **K-F1** (C-1, mesure M-F1, `outils/exp_orphelin.sh`) : job qui lance le vrai vérificateur, mutant qui fait dormir
  la suite 8 s, borne 3 s : FATAL, `relevé ps de fin : aucun processus des 2 groupes`, sortie 0, et la suite pose sa
  marque 6 s après la fin de la campagne. C'est l'orphelin de l'écart E-CA3-1, rouvert par la session propre de DT7-d,
  sur tous les jobs unittest. **K-F2** (C-1, M-F2) : un mutant de `gates.yml` (`run: echo premier` vers
  `run: exit 1`) est classé vivant, les étapes étant lues une fois avant le témoin ; la première étape n'est pas
  contrôlée (checkout supposé).
- **F8, équivalent : jugement.** Équivalent au sens strict, dans la série comme avec C-1 : chaque groupe relevé est
  arrêté par `SIGKILL`, aucun membre vivant ne peut rester, le relevé ne peut rien trouver (sauf réemploi de PID) ;
  c'est une garde redondante, aucun test ne la distingue seule. Mais l'équivalence cachait le vrai défaut : le relevé
  ne portait que sur les groupes des étapes, non sur ceux des descendants partis dans leur propre session (K-F1).
  Avec C-1, ces groupes sont arrêtés et comptés ; mon mutant GF5 (descendants retirés) est tué par le cas M6.

## 4. Workflows (DT7-f, DT7-g)

- YAML valide : `workflows-yaml : conforme (7 workflow(s), PyYAML 6.0.1)` ; `runners-epingles : conforme (7
  workflow(s), 22 clé(s) runs-on/os lues)` ; étape Git Bash sous `windows-2025`, `if: runner.os == 'Windows'`,
  `shell` par `defaults.run.shell: bash`.
- Plancher de l'étape éprouvé sur l'`awk` de `squelette.yml` l.75 (même texte) : 227 ok/0 échec : 0 ; 1 000/0 : 0 ;
  226/0, 228/1, 0/0, autre runner, sortie vide : 1. Sous `pipefail`, un runner en échec ou un `tee` qui ne peut
  écrire fait échouer l'étape : elle ne peut pas passer à vide.

## 5. Rust (DT7-h)

- `cargo build --locked --workspace --all-targets` puis l'étape Tests du job `squelette`
  (`cargo test --locked --workspace -- --nocapture`), cible par défaut de la copie, hors réseau : sortie 0, 29 lignes
  `test result: ok.`, 272 passés, 0 échec ; 0 entrée dans le `TMPDIR` du run, `target/tmp` vide. Même mesure à
  `622eede` sans la série (28 lignes `test result: ok.`) : 34 dossiers `shogen-*` laissés.
- Le témoin voit un chemin temporaire composé à la main : GH4 (`std::env::temp_dir()` dans `bout_en_bout.rs`) et
  GH5 (`env!("CARGO_TARGET_TMPDIR")` dans `coquille.rs`) tués par `aucun_test_ne_compose_de_chemin_temporaire_a_la_main`.
  Toutes les liaisons de `commun::Arbre` vivent jusqu'à la fin de leur test (aucun temporaire lâché).

## 6. Fiches et textes (DT7-a, DT7-i, DT7-j, DT7-k) et point ouvert

- DT7-j : `CLAUDE.md` l.1 à 49 identiques à la tête à l'octet ; ajout l.50-55 ; point 8 décalé de l.50-51 à l.56-57.
  DT7-k : préfixe de `s2-harness/README.md` identique à la tête (ajout en fin seulement) ; chaque phrase vérifiée,
  sauf celle de la copie d'essai où deux causes sont levées (mesure du générateur, non refaite : L-G3).
- DT7-a : ajouts datés ; l'exception de la règle 3 s'insère au milieu de la fiche (+8 lignes à partir de l.29) ; DT7-i
  décale `shogen-extracteur` (+2). **K-T1** (C-8) : DT7-i réécrit sans date deux textes validés (description, règle 6)
  et date la règle 7 à 05:14:30, avant l'adjudication qu'elle cite (06:24:31) : C-8 rend les deux textes à l'octet de
  la tête et ajoute des phrases datées. **K-T2** (C-6) : renvoi `l.18-21` (l'épinglage finit l.22) ; puce Matrice :
  un test et une cause de moins que l'errata de DT7-k. **K-T3** (C-4) : README de l'outil, `à adjuger` pour Q-3 et
  `décision proposée` pour Q-5, faux depuis 06:24:31.
- Rôle trieur de sources (DT7-i, DT7-j) : rien n'y décide (pas de retrait, d'écart, de fusion, de niveau ; proposition
  sans effet avant adjudication ; aiguiller, constituer la liste, juger admissible : refusés). Limite du doc 03 lu en
  [2nd] : je la juge juste et sans effet sur le rôle tant que le doc 03 ne le contredit pas, puisque le rôle n'attribue
  aucun niveau ; mais la relecture du doc 03 au poste local n'a pas de déclencheur inscrit (O-1).
- **Point ouvert, lint l.8** : C-5, ligne réécrite en place, même longueur, 212 lignes avant et après, aucun
  décalage. Sur la copie série + C-1..C-8 : `bash enforcement/lint-model-pinning.sh .` donne `OK (R-1) : 7
  fichier(s)` et le runner `model-pinning : 227 ok, 0 échec`. Les quatre pièces de `docs/adr-0028/lint-haiku/` qui
  citent `CLAUDE.md l.23-49` sont des pièces datées : inchangées.

## 7. Tests et mutants

- Rouges de mes corrections, sur le code de la série : C-1 `sorties/C-1-rouge.txt` (2 FAIL : durée de la campagne,
  cas `tete`), `C-1-rouge-M6.txt` (`petit-enfant d'une autre session vivant après la borne`), `C-1-rouge-M8.txt` ;
  C-2 `C-2-rouge.txt` (`duree3 < 30` faux, 95 s) ; C-3 `C-3-rouge.txt` (`FileNotFoundError`). Verts : `C-1-vert.txt`,
  `C-2-vert.txt`, `C-3-vert.txt` (sous `-X dev -W error`, environnement compris : 0 ligne `Exception ignored`).
- Mutants du réviseur (25), tous classés par la commande du job qui porte le code (outil de `tmp/val`, arbre relu, à
  part de la copie mutée `tmp/mut` = série + corrections ; borne 300 s ; Rust : `outils/mutants_rs.py`, étape Tests
  du job `squelette`, borne 600 s, fichier rendu contrôlé par sha256) ; témoin vivant d'abord, relevé `ps` vide à la fin
  de chaque campagne. Définitions : `mutants/mut-s2.json`, `mut-controle.json`, `mut-rs.json` ; diffs et sorties :
  `mutants/s2/`, `mutants/controle/`, `mutants/rs/` ; classements : `mutants/*-classement.txt`.

| diff | mutants | job | tués | par |
|---|---|---|---|---|
| DT7-b | GB1 (dossier sans barre), GB2 (dossiers comptés), GB3 (`tree.exclus` non comparé), GB5 (`n = 0`) | s2-harness-unittest | 4/4 | `test_extraction_sans_emplacement_interdit` |
| DT7-c | GC1 (U+001F), GC2 (clé entre guillemets), GC3 (LC-02 +2), GC4 (alias), GC6 (site d'appel : `residus` retiré de l'enregistreur) | idem | 5/5 | runner S-02, S-03, S-04, S-07 à S-11 (GC1 à GC4) ; `test_ligne_du_job_forme_k_et_residus_nommes` (GC6) |
| DT7-d | GD1 (`groupes` réduit à la racine), GD2 (arrêt après la sortie retiré), GD3 (`os.killpg` vers `p.kill()` au vérificateur), GD5 (`RELIQUAT` de C-2 retiré) | idem | 4/4 | `test_delai_arrete_l_arbre_entier` ; F-16 (GD3) |
| DT7-e | GE1 (`-B -c` réduit à `-B`), GE2 (`-I` lu en position 2), GE3 (contrôle de type retiré) | idem | 3/3 | test DT7-e (GE1, GE3) ; quatre autres tests (GE2) |
| DT7-f | GF1 (sortie 3 tuée), GF3 (témoin non exigé), GF4 (aucun arrêt de groupe, C-1), GF5 (descendants retirés, C-1) | controle-unittest | 4/4 | `test_classement_…`, `test_refus_…` |
| DT7-h | GH1 (`Drop` vide), GH2 (rang retiré du nom), GH3 (`sur` sans vidage), GH4, GH5 (chemins à la main) | squelette, étape Tests | 5/5 | `arbres.rs` |

  Aucun vivant, aucun FATAL, aucun mutant équivalent dans mon jeu. Sites d'appel et étiquettes : GC6, GD3, GE2.

## 8. Gates

- **Copie finale (série seule)**, chaque étape `run:` de `gates.yml` telle qu'écrite (g3 `--history` non lancé),
  `outils/etapes.py`, réseau coupé : toutes à 0 (06:53-07:00) : hooks `57 ok` ; `OK: aucun marqueur de dette nu.` ;
  runners épinglés et workflows conformes ; `model-pinning : 227 ok, 0 échec` ; `OK (R-1) : 7 fichier(s)` ;
  `journaux-modele : conforme` ; `docs-sha256sums : conforme : 39 SHA256SUMS, 314 ligne(s)` ; secrets `147 ok` et
  arbre OK ; runner `152 ok, 0 échec` ; S2 `Ran = 423`, s2bis 342, sim-bis 279, calib-actifs 65, controle 39 (`--egal`).
- **Matrice** (`-X dev -W error`, `PYTHONDEVMODE=1 PYTHONWARNINGS=error` rendus aux enfants) : runner et ligne du job
  controle sous 3.10.20, 3.11.15, 3.12.3, 3.13.14 ; suite S2 sous 3.11 à 3.13 : tout en 0, 0 ligne `Exception ignored`
  ni `Warning` ; même matrice sur la série + C-1..C-8 : identique.
- **xtask** (lignes VERDICT seules) : S-G1 à S-G8 `VERT (0 violation(s))`, `cargo fmt --check : VERT`, no_std `VERT`,
  `cargo clippy -D warnings : VERT`, S-G9 `ROUGE (1 violation(s))` : `docs/17-modele-de-menace.md:70` (copie creuse) ;
  verdict global ROUGE, le même sur la série + C-1..C-8.
- **Série + C-1..C-8** (`tmp/val`) : toutes les étapes de `gates.yml` à 0, mêmes comptes ; voir section 10 pour la tête.

## 9. Enregistrement du rôle G2 (outil de la série)

- Commande (forme du bloc de gabarit), depuis `g2/tmp/copie` (622eede + série), réseau coupé, `TMPDIR` de la G2 :
  `env -u SHOGEN_S2_CAMPAGNE_CONTROL PYTHONDONTWRITEBYTECODE=1 python3 -B s2-harness/tools/oracle_record.py --role G2 --commit 622eede75f54f1b51c9218d04ec50668232c950d --auteur claude-opus-5-5 --depot <g2>/tmp/copie --sortie <g2>/enregistrement`
  (sortie 0, 07:59:02-07:59:56).
- Enregistrement : `enregistrement/shogen-622eede-G2-20261010T075902Z-15732.json`, sha256
  `2168cf28eb3a2ca301c9d6b26f6525f4ba8788f1e9a6abcb9468fb8b485d216e` ; sortie du run `…15732.0-suite.out`, sha256
  `465c542e71449e7e6c24a5b34193819529513709755d2af70c56f18da8c5a962` (`Ran 419 tests`, `OK (skipped=2)`). Champs :
  rôle G2, auteur `claude-opus-5-5`, `tree.commit` 622eede…, 1 214 fichiers, `tree.exclus` `{nombre: 58, sha256:
  9bfc5daf…0c71}`, exit 0, run `suite` lancé par `-B -c`.
- `--verifier … --role G2 --commit 622eede… --depot <g2>/tmp/copie` : `conforme : … tree.sha256 recalculé`, sortie 0.
- L'enregistrement atteste la base et la suite lancée sur elle ; il se rattache à la série par l'empreinte
  `687d68e0…7704` écrite plus haut.

## 10. Tête relue, écarts, limites

- **Tête relue à 08:04:23** : `d3d897bd79cf40427234d0517b7735b0fc51be20` (14 commits : versement de DETTES-T14,
  DETTES-T6 DT6-a à DT6-l). `git diff --stat 622eede d3d897b` limité aux chemins de la série et des corrections :
  seul `.github/workflows/gates.yml` change (DT6-j : quatre lignes de commentaire au job `s2bis-unittest`, plancher
  s2bis 342 vers 358). Sur une copie neuve de `d3d897b` : série 14/14 et C-1..C-8 8/8 (`git apply --check` puis
  `git apply`), `residus` vide, forme K des cinq jobs ; toutes les étapes `run:` de `gates.yml` (g3 `--history`
  excepté) à 0 (08:10-08:16) : runner `152 ok`, S2 `Ran = 423`, s2bis `Ran = 358`, sim-bis 279, calib-actifs 65,
  controle 39, lint 227 cas, `docs-sha256sums : conforme : 40 SHA256SUMS, 319 ligne(s)`.
- **Tête relue à 08:16:44** : `1b8a44df2567b7f80ea25b8276fc4b6505f7706e` (DT6-m, DT6-n) ; `git diff --stat d3d897b
  1b8a44d` limité aux mêmes chemins : vide ; copie neuve de `1b8a44d` : série 14/14 et C-1..C-8 8/8 (`git apply
  --check` puis `git apply`). Aucun chemin de la série n'a changé depuis, hors `gates.yml` (DT6-j, ci-dessus).
- **Écarts du réviseur.** E-1 : un `grep -rn` limité à `crates/shogen-verifier/{tests,src}` de la copie (code Rust,
  aucun emplacement interdit possible), contraire à la lettre du brief ; listes explicites ensuite. E-2 : copie par
  clone creux, non par `git archive` nu : l'enregistrement de rôle exige un dépôt (`--depot`, `--commit`). E-3 :
  `git ls-tree --name-only HEAD --` sur trois dossiers explicites de `docs/` (`adr-0028/lint-haiku/`,
  `adr-0029/g0-plan/`, `adr-0029/plan-s2bis/`), noms permis seuls affichés. E-4 : des échappements Python (barre
  oblique inverse) tapés dans des scripts de commande ; les fichiers écrits ont été contrôlés sur leurs octets
  (aucune barre ajoutée aux corrections ; 23 lignes d'items sur 23 égales à la source). E-5 : `SHA256SUMS` de ce
  dossier calculé par un parcours de ce seul dossier (sorties du réviseur, copies effacées avant).
- **Limites rendues à l'orchestrateur.** L-G1 : l'étape g3 `--tree` lit par `git show :0:<chemin>` le blob de chaque
  fichier suivi, emplacements interdits compris (index complet d'une copie creuse), dans un temporaire jamais affiché ;
  le brief n'exclut que `--history` (déclencheur : prochain brief qui fait jouer les gates sur une copie creuse).
  L-G2 : l'absence de renvoi par numéro de ligne aux deux fiches (`shogen-worker` : +8 lignes dès l.29 ;
  `shogen-extracteur` : +2 dès l.11 avec DT7-i, +3 puis +4 avec C-8) n'est vérifiée que sur 17
  fichiers nommés, la recherche récursive m'étant interdite (déclencheur : avant le commit de DT7-a et DT7-i, mesure
  par `git grep` à pathspecs d'exclusion, forme de la phase 2 du générateur). L-G3 : la phrase de DT7-k sur la copie
  d'essai (deux causes levées) n'est pas re-mesurée. O-1 : la relecture du doc 03 au poste local (limite Q-4) n'a pas
  de déclencheur inscrit à l'annexe B ou au JOURNAL.

## Journal de provenance (G1)

- Sources [lu] : pièces du lot citées en tête ; annexe B l.380, 935, 971-972, 990, 1042-1043, 1047, 1074, 1209,
  1219-1220, 1230-1235, 1261, 1356, 1364, 1378, 1388 (23 lignes égales à `ITEMS-ANNEXE-B.md`, script), l.1615 ;
  annexe D l.28-60 (D.2 en noms) ; ADR-0028 l.141-146, 203-212, fin ; `PAQUET-PREREG-S2.md` l.15-16, 189-223 ;
  `CP2-S2.md` (renvois) ; G0 `docs/adr-0029/G0-lot-PLAN-S2BIS.md` l.15-24 ; `scripts/plan-s2bis-2/README.md` l.28-34 ;
  `s2-harness/README.md` l.12-22 ; `docs-sha256sums.py` ; `METHODE-PARTIES.md` (aucun gabarit) ; dossier de l'épreuve
  de forge (`ADJUDICATION.md`, sondes, `runs/`) ; fiches, outils, tests, workflows et sources Rust de la série en
  entier. Doc 03 du corpus : [2nd] (par `CLAUDE.md`). Aucune source [abs] ; aucun chiffre de seconde main.
- Commandes et sorties : `outils/` (copie, isolement, étapes, matrice, mesures, mutants), `sorties/` (gates,
  matrices, rouges et verts, cargo, xtask filtré, 3.10), `mutants/`, `corrections/`, `NOTES.md`.

- Fin de la passe : 2026-10-10 08:18:02 UTC (`date -u`). Aucun processus du réviseur vivant ; copies et cibles effacées ; aucun
  commit, aucun push, aucun réseau ; `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée ; `SHA256SUMS` écrit en dernier.
