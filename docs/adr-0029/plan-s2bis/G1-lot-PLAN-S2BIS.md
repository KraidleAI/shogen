# Lot PLAN-S2BIS, phase 1 : rapport du worker

**Gate 0** : modèle résolu `claude-opus-5-5`, effort max. Horloge relevée par `date -u` : début 14:57:42 UTC, fin 15:49:03 UTC (2026-10-04).

## 1. Résumé

- **Livré** : le code des trois sorties du G0, les tests, `parametres.json` et `lancer.sh`, en 9 diffs R-25 (fichiers neufs sous `scripts/plan-s2bis/`).
- **Aucune exécution sur les journaux.** Le dossier `execution/journaux/` n'a été ni listé, ni haché, ni ouvert.
- **Tests d'abord** : 31 tests. Chaque module a d'abord été montré rouge (module absent), puis vert.
- **Mutants** : 39 mutations nommées, 39 tuées, chacune par son test nommé ; 0 vivant, 0 FATAL ; témoin vert.
- **Répétitions** : sur journaux synthétiques à l'échelle de S2, le flux complet de phase 2 passe. `lancer.sh` sort en 0 en 72 s, avec l'extraction réelle de `f35a70c` et les épingles du harnais extrait.
- Le dépôt n'a reçu aucune écriture. La tête a avancé pendant la session (§6, E-2).

## 2. sha256 à épingler au JOURNAL

| fichier (`scripts/plan-s2bis/`) | sha256 |
|---|---|
| `tau_sigma.py` | 56f2c35a1ecd7de32b8146b19719746df9a2d4824f7dfe61c372bd0ecfabe20c |
| `episodes.py` | 90c7842d9e1193b0629de41cfd91fbbebb45d4ec4731af89b77e70a96af43fd2 |
| `okx.py` | 5efe4e584b09817088bf95a340e404555333a583c031c0cb78b82f500cd9f7d0 |
| `commun.py` | 22cc645f033d47e2dbfcc64b1ee24ddf3486c03dcdf5052a0fbb8f696653f820 |
| `regles.py` | 7bfbb14f2e7d0fca50d1a3e8864440711c4a4ee99e336157b604ddce90172028 |
| `parametres.json` | 0c8c8d8c8d56145b698fbd2c61c6bf4273641e137bdab2ca2c827da3414cf693 |
| `lancer.sh` | f5b7e89c2d1d5126547f2521e46c904c6eb2d5cc6b85f59c38cb22a58b103307 |
| `README.md` | 91af7259364a8095f68090cc280337275ec7635db43e9fc7ac4f4a730bb6fe3e |
| `tests/__init__.py` | 1a31ff4699cca3fab50ff2e8433bac4ce762d9a2f26b73c9126dff1e91f7aac5 |
| `tests/fixtures.py` | 17ae3c130a1e4a1fcde2b3fc8d8a4384a77f513533836f0ec6fad657b4903913 |
| `tests/test_commun.py` | b222ced9c53fc8867ae1c6c698e0eef11854a2ffe2df7cea5b0decd4414ad885 |
| `tests/test_regles.py` | 48f4dc469403391bef661e018d54385436c5a3b7db66b6ad0e9279bfdee04546 |
| `tests/test_tau_sigma.py` | 86d4eb23373f038698e8ad70a0110907b02b11c7bb149728ae5e278b5aef1911 |
| `tests/test_episodes.py` | 33b82372281322cf2518668f3eec408bc627a6a64445ac9fd1d340e53e814446 |
| `tests/test_okx.py` | f27ef48439314cda8d7e9d097bc9a91280715a7a365fa846144cbc89775572a8 |
| `tests/test_lancer.py` | f1116b1857be1933c6165704a8ca6a080c5922e8b877d0f87f8b2bd6db1ce109 |

Ces sha256 ont été vérifiés une seconde fois après le dernier changement (même valeurs). Les en-têtes des sorties de la répétition générale portent ces mêmes sha256 pour les scripts et `commun.py`.

## 3. Diffs (R-25), contre la tête 6c37859

Dossier : `/tmp/claude-0/-home-user-shogen/7ba84933-ba6d-5813-9ef4-ca3ac4febd16/scratchpad/s2bis/plan/diffs/`, à appliquer dans l'ordre (`git apply`).

