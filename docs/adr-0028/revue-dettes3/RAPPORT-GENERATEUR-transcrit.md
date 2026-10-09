# Rapport du générateur de DETTES-T3, avec ses sections datées de correction (transcrit)

> Transcription par l'orchestrateur le 2026-10-09 18:07:35 UTC du fichier RAPPORT-GENERATEUR.md ; contrôle FM-1.1 des transcripts du générateur-correcteur, du réviseur et du contre-contrôleur, par le fm11.py versé et par celui de DT3-E : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Rapport du générateur G1, lot de dettes DETTES-T3

- **Modèle** : `claude-opus-5-5` (forme de la ligne contrôlée par DT3-B, ajoutée à la reprise du 2026-10-09)
- Gate 0 : modèle résolu `claude-opus-5-5` (identifiant exact donné par l'environnement), effort `max` demandé par le
  brief (non observable de l'intérieur). Heures lues par `date -u` : début 2026-10-09 15:27:02Z ; dernière lecture
  15:49:38Z.
- Base : `/home/user/shogen` HEAD `0cfbe3ecaeac81cbb35f606b3c53ef3df856dff5`, égale à la tête du brief (`0cfbe3e`).
  Dépôt réel jamais modifié (ni index, ni arbre, ni commit) : lectures seules (`git archive`, `git log`, `git show
  --numstat`, `git clone --no-checkout`).
- Copies sous `$D` : `copie/` (travail) et `base/` (tête seule), toutes deux `git archive HEAD` avec les exclusions du
  brief ; `clone/` et `clone-tete/`, clones creux (`sparse-checkout`, mêmes exclusions, 0 fichier exclu présent dans
  l'arbre) pour les gates qui exigent un dépôt (sim-bis, xtask) ; `g3/`, dépôt jetable pour la gate des secrets.
- Rattachement (G0) : `docs/adr-0028/ANNEXE-B-items.md` (sha256 `16f6e561…`), B.87 l.1390 (règle « aucune dette ») et
  l.1507 (« Restent ouverts ») ; lignes des items l.520, l.894, l.1014, l.1367 ; `docs/adr-0028/G0-lot-D8a.md` l.424 et
  CH-4 l.190-198 ; `docs/adr-0028/ANNEXE-A-lots.md` l.99. Tous [lu].

## A. SHOGEN-FM11-VERIFIABLE-1 : fermé par DT3-A (à adjuger)

Fait :
- `scripts/controle/tests/test_fm11.py` (neuf, 6 tests) et `tests/__init__.py`. `fm11.py` tourne **tel que versé**
  (sha256 `886cc676…` contrôlé par un test) dans un sous-processus `python3 -I -B`, sur des transcriptions
  synthétiques écrites par le test. Ses deux lignes de D.2 ne sont jamais lues : une doublure remplace `hashlib`,
  `subprocess` et `open` ; elle sert deux lignes synthétiques de 100 caractères sous les sha256 SHA51 et SHA14 de
  `fm11.py`, et refuse toute autre commande et toute lecture sous `/home/user/shogen/` (test de garde dédié).
- Comptes attendus écrits à la main (fragment = 40 caractères tous les 20 ; un bloc compte une fois par ligne) :
  entrée propre, 3 événements dont les 39 premiers caractères de chaque ligne : 0 fragment, aucun motif ; entrée
  chargée, 5 événements : `fragments_l51_l14` = 1 en résultats, 3 en entrées, avec les numéros d'événements et deux
  motifs ; lignes introuvables : sortie non nulle et motif « contrôle impossible ».
- `scripts/controle/SHA256SUMS` : 28 sorties de `sorties-fm11/` n'y étaient pas (43 lignes pour 68 sorties et 3
  scripts) ; 28 lignes ajoutées (sha256 des fichiers versés à `0cfbe3e`) ; le test exige la couverture de `fm11.py` et
  de chaque sortie, sans doublon, aux bons sha256. `sha256sum -c` : 71 OK.
- Câblage : job neuf `controle-unittest` dans `gates.yml` (patron du job calib-actifs, `--aucun-saut --egal
  --plancher 6`), lu par le cas neuf K-04 du runner (`CAS` 136 → 137). README de `scripts/controle` : ajout daté.
- Diff : `diffs/DT3-A.diff`, +199 −4 (`git apply --numstat`) ; `git apply --check` vert sur la tête.

Rouges avant le code :
- `test_sommes_couvrent_script_et_sorties` : FAIL, `AssertionError: Lists differ: ['sorties-fm11/adr0029-v3-redacteur.json',
  …]`, 28 éléments (`sorties/A-rouge-sommes.txt`) ; vert après les 28 lignes.
- Runner avec K-04 sans le job : `ÉCHEC K-04 …`, sortie 1, `135 ok, 2 échec` ; le second échec est R-09, par contrecoup
  (sa capture lance une copie du runner, rouge pour la même raison) ; `137 ok, 0 échec` avec le job
  (`sorties/A-rouge-K04.txt`, `A-vert-K04.txt`). Forme du rouge : contrat du runner (sortie 1), pas `AssertionError`.
- Tests du comportement de `fm11.py` : verts dès l'écriture (le script existe et n'est pas changé) ; leur rouge est
  montré par les mutants.

Mutants (`outils/mutants.py`, borne 300 s, `start_new_session`, `killpg`, relevé `ps` de fin : 0 processus restant ;
`sorties/mutants-A.json`) : 12 sur 12 tués. M-A1 à M-A8 sur `fm11.py`, jugés par la classe `Temoin` seule (la classe
`Empreintes` tuerait tout mutant du script par son sha256) : fragment de 30, rôle `tool_use`, `any` → `all`, garde
« introuvable » retirée, pas de 40, numérotation depuis 1, contenu en chaîne ignoré, compte de motif à 1 ; tous par
FAIL sans ERROR. M-A9 à M-A11 sur `SHA256SUMS` (ligne retirée, somme altérée, ligne doublée), classe `Empreintes`,
FAIL. M-A12, `--egal` retiré de la ligne du job : runner en sortie 1, `ÉCHEC K-04`.

## B. SHOGEN-R1-FORME-RESOLUE-1 (ligne « Modèle » des journaux G1/G2) : arrêté à Q-B1, aucun diff

Constat [mesuré] : aucun gabarit de journal G1/G2, aucun script ni lint ne porte ou ne contrôle une ligne « Modèle »
(lus : `.claude/agents/*.md`, `enforcement/`, `scripts/controle/`, `.github/workflows/`, `docs/adr-0028/*.md`). Sur les
52 journaux `docs/G1-*.md` et `docs/G2-*.md`, la première ligne qui porte un identifiant `claude-…` (hors
`claude-fable-5-1`) a **25 formes distinctes** (la plus fréquente, `- **Modèle** : \`…\``, dans 16) ; 51 portent
`claude-opus-5-5`, 1 `claude-sonnet-5-5` ; `docs/G1-lot-adr0025-filtre.md` l.3 porte deux identifiants
(`claude-opus-5-5`, puis « identifiant résolu … `claude-opus-5-5[1m]` »). La forme n'est donc pas établie sur pièce.

## C. SHOGEN-G2-ENREG-ROLE-1 : arrêté à Q-C1, aucun diff

Aucun gabarit de brief G2, du chemin S2 ou autre, n'est versé dans les lieux permis (`.claude/agents/`,
`docs/adr-0028/*.md` et ses sous-dossiers permis, `s2-harness/*.md`, `s2-harness/tools/README.md`). Les briefs G2
versés sont des instances par lot (S2-bis : 2 sur 10 citent `oracle_record`). L'outil est
`s2-harness/tools/oracle_record.py` (il n'y a pas de `tools/` à la racine). Son aide est lue. La forme de la commande
cp-2 (`docs/adr-0028/CP2-S2.md` l.36-37) donne la ligne proposée :
`env -u SHOGEN_S2_CAMPAGNE_CONTROL PYTHONDONTWRITEBYTECODE=1 python3 -B s2-harness/tools/oracle_record.py --role G2
--commit <sha complet relu> --auteur <identifiant résolu du réviseur> --depot <copie du réviseur> --sortie <dossier>`,
puis `--verifier <enregistrement> --role G2 --commit <sha complet> --depot <copie>`. La règle d'usage de
`s2-harness/tools/README.md` s'applique : outil lancé depuis un arbre relu. Aucun test ne lit les gabarits.

## D. SHOGEN-S2BIS-P1-ESTIMATION-1 : règle proposée par DT3-D (texte seul, à adjuger)

- Ni `docs/adr-0029/plan-s2bis/` ni `plan-s2bis-2/` ne portent de calendrier : leurs deux README, lus en entier,
  décrivent des sorties. Le calendrier du plan S2-bis se trouve dans le G0 adjugé
  `docs/adr-0029/g0-collecte/G0-COLLECTE-RECALC-DEPLOI.md`, point 4 (jalons), avec les tailles du §5 de
  `PROPOSITION.md` (l.787, P1 ≈ 1 620). Le diff ajoute à ce G0 un ajout daté (2 lignes), au point 4 : toute taille
  [inféré] entre au calendrier multipliée par 2 (borne basse) et par 3 (borne haute), le jalon se posant sur la
  borne haute ; le rapport mesuré de chaque partie close remplace ensuite ce facteur.
- Chiffres : 3 168 [mesuré] = 21 commits `1ed872c` à `19a0c7e` sous `scripts/calib-actifs`, toutes voies,
  `git show --numstat` (22 commits sous ce chemin, dont `60fad53` de DETTES-T1, exclu) ; ×2,44 à ×2,88 [calc,
  3168/1300, 3168/1100]. 998 et ≈ 560 : [lu] `docs/adr-0029/s2bis/revue-p1a/G2-P1A.md` l.83 (« 998 lignes de code et
  238 de documents ») et l.389, ×1,782 [calc]. Non recompté : la base de compte (code seul) n'est pas retrouvée. Mes
  comptes sur les 9 commits CB-0a à CB-2e : 1 660 lignes toutes voies, 1 195 sous `s2bis/`.
- `git apply --check` vert ; +2 lignes.

## Gates (tête + DT3-A + DT3-D)

| gate | copie (archive) | clone creux (dépôt) |
|---|---|---|
| runner `run-fixtures-verdict-suite-s2.py` | 137 ok, 0 échec | 137 ok, 0 échec |
| s2-harness `--egal` | conforme, Ran = 415 | conforme, Ran = 415 |
| s2bis `--plancher 341` | conforme, Ran = 341 | conforme, Ran = 341 |
| sim-bis `--plancher 268` | refus : 3 ERROR `ORACLE/extraction` (pas de dépôt git, `git archive f35a70c`/`f458980` : 128) | conforme, Ran = 268 |
| calib-actifs `--plancher 65` | conforme, Ran = 65 | conforme, Ran = 65 |
| controle-unittest (neuf) `--plancher 6` | conforme, Ran = 6 | conforme, Ran = 6 |
| g1 lint R-1 (`.`) | OK, 7 fichiers | OK, 7 fichiers |
| g5 motif R-13 sur les fichiers du lot | 0 marqueur | 0 marqueur |
| g3 secrets, mode indexé (fichiers du lot) | OK, 6 fichiers (`g3/`) | OK, 6 fichiers |
| hooks (`run-fixtures-hooks.sh`) | n/a | 54 ok, 0 échec |

Tout a tourné réseau coupé (`isole.sh`, variables de mandataire retirées, TMPDIR sous `$D/tmp`), sans
`SHOGEN_S2_CAMPAGNE_CONTROL`.

xtask `cargo xtask verify` (lignes VERDICT seules) : ROUGE global, une gate ROUGE (1 violation, 9e VERDICT), 8 VERT, sur
les quatre arbres : copie, base (tête seule), clone avec diffs, clone de la tête seule. Les lignes VERDICT sont
identiques entre la copie et la base, et entre le clone avec diffs et le clone de la tête (`cmp`). Le rouge est donc
présent à la tête sous exclusions, et les diffs ne changent aucun VERDICT. La gate n'est pas nommée (seules les lignes
VERDICT sont lues), et sa cause n'est pas établie : exclusions ou tête.

