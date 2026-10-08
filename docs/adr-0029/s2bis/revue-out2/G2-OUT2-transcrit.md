# Relecture G2 — OUT2 (transcrit)

> Transcription par l'orchestrateur le 2026-10-08 12:11:04 UTC du rapport rendu par l'agent a70f61e730b828183 (workflow wf_34ba9b2a-037) ; contrôle FM-1.1 : fragments_l51_l14 = 0 ; modèle résolu au transcript : claude-opus-5-5. Texte de l'agent ci-dessous, sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

**Gate 0 : `claude-opus-5-5`.** Je tiens l'identifiant exact du contexte système. L'effort `max` vient de la fiche ; je ne peux pas le mesurer de l'intérieur.

**Horloge** (`date -u`) : de 11:17:47 à 12:09:16 UTC, le 2026-10-08.

**Base** : e6657dcc3154bf2d35c69b84d9deae1385e702a7, tête de `claude/compassionate-noether-szmdyj`. Le dépôt n'a pas bougé : statut vide, `.git/index` (aa0bb89d…) et `HEAD` (e29f8e8d…) ont le même sha256 au début et à la fin, aucune écriture git.

**Rôle** : je suis réviseur neuf et n'ai écrit aucun des trois diffs.

## Verdict : ACCEPTE-AVEC-CORRECTIONS (C-1 à C-3)

- Les trois items sont tenus dans le code produit et dans le texte.
- Les trois corrections portent sur des tests d'OUT-2b seulement : deux règles du lot ne sont pas figées par les tests. Le code produit est juste.

**Contrôles d'entrée**
- SHA256SUMS du générateur : sha256 43116a77…1397, 142 entrées sur 142 OK. `RAPPORT-GENERATEUR.md` est hors de la liste, comme il le déclare (sha256 3b3fddc6…).
- Copie de base : `git archive` avec les 7 exclusions passées en pathspec, 991 entrées, aucun chemin exclu présent.
- Application : `patch -p1 -F0` en série, sans décalage ni rejet. Les états a, b et c ont les sha256 des livrables du générateur.

## Corrections (liste fermée)

**C-1 — `enforcement/tests/run-fixtures-verdict-suite-s2.py:277-279` (cas M-05).**
- **Preuve** : mon mutant B4 survit. Il prend le nom avant le *dernier* point dans `masques` du vérificateur (`os.path.splitext`) au lieu du premier. Il sort en 0 au runner, en 0 à la ligne s2bis et en 0 à S2.
- **Ce mutant n'est pas équivalent.** J'ai mesuré sous 3.10 à 3.13 :
  - `json.abi3.so` (importé par un test) et `argparse.cpython-31x-x86_64-linux-gnu.so` posés à la racine forgent un « OK » : la marque est posée et le code vaut 0 ;
  - la règle actuelle, prise avant le premier point, les refuse et les nomme ;
  - aucun cas ne fige cette différence.
- **Remède** : ajouter `"json.abi3.so"` aux entrées de `masquee("M-05", …)` et mettre l'attendu à `["json.abi3.so", "json.py", "unittest.py"]`. Le diff est dans `g2/preuves/remede/remede-runner.diff`.

**C-2 — `s2-harness/tests/test_oracle_record.py:517-519`.**
- **Preuve** : mon mutant C4, la même règle « dernier point » dans `oracle_record.masques`, survit (S2 en 0).
- **Remède** :
  - ajouter `"json.abi3.so"` aux fichiers posés ;
  - mettre l'attendu écrit à la main à `["argparse", "json.abi3.so", "json.py", "unittest.py"]` ;
  - compléter la phrase « Rougit si » de la docstring (l.492-493) avec la règle prise avant le dernier point.

**C-3 — `s2-harness/tests/test_oracle_record.py:505-507`.**
- **Preuve** : mon mutant C7 survit (S2 en 0). Il ne contrôle `suite` que si c'est la première commande (`commandes[0] == "suite"`). Le test ne lance jamais `suite` seule après une autre commande, alors que la CLI admet `--commande suite-s2bis --commande suite`.
- **Remède** :
  - après le premier refus, appeler `orc.enregistrer(d, "G2", a, dep, s2bis, ("suite-s2bis", "suite"))` sous le même `assertRaisesRegex(ValueError, "unittest[.]py.* — refus$")`, avant le contrôle « rien d'écrit » ;
  - ajouter l'ordre des commandes à « Rougit si ».

