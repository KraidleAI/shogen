# Métriques du paquet `s2bis/` : baseline G4 et fonctions de fitness

- **Rattachement** : PROPOSITION du G0 des lots COLLECTE-BIS, RECALC-BIS et DEPLOI-BIS (`docs/adr-0029/g0-collecte/`),
  exigence E-C-41 : fonctions de fitness dès CB-0, baseline versée (lignes et tests par module, score de mutation par
  sous-lot) ; leçon de SHOGEN-G4-RECALCUL-METRIQUES-1 (annexe B d'ADR-0028, l.892).
- **Mesures** : lignes physiques par `wc -l` ; tests par `unittest` (compte de la découverte, sans sous-tests) ;
  campagnes de mutants classées par la sortie du lanceur (SHOGEN-MUT-FATAL-1 : 1 tué par le test nommé, 0 vivant, toute
  autre sortie FATAL), témoin vert avant chaque campagne. Chaque sous-lot ajoute sa section à la fin de ce fichier.
- **Compte de R-25** (SHOGEN-S2BIS-R25-COMPTE-1, O-7 de la G2 de P2A ; lot DETTES-T6, diff DT6-a) : la borne de
  200 lignes par sous-lot porte sur les lignes ajoutées des fichiers de code, `.py` et `.yml` (colonne des ajouts de
  `git diff --numstat`) ; données (`.json`, `.bin`), fixtures et documents (`.md`) sont hors compte et déclarés dans
  la section du sous-lot.

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

## CB-18x (2026-10-05) : égalité exacte et place de la ligne `fetch-depth: 0` (CC4-1 du contre-contrôle cc4)

Objet : deux mutants du réviseur survivaient à CB-18w, faute de cas :
- MV-01 admet aussi la ligne après le nom de l'étape du runner ;
- MV-02 compare la ligne après `strip()`, ce qui rend l'indentation libre.

Le gabarit exige la ligne à la lettre et à sa place, mais aucun cas ne le fixait. Adjudication de l'orchestrateur :
ajouter les cas. Cas : L-43 (la ligne à l'indentation 8, refusée) et L-44 (la ligne après le nom de l'étape du runner,
refusée). Le code du gabarit ne change pas.

Rouge : sans ces cas, le runner de CB-18w sous MV-01 ou sous MV-02 donne 83 ok. Avec eux : 85 ok ; sous MV-02, seul
L-43 échoue ; sous MV-01, seul L-44.

| fichier | lignes | tests |
|---|---|---|
| `enforcement/tests/run-fixtures-verdict-suite-s2.py` | 321 | 85 cas (2 de plus : L-43, L-44) |

Mutants (commande du job s2bis-unittest, borne de 300 s ; python3.12 ; réseau isolé) :
- 2 mutants neufs, 2 tués : ligne cherchée de b[7] à b[9] (L-44) ; indentation quelconque (L-43) ;
- MV-01 et MV-02 : tués ;
- les 6 mutants de CB-18w, rejoués : tués.

Runner : 85 ok sur la tête suivie de CB-18v, de la série SIM-T4, de CB-18w et de CB-18x. Suite s2bis : 184 tests,
plancher 184 inchangé.

## CB-19a (2026-10-05) : réponse DNS appariée de plus de 512 octets en `forme` (C-1 (a) de la relecture d'intégration)

Objet : la relecture G2 d'intégration de P1 (C-1) mesure qu'une seule réponse DNS appariée de 65 502 octets (un nom
de 255 octets de caractères de contrôle, puis 4 076 pointeurs vers lui) porte la `sante` à 6 209 510 octets, au-delà
de LIMITE : refus `JOURNAL/taille` et arrêt du collecteur à chaque fenêtre. Correction (a), adjugée telle qu'écrite :
une réponse appariée de plus de 512 octets est `forme` (RFC 1035 §2.3.4 et §4.2.1, citées mot pour mot au FORMAT §12,
fichier du registre lu, sha256 `d14ae809…`). Le contrôle suit l'appariement, dans `interroger` : un datagramme non
apparié reste ignoré quelle que soit sa taille ; `analyser` ne porte pas la borne de l'UDP.

Rouge : les tests neufs sur le code et le FORMAT de la base 47b2177 échouent par assertion (513 octets et réponse
hostile retenus en `reponse` ; trois textes du §12 absents).

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/collecte/dns.py` | 123 | — |
| `tests/test_dns.py` | 224 | 15 (2 de plus : 512 octets retenue, 513 en `forme`, non apparié de 600 octets ignoré, `analyser` sans la borne ; réponse hostile du réviseur en `forme`) |
| `tests/test_format.py` | 129 | 5 (1 de plus : §12, statut, deux citations de la RFC 1035, puce « Corrections ») |

Mutants (commande du job s2bis-unittest : runner, puis ligne de `gates.yml` ; borne de 300 s ; python3.12, `-X dev
-W error` ; réseau isolé ; témoin VIVANT) : 13 mutants neufs, 13 tués par leur test visé (0 vivant, 0 FATAL) : borne
retirée, à 512 octets compris, à 513, à 65 507 (ces deux réécrits sur une ancre unique, la première écriture étant
inapplicable : texte présent aussi dans la docstring), avant l'appariement, réponse ignorée au lieu de `forme`, borne
après la mise à jour du résultat, borne portée par `analyser`, quatre retouches du §12 défaites, plancher non relevé.
Suite : 187 tests ; plancher du job : 187, égalité exigée (`--egal`).

## CB-19b (2026-10-05) : sept témoins et sept noms au plus, plus grande `sante` sous LIMITE (C-1 (b) de la relecture)

Objet : C-1 (b), adjugée telle qu'écrite : borner au schéma de `sante.json` le nombre de témoins et de noms, calculé
pour que la plus grande `sante` possible reste sous LIMITE (4 194 304 octets), calcul écrit au FORMAT (§13.6) et ici.
Le schéma admet désormais `[s, n]` (n éléments au plus, refus `CONFIG/borne`) ; `temoins` et `noms` : sept au plus
(production : trois témoins, deux noms, ADR-0029 l.109-110).

Calcul. Borne de `reponses` d'une sonde, réponse retenue de U = 512 octets au plus (CB-19a), question de 17 octets au
moins (« . » : en-tête de 12, nom de 1, type et classe de 4) :
- un nom décodé a au plus 2U = 1 024 caractères. Lemme : `_nom` lit des segments ; chacun couvre, depuis son début, des
  octets d'étiquette (longueur < 0x40, contenu ASCII, < 0x80) jusqu'à un pointeur (premier octet ≥ 0xC0) ou à un
  octet nul ; un pointeur vise avant le début du segment courant. Un octet de pointeur n'est donc jamais couvert par
  un segment : deux segments terminés par un pointeur sont disjoints (sinon l'un couvrirait le pointeur de l'autre, ou
  ils auraient le même pointeur, donc la même cible) ; le dernier segment finit avant le dernier pointeur et ne
  chevauche que le segment qui précède. Les caractères du nom sont les octets couverts (une longueur devient un point) ;
- le sérialiseur écrit un caractère en six octets au plus (caractère de contrôle) ; un nom fait au plus 6 × 1 024 + 2
  octets, un entier de type 5 caractères, un TTL 10 ;
- octets de JSON par octet du message, élément de `reponses` virgule comprise :

| réponse (nom en pointeur, 2 octets) | octets du message | JSON au plus | par octet |
|---|---|---|---|
| SOA, `mname` et `rname` en pointeurs | 2 + 10 + 2 + 2 + 20 = 36 | 18 × 1 024 + 85 = 18 517 | 514,36 |
| type inconnu, données vides | 12 | 6 × 1 024 + 27 = 6 171 | 514,25 |
| TXT vide | 12 | 6 × 1 024 + 25 = 6 169 | 514,08 |
| A | 16 | 6 × 1 024 + 40 = 6 184 | 386,5 |

  un nom en étiquettes sur place ou à la racine coûte plus d'octets pour un nom au plus aussi long ; une chaîne TXT
  donne au plus six octets par octet. D'où `reponses` ≤ 1 + 495 × 18 517 / 36 = 254 609,75 octets.

Témoin (`test_sante.Taille`, bornes lues au code) : 14 réponses SOA par sonde, trois noms de 1 024 caractères de
contrôle chacun (259 239 octets, au-delà de la borne) ; tout autre champ à sa borne. Ligne canonique, recomptée par le
test et par un calcul indépendant du code (`json.dumps`, brouillon du worker) :

| champ | octets |
|---|---|
| `d4` : 7 × 259 373 (`adresse` de 15 caractères) | 1 815 619 |
| `d5` : 7 × 260 872 (`nom` de 253 caractères de contrôle) | 1 826 112 |
| `fils` : `tardives` de 2 × 4 096 écarts de 18 caractères, comptes de 19 chiffres | 155 724 |
| `d3` : `sortie` de 4 096 caractères de contrôle, `code` de 11, instants de 17 | 24 658 |
| `disque` (2 × 39 chiffres), `d2`, `horloges`, `resolveur` | 97 + 67 + 59 + 66 |
| clés, `type`, `ws` de 11 caractères, `seq` de 640 chiffres, `prec`, ponctuation, saut de ligne | 822 |
| **ligne** | **3 823 224** (marge 371 080 sous LIMITE) |

Bornes voisines, même témoin : huit témoins et sept noms, 4 082 598 octets (marge 111 706) ; sept et huit,
4 084 097 ; huit et huit, 4 343 471, au-delà de LIMITE. Sept et sept laisse une marge qui couvre l'hypothèse sur
`tardives` (FORMAT §13.6 : 2 × `places` latences, un fil saisi entre la remise de sa place et le rendu de son
résultat non compté) pour 19 530 latences de plus.

Rouge : sur l'état CB-19a, huit témoins et huit noms admis, aucune borne au schéma (assertion du témoin), §13.6 et
§14.1 absents.

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/collecte/config.py` | 73 | — |
| `shogen_s2bis/collecte/entree.py` | 126 | — |
| `tests/test_entree.py` | 229 | 7 (1 de plus : sept admis, huit refusés, témoins puis noms) |
| `tests/test_sante.py` | 274 | 13 (1 de plus : plus grande `sante`, 3 823 224 octets, écrite sans refus) |
| `tests/test_format.py` | 141 | 6 (1 de plus : §13.6, §14.1, puce « Corrections ») |

Mutants (commande du job s2bis-unittest : runner, puis ligne de `gates.yml` ; borne de 300 s ; python3.12, `-X dev
-W error` ; réseau isolé ; témoin VIVANT) : 15 mutants neufs, 15 tués par leur test visé (0 vivant, 0 FATAL) :
- contrôle du nombre d'éléments retiré, n éléments refusés, huit témoins, huit noms, témoins ou noms sans borne,
  refus mal nommé, borne jamais lue : test des bornes au schéma ;
- sortie de D-3 doublée, pool de 8 192 places, nom de 254 caractères : témoin de la plus grande `sante`, recompté à
  l'octet (huit témoins, huit noms et bornes retirées aussi) ;
- trois textes du FORMAT défaits (total, borne du §14.1, hypothèse) ; plancher non relevé.

Suite : 190 tests ; plancher du job : 190, égalité exigée (`--egal`).

## CB-19c (2026-10-05) : fsync du dossier après chaque création (C-2 (a) de la relecture d'intégration de P1)

Objet : C-2 (a), adjugée telle qu'écrite : après la création d'un fichier du journal (journal neuf, bascule, segment
de reprise), sa première ligne écrite, et après la création du fichier de sommes, sa première ligne écrite et
synchronisée, l'écrivain appelle `fsync` sur le dossier (descripteur en lecture seule, `fsync` injecté). La première
ligne précède ce `fsync`, dont l'échec ne laisse pas un fichier vide. FORMAT §6.4 réécrit (la limite déclarée d'avant
est retirée ; celle du modèle du banc est écrite). L'espion de `test_journal.Base` relève à part les `fsync` du dossier
(`appels` : nom, instantané du dossier) ; `fsyncs` et `tailles` restent ceux des fichiers, et les assertions d'avant
sur eux tiennent sans changement. Le test du point d'entrée qui injecte une panne au « premier fsync » la vise
désormais au premier `fsync` d'un fichier, celui du dossier passant : c'est le scénario qu'il énonce (premier
marqueur), inchangé.

Rouge : sur l'état CB-19b, aucun `fsync` du dossier (`[] != [[…], …]`) ; §6.4 d'avant.

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/collecte/journal.py` | 397 | — |
| `tests/test_journal.py` | 294 | 14 (espion : `fsync` du dossier relevés à part) |
| `tests/test_fichiers.py` | 100 | 5 (1 de plus : un `fsync` du dossier après chaque création, fichier créé déjà écrit, aucun sans création) |
| `tests/test_entree.py` | 232 | 7 (panne injectée au premier `fsync` d'un fichier) |
| `tests/test_format.py` | 151 | 7 (1 de plus : §6.4, puce « Corrections ») |

Mutants (commande du job s2bis-unittest : runner, puis ligne de `gates.yml` ; borne de 300 s ; python3.12, `-X dev
-W error` ; réseau isolé ; témoin VIVANT) : 12 mutants neufs, 12 tués (0 vivant, 0 FATAL) :
- création sans `fsync` du dossier, `fsync` du dossier avant la première ligne, avant la création ; sommes créées
  sans lui, `fsync` à chaque somme sauf à la création, avant la première somme, création testée après l'ouverture :
  test des créations ;
- `fsync` du fichier courant au lieu du dossier, descripteur fermé avant le `fsync` : plusieurs tests de l'écrivain ;
- deux textes du FORMAT ; plancher non relevé.

Suite : 192 tests ; plancher du job : 192, égalité exigée (`--egal`).

## CB-19d (2026-10-05) : fsync de ce dont dépend une `reprise` en segment neuf (C-2 (b) et C-4 (c) de la relecture)

Objet : C-2 (b), adjugée telle qu'écrite : avant d'écrire une `reprise` en segment neuf, l'écrivain synchronise le
fichier dont elle chaîne la dernière ligne intègre et ceux dont elle déclare la queue, même déjà sommés ; avant
d'écrire la somme d'un fichier (reprise sur place comprise), il synchronise ce fichier. FORMAT §4 réécrit : points de
`fsync` énumérés, ce qui retire le « et seulement là » que les §6.2, §6.3 et §7.4 contredisaient (C-4 (c), portée ici
parce que C-2 réécrit le même paragraphe), preuve du banc, ce que son modèle prouve et ne prouve pas.

Preuve exigée, banc à coupures du réviseur (`outils/banc_ecrivain.py`, sha256 `edca2fa8…`, et sa sonde, `0b2d0dcd…`,
rejoués sans modification par un agrégateur du worker qui appelle `graine(g)` et compte l'état final comme la
relecture ; le même agrégateur sur la base 47b2177 redonne les chiffres de la relecture, ce qui valide le compte) :

| banc (graines) | état | redémarrages | queues déclarées | rupture finale | dont lien rompu | dont déclaration fausse | somme fausse | illisibles |
|---|---|---|---|---|---|---|---|---|
| coupures (0 à 299) | base 47b2177 | 1 455 | 576 | 128 | 86 | 86 | 131 | 14 |
| coupures (0 à 299) | CB-19d | 1 438 | 533 | 0 | 0 | 0 | 0 | 19 |
| sans coupure (0 à 999) | CB-19d | 4 876 | 1 622 | 0 | 0 | 0 | 0 | 27 |

Sans coupure, les 27 journaux illisibles et les trois refus finals (graines 39, 97 et 297) sont ceux de la mesure du
réviseur : C-2 n'ajoute aucune cause. Sous coupures, les trajectoires diffèrent de la base (le banc tire ses pannes
au sort à chaque `fsync`, et C-2 en ajoute) ; les illisibles restent ceux d'un journal neuf dont le premier fichier
n'est pas synchronisé avant son premier marqueur (item 1 de la relecture, non traité ici). Le modèle ne porte que sur
la taille des fichiers : la durabilité des entrées de dossier (C-2 (a)) n'est pas prouvée par ce banc.

Rouge : sur l'état CB-19c, aucun `fsync` des dépendances ni du fichier avant sa somme (`[] != […]`), §4 d'avant.

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/collecte/journal.py` | 405 | — |
| `tests/test_reprise.py` | 320 | 25 (2 de plus : deux reprises, la seconde après la coupure du segment de la première, dépendances déjà sommées ; somme rattrapée après le `fsync` du fichier) |
| `tests/test_format.py` | 163 | 8 (1 de plus : §4, points de `fsync`, preuve du banc et ses limites) |

