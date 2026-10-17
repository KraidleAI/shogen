# Rapport du générateur du groupe C (transcrit)

> Transcription par l'orchestrateur le 2026-10-17 07:31:23 UTC du fichier garde-fous/p3c/RAPPORT-GENERATEUR.md ; contrôle FM-1.1 du transcript du générateur par le fm11.py versé : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5 (308 occurrences, aucune autre). Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Rapport du générateur G1 — GARDE-FOUS phase 3, groupe C (journal des refus et lints de l'arbre)

- Gate 0 : modèle `claude-opus-5-5` (identifiant donné par le système à ce générateur), effort `high`, fiche
  `shogen-worker`. Ce rapport ne fait pas preuve du modèle résolu (lecture de l'orchestrateur).
- Rattachement : annexe B (`docs/adr-0028/ANNEXE-B-items.md`) l.1864 (B.108 : SHOGEN-GARDE-FOUS-ORCH-1, phase 3,
  lecture du journal des refus, restante), l.1874 (SHOGEN-GARDE-D3-MOT-COMMUN-1), l.1890 (B.109 :
  SHOGEN-MOTIFS-ARBRE-REDOS-1) ; ADR-0028. Lignes lues avant tout code ([lu]).
- Base : tête du dépôt `fddedcfe6c64c43c5c25aa1477f1b8fe1d6f9933` (lue par `git rev-parse HEAD`), copie creuse par
  `git archive` d'une liste explicite de chemins, chaque chemin passé par `garde_commun.chemin_interdit` (0 écarté) ;
  commit de base de la copie jetable `09eba7a`. Dépôt jamais écrit.
- Écart de base (rendu à l'orchestrateur) : la tête du dépôt a avancé pendant le lot, de `fddedcf` à `fe9a72b`
  (un commit, FORGE-PR12) ; `git diff --stat fddedcf fe9a72b` limité aux chemins touchés par la série
  (`scripts/controle`, `.claude/hooks`, `.github/workflows/gates.yml`) est vide : la série s'applique de même sur
  `fe9a72b`, non rejouée sur une copie de cette tête.
- Série (diffs dans `diffs/`, à appliquer dans cet ordre, chacun sur la tête laissée par le précédent) :

| ordre | diff | item | lignes ajoutées / retirées | suite du job après le diff |
|---|---|---|---|---|
| 1 | `GF3C-1-d3-mot-commun.diff` | SHOGEN-GARDE-D3-MOT-COMMUN-1 | +36 −3 | Ran 178, conforme |
| 2 | `GF3C-2-motifs-arbre.diff` | SHOGEN-MOTIFS-ARBRE-REDOS-1 | +150 −7 | Ran 179, conforme |
| 3 | `GF3C-3-journal-refus.diff` | SHOGEN-GARDE-FOUS-ORCH-1, phase 3 (écriture) | +186 −2 | Ran 181, conforme |
| 4 | `GF3C-4-releve-refus.diff` | SHOGEN-GARDE-FOUS-ORCH-1, phase 3 (relevé) | +86 −6 | Ran 182, conforme |
| 5 | `GF3C-5-lecteur-refus.diff` | SHOGEN-GARDE-FOUS-ORCH-1, phase 3 (lecture) | +109 −4 | Ran 183, conforme |

Le journal des refus est découpé en trois diffs pour tenir sous 200 lignes ajoutées par diff (R-25). Plancher du job
`controle-unittest` recalé par chaque diff (177 lu dans `gates.yml` de la copie, puis 178, 179, 181, 182, 183,
`--egal`), un commentaire daté par diff au-dessus du job. Chaque diff ajoute en fin de `scripts/controle/README.md` un
ajout daté (heure lue par `date -u`) ; aucune ligne existante d'un fichier cité par numéro n'est décalée (contrôle C7 de
`avant_acte.py diff`, sortie 0).

## Contrôles de réception rejoués

- `python3 -I -B scripts/controle/avant_acte.py --depot . diff --fichier <diff> --rapport <rapport>`, chaque diff sur
  une copie à l'état d'avant lui, avec l'outil de cet état (comme l'orchestrateur à la réception) : sortie 0, aucune
  ligne, pour les cinq (D1, D2, C4, C5, G5, C7, C8, RX, D3, D4).
- Motif R-13 du job g5 sur les lignes ajoutées des cinq diffs : 0 marqueur ; `git grep` du même motif sur les fichiers
  touchés de l'état final : sortie 1 (rien).
- Ligne du job `controle-unittest` rejouée après chaque diff (`python3 -B enforcement/verdict-suite-s2.py
  scripts/controle --aucun-saut --egal --plancher N`, TMPDIR dédié) : conforme à chaque pas (tableau ci-dessus).
- Tests neufs sous `python3.12` et `python3.13`, `-X dev -W error` : sortie 0, aucune ligne `Exception ignored` ni
  `Warning`.
- Application en série des cinq diffs sur la base (`git apply --index`) : l'arbre obtenu égale l'état final.

## GF3C-1 — SHOGEN-GARDE-D3-MOT-COMMUN-1 (annexe B l.1874)

- Ce que l'outil refuse désormais : D3 (`avant_acte.py diff`) refuse une fonction publique ajoutée à
  `scripts/controle/*.py` dont le nom n'est au README que comme mot courant (`non suivi`), dans un autre mot
  (`suivis`, `poursuivi(x)`) ou dans un passage de code qui ne fait que le porter ; il l'admet nommée en code
  (passage entre accents graves qui est le nom seul ou qualifié : `suivi`, `avant_acte.suivi`) ou en signature
  (`suivi(`, en code ou non). Fonction `nomme_en_code(nom, texte)`.
- Preuve rouge/vert : `test_d3_mot_commun` rouge contre l'outil de la base (`tmp/r5-C1-rouge.txt` :
  `FAILED (failures=1)`), vert après le diff (`tmp/r5-C1-vert.txt` : `OK`).