**Remède vérifié sur une copie corrigée**
- B4 est tué par M-05, C4 par S2 (« Lists differ »), C7 par S2 (« ValueError not raised », l.507).
- Le runner donne 105 ok sous 3.10 à 3.13.
- S2 est conforme à Ran = 408 sous 3.11 à 3.13. Sous 3.10, on retrouve le rouge connu (80 noms, sha256 6de48d41, comme la base) ; le test neuf est « ok » sous les quatre versions.
- Forme : aucune ligne de plus de 120 caractères, aucun octet 92 ajouté, environ +3 lignes à OUT-2b.
- sha256 des fichiers corrigés : runner a0ba8430…, test 8d6dae71….
- Le générateur doit rejouer ses campagnes OUT-2b en y ajoutant B4, C4 et C7.

## Points du brief

| Point | Tenu | Fichier:ligne (état final) | Figé par |
|---|---|---|---|
| 1a garantie et limite | oui | runner l.34-40 | N6 mesure la limite : rejeu synchrone au nonce lu, sortie 0, ce que la docstring annonce |
| 1b nonce par requête | oui | runner l.52 ; serveur l.76-83 ; `demande` l.107-127 (tirage l.108, refus nommé l.123-124) | R-09 (D7), R-10, R-11 ; mutants A1 à A6 |
| D7 rejoué | oui | — | base : 0 (97 ok) ; final : 1, « réponse sans le nonce de sa requête » |
| D4, D5, D6b refusés ; D6a sans effet | oui | — | 1 / 1 / 1, puis 0 |
| 2 règle d'usage de l'enregistreur | oui | `s2-harness/tools/README.md` l.1-31 ; `oracle_record.py` l.19-22 | leurre E1, mesuré |
| 3 masquage | oui | vérificateur l.20-24, l.61-64, l.150-154 ; `oracle_record.py` l.110-115, l.204-207 | M-01 à M-05 ; `test_racine…` l.486-520 |
| `-I` avec `-m`, mesuré | oui | Q-2 ; docstring du vérificateur l.22-24 | mesures ci-dessous |
| 4 rien retiré ni affaibli | oui | — | voir ci-dessous |
| Planchers exacts | oui | `CAS` 105 (l.180) ; `PLANCHER` 408 (vérificateur l.33) ; `gates.yml` et FORMAT inchangés | P1 et P2 tués |

**Détail de la règle d'usage (E1).** J'ai lancé l'outil depuis l'arbre du commit enregistré, avec un vérificateur complaisant réaliste (vrai analyseur, `main` menteur) et un test rouge. Résultat : exit 0 conforme, et la relecture par le même arbre dit aussi conforme. L'arbre relu, lui, refuse ce commit à l'écriture et à la lecture. Le README décrit donc exactement le comportement du code.

**Détail de la mesure de `-I` avec `-m` (3.10 à 3.13).**
- Sans `-I`, `unittest.py` et `json.py` masquent la bibliothèque.
- Avec `-I`, `unittest.py` ne masque plus : le chemin 0 est absent ; `safe_path` vaut None sous 3.10 et True sous 3.11 et plus.
- Avec `-I`, `json.py` masque encore : la découverte `-t .` remet la racine en tête.
- `-I` implique `-E`.
- J'ai recompté le chiffre « 40 à 43 autres » de la docstring : 44, 41, 41 et 44 noms sous 3.10, 3.11, 3.12 et 3.13, unittest compris. Le chiffre est juste.

**Détail du point 4.**
- Les 97 noms de cas de la base sont présents à l'identique.
- Les 13 tests de l'enregistreur ont un AST identique, et le niveau module aussi.
- `copie()` est équivalente à l'ancien bloc R-01 à R-08 : `CAS + 0`, `capture = 0`.
- D5 change de motif (« ÉCHEC V-03 » devient « réponse illisible ») mais garde la sortie 1 : le refus vient plus tôt.

## Leurres

