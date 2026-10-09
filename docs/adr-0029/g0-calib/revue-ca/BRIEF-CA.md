# Brief — lot CALIB-ACTIFS, code CA-0 à CA-6 (`scripts/calib-actifs/`), sur fixtures synthétiques, sans épinglage ni lancement

Worker `shogen-worker`, effort max. Dépôt `/home/user/shogen` en lecture seule (`git --no-optional-locks`), **aucune écriture git**. `date -u` avant toute date. Dossier : `<scratchpad>/s2bis/calib3/` (scratchpad = `<scratchpad>`), `TMPDIR` dédié, `NOTES.md` tenu (reprise depuis lui après un compactage, jamais depuis un `.jsonl`).

## Contrat (lis-le d'abord)
- G0 `docs/adr-0029/g0-calib/G0-CALIB-ACTIFS.md` **et son ajout daté** (INV-1 = option A). Son contenu est `PROPOSITION.md` du même dossier, corrigée par `AVIS.md`, qui prime (adjudication 1 : modifications de Q-CA-11 et Q-CA-15, précisions de Q-CA-02, Q-CA-04, Q-CA-06, Q-CA-07, Q-CA-13).
- `PROPOSITION.md` : §2 (pools, formes ; entrées), §3.1 (sources), **§4 (règles de calcul), §5 (exigences E-CA-01 à E-CA-33), §5.7 (refus nommés), §6 (sous-lots CA-0 à CA-6, tests T-CA-*, mutants M-CA-*), §7 (oracles)**. `PAIRES-ET-TEMOIN.md` pour les faits relevés.
- ADR-0029 : l.181-191, l.212, et les ajouts datés du 2026-10-08 (lettre de l.189 : dénominateur = maximum des deux classes de places de BTC ; troisième terme = places à horodatage de dernière transaction, P99 des âges par cellule).
- `docs/adr-0029/calib/SOURCES-HISTORIQUES.md` (en entier : sources, formats, §4 comptes de l'oracle d'exécution, sha256 de Kraken).
- Patron : `scripts/plan-s2bis/` et `scripts/plan-s2bis-2/` (socle, lanceur épinglé, refus nommés, passes A et B), lus en entier pour ce que tu reprends ; `scripts/plan-s2bis/regles.py` (`quantile`, `regle_tau`) en lecture, **jamais importé** (Q-CA-13 : réimplémentation croisée par un fichier de vecteurs relu des deux côtés).
- Côté recalcul, pour T-CA-FRG-1 seulement : le chargeur de configuration de l'analyse, `s2bis/shogen_s2bis/recalc/config_analyse.py` (`charger`, l.125), en lecture ; tu ne modifies rien sous `s2bis/` (E-CA-23 relève de RB-2, hors de ce lot).
- Items, à lire dans `docs/adr-0028/ANNEXE-B-items.md` **par leur nom seulement** : SHOGEN-S2BIS-SIGMA-ACTIFS-1, SHOGEN-S2BIS-CALIB-L189-1, SHOGEN-S2BIS-HORODATAGE-SENS-1, SHOGEN-S2BIS-CADENCE-AGREG-1, SHOGEN-S2BIS-P1-ESTIMATION-1.

## Base
Tête **ebd1560** de `claude/compassionate-noether-szmdyj` (`git archive`, exclusions habituelles : `docs/rapports`, `docs/adr-0025`, `docs/adr-0028/monark-m009a`, `docs/adr-0028/execution`, `docs/15-*`, `docs/16-*`, `docs/pocket-report`).

## Périmètre (liste fermée)
1. **CA-0 à CA-6** de la PROPOSITION §6.1, sous `scripts/calib-actifs/`, avec le mode explicite `calibre` / `planchers_seuls` par actif dans le fragment (Q-CA-15 modifiée) et les impressions de Q-CA-04 (part des cellules de la queue et âge médian, par place) et le drapeau descriptif de Q-CA-06.
2. **Liste des places de calibration** dans `parametres.json` **par lecture** (A : six places, SOURCES-HISTORIQUES §1 ; A′ en variante, Q-CA-15), la lecture retenue étant A ; aucune valeur d'historique dans le dépôt.
3. **Relevé de cadence des agrégateurs** (Q-CA-11 modifiée) : script séparé, **hors de `lancer.sh`**, sans prix écrit (horodatages seuls), avec ses tests ; jamais lancé contre le réseau par toi.
4. **Job CI** du lot : une ligne `calib-actifs-unittest` dans `.github/workflows/gates.yml`, sur le patron des jobs `sim-bis-unittest` et `s2bis-unittest` (vérificateur `enforcement/verdict-suite-s2.py`, `--plancher` exact, aucun saut admis) ; dis en question si le patron ne s'applique pas.
5. **Répétition à l'échelle** (E-CA-26) sur bougies **synthétiques** (131 040 minutes, six places) : durée et mémoire mesurées.
6. Hors périmètre : tout téléchargement réel, l'épinglage (E-CA-27), le lancement (E-CA-28), le versement des sorties, toute statistique de dispersion sur un historique réel (E-CA-25), E-CA-23 côté RB-2, toute modification sous `s2bis/`, `s2-harness/`, `scripts/plan-s2bis*/`. Si le contrat est muet ou contredit le code : question **Q-CA3-n**, avec ton choix et sa raison ; tu ne tranches aucune valeur scellée.

