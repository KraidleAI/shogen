# Lot CALIB-ACTIFS : τ et σ d'ETH, d'USDC et d'USDT sur historiques publics (préparation de S2-bis)

Rattachement : G0 `docs/adr-0029/g0-calib/G0-CALIB-ACTIFS.md` et son ajout daté (INV-1 = A), dont le contenu est
`PROPOSITION.md` corrigée par `AVIS.md` ; ADR-0029 l.185-191 et ajouts datés du 2026-10-08 (l.403, l.405) ;
`docs/adr-0029/calib/SOURCES-HISTORIQUES.md`. Première ligne de chaque sortie, mot pour mot : « préparation de S2-bis ;
calibration d'ETH, d'USDC et d'USDT sur historiques publics ; ne lit aucune donnée de S2 ni de S2-bis » (clé
`etiquette` du fragment JSON).

- `parametres.json` : fenêtres, strates, lectures A (retenue) et A-prime, unités, classes, séries (URL, formats),
  sommes de Kraken (SH §7), oracle de SH §4, τ, σ, Chainlink, cadence, réseau, passes ;
- `socle.py` : refus nommés, garde de la variable, lecture stricte, épingle et bloc de `tau_sigma.txt`, fenêtre et
  strates, planchers des oracles, quantile et règle de grille (Q-CA-13), écriture `.partiel` ;
- `acquerir.py` : étape réseau ; mensuels de Binance (`.CHECKSUM`) et d'OKX, archive de Kraken lue par plages, pages de
  Coinbase, Bitstamp et Bitfinex à débit borné, manifeste et reprise ;
- `bougies.py` : six lecteurs, normalisation, dernier prix connu et âges, oracle d'exécution de SH §4 ;
- `sigma.py` : σ par classe, troisième terme (P99 des âges par cellule, places à horodatage de dernière transaction) ;
- `tau.py` : population et médiane leave-one-out, τ des places, des agrégateurs et des oracles, fragment et son
  contrôle, descriptifs, septembre, sorties ; point d'entrée du calcul ;
- `lancer.sh` : lanceur unique (épingle, étape réseau, passes A et B, identité, copie) ;
- `cadence.py` : relevé de cadence des agrégateurs (Q-CA-11 modifiée), hors du lanceur.

Aucune barre oblique inverse dans le lot ; bibliothèque standard seule ; arithmétique en Decimal et Fraction.

## Tests (fixtures synthétiques seulement ; aucun historique réel, aucun réseau)

Depuis ce dossier : `env -u SHOGEN_S2_CAMPAGNE_CONTROL python3 -B -m unittest discover -s tests -t .` ; job
`calib-actifs-unittest` de `.github/workflows/gates.yml`. Les tests retirent les variables de mandataire et posent une
garde réseau (boucle locale seule) ; le serveur des tests d'acquisition écoute sur 127.0.0.1. Le vrai `tau_sigma.txt`
n'y est que haché ou copié, jamais interprété. Exception écrite (E-CA-03) : seul `tests/test_lancer.py` pose
`SHOGEN_S2_CAMPAGNE_CONTROL`, à une valeur fictive, dans le seul sous-processus du lanceur. L'identité (T-CA-DET-1)
tourne sous l'interpréteur de la suite et chaque `python3.10` à `python3.13` présent ; la matrice 3.10 à 3.13 en
`-X dev -W error` reste une étape écrite du G3 opérant et de la G2.

## Lancement (orchestrateur seul, une fois, après la G2 et l'épinglage au JOURNAL, E-CA-27 et E-CA-28)

1. Dans ce dossier, `sha256sum -c SHA256SUMS` sort 0 et le sha256 de `SHA256SUMS` est celui du JOURNAL ; le dossier ne
   porte que les fichiers de `SHA256SUMS` (et des dossiers), `__pycache__` compris refusé. Puis, détaché, PID consigné
   et fin constatée en sondant le PID :
   `setsid nohup bash scripts/calib-actifs/lancer.sh <bruts> <sortie> <travail> <sha256> > <travail>.out 2>&1 &`
2. Codes : 0 (A = B, sorties copiées) ; 2 usage ; 3 refus avant tout lancement ; 4 acquisition impossible ; 5 calcul
   hors 0, A ≠ B ou écriture impossible. Un lancement coupé par une borne de temps se refait et ne se compte pas ;
   l'étape réseau reprend sur le manifeste des bruts.
3. Sorties : `calib_actifs.txt`, `fragment_analyse.json`, `manifeste.tsv`, `SHA256SUMS`. Les octets bruts restent hors
   du dépôt (référence : URL, taille, sha256 du manifeste). Le fragment entre à `s2bis/config/analyse.json` au lot du
   paquet, avec les valeurs de BTC (E-CA-29). Sous un refus CA/borne, une ligne descriptive suit le refus dans
   `calib_actifs.txt` : la valeur calculée de la règle, nommée, jamais décisive (le refus et le JSON n'en portent pas).
   Le calcul va au bout pour chaque actif (SHOGEN-CALIB-BORNE-MULTI-1) : le refus écrit est celui du premier actif
   refusé ; chaque actif à la borne a sa ligne de valeur, dans l'ordre des actifs, puis chaque refus suivant sans
   valeur a sa ligne `descriptif hors refus (jamais décisif) : refus suivant : <refus>` (exception non nommée :
   CA/calcul, type seul), chaque texte une fois et jamais celui du refus écrit (un refus global aux paramètres se
   lève à chaque actif) ; le JSON ne porte que le refus.

## Relevé de cadence (séparé, avant le sceau)

`python3 scripts/calib-actifs/cadence.py --sortie <fichier>` : 120 lectures à 60 s (deux heures), horodatages seuls ;
versé daté, hors du lancement du lot.
