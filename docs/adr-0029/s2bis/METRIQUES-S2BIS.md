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
| frontière d'imports | `test_fitness.Fitness.test_frontiere_du_paquet`, `test_frontiere_refuse` | import hors bibliothèque standard et hors sous-paquet, import relatif sortant, import dynamique, sous-paquet sans règle |
| absence de réseau | `test_garde.Garde` (garde posée par `tests/__init__.py`) | connexion, envoi, résolution hors boucle locale, même sous un attrape-tout |
| déterminisme | `test_fitness.Fitness.test_memes_octets_sous_cinq_graines` | sortie qui dépend de la graine de hachage (`PYTHONHASHSEED` de 0 à 4) |
| compilation | `test_fitness.Fitness.test_compilation_avertissements_en_erreur` | avertissement de compilation (séquence d'échappement invalide, par exemple) |

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
