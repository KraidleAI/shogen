# Rapport du générateur de DETTES-T5, avec ses sections datées de correction (transcrit)

> Transcription par l'orchestrateur le 2026-10-10 02:32:22 UTC du fichier RAPPORT-GENERATEUR.md ; contrôle FM-1.1 des transcripts du générateur-correcteur, du réviseur G2 et du contre-contrôleur, par le fm11.py versé et par celui de DT3-E : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte ci-dessous sans retouche, sauf : le chemin du scratchpad est abrégé en `<scratchpad>` ; Retouche déclarée (précédent : versement du G0 de CALIB-ACTIFS) : 2 message(s) d'outil cité(s) entre guillemets sont mis en code, sans autre changement (S-G5 lit les guillemets comme une citation bibliographique).

# Rapport du générateur G1, lot de dettes DETTES-T5 (volets codables des items « forge »)

- **Modèle** : `claude-opus-5-5`
- Gate 0 : modèle résolu `claude-opus-5-5` (identifiant exact donné par l'environnement), effort `max` demandé par le
  brief (non observable de l'intérieur). Heures lues par `date -u` : début 2026-10-09 19:55:05Z ; écriture du rapport
  20:21:00Z (fin : voir « Clôture »).
- Base : `/home/user/shogen` HEAD `6356a945c4faf667b9b4a432cd6cb9b2200432a6` (branche
  `claude/compassionate-noether-szmdyj`), celle de FERMETURES-FORGE.md ; relue à 20:20:49Z, inchangée. Dépôt réel jamais
  modifié : lectures seules (`git clone --no-hardlinks --no-checkout`, `git rev-parse`).
- Copies sous `$D/tmp` : `clone/` (travail, série appliquée) et `tete/` (6356a94 seule), clones creux
  (`sparse-checkout` non-cone : `docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`,
  `docs/adr-0028/monark-m009a/`, `docs/adr-0028/execution/` et `*.jsonl` exclus ; 58 fichiers sautés, 0 `*.jsonl`
  présent). Aucune pièce de D.2 ouverte, aucune recherche récursive (greps par fichier ou par dossier à un niveau).
- Rattachement (G0) : `docs/adr-0028/ANNEXE-B-items.md` (sha256 `377283b3…b6af`) B.87 l.1390-1396 (règle « aucune
  dette »), items l.78 (SHOGEN-CI-S2-FORGE-1), l.80 et l.822-824 (SHOGEN-CI-RUNNERS-1), l.269 et l.285
  (SHOGEN-G5-FORGE-1), l.1250 (SHOGEN-LINT-ENVIRONNEMENTS-1) ; `docs/adr-0028/G0-lot-D8a.md` l.431
  (SHOGEN-G1-FORGE-1). Tous [lu].

## Série rendue (s'applique dans cet ordre sur 6356a94 ; `git apply --check` puis application, arbre identique à la copie de travail, octet pour octet)

| diff | volet | lignes | sha256 |
|---|---|---|---|
| `diffs/DT5-1.diff` | 1, SHOGEN-CI-RUNNERS-1 : limite « par libellé, pas par digest » | +9 −0 | `1bb787b7…571a` |
| `diffs/DT5-2.diff` | 2, SHOGEN-CI-S2-FORGE-1 (d) : garde réseau de s2-harness, plancher 418 | +112 −6 | `c7526f81…51a8` |
| `diffs/DT5-3.diff` | 3, SHOGEN-G5-FORGE-1 (c) : bit d'exécution dans l'installeur | +22 −6 | `ce8bc458…85bc` |
| `diffs/DT5-4.diff` | 4, LINT-ENVIRONNEMENTS-1, CI-S2-FORGE-1 (c), G1-FORGE-1 (awk) : étape d'environnement du job g1 | +17 −3 | `dfaf596f…e59a` |
| `diffs/DT5-5.diff` | 5, commentaires périmés de `gates.yml` | +17 −12 | `3e047c0e…c4d7` |
| `diffs/DT5-1w-A.diff` | variante A de Q-1 (`windows-2025-vs2026`), après DT5-5, **exclusive de B** | +10 −4 | `3006e7b6…dfb` |
| `diffs/DT5-1w-B.diff` | variante B de Q-1 (`windows-2025`), après DT5-5, **exclusive de A** | +10 −4 | `deeeaf24…304d` |

Sommes complètes dans `SHA256SUMS`. Toutes ≤ 200 lignes ajoutées (R-25). Aucun `TODO`/`FIXME` nu (g5 vert sur la copie).

## Volet 1 : SHOGEN-CI-RUNNERS-1

Fait (DT5-1) : la limite est écrite en tête de `squelette.yml` (sous ADR-0013 point 5, là où l'épinglage des actions
est documenté) : actions par SHA de commit, images des runners hébergés par libellé, jamais par digest ; le libellé fixe
le système et la lignée d'image, pas sa version, qui se lit au journal (section « Runner Image »). Renvoi d'une phrase
en tête de `gates.yml`. Pièce : annexe B l.823 ; FAITS-FORGE l.9 pour la section « Runner Image ».

**Q-1 (libellé Windows, non choisi)** : aucune pièce lisible depuis la session n'établit que `windows-2025-vs2026` est
un libellé `runs-on` valide. FAITS-FORGE l.9 donne le **nom d'image** imprimé pour un job `windows-latest` (« Image:
windows-2025-vs2026 », version 20260925.250.1, Windows Server 2025 10.0.26100), pas la liste des libellés acceptés.
Candidats :
- A, `windows-2025-vs2026` (`DT5-1w-A.diff`) : nom de l'image qui a tourné en vert ; validité comme libellé non établie.
- B, `windows-2025` (`DT5-1w-B.diff`) : forme `windows-AAAA` des libellés ; non établi qu'il désigne la même image
  (Visual Studio 2026) plutôt qu'une variante : une image différente change la chaîne MSVC sous laquelle `squelette`,
  `compagnon` et `temoignage` ont été verts.
Ce qui tranche : la table des libellés du README de `actions/runner-images` (colonne YAML Label), lue par l'outil
GitHub, ou une poussée de la variante sur une branche jetable et la lecture de « Runner Image » (actes de
l'orchestrateur). Conséquence commune aux deux : les noms des contrôles deviennent `squelette (<libellé>)`,
`compagnon (<libellé>)` et `temoignage (<libellé>)`, à fixer **avant** de poser les contrôles requis. Chaque variante
retire aussi « sur `windows-latest` » du commentaire de `temoignage.yml` (l.37 → « sur l'image Windows »).

Test ou lint de l'épinglage : le seul contrôle existant est le gabarit des cas K-01 à K-04 du runner du vérificateur
(`runs-on: ubuntu-24.04` exact, quatre jobs unittest) ; il ne lit pas les workflows Windows. Rien à étendre sans
desserrer ni créer une gate. **Q-2** : faut-il un contrôle neuf qui refuse tout `-latest` dans `runs-on` et les matrices
des 7 workflows (lot à part : un cas dans un runner existant change son compte exigé) ?

Reste (hors code) : résidu B.47 (`3d3c42e5` dans le tag v7.0.1), ligne B l.80 périmée (« 12 définitions »).

## Volet 2 : SHOGEN-CI-S2-FORGE-1 (d)

Fait (DT5-2) :
- `s2-harness/tests/__init__.py` : garde réseau de `s2bis/tests/__init__.py`, même forme (purge de `http_proxy`,
  `https_proxy`, `all_proxy` en toute casse avant la garde ; `connect`, `connect_ex`, `sendto`, `getaddrinfo`,
  `gethostbyname`, `gethostbyname_ex`, `gethostbyaddr` hors boucle locale → `ReseauInterdit(BaseException)`,
  inscrit dans `TENTATIVES`). Le contenu existant (SHOGEN-TESTS-TMP-1, E-4) est gardé.
- `s2-harness/tests/test_garde_reseau.py`, 3 tests : sorties refusées et inscrites (8 appels, dont un sous attrape-tout,
  `gethostbyname_ex` et `gethostbyaddr` en plus du témoin s2bis), boucle locale permise (assertion, pas une exception),
  mandataires purgés vérifiés dans un **sous-processus** qui pose dix variables (majuscules, minuscules, casses mêlées)
  quel que soit l'environnement du job. Adresses RFC 5737 et domaine `.invalid`.
- `enforcement/verdict-suite-s2.py` : `PLANCHER` 415 → **418** (le job passe `--egal` : plancher exact).
- `gates.yml`, commentaire du job s2-harness-unittest (l.155-157 de la tête) : la suite pose sa garde ; le job ne coupe
  pas le réseau du runner ; limites dites.

Tests d'abord : rouge sur l'`__init__.py` de la tête (`sorties/rouge-DT5-2-final.txt`) : `FAILED (failures=2)`, deux
`AssertionError` (exceptions relevées `OSError`, `gaierror`, `herror`, `None` au lieu de `ReseauInterdit` ; dix variables
de mandataire gardées), 0 `ERROR`. Vert : 3 OK. Suite entière sous la garde : `Ran 418`, `OK (skipped=2)`, deux sauts
nommant la variable, `TENTATIVES` = 8, exactement les 8 appels du test neuf (`sorties/s2-tentatives.txt`) : aucun autre
test ne sort de la boucle locale.

Mutants (8, tous tués, `FAILED (failures=1)` sans erreur) : purge retirée ; purge sensible à la casse ; `connect` non
gardé ; `sendto` non gardé ; `getaddrinfo` non gardé ; `ReseauInterdit` dérivée d'`Exception` ; tout local ; rien local.

Écart à adjuger (**E-1**) : la ligne l.78 vise « la même garde » que `F:/tmp/shogen-lots/CI-S2/work/netguard/sitecustomize.py`
(sha256 `1f5f174f…`), pièce du poste local, illisible ici ; le brief prescrit la forme de `s2bis/tests/__init__.py`.
Limites (**L-1**) : appel direct à `_socket` ; sous-processus Python qui n'importe pas `tests` (la garde n'y est pas
posée) ; mutants éprouvés réseau coupé seulement. La fermeture de (d) exige encore un run de la forge (acte de lecture).

## Volet 3 : SHOGEN-G5-FORGE-1 (c), complété (l.285)

Fait (DT5-3) : `install-pre-commit.sh` exige `-x` en `--verifier` (refus « conforme mais non exécutable ») et après la
copie (refus « non exécutable après copie ») ; en-tête mis à jour. Cas neufs du runner des hooks :
- I-15 : hook conforme passé en 644, `--verifier` → sortie 2, dossier des hooks inchangé ;
- I-16 : `chmod` neutralisé par une souche en tête de `PATH` → l'installeur refuse après la copie, sortie 2 ;
- I-17 : hook conforme passé en 644, installeur → sortie 0, hook exécutable, mêmes octets, aucune sauvegarde.

**E-2** (cas I-17 et changement du chemin « déjà conforme », au-delà des deux cas du brief) : sans lui, l'installeur
répondait « déjà conforme ; rien écrit » sur un hook non exécutable que `--verifier` refuse désormais, et la consigne
« relancer l'installeur » tournait en rond. Le hook conforme non exécutable est recopié (mode 755) sans sauvegarde
(mêmes octets) ; aucune autre branche ne change.

Rouge (`sorties/rouge-DT5-3.txt`, installeur de la tête) : `ÉCHEC I-15`, `ÉCHEC I-16`, `ÉCHEC I-17`, 54 ok. Vert :
57 ok. Mutants (7, tous tués, runner sortie 1) : `-x` retiré en `--verifier` ; retiré après copie ; « déjà conforme » sans
`-x` ; hook conforme traité comme inconnu ; `-x` lu `-e` ; `chmod 644` ; `-x` lu `-f` après copie.

**Q-3** (limite Windows) : sous Git Bash (NTFS), `chmod 644` ne retire pas `-x` d'un fichier à `#!` et `-x` y est vrai
[inféré, non mesuré : aucun poste Windows dans la session]. I-15 à I-17 y échoueraient donc par construction, et les
contrôles neufs de l'installeur y sont vides. Choix : (a) garder (le runner des hooks est une gate Linux ; le poste
local le lance sous Linux ou WSL) ; (b) sonder le bit à l'entrée du runner et compter ces cas « sans objet » à part (un
chemin de saut, donc un mutant qui survit par construction). Je n'ai pas construit (b) : il desserre la gate.

