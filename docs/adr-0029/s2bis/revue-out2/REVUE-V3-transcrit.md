# Contre-contrôle et relecture G2 neuve — OUT2, vague 3 (transcrit)

> Transcription par l'orchestrateur le 2026-10-08 17:39:28 UTC du rapport rendu par l'agent a2e19320cea9d85a0 (workflow wf_ae64f812-f4d) ; contrôle FM-1.1 : fragments_l51_l14 = 0 ; modèle résolu au transcript : claude-opus-5-5. Texte de l'agent ci-dessous, sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

**Gate 0 : `claude-opus-5-5`** (identifiant tiré du contexte système ; l'effort `max` vient de la fiche, je ne peux pas le mesurer de l'intérieur). Horloge : de 16:43:05 à 17:38 UTC, le 2026-10-08.

## Verdict : ACCEPTE-AVEC-CORRECTIONS (C-1)

Le code des quatre diffs est juste. Il reste un seul défaut, un trou de test dans OUT-2j : la règle « PYTHONDEVMODE non vide → `-X dev` » n'est épinglée que pour « 1 » et « ». Un mutant non équivalent survit aux quatre lignes du job.

## Correction (liste fermée)

**C-1 — OUT-2j, `s2-harness/tests/test_oracle_record.py:705-707` et le « Rougit si » des l.699-700 ; règle dans `s2-harness/tools/oracle_record.py:109-112`.**
- **Preuve.**
  - Le mutant J09 remplace `bool(environ.get("PYTHONDEVMODE"))` par `== "1"`. Il reste VIVANT : runner 0, s2bis 0, S2 0, sim-bis 0, sous la matrice comme hors matrice.
  - Il n'est pas équivalent. Avec PYTHONDEVMODE=« 0 », la référence lancée sans `-I` voit `True ['default']` sous 3.10 à 3.13, et l'enfant `-I` de j aussi. Le mutant lui retire `-X dev`.
- **Remède, tests seulement.** Ajouter l'environnement `{"PYTHONDEVMODE": "0", "PYTHONWARNINGS": ""}` → `["-X", "dev"]`. C'est un sous-test : PLANCHER reste à 415.
  - Ma version, à réécrire et prouver par le correcteur : `remede/remede-J09.diff` (3 lignes ajoutées, 2 retirées ; sha256 `32eb0005…`).
  - Sur l'état final, elle donne 21 OK et la ligne S2 reste conforme (Ran = 415).
  - Avec J09, elle donne 1 FAIL et 0 ERROR, et la ligne S2 refuse.

## (a) Contre-contrôle

| | f (anciens tests) | g | j |
|---|---|---|---|
| D02 (C-1) | VIVANT | TUÉ, runner, I-01 | TUÉ, runner, I-01 |
| D04 (C-2) | VIVANT | TUÉ, runner, I-04 | TUÉ, runner, I-04 |
| D11 (C-3) | VIVANT | TUÉ, S2, 3 FAIL « ValueError not raised » | TUÉ, S2, 12 FAIL |
| F10 (C-3) | VIVANT | TUÉ, S2, 1 FAIL | TUÉ, S2, 4 FAIL |

- **C-4.** LE-11, LE-13 et LF-04 étaient conformes sur f ; sur j ils sont refusés et nommés, sous 3.10 à 3.13.
- **Textes.** Les l.31-32 et l.69 sont vraies ; F-15 tue H17. O-1 (l.34-37) et O-2 (l.4-5) sont écrits mot pour mot.
- **Racines actuelles.** Sur la base et sur j : `compiles` = [], `masques` = [], aucun lien sous s2-harness, s2bis et sim-bis. `bytecode` = [] sur les 871 et 872 fichiers de la copie. Rien n'est apparu après la matrice.

## (b) Relecture neuve (mes leurres, 3.10 à 3.13)

- **Vérificateur, 21 formes de code compilé.** Sur f, 10 sont exécutées, conforme. Sur j, toutes ont la sortie 1, un refus nommé, la suite n'est pas lancée.
  - Formes couvertes : `.pyc` sans source, `.pyo`, `.pyd`, et chaque suffixe d'EXTENSION_SUFFIXES (extension abi3 réelle compilée par gcc, `.so` nu compris).
  - Aussi : paquets, sous-dossiers, dossier caché, liens de dossier et de fichier, lien mort, double lien, racine, `__pycache__`.
  - Témoin conforme. Les trois lignes du job refusent en 0 à 1 s.
  - Seule exception : la casse (`.SO`, `.PYC`). Ces fichiers ne sont ni refusés ni importés sous Linux (O-1).
- **Enregistreur, fichiers compilés (r01 à r12).** Écrits par f, ils sont lus par j en refus (masque). Écrits par j, ils sont refusés à l'écriture et rien n'est écrit.
- **Commande `suite` (s01 à s12).** Formes testées : résumé forgé avec `os._exit`, `sys.exit`, trois variantes de fork, SIGTERM, atexit, flux réécrit, nonce deviné. Sur j, toutes donnent exit 1 à l'écriture et refus (exit) à la lecture ; quand l'outil nomme le motif, la lecture le cite. Seul s11 (nonce lu en mémoire, limite écrite) passe.
- **Drapeaux (d01 à d05).** Sur i, l'enfant `-I` voyait `False []`. Sur j, il voit la même chose que la référence lancée sans `-I`, dans les 5 environnements.
- **Rouges recontrôlés.** OUT-2i : 9 FAIL, 0 ERROR. OUT-2j : 5 FAIL, 0 ERROR. J'ai reproduit l'E-2 du correcteur (R-09 sous 3.13).
- **Leurres anciens rejoués sur j.** R-1, G2 et revue de la vague 2 gardent leur verdict. Seuls changent ceux que ce tour devait faire refuser : LE-11, LE-13, LF-04, LF-06.

