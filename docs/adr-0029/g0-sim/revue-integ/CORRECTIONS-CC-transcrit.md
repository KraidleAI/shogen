# Corrections CC-1 et CC-2 de SIM-INTEG (transcrit)

> Transcription par l'orchestrateur le 2026-10-08 20:46:23 UTC du texte écrit par l'agent af6b0fe34698cd60d dans `<scratchpad>/s2bis/sim5/RAPPORT-GENERATEUR.md` (sha256 6f1e4c32…) ; contrôle FM-1.1 de son transcript : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte de l'agent ci-dessous, sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

## 13. Corrections du contre-contrôle (CC-1, CC-2) — 2026-10-08, de 19:36 à 19:56 UTC

**Gate 0 : `claude-opus-5-5`.** Entrée : `g2/cc/RAPPORT-CC.md`, lu en entier (NON-CONFORME, CC-1 et CC-2), et
l'adjudication de l'orchestrateur. Tests seulement, planchers inchangés. Base gardée : b46672b ; tête courante 5cfe746.
J'ai écrit mes propres tests : `g2/cc/outils/test_cc.py` n'a pas été ouvert. MG-14 a été lu dans
`g2/cc/outils/mutants_cc.py` (empreinte c7d77b8c…), MR-18 dans `g2/outils/mutants_g2.py` (6903583c…).

**Corrections :**
- **CC-2** (SB-15D, donc D à G), `test_fiv_unites_indefini` : on prend la ligne versée de binance à ℓ = 1 (n = 24 585,
  K = 372, γ̂₀ et cv recopiés, donc cohérents) et on la réécrit FIV « - », σ̂²_bloc = 0. Refus attendu : CALIB/coherence.
  La docstring est corrigée : le cas K = 3 écrit γ̂₀ « 0 », il est donc refusé par le contrôle de γ̂₀.
- **CC-1** (SB-15G), `test_croisement_q_si_9` : `charger_unites(PRM, environ={})` doit lever `TypeError`.

**Diffs :**

| diff | sha256 | code (ajouts, retraits) | plancher |
|---|---|---|---|
| SB-15D | b568584f… | +152 −21 | 181 |
| SB-15G | 87085b1b… | +62 −6 | 194 |

Les diffs A, B, C, E et F sont inchangés à l'octet (483b6963…, 15209f3e…, 652a5c8f…, e59aeb80…, 89b8ae90…).

**Rouges :**
- **Contre les survivants** (`journal/rouge-cc.txt`), un seul FAIL d'assertion à chaque fois, 0 ERROR :
  - MR-18 sur e15d corrigé : `test_fiv_unites_indefini`, « Refus not raised » ;
  - MG-14 sur e15g corrigé : `test_croisement_q_si_9`, « TypeError not raised » ;
  - les deux mutants restent verts sur les étapes d'avant (`avant-cc/`), ce qui montre le manque que comblent les
    tests.
- **Avec les ébauches :** D, 2 FAIL ; G, 1 FAIL ; 0 ERROR.

**Mutants** (commande du job, borne 300 s) :
- D : 14/14 tués (13, plus MR-18) ;
- G : 54/54 tués (12 + les 26 de la G2, dont MR-18 + les 16 du contre-contrôle, dont MG-14) ;
- témoins verts, 0 FATAL.

Avec les campagnes A, B, C, E et F (inchangées, 18:59-19:06) : 139 exécutions, **139 TUÉS, aucun vivant**.

**Matrice et portes :**
- **Mode strict** sur e15g, `-X dev -W error`, Python 3.10.20 à 3.13.14 × `PYTHONHASHSEED` 0 et 7 : 8/8, Ran 194, aucune
  ligne « Exception ignored » ni « Warning ».

| porte | série A…G sur b46672b | série A…G sur 5cfe746 |
|---|---|---|
| application | 7/7 | 7/7 |
| runner | 97 ok | 136 ok |
| sim-bis | 194 conforme, aussi sous `isole.sh` | 194 conforme |
| s2bis | 255 conforme | 255 conforme |
| S2 (s2-harness) | 407 conforme | 415 conforme |
| hooks / model-pinning / secrets | 54 / 95 / 147 | non relancé |
| `gate-secrets --tree` | OK | non relancé |
| R-13 | 0 constat | non relancé |
| xtask | égal à la base : S-G9 seul ROUGE (violation connue `docs/17:70`) | non relancé |

Sur 5cfe746, `scripts/sim-bis` et `gates.yml` sont égaux à e15g ; seul le runner de la tête diffère, et mes diffs n'y
touchent pas.

**Forme :** 0 octet 92 dans le lot, les diffs, les journaux et les outils ; fichiers Python : aucune ligne de plus de
120 caractères.

**Écarts :** E-14, j'ai lu `g2/cc/outils/mutants_cc.py` et l'ai exécuté par `runpy`, empreinte contrôlée, sans lancer
sa campagne. `avant-cc/` garde l'état d'avant le contre-contrôle.
