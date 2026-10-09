# Brief — SIM-BIS, SB-13 première passe : `oracle_recalc.py`, oracle croisé avec RB-6 (E-S-51, première moitié)

Worker `shogen-worker`, effort max. Dossier : `<scratchpad>/s2bis/sb13/` (scratchpad = `<scratchpad>`), `TMPDIR` dédié, `NOTES.md` tenu (reprise depuis lui, jamais depuis un `.jsonl`). Dépôt `/home/user/shogen` en lecture seule (`git --no-optional-locks`), **aucune écriture git**. `date -u` avant toute date. Base : tête **5cfe746** (`git archive`, exclusions habituelles : `docs/rapports`, `docs/adr-0025`, `docs/adr-0028/monark-m009a`, `docs/adr-0028/execution`, `docs/15-*`, `docs/16-*`, `docs/pocket-report`). Un autre lot de SIM-BIS (SB-15A à SB-15G, intégration de PLAN-S2BIS-2) est en relecture et sera commis avant toi : n'y touche pas ; tes diffs ne doivent toucher que `oracle_recalc.py`, son test et ce qu'exige le plancher.

## Contrat
- G0 `docs/adr-0029/g0-sim/G0-SIM-BIS.md` et ses ajouts datés ; `PROPOSITION.md` **E-S-01** (l.135 : le moteur n'importe ni `shogen_s2` ni `shogen_s2bis` ; deux adaptateurs d'oracle seulement, dont `oracle_recalc.py`, paquet `s2bis` au commit cité ; frontière testée par analyse syntaxique des imports) et **E-S-51** (l.220 : o(r, u) et K^(r) égaux à ceux de RB-6 sur 5 vecteurs de test, dont o = 0 et o = n − 1, et 100 séries synthétiques, dès le commit de RB-6) ; ligne SB-13 (l.366) ; `AVIS.md` Q-S-02.
- RB-6 : `s2bis/shogen_s2bis/recalc/rotation.py` et ses tests (commits RECALC-BIS RB-6a, RB-6b) ; `docs/adr-0029/s2bis/ROTATION-S2BIS.md`.
- SIM-BIS : `scripts/sim-bis/regle.py` (SB-7 : décalages SHA-256, rotation enroulée, K) et `oracle_r1.py` (forme d'un adaptateur d'oracle existant).
- Items à fermer ici : **SHOGEN-SIM-BIS-CONTRAT-RB6-1** (annexe B l.1095 : un test lie les règles de noms, de seuils et de vecteurs des deux textes) ; lis aussi SHOGEN-SIM-BIS-ORACLE-RB7-1, qui reste ouvert (seconde passe après RB-7).

## À faire
1. `scripts/sim-bis/oracle_recalc.py` : adaptateur qui charge `shogen_s2bis.recalc.rotation` **au commit cité** (forme : extraction par `git archive` du paquet `s2bis` au commit épinglé dans `parametres.json`, comme `oracle_r1.py` extrait le harnais de `f35a70c`), sans que le moteur l'importe.
2. Tests : o(r, u) et K^(r) égaux à RB-6 sur 5 vecteurs (dont o = 0 et o = n − 1) et 100 séries synthétiques à graine fixe ; le test lie les règles de noms, de seuils et de vecteurs (CONTRAT-RB6-1) ; la frontière E-S-01 reste testée.
3. Si le commit à citer, ou la forme de l'extraction, n'est pas fixé par le contrat : question Q-SB13-n, avec ton choix et sa raison.

## Règles
Tests d'abord, rouge d'assertion montré ; diffs SB-13a, SB-13b… ≤ 200 lignes de code ajoutées ; plancher sim-bis exact dans `gates.yml` ; au moins 10 mutants par diff, classés par la commande du job sim-bis (borne 300 s, FATAL au-delà) ; bibliothèque standard seule ; Python 3.11 à 3.13 en `-X dev -W error` (3.10 : dis-le) ; R-13, R-8, octets 92, 120 caractères ; réseau isolé ; avant livraison : runner (136), jobs s2bis (255), S2 (415), sim-bis ; `cargo --locked xtask verify` sur la copie (lignes de verdict seules). Aucun `__pycache__` laissé dans une racine de suite.

## Interdits
Aucun journal réel ; ne jamais poser `SHOGEN_S2_CAMPAGNE_CONTROL` ; `docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, `docs/adr-0028/execution/` ; tout `*.jsonl` ; toute pièce de D.2 ; toute recherche ou énumération récursive sur `docs/`, le dépôt entier ou le scratchpad entier ; aucun fichier sous un `.claude/` du dépôt réel ; rien sur Pocket.

## Rendu
Par message (ta valeur de retour), Gate 0 en tête : diffs (sha256, lignes), tableau E-S-51 et CONTRAT-RB6-1 avec fichier:ligne et test, mutants, matrice, plancher, questions, écarts. Écris-le aussi dans `<scratchpad>/s2bis/sb13/RAPPORT-GENERATEUR.md`, couvert par ton `SHA256SUMS`.
