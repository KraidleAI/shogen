# Contre-contrôle de SB-13 (CONFORME) (transcrit)

> Transcription par l'orchestrateur le 2026-10-09 00:44:06 UTC du texte rendu par l'agent af7600974a0caa502 (g2/cc/RAPPORT-CC.md) ; contrôle FM-1.1 de son transcript : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte de l'agent ci-dessous, sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Contre-contrôle des corrections de SB-13 (après la G2), première passe

**Gate 0** : modèle `claude-opus-5-5` (identifiant exact de l'environnement), contre-contrôleur neuf (shogen-worker,
effort max). Je n'ai écrit ni les diffs de SB-13 ni leurs corrections. Travail du 2026-10-08 23:47:15 au 2026-10-09
00:26 UTC (`date -u`). Mes écritures sont limitées à `sb13/g2/cc/`, avec un TMPDIR dédié (`cc/moi/tmp`, vide à la fin)
et `NOTES.md` tenu.

Interdits respectés :
- aucune écriture git dans `/home/user/shogen` (commandes en `--no-optional-locks`, lecture seule ; `status --porcelain`
  vide, HEAD ebd1560 avant et après) ;
- `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée (absente de l'environnement, `env -u` partout) ;
- aucun `*.jsonl`, aucune pièce de D.2, aucun dossier interdit (copie `git archive` avec les exclusions) ;
- aucune recherche récursive sur `docs/`, le dépôt ou le scratchpad entier ; rien sur Pocket ;
- un seul processus lourd à la fois (chaîne séquentielle, puis xtask).

Un contre-contrôleur précédent avait été interrompu. J'ai lu ses notes et ses journaux comme données seulement, et j'ai
tout refait dans `cc/moi/`. Mes résultats concordent avec les siens.

## Verdict : CONFORME

Les six corrections C-1 à C-6 de l'adjudication tiennent sur la série de `diffs-apres-sb15/` appliquée à ebd1560.
Chacun des quatre mutants visés (M-G2-01, 02, 12, 13) est tué par le test nommé, en FAIL d'assertion sans ERROR. Les
17 mutants du réviseur sont tous tués (0 FATAL). Il n'y a aucune régression :
- planchers exacts 194, 199, 204, 207, 210 ;
- runner 136 ;
- s2bis 255 ;
- S2 415 ;
- hooks 54, model-pinning 227, secrets 147 ;
- strict 10/10 ;
- lignes de verdict de xtask identiques à la base.

Aucun CC-n. Trois observations non bloquantes, à reprendre à la seconde passe : O-CC-1, O-CC-2, O-CC-3.

## 1. Intégrité et application

- `SHA256SUMS` du correcteur (b1bd5d91…) : 662 lignes, `sha256sum -c` sortie 0. Il couvre exactement les fichiers de
  `sb13/` hors lui-même et hors `g2/` (os.walk : 0 fichier non listé, 0 listé absent). `g2/SHA256SUMS` du réviseur :
  `-c` sortie 0.
- Pièces lues : `BRIEF-SB13.md` f5624158…, `ADJUDICATION-G2.md` 797bdaab…, `g2/RAPPORT-G2.md` 64e2630c…,
  `RAPPORT-GENERATEUR.md` dcba1ff3… (§13 lu en entier, §9 lu).
- Empreintes des diffs égales au §13.2 : SB-13A a1993dfc…, SB-13B f54486cc…, SB-13C a63ae232…, SB-13D 9a62d87a….
  Code ajouté (`git apply --numstat`, hors `.md`) : 162, 132, 188, 115, donc chaque diff est sous 200 lignes. Aucun octet
  92, aucun TODO/FIXME, imports de la bibliothèque standard seuls. Deux lignes ajoutées dépassent 120 caractères : la
  `source` de `parametres.json` (E-7) et la ligne de README (E-12).
- Base : `git rev-parse` donne ebd156071794… pour la branche claude/compassionate-noether-szmdyj, qui est aussi HEAD.
  `git archive` avec les exclusions du brief donne 1 072 membres, dont 0 sous un chemin exclu. Les quatre diffs passent
  `git apply --check` puis s'appliquent dans l'ordre (sortie 0). `scripts/sim-bis` et `gates.yml` de mes étapes e0 à e4
  sont égaux à `etapes/e0`, `e13a` à `e13d` du correcteur (`diff -r` vide). Entre c58b997 et ebd1560, `git diff
  --quiet` sur `scripts .github s2bis s2-harness enforcement` donne 0 (E-9).

## 2. Tableau des corrections (lignes dans ebd1560 + série)

| C | tient ? | fichier:ligne (lu) | test | mutant visé | preuve |
|---|---|---|---|---|---|
| C-1 | oui | `tests/test_oracle_recalc.py:309-313` (g.h en ETH seule, o(7, g.h) altéré, attendu `[("o", 7, "g.h")]`) | `test_croiser_voit_les_ecarts` | M-G2-01 | TUÉ, FAIL 1 / ERROR 0 ; neufs M-CC-11 (classe ETH ignorée), M-CC-12 (dernière unité hors BTC ignorée) TUÉS ; voir O-CC-2 |
| C-2 | oui | `:257-259` (6ᵉ vecteur, n′ = 54 720, n_s = 109 440, 0 écart) ; `:226` (i % 6 = 5) ; `:283` (16) | `test_vecteurs_e_s_51`, `test_series_synthetiques_e_s_51` | M-G2-02 | TUÉ, FAIL 2 / ERROR 0 ; neuf M-CC-14 (n_s vers RB-6 si n < n_s ≤ 2n) TUÉ ; recompte hors code : 16 séries à n_s > n, toutes ≤ 2n |
| C-3 | oui | `scripts/sim-bis/README.md:27` (799 caractères, forme des 16 lignes de la table) | texte | sans objet | lu ; chaque module de tête (12) a exactement une ligne |
| C-4 | oui | `:191`, `:209-210`, `:219`, `:281-283` | `test_series_synthetiques_e_s_51` | M-G2-13 | TUÉ, FAIL 2 / ERROR 0, désormais aussi par le test des séries ; neufs M-CC-15 (terme p0∧p3), M-CC-16 (p1∧p3) TUÉS ; recompte hors code : 40 classes de dix, 22 à m_t ≥ 8 ; durée du test mesurée 2,60, 2,51 et 2,52 s (charge 1,1), contre 2,0 s chez le correcteur ; voir O-CC-3 |
| C-5 | oui | `.github/workflows/gates.yml:231-232` | commentaire | sans objet | lu : nomme SB-13, f458980, « seconde raison de fetch-depth: 0 » |
| C-6 | oui | `:164-178` (processus neuf, `builtins.open` relevé pendant `charger`) | `test_analyse_lu_dans_l_extraction` | M-G2-12 | TUÉ, FAIL 1 / ERROR 0 ; neufs M-CC-17 (arbre de travail lu par `io.open`), M-CC-18 (écriture par `io.open`) TUÉS ; voir O-CC-1 |

## 3. Mutants (commande du job sim-bis, borne 300 s, un à la fois, e4 = ebd1560 + série)

`cc/moi/outils/campagne.py` lit les 17 mutants du réviseur dans `g2/outils/campagne_g2.py` (364ac436…, égale à
`g2/SHA256SUMS`). La lecture passe par `ast` et ne garde que les affectations `NL`, `O/R/P/C` et `MUTANTS` ; rien
d'autre n'est exécuté. Ces 17 mutants sont égaux, clé par clé, à ceux du contre-contrôleur précédent. La campagne a
tourné de 23:56:02 à 00:14:55 UTC (lignes DEBUT et FIN présentes). Les 28 runs donnent tous runner 0 et TMPDIR vide
après le run. Le témoin est VIVANT (sortie 0, Ran 210).

| mutant | sortie | classement | tests rouges |
|---|---|---|---|
| M-G2-01 | 1 | TUÉ | test_croiser_voit_les_ecarts |
| M-G2-02 | 1 | TUÉ | test_series_synthetiques_e_s_51, test_vecteurs_e_s_51 |
| M-G2-03 | 1 | TUÉ | test_epingles |
| M-G2-04 | 1 | TUÉ | test_premiere_avant_absorption_q_t3_15, test_series_synthetiques_e_s_51, test_tester_rotation_r_1 |
| M-G2-05 | 1 | TUÉ | test_croiser_voit_les_ecarts, test_series_synthetiques_e_s_51, test_vecteurs_e_s_51, … |
| M-G2-06 | 1 | TUÉ | test_croiser_voit_les_ecarts, test_series_synthetiques_e_s_51, test_vecteurs_e_s_51, … |
| M-G2-07 | 1 | TUÉ | test_noms, test_noms_d_unite_p_7 |
| M-G2-08 | 1 | TUÉ | test_seuils, test_parametres_et_seuil, … (7) |
| M-G2-09 | 1 | TUÉ | test_vecteurs_e_s_51, test_series_synthetiques_e_s_51, … (6) |
| M-G2-10 | 1 | TUÉ | test_frontiere_du_moteur |
| M-G2-11 | 1 | TUÉ | test_frontiere_du_moteur |
| M-G2-12 | 1 | TUÉ | test_analyse_lu_dans_l_extraction |
| M-G2-13 | 1 | TUÉ | test_k_et_s_t_rot_2, test_series_synthetiques_e_s_51 |
| M-G2-14 | 1 | TUÉ | test_noms, test_refus_du_contrat_rb6 |
| M-G2-15 | 1 | TUÉ | test_vecteurs, test_vecteurs_e_s_51, … (5) |
| M-G2-16 | 1 | TUÉ | test_series_synthetiques_e_s_51 |
| M-G2-17 | 1 | TUÉ | test_parametres_et_seuil, test_seuils |
| M-CC-01 (cc précédent, rejoué) | 0 | VIVANT | — (O-CC-1) |
| M-CC-02 (cc précédent, rejoué) | 0 | VIVANT | — (O-CC-2) |
| M-CC-11 | 1 | TUÉ | test_croiser_voit_les_ecarts |
| M-CC-12 | 1 | TUÉ | test_croiser_voit_les_ecarts |
| M-CC-13 (n_s ignoré par la réplique) | 0 | VIVANT, équivalent | — |
| M-CC-14 | 1 | TUÉ | test_series_synthetiques_e_s_51, test_vecteurs_e_s_51 |
| M-CC-15 | 1 | TUÉ | test_k_et_s_t_rot_2, test_series_synthetiques_e_s_51 |
| M-CC-16 | 1 | TUÉ | test_k_et_s_t_rot_2, test_series_synthetiques_e_s_51 |
| M-CC-17 | 1 | TUÉ | test_analyse_lu_dans_l_extraction |
| M-CC-18 | 1 | TUÉ | test_analyse_lu_dans_l_extraction |

Bilan : 17 sur 17 mutants du réviseur tués et 0 FATAL. Parmi mes 8 mutants neufs, 7 sont tués et 1 est équivalent.
M-CC-13 est équivalent pour `croiser` : dans `regle._entrees` (l.207), n_s n'entre que dans `suffisant = 2n ≥ n_s`,
argument de `_valeur`. Aucune des clés `CLES` comparées n'en dépend, et RB-6 ne reçoit pas n_s.

## 4. Absence de régression

- **Jobs par étape** (runner, puis ligne lue dans le `gates.yml` de l'étape, sur ebd1560) : tous en sortie 0 et
  « conforme » sous `--egal`, sans `__pycache__` laissé.

  | étape | plancher | Ran |
  |---|---|---|
  | e0 | 194 | 194 |
  | SB-13A | 199 | 199 |
  | SB-13B | 204 | 204 |
  | SB-13C | 207 | 207 |
  | SB-13D | 210 | 210 |

  Le runner donne « 136 ok, 0 échec » à chaque étape.
- **Mode strict** (e4, `scripts/sim-bis`, `-X dev -W error -B`) :
  - 3.10.20, 3.11.15, 3.12.3 et 3.13.14, avec PYTHONHASHSEED 0 et 5 : 8 runs sur 8 en sortie 0, Ran 210 OK,
    0 « Exception ignored », 0 « Warning » ;
  - plus serré (PYTHONDEVMODE=1 et PYTHONWARNINGS=error hérités) sous 3.11 et 3.13 : 2 sur 2 verts.
  - 3.10 passe.
- **Portes** (e4 ; copie sans `.git` pour s2bis et S2) :
  - sous `unshare -n` (interfaces vues : lo seule) : sim-bis Ran 210 conforme ; s2bis Ran 255 conforme ; S2 Ran 415
    conforme, sauts qui nomment la variable ;
  - hooks 54 ok, model-pinning 227 ok, secrets 147 ok.
- **xtask** (`cargo --locked xtask verify`, `unshare -n`, hors ligne, copies sans `.git`) : 13 lignes de verdict.
  Elles sont identiques entre la série et la base, et identiques à celles du correcteur
  (`journal/xtask-verdicts-tete-serie.txt`) : S-G1 à S-G8 VERT, S-G9 ROUGE (1 violation, déjà sur la base),
  `cargo fmt --check` VERT, no_std VERT, clippy VERT ; global ROUGE comme la base.

## 5. Observations (non bloquantes ; aucune ne touche la liste fermée C-1 à C-6)

- **O-CC-1 (C-6).** Le test observe le chemin et le mode des ouvertures par `builtins.open`, pas le contenu lu. M-CC-01
  survit : il fait une ouverture factice du fichier extrait, puis lit l'arbre de travail par
  `pathlib.Path.read_bytes`, qui passe par `io.open` et échappe à l'espion. Ce mutant est construit pour tromper le
  test. Une régression ordinaire (lecture de l'arbre de travail par `open` ou par `io.open`, sans lecture factice) est
  tuée : M-G2-12, M-13B-13, M-13B-14, M-CC-17. Remède proposé pour la seconde passe (SHOGEN-SIM-BIS-ORACLE-RB7-1) :
  dans le processus neuf, envelopper `extraire` pour réécrire `config/analyse.json` extrait avec une sentinelle, et
  exiger `charger(...)["analyse"]` égal à la sentinelle (environ 5 lignes).
- **O-CC-2 (C-1).** Le cas ajouté n'a que deux classes (BTC, ETH). M-CC-02 survit : il ne prend que les unités des deux
  premières classes. « Toute unité de toutes les classes » (docstring de `croiser`, README l.27) n'est donc montré que
  pour deux classes sur quatre. Remède proposé : mettre aussi une unité décalée seule en USDT, avec un o altéré.
- **O-CC-3 (C-4).** Sur les masques non tournés, les classes de dix ne donnent que m_t = 10 (688 positions, séries
  liées) et m_t = 8 (2), jamais 9. M-CC-15, qui porte sur le terme p0∧p3 et demande m = 9, est tout de même tué par le
  test des séries : les rotations font apparaître m_t^(r) = 9. Aucune action exigée. Le compte 22 du test (L-4 du
  correcteur) est désormais recompté hors du code.

## 6. Avis sur les écarts E-8 à E-13 du correcteur

- **E-8** (premier rouge de C-6 en ERROR, arbre léger sans `s2bis/`) : accepté. Sur l'arbre complet, M-G2-12 donne
  FAIL 1, ERROR 0.
- **E-9** (tête avancée de c58b997 à ebd1560, documents seuls) : accepté, recompté (`diff --quiet` = 0 sur les cinq
  racines de code). La série s'applique sans reste sur ebd1560 et y donne les planchers exacts. Base à citer :
  ebd1560 ; le choix relève de l'orchestrateur.
- **E-10** (C-3 et C-5 sont du texte, sans mutant possible) : accepté. Aucun test de `scripts/sim-bis` ne lit le README
  ni ce commentaire. Les deux sont contrôlés par lecture (README l.27, `gates.yml` l.231-232).
- **E-11** (octets 92 de `tete.sh` retirés) : accepté. Les outils du correcteur ont 0 octet 92, sauf `rouges_jobs.sh`
  (2), déjà déclaré en E-4 de la première passe. Le rapport et NOTES.md en ont 0.
- **E-12** (ligne de README de 799 caractères) : accepté. Recompté en caractères : 799. Les 16 lignes de la table
  dépassent toutes 120.
- **E-13** (SHA256SUMS recalculé par Python) : accepté. `-c` donne 0 et la couverture est exacte. Défaut de forme
  seulement : E-13 est placé avant E-12 dans le §13.6.

## 7. Avis sur l'item proposé SHOGEN-SIM-BIS-README-MODULES-1

À former, à faible priorité, rattaché à SIM-BIS. Cet item est un test qui exige une ligne de la table du README par
module de tête de `scripts/sim-bis`. Il aurait évité C-3 et coûte peu. Mesure : à ebd1560 + série, les 12 modules de
tête (`*.py`, `parametres.json`) ont chacun exactement une ligne. Les fichiers de `tests/` sont couverts par la ligne
`tests/` et par deux lignes nommées. Le test ne demande donc aucune reprise du README. Il sort du périmètre du brief
de SB-13, et ne bloque pas le commit.

## 8. Écarts du contre-contrôleur

- **E-CC-1.** Une commande de lecture (lignes du README contre les modules) portait des barres obliques inverses
  tapées dans un regex Python. Sa sortie n'a servi que de signal. Le résultat a été refait par `grep -F` sans barre.
  Mes outils ont 0 octet 92 (`tr -cd` puis `wc -c`).
- **E-CC-2.** Une suppression des copies lourdes écrite avec des variables shell a été refusée par la garde de l'outil.
  Je l'ai refaite avec des chemins absolus littéraux, comme la garde le propose. Sont retirés : mes copies (base, e0 à
  e4, e4-sans-git, cible cargo de 137 Mo) et `cc/copies/` du contre-contrôleur précédent (105 Mo). Restent
  `logs/`, `outils/`, `sonde/` et les journaux du précédent.
- **E-CC-3.** PYTHONHASHSEED 0 et 5 (le correcteur avait 0 et 7). Le mode serré a été fait sous 3.11 et 3.13 (le
  réviseur l'avait fait sous 3.12 et 3.13).

## 9. Limites (règle PAROXYSME)

- L-CC-1 : tous les runs ont tourné sur l'hôte de session (Linux, 4 vCPU partagés avec d'autres lots en campagne) ; la
  CI n'a pas été lancée.
- L-CC-2 : O-CC-1 et O-CC-2 sont des items à former pour la seconde passe, rattachés à SHOGEN-SIM-BIS-ORACLE-RB7-1, qui
  reste ouvert.

## 10. Journal de provenance (G1)

- **Lu [lu]** :
  - pièces : `BRIEF-SB13.md`, `ADJUDICATION-G2.md` et `g2/RAPPORT-G2.md` en entier ; `RAPPORT-GENERATEUR.md` §9 et
    §13 ;
  - code (e4) : `oracle_recalc.py` et `tests/test_oracle_recalc.py` en entier ; `regle.py` l.81-106 et 194-243 ;
  - textes : `gates.yml` l.220-250 ; README l.1-30 ;
  - outils du réviseur : `campagne_g2.py` (par `ast`), `lo_up_g2.py`, `arbre.sh` ;
  - outils et journaux du contre-contrôleur précédent (données) ;
  - journaux du correcteur : `rouges-g2.txt`, `mutants-g2-13c.txt`, `mutants-g2-13b.txt`, `duree-c4.txt`,
    `xtask-verdicts-tete-*.txt` ;
  - dépôt : `git rev-parse`, `log --oneline`, `diff --stat` et `--quiet` (lecture seule).
- **[abs]** : ROTATION-S2BIS.md, PROPOSITION.md, G0-SIM-BIS.md (la G2 les a lus ; je ne juge que les corrections).
- **[2nd]** : aucun chiffre repris sans recompte.
- **Commandes** (sorties dans `cc/moi/logs/`) :

  | commande | résultat |
  |---|---|
  | `sha256sum -c` (sb13 et g2) | 0 et 0 |
  | `git apply --numstat`, `--check`, apply | voir §1 |
  | `diff -r` étapes | vide |
  | `sonde/recompte.py` | 16 / 40 / 22 |
  | `outils/chaine.sh` (PID 24458), journal `chaine.log` | 23:52:46 à 00:24:03, lignes DEBUT et FIN |
  | `outils/campagne.py` (PID 749), `campagne.log` | 25 TUÉ, 3 VIVANT (dont 1 équivalent), 0 FATAL |
  | `outils/xtask.sh` (PID 26093), `xtask.log` | sortie 1 sur les deux arbres, verdicts identiques |
  | durée du test des séries (3 runs) | 2,60, 2,51, 2,52 s |
- **Recomptes** :
  - 16 séries à n_s > n, 40 classes de dix, 22 à m_t ≥ 8 (chaînes binaires, hors code) ;
  - lignes ajoutées par diff ;
  - longueur de la ligne de README (799 caractères) ;
  - modules de tête du README (12 sur 12).
- **Empreintes** (préfixes) :

  | fichier | empreinte |
  |---|---|
  | `outils/campagne.py` | fc38d87c… |
  | `chaine.sh` | abad5026… |
  | `isole.sh` | 69dc719a… |
  | `xtask.sh` | b5f7e2d3… |
  | `sonde/recompte.py` | dcadab92… |
  | `chaine.log` | 60a21a96… |
  | `campagne.log` | d8ad2946… |
  | `xtask.log` | f27cd715… |

  `cc/SHA256SUMS` couvre `cc/` hors lui-même.
