# Relecture G2 neuve de DETTES-T15 (C-1 à C-10) (transcrit)

> Transcription par l'orchestrateur le 2026-10-16 07:29:19 UTC du fichier dettes15/g2/RAPPORT-G2.md ; contrôle FM-1.1 des transcripts du générateur (phases 1 à 4), du réviseur G2 et du contre-contrôleur, par le fm11.py versé et par celui de DT3-E : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Relecture G2 neuve — lot DETTES-T15 (S-G5, registre des renvois de S-G9, FLOTTANT)

Rédaction commencée le 2026-10-15 à 14:19:20 UTC (`date -u`) ; départ de la passe à 13:07:55 UTC.

## 0. Gate 0, rôle, cadre

- Modèle : **`claude-opus-5-5`**, identifiant exact donné par l'environnement de la session ; effort `max` demandé par
  l'orchestrateur, non observable de l'intérieur.
- Rôle : réviseur G2 neuf. Je n'ai écrit ni relu aucun diff de la série avant cette passe.
- Brief relu après le message de l'orchestrateur (`g2/BRIEF-G2.md`, 9136 octets, sha256 en `SHA256SUMS`). Les trois
  ajouts datés de `ADJUDICATION.md` sont lus et priment.
- Dépôt en lecture seule (`git --no-optional-locks`, aucune écriture git dans le dépôt ; un `git init` dans un dossier
  jetable de `g2/`, déclaré en E-6). `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée. Seul appel réseau : la page WHATWG
  nommée au brief, par `curl` à travers le mandataire. Tout ce que j'ai écrit est sous `g2/` (copies, cibles cargo,
  journaux), hors les fichiers de sortie que l'outil des tâches de fond tient lui-même.
- Enregistrement du rôle G2 par `oracle_record.py` : sans objet. La règle vise les lots du chemin S2 (dossier du cp-2),
  et ce lot ne touche aucun fichier de `s2-harness/`.

## 1. Verdict

**ACCEPTE-AVEC-CORRECTIONS**, liste fermée **C-1 à C-10** (§11). Les diffs DT15-a à k et DT15-i font ce qu'ils annoncent,
à quatre défauts près, tous corrigeables dans le lot :

- **C-4** (registre, Q-7). Trois entrées gardent un autre passage que celui que leur document cite :
  PAQUET-PREREG-S2 l.56 et l.63, CP1-PAQUET l.101. Ce sont des renvois à doc 10 recopiés d'ADR-0028 après que
  `4d49757` a inséré quatorze lignes dans doc 10. Un repère du paquet manque aussi au registre (l.57). **C-4 amende
  l'adjudication Q-2** (le paquet se lit à `8b14567`) : à adjuger.
- **C-3** (sûreté). La gate lisait le document citant et hachait les lignes citées d'une entrée qui nommerait un
  emplacement interdit. Le registre n'en porte aucune, mais le code ne le refusait pas.
- **C-6** (S-G5, sens dangereux). Un `<!--` ou un `<script` écrit dans un `title`, un `textarea` ou un `iframe` (texte
  pour la tokenisation) pouvait se clore dans un script ou un commentaire vrai, et en laisser la fin au corpus. La doc
  disait pourtant « jamais gardé en trop, hors SVG ou MathML ». Aucun cas au corpus réel.
- **C-2** (L-10). La page lue contredit le mot « commentaire factice » pour `<?`. C'est une instruction de traitement
  (13.2.5.72 à 13.2.5.76), close elle aussi au premier `>` : le code est juste, la doc et les phrases ne le sont pas.

Le reste de la liste : la rangée de l'INDEX demandée (C-1), trois tests contre des mutants vivants (C-5), la phrase de
DT15-e (C-7), les phrases de fermeture (C-8), la commande de rejeu en tête du registre (C-9) et DT15-f recalé sur la
dernière tête (C-10) : à `4543667`, le lot GARDE-FOUS a porté le plancher de `controle-unittest` à 60 et écrit en fin
du README des contrôles, et DT15-f ne s'y applique plus. Le même lot a versé dans le dépôt l'ancien `presg5.py`
(`scripts/controle/presg5.py`, GF-2), puis en a fait un outil sans toucher à sa lecture (GF-2b) : la lecture
quadratique que corrige DT15-i y reste (plus de 20 s sur 8 000 000 de caractères). Porter DT15-i dans le dépôt est un
item à former, à adjuger (§10).

## 2. Série, empreintes, têtes

- **Empreintes recalculées** (concaténation dans l'ordre) : a à f `cb06725a…6032`, a à h puis j `8f219939…d425`,
  a à h, j, k `8949734c…9046` (91 280 octets) : égales à celles des phases 1 à 3. DT15-i : `575a6a09…320a`. Chaque
  sha256 de diff égale celui du rapport.
- **`SHA256SUMS` du générateur** : tout conforme sauf `ADJUDICATION.md`, réécrit par l'orchestrateur à 13:07:03, après
  les sommes de 13:06 (attendu).
- **Têtes vues** : `9b83a00` au départ (13:07), `6117ea1` (DETTES-T16 versé) à 13:52, `d66e8b6` à 14:13, `f3a43b9` à
  14:32, `3ad8d9d` à 14:41, `0e30330` à 14:54, `4543667` à 15:01. Sur les trois premières, les dix diffs passent `git apply --check` puis `git apply`, et
  les fichiers obtenus égalent ceux de ma copie de série, hormis le plancher `s2bis` de la tête (373 puis 374). À
  `f3a43b9`, puis à `3ad8d9d`, `0e30330` et `4543667`, DT15-f ne s'applique plus (§12, C-10). Entre `6117ea1` et `d66e8b6`, parmi les chemins de la série et
  les cibles du registre, seuls `JOURNAL.md` et l'annexe B changent, par ajouts. La troisième voix reste à 0 écart sur
  la copie finale. La dernière relecture de la tête est au §12.
- **Copies** : `git archive` avec les exclusions des interdits, puis un filtre à moi qui n'imprime que des comptes
  (`outils/extraire_g2.sh`, `filtre_tar.py` : 1396, 1401, 1416, 1420, 1421 puis 1423 membres, 0 écarté au filtre).
- **Forme** : au plus 198 lignes ajoutées par diff (R-25) ; aucun marqueur TODO, FIXME ou XXX ajouté (R-13) ; aucune
  ligne ajoutée au-delà de 120 caractères, hors de la ligne datée de docs/17 (un paragraphe par ligne, comme les ajouts
  précédents de ce document) et des lignes du registre.

## 3. Point 1 — phrases de fermeture

| phrase | jugement |
|---|---|
| §4 et §P2.8, SHOGEN-SG5-COMMENTAIRE-HTML-1 | inexacte sur trois points : `<?` n'ouvre pas un commentaire factice mais une instruction de traitement (C-2) ; « les tests sont rouges d'assertion sur l'ancien code » ne vaut que pour les tests mutants, 32 des 53 tests neufs, les 21 autres étant des témoins verts ; « 347 fragments » vaut à la tête du générateur, 353 aux têtes `6117ea1` et `d66e8b6`. Forme corrigée en C-8, avec C-6. |
| §P2.8, DT15-g | vraie : 5 des 15 tests rouges d'assertion sur l'état f (rejeu). |
| §P2.8, DT15-h | vraie pour l'effet (5 rouges sur l'état g ; corpus : 80 DOCTYPE, aucun autre factice) ; ajouter les instructions de traitement (C-2). |
| §P2.8, DT15-j | vraie : 7 des 12 tests rouges sur l'état h. |
| §P2.8, SHOGEN-PRESG5-QUADRATIQUE-1 (DT15-i) | vraie pour le `presg5.py` du scratchpad (§10) ; fausse pour le dépôt tant que DT15-i n'y est pas porté : l'outil de GF-2b garde la lecture quadratique (C-8). |
| §P3.5, Q-8 et Q-9 | vraies : 11 des 14 tests rouges sur l'état j, dont le test de temps (`plus de 10 s`) ; seul le compte de fragments est à mettre à jour (353). |
| §4, SHOGEN-REFS-LIGNE-CONTENU-1 | fausse sur le paquet : « son texte est retrouvé deux lignes plus bas » est faux pour deux des trois entrées (§5.1) ; « 19 tests, rouges sur l'ancien code » : 18 des 19 ; les 77 références sont aussi hors MONARK. Forme corrigée en C-8, avec C-3 et C-4. |
| §4, SHOGEN-RUNNERS-FLOTTANT-QUADRATIQUE-1 | vraie à la tête du générateur ; L-7 se ferme et s'ajoute à la phrase ; à `4543667`, le plancher n'est plus 38 mais 61 (C-10, C-8). |

## 4. Point 2 — S-G5 (`xtask/src/sg5.rs`, lu en entier, 630 lignes à l'état k)

### 4.1 Règle lue

Pièce : `pieces/whatwg-html-parsing.html`, URL exacte `https://html.spec.whatwg.org/multipage/parsing.html`, reçue le
2026-10-15 à 13:10:50 UTC (HTTP 200, `last-modified: Wed, 14 Oct 2026 06:15:46 GMT`), 826 098 octets, sha256
`aeb8d0c0…5d97`. En-tête de page : « Living Standard — Last Updated 14 October 2026 ». **Licence : aucune mention sur
la page multipage** (aucune occurrence de « licen », « copyright », « © ») : « aucune licence lue ». Texte de §13.2.5
extrait par `outils/whatwg_texte.py` (`pieces/whatwg-tokenisation.txt`) ; métadonnées dans
`pieces/whatwg-html-parsing.META.txt`.

