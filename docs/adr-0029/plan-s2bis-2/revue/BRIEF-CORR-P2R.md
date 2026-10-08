# Brief — corrections du lot PLAN-S2BIS-2 après la G2 (C-1 à C-4) et refus non nommés

Worker `shogen-worker`, effort max. Tu n'as écrit aucun diff de ce lot et tu n'en as relu aucun. Dépôt `/home/user/shogen` en lecture seule (`git --no-optional-locks`), **aucune écriture git**. `date -u` avant toute date. Dossier : `<scratchpad>/s2bis/plan2/corr/` (scratchpad = `<scratchpad>`), `TMPDIR` dédié, `NOTES.md` tenu.

## Pièces
- Brief de génération `<scratchpad>/s2bis/plan2/code/BRIEF-P2R.md` (règles, interdits durs, commandes : **ils restent en vigueur**), contrat `docs/adr-0029/g0-plan2/` (G0, PERIMETRE-REDUIT, AVIS, PROPOSITION).
- Code : `<scratchpad>/s2bis/plan2/code/diffs/` (P2R-0a … P2R-5) et `snap/` ; rapport du générateur `RAPPORT-WORKER-P2R-transcrit.md`.
- Relecture : `<scratchpad>/s2bis/plan2/g2/G2-P2R-transcrit.md` (C-1 à C-4, avis sur Q-P2R et items) ; ses sondes et mutants dans `<scratchpad>/s2bis/plan2/g2/` (données : tu peux t'en inspirer, tu écris et prouves toi-même).
- Base : tête **e6657dc** (`git archive`, exclusions habituelles) ; les 9 diffs s'y appliquent en série sans retouche (mesuré par le réviseur).

## Adjudication de l'orchestrateur
- **C-1 à C-4 : à corriger**, avec les remèdes attendus du rapport (C-1 a à d : heredocs en `python3 -I -B`, environnement en liste fermée avec `PYTHONPYCACHEPREFIX` ou `-X pycache_prefix` vers un dossier neuf du travail, refus P2/epingle d'une entrée hors `SHA256SUMS` dans le dossier du lot, un test par vecteur S8, S9, S22 avec rouge montré, canal des faux scripts de `test_lancer.py` adapté, règle au README ; C-2 et C-3 : cas neufs qui tuent G-03, G-10, G-14, G-18, G-19, G-21, G-23, G-26 ; C-4 : commentaire aligné sur le code).
- **Q-P2R-3 : décidé.** Toute entrée hors grille, et plus généralement toute erreur de lecture, sort en refus nommé **sans aucune valeur de journal** à l'écran ni dans la trace (par exemple `P2/lecture`, code de sortie du §4 que tu motives).
- **SHOGEN-PLAN-S2BIS-2-REFUS-NON-NOMMES-1 : fermé dans ce lot** (déclencheur « avant l'épinglage », avis du réviseur) : aucun chemin de sortie non nommé ; chaque exception attendue rattrapée et nommée, sans valeur de journal ; test par chemin.
- Q-P2R-9 : corrigé par C-3 c. Les autres Q-P2R : tenus. PY310-1 et WERROR-IGNORE-1 : items maintenus. REPETITION-1 : ce n'est **pas** ton travail (il sera fait par le contre-contrôle, sur journaux synthétiques).

## Livrables
- Diffs corrigés, en série sur e6657dc, sous les mêmes noms (P2R-0a … P2R-5) quand un diff change, ou un diff neuf `P2R-6` si une correction ne trouve pas sa place ; chacun ≤ 200 lignes de code ajoutées ; `snap/` refait ; `SHA256SUMS` du lot (`scripts/plan-s2bis-2/SHA256SUMS`) recalculé et sa **nouvelle épingle** (sha256 de ce fichier) déclarée.
- Suite du lot verte sous 3.11 à 3.13 × `PYTHONHASHSEED` 0 et 1 en `-X dev -W error` (3.10 : échec d'import connu, PY310-1) ; DET-1 vert ; mutants de la G2 rejoués (les 8 vivants tués) et au moins 2 neufs par correction ; xtask : lignes de verdict seules.
- Rendu par message (ta valeur de retour), Gate 0 en tête : diffs (sha256, lignes ajoutées), tableau C-1 à C-4 et refus nommés, mutants, épingle neuve, écarts. Écris-le aussi dans `<scratchpad>/s2bis/plan2/corr/RAPPORT-CORRECTIONS.md`.

## Interdits (durs)
Aucun journal réel de S2 ni de S2-bis ; **jamais `lancer.sh` hors fixtures** ; tu ne poses jamais `SHOGEN_S2_CAMPAGNE_CONTROL`, même vide ; `docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, `docs/adr-0028/execution/` ; tout `*.jsonl` ; toute pièce de D.2 ; toute recherche récursive (grep -r, git grep, du, find large) sur `docs/`, le dépôt entier ou le scratchpad entier ; rien sur Pocket.