Mutants (commande du job s2bis-unittest : runner, puis ligne de `gates.yml` ; borne de 300 s ; python3.12, `-X dev
-W error` ; réseau isolé ; témoin VIVANT) : 13 mutants neufs, 13 tués (0 vivant, 0 FATAL) :
- aucun `fsync` des dépendances, le fichier chaîné seul, les queues seules, après l'écriture de la reprise, condition
  inversée, `fsync` répété du seul fichier chaîné : test des deux reprises ;
- somme sans `fsync` du fichier, `fsync` après la somme : test de la somme rattrapée ;
- quatre textes du FORMAT (« et seulement là » revenu, résultat du banc, limites du modèle, puce) ; plancher non
  relevé.

Suite : 195 tests ; plancher du job : 195, égalité exigée (`--egal`).

## CB-19e (2026-10-05) : client réel dans la boucle, adresse avant la phase `dns` (C-3 (a) et (b) de la relecture)

Objet : C-3 (b) : le client pose l'adresse au suivi partagé avant la phase `dns`, que la boucle relève avant
l'adresse ; un relevé entre les deux écritures lisait une phase `dns` sans adresse (espion du réviseur). Test par
suivi espion. C-3 (a), tests seuls : le client réel (`http.lire`) dans la boucle, horloge murale de la boucle
partagée, horloge monotone réelle (délai réel de 10 s : la lecture pend encore au relevé, sans course) ; serveur qui
accepte, lit la requête et ne répond pas ; à E, `panne_transport`, `delai`, `phases` avec `dns` et `connexion`,
adresse posée. FORMAT §11.4 : l'ordre est écrit.

Rouge : sur l'état CB-19d, le suivi espion lit `[('dns', False)]` ; le test du client réel passe sur le code juste et
rougit sous MI-09 et MI-10 (échec d'assertion : `dns`, phases vides, adresse nulle).

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/collecte/http.py` | 134 | — |
| `tests/test_http_reseau.py` | 288 | 15 (1 de plus : suivi espion) |
| `tests/test_lecture_pendue.py` | 160 | 9 (1 de plus : client réel dans la boucle) |
| `tests/test_format.py` | 172 | 9 (1 de plus : §11.4, puce « Corrections ») |

Mutants (commande du job s2bis-unittest : runner, puis ligne de `gates.yml` ; borne de 300 s ; python3.12, `-X dev
-W error` ; réseau isolé ; témoin VIVANT) : 13 mutants (11 neufs ; MI-09 et MI-10 du réviseur), 13 tués (0 vivant,
0 FATAL) :
- MI-09 du réviseur, tel quel, et MI-10, réécrit sur le nouveau texte avec la même mutation (MI-10r) : tués par le
  test du client réel dans la boucle et par le suivi espion ;
- ordre d'avant (suivi espion) ; adresse jamais posée au suivi ; boucle : adresse jamais relevée, phases atteintes à E
  oubliées, sous-types échangés ; client : phases dans un dictionnaire neuf, phase `connexion` jamais posée, adresse
  sans port ;
- deux textes du FORMAT ; plancher non relevé.

Suite : 198 tests ; plancher du job : 198, égalité exigée (`--egal`).

## CB-19f (2026-10-05) : point d'entrée à w = 60, délai et places câblés (C-3 (c) et (d) de la relecture, tests seuls)

Objet : C-3 (c) : point d'entrée à w = 60 (valeurs de l'ADR : δ 20 s, tolérance 5 s, délai 10 s, marge 1 s) et une
horloge hors de la grille (12:34:56,789012 UTC le 2026-10-05, instant calculé par `date -u -d`) : journal ouvert à la
fenêtre de 12:34, `suivante` 12:35, `run_params` à 12:35, sortie 0 (`--fenetres 0`). C-3 (d) : `delai` (0,3 s) et
`places` (4 pour 2 formes) lus de `formes.json` arrivent à la boucle (client appelé avec ce délai ; quatre places,
pas une de plus). Aucun code de production ; puce « Corrections » du FORMAT.

Rouge : les tests passent sur le code juste ; sous MI-12, sortie 1 `JOURNAL/fenetre` ; sous MI-13, délai absent ;
sous MI-14, deux places : échecs d'assertion.

| fichier | lignes | tests |
|---|---|---|
| `tests/test_entree.py` | 259 | 9 (2 de plus : w = 60 sur la grille ; délai et places jusqu'à la boucle) |

Mutants (commande du job s2bis-unittest : runner, puis ligne de `gates.yml` ; borne de 300 s ; python3.12, `-X dev
-W error` ; réseau isolé ; témoin VIVANT) : 13 mutants, 13 tués (0 vivant, 0 FATAL) :
- MI-12, MI-13 et MI-14 du réviseur, tels quels : tués par le test w = 60 (MI-12) et par celui du délai et des places
  (MI-13, MI-14) ;
- journal ouvert une fenêtre plus tard, ouverture au rang de la fenêtre, journal sur une grille d'une seconde,
  `run_params` une minute après la première fenêtre admise : test w = 60 (et d'autres) ;
- `delta` au lieu du délai, une place de plus (entrée ou boucle), délai divisé, délai de l'ADR au lieu du délai
  scellé : test du délai et des places ;
- plancher non relevé.

Suite : 200 tests ; plancher du job : 200, égalité exigée (`--egal`).

## CB-19g (2026-10-05) : quatre phrases du FORMAT rendues exactes (C-4 (a), (b) et (d) de la relecture, FORMAT seul)

Objet : C-4, FORMAT seul, (c) étant portée par CB-19d (§4) : (a) §11.6, une lecture finie entre E et le relevé compte
en `tardives` à la fenêtre suivante ; (b) §11.5, `run_params` suit l'`ouverture` de la bascule qu'il déclenche ;
(d) §9.1 et §10.1, l'adresse d'une lecture est l'adresse résolue, contactée seulement si `phases` porte la connexion,
et une `dns` rendue après une résolution tardive porte `phases.dns` et une adresse non contactée. Aucun code de
production. Deux tests lient le texte au code existant : (d) résolution tardive (adresse résolue `127.0.0.1:1`, phase
`dns` seule) ; (b) redémarrage à 23:59, `reprise` et `cloture` au fichier du 4, `ouverture` et `run_params` au fichier
du 5. (a) l'est déjà par `test_boucle.Boucle.test_echeance_exacte_ecrivain_ralenti`.

Rouge : sur l'état CB-19f, les cinq textes attendus manquent ; les deux tests de comportement passent sur le code (ils
le décrivent) et rougissent sous les mutants qui le changent.

| fichier | lignes | tests |
|---|---|---|
| `tests/test_format.py` | 188 | 10 (1 de plus : C-4 (a), (b), (d), puce « Corrections ») |
| `tests/test_http_reseau.py` | 295 | 16 (1 de plus : résolution tardive) |
| `tests/test_reprise.py` | 333 | 26 (1 de plus : `run_params` après l'`ouverture` de la bascule) |

Mutants (commande du job s2bis-unittest : runner, puis ligne de `gates.yml` ; borne de 300 s ; python3.12, `-X dev
-W error` ; réseau isolé ; témoin VIVANT) : 11 mutants neufs, 11 tués (0 vivant, 0 FATAL) :
- cinq textes du FORMAT défaits ((a), (b), (d) au §9.1 et au §10.1, puce) : test nommé de C-4 ; l'ordre de
  `run_params` perdu au §11.5 : test de la convention (CB-18j) ;
- client : adresse retirée, phase `dns` retirée, résolution tardive classée `delai` : test de la résolution tardive
  (et deux tests existants) ;
- boucle : lecture rendue entre E et le relevé jamais tardive : tests de l'échéance (CB-11c) ;
- plancher non relevé.

Suite : 203 tests ; plancher du job : 203, égalité exigée (`--egal`).

## CB-19h (2026-10-05) : outillage de la CI, plancher 0 et chargement du vérificateur (C-5 de la relecture)

Objet : C-5 (a) : l'enregistreur de rôle (`s2-harness/tools/oracle_record.py`) lit la ligne du vérificateur du job
avec `--plancher [1-9][0-9]*`, comme K-02 du runner ; un commit dont la ligne porte `--plancher 0` (s2bis) ou
`--plancher 07` (sim-bis) est refusé avant toute écriture (sous-tests ajoutés au test des suites par la ligne du job).
C-5 (b) : le runner échoue fermé, sortie 3, sur toute exception au chargement du vérificateur, `SystemExit` compris ;
R-01 et R-02 lancent une copie du runner, avec le `gates.yml` réel, à côté d'un vérificateur qui sort en 0 ou lève à
son chargement. Aucun cas existant retiré ni affaibli ; les leurres du réviseur de CB-18 (`leurres_cc.py`,
`leurres_cc2.py`, `leurres_fetch.py`, du contre-contrôle cc5) donnent les mêmes verdicts sur la base et sur CB-19h
(sorties comparées après normalisation du chemin de l'arbre et du plancher affiché).

Rouge : runner de CB-19h avant le correctif du chargement, R-01 sortie 0 sans aucun cas, R-02 sortie 1 par trace
(85 ok, 2 échecs) ; test de l'enregistreur sur l'outil de la base, « ValueError not raised » pour les deux commits.

| fichier | lignes | tests |
|---|---|---|
| `enforcement/tests/run-fixtures-verdict-suite-s2.py` | 338 | 87 cas (2 de plus : R-01, R-02) |
| `s2-harness/tools/oracle_record.py` | 310 | — |
| `s2-harness/tests/test_oracle_record.py` | 436 | 12 (deux sous-tests de plus ; plancher de S2 inchangé, 406) |

Mutants (borne de 300 s ; python3.12, `-X dev -W error` ; réseau isolé ; témoins VIVANTS) : 11 mutants neufs, 11
tués (0 vivant, 0 FATAL) :
- runner, classés par la commande du job s2bis-unittest (le runner en est la première étape ; sortie 1 du runner :
  tué) : chargement réduit à deux exceptions (avant C-5), `SystemExit` non attrapé, chargement en échec en sortie 0 ou
  1, message du refus altéré, runner qui continue après l'échec du chargement : R-01 et R-02 ;
- enregistreur, classés par la commande du job s2-harness-unittest (runner, puis `verdict-suite-s2.py --egal`) :
  plancher 0 admis (trois écritures), zéro de tête admis : test des suites par la ligne du job (sous-tests des
  planchers 0 et 07).

Runner : 87 cas. Suite s2bis : 203 tests, plancher 203 inchangé. Suite S2 : 406 tests, plancher 406 inchangé.

### Mutants de la relecture d'intégration de P1 rejoués sur l'état final, par la commande du job

Les 30 mutants du réviseur (`outils/mutants.py`, sha256 `59b4fd2c…`, liste lue sans modification) rejoués sur l'état
de CB-19h par la commande du job s2bis-unittest (runner, puis ligne de `gates.yml` à `--plancher 203` ; borne de
300 s ; python3.12, `-X dev -W error` ; réseau isolé ; témoin VIVANT) : 30 tués, 0 vivant, 0 FATAL. MI-10, dont le
texte visé a changé avec C-3 (b), est rejoué réécrit avec la même mutation (MI-10r). Les cinq vivants de la relecture
sont tués par les tests neufs qui les visent : MI-09 et MI-10 par le client réel dans la boucle (et le suivi espion),
MI-12 par le point d'entrée à w = 60, MI-13 et MI-14 par le délai et les places jusqu'à la boucle.

| série | mutants | tués | vivants | FATAL |
|---|---|---|---|---|
| neufs, CB-19a à CB-19h (13, 15, 12, 13, 11, 10, 11, 11) | 96 | 96 | 0 | 0 |
| du réviseur, rejoués sur l'état final | 30 | 30 | 0 | 0 |

## RB-1h (2026-10-05) : définition unique d'« intègre » au lecteur du recalcul (lettres C-1 et C-2 ; C-14)

Objet (lettres C-1 et C-2 du FORMAT, adjugées par l'orchestrateur le 2026-10-05 ; correction C-14 de la relecture G2
de RB-18) : le lecteur fait la définition unique du FORMAT §7.1, points (c) et (d), comme l'écrivain de référence.
`_types` exige un objet dont `type` est une chaîne, `seq` un entier et `prec` 64 chiffres hexadécimaux minuscules, en
tête de fichier comme ailleurs, et dont les champs propres des types réservés (§2 : `jour`, `suivante`, `ws`, `de`,
`a`, `queue`, `cause`) sont présents à leurs types exacts ; `ws` est un entier requis pour tout type non réservé
(risque R-2, vérifié type par type : `ws` null rend non intègre toute ligne d'un type qui porte `ws`, et reste un champ
ordinaire d'une `ouverture`, d'une `cloture` ou d'un `trou`). `type(v)` et non `isinstance` : un booléen n'est jamais
un entier. Avant (sondes du worker sur la tête) : `type` non contrôlé ; `seq` booléen admis par l'égalité `True == 1`
du lien ; `prec` de tête non contrôlé ; `a` d'un trou admis booléen (`+ 0`) ; `de`, `cause`, `jour`, `queue` et le `ws`
d'un `point` ou d'une `reprise` non contrôlés ; `ws` null admis pour un type non réservé. Une `reprise` dont `queue`
est un objet nu, ou dont `prec` est en majuscules, est une ligne non intègre (une queue), non une rupture : le §7.1
s'applique avant le §7.4. Déjà tenus, désormais fixés par un test : C-1 (un entier de plus de 640 chiffres rend la
ligne non intègre, quel que soit le réglage ; tests existants) ; point (a), ligne de 4 194 304 octets intègre et d'un
octet de plus en queue ; point (b), caractères hors ASCII en clair (séquence d'échappement : non canonique) ; état
après un `point` (type réservé : ni attendu ni dernière fenêtre). FORMAT §7.1.

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/recalc/lecteur.py` | 164 | — |
| `tests/test_lecteur.py` | 408 | 26 (6 de plus : champs propres type par type, champs communs et objet, `ws` null type par type, tête de segment non intègre, caractères hors ASCII en clair, ligne de LIMITE octets ; 1 complété : état après un `point`) |

Rouge : sur le code d'avant, 15 échecs d'assertion dans les 4 tests de C-14 et C-2 (11 sous-tests des champs propres,
champs communs, `ws` null, et les deux têtes de segment, lues comme ruptures) ; les deux tests des points (a) et (b) et
l'état après un `point` passent déjà (preuves de conformité). Mutants (commande du job, runner puis `--plancher 209`,
borne de 300 s ; python3.12 ; réseau isolé) : 19 tués sur 19 par leur test visé (0 vivant, 0 FATAL) : booléen admis pour
un entier, ou par `isinstance` ; `prec` en majuscules, de plus de 64 chiffres ou de forme libre ; `type` entier ou null
admis ; `de` et `cause` d'un trou, `jour` d'une clôture non exigés ; objet nu admis pour `queue` ; champ manquant pris
pour null ; `ws` d'un type non réservé non exigé et, en resserrement, exigé partout où il figure ; `point` retiré des
types réservés ; types jugés après la chaîne ; première ligne quelconque ; attendu d'un trou pris à `de` ; borne LIMITE
décalée d'un octet dans les deux sens ; forme canonique en séquences d'échappement. Première passe, 16 mutants sur
l'état d'avant les deux tests des points (a) et (b) : 16 tués, versée sans être comptée. Suite : 209 tests ; plancher du
job : 209, égalité exigée (`--egal`).

## RB-1i (2026-10-05) : déclaration des queues comparée sous forme canonique (lettre C-3 ; C-15)

