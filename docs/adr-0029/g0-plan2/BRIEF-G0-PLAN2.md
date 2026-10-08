# Brief — proposition de G0 du lot PLAN-S2BIS-2 (identification du groupement des pannes source par source)

Tu es le rédacteur de la proposition de G0 (`shogen-worker`, effort max). Tu écris un document de conception, pas de code.

- Le dépôt `/home/user/shogen` est en lecture seule : aucune opération git en écriture. Utilise `git --no-optional-locks`.
- Lis `date -u` avant toute date.
- Tu écris seulement dans `<scratchpad>/s2bis/plan2/`, et tu rends ton rapport par message.
- Tiens un fichier `NOTES.md`. Après un compactage, tu reprends depuis lui, jamais depuis un `.jsonl`.

## Pourquoi ce lot, et pourquoi maintenant

Le G0 de SIM-BIS (`docs/adr-0029/g0-sim/G0-SIM-BIS.md` l.13-15 ; AVIS l.23, l.100, l.104 ; PROPOSITION l.324-332, l.492-493, l.601) a prévu PLAN-S2BIS-2. Ce lot identifie, unité par unité, le groupement propre à chaque source : FIV_u(ℓ) par unité, intervalles entre épisodes, à `f35a70c`, scripts épinglés avant exécution.

La tranche 4 de SIM-BIS a constaté que la famille E1 n'atteint pas la courbe de S2 : FIV(240) ≈ 2, contre 22,9 et 34,6 sur EP (`…/s2bis/sim4/g2/RAPPORT-WORKER-SIM-T4-transcrit.md`, point 9).

L'advisor recommande l'**option B** (`…/s2bis/sim4/g2/AVIS-SIM-T4.md`, §2) : avancer PLAN-S2BIS-2 maintenant, en lot parallèle d'environ 150 lignes, de classe M. Il y ajoute :
- le masque des fenêtres évaluables J28 (limite Q-T4-5) ;
- avant E0, un ajout daté au G0 de SIM-BIS : C1 = point de la grille calibré sur les FIV_u par unité.

L'orchestrateur a adopté l'option B. Ta proposition en est la première pièce.

## Patron

Le lot PLAN-S2BIS (1) :
- code : `scripts/plan-s2bis/` (README, `parametres.json`, `commun.py`, `episodes.py`, `regles.py`, `lancer.sh`, tests) ;
- sorties : `docs/adr-0029/plan-s2bis/` (README, G1, G2, `episodes.txt` = EP) ;
- annexe B, bloc B.58 seulement, pour la règle d'épinglage au JOURNAL avant toute lecture des journaux scellés, et pour l'exception écrite au G0 qui permet aux scripts du lot de lire ces journaux.

**Ta proposition reprend ce patron, sans le relâcher.** Ni toi, ni le worker qui écrira le code, ni aucun agent ne lit un journal de campagne (`*.jsonl`). Seuls les scripts du lot, épinglés, les lisent une fois, lancés par l'orchestrateur.

## Ce que doit contenir la proposition

À écrire dans `PROPOSITION-PLAN2.md`, avec la forme et le niveau de détail de `docs/adr-0029/g0-sim/PROPOSITION.md` :

1. **Objet et rattachements** : ADR-0029, G0 de SIM-BIS, items FIV-IDENTIF-1 et SIM-BIS-SOURCES-LIMITES-1.
2. **Sorties exactes, avec leur forme** :
   - FIV_u(ℓ) par unité (hôte D1-bis), par strate, sur la grille ℓ de calibration ;
   - lois des intervalles entre épisodes, par unité ;
   - masque des fenêtres évaluables J28 (positions de la portée et plage D5) ;
   - précision des calculs exacts (Fraction, Decimal sous le contexte de r1).
3. **Lien avec SIM-BIS** : comment C1 se calibre sur ces sorties (lettre proposée pour l'ajout daté au G0 de SIM-BIS), et ce que deviennent C0 et C2.
4. **Exigences numérotées E-P2-nn** :
   - frontière : le lot lit les journaux scellés à `f35a70c`, et seulement par ses scripts ;
   - refus nommés ;
   - identité bit à bit ;
   - épinglage au JOURNAL avant toute lecture ;
   - exécution unique par l'orchestrateur ;
   - versement.
5. **Sous-lots**, chacun ≤ 200 lignes, avec leurs tests. Tests sur fixtures synthétiques seulement.
6. **Oracles** : FIV_u contre l'estimateur de SB-10 (`calib_fiv.py`), qui est à la tranche 4 et pas encore commis ; contre `r1` extrait de f35a70c ; comptages naïfs.
7. **Questions** Q-P2-n pour l'advisor : tout ce que l'ADR et le G0 ne fixent pas.
8. **Calendrier**, risques et items.

## Pièces à lire

- G0 de SIM-BIS, `PROPOSITION.md`, `AVIS.md`, en entier.
- `revue-t1` à `revue-t3` : les AVIS seulement.
- `AVIS-SIM-T4.md` et `RAPPORT-WORKER-SIM-T4-transcrit.md`.
- ADR-0029, par plages : §2.4, §2.6 et les ajouts datés.
- `scripts/plan-s2bis/` (code et README).
- `docs/adr-0029/plan-s2bis/` : README, G1, G2 et `episodes.txt` (sorties versées, pas des journaux).
- Annexe B : B.58, B.61, B.64 et B.66 seulement.
- `calib_fiv.py` dans les diffs `…/sim4/diffs/SB-10A.diff` à `SB-10C.diff`.

## Interdits

- `docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, `docs/adr-0028/execution/` ;
- tout `*.jsonl` ;
- toute pièce de D.2 ;
- **toute recherche récursive (grep -r, git grep, du, find large, Glob large) sur `docs/`, sur le dépôt entier ou sur le scratchpad entier**.

Gate 0 : l'identifiant exact du modèle en tête. Résumé court en français.
