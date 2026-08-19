# Le certificat de diversité — spécification v0 (2026-07-30)

> Statut : premier jet. Rien ici n'est proven ni tested. Document jumeau de
> `03-temoignage.md` : le témoignage est l'objet unitaire, le certificat est
> l'objet de quorum. Les points **[à décider]** attendent leurs ADRs.

## 0. Ce que le certificat remplace

Les architectures de quorum recensées dans la passe web du 2026-07-30
(01-precedents §3) reposent sur une indépendance des signataires qu'elles
ne mesurent pas — même la plus explicite détenue, Chainlink OCR, **nomme**
son postulat (≤ f fautifs, le modèle du Lemme 8) sans le mesurer. Le
postulat a un nom dans la littérature adverse elle-même :
Avizienis l'appelle « the fundamental conjecture of the NVP approach »
(cité dans le Reply détenu, p. 1). Et il a une réfutation expérimentale
détenue et lue au texte : Knight & Leveson, 27 versions, un million de
tests, K = 1255 co-défaillances observées, z = 100,51 contre un seuil à
99 % de 2,33 — « we reject the null hypothesis with a confidence level of
99% … Thus, we reject this assumption » (§5).

Le certificat de diversité est le remplacement du postulat par une mesure :
pour un quorum de k sources, il publie **ce qui a été mesuré, ce qui n'est
que déclaré, et le quorum effectif qui en résulte**.

## 1. La leçon structurante : trois rangs de diversité, jamais confondus

Knight & Leveson §4, lu au texte : l'axe de diversité *organisé* — deux
universités, populations distinctes — n'a rien protégé ; « In the
preliminary analysis of common faults, *all* were found to involve versions
from both schools ». Un axe déclaré n'est pas un axe protecteur.

Le certificat classe donc chaque énoncé de diversité dans un des trois
rangs, du plus fort au plus faible — et le rang fait partie du certificat :

| rang | nature | exemple | ce que ça vaut |
|---|---|---|---|
| **R1 — co-défaillance mesurée** | historique observé des défaillances conjointes des sources (pannes, valeurs aberrantes, staleness simultanées), testé contre le modèle d'indépendance | « sur n fenêtres, K co-défaillances ; z = … » | la seule mesure qui teste réellement la conjecture — c'est le test de K&L §5 lui-même, transposé aux sources |
| **R2 — observable d'infrastructure** | recouvrements constatables au moment du quorum : ASN/hébergeur, CDN, émetteur de certificat, dépendance amont détectée (deux « sources » servant les octets du même agrégateur), **et les attestors des témoignages** (ADR-0004 : le même attestor derrière deux témoignages est un mode commun), la *méthode* commune (même estimateur ou logique d'agrégation amont — récolte K&L §6, cf. §6.4) | « src3 et src7 : même ASN ; corrélation de contenu à 0,999 sur 30 j » | borne les modes communs *visibles dans ces axes* ; ne teste pas la conjecture |
| **R3 — déclaration** | entité légale, juridiction, méthodologie annoncée | « opérateurs distincts (déclaré) » | aucun poids protecteur propre — publié pour la traçabilité, jamais compté seul |

**Règle de rédaction transposée du vocabulaire Kraidle** : une phrase sur la
diversité d'un quorum porte le rang de chaque axe qu'elle invoque. « Quorum
de 5 sources diverses » sans rangs est une formulation interdite du projet.

## 2. Le test R1 : la machinerie de Knight & Leveson, transposée

La transposition est directe et c'est une force (un précédent de quarante
ans, détenu, au lieu d'une méthode inventée) :

