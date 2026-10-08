# G0 — proposition pour le lot PLAN-S2BIS-2 (groupement des pannes, source par source), sans code

- **Statut** : proposition d'un worker à l'orchestrateur, à adjuger. Rien n'est décidé ici. Aucun code, aucune écriture au
  dépôt, aucune opération git en écriture.
- **Gate 0** : modèle résolu `claude-opus-5-5`, effort max (fiche `shogen-worker`).
- **Dates** (`date -u`) : lecture des pièces le 2026-10-05 de 13:22 à 13:44 UTC ; calculs à 13:38 UTC (horodatage des
  fichiers de `calc/`) ; rédaction de 13:49 à 13:59 UTC.
- **Brief** : `scratchpad/s2bis/plan2/BRIEF-G0-PLAN2.md`, 72 lignes, sha256 `596e66ef…591c` [mesuré] ; le brief n'annonce ni
  sha256 ni base.
- **Base lue** : branche `claude/compassionate-noether-szmdyj`, tête `5f99ab5` au début et à 13:49 UTC, `git status --short`
  vide [mesuré]. SB-9, SB-10 et SB-14 (tranche 4 de SIM-BIS) ne sont pas commis : `calib_fiv.py` est lu dans les diffs
  `scratchpad/s2bis/sim4/diffs/SB-10A.diff` à `SB-10C.diff` (sha256 égaux au rapport du worker, RW-T4 l.22-24 [mesuré]).
- **Rattachement** : ADR-0029 révision 3, acceptée : §2.4 (l.118-164, dont (c) l.135-137 et l.143, (e) l.158) ; §2.6
  (l.177-192, dont l.179 : calcul sur une extraction de `f35a70c`) ; §6 lot 3 (l.383 : « distributions des longueurs
  d'épisodes par source et courbe FIV_série(ℓ) pour calibrer les simulations » ; « tout calcul sur les journaux de S2 se fait
  sur une extraction du commit d'analyse `f35a70c` ») ; ajout daté du 2026-10-04 23:02:56 UTC (l.399, pts 2 et 5). G0 de
  SIM-BIS : adjudication 2 (G0-SIM l.13-15) ; ajout daté du 2026-10-05 01:45:03 UTC, pt 2 (G0-SIM l.33). Proposition de
  SIM-BIS : E-S-38 (PROP l.197), §5.3 (PROP l.324-332), Q-S-03 (PROP l.492-495), item FIV-IDENTIF-1 (PROP l.601). Avis :
  AVIS l.18-25, l.100, l.104 ; avis SIM-T4, option B (T4 l.16, l.45, l.108-116). Items : SHOGEN-SIM-BIS-FIV-IDENTIF-1
  (B.61 l.1022) et SHOGEN-SIM-BIS-SOURCES-LIMITES-1 (B.64 l.1070, précisé à B.66 l.1091). Patron : G0 de PLAN-S2BIS
  (`docs/adr-0029/G0-lot-PLAN-S2BIS.md` l.17-26), B.58 (l.956-972), `scripts/plan-s2bis/`, `docs/adr-0029/plan-s2bis/`.
- **Modèle de forme** : `docs/adr-0029/g0-sim/PROPOSITION.md`.
- **Conventions** : [lu] lu sur la pièce ; [mesuré] commande lancée par le rédacteur (§14) ; [calc] calcul du rédacteur
  (`calc/calc_p2.py`, §14) ; [inféré] raisonnement du rédacteur ; [abs] absent des pièces lues. Exigences : E-P2-nn.
  Sous-lots : P2-n. Tests : T-P2-… ; mutants : M-P2-nn ; questions : Q-P2-nn. **[G0]** = touche la lettre du G0 de SIM-BIS ;
  **[ADR]** = touche la lettre de l'ADR-0029 (ajout daté) ; **[INV]** = information ou décision de l'investisseur. Tailles :
  lignes ajoutées, tests et données compris, documents hors compte (convention de PROP l.31-33) ; toutes [inféré].
- **Renvois** : « l.n » = ADR-0029 à `5f99ab5` (sha256 `b908842d…`, 569 lignes). « EP l.n » = `docs/adr-0029/plan-s2bis/
  episodes.txt` (`c0371ca5…`). « PROP l.n », « AVIS l.n », « G0-SIM l.n » = `docs/adr-0029/g0-sim/PROPOSITION.md`,
  `AVIS.md`, `G0-SIM-BIS.md`. « T2 l.n », « T3 l.n » = `g0-sim/revue-t2/AVIS-SIM-T2.md`, `revue-t3/AVIS-SIM-T3.md`. « T4 l.n »
  et « RW-T4 l.n » = `scratchpad/s2bis/sim4/g2/AVIS-SIM-T4.md` et `RAPPORT-WORKER-SIM-T4-transcrit.md`. « B.nn l.n » = annexe B
  d'ADR-0028 à `5f99ab5` (`f7cf4cd5…`). « PS2 <fichier> l.n » = `scripts/plan-s2bis/<fichier>`. « G1-PS2 », « G2-PS2 » =
  `docs/adr-0029/plan-s2bis/G1-lot-PLAN-S2BIS.md`, `G2-lot-PLAN-S2BIS.md`. « SB-10A l.n » = ligne du fichier de diff.

## 0. En bref

1. **Objet** : mesurer une fois, sur les journaux scellés de S2 lus à `f35a70c` par les seuls scripts du lot, ce que les
   sorties de PLAN-S2BIS ne donnent pas : (a) FIV_u(ℓ), facteur d'inflation de variance de la série d'écart de chaque hôte du
   pool D1-bis, par strate, aux 17 ℓ de la grille de calibration ; (b) la loi des pauses entre épisodes de chaque hôte ; (c) le
   masque des fenêtres évaluables du segment J28. Lectures de classe M : structure sérielle d'une seule source, validité de
   l'observateur, aucune co-occurrence entre hôtes (AVIS l.23 ; T4 l.45).
2. **Pourquoi maintenant** : la famille E1 culmine vers FIV(240) ≈ 2 pour I_t, contre 22,9 et 34,6 sur EP (RW-T4 l.64-67).
   C'est une dilution structurelle (T4 l.93-95) : I_t, qui exige deux hôtes en écart, mesure mal le régime propre de chaque
   source, que FIV_u mesure directement (PROP l.331-332). Option B de l'avis SIM-T4 (T4 l.111, l.114), adoptée par
   l'orchestrateur (brief l.20).
3. **Usage dans SIM-BIS** : C1 devient le point de la grille d'E1 calibré sur les FIV_u (lettre proposée de l'ajout daté au
   G0 de SIM-BIS, §3.2) ; C2 garde sa définition sur I_t, C0 la sienne ; les trois tournent sur le masque mesuré, ce qui lève
   la limite Q-T4-5 (T4 l.45).
4. **Patron de PLAN-S2BIS, sans relâchement** : exception écrite au G0 pour les seuls scripts du lot ; sha256 des journaux
   contre le bloc machine du paquet de S2 ; harnais extrait de `f35a70c`, modules épinglés ; contrôle au bloc 3 du rendu J28 ;
   épinglage au JOURNAL avant toute lecture ; exécution unique, détachée, par l'orchestrateur ; tests sur fixtures seulement ;
   G1 ; G2 neuve à 100 %.
5. **Plus serré que le patron** (proposé) : `scripts/plan-s2bis/` réemployé par chemin et sha256, jamais modifié ; recomptes
   fail-closed contre EP (épisodes de chaque hôte ; courbe de I_t aux 17 ℓ) ; chaque FIV_u calculé deux fois (r1 extrait et
   estimateur exact du lot) ; épingle du JOURNAL passée en argument au lanceur ; deux passes A et B comparées à l'octet dans
   l'unique lancement (Q-P2-08) ; critère de C1 adjugé **avant** l'exécution du lot (Q-P2-07).
6. **Taille** : l'item annonçait ≈ 150 lignes (B.61 l.1022), ce qui couvre le seul noyau d'analyse. Au patron complet :
   ≈ 1 100 à 1 400 lignes en 8 sous-lots de 200 lignes au plus [inféré, par analogie mesurée : PLAN-S2BIS, 1 477 lignes en
   9 diffs, G1-PS2 l.43-51 [calc]]. Côté SIM-BIS, un diff d'intégration de ≈ 180 à 250 lignes avant E0 (§3.5).
7. **Calendrier** : ≈ 4 à 6 h de session après l'adjudication [inféré : PLAN-S2BIS est passé de son G0, 14:55:41 UTC, à son
   versement, 17:01:22 UTC, en 2 h 06 min [calc], G0-lot-PLAN-S2BIS l.3, B.58 l.956] ; hors du chemin critique tant que SB-11
   à SB-13 ne sont pas finis (RW-T4 l.129-136).
8. **13 questions** (§7). Les plus lourdes : le critère de C1 (Q-P2-05), ce que devient la durée déclarée sur C2 (Q-P2-06,
   [G0] et [ADR]), le moment de l'ajout daté (Q-P2-07), l'artefact de censure en stress (Q-P2-10).
9. **Constat neuf** [calc, EP l.13-92] : en stress, 453 des 674 épisodes d'écart des dix hôtes sont censurés, c'est-à-dire
   voisins d'une fenêtre non retenue (chainlink 109 sur 112, coingecko 119 sur 127, kraken 44 sur 46, bitfinex 49 sur 51 ;
   EP l.67, l.75, l.87, l.59) ; en calme, 186 sur 1 208. En stress, les pannes collent aux absences de l'observateur unique
   [inféré : la censure d'EP compte aussi les bords de strate, au plus deux positions par week-end, dix sur les cinq week-ends
   de la portée [calc]] ; FIV_u en portera l'empreinte. D'où une C1 déclarée borne haute (T4 l.111) et un diagnostic proposé
   (Q-P2-10).

## 1. Objet, rattachements, périmètre

### 1.1 Objet et rattachements

- **ADR-0029** : §6 lot 3 (l.383) couvre déjà la courbe FIV par source et impose l'extraction de `f35a70c` ; le lot ne change
  pas la lettre de l'ADR (AVIS l.18). Seule la question Q-P2-06 (b) toucherait un ajout daté (l.399, pt 2).
- **G0 de SIM-BIS** : adjudication 2 (G0-SIM l.13-15 : PLAN-S2BIS-2 avant toute question de durée, aucun allongement sur un
  artefact de calibration) ; ajout daté pt 2 (G0-SIM l.33 : E-S-10 irréalisable à la lettre, « recours : PLAN-S2BIS-2 ») ;
  Q-S-03 (b) (PROP l.492-493 : FIV_u(ℓ) par unité et loi des intervalles entre épisodes, par strate, à `f35a70c`, scripts
  épinglés avant exécution).
