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
- formes des API (SHOGEN-CALIB-FORMES-API-1, DETTES-T2 ; décision sur `RAPPORT.md` et ses ajouts datés) : aucun
  pari sur une borne ou un plafond non écrits.
  Demi-capacité (C-9) : une page ne demande jamais plus de ⌊`pas`/2⌋ créneaux, chevauchement compris (`pas` = maximum
  de la place, [lu] : Coinbase 300, Bitstamp 1000, Bitfinex 10000) ; `chevauchement` 1 pour Coinbase et Bitstamp
  (inclusion de `start` et de `end` non écrite : une minute de chaque côté, 148 et 498 minutes utiles), 0 pour
  Bitfinex (bornes incluses, [lu] ; 5000 minutes). Sous toute lecture où le plafond vaut `pas` (bougies ou créneaux,
  ancré au début, à la fin, ou au plus ⌈`pas`/2⌉ minutes avant `start`), une réponse n'est donc jamais coupée.
  Chargement : fichiers exactement les pages de `socle.pages` ; bougie hors de la fenêtre de sa page (bougies qui
  précèdent `start`, minute qui suit la fenêtre) écartée ; minute servie deux fois aux mêmes valeurs gardée une fois,
  aux valeurs différentes : CA/format nommé ; réponse de plus de bougies, à partir du départ, que de créneaux
  demandés : CA/format nommé. Binance et Kraken restent stricts.
  Garde (C-7, C-8) : une réponse d'au moins `pas` bougies, dont une avant le départ et aucune à la dernière minute de
  la page, est redemandée en deux demi-pages (`page-<début>.1.json` et `.2.json`), au même débit, qui la remplacent au
  chargement ; elle n'est refusée (CA/format : fin de page tronquée, ou demi-page redemandée plafonnée et tronquée)
  que sur preuve, si un fichier acquis porte une bougie entre sa dernière bougie et la dernière minute à couvrir ;
  sans preuve, ces minutes sont sans échange (lecture « les `pas` plus récentes jusqu'à `end` »).
  Limites (vérification de C-9, propriété du contre-contrôle rejouée) : un serveur qui décalerait sa fenêtre de
  quelques minutes quel que soit le plafond, ou ancrerait son plafond plus de ⌈`pas`/2⌉ minutes avant `start`, peut
  faire perdre des minutes sans refus ; les lignes de complétude le montreraient (déficit systématique par page).
  OKX (alignement UTC ou UTC+8 non écrit) : `voisins` 1, le mois précédent et le suivant sont acquis, seules les
  minutes de la fenêtre sont gardées, une minute hors des mois acquis (± 14 h) est refusée ; le mois qui suit la
  fenêtre descriptive (2026-10) n'est publié qu'après sa fin : jusque-là, l'acquisition sort en code 4 sur
  `REFUS CA/acquisition : mensuel 2026-10 non obtenu (téléchargement impossible (HTTPError)) ; un mensuel n'est publié
  qu'après la fin de son mois ; actif ETH ; place okx`.
  `calib_actifs.txt` porte, après septembre, les minutes reçues sur attendues de chaque place et de chaque fenêtre, au
  total et par page, et le nombre de pages redemandées (une perte systématique se voit), jamais décisifs ;
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