- Mutants (chaque ligne : le test nommé est rouge sous le mutant lancé seul ; dernière colonne : classement par la
  commande du job, `scripts/controle/mutants.py`) :

| mutant | fichier | avant (abrégé) | après (abrégé) | test rouge sous le mutant (seul) | job `controle-unittest` |
|---|---|---|---|---|---|
| D3-1 | `avant_acte.py` | `if not nomme_en_code(nom, readme):` | `if not re.search("(?<![A-Za-z0-9_])" + re.escape(nom) + "(?![A-Za-z0-9…` | `test_d3_mot_commun` : tué | tué |
| D3-2 | `avant_acte.py` | `return any(re.fullmatch(code, x.strip()) for x in` | `return any(re.search(code, x.strip()) for x in` | `test_d3_mot_commun` : tué | tué |
| D3-3 | `avant_acte.py` | `return any(re.fullmatch(code, x.strip()) for x in re.findall("'([^'" +…` | `return False or bool(` | `test_d3_mot_commun` : tué | tué |
| D3-4 | `avant_acte.py` | `or bool( re.search("(?<![A-Za-z0-9_.])" + re.escape(nom) + "[(]", text…` | `or False` | `test_d3_mot_commun` : tué | tué |
| D3-5 | `avant_acte.py` | `re.search("(?<![A-Za-z0-9_.])" + re.escape(nom) + "[(]", texte)` | `re.search(re.escape(nom) + "[(]", texte)` | `test_d3_mot_commun` : tué | tué |
| D3-6 | `avant_acte.py` | `nomme_en_code(nom, readme)` | `nomme_en_code(readme, nom)` | `test_d3_mot_commun` : tué | tué |
| D3-7 | `avant_acte.py` | `code = "(?:[A-Za-z0-9_]+[.])*" + re.escape(nom)` | `code = re.escape(nom)` | `test_d3_mot_commun` : tué | tué |

- Limites : D3 juge le README entier, non le passage de l'ajout daté ; un nom en code dans un paragraphe sans rapport
  compte. La forme `nom(` hors code compte comme signature, même dans une phrase.
