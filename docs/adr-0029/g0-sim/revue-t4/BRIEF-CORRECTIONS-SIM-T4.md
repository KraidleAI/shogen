# Brief — corrections G2 et avis de la tranche 4 du lot SIM-BIS (diffs SB-14C, SB-14D…, après SB-14B)

Worker `shogen-worker`, effort max.

- Le dépôt `/home/user/shogen` est en lecture seule : **aucune opération git en écriture**. Utilise `git --no-optional-locks`.
- Lis `date -u` avant toute date.
- Tu travailles dans `<scratchpad>/s2bis/sim4/corr/`, avec un `TMPDIR` dédié.
- Tiens un fichier `NOTES.md`. Après un compactage ou un redémarrage, reprends depuis lui, jamais depuis un `.jsonl`.

## Base

- Copie de la tête 5f99ab5 par `git archive`, avec les exclusions habituelles.
- Puis les sept diffs `…/sim4/diffs/SB-9A.diff` à `SB-14B.diff`, en série, contrôlés par `…/sim4/SHA256SUMS`.
- L'orchestrateur committera en parallèle la tranche C de P1. Il recalera ton plancher sim-bis s'il le faut.

## Pièces

- Relecture G2 : `…/sim4/g2/G2-SIM-T4-transcrit.md` (ACCEPTE-AVEC-CORRECTIONS, C-1 à C-5).
- Outils et mutants R-01 à R-20 du réviseur : `…/sim4/g2/outils/` ; preuves : `…/sim4/g2/sorties/`.
- Avis de l'advisor : `…/sim4/g2/AVIS-SIM-T4.md`.
- Ton rapport précédent : `…/sim4/g2/RAPPORT-WORKER-SIM-T4-transcrit.md` ; tes notes et ton journal : `…/sim4/`.

**Contrat** : le G0 `docs/adr-0029/g0-sim/G0-SIM-BIS.md`, avec ses ajouts datés.

## Adjudications de l'orchestrateur (liste fermée)

- **C-1 à C-5** : telles qu'écrites par le réviseur.
  - C-1 : composition d'E1 dans `parametres.json`, section `e1`, sourcée, lue par `replication` ; test qui tue R-02 et R-03.
  - C-2 : R-04, R-06, R-07.
  - C-3 : verse les scripts et les sorties brutes des mesures de mise au point, avec les noms de cellule. Atteste qu'aucun n'est une cellule d'E1. Sinon, déclare-les « non versées ».
  - C-4 : le bon chiffre est 5 701.
  - C-5 : Q-T4-12 marqué dans `oracle_r1.charger`.
- **Q-T4-8, modifié par l'avis** : nom de cellule sans « / ». Choisis la forme de l'avis (par exemple `1_100`), écris-la dans `parametres.json`, et teste-la.
- **O-1** : trois cas à la main, chacun rouge sous son mutant.
  - R-05 : C1 = C2 admis, lettre du G0.
  - R-08 : nettoyage du dossier d'extraction.
  - R-15 : schéma du commit épinglé.
- **O-3** (cache d'`oracle_r1.charger`) : si c'est simple, le cache est indexé sur l'épingle. Sinon, décris la limite dans la docstring.
- **O-7** : refus nommés dans `selection` pour `ell_c1` absent et pour une strate manquante.
- **Valeurs Q-T4-1 à Q-T4-13 adoptées par l'avis** : la mention d'adjudication, forme P-2 de la tranche 3, dans `parametres.json` et le README, avec les lignes de l'avis.
- **Restent en items, sans code dans ce lot** :
  - O-2 : `fetch-depth` contrôlé par K-03, à faire après le commit de P1-C qui touche le runner ;
  - O-4 et les lignes de l'avis pour le brief de SB-11 : oracle E-S-29 de la variante, écart-type des 200 FIV ;
  - O-5 : seuil déclaré sous E-4 ;
  - O-6 : limite.

## Règles

- **Tests d'abord**, avec un rouge d'assertion montré avant le code.
- **Mutants**, rejoués par la commande du job (runner, puis la ligne de `gates.yml`, borne de 300 s ; dépassement = FATAL) :
  - les 20 du réviseur : tout vivant meurt, sauf R-16 (équivalent pour la sélection) et R-17 (indétectable en local), à justifier ;
  - ton M-VAR-1b reste vivant, équivalent démontré ;
  - au moins dix mutants neufs.
- Identité bit à bit sous Python 3.10 à 3.13 × PYTHONHASHSEED ; nouvelles empreintes déclarées.
- Bibliothèque standard seule.
- Diffs en série, **chacun ≤ 200 lignes de code ajoutées**, plancher exact relevé à chaque diff.
- R-13, R-8, octets 92 comptés juste.
- `unshare -n` avec `lo` allumée (`…/p1b/g2/travail/outils/isole.sh`).
- `cargo --locked xtask verify` : lignes de verdict seules ; S-G9 `docs/17:70` est connu.
- **Livrables** : journal G1 et SHA256SUMS.
- Consigne le PID réel ; pas de `pgrep -f` sur un motif large.
- Nettoie tes copies lourdes à la fin.

## Interdits

- `docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, `docs/adr-0028/execution/` ;
- tout `*.jsonl` ; toute pièce de D.2 ;
- **toute recherche récursive (grep -r, git grep, du, find large) sur `docs/`, sur le dépôt entier ou sur le scratchpad entier**.

Rapport par message. Gate 0 : l'identifiant exact du modèle en tête. Résumé court en français, point par point.
