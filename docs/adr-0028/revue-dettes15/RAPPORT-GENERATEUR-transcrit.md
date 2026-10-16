# Rapport du générateur de DETTES-T15, phases 1 à 4 (transcrit)

> Transcription par l'orchestrateur le 2026-10-16 07:29:19 UTC du fichier dettes15/RAPPORT-GENERATEUR.md ; contrôle FM-1.1 des transcripts du générateur (phases 1 à 4), du réviseur G2 et du contre-contrôleur, par le fm11.py versé et par celui de DT3-E : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Rapport du générateur G1 — lot DETTES-T15 (gates S-G5 et S-G9 de xtask, contrôle des images de runner)

## 0. Gate 0

- Modèle : **`claude-opus-5-5`**, l'identifiant exact que donne l'environnement de la session ; effort `max` demandé par
  l'orchestrateur, non observable de l'intérieur.
- Rôle : générateur G1 de la série DT15-a à DT15-f. Je n'ai relu le diff d'aucun autre auteur.
- `date -u` : départ 2026-10-10 08:12:29 UTC ; rédaction de ce rapport à partir de 09:19:02 UTC.

## 1. Base, têtes, copies

- **Base** : `9a9bb23c74ac995ac942d55dab14a148aade059c`, tête de `claude/compassionate-noether-szmdyj` au départ
  (`git rev-parse HEAD`). `4c98594` (DETTES-T14) et `0e03a9f` en sont des ancêtres.
- **Tête en fin de travail** : `6f77aca8d11838114a2cc8d9cbe8ff79ee30b978`, après `7b132bf` (commits DETTES-T6).
  - J'ai suivi 63 chemins : ceux que la série touche et ceux que le registre cite. Entre la base et `6f77aca`, seuls
    `JOURNAL.md` et `docs/adr-0028/ANNEXE-B-items.md` ont changé, par des ajouts en fin de fichier.
  - Sur une extraction de `6f77aca`, les six diffs passent `git apply --check` puis `git apply`, dans l'ordre. Les fichiers
    obtenus sont égaux, à l'octet, à ceux de la série rejouée sur la base.
  - Le registre reste conforme à `6f77aca` (outil indépendant, §3.2).
  - Contrôle refait à 09:22:44 UTC sur la tête suivante, `750ed24` (DETTES-T2 DT2-a). Elle ne change, parmi les chemins
    suivis, que `gates.yml`, et seulement le plancher du job `calib-actifs` (65 devient 66). `scripts/controle/`,
    `enforcement/` et `xtask/` sont inchangés. Les six diffs s'appliquent sur `750ed24`, et le registre y est conforme.
- **Copies** : chaque copie vient d'un `git archive` avec des exclusions de chemins, passé par un filtre
  (`outils/copie_creuse.py`). Le filtre n'a écarté aucun membre : les exclusions de git suffisaient.
  - Dossiers : `copie-base`, `copie-travail`, `copie-serie` (rejeu pas à pas), `copie-tete`, `copie-corpus` (avec les
    octets de `biblio/` de la session), plus les copies de mutation.
  - Le dépôt est resté en lecture seule : aucune écriture git, aucun commit.

## 2. Série (dans l'ordre d'application)

| diff | fichiers | + / − | sha256 | contenu |
|---|---|---|---|---|
| DT15-a | `xtask/src/sg5.rs`, `xtask/tests/mutants.rs` | +189 −1 | `25296d5a…9e17` | item 1 : commentaires HTML ôtés du corpus ; 6 tests |
| DT15-b | `docs/RENVOIS-LIGNES.tsv` (neuf) | +142 −0 | `37b80d5a…32f9` | item 2 : registre des renvois, 133 entrées |
| DT15-c | `xtask/src/sg9.rs`, `xtask/tests/mutants.rs` | +198 −7 | `bd93f73e…559b` | item 2 : contrôle du registre ; arbre synthétique |
| DT15-d | `xtask/tests/mutants.rs` | +114 −0 | `e8efbf7c…ac60` | item 2 : 19 tests du registre |
| DT15-e | `docs/17-modele-de-menace.md` | +1 −0 | `a8566e75…b884` | item 2 : ajout daté en fin de document |
| DT15-f | `enforcement/runners-epingles.py`, test, `gates.yml`, README des contrôles | +29 −2 | `46d102c0…7dc6` | item 3 |

- **Empreinte de la concaténation** a…f, dans l'ordre (57 774 octets) :
  `cb06725a95b1e70b57315dfdfa3a683cf76dbff0b10a0a0b4ba42ee193986032` ; `SHA256SUMS` donne chaque sha256 en entier.
- **R-25** : au plus 198 lignes ajoutées par diff. **R-13** : aucun marqueur de tâche (TODO, FIXME, XXX) dans les lignes
  ajoutées.
