# Corrections C-1 à C-6 de SB-13 (transcrit)

> Transcription par l'orchestrateur le 2026-10-09 00:44:06 UTC du texte rendu par l'agent a83a987fb3822ab74 (section datée de RAPPORT-GENERATEUR.md) ; contrôle FM-1.1 de son transcript : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte de l'agent ci-dessous, sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

## 13. Corrections après la G2 (section datée du 2026-10-08, 23:12 UTC)

**Gate 0** : modèle `claude-opus-5-5` (worker, effort max). L'agent des corrections a été arrêté par un redémarrage
après la fin de sa campagne (FIN 22:51:12 UTC, `journal/reprise_g2.log`). La reprise (23:04 UTC) s'est faite depuis
NOTES.md et l'état réel des fichiers ; aucune campagne n'avait été coupée, aucune n'a été comptée sans sa ligne FIN.
Mandat : `ADJUDICATION-G2.md` (797bdaab…), liste fermée C-1 à C-6 ; pièce d'entrée `g2/RAPPORT-G2.md` (64e2630c…),
lue en entier. Aucune écriture git, `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée (`env -u` partout), aucun `*.jsonl`.

### 13.1 Base

Adjudication : c58b997. La tête réelle est **ebd1560** à la reprise (81dac8f, puis ebd1560, après c58b997).
c58b997..ebd1560 ne touche que `docs/` (g0-calib, ADR-0029, annexe B) et JOURNAL.md. `git diff --stat` est vide sur
`scripts`, `.github`, `s2bis`, `s2-harness` et `enforcement`. Aucun test de `scripts/sim-bis` ne lit ces fichiers.
Les diffs ont été faits sur c58b997. Je les ai contrôlés sur ebd1560 (`outils/tete.sh`, `journal/tete.txt`) :
`git archive` avec les exclusions (1 072 membres, 0 sous un chemin exclu) ; `git apply --check` puis `apply` des
quatre diffs, sortie 0 ; `scripts/sim-bis` et `gates.yml` égaux à `etapes/e13d` (diff 0) ; la base est égale à
`etapes/e0`. Je n'ai avancé aucune base.

### 13.2 Diffs (`diffs-apres-sb15/`, à appliquer dans l'ordre)

| diff | sha256 | code ajouté / retiré | doc | plancher | contenu |
|---|---|---|---|---|---|
| SB-13A | a1993dfc53d8f60274817a8d107b28cdebaab640aa3f82ae4b1f5514d79b8eb7 | +162 / −2 | 0 | 194 → 199 | épingle, extraire, 5 tests ; C-5 |
| SB-13B | f54486ccf1e548dcae618aa8a97ae01291f8fc22d178157e244b04fb7e13e13b | +132 / −6 | 0 | 199 → 204 | charger, 5 tests (dont C-6) |
| SB-13C | a63ae232d1e9d96cf4b079b81fe1656107b212132f6014a19c1d110b6d73115b | +188 / −5 | 0 | 204 → 207 | croiser, 3 tests ; C-1, C-2, C-4 |
| SB-13D | 9a62d87af4f6228448caa7e581659c87e28e6d81a061fb0210ba6483ed3b961e | +114 / −2 (+1/−1 gates.yml) | +1 | 207 → 210 | 3 tests de CONTRAT-RB6-1 ; C-3 |

Le code ajouté vaut 162, 132, 188 et 115 lignes (`git apply --numstat`, tout fichier hors `.md`). Aucun SB-13E n'a été
nécessaire. Chaque plancher est exact sous `--egal` (§13.5). Forme : 0 octet 92 dans les quatre diffs, aucun
TODO/FIXME, bibliothèque standard seule. Deux lignes ajoutées dépassent 120 caractères : la `source` de
`parametres.json` (E-7) et la ligne de tableau du README (E-12, forme de toutes les lignes de cette table).

### 13.3 Tableau des corrections (lignes dans `etapes/e13d`, égal à ebd1560 + série)

| C | fichier:ligne | test | diff | rouge (test seul, sous le mutant) | mutants tués |
|---|---|---|---|---|---|
| C-1 | `scripts/sim-bis/tests/test_oracle_recalc.py:309-313` (cas : g.h en ETH seule, o(7, g.h) altéré ; écart `[("o", 7, "g.h")]` attendu) | `test_croiser_voit_les_ecarts` (l.285) | SB-13C | M-G2-01 : FAIL 1, ERROR 0 | M-G2-01, M-13C-14, M-13C-15 |
| C-2 | `test_oracle_recalc.py:257-259` (sixième vecteur à n′ = 54 720, n_s = 109 440, sans écart) ; `:226` (séries i % 6 = 5 : n < n_s ≤ 2n) ; `:283` (16 séries comptées) | `test_vecteurs_e_s_51` (l.241), `test_series_synthetiques_e_s_51` (l.261) | SB-13C | M-G2-02 : FAIL 1, ERROR 0 | M-G2-02, M-13C-16, M-13C-17, M-13C-18 |
| C-3 | `scripts/sim-bis/README.md:27` (ligne `oracle_recalc.py`, sous-lot SB-13 première passe) | aucun (texte) | SB-13D | sans objet | sans objet (E-10) |
| C-4 | `test_oracle_recalc.py:191` (HOTES10), `:209-210` et `:219` (i % 10 = 5 : dix unités dans les quatre classes), `:281-283` (40 classes de dix, dont 22 à m_t ≥ 8 à une même position) | `test_series_synthetiques_e_s_51` | SB-13C | M-G2-13 : FAIL 1, ERROR 0 | M-G2-13, M-13C-19, M-13C-20 |
| C-5 | `.github/workflows/gates.yml:231-232` (commentaire de `fetch-depth: 0` : SB-13, f458980, seconde raison) | aucun (commentaire) | SB-13A | sans objet | sans objet (E-10) |
| C-6 | `test_oracle_recalc.py:164-178` (processus neuf, `builtins.open` relevé pendant `charger` : `config/analyse.json` écrit puis lu dans le dossier extrait) | `test_analyse_lu_dans_l_extraction` | SB-13B | M-G2-12 : FAIL 1, ERROR 0 | M-G2-12, M-13B-13, M-13B-14 |

Le rouge est relevé par `outils/rouges_g2.py` (`journal/rouges-g2.txt`) : chaque test est vert sur le code intact, puis
FAIL d'assertion sans ERROR sous le mutant du réviseur qu'il vise. C-6 tient dans le lot : +15 lignes, une seule
pièce. La première exécution de son rouge donnait ERROR, faute de `s2bis/` dans l'arbre léger (E-8). Le rouge refait
donne FAIL. Après la correction, les tests de CONTRAT-RB6-1 sont aux lignes 338 (`test_noms`), 368 (`test_seuils`) et
411 (`test_vecteurs`), et non plus 299, 329 et 372 (§10).

**Durée du test des 100 séries (C-4)** : test seul, trois fois (`outils/duree.sh`, `journal/duree-c4.txt`, 4 vCPU
partagés, charge 3,3 à 4,5). Après C-4 : 2,010 s, 1,995 s, 1,997 s. Avant (ancienne e13d) : 1,656 s, 1,805 s, 1,627 s.
Le surcoût est d'environ 0,3 s. Les croisements sont calculés une fois par processus (`croisements`) et servent aussi à
`test_seuils`.

### 13.4 Mutants (commande du job sim-bis, borne 300 s, 3 en parallèle ; sortie 1 tué, 0 vivant, autre FATAL)

| campagne | étape | mutants | tués | vivants | FATAL | journal |
|---|---|---|---|---|---|---|
| 17 du réviseur (lus dans `g2/outils/campagne_g2.py`, empreinte 364ac436… égale à `g2/SHA256SUMS`, préfixe seul évalué) | e13d | 17 | 17 | 0 | 0 | `mutants-reviseur.txt` |
| neufs de C-1, C-2, C-4 (M-13C-14 à 20) | e13c | 7 | 7 | 0 | 0 | `mutants-g2-13c.txt` |
| neufs de C-6 (M-13B-13, 14) | e13b | 2 | 2 | 0 | 0 | `mutants-g2-13b.txt` |
| anciens de SB-13a, rejoués | e13a | 12 | 12 | 0 | 0 | `mutants-13a.txt` |
| anciens de SB-13b et complément, rejoués | e13b | 12 | 12 | 0 | 0 | `mutants-13b.txt` |
| anciens de SB-13c, rejoués | e13c | 13 | 13 | 0 | 0 | `mutants-13c.txt` |
| anciens de SB-13d, rejoués | e13d | 12 | 12 | 0 | 0 | `mutants-13d.txt` |

Total : 75 mutants, 75 tués, 0 vivant, 0 FATAL. Les témoins sont verts aux planchers 199, 204, 207 et 210. Les quatre
mutants visés par l'adjudication (M-G2-01, 02, 12, 13) sont tués, marque oui : le test nommé est parmi les rouges.
M-G2-13 est désormais tué aussi par `test_series_synthetiques_e_s_51`, et pas seulement par `test_k_et_s_t_rot_2`.
Seul M-13B-01 garde la marque non (module de tests non chargeable), comme avant.

### 13.5 Matrice et portes

- **Mode strict** (`journal/strict.txt`, e13d) : `-X dev -W error` sous 3.10.20, 3.11.15, 3.12.3 et 3.13.14, avec
  PYTHONHASHSEED 0 et 7. Résultat 8/8 : sortie 0, Ran 210 OK, 0 « Exception ignored », 0 « Warning ».
- **Jobs par étape** (c58b997, `journal/reprise_g2.log`) : e0 194, e13a 199, e13b 204, e13c 207, e13d 210, tous
  « conforme » sous `--egal`. Le runner donne 136 ok, 0 échec.
- **Portes sur ebd1560 + série** (`journal/portes-tete.txt`, 23:08 à 23:10 UTC) ; mêmes sorties sur c58b997 + série
  (`journal/portes.txt`) :
  - runner : 136 ok ;
  - sim-bis : Ran 210 conforme, aussi sous `unshare -n` ;
  - s2bis : Ran 255 conforme, sous `unshare -n` ;
  - S2 : Ran 415, OK (skipped=2, sauts qui nomment la variable), conforme, sous `unshare -n` ;
  - hooks 54, model-pinning 227, secrets 147 ;
  - `gate-secrets --tree` : OK (28 fichiers) ;
  - R-13 : motif lu dans `gates.yml`, 0 constat.
- **xtask** (`cargo --locked xtask verify` sous `unshare -n`, lignes de verdict seules) : lignes identiques entre
  série et base, sur ebd1560 comme sur c58b997. S-G1 à S-G8 VERT, S-G9 ROUGE (1 violation, déjà sur la base),
  `cargo fmt --check` VERT, no_std VERT, clippy VERT ; global ROUGE, comme la base.

### 13.6 Écarts (suite de §9)

- **E-8** : le premier rouge de C-6 donnait ERROR, et non FAIL. L'arbre léger n'avait pas de `s2bis/`, donc le mutant
  ne trouvait pas l'`analyse.json` de l'arbre de travail. `leger.sh` copie désormais `s2bis/`, comme le ferait un
  clone. Le rouge refait donne FAIL d'assertion, 0 ERROR.
- **E-9** : la tête a avancé de c58b997 à ebd1560 pendant les corrections, sur des documents seuls (§13.1). La série
  s'applique sans reste sur ebd1560 et y donne les mêmes portes. La base à citer au commit relève de l'orchestrateur.
- **E-10** : C-3 (ligne de README) et C-5 (commentaire de `gates.yml`) sont du texte. Aucun test de `scripts/sim-bis`
  ne lit le README ni ce commentaire, donc aucun mutant ne peut les rougir. L'exigence « deux mutants neufs par
  correction » ne s'applique pas à ces deux-là ; ils sont contrôlés par lecture et par `diff`. Un test qui exigerait
  une ligne de README par module du lot sortirait du périmètre du brief. S'il est voulu, c'est un item à former, par
  exemple SHOGEN-SIM-BIS-README-MODULES-1.
- **E-11** : `outils/tete.sh` (reprise) portait deux octets 92, des continuations de ligne tapées dans un heredoc.
  `compte92` les a vus avant toute exécution. Je les ai retirés par gabarit (`chr(92) + chr(10)`) et le recompte donne
  0. Les quatre outils de la reprise (`tete.sh`, `portes_tete.sh`, `duree.sh`, ce rapport) ont 0 octet 92.
- **E-13** : une première commande de SHA256SUMS (find | xargs) portait une barre oblique inverse tapée en argument ;
  sa sortie a été jetée sans usage et SHA256SUMS a été recalculé par Python (os.walk, hashlib), contrôlé par sha256sum -c.
- **E-12** : la ligne `oracle_recalc.py` du README fait 799 caractères. C'est la forme de chaque ligne de la table des
  modules (une ligne par module).

### 13.7 Items et limites

- SHOGEN-SIM-BIS-ORACLE-RB7-1 reste ouvert. SHOGEN-S2BIS-HOTE-COMMUN-1 reste ouvert aussi (« deux textes sur trois
  liés », Q-SB13-6). CONTRAT-RB6-1 est fermé au commit par l'orchestrateur, après contre-contrôle.
- L-4 : le compte de 22 classes à m_t ≥ 8 vient des tirages SHA-256 de `synthetique`. Il est vérifié par le test
  lui-même, sans recompte hors du code. Les comptes 16 (i % 6 = 5 parmi 0 à 99) et 40 (dix séries × quatre classes)
  sont recomptés à la main.
- L-5 : les campagnes, la matrice et les portes ont tourné sur l'hôte de session, 4 vCPU partagés avec d'autres
  lots ; la CI n'a pas été lancée.

### 13.8 Provenance de la reprise (G1)

- **Lu [lu]** : `ADJUDICATION-G2.md`, `BRIEF-SB13.md`, `g2/RAPPORT-G2.md` et NOTES.md, en entier ; `oracle_recalc.py` et
  `tests/test_oracle_recalc.py` de e13d, en entier ; les hunks non Python des quatre diffs (`gates.yml`, `commun.py`,
  `parametres.json`, README) ;
- **outils lus** : `reprise_g2.sh`, `leger.sh`, `job.sh`, `faire_diffs2.py`, `etats2.py` l.1-80, `portes.sh`,
  `strict.sh`, `rouges_g2.py` l.1-25, `mutants_g2_13b.py`, `mutants_g2_13c.py`, `mutants_reviseur.py` ;
- **journaux** : tous les journaux de `journal/` de la campagne de 22:19 à 22:51 ;
- **dépôt** : `git log` et `git diff --stat` c58b997..ebd1560, en lecture seule.

Les journaux de la campagne de 22:19 à 22:51 viennent de l'agent précédent. Je les ai lus, sans refaire la
campagne. J'ai refait moi-même : les empreintes et les comptes de lignes des diffs, la forme (octets 92, longueurs,
TODO/FIXME), l'application et l'égalité sur ebd1560, les portes et xtask sur ebd1560, la durée de C-4, l'intégrité de
`g2/SHA256SUMS` (`sha256sum -c`, 0) et l'empreinte de `campagne_g2.py`.

### 13.9 Dossier

- **Livrables** : `diffs-apres-sb15/` (série corrigée, base c58b997, valable sur ebd1560), `etapes/` (e0, e13a à e13d
  corrigées), `journal/`, `outils/`, `NOTES.md`, ce rapport.
- **Pièces d'avant la G2** : rangées dans `essais/avant-g2/` (`diffs-5cfe746`, ancienne `diffs-apres-sb15`, anciennes
  étapes, journaux).
- **Copies retirées** : les copies lourdes (`base`, `serie`, `tete`, `cible`) et le contenu de `tmp/`. `travail/` (état
  final source d'`etats2.py`) est conservé.
- **`SHA256SUMS`** : recalculé en dernier, il couvre tout fichier du dossier sauf lui-même et sauf `g2/`, couvert par
  le `SHA256SUMS` du réviseur. `g2/` n'est pas modifié.