## Questions

- **Q-A1** (câblage, écart E-1) : le job neuf `controle-unittest`, lu par K-04, est-il retenu, ou faut-il un autre
  lieu ? Les jobs s2bis et sim-bis ne peuvent pas recevoir d'étape : `cable` exige trois étapes (K-02, K-03). Le job
  calib-actifs n'a pas de cas K (SHOGEN-CI-CABLAGE-CALIB-1). Le README de `scripts/controle` (l.5-6, « hors de la suite `s2-harness` » l.6) le tient hors de
  la suite s2-harness.
- **Q-B1** : quelle forme fait foi pour la ligne « Modèle » des journaux G1/G2 ? Proposition : la forme majoritaire
  (16/52), une ligne `- **Modèle** : \`<id>\`` en tête de journal. Contrôle : égalité exacte avec
  `oracle_record.auteur_admis` (liste blanche lue sur la ligne `ALLOWED=` du lint, ou `<id>[1m]`), appliqué aux
  journaux versés après la date du gabarit, les 52 journaux existants restant exemptés par une liste figée. Il faut
  aussi dire si les journaux « transcrits » de `docs/adr-0029/**/revue-*` entrent dans la portée, et quel identifiant
  vaut quand une ligne en porte deux (`G1-lot-adr0025-filtre.md` l.3).