- **Largeur des lignes** : toutes les lignes ajoutées font au plus 120 caractères, sauf les lignes de données du registre
  (jusqu'à 175 caractères, un fichier TSV ne se replie pas). `mutants.rs` et `sg5.rs` portaient déjà des lignes de plus
  de 120 caractères ; je n'en ai ajouté aucune.
- **Générateur** : `outils/faire_diffs.py`. Il construit les états intermédiaires de `mutants.rs` par des retraits nommés
  et contrôlés.
- **Chaque état de la série est vert** (`outils/rejouer_serie.sh`, `journaux/serie.txt`) :
  - `cargo test -p xtask` après a, c et d : `mutants` donne 87, 87 puis 106 tests, tous passés ; les autres binaires de
    tests restent verts.
  - Les gates (`xtask gates`) après a, c, d et e ont une seule violation, `docs/17-modele-de-menace.md:70` ; elle est
    expliquée au §3.4.
  - Après f, quatre contrôles passent :
    - runner du vérificateur : `137 ok, 0 échec` ;
    - job `controle-unittest` : sortie 0, `Ran 38`, conforme ;
    - `runners-epingles` : conforme (7 workflows, 22 clés) ;
    - suite s2-harness : `Ran 419`, `OK (skipped=2)`, sur l'état final. La série ne touche pas `s2-harness/`.

## 3. Items : fermeture

| item | diffs | tests (rouges sur l'ancien code) | mutants | état |
|---|---|---|---|---|
| SHOGEN-SG5-COMMENTAIRE-HTML-1 | DT15-a | 6 (4 mutants rouges, 2 témoins) | 12 / 12 tués | fermé |
| SHOGEN-REFS-LIGNE-CONTENU-1 | DT15-b, c, d, e | 19 neufs ; 20 échecs sur l'ancien code (17 mutants, 3 témoins de couverture) | 20 / 20 de code, 8 / 8 de données | fermé |
| SHOGEN-RUNNERS-FLOTTANT-QUADRATIQUE-1 | DT15-f | 1 (rouge d'assertion) | 13 : 12 tués, 1 équivalent prouvé | fermé |

### 3.1 SHOGEN-SG5-COMMENTAIRE-HTML-1 (DT15-a)

**Constat mesuré [lu]** : la page NIST §1.3.5.15 détenue (`biblio/nist-sematech-ehandbook-eda35f-…-2026-10-09.html`)
contient 15 commentaires. L'un fait 1 643 octets et porte la règle « at least 5 ». Son premier `>` est à 215 octets de
`<!--`. Le débalisage prenait donc `<!-- … >` pour une balise et gardait le reste du commentaire au corpus.

**Construction** : `retirer_commentaires` tourne avant la pagination et le débalisage, sur les pages `html`, `htm` et
`md` (Q-4).
- Elle ôte tout de `<!--` jusqu'à la fin du commentaire, selon la tokenisation HTML du WHATWG (états du commentaire) :
  - `>` ou `->` juste après `<!--` ferme un commentaire vide ;
  - sinon, le premier `-->` ou `--!>` ferme le commentaire ;
  - sans fin, le commentaire court jusqu'au bout du fichier.
- Je n'ai pas relu la spécification WHATWG dans ce lot : ces règles viennent de ma connaissance [2nd]. Les tests les
  figent.

**Tests** : fixture minimale, de la forme de la page NIST, sans rien en copier.
- 4 mutants rouges :
  - règle dans un commentaire balisé ;
  - commentaire long sans balise, en `.html`, `.htm` et `.md` ;
  - commentaire jamais fermé ;
  - fausse fermeture `<!---!>`.
- 2 témoins verts :
  - le texte affiché reste après un commentaire NIST, après `<!-->`, `<!--->`, `--!>`, et après `<!-xy>`, qui n'ouvre
    pas de commentaire ;
  - en `.txt`, `<!--` n'ouvre rien.
- Rouge d'assertion montré sur l'ancien `sg5.rs` : 4 tests en échec, `S-G5 devait être ROUGE et ne l'est pas`
  (`journaux/rouge-final-sg5.txt`). Vert ensuite.

**Corpus réel** : sur le corpus complet de la session (196 artefacts sur 196 déclarés), S-G5 est **VERT avant et après**
le changement : 347 fragments contrôlés, 0 violation (`journaux/gates-corpus-base.txt`, `gates-corpus-travail.txt`).
Aucune citation ne dépendait d'un commentaire.

**Mutants** : 12 mutants, S01 à S12, jugés par `cargo test -p xtask` : **12 tués**, 0 FATAL, témoins en sortie 0
(`journaux/mutants-rust-final.out`). Ils couvrent :
- l'appel ;
- chaque extension de la liste, plus `txt` ajouté ;
- chaque règle de fin ;
- le passage de min à max ;
- le décalage du corps ;
- l'ouvrant `<!-`.

Le premier passage laissait S12 vivant ; le témoin `<!-xy>` a été ajouté pour le tuer.

### 3.2 SHOGEN-REFS-LIGNE-CONTENU-1 (DT15-b à DT15-e)

**Formes étudiées et coût sur docs/17** : voir Q-1. docs/17 porte 85 références `chemin:ligne` hors MONARK, sur
24 lignes. Les références MONARK, au nombre de 20, sont épinglées par sha de construction.

**Forme retenue, codée : un registre compagnon**, `docs/RENVOIS-LIGNES.tsv`.
- Le fichier commence par 8 lignes de commentaire, puis l'en-tête, puis une ligne par renvoi.
- Colonnes :
  - `renvoi` : fichier citant et numéro de sa ligne ;
  - `jeton` : texte du renvoi dans cette ligne ;
  - `cible` ;
  - `ecrit` : ligne ou plage écrite ;
  - `lignes` : où se trouve aujourd'hui le texte cité, ou `-` s'il n'est plus dans l'arbre ;
  - `empreinte` : 16 premiers chiffres du SHA-256 des lignes citées, jointes par LF, au commit de lecture ;
  - `commit` : commit de lecture.
- Le commit de lecture est la base que déclare le document citant (Q-7) : `cf696bd` pour docs/17 (l.4 et l.8), et
  `8b14567` pour le paquet scellé (l.5 et l.8).
- Contenu à la base : **133 entrées**.
  - 77 viennent de docs/17 : 62 exactes, 5 déplacées, 10 épinglées.
  - 56 viennent des 84 numéros relevés par DETTES-T14 (les 83 et la l.3 de l'INDEX) : 43 entrées dont le texte est
    retrouvé, 13 épinglées. Un renvoi est exclu parce qu'il est hors du dépôt (Q-2).
  - Au total, 23 entrées sont épinglées.

**La gate (S-G9 (a), `sg9.rs`)** :
- Le registre est lu comme cinquième fichier exact, et la couverture passe à 5 sur 5.
- Chaque référence (a) de docs/17 résolue doit avoir son entrée. Font exception, en bornes listées :
  - les octets de `biblio/` hors de l'INDEX ;
  - les emplacements interdits.
- Chaque entrée est contrôlée :
  - forme ;
  - doublon ;
  - jeton dans sa ligne citante ;
  - numéro écrit dans le jeton, comme nombre entier ;
  - pour une entrée de docs/17, correspondance à une référence de sa ligne ;
  - empreinte des lignes actuelles, sauf pour une entrée épinglée ;
  - pour le paquet scellé, lecture au commit de scellement (constante `SCELLES`).
- Les entrées épinglées sont listées dans une note.

**Les 83 renvois de DETTES-T14 et le paquet scellé** : voir Q-2. Les 6 numéros du paquet vers doc 10 (l.16, l.56,
l.63) forment 3 entrées.
- Leur commit est `8b14567`, et la gate exige ce commit.
- Leur texte de `8b14567` est retrouvé deux lignes plus bas à la base. La gate contrôle ces lignes.

**Tests** : 19 tests à `mutants.rs`, plus l'arbre synthétique muni d'un registre de 6 entrées.
- 17 mutants :
  - insertion au milieu d'un fichier cité (le cas de l'item) ;
  - ligne citée réécrite sur place ;
  - référence sans entrée ;
  - registre absent ;
  - 13 altérations du registre.
- 2 témoins : entrées épinglées et bornes listées ; même référence deux fois sur une ligne. Les empreintes de l'arbre
  synthétique sont calculées hors du code (`sha256sum` et `hashlib`, 16 chiffres).
- Rouge sur l'ancien `sg9.rs`, 20 tests en échec (`journaux/rouge-final-sg9.txt`) :
  - 17 mutants donnent `S-G9 devait être ROUGE et ne l'est pas` ;
  - 3 témoins (deux anciens, un neuf) donnent une couverture `(4, 4)` au lieu de `(5, 5)`.

**Mutants** :
- De code : G01 à G20, **20 tués sur 20** (`journaux/mutants-rust-final.out`).
- De données, sur le registre réel, jugés par S-G9 sur l'arbre de la série : D01 à D08, **8 tués sur 8**
  (`journaux/mutants-registre-reel.out`). Ils couvrent l'empreinte, l'entrée retirée, le sceau, les lignes décalées, le
  jeton, le doublon, une ligne insérée au milieu d'ADR-0028 (15 violations neuves) et une ligne de doc 10 réécrite sur
  place.

**Contrôle indépendant** : `outils/verifier_registre.py` est un autre code que le générateur `registre_renvois.py`.
- Il recalcule chaque empreinte au commit de lecture par `git show` et `sha256sum`, et aux lignes actuelles par `hashlib`.
- Il contrôle que chaque bloc épinglé est absent de la cible.
- Il contrôle que les 84 numéros sont couverts, et que docs/17 compte 77 références pour 77 entrées.
- Résultat **CONFORME** à `9a9bb23` comme à `6f77aca`.
- Le contrôle de la gate en Rust (shogen-core) retrouve les 110 empreintes à lignes actuelles calculées en Python.

**docs/17 (DT15-e)** : une puce datée en fin de liste du §7 (forme sans décalage, règle C-3).
- Elle vise la ligne **Références** et annonce le registre, son commit de lecture, la gate, les bornes et les comptes.
- Les gates S-G4, S-G5 et S-G9 sur cet état n'ont aucune violation neuve.

### 3.3 SHOGEN-RUNNERS-FLOTTANT-QUADRATIQUE-1 (DT15-f)

**Construction** : le nouveau motif est l'ancien, précédé de `(?<![A-Za-z0-9_.-])`.
- Une occurrence de l'ancien motif est toujours une suite maximale de caractères de libellé, prise depuis son début.
- Le regard arrière fait échouer en un pas toute position qui n'est pas un début de suite. Le temps devient linéaire.

**Preuve d'égalité des occurrences de `findall`** : par raisonnement, puis mécaniquement (`outils/flottant_equivalence.py`,
`journaux/flottant-equivalence.out`).
- Raisonnement : l'ancien motif ne peut réussir qu'au début d'une suite. Une position intérieure réussit seulement si le
  début de sa suite réussit, et le balayage a alors déjà consommé la suite entière.
- Partition des 1 114 112 points de code en 8 classes, faite par le moteur `re` lui-même :
  - les atomes sont lus dans le source par son arbre syntaxique ;
  - L moins M vaut `-` seul ;
  - `ſ` (U+017F) compte comme `s` ; K (U+212A), İ et ı comptent comme des lettres.
- Contrôle exhaustif par classes, longueurs 0 à 8 : 19 173 961 chaînes.
- Contrôle exhaustif par jetons, suites de 0 à 5 jetons : 271 453 chaînes.
- Contrôle aléatoire structuré (graine 20261010) : 200 000 chaînes, avec réservoirs réels hors ASCII.
- Trois voix : ancien motif, nouveau motif, et une référence écrite sans expression régulière. Résultat : **0 écart**.

**Temps** (`journaux/flottant-mesures.out`) :
- Ancien motif : ×4 par doublement ; 16 000 « a » prennent 1,17 s, et 32 000 dépassent la borne de 2 s.
- Nouveau motif : ×10 par décade ; à 10^6 caractères, 20 à 48 ms selon la famille.

**Test** : `test_libelle_long_en_temps_lineaire` envoie cinq valeurs de 200 000 caractères, dont une qui doit être refusée
d'un seul jeton, avec une borne de 20 s. `TimeoutExpired` est changé en échec d'assertion.
- Sur l'ancien motif : `AssertionError: plus de 20 s pour 'aaaaaaaaaaaaaaaa'… (200000 caractères)`, `Ran 12`,
  `FAILED (failures=1)` (`journaux/rouge-final-flottant.txt`).
- Sur le nouveau : 12 tests OK en 0,7 s.

**Plancher et documents** :
- Plancher de `controle-unittest` : 37 devient 38 (`--egal`), avec un commentaire daté dans le job.
- Ajout daté du 2026-10-10 08:45:35 UTC à `scripts/controle/README.md`.
- K-04 du runner : ok.

**Mutants** jugés par la ligne du job lue dans le `gates.yml` muté (`journaux/mutants-runners-final.out`). Sur M01 à M13,
**12 sont tués** :
- M01 à M06 par le test de temps borné : regard arrière retiré, ou privé de `-`, de `.`, de `_`, des chiffres, des
  lettres ;
- M08 à M10 par les tests fonctionnels : regard arrière positif, changé en regard avant, drapeau IGNORECASE retiré ;
- M11 à M13 par le vérificateur : plancher 37 ou 39, test retiré.

**M07 est équivalent, et c'est prouvé** : `[A-Z0-9_.-]` et `[A-Za-z0-9_.-]` sous IGNORECASE reconnaissent les mêmes
points de code, et ils diffèrent sur 0 des 1 114 112. Deux mutants doubles montrent le rôle des valeurs du test :
- M14 (M02, test privé de `"-" * n`) est tué : la valeur mêlée suffit ;
- M15 (M03, test privé de la valeur mêlée) est vivant : cette valeur est la seule à porter `.`, `_` et des chiffres. Elle
  est donc nécessaire.

### 3.4 Gates de la série (copie creuse, cible cargo par défaut, `journaux/verify-serie.txt`)

`cargo --locked --offline xtask verify`, lignes VERDICT :
- S-G1 à S-G8 : VERT.
- S-G9 : ROUGE, une violation, `docs/17-modele-de-menace.md:70`. La référence de cette ligne pointe vers un emplacement
  interdit, absent de la copie creuse ; c'était déjà le cas à la base.
- `cargo fmt --check` : VERT ; `no_std` : VERT ; `cargo clippy -D warnings` : VERT.

Sur `copie-corpus` (octets de `biblio/` de la session, registre posé), S-G9 n'a que la même violation. Les 6 références
aux sidecars y sont résolues et listées en borne.

## 4. Phrases de fermeture proposées (bloc daté de l'annexe B)

- **SHOGEN-SG5-COMMENTAIRE-HTML-1** : « Fermé par DT15-a. S-G5 ôte du corpus les commentaires `<!-- … -->` des pages
  HTML et Markdown avant le débalisage. La fin d'un commentaire suit la tokenisation HTML : `>` ou `->` juste après
  `<!--`, sinon `-->` ou `--!>` ; sans fin, le commentaire court jusqu'au bout du fichier. Six tests sur une fixture
  minimale, de la forme de la page NIST §1.3.5.15 (règle restée seulement en commentaire, balises comprises) ; quatre
  sont rouges d'assertion sur l'ancien code. 12 mutants, tous tués. Sur le corpus complet de la session, S-G5 est vert
  avant et après (347 fragments contrôlés). »
- **SHOGEN-REFS-LIGNE-CONTENU-1** : « Fermé par DT15-b à DT15-e. Le registre des renvois `docs/RENVOIS-LIGNES.tsv` est
  un fichier compagnon : aucun texte validé n'est réécrit. Il porte 133 entrées : les 77 références de docs/17 hors
  bornes, et les 84 numéros non exacts relevés par DETTES-T14 (83 et la l.3 de l'INDEX), en 56 entrées ; un renvoi hors
  dépôt est exclu. Chaque
  entrée donne les lignes où se trouve aujourd'hui le texte cité, et l'empreinte de ce texte au commit de lecture que
  déclare le document citant. Elle porte `-` quand ce texte n'est plus dans l'arbre : 23 entrées se lisent ainsi à leur
  commit seul. S-G9 (a) contrôle le jeton, l'empreinte, la complétude de docs/17 et le paquet scellé. Le paquet se lit à
  son commit de scellement `8b14567` (3 entrées, 6 numéros), et son texte est retrouvé deux lignes plus bas. Un ajout
  daté est placé en fin de docs/17. Tests : 19, rouges sur l'ancien code. Mutants : 20 de code et 8 de données, tous
  tués. »
- **SHOGEN-RUNNERS-FLOTTANT-QUADRATIQUE-1** : « Fermé par DT15-f. FLOTTANT est désormais précédé du regard arrière
  `(?<![A-Za-z0-9_.-])`. Les occurrences sont les mêmes : partition d'Unicode par le moteur ; 19 173 961 chaînes
  exhaustives par classes, 271 453 par jetons et 200 000 aléatoires, à trois voix, 0 écart. Le temps est linéaire :
  ×10 par décade jusqu'à 10^6 caractères. Le test de temps borné est rouge d'assertion sur l'ancien motif. Le plancher
  de `controle-unittest` passe à 38 (`--egal`), avec un ajout daté au README des contrôles. 13 mutants : 12 tués,
  1 équivalent prouvé. »

## 5. Questions à l'orchestrateur (Q-n), avec recommandation

- **Q-1 — Forme du contrôle (item 2). Recommandation codée : le registre compagnon (B), avec l'épinglage (C) pour les
  textes absents de l'arbre.** Formes étudiées :
  - **(A) empreinte courte à côté du numéro dans docs/17.**
    - Coût : réécrire 24 lignes validées, qui portent 85 références. Sans réécriture, il faut un ajout daté qui
      recopie les 85 références.
    - La réécriture serait à refaire à chaque changement d'un code cité.
    - Elle ne règle pas les renvois en prose des 24 autres documents.
  - **(B) registre compagnon, mis à jour par un lot revu.**
    - Coût : aucune ligne réécrite, un ajout daté d'une ligne en fin de docs/17, un fichier de 142 lignes.
    - Il détecte une insertion et une réécriture sur place.
    - Le même format couvre les renvois en prose.
  - **(C) renvoi épinglé seul.**
    - Le renvoi est exact par définition. Mais une gate sans historique git ne peut rien contrôler : la CI fait une
      extraction superficielle.
    - Il ne détecte pas une insertion.
  - Pourquoi le fichier compagnon plutôt qu'un ajout daté : un seul lieu pour 25 documents citants, une forme lisible par
    la gate, et une mise à jour qui ne touche aucun texte validé.
- **Q-2 — Les 83 renvois de DETTES-T14 et le paquet. Recommandation codée.**
  - Les 84 numéros (83, plus la l.3 de l'INDEX) se répartissent ainsi :
    - 43 entrées dont le texte est retrouvé : leurs lignes actuelles sont contrôlées par la gate ;
    - 13 entrées épinglées à leur commit de lecture : plages de fichier entier lues par des relecteurs, lignes réécrites
      depuis, ligne du compte de l'INDEX ;
    - 1 exclusion. Le renvoi d'ADR-0028 l.319, « corpus doc 06 l.269 », vise le doc 06 du corpus de conformité, hors du
      dépôt. Il est exact par nature.
  - Paquet scellé : son texte n'est pas touché. Ses entrées sont lues à `8b14567`, et la constante `SCELLES` le
    contrôle.
  - Je n'ai pas fait d'ajout daté dans les 24 documents citants : le registre est le lieu unique.
- **Q-3 — Portée.** Les renvois exacts du relevé ne sont pas au registre : 228 numéros vers les huit cibles, 64 vers
  l'INDEX.
  - **Recommandation : ne pas les porter dans ce lot.**
    - Ils sont exacts aujourd'hui.
    - Le relevé est heuristique et compte de faux renvois, comme « corpus doc 06 ». Les porter exigerait de les trier à
      la lecture.
    - La règle C-3 de l'orchestrateur les protège.
    - Les 43 entrées à lignes actuelles servent de fils-pièges sur ADR-0028, doc 10, annexe A et docs/11. Le mutant D07
      le montre : une ligne insérée au milieu d'ADR-0028 donne 15 violations.
  - Le format les accueille sans changer le code, si l'orchestrateur le décide.
- **Q-4 — S-G5, extensions.** Les commentaires sont ôtés des pages `html`, `htm` et `md` : le rendu Markdown cache aussi
  les commentaires. Ils ne sont pas ôtés du `xml`, du `json`, du `txt`, ni du code : `<!--` n'y ouvre rien.
  - Sens de l'erreur : une lecture sans analyseur peut ôter trop de texte (attribut, script, bloc de code Markdown). Elle
    ne garde jamais un commentaire.
  - Aucun `<!--` dans les fichiers `md`, `txt`, `json` ou code du corpus mesuré.
- **Q-5 — Limite rencontrée : le contenu des éléments `script` et `style`.** Ce texte n'est pas affiché, mais il reste au
  corpus : le corpus compte 788 `<script` et 107 `<style` dans 81 pages `html`, `htm` ou `md`.
  - Un essai non versé l'ôte : S-G5 reste vert sur le corpus complet, avec 347 fragments contrôlés et 0 violation
    (`journaux/essai-script-corpus.txt`).
  - Ce travail est hors de la liste fermée du lot. **Recommandation : former l'item SHOGEN-SG5-SCRIPT-STYLE-1.**
    - Déclencheur : le prochain lot qui touche `xtask/src/sg5.rs`.
    - Prix : ôter le contenu de `<script>` et `<style>` des pages HTML, avec test et mutants. L'essai fait une vingtaine
      de lignes.
  - Autre voie, si l'orchestrateur le préfère : un diff DT15-g dans ce lot.
- **Q-6 — La référence de docs/17:70.** Elle pointe vers `docs/rapports/cartographie-2026-09-29.md:21`, un emplacement
  interdit, et la gate l'exempte du registre : sa plage seule est contrôlée. Aucun agent ne peut en poser l'empreinte
  sans ouvrir la pièce, et une entrée pour elle serait rejetée comme orpheline. **Recommandation : garder la borne.**
- **Q-7 — Commits de lecture.** La table `BASES` (21 documents) et 3 exceptions (`LECTURES`) sont relevées à la main
  dans les documents eux-mêmes, dans `outils/registre_renvois.py`.
  - Exemples de bases déclarées : G0-lot-D8a déclare `fb089dc`. E1:13 dit « à `aa0afdc` ». G2-partie-2:443 et :444
    citent les sha256 `bc146415…` et `1995066b…`, qui désignent les versions `37ea234` et `6eabaa4`.
  - J'ai vérifié 21 renvois à la lecture, en comparant le contexte du jeton au texte cité aux deux commits candidats, et
    5 autres par l'identité de la version lue (sha256 cités, nombre de lignes). Exemple :
    pour G0-lot-D8a, la l.85 à `fb089dc` porte les « Champs » de D6 (viii) ; à `7425a49`, c'est une ligne vide.
  - **Recommandation : que la G2 relise la table.**

## 6. Limites (L-n)

- **L-1** : la gate ne contrôle ni le contenu ni la cible des 23 entrées épinglées. Elle est lexicale et ne lit pas
  l'historique git ; le jeton et la forme de ces entrées restent contrôlés.
  - Ces entrées se rejouent par `git show` (commande en tête du registre).
  - L'outil indépendant les a contrôlées à `9a9bb23` et à `6f77aca`.
- **L-2** : la complétude n'est mécanisée que pour docs/17. Un nouveau renvoi en prose d'un autre document n'entre au
  registre que par le lot qui l'écrit : c'est une règle de procédure, à poser au bloc daté.
- **L-3** : quand un document ne déclare pas sa base, le commit de lecture est le premier commit qui porte le jeton. Sinon,
  c'est un jugement (Q-7).
- **L-4** : l'empreinte porte sur la plage entière. Toute retouche dans une plage citée rougit la gate, même sans changer
  le sens : ce coût de mise à jour est assumé.
- **L-5** : bornes de (a). Les 6 références aux sidecars de `biblio/`, non versionnés, et la référence vers un
  emplacement interdit ne sont contrôlées qu'en plage.
- **L-6** : S-G5 garde les commentaires factices de la tokenisation (`<!x … >`, `<?…>`) quand leur `>` est à plus de
  300 octets. Le corpus n'en compte aucun : 15 `<!` factices, tous fermés à moins de 300 octets, et aucun `<?`. Le contenu
  des scripts et des styles relève de Q-5.
- **L-7** : la preuve et les mesures de FLOTTANT ont tourné sous Python 3.11.15. La CI tourne sous 3.12 [inféré]. La
  partition dépend du moteur `re` ; l'outil la rejoue sur tout interpréteur.
- **L-8** : la marge du test de temps dépend de la machine.
  - Sur cet hôte : 20 s de borne pour l'ancien motif, dont le coût sur 200 000 caractères est d'environ 180 s, extrapolé
    de 4,7 s à 32 000 [inféré : coût quadratique].
  - Le nouveau motif juge les 12 tests en 0,7 s.

## 7. Écarts (E-n)

- **E-1, exposition déclarée pour le contrôle FM-1.1 du transcript.** Pour vérifier les renvois de docs/17:106, j'ai lu
  `s2-harness/tests/test_exclusion.py`, l.240-245 et l.267-272, à `cf696bd` et à `e970c38`. La docstring de ces tests
  porte des comptes de la décision 1 d'ADR-0025.
  - Le fichier est permis : il fait partie de la suite du dépôt.
  - Je n'en ai rien recopié dans les livrables.
- **E-2** : un `grep -n` sur la page NIST détenue a imprimé une ligne de la page. `biblio/` est permis.
- **E-3** : à deux reprises, deux processus lourds ont tourné en même temps. Un `cargo test` a tourné pendant la passe des
  gates sur le corpus complet, qui dure environ 3 min. La charge est restée sous 4,5.
- **E-4** : la première campagne de mutants du job (`journaux/mutants-runners.*`) a tourné avec une version antérieure de
  l'outil : sans relevé des tests en échec, et avec deux mutants du test. La campagne finale (`mutants-runners-final.*`)
  fait foi.
- **E-5** : la vérification de la série a vu `clippy::sliced_string_as_bytes` dans `sg9.rs` (`numero_ecrit`). Je l'ai
  corrigé, puis j'ai régénéré la série, l'ai rejouée et revérifiée. Toutes les sorties citées ici sont postérieures à ce
  correctif.
- **E-6** : échappements (SHOGEN-HARNAIS-ECHAPPEMENTS-1).
  - `ſ` et `K`, tapés dans un outil d'analyse, sont arrivés en caractères littéraux. Je les ai remplacés par
    `chr()`, puis contrôlés par `od`.
  - Les tabulations Rust des tests sont écrites par `chr(92)` ; c'est attesté par `od` et par le rejeu vert.
- **E-7** : la tête a avancé deux fois pendant le travail (`7b132bf`, puis `6f77aca`) ; le constat et le rejeu sont au §1.

## 8. Observation à adjuger

- **O-1** : le relevé de DETTES-T14 datait chaque renvoi par `git blame`, c'est-à-dire au commit de versement.
  - Lus à la base que déclare chaque document, 64 numéros changent de commit de lecture, et 26 de ligne actuelle.
  - Exemples : G0-lot-D8a passe de +1 à +121 ; SIM-NIVEAU passe de +16 à +42. Dans les deux cas, j'ai vérifié la cible à
    la lecture.
  - Le compte « 75 décalés, 6 réécrits, 2 hors plage » devient : 43 entrées retrouvées, 13 épinglées, 1 exclue
    (`mesures/verdicts-registre.tsv`).
  - Le bloc daté de DETTES-T14 cite les chiffres d'origine. Je ne le corrige pas : c'est un acte de l'orchestrateur.

## 9. Journal de provenance (G1)

**Sources lues** :
- [lu] le brief, en entier, avec son ajout de 05:17:57.
- [lu] dans DETTES-T14 :
  - `ADJUDICATION.md`, en entier ;
  - `RAPPORT-GENERATEUR.md`, §4 (Q-6), §9-§10 et §12.1-§12.5 ;
  - les deux TSV de décalages ;
  - les outils `refs_decalees.py`, `lignes_conservees.py`, `decalages_anterieurs.py` et `decalages_anterieurs_index.py`.
- [lu] `RAPPORT-G2.md` du correctif DT5-24, §0 à §12, dont O-5 et `sorties/flottant.out`.
- [lu] à la base :
  - `xtask/src/sg5.rs`, `sg9.rs`, `lib.rs`, `rapport.rs`, `xtask/tests/mutants.rs` et `arbres.rs` ;
  - docs/17, en entier ;
  - `enforcement/runners-epingles.py` et son test ;
  - `scripts/controle/README.md` ;
  - `gates.yml`, l.100-170 et l.336-364 ;
  - `run-fixtures-verdict-suite-s2.py`, l.540-640 ;
  - `docs/09-vocabulaire.md`, l.1-55.
- [lu] les lignes d'annexe B des trois items (l.1605-1612 et l.1640-1650).
- [lu] la page NIST détenue, par mesure seulement ; les contextes de jeton de 25 documents citants ; les lignes citées aux
  commits candidats (§5, Q-7).
- [2nd] les règles de fin d'un commentaire HTML (WHATWG) : connaissance du générateur, non relues ici. Elles sont figées
  par les tests.

**Commandes et sorties** : toutes sont consignées dans `journaux/`.
- Base : `verify-base.txt`.
- Corpus : `gates-corpus-*.txt`.
- Série : `serie.txt` et `verify-serie.txt`.
- Rouges : `rouge-final-*.txt`.
- Mutants : `mutants-rust-final.*`, `mutants-runners-final.*` et `mutants-registre-reel.*`.
- FLOTTANT : `flottant-equivalence.out` et `flottant-mesures.out`.
- s2-harness : `s2-harness-serie.txt`.
- Tête : `gates-tete.txt`.
- Essai Q-5 : `essai-script-corpus.txt`.

**Chiffres recomptés** : tous sortent de ces fichiers ou des outils du dossier. Aucun n'est repris du brief ou de
DETTES-T14 sans recompte ; les 83 numéros ont été relus un par un (§3.2, O-1).

## 10. Livrables

`SHA256SUMS` du dossier couvre :
- les six diffs ;
- `NOTES.md` et ce rapport ;
- les outils (`outils/`) ;
- les mesures (`mesures/RENVOIS-LIGNES.tsv`, identique à DT15-b ; `verdicts-registre.tsv` ; `docs17-references.tsv`) ;
- les journaux.

Les copies de travail ne sont pas sommées : elles se refont par `git archive` et la série.

## Phase 2 — 2026-10-15 (rédaction à partir de 12:34:23 UTC, `date -u`)

Section ajoutée après l'adjudication du 2026-10-10 09:25:00 UTC (`ADJUDICATION.md`, relue en entier le 2026-10-15,
sha256 `2259132072f1c1f9…`). Les sections 0 à 10 ne sont pas réécrites ; ce qui suit les complète ou les remplace là où
c'est dit.

### P2.0 Gate 0 et reprise

- Modèle : **`claude-opus-5-5`** (identifiant de l'environnement) ; effort `max` demandé, non observable de l'intérieur.
- Rôle : générateur G1 de DT15-g, DT15-h et DT15-j (dépôt), et de DT15-i (outil du scratchpad, hors dépôt).
- Phase 2 commencée le 2026-10-10 à 09:25:39 UTC, arrêtée, reprise le 2026-10-15 à 11:46:03 UTC (`NOTES.md`).

### P2.1 Base, têtes, copies

- **Base inchangée** : `9a9bb23c74ac995ac942d55dab14a148aade059c`. Le rejeu part d'une extraction neuve
  (`outils/extraire.sh` : `git archive` avec les exclusions, écrites cette fois dans l'outil, puis le filtre
  `copie_creuse.py`) : 1371 membres, 0 écarté au filtre, comme en phase 1.
- **Têtes vues** : `591acf8` à la reprise, puis `5d4f2dd30fe9b7075c6b5404cb74bb88bcbc0d0a`, puis
  `f56b777888b4cb0a1a0731f530d4b81109caa683` (DEPLOI-BIS DB1-i), où portent les contrôles ci-dessous.
- **Dernière tête, 12:37:40 UTC** : `24c89ef27f2c913ad9f88589381857eae99fdb17` (DEPLOI-BIS DB1-j). Parmi les 120
  chemins, seul le plancher `s2bis` de `gates.yml` change (371 → 372). Les neuf diffs y passent `git apply --check`
  puis `git apply`, et les fichiers égalent ceux du rejeu, hors des planchers de la tête
  (`journaux/tete-apply-final.txt`).
- **Chemins suivis : 120** (`mesures/chemins-a-comparer-p2.txt`) : les 63 de la phase 1, tout `xtask/`, les manifestes
  cargo, `enforcement/` et `scripts/controle/`. Entre la base et `f56b777`, seuls changent `gates.yml` (planchers
  `s2bis` 358 → 371 et `calib-actifs` 65 → 78), `JOURNAL.md` (+11) et l'annexe B (+55), par ajouts.
- **Tête `f56b777`** (extraction : 1396 membres ; `journaux/tete-apply.txt`) :
  - les neuf diffs passent `git apply --check` puis `git apply`, dans l'ordre ;
  - les fichiers obtenus égalent ceux du rejeu sur la base, sauf `gates.yml`, qui ne diffère que des deux planchers
    de la tête ;
  - le registre y est conforme (`verifier_registre.py`, `journaux/registre-tete.txt`) ;
  - contrôles de DT15-f : `runners-epingles` conforme (7 workflows, 22 clés), job `controle-unittest` `Ran 38`
    conforme, runner 137 ok (`journaux/tete-controles.txt`).
- **Copies** : gardées, `copie-travail` et `copie-rejeu` (état final, sources seules). Supprimées : `copie-base`,
  `copie-tete`, `copie-serie`, les copies et cibles de mutation, les cibles cargo, et la copie de la tête qui portait
  les octets de `biblio/`.

### P2.2 Série (dans l'ordre d'application)

| diff | fichiers | + / − | sha256 | contenu |
|---|---|---|---|---|
| DT15-a à f | inchangés (§2) | | | |
| DT15-g | `xtask/src/sg5.rs`, `xtask/tests/mutants.rs` | +153 −31 | `ab640bb3…2889` | Q-5 : contenu de `script` et de `style` ôté ; 15 tests |
| DT15-h | `xtask/src/sg5.rs`, `xtask/tests/mutants.rs` | +36 −8 | `f07105e7…c226` | L-6 : commentaires factices ; 6 tests |
| DT15-j | `xtask/src/sg5.rs`, `xtask/tests/mutants.rs` | +86 −10 | `6b54b2d7…4435` | balises de script et de style lues jusqu'à leur vrai `>` ; 12 tests |

- **Hors série du dépôt** : `diffs-hors-depot/DT15-i.diff` (+96 −24, `575a6a09…320a`), pour
  `<scratchpad>/outils/presg5.py` et son test neuf `outils/test_presg5.py` (§P2.7). La lettre i est celle que le
  coordinateur a donnée à ce diff ; la série du dépôt saute donc de h à j.
- **Empreinte de la concaténation** a…h puis j, dans cet ordre (81415 octets) :
  `8f219939fef3d356f3f8b3d0225acfeac6d217e35e1aeadca173a5332470d425`. Celle de a…f, recalculée, reste
  `cb06725a95b1e70b57315dfdfa3a683cf76dbff0b10a0a0b4ba42ee193986032`.
- **R-25** : au plus 153 lignes ajoutées par diff. **R-13** : aucun marqueur de tâche dans les lignes ajoutées. Aucune
  ligne ajoutée ne dépasse 120 caractères.
- **Générateur** : `outils/faire_diffs_p2j.py`, depuis les états gardés sous `etats/`. Chaque pas de `mutants.rs` est
  une insertion seule (contrôlé) ; l'état h dérivé égale l'état h gardé.

### P2.3 DT15-g : contenu de `script` et de `style` (Q-5)

**Construction** : `retirer_non_affiche` remplace `retirer_commentaires`. C'est un balayage de gauche à droite : à
chaque `<`, un commentaire, un commentaire factice (DT15-h) ou un élément `script` ou `style` est ôté ; sinon le `<`
reste.
- Ouvrante : `<script` ou `<style`, casse ASCII ignorée, suivi d'un blanc, de `/`, de `>` ou de la fin du texte
  (`<scripts>` n'ouvre rien).
- Fin : la fermante `</script` ou `</style`, avec la même frontière. `style` se clôt à sa première fermante. `script`
  suit les trois états de la tokenisation : données ; échappé, après `<!--` ; doublement échappé, après `<script` dans
  l'état échappé. `-->` rend aux données ; une fermante dans l'état doublement échappé rend à l'état échappé.
- Sans fermante, l'élément court jusqu'au bout du fichier.
- Extensions : `html`, `htm` et `md`, celles de Q-4. Je n'ai pas d'avis contraire : le Markdown rend aussi le HTML brut,
  et le corpus ne compte aucun script dans ses pages `md`.
- La fin d'un commentaire se cherche désormais en un seul passage. Le code de l'état f cherchait `-->` puis `--!>`
  depuis le début de chaque commentaire ; la recherche de `--!>`, le plus souvent absent, relisait la fin de la page à
  chaque commentaire. Les règles de fin sont les mêmes (témoins). Aucun test de temps ne couvre ce point.

**Règle du texte affiché** :
- Ôté : ce que la page ne donne jamais à lire, quels que soient les scripts et les interactions (commentaires,
  commentaires factices, contenu de `script` et de `style`).
- Gardé : ce qu'un script ou une interaction peut montrer (`template`, attribut `hidden`, CSS `display: none`,
  `noscript`). L'ôter pourrait faire rougir une citation vraie.
- Occurrences brutes au corpus : 59 `<template`, 68 `display:none` et 65 `display: none`, 19 `<noscript`.

**Tests** : 15, sur une fixture minimale (une ligne de page par test, rien de copié d'une page).
- 7 mutants (ROUGE exigé), 8 témoins.
- Sur le code de l'état f, 5 sont rouges d'assertion (`S-G5 devait être ROUGE et ne l'est pas`,
  `journaux/rouge-ghj-etat-f.txt`). Les deux tests du double échappement y sont verts : le code de l'état f ôtait ce
  texte comme un commentaire HTML. Ils tuent les mutants P07, P08 et P11.

**Mutants** : P01 à P17, tous tués. Ils couvrent la liste des éléments, la casse, la frontière du nom, la fin au bout du
fichier, chaque état du script, chaque règle de fin de commentaire et l'extension `md`.

**Mesure du corpus** (`outils/mesure_corpus_p2.py`, dans l'ordre du balayage, 81 pages : 74 `html`, 7 `md`) :
784 éléments `script` et 107 éléments `style`, tous fermés. 2 scripts contiennent `<!--`, aucun n'est doublement
échappé. 6 styles sont dans un `svg`. Le compte de la phase 1 (788 `<script`) venait d'une recherche brute ; l'écart de
4 tient vraisemblablement aux `<script` écrits dans des commentaires [inféré]. Il n'est pas repris.

### P2.4 DT15-h : commentaires factices (L-6 fermée)

- Sont factices : `<!` non suivi de `--`, `<?`, et `</` suivi d'un caractère qui n'est ni une lettre ASCII ni `>`. Ils
  sont ôtés jusqu'au premier `>`, sans la borne de 300 octets ; sans `>`, jusqu'au bout du fichier.
- `</>` et un `</` final ne changent pas de traitement : la tokenisation ignore le premier, que le débalisage ôte ; elle
  affiche le second.
- Tests : 6, soit 5 mutants et 1 témoin. Le témoin vérifie que DOCTYPE, `<?xml …?>`, `</ x>` et `<!x>` se closent au
  premier `>` et que le texte qui suit reste. Les 5 mutants sont rouges sur le code de l'état g
  (`journaux/rouge-hj-etat-g.txt`) et sur celui de l'état f.
- Mutants Q01 à Q09, tous tués. Q07 remet la borne de 300 octets ; Q09 prend une lettre non ASCII pour un nom de balise.
- Corpus, dans l'ordre du balayage : 73 DOCTYPE, aucun autre factice (`<!`, `<?`, `</` suivi d'une non-lettre), aucun
  au-delà de 300 octets. Les 15 `<!` factices comptés en phase 1 venaient d'une recherche brute ; ils sont, selon toute
  vraisemblance, dans des commentaires ou des scripts que le balayage consomme d'abord [inféré].

### P2.5 DT15-j : balises de script et de style lues jusqu'à leur vrai `>`

- **Défaut trouvé dans mon code de DT15-g**, après la campagne de g et h :
  - l'ouvrante d'un script ou d'un style se lisait jusqu'à son premier `>`, même entre guillemets ;
  - une fermante écrite dans une valeur d'attribut (`<script data-x="a></script>">…`) clôturait donc l'élément, et
    son contenu restait au corpus (texte gardé en trop) ;
  - la fermante avait le même défaut (`</script a=">…">`).
- **Correction** : `fin_de_balise` suit les états de la balise dans la tokenisation (nom, avant l'attribut, attribut,
  après l'attribut, avant la valeur, valeur sans guillemets).
  - Une valeur entre guillemets se saute jusqu'au même guillemet.
  - Sans guillemet fermant ni `>`, la balise court jusqu'au bout du texte : une balise inachevée n'affiche rien.
  - Elle sert à l'ouvrante et à la fermante.
- **Tests** : 12, soit 7 mutants et 5 témoins.
  - Les 7 mutants sont rouges sur les états h, g et f (`journaux/rouge-j-etat-h.txt`).
  - Les témoins couvrent : un guillemet dans un nom, un `=` avant un nom, un guillemet dans une valeur sans guillemets,
    une valeur entre guillemets refermée, une fermante dont la valeur porte `>`.
- **Mutants** J01 à J13, tous tués. Le corpus ne compte aucune balise de script ou de style dont un `>` serait entre
  guillemets : DT15-j ne change rien au corpus actuel.
- **Borne écrite dans la doc de `retirer_non_affiche`** : rien n'est gardé en trop, hors d'un contenu SVG ou MathML,
  lu ici comme du HTML. Un `</script` ou un `</style` écrit dans un commentaire, une section CDATA ou une valeur
  d'attribut à l'intérieur d'un tel script ou style l'y clôt trop tôt.
  - Corpus : 1441 `<svg`, aucun `<math`, aucune section CDATA, aucun script dans un `svg`.
  - Les 6 styles des `svg` n'ont aucun `<` avant leur fermante : les deux lectures y donnent le même texte (L-9).

### P2.6 Rejeu, vérification, corpus

- **Rejeu pas à pas** sur l'extraction neuve de la base (`outils/rejouer_serie_p2.sh`, `journaux/rejeu.txt`, de
  12:22:11 à 12:23:29 UTC) :
  - `cargo test -p xtask`, cible par défaut, après a, c, d, g, h et j : `mutants` donne 87, 87, 106, 121, 127 puis 139
    tests, tous passés. `arbres` (3), `distillation` (7) et `reproductible` (9) restent verts. L'erreur de compilation
    du paquet `jouet` que montre `journaux/vert-j.txt` est voulue : c'est le cas `mutant-compilation` de
    `reproductible.rs`.
  - Les gates (`xtask gates`, lignes VERDICT) après a, c, d, e, g, h et j : tout est VERT sauf S-G9, dont la seule
    violation est `docs/17-modele-de-menace.md:70`, la borne de Q-6.
  - Après f : runner 137 ok, job `controle-unittest` conforme (`Ran 38`), `runners-epingles` conforme.
  - Les fichiers finals égalent ceux de `copie-travail`.
- **`cargo xtask verify`** sur l'état final (`journaux/verify-rejeu.txt`) : S-G1 à S-G8 VERT, S-G9 ROUGE
  (`docs/17:70` seule, Q-6), `cargo fmt --check` VERT, no_std VERT, `cargo clippy -D warnings` VERT.
- **s2-harness** (état final) : `Ran 419`, `OK (skipped=2)` (`journaux/s2-harness-rejeu.txt`).
- **Corpus complet de la session** : tête `f56b777`, plus la série, plus les octets de `biblio/` de la session (252
  entrées), jugés par le binaire de l'état final (`journaux/gates-corpus-tete-j.txt`).
  - S-G5 est **VERT** : 347 fragments contrôlés, 11838 écartés sous seuil, corpus INDEX plus 196 artefacts sur 196
    déclarés.
  - Les autres gates sont VERT, sauf S-G9 (`docs/17:70`, Q-6).
  - La copie qui portait ces octets est supprimée.

### P2.7 SHOGEN-PRESG5-QUADRATIQUE-1 : réponse et DT15-i

- **Réponse : oui, la cause est une boucle que le travail sur `sg5.rs` éclaire.**
  - `retirer_balises` de `presg5.py` recopiait le reste du texte à chaque `<`, par trois tranches Python (`reste[i:]`,
    `apres[1:]`, `apres[j + 2:]`). Le coût est donc quadratique en la taille de la page.
  - `scinder_crochets` avait la même forme.
  - Le débalisage de `sg5.rs`, qu'il imite, prend des tranches empruntées, sans copie, et n'a pas ce coût.
- **Correction (DT15-i)** : une lecture par indices. Le fermant se cherche dans la seule fenêtre
  (`t.find(">", k + 1, k + 302)` : la même borne de 300 caractères), et de même pour les crochets (fenêtre de 30).
- **Mesures** (`outils/presg5_mesure.py`, `journaux/presg5-mesure.out`) :
  - ancienne lecture : 1 000 000 de caractères en 13,75 s ; 2 000 000 au-delà de la borne de 20 s ;
  - nouvelle lecture : 8 000 000 de caractères en 0,31 s ;
  - égalité des sorties : 4071122 entrées comparées (exhaustif sur un petit alphabet, aléatoire, bords de fenêtre),
    0 écart.
- **De bout en bout** sur le corpus du dépôt, avec `docs/17` à contrôler (`journaux/presg5-bout-en-bout.txt`) :
  28,27 s avant, 4,58 s après, sorties identiques. Les 16 minutes sur une page de 5 Mo vont avec un coût quadratique,
  environ 25 fois celui d'une page de 1 Mo [inféré] ; je n'ai pas la page.
- **Tests** : `outils/test_presg5.py`, versé dans DT15-i, 3 tests.
  - Balises, puis crochets, en temps borné : 20 s pour 8 000 000 de caractères. Les deux sont rouges d'assertion sur
    l'ancien `presg5.py` (`journaux/rouge-presg5.txt`).
  - Valeurs de référence écrites à la main : vertes sur les deux versions ; ce test garde l'équivalence.
  - Les trois sont verts sur le nouveau, en 0,6 s (`journaux/vert-presg5.txt`).
  - Mutants : 12 sur 12 tués (`journaux/mutants-presg5.out`).
- **Application** : DT15-i s'applique depuis la racine du scratchpad (`git apply`). C'est contrôlé sur une copie : le
  résultat égale `presg5/apres`, et les tests y passent (`journaux/presg5-apply.txt`).

### P2.8 Phrases de fermeture proposées (bloc daté de l'annexe B)

- **SHOGEN-SG5-COMMENTAIRE-HTML-1**, phrase qui remplace celle du §4 : « Fermé par DT15-a, complété par DT15-g, DT15-h
  et DT15-j. S-G5 ôte des pages HTML et Markdown du corpus, avant le débalisage, ce qu'elles ne donnent jamais à lire :
  - les commentaires `<!-- … -->`, dont la fin suit la tokenisation HTML ;
  - les commentaires factices (`<!` sans `--`, `<?`, `</` suivi d'un caractère qui n'est ni une lettre ni `>`),
    jusqu'au premier `>`, sans borne de longueur ;
  - le contenu des éléments `script` et `style`, jusqu'à la fermante qui les clôt : casse ignorée, états de la
    tokenisation pour `script`, balises lues jusqu'à leur vrai `>`.
  Sans fin, la construction court jusqu'au bout du fichier. Ce qu'un script ou une interaction peut montrer reste au
  corpus. Les tests sont rouges d'assertion sur l'ancien code. 12 mutants de DT15-a et 39 de DT15-g à j, tous tués. Sur
  le corpus complet de la session, S-G5 est vert (347 fragments contrôlés). »
- **DT15-g (Q-5)** : « Le contenu des éléments `script` et `style` sort du corpus de S-G5 (DT15-g, adjudication Q-5,
  voie « aucune dette »). 15 tests, dont 5 rouges d'assertion sur DT15-f ; 17 mutants tués ; corpus complet vert. »
- **DT15-h (L-6)** : « L-6 fermée par DT15-h : les commentaires factices sont ôtés jusqu'au premier `>`, sans la borne
  de 300 octets. 6 tests, dont 5 rouges d'assertion ; 9 mutants tués ; le corpus n'en compte aucun hors DOCTYPE. »
- **DT15-j** : « DT15-j lit l'ouvrante et la fermante d'un script ou d'un style jusqu'à leur vrai `>`, hors des valeurs
  d'attribut entre guillemets. 12 tests, dont 7 rouges d'assertion ; 13 mutants tués ; aucun cas au corpus. »
- **SHOGEN-PRESG5-QUADRATIQUE-1**, si l'orchestrateur verse DT15-i : « Fermé par DT15-i (outil du scratchpad, hors
  dépôt). `presg5.py` lit par indices, fenêtre bornée : 8 000 000 de caractères en 0,31 s, contre plus de 20 s pour
  2 000 000 avant, et les sorties sont égales. 3 tests, dont 2 rouges d'assertion sur l'ancien outil ; 12 mutants
  tués. »

### P2.9 Questions et limites nouvelles

- **Q-8 — Balises longues (préexistant).** Le débalisage garde entière toute balise de plus de 300 octets : 2842 sur
  185540 dans les pages du corpus.
  - Par nom : `a` 1353, `path` 541, `div` 273, `span` 173, `button` 126, `img` 111.
  - Le texte de leurs attributs reste au corpus : adresses, tracés SVG, classes, `data-*`. Il n'est pas affiché, mais
    c'est rarement de la prose.
  - **Recommandation : former un item.** Le remède serait de débaliser les pages `html` et `htm` par les états de
    `fin_de_balise` (DT15-j), sans borne. La borne resterait pour le texte brut et le code, où `<` est souvent un signe.
  - Autre voie, si l'orchestrateur applique la règle « aucune dette » : un diff de plus dans ce lot.
- **Q-9 — Recherche du fermant sans fenêtre (préexistant).** `retirer_balises` de `sg5.rs` cherche le `>` jusqu'au
  bout du texte à chaque `<`. Le coût est quadratique au pire, pour un texte qui porte beaucoup de `<` sans `>` après
  eux.
  - Mesure sur le corpus (`outils/mesure_debalisage.py`) : 0,597 octet lu par octet en `html`, 1,782 en `md` ; le pire
    fichier est à 6,03.
  - **Recommandation : le même item que Q-8.** Le remède est une fenêtre de 301 octets, avec un test de temps.
- **L-9** : contenu SVG ou MathML lu comme du HTML (§P2.5). Le corpus n'en souffre pas.
- **L-10** : les règles de la tokenisation (commentaires, factices, états du script, états de la balise) viennent de
  ma connaissance [2nd]. Je ne les ai pas relues dans la spécification : aucun réseau dans ce lot. Les tests les
  figent.

### P2.10 Écarts (E-n)

- **E-8 : deux valeurs écrites à la main fausses dans `test_presg5.py`.** `<<b>` et `[[s]` avaient pour attendus `<`
  et `[…` ; la règle (du premier ouvrant au premier fermant) donne la chaîne vide et `…`.
  - Le premier passage sur l'ancien outil l'a montré. Je les ai corrigées d'après la règle, avant tout passage sur le
    nouveau.
  - Ce premier journal est écrasé : `journaux/rouge-presg5.txt` garde le dernier passage.
- **E-9 : taille du test de temps de `presg5` relevée.** La première campagne laissait vivant un mutant à une seule
  recopie par crochet : 9,5 s pour 2 000 000 de caractères, sous la borne de 20 s. La taille est passée à 8 000 000.
  La campagne refaite tue 12 mutants sur 12 ; son journal remplace le premier.
- **E-10 : la campagne finale ne tourne pas sur le texte exact de l'état final.** Elle a tourné sur une copie dont
  `sg5.rs` ne diffère de l'état final que par 4 lignes de doc, reformulées pendant la campagne (diff montré au journal
  de session).
  - La campagne de g et h (26 sur 26, `journaux/mutants-rust-p2.*`) a tourné sur l'état h.
  - La campagne finale (`journaux/mutants-rust-p2j.*`) compte 39 mutants sur 39 tués : P01 à P17, Q01 à Q09 et J01 à
    J13. L'ancre de P06, devenue double avec `fin_de_balise`, a été allongée.
- **E-11 : la charge vient aussi d'autres travaux.** J'ai lancé un seul processus lourd à la fois. D'autres travaux
  tournaient sur la machine : charge sur 1 min jusqu'à 3.74 (12:23:47 UTC).
- **E-12 : comptes de la phase 1 remplacés.** Les comptes de corpus de la phase 1 (788 `<script`, 15 `<!` factices)
  sont remplacés par ceux de §P2.3 et §P2.4, pris dans l'ordre du balayage.

### P2.11 Journal de provenance (G1)

**Sources lues** :
- [lu] `ADJUDICATION.md`, en entier.
- [lu] `xtask/src/sg5.rs`, aux états f à j ; dans `mutants.rs`, les aides de S-G5.
- [lu] `xtask/src/lib.rs` (étapes de `verify`) ; `xtask/tests/reproductible.rs` (cas `mutant-compilation`).
- [lu] `<scratchpad>/outils/presg5.py`, en entier.
- [lu] les deux TSV de DETTES-T14, par l'outil `verifier_registre.py`.
- [lu] les sujets des commits de la branche (`git log`) ; les comptes de lignes des 120 chemins suivis
  (`git diff --numstat`, liste explicite).
- [lu] les pages du corpus, par mesure seulement : aucun texte imprimé.
- [2nd] la tokenisation HTML (L-10).

**Commandes et sorties** (`journaux/`) :
- Rouges : `rouge-ghj-etat-f.txt`, `rouge-hj-etat-g.txt`, `rouge-j-etat-h.txt`. Les journaux antérieurs
  `rouge-g-etat-f.txt`, `rouge-h-etat-g.txt` et `rouge-gh-etat-f.txt` sont gardés, mais ils précèdent des tests
  ajoutés depuis.
- Verts : `vert-j.txt`.
- Mutants : `mutants-rust-p2.*`, `mutants-rust-p2j.*`, `mutants-presg5.out`.
- Rejeu : `rejeu.txt` et `rejeu-gates-*.txt`, `rejeu-controle-f.txt`, `verify-rejeu.txt`, `s2-harness-rejeu.txt`.
- Tête : `tete-apply.txt`, `tete-apply-final.txt`, `registre-tete.txt`, `tete-controles.txt`, `tete-controle-f.txt`.
- Corpus : `gates-corpus-tete-j.txt`, `mesure-corpus-p2.out`, `mesure-debalisage.out`.
- `presg5` : `presg5-mesure.out`, `rouge-presg5.txt`, `vert-presg5.txt`, `presg5-bout-en-bout.txt`,
  `presg5-apply.txt`.

**Chiffres recomptés** : tous sortent de ces fichiers ou des outils du dossier ; aucun n'est repris de seconde main.

### P2.12 Livrables

- `SHA256SUMS`, régénéré, couvre :
  - les diffs (`diffs/`, `diffs-hors-depot/`) ;
  - `NOTES.md` et ce rapport ;
  - les outils, les mesures et les journaux ;
  - les états gardés (`etats/`) ;
  - les deux versions de `presg5.py` (`presg5/`).
- Les copies de travail ne sont pas sommées : elles se refont par `outils/extraire.sh` et la série.

## Phase 3 — 2026-10-15 (rédaction à partir de 13:04:17 UTC, `date -u`)

Section ajoutée après l'ajout daté du 2026-10-15 12:39:11 UTC à `ADJUDICATION.md`, lu en entier (sha256 du fichier :
`6e16092dd579be72…`). Les sections précédentes ne sont pas réécrites.

### P3.0 Gate 0 et objet

- Modèle : **`claude-opus-5-5`** ; effort `max` demandé, non observable de l'intérieur. Rôle : générateur G1 de DT15-k.
- Objet : Q-8 et Q-9 se ferment dans ce lot (règle « aucune dette »). **Un seul diff, DT15-k**, porte les deux : R-25
  le permet, et la lecture des balises de Q-8 rend à elle seule la recherche du `>` linéaire (Q-9).

### P3.1 Série

| diff | fichiers | + / − | sha256 | contenu |
|---|---|---|---|---|
| DT15-a à h, j | inchangés (§2 et §P2.2) | | | |
| DT15-k | `xtask/src/sg5.rs`, `xtask/tests/mutants.rs` | +114 −32 | `ddc1b525…11de` | Q-8 et Q-9 : balises lues entières, sans borne, en temps linéaire ; 14 tests |

- **Empreinte de la concaténation** a…h, j puis k, dans cet ordre (91280 octets) :
  `8949734c888d31f8a8d887e69c207c4f2bb7420de3a58e41abdc040f15bf9046`. Celle de a…h, j, recalculée, reste `8f219939…`.
- R-25 : 114 lignes ajoutées. R-13 : aucun marqueur. Aucune ligne ajoutée au-delà de 120 caractères.
- Générateur : `outils/faire_diffs_p3.py`, depuis `etats/`. DT15-g, h, j et i en sortent identiques à l'octet.

### P3.2 Construction de DT15-k

- **`longueur_de_balise`** (neuve) : une balise est ce que la tokenisation HTML lit comme telle.
  - `<` suivi d'une lettre ASCII (ouvrante) ou `</` suivi d'une lettre ASCII (fermante) : lue par `fin_de_balise`
    (DT15-j) jusqu'à son vrai `>`, hors des valeurs d'attribut entre guillemets, **sans borne de longueur** ; sans
    `>`, jusqu'au bout du texte.
  - `</>` : 3 octets, que la tokenisation ignore.
  - Tout autre `<` (blanc, chiffre, signe, lettre non ASCII, `<!`, `<?`) : du texte.
- **`retirer_balises`** (le débalisage) a désormais la forme de `retirer_non_affiche` : tranches empruntées, et à
  chaque `<` soit une balise lue entière et ôtée, soit un `<` de texte gardé. Chaque octet est lu une fois : **temps
  linéaire** (Q-9). Le texte des attributs ne reste jamais au corpus (Q-8).
- **Première passe** (`retirer_non_affiche`, pages rendues) : une balise ordinaire y est recopiée entière pour le
  débalisage. Un `<!--`, un `<script` ou un `<!x` écrit dans une valeur d'attribut n'ouvre donc plus rien ; la doc ne
  compte plus les valeurs d'attribut parmi le texte ôté en trop.
- Ce qui change hors des pages rendues (texte brut, code, données) : seules les vraies balises sortent. `<` suivi
  d'autre chose qu'une lettre reste du texte ; à l'état j, il ouvrait une pseudo-balise si un `>` suivait à moins de
  300 octets.

**Mesure avant codage** (`outils/mesure_debalisage_k.py`, `journaux/mesure-debalisage-k.out` ; pages rendues lues dans
l'ordre du balayage, autres fichiers bruts) :
- html : 97118 ouvrantes et 88356 fermantes. 2844 ouvrantes ont leur vrai `>` à plus de 300 octets ; elles
  restaient au corpus à l'état j. 2861 sont lues autrement qu'à l'état j. Le compte de Q-8 (2842) prenait le premier
  `>` ; celui-ci prend le vrai.
- md : 1 ouvrante de plus de 300 octets.
- `<` de texte, ôtés à l'état j et gardés désormais : html 4, md 1, rs 46, txt 157.
- Aucune balise jamais close ; aucun `<!` ni `<?` hors des pages rendues.

### P3.3 Tests, rouges, mutants

- **14 tests** sur une fixture minimale : 6 mutants (ROUGE exigé), 7 témoins, 1 test de temps.
  - Mutants : attribut de plus de 300 octets, en `.html` et en `.txt` ; `>` entre guillemets ; `>` entre
    apostrophes ; balise jamais close ; fermante à long attribut.
  - Témoins :
    - `<` de texte suivi d'un blanc, puis d'une lettre non ASCII ;
    - texte entre balises, texte après la dernière balise ;
    - `</>` ôté ;
    - `<!--`, puis `<script`, écrits dans une valeur d'attribut.
  - Temps : une page de 4 000 002 octets de `x < y `, sans `>`, doit se juger en moins de 10 s (fil d'exécution et
    délai d'attente).
- **Rouges sur l'état j** (`journaux/rouge-k-etat-j.txt`) : 11.
  - 6 « S-G5 devait être ROUGE et ne l'est pas » ;
  - 4 « texte affiché perdu », car l'état j ôtait aussi du texte affiché ;
  - 1 « plus de 10 s ».
  - Les 3 autres témoins (texte entre balises, après la dernière, `</>`) sont verts sur j comme sur k.
- **État k** (`journaux/vert-k.txt`) : `mutants` 153 tests, tous passés. Le test de temps passe en 0,61 s, contre une
  borne de 10 s. `clippy -D warnings` et `fmt` sont verts.
- **Mutants K01 à K13** : borne de 300 octets remise ; balise close au premier `>` ; balise jamais close gardée ; tout
  `<` ouvre une balise ; lettre non ASCII prise pour un nom ; fermante non reconnue ; `</>` gardé ; première passe qui
  relit une balise octet par octet ; texte perdu avant une balise, ou après la dernière ; `<` de texte perdu ; relecture
  jusqu'au `>` à chaque `<` ; recopie du reste à chaque `<`. Le test de temps tue les deux derniers.
- **Campagne finale** (`journaux/mutants-rust-p3.*`) : 52 mutants sur 52 tués (P01 à P17, Q01 à Q09, J01 à J13, K01
  à K13), 0 FATAL, témoins vivants.

### P3.4 Rejeu, vérification, corpus, tête

- **Rejeu pas à pas** (`outils/rejouer_serie_p3.sh`, `journaux/rejeu-p3.txt`, de 13:00:47 à 13:02:07 UTC) : il part
  d'une extraction neuve de la base (1371 membres).
  - `cargo test -p xtask`, cible par défaut, après a, c, d, g, h, j et k : `mutants` donne 87, 87, 106, 121, 127, 139
    puis 153 tests, tous passés.
  - Gates : S-G1 à S-G8 VERT à chaque pas contrôlé ; S-G9 n'a que `docs/17:70` (Q-6).
  - Après f : runner 137 ok, `controle-unittest` conforme (`Ran 38`), `runners-epingles` conforme.
  - Les fichiers finals égalent ceux de `copie-travail`.
- **`cargo xtask verify`** (`journaux/verify-rejeu-k.txt`) : S-G1 à S-G8 VERT ; S-G9 ROUGE, par `docs/17:70` seule ;
  fmt, no_std et clippy VERT.
- **s2-harness** : `Ran 419`, `OK (skipped=2)` (`journaux/s2-harness-rejeu-k.txt`).
- **Corpus complet de la session** : tête `8b3ead36d390f0a713e5649456892d28d4af24ec`, plus la série a…k, plus les
  octets de `biblio/` (252 entrées) (`journaux/gates-corpus-tete-k.txt`).
  - S-G5 est **VERT** : 347 fragments contrôlés, 11838 écartés sous seuil, 196 artefacts sur 196.
  - Les autres gates sont VERT, sauf S-G9 (`docs/17:70`). La copie est supprimée.
- **Contrôles de DT15-f** à cette tête (`journaux/tete-controles.txt`) : conformes (7 workflows, `Ran 38`, 137 ok).
- **Tête du moment** : `17d0d2895d34e73798684a8c8403a24140e2c6fe`, 13:04:03 UTC (`journaux/tete-apply-final.txt`).
  - Les dix diffs passent `git apply --check` puis `git apply`.
  - Les fichiers égalent ceux du rejeu, sauf `gates.yml`, qui ne diffère que des planchers de la tête (`s2bis` 373,
    `calib-actifs` 78).
  - Le registre y est conforme (`journaux/registre-tete-final.txt`).
  - Têtes vues pendant la phase : `a83b74fb570fcff5220494f164024a4cb4d63da4`, `8b3ead3…`, `17d0d28…`. Parmi les 120
    chemins suivis, seuls les planchers de `gates.yml` y changent.
- **Dernière tête, 13:06:24 UTC** : `9b83a00f7294db73785ce53a4aca43e6b0a15d50`. Aucun des 120 chemins n'y change depuis
  `17d0d28` ; les dix diffs passent `git apply --check` puis `git apply`, et les fichiers égalent ceux du rejeu hors des
  planchers (`journaux/tete-apply-9b83a00.txt`).

### P3.5 Phrases de fermeture proposées (bloc daté de l'annexe B)

- **Q-8** : « Fermée par DT15-k. Le débalisage de S-G5 lit une balise (`<` ou `</` suivi d'une lettre ASCII) jusqu'à
  son vrai `>`, hors des valeurs d'attribut entre guillemets, sans borne de longueur. Une balise jamais close court
  jusqu'au bout du fichier ; `</>` sort ; tout autre `<` est du texte. Le texte des attributs ne reste jamais au corpus.
  Dans une page rendue, la première passe lit aussi les balises entières : une valeur d'attribut n'ouvre ni commentaire
  ni script. 14 tests, dont 11 rouges sur l'état j ; 13 mutants tués ; corpus complet vert (347 fragments). »
- **Q-9** : « Fermée par DT15-k. La recherche du `>` est linéaire : chaque octet est lu une fois, sans recopie. Une
  page de 4 000 002 octets de `x < y ` se juge en 0,61 s, contre plus de 10 s à l'état j : ce test de temps borné est
  rouge sur j. Les deux mutants qui rendent la lecture quadratique sont tués. »
- **SHOGEN-SG5-COMMENTAIRE-HTML-1** : la phrase de §P2.8 reste, à un compte près. Au lieu de « 39 de DT15-g à j », lire
  « 52 de DT15-g à k ».

### P3.6 Limites

- **L-11** : hors des pages rendues, seules les vraies balises sortent du corpus.
  - En `xml` (aucun fichier au corpus), une déclaration, une instruction ou un commentaire restent du texte. C'est la
    règle de Q-4 pour les commentaires ; à l'état j, le débalisage les ôtait s'ils faisaient moins de 300 octets.
- **L-12** : en Markdown, un `<` suivi d'une lettre que CommonMark affiche comme du texte (pas de balise valide) se lit
  ici comme une balise : c'est du texte ôté en trop. Au corpus, aucune balise `md` n'est jamais close.
- L-9 et L-10 : inchangées (§P2.9 ; adjudication du 2026-10-15 12:39:11).

### P3.7 Écarts (E-n)

- **E-13 : une campagne interrompue.** Une première campagne de phase 3 tournait sur une version de DT15-k qui ne
  touchait que le débalisage. Je l'ai arrêtée à J03 (12:52:21 UTC) pour ajouter la lecture entière des balises dans la
  première passe. Elle n'est pas comptée (`journaux/mutants-rust-p3-interrompue.out`).
- **E-14 : le passage provisoire sur le corpus est remplacé.** Ce passage, fait à 12:48 UTC sur la tête `a83b74f…`
  avec cette version, était vert (347 fragments, `NOTES.md`). Son journal a été remplacé par le passage final.
- **E-15 : un témoin réécrit.** Sa citation porte désormais le `<` : sans cela, un mutant qui perd un `<` de texte
  survivait. Les rouges et les verts ont été refaits ensuite.
- **E-16 : outil de mesure rendu autonome.** `mesure_debalisage_k.py` importait d'abord `mesure_corpus_p2.py`, dont le
  `main()` tournait à l'import et imprimait ses comptes en tête du journal. L'outil est désormais autonome, et le
  journal est refait.
- **E-17 : une commande refusée.** La vérification de sûreté du harnais a refusé une commande qui joignait un script
  `bash -c` et une suppression. J'ai relancé les contrôles sans script. Puis j'ai supprimé seule, par son chemin
  littéral, la copie qui portait les octets de `biblio/`.
- **E-18 : le test de temps est rouge sur j, non sur k.** Le message demandait un test rouge sur l'état k : il supposait
  deux diffs. Un seul diff porte Q-8 et Q-9, donc le rouge se montre sur l'état j.
- **E-19 : charge.** J'ai lancé un seul processus lourd à la fois ; la charge sur 1 min est montée jusqu'à 3.87
  (12:52:27 UTC).

### P3.8 Journal de provenance (G1)

- [lu] l'ajout daté de 12:39:11 à `ADJUDICATION.md`, en entier ; `xtask/src/sg5.rs` à l'état j (débalisage, boucle du
  corpus, extensions) ; les aides de S-G5 de `mutants.rs` et `tests/commun/mod.rs` (`Arbre`).
- [lu] les pages du corpus, par mesure seulement, sans texte imprimé.
- [2nd] la tokenisation HTML (L-10).
- **Journaux** : `mesure-debalisage-k.out`, `rouge-k-etat-j.txt`, `rouge-k2-etat-k1.txt` (témoins de la première
  passe, rouges sur la version provisoire), `vert-k.txt`, `mutants-rust-p3.*`, `rejeu-p3.txt`, `rejeu-gates-*.txt`,
  `verify-rejeu-k.txt`, `s2-harness-rejeu-k.txt`, `gates-corpus-tete-k.txt`, `tete-apply-k.txt`, `tete-controles.txt`,
  `tete-apply-final.txt`, `registre-tete-final.txt`.
- **Chiffres recomptés** : tous sortent de ces fichiers ou des outils du dossier.

### P3.9 Livrables

- `diffs/DT15-k.diff` ; `etats/sg5-k.rs` et `mutants-k.rs` ; outils `faire_diffs_p3.py`, `mutants_rust_p3.py`,
  `rejouer_serie_p3.sh` et `mesure_debalisage_k.py`.
- `SHA256SUMS` est régénéré. Les copies `copie-travail` et `copie-rejeu` sont gardées, sources seules ; cibles cargo
  et copies de tête supprimées.

## Phase 4 — 2026-10-15 (rédaction à partir de 21:10:43 UTC, `date -u`)

Section ajoutée après les ajouts datés de 15:05:10 (G2 neuve, C-1 à C-10) et de 16:37:17 (contre-contrôle, R-1 à R-8)
à `ADJUDICATION.md`, lus en entier (sha256 du fichier : `b19bbc5a…`). Les sections précédentes ne sont pas réécrites.

### P4.0 Gate 0 et objet

- Modèle : **`claude-opus-5-5`** ; effort `max` demandé, non observable de l'intérieur. Rôle : générateur G1 de DT15-m.
- Objet : DT15-m, port de DT15-i dans `scripts/controle/presg5.py` du dépôt, tel que la chaîne GARDE-FOUS l'a laissé
  (GF-2, GF-2b, C-10, C-18 de sa G2). DT15-m s'applique après toute la série de commit.

### P4.1 État de départ : tête neuve et série de commit

- **Tête de départ** : `9dbf69279c2a8ce7959281108d1450f163a76670` (versement de la phase 1 de GARDE-FOUS-ORCH),
  extraite par `outils/extraire.sh` (1448 membres, 0 écarté).
- **C-10 refait** à cette tête par `outils/c10_p4.py` : c'est `g2/outils/c10_generique.py`, avec R-5 puis R-8
  appliqués par `git apply`, et ses sorties redirigées vers mon dossier. Il ne diffère de `g2/cc/outils/c10_r8.py` que
  par ces chemins.
  - Date du recalage : 2026-10-15 20:18:02 UTC (`date -u`).
  - Sortie : plancher 115 → 116 ; dernier ajout du README daté 2026-10-15 11:48:38 UTC.
  - `phase4/C-10-9dbf692.diff` (`0ac8be64…`).
- **Série appliquée dans l'ordre de l'ajout de 16:37:17** : DT15-a à e, C-10, DT15-g, h, j, k, C-2 à C-7 et C-9, R-1 à
  R-4 et R-6 (`journaux/p4-serie.txt`).
  - Les 22 diffs passent `git apply --check`, puis `git apply`.
  - C-n et R-n sont égaux à l'octet aux `SHA256SUMS` de la G2 et du contre-contrôle (`sha256sum -c`).
- **Ligne exacte du job** sur cet état : `controle-unittest` conforme, `Ran 116` (plancher 116 ;
  `journaux/p4-depart.txt`).

### P4.2 DT15-m

| diff | fichiers | + / − | sha256 |
|---|---|---|---|
| DT15-m | `scripts/controle/presg5.py`, `tests/test_presg5_lineaire.py` (neuf), `scripts/controle/README.md`, `gates.yml` | +110 −26 | `7403df17…759d` |

- **`presg5.py`** : `retirer_balises` et `scinder_crochets` sont celles de DT15-i, prises à l'octet par leur arbre
  dans `presg5/apres`. Une phrase s'ajoute à la doc du module. Le reste du fichier est inchangé, sorties 0, 1 et 3
  comprises.
- **Test portable**, `tests/test_presg5_lineaire.py` (3 tests) : l'outil est trouvé par `importlib.util.find_spec`,
  dans le chemin d'import de la suite, à côté de `garde_commun.py`, puis chargé comme un module. Le fichier ne lit
  jamais `__file__` : le chargeur de DT15-i levait `NameError` ici (G2).
  - Deux tests de temps : 8 000 000 de caractères en sous-processus (`-X dev -W error -I -B`), arrêtés à 20 s.
  - Un test de valeurs de référence, écrites à la main.
- **`gates.yml`** : le plancher de `controle-unittest` passe de 116 à 119 (`--egal`), avec deux lignes de commentaire.
- **README** : un ajout daté en fin, 2026-10-15 21:00:52 UTC (`date -u` lu à l'écriture), après celui de C-10.
  `garde/lignes-citees.txt` n'y admet qu'un ajout en fin.

### P4.3 Preuves

- **Rouge sur l'ancien code** (`journaux/rouge-m-avant.txt`) : les deux tests de temps échouent d'assertion (`plus de
  20 s pour 8000000 caractères`) ; le test des valeurs est vert, car l'ancienne lecture donne les mêmes valeurs.
- **Vert sur le nouveau** (`journaux/vert-m.txt`) : les 10 tests de `presg5` passent en 1,52 s, dont la sortie dorée
  (sha256 épinglé) de `tests/test_presg5.py`.
- **Ligne exacte du job sur l'état final** : conforme, `Ran 119` (`journaux/p4-final.txt`).
- **Mutants** (`outils/mutants_presg5_m.py`, `journaux/mutants-presg5-m.*`) : 12 sur 12 tués, chacun par la ligne exacte
  du job (sortie 1), 0 FATAL ; témoins en sortie 0. Mutants :
  - les deux fenêtres, élargies ou réduites d'un caractère ;
  - le saut après la balise ;
  - le chevron perdu ;
  - une recherche sans fenêtre ;
  - l'élision inversée ;
  - le reste perdu, le chevron sauté ;
  - deux recopies quadratiques, tuées par les tests de temps.
- **Matrice** (`outils/matrice_m.sh`, `journaux/matrice-m.txt`) : sous Python 3.10.20, 3.11.15, 3.12.3 et 3.13.14,
  la suite tourne en `-X dev -W error` : `Ran 119`, OK, 0 avertissement ; la ligne du job est conforme.
- **Contrôles de `enforcement/`** (`journaux/p4-enforcement.txt`, Python 3.12 en `-X dev -W error`), tous conformes :
  - runner du vérificateur : 137 ok ;
  - `workflows-yaml` : 16 cas ; 7 workflows conformes ;
  - `runners-epingles` ; `docs-sha256sums` ; `journaux-modele`.
- **Sorties identiques sur le corpus du dépôt** (`outils/presg5_corpus.py`, `journaux/presg5-corpus-*`).
  - Ancienne et nouvelle version, racine `/home/user/shogen`, sur 35 documents de `docs/` en liste explicite
    (`phase4/fichiers-presg5.txt`, aucun interdit).
  - Les 201 textes de corpus ont le même sha256 un à un, et le résultat est le même (0 fragment introuvable). Les deux
    sorties sont identiques à l'octet (`d455794e…`).
  - Le corpus se lit en 990,86 s avant, 5,12 s après. `biblio/` porte désormais une page de 5 247 633 octets, de la
    taille de la page des 16 minutes [inféré : je ne l'ai pas chronométrée seule].

### P4.4 DT15-m à une autre tête

- DT15-m dépend du C-10 de la même tête, par ses lignes de contexte : le commentaire de C-10 dans `gates.yml` nomme la
  tête, et l'ajout daté de DT15-m doit suivre celui de C-10. Le diff fixe s'applique donc après `C-10-9dbf692`.
- **À une autre tête, DT15-m se refait** par `outils/m_generique.py <copie> "<date UTC>" <sortie>`, après C-10, avec le
  `date -u` du moment.
  - Sur l'état de départ gardé (`etats/p4-avant`), avec la date 2026-10-15 21:00:52, il redonne `diffs/DT15-m.diff` à
    l'octet.
  - Il refuse une date antérieure au dernier ajout (`journaux/m-generique-reproduction.txt`).
- **Tête du moment** : `7b8f999c3bc8e4698d68f899a7daa036db34748c` (DETTES-T7 DT7-d), 21:09:44 UTC
  (`outils/tete_p4.sh`, `journaux/tete-p4.txt`).
  - Extraction : 1459 membres.
  - C-10 refait : 116, daté 21:09:45 ; les 22 diffs de la série passent `--check`, puis s'appliquent.
  - DT15-m refait (daté 21:09:46) passe `--check`, puis s'applique ; `presg5.py` et le test neuf sont égaux à l'état
    final.
  - Ligne du job conforme, `Ran 119`.
  - Les deux DT15-m ne diffèrent que par la date de l'ajout et la tête nommée en contexte.

### P4.5 Empreintes

- **Série du générateur** a…h, j, k, m, dans cet ordre (100868 octets) :
  `28bcc83c51384ca42684371a3f2860c667118975c15f923335a14f309bc37344`. Celle de a…h, j, k reste `8949734c…`.
- **Série de commit construite**, à titre de contrôle : 23 diffs, dans l'ordre de l'ajout de 16:37:17, avec
  `C-10-9dbf692`, puis DT15-m (153668 octets) : `dcb09d898dbc831914c249a22b69cec684a3eee29f94b0f1a2837b7ec259daaa`.
  C-10 et DT15-m se refont à la tête de la chaîne : cette empreinte vaut pour `9dbf692` seulement.

### P4.6 Phrase de fermeture proposée (bloc daté de l'annexe B)

- **SHOGEN-PRESG5-QUADRATIQUE-1** : « Fermé dans le dépôt par DT15-m (port de DT15-i, versé au scratchpad).
  `scripts/controle/presg5.py` lit les balises et les crochets par indices, le fermant cherché dans la seule fenêtre :
  le corpus du dépôt se lit en 5,12 s au lieu de 990,86 s, avec des sorties identiques avant et après (201 textes de
  corpus, mêmes sha256). Trois tests portables : deux tests de temps rouges sur l'ancien code, des valeurs de
  référence. 12 mutants tués par la ligne exacte du job `controle-unittest`, plancher 119 (`--egal`), matrice 3.10 à
  3.13 en `-X dev -W error`. »

### P4.7 Écarts (E-n)

- **E-20 : deux comparaisons interrompues.** La première tournait en `-X dev` : l'allocateur de débogage ralentit les
  recopies de l'ancienne lecture, et je l'ai arrêtée après plus de 10 min. La seconde calculait le corpus deux fois ;
  arrêtée à 10 min 52 s. Aucune n'est comptée (`journaux/presg5-corpus-avant-*-interrompu.err`). La comparaison
  retenue tourne en `-W error -I -B`, sans `-X dev` ; la matrice garde `-X dev -W error` pour la suite.
- **E-21 : `avant_acte.py diff --fichier` non lancé.** Il écrit son journal sous le dossier git du dépôt, que je ne
  touche pas, et D2 exige un diff applicable sur HEAD seul, ce que DT15-m n'est pas (il suit la série). La chaîne de
  commit le lance.
- **E-22 : le chemin de l'outil de C-10 diffère du message.** Le message nommait `g2/cc/outils/c10_generique.py`, qui
  n'existe pas. J'ai pris `g2/outils/c10_generique.py` corrigé par R-5 et R-8 ; c'est le code de
  `g2/cc/outils/c10_r8.py` (diff montré au journal). Ses sorties vont dans mon dossier, jamais dans ceux des relecteurs.
- **E-23 : la tête a bougé pendant le travail.** La chaîne DETTES-T7 committait : la tête est passée de `9dbf692` à
  `7b8f999`. J'ai lancé un seul processus lourd à la fois.

### P4.8 Journal de provenance (G1)

- [lu] les ajouts datés de 13:07:03, 15:05:10 et 16:37:17 à `ADJUDICATION.md`. Dans `g2/RAPPORT-G2.md`, le passage du
  port de `presg5` et la `NameError` ; dans `g2/NOTES.md`, l.35-45 ; dans `g2/cc/RAPPORT-CC.md`, §2, §3, §9 et §10.
- [lu] les outils de C-10 (`g2/outils/c10_generique.py`, `g2/cc/outils/c10_r8.py`, R-5, R-8), `appliquer.sh` et
  `tete_serie.sh`.
- [lu] à la tête : `scripts/controle/presg5.py` en entier ; le début de `tests/test_presg5.py` ;
  `garde/lignes-citees.txt` ; le job `controle-unittest` de `gates.yml` ; l'en-tête de
  `enforcement/verdict-suite-s2.py` et de `scripts/controle/avant_acte.py`.
- [lu] le corpus de `biblio/` du dépôt, par mesure seulement.
- **Journaux** : `p4-serie.txt`, `p4-depart.txt`, `c10-9dbf692.txt`, `rouge-m-avant.txt`, `vert-m.txt`,
  `p4-final.txt`, `mutants-presg5-m.*`, `matrice-m.txt` et `matrice-m/`, `p4-enforcement.txt`, `presg5-corpus-*`,
  `m-generique-reproduction.txt`, `tete-p4.txt` et `tete-p4-7b8f999-controle.txt`.
- **Chiffres recomptés** : tous sortent de ces fichiers ou des outils du dossier.

### P4.9 Livrables

- `diffs/DT15-m.diff`.
- `phase4/` : `C-10-9dbf692.diff`, `C-10-7b8f999.diff`, `DT15-m-7b8f999.diff`, `fichiers-presg5.txt`.
- `etats/p4-avant/`, `etats/presg5-m.py`, `etats/test_presg5_lineaire.py`.
- Outils : `c10_p4.py`, `m_generique.py`, `tete_p4.sh`, `mutants_presg5_m.py`, `matrice_m.sh`, `presg5_corpus.py`,
  `presg5_corpus_compare.sh`, `faire_diff_m.py`.
- `SHA256SUMS` est régénéré. La copie `copie-p4-serie` (état final, sources seules) est gardée ; les autres copies de la
  phase sont supprimées.
