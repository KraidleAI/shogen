# Shōgen — Vision (v0, 2026-07-30)

> Statut : premier jet au format Kraidle, écrit après la passe librarian du
> 2026-07-30 (`01-precedents.md`, `biblio/INDEX.md`, ADR-0001). Les
> citations ci-dessous sont vérifiées dans les artefacts détenus sauf
> mention contraire. Rien ici n'est proven ni tested : c'est une vision,
> ses théorèmes restent à écrire.

## Le produit en une phrase

Une couche de perception attestée pour agents : des **témoignages** (ce
qu'une source a dit, capturé par un transport attesté), typés en **faits**
(classe, valeur, unité, méthode, fraîcheur), agrégés en **verdicts de
quorum** dont la diversité des sources est **mesurée et publiée**, le tout
vérifiable **offline par un tiers** sans confiance dans Shōgen.

## La phrase fondatrice, et sa lignée

**Une attestation prouve ce que la source a dit — jamais que la source dit
vrai.** Cette distinction n'est pas une prudence de style : c'est la ligne
que les quatre précédents détenus tracent eux-mêmes.

- DECO (CCS '20, détenu, abstract lu au fichier p. 1) prouve « that a
  piece of data accessed via TLS came from a particular website » —
  provenance, pas contenu de vérité.
- TLSNotary (FAQ détenue) : « does not solve the "Oracle Problem" ».
- C2PA 2.4 (spec détenue, §1.2 Scope, citant les Guiding Principles —
  localisation vérifiée par grep) : les spécifications « SHOULD NOT
  provide value judgments » — valider l'intégrité et l'association, jamais
  la bonté du contenu.
- Chainlink OCR (détenu côté Kraidle, Lemme 8) : la médiane attestée « is
  either the observation of a correct oracle or lies between the
  observations of two correct oracles » — le confinement dans l'enveloppe
  honnête, pas l'exactitude.

Shōgen adopte cette ligne comme **spécification**, pas comme excuse : tout
énoncé du produit dit lequel des deux il revendique, et le vocabulaire
interdit les formulations qui les confondent (« la donnée est vérifiée »,
« le prix est garanti correct »).

## Les quatre objets

1. **Témoignage (shōgen)** — la sortie brute d'un transport attesté :
   contenu, source, instant, transport, et le résidu de confiance propre au
   transport (ADR-0001). Un témoignage n'est jamais consommé nu par une
   décision.
2. **Fait** — un témoignage typé : classe (prix, solde, état…), valeur,
   unité, méthode d'extraction, fenêtre de fraîcheur. Le typage est un
   adapter (testé, jamais prouvé) ; le fait porte l'identité du typeur.
3. **Verdict de quorum** — k faits de la même classe, un estimateur au
   confinement énonçable (lignée Lemme 8), et **le certificat de
   diversité** : la mesure d'indépendance des k sources.
4. **Lot vérifiable** — l'artefact portable : témoignages + faits +
   verdict + certificat, vérifiable offline contre des clés épinglées.
   Le miroir perceptuel de la preuve M3 de Kraidle.

## Le cœur différenciant : la diversité mesurée, contre l'axiome d'indépendance

Le précédent qui gouverne est Knight & Leveson (1986 ; article complet
détenu et lu aux sections citées, `biblio/INDEX.md`) : 27 versions
développées indépendamment depuis la même spécification, un million de
tests, K = 1255 cas où plus d'une version échoue, statistique z = 100,51
contre un seuil à 99 % de 2,33 — « we reject the null hypothesis with a
confidence level of 99% … Thus, we reject this assumption » (§5).
**Dans la seule expérience de cette échelle, l'hypothèse d'indépendance a
été rejetée à 99 % alors même que l'indépendance de développement était
organisée** — et K&L bornent eux-mêmes la portée de leur résultat (§8, lu
au texte) : « it is conditional on the application that we used », la
généralisation exige d'autres expériences. Personne n'a mené l'équivalent
sur des sources de données ; c'est précisément le vide que le certificat
R1 instrumente. Et le détail qui fonde le certificat de
diversité : l'axe organisé (deux universités) n'a rien protégé — « In the
preliminary analysis of common faults, *all* were found to involve versions
from both schools » (§4). Un axe de diversité *déclaré* n'est pas un axe
*protecteur* ; seule la mesure des défaillances conjointes le dit — d'où le
certificat. Quarante ans plus tard, les architectures de quorum recensées
dans la passe du 2026-07-30 (01-precedents §3) reposent sur une
indépendance des signataires qu'elles ne mesurent pas — Chainlink OCR, le
modèle le plus explicite détenu, *nomme* son postulat (≤ f fautifs, Lemme
8) sans le mesurer davantage — l'axiome que K&L ont rejeté sur leur
terrain, jamais testé sur celui-ci, et exactement la
dette que Kraidle nomme A(indépendance des sources) sans pouvoir la
décharger.

Shōgen en fait son objet central : ne jamais postuler l'indépendance — la
**mesurer** là où elle est observable, et publier le rang de ce qui ne
l'est pas (04 §1). Axes observables candidats : infrastructure
d'hébergement commune, dépendances amont communes (le même agrégateur
derrière deux « sources »), méthode commune. Axes déclaratifs, publiés
sans poids protecteur propre : juridiction, opérateur. Le certificat de diversité publie ce qui a été mesuré et
ce qui reste déclaratif — un quorum dont deux sources partagent un amont
n'est pas un quorum de k, et le certificat le dit.

**Ce que la diversité mesurée n'achète pas, écrit d'emblée** : un axe non
mesuré reste un mode commun possible ; la mesure borne les corrélations
*visibles* dans les axes choisis. C'est le Knight & Leveson appliqué à
nous-mêmes — et il sera écrit à ce rang dans toute publication.

## Relation à Kraidle

Kraidle : *bounded authority* — la perception y est bornée et rendue
visible, jamais empêchée. Shōgen : *attested perception* — remplit le
`gather` (faits typés depuis des témoignages attestés), fournit l'instrument qui
décharge A(indépendance des sources). Souverains l'un de l'autre : Shōgen
sert tout agent, Kraidle accepte d'autres sources de faits. Le duo se vend
en une ligne : *bounded authority, attested perception*.

## Non-buts

- Pas de transport propriétaire (ADR-0001).
- Pas de jugement de vérité : Shōgen ne dit jamais qu'une source dit vrai.
- Pas d'oracle-métier : Shōgen ne choisit pas les sources d'un client, il
  qualifie celles qu'on lui désigne.
- Pas de composant en chemin de décision d'un tiers : Shōgen produit des
  artefacts vérifiables, il n'autorise rien — autoriser est le métier de
  l'autre projet.

## Premier produit visé

L'attestation de prix multi-sources pour agents de trading : la classe de
faits la plus demandée, le client du beachhead Kraidle, et la classe où le
confinement type Lemme 8 a un précédent publié à citer.

## Prochaines étapes

1. Fermer les dettes du registre (`biblio/INDEX.md` §Dettes) — l'article
   IEEE original en tête.
2. Fetcher un artefact primaire Reclaim + le modèle de menace proxy vs MPC
   au texte (les résidus par transport de ADR-0001 en dépendent).
3. Spécifier la forme canonique de témoignage (le coût nommé d'ADR-0001).
4. Chercher la littérature récente sur la mesure de défaillances corrélées
   appliquée aux oracles/sources de données (la recherche du 2026-07-30 n'a
   rien trouvé d'industrialisé — absence à re-vérifier par une recherche
   dédiée avant d'écrire « neuf » dans une publication).