| Leurre | base | final |
|---|---|---|
| R-1 runner, 3.12 : V0 / D1 / D2 / D3 / D4 / D5 / D6a / D6b / D-CAPTURE / D7 | 0 / 3 / 1 / 1 / 1 / 1 / 0 / 1 / 0 / **0** | 0 / 3 / 1 / 1 / 1 / 1 / 0 / 1 / 0 / **1, nonce nommé** |
| R-1 enregistreur, 3.11 et 3.12 : L0 / L0b / L1 / L2 / L3 | conforme / 1 / refus / refus / 1 | identiques |
| N1 nonce deviné ; N2 nonce null ou vide ; N4 transcript partiel ; N5 réponse écrite après sa requête mais au nonce périmé | — | 1, nonce nommé |
| N3 réponse anticipée au format à deux champs | 1, illisible | 1, illisible |
| N6 rejeu synchrone au nonce lu | — | **0** (limite « lit les requêtes », écrite) |
| `unittest.py`, `unittest/`, `argparse.py`, `argparse.<EXT>.so` sur les lignes s2bis et S2 | 0, conforme forgé | 1, refus nommé, suite non lancée (pas de marque), sous 3.10 à 3.13 |
| `unittest.pth` | sans effet | 1, refusé (sur-refus inoffensif) |
| `sitecustomize.py`, `usercustomize.py` | sans effet | non refusés, sans effet ; témoin en place : conforme réel en 28 s |
| E2 `json.py`, E3 extension `argparse.<EXT>.so` (commande `suite`) | — | refusés avant tout run |
| E5 `unittest/` (`suite-s2bis`), E6 `argparse.py` (`suite-sim-bis`) | — | exit 1 consigné et nommé ; relecture : refus (exit) |
| E7 enregistrement `suite` écrit par l'outil de base sur une racine masquée | — | **lu conforme** par l'arbre relu |

N5 montre que le nonce est strictement plus fort que le refus d'une réponse disponible avant sa requête. E7 fait passer MASQUES-LECTURE-1 au niveau [mesuré].

## Mutants (3.12, réseau isolé, borne de 300 s par commande, classés runner puis ligne s2bis puis S2)

Mon classement est plus serré que la règle SHOGEN-MUT-FATAL-1 : un mutant n'est tué que si la sortie vaut 1 **avec** un refus nommé ; sinon il est FATAL.

| Mutants | Tués par |
|---|---|
| A1 contrôle coupé ; A2 nonce par run ; A3 constant ; A4 vide ; A5 dérivé de la requête ; A6 refus non nommé | runner (R-09 à R-11 ; A2 par R-11 seul) |
| B1, B2, B3, B5 à B10 (vide, unittest seul, préfixe, nom complet, refus après lancement, sortie 3, non nommé, `tests/`, `builtin_module_names`) | runner (M-01 à M-05) |
| P2 `CAS` 104 | runner (compte des cas) |
| C1, C2, C3, C5, C6 (enregistreur) | S2 |
| P1 `PLANCHER` 407 | S2 (« Ran 408 > plancher 407 ») |
| **B4, C4, C7** | **vivants**, d'où C-1 à C-3 |

Total : 25 mutants, 22 tués (16 par le runner, 6 par S2), 3 vivants, 0 FATAL.

## Matrice (`-X dev -W error`, réseau isolé, état final)

| Python | runner | s2bis | sim-bis | S2 |
|---|---|---|---|---|
| 3.10 | 105 ok | Ran = 255, conforme | Ran = 172, conforme | rouge connu PY310-1 : 77 FAIL + 3 ERROR, 80 noms identiques à la base (sha256 6de48d41), Ran 408 ; test neuf ok |
| 3.11 / 3.12 / 3.13 | 105 ok | Ran = 255, conforme | Ran = 172, conforme | Ran = 408, conforme |

Aucune ligne « Warning » ni « Exception ignored » dans les sorties des lignes du job. Celles qu'on voit aux leurres de l'enregistreur de R-1 viennent du script de leurres lui-même (`open()` non fermés l.22 et l.83).

## Forme et xtask

| Diff | + / − | > 120 caractères | octets 92 ajoutés | R-13 | R-8 |
|---|---|---|---|---|---|
| OUT-2a | 73 / 35 | 0 | 0 | 0 | `secrets` (bibliothèque standard) |
| OUT-2b | 98 / 5 | 0 | 0 | 0 | aucun import neuf |
| OUT-2c | 35 / 1 | 0 | 0 | 0 | aucun import neuf |

