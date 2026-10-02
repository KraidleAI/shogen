# Journal G1 — partie 3 de S2, lot P3, complément P3g

Journal du même worker que `docs/G1-partie-3-P3.md` (versé, non modifié). Une section datée par complément.

## P3g — SHOGEN-SCEAU-VERIFY-DATA-1 (2026-10-02, 15:25 à 15:3x UTC)

### 1. Gate 0 et cadre

- **Modèle résolu sous lequel le worker a tourné : `claude-opus-5-5`** (identifiant exact fourni par l'environnement de
  la session ; préfixe attendu `claude-opus-5-5` : conforme). Effort : `max`.
- Horloge (`date -u`) : 15:25:46 UTC au départ, 15:29:44 avant la rédaction. Branche `partie-3-paquet`, HEAD `bf51c71`
  (journal de P3 versé, annexe B bloc B.30) au départ ; l'orchestrateur a commis pendant le travail `c32c285` (15:29:38
  UTC, `biblio/INDEX.md`) et `25fc3e2` (15:31:09 UTC, `docs/adr-0028/LECTURES-PARTIE-3.md`) ; `s2-harness/` et
  `scripts/` sont identiques entre `bf51c71` et `25fc3e2` (`git diff --quiet`) : base des diffs `bf51c71`, valable pour
  la tête.
- Rattachement (G0) : message de l'orchestrateur (réponse à Q3 du G1 de P3 : complément P3g) et ligne d'annexe lue avant
  tout code : `docs/adr-0028/ANNEXE-B-items.md` (`6b1ee6a0…` à `bf51c71`), bloc B.30, l.444 (construction :
  `openssl ts -verify -data PAQUET.sha256` à l'étape (2), cas de test ; déclencheur : complément P3g, avant le
  scellement) ; l.440-453 lues (titre du bloc, lignes du bloc, réponses de l'orchestrateur).
- Aucune opération git en écriture sur le dépôt ; dépôts jetables seulement. Fichiers touchés :
  `scripts/sceau/verify.sh` et `s2-harness/tests/test_sceau.py`. Non touchés : `scripts/sim/`, les fichiers du worker de
  l'étape S (`docs/G1-partie-3-S.md`, `scripts/sim/sim_garde_niveau.py`, `scripts/sim/sim_garde_niveau_oracle_r1.py`) et
  `docs/adr-0028/LECTURES-PARTIE-3.md` (vu non suivi à 15:29 UTC, commis par l'orchestrateur à 15:31 UTC ; nom
  seulement).
- Pré-enregistrement : fixtures seulement (D.4 a), autorité RFC 3161 de test, aucun réseau ; aucune pièce de D.2 ouverte
  ni prise dans une recherche ; `SHOGEN_S2_CAMPAGNE_CONTROL` et `SHOGEN_RENDU_PRODUCTION` absentes de l'environnement
  (`env | grep -c` : 0) ; `TMPDIR` sur `<S>/lot-P3/tmp`, où `<S>` est le scratchpad de la session
  (`/tmp/claude-0/-home-user-shogen/7ba84933-ba6d-5813-9ef4-ca3ac4febd16/scratchpad`).

### 2. Provenance

- Sources [lu] : `scripts/sceau/verify.sh` à `bf51c71` (`f4719869…`, 19 lignes, en entier) ;
  `s2-harness/tests/test_sceau.py` à `bf51c71` (`1e4eb264…`, l.28-79) ; annexe B, l.440-453.
- Base contrôlée : export de `bf51c71` (`git archive`) égal à l'instantané P3f du lot (`diff -r` vide sur `s2-harness/`
  et `scripts/sceau/`) ; `docs/G1-partie-3-P3.md` versé égal au journal remis (`b4b12680…`).
- Sondes (`<S>/lot-P3/sondes/`) : `sonde_sceau_data.sh` du G1 de P3 (`e589f2bd…`, sortie `9a93f26d…`) : paquet et
  manifeste réécrits d'accord après le jeton, `verify.sh` sort code 0 ; `sonde_sceau_equivalence.sh` (neuve,
  `867ee8cb…`, sortie `2adf869d…`) : deux requêtes sur le même manifeste (nonces différents), jeton de la TSA de test
  sur la seconde : `-queryfile` de la seconde code 0, de la première code 1 ; `-data` du manifeste code 0 ; `-data`
  d'autres octets code 1.
- Outils (`<S>/lot-P3/outils/`) : `instantane.sh` et `moteur.py` du lot ; liste `mutants_P3g.py` (neuve).

### 3. Construction

- Étape (2) de `verify.sh` : la vérification existante (`-queryfile`) est gardée, et une seconde la suit :
  `openssl ts -verify -in "$D/paquet.tsr" -data "$D/PAQUET.sha256" -CAfile … -untrusted …` ; écart :
  `JETON : ÉCART (manifeste)`, code 3 (contrat de codes inchangé : 2 pour le manifeste, 3 pour le jeton), avant
  l'impression du genTime. En-tête et titre de l'étape nomment la requête et le manifeste.
