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
sources, et le témoignage le porte par référence. **Le registre qui fait
foi est `08-assumptions.md`** (format A(...) complet : assurance, sites
porteurs, condition de décharge) ; la table ci-dessous en est le rappel
au point d'usage :

| transport | résidu (hypothèse nommée) | source du résidu (détenue) |
|---|---|---|
| `tlsn-mpc` | A(notary-neutrality) : la preuve vaut envers un vérificateur désigné ; s'il n'a pas conduit le MPC lui-même, il doit « trust in the notary's neutrality » — **et, pour la durée de S3, A(self-attestation)** : le notaire est opéré par Shōgen (ADR-0015 pt 4, service public amont arrêté) | FAQ TLSNotary, grep vérifié ; ADR-0015 |
| `proxy-witness` | A(attestor-honesty) : un attestor compromis ne lit pas les données mais **peut forger des preuves** — « The only protection against fake proofs here is decentralisation or self-hosting of the attestor » | FAQ sécurité Reclaim, copie du 2026-07-30 |
| `tee-*` | A(enclave-integrity) : l'attestation vaut ce que vaut l'enclave et sa chaîne d'attestation | DECO §3.1 (détenu, lu) : « If a single TEE is broken, TLS session content, including user credentials, can leak » |
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

Pour un témoignage isolé : (1) le `transport_proof` se vérifie avec
l'outil du transport contre les clés épinglées de `attestor` — **et pour
les transports à vérificateur participant (MPC, 3P-handshake), cette
étape n'a de valeur pour un tiers que sous A(verifier-designation)** : ce
que le tiers vérifie alors est la signature du participant, pas le
transport. *(Forme fixée par ADR-0015 pour S3 : ce contrôle est délégué au
binaire compagnon `shogen-tlsn-verify` construit depuis l'amont épinglé ;
`shogen-verifier` contrôle la liaison hash→preuve et son verdict nomme la
délégation — A(transport-check-delegated).)* ; (2) le hash de `utterance`
correspond ; (3) le `residual` résout dans le registre publié.
Le verdict du vérificateur nomme le résidu : « témoignage valide **sous
A(attestor-honesty)** » — jamais « témoignage vrai ».

Pour un lot (verdict de quorum) : s'ajoutent la fenêtre de fraîcheur, la
liste des résidus, et le **certificat de diversité** — spécifié dans un
document séparé, car il a son propre appareil (les axes mesurés, la leçon
Knight & Leveson §4 : un axe déclaré n'est pas un axe protecteur).

## 5. [À décider] — état au 2026-07-30 (S1)

1. ~~Encodage concret~~ — **tranché par ADR-0002** : CBOR déterministe
   (RFC 8949) + COSE (RFC 9052), précédent C2PA vérifié au fichier.
   **Reste ouvert** : la canonicalisation de `subject` (sous-décision
   explicitement non réglée par l'ADR).
2. ~~Le registre des résidus~~ — **fait** : `08-assumptions.md` (v1), les
   identifiants du §2 y résolvent tous.
3. ~~Multi-attestor~~ — **tranché par ADR-0004** : k témoignages agrégés
   au-dessus ; les attestors deviennent un axe R2 du certificat.
4. ~~Rétention~~ — **tranché par ADR-0005** : hash toujours, octets par
   politique de classe, rédaction possible et déclarée (précédent DECO
   §3.4.3, selective opening).