- Phrase de fermeture proposée (pour l'annexe B) : SHOGEN-GARDE-D3-MOT-COMMUN-1 fermé : D3 cherche le nom de la fonction en code ou
  en signature (`nomme_en_code`), cas `test_d3_mot_commun`, mutants D3-1 à D3-7 tués (GF3C-1).

## GF3C-2 — SHOGEN-MOTIFS-ARBRE-REDOS-1 (annexe B l.1890)

- Ce que l'outil refuse : `avant_acte.py motifs --arbre` (`motifs_arbre(a, fautes)`) passe `motifs_suspects` sur
  tous les motifs déjà dans l'arbre de `scripts/controle/`, `.claude/hooks/` et `enforcement/` : appels de `re` des
  `.py` lus sur l'arbre d'ast (`motifs_du_code(texte)` de `garde_commun.py` : appel sur plusieurs lignes,
  concaténation, `chr(N)`, `sep.join`, noms de premier niveau, drapeaux `re.I` et `re.X`), motifs YAML des `.yml`
  (`motifs_ajoutes`). Une ligne `REFUS RX chemin:ligne` par motif suspect, sortie 1 ; `ADMIS RX` sous `redos-admis`
  (la ligne d'un appel sur plusieurs lignes est l'appel entier) ; `NON-LU chemin:ligne` pour un motif construit
  autrement, jamais jugé ; code illisible par ast : avertissement ; `__pycache__` et interdits sautés.
- Preuve rouge/vert : `test_motifs_arbre` (motifs suspects plantés dans un dépôt temporaire) rouge contre l'outil
  d'avant (`tmp/r5-C2-rouge.txt` : sortie 3, sous-commande inconnue), vert après (`tmp/r5-C2-vert.txt`).
- Passage réel sur l'arbre (copie à la base `09eba7a`, outil de l'état final ; sortie `tmp/arbre-reel-base.txt`,
  sha256 `6543d076cb55d43364042c8747abaa17df97c3cd1d7c2e3cae6e128331873ff4`) : 136 motifs lus, 21 non lus, un motif
  suspect : `scripts/controle/tests/test_garde_codeql.py:23` (`ANCIEN`, l'ancien `NOM_PROPRE` d'avant CQ-1, gardé à
  dessein par le cas CQ-1 pour comparer les mots reconnus ; quantificateurs imbriqués). Non corrigé (consigne du
  brief). Le `NOM_PROPRE` actuel du crochet n'est pas signalé. État final de la série : 145 lus, 22 non lus, même
  suspect seul (`tmp/arbre-reel-final.txt`, sha256 `263ca9c8e900dab34207ff07f9a99b0b25669ef2c4cb1aa30806ba075590981c`) ;
  les motifs neufs de la série (masques de secret du crochet) sont lus et sains.
- Les 21 motifs non lus de la base, chacun construit hors littéraux (variable, `re.escape`) :
  `scripts/controle/avant_acte.py` l.321, 322, 590, 753 ; `scripts/controle/fm11.py` l.43 ;
  `scripts/controle/garde_commun.py` l.75, 152, 321 ; `scripts/controle/tests/test_gabarit_controle.py` l.63, 64 ;
  `.claude/hooks/acte_shell.py` l.114 ; `.claude/hooks/garde_faits.py` l.96, 238, 254, 480, 564, 822 ;
  `enforcement/runners-epingles.py` l.35 ; `enforcement/verdict-suite-s2.py` l.280, 281, 324.
- Mutants :

