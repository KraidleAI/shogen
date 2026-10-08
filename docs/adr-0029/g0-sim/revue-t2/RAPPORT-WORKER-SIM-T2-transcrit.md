# Rapport du worker, lot SIM-BIS tranche 2 (SB-3, SB-4 : couche des sources) — transcription par l'orchestrateur

Rapport rendu par message. Worker `claude-opus-5-5`, effort max, 2026-10-05 00:13:00 à 02:03:09 UTC. Brief `…/sim2/BRIEF-SIM-T2.md`
(sha256 `e8fa73c4…1c5a`). Base finale : tête `784ebd2` (tranche 1 commise), plancher de départ 49.

## Livraison : `…/sim2/diffs-784ebd2/` (SHA256SUMS de `…/sim2/`, 121 entrées, sha256 `daad68ff…eeb6`)
| diff | contenu | code | plancher |
|---|---|---|---|
| SB-3a | lois de durée (empirique, géométrique), loi résiduelle P(R=k)=P(L≥k)/E[L], renouvellement alterné stationnaire, chaîne à deux états (T-GEN-1), masques, cache des tables | 196 | 53 |
| SB-3b | flux des composants pré-déclarés ; taux exacts cellules/n_s ; loi « tous épisodes » regroupée en stress (E-S-10) ; pannes longues, régime ; oracle C0 (E-S-39) ; `tests/test_fitness_tirages.py` (ni `**` ni `pow` ; de `random`, `random()` seule) | 199 | 60 |
| SB-3c | indices de flux ; `Replication` ; régime Z par (hôte, strate) ; union E ∪ (E′∩Z) ∪ L ; H(u) par strate ; refus SOURCES/regime, SOURCES/taux | 156 | 64 |
| SB-3d | dérives E-S-13 (tendances, sauts, panne initiale, commune, transitoire) par amincissement des épisodes | 147 | 68 |
| SB-4a | pools par classe ; F(u,c) ; F d'ETH et des stables = F de BTC × autres ; composante hors-enveloppe ; état vrai typé (T-GEN-2) | 120 | 71 |
| SB-4b | incidents E-S-15 (cible, grille, ETH) : à π, k parmi sans remise, imposés ; unités faibles E-S-16 ; triplets | 175 | 75 |

993 lignes de code (≈ 370 au G0, ×2,7). Fichiers : `sources.py` (414), `tests/test_sources.py` (442), `tests/test_fitness_tirages.py` (70),
`parametres.json` (section `sources`), `commun.SCHEMA`, README, `gates.yml` (plancher seul). Items B.62 traités : LIBM-POW-1 (tout `**`
refusé), TABLES-CACHE-1 (cache, coût mesuré), EP-COMPLETS-1 (limite écrite), MUT-COMMANDE-1 (campagnes).

