# Brief — lot PLAN-S2BIS-2, sous-lots P2R-0 à P2R-5 (groupement des pannes source par source ; code et tests, fixtures seules)

Worker `shogen-worker`, effort max. Le dépôt `/home/user/shogen` est en lecture seule : **aucune opération git en écriture** (`git --no-optional-locks`). Lis `date -u` avant toute date. Tu travailles dans `<scratchpad>/s2bis/plan2/code/` (scratchpad = `<scratchpad>`), avec un `TMPDIR` dédié. Tiens un `NOTES.md` ; après un compactage ou un redémarrage, reprends depuis lui, jamais depuis un `.jsonl`.

## Contrat (lis-le d'abord)

- **G0 du lot** : `docs/adr-0029/g0-plan2/G0-PLAN-S2BIS-2.md` (commis) et ses pièces dans le même dossier : `PERIMETRE-REDUIT.md` (**ta spécification** : §1 fichiers et épingles, §2 sous-lots, tests et mutants, §3 exigences, §4 refus nommés, §5 bilan, §7 lettre de Q-P2-08, §9 précisions P-1 à P-9 adoptées), `AVIS.md` (adopté, ses trois modifications comprises), `PROPOSITION.md` (exigences E-P2-01 à E-P2-29, telles que modifiées par le périmètre réduit).
- ADR-0029 et son ajout daté de ce jour ; G0 de SIM-BIS `docs/adr-0029/g0-sim/G0-SIM-BIS.md` et son ajout daté du 2026-10-05 15:05:43 UTC.
- Lot PLAN-S2BIS, réemployé par chemin et sha256, **jamais modifié** : `scripts/plan-s2bis/` (`commun.py`, `episodes.py`, `regles.py`, `parametres.json`, `tests/fixtures.py`, `SHA256SUMS`, `lancer.sh` en lecture) ; `docs/adr-0029/plan-s2bis/episodes.txt` (EP) et son `SHA256SUMS`.
- Le cas échéant : `scripts/sim-bis/oracle_r1.py` (forme de l'extraction de `f35a70c`, AV l.89).

## Base

- Copie de la tête que l'orchestrateur te donne au lancement, par `git archive`, exclusions habituelles : `docs/rapports`, `docs/adr-0025`, `docs/adr-0028/monark-m009a`, `docs/adr-0028/execution`, `docs/15-*`, `docs/16-*`, `docs/pocket-report`.
- Le harnais de `f35a70c` s'extrait par `git archive` **avec les mêmes exclusions** (P-9 ; item SHOGEN-PLAN-S2BIS-EXCLUSIONS-1) ; vérifie après extraction, chemin par chemin, l'absence de `docs/adr-0028/execution` et des autres dossiers exclus, sans jamais ouvrir un fichier de ces dossiers.

## Livrables

- Six diffs en série **P2R-0 à P2R-5**, sous `scripts/plan-s2bis-2/` (§1), chacun **≤ 200 lignes de code ajoutées** (règle de coupe du §1 si besoin, déclarée) ; avec tests, mutants et METRIQUES par diff.
- Le job CI est différé (Q-P2-12, item SHOGEN-PLAN-S2BIS-CI-1) : **ne touche pas** `.github/workflows/gates.yml` ni le runner. La suite du lot se lance par `python3 -B -m unittest discover` dans `scripts/plan-s2bis-2` (ou la forme que le périmètre fixe), compte exact relevé à chaque diff.
- Identité bit à bit des sorties sur fixtures sous Python 3.10 à 3.13 × `PYTHONHASHSEED` 0 et 1 (T-P2-DET-1) ; empreintes déclarées.
- Journal G1 ([lu]/[abs]), SHA256SUMS de ton dossier, tableau final des exigences E-P2 et des refus du §4, chacun avec le test qui le fixe.

## Règles

- **Tests d'abord**, rouge d'assertion montré avant le code, sous-lot par sous-lot.
- **Mutants** : tous ceux du §2 (M-P2-nn), plus au moins deux neufs à toi par sous-lot ; lancés par la commande de la suite du lot, borne 300 s (dépassement = FATAL) ; un vivant est tué ou déclaré équivalent avec démonstration.
- Bibliothèque standard seule ; aucun flottant dans `parametres.json` ; aucune formule de FIV, d'épisode, de pause, de quantile ni d'histogramme écrite par le lot (§0 point 1) : tout passe par les fonctions épinglées de PLAN-S2BIS et par r1 extrait.
- `-X dev -W error` sous 3.10 à 3.13. R-13, R-8, octets 92 comptés juste, lignes ≤ 120 caractères.
- `cargo --locked xtask verify` sur la copie : lignes de verdict seules ; S-G9 `docs/17:70` est connu.
- `unshare -n` avec `lo` allumée (`<scratchpad>/s2bis/p1b/g2/travail/outils/isole.sh`) pour la suite.
- Consigne le PID réel de tes processus ; pas de `pgrep -f` sur un motif large ; nettoie tes copies lourdes à la fin (extractions de `f35a70c` comprises).
- Si le périmètre est muet ou contredit le code de PLAN-S2BIS : question Q-P2R-n, avec ton choix et sa raison ; ne tranche pas une valeur.

## Interdits (durs)

- **Aucun journal réel de S2 ni de S2-bis**, scellé ou copié, où qu'il soit : tu ne le lis pas, ne le listes pas, ne le cherches pas. **Tu ne lances jamais `lancer.sh`** (ni celui de PLAN-S2BIS ni le tien) hors des tests sur fixtures. Seul l'orchestrateur lancera le lot, une fois, après l'épinglage au JOURNAL.
- Aucune lecture du rendu J28 réel hors du bloc 3 déjà versé à EP.
- `docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, `docs/adr-0028/execution/` ; tout `*.jsonl` ; toute pièce de D.2.
- **Toute recherche récursive (grep -r, git grep, du, find large) sur `docs/`, sur le dépôt entier ou sur le scratchpad entier.**

Rapport par message à la fin des six sous-lots (ou à un blocage). Gate 0 : l'identifiant exact du modèle en tête. Résumé court en français, point par point.
