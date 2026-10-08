# Rapport des corrections — OUT2, vague 2 (transcrit)

> Transcription par l'orchestrateur le 2026-10-08 14:56:51 UTC du rapport rendu par l'agent ab76d65253c08b69f (workflow wf_eabb8e95-e1a) ; contrôle FM-1.1 : fragments_l51_l14 = 0 ; modèle résolu au transcript : claude-opus-5-5. Texte de l'agent ci-dessous, sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Rapport du worker : corrections d'OUT-2 (C-1 à C-3), puis OUT-2d, OUT-2e et OUT-2f

**Gate 0 : `claude-opus-5-5`.** L'identifiant exact vient du contexte système. L'effort `max` vient de la fiche ; je ne peux pas le mesurer de l'intérieur.

- **Horloge** (`date -u`) : de 12:13:29 à 14:05:38 UTC, le 2026-10-08.
- **Base** : `e6657dcc3154bf2d35c69b84d9deae1385e702a7`, la base du brief. Copie faite par `git archive` avec les 7 exclusions.
  - Le dépôt n'a pas bougé : statut vide, et les sha256 de `.git/index` et de `.git/HEAD` sont identiques au début et à la fin.
  - Aucune écriture git.
- **Rattachement** [lu] : G0 COLLECTE (point 5 : 200 lignes ajoutées au plus par sous-lot) et ANNEXE-B, bloc B.73.
  - Les trois items du lot n'ont pas encore de ligne d'annexe. Il reste à les inscrire.

## Verdict

- **C-1, C-2 et C-3** sont corrigés dans OUT-2b, par les tests seulement. Les mutants B4, C4 et C7 de la G2 sont maintenant tués.
- **OUT-2d, OUT-2e et OUT-2f** ferment les trois items mesurés. Pour chacun, les tests sont écrits d'abord et leur rouge d'assertion est montré.
- **Mutants** : 55 sur 55 tués, aucun FATAL.
- **Matrice 3.10 à 3.13** : verte, sauf S2 sous 3.10, qui est le rouge connu PY310-1 avec les mêmes 80 noms que la base.
- **Fichiers inchangés** : `gates.yml` (ses lignes et les trois motifs du brief tiennent tels quels), et les suites s2bis et sim-bis.
- **Deux leurres changent de verdict** sans que le lot le vise. Les deux sont expliqués plus bas (E-4 et E-5).

## Diffs finaux

La série est vérifiée : base + OUT-2a … OUT-2f redonne l'état final par `patch -p1 -F0`.

| Diff | Lignes ajoutées (dont .py) / retirées | sha256 |
|---|---|---|
| OUT-2a (inchangé) | 73 (73) / 35 | `33a25a593aa225b7ad4c44043953bdab395863ca566d20789d98be551b3809e8` |
| **OUT-2b corrigé** (remplace ea802333) | 102 (102) / 5 | `984d96677ddc17787d9c634a6219d91cf5f3e3d08893ed2574e2716219f16e56` |
| OUT-2c (inchangé) | 35 (4, plus 31 dans le README) / 1 | `6ef56a8c48c9a9e8e5b51f784da51a36e583a86f2ea16fe28bf79fc860fcd20d` |
| **OUT-2d** (SCRIPT-MASQUE-1) | 152 (152) / 19 | `010192a8c469677cd36dfc7bfc25e69500cb250d8fc63c530033745ab044881c` |
| **OUT-2e** (RESUME-FORGE-1) | 126 (126) / 10 | `ce7c500f1cc439d5e74bebb78e92ec77be946e8768d6cd358154faa0fb5c847b` |
| **OUT-2f** (MASQUES-LECTURE-1, texte 3.10) | 54 (52, plus 2 dans le README) / 10 | `589b704ab4ad98f97da913a29bb747d0a089d0f2d0396c4c31d7f9dc23191047` |

## C-1 à C-3

| Correction | Ce qui change (état OUT-2b corrigé) | Rouge d'assertion sur l'état corrigé | Avec l'ancien test | Campagne |
|---|---|---|---|---|
| C-1 | Cas M-05 du runner (l.278-280) : `json.abi3.so` ajouté, attendu écrit à la main | G2-B4 : « ÉCHEC M-05 … écart » | vivant, 105 ok | tué par le runner |
| C-2 | Test de l'enregistreur (l.520-522) : `json.abi3.so` ajouté, et la règle du dernier point dans « Rougit si » | G2-C4 : « Lists differ » | vivant | tué par S2 |
| C-3 | Même test (l.508-509) : appel `("suite-s2bis", "suite")` attendu en refus, et l'ordre des commandes dans « Rougit si » | G2-C7 : « ValueError not raised » | vivant | tué par S2 |

## Choix

### Q-5 (OUT-2d) : isolement des scripts de preuve