- En plus, non à la place : l'équivalence ne tient dans aucun sens. `-queryfile` admet un manifeste réécrit après le
  jeton (sonde du G1 de P3) ; `-data` admet le jeton d'une autre requête sur le même manifeste (autre nonce, sonde
  neuve). Les deux ensemble lient le jeton à la requête faite et aux octets du manifeste présent, comme la voie (a) de
  `rendu_unique` (E2 du G1 C-1).

### 4. Tests, échec avant, mutants

- Test neuf `test_verify_lie_le_jeton_au_manifeste` (la sonde du G1 de P3 rendue reproductible) : après le jeton, paquet
  et manifeste réécrits d'accord (une ligne au format de `make-tsq.sh` sur les nouveaux octets) : étape (1) passe
  (`<chemin du paquet>: OK`), code 3, dernière ligne `JETON : ÉCART (manifeste)`, étape (3) jamais atteinte. Mise en
  place commune extraite du test nominal dans l'aide `sceller` (mêmes assertions, dont le format du manifeste).
- Échec avant (`verify.sh` de `bf51c71` ; `preuves/P3g-avant.out`, `71850678…`) : `FAILED (failures=1)`, code 0,
  dernière ligne `SCEAU : VÉRIFIÉ HORS LIGNE …`, étape (3) atteinte ; les deux autres tests verts (l'aide extraite ne
  change rien au nominal). Après : `Ran 3 tests`, `OK` (`e8382d56…`).
- Mutants (`preuves/P3g-mutants.out`, `d1d83ae8…`) : **5 tués sur 5** — G1 seconde vérification retirée, G2 écart
  ignoré, G3 jeton lié à un autre fichier (`paquet.tsq` : tué par le test nominal), G4 vérification placée après
  l'impression du genTime, G5 écart rendu en code 0. Liste P3a rejouée sur l'arbre P3g (`preuves/P3g-rejeu-P3a.out`,
  `9edd2d3f…`) : 8 tués sur 8.

### 5. Comptes et empreintes

- Suite : `Ran 383 tests in 46.490s`, `OK (skipped=2)` (`preuves/suite-P3g.out`, `3bbf8fdd…`) ; départ 382 (fin de P3).
  Règle scellée sur l'instantané P3g : `ea3a2d94…`, identique à l'octet (aucun fichier de `shogen_s2/` touché).
- Diff : `<S>/lot-P3/P3g.diff`, contre `bf51c71`, sha256
  `b817d9b4ad549b8257d5921101ccad57b5d24eac62f9f2ee4a56cc736d2b9fda` ; numstat :
  `s2-harness/tests/test_sceau.py +28 −9`, `scripts/sceau/verify.sh +5 −2` ; total +33 −11 = 44 lignes. Contrôle :
  `patch -p1` sur un export de `bf51c71`, puis `cmp` et `diff -r` contre l'arbre de travail : identiques.
- Fichiers finaux : `s2-harness/tests/test_sceau.py` `44a1640ac304c60b8634766dc8447e00cec4e64945ef0e9bb231d78616273eb0`
  (97 lignes ; base `1e4eb264…`) ; `scripts/sceau/verify.sh`
  `b6f7b66a9a01b053515a0d8f5076d673bc11d76a67ab62b99388b15a1962d166` (22 lignes ; base `f4719869…`).

### 6. Écarts

- **E1** : le test nominal de P3a est restructuré autour de l'aide `sceller` (mise en place partagée avec le test
  neuf) ; ses assertions sont inchangées, et l'assertion du format du manifeste passe dans l'aide, donc dans les deux
  tests.
- **E2** : l'étape (3) imprime toujours l'étiquette `Message data:` sans l'empreinte (lignes suivantes filtrées) ; le
  lien jeton-manifeste est désormais contrôlé par le script, l'affichage n'en est plus la seule trace : sans item.

### 7. Limites et questions

- Aucune limite neuve : la vérification sur la chaîne réelle (FreeTSA) et sous l'OpenSSL de l'hôte relève de
  SHOGEN-P3-HOTE-1 et de SHOGEN-RENDU-HOTE-1 (suite sur l'hôte, `test_sceau` compris). Aucune question.

### 8. Clôture

- `cargo --locked xtask verify` avec ce journal en place et hook pre-commit versionné rejoué dans un clone jetable (diff
  P3g et ce journal indexés) : verdicts et sha256 dans le rapport de remise (un fichier ne porte pas son propre sha).
- `git status` : `scripts/sceau/verify.sh` et `s2-harness/tests/test_sceau.py` modifiés, ce journal neuf ; rien d'autre
  de mon fait.