| diff | contenu | lignes | sha256 |
|---|---|---|---|
| 01-parametres-readme | `parametres.json`, `README.md` | +127 | ed9e253a… |
| 02-commun | `commun.py` | +198 | 5a3afefc… |
| 03-regles-fixtures | `regles.py`, `tests/__init__.py`, `tests/fixtures.py`, `tests/test_regles.py` | +199 | 93ed5fde… |
| 04-tests-commun | `tests/test_commun.py` | +152 | 79c1dd43… |
| 05-tau-sigma | `tau_sigma.py`, `tests/test_tau_sigma.py` | +198 | 66299254… |
| 06-episodes | `episodes.py` | +129 | 5aaa8b2d… |
| 07-tests-episodes-okx | `tests/test_episodes.py`, `okx.py` | +166 | af2f83ed… |
| 08-tests-okx-lanceur | `tests/test_okx.py`, `lancer.sh` | +162 | ce5c97d4… |
| 09-tests-lanceur | `tests/test_lancer.py` | +146 | 82e65abb… |

- **Vérification sur une copie neuve de la tête** (`git archive HEAD`, dossiers interdits exclus) : `git apply --check`, puis `git apply`.
- La suite du lot reste verte à chaque pas : 3, 14, 17, 17, 22, 25, 31 tests.
- L'arbre reconstruit est identique à l'octet à l'arbre de travail.
- Aucun octet de barre oblique inverse, de tabulation ni de retour chariot, ni dans les fichiers ni dans les diffs.

## 4. Ce que fait le code

**Socle commun**
- **`commun.py`**
  - Importe `shogen_s2` depuis une extraction de `f35a70c` (`--harnais`), après contrôle du sha256 des 5 modules chargés (`__init__`, `model`, `records`, `window`, `r1`). Tout autre module chargé est refusé. Le `r1.py` de la tête diffère de l'épingle (c5666e8d… contre 0a16e5de…), donc le harnais de la tête est refusé.
  - Lit les journaux par les appels de `r1.recompute_from_journal` : segment J28 (t0 1787770800, n fixe 38600), plage D5 [1790273880 ; 1790435280] exclue.
  - Construit le pool S2 (D1) et la sortie « base » de `compute_r1`, puis le pool D1-bis.
  - **Contrôle de cohérence** : n, K et P̂_more par strate, chaîne pour chaîne, comparés aux valeurs du bloc 3 épinglées dans les paramètres, puis au bloc 3 relu dans le rendu J28 (sha256 épinglé).
  - **Fail-closed** : en écart, la sortie ne porte aucune valeur d'analyse (code 1). Le fichier est écrit en entier ou pas du tout.
  - Première ligne de chaque sortie : « préparation de S2-bis ; ne change pas le verdict de S2 (« R1 discrimine » = FAUX) ».
- **`regles.py`** : quantile au rang le plus proche ⌈num·N/den⌉ ; τ = grid-ceil(1,5 × max_s P99,9, 0,0005), en rationnels exacts, avec ses bornes ; σ = max(plancher, 3 × max_s P99 staleness).

**Les trois sorties**
1. **`tau_sigma.py`** : par classe, N, P99,9, P99, maximum et staleness, par strate ; puis τ_c, la règle au maximum (descriptive), σ_c, la limite Chainlink, et un bloc `[VALEURS POUR LE PAQUET DE S2-BIS]`.
2. **`episodes.py`** : épisodes de panne et d'écart par unité D1-bis et par strate (comptes, taux, moyenne, maximum, P50/P90/P99, censurés, complets, histogramme). Puis la courbe FIV_série(ℓ) pour le pool S2 et le pool D1-bis. À ℓ = 240, le pool S2 doit égaler le bloc de `compute_r1`, sinon refus.
3. **`okx.py`** : co-écarts des deux flux OKX (dans K, par type, en panne_transport des deux), puis K recalculé quatre fois : paire fusionnée en une unité, sans okx_index, sans okx_ticker, sur le pool D1-bis. Comptes seulement, aucun z.

**Le lanceur**
- **`lancer.sh <journaux> <sortie> <travail>`** contrôle, dans l'ordre :
  1. la variable `SHOGEN_S2_CAMPAGNE_CONTROL` n'est pas posée, la sortie est vide ;
  2. le sha256 du paquet de S2 est égal à l'épingle (4d2a8276…, égale au manifeste du sceau) ;
  3. le bloc machine a une seule ouverture et une clôture, et son `commit_analyse` est égal à celui des paramètres ;
  4. le sha256 de chaque journal du bloc est égal (y compris `raw.jsonl`, haché seulement).
- Il extrait ensuite `f35a70c` avec la commande du brief et ses exclusions, puis lance les trois scripts.
- Il n'affiche que des noms, des codes et des sha256. Codes : 0, 2 usage, 3 refus, 4 extraction, 5 script en échec.

## 5. Preuves