- **Q-C1** : où vit le gabarit de brief G2 du chemin S2 ? Deux voies : (a) une consigne de plus au bloc
  « Consignes de gabarit » de `.claude/agents/shogen-worker.md` (bloc B.16), avec la ligne proposée en C ;
  (b) un gabarit versé, à créer par décision. Je n'en ai créé aucun.
- **Q-D1** : le lieu du texte. Le brief nommait `plan-s2bis/` ou `plan-s2bis-2/`, qui n'ont pas de calendrier ; j'ai
  écrit au G0 adjugé, point 4 (jalons). L'heure de l'ajout daté est la mienne et est à réécrire à l'adjudication.
  L'information de l'investisseur reste un acte de l'orchestrateur.

## Écarts

- **E-1** : A est câblé par un job neuf, pas par un job existant (voir Q-A1).
- **E-2** : 12 mutants pour A, au lieu de 3 à 8.
- **E-3** : le brief écrit `tools/oracle_record.py` ; le chemin réel est `s2-harness/tools/oracle_record.py`.
- **E-4** : en cherchant le calendrier et les gabarits, j'ai listé des noms de fichiers dans `docs/adr-0029`
  (`find . -iname '*brief*'…`), compté `oracle_record` dans les `BRIEF-G2*` de ses sous-dossiers `revue-*` et cherché
  « 998 » dans `docs/adr-0029/s2bis/revue-p1a/`. Ces lectures sont ciblées, mais vont au-delà de `plan-s2bis*/`.
  Aucun dossier interdit n'a été touché.
