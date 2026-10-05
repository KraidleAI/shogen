# Métriques du paquet `s2bis/` : baseline G4 et fonctions de fitness

- **Rattachement** : PROPOSITION du G0 des lots COLLECTE-BIS, RECALC-BIS et DEPLOI-BIS (`docs/adr-0029/g0-collecte/`),
  exigence E-C-41 : fonctions de fitness dès CB-0, baseline versée (lignes et tests par module, score de mutation par
  sous-lot) ; leçon de SHOGEN-G4-RECALCUL-METRIQUES-1 (annexe B d'ADR-0028, l.892).
- **Mesures** : lignes physiques par `wc -l` ; tests par `unittest` (compte de la découverte, sans sous-tests) ;
  campagnes de mutants classées par la sortie du lanceur (SHOGEN-MUT-FATAL-1 : 1 tué par le test nommé, 0 vivant, toute
  autre sortie FATAL), témoin vert avant chaque campagne. Chaque sous-lot ajoute sa section à la fin de ce fichier.

## Fonctions de fitness

| fonction | test | ce qu'elle refuse |
|---|---|---|
| frontière d'imports | `test_fitness.Fitness.test_frontiere_du_paquet`, `test_frontiere_refuse` | import hors bibliothèque standard et hors sous-paquet, import relatif sortant, import dynamique, sous-paquet sans règle ; `recalc` : ni `collecte` (décodeurs compris, RB-1g) ni `shogen_s2` (RB-0a) |
| absence de réseau | `test_garde.Garde` (garde posée par `tests/__init__.py`) | connexion, envoi, résolution hors boucle locale, même sous un attrape-tout |
| déterminisme | `test_fitness.Fitness.test_memes_octets_sous_cinq_graines`, `test_rotation.Lois.test_memes_octets_sous_cinq_graines_de_hachage` (RB-6b) | sortie qui dépend de la graine de hachage (`PYTHONHASHSEED` de 0 à 4) |
| compilation | `test_fitness.Fitness.test_compilation_avertissements_en_erreur` | avertissement de compilation (séquence d'échappement invalide, par exemple) |
| copie de la lecture JSON stricte | `test_fitness.Fitness.test_copie_de_la_lecture_json_stricte` (RB-1g) | une des deux copies (`collecte/config.py` l.20-46, `recalc/config_analyse.py`) modifiée sans l'autre (Q-RB-1) |

## CB-0a (2026-10-04) : paquet, configuration scellée, garde réseau

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/__init__.py` | 2 | — |
| `shogen_s2bis/collecte/__init__.py` | 1 | — |
| `shogen_s2bis/collecte/config.py` | 70 | 4 (`tests/test_config.py`, 57 lignes) |
| `tests/__init__.py` (garde réseau) | 35 | 2 (`tests/test_garde.py`, 32 lignes) |

Mutants : 19 tués sur 19 (0 vivant, 0 FATAL au passage retenu ; un passage antérieur, invalide, comptait un mutant
inapplicable, FATAL, corrigé puis relancé). Suite : 6 tests.

## CB-0b (2026-10-04) : fitness et CI

| fichier | lignes | tests |
|---|---|---|
| `tests/test_fitness.py` | 68 | 4 |
| `enforcement/verdict-suite-s2.py` (options `--aucun-saut`, `--plancher`) | 25 ajoutées, 9 retirées | cas V-14, V-15, C-03 à C-05 du runner |
| `enforcement/tests/run-fixtures-verdict-suite-s2.py` | 42 ajoutées, 5 retirées | 27 cas, dont K-01 et K-02 (étapes des deux jobs) |
| `.github/workflows/gates.yml` (job `s2bis-unittest`) | 25 ajoutées, 1 retirée | — |

Mutants : 20 tués sur 20 (0 vivant, 0 FATAL). Suite : 10 tests ; plancher du job : 10.

## CB-1a (2026-10-04) : écrivain chaîné (chaîne canonique, fsync au marqueur, point horaire, fenêtres)

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/collecte/journal.py` | 100 | 4 (`tests/test_journal.py`, 98 lignes) |

Mutants : 19 tués sur 19 (0 vivant, 0 FATAL). Suite : 14 tests ; plancher du job : 14.

## CB-1b (2026-10-04) : verrou exclusif

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/collecte/journal.py` | 113 | 5 (`tests/test_journal.py`, 118 lignes) |

Mutants : 4 tués sur 4 (0 vivant, 0 FATAL ; le mutant « verrou bloquant » est tué par le délai interne du test, 5 s).
Suite : 15 tests ; plancher du job : 15.

## CB-2a (2026-10-04) : fichiers quotidiens, clôture, sommes

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/collecte/journal.py` | 139 | 1 (`tests/test_fichiers.py`, 29 lignes : deux bascules, 1 442 fenêtres) |

Mutants : 11 tués sur 11 (0 vivant, 0 FATAL). Suite : 16 tests ; plancher du job : 16.

## CB-2b (2026-10-04) : reprise, queues, segments, borne de ligne

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/collecte/journal.py` | 219 | 9 (`tests/test_reprise.py`, 108 lignes) |

Mutants : 15 tués sur 15 (0 vivant, 0 FATAL). Suite : 25 tests ; plancher du job : 25.

## CB-2c (2026-10-04) : trous et causes, sommes rattrapées

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/collecte/journal.py` | 243 | 7 (`tests/test_trous.py`, 75 lignes) ; 2 de plus dans `tests/test_reprise.py` (132 lignes) |

Mutants : 14 tués sur 14 au dernier passage (0 vivant, 0 FATAL). Premier passage : 10 tués, 2 vivants (M-2c-04,
M-2c-07) ; tests renforcés (un cas « reprise, marqueur sans trou, puis saut » ; assertion élargie au doublon de trou),
campagne relancée ; puis deux mutants ajoutés avec le durcissement contre l'imbrication excessive (M-2c-13, M-2c-14).
Suite : 34 tests ; plancher du job : 34.

## CB-2d (2026-10-04) : corrections C-1, C-2 et C-6 (a) de la relecture G2 de la tranche A de P1

Objet : `window_start` non décroissant dans une exécution et dernière fenêtre écrite restaurée à la reprise (C-1) ;
écrivain inutilisable après une `OSError`, verrou toujours rendu, aucun descripteur refermé (C-2) ; refus contrôlé
avant toute bascule et tout trou, au rang réel de l'enregistrement (C-6 (a)). La ligne qui avançait l'état après un
trou dans `_fenetre` est retirée : avec le contrôle préalable, `marqueur` l'écrasait toujours (le mutant M-2c-07 de
CB-2c ne s'applique plus).

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/collecte/journal.py` | 289 | — |
| `tests/test_journal.py` | 147 | 7 (2 de plus : fsync en échec, verrou rendu malgré une fermeture en échec) |
| `tests/test_reprise.py` | 159 | 13 (2 de plus : écriture partielle, fenêtre non entière relue comme queue) |
| `tests/test_trous.py` | 122 | 10 (3 de plus ; 2 renforcés pour S-1 et S-2 ; 3 réécrits, dont la prémisse de Q-4) |
| `tests/test_fichiers.py` | 35 | 2 (1 de plus : bascule en échec, puis `fermer`) |

Mutants (lanceur des corrections, même contrat ; témoin vert ; réseau isolé par `unshare -n`) : 19 tués sur 19 par
leur test visé (0 vivant, 0 FATAL), dont les deux qu'exige C-1 (d). Suite : 42 tests ; plancher du job : 42.

## CB-2e (2026-10-04) : corrections C-3, C-4 et C-5, option `--egal` (Q-2) de la relecture G2 de la tranche A de P1

Objet : structure cyclique refusée en temps borné (C-3) ; plancher par défaut et option `--plancher` exercés, aucun
`if:` dans les deux jobs unittest (C-4) ; tests qui tuent les vivants non équivalents de la G2 (C-5) ; `--egal` au
seul job s2bis, Ran égal au plancher (Q-2, adjugée par l'orchestrateur).

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/collecte/journal.py` | 291 | — |
| `tests/test_journal.py` | 179 | 9 (2 de plus : refus nommés à l'ouverture, cycle ; 3 renforcés : M-07, G-13, G-19) |
| `tests/test_reprise.py` | 205 | 18 (5 de plus : G-01 et M-18, G-02, G-07, G-08, G-10 et G-11 ; 1 renforcé : G-06) |
| `tests/test_config.py` | 59 | 4 (1 renforcé : G-20) |
| `tests/test_garde.py` | 33 | 2 (1 renforcé : M-26) |
| `enforcement/verdict-suite-s2.py` (option `--egal`) | 13 ajoutées, 7 retirées | cas V-16, V-17 et C-08 du runner |
| `enforcement/tests/run-fixtures-verdict-suite-s2.py` | 15 ajoutées, 8 retirées | 32 cas, dont C-06 à C-08, V-16, V-17 |
| `.github/workflows/gates.yml` (job `s2bis-unittest`) | 2 ajoutées, 1 retirée | ligne du vérificateur : `--egal --plancher 49` |

Mutants : 11 tués sur 11 par leur test visé (0 vivant, 0 FATAL). Suite : 49 tests ; plancher du job : 49, égalité
exigée par `--egal`.

### Campagnes du réviseur G2 rejouées après les corrections (C-6 (d))

Les deux jeux du réviseur (`mutants_g2.py`, 41 mutants ; `mutants_prec.py`, 32), chargés sans changement, rejoués sur
l'état final (CB-2c, CB-2d, CB-2e) par le lanceur des corrections, même contrat, témoins verts, réseau isolé :

| jeu | mutants | tués par leur test visé | vivants | FATAL |
|---|---|---|---|---|
| `mutants_g2.py` | 41 | 41 | 0 | 0 |
| `mutants_prec.py` | 32 | 32 | 0 | 0 |

- Les 19 vivants non équivalents de la relecture sont tués : M-07, M-18, M-26, M-28, M-29, M-32 ; G-01 à G-08,
  G-10, G-11, G-13, G-19, G-20 (G-27 et G-29 sont les doublons de M-32 et M-28).
- G-26 (plancher du job abaissé à 1) relevait de Q-2 : il est tué par l'étape du job, que `--egal` fait refuser
  (Ran 49 > plancher 1). Contre le seul runner, qui lit les étapes sans compter les tests, il survit.
- Sept fragments ne s'appliquaient plus au texte changé par CB-2d et CB-2e. Ils sont réécrits sur le nouveau texte,
  avec la même mutation : M-12, M-20, M-31, M-33, M-47, G-18 et G-26.
- Aucune équivalence n'a été invoquée.

## CB-3a (2026-10-04) : lecture typée, octets de la requête, analyse de la réponse

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/collecte/lecture.py` | 34 | 3 (`tests/test_http.py`, classe `LectureTypee`) |
| `shogen_s2bis/collecte/http.py` (partie sans réseau) | 68 | 6 (`tests/test_http.py`, classes `Requete` et `Analyse` ; 97 lignes en tout) |

Mutants : 14 tués sur 14 (0 vivant, 0 FATAL). Suite : 58 tests ; plancher du job : 58, égalité exigée (`--egal`).

## CB-3b (2026-10-04) : lecture par phases (IPv4, TLS, délai global, attrape-tout)

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/collecte/http.py` | 125 | 9 (`tests/test_http_reseau.py`, 140 lignes : serveurs factices de boucle locale) |

Mutants : 15 tués sur 15 au dernier passage (0 vivant, 0 FATAL). Premier passage : 14 tués, 1 vivant (M-3b-15, seconde
adresse prise au lieu de la première : le résolveur injecté n'en rendait qu'une) ; résolveur injecté porté à deux
adresses, campagne relancée. Suite : 67 tests ; plancher du job : 67, égalité exigée (`--egal`).

## CB-4 (2026-10-04) : boucle du pool

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/collecte/boucle.py` | 83 | 6 (`tests/test_boucle.py`, 116 lignes : horloge et attentes injectées, journal réel) |

Mutants : 16 tués sur 16 (0 vivant, 0 FATAL). Suite : 73 tests ; plancher du job : 73, égalité exigée (`--egal`).

## CB-5 (2026-10-04) : tests « lecture pendue » (T-LP-1 à T-LP-6) et leurs mutants

| fichier | lignes | tests |
|---|---|---|
| `tests/test_lecture_pendue.py` | 135 | 8 (T-LP-1 à T-LP-5 ; T-LP-6 en deux tests : corps au goutte-à-goutte, dernière attente bornée au temps qui reste ; corps maximal sous la borne de ligne, SHOGEN-S2BIS-CORPS-BORNE-1) |

Aucun code de production. Chaque test a son propre délai : boucle dans un fil joint en 5 s ; T-LP-4 en sous-processus
(fils et horloge réels, w = 1 s, délai de 30 s). Dans T-LP-3, le client garde son horloge réelle (suivi propre) :
l'horloge factice de la boucle n'est jamais comparée à l'heure réelle (rebase sur la tête du 2026-10-04 22:40 UTC ;
mesure : avec une horloge factice antérieure à l'heure réelle, le résultat tardif tombait en `dns` et le test durait
cinq secondes de plus). Mutants : 14 tués sur 14 au dernier passage (M-LP-1 en deux formes, injectée et réelle, M-LP-2
à M-LP-8, fils non démons, attente de départ ignorée, place jamais rendue, délai entier redonné à chaque opération,
plafond du client porté à 4 Mio ; 0 vivant, 0 FATAL). Premier passage : 11 tués, 1 vivant, M-LP-8 écrit « délai entier
à chaque opération, contrôle du temps restant gardé », que le goutte-à-goutte ne distingue pas ; M-LP-8 réécrit
« délai par opération seulement » (aucun temps restant), et un test de plus tue la première forme (M-5-04). Suite : 81
tests ; plancher du job : 81, égalité exigée (`--egal`).

## CB-10a (2026-10-04) : DNS filaire, requête et analyse de la réponse

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/collecte/dns.py` (format filaire) | 77 | 4 (`tests/test_dns.py`, 64 lignes) |

Valeurs de référence : octets écrits à la main selon la RFC 1035 ; les quatre réponses ont été analysées par c-ares
(Node 22, en boucle locale) avec les mêmes valeurs. Mutants : 18 tués sur 18 au dernier passage (0 vivant, 0 FATAL).
Premier passage : 16 tués, 1 vivant (M-10a-09, contrôle de la taille des données SOA : redondant avec `struct.unpack`,
qui exige 20 octets) ; contrôle retiré, mutant remplacé. Suite : 85 tests ; plancher du job : 85, égalité exigée (`--egal`).

## CB-10b (2026-10-04) : requête DNS en UDP

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/collecte/dns.py` | 106 | 2 de plus (`tests/test_dns.py`, 118 lignes : serveur UDP factice de boucle locale) |

Mutants : 12 tués sur 12 au dernier passage (0 vivant, 0 FATAL). Premier passage : 11 tués, 1 vivant (M-10b-12, délai
doublé : la borne haute du test était trop large) ; borne resserrée, délai du test porté à 0,2 s, campagne relancée.
Suite : 87 tests ; plancher du job : 87, égalité exigée (`--egal`).

## CB-11a (2026-10-04) : sondes de santé (D-3 brute, D-4, D-5, disque, empreinte du résolveur)

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/collecte/sante.py` | 80 | 4 (`tests/test_sante.py`, 89 lignes : commande, requêtes DNS et lancement injectés) |

Mutants : 15 tués sur 15 (0 vivant, 0 FATAL). Limite : le mutant « blocs libres pour l'administrateur au lieu des blocs
disponibles » (M-11a-07) n'est tué que sur un système de fichiers qui réserve des blocs (ext4 de l'hôte de session :
oui). Suite : 91 tests ; plancher du job : 91, égalité exigée (`--egal`).

## CB-11b (2026-10-04) : sondes branchées à la boucle, liste blanche de `sante`

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/collecte/boucle.py` | 89 | 1 (`tests/test_sante.py`, classe `Branchement` ; 114 lignes en tout) |

Mutants : 10 tués sur 10 au dernier passage (0 vivant, 0 FATAL). Premier passage : 9 tués, 1 hors cible (M-11b-02,
mutant mal écrit : bloc vide, erreur de syntaxe, le test nommé n'a pas tourné) ; mutant corrigé, campagne relancée.
Suite : 92 tests ; plancher du job : 92, égalité exigée (`--egal`).

## CB-11c (2026-10-05) : corrections C-1, C-6 et C-7 (boucle), observation O-5, de la relecture G2 de la tranche B

Objet : état des lectures et des sondes relevé une seule fois à l'échéance, avant toute écriture ; lecture non finie
au relevé, ou finie après E, classée à E (`fin` = E, phases et adresse atteintes à E) et comptée tardive ensuite (C-1) ;
boucle des tests dans un fil joint en temps borné, exception du fil relevée dans le test (C-6) ; tests nommés des
mutants vivants MG-11, MG-13 et MG-29 (C-7) ; futur rendu même si une lecture lève une BaseException (O-5).

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/collecte/boucle.py` | 94 | — |
| `tests/test_boucle.py` | 225 | 10 (4 de plus : échéance exacte sous écrivain ralenti, place rendue, pool plein sans attente, BaseException) |
| `tests/test_sante.py` | 132 | 6 (1 de plus : sonde rendue après l'échéance, null) |
| `tests/test_lecture_pendue.py` | 131 | 8 (fil borné partagé, `borne` de `test_boucle`) |

Mutants, classés par la commande du job (SHOGEN-S2BIS-MUT-COMMANDE-1 : ligne `verdict-suite-s2.py s2bis --aucun-saut
--egal --plancher 97` de `gates.yml`, suite entière, borne de 300 s, dépassement FATAL) : 14 tués sur 14 par leur test
visé (0 vivant, 0 FATAL), dont MG-11, MG-13, MG-29 du réviseur et M-LP-3 du worker, qui sort désormais en 1 en 76 s
(la suite pendait). Suite : 97 tests ; plancher du job : 97, égalité exigée (`--egal`).

## CB-11d (2026-10-05) : correction C-5, observation O-7 et mutant MG-26 (C-7) de la relecture G2 de la tranche B

Objet : une sonde dont l'instance précédente n'a pas rendu n'est pas relancée (null), une sonde qui lève rend null et
repart, au plus un fil par sonde ; nombre de sondes vivantes journalisé (`fils.sondes`) (C-5) ; `sante` complète sans
sondes (O-7) ; test nommé du mutant vivant MG-26 (C-7).

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/collecte/sante.py` | 103 | — |
| `shogen_s2bis/collecte/boucle.py` | 95 | — |
| `tests/test_sante.py` | 191 | 10 (4 de plus : sonde pendue jamais relancée, sonde qui lève, disque du dossier du journal, sondes pendues sur trois fenêtres) |
| `tests/test_boucle.py` | 228 | 10 (santé complète sans sondes, `fils.sondes`) |

Mutants (commande du job, `--plancher 101`, borne de 300 s) : 11 tués sur 11 par leur test visé (0 vivant, 0 FATAL),
dont MG-26 et deux mutants du réviseur réécrits sur le texte de CB-11d avec la même mutation (MG-12, sondes non
attendues ; MG-27, sonde inachevée non nulle). Suite : 101 tests ; plancher du job : 101, égalité exigée (`--egal`).

## CB-11e (2026-10-05) : correction C-4 et mutant MG-23 (C-7) de la relecture G2 de la tranche B

Objet : délais de `lire` et `interroger` comptés sur l'horloge monotone, instants journalisés sur l'horloge murale ;
temps écoulé depuis `depart` retranché, jamais négatif ; `horloges` de la `sante` (temps écoulé depuis le relevé
précédent, sur chaque horloge) : un recul de l'horloge murale entre deux fenêtres s'y lit (C-4, ferme
SHOGEN-S2BIS-HORLOGE-RECUL-JOURNAL-1) ; test nommé du mutant vivant MG-23 (C-7).

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/collecte/lecture.py` | 40 | — |
| `shogen_s2bis/collecte/http.py` | 127 | — |
| `shogen_s2bis/collecte/dns.py` | 108 | — |
| `shogen_s2bis/collecte/boucle.py` | 103 | — |
| `tests/test_boucle.py` | 248 | 11 (1 de plus : recul de l'horloge murale entre deux fenêtres) |
| `tests/test_http.py` | 98 | 9 (horloge monotone entière, en microsecondes) |
| `tests/test_http_reseau.py` | 181 | 11 (2 de plus : recul pendant une lecture, S-C1 ; `depart` posé après le début) |
| `tests/test_dns.py` | 145 | 8 (2 de plus : recul pendant une requête, S-C2 ; MG-23) |

Mutants (commande du job, `--plancher 106`, borne de 300 s) : 12 tués sur 12 (0 vivant, 0 FATAL), dont MG-23 et M-LP-8
réécrits sur le texte de CB-11e avec la même mutation ; M-11e-06 (délai DNS doublé) est tué par
`test_delai_reseau_forme_et_identifiant_aleatoire`, et non par le test qu'il visait. Suite : 106 tests ; plancher du
job : 106, égalité exigée (`--egal`).

## CB-11f (2026-10-05) : correction C-2 et mutants MG-18, MG-19, MG-21, MG-24 (C-7) de la relecture G2 de la tranche B

Objet : un datagramme qui ne répond pas à la requête (source, identifiant, bit QR, une seule question, la même) est
ignoré et l'attente continue ; `forme` réservé à une réponse appariée mal formée ; adresse qui n'est pas une IPv4
littérale canonique refusée en `forme`, sans exception, résolution ni envoi (C-2) ; tests nommés des mutants vivants
MG-18, MG-19, MG-21 et MG-24 (C-7).

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/collecte/dns.py` | 119 | — |
| `tests/test_dns.py` | 191 | 13 (5 de plus : TXT en latin-1, types d'étiquette réservés, datagrammes non appariés, adresse non littérale, identifiant sur 16 bits) |

Mutants (commande du job, `--plancher 111`, borne de 300 s) : 12 tués sur 12 par leur test visé (0 vivant, 0 FATAL),
dont MG-18, MG-19, MG-24, et MG-17 et MG-21 réécrits sur le texte de CB-11f avec la même mutation. MG-22 (rcode sur
3 bits) reste équivalent en pratique (relecture G2) : non rejoué ici. Suite : 111 tests ; plancher du job : 111,
égalité exigée (`--egal`).

## CB-11g (2026-10-05) : correction C-3 et mutant MG-31 (C-7) de la relecture G2 de la tranche B

Objet : `CONTEXTE` armé comme le contexte d'urllib en S2 (ALPN `http/1.1`, authentification après poignée annoncée) ;
ClientHello mesurée en boucle locale avant et après (outil du réviseur), mêmes extensions qu'urllib sous Python 3.10 à
3.13 (C-3 (a)) ; tests sans réseau des attributs de `CONTEXTE` (ClientHello écrite en mémoire) et du chemin TLS réussi
par une couche injectée (C-3 (b), tuent MG-01 à MG-03) ; test nommé du mutant vivant MG-31 (C-7).

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/collecte/http.py` | 131 | — |
| `tests/test_http_reseau.py` | 261 | 14 (3 de plus : contexte TLS d'urllib, poignée réussie par une couche injectée, connexion sans réponse) |

Mutants (commande du job, `--plancher 114`, borne de 300 s) : 10 tués sur 10 par leur test visé (0 vivant, 0 FATAL),
dont MG-01, MG-02, MG-03 et MG-31 du réviseur. Suite : 114 tests ; plancher du job : 114, égalité exigée (`--egal`).

### Mutants du réviseur G2 et du worker rejoués sur l'état final, par la commande du job (C-6, C-7)

Lanceur des corrections (SHOGEN-S2BIS-MUT-COMMANDE-1 : ligne du job `--egal --plancher 114` lue dans `gates.yml`,
suite entière, borne de 300 s, dépassement FATAL ; témoins verts ; réseau isolé) :

| jeu | mutants | tués | vivants | inapplicables (texte changé) |
|---|---|---|---|---|
| `mutants_g2.py` du réviseur (MG-01 à MG-30) | 30 | 24 | 1 (MG-22, équivalent en pratique selon la relecture) | 5 |
| `mutants_g2_b.py` du réviseur (MG-31) | 1 | 1 | 0 | 0 |
| M-LP du worker (`mutants-final-cb5.py`) | 14 | 11 | 0 | 3 |
| formes réécrites des huit inapplicables, même mutation | 8 | 8 | 0 | 0 |

- Les dix vivants non équivalents de C-7 sont tués : MG-11, MG-13, MG-18, MG-19, MG-21 (réécrit), MG-23 (réécrit),
  MG-24, MG-26, MG-29, MG-31 ; MG-01 à MG-03 le sont aussi (C-3 (b)).
- M-LP-3 (marqueur écrit seulement quand tous les fils ont fini) sort en 1 en 79 s : la suite échoue en temps borné au
  lieu de pendre (C-6).
- Réécrits sur le nouveau texte : MG-12, MG-27, M-LP-1a (CB-11d), MG-23, M-LP-8 (CB-11e), MG-17, MG-21 (CB-11f),
  M-LP-6 (CB-11c). Aucune équivalence invoquée hors MG-22.

## RB-0a (2026-10-05) : paramètres d'analyse, lecture stricte et schéma (RECALC-BIS, partie P3)

Objet : sous-paquet `recalc` et sa règle de frontière (bibliothèque standard et `recalc` seuls, PROPOSITION §1 pt 2) ;
`config_analyse.py` : fichier des paramètres d'analyse scellés lu en octets, sha256 des octets, JSON strict (clé
double, nombre à virgule, constante non finie, entier de plus de 30 chiffres), blocs à fixer par un lot amont (null au
premier niveau) refusés d'abord, puis schéma : seuils de D-2 à D-5, gardes, n_s, T_max, R et seuil, tolérance des
événements, P_j, τ et σ par (actif, classe de source), unités par classe.

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/recalc/__init__.py` | 1 | — |
| `shogen_s2bis/recalc/config_analyse.py` | 111 | 3 (`tests/test_config_analyse.py`, 77 lignes) |
| `tests/test_fitness.py` | 74 | 4 (règle de `recalc`, cas de refus de `recalc`) |

Mutants, classés par la commande du job (runner, puis ligne `verdict-suite-s2.py s2bis --aucun-saut --egal
--plancher 117` de `gates.yml`, suite entière, borne de 300 s, réseau isolé) : 21 tués sur 21 par leur test visé
(0 vivant, 0 FATAL). Suite : 117 tests ; plancher du job : 117, égalité exigée (`--egal`).

## RB-0b (2026-10-05) : règles de τ, de σ et des noms d'unité, cohérence, gabarit `analyse.json`

Objet : τ en fraction décimale écrite en chaîne, 0,05 % <= τ < 2,85 % (refus nommé, jamais d'écrêtage) ; σ au moins
égal au plancher de sa classe (30, 300, 5 400 s), null pour les places sans horodatage ; noms d'unité en ASCII
imprimable sans « : » ; cohérence : alpha = 0,01 exactement ((seuil + 1) × 100 = R + 1), T_max sur la grille de 60 s,
grille de P_j strictement croissante et seuil dans la grille, unités en ordre strict des points de code, pools
d'ETH, d'USDC et d'USDT pris parmi les hôtes de BTC ; gabarit `s2bis/config/analyse.json` : valeurs fixées par
l'ADR-0029 remplies, blocs des lots amont (n_s, T_max, τ et σ, tolérance des événements, unités) à null, donc refusé
tant qu'ils ne sont pas fixés.

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/recalc/config_analyse.py` | 143 | 8 (`tests/test_config_analyse.py`, 151 lignes ; 5 de plus) |
| `config/analyse.json` | 12 | 1 (valeurs de l'ADR, blocs des lots amont, gabarit complété accepté) |

Mutants (commande du job, runner puis `--plancher 122`, borne de 300 s, réseau isolé) : 20 tués sur 20 par leur test
visé (0 vivant, 0 FATAL), dont « R = 9 998 au gabarit ». Suite : 122 tests ; plancher du job : 122, égalité exigée
(`--egal`).

## RB-6a (2026-10-05) : décalages o(r, u) de la loi de rotation, sens du décalage

Objet : `rotation.py`, entrée de SHA-256 scellée (AVIS Q-R-02 : chaîne ASCII « graine:strate:r:u », graine en 64
hexadécimaux minuscules, strate `calme` ou `stress`, r de 1 à 9 999 sans zéro de tête, unité en ASCII imprimable sans
« : »), entier big-endian des 32 octets modulo n, refus nommés avant tout calcul ; décalage d'un masque de n bits, la
valeur de la position t allant en (t + o) mod n. Contrat et vecteurs : `docs/adr-0029/s2bis/ROTATION-S2BIS.md`.

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/recalc/rotation.py` | 55 | 3 (`tests/test_rotation.py`, 46 lignes : six vecteurs calculés hors du code par `sha256sum` et `bc`, dont o = 0 et o = n − 1 ; refus nommés ; masques décalés écrits à la main) |

Mutants (commande du job, runner puis `--plancher 125`, borne de 300 s, réseau isolé) : 18 tués sur 18 par leur test
visé (0 vivant, 0 FATAL), dont « sens du décalage inversé » et « modulo autre que la longueur de la suite retenue ».
Suite : 125 tests ; plancher du job : 125, égalité exigée (`--egal`).

## RB-6b (2026-10-05) : lois de K et de S sous les rotations jointes par hôte

Objet : `compter` (K par le compteur « au moins deux » sur masques, S par les paires d'unités), `resume` (C = #{r :
K^(r) >= K}, K_crit = plus petit k tel que #{r : K^(r) >= k} <= seuil, moyenne exacte en `Fraction`), `lois` (R
rotations, décalage commun à toutes les classes pour un même hôte, première unité jamais décalée, classes triées,
refus nommés de toutes les entrées) ; R et seuil passés par l'appelant depuis `analyse.json`.

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/recalc/rotation.py` | 107 | 8 (`tests/test_rotation.py`, 133 lignes ; 5 de plus : comptage naïf position par position sur 24 tirages de deux classes jointes, R = 9 999 jusqu'à la dernière rotation, résumé fait à la main aux bornes du seuil 99, refus nommés, mêmes octets sous cinq graines de hachage) |

Mutants (commande du job, runner puis `--plancher 130`, borne de 300 s, réseau isolé) : 17 tués sur 17 par leur test
visé au second passage (0 vivant, 0 FATAL), dont « classe dans l'entrée du hachage », « première unité décalée »,
« une rotation de moins » et « > au lieu de >= dans C ». Premier passage invalide, arrêté : M-6b-01 a atteint la
borne de 300 s (FATAL), le diff de `unittest` sur deux listes de 9 999 valeurs ne se terminant pas ; l'assertion compare
désormais des booléens, puis la campagne a été relancée en entier. Coût mesuré : `ROTATION-S2BIS.md` §6. Suite :
130 tests ; plancher du job : 130, égalité exigée (`--egal`).

## RB-1a (2026-10-05) : lecteur en flux, ligne intègre et ordre des fichiers

Objet : `lecteur.py`, intégrité d'une ligne au sens de l'écrivain de référence (FORMAT §7.1, `collecte/journal.py`
`_lire` : saut de ligne final, JSON canonique, chaîne dans le fichier, première ligne `ouverture` ou `reprise`, champs
typés comme l'écrivain les relit), cause nommée de toute ligne non intègre (`LECTEUR/fin`, `json`, `canonique`,
`chaine`, `champ`, `flottant`, `entier-long`), entier JSON de plus de 640 chiffres nommé quel que soit le réglage
`int_max_str_digits` de l'interpréteur (SHOGEN-JSON-ENTIER-LONG-1, transposé) ; fichiers d'un préfixe dans l'ordre de la
chaîne (jour, segment en entier) ; aucun fichier : refus nommé `LECTEUR/absent`.

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/recalc/lecteur.py` | 82 | 4 (`tests/test_lecteur.py`, 76 lignes) |

Mutants (commande du job, runner puis `--plancher 134`, borne de 300 s, réseau isolé) : 20 tués sur 20 par leur test
visé (0 vivant, 0 FATAL). Suite : 134 tests ; plancher du job : 134, égalité exigée (`--egal`).

## RB-1b (2026-10-05) : lecture en flux, genèse, lien entre fichiers, ruptures, queue finale

Objet : itération du lecteur, ligne à ligne (LIMITE octets au plus), sans jamais tenir un fichier en mémoire ; genèse
(`seq` 0, `prec` nul, `ouverture`) et lien de chaque fichier au précédent contrôlés (FORMAT §7.7) ; toute rupture
(`LECTEUR/lien`, `LECTEUR/queue-non-declaree`) rendue à sa place dans le flux, sans arrêt ni réparation, le premier
enregistrement qui la suit devenant l'ancre ; queue d'un fichier relevée (position, octets, sha256, cause), tolérée en
fin de journal (`queue_finale`) ; état remis à zéro à chaque lecture.

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/recalc/lecteur.py` | 136 | 11 (`tests/test_lecteur.py`, 202 lignes ; 7 de plus, journaux écrits par l'écrivain de `collecte/journal.py`) |

Mutants (commande du job, runner puis `--plancher 141`, borne de 300 s, réseau isolé) : 16 tués sur 16 par leur test
visé (0 vivant, 0 FATAL), dont « contrôle de lien sauté » et « lien contrôlé sur seq seul ». Suite : 141 tests ;
plancher du job : 141, égalité exigée (`--egal`).

## RB-1c (2026-10-05) : déclaration des queues par la reprise, mémoire bornée

Objet : une queue relevée doit être déclarée, champ pour champ (fichier, position, octets, sha256), par la `reprise` qui
la suit (FORMAT §7.4) ; null sans queue en attente ; déclaration différente : rupture `LECTEUR/declaration` ; queues
déclarées relevées (`queues`). Mémoire : pic de `tracemalloc` d'une lecture complète, journaux synthétiques de tailles 1
et 4 (500 et 2 000 enregistrements, environ 167 et 670 Ko) : environ 24 Ko puis 11 à 14 Ko sous Python 3.10 et 3.13,
le pic ne croît pas avec la taille.

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/recalc/lecteur.py` | 142 | 14 (`tests/test_lecteur.py`, 248 lignes ; 3 de plus) |

Mutants (commande du job, runner puis `--plancher 144`, borne de 300 s, réseau isolé) : 10 tués sur 10 par leur test
visé (0 vivant, 0 FATAL), dont « fichier lu en entier » (test de mémoire). Suite : 144 tests ; plancher du job : 144,
égalité exigée (`--egal`).

## RB-1d (2026-10-05) : corrections C-2, C-3 et C-4 de la relecture G2 de la tranche 1 de P3 (lecteur, comptes)

Objet : un cas nommé par mutant vivant de la relecture (C-2), sur des journaux de l'écrivain de `collecte/journal.py`
complétés à la main : reprise à `queue` null derrière une queue en attente, et reprise déclarant une queue quand aucune
n'attend (`LECTEUR/declaration`, G-13 et G-14) ; deux queues en fin de journal, toutes deux en `queue_finale` (G-15) ;
deux queues déclarées ensemble par la reprise que l'écrivain réel écrit après deux pannes, sans rupture (G-16) ; queue
d'un octet relevée (G-19) ; reprise en tête de segment au lien faux (`LECTEUR/lien`, G-20). Docstring de `_integre`
récrite pour dire ce que le lecteur calcule (C-4 : `ws` d'un marqueur et `a` d'un trou, là où l'écrivain retient
`ws + w` et `a + w` ; valeur inchangée) ; l'état rendu pour un marqueur est fixé par `test_lignes_integres_et_etat`.
Comptes de lignes corrigés (C-3, `wc -l` sur les états de la série) : RB-0a, `tests/test_fitness.py`, 74 lignes et non
76 ; RB-1a, `tests/test_lecteur.py`, 76 et non 77 ; RB-1b, 202 et non 203.

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/recalc/lecteur.py` | 147 | — |
| `tests/test_lecteur.py` | 313 | 20 (6 de plus, un par mutant vivant de C-2) |

Mutants (commande du job, runner puis `--plancher 150`, borne de 300 s, réseau isolé) : 9 tués sur 9 par leur test
visé (0 vivant, 0 FATAL) : G-13 à G-16, G-19 et G-20 du réviseur, rejoués tels qu'écrits, et M-1d-01 à M-1d-03 (état
rendu par `_integre`). Sur l'état RB-1c, les mêmes neuf mutants : 7 vivants (les six du réviseur et M-1d-01), 2 tués.
Suite : 150 tests ; plancher du job : 150, égalité exigée (`--egal`).

## RB-1e (2026-10-05) : corrections C-1, Q-RB-4 et Q-RB-6 de la relecture G2 de la tranche 1 de P3 (paramètres)

Objet : planchers des oracles poussés hors BTC (ADR-0029 l.188) : σ au moins égal à 124 200 s pour USDC et à
129 600 s pour USDT (C-1 ; ETH : 5 400 s, égal au plancher de la classe), refus `ANALYSE/sigma` ; τ au moins égal à
0,75 % pour ETH et à 0,375 % pour les stables, refus `ANALYSE/tau-plancher` (Q-RB-4). τ de BTC sur la grille de
0,05 % (l.181), refus `ANALYSE/tau-grille` ; la grille des autres actifs relève du G0 de CALIB-ACTIFS (l.186). σ des
places et des agrégateurs d'un actif au moins égal à celui de BTC de la même classe (l.189), une classe absente de BTC
étant refusée : `ANALYSE/incoherent : sigma-btc` ; les oracles des autres actifs en sont exclus (l.189 : « planchers
seuls », aux valeurs de l.188, que le σ de BTC peut dépasser). R = 9 999 et seuil = 99 exacts au chargeur (Q-RB-6),
refus `ANALYSE/borne` ; la cohérence alpha reste en seconde garde, contrôlée sur la règle elle-même. VALIDE : σ des
places horodatées de BTC ramené à 30 s, sha256 recalculé hors du code (`sed`, `sha256sum`).

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/recalc/config_analyse.py` | 164 | 13 (`tests/test_config_analyse.py`, 201 lignes ; 5 de plus) |

Mutants (commande du job, runner puis `--plancher 155`, borne de 300 s, réseau isolé) : 17 tués sur 17 par leur test
visé (0 vivant, 0 FATAL), dont « σ des oracles comparé à celui de BTC » (l.188 contredit), « classe absente de BTC
admise » et les bornes de R et du seuil d'avant Q-RB-6. Suite : 155 tests ; plancher du job : 155, égalité exigée
(`--egal`).

## RB-1f (2026-10-05) : décision Q-RB-13 et précisions Q-RB-5, Q-RB-6, Q-RB-12 et Q-RB-14 de la tranche 1 (rotation)

Objet : noms d'unité aux seuls caractères d'un nom d'hôte, en minuscules (lettres a à z, chiffres, « - » et « . », de 1
à 253 caractères), par une seule règle `HOTE` de `rotation.py`, appliquée aux décalages (`ROTATION/unite`) et au
chargeur (`ANALYSE/unite`) : espace, tilde, majuscule et « _ » refusés (Q-RB-13). Contrat `ROTATION-S2BIS.md` : règle
des noms (§1 pt 6) ; ordre strict des points de code sur les noms d'hôte de la configuration, précision de l.200, la
première unité effective étant imprimée au rendu (§1 pt 8 ; Q-RB-5, item pour RB-15) ; R et seuil exacts au chargeur,
paramètres de `lois` (§1 pt 9 ; Q-RB-6) ; six points de cohérence avec SIM-BIS (§8 ; Q-RB-12). Mutant obligatoire
« modulo n_s au lieu de n′_s » (PROPOSITION §3.4) : dû au sous-lot RB-7, où n_s et n′_s coexistent, déclaré au §7 du
contrat et dans la docstring de `tests/test_rotation.py` (Q-RB-14).

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/recalc/rotation.py` | 111 | 8 (`tests/test_rotation.py`, 141 lignes) |
| `shogen_s2bis/recalc/config_analyse.py` | 166 | 13 (`tests/test_config_analyse.py`, 204 lignes) |

Mutants (commande du job, runner puis `--plancher 155`, borne de 300 s, réseau isolé) : 11 tués sur 11 par leur test
visé (0 vivant, 0 FATAL), dont « espace admise » (G-02 du réviseur transposé sur la règle) et « préfixe seul
contrôlé » ; M-1f-07 (nom vide admis), tué au premier passage par `test_refus_nommes` sous un test visé mal déclaré,
a été rejoué avec ce test visé. Mutant dû au sous-lot RB-7 : « modulo n_s au lieu de n′_s ». Suite : 155 tests,
tests des noms récrits ; plancher du job : 155, égalité exigée (`--egal`).

## RB-1g (2026-10-05) : décision Q-RB-1 et observation O-6 de la relecture G2 de la tranche 1 de P3 (fitness)

Objet : fonction de fitness `test_copie_de_la_lecture_json_stricte` (Q-RB-1) : le texte de la lecture JSON stricte
recopiée dans `recalc/config_analyse.py` (`_objet`, `_entier`, lecture des octets, appel de `json.loads` avec ses
crochets et son except, retour des données et du sha256) est égal à celui de `collecte/config.py` l.20-46, les deux
fichiers lus en octets sans import, aux seuls préfixes des refus (`CONFIG/`, `ANALYSE/`) et nom d'exception près ; la
copie est alignée sur l'original (docstring de `_entier`, nom `donnees`). Commentaire de la règle de `recalc` récrit
pour dire la règle codée, plus serrée que la PROPOSITION (O-6 : ni `collecte`, décodeurs compris, ni S2), avec un cas de
refus des décodeurs.

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/recalc/config_analyse.py` | 168 | — |
| `tests/test_fitness.py` | 96 | 5 (1 de plus) |

Mutants (commande du job, runner puis `--plancher 156`, borne de 300 s, réseau isolé) : 6 tués sur 6 par leur test
visé (0 vivant, 0 FATAL), dont chaque copie modifiée sans l'autre, un commentaire seul changé dans la copie, et
« décodeurs admis dans `recalc` ». Suite : 156 tests ; plancher du job : 156, égalité exigée (`--egal`).

### Mutants du réviseur G2 et du worker rejoués sur l'état final, par la commande du job (corrections de la tranche 1)

Lanceur du réviseur (`campagne_g2.py` et `job.py` : runner, puis ligne `--egal --plancher 156` de `gates.yml`, suite
entière, borne de 300 s, dépassement FATAL ; témoins verts ; copie fraîche par mutant ; réseau isolé) :

| jeu | mutants | tués par leur test visé | vivants | FATAL |
|---|---|---|---|---|
| réviseur, G-01 à G-20 sauf G-02, texte inchangé | 19 | 19 | 0 | 0 |
| G-02 transposé sur la règle `HOTE` (espace admise dans un nom d'unité) | 1 | 1 | 0 | 0 |
| G-02 tel qu'écrit, sur l'état RB-1e (son texte, `_nom` d'avant Q-RB-13, n'existe plus) | 1 | 1 | 0 | 0 |
| échantillon de 23 mutants du worker (RB-0a à RB-1c) | 23 | 23 | 0 | 0 |
| mutants neufs de RB-1d à RB-1g | 37 | 37 | 0 | 0 |

Les six vivants de C-2 (G-13 à G-16, G-19, G-20) sont tués, chacun par son cas nommé. Durée d'un passage : de 18,9 à
22,9 s.

## CB-18a (2026-10-05) : écrivain, garde d'un seul fil et refus nommés (SHOGEN-S2BIS-ECRIVAIN-USAGE-1)

Objet : le fil qui ouvre l'écrivain est le seul qui écrive (`JOURNAL/fil`) ; un écrivain s'ouvre une fois
(`JOURNAL/ouvert`) et n'écrit qu'ouvert (`JOURNAL/ferme`) ; une ouverture refusée le ferme et rend le verrou ; toute
méthode publique d'écriture porte `_terminal`, sous un contrôle mécanique. Les tests qui font tourner la boucle ouvrent
le journal dans le fil où elle tourne (`borne` : un fil par test). FORMAT §5 ; retouches du §12 et de l'en-tête
(SHOGEN-S2BIS-FORMAT-RETOUCHES-1).

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/collecte/journal.py` | 312 | — |
| `tests/test_journal.py` | 229 | 12 (3 de plus : garde d'un seul fil ; refus de l'écrivain neuf, fermé ou déjà ouvert ; garde `_terminal` sur toute méthode publique ; 1 réécrit : cycle refusé, écrivain ouvert dans le fil qui écrit) |
| `tests/test_boucle.py` | 258 | 11 (`borne` : un fil par test, journal ouvert dans ce fil) |
| `tests/test_sante.py` | 192 | 10 (journal ouvert dans le fil de la boucle) |
| `tests/test_lecture_pendue.py` | 131 | 8 (journal ouvert dans le fil de la boucle) |

Mutants (commande du job : runner, puis la ligne `verdict-suite-s2.py s2bis --aucun-saut --egal --plancher 159` de
`gates.yml`, suite entière, borne de 300 s, dépassement FATAL ; python3.12 ; réseau isolé, `lo` allumée) : 12 tués sur
12 par leur test visé (0 vivant, 0 FATAL). Suite : 159 tests ; plancher du job : 159, égalité exigée (`--egal`).

## CB-18b (2026-10-05) : attentes sur l'horloge murale, départ monotone, plan câblé, sondes à l'échéance

Objet : départ et échéance attendus sur l'horloge murale par pas d'au plus 1 s, l'horloge relue après chaque pas
(SHOGEN-S2BIS-SOMMEIL-MURAL-1 ; mesures du worker et du réviseur des corrections de la tranche B rejouées : départ en
avance de 999 850 et 1 498 115 µs avant, en retard de 198 et 173 µs après) ; départ de chaque lecture relevé aussi sur
l'horloge monotone et porté dans le suivi, d'où le client fait partir son délai (limite E-4 levée) ; nom du plan sans
lecture refusé à la construction (`BOUCLE/plan`), plus de cinq lectures par hôte refusées par un refus nommé
(`BOUCLE/hote`) (SHOGEN-S2BIS-PLAN-CABLAGE-1, volet boucle) ; règle `fin` > E appliquée aux sondes sur l'horloge
monotone de la boucle, disque et empreinte relevés après l'état des futurs (SHOGEN-S2BIS-SONDES-ECHEANCE-1). FORMAT
§10.2, §11.4, §11.8, §11.9, §13.2.

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/collecte/boucle.py` | 132 (131 auparavant : C-3 de la G2 de la tranche C, recompté au diff CB-18j) | — |
| `shogen_s2bis/collecte/sante.py` | 109 | — |
| `shogen_s2bis/collecte/http.py` | 132 | — |
| `tests/test_boucle.py` | 312 | 14 (3 de plus : sommeil malgré un recul de 1 s ou une avance de 30 s ; départ monotone dans le suivi ; plan sans lecture refusé) |
| `tests/test_sante.py` | 239 | 12 (2 de plus : sonde rendue après E et avant le relevé, null ; état des futurs relevé avant le disque) |
| `tests/test_http_reseau.py` | 272 | 14 (1 réécrit : le délai court depuis le départ monotone, jamais depuis l'horloge murale) |

Mutants (commande du job, `--plancher 164`, borne de 300 s ; python3.12 ; réseau isolé) : 13 tués sur 13 par leur test
visé au dernier passage (0 vivant, 0 FATAL). Premier passage : 12 tués, 1 vivant (M-18b-10, disque relevé avant les
futurs) : à la boucle, l'instant du relevé lu d'abord et la règle `fin` > E rendent cet ordre sans effet ; le test est
devenu un test de `joindre` sans échéance, où seul l'ordre décide, et la campagne entière a été relancée. Suite : 164
tests ; plancher du job : 164, égalité exigée (`--egal`).

## CB-18c (2026-10-05) : configurations scellées, descripteur, câblage (E-C-02, E-C-23 ; PLAN-CABLAGE-1)

Objet : `configurer` charge `formes.json`, `sante.json` et le descripteur d'observateur (sha256 des octets lus),
contrôle champs, types, bornes, puis treize règles nommées (grille, marge, budget de δ, noms uniques, méthode et
corps, espacement par hôte, témoins IPv4 canoniques, noms DNS, résolveur IPv4, empreinte, délai des sondes, commit,
cinq lectures par hôte) ; `construire` câble lectures, plan, sondes (commande, témoins, noms et délai de `sante.json`,
résolveur et sa configuration du descripteur, disque du dossier du journal) et boucle (SHOGEN-S2BIS-PLAN-CABLAGE-1,
volet sondes). FORMAT §14.

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/collecte/entree.py` | 83 | — |
| `tests/test_entree.py` | 93 | 2 (refus nommés de configuration, une règle par cas ; câblage des sondes et de la boucle) |

Mutants (commande du job, `--plancher 166`, borne de 300 s ; python3.12 ; réseau isolé) : 15 tués sur 15 par leur test
visé (0 vivant, 0 FATAL). Historique : avant sa scission en CB-18c et CB-18d (259 lignes de code, au-delà du plafond
de 200), le diff unique a connu trois passages : le premier, arrêté au FATAL de M-18c-11 (le test des refus appelait
le point d'entrée sans `--fenetres` : une configuration non refusée faisait tourner la boucle sans fin, au-delà de la
borne de 300 s ; non compté tué), puis 17 tués sur 18 (M-18c-16 vivant : `run_params` une fenêtre plus tard ; test
renforcé), puis 18 sur 18 ; les deux jeux ont été rejoués après la scission. Suite : 166 tests ; plancher du job : 166,
égalité exigée (`--egal`).

## CB-18d (2026-10-05) : point d'entrée `pool`, `run_params`, fermeture (E-C-16, E-C-23 ; ECRIVAIN-USAGE-1)

Objet : `python3 -m shogen_s2bis.collecte pool` ; refus de configuration en sortie 2, sans rien écrire ; journal ouvert
à la fenêtre courante, `run_params` (commit, sha256 des trois fichiers, contenus, version de Python) à la première
fenêtre admise ; une OSError ou un refus de l'écrivain (JOURNAL/casse compris) arrête la boucle en sortie 1, et le
journal est fermé à la sortie, quelle qu'elle soit (SHOGEN-S2BIS-ECRIVAIN-USAGE-1, volet point d'entrée). FORMAT §14.

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/collecte/entree.py` | 117 | — |
| `shogen_s2bis/collecte/__main__.py` | 7 | — |
| `tests/test_entree.py` | 171 | 4 (2 de plus : refus au point d'entrée, sortie 2, aussi par `python3 -m` ; `run_params` et fermeture sur une erreur du journal, puis reprise) |

Mutants (commande du job, `--plancher 168`, borne de 300 s ; python3.12 ; réseau isolé) : 11 tués sur 11 par leur test
visé (0 vivant, 0 FATAL), dont « `--fenetres` ignoré » (la boucle ne s'arrête pas) : le point d'entrée tourne, dans
les tests, dans le fil borné du test (10 s), et le test échoue sans pendre la suite. Dernier passage sur l'état
corrigé : les fichiers du journal y sont lus par `pathlib` (un `open` sans `with` levait un ResourceWarning sous
`-X dev`), campagne entière rejouée, même bilan. Suite : 168 tests ; plancher du job : 168, égalité exigée (`--egal`).

## CB-18e (2026-10-05) : test de bout en bout, conformité au FORMAT (E-C-24)

Objet : le collecteur entier tourne en sous-processus (garde réseau posée par `import tests`, temps réel, w = 1 s ;
sondes au délai de 0,2 s, D-3 par `/bin/echo` : sous la charge de l'hôte, une sonde D-3 `python3 -c` dépassait le
délai de 0,1 s des configurations de `test_entree`, relevé à deux états ; à 0,4 s, D-4 et D-5, sans réponse sur la
boucle locale, finissaient après l'échéance, nulles, et un mutant DNS survivait ; le test exige désormais au moins
une requête D-4 ou D-5 relevée) :
exécution A par `entree.main` sans TLS vers un serveur en clair de boucle locale (trois fenêtres : lectures `ok`,
`panne_http` 503, `panne_transport` `connexion`), puis exécution B par le point d'entrée `python3 -m
shogen_s2bis.collecte` tel quel, qui reprend le même journal (deux fenêtres, poignée TLS refusée). Le journal est
validé contre le FORMAT par `anomalies`, code de test écrit d'après le texte, sans import du collecteur : champs
exacts par type, grille, instants planifiés et échéance, phases, adresse, corps et empreinte, santé (D-2 recalculé,
sondes, disque, résolveur), `run_params`, ordre de la fenêtre, marqueurs croissants, trous, points, sommes. Aucun code
de production : le rouge se lit sur les mutants (« champ obligatoire omis », PROPOSITION §2.4).

| fichier | lignes | tests |
|---|---|---|
| `tests/test_bout_en_bout.py` | 193 | 1 (deux exécutions et une reprise, journal conforme au FORMAT) |

Mutants (commande du job, `--plancher 169`, borne de 300 s ; python3.12 ; réseau isolé) : 11 tués sur 11 par le test
de bout en bout (0 vivant, 0 FATAL), dont trois « champ obligatoire omis » (`adresse`, `horloges`, `python` de
`run_params`). Suite : 169 tests ; plancher du job : 169, égalité exigée (`--egal`).

## CB-18f (2026-10-05) : tests nommés des retouches du FORMAT (SHOGEN-S2BIS-FORMAT-RETOUCHES-1, étendu par I-2)

Objet : `tests/test_format.py` lit le FORMAT. Premier test : retouches de l'item (B.63 de l'annexe B d'ADR-0028),
valeurs prises au texte de l'item : la citation du §12 garde RFC 1035 §4.1.1-4.1.2 et ajoute §7.3 ; la phrase de la
règle de source (adresse et port interrogés) la marque « choix du lot », non règle de la RFC, et renvoie au §7.3 ; la
puce « Corrections » de l'en-tête, une seule, nomme CB-11h. Second test (I-2 de la G2 du recalcul, adjugé en extension
de l'item) : le §7.1 dit les contrôles de type de `_lire` (`suivante`, `ws`, `a`, dernière fenêtre), écrits à ce diff
d'après une sonde sur `_lire` (limites déclarées : booléen admis dans `a` et, hors première ligne, dans `seq`), et
`_lire` les fait (une valeur textuelle rend la ligne non intègre). Rouges : texte de la base 122c670 (les deux tests),
texte de CB-18e (test du §7.1). Aucun code de production.

| fichier | lignes | tests |
|---|---|---|
| `tests/test_format.py` | 74 | 2 (retouches du §12 et de l'en-tête ; contrôles de type du §7.1, dits et faits) |

Mutants (commande du job, `--plancher 171`, borne de 300 s ; python3.12 ; réseau isolé) : 20 tués sur 20 par leur test
visé (0 vivant, 0 FATAL) : onze défont une retouche du §12 ou de l'en-tête, six la phrase du §7.1, trois le contrôle
correspondant de `_lire`. Premier passage, avant l'extension I-2 : 11 tués sur 11 (`--plancher 170`). Suite : 171
tests ; plancher du job : 171, égalité exigée (`--egal`).

## SEGMENT-JOUR (2026-10-05) : jour et numéro des fichiers neufs de l'écrivain (SHOGEN-S2BIS-SEGMENT-JOUR-1)

Objet (N-1 de la G2 du recalcul, tranche 1 ; adjugé par l'orchestrateur à P1) : un segment de reprise prend le jour le
plus tardif entre celui de l'horloge et celui des fichiers présents (fichier repris compris), au numéro suivant de ce
jour ; à la bascule, le fichier du nouveau jour prend aussi le numéro suivant de son jour (`_numero`, sur la liste des
fichiers du dossier, `_fichiers`). Défaut reproduit à la main, de façon déterministe : panne juste après la bascule
(fichier du lendemain vide, ou ouverture coupée à 8 octets), horloge du redémarrage revenue à la veille ; avant, segment
`2026-10-04-1` nommé avant le fichier `2026-10-05-0` qu'il déclare, puis FileExistsError à la bascule suivante ; après,
segment `2026-10-05-1`, noms, chaîne et sommes dans le même ordre. Le test C-2 de la bascule en échec (O-3 de la G2 de
la tranche A), qui se servait d'un fichier du lendemain présent, provoque désormais l'échec par une création refusée
(ENOSPC simulé). FORMAT §6.1, §6.2, §7.2, §7.3.

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/collecte/journal.py` | 324 | — |
| `tests/test_fichiers.py` | 59 | 3 (1 de plus : bascule vers un jour déjà présent, segment suivant ; 1 réécrit : bascule en échec par création refusée) |
| `tests/test_reprise.py` | 232 | 19 (1 de plus : horloge avant le jour d'un fichier sans ligne intègre, vide ou coupé) |

Mutants (commande du job, `--plancher 173`, borne de 300 s ; python3.12 ; réseau isolé) : 11 tués sur 11 par leur test
visé (0 vivant, 0 FATAL), dont le défaut N-1 rétabli, la bascule au segment 0 et le descripteur gardé à la bascule
(C-2). Suite : 173 tests ; plancher du job : 173, égalité exigée (`--egal`).

## ENTIER-ECRIVAIN (2026-10-05) : entiers de 640 chiffres au plus (SHOGEN-S2BIS-ENTIER-ECRIVAIN-1)

Objet (I-1 de la G2 du recalcul, tranche 1 ; adjugé par l'orchestrateur à P1) : `canonique` refuse avant le
sérialiseur tout entier de plus de 640 chiffres (`JOURNAL/entier`), à toute profondeur, par un parcours qui ne voit
chaque conteneur qu'une fois (il se termine sur un cycle, que le sérialiseur refuse ensuite, C-3) ; le refus ne dépend
plus de la limite de conversion de l'interpréteur (4 300 chiffres par défaut, réglable). 640 est
`sys.int_info.str_digits_check_threshold` sous Python 3.10 à 3.13. `_lire` passant par `canonique`, une ligne qui
porte un tel entier est une queue, comme pour le lecteur du recalcul. FORMAT §1.2, §2.

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/collecte/journal.py` | 343 | — |
| `tests/test_journal.py` | 255 | 13 (1 de plus : 640 chiffres écrits et relus intègres ; 641 refusés à toute profondeur, sous tout réglage) |
| `tests/test_reprise.py` | 235 | 20 (1 de plus : queue d'une ligne chaînée qui porte un entier de 641 chiffres) |

Mutants (commande du job, `--plancher 175`, borne de 300 s ; python3.12 ; réseau isolé) : 11 tués sur 11 par leur test
visé (0 vivant, 0 FATAL), dont la borne décalée d'une unité, le parcours sans garde de cycle (fil d'essai pendu, test
du cycle en échec ; 41 s, puis 53 s au passage sur l'état final) et le sérialiseur appelé d'abord. Suite : 175 tests ;
plancher du job : 175, égalité exigée (`--egal`).

## CB-18g (2026-10-05) : tolérance de départ scellée, budget de l'ADR (C-1 de la G2 de la tranche C)

Objet : `formes.json` scelle `tolerance` (µs) : la tolérance de départ de D-2, 5 s en production (ADR-0029 l.107,
reformulée par l'ajout daté du 2026-10-04 17:03:38 UTC) ; `run_params` la porte avec le contenu de `formes.json`. La
règle `budget` devient celle de l'ADR-0029 l.233-234 : tolérance + plus grand décalage + délai + marge ≤ δ, égalité
admise. Avant, elle omettait la tolérance : la sonde du réviseur admettait des délais de 14 et 15 s (24 et 25 s au
budget de l'ADR, au-delà de 20 s). Rejouée, sa copie avec `tolerance` = 5 s admet 10 s et refuse 14, 15 et 16 s ;
la sonde telle quelle est refusée en `CONFIG/champ-absent`. FORMAT §14.1, §14.4.

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/collecte/entree.py` | 119 | — |
| `tests/test_entree.py` | 190 | 5 (1 de plus : budget de l'ADR à la borne, 5 + 4 + 10 + 1 = 20 ≤ 20 s admis, 1 µs de plus sur un terme ou de moins sur δ refusé, délai de 14 s refusé ; refus d'une tolérance nulle) |

Mutants (commande du job, `--plancher 176`, borne de 300 s ; python3.12 ; réseau isolé) : 6 tués sur 6 (0 vivant,
0 FATAL), dont la règle d'avant C-1 rétablie. MR-17 du réviseur (égalité refusée) est tué par le test à la borne,
rejoué sur l'état final. Suite : 176 tests ; plancher du job : 176, égalité exigée (`--egal`).

## CB-18h (2026-10-05) : règles de forme des configurations (SHOGEN-S2BIS-CONFIG-REGLES-1)

Objet : trois règles nommées de `formes.json` : `places-formes` (places ≥ nombre de formes : le pool est dimensionné
sur le nombre de lectures, ADR-0029 l.234), `hote-forme` (`[a-z0-9.-]{1,253}`, la règle du recalcul, Q-RB-13 de sa
tranche 1) et `chemin-forme` (« / » puis ASCII imprimable sans espace, choix du lot : la lecture refuserait tout autre
chemin à chaque fenêtre, FORMAT §10.4). Tests à la borne du délai des sondes (`delai` + `marge` = δ admis, 1 µs de
plus refusé ; tue MR-18) et du commit (majuscules refusées ; tue MR-22). FORMAT §14.1.

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/collecte/entree.py` | 125 | — |
| `tests/test_entree.py` | 218 | 6 (1 de plus : règles à la borne ; 3 refus nommés de plus au test des refus) |

Mutants (commande du job, `--plancher 177`, borne de 300 s ; python3.12 ; réseau isolé) : 10 tués sur 10 (0 vivant,
0 FATAL). MR-18 et MR-22 du réviseur sont tués, rejoués sur l'état final. Suite : 177 tests ; plancher du job : 177,
égalité exigée (`--egal`).

## CB-18i (2026-10-05) : disque injecté, onze segments d'un jour, tuple (tests seuls)

Objet : SHOGEN-S2BIS-TEST-DISQUE-INSTABLE-1 : `test_disque_et_empreinte_du_resolveur` injecte `os.statvfs` (valeurs
écrites à la main ; `f_bsize` et `f_bfree` distincts de `f_frsize` et `f_bavail`) et devient déterministe. Sous un
statvfs « mouvant », qui perd un bloc à chaque appel comme sous un écrivain concurrent, l'ancien test échoue et le
neuf passe. SHOGEN-S2BIS-SEGMENTS-10-1 : onze redémarrages d'un même jour, chacun sur une ligne coupée, donnent les
segments 1 à 11 ; chaque segment déclare la queue du précédent par numéro et se chaîne à sa `reprise`, et les sommes
suivent le même ordre (tue MR-26 et un tri des noms en texte). MR-09 : tuple admis (écrit en liste JSON) puis refusé
à 641 chiffres dans le test des 640 chiffres. Aucun code de production. FORMAT §6.1 : le numéro se compare en entier ;
au-delà de 9 segments, l'ordre de `ls` n'est plus celui de la chaîne (le nom sur trois chiffres reste un item).

| fichier | lignes | tests |
|---|---|---|
| `tests/test_sante.py` | 248 | 12 (1 réécrit : statvfs injecté) |
| `tests/test_reprise.py` | 257 | 21 (1 de plus : onze redémarrages d'un même jour) |
| `tests/test_journal.py` | 256 | 13 (1 complété : tuples) |

Mutants (commande du job, `--plancher 178`, borne de 300 s ; python3.12 ; réseau isolé) : 4 tués sur 4 (0 vivant,
0 FATAL). MR-09 et MR-26 du réviseur sont tués, rejoués sur l'état final. Suite : 178 tests ; plancher du job : 178,
égalité exigée (`--egal`).

## CB-18j (2026-10-05) : convention des citations, `run_params` dans l'ordre de la fenêtre, recompte

Objet (G2 de la tranche C de P1) : l'en-tête du FORMAT écrit que « ADR-0029 l.N » renvoie à l'ADR-0029 au commit
`e16956b`, convention du G0 (SHOGEN-S2BIS-CITATIONS-ADR-DECALEES-1). Relevé : toutes les citations de l'ADR-0029 du
FORMAT (l.83, 107, 108, 109, 233, 234, 238-240), du code et des tests du collecteur (l.109-110, 217, 233, 234, 236,
237, 238, 239) suivent cette convention ; aucune n'est à corriger. §11.5 : `run_params` ouvre la première fenêtre
admise d'une exécution (observation de la G2) ; le test de bout en bout le contrôle (`run_params` suit l'`ouverture`
ou la `reprise`). C-3 : `boucle.py` recompté à 132 lignes à l'état CB-18b (8 873 octets, 132 sauts de ligne, égal à
l'état final) ; les autres comptes des sections CB-18 sont recomptés égaux.

| fichier | lignes | tests |
|---|---|---|
| `tests/test_format.py` | 88 | 3 (1 de plus : convention des citations, `run_params` au §11.5) |
| `tests/test_bout_en_bout.py` | 194 | 1 (`run_params` en tête de sa fenêtre, contrôlé) |

Mutants (commande du job, `--plancher 179`, borne de 300 s ; python3.12 ; réseau isolé) : 4 tués sur 4 (0 vivant,
0 FATAL), dont `run_params` écrit après la boucle. Suite : 179 tests ; plancher du job : 179, égalité exigée
(`--egal`).

## CB-18k (2026-10-05) : enregistreur de rôle, ligne du seul job suivant (C-2 de la G2 de la tranche C)

Objet : `test_suites_s2bis_et_sim_bis_par_la_ligne_du_job` ajoute un commit où la ligne du vérificateur de s2bis ne
figure que dans le job suivant (`sim-bis-unittest`) : refus avant toute écriture. Rouge montré avec MR-24 du
réviseur (ligne cherchée jusqu'à la fin du fichier), qui survivait. Le dépôt jetable du test porte aussi
`s2-harness/tests`, pour que ce rouge soit d'assertion. Aucun code de production.

| fichier | lignes | tests |
|---|---|---|
| `s2-harness/tests/test_oracle_record.py` | 423 | 12 (1 complété : ligne du seul job suivant) |

Mutants (commande du job s2-harness-unittest, borne de 300 s ; python3.12 ; réseau isolé ; état CB-18k) : MR-24 et
une fin de job manquée sur un nom à tiret, 2 tués sur 2 (0 vivant, 0 FATAL). Suite S2 : 406 tests, inchangée.

## CB-18l (2026-10-05) : analyseur unique de la ligne d'un job (SHOGEN-S2BIS-LIGNE-JOB-LEURRE-1)

Objet : `enforcement/verdict-suite-s2.py` porte `etapes` et `lignes_du_job`, seul analyseur de la ligne d'un job de
gates.yml. Il sert aux cas K-01 à K-03 du runner et à `ligne_du_job` de l'enregistreur de rôle, qui le charge depuis
l'arbre de l'outil, jamais depuis le commit extrait. Il ne lit que les blocs `run:` des étapes admises : clés `name`,
`shell: bash` et `run` seules, `run` en ligne ou en bloc littéral `|` ; les étapes `if:`, `continue-on-error`, `env:`
et `working-directory` sont exclues. La ligne compte si son bloc ne porte, en dehors d'elle, que `python3 --version`
ou `unset SHOGEN_S2_CAMPAGNE_CONTROL`. Un job aux clés hors de `name`, `runs-on`, `timeout-minutes` et `steps`, ou de
forme illisible, n'a aucune étape admise. Un job absent ou répété, une ligne de premier niveau hors de `name`, `on`,
`permissions` et `jobs` (un `defaults` ou un `env`, même écrit `env :` ou entre guillemets) ou répétée, une fin de
ligne autre que LF donnent un refus. Les cas K gardent leurs contrôles d'avant et y ajoutent ceux de l'analyseur
(trois étapes : checkout, runner, bloc du vérificateur) : aucun cas n'est affaibli, et le runner passe de 33 à 57
cas. Les leurres C1 (`name: >`) et C4 (`if: false`) du réviseur sont refusés par les deux. Au runner : L-01 à L-21,
A-01 et A-02 ; sous un squelette qui lit les lignes brutes comme K-02 d'avant, 19 de ces cas échouent. Au test de
l'enregistreur : C1, C4 et un analyseur complaisant porté par le commit.

| fichier | lignes | tests |
|---|---|---|
| `enforcement/verdict-suite-s2.py` | 148 | — |
| `enforcement/tests/run-fixtures-verdict-suite-s2.py` | 209 | 57 cas (24 de plus : L-00 à L-21, A-01, A-02) |
| `s2-harness/tools/oracle_record.py` | 309 | — |
| `s2-harness/tests/test_oracle_record.py` | 434 | 12 (1 complété : leurres C1 et C4, analyseur complaisant du commit) |

Mutants (commande du job s2-harness-unittest, borne de 300 s ; python3.12 ; réseau isolé) : 25 tués sur 25 au
dernier passage (0 vivant, 0 FATAL). Ce sont treize mutants de l'analyseur, un de l'enregistreur, deux des cas K,
quatre mutants M-R du worker de CB-18 portés sur le code réécrit, et cinq leurres neufs portés sur le gates.yml réel
(`name: >`, `set +e` et `exit 0`, `working-directory`, `defaults`, `env` du job). MR-24 y est porté en « fin du job
ignorée ». Passages précédents, non comptés : le premier donnait 18 tués et 2 vivants (clés du job non contrôlées, clé
`run` répétée), que L-12 et L-14 ne séparaient pas ; ces deux cas ont été réécrits (`env` du job en flux, première
clé `run` en ligne avant le bloc), et la campagne a été relancée en entier (24 sur 24). Ensuite, une clé de premier
niveau écrite `env :` ou entre guillemets échappait au contrôle de `defaults` et d'`env` (L-19 et L-20 rouges, comme
L-21, clé `jobs` répétée) : les clés de premier niveau sont désormais fermées, et toute la campagne a été rejouée.
Suite S2 : 406 tests, inchangée.

## CB-18m (2026-10-05) : `--egal` au job s2-harness-unittest (décision de l'orchestrateur, G2 de la tranche C)

Objet : la ligne du job S2 devient `python3 -B enforcement/verdict-suite-s2.py --egal` : Ran = PLANCHER du
vérificateur, 406. K-01 l'exige, et L-22 refuse la même ligne sans `--egal`. Le couplage avec le test de comptes de
B-SEG-1 (motif de l'inégalité au G0 de D8a-3, rappelé par Q-2 de la G2 de P1-A) a été vérifié. Les deux tests nommés
de `test_exclusion` lèvent SkipTest dans leur corps, et un test sauté compte dans Ran, variable posée ou non ; le
vérificateur retire la variable de l'environnement de la suite. Ran ne dépend donc pas d'elle, et `--egal` est tenable.
MR-25 du réviseur (PLANCHER rendu à 405) est tué.

| fichier | lignes | tests |
|---|---|---|
| `enforcement/verdict-suite-s2.py` | 152 | — |
| `enforcement/tests/run-fixtures-verdict-suite-s2.py` | 214 | 58 cas (1 de plus : L-22 ; K-01 exige `--egal`) |

Mutants (commande du job s2-harness-unittest, borne de 300 s ; python3.12 ; réseau isolé) : 4 tués sur 4 (0 vivant,
0 FATAL), dont `--egal` retiré de la ligne du job et K-01 desserré (tué par L-22). MR-25 du réviseur est tué, rejoué
sur l'état final. Suite S2 : 406 tests ; PLANCHER : 406, égalité exigée (`--egal`).

## CB-18n (2026-10-05) : 64 niveaux d'imbrication au plus (lettre C-4 du FORMAT)

Objet (avis de l'advisor sur le banc de concordance des lecteurs du recalcul, adjugé par l'orchestrateur le
2026-10-05) : le niveau d'une valeur est 1 pour l'objet de la ligne, n + 1 dans un conteneur de niveau n.
`canonique` refuse avant le sérialiseur un enregistrement dont un conteneur dépasse le niveau 64
(`JOURNAL/imbrication`), dans le parcours des entiers d'I-1, devenu postfixe : chaque conteneur est développé une fois
et sa hauteur retenue, si bien qu'un conteneur partagé compte à sa plus grande profondeur, sans parcours exponentiel ;
un cycle reste refusé en `JOURNAL/type` par le sérialiseur. `_lire` passant par `canonique`, une ligne de 65 niveaux
est une queue quel que soit l'interpréteur ; avant, le refus venait de RecursionError (de 988 à 9 996 niveaux selon la
version et l'appelant). Profondeur réelle mesurée au test de bout en bout : M = 4 (`run_params`, `formes.formes[i]`),
écrite au FORMAT et fixée par ce test. FORMAT §2, §8.3.

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/collecte/journal.py` | 359 | — |
| `tests/test_journal.py` | 285 | 14 (1 de plus : conteneurs au niveau 64 écrits puis relus intègres, au niveau 65 refusés, liste partagée vue par les deux chemins ; 1 complété : cycle profond refusé en `JOURNAL/type`) |
| `tests/test_reprise.py` | 260 | 22 (1 de plus : queue d'une ligne chaînée de 65 niveaux ; 1 complété : refus `JOURNAL/imbrication` à l'écriture) |
| `tests/test_bout_en_bout.py` | 202 | 1 (complété : niveau ≤ 64 de tout enregistrement, M = 4) |

Mutants (commande du job, `--plancher 181`, borne de 300 s ; python3.12 ; réseau isolé) : 7 tués sur 7 (0 vivant,
0 FATAL), dont N décalé d'une unité dans les deux sens, la hauteur prise au premier enfant et le cycle non relevé.
MR-08 et MR-09 du réviseur, dont les lignes visées ont changé, y sont portés et tués. Suite : 181 tests ; plancher du
job : 181, égalité exigée (`--egal`).

## CB-18o (2026-10-05) : définition unique d'« intègre » (lettres C-1 et C-2 du FORMAT)

Objet : le §7.1 porte une seule définition d'« intègre », points (a) à (e) de la lettre adjugée : ligne close par
0x0A d'au plus LIMITE octets ; objet JSON canonique aux entiers de 640 chiffres au plus (C-1 : une telle ligne est une
queue ; le refus de l'écrivain reste `JOURNAL/entier`) et aux conteneurs au niveau 64 au plus ; `type` chaîne, `seq`
entier, `prec` de 64 chiffres hexadécimaux minuscules ; champs propres des types réservés présents et typés ; chaîne.
Un booléen n'est jamais un entier : `_types` compare `type(v)`, jamais `isinstance`. Les limites déclarées de CB-18f
sont retirées (l'item proposé SHOGEN-S2BIS-LIRE-BOOLEENS-1 n'a plus d'objet). Risque R-2, vérifié type par type :
aucun type n'écrit `ws` null (`ouvrir`, `ecrire` et `marqueur` refusent tout `ws` qui n'est pas un entier) ; le `ws`
d'un type non réservé est typé et requis de même, et la reprise du second démarrage du test de bout en bout ne déclare
aucune queue. `RESERVES` est tiré de la table des champs propres. Rouge : sur le code d'avant, dix sous-tests en échec
(champs propres non typés ou absents, booléen pour `seq`), `type` non chaîne et `prec` mal formé admis. FORMAT §7.1.

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/collecte/journal.py` | 373 | — |
| `tests/test_format.py` | 104 | 3 (1 réécrit : définition unique au §7.1, sans limite déclarée ; `_lire` la fait, champ par champ et type par type, booléen, absence, ligne JSON qui n'est pas un objet et `prec` en tête compris) |
| `tests/test_journal.py` | 286 | 14 (1 complété : les six types réservés refusés à `ecrire`) |
| `tests/test_bout_en_bout.py` | 203 | 1 (complété : aucune queue déclarée au second démarrage, R-2) |

Mutants (commande du job, `--plancher 181`, borne de 300 s ; python3.12 ; réseau isolé) : 20 tués sur 20 au dernier
passage (0 vivant, 0 FATAL) : objet exigé ; `type` ; `seq` booléen ; forme et casse de `prec` ; `queue`, `cause`,
`de`, `ws` d'un `point`, `jour` d'une `cloture` et d'une `ouverture` ; `ws` d'un type non réservé ; booléen admis
partout, ou par `isinstance` ; champ manquant pris pour null ; première ligne ; canonicité ; RecursionError du
décodeur ; `point` retiré des types réservés ; sonde R-2 (`ws` de `run_params` exigé null : le test de bout en bout
échoue). Passage précédent, non compté : 19 tués et 1 vivant (`point` retiré des types réservés, le test des
refus ne couvrant que `marqueur`) ; le test a été complété. Suite : 181 tests ; plancher du job : 181, égalité exigée
(`--egal`).

## CB-18p (2026-10-05) : ordre de la liste `queue` (lettre C-3 du FORMAT)

Objet : le §7.4 porte la lettre C-3 : `queue` est une liste non vide dans l'ordre croissant (jour, k) des fichiers, ou
null sans queue ; une liste vide, un objet nu, un autre ordre ou un booléen pour un entier font une déclaration
fausse ; à toute rupture, toutes les queues en attente sont rendues avec elle ; seules comptent comme déclarées les
`reprise` intègres, au lien juste, à déclaration exacte. Le §7.4 dit que l'écrivain écrit la liste dans cet ordre :
il relit du plus récent au plus ancien et range chaque queue devant les précédentes ; aucun code ne change. Risque
R-1 : un test de deux pannes réelles (disque plein sur une `lecture` du 4, puis sur la `reprise` du segment neuf du 5)
fixe l'ordre ; il échoue sous le mutant qui ajoute en fin de liste. FORMAT §7.4.

| fichier | lignes | tests |
|---|---|---|
| `tests/test_reprise.py` | 286 | 23 (1 de plus : deux pannes réelles, deux queues dans l'ordre (jour, k)) |

Mutants (commande du job, `--plancher 182`, borne de 300 s ; python3.12 ; réseau isolé) : 2 tués sur 2 (0 vivant,
0 FATAL) : queues rangées dans l'ordre de relecture, plancher non relevé. Suite : 182 tests ; plancher du job : 182,
égalité exigée (`--egal`).

## CB-18q (2026-10-05) : grammaire des noms de fichiers (lettre C-5 du FORMAT)

Objet : dans `_fichiers`, k suit `0|[1-9][0-9]*`, et l'ordre est (jour, k entier). À l'ouverture, un nom qui commence
par `<préfixe>-` et finit par `.jsonl` hors de cette grammaire est refusé (`JOURNAL/nom`) : rien n'est écrit,
l'écrivain est fermé et le verrou rendu. À la bascule, un tel nom est ignoré, parce que le refuser là écrirait la
`cloture` avant le refus ; le redémarrage suivant le refuse. Il n'y a pas de numéro sur trois chiffres : la lettre
écarte le nom sur trois chiffres que le diff CB-18i laissait en item. Le test des onze segments d'un jour (CB-18i)
tient lieu du test à dix segments ou plus (MR-26, porté). Rouge : sur le code d'avant, un nom à zéro de tête était lu
comme segment (`JOURNAL/illisible` sur un fichier vide) et les autres noms non conformes étaient ignorés. FORMAT §5,
§6.1, §7.7 (lettre des lecteurs : grammaire, refus nommé d'un nom non conforme et d'un dossier sans fichier du
journal).

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/collecte/journal.py` | 381 | — |
| `tests/test_fichiers.py` | 83 | 4 (1 de plus : sept noms non conformes refusés à l'ouverture sans rien écrire, verrou rendu ; quatre noms voisins ignorés (autre préfixe, préfixe sans tiret, autre fin, fin en majuscules) ; nom non conforme ignoré à la bascule, refusé au redémarrage) |

Mutants (commande du job, `--plancher 183`, borne de 300 s ; python3.12 ; réseau isolé) : 9 tués sur 9 (0 vivant,
0 FATAL) : zéro de tête admis, segments à deux chiffres hors grammaire (MR-26 porté), refus jamais levé, ouverture
sans refus, refus aussi à la bascule, préfixe sans tiret ou autre fin refusés, k comparé en texte, plancher non
relevé. Suite : 183 tests ; plancher du job : 183, égalité exigée (`--egal`).

## CB-18r (2026-10-05) : gabarit des lignes brutes des jobs unittest (CC-1 du contre-contrôle de CB-18, remède (a))

Objet : `cable()`, qui juge les cas K-01 à K-03 du runner, contrôlait `runs-on`, le checkout épinglé et le runner par
la présence de lignes dépouillées de leur indentation : une ligne cachée dans un nom plié (`name: >`) ou dans le
`with:` du checkout suffisait (leurres N-01 à N-04 et N-17 à N-20 du contre-contrôle). `cable()` exige désormais
`gabarit` et `analyseur`. `gabarit` lit les lignes brutes du job, à indentation exacte, contre un gabarit fixe :
`name`, `runs-on: ubuntu-24.04`, `timeout-minutes`, `steps` ; le checkout épinglé, dont le `with:` se réduit à
`persist-credentials: false` ; le runner ; une étape `run: |` ; puis seulement des lignes d'indentation 10.
`analyseur` est la lecture de l'enregistreur de rôle, inchangée. `job()` rend les lignes brutes, sans les lignes vides
ni les commentaires d'indentation 8 au plus. Le docstring de `cable()` dit exactement ces contrôles.

Cas du runner :
- L-01 à L-21 sont désormais jugés par l'analyseur seul ; jugés par `cable`, le gabarit masquerait ses mutants (sonde :
  CA-03 survit alors).
- L-23 à L-29 sont refusés par le gabarit : classes N-01, N-02, N-03, N-04, N-17, N-18, et un `with:` vers un dépôt
  tiers.
- L-30 (`if:` sur le checkout), L-31 (`runs-on: ubuntu-24.04-arm`) et L-32 (checkout épinglé à un autre commit)
  gardent les refus d'avant.
- G-01 fige l'indentation exacte du bloc.

Rouge : sous le `cable` d'avant, L-23 à L-29 et G-01 sont admis. Les 20 leurres du réviseur, rejoués par son outil : les
8 failles sont refusées, les 10 refus sont gardés, N-12 et N-14 restent admis (résidu SHOGEN-S2BIS-ANALYSEUR-RESIDUS-1,
sans code).

| fichier | lignes | tests |
|---|---|---|
| `enforcement/tests/run-fixtures-verdict-suite-s2.py` | 265 | 69 cas (11 de plus : L-23 à L-32, G-01 ; L-01 à L-21 jugés par l'analyseur seul) |

Mutants (commande du job s2bis-unittest, dont le runner est la première étape, borne de 300 s ; python3.12 ; réseau
isolé) : 8 tués sur 8 (0 vivant, 0 FATAL) :
- gabarit non appelé ;
- `runs-on`, checkout et `with:` quelconques ;
- lignes après le gabarit non contrôlées ;
- fin du job non vue ;
- commentaires gardés ;
- préfixe seul (`re.match`).

Passage précédent, non compté : le checkout quelconque survivait, parce que les leurres cachaient une ligne dans un nom
plié, ce qui rompait déjà la suite. L-32 a été ajouté. Les CA-01 à CA-12 du réviseur et les leurres sont comptés à
CB-18s. Suite : 183 tests ; plancher du job : 183.

## CB-18s (2026-10-05) : trois refus de l'analyseur figés (CC-2 du contre-contrôle de CB-18)

Objet : trois mutants de l'analyseur survivaient à la commande du job : CA-01 (`env` admis au premier niveau), CA-07
(clé de job répétée admise) et CA-12 (étapes lues hors de `steps`). Trois cas les figent :
- L-33 : `env:` de premier niveau, forme simple ;
- L-34 : `runs-on` répété ;
- A-03 : étapes imitées dans le nom plié du job, où `etapes` doit rendre `[]`.

Rouge : à l'état r, les trois mutants survivent (69 cas, 0 échec) ; à l'état s, chacun fait échouer son cas, et lui
seul.

| fichier | lignes | tests |
|---|---|---|
| `enforcement/tests/run-fixtures-verdict-suite-s2.py` | 271 | 72 cas (3 de plus : L-33, L-34, A-03) |

Mutants (commande du job s2bis-unittest, borne de 300 s ; python3.12 ; réseau isolé) : CA-01, CA-07 et CA-12 du
réviseur sont tués sur l'état s (3 sur 3).

Sur l'état final (CB-18t) :
- CA-01 à CA-12 du réviseur : 12 tués sur 12.
- Les 20 leurres du réviseur, régénérés par son outil sur le gates.yml final, et 11 leurres neufs :
  - à LN-01 à LN-04 : `with:` complété d'un `ref:` ou d'un `repository:`, `runs-on` répété, `if:` du job ;
  - à LN-05 à LN-08 : `container:`, `continue-on-error` du job, runner caché dans un nom plié, checkout dans le nom plié
    du job ;
  - à LN-09 à LN-11 : quatrième étape, `env:` du job en bloc, `runs-on: ubuntu-24.04-arm`.
- Leurres classés par l'étape du runner, commune aux trois jobs : 29 tués, 2 vivants (N-12 et N-14, résidu
  ANALYSEUR-RESIDUS-1, sans code). La commande du job exécuterait les étapes du leurre lui-même.

Suite : 183 tests ; plancher du job : 183.

## CB-18t (2026-10-05) : incise O-1 au §7.4 et limite O-2 au §5 du FORMAT

Objet (adjudication de l'orchestrateur sur les observations O-1 et O-2) :
- au §7.4, l'incise « (un objet nu rend déjà la ligne non intègre, §7.1 d) » ;
- la phrase de l'avis l.78, mot pour mot, qui remplace sa paraphrase de CB-18p ;
- « Les lecteurs appliquent le §7.1 avant le §7.4. » ;
- au §5, une ligne de limite : un dossier par journal ; un préfixe qui en prolonge un autre dans le même dossier fait
  refuser le plus court (`JOURNAL/nom`). L'item SHOGEN-S2BIS-PREFIXE-NOM-1 est formé par l'orchestrateur.

Aucune autre lettre ne change : la comparaison mot à mot ne donne que ces ajouts. Rouge : sur le FORMAT d'avant, les
trois textes attendus manquent.

| fichier | lignes | tests |
|---|---|---|
| `tests/test_format.py` | 116 | 4 (1 de plus : §7.4, incise, phrase de l'avis l.78 et ordre de lecture) |

Mutants (commande du job s2bis-unittest, borne de 300 s ; python3.12 ; réseau isolé) : 4 tués sur 4 (incise retirée,
phrase de l'avis non mot pour mot, ordre de lecture retiré, plancher non relevé). Suite : 184 tests ; plancher du job :
184, égalité exigée (`--egal`).

## CB-18u (2026-10-05) : valeurs libres du gabarit en scalaire simple (CC2-1 du contre-contrôle bref de CB-18r à t)

Objet : une chaîne entre guillemets écrite sur plusieurs lignes, dans une valeur libre du gabarit (`name` du job ou
d'une étape), avalait des lignes du gabarit que celui-ci lisait une à une :
- LC-03 : le nom de l'étape du runner, ouvert par un guillemet et fermé au nom de l'étape suivante ; le runner ne
  s'exécute plus ;
- LC-01 : le nom du job avale `runs-on`.

Remède du réviseur, adjugé par l'orchestrateur : les trois `name` suivent `[0-9A-Za-z].*` (scalaire simple : ni
guillemet, ni bloc, ni ancre, ni flux) et `timeout-minutes` suit `[1-9][0-9]*`. Cas : L-35 (LC-03), L-36 (LC-01) ;
pour le gabarit seul, G-02 (`timeout-minutes` entre guillemets), G-03 et G-04 (le nom du job, le nom de l'étape 3,
ouverts par un guillemet fermé à la dernière ligne du bloc). Rouge : sous le gabarit de CB-18t, les cinq sont admis.

Leurres rejoués avec les outils du réviseur. Seuls passent :
- N-12 et N-14 (résidu) ;
- LC-02 (YAML invalide) ;
- LC-09 et LC-10 (échec à l'exécution) ;
- LC-08 (`timeout-minutes: 600`, sans effet), que `[1-9][0-9]*` admet.

LC-13 (ancre et alias) est refusé.

| fichier | lignes | tests |
|---|---|---|
| `enforcement/tests/run-fixtures-verdict-suite-s2.py` | 289 | 77 cas (5 de plus : L-35, L-36, G-02 à G-04) |

Mutants (commande du job s2bis-unittest, borne de 300 s ; python3.12 ; réseau isolé) : 6 mutants, 6 tués. Ils
rendent quelconques les valeurs libres, l'entier de `timeout-minutes`, le nom du job, le nom de l'étape du runner ou
celui de l'étape 3, ou admettent un guillemet en tête d'une valeur libre.

Rejoués sur la base recalée :
- les mutants de CB-18r (8), de CB-18s (3) et de CB-18t (4) : tous tués ;
- CA-01 à CA-12 du réviseur : 12 tués sur 12 ;
- les leurres N-01 à N-20, LN-01 à LN-11 et LC-01 à LC-13, classés par l'étape du runner : 38 tués, 6 vivants (ceux
  listés plus haut).

Suite : 184 tests ; plancher du job : 184, égalité exigée (`--egal`).

## CB-18v (2026-10-05) : `fetch-depth: 0` admis dans le seul job sim-bis (Q-T4-11, tranche 4 de SIM-BIS)

Objet : l'adaptateur oracle_r1 de la tranche 4 de SIM-BIS (SB-14A) lit le harnais de f35a70c par `git archive`. Le
job sim-bis-unittest demande donc l'historique complet, `fetch-depth: 0` sous le `with:` du checkout (Q-T4-11,
adjugée). Le gabarit de K-03 réduisait ce `with:` à `persist-credentials: false` : sur la tête 98c8537, la série
SIM-T4 (SB-9A à SB-14H) donnait 76 ok et 1 échec (K-03).

Adjudication de l'orchestrateur : pour le seul job sim-bis-unittest, la ligne `fetch-depth: 0` (valeur exacte) peut
suivre `persist-credentials: false` ; les jobs s2bis et S2 restent tels quels. Cas :
- L-37 : la ligne, admise ;
- L-38 : `fetch-depth: 1`, refusé ;
- L-39 : la ligne dans le job s2bis, refusée ;
- L-40 : une autre clé du `with:` après la ligne (`ref: main`), refusée ;
- L-41 : la ligne avant `persist-credentials: false`, refusée (ordre du gabarit).

Rouge : sous le gabarit de la tête, L-37 échoue ; avec la série SIM-T4, K-03 aussi.

| fichier | lignes | tests |
|---|---|---|
| `enforcement/tests/run-fixtures-verdict-suite-s2.py` | 312 | 82 cas (5 de plus : L-37 à L-41) |

Mutants (commande du job s2bis-unittest, borne de 300 s ; python3.12 ; réseau isolé) : 5 mutants, 5 tués, chacun
par un seul cas :
- ligne admise dans tous les jobs : L-39 ;
- valeur quelconque : L-38 ;
- ligne jamais admise : L-37 ;
- lignes suivantes du `with:` admises : L-40 ;
- ligne admise à toute place du job : L-41.

Runner : 82 ok sur la tête, comme sur la tête suivie de la série SIM-T4. Suite s2bis : 184 tests, plancher 184
inchangé.

## CB-18w (2026-10-05) : `fetch-depth: 0` exigé dans le job sim-bis (O-2 de la relecture de SIM-T4)

Objet : la relecture de la tranche 4 de SIM-BIS demande (O-2) que K-03 exige la ligne `fetch-depth: 0` dans le job
sim-bis-unittest ; sans elle, l'adaptateur oracle_r1 échoue fermé (ORACLE/extraction). CB-18w suit la série SIM-T4,
qui pose la ligne (SB-14A) ; avant elle, K-03 échouerait sur la tête.

Le gabarit du job sim-bis exige désormais la ligne, à sa place (après `persist-credentials: false`), valeur exacte.
Les jobs s2bis et S2 restent tels quels. Cas : L-42, le job sim-bis sans la ligne, refusé. Rouge : sous le gabarit
de CB-18v, sur la tête suivie de CB-18v et de la série SIM-T4, L-42 échoue.

| fichier | lignes | tests |
|---|---|---|
| `enforcement/tests/run-fixtures-verdict-suite-s2.py` | 316 | 83 cas (1 de plus : L-42) |

Mutants (commande du job s2bis-unittest, borne de 300 s ; python3.12 ; réseau isolé) : 6 mutants, 6 tués :
- ligne seulement admise : L-42 ;
- ligne exigée dans tous les jobs : K-01, K-02, L-00 et L-39 ;
- ligne quelconque à sa place : L-38 ;
- valeur quelconque : L-38 ;
- lignes suivantes du `with:` admises : L-40 ;
- ligne exigée à toute place du job : L-41.

Runner : 83 ok sur la tête suivie de CB-18v, de la série SIM-T4 et de CB-18w. Suite s2bis : 184 tests, plancher 184
inchangé.
