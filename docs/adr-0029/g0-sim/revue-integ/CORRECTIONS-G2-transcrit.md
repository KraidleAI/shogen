# Corrections C-1 à C-4 de SIM-INTEG après la G2 neuve (transcrit)

> Transcription par l'orchestrateur le 2026-10-08 20:46:23 UTC du texte écrit par l'agent af6b0fe34698cd60d dans `<scratchpad>/s2bis/sim5/RAPPORT-GENERATEUR.md` (sha256 6f1e4c32…) ; contrôle FM-1.1 de son transcript : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte de l'agent ci-dessous, sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

## 12. Corrections après la G2 neuve — 2026-10-08, de 18:31 à 19:10 UTC

**Gate 0 : `claude-opus-5-5`.** Entrée : `g2/G2-SIM-INTEG-transcrit.md`, lu en entier, ACCEPTE-AVEC-CORRECTIONS C-1 à
C-4, et l'adjudication de l'orchestrateur. Base gardée : b46672b. Tête courante : 783f426, et non f139242 comme dans la
G2. `scripts/sim-bis`, `gates.yml` et les entrées y sont inchangés.

**Diffs** (`diffs/`, mêmes noms, plus **SB-15G**). Le code de production est inchangé de A à F ; seuls les tests et le
README changent.

| diff | sha256 | code (ajouts, retraits) | plancher | rouge | mutants |
|---|---|---|---|---|---|
| SB-15A | 483b6963… | +66 −9 | 174 | 2 FAIL | 11/11 tués |
| SB-15B | 15209f3e… | +152 −4 | 177 | 3 FAIL | 15/15 tués (complément compris) |
| SB-15C | 652a5c8f… | +68 −19 | 179 | 3 FAIL | 11/11 tués |
| SB-15D | 35eeb496… | +144 −21 | 181 | 2 FAIL | 13/13 tués |
| SB-15E | e59aeb80… | +187 −79 | **185** | 6 FAIL | 13/13, plus MR-03 à MR-06 tués |
| SB-15F | 89b8ae90… | +149 −4 | **193** | 7 FAIL | 15/15, plus MR-10 et MR-26 tués |
| SB-15G | 563ba755… | +59 −6 | **194** | 1 FAIL | 12/12 ; mutants du réviseur 25/26 |

Rouges avec les ébauches : 0 ERROR partout. B, C et D ne changent que par une ligne de contexte du README.

**Corrections :**
- **C-1** (SB-15E), `test_c1_egalites_grille_scellee` : grille scellée de 64 points, Q₁ nul à deux points. Les trois
  paires de la G2 sont départagées par κ, puis par τ_D, puis par le plus petit φ.
- **C-2** :
  - SB-15E, `test_q1_dernier_hote_du_format` : dix hôtes, un seul s'écarte, Q₁ = 16·(ln 2)² par `bc -l`. Testé avec
    okx, le dernier du format, puis avec le premier.
  - SB-15F, `test_bord_derniers_hotes_du_format` : les six hôtes négatifs sont les six derniers ; avec okx remis
    au-dessus, le compte tombe à 5.
- **C-3** (SB-15F), `test_bord_selection_grille_scellee` : `selection` sur la grille scellée, C1 = (1/50, 10, 240),
  C2 = (1/10, 5, 60). Le constat affirme `extremes = []`, ℓ retenus 60 et 240, `hotes = 6`, au bord.
- **C-4** (SB-15F) : docstring corrigée, Q-SI-1 pour la vacuité, Q-SI-2 pour l'hôte à F_u indéfini.
- **README, ligne 9** (SB-15A) : coupée en 114 + 45 caractères. Les seules lignes de prose de plus de 120 caractères qui
  restent viennent de la base.
- **Rouge des corrections**, montré contre chaque survivant appliqué à l'étape corrigée (`journal/rouge-MR-*.txt`) :
  un seul FAIL d'assertion à chaque fois, celui du test visé, 0 ERROR.
  - MR-03, MR-04, MR-05 → `test_c1_egalites_grille_scellee`
  - MR-06 → `test_q1_dernier_hote_du_format`
  - MR-10 → `test_bord_selection_grille_scellee`
  - MR-26 → `test_bord_derniers_hotes_du_format`

  Les tests sont les miens. Je n'ai ni ouvert ni recopié `g2/outils/test_revue_g2.py`. Les mutants du réviseur ont été
  recopiés (`outils/mutants_mr.py`, identité vérifiée sur ses chaînes), et ses 26 mutants lus par empreinte (6903583c…).