- **E-5** : recomptes par `git log`/`git show --numstat` sur le dépôt réel, en lecture seule. Des sujets de commits
  CB-0 à CB-2 ont été affichés : 9 sujets, tronqués à 4 mots.
- **E-6** : un dépôt jetable `$D/g3` (`git init`, `git add`, aucun commit) et les deux clones creux (`git add` dans
  `clone/`, aucun commit) ont été créés hors du dépôt réel.
- **E-7** : DT3-B et DT3-C sont vides, par Q-B1 et Q-C1. B et C n'ont donc ni rouge, ni mutant.

## Limites, items à former (PAROXYSME)

- **L-1 (SHOGEN-FM11-QUEUE-1, proposé)** : `fm11.py` l.19, `range(0, max(1,len(v)-40), 20)`, exclut la dernière
  fenêtre. Les 1 à 20 derniers caractères d'une ligne interdite de plus de 40 caractères ne sont dans aucun fragment
  ([calc], longueurs 41 à 299). Corriger change le sha256 cité : c'est une décision (version 2 du script, ou limite
  écrite au README, déjà portée par DT3-A).
- **L-2** : les 28 sommes ajoutées attestent les octets versés à `0cfbe3e`, non l'égalité avec les sorties d'origine
  (transcriptions non versées).
- **L-3** : désormais, une sortie versée à `sorties-fm11/` sans sa ligne de `SHA256SUMS` fait rougir
  `controle-unittest`. C'est un serrage voulu, à porter à la procédure de versement de l'orchestrateur.
- **L-4** : le témoin ne prouve pas que les vraies lignes de D.2 sont trouvées par leur sha256 au dépôt. Le prouver
  demanderait de les ouvrir. Seuls les contrôles de l'orchestrateur l'exercent.

## Journal de provenance (G1)

Sources [lu] : `CLAUDE.md` ; `.claude/agents/shogen-worker.md`, `shogen-orchestrator.md` ;
`docs/adr-0028/ANNEXE-B-items.md` l.515-525, 890-898, 1010-1018, 1360-1372, 1390, 1490-1518 ; `G0-lot-D8a.md`
l.190-198, 418-428 ; `ANNEXE-A-lots.md` l.99 ; `CP2-S2.md` l.32-37 ; `scripts/controle/` (README, SHA256SUMS,
`fm11.py` en entier) ; `.github/workflows/gates.yml` (en entier) ; `enforcement/verdict-suite-s2.py` (en entier) ;
`enforcement/tests/run-fixtures-verdict-suite-s2.py` l.1-76, 196-199, 436-446, 540-625, 716-736 ;
`enforcement/gate-secrets.sh` l.1-40 ; `s2-harness/tools/oracle_record.py` l.1-80, 110-135, 405-443 et `--help` ;
`s2-harness/tools/README.md` ; `scripts/calib-actifs/tests/__init__.py` l.1-30 ;
`docs/adr-0029/plan-s2bis/README.md` et `plan-s2bis-2/README.md` (entiers) ; `g0-collecte/G0-COLLECTE-RECALC-DEPLOI.md`
(entier) ; `g0-collecte/PROPOSITION.md` l.775-800 et titres ; `s2bis/revue-p1a/G2-P1A.md` l.83, 389, 589 (grep) ;
`docs/G1-*.md`, `docs/G2-*.md` : lignes à identifiant `claude-` (script de mesure de B). [abs] : gabarit de journal
G1/G2, gabarit de brief G2. Aucune pièce de D.2 ouverte, aucun `*.jsonl`.

