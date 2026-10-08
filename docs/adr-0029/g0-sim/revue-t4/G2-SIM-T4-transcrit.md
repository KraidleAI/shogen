# Relecture G2 neuve — SIM-BIS tranche 4 (transcrit)

> Transcription par l'orchestrateur le 2026-10-05 13:58:54 UTC du rapport rendu par message par le réviseur G2 (agent a16dbe18b742b1838) ; contrôle FM-1.1 : fragments_l51_l14 = 0. Texte du réviseur ci-dessous, sans retouche.

claude-opus-5-5

# Relecture G2 neuve : SIM-BIS, tranche 4 (SB-9A à SB-14B : variante, estimateur FIV, adaptateur r1)

- **Gate 0** : je tourne sous `claude-opus-5-5`, effort max. Je n'ai rien généré de ce lot.
- **Horloge** (`date -u`, 2026-10-05) : de 13:11:47 à 13:57:10 UTC.
- **Dépôt** : tête `5f99ab5` au début et à la fin, `git status --short` vide. Aucune opération git en écriture dans `/home/user/shogen` (lecture par `git --no-optional-locks`).
- **Preuves** : `…/sim4/g2/outils/` et `…/sim4/g2/sorties/`, empreintes dans `…/sim4/g2/SHA256SUMS-REVISEUR` (87 entrées, sha256 `46289ca0…25fa`, 87 sur 87 OK). Notes de reprise dans `…/sim4/g2/NOTES.md`.
- **Indépendance** : je n'ai pas ouvert `AVIS-SIM-T4.md`, l'avis de l'advisor rendu en parallèle.
- **Nettoyage** : copies, cible cargo et TMPDIR supprimés ; 9,3 Go libres à la fin.

## Verdict : ACCEPTE-AVEC-CORRECTIONS (C-1 à C-5, liste fermée)

## Résumé

- **Série** : les sept diffs s'appliquent sur `5f99ab5`. Chacun ajoute au plus 182 lignes de code. Chaque état est vert seul, à son plancher exact, par la commande du job (129, 134, 140, 147, 153, 156, 160, 162). `fetch-depth: 0` est sain et n'affaiblit aucune gate.
- **Code** : il est juste. Mes oracles indépendants ne trouvent aucun écart :
  - variante : 1 100 instances ;
  - FIV : 28 356 valeurs, mon estimateur contre `calib_fiv` et contre r1 de f35a70c ;
  - E-S-39 rejoué : 2 448 valeurs.
- **Recomptes** : le calendrier J28 est exact (30 286 et 13 491). M-VAR-1b est bien équivalent : preuve vérifiée et contrôle exhaustif. L'extraction de f35a70c est épinglée et échoue fermée.
- **Identité** : 6998101d… est reproduite 16 fois sur 16. Les quatre empreintes antérieures sont inchangées. Mode strict : 8 sur 8.
- **Constat du point 9 confirmé** : la famille E1 culmine vers FIV(240) ≈ 1,4 à 2,1, contre 22,9 et 34,6 pour EP.
- **Défauts** : des trous de tests (la composition d'E1 n'est épinglée par aucun test, et une règle d'égalité du G0 n'est pas testée), une lacune de provenance sur les mesures de mise au point, et une erreur de chiffre dans le rapport.

## Contrôles

**1. Série**
- **Application** : copie `git archive 5f99ab5` avec les sept exclusions. `git apply --check` puis `git apply`, dans l'ordre, sans échec.
  - Les sha256 des diffs sont égaux à `sim4/SHA256SUMS` (fichier `f6c05f94…`, 311 sur 311 OK).
  - Chaque état est égal à l'étape du worker, sur `scripts/sim-bis` et `gates.yml` (`compare_etapes.txt`).
