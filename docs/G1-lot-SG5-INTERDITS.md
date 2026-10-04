# Lot SG5-INTERDITS : rapport du worker et journal G1

**Gate 0** : modèle résolu `claude-opus-5-5` (identifiant exact), effort max.
**Horloge** (`date -u`) : début dim. 4 oct. 2026 13:23:42 UTC, fin 13:45:33 UTC.
**Brief** : sha256 recalculé `930d8826f2781770140fe22adc818a873189a5da09b95e45128e61ffe7129300`, conforme.
**Base** : `75bf25862c12332bc8aba2dcd0b78d161ee1fa5b` (branche `claude/compassionate-noether-szmdyj`, arbre propre). La tête a avancé pendant le lot, à `2c2fbe9c57fa80976a7598fec841b54dd3c09030` (voir E-3). Tout a été recontrôlé sur cette tête.
**Git** : aucune opération en écriture sur le dépôt. Tout le travail est fait dans la copie `git archive` du brief, avec cible cargo et `TMPDIR` dédiés.

## 1. Résumé

- **Ce qui change** : quand une citation introuvable se trouve dans un emplacement interdit, S-G5 n'imprime plus que `chemin:ligne`, jamais le texte. C'est vrai dans les deux régimes, en note (corpus incomplet) comme en violation (corpus complet).
- **Ce qui ne change pas** : le verdict et les comptes.
- **Note ajoutée** : une ligne de note donne le nombre de lignes masquées.
- **Tests** : rouge avant (2 échecs, sur l'assertion « texte imprimé »), vert après (80 + 9 tests).
- **Mutants** : 21 sur 21 tués, aucun FATAL.
- **Écart principal** : `verify` sur la copie reste ROUGE par S-G9 seule. Ce rouge préexiste, il est identique sans mon changement : c'est l'item SHOGEN-SG9-COPIE-INTERDITS-1. Les autres gates ainsi que fmt, no_std et clippy sont VERT.
- **Items à former** : trois, dont une fuite latente de même nature dans S-G4, démontrée sur fixture.

## 2. Livrables

Dossier du lot : `/tmp/claude-0/-home-user-shogen/7ba84933-ba6d-5813-9ef4-ca3ac4febd16/scratchpad/s2bis/sg5/`

| fichier | sha256 | lignes |
|---|---|---|
| `sortie/01-tests-sg5-interdits.diff` (`xtask/tests/mutants.rs`) | `a6b795286fd6d08158ad58b6a19fe386bd1a7b10787891a684bc05ab0032483b` | +136 −0 |
| `sortie/02-sg5-emplacements-interdits.diff` (`xtask/src/sg5.rs`) | `ab780a83216186e4aecb06197a6dabe6dea6ccc7a8e00b77d955c42869a3fb03` | +52 −7 |
| `sortie/SHA256SUMS` (53 entrées : diffs, outils, journaux, fichiers avant/après) | `5021c17c059fd6cda21f738ccaa6c17b336505c2ef88f5e112d5f788a3edc3f5` | `sha256sum -c` : 0 |

Fichiers obtenus après application :
- `xtask/src/sg5.rs` : `57c4c71cec68cccba838230c418dfe62041ca67167c26df630cd85a34467a4d9`.
- `xtask/tests/mutants.rs` : `8c223c806cf16fc9a1b8c8e704a982b6f2aba51e0f77b7d6c9baa06ed7e7c20d`.

Contrôle d'application :
- `git apply --check --whitespace=error` sort 0, pour chaque diff seul et pour 01 puis 02.
- Ce contrôle a été fait sur une extraction neuve de `75bf258`, puis refait sur `2c2fbe9`.
- Les deux diffs ensemble font 188 lignes ajoutées, sous le plafond de 200 d'un commit.

Hygiène :
- R-13 : aucun `TODO`, `FIXME` ni `XXX` dans les lignes ajoutées.
- Aucune espace en fin de ligne, aucun caractère de contrôle.
- R-8 : aucune dépendance nouvelle (std seule, `--locked` vert).

## 3. Construction

Fichier `xtask/src/sg5.rs` :
- **Liste** `EMPLACEMENTS_INTERDITS` (`pub(crate)`) : `docs/15-`, `docs/16-`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`.
  - Ce sont des préfixes exacts de chemin relatif, avec `/` comme séparateur (invariant 1 d'ADR-0013).
  - À HEAD, `docs/15-*` et `docs/16-*` sont des fichiers, pas des dossiers. Ces deux préfixes couvrent les deux cas.
- **Prédicat** `emplacement_interdit(relatif)` (`starts_with`), évalué une fois par fichier.
- **Corpus incomplet** : la note est `chemin:ligne` seul. L'ancienne forme `chemin:ligne — « texte »` est gardée hors emplacement interdit.
- **Corpus complet** : la violation reste à `chemin:ligne`, avec un motif constant : `citation introuvable dans le registre et les octets détenus (emplacement interdit : texte jamais imprimé)`. L'extrait reste vide.
- **Note toujours imprimée** : `emplacements interdits (SHOGEN-SG5-NOTES-INTERDITS-1) : N fragment(s) introuvable(s) rapporté(s) par chemin:ligne seul, texte jamais imprimé ; verdict inchangé`.
- **Doc du module** : elle porte la règle et sa limite (un emplacement absent de la liste imprime son texte).

**Choix motivé : masquer les emplacements interdits seulement, pas partout.**
1. En régime CI (corpus incomplet), la copie imprime 267 fragments non contrôlés de documents publics (mesuré). Leur texte est ce qui permet de les vérifier ensuite sur le corpus complet. Avec `chemin:ligne` seul, il faudrait ouvrir chaque fichier, et une ligne qui porte plusieurs fragments deviendrait ambiguë.
2. Masquer partout changerait un contrat déjà revu : le témoin `temoin_sg5_corpus_incomplet_dit_partiel_et_liste_les_non_controles` (G2 du 2026-08-13, majeure 4) exige que chaque fragment non contrôlé soit listé nommément. Le mutant M09 montre exactement quels tests portent ce contrat.
3. Le prix de la liste (il faut la tenir à jour) est nommé dans le code et rendu en item I-2.

Si tu préfères masquer partout : c'est une ligne (`let interdit = true;`) plus l'adaptation des deux témoins.

## 4. Tests : rouge avant, vert après

Trois tests, dans une section de `mutants.rs` placée avant S-G9 :
- `mutant_sg5_interdits_complet_chemin_ligne_sans_texte` (corpus complet) et `mutant_sg5_interdits_incomplet_chemin_ligne_sans_texte` (corpus incomplet).
  - Les fixtures factices sont les six emplacements, recopiés du brief indépendamment du code.
  - Chaque fixture porte une citation marquée `zorglub0` à `zorglub5`, à la ligne 3.
  - Les tests vérifient d'abord le verdict : 6 violations en corpus complet ; VERT avec 8 fragments non contrôlés en corpus incomplet.
  - Puis ils vérifient la **sortie réelle du binaire** (`CARGO_BIN_EXE_xtask gates`) : aucun `zorglub`, et chaque `chemin:3` présent.
  - Enfin, ils vérifient la note (6 lignes masquées).
- `temoin_sg5_interdits_voisins_gardent_le_texte` : sur `docs/150-…`, `docs/rapports-publics/…`, `docs/adr-0028/voisin.md` et `s2-harness/docs/rapports/…`, le texte reste imprimé (bornes exactes des préfixes).

Résultats :
- **Rouge avant** (`journal/01-rouge-avant.txt`, `sg5.rs` d'origine `b60518b2…`) : 78 passent, 2 échouent. Les deux échecs sont à `mutants.rs:799`, avec le message « texte d'une citation en emplacement interdit imprimé ». Les assertions de verdict passent sur le code d'origine.
- **Vert après** (`02-vert-apres.txt`, puis `05-final-xtask-tests.txt`) : 80 + 9 passent.
- **Rejeu avec les diffs livrés** (`06-rejeu-*`) : le diff 01 seul donne 2 échecs (ligne 799) ; 01 + 02 donnent 80 tests OK.
- **Suite `s2-harness`** (sans `SHOGEN_S2_CAMPAGNE_CONTROL`) : 405 tests OK, 2 sautés (état normal), avant et après.
- **Sortie de S-G5 sur la copie** : elle ne diffère que par la nouvelle note (0 masqué). Les comptes 310 contrôlés, 6669 écartés et 267 non contrôlés sont identiques.

## 5. Mutants : 21 sur 21 tués

Le lanceur est `outils/mutants_sg5.py`. Il construit d'abord (`--no-run` doit sortir 0, sinon FATAL), puis classe : sortie 0 = VIVANT ; sortie 101 avec « test result: FAILED » = TUÉ ; toute autre sortie = FATAL.
- Chaque mutant a recompilé `xtask` une fois.
- Les 21 sources mutés ont 21 sha256 distincts.
- `sg5.rs` a été restauré (sha256 contrôlé).
- Journaux : `journal/mutants/M01…M21.txt` ; bilan : `04-mutants-bilan.txt`.

| id | mutation | tué par |
|---|---|---|
| M01–M06 | un préfixe retiré de la liste (chacun des six) | les deux cas de non-régression |
| M07 | `starts_with` remplacé par `contains` | témoin voisins |
| M08 / M09 | prédicat toujours faux / toujours vrai | les deux cas / cas incomplet, témoin existant, témoin voisins |
| M10–M12 | bornes `docs/15`, `docs/rapports`, `docs/adr-0028/` | témoin voisins |
| M13 / M14 | texte imprimé (corpus incomplet / complet) | cas incomplet / cas complet |
| M15 / M16 | ligne perdue / ligne 0 | cas incomplet / cas complet |
| M17 / M18 | fragment sauté ; violation devenue note muette (le verdict change) | les deux cas / cas complet |
| M19–M21 | compte jamais incrémenté, compte sur tout fragment, note retirée | cas de non-régression |

## 6. `cargo --locked xtask verify` sur la copie

Sortie redirigée vers `journal/05-final-verify.txt` et `08-tete-2c2fbe9-verify.txt` ; seules les lignes de verdict ont été lues.
- S-G1 à S-G8 : VERT. fmt, no_std et clippy `-D warnings` : VERT.
- S-G9 : ROUGE, une violation, `docs/17-modele-de-menace.md:70`, motif « (a) référence : fichier introuvable depuis la racine ».
- **Le résultat est identique sur la copie vierge** (`03-verify-base.txt`).

## 7. Écarts

- **E-1** : la consigne « verify vert sur ta copie » est intenable sans toucher S-G9, hors G0.
  - Cause mesurée par `outils/cause_sg9.py`, qui n'affiche que des booléens : la référence n° 3 de la ligne 70 vise un fichier présent à HEAD, sous le préfixe n° 4 (`docs/rapports/`), exclu de la copie.
  - C'est l'item SHOGEN-SG9-COPIE-INTERDITS-1 (B.51, ouvert).
  - Suggestion : jusqu'à sa fermeture, écrire dans le gabarit de brief « vert hors S-G9 docs/17:70 ».
- **E-2** : une recherche `git grep` sur les noms des dossiers interdits a affiché quatre lignes de `JOURNAL.md` (l.53, 102, 208, 268), coupées à 220 caractères. `JOURNAL.md` n'est ni dans les interdits du brief ni dans D.2. Aucun chiffre n'a été repris.
- **E-3** : la tête a avancé (commit `2c2fbe9`, 13:42:52 UTC). Il touche 4 fichiers : `JOURNAL.md`, deux sous `docs/adr-0029/calib/`, un sous `scripts/controle/sorties-fm11/`. Aucun n'est sous `xtask/`. Diffs, tests et `verify` ont été rejoués sur cette tête : résultats identiques.
- **E-4** (SHOGEN-HARNAIS-ECHAPPEMENTS-1) : dans un outil Python, la séquence `\u00ab` que j'ai tapée a été écrite comme le caractère « littéral (constaté par `od -c` : 302 253). Le sens est le même. Les `\n` des tests Rust sont restés intacts (vérifié par `od -c`).
- **E-5** : deux défauts du lanceur de mutants, corrigés avant la campagne comptée.
  - M21, tel que je l'avais d'abord écrit, changeait le libellé de la note au lieu de la retirer. Corrigé avant tout lancement.
  - L'essai de M01 seul ne gardait pas la sortie de construction. Le lanceur a été corrigé et la campagne entière relancée ; l'essai n'est pas compté.
- **E-6** : le test de bout en bout n'a pas tourné sous Windows (hôte Linux), alors que `squelette.yml` lance `cargo test --workspace` sur `windows-latest`. L'analyse dit qu'il doit passer (séparateurs `/` via `chemin_relatif`, `println!` écrit `\n`, chemin `.exe` donné par cargo), mais ce n'est pas vérifié.
- **E-7** : le déclencheur de SHOGEN-XTASK-TMP-NOMS-FIXES-1 (« prochain lot qui touche `xtask/tests` ») est atteint par ce lot. Je ne l'ai pas traité (hors ligne G0). Mes 3 tests suivent la convention existante (noms fixes sous `temp_dir`) ; j'ai travaillé avec un `TMPDIR` dédié. À toi de décider.
- **E-8** : la fuite citée par l'item (« mesuré : une note Pocket », B.51) est de seconde main [2nd]. Je ne l'ai pas re-mesurée sur l'arbre réel, volontairement. Ma preuve porte sur le mécanisme, sur fixtures factices.

## 8. Items à former (PAROXYSME)

- **I-1, SHOGEN-SG4-EXTRAIT-INTERDITS-1** (même nature que l'item du lot, latente)
  - Constat : S-G4 imprime en entier la ligne d'une violation située dans un emplacement interdit.
  - Démontré avec le binaire corrigé sur une fixture factice : `docs/rapports/factice.md:5`, puis la ligne entière après `|` (`journal/07-controle-corrige-demo-sg4.txt`).
  - Prix : extrait vide quand `crate::sg5::emplacement_interdit(&relatif)`, un test et ses mutants.
- **I-2, SHOGEN-INTERDITS-LISTE-UNIQUE-1**
  - Constat : la liste des emplacements vit maintenant dans le code, dans les briefs (`tar --exclude`), en partie dans `scripts/controle/fm11.py` et dans mon outil, sans lien mécanique. Un emplacement ajouté aux briefs mais pas au code imprimerait son texte.
  - Prix : une liste versionnée unique et un test.
- **I-3, SHOGEN-SG5-INTERDITS-LIENS-1** (basse)
  - Constat : le recensement suit les liens symboliques de dossiers (`is_dir()`). Un lien sous `docs/` vers un emplacement interdit exposerait ses citations sous un chemin autorisé.
  - Mesuré : 0 lien symbolique sous `docs/` et `s2-harness/` à HEAD.
  - Prix : refuser les liens (incident) ou canoniser, avec un test.

## 9. Contrôle proposé après application sur l'arbre réel

```
cargo --locked xtask verify > <fichier> 2>&1
python3 -B /tmp/claude-0/-home-user-shogen/7ba84933-ba6d-5813-9ef4-ca3ac4febd16/scratchpad/s2bis/sg5/outils/controle_sortie_verify.py <fichier>
```

L'outil n'imprime que des comptes, jamais un chemin ni un texte. Attendu : fuites 0, note égale au nombre de lignes masquées, extraits d'autres gates 0, sortie 0.
- Validé sur sorties réelles du binaire (`journal/07-*`) : binaire d'origine, 6 fuites (sortie 1) ; binaire corrigé, 0 fuite et 6 masqués (sortie 0) ; démo S-G4, 1 extrait (sortie 1).
- Sur l'arbre réel, S-G5 lit 8 `.md` dans des emplacements interdits : 2 sous `docs/rapports/`, 1 sous `docs/adr-0025/`, 3 sous `docs/pocket-report/`, et les 2 fichiers `docs/15-*`/`docs/16-*`. Comptés par leurs noms (`git ls-tree`) ; aucun contenu ouvert.

## 10. Journal G1 (provenance)

**Lectures [lu]**
- Le brief.
- G0 `docs/adr-0029/G0-lots-S2BIS.md` (24 lignes ; ligne du lot : l.12).
- ADR-0028 `ANNEXE-B-items.md` l.800–859 (item l.828 ; aussi l.832 et l.834).
- `ANNEXE-D-preenregistrement.md` l.32–48 (D.2), plus les lignes affichées par une recherche de « D.2 » et « D.4 ».
- `docs/PASSATION-CLOUD.md` : titres et l.101–157.
- Code de `xtask` lu en entier : `sg5.rs`, `rapport.rs`, `documents.rs`, `sg4.rs`, `roles.rs`, `lib.rs`, `main.rs`.
- Code de `xtask` lu en partie : `source.rs` (`ligne_de`), `sg9.rs` l.1–130, `sg2.rs` l.195–248, `tests/mutants.rs` l.1–175 et l.376–755, `tests/reproductible.rs` l.1–40.
- Configuration : les deux `Cargo.toml` (racine et `xtask`), `.cargo/config.toml`, `rust-toolchain.toml`, `scripts/controle/fm11.py`, et une recherche dans `.github/workflows/`.

**Seconde main [2nd]** : la note Pocket mesurée et le VERT de S-G4 sur l'arbre réel, cités tous deux de B.51. Aucun résumé [abs] utilisé.

**Jamais ouverts** : les six emplacements interdits, tout `*.jsonl`, toute pièce de D.2.

**Exposition FM-1.1** : ma transcription contient des motifs par leur nom. Ils viennent de D.2 (annexe D, non interdite), de `fm11.py`, du chemin de copie imposé et de la liste du code. La cartographie l.51 et ADR-0025 l.14 n'ont jamais été affichées ; je n'ai vu que leurs sha256, dans `fm11.py`. Fragments attendus : 0.

**Chiffres recomptés de première main** :
- Tests `xtask` : 77 + 9 avant, 80 + 9 après ; rouge 78/2.
- `s2-harness` : 405 tests (2 sautés), deux fois.
- Mutants : 21/21.
- Diffs : +136/−0 et +52/−7.
- S-G5 sur la copie : 310 / 6669 / 267.
- Copie : 144 `.md` sous `docs/`, 2 sous `s2-harness/`.

Les commandes et sorties sont dans `journal/` : `00-*` départ, `01-*` rouge, `02-*` et `05-*` vert, `03-*` verify avant et après, `04-*` mutants, `06-*` rejeu, `07-*` outil de contrôle, `08-*` tête `2c2fbe9`.

**Nettoyage** : j'ai supprimé les copies et cibles de build redondantes. Dossier restant : 388 Mo (`arbre`, `cible`, `rejeu-2c2fbe9`, `orig`, `sortie`, `journal`, `outils`, `tmp`).