Commandes principales et sorties (fichiers sous `$D/sorties/`) : rouges A (`A-rouge-sommes.txt`, `A-rouge-K04.txt`),
verts (`A-vert-K04.txt`, `A-job-controle.txt`) ; mutants (`mutants-A.json`) ; gates (`g-copie-*.txt`,
`g-clone-*.txt`, `hooks-clone.txt`) ; xtask (`xtask-copie.txt`, `xtask-base.txt`, `xtask-clone.txt`,
`xtask-clone-tete.txt`, lignes VERDICT seules lues). Outils : `outils/iso.sh`, `mutants.py`, `gates.sh`,
`faire_diff.sh`, `xtask*.sh`.

Chiffres recomptés : 43 lignes de sommes, 68 sorties, 28 non listées ; 71 OK après l'ajout ; 25 formes sur 52
journaux ; 3 168 (21 commits) ; 1 660 et 1 195 (9 commits CB) ; ratios 1,782, 2,437, 2,88 ; queue non couverte de 1
à 20 caractères ; +199 −4 (DT3-A), +2 (DT3-D).

## Reprise après l'adjudication (section datée du 2026-10-09 16:04:27 UTC, `date -u`)

L'adjudication `ADJUDICATION-G1.md` (15:51:56 UTC) a été lue à 15:52:23 UTC. Mêmes règles qu'au brief : copies de la
tête `0cfbe3e`, dépôt réel intact, réseau coupé, sans `SHOGEN_S2_CAMPAGNE_CONTROL`. **La série s'applique dans
l'ordre A, E, B, C, D**, vérifié sur une extraction neuve (`git apply` en série, arbre égal à `st-D/`). L'ordre est
obligé pour A → E → B → C, qui touchent les mêmes fichiers (plancher de `controle-unittest` : 6, 8, 14, 16 ;
`SHA256SUMS`, README et `test_fm11.py` pour A et E) ; D est indépendant.

| diff | lignes | contenu |
|---|---|---|
| DT3-A | +199 −4 | inchangé, sauf l'ajout daté du README : la phrase sur la queue (corrigée par E) est remplacée par L-2 (les 28 sommes attestent les octets versés à `0cfbe3e`) et L-4 (vraies lignes : la sortie « contrôle impossible » de chaque exécution réelle) |
| DT3-E | +33 −12 | `fm11.py` l.18-20 : `| {v[-40:]}`, les 40 derniers caractères toujours un fragment (ligne de moins de 40 = fragment entier) ; tests `test_fragment_en_queue` et `test_ligne_courte_fragment_entier`, quasi-fragment de 39 caractères de queue dans le cas propre ; épingle et `SHA256SUMS` au nouveau sha256 `4a0b8abcc0b249034eb2e73397334e85f35d19a957ac4f8a9ddcf3efdda958b5` ; README : ligne du tableau (ancien `886cc676…` cité) et ajout daté ; plancher 8 |
| DT3-B | +189 −1 | `enforcement/journaux-modele.py` : tout `docs/G1-*.md` ou `docs/G2-*.md` hors liste figée (52 noms et sha256, égaux aux blobs de HEAD) porte une seule ligne `- **Modèle** : \`<id>\``, fin de ligne ou espace ensuite, `<id>` admis par `auteur_admis` d'`oracle_record.py` (égalité exacte, ou suivi de `[1m]`) ; sortie 0, 1 ou 3 ; nouvelle étape du job `g1-model-pinning` (`python3 -B enforcement/journaux-modele.py .`) ; 6 tests dans la suite `controle-unittest` (plancher 14) |
| DT3-C | +38 −1 | consigne datée (15:58:07 UTC) au bloc « Consignes de gabarit » de `.claude/agents/shogen-worker.md`, avec la commande `--role G2` de l'adjudication ; test `test_fiche_worker.py` (commande une fois, à la lettre, dans le bloc ; options et rôle G2 lus dans l'aide de l'outil) ; plancher 16 |
| DT3-D | +2 | ajout daté (15:58:38 UTC) au point 4 du G0 adjugé, texte complété selon Q-D1 : règle ×2 à ×3, jalon sur la borne haute, rapport mesuré qui remplace le facteur ; fondement CALIB-ACTIFS ×2,44 à ×2,88 recompté ; compte P1 lu dans `G2-P1A.md` l.389, base non retrouvée, règle indépendante |