| mutant | fichier | avant (abrégé) | après (abrégé) | test rouge sous le mutant (seul) | job `controle-unittest` |
|---|---|---|---|---|---|
| MA-1 | `garde_commun.py` | `return noms.get(n.id)` | `return None` | `test_motifs_arbre` : tué | tué |
| MA-2 | `garde_commun.py` | `return None if g is None or d is None else g + d` | `return None` | `test_motifs_arbre` : tué | tué |
| MA-3 | `garde_commun.py` | `return chr(n.args[0].value)` | `return None` | `test_motifs_arbre` : tué | tué |
| MA-4 | `garde_commun.py` | `return None if sep is None or None in parts else sep.join(parts)` | `return None` | `test_motifs_arbre` : tué | tué |
| MA-5 | `garde_commun.py` | `tete = "(?i)" * bool(` | `tete = "" * bool(` | `test_motifs_arbre` : tué | tué |
| MA-6 | `garde_commun.py` | `out.append((n.lineno, n.end_lineno,` | `out.append((n.end_lineno, n.end_lineno,` | `test_motifs_arbre` : tué | tué |
| MA-7 | `avant_acte.py` | `DOSSIERS_MOTIFS = ("scripts/controle", ".claude/hooks",` | `DOSSIERS_MOTIFS = ("scripts/controle",` | `test_motifs_arbre` : tué | tué |
| MA-8 | `avant_acte.py` | `if not x.endswith(".py"):` | `if False:` | `test_motifs_arbre` : tué | tué |
| MA-9 | `avant_acte.py` | `motifs(None, fautes, liste)` | `motifs(None, fautes, [])` | `test_motifs_arbre` : tué | tué |
| MA-10 | `avant_acte.py` | `non_lus += [f"{rel}:{n}" for n, _f, m in appels if m is None]` | `non_lus += []` | `test_motifs_arbre` : tué | tué |
| MA-11 | `avant_acte.py` | `f.endswith((".py", ".yml", ".yaml"))` | `f.endswith((".py",))` | `test_motifs_arbre` : tué | tué |
| MA-12 | `avant_acte.py` | `chr(10).join(lignes[n - 1:fin])` | `lignes[n - 1]` | `test_motifs_arbre` : tué | tué |
| MA-14 | `garde_commun.py` | `"compile": 1,` | `"compile": 2,` | `test_motifs_arbre` : tué | tué |
| MA-15 | `garde_commun.py` | `+ "(?x)" * bool(` | `+ "" * bool(` | `test_motifs_arbre` : tué | tué |
| MA-13 | `avant_acte.py` | `dossiers[:] = sorted(x for x in dossiers if x != "__pycache__" and not` | `dossiers[:] = sorted(x for x in dossiers if not` | `test_motifs_arbre` : tué | tué |

- Limites : motifs des scripts shell (`grep` des `.sh`) et des workflows de `.github/` non lus ; un motif non lu
  n'est pas jugé ; parcours du système de fichiers (fichiers non suivis compris), non de `git ls-files` ; le garde
  `.jsonl` et les interdits du parcours ne sont pas couverts par le cas.
