# Relecture G2 — préparation de la partie 4 de S2 (réviseur neuf)

- Ouvert le 2026-10-03 01:07 UTC (`date -u` : Sat Oct  3 01:07:11 UTC 2026).
- Brief : `g2-p4/BRIEF-G2-P4.md`, sha256 `d3293a3c75ca8f1697a2e8cba0ef9ec9458fe76d3432317ac8558953e1b217b6` (recalculé, égal).
- Dépôt `/home/user/shogen`, branche `partie-4-execution`, tête `b7a1b4a35967d41d36e63187c23da7c48f7997af`, arbre propre
  (`git --no-optional-locks status --porcelain` vide).
- Périmètre : `git log b254b89..b7a1b4a`, 25 commits (18cbfb6 … b7a1b4a).

## Gate 0

Identifiant exact du modèle : `claude-opus-5-5` (Opus 5.5), effort `max`. Préfixe attendu `claude-opus-5-5` : conforme.
Je n'ai généré aucun lot de cette partie (réviseur neuf).

## Attestation D.3

« Je n'ai vu aucun z, aucun K, aucun P̂_more ni aucun φ de campagne, et je n'en ai calculé aucun ; je n'ai lu aucun taux
d'écart, de présence ou de panne d'une source réelle. Je n'ai ouvert aucune pièce de la liste fermée D.2 (points 1 à 12,
liste lue à l'annexe D l.32-45 sans ouvrir aucune pièce). Je n'ai rien lu sous `docs/rapports/`, `docs/adr-0025/` ni
`docs/adr-0028/monark-m009a/` ; de `JOURNAL.md`, seules les 20 lignes de la sélection prescrite ; aucun `*.jsonl` ;
hors du dépôt, seulement mon dossier `g2-p4/` et le fichier de sommes (empreintes). `SHOGEN_S2_CAMPAGNE_CONTROL` n'a
jamais été posée. Aucune opération git en écriture. »

Exposé à (classe M ou synthétique, déjà écrit dans les pièces admises) : comptes de D1 (Pyth), diagnostics DNS de D5
(dont deux pourcentages de `resolve_failed`, santé du harnais) et comptes de fenêtres, vus en lisant l'annexe D entière ;
D.3 (a) masquée ; tailles des trois journaux (JOURNAL l.278, métadonnées) ; sorties **synthétiques** des oracles (dont
« `T3_P_more_egaux_a_l_identique` 378 », compte de réplications synthétiques, et JOURNAL l.252) et durées synthétiques de
R-B §5 ; seuils de conception (2,33 ; 10 ; ℓ = 240 ; 7 200 ; 0,8416) ; noms de pièces de D.2 ; sujets de commits du dépôt.

Lectures **mécaniques** sans affichage (déclarées) : `cargo xtask verify` (S-G4, S-G5) a lu `docs/**/*.md`, dont
`docs/rapports/` et `docs/adr-0025/`, et S-G8 `JOURNAL.md`, sortie filtrée avant écriture (0 extrait, 0 violation) ;
`git archive HEAD | tar -x --exclude=…` et `git archive --format=tar HEAD | wc -c` ont fait passer ces octets dans un
tube, rien d'extrait ni d'affiché ; `rendu_unique.py --gardes-seules` lit `JOURNAL.md` à HEAD (garde (1), prescrit par le
brief) ; comptes de lignes de `JOURNAL.md` à 17 commits (`git show <c>:JOURNAL.md | wc -l`) et `--numstat`, nombres
seuls.

## Fichiers ouverts

Niveau [lu] sauf mention. Aucun fichier de D.2 ; aucun `*.jsonl` ; `JOURNAL.md` seulement par lignes sélectionnées (§ dédié).