- **Items** : SHOGEN-SIM-BIS-FIV-IDENTIF-1 (B.61 l.1022 ; second constat : RW-T4 point 9, T4 l.86) ; le lot en est la
  construction, avancée par décision datée de l'orchestrateur (option B). SHOGEN-SIM-BIS-SOURCES-LIMITES-1 (B.64 l.1070 ;
  B.66 l.1091) : ses limites de générateur, dont O-5 (« loi des longueurs conforme à EP sous C0 seulement »), deviennent
  chiffrables par les pauses et épisodes mesurés ; le lot y ajoute trois limites (§11).

### 1.2 Ce que le lot fait

- Trois sorties, chacune par un script, sur les journaux scellés (§2) : `masque_j28.txt`, `fiv_unites.txt`,
  `intervalles.txt`, plus leur `SHA256SUMS`.
- Avant toute valeur, des contrôles fail-closed (E-P2-11) : bloc 3 du rendu J28 ; masque contre l'ADR ; recomptes égaux à EP ;
  double calcul de chaque FIV_u.
- Rien d'autre : aucune statistique de test, aucun z, aucune mesure de co-occurrence au-delà du recompte de I_t contre EP, qui
  est déjà publiée.

### 1.3 Entrées

| entrée | usage | état |
|---|---|---|
| journaux scellés de S2, copie de session (`control.jsonl`, `journal.jsonl` ; `raw.jsonl` haché seulement) | lecture par les scripts du lot, seuls | pièce D.2 n° 7 (« et toute copie ») : pour tout agent, sha256 seuls (annexe D l.40 [lu, noms seulement]) ; chemin de la copie : G1-PS2 l.130 |
| harnais `s2-harness` extrait de `f35a70c` | lecteurs (`records`, `window`, `r1`), classement, `r1.block_long_run_variance` | cinq épingles de PS2 parametres.json l.13-20 |
| `scripts/plan-s2bis/commun.py` (`14920e87…`) et `parametres.json` (`7e214864…`) | chemin de lecture, pools, classement, contrôle du bloc 3 ; segment, strates, pool D1-bis, classes, types d'épisodes, quantiles, grille ℓ | commis ; code épinglé au JOURNAL le 2026-10-04 à 16:57:31 UTC (B.58 l.960-961) ; sha256 égaux à `scripts/plan-s2bis/SHA256SUMS` (`65c26310…`) [mesuré] |
| EP (`c0371ca5…`) | recomptes : épisodes par hôte (EP l.13-92), courbe de I_t du pool D1-bis (EP l.128-161) | versée ; égale à `docs/adr-0029/plan-s2bis/SHA256SUMS` (`f21f9293…`) [mesuré] |
| paquet de S2 (`4d2a8276…`) ; rendu J28 (`26877549…`) | bloc machine (sha256 des journaux, commit d'analyse) ; bloc 3 | épingles de PS2 parametres.json l.21-31 ; le rendu, dans un dossier interdit aux agents, n'est lu que par `commun.controle` |
| l.31 | fenêtres sautées hors D5 : 5 701 en calme, 2 094 en stress | contrôle du masque |

### 1.4 Hors périmètre

- Toute co-occurrence entre hôtes : la variante « écarts isolés » (Q-P2-02 c) est écartée. Toute donnée de S2-bis, tout taux du
  rodage. Les flux hors D1-bis (`okx_index`, Pyth). τ, σ et OKX, déjà faits par PLAN-S2BIS.
- Le code de SIM-BIS : lecteur des sorties, masque dans le calendrier d'E1, critère de C1 et impressions forment un diff de
  SIM-BIS, décrit au §3.5, hors de ce lot.

### 1.5 Items traités

| item | ce que le lot en fait |
|---|---|
| SHOGEN-SIM-BIS-FIV-IDENTIF-1 (B.61 l.1022) | construction faite par ce lot ; l'item reste ouvert jusqu'à l'épinglage de C1 par E1 et l'écriture de sa limite (§11) |
| SHOGEN-SIM-BIS-SOURCES-LIMITES-1 (B.64 l.1070) | reçoit trois limites mesurables (§11) ; O-5 devient chiffrable |
| SHOGEN-SIM-BIS-STRESS-EPISODES-1 (B.61 l.1029) | si Q-P2-11 (b) : histogrammes des épisodes complets, pour chiffrer la limite |
| SHOGEN-LECTEUR-INDEP-1 (G2-PS2 l.182) | la limite s'étend : ce lot réemploie aussi les lecteurs du harnais |
| SHOGEN-PLAN-S2BIS-LOG-1, -VARIABLE-TEST-1 (G2-PS2 l.170-175) | consignes appliquées (E-P2-05, E-P2-07) |
| SHOGEN-FICHE-WORKER-POSTEXEC-2 (B.58 l.972) | l'exception reste écrite au G0 du lot, faute de fiche complétée |
| SHOGEN-PLAN-S2BIS-GARDES-1 (B.58 l.970) | non déclenché : `scripts/plan-s2bis/` n'est pas touché (E-P2-01) |

## 2. Sorties exactes et leur forme

### 2.1 En-tête commun des trois sorties

1. Ligne 1, mot pour mot, l'étiquette de PLAN-S2BIS : « préparation de S2-bis ; ne change pas le verdict de S2 (« R1
   discrimine » = FAUX) » (PS2 parametres.json l.3 ; G0-lot-PLAN-S2BIS l.25).
2. Ligne 2 : `<script> — <objet> (PLAN-S2BIS-2 ; SHOGEN-SIM-BIS-FIV-IDENTIF-1)`.
3. Puis, dans la forme de PS2 commun.py l.181-194 : sha256 de chaque module chargé (modules du lot, `commun.py` de PLAN-S2BIS)
   et des deux `parametres.json` ; commit d'analyse et épingles du harnais ; sha256 des journaux ; portée au format d'EP l.6 ;
   pools S2 et D1-bis ; les deux lignes du contrôle du bloc 3 ; les lignes des contrôles propres du script (E-P2-11).
4. Aucune heure, aucun hôte, aucune version dans une sortie. Les heures vont au README du versement (E-P2-24).

### 2.2 `masque_j28.txt` (masque des fenêtres évaluables de J28)

Positions j = (ws − t0)/w de la portée [t0 ; t_fin), pas w = 60 s. Strate de chaque position par le calendrier du harnais
(jour UTC, `window` de `f35a70c`). Position retenue = fenêtre de `r1.build_window_strate` après `records.filtre_lecture`
(segment J28 à n fixe, plage D5 exclue ; PS2 commun.py l.64-87).

```
[MASQUE J28] positions j = (ws − t0)/w de la portée ; strate par jour UTC ; retenue = fenêtre retenue de la strate
  portée : t0 = 1787770800 ; t_fin = 1790558880 ; positions = 46468 ; plage D5 : j = 41718 à 44408 (2691 positions)
  « calme » : calendrier hors D5 = 30286 ; retenues = 24585 ; sautées hors D5 = 5701
  « stress » : calendrier hors D5 = 13491 ; retenues = 11397 ; sautées hors D5 = 2094
  contrôle : retenues = n du bloc 3 ; sautées = ADR-0029 l.31 ; strate de chaque retenue = calendrier : égaux
  empreinte : sha256 de la chaîne de 46468 caractères (c calme retenue, s stress retenue, - non retenue) = <64 hex>
  lacunes : <m> suites maximales de positions non retenues, plage D5 comprise, en ordre croissant
  lacune j = <a> à <b> : <b − a + 1> positions (calme <x>, stress <y>)
```

Les nombres de la portée et des comptes sont les valeurs attendues, contrôlées à l'exécution (refus P2/masque sinon) :
46 468 positions ; D5 de j = 41 718 à 44 408 ; calendrier 32 068 et 14 400 ; D5 1 782 et 909 ; hors D5 30 286 et 13 491 ;
sautées 5 701 et 2 094, total 7 795 (l.31, l.39) [calc, recompte du rédacteur, égal au test de SB-10B l.148-161]. Le
« 5 707 » de RW-T4 l.87 est une coquille (T4 l.45, l.158) : 30 286 − 24 585 = 5 701 [calc].

### 2.3 `fiv_unites.txt` (FIV_u par hôte, strate et ℓ)

