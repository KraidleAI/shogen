# Contre-contrôle neuf de la série intégrée (R-1 à R-3) (transcrit)

> Transcription par l'orchestrateur le 2026-10-16 12:03:37 UTC du fichier garde-fous/int/cc/RAPPORT-CC.md ; contrôle FM-1.1 des transcripts (générateurs des groupes A, B, C, réviseurs G2 des trois groupes, intégrateur, contre-contrôleur) par le fm11.py versé : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte ci-dessous avec une retouche (E35) : les deux noms de marqueur de dette du compte « 0 » sont mis en code, le motif R-13 du job g5 les lisant sinon comme un marqueur nu ; sans autre retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Contre-contrôle neuf — lot INTEGRATION-P2 (GARDE-FOUS phase 2, série unique C, B, A)

Gate 0 : `claude-opus-5-5` (identifiant de l'environnement de l'agent). Rôle : contre-contrôleur neuf (ni intégrateur,
ni générateur ni réviseur des groupes A, B, C). Brief : `BRIEF-CC.md` (orchestrateur, 2026-10-16 05:51:08 UTC).
Journal G1 : `NOTES.md` (ouvert à 05:52:30 UTC, `date -u`). Dépôt lu seulement (aucune écriture git sur lui, aucun
cargo) ; tout git en écriture dans des dépôts jetables de ce dossier.

## Verdict : CONFORME-AVEC-RÉSERVES (R-1 à R-3, liste fermée)

Les 24 diffs s'appliquent dans l'ordre, chaque pas est vert à son plancher, le code est à l'octet celui des groupes
hors des zones déclarées, le point bloquant `cibles` est fermé sur le crochet réel, les décisions des adjudications
tiennent. Trois réserves, chacune un diff écrit et éprouvé dans `propose/` :

