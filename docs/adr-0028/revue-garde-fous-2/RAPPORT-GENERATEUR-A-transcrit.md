# Rapport du générateur du groupe A (transcrit)

> Transcription par l'orchestrateur le 2026-10-16 12:03:37 UTC du fichier garde-fous/p2a/RAPPORT-GENERATEUR.md ; contrôle FM-1.1 des transcripts (générateurs des groupes A, B, C, réviseurs G2 des trois groupes, intégrateur, contre-contrôleur) par le fm11.py versé : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Rapport du générateur G1 — GARDE-FOUS-ORCH, phase 2, groupe A (briefs et comptes)

- **Modèle** : `claude-opus-5-5` (Gate 0 : identifiant déclaré par l'environnement de l'agent).
- **Rattachement (G0)** : annexe B, B.102 (`docs/adr-0028/ANNEXE-B-items.md` l.1756-1783), items
  SHOGEN-GARDE-OUTIL-E6-E7-E12-E13-1 (l.1772) et SHOGEN-GARDE-OUTIL-E22-E23-E24-1 (l.1774) ; adjudication de la
  phase 1, Q-11 (`docs/adr-0028/revue-garde-fous/ADJUDICATION.md` l.40) et décision de l'investisseur du 2026-10-10
  (même pièce, l.47-72) ; registre des erreurs du scratchpad (E6, E7, E12, E13, E22, E23, E24).
- **Base** : travail commencé sur 84993090 ; la tête a avancé pendant le lot (chaîne DT7) ; diffs livrés recalés sur
  la tête lue à la fin (voir §1), par `outils/recaler.py` (README et plancher recalés, fichiers du lot contrôlés
  inchangés entre les deux bases). Aucune base du dépôt n'a été avancée, aucune écriture dans le dépôt.
- Journal G1 : `NOTES.md` (sources, commandes, mesures, écarts).

## 1. Diffs (série, à appliquer dans l'ordre)

Base des diffs : `7d9dabe6c28ce55a1b6fbc439b6c97e520a88813` (après GARDE-FOUS E29 et ROSTER) ; la série s'applique
aussi, telle quelle, sur `88308e540239d765bc223f0791261fcc46973e32` (DT15-a à DT15-c, tête lue à la clôture ; seul
`xtask/src/sg5.rs` y change parmi les chemins de la copie).

| diff | fichiers | lignes ajoutées / retirées | objet |
|---|---|---|---|
| P2A-1 | `scripts/controle/garde_commun.py`, `scripts/controle/avant_acte.py`, `scripts/controle/tests/test_garde_brief.py`, `scripts/controle/README.md`, `.github/workflows/gates.yml` | 198 / 4 | E6, E24 : `etat_items`, `brief` B1 et B4 ; plancher 117 → 120 |
| P2A-2 | `scripts/controle/avant_acte.py`, `scripts/controle/tests/test_garde_brief.py`, `scripts/controle/README.md`, `.github/workflows/gates.yml` | 115 / 4 | E22, E23 : `brief` B2 et B3 ; plancher 122 |
| P2A-3 | `.claude/hooks/garde_faits.py`, `.claude/skills/shogen-avant-lancer/SKILL.md`, `scripts/controle/tests/test_garde_brief.py`, `scripts/controle/README.md`, `.github/workflows/gates.yml` | 86 / 3 | branchement : crochet R7, skill shogen-avant-lancer ; plancher 123 |
| P2A-4 | `.claude/hooks/garde_faits.py`, `scripts/controle/tests/test_garde_brief.py`, `scripts/controle/README.md`, `.github/workflows/gates.yml` | 84 / 3 | E7 : R5 aux comptes des `BRIEF*.md` ; plancher 124 |
| P2A-5 | `scripts/controle/garde_commun.py`, `scripts/controle/tests/test_garde_regex.py`, `scripts/controle/README.md`, `.github/workflows/gates.yml` | 197 / 2 | E12 : `motifs_suspects` ; plancher 126 |
| P2A-6 | `scripts/controle/garde_commun.py`, `scripts/controle/avant_acte.py`, `scripts/controle/tests/test_garde_regex.py`, `scripts/controle/README.md`, `.github/workflows/gates.yml` | 162 / 12 | E12 : absorption, `motifs_ajoutes`, RX à commit, diff, pousser ; plancher 127 |
| P2A-7 | `scripts/controle/avant_acte.py`, `scripts/controle/tests/test_garde_suivi.py`, `.claude/skills/shogen-avant-committer/SKILL.md`, `scripts/controle/README.md`, `.github/workflows/gates.yml` | 125 / 5 | E13 : `diff --rapport`, D3, D4, skill shogen-avant-committer ; plancher 129 |

