# Shōgen — registre des décisions (ADRs)

| ADR | titre | statut | date |
|---|---|---|---|
| ADR-0001 | Les transports d'attestation sont des adapters — Shōgen n'en construit aucun | acceptée | 2026-07-30 |
| ADR-0002 | Encodage : CBOR déterministe (RFC 8949) + COSE (RFC 9052) | acceptée | 2026-07-30 |
| ADR-0003 | Le certificat est recalculable offline, jamais seulement émis | acceptée | 2026-07-30 |
| ADR-0004 | Multi-attestor : k témoignages agrégés au-dessus, jamais un objet co-signé | acceptée | 2026-07-30 |
| ADR-0005 | Rétention : hash toujours, octets par politique de classe, rédaction possible et déclarée | acceptée | 2026-07-30 |

---

## ADR-0001 — Les transports d'attestation sont des adapters — Shōgen n'en construit aucun

**Statut** : acceptée · 2026-07-30

### Contexte

Le champ zkTLS (« web proofs ») est passé des papiers aux SDKs : TLSNotary
(MPC, open source), Reclaim (proxy-witness, production), zkPass (hybride),
Opacity (réseau MPC), vlayer — recensés par l'index « zkTLS Canon » de
Reclaim et confirmés par la présence d'un « zkTLS Day » à Devconnect
(recherche du 2026-07-30, `docs/01-precedents.md`). La racine académique est
DECO (Zhang, Maram, Malvai, Goldfeder, Juels, CCS '20, détenue :
`biblio/deco-2019.pdf`) : prouver « that a piece of data accessed via TLS
came from a particular website », sans matériel de confiance ni coopération
du serveur. Les attestations TEE (lignée Marlin/Phala/Automata) couvrent le
cas calcul. La question : Shōgen doit-il construire son propre transport
attesté ?

### Décision