1. `g2-p4/BRIEF-G2-P4.md` [lu] (sha recalculé, égal).
2. `docs/adr-0028/ANNEXE-D-preenregistrement.md` [lu] en entier (211 l. ; n'est pas une pièce de D.2 : D.2 dernier alinéa).
3. `scripts/controle/README.md`, `scripts/controle/SHA256SUMS` [lu] ; `scripts/controle/fm11.py` [lu] (source seul, **non exécuté** :
   il ouvre lui-même la cartographie l.51 et ADR-0025 l.14 par sha, ce serait ouvrir une pièce de D.2 par procuration).
4. `docs/adr-0028/PLAN-PARTIE-4.md` (33 l.), `docs/adr-0028/PROCEDURE-EXECUTION.md` (75 l.), `docs/adr-0028/execution/README.md` (7 l.) [lu] en entier.
5. `s2-harness/tools/rendu_unique.py` (507 l.), `s2-harness/tools/oracle_record.py` (274 l.) [lu] en entier.
6. `scripts/sceau/verify.sh`, `scripts/sceau/make-tsq.sh` [lu] ; `.gitattributes` [lu] (sa l.72 nomme le dossier
   `docs/adr-0028/monark-m009a/` : nom seulement, dossier non ouvert).
7. `docs/adr-0028/sceau/README.md` (34 l.), `docs/adr-0028/sceau/premier-2026-10-02/README.md` (41 l.) [lu].
8. `JOURNAL.md` : **seules** les 20 lignes sélectionnées par `grep -n "2026-10-0[23]" JOURNAL.md | grep -n "Partie 4\|CORR\|SCELLEMENT\|Jeton\|gel"`
   (numéros et longueurs d'abord, puis `sed -n '<l>p'`) : l.228, 246, 252, 254, 264, 278, 280, 282, 284, 286, 288, 290,
   292, 294, 296, 298, 300, 302, 304, 306. Signalement : aucune ne porte de z, K, P̂_more, φ ni taux par source de
   campagne ; l.228, 246, 252, 254, 264 sont antérieures à la partie 4 (parties 2 et 3) et entrent dans la sélection par
   « CORR »/« gel »/« SCELLEMENT » ; l.252 porte « P̂_more identique dans 378 » = compte de réplications **synthétiques**
   de l'oracle S-b (pas une valeur de campagne) ; l.278 porte les tailles des trois journaux (métadonnées, classe M).
9. `docs/adr-0028/PAQUET-PREREG-S2.md` : diff `ddf8c54..HEAD` (deux hunks : puce l.8, bloc l.215-216), bloc l.214-223 ;
   le reste du paquet n'a été traité que par commandes (sha256, remplacement de la correction C-1 du cp-1 bref).
10. `docs/adr-0028/CP1-BREF-REVISION-2026-10-03.md` (171 l.) [lu] en entier ; `docs/adr-0028/G0-lot-CORR.md` (92 l.) [lu]
    en entier ; `docs/adr-0028/ANNEXE-B-items.md` l.545-643 (B.38 fin à B.44) [lu], plus lignes isolées par `grep -n`
    (l.32, 50, 175, 219, 225, 277, 307, 310, 314, 319, 356, 372, 412, 507, 520) ; `docs/adr-0028/ANNEXE-A-lots.md` :
    **non lue** (L-3).
11. Rapports de rattrapage : `G2-RATTRAPAGE-R-A.md` (plan des sections ; l.241-269 ; l.198, 251-252), `-R-B.md` (plan ;
    l.202-220 ; l.253-282), `-R-C.md` (plan ; l.212-222 ; l.255-317) [lu, plages] ; `INVENTAIRE-G2-RECALCUL.md` (en-têtes
    et lignes G-1..G-4 par `grep`) ; `AVIS-SEUIL-FLUX-QUASI-MORT.md` (en-têtes ; l.71-83 ; contrôles de recopie par
    script) ; `docs/G2-lot-CORR.md` (l.20-41, 78-90, 255-257, 279-283, 369, 421-422, 442-445 par `grep`/`sed`) ;
    `docs/G1-lot-CORR.md` (lignes isolées par `grep` : 13, 263, 287-288, 323-324, 519-524).
12. Code [lu, plages] : `s2-harness/shogen_s2/records.py` l.50-80 et lignes `grep` ; `r2.py` lignes `grep`
    (`run_params`) ; `collector.py` à `ed479c5` (l.114, 208-216 par `git grep`) ; `s2-harness/tests/test_oracle_record.py`
    l.335-375 ; lignes `grep` de `tests/` (`JETON`, `produire(`, `datetime.now`, `SCEAU`, `PAQUET`, chemins exclus) ;
    `test_exclusion.py` l.43, 217, 275 ; `scripts/sim/sim_niveau_oracle4.py` et `sim_garde_niveau_oracle_r1.py` (l.1-25
    et lignes `grep`) ; `xtask/src/main.rs` l.1-60, `lib.rs` l.40-106 et 132-215, `sg4.rs` l.100-135, `sg5.rs` l.70-100,
    `sg2.rs` l.205-235, `rapport.rs` l.70-100 ; `rust-toolchain.toml` ; `.cargo/config.toml`.
13. Données synthétiques et outils : `docs/adr-0028/sim-niveau/SHA256SUMS` et les deux paires d'enregistrements
    (`oracle4-*`, `garde_niveau_oracle_r1-*`, par `json.load`) ; résumés des huit sorties `scripts/controle/sorties-fm11/*.json`
    (comptes et noms de motifs seulement).
14. Hors dépôt : `scratchpad/sceau/SHA256SUMS-cloture-2026-09-28.txt` (411 o, empreintes et noms) ; rien d'autre.

## Commandes et sorties

- `git --no-optional-locks rev-parse --abbrev-ref HEAD` → `partie-4-execution` ; `rev-parse HEAD` → `b7a1b4a35967d41d36e63187c23da7c48f7997af` ;
  `status --porcelain` → vide.
- `git log --oneline b254b89..b7a1b4a` → 25 commits (18cbfb6 → b7a1b4a).
- `git diff --stat b254b89 b7a1b4a` → 58 fichiers, 9 233 insertions, 49 suppressions (dont `JOURNAL.md` +32, jamais affiché).
- `sha256sum -c scripts/controle/SHA256SUMS` → 11 × OK, rc 0 ; égaux aux sha du README des outils.

### Contrôle 1 — sceau

- `bash scripts/sceau/verify.sh` (01:10:44 UTC) → rc 0 ; `docs/adr-0028/PAQUET-PREREG-S2.md: OK` ; `Verification: OK` × 2 ;
  `Time stamp: Oct  3 01:04:10 2026 GMT` ; série `0x08CFC8D5` ; manifeste `519423510b21ecbebda895d6e225ab0748fb0fe5a2b257a36c9301e36bfaa3e9`.
  (Avertissement OpenSSL “is not a CA cert” sur `tsa.crt` en `-untrusted` : attendu.) OpenSSL de l'hôte : 3.0.13.
- Manifeste : 100 octets, `od -c` : une ligne `4d2a8276…f528 *docs/adr-0028/PAQUET-PREREG-S2.md\n`, 0 CR, pas de BOM ;
  `git check-attr -a` → `text: unset`, `eol: lf` (les deux manifestes) ; `.gitattributes` l.67-68 (`-text`), l.68 ajoutée
  dans la partie (seul changement de `.gitattributes`).
- `sha256sum docs/adr-0028/PAQUET-PREREG-S2.md` → `4d2a8276316b1c66a08aabb15ff3b39be812978e93dafc01a4e627f20d0af528`
  (= manifeste, = README du sceau l.9, = JOURNAL l.304) ; paquet identique à `3be95be`, `2d51940`, `b7a1b4a`.
- Jeton : `openssl ts -reply -text` → empreinte `51 94 23 51 … a3 e9` = sha du manifeste ; nonce `0xD945E64709D187D4`
  = nonce de `paquet.tsq` (`openssl ts -query -text`) ; `paquet.tsr` 4 644 o, sha `9edb19b53379f370e291c5da01d4df3bc269b67a44feddb589d1211ec5ec6b0e`
  (= README l.19, = JOURNAL l.306).
- Échéance : genTime 2026-10-03T01:04:10Z + 24 h = **2026-10-04T01:04:10Z** (= README l.22, JOURNAL l.306, PLAN l.33,
  PROCÉDURE l.75).
- Premier sceau : `git log --name-status -M ddf8c54..HEAD -- docs/adr-0028/sceau` → manifeste et requête créés à
  `0743365`, jeton à `48797f1`, déplacés en **R100** (octets identiques) à `972612a` ; README déplacé en R074 = ajout daté
  en fin de fichier seulement (`git diff 86a8a5b 972612a -M`). À `ddf8c54`, le dossier ne portait que `chain/` : la
  commande du brief (`git diff ddf8c54 HEAD -M --stat`) ne montre que des créations (voir constat C).
- Vérification hors ligne du premier sceau sur copie (`g2-p4/premier-copie/` : paquet de `ddf8c54`, fichiers de
  `premier-2026-10-02/`, `chain/`) : `sha256sum -c` OK (paquet `494d770d…8097`), `openssl ts -verify -queryfile` OK,
  `-data` OK, genTime `Oct  2 17:44:30 2026 GMT`, série `0x08CC76D7`, manifeste `680a95fd…4209`, jeton `5f5ce535…0ee8`
  (= README du premier sceau l.27) ; `chain/` : `2151b611…` et `8bfb0305…` (préfixes de D.4 c).

### Contrôle 2 — bloc machine (recalculé)

- `git diff ddf8c54 HEAD -- docs/adr-0028/PAQUET-PREREG-S2.md` : `--numstat` 3/2 ; +1 puce « Révision datée du
  2026-10-03 00:49:47 UTC » (l.8) ; bloc l.215-216 seules changées (`commit_analyse`, `sha256_script`). Conforme.
- Bloc présent (l.214-223), recalculé :
  - `commit_analyse f35a70c19ba8269f1f7e2bcd31775e4fc513da20` : `rev-parse` complet égal ; ancêtre de HEAD ;
    `git diff --quiet f35a70c… HEAD -- s2-harness/shogen_s2 s2-harness/tools` rc 0 ; `git diff --quiet HEAD -- …` rc 0 ;
    `git status --porcelain --untracked-files=all --ignored -- …` vide.
  - `sha256_script 06d189cf…9050` = `git show f35a70c:…/rendu_unique.py | sha256sum` = HEAD = fichier.
  - `sommes 70910984…caf4` = `sha256sum` du fichier de sommes du brief (411 o, 5 lignes, LF, 0 CR, ASCII).
  - trois lignes `journal` : égales, en chaîne fixe (`grep -qxF`), aux lignes `<sha> *<nom>` du fichier de sommes
    (`control.jsonl` `351f51b2…66ff`, `journal.jsonl` `98c5793e…5d74`, `raw.jsonl` `39ffb13f…c15d`) ; `control.jsonl` égal
    en outre à l'épingle `SHA_CONTROL_SCELLE` (`s2-harness/tests/test_exclusion.py` l.43). Le fichier porte deux autres
    lignes (`../campagne-driver.out.log`, `../watchdog.log`), hors bloc, sans effet (`lire_sommes` ne lit que les noms du bloc).
    *(Premier passage de ma comparaison faux-négatif : `grep -qx` sans `-F` lit ` *` comme expression régulière ;
    refait avec `-F` : 3 × OK. Erreur de ma commande, pas du paquet.)*
  - `cacert_sha256 2151b611…4438`, `tsa_crt_sha256 8bfb0305…3467` = `sha256sum` de `sceau/chain/*`.
- Puce de révision, point (v) : annexe D sha `deb64179…0eaf` à `e586c0b`, `245cbe0`, `3be95be`, HEAD ; dernier changement
  `e586c0b` ; 16 lignes en D.1, 12 points en D.2. Exact.

### Contrôle 3 — gardes seules

- Avant : `find s2-harness -name __pycache__` → `s2-harness/tests/__pycache__` seul (préexistant, 1 fichier
  `__init__.cpython-311.pyc` du 2026-10-02 04:36:57 UTC, ignoré par `.gitignore` l.33, hors des chemins gardés ; observation,
  pas un constat) ; `SHOGEN_S2_CAMPAGNE_CONTROL` absente ; `g2-p4/journaux-vide/` créé vide ; ni `g2-p4/essai` ni `.essai.*`.
- 01:14:37 UTC, depuis la racine du dépôt : `env -u SHOGEN_S2_CAMPAGNE_CONTROL PYTHONDONTWRITEBYTECODE=1 python3 -B
  s2-harness/tools/rendu_unique.py --depot . --paquet docs/adr-0028/PAQUET-PREREG-S2.md --journaux g2-p4/journaux-vide
  --sommes scratchpad/sceau/SHA256SUMS-cloture-2026-09-28.txt --sortie g2-p4/essai --auteur claude-opus-5-5 --gardes-seules`
  (chemins absolus) → **rc 2**, stdout vide, stderr :
  - `refus (3) : non évaluée (FileNotFoundError : … journaux-vide/control.jsonl)` — le contrôle du sha du fichier de
    sommes contre `sommes` du bloc est donc passé avant (g3, l.180-181) ;
  - `refus (5) : T_now 2026-10-03T01:14:37Z < T0 + 24 h (T0 : 2026-10-03 01:04:10+00:00)` — T0 = genTime du jeton : voie
    (a) établie, (6) levée ; (1), (2), (4), bloc, auteur, sortie levés.
- Après : ni `essai` ni `.essai.*` ; `journaux-vide` toujours vide ; `find s2-harness/shogen_s2 s2-harness/tools -name
  __pycache__` vide ; seul `s2-harness/tests/__pycache__` (inchangé). **Conforme : seuls (3) et (5), rien d'écrit.**

### Contrôle 5 — rejeux au gel

- Diff JSON récursif (script Python, `json.load` des deux côtés, comparaison par chemin et par type) :
  - `oracle4-6564c0f.json` → `oracle4-f35a70c.json` : **3 différences**, toutes d'identité : `/blob_r1`
    `7ae940ec…` → `95c93d37…`, `/commit_r1` `6564c0fd…` → `f35a70c1…`, `/sha256_r1` `79186890…` → `0a16e5de…` ;
    `egalites_total` 320, `cas` (8) égaux.
  - `garde_niveau_oracle_r1-6564c0f.json` → `…-f35a70c.json` : **3 différences**, les mêmes trois champs ; `T0_cas` 20,
    `T1_invariants` 260, `T3_replications` 2 367, `T3_P_more_egaux_a_l_identique` 378, écarts relatifs, `script_sha256`
    et `sha256_json` égaux (valeurs synthétiques).
- Champs d'identité recalculés : `git rev-parse f35a70c:s2-harness/shogen_s2/r1.py` = `95c93d37…` ; `git show … | sha256sum`
  = `0a16e5de…f2cc7f` ; idem à `6564c0f` (`7ae940ec…`, `79186890…5e`). Exacts.
- `sha256sum -c docs/adr-0028/sim-niveau/SHA256SUMS` : les deux lignes ajoutées par la partie (`2ce3a4b9…` oracle4-f35a70c,
  `97b3f13b…` garde-f35a70c) **OK**, ainsi que les 11 autres fichiers présents ; rc 1 à cause de **11 lignes antérieures
  à la partie** (présentes à `b254b89`, 21 lignes) qui nomment des fichiers jamais versionnés (`execution-B/*`,
  `oracle-1b/*`, `oracle-4a-4b/*`, `sim_niveau.log.txt` ; `git log --all --diff-filter=A` vide). Hors du périmètre de la
  partie 4 : observation O-2 (pas un constat de la partie).
- **Rejeu indépendant sur ma copie** (01:32:18 → 01:33:03 UTC), Python 3.13.14 comme au gel (JOURNAL l.302), `env -u
  SHOGEN_S2_CAMPAGNE_CONTROL PYTHONDONTWRITEBYTECODE=1 python3.13 -B`, depuis `arbre/scripts/sim/` :
  `sim_niveau_oracle4.py --r1 arbre/s2-harness --commit f35a70c… --sortie g2-p4/oracle4-rejeu.json` → rc 0 ;
  `sim_garde_niveau_oracle_r1.py --r1 arbre/s2-harness --commit f35a70c… --json arbre/docs/adr-0028/sim-niveau/garde_niveau.json
  --sortie g2-p4/garde-rejeu.json --processus 4` → rc 0. `cmp` : **identiques à l'octet** aux enregistrements versés
  (`2ce3a4b9…`, `97b3f13b…`). Les champs d'identité sont calculés sur les octets de `r1.py` (l.43-44 et l.170-171 des
  scripts), sans git.
- Non-régression des outils versés en P2, sur ma copie : `scripts/controle/regle_fixtures.py` → rc 0, JSON
  `ea3a2d94ef1075603e8f7cfc53c68b26e51729b61714028e3fb03dc32f79cb29` (= README des outils) ; `render_fixture.py` → rc 0,
  `sans_option` `4e62fbb8a4a7a29c…`, `avec_option` `d079dd9d62a3f585…` (= épingles). 0 `__pycache__`.

### Contrôle 7 (a) — suite sur ma copie

- Copie : `git archive HEAD | tar -x -C g2-p4/arbre --exclude=docs/rapports --exclude=docs/adr-0025
  --exclude=docs/adr-0028/monark-m009a --exclude=JOURNAL.md --exclude=biblio` → rc 0, 415 fichiers, chemins exclus
  absents, 0 `*.jsonl`. Aucun test ne lit un chemin exclu (`grep` des tests : seuls des `JOURNAL.md` de dépôts-fixtures).
- 01:16:02 UTC : `cd arbre/s2-harness && env -u SHOGEN_S2_CAMPAGNE_CONTROL PYTHONDONTWRITEBYTECODE=1 python3 -B -m
  unittest discover -s tests -t .` (Python 3.11.15) → **rc 0, `Ran 398 tests in 50.921s`, `OK (skipped=2)`**, 53 s.
- Même commande avec `-v` (forme de l'enregistreur) : rc 0, 396 `ok`, 2 sautés = les deux tests nommés de D.4 a
  (`(ii)` et `(ii bis)`, « SHOGEN_S2_CAMPAGNE_CONTROL absente … NON exécuté ») ; 0 `__pycache__` dans la copie.
- Concorde avec JOURNAL l.300 (« suite 398 OK ») ; **ne concorde pas** avec la procédure §4 l.62 (`Ran 383 tests`) :
  constat B-1.
- Même suite **dans l'environnement du run `suite` de production** (`SHOGEN_RENDU_PRODUCTION` posée sur un répertoire
  `g2-p4/.rendu-essai.XXXX`, comme `produire_tout` l.437 la pose avant `orc.enregistrer`) : rc 0, `Ran 398 tests`,
  `OK (skipped=2)`, 396 `ok`. Le test de refus de `--produire` retire bien le jeton hérité
  (`test_rendu_production.py` l.169) ; aucun autre test n'en dépend. Répertoire temporaire retiré.

### Contrôle 7 (b) — `cargo --locked xtask verify`

- Lancé sur le **dépôt réel** (01:19:54 → 01:21:30 UTC), `CARGO_TARGET_DIR=g2-p4/target-xtask` (rien écrit dans le
  dépôt), sortie standard passée **avant écriture** dans un filtre `awk` (`g2-p4/filtre.awk`) qui retire les lignes
  d'extrait (`      | …`), les motifs des lignes VIOLATION et toute note qui nommerait un chemin de D.2 ; stderr (journal
  de compilation, 22 lignes) à part.