Comparaison du code à la règle, état par état ; chaque règle du générateur [2nd] passe à [lu], sauf `<?` :

| construction | règle lue (états) | code | verdict |
|---|---|---|---|
| commentaire `<!--` | 13.2.5.43 à 13.2.5.52 : `>` ou `->` juste après `<!--` clôt un commentaire vide ; ensuite, l'état de fin n'est atteint qu'après `--` (y compris le `<!--` imbriqué, 13.2.5.46 à 49), et un `>` ne clôt qu'après `--` ou `--!` ; fin de fichier : rien d'affiché | `fin_de_commentaire` : premier `-->` ou `--!>` du corps, recherche chevauchante | égal, vérifié transition par transition (`--->`, `--!-->`, `<!---!>`, `<!-->` imbriqué) ; [lu] |
| `<!` sans `--` | 13.2.5.42 : DOCTYPE (13.2.5.53 à 68 : tout `>` rend aux données, même entre guillemets), `[CDATA[` hors contenu étranger et tout autre : commentaire factice, clos au premier `>` (13.2.5.41) | premier `>` | égal ; [lu] |
| `</` suivi d'une non-lettre | 13.2.5.7 : `>` ignoré (`</>`), fin de fichier : `</` affiché, sinon commentaire factice | factice sauf `</>` et fin de texte | égal ; [lu] |
| `<?` | **13.2.5.6 et 13.2.5.72 à 76 (page du 2026-10-14)** : instruction de traitement ; cible invalide, `xml` ou `xml-stylesheet` : commentaire factice ; toutes les voies finissent au premier `>`, et une fin de fichier n'affiche rien | factice, premier `>` | **effet égal, mot faux** : C-2 |
| balise ouvrante ou fermante | 13.2.5.6 à 8, 13.2.5.32 à 40 : nom, attributs, valeur nue, entre guillemets ; `>` entre guillemets ne clôt pas | `fin_de_balise` | égal pour la position du `>`, chaque transition comparée ; [lu] |
| `script` | 13.2.5.4 et 13.2.5.15 à 31 : données, échappé après `<!--`, doublement échappé après `<script` + frontière, `-->` rend aux données, fermante appropriée (casse pliée, blanc, `/` ou `>`) | `fin_d_element`, trois états | égal ; seule différence, `</script` en fin de fichier, sans effet (tout est ôté dans les deux lectures) ; [lu] |
| `style` | RAWTEXT, 13.2.5.3 et 13.2.5.12 à 14 : première fermante appropriée, aucun état échappé | idem | égal ; [lu] |
| éléments de texte brut | §13.2.6, balises ouvrantes : `title`, `textarea` en RCDATA ; `xmp`, `iframe`, `noembed`, `noframes`, `style` en RAWTEXT ; `noscript` en RAWTEXT si le script n'est pas désactivé, sinon balisage ; `plaintext` en PLAINTEXT | **non lus** : un ouvreur écrit dedans est pris pour un vrai | **écart, sens dangereux possible** : C-6 |

### 4.2 Sens de l'erreur

Formes du brief, une à une : `</script >` et `</SCRIPT>` closent (frontière blanc, casse pliée ; tests et mutants S08,
S09 tués) ; un `>` dans une valeur d'attribut ne clôt rien (DT15-j et k ; S13, S14 tués) ; fermante absente : ôté
jusqu'au bout ; `<!--` dans un script et double échappement : suivis (S05, S06 tués ; S04, fermante dans l'état
échappé, était vivant : C-5) ; entités : `&lt;script&gt;` n'ouvre rien, et c'est juste, la page l'affiche ; CDATA hors
contenu étranger : commentaire factice, juste ; `<style>` dans un bloc de code Markdown : ôté en trop (sens sûr), sauf le
cas de L-13.

**Faux vert trouvé (C-6)** : `<title><!--</title><script>var s = "-->CACHÉ";</script>` laisse `CACHÉ";` au corpus.
L'ouvreur écrit dans le titre se clôt sur le `-->` du script vrai. Même mécanisme avec `textarea` et `iframe`. Constaté
sur le code de la série par ma réécriture Python et par trois tests rouges (§7). C-6 lit ces éléments comme la
tokenisation (contenu recopié tel quel, profondeur `svg` et `math` tenue pour ne pas changer L-9).