| R-n | objet | diff | épreuve |
|---|---|---|---|
| R-1 | point 4 : la table R1 à R11 de `readme/A.txt` ne nomme aucun cas ; paragraphe des cas ajouté après la table | `propose/R-1-readme-A.diff` | 23 noms contrôlés présents ; D3/D4 par groupe : sortie 0 ; presg5 : 0 fragment introuvable ; job `conforme`, `Ran = 174` |
| R-2 | relevé du registre de `readme/C.txt` (l.50-51) donné à `ccc29190` seul ; relevé à la tête lue ajouté (C-3 de la G2 de C) | `propose/R-2-readme-C.diff` | `outils/registre_tete.py` : à `9c04eec` comme à `6a9434f`, 111 répondent, 0 non, 23 hors de l'arbre, 134 rangées |
| R-3 | mutant CC-07 vivant (site d'appel de `lignes_ajoutees` dans `diff()` sans `racine`) : cas ajouté au test existant `test_l12_rien_n_est_ecrit` (TMPDIR sous un interdit) | `propose/R-3-test-l12-jetable.diff` | vert sur l'état final (3.11, 3.12, 3.13, `-X dev -W error`) ; rouge sous CC-07 (`REFUS D1`) ; `mutants.py` : témoin vivant, CC-07 tué ; job `Ran = 174` ; aucun test neuf, plancher inchangé |

R-1 et R-2 s'appliquent à `readme/A.txt` et `readme/C.txt` (`git apply` depuis `int/`, `--check` vert) ; R-3 après
INT-24 (ou dans son commit), `git apply --check` vert sur l'état final, `avant_acte.py --lecture-seule diff` : sortie 0.
Si la tête bouge encore avant la chaîne, R-2 se remesure par `outils/registre_tete.py <copie> <scripts/controle>`.

## Points du brief

1. **Application : CONFORME.** Tête lue à 05:53:14 UTC : `6a9434fb5bdd61d0eaeda48cc89eb8c05fd786e3` (plancher 126,
   `gates.yml` l.369). Chaîne émulée (`outils/chaine.sh`, `preuves/chaine.txt`) : 24 pas, `C-table.diff` avec INT-01,
   `C.txt` avec INT-07, `B.txt` avec INT-16, `A.txt` avec INT-24 (`<DATE>` par `date -u`, `<tête + n>` en nombre).
   Pas à pas (`preuves/pas_a_pas.txt`) : runner `153 ok, 0 échec` et ligne exacte du job `conforme` aux 24 pas,
   Ran = 127 … 174 (tête + n de `planchers.tsv`), aucune ligne Warning ni Exception. `gates.yml` : seule la ligne du
   plancher change ; README : l.11 à INT-01, puis ajouts en fin seulement (`preuves/touches-readme-gates.txt`). Lignes
   ajoutées : 198 au plus (INT-08) ; `TODO`/`FIXME` : 0 ; aucun diff ne touche `xtask/` ni `docs/` (`preuves/comptes.txt`).
   Tête relue à 07:11:11 UTC : `9c04eec53e60e1b3a349b1c1cba492c42cef2994` (PRODUIT-R2 : ajout daté en fin du README à
   06:58:15 UTC, `tests/test_gabarit_controle.py`, plancher toujours 126) : les 24 diffs s'y appliquent
   (`preuves/chaine2.txt`), job `conforme` à INT-07, INT-16, INT-24 (Ran = 138, 161, 174), groupes en sortie 0
   (`preuves/tete2.txt`).
2. **Fidélité : CONFORME.** `outils/fidelite.py` (`preuves/fidelite.txt`) : par pas, mêmes lignes + et − que le diff
   d'origine (A renuméroté R7 → R11), hors INT-15, 17, 20, 22, 23, zones nommées au §3 du rapport. Union naïve
   (`outils/groupes.sh` puis `outils/union.py`, fusion à trois par fichier des trois états corrigés posés seuls sur la
   tête ; `preuves/union.txt`) : les seuls écarts à l'état final sont les résolutions déclarées : `fc["ecrit"]` pour
   `cibles`, appel R11 après R4 et avant R9, renumérotation R11 (crochet, SKILL `shogen-avant-lancer`, tests), signature
   `lignes_ajoutees(depot, env=None, racine=None, plage=None)`, fins de docstring dans l'ordre C, B, A, liste E de la
   SKILL `shogen-avant-committer`, classe `Serie`. Aucune résolution non déclarée. Résolutions jugées justes ; le doublon
   `OUTILS` (l.103, A) et `RACINE` (l.123, B) du crochet, même valeur, est sans effet (observation).
3. **Point bloquant `cibles` : CONFORME.** `test_bash_juge_apres_la_serie` : OK. Crochet réel hors tests
   (`outils/crochet10.py`, `preuves/crochet10.txt`) : `git commit -q -m x` (R3), `pkill -f chaine_x.sh` (R7 E28),
   `sleep 60` (R7 E18), `C='git commit -m x'; eval "$C"` (R3), `os.system` python (R3) : refusés, code 2 ; `git
   status`, `cat x.txt`, `until test -f fin; do sleep 5; done`, `grep -c a x.txt`, `ls lot` : code 0, stderr vide.
   Témoin (même crochet, `cibles` remis) : les dix en `erreur interne (NameError …)`, acte permis.
4. **Règles R1 à R11 : CONFORME avec R-1.** Table exacte sur le code (crochets, actes, origines ; R10 :
   UserPromptSubmit et Stop, SubagentStop non jugé). Chaque règle a un cas nommé qui existe ; R4 et R6 seulement hors
   CI. Ordre d'appel : R4, R11, R9. `outils/crochet_r11_r9.py` (`preuves/crochet-r11-r9.txt`) : cas C-8 (Workflow,
   brief nommé dans `script`) refusé par R11 ; dix agents et brief refusé : R11 d'abord ; dix agents sans jeton, et fan
   out dans une phrase niée : R9 ; fan out sans négation, `FANOUT-AUTORISE`, Agent au brief conforme : permis.
5. **Décisions : CONFORME.** `preuves/decisions.txt` : règle git dans le brief même avec une fiche qui la porte
   (REFUS B4) ; `CONSIGNE_MAX = 1500` ; `while`/`until` à condition admis, `while true`, `until false`, `for` refusés,
   `while true … break` admis ; marqueur de forge à identifiant lu (CC-20 tué) ; `garde/dossiers.txt` lu, aucune liste
   codée (CC-29 tué) ; fan out sans négation (CC-19 tué) ; `heure-sans-date` refuse ; aucune option `--verif-admise`.