Série D_u(t) = 1 si la cellule (t, u) est classée PANNE, STALENESS ou HORS_ENVELOPPE (`r1.ECARTS`, égal au type « ecart » de
PS2 parametres.json l.75, contrôlé), par `r1._classify_window` sous les σ et τ committés de S2, sur le pool D1-bis de la
strate (`commun.classer`, appel d'EP), aux fenêtres retenues de la strate. Grille ℓ : les 17 valeurs de PS2 parametres.json
l.83 (1 à 1 440), celle de la calibration d'E1.

```
[FIV_u(ℓ)] série d'écart de l'hôte u (r1.ECARTS) sur les fenêtres retenues de la strate, pool D1-bis ; FIV_série = σ̂²_bloc/γ̂₀
  de r1.block_long_run_variance (forme d'EP) ; N = ℓ·n²·σ̂²_bloc et FIV exact = N/(ℓ·n·K·(n − K)) par l'estimateur du lot ;
  garde n ≥ 30·ℓ imprimée
  contrôle : K de chaque hôte = cellules « ecart » d'EP ; FIV_série de I_t (D1-bis) recalculée depuis les D_u = EP aux 17 ℓ ;
  estimateur exact et r1 : n et K égaux, écart relatif ≤ 10^-45 : égaux
  « <strate> » <flux> (hôte <h>) ℓ = <ℓ> : n = <n> ; K = <K> ; N = <entier> ; FIV exact = <p>/<q> ; FIV_série = <chaîne> ;
  σ̂²_bloc = <chaîne> ; γ̂₀ = <chaîne> ; garde : tenue|non tenue
```

Une ligne par (strate, hôte, ℓ) : 2 × 10 × 17 = 340 lignes [calc], dans l'ordre des strates, puis des hôtes de PS2
parametres.json l.40, puis de ℓ. Si K ∈ {0, n} : « FIV exact = indéfini » et « FIV_série = - » (forme de PS2 episodes.py
l.66), σ̂²_bloc et γ̂₀ tels que r1 les rend. Garde tenue en calme jusqu'à
ℓ = 720 (16 ℓ), en stress jusqu'à ℓ = 360 (14 ℓ) [calc]. Si Q-P2-10 (b) : section `[DIAGNOSTIC VOISINAGE]`, mêmes lignes
sur les positions retenues qui ne jouxtent aucune lacune, imprimée hors C1.

### 2.4 `intervalles.txt` (pauses entre épisodes, par hôte)

Segment = suite maximale de positions retenues consécutives (pas w) de la strate. Épisode et censure : définitions d'EP
(PS2 parametres.json l.74-81 ; PS2 episodes.py l.23-36). Pause = suite maximale de positions sans le type, entre deux
épisodes d'un même segment. Pause de bord = suite sans le type au début ou à la fin d'un segment (censurée). Types : panne
(PANNE) et écart (PANNE, STALENESS, HORS_ENVELOPPE).

```
[PAUSES] par hôte du pool D1-bis, strate et type ; segment, épisode, censure : définitions d'EP ; pause entre deux épisodes
  d'un même segment ; pause de bord censurée, comptée à part
  contrôle : épisodes recomptés = EP l.13-92 (n_s, cellules, épisodes, censurés, complets, max, P50, P90, P99,
  histogramme) : égaux
  « <strate> » <flux> (hôte <h>) <type> : segments = <s> ; épisodes = <e> (complets <c>) ; pauses = <p> ; moyenne = <chaîne>
  ; max = <m> ; P50 = <x> ; P90 = <y> ; P99 = <z> ; pauses de bord = <b> (dont segments sans épisode <v>)
    histogramme des pauses (longueur×nombre) : <l1>×<k1> <l2>×<k2> …
    histogramme des pauses de bord (longueur observée×nombre) : …
    histogramme des épisodes complets (longueur×nombre) : …        (si Q-P2-11 b)
```

Une entrée par (strate, hôte, type) : 2 × 10 × 2 = 40 [calc]. Quantiles au rang le plus proche ⌈num·N/den⌉ (forme de PS2
regles.py l.12-16).

### 2.5 Précision des calculs exacts

- Comptes, longueurs, positions et numérateurs N : entiers. FIV exact : `Fraction` irréductible, écrite `p/q`.
- Chaînes décimales γ̂₀, σ̂²_bloc, FIV_série : celles de `r1.block_long_run_variance`, sous `r1.contexte_decimal()`
  (précision 50, ROUND_HALF_EVEN), FIV_série étant le quotient des deux valeurs publiées, forme d'EP. Les deux formes sont
  publiées ; le critère de C1 lit le FIV exact (réponse à l'observation 3 de T4 l.156).
- Moyennes : `Fraction(somme, compte)`, puis chaîne sous le même contexte (`commun.dec`).
- Égalité de contrôle entre r1 et l'estimateur du lot : n et K égaux ; |FIV_série − FIV exact| ≤ FIV exact × 10^-45, borne de
  deux quotients arrondis à 50 chiffres (forme de SB-10A l.159-171).
- Ni flottant, ni fonction de libm, ni puissance flottante ; empreinte du masque par `hashlib.sha256` de la chaîne ASCII.

## 3. Lien avec SIM-BIS

### 3.1 Ce que les sorties changent, et ce qu'elles ne changent pas

- **FIV_u** remplace, pour C1 seulement, la convention « point dont ln FIV(240) est le plus proche de la moyenne des logs de
  C0 et de C2 » (PROP l.197 ; SB-10C l.113-136), qui n'avait aucun ancrage (T4 l.114). Le modèle fournit déjà les séries par
  hôte : la réplication d'E1 rend l'état D*(u) = H(u) ∪ F(u, BTC) de chaque hôte (SB-10B l.90-102) ; le critère de C1 se
  calcule sur les **mêmes 200 réplications par point** que celui de C2, sans simulation de plus.
- **Le masque** remplace, dans le calendrier d'E1, les positions de la portée hors D5 (SB-10B l.72-87) par les positions
  retenues de S2 : EP a été calculée sur ces dernières, où une lacune ne forme aucune paire (SB-10A l.128-134) ; un modèle sur
  30 286 positions de calme en compte 5 701 de plus (T4 l.45 ; l.31). Le masque s'applique après génération : les processus
  des sources sont tirés sur toute la grille, puis masqués par strate [inféré, T2 l.40-43 ; à vérifier par la G2 du diff
  d'intégration].
- **Les pauses** n'entrent dans aucune sélection : elles servent au diagnostic du modèle à C1 et aux phrases de limite de
  SOURCES-LIMITES-1 (O-5).
- **Ce qui ne change pas** : la grille d'E1 (64 points), 200 réplications par point, le critère de C2 sur I_t contre EP,
  l'épinglage de la sortie d'E1 avant E2 et E3, et toute la suite du G0 de SIM-BIS.

### 3.2 Lettre proposée de l'ajout daté au G0 de SIM-BIS

À adjuger avec ce G0, avant l'exécution de PLAN-S2BIS-2 (Q-P2-07). Les crochets renvoient aux questions dont la réponse
fixe le texte.

> *Ajout daté du <date> (lot PLAN-S2BIS-2, G0 `docs/adr-0029/G0-lot-PLAN-S2BIS-2.md` ; avis SIM-T4, option B ; motif :
> constat du point 9 du rapport de la tranche 4, vu à la mesure de mise au point E-4 du 2026-10-05, et §3.2 de l'avis
> SIM-T4)* :
> (1) **C1** : dans chaque strate, point p de la grille d'E1 qui minimise Q₁(p) = Σ_u Σ_ℓ (ln F̄_u,p(ℓ) − ln F_u(ℓ))², somme
> sur les hôtes u du pool d'E1 (D1-bis) et sur les ℓ de la grille de calibration où la garde de `fiv_unites.txt` est tenue et
> où F_u(ℓ) est défini ; F_u(ℓ) = FIV exact de PLAN-S2BIS-2 ; F̄_u,p(ℓ) = moyenne exacte, sur les réplications définies parmi
> les 200 du point p (celles de C2), du FIV exact de la série D*(u) sur le masque mesuré ; logarithmes par `Decimal.ln` sous
> le contexte de r1 ; égalités au plus petit κ, puis τ_D, puis φ ; un point dont un F̄_u,p(ℓ) retenu est indéfini est écarté.
> La convention « milieu des logs de C0 et de C2 à ℓ = 240 » est retirée. [Q-P2-05]
> (2) **C2** : définition inchangée (critère sur ln FIV_série de I_t contre EP l.128-161) ; **C0** : inchangé (aucun régime).
> (3) **Calendrier d'E1** : positions présentes = masque des fenêtres évaluables de J28 versé par PLAN-S2BIS-2, empreinte
> contrôlée, au lieu des positions de la portée hors D5, pour C0, C1 et C2 ; le masque s'applique après génération. [Q-P2-04]
> (4) **Nature** : C1 est le groupement propre mesuré par hôte, déclaré **borne haute** (FIV_u porte aussi les artefacts de
> l'observateur unique de S2) ; C2 reste le cas le plus défavorable plausible.
> (5) **Durée** : [Q-P2-06 (b), recommandée] la règle du §3 de la proposition se lit au niveau C1 pour l'acte A-2 : A-2 est
> posé si W*(C1) > 16 ; si W*(C2) > 16 ≥ W*(C1), aucune question n'est posée, la durée écrite au paquet reste 16 semaines, la
> puissance à la cible y est imprimée aux trois niveaux et une phrase de limite nomme C2. [Q-P2-06 (a) : texte inchangé.]
> (6) **Contrôles et impressions** : SHOGEN-SIM-BIS-REGIME-FAISABILITE-1 sur C1 dès son épinglage ; SB-11 imprime, par strate
> et par hôte, les résidus ln F̄_u,C1(ℓ) − ln F_u(ℓ) aux ℓ retenus, le point qui minimiserait Q₁ pour cet hôte seul (diagnostic,
> jamais candidat), et la loi des pauses du modèle à C1 sur le masque, à côté de `intervalles.txt`.
> (7) **Ordre** : cet ajout est adjugé avant l'exécution de PLAN-S2BIS-2 ; E0 attend le versement de PLAN-S2BIS-2 et le diff
> de SIM-BIS qui lit ses sorties ; aucune exécution provisoire avec la C1 de la lettre d'E-S-38. Le texte d'E-S-38 reste tel
> quel.

### 3.3 Ce que deviennent C0 et C2

- **C0** (aucun régime) : même rôle (cellule N2, échelle des durées aux trois niveaux, AVIS l.22), même définition ; calculé
  sur le masque mesuré dans E1 ; il n'entre plus dans la définition de C1.
- **C2** : même définition, même rôle de garde-fou (N3 à portée longue, PROP l.289 ; P-cible à C2, AVIS l.22), désormais sur
  le masque. Il tombera vraisemblablement au bord de la grille (RW-T4 l.66 ; T2 l.285-291) : la limite de FIV-IDENTIF-1
  l'écrit, avec le calcul de dilution de T4 l.93-96 à refaire proprement (T4 l.96).
- **Durée** : sous la lettre actuelle, la durée déclarée est celle de C2 (G0-SIM l.13-14). L'avis du G0 avait prévu la suite :
  « SIM-PUISSANCE-BIS est rejouée sur le niveau que PLAN-S2BIS-2 permet de fixer » (AVIS l.23). L'option B réalise PLAN-S2BIS-2
  avant E1 : ce niveau est C1. D'où Q-P2-06, qui touche la lettre du G0 et l'ajout daté à l'ADR (l.399, pt 2 : « groupement
  au niveau C2 »).

### 3.4 Ordre

1. Adjudication de ce G0, de l'avis de l'advisor et de l'ajout daté du §3.2 (Q-P2-07), éventuellement après un cp-1 bref de
   l'ajout (Q-P2-13) ; ligne du lot ajoutée au G0 de vague (forme de `docs/adr-0029/G0-lots-S2BIS.md` l.25).
2. Sous-lots P2-0 à P2-7, G2 neuve à 100 %, corrections, commit par l'orchestrateur.
3. Répétition sur journaux synthétiques à l'échelle de S2 (E-P2-20).
4. Épinglage au JOURNAL (E-P2-21), puis un lancement détaché (E-P2-22).
5. Versement (E-P2-24) ; bloc d'annexe B ; entrée de l'inventaire D.1-bis (AVIS l.23).
6. Diff d'intégration de SIM-BIS (§3.5), commencé dès l'adjudication sur des sorties synthétiques de même forme ; puis E0,
   puis E1.

### 3.5 Lignes d'intégration côté SIM-BIS (hors de ce lot)

| ligne | contenu | taille [inféré] |
|---|---|---|
| lecteur | sorties de PLAN-S2BIS-2 lues sous deux épingles (`parametres.json` de SIM-BIS et `SHA256SUMS` de `docs/adr-0029/plan-s2bis-2/`), forme exigée ligne à ligne, rationnels exacts depuis `p/q`, contrôles (n et K de chaque hôte égaux à EP ; empreinte du masque) ; liste des dix hôtes du format, distincte du pool opérationnel (SHOGEN-SIM-BIS-POOL-EP-SEPARES-1, B.66 l.1096) | ≈ 60 à 90 |
| masque | présentes = calendrier de la strate moins les lacunes, dans `calib_fiv.calendrier_j28` ; empreinte recalculée égale | ≈ 30 à 40 |
| C1 | second critère et sélection (forme de `critere` et `selection`, SB-10C l.91-136) ; `e1.ell_c1` sans objet | ≈ 50 à 70 (T4 l.111 : ≈ 50) |
| impressions | résidus par hôte, meilleur point par hôte, loi des pauses du modèle (SHOGEN-SIM-BIS-SB11-IMPRESSIONS-1) | ≈ 20 à 30 |
| vecteurs croisés | test de `calib_fiv.courbe` sur `tests/vecteurs_fiv.json` de PLAN-S2BIS-2 (Q-P2-09) | ≈ 15 |

Total ≈ 180 à 250 lignes avec tests, un ou deux diffs avant E0. Coût de calcul en plus pour E1 : 65 points × 200 réplications
× 2 strates × 10 hôtes = 260 000 courbes de séries d'hôte, contre 26 000 courbes de I_t [calc] ; de l'ordre d'une heure de CPU de plus
[inféré], à mesurer par E-S-46.

## 4. Exigences numérotées

### 4.1 Cadre et frontière

| n° | exigence (testable) | rattachement |
|---|---|---|
| E-P2-01 | Code sous `scripts/plan-s2bis-2/` (README, `parametres.json`, `socle.py`, `estimateur.py`, `masque.py`, `fiv_unites.py`, `intervalles.py`, `lancer.sh`, `SHA256SUMS`, `tests/`) ; sorties sous `docs/adr-0029/plan-s2bis-2/` ; bibliothèque standard seule (R-8 sans objet) ; aucun fichier de `scripts/plan-s2bis/`, `scripts/sim-bis/` ni `s2-harness/` modifié (contrôle sur la liste des chemins de chaque diff) | patron ; Q-P2-01 ; B.58 l.970 |
| E-P2-02 | **Frontière** : les journaux scellés de S2 ne sont lus qu'**à `f35a70c`**, c'est-à-dire par les lecteurs du harnais extrait de ce commit (`git archive`, dossiers interdits exclus, forme de PS2 lancer.sh l.66-69), modules contrôlés contre les cinq épingles ; et **seulement par les scripts du lot**, lancés par `lancer.sh` sur ordre de l'orchestrateur. Aucun agent (worker, réviseur, advisor, orchestrateur) n'ouvre, ne liste, n'affiche ni ne copie un journal ; seuls leurs sha256 sont admis ; `raw.jsonl` est haché, jamais lu. Exception écrite au G0 du lot, dans la forme du G0 de PLAN-S2BIS l.18-20 | l.179, l.383 ; G0 de vague l.15 ; annexe D l.40 ; B.58 l.972 |
| E-P2-03 | **Réemploi épinglé** : `scripts/plan-s2bis/commun.py` chargé par chemin sous le nom `commun` après contrôle de son sha256 (`14920e87…`) ; `scripts/plan-s2bis/parametres.json` lu après contrôle du sien (`7e214864…`) ; segment, strates, pool D1-bis, classes, types d'épisodes, quantiles, grille ℓ, commit d'analyse, épingles du harnais, paquet et rendu en sont pris tels quels, jamais recopiés ; refus nommé sinon | Q-P2-01 |
| E-P2-04 | Entrées versées sous épingles : EP (`c0371ca5…`) et `docs/adr-0029/plan-s2bis/SHA256SUMS` (`f21f9293…`) ; le rendu J28 n'est lu que par `commun.controle`, qui n'en extrait que le bloc 3 (PS2 commun.py l.126-141), jamais affiché | forme d'E-S-02 (PROP l.136) ; G1-PS2 l.111 |
| E-P2-05 | **Variable de campagne** : refus si `SHOGEN_S2_CAMPAGNE_CONTROL` est posée, au lanceur et dans `socle` ; la garde de `socle` lit un environnement passé en argument, pour qu'aucun test Python ne pose la variable ; le seul test qui la pose est celui du lanceur, à une valeur fictive, dans son seul sous-processus (exception A-3 de PLAN-S2BIS, G2-PS2 l.31-34), écrite au G0 et au README | règle 3 de la fiche ; G2-PS2 l.170-172 |
| E-P2-06 | **Étiquette et en-tête** du §2.1 ; aucune heure, aucun hôte, aucune version dans une sortie | G0-lot-PLAN-S2BIS l.25 ; C-3 de G2-PS2 (l.42) |
| E-P2-07 | **Hygiène** : `TMPDIR` dans le dossier de travail ; partiels `.partiel` puis renommage, jamais `.jsonl` ; fixtures `*.jsonl` synthétiques écrites et lues par les seuls tests, sous `TMPDIR`, retirées à la fin, jamais affichées (forme d'E-5 de G1-PS2 l.109) ; 0 octet 92 dans les fichiers du lot ; `lancer.log` lu par lignes nommées seulement | B.58 l.971 ; consignes de gabarit (B.16) ; G2-PS2 l.157, l.173-175 |

### 4.2 Sorties et contrôles

| n° | exigence (testable) | rattachement |
|---|---|---|
| E-P2-08 | `masque_j28.txt` dans la forme du §2.2 | brief l.39 ; T4 l.45 ; Q-P2-04 |
| E-P2-09 | `fiv_unites.txt` dans la forme du §2.3 : 340 lignes, double calcul publié | PROP l.492-493 ; T4 l.111 ; Q-P2-02 |
| E-P2-10 | `intervalles.txt` dans la forme du §2.4 : 40 entrées | brief l.38 ; Q-P2-03, Q-P2-11 |
| E-P2-11 | **Contrôles fail-closed**, avant toute valeur : (a) bloc 3 (`commun.controle`) ; (b) masque : calendrier hors D5 = 30 286 et 13 491, retenues = n du bloc 3, sautées = 5 701 et 2 094 (l.31), strate de chaque retenue = strate du calendrier, aucune position de D5 retenue ; (c) pool D1-bis de chaque strate = les 10 hôtes d'EP l.8 ; (d) type écart du lot = `r1.ECARTS` ; (e) épisodes recomptés = EP l.13-92 (entiers) ; (f) courbe de I_t du pool D1-bis recalculée depuis les D_u = EP l.128-161 (chaînes) ; (g) estimateur exact et r1 : n et K égaux, écart relatif ≤ 10^-45. Un écart : refus nommé (§4.4), aucune valeur | PS2 commun.py l.144-160 ; PS2 episodes.py l.73-91 (forme) |
| E-P2-12 | Un refus ne recopie ni ligne de journal ni valeur : il nomme le code, la strate, l'hôte et ℓ | G2-PS2 l.157 (O-1) |
| E-P2-13 | Si Q-P2-10 (b) : diagnostic du voisinage, pré-déclaré (d = 1 ; bords de la portée comptés comme lacunes), imprimé, hors C1 | Q-P2-10 |
| E-P2-14 | Aucune autre sortie : ni z, ni mesure de co-occurrence, ni statistique de test | §1.4 ; AVIS l.23 |

### 4.3 Précision, déterminisme, identité bit à bit

| n° | exigence (testable) | rattachement |
|---|---|---|
| E-P2-15 | Précision du §2.5 | brief l.40 ; PROP l.207 ; SB-10A l.29-34 |
| E-P2-16 | **Déterminisme** : itérations triées ; aucun ensemble itéré pour produire une ligne ; sorties indépendantes de `PYTHONHASHSEED`, du dossier de travail et de l'ordre des fichiers | PROP l.206 (forme) |
| E-P2-17 | **Identité sur fixtures** : deux exécutions, `PYTHONHASHSEED` 0 et 1, sous Python 3.11, 3.12 et 3.13 (3.11 au moins : `hashlib.file_digest`, PS2 commun.py l.30) ; sorties égales à l'octet | PROP l.208 (forme) |
| E-P2-18 | **Identité sur les journaux** (Q-P2-08 b) : le lanceur fait deux passes A et B dans l'unique lancement, `PYTHONHASHSEED` 0 puis 1, sorties dans deux dossiers de travail ; sha256 égaux exigés avant que A soit copiée dans le dossier de sortie ; sinon code 5 et rien n'est versé | Q-P2-08 |

### 4.4 Refus nommés (E-P2-19)

| code | cause | où |
|---|---|---|
| P2/usage | arguments du lanceur (code 2) | lanceur |
| P2/variable | `SHOGEN_S2_CAMPAGNE_CONTROL` posée | lanceur ; `socle` |
| P2/sortie | dossier de sortie non vide ; extraction déjà présente | lanceur |
| P2/epingle | sha256 du `SHA256SUMS` du code différent de l'argument ; `sha256sum -c` en échec | lanceur |
| P2/paquet | sha256 du paquet de S2 différent de l'épingle ; bloc machine absent, multiple ou non fermé | lanceur |
| P2/journal | journal nommé absent, sha256 différent du bloc machine, ligne malformée | lanceur |
| P2/commit | commit du bloc machine différent du commit d'analyse | lanceur |
| P2/plan-s2bis | `commun.py`, `parametres.json`, EP ou `SHA256SUMS` de PLAN-S2BIS différents de l'épingle | lanceur ; `socle` |
| P2/harnais | module du harnais hors épingles ou de sha256 différent (`commun.importer_harnais`) | `socle` |
| P2/parametres | schéma de `parametres.json` du lot (clés exactes, aucun flottant) | `socle` |
| P2/coherence | bloc 3 recompté différent de l'épingle | `socle` |
| P2/masque | contrôle (b) d'E-P2-11 | `masque.py` |
| P2/pool | contrôle (c) | scripts |
| P2/ecarts | contrôle (d) | `socle` |
| P2/ep | contrôles (e) et (f) | `fiv_unites.py` ; `intervalles.py` |
| P2/r1 | contrôle (g) | `fiv_unites.py` |
| P2/entree | entrée d'une fonction pure (masques, ℓ, listes) | `estimateur.py` |
| P2/identite | passes A et B différentes (code 5) | lanceur |

Codes : lanceur 0 (trois scripts en 0, A = B), 2 usage, 3 refus avant tout lancement, 4 extraction impossible, 5 un script
hors 0 ou A ≠ B (forme de PS2 lancer.sh l.16) ; scripts 0 ou 1, en-tête et une ligne de refus, aucune valeur.

### 4.5 Épinglage, exécution, versement

| n° | exigence (testable) | rattachement |
|---|---|---|
| E-P2-20 | **Répétition** avant l'épinglage, par le worker : tout le lanceur sur journaux synthétiques à l'échelle de S2 (forme de G1-PS2 l.98-101 : environ 39 000 fenêtres, extraction réelle de `f35a70c`), durée et mémoire mesurées, plan de lancement écrit au G1 | G1-PS2 l.98-101 |
| E-P2-21 | **Épinglage au JOURNAL avant toute lecture** : après la G2 et ses corrections, l'orchestrateur inscrit au JOURNAL le sha256 de chaque fichier de `scripts/plan-s2bis-2/` et celui de son `SHA256SUMS` ; le lanceur reçoit ce dernier en argument et refuse s'il diffère ou si `sha256sum -c` échoue ; aucune lecture des journaux avant cette inscription | SHOGEN-POSTPREREG-PARAMS-SCEAU-1, règle maintenue (B.58 l.965) ; G0-lot-PLAN-S2BIS l.21-22 |
| E-P2-22 | **Exécution unique par l'orchestrateur** : un lancement détaché (`setsid nohup`, PID et fichier de sortie consignés, fin constatée en sondant le PID ; délai explicite si tâche de fond), dossier de sortie absent ou vide, dossier de travail neuf ; le lanceur n'affiche que des noms, des codes et des sha256 | PS2 README l.42-51 ; consigne « tâches longues » (B.16) |
| E-P2-23 | **Seconde lecture** : un lancement sans code 0 n'a pas de résultat. Un second lancement est une déviation déclarée (motif, correctif relu en G2, nouvelles épingles au JOURNAL, mention à l'annexe B), jamais silencieuse ; un lancement coupé par une borne de temps se refait et ne se compte pas | PROP l.138 (forme) ; B.16 |
| E-P2-24 | **Versement** : sur code 0, l'orchestrateur verse les trois sorties et leur `SHA256SUMS` dans `docs/adr-0029/plan-s2bis-2/`, avec un README (heures de production, entrée du JOURNAL, sha256 du `SHA256SUMS` du code, commit d'analyse), le G1 et le G2 ; puis le bloc d'annexe B, l'entrée de l'inventaire D.1-bis et la ligne JOURNAL | PS2 README des sorties (forme) ; AVIS l.23 |
| E-P2-25 | **Exposition** : sorties de classe M, valeurs de S2 post-rendu ; les rôles qui les lisent le déclarent dans leur attestation D.3 ; aucune donnée de S2-bis n'existe | AVIS l.23 ; T4 l.131 |

### 4.6 Tests

| n° | exigence (testable) | rattachement |
|---|---|---|
| E-P2-26 | Tests d'abord, sur fixtures synthétiques seulement (D.4 a) ; valeurs de référence indépendantes du code : à la main, `sha256sum`, `bc`, comptage naïf, `scripts/plan-s2bis/episodes.py` épinglé ; rouge montré avant le vert ; une mutation nommée par test | règle 4 de la fiche |
| E-P2-27 | Mutants classés par la sortie du runner : 0 vivant, 1 tué, 3 ou toute autre sortie FATAL ; campagne relancée après correction | SHOGEN-MUT-FATAL-1 (B.16) |
| E-P2-28 | Suites : `scripts/plan-s2bis-2` verte à chaque sous-lot ; `scripts/plan-s2bis`, `scripts/sim-bis` et `s2-harness` (405 tests, OK, skipped=2, PROP l.229) inchangées et vertes | règle 4 de la fiche |
| E-P2-29 | Oracle croisé avec `calib_fiv.py` selon Q-P2-09 | brief l.50 |

## 5. Sous-lots, tests attendus, mutants

### 5.1 Sous-lots (≤ 200 lignes ajoutées chacun, tests et données compris)

| sous-lot | objet | taille | dépend de |
|---|---|---|---|
| P2-0 | socle : `parametres.json` (clés propres, chacune avec sa source : épingles de PLAN-S2BIS, comptes de l.31, tolérance 10^-45, voisinage, passes) ; `socle.py` (garde de la variable sur un environnement passé en argument, chargement épinglé de `commun.py` et des paramètres de PLAN-S2BIS, schéma, refus nommés, CLI, en-tête, écriture `.partiel` puis renommage) ; `tests/__init__.py`, `test_socle.py` | ≈ 190 | — |
| P2-1 | `masque.py` : positions, calendrier par le harnais, lacunes, empreinte, contrôle (b) ; tests | ≈ 150 | P2-0 |
| P2-2 | `estimateur.py` I : FIV exact sur masques entiers (numérateur entier, forme de SB-10A l.50-79), contrôle des entrées ; tests | ≈ 150 | P2-0 |
| P2-3 | `estimateur.py` II : segments, épisodes et censure, pauses, quantiles au rang le plus proche, histogrammes ; tests | ≈ 160 | P2-0 |
| P2-4 | `fiv_unites.py` : séries D_u, chemin r1, double calcul, contrôles (c), (d), (f), (g), diagnostic du voisinage ; tests | ≈ 190 | P2-1, P2-2 |
| P2-5 | `intervalles.py` : contrôle (e), pauses, épisodes complets ; tests | ≈ 170 | P2-3 |
| P2-6 | `lancer.sh` (forme de PS2 lancer.sh : contrôles d'entrée, épingle en argument, épingles de PLAN-S2BIS, extraction, trois scripts, passes A et B, sommes) ; tests I | ≈ 190 | P2-1, P2-4, P2-5 |
| P2-7 | tests du lanceur II ; identité (T-P2-DET-1) ; vecteurs croisés (`tests/vecteurs_fiv.json`, T-P2-ORA-1) ; job CI si Q-P2-12 (a) | ≈ 170 | P2-6 |

Total ≈ 1 370 lignes [inféré], dont un noyau d'analyse (estimateur et trois scripts, sans tests) d'environ 300 lignes : c'est
lui que visaient les ≈ 150 lignes de l'item. L'estimation part d'un réalisé (PLAN-S2BIS, 1 477 lignes en 9 diffs, G1-PS2
l.43-51), non d'un multiple ; le rapport réalisé sur estimé de SIM-BIS vaut × 2,28 sur sa tranche 4 (RW-T4 l.127), d'où la
fourchette 1 100 à 1 400. Une seule partie, une G2 neuve à 100 % à la fin (forme de PLAN-S2BIS).

### 5.2 Tests attendus (fixtures synthétiques seulement ; valeurs de référence indépendantes du code)

| test | valeur de référence | mutant qu'il doit tuer |
|---|---|---|
| T-P2-SOC-1 épingles | sha256 de `commun.py` et de `parametres.json` de PLAN-S2BIS par `sha256sum` ; une copie altérée d'un octet : P2/plan-s2bis | M-P2-01 contrôle retiré |
| T-P2-SOC-2 variable | environnement passé en argument avec la variable : P2/variable ; sans : aucun refus | M-P2-02 garde retirée |
| T-P2-SOC-3 sous-arbres | valeurs recopiées à la main : t0 = 1787770800, n fixe 38 600, D5 [1790273880 ; 1790435280], 10 hôtes, 17 ℓ ; égales à ce que lit `socle` | M-P2-03 sous-arbre pris aux paramètres du lot au lieu de ceux de PLAN-S2BIS |
| T-P2-MAS-1 lacunes | journaux synthétiques du mercredi 19:00 au samedi, une fenêtre absente, une plage exclue de trois positions : lacunes, comptes, chaîne c/s/- écrite à la main, sha256 par `printf`, puis `sha256sum` | M-P2-04 borne haute de la plage exclue ; M-P2-05 lacunes contiguës non fusionnées |
| T-P2-MAS-2 portée réelle | sans journal, depuis EP l.6 : 46 468 positions ; 32 068 et 14 400 ; 1 782 et 909 ; 30 286 et 13 491 (deux sources : `calc_p2.py` du rédacteur et le test de SB-10B l.148-161) | M-P2-06 jour pris en heure locale ; M-P2-07 premier jour partiel ignoré |
| T-P2-MAS-3 fail-closed | retenues différentes du n du bloc 3 dans une fixture : P2/masque, aucune valeur | M-P2-08 contrôle (b) retiré |
| T-P2-FIV-1 à la main | I = 1, 1, 0, 0 : N = 16, 40, 48 ; FIV 1, 5/4, 1 (PS2 tests/test_episodes.py l.36-44 ; SB-10A l.118-126) | M-P2-09 poids 1 − (k + 1)/ℓ |
| T-P2-FIV-2 lacune | positions 0, 1, 3, 4 ; I = 1, 1, ·, 0, 0 : FIV(2) = FIV(3) = 3/2 ; N = 48 et 72 (SB-10A l.128-134) | M-P2-10 série comprimée (paires à travers la lacune) |
| T-P2-FIV-3 naïf | 300 séries aléatoires à lacunes, ℓ de 1 à 9 : FIV exact égal au comptage naïf des γ̂_k en `Fraction` | M-P2-11 paires comptées sur les seules positions à 1 |
| T-P2-FIV-4 r1 | journaux synthétiques : chaînes de `r1.block_long_run_variance` (harnais extrait) égales à celles que donne N exact, pour chaque (strate, hôte, ℓ) | M-P2-12 contexte décimal par défaut (28 chiffres) |
| T-P2-FIV-5 contre EP | journaux synthétiques portant au moins une cellule périmée : `scripts/plan-s2bis/episodes.py` (épinglé) produit dans le test une sortie de la forme d'EP ; contrôles (e) et (f) égaux ; un chiffre altéré : P2/ep | M-P2-13 contrôle (f) neutralisé ; M-P2-32 FIV_u sur le type panne |
| T-P2-EPI-1 épisodes | positions 0 à 9, la 5 absente, vrai en 0, 1, 2, 4, 6, 7, 9 : (3, censuré à gauche), (1, à droite), (2, à gauche), (1, à droite) (PS2 tests/test_episodes.py l.19-24) | M-P2-14 suite comprimée |
| T-P2-EPI-2 contre EP | journaux synthétiques : entiers recomptés égaux à la sortie d'`episodes.py` épinglé | M-P2-15 censure à droite non comptée |
| T-P2-INT-1 pauses | segment [0 ; 11] vrai en 2, 3 et 7 ; lacune en 12 ; segment [13 ; 16] sans épisode : pause complète 3 (positions 4 à 6) ; pauses de bord 2 (0-1), 4 (8-11), 4 (13-16), dont un segment sans épisode | M-P2-16 pause coupée par une lacune comptée complète |
| T-P2-INT-2 résumé | pauses 1, 2, 2, 7 : moyenne 3, P50 = 2, P90 = 7, P99 = 7, max 7 (rang ⌈num·N/den⌉) | M-P2-17 moyenne en flottant ; M-P2-18 quantile interpolé |
| T-P2-OUT-1 sortie | étiquette mot pour mot ; en-tête : sha256 de chaque module chargé et des deux `parametres.json` ; trois lignes d'une fixture écrites à la main | M-P2-19 un module absent de l'en-tête |
| T-P2-DET-1 identité | deux exécutions sur fixtures, `PYTHONHASHSEED` 0 et 1, Python 3.11 à 3.13 : sorties égales à l'octet | M-P2-20 itération sur un ensemble |
| T-P2-LAN-1 à 9 lanceur | forme de PS2 tests/test_lancer.py, plusieurs cas par test : lancement complet (code 0 ; écran fait de noms, de codes et de sha256 seuls), dossiers interdits non extraits, épingle en argument, paquet, bloc double ou non fermé, journal, commit, variable (exception A-3), sortie non vide, usage (2), extraction impossible (4), script en échec (5), A ≠ B (5) | M-P2-21 à M-P2-30, un contrôle retiré par mutant : variable, sortie, épingle, paquet, bloc, journal, commit, exclusions de l'extraction, code d'un script en échec, comparaison A et B |
| T-P2-ORA-1 vecteurs | `tests/vecteurs_fiv.json`, ≈ 40 vecteurs (lacunes, K = 0, K = n, n = 0, ℓ ≤ 9) : numérateurs du fichier égaux au comptage naïf et à l'estimateur du lot | M-P2-31 un numérateur du fichier altéré |

Mutant de spécification sans oracle propre, déclaré : pause de bord confondue avec une pause complète quand le segment ne
porte qu'un épisode (relu en G2 ; T-P2-INT-1 en couvre la forme générale).

## 6. Oracles

1. **r1 extrait de `f35a70c`** : au code (T-P2-FIV-4, T-P2-FIV-5) et à l'exécution (contrôles (f) et (g)). Le contrôle (f) lie
   le lot à la courbe publiée par PLAN-S2BIS, elle-même contrôlée contre `compute_r1` à ℓ = 240 (PS2 episodes.py l.73-91).
2. **Comptages naïfs** : γ̂_k par leur définition, en `Fraction` (T-P2-FIV-3, T-P2-ORA-1 ; forme de SB-10A l.107-114) ;
   épisodes, pauses et lacunes à la main (T-P2-EPI-1, T-P2-INT-1, T-P2-MAS-1).
3. **`calib_fiv.py` de SB-10** (tranche 4, non commis ; Q-P2-09) : les deux estimateurs suivent la même formule (SB-10A
   l.50-57). L'oracle passe par le fichier de vecteurs, relu des deux côtés, et par un passage ad hoc du réviseur G2 sur une
   copie `git archive 5f99ab5` où SB-10A à SB-10C sont appliqués (résultat au G2). Aucune dépendance de code entre les lots.
4. **PLAN-S2BIS** : `episodes.py` épinglé, sur journaux synthétiques (T-P2-FIV-5, T-P2-EPI-2) ; EP à l'exécution
   (contrôles (e) et (f)).
5. **ADR** : sautées 5 701 et 2 094 (l.31) ; calendrier recompté par deux sources (T-P2-MAS-2).
6. **Modèle d'E1** (dans SIM-BIS, après versement) : sous C0, FIV_u du modèle voisin de 1 aux grands ℓ ; résidus par hôte
   imprimés à C1 (§3.2 pt 6). Diagnostic, non sélection.

## 7. Questions techniques (adjudication : orchestrateur ; advisors désignés)

- **Q-P2-01 Emplacement et réemploi.** (a) dossiers neufs ; `scripts/plan-s2bis/` réemployé par chemin et sha256, jamais
  modifié ; (b) scripts ajoutés à `scripts/plan-s2bis/` et lanceur étendu : change les fichiers d'un lot exécuté et épinglé,
  déclenche SHOGEN-PLAN-S2BIS-GARDES-1 (B.58 l.970), mêle deux épinglages dans un dossier ; (c) dossiers neufs, chemin de
  lecture recopié : deux implémentations du même chemin, dont une seule a produit EP. **Recommandé : (a).** [orchestrateur]
- **Q-P2-02 Série de FIV_u.** (a) type écart, D_u = 1{`r1.ECARTS`} : la série dont I_t compte les coïncidences et que la
  réplication d'E1 simule (D* = H ∪ F, SB-10B l.90-102) ; (b) type panne en plus : redondant (écart − panne ≤ 3 cellules par
  hôte et par strate [calc, EP l.13-92]) ; (c) « écarts isolés » (D_u hors des fenêtres où un autre hôte est en écart), qui
  retirerait les modes communs de l'observateur : lit des co-occurrences, hors classe M (AVIS l.23). **Recommandé : (a)** ;
  (b) et (c) écartées par écrit. [STATS]
- **Q-P2-03 Pauses.** (a) pause = suite sans le type entre deux épisodes d'un même segment de positions retenues
  consécutives ; pauses de bord censurées, comptées et décrites à part ; sur la grille, comme les épisodes d'EP (PS2
  parametres.json l.78-79) et comme l'estimateur, où une lacune ne forme aucune paire ; (b) intervalle de début à début ;
  (c) pauses sur la suite comprimée : fusionne à travers les lacunes, ce que M-10-03 refuse pour le FIV (SB-10A l.128-132).
  **Recommandé : (a)**, types panne et écart. Limite écrite : les pauses complètes penchent vers les courtes (une longue pause
  est plus souvent coupée) ; SIM-BIS compare le modèle passé par le même masque, jamais une loi corrigée. [STATS]