Chaque diff : ≤ 200 lignes ajoutées (R-25), aucun marqueur de dette nu (R-13), saut de ligne final ; série appliquée
par `git apply --check` puis `git apply` sur une copie de la base, résultat identique à l'étape finale ; suite du
job `controle-unittest` rejouée à chaque étape (ligne exacte de `gates.yml`, `--egal`), verte. Autocontrôle : chaque diff passe
`avant_acte.py diff --fichier <diff> --rapport RAPPORT-GENERATEUR.md` (outil de l'étape finale : D1 à D4, C4, C5, G5,
C7, C8, RX) dans un dépôt jetable dont la tête est la base du diff : sortie 0 pour les sept (`outils/autocontrole.txt`).
Rouge avant, vert après : les tests de chaque étape échouent sur l'étape précédente et passent sur la leur
(`outils/suites-etapes.txt`) ; `test_garde_*` sous 3.11, 3.12 et 3.13 avec `-X dev -W error` : 30 tests, aucune ligne
Warning ni Exception.

## 2. Outils, un par erreur

### E6 — item cité ouvert alors que fermé (P2A-1, branché par P2A-3)
- **Outil** : `garde_commun.etat_items` (annexe B lue par marqueurs) et `avant_acte.py brief`, B1 ; crochet
  GARDE-FAITS R7 (PreToolUse Agent, Workflow) : tout fichier `BRIEF*.md` que nomme la consigne passe `brief`.
- **Refuse** : un item `SHOGEN-…` ou `MONARK-…` fermé à l'annexe B que le brief cite sans l'écrire fermé
  (`REFUS B1 : <item> cité ouvert ; fermé à l'annexe B l.N (E6)`). Absent de l'annexe : avertissement.
- **Preuve** : cas réel, SHOGEN-E1-XTASK-REFS-1 (lignes 819-822 et 1583 de l'annexe copiées à l'octet) : rouge sur
  l'outil d'avant (`brief` absent : sortie 3 ; `etat_items` absent), vert après ; mesure sur l'annexe à 84993090 :
  502 items, 222 fermés ; SHOGEN-E1-XTASK-REFS-1 fermé (l.1583), SHOGEN-CI-RUNNERS-1 fermé (l.1564), les items de
  B.102 ouverts.
- **Limites** : une fermeture écrite sans fermé ni clos (sans objet, tranché, soldé) n'est pas vue (faux vert) ; une
  ligne de tableau dont une cellule commence par fermé ferme l'item de sa première cellule ; la consigne écrite en
  ligne, sans fichier `BRIEF*.md`, n'est pas contrôlée.
- **Phrase de fermeture** : E6 a son outil : `avant_acte.py brief` (B1, `garde_commun.etat_items`) refuse un item
  fermé de l'annexe B cité ouvert, rejoué par le crochet GARDE-FAITS R7 au lancement de tout agent dont la consigne
  nomme un `BRIEF*.md` (P2A-1, P2A-3).

### E7 — compte affirmé non vérifié (P2A-4)
- **Outil** : crochet GARDE-FAITS, R5 étendue : dans un `BRIEF*.md` écrit par Write, Edit, MultiEdit ou une
  redirection du shell, chaque compte à unité (`N tests`, fichiers, lignes, mutants, cas, commits, diffs, gardes,
  items, en chiffres ou de deux à douze en lettres ; `Ran N`) doit avoir été affiché par un outil avec la même unité.
- **Refuse** : `R5 : le compte « deux gardes » du brief n'a été affiché par aucun outil, avec son unité …` ; un
  compte précédé d'une borne (≤, au plus, moins de, chacun…) n'est pas jugé.
- **Preuve** : cas réel reproduit (« deux gardes » écrit, trois affichées) : permis par le crochet d'avant (rouge),
  refusé après ; affiché en chiffres, en lettres ou en anglais (`3 files`) : permis ; même nombre, autre unité :
  refus.
- **Limites** : un compte affiché par `echo` d'un nombre tapé passe (présence jugée, pas provenance) ; un compte
  écrit hors d'un `BRIEF*.md` n'est pas jugé par cette règle (R6 juge les nombres de trois chiffres d'un message
  final).
- **Phrase de fermeture** : E7 a son outil : la règle R5 du crochet GARDE-FAITS refuse l'écriture d'un brief dont un
  compte à unité n'a été affiché par aucun outil (P2A-4).

### E12 — regex ambiguë avant poussée (P2A-5, P2A-6)
- **Outil** : `garde_commun.motifs_suspects`, détecteur statique sur l'arbre de l'analyseur de `re` (aucune
  exécution du motif : avis c.1) ; `garde_commun.motifs_ajoutes` ; contrôle RX de `avant_acte.py` à `commit`,
  `diff` et `pousser` (plage poussée).