Rouges avant correction (AssertionError) :
- E : `test_fragment_en_queue`, `{'resultats': 0, 'entrees': 0} != {'resultats': 1, 'entrees': 1}`, et l'épingle
  (`886cc676… != 4a0b8abc…`) : 2 FAIL (`sorties/E-rouge.txt`).
- B : script absent, 13 FAIL sur les 6 tests, sous-cas compris (`sorties/B-rouge.txt`).
- C : `test_consigne_au_bloc_de_gabarit`, `0 != 1` (`sorties/C-rouge.txt`).

Mutants (borne 300 s, `start_new_session`, `killpg`, relevé `ps` de fin), tous tués par FAIL sans ERROR :
- E : 5 sur 5 (correction retirée, queue de 39, queue de 41, queue pour une seule ligne, tête au lieu de queue) ;
- B : 7 sur 7 (exemption par nom seul, test de préfixe, casse de `[1m]`, deux lignes admises, G2 non lus, texte
  collé admis, refus en sortie 0) ;
- C : 4 sur 4 (commande retirée, rôle G1, option `--auteurs`, rôle G2 retiré de l'outil).

Le relevé `ps` de la campagne E a compté un processus étranger au lot (un `mut_` de `dettes2/`). Le filtre est
resserré à `dettes3/tmp/mut_` : 0 processus du lot restant pour E, B et C (`sorties/mutants-{E,B,C}.json`).

Gates sur un clone creux de la tête avec la série A, E, B, C, D (`sorties/s-clone-*`) :

| gate | résultat |
|---|---|
| runner | 137 ok, 0 échec |
| s2-harness `--egal` | Ran = 415, conforme |
| s2bis | Ran = 341, conforme |
| sim-bis | Ran = 268, conforme |
| calib-actifs | Ran = 65, conforme |
| controle-unittest | Ran = 16, conforme |
| cas du lint (`run-fixtures-model-pinning.sh`) | 227 ok |
| lint R-1 | OK |
| journaux-modele | conforme, 52 exemptés |
| hooks | 54 ok |
| G5, motif sur les 12 fichiers du lot | 0 marqueur |
| G3 secrets, mode indexé | OK, 11 fichiers |

xtask (lignes VERDICT seules) : 8 VERT, 1 ROUGE ; lignes VERDICT identiques à celles du clone de la tête seule
(`cmp`), donc aucun changement apporté par la série.

Points à porter :
- les journaux G1 et G2 nouveaux de ce lot, versés sous `docs/G1-*.md` ou `docs/G2-*.md`, doivent porter la ligne
  `- **Modèle** : \`<id>\``, faute de quoi l'étape g1 et le cas `test_arbre_du_depot` rougissent. Ce rapport la porte
  en tête, et le contrôle l'accepte (essayé sous le nom `G1-lot-DETTES-T3.md`) ;
- un journal exempté puis retouché perd son exemption (règle de la liste figée) ;
- les cas de `journaux-modele.py` vivent dans la suite `scripts/controle`, seule suite à plancher sans gabarit de
  job qui interdise une étape ; le contrôle lui-même est dans `enforcement/`, lancé par le job g1. Si un autre lieu
  est voulu pour les cas, c'est un déplacement sans changement de code.

## Corrections de la G2 (section datée du 2026-10-09 16:32:47 UTC, `date -u`)

L'ajout daté de 16:22:00 UTC à `ADJUDICATION-G1.md` et `g2/RAPPORT-G2.md` (C-1 à C-9, N-1 à N-6) ont été lus à
16:22:20 UTC. La forme de `g2/propositions/corrections-G2.diff` a servi de donnée, relue et non recopiée telle quelle.
Les anciennes versions des diffs sont sous `travail/avant-g2/`. La série est désormais **A, E, B, C, D, F**, appliquée
par `git apply` successifs sur une extraction neuve de `0cfbe3e`, arbre égal à `nst-F/`.

| diff | lignes | changement |
|---|---|---|
| DT3-A | +199 −4 | inchangé ; l'heure de son ajout du README est posée par E, qui touche ce fichier en dernier (C-8) |
| DT3-E | +54 −17 | C-1 : `test_queue_aux_longueurs_limites`, longueurs 39, 40, 41, 59, 60 et 61, extraits recalculés à la main (fenêtres `range(0, max(1, n−40), 20)` plus la queue `[n−40, n)`) ; C-8 : heures des deux ajouts du README (16:23:29 UTC) ; C-9 : garantie de détection au README ; plancher 9 |
| DT3-B | +193 −1 | C-2 : `claude-opus-5[1m]`, `opus[1m]` et `claude-opus-5-5[1m][1m]` refusés ; mêmes octets qu'un journal exempté, sous un nom neuf, refusés ; plancher 15 |
| DT3-C | +69 −1 | C-3 : `test_commande_passe_l_analyseur`, avec l'analyseur réel (pas de `usage:`, sortie 2 sur le dépôt absent) ; C-7, décision de l'adjudication : vérifié sur le code d'`oracle_record.py` (l.253-255), `--paquet-sha256` est refusé hors du rôle `rendu`. La consigne dit donc, en une phrase : tête de la copie comme `<commit relu>`, empreinte des diffs (sha256 de leur concaténation dans l'ordre de la série) écrite au rapport G2. Le test vérifie la phrase dans le bloc et le refus réel de `--paquet-sha256` au rôle G2 ; plancher 18 |
| DT3-D | +2 | C-6 : « annexe B, B.60 ; volets B.61 et B.85 » (en-têtes vérifiés l.992 et l.1352 ; mon rapport du premier tour citait à tort B.55 pour l.1014) |
| DT3-F (neuf) | +13 −3 | C-4 : `except Exception`, sortie 3, jamais 1, avec un cas (outil vide) dans `test_racine_illisible` ; C-5 : procédure de retouche d'un journal exempté dans la docstring, cas de `G1-lot-DETTES-B2.md` et `G2-lot-DETTES-B2.md` compris (lignes de cette tête hors forme, l.6 et l.7, vérifiées) |

