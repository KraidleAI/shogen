# Brief — relecture G2 neuve à 100 % du lot PLAN-S2BIS-2 (diffs P2R-0a à P2R-5)

Tu es **réviseur G2 neuf** (`shogen-worker`, effort max). Tu n'as écrit aucun diff de ce lot et tu n'en as relu aucun.
- Dépôt `/home/user/shogen` en lecture seule (`git --no-optional-locks`), **aucune écriture git**. `date -u` avant toute date.
- Tu écris seulement dans `<scratchpad>/s2bis/plan2/g2/` (scratchpad = `<scratchpad>`). `TMPDIR` dédié, `NOTES.md` tenu (reprise depuis lui, jamais depuis un `.jsonl`).

## Base
- Tête **e6657dc** de `claude/compassionate-noether-szmdyj` (`git archive`, exclusions habituelles : `docs/rapports`, `docs/adr-0025`, `docs/adr-0028/monark-m009a`, `docs/adr-0028/execution`, `docs/15-*`, `docs/16-*`, `docs/pocket-report`).
- Les diffs ont été écrits sur la base 12ce67f ; ils ne créent que `scripts/plan-s2bis-2/`. Applique-les **en série** (P2R-0a, 0b, 1a, 1b, 2, 3, 4a, 4b, 5) sur e6657dc et dis s'ils s'appliquent sans retouche ; vérifie que rien de ce que le lot réemploie (`scripts/plan-s2bis/`, `docs/adr-0029/plan-s2bis/`, `scripts/sim-bis/`) n'a changé entre 12ce67f et e6657dc (sha256 chemin par chemin).

## Pièces
- Le code : `<scratchpad>/s2bis/plan2/code/diffs/*.diff`, `snap/`, `SHA256SUMS` (vérifie-le d'abord par `sha256sum -c`).
- Épingle déclarée avant la G2 : sha256 de `scripts/plan-s2bis-2/SHA256SUMS` = `a8bb826d2c8dc67f14aca13a722345ff974d72b876b7fe1c103db5a1aab40e08` (vérifie-la sur l'arbre après P2R-5).
- Contrat : `docs/adr-0029/g0-plan2/G0-PLAN-S2BIS-2.md`, `PERIMETRE-REDUIT.md` (§1 à §9), `AVIS.md`, `PROPOSITION.md` (E-P2-01 à E-P2-29) ; ADR-0029 et son ajout ; G0 de SIM-BIS `docs/adr-0029/g0-sim/G0-SIM-BIS.md`.
- Le rapport du générateur : `<scratchpad>/s2bis/plan2/code/RAPPORT-WORKER-P2R-transcrit.md` et `BRIEF-P2R.md`. **Fais d'abord ta propre lecture du contrat et du code**, puis lis le rapport et confronte-le.

## Contrôles
1. **Couverture.** Pour chaque exigence E-P2 et chaque refus du §4 du périmètre : où elle est tenue (fichier:ligne) et quel test la fige ; toute exigence sans test, ou test qui ne la fige pas vraiment.
2. **Ton propre estimateur.** Écris d'après le contrat seul (PERIMETRE-REDUIT et PROPOSITION, sans lire le code du lot) une sonde indépendante des sorties (masque FIV, intervalles, sections du bilan) et compare-la au lot sur les fixtures, plus des fixtures à toi (bords : bloc vide, une seule source, pannes adjacentes, D5, hors grille). Tout écart est un constat.
3. **Fidélité au réemploi.** Aucune formule de FIV, d'épisode, de pause, de quantile ni d'histogramme réécrite par le lot (§0 point 1) : tout passe par les fonctions épinglées de PLAN-S2BIS et par r1 extrait ; épingles sha256 justes et contrôlées à l'exécution.
4. **Lanceur.** `lancer.sh` lu, et éprouvé **sur fixtures seulement** : refus nommés, codes de sortie, identité, épingles, environnement hostile (variables, chemins, droits, fichiers manquants ou altérés). Tu ne le lances jamais sur un journal réel.
5. **Déterminisme.** Identité bit à bit sous 3.11 à 3.13 × `PYTHONHASHSEED` 0 et 1 ; et 3.10 : mesure toi-même si le `commun.py` épinglé tourne sous 3.10 (Q-P2R-1).
6. **Mutants.** Au moins vingt mutants à toi, à l'échelle du lot, classés par la commande de la suite du lot (`python3 -B -m unittest discover` dans `scripts/plan-s2bis-2`, ou la forme du périmètre), borne 300 s (au-delà FATAL).
7. **Questions du générateur.** Pour Q-P2R-1 à Q-P2R-12 : ton avis motivé (tenir, corriger, ou décision à prendre), sans trancher une valeur de valeur. Pour ses items proposés (PY310-1, WERROR-IGNORE-1, REPETITION-1, REFUS-NON-NOMMES-1) : justes ou non, déclencheur juste ou non. REPETITION-1 : dis qui doit répéter le lanceur à l'échelle et comment, sans jamais le lancer sur des données réelles.
8. **Forme.** ≤ 200 lignes de code ajoutées par diff, R-13, R-8, octets 92, ≤ 120 caractères, `-X dev -W error`, bibliothèque standard seule, aucun flottant dans `parametres.json`. `cargo --locked xtask verify` sur la copie : lignes de verdict seules (S-G9 `docs/17:70` connu).

## Exécution
`unshare -n` avec `lo` allumée (`<scratchpad>/s2bis/p1b/g2/travail/outils/isole.sh`) ; PID réels consignés ; pas de `pgrep -f` sur un motif large ; nettoyage des copies lourdes à la fin.

## Interdits (durs)
- **Aucun journal réel de S2 ni de S2-bis**, scellé ou copié : tu ne le lis pas, ne le listes pas, ne le cherches pas. **Jamais `lancer.sh` hors fixtures.**
- `docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, `docs/adr-0028/execution/` ; tout `*.jsonl` ; toute pièce de D.2 ; toute recherche récursive (grep -r, git grep, du, find large) sur `docs/`, le dépôt entier ou le scratchpad entier.

## Rendu
Rapport final par message (ta valeur de retour), en français : Gate 0 (identifiant exact du modèle) en tête ; verdict **ACCEPTE**, **ACCEPTE-AVEC-CORRECTIONS** (liste fermée C-1…, chacune avec fichier:ligne, preuve et remède attendu) ou **REFUSE** ; tableau de couverture ; écarts de l'estimateur ; mutants ; avis sur Q-P2R-1 à 12 et sur les items ; écarts de ta propre exécution ; fichiers produits (et leur `SHA256SUMS`).