## Preuves (base `784ebd2`, journal `final2.txt`)
Rouges : tests de chaque étape sur le code de l'étape précédente (6/6) ; rouges d'assertion sur ébauches (4, 5, 4, 4, 3, 4 FAIL) ;
chronologie : rouges d'import ou d'attribut avant le code pour SB-3a à SB-4a, rouge d'assertion avant le code pour SB-4b. Verts : ligne du
job aux planchers exacts ; runner 33 ; Python 3.10 à 3.13 avec `-W error`. Mutants : 80/80 tués par leur test nommé, classés par la
commande du job (runner d'abord, borne 120 s). Série = dernière étape à l'octet. Gates : sim-bis 75, s2bis 49, S2 405, hooks 54,
model-pinning 95, secrets OK, xtask S-G1 à S-G8 vertes (S-G9 connu sur copie). Identité : sonde W = 16 (241 920 fenêtres, 38 séries),
12/12 même sha256 `85c7fbdd…9d550e29`. Coût : 0,29 s par réplication (N1), 0,34 s avec sauts, amorçage 4,7 s par processus.

## Questions de conception à adjuger
- Q-T2-1 : un processus stationnaire indépendant par strate (épisode coupé à chaque jonction ; régime indépendant d'une strate à l'autre).
- Q-T2-2 : régime par superposition E ∪ (E′∩Z) ; taux marginal et κ exacts ; E′ tirée fenêtre par fenêtre, indépendante (convention
  L = 1 de S2) : toute la grille E1 faisable à f = 1 (r′ max ≈ 0,66) ; r′ ≥ 1 refusé.
- Q-T2-3 : H suit l'histogramme « panne » d'EP, F l'histogramme « ecart » ; histogramme différence écarté ; regroupement en stress par type.
- Q-T2-4 : F des autres classes = même taux et même loi que BTC, réalisation indépendante, × `autres` ; composante hors-enveloppe par
  (hôte, classe, strate), épisodes d'une fenêtre, ni × f ni amincie.
- Q-T2-5 : pannes longues sur H seulement, durées 1 h, 1 jour, 3 jours équiprobables (poids non fixés par le G0).
- Q-T2-6 : dérives : tendance sur W·10 080 puis tenue jusqu'à T_max ; saut d'amplitude 0,1 à 1,9 à instant uniforme sur 3 hôtes sur 10 ;
  panne initiale de 4 320 fenêtres sur un hôte décalé ; transitoire ×3 sur 10 080 fenêtres ; ni sur incidents ni sur unités faibles.
- Q-T2-7 : pools provisoires ETH 10, USDC 8 (sans coinbase ni okx), USDT 10 ; présence des agrégateurs et de l'oracle [inféré].
- Q-T2-8 : incidents : un processus de débuts au taux ρ·w/86 400 sur toute la grille ; durée D fixe ou géométrique, coupée à T_max ;
  chevauchements fusionnés ; ajoutés à H.
- Q-T2-9 : unités faibles : type « panne » (toutes classes de l'hôte) ou « ecart » (BTC seul), un processus sur toute la grille.
- Q-T2-10 : E-S-16 ne fixe ni les hôtes faibles, ni la population des triplets, ni le partenaire de l'unité faible : paramètres de
  cellule à pré-déclarer à SB-11.
- Q-T2-11 : indice de flux = (h·S + s)·10 + k ; un hôte retiré décale les tirages des suivants : acceptable sous l'épinglage E0, ou indice
  par nom ?
- Q-T2-12 : le coût de la couche des sources seule égale l'estimation de la proposition pour toute la chaîne (0,3 s) : budget E-S-46.

## Écarts
E-1 ×2,7 ; E-2 base avancée puis rebasage ; E-3 rouge d'assertion avant le code seulement pour SB-4b (consigne arrivée en cours de
passe), rouges d'assertion des cinq autres étapes consignés après le code ; E-4 corrections de tests en cours de route (fuite de
flottant, cas T-GEN-2, attendu manuscrit faux refait à la main, tirage changé pour rendre M-3D-05 non équivalent) ; E-5 contrôle I-3 dans
un fichier neuf ; E-6 deux changements de conception en cours de passe (E′ indépendante, garde nommée du régime) ; E-7 S-G9 sur copie,
`gate-secrets --tree` dans un dépôt jetable ; E-8 exposition : EP en entier, JOURNAL l.438-445, trois lignes « note » de xtask affichées
(documents permis) ; E-9 défauts d'outillage (fichier affiché pour M-3B-14, PID) ; E-10 deux commandes finies en tâche de fond ; E-11
octets 92 voulus dans trois outils hors dépôt ; E-12 rapport par message ; E-13 première reconstruction de série invalide, refaite.

## Items proposés
SHOGEN-SIM-BIS-SOURCES-STRATES-1 (Q-T2-1) ; SHOGEN-SIM-BIS-DERIVE-AMPLITUDE-1 (amplitude du saut, durée de la panne initiale, poids des
pannes longues, à adjuger avant E0) ; SHOGEN-SIM-BIS-REGIME-FAISABILITE-1 (r′ ≥ 1 possible pour des combinaisons extrêmes, à contrôler sur
N8, N9, X1, X2 dès que C1 et C2 sont épinglés) ; SHOGEN-SIM-BIS-ABS-POPULATIONS-1 (Q-T2-10, à SB-11) ; constats pour CALCUL-1 (coût) et
PAIRES-1 (part inférée des pools provisoires).

## Estimation
SB-6 à SB-14 : ≈ 2 600 à 4 000 lignes en 14 à 21 diffs ; lot ≈ 4 800 à 6 200 lignes [inféré].