- Phrase de fermeture proposée (pour l'annexe B) : SHOGEN-MOTIFS-ARBRE-REDOS-1 fermé : `avant_acte.py motifs --arbre` juge les motifs
  de l'arbre (GF3C-2), cas `test_motifs_arbre`, mutants MA-1 à MA-15 tués ; passage réel : un suspect, le motif
  `ANCIEN` de `tests/test_garde_codeql.py:23`, item formé.

## GF3C-3, GF3C-4, GF3C-5 — journal des refus (annexe B l.1864, phase 3 de SHOGEN-GARDE-FOUS-ORCH-1)

- GF3C-3, écriture : chaque refus et chaque passage du crochet `.claude/hooks/garde_faits.py` écrit une ligne au
  journal `scripts/controle/garde/refus.tsv` (`consigner`) : heure lue par `date -u`, événement
  (`PreToolUse:Bash`, `Stop`…), règle du refus (`R1` à `R11` ; `R6` et `R10` au Stop) ou `permis`, `erreur` (erreur
  interne, acte permis sans contrôle), acte abrégé à 80 caractères (`abreger` : blancs réduits, valeur d'une clé de
  secret et jeton mêlant chiffres, minuscules et majuscules masqués par `***` avant la coupe ; le texte d'un message de
  l'humain n'est jamais écrit), agent (`principal` ou identifiant du sous-agent). Écriture atomique : en-tête posé par
  `os.link` d'un fichier complet (jamais deux en-têtes, jamais un fichier à demi écrit), ligne ajoutée d'un seul
  `os.write` en `O_APPEND` ; dossier absent, erreur ou chemin en `.jsonl` : rien, jamais un refus. Jamais un
  `.jsonl`. La règle R6 n'est pas touchée : `stop()` est inchangé, sa sortie 2 est consignée `R6` par `main`.
- Choix pour le journal du dépôt : `.gitignore` de son contenu (`scripts/controle/garde/.gitignore` : `refus.tsv`
  et ses fichiers temporaires), non l'en-tête seul versionné, qui rendrait l'arbre sale à chaque passage du crochet
  (refus S1 de `avant_acte.py sceller`) ; le journal n'est donc jamais au commit. Écrit au README. Les cas posent
  `SHOGEN_GARDE_REFUS=/dev/null` (`tests/__init__.py`, et `.claude/hooks/tests/test_garde_faits.py`) : aucun cas
  n'écrit au journal du dépôt (vérifié : dossier `garde/` de la copie inchangé après chaque suite).
- GF3C-4, relevé : au premier message d'une session (aucun autre message de l'humain au journal de la session), le
  crochet UserPromptSubmit affiche, après le relevé E26 des noms propres, une ligne `RELEVÉ DES REFUS` : refus depuis
  la dernière ligne `releve`, par règle (plus fréquente d'abord), et la commande du détail
  (`avant_acte.py refus --depuis <jour du dernier relevé>`), puis écrit une ligne `releve`. Journal éteint
  (`/dev/null`) : rien (le cas existant `test_e26_releve_puis_rattachement` reste vert sans retouche).
- GF3C-5, lecture : `avant_acte.py refus [--depuis AAAA-MM-JJ] [--journal F]` rend les refus par règle et par jour,
  les dix actes refusés les plus fréquents (avec leurs règles), les règles du crochet sans refus depuis trente jours
  (borne lue par `date -u`, comprise, sur tout le journal ; règles lues dans la docstring du crochet par
  `regles_du_crochet`), le nombre de passages (`permis`, `erreur` ; `releve` exclu) et les lignes illisibles ; date
  mal formée ou journal absent : sortie 3.
- Preuves rouge/vert : GF3C-3 `test_refus_journal_des_passages` et `test_refus_entete_unique` rouges contre le
  crochet d'avant (`tmp/r5-C3-rouge.txt` : `FAILED (errors=2)`) ; GF3C-4 `test_refus_releve_premier_message` rouge
  (`tmp/r5-C4-rouge.txt`) ; GF3C-5 `test_refus_lecteur` rouge (`tmp/r5-C5-rouge.txt`, sortie 3) ; tous verts après
  (`tmp/r5-C3-vert.txt`, `-C4-`, `-C5-`).
- Mutants de l'écriture (GF3C-3) :

| mutant | fichier | avant (abrégé) | après (abrégé) | test rouge sous le mutant (seul) | job `controle-unittest` |
|---|---|---|---|---|---|
| JR-1 | `garde_faits.py` | `REGLE[0] = (re.match("R[0-9]+", motif) or ["?"])[0]` | `REGLE[0] = REGLE[0]` | `test_refus_journal_des_passages` : tué | tué |
| JR-2 | `garde_faits.py` | `REGLE[0] = "R6"` | `REGLE[0] = "permis"` | `test_refus_journal_des_passages` : tué | tué |
| JR-3 | `garde_faits.py` | `REGLE[0] = "erreur"` | `REGLE[0] = "permis"` | `test_refus_journal_des_passages` : tué | tué |
| JR-4 | `garde_faits.py` | `consigner(entree, REGLE[0] if e.code == 2 else "permis", acte)` | `(retiré)` | `test_refus_journal_des_passages` : tué | tué |
| JR-5 | `garde_faits.py` | `REGLE[0] if code == 2 or REGLE[0] == "erreur" else` | `REGLE[0] if code == 2 else` | `test_refus_journal_des_passages` : tué | tué |
| JR-6 | `garde_faits.py` | `t = CLE_SECRETE.sub(lambda m: m[1] + "***", " ".join(str(texte).split(…` | `t = " ".join(str(texte).split())` | `test_refus_journal_des_passages` : tué | tué |
| JR-7 | `garde_faits.py` | `return JETON_SECRET.sub("***", t)[:80]` | `return t[:80]` | `test_refus_journal_des_passages` : tué | tué |
| JR-8 | `garde_faits.py` | `return JETON_SECRET.sub("***", t)[:80]` | `return JETON_SECRET.sub("***", t[:80])` | `test_refus_journal_des_passages` : tué | tué |
| JR-9 | `garde_faits.py` | `, " ".join(str(texte).split()))` | `, str(texte))` | `test_refus_journal_des_passages` : tué | tué |
| JR-10 | `garde_faits.py` | `os.link(tmp, chemin)` | `os.replace(tmp, chemin)` | `test_refus_journal_des_passages`, `test_refus_entete_unique` : tué | tué |
| JR-11 | `garde_faits.py` | `os.unlink(tmp)` | `pass` | `test_refus_journal_des_passages`, `test_refus_entete_unique` : tué | tué |
| JR-12 | `garde_faits.py` | `f.write(ENTETE_REFUS)` | `f.write("")` | `test_refus_journal_des_passages`, `test_refus_entete_unique` : tué | tué |
| JR-13 | `garde_faits.py` | `entree.get("agent_id") or "principal"]` | `"principal"]` | `test_refus_journal_des_passages` : tué | tué |
| JR-14 | `garde_faits.py` | `+ (":" + entree["tool_name"] if entree.get("tool_name") else "")` | `+ ""` | `test_refus_journal_des_passages` : tué | tué |
| JR-16 | `garde_faits.py` | `except FileExistsError: pass` | `except OSError: raise` | `test_refus_entete_unique` : tué | tué |
| JR-17 | `garde_faits.py` | `return os.environ.get("SHOGEN_GARDE_REFUS") or os.path.join(` | `return os.path.join(` | `test_refus_journal_des_passages`, `test_refus_entete_unique` : tué | tué |

- Mutants du relevé (GF3C-4 ; RV-2 est tué par le cas existant `test_e26_releve_puis_rattachement`, qui attend une
  sortie vide quand le journal est éteint) :

| mutant | fichier | avant (abrégé) | après (abrégé) | test rouge sous le mutant (seul) | job `controle-unittest` |
|---|---|---|---|---|---|
| RV-1 | `garde_faits.py` | `if txt and txt != prompt and MARQUE not in txt and not outils:` | `if txt and MARQUE not in txt and not outils:` | `test_refus_releve_premier_message` : tué | tué |
| RV-2 | `garde_faits.py` | `if chemin_refus() == os.devnull: return None` | `(retiré)` | `test_e26_releve_puis_rattachement` : tué | tué |
| RV-3 | `garde_faits.py` | `k = max((i for i, x in enumerate(lignes) if x[2] == "releve"), default…` | `k = -1` | `test_refus_releve_premier_message` : tué | tué |
| RV-4 | `garde_faits.py` | `key=lambda r: (-refus.count(r), int(r[1:])))` | `key=lambda r: int(r[1:]))` | `test_refus_releve_premier_message` : tué | tué |
| RV-5 | `garde_faits.py` | `refus = [x[2] for x in lignes[k + 1:] if re.fullmatch("R[0-9]+", x[2])…` | `refus = [x[2] for x in lignes[k + 1:]]` | `test_refus_releve_premier_message` : tué | tué |
| RV-6 | `garde_faits.py` | `--depuis {lignes[k][0][:10]}` | `--depuis {lignes[k][0][:7]}` | `test_refus_releve_premier_message` : tué | tué |
| RV-7 | `garde_faits.py` | `consigner(entree, "releve", f"{len(refus)} refus")` | `(retiré)` | `test_refus_releve_premier_message` : tué | tué |
| RV-8 | `garde_faits.py` | `print(texte + (chr(10) + ligne if ligne else ""))` | `print((ligne + chr(10) if ligne else "") + texte)` | `test_refus_releve_premier_message` : tué | tué |
| RV-9 | `garde_faits.py` | `print(ligne or "", end=chr(10) if ligne else "")` | `print("", end="")` | `test_refus_releve_premier_message` : tué | tué |

- Mutants de la lecture (GF3C-5) :

| mutant | fichier | avant (abrégé) | après (abrégé) | test rouge sous le mutant (seul) | job `controle-unittest` |
|---|---|---|---|---|---|
| LR-1 | `avant_acte.py` | `vus = [x for x in lignes if x[0][:10] >= (a.depuis or "")]` | `vus = lignes` | `test_refus_lecteur` : tué | tué |
| LR-2 | `avant_acte.py` | `actives = {x[2] for x in lignes if regle(x)` | `actives = {x[2] for x in vus if regle(x)` | `test_refus_lecteur` : tué | tué |
| LR-3 | `avant_acte.py` | `and x[0][:10] >= borne}` | `and x[0][:10] > borne}` | `test_refus_lecteur` : tué | tué |
| LR-4 | `avant_acte.py` | `timedelta(days=30)` | `timedelta(days=31)` | `test_refus_lecteur` : tué | tué |
| LR-5 | `avant_acte.py` | `key=lambda kv: (-kv[1], kv[0]))[:10]:` | `key=lambda kv: (-kv[1], kv[0]))[:11]:` | `test_refus_lecteur` : tué | tué |
| LR-6 | `avant_acte.py` | `key=lambda kv: (-kv[1], kv[0]))[:10]:` | `key=lambda kv: -kv[1])[:10]:` | `test_refus_lecteur` : tué | tué |
| LR-7 | `avant_acte.py` | `key=lambda kv: (kv[0][0], numero(kv[0][1])))` | `key=lambda kv: kv[0])` | `test_refus_lecteur` : tué | tué |
| LR-8 | `avant_acte.py` | `if x[3] == acte}, key=numero))` | `if x[3] == acte}))` | `test_refus_lecteur` : tué | tué |
| LR-9 | `avant_acte.py` | `passages = [x[2] for x in vus if x[2] in ("permis", "erreur")]` | `passages = [x[2] for x in vus if not regle(x)]` | `test_refus_lecteur` : tué | tué |
| LR-10 | `avant_acte.py` | `if x.strip() and not x.startswith("heure" + chr(9))]` | `if x.strip()]` | `test_refus_lecteur` : tué | tué |
| LR-11 | `avant_acte.py` | `if a.depuis and not re.fullmatch(` | `if False and not re.fullmatch(` | `test_refus_lecteur` : tué | tué |
| LR-12 | `avant_acte.py` | `muettes = [r for r in regles_du_crochet() if r not in actives]` | `muettes = [r for r in sorted({x[2] for x in lignes if regle(x)}) if r …` | `test_refus_lecteur` : tué | tué |
| LR-13 | `avant_acte.py` | `return sorted(set(re.findall("(?<![A-Za-z0-9-])(R[0-9]+)(?![0-9])", do…` | `return sorted(set(re.findall("(?<![A-Za-z0-9-])(R[0-9]+)(?![0-9])", do…` | `test_refus_lecteur` : tué | tué |
| LR-14 | `avant_acte.py` | `"refus": refus}` | `"refus": motifs_arbre}` | `test_refus_lecteur` : tué | tué |
| LR-15 | `avant_acte.py` | `regle = lambda x: re.fullmatch("R[0-9]+", x[2]) is not None` | `regle = lambda x: x[2] != "permis"` | `test_refus_lecteur` : tué | tué |

- Limites : le masque des secrets est une heuristique (un secret hexadécimal en minuscules sans nom de clé, ou coupé par
  des guillemets, passe) ; l'atomicité de l'ajout vaut sur un système de fichiers local POSIX (pas sur NFS) ; sans
  liens durs, rien n'est écrit (silence) ; le journal croît sans rotation ; le relevé lit les 6 derniers Mo
  (`QUEUE`), la lecture lit tout le journal ; un appel de `date -u` par passage du crochet ; le garde `.jsonl` de
  `consigner` n'a pas de cas (le cas créerait un `.jsonl`) ; une règle absente de la docstring du crochet n'est
  jamais listée sans refus ; le relevé n'est montré qu'au premier message d'une session neuve (une session reprise
  porte déjà des messages).