## Mutants (72, Python 3.12, borne 300 s, classés runner, puis s2bis, S2, sim-bis)

| Campagne | N | Tués (runner / S2) | Vivants | FATAL |
|---|---|---|---|---|
| Contre-contrôle | 12 | 8 (4 / 4) | 4 sur f, témoins attendus | 0 |
| OUT-2g | 13 | 12 (10 / 2) | G01, équivalent (`atexit` est intégré) | 0 |
| OUT-2h | 18 | 18 (14 / 4) | 0 | 0 |
| OUT-2i | 15 | 15 (0 / 15) | 0 | 0 |
| OUT-2j | 12, plus 2 hors matrice | 11 (0 / 11) | **J09** ; hors matrice, J06s et J09s | 0 |

## Matrice, planchers, forme

- **Matrice (état j).** Sous 3.10 à 3.13 : runner 136 ok, s2bis 255, sim-bis 172. S2 donne Ran = 415, conforme, sous 3.11 à 3.13. Sous 3.10, le rouge connu PY310-1 garde les mêmes 80 entêtes et la même première ligne d'erreur qu'à la base. Aucune ligne « Exception ignored » ni « Warning ».
- **Planchers exacts.** `CAS` vaut 123 puis 136. `PLANCHER` vaut 413, 413, 414, 415. Les suites s2bis et sim-bis sont inchangées. Rien n'est retiré ni affaibli : 123 → 136 cas, 413 → 415 tests.
- **Forme.** Lignes ajoutées : 50, 160, 142 et 48. Aucune ligne de plus de 120 caractères, aucun marqueur R-13. Imports de la bibliothèque standard seulement. Octets 92 égaux de f à j.
- **`gates.yml`** est inchangé (`ee03d7b1…`) ; les trois motifs tombent sur l.220, l.196 et l.247.
- **xtask** : S-G1 à S-G8 VERT ; S-G9 ROUGE sur sa seule violation connue (`docs/17:70`) ; fmt, no_std et clippy VERT.
- **Dépôt.** La série s'applique aussi sur la tête actuelle `b46672b`, sans décalage. Aucune écriture git : `.git/HEAD` et `.git/index` sont inchangés.

## Confrontation avec le rapport du correcteur

- Je suis d'accord sur tout, à trois réserves près.
- **« 55 sur 55 tués »** est vrai pour ses mutants, mais aucun ne visait PYTHONDEVMODE strict (C-1).
- **« L'arbre entier compte 872 fichiers »** : c'est en fait la copie à 7 exclusions, alors que la règle `bytecode` porte sur toute l'extraction (item 1).
- **Coût de Q-10** : je l'ai mesuré (item 4) et rencontré moi-même (E-3).

## Observations

- **O-1, casse.** Sous win ou darwin, avec PYTHONCASEOK posé, un `aide.SO` serait importé sans être refusé. C'est inféré du code de CPython ([lu] `_bootstrap_external.py`), non mesurable ici. Remède possible : `f.lower().endswith(COMPILES)`.
- **O-2, CI hors matrice.** Hors matrice, J06s survit : les drapeaux des commandes de JOBS n'y sont épinglés par aucun test. C'est sans effet aujourd'hui, la CI ne posant pas ces variables.
- **O-3.** F-13 bute maintenant sur le refus avant lancement ; c'est F-15 qui épingle `pycache_prefix`.

## Mes écarts

- **E-1, E-4** : énumérations de noms sur ma copie entière, `docs/` compris. Noms seuls, comptés, non affichés.
- **E-2** : trois lignes « note » de xtask ont été affichées, dont une citation de `docs/adr-0028`. Aucune pièce de D.2.
- **E-3** : mon leurre lancé sans `-B` a pollué mes copies i et j avec un `__pycache__`. Le run S2 de i a été invalidé puis refait.
- **E-5** : quelques barres obliques inverses dans des commandes ; octets contrôlés.
- **E-6** : réservation `O_EXCL` ajoutée à `muter.py` ; aucun mutant joué deux fois.

Aucune pièce de D.2, aucun `*.jsonl`, variable scellée jamais posée, rien sur Pocket. Copies lourdes supprimées, aucun processus restant.

## Items à former

1. Faire mesurer par l'orchestrateur les 7 dossiers exclus : l'enregistreur refuse tout arbre qui porte un fichier compilé n'importe où.
2. Enregistrements écrits par un outil d'avant OUT-2i : 6 formes forgées sont lues conformes par j (s01, s03, s05, s07, s08, s09). Garde possible : exiger la commande AMORCE pour un run `suite`. C'est une décision.
3. La casse (O-1), si une plateforme insensible à la casse entre dans les jobs.
4. README de s2-harness, l.40 : dire `-B`, sinon le `__pycache__` laissé fait refuser la ligne S2.
5. Items 1 et 3 à 8 du correcteur : confirmés.

## Fichiers produits

Dans `<scratchpad>/s2bis/outillage2/corr3/revue/` :
- `RAPPORT-REVUE.md` (sha256 `5f66eb9846723551e94e2c5045e787058ff1c5e361ec2f113830d31ac0a1d0a8`)
- `NOTES.md` (`3e918f28…`)
- `remede/remede-J09.diff` (`32eb0005…`)
- `outils/`, `mutants/`, `preuves/` (dont `mutants/bilan.txt` et `xtask/verdicts.txt`), `leurres/`
- `SHA256SUMS` : 325 entrées, 0 écart, rapport compris ; sha256 `f0e683fea67894b05066c62c0f54daa0cfe8df538ced40a30bca26fa646ff7ea`