- **Rouge, puis vert** : les tests de chaque module, lancés avant ce module, échouaient (ModuleNotFoundError ; FileNotFoundError ×6 pour le lanceur). Ils passent ensuite. Trois échecs intermédiaires venaient de mes tests, corrigés :
  - un `Decimal` arrondi par le contexte par défaut dans le test ;
  - un `round` hors de la précision ;
  - une variable mal nommée.
- **Valeurs de référence calculées à la main** :
  - P̂_more = 161/625 = 0,2576 et 0,3484 (fixtures) ;
  - FIV_série(2) = 1,25 et 35/36 ;
  - K des quatre variantes OKX ;
  - populations exactes par classe et par strate.
- **Mutants** (`outils/mutants.py`, journal `outils/mutants-3.txt`) : MC-1 à MC-12, MR-1 à MR-4, MT-1 à MT-7, ME-1 à ME-5, MO-1 à MO-4, ML-1 à ML-7. Résultat 39/39 tués, test nommé parmi les échecs dans les 39 cas. Classement selon le contrat du runner : 0 vivant, 1 tué, toute autre sortie FATAL.
- **Suite `s2-harness`** (non modifiée) : 405 tests, OK (2 sautés), au début et à la fin.
- **R-13** : aucun TODO/FIXME. **Gate des secrets** : les deux motifs, chargés depuis `gate-secrets.sh`, ne trouvent rien. **R-8** : bibliothèque standard ; bash, awk, tar, git et sha256sum seulement.
- **Répétition à l'échelle** (journaux synthétiques, 39 102 fenêtres, 106 Mo) :
  - chaque script prend 22 à 25 s, avec une mémoire maximale d'environ 1 Go ;
  - répétition générale par `lancer.sh`, dans un clone jetable : code 0 en 71,9 s, `lancer.log` vide, dossiers interdits absents de l'extraction ;
  - estimation sur les vrais journaux (149 Mo) : environ 2 min. **Non mesuré** sur les journaux scellés.

## 6. Écarts à adjuger

- **E-1** : les tests et la campagne de mutants ont d'abord créé 2 617 dossiers temporaires dans `/tmp` (valeur par défaut de `tempfile`), hors du dossier d'écriture du brief. Ils ne contenaient que des fixtures synthétiques. Je les ai retirés (seulement les miens). Correction : chaque test retire désormais son dossier (`addCleanup`), et mes runs suivants ont posé `TMPDIR` dans le scratchpad.
- **E-2** : la tête a avancé pendant la session, de 2aa4d6b à 6c37859 (c354d15 à 15:08:39, 6c37859 à 15:17:34 UTC). Les diffs sont faits et vérifiés contre 6c37859. Les pièces épinglées sont inchangées : G0 81bf3f33…, ADR-0029 6770cc5c…, paquet 4d2a8276…, rendu 26877549… ; `s2-harness` est identique (`git diff --quiet`).
- **E-3** : `test_lancer.py` crée un dépôt git jetable (`git init`, `git add`, `git write-tree`, aucun commit). La répétition générale a utilisé un clone jetable (`git clone --no-hardlinks --no-checkout`), qui ne fait que lire la source. Ce n'est jamais le dépôt du projet, mais c'est à confronter à « aucune opération git en écriture ».
- **E-4** : la commande d'extraction du brief fait passer tous les fichiers dans le tube, dossiers interdits compris ; `tar` les écarte du disque. C'est conforme au brief ; je le signale seulement.
- **E-5** : des `*.jsonl` **synthétiques** (fixtures, répétition) ont été écrits et lus par mes outils. Ils sont maintenant retirés. Aucun journal réel n'a été ouvert.
- **E-6** : le dossier `s2-harness/tests/__pycache__` existe, daté du 2026-10-02 et ignoré par git. Il est antérieur à la session ; ce n'est pas de mon fait.
- **E-7** : j'ai lu le bloc 3 du rendu J28 seulement par ses 4 lignes (en-têtes de strate et P̂_more), comme le brief l'autorise.

## 7. Choix du worker fixés dans `parametres.json`, à adjuger