**Ce que `-I` change, mesuré sous 3.10 à 3.13.** `-I` implique `-E`.
- Sont ignorés : `PYTHONDEVMODE`, `PYTHONWARNINGS`, `PYTHONHASHSEED` (le hachage devient aléatoire), `PYTHONPATH` et `PYTHONIOENCODING`.
- Les drapeaux `-X dev -W error` passés en ligne de commande restent tenus.
- Les variables restent dans `os.environ`, et un enfant lancé sans `-I` les applique.

**Runner et vérificateur : isolement fait dans le script.** C'est la forme équivalente motivée.
- Le script importe d'abord `os` et `sys` (mesuré : ils sont déjà chargés au démarrage), puis retire son propre dossier de `sys.path` avant tout autre import.
- Cela couvre la ligne du job, un lancement à la main, le serveur du runner et ses copies.
- J'ai écarté `-I` dans `gates.yml` pour trois raisons :
  - les motifs du brief et la forme `python3 -B …` restent intacts ;
  - le témoin L0 de R-1 garde son verdict ;
  - il n'y a pas d'effet `-E` sur la matrice.

**Serveur du runner et enregistreur : la source, pas le cache.** Le vérificateur est exécuté depuis sa source (`compile` puis `exec`), jamais depuis un `.pyc` de `__pycache__`.
- Mesure D-R4 : un `.pyc` posé dans `enforcement/__pycache__`, sans contrôle de la source, était exécuté par le serveur.

**Enregistreur : `-I` pour toute commande autre que `suite`.** Ces commandes ignorent donc l'environnement consigné ; la docstring le dit. La sortie de production est écrite en octets UTF-8, donc elle n'est pas affectée.

**Refus nommés là où l'isolement ne suffit pas (mesuré).**
- Une racine `s2-harness` masquée est refusée pour toute commande qui y tourne (D-P3 : un `dataclasses.py` posé là est importé même en `-I`).
- Un `.pyc` committé dans l'extraction est refusé (D-P4 et D-U1).

### Q-6 (OUT-2e) : un amorçage fourni par le vérificateur

AMORCE est passé par `-c` et reproduit `-m unittest` :
- la racine de la suite en tête, en chemin absolu ;
- le même `sys.argv[0]` ;
- les codes de sortie de unittest.

Fonctionnement :
- Après `import unittest`, `sys.pycache_prefix` est pointé vers un dossier vide (cas F-13).
- Au retour de `TextTestRunner.run`, AMORCE écrit le compte réel avec un nonce : lancés, échecs, erreurs, sautés, échecs attendus, succès inattendus.
- Le nonce vient de `secrets` et passe sur stdin. Le compte va dans un fichier neuf, en mode `x`.
- `accord` refuse, en le nommant, un compte absent, sans nonce, illisible, ou en désaccord avec le résumé.

**Limite**, écrite dans la docstring : un test écrit pour viser ce mécanisme peut lire le nonce dans la mémoire du processus. Mesuré : le leurre E-F3 reste conforme. La lecture humaine du diff des tests reste nécessaire.

### Q-7 (OUT-2f) : contrôle « masque » à la lecture

- Le contrôle est placé après celui des sorties.
- Il refuse un `tree.sha256` qui porte un module standard à la racine de la suite d'un run lancé, ou un `.pyc` n'importe où.
- Les règles `masquants` et `bytecode` sont les mêmes qu'à l'écriture.
- **Limite** : le contrôle juge l'arbre, pas la commande.

### Q-8 : la limite sous 3.9