- **Tailles**, recomptées par mon script (code ajouté / retiré) : +126/−2, +121/−3, +151/−1, +169/−2, +167/−5, +182/−17, +66/−5. Total +982/−35, README +10/−7. Ligne Python ajoutée la plus longue : 120 caractères. Le lot passe de 4 018 à 4 962 lignes.
- **Job** : runner d'abord (33 ok à chaque état), puis la ligne lue dans le `gates.yml` de l'état. Sous `isole.sh`, borne de 300 s. Sortie 0 huit fois, Ran égal au plancher (`etapes.txt`).
- **`fetch-depth: 0`**, sain :
  - f35a70c est un ancêtre de `5f99ab5` (209 commits plus tôt) et se trouve sur les branches distantes ; c'est le même réglage que `g3-secrets`.
  - `persist-credentials: false`, `--aucun-saut --egal` et l'étape du runner sont gardés.
  - Diff net de `gates.yml` entre e0 et e14b : un commentaire, `fetch-depth: 0` et le plancher 129 → 162. `enforcement/` est identique.
  - Échec fermé vérifié : sur une copie sans `.git`, et dans un dépôt git sans f35a70c, le job sort en 1 : `ORACLE/extraction` (git archive sort en 128), Ran 158 au lieu de 162 (`echec_ferme.txt`).
  - Limite : le cas K-03 ne lit pas `with:`. Mon mutant R-17 (ligne retirée) reste donc vivant en local (O-2).

**2. Conformité, exigence par exigence**

| exigence | constat |
|---|---|
| E-S-33 | Conforme : segment [N, n − N) ; décalages SHA-256 « minus » mod 2N + 1 moins N, big-endian ; première unité non décalée ; aucun enroulement ; K_H pour r = 0 et chaque r ; même R, même seuil, même garde sur le segment ; n′ sur la suite ; N = ⌊n/4⌋, sensibilité ⌊n/8⌋. Q-T4-1 à Q-T4-4 sont fidèles. |
| E-S-38 | Conforme à la lettre : grille, critère aux ℓ gardés d'EP, C2, C1 en log à ℓ = 240, égalités κ puis τ_D (puis φ, Q-T4-9), 200 réplications, f = 1, calendrier J28. La composition du fond d'E1 est codée en dur et n'est épinglée par aucun test : C-1. Le niveau τ_D de l'égalité n'est pas testé : C-2. |
| E-S-39 | Conforme. Taux sous C0 : `test_taux_c0_e_s_39` ; histogramme : `test_sources` de la tranche 2. FIV égal à r1 extrait sur 10 réplications ; mon rejeu sur 12 réplications donne 0 écart. |
| E-S-01, E-S-14 (T-CAL-2) | Conformes. L'adaptateur n'est pas importé par le moteur. `window` est désormais extrait de f35a70c : WINDOW-EPINGLE-1 est fermable. |
| E-S-02, 03, 06, 41 à 44, 53 à 55 | Tenues. Réserves : E-S-03 pour le fond d'E1 (C-1) ; marquage de Q-T4-12 (C-5) ; seuil mesuré de `test_regime_groupe` (O-5). |

**3. Justesse, par des calculs indépendants**
- **Décalages « minus »**, par `sha256sum` et `bc` seuls :
  - graine `89b463e5…` = sha256 de « SHOGEN-SB9-VECTEURS » ;
  - les douze décalages de calme (N = 3) et les deux de stress (+3, +2) sont égaux aux attendus (`vecteurs_minus.txt`).
- **K_H refaits à la main** :
  - T-VAR-1 : [1 | 3, 2, 0, 0] ;
  - REJETTE : [2 | 1, 1, 0, 1] ;
  - première unité absente : [1 | 1, 1, 0, 1] ;
  - suite courte et n′ ;
  - série hors segment : [0 | 1, 1, 0, 0].
- **Défaut trouvé par le worker** : confirmé. Il ne touchait que les causes, C1 et la loi, jamais la valeur, puisque le raccourci n'agissait que si unites < 2.
- **Oracle de la variante**, en listes 0/1, avec une décision recomptée : 800 + 300 instances, 0 écart. Elles couvrent 59 REJETTE et 217 arrêts anticipés.
- **M-VAR-1b** : la preuve tient. Pour t ∈ [N, n − N) et |s| ≤ N, on a t − s ∈ [0, n). Contrôle exhaustif (n = 1 à 12, tout N ≤ n/2, tout x, |s| ≤ N) : 334 050 cas, 0 différence. Hors domaine, 612 844 différences, mais `decalage` n'y produit jamais rien.
- **FIV_série**, mon estimateur en Fraction, écrit depuis la définition de r1 :
  - comparé à `calib_fiv` et à r1 (`bloc_strate` lui-même, extrait par `git show f35a70c`, cinq sha égaux aux épingles) ;
  - 1 427 séries dont 729 à lacune interne, 28 356 valeurs, 0 écart.
