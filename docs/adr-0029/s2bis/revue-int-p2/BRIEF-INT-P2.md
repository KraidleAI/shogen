# Brief — intégrateur de la partie P2 du collecteur de S2-bis (tranches C et D, corrections, CB-16)

Orchestrateur, 2026-10-17 12:07:18 UTC (`date -u`). Worker `shogen-worker`, effort high, **intégrateur neuf** (ni générateur de P2C, ni de P2D). Tu travailles dans `<scratchpad>/s2bis/int-p2/` (`NOTES.md` tenu, `TMPDIR` et cible cargo dédiés). Dépôt `/home/user/shogen` en lecture seule ; base : copie de la tête **2a07ae6** (`git archive`, exclusions des interdits). Lis `date -u` avant toute date.

## Entrées (lis en entier)
- Tranche C (CB-7, CB-8) : `<scratchpad>/s2bis/p2c/RAPPORT-GENERATEUR.md`, `<scratchpad>/s2bis/p2c/diffs/` (six diffs, dans l'ordre), adjudication `<scratchpad>/s2bis/p2c/ADJUDICATION.md` (décisions Q-1 à Q-7, Q-C-10, C-P2C-1).
- Tranche D (CB-9) : `<scratchpad>/s2bis/p2d/RAPPORT-GENERATEUR.md`, `<scratchpad>/s2bis/p2d/diffs/` (trois diffs), adjudication `<scratchpad>/s2bis/p2d/ADJUDICATION.md` (décisions Q-1 à Q-4, C-P2D-1, C-P2D-2 ; ajout daté sur Curve) et la lecture `<scratchpad>/s2bis/curve-doc/RAPPORT-LECTEUR.md`.
- Contrat : `docs/adr-0029/g0-collecte/G0-COLLECTE-RECALC-DEPLOI.md` (contenu : `docs/adr-0029/g0-collecte/PROPOSITION.md` corrigé par `docs/adr-0029/g0-collecte/AVIS.md`, qui prime) ; ADR-0029 `docs/adr-0029/ADR-0029-campagne-S2-bis.md` (l.174 : ensemble témoin hors des classes USD et hors du vote) ; FORMAT `docs/adr-0029/s2bis/FORMAT-JOURNAUX-S2BIS.md` ; code `s2bis/shogen_s2bis/collecte/decodeurs.py`, `s2bis/shogen_s2bis/recalc/config_analyse.py` (classes du recalc l.21 et l.31), `s2bis/tests/`.

## Travail, dans cet ordre, une série unique de diffs `diffs/INT-P2-nn.diff` appliquée sur 2a07ae6
1. Les six diffs de P2C **tels quels** (à l'octet ; si l'un ne s'applique plus, dis-le, ne le réécris pas).
2. Les trois diffs de P2D **rebasés** sur l'état 1 (conflits : `test_decodeurs` l.52, plancher de `gates.yml`, table `DECODEURS`) ; le contenu de CB-9 ne change pas hors des hunks en conflit ; les planchers sont recalculés en série (`--egal`, de 394 vers la fin).
3. **C-P2D-1** : classe de source `temoin` pour les trois lectures du témoin (table `DECODEURS`), hors `PLANCHERS` et `SIGMA_*` du recalc : le recalc **refuse** explicitement une classe `temoin` dans une entrée du vote (test nommé) ; FORMAT §9.1 si les classes y sont listées.
4. **C-P2D-2** : limites de la lecture Curve déclarées dans la docstring du décodeur et au FORMAT (identité du code `master` avec le bytecode déployé non vérifiée ; rattachement direct du pool NG non lu ; absence du bogue d'oracle non vérifiée sur chaîne).
5. **C-P2C-1** : le test `Bornes` de `test_decodeurs.py` rendu indépendant de la charge (aucune mesure de temps réel dans un verdict) ; preuve : rejoué dix fois pendant une campagne de mutants, dix verts.
6. **CB-16, smoke sans prix** (PROPOSITION l.224 et E-C-37 l.198) : commande qui joue chaque forme (hôte, actif) du pool, le témoin et chaque source de la carte, et imprime statut, code HTTP et sous-type **sans aucun prix** (le rodage interdit toute lecture de prix, ADR l.222) ; lecture HTTP injectable, tests sur fixtures seulement, aucune opération réseau ; un test prouve qu'aucune chaîne de prix ne sort (mutant qui imprime le prix : tué).
7. Table des pas (`pas.tsv` : `id\tsujet\tn_tests`) et `source-pas.md` (ce que chaque pas porte et d'où il vient), pour les messages de commit de la chaîne.

## Règles
- **tests d'abord** ; **mutants** sur chaque diff neuf (3 à 6 : au moins dix par diff, classés par la commande du job ; borne 300 s ; dépassement = FATAL ; règle de l'item SHOGEN-S2BIS-MUT-COMMANDE-1, fermé à l'annexe B) ; les mutants des générateurs ne sont pas rejoués ;
- **bibliothèque standard seule** (R-8) ; R-13 ; aucun flottant dans un journal ; `parse_float=Decimal` ;
- diffs ≤ 200 lignes de code ajoutées (R-25), plancher exact du job s2bis à chaque diff, section METRIQUES (`docs/adr-0029/s2bis/METRIQUES-S2BIS.md`) par diff ;
- **aucune opération réseau** (`unshare -n`, `<scratchpad>/s2bis/p1b/g2/travail/outils/isole.sh`, `env -u SHOGEN_S2_CAMPAGNE_CONTROL`) ; fixtures seulement ;
- Python 3.10 à 3.13 en `-X dev -W error` ; **tout Python s'écrit `python3 -I -B`** ; aucun `__pycache__` dans une racine de suite ;
- avant livraison, sur l'arbre final : runner, jobs s2bis, S2 et sim-bis aux planchers exacts ; `cargo --locked xtask verify` : lignes de verdict seules (S-G9 `docs/17:70` connu sur les copies) ; la série rejouée depuis une extraction neuve de 2a07ae6 égale à l'arbre final (`diff -r`) ;
- un seul processus lourd à la fois ; nettoie tes copies lourdes à la fin ;
- journal G1 ([lu], [2nd], [abs]) ; `RAPPORT-INTEGRATEUR.md`, `SHA256SUMS` ; les écarts au brief consignés.

Interdits : `docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, `docs/adr-0028/execution/` ; tout `*.jsonl` réel ; toute pièce de D.2 ; ne jamais poser `SHOGEN_S2_CAMPAGNE_CONTROL` ; **aucune recherche ou énumération récursive (grep -r, git grep, git ls-tree -r, du, find large) sur `docs/`, sur le dépôt entier ni sur le scratchpad entier, même sur tes copies** ; aucun fichier sous un `.claude/` du dépôt réel ; rien sur Pocket ; aucune opération git en écriture sur `/home/user/shogen` ; toute commande git qui liste ou compare des chemins est limitée à une liste explicite de chemins ; `git --no-optional-locks`.

Gate 0 : identifiant exact de ton modèle en tête (attendu `claude-opus-5-5`). Rapport final par message, court, en français ; écrit aussi dans `RAPPORT-INTEGRATEUR.md`, couvert par ton `SHA256SUMS`.
