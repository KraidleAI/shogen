# Contre-contrôle et relecture G2 neuve — OUT2, vague 2 (transcrit)

> Transcription par l'orchestrateur le 2026-10-08 14:56:51 UTC du rapport rendu par l'agent abec17e75b972e614 (workflow wf_eabb8e95-e1a) ; contrôle FM-1.1 : fragments_l51_l14 = 0 ; modèle résolu au transcript : claude-opus-5-5. Texte de l'agent ci-dessous, sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Revue G2 neuve : corrections d'OUT-2 (C-1 à C-3) et diffs neufs OUT-2d, OUT-2e, OUT-2f

**Gate 0 : `claude-opus-5-5`.** L'identifiant exact vient du contexte système. L'effort `max` vient de la fiche : je ne peux pas le mesurer de l'intérieur.

- **Horloge** (`date -u`) : de 14:06:43 à 14:54:53 UTC, le 2026-10-08.
- **Rôle** : je suis réviseur neuf. Je n'ai écrit aucun des six diffs, ni la G2 d'OUT-2.
- **Base** : `e6657dcc3154bf2d35c69b84d9deae1385e702a7`, tête de `claude/compassionate-noether-szmdyj`.
  - Le dépôt n'a pas bougé : statut vide, et les sha256 de `.git/index` (aa0bb89d…) et de `.git/HEAD` (e29f8e8d…) sont les mêmes au début et à la fin.
  - Aucune écriture git. sim-bis lit l'historique dans un clone nu fait dans le scratchpad.
- **Ordre de travail** : j'ai lu et mesuré d'abord. J'ai lu le rapport écrit du correcteur à 14:33, après mes mesures, puis j'ai confronté.

## Verdict : ACCEPTE-AVEC-CORRECTIONS (C-1 à C-4)

- **(a) Contre-contrôle de C-1 à C-3 : tenu.**
  - Les corrections sont faites par les tests seuls. Le code produit est le même, octet pour octet, que dans l'ancien OUT-2b.
  - B4, C4 et C7 sont tués sur OUT-2b corrigé et sur l'état final. Ils restent vivants sur l'ancien OUT-2b : ce sont donc bien les tests neufs qui les tuent.
- **(b) OUT-2d, OUT-2e et OUT-2f ferment les trois items dans le code.**
  - Mes leurres de la classe visée sont refusés sous 3.10 à 3.13.
  - La matrice est verte, sauf le rouge connu PY310-1, qui garde les mêmes 80 entêtes qu'à la base.
  - Les planchers sont exacts aux états d, e et f, et `gates.yml` est inchangé.
  - Forme conforme, et aucun cas ni test n'est retiré ou affaibli.
- **Quatre corrections, toutes dans les tests ou le texte ; le code produit est juste.**
  - C-1 à C-3 : trois règles du lot ne sont épinglées par aucun test, et trois mutants non équivalents survivent aux quatre lignes du job.
  - C-4 : un énoncé du vérificateur est faux, mesuré.
- **Vecteur neuf mesuré**, rendu en item 5 : une extension compilée posée à côté d'un module de test.

## Corrections (liste fermée ; lignes de l'état final)

J'ai écrit et vérifié un remède à C-1, C-2 et C-3 sur une copie de l'état final : `remede/remede-C1-C3.diff` (25 lignes ajoutées, 14 retirées). C'est une donnée : le correcteur écrit et prouve lui-même.

**C-1 — OUT-2d, `enforcement/tests/run-fixtures-verdict-suite-s2.py:433-435` (cas I-01), commentaire l.53-54.**
- **Preuve** : mon mutant D02 place la garde du runner après `import io`, juste avant `import json`.
  - Il survit aux quatre lignes : runner 0 (109 ok), s2bis 0, S2 0, sim-bis 0.
  - I-01 ne pose que `json.py`, et I-02 que `secrets.py`. Or `contextlib` et `importlib` sont importés entre la garde et `json`, et ils ne sont ni préchargés, ni intégrés, ni gelés sous 3.10 à 3.13 (mesuré).
  - Sur une copie mutée de l'état final, un `contextlib.py` marqué posé à côté du runner est exécuté, et le runner sort en 0 avec 123 ok (`preuves/equiv/D02f-LD03a.txt`).
