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
  Couverture double (C-13, Coinbase et Bitstamp, `couverture` 2 ; Bitfinex, bornes lues, reste simple) : un second
  découpage décalé d'une demi-page (74 et 249 minutes), de début − demi-page à fin + demi-page au moins, fichiers
  `double-<début>.json` ; chaque minute est couverte par deux requêtes d'ancrages différents. Chargement : fichiers
  exactement ceux des deux découpages ; bougie hors de la fenêtre de sa page (bougies qui précèdent `start`, minute
  hors fenêtre) écartée de la série ; minute servie deux fois aux mêmes valeurs gardée une fois, aux valeurs
  différentes : CA/format nommé (« couverture double discordante » si le second découpage est en cause) ; réponse de
  plus de bougies, à partir du départ, que de créneaux demandés : CA/format nommé. Contrôle de chaque réponse, sans
  modèle du plafond : une bougie servie par n'importe quel fichier entre la première bougie de la réponse (ou le début
  de sa page) et la dernière minute de sa page, absente de la réponse : CA/format (« couverture double discordante » ;
  « fin de page tronquée » pour une page du premier découpage suspecte au sens de C-7 ; demi-page : son motif).
  Réponse dont toutes les bougies suivent la fin demandée et son chevauchement (décalage vers l'avant, R-2 du
  contre-contrôle cc2 ; un décalage plus long que la fenêtre la laisserait vide sans preuve) : CA/format nommé ; une
  bougie isolée après la fin reste écartée (pt 2 de la décision).
  Binance et Kraken restent stricts.
  Garde (C-7, C-8, C-14) : une réponse d'au moins `pas` bougies, dont une avant le départ et aucune à la dernière
  minute de la page, est redemandée en deux demi-pages (`<page>.1.json` et `.2.json`), au même débit, qui la
  remplacent au chargement ; une page d'un seul point n'est jamais redemandée.
  Sonde de première bougie (C-15, couverture double) : sondes de ⌊`pas`/2⌋ créneaux, la première en fin − ⌊`pas`/2⌋
  minutes, puis, tant qu'elles reviennent vides, en recul de ⌊`pas`/2⌋ (2^j − 1) minutes jusqu'à `historique.debut`
  (2009-01-03, avant toute cotation), enfin dichotomie depuis `historique.debut` jusqu'à la plus précoce non vide
  (`sonde-<x>.json`, environ 24 par paire et par fenêtre, rejouées au chargement) ; T0 = sa première bougie.
  CA/avant-historique : requête de la fenêtre partant moins de `pas` − ⌊`pas`/2⌋ + 1 minutes après T0 ; réponse
  portant une bougie au plus tard en T0 (plafond ancré avant le début de l'historique) ; aucune sonde non vide, que
  la fenêtre serve des bougies ou non (R-1 du contre-contrôle cc2 : un décalage, ou un plafond ancré avant start, de
  plus que la fenêtre rend toutes les sondes vides quand l'historique commence entre leur portée et celle de la
  dernière requête, qui sert alors seule des bougies, toutes hors de la fenêtre).
  Limite résiduelle mesurée (L-C13-2, sans item) : un décalage ou un retard de plus d'une demi-page au-delà de la fin
  n'est pas vu si toutes les fins de page des deux découpages sont sans échange : 32 cas sur 60 000 dans la propriété
  du générateur, fenêtres de 1 à 10 minutes, dont 23 à chevauchement 0, configuration absente des places du lot en
  couverture double (c = 1) ; la propriété du contre-contrôle cc2 (24 000 cas) trouve 11 pertes de queue, fenêtres
  jusqu'à 27 minutes, et 29 autres hors de ce compte : 28 en marché mince (densité 0,3 ou moins, fenêtres jusqu'à 95
  minutes) et 1 à densité 1 dont toutes les fins de page des deux découpages sont muettes (fenêtre de 15 minutes, 5
  échangées) ; une fenêtre du lot (87 pages ou plus par découpage) le verrait dès un seul échange dans une fin de
  page. En miroir (R-2 du contre-contrôle cc2), un décalage vers l'avant de plus d'une demi-page mais de moins d'une
  requête n'est pas vu au début de la fenêtre si tous les débuts de page sont sans échange.
  Résidu de R-1 et R-2 (propriété cc2) : 66 pertes vers l'avant ; 64 où rien n'est servi pour la fenêtre (le
  décalage porte toutes les requêtes au-delà de la fin des données), 1 miroir ci-dessus (fenêtre d'une minute), 1 en
  marché mince (densité 0,1 ; décalage de 58 minutes, plus long que la fenêtre de 28 : toutes les réponses décalées
  tombent sur des minutes sans échange, donc rien n'est servi, comme les 64). Une fenêtre où rien n'est servi est
  indiscernable au chargement d'une fenêtre muette, admise par conception : la garde est au calcul (Q-DT2-11).
  OKX : mensuels découpés en UTC+8, établi sur pièce (DECISION de FORMES-API-1, ajout daté du 2026-10-09 19:51:45 UTC :
  le mensuel ETH-USDT de 2026-09 va du 2026-08-31 16:00 au 2026-09-30 15:59 UTC) ; `voisins` 1, le mois précédent et
  le suivant sont acquis, seules les minutes de la fenêtre sont gardées, une minute hors des mois acquis (± 14 h) est
  refusée ; le mois qui suit la fenêtre descriptive (2026-10) n'est publié qu'après sa fin : jusque-là, l'acquisition
  sort en code 4 sur `REFUS CA/acquisition : mensuel 2026-10 non obtenu (téléchargement impossible (HTTPError)) ; un
  mensuel n'est publié qu'après la fin de son mois ; actif ETH ; place okx`.
  `calib_actifs.txt` porte, après septembre, les minutes reçues sur attendues de chaque place et de chaque fenêtre, au
  total et par page, le nombre de pages redemandées et celui du second découpage (une perte systématique se voit),
  jamais décisifs ;
- `bougies.py` : six lecteurs, normalisation, dernier prix connu et âges, oracle d'exécution de SH §4 ;
- `sigma.py` : σ par classe, troisième terme (P99 des âges par cellule, places à horodatage de dernière transaction) ;
- `tau.py` : place de la lecture sans minute active dans la fenêtre (rien de servi, ou minutes toutes sans échange) :
  CA/population, avant tout calcul (Q-DT2-11 : sans elle, Coinbase vide passait, σ des places horodatées changé) ;
  population et médiane leave-one-out, τ des places, des agrégateurs et des oracles, fragment et son
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
