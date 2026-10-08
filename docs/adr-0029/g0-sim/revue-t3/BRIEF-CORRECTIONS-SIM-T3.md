# Brief — corrections G2 et avis de la tranche 3 du lot SIM-BIS (diffs SB-8D, SB-8E…, après SB-8C)

Worker `shogen-worker`, effort max. Le dépôt `/home/user/shogen` est en lecture seule : **aucune opération git en écriture**, et lis-le avec `git --no-optional-locks`. Lis `date -u` avant toute date. Tu travailles dans `<scratchpad>/s2bis/sim3/corr/`, avec un `TMPDIR` dédié.

## Base

Copie de la tête 3164348, par `git archive`, avec les exclusions `docs/rapports`, `docs/adr-0025`, `docs/adr-0028/monark-m009a`, `docs/adr-0028/execution`, `docs/15-*`, `docs/16-*` et `docs/pocket-report`. Puis les neuf diffs `…/sim3/diffs/SB-4I.diff` … `SB-8C.diff`, en série, avec les sha256 de `…/sim3/SHA256SUMS`.

## Pièces

- Relecture G2 : `…/sim3/g2/G2-SIM-T3-transcrit.md`. Verdict ACCEPTE-AVEC-CORRECTIONS, liste fermée C-1 à C-3.
- Outils, prototypes (`rev/outils/proto_corrections.py`) et mutants V-01 à V-28 : `…/sim3/g2/rev/`.
- Avis de l'advisor : `…/sim3/g2/AVIS-SIM-T3.md`.
- Ton rapport précédent : `…/sim3/g2/RAPPORT-WORKER-SIM-T3-transcrit.md`.
- Avis du recalcul sur les noms d'unité : `…/s2bis/rb1/g2/AVIS-RB-T1.md`, Q-RB-13.

**Contrat** : le G0 `docs/adr-0029/g0-sim/G0-SIM-BIS.md`, avec son ajout daté.

## Adjudications de l'orchestrateur (liste fermée de ce lot)

- **C-1** : `oracle()` couvre C_S quand S est suivie, par un refus `REGLE/oracle`. T-REG-2 est étendu à des instances où S est suivie.
- **C-2** : (a), (b) et (c), un cas par mutant vivant (V-02, V-25, V-22, V-20). Chaque cas est rouge sous le mutant et vert sur le code.
- **C-3** : dans ton rapport, recompte les octets 92 de tes outils, fichier par fichier.
- **Avis Q-T3-7 (modifié)** : l'instant de la perte est tiré sur la durée **nominale** W, et non sur T_max.
- **Avis Q-T3-13 (modifié)** : garde la construction. La loi du compte d'événements rend les deux queues, #{E^(r) ≥ E} et #{E^(r) ≤ E}. Test et oracle.
- **Avis Q-T3-15 (modifié)** :
  - la première unité est prise après les retraits D1-bis (a) et (b) et « presque mort », avant le critère collectif ;
  - si l'absorption la retire, toutes les unités sont décalées (ADR l.200) ;
  - pool vide : None.
  - La règle est écrite dans `ROTATION`, dans la docstring de `regle.py`, et en une ligne pour le futur RB-7.
- **Valeurs Q-T3-2 à Q-T3-16 adoptées par l'avis** (P-2) :
  - écris-les dans `parametres.json`, chacune avec sa source (lignes de l'AVIS-SIM-T3 et de la PROPOSITION), comme C-7 de la tranche 2 ;
  - marque le numéro Q-T3-n dans le code là où la valeur est employée ;
  - un test vérifie leur présence et leur forme sous le schéma.
- **P-7 (avis) : noms d'unité aux seuls caractères d'un nom d'hôte, en minuscules.**
  - Lettres, chiffres, « - » et « . », au plus 253 caractères, comme Q-RB-13 adoptée pour RB-6.
  - Refus nommé dans `_cle` et ses appelants.
  - Les noms courts actuels restent admis.
- **O-1 de la G2** : en stress, la loi regroupée est ancrée sur la liste scellée de calibration, et non plus sur le pool opérationnel. Retirer un hôte ne change alors plus l'état en stress des autres. Test de stabilité en stress, avec un rouge avant le code. Déclare la nouvelle empreinte d'identité.
- **O-4 de la G2** : refus nommé pour `observateurs.ue` ou `repli` ≥ M.
- **Restent en items, sans code dans ce lot** :
  - O-3, panne initiale contre première unité après retraits : à trancher au câblage de SB-11 ;
  - O-5, grille de la couche d'observateurs : avec les cellules de SB-11 ;
  - P-3, P-5, P-6, P-9 : briefs de SB-11 et SB-13 ;
  - Q-T3-1 : limite écrite.

## Règles

- Tests d'abord, avec un rouge d'assertion montré avant le code.
- Mutants, rejoués par la commande du job : runner, puis la ligne de `gates.yml`, borne de 300 s, dépassement = FATAL.
  - les 28 mutants du réviseur : tout vivant meurt, sauf R-28, qui est une limite ;
  - tes mutants de la tranche ;
  - au moins dix mutants neufs.
- Identité bit à bit sous Python 3.10 à 3.13 × PYTHONHASHSEED, avec les nouvelles empreintes déclarées.
- Bibliothèque standard seule.
- Diffs en série, **chacun ≤ 200 lignes de code ajoutées**, plancher exact relevé à chaque diff.
- R-13, R-8, octets 92 comptés juste.
- Réseau : `unshare -n`, avec `lo` allumée (`…/p1b/g2/travail/lo_up.py`, `isole.sh`).
- `cargo --locked xtask verify` sur la copie, lignes de verdict seules ; S-G9 `docs/17:70` est connu.
- Journal G1 et SHA256SUMS.
- Machine partagée : consigne le PID réel et lis `/proc/PID/cmdline` ; jamais de `pgrep -f` sur un motif large.
- Nettoie tes copies lourdes à la fin.
- **Après un compactage de contexte, reprends depuis un fichier de notes que tu tiens dans ton dossier, jamais depuis un `.jsonl`.**

## Interdits

- `docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, `docs/adr-0028/execution/` ;
- tout `*.jsonl`, y compris ton propre journal de session ;
- toute pièce de D.2 ;
- **toute recherche récursive (grep -r, git grep, du, find large) sur `docs/`, sur le dépôt entier ou sur le scratchpad entier**.

Rapport par message. Gate 0 : l'identifiant exact du modèle en tête. Résumé court en français, point par point.