Rouges par AssertionError :
- E : nouveau test sur l'ancien `fm11.py`, FAIL aux longueurs 41, 59, 60 et 61 (`[1] != [0, 1]`, `[] != [0]`),
  avec `test_fragment_en_queue` (`sorties/G2-E-rouge.txt`).
- C : phrase absente de la fiche, `0 != 1` (`sorties/G2-C-rouge.txt`).
- F : `1 != 3` (`sorties/G2-F-rouge.txt`).
- Les tests ajoutés par C-2 et C-3 portent sur un code déjà juste : leur rouge est montré par N-4, N-5 et N-6.

Mutants rejoués sur l'arbre final (borne 300 s, `start_new_session`, `killpg`, relevé `ps` filtré sur `dettes3/`) :
37 sur 37 tués (`sorties/g2-mutants.txt`, `g2-mutants-{A,E,B,C,N}.json`). Détail :
- A : 12 sur 12 (M-A12 réécrit au plancher 18) ;
- E : 5 sur 5 ;
- B : 7 sur 7 ;
- C : 4 sur 4 ;
- N-1 à N-6 : 6 sur 6 ;
- M-F1 (`except` resserré) et M-F2 (erreur en sortie 1) : 2 sur 2.

Tous par FAIL sans ERROR, sauf M-A12 (runner, `ÉCHEC K-04`). Le relevé `ps` de fin compte 0 processus du lot.

Gates sur un clone creux de la tête avec la série (`sorties/f-clone-*`) :

| gate | résultat |
|---|---|
| runner | 137 ok |
| s2-harness | Ran = 415 |
| s2bis | Ran = 341 |
| sim-bis | Ran = 268 |
| calib-actifs | Ran = 65 |
| controle-unittest | Ran = 18, plancher exact |
| cas du lint | 227 ok |
| lint R-1 | OK |
| journaux-modele | conforme |
| hooks | 54 ok |
| G5, fichiers du lot | 0 marqueur |
| G3 secrets, mode indexé | OK, 11 fichiers |

xtask : lignes VERDICT identiques à celles de la tête seule (8 VERT, 1 ROUGE préexistant).

Écart : une suppression de clone scratch (`rm -rf` dans le dossier du lot) a été refusée par la garde du harnais. J'ai
cloné à côté (`clone3/`) sans rien supprimer. Les dossiers `clone/`, `clone-tete/`, `st-A/` et `nst-*/` restent sous
`$D` : ils sont à nettoyer par l'orchestrateur s'il le veut.

## Corrections du contre-contrôle (section datée du 2026-10-09 17:07:04 UTC, `date -u`)