**Q-SI-9, fermé dans ce lot (SB-15G).**
- **Construction.** Les égalités tiennent par construction, d'après le code et le contrat de PLAN-S2BIS-2 :
  - `classer` (`scripts/plan-s2bis/commun.py` l.113-123) range chaque fenêtre retenue sous sa strate journalisée ;
  - D_u est construite sur ce rangement (`masque_fiv.py` l.99) ;
  - le masque compte les mêmes fenêtres par strate du calendrier (l.37), et le contrôle (b) exige que les deux strates
    soient égales (l.46) ;
  - le contrôle (f)(i), P-5, exige n_s = n et cellules « ecart » = K à EP (l.101-103) ;
  - SIM-BIS reconstruit le masque, puis contrôle ses comptes et son empreinte.
- **Mesure** sur les données versées (`outils/mesure_croisement.py`, `journal/mesure_croisement.txt`) : 20 couples
  (strate, hôte), 0 écart ; n = 24 585 en calme et 11 397 en stress, K = cellules « ecart » d'EP.
- **Code.** `calibration.croiser_unites(unites, presentes, ep)` lève le refus nommé `CALIB/croisement`. Elle est appelée
  par `charger_unites(prm, presentes, ep, lus, environ)` : la signature change, le contrôle ne peut pas être sauté.
- **Test.** `test_croisement_q_si_9` : retouches sur okx ou sur la dernière ligne seulement ; strate ou hôte absents.
- **Conséquence pour SB-11.** La ligne (b) de Q-SI-8 devient
  `calibration.charger_unites(prm, cal["presentes"], ep)`. À verser à SHOGEN-SIM-BIS-SB11-BRIEF-1 avec la ligne (e).

**Mutants.** 122 exécutions par la commande du job, borne 300 s : **121 TUÉS, 1 VIVANT, 0 FATAL**, témoins verts.
- Le vivant est **MR-18** du réviseur, qu'il tient pour équivalent (σ̂²_bloc > 0 dès que 0 < K < n, mesuré sur 819 cas).
  Je vérifie seulement que σ̂²_bloc = 0 quand K ∈ {0, n} ; je ne démontre pas le reste.
- Les six survivants exigés (MR-03, -04, -05, -06, -10, -26) sont tués, sur leur diff et sur l'étape finale.
- Les campagnes A à D ont été refaites aussi, sur les étapes à README corrigé.

**Matrice et portes.**
- **Mode strict** sur e15g, `-X dev -W error`, `PYTHONHASHSEED` 0 et 7, Python 3.10.20, 3.11.15, 3.12.3 et 3.13.14 :
  8/8 verts, Ran 194, aucune ligne « Exception ignored » ni « Warning ».
- **Portes** sur la série A…G appliquée à b46672b :

| porte | résultat |
|---|---|
| runner | 97 ok |
| sim-bis | 194 conforme, aussi sous `isole.sh` |
| s2bis | 255 conforme, sous `unshare -n` |
| s2-harness | 407 (2 sauts) conforme, sous `unshare -n` |
| hooks / model-pinning / secrets | 54 / 95 / 147 ok |
| `gate-secrets --tree` | OK |
| R-13 | 0 constat |
| xtask, série = base | S-G1 à S-G8, fmt, no_std et clippy VERT ; S-G9 ROUGE, 1 violation connue (`docs/17-modele-de-menace.md:70`), section S-G9 identique |

- **Tête 783f426 :** la série s'applique 7/7 ; `scripts/sim-bis` et `gates.yml` y sont égaux à e15g. Runner de la tête :
  136 ok ; job sim-bis : 194 conforme.
- **Forme :** 0 octet 92 dans le lot, les diffs et mes outils. Les 510 octets 92 des étapes sont les copies de
  `gates.yml` (4) et du runner (30) de la base, dans 15 instantanés. Fichiers Python : aucune ligne de plus de 120
  caractères.

**Écarts.**
- **E-12 :** j'ai lu `g2/outils/mutants_g2.py` (les définitions des survivants) et l'ai exécuté par `runpy` pour en
  rejouer les 26 mutants. Sa campagne n'a pas été lancée.
- **E-13 :** `avant-g2/` garde les étapes, les diffs et les journaux d'avant la G2, pour référence ; les fichiers
  courants portent les mêmes noms.
- **E-2 :** consigné, sans suite (adjudication).

**Q-SI.** Q-SI-1 à Q-SI-6 adoptées. Q-SI-7 et Q-SI-8 sont à l'orchestrateur, rien à coder ici. Q-SI-9 est fermé.

