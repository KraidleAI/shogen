# Second contre-contrôle de SIM-INTEG (CONFORME) (transcrit)

> Transcription par l'orchestrateur le 2026-10-08 20:46:23 UTC du texte écrit par l'agent a059fa5f14a203e0a dans `<scratchpad>/s2bis/sim5/g2/cc2/RAPPORT-CC2.md` (sha256 ce24ba55…) ; contrôle FM-1.1 de son transcript : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte de l'agent ci-dessous, sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Contre-contrôle 2 de SIM-INTEG : CC-1 et CC-2

**Gate 0 : modèle `claude-opus-5-5`** (réviseur de la G2 et du premier contre-contrôle de ce lot, effort max ; je n'ai
écrit aucune correction). Contre-contrôle du 2026-10-08, de 19:57:46 à 20:22 UTC (`date -u`).

## Verdict : CONFORME (liste fermée vide)

- **Tests seulement.** CC-1 et CC-2 sont corrigées par des tests seulement. A, B, C, E et F sont inchangés à l'octet ;
  aucune ligne de production ne change ; le plancher reste 194.
- **Mutants visés tués**, sous la commande du job :
  - MR-18 est tué par `test_fiv_unites_indefini` seul (« Refus not raised ») ;
  - MG-14 est tué par `test_croisement_q_si_9` seul (« TypeError not raised »).
- **Campagnes complètes.** Mes 26 mutants de la G2 et mes 16 mutants de SB-15G sont tous tués sur l'état final.
- **Série, matrice, portes et forme** : vertes.

## Contrôles

| contrôle | résultat |
|---|---|
| SHA256SUMS de sim5 | 3fa444ec… = le message ; 910 lignes ; `sha256sum -c` 910 OK ; aucun `jsonl` ; mes `g2/` et `g2/cc/` intacts (0 non-OK chacun) |
| diffs A, B, C, E, F | inchangés à l'octet : 483b6963…, 15209f3e…, 652a5c8f…, e59aeb80…, 89b8ae90…, égaux à ceux de mon contre-contrôle |
| diffs D et G | D b568584f…, G 87085b1b… ; les anciens (`avant-cc/`) valent 35eeb496… et 563ba755…, ceux de mon contre-contrôle. Différences : docstring et un cas de test dans `test_fiv_unites_indefini` (D) ; docstring et `assertRaises(TypeError)` dans `test_croisement_q_si_9` (G) ; en-têtes d'index et de bloc (`index`, `@@`) |
| production | série d'avant contre série neuve, étape par étape (e15a à e15g) : seul `tests/test_calibration.py` diffère (D à G) ; 0 fichier de production différent ; `gates.yml` identique, planchers 174, 177, 179, 181, 185, 193, 194 inchangés |
| application | A à G : 7/7 sur b46672b et 7/7 sur 5cfe746 (HEAD, `git status` vide) ; état final identique sur les deux bases (`scripts/sim-bis`, `gates.yml`) ; égal aux `etapes/e15a…e15g` du générateur |
| base courante | entre b46672b et 5cfe746 : `scripts/sim-bis`, `gates.yml`, `scripts/plan-s2bis(-2)` et `docs/adr-0029/plan-s2bis(-2)` inchangés |
| CC-2 | `tests/test_calibration.py:167`, l.179 : la ligne versée de binance à ℓ = 1 (n = 24 585, K = 372, γ̂₀ et cv recopiés, donc cohérents) est réécrite FIV « - », σ̂²_bloc = 0 ; refus attendu `CALIB/coherence`, par la seule règle « - » si et seulement si γ̂₀ = 0. Le cas K = 3 est requalifié dans la docstring (γ̂₀ écrit « 0 », refusé par le contrôle de γ̂₀) |
| CC-1 | `tests/test_calibration.py:233` : `calibration.charger_unites(PRM, environ={})` lève `TypeError` |
| tueurs exacts (suite directe `-v`, mutant appliqué) | MR-18 : seul FAIL `test_fiv_unites_indefini`, « Refus not raised » ; MG-14 : seul FAIL `test_croisement_q_si_9`, « TypeError not raised » ; Ran 194 |
| commande du job (plancher, borne 300 s) | MR-18 TUÉ à e15d (181) et à e15g (194) ; MG-14 TUÉ à e15g |
| mes 26 mutants de la G2 à e15g | 26 TUÉS, 0 vivant, 0 FATAL ; témoins verts |
| mes 16 mutants de SB-15G à e15g | 16 TUÉS, 0 vivant, 0 FATAL ; témoins verts |
| rouges rejoués (ébauches du générateur) | D : 2 FAIL / 0 ERROR (Ran 181) ; G : 1 FAIL / 0 ERROR (Ran 194) |
| jobs à chaque étape (`isole.sh`) | 174, 177, 179, 181, 185, 193, 194 : tous conformes ; à 193, le job refuse l'état final (Ran 194 > 193) |
| matrice stricte | Python 3.10.20, 3.11.15, 3.12.3, 3.13.14 × `PYTHONHASHSEED` 3 et 4 099 : 8/8, Ran 194, OK, 0 « Exception ignored », 0 « Warning » |
| forme | code ajouté : A 66, B 152, C 68, D 152, E 187, F 149, G 62 (au plus 200) ; 0 octet 92 dans les diffs et dans `scripts/sim-bis` final ; R-13 0 ; Python : 0 ligne de plus de 120 caractères ; aucun import ajouté par D ni G |