J'ai lu à 16:58:03 UTC le dernier ajout daté de `ADJUDICATION-G1.md` (16:57:58 UTC ; C-10 à C-13) et
`g2/cc/RAPPORT-CC.md` (R-1 à R-4, CC-1 à CC-6). La forme de `g2/cc/corrections-CC.diff` m'a servi de donnée, non de
texte à recopier. Les anciennes versions sont sous `travail/avant-cc/`. La série reste A, E, B, C, D, F sur
`0cfbe3e` : `git apply` successifs sur une extraction neuve, arbre égal à l'étape F.

| diff | lignes | changement |
|---|---|---|
| DT3-A | +199 −4 | inchangé |
| DT3-E | +55 −17 | C-11 : longueur 121 dans `test_queue_aux_longueurs_limites` (fenêtres 0 à 80, queue [81, 121), extraits recalculés à la main) ; README inchangé : ses ajouts gardent 16:23:29 UTC, heure de leur dernière écriture |
| DT3-B | +193 −1 | inchangé (octets identiques) |
| DT3-C | +73 −1 | C-12 : phrase « L'enregistrement atteste alors la base et la suite lancée sur elle, non les diffs… » ; le test exige la suite DIFFS + BASE ; C-13 : ajout re-daté 16:58:59 UTC, dernière écriture |
| DT3-D | +2 | C-13 : re-daté 16:59:08 UTC (« heure lue par `date -u` à la dernière écriture du texte ») |
| DT3-F | +25 −4 | C-10 : docstring, « lui ajoute la ligne s'il n'en porte aucune (… 16 la portent déjà dans la forme …) … par un lot (texte de DT3-F) » ; décompte 16 / 34 / 2 recompté sur les 52 journaux. C-11 : trois autres identifiants de la liste blanche admis ; octets de `G1-lot-CORR.md` sous le nom exempté `G1-lot-D8a.md` refusés ; sortie 3 pour deux racines et pour un outil vide, en erreur de syntaxe ou à import manquant. Plancher inchangé : 18 |

Rouges par AssertionError :
- E : longueur 121 sur l'ancien `fm11.py`, `[0, 1] != [0, 1, 3]`, avec 41, 59, 60 et 61 (`sorties/CC-E-rouge.txt`) ;
- C : phrase absente, `0 != 1` (`sorties/CC-C-rouge.txt`).

Les cas de C-11 dans F portent sur du code déjà juste : leur rouge est donné par CC-2 à CC-5.

Mutants rejoués sur l'arbre final (borne 300 s, `start_new_session`, `killpg`, `ps` filtré sur `dettes3/`) : **42 sur
42 tués** (`sorties/cc-mutants.txt`, `cc-mutants-*.json`), relevé `ps` de fin : 0 processus du lot. Détail :
- A : 12 ;
- E : 5 ;
- B : 7 ;
- C : 4 ;
- N-1 à N-6 et M-F1, M-F2 : 8 ;
- CC-1 à CC-6 : 6. CC-1 est désormais tué par `Temoin`, sans l'épingle.

Gates sur un clone creux de la tête avec la série (`sorties/h-clone-*`) :

| gate | résultat |
|---|---|
| runner | 137 ok |
| s2-harness | Ran = 415 |
| s2bis | Ran = 341 |
| sim-bis | Ran = 268 |
| calib-actifs | Ran = 65 |
| controle-unittest | Ran = 18, plancher exact |
| cas du lint | 227 ok |
| lint R-1 | OK |
| journaux-modele | conforme |
| hooks | 54 ok |
| G5, fichiers du lot | 0 marqueur |
| G3 secrets, mode indexé | OK, 11 fichiers |

xtask : lignes VERDICT identiques à celles de la tête seule (`cmp`).

Écart : en recomptant les journaux, j'ai importé `oracle_record.py` sans `-B` dans ma copie `base/`, ce qui y a écrit un
`__pycache__`. Je l'ai vu par `diff -rq` et supprimé avant la vérification finale de la série. Le dépôt réel n'a pas été
touché.

Nettoyage fait (17:07:04 UTC) : copies de travail supprimées (`base/`, `W/`, `etapes/`, `clone4/`, `g3/`, `tmp/`,
`cible-copie/`). Restent sous `$D` : les diffs, le rapport, `SHA256SUMS`, `NOTES.md`, `sorties/`, `outils/`,
`travail/` (anciennes versions), et `g2/` (pièces du réviseur et du contre-contrôleur, que je n'ai pas touchées).
