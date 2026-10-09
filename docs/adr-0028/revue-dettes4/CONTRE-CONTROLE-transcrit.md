# Contre-contrôle de DETTES-T4 (CONFORME en passe 2) (transcrit)

> Transcription par l'orchestrateur le 2026-10-09 21:12:10 UTC du fichier g2/cc/RAPPORT-CC.md ; contrôle FM-1.1 des transcripts du générateur-correcteur, du réviseur et du contre-contrôleur, par le fm11.py versé et par celui de DT3-E : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# CONTRE-CONTRÔLE — lot DETTES-T4 (SHOGEN-DOCS-SHA256SUMS-GATE-1, annexe B, bloc B.90, l.1546)

- **Modèle** : `claude-opus-5-5` (identifiant exact de l'environnement), effort max. Contre-contrôleur neuf : je n'ai
  écrit ni les diffs, ni la G2, ni l'adjudication. Gate 0 : préfixe `claude-opus-5-5`, conforme. Heures lues par
  `date -u` : début 2026-10-09 19:41:42 UTC, rapport écrit à partir de 19:55:15 UTC.
- Rattachement (G0) : ligne d'item lue sur la copie à `6356a94` (`docs/adr-0028/ANNEXE-B-items.md` l.1546 [lu]) : « une
  gate (xtask ou job) qui rejoue `sha256sum -c` de chaque `SHA256SUMS` de `docs/` hors des dossiers interdits, et ses
  tests ».
- Base : `git rev-parse HEAD` du dépôt réel (lecture seule) = `6356a945c4faf667b9b4a432cd6cb9b2200432a6`, égale à
  celle du brief. Aucun écart de base. Rien écrit hors de `$D/g2/cc/`, rien commis dans le dépôt, rien poussé.
- Série relue, dans cet ordre : `DT4-a` `2f5827c7…1dbb`, `DT4-b` `ed529fa4…9d90`, `DT4-c` `93688eef…35d8`, `DT4-d`
  `2efaadb7…17a1`. **Empreinte de la série** (sha256 de la concaténation a|b|c|d) :
  `5048855c7597156d432bf0535a0eeeb8adb16b998187697e7772012ccd95481d`, égale à celle du générateur. `git apply --check`
  puis `git apply` : OK sur `6356a94`. Script obtenu : sha256 `9b61ebc8…66d2` ; avant DT4-d (a+b+c, reconstruit par
  `git apply -R` de DT4-d) : `0c715e91…c5dc`, égal au chiffre de la G2.
- Enregistrement `oracle_record.py` : sans objet, comme l'adjudication l'a dit pour la G2 (lot hors du chemin S2).

## Verdict : **CONFORME-AVEC-RÉSERVES**

Liste fermée : **R-1, R-2, R-3**. Elles forment un diff proposé, `DT4-e-propose.diff` (sha256 `21190474…40fe`,
**+13 −9** : script +2 −1, tests +11 −8). Il s'applique après DT4-d (`git apply --check` OK sur la série). Je l'ai
éprouvé sur une copie jetable :
- rouge des tests de R-1 contre le script de la série (`sorties/R-rouge.txt` : `FAILED (failures=1)`,
  `AssertionError: Tuples differ: (1, False) != (0, True)`, 0 `ERROR`) ;
- vert avec le script corrigé (`sorties/R-vert.txt`, `Ran 8 tests`, OK) ;
- suite `controle` : Ran = 26, conforme à `--egal --plancher 26` (le plancher ne bouge pas) ;
- contrôle de l'arbre : conforme (33, 290, 11, 4) ;
- mutants : 14 tués sur 14 ;
- sondes : la seule fuite restante est H1 (lien physique, O-3).

- **R-1 (script et tests) : un dossier nommé `*.jsonl` n'est pas traité comme interdit.**
  - La sonde C6 le montre : `docs/b/z.jsonl/SHA256SUMS` est lu, et son contenu passe sur stderr (motif « ligne hors
    forme b'SECRET-…' »).
  - La sonde C5 le montre aussi : la ligne `z.jsonl/k.md` est ouverte et hachée, et `os.walk` liste le dossier.
  - Cause : `interdit()` teste `relatif.endswith(".jsonl")`. Le parcours appelle `interdit()` sur `…/z.jsonl/`, avec
    une barre finale, donc ce dossier n'est jamais élagué. Un chemin listé qui le traverse ne finit pas en `.jsonl`.
  - Le motif `!*.jsonl` des copies creuses de ce lot (générateur, G2, la mienne) exclut le dossier et tout son contenu.
    Je l'ai mesuré sur un dépôt synthétique : `b/z.jsonl/k.md` est absent de l'arbre extrait, `b/ok.md` présent.
  - Forme proposée, un serrage : `any(p.endswith(".jsonl") for p in relatif.split("/"))`. On ajoute `b/z.jsonl` aux
    dossiers jamais lus de `test_interdits`, et `z.jsonl/x.md` aux chemins refusés.
  - Effet à la tête : nul. Aucun chemin indexé ne contient `.jsonl/` (`git ls-files | grep -c '[.]jsonl/'` : 0), et le
    contrôle de l'arbre reste conforme.
- **R-2 (tests) : les bornes « hors du dossier » ne sont pas épinglées contre un voisin de préfixe.**
  - Deux mutants restent **vivants** sur la série : K1 (`reel.startswith(reel_dossier)` sans `os.sep`) et K2
    (`reel_somme.startswith(dossier)` sans `/`).
  - Raison : les deux cas de lien hors du dossier visent `docs/b/`, qui ne partage pas de préfixe avec `docs/a/`.
  - Forme proposée : `docs/b/` devient `docs/ab/` dans ces deux arbres (0 ligne ajoutée). K1 et K2 sont alors tués.
- **R-3 (tests) : `test_formes_refusees` n'exige que le refus, pas son motif.**
  - Deux mutants restent **vivants** sur la série : K3 (barre oblique inverse admise) et K4 (retour chariot admis). La
    ligne mutée finit en « absent », donc en sortie 1 quand même.
  - De plus, aucun cas ne porte de barre oblique inverse, alors que la docstring en promet le refus.
  - Forme proposée : exiger « hors forme » dans le motif, et ajouter le cas `x` + `chr(92)` + `y.md` (écrit par
    `chr(92)`, 0 octet 92 dans le diff). K3 et K4 sont alors tués. J'ai vérifié que les 11 cas existants produisent
    tous ce motif.

## Points du brief

1. **C-1 à C-4, README, Q-1, Q-3 : conformes.**
   - C-1 est posé dans `verifier`, avec la forme de la G2. Il est prouvé par les sondes A3, A4, A5, A8 et A9 : ce sont
     des fuites sur a+b+c, aucune sur la série (tableau des sondes ci-dessous).
   - C-2 : les trois cas sont présents. N3 et N8 sont tués.
   - C-3 : docstring et README nomment les deux `PAQUET.sha256`.
     - Je l'ai recompté : `sha256sum -c --status` depuis la racine sort en 0 pour le courant et en 1 pour
       `premier-2026-10-02/`.
     - Chacun tient en une ligne qui nomme `*docs/adr-0028/PAQUET-PREREG-S2.md`, fichier hors de la liste D.2
       (D.2 l.32-44 [lu]).
     - `scripts/sceau/verify.sh` l.13 [lu] rejoue le courant ; `sceau/README.md` l.4-5 [lu] donne le motif du
       rescellement.
   - C-4 : `onerror=lever` est posé. Il est prouvé par M12, tué.
   - README (ajout de 19:28:17 UTC, l.50-59 de la copie [lu]) : il porte le serrage « relative et sans `./` », avec la
     manière de produire le fichier, et la consigne « un `SHA256SUMS` versé ne nomme que des pièces versées ».
   - Q-1 reste juste. J'ai recompté l'épingle indépendamment du script (Python : lignes 1-10 et 12 jointes par LF) :
     `7f45c55e…5596`, égale à la constante. Les 11 fichiers sont absents, aucune autre ligne n'est absente, aucune des
     11 n'est en `*.jsonl`, et toutes sont en mode `*`. Le test d'interdit précède l'exemption, qui ne peut donc jamais
     admettre un chemin interdit.
   - Q-3 reste juste : `sg5.rs` l.80-93 [lu], liste à 7 entrées. `test_liste_egale_sg5` exige l'égalité, et
     `cargo test -p xtask` passe (80 + 9).
2. **Sondes d'ouverture et d'impression (fixtures synthétiques, jamais sous un vrai interdit)**.
   - Outils : `outils/sondes.py` (34 cas) et `outils/espion.py`. Ce dernier est un crochet d'audit Python qui journalise
     chaque `open`, `os.scandir` et `os.listdir`, chemin réel compris.
   - Un cas « fuit » si un emplacement interdit est ouvert ou listé, ou si un contenu secret ou son sha256 paraît sur
     la sortie.

   | famille | cas | série a+b+c+d | a+b+c (témoin) |
   |---|---|---|---|
   | lien sur le `SHA256SUMS` | A1-A9 : relatif, absolu, chaîne de liens, détour `..`/`.`/`//`, vers `execution/`, `*.jsonl`, `15-`, `monark-m009a/`, vers un `SHA256SUMS` interdit | 0 fuite, sortie 1, refus « lien … (non ouvert) » | 5 fuites (A3, A4, A5, A8, A9) |
   | lien sur une ligne | B1-B5, dont une chaîne de liens dans le même dossier | 0 fuite, refus « sous un emplacement interdit » | 0 |
   | dossier intermédiaire | C1, C2 (lien vers `rapports`/`execution`), C3 (dossier lien jamais parcouru), C4 (`docs` lui-même lien) | 0 fuite | 0 |
   | dossier nommé `*.jsonl` | C5 (ligne traversante), C6 (`SHA256SUMS` dedans) | **2 fuites → R-1** | 2 |
   | casse | D1 `Rapports/`, D2 `Execution/`, D3 `y.JSONL`, D4 `sha256sums` | 0 fuite (absents ; nom exact) | 0 |
   | forme | E1 `//`, E2 `./`, E3 `..`, E4 `a/./../`, E5 barre finale, E6 absolu, E7 octet nul, E8 interdit direct, E9 voisins `rapportsX/`, `execution-bis/` (témoin : ouverts) | 0 fuite | 0 |
   | lien physique | H1 | 1 fuite (O-3, limite) | 1 |

   Proposition DT4-e : 1 fuite sur 34, H1 seule.
3. **Force des tests : N1 à N8 et M12 tués.**
   - Outil : `outils/mutants_cc.py`. Les mutants y sont reformulés depuis leur description, sans recopier l'outil de
     la G2.
   - Borne : 300 s par run, `start_new_session` et `killpg`. Classement SHOGEN-MUT-FATAL-1.
   - Le script est restauré après la campagne, sha256 contrôlé. `ps` de fin, filtré sur mon dossier : 0 processus.

   | mutant | série | + DT4-e proposé |
   |---|---|---|
   | N1 exemption décalée d'une ligne | tué (failures=2) | tué |
   | N2 épingle : bloc non vide suffit | tué (2) | tué |
   | N3 réel d'un chemin listé non contrôlé | tué (1) | tué |
   | N4 `SHA256SUMS` vide admis | tué (2) | tué |
   | N5 mode `*` refusé | tué (3) | tué |
   | N6 CRLF admis | tué (1) | tué |
   | N7 garde C-1 (interdit) retirée | tué (1) | tué |
   | N8 garde C-1 (hors du dossier) retirée | tué (1) | tué |
   | M12 `os.walk` sans `onerror` | tué (1) | tué |
   | K1 borne d'une ligne sans séparateur | **vivant** | tué (R-2) |
   | K2 borne du `SHA256SUMS` sans séparateur | **vivant** | tué (R-2) |
   | K3 barre oblique inverse admise | **vivant** | tué (R-3) |
   | K4 retour chariot admis | **vivant** | tué (R-3) |
   | K5 `*.jsonl` du réel d'une ligne non refusé | tué (1) | tué |

   - Série : 10 tués sur 14, 0 FATAL. Proposition : 14 sur 14, 0 FATAL.
   - Le rouge de R-1 est montré à part (`R-rouge.txt`). Ce n'est pas un mutant : c'est le script de la série lui-même.
4. **Gates** : `6356a94` + série contre `6356a94` seule, avec `outils/cc_gates.sh` et `cc_tout.sh`.
   - Lignes relevées dans le `gates.yml` de chaque arbre. Elles ne diffèrent que par le plancher 18 → 26.
   - Réseau coupé (`isole.sh`), variables de mandataire et `SHOGEN_S2_CAMPAGNE_CONTROL` retirées par `env -u`,
     `TMPDIR` sous mon dossier.
   - Copie : clone local sparse, sans les dossiers interdits ni `*.jsonl`, historique complet.
   - G5 et G3 `--tree` tournent sur un dépôt jetable des seuls fichiers présents, construit avant tout run. La commande
     G5 est extraite de chaque `gates.yml`, et les deux sont égales octet pour octet (`cmp`).

   | gate | série | tête seule |
   |---|---|---|
   | runner du vérificateur | 0 — 137 ok, 0 échec | 0 — 137 ok |
   | S2 `--egal` | 0 — Ran = 415 (sauts nommant la variable scellée) | 0 — 415 |
   | s2bis `--plancher 341` | 0 — 341 | 0 — 341 |
   | sim-bis `--plancher 279` (clone git) | 0 — 279 | 0 — 279 |
   | calib-actifs `--plancher 65` | 0 — 65 | 0 — 65 |
   | controle `--egal` | 0 — **Ran = 26** (plancher 26) | 0 — Ran = 18 (plancher 18) |
   | g1 : cas du lint R-1 | 0 — 227 ok | 0 — 227 ok |
   | g1 : lint R-1 de l'arbre | 0 | 0 |
   | g1 : `journaux-modele.py` | 0 — 52 exemptés | 0 — 52 |
   | g1 : `docs-sha256sums.py` | 0 — 33 SHA256SUMS, 290 lignes, 11 absentes admises, 4 non listés | sans objet |
   | g5 : cas du hook | 0 — 54 ok | 0 — 54 ok |
   | g5 : grep R-13 | 1 = aucun marqueur | 1 |
   | g3 : cas des secrets | 0 — 147 ok | 0 — 147 ok |
   | g3 : `--tree` | 0 — 1 058 fichiers | 0 — 1 056 |
   | `cargo test -p xtask` (lignes `test result`) | 0 — 80 + 9 passés, 0 échec | 0 — identiques, à la durée près |
   | `cargo xtask verify` (lignes VERDICT seules) | 1 — 8 VERT, 1 ROUGE (1 violation), global ROUGE | 1 — **identique ligne à ligne** (`diff` vide) |

   - Le ROUGE de xtask est préexistant et identique à la tête seule.
   - Le job g1 est complet : quatre étapes après le checkout (l.89-114 [lu]), toutes rejouées.
   - Équivalence de la copie creuse pour ce contrôle : l'index compte 1 123 entrées, toutes en mode 100644, sans lien
     ni sous-module. Le script élague les seuls dossiers que la copie omet. La copie creuse donne donc ici le même
     résultat qu'une copie complète.
5. **Forme**.
   - R-25 (`git apply --numstat`) : DT4-a +200 −1 (4, 96, 100), DT4-b +20 −15, DT4-c +13 −2, DT4-d +50 −6 ; tous
     ≤ 200.
   - TODO/FIXME ajoutés : 0 ; G5 vert.
   - Octets 92 dans les lignes ajoutées : 0 dans a, c et d. Dans b : 1, `"sept violations attendues :\n{motifs}"`,
     échappement Rust voulu, de même forme que la ligne remplacée.
   - Retours chariot : 0.
   - Ajouts datés :
     - README de DT4-c, daté 18:50:07 : diff écrit à 18:50:35.
     - README de DT4-d, daté 19:28:17 : après l'adjudication de 19:26:58 et `D-vert.txt` de 19:28:11, diff écrit à
       19:29:02.
     - Sections du rapport du générateur : la version d'avant G2 (`travail/avant-g2/`, 19:27:31) ne diffère de
       l'actuelle que par l'ajout de la section de 19:40:38 (`diff` : ajout seul). Les sections plus anciennes n'ont
       donc pas été réécrites après leur heure.
     - Aucune heure contredite.
6. **Versement**. Simulation : `outils/versement.sh`, script de la série, sur un arbre synthétique
   `docs/adr-0028/revue-dettes4/` (forme de `revue-dettes3/` [lu] : pièces `-transcrit.md` à plat, plus
   `ADJUDICATION.md`). Résultats :
   - V1 : `SHA256SUMS` écrit dans le dossier par `sha256sum ADJUDICATION.md *-transcrit.md` → **conforme**.
   - V5 : même chose avec `sha256sum -b` (mode `*`) → conforme.
   - V2 : `SHA256SUMS` du dossier de travail du lot recopié tel quel → refus « absent » (`diffs/`, `outils/`,
     `sorties/`).
   - V7 : `g2/cc/SHA256SUMS` versé avec `RAPPORT-CC.md` seul → refus « absent » (`DT4-e-propose.diff`, `outils/`,
     `sorties/`, `NOTES.md` non versés).
   - V3 : `find . -exec sha256sum` → refus « hors forme » (`./`).
   - V4 : fins CRLF → refus « hors forme ».
   - V6 : ligne vide finale → refus « hors forme » (l.6).
   - V8 : pièce retouchée après la somme → refus « somme écrite …, réelle … ».

   **Forme exacte à respecter** :
   - Le dossier versé est hors des préfixes interdits, et aucun composant de son chemin ne finit en `.jsonl`.
   - Le fichier se nomme exactement `SHA256SUMS`.
   - Il est **régénéré dans le dossier versé, sur les pièces versées seules, après leur transcription** :
     `cd <dossier> && sha256sum <fichiers>`.
   - Une ligne par pièce : 64 hexadécimaux minuscules, deux espaces (ou espace et `*`), chemin relatif sans `./`,
     `..`, `//`, absolu ni barre oblique inverse.
   - Fins LF, un seul LF final, aucune ligne vide.
   - Jamais le `SHA256SUMS` du scratchpad, ni celui de `g2/` ou de `g2/cc/`, qui nomment des pièces non versées.
   - Sommes prises sur les octets tels que commis (`.gitattributes` : `* text=auto eol=lf` [lu]) : écrire en LF avant de
     sommer.
   - Toute retouche d'une pièce versée met sa somme à jour dans le même commit.
   - Un sous-dossier versé avec son propre `SHA256SUMS` est contrôlé pour lui-même. Les fichiers non listés sont
     comptés, non refusés.
7. **Aucune dette**.
   - R-1 à R-3 sont corrigeables : ce sont des réserves, avec leur forme.
   - O-3 et O-4 ne sont pas des défauts du contrôle (raisons ci-dessous) : pas de réserve.
   - O-5 est rendu à l'orchestrateur comme question, pas comme dette de ce lot.

## Constats (O-CC-n)

- **O-1 (C-1 tient)** : les 9 cas de lien sur le `SHA256SUMS` sont refusés sans ouverture. Le crochet d'audit ne
  relève aucun `open` sous un interdit. Le témoin a+b+c fuit sur 5 d'entre eux, ce qui montre que la sonde discrimine.
- **O-2 (parcours)** : aucun `os.scandir` sous un dossier interdit, sur 34 cas. `docs/` et `docs/adr-0028/` sont listés
  par nom, ce qui est inévitable (noms seuls).
- **O-3 (limite, H1)** : un lien physique (`os.link`) d'un fichier interdit vers `docs/a/SHA256SUMS` est lu et imprimé.
  `realpath` ne le voit pas. Il est impossible dans un arbre extrait par git, où l'index ne compte que des 100644. Le
  cas équivaut à une copie des octets interdits dans un fichier permis, ce qu'aucun contrôle par chemin ne peut voir.
  Pas de réserve.
- **O-4 (FIFO)** : un `SHA256SUMS` qui est un tube nommé bloque le contrôle (`timeout 10` : sortie 124). Il n'y a ni
  fuite ni faux vert : en CI, le dépassement de la borne du job est un échec fermé. Git ne peut enregistrer un FIFO.
  Pas de réserve.
- **O-5 (casse, hors de mesure)** : sur cet hôte sensible à la casse, `Rapports/` et `Execution/` sont absents (D1,
  D2). Sur un système insensible à la casse qui ne canonise pas `realpath`, `Execution/x.md` serait ouvert. Un tmpfs
  `casefold` est refusé ici (option rejetée, `/sys/fs/unicode` absent) : je ne l'ai pas mesuré [abs]. Sous Windows,
  `ntpath.realpath` passe par `_getfinalpathname` (présent dans `ntpath.py` [lu]), qui rend la casse du disque
  [2nd, non mesuré]. La CI tourne sous Linux. Question à l'orchestrateur : faut-il un serrage `casefold()` dans
  `interdit()` ? Il divergerait de S-G5, sensible à la casse. Je ne le propose pas sans hôte où le mesurer.
- **O-6 (S-G5 et `*.jsonl`)** : `EMPLACEMENTS_INTERDITS` de `sg5.rs` ne porte pas `*.jsonl`. S-G5 ne lit que des `*.md`,
  mais un `*.md` placé sous un dossier `*.jsonl` y serait cité en texte. Ce n'est pas un défaut de DT4. Si
  l'orchestrateur adopte R-1, la même lecture vaudrait pour S-G5 : un item à former, au lot que l'orchestrateur nommera.

## Écarts (E-CC-n)

- **E-CC-1** : pour mesurer la sémantique de `!*.jsonl`, j'ai fait un commit (`--no-verify`) dans un dépôt synthétique
  jetable de mon dossier. Ce dépôt ne contenait aucune pièce du projet : trois fichiers d'un octet. C'est contraire à la
  lettre de la règle 2. Le dépôt a été supprimé aussitôt.
- **E-CC-2** : `grep -n 'D\.2'` sur `ANNEXE-D-preenregistrement.md` a affiché les lignes 3 et 24-30 en entier, plus que
  les titres cherchés. Le fichier n'est pas interdit et n'est pas une pièce D.2.
- **E-CC-3** : listages qui passent des noms par un tube, sans les afficher (comptes seuls) :
  - `git ls-files -t`, `git ls-files -s` et `git ls-files | grep -c` sur ma copie ;
  - `git ls-files -co` dans `cc_gates.sh`, filtré par `[ -f ]` pour le dépôt jetable ;
  - `ls docs` et `ls docs/adr-0028` (non récursifs) de la copie creuse, où les interdits sont absents.

## Journal de provenance (G1 du contre-contrôleur)

- [lu] Dossier du lot :
  - `ADJUDICATION.md` (entier) ;
  - `g2/RAPPORT-G2.md` (entier) ;
  - `RAPPORT-GENERATEUR.md` (entier, avec le `diff` contre `travail/avant-g2/`) ;
  - `INVENTAIRE.md` (entier) ;
  - `NOTES.md` du générateur ;
  - les quatre diffs (entiers) ;
  - `outils/mutants3.py` (liste des mutants, pour les reformuler) ;
  - `g2/outils/gates_g2.sh` et `tout_g2.sh` (forme) ;
  - `isole.sh`.
- [lu] Sur la copie à `6356a94` + série :
  - `xtask/src/sg5.rs` l.78-100, plus les lignes trouvées par grep « interdit » ;
  - `.github/workflows/gates.yml` : l.60-80, l.89-114, lignes `run:` relevées par grep ;
  - `scripts/sceau/verify.sh` l.1-20 ;
  - `docs/adr-0028/sceau/README.md` l.1-8 ;
  - `ANNEXE-D-preenregistrement.md` l.32-44 (et E-CC-2) ;
  - `ANNEXE-B-items.md` l.515 et l.1546 ;
  - `scripts/controle/README.md` l.47-60 ;
  - `.gitattributes` l.1-10 ;
  - `docs/adr-0028/revue-dettes3/` (noms, et noms du `SHA256SUMS`) ;
  - `docs/adr-0028/sim-niveau/SHA256SUMS` (octets 64-66 et chemins, par script).
- Commandes, sorties sous `sorties/` :
  - `cc_tout.sh` → `g-tete-*` et `g-copie-*`, codes dans `g-*-codes.txt` ;
  - `mutants_cc.py` → `mutants-cc.json` (série), `mutants-cc-prop.json` (proposition) ;
  - `sondes.py` → `sondes-serie.txt`, `sondes-abc.txt`, `sondes-prop.txt` ;
  - `proposition.py` → `R-rouge.txt`, `R-vert.txt` ;
  - `versement.sh` → résultats V1-V8 ci-dessus, rejoués après l'écriture de ce rapport.
- Chiffres recomptés par moi :
  - numstat des quatre diffs ; octets 92 et CR ;
  - empreinte de la série ; sha256 des scripts ;
  - épingle `7f45c55e…` ;
  - 11 absents, 0 autre ;
  - 137, 227, 54 et 147 cas ;
  - Ran = 415, 341, 279, 65, 26 et 18 ;
  - 1 058 et 1 056 fichiers ;
  - 80 + 9 tests ;
  - VERDICT identiques ;
  - 33 / 290 / 11 / 4 ;
  - 1 123 entrées d'index en 100644 ;
  - 0 chemin en `.jsonl/` ;
  - PAQUET 0 et 1 ;
  - 14 mutants ; 34 sondes.
- Aucun fichier des dossiers interdits, aucun `*.jsonl` réel, aucune pièce D.2 ouverts ; `SHOGEN_S2_CAMPAGNE_CONTROL`
  jamais posée ; aucun accès réseau (runs sous `isole.sh`). Copies supprimées en fin de travail (`tmp/`), `ps` de fin
  filtré sur mon dossier : 0 processus.

## Passe 2 — section datée du 2026-10-09 20:26:41 UTC (`date -u`) : DT4-e et DT4-f (adjudication du 19:58:14 UTC)

- **Modèle** : `claude-opus-5-5`, effort max (Gate 0 de la passe 1 ; même instance). Heure de début lue : 20:14:36 UTC.
- **Base** : la tête du dépôt réel est relue à `6356a945c4fa…`, inchangée. Le dépôt réel est intact (`git status` : 0
  ligne).
- **Sources lues** [lu] :
  - dernier ajout de `ADJUDICATION.md` (19:58:14) ;
  - section 20:13:36 de `RAPPORT-GENERATEUR.md` ;
  - `DT4-e.diff` et `DT4-f.diff` (entiers) ;
  - `xtask/src/sg5.rs` l.196-280 de la copie (impression des violations et des notes).
- **Série a à f** : `git apply` OK dans l'ordre, sur un clone sparse neuf (sans interdits ni `*.jsonl`). Empreinte
  a|…|f : `55b38839…72de`, égale à celle du générateur. `DT4-e` `40c9b36e…4edc`, `DT4-f` `730ec896…7c54`.

### Verdict de la passe 2 : **CONFORME-AVEC-RÉSERVES (R-4)**

R-1 à R-3 sont levées en entier, et C-8 et C-9 sont justes. Il reste une seule réserve, sur la force des tests :

- **R-4 (tests Python) : aucun témoin ne prouve que le pli de casse épargne les voisins autorisés.**
  - Le mutant PX4 étend les préfixes sans leur barre finale. Il rend donc interdits `docs/rapportsX/`,
    `docs/adr-0028/Execution-bis/`, et tout autre voisin de préfixe. Il reste **vivant** sur la série a à f : aucun cas
    Python ne vérifie qu'un voisin autorisé est encore lu.
  - Côté Rust, ce témoin existe : `temoin_sg5_interdits_voisins_gardent_le_texte`.
  - Forme proposée : `DT4-g-propose.diff` (sha256 `99e70eec…a5b3`, **+3 −0**, `test_interdits`). Quatre voisins sont
    ajoutés : `rapportsX`, `adr-0028/Execution-bis`, `b.jsonlx`, `ADR-00250`. Pour chacun, le cas exige le motif
    « l.1 : x.md absent », ce qui prouve que le voisin est bien lu.
  - Résultat sur une copie : vert, Ran = 26 exact (le plancher ne bouge pas). PX4 est tué. Les 17 mutants Python de la
    passe sont tous tués sur la proposition.

### Points

1. **R-1 à R-3, C-8, C-9**.
   - **R-1 → C-5** : levée. Le cas `b/z.jsonl` est jamais lu, `z.jsonl/x.md` est refusé. Sondes C5 et C6 : refusées
     sans ouverture ni listage.
   - **R-2 → C-6** : levée. K1 et K2 sont tués.
   - **R-3 → C-7** : levée. K3 et K4 sont tués.
   - **C-8, faux interdits** : aucun dans l'arbre. Les 1 123 chemins indexés sont tous ASCII. Le nombre d'interdits est
     de 58 avant et 58 après, pour la règle Python comme pour la règle Rust : 0 chemin autorisé devenu interdit, 0
     interdit perdu. Le masque S-G5 couvre 11 `*.md` avant et 11 après.
   - **C-8, sondes** :
     - témoin P3 (voisins en casse mêlée, `RapportsX`, `Execution-bis`, `b.JSONLx`, `ADR-00250`) : 4 `SHA256SUMS` lus,
       conforme ;
     - P1 (`Rapports/` et `adr-0028/EXECUTION/`) et P2 (`b/Z.JSONL/`) : jamais lus, aucun contenu imprimé ;
     - D1 à D3 : désormais refusés « interdit ».
   - **C-9, sortie de S-G5** : `sg5.rs` l.202-262 [lu]. Un seul drapeau `interdit` par fichier règle les deux branches
     (violation et « non contrôlé »). Pour un interdit, la sortie porte le chemin et la ligne, jamais le texte : le pli
     ne fait qu'élargir ce masque.
   - **C-9, ce que S-G5 lit** : S-G5 ouvre encore les `*.md` interdits pour en chercher les citations. Ce choix vient
     de SG5-INTERDITS (verdict inchangé) ; DT4-f ne l'introduit pas.
   - **C-9, test** : `mutant_sg5_interdits_casse_et_jsonl` ne contrôle que les motifs du rapport, branche corpus
     complet. La branche corpus incomplet partage le même drapeau, donc aucune réserve.
   - **C-9, Python et Rust** : `casefold` et le pli Rust (majuscules puis minuscules) peuvent différer sur du non-ASCII
     autre que `ſ` [inféré]. Effet nul aujourd'hui (0 chemin non ASCII) et toujours dans le sens du serrage : pas de
     réserve.
2. **Mutants** (borne 300 s, `start_new_session` + `killpg`, fichiers restaurés au sha256, 0 FATAL).
   - Python, `outils/mutants_p2.py`, sur la série a à f : **17 tués sur 17**.
     - N1 à N8, M12, K1 à K5 ;
     - mutants neufs PX1 (`.jsonl` testé sur le chemin non plié), PX2 (`.jsonl` sur les seuls dossiers), PX3 (pli
       limité au premier composant).
   - PX4 (sur-pli) : **vivant** sur la série, d'où R-4 ; tué sur la proposition.
   - Rust, `outils/mutants_rs_p2.py` : RX1 (`.jsonl` sur le chemin non plié) et RX2 (dernier composant seul) sont
     tués (`test result: FAILED`, 6 passed, 1 failed).
   - Sondes rejouées (`sorties/p2-sondes.txt`, 37 cas) : 1 fuite, H1 (lien physique, limite admise en passe 1). C5, C6,
     P1 et P2 sont refusés sans ouverture.
3. **Gates** : `6356a94` + a à f contre `6356a94` seule, `outils/cc_tout2.sh`.

   | gate | série a à f | tête seule |
   |---|---|---|
   | runner du vérificateur | 0 — 137 ok | 0 — 137 ok |
   | S2 | 0 — Ran = 415 | 0 — 415 |
   | s2bis | 0 — 341 | 0 — 341 |
   | sim-bis (clone git) | 0 — 279 | 0 — 279 |
   | calib-actifs | 0 — 65 | 0 — 65 |
   | controle | 0 — **Ran = 26 exact** | 0 — 18 |
   | job g1 : cas du lint, lint, journaux-modele, docs-sha256sums | 0 — 227 ok, lint 0, 52 exemptés, conforme (33, 290, 11, 4) | 0 (sans l'étape neuve) |
   | hooks | 0 — 54 ok | 0 — 54 ok |
   | G5 grep (commande égale octet pour octet) | 1 = aucun marqueur | 1 |
   | G3 cas, `--tree` | 0 — 147 ok ; 1 058 fichiers | 0 — 147 ; 1 056 |
   | `cargo test -p xtask` | 0 — **81** + 9 passés (le test neuf) | 0 — 80 + 9 |
   | `cargo xtask verify`, lignes VERDICT | 1 — 8 VERT, 1 ROUGE (1 violation) | identiques ligne à ligne (`diff` vide) |

4. **Forme**.
   - R-25 : DT4-e +17 −10, DT4-f +42 −3 ; la proposition DT4-g +3.
   - `cargo fmt --all --check` : sortie 0 sur la tête comme sur la série, 0 ligne.
   - Retours chariot : 0. TODO/FIXME ajoutés : 0.
   - Octets 92 :
     - 0 dans DT4-e ;
     - 3 lignes dans DT4-f, échappements Rust voulus (`\u{17F}`, deux `\n`) ;
     - 0 dans DT4-g.
   - Section du générateur datée 20:13:36 : postérieure aux diffs (20:01) ; aucune heure contredite.

**Écart de la passe 2** :
- **E-CC-4** : le détecteur de mes sondes est sensible à la casse. Pour P1 et P2, l'absence de fuite repose donc sur la
  sortie (« 0 SHA256SUMS », aucun contenu imprimé) et sur l'élagage du parcours, pas sur le journal d'audit.

**Provenance (passe 2)** :
- Commandes et sorties sous `sorties/p2-*` :
  - codes, Ran, lignes `test result`, VERDICT ;
  - `p2-fmt-*` ;
  - `p2-mutants-py.json`, `p2-mutants-rs.json`, `p2-mutants-py-PX4*.json`, `p2-mutants-py-prop.json` ;
  - `p2-sondes.txt`.
- Recensement des faux interdits : script Python sur `git ls-files -z` de la copie, comptes seuls affichés, plus la
  liste des chemins autorisés devenus interdits (vide).
- Copies supprimées en fin de passe ; `ps` de fin filtré sur mon dossier : 0.
