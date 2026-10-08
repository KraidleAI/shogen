# Lot PLAN-S2BIS : données de S2 pour la préparation de S2-bis

Rattachement : G0 `docs/adr-0029/G0-lot-PLAN-S2BIS.md` ; ADR-0029 révision 3, §2.6 (règle de τ et σ de BTC/USD, recopiée
mot pour mot dans `parametres.json`, clé `regle_adr0029_l178_180`) et §6 lot 3 ; annexe B d'ADR-0028 (SHOGEN-TAU-REDERIV-1,
SHOGEN-R1-HOTE-STRUCTUREL-1, SHOGEN-POSTPREREG-PARAMS-SCEAU-1, SHOGEN-FICHE-WORKER-POSTEXEC-1). Chaque sortie porte en
première ligne : « préparation de S2-bis ; ne change pas le verdict de S2 (« R1 discrimine » = FAUX) ».

| fichier | rôle |
|---|---|
| `parametres.json` | tous les paramètres, fixés avant toute exécution sur les journaux, avec leur source |
| `commun.py` | harnais de `f35a70c` importé d'une extraction (modules contrôlés par sha256), lecture des journaux (segment J28, plage D5 exclue), pools S2 (D1) et D1-bis, classement, contrôle de cohérence (n, K, P̂_more par strate contre le bloc 3 du rendu J28), sortie fail-closed |
| `regles.py` | quantile au rang le plus proche, règle de τ (grille, bornes), règle de σ |
| `tau_sigma.py` | sortie 1, TAU-SIGMA-S2BIS : τ_c et σ_c par classe de source, valeurs pour le paquet de S2-bis |
| `episodes.py` | sortie 2 : longueurs d'épisodes de panne et d'écart par unité, courbe FIV_série(ℓ) |
| `okx.py` | sortie 3 : contribution de la paire de flux OKX à K de S2 |
| `lancer.sh` | lanceur unique : sha256 du paquet et des journaux contre le bloc machine, extraction de `f35a70c`, trois scripts |

Adjudications de l'orchestrateur (2026-10-04, avant tout calcul sur les journaux), écrites dans `parametres.json` :
- **A-1** : σ au paquet sur la population (B) de la règle de clôture d'ADR-0021 (répondantes statut ok, prix et horodatage
  porté, pool D1-bis ; clé `sigma_population` = `cloture`) ; la population (A), cellules à l'axe (i) sous le σ de S2, est
  imprimée, descriptive, avec les comptes au-delà du σ de S2 et la limite « σ_c ≤ max(plancher, 3 × σ_S2) ».
- **A-2** : à la borne haute de τ (≥ 2,85 %), refus nommé : la ligne `tau <classe>` porte REFUS et la valeur de la règle,
  jamais une valeur écrêtée ; la borne basse (0,05 %, seulement si P99,9 = 0) reste un écrêtage signalé.
- Choix du worker gardés par le G2 : pool D1-bis = D1 (a), (b) et seuil de l'annexe B.39, par strate ; épisodes classés
  sous les σ et τ committés de S2, coupés par toute fenêtre non retenue ; grille de ℓ de 1 à 1 440 fenêtres.

## Tests (fixtures seulement ; aucun journal réel)

Depuis ce dossier, contre le harnais du commit d'analyse :

    T=$(mktemp -d) && git -C ../.. archive f35a70c s2-harness | tar -x -C "$T"
    env -u SHOGEN_S2_CAMPAGNE_CONTROL PLAN_S2BIS_HARNAIS="$T/s2-harness" PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s tests -t .

Sans `PLAN_S2BIS_HARNAIS`, ou avec le harnais de la tête (`r1.py` différent de l'épingle), les tests refusent de
démarrer. `tests/test_lancer.py` crée un dépôt git jetable (`git init`, `git add`, `git write-tree`, aucun commit).
Poser `TMPDIR` dans le dossier d'écriture du lot ; chaque test retire son dossier temporaire.

**Exception écrite (adjudication A-3)** : `test_refus_commit_journal_variable_sortie_usage` pose
`SHOGEN_S2_CAMPAGNE_CONTROL` à une valeur fictive, dans le seul sous-processus du lanceur ; le lanceur refuse à sa
ligne 27 (code 3), et aucun test du harnais ne tourne dans ce sous-processus.

## Exécution sur les journaux scellés (phase 2, sur ordre de l'orchestrateur seulement)

1. Dans ce dossier, `sha256sum -c SHA256SUMS` sort 0, et chaque sha256 est égal aux épingles écrites au JOURNAL ; sinon,
   rien ne se lance.
2. Lancement détaché (durée non mesurée sur les journaux), dossier de sortie absent ou vide, dossier de travail neuf :
   `setsid nohup bash scripts/plan-s2bis/lancer.sh <journaux> <sortie> <travail> > <travail>.out 2>&1 &` ; fin constatée
   en sondant le PID. Codes : 0 trois scripts en 0 ; 2 usage ; 3 refus avant tout lancement ; 4 extraction impossible ;
   5 un script hors 0 (contrôle de cohérence en écart, ou refus nommé ; messages dans `<travail>/lancer.log`).
3. Le lanceur n'affiche que des noms, des codes et des sha256 ; il n'ouvre aucun journal (sha256sum seul) et n'affiche
   aucune sortie. Les sorties vont ensuite à `docs/adr-0029/plan-s2bis/`, avec leurs sommes.