6. **D3/D4 : CONFORME.** Outil final, `--lecture-seule diff --rapport RAPPORT-INTEGRATEUR.md` (`preuves/d3d4.txt`) :
   groupes C, B, A en sortie 0, arbre jetable inchangé. Limite (pas isolé) : sortie 1, D3 seul, aux neuf pas INT-02,
   03, 04, 06, 15, 17, 18, 21, 22 (fonction publique nommée par l'ajout README du groupe, posé à son dernier pas) ; D4 :
   aucun refus. Limite de l'outil, item à former : D3 cherche le nom comme mot du README, `suivi` (INT-23) passe par le
   mot commun (7 lignes du README d'avant le portent).
7. **Matrice et portes : CONFORME.** `preuves/matrice.txt` : python3.11, 3.12, 3.13 sous `-X dev -W error` : rc 0,
   `Ran 174`, OK, 0 ligne Warning ni Exception ; cinq portes en sortie 0 (docs-sha256sums, journaux-modele,
   runners-epingles, workflows-yaml, lint R-1) ; cas hors CI du crochet sous un TMPDIR à segment `7ba84933` :
   `Ran 26`, OK. Empreintes et comptes de tests des trois ajouts README égaux aux fichiers de leur pas
   (`preuves/readme-verif.txt`) ; `SHA256SUMS` de `scripts/controle` : tout OK à l'état final.
8. **Mutants : CONFORME avec R-3.** `scripts/controle/mutants.py` de la tête (sha256 `68406b96…`), lancé de `tete/`, à
   part de `mutcc/copie/`, job `controle-unittest`, borne 300 s, deux lots détachés : 34 mutants à moi (`mutcc/lot1.json`,
   `lot2.json`), dont 16 sur les zones de conflit et les sites d'appel (CC-01 à CC-16 : `fc["ecrit"]` des briefs, appel
   R11 déplacé après R9, R11 limité à Agent, `racine` et `plage` de `lignes_ajoutees` et leurs sites d'appel, `motifs` et
   `suivi` au commit et au diff, `passees` au commit et au diff, `workflows` sans `racine`, message R11, `biblio` dans
   `verser`). Résultat : témoin vivant aux deux lots ; 32 tués (sortie 1), 2 vivants, 0 FATAL ; relevé `ps` de fin :
   aucun processus des 36 groupes, aux deux lots. Vivants : CC-07 (non équivalent : R-3) ; CC-22 (clause `eval` de
   `douteux` ôtée) **équivalent** : `acte_shell.analyser` relit l'argument d'`eval` et en fait des actes (`eval "$C"`
   donne l'acte de programme `$C`, déjà douteux par la première clause) ; sondes (`eval "${X}" git commit`,
   `eval "git \$(echo commit) -m x"`, citation non fermée) : même décision avec et sans la clause ; les motifs d'avant ne
   résolvent aucune variable.
9. **Écarts E-1 à E-3 de l'intégrateur : CONFORME.** `test -e` des cinq dossiers interdits dans ses quinze copies :
   aucun ; ses outils ne nomment les interdits que dans la liste d'exclusion de `copie.py`. E-2 : noms seuls, d'après
   son NOTES (non vérifiable au-delà).

## Limites et items (règle PAROXYSME)

- SHOGEN-GARDE-D3-MOT-COMMUN-1 (proposé) : D3 juge présente une fonction dont le nom est un mot du README (`suivi`).
- Observations : en-tête du crochet `Règles PreToolUse (R1 à R5, R11)` (R7 à R9 décrites plus bas) ; l.8 du crochet ne
  nomme pas UserPromptSubmit ni les outils `mcp__github__` (texte du groupe B) ; `OUTILS`/`RACINE` en double.
- Le pas isolé reste refusé D3 aux neuf pas nommés au point 6 : un `diff` de pas se juge par groupe.

## Écarts du contre-contrôle

- E-1 : un `sleep 1` d'avant-plan après un lancement détaché (forme que R7 refuse) ; sans effet.
- E-2 : un `grep` sans chemin absolu a lu `.claude/hooks/tests/test_garde_faits.py` du dépôt (le shell y démarre) au
  lieu de ma copie ; lecture seule, fichier non interdit ; refait sur la copie.
- E-3 : `outils/matrice.sh`, motif de la ligne du job trop large : sur `chaineR/`, `bash -c` a lancé les lignes de
  tous les jobs (`s2bis`, `sim-bis` démarrés), arrêtées après environ 4 min (descendants relevés par parenté et arrêtés,
  aucun processus restant de la session) ; ligne du job `controle-unittest` relancée seule : `conforme`, `Ran = 174`.
  Pendant ce temps, un processus lourd de plus que prévu.
- E-4 : les contrôles légers (crochet, union, D3/D4) ont tourné pendant le pas à pas détaché. Disque à 07:16 UTC :
  3,4 G libres (`df -h /`) ; ce dossier pèse 520 M (copies jetables), à retirer après adjudication.

## Provenance

- [lu] `BRIEF-CC.md` ; `../BRIEF.md`, `../ADJUDICATION.md`, `../RAPPORT-INTEGRATEUR.md`, `../NOTES.md`, `../ordre.txt`,
  `../planchers.tsv`, `../readme/C.txt`, `B.txt`, `A.txt`, `C-table.diff`, `../SHA256SUMS` (`sha256sum -c` : 97 OK) ;
  `p2a`, `p2b`, `p2c` : `ADJUDICATION.md`, `g2/RAPPORT-G2.md` ; `ERREURS-ORCHESTRATEUR.md` ; INT-01 à INT-04 à l'écran,
  les 24 par les outils et les zones de conflit à l'écran ; diffs d'origine des groupes (lus par les outils).
- Commandes et sorties : `NOTES.md`, `preuves/` ; outils : `outils/` ; mutants : `mutcc/`.
