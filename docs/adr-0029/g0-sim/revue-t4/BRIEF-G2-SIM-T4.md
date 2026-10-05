# Brief — relecture G2 du lot SIM-BIS, tranche 4 (SB-9A à SB-14B : variante, estimateur FIV, adaptateur r1)

Tu es **réviseur G2 neuf** (`shogen-worker`). Tu n'as rien écrit de ce lot.

- Le dépôt `/home/user/shogen` est en lecture seule : **aucune opération git en écriture**. Utilise `git --no-optional-locks`.
- Lis `date -u` avant toute date.
- Tu écris seulement dans `<scratchpad>/s2bis/sim4/g2/`. Rapport par message.
- Tiens un fichier `NOTES.md` dans ton dossier. Après un compactage ou un redémarrage, reprends depuis lui, jamais depuis un `.jsonl`.

## Pièces

- Sept diffs, dans l'ordre : `…/sim4/diffs/SB-9A.diff`, SB-9B, SB-10A, SB-10B, SB-10C, SB-14A, SB-14B (empreintes `…/sim4/SHA256SUMS`).
- Rapport du worker transcrit : `…/sim4/g2/RAPPORT-WORKER-SIM-T4-transcrit.md`.
- Brief du worker : `…/sim4/BRIEF-SIM-T4.md`.
- Outils et preuves du worker : `…/sim4/outils/`, `…/sim4/journal/`.

**Base** : tête 5f99ab5, puis les sept diffs.

## Contrat

- G0 `docs/adr-0029/g0-sim/G0-SIM-BIS.md`, avec ses ajouts datés ; il s'appuie sur `PROPOSITION.md` corrigée par `AVIS.md`.
- ADR-0029.
- Pièces de revue `docs/adr-0029/g0-sim/revue-t1/` à `revue-t3/`.
- Code de f35a70c, lu par `git --no-optional-locks show f35a70c:<chemin>`.

Un avis de l'advisor sur les treize questions Q-T4-1 à Q-T4-13 et sur le constat du point 9 est demandé en parallèle. Toi, tu juges la fidélité au G0 et la justesse du code.

## Contrôles

1. **Série.**
   - Les diffs s'appliquent sur la tête ; chacun ajoute au plus 200 lignes de code.
   - Chaque état est vert seul, à son plancher exact, par la commande du job : runner d'abord, puis la ligne de `gates.yml`.
   - Le changement `fetch-depth: 0` (Q-T4-11) est-il sain ? N'affaiblit-il aucune gate ?
2. **Conformité, exigence par exigence** : toutes celles que la proposition rattache à SB-9, SB-10 et SB-14, en particulier E-S-33 et E-S-39.
3. **Justesse, par des calculs indépendants du code.**
   - Variante non enroulée : décalages, segment central et K_H recalculés à la main sur de petits cas. Vérifie aussi le défaut que le worker a trouvé (série nulle entrée par décalage).
   - FIV_série : ton propre estimateur, écrit d'après PLAN-S2BIS et `r1` de f35a70c, sur des séries à lacunes. Il doit concorder exactement.
   - Calendrier J28 : recompte les comptes de positions de Q-T4-5 (calme 30 286, stress 13 491).
   - Oracle E-S-39 : rejoue-le, et vérifie que l'extraction de f35a70c est épinglée et échoue fermée.
   - Le mutant vivant M-VAR-1b est déclaré équivalent : contrôle la preuve.
4. **Identité bit à bit**, sous Python 3.10 à 3.13 × PYTHONHASHSEED : reproduis la nouvelle empreinte T4 (`6998101d…`) et les empreintes antérieures.
5. **Mutants.**
   - Rejoue le rouge puis le vert sur au moins trois pas.
   - Écris au moins quinze mutants à toi, classés par la commande du job, avec une borne de temps (un dépassement est FATAL).
   - Rejoue un échantillon d'au moins vingt mutants du worker.
6. **CI et règles.**
   - Aucune gate affaiblie.
   - R-13, R-8, octets 92, garde `ast` (étendue aux adaptateurs : vérifie qu'elle reste sûre).
   - `cargo --locked xtask verify` sur une copie : lignes de verdict seules ; la violation S-G9 `docs/17:70` est connue.
7. **Écarts E-1 à E-9.** Donne un avis motivé sur chacun.
   - **E-4** : des FIV de type E1 ont été imprimées avant E0. Ce coup d'œil a-t-il pu orienter un choix ? Compare au G0, à la grille et au critère.
8. **Constat du point 9** (la famille E1 n'atteint pas la courbe de S2). Recompte-le toi-même sur quelques réplications. Dis ce qu'il implique d'après le G0 : FIV-IDENTIF-1, PLAN-S2BIS-2 avant A-2.

## Exécution

- Copies par `git archive` avec les exclusions habituelles. `TMPDIR` dédié.
- Réseau isolé : `unshare -n` avec `lo` allumée (`…/s2bis/p1b/g2/travail/outils/isole.sh`).
- Consigne les PID réels ; pas de `pgrep -f` sur un motif large.
- Nettoie tes copies lourdes à la fin.

## Interdits

- `docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, `docs/adr-0028/execution/` ;
- tout `*.jsonl` ;
- toute pièce de D.2 ;
- **toute recherche récursive (grep -r, git grep, du, find large) sur `docs/`, sur le dépôt entier ou sur le scratchpad entier**.

## Rendu

Verdict : ACCEPTE, ACCEPTE-AVEC-CORRECTIONS (liste fermée) ou REFUSE.
Gate 0 : l'identifiant exact du modèle en tête. Résumé court en français.
