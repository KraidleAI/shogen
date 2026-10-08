# Brief — LINT-HAIKU, troisième tour

Worker `shogen-worker`, effort max. Mêmes règles, base (e6657dc) et interdits que `<scratchpad>/lot-haiku/BRIEF-LINT-HAIKU.md` (scratchpad = `<scratchpad>`). Tu écris dans `<scratchpad>/lot-haiku/corr3/`.

- Lis le G0 `<scratchpad>/lot-haiku/G0-LINT-HAIKU.md` **en entier, ajouts datés §6 et §7 compris** (le §7 fixe : Haiku refusé partout dans les réglages JSON, `R-1/role` ; admis seulement en `model` de frontmatter ; contrôle du commentaire limité à l'UTF-8 invalide ; C-1 à C-3 de la revue).
- Pièces : diffs de la vague 2 `<scratchpad>/lot-haiku/corr/diffs/` et rapport `corr/RAPPORT-CORRECTIONS-transcrit.md` ; revue `corr/REVUE-transcrit.md` et son remède `corr/revue/tmp/proposition/` (donnée : tu écris et prouves toi-même).
- Livrables dans `corr3/` : `diffs/LH-1.diff` et `diffs/LH-2.diff` refaits sur e6657dc (≤ 200 lignes de code ajoutées chacun) ; rouge d'assertion montré pour chaque cas neuf ou inversé ; mutants de la revue (M-01 à M-16) et au moins 6 neufs (dont : un réglage JSON qui admet haiku sous une clé, un commentaire non ASCII valide refusé à tort) ; runner vert sous POSIX, C.UTF-8 et les locales de la revue ; lint de l'arbre (copie + diffs) vert ; `SHA256SUMS` couvrant aussi ton rapport ; `NOTES.md`. Tu ne crées jamais de fichier sous un `.claude/` du dépôt réel.
- Rendu par message (ta valeur de retour), Gate 0 en tête ; écris-le aussi dans `corr3/RAPPORT-CORRECTIONS.md`.