- **Calendrier J28**, à la main et par datetime :
  - calme 300 + 2 880 + 4 × 7 200 + 88 = 32 068 ; stress 14 400 ;
  - plage D5 : 342 + 1 440 = 1 782 en calme et 909 en stress ;
  - d'où **30 286 et 13 491, exacts**.
  - Contre EP, il manque **5 701** fenêtres en calme (le rapport dit 5 707 : C-4) et 2 094 en stress.
  - Recoupement par `n fixe` = 38 600 fenêtres distinctes du journal (`records.t_fin_n_fixe` de f35a70c) : 46 468 − 38 600 = 7 868 positions sans fenêtre dans S2, dont 73 dans D5 et 7 795 = 5 701 + 2 094 hors D5. C'est cohérent.
- **Oracle E-S-39 rejoué** :
  - 12 réplications (C0, (1/10, 50, 1 440), (1/20, 20, 240) ; cellules `E1-oracle-rev`), 2 strates, 17 ℓ, 6 champs : 2 448 valeurs, 0 écart ;
  - recalcul centré entier contre r1 : 612 valeurs, 0 écart.
- **Épinglage** : commit sur 40 hexadécimaux et cinq sha256 égaux à PLAN-S2BIS. Refus `ORACLE/sha256` (`test_refus`, M-14-01) ; refus `ORACLE/modules` (mes R-09 et R-10, tués).
- **Logarithmes** : les références `bc -l` de `test_critere` sont exactes à 60 chiffres. `Decimal.ln` est correctement arrondi sur trois cas (`bc_logs.txt`).

**4. Identité bit à bit** (Python 3.10.20, 3.11.15, 3.12.3, 3.13.14 × PYTHONHASHSEED 0, 1, 4242, aléatoire)
- Sonde T4 du worker : `6998101d…` 16 sur 16.
- Ma sonde (variante, courbes à lacunes, sélection, J28, cellules `G2T4-REV-ID-*`) : `aa35ad014083c8aa1080383a810b69d006f1299328805f29818115b5afa57ef3` 16 sur 16. C'est une empreinte neuve, déclarée.
- Empreintes antérieures, 8 sur 8 chacune sur e14b et égales sur e0 : T2 `8d97a9dc…` et `d3ba1eb6…` ; T3 `8895661a…` et `03304e5e…`.
- Mode strict `-X dev -W error` : 8 sur 8, 162 tests.

**5. Rouge, vert et mutants**
- **Rouge puis vert**, sur quatre pas :

| pas | rouge rejoué | vert |
|---|---|---|
| 9A | 5 FAIL, 0 ERROR | 5 OK |
| 10A | 7 FAIL | 7 OK |
| 10C | 3 FAIL avec les données du pas | 16 OK |
| 14B | 2 FAIL | 5 OK |

  Pour 10C, un premier essai avec les paramètres de 10B a donné 2 FAIL et 1 ERROR (`KeyError` sur `e1`).
- **Mes 20 mutants**, classés par la commande du job, borne de 300 s, témoin 0/0 : 10 tués, 10 vivants, 0 FATAL (`mutants-rev*.txt`).
  - Tués : R-01, R-09 à R-14, R-18, R-19 (T-CAL-2 mord encore contre `window` extrait), R-20.
  - Vivants : R-02, R-03, R-04, R-05, R-06, R-07, R-08, R-15, R-16 (équivalent pour la sélection) et R-17 (indétectable en local).
- **Échantillon de 29 mutants du worker**, définitions versées et rejouées par mon classeur : 28 tués, M-VAR-1b vivant, 0 FATAL. Le classement est identique au journal du worker.
- **Comptes du worker recomptés** : 92 tués, 1 vivant, 0 FATAL. Les 62 mutants cités dans les docstrings sont tous versés.

**6. CI et règles**
- Aucune gate affaiblie.
  - s2bis : 156 conforme ; s2-harness : 405 OK (skipped=2), sous `isole.sh`.
  - hooks 54, model-pinning 95, secrets 147 ; `gate-secrets --tree` dans un dépôt jetable : 26 fichiers OK.