- **Q-P2-04 Masque et E1.** (a) le masque mesuré remplace les positions de la portée hors D5 pour C0, C1 et C2 ; (b) pour C1
  seulement ; (c) masque imprimé, E1 inchangée. **Recommandé : (a)** : EP est calculée sur les fenêtres retenues ; la limite
  Q-T4-5 se ferme (T4 l.45) ; [G0] sur E-S-38 (calendrier), écrit au §3.2 pt 3. [STATS ; orchestrateur]
- **Q-P2-05 Critère de C1.** (a) lettre de T4 l.111 : un point commun aux hôtes, Q₁ non pondéré, ℓ à garde tenue, hôtes à F_u
  défini ; (b) Q₁ pondéré par K_u ; (c) un point par hôte : le générateur prendrait un régime par hôte (`sources.Replication`
  en change, dix points par strate). **Recommandé : (a)**, avec en diagnostic le point qui minimiserait chaque hôte seul.
  Motifs : même forme que le critère de C2 (SB-10C l.91-104) ; aucun poids choisi après lecture ; (b) donnerait à binance,
  bitstamp et defillama 1 006 des 1 387 cellules d'écart du calme [calc, EP l.15, l.23, l.39] ; (c) est plus fidèle mais change
  le générateur et la forme des cellules alors qu'E0 attend. Limite écrite : okx (6 cellules) et coinbase (11) en stress
  (EP l.91, l.71) pèsent autant que binance. [G0] [STATS]