- Les « versions » deviennent les **sources** ; les « cas de test »
  deviennent les **fenêtres d'observation** (une lecture de la classe de
  fait par fenêtre) ; une « défaillance » devient un **écart observable**
  de la source (panne, staleness au-delà du seuil de classe, valeur hors
  de l'enveloppe des autres au-delà du seuil de classe).
- Sous indépendance, le nombre K de fenêtres à écarts multiples suit la
  binomiale de K&L §5 (P_more, approximation normale, statistique z).
  **Le test agrégé suppose A(window-stationarity)** — l'hypothèse (ii)
  d'Eckhardt & Lee (« stationary input series ») transposée aux fenêtres
  d'une classe de faits ; elle est écrite dans chaque certificat R1.
- Le certificat R1 publie : n, K, z, la définition d'écart utilisée, et la
  fenêtre d'historique. **Un z élevé ne « prouve » pas la dépendance d'une
  paire précise — il rejette le modèle d'indépendance du pool**, exactement
  le scope de K&L (« from an operational viewpoint, it does not matter
  *why* programs fail on the same input, it merely matters that they *do* »,
  §5, lu au texte).

**[À décider]** : définitions d'écart par classe de faits (le seuil
« hors enveloppe » réutilise l'estimateur du verdict — lignée Chainlink OCR
Lemme 8, détenu côté Kraidle) ; **stratification des fenêtres par régime**
— son cas motivant est daté : l'ouverture de pré-marché illiquide du
28 juillet 2026 (SK Hynix), régime où A(window-stationarity) casse et où
un test agrégé sur des fenêtres de séance normale ne dit rien ;
taille minimale d'historique avant qu'un certificat R1 soit émissible (en dessous : le certificat dit « historique
insuffisant », jamais un z non significatif présenté comme une absence de
dépendance).

**La forme statistique mûre du R1 est déjà publiée** (Littlewood & Miller,
IEEE TSE 15(12), 1989 — détenu, lu pp. 1596-1604) : l'écart à
l'indépendance de deux composants est exactement Var(Θ) dans le cas d'une
« méthodologie » unique (éq. 14-16), et entre deux méthodologies le
facteur d'élévation conditionnel est 1 + Corr(Θ_A,Θ_B)·CV(Θ_A)·CV(Θ_B)
(éq. 28) — la corrélation des fonctions de difficulté *est* la mesure du
degré de dépendance. Le R1 de Shōgen peut donc publier, au-delà du z de
K&L, l'estimée de Corr entre paires de sources ; et L&M p. 1601 ouvre une
possibilité que le certificat doit savoir exprimer : **Cov < 0 existe** —
un pool anti-corrélé fait *mieux* que l'indépendance. Nuance apportée par
leur ré-analyse des données K&L en deux méthodologies (p. 1603) : l'axe
deux-écoles, que K&L §4 montrait non-protecteur au sens « toutes les
fautes communes traversaient les deux écoles », *réduisait* néanmoins la
probabilité de co-échec en espérance (ρ = 0,1808 ; 10,944e-6 contre
12,963e-6 en tirage aléatoire) — un axe déclaré peut porter un poids
réel, mais **seule la mesure le convertit en évidence**, ce qui est
précisément la thèse des rangs.

## 3. Le quorum effectif k_eff

Le chiffre de tête du certificat. Principe : **des sources indistinguables
dans un axe fort comptent pour une**.

- Partition du pool par les recouvrements R2 constatés (même amont détecté,
  même infrastructure) : k_eff = nombre de classes de la partition, pas de
  membres du pool. « Un quorum dont deux sources partagent un amont n'est
  pas un quorum de k » (02-vision) devient calculable.
- **La partition nomme ses amonts** (ADR-0007) : le certificat écrit
  « cluster A = {src1, src2} via place X », jamais « 3 sources → 2
  clusters ». Nommer rend répondable, par celui à qui elle appartient, la
  question que nous ne traitons pas — la profondeur de X.
- R1 module la confiance dans la partition : un z de pool élevé avec une
  partition R2 propre signifie que les axes mesurés ne capturent pas le
  mode commun — le certificat le dit en clair (« co-défaillance observée
  non expliquée par les axes R2 »), et c'est un signal de refus côté
  politique, pas un détail.
- R3 ne modifie jamais k_eff.

