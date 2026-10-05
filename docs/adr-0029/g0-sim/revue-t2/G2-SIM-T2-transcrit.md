# Relecture G2 neuve — SIM-BIS tranche 2 (transcrit)

> Transcription par l'orchestrateur le 2026-10-05 02:48:25 UTC du rapport rendu par message par le réviseur G2 (agent a507e004d00e5d755) ; contrôle FM-1.1 du transcript : fragments_l51_l14 = 0. Texte du réviseur ci-dessous, sans retouche.

# Relecture G2 neuve : lot SIM-BIS, tranche 2 (SB-3a à SB-4b, couche des sources)

**Gate 0** : le modèle qui m'exécute est `claude-opus-5-5` (identifiant exact), effort max. Je suis réviseur G2 neuf et n'ai rien généré de ce lot.
**Dates** (`date -u`) : 2026-10-05, de 02:06:18 à 02:46:09 UTC.
**Base** : `git rev-parse HEAD` donne `784ebd2bab7953becf53dea33e596f67c1096d11` au début et à la fin, et `git status --short` est vide. C'est la base des diffs (`diffs-784ebd2/`) et celle du rapport du worker : aucun écart de base.
**Pièces** : `…/sim2/SHA256SUMS` (sha256 `daad68ff…eeb6`, égal à celui du rapport) : 121 entrées sur 121 OK. G0 `d9cffc0a…` ; l'épingle `eeaceb6b…` de `g0-sim/SHA256SUMS` et de `parametres.json` date d'avant l'ajout daté de 01:45:03. PROPOSITION `0e78afab…`, AVIS `aaf70a4f…`, ADR-0029 `b908842d…`, EP `c0371ca5…` (égal à son SHA256SUMS).
**Rendu** : rapport par message. Outils et sorties dans `<scratchpad>/s2bis/sim2/g2/rev/` (`SHA256SUMS` `5a71b65a…`, 76 entrées). Copies, cible cargo et TMPDIR supprimés (disque : 8,5 → 8,8 Go libres).

## Verdict : ACCEPTE-AVEC-CORRECTIONS (C-1 à C-5, liste fermée)

## Résumé
- **Le code est juste.** Les lois produites sont celles que vise le G0, vérifiées par des calculs exacts et par une simulation indépendante (contrôle 3).
- **Les tests ont des trous.** 15 de mes 28 mutants survivent. Les tests ne protègent pas :
  - l'indépendance des unités faibles d'un hôte à l'autre ;
  - l'indépendance des écarts F d'une classe à l'autre ;
  - la différence entre tendances indépendantes (cellule N8) et tendance commune (X1) ;
  - l'indépendance du régime entre strates ;
  - les lois d'épisodes réellement employées par strate et par type.
- **Deux défauts de validation** : la garde nommée du régime est contournée par le chemin principal, et une unité faible hors du pool est ignorée sans refus.
- **Ce qui est demandé** (C-1 à C-5) : des cas écrits à la main pour tuer les mutants vivants, deux refus nommés, l'extension de la garde `ast` des puissances, et la mise à jour des citations de `parametres.json`. Pour C-1, j'ai écrit et vérifié onze prototypes de cas (`stat/proto_corrections.py`) : chacun passe sur le code livré et tue son mutant (sortie 1).

## Contrôles

**(1) Série et tailles**
- Copie `git archive HEAD` avec les exclusions du brief. Les six diffs passent `git apply --check` puis `git apply`, dans l'ordre.
- Arbre final égal aux empreintes de `etapes-784ebd2/rb4b` : 17 sur 17.
- Lignes de code ajoutées (hors `.md`, recomptées par awk) : 196, 199, 156, 147, 120, 175, soit 993. Documents : +1, +2, +1, +1, +1, +1.
- Chaque état, de la tête jusqu'à SB-4b, rejoué par la commande du job : runner (33 ok), puis la ligne de `gates.yml`. Sortie 0 avec Ran = 49, 53, 60, 64, 68, 71, 75.
- Suite finale sous python3.10 à 3.13, `-W error`, PYTHONHASHSEED 0 et 7 : 75 OK partout.