- **R-13** : motif lu dans `gates.yml` (67 octets). 0 constat dans le lot et dans les lignes ajoutées ; le témoin positif donne 1.
- **R-8** : bibliothèque standard et lot seuls.
- **Octets 92** : 0 dans le lot (25 fichiers), les diffs, les outils, le journal, les ébauches et les brouillons du worker. Les étapes en portent 4 (`gates.yml`) + 33 (runner), venus de la base.
- **Garde `ast`** :
  - `variante` et `calib_fiv` passent les quatre gardes du moteur.
  - `oracle_r1` : libm, puissance et hasard vides ; il importe `importlib`, hors du moteur, comme le veut E-S-01.
  - L'extension est sûre : les gardes du moteur sont inchangées et couvrent les neuf modules ; la garde des adaptateurs mord (R-13, R-14, M-14-07 tués) ; aucune double collecte (Ran 162).
- **`cargo --locked xtask verify`** (unshare -n, série puis témoin e0), lignes de verdict seules :
  - S-G1 à S-G8 VERT ; fmt, no_std et clippy VERT ;
  - S-G9 ROUGE, 1 violation, une mention de `17-modele-de-menace.md:70` de chaque côté ;
  - section S-G9 identique (sha `87b165c4…`).

## Corrections demandées (liste fermée)

- **C-1 — Composition d'E1 (Q-T4-13), E-S-03 ; tue R-02 et R-03.** La composition du fond d'E1 (f = 1, longues 0, autres 1, hors-enveloppe 0, classe BTC de rang 0) est codée en dur dans `calib_fiv.replication`. Aucun test ne voit :
  - l'ajout d'un hors-enveloppe à 2,5·10⁻⁴ (R-02) ;
  - le tirage sur la classe de rang 1 (R-03).
  - Attendu : cette composition écrite dans `parametres.json`, section `e1`, avec sa source, et lue par `replication`. Un test écrit à la main l'épingle ; il est rouge sous R-02 et R-03.