- **Refuse** : sous une répétition de borne haute > 10, une répétition variable en queue du corps qui peut lire un
  début du corps, ou qui peut lire tout ce qui la suit dans le corps et un début du corps (`(.*,)*`, règle
  d'absorption de P2A-6) (`quantificateurs-imbriques`), une alternative de largeur variable en queue, ou des branches
  que rien ne sépare (`alternatives-ambigues`) ; ligne qui porte `redos-admis` : admis, journalisé en contournement.
- **Preuve** : VIDE et BLOC d'avant DT5-24 (littéraux contrôlés égaux à ceux de `e7ffd12`, l.25-26) signalés ; ceux
  de DT5-24 (tête) non signalés ; ligne VIDE de DT5-7 refusée au diff, au commit et à la poussée, sa réécriture
  conforme ; mesure sur le code suivi de `scripts`, `enforcement`, `s2-harness`, `s2bis`, `.claude`, `.github`
  (275 fichiers) : 162 motifs lus par le premier extracteur, aucun motif sûr signalé ; 141 par l'extracteur final
  (concaténations non lues), 0 signalé. L'autocontrôle de la série (§1) a trouvé un défaut du détecteur (nœud `.` :
  `TypeError`, sortie 3) : corrigé dans P2A-5, cas ajoutés, mutants M59 et M60 tués.
- **Limites** : heuristique prudente (un motif sûr peut être signalé, `(?:a+b|ac)*`) ; formes polynomiales non
  jugées ; motif construit par concaténation, passé par un nom ou sur plusieurs lignes : non lu ; CodeQL reste le
  juge sur la forge.
- **Phrase de fermeture** : E12 a son outil : le contrôle RX d'`avant_acte.py` (commit, diff, pousser) refuse un motif
  ajouté à retour arrière exponentiel, cas de DT5-7 rouge et de DT5-24 vert (P2A-5, P2A-6).

### E13 — test non mutationné, README non suivi (P2A-7)
- **Outil** : `avant_acte.py diff --fichier F --rapport R`, fonction `suivi` : D3 et D4.
- **Refuse** : D3, fonction publique ajoutée à `scripts/controle/*.py` absente du README des contrôles d'après le
  diff ; D4, test ajouté (`def test_…` sous `tests/`) sans ligne du rapport qui le nomme avec un mutant tué, ou tests
  ajoutés sans `--rapport`.
- **Preuve** : forme du correctif DT5-24 reproduite (fonction sans README, test sans mutant) : conforme avant (rouge),
  refusée après ; README nommé par le même diff, mutant tué au rapport : conforme.
- **Limites** : le rapport est lu, le mutant n'est pas rejoué (la G2 le rejoue) ; une valeur de test qui ne teste
  rien dans un test tué par un autre mutant n'est pas vue (le cas exact de E13) ; un nom présent au README pour une
  autre raison passe.
- **Phrase de fermeture** : E13 a son outil le plus proche : `avant_acte.py diff --rapport` refuse une fonction
  publique ajoutée sans README et un test ajouté sans mutant tué au rapport (P2A-7) ; la valeur inerte d'un test
  reste à la G2 (limite écrite).

### E22 — constat relayé sans référence exacte (P2A-2, branché par P2A-3)
- **Outil** : `avant_acte.py brief`, B2 (et R7).
- **Refuse** : un constat relayé (sujet : le CC, la G2, le réviseur, le générateur, l'avis, un lot nommé comme
  `DB-1` ; verbe : a relevé, a trouvé, dit, signale, constate… ; ou `selon la G2`), hors citations entre guillemets
  français et hors code, sans `chemin:N`, `chemin l.N` ou `JOURNAL l.N` sur sa ligne ou la suivante.
- **Preuve** : message de reprise de DT6 reproduit (« le contre-contrôle de DB-1 a relevé un test instable ») :
  rouge avant (sous-commande sans B2), refusé après ; référence sur la ligne ou la suivante : conforme.
- **Limites** : un relais écrit sans les mots reconnus passe ; la référence est exigée par sa forme (son existence
  relève de B3 quand elle est de la forme `chemin:N`).
- **Phrase de fermeture** : E22 a son outil : `avant_acte.py brief` (B2) refuse un constat relayé sans fichier ni
  ligne, rejoué par le crochet GARDE-FAITS R7 (P2A-2, P2A-3).

### E23 — faisabilité d'un acte non vérifiée (P2A-2, branché par P2A-3)
- **Outil** : `avant_acte.py brief`, B3 (et R7).
- **Refuse** : `chemin:N` dont le fichier manque ou dont la ligne sort du fichier ; chemin entre accents graves de
  base connue (absolu, ou premier composant présent à la racine du dépôt) absent, sauf sur une ligne qui dit le
  produire ; sha court (hors sha256) qui n'est pas un commit ; sous-commande `avant_acte.py` inconnue ; un interdit
  n'est jamais lu ni nommé.
- **Preuve** : outil nommé absent (`scripts/copier_drive.py`, forme de la copie au Drive de Q-A), ligne hors du
  fichier, commit inconnu, sous-commande inconnue : rouges avant, refusés après ; mesure sur six briefs réels du lot
  (avec la fiche `shogen-worker`) : un refus, `docs/RENVOIS-LIGNES.tsv` nommé par le brief du groupe C, absent de la
  tête mesurée (versé depuis par DT15-b).