- Le contrôle positif de R-13 répond. Aucune espace de fin ni tabulation ; la seule ligne réindentée est la continuation de `subprocess.run` dans `copie()`, légitime.
- **xtask** (`cargo --locked xtask verify` sur la copie, réseau isolé) :
  - S-G1 à S-G8 VERT, S-G7a compris ; fmt, no_std et clippy VERT ;
  - S-G9 ROUGE, seule violation `docs/17-modele-de-menace.md:70`, la violation connue ;
  - verdict global ROUGE.

## Avis sur les choix Q-n du générateur

- **Q-1 (nonce par requête)** : d'accord.
  - N5 passerait un contrôle « réponse avant sa requête », mais le nonce le refuse.
  - Le nonce par run est inutile : A2 n'est tué que par R-11.
  - Nuance de texte : la phrase « le nonce est déterministe » du rapport doit se lire « le contrôle est déterministe ».
- **Q-2 (refus de tout nom standard, pris avant le premier point)** : d'accord, et `-I` seul ne suffit pas, comme mesuré.
  - Coût : un sur-refus d'entrées non importables, comme `unittest.pth`. L'échec reste fermé et nommé, et aucune racine actuelle n'est touchée. Je l'accepte.
  - Hors de `sys.stdlib_module_names` : `test`, `sitecustomize`, `usercustomize`. Les deux derniers sont sans effet mesuré depuis la racine, et aucune suite n'importe `test`.