- **Q-P2-06 Rôle de C2 et durée déclarée.** (a) lettre de l'adjudication 2 : durée déclarée = celle de C2, A-2 si
  W*(C2) > 16 ; le recours « PLAN-S2BIS-2 avant A-2 » est accompli ; (b) suite écrite de l'avis (AVIS l.23 : « SIM-PUISSANCE-BIS
  est rejouée sur le niveau que PLAN-S2BIS-2 permet de fixer » ; T4 l.114) : la durée pour A-2 se lit à C1 ; si
  W*(C2) > 16 ≥ W*(C1), la durée écrite au paquet reste 16 semaines sans question, la puissance à 16 semaines est imprimée aux
  trois niveaux et une phrase de limite nomme C2 ; A-2 si W*(C1) > 16. **Recommandé : (b)** : « aucun allongement n'est
  demandé sur un artefact de calibration » (G0-SIM l.15) ; C2 garde son rôle de garde-fou imprimé (N3, P-cible à C2). [G0]
  (G0-SIM l.13-14) ; [ADR] (ajout daté l.399, pt 2) ; [INV] information à l'accord A-1 de S-2 (forme de T4 l.126).
  [orchestrateur ; STATS]
- **Q-P2-07 Moment de l'ajout daté.** (a) avant E0 (T4 l.114, l.148) ; (b) avant l'exécution de PLAN-S2BIS-2, adjugé avec ce
  G0. **Recommandé : (b)** : aucune valeur de FIV_u n'existe aujourd'hui ; écrire le critère de C1, l'entrée du masque et la
  règle de durée avant de les calculer est le seul ordre qu'un tiers ne peut pas lire comme un réglage après coup (des FIV de
  modèle ont déjà été vus à la mise au point E-4, T4 l.132-137) ; coût nul. [orchestrateur]
