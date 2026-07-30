# La forme canonique de témoignage — spécification v0 (2026-07-30)

> Statut : premier jet. Rien ici n'est proven ni tested. C'est le coût nommé
> d'ADR-0001 (« un travail d'interface : la forme canonique de témoignage
> que tous les adapters produisent ») payé en spécification. Les choix
> marqués **[à décider]** attendent un ADR.

## 0. Le principe de construction

La forme canonique est à Shōgen ce que la forme canonique d'action est à
l'émetteur de Kraidle (ADR-0100 Kraidle) : **elle n'a pas de slot pour ce
que la couche au-dessus ne doit pas croire**. Un témoignage ne porte aucun
champ « vérité », aucun champ « qualité de la source », aucun champ
« confiance » — ces jugements n'existent pas à ce rang. Il porte
exclusivement ce qui a été observé, par quel mécanisme, et ce que ce
mécanisme laisse comme résidu.

Le précédent de structure est C2PA 2.4 (détenu) : assertions → claim signé
→ claim signature, avec le refus explicite du jugement de valeur (« SHOULD
NOT provide value judgments », vérifié au fichier). Shōgen adopte la même
stratification avec un vocabulaire propre.

## 1. Le témoignage (shōgen) — l'objet

Champs, tous obligatoires sauf mention :

| champ | contenu | pourquoi |
|---|---|---|
| `subject` | désignation canonique de la source interrogée (domaine + endpoint normalisé + paramètres de requête normalisés) | ce dont on témoigne |
| `utterance` | les octets exacts de la réponse (ou leur hash + extraction, voir §3) | le « dire » — jamais interprété à ce rang |
| `observed_at` | instant de l'observation, avec l'horloge qui l'a produit (celle du transport, jamais celle de Shōgen) | la fraîcheur se calcule plus haut ; ici on enregistre qui a daté |
| `transport` | identifiant du mécanisme d'attestation (ex. `tlsn-mpc/1`, `proxy-witness/1`, `tee-sgx/1`, `source-sig/1`) | chaque transport a un modèle de menace distinct |
| `transport_proof` | l'artefact de preuve du transport, opaque pour Shōgen, vérifiable par l'outil du transport | Shōgen ne re-spécifie pas les transports (ADR-0001) |
| `residual` | **l'identifiant de l'hypothèse résiduelle du transport**, résolu dans le registre des assumptions | voir §2 — le champ central |
| `attestor` | identité(s) de l'attestateur/notaire/enclave impliqué, clés épinglées | qui pourrait forger, nominativement |

Ce que la forme n'a **pas** : de champ vérité, de score de confiance, de
« validated ». Et le témoignage ne tire aucun paramètre de la requête qu'il
médiatise au-delà de `subject` normalisé — la leçon R4/ADR-0100 de Kraidle,
transposée.

## 2. Le résidu par transport — des hypothèses nommées, jamais fusionnées

Chaque transport importe un résidu distinct, documenté par ses propres
sources, et le témoignage le porte par référence. Registre initial
(chaque entrée à développer au format A(...) avec niveau d'assurance et
condition de décharge) :

| transport | résidu (hypothèse nommée) | source du résidu (détenue) |
|---|---|---|
| `tlsn-mpc` | A(notary-neutrality) : la preuve vaut envers un vérificateur désigné ; s'il n'a pas conduit le MPC lui-même, il doit « trust in the notary's neutrality » | FAQ TLSNotary, grep vérifié |
| `proxy-witness` | A(attestor-honesty) : un attestor compromis ne lit pas les données mais **peut forger des preuves** — « The only protection against fake proofs here is decentralisation or self-hosting of the attestor » | FAQ sécurité Reclaim, copie du 2026-07-30 |
| `tee-*` | A(enclave-integrity) : l'attestation vaut ce que vaut l'enclave et sa chaîne d'attestation | à documenter (littérature TEE, dette) |
| `source-sig` | A(source-key) : la clé de la source est la bonne et n'est pas compromise | à documenter |

**Règle transposée de Kraidle (les trois latences, RFC 5280 §3.3)** : les
résidus se publient par mécanisme, jamais agrégés en un « niveau de
sécurité » unique. Un lot mélangeant des transports porte la liste de ses
résidus, pas leur moyenne.

## 3. `utterance` : octets exacts, extraction séparée

Deux rangs, jamais confondus :

- **Le dire brut** : hash des octets exacts de la réponse (le lien au
  `transport_proof`).
- **L'extraction** : le passage du brut au fait typé (« ce JSON, champ
  `price`, vaut 42,17 USDC ») est le travail d'un **typeur**, adapter
  identifié, testé jamais prouvé, dont l'identité et la version figurent
  dans le *fait*, pas dans le témoignage. Un témoignage peut porter
  plusieurs extractions concurrentes ; le fait cite la sienne.

C'est la séparation adapter/kernel de Kraidle : le témoignage est
l'artefact de frontière, le typage est de la plomberie testée, et rien en
aval ne re-décide ce que les octets « voulaient dire » sans citer son
typeur.

## 4. Ce qu'un vérificateur offline vérifie (cible)

Pour un témoignage isolé : (1) le `transport_proof` se vérifie avec l'outil
du transport contre les clés épinglées de `attestor` ; (2) le hash de
`utterance` correspond ; (3) le `residual` résout dans le registre publié.
Le verdict du vérificateur nomme le résidu : « témoignage valide **sous
A(attestor-honesty)** » — jamais « témoignage vrai ».

Pour un lot (verdict de quorum) : s'ajoutent la fenêtre de fraîcheur, la
liste des résidus, et le **certificat de diversité** — spécifié dans un
document séparé, car il a son propre appareil (les axes mesurés, la leçon
Knight & Leveson §4 : un axe déclaré n'est pas un axe protecteur).

## 5. [À décider] — matière des prochains ADRs

1. Encodage concret (CBOR déterministe ? le précédent COSE/C2PA à
   examiner) et canonicalisation de `subject`.
2. Le registre des résidus : format A(...) complet, niveaux, conditions de
   décharge.
3. Multi-attestor : Reclaim documente un attestor unique ; un témoignage
   Shōgen à k attestors du même transport est-il un objet (co-signatures)
   ou k témoignages agrégés plus haut ? [pèse sur le certificat de
   diversité]
4. La politique de rétention des octets bruts (`utterance` complète vs
   hash + extraction — vie privée vs rejouabilité).