**Reste hors code (L-13)** : en Markdown, un ouvreur écrit dans un extrait ou un bloc de code est affiché par le rendu ;
lu ici comme un vrai, il peut se clore dans une construction vraie plus loin. Aucune page `md` du corpus ne porte
d'ouvreur.

### 4.3 Mesures sur le corpus réel

- Outil : ma réécriture de l'état k (`outils/sg5_masque.py`) contre une référence écrite d'après les états lus
  (`outils/reference_html.py`, tokeniseur réduit, construction de l'arbre limitée aux bascules de tokenisation) ;
  `outils/mesure_ecarts.py` et `detail_ecarts.py`, comptes seulement. Corpus de la tête `6117ea1` : 81 pages html
  (19 645 108 octets) et 7 pages md (hors `INDEX.md`, que la gate ajoute sans le débaliser).
- **Gardé en trop : 0 octet.**
- **Ôté en trop : 1 330 octets hors blancs**, en 5 régions d'une seule page (`intel-tdx-overview-2026-10-04.html`),
  toutes dans des `textarea` : 1 008 octets de balises écrites dans le texte (ôtées au débalisage) et 322 octets d'un
  `<script` écrit dans un `textarea` (ôtés comme un script). C'est le sens sûr ; C-6 rend au corpus le texte de ce `<script` (305 octets hors blancs, ses balises ôtées).
- Constructions vues par la première passe, hors commentaires (1 967) et scripts ou styles (1 291) : 80 DOCTYPE, aucun
  `<!` d'une autre forme, aucun `<?`, aucun `</` suivi d'une non-lettre (`outils/compte_factices.py`).
- Éléments de texte : 109 `title`, 6 `textarea` (1 avec un `<script` écrit dedans), 10 `iframe` (aucun ouvreur),
  23 `noscript`, 60 `template` (7 avec un ouvreur, lus comme du balisage par les deux lectures : juste).
- **Équivalence de ma réécriture et du Rust** : 88 pages sur 88 égales à l'octet entre ma réécriture Python et la sortie Rust de l'état final (test d'unité ajouté dans une copie à part, `copie-instr`, hors série) : mes masques valent pour le code réel. C-6 ne change qu'une page du corpus (`intel-tdx-overview-2026-10-04.html`) et n'y fait qu'insérer du texte : la sortie de la série est une sous-suite de la sortie corrigée (57 044 → 57 351 octets ; 5 603 → 5 908 hors blancs).

### 4.4 Corpus complet de la session (régime complet)

Copie de la tête `6117ea1` plus les 260 entrées de `/home/user/shogen/biblio/` (INDEX égal à celui de la tête,
204 artefacts déclarés), lue par la gate seule ; sortie filtrée à la source (`outils/xtask_filtre.awk` : en-têtes,
VERDICT, comptes de S-G5 ; jamais une citation).

| état | S-G5 | fragments contrôlés | écartés sous seuil | artefacts |
|---|---|---|---|---|
| tête, sans la série | VERT | 353 | 11 927 | 204 sur 204 |
| tête plus série a à k | VERT | 353 | 11 927 | 204 sur 204 |

S-G1 à S-G8 VERT dans les deux états ; S-G9 rouge par la seule borne `docs/17-modele-de-menace.md:70` (copie creuse).
Copie supprimée après usage.

### 4.5 Entrée du registre bibliographique (C-1)

Rangée exacte, section datée et mise à jour de la ligne du compte : `corrections/C-1-INDEX-rangee.txt`. Forme de la
section DETTES-T16 (sept colonnes) et de la l.279 (page mutable, ancre = couple date de copie et sha256). Citations :
quatre, de 6 à 15 mots, contrôlées par script sur le texte de la page. Redistribuable : « non » (aucune licence lue,
règle de la note datée du 2026-10-10).

## 5. Point 3 — registre des renvois et S-G9 (`xtask/src/sg9.rs`, lu en entier, 735 lignes)

### 5.1 Q-7 : table BASES, trois exceptions LECTURES, échantillon de 29 renvois

Pour chaque entrée, j'ai calculé l'empreinte de la plage écrite au commit retenu et au commit d'écriture
(DETTES-T14 ; docs/17 : `e970c38`) (`outils/q7_candidats.py`) : 133 sur 133 égalent l'empreinte du registre au commit
retenu ; 21 ont un texte différent entre les deux candidats. Ce sont celles où le choix compte, et toutes sont dans mon
échantillon (directement, ou par un jeton et une cible identiques). Contexte du jeton et texte aux deux commits lus pour
29 renvois (`outils/q7_lire.py`) :

- **Justes** (contexte et base déclarée concordent) : G1-B-SEG-2 l.244 (`b72509b`, base l.13) ; G1-DOCS-S2 l.31
  (ligne FISHER de la base `fb089dc`) et l.67 (« trois formes ») ; G1-POOLEE l.108 (`40b4cfb`, DOCS-S2-b) ; G1-SIM-NIVEAU
  l.5 (`f5b8269`) ; G2-DETTES-B2 l.301 (§4.11 exact à `3cc0892`) ; CP1-PAQUET l.36 (`8b9536b`, tête déclarée l.7) et
  l.136 ; G0-lot-D8a l.25, l.35, l.59, l.62, l.372, l.413 (`fb089dc`, base l.7) ; les trois exceptions : G2-partie-2
  l.443 (ADR-0028 à `37ea234` : sha256 cité égal, 327 lignes, plage 1-328 lue entière) et l.444 (annexe A à `6eabaa4` :
  sha256 cité égal, 113 lignes), G1-E1 l.13 (`aa0afdc` : rangée E1 « 150-250 lignes ») ; les cinq entrées déplacées de
  docs/17 (`squelette.yml:135` et `:55`, `test_exclusion.py:242-244` et `:269-271`, `records.py:17-21`, lues à
  `cf696bd`, contexte concordant) ; PAQUET l.16 (§6 exact à `8b14567`) ; G1-partie-3-R l.46 et l.138.
- **Serré** : G1-DETTES-B2-corrections l.157 (« ADR-0028 §4.11 l.287-301 », « à la tête ») : à `99d2aa4`, tête que le
  document déclare (l.100), la plage déborde d'une ligne sur le titre du §4.12 ; à `7bfff83`, elle couvre exactement le
  §4.11 avec l'amendement que ce même travail écrivait. Le choix suit la déclaration ; entrée épinglée, sans effet sur
  la gate.
- **Faux (C-4)** : un même renvoi, avec la même phrase, désigne deux passages dans le registre.
  - ADR-0028 l.35, `doc 10 l.379-380` (« le point à 99 % de la normale standard ») : lu à `ce63fed`, lignes 395-396 ;
    PAQUET l.56, même phrase recopiée : lu à `8b14567`, où l.379-380 portent la page du PDF de Knight et Leveson ;
    registre : 381-382. Le paquet donne lui-même son repère l.57 : à `8b14567`, la citation est en l.392-395.
  - ADR-0028 l.44, `doc 10 l.519-522` (structure à deux étages) : 535-538 ; PAQUET l.63 (« Texte (ADR l.44-49),
    recopié pour l'essentiel ») : lu à `8b14567`, où l.519-522 portent les formules de Θ̂ ; registre : 521-524.
  - ADR-0028 l.46, `doc 10 l.521-522` : 537-538 ; CP1-PAQUET l.101 cite entre guillemets la parenthèse de l'ADR : lu
    à `8b9536b` ; registre : 523-524.
  - Cause : `4d49757` (2026-09-30) insère quatorze lignes dans doc 10 avant l.379 ; ADR-0028 (`ce63fed`, 2026-09-29) est
    juste à sa date ; le paquet (`8b9536b`, 2026-10-02) recopie ses numéros.
  - Effet : le passage voulu reste gardé par les entrées d'ADR-0028, mais le registre dit faux pour ces trois renvois.
    La phrase « le paquet se lit à `8b14567` … son texte est retrouvé deux lignes plus bas » est fausse pour deux
    entrées sur trois.
- **Manquant** : PAQUET l.57, `l.392-395` (repère à `8b14567`, deux lignes plus bas aujourd'hui), hors du relevé
  heuristique de DETTES-T14 (L-2).

### 5.2 Troisième voix

`outils/troisieme_voix.sh` (bash, `git show`, `sed`, `sha256sum`, `cmp` : ni `registre_renvois.py` ni
`verifier_registre.py`) : pour chaque entrée, jeton dans sa ligne citante, empreinte de la plage écrite au commit de
lecture (la commande de rejeu du registre elle-même), empreinte aux lignes actuelles, et absence du bloc épinglé dans la
cible actuelle. Résultat sur la série, à `9b83a00` puis à `d66e8b6` : **133 entrées, 77 de docs/17, 56 autres,
110 à lignes actuelles, 23 épinglées, 0 écart**, aucune plage sur une dernière ligne sans saut de ligne. L'outil voit
les trois fautes semées (empreinte, épinglage d'un texte présent, jeton). `outils/comptes_registre.py` (analyse à moi
des spans de docs/17) : 77 références à couvrir, 20 MONARK, 7 bornes (6 sidecars, `docs/rapports/…:21`), 0 sans
entrée, 0 orpheline ; 62 exactes, 5 déplacées, 10 épinglées ; les 84 numéros de DETTES-T14 couverts par les
56 entrées, sauf l'exclusion `doc 06 l.269` ; paquet : 3 entrées, toutes à `8b14567`.

### 5.3 Sûreté (jugée sur le code)

- `controle_a` lit un fichier sous un emplacement interdit pour en compter les lignes : la plage seule est contrôlée,
  rien n'est imprimé ni haché ; la référence va en bornes (`sans_empreinte`). Conforme à Q-6.
- **`controle_renvois` n'avait aucune garde** : une entrée dont le document citant ou la cible est sous un emplacement
  interdit faisait lire la ligne citante (contrôle du jeton) et hacher les lignes citées. Un test le montre : deux
  entrées justes de cette forme passent sur le code de la série. **C-3** les refuse avant toute lecture.
- Hors lot, contexte : le contrôle (e) de S-G9 (`corpus_francais`, DETTES-B2) parcourt `docs/**/*.md`, emplacements
  interdits compris, pour y chercher une citation française de docs/17 ; il n'imprime ni ne hache rien.

### 5.4 Forme du fichier

Les commandes de rejeu en tête marchent : ma troisième voix les applique telles quelles aux 133 entrées. Elles ne disent
pas que `<a>,<b>` est la plage `ecrit` ni comment rejouer aux lignes actuelles (C-9). Commentaires : toute ligne qui
commence par `#`, partout ; en-tête exigé tel quel en première ligne non commentée ; refus nommés : forme, doublon,
jeton, cible, texte, sceau, orpheline, sans entrée, et, avec C-3, emplacement interdit. Une fin de ligne CRLF ou une
ligne d'espaces donnent un refus de forme (échec fermé).

### 5.5 docs/17 (DT15-e)

L'ajout est daté, placé en dernière ligne (l.115), sans décalage. Vrai : comptes 77, 62, 5, 10 ; les deux références
dites périmées sont épinglées ; bornes. **Inexact** : la phrase n'excepte pas les 20 références MONARK ; « son propre
commit pour chaque ajout daté » est faux pour les deux références de l'ajout du 2026-10-04 qui reprennent les cellules
d'E1 (`gates.yml:35`, `:54-92`, lues à `cf696bd`) ; l'empreinte est de 16 chiffres. Forme corrigée : C-7, en place
dans la ligne de l'ajout (docs/17 n'est la cible d'aucun renvoi).

## 6. Point 4 — FLOTTANT (DT15-f)

- `flottant_equivalence.py` rejoué sous **3.10.20, 3.11.15, 3.12.3, 3.13.14** : même partition en 8 classes, 19 173 961,
  271 453 et 200 000 chaînes, **AUCUN ÉCART** sous chacune. **L-7 se ferme.**
- Mon contrôle (`outils/flottant_g2.py`, sous les quatre versions) : M07 (`[A-Z0-9_.-]` contre `[A-Za-z0-9_.-]` sous
  IGNORECASE) diffère sur 0 des 1 114 112 points de code : équivalent ; différentiel `findall` ancien contre nouveau sur
  300 000 chaînes d'un générateur à moi (casse, ſ, K, İ, ı, `-latest` coupé) : 0 écart.
- Raisonnement relu, juste : une occurrence de l'ancien motif tient dans une suite maximale de caractères de libellé,
  en part du début et finit à sa fin ; une position intérieure ne réussit que si le début réussit, et le balayage a
  alors sauté la suite ; le regard arrière fait échouer ces positions en un pas.
- Test de temps : sur le nouveau motif, chaque appel prend 0,045 à 0,051 s (dont 0,013 s de démarrage) contre une
  borne de 20 s, soit une marge d'environ 400 par appel. Un faux rouge en CI est hors de portée. L'inverse (rouge sur
  l'ancien motif) dépend de la machine (L-8, inchangée).

## 7. Point 5 — tests et mutants

**Rouges** (`outils/rouges.sh`, états reconstruits par application des diffs un à un ; commande du job) :

| diff | tests neufs | rouges sur le code d'avant | verts (témoins visés par un mutant) |
|---|---|---|---|
| DT15-a | 6 | 4 | 2 |
| DT15-c et d | 19 | 18 (17 mutants et le témoin des épinglées, couverture `(5, 5)`), plus 2 témoins anciens dont l'attendu change | 1 |
| DT15-g | 15 | 5 | 10 (dont les 2 du double échappement, verts sur f) |
| DT15-h | 6 | 5 | 1 |
| DT15-j | 12 | 7 | 5 |
| DT15-k | 14 | 11 (6 « devait être ROUGE », 4 « texte affiché perdu », 1 « plus de 10 s ») | 3 |
| corrections C-3 à C-6 | 14 | 9 sur le code de la série | 5 |

Tous les rouges sont des rouges d'assertion. Le test de FLOTTANT est rouge sur l'ancien motif (mutant P01).

**Mes mutants** (`outils/mutants_g2.py`, puis `mutants_g2_corr.py` sur la copie corrigée ; juges : `cargo test -p xtask`
pour le Rust ; S-G9 dans `cargo xtask gates`, violations comparées à la référence, pour les données ; ligne exacte du
job `controle-unittest` lue dans le `gates.yml` muté pour le Python ; contrat SHOGEN-MUT-FATAL-1, 0 FATAL ; témoins
vivants avant chaque campagne) :

- Campagne 1, sur la série, 41 mutants : `sg5.rs` 17 (commentaires S01 à S03 ; script et style S04 à S09, S18 ;
  factices S10 à S12 ; balises S13 à S16), `sg9.rs` 9 (G01 à G09), données du registre 9 (D01 à D09),
  `runners-epingles.py` et plancher 6 (P01 à P06). **36 tués**. Vivants : S11 (équivalent : `</>` ôté en première
  passe ou au débalisage, même sortie), D08 (commit d'une entrée épinglée : L-1), et trois trous de test : S04 (fermante
  dans l'état échappé), S07 (`style` lu avec les états du script), G04 (empreinte comparée sur 8 chiffres).
- C-5 ajoute trois tests (deux témoins, et une paire « ligne 1012 » et « ligne 16091 », dont les SHA-256 partagent 8
  chiffres, trouvée par recherche des anniversaires).
- Campagne 2, sur la copie corrigée, 18 mutants : S04, S07, G04 rejoués, **tués** ; C-6 K01 à K09 et C-3 et C-4 K10 à
  K13 tués ; données K14 tué, K15 vivant (commit d'une entrée à lignes actuelles : seule la forme est lue, L-1).
- Planchers exacts : `controle-unittest` 37 à l'état e (`Ran 37`, conforme) et 38 aux états f à k et sur la copie
  finale (`Ran 38`, conforme sous 3.10 à 3.13). P05 (plancher 37 sur l'état final) est refusé par `--egal`.

## 8. Point 6 — gates de la copie finale (`d66e8b6` plus la série)

Sous `isole.sh`, sans mandataire ni `SHOGEN_S2_CAMPAGNE_CONTROL` (`outils/gates_finale.sh`, `journaux/gates-finale.out`) :

- **Matrice 3.10 à 3.13, `-X dev -W error`** : `scripts/controle` `Ran 38`, OK, 0 avertissement ; ligne du job conforme ;
  `enforcement` : runner 137 ok, runner des workflows 16 ok, `runners-epingles` conforme (7 workflows, 22 clés),
  `docs-sha256sums` conforme (45 sommes, 338 lignes), `journaux-modele` conforme (52), `workflows-yaml` conforme
  (PyYAML 6.0.1) ; rc 0 et 0 avertissement partout.
- **Étapes `run:`** (interpréteur 3.12) : g5 cas du hook 57 ok, 0 échec ; R-13 sur un dépôt jetable des fichiers du lot :
  0 ligne ; g1 runners-epingles, workflows YAML (python3-yaml 6.0.1-2build2 du paquet), lint 227 ok et arbre OK,
  journaux et sommes : conformes ; g3 runner 147 ok, gate des secrets indexée et `--tree` sur le dépôt jetable : OK
  (`--history` non joué) ; runner des jobs unittest 137 ok ; s2-harness `Ran 419` conforme ; s2bis `Ran 374` conforme ;
  calib-actifs `Ran 78` conforme ; controle `Ran 38` conforme ; **sim-bis refusé (`Ran 257`, 3 erreurs)** : son oracle
  extrait du code par `git archive <commit>` et ma copie creuse n'est pas un dépôt git (`Refus("ORACLE/extraction")`).
  Sur la tête sans la série : mêmes trois erreurs, `Ran 257` : sans lien avec la série, qui ne touche pas `scripts/sim-bis/` (limite d'environnement de ma copie).
- **`cargo --locked xtask verify`** (lignes VERDICT) : S-G1 à S-G8 VERT ; S-G9 ROUGE par `docs/17-modele-de-menace.md:70`
  seule ; `cargo fmt --check`, `no_std`, `cargo clippy -D warnings` VERT.
- **`cargo test -p xtask`** à la cible par défaut de la copie (I-1) : `mutants` 153, `arbres` 3, `distillation` 7,
  `reproductible` 9, tous passés (de même sur ma première copie de série).
- **Corrections C-2 à C-9 sur la copie finale** : copie `d66e8b6` plus la série plus C-2 à C-9 : application dans l'ordre, `fmt` sans demande, `cargo test -p xtask` (`mutants` 167 passés, le reste vert), `xtask verify` : S-G1 à S-G8 VERT, S-G9 par `docs/17-modele-de-menace.md:70` seule (le registre corrigé passe), `cargo fmt --check`, `no_std` et `cargo clippy -D warnings` VERT. Corpus complet (`6117ea1`, série et corrections, octets de `biblio/`) : S-G5 VERT, 353 fragments contrôlés, 11 927 écartés, 204 artefacts sur 204 ; S-G9 par la même borne seule.

## 9. Point 7 — limites et écarts du générateur

| limite | jugement |
|---|---|
| L-1 | juste, à préciser : la gate ne relie jamais une empreinte à son commit de lecture (pas d'historique en CI) ; le champ `commit` n'est lu qu'en forme, hors du paquet (mutants D08 et K15 vivants). Déclencheur : toute mise à jour du registre ; la G2 du lot rejoue une troisième voix avec `git show`. |
| L-2 | juste ; illustrée par PAQUET l.57, hors du relevé heuristique (ajouté par C-4). Déclencheur : un lot qui écrit un renvoi par numéro de ligne dans un autre document que docs/17 porte son entrée au registre. |
| L-3 | juste, à préciser : un renvoi recopié d'un autre document se lit au commit de lecture de sa source (C-4). |
| L-4, L-5 | justes ; L-5 est désormais tenue aussi par le registre (C-3). |
| L-6 | fermée par DT15-h (rejoué : 5 rouges, mutants S10 et S12 tués, aucun factice au corpus hors DOCTYPE). |
| L-7 | **fermée** par mon rejeu sous 3.10 à 3.13. |
| L-8 | juste (marge mesurée §6). Déclencheur : un hôte de CI plus de neuf fois plus rapide, sur lequel l'ancien motif tiendrait la borne. |
| L-9 | juste ; C-6 tient la profondeur `svg` et `math` pour ne pas l'étendre. Points d'intégration non lus. Déclencheur : une page du corpus avec un `</script`, `</style`, CDATA ou commentaire dans un contenu SVG ou MathML. |
| L-10 | **fermée** par cette relecture : règles [lu] ; une contradiction (`<?`, C-2) et un manque (texte brut, C-6). |
| L-11, L-12 | justes (sens sûr ; aucun `xml` au corpus). |
| L-13 (neuve) | ouvreur écrit dans un extrait ou un bloc de code Markdown, affiché par le rendu, lu comme un vrai : il peut se clore dans une construction vraie (faux vert). Hors d'atteinte sans lecture du Markdown. Déclencheur : une page `md` versée au corpus avec `<!--`, `<!`, `<?`, `</` suivi d'une non-lettre, `<script` ou `<style` dans un code ; aujourd'hui aucune. |

Observation hors liste : le contenu d'un `iframe`, `noembed` ou `noframes` reste au corpus. La page lue en fait du
RAWTEXT, mais ce qu'il affiche relève du rendu, non lu ici [abs]. C'est un choix de portée (Q-5 visait `script` et
`style`), cohérent avec `noscript`.

Écarts du générateur : E-10 (campagne sur un texte différent de quatre lignes de doc) est levé, mes campagnes ayant
tourné sur le texte exact ; E-13 et E-18 sont vérifiés (11 rouges sur j, dont le test de temps) ; les autres
n'appellent pas de remarque.

## 10. DT15-i (`presg5.py`)

- Le `presg5.py` du scratchpad est encore la version d'avant. DT15-i passe `git apply --check` depuis la racine du
  scratchpad ; appliqué à une copie de l'ancienne version, il redonne `presg5/apres` à l'octet.
- Équivalence relue : l'ancienne condition `0 ≤ j ≤ 300` sur `apres[1:]` vaut `t.find(">", k + 1, k + 302)`, et le saut
  tombe au même indice ; de même pour les crochets (fenêtre de 30). Coût linéaire : chaque `<` coûte au plus une
  fenêtre de 301 caractères.
- Mon différentiel (`outils/presg5_diff.py`) : 400 024 cas (aléatoires et bords de fenêtre), 0 écart.
- **À la tête `f3a43b9`**, GF-2 (lot GARDE-FOUS) a versé `scripts/controle/presg5.py`, égal à l'octet à l'ancienne
  version (sha256 `60de40770b2889b7`), avec un test à sortie dorée (`tests/test_presg5.py`, 1 test). DT15-i s'y
  applique en changeant de chemin ; ce test reste vert sur la version corrigée (rejoué).
- **À la tête `3ad8d9d`**, GF-2b en a fait un outil (fonction `introuvables`, sorties 0, 1 et 3, chemins interdits
  jamais ouverts), sans toucher à `retirer_balises` ni à `scinder_crochets`. Rejoué sur une copie de `scripts/controle`
  (`outils/port_presg5.sh`, `outils/presg5_port.py`, `journaux/port-presg5.out`) :
  - les deux hunks de DT15-i s'appliquent en changeant de chemin, décalés de 25 lignes ;
  - les 5 tests du dépôt restent verts sur la version portée, sous Python 3.10 à 3.13 en `-X dev -W error`, sortie
    dorée (sha256 épinglé) comprise ;
  - valeurs de référence de DT15-i : 12 sur 12 sur les deux versions ; 32 000 entrées aléatoires (chevrons, crochets,
    bornes 300 et 30), deux fonctions : 0 écart entre l'outil et sa version portée ;
  - sur 8 000 000 de caractères, plus de 20 s pour chacune des deux fonctions de l'outil du dépôt ; 0,222 s et 0,258 s
    une fois porté ;
  - le test de DT15-i ne se porte pas tel quel : son chargeur exécute `GC = _module("garde_commun")`, qui lit
    `__file__`, absent de l'espace où il exécute l'arbre (`NameError` 3 fois ; `Ran 3`, 2 échecs, 1 erreur). L'outil
    étant importable, un port le charge par `importlib`, comme `outils/presg5_port.py` ;
  - rejoué à `0e30330` (GF-3 et GF-4b changent `garde_commun.py`), par `outils/port_presg5_tete.sh` : mêmes
    résultats, 0,215 s et 0,199 s une fois porté (`journaux/port-presg5-0e30330.out`).

  **Item à former** (règle PAROXYSME) : porter DT15-i dans `scripts/controle/presg5.py`, avec des tests de temps
  adaptés au chargeur et le plancher de `controle-unittest` relevé d'autant (61 plus les tests neufs à `4543667`, si
  C-10 est versé avant). Sans cela, le dépôt garde la lecture quadratique, et la phrase de fermeture ne peut pas dire « hors dépôt »
  (C-8).
- Tests : 3 verts en 0,8 s sur la nouvelle version ; sur l'ancienne, les deux tests de temps sont rouges (`plus de 20 s pour 8000000 caractères`), le test des valeurs de référence vert : `Ran 3`, `FAILED (failures=2)`.

## 11. Corrections (liste fermée), à appliquer dans l'ordre après DT15-k

| C-n | fichier (sha256, 16 premiers chiffres) | lignes ajoutées | objet |
|---|---|---|---|
| C-1 | `corrections/C-1-INDEX-rangee.txt` | — | section et rangée de `biblio/INDEX.md` pour la pièce WHATWG, ligne du compte 204 → 205, octets à verser |
| C-2 | `corrections/C-2.diff` (`cad8523e953c9faf`) | 14 | doc de `sg5.rs` et de `mutants.rs` : `<?` est une instruction de traitement |
| C-3 | `corrections/C-3.diff` (`0fad185299ba56e0`) | 37 | `sg9.rs` : refus avant lecture d'une entrée qui nomme un emplacement interdit ; un test |
| C-4 | `corrections/C-4.diff` (`096891244d325db5`) | 62 | registre : PAQUET l.56 et l.63, CP1 l.101 lus à `ce63fed`, aux lignes 395-396, 535-538 et 537-538 ; entrée PAQUET l.57 ; commentaire ; `SCELLES` (alias de type `Scelle`) admet les lignes 56 et 63 du paquet à `ce63fed` ; un test. **Amende Q-2.** |
| C-5 | `corrections/C-5.diff` (`f60fa2fcbd1c04a1`) | 20 | trois tests (mutants S04, S07, G04) |
| C-6 | `corrections/C-6.diff` (`d9ce811c3719dcce`) | 88 | `sg5.rs` : `TEXTE_BRUT`, `texte_brut`, profondeur `svg` et `math` ; doc ; neuf tests |
| C-7 | `corrections/C-7.diff` (`3dce2adaf5effbe9`) | 1 | docs/17, ligne de DT15-e : MONARK, commit des références reprises, 16 chiffres |
| C-8 | `corrections/C-8-phrases.txt` | — | phrases de fermeture corrigées pour le bloc daté de l'annexe B |
| C-9 | `corrections/C-9.diff` (`04b24e724aaf1c39`) | 2 | registre : commande de rejeu précisée |
| C-10 | `corrections/C-10.diff` (`1feda8e328b3a6e1`) | 29 | DT15-f recalé sur `4543667` : même code, même test ; plancher de `controle-unittest` 60 → 61 ; ajout daté du README placé en fin, après celui de GF-5, chiffres recalés. Remplace DT15-f à `4543667`. Si la tête avance encore, `outils/c10_generique.py <commit court> <copie>` le refait (plancher P lu dans `gates.yml`, écrit P + 1 ; refus si le dernier ajout du README est daté après le sien). Les versions pour `f3a43b9` (`0362f497cc824d67`), `3ad8d9d` (`b7415985e911edd9`) et `0e30330` (`3e8cd17ce016d978`) restent au dossier, hors liste. |

Éprouvées sur la série (copie de série plus C-2 à C-9, cibles cargo neuves) : application par `git apply` dans l'ordre ;
`cargo fmt --check` sans demande ; `cargo test -p xtask` : `mutants` 167 passés ; sur le code de la série, les 9 tests
attendus sont rouges d'assertion ; campagne 2 au §7 ; S-G9 sur le registre corrigé : seule la borne `docs/17:70`.
Les diffs C-2 à C-9 sont produits par `outils/corrections_g2.py`, qui repart de la copie de série ; C-10 par
`outils/c10_generique.py`, sur une extraction de la tête. C-10 est éprouvé à `3ad8d9d`, `0e30330` puis `4543667` avec
toute la série et C-2 à C-9 (§12).

## 12. Écarts du réviseur

- **E-1** : un `du -sh` lancé sur ma copie creuse (une taille totale, aucun nom) ; la règle l'interdit même dans une
  copie creuse. Non relancé.
- **E-2** : `q7_lire.py` a affiché, pour docs/17 l.106, une ligne de docstring de `s2-harness/tests/test_exclusion.py` à
  `e970c38` qui porte un compte. Fichier permis (suite du dépôt) ; exposition déclarée pour le contrôle FM-1.1, comme
  l'E-1 du générateur ; rien n'en est recopié ici.
- **E-3** : `outils/faire_diff.sh` a lancé une fois `find . -type f` dans ma copie de correction (cinq fichiers que j'y
  avais copiés) ; remplacé par une liste explicite, puis par `corrections_g2.py`.
- **E-4** : ma seconde campagne a d'abord partagé une cible cargo entre copies du même workspace ; une copie aux dates
  anciennes a été jugée fraîche et a réutilisé le binaire de la copie précédente (témoin en échec, référence fausse).
  Campagne refaite sur cible neuve ; la première campagne et les tests de la copie corrigée n'en sont pas touchés
  (cible neuve, ou fichiers patchés plus récents que le dernier build) ; journal invalide gardé sous un nom qui le dit.
- **E-5** : une comparaison `difflib` (quadratique) a tourné environ une minute en même temps que la fin de la revérification des corrections ; je l'ai arrêtée (le seul processus que j'avais lancé ainsi) et remplacée par un contrôle linéaire de sous-suite.
- Une première version de C-4 faisait rougir `cargo clippy -D warnings` (`type_complexity` sur `SCELLES`), vu par `xtask verify` sur la copie finale corrigée : alias de type ajouté, diffs recoupés, toute la vérification des corrections refaite sur cibles neuves. Seule la version corrigée est livrée.
- **E-6** : pour la gate des secrets et R-13, qui exigent un arbre git, `outils/gates_finale.sh` a fait à `d66e8b6` un
  `git init` et un `git add` dans un dossier jetable de mon dossier (copie des fichiers du lot), jamais dans le dépôt.
  La consigne « aucune opération git en écriture » peut s'entendre de tout dépôt : déclaré. À `3ad8d9d`, R-13 est
  rejoué par `grep` sur la liste explicite des fichiers du lot, sans dépôt jetable ; la gate des secrets n'y est pas
  rejouée (C-10 n'ajoute que des commentaires, de la prose et un test).
- Hook GARDE-FAITS (R5) : refus d'une première écriture de ce rapport, pour un préfixe d'empreinte jamais affiché seul ;
  chaque identifiant de ce rapport a été relu à sa source avant l'écriture.
- Charge : un seul processus lourd à la fois ; charge sur 1 min au plus 4,01 (13:49:55 UTC, pendant ma campagne).
- **Dernière relecture de la tête** : 2026-10-15 14:32:07 UTC, `f3a43b9` (GF-1, GF-4, GF-2 du lot GARDE-FOUS). Parmi
  les chemins de la série et les cibles du registre, seuls `gates.yml` (plancher de `controle-unittest` 37 → 49) et
  `scripts/controle/README.md` (trois ajouts datés) changent. DT15-a à e et g à k s'y appliquent ; **DT15-f ne s'y
  applique plus** (`patch failed` sur ces deux fichiers). C-10 le recale : la série avec C-10 à la place de DT15-f,
  puis C-2 à C-9, s'applique sur une extraction neuve de `f3a43b9` ; `controle-unittest` `Ran 50`, conforme au
  plancher 50 ; runner 137 ok ; `runners-epingles`, `workflows-yaml`, sommes et journaux conformes ; troisième voix
  sur le registre corrigé : 134 entrées, 111 à lignes actuelles, 23 épinglées, 0 écart.
- **Relecture de la tête après le rapport** : 2026-10-15 14:41:39 UTC, `3ad8d9d` (GF-2b du lot GARDE-FOUS). Parmi les
  chemins de la série, seuls `gates.yml` (plancher de `controle-unittest` 49 → 53) et `scripts/controle/README.md` (un
  ajout daté) changent, avec `presg5.py` et son test hors de la série. DT15-f et la version de C-10 pour `f3a43b9` ne
  s'y appliquent plus (`patch failed` sur ces deux fichiers). C-10 refait (`outils/c10_tete.py`) : la série avec C-10 à
  la place de DT15-f, puis C-2 à C-9, s'applique sur une extraction neuve de `3ad8d9d` (1420 membres)
  (`outils/tete_3ad8d9d.sh`, `journaux/tete-3ad8d9d.out`) :
  - `controle-unittest` : `Ran 54`, conforme au plancher 54, sous Python 3.10, 3.11, 3.12 et 3.13 en `-X dev -W
    error`, 0 avertissement ; runner des jobs 137 ok ; `workflows-yaml` 16 ok et conforme ; `runners-epingles`,
    `docs-sha256sums`, `journaux-modele` conformes à chaque version ;
  - étapes de g1 et g5 : hooks 57 ok ; lint 227 ok et `OK (R-1)` ; R-13 : 0 ligne ;
  - troisième voix : 134 entrées (77 de docs/17, 57 autres), 111 à lignes actuelles, 23 épinglées, 0 écart ;
  - cible cargo neuve : `cargo test -p xtask` 3, 7, 167 et 9 passés ; `xtask verify` : S-G5 372 fragments contrôlés,
    12 309 écartés (corpus incomplet de la copie creuse, comme avant), S-G9 la seule borne `docs/17:70`, fmt, no_std et
    clippy VERT.

  La série s'appliquait donc à `3ad8d9d` avec C-10 à la place de DT15-f.
- **Tête suivante** : 2026-10-15 14:54:35 UTC, `0e30330` (GF-3 `61b1c3b`, GF-4b `0e30330`). Parmi les chemins de la
  série, seuls `gates.yml` (plancher 53 → 57) et `scripts/controle/README.md` (deux ajouts datés) changent ; les
  versions de C-10 pour `f3a43b9` et `3ad8d9d` ne s'appliquent plus. C-10 refait par `outils/c10_generique.py`, puis
  `outils/tete_serie.sh` sur une extraction neuve de `0e30330` (1421 membres ; `journaux/tete-0e30330.out`) :
  application de toute la série avec C-10, puis de C-2 à C-9 ; `controle-unittest` `Ran 58`, conforme au plancher 58,
  sous 3.10 à 3.13 en `-X dev -W error`, 0 avertissement ; runner 137 ok ; `workflows-yaml` 16 ok et conforme ;
  `runners-epingles`, `docs-sha256sums`, `journaux-modele` conformes ; hooks 57 ok ; lint 227 ok et `OK (R-1)` ;
  R-13 : 0 ligne ; troisième voix : 134 entrées, 111 à lignes actuelles, 23 épinglées, 0 écart ; cible neuve :
  `cargo test -p xtask` 3, 7, 167 et 9 passés ; `xtask verify` : S-G5 372 et 12 309 (corpus incomplet), S-G9 la seule
  borne `docs/17:70`, fmt, no_std et clippy VERT. Tête relue à 14:59:51 : toujours `0e30330`.

  La série s'appliquait donc à `0e30330` avec C-10 à la place de DT15-f.
- **Dernière tête vue** : 2026-10-15 15:01:03 UTC, `4543667` (GF-5). Mêmes chemins de la série changés (plancher
  57 → 60, un ajout daté du README). `outils/tete_serie.sh` (`journaux/tete-4543667.out`, 1423 membres) : application
  de toute la série avec C-10, puis de C-2 à C-9 ; `controle-unittest` `Ran 61`, conforme au plancher 61, sous 3.10 à
  3.13 en `-X dev -W error`, 0 avertissement ; runner 137 ok ; `workflows-yaml`, `runners-epingles`,
  `docs-sha256sums`, `journaux-modele` conformes ; hooks 57 ok ; lint 227 ok et `OK (R-1)` ; R-13 : 0 ligne ;
  troisième voix : 134 entrées, 0 écart ; `cargo test -p xtask` 3, 7, 167 et 9 passés ; `xtask verify` comme à
  `0e30330`. `presg5.py` et `garde_commun.py` n'y changent pas : le rejeu du port à `0e30330` vaut. Tête relue à
  15:03:39 : toujours `4543667`.

  **La série s'applique à `4543667` avec C-10 à la place de DT15-f** ; DT15-f seul ne s'y applique pas. Le lot
  GARDE-FOUS verse encore : à chaque avance qui ne touche que le plancher de `controle-unittest` et la fin du README,
  `outils/c10_generique.py` refait C-10 et `outils/tete_serie.sh` l'éprouve (deux minutes).

## 13. Journal de provenance (G1)

**Sources** :
- [lu] `BRIEF-G2.md` (mis à jour), `ADJUDICATION.md` (trois ajouts datés), `RAPPORT-GENERATEUR.md` en entier (phases 1
  à 3), `BRIEF-DETTES-T15.md`.
- [lu] les dix diffs et DT15-i, en entier ; `xtask/src/sg5.rs` et `sg9.rs` en entier à l'état final ; dans
  `mutants.rs`, les aides et tous les tests neufs ; `documents.rs` (`fichiers_markdown`, `fichiers_du_repertoire`,
  `compte_declare_en_tete`) ; `rapport.rs` (impression) ; `lib.rs` (`verify`, étapes cargo) ; `gates.yml` (toutes les
  étapes) ; `squelette.yml` l.108-124 ; `gate-secrets.sh` l.1-100 ; `verdict-suite-s2.py` (en-tête, contrat de sortie).
- [lu] `docs/RENVOIS-LIGNES.tsv` en entier ; `registre_renvois.py` et `verifier_registre.py` du générateur ; les deux
  TSV de DETTES-T14 ; les contextes de jeton et les textes cités de 29 renvois aux deux commits ; docs/17 l.112-115 ;
  le paquet l.5, l.8, l.56-57, l.61-63 ; annexe D, §D.2 ; `PASSATION-CLOUD.md` l.128-142 et l.268-276 ; `CP2-S2.md`
  l.30-40 ; `biblio/INDEX.md` l.1-30, l.264-283, l.388-452.
- [lu] la page WHATWG détenue : §13.2.5 en entier (états 13.2.5.1 à 13.2.5.76), §13.2.6 pour les balises ouvrantes
  nommées au §4.1.
- [lu] les octets du corpus, par la gate et par mes mesures seulement, aucun texte imprimé.
- [abs] la licence du standard HTML (absente de la page détenue) ; le rendu des éléments (section non détenue).
- [2nd] aucun chiffre repris sans recompte : chaque chiffre de ce rapport sort d'un journal de `g2/journaux/` ou d'une
  commande ci-dessous.

**Commandes et sorties** (`g2/journaux/`) : `cargo-test-serie-defaut.txt` ; `rouge-*.txt` et `.echecs` ;
`mutants-g2.out`, `mutants-g2-corrections.out` (et `…-INVALIDE-cache.out`, E-4), `mut-*.txt` ;
`flottant-equivalence-python3.1x.out` ; `q7-candidats.tsv` ; `corpus-avant.txt`, `corpus-apres.txt` ;
`mesure-ecarts.out` ; `gates-finale.out` et `gates-copie-finale/` ; `xtask-verify-finale.txt` ;
`cargo-test-corrections.txt`, `rouge-corrections-sur-serie.txt`, `reverif-corrections.out`,
`cargo-test-finale-c.txt`, `xtask-verify-finale-c.txt`, `corpus-apres-corrections.txt` ; `fin-de-passe.out`,
`simbis-tete.txt`, `presg5-ancien.txt`, `instr-*.txt` ; `tete-3ad8d9d.out` et `tete-3ad8d9d/` ; `port-presg5.out` ; `tete-0e30330.out` et `tete-0e30330/`, `port-presg5-0e30330.out` ; `tete-4543667.out` et `tete-4543667/`. Outils : `g2/outils/`.

## 14. Livrables

`RAPPORT-G2.md`, `NOTES.md`, `pieces/` (page WHATWG, métadonnées, texte extrait), `corrections/` (dont
`C-10-f3a43b9.diff`, `C-10-3ad8d9d.diff` et `C-10-0e30330.diff`, hors liste, pour mémoire), `outils/`,
`journaux/`, `SHA256SUMS` (tous les fichiers du dossier, hors copies et cibles, supprimées ou à supprimer).
