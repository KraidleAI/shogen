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