Non, jamais. Les transports — zkTLS proxy, zkTLS MPC, attestation TEE,
signature native de la source quand elle existe — sont des **adapters
interchangeables sous Shōgen**, au sens architectural que Kraidle donne à ce
mot : ils apportent les témoignages bruts, sont testés et jamais prouvés, et
la couche Shōgen (typage des faits, fraîcheur, quorum, mesure de diversité,
vérification du lot) ne dépend d'aucun d'eux en particulier. Le vocabulaire
de faits de Shōgen ne nomme aucun transport (l'analogue de R2 Kraidle).

### Alternative considérée

Construire un transport propriétaire (un notaire Shōgen). Rejetée : (a) le
champ est industrialisé et concurrentiel — y entrer coûterait l'essentiel de
l'effort pour un composant non différenciant ; (b) chaque transport porte un
modèle de menace distinct (la FAQ TLSNotary détenue : la preuve vaut envers
un vérificateur désigné et exige « trust in the notary's neutrality » si le
vérificateur n'a pas conduit le MPC lui-même) — en épouser un seul
importerait ses limites dans toute la pile ; (c) la valeur du projet est
au-dessus : c'est le gap §3 de `01-precedents.md`.

### La source qui tranche

TLSNotary, FAQ (détenue, grep vérifié) : le projet lui-même écrit qu'il
« does not solve the "Oracle Problem" ». Le transport le plus mûr du champ
déclare que la couche que Shōgen vise n'est pas son objet. DECO (abstract)
revendique la provenance, pas la vérité. La couche au-dessus est vacante.

### Ce que la décision coûte

- Une **hypothèse par transport**, au rang d'assumption nommée — le
  nommage est celui du registre de `03-temoignage.md` §2 :
  A(notary-neutrality), A(attestor-honesty), A(enclave-integrity),
  A(source-key) — chacune avec le résidu propre du mécanisme. Shōgen
  hérite de ces résidus et doit les publier par transport, jamais
  fusionnés — la règle des trois latences de Kraidle, transposée.
  *(Amendement du 2026-07-30, même jour : la première rédaction nommait un
  schéma provisoire A(transport-*) qui ne résolvait dans aucun registre —
  trouvaille « identifiants morts » de l'audit documentaire ; remplacé
  sans changer la décision.)*
- La qualité des témoignages bruts est bornée par l'écosystème externe
  (couverture TLS 1.2/1.3, sources supportées).
- Un travail d'interface : la forme canonique de témoignage que tous les
  adapters produisent — c'est le premier objet technique à spécifier.

### Registres touchés

Crée le besoin des registres : assumptions par transport et forme
canonique de témoignage — **ouverts le 2026-07-30** :
`08-assumptions.md` (le registre qui fait foi) et `03-temoignage.md`.

---

## ADR-0002 — Encodage : CBOR déterministe (RFC 8949) + COSE (RFC 9052)

**Statut** : acceptée · 2026-07-30

### Contexte

La forme canonique de témoignage (03 §5.1) et le lot vérifiable exigent un
encodage à représentation unique : deux encodeurs honnêtes produisent les
mêmes octets, sinon le hash du témoignage dépend de l'outil et la
vérification offline devient fragile.

### Décision

Payloads en CBOR contraint aux **Core Deterministic Encoding Requirements**
de RFC 8949 ; signatures et co-signatures en **COSE** (RFC 9052,
`Cose_Sign1` par défaut). La canonicalisation de `subject` (URL + requête
normalisées) est une sous-décision séparée, ouverte, qui n'est pas réglée
par le choix du conteneur.

### Alternative considérée

JSON + JCS (RFC 8785) : lisible, mais la canonicalisation JSON des nombres
est un terrain à défauts connus et l'écosystème de vérification visé
(no_std à terme, S3) favorise CBOR. Protobuf : représentation
déterministe non garantie par la spec, rejeté.

### La source qui tranche

Le précédent structurel du projet : C2PA 2.4 (détenu, vérifié par grep) —
la claim est « a CBOR payload, which shall comply with the Core
Deterministic Encoding Requirements of CBOR », signée en COSE (40
occurrences dans la spec). Le cousin le plus proche du fait typé fait
exactement ce choix, pour les mêmes raisons de vérifiabilité.

### Ce que la décision coûte

Une dépendance de parsing CBOR dans le vérificateur (S-G2 : elle devra
être minimale et sans réseau) ; l'outillage de debug est moins lisible que
JSON (atténué par une vue texte non normative). RFC 8949/9052 sont
détenues côté Kraidle (référence croisée — 08-assumptions, note 2).

### Registres touchés

03-temoignage §5.1 : fermé par cette ADR (reste `subject`, ouvert).

---

## ADR-0003 — Le certificat est recalculable offline, jamais seulement émis

**Statut** : acceptée · 2026-07-30

### Contexte

Le [à décider] majeur de 04 §5 : un certificat émis par Shōgen (signé,
opaque) ou recalculable par le vérificateur depuis les témoignages
embarqués ?

### Décision

**Recalculable.** Le lot embarque (ou référence par hash, avec
récupérabilité) les témoignages R2 et les données d'historique R1
nécessaires ; `shogen verify` recalcule partition, k_eff et statistiques
et compare au certificat. La signature de Shōgen sur le certificat est un
commodité de cache, jamais la racine de confiance.

### Alternative considérée

Certificat émis-signé seul : lots plus petits, mais il réintroduit
exactement la confiance que la vision exclut (« sans confiance dans
Shōgen », 02) — et il reproduirait la faiblesse d'INDaaS (détenu, p. 1
lue) : un *rapport d'audit* qu'on croit, au lieu d'un artefact qu'on
revérifie. Rejetée.

### La source qui tranche

02-vision (la promesse fondatrice) ; le contraste INDaaS ; et le GTM §4 :
la neutralité du benchmark n'est défendable que si « tout est
recalculable offline » (parade au risque n°1).

### Ce que la décision coûte

Volume du lot (les témoignages R2 sont des données réelles) — atténué par
hash + référence récupérable, à dimensionner en S4 ; et le vérificateur
doit implémenter la statistique R1 (complexité assumée, elle est le
produit).

### Registres touchés

04 §5 [à décider] : fermé. A(history-integrity) créée (08-assumptions).

---

## ADR-0004 — Multi-attestor : k témoignages agrégés au-dessus, jamais un objet co-signé

**Statut** : acceptée · 2026-07-30

### Contexte

03 §5.3 : un témoignage à k attestors du même transport est-il un objet
(co-signatures) ou k témoignages agrégés plus haut ?

### Décision

**k témoignages.** Un témoignage porte un attestor ; la redondance
d'attestors est traitée au rang du quorum, comme la redondance de
sources — et **l'ensemble des attestors entre dans les observables R2**
(le même attestor derrière deux témoignages « indépendants » est un mode
commun, exactement comme un amont partagé).

### Alternative considérée

L'objet co-signé (façon COSE multi-signataires) : lot plus compact, mais
il crée une *seconde* couche de quorum, interne au témoignage, dont la
diversité ne serait ni mesurée ni certifiée — l'anti-patron exact que le
projet reproche aux DONs (indépendance intra-objet postulée). Rejetée.

### La source qui tranche

Reclaim (détenu, grep) : l'architecture réelle du champ est à attestor
unique, la décentralisation n'étant qu'une parade évoquée — « The only
protection against fake proofs here is decentralisation or self-hosting
of the attestor » ; la forme à un attestor est le cas natif des
transports. Et le *mirroring* du whitepaper Chainlink v1 (détenu, §5.3
p. 19 lue au texte le 2026-07-30) : « a Sybil attacker can adopt a
behavior called *mirroring*, in which it causes oracles to send
individual responses based on data obtained from a *single data-source
query* … misbehaving oracles may share data off-chain but pretend to
source data independently » — toute agrégation dont les membres ne sont
pas comptés dans la diversité est une façade possible.

### Ce que la décision coûte

Pas de liaison anti-rejeu inter-attestors au rang du témoignage (chaque
témoignage porte la sienne) ; k attestations = k artefacts de preuve
(volume, cohérent avec le coût assumé d'ADR-0003).

### Registres touchés

03 §5.3 : fermé. 04 §1 (ligne R2) : les attestors sont un axe R2
explicite — **porté le 2026-07-30**.

---

## ADR-0005 — Rétention : hash toujours, octets par politique de classe, rédaction possible et déclarée

**Statut** : acceptée · 2026-07-30

### Contexte

03 §5.4 : conserver l'`utterance` complète (rejouabilité, détection
d'amont commun par corrélation de contenu) ou hash + extraction (vie
privée, volume) ?

### Décision

Trois règles : (1) le **hash des octets exacts est toujours porté** — il
lie le témoignage à sa preuve de transport, sans exception ; (2) la
rétention des octets est une **politique par classe de faits** (défaut
pour les classes de marché : rétention, fenêtre à dimensionner en S2) ;
(3) une **rédaction** (suppression de sous-chaînes sensibles) est
possible mais **déclarée dans le témoignage**, et le certificat dit
quelles entrées étaient rédigées.

### Alternative considérée

Hash-seul systématique : minimal et privé, mais il tue l'observable
« corrélation de contenu » (détection d'amont commun, R2) et la
rejouabilité du typage — le cœur différenciant paierait le choix.
Rejetée en défaut, disponible par classe.

### La source qui tranche

DECO §3.4.3 (détenu, lu) : le champ a déjà tranché la même tension par le
**selective opening** — « revealing a substring to V or redacting, i.e.,
excising, a substring, concealing it from V » — la rédaction déclarée est
la forme standard, pas une invention.

### Ce que la décision coûte

Le coût est *nommé dans le certificat* : une entrée rédigée est exclue de
la corrélation de contenu, donc l'axe amont-commun de son témoignage est
non mesuré (A(axis-coverage) s'élargit d'autant, visiblement). Stockage
et vie privée par classe à spécifier en S2/S4.

### Registres touchés

03 §5.4 : fermé. 04 §4, item 5 : la liste des entrées rédigées est au
périmètre embarqué du certificat — **porté le 2026-07-30**.