**Portes :**

| porte | état final, série sur b46672b | état final, série sur 5cfe746 |
|---|---|---|
| runner | 97 ok | 136 ok |
| sim-bis | 194 conforme | 194 conforme |
| s2bis | 255 conforme | 255 conforme |
| s2-harness | 407 conforme | 415 conforme |
| hooks / model-pinning / lint R-1 / secrets | 54 / 95 / OK / 147 | non relancé |
| R-13 et `gate-secrets --tree` | 0 constat, OK (26 fichiers) | non relancé |
| `cargo --locked xtask verify` (`unshare -n`) | verdicts égaux à ceux de la base : S-G1 à S-G8, fmt, no_std et clippy VERT ; S-G9 ROUGE, 1 violation (`docs/17-modele-de-menace.md:70`, connue) ; section S-G9 identique | non relancé |

## Observations

- **E-14 du générateur :** il a lu et exécuté mes `mutants_g2.py` (6903583c…) et `mutants_cc.py` (c7d77b8c…), empreintes
  égales. Il déclare n'avoir pas ouvert mon `test_cc.py`. Ses deux cas de test diffèrent des miens, par la ligne de
  binance à ℓ = 1 et par l'emplacement dans les tests existants.
- **Chemin vu dans xtask :** la section S-G9 nomme aussi un chemin sous `docs/rapports/`. Je n'en ai vu que le chemin ; il
  n'a pas été ouvert.

## Écarts

- **E-CC2-1 :** mon script de portes, dérivé de celui du premier contre-contrôle, a écrit son journal sous le nom
  `portes_cc.txt` dans `cc2/journal/`. Il a été renommé `portes_cc2.txt` ; contenu inchangé.
- **E-CC2-2 :** une attente d'avant-plan a dépassé la borne de 10 min et l'outil l'a passée en arrière-plan. Je l'ai
  arrêtée : elle attendait le nom de fichier de l'écart E-CC2-1. Aucun résultat n'en dépend.
- **E-CC2-3 :** pour l'adaptateur `oracle_r1`, un clone nu en lecture seule a été fait dans `cc2/tmp`, puis supprimé.
  Aucune écriture git dans `/home/user/shogen` (HEAD 5cfe746, `git status` vide).
- **Interdits :** aucun journal, aucun `*.jsonl`, aucune pièce de D.2. `SHOGEN_S2_CAMPAGNE_CONTROL` n'a jamais été posée.
  Aucune énumération récursive de `docs/`, du dépôt ou du scratchpad. Les copies lourdes sont supprimées.

## Journal de provenance (G1)

**[lu] :** §13 de `RAPPORT-GENERATEUR.md` (l.299-fin) ; les différences entre les diffs D et G anciens (`avant-cc/`) et
neufs, en entier.

**Commandes et sorties**, dans `cc2/journal/` :
- `mr18_e15d.txt`, `mr_e15g.txt`, `mg_e15g.txt`, `tueurs_cc2.out` ;
- `rouge_cc2.out`, `jobs_cc2.out`, `strict_cc2.out`, `portes_cc2.txt`, `xtask-verdicts-*.txt`.

Les tâches longues ont été lancées détachées, leur fin constatée.
