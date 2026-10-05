# Lot SIM-BIS : SIM-NIVEAU-BIS ‖ SIM-PUISSANCE-BIS (préparation de S2-bis)

Rattachement : G0 `docs/adr-0029/g0-sim/G0-SIM-BIS.md`, dont le contenu est la proposition (`PROPOSITION.md`) corrigée par
l'avis de l'advisor (`AVIS.md`, qui prime) ; ADR-0029 révision 3, acceptée, avec ses ajouts datés (§2.4, §2.7, §6 lot 4,
§8). Données synthétiques seules ; seule entrée lue : les sorties versées de PLAN-S2BIS (`docs/adr-0029/plan-s2bis/`), sous
leurs empreintes. Aucun journal de campagne, aucun `*.jsonl`, aucune donnée de S2-bis.

| fichier | rôle | sous-lot |
|---|---|---|
| `parametres.json` | tous les paramètres, chacun avec sa source ; schéma fermé contrôlé par `commun.py` | SB-0 |
| `commun.py` | chargement de `parametres.json` (aucun flottant, aucune clé double, clés exactes), garde de la variable de campagne | SB-0 |
| `tests/` | tests unitaires, attendus écrits à la main ou produits par un outil distinct (`sha256sum`, `bc`) | chaque sous-lot |

## Tests

Depuis ce dossier, sans la variable de la copie scellée de S2 (le socle refuse de démarrer si elle est posée, même vide) :

    env -u SHOGEN_S2_CAMPAGNE_CONTROL PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s tests -t .

`TMPDIR` se pose dans le dossier de travail du lot (E-S-06). Aucun octet de barre oblique inverse dans les fichiers du lot :
un texte qui en porte un s'écrit par gabarit (`chr(92)`) et se contrôle sur les octets.