- Phrase de fermeture proposée (pour l'annexe B) : SHOGEN-GARDE-FOUS-ORCH-1, phase 3 faite : journal des refus du crochet (GF3C-3),
  relevé au premier message (GF3C-4), lecture `avant_acte.py refus` (GF3C-5) ; cas `test_refus_journal_des_passages`,
  `test_refus_entete_unique`, `test_refus_releve_premier_message`, `test_refus_lecteur` ; mutants JR, RV et LR tués ;
  item fermé.

## Campagne de mutants

- Outil : `scripts/controle/mutants.py` du dépôt (arbre relu, lancé à part de la copie mutée `verif/refonte`, état
  final), job `controle-unittest`, borne 300 s, groupes de processus neufs, relevé `ps` de fin ; `mutants.json`
  (sha256 au journal), sortie `mutants/campagne.txt`, diff et sortie de chaque mutant dans `mutants/sortie/`.
- Témoin : vivant. Mutants : 62 ; tués par la commande du job : 62 ; autres classements :
  aucun.
- Attribution par test : chaque mutant posé dans une autre copie (`verif/pas`), le test visé lancé seul
  (`outils/attribuer.py`, sortie `mutants/attribution.txt`) : les 62 rouges.
- Écarts de méthode (journal G1, `NOTES.md`) : deux campagnes arrêtées par le générateur et non comptées (code ou cas
  corrigés après une attribution qui montrait six mutants vivants, puis après un refus RX d'`avant_acte.py diff` sur
  des motifs écrits en clair dans les fixtures de `test_motifs_arbre`) ; deux heures d'ajout daté tapées en avance sur
  l'horloge, remplacées par l'heure lue avant tout diff ; un `sleep` d'avant-plan refusé par le crochet R7 du dépôt.

## Items à former (règle PAROXYSME)

| item proposé | constat | prix |
|---|---|---|
| SHOGEN-MOTIFS-ARBRE-ANCIEN-1 | `tests/test_garde_codeql.py:23` porte l'ancien `NOM_PROPRE` exponentiel (à dessein) : `motifs --arbre` sort en 1 sur l'arbre réel | `redos-admis` et sa raison sur la ligne, par un diff relu |
| SHOGEN-MOTIFS-ARBRE-NON-LUS-1 | 21 motifs de l'arbre (22 après la série) construits hors littéraux ne sont pas jugés | les réécrire en constantes lisibles, ou un juge à l'exécution |
| SHOGEN-MOTIFS-ARBRE-SHELL-1 | motifs des `.sh` et des workflows de `.github/` hors du passage | lecture des `grep`, `sed`, `rg` des scripts |
| SHOGEN-GARDE-REFUS-ROTATION-1 | journal des refus sans rotation ni borne de lecture côté `avant_acte.py refus` | rotation datée, borne |
| SHOGEN-GARDE-REFUS-MASQUE-1 | masque des secrets heuristique (hexadécimal en minuscules sans clé) | motifs de `enforcement/gate-secrets.sh` lus par le crochet |
| SHOGEN-GARDE-REFUS-BRANCHE-1 | le relevé n'est vu qu'au premier message d'une session neuve ; aucun crochet ne relit le journal d'un lot clos | relevé à la clôture d'un lot |
