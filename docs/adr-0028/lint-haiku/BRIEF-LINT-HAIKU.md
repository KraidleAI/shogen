# Brief — lot LINT-HAIKU (G1) : `claude-haiku-5-5` dans la liste blanche du lint R-1

Worker `shogen-worker`, effort max. Dépôt `/home/user/shogen` en lecture seule (`git --no-optional-locks`), **aucune écriture git**. `date -u` avant toute date. Dossier : `<scratchpad>/lot-haiku/` (scratchpad = `<scratchpad>`), `TMPDIR` dédié, `NOTES.md` tenu.

## Contrat
- **Ta spécification : `<scratchpad>/lot-haiku/G0-LINT-HAIKU.md`** (exigences E-LH-1 à E-LH-4, cas, mutants, critères de sortie).
- Base : tête **e6657dc** (`git archive`, exclusions habituelles : `docs/rapports`, `docs/adr-0025`, `docs/adr-0028/monark-m009a`, `docs/adr-0028/execution`, `docs/15-*`, `docs/16-*`, `docs/pocket-report`).
- Lis : `enforcement/lint-model-pinning.sh`, `enforcement/tests/run-fixtures-model-pinning.sh`, ses fixtures `enforcement/tests/fixtures/model-pinning/`, `CLAUDE.md` point 7, le bloc B.76 de `docs/adr-0028/ANNEXE-B-items.md` (fin du fichier), la fiche brouillon `<scratchpad>/lot-haiku/shogen-extracteur.md`.

## Livrables
- `diffs/LH-1.diff` (lint et runner, ≤ 200 lignes de code ajoutées) et `diffs/LH-2.diff` (la fiche `.claude/agents/shogen-extracteur.md`, corrigée si besoin), appliqués en série sur e6657dc.
- Runner du lint vert, lint de l'arbre (copie + LH-1 + LH-2) vert, `cargo --locked xtask verify` sur la copie (lignes de verdict seules).
- Rouge montré avant le code ; mutants classés ; `SHA256SUMS`, `NOTES.md`, journal G1 bref.
- Tu ne crées jamais de fichier sous un `.claude/agents/` du dépôt réel (Claude Code le chargerait) : seulement dans tes copies sous `TMPDIR`.

## Règles
R-13, R-8, octets 92 comptés, lignes ≤ 120 caractères ; l'identifiant banni reste construit à l'exécution (jamais son littéral). Bibliothèque standard et bash seuls.

## Interdits
`docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, `docs/adr-0028/execution/` ; tout `*.jsonl` ; toute pièce de D.2 ; toute recherche récursive (grep -r, git grep, du, find large) sur `docs/`, le dépôt entier ou le scratchpad entier.

## Rendu
Rapport final par message (ta valeur de retour), court, en français : Gate 0 en tête, diffs (sha256, lignes ajoutées), tableau des cas neufs et des mutants, écarts, questions.
