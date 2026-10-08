# Lot PLAN-S2BIS-2 : sorties du lancement unique (versement, E-P2-24)

Versé par l'orchestrateur le 2026-10-08 16:10:16 UTC (heure produite par `date -u`). Rattachement : G0 `docs/adr-0029/g0-plan2/G0-PLAN-S2BIS-2.md` et ses pièces ; annexe B, B.77 ; épinglage au JOURNAL du 2026-10-08 (commit `5316410`). Première ligne de chaque sortie : « préparation de S2-bis ; ne change pas le verdict de S2 (« R1 discrimine » = FAUX) ».

## Lancement
- Code : `scripts/plan-s2bis-2/`, commits `87901f8` à `4c6b602` ; `SHA256SUMS` du lot = `ffe6e5aaf683a782200d65c4ba1541556917fe788afce000d8c9ec5332a4d005`, contrôlé par le lanceur.
- Une commande, détachée, par l'orchestrateur : `setsid -w nohup bash scripts/plan-s2bis-2/lancer.sh <journaux> <sortie> <travail> <épingle>`, sur la copie de session des journaux scellés ; PID 12258 ; début 2026-10-08 16:06:12 UTC, fin 2026-10-08 16:09:34 UTC.
- Écran (noms, codes, sha256 seuls) : les trois journaux du bloc machine (`control.jsonl`, `journal.jsonl`, `raw.jsonl`) de sha256 égal au paquet ; passes A (`PYTHONHASHSEED` 0) et B (1), deux scripts chacune en code 0 ; **A = B** (les deux `SHA256SUMS` identiques à l'octet) ; copie de A ; code de sortie 0. `lancer.log` : 0 octet. Aucune relance.
- Interpréteur et outils : consignés au JOURNAL avec l'épinglage.

## Sorties
| fichier | rôle |
|---|---|
| `masque_j28.txt` | masque du J28 (contrôle (b)) |
| `fiv_unites.txt` | FIV par unité, et sensibilité au voisinage (contrôle (f)) |
| `intervalles.txt` | pauses complètes et de bord, épisodes complets (contrôle (e)) |
| `SHA256SUMS` | sommes des trois sorties, celles de la passe A |

Pièces de revue (G1 du générateur, G2 neuve, corrections, contre-contrôles, répétition à l'échelle) : `revue/`.

## Suite
Diff d'intégration côté SIM-BIS (nouvelle règle de C1, masque mesuré, retrait de `e1.ell_c1`) et sa relecture G2, avant E0 de SIM-BIS (G0, adjudication 5).