- **Limites** : la capacité d'un outil de session (connecteur Drive, mandataire, contenu en ligne seulement) n'est
  pas vue : le cas exact de E23 (Drive à contenu en ligne seulement) reste hors de l'outil ; un chemin relatif à un
  dossier inconnu n'est pas jugé.
- **Phrase de fermeture** : E23 a son outil le plus proche : `avant_acte.py brief` (B3) refuse un fichier, une ligne,
  un commit ou une sous-commande nommés qui n'existent pas (P2A-2, P2A-3) ; la capacité d'un connecteur reste hors de
  l'outil (limite écrite, item à former).

### E24 — volet brief : règle des commandes git à chemins explicites (P2A-1, branché par P2A-3)
- **Outil** : `avant_acte.py brief`, B4 (et R7, qui passe `--fiche <subagent_type>`).
- **Refuse** : un brief qui nomme une commande git (`git diff`, `git ls-files`, `git read-tree`…, ou « commande
  git ») sans la règle `liste explicite de chemins`, ni dans son texte ni dans la fiche nommée.
- **Preuve** : brief à copie creuse et `git diff --numstat` sans la règle : conforme avant (rouge), refusé après ; la
  règle au brief, ou à la fiche (lignes repliées) : conforme.
- **Limites** : la règle se lit comme texte, citée ou prescrite ; seule la fiche `shogen-worker` porte la règle à la
  tête lue : un brief de lecteur, d'advisor, de validateur ou d'extracteur qui nomme git doit la porter lui-même.
- **Phrase de fermeture** : E24 (volet brief) a son outil : `avant_acte.py brief` (B4) refuse un brief qui nomme git
  sans la règle des chemins explicites, ni lui ni sa fiche, rejoué par le crochet GARDE-FAITS R7 (P2A-1, P2A-3).

## 3. Mutants