Objet (lettre C-3 du FORMAT, adjugée par l'orchestrateur le 2026-10-05 ; correction C-15 de la relecture G2 de RB-18,
premier point) : la déclaration d'une `reprise` est comparée sous forme canonique (`_canonique`, FORMAT §1.2, qui sert
aussi au contrôle de canonicité de la ligne), non par l'égalité de Python, qui tient `true` pour `1` et `false` pour
`0` : une déclaration à booléens pour des entiers était lue comme exacte. Déjà tenus, désormais fixés par un test : une
liste exacte, dans l'ordre croissant (jour, k) des fichiers, déclare les queues ; un autre ordre, un champ de plus, une
liste vide ou null devant des queues en attente, une liste vide sans queue en attente (null exigé) font une
déclaration fausse ; à toute rupture (déclaration fausse, lien faux sous une déclaration exacte, `ouverture` au lieu
d'une reprise), toutes les queues en attente sont rendues avec elle et aucune n'est réputée déclarée ; une ligne aux
clés non triées n'est pas canonique. FORMAT §7.4.

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/recalc/lecteur.py` | 172 | — |
| `tests/test_lecteur.py` | 451 | 28 (2 de plus : déclaration exacte à deux queues en attente, huit cas ; liste vide sans queue en attente, null exigé ; 1 complété : clés non triées) |

Rouge : sur le code de RB-1h, 1 échec d'assertion (la déclaration à booléens, lue comme exacte) ; les autres cas passent
déjà (preuves de conformité). Mutants (commande du job, runner puis `--plancher 211`, borne de 300 s ; python3.12 ;
réseau isolé) : 12 tués sur 12 par leur test visé (0 vivant, 0 FATAL) : égalité de Python au lieu de la forme
canonique ; forme canonique sans tri des clés, ou en séquences d'échappement ; ordre décroissant attendu ; liste vide
attendue sans queue, ou prise pour null ; `cause` exigée dans la déclaration ; comparaison sans ordre ; queues non
rendues avec la rupture, ou réputées déclarées malgré elle ; lien jugé sur `seq` seul ; queue non déclarée tolérée
devant une `ouverture`. Suite : 211 tests ; plancher du job : 211, égalité exigée (`--egal`).

## RB-1j (2026-10-05) : 64 niveaux d'imbrication au plus, comptés par le lecteur (lettre C-4 ; C-15)

Objet (lettre C-4 du FORMAT, adjugée par l'orchestrateur le 2026-10-05 ; correction C-15 de la relecture G2 de RB-18,
second point) : le niveau d'une valeur est 1 pour l'objet de la ligne, n + 1 dans un conteneur de niveau n ; une ligne
dont un conteneur passe le niveau N = 64 n'est pas intègre (`LECTEUR/imbrication`). Le lecteur compte les niveaux
lui-même, sur les octets et avant tout décodeur (`_trop_profonde`) : échappements retirés (barre doublée, puis barre et
guillemet), guillemets restants pris pour bornes des chaînes, seuls les crochets hors des chaînes comptés, arrêt au
premier conteneur au-delà de 64 ; la barre oblique inverse est écrite par sa valeur (`bytes([92])`), le code n'ajoute
aucun octet 92. Une RecursionError du décodeur n'est plus prise pour un verdict : sur une ligne de 64 niveaux au plus,
elle remonte au lieu de faire une queue d'une ligne intègre. Avant : une ligne de 65 niveaux et plus était intègre
jusqu'au seuil de RecursionError du décodeur, puis nommée `LECTEUR/json` par l'exception ; ce seuil dépend de la
version (mesure du worker par dichotomie, appel depuis un script : `json` dès le niveau 992 sous 3.10 et 3.11, 9 998
sous 3.12, 9 999 sous 3.13), si bien que le verdict d'une même ligne changeait d'une version à l'autre. FORMAT §8.3,
§7.1 b.

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/recalc/lecteur.py` | 193 | — |
| `tests/test_lecteur.py` | 481 | 30 (2 de plus : niveaux 64 et 65 en listes, en objets et derrière une barre échappée, conteneurs larges, crochets d'une chaîne, guillemet échappé, 100 000 niveaux ; RecursionError non rattrapée ; 2 complétés : 100 000 niveaux nommés `LECTEUR/imbrication`, queue d'une ligne de 65 niveaux) |

Rouge : sur le code de RB-1i, 4 échecs d'assertion (dix cas des niveaux, dont 65 lus intègres en listes et en objets, et
100 000 nommés par RecursionError ; RecursionError rattrapée ; cause des 100 000 niveaux ; ligne de 65 niveaux lue
intègre en fin de fichier). Mutants (commande du job, runner puis `--plancher 213`, borne de 300 s ; python3.12 ; réseau
isolé) : 12 tués sur 12 par leur test visé (0 vivant, 0 FATAL) : N décalé d'une unité dans les deux sens (64 refusés, 65
admis) ; racine comptée deux fois ; barre doublée non retirée ; guillemet échappé pris pour une borne ; crochets des
chaînes comptés, ou seuls comptés ; objets non comptés ; fermants ignorés (nombre d'ouvrants pris pour le niveau) ;
octets effacés inversés ; niveaux non comptés (RecursionError seule) ; RecursionError prise pour un verdict. Suite : 213
tests ; plancher du job : 213, égalité exigée (`--egal`).

## RB-1k (2026-10-05) : grammaire des noms de fichiers au lecteur (lettre C-5)

Objet (lettre C-5 du FORMAT, adjugée par l'orchestrateur le 2026-10-05 ; FORMAT §6.1 et §7.7) : k suit `0|[1-9][0-9]*`
et l'ordre des fichiers est (jour, k entier) ; un nom qui commence par `<préfixe>-` et finit par `.jsonl` hors de cette
grammaire est un refus nommé (`LECTEUR/nom`), y compris un numéro complété de zéros, une date mal formée, un nom
prolongé après `.jsonl` et un préfixe prolongé (limite O-2, §5) ; « pas de numéro sur trois chiffres » s'entend d'un
numéro complété de zéros (parenthèse du FORMAT §6.1) : `-100`, sans zéro de tête, est le segment 100 ; un autre préfixe,
une autre fin ou le préfixe sans tiret sont ignorés ; un dossier sans fichier du journal, vide ou non, reste un refus
nommé (`LECTEUR/absent`). Avant (sondes du worker sur la souche) : `-01`, `-00` et `-007` étaient lus comme segments 1,
0 et 7 (`-00` à côté de `-0` : deux segments 0), les sept autres noms non conformes ignorés.

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/recalc/lecteur.py` | 203 | — |
| `tests/test_lecteur.py` | 511 | 31 (1 de plus : dossier vide, six voisins ignorés, ordre de six fichiers dont le segment 100, dix noms refusés) |

Rouge : sur le code de RB-1j, 1 échec d'assertion (premier nom non conforme lu sans refus). Mutants (commande du job,
runner puis `--plancher 214`, borne de 300 s ; python3.12 ; réseau isolé) : 12 tués sur 12 par leur test visé (0 vivant,
0 FATAL) : zéro de tête admis ; k = 0 refusé ; k de trois chiffres refusé ; date hors grammaire admise ; k comparé en
texte ; nom hors grammaire ignoré, ou refusé seulement sans fichier du journal ; préfixe sans tiret, ou fin en
majuscules, refusés ; nom prolongé après `.jsonl` ignoré (`match` au lieu de `fullmatch`) ; dossier sans fichier du
journal admis ; refus mal nommé. Première passe, 11 mutants, avant l'ajout du segment 100 au test : 11 tués, versée sans
être comptée. Suite : 214 tests ; plancher du job : 214, égalité exigée (`--egal`).

## RB-18a (2026-10-05) : lecteur indépendant, ligne canonique, champs communs, noms (recalé sur 98c8537)

Objet : premier diff du lecteur indépendant `recalc/oracle_indep.py` (E-R-33 ; PROPOSITION du G0 de RECALC-BIS l.396,
l.486, l.539-540), écrit d'après le seul FORMAT, sans lire le lecteur principal (RB-1) : `objet` (ligne terminée par
0x0A, objet JSON canonique, sans flottant ni NaN), `champs` (champs communs du §1.3), `fichiers` (noms
`<préfixe>-AAAA-MM-JJ-k.jsonl`, ordre (jour, k entier)) ; frontière : bibliothèque standard seule, ni lecteur principal
ni écrivain. Recalage (C-13 de la G2 de RB-18) : `recalc/__init__.py` et la règle `recalc` de `REGLES` sont déjà en
tête, ce diff n'y touche plus. Le refus d'un entier long et l'oubli des noms hors grammaire sont corrigés par RB-18e et
RB-18g.

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/recalc/oracle_indep.py` | 64 | — |
| `tests/test_oracle_indep.py` | 96 | 10 (ligne canonique, échappements, non canonique, UTF-8, imbrication, entiers longs, réglage de l'interpréteur, champs communs, noms, frontière) |

Mutants (commande du job, `--plancher 224`, borne de 300 s ; python3.12 ; réseau isolé) : 19 tués sur 19 (0 vivant,
0 FATAL) : canonicité sautée, clés non triées, hors ASCII en séquence `u`, bornes 639 et 641, signe compté, flottant,
NaN, ligne non objet, refus avant le jugement, RecursionError non attrapée, nom du refus, booléen pour `seq`, majuscules
dans `prec`, k comparé en texte, zéro de tête, préfixe non échappé, import de l'écrivain, décodage latin-1. Suite : 224
tests ; plancher du job : 224, égalité exigée (`--egal`).

## RB-18b (2026-10-05) : lecture en flux, genèse, lien entre fichiers, queues, ruptures (recalé sur 98c8537)

Objet : `Lecture` lit chaque fichier jusqu'à la première ligne non intègre, qui ouvre la queue du fichier (octet de
début, longueur, sha256) ; la première ligne d'un fichier est une `ouverture` ou une `reprise` ; au premier
enregistrement de chaque fichier, lien au dernier intègre, ou genèse (`ouverture`, `seq` 0, `prec` nul) ; rupture à
causes nommées (`genese`, `lien`, `queue-non-declaree`), la lecture continue ; queue finale, tête ; `lire`. FORMAT §1.3,
§1.4, §7.1, §7.7. Journaux produits par l'écrivain réel, puis altérés à la main.

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/recalc/oracle_indep.py` | 143 | — |
| `tests/test_oracle_indep.py` | 213 | 17 (7 de plus : journal intact sur deux jours, queue tronquée, rupture sans reprise, lien rompu par le seul `prec`, fichiers manquants, genèse et première ligne, dossier vide ou absent) |

Mutants (commande du job, `--plancher 231`, borne de 300 s ; python3.12 ; réseau isolé) : 17 tués sur 17 (0 vivant,
0 FATAL) : première ligne de type quelconque, `prec` ou `seq` non contrôlés, champs communs non contrôlés, `prec` et
type de la genèse non contrôlés, lien sans `prec`, jonction au seul premier fichier, liste de la rupture vidée, queue
soldée deux fois ou non signalée, queue prise depuis le début, ligne coupée finale ignorée, queue finale perdue, nom du
refus de lecture, rupture sans cause, chaînage figé. Suite : 231 tests ; plancher du job : 231, égalité exigée
(`--egal`).

## RB-18c (2026-10-05) : déclaration des queues par la `reprise` (recalé sur 98c8537)

Objet : `cle` (forme canonique de comparaison : `true` n'égale pas 1) ; à chaque `reprise`, les queues en attente sont
comparées à la liste `queue`, rupture `declaration` sinon ; une `reprise` au milieu d'un fichier ne déclare rien. FORMAT
§7.2 à §7.4. L'appariement est encore un multiensemble : RB-18h le remplace par la déclaration exacte de la lettre C-3.

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/recalc/oracle_indep.py` | 157 | — |
| `tests/test_oracle_indep.py` | 322 | 27 (10 de plus : ligne coupée dans un caractère, reprise d'un segment neuf, reprise à la suite, reprise un autre jour, segments de jour, déclaration fausse, déclaration stricte, douze segments d'un jour, fichier renommé, reprise au milieu) |

Mutants (commande du job, `--plancher 241`, borne de 300 s ; python3.12 ; réseau isolé) : 11 tués sur 11 (0 vivant,
0 FATAL) : reprise au milieu non contrôlée, `true` égal à 1, déclaration soldée laissée en compte, queue déclarée non
rendue, déclaration sans queue non signalée, liste de la rupture vidée, appariement inversé, clés non triées dans la
comparaison, champ mal nommé, liste lue comme une seule déclaration, queue non déclarée non signalée. Suite : 241 tests
; plancher du job : 241, égalité exigée (`--egal`).

## RB-18d (2026-10-05) : LIMITE, lieu du refus, sortie canonique, ligne de commande (recalé sur 98c8537)

Objet : lignes lues par `readline(LIMITE)` (une ligne de plus de 4 194 304 octets, saut compris, ouvre la queue) ;
`sortie` (JSON trié, séparateurs sans espace, UTF-8, 0x0A final) et `main` (code 0, refus nommé en code 1, usage en code
2) ; lieu du refus. FORMAT §7.1. Recalage : à la tête, l'écrivain refuse un entier de 641 chiffres (`JOURNAL/entier`,
SHOGEN-S2BIS-ENTIER-ECRIVAIN-1) ; la ligne qui en porte un est écrite à la main dans le test.

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/recalc/oracle_indep.py` | 187 | — |
| `tests/test_oracle_indep.py` | 394 | 32 (5 de plus : limite d'une ligne, entiers longs dans un journal, premier fichier manquant, queue finale sur deux fichiers, sortie dorée, refus et usage) |

Mutants (commande du job, `--plancher 246`, borne de 300 s ; python3.12 ; réseau isolé) : 11 tués sur 11 (0 vivant,
0 FATAL) : bornes LIMITE + 1 et LIMITE - 1, ligne non bornée, position du refus perdue, refus sans lieu, sortie sans
0x0A final, séparateurs avec espaces, codes de sortie du refus et de l'usage, nom du refus altéré, refus muet sur la
sortie. Suite : 246 tests ; plancher du job : 246, égalité exigée (`--egal`).

## RB-18e (2026-10-05) : entier long et imbrication, ligne non intègre (C-7, C-11 de la G2 de RB-18 ; lettres C-1, C-4)

Objet : un entier de plus de 640 chiffres, signe exclu, rend la ligne non intègre (§1.2, §7.1 b) : le refus
`ORACLE/entier-long` disparaît. Les niveaux d'imbrication sont comptés par le lecteur sur le texte de la ligne, avant le
décodeur (échappements, puis chaînes, puis tout sauf crochets et accolades sont retirés) : un conteneur au-delà du
niveau N = 64, l'objet de la ligne au niveau 1, rend la ligne non intègre, que `json` la lise (65 niveaux) ou lève
RecursionError (100 000 niveaux) ; l'exception n'est plus attrapée (§8.3). La forme canonique du contrôle est `cle`.
Rouge : sur le code de RB-18d, 65 niveaux admis, et refus `ORACLE/entier-long` au lieu d'une queue.

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/recalc/oracle_indep.py` | 196 | — |
| `tests/test_oracle_indep.py` | 406 | 32 (4 réécrits : imbrication comptée par le lecteur (64 et 65 niveaux, listes et objets alternés, crochets dans les chaînes, guillemet et barre échappés), entiers longs, réglage de l'interpréteur, entier long ou imbrication dans un journal ; refus de la ligne de commande sur un dossier absent) |

Mutants (commande du job, `--plancher 246`, borne de 300 s ; python3.12 ; réseau isolé) : 15 tués sur 15 (0 vivant,
0 FATAL) : bornes N + 1 et N - 1, niveau N refusé, niveaux non comptés (décodeur seul), seul le guillemet échappé
retiré, échappements laissés dans les chaînes, crochets des chaînes comptés, fermetures non décomptées, racine au niveau
0, borne 641, signe compté, entier long lu par int, flottant admis, ligne non objet admise, dossier absent en exception
nue. Suite : 246 tests ; plancher du job : 246, égalité exigée (`--egal`).

## RB-18f (2026-10-05) : champs propres typés, `queue` ni liste ni null (C-9, C-6 de la G2 de RB-18 ; lettre C-2)

Objet : `champs` suit le §7.1 c et d : `seq` entier, `prec` 64 chiffres hexadécimaux minuscules, puis les champs propres
du §2 (`jour` et `cause` chaînes, `queue` liste ou null, `suivante`, `ws`, `de`, `a` entiers), présents ; le `ws` d'un
type non réservé est requis et entier ; un booléen n'est jamais un entier ; un champ de plus est admis. C-6 : une
`reprise` dont `queue` n'est ni une liste ni null n'est pas intègre (§7.1 d ; le §7.4 le dit d'un objet nu) : elle ouvre
la queue de son fichier, au lieu d'être lue comme déclaration (défaut E11). Rouge : sur le code de RB-18e, champs
propres manquants admis, et un objet nu `queue` égal à la queue en attente la déclarait.

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/recalc/oracle_indep.py` | 204 | — |
| `tests/test_oracle_indep.py` | 437 | 34 (2 de plus : champs propres des types réservés et `ws` des autres ; `queue` objet, chaîne, entier ou booléen ; lignes de genèse écrites avec leurs champs propres) |

Mutants (commande du job, `--plancher 248`, borne de 300 s ; python3.12 ; réseau isolé) : 13 tués sur 13 (0 vivant,
0 FATAL) : suivante d'ouverture, queue de reprise, cause de trou, jour de clôture, ws du marqueur, du point et d'un type
non réservé non exigés, objet nu admis pour queue, booléen admis pour un entier, jour typé entier, cause entière admise,
champ manquant lu comme null, seq non contrôlé. Suite : 248 tests ; plancher du job : 248, égalité exigée (`--egal`).

## RB-18g (2026-10-05) : grammaire des noms, refus `ORACLE/nom` et `ORACLE/vide` (C-8 de la G2 de RB-18 ; lettre C-5)

Objet : un nom qui commence par `<préfixe>-` et finit par `.jsonl` hors de la grammaire `<préfixe>-AAAA-MM-JJ-k.jsonl`
(k suivant `0|[1-9][0-9]*`, chiffres ASCII, nom entier) est un refus `ORACLE/nom`, qui nomme le premier en ordre des
points de code ; un dossier sans fichier du journal est un refus `ORACLE/vide` ; tout autre nom reste ignoré ; date non
contrôlée au calendrier (validité, RB-3). La sortie échappe en séquence JSON un caractère qu'UTF-8 n'écrit pas (nom hors
UTF-8 rendu par `os.listdir`), au lieu de lever. FORMAT §6.1, §7.7. Rouge : sur le code de RB-18f, noms fautifs ignorés
et dossier vide lu sans refus.

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/recalc/oracle_indep.py` | 214 | — |
| `tests/test_oracle_indep.py` | 472 | 35 (1 de plus : quatorze noms hors grammaire, dont zéro de tête, numéro sur trois chiffres, chiffre non ASCII, nom prolongé, nom hors UTF-8, et le premier de deux en ordre des points de code ; grammaire et ordre, dossier vide et sortie de la ligne de commande réécrits) |

Mutants (commande du job, `--plancher 249`, borne de 300 s ; python3.12 ; réseau isolé) : 15 tués sur 15 (0 vivant,
0 FATAL) : nom hors grammaire ignoré, préfixe sans tiret refusé, fin en .jsonl non reconnue, premier nom fautif pris
dans l'ordre du listage, dossier sans fichier du journal admis, dossier rendu comme fichier du refus, octet hors UTF-8
brut ou exception en sortie, zéro de tête admis, mois sur un chiffre, chiffres Unicode dans k, nom prolongé après .jsonl
admis, nom en .jsonl.bak lu, k comparé en texte, préfixe non échappé. Suite : 249 tests ; plancher du job : 249, égalité
exigée (`--egal`).

## RB-18h (2026-10-05) : déclaration exacte, queues rendues avec la rupture (C-10 de la G2 de RB-18 ; lettre C-3)

Objet : une `reprise` au lien juste déclare exactement les queues en attente : liste dans l'ordre (jour, k) des
fichiers, ou null sans queue, comparée sous forme canonique ; une liste vide, null avec une queue en attente, un autre
ordre, une partie, un doublon ou un booléen pour un entier font une déclaration fausse ; à toute rupture, toutes les
queues en attente sont rendues avec elle ; la déclaration d'une `reprise` au lien rompu n'est pas lue (G-07). Test de
deux pannes de l'écrivain réel, la seconde coupant la `reprise` du segment neuf : le troisième démarrage déclare les
deux queues (G-08). FORMAT §7.4, §7.7. Rouge : sur le code de RB-18g, appariement en multiensemble, déclaration lue
malgré le lien rompu, liste vide et null admis.

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/recalc/oracle_indep.py` | 214 | — |
| `tests/test_oracle_indep.py` | 510 | 37 (2 de plus : reprise au lien faux, par `prec` puis par `seq` ; reprise qui déclare deux queues, puis autre ordre, partie, doublon ; déclaration stricte et reprise au milieu réécrites) |

Mutants (commande du job, `--plancher 251`, borne de 300 s ; python3.12 ; réseau isolé) : 11 tués sur 11 (0 vivant,
0 FATAL) : déclaration lue malgré le lien rompu, null refusé et liste vide admise, ordre (jour, k) non exigé,
déclaration fausse sans cause nommée, queues d'une déclaration fausse non dites non déclarées, liste des queues vidée
après la rupture, une seule queue retenue comme déclarée, genèse par une reprise admise, queues en attente jamais
soldées, prec du lien non contrôlé, null sans queue refusé. Suite : 251 tests ; plancher du job : 251, égalité exigée
(`--egal`).

## RB-18i (2026-10-05) : sortie hors ASCII, usage, mémoire de `Lecture` (C-12 de la G2 de RB-18, tests seuls)

Objet : tests vivants fermés : G-13, un caractère hors ASCII (é, U+2028) sort en UTF-8, sans séquence d'échappement ;
G-14, la ligne de commande exige deux arguments (zéro, un ou trois : code 2, sortie vide) ; mémoire de `Lecture` mesurée
par tracemalloc sur des journaux de 1 et 4 Mio (pics mesurés de 35 360 à 47 762 octets sous Python 3.10 à 3.13) : moins
de 256 Kio, et le pic ne croît pas avec le journal. Seule la docstring de `Lecture` change dans le code. Rouge : chaque
test contre le mutant qu'il ferme (sortie en séquences `u`, trois arguments admis, fichier lu en entier : pic de
4 300 762 octets) ; les deux premiers mutants survivaient aux tests de RB-18h.

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/recalc/oracle_indep.py` | 215 | — |
| `tests/test_oracle_indep.py` | 547 | 40 (3 de plus : sortie hors ASCII, usage, mémoire bornée ; le test de la sortie dorée ne porte plus l'usage) |

Mutants (commande du job, `--plancher 254`, borne de 300 s ; python3.12 ; réseau isolé) : 11 tués sur 11 (0 vivant,
0 FATAL) : sortie en séquences u, sortie en latin-1, forme canonique en séquences u, trois arguments admis, zéro ou un
argument admis, un ou trois arguments admis, codes d'usage 1 et 0, usage sur la sortie standard, fichier lu en entier,
tampon de 8 Mio. Suite : 254 tests ; plancher du job : 254, égalité exigée (`--egal`).

## RB-1l (2026-10-05) : ligne en UTF-8 strict avant le compte des niveaux et le décodeur (NC-1 du contre-contrôle)

Objet (NC-1 du contre-contrôle de RB-1, adjugé par l'orchestrateur) : `_integre` décode la ligne en UTF-8 strict avant
le compte des niveaux et le décodeur JSON, qui lisent ainsi le même texte ; une erreur de décodage rend la ligne non
intègre (`LECTEUR/utf8`). Avant : `json.loads` recevait les octets bruts et y reconnaissait l'UTF-16 ou l'UTF-32 par
leurs octets nuls, alors que `_trop_profonde` comptait sur l'UTF-8 : une ligne en UTF-16-LE close par 00 0A, d'un niveau
au compte, menait le décodeur dans K crochets, et RecursionError sortait sans verdict (K = 2 000 sous 3.10 ; K = 20 000
sous 3.10 et 3.12). Un BOM UTF-8 n'est plus retiré en silence (ligne non intègre, `LECTEUR/json`). FORMAT §7.1 b.

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/recalc/lecteur.py` | 209 | — |
| `tests/test_lecteur.py` | 539 | 32 (1 de plus : les deux lignes minimales de NC-1, K = 2 000 et 20 000, un octet 0xFF, un BOM ; chacune en queue à la position 145) |

Rouge : sur le code d'avant, 4 échecs d'assertion sous 3.10 (les deux lignes de NC-1 : RecursionError ; 0xFF nommé
`json` ; BOM nommé `canonique`), 3 sous 3.12 (K = 2 000 y passe). Mutants (commande du job, runner puis `--plancher
255`, borne de 300 s ; python3.12 ; réseau isolé) : 6 tués sur 6 par leur test visé (0 vivant, 0 FATAL) : `json.loads`
rétabli sur les octets bruts (NC-1) ; décodage non strict (remplacement), en latin-1, ou avec retrait du BOM ; erreur de
décodage non rattrapée ; cause de l'octet invalide mal nommée. Suite : 255 tests ; plancher du job : 255, égalité exigée
(`--egal`).

## CB-6a (2026-10-08) : décodeurs BTC des huit places repris de S2, finitude (E-C-06, E-C-08)

Objet (partie P2, tranche A ; sous-lot CB-6 de la PROPOSITION) : module `collecte/decodeurs.py`, un décodeur par
(hôte, actif) pour les huit places BTC de S2 (Binance, Coinbase, Kraken, OKX ticker et index, Bitstamp, Gemini,
Bitfinex), repris par copie de `s2-harness/shogen_s2/sources.py` (l.84-218) avec leurs pièges (Bitfinex position 6,
Kraken clé rendue et liste d'erreurs, code d'OKX) ; fixtures de S2 copiées octet pour octet (`tests/fixtures/btc/`,
sha256 comparés aux originaux par le test ; pièce G6). Écarts à S2, nommés : aucun flottant (prix : texte du Decimal
lu ; instant de la source en microsecondes entières, de 0 à 2^53 exclu) ; prix fini, > 0, exposant dans les bornes du
contexte nommé, copie de celui de S2 (r1.py l.62-68) ; instant ISO lu par un motif (`fromisoformat` lit autrement de
3.10 à 3.13 : essai du worker) ; `decoder` ne lève jamais (`panne_decode`). Valeurs attendues hors du code :
`s2-harness/tests/expected.json`, lu en Decimal depuis son texte.

Rouge : sur un bouchon qui rend toujours `panne_decode`, 6 des 8 tests neufs échouent par assertion ; les deux autres
(fixtures identiques à celles de S2 ; corps illisible, vide ou trop profond en panne) passent sur ce bouchon par
construction.

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/collecte/decodeurs.py` | 91 | — |
| `tests/test_decodeurs.py` | 108 | 8 (neuf : reprise des fixtures et des valeurs de S2 ; pièges ; finitude ; corps illisible) |
| `tests/fixtures/btc/` (huit fichiers `.bin`, copies) | — | — |

Mutants (commande du job s2bis-unittest : runner, puis ligne de `gates.yml` ; borne de 300 s ; python3.12, `-X dev
-W error` ; réseau isolé ; témoin vert) : 20 mutants, 20 tués par leur test visé (0 vivant, 0 FATAL) : finitude
retirée, prix nul admis, exposant non borné, Bitfinex au dernier élément ou à moins de 10 champs, Kraken à la clé
demandée ou sans sa liste d'erreurs, code d'OKX ignoré, champ ou devise d'OKX échangés, classe de Coinbase,
millisecondes de Gemini lues en secondes, fraction ISO non tronquée, décalage ignoré, 2^53 ou instant négatif admis,
attrape-tout réduit, motif ISO partiel, instant sans décalage lu hors UTC, plancher non relevé. Suite : 263 tests ;
plancher du job : 263, égalité exigée (`--egal`).

## CB-6b (2026-10-08) : agrégateurs et Chainlink BTC de S2, contexte nommé, instants bornés (E-C-06, E-C-07, E-C-11)

Objet : décodeurs CoinGecko, DefiLlama (`confidence` en extra) et Chainlink (`latestRoundData` : cinq mots en
hexadécimal strict, réponse signée au mot 2, instant `updatedAt` au mot 4, `roundId` en extra ; prix construit
exactement, mantisse et exposant −8, sans division), fixtures copiées ; tout décodage sous le contexte nommé, jamais
celui du fil (Q-C-14). Correction C-1 de la G2 de P2A : les cinq instants convertis par `int()` (OKX `ts`, DefiLlama
`timestamp`, Bitstamp `timestamp`, Gemini `volume.timestamp`, CoinGecko `last_updated_at`) passent par une aide unique,
`_entier`, qui refuse avant la conversion un Decimal fini d'exposant ajusté de 16 ou plus (10^16 > 2^53 : aucun instant
recevable n'est refusé) et un texte de plus de 4 300 caractères : `int()` d'un Decimal à grand exposant est quadratique
et tient le GIL (1E+1000000 : 10,5 s, mesuré), ce qui faisait manquer l'échéance du pool (E-C-11, E-C-12).
Corrections C-2 (G01 à G03) : six mots de Chainlink, réponse égale à 2^255 (négative) et décalage ISO négatif figés par
un cas de test chacun.

Rouge : sur le code de CB-6a, le test de Chainlink et la reprise des valeurs de S2 (onze décodeurs attendus)
échouent par assertion ; le test du contexte nommé passe sur ce code, qui portait déjà le contexte : ses trois mutants
(contexte du fil, précision 28, Overflow non piégé) le font échouer. C-1 : sur le code de CB-6b d'avant la G2, les
cinq tests de `Bornes` échouent par assertion (un par champ : `panne_decode`, mais après plus de 0,1 s). C-2 : le code
d'avant était juste ; chaque cas neuf échoue sous le mutant du réviseur qu'il vise (G01, G02, G03).

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/collecte/decodeurs.py` | 128 | — |
| `tests/test_decodeurs.py` | 172 | 15 (7 de plus : Chainlink, cas hostiles tirés de la réponse valide ; contexte nommé sous un contexte de fil hostile ; un test de `Bornes` par champ d'instant, cinq) |
| `tests/fixtures/btc/` (trois fichiers `.bin` de plus, copies) | — | — |

Mutants (même commande) : 12 mutants du sous-lot, 12 tués par leur test visé (0 vivant, 0 FATAL), rejoués sur l'état
corrigé ; au premier passage d'origine, « hexadécimal non strict » vivait (cas hostiles tous à réponse nulle) : test
corrigé, campagne relancée. Liste : `startedAt` au lieu d'`updatedAt`, réponse non signée, hexadécimal non strict, six
décimales, `roundId` au mot 3, `confidence` perdue, secondes de CoinGecko lues en millisecondes, classe agrégateur pour
Chainlink, contexte du fil, précision 28, Overflow non piégé, plancher non relevé. Corrections : 10 mutants neufs, 10
tués par leur test visé : borne d'exposant retirée (« borne retirée »), borne de texte retirée, l'une ou l'autre
relâchée, OKX, Gemini ou DefiLlama sans l'aide, borne serrée qui refuse le témoin, six mots admis, 2^255 lu positif.
Suite : 270 tests ; plancher du job : 270, égalité exigée.

## CB-6c (2026-10-08) : lecture décodée, valeurs refusées par l'écrivain jamais rendues (E-C-06, E-C-17)

Objet : chaque forme de `formes.json` nomme son décodeur (`decodeur`, règle `decodeur-connu`) ; `decodeurs.appliquer`
décode le corps de chaque lecture `ok`, dans le fil de la lecture (`valeurs` : liste de relevés, FORMAT §9.1, §14.1).
Des valeurs que l'écrivain refuserait (types, `journal.canonique`) ou de plus de 2 097 152 octets canoniques ne sont
jamais rendues : la lecture est `panne_decode`, la boucle continue ; l'item SHOGEN-S2BIS-ECRIVAIN-REFUS-ARRET-1 est
fermé pour les décodeurs. Témoin : la plus longue ligne de lecture (corps de 1 048 576 octets, valeurs à leur borne)
mesure 3 496 800 octets, sous LIMITE (4 194 304). Correction C-5 de la G2 de P2A : la restriction du motif ISO
(« T » et « Z » majuscules ; « t », « z », l'espace et `+hhmm` refusés) est écrite au §9.1 avec sa raison (même
lecture de 3.10 à 3.13), écart à S2 et à la RFC 3339 §5.6 nommé ; deux cas de casse ajoutés au test de l'instant ISO.

Formes BTC (C-3 de la G2 de P2A, écart déclaré) : ce diff ne verse aucune forme de requête BTC (aucune donnée sous
`s2bis/config/`) ; les décodeurs et les fixtures de S2 sont versés, pas les requêtes. Les formes viennent avec CB-8
(regroupement de CoinGecko, DefiLlama et Bitfinex, E-C-09 ; plan d'OKX), chacune comparée aux octets de la requête de
S2 : item SHOGEN-S2BIS-FORMES-BTC-1, déclencheur CB-8.

Rouge : sur le code de CB-6b, les tests neufs échouent par assertion ; les tests existants dont la configuration de
test porte désormais `decodeur` échouent aussi (refus `CONFIG/champ-inconnu` du schéma d'avant), trois d'entre eux en
erreur (configuration refusée avant l'assertion). Puis le §9.1 et le §14.1 du FORMAT, absents : échec d'assertion.
C-5 : sur le FORMAT d'avant la G2, le test des §9 et §14 échoue par assertion (restriction et raison absentes).

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/collecte/decodeurs.py` | 146 | — |
| `shogen_s2bis/collecte/entree.py` | 128 | — |
| `tests/test_bout_en_bout.py` | 218 | 1 (corps de `binance.bin` servi ; `valeurs` contrôlées contre le §9.1) |
| `tests/test_decodeurs.py` | 239 | 19 (4 de plus : valeurs refusées jamais rendues ; panne HTTP inchangée ; boucle continue ; plus longue ligne) |
| `tests/test_entree.py` | 274 | 10 (1 de plus : lecture décodée par le décodeur de sa forme) |
| `tests/test_format.py` | 206 | 11 (1 de plus : §9.1, dont la restriction ISO, §14.1 et puce « Partie P2 ») |

Mutants (même commande) : 16 mutants du sous-lot, 16 tués par leur test visé (0 vivant, 0 FATAL), rejoués sur l'état
corrigé : garde de l'écrivain retirée, borne de taille retirée, exclue ou doublée, prix flottant admis, instant booléen
admis, extra non contrôlé, pannes décodées, corps ou code perdus, lecture non décodée, décodeur d'une autre forme, règle
`decodeur-connu` retirée, champ `decodeur` hors du schéma, item retiré du §9, plancher non relevé. Corrections : 3
mutants neufs, 3 tués par leur test visé : majuscule effacée du §9.1, motif ISO sans casse, « t » minuscule admis.
Suite : 276 tests ; plancher du job : 276, égalité exigée.

## CB-6d (2026-10-08) : trois items de l'annexe B fermés (tardives bornées, niveaux comptés sur les octets, graphe)

Objet :
- SHOGEN-S2BIS-TARDIVES-BORNE-1 : la boucle rend le résultat d'une lecture avant sa place ; une lecture non rendue tient
  donc toujours sa place, et `tardives` reste borné par `places` (FORMAT §13.6) ;
- SHOGEN-S2BIS-ECRIVAIN-IMBRICATION-OCTETS-1 : `Journal._lire` compte les niveaux sur les octets de la ligne, en UTF-8
  strict, avant tout décodeur (copie du compte du lecteur du recalcul, gardée identique par un test de fitness) ;
  RecursionError n'est plus prise pour un verdict (FORMAT §8.3) ;
- SHOGEN-S2BIS-CORPS-BORNE-1, volet graphe : `canonique` compte les valeurs une fois par occurrence, chaque conteneur
  partagé développé une seule fois, et refuse au-delà de LIMITE (`JOURNAL/taille`) en temps borné (FORMAT §8.4).

Rouge : sur le code de CB-6c, les 5 tests neufs échouent par assertion (graphe partagé non refusé, niveaux comptés
après le décodeur, place rendue avant le résultat, copie du compte absente, FORMAT).

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/collecte/boucle.py` | 136 | — |
| `shogen_s2bis/collecte/journal.py` | 430 | — |
| `tests/test_boucle.py` | 325 | 15 (1 de plus : résultat rendu avant la place) |
| `tests/test_fitness.py` | 106 | 6 (1 de plus : copie du compte des niveaux identique à celle du recalcul) |
| `tests/test_format.py` | 217 | 12 (1 de plus : §8.3, §8.4, §13.6 et puce « Partie P2 ») |
| `tests/test_journal.py` | 316 | 15 (1 de plus : graphe partagé refusé en temps borné) |
| `tests/test_reprise.py` | 352 | 27 (1 de plus : niveaux comptés sur les octets avant le décodeur) |

Mutants (même commande) : 11 mutants, 11 tués par leur test visé (0 vivant, 0 FATAL), rejoués sur l'état corrigé ; un
mutant reconnu équivalent avant la campagne (décodage UTF-8 avec remplacement) a été remplacé (copie altérée). Liste :
place rendue avant le résultat, niveaux non comptés avant le décodeur, RecursionError prise pour un verdict, décodeur
sur les octets bruts (NC-1), copie altérée (échappement, compte), valeurs non comptées, comptées sans multiplicité,
borne doublée, §13.6 défait, plancher non relevé. Suite : 281 tests ; plancher du job : 281, égalité exigée.

## CB-12a (2026-10-08) : drapeau TC et identifiant sur 16 bits du client DNS (SHOGEN-S2BIS-DNS-TC-1, -DNS-ID-16BITS-1)

Objet : une réponse appariée au drapeau TC est retenue, `tc` vrai, `rcode` lu, section réponse non lue (`reponses`
null), sans repli en TCP (choix du lot) ; un identifiant hors de 0 à 65 535, booléen compris, est un refus nommé de
`requete`, donc `forme` pour `interroger` (avant : `struct.error`, non nommé). FORMAT §12.

Rouge : sur le code de CB-6d, les 3 tests neufs échouent par assertion (réponse coupée lue, drapeau perdu ;
`struct.error` ; §12).

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/collecte/dns.py` | 130 | — |
| `tests/test_dns.py` | 265 | 17 (2 de plus : drapeau TC, section non lue ; identifiant hors de 16 bits) |
| `tests/test_format.py` | 226 | 13 (1 de plus : §12 et puce « Partie P2 ») |

Mutants (même commande) : 11 mutants, 11 tués par leur test visé (0 vivant, 0 FATAL) au second passage, rejoués sur
l'état corrigé ; au premier, « bit RD pris pour TC » était tué par un autre test que le visé : le test du drapeau
emploie désormais 0x82 (TC sans RD), campagne relancée. Liste : section lue malgré TC, drapeau perdu, rcode non lu sous
TC, bit RD pris pour TC, identifiant non contrôlé, 65 536, booléen ou −1 admis, refus non rattrapé par `interroger`, §12
défait, plancher non relevé. Suite : 284 tests ; plancher du job : 284, égalité exigée.

## CB-12b (2026-10-08) : relevé ASN d'un hôte : A propre, RIPEstat, Team Cymru (E-C-30)

Objet : module `collecte/asn.py`, `releve(hote, resolveur)` : A de l'hôte au résolveur de l'observateur (client DNS de
CB-10, récursion demandée), première adresse de type A ; RIPEstat prefix-overview sur cette adresse (client HTTPS de
CB-3 ; forme de S2, `r2._ripestat_asn` : `data.asns[0].asn` et `.holder`, `data.resource`) ; TXT de Team Cymru au même
résolveur (forme de S2, `_cymru_asn`). Chaque partie journalisée à part, brute et décodée ; échec typé, sans jugement ;
sans adresse (NXDOMAIN, CNAME seul, drapeau TC), RIPEstat et Cymru non interrogés ; ne lève jamais. Corps RIPEstat
synthétique, sans capture ni réseau (AS de documentation 64500, préfixe 192.0.2.0/24). FORMAT §15.4 (CB-13b).
Corrections C-2 de la G2 de P2A (G14, G17) : l'AS 0, admis par le FORMAT §15.4 (de 0 à 2³² exclu), et la première
chaîne d'un TXT à deux chaînes, figés par un cas de test chacun (RIPEstat `asn` 0 et TXT « 0 | x » : 0 ; TXT
« 64500 | x », « 64501 | y » : 64500).

Rouge (refait sur les tests finals ; bouchon sans effet : constantes de CB-12b, fonctions qui ne lisent rien) : 4 des 5
tests échouent par assertion (7 échecs, sous-tests compris) ; le témoin de taille passe sur ce bouchon par construction.
Le premier rouge, pris en cours de sous-lot, finissait sur une erreur après trois échecs d'assertion du même test. C-2 :
le code d'avant était juste ; chaque cas neuf échoue sous le mutant du réviseur qu'il vise (G14, G17).

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/collecte/asn.py` | 68 | — |
| `tests/test_asn.py` | 129 | 5 (neuf : relevé complet ; échecs typés ; RIPEstat, bornes et base muette ; Cymru ; plus grand relevé sous LIMITE) |

Mutants (même commande) : 17 mutants du sous-lot, 17 tués (0 vivant, 0 FATAL), 16 par leur test visé, rejoués sur l'état
corrigé ; « borne doublée » l'est par le test de RIPEstat (détenteur de 4 096 caractères admis), le témoin de taille,
visé, se calculant sur la borne. Liste : dernière adresse au lieu de la première, A sans filtre de type, RIPEstat sans
l'adresse, nom de Cymru non inversé, RIPEstat non décodé, indécodable gardé `ok`, dernier AS au lieu du premier, booléen
ou 2^32 admis, borne des valeurs relâchée ou doublée, types des champs non contrôlés, premier TXT seulement, TXT sans
filtre de type, dernier champ du TXT, bases interrogées sans adresse, plancher non relevé. Corrections : 2 mutants
neufs, 2 tués par leur test visé : AS 0 refusé, seconde chaîne du TXT. Suite : 289 tests ; plancher du job : 289,
égalité exigée.

## CB-13a (2026-10-08) : processus secondaire, relevé ASN hors du fil qui écrit (E-C-30 à E-C-32 ; Q-C-04)

Objet : module `collecte/secondaire.py`, classe `Secondaire`, sous-classe de la boucle du pool : lectures de la carte
au départ ws + w − δ, sans sondes ; relevé ASN dû à la première fenêtre de l'exécution, puis à la première fenêtre lue
qui suit un instant de la cadence scellée (ws mod `periode` = `decalage`) : un instant sauté (fenêtre sautée, arrêt)
est rattrapé, en mémoire seule, sans relecture du journal (E-C-15 ; C-4 de la G2 de P2A, Q-2 adoptée) ; noté par
`releve_asn` (`hotes`, `lance`), lancé sur un fil démon si le précédent a rendu (un fil de relevé au plus) ; chaque hôte
relevé est remis par une file au fil de la boucle, seul écrivain, qui l'écrit en `asn` en tête de la fenêtre suivante ;
un défaut imprévu d'un hôte s'écrit `asn` à `a` null, et le relevé continue. FORMAT §15.3 et §15.4 (CB-13b).

Rouge : sur un bouchon (boucle de la carte sans relevé), 2 des 3 tests d'origine échouent par assertion ; le troisième
(départ à ws + 5 s sans sondes) passe sur ce bouchon, comportement hérité de la boucle : M13a-04 le fait échouer. C-4 :
sur le code de CB-13a d'avant la G2 (relevé aux seuls instants de la cadence), le test neuf échoue par assertion (un
seul `releve_asn`, à m(6), au lieu de m(3), m(5) et m(6)).

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/collecte/secondaire.py` | 46 | — |
| `tests/test_secondaire.py` | 86 | 4 (neuf : départ à ws + 5 s sans sondes ; relevé hors du fil qui écrit, jamais relancé en double ; cadence, défaut noté sans arrêt ; relevé au démarrage, instant sauté rattrapé) |

Mutants (même commande) : 11 mutants du sous-lot, 11 tués par leur test visé (0 vivant, 0 FATAL), rejoués sur l'état
corrigé : relevé sur le fil de la boucle, écriture depuis le fil du relevé, relevé relancé malgré le précédent vivant,
cadence ou décalage ignorés, hôtes dans l'ordre de la configuration, défaut imprévu qui arrête le relevé, hôte perdu sur
défaut, relevés jamais écrits, résolveur de l'observateur perdu, plancher non relevé. Corrections : 3 mutants neufs, 3
tués par leur test visé : aucun relevé au démarrage, instant sauté non rattrapé, mémoire de la dernière fenêtre non
tenue. Suite : 293 tests ; plancher du job : 293, égalité exigée.

## CB-13b (2026-10-08) : `carte.json`, budget de débit partagé, commande `secondaire`, isolement (E-C-32, E-C-33)

Objet : `carte.json` scellé (`depart`, `delai`, `marge`, `places`, cadence `asn`, `formes`, liste vide admise : forme
de schéma `[s, n, 0]` neuve dans `config.controler`) ; règles de forme du pool appliquées aux formes de la carte ; cinq
règles croisées avec `formes.json` du pool, refus nommés : `budget-partage` (E-C-33 : lectures du pool et de la carte,
ensemble, au plus 5 par hôte et par fenêtre ; règle scellée, Q-1 de la G2 de P2A adoptée : plafond que le G0 de la
carte peut serrer hôte par hôte), `espace-partage`, `hors-delta` (E-C-32 : toute lecture de la carte finit avant le
départ du pool), `marge-carte`, `cadence` ; `construire_secondaire` (journal `secondaire` sur la grille du pool, départ
ws + `depart`, hôtes du pool et de la carte relevés au résolveur du descripteur) ; commande `secondaire`. FORMAT §15
écrit (processus secondaire, relevé ASN de CB-12b et CB-13a, dont le relevé au démarrage et le rattrapage de C-4) ;
§12, §13.1 et §14.2 retouchés (§12 : aucun repli en TCP pour le relevé ASN non plus, Q-3 adjugée, taux de troncature
au rodage, SHOGEN-S2BIS-ASN-TRONCATURE-1). Correction C-2 de la G2 de P2A (G20) : `periode` de 86 401 s refusée
(`CONFIG/borne`), figée par un cas de test.

Rouge : sur des bouchons (aucune règle croisée, câblage du pool, pas de commande `secondaire`), les 4 tests neufs
échouent par assertion (12 échecs, sous-tests compris). C-2 : le code d'avant était juste ; le cas neuf échoue sous le
mutant du réviseur qu'il vise (G20).

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/collecte/config.py` | 73 | — |
| `shogen_s2bis/collecte/entree.py` | 191 | — |
| `tests/test_format.py` | 237 | 14 (1 de plus : §15, règles croisées du code nommées, renvoi du §12, puce « Partie P2 ») |
| `tests/test_secondaire.py` | 195 | 7 (3 de plus : règles croisées à la borne ; construction ; pool et secondaires ensemble, carte pendue, carte refusée) |

Mutants (même commande) : 21 mutants du sous-lot, 21 tués par leur test visé (0 vivant, 0 FATAL), rejoués sur l'état
corrigé : budget relâché d'une lecture ou compté sur la carte seule, espace de la carte seule, `hors-delta` sans les
décalages, sans égalité ou sans le δ du pool, marge ignorée, décalage hors de la période ou période hors de la grille
admis, règles de forme non appliquées à la carte, délai, départ, places ou préfixe du journal pris au pool, hôtes du
pool non relevés, budget non contrôlé à la commande, carte vide refusée, liste vide admise partout, fichiers du
secondaire dans le désordre, renvoi du §12 perdu, plancher non relevé. Corrections : 1 mutant neuf, tué par son test
visé (`periode` de 86 401 s admise). Les 26 mutants de la G2 de P2A, rejoués sur cet état : 26 tués, dont les six
vivants de la G2 (G01, G02, G03, G14, G17, G20), chacun par le cas neuf qui le vise. Suite : 297 tests ; plancher du
job : 297, égalité exigée.

## CB-15a (2026-10-08) : requête RFC 3161, statut d'une réponse, manifeste (E-C-36)

Objet : premier sous-lot de CB-15 (PROPOSITION l.223 ; FORMAT §16.1 à §16.3). Requête d'horodatage en DER, construite en
bibliothèque standard, égale aux octets d'`openssl ts -query -sha256 -cert -no_nonce` (PROPOSITION §2.4 « Jeton ») et,
avec nonce, aux octets d'openssl pour le nonce qu'il a tiré ; statut d'une réponse lu sans plus (signature contrôlée
hors ligne, `openssl ts -verify`) ; manifeste des têtes en ligne canonique. RFC 3161 lue au fichier du registre ; X.690
non détenue : octets de référence d'OpenSSL 3.0.13.

Rouge : squelette d'interface (fonctions qui rendent une valeur fausse), 7 tests en échec d'assertion.

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/collecte/tetes.py` | 79 | — |
| `tests/test_tetes.py` | 98 | 7 |

Mutants (campagne refaite sur l'état corrigé ; commande exacte du job s2bis-unittest : runner, puis ligne de `gates.yml`
; borne de 300 s ; python3.12 ; réseau isolé ; témoin VIVANT) : 19 mutants (19 de la phase 1, 0 neufs de la correction),
19 tués (18 par leur test visé, 1 par la ligne du job sans test visé), 0 vivant, 0 FATAL : certReq absent (PROPOSITION
§2.4), certReq faux, identifiant d'algorithme faux (sha384) (PROPOSITION §2.4), paramètres NULL absents, version 2,
INTEGER sans zéro de tête, forme courte jusqu'à 255, forme longue non minimale, empreinte courte admise, nonce sans
borne haute, nonce booléen admis, présence du jeton non contrôlée, statut 6 admis, octets en trop admis, longueur longue
non minimale admise, jeton hors SEQUENCE admis, statut sur plusieurs octets admis, manifeste non trié, plancher non
relevé.

Variante sur c58b997 et la série P2A corrigée (FORMAT : ces paragraphes deviennent §16 et §17) : mutants de la campagne
de la série sur c58b997 (mêmes fichiers mutés, code de P2B inchangé hors des fusions de `boucle.py` et `entree.py`), non
rejoués sur la variante ; suite et plancher mesurés sur l'état de la variante.

Suite : 304 tests ; plancher du job : 304, égalité exigée (`--egal`).

## CB-15b (2026-10-08) : fichiers de tête, export atomique, lecture stricte du dépôt (E-C-35)

Objet : dépôt des têtes (AVIS du G0, Q-D-03 : un dossier, lisible ou non ; FORMAT §16.4, §16.5). Export de la tête du
point de contrôle par écriture atomique (fichier temporaire synchronisé, renommé, dossier synchronisé), sans jamais
lever ; lecture des fichiers de tête des autres journaux, 16 au plus, 1 024 octets au plus, refus nommés `TETES/…` ;
aucune valeur lue n'est un entier que l'écrivain refuserait (SHOGEN-S2BIS-ECRIVAIN-REFUS-ARRET-1). Correction de la G2
de P2B (2026-10-08) : noms d'observateur en minuscules seules au dépôt (C-6 : un jumeau de casse est ignoré) ; FORMAT
§16 : le dépôt est un dossier local, synchronisé par une unité séparée (C-7, Q-2 ; DB-4).

Rouge : `Depot` d'interface, 4 tests en échec d'assertion. Rouges de la correction (correction retirée du code, test
gardé ; python3.12 -X dev -W error) : R-C6a (ROUGE D'ASSERTION : FAIL 1, ERROR 0).

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/collecte/tetes.py` | 166 | — |
| `tests/test_tetes.py` | 205 | 11 (4 de plus) |

Mutants (campagne refaite sur l'état corrigé ; commande exacte du job s2bis-unittest : runner, puis ligne de `gates.yml`
; borne de 300 s ; python3.12 ; réseau isolé ; témoin VIVANT) : 20 mutants (19 de la phase 1, 1 neufs de la correction),
20 tués (19 par leur test visé, 1 par la ligne du job sans test visé), 0 vivant, 0 FATAL : écriture sur place, non
atomique, fichier temporaire non synchronisé, dossier non synchronisé, un échec d'export lève dans la boucle, échec
jamais effacé, sa propre tête relue, tête de son autre journal exclue, taille non bornée, forme canonique non contrôlée,
clés exactes non contrôlées, nom et contenu non comparés, booléen admis comme entier, entiers sans borne haute,
empreinte non contrôlée, nombre de têtes non borné, têtes ignorées non comptées, dossier illisible : la lecture lève,
grammaire des noms relâchée, plancher non relevé, C-6 : jumeau de casse lu au dépôt.

Variante sur c58b997 et la série P2A corrigée (FORMAT : ces paragraphes deviennent §16 et §17) : mutants de la campagne
de la série sur c58b997 (mêmes fichiers mutés, code de P2B inchangé hors des fusions de `boucle.py` et `entree.py`), non
rejoués sur la variante ; suite et plancher mesurés sur l'état de la variante.

Suite : 308 tests ; plancher du job : 308, égalité exigée (`--egal`).

## CB-15c (2026-10-08) : enregistrement `tetes` et export dans la boucle, `--depot` (E-C-35)

Objet : avec un dépôt, la fenêtre qui clôt l'heure porte `tetes` avant sa `sante` (têtes des autres journaux consignées
dès leur lecture), et la tête de son point de contrôle est exportée après le marqueur (FORMAT §2, §11.5, §14.1, §14.3,
§16.6) ; option `--depot` du point d'entrée ; nom d'observateur `[a-z0-9]{1,16}` (règle `observateur-nom`, il nomme ses
fichiers au dépôt). Correction de la G2 de P2B (2026-10-08) : nom d'observateur `[a-z0-9]{1,16}` au descripteur (C-6,
Q-8) : « O1 » est refusé.

Rouge : boucle et point d'entrée qui ignorent le dépôt, 3 tests en échec d'assertion (le quatrième, sans dépôt, est vert
par construction : non-régression). Rouges de la correction (correction retirée du code, test gardé ; python3.12 -X dev
-W error) : R-C6b (ROUGE D'ASSERTION : FAIL 1, ERROR 0) ; R-G18a (ROUGE D'ASSERTION : FAIL 1, ERROR 0).

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/collecte/boucle.py` | 146 | — |
| `shogen_s2bis/collecte/entree.py` | 198 | — |
| `tests/test_tetes.py` | 272 | 15 (4 de plus) |
| `tests/test_entree.py` | 274 | 10 |

Mutants (campagne refaite sur l'état corrigé ; commande exacte du job s2bis-unittest : runner, puis ligne de `gates.yml`
; borne de 300 s ; python3.12 ; réseau isolé ; témoin VIVANT) : 14 mutants (13 de la phase 1, 1 neufs de la correction),
14 tués (13 par leur test visé, 1 par la ligne du job sans test visé), 0 vivant, 0 FATAL : `tetes` jamais écrit, `tetes`
et export à chaque fenêtre, tête jamais exportée, tête exportée qui n'est pas celle du point, fenêtre exportée décalée,
sans dépôt, la boucle casse à l'heure, champs de la lecture du dépôt perdus, dépôt non câblé, journal du dépôt mal
nommé, nom d'observateur non contrôlé, nom d'observateur relâché, option --depot sans effet, plancher non relevé, C-6 :
nom en majuscules admis au descripteur.

Variante sur c58b997 et la série P2A corrigée (FORMAT : ces paragraphes deviennent §16 et §17) : mutants de la campagne
de la série sur c58b997 (mêmes fichiers mutés, code de P2B inchangé hors des fusions de `boucle.py` et `entree.py`), non
rejoués sur la variante ; suite et plancher mesurés sur l'état de la variante.

Suite : 312 tests ; plancher du job : 312, égalité exigée (`--egal`).

## CB-15d (2026-10-08) : jeton du jour, `.tsr` conservé et journalisé (E-C-36)

Objet : jeton du jour (AVIS Q-D-03, point 1 ; FORMAT §16.5, §16.7) : manifeste des têtes valides du dépôt, dont au moins
une de l'observateur, et requête au nonce donné, écrits au dépôt ; envoi seulement par une fonction donnée ; réponse
accordée conservée en `.tsr`, jamais redemandée le même jour ; ses têtes lues d'abord. Correction de la G2 de P2B
(2026-10-08) : la réponse accordée est liée à la requête avant d'être conservée (C-1 ; RFC 3161 §2.2 : contenus
SignedData et TSTInfo ; au TSTInfo, algorithme SHA-256, empreinte du manifeste, nonce ; refus `JETON/liaison` ou
`JETON/reponse`, rien de conservé ; signature et certificat contrôlés hors ligne, limite déclarée), éprouvée sur des
réponses d'`openssl ts -reply` d'une TSA jetable à clé détruite (juste, autre empreinte, autre nonce, sans nonce) ; une
réponse au statut 1 est conservée (G-01) ; les têtes de l'observateur sont lues d'abord, hors de la borne des autres
(C-2) ; le champ `jeton` du `tetes` passe à CB-15e (R-25) (FORMAT §16.2, §16.5, §16.7).

Rouge : `lire_tetes` et `jeton` d'interface, 5 tests en échec d'assertion. Rouges de la correction (correction retirée
du code, test gardé ; python3.12 -X dev -W error) : R-C1 (ROUGE D'ASSERTION : FAIL 1, ERROR 0) ; R-C2 (ROUGE D'ASSERTION
: FAIL 1, ERROR 0) ; R-G01 (ROUGE D'ASSERTION : FAIL 1, ERROR 0).

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/collecte/tetes.py` | 241 | — |
| `tests/test_tetes.py` | 377 | 19 (4 de plus) |

Mutants (campagne refaite sur l'état corrigé ; commande exacte du job s2bis-unittest : runner, puis ligne de `gates.yml`
; borne de 300 s ; python3.12 ; réseau isolé ; témoin VIVANT) : 18 mutants (9 de la phase 1, 9 neufs de la correction),
18 tués (17 par leur test visé, 1 par la ligne du job sans test visé), 0 vivant, 0 FATAL : jeton du jour redemandé,
jeton sans tête de l'observateur, sa tête exclue du manifeste, requête non écrite, rejet conservé, réponse non
contrôlée, nonce omis, armement inversé, plancher non relevé, C-1 : empreinte du TSTInfo non contrôlée, C-1 : nonce du
TSTInfo non contrôlé, C-1 : algorithme du TSTInfo non contrôlé, C-1 : types de contenu (SignedData, TSTInfo) non
contrôlés, C-1 : liaison au nonce absent, C-1 : écart de liaison sous le code d'une réponse mal formée, C-2 : la borne
des autres appliquée à ses têtes, C-2 : ses têtes non lues d'abord, C-2 : têtes ignorées comptées sous une seule borne.

Variante sur c58b997 et la série P2A corrigée (FORMAT : ces paragraphes deviennent §16 et §17) : mutants de la campagne
de la série sur c58b997 (mêmes fichiers mutés, code de P2B inchangé hors des fusions de `boucle.py` et `entree.py`), non
rejoués sur la variante ; suite et plancher mesurés sur l'état de la variante.

Suite : 316 tests ; plancher du job : 316, égalité exigée (`--egal`).

## CB-15e (2026-10-08) : envoi HTTPS armé par `--envoi`, commande `jeton` (E-C-36)

Objet : envoi de la requête à la TSA (RFC 3161 §3.4 : POST, `application/timestamp-query`, aucune redirection suivie,
réponse 200 de 65 536 octets au plus) ; commande `jeton`, dont l'envoi n'est armé que par `--envoi` (FORMAT §16.8 ;
ADR-0029 l.218 : sous le go écrit de l'investisseur). Aucune requête réseau réelle : serveur de boucle locale.
Correction de la G2 de P2B (2026-10-08) : envoi borné en temps et en octets, éprouvé par une TSA de boucle locale muette
puis bavarde (G-03, G-04) ; nonce de 64 bits tiré à chaque requête, figé par le test de la commande (G-16, C-5) ;
contexte TLS du point d'entrée transmis, http refusé (G-17) ; champ `jeton` du `tetes`, reçu de CB-15d (FORMAT §16.5,
§16.8).

Rouge : `envoyer` et commande d'interface, 2 tests en échec d'assertion. Rouges de la correction (correction retirée du
code, test gardé ; python3.12 -X dev -W error) : R-G03 (ROUGE D'ASSERTION : FAIL 1, ERROR 0) ; R-G04 (ROUGE D'ASSERTION
: FAIL 1, ERROR 0) ; R-G16 (ROUGE D'ASSERTION : FAIL 1, ERROR 0) ; R-G17 (ROUGE D'ASSERTION : FAIL 1, ERROR 0) ; R-G18b
(ROUGE D'ASSERTION : FAIL 1, ERROR 0).

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/collecte/tetes.py` | 278 | — |
| `shogen_s2bis/collecte/entree.py` | 228 | — |
| `tests/test_tetes.py` | 483 | 22 (3 de plus) |

Mutants (campagne refaite sur l'état corrigé ; commande exacte du job s2bis-unittest : runner, puis ligne de `gates.yml`
; borne de 300 s ; python3.12 ; réseau isolé ; témoin VIVANT) : 17 mutants (14 de la phase 1, 3 neufs de la correction),
17 tués (16 par leur test visé, 1 par la ligne du job sans test visé), 0 vivant, 0 FATAL : type de contenu faux (RFC
3161 §3.4), réponse HTTP non 200 admise, réponse sans borne, schéma de l'URL non contrôlé, chemin de l'URL perdu, envoi
armé sans --envoi, refus en sortie 0, jour non contrôlé, règles du descripteur non appliquées, refus du descripteur en
sortie 1, premier `.tsr` au lieu du dernier (champ `jeton`, porté par CB-15e), `.tsr` d'un autre observateur pris (champ
`jeton`, porté par CB-15e), `.tsr` illisible : la lecture lève (champ `jeton`, porté par CB-15e), plancher non relevé,
C-4 : lecture au-delà du plafond, attente du corps, C-5 : nonce de 63 bits, C-4 : point d'entrée sans contexte TLS par
défaut (http admis).

Variante sur c58b997 et la série P2A corrigée (FORMAT : ces paragraphes deviennent §16 et §17) : mutants de la campagne
de la série sur c58b997 (mêmes fichiers mutés, code de P2B inchangé hors des fusions de `boucle.py` et `entree.py`), non
rejoués sur la variante ; suite et plancher mesurés sur l'état de la variante.

Suite : 319 tests ; plancher du job : 319, égalité exigée (`--egal`).

## CB-17a (2026-10-08) : `status`, lecture du journal et jugement d'une santé (E-C-38)

Objet : lecture du journal du pool sans rien écrire ni prendre le verrou, une ligne `lecture` reconnue à ses premiers
octets et jamais décodée (PROPOSITION §2.4 « Status ») ; jugement d'une `sante` aux seuils de l'ADR-0029 §2.3, égaux au
bloc `degradation` d'`analyse.json` (test croisé) ; D-3 non jugé (SHOGEN-S2BIS-CHRONYC-FORMAT-1) ; FORMAT §17.1, §17.2.

Rouge : lecture et jugement d'interface, 5 tests en échec d'assertion.

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/collecte/status.py` | 69 | — |
| `tests/test_status.py` | 122 | 5 |

Mutants (campagne refaite sur l'état corrigé ; commande exacte du job s2bis-unittest : runner, puis ligne de `gates.yml`
; borne de 300 s ; python3.12 ; réseau isolé ; témoin VIVANT) : 17 mutants (17 de la phase 1, 0 neufs de la correction),
17 tués (16 par leur test visé, 1 par la ligne du job sans test visé), 0 vivant, 0 FATAL : `status` décode les lectures
(PROPOSITION §2.4 « Status »), `status` lit les lectures en panne, lecture à adresse null décodée, ligne illisible
sautée, fichier poursuivi, objet sans `seq` admis, journal absent sans refus, D-2 à 5 s tout juste, lecture non partie
ignorée (Q-C-02), retard null non admis, D-4 à 3 témoins, sonde nulle comptée répondue, rcode non nul compté résolu,
réponse sans A comptée résolue, santé illisible valide, relevé D-3 de code non nul non compté, seuil D-5 autre que celui
du recalcul, plancher non relevé.

Variante sur c58b997 et la série P2A corrigée (FORMAT : ces paragraphes deviennent §16 et §17) : mutants de la campagne
de la série sur c58b997 (mêmes fichiers mutés, code de P2B inchangé hors des fusions de `boucle.py` et `entree.py`), non
rejoués sur la variante ; suite et plancher mesurés sur l'état de la variante.

Suite : 324 tests ; plancher du job : 324, égalité exigée (`--egal`).

## CB-17b (2026-10-08) : `status`, état par fenêtre, rapport, strates, commande (E-C-38)

Objet : fenêtres de la première admise au dernier marqueur, D-1 sans marqueur, tête du dernier enregistrement lu ;
rapport de santé seule (FORMAT §17.3, §17.4), même sortie avec et sans `lecture` ; strates du calendrier ; commande
`status --journal`. Correction de la G2 de P2B (2026-10-08) : « hors D-3 » sur la ligne du compte local (C-7, Q-9 ;
FORMAT §17.4).

Rouge : état, rapport et commande d'interface, 4 tests en échec d'assertion (la sortie identique avec et sans lectures
est verte par construction sur un rapport constant : invariance). Rouges de la correction (correction retirée du code,
test gardé ; python3.12 -X dev -W error) : R-C7a (ROUGE D'ASSERTION : FAIL 1, ERROR 0).

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/collecte/entree.py` | 245 | — |
| `shogen_s2bis/collecte/status.py` | 121 | — |
| `tests/test_status.py` | 231 | 10 (5 de plus) |

Mutants (campagne refaite sur l'état corrigé ; commande exacte du job s2bis-unittest : runner, puis ligne de `gates.yml`
; borne de 300 s ; python3.12 ; réseau isolé ; témoin VIVANT) : 16 mutants (15 de la phase 1, 1 neufs de la correction),
16 tués (15 par leur test visé, 1 par la ligne du job sans test visé), 0 vivant, 0 FATAL : fenêtre sans marqueur valide,
première fenêtre admise ignorée, tête du premier enregistrement, relevés D-3 non cumulés, santé d'une autre fenêtre,
strates décalées, dernière fenêtre jugée sur la première, première fenêtre non comptée, disque inversé, nombre de
fenêtres faux, fenêtres dégradées comptées valides, format de l'heure, tête sans empreinte, refus en sortie 0, plancher
non relevé, C-7 : compte local sans « hors D-3 ».

Variante sur c58b997 et la série P2A corrigée (FORMAT : ces paragraphes deviennent §16 et §17) : mutants de la campagne
de la série sur c58b997 (mêmes fichiers mutés, code de P2B inchangé hors des fusions de `boucle.py` et `entree.py`), non
rejoués sur la variante ; suite et plancher mesurés sur l'état de la variante.

Suite : 329 tests ; plancher du job : 329, égalité exigée (`--egal`).

## CB-17c (2026-10-08) : résumés par jour, liste blanche, commande `resume` (AVIS Q-D-03, point 2)

Objet : un résumé par jour UTC, `[ws, codes]` de chaque fenêtre, publié au dépôt par la commande `resume` (FORMAT §17.5)
: clés fermées, aucun statut de source ; projection du journal, recalculable. Correction de la G2 de P2B (2026-10-08) :
C-3, portée ici (R-25 : CB-17b, où naît la grille, est à 183 lignes ; `resume` publie la grille jour par jour) : un `ws`
à la fin du jour de son fichier ou au-delà, ou une `suivante` au-delà, rend la ligne illisible et arrête le fichier ; un
fichier au jour hors du calendrier n'est pas lu ; la grille ne commence jamais avant le jour du premier fichier présent,
moins un jour (FORMAT §6.1, §17.1, §17.3). Les journaux corrompus de la G2 (MemoryError à 1,5 Gio) rendent la sortie 0
en moins de 2 s, espace d'adressage borné à 512 Mio.

Rouge : `resumes` et commande d'interface, 2 tests en échec d'assertion. Rouges de la correction (correction retirée du
code, test gardé ; python3.12 -X dev -W error) : R-C3 (ROUGE D'ASSERTION : FAIL 1, ERROR 0) ; R-C3b (ROUGE D'ASSERTION :
FAIL 1, ERROR 0) ; R-G18c (ROUGE D'ASSERTION : FAIL 1, ERROR 0).

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/collecte/entree.py` | 265 | — |
| `shogen_s2bis/collecte/status.py` | 155 | — |
| `tests/test_status.py` | 310 | 13 (3 de plus) |

Mutants (campagne refaite sur l'état corrigé ; commande exacte du job s2bis-unittest : runner, puis ligne de `gates.yml`
; borne de 300 s ; python3.12 ; réseau isolé ; témoin VIVANT) : 17 mutants (12 de la phase 1, 5 neufs de la correction),
17 tués (16 par leur test visé, 1 par la ligne du job sans test visé), 0 vivant, 0 FATAL : clé hors liste blanche,
fenêtres valides omises du résumé, fenêtre rangée au jour suivant, observateur faux au résumé, nom de fichier faux,
résumé non canonique, codes admis amputés, `resume` n'écrit rien, refus du descripteur en sortie 1, refus du journal en
sortie 0, règles du descripteur non appliquées, plancher non relevé, C-3 : jour du fichier non contrôlé, C-3 : grille
sans plancher, C-3 : plancher sans le jour de reprise, C-3 : jour hors du calendrier : exception, C-3 : `suivante` au-
delà du jour admise.

Variante sur c58b997 et la série P2A corrigée (FORMAT : ces paragraphes deviennent §16 et §17) : mutants de la campagne
de la série sur c58b997 (mêmes fichiers mutés, code de P2B inchangé hors des fusions de `boucle.py` et `entree.py`), non
rejoués sur la variante ; suite et plancher mesurés sur l'état de la variante.

Suite : 332 tests ; plancher du job : 332, égalité exigée (`--egal`).

## CB-17d (2026-10-08) : compte à quorum sur les résumés des autres (AVIS Q-D-03, point 3)

Objet : `status --depot --descripteur` ajoute le compte à quorum (M_j ≥ 2, ADR-0029 §2.2 pt 5) sur les résumés lisibles
des autres observateurs, lus strictement (`RESUME/…`), avec leur âge (FORMAT §17.6). Correction de la G2 de P2B
(2026-10-08) : « hors D-3 » sur la ligne du quorum (C-7 ; FORMAT §17.6) ; le résumé d'un nom en majuscules est ignoré
(C-6).

Rouge : rapport et commande qui ignorent le dépôt, 3 tests en échec d'assertion ; puis, à la relecture du générateur, un
résumé aux codes non textes faisait lever `status` (tri avant reconnaissance) : trois cas ajoutés au test des résumés
hostiles, l'exception comparée par son nom (échec d'assertion), puis codes reconnus avant le tri. Rouges de la
correction (correction retirée du code, test gardé ; python3.12 -X dev -W error) : R-C6c (ROUGE D'ASSERTION : FAIL 1,
ERROR 0) ; R-C7b (ROUGE D'ASSERTION : FAIL 1, ERROR 0).

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/collecte/entree.py` | 269 | — |
| `shogen_s2bis/collecte/status.py` | 208 | — |
| `tests/test_status.py` | 379 | 16 (3 de plus) |

Mutants (campagne refaite sur l'état corrigé ; commande exacte du job s2bis-unittest : runner, puis ligne de `gates.yml`
; borne de 300 s ; python3.12 ; réseau isolé ; témoin VIVANT) : 20 mutants (18 de la phase 1, 2 neufs de la correction),
20 tués (19 par leur test visé, 1 par la ligne du job sans test visé), 0 vivant, 0 FATAL : son propre résumé compté,
quorum à 1, sa validité non comptée, jours hors du journal local lus, taille non bornée, forme canonique non contrôlée,
clés exactes non contrôlées, nom et contenu non comparés, fenêtre hors du jour admise, fenêtre hors grille admise, code
inconnu admis, code en double admis, résumé sans fenêtre admis, âge au début de la fenêtre, --depot sans --descripteur
admis, quorum sans dépôt, codes triés avant d'être reconnus : un code non texte fait lever, plancher non relevé, C-6 :
résumé d'un nom en majuscules lu, C-7 : quorum sans « hors D-3 ».

Variante sur c58b997 et la série P2A corrigée (FORMAT : ces paragraphes deviennent §16 et §17) : mutants de la campagne
de la série sur c58b997 (mêmes fichiers mutés, code de P2B inchangé hors des fusions de `boucle.py` et `entree.py`), non
rejoués sur la variante ; suite et plancher mesurés sur l'état de la variante.

Suite : 335 tests ; plancher du job : 335, égalité exigée (`--egal`).

## CB-15f (2026-10-08) : dépôt, fichiers ordinaires seuls lus sans attente, aucun lien suivi (E-C-35)

Objet : relecture du générateur, après CB-17d. Au dépôt, un tube nommé au nom d'une tête, d'un `.tsr` ou d'un résumé
bloquait `open` sans fin (la boucle à la fenêtre qui clôt l'heure, `status`, `jeton`) ; un lien posé au nom du fichier
temporaire faisait écrire la tête dans sa cible. Lecture : fichier ordinaire seul, ouvert sans attente (`O_NONBLOCK`,
puis `fstat`), refus `TETES/lecture` ou `RESUME/lecture` ; `.tsr` de 65 536 octets au plus. Écriture atomique :
temporaire effacé, puis créé en exclusif (`O_EXCL`) ; un lien reposé entre les deux fait échouer l'écriture, la cible
intacte. Un dépôt illisible ne fait plus échouer `status` : le compte local reste, suivi de `quorum : dépôt illisible
(<exception>)` (AVIS Q-D-03, point 3 : le compte local toujours rendu) (FORMAT §16.9, §17.6). Correction de la G2 de P2B
(2026-10-08) : au `tetes`, avec le sha256 du dernier `.tsr`, ceux de son manifeste et de sa requête, null pour un
fichier illisible (C-5, Q-5 ; `empreinte_tsr` devient `empreinte`) (FORMAT §16.5).

Rouge : sur l'état CB-17d, 5 tests en échec d'assertion (trois appels bloqués, interrompus par une alarme de 2 s ; la
cible du lien écrasée par la tête ; `status` qui lève sur un dépôt absent, l'exception comparée par son nom) ; puis, la
première forme de la lecture perdant un descripteur à chaque dossier lu (relevé à la relecture : `open` d'un descripteur
de dossier lève sans le fermer), un échec d'assertion de plus (64 lectures, descripteurs comptés) avant la forme
`try`/`finally`. Rouges de la correction (correction retirée du code, test gardé ; python3.12 -X dev -W error) : R-C5
(ROUGE D'ASSERTION : FAIL 2, ERROR 0).

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/collecte/tetes.py` | 316 | — |
| `shogen_s2bis/collecte/status.py` | 212 | — |
| `tests/test_tetes.py` | 570 | 25 (3 de plus) |
| `tests/test_status.py` | 396 | 18 (2 de plus) |

Mutants (campagne refaite sur l'état corrigé ; commande exacte du job s2bis-unittest : runner, puis ligne de `gates.yml`
; borne de 300 s ; python3.12 ; réseau isolé ; témoin VIVANT) : 17 mutants (14 de la phase 1, 3 neufs de la correction),
17 tués (16 par leur test visé, 1 par la ligne du job sans test visé), 0 vivant, 0 FATAL : ouverture qui attend (tube
nommé), type du fichier non contrôlé, `.tsr` sans borne, `.tsr` de 65 536 octets refusé, tête lue par `open` (attente),
dernier `.tsr` lu par `_empreinte`, `.tsr` du jour lu par `_empreinte`, temporaire resté non effacé, création non
exclusive (lien suivi), résumé lu par `open` (attente), lecture bornée à la taille (dépassement jamais vu), dépôt
illisible qui fait échouer `status`, descripteur jamais fermé, plancher non relevé, C-5 : sha256 de la requête non
journalisé, C-5 : fichier illisible noté par une chaîne vide, C-5 : sha256 du `.tsr` au lieu du manifeste et de la
requête. Les 30 mutants de la G2 (G-01 à G-30), rejoués sur cet état : 30 tués (24 par leur test visé, 6 sans test
visé), 0 vivant, 0 FATAL ; G-01, G-03, G-04, G-16 et G-17, vivants à la G2, sont tués par leurs tests nommés (C-4).

Variante sur c58b997 et la série P2A corrigée (FORMAT : ces paragraphes deviennent §16 et §17) : mutants de la campagne
de la série sur c58b997 (mêmes fichiers mutés, code de P2B inchangé hors des fusions de `boucle.py` et `entree.py`), non
rejoués sur la variante ; suite et plancher mesurés sur l'état de la variante.

Suite : 340 tests ; plancher du job : 340, égalité exigée (`--egal`).

## DT6-a (2026-10-09) : borne basse des octets par occurrence, cycle refusé avant le sérialiseur (lot DETTES-T6)

Objet : SHOGEN-S2BIS-CANONIQUE-OCTETS-1 (O-4 de la G2 de P2A) et résiduel du volet graphe de SHOGEN-S2BIS-CORPS-BORNE-1.
`canonique` comptait une valeur par occurrence : une chaîne de 1 Mio partagée 1 000 fois passait la borne, puis le
sérialiseur écrivait 1 Gio (10 s, pic de 2 Gio, mesuré) ; un cycle placé derrière un graphe partagé n'était vu par le
sérialiseur qu'après le développement du graphe (2^20 feuilles : 3,8 s, mesuré). La borne porte sur une borne basse des
octets, comptée une fois par occurrence, et un cycle est refusé avant le sérialiseur (FORMAT §8.4). En-tête : convention
du compte de R-25.

Rouge : sur la base, 2 tests en échec d'assertion (FAIL 2, ERROR 0) : sérialiseur appelé (espion qui lève).

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/collecte/journal.py` | 452 | — |
| `tests/test_journal.py` | 356 | 17 (2 de plus) |

Mutants (commande exacte du job s2bis-unittest : runner, puis ligne de `gates.yml` ; borne de 300 s ; python3.12 ;
réseau isolé ; témoin VIVANT) : 12 mutants, 12 tués par leur test visé, 0 vivant, 0 FATAL : cycle laissé au
sérialiseur, chaîne comptée 1, entier compté 1, chiffres surestimés (4/10), clés non comptées, virgules non comptées,
saut de ligne non compté, signe non compté, null et booléens comptés 5, nombre à virgule compté 24, borne retirée,
conteneur partagé compté une fois.

Suite : 344 tests ; plancher du job : 344, égalité exigée (`--egal`).

## DT6-b (2026-10-09) : borne d'exposant de `decodeurs._entier` figée, docstring exacte (lot DETTES-T6)

Objet : SHOGEN-S2BIS-DECODEURS-BORNE-TEST-1 (O-A1 et O-A2 du contre-contrôle de P2A). La borne d'exposant de `_entier`
(16) n'était figée par aucun test au-dessous de 10^6 : le mutant K1-03 (borne à 200 000) vivait, alors que
`int(Decimal("1E+199999"))` coûte 0,51 s. Test de la borne exacte (9E+15 et 9,999999999999999E+15 convertis ;
1E+16, 1E+17, 10000000000000000 et 0E+16 refusés avant int(), espion qui lève) et des nombres JSON 1E+199999 et
1E+200000 à chaque champ d'instant (`panne_decode` en moins de 0,1 s) ; docstring rendue exacte (0E+16, l'instant 0,
est refusé). Code inchangé.

Rouge : sur la base, le test passe (code juste) ; sur le mutant K1-03, 5 échecs d'assertion (FAIL 5, ERROR 0 : quatre
refus attendus avant int(), puis 1E+199999 décodé en 0,48 s).

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/collecte/decodeurs.py` | 147 | — |
| `tests/test_decodeurs.py` | 260 | 20 (1 de plus) |

Mutants (commande exacte du job s2bis-unittest : runner, puis ligne de `gates.yml` ; borne de 300 s ; python3.12 ;
réseau isolé ; témoin VIVANT) : 9 mutants, 9 tués par le test visé, 0 vivant, 0 FATAL : K1-03 (200 000), borne à
200 001, à 100 000, à 17 et à 15, comparaison stricte, branche Decimal retirée, zéro admis à tout exposant, exposant
brut au lieu de l'exposant ajusté.

Suite : 345 tests ; plancher du job : 345, égalité exigée (`--egal`).

## DT6-c (2026-10-09) : fichiers du journal ordinaires, lus sans attente (lot DETTES-T6)

Objet : SHOGEN-S2BIS-JOURNAL-FICHIER-SPECIAL-1 (O-4 de la G2 de P2B). Un tube nommé au nom d'un fichier du journal
bloquait `status` (ouverture sans `O_NONBLOCK`) et la reprise de l'écrivain ; un dossier à ce nom faisait lever
`IsADirectoryError` à `status`. L'écrivain refuse de démarrer devant un nom du journal ou des sommes qui n'est pas un
fichier ordinaire (`JOURNAL/fichier`, contrôle par `stat`, avant toute lecture et toute écriture) et ouvre toute lecture
sans attente (`journal.ordinaire`, comme au dépôt) ; `status` ne lit pas un tel fichier (FORMAT §5, §7.7, §17.1).

Rouge : sur l'état DT6-b, 2 tests en échec d'assertion (FAIL 2, ERROR 0) : appels bloqués, interrompus par l'alarme de
2 s (`bloqué`), puis `JOURNAL/occupe` (verrou tenu par l'instance bloquée).

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/collecte/journal.py` | 471 | — |
| `shogen_s2bis/collecte/status.py` | 219 | — |
| `tests/test_reprise.py` | 376 | 28 (1 de plus) |
| `tests/test_status.py` | 407 | 19 (1 de plus) |

Mutants (commande exacte du job s2bis-unittest : runner, puis ligne de `gates.yml` ; borne de 300 s ; python3.12 ;
réseau isolé ; témoin VIVANT) : 10 mutants, 10 tués par leur test visé, 0 vivant, 0 FATAL : lecture ouverte en attente,
type du fichier lu non contrôlé, contrôle d'ouverture retiré, sommes hors du contrôle, tube seul refusé (contrôle
d'ouverture ; lecture), refus de l'écrivain non rattrapé par `status`, ouverture de `status` d'avant DT6-c, relecture
de la reprise et sommes relues par `open` (tués par le cas du tube posé après le contrôle).

Suite : 347 tests ; plancher du job : 347, égalité exigée (`--egal`).

## DT6-d (2026-10-09) : `status`, fichiers arrêtés nommés, étendue de la grille bornée (lot DETTES-T6)

Objet : SHOGEN-S2BIS-STATUS-QUEUES-1 (O-3 de la G2 de P2B ; résiduel de C-3 ; R-B1 du contre-contrôle ; I-3 du
générateur). Un fichier arrêté avant sa fin l'était sans le dire : il est nommé en dernière ligne du rapport local, avec
son motif. Un saut d'horloge en avant, sans fichier forgé (l'écrivain nomme le fichier par le jour de `ws`), étendait la
grille jusqu'à MemoryError (trace Python, 3,6 s sous 512 Mio, mesuré) : la grille compte au plus 46 080 fenêtres
(32 jours), au-delà le refus nommé `STATUS/grille` (0,15 s). Un `disque` partiel faisait lever KeyError (FORMAT §17.1,
§17.3, §17.4).

Rouge : sur l'état DT6-c, 4 tests en échec d'assertion (FAIL 4, ERROR 0) : ligne des arrêts absente, grille de 46 081
fenêtres admise, `KeyError` rendu par le rapport, trace Python au lieu du refus nommé.

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/collecte/status.py` | 242 | — |
| `tests/test_status.py` | 473 | 23 (4 de plus) |

Mutants (commande exacte du job s2bis-unittest : runner, puis ligne de `gates.yml` ; borne de 300 s ; python3.12 ;
réseau isolé ; témoin VIVANT) : 11 mutants, 11 tués par leur test visé, 0 vivant, 0 FATAL : borne relâchée et serrée
d'une fenêtre, comparaison large, borne retirée, ligne illisible non notée, motifs confondus, ligne coupée non notée,
fichier spécial noté illisible, ligne des arrêts omise, disque partiel lu, arrêts non transmis.

Suite : 351 tests ; plancher du job : 351, égalité exigée (`--egal`).

## DT6-e (2026-10-09) : D-3 jugé sur la sortie de `chronyc -n tracking`, forme lue sur pièce (lot DETTES-T6)

Objet : SHOGEN-S2BIS-CHRONYC-FORMAT-1 (I-B1 et O-3 de la G2 de P1-B ; Q-9 de la G2 de P2B). La forme de la sortie de
`chronyc tracking` est lue dans la source de chrony 4.6.1 (`client.c`, `doc/chronyc.adoc` ; inchangée en 4.9) et écrite
au FORMAT §13.3 ; `status` juge D-3 (§17.2) : relevé lisible (code 0 ; System time, Root delay, Root dispersion et Leap
status une fois chacune ; neuf décimales), borne |System time| + Root dispersion + Root delay / 2 de plus de 1 s,
statut autre que Normal, Insert second ou Delete second, ou aucun relevé lisible d'une fenêtre commencée moins de 120 s
avant (âge compté en fenêtres du journal, Q-1 du lot). La sonde garde la sortie d'erreur, à la suite de la sortie
standard, dans la borne de 4 096 caractères (O-3). Une `sante` sans `ws` et un `code` non entier (booléen compris),
hors FORMAT, ne font jamais lever ni lire un relevé (I-3 ; défaut de la première écriture, vu en relecture du
générateur). Fixture `tests/fixtures/chrony/tracking.txt` : l'exemple de la documentation (l.147-159), copié octet pour
octet ; 13 lignes, hors compte de R-25.

Rouge : sur les tests de DT6-e et le code de l'état DT6-d (`status.py`, `sante.py`), 10 tests en échec d'assertion
(FAIL 10, ERROR 0) : D-3 non jugé (grille, rapport, résumés, quorum, arrêts), `juger` rendant un couple, seuils D-3
absents, sortie d'erreur jetée. Correctif de relecture : sur le code d'avant lui, 2 tests en échec d'assertion
(FAIL 2, ERROR 0 : `code` faux lu comme 0, `KeyError` sur une `sante` sans `ws`).

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/collecte/sante.py` | 111 | — |
| `shogen_s2bis/collecte/status.py` | 272 | — |
| `tests/fixtures/chrony/tracking.txt` | 13 | — |
| `tests/test_sante.py` | 285 | 14 (1 de plus) |
| `tests/test_status.py` | 517 | 24 (1 de plus) |

Mutants (commande exacte du job s2bis-unittest : runner, puis ligne de `gates.yml` ; borne de 300 s ; python3.12 ;
réseau isolé ; témoin VIVANT) : 17 mutants, 17 tués par leur test visé, 0 vivant, 0 FATAL : âge en comparaison
stricte, âge porté à 180 s, borne en comparaison large, borne sans le facteur 2, « Not synchronised » admis,
« Invalid » admis, « Insert second » refusé, ligne en double admise, code de sortie ignoré, « fast » illisible, délai
racine compté entier, décimales libres, D-3 ajouté à une fenêtre D-1, première fenêtre sans relevé lisible jugée sans
D-3 (vivant au premier passage : cas ajouté), sortie d'erreur jetée, `code` booléen admis, `ws` lu par indexation.

Suite : 353 tests ; plancher du job : 353, égalité exigée (`--egal`).

## DT6-f (2026-10-09) : numéro d'AS en chiffres ASCII, IPv4 littérale relevée directement (lot DETTES-T6)

Objet : SHOGEN-S2BIS-ASN-LECTURE-1 (O-2 de la G2 de P2A ; Q-3 du lot) et SHOGEN-S2BIS-ASN-HOTE-IPV4-1 (O-6 ; Q-2).
`asn` de RIPEstat et premier mot du TXT de Cymru : entier, ou texte de 1 à 10 chiffres ASCII, de 0 à 2³² exclu
(souligné, signe, blancs et chiffres d'autres écritures refusés : écart à `int()` de S2, écrit au §15.4). Un hôte écrit
en IPv4 littérale canonique est relevé directement : `a` null, `ip` l'hôte, aucune requête A ; écrit autrement, c'est
un nom (§15.4). Le relevé du secondaire devient injectable (`entree.main`, `construire_secondaire`) : le test
d'isolement des deux processus le dirige vers des ports fermés de boucle locale (sans lui, les hôtes 127.0.0.1 partaient
vers RIPEstat, arrêtés par la garde réseau des tests, mesuré).

Rouge : sur les tests de DT6-f et le code de l'état DT6-e (`asn.py`, `entree.py`), 4 tests en échec d'assertion
(FAIL 4, ERROR 0) : textes signés, soulignés et non ASCII admis (RIPEstat, Cymru), IPv4 littérale jamais relevée,
relevé du secondaire non injectable (sous-processus en échec).

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/collecte/asn.py` | 85 | — |
| `shogen_s2bis/collecte/entree.py` | 269 | — |
| `tests/test_asn.py` | 150 | 6 (1 de plus) |
| `tests/test_secondaire.py` | 207 | 7 |

Mutants (commande exacte du job s2bis-unittest : runner, puis ligne de `gates.yml` ; borne de 300 s ; python3.12 ;
réseau isolé ; témoin VIVANT) : 11 mutants, 11 tués par leur test visé, 0 vivant, 0 FATAL : lecture d'avant DT6-f
(`int()` de S2), chiffres de toute écriture (`isdigit`), signe admis, blancs admis, souligné admis, texte vide lu 0,
littérale toujours fausse (forme d'avant DT6-f), littérale reconnue à un motif (zéros de tête admis), requête A gardée
pour une littérale, relevé injecté ignoré par `construire_secondaire`, puis par `main`.

Suite : 354 tests ; plancher du job : 354, égalité exigée (`--egal`).

## DT6-g (2026-10-09) : journal du secondaire contrôlé de bout en bout contre le FORMAT (lot DETTES-T6)

Objet : SHOGEN-S2BIS-SECONDAIRE-CONFORMITE-1 (O-5 de la G2 de P2A ; E-C-24). Test seul : le processus secondaire entier
en sous-processus (w = 1 s, cinq fenêtres), son relevé ASN dirigé vers des serveurs factices de boucle locale
(résolveur, RIPEstat en clair) ; chaque enregistrement est contrôlé contre le FORMAT par `anomalies` de
`test_bout_en_bout` (§1 à §14 ; `sante` sans sondes, §13.1 ; lectures de la carte aux instants du §15.3), puis contre le
§15 par des règles écrites dans le test (préfixe et fichiers, `run_params` à `{formes, carte, descripteur}`,
`releve_asn` des hôtes du pool et de la carte dans l'ordre, un `asn` par hôte en tête de fenêtre, champs d'un hôte
nommé et d'une IPv4 littérale). `anomalies` reçoit les champs par type, `servir` ses routes. Code inchangé.

Rouge : sur l'état DT6-f, le mutant G05 (`run_params` du secondaire sans le sha256 de la carte) vit (aucun test ne le
voit) ; sur les tests de DT6-g, `Conformite` échoue (FAIL 1, ERROR 0 : `seq 1 run_params : run_params`).

| fichier | lignes | tests |
|---|---|---|
| `tests/test_bout_en_bout.py` | 226 | 1 |
| `tests/test_secondaire.py` | 253 | 8 (1 de plus) |

Mutants (commande exacte du job s2bis-unittest : runner, puis ligne de `gates.yml` ; borne de 300 s ; python3.12 ;
réseau isolé ; témoin VIVANT) : 10 mutants, 10 tués, 0 vivant, 0 FATAL, dont 9 par `Conformite` (G05 par elle seule) :
`a` gardé null pour un hôte nommé, `ip` à la deuxième adresse A, `asn` écrits après la fenêtre (tué par un test du
relevé seul), hôtes du pool non relevés, `run_params` sans le sha256 de la carte, santé sans sondes à `disque` {},
`asn` de Cymru non relevé, journal au préfixe `carte`, `releve_asn` sans `lance`, hôtes non triés.

Suite : 355 tests ; plancher du job : 355, égalité exigée (`--egal`).

## DT6-h (2026-10-09) : `run_params` trop grand, refus de configuration avant l'ouverture du journal (lot DETTES-T6)

Objet : SHOGEN-S2BIS-ECRIVAIN-REFUS-ARRET-1, volet restant (sondes DNS de P1 : C-1 ; décodeurs : CB-6c). `run_params`,
seul enregistrement écrit d'une configuration, pouvait atteindre un refus de l'écrivain : admis au premier démarrage
(`seq` et `ws` courts), refusé plus tard, chaque relance écrivant une `reprise`. Sa taille est contrôlée avant
l'ouverture du journal, `seq` et `ws` écrits sur 19 chiffres : au-delà de LIMITE, refus `CONFIG/taille` (sortie 2,
rien d'écrit) ; un refus de l'écrivain sur ses valeurs devient un refus de configuration (FORMAT §14.4).

Rouge : sur les tests de DT6-h et le code de l'état DT6-g (`entree.py`), 1 test en échec d'assertion (FAIL 1, ERROR 0) :
ligne de LIMITE + 1 octets admise au premier démarrage (sortie 0, journal écrit).

| fichier | lignes | tests |
|---|---|---|
| `shogen_s2bis/collecte/entree.py` | 285 | — |
| `tests/test_entree.py` | 300 | 11 (1 de plus) |

Mutants (commande exacte du job s2bis-unittest : runner, puis ligne de `gates.yml` ; borne de 300 s ; python3.12 ;
réseau isolé ; témoin VIVANT) : 9 mutants, 9 tués par leur test visé, 0 vivant, 0 FATAL : contrôle retiré, borne
doublée, comparaison large, `seq` et `ws` courts (0), `ws` court seul, refus de l'écrivain propagé sans conversion,
contrôle après l'ouverture du journal (forme d'avant DT6-h), version de Python omise du calcul, contenus omis du
calcul.

Suite : 356 tests ; plancher du job : 356, égalité exigée (`--egal`).

## DT6-i (2026-10-09) : phrases normatives des §16 et §17 figées par `test_format` (lot DETTES-T6)

Objet : SHOGEN-S2BIS-FORMAT-P2B-TESTS-1 (O-B1 du contre-contrôle de P2B). Tests seuls : 23 phrases normatives du §16
(dont celle du dépôt local de C-7) et 23 du §17, prises au texte, et les bornes du texte égales à celles du code
(`tetes` : 1 024 octets, 16 têtes, 65 536 octets ; `status` : 46 080 fenêtres, 131 072 octets).

Rouge : le mutant K-C7-2 du contre-contrôle de P2B (« local » retiré de la phrase du dépôt, vivant à ce contre-contrôle)
fait échouer `test_paragraphe_16_tetes_depot_et_jeton` (FAIL 1, ERROR 0) ; la grille écrite 46 081 fenêtres,
`test_paragraphe_17_status_et_resumes` (FAIL 1, ERROR 0).

| fichier | lignes | tests |
|---|---|---|
| `tests/test_format.py` | 280 | 16 (2 de plus) |

Mutants (commande exacte du job s2bis-unittest : runner, puis ligne de `gates.yml` ; borne de 300 s ; python3.12 ;
réseau isolé ; témoin VIVANT) : 12 mutants, 12 tués par leur test visé, 0 vivant, 0 FATAL : K-C7-2 (« local » retiré
du §16), taille d'une tête écrite 2 048, `TAILLE` de `tetes` à 2 048, refus de liaison renommé, `NOMBRE` de têtes à 32,
grille écrite 46 081 fenêtres, `GRILLE` de 64 jours, taille d'un résumé écrite 65 536, arrêts nommés retirés du §17,
quorum écrit à 3, `PLAFOND` de réponse à 2^17, nonce écrit sur 32 bits.

Suite : 358 tests ; plancher du job : 358, égalité exigée (`--egal`).