**(2) Conformité, exigence par exigence**
- **E-S-07** : BTC est servi par `calibration.unites` (10 hôtes) ; les autres pools sont pris parmi eux, avec refus `SOURCES/classes` sinon. Pools provisoires [inféré], recoupés avec CALIB-ACTIFS-G0 §3.2 et §3.3 : USDC/USD chez Binance, Kraken, Bitstamp, Bitfinex, Gemini listé ; ni Coinbase ni OKX.
- **E-S-08** : H est commun aux classes de l'hôte, F est propre à chaque (hôte, classe), l'état est typé (panne ; écart hors panne). T-GEN-2 est tenu. L'indépendance n'est pas testée : C-1 a et b.
- **E-S-09** : taux exacts `Fraction(cellules, n_s)`, écart propre (e − p)/n_s, facteur f, facteur `autres`. Composante hors-enveloppe τ modélisée côté source, en épisodes d'une fenêtre, non multipliée par f (conforme à l'AVIS, Q-S-21).
- **E-S-10** : loi « tous épisodes », selon l'ajout daté du G0 (point 2). En stress, elle est regroupée sur les dix hôtes ; mes sommes sur EP l.54-92 donnent 1×662 2×11 (panne) et 1×662 2×12 (écart). C-1 i.
- **E-S-11** : r_L = part·p et reste renormalisé ; P(A ∪ L) = p exactement.
- **E-S-12** : régime Z par (hôte, strate) de paramètres φ et τ_D ; κ est le rapport des taux de A = E ∪ (E′ ∩ Z) ; la marge est exacte. C-2.
- **E-S-13** : (a), (b), (c) et (d) sont présents. Les valeurs que le G0 ne fixe pas vont à l'item DERIVE-AMPLITUDE-1. C-1 c.
- **E-S-14** : grille et horizon viennent de `calendrier`.
- **E-S-15** : débuts de Bernoulli au taux ρ·w/86 400 par fenêtre ; durée D fixe ou géométrique ; hôtes tirés à π, ou paire ou triplet sans remise, avec imposés ; l'incident s'ajoute à H, donc à toutes les classes.
- **E-S-16** : chaîne de S2 (G0 SIM-NIVEAU l.54 lu : L = 1 signifie tirages indépendants). C-1 a, e, j ; C-3.
- **E-S-39** : taux et histogramme sous C0 testés ; FIV prévu à SB-10.
- **Transverses** : E-S-01, 03, 06, 41, 42, 43, 53, 54 et 55 sont tenues.

**(3) Justesse statistique, par des calculs indépendants du code**