## Règles
- **Tests d'abord**, rouge d'assertion montré ; valeurs de référence indépendantes du code (à la main, `sha256sum`, `date -u -d`) ; tous les T-CA-* du §6.2, avec les deux vecteurs ajoutés par l'avis à Q-CA-13 (borne basse exacte, 1/3 %).
- Diffs en série **CA-0a, CA-0b…**, chacun ≤ 200 lignes de code ajoutées (R-25) ; plancher du job recalé exactement à chaque diff ; METRIQUES si la forme du dépôt l'exige.
- **Au moins 10 mutants par diff**, dont les M-CA-* du §6.2 rattachés à ce diff, classés par la commande du job (borne 300 s, dépassement FATAL) ; selon SHOGEN-MUTANTS-SITE-APPEL-1, des mutants du site d'appel des fonctions partagées et de la source des données passées sous une étiquette inchangée.
- Bibliothèque standard seule (R-8) ; Python 3.10 à 3.13 en `-X dev -W error` (critère de vert : code 0, aucune ligne « Exception ignored » ni « Warning ») ; aucune fonction transcendante de libm dans le calcul ; Decimal depuis les chaînes, Fraction pour les rapports (E-CA-18).
- R-13 ; octets 92 comptés juste (`chr(92)` dans les gabarits) ; lignes ≤ 120 caractères. Réseau isolé pour les tests (`<scratchpad>/s2bis/p1b/g2/travail/outils/isole.sh`) ; serveur local de fichiers synthétiques pour CA-1 et CA-2.
- Machine partagée : PID réel consigné, `/proc/PID/cmdline` lu, jamais de `pgrep -f` large ; tâches longues détachées (`setsid nohup`), fin constatée ; copies lourdes supprimées à la fin.
- Avant livraison : runner (`enforcement/tests/run-fixtures-verdict-suite-s2.py`), jobs s2bis, S2, sim-bis et le job neuf aux planchers exacts, hook, gate des secrets, `cargo --locked xtask verify` sur la copie (lignes de verdict seules ; S-G9 `docs/17:70` connu sur copie ; S-G5 : aucune citation anglaise entre guillemets « » qui ne soit au registre, un message d'erreur se met en code).

## Interdits (durs)
Aucun journal réel de S2 ni de S2-bis ; aucune extraction de `f35a70c` ; aucun téléchargement d'historique réel ; ne jamais poser `SHOGEN_S2_CAMPAGNE_CONTROL`, même vide (seul le test du lanceur la pose à une valeur fictive dans son propre sous-processus, E-CA-03) ; `docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, `docs/adr-0028/execution/` ; tout `*.jsonl` ; toute pièce de D.2 ; `tau_sigma.txt` jamais ouvert (son sha256 seulement, E-CA-02) ; toute recherche ou énumération récursive (grep -r, git grep, git ls-tree -r, du, find large) sur `docs/`, le dépôt entier ou le scratchpad entier ; aucun fichier sous un `.claude/` du dépôt réel ; rien sur Pocket.

## Rendu
Rapport final par message (ta valeur de retour), en français, Gate 0 (identifiant exact du modèle) en tête : diffs (sha256, lignes de code ajoutées, planchers), tableau E-CA-01 à E-CA-33 (tenue, fichier:ligne, test ; « hors lot » dit pour E-CA-23, E-CA-27 à E-CA-29), T-CA-* et M-CA-*, mutants, matrice, répétition (durée, mémoire), questions Q-CA3-n, écarts, items à former, estimation révisée. Écris-le aussi dans `<scratchpad>/s2bis/calib3/RAPPORT-GENERATEUR.md`, couvert par ton `SHA256SUMS`.