- **Q-3 (README de l'outil)** : d'accord. Le FORMAT spécifie l'observateur et `test_format.py` lit son texte. La garde `outil` (schéma v2) donne de la traçabilité, pas une preuve de revue : elle relève d'un item.
- **Q-4 (règle écrite deux fois)** : d'accord. J'ai vérifié que l'arbre de production de `test_rendu_production.py` (l.297-301) n'a pas de vérificateur. Mais deux copies de la règle exigent deux épingles complètes : c'est l'objet de C-1 et C-2.
- **E-7 (OUT-2c sans mutants)** : sans objet, c'est du texte seul. Le leurre E1 en tient lieu de contrôle.

## Items à former et observations (hors liste fermée)

1. **SCRIPT-MASQUE-1, [mesuré] sur l'état final.**
   - Un `enforcement/subprocess.py` complaisant fait rendre « conforme Ran = 255 » à la ligne s2bis sans lancer la suite.
   - Un `enforcement/tests/json.py` fait rendre « 105 ok » et la sortie 0 au runner, sans jouer un seul cas.
   - Cela annule la garantie écrite du runner. Par un `enforcement/tests/secrets.py` [inféré], cela annule aussi l'imprévisibilité du nonce d'OUT-2a. L'item doit le dire.
2. **RESUME-FORGE-1, [mesuré] sur l'état final** : une suite de 2 tests dont un en FAIL obtient « conforme, Ran = 255 ».
3. **MASQUES-LECTURE-1** : passe de [inféré] à [mesuré] par E7.
4. **Limite sous 3.9, à former comme item** (le générateur l'écrit « sans item »).
   - `s2-harness/README.md:17` annonce Python ≥ 3.9, mais `sys.stdlib_module_names` n'existe qu'à partir de 3.10.
   - Sous 3.9, l'AttributeError n'est pas rattrapée par `oracle_record.main` : sortie 1, qui se confond avec « une commande a échoué » [inféré : 3.9 absent de l'hôte].

## Écarts du réviseur

- **E-1** : ma boucle d'attente `pgrep -f` se reconnaissait elle-même. Je l'ai arrêtée (sortie 144), sans effet sur les mesures.
- **E-2** : première passe des formes `.so` fausse, par un bug de mon script. Je l'ai corrigée et refaite ; seule la passe finale compte.
- **E-3** : le témoin relogé hors de l'arbre est rouge, parce que la suite s2bis lit le FORMAT de l'arbre. Je l'ai remplacé par des témoins en place.
- **E-4** : le leurre N4 sur la base bloque : un serveur muet bloque le runner de base, limite connue de R-1. Le script s'est arrêté là, donc N4 à N6 ne sont pas mesurés sur la base ; c'est sans objet.
- **E-5** : premier E1 refusé au chargement de l'analyseur ; je l'ai refait avec un vérificateur complaisant réaliste.
- **E-6** : sim-bis tourne avec `GIT_DIR` pointé sur le dépôt et `GIT_OPTIONAL_LOCKS=0` ; j'ai contrôlé que l'index et `HEAD` sont inchangés.

## Journal G1 (bref)

- **Lu [lu]** :
  - le brief ; le G0 COLLECTE en entier ; ANNEXE-B l.1175-1185 (B.73) ; ANNEXE-D l.32-48 (liste D.2, pour l'éviter) ; `revue-r1/` en entier ;
  - les trois diffs ; en entier, le runner, le vérificateur et `oracle_record.py` finaux ;
  - `test_oracle_record.py` l.1-120 et l.400-523 ; `gates.yml` par grep ; `test_format.py` l.1-30 ; `test_rendu_production.py` l.290-310 ;
  - les scripts de leurres de R-1 ; puis RAPPORT-GENERATEUR.md, après mes mesures.
- **Chiffres recomptés par moi** : 97 et 105 cas, 255, 172, 408, 80 rouges (sha256 6de48d41), 44/41/41/44 noms, transcripts de 175 et 185 lignes.
- **PID** (tous terminés) : `leurres_r1.sh` 31707 ; runners 31527 et 31528 ; `leurres_verif.sh` 502 ; `matrice.sh` 12068 ; campagne de mutants 25832 ; `xtask.sh` 25092 ; leurres de l'enregistreur 4196 et 4197 ; leurres nonce 10485 et 10486.
- **Interdits respectés** :
  - aucune pièce de D.2, aucun `*.jsonl`, aucun dossier interdit ouvert ;
  - les recherches récursives sont restées bornées à `s2-harness`, `s2bis` et `scripts/sim-bis` de la copie ;
  - `SHOGEN_S2_CAMPAGNE_CONTROL` n'a jamais été posée (`env -u` et `isole.sh` la retirent) ; rien sur Pocket.
- **Nettoyage** : les copies, `cible/` et `tmp/` sont supprimés.

## Fichiers

Tous sous `<scratchpad>/s2bis/outillage2/g2/` :
- `SHA256SUMS` : 156 entrées, toutes OK ; sha256 281f9d35f68d51542aa506842b2e740c6376d6427a7d233ebc84ac88827a318d.
- `NOTES.md` : sha256 bec40dcf27574ab21f400a77344b0457c0d9487d51ee035508957534d383c1f4.
- Remède à transmettre au générateur :
  - `preuves/remede/remede-runner.diff` (b0af92b3…) ;
  - `preuves/remede/remede-test_oracle_record.diff` (0f9d2139…).
- Mutants : `preuves/mutants/campagne1.txt` (0cf0770d…), `preuves/mutants/campagne2-C7.txt` (b33b4e85…), et les vérifications du remède `preuves/remede/mutants-B4-C4-sur-corr.txt` (a418059e…) et `preuves/remede/mutants-C4-C7-sur-corr.txt` (58186f2c…).
- Autres preuves : `preuves/matrice/`, `preuves/leurres-r1/`, `preuves/leurres-nonce/`, `preuves/leurres-masque/`, `preuves/leurres-enreg/`, `preuves/place/`, `preuves/masque-formes.txt` (985c6612…), `preuves/xtask/verdicts.txt` (8fb029b7…), `preuves/rouge/`.
- Outils :
  - `outils/lance.sh` (72911f1c…) ;
  - `outils/mutants_g2.py` (bb71cbed…) ;
  - `outils/leurres_nonce.py` (24f25c16…) ;
  - `outils/leurre_verif.py` (00674464…) ;
  - `outils/leurres_enreg_g2.py` (81017ae5…) ;
  - `outils/masque_formes.py` (0522c546…) ;
  - `outils/compte_masques.py` (33326d92…) ;
  - `outils/mesure_I.py` (b8b8c5ec…).
- `leurres/` : les scripts de R-1, octets inchangés (151cb390…, c39c4711…).
