# Brief — corrections du lot LINT-HAIKU (après la G2)

Worker `shogen-worker`, effort max. Mêmes règles, base et interdits que `<scratchpad>/lot-haiku/BRIEF-LINT-HAIKU.md` (scratchpad = `<scratchpad>`). Tu écris dans `<scratchpad>/lot-haiku/corr/`.

- Lis le G0 `<scratchpad>/lot-haiku/G0-LINT-HAIKU.md` **en entier, ajout daté du §6 compris** (il corrige E-LH-1 et ajoute E-LH-5), et la relecture `<scratchpad>/lot-haiku/G2-LINT-HAIKU-transcrit.md` (C-1 à C-3, items I-1 et I-4). Le remède proposé par le réviseur (`<scratchpad>/lot-haiku/g2/tmp/proposition/`) est une donnée : tu peux t'en inspirer, mais tu écris et tu prouves toi-même.
- Livrables : `corr/diffs/LH-1.diff` et `corr/diffs/LH-2.diff` refaits sur e6657dc (lint, runner, fiche), chacun ≤ 200 lignes de code ajoutées ; rouge d'assertion montré pour chaque cas neuf (T-100 inversé, T-108 à T-110, cas de locale) ; au moins 6 mutants neufs (dont : advisorModel qui admet haiku, locale non fixée, casse de la première lettre, NBSP, U+200B), plus le rejeu des campagnes précédentes ; runner vert sous POSIX et sous C.UTF-8 ; lint de l'arbre (copie + diffs) vert ; `SHA256SUMS`, `NOTES.md`.
- Rendu par message (ta valeur de retour) : Gate 0 en tête, diffs (sha256, lignes), tableau C-1 à C-3 et E-LH-1 corrigé, E-LH-5, mutants, écarts.
