# Brief — contre-contrôle des corrections de P1 tranche C (CB-18g à CB-18q)

Réviseur de la G2 de CB-18 (toi), effort max. Le dépôt `/home/user/shogen` est en lecture seule : **aucune opération git en écriture**, et lis-le avec `git --no-optional-locks`. L'orchestrateur y committe pendant ton lot. Lis `date -u` avant toute date. Tu travailles dans `<scratchpad>/s2bis/cb18/cc/`, avec un `TMPDIR` dédié.

## Base

Copie de **3164348** par `git archive`, avec les exclusions habituelles. Puis, en série :
- les 9 diffs `…/cb18/diffs/`, contrôlés par `…/cb18/SHA256SUMS` ;
- les 11 diffs `…/cb18/corr/diffs/CB-18g.diff` à `CB-18q.diff`, contrôlés par `…/cb18/corr/SHA256SUMS`.

Arbre attendu : 199454e1.

## Pièces

- Ta relecture : `…/cb18/g2/G2-CB18-transcrit.md`. Tes outils sont dans `…/cb18/g2/travail/`.
- Le brief des corrections : `…/cb18/corr/BRIEF-CORRECTIONS-CB18.md`.
- Le rapport du worker : `…/cb18/corr/RAPPORT-CORRECTIONS-CB18-transcrit.md`, avec les preuves `…/cb18/corr/preuves/` et les mutants `…/cb18/corr/mutants/`.
- Les lettres du FORMAT, ajoutées au lot :
  - avis `…/s2bis/rb18/g2/AVIS-FORMAT.md` ;
  - adjudication `…/s2bis/rb18/g2/ADJUDICATION-FORMAT.md` ;
  - la lettre du réviseur de RB-18 (C-1 à C-5 et N-1) : `…/s2bis/rb18/g2/G2-RB18-transcrit.md`, l.68-202.

## À contrôler (liste fermée)

1. **Les corrections C-1 à C-3 et les adjudications du brief** : chacune est fermée, avec un test qui échoue sans elle. Rejoue toi-même :
   - `sonde_budget.py` et `contournement_role.py` ;
   - tes mutants MR-01 à MR-26, par la commande du job (runner puis ligne de `gates.yml`, borne de 300 s, réseau isolé).
2. **LIGNE-JOB-LEURRE-1.**
   - Vérifie qu'un seul analyseur sert à K-01 à K-03 et à `ligne_du_job`.
   - Vérifie qu'aucun cas existant du runner n'est affaibli (33 → 57).
   - Cherche au moins cinq leurres neufs de ton cru.
3. **`--egal` sur le job S2** (plancher 406) : le couplage avec B-SEG-1 est-il juste ?
4. **Les lettres C-1 à C-5 du FORMAT**, telles que l'avis et l'adjudication les tranchent :
   - le §7.1 est-il conforme à la lettre et le seul lieu de la définition ?
   - `_lire` applique-t-il exactement le §7.1 ?
   - l'ordre de `queue` (§7.4), l'imbrication N = 64, la grammaire des noms (§5, §6.1, §7.7) ;
   - mutants neufs de ton cru.
5. **Les observations O-1 à O-3 du worker** (§9 de son rapport) : ton avis motivé, en une ligne chacune.
6. **Recalage** : le worker propose un plancher s2bis de 183 sur la tête 72aa806 (156 + 27). L'orchestrateur rebasera la série sur la tête qui suivra la tranche 3 des simulations. Il te montrera le rebasage dans un second message, pour une vérification brève.

## Règles

- Mêmes règles que ta G2 : Python 3.10 à 3.13 en `-X dev -W error`, `cargo --locked xtask verify` sur la copie (lignes de verdict seules ; S-G9 `docs/17:70` est connu), R-13, octets 92.
- Mutants classés par la commande du job (sortie 1 = tué, 0 = vivant, autre = FATAL).
- Les journaux d'exemple de RB-18 sont des `*.jsonl` : tu ne les lis pas, même par programme.
- Machine partagée : consigne le PID réel ; jamais de `pgrep -f` sur un motif large.
- Nettoie tes copies lourdes à la fin.
- Après un compactage, reprends depuis un fichier de notes tenu dans ton dossier, jamais depuis un `.jsonl`.

## Interdits

- `docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, `docs/adr-0028/execution/` ;
- tout `*.jsonl`, y compris ton propre journal de session ;
- toute pièce de D.2 ;
- `recalc/lecteur.py` et l'oracle de RB-18 ;
- **toute recherche récursive (grep -r, git grep, du, find large) sur `docs/`, sur le dépôt entier ou sur le scratchpad entier**.

## Verdict

CONFORME, ou NON-CONFORME avec une liste fermée de points CC-n, chacun avec sa preuve.

Rapport par message. Gate 0 : l'identifiant exact du modèle en tête. Résumé court en français, point par point.