Outil : `scripts/controle/mutants.py` de la tête du dépôt (classement par la commande du job `controle-unittest`,
étapes de `gates.yml` de la copie, borne 300 s, groupes de processus arrêtés, moissonneur ; relevé `ps` de fin vide
aux quatre campagnes). Campagne 1 (c1) : 53 mutants sur `mut/copie` (lignée 84993090), témoin vivant, 52 tués,
1 vivant (M24). M24 vivant : le cas « brief absolu absent » sortait en 2 par R5 (le chemin temporaire porte le segment
hexadécimal du scratchpad), non par R7 : test renforcé (motif R7 exigé dans stderr, aussi pour la fiche sans règle) ;
campagne 2 (c2, M22 à M25) : 4 tués. Campagne 3 (c3, M22 à M30, crochet fusionné avec E29, copie de l'étape finale) :
9 tués. Campagne 4 (c4, étape finale, après la correction du nœud `.` et la règle d'absorption trouvées par
l'autocontrôle) : les 18 mutants de `garde_commun.py` rejoués et M57 à M60 ajoutés, 22 tués. Aucun équivalent
déclaré. Diffs et sorties de chaque mutant : `mut*/sortie/` ; lignes JSON des runs : `mut*/campagne.txt` ; listes :
`mut*/mutants.json` (générées et contrôlées : texte avant présent une fois).

| mutant | fichier | avant → après | test visé | classement | tests en échec | reprises |
|---|---|---|---|---|---|---|
| M01 | `garde_commun.py` | if not (ferme and NIE.search( → if not (ferme and False and NIE.search( | test_e6_etat_des_items | c1 : tué (sortie 1) | test_e6_etat_des_items | c4 : tué (sortie 1) |
| M02 | `garde_commun.py` | portee = "fermé" if marque(m[0]) == "fermé" or → portee = None if marque(m[0]) == "fermé… | test_e6_etat_des_items | c1 : tué (sortie 1) | test_e6_etat_des_items | c4 : tué (sortie 1) |
| M03 | `garde_commun.py` | if any(CLOS.match(c) for c in cellules[1:]): → if any(CLOS.match(c) for c in cellules[… | test_e6_etat_des_items | c1 : tué (sortie 1) | test_e6_etat_des_items | c4 : tué (sortie 1) |
| M04 | `garde_commun.py` | etats[m[1]] = (etat, n) if etat else etats.get(m[1], ("ouve… → etats.setdefault(m[1], (etat or "ouvert… | test_e6_etat_des_items | c1 : tué (sortie 1) | test_e6_etat_des_items, test_e6_item_ferme_cite_ouvert | c4 : tué (sortie 1) |
| M05 | `garde_commun.py` | reste(?:nt)? [*]*ouverte?s? → restent [*]*ouverte?s? | test_e6_etat_des_items | c1 : tué (sortie 1) | test_e6_etat_des_items, test_e6_item_ferme_cite_ouvert, test_r7_crochet_agent | c4 : tué (sortie 1) |
| M07 | `avant_acte.py` | elif etat == "fermé" and propres[item][0] != "fermé": → elif etat == "fermé": | test_e6_item_ferme_cite_ouvert | c1 : tué (sortie 1) | test_e6_item_ferme_cite_ouvert | — |
| M08 | `avant_acte.py` | etats, propres = GC.etat_items(lire(os.path.join(a.depot, A… → propres, etats = GC.etat_items(lire(os.… | test_e6_item_ferme_cite_ouvert | c1 : tué (sortie 1) | test_e22_constat_relaye_sans_reference, test_e23_faisabilite, test_e24_git_sans_regle, test_e6_item_ferme_cite_ouvert, test_r7_crochet_agent | — |
| M09 | `avant_acte.py` | fautes.append(("avertissement", "B1" → fautes.append(("refus", "B1" | test_e6_item_ferme_cite_ouvert | c1 : tué (sortie 1) | test_e6_item_ferme_cite_ouvert | — |
| M10 | `avant_acte.py` | REGLE_GIT not in GC.plier(texte + chr(10) + fiche) → REGLE_GIT not in GC.plier(texte) | test_e24_git_sans_regle | c1 : tué (sortie 1) | test_e24_git_sans_regle, test_r7_crochet_agent | — |
| M11 | `avant_acte.py` | REGLE_GIT not in GC.plier(texte + chr(10) + fiche) → REGLE_GIT not in (texte + chr(10) + fic… | test_e24_git_sans_regle | c1 : tué (sortie 1) | test_e24_git_sans_regle, test_r7_crochet_agent | — |
| M12 | `avant_acte.py` | ¦worktree)(?![A-Za-z-])¦(?i:commandes? git)(?![A-Za-z-])") → ¦worktree)(?![A-Za-z-])") | test_e24_git_sans_regle | c1 : tué (sortie 1) | test_e24_git_sans_regle | — |
| M56 | `avant_acte.py` | if not re.fullmatch("[a-z0-9-]+", a.fiche) or not os.path.i… → if not os.path.isfile(chemin): | test_e24_git_sans_regle | c1 : tué (sortie 1) | test_e24_git_sans_regle | — |
| M13 | `avant_acte.py` | relais = RELAIS.search(GC.MASQUE.sub(lambda m: " " * len(m[… → relais = RELAIS.search(ligne) | test_e22_constat_relaye_sans_reference | c1 : tué (sortie 1) | test_e22_constat_relaye_sans_reference | — |
| M14 | `avant_acte.py` | if relais and not REF.search(ligne + " " + lignes[n]): → if relais and not REF.search(ligne): | test_e22_constat_relaye_sans_reference | c1 : tué (sortie 1) | test_e22_constat_relaye_sans_reference | — |
| M15 | `avant_acte.py` | + VERBE + "¦(?<![a-zà-ÿ])(?i:selon) " + SUJET) → + VERBE) | test_e22_constat_relaye_sans_reference | c1 : tué (sortie 1) | test_e22_constat_relaye_sans_reference | — |
| M16 | `avant_acte.py` | <= int(m[3] or m[2]) <= total: → <= int(m[3] or m[2]) < total: | test_e23_faisabilite | c1 : tué (sortie 1) | test_e23_faisabilite | — |
| M17 | `avant_acte.py` | if x.startswith("-") or PRODUIRE.search(ligne) or → if x.startswith("-") or | test_e23_faisabilite | c1 : tué (sortie 1) | test_e23_faisabilite | — |
| M18 | `avant_acte.py` | if "sha256" not in ligne[max(0, m.start() - 16):m.start()] … → if not resolu( | test_e23_faisabilite | c1 : tué (sortie 1) | test_e23_faisabilite | — |
| M19 | `avant_acte.py` | if c not in COMMANDES: → if c not in COMMANDES and False: | test_e23_faisabilite | c1 : tué (sortie 1) | test_e23_faisabilite | — |
| M20 | `avant_acte.py` | connue = os.path.isabs(chemin) or os.path.exists(os.path.jo… → connue = True | test_e23_faisabilite | c1 : tué (sortie 1) | test_e23_faisabilite | — |
| M21 | `avant_acte.py` | if any(GC.chemin_interdit(x) for x in essais): → if False: | test_e23_faisabilite | c1 : tué (sortie 1) | test_e23_faisabilite | — |
| M22 | `garde_faits.py` | controler_briefs(inp, cwd) # R7 → pass | test_r7_crochet_agent | c1 : tué (sortie 1) | test_r7_crochet_agent | c2 : tué (sortie 1); c3 : tué (sortie 1) |
| M23 | `garde_faits.py` | cmd += ["--fiche", fiche] → cmd += [] | test_r7_crochet_agent | c1 : tué (sortie 1) | test_r7_crochet_agent | c2 : tué (sortie 1); c3 : tué (sortie 1) |
| M24 | `garde_faits.py` | if os.path.isabs(nom_brief): → if False: | test_r7_crochet_agent | c1 : vivant (toutes les étapes à 0) | — | c2 : tué (sortie 1); c3 : tué (sortie 1) |
| M25 | `garde_faits.py` | if p.returncode == 1: → if p.returncode == 3: | test_r7_crochet_agent | c1 : tué (sortie 1) | test_r7_crochet_agent | c2 : tué (sortie 1); c3 : tué (sortie 1) |
| M26 | `garde_faits.py` | if (n, u) not in vus: → if n not in {x for x, _y in vus}: | test_e7_comptes_du_brief | c1 : tué (sortie 1) | test_e7_comptes_du_brief | c3 : tué (sortie 1) |
| M27 | `garde_faits.py` | if m[3] or not (bornes and BORNE.search( → if True or not (bornes and BORNE.search( | test_e7_comptes_du_brief | c1 : tué (sortie 1) | test_e7_comptes_du_brief | c3 : tué (sortie 1) |
| M28 | `garde_faits.py` | briefs_ecrits.append(c) → pass | test_e7_comptes_du_brief | c1 : tué (sortie 1) | test_e7_comptes_du_brief | c3 : tué (sortie 1) |
| M29 | `garde_faits.py` | briefs_ecrits.append(textes_ecrits[-1]) → pass | test_e7_comptes_du_brief | c1 : tué (sortie 1) | test_e7_comptes_du_brief | c3 : tué (sortie 1) |
| M30 | `garde_faits.py` | int(m[3] or NOMBRES.get(m[1].lower(), m[1])) → int(m[3] or (m[1] if m[1].isdigit() els… | test_e7_comptes_du_brief | c1 : tué (sortie 1) | test_e7_comptes_du_brief | c3 : tué (sortie 1) |
| M31 | `garde_commun.py` | if o in REPETE and av[1] > av[0]: → if o in REPETE: | test_e12_formes | c1 : tué (sortie 1) | test_e12_formes | c4 : tué (sortie 1) |
| M32 | `garde_commun.py` | codes ¦= {code for code, fin in _queues(av[2]) if fin & deb… → codes ¦= {code for code, fin in _queues… | test_e12_formes | c1 : tué (sortie 1) | test_e12_formes, test_e12_motifs_de_dt5, test_e12_rx_diff_commit_pousser | c4 : tué (sortie 1) |
| M33 | `garde_commun.py` | (av[1] == analyseur.MAXREPEAT or av[1] > 10) → (av[1] == analyseur.MAXREPEAT or av[1] … | test_e12_formes | c1 : tué (sortie 1) | test_e12_formes | c4 : tué (sortie 1) |
| M34 | `garde_commun.py` | if not _premiers([(op, av)])[1]: return out return out → return out return out | test_e12_motifs_de_dt5 | c1 : tué (sortie 1) | test_e12_motifs_de_dt5, test_e12_rx_diff_commit_pousser | c4 : tué (sortie 1) |
| M35 | `garde_commun.py` | for x, (_lo, hi) in zip(av[1], largeurs) if hi > court → for x, (_lo, hi) in zip(av[1], largeurs… | test_e12_formes | c1 : tué (sortie 1) | test_e12_formes | c4 : tué (sortie 1) |
| M36 | `garde_commun.py` | if va and vb or a and b and ouvert → if a and b and ouvert | test_e12_formes | c1 : tué (sortie 1) | test_e12_formes | c4 : tué (sortie 1) |
| M37 | `garde_commun.py` | ouvert = None in a[:len(b)] + b[:len(a)] or len(a) == len(b) → ouvert = True | test_e12_formes | c1 : tué (sortie 1) | test_e12_formes | c4 : tué (sortie 1) |
| M38 | `garde_commun.py` | s ¦= {c for c in UNIVERS if f(c) != nom.startswith("NOT_")} → s ¦= {c for c in UNIVERS if f(c)} | test_e12_motifs_de_dt5 | c1 : tué (sortie 1) | test_e12_formes, test_e12_motifs_de_dt5, test_e12_rx_diff_commit_pousser | c4 : tué (sortie 1) |
| M39 | `garde_commun.py` | except Exception: return ["motif-illisible"] → except Exception: return [] | test_e12_formes | c1 : tué (sortie 1) | test_e12_formes, test_e12_rx_diff_commit_pousser | c4 : tué (sortie 1) |
| M40 | `garde_commun.py` | (o.endswith("REPEAT") and av[0] == 0) → (o.endswith("REPEAT") and False) | test_e12_motifs_de_dt5 | c1 : tué (sortie 1) | test_e12_motifs_de_dt5, test_e12_rx_diff_commit_pousser | c4 : tué (sortie 1) |
| M41 | `garde_commun.py` | return "".join(vus) if vus and jeton.string in (",", ")") e… → return "".join(vus) if vus else None | test_e12_rx_diff_commit_pousser | c1 : tué (sortie 1) | test_e12_rx_diff_commit_pousser | c4 : tué (sortie 1) |
| M42 | `avant_acte.py` | motifs(fichiers, fautes) suivi( → suivi( | test_e12_rx_diff_commit_pousser | c1 : tué (sortie 1) | test_e12_rx_diff_commit_pousser | — |
| M43 | `avant_acte.py` | motifs(fichiers, fautes) if a.id → if a.id | test_e12_rx_diff_commit_pousser | c1 : tué (sortie 1) | test_e12_rx_diff_commit_pousser | — |
| M44 | `avant_acte.py` | plage=(base, "HEAD") → plage=None | test_e12_rx_diff_commit_pousser | c1 : tué (sortie 1) | test_e12_rx_diff_commit_pousser | — |
| M45 | `avant_acte.py` | elif codes and "redos-admis" in ligne: → elif False: | test_e12_rx_diff_commit_pousser | c1 : tué (sortie 1) | test_e12_rx_diff_commit_pousser | — |
| M46 | `garde_commun.py` | vus = [m[1] or m[2] for m in GREP.finditer(x)] + ( → vus = [] + ( | test_e12_rx_diff_commit_pousser | c1 : tué (sortie 1) | test_e12_rx_diff_commit_pousser | c4 : tué (sortie 1) |
| M47 | `garde_commun.py` | sel = list(plage) if plage else ["--cached", "HEAD"] → sel = ["--cached", "HEAD"] | test_e12_rx_diff_commit_pousser | c1 : tué (sortie 1) | test_e12_rx_diff_commit_pousser | c4 : tué (sortie 1) |
| M48 | `avant_acte.py` | if not re.search("(?<![A-Za-z0-9_])" + re.escape(nom) → if False and not re.search("(?<![A-Za-z… | test_e13_readme_des_controles | c1 : tué (sortie 1) | test_e13_readme_des_controles | — |
| M49 | `avant_acte.py` | ":scripts/controle/README.md", env=env) → "HEAD:scripts/controle/README.md", env=… | test_e13_readme_des_controles | c1 : tué (sortie 1) | test_e13_readme_des_controles | — |
| M53 | `avant_acte.py` | DEF_PUBLIQUE = re.compile("def ([a-z][A-Za-z0-9_]*)[(]") → DEF_PUBLIQUE = re.compile("def ([a-z_][… | test_e13_readme_des_controles | c1 : tué (sortie 1) | test_e13_readme_des_controles | — |
| M50 | `avant_acte.py` | if tests and not a.rapport: → if False: | test_e13_test_sans_mutant_tue | c1 : tué (sortie 1) | test_e13_test_sans_mutant_tue | — |
| M51 | `avant_acte.py` | if not any(nom in x and TUE.search(x) for x in lignes): → if not any(nom in x for x in lignes): | test_e13_test_sans_mutant_tue | c1 : tué (sortie 1) | test_e13_test_sans_mutant_tue | — |
| M52 | `avant_acte.py` | suivi(a, fichiers, env, fautes) → pass | test_e13_test_sans_mutant_tue | c1 : tué (sortie 1) | test_e13_readme_des_controles, test_e13_test_sans_mutant_tue | — |
| M57 | `garde_commun.py` | _tous(plat[k + 1:]) <= _tous(av[2]) and → True and | test_e12_formes | c4 : tué (sortie 1) | test_e12_formes, test_e12_motifs_de_dt5, test_e12_rx_diff_commit_pousser | — |
| M58 | `garde_commun.py` | codes ¦= {"quantificateurs-imbriques"} if _absorbe(av[2], d… → pass | test_e12_formes | c4 : tué (sortie 1) | test_e12_formes | — |
| M59 | `garde_commun.py` | return set(UNIVERS) if o == "ANY" else → return set(UNIVERS) if o == "NOT_LITERA… | test_e12_formes | c4 : tué (sortie 1) | test_e12_formes | — |
| M60 | `garde_commun.py` | for x in (_deplie(av[-1]) if str(op) == "SUBPATTERN" else [… → for x in [(op, av)] | test_e12_formes | c4 : tué (sortie 1) | test_e12_formes | — |

Tests ajoutés et mutant tué (D4) : test_e6_etat_des_items tué par M01 ; test_e6_item_ferme_cite_ouvert tué par M07 ;
test_e24_git_sans_regle tué par M12 ; test_e22_constat_relaye_sans_reference tué par M13 ; test_e23_faisabilite tué
par M16 ; test_r7_crochet_agent tué par M22 ; test_e7_comptes_du_brief tué par M26 ; test_e12_motifs_de_dt5 tué par
M34 ; test_e12_formes tué par M31 ; test_e12_rx_diff_commit_pousser tué par M41 ; test_e13_readme_des_controles tué
par M48 ; test_e13_test_sans_mutant_tue tué par M50.

## 4. Items à former, limites (règle PAROXYSME)

| item proposé | constat | déclencheur proposé |
|---|---|---|
| SHOGEN-GARDE-BRIEF-EN-LIGNE-1 | R7 ne contrôle qu'un fichier `BRIEF*.md` nommé par la consigne ; une consigne écrite en ligne échappe à B1-B4 | phase 2, avec le bloc commun GF-20 |
| SHOGEN-GARDE-CAPACITE-OUTIL-1 | E23 : la capacité d'un connecteur ou du mandataire (Drive à contenu en ligne seulement, cas exact de E23) n'est pas vérifiable par `brief` | lot E26-E28 (registre des capacités, forme de `hors-distant.txt`) |
| SHOGEN-GARDE-VALEUR-INERTE-1 | E13 : une valeur de test qui ne teste rien dans un test déjà tué par un autre mutant n'est pas vue ; D4 lit le rapport sans rejouer le mutant | G2 de chaque lot (rejeu) ; outil de mutants par valeur à concevoir |
| SHOGEN-GARDE-FERMETURE-MOTS-1 | E6 : `etat_items` ne voit une fermeture que par fermé, clos, une cellule ou un en-tête ; sans objet, tranché, soldé : faux vert | prochain versement à l'annexe B (forme fixe de fermeture) |
| SHOGEN-GARDE-REGLE-GIT-FICHES-1 | E24 : seule la fiche `shogen-worker` porte la règle des chemins explicites à la tête lue ; un brief de lecteur, d'advisor, de validateur, d'extracteur, de devops ou d'orchestrateur qui nomme git est refusé par R7 s'il ne la porte pas | bloc commun GF-20 (avec C-13) |
| SHOGEN-GARDE-COMPTE-PROVENANCE-1 | E7 : un compte affiché par `echo` d'un nombre tapé passe ; le crochet juge la présence, pas la provenance | phase 3 (lecture du journal des refus) |
| SHOGEN-GARDE-REDOS-POLY-1 | E12 : formes polynomiales, motifs construits par concaténation, passés par un nom ou sur plusieurs lignes non jugés | prochain lot qui touche `garde_commun.py` |
| SHOGEN-CROCHET-TESTS-JOB-1 | `.claude/hooks/tests/test_garde_faits.py` n'est dans aucun job de `gates.yml` ; il échoue (2 cas) quand TMPDIR porte un segment hexadécimal, comme le dossier du scratchpad (R5 lit le chemin comme un identifiant) : mesuré identique sur la base et l'étape finale | lot qui touche le crochet |

Constats rendus à l'orchestrateur (hors items) :
- Le brief du groupe C (`p2c/BRIEF.md` l.9) nomme `docs/RENVOIS-LIGNES.tsv` comme registre de DETTES-T15 : absent de la
  tête mesurée (84993090, `git cat-file -e` : absent), B3 le refusait ; versé depuis par DT15-b (`413321b`) : à la tête
  de clôture, ce refus tombe. Le brief nommait un fichier à venir d'un autre lot sans le dire « à produire ».
- Les groupes B et C touchent les mêmes fichiers (`avant_acte.py`, `garde_commun.py`, `garde_faits.py`, fin du README,
  plancher) : les séries se recalent l'une sur l'autre à l'adjudication ; `outils/recaler.py` refait les étapes sur une
  base neuve (README et plancher recalés, fusion à trois de git merge-file, repli par ancres pour un conflit de
  proximité, arrêt sur un conflit vrai), comme il l'a fait ici sur E29.
- R7 lance `avant_acte.py brief`, qui écrit son journal dans `.git/shogen-garde/journal.tsv` du projet à chaque
  lancement d'agent (même contrat que les autres sous-commandes ; item existant SHOGEN-GARDE-LECTURE-SEULE-1).

## 5. Écarts

- E-1 : git en écriture dans le scratchpad seulement : dépôt jetable `tmpdir/jetable` (git init, add, commit, apply
  --index ; configuration isolée) pour lancer `avant_acte.py diff --rapport` sur la série ; rien dans le dépôt du projet.
- E-2 : listes non récursives de dossiers du scratchpad (`garde-fous/`, `gf1/`, `p2b/`, `p2c/`, `r6b/`, noms seuls) et
  lecture des briefs voisins, du script `chaine_e29.sh` et de `r6b/E29-garde.diff`, pour mesurer B1-B4 et prévoir le
  conflit sur le crochet ; aucun interdit.
- E-3 : `git ls-files -- scripts enforcement s2-harness s2bis .claude .github` (liste explicite, hors `docs/`) et
  `git show HEAD:<chemin>` pour la mesure de E12 ; `git show e7ffd12:enforcement/runners-epingles.py` pour le cas réel.
- E-4 : première attente de la campagne sur le PID de `setsid` (fausse fin, sans effet) ; un `sleep 1` d'avant-plan ;
  une commande sur un fichier inexistant (`enforcement/run-fixtures-verdict-suite-s2.py`), sans effet.
- E-5 : la campagne 1 a tourné sur la lignée 84993090 (code du lot identique hors crochet) ; mutants du crochet rejoués
  sur l'étape finale (campagne 3).
- E-6 : `diff -rq` récursifs sur mes copies (`scripts`, `.claude`, `.github`, `enforcement`), jamais sur `docs/`.
- E-7 : `find` limité aux sous-dossiers du lot (`outils`, `mut*`, copies exclues) pour écrire `SHA256SUMS`.
