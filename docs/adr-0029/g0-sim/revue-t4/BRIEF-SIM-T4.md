# Brief — lot SIM-BIS, tranche 4 : SB-9 (variante), SB-10 (estimateur FIV), SB-14 (adaptateur r1)

Worker `shogen-worker`, effort max.

- Tu travailles dans `<scratchpad>/s2bis/sim4/`, avec un `TMPDIR` dédié.
- Le dépôt `/home/user/shogen` est en lecture seule : **aucune opération git en écriture**. Lis-le avec `git --no-optional-locks`.
- Lis `date -u` avant toute date.

## Base

Copie de la tête **5f99ab5** : `git archive 5f99ab5 | tar -x …`, avec les exclusions `docs/rapports`, `docs/adr-0025`, `docs/adr-0028/monark-m009a`, `docs/adr-0028/execution`, `docs/15-*`, `docs/16-*` et `docs/pocket-report`.

Pendant ton lot, l'orchestrateur committera la tranche C de P1 (collecteur `s2bis/`, plancher s2bis). Il recalera tes diffs sur la ligne de plancher de `sim-bis-unittest` s'il le faut. Toi, travaille sur 5f99ab5.

## Contrat

Le G0 est `docs/adr-0029/g0-sim/G0-SIM-BIS.md`, avec ses ajouts datés. Son contenu est `PROPOSITION.md`, corrigé par `AVIS.md`, qui prime. S'y ajoute l'ADR-0029. La numérotation SB-0 à SB-14 fait foi.

Sous-lots (PROPOSITION §6.1, l.362, 363 et 367 ; exigences E-S-nn rattachées par la proposition ; tests du §6.2) :
- **SB-9** : `variante.py`, rotation non enroulée sur segment central (≈ 140 lignes ; dépend de SB-7) ;
- **SB-10** : `calib_fiv.py`, estimateur FIV_série (forme de PLAN-S2BIS), grille et critère d'E1, oracle contre `r1` extrait (≈ 190 lignes ; dépend de SB-3 et SB-5) ;
- **SB-14** : `oracle_r1.py`, adaptateur r1 de `f35a70c` (FIV, `window`) (≈ 100 lignes ; dépend de SB-5 et SB-10).

Un sous-lot de plus de 200 lignes se scinde (SB-10a, SB-10b…).

## Pièces de revue à lire

- `docs/adr-0029/g0-sim/revue-t1/`, `revue-t2/`, `revue-t3/` : au moins les relectures G2, les avis et les rapports de corrections.
- Annexe B, items du lot (`docs/adr-0028/ANNEXE-B-items.md`, blocs B.61, B.62, B.64 et B.66, à lire seulement par ces blocs). Ceux qui te concernent directement :
  - SHOGEN-SIM-BIS-FIV-IDENTIF-1 ;
  - SHOGEN-SIM-BIS-WINDOW-EPINGLE-1 (SB-14) ;
  - SHOGEN-SIM-BIS-CONTRAT-RB6-1 (pour SB-9, si la variante touche la rotation).
- Code de `f35a70c` : lis-le par `git --no-optional-locks show f35a70c:<chemin>`, sur les seuls chemins dont tu as besoin.

## Règles propres à la tranche

Elles s'ajoutent aux règles communes plus bas.
- Identité bit à bit : graines, PYTHONHASHSEED, Python 3.10 à 3.13. Toute empreinte nouvelle est déclarée.
- Garde `ast` des puissances et du hasard (LIBM-POW-1) appliquée à tes modules.
- Aucune lecture de journal de campagne.
- Oracles exacts là où la proposition le dit. L'oracle de SB-10 contre `r1` extrait est mesuré sur la même entrée, avec l'écart déclaré.
- Toute valeur que le G0 ne fixe pas devient une question numérotée Q-T4-n, jamais un choix silencieux.

## Règles communes

- **Tests d'abord** : un rouge d'assertion montré avant le code, puis le vert.
- **Mutants** : au moins dix par sous-lot, classés par la commande du job (SHOGEN-S2BIS-MUT-COMMANDE-1). Verse tous les mutants que tu cites.
  - Runner d'abord, puis la ligne de `gates.yml`, sur la suite entière.
  - Borne de 300 s : un dépassement est FATAL, jamais « tué ».
- **Bibliothèque standard seule** (R-8). R-13. Octets 92 comptés juste, fichier par fichier.
- **Diffs en série**, chacun ≤ 200 lignes de code ajoutées (R-25). Plancher exact du job relevé à chaque diff (`--egal`).
- **Aucune opération réseau** : `unshare -n` avec `lo` allumée quand la suite l'exige (outils `lo_up.py` et `isole.sh` dans `…/s2bis/p1b/g2/travail/`).
- Python 3.10 à 3.13 en `-X dev -W error`.
- `cargo --locked xtask verify` sur la copie : lignes de verdict seules. S-G9 `docs/17:70` est connu sur les copies.
- **Livrables** : journal G1 dans le rapport ([lu], [2nd], [abs]), SHA256SUMS, estimation révisée des sous-lots restants (SB-11, SB-12, SB-13).
- **Machine partagée** :
  - consigne le PID réel et lis `/proc/PID/cmdline` ; jamais de `pgrep -f` sur un motif large ;
  - nettoie tes copies lourdes à la fin.
- **Après un compactage de contexte**, reprends depuis un fichier de notes tenu dans ton dossier, jamais depuis un `.jsonl`.

## Interdits

- `docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, `docs/adr-0028/execution/` ;
- tout `*.jsonl`, y compris ton propre journal de session ; toute pièce de D.2 ;
- **toute recherche récursive (grep -r, git grep, du, find large) sur `docs/`, sur le dépôt entier ou sur le scratchpad entier**, même sur tes copies.

D'autres agents et l'orchestrateur travaillent en parallèle. Ne prends aucun verrou git sur le dépôt.

Rapport par message. Gate 0 : l'identifiant exact du modèle en tête. Résumé court en français, point par point.
