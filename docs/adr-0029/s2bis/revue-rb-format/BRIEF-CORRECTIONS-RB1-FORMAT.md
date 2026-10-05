# Brief — corrections de RB-1 (lecteur principal `recalc/lecteur.py`) d'après la lettre du FORMAT, C-14, C-15 et C-1 à C-5

Worker `shogen-worker`, effort max. Le dépôt `/home/user/shogen` est en lecture seule : **aucune opération git en écriture** (`git --no-optional-locks`). Lis `date -u` avant toute date. Tu travailles dans `<scratchpad>/s2bis/rb1/corr2/` (scratchpad = `<scratchpad>`), avec un `TMPDIR` dédié.

## Base

- Copie de la tête **98c8537** par `git archive`, exclusions habituelles : `docs/rapports`, `docs/adr-0025`, `docs/adr-0028/monark-m009a`, `docs/adr-0028/execution`, `docs/15-*`, `docs/16-*`, `docs/pocket-report`.
- Tes diffs en série : **RB-1h** et suivants.
- L'orchestrateur committe en parallèle d'autres lots (runner, `scripts/sim-bis`) et le lecteur indépendant RB-18 (qui ajoute des tests à la suite s2bis) : il recalera les planchers. **Ta série est commise avant celle de RB-18.**

## Pièces

- **Lettre** : le FORMAT de la tête `docs/adr-0029/s2bis/FORMAT-JOURNAUX-S2BIS.md` (lettres C-1 à C-5 commises par P1 tranche C : §1.2, §6.1, §7, §7.1, §7.4, §8.3, et les autres paragraphes qu'elles touchent). C'est ta source.
- Adjudication de l'orchestrateur : `<scratchpad>/s2bis/rb18/g2/ADJUDICATION-FORMAT.md` (seule pièce de `rb18/` que tu lis).
- Corrections demandées : `<scratchpad>/s2bis/rb1/corr2/EXTRAIT-G2-RB1.md` (C-14, C-15).
- Le lecteur commis `s2bis/shogen_s2bis/recalc/lecteur.py` et ses tests ; tes pièces de la tranche 1 : `<scratchpad>/s2bis/rb1/` (brief, corr, notes, preuves).
- Contrat : G0 `docs/adr-0029/g0-collecte/G0-COLLECTE-RECALC-DEPLOI.md` et son ajout daté (Q-RB-13, Q-RB-14), `PROPOSITION.md`, `AVIS.md`.

## Indépendance

- Tu ne lis **rien** dans `<scratchpad>/s2bis/rb18/` hormis `g2/ADJUDICATION-FORMAT.md` : ni `oracle_indep`, ni ses diffs, ni la relecture, ni le banc, ni la contre-épreuve. Les deux lecteurs sont corrigés d'après la lettre seule ; le banc tiers les comparera ensuite.

## Corrections (liste fermée)

- **C-14** et **C-15**, telles qu'écrites dans l'extrait.
- **Alignement sur C-1 à C-5 de la lettre** : passe chaque lettre et corrige tout écart du lecteur. Précisions de l'adjudication à suivre à la lettre : intègre = la définition unique du §7.1 (types exacts, booléen jamais entier, `ws` null vérifié type par type) ; déclaration de `queue` exacte et en ordre croissant (jour, k), toutes les queues rendues avec la rupture ; imbrication N = 64 racine au niveau 1, comptée par le lecteur lui-même (jamais `RecursionError`) ; k suit `0|[1-9][0-9]*`, un nom du préfixe non conforme est un refus nommé, un dossier vide est un refus nommé, ordre (jour, k entier).
- Tableau final : lettre par lettre, l'écart trouvé, le diff et le test qui le fixe (ou « déjà conforme », avec le test qui le prouve).

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
