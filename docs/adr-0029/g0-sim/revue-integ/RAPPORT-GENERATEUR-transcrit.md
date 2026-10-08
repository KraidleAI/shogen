# Rapport du générateur — SIM-BIS, intégration des sorties de PLAN-S2BIS-2 (transcrit)

> Transcription par l'orchestrateur le 2026-10-08 18:31:28 UTC du rapport rendu par l'agent af6b0fe34698cd60d (workflow wf_fdc8272f-e05) ; contrôle FM-1.1 : fragments_l51_l14 = 0 ; modèle résolu au transcript : claude-opus-5-5. Texte de l'agent ci-dessous, sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

**Gate 0 : modèle `claude-opus-5-5`** (worker, effort max).

# SIM-BIS : intégration des sorties de PLAN-S2BIS-2 (SB-15A à SB-15F), rapport du générateur

Les six diffs sont prêts, à appliquer dans l'ordre sur b46672b. Les quatre points demandés sont couverts : (1) la nouvelle règle de C1, (3) le masque de J28 appliqué après la génération, (7) le retrait de `e1.ell_c1`, (8) le bord de la grille. Les 78 mutants sont tous tués, aucun FATAL. Le mode strict et les portes sont verts. Seul S-G9 est ROUGE au xtask, comme sur la base (violation connue `docs/17-modele-de-menace.md:70`). Neuf questions sont à adjuger (§6) et un point doit passer au brief de SB-11 (Q-SI-8).

Dossier de travail : `<scratchpad>/s2bis/sim5/`. Le rapport complet est dans `RAPPORT-GENERATEUR.md` (sha256 2143846e…). Il est couvert par `SHA256SUMS` (274 fichiers, contrôle `sha256sum -c` OK, sha256 2d1dd357…).