- Résultat : **rc 0 ; 0 ligne VIOLATION ; « VERDICT GLOBAL : VERT »** ; S-G1 (14/14), S-G2 (14/14), S-G3 (12/12), S-G4
  (105/105), S-G5 (106/106 ; 281 fragments contrôlés), S-G6 (129/129), S-G7a (2/2), S-G8 (1/1) VERT ; `cargo fmt --check`,
  construction `no_std`, `clippy -D warnings` VERT ; filtre : 0 ligne d'extrait retirée.
- Écart déclaré : S-G4 et S-G5 balaient `docs/**/*.md`, donc le **programme** a lu les fichiers de `docs/rapports/` et
  `docs/adr-0025/` ; rien n'en a été affiché ni écrit (0 extrait, 0 violation).

### Contrôle 4 — procédure d'exécution

- Gardes, suite, sceau, dossier parent `docs/adr-0028/execution/` (suivi, présent) : exécutables tels qu'écrits sur cet
  hôte (contrôles 1, 3, 7). Hôte : Python 3.11.15 (`/usr/local/bin/python3`), OpenSSL 3.0.13, `python3.13` présent.
- **Limite rencontrée (item à former, règle PAROXYSME)** : le téléchargement des journaux (§2, `curl -L
  'https://drive.usercontent.google.com/download?id=<id>&export=download&confirm=t'`) n'a **pas** pu être éprouvé par
  moi : l'essai sur le seul fichier permis (fichier de sommes, id `1bA3bmuU…`, écrit dans `g2-p4/`, comparaison par
  empreinte) a été **refusé par le système de permissions** ; je ne l'ai pas contourné. Aucune entrée JOURNAL
  sélectionnée n'atteste ce mécanisme sur cet hôte (l.252 : fichier de sommes « lu par l'orchestrateur », moyen non
  dit ; l.278 : métadonnées seules). Voir constat B-3.