- **Remède (tests seulement)** : I-01 pose son corps (« 999 ok » puis `os._exit(0)`) sous le nom de chaque import qui suit la garde : `contextlib.py`, `importlib/__init__.py`, `json.py`, `py_compile.py`, `re.py`, `shutil.py`, `subprocess.py`, `tempfile.py`. `voisin` accepte alors un tuple de noms.
- **Vérifié sur le remède** : runner 123 ok, et D02 y est tué par I-01.

**C-2 — OUT-2d, même fichier, l.446-454 (cas I-04).**
- **Preuve** : mon mutant D04 place la garde du vérificateur après `import re`, et il survit aux quatre lignes.
  - I-04 ne pose que `subprocess.py`.
  - Sur une copie mutée, un `re.py` marqué est exécuté, et le verdict reste « conforme » (`preuves/equiv/D04f-LD03b.txt`).
- **Remède (tests seulement)** : I-04 pose un module transparent et marqué sous chacun des noms `re`, `secrets`, `shutil`, `subprocess` et `tempfile`. Le cas exige qu'aucune marque ne soit posée.
- **Vérifié sur le remède** : runner 123 ok, et D04 y est tué par I-04.

**C-3 — OUT-2d et OUT-2f, `s2-harness/tests/test_oracle_record.py:552-566` (`test_bytecode…`) et l.585-611 (`test_verifier_refuse…`).**
- **Preuve** : la docstring de `bytecode` (`oracle_record.py:129-133`) annonce « .pyc : cache d'un __pycache__, ou module sans source ». Les deux tests ne posent qu'un .pyc de `__pycache__`.
  - Mon mutant D11 restreint la règle à `__pycache__/` à l'écriture, F10 fait de même à la lecture. Les deux survivent.
  - Sur une copie mutée par D11, un `tests/aide.pyc` sans source est écrit avec exit 0 et lu conforme. L'état final le refuse à l'écriture et à la lecture (LF-05).
- **Remède (tests seulement)** :
  - `test_bytecode…` ajoute un commit qui ne porte qu'un `.pyc` sans source, refusé pour chaque commande, sans rien écrire ;
  - `test_verifier_refuse…` ajoute un enregistrement qui ne porte que ce `.pyc` dans `tree.sha256`, et attend « refus (masque) ».
- **Vérifié sur le remède** : `test_oracle_record` 19 OK, S2 complet conforme (Ran = 413), et D11 comme F10 y sont tués par S2.