- **Q-P2-08 Identité bit à bit sur les journaux.** (a) une passe ; identité montrée sur fixtures et sur la répétition ;
  (b) deux passes A et B (`PYTHONHASHSEED` 0 et 1) dans l'unique lancement, sha256 comparés avant tout versement.
  **Recommandé : (b)** : PLAN-S2BIS a fait lire les journaux par trois scripts dans un seul lancement (PS2 lancer.sh l.74-79) ;
  « une exécution » s'entend d'un lancement ; coût de l'ordre de quelques minutes [inféré : 87 s pour trois scripts, B.58
  l.961]. Si l'orchestrateur lit « les lisent une fois » (brief l.29) comme une lecture par script : (a). [orchestrateur]
- **Q-P2-09 Oracle avec `calib_fiv.py` non commis.** (a) fichier de vecteurs croisés commis par ce lot (attendus par comptage
  naïf), relu par un test de SIM-BIS au diff d'intégration ; (b) test de ce lot qui importe `calib_fiv` dans un sous-processus :
  collision de nom `commun`, dépendance à un fichier encore révisable ; (c) passage ad hoc du réviseur G2 sur SB-10A à SB-10C
  appliqués à une copie. **Recommandé : (a) et (c).** [orchestrateur]
- **Q-P2-10 Artefact de censure en stress** (§0 pt 9). (a) limite écrite seule ; (b) diagnostic pré-déclaré : FIV_u recalculé
  après retrait des positions voisines (d = 1) d'une lacune, bords de la portée comptés comme lacunes, imprimé hors C1 ; (c) (b)
  employé pour C1 en stress. **Recommandé : (b)** : il chiffre la part de FIV_u liée aux absences de l'observateur, dont la
  limite « borne haute » a besoin ; (c) changerait le critère sur une hypothèse non testée. Coût ≈ 15 lignes et 340 lignes de
  sortie [inféré]. [STATS]