- Une lecture de `enforcement/lint-model-pinning.sh` (liste blanche de `--auteur`) a aussi été refusée ; non poursuivie.
  L'admission de `claude-opus-5-5` est établie au premier degré par le contrôle 3 (aucun refus « auteur »).

- Suite de la procédure, lue contre le code et l'hôte :
  - §3 (production « en tâche de fond ») : durées mesurées sur synthétique **sur cet hôte** par R-B (§5, l.202-220) :
    `j14-second` 49-55 s, `j14-principal` 62-66 s, `j28` 117-125 s, `recalcul-tiers` 402-442 s, `raw` 12,6 s (petit
    fichier) ; ma suite : 50-53 s. Total attendu ≈ 13 à 15 min (raw réel de 204 Mo non mesuré). L'outil de commandes de
    l'hôte arrête une tâche de fond à son `timeout` (défaut 30 min, maximum 2 h) et borne le premier plan à 10 min
    (documentation de l'outil, [lu]). Constat B-2.
  - §4 (`--verifier … --commit <HEAD>`) : `oracle_record.verifier` compare la chaîne telle quelle à `tree.commit`
    (l.213), que `rendu_unique` remplit avec la tête résolue au lancement (l.438, `c["head"]`). Constat C-2.
  - §4 (compte de la suite) : constat B-1.
  - §2 (journaux) : constat B-3.
  - Garde (2), (4) : HEAD de l'exécution sera postérieure (commits de documents) ; code identique attendu ; rien à
    signaler. Extraction de l'enregistreur : 428 entrées, toutes `100644` (ni lien ni sous-module : le filtre `data` de
    `tarfile` ne refusera rien), archive de 7 147 520 octets.
  - Aucune « bombe à retardement » : les tests de garde et de sceau travaillent sur des dépôts-fixtures, horloges
    relatives ou injectées (`grep` de `datetime.now`, `SCEAU`, `PAQUET` dans `tests/`).
  - Signature : 25 commits du périmètre sur 25 portent `gpgsig` (SSH) (paquet §12 pt 16).

### Lot CORR — les commits sont-ils les diffs relus ? (sans refaire la relecture)

- Chaîne linéaire `19eb912 → 02f9c00 → 4002239 → 35cd2e2 → 4c831b8 → e4bc2f1 → a5a9de9 → f35a70c` ; aucun de ces commits
  ne touche `JOURNAL.md` ; fichiers changés `19eb912..f35a70c` : 6 modules (`lm`, `r1`, `r2`, `records`, `report`,
  `rendu_unique`) et 10 fichiers de tests ; ni `model.py` ni `oracle_record.py`.
- `git show --numstat` par commit = table du rapport G2 du lot (`docs/G2-lot-CORR.md` l.36-41) et diff K (l.445),
  fichier par fichier : corr-1 +94/−1, corr-2 +142/−2, corr-3a +122/−0, corr-3b +37/−6, corr-3c +26/−15 (sans
  `model.py`, décision Q-5), corr-3d +23/−4, K +19/−0 (`test_prix_non_fini.py` 10, `test_r2.py` 9). **7/7 égaux.**
- sha256 (16 car.) des modules à `f35a70c` = ceux de l'arbre corrigé relu (`docs/G2-lot-CORR.md` l.83-85) :
  `rendu_unique.py` `06d189cf84e7dca9`, `r1.py` `0a16e5defb7c373c`, `r2.py` `e9d9825cbf90f1b1`, `lm.py` `33943649fa2cd57f`,
  `report.py` `95aa549e6a8340b3`, `records.py` `a2e9a7744d8d60a0` (**6/6**) ; `model.py` blob `7264d3fe…` (= `ed479c5`),
  `oracle_record.py` blob `056733b5…` inchangé depuis `19eb912`.
- **Limites** : (i) l'égalité *à l'octet* des commits et des fichiers `corr-*.diff` (`8dd27415`, `0847c663`, `c6580375`,
  `c0043861`, `85ee60e4`, `d19ee0a8`, `aae3daa6`) n'est pas vérifiable par moi : ces fichiers sont hors du dépôt
  (hors de mon périmètre de lecture) et produits par `diff -u` (en-têtes de répertoires, `docs/G2-lot-CORR.md` l.283),
  donc non régénérables depuis git ; l'identité est établie au niveau des comptes par fichier et des empreintes des
  modules, pas des tests à l'octet ; (ii) la **ligne CORR de l'annexe A** n'a pas pu être lue : ma commande (diff de
  l'annexe A dans le périmètre) a été **refusée par le système de permissions** ; je ne l'ai pas contournée. Les
  empreintes que cette ligne porte ne sont donc pas comparées par moi. Item à former (voir « Limites »).

### Contrôle 6 — traçabilité

- `JOURNAL.md` : +32 lignes dans le périmètre, ajouts seuls, en fin de fichier ; nombre de lignes du fichier après
  chaque commit (sans contenu) : 274 à `b254b89`, puis +2 à chacun des 16 commits `18cbfb6`, `931854c`, `9574739`,
  `e586c0b`, `35a601e`, `5f6dcb6`, `eb71f5a`, `e298b9e`, `f6c5d83`, `1f74183`, `e25d840`, `19eb912`, `638f914`,
  `972612a`, `2d51940`, `b7a1b4a` → entrées l.276 à l.306. l.278-306 lues (sélection) et concordantes avec le sujet de
  chaque commit ; l.276 (`18cbfb6`, ouverture de la partie) hors de la sélection, non lue (règle du brief).
- Sans entrée JOURNAL propre : les 7 commits CORR (tous cités par sha dans l.300 ; ligne CORR de l'annexe A non lue,
  limite ci-dessus), `245cbe0` (paquet révisé ; cité 24 fois par `CP1-BREF-REVISION-2026-10-03.md`, décrit par l.304),
  `3be95be` (paquet final ; cité par l.304 et le README du sceau l.9).
- R-13 : 57 fichiers ajoutés ou modifiés (hors `JOURNAL.md`) ; `TODO`, `FIXME`, `XXX` dans les lignes ajoutées : **0**.
- Annexes : `git diff --numstat b254b89 HEAD` → A +1/−0, B +98/−0, D +15/−0 (ajouts seuls).
- Empreintes des pièces citées par l'annexe B, recalculées : avis du seuil `513941d0…` (B.39), inventaire `2a22f47d…`
  (B.40), R-C `f06a69f0…` (B.41), R-B `894ed219…` (B.42), R-A `d2fdd8cc…` (B.43), G1 du lot CORR `1849053c…ac56` et G2
  `96210705…680c` (B.44) : **toutes égales**.