*Calculs exacts en `Fraction`*
- Récurrence avant sur les états (pause) et (en cours, reste r), pour cinq cas : 1×1 3×1 à q = 1/2 ; EP l.14 à q = 1/700 et à q = 3/7 ; longues réduites ; q = 1.
- Avec P(R = k) = P(L ≥ k)/E[L] et un départ en cours avec probabilité π = μq/(μq + 1) : P(en épisode à t) = π pour tout t de 0 à 60, et la loi jointe (état, reste) est invariante.
- Le témoin qui tire le reste dans L n'est pas stationnaire.
- Loi résiduelle d'EP l.14 : poids 332, 31, 7, 1, 1 sur 372.
- `sources.composantes` sur 2 208 combinaisons (23 taux d'EP × f ∈ {1 ; 0,3} × parts {0 ; 0,2 ; 0,5} × grille E1 en φ et κ) : P(A ∪ L) = p, rapport des taux = κ, r_L = part·p, tous exacts.
- r′ maximal : 0,6609, atteint pour defillama en stress, φ = 0,01, κ = 50 (le worker annonce ≈ 0,66).
- À la main : q = 332/24 213 et μq/(μq + 1) = 372/24 585.

*Monte Carlo indépendant, graine fixe (cellules `G2-REV-T2-*`)*
- **alterner et markov** : 20 000 chaînes ; P(en cours) à 8 instants de 0 à 59 : |z| ≤ 1,83. Transitions mesurées 0,9501 et 0,0333 pour a = 0,95 et b = 1/30.
- **Régime** (600 réplications) :
  - marge 0,04995 contre 0,05 (z −0,20) ;
  - part de Z 0,1011 (z +1,01) ; séjour moyen dans Z 20,05 contre 20 ;
  - P(·|Z = 0) = 0,03827 contre 0,03857 ; P(·|Z = 1) = 0,15348 contre 0,15286.
- **Dérives** : 16 tranches |z| ≤ 1,9. Transitoire : 0,14944 contre 0,15, puis 0,04986 contre 0,05.
- **Incidents** :
  - 0,0997 début par jour contre ρ = 0,1 ;
  - paires : 21 sur 21, χ²(20) = 15,7 et 14,1 ; triplets imposant gemini : 21 sur 21, χ² = 20,2 ;
  - couverture « chacun à 0,7 » : 0,16274 contre 0,16317 ;
  - durée géométrique moyenne 19,92 contre 20 ;
  - hôtes à saut 0,288 à 0,318 contre 0,3 ;
  - panne initiale : binance 0, les autres de 0,102 à 0,124 contre 1/9.
- **Réplication complète** : W = 4 (60 480 fenêtres), 400 réplications, f = 1, régime (1/20, 10, 240), τ = 1/4 000. 60 taux (H par hôte et strate ; F de BTC et d'ETH) comparés aux cibles lues dans EP par mon propre regex : χ² = 40,1, |z| max = 1,89. Avec les pannes longues (part 1/5), sur 3 000 réplications : |z| ≤ 1,13.
- **Histogrammes sous C0** (binance, bitstamp, defillama en calme) : égaux à EP à 5·10⁻⁴ près.
- **Coût** : 0,282 s par réplication, 4,46 s pour la première (90 tables).

**(4) Identité bit à bit**
- Ma sonde couvre toutes les branches (4 fonds × 2 réplications). Sous 3.10.20, 3.11.15, 3.12.3 et 3.13.14, avec PYTHONHASHSEED 0, 1, 4242 et aléatoire : 16 sur 16 donnent `9e288226…9efbcc6`.
- La sonde du worker, rejouée sur ma copie, donne `85c7fbdd…9d550e29` (égal au journal).

**(5) Rouge, vert et mutants**
- Rouges rejoués : les tests de chaque pas sur le code du pas précédent sont rouges 6 fois sur 6.
- Rouges d'assertion avec mes propres ébauches : SB-3b 5 FAIL ; SB-3d 4 FAIL ; SB-4b 3 FAIL et 1 ERROR. Verts sur le code de chaque pas.
- Mes 28 mutants, classés par la commande du job (runner d'abord, puis la ligne de `gates.yml`, borne 300 s) : 13 TUÉS, 15 VIVANTS, 0 FATAL.
  - Vivants : R-01 à R-09, R-19, R-22, R-25, R-26, R-27, R-28.
- Les 80 mutants du worker, rejoués sur l'état final : 76 tués tels quels. Les 4 autres (M-3C-05, M-GEN-3, M-4A-02, M-4A-03) visaient le code d'une étape antérieure ; adaptés à l'état final, ils sont tués tous les quatre.

**(6) CI**
- `gates.yml` ne change que le plancher (49 → 75). `--aucun-saut --egal` est gardé et le runner reste la première étape : aucune gate affaiblie.
- `test_fitness_tirages.py` est découvert par la suite (+2 au compte Ran de SB-3b).
- Rejoués : s2bis 49 OK ; s2-harness 405 OK (skipped=2) ; secrets : 147 cas ok, et `--tree` vert sur 19 fichiers (dépôt jetable).
- Hooks et épinglage des modèles non rejoués : les diffs ne touchent pas leur portée.

**(7) R-13, R-8, xtask**
- R-13 : aucun marqueur dans les lignes ajoutées.
- R-8 : bibliothèque standard seule.
- `cargo --locked xtask verify`, hors réseau, sur la série puis sur la tête sans les diffs : S-G1 à S-G8 VERT ; fmt, no_std et clippy VERT ; S-G9 ROUGE sur les deux (docs/17:70, déjà connu).
- Aucune octet 92 dans le lot.

**(8) Écarts et items**
- **E-1 à E-13 du worker : acceptés tels que déclarés.**
- E-3 : les rouges d'assertion faits après le code sont recoupés par mon rejeu indépendant. Pour la tranche suivante, mettre l'exigence dans le brief dès le départ.
- E-6 : la « garde nommée du régime » est incomplète, voir C-2.
- E-4 : j'ai vérifié à la main l'attendu corrigé (début à la fenêtre 5).
- Items SOURCES-STRATES-1, DERIVE-AMPLITUDE-1, REGIME-FAISABILITE-1 et ABS-POPULATIONS-1, et les constats CALCUL-1 et PAIRES-1 : d'accord pour les former.
  - REGIME-FAISABILITE-1 : r′ = 0,661 sur la grille E1 à f = 1 ; aucune cellule prévue ne combine f = 1 et une dérive.
- LIBM-POW-1 : avancé, mais pas clos (voir C-4).

## Corrections demandées (liste fermée)

**C-1 — Mutants vivants à tuer, un cas écrit à la main chacun (rouge sous le mutant, vert sur le code)**
- (a) R-01 : deux unités faibles indépendantes. Exemple : p = 1/2, L = 1, P(les deux) = 1/4 à 5 erreurs-types.
- (b) R-02 : F(u, BTC) ≠ F(u, ETH), et P(les deux) = p² à 5 erreurs-types, sur un EP d'essai où l'écart propre est non nul.
- (c) R-03 et R-04 : sens tirés à la main. « tendances » : un tirage par hôte, dans l'ordre du pool. « commune » : un seul tirage pour les dix.
- (d) R-05 : Z(h, calme) et Z(h, stress) tirés sur des flux distincts (φ différent par strate).
- (e) R-06 : une paire qui impose un hôte déjà membre de la liste de candidats rend deux hôtes distincts.
- (f) R-07 : seuil de départ d'une loi empirique épinglé des deux côtés. Exemple : loi 1×1 3×1, q = 1/2, u = 0,49 donne « en cours ».
- (g) R-08 : avec un horizon < 4 320, la panne initiale vaut exactement (1 << horizon) − 1.
- (h) R-09 : « transitoire » avec un autre multiplicateur est refusé (`SOURCES/derive`).
- (i) R-19 et R-22 : sur un EP d'essai à histogrammes distinctifs, F suit la loi « ecart » et H en stress suit la loi regroupée de la strate.
- (j) R-25 : l'écart d'une unité faible de type « ecart » reste disjoint de la panne quand les deux se recouvrent.

**C-2 — Garde du régime (E-S-12)**
- Aujourd'hui, `pannes()` et `etat()` rendent `ALEAS/geometrique` pour κ < 1.
- Avec κ = 1, ils acceptent en silence un φ hors de [0, 1[ ou un τ_D invalide.
- Attendu : `SOURCES/regime` dans les deux cas, la validation étant faite avant tout usage dans `union()`. Cas rouge montré avant le code.

**C-3 — Unité faible hors du pool (E-S-16)**
- Aujourd'hui, `etat()` l'ignore en silence.
- Attendu : `SOURCES/faible`, comme `touches()` rend `SOURCES/incident` pour les incidents. Cas rouge montré avant le code.

**C-4 — Garde `ast` des puissances (I-3, LIBM-POW-1)**
- Étendre `refus_puissance` à `operator.pow` et `operator.ipow` (import ou attribut), et aux attributs `__pow__`, `__rpow__`, `__ipow__`, avec les cas du vérificateur. Cela tue R-26 et R-27.
- L'accès dynamique par `getattr` (R-28) ne peut pas être vu : l'écrire comme limite.

**C-5 — Provenance (E-S-03)**
- `sources.source` de `parametres.json` doit citer l'ajout daté du G0 du 2026-10-05 01:45:03 (points 2 et 3), au lieu de « adjudication provisoire de l'orchestrateur, brief de la tranche 2 ».
- `rattachement` porte encore le sha256 du G0 d'avant cet ajout (`eeaceb6b…` au lieu de `d9cffc0a…`). Ce champ a été posé par SB-0 : à toi de dire si tu le veux dans cette correction.

## Observations (non bloquantes)
- **O-1** : certaines spécifications de cellule invalides donnent une exception non nommée : p = 1 ou L = 0 pour une unité faible, durée de dérive nulle, mode d'incident inconnu. ρ = 0 donne `ALEAS/geometrique`. À traiter par le schéma fermé des cellules, à SB-11.
- **O-2** : la phrase « prend le taux local m(t)·p » de `amincir` est approchée : le multiplicateur est pris au début de chaque épisode. Écrire « ≈ ».
- **O-3** : avec P(F) = (e − p)/n_s, la part « écart hors panne » obtenue est (e − p)/n_s·(1 − P(H)). L'écart à EP est de 2 % au plus en relatif et de 3,2·10⁻⁷ au plus en absolu. Le texte du G0 est suivi.
- **O-4** : l'ajout daté du G0 (point 2) donne −0,035 en calme. Recompté exactement : −19/528 ≈ −0,0360 (gemini, calme, panne). La valeur en stress est juste.
- **O-5** : sous Z, les fenêtres E′ tirées indépendamment se fondent aux épisodes de E. La loi des longueurs n'est donc conforme à EP que sous C0.
- **O-6** : la composante des pannes longues est rare : à W = 4, seules 1 à 3 % des réplications sont touchées. Il faut des milliers de réplications pour la contrôler ; mon premier passage à 400 réplications donnait un faux |z| de 19,9.
- **O-7** : l'enregistrement de rôle (ENREG-ROLE-1) reste à faire avant la G2 de la partie S-1.

## Questions Q-T2-1 à Q-T2-12 (fidélité seulement ; le fond relève de l'advisor)
- **Q-T2-1** : fidèle ; le G0 ne dit rien de la jonction entre strates. Les marges par strate sont exactes. Conséquence : en stress, une panne de 3 jours se voit au plus sur 2 jours par week-end.
- **Q-T2-2** : la lettre d'E-S-12 est tenue.
- **Q-T2-3 et Q-T2-4** : fidèles ; C-1 i et b.
- **Q-T2-5 et Q-T2-6** : valeurs non fixées par le G0. Note : le saut 0,1 ↔ 1,9 multiplie ou divise le taux par 19.
- **Q-T2-7** : d'accord avec le recoupement CALIB ; les autres questions vont à l'advisor.
- **Q-T2-8** : fidèle.
- **Q-T2-11** : vaut aussi pour l'indice des unités faibles, qui est leur rang dans la liste de la cellule.
- **Q-T2-12** : coût confirmé.

## Mes propres écarts
1. Trois outils hors dépôt portent 31 octets 92 voulus (`mc_global.py`, sa variante, `rougevert.sh`), écrits dans des heredocs et non par gabarit. Je les ai contrôlés sur les octets, et les résultats sont recoupés. Deux commandes portaient aussi une barre (grep, regex d'EP), avec des résultats recoupés à la main. Le lot n'en contient aucun.
2. xtask : j'ai affiché neuf lignes « note » de S-G9 (tronquées) en plus des lignes de verdict. Elles ne contiennent rien de D.2.
3. Exposition, toute permise :
   - EP l.1-100 ;
   - docs/11 l.340 et l.354-358 ;
   - annexe D l.28-52 (noms de D.2 seulement, aucune pièce ouverte) ;
   - CALIB-ACTIFS-G0 par recherche dans ce seul fichier.
4. Dépôt git jetable (init, add) pour `gate-secrets --tree`, hors du dépôt du projet.
5. Je n'ai pas ouvert `AVIS-SIM-T2.md`, pour rester indépendant de l'advisor.
6. Mon premier Monte Carlo global était invalide (O-6) ; il est refait et n'est pas compté.

## Journal de provenance (G1)

**Lu en entier [lu]** :
- briefs G2, worker et advisor ; rapport du worker transcrit ;
- G0, PROPOSITION, AVIS ;
- `revue-t1/` (G2, corrections, brief) ;
- `sources.py`, `test_sources.py`, `test_fitness_tirages.py`, `test_fitness.py`, `aleas.py`, `calendrier.py`, `parametres.json` ;
- diffs SB-3A et SB-3B ;
- journal et outils du worker cités ci-dessus.

**Lu par extraits [lu]** :
- ADR-0029 l.140-176 ;
- annexe B l.1016-1043 ;
- G0 SIM-NIVEAU l.45-62 ;
- `commun.py` l.1-120 ;
- `gates.yml` l.200-245 ;
- `verdict-suite-s2.py` l.1-40.

**Seconde main [2nd]** : aucun chiffre.

**Commandes et sorties** :
- `rev/sorties/` contient : états de la série, rouge et vert, mutants (`mutants_rev*.txt`, `rejeu_mutants_worker.txt`), identité, Monte Carlo, xtask, suites.
- Les sorties des autres scripts de `rev/stat/` (renouvellement exact, composantes exactes, Monte Carlo par composante, prototypes, constats) sont recopiées dans ce rapport.
- Tous les mutants cités sont versés, avec leurs outils, dans `rev/outils/`.

**Chiffres recomptés** : tous ceux de ce rapport, par mes propres commandes.