**[À décider]** : la relation exacte entre k_eff et le f de l'estimateur de
confinement (le verdict de quorum hérite du Lemme 8 : la valeur admise est
dans l'enveloppe honnête *du quorum effectif*, pas du quorum nominal).

## 4. Ce que le certificat n'achète pas — écrit dans l'objet

Chaque certificat embarque, en clair, son périmètre :

1. Un axe non mesuré reste un mode commun possible. La liste des axes
   mesurés est exhaustive dans le certificat ; tout le reste est hors
   mesure. (Knight & Leveson appliqué à nous-mêmes : nos axes sont nos
   deux universités.) **Cette exhaustivité est un champ NON OPTIONNEL du
   certificat** (ADR-0019 D7, GTM canal 2) : c'est la parade au seul canal de
   conflit que ni la vérification offline ni le benchmark public ne ferment —
   le jeu sur les axes ; le canal 2 payant (oracle certifiant son propre feed)
   n'est défendable que si chaque certificat publie ce qu'il n'a **pas** mesuré.
   Exigence ferme en S4, candidate à un ADR de spec du certificat.
2. R1 mesure le passé ; il ne borne pas un adversaire qui ne s'est pas
   encore exprimé. Un pool à l'historique impeccable peut être capturé
   demain.
3. La diversité mesurée borne les corrélations *visibles* ; le confinement
   du verdict reste « dans l'enveloppe honnête », jamais « proche du
   vrai » — la ligne quorum-confinement-jamais-exactitude, ici comme
   partout.
4. Les observables R2 sont eux-mêmes des témoignages (une mesure d'ASN, une
   corrélation de contenu) avec leurs transports et leurs résidus — le
   certificat cite les siens.
5. Les entrées **rédigées** (ADR-0005) sont listées : une utterance
   rédigée est exclue de la corrélation de contenu, donc l'axe
   amont-commun de son témoignage est non mesuré — A(axis-coverage)
   s'élargit d'autant, visiblement.
6. **La qualité du marché sous-jacent n'est pas mesurée** (ADR-0007) :
   profondeur, liquidité, largeur de fourchette de la place citée sont
   hors périmètre. Le certificat *nomme* l'amont ; il ne le note pas. Un
   pool de k_eff élevé dont tous les amonts sont peu profonds reste
   exposé — le cas SK Hynix du 28 juillet 2026, où le prix était
   « accurate but anomalous », est la démonstration à citer.

## 5. Résistance au jeu — le certificat comme cible

Un certificat qui a de la valeur sera attaqué. Surface minimale à traiter
dès la v1 (chacun → corpus de classes d'attaque, le geste Kraidle) :

- **Sybil de sources** : k sources de façade sur des amonts distincts *en
  apparence* — la détection d'amont commun par corrélation de contenu (R2)
  est la contre-mesure primaire, et sa limite (un amont qui bruite ses
  copies) est un mode commun non mesuré à déclarer (§4.1).
- **Fenêtre de complaisance** : choisir l'historique R1 qui arrange. Le
  certificat fixe la fenêtre par politique de classe, pas par émetteur.
- **Gonflement de k nominal** : sans effet — seul k_eff est publié en tête.

~~[À décider] : certificat émis ou recalculable ?~~ — **tranché par
ADR-0003** (2026-07-30) : **recalculable** par le vérificateur offline
depuis les témoignages embarqués ; la signature de Shōgen n'est qu'un
cache, jamais une racine de confiance. La branche « émis » est morte, et
avec elle le résidu A(shogen-mesure) qu'elle aurait exigé — il n'est
créé nulle part. Le résidu réellement créé par la décision est
**A(history-integrity)** (`08-assumptions.md`). Coût assumé : volume du
lot, à dimensionner en S4.

## 6. Dettes de cette spec

1. ~~Recherche académique formelle~~ — **fait le 2026-07-30** : verdict
   R-1 rendu dans `06-etat-de-lart-diversite.md`. Conséquences pour cette
   spec : le claim est rescopé (le geste « mesurer plutôt que postuler »
   est occupé ; la case propre est sources + historique testé + partition
   par observables + certificat par décision) ; k_eff doit être défini
   par contraste avec le n_eff de Kish (Kohli 2026), le nombre effectif
   TIFS 2016 et le Vendi Score — tous détenus ou en dette de fetch.
2. Les définitions d'écart par classe (§2) et la relation k_eff/f (§3).
3. Le corpus d'attaques du certificat (§5) au format classes numérotées.
4. ~~Lecture au texte de K&L §6-8~~ — **fait le 2026-07-30** (INDEX, entrée
   K&L : pp. fichier 10-25). Récolte pour les axes : les fautes corrélées
   venaient de *méconceptions partagées* (§6 — quatre versions sur
   vingt-sept ont fait la même hypothèse fausse sur la comparaison de
   cosinus), « approximately one half of the total software faults found
   involved two or more programs » (§8), et le mandat du certificat est
   dans la conclusion même : les concepteurs matériels « use sophisticated
   techniques to determine common failure modes and systematically alter
   their designs » (§8). Conséquence pour R2 : la *méthode* commune (même
   estimateur, même logique d'agrégation amont) est un axe candidat au
   même titre que l'infrastructure.