## 1. Base et cadre
- **Base :** b46672b0ec6da9479361351660b608ce7f6c5343, HEAD du dépôt et tête de `claude/compassionate-noether-szmdyj`, relevée à 16:13 UTC. Elle est égale à celle du brief.
- **Dépôt :** aucune écriture git dans le dépôt. Copies faites par `git archive`, avec les exclusions du brief.
- **Interdits respectés :** `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée, aucun journal ni `*.jsonl` ouvert.
- **Entrées :** les trois sorties de PLAN-S2BIS-2 ont été contrôlées par `sha256sum -c` (3 OK). Leurs empreintes sont égales aux préfixes du JOURNAL, ligne 478.

## 2. Diffs (`sim5/diffs/`)

| diff | contenu | sha256 | code (ajouts, retraits) | plancher | rouge | mutants tués |
|---|---|---|---|---|---|---|
| SB-15A | entrées de PLAN-S2BIS-2 sous deux épingles ; `lire_entree(…, sommes=)` | 3c2c8f77… | +66 −9 | 174 | 2 FAIL, 0 ERROR | 11/11 |
| SB-15B | `masque_j28`, `calendrier_e1` | 8b70e5b7… | +152 −4 | 177 | 3 FAIL, 0 ERROR | 14/14, plus 1/1 en complément |
| SB-15C | réplication : masque appliqué après la génération | 91cb1953… | +68 −19 | 179 | 3 FAIL, 0 ERROR | 11/11 |
| SB-15D | lecteur de `fiv_unites.txt`, même analyseur de ligne que EP | c4e9676c… | +144 −21 | 181 | 2 FAIL, 0 ERROR | 13/13 |
| SB-15E | `q1`, règle de C1, retrait de `ell_c1` | 11bc8970… | +157 −79 | 183 | 4 FAIL, 0 ERROR | 13/13 |
| SB-15F | `e1.bord` (60, 6), `bord`, `ligne_bord` | 0949c81d… | +120 −4 | 189 | 5 FAIL, 0 ERROR | 15/15 |

- Les six diffs passent `git apply --check` puis `git apply` sur une copie neuve de b46672b. Le résultat est égal à l'étape finale e15f.
- Le job tourne conforme à chaque étape : 172, 174, 177, 179, 181, 183, 189.

## 3. Points du contrat (état final)

| point | où c'est fait | tests |
|---|---|---|
| (1) C1 | `calibration.py:22` (forme de ligne), `:66`, `:80`, `:136` (lecteur de `fiv_unites.txt`), `:166` ; `calib_fiv.py:240` `q1`, `:316` C1 = Q₁ minimal, égalités par κ, puis τ_D, puis φ ; `:180-181` séries des hôtes sur le masque | `test_calibration.py:143`, `:164` ; `test_calib_fiv.py:513`, `:530`, `:546`, `:557` |
| (3) calendrier d'E1 | `parametres.json:8-11` ; `commun.py:167` ; `calib_fiv.py:109` `masque_j28` (empreinte recalculée), `:148`, `:168-181` (génération sur le calendrier d'origine, puis restriction au masque, refus `E1/masque` sinon) ; E2 et E3 inchangés | `test_commun.py:229`, `:248` (fige la lecture des trois sorties par leur empreinte) ; `test_calib_fiv.py:279`, `:294`, `:321`, `:344` (masque après génération, à vérifier en G2), `:358`, `:147` ; `test_oracle_r1.py:132` |
| (7) retrait de `ell_c1` | `parametres.json:93` ; schéma de `commun.py` ; plus aucune lecture de la clé, refus `E1/ell` supprimé | `test_calib_fiv.py:416` |
| (8) bord | `parametres.json:94` ; `commun.py:96` ; `calib_fiv.py:264` `bord`, `:282` `ligne_bord` (ligne nommée `[BORD E1]`), `:318` constat rendu par `selection`, C1 inchangé | `test_calib_fiv.py:609` à `:662` (6 tests) |

## 4. Mutants
- 78 mutants, classés par la commande du job (borne 300 s) : 78 tués, 0 vivant, 0 FATAL.
- Le témoin non muté est vert à chaque campagne.
- M-15B-06 visait la mauvaise ligne et a été tué pour cette autre raison. Le mutant voulu a été rejoué (M-15B-06b) et tué.

## 5. Matrice et portes
- **Mode strict :** `-X dev -W error`, avec `PYTHONHASHSEED` 0 et 7, sous Python 3.10.20, 3.11.15, 3.12.3 et 3.13.14. Résultat 8/8 : Ran 189, OK, aucune ligne « Exception ignored », aucune ligne « Warning ». Sous 3.10, rien de particulier.
- **Portes sur la série finale :**

| porte | résultat |
|---|---|
| runner | 97 ok |
| sim-bis | 189 conforme, aussi sous `isole.sh` |
| s2bis | 255 conforme, sous `unshare -n` |
| s2-harness (`--egal`) | 407 OK (2 sauts) conforme, sous `unshare -n` |
| hooks / model-pinning / secrets | 54 / 95 / 147 ok |
| `gate-secrets --tree` | OK |
| R-13 | 0 constat |
| xtask, série = base | S-G1 à S-G8, fmt, no_std et clippy VERT ; S-G9 ROUGE, 1 violation (connue) |

- **Octets 92 :** aucun dans le lot. `gates.yml` en garde 4, comme la base.
- **Longueur de ligne :** tous les fichiers Python font 120 caractères au plus.
- **R-8 :** bibliothèque standard seule, aucune dépendance ajoutée.

## 6. Questions à adjuger (Q-SI)
Aucune ne change de valeur sur les données versées sauf mention contraire.

- **Q-SI-1 :** sans aucun ℓ ≥ 60 dont la garde tient, aucun hôte ne compte pour le bord (pas de condition vraie à vide). Sans effet ici : ℓ retenus de 60 à 720 en calme, de 60 à 360 en stress.
- **Q-SI-2 :** un hôte à F_u indéfini compte parmi les « dix » mais ne satisfait jamais la condition. Sans effet ici : les 20 F_u sont définis.
- **Q-SI-3 :** si aucun couple (hôte, ℓ) n'est retenu dans une strate, refus `E1/indefini` au lieu d'un C1 fixé par les seules égalités.
- **Q-SI-4 :** si aucun point n'a de Q₁ défini, refus `E1/indefini`.
- **Q-SI-5 :** Q₁ est sommé hôte par hôte (ℓ dans l'ordre de la grille), puis dans l'ordre des hôtes, sous le contexte de r1.
- **Q-SI-6 :** `selection` exige toujours la courbe de C0, bien que C0 n'entre plus dans C1.
- **Q-SI-7 :** le texte adjugé de Q-T4-10 garde une clause sur `ell_c1` devenue sans objet. Je l'ai laissé intact et noté la caducité dans `e1.source`. À vous de dire s'il faut l'amender.
- **Q-SI-8, ligne indispensable au brief de SB-11 :** ce lot fournit les pièces mais rien ne les enchaîne. Le brief doit demander :
  - les courbes des dix hôtes sur le masque et leur moyenne, pour chaque point et chaque réplication ;
  - l'appel de `selection` avec `charger_unites` et ces moyennes ;
  - l'impression de `ligne_bord` par strate et, au bord, des phrases de (8)(ii) et (iii) ;
  - le nombre de réplications à FIV indéfini par hôte.
- **Q-SI-9 :** aucun contrôle croisé à l'exécution de n et K de `fiv_unites.txt` contre EP et le masque. Les tests mesurent seulement l'égalité 24 585 / 11 397.

Lecture déclarée pour (8) : « valeur extrême de sa grille » est prise comme la plus grande valeur de chaque coordonnée (1/10, 50, 4 320), comme la parenthèse du G0.

## 7. Écarts
- **E-1 et E-11 :** des barres obliques inverses tapées dans des heredocs. La première a atterri dans un fichier de test, puis a été réécrite. Les octets ont été recomptés : 0 dans le lot comme dans le rapport.
- **E-2 :** un `diff -r` lancé sur deux copies entières du dépôt (sortie vide, rien affiché). Seules des comparaisons ciblées ont suivi.
- **E-3 :** le premier diff faisait +264 lignes. Je l'ai scindé avant toute campagne.
- **E-4, lectures hors liste et ciblées :**
  - l'item SHOGEN-SIM-BIS-POOL-EP-SEPARES-1 (annexe B, ligne 1096), nommé par la précision B.77 ;
  - le JOURNAL, ligne 478 ;
  - `masque_fiv.py`, `dec` et `courbe` de PLAN-S2BIS, pour la forme exacte des sorties ;
  - les outils de `sim4`.
- **E-5 :** les campagnes de mutants et le mode strict ont tourné hors `unshare -n`. Le job final a été rejoué sous `isole.sh`, conforme.
- **E-6 :** la machine partagée était chargée (charge 10 à 12). Mutants jusqu'à 134 s, borne de 300 s jamais atteinte.
- **E-7 :** `parametres.json` et le `README.md` du lot gardent leurs lignes longues existantes.
- **E-8 :** la mesure de coût porte sur deux réplications synthétiques, sans aucune sortie d'E1.
- **E-9 :** au rouge, les tests qui épinglent des données restent verts. Tous les nouveaux tests de code sont rouges par assertion.
- **E-10 :** le README a été complété après les campagnes. Documents seuls : diffs refaits, jobs relancés, portes refaites.

## 8. Items à former
- **I-1 (proposé : SHOGEN-SIM-BIS-E1-COUT-C1-1) :** la règle de C1 ajoute 20 courbes par réplication, soit 0,34 s mesuré. Cela fait environ 73 min de CPU de plus pour E1 (12 800 réplications), à porter au budget et au découpage de SB-11.
- **I-2 :** les lignes du brief de SB-11 décrites en Q-SI-8. Il faut aussi y mettre REGIME-FAISABILITE-1 sur C1 dès son épinglage.
- **I-3 :** la clause de Q-T4-10 devenue sans objet (Q-SI-7).
- **FIV-IDENTIF-1** reste ouvert jusqu'à la sortie d'E1 épinglée.

## 9. Journal de provenance (G1)
- **Lu [lu] :**
  - les deux G0 en entier ;
  - les sorties de PLAN-S2BIS-2 aux lignes citées dans le rapport, avec leur README et `SHA256SUMS` ;
  - PROPOSITION et AVIS de SIM-BIS aux lignes ciblées ;
  - ADR-0029, lignes 31, 38, 401 ;
  - annexe B, lignes 1022, 1067, 1069, 1096, 1097, 1135 ;
  - le code de `scripts/sim-bis` touché.
- **Lu de seconde main [2nd] :** P-5, P-6 et Q-P2-10, connus par le G0 de PLAN-S2BIS-2 et l'ajout daté, sans ouvrir leurs fichiers. **[abs] :** aucune.
- **Valeurs recomptées hors code :**
  - `sha256sum` et `wc -c` des sorties de PLAN-S2BIS-2 ;
  - un oracle indépendant du masque : 46 468 positions, 386 lacunes, 24 585 en calme et 11 397 en stress, empreinte 670dc46e… égale à celle du fichier ;
  - les empreintes des fixtures par `printf | sha256sum` ;
  - la valeur de Q₁ du test par `bc -l` ;
  - les formes de r1 pour K ∈ {0, n}.
- **Copies lourdes** (base, travail, série, cible cargo, arbres temporaires) supprimées à la fin.