- **Q-P2-11 Histogramme des épisodes complets.** (a) non produit ; (b) produit (même balayage), pour chiffrer les limites
  d'E-S-10 et de STRESS-EPISODES-1, SB-3 inchangé ; (c) produit, et SB-3 passe à la loi des épisodes complets.
  **Recommandé : (b)** : c'est le recours qu'écrit le G0 de SIM-BIS (G0-SIM l.33, pt 2) ; (c) changerait le générateur pour
  un écart de moyennes de −0,035 à +0,134 fenêtre en calme (même ligne), du second ordre. [STATS]
- **Q-P2-12 CI.** (a) job `plan-s2bis-2-unittest` calqué sur `sim-bis-unittest` (`gates.yml` l.220-242), historique complet,
  harnais extrait par les tests eux-mêmes (forme d'`oracle_r1`, RW-T4 l.25) ; (b) tests rejoués par l'orchestrateur seul
  (forme de PLAN-S2BIS). **Recommandé : (a)** : on serre, et le code reste au dépôt comme preuve rejouable ; ≈ 30 lignes ; le
  cas K-02 du runner est à étendre (SHOGEN-CI-S2-CABLAGE-1, cité PROP l.571). [orchestrateur]
- **Q-P2-13 cp-1.** (a) G2 neuve seule (forme de PLAN-S2BIS) ; (b) en plus, cp-1 bref de l'ajout daté du §3.2 par un
  validateur frais, puisqu'il touche la durée déclarée et, par Q-P2-06 (b), un ajout daté de l'ADR. **Recommandé : (b)**, pour
  l'ajout seul. [orchestrateur]

**Advisors proposés** : STATS : Q-P2-02, Q-P2-03, Q-P2-04, Q-P2-05, Q-P2-06, Q-P2-10, Q-P2-11 ; l'orchestrateur seul :
Q-P2-01, Q-P2-07, Q-P2-08, Q-P2-09, Q-P2-12, Q-P2-13 ; l'orchestrateur avec STATS : Q-P2-04 et Q-P2-06.

## 8. Écarts à la lettre, signalés et non appliqués

| où | lettre | écart proposé | question |
|---|---|---|---|
| B.61 l.1022 | FIV-IDENTIF-1 déclenché par « W* différente entre C0 et C2 » | lot avancé avant E0 (option B), par décision datée de l'orchestrateur | brief l.16-20 ; T4 l.111 |
| B.61 l.1022 | « ≈ 150 lignes » | ≈ 1 100 à 1 400 lignes au patron complet | §5.1 |
| PROP l.197 (E-S-38) | C1 = point le plus proche du milieu des logs de C0 et C2 à ℓ = 240 | C1 calibré sur FIV_u | Q-P2-05 |
| PROP l.197 (E-S-38) | calendrier « portée et plage D5 d'EP l.6 » | masque mesuré | Q-P2-04 |
| G0-SIM l.13-14 ; l.399 pt 2 | durée déclarée = celle de C2 ; groupement au niveau C2 | durée pour A-2 lue à C1, C2 imprimé | Q-P2-06 |
| T4 l.114 | ajout daté « avant E0 » | avant l'exécution de PLAN-S2BIS-2 | Q-P2-07 |
| brief l.29 | les scripts lisent les journaux « une fois » | deux passes A et B dans un seul lancement | Q-P2-08 |

## 9. Calendrier

| étape | contenu | durée [inféré] |
|---|---|---|
| 0 | avis de l'advisor sur ce G0 ; adjudication : G0 du lot, ajout daté au G0 de SIM-BIS (§3.2), ligne au G0 de vague ; cp-1 bref de l'ajout si Q-P2-13 (b) | 1 à 2 h |
| 1 | P2-0 à P2-7, worker `claude-opus-5-5` effort max | 1 à 2 h (PLAN-S2BIS : 9 diffs en 51 min, G1-PS2 l.3 ; SIM-BIS T4 : 7 diffs en 1 h 24, RW-T4 l.10) |
| 2 | G2 neuve à 100 %, corrections, contre-contrôle, commits par l'orchestrateur | 1 à 2 h |
| 3 | répétition, épinglage au JOURNAL, lancement, versement | ≈ 0,5 h (PLAN-S2BIS : lancement de 87 s, B.58 l.961 [calc]) |
| total | | ≈ 4 à 6 h de session |

- **En parallèle** : SB-11 à SB-13 (8 à 10 diffs, RW-T4 l.129-136) et leur G2 ; le diff d'intégration de SIM-BIS (§3.5)
  peut commencer dès l'adjudication, sur des sorties synthétiques de la forme du §2.
- **E0** attend le versement de PLAN-S2BIS-2, le diff d'intégration et SB-11. PLAN-S2BIS-2 n'allonge le chemin critique que
  s'il dure plus que SB-11 [inféré] ; versement possible au plus tôt le 2026-10-05 au soir, plus vraisemblablement le
  2026-10-06 [inféré, à partir de 13:55 UTC le 2026-10-05].

## 10. Risques

1. **Échec fermé après la lecture** : un contrôle d'E-P2-11 qui échoue sur les vrais journaux force une seconde lecture, donc
   une déviation (E-P2-23). Parade : chaque contrôle est éprouvé sur fixtures contre le code épinglé de PLAN-S2BIS (T-P2-FIV-5,
   T-P2-EPI-2) et sur la répétition à l'échelle ; tolérance de 10^-45 en relatif plutôt qu'égalité de chaînes pour (g).
2. **Artefact de l'observateur dans FIV_u** (§0 pt 9) : si les FIV_u de stress sont faits des pannes voisines des lacunes, la
   C1 de stress l'est aussi. Parade : C1 déclarée borne haute ; diagnostic du voisinage (Q-P2-10) ; C2 garde-fou ; limite
   écrite (§11).
3. **Hôtes à peu d'écarts** : okx (6 cellules) et coinbase (11) en stress pèsent autant que binance dans Q₁ (Q-P2-05 a).
   Parade : critère écrit avant le calcul ; résidus et meilleur point par hôte imprimés ; limite écrite.
4. **Taille** : ≈ 1 100 à 1 400 lignes contre ≈ 150 annoncées. Parade : le noyau reste petit, le patron se reprend de
   PLAN-S2BIS ; SHOGEN-S2BIS-P1-ESTIMATION-1 reçoit le chiffre mesuré à la clôture.
5. **`calib_fiv.py` non commis et encore en revue** : l'oracle croisé passe par un fichier de vecteurs, jamais par un import
   (Q-P2-09) ; item neuf (§11).
6. **E0 qui attend** : la tentation serait de lancer l'exécution provisoire avec l'ancienne C1 (T4 l.116) ; l'ajout daté
   l'interdit (§3.2 pt 7).
7. **Critère écrit après la vue des données** : il serait lu comme un réglage. Parade : Q-P2-07 (b).
8. **Bornes de temps** : lancement détaché, délai explicite ; la répétition mesure la durée et la mémoire (E-P2-20).

## 11. Items (règle PAROXYSME)

| item | constat | construction | prix [inféré] | déclencheur |
|---|---|---|---|---|
| SHOGEN-SIM-BIS-FIV-IDENTIF-1 (existant, B.61 l.1022) | précisé : construction avancée (option B) ; reste ouvert jusqu'à C1 épinglée par E1 et sa limite écrite : « sous indépendance, aucune famille de régimes propres n'atteint la courbe de S2 à taux d'écart réalistes » (T4 l.96), C1 borne haute | ce lot, puis le diff d'intégration de SIM-BIS | ce lot | remplacé par « sortie d'E1 épinglée » |
| SHOGEN-SIM-BIS-SOURCES-LIMITES-1 (existant, B.64 l.1070) | trois limites de plus : (i) C1 borne haute, FIV_u porte les artefacts de l'observateur unique ; (ii) en stress, 453 des 674 épisodes d'écart jouxtent une fenêtre non retenue, ce que le générateur, aux pannes indépendantes du masque, ne reproduit pas ; (iii) pauses complètes penchées vers les courtes par la censure des segments | phrases au paquet (SB-12), chiffrées par les sorties du lot | aucun | phrases de limite (SB-12) |
| SHOGEN-PLAN-S2BIS-2-ORACLE-CALIB-1 (neuf) | l'oracle de FIV_u contre `calib_fiv.py` n'est possible qu'au commit de SB-10, encore en revue ; aucun import entre les lots | fichier de vecteurs ; test côté SIM-BIS au diff d'intégration ; passage ad hoc en G2 | ≈ 15 lignes dans SIM-BIS | commit de SB-10, puis diff d'intégration |
| SHOGEN-SIM-BIS-SB11-IMPRESSIONS-1 (existant, B.64 l.1069) | précisé : résidus de C1 par hôte, meilleur point par hôte (diagnostic), loi des pauses du modèle à C1 | impressions | ≈ 20 à 30 lignes | brief de SB-11 |
| SHOGEN-SIM-BIS-REGIME-FAISABILITE-1 (existant, B.64 l.1067) | précisé : s'applique au point C1 mesuré (T4 l.116) | un calcul | aucun | épinglage de C1 |
| SHOGEN-SIM-BIS-POOL-EP-SEPARES-1 (existant, B.66 l.1096) | précisé : le lecteur des sorties de PLAN-S2BIS-2 lit la liste des dix hôtes du format, jamais le pool opérationnel | séparation des deux listes | compris dans le diff d'intégration | diff d'intégration |
| SHOGEN-SIM-BIS-SB11-BRIEF-1 (existant, B.66 l.1097) | précisé : ligne due au brief de SB-11, l'ordre « PLAN-S2BIS-2 versée, ajout daté, E0, E1 » (T4 l.148) et l'interdit d'une exécution provisoire avec l'ancienne C1 (T4 l.116) | ligne de brief | aucun | brief de SB-11 |
| SHOGEN-SIM-BIS-STRESS-EPISODES-1 (existant, B.61 l.1029) | précisé si Q-P2-11 (b) : limite chiffrée sur les épisodes complets mesurés | phrase | aucun | sortie d'E1 |
| SHOGEN-S2BIS-P1-ESTIMATION-1 (existant, B.61 l.1018) | s'applique à ce lot (≈ 150 contre ≈ 1 100 à 1 400) | une ligne à la clôture | aucun | clôture du lot |
| SHOGEN-LECTEUR-INDEP-1 (existant, G2-PS2 l.182) | la limite s'étend à ce lot (lecteurs du harnais réemployés) | aucune | aucun | — |

Consignes appliquées sans item neuf : SHOGEN-WORKER-TMPDIR-1, SHOGEN-PLAN-S2BIS-LOG-1, SHOGEN-PLAN-S2BIS-VARIABLE-TEST-1,
SHOGEN-FICHE-WORKER-POSTEXEC-2 (l'exception reste écrite au G0 du lot). Aucune limite rencontrée n'est laissée sans item.

## 12. Actes de l'investisseur (en langage clair)

- **Aucun acte neuf, aucune dépense** : le lot tourne sur l'hôte de session et ne lit que des données de S2 déjà closes.
- **Information, à l'accord de la partie S-2 de SIM-BIS** (forme de T4 l.126) : « Le simulateur ne reproduit pas, avec des
  sources indépendantes, le regroupement des pannes vu en S2 ; ce regroupement venait surtout du point d'observation unique.
  Nous mesurons maintenant, sans dépense, sur les journaux de S2, le regroupement propre à chaque source. »
- **Si Q-P2-06 (b) est adoptée** : « On ne vous demandera pas d'allonger la campagne sur la seule base de l'hypothèse la plus
  défavorable ; la puissance sous cette hypothèse sera imprimée. La question de durée ne vous sera posée que si le niveau
  mesuré l'exige. » Les autres questions de valeur restent celles du G0 de SIM-BIS (A-2, A-3, 20 % sous H0 ; G0-SIM l.20-22).

## 13. Critères de sortie

1. **Par sous-lot** : suite `scripts/plan-s2bis-2` verte, plancher relevé ; suites `scripts/plan-s2bis`, `scripts/sim-bis` et
   `s2-harness` inchangées ; campagne de mutants conforme au contrat ; hook, gate des secrets, `cargo --locked xtask verify`
   verts (lignes de verdict seules) ; journal G1 ; ligne JOURNAL.
2. **Lot** : G2 neuve à 100 % (réviseur ≠ générateur, checklist) ; corrections rouges avant, vertes après ; contrôle FM-1.1
   des transcriptions ; répétition (E-P2-20) ; épinglage au JOURNAL (E-P2-21) ; un lancement au code 0, A = B ; versement avec
   `SHA256SUMS` et README ; bloc d'annexe B ; entrée de l'inventaire D.1-bis ; items du §11 formés ou précisés.
3. **G0** : avis de l'advisor ; adjudication ; ajout daté au G0 de SIM-BIS adjugé avant l'épinglage (Q-P2-07) ; cp-1 bref
   de l'ajout si Q-P2-13 (b).
4. **Suite dans SIM-BIS** : diff d'intégration commis avant E0 ; E1 calcule C1 selon l'ajout ; FIV-IDENTIF-1 fermé à la
   sortie d'E1 épinglée, avec sa limite.

## 14. Provenance

**Pièces lues dans le dépôt** [lu] (sha256 à `5f99ab5`) :
- `docs/adr-0029/g0-sim/G0-SIM-BIS.md` (`d9cffc0a…`), `PROPOSITION.md` (`0e78afab…`), `AVIS.md` (`aaf70a4f…`), en entier ;
  égaux à `g0-sim/SHA256SUMS` [mesuré].
- `g0-sim/revue-t2/AVIS-SIM-T2.md` (`30950295…`) et `revue-t3/AVIS-SIM-T3.md` (`da343918…`), en entier, égaux à leurs
  `SHA256SUMS` [mesuré] ; `revue-t1/` ne contient aucun AVIS (liste par `ls`) : rien n'y est lu.
- ADR-0029 (`b908842d…`, 569 lignes) : titres par `grep -n` des lignes de titre, ajouts datés par `grep -n -i` ; l.15-58,
  l.118-165, l.177-193, l.377-400.
- Annexe B d'ADR-0028 (`f7cf4cd5…`) : titres des blocs par `grep -n` ; B.58 l.956-972, B.61 l.1016-1029, B.64 l.1060-1070,
  B.66 l.1089-1097.
- Annexe D d'ADR-0028 : lignes trouvées par `grep -n` dans ce seul fichier, puis l.32-58 (liste D.2, noms seulement, et début
  de D.3) ; aucune pièce de la liste ouverte.
- `docs/adr-0029/plan-s2bis/` : `README.md` (`93fd70c2…`), `G1-lot-PLAN-S2BIS.md` (`cb9d1be0…`), `G2-lot-PLAN-S2BIS.md`
  (`7fc6b8a8…`), `episodes.txt` (`c0371ca5…`), en entier ; `SHA256SUMS` (`f21f9293…`) ; sha256 des trois sorties égaux
  [mesuré].
- `scripts/plan-s2bis/` : `README.md`, `parametres.json`, `commun.py`, `episodes.py`, `regles.py`, `lancer.sh` en entier ;
  `tau_sigma.py` l.1-20 ; `okx.py` l.1-25 ; `tests/__init__.py`, `tests/fixtures.py`, `tests/test_episodes.py` en entier ;
  `tests/test_lancer.py` l.1-150 ; `tests/test_commun.py` l.24-41 et l.143-162, noms des tests par `grep -n` ; 16 sha256 égaux
  à `SHA256SUMS` (`65c26310…`) [mesuré].
- Hors de la liste du brief (écart E-2) : `docs/adr-0029/G0-lot-PLAN-S2BIS.md` (`81bf3f33…`, 28 lignes) et
  `docs/adr-0029/G0-lots-S2BIS.md` (`db49d5f2…`, 25 lignes), en entier ; `.github/workflows/gates.yml`, lignes des jobs par
  `grep -n`.

**Pièces lues hors du dépôt** [lu] : le brief (`596e66ef…`) ; `sim4/g2/AVIS-SIM-T4.md` (`6dfc13e7…`) et
`RAPPORT-WORKER-SIM-T4-transcrit.md` (`fc178785…`), en entier ; `sim4/diffs/SB-10A.diff` (`5d62169b…`), `SB-10B.diff`
(`847fae13…`), `SB-10C.diff` (`91b31f55…`), en entier.

**Mesures** [mesuré, 2026-10-05, hôte de session, Python 3.11.15] :
1. `git rev-parse HEAD` : `5f99ab5…` à 13:23, 13:49 et 13:55 UTC ; `git status --short` vide à chaque relevé ;
   `git cat-file -t` et `git log -1` sur `f35a70c…` : commit du 2026-10-03T00:44:31Z.
2. `sha256sum` des pièces ci-dessus, égalités notées.
3. `date -u -d @…` : t0 = mercredi 2026-08-26 19:00 UTC ; t_fin = lundi 2026-09-28 01:28 UTC ; plage D5 du jeudi 2026-09-24
   18:18 au samedi 2026-09-26 15:08 UTC.
4. `calc/calc_p2.py` (`ce42843e…0f37`, 0 octet 92), sortie `calc/calc_p2.out.txt` (`eace3fe5…f304`) : portée, calendrier,
   D5, sautées, gardes, cv, comptes d'EP, tailles de PLAN-S2BIS, rapport de la tranche 4. Vérifiables sur la page :
   30 286 − 24 585 = 5 701 ; 13 491 − 11 397 = 2 094 ; 2 × 10 × 17 = 340 ; 65 × 200 × 2 × 10 = 260 000 ; 372 + 475 + 159 =
   1 006 ; de 14:55:41 à 17:01:22, 2 h 05 min 41 s ; de 16:59:04 à 17:00:31, 87 s.

**Non ouverts** : `docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`,
`docs/adr-0028/monark-m009a/`, `docs/adr-0028/execution/` (dont le rendu J28), tout `*.jsonl`, toute pièce de D.2 (dont la
copie de session des journaux, n° 7, et la transcription de session de l'orchestrateur, n° 11), le JOURNAL, `scripts/sim-bis/`
à la tête, `s2-harness/` (ni à la tête ni à `f35a70c`). Aucune recherche récursive, aucun Glob ; `ls` de dossiers nommés
seulement. `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée.

**Exposition** : valeurs de S2 post-rendu portées par l'ADR §1.1 et par EP (taux, épisodes, censure, FIV_série) ; FIV
synthétiques de mise au point de la tranche 4 (RW-T4 l.65) ; noms des pièces de D.2. Aucune donnée de S2-bis n'existe.
Aucune valeur de seconde main n'entre dans un chiffre de ce G0 ; 5 701 et 2 094 (l.31, venus du rendu) sont recomptés
[calc].

**Écarts du rédacteur** :
- **E-1** : barres obliques inverses tapées dans deux commandes de contrôle (un motif de `grep` sur la sortie d'`od -c` ; le
  point échappé d'une recherche de « D.2 » dans l'annexe D), et une fois dans le texte de cette proposition (une barre
  verticale échappée dans un tableau), retirée par gabarit `chr(92)`. Le comptage des octets 92 par Python fait foi : 0 dans
  `calc_p2.py` et dans cette proposition.
- **E-2** : pièces lues hors de la liste du brief, pour le patron et l'attestation : G0 de PLAN-S2BIS, G0 de vague, lignes de
  `gates.yml`, liste D.2 (noms) et l.49-58 de l'annexe D.
- **E-3** : `revue-t1/` ne contient aucun AVIS ; rien n'y est lu.
- **E-4** : le brief ne nomme pas de base ; base relevée `5f99ab5`, inchangée du début à la fin.

**Réviseur attendu** : l'advisor désigné, puis l'orchestrateur ; cp-1 bref de l'ajout daté si Q-P2-13 (b). Le rédacteur n'a
généré aucun des lots qu'il décrit.
