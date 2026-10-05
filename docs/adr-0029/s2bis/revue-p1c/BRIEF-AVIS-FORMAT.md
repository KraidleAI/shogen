# Brief — avis de l'advisor : lettres à écrire au FORMAT des journaux de S2-bis, après le banc de concordance des deux lecteurs

Tu es l'advisor (`shogen-advisor`, R-26). Tu n'agis pas.
- Écris seulement `<scratchpad>/s2bis/rb18/g2/AVIS-FORMAT.md`.
- Rends aussi un résumé par message.

**But du projet**, à garder présent : faire de Shōgen un standard institutionnel vendable. La définition d'une ligne intègre et d'une rupture est au cœur de ce qu'un tiers peut recalculer : elle doit être sans ambiguïté et la même chez l'écrivain et chez les deux lecteurs.

## Pièces
- Relecture G2 avec banc de concordance : `…/rb18/g2/G2-RB18-transcrit.md`.
  - Ses §4 et §6 : 10 099 journaux, 973 discordances en 14 classes.
  - Les lettres C-1 à C-5 qu'il propose. Une contre-épreuve alignée sur ces lettres donne 0 discordance.
- FORMAT : `docs/adr-0029/s2bis/FORMAT-JOURNAUX-S2BIS.md`, état commis.
- Le lot P1 tranche C, en correction (`…/s2bis/cb18/`), le retouche aussi : §1.2 (640 chiffres, `JOURNAL/entier`), §6.1, §7.1, §7.2, §11.5, §12, §14. Son rapport est dans `…/cb18/g2/RAPPORT-WORKER-CB18-transcrit.md`, et sa G2 dans `…/cb18/g2/G2-CB18-transcrit.md`.
- AVIS du G0 COLLECTE : `docs/adr-0029/g0-collecte/AVIS.md`, Q-R-03.
- Avis du recalcul : `…/s2bis/rb1/g2/AVIS-RB-T1.md`, Q-RB-9 et Q-RB-10.
- ADR-0029.

## Ce qui est demandé
Pour chacune des lettres C-1 à C-5 :
- **Adoptée**, **modifiée** (donne la lettre exacte) ou **rejetée** ;
- un motif sourcé ;
- l'effet sur l'écrivain, sur RB-1 et sur RB-18.

Points précis :
- **C-3, la lecture la plus sévère** : à toute rupture, aucune queue en attente n'est réputée déclarée. Est-ce le bon choix pour un recalcul tiers ? Comment s'articule-t-il avec SHOGEN-S2BIS-RUPTURE-PORTEE-1 (annexe B, B.65) ?
- **C-4, la borne d'imbrication** : faut-il N = 64 ? D'où vient la mesure ? Le refus se fait-il à l'écriture ?
- **C-1 : le code de refus de l'écrivain.** Le lot P1-C a écrit `JOURNAL/entier`, alors que le réviseur propose `JOURNAL/type`. Lequel garder ?
- **C-5** : la grammaire des noms de fichiers, et le dossier vide refusé.

Dis aussi :
- quel lot porte chaque changement : le FORMAT et l'écrivain dans P1-C, RB-1 en correction, RB-18 en correction ;
- dans quel ordre les faire, pour que le critère « 0 discordance » (PROPOSITION l.551) soit atteint sans travail perdu.

## Interdits
- `docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, `docs/adr-0028/execution/` ;
- tout `*.jsonl` ;
- toute pièce de D.2 ;
- aucune recherche récursive, y compris par Glob, sur `docs/`, sur le dépôt ou sur le scratchpad.

Gate 0 : l'identifiant exact du modèle et l'effort, en tête.
