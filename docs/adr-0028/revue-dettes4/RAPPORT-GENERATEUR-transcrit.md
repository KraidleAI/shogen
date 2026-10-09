# Rapport du générateur de DETTES-T4, avec ses sections datées de correction (transcrit)

> Transcription par l'orchestrateur le 2026-10-09 21:12:10 UTC du fichier RAPPORT-GENERATEUR.md ; contrôle FM-1.1 des transcripts du générateur-correcteur, du réviseur et du contre-contrôleur, par le fm11.py versé et par celui de DT3-E : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# RAPPORT DU GÉNÉRATEUR G1 — lot DETTES-T4 (SHOGEN-DOCS-SHA256SUMS-GATE-1)

- **Modèle** : `claude-opus-5-5` (identifiant exact de l'environnement ; Gate 0 : préfixe `claude-opus-5-5` conforme),
  effort max ; heure lue par `date -u` avant écriture : 2026-10-09 18:08:01 UTC (début), 2026-10-09 18:46:15 UTC (fin).
- Rôle : générateur G1. Rien commis, rien poussé, rien écrit dans `/home/user/shogen` ni dans `docs/`.
- Bases : copie de travail à `6f8bfd8` (tête au début) ; la tête a avancé pendant le lot (`766f0c2`, `9418db8`,
  `aff8c3b`, `2f32432`, `963eba9`). **Le diff est vérifié sur `963eba9`** (tête relue à la fin : `963eba9` à 18:45:45 UTC, `git apply --check` OK) :
  `git apply --check` OK, gates rejouées sur `963eba9` + DT4-a et comparées à `963eba9` seule (passage précédent,
  identique, sur `aff8c3b` : `travail/run-aff8c3b/`).
- Rattachement (G0) : item SHOGEN-DOCS-SHA256SUMS-GATE-1, annexe B, bloc B.90, l.1546 [lu à `963eba9`] : « une gate
  (xtask ou job) qui rejoue `sha256sum -c` de chaque `SHA256SUMS` de `docs/` hors des dossiers interdits, et ses
  tests » ; déclencheur « lot de dettes DETTES-T4 » ; règle « aucune dette » B.87 [lu : l.1390-1392].

## Livrables (sous `$D`)

| pièce | contenu |
|---|---|
| `diffs/DT4-a.diff` | contrôle `enforcement/docs-sha256sums.py` (95 lignes), tests `scripts/controle/tests/test_docs_sha256sums.py` (101 lignes, 7 cas), câblage `.github/workflows/gates.yml` (+4 −1) : **200 lignes ajoutées** (`git diff --numstat` : 4, 95, 101) |
| `INVENTAIRE.md` | 33 `SHA256SUMS` à `963eba9`, 290 lignes : 0 somme en échec, 11 lignes absentes (toutes `sim-niveau`), 4 fichiers non listés |
| `RAPPORT-GENERATEUR.md` | ce rapport |
| `SHA256SUMS` | sommes des pièces ci-dessus et des sorties citées |

DT4-b (correction de sommes) : **sans objet** — aucune somme en échec à la tête (point 3 du brief : rien à
« réparer ») ; les 11 lignes absentes sont la question Q-1.

## Décisions du générateur (à adjuger)

- **D-1 Forme du contrôle** (forme de `journaux-modele.py`) : bibliothèque standard ; sortie 0 conforme, 1 refus avec
  motifs sur stderr, 3 erreur interne, toute exception comprise. Rejeu de `sha256sum --strict -c` dans le dossier de
  chaque `SHA256SUMS` : ligne `<64 hex minuscules><espace><espace|*><chemin>`, chemin relatif sous le dossier (refus :
  absolu, composant vide, `.`, `..`, barre oblique inverse, retour chariot, ligne vide, fichier vide, format BSD).
  Motif : `<SHA256SUMS> l.<n> : <chemin> : somme écrite <…>, réelle <…>` (noms et sommes seuls, jamais un contenu).
- **D-2 Emplacements interdits** : la liste existante du dépôt est `EMPLACEMENTS_INTERDITS` de `xtask/src/sg5.rs`
  (l.84-91 [lu], préfixes exacts, séparateur `/`) ; une constante Rust ne se lit pas depuis Python : le script porte
  la même forme (tuple de préfixes, `startswith`), **plus `docs/adr-0028/execution/`** (liste du brief), et le cas
  `test_liste_couvre_sg5` lit `sg5.rs` et exige que la liste du script la contienne (une entrée ajoutée à S-G5 sans
  l'être ici fait rougir la suite). Les `SHA256SUMS` sous un interdit ne sont ni listés (parcours élagué) ni lus ;
  un chemin listé qui mène sous un interdit, en `*.jsonl` ou hors du dossier par un lien est refusé **sans
  ouverture** ; un `SHA256SUMS` qui est un lien hors de son dossier est refusé sans lecture.
- **D-3 Fichier présent non listé : pas un refus**, compté sur stdout (« 4 fichier(s) non listé(s), non refusés »).
  Raisons : l'item fixe la sémantique de `sha256sum -c`, qui ne voit pas les fichiers non listés ; un `SHA256SUMS`
  scelle les pièces qu'il nomme (`docs/adr-0029/plan-s2bis/README.md` l.12 [lu] : « `SHA256SUMS` : empreintes des
  trois sorties » ; `plan-s2bis-2/README.md` l.17 [lu] : « sommes des trois sorties ») ; les 4 non listés de la tête
  sont des README et journaux G1/G2 hors de ce périmètre déclaré. Les sous-dossiers qui ont leur propre `SHA256SUMS`
  relèvent de lui (6 + 69 + 10 fichiers à la tête, tous listés par le `SHA256SUMS` de leur sous-dossier).
- **D-4 Les 11 lignes absentes de `docs/adr-0028/sim-niveau/SHA256SUMS`** (l.1-10, l.12) : admises par une exemption
  fermée, `ABSENTS_ADMIS`, épinglée par numéros et par le sha256 de ces 11 lignes jointes par un saut de ligne
  (`7f45c55e…5596`, recompté par `sed -n '1,10p;12p' | head -c -1 | sha256sum`, indépendant du script) ; admise
  seulement tant que le fichier manque (présent, il est vérifié). Toute autre ligne absente est refusée. Voir Q-1.
- **D-5 Job** : étape ajoutée au job `g1-model-pinning` (nature la plus proche : contrôle de provenance sur `docs/`,
  précédent de `journaux-modele.py` dans ce même job, DT3-B) ; ses cas dans la suite `scripts/controle`
  (job `controle-unittest`), **plancher 18 → 25** (Ran = 25 mesuré, `--egal`). Aucune action, aucune installation
  (R-8) : `python3` de l'image.

## Questions à l'orchestrateur

- **Q-1 (sim-niveau)** : garder l'exemption D-4 (proposition du générateur) ? Fichier `docs/adr-0028/sim-niveau/SHA256SUMS`,
  lignes l.1-10 et l.12, sommes écrites dans `INVENTAIRE.md` (réelle : sans objet, fichiers jamais versés,
  `git log --all` : 0 commit) ; dernier commit sur le `SHA256SUMS` : `972612a` (2026-10-03T00:49:18Z) ; fichiers
  listés : jamais au dépôt (sortie du lot SIM-NIVEAU sur le poste local, `docs/G1-lot-SIM-NIVEAU.md` l.48-49, l.206-210
  [lu]). Alternatives : (b) retirer les 11 lignes, contraire à la clôture de SHOGEN-SIM-SOMMES-1 (annexe B l.515 [lu] :
  « Lignes existantes non touchées (le paquet cite l.11, l.13, l.15-16) ») — les numéros cités glisseraient ;
  (c) verser les fichiers manquants, qui n'existent que sur le poste local (acte extérieur, item avec déclencheur) ;
  (d) refuser sans exemption : gate rouge à la tête, non câblable.
- **Q-2 (`*.jsonl`)** : un chemin listé en `*.jsonl` sous `docs/` est refusé sans ouverture (serrage, transposé de la
  liste des interdits du brief ; 0 cas à la tête). À confirmer, ou à desserrer par un lot.
- **Q-3 (liste de S-G5)** : `EMPLACEMENTS_INTERDITS` de `xtask/src/sg5.rs` ne contient pas `docs/adr-0028/execution/`,
  que le brief interdit ; S-G5 imprimerait donc le texte d'une citation introuvable sous ce dossier. Hors du périmètre
  de DT4 (code Rust) : item à former (PAROXYSME), ou confirmation que ce dossier est hors de la liste à dessein.

## Limites rendues (PAROXYSME)

- **L-1** Les fichiers de sommes d'un autre nom ne sont pas couverts par l'item ni par le contrôle :
  `etude-marche/carto/SHA256SUMS.raw` (37 lignes), `etude-marche/hylo/SHA256SUMS.copies` (193),
  `calib/SHA256SUMS-ECHANTILLONS.txt` (148) ; tous leurs fichiers listés sont absents (copies non versées) : un rejeu
  n'y est pas possible en CI. Item à former si l'orchestrateur veut une règle (par exemple : interdire le nom
  `SHA256SUMS` aux manifestes de copies non versées).
- **L-2** La forge ne démarre pas les jobs (GC-01, en-tête de `gates.yml`) : le contrôle opère par le rejeu local de
  l'orchestrateur, comme les autres étapes du job g1 (item existant SHOGEN-G1-FORGE-1).
- **L-3** Mutant M1 (élagage des dossiers interdits seul retiré) vivant : équivalent en sortie, car le filtre par
  fichier écarte encore tout `SHA256SUMS` interdit ; sa seule différence est que `os.walk` listerait les noms sous un
  interdit (sans ouvrir). M1b (les deux gardes retirées) est tué.
- **L-4** Le contrôle atteste l'accord des octets avec les sommes écrites, non que la somme a été mise à jour par le
  bon lot : un fichier modifié avec sa somme dans le même commit passe (par construction).

## Écarts (E-n)

- **E-1** `git ls-files docs | grep SHA256SUMS` (inventaire, 18:10Z) a listé 4 **noms** sous des dossiers interdits
  (3 sous `docs/adr-0028/execution/`, 1 sous `docs/adr-0028/monark-m009a/`) ; aucun ouvert. Contraire à « ne liste
  rien dedans » du brief.
- **E-2** Un `grep -rln` récursif sur toute la copie creuse (18:1xZ, recherche des usages de `journaux-modele`) :
  interdit par le brief (« aucune recherche récursive sur le dépôt entier »). Copie creuse : dossiers interdits et
  `*.jsonl` absents de l'arbre ; sortie : noms de fichiers seuls, filtrés hors `docs/`.
- **E-3** 10 mutants au lieu de 4 à 8 (M1 révélé équivalent, M1b et M9 ajoutés pour couvrir les gardes).
- **E-4** La tête a avancé cinq fois pendant le lot ; le premier passage des gates (sur `6f8bfd8`, puis sur l'avant-
  dernière version du diff) a été interrompu par moi (`kill` du groupe) et **ne compte pas** ; sorties partielles
  sous `travail/run1-interrompu/`. Passages complets : `aff8c3b` (codes sous `travail/run-aff8c3b/`) et `963eba9`
  (rapporté ci-dessous). Le `kill` a laissé 7 dossiers temporaires de suites sous `$D/tmp` (supprimés à la fin).
- **E-5** Lectures du dépôt réel : `git clone --no-hardlinks` (source des copies) et `git -C /home/user/shogen
  rev-parse HEAD` (relecture de la tête) ; aucune écriture.

## Tests d'abord, mutants

- Rouge (script absent, tests finaux) : `sorties/rouge-final.txt` : 7 cas, `FAILED (failures=17)`, 17
  `AssertionError`, 0 `ERROR` (sous-cas compris).
- Vert : `sorties/vert-final.txt` : `Ran 7 tests`, `OK`.
- Valeurs de référence indépendantes : SHA-256 de « abc » (FIPS 180-2, annexe B.1) et du message vide, écrits en dur ;
  épingle des 11 lignes recomptée par `sed`/`sha256sum`.
- Mutants (`outils/mutants.py`, `sorties/mutants.json`, borne 300 s, `start_new_session` + `killpg`, classement
  SHOGEN-MUT-FATAL-1 : 1 avec `FAILED (failures=` sans erreur = tué) : 9 tués / 10, 1 équivalent (L-3), 0 FATAL ;
  `ps` de fin filtré sur `$D` : 0 processus.

## Gates (copie `963eba9` + DT4-a, comparée à `963eba9` seule)

Lignes des jobs telles qu'écrites dans le `gates.yml` de chaque arbre (`outils/gates.sh`, réseau coupé par
`isole.sh`, variables de mandataire retirées, `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée). Sorties `sorties/g-copie-*`,
`sorties/g-tete-*`, codes `sorties/g-*-codes.txt`.

| gate (job) | `963eba9` + DT4-a | `963eba9` seule |
|---|---|---|
| cas du vérificateur (runner) | 0 — 137 ok, 0 échec | 0 — 137 ok |
| S2 `verdict-suite-s2.py --egal` (s2-harness) | 0 — Ran = 415, sauts nommant la variable scellée | 0 — 415 |
| s2bis `--plancher 341` | 0 — Ran = 341 | 0 — 341 |
| sim-bis `--plancher 279` (clone git complet, `fetch-depth` équivalent) | 0 — Ran = 279 | 0 — 279 |
| calib-actifs `--plancher 65` | 0 — Ran = 65 | 0 — 65 |
| controle `--plancher 25` / `18` | 0 — Ran = 25 | 0 — Ran = 18 |
| g1 : cas du lint R-1 | 0 — 227 ok | 0 |
| g1 : lint R-1 de l'arbre | 0 | 0 |
| g1 : `journaux-modele.py` | 0 — conforme (52 exemptés) | 0 |
| g1 : **`docs-sha256sums.py`** (nouvelle étape) | 0 — 33 SHA256SUMS, 290 lignes, 11 absentes admises, 4 non listés | sans objet |
| g5 : cas du hook pre-commit | 0 — 54 ok | 0 — 54 ok |
| g5 : grep R-13 (motif de `gates.yml`, octets égaux) | 1 = aucun marqueur | 1 |
| g3 : cas de la gate des secrets | 0 — 147 ok | 0 |
| g3 : `gate-secrets.sh --tree` (dépôt jetable des fichiers présents, index seul) | 0 — 1 058 fichiers | 0 — 1 056 (+2 : les deux fichiers neufs) |
| `cargo xtask verify` (lignes VERDICT seules, `CARGO_NET_OFFLINE`) | sortie 1 : 8 VERT, 1 ROUGE (1 violation), global ROUGE | **identiques ligne à ligne** (sortie 1) |

Le ROUGE de xtask est présent à la tête seule, à l'identique (une violation) : préexistant, non causé par DT4-a ;
seules les lignes VERDICT ont été lues, sa gate n'est pas identifiée ici (la copie creuse, sans les dossiers
interdits ni les `*.jsonl`, peut en être la cause [inféré]). Passage précédent sur `aff8c3b` : mêmes résultats
(`travail/run-aff8c3b/`). `ps` de fin filtré sur `$D` : 0 processus. Les g3 `--history` et G4/G6 de forge ne sont
pas rejoués (hors liste du brief).

## Journal de provenance (G1)

Sources lues :
- [lu] `enforcement/journaux-modele.py` (entier, forme du contrôle) ; `.github/workflows/gates.yml` (entier, à
  `6f8bfd8` ; diff `6f8bfd8..aff8c3b` relu : plancher sim-bis 268 → 273) ; `xtask/src/sg5.rs` l.1-140 (liste
  `EMPLACEMENTS_INTERDITS` l.84-91) ; `scripts/controle/tests/test_journaux_modele.py`, `scripts/controle/tests/__init__.py`,
  `scripts/controle/README.md` l.1-60 ; `enforcement/tests/run-fixtures-verdict-suite-s2.py` l.58-59, l.590-640 (cas K) ;
  `enforcement/gate-secrets.sh` l.160-200 (lecture des blobs de l'index : d'où le dépôt jetable des seuls fichiers
  présents pour G3/G5).
- [lu] `docs/adr-0028/ANNEXE-B-items.md` l.461, l.515 (SHOGEN-SIM-SOMMES-1), l.1390-1392 (B.87), titres B.88-B.89 ;
  `docs/adr-0028/ANNEXE-A-lots.md` l.129 ; `docs/G1-lot-SIM-NIVEAU.md` (lignes trouvées par `grep -n` : 34, 48-49,
  64, 96-97, 153, 206-210, 227, 274) ; `docs/adr-0029/plan-s2bis/README.md` et `plan-s2bis-2/README.md` (lignes
  trouvées par `grep -n sha256|somme|empreinte`) ; les 32 `SHA256SUMS` (chemins et sommes).
- [lu] bloc B.90 à `963eba9` : titre l.1535, ligne d'item l.1546 ; `xtask/src/sg9.rs` l.480-495 (la « seule
  occurrence » que cite l'item : `NOMS_D2`, noms de pièces, aucune vérification de somme).

Commandes et sorties (recomptées) :
- `find docs -name SHA256SUMS` (copie creuse) : 31 à `6f8bfd8`, 32 à `aff8c3b`, 33 à `963eba9` ; lignes : 281,
  285, 290.
- `outils/inventaire.py` : `sorties/inventaire-tete.txt` (`6f8bfd8`), `inventaire-aff8c3b.txt`,
  `inventaire-963eba9.txt` ; différences : `revue-dettes3/SHA256SUMS` (4 lignes OK), `revue-nprime/SHA256SUMS`
  (5 lignes OK).
- `sha256sum -c --quiet` dans chaque dossier à `963eba9` : 32 sorties 0, 1 sortie 1 (`sim-niveau`).
- `python3 -B enforcement/docs-sha256sums.py .` à `963eba9` + DT4-a : sortie 0, « conforme : 33 SHA256SUMS, 290
  ligne(s), dont 11 absente(s) admise(s) (SHOGEN-SIM-SOMMES-1) ; 4 fichier(s) non listé(s), non refusés ».
- Historique de `g0-sim/SHA256SUMS` l.4 (`git show <c>:…` + `sha256sum`) : OK `435fa12`, **échec `784ebd2`**
  (écrite `eeaceb6b…`, réelle `d9cffc0a…`), OK `3164348`, `12ce67f`, `2f32432`, tête (5 commits touchent l'un des deux fichiers) ; contrôle sur `git archive 784ebd2
  docs/adr-0029` : sortie 1, refus l.4 (`sorties/retro-784ebd2.txt`).
- `git log --all -- docs/adr-0028/sim-niveau/{execution-B,oracle-1b,oracle-4a-4b,sim_niveau.log.txt}` : 0 commit.
- `git ls-files --eol` des 32 `SHA256SUMS` (à `aff8c3b`) : `i/lf w/lf` (`.gitattributes` : `* text=auto eol=lf`) : pas de risque
  CRLF sur un poste Windows.
- Octets : aucun caractère barre oblique inverse dans le script ni dans les tests (`chr(92)` compté : 0) ; regex du
  G5 rejoué identique à celle de `gates.yml` (sha256 de la commande extraite égal : `447938f7…`).

## Section datée du 2026-10-09 19:02:07 UTC (`date -u`) : suite de l'adjudication (`ADJUDICATION.md`, 18:47:13 UTC, lue à 18:47:21 UTC)

Base : tête relue à 19:02:07 UTC = `6356a945c4faf667b9b4a432cd6cb9b2200432a6` (commit de fusion « Merge pull request #9 »,
**arbre identique** à `963eba9`, `git diff --quiet` et même arbre `7bb7ac53…`). Série **DT4-a, DT4-b, DT4-c**, à
appliquer dans cet ordre : `git apply` OK sur `6356a94`. Le nom DT4-b désigne désormais le diff de Q-3 ; la correction
de sommes reste sans objet (aucune somme en échec). Versions avant adjudication : `travail/avant-adj/`.

| diff | sha256 | lignes (+/−) | contenu |
|---|---|---|---|
| `diffs/DT4-a.diff` | `2f5827c7…1dbb` | +200 −1 | contrôle, tests, câblage ; **Q-1** : motif écrit dans la docstring (fichiers jamais versés, restés sur le poste local ; lignes gardées à la clôture de SHOGEN-SIM-SOMMES-1, `04beacd`, parce que le paquet les cite par numéro ; toute autre ligne absente refusée) ; test de `test_conforme` regroupé (une ligne) pour tenir à 200 |
| `diffs/DT4-b.diff` | `ed529fa4…9d90` | +20 −15 | **Q-3** : `docs/adr-0028/execution/` ajouté à `EMPLACEMENTS_INTERDITS` (`xtask/src/sg5.rs`) avec son test (`xtask/tests/mutants.rs` : septième fixture, comptes 7 et 9, voisin `execution-bis/`) ; cas Python resserré en **égalité** des deux listes (`test_liste_egale_sg5`) ; docstring du contrôle accordée |
| `diffs/DT4-c.diff` | `93688eef…35d8` | +13 −2 | **L-1** : docstring du contrôle et ajout daté de `scripts/controle/README.md` (noms `SHA256SUMS.raw`, `SHA256SUMS.copies`, `SHA256SUMS-ECHANTILLONS.txt` hors du contrôle : manifestes de copies dont aucun fichier listé n'a été versé, 37, 193 et 148 lignes) ; cas de garde dans `test_conforme` (`docs/c/SHA256SUMS.raw` à ligne absente : non lu) |

**Q-3, sens de la liste de S-G5** (lecture ciblée, [lu]) : `xtask/src/sg5.rs` l.80-83 : « Les emplacements interdits
de lecture, liste du brief du lot SG5-INTERDITS » ; l.93-94 : sous un emplacement interdit, « ses citations se
rapportent par `chemin:ligne` seul » ; `xtask/tests/mutants.rs` l.740-746 : « Les six emplacements sont recopiés de la
liste des briefs, indépendamment du code » ; `docs/G1-lot-SG5-INTERDITS.md` l.128-130 (item I-2,
SHOGEN-INTERDITS-LISTE-UNIQUE-1 : « Un emplacement ajouté aux briefs mais pas au code imprimerait son texte »). La liste
a donc le sens « dossiers interdits des briefs » : l'ajout est fait, sans item. L'ajout ne retire aucune violation
(verdict inchangé, l'extrait seul est masqué).

**Tests d'abord** :
- DT4-b, Rust : tests modifiés, `sg5.rs` encore ancien : `cargo test -p xtask --test mutants sg5_interdits` sortie 101,
  2 échecs (`panicked at xtask/tests/mutants.rs:801:5`, l'`assert!` « texte d'une citation en emplacement interdit
  imprimé »), 1 ok ; après l'ajout : 3 ok (`sorties/B-rouge.txt`, `sorties/B-vert.txt`).
- DT4-b, Python : `test_liste_egale_sg5` contre l'ancien `sg5.rs` : `FAILED (failures=1)`, `AssertionError: Lists
  differ` (`sorties/B-rouge-py.txt`) ; vert avec le nouveau.
- DT4-c : la garde de L-1 décrit un comportement déjà en place (nom exact) : pas de rouge possible ; elle est prouvée
  par le mutant M10 (nom `SHA256SUMS*`), tué.

**Mutants** (`sorties/mutants.json`, `sorties/mutants-rs.json` ; borne 300 s, `start_new_session` + `killpg`) :
Python 11 tués sur 12 (M1 équivalent, inchangé ; M10 nom `SHA256SUMS*` tué ; M11 `execution/` retiré de la liste du
contrôle tué) ; Rust 2 sur 2 (R1 `execution/` retiré de `EMPLACEMENTS_INTERDITS`, R2 sans barre finale, tué par le
témoin des voisins) ; 0 FATAL ; `ps` de fin : 0.

**Gates** (`6356a94` + DT4-a/b/c contre `6356a94` seule, mêmes lignes qu'au passage précédent ; codes
`sorties/g-*-codes.txt`) : toutes en 0 des deux côtés (runner 137 ; S2 Ran 415 ; s2bis 341 ; sim-bis 279 ; calib 65 ;
controle 25 contre 18 ; cas du lint 227 ; lint ; journaux-modele ; docs-sha256sums « 33 SHA256SUMS, 290 lignes » ;
hooks 54 ; G5 grep 1 = aucun marqueur ; G3 cas 147, arbre 1 058 contre 1 056 fichiers). `cargo test -p xtask` :
sortie 0 des deux côtés (80 + 9 tests, lignes `test result` seules lues). `cargo xtask verify` : **VERDICT identiques
ligne à ligne** (8 VERT, 1 ROUGE à 1 violation, global ROUGE, des deux côtés). Le VERT de xtask sur une copie complète
n'a pas été tenté : une copie complète extrait les dossiers interdits et les `*.jsonl`, et la sortie de `verify`
imprimerait leurs extraits (S-G4 imprime la ligne d'une violation, I-1 de `docs/G1-lot-SG5-INTERDITS.md` l.124-127) ;
lignes VERDICT comparées à la place, comme l'adjudication le permet. Passages précédents : `travail/run-963eba9/`.

**L-2 précisé** : la forge est l'hôte GitHub du dépôt (le commit de tête est la fusion de la PR n° 9 de
`KraidleAI/…` [lu : message de `6356a94`]) ; les jobs sont ceux de `.github/workflows/gates.yml`, ici le job
`g1-model-pinning` qui porte l'étape nouvelle (et `controle-unittest` qui porte ses cas). ADR-0028 l.198 [lu] : « Tant
que la forge est morte (GC-01), le G3 opérant est l'oracle local, rejoué par l'orchestrateur » ; la première exécution
sur la forge du job g1 est l'item SHOGEN-G1-FORGE-1 (b), déclencheur « forge rétablie (§4.1) »
(`docs/adr-0028/G0-lot-D8a.md` l.431 [lu]). Ce que l'oracle local ne prouve pas pour l'étape nouvelle : le `python3` de
l'image `ubuntu-24.04` (3.12.3 au manifeste lu le 2026-09-29, annexe B l.78 [lu] ; mesuré ici : 3.11.15 ; le script
exige ≥ 3.9, `bytes.removesuffix`). Que les Actions démarrent de nouveau depuis la PR n° 9 n'est pas mesuré (aucun
accès réseau) [abs].

Écart **E-6** : sorties complètes de `cargo test`/`verify` écrites sous `sorties/` puis supprimées après extraction des
seules lignes `test result` et `VERDICT`.

## Section datée du 2026-10-09 19:40:38 UTC (`date -u`) : DT4-d, corrections de la G2 (adjudication du 19:26:58 UTC)

Base : tête relue à 19:40:38 UTC = `6356a945c4faf667b9b4a432cd6cb9b2200432a6` (inchangée). Série **DT4-a, DT4-b, DT4-c,
DT4-d** : `git apply` OK dans cet ordre sur une copie neuve ; empreinte de la série (sha256 de la concaténation
a|b|c|d) : `5048855c7597156d432bf0535a0eeeb8adb16b998187697e7772012ccd95481d`. Sources lues : `ADJUDICATION.md`
(ajout de 19:26:58), `g2/RAPPORT-G2.md` (entier), `g2/DT4-d-propose.diff` (donnée), `g2/outils/mutants_g2.py`
(liste N1-N8) [lu].

`diffs/DT4-d.diff` (sha256 `2efaadb7…17a1`, **+50 −6**) :
- **C-1** (`docs-sha256sums.py`) : le chemin réel du `SHA256SUMS` (relatif à la racine réelle) doit rester sous son
  dossier et hors des interdits, sinon refus « lien hors de son dossier ou vers un interdit (non ouvert) », sans
  lecture (forme de la G2).
- **C-2** (`test_interdits`) : les trois cas de la G2 : lien de `SHA256SUMS` hors du dossier vers un fichier non
  interdit ; chemin listé `l.md` lien vers `execution/x.md` ou `a.jsonl` du même dossier ; le même lien porté par le nom
  `SHA256SUMS` (refusé, contenu `'abc'` absent de stderr).
- **C-3** : les deux `PAQUET.sha256` de `docs/adr-0028/sceau/` nommés hors du contrôle (docstring et README) ; recompté
  à `6356a94` : une ligne chacun, `sha256sum -c` depuis la racine : 0 (courant, rejoué par `scripts/sceau/verify.sh`
  l.13 [lu]) et 1 (`premier-2026-10-02/`, paquet rescellé).
- **C-4** : `os.walk(..., onerror=lever)`, `lever` relève l'`OSError` : un dossier illisible fait sortir en 3 (erreur
  interne), jamais un saut silencieux. Test neuf `test_dossier_illisible` : doublure de `os.scandir` (via
  `unittest.mock.patch`) qui lève `PermissionError` sur `docs/b`, `main` appelée en processus (`runpy`) : 3 exigé.
  Démontrable sur cet hôte root, ce que la G2 ne pouvait pas faire par les permissions.
- **README** (`scripts/controle/README.md`, ajout daté 19:28:17 UTC) : C-3, C-1, C-4 ; **serrage gardé** (Q-G2-1) :
  chemins relatifs sans `./` (écrire le fichier depuis le dossier par `sha256sum <fichiers>`) ; **consigne** : un
  `SHA256SUMS` versé ne nomme que des pièces versées.
- Plancher `controle-unittest` : **25 → 26** (Ran = 26 mesuré, `--egal`).

**Rouge avant** (script de la série a+b+c, tests de DT4-d) : `sorties/D-rouge.txt` : `FAILED (failures=2)`, deux
`AssertionError` (`0 != 3` pour C-4 ; `Tuples differ: (1, False, True) != (1, True, False)` pour C-1 : le contenu de
l'interdit était imprimé), 0 `ERROR`. **Vert après** : `sorties/D-vert.txt`, `Ran 8 tests`, OK.

**Mutants** (`outils/mutants3.py`, `sorties/mutants-d.json` ; borne 300 s, `start_new_session` + `killpg`) : **20 tués
sur 21**, 0 FATAL : M1b à M12 (M9 transposé : garde entière de C-1 retirée ; M12 : `onerror` retiré, tué par C-4) et
N1 à N8 de la G2 (N3, N7, N8 compris) ; M1 vivant, équivalent (inchangé). Mutants Rust R1 et R2 : DT4-d ne touche pas
`sg5.rs` (campagne précédente valable). `ps` de fin : 0.

**Gates** (`6356a94` + a/b/c/d contre `6356a94` seule ; codes `sorties/g-*-codes.txt`) : toutes en 0 des deux côtés
(runner 137 ; S2 415 ; s2bis 341 ; sim-bis 279 ; calib 65 ; **controle 26** contre 18 ; cas du lint 227 ; lint ;
journaux-modele ; docs-sha256sums « 33 SHA256SUMS, 290 lignes, 11 absentes admises, 4 non listés » ; hooks 54 ; G5
grep 1 = aucun marqueur ; G3 cas 147, arbre 1 058 contre 1 056) ; `cargo test -p xtask` 0 des deux côtés, lignes
`test result` identiques (80 + 9) ; `cargo xtask verify` : VERDICT identiques ligne à ligne (8 VERT, 1 ROUGE préexistant,
global ROUGE). Passage précédent (a+b+c) : `travail/run-6356a94-abc/`.

R-25 : DT4-a +200, DT4-b +20, DT4-c +13, DT4-d +50. Octets 92 (barre oblique inverse) dans DT4-d : 0 ; retours
chariot : 0. Aucune recherche récursive dans cette phase.

## Section datée du 2026-10-09 20:13:36 UTC (`date -u`) : DT4-e et DT4-f, réserves du contre-contrôle (adjudication du 19:58:14 UTC)

Base : tête relue à 20:13:31 UTC = `6356a945c4faf667b9b4a432cd6cb9b2200432a6` (inchangée). Série **DT4-a à DT4-f**,
`git apply` OK dans l'ordre sur une copie neuve ; empreinte (sha256 de la concaténation a|b|c|d|e|f) :
`55b38839ddd022860af6f89b0d04e182e3f83eb99568cc8056f8eb2c68fd72de`. Sources lues : `ADJUDICATION.md` (ajout de
19:58:14), `g2/cc/RAPPORT-CC.md` (entier), `g2/cc/DT4-e-propose.diff` (donnée), `g2/cc/outils/mutants_cc.py`
(définitions K1-K5) [lu] ; `xtask/src/sg5.rs` l.30-45, l.78-101 et `xtask/tests/mutants.rs` l.855-885 [lu].

| diff | sha256 | lignes | contenu |
|---|---|---|---|
| `diffs/DT4-e.diff` | `40c9b36e…4edc` | +17 −10 | `interdit()` : **C-5** tout composant en `.jsonl` (dossier compris) ; **C-8** comparaison sur le chemin plié (`casefold`, `ſ` → `s` compris). Tests : **C-6** voisins de préfixe `docs/ab/` dans les deux cas de lien ; **C-7** motif « hors forme » exigé et cas barre oblique inverse (`chr(92)`) ; C-5 et C-8 : dossiers `b/z.jsonl`, `Rapports`, `adr-0028/EXECUTION`, `ADR-0025`, `b/Z.Jsonl`, `rapport` + `ſ` jamais lus, chemins listés `z.jsonl/x.md`, `Monark-M009A/x.md`, `Execution/x.md`, `a/x.JSONL`, `Z.jsonL/x.md` refusés « interdit » ; docstring |
| `diffs/DT4-f.diff` | `730ec896…7c54` | +42 −3 | **C-9** : `emplacement_interdit` de `sg5.rs` plie la casse (`to_uppercase().to_lowercase()`, au plus près d'un système insensible à la casse, `ſ` compris) et interdit tout composant en `.jsonl` ; test Rust `mutant_sg5_interdits_casse_et_jsonl` (cinq fixtures : `Rapports/`, `adr-0028/EXECUTION/`, `rapport` + `ſ`, `b.jsonl/`, `x/Y.JSONL/` : violation à `chemin:3`, texte jamais imprimé) ; voisin `docs/b.jsonlx/` au témoin des voisins (texte gardé) ; commentaire de module ; `cargo fmt --check` propre |

**C-9, lecture** : S-G5 compare des chemins par préfixe (`emplacement_interdit`, l.95-101 à la tête) et ne lit que des
`*.md` ; un `*.md` sous un dossier `*.jsonl`, ou sous un interdit écrit dans une autre casse, y était cité en texte : la
règle s'applique, d'où DT4-f. Le pli Rust (majuscules puis minuscules) et le `casefold` Python donnent le même résultat
sur les préfixes de la liste (ASCII) et sur `ſ` (mesuré par les deux tests) ; ils peuvent différer sur d'autres
caractères non ASCII sans effet sur ces préfixes [inféré].

**Rouges avant** :
- DT4-e, tests neufs contre le script de DT4-d : `sorties/E-rouge.txt`, `FAILED (failures=1)`, `AssertionError:
  Tuples differ: (1, False) != (0, True)` (dossier `b/z.jsonl` lu) ; avec C-5 seul :
  `sorties/E-rouge-casse.txt`, même `AssertionError` (dossiers en casse mêlée lus) ; 0 `ERROR`. Vert :
  `sorties/E-vert.txt` (Ran 8, OK).
- DT4-f, test Rust contre l'ancien `sg5.rs` : `sorties/F-rouge.txt`, sortie 101, `panicked at
  xtask/tests/mutants.rs:908:5` (`assert!` « texte imprimé »), 3 ok, 1 échec ; vert : `sorties/F-vert.txt` (4 ok).

**Mutants** :
- Python (`outils/mutants3.py`, `sorties/mutants-e.json`, `sorties/mutants-e.txt`) : **28 tués sur 29**, 0 FATAL. Sont
  tués M1b à M15, K1 à K5 et N1 à N8. M13 (casse non pliée) et M15 (`lower()` au lieu de `casefold()`, tué par le cas
  `ſ`) portent sur C-8, M14 (fin de chemin seule) sur C-5. M1 reste vivant (équivalent, inchangé).
- Rust (`outils/mutants_rs.py`, `sorties/mutants-rs-f.json`) : **6 sur 6** tués : R1, R2, RF1 (casse non pliée), RF2
  (minuscules seules : `ſ`), RF3 (`.jsonl` non interdit), RF4 (`contains` au lieu de `ends_with` : voisin
  `b.jsonlx`).
- Borne 300 s, `start_new_session` + `killpg`, fichiers restaurés (sha256 contrôlé) ; `ps` de fin : 0.

**Gates** (`6356a94` + a à f contre `6356a94` seule ; codes `sorties/g-*-codes.txt`) : toutes en 0 des deux côtés
(runner 137 ; S2 415 ; s2bis 341 ; sim-bis 279 ; calib 65 ; **controle 26**, plancher inchangé et exact, contre 18 ;
cas du lint 227 ; lint ; journaux-modele ; docs-sha256sums « 33 SHA256SUMS, 290 lignes, 11 absentes admises, 4 non
listés » ; hooks 54 ; G5 grep 1 = aucun marqueur ; G3 cas 147, arbre 1 058 contre 1 056). `cargo test -p xtask` :
sortie 0, **81** + 9 tests contre 80 + 9 à la tête (le test neuf). `cargo xtask verify` : VERDICT identiques ligne à
ligne (8 VERT, 1 ROUGE préexistant, global ROUGE). Passage précédent (a à d) : `travail/run-6356a94-abcd/`.

R-25 : DT4-e +17, DT4-f +42. Retours chariot : 0. Barres obliques inverses ajoutées : 0 dans DT4-e ; 3 lignes dans
DT4-f, échappements Rust voulus (`\u{17F}`, deux `\n` de messages, de la forme des lignes voisines), octets contrôlés
par `od -c`. Aucune recherche récursive dans cette phase. Écart **E-7** : `cargo fmt -p xtask` a récrit en place les
deux fichiers Rust touchés (mise en forme seule, tête déjà propre : `cargo fmt --check` sortie 0 sur une copie de la
tête, supprimée).

## Section datée du 2026-10-09 20:29:36 UTC (`date -u`) : DT4-g, réserve R-4 du contre-contrôle (adjudication du 20:27:50 UTC)

Base : tête relue à 20:29:17 UTC = `6356a94` (inchangée). `diffs/DT4-g.diff` = `g2/cc/DT4-g-propose.diff` **à l'identique**
(`cmp`), sha256 `99e70eecdf7553b45b254963bf3d7c3c28dfe2b89844257d944d1142856aa5b3`, +3 −0 (test `test_interdits` : quatre voisins autorisés `rapportsX`,
`adr-0028/Execution-bis`, `b.jsonlx`, `ADR-00250` lus, motif « l.1 : x.md absent » exigé). Série a à g : `git apply`
OK dans l'ordre ; empreinte (concaténation a|b|c|d|e|f|g) `3f6d619d40043171c0a0be51533fa5e3a3b31f6e76a6ab5ad10a4b180dd6a95c`.

**Preuve** : PX4 (barre finale retirée des préfixes interdits du script) avec DT4-g : `FAILED (failures=2)`, deux
`AssertionError` (`test_interdits` : « docs/b.jsonlx/SHA256SUMS l.1 : x.md absent » non trouvé ; `test_liste_egale_sg5` :
listes différentes), `sorties/G-PX4-avec-DT4g.txt`. Sans DT4-g, PX4 est tué par le seul cas d'égalité des listes
(`failures=1`, `sorties/G-PX4-sans-DT4g.txt`) : DT4-g lui ajoute un témoin de comportement, indépendant de la liste de S-G5.
Mutants Python rejoués (`sorties/mutants-g.txt`, `mutants-g.json`) : 29 tués sur 30 (PX4 compris), M1 vivant (équivalent),
0 FATAL ; `ps` de fin : 0.

**Gates courtes** (`6356a94` + a à g, `sorties/gg-*`) : runner 0 (137 ok) ; controle 0, **Ran = 26** exact (`--egal
--plancher 26`) ; job g1 : cas du lint 0 (227), lint 0, journaux-modele 0, docs-sha256sums 0 (33, 290, 11, 4).