- Texte seul, sans élargir le lot : `s2-harness/README.md` (l.17-18) et la docstring de `masquants` disent « ≥ 3.10 pour l'enregistreur, sa suite et le vérificateur ».
- Sous 3.9, le refus devient une `AttributeError` : échec fermé mais non nommé [inféré : 3.9 est absent de l'hôte].

## Leurres

| Leurre | Avant | Final |
|---|---|---|
| R-1 runner (V0 à D7) | base : D7 = 0 | identique à l'état c, et D7 = 1, refus nommé (nonce) |
| R-1 enregistreur (L0 à L3) | — | identiques à la base |
| G2 nonce N1 à N5 | refusés | inchangés, refusés |
| G2 nonce N6 (octets inchangés) | 0 | **1**, voir E-5 |
| G2 N6' (N6 adapté) | — | 0, la limite reste la même |
| G2 masque, sous 3.10 à 3.13 | — | identiques |
| G2 enregistreur E1 à E6 | — | identiques |
| G2 enregistreur **E7** | lu conforme | **refus (masque)** |
| Les miens, D-S\*, D-R\*, D-U1 | base ou état c : forgés ou importés | refusés ou non importés, sous 3.10 à 3.13 |
| D-P5 et D-P6 (passent par l'enregistreur) | enregistrement écrit | refus nommé avant tout run |
| E-F1, E-F2, E-U1 | conformes | 1, refus nommé |
| E-F3 | conforme | conforme : c'est la limite écrite |

## Mutants

Python 3.12, borne de 300 s par commande, classés par runner, puis ligne s2bis, puis S2, selon SHOGEN-MUT-FATAL-1.

| Diff | Mutants | Tués | Vivants | FATAL |
|---|---|---|---|---|
| OUT-2b corrigé (ses mutants, plus G2-B4, G2-C4, G2-C7) | 17 | 17 | 0 | 0 |
| OUT-2d | 15 | 15 | 0 | 0 |
| OUT-2e | 14 | 14 | 0 | 0 |
| OUT-2f | 9 | 9 | 0 | 0 |

## Matrice (`-X dev -W error`, réseau isolé)

| Python | runner | s2bis | sim-bis | S2 |
|---|---|---|---|---|
| 3.10 | 123 ok | 255 | 172 | rouge PY310-1 : 77 FAIL + 3 ERROR, 80 noms identiques à la base ; les tests neufs passent |
| 3.11, 3.12, 3.13 | 123 ok | 255 | 172 | Ran = 413, conforme |

Aucune ligne « Exception ignored » ni « Warning » dans les sorties.

## Planchers

- `CAS` du runner : 105, puis 109 après OUT-2d, puis 123 après OUT-2e.
- `PLANCHER` de S2 : 408, puis 412 après OUT-2d, puis 413 après OUT-2f.
- s2bis (255) et sim-bis (172) ne changent pas, donc pas de section METRIQUES.

## Forme et xtask

- Forme : aucune ligne de plus de 120 caractères, aucun marqueur R-13, aucune dépendance hors bibliothèque standard (R-8).
- Octets 92 : le compte par fichier est inchangé.
- xtask : S-G1 à S-G8, fmt, no_std et clippy VERT. S-G9 est ROUGE sur sa seule violation connue, `docs/17-modele-de-menace.md:70`.

## Écarts

- **E-1** : une mesure a tourné sans `TMPDIR` dédié ; son dossier temporaire a été nettoyé.
- **E-2** : la première forme des tests S2 d'OUT-2d était rouge par ERROR et non par assertion. Corrigée avant le rouge retenu.
- **E-3** : AMORCE posait d'abord `pycache_prefix` avant `import unittest`, ce qui faisait passer le runner à 19 s. Après correction, 8 s.
- **E-4** : le cas I-04 exigeait une sortie 1. Il faisait donc échouer les leurres D6a et D-CAPTURE de R-1, dont l'enveloppe neutralise `__main__`.
  - I-04 ne juge maintenant que la marque, et il est lancé avec stdin à `DEVNULL`.
  - D6a et D-CAPTURE sont revenus à 0.
- **E-5** : N6 sort en 1. Les cas F-10 à F-12 lisent le stderr du serveur, et N6 n'imite que le motif de M-01.
  - N6', qui imite aussi ces motifs, sort en 0 : la limite reste celle écrite.
- **E-6** : la règle `bytecode` est réduite à « `.pyc` ».
- **E-7** : sim-bis tourne avec `GIT_DIR` en lecture seule.
- **E-8** : un octet 92 « ajouté » se trouve sur une ligne modifiée qui le portait déjà. Le test `test_journaux…` exige maintenant `-I`.
- **E-9** : les mutants de la G2 sont renommés G2-B4, G2-C4 et G2-C7.
- **E-10** : les PID des lignes du job sur les états e et f n'ont pas été relevés ; la matrice finale les refait avec PID.

## Items à former

1. **SHOGEN-S2BIS-ENREG-SUITE-COMPTE-1** [mesuré]. La commande `suite` de l'enregistreur consigne le code de sortie de `-m unittest`, sans AMORCE.
   - Un résumé forgé suivi de `os._exit(0)` donne « exit 0 », et la lecture dit conforme.
   - La même suite passée par `suite-s2bis` est refusée.
2. **SHOGEN-S2BIS-ENREG-DRAPEAUX-1** [mesuré pour `-I`]. Les enfants `-I` de l'enregistreur ne voient ni `PYTHONDEVMODE` ni `PYTHONWARNINGS` sous la matrice.
3. **Limite d'OUT-2f** [inféré]. Un run de production sans `-I`, écrit par un outil d'avant OUT-2d, n'est pas refusé à la lecture si `tools/` porte un masque.
4. **Limites écrites, à garder visibles** : un code qui vise le mécanisme peut lire le nonce (E-F3, N6') ; sous 3.9, l'échec est fermé mais non nommé.

## Journal G1 (résumé ; le détail est dans le rapport écrit et dans `NOTES.md`)

- **Pièces de D.2, `*.jsonl`, dossiers interdits** : aucun ouvert.
- **Recherches récursives** : restées bornées à la copie.
- **`SHOGEN_S2_CAMPAGNE_CONTROL`** : jamais posée.
- **Pocket** : rien.
- **Copies lourdes** : supprimées.

Le dossier `<scratchpad>/s2bis/outillage2/corr/` contient :
- RAPPORT-CORRECTIONS.md
- diffs/ (les six diffs : OUT-2a à OUT-2f)
- SHA256SUMS (267 entrées, sha256 `237982bcacfa0142a7f457a309ceaab1bdfb909c9df29db6e3ef1d2bc80407b1`, tout le dossier sauf le rapport)
- NOTES.md
- livrables/
- preuves/
- outils/