- B.39 : la citation de l'amendement (460 caractères) figure telle quelle dans l'avis ; D.3 (j) (annexe D l.198-211) est
  recopiée à l'identique de l'avis §5 (contrôle ligne à ligne) ; limites L1-L10 de l'avis §4 toutes disposées (items
  FLUX-QUASI-MORT-2, FLUX-DEVIANT-1, FLUX-FAIBLE-1, POOL-MIN-1 ; L4, L5, L7-L10 traitées dans l'avis ou par l'item -1).
- B.40 : neuf modules et lacunes G-1 à G-4 conformes à l'inventaire ; « constat annexe » : `git rev-list --count
  0711cc1..86a8a5b` = **33** (le G2 de la partie 3 l.13 dit 28) : exact.
- B.41 : R-C B-1 → SHOGEN-RAW-CHEMIN-1 ; C-1 → procédure ; C-2, C-3 → SHOGEN-TESTS-C8-SUITE-1 ; C-4, C-5 sans suite ; H-1 →
  SHOGEN-RENDU-MKDTEMP-1 + dossier créé ; H-2 observation ; mutants 37/31/6 (4 équivalents, M29 compris) : conforme.
- B.42 : R-B A-1, B-1, B-2, C-2, C-3, C-4 disposés ; **C-1 et §8 pt 7 sans disposition** (constats C-4 et B-4).
- B.43 : R-A A-1 (I-1), C-2 (I-2) disposés ; **I-3 « note à PX-Shogen-13 » annoncée, contenu absent du dépôt** (C-4).
- B.44 : onze items fermés, cinq formés (L-1, L-2, L-5, L-6, C-5) : conformes au G0 « Adjudication » (Q-2, Q-5) et aux
  commits ; L-3 fermé sans code ; sorties FM-1.1 `corr-worker.json` (941 événements = G0 l.73) et `g2-corr.json` (535 =
  B.44) versées.
- cp-1 bref (`CP1-BREF-REVISION-2026-10-03.md`) : ACCEPTE-AVEC-CORRECTIONS, C-1 seule ; **appliquée mot pour mot** :
  remplacer, dans le paquet de `245cbe0`, le « texte actuel » de son §11 (l.114) par le « texte proposé » (l.120) donne
  exactement le paquet de HEAD (`3be95be`, `numstat` 1/1). FM-1.1 du validateur : `validateur-revision.json`, 115
  événements, 0 fragment.
- Sorties FM-1.1 versées (8) : 0 fragment de la l.51 ni de la l.14, en résultats comme en entrées, dans les huit.
  Contrôles FM-1.1 de la partie 4 **non versés** : advisor (B.39, 72), lecteur (B.40, 280), R-C (B.41, 448), R-B (B.42,
  637), R-A (B.43, 721) ; et B.42 « 637 » = compte de B.35 l.507 et de `g2p3.json` (partie 3) : constat B-5.
- Errata déclarés dans la partie : `e25d840` (heure de l'extension CORR-3, JOURNAL l.296) ; B.44 déclare que le journal G1
  du lot décrit encore la retouche retirée de `model.py` et l'ancien sha de `corr-3c.diff`. Aucun autre écart de date
  trouvé : heures des ajouts datés (00:44:44, 00:48:08, 00:49:47, 01:02:51, 01:04:33) comprises entre les commits qui
  les précèdent et ceux qui les portent.

## Constats

Classes : **A** touche la décision ou peut laisser l'exécution sans sortie (brief) ; **B** à corriger avant l'exécution
unique (ou avant le cp-2 quand c'est dit), sans valeur fausse possible ; **C** rédaction ou traçabilité mineure.

### A — aucun

Sceau, bloc machine, gardes, rejeux au gel, identité du lot CORR (au niveau mesurable), gates et suite tiennent. Aucun
défaut trouvé ne touche la règle (§10.2 à l'octet, bloc recalculé) ni ne laisse, à coup sûr ou par un défaut de code,
l'exécution sans sortie.

### B

**B-1 — compte attendu de la suite périmé** (`docs/adr-0028/PROCEDURE-EXECUTION.md` l.62-63, §4, SHOGEN-CI-S2-SAUT-1).
Texte : « la sortie du run `suite` doit finir par `Ran 383 tests` et `OK (skipped=2)` ». Mesuré à HEAD (code de
`f35a70c`) : **`Ran 398 tests`, `OK (skipped=2)`** (trois passages sur ma copie : forme du brief, forme `-v` de
l'enregistreur, et avec `SHOGEN_RENDU_PRODUCTION` hérité) ; JOURNAL l.300 dit déjà « suite 398 OK » ; 383 était le compte
de `931854c` (JOURNAL l.280). L'ajout daté de 01:04:33 (l.75) ne le met pas à jour. Suivie à la lettre, la procédure
produit un écart **certain** au §4 (« constat au JOURNAL, examiné avant toute lecture des rendus ») : le contrôle ne
discrimine plus un saut silencieux réel. Aucune valeur touchée ; la production a lieu.

**B-2 — mode de lancement de la production non fixé face aux bornes de l'outil** (PROCÉDURE l.50, §3 : « lancée en
tâche de fond (délai par commande : 3 600 s, `DELAI_DEFAUT`) »). Sur l'hôte cloud, l'outil de commandes arrête une
tâche de fond à son `timeout` (défaut 30 min, maximum 2 h) et borne le premier plan à 10 min. Durée attendue (R-B §5,
synthétique, même hôte) ≈ 13 à 15 min, `raw` réel non mesuré : marge ≈ ×2 sous le défaut ; le coût réel dépend des
données (R-B §5). Si la borne est atteinte : processus arrêté pendant un run, `finally` (l.455-461) non exécuté,
débris `.rendu-<date>.*` ; si l'arrêt tombe entre `os.mkdir(cible)` (l.447) et `os.rename` (l.449), une réserve vide
`rendu-<date>` reste, que `destination` (l.352-353) prend pour une première exécution (« déjà présent … --deviation »),
cas que la procédure §3 l.53-54 ne nomme pas. Aucune sortie ; tentative à refaire (pas une seconde exécution, §3).
La borne des tâches de fond est déjà connue du projet (annexe B l.277, SHOGEN-HARNAIS-TACHE-10MIN-1). Classé B et non A :
conditionnel (durée > 30 min), levable sans code, recommençable.

**B-3 — étape de téléchargement non éprouvée et références manquantes** (PROCÉDURE l.30-39, §2). (i) Le téléchargement
`curl -L 'https://drive.usercontent.google.com/download?id=<id>&export=download&confirm=t'` n'est attesté sur cet hôte
par aucune entrée JOURNAL que j'ai pu lire (l.252 : fichier de sommes « lu par l'orchestrateur », moyen non dit ; l.278 :
métadonnées seules) ; mon essai sur le seul fichier permis a été refusé par le système de permissions (limite L-1) :
rien n'établit que ce moyen (partage du dossier, mandataire sortant, page de confirmation au-delà de 100 Mo) aboutit.
(ii) l.33 renvoie aux « ids notés au JOURNAL du 2026-10-02 21:2x UTC » : les entrées de 21:2x que j'ai lues (l.278,
l.280, l.282, l.284) ne portent aucun identifiant de fichier, seulement noms et tailles (l.276, de 21:1x, hors de ma
sélection, non lue). (iii) l.36-39 : tailles attendues données, mais aucune conduite si une taille diffère ; un
transfert tronqué produirait un écart de sha256 que l.39 envoie à « arrêt, ligne de JOURNAL, question à
l'investisseur » au lieu d'un nouveau téléchargement. Effet : blocage au §2, aucune exécution, aucune valeur fausse.

**B-4 — limite rendue par R-B non formée : concordance des clés porteuses R2** (`docs/adr-0028/ANNEXE-B-items.md` B.42
l.586-599, contre `docs/adr-0028/G2-RATTRAPAGE-R-B.md` §8 pt 7, l.267-268). La limite « concordance des clés porteuses
R2 sur les `run_params` du `control.jsonl` réel (les tests D.4 a ne contrôlent que les clés R1) » n'est ni formée en
item ni disposée (aucune autre mention dans `docs/`, `grep -rl` exclusions D.2 à la source). Mécanisme : 
`records.effective_run_params` (l.143-199) refuse des clés porteuses absentes ou divergentes entre démarrages
(fail-closed voulu, §E) ; il reçoit `R2_LOAD_BEARING_KEYS` (l.73-77 : `flux_hosts`, sept paramètres `content_*` et
`tick_rule`) sur les chemins R2 (`r2.py` l.1066-1072 ; blocs 5-6 du rendu) : les runs `j14-*`, `j28` et
`recalcul-tiers` échoueraient et l'exécution unique ne laisserait aucune sortie (aucune valeur fausse). Plausibilité
très faible [inféré] : à `ed479c5`, `collector.py` l.208-216 écrit les neuf clés depuis des constantes de `r2` et les
specs ; la collecte est déclarée sur ce seul commit (paquet §1) ; les clés R1 issues des mêmes specs (`pool`,
`sigma_class_of_flux`) sont contrôlées concordantes par les tests nommés de D.4 a [2nd]. C'est la garde qui jouerait son
rôle ; ce qui manque est la disposition écrite (règle PAROXYSME), donc la conduite pré-écrite si elle refuse.

**B-5 — contrôles FM-1.1 de la partie 4 non rejouables** (`scripts/controle/README.md` l.20-23, `sorties-fm11/` ;
annexe B.39-B.43). Les sorties FM-1.1 des cinq transcriptions de rôles frais antérieures au lot CORR ne sont pas versées
— advisor du seuil (B.39 l.551, 72 événements), lecteur de l'inventaire (B.40 l.566, 280), R-C (B.41 l.570, 448), R-B
(B.42 l.586, 637), R-A (B.43 l.603, 721) — alors que celles de `corr-worker`, `g2-corr` et `validateur-revision` le
sont. SHOGEN-FM11-VERIFIABLE-1 est dit « traité » en P2 (JOURNAL l.278) mais son principe (annexe B l.520 : verser les
sorties « pour qu'un réviseur puisse les relire ») n'est pas appliqué à ces cinq contrôles, dont celui de l'auteur du
seuil (attestation D.3 (j)). En outre, B.42 attribue à R-B **637** événements, exactement le compte que B.35 (l.507)
attribue au réviseur G2 de la partie 3 et que porte `g2p3.json` : coïncidence ou recopie, indécidable sans la sortie de R-B.

### C

**C-1 — README du dossier d'exécution périmé** (`docs/adr-0028/execution/README.md` l.3-6) : « `tempfile.mkdtemp`,
`rendu_unique.py` l.426) hors de son `try` ; un dossier parent absent ferait échouer la production après les gardes,
sans ligne « échec de production » » — faux depuis `4c831b8` (CORR-3b, SHOGEN-RENDU-MKDTEMP-1 fermé en B.44) :
`mkdtemp` est l.431, dans le `try` ; un parent absent donne « échec de production », code 1. Le dossier reste requis.

**C-2 — `--commit <HEAD>` ambigu** (PROCÉDURE l.59) : `verifier` compare la chaîne telle quelle à `tree.commit`
(`oracle_record.py` l.213) ; il faut le sha complet de la tête notée au §1 (celle que `rendu_unique` enregistre, l.438),
ni `HEAD` littéral, ni une tête postérieure aux commits de JOURNAL du §4 (sinon « refus (tree.commit) »).

**C-3 — `--auteur claude-opus-5-5` écrit en dur** (PROCÉDURE l.47) : l'enregistrement doit porter l'identifiant exact
du modèle de l'orchestrateur qui exécute (Gate 0 de sa session) ; CLAUDE.md §7 nomme `claude-fable-5-1` pour
l'orchestrateur, la session cloud tourne sous `claude-opus-5-5` (annexe D.1 n° 15).

**C-4 — deux limites des rattrapages sans trace écrite** : (i) R-B C-1 et §8 pt 4, l.263 (« précédence D-4 non écrite au
paquet ; à citer au rapport avec le drapeau 2 si le cas se présente ») : citée en B.42 l.591 sans item ni « sans
suite » ; (ii) R-A I-3 : B.43 l.606 annonce une « note à PX-Shogen-13 » dont le contenu (« τ observé … et le P99 de
calibration … ne portent pas sur la même population », R-A l.251-252) n'est écrit nulle part dans le dépôt
(PX-Shogen-13 vit dans le registre hors dépôt, D.2 n° 10).

**C-5 — renvoi inexact dans l'ajout daté du plan** (`docs/adr-0028/PLAN-PARTIE-4.md` l.33) : « (la commande de garde
(2) du §1 se lit avec ce commit à la place de `41f087e…`) » : le §1 du plan ne porte aucune commande de garde (2) ; c'est
le §1 de la procédure (l.18-19).

### Observations (aucune correction demandée)

- **O-1** `s2-harness/tests/__pycache__/` préexistant (2026-10-02 04:36:57 UTC ; R-C H-2) : hors des chemins gardés,
  inchangé par moi.
- **O-2** `docs/adr-0028/sim-niveau/SHA256SUMS` : 11 lignes antérieures à la partie nomment des fichiers jamais
  versionnés ; `sha256sum -c` sort 1. Hors période ; une ligne de README ou un item lèverait l'ambiguïté.
- **O-3** Brief, contrôle 1 : `git diff ddf8c54 HEAD -M --stat -- docs/adr-0028/sceau` ne montre que des créations (à
  `ddf8c54` le dossier ne portait que `chain/`) ; la preuve d'octets inchangés est `git log -M --name-status
  ddf8c54..HEAD -- docs/adr-0028/sceau` (R100 à `972612a`), plus la vérification hors ligne sur copie (faites).
- **O-4** Plan et procédure gardent, par la convention d'ajout, l'ancienne échéance (procédure l.10, plan l.5 et l.20),
  l'ancien sha (procédure l.3, plan l.7) et l'ancien commit d'analyse (procédure l.18) ; seuls les ajouts datés finaux
  les remplacent. Les gardes (2) et (5) refuseraient une exécution qui suivrait les anciennes valeurs : risque de
  lecture seulement.
- **O-5** Hôte : OpenSSL 3.0.13 (D.4 c citait 3.5.7, hôte Windows de l'époque) ; vérification conforme.

## Verdict : **ACCEPTE-AVEC-CORRECTIONS**

Aucun constat A. Le sceau (second et premier), le bloc machine recalculé, les gardes (seules (3) et (5)), les rejeux au
gel (diff JSON et rejeu indépendant à l'octet), l'identité du lot CORR (comptes par fichier et empreintes des modules),
la règle et les épingles, la suite (398, `OK (skipped=2)`) et `xtask verify` (0 VIOLATION) tiennent. La procédure
d'exécution n'est pas exécutable telle qu'écrite sans les ajouts K-1 à K-4 : B-1 fait échouer à coup sûr un contrôle du
§4, B-2 et B-3 laissent ouverts deux chemins d'échec sans sortie ou de blocage. **K-1 à K-4 et K-7 sont à appliquer
avant l'exécution unique** ; K-8 avant le contrôle FM-1.1 de l'exécution (au plus tard avant le cp-2) ; K-5 et K-6 à
la clôture de la partie au plus tard. Aucune correction ne touche les octets scellés, le bloc ni le code gelé : toutes
sont des ajouts datés (convention des pièces), en fin de fichier.

### Liste fermée des corrections

Format : fichier ; ligne ; texte actuel (conservé) ; texte proposé (nouvelle ligne en fin de fichier, heure produite par
le script d'écriture).

**K-1 (B-1)** — `docs/adr-0028/PROCEDURE-EXECUTION.md`, après l.75 ; texte actuel l.62 : « - SHOGEN-CI-S2-SAUT-1 : la
sortie du run `suite` doit finir par `Ran 383 tests` et `OK (skipped=2)` (les deux tests » ; texte proposé :

> *Ajout daté du <date -u> (relecture G2 de la partie 4, B-1 ; lignes ci-dessus conservées)* : au §4, le run `suite` doit finir par `Ran 398 tests` et `OK (skipped=2)` (suite du commit d'analyse `f35a70c` : 396 tests verts, les deux tests nommés de D.4 a sautés, variable absente ; mesuré le 2026-10-03 sur une extraction de `b7a1b4a`, avec et sans `SHOGEN_RENDU_PRODUCTION` posée) ; `383` était le compte de `931854c`. Tout autre compte reste un constat au JOURNAL, examiné avant toute lecture des rendus.

**K-2 (B-2)** — même fichier, après l.75 ; texte actuel l.50 : « - Même commande **sans** `--gardes-seules`, lancée en
tâche de fond (délai par commande : 3 600 s, `DELAI_DEFAUT`). » ; texte proposé :

> *Ajout daté du <date -u> (relecture G2 de la partie 4, B-2)* : au §3, la production n'est lancée ni au premier plan de l'outil de commandes (borne de 10 min) ni en tâche de fond à son délai par défaut (30 min) : soit détachée (`setsid nohup env -u SHOGEN_S2_CAMPAGNE_CONTROL PYTHONDONTWRITEBYTECODE=1 python3 -B s2-harness/tools/rendu_unique.py … > <scratchpad>/execution/production.log 2>&1 &`, PID et heure écrits au JOURNAL, fin attendue en sondant le PID et ce fichier), soit en tâche de fond avec un délai explicite de 7 200 000 ms. Durée attendue d'après R-B §5 (synthétique, même hôte) : 13 à 15 min. Après toute interruption (borne atteinte, redémarrage de la machine), consigner puis retirer à la main les débris `.rendu-<date>.*` et, s'il existe et est vide, le répertoire `rendu-<date>` (réserve de `rendu_unique.py` l.447) ; ce n'est pas une seconde exécution.

**K-3 (B-3)** — même fichier, après l.75 ; texte actuel l.33-34 : « - Téléchargement des trois fichiers du dossier Drive
`1TwP2Jtc0-_gAYjDOHHpvfh3XxnR6jtR6` (ids notés au JOURNAL du 2026-10-02 21:2x UTC) par `curl -L …` » et l.38-39
(« Un écart : arrêt, ligne de JOURNAL, question à l'investisseur. ») ; texte proposé :

> *Ajout daté du <date -u> (relecture G2 de la partie 4, B-3)* : au §2, (i) avant le go, le moyen de téléchargement est éprouvé sur le seul fichier de sommes (id `1bA3bmuUZn0XCljRH7GIE54RjMsRI5q9Q`, écrit hors du dépôt, sha256 attendu `70910984076474987239d8c7a9da786acc95c38b375ad572d78afa297bf8caf4`), jamais sur un journal ; code HTTP, taille et sha256 écrits au JOURNAL ; (ii) les identifiants Drive des trois journaux sont écrits dans cet ajout, ou l'entrée du JOURNAL qui les porte est citée par son numéro de ligne (les entrées de 21:2x, l.278 à l.284, n'en portent pas) ; (iii) chaque fichier est téléchargé avec `curl --fail -L` ; sa taille est comparée d'abord : une taille différente est un transfert incomplet, refait et consigné ; seul un sha256 différent à taille égale est l'écart qui arrête l'exécution et va à l'investisseur.

**K-4 (C-2, C-3)** — même fichier, après l.75 ; textes actuels l.59 (« `--commit <HEAD>` ») et l.47 (« `--auteur
claude-opus-5-5` ») ; texte proposé :

> *Ajout daté du <date -u> (relecture G2 de la partie 4, C-2, C-3)* : au §4, `--commit` reçoit le sha complet (40 caractères) de la tête notée au §1, celle que porte `tree.commit` de l'enregistrement, jamais `HEAD` littéral ni une tête postérieure aux commits de JOURNAL du §4 ; au §3, `--auteur` reçoit l'identifiant exact du modèle de l'orchestrateur qui exécute (Gate 0 de sa session), pris dans la liste blanche du lint.

**K-5 (C-1)** — `docs/adr-0028/execution/README.md`, après l.7 ; texte actuel l.3-6 (« … `rendu_unique.py` l.426) hors de
son `try` ; un dossier parent absent ferait échouer la production après les gardes, sans ligne « échec de production »
… ») ; texte proposé :

> *Ajout daté du <date -u> (relecture G2 de la partie 4, C-1 ; lignes ci-dessus conservées)* : depuis `4c831b8` (lot CORR, CORR-3b ; SHOGEN-RENDU-MKDTEMP-1 fermé, annexe B.44), `mkdtemp` est dans le `try` de `produire_tout` (`rendu_unique.py` l.431) : un dossier parent absent donne une ligne « échec de production », code 1, rien d'écrit. Le dossier reste requis (procédure §1).

**K-6 (C-5)** — `docs/adr-0028/PLAN-PARTIE-4.md`, après l.33 ; texte actuel l.33 : « (la commande de garde (2) du §1 se
lit avec ce commit à la place de `41f087e…`) » ; texte proposé :

> *Ajout daté du <date -u> (relecture G2 de la partie 4, C-5)* : dans l'ajout précédent, « la commande de garde (2) du §1 » désigne le §1 de `docs/adr-0028/PROCEDURE-EXECUTION.md` (l.18-19) ; le §1 de ce plan n'en porte pas.

**K-7 (B-4, C-4)** — `docs/adr-0028/ANNEXE-B-items.md`, après l.643 ; texte actuel : B.42 l.591 (R-B C-1 sans
disposition), B.42 sans mention de R-B §8 pt 7, B.43 l.606 (« note à PX-Shogen-13 » sans contenu) ; texte proposé
(nouveau bloc) :

> ## B.45 Amendement daté du <date -u> : relecture G2 de la partie 4 (préparation) — limites des rattrapages formées
>
> | item | constat | propriétaire | déclencheur | prix | origine |
> |---|---|---|---|---|---|
> | SHOGEN-R2-RUNPARAMS-CONCORDANCE-1 | clés porteuses R2 (`records.R2_LOAD_BEARING_KEYS`) non contrôlées présentes et concordantes sur les `run_params` du `control.jsonl` réel (les tests nommés de D.4 a appellent `effective_run_params` avec le seul jeu R1) ; une absence ou une divergence fait refuser les chemins R2 (fail-closed voulu, §E) : exécution unique sans sortie, aucune valeur fausse ; plausibilité très faible (collecte sur `ed479c5`, clés écrites depuis des constantes de `r2` et les specs, `collector.py` l.208-216 à ce commit) | orch. | avant l'exécution unique : limite déclarée ; si le refus « run_params divergents » survient, échec de production consigné, aucune correction du code, déviation déclarée (pt 11) | aucun (disposition) [inféré] | R-B §8 pt 7 ; relecture G2 de la partie 4, B-4 |
> | SHOGEN-D4-PRECEDENCE-RAPPORT-1 | pt 10 : la précédence D-4 (cas FAUX avec k_eff non évaluable rendu NON ÉVALUABLE) n'est pas écrite au paquet ; elle est citée au rapport, avec le drapeau 2, si le cas se présente | orch. ; rédacteur du rapport | rapport `docs/11` | une phrase [inféré] | R-B C-1, §8 pt 4 ; relecture G2 de la partie 4, C-4 |
>
> Note à PX-Shogen-13 annoncée en B.43 (R-A I-3), recopiée de `docs/adr-0028/G2-RATTRAPAGE-R-A.md` l.251-252 : « PX-Shogen-13 déclare que τ observé (axe (i) atteint) et le P99 de calibration (`closure.py`, toutes cellules évaluables) ne portent pas sur la même population. »

**K-8 (B-5)** — action et ajout daté : verser dans `scripts/controle/sorties-fm11/` les cinq sorties FM-1.1 de B.39 à
B.43, avec leurs sha256 dans `scripts/controle/SHA256SUMS` ; `scripts/controle/README.md`, après l.23 ; texte actuel l.20
(liste des sorties versées, sans B.39-B.43) ; texte proposé :

> *Ajout daté du <date -u> (relecture G2 de la partie 4, B-5)* : sorties FM-1.1 des contrôles de la partie 4 antérieurs au lot CORR versées : advisor du seuil (B.39), lecteur de l'inventaire (B.40), R-C (B.41), R-B (B.42), R-A (B.43) ; sha256 dans `SHA256SUMS`. Compte d'événements de R-B relu sur sa sortie : <n> (B.42 écrit 637).

Si la sortie de R-B ne compte pas 637 événements : erratum daté en B.42. Si une sortie ne peut plus être produite (transcription
perdue) : l'écrire dans cet ajout, et former SHOGEN-FM11-VERIFIABLE-2 (contrôle non rejouable déclaré).

## Limites rencontrées (rendues comme items à former, règle PAROXYSME)

- **L-1** Essai du moyen de téléchargement du §2 sur le fichier de sommes (`curl` vers Drive, écriture dans `g2-p4/`) :
  **refusé par le système de permissions** ; non contourné. Item : B-3 / K-3 (i) (l'essai revient à l'orchestrateur).
- **L-2** Lecture de la ligne `ALLOWED=` de `enforcement/lint-model-pinning.sh` : **refusée** ; non poursuivie. Admission
  de `claude-opus-5-5` établie par le contrôle 3 ; celle de `claude-fable-5-1` non vérifiée par moi (C-3).
- **L-3** Lecture de la ligne CORR ajoutée à l'annexe A (`git diff b254b89 HEAD -- docs/adr-0028/ANNEXE-A-lots.md`) :
  **refusée** ; non contournée. Ses empreintes ne sont pas comparées par moi ; le cp-1 bref (§4 f, l.47) la dit présente
  à l.130 et cohérente [2nd]. Item : comparaison à faire par l'orchestrateur (ou une instance autorisée).
- **L-4** Identité à l'octet des commits CORR et des fichiers `corr-*.diff` : non vérifiable (fichiers hors du dépôt,
  `diff -u`) ; établie au niveau des comptes par fichier (7/7) et des empreintes des modules (6/6).
- **L-5** JOURNAL l.276 (entrée de `18cbfb6`) hors de la sélection prescrite : non lue.
- **L-6** Je ne peux pas lancer `fm11.py` sur ma propre transcription sans ouvrir, par procuration, deux pièces de D.2 :
  le contrôle FM-1.1 de cette relecture revient à l'orchestrateur.
- **L-7** Effet de bord de l'outil : les deux commandes lancées en tâche de fond ont écrit leur sortie standard (lignes
  `rc_…` et dates seulement) sous `…/7ba84933-ba6d-…/tasks/`, hors de `g2-p4/` (fichiers de l'outil, pas de moi).

## Occurrences de chemins D.2 dans mes appels d'outils

Base : les motifs de `scripts/controle/fm11.py` l.20-24 (sha `886cc676…`).

- **Entrées (mes appels)** : *tout* appel qui cite mon dossier de travail porte le motif `7ba84933-ba6d` (le dossier
  `…/7ba84933-ba6d-5813-9ef4-ca3ac4febd16/scratchpad/g2-p4/` imposé par le brief est un frère de la session de
  l'orchestrateur ; aucun accès à la transcription, D.2 n° 11, ni à aucun autre sous-dossier de cette session, hors
  `scratchpad/sceau/SHA256SUMS-cloture-2026-09-28.txt`, empreintes seulement). Liste détaillée des autres motifs en fin de rapport.
- **Résultats** : la lecture de l'annexe D, du brief et de `fm11.py` affiche des *noms* de pièces de D.2 (motifs
  `cartographie-2026-09-29`, `adr-0025`, `shogen-j28`, `measure-M009a`, `session_013dvmub`, `7ba84933-ba6d`,
  `control.jsonl`, etc.) : noms seulement, aucun contenu.

Détail des **entrées** (arguments de mes appels), par motif de `fm11.py` ou chemin de D.2 / du brief :

| motif ou chemin | appels qui le portent | nature |
|---|---|---|
| `7ba84933-ba6d` | la lecture du brief, l'écriture et toutes les mises à jour de ce rapport, et toutes les commandes qui citent `g2-p4/` ou le fichier de sommes (copies, suites, gardes, `xtask`, rejeux, filtre) | chemin de mon dossier imposé par le brief |
| `SHA256SUMS-cloture` | `sha256sum`/`cat` du fichier de sommes ; comparaison au bloc ; `--sommes` de l'essai des gardes ; textes de ce rapport | fichier permis (empreintes) |
| `adr-0025`, `docs/rapports`, `monark-m009a` | `git archive … --exclude=…` (1) ; `grep -rl --exclude-dir=rapports --exclude-dir=adr-0025 --exclude-dir=monark-m009a` sur `docs/` (3 : `execution-B`, `clés porteuses R2`, `PX-Shogen-13`) ; motifs de recherche dans le code (2 : `s2-harness`/`scripts/sim`, `xtask/src`) ; motif du filtre `awk` de `xtask` (1) ; textes de ce rapport | exclusions, motifs de recherche, noms |
| `JOURNAL.md` | sélection prescrite (`grep -n … \| grep -n …` puis `awk` pour numéros et longueurs, puis `sed -n '<l>p'` ×20) ; `wc -l` ; `--numstat -- JOURNAL.md` et `git show <c>:JOURNAL.md \| wc -l` (comptes) ; exclusions `':!JOURNAL.md'` et `--exclude=JOURNAL.md` ; motifs de recherche dans le code | lignes sélectionnées seulement, sinon comptes |
| `(control\|journal\|raw).jsonl` | textes de ce rapport (noms des lignes du bloc) | noms |
| `cartographie-2026-09-29`, `shogen-j28`, `measure-M009a`, `session_013dvmub` | textes de ce rapport (liste des motifs vus en résultat) | noms |

**Résultats** portant des noms (jamais un contenu) : brief ; annexe D (liste D.2, D.1) ; `fm11.py` ; `.gitattributes`
(nom du dossier `monark-m009a`) ; `git diff --stat` (nom `JOURNAL.md`) ; README des outils ; JOURNAL l.252, l.278 (noms
des journaux, nom du fichier de sommes) ; stderr des gardes (`…/journaux-vide/control.jsonl`) ; fichier de sommes (noms
des journaux) ; résumés des sorties FM-1.1 (noms de motifs) ; cp-1 bref (chemin du brief du validateur, noms de D.2) ;
annexe B, rapports R-A, R-B, R-C, G2 du lot CORR (noms). **Aucun fragment** de la cartographie l.51 ni d'ADR-0025 l.14 :
ces fichiers n'ont jamais été affichés ; le filtre de `xtask` a retiré 0 ligne d'extrait.

## Clôture

- 01:40:38 UTC : copies supprimées (`g2-p4/arbre` 7,0 Mo, `g2-p4/premier-copie`, `g2-p4/target-xtask` 128 Mo,
  `g2-p4/paquet-245cbe0.md`, `g2-p4/journaux-vide`). Restent dans `g2-p4/` : ce rapport, le brief, les sorties de mes
  commandes (`suite*.out`, `gardes.*`, `xtask.*`, `filtre.awk`, `rejeu.*`, `oracle4-rejeu.json`, `garde-rejeu.json`,
  `regle.*`, `render.log`, `rendus-fixture/` (rendus de fixture synthétique), `bloc-journaux.txt`, `fichiers-partie4.txt`).
- Dépôt : `git status --porcelain` vide ; HEAD `b7a1b4a35967d41d36e63187c23da7c48f7997af` inchangée ; 0 `__pycache__`
  sous `s2-harness/shogen_s2` et `s2-harness/tools` ; `s2-harness/tests/__pycache__` inchangé (même horodatage) ;
  `SHOGEN_S2_CAMPAGNE_CONTROL` absente. Aucune opération git en écriture.
- R-13 : aucun marqueur de dette nu dans ce rapport ni dans mes fichiers de travail.
- Le sha256 de ce rapport est donné dans la remise (un fichier ne porte pas son propre sha).
