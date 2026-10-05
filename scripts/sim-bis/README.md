# Lot SIM-BIS : SIM-NIVEAU-BIS ‖ SIM-PUISSANCE-BIS (préparation de S2-bis)

Rattachement : G0 `docs/adr-0029/g0-sim/G0-SIM-BIS.md`, dont le contenu est la proposition (`PROPOSITION.md`) corrigée par
l'avis de l'advisor (`AVIS.md`, qui prime) ; ADR-0029 révision 3, acceptée, avec ses ajouts datés (§2.4, §2.7, §6 lot 4,
§8). Données synthétiques seules ; seule entrée lue : les sorties versées de PLAN-S2BIS (`docs/adr-0029/plan-s2bis/`), sous
leurs empreintes. Aucun journal de campagne, aucun `*.jsonl`, aucune donnée de S2-bis.

| fichier | rôle | sous-lot |
|---|---|---|
| `parametres.json` | tous les paramètres, chacun avec sa source ; schéma fermé contrôlé par `commun.py` | SB-0 |
| `commun.py` | chargement de `parametres.json` (aucun flottant, aucune clé double, clés exactes), garde de la variable de campagne ; entrées lues sous deux épingles (`parametres.json`, puis le `SHA256SUMS` de PLAN-S2BIS) ; écriture atomique sans écrasement ; étiquette et en-tête des sorties ; JSON canonique | SB-0 |
| `aleas.py` | flux par (cellule, réplication, composant, indice) : 8 premiers octets de SHA-256, puis `random.Random`, dont seule la méthode `random()` est rendue ; graine de règle par réplication ; `seuil(x)`, plus petit flottant ≥ x rationnel, d'où des tirages exacts (Bernoulli, loi empirique, loi géométrique par tables et `bisect`), sans fonction transcendante | SB-1 |
| `tests/` | tests unitaires, attendus écrits à la main ou produits par un outil distinct (`sha256sum`, `bc`) | chaque sous-lot |
| `tests/test_fitness.py` | frontière du moteur lue par `ast` (bibliothèque standard et lot seuls ; ni `shogen_s2`, ni `shogen_s2bis`, ni import dynamique, ni module réseau ; adaptateurs `oracle_r1.py` et `oracle_recalc.py` à part, E-S-01) ; aucun octet de barre oblique inverse ; aucune fonction transcendante de libm dans le moteur (E-S-43) | SB-0, SB-1 |

CI : job `sim-bis-unittest` de `.github/workflows/gates.yml`, jugé par `enforcement/verdict-suite-s2.py scripts/sim-bis
--aucun-saut --egal --plancher N`, N égal au compte des tests, relevé à chaque sous-lot ; étapes lues par le cas K-03 du runner.

## Tests

Depuis ce dossier, sans la variable de la copie scellée de S2 (le socle refuse de démarrer si elle est posée, même vide) :

    env -u SHOGEN_S2_CAMPAGNE_CONTROL PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s tests -t .

`TMPDIR` se pose dans le dossier de travail du lot (E-S-06). Aucun octet de barre oblique inverse dans les fichiers du lot :
un texte qui en porte un s'écrit par gabarit (`chr(92)`) et se contrôle sur les octets.
