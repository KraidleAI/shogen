# Brief — corrections de la relecture G2 d'intégration de P1 (C-1 à C-5), diffs CB-19a et suivants

Worker `shogen-worker`, effort max. Le dépôt `/home/user/shogen` est en lecture seule : **aucune opération git en écriture** (`git --no-optional-locks`). Lis `date -u` avant toute date. Tu travailles dans `<scratchpad>/s2bis/p1-integ/corr/` (scratchpad = `<scratchpad>`), avec un `TMPDIR` dédié. Tiens un `NOTES.md` ; après un compactage ou un redémarrage, reprends depuis lui, jamais depuis un `.jsonl`.

## Base

- Copie de la tête que l'orchestrateur te donne au lancement, par `git archive`, exclusions habituelles : `docs/rapports`, `docs/adr-0025`, `docs/adr-0028/monark-m009a`, `docs/adr-0028/execution`, `docs/15-*`, `docs/16-*`, `docs/pocket-report`.
- En parallèle, d'autres workers corrigent le recalcul (`recalc/lecteur.py`, `oracle_indep.py`, tests du recalcul) : n'y touche pas. L'orchestrateur recalera les planchers de la suite s2bis entre les séries.

## Pièces

- Relecture : `<scratchpad>/s2bis/p1-integ/G2-P1-INTEG-transcrit.md` (ACCEPTE-AVEC-CORRECTIONS, liste fermée C-1 à C-5) ; outils et preuves du réviseur : `<scratchpad>/s2bis/p1-integ/outils/`, `preuves/` (sonde du FORMAT, banc de l'écrivain avec coupures, bout en bout, mutants MI-01 à MI-30) ; `CLOTURE-P1.md`.
- Contrat : G0 `docs/adr-0029/g0-collecte/G0-COLLECTE-RECALC-DEPLOI.md` et ses ajouts datés, `PROPOSITION.md`, `AVIS.md` ; FORMAT `docs/adr-0029/s2bis/FORMAT-JOURNAUX-S2BIS.md` ; RFC 1035 dans `biblio/`.

## Adjudications de l'orchestrateur (liste fermée)

- **C-1** telle qu'écrite : (a) une réponse DNS de plus de 512 octets est `forme`, règle RFC 1035 §2.3.4 et §4.2.1 citée au FORMAT §12 (citation en anglais exacte, vérifiable dans `biblio/`) ; (b) borne au schéma de `sante.json` du nombre de témoins et de noms, calculée pour que la plus grande `sante` possible reste sous LIMITE, calcul écrit (FORMAT et METRIQUES). Tests : 513 octets, la réponse hostile du réviseur, `sante` maximale construite sous LIMITE ; mutant tué.
- **C-2** telle qu'écrite : (a) fsync du dossier après création d'un fichier du journal et du fichier de sommes ; (b) avant d'écrire une `reprise` en segment neuf, fsync des fichiers dont elle chaîne la dernière ligne intègre, dont elle déclare la queue, qu'elle somme. Tests par espion de fsync ; FORMAT §4 et §6.4. **Preuve exigée** : le banc à coupures du réviseur (`outils/banc_ecrivain.py`, modèle « chaque inode revient au plus à sa taille au dernier fsync ») rejoué sur le code corrigé, 300 graines : 0 rupture, 0 somme fausse (contre 128 et 131 avant). Le modèle ne couvre pas l'entrée de dossier : écris ce que le modèle prouve et ce qu'il ne prouve pas.
- **C-3** telle qu'écrite : (a) client réel dans la boucle, lecture pendante à E après dns et connexion (`panne_transport:delai`, phases présentes, adresse posée), tue MI-09 et MI-10 ; (b) l'adresse posée au suivi **avant** `phases["dns"]`, test par suivi espion ; (c) point d'entrée avec w > 1, tue MI-12 ; (d) délai et places lus de `formes.json` jusqu'à la boucle, tue MI-13 et MI-14. Rejoue les 30 mutants du réviseur : 30 tués attendus.
- **C-4**, FORMAT seul : (a), (b), (c) telles qu'écrites ; **(d) : l'écrire** (pas de changement du client au-delà de C-3 b) : l'adresse d'une lecture est l'adresse résolue ; elle n'a été contactée que si `phases` porte la connexion ; une `dns` rendue après une résolution tardive porte `phases.dns` et une adresse non contactée.
- **C-5** telle qu'écrite : (a) `oracle_record.py` : `--plancher` suit `[1-9][0-9]*`, test avec un commit `--plancher 0` ; (b) le runner échoue fermé (sortie 3) sur toute exception au chargement du vérificateur, `SystemExit` compris, test avec un vérificateur qui fait `sys.exit(0)` à son chargement. Aucun cas existant du runner retiré ni affaibli ; les leurres du réviseur CB-18 (`<scratchpad>/s2bis/cb18/cc*/travail/outils/leurres_*.py`) donnent les mêmes verdicts.
- Observations O-1 à O-4 : **pas de code** ; elles iront au registre.

## Règles

- **Tests d'abord**, rouge d'assertion montré avant le code.
- **Mutants** : au moins dix neufs par diff, plus les 30 du réviseur rejoués à la fin ; classés par la commande du job s2bis (runner, puis la ligne de `gates.yml`), borne 300 s, dépassement = FATAL.
- Bibliothèque standard seule. Python 3.10 à 3.13 en `-X dev -W error`.
- Diffs en série **CB-19a, CB-19b…**, chacun ≤ 200 lignes de code ajoutées, plancher exact relevé à chaque diff (`--egal`) ; METRIQUES par diff.
- R-13, R-8, octets 92 comptés juste ; lignes ≤ 120 caractères ; citations anglaises au FORMAT vérifiables dans `biblio/` (gate S-G5).
- `unshare -n` avec `lo` allumée (`<scratchpad>/s2bis/p1b/g2/travail/outils/isole.sh`) pour les jobs s2bis et S2 et pour tout bout en bout.
- `cargo --locked xtask verify` sur la copie : lignes de verdict seules ; S-G9 `docs/17:70` connu.
- Livrables : diffs, SHA256SUMS, journal G1 ([lu]/[abs]), tableau final C-1 à C-5 (diff, test, mutant).
- PID réel consigné ; pas de `pgrep -f` large ; nettoie tes copies lourdes à la fin.

## Interdits

- `docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, `docs/adr-0028/execution/` ; tout `*.jsonl` réel ; toute pièce de D.2 ;
- **toute recherche récursive (grep -r, git grep, du, find large) sur `docs/`, sur le dépôt entier ou sur le scratchpad entier**.

Rapport par message. Gate 0 : l'identifiant exact du modèle en tête. Résumé court en français, point par point.
