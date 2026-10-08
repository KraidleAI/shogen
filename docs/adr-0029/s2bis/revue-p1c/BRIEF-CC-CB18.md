# Brief — points CC-1 et CC-2 du contre-contrôle de P1 tranche C, et incise O-1 (diffs CB-18r, CB-18s…)

Toi, worker des corrections de CB-18, effort max.

- Le dépôt `/home/user/shogen` est en lecture seule : **aucune opération git en écriture**. Lis-le avec `git --no-optional-locks`.
- Lis `date -u` avant toute date.
- Tu travailles dans `<scratchpad>/s2bis/cb18/corr2/`, avec un `TMPDIR` dédié.

## Base

La série recalée, sur la tête poussée **5f99ab5**.
- Copie de 5f99ab5 par `git archive`, avec les exclusions habituelles.
- Puis les 20 diffs `…/s2bis/cb18/rebase/diffs/`, dans l'ordre suivant : CB-18a à CB-18f, ENREG-ROLE, SEGMENT-JOUR, ENTIER-ECRIVAIN, CB-18g à CB-18q. Contrôle-les par `…/rebase/diffs/SHA256SUMS`.
- Arbre attendu : f342a14b. Plancher s2bis 183, sim-bis 129, S2 406 avec `--egal`.

## Pièces

- Le contre-contrôle : `…/s2bis/cb18/cc/CONTRE-CONTROLE-CB18-transcrit.md`.
- Ses preuves et outils : `…/cb18/cc/travail/preuves/` et `outils/`, en particulier :
  - `poc-remede-cc1.diff` et `.txt` ;
  - `poc-remede-cc2.diff` et `.txt` ;
  - `leurres-sq.txt`, `mutants-CC-sq.txt` ;
  - les 20 leurres de `…/cc/travail/leurres/`.
- Ton rapport précédent : `…/cb18/corr/RAPPORT-CORRECTIONS-CB18-transcrit.md` ; tes notes `…/cb18/corr/NOTES.md`.

## Adjudications de l'orchestrateur (liste fermée)

- **CC-1, remède (a).**
  - K-01 à K-03 contrôlent `runs-on`, le checkout épinglé et les trois étapes sur les lignes brutes, à indentation exacte, dans le bloc du job. Ce contrôle remplace la présence de texte dans des lignes dépouillées.
  - Le docstring de `cable()` dit exactement ce qui est contrôlé.
  - Les 8 leurres admis (N-01, N-02, N-03, N-04, N-17, N-18, N-19, N-20) sont refusés. N-01 et N-02 entrent au runner comme cas L ; ajoute aussi tout autre leurre dont la classe n'est pas déjà couverte.
  - C'est un serrage de gate : aucun cas existant du runner n'est affaibli, et le compte monte.
  - La preuve du réviseur te guide, mais le code est le tien.
- **CC-2.** Trois cas qui tuent CA-01, CA-07 et CA-12 :
  - `env:` simple de premier niveau ;
  - clé `runs-on` (ou autre clé de job) répétée ;
  - étapes imitées hors de `steps`.
  Le rouge de chacun est montré sous son mutant.
- **O-1 (adopté).** Au FORMAT §7.4, ajoute l'incise « (un objet nu rend déjà la ligne non intègre, §7.1 d) ». Ajoute aussi la phrase de l'avis l.78 sur les reprises déclarées, si elle n'y est pas mot pour mot. Les lecteurs appliquent le §7.1 avant le §7.4. Ne change aucune autre lettre.
- **O-2 (item, sans code).** Écris seulement, au FORMAT §5, une ligne de limite : un dossier par journal ; un préfixe qui en prolonge un autre dans le même dossier fait refuser le plus court (`JOURNAL/nom`). L'orchestrateur forme l'item SHOGEN-S2BIS-PREFIXE-NOM-1.
- **N-12 et N-14** restent dans le résidu ANALYSEUR-RESIDUS-1 (forge et validité YAML) : aucun code.

## Règles

- **Tests d'abord**, avec le rouge montré avant le code.
- **Mutants**, rejoués par la commande du job (runner, puis ligne de `gates.yml`, borne de 300 s, réseau isolé, dépassement = FATAL) :
  - CA-01 à CA-12 du réviseur ;
  - les 20 leurres du réviseur (`leurres_cc.py`) ;
  - au moins dix mutants neufs, dont des leurres neufs.
- Bibliothèque standard seule : PyYAML n'entre pas dans le code. Le réviseur ne s'en servait que comme témoin.
- Diffs en série, chacun ≤ 200 lignes de code ajoutées. Plancher exact relevé à chaque diff.
- Python 3.10 à 3.13 en `-X dev -W error` pour s2bis ; job S2 Ran 406 ; job sim-bis 129.
- `cargo --locked xtask verify` sur la copie : S-G9 `docs/17:70` est connu.
- R-13, R-8, octets 92 comptés.
- METRIQUES : ta section par diff, en fin de fichier.
- **Livrables** : journal G1 et SHA256SUMS.
- Machine partagée :
  - consigne le PID réel ; jamais de `pgrep -f` sur un motif large ;
  - nettoie tes copies lourdes à la fin.
- Après un compactage, reprends depuis tes notes, jamais depuis un `.jsonl`.

## Interdits

- `docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, `docs/adr-0028/execution/` ;
- tout `*.jsonl` ; toute pièce de D.2 ;
- `recalc/lecteur.py` et l'oracle de RB-18 ;
- **toute recherche récursive (grep -r, git grep, du, find large) sur `docs/`, sur le dépôt entier ou sur le scratchpad entier**.

Rapport par message. Gate 0 : l'identifiant exact du modèle en tête. Résumé court en français, point par point.
