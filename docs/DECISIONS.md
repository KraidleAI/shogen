# Shōgen — registre des décisions (ADRs)

| ADR | titre | statut | date |
|---|---|---|---|
| ADR-0001 | Les transports d'attestation sont des adapters — Shōgen n'en construit aucun | acceptée | 2026-07-30 |
| ADR-0002 | Encodage : CBOR déterministe (RFC 8949) + COSE (RFC 9052) | acceptée | 2026-07-30 |
| ADR-0003 | Le certificat est recalculable offline, jamais seulement émis | acceptée | 2026-07-30 |
| ADR-0004 | Multi-attestor : k témoignages agrégés au-dessus, jamais un objet co-signé | acceptée | 2026-07-30 |
| ADR-0005 | Rétention : hash toujours, octets par politique de classe, rédaction possible et déclarée | acceptée | 2026-07-30 |
| ADR-0006 | Aucun token, aucun calcul on-chain — l'ancrage reste ouvert | acceptée | 2026-07-30 |
| ADR-0007 | La profondeur du marché de référence n'est pas un axe — le certificat nomme l'amont, il ne le note pas | acceptée | 2026-07-31 |

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
Deterministic Encoding Requirements of CBOR », signée en COSE (56
occurrences du mot sur 40 lignes de la copie détenue). Le cousin le plus proche du fait typé fait
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

02-vision (la promesse fondatrice) ; le contraste INDaaS ; et le GTM (thèse
de neutralité au §4 ; parade au risque n°1 au §6, où la chaîne « tout est
recalculable offline » est écrite verbatim).

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

---

## ADR-0006 — Aucun token, aucun calcul on-chain — l'ancrage reste ouvert

**Statut** : acceptée · 2026-07-30

### Contexte

La quasi-totalité des acteurs visés (protocoles de prêt, réseaux d'oracle,
cabinets de risque) opère on-chain, et le mainteneur a posé la question de
notre absence de présence sur chaîne. L'analyse distingue **trois surfaces
qu'on confond souvent** : y *calculer*, y *ancrer* un engagement, y *lire*
une valeur. Elles n'ont ni le même coût, ni le même risque.

### Décision

1. **Aucun token, jamais** — sur ce projet comme sur ses frères.
2. **Aucun calcul on-chain** : le test R1 (milliers de fenêtres, matrices
   de corrélation) reste hors ligne ; c'est précisément ce que la
   vérifiabilité hors ligne existe pour permettre.
3. **L'ancrage reste une question ouverte**, avec une recommandation
   consignée : publier périodiquement un engagement (hash / racine de
   Merkle) des certificats émis, dès l'existence du benchmark public (S2).
   Non tranché ici — la décision appartient au mainteneur.
4. **Invariant qui borne toute présence future** : ce qui irait sur la
   chaîne serait un **engagement**, jamais une **affirmation**. Publier
   k_eff comme valeur à croire ferait de Shōgen un oracle à l'indépendance
   postulée — l'auto-réfutation exacte que le projet combat. La valeur
   voyage avec sa preuve, la chaîne n'atteste que la non-répudiation.

### Alternative considérée

Un token de protocole avec période de contestation, staking et slashing —
la forme optimiste qui rendrait le certificat contestable économiquement.
Rejetée : elle transforme un instrument de mesure en protocole à
gouverner, et surtout elle **détruit le moat**. Notre différenciation est
qu'un certificat émis par un tiers neutre vaut ce que l'auto-notation d'un
mesuré ne vaudra jamais (GTM §4) ; un jeton fait de nous une partie
intéressée au résultat de nos propres mesures.

### La source qui tranche

Décision du mainteneur, énoncée le 2026-07-30 — assurance : *reviewed*
(mainteneur, 2026-07-30), pas *proven* ni *tested*. Elle est renforcée par
un argument interne : le risque n°1 du GTM (riposte narrative sur la
méthodologie) ne se pare que par la neutralité vérifiable, qu'un token
compromettrait.

### Ce que la décision coûte

Pas de financement par émission ; le revenu vient des canaux 1 à 4 du GTM.
Pas de mécanisme de contestation économique — la contestation reste
scientifique (recalculer hors ligne et publier le contre-calcul), ce qui
est cohérent avec le produit mais plus lent qu'un slashing.

### Registres touchés