**C-4 — OUT-2e, `enforcement/verdict-suite-s2.py:30` (docstring) et l.59 (commentaire d'AMORCE).**
- **Énoncés** : l.30 dit « écarte tout .pyc de l'arbre », et l.59 « aucun .pyc de l'arbre n'est lu (F-13) ». Le rapport du correcteur reprend ces énoncés.
- **Preuve** : ils sont faux. `sys.pycache_prefix` ne déplace que la recherche du cache `__pycache__`.
  - LE-11 : un `aide.pyc` sans source, importé par un test, est exécuté (sa marque est posée), et le verdict est « conforme » sous 3.10 à 3.13.
- **Remède** : deux voies, au choix de l'orchestrateur.
  - Au minimum, rendre le texte vrai : « écarte les .pyc de cache (__pycache__) … ; un .pyc sans source ou une extension compilée posés dans l'arbre restent importés : limite, item 5 ».
  - Ou fermer le vecteur : refus nommé, avant lancement, de tout fichier compilé sous la racine de la suite (`.pyc` et suffixes de `EXTENSION_SUFFIXES`), avec un cas, et `CAS` et `PLANCHER` recalés.

## Contre-contrôle de C-1 à C-3 (Python 3.12)

| Correction | Fichier:ligne (OUT-2b corrigé) | Mutant | Ancien OUT-2b | Corrigé | État final |
|---|---|---|---|---|---|
| C-1 | runner l.278-280 | B4 (`splitext`, vérificateur) | VIVANT | TUÉ par le runner (M-05 « écart ») | TUÉ |
| C-2 | test l.520-522, « Rougit si » l.492-494 | C4 (`splitext`, enregistreur) | VIVANT | TUÉ par S2 (« Lists differ ») | TUÉ |
| C-3 | test l.508-509 | C7 (`suite` en première commande seulement) | VIVANT | TUÉ par S2 (« ValueError not raised ») | TUÉ |

## Contrôles d'entrée

- **SHA256SUMS du correcteur** : sha256 `237982bc…`, conforme à la valeur déclarée ; 267 entrées sur 267 OK.
- **Copie** : `git archive` avec les 7 exclusions, 991 entrées.
- **Application** : `patch -p1 -F0` en série, sans décalage ni rejet. Les états a à f ont les sha256 des livrables du correcteur.

## Points du brief, OUT-2d à OUT-2f

- **Garde du runner, du serveur et des copies** : tenue (runner l.53-56), mais épinglage partiel (C-1).
- **Garde du vérificateur lancé en script** : tenue (l.38-41), mais épinglage partiel (C-2).
- **Source exécutée, jamais un .pyc** : tenu pour le serveur et pour `ligne_du_job`.
- **Ce que change `-I`, mesuré sous 3.10 à 3.13** : `-I` ignore PYTHONDEVMODE, PYTHONWARNINGS, PYTHONHASHSEED (le hachage devient aléatoire), PYTHONPATH et PYTHONIOENCODING. `-X dev -W error` en ligne de commande restent tenus. C'est conforme à Q-5.
- **Enregistreur** :
  - la production tourne en `-I` ;
  - une racine s2-harness masquée est refusée pour toute commande ;
  - le bytecode committé est refusé (C-3 pour le cas sans source).
- **AMORCE** : équivalente à `-m unittest`, mesuré sous 3.10 à 3.13.
  - `sys.path[0]` vaut le dossier absolu et `''` est absent.
  - `argv[0]` vaut « python3.X -m unittest », et le code de sortie est celui de unittest.
- **`accord`** : refuse, en le nommant, un compte absent, sans nonce, illisible ou en désaccord.
- **Lecture `masque`** : tenue.
- **Version minimale (3.9)** : dite dans `s2-harness/README.md` l.17-18.
- **`gates.yml`** : inchangé (`ee03d7b1…`). Les motifs du brief tombent sur l.220, l.196 et l.247, une ligne chacun.
- **Rien retiré ni affaibli** :
  - les 105 cas de l'état c sont présents, plus 18 neufs ;
  - les 21 fonctions de test de c sont présentes, plus 5 neuves ;
  - seul `test_journaux…` change d'attendu : il exige maintenant `-I`, ce qui le durcit.
- **Rouges d'assertion recontrôlés** : 6 FAIL et 0 ERROR pour OUT-2d, 3 sous-tests FAIL pour OUT-2f.

## Leurres (états d'avant mesurés sous 3.12 ; état final sous 3.10 à 3.13)

| Leurre | Avant | Final |
|---|---|---|
| LD-01 `enforcement/subprocess.py` complaisant, ligne s2bis, suite rouge | 0, « conforme Ran = 255 », module importé | 1, refus réel, non importé |
| LD-02 `tests/json.py` (« 999 ok », `os._exit(0)`) | 0 | 1 (115 ok, 8 échecs) |
| LD-03 modules masquants, 8 à côté du runner et 5 à côté du vérificateur, chemin relatif, absolu ou par lien | contextlib, re importés | aucune marque |
| LD-04 paquet masquant ; LD-05 `sitecustomize`, `usercustomize`, `.pth` | paquet importé ; LD-05 sans effet | non importé ; sans effet |
| LE-01 résumé forgé puis `os._exit(0)` | 0, « conforme Ran = 255 » | 1, « compte réel absent » |
| LE-04 SIGTERM, LE-05 fork, LE-06 stdout fermé, LE-07 fd 2 détourné + `atexit` | 0 | 1 |
| LE-14 compte d'un run précédent rejoué | — | 1, « sans le nonce du run » |
| LE-08 nonce lu dans `__main__` | — | 0 : limite écrite (E-F3) |
| LE-09 `addFailure` neutralisé | 0 | 0 : limite, voir O-1 |
| LE-11 `.pyc` sans source importé par un test | 0 | **0, exécuté** : C-4 |
| LE-13 extension `tests/test_t.so` | 0 | **0** : item 5 |
| LF-01 et LF-02 : enregistrement ancien sur racine masquée, ou avec .pyc | écrit exit 0, lu conforme | refus (masque) à la lecture ; refus à l'écriture |
| LF-04 `.so` dans l'arbre de l'enregistreur | conforme | **conforme** : item 5 |
| LF-06 `suite`, test qui forge puis `os._exit(0)` | — | exit 0, conforme (item 1, confirmé) |

- **R-1, runner** : D7 passe de 0 à 1, refusé au nom du nonce ; les autres leurres gardent leur verdict.
- **R-1, enregistreur** : identique à la base.
- **G2, nonce** : N1 à N5 sortent en 1, et N6 en 1 aussi (écart E-5 du correcteur).

## Mutants (Python 3.12, borne 300 s, classés runner, puis s2bis, S2, sim-bis)

| Campagne | N | Tués (runner / S2) | Vivants | FATAL |
|---|---|---|---|---|
| Contre-contrôle (B4, C4, C7 sur l'état b et l'état final) | 6 | 6 (2 / 4) | 0 | 0 |
| Témoins sur l'ancien OUT-2b | 3 | 0 | 3, attendus | 0 |
| OUT-2d | 16 | 13 (6 / 7) | **D02, D04, D11** | 0 |
| OUT-2e | 15 | 14 (14 / 0) | E12, équivalent | 0 |
| OUT-2f | 12 | 11 (0 / 11) | **F10** | 0 |
| Remède (D02, D04, D11, F10) | 4 | 4 (2 / 2) | 0 | 0 |

## Matrice (état final, PYTHONDEVMODE=1, PYTHONWARNINGS=error, réseau isolé)

| Python | runner | s2bis | sim-bis | S2 |
|---|---|---|---|---|
| 3.10 | 123 ok | 255 | 172 | PY310-1 : 77 FAIL et 3 ERROR, 80 entêtes identiques à la base ; tests neufs « ok » |
| 3.11, 3.12, 3.13 | 123 ok | 255 | 172 | Ran = 413, conforme |

- Aucune ligne « Exception ignored » ni « Warning » dans les sorties.
- **États intermédiaires (3.12)** : l'état d donne 109 ok et S2 412 ; l'état e donne 123 ok et S2 412. Les deux sont verts.

## Planchers et forme

- **Planchers exacts** : `CAS` vaut 105, puis 109, puis 123 ; `PLANCHER` de S2 vaut 408, puis 412, puis 413. s2bis (255) et sim-bis (172) sont inchangés.
- **Forme** :
  - lignes ajoutées : 102, 152, 126 et 54, toutes sous 200 ;
  - aucune ligne de plus de 120 caractères, aucun marqueur R-13, imports de la bibliothèque standard seulement ;
  - octets 92 par fichier : même compte à chaque état.
- **xtask** (lignes de verdict seules) :
  - S-G1 à S-G8 VERT ;
  - S-G9 ROUGE sur sa seule violation connue, `docs/17-modele-de-menace.md:70` ;
  - fmt, no_std et clippy VERT ;
  - verdict global ROUGE, connu.

## Confrontation avec le rapport du correcteur

- **Je suis d'accord** avec : C-1 à C-3, Q-5 à Q-8, les leurres, la matrice, les planchers, xtask et les items 1 à 4.
- **« 55 sur 55 tués »** : vrai pour ses mutants. Mais aucun test ne fige les positions intermédiaires de la garde (D02, D04), ni la branche « sans source » de `bytecode` (D11, F10).
- **« Aucun .pyc de l'arbre n'est lu »** : faux pour un .pyc sans source (C-4).
- **Preuves des états intermédiaires** : ses `lignes-e` et `lignes-f` comptent 121 ok, donc datent d'avant les diffs finaux. Je les ai repassées sur les diffs finaux : vertes.

## Observations (non bloquantes)

- **O-1** : la limite d'AMORCE est plus large qu'écrit. LE-09 neutralise `addFailure` sans viser AMORCE, et le verdict reste « conforme ». Je propose « un test qui altère unittest dans son processus, qu'il vise ce mécanisme ou non ».
- **O-2** : la docstring du vérificateur dit encore, l.4-5, qu'il lance la suite par « python3 -B -m unittest discover … » ; il passe désormais par AMORCE (`-c`).
- **O-3** : hors de la forme du job, sous `python -S` en 3.10, un `os.py` voisin est importé avant la garde. Depuis 3.11, `os` est gelé et ce n'est plus le cas.
- **O-4** : l'écart de preuve E-10 du correcteur est comblé par mes passes des états d et e.
- **O-5** : le mode `x` du compte n'apporte rien ; c'est pourquoi E12 est équivalent.

## Items à former

1. **SHOGEN-S2BIS-ENREG-SUITE-COMPTE-1** (du correcteur), confirmé [mesuré, LF-06, sous 3.10 à 3.13].
2. **SHOGEN-S2BIS-ENREG-DRAPEAUX-1** (du correcteur).
3. **Limite d'OUT-2f** (du correcteur) : un run de production sans `-I` n'est pas refusé à la lecture si `tools/` porte un masque [inféré].
4. **Limites écrites** : E-F3 et N6' ; l'échec sous 3.9 est fermé mais non nommé.
5. **Neuf : SHOGEN-S2BIS-SUITE-CODE-COMPILE-1** [mesuré sous 3.10 à 3.13].
   - **Constat** : une extension `tests/test_t.so` (suffixe `.so` nu) remplace `test_t.py` à l'import.
     - unittest ne le détecte pas : son contrôle n'ôte que la dernière extension (`loader.py` l.59-60 et l.405-417, [lu]).
     - Le vérificateur dit « conforme » (LE-13), et l'enregistreur écrit puis lit « conforme » (LF-04).
     - Un `.pyc` sans source importé par un test est exécuté par le vérificateur (LE-11).
   - **Prix** [inféré] :
     - côté vérificateur, un refus nommé des fichiers compilés sous la racine de la suite ;
     - côté enregistreur, ajouter les suffixes d'extension à la règle `bytecode`, à l'écriture comme à la lecture.
6. **Annexe** : les trois items du lot n'ont pas encore de ligne d'annexe.

## Écarts du réviseur

- **E-1** : deux leurres étaient mal construits au premier jet. LD-01 devenait transparent, et LE-07 détournait le flux trop tard. Je les ai refaits, et seuls les jets corrigés comptent.
- **E-2** : mon premier compte des octets 92 était faux. Je l'ai refait en octets.
- **E-3** : ma première attente visait un mauvais PID ; une seconde attente l'a remplacée.
- **E-4** : une commande a imprimé 4 lignes « note » de la sortie de xtask, en plus des lignes de verdict. Parmi elles, un AVIS de `docs/adr-0028`, qui n'est pas interdit ; aucune pièce de D.2 n'est concernée.
- **E-5** : j'ai lu trois fichiers du dépôt par des chemins relatifs. Ils ne sont pas interdits, la lecture était seule, et j'ai refait le contrôle sur ma copie.
- **E-6** : pour les premières lignes, j'avais relevé les PID de l'enveloppe `setsid` (30559 et 30560). Les vrais processus étaient 30562 et 30563, ce que consigne `NOTES.md`.
- **E-7** : une recherche `find` de `*.orig` et `*.rej` a parcouru les noms de fichiers de mes copies, y compris leur `docs/`. Elle portait sur les noms seuls, sans lire de contenu, et n'a rien trouvé.

**Interdits** : aucune pièce de D.2, aucun `*.jsonl`, aucun dossier interdit ouvert. `SHOGEN_S2_CAMPAGNE_CONTROL` n'a jamais été posée, et rien n'a été fait sur Pocket. Les copies lourdes sont supprimées et aucun processus ne reste.

## Fichiers produits

Tous sont dans `<scratchpad>/s2bis/outillage2/corr/revue/` :

- `RAPPORT-REVUE.md` : sha256 `f182c044a3e96682ccbd7c2ecadb9891c9816c8c3030f5edaee2ada2fc147d3d`. Il est hors de SHA256SUMS.
- `SHA256SUMS` : sha256 `1393ceac56e36390148f3ef9ae4b3922adc61db92263d596cc1a2387839188c9`, 262 entrées, toutes OK.
- `NOTES.md` (`97ff9f86…`).
- `remede/remede-C1-C3.diff` (`91a3f423…`).
- Résultats des mutants, dans `preuves/mutants/` :
  - `cc-resultats.txt` (`852ebdf2…`) ;
  - `d-resultats.txt` (`2e5ad749…`) ;
  - `e-resultats.txt` (`e0ba5387…`) ;
  - `f-resultats.txt` (`b24668cf…`) ;
  - `remede-resultats.txt` (`212ac5d5…`).
- `preuves/` : sorties des leurres, de la matrice (`py310-comparaison.txt`, `4b780d21…`) et de xtask (`verdicts.txt`, `8fb029b7…`).
- `outils/` et `mutants/` : scripts et spécifications des mutants.
- `leurres/` : scripts de R-1 aux octets inchangés, et `leurres_nonce.py` de la G2.