- **Q-1, population de σ** : je prends celle de τ, lecture littérale de « même population » (cellules à l'axe (i) sous le σ de S2). Conséquence : la staleness est tronquée à σ_S2, donc σ_c ≤ 3·σ_S2. L'autre lecture serait la règle de clôture sur toutes les répondantes horodatées.
- **Q-2, pool D1-bis** : D1 (a), D1 (b) et le seuil « presque mort » de B.39 (2·ok < n_s), appliqués par strate (ADR-0029 §2.5 l.168). Un retrait éventuel est imprimé ; le pool compterait alors moins de 10 hôtes.
- **Q-3, bornes de τ** : écrêtage sur la grille, avec un signal (0,0005 en bas ; 0,0280 en haut, dernier multiple sous 2,85 %). L'autre option serait de refuser et de remonter la question.
- **Q-4, épisodes** : classés sous les σ et τ committés de S2, coupés par toute fenêtre non retenue ; les épisodes au bord sont marqués censurés.
- **Q-5, grille de ℓ** : 1, 2, 3, 5, 10, 15, 20, 30, 60, 90, 120, 180, 240, 360, 480, 720, 1440 ; la garde n ≥ 30·ℓ est imprimée.
- **Q-6** : je laisse le README de `docs/adr-0029/plan-s2bis/` à la phase 2, puisque le lanceur exige un dossier de sortie vide.

## 8. Items à former (PAROXYSME)

- **SHOGEN-WORKER-TMPDIR-1** (proposé) : des tests qui utilisent `tempfile` écrivent par défaut sous `/tmp`. Consigne à ajouter aux fiches et aux briefs : poser `TMPDIR` dans le dossier d'écriture du lot (constat E-1).
- **SHOGEN-LECTEUR-INDEP-1** (existant) : ce lot réutilise aussi les lecteurs du harnais ; la limite s'y étend.

## 9. Phase 2, sur ordre

1. Vérifier les sha256 du §2 sur les fichiers commis.
2. Lancer en détaché : `setsid nohup bash scripts/plan-s2bis/lancer.sh <scratchpad>/execution/journaux <sortie neuve> <travail neuf> > <travail>.out 2>&1 &` (PID consigné, fin constatée en sondant le PID).
3. Verser ensuite les trois sorties et `SHA256SUMS` dans `docs/adr-0029/plan-s2bis/`, avec leur README.

## 10. Journal G1 (provenance)

**Lu [lu]**
- Le brief (sha256 recalculé égal : 9b87f087…f287), `CLAUDE.md`.
- G0 PLAN-S2BIS en entier ; G0 de vague en entier.
- ADR-0029 : l.1-212 et l.374-463 (§1, §2.1 à §2.7, §6, §8.1, §8.2).
- AVIS-STATS : l.32, l.48, l.52, l.61, l.66.
- Annexe B : l.32, l.545-556 (B.39), l.683, l.735-801 (B.49, B.50).
- Annexe D : l.32-48 (liste D.2, pièces non ouvertes).
- Paquet de S2 : §2, §3, §6, §11, §13 (bloc machine) ; manifeste `docs/adr-0028/sceau/PAQUET.sha256`.
- `PROCEDURE-EXECUTION.md` en entier.
- Rendu J28 : repères `[BLOC` et 4 lignes du bloc 3.
- Lot POST-PREREG : README des sorties, README des scripts, `commun.py`, fixtures, tests.
- Harnais à `f35a70c` : `r1`, `records`, `window`, `closure`, `journal` en entier ; `sources` l.226-401 ; `run_campaign` l.1-60 ; `rendu_unique` l.1-82.
- doc 10 l.420-443 ; ADR-0022 l.1-60 ; `docs/adr-0022/sigma-tau.json` (servi seulement à la répétition synthétique).
- `gates.yml` (job R-13) ; `lint-model-pinning.sh` l.1-60 ; `gate-secrets.sh` l.62-63 ; `xtask/src/sg5.rs` l.1-72.

**Non ouverts** : `docs/11`, `docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, toute pièce de D.2, `JOURNAL.md`, les sorties du lot POST-PREREG, tout journal réel. Aucune valeur de seconde main [2nd] n'est utilisée.

**Valeurs reprises dans `parametres.json`, relues ou recalculées par programme** (`outils/gen_parametres.py`)
- Bloc 3 : calme (24585, 154, 0.0013629504…3986) ; stress (11397, 133, 0.0014663989…3928).
- 5 épingles du harnais, calculées sur l'extraction et égales aux blobs de `f35a70c`.
- Segment et plage, égaux à `rendu_unique.SORTIES` « j28 » ; un test le vérifie.
- Planchers et classes, pris à `sources.py` à `f35a70c`.
- Règle d'ADR-0029 l.178-180, recopiée par programme ; l'aller-retour JSON est vérifié.

**Exposition** : valeurs de S2 déjà portées par ADR-0029 (K, z, FIV, P99 du τ observé, OKX 64/64) et le bloc 3. Aucun P99,9, aucune valeur des trois sorties.

Fichiers utiles, sous `/tmp/claude-0/-home-user-shogen/7ba84933-ba6d-5813-9ef4-ca3ac4febd16/scratchpad/s2bis/plan/` :
- `travail/scripts/plan-s2bis/` (arbre livré)
- `diffs/`
- `outils/mutants-3.txt`, `outils/generale.log`
- `repetition/sorties-SYNTHETIQUES/`
