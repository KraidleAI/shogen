# Brief — corrections de RB-18 (lecteur indépendant `oracle_indep.py`) d'après la lettre du FORMAT, C-6 à C-13

Worker `shogen-worker`, effort max. Le dépôt `/home/user/shogen` est en lecture seule : **aucune opération git en écriture** (`git --no-optional-locks`). Lis `date -u` avant toute date. Tu travailles dans `<scratchpad>/s2bis/rb18/corr/` (scratchpad = `<scratchpad>`), avec un `TMPDIR` dédié.

## Base

- Copie de la tête **98c8537** par `git archive`, exclusions habituelles : `docs/rapports`, `docs/adr-0025`, `docs/adr-0028/monark-m009a`, `docs/adr-0028/execution`, `docs/15-*`, `docs/16-*`, `docs/pocket-report`.
- Tes diffs RB-18a à RB-18d (`<scratchpad>/s2bis/rb18/diffs/`, écrits sur une tête plus ancienne) sont **recalés** sur 98c8537 (C-13) : ne plus créer `recalc/__init__.py` (il existe), ne plus toucher `REGLES`. Puis tes corrections en RB-18e et suivants.
- L'orchestrateur committe en parallèle d'autres lots (runner, `scripts/sim-bis`) et les corrections de RB-1 (qui ajoutent des tests à la suite s2bis) : il recalera ton plancher s'il le faut.

## Pièces

- **Lettre** : le FORMAT de la tête `docs/adr-0029/s2bis/FORMAT-JOURNAUX-S2BIS.md` (lettres C-1 à C-5 commises par P1 tranche C : §1.2, §6.1, §7, §7.1, §7.4, §8.3, et les autres paragraphes qu'elles touchent). C'est ta source.
- Adjudication de l'orchestrateur : `<scratchpad>/s2bis/rb18/g2/ADJUDICATION-FORMAT.md` (seule pièce de `rb18/g2/` que tu lis).
- Corrections demandées : `<scratchpad>/s2bis/rb18/corr/EXTRAIT-G2-RB18.md` (C-6 à C-13, liste fermée).
- Tes propres pièces : `rb18/BRIEF-RB18.md`, `rb18/G1-RB18.md`, `rb18/notes/`, `rb18/diffs/`, `rb18/fixtures/`, `rb18/outils/`, `rb18/preuves/`.
- Contrat : G0 `docs/adr-0029/g0-collecte/G0-COLLECTE-RECALC-DEPLOI.md`, `PROPOSITION.md` (l.396, l.486, l.539-540, l.551), `AVIS.md`.

## Indépendance (règle dure)

- Tu ne lis **pas** le lecteur principal : ni `<scratchpad>/s2bis/rb1/` (tout), ni `s2bis/shogen_s2bis/recalc/lecteur.py`, ni les autres fichiers de `recalc/` hormis l'existence de `__init__.py`.
- Tu ne lis **rien d'autre** dans `<scratchpad>/s2bis/rb18/g2/` que `ADJUDICATION-FORMAT.md` : ni la relecture, ni ses outils (`aligner.py`, banc), ni ses preuves (contre-épreuve).
- Tu peux lire l'écrivain `s2bis/shogen_s2bis/collecte/journal.py` de la tête pour produire des journaux réels de test.
- Test de frontière : `oracle_indep` n'importe ni le lecteur principal ni l'écrivain.
- Si la lettre est muette, écris une Q-R18-n (ton choix, sa raison) ; ne devine jamais en lisant RB-1.

## Corrections (liste fermée, `EXTRAIT-G2-RB18.md`)

C-6 à C-11 d'après la lettre ; C-12 (tests G-07, G-08, G-13, G-14, comportements de C-6 à C-11, tracemalloc de `Lecture` sur tailles 1 et 4, G1 corrigé) ; C-13 (recalage, plancher re-mesuré). Précisions de l'adjudication à suivre à la lettre : imbrication N = 64 racine au niveau 1, comptée par le lecteur lui-même (jamais `RecursionError`) ; k suit `0|[1-9][0-9]*`, un nom du préfixe non conforme est un refus nommé, un dossier vide est un refus nommé, ordre (jour, k entier) ; `queue` en ordre croissant (jour, k).

Sortie canonique inchangée (JSON trié) sauf si la lettre l'exige ; toute modification déclarée.

## Règles

- **Tests d'abord**, avec un rouge d'assertion montré avant le code.
- **Mutants** : au moins dix par diff, classés par la commande du job (runner, puis la ligne s2bis de `gates.yml`, borne 300 s ; dépassement = FATAL).
- Bibliothèque standard seule. Python 3.10 à 3.13 en `-X dev -W error`. Identité de sortie entre versions.
- Diffs en série, **chacun ≤ 200 lignes de code ajoutées**, plancher exact relevé à chaque diff (`--egal`).
- R-13, R-8, octets 92 comptés juste ; lignes ≤ 120 caractères.
- `unshare -n` avec `lo` allumée (`<scratchpad>/s2bis/p1b/g2/travail/outils/isole.sh`) pour les jobs s2bis et S2.
- `cargo --locked xtask verify` sur la copie : lignes de verdict seules ; S-G9 `docs/17:70` est connu.
- **Livrables** : diffs, SHA256SUMS, journal G1 ([lu]/[abs]), section METRIQUES de chaque diff, questions Q-n avec ton choix et sa raison si la lettre est muette.
- Consigne le PID réel de tes processus ; pas de `pgrep -f` sur un motif large. Nettoie tes copies lourdes à la fin.
- Tiens un `NOTES.md` dans ton dossier ; après un compactage ou un redémarrage, reprends depuis lui, jamais depuis un `.jsonl`.

## Interdits (communs)

- `docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, `docs/adr-0028/execution/` ;
- tout `*.jsonl` réel ; toute pièce de D.2 ;
- **toute recherche récursive (grep -r, git grep, du, find large) sur `docs/`, sur le dépôt entier ou sur le scratchpad entier**.

Rapport par message. Gate 0 : l'identifiant exact du modèle en tête. Résumé court en français, point par point.