- **C-2 — Trois cas écrits à la main**, chacun rouge sous son mutant et vert sur le code :
  - R-04 : égalité à κ égal, départagée par τ_D avant φ (lettre d'E-S-38) ;
  - R-06 : t0 répété d'EP l.6 différent du début du segment, `CALIB/forme` attendu ;
  - R-07 : C0 absent de `moyennes`, `E1/point` attendu (promis par la docstring ; aujourd'hui `KeyError` non nommée).
- **C-3 — Provenance (G1), E-4 et point 9.**
  - Ni les mesures de mise au point ni leurs chiffres n'ont de trace dans `journal/` ou `outils/` : FIV(240) de I_t ≈ 2,0 et 2,2, C0 1,06 et 1,04, seuil de `test_regime_groupe`.
  - Attendu : verser les scripts, les sorties brutes et les noms de cellule employés, en attestant qu'aucun n'est une cellule d'E1 (`E1-C0`, `E1-<φ>-<κ>-<τ_D>`). À défaut, déclarer ces chiffres non versés.
  - Corriger en conséquence « Tous les chiffres de ce rapport y sont recomptés ».
- **C-4 — Rapport, Q-T4-5** : « 5 707 » doit se lire **5 701** (30 286 − 24 585). Les NOTES du worker portent déjà 5 701.
- **C-5 — Q-T4-12** : marquer son numéro dans le module qui l'emploie (`oracle_r1.charger`), comme aux questions de la tranche 3. Q-T4-13 relève de C-1.

## Observations (non bloquantes ; limites rendues pour être formées)

- **O-1** : vivants mineurs.
  - R-05 : C1 peut égaler C2. C'est la lettre du G0, mais le cas n'est pas testé ; lecture à confirmer à l'adjudication.
  - R-08 : le nettoyage du dossier d'extraction (Q-T4-12) n'est pas testé.
  - R-15 : le schéma du commit n'est pas testé ; un mauvais commit échoue de toute façon fermé à l'extraction.
- **O-2** : K-03 ne contrôle pas `fetch-depth: 0`. Serrer est possible : exiger la ligne dans le job `sim-bis-unittest`, à rattacher à SHOGEN-CI-S2-CABLAGE-1.
- **O-3** : `oracle_r1.charger` met le résultat en cache par processus et ignore `prm` après le premier appel. C'est sans effet dans le lot ; à retenir pour SB-13.
- **O-4** : `variante.deux_modes` existe, mais l'oracle d'équivalence de l'arrêt anticipé de la variante (forme d'E-S-29) n'est pas câblé. Ligne pour le brief de SB-11.
- **O-5** : le seuil de `test_regime_groupe` (12,05 et « 4 × ») est mesuré sur le code, pas indépendant (E-S-53). Je l'accepte comme test de mécanisme, déclaré sous E-4.
- **O-6** : sous E1, K vaut environ 20 à 50 fenêtres en calme (n = 30 286), contre 148 pour EP (n = 24 585). L'estimation de FIV(240) par réplication est très bruitée (0,94 à 6,6 au point extrême).
- **O-7** : d'accord avec le worker sur les erreurs non nommées de `selection` (`ell_c1` absent, strate manquante).

## Écarts E-1 à E-9 du worker

- **E-1** : accepté. 0 octet 92 vérifié fichier par fichier. Le rapport transcrit porte 5 octets 92 : ce sont les citations de la transcription, hors des pièces.
- **E-2** : accepté. Le mode strict passe 8 fois sur 8 chez moi.
- **E-3** : accepté. Des comptes et des empreintes seulement, et les dossiers exclus étaient absents des copies. J'ai commis le même écart une fois (R-1 plus bas).
- **E-4** : accepté, sous C-3.
  - Le coup d'œil n'a pu orienter aucun élément fixé par le G0 : grille, critère, règles de C1 et C2, égalités κ puis τ_D, 200 réplications et f = 1 sont recopiés à la lettre d'E-S-38. Je l'ai vérifié contre `parametres.json`.
  - Les choix libres faits après lui (Q-T4-6 à Q-T4-10, Q-T4-13) restent des questions à adjuger avant E0. Q-T4-13 garde la lecture stricte (sans pannes longues ni hors-enveloppe), contraire à un ajustement « vers la courbe ».
  - Ce n'est pas un écart à E-S-04 : il lie après E0, et sur une sortie d'E1. Mais toute modification de la grille décidée maintenant serait informée par ces mesures et doit l'écrire dans son ajout daté.
  - La sonde d'identité calcule bien des cellules d'E1 réelles (i = 0 et 1), mais n'imprime que l'empreinte.
- **E-5** : accepté. Le pouvoir de détection est montré par M-14-07, et par mes R-13 et R-14, tués.
- **E-6** : accepté. Les rouges, rejoués avec les tests finaux sur quatre pas, sont concordants.
- **E-7** : accepté. PyYAML de l'hôte, en lecture ; rien d'installé, rien d'importé par le lot.
- **E-8** : accepté. Motif étroit, PID vérifié par `/proc` ; j'ai fait de même (R-7).
- **E-9** : accepté. Les alternates ne lisent que les objets ; je les ai employés aussi. Dépôt propre à la fin.

## Questions Q-T4 (fidélité seulement)

Les treize décrivent fidèlement le code et portent chacune sur une valeur que le G0 ne fixe pas. Les seules réserves portent sur le lieu et le marquage : Q-T4-13 hors de `parametres.json` (C-1), Q-T4-12 sans numéro dans le code (C-5).

## Constat du point 9, recompté

Mes mesures, sur mes propres flux `G2T4-REV-*`, jamais sur les cellules d'E1 (`constat9.txt`) :

| point | strate | 10 réplications | 40 réplications de plus |
|---|---|---|---|
| C0 | calme | 1,06 | — |
| C0 | stress | 0,90 | — |
| (1/10, 50, 4 320) | calme | 1,39 | moyenne 2,02 ; médiane 1,44 ; max 6,55 ; aucune > 10 |
| (1/10, 50, 4 320) | stress | 2,10 | moyenne 1,82 ; max 6,07 ; aucune > 10 |

EP donne 22,9 et 34,6. Le constat est confirmé, au même ordre de grandeur que le worker.

Ce qu'il implique d'après le G0 :
1. **C'est le second constat de SHOGEN-SIM-BIS-FIV-IDENTIF-1.** C2 sera le point le plus proche, vraisemblablement au bord de la grille, et la limite est écrite (PROPOSITION l.330-331 ; AVIS l.24 ; B.61).
2. **Le déclencheur de PLAN-S2BIS-2 reste W*(C0) ≠ W*(C2)**, et PLAN-S2BIS-2 passe avant tout acte A-2 si W*(C2) > 16 ≥ W*(C0) (adjudication 2 du G0). Le constat seul ne le déclenche pas.
3. **Élargir la grille est une modification du G0.** La grille est « pré-déclarée » (E-S-38). Il faudrait un ajout daté avant E0, déclaré comme informé par ces mesures synthétiques ; la décision revient à l'orchestrateur sur avis.
4. **Limite hors théorie, rendue pour être formée (PAROXYSME).** Si la famille n'encadre pas S2, alors W*(C0) = W*(C2) devient vraisemblable. Le filet du G0 ne joue plus, alors que C2 n'est plus le « cas le plus défavorable plausible » (prémisse de l'AVIS Q-S-03). Le G0 ne dit rien de ce cas. À ajouter en précision de FIV-IDENTIF-1.
5. **Lecture des chiffres.** Avec des unités indépendantes, le groupement de I_t exige deux régimes dégradés simultanés. Le modèle nul ne peut donc pas reproduire un groupement venu de modes communs. C'est cohérent avec la lecture de l'AVIS (l.38 de l'ADR : 153 des 154 fenêtres K de S2 étaient des pannes de transport vues d'un seul point).

## Mes écarts

- **R-1** : un `find | wc -l` sur ma copie : un compte seul (786 fichiers), dossiers exclus absents.
- **Barres obliques inverses tapées**, sans effet sur les octets écrits (0 octet 92 dans mes 87 fichiers) :
  - R-2 : un `grep -c` sur une sortie `od`, sans usage ;
  - R-3 : un `tr` sur `/proc/PID/cmdline`, deux fois, remplacé par `cmdline.py` ;
  - R-4 et R-8 : `r13.sh`, `portes.sh`, `rouge_vert_10c.sh`, vus au compte d'octets et réécrits avant exécution ;
  - R-6 : un heredoc Python.
- **R-5** : des heures écrites dans NOTES sans lire l'horloge, corrigées et marquées « non relevée ».
- **R-7** : un PID cherché dans `/proc` par un motif étroit (mon script).
- **R-9** : un `grep -rn` sur `journal/*.txt` du worker (un seul dossier, aucun sous-dossier parcouru).
- **Mesures de type E1** : imprimées sur demande du brief (point 8) et pour le rejeu d'E-S-39, sur mes cellules, jamais sur celles d'E1. Elles n'alimentent aucun choix.

## Journal G1

**[lu]** :
- mon brief ; le rapport transcrit ; BRIEF-SIM-T4 ; BRIEF-AVIS-SIM-T4 (pour connaître la tâche parallèle) ;
- G0 (d9cffc0a…), PROPOSITION (0e78afab…) et AVIS (aaf70a4f…) en entier ;
- ADR-0029 (b908842d…) l.128-166 et l.194-218 ;
- G2-SIM-T3 en entier ; AVIS-SIM-T2 l.276-300 ; AVIS-SIM-T3 l.141-160 ; lignes trouvées dans revue-t1 à revue-t3 par recherche fichier par fichier ;
- annexe B (f7cf4cd5…), blocs B.61, B.62, B.64 et B.66 seulement ;
- EP (c0371ca5…) l.1-16 et l.93-161 ;
- `scripts/plan-s2bis/episodes.py` en entier ; `commun.importer_harnais` ;
- f35a70c par `git show` : `r1.py` l.1-120 et l.300-400 ; `records.py` l.355-423 ;
- les sept diffs ; le code de e14b utile (`regle.py` l.1-265, `calendrier.py`, extraits de `sources.py`, `test_fitness*`) ; `verdict-suite-s2.py` ; le runner l.120-146 ; `gates.yml` l.39-77 et l.100-245 ;
- les outils, le journal, les ébauches et les NOTES du worker ; `isole.sh` (ebaa1c78…) et `lo_up.py` (b532be4b…).

**[abs]** : AVIS-SIM-T4 (non ouvert) ; le reste des pièces de revue-t1 à revue-t3 ; ROTATION-S2BIS.md.

**[2nd]** : la stabilité de `random()` d'une version de Python à l'autre (recoupée 16 fois sur 16) ; l'arrondi correct de `Decimal.ln` (recoupé sur trois cas par `bc`).

**Exposition** : aucune pièce de D.2, aucun `*.jsonl`, aucun dossier exclu. `SHOGEN_S2_CAMPAGNE_CONTROL` n'a jamais été posée. Aucune recherche récursive sur `docs/`, sur le dépôt ou sur le scratchpad.

**Commandes et sorties**, toutes dans `…/sim4/g2/sorties/`. Les PID réels y sont consignés :
- identité : 11053 ;
- campagnes de mutants : 15643 et 17069 ;
- portes : 3710.

Tous les chiffres de ce rapport sont recomptés par mes propres commandes.
