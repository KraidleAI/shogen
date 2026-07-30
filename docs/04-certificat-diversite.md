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
| **R2 — observable d'infrastructure** | recouvrements constatables au moment du quorum : ASN/hébergeur, CDN, émetteur de certificat, dépendance amont détectée (deux « sources » servant les octets du même agrégateur) | « src3 et src7 : même ASN ; corrélation de contenu à 0,999 sur 30 j » | borne les modes communs *visibles dans ces axes* ; ne teste pas la conjecture |
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
- Le certificat R1 publie : n, K, z, la définition d'écart utilisée, et la
  fenêtre d'historique. **Un z élevé ne « prouve » pas la dépendance d'une
  paire précise — il rejette le modèle d'indépendance du pool**, exactement
  le scope de K&L (« from an operational viewpoint, it does not matter
  *why* programs fail on the same input, it merely matters that they *do* »,
  §5, lu au texte).

**[À décider]** : définitions d'écart par classe de faits (le seuil
« hors enveloppe » réutilise l'estimateur du verdict — lignée Chainlink OCR
Lemme 8, détenu côté Kraidle) ; taille minimale d'historique avant qu'un
certificat R1 soit émissible (en dessous : le certificat dit « historique
insuffisant », jamais un z non significatif présenté comme une absence de
dépendance).

## 3. Le quorum effectif k_eff

Le chiffre de tête du certificat. Principe : **des sources indistinguables
dans un axe fort comptent pour une**.

- Partition du pool par les recouvrements R2 constatés (même amont détecté,
  même infrastructure) : k_eff = nombre de classes de la partition, pas de
  membres du pool. « Un quorum dont deux sources partagent un amont n'est
  pas un quorum de k » (02-vision) devient calculable.
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
   deux universités.)
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

**[À décider]** : le certificat est-il émis par Shōgen (centralisé, résidu
A(shogen-mesure) à nommer) ou recalculable par le vérificateur offline
depuis les témoignages R2 embarqués ? La seconde option est la seule
cohérente avec « sans confiance dans Shōgen » — son coût (volume du lot)
est l'objet de l'ADR.

## 6. Dettes de cette spec

1. Recherche académique formelle sur la quantification de diversité de
   sources (deux périmètres web sans contre-exemple au 2026-07-30 —
   insuffisant pour écrire « nouveau » dans une publication ; il faut une
   passe arXiv/ACM/IEEE dédiée, mots-clés : common-mode failure, diversity
   metrics, oracle independence, N-version).
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