## Volet 4 : étape d'environnement (SHOGEN-LINT-ENVIRONNEMENTS-1, SHOGEN-CI-S2-FORGE-1 (c), SHOGEN-G1-FORGE-1 (c) awk)

Fait (DT5-4) : dans `g1-model-pinning`, après le checkout, une étape `shell: bash` qui imprime `locale`,
`python3 --version`, le chemin réel d'`awk`, `awk --version` (repli `awk -W version`, stdin fermé), `cat /etc/os-release`
et `ImageOS`/`ImageVersion` (variables des images hébergées, **inférées, non lues** ; « absente » sinon). Chaque commande
est suivie de `|| true`. Commentaire du job mis à jour (numérotation des étapes, awk).

**E-3** : rien n'est ajouté à `s2-harness-unittest`. Son câblage est contrôlé exactement par le gabarit du cas K-01
(trois étapes, la troisième sans autre ligne que `python3 --version` et `unset …`) et par l'analyseur de
l'enregistreur de rôle (`v.etapes`, trois étapes) : une étape de plus ferait échouer K-01, et l'admettre desserrerait le
contrôle. Ce job imprime déjà `python3 --version` ; la version de son image se lit à la section « Runner Image » de son
journal (acte de lecture). L'étape du job g1 imprime le système de la même étiquette `ubuntu-24.04`, pas de ce job-là.

Mesure (`outils/etape_env.py`, `sorties/etape-env-DT5-4.txt`) : l'étape extraite du `gates.yml` de la copie, lancée par
`bash --noprofile --norc -eo pipefail` : sortie 0 avec les outils de l'hôte (hôte cloud : `LC_CTYPE=C.UTF-8`, reste en
POSIX, Python 3.11.15, `/usr/bin/mawk`, mawk 1.3.4 20240123 — `--version` y est accepté —, Ubuntu 24.04.4 LTS ; ce n'est
**pas** l'image de la forge) ; sortie 0 avec `locale`, `python3`, `readlink`, `awk` et `cat` remplacés par des souches
qui sortent en 7 ; chacun des 5 `|| true` retiré tour à tour : sortie 7 (5 mutants tués). Rouge : sur la tête,
`ETAPE-ABSENTE`.

Reste : lire le journal du prochain run (locale, awk, python3, système), puis l'inscrire au JOURNAL. Le volet « runner
sous Git Bash » de LINT-ENVIRONNEMENTS-1 reste un acte du mainteneur.

## Volet 5 : commentaires périmés de `gates.yml` (DT5-5)

Les lignes changées sont des retouches datées (2026-10-09, lot DETTES-T5) :
- l'en-tête (l.20-26) : la forge exécute de nouveau les jobs depuis le 2026-10-09 (GC-01 ; dépôt public, check runs des
  PR #7 à #9, de seconde main par FAITS-FORGE) ; l'état de la protection de `main` n'est pas vérifiable depuis la session ;
  l'oracle local reste rejoué ;
- « futur required check » (l.88, 122, 165) → « contrôle requis (état sur main non vérifiable depuis la session) » ;
- sim-bis (l.233-234) : « Tant que la forge ne lance pas les jobs » retiré ; la règle SHOGEN-S2BIS-G3-LIGNE-JOB-1 est
  gardée telle quelle, et la forge exécute aussi le job ;
- **E-4** : la l.46 (« aucun required check n'existe ») est passée au passé daté (« n'existait, 2026-09-30 »). Elle est
  de la même classe, mais n'était pas dans la liste du brief.

Les commentaires d'indentation 4 sont hors des lignes lues par `job()` et `etapes` : les cas K, H-20 et H-24 restent
verts.

## Gates (copie 6356a94 + DT5-1..5 contre 6356a94 seule)

