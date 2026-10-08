# Lot PLAN-S2BIS-2 : groupement des pannes, source par source (S2-bis)

Rattachement : G0 `docs/adr-0029/g0-plan2/G0-PLAN-S2BIS-2.md` (adjugé le 2026-10-05 17:06:39 UTC) et ses pièces
(`PERIMETRE-REDUIT.md`, `AVIS.md`, `PROPOSITION.md`) ; ADR-0029, ajout daté du 2026-10-05 17:06:39 UTC ; G0 de
SIM-BIS, ajout daté du 2026-10-05 15:05:43 UTC. Première ligne de chaque sortie : « préparation de S2-bis ; ne change
pas le verdict de S2 (« R1 discrimine » = FAUX) ».

| fichier | rôle |
|---|---|
| `parametres.json` | huit épingles de PLAN-S2BIS, comptes du masque (ADR-0029 l.31), voisinage, passes A et B |
| `socle.py` | refus nommés, variable, schéma, chargement épinglé (P-1), contrôles (a), (c), (d), CLI, en-tête |
| `masque_fiv.py` | `masque_j28.txt` (contrôle (b)) et `fiv_unites.txt` (contrôle (f), sensibilité au voisinage) |
| `intervalles.py` | `intervalles.txt` : pauses complètes et de bord, épisodes complets (contrôle (e)) |
| `lancer.sh` | lanceur unique : contrôles, extraction de `f35a70c`, passes A et B, comparaison, copie de A |

Réemplois, jamais modifiés, sous leurs sha256 : `commun.py`, `regles.py`, `episodes.py` (chargés sous ces noms),
`parametres.json` (sous-arbres de P-3 seuls), `tests/fixtures.py` et `SHA256SUMS` de `scripts/plan-s2bis/` ; EP et son
`SHA256SUMS`. Aucune formule de FIV, d'épisode, de pause, de quantile ni d'histogramme n'est écrite ici.

**Frontière, exception écrite au G0 (adjudication 4 ; E-P2-02 ; AV l.199)** : les journaux scellés de S2 et le rendu J28
ne sont lus que par les scripts de ce lot, à `f35a70c`, épinglés au JOURNAL et lancés une fois par l'orchestrateur ; le
rendu, par `commun.controle` seul (bloc 3). Aucun agent ne les ouvre, ne les liste ni ne les copie.

## Tests (fixtures seulement ; aucun journal réel)

Depuis ce dossier, contre le harnais du commit d'analyse, avec `TMPDIR` dans le dossier d'écriture :

    T=$(mktemp -d) && git -C ../.. archive f35a70c s2-harness | tar -x -C "$T"
    export PLAN_S2BIS_HARNAIS="$T/s2-harness" PYTHONDONTWRITEBYTECODE=1
    env -u SHOGEN_S2_CAMPAGNE_CONTROL python3 -B -m unittest discover -s tests -t .

Python 3.11 au moins (`hashlib.file_digest` de `commun.py`) ; le test d'identité exige python3.11, 3.12 et 3.13.
**Exception écrite (A-3 de PLAN-S2BIS ; E-P2-05)** : seul `tests/test_lancer.py` pose
`SHOGEN_S2_CAMPAGNE_CONTROL`, à une valeur fictive, dans le seul sous-processus du lanceur, qui refuse aussitôt
(code 3) ; la garde de `socle.py` lit un environnement passé en argument, et aucun autre test ne pose la variable.

## Lancement (sur ordre de l'orchestrateur, une fois, après l'épinglage au JOURNAL)

1. Dans ce dossier, `sha256sum -c SHA256SUMS` sort 0, et le sha256 de `SHA256SUMS` est celui du JOURNAL. Puis, détaché,
   sortie absente ou vide, travail neuf, PID consigné et fin constatée en sondant le PID :
   `setsid nohup bash scripts/plan-s2bis-2/lancer.sh <journaux> <sortie> <travail> <sha256> > <travail>.out 2>&1 &`
2. Codes : 0 deux scripts en 0 dans chaque passe et A = B ; 2 usage ; 3 refus avant tout lancement ; 4 extraction
   impossible ; 5 un script hors 0, ou A ≠ B. L'écran ne porte que des noms, des codes et des sha256.
3. Lettre de Q-P2-08 (PERIMETRE-REDUIT.md §7), mot pour mot :

> « un seul lancement ; dans ce lancement, deux passes A et B (`PYTHONHASHSEED` 0 et 1) ; sha256 comparés ; A ≠ B est
> un refus (code 5), aucune sortie n'est versée ni ouverte par quiconque, les deux `SHA256SUMS` seuls sont consignés ;
> la cause est cherchée sur fixtures ; toute relance est une déviation déclarée (E-P2-23) »