`05-roadmap.md` §Non-buts : « pas de token, pas de chaîne » est trop large
et devient « pas de token, pas de calcul on-chain ; ancrage : question
ouverte, ADR-0006 » — **porté le 2026-07-30**. Si l'ancrage est adopté, il
décharge partiellement A(history-integrity) (`08-assumptions.md`), sa
seule voie de décharge connue à ce jour.

---

## ADR-0007 — La profondeur du marché de référence n'est pas un axe — le certificat nomme l'amont, il ne le note pas

**Statut** : acceptée · 2026-07-31

### Contexte

L'incident SK Hynix du 28 juillet 2026 (Galaxy Research, détenu :
`biblio/galaxy-2026-07-31-tradexyz-oracle.html`, citations vérifiées par
grep) : une action s'échange à 1 272 000 won, « 29.96% below the previous
close », dans les premières secondes du pré-marché NextTrade ; le prix se
propage et déclenche ≈ 60 M$ de liquidations. L'article qualifie lui-même
la lecture de **« accurate but anomalous »** — une exécution réelle a eu lieu à ce prix, au sens de l'article — et
conclut : « The oracle worked. The risk system didn't. »

Deux constats pour nous. **Le premier illustre exactement ce que le rang R2 existe pour révéler** : le prix de
référence est « the median of three inputs: the oracle price, the oracle
plus a 150-second exponential moving average of the book's deviation from
it, and the median of best bid, best ask, and last trade » — deux des
trois entrées sont des fonctions de la même entrée, soit k nominal = 3
pour un k_eff ≤ 2, et le cluster décide la médiane. C'est exactement
l'illusion de redondance que le rang R2 existe pour révéler. **Le second
ouvre une dette** : la cause racine tient à la profondeur du marché cité,
qui n'est aucun de nos axes.

### Décision

La profondeur, la liquidité et plus généralement la **qualité du marché
sous-jacent ne sont pas des axes du certificat** — c'est un non-but
explicite. En contrepartie, obligation nouvelle : **le certificat nomme
les amonts identifiés par la partition**, et pas seulement leur nombre.
Il écrit « cluster A = {src1, src2} via place X », jamais « 3 sources → 2
clusters ». Nommer l'amont rend la question de la profondeur *répondable*
par celui à qui elle appartient ; la noter nous-mêmes ferait de nous
autre chose.

### Alternative considérée

Ajouter la profondeur comme axe R2 (carnet, volume, spread de la place
citée). Rejetée pour trois raisons : (a) ce n'est pas une propriété
d'**indépendance** — la profondeur qualifie *une* source, quand nos axes
qualifient une *relation entre* sources, et mélanger les deux brouille ce
que k_eff signifie ; (b) c'est un autre métier, avec d'autres
concurrents établis (fournisseurs de données de marché), et il diluerait
la seule revendication qui nous distingue ; (c) il nous placerait en
notation de qualité, cousine du jugement de vérité que la vision
interdit.

### La source qui tranche

L'article lui-même situe la couche fautive : « The oracle worked. The
risk system didn't », et rappelle que « Traditional markets separated
last trade, index price, and fair value for risk purposes decades ago,
precisely so one local execution cannot decide the fate of a leveraged
account » — la séparation dire / référence / valeur de risque est
exactement la nôtre (témoignage / fait / verdict), et la profondeur
appartient au dernier étage, celui du système de risque, qui n'est ni
Shōgen ni Kraidle.

### Ce que la décision coûte

**Nous ne couvrons pas la classe de défaillance SK Hynix**, et il faut le
dire là où un lecteur pourrait croire l'inverse : le panneau « ce que ce
certificat ne dit pas » (04 §4, planche 6 du dossier) gagne une ligne
explicite sur la qualité du marché sous-jacent. Un prospect qui cherche
une couverture du risque de profondeur doit être redirigé, pas converti.
Contrepartie assumée : c'est ce qui rend le canal 1 du GTM (cabinets de
risque) complémentaire plutôt que concurrent — nous livrons la partition
nommée, ils en tirent le prix du risque de profondeur.

### Registres touchés

`04-certificat-diversite.md` §3 (le certificat nomme les amonts) et §4
(nouvelle limite publiée) — **portés le 2026-07-31**.
`09-vocabulaire.md` : nouvelle formulation interdite — « Shōgen évalue la
qualité d'une source » — **portée**. `05-roadmap.md` §Non-buts —
**porté**. Le [à décider] de 04 §2 sur la stratification des fenêtres par
régime gagne son cas motivant : l'ouverture de pré-marché illiquide est
précisément le régime où A(window-stationarity) casse.