Chaque étape `run:` de chaque job de `gates.yml`, telle qu'écrite dans le `gates.yml` de l'arbre (`outils/jobs.py` :
extraction par `yaml.safe_load` [outil de mesure, PyYAML 6.0.1 du système, hors dépôt], `bash --noprofile --norc -eo
pipefail`, réseau coupé par `isole.sh`, mandataires retirés, `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée). Sorties
`sorties/g-copie-*`, `sorties/g-tete-*` ; codes `sorties/g-*-codes.txt`.

| gate (étape du job) | 6356a94 + série | 6356a94 seule |
|---|---|---|
| g5 : cas du hook | 0 — 57 ok | 0 — 54 ok |
| g5 : balayage R-13 (dépôt jetable des fichiers présents) | 0 — aucun marqueur | 0 |
| g1 : environnement (neuve) | 0 | sans objet |
| g1 : cas du lint | 0 — 227 ok | 0 — 227 ok |
| g1 : lint R-1 de l'arbre | 0 | 0 |
| g1 : `journaux-modele.py` | 0 — conforme (52 exemptés) | 0 |
| g3 : cas | 0 — 147 ok | 0 — 147 ok |
| g3 : `--tree` (dépôt jetable) | 0 | 0 |
| g3 : `--history` | non lancé (E-5) | non lancé |
| cas du vérificateur (runner, 5 jobs) | 0 — 137 ok ×5 | 0 — 137 ok ×5 |
| s2-harness `--egal` | 0 — **Ran = 418**, 2 sauts nommés | 0 — Ran = 415 |
| s2bis `--plancher 341` | 0 — 341 | 0 — 341 |
| sim-bis `--plancher 279` (clone git complet) | 0 — 279 | 0 — 279 |
| calib-actifs `--plancher 65` | 0 — 65 | 0 — 65 |
| controle `--plancher 18` | 0 — 18 | 0 — 18 |
| `cargo test -p xtask` | 0 — 80 et 9 passés (+ 3 binaires à 0 test) | 0 — idem |
| `cargo xtask verify`, lignes VERDICT | 8 VERT, 1 ROUGE (1 violation), global ROUGE | **identiques** (`diff` vide) |

Le ROUGE de `cargo xtask verify` est celui de la tête seule (même ligne, même compte) ; la série n'y change rien.

Variantes A et B : `git apply --check` vert après DT5-5 ; les trois workflows se lisent par `yaml.safe_load`, matrice
`[ubuntu-24.04, <libellé>]`. Aucun job local ne lance les workflows Windows.

## Écarts

- **E-1** à **E-4** : ci-dessus (forme de la garde ; I-17 ; pas d'étape dans s2-harness ; l.46).
- **E-5** : `gate-secrets.sh --history` n'est pas lancé : sur la copie, il lirait l'historique des pièces interdites.
  `--tree` tourne sur un dépôt jetable des seuls fichiers présents. Même pratique que DETTES-T4.
- **E-6** : un premier passage des gates a été interrompu par moi, avant l'amendement du commentaire du job s2-harness
  (DT5-2). Il **ne compte pas** (`travail/run1-interrompu/`). En voulant l'arrêter, un `pgrep -f` a d'abord désigné mon
  propre shell (le motif figurait dans sa ligne de commande) : le signal n'a tué que lui, sans effet sur les fichiers.
- **E-7** : FAITS-FORGE.md a pour sha256 `90a40fc1…d786` ; FERMETURES-FORGE cite `fc97a06d…35ce`. Écart expliqué par
  l'ajout de l'orchestrateur daté vers 19:58 UTC (section « Ajout »), postérieur à la vérification.
- **E-8** : dans les clones, `main` est `afc7756` (ancienne) ; la base employée est `6356a94` (tête du dépôt), désignée
  explicitement.

## Actes extérieurs restants (hors lot, à lister)

1. Contrôles requis sur `main` : `s2-harness-unittest`, `g1-model-pinning`, `g3-secrets`, `g5-no-naked-todo`,
   `s2bis-unittest`, `sim-bis-unittest` (et, selon décision, `calib-actifs-unittest`, `controle-unittest`, les jobs
   Windows sous leur nom définitif après Q-1). L'investisseur ou le mainteneur règle, puis `gh api
   repos/KraidleAI/shogen/branches/main/protection` est lu.
2. Secret scanning et protection des poussées : lire `security_and_analysis`, puis décision de l'investisseur
   (SHOGEN-FORGE-SECRET-SCANNING-1).
3. Épreuve des formes résiduelles sur une branche jetable (SHOGEN-S2BIS-ANALYSEUR-RESIDUS-1).
4. Appartenance de `3d3c42e5` au tag v7.0.1 d'`actions/checkout` (résidu B.47) : lecture de `refs/tags/v7.0.1`.
5. SHOGEN-RUSTUP-ETAT-1 : décision (a)/(b), ajout daté à ADR-0028 §4.12 l.307, constat sur le poste local.
6. Lectures au prochain run, puis JOURNAL : sortie de l'étape d'environnement du job g1 ; « Runner Image » et
   `python3 --version` de `s2-harness-unittest` ; durées des jobs g3 et g5 sous Linux ; Q-1 tranchée.
7. Annexe B (orchestrateur) : l.80 périmée ; SHOGEN-G1-FORGE-1 absent du registre (l'inscrire ou le fermer) ; états
   de G5-FORGE-1 (c), CI-S2-FORGE-1 (c)/(d), LINT-ENVIRONNEMENTS-1 et CI-RUNNERS-1 après adjudication.
8. Relecture G2 : DT5-2 touche le chemin S2 (`enforcement/verdict-suite-s2.py`, `s2-harness/tests/`). La G2 enregistre
   donc son rôle par `oracle_record.py --role G2` (consigne DT3-C) et cite l'empreinte de la série.

## Journal de provenance (G1)

Sources :
- [lu] `scratchpad/haiku/FERMETURES-FORGE.md` (sha256 `073e9d7e…19a8`), en entier ; [lu] `FAITS-FORGE.md`
  (`90a40fc1…d786`), en entier. Les faits de forge (check runs, journaux) y sont de seconde main, attribués à
  l'orchestrateur : [2nd] pour ce rapport.
- [lu] `docs/adr-0028/ANNEXE-B-items.md` (`377283b3…b6af`) l.72, 78, 80, 269, 285, 822-824, 1250, 1388-1396 ;
  `docs/adr-0028/G0-lot-D8a.md` (`a5d70848…81e7`) l.429-433.
- [lu] à 6356a94 : `.github/workflows/gates.yml` en entier (`23862f9a…91db`) ; `compagnon.yml` l.1-110 ; `squelette.yml`
  l.1-80 ; `temoignage.yml` l.1-60 ; lignes `runs-on`/`latest`/`épingl` des 7 workflows ; `enforcement/verdict-suite-s2.py`
  en entier (`de48c6bf…4888`) ; `enforcement/tests/run-fixtures-verdict-suite-s2.py` l.540-640 (`d5cb346d…c9b7`) ;
  `enforcement/hooks/install-pre-commit.sh` en entier (`dccfbe52…6ebf`) ; `enforcement/tests/run-fixtures-hooks.sh` en
  entier (`43411afb…1d4a`) ; `s2bis/tests/__init__.py` (`66ced233…0b7b`) et `s2bis/tests/test_garde.py` (`e522329f…5ff2`) ;
  `s2-harness/tests/__init__.py` (`717c1a87…e7b3`) ; greps par fichier (`runs-on`, `415`, `gates.yml`, `__init__`) dans
  `enforcement/`, `xtask/src/`, `s2-harness/tools/`, `docs/adr-0028/sceau/*.sha256`, `biblio/INDEX.md`, `JOURNAL.md`.
- [abs] liste des libellés `runs-on` de la forge (Q-1) ; garde `sitecustomize.py` du poste local (E-1) ; comportement de
  `-x` sous Git Bash (Q-3).

Commandes (sorties sous `sorties/`) : rouges et verts cités par volet ; `outils/mutants.py` → `sorties/mutants.json`
(15/15 tués, 0 FATAL ; borne 300 s, `start_new_session` + `killpg`) ; `outils/etape_env.py` (5/5) ; `outils/jobs.py`
et `outils/tout.sh` (gates, `cargo test -p xtask`, `cargo xtask verify` : seules les lignes `test result` et `VERDICT`
sont gardées) ; `git -C /home/user/shogen rev-parse HEAD` → `6356a945…` (19:55Z, 20:20Z, et à la clôture).
Chiffres recomptés : tailles des diffs par `git apply --numstat` ; comptes de tests par les sorties des runs ci-dessus.

## Clôture

- Tête relue à 20:22:48Z (`date -u`) : `6356a945…`, inchangée. La série DT5-1..5 et chacune des variantes s'y appliquent
  (vérifié sur le clone de la tête avant suppression).
- `ps` de fin filtré sur `$D` : 0 processus. Copies, cibles cargo, dépôts jetables et sorties complètes de cargo
  supprimés (`$D/tmp` vide) ; seules les lignes `test result` et `VERDICT` sont gardées sous `sorties/`.
- Aucun commit, aucune poussée. `SHOGEN_S2_CAMPAGNE_CONTROL` n'a jamais été posée (retirée par `env -u` à chaque
  lancement). Aucun accès réseau : tout s'est lancé sous `isole.sh`, mandataires retirés.
- Questions : Q-1 (libellé Windows), Q-2 (contrôle neuf de l'épinglage des runners), Q-3 (I-15 à I-17 sous Git Bash).

## Ajout daté du 2026-10-09 21:26:12 UTC (`date -u`) : phase 2, après l'adjudication de 20:24:20 UTC (Q-1 B, Q-2, Q-3)

Base finale : HEAD **`b837efefe0a255d0aca20ae35bb05a8ab0eca405`**, relue à 21:26:04Z. La tête a avancé trois fois pendant
la phase : 6356a94 → 4a4806f (DT4-a) → cc665e3 (DT4-b à g) → b837efe (versement de DETTES-T4, docs seulement). La série
remplace celle de la phase 1, et **la table ci-dessous annule la première table « Série rendue »**. Les diffs des bases
antérieures sont gardés sous `travail/diffs-base-6356a94/` et `travail/diffs-base-4a4806f/`, la variante A sous
`travail/variante-A/`.

| diff | objet | lignes | sha256 |
|---|---|---|---|
| `diffs/DT5-0.diff` | **neuf, constat C-1** : nom d'étape de DT4-a invalide en YAML | +3 −1 | `51966bcd…7cb315e3` |
| `diffs/DT5-1.diff` | volet 1, limite « par libellé, pas par digest » | +9 −0 | `39d69cd2…0562a901` |
| `diffs/DT5-2.diff` | volet 2, garde réseau de s2-harness, plancher S2 418 | +112 −6 | `88810047…70439dd9` |
| `diffs/DT5-3.diff` | volet 3, bit d'exécution, plus la phrase de Q-3 | +25 −6 | `d94e7dd6…b7b8169a` |
| `diffs/DT5-4.diff` | volet 4, étape d'environnement du job g1 | +17 −3 | `72e01f6a…ac6ee42d` |
| `diffs/DT5-5.diff` | volet 5, commentaires périmés | +17 −12 | `919c5b1a…1fa5f1cc` |
| `diffs/DT5-6.diff` | Q-1, variante B : `windows-2025` dans les trois matrices | +10 −4 | `deeeaf24…be4c304d` |
| `diffs/DT5-7.diff` | Q-2 : contrôle `enforcement/runners-epingles.py`, tests, câblage, plancher controle 26 → 33 | +166 −1 | `40d678c6…f9bb60a2` |

Ordre d'application : DT5-0 à DT5-7, sur b837efe. Chaque diff a été appliqué par `git apply --check` puis `git apply`
sur un clone de b837efe. Hors DT5-0 et le plancher de DT5-7, les lignes `+`/`−` sont celles de la phase 1 : seules les
lignes `index` et les numéros de hunk changent.

### C-1 (constat neuf, corrigé par DT5-0) : `gates.yml` de la tête n'est pas du YAML valide

Depuis 4a4806f (DT4-a), la ligne 112 de `gates.yml` est
`      - name: SHA256SUMS de docs/ hors interdits (DT4-a, SHOGEN-DOCS-SHA256SUMS-GATE-1 ; cas : controle-unittest)`.
Un deux-points suivi d'une espace dans un scalaire simple est refusé : `yaml.safe_load` lève `mapping values are not
allowed here, line 112, column 94` à 4a4806f, à cc665e3 et à b837efe. Les six autres workflows se lisent. Ce sont
mon extraction des étapes et la lecture de la forge [inféré] qui échouent, pas les contrôles du dépôt : ceux-ci lisent
par lignes (cas K, `etapes`), et le défaut n'y paraît pas. Conséquence attendue sur la forge [inféré, non observé] :
workflow `gates` déclaré invalide, aucun de ses jobs lancé. Sans contrôle requis sur `main`, une PR resterait alors
fusionnable.

DT5-0 : « cas : » devient « cas dans », avec un commentaire daté. Le sens ne change pas, et l'étape reste à sa place
(aucun contrôle ne lit ce nom). Après DT5-0 et après toute la série, les 7 workflows se lisent (`yaml.safe_load`).

**Item à former** (PAROXYSME) : aucune gate ne vérifie que les workflows sont du YAML valide. La bibliothèque standard
n'a pas d'analyseur YAML, et en ajouter un est une dépendance (R-8). Construction possible : un lot avec vérification
de registre, ou un contrôle par lignes étroit (deux-points suivi d'une espace dans un `name:` en scalaire simple).
DT5-0 peut être commis seul, avant le reste.

### Q-1 : variante B intégrée (DT5-6)

`windows-2025` remplace `windows-latest` dans `compagnon.yml`, `squelette.yml` et `temoignage.yml`. Les trois
workflows se lisent. La variante A est retirée de `diffs/` et gardée sous `travail/variante-A/`.

### Q-2 : contrôle neuf (DT5-7)

- `enforcement/runners-epingles.py` (78 lignes, bibliothèque standard, sha256 `cf756504…091fa53a`). Il refuse toute
  valeur de clé `runs-on` ou `os` qui porte un libellé `…-latest` (suffixe compris, comme `ubuntu-latest-4core`), dans
  `.github/workflows/*.yml` et `*.yaml` (premier niveau). Formes lues : en ligne, entre guillemets (valeur et clé),
  liste ou mapping de flux, flux ouvert sur plusieurs lignes, bloc (lignes plus indentées). Les commentaires sont
  écartés hors guillemets. Sorties : 0 conforme, 1 refus (`fichier:ligne : jeton`), 3 erreur, toute exception comprise.
  Limites écrites dans le script : ancres et alias, libellé posé par une variable ou par une expression autre que la
  matrice, refus en plus possibles dans un bloc `run:` qui suit une clé lue.
- `scripts/controle/tests/test_runners_epingles.py` : 7 tests. Le premier lance le contrôle sur l'arbre du dépôt ; les
  autres travaillent sur des arbres temporaires (formes refusées avec ligne et jeton exacts, formes admises avec le
  compte de clés, erreurs en 3).
- Câblage : étape `python3 -B enforcement/runners-epingles.py .` dans `g1-model-pinning`, après l'étape
  d'environnement (loin de l'étape de DT4-a). Plancher de `controle-unittest` : 26 → **33**, exact (`--egal`).
- Rouges :
  - script absent : 7 `FAIL`, 7 `AssertionError`, 0 `ERROR` (`sorties/rouge-DT5-7-sans-script.txt`) ;
  - script présent, arbre de la tête : seul `test_arbre_du_depot_conforme` échoue, `AssertionError: 1 != 0`, avec les
    3 refus `compagnon.yml:34`, `squelette.yml:49` et `temoignage.yml:43 : windows-latest`
    (`sorties/rouge-DT5-7-tete.txt`, `sorties/controle-runners-sur-tete.txt`, sortie 1).
  - Vert après DT5-6 : 7 OK ; « conforme (7 workflow(s), 22 clé(s) runs-on/os lues) ».
- Mutants (`outils/mutants_re.py`, `sorties/mutants-DT5-7.json`) : 9 tués sur 9, tous en `FAILED (failures=…)` sans
  erreur. Mutations : clé `os` non lue ; commentaires lus ; bloc non lu ; flux ouvert non suivi ; suffixe après
  `-latest` non lu ; erreur rendue en refus ; `.yaml` non lu ; clé entre guillemets non lue ; bloc lu au-delà de son
  retrait. Le brief en demandait 3 à 8 par volet ; un neuvième est gardé, parce que chaque forme lue a son mutant.

### Q-3 : phrase dans l'installeur (DT5-3)

Ajoutée en tête d'`install-pre-commit.sh` : sous Git Bash, `test -x` suit l'heuristique de MSYS (fichier qui commence
par `#!`), pas le mode [inféré]. Les contrôles du bit y sont donc vides, et I-15 à I-17 sont une gate Linux. Le premier
passage de l'installeur sur le poste local (acte du mainteneur) le confirmera. Aucun saut n'a été ajouté au runner. Les
mutants de l'installeur et de la garde ont été rejoués sur la version finale (sha256 de l'installeur `d21b7109…`, de la
garde `42cb178b…`) : 15 tués sur 15 (`sorties/mutants.json`). Les sorties de la phase 1 sont sous
`travail/run-6356a94-phase2/`.

### Gates de la phase 2

Le passage complet a tourné sur **cc665e3** : chaque étape `run:` des jobs, d'après le `gates.yml` de l'arbre,
`outils/jobs.py`, sorties `sorties/g-*`. La comparaison oppose cc665e3 + DT5-0..7 à cc665e3 + DT5-0. DT5-0 est
nécessaire au témoin, parce que le `gates.yml` de la tête ne se lit pas (C-1) : le passage lancé sur 4a4806f sans
lui a échoué à l'extraction, n'a aucun résultat et ne compte pas (`travail/run-4a4806f-yaml-invalide/`). Le passage
sur 4a4806f + DT5-0 est gardé sous `travail/run-4a4806f/`.

| gate | cc665e3 + DT5-0..7 | cc665e3 + DT5-0 |
|---|---|---|
| g5 : cas du hook / balayage | 0 — 57 ok / aucun marqueur | 0 — 54 ok / idem |
| g1 : environnement / **runners-epingles** / cas du lint / lint / journaux-modele / docs-sha256sums | 0 / 0, 7 workflows, 22 clés / 227 / 0 / 0 / 0, 33 SHA256SUMS | — / — / 227 / 0 / 0 / 0, 33 |
| g3 : cas / `--tree` (`--history` non lancé, E-5) | 0 — 147 / 0 | 0 — 147 / 0 |
| runner du vérificateur (5 jobs) | 137 ok ×5 | 137 ok ×5 |
| s2-harness `--egal` | 0 — Ran = 418 | 0 — Ran = 415 |
| s2bis / sim-bis / calib-actifs | 341 / 279 / 65 | 341 / 279 / 65 |
| controle `--egal` | 0 — **Ran = 33** | 0 — Ran = 26 |
| `cargo test -p xtask` | 0 — 81 et 9 passés | 0 — idem |
| `cargo xtask verify`, lignes VERDICT | 8 VERT, 1 ROUGE | identiques |

Sur **b837efe** (tête finale, docs seulement depuis cc665e3), les fichiers touchés par la série ont des blobs
identiques à cc665e3. J'y ai rejoué les gates qui lisent `docs/` (`sorties/b837efe/`) :

| gate | b837efe + série | b837efe + DT5-0 |
|---|---|---|
| `docs-sha256sums` | conforme, 34 SHA256SUMS, 295 lignes | idem |
| `journaux-modele` | conforme | conforme |
| runners-epingles | conforme (7, 22) | sans objet |
| suite controle | Ran = 33 | Ran = 26 |
| `cargo xtask verify`, lignes VERDICT | identiques (8 VERT, 1 ROUGE) | identiques |

### Écarts de la phase 2

- **E-9** : un `grep -r` limité à `enforcement/` et `scripts/controle/tests/` de ma copie creuse. Il cherchait si un
  contrôle lit le nom d'étape corrigé par DT5-0 (aucun résultat). C'est une recherche récursive, contraire au brief ;
  les dossiers interdits étaient absents de la copie.
- **E-10** : la tête a bougé trois fois. Les passages complets comptés sont : 6356a94 (phase 1), cc665e3 (phase 2) et
  le rejeu ciblé sur b837efe. Le passage sur 4a4806f sans DT5-0 ne compte pas (extraction en échec, C-1).
- **E-11** : DT5-7 porte le plancher 33 (26 + 7). Si un autre lot change le plancher de `controle-unittest` avant
  versement, la ligne est à rebaser : le hunk échouera alors, sans silence.

### Actes extérieurs (mise à jour)

- Fait par l'orchestrateur : n° 4 (v7.0.1). Pris en charge au versement : n° 6 et n° 7.
- Neuf : confirmer Q-3 sur le poste local (premier passage de l'installeur, acte du mainteneur).
- Neuf : le comportement de la forge sur le `gates.yml` invalide de b837efe, à lire au prochain run (attendu :
  workflow refusé) ; DT5-0 à commettre au plus tôt.
- Neuf : un item pour un contrôle de validité YAML des workflows (C-1).
- Rappel : la G2 de ce lot enregistre son rôle (`oracle_record.py --role G2`, consigne DT3-C) : DT5-2 touche le chemin
  S2.

### Clôture de la phase 2

Tête relue à 21:26:04Z (`b837efe…`). `ps` filtré sur `$D` : 0 processus. Copies et dépôts jetables supprimés
(`$D/tmp` vide). Aucun commit, aucune poussée, aucun accès réseau, `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée.

## Ajout daté du 2026-10-09 21:43:41 UTC (`date -u`) : phase 3, après l'adjudication de 21:28:17 UTC (C-1, C-2)

- Tête lue au début (21:28:25Z) : `b837efe…`. Tête lue à la fin (21:43:41Z) : **`c1122de73ec0e07812fef30d41ddb4269a76a1c8`**,
  le commit de DT5-0 par l'orchestrateur. Contrôle fait : son seul changement depuis b837efe est `gates.yml`, et ce
  fichier a le même blob que b837efe + mon DT5-0.
- **Série finale, à appliquer dans l'ordre sur c1122de.** Chaque diff a été vérifié par `git apply --check`, puis
  appliqué ; l'arbre obtenu est identique à la copie des gates. **Cette table annule celles des phases 1 et 2.**

| diff | objet | lignes | sha256 |
|---|---|---|---|
| `diffs/DT5-1.diff` | volet 1, limite « par libellé, pas par digest » | +9 −0 | `39d69cd2…0562a901` |
| `diffs/DT5-2.diff` | volet 2, garde réseau de s2-harness, plancher S2 418 | +112 −6 | `88810047…70439dd9` |
| `diffs/DT5-3.diff` | volet 3, bit d'exécution, phrase de Q-3 | +25 −6 | `d94e7dd6…b7b8169a` |
| `diffs/DT5-4.diff` | volet 4, étape d'environnement du job g1 | +17 −3 | `72e01f6a…ac6ee42d` |
| `diffs/DT5-5.diff` | volet 5, commentaires périmés | +17 −12 | `919c5b1a…1fa5f1cc` |
| `diffs/DT5-6.diff` | Q-1 : `windows-2025` | +10 −4 | `deeeaf24…be4c304d` |
| `diffs/DT5-7.diff` | Q-2 : `runners-epingles.py`, plancher controle 26 → 33 | +166 −1 | `40d678c6…f9bb60a2` |
| `diffs/DT5-8.diff` | **C-2 : lecture YAML des workflows** | +193 −1 | `965ed36a…624bc3bc` |

  Les lignes `+`/`−` de DT5-1 à DT5-7 sont celles de la phase 2. Le DT5-0 commis est gardé sous
  `travail/diffs-base-b837efe/`, avec la série précédente.

### C-2 : DT5-8

- **R-8 écrit avant tout emploi au dépôt** : une section neuve de `docs/R-8-outillage.md`. Elle est rédigée sur le
  modèle de la section OCR, avec les champs de `apt-cache show python3-yaml` et du fichier `copyright` :
  - version : `python3-yaml` 6.0.1-2build2, source `pyyaml` ;
  - origine : `noble/main`, `pool/main/p/pyyaml/python3-yaml_6.0.1-2build2_amd64.deb`, SHA256 de l'index `315e5950…1ec23` ;
  - priorité `important` ; licence MIT ; Ubuntu Developers, d'origine Debian Python Team ; amont
    `github.com/yaml/pyyaml`.

  Limites écrites dans cette section : pas de compte de téléchargements pour un paquet d'archive ; YAML 1.1 de PyYAML
  contre l'analyseur de la forge ; présence du paquet sur l'image non lue. La forme retenue est le paquet de la
  distribution, jamais `pip`.
- **`enforcement/workflows-yaml.py`** (65 lignes, sha256 `256060c8…6a0f366`). Il charge chaque workflow
  (`.github/workflows/*.yml` et `*.yaml`, premier niveau) avec un `SafeLoader` qui refuse toute clé répétée, à tout
  niveau.
  - Refus (sortie 1), avec fichier, ligne et colonne quand il y en a : erreur de lecture, clé répétée, document vide
    ou autre qu'un mapping, plusieurs documents, octets hors UTF-8, aucun workflow.
  - Erreur (sortie 3) : arguments, racine sans `.github/workflows`, PyYAML absent, toute autre exception.
  - Une clé non hachable donne 3, et non 1 : le job échoue fermé.
- **Cas : `enforcement/tests/run-fixtures-workflows-yaml.py`**. C'est un runner au contrat 0/1/3, avec CAS = 11 cas
  exigés, ni plus ni moins.
  - W-01 : l'arbre du dépôt.
  - W-02 : la forme exacte de DT4-a (« cas : » dans un nom d'étape), refusée à « ligne 7, colonne ».
  - W-03, W-04 : clé répétée, au niveau d'un job et d'une étape.
  - W-05 : tabulation.
  - W-06, W-07 : document vide, liste au premier niveau.
  - W-08 : deux documents.
  - W-09 : octets hors UTF-8, dans un fichier `.yaml`.
  - W-10 : sous-dossier et `.txt` non lus ; aucun workflow, refusé.
  - W-11 : erreurs en 3, dont PyYAML absent, simulé par un faux paquet `yaml` en tête de `PYTHONPATH`.
- **Pourquoi un runner et non la suite de `controle-unittest`** : ce job tourne sur l'interpréteur de l'image sans
  PyYAML garanti. Son gabarit (cas K-04) fixe trois étapes exactes, donc aucune étape d'installation n'y est possible.
  Le runner tourne donc dans le job g1, après l'installation ; « plancher exact » y prend la forme de CAS.
- **Câblage** : une étape du job `g1-model-pinning`, placée après `runners-epingles`.
  - Si `dpkg-query` ne donne pas exactement `6.0.1-2build2`, l'étape lance `sudo apt-get install … python3-yaml=6.0.1-2build2`,
    et en cas d'échec `apt-get update` puis la même installation.
  - `dpkg-query -W python3-yaml` met la version au journal.
  - Puis, par `/usr/bin/python3` (l'interpréteur du paquet) : le runner, puis le contrôle sur l'arbre.
  - Le commentaire du job sur les installations est mis à jour.
- **Crochet local** : non câblé. Le hook versionné ne porte aucune étape Python du job g1 (seulement le lint R-1 et la
  gate des secrets, en bash). Y ajouter PyYAML créerait une dépendance sur le poste local et changerait l'`ATTENDU`
  du hook : ce serait une décision à part (**Q-4**).
- **Rouges** :
  - contrôle absent : 11 `ÉCHEC` nommés sur 11 (`sorties/rouge-DT5-8.txt`) ;
  - contrôle lancé sur les workflows de b837efe : sortie 1, `gates.yml : ligne 112, colonne 94 : mapping values are
    not allowed here` (`sorties/controle-yaml-sur-tete.txt`).
  - Vert : 11 ok ; contrôle sur la série : « conforme (7 workflow(s), PyYAML 6.0.1) ».
- **Mutants** (`outils/mutants_yaml.py`, `sorties/mutants-DT5-8.json`) : 8 tués sur 8, runner en sortie 1, aucun FATAL.
  Mutations : clés répétées admises ; non-mapping admis ; hors UTF-8 rendu en erreur 3 ; `.yaml` non lu ; aucun
  workflow admis ; erreur de lecture admise ; erreur interne rendue en refus ; premier document seul lu.

### Gates de la phase 3

Comparaison de c1122de + DT5-1..8 avec c1122de seule. Les passages ont tourné sur b837efe + DT5-0 + série, et sur
b837efe + DT5-0, avant le commit ; ce sont les mêmes arbres, au blob près. Toutes les sorties valent 0, sauf
`cargo xtask verify`, à 1 des deux côtés (son ROUGE est sur la tête).

| gate | série | tête |
|---|---|---|
| g5 : hooks / balayage | 57 / vert | 54 / vert |
| g1 : env / runners-epingles / **workflows-yaml (runner 11 ok, contrôle conforme, `python3-yaml 6.0.1-2build2`)** / lint 227 / R-1 / journaux-modele / docs-sha256sums (34, 295) | 0 partout | lint, R-1, journaux, docs : 0 |
| g3 : cas 147 / `--tree` | 0 | 0 |
| runner vérificateur ×5 | 137 ok | 137 ok |
| s2-harness / s2bis / sim-bis / calib / controle | 418 / 341 / 279 / 65 / 33 | 415 / 341 / 279 / 65 / 26 |
| `cargo test -p xtask` | 0 (81 et 9) | 0 |
| `cargo xtask verify`, lignes VERDICT | 8 VERT, 1 ROUGE | identiques |

### Écarts et limites de la phase 3

- **E-12** : `yaml.safe_load` du paquet système a servi d'outil de mesure hors dépôt aux phases 1 et 2 (`outils/jobs.py`,
  contrôles de lecture), avant l'écriture du R-8. Le paquet était déjà installé dans le conteneur. L'écart est
  consigné dans la ligne R-8 elle-même.
- **E-13** : sur l'hôte cloud, `/usr/bin/python3` est un Python 3.11.15. Le paquet est construit pour 3.12
  (`Depends: python3 (>= 3.12~)`). PyYAML s'y charge sans libyaml (`__with_libyaml__ = False`). Sur l'image
  `ubuntu-24.04`, `/usr/bin/python3` est un 3.12 [inféré, non lu] : la version de Python et celle du paquet seront
  au journal du job.
- **L-5** : un fichier admis par PyYAML (YAML 1.1) peut encore être refusé par la forge. Le contrôle ferme la classe de
  DT4-a et les clés répétées, pas toutes les divergences.
- **Q-4** : faut-il câbler la lecture YAML au crochet local ? Il faudrait PyYAML sur le poste local, et un nouvel
  `ATTENDU` du hook.
- Actes extérieurs neufs : lire au premier run de la PR la sortie de `dpkg-query` et la branche prise (paquet présent
  ou installé), puis la reporter au JOURNAL.

### Clôture de la phase 3

Tête relue à 21:43:41Z : `c1122de…`. `ps` filtré sur `$D` : 0 processus. Copies et dépôts jetables supprimés
(`$D/tmp` vide). Sorties des passages antérieurs sous `travail/run-*`. Aucun commit, aucune poussée, aucun accès
réseau (`apt-get` n'a pas tourné : le paquet était présent à version exacte), `SHOGEN_S2_CAMPAGNE_CONTROL` jamais
posée. La G2 de ce lot relit DT5-0 avec la série et enregistre son rôle (consigne DT3-C).

## Ajout daté du 2026-10-09 22:52:44 UTC (`date -u`) : phase 4, corrections de la G2 (adjudication de 22:37:10 UTC, C-1 à C-10)

- Tête lue au début (22:37:16Z) et à la fin (22:52:44Z) : **`094fa5d3d5debe9dd466e37feee95200ca460dcf`** (fusion de la
  PR n° 10). `git diff c1122de 094fa5d` est vide : l'arbre est identique.
- **Série finale, à appliquer dans l'ordre DT5-1 à DT5-14 sur 094fa5d.** Je l'ai reconstruite sur un clone neuf ; l'arbre
  obtenu est identique, fichier par fichier, à celui des gates. DT5-1 à DT5-8 sont inchangés (mêmes sha256 qu'en
  phase 3).

| diff | objet | lignes | sha256 |
|---|---|---|---|
| `diffs/DT5-9.diff` | C-6 (garde de s2-harness : appels gardés nommés, `sendmsg` non gardé) | +7 −5 | `4b452944…3c969177` |
| `diffs/DT5-10.diff` | C-5 (en-tête et commentaire sim-bis de `gates.yml`) | +12 −10 | `10130685…4e9a5d7a` |
| `diffs/DT5-11.diff` | C-1, C-7 (`runners-epingles.py`, 2 tests, README, plancher 35) | +86 −26 | `172327f0…65c87461` |
| `diffs/DT5-12.diff` | C-2, C-3, C-4, C-5 (job g1), C-8 | +81 −14 | `f905744d…b4da81c4` |
| `diffs/DT5-13.diff` | **C-9** : même correction documentaire dans `s2bis/tests/__init__.py` | +5 −3 | `857cccda…827238a5` |
| `diffs/DT5-14.diff` | **C-10** : extensions pliées en casse, fichiers cachés, autres entrées nommées (deux contrôles, tests, plancher 36) | +83 −35 | `ae0ce865…de9acf1e` |

Concaténation de DT5-9 à DT5-14, dans l'ordre : `bd473d45…7b43e3d`.

### DT5-9 à DT5-12 : propositions de la G2, appliquées telles quelles et relues

- Les quatre diffs proposés s'appliquent après DT5-8 (`git apply --check`, puis application). Les diffs versés sont
  **identiques octet pour octet** aux propositions (mêmes sha256 que la table de `g2/RAPPORT-G2.md`). R-25 : quatre diffs
  séparés, chacun sous 200 lignes ajoutées.
- **Relecture, dont je réponds** :
  - **C-6** : rejoué indépendamment, réseau coupé. `sendmsg` vers 192.0.2.1, sous la garde, lève `OSError` (Network is
    unreachable) et `TENTATIVES` reste vide. La phrase corrigée est exacte.
  - **C-1** :
    - La clé est lue sans exiger d'espace après « : ». C'est plus strict ; la clé reste ancrée sur un blanc, `{`, `,` ou
      `[` qui la précède, donc `macos:` n'est pas lu.
    - La casse est ignorée.
    - Les clés de matrice nommées par `runs-on` sont lues ; des refus en plus sont possibles, jamais un en moins.
    - Les lignes suivantes sont lues après une ancre, une étiquette, un en-tête de bloc ou un flux ouvert. Les limites
      (alias, `<<`, échappements, clé explicite) sont écrites et couvertes par C-8.
  - **C-2** : la relecture de la version après installation et le rattachement du module au paquet (`dpkg -S`) se sont
    exécutés sur l'hôte. L'étape imprime « PyYAML lu : /usr/lib/python3/dist-packages/yaml/__init__.py ». `-P` existe
    depuis Python 3.11 (3.11 sur l'hôte, 3.12 attendu sur l'image [inféré]).
  - **C-3** : la valeur d'un `!!python/object/apply` est refusée sans effet. La clé non hachable sort en 3 par le
    `TypeError` de mon chargeur, rattrapé par `main`.
  - **C-8** : les valeurs lues de `runs-on` et de `strategy.matrix` sont parcourues à toute profondeur ; des refus en
    plus sont possibles dans la matrice (toute valeur en `-latest`), ce qui serre.
- **Mutants de la G2 rejoués sur l'arbre final** (son outil `g2/outils/mutants_propose.py`, sorties
  `sorties/mutants-g2-rejoues-{re,wy}.*`) :
  - `runners-epingles` : 23 tués, 1 FATAL ;
  - `workflows-yaml` : 18 tués, 2 FATAL.
  - Les 3 FATAL (« remplacement trouvé 0 fois » : R-7 et Y-4 `.yaml` non lu, MY-6 sous-dossiers lus) visent les lignes
    `glob` que C-10 remplace. Ils ne comptent pas. Les mutants de C-10 couvrent la même classe (ci-dessous).

### DT5-13 : C-9

La docstring de `s2bis/tests/__init__.py` nomme les appels gardés, et sa limite nomme `sendmsg` (documentaire ; le code
est inchangé). Aucune empreinte ne pèse sur ce fichier : les 32 listes de sommes de `docs/adr-0029` et de `s2bis`,
lues une à une (liste par `git ls-files`), ne le nomment pas. La suite s2bis reste à 341.

### DT5-14 : C-10

- `runners-epingles.py` et `workflows-yaml.py` partagent la même règle, `entrees(dossier)` : tout **fichier** de
  `.github/workflows` dont le nom, plié en casse, finit par `.yml` ou `.yaml` est lu, fichiers cachés compris. Toute
  autre entrée (autre fichier, dossier, même au nom en `.yml`) est comptée et nommée sur la sortie standard, par une
  ligne « N autre(s) entrée(s) de .github/workflows non lue(s) : … », et n'est pas refusée. `glob` est retiré.
- Docstrings mises à jour et reformatées à 120 colonnes au plus (le paragraphe de tête de chaque script).
- Tests :
  - `test_extension_en_capitales_caches_et_autres_entrees` : `A.YML` et `.b.Yaml` refusés ; `c.yml.txt` et le dossier
    `sous.yml` nommés.
  - `test_admis` : vérifie aussi la ligne des autres entrées, sur une sortie conforme.
  - W-15 du runner : `G.YAML` et `.h.yml` refusés ; `i.yml.bak` et `sous.yml` nommés.
  - W-10 : vérifie aussi la ligne des autres entrées. `CAS` passe de 14 à 15.
- Plancher de `controle-unittest` : 35 → **36**, exact. Commentaire du job et README de `scripts/controle` mis à jour.
- Rouges :
  - `sorties/rouge-DT5-14-re.txt` : 2 `FAIL` par `AssertionError` (`test_admis`, test neuf), 0 `ERROR` ;
  - `sorties/rouge-DT5-14-wy.txt` : `ÉCHEC W-10` et `ÉCHEC W-15`, 13 ok, sortie 1.
- Mutants (`outils/mutants_c10.py`, `sorties/mutants-C10.json`) : 8 tués sur 8. Pour chacun des deux contrôles :
  casse non pliée, fichiers cachés écartés, autres entrées tues, dossier au nom en `.yml` lu.

### Gates de la phase 4 (094fa5d + DT5-1..14 contre 094fa5d seule)

Toutes les sorties valent 0, sauf `cargo xtask verify`, à 1 des deux côtés (le ROUGE est sur la tête).

| gate | série | tête |
|---|---|---|
| g5 : hooks / balayage | 57 / vert | 54 / vert |
| g1 : env / runners-epingles (7 workflows, 22 clés) / workflows-yaml (`python3-yaml 6.0.1-2build2`, « PyYAML lu : /usr/lib/python3/dist-packages/yaml/__init__.py », runner 15 ok, conforme) / lint 227 / R-1 / journaux-modele / docs-sha256sums (34, 295) | 0 partout | lint, R-1, journaux, docs : 0 |
| g3 : cas 147 / `--tree` | 0 | 0 |
| runner du vérificateur ×5 | 137 ok | 137 ok |
| s2-harness / s2bis / sim-bis / calib / controle | 418 / 341 / 279 / 65 / **36** | 415 / 341 / 279 / 65 / 26 |
| `cargo test -p xtask` | 0 (81 et 9) | 0 |
| `cargo xtask verify`, lignes VERDICT | 8 VERT, 1 ROUGE | identiques |

### Écarts et clôture de la phase 4

- **E-14** : C-10 a remplacé les lignes `glob` que visaient trois mutants de la G2. Ils sortent en FATAL (remplacement
  introuvable) et ne comptent pas ; leur classe est couverte par les 8 mutants de C-10.
- **E-15** : le reformatage des docstrings de DT5-14 touche des lignes écrites par la G2 (DT5-11, DT5-12). Le texte est
  le même au mot près (contrôlé par comparaison des mots avant et après), seule la coupe des lignes change.
- `ps` filtré sur `$D` : 0 processus. `$D/tmp` vide. Aucun commit, aucune poussée, aucun accès réseau,
  `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée. Suite de l'adjudication : contre-contrôle neuf.

## Ajout daté du 2026-10-09 23:56:25 UTC (`date -u`) : phase 5, réserves du contre-contrôle (adjudication de 23:39:53 UTC, R-1 à R-6, C-11)

- Tête lue au début (23:40:06Z) et à la fin (23:56:16Z) : **`094fa5d3d5debe9dd466e37feee95200ca460dcf`**.
- **Série finale, à appliquer dans l'ordre DT5-1 à DT5-21 sur 094fa5d.** DT5-1 à DT5-14 sont inchangés. Je l'ai vérifiée
  sur un clone neuf de la tête, diff par diff (`git apply --check`, puis application) ; l'arbre obtenu est identique à celui
  des gates. Concaténation de DT5-1 à DT5-21 : `8462701f…37c21f72`.

| diff | objet | lignes | sha256 |
|---|---|---|---|
| `diffs/DT5-15.diff` | R-1 : étiquettes explicites qui perdent le texte refusées (WY), W-16, CAS 16 | +35 −5 | `a6092c6d…13b630c3` |
| `diffs/DT5-16.diff` | R-2 : formes fixées par les tests (RE : 3 tests étendus ; WY : W-14 étendu) | +29 −12 | `ae6115ee…1f0c835a` |
| `diffs/DT5-17.diff` | R-3 : limites des gardes (documentaire ; remplacée par DT5-21) | +7 −3 | `61fabf17…451c4738` |
| `diffs/DT5-18.diff` | R-4 : limites de RE et de WY | +6 −3 | `a790c275…7d34f98a` |
| `diffs/DT5-19.diff` | R-5 : en-tête de `gates.yml` (PR n° 10) | +3 −2 | `32f7c1af…7518b45a` |
| `diffs/DT5-20.diff` | R-6 : datation du paragraphe C-7 du README | +2 −1 | `a3737577…d52f5454` |
| `diffs/DT5-21.diff` | **C-11** : `getaddrinfo` (`host=`) et `getnameinfo` gardés dans les deux gardes, tests, planchers | +67 −28 | `e917ebaf…1528fa1a` |

### DT5-15 à DT5-20 : propositions du contre-contrôle, appliquées telles quelles et relues

- Les six diffs s'appliquent dans l'ordre après DT5-14. Les diffs versés sont **identiques octet pour octet** aux
  propositions (mêmes sha256 que la table de `g2/cc/RAPPORT-CC.md`).
- **Relecture, dont je réponds** :
  - **R-1** : le refus se fait à la composition (`compose_node`, `peek_event`) et avant toute construction, pour les
    seules étiquettes de `PERTE` (forme développée `tag:yaml.org,2002:…`).
    - Un alias ou un nœud sans étiquette explicite n'est pas visé (pas d'attribut `tag`, ou `tag` nul).
    - Les étiquettes inconnues, `python/*` comprises, continuent vers le constructeur sûr, qui les refuse : W-12 garde
      son sens.
    - La docstring dit vrai pour `<<` : le chargeur construit chaque clé avant la fusion.
  - **R-2** : tests seulement ; aucun compte ne change (plancher controle 36, `CAS` 16 de R-1).
  - **R-4, R-5, R-6** : textes exacts sur pièces : sondes P-06, P-08, P-12, P-17, P-18 du contre-contrôle, constat de
    l'adjudication de 21:28:17 UTC [2nd], heure de l'adjudication C-10.
  - **R-3** : vrai à DT5-17, rendu faux par C-11. DT5-21 retire ces limites et nomme les appels désormais gardés.
- Mutants de DT5-2 et de DT5-3 rejoués sur l'arbre final (`sorties/mutants-DT5-2-3-phase5.json`) : 15 tués sur 15.

### DT5-21 : C-11

- **Code**, identique octet pour octet dans les deux paquets : `s2-harness/tests/__init__.py` et
  `s2bis/tests/__init__.py`, bloc de garde comparé par `cmp`, comme le veut la forme adjugée (E-1).
  - `_garde` passe `(a, k)` à la fonction qui lit l'hôte. `getaddrinfo` et les trois `gethostby*` lisent l'hôte
    positionnel, ou `host=`.
  - `socket.getnameinfo` est gardé : l'hôte est le premier élément de `sockaddr`. Un `sockaddr` vide passe à l'appel
    d'origine, qui juge seul.
  - Boucle locale admise, inchangée : `None`, « localhost », littéraux de 127.0.0.0/8 et de ::1.
- **Docstrings** des deux gardes et commentaire du job `s2-harness-unittest` : les appels gardés sont nommés (`host=` et
  `getnameinfo` compris) ; les limites R-3 sont retirées. Restent `_socket`, `sendmsg` et le sous-processus qui
  n'importe pas `tests`.
- **Tests**, un par suite : `test_resolution_par_mot_cle_et_getnameinfo`.
  - Refusés, et inscrits dans `TENTATIVES` : `getaddrinfo(host="example.invalid")`, `getnameinfo` vers 192.0.2.1
    (RFC 5737) et vers 2001:db8::1 (RFC 3849).
  - Admis : `getaddrinfo(host="127.0.0.1")`, `getnameinfo` sur 127.0.0.1 et ::1 (`NI_NUMERICHOST | NI_NUMERICSERV`).
  - Rouge (`sorties/rouge-DT5-21-s2.txt`, `-s2bis.txt`) : `FAILED (failures=1)` dans chaque suite, `AssertionError`
    (`['gaierror', 'gaierror', 'gaierror']` au lieu de `ReseauInterdit` ×3), 0 `ERROR`. Vert : 4 OK dans chaque suite.
- **Planchers exacts** : S2 `PLANCHER` 418 → **419** (`enforcement/verdict-suite-s2.py`, commentaire mis à jour) ; s2bis
  341 → **342** (ligne du job, forme du cas K-02).
- **Mesure : aucune suite ne dépend d'une résolution non locale** (`sorties/tentatives-s2-harness.txt`,
  `tentatives-s2bis.txt`, suites entières sous la garde neuve, réseau coupé).
  - s2-harness : Ran 419, OK (skipped=2) ; `TENTATIVES` = 11 (3 + 8).
  - s2bis : Ran 342, OK ; `TENTATIVES` = 9 (3 + 6).
  - Dans les deux cas, ce sont exactement les appels des tests de garde : aucun autre test ne sort de la boucle locale.
- **Mutants** (`outils/mutants_c11.py`, `sorties/mutants-C11.json`) : 8 tués sur 8, 4 par paquet. Mutations : `host=`
  ignoré ; `getnameinfo` non gardé ; port lu pour l'hôte ; mots-clés non transmis à l'appel d'origine.

### Gates de la phase 5 (094fa5d + DT5-1..21 contre 094fa5d seule)

Toutes les sorties valent 0, sauf `cargo xtask verify`, à 1 des deux côtés (le ROUGE est sur la tête).

| gate | série | tête |
|---|---|---|
| g5 : hooks / balayage | 57 / vert | 54 / vert |
| g1 : env / runners-epingles (7, 22) / workflows-yaml (runner 16 ok, conforme, « PyYAML lu : /usr/lib/python3/dist-packages/yaml/__init__.py ») / lint 227 / R-1 / journaux-modele / docs-sha256sums (34, 295) | 0 partout | lint, R-1, journaux, docs : 0 |
| g3 : cas 147 / `--tree` | 0 | 0 |
| runner du vérificateur ×5 | 137 ok | 137 ok |
| s2-harness / s2bis / sim-bis / calib / controle | **419 / 342** / 279 / 65 / 36 | 415 / 341 / 279 / 65 / 26 |
| `cargo test -p xtask` | 0 (81 et 9) | 0 |
| `cargo xtask verify`, lignes VERDICT | 8 VERT, 1 ROUGE | identiques |

Les processus lourds ont tourné un par un (gates, puis xtask), dans la borne de deux fixée par l'orchestrateur.

### Écarts et clôture de la phase 5

- **E-16** : DT5-17 (R-3, adoptée telle quelle) écrit des limites que DT5-21 retire aussitôt. Les deux diffs sont gardés,
  dans l'ordre adjugé : la série dit l'état final juste. Fondre DT5-17 dans DT5-21 est possible si l'orchestrateur le
  préfère.
- `ps` filtré sur `$D` : 0 processus. `$D/tmp` vide. Aucun commit, aucune poussée, aucun accès réseau,
  `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée. Suite de l'adjudication : passe 2 du contre-contrôle.

## Ajout daté du 2026-10-10 00:33:31 UTC (`date -u`) : phase 6, R-7 et R-8 du contre-contrôle (adjudication de 00:22:41 UTC)

- Tête lue au début (00:22:47Z) et à la fin (00:33:23Z) : **`094fa5d3d5debe9dd466e37feee95200ca460dcf`**.
- Espace disque : `df -h /` avant la compilation, 5,9 G libres. Une seule cible cargo, partagée par les deux arbres (184 M) ;
  8,4 G libres à la fin, copies supprimées.
- **Série finale, à appliquer dans l'ordre DT5-1 à DT5-23 sur 094fa5d.** DT5-1 à DT5-21 sont inchangés. Je l'ai
  vérifiée sur un clone neuf de la tête, diff par diff (`git apply --check`, puis application) ; l'arbre obtenu est
  identique à celui des gates. Concaténation de DT5-1 à DT5-23 : `30e600ca…6e16480c`.

| diff | objet | lignes | sha256 |
|---|---|---|---|
| `diffs/DT5-22.diff` | R-7 : l'hôte n'est lu que dans les formes d'appel valides ; tests étendus dans les deux suites | +50 −16 | `6586e5a2…f727045019` |
| `diffs/DT5-23.diff` | R-8 : troisième garde (`scripts/calib-actifs`) alignée ; test ; 2 lignes du `SHA256SUMS` du lot | +36 −11 | `7db1663f…c0c6902` |

- **Reprise à l'identique** : DT5-22 et DT5-23 sont des copies, octet pour octet (`cmp`), de
  `g2/cc/propose/R-7-propose.diff` et de `R-8-propose.diff`, sans retouche. Ils s'appliquent dans l'ordre après DT5-21.
  Concaténation des deux : `84ee75d1…66f93538`, égale à celle du rapport du contre-contrôle.

### Relecture, dont je réponds

- **R-7** :
  - L'hôte n'est lu que dans une forme d'appel valide. Pour `getaddrinfo` : positionnel, ou `host=`. Pour les trois
    `gethostby*` : positionnel seul. Pour `getnameinfo` : premier élément d'un sockaddr en tuple non vide, sans
    mot-clé.
  - Toute autre forme rend `None` (local) et part à l'appel d'origine, qui lève TypeError ; rien n'est inscrit.
  - Ces fonctions C n'acceptent aucun mot-clé (TypeError constatée par le contre-contrôle sous 3.11 et 3.12). Le
    défaut d'argument `n=_n` fixe bien le nom dans chaque lambda.
  - Aucun appel valide hors de la boucle locale n'est perdu : l'hôte positionnel avec `type=` est désormais lu et refusé
    (forme du mutant K11-1).
- **R-8** :
  - Les trois blocs de garde, de « `TENTATIVES = []` » à la fin, sont égaux octet pour octet (même sha256 de bloc,
    `26a94348…`, dans `s2-harness`, `s2bis` et `scripts/calib-actifs`).
  - `scripts/calib-actifs/SHA256SUMS` : `sha256sum -c` OK ; son sha256 passe à `a4a34b14…a709`.
  - `lancer.sh` reçoit l'épingle en argument (l.29-31) : aucun sha256 n'est recopié dans le code.
  - D'après l'adjudication, l'épingle de ce lot n'est pas encore au JOURNAL : aucun ré-épinglage dans ce lot.
- **Rouges rejoués** (tests de R-7 et R-8 contre les gardes d'avant, puis restauration contrôlée par le sha256 des blocs) :
  - `sorties/rouge-DT5-22-s2.txt` et `rouge-DT5-22-s2bis.txt` : `FAILED (failures=1)`, `AssertionError` (formes
    invalides en `ReseauInterdit` au lieu de `TypeError`) ;
  - `sorties/rouge-DT5-23.txt` : `FAILED (failures=1)`, `['gaierror', 'gaierror']` au lieu de `ReseauInterdit` ×2.
  - Vert : les trois modules OK.
- Mutants : ceux du contre-contrôle (16 sur 16 pour R-7, 2 sur 2 pour R-8) n'ont pas été rejoués par moi. Les diffs sont
  ses formes exactes, et les rouges ci-dessus montrent que chaque test neuf mord.

### Gates de la phase 6 (094fa5d + DT5-1..23 contre 094fa5d seule)

Toutes les sorties valent 0, sauf `cargo xtask verify`, à 1 des deux côtés (le ROUGE est sur la tête).

| gate | série | tête |
|---|---|---|
| g5 : hooks / balayage | 57 / vert | 54 / vert |
| g1 : env / runners-epingles (7, 22) / workflows-yaml (runner 16 ok, conforme) / lint 227 / R-1 / journaux-modele / docs-sha256sums (34, 295) | 0 partout | lint, R-1, journaux, docs : 0 |
| g3 : cas 147 / `--tree` | 0 | 0 |
| runner du vérificateur ×5 | 137 ok | 137 ok |
| s2-harness / s2bis / sim-bis / calib / controle | 419 / 342 / 279 / 65 / 36 | 415 / 341 / 279 / 65 / 26 |
| `cargo test -p xtask` | 0 (81 et 9) | 0 |
| `cargo xtask verify`, lignes VERDICT | 8 VERT, 1 ROUGE | identiques |

Les comptes ne changent pas par rapport à la phase 5 : R-7 et R-8 étendent des tests existants. Le plancher de
calib-actifs reste 65, exact.

### Clôture de la phase 6

`ps` filtré sur `$D` : 0 processus. `$D/tmp` vide. Aucun commit, aucune poussée, aucun accès réseau,
`SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée. Selon l'adjudication, si l'orchestrateur constate l'identité de DT5-22 et
DT5-23 avec les propositions, le lot clôt CONFORME sans passe 3.
