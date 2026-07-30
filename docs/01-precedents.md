# Précédents — première passe, 2026-07-30

> **Mise à jour, même jour** : la passe librarian profonde a été exécutée.
> Les artefacts sont détenus et enregistrés (`../biblio/INDEX.md`), la
> décision structurante est prise (ADR-0001, `DECISIONS.md`), la vision est
> écrite (`02-vision.md`). Les dettes restantes sont listées dans l'INDEX.

> **Statut initial (conservé pour trace — antérieur à la mise à jour
> ci-dessus).** Passe de reconnaissance web (recherches du 2026-07-30), au
> standard « lead » et non « source ». Depuis la mise à jour du même jour,
> les éléments détenus et vérifiés sont enregistrés dans
> `../biblio/INDEX.md`, qui fait foi ; le statut « lead » ne couvre plus
> que ce qui n'y figure pas (zkPass, Opacity, vlayer, les arXiv cités, les
> chiffres vendeur). Les absences revendiquées portent le périmètre de
> cette recherche seulement.

## 1. La découverte qui recadre le projet

**Le primitif de transport attesté est mûr et industrialisé.** Le champ
zkTLS (« web proofs ») est passé des papiers aux SDKs :

- **TLSNotary** — pionnier open source de l'approche MPC
  ([crypto.news](https://crypto.news/what-is-zktls-web-proofs-explained/)).
- **Reclaim Protocol** — modèle proxy-witness ; le vendeur annonce des
  preuves mobiles en 2–4 s et 889 sources de données, et se présente comme
  le plus avancé du champ (chiffres et jugement vendeur, relevés au web le
  2026-07-30, non vérifiés sur artefact détenu — INDEX, dette 3)
  ([Reclaim — zkTLS Canon](https://blog.reclaimprotocol.org/posts/zktls-canon),
  [Shoal Research](https://www.shoal.gg/p/zktls-verifiable-data-composability)).
- **zkPass** — hybride proxy/MPC, déploiements en production
  ([zkPass/Medium](https://medium.com/zkpass/zktls-the-cornerstone-of-verifiable-internet-da8609a32754)).
- **Opacity Network** — réseau décentralisé de vérificateurs MPC ;
  **vlayer** — web proofs pour développeurs Ethereum.
- Signal d'adoption : Devconnect tient un **zkTLS Day** dédié avec ateliers
  sur les implémentations concurrentes ([Telah](https://telah.vc/zktls)).

**Conséquence structurante (proposition d'ADR-0001 Shōgen) : Shōgen ne
construit pas de transport.** Les transports (zkTLS proxy, zkTLS MPC,
attestation TEE, signature native de la source quand elle existe) sont des
**adapters interchangeables** en dessous de Shōgen — exactement la position
des adapters dans l'architecture Kraidle : ils apportent les témoignages
bruts, la couche Shōgen les type, les agrège et les qualifie.

## 2. Le paysage adjacent (attestation, provenance, oracles)

- **TEE pour l'IA vérifiable** : le patron « exécution isolée + attestation
  distante » est en production (Marlin Oyster, Phala, Atoma, Automata,
  Flashbots/attested inference)
  ([Eco — TEEs for AI Agents](https://eco.com/support/en/articles/14796365-tees-for-ai-agents-verifiable-compute)).
  Un transport de plus pour Shōgen, pas un concurrent.
- **Identité et mandats d'agents** : quatre modèles en 2026 — Mastercard
  Agent Pay (identités tokenisées), Visa Trusted Agent Protocol (en-têtes
  d'attestation), Google AP2 (Verifiable Credentials + mandats signés),
  DIDs crypto-natifs
  ([Autheo](https://www.autheo.com/blog/ai-agent-identity-trust-infrastructure-2026),
  [arXiv:2604.23280 — AI Identity: Standards, Gaps](https://arxiv.org/pdf/2604.23280)).
  C'est l'attestation de *l'agent* ; Shōgen atteste *ce que l'agent lit* —
  couches complémentaires, interop à prévoir.
- **Oracles** : les architectures « sûres » listées par les praticiens —
  diversité de sources, snapshots d'entrée, signatures de quorum,
  attestations TEE optionnelles, bornes de fraîcheur, circuit breakers
  ([TokenToolHub](https://tokentoolhub.com/ai-and-blockchain-oracles/)) —
  sont une **liste de vœux sans produit** : citée comme bonne pratique,
  pas comme offre. Le corpus Kraidle détient déjà le papier Chainlink OCR
  (Lemme 8 : la médiane est bornée par l'enveloppe honnête) — le résultat
  d'estimateur que Shōgen devra prouver dans son propre modèle ou citer.
- **Littérature émergente** : attestation comme primitive de consensus
  ([arXiv:2605.25844](https://arxiv.org/pdf/2605.25844)), pile protocolaire
  agents ([arXiv:2602.13795 — Agent-OSI](https://arxiv.org/pdf/2602.13795)),
  services d'attestation pour agents (Prova, Attestix) — à ouvrir au texte.

## 3. Le gap, reformulé après cette passe

Ce que personne n'offre (périmètre : cette recherche) :

1. **Un vocabulaire de faits typés orienté décision** — pas « une preuve
   qu'une page disait X », mais un fait de classe connue (prix, solde,
   état), daté, avec fraîcheur, unité et méthode, consommable par un noyau
   de décision fail-closed.
2. **La diversité de quorum MESURÉE** — les quorums recensés dans cette
   passe comptent des signatures ; personne n'y mesure l'indépendance des
   sources sur ses axes observables (infrastructure commune, dépendance
   amont commune — la juridiction ou l'opérateur communs restent des
   déclaratifs, rang distinct, cf. 04 §1 : les modes de défaillance
   corrélés). C'est précisément A(indépendance des sources), la dette que
   Kraidle nomme sans pouvoir la décharger. **C'est le cœur différenciant
   de Shōgen.**
3. **La vérification offline du LOT de faits** — un tiers vérifie sans
   confiance dans Shōgen que k témoignages de sources mesurées-diverses,
   dans la fenêtre de fraîcheur, supportent la valeur admise — le miroir
   perceptuel de la preuve portable M3 de Kraidle.
4. **L'honnêteté sémantique comme spécification** — l'attestation prouve le
   dire, pas le vrai ; le quorum achète le confinement, pas l'exactitude.
   Aucun acteur du champ ne borne ses claims ainsi ; c'est un
   différenciateur *et* une protection.

## 4. Prochaines étapes de la passe librarian (à faire)

1. Fetcher et lire au texte : le whitepaper/spec TLSNotary, la doc
   d'architecture Reclaim (modèle de menace du proxy-witness — où est le
   trust ?), zkPass, un survey zkTLS s'il existe.
2. Chainlink OCR (déjà en biblio Kraidle) : relire le Lemme 8 et son modèle
   de fautes — la base de l'estimateur Shōgen.
3. Chercher la littérature sur la **mesure d'indépendance/défaillances
   corrélées** (common-mode failures, N-version programming — Knight &
   Leveson est le précédent classique à vérifier ; diversité des oracles).
   C'est le point où Shōgen peut être *neuf* au sens fort — la recherche de
   cette passe n'a rien trouvé d'industrialisé, absence à re-vérifier par
   une recherche dédiée.
4. ~~C2PA : lire la spec au texte~~ — **fait le 2026-07-30**
   (`c2pa-spec-2.4.html` détenu, sections lues : INDEX) ; le modèle
   « manifeste de provenance signé » est bien le cousin le plus proche du
   fait typé Shōgen.
5. ~~Écrire l'ADR-0001 puis la vision~~ — **fait le 2026-07-30** :
   ADR-0001 acceptée (`DECISIONS.md`), vision écrite (`02-vision.md`).
