# Shōgen — registre des décisions (ADRs)

| ADR | titre | statut | date |
|---|---|---|---|
| ADR-0001 | Les transports d'attestation sont des adapters — Shōgen n'en construit aucun | acceptée | 2026-07-30 |
| ADR-0002 | Encodage : CBOR déterministe (RFC 8949) + COSE (RFC 9052) — sous-décision `subject` fermée par ADR-0016 le 2026-08-13 | acceptée | 2026-07-30 |
| ADR-0003 | Le certificat est recalculable offline, jamais seulement émis | acceptée | 2026-07-30 |
| ADR-0004 | Multi-attestor : k témoignages agrégés au-dessus, jamais un objet co-signé | acceptée | 2026-07-30 |
| ADR-0005 | Rétention : hash toujours, octets par politique de classe, rédaction possible et déclarée | acceptée | 2026-07-30 |
| ADR-0006 | Aucun token, aucun calcul on-chain — l'ancrage reste ouvert | acceptée | 2026-07-30 |
| ADR-0007 | La profondeur du marché de référence n'est pas un axe — le certificat nomme l'amont, il ne le note pas | acceptée | 2026-07-31 |
| ADR-0008 | Une arête d'amont `basis:doc` ne partitionne pas k_eff ; elle déclenche la mesure de contenu | acceptée | 2026-08-05 |
| ADR-0009 | Stack et toolchain : Rust, `forbid(unsafe_code)` sur cœur et vérificateur, toolchain épinglée | acceptée (ratifiée par délégation mainteneur du 2026-08-12) | 2026-08-12 |
| ADR-0010 | Architecture : cœur pur, total, sans I/O, sans panique ; découpe par information hiding ; coquille impérative | acceptée (ratifiée par délégation mainteneur du 2026-08-12) | 2026-08-12 |
| ADR-0011 | Tests : pyramide par rôle, property-based sur le cœur, mutation en validateur, couverture en garde-fou — 7 seuils candidats | acceptée (ratifiée par délégation mainteneur du 2026-08-12) | 2026-08-12 |
| ADR-0012 | Environnement : le lockfile fait foi, exact au manifeste sur cœur/vérificateur, R-8 en deux moitiés, reproductibilité bit-à-bit du vérificateur visée, SLSA L2 candidat | acceptée (ratifiée par délégation mainteneur du 2026-08-12) | 2026-08-12 |
| ADR-0013 | DevOps : gates bloquantes (doctrine gatewright : mutant semé tué), trunk-based sur main protégée, CI Windows+Linux, actions épinglées SHA, JOURNAL opposable | acceptée (ratifiée par délégation mainteneur du 2026-08-12) | 2026-08-12 |
| ADR-0014 | Licence : décision contractée à l'entrée de S3 (dette prudente-délibérée, Fowler/G5) ; crates non publiables d'ici là, gate re-serrée mécaniquement | acceptée (ratifiée par délégation mainteneur du 2026-08-12) | 2026-08-12 |
| ADR-0015 | Transport de S3 : TLSNotary `tlsn-mpc/1` en mode Notary (notaire opéré par Shōgen, résidu aggravé A(self-attestation)) ; vérification déléguée à un binaire compagnon épinglé — `shogen-verifier` reste à zéro dépendance | acceptée (adjugée orchestrateur sur pièces — révision mainteneur ouverte) | 2026-08-13 |
| ADR-0016 | Canonicalisation de `subject` : forme construite à l'adapter, prédicat total au cœur, refus nommés, requête verbatim jamais triée — ferme la sous-décision ouverte d'ADR-0002 | acceptée (adjugée orchestrateur sur pièces — révision mainteneur ouverte) | 2026-08-13 |

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

---

## ADR-0008 — Une arête d'amont `basis:doc` ne partitionne pas k_eff ; elle déclenche la mesure de contenu

**Statut** : acceptée · 2026-08-05 (décision déléguée à l'orchestrateur — révision mainteneur ouverte)

### Contexte

Le pool S2 (décidé le 2026-08-05, 10 §9) inclut agrégateurs et oracles,
dont les liens d'amont sont d'abord connus par **déclaration
documentaire** (CoinGecko ← Binance, Pyth ← Coinbase, DefiLlama ←
CoinGecko — 10 §4.3), pas par mesure. La question, structurante pour
k_eff : une arête d'amont établie seulement par doc (`basis:doc`)
doit-elle réduire k_eff — fusionner deux sources dans une même classe de
partition — au même titre qu'une arête **mesurée** (`basis:measured` :
ASN partagé re-mesuré, ou co-résidus corrélés) ?

### Décision

Une arête `basis:doc` seule **ne réduit pas k_eff**. Elle **déclenche** la
mesure de contenu (b) (10 §4.2) sur la paire concernée, et ne partitionne
(fusionne) qu'une fois **corroborée `basis:measured`**. C'est la
hiérarchie des rangs R2 (a/b mesurés > c déclaré, 04 §1) appliquée à
l'intérieur du calcul de partition : une déclaration d'amont, seule, ne
fait pas chuter un quorum — elle désigne **où** mesurer.

### Alternative considérée

Faire chuter k_eff dès la déclaration doc (traiter `basis:doc` ≡
`basis:measured`). Rejetée : (a) elle donne un poids protecteur à une
déclaration invérifiée — exactement le rang R3 que 04 §1 refuse de
compter ; (b) une source pourrait **gonfler** sa diversité apparente en
cachant un amont documentaire (fausse indépendance), ou une source
honnête serait pénalisée par une doc périmée ; (c) elle rend k_eff
tributaire de la fraîcheur et de l'honnêteté d'une page web, pas d'une
mesure recalculable.

### La source qui tranche

Décision **déléguée par le mainteneur à l'orchestrateur** le 2026-08-05
(« choisis chaque dilemme avec rigueur académique, solutions
documentées »), tranchée sur pièce et non par préférence. Le précédent
académique qui la fonde : **INDaaS** (Zhai, Chen, Wolinsky, Ford, 2014,
détenu) — « seemingly independent systems may share deep, hidden
dependencies » — construit un service qui **audite** les dépendances au
lieu de les croire déclarées ; c'est exactement « ne pas partitionner sur
du déclaré, mesurer d'abord ». Renfort : Chainlink v1 (détenu) nomme le
vecteur — des oracles qui « pretend to source data independently ». Et
c'est la hiérarchie R2 déjà actée (04 §1, mesuré > déclaré) appliquée au
calcul de partition. Assurance : décision déléguée, **fondée sur les
précédents cités** (INDaaS, Chainlink v1, 04 §1) — ni proven ni tested,
et pas encore *reviewed* : la révision du mainteneur reste ouverte.

### Ce que la décision coûte

Un amont réel que la mesure de contenu ne capte pas (un copieur qui
**bruite** ses copies — 10 §4.2, A(axis-coverage)) restera compté comme
deux classes tant que `basis:measured` n'est pas atteint : k_eff peut donc
**surestimer** la diversité dans ce cas précis. C'est le prix de ne pas
faire confiance aux déclarations. Garde-fous : l'arête `basis:doc` est
publiée (visible au lecteur), et le drapeau « co-défaillance observée non
expliquée par les axes R2 » (04 §3 ; 10 §5.6) teste A(axis-coverage) en
continu.

### Registres touchés

`04-certificat-diversite.md` §3 (calcul de k_eff) — à porter à la
prochaine passe docs (10 dette §10.11, avec les autres fermetures dues à
04). `docs/10-mesures-pilotes-design.md` §3.2, §4.3, §5.6 : la règle y est
écrite. `09-vocabulaire.md` : candidate — « une arête déclarée fait
chuter k_eff » comme formulation interdite. **Accepté le 2026-08-05** : la
règle est invariante du calcul de partition en S2 — `partition.py`
l'applique, et un test la vérifie (une arête `basis:doc` seule laisse
k_eff inchangé).

---

## ADR-0009 — Stack et toolchain du produit : Rust pour `shogen-core`, `shogen-verifier` et les adapters, toolchain épinglée par fichier committé

**Statut** : acceptée · 2026-08-12 · ratifiée le 2026-08-12 par délégation explicite du mainteneur (« je délègue cette décision à mon agent orchestrateur… les réponses doivent se baser sur une étude académique rigoureuse ») — seuils chiffrés ratifiés comme **budgets déclarés révisables par ADR**, au statut exact que leurs sources autorisent

**Adjudication orchestrateur (2026-08-12)** : draft rendu par un worker de
la passe S2.5 (run `wf_e704a674-9da`) ; les 34 citations du draft ont été
re-établies par l'orchestrateur avant écriture — 28 relues aux fichiers
détenus (RustBelt pp. 66:1-66:3 ; CACM version auteur pp. 1-3 ; CISA
pp. 4-5, 9-10, 13, 19-20), 6 contrôlées aux documents internes — et la
mesure de toolchain a été re-exécutée par l'orchestrateur (frontière de
passe). Une citation tronquée du draft a été complétée à sa forme du texte.

### Contexte

`DEVOPS.md` présuppose déjà la stack — il nomme `rust-toolchain.toml`,
`cargo-deny` et un `Cargo.lock` committé (§4) — tout en se déclarant en
tête « plan, rien n'est encore en place ». La passe S2.5 existe pour
convertir ce présupposé en choix instruit (12 §1) : aucun code produit
avant que la fondation ne soit tracée.

Le choix n'est pas libre — quatre bornes déjà fermées le contraignent :

1. **ADR-0002** : payloads en CBOR déterministe + COSE, et le motif de
   rejet de JSON/JCS y est écrit — « l'écosystème de vérification visé
   (no_std à terme, S3) favorise CBOR ». La cible `no_std` du vérificateur
   est donc *déjà* une borne, datée « à terme, S3 ».
2. **ADR-0003** : le certificat est recalculable offline ; le vérificateur
   doit implémenter la statistique R1, pas seulement lire une signature.
3. **DEVOPS §1** : « un vérificateur fermé contredit la vision » — le
   binaire du vérificateur est l'artefact qu'un tiers doit pouvoir
   reconstruire, donc la chaîne de compilation est une pièce du produit,
   pas un détail d'atelier.
4. **DEVOPS §3, gates S-G2 et S-G3** : le vérificateur ne doit avoir ni
   arête vers un adapter ni « dépendance réseau/horloge », et « un
   vérificateur qui panique sur un lot malveillant est un déni qui ne dit
   pas son nom ».

Les critères d'arbitrage sont ceux du 12 §3 : sûreté mémoire à fondation
académique ; aptitude `no_std` et dépendances minimales du vérificateur ;
déterminisme ; écosystème CBOR/COSE ; outillage de chaîne
d'approvisionnement. Le harnais Python de S2 est **hors-champ** : jetable
(10 §1), il n'est pas un ancêtre du produit.

Un fait de contexte, mesuré par l'orchestrateur dans la passe qui écrit
cette ADR (2026-08-12, rejouable) : la machine du mainteneur porte
`rustc 1.97.1 (8bab26f4f 2026-07-14)`, `cargo 1.97.1 (c980f4866
2026-06-30)`, `rustup 1.29.0`, toolchain active
`stable-x86_64-pc-windows-msvc` (`rustc --version`, `cargo --version`,
`rustup show active-toolchain`). Aucun artefact bibliographique sur les
versions de Rust n'est détenu — ce chiffre est une **mesure locale**, pas
une citation.

### Décision

1. **Rust** pour les trois rôles du workspace (`shogen-core`,
   `shogen-verifier`, `adapters/*`). Un seul langage produit ; pas de
   cœur dans un second langage.
2. **`#![forbid(unsafe_code)]` sur `shogen-core` et `shogen-verifier`**, et
   sur tout adapter sauf ADR contraire. Raison exacte : ce qui est
   machine-checked par RustBelt est le fragment *sans* `unsafe` ; le mot-clé
   `unsafe` est précisément ce qui porte l'obligation de preuve (« for each
   new Rust library that uses unsafe features, we can say what verification
   condition it must satisfy »). L'interdit est une gate, pas une intention
   — il rejoint la famille S-G3.
3. **Toolchain épinglée par `rust-toolchain.toml` committé** : version
   exacte (pas `stable`), composants et cibles déclarés ; la CI Windows et
   Linux consomme ce même fichier, jamais un canal flottant. La *politique*
   d'épinglage des dépendances (lockfile, `cargo-deny`, vendoring) n'est pas
   tranchée ici : elle appartient à **ADR-0012**, à qui ce point est passé
   avec le critère « chaîne d'approvisionnement outillée ».
4. **MSRV = la version épinglée**, déclarée mécaniquement en manifeste
   (`rust-version`). Valeur candidate : **`1.97`** (toolchain `1.97.1`) —
   *candidat — ratification mainteneur due*.
5. **Edition 2024** — *candidat — ratification mainteneur due*.
6. **Cible `no_std` du vérificateur : à terme (S3), pas immédiate** —
   *candidat — ratification mainteneur due*. En S2.5, le walking skeleton
   pose et **teste** les contraintes qui rendent ce basculement possible :
   pas de dépendance réseau ni d'horloge (S-G2), le vérificateur compile
   avec `--no-default-features`, l'arête de dépendance va du vérificateur
   vers le cœur et jamais l'inverse. `#![no_std]` + `alloc` devient une
   gate en S3, cohérent avec le « no_std à terme, S3 » d'ADR-0002.
7. **Zéro `unsafe` admis** dans `shogen-core` et `shogen-verifier` —
   plancher chiffré 0, mesuré par la gate — *candidat — ratification
   mainteneur due*.

Ce que cette décision **ne dit pas**, et qui doit être écrit ici pour que
personne ne le lise à l'envers : elle ne rend notre code ni correct ni
exempt de défauts. Ce qui est *proven* (machine-checked) l'est d'un langage
formalisé — les auteurs écrivent « we do not consider the full Rust
language, for which no formal description exists anyway » — donc ni de
`rustc`, ni de la bibliothèque standard, ni de Shōgen. La classe de défauts
« sûreté mémoire » est retirée du fragment sans `unsafe`, selon les pièces
citées ; tout le reste reste à tester.

### Alternative considérée

**C/C++ contemporain — rejeté.** Le dossier interagences le classe sans
ambiguïté : « Programming languages such as C and C++ are examples of memory
unsafe programming languages that can lead to memory unsafe code and are
still among the most widely used languages today » (CISA et al. 2023, p. 5).
L'argument technique qui compte pour nous est celui de RustBelt p. 66:2 :
le C++ moderne offre bien des mécanismes d'ownership (RAII, smart pointers),
mais « the type system of C++ is too weak to enforce its ownership
disciplines statically, so it is still easy to write programs with unsafe or
undefined behavior using these features » — une discipline non tenue par le
type system est une convention, et une convention ne franchit pas une gate.
Motif propre à Shōgen : un vérificateur au comportement indéfini sur un
octet muté n'échoue pas fail-closed, il échoue *sans le dire* — exactement
le déni que S-G3 existe pour interdire.

**Go — rejeté**, bien qu'il soit co-listé comme langage à sûreté mémoire par
le dossier interagences (annexe p. 19 : « It is syntactically like C, but
with memory safety, garbage collection, and structural typing »). Deux
motifs sur pièce : (a) le ramasse-miettes — « Some MSLs use a garbage
collector as part of their memory management. The process of garbage
collecting can introduce unpredictable latency » (CISA p. 13), et « these
performance characteristics can still affect constrained devices, such as
those in embedded systems » (même page) : la cible `no_std`/dépendances
minimales d'ADR-0002 suppose un binaire sans runtime imposé, ce qu'un
langage à GC obligatoire ne propose pas ; (b) la maîtrise de la
représentation — « Languages like Java, Go, and OCaml avoid use-after-free
bugs using garbage collection » et, sur le prix payé par cette famille de
langages (le « boxing » des éléments), « This sacrifices performance and
control over memory layout in return for safety » (Jung et al. 2021,
version auteur, p. 2). Or l'objet même du produit est un encodage
à représentation unique (ADR-0002) : abandonner la maîtrise de la
représentation est le mauvais échange ici. Motif complémentaire, même
source p. 1 : sur les courses de données, « most "safe" languages (such as
Java and Go) permit them, and they are a reliable source of concurrency
bugs », là où le « type system rules out data races at compile time » en
Rust.

**Zig — rejeté faute de pièce, et le motif est nommé comme tel.** Aucun
artefact sur Zig n'est détenu dans `biblio/` ; le langage ne figure pas dans
l'annexe « Memory Safe Languages » du dossier interagences (p. 19, qui liste
C#, Go, Java, Python, Rust, Swift). L'absence d'une liste n'est pas une
réfutation, et cette ADR ne la présente pas comme telle : elle signifie que
le critère n°1 (sûreté mémoire à fondation académique ou institutionnelle)
**ne peut pas être instruit sur pièce** pour Zig. Retenir Zig serait une
préférence non tracée ; le rejeter *sur pièce* exige une acquisition. La
demande est portée en manque (documentation officielle du langage, section
sûreté mémoire, copie datée) — si le mainteneur veut l'option rouverte, elle
se rouvre par acquisition, pas par argument.

**OCaml ou Haskell pour le cœur pur — rejeté.** Trois motifs : (a) même
objection GC, et OCaml est nommément dans la liste des langages à GC (Jung
et al. 2021, p. 2) ; (b) un cœur dans un second langage place une frontière
FFI *à l'intérieur* du produit, là où le dossier interagences avertit que
« The memory safety guarantees offered by MSLs are going to be qualified
when data flows across these boundaries » (p. 13) — la frontière tomberait
précisément sur l'arête cœur ↔ vérificateur que S-G2 doit tenir nette ; (c)
le vérificateur est l'artefact que des tiers doivent reconstruire (DEVOPS
§1) : deux chaînes de compilation à reconstruire au lieu d'une double le
coût de la promesse offline, sans qu'aucune pièce détenue ne montre un gain
compensatoire sur nos critères.

**Rust — retenu, avec ses réserves écrites.** Deux réserves, toutes deux sur
pièce, et toutes deux converties en décisions ci-dessus : (a) « it is
possible to defeat the memory protection guarantees in some MSLs » — le
mot-clé `unsafe` est nommé (CISA p. 13) ; d'où le point 2 de la décision ;
(b) des défauts de solidité ont été trouvés — « several soundness bugs have
been found in Rust, both in the type system itself » et dans des
bibliothèques utilisant `unsafe`, certains subtils au point qu'« they involve an
interaction of multiple libraries, each of which is (or seems to be)
perfectly safe on its own » (RustBelt, p. 66:3) ; d'où la règle de
dépendances minimales du vérificateur, qui n'est pas une élégance mais une
réduction de cette surface.

### La source qui tranche

Elle tranche en **deux temps**, et il faut les distinguer sous peine de
faire dire à un document ce qu'il ne dit pas.

**Premier temps — ce qui est écarté.** Le dossier interagences CISA / NSA /
FBI / ASD ACSC / CCCS / NCSC-UK / NCSC-NZ / CERT-NZ, *The Case for Memory
Safe Roadmaps* (décembre 2023, TLP:CLEAR, détenu) écarte C/C++ (p. 5) et
pose que « the most promising mitigation is for software manufacturers to
use a memory safe programming language because it is a coding language not
susceptible to memory safety vulnerabilities » (p. 9). **Il ne choisit pas
Rust** : son annexe co-liste six langages (C#, Go, Java, Python, Rust,
Swift — p. 19), son corps pose que « There are numerous MSLs, and each one
has its own set of tradeoffs in terms of architecture, tooling, performance,
popularity, cost, and other factors. No one MSL is right for all programming
needs » (p. 10), et son avertissement final précise que les agences « do not
endorse any commercial product or service, including any subjects of
analysis » (p. 20). Ce document rétrécit le champ ; il ne le ferme pas, et
toute ADR qui lui ferait dire « Rust » le surciterait.

**Second temps — ce qui ferme le champ pour *nous*.** RustBelt (Jung,
Jourdan, Krebbers, Dreyer, PACMPL 2(POPL), art. 66, 2018, DOI 10.1145/3158154
imprimé en page de titre, détenu) : « we give the first formal (and
machine-checked) safety proof for a language representing a realistic subset
of Rust », et l'extensibilité qui nous intéresse directement — « Our proof
is extensible in the sense that, for each new Rust library that uses unsafe
features, we can say what verification condition it must satisfy in order
for it to be deemed a safe extension to the language » (p. 66:1). Aucun
autre candidat du champ retenu ne porte, **dans le corpus détenu**, une
preuve machine-checked de son fragment sûr. Le même papier fixe l'honnêteté
du registre — « Unfortunately, none of Rust's safety claims have been
formally proven, and there is good reason to question whether they actually
hold » (p. 66:1, repris p. 66:2) : la preuve est récente, partielle et porte
sur un langage formalisé, pas sur `rustc`.

**Renfort, non décisif** : Jung et al., *Safe Systems Programming in Rust*
(version auteur datée 2021/2/22 — l'identité CACM 64(4) et sa pagination
restent candidates, non citables depuis cette copie), encadré *Key
Insights*, p. 1 : « Rust is the first industry-supported programming language
to overcome the longstanding tradeoff between the safety guarantees of
higher-level languages (like Java) and the control over resource management
provided by lower-level "systems programming" languages (like C and C++) ».
Et sur le déterminisme du coût mémoire, p. 3 : la gestion mémoire statique
« yields enormous benefits: it helps not only to keep the maximal memory
consumption down, but also to provide good worst-case latency in a reactive
system » — ce qui sert la reconstructibilité du vérificateur, sans qu'aucune
source détenue n'affirme pour autant que Rust rende un *build* déterministe
(cette question appartient à ADR-0012).

**Le chiffre, cité comme chiffre tiers, jamais nu** : 70 % — *rapporté par
Jung et al. (2021, p. 1) citant Microsoft [33]* : « Microsoft recently
reported that 70% of the security vulnerabilities they fix are due to memory
safety violations ». Corroboré par un second rapporteur, lui aussi de
seconde main : le dossier interagences écrit « About 70 percent of Microsoft
common vulnerabilities and exposures (CVEs) are memory safety
vulnerabilities » (p. 4, appuyé sur sa note 8). Deux rapporteurs, une même
mesure d'origine Microsoft ; ni l'un ni l'autre n'est la mesure.

**Assurance de cette ADR** : décision *déléguée* (patron ADR-0008), fondée
sur les pièces citées — ni *proven*, ni *tested*, et pas encore *reviewed* :
la révision du mainteneur reste ouverte. Le seul énoncé *proven* du dossier
est celui de RustBelt, et il porte sur le langage formalisé du papier.

### Ce que la décision coûte

- **L'interdit `unsafe` coûte l'écriture de certaines structures.** La pièce
  le dit : « There are a number of data types whose implementations
  fundamentally depend on shared mutable state » et, pour les supporter,
  « Rust embraces the judicious use of unsafe code encapsulated within safe
  APIs » (Jung et al. 2021, encadré *Key Insights*, p. 1). En posant
  `forbid(unsafe_code)` sur le cœur et le vérificateur, nous ne supprimons
  pas ce besoin : nous le **déplaçons dans nos dépendances**, où il devient
  un objet d'audit (ADR-0012) au lieu d'un objet de revue interne. Le coût
  est réel et il est transféré, pas annulé.
- **La règle de dépendances minimales devient chère en écriture.** RustBelt
  p. 66:3 nomme des défauts nés d'« an interaction of multiple libraries,
  each of which is (or seems to be) perfectly safe on its own » : réduire
  l'arbre du vérificateur, c'est écrire plus soi-même, donc tester plus
  soi-même. Le corpus détenu ne fournit **aucun chiffre** de ce coût ; cette
  ADR n'en invente pas.
- **La frontière C/C++ ne disparaît pas.** « MSLs, whether they use a
  garbage collection model or not, will almost certainly need to rely on
  libraries written in languages such as C and C++ » (CISA p. 13). Pour nous
  le point de contact probable est la cryptographie de COSE (ADR-0002) : si
  la crate retenue s'adosse à du C, la promesse de reconstruction du
  vérificateur (DEVOPS §1) hérite d'un compilateur C dans sa chaîne. À
  mesurer au choix de crate, en S2.5-C, avec le pouvoir d'écarter la crate.
- **L'épinglage exact coûte un rythme de mise à jour.** Toute dépendance
  exigeant un `rustc` plus récent que la MSRV épinglée force une décision
  tracée (note d'ADR ou amendement), et la CI doit installer la version
  épinglée sur **Windows et Linux** (DEVOPS §3) — deux plateformes à
  maintenir, ce que la doctrine assume déjà.
- **Le coût d'apprentissage est réel et non chiffré ici.** Le dossier
  interagences y consacre une section entière (« Staff Capabilities and
  Resourcing », p. 12) sans avancer de chiffre exploitable ; aucun n'est
  donc avancé.
- **Ce que la décision n'achète pas** : ni le déterminisme du CBOR (c'est un
  travail de code et de tests sous ADR-0002), ni le déterminisme du build
  (ADR-0012), ni la correction des statistiques (S3). Le langage retire une
  classe de défauts ; il ne dit rien des nôtres.

### Registres touchés

- **`docs/DEVOPS.md` §2 et §4** : le présupposé devient décision ;
  `rust-toolchain.toml` et l'épinglage gagnent leur fondation. Le §3 gagne
  une gate proposée — `forbid(unsafe_code)` / zéro `unsafe` dans
  `shogen-core` et `shogen-verifier` — famille S-G3. Réécriture due en
  phase D (12 §6.1), par l'orchestrateur.
- **`docs/12-fondations-ingenierie-design.md` §9, item 1** : les trois
  seuils (MSRV, edition, cible `no_std`) et le plancher zéro-`unsafe`
  remontent en ratification.
- **`docs/DECISIONS.md`** : rien n'est rouvert. ADR-0002 (`no_std` à terme,
  S3) et ADR-0003 (recalculable offline) **bornent** cette ADR ; ADR-0001
  n'est pas touchée (les adapters restent des adapters, ils sont seulement
  écrits dans le même langage).
- **`docs/08-assumptions.md`** : entrée **candidate** à ouvrir par
  l'orchestrateur — *A(toolchain-soundness)* : la solidité de `rustc` et de
  la bibliothèque standard (qui utilise `unsafe`) est supposée, non établie
  ; RustBelt couvre un langage formalisé, pas le compilateur. Voies de
  décharge connues à ce jour : aucune complète ; réduction possible par
  dépendances minimales et par la reproductibilité du binaire vérificateur
  (ADR-0012).
- **`docs/09-vocabulaire.md`** : formulation interdite **candidate** — « le
  vérificateur est sûr parce qu'il est en Rust » / « Rust garantit la sûreté
  mémoire de notre code ». On écrit à la place : « cœur et vérificateur sont
  posés `forbid(unsafe_code)` ; ce qui est machine-checked (Jung et al.
  2018) est un langage formalisé, pas `rustc` ni notre code ».
- **ADR-0012** hérite explicitement du critère « chaîne d'approvisionnement
  outillée » : lockfile committé, `cargo-deny`, reproductibilité du binaire.
  Cette ADR ne tranche que le langage et l'épinglage de la toolchain.

---

## ADR-0010 — Architecture : cœur pur, coquille impérative

**Statut** : acceptée · 2026-08-12 · ratifiée le 2026-08-12 par délégation explicite du mainteneur (« je délègue cette décision à mon agent orchestrateur… les réponses doivent se baser sur une étude académique rigoureuse ») — seuils chiffrés ratifiés comme **budgets déclarés révisables par ADR**, au statut exact que leurs sources autorisent

**Adjudication orchestrateur (2026-08-12)** : draft rendu par un worker de
la passe S2.5 (run `wf_e704a674-9da`) ; les 27 citations du draft ont été
re-établies par l'orchestrateur avant écriture — Parnas relu aux
pp. 1053-1058 (pages fichier 1, 4-6), Meyer relu aux pp. 40-46 (pages
fichier 1-3, 5-7, dont la commande *short* p. 46, hors liste du worker,
contrôlée aussi), Saltzer & Schroeder §I.A.3 re-greppé à la copie (lignes
65-92), documents internes contrôlés en lecture directe.

### Contexte

`DEVOPS.md` §2 dessine un workspace (`crates/shogen-core`, `crates/shogen-verifier`, `adapters/`, `xtask/`) et affirme que « La structure EST la doctrine, et les gates la tiennent » — mais le document se déclare lui-même « plan, rien n'est encore en place » (en-tête). Trois bornes déjà acceptées le contraignent sans le décider : **ADR-0001** (les transports sont des adapters ; le vocabulaire de faits ne nomme aucun transport), **ADR-0002** (CBOR déterministe + COSE, écosystème `no_std` visé pour la vérification), **ADR-0003** (le certificat est recalculé hors ligne, la signature de Shōgen n'étant qu'une commodité de cache). Aucune ne dit **quel module cache quelle décision**, **dans quel sens une arête de dépendance a le droit d'aller**, ni **ce qu'une fonction du cœur a le droit de faire quand son entrée est hostile**.

Or l'entrée du vérificateur est, par construction d'ADR-0003, un lot **fourni par un tiers** : témoignages embarqués, données d'historique, octets d'un adversaire possible. La question n'est donc pas de style. Un cœur qui lit une horloge rend la recalculabilité d'ADR-0003 non reproductible ; un vérificateur qui panique sur un lot forgé est un déni qui ne dit pas son nom (DEVOPS §3, S-G3) ; une arête `verifier → adapter` transforme « vérifiable hors ligne sans confiance dans Shōgen » en promesse à croire.

Cette ADR décide la doctrine de dépendances, **ratifie DEVOPS §2** et **fonde S-G1/S-G2/S-G3**.

### Décision

**1. Le cœur (`shogen-core`) est pur, total, sans I/O, sans panique.** Les quatre mots ont un contenu opérationnel, chacun gatable :

- *sans I/O* — aucun accès fichier, réseau, horloge, aléa, variable d'environnement, ni écriture de journal. Toute entrée est un argument, toute sortie une valeur de retour. Un horodatage est une **donnée** qui entre en argument, jamais une lecture d'horloge.
- *pur* — mêmes arguments, mêmes octets de sortie, d'une exécution et d'une machine à l'autre. C'est la condition d'existence de la recalculabilité d'ADR-0003 : un tiers qui rejoue le calcul doit obtenir le même verdict, sinon « recalculable » ne veut rien dire.
- *total* — tout point d'entrée public est défini sur tout son type d'entrée. Une entrée mal formée est une **valeur** du type de retour (erreur nommée), jamais une divergence. Ce qui n'est pas rendu total par le typage porte une précondition **écrite** et établie à la frontière (point 6).
- *sans panique* — ni `unwrap`/`expect`/`panic!`, ni arithmétique non contrôlée, ni allocation dimensionnée par une longueur venue du lot. S-G3 mécanise les formes syntaxiques ; ce qu'elle n'atteint pas est écrit au §« Ce que la décision coûte », point 6.

**2. Le critère de découpe est l'information hiding, pas la chronologie du traitement.** Chaque module cache une décision susceptible de changer et son interface en révèle le moins possible (Parnas p. 1056). La liste de départ — le « list of difficult design decisions » par lequel Parnas demande de commencer (p. 1058) — pour Shōgen : (a) l'encodage octet des témoignages (ADR-0002), caché derrière la forme canonique ; (b) le mécanisme de transport et son modèle de menace (ADR-0001), caché derrière cette même forme ; (c) les règles de typage des typeurs ; (d) l'algorithme de partition et de k_eff ; (e) la politique de rétention et de rédaction (ADR-0005) ; (f) la présentation du certificat. Aucun de ces modules ne correspond à une étape du pipeline.

**3. La direction de dépendance est un ordre partiel, et un fait de link-time.** `shogen-verifier → shogen-core`, et rien d'autre ; `adapters/* → shogen-core` ; jamais `core → adapter`, jamais `verifier → adapter`. C'est S-G2, avec l'interdiction de toute dépendance réseau ou horloge dans le vérificateur.

**4. La coquille impérative porte tout le reste.** I/O, réseau, horloge, aléa, environnement, journalisation, lecture d'arguments : `adapters/*`, binaire CLI, `xtask`. La coquille a le droit d'échouer ; elle échoue **fermée** et ne passe au cœur que des valeurs.

**5. Fail-closed par défaut à chaque frontière.** Le verdict par défaut est le refus ; l'admission est explicite et énumérée — *fail-safe defaults* de Saltzer & Schroeder appliqué à un vérificateur, jusqu'au cas dégénéré : un lot que le cœur ne sait pas classer est refusé, jamais admis par défaut.

**6. Contrats, pas conventions — avec une frontière explicitement tolérante.** Chaque entrée publique du cœur porte pré/postcondition (assertions de debug + propriétés testées) ; chaque forme canonique porte son invariant de type, préservé par toute opération exportée. La répartition des responsabilités est celle de Meyer : une condition de cohérence appartient à **un seul** côté, nommé ; la double vérification défensive est refusée. **Nuance décidée ici**, sans quoi « pas de programmation défensive » et « fail-closed sur entrée hostile » se contrediraient : les points d'entrée **de frontière** (ceux qui reçoivent des octets venus de la coquille) sont écrits en style *tolérant* — précondition faible, mal-formé = erreur nommée en retour — et ce contrôle n'est **pas** redondant : il est l'**établissement unique** de la précondition dont tout l'intérieur dépend ensuite. Les fonctions internes sont écrites en style *exigeant*. La **carte des points de frontière** est un livrable du walking skeleton (12 §5) ; sans elle, la règle se dégrade en préférence personnelle.

**7. Les statistiques héritent de la pureté** le jour où elles entrent au cœur (k_eff, partition — S3/S4) : pas d'aléa non passé en argument, pas de résultat dépendant d'un ordre d'ordonnancement. Le choix d'arithmétique (exacte, ou flottant à ordre de sommation imposé) n'est pas tranché ici : la logique produit est un **non-objet** de S2.5 (12 §1) et ce choix appartient à la passe qui écrit la statistique.

**8. Moindre privilège partout.** Le vérificateur ne réclame aucune capacité qu'il n'exerce (ni réseau, ni horloge) ; les jobs CI portent le droit minimal, le droit de publier n'existant que dans le job de release (DEVOPS §4). *Least privilege* de Saltzer & Schroeder, appliqué au binaire comme à la chaîne.

### Alternative considérée

**(a) Couches classiques** — découpe par étapes de traitement (lecture → typage → partition → verdict). **Rejetée comme critère de découpe** : Parnas démontre qu'une découpe par organigramme place les décisions difficiles *dans les interfaces*, où chaque changement se propage à plusieurs modules ; sa conclusion (p. 1058) est explicite sur l'incorrection de ce point de départ. **Retenue comme ordre** : la hiérarchie de dépendance reste — Parnas écrit lui-même (p. 1058) que structure hiérarchique et découpe propre sont deux propriétés désirables mais *indépendantes*. On prend les deux, chacune de sa source : l'ordre partiel « uses / depends upon » (p. 1057) devient S-G2, l'information hiding devient le critère de découpe.

**(b) Monolithe modulaire** — une seule crate, frontières par module et par revue. **Rejetée** : la frontière ne serait pas un fait de link-time. ADR-0003 promet une vérification « sans confiance dans Shōgen » ; « le vérificateur ne dépend d'aucun adapter » doit alors être contrôlable par un tiers depuis les manifestes, pas cru sur parole. Parnas nomme le mode de défaillance (p. 1057) : si des modules « bas » se servent des modules « haut », la hiérarchie disparaît — et à l'intérieur d'une crate, rien de mécanique n'empêche cette arête d'apparaître un mardi à 2 h du matin. Coût assumé : plus de crates, compilation plus longue, discipline de versions inter-crates.

**(c) Totalité et fail-closed par conventions** — guide de style et revue humaine, sans gate. **Rejetée** pour la raison exacte de Saltzer & Schroeder : un mécanisme qui *exclut* explicitement tend à échouer en *laissant passer*, et cet échec passe inaperçu à l'usage normal ; une convention est précisément un mécanisme dont la violation n'est pas détectée à l'usage normal. Renfort non discrétionnaire : corpus doc 02, R-22 (les gates sont bloquantes, ni l'urgence ni le prototype ne les suspendent) ; et la doctrine gatewright du dépôt (`shogen-devops` §2) : une gate qui n'a jamais échoué n'a rien montré.

**(d) Programmation défensive généralisée** — chaque routine revérifie tout, « au cas où ». **Rejetée** sur Meyer : le contrôle aveugle ajoute du logiciel, donc des sources de défaillance, donc des contrôles (p. 41), et la répartition claire des responsabilités rend la redondance inutile (p. 44). Le contrôle de frontière du point 6 n'est pas cette redondance : il a lieu **une fois**, à l'entrée, là où aucune précondition n'a encore été établie.

**(e) Cœur « pragmatiquement » impur** — une ligne de log ici, une lecture d'horloge pour la fraîcheur là. **Rejetée sans instruction longue** : elle contredit frontalement ADR-0003 (recalcul non reproductible) et ADR-0002 (cible `no_std` à terme, où ces appels n'existent pas). Borne non rouvrable.

**(f) Cœur à contrats *prouvés*** — spécification formelle et preuve mécanisée. **Ni retenue ni rejetée** : hors objet de S2.5 (12 §1, aucune logique produit) et hors de son budget. Ce que cette ADR décide n'en ferme rien — un cœur pur, total et sans I/O est exactement le fragment sur lequel une telle preuve serait praticable. La question se rouvre d'elle-même le jour où le noyau statistique existe.

### La source qui tranche

Trois pièces détenues, lues à la section, chacune tranchant une des trois questions.

- **Le critère de découpe** — Parnas 1972 (`biblio/parnas-1972-criteria-cacm.pdf`), p. 1053 (résumé : l'efficacité d'une modularisation dépend du critère de découpe), p. 1056 (chaque module est caractérisé par la décision qu'il cache à tous les autres, son interface en révélant le moins possible), p. 1057 (l'ordre partiel « uses / depends upon » ; ce qu'on perd si les modules bas utilisent les modules hauts), p. 1058 (commencer par la liste des décisions difficiles ; hiérarchie et découpe propre sont indépendantes). C'est la seule source du dossier qui sépare *l'ordre de dépendance* du *critère de découpe* — la distinction dont dépendent S-G2 d'un côté et la structure de DEVOPS §2 de l'autre.
- **Le défaut fermé et le moindre privilège** — Saltzer & Schroeder 1975 (`biblio/saltzer-schroeder-1975-protection-Basic-2026-08-12.html`), §I.A.3 « Design Principles », alinéas b) et f). *Fail-safe defaults* fonde S-G3 par son argument même, et non par son autorité : l'erreur d'un mécanisme à permission explicite échoue en refusant — situation sûre, détectée vite ; l'erreur d'un mécanisme à exclusion explicite échoue en autorisant, sans être remarquée à l'usage normal. Un vérificateur est le cas d'application littéral. *Least privilege* fonde le point 8.
- **La totalité comme obligation écrite** — Meyer 1992 (`biblio/meyer-1992-dbc-computer.pdf`), p. 41 (les éléments logiciels sont des implémentations d'une spécification, pas des textes exécutables arbitraires ; critique du contrôle aveugle), p. 42 (ce qu'expriment précondition et postcondition), p. 44 (le rejet de la programmation défensive et le spectre *demanding* / *tolerant*), p. 45 (l'invariant de classe, préservé par toute routine exportée ; et l'exigence faite aux fonctions utilisées dans les assertions de ne changer aucun état). Le point 6 de la décision est ce spectre appliqué à une **frontière de confiance**.

Et l'avertissement qui explique **pourquoi ces principes deviennent des gates chez nous** : Saltzer & Schroeder ferment leur §I.A.3 en écrivant que ces principes ne sont pas des règles absolues et qu'ils servent d'abord d'avertissements. Un avertissement qui reste un avertissement se perd ; mécanisé en gate bloquante, il tient. C'est la doctrine du corpus (doc 02, R-22), pas une invention locale.

**Assurance** : décision **déléguée** à l'orchestrateur (12 §2, patron ADR-0008), **fondée sur les précédents cités** — ni *proven*, ni *tested*, et pas encore *reviewed* : la révision du mainteneur reste ouverte.

### Ce que la décision coûte

1. **La totalité coûte un type de retour partout.** Chaque entrée publique du cœur rend un résultat, y compris là où « ça ne peut pas arriver » : verbosité, taxonomie d'erreurs nommées à maintenir, accès indexés contrôlés. **Aucune source détenue ne chiffre ce surcoût** — il est assumé, pas mesuré, et aucun nombre ne sera écrit ici pour faire sérieux.
2. **La découpe par décision cachée coûte de l'efficacité, et Parnas le dit lui-même** (p. 1057) : la seconde décomposition peut se révéler bien moins efficace que la première, par commutation répétée entre modules ; son remède de 1972 — assembler les routines dans le code au lieu de les appeler — est l'ancêtre de l'inlining. Notre chaîne le fait, mais pas gratuitement à travers une frontière de crate : une politique d'inlining/LTO est due, et elle appartient à ADR-0009/0012, pas ici.
3. **Le multi-crate coûte du temps de compilation** et une discipline de versions entre crates, sur un projet à un mainteneur.
4. **Les contrats coûtent une écriture double** (assertion et propriété testée). Contrepartie prise chez Meyer (p. 46, la forme *short* : la documentation d'interface est extraite du texte, assertions comprises) : le contrat n'est pas un document de plus, il **est** le document d'interface.
5. **La pureté ferme le canal de débogage facile** : pas de `println!` dans le cœur. La coquille journalise, le cœur retourne. Un incident se diagnostique par rejeu d'entrées — cohérent avec ADR-0003, mais plus lent le jour où ça brûle.
6. **S-G3 ne fait pas ce que son nom laisse croire, et il faut l'écrire.** Interdire `unwrap`/`expect`/`panic!` est un contrôle **syntaxique** : il n'atteint ni le débordement arithmétique, ni l'indexation de tranche, ni l'échec d'allocation, ni une panique venue d'une dépendance. « Zéro panique » n'est donc **pas établi** par la gate : elle rejette une liste de formes nommées, et le reste est couvert — partiellement — par l'arithmétique contrôlée, les tests de propriété et la revue. Toute phrase du dépôt disant « le cœur ne peut pas paniquer » serait une surclamation.
7. **La frontière tolérante coûte une carte explicite** des points d'entrée concernés. Meyer note déjà (p. 44) que l'arbitrage *demanding* / *tolerant* relève en partie de la préférence ; ce qui l'en sort chez nous est la carte, livrable du walking skeleton (12 §5) — sans elle, le point 6 n'est pas une décision, c'est un goût.

### Registres touchés

- **`DEVOPS.md` §2 : ratifié.** La structure du workspace est la doctrine de cette ADR, non plus un plan ; réécriture due en phase D (12 §6.1), de « plan » à « décidé ».
- **Gates fondées** (elles *exécutent* cette ADR ; aucune n'est nouvelle) : **S-G1** — ADR-0001 plus l'information hiding : le cœur ne nomme aucun transport ; **S-G2** — l'ordre partiel de Parnas rendu mécanique (arête interdite), plus l'absence de dépendance réseau/horloge dans le vérificateur ; **S-G3** — *fail-safe defaults* appliqué au code du cœur et du vérificateur. Chacune sous le régime du dépôt : sélection par rôle à chemins exacts, ligne de couverture avant verdict, **mutant semé tué avant tout vert** (`shogen-devops` §2).
- **Gate candidate, à instruire avec ADR-0009** (ce n'est pas un seuil) : rendre « sans I/O » mécanique et non seulement syntaxique — cible `no_std` du cœur, ou jeu de features contrôlé qui prive le cœur des API d'I/O. Tant qu'elle n'existe pas, « sans I/O » repose sur S-G3 étendue et sur la revue, et doit être dit ainsi.
- **`09-vocabulaire.md` — deux candidates** : « le cœur est sûr » / « le cœur ne peut pas paniquer », et « la totalité garantit l'absence d'erreur ». Formulation correcte : « S-G3 rejette les formes nommées ; l'absence de panique n'est pas établie » (§Coûts, point 6).
- **`08-assumptions.md` — candidate** : le résidu du point 6 mérite un identifiant d'assumption le jour où un document public s'appuie sur la robustesse du vérificateur. Ouverture réservée à l'orchestrateur.
- **Aucun seuil chiffré.** Les invariants de cette ADR **deviennent des gates**, pas des nombres : direction de dépendance (S-G2), zéro panique syntaxique (S-G3), aucun nom de transport au cœur (S-G1), et — candidate — aucune I/O au cœur. Rien ne remonte au titre de 12 §9.1 (les seuils) ; ce qui remonte est la **révision de l'ADR** elle-même, 12 §9.2.

---

## ADR-0011 — Stratégie de test : pyramide par rôle, property-based sur le cœur pur, mutation en validateur de la suite, couverture en garde-fou

**Statut** : acceptée · 2026-08-12 · ratifiée le 2026-08-12 par délégation explicite du mainteneur (« je délègue cette décision à mon agent orchestrateur… les réponses doivent se baser sur une étude académique rigoureuse ») — seuils chiffrés ratifiés comme **budgets déclarés révisables par ADR**, au statut exact que leurs sources autorisent

**Adjudication orchestrateur (2026-08-12)** : draft rendu par un worker de
la passe S2.5 (run `wf_e704a674-9da`) ; les 39 citations du draft ont été
re-établies par l'orchestrateur avant écriture — DeMillo relu aux
pp. 34-36 et 39, Jia & Harman aux pp. 3-4 de la copie, Inozemtseva &
Holmes aux pp. 1 et 8-10 de la copie, QuickCheck aux pp. 1-3 de la copie,
Vocke et Dodds re-greppés aux copies datées (toutes les lignes citées
retrouvées). Les sept seuils candidats du worker sont inlinés ci-dessous
(§Décision, point 6) pour que l'ADR les porte elle-même.

### Contexte

`DEVOPS.md` se déclare lui-même « plan, rien n'est encore en place ». Il porte pourtant déjà une doctrine de test complète et non fondée : les gates S-G1…S-G7 (§3), la ligne de couverture avant verdict, et surtout la règle qui commande tout le reste — « **Aucun vert n'est rapporté sans mutant semé** : introduis la violation que la gate existe à attraper, regarde-la mourir, restaure, committe le mutant comme test permanent » (charte `shogen-devops` §2). Cette règle est héritée de Kraidle par cicatrice, jamais adossée à une source. La passe S2.5 (12 §3) existe pour convertir ces présupposés en choix instruits ; cette ADR est la conversion pour le test.

Trois bornes non rouvrables la contraignent. **ADR-0002** : encodage CBOR déterministe + COSE, vérificateur `no_std` à terme — donc rien de ce que la stratégie de test impose ne peut entrer dans le graphe de dépendances du vérificateur. **ADR-0003** : le certificat est recalculable offline, jamais seulement émis — le vérificateur est l'artefact de confiance du projet (DEVOPS §1), il mérite le régime le plus strict, pas le régime moyen. **ADR-0010** (même passe) : un cœur pur, total, sans I/O, sans panique — un terrain où toute une famille d'instruments devient disponible, indisponible aux adapters qui font de l'I/O.

Quatre questions, donc : quelle **forme** prend la suite ; quel instrument **valide** la suite elle-même ; quel rôle exact joue la **couverture** ; et quels **planchers** lient. Les trois premières se tranchent sur artefacts détenus ; la quatrième produit des seuils candidats, qui remontent (12 §2 et §9) et ne sont jamais adjugés seuls.

Périmètre : S2.5 interdit toute logique produit (12 §1). Cette ADR fixe le **régime** ; les propriétés qui portent sur k_eff lient au moment où le calcul atterrit (S3/S4), pas avant. Elle ne crée aucune gate — l'instrumentation (nom, chemins, place dans le pipeline) appartient à ADR-0013.

### Décision

**1. La forme : une pyramide par rôle de crate, sélectionnée à chemins exacts.**

- *Socle* : tests unitaires **et** property-based sur `shogen-core` — le plus gros de la suite, là où le code est pur (ADR-0010).
- *Étage* : intégration cœur ↔ `shogen-verifier` (un lot CBOR déterministe traverse et se recalcule — ADR-0002/0003), et un test de contrat par adapter (ADR-0001).
- *Sommet* : de bout en bout, très peu — au démarrage, **exactement un** : le walking skeleton lui-même (12 §5).

Deux règles de flux, reprises de la copie datée de Vocke : « Push your tests as far down the test pyramid as you can » ; et un défaut trouvé par un test haut sans qu'aucun test bas échoue **crée** le test bas (« If a higher-level test spots an error and there's no lower-level test failing, you need to write a lower-level test »). La place d'un test dans le pipeline se décide par sa **vitesse et sa portée**, pas par son étiquette de type — « defining the stages of your deployment pipeline is not driven by the types of tests but rather by their speed and scope ».

La sélection est **par rôle à chemins exacts**, jamais par le nom qu'un fichier se choisit lui-même (doctrine gatewright, charte §2). C'est le point où l'objection de Dodds — les définitions de « unit » et « integration » ne sont pas de la connaissance scientifique — porte réellement, et la sélection par chemin la neutralise : `crates/shogen-core/**` est un fait de dépôt, « test unitaire » est une opinion.

**2. Le property-based est obligatoire sur le cœur pur, facultatif ailleurs.** Propriétés dues, nommées :

- (a) **round-trip de la forme canonique** : `decode(encode(x)) == x` pour tout fait `x`, et `encode(decode(b)) == b` pour tout `b` accepté (ADR-0002) ;
- (b) **unicité de représentation** : deux chemins d'encodage d'un même fait produisent les mêmes octets — les Core Deterministic Encoding Requirements d'ADR-0002 énoncées comme propriété, pas comme intention ;
- (c) **totalité du vérificateur** : aucune suite d'octets ne fait paniquer `shogen-verifier` — le pendant *tested* de la gate S-G3, qui est lexicale (elle interdit `unwrap` dans le source ; elle ne dit rien de ce que fait le binaire sur une entrée hostile) ;
- (d) **à l'apparition du calcul de partition** (S3/S4, hors S2.5) : k_eff ≤ k nominal ; une arête `basis:doc` seule laisse k_eff inchangé (ADR-0008 — la règle est déjà testée dans le harnais S2 jetable, elle doit renaître comme propriété dans le produit) ; fusionner deux classes ne fait jamais monter k_eff.

Trois obligations d'exécution, qui font la différence entre un vert lu et un vert cru :

- la **graine est consignée** et le rejeu est exact — un échec aléatoire non rejouable n'est pas un fait ;
- la **distribution des cas est imprimée avant le verdict** — l'analogue exact de la ligne de couverture des gates. QuickCheck fournit `classify`/`collect` pour cela et ses auteurs s'en servent à charge contre leur propre exemple ;
- **tout contre-exemple devient un test example-based permanent et nommé** — « l'évasion devient un test » (DEVOPS §3), ici en régime automatique.

**3. Le validateur de la suite est le score de mutation ; la couverture ne l'est pas.** Le mutant semé de la doctrine gatewright **reçoit ici sa fondation** : il est la forme manuelle et unitaire de l'analyse de mutation de DeMillo, Lipton & Sayward (1978), dont Jia & Harman (2011) donnent la forme mesurée — « The mutation score (MS) is the ratio of the number of killed mutants over the total number of non-equivalent mutants ». Ce que la fondation apporte n'est pas une permission, c'est une **limite** : le coupling effect est déclaré empirique par ses auteurs eux-mêmes (« no hope of "proving" »), donc un score de mutation est un énoncé *tested* sur une population de fautes semées, jamais un énoncé sur les fautes réelles. Le registre d'assurance du projet s'applique sans remise : *tested (avec compte)*, pas *proven*.

**4. Trois registres de « semé », qui ne se confondent jamais.** La confusion serait une surclamation du même genre que celles du 09-vocabulaire :

- *mutant de gate* — la violation qu'une gate existe pour attraper, semée à la main dans un fichier, tuée, committée en test permanent (DEVOPS §3). Ce n'est **pas** de l'analyse de mutation : la population n'est ni systématique ni comptée. C'est un test négatif de l'outil, et il reste obligatoire tel quel.
- *mutant de programme* — un opérateur de mutation appliqué à `shogen-core`. C'est le seul des trois qui produit un **score**, au sens défini ci-dessus.
- *octet muté du lot* — la mutation de l'**entrée** du vérificateur (12 §5 : « échoue fail-closed sur un octet muté »). C'est un test négatif de données. L'appeler « mutation testing » ou en tirer un score serait un faux.

**5. La couverture est un garde-fou par rôle, jamais une cible.** Planchers candidats (bloc des seuils), fail-closed, imprimés à chaque exécution, plus stricts sur `shogen-core` et `shogen-verifier` que sur les adapters — parce que le cœur est pur et total (toute ligne y est atteignable par construction : un trou y est un oubli, pas une contrainte d'environnement) et parce que le vérificateur est l'artefact qu'un tiers exécute hors ligne. L'usage retenu est **exactement** celui que l'artefact accorde : identifier le sous-testé. Il devient interdit d'écrire qu'un pourcentage de couverture dit quoi que ce soit de l'efficacité de la suite (entrée candidate au 09-vocabulaire).

**6. Ce qui remonte.** Les sept seuils ci-dessous sont **candidats —
ratification mainteneur due** (12 §2, §9). Ils s'appliquent à titre
provisoire dès le squelette, fail-closed, et **aucun ne se desserre sans
ADR** (charte §2 : serrer oui, desserrer jamais de sa propre initiative).
Aucun des nombres n'est adossé à un artefact détenu (§Coûts, point 7) —
le régime l'est, les valeurs sont des choix de budget nommés :

1. *Couverture cœur et vérificateur* : **≥ 90 % de lignes**, mesurée
   séparément sur `shogen-core` et `shogen-verifier`, imprimée avant
   verdict. Alternatives instruites : 100 % (rejetée — transforme le
   garde-fou en cible, l'anti-patron documenté) ; 80 % d'usage (rien ne
   fonde 80 plutôt que 90, et un cœur pur n'a pas d'excuse
   d'environnement) ; branches vs lignes (à instruire — l'artefact mesure
   que le type de couverture change peu la corrélation, p. 8, Table 5).
2. *Couverture adapters* : **≥ 60 % de lignes ET un test de contrat par
   adapter** (forme canonique produite/consommée). Alternative : aucun
   plancher chiffré, contrat seul (défendable — l'environnement, pas le
   code, domine le risque d'un adapter, ADR-0001).
3. *Score de mutation du cœur* : régime en deux temps — (1) S2.5 :
   plancher binaire, le mutant semé de la gate meurt, sans score ;
   (2) dès la logique (S3) : **≥ 80 % de mutants tués**, calculé sur
   mutants non équivalents (la définition de Jia & Harman p. 4), chaque
   survivant justifié nommément en une ligne, plus non-régression.
   Alternatives : 100 % (rejetée — indécidabilité de l'équivalence,
   p. 4) ; non-régression seule (défendable si le mainteneur juge 80
   arbitraire).
4. *Budget de mutation en CI* : **≤ 10 min sur `shogen-core` par PR** ;
   au-delà, run complet en nightly avec non-régression bloquante.
   Alternatives : nightly seul (un vert de PR ne dit plus rien) ;
   mutation du diff seul (mesure la PR, plus la suite).
5. *Cas property-based par propriété* : **≥ 1 000 en CI**, graine
   consignée, rejeu exact ; **≥ 100 000 en nightly**. Alternatives :
   budget de temps plutôt que compte fixe (probablement supérieur) ; 256,
   défaut courant (pas plus fondé que le « 100 » que les auteurs
   déclarent arbitraire).
6. *Part minimale de cas non triviaux* : **≥ 50 %** dans la classe
   déclarée « utile », distribution imprimée à chaque exécution ; sous le
   seuil, la propriété est refusée (générateur à corriger, jamais seuil à
   baisser). Seul ancrage chiffré de l'artefact, fourni à charge : « OK,
   passed 100 tests (43% trivial) », jugé « worrying » par ses auteurs.
   Alternative : ≥ 20 % (accepte une distribution que les auteurs de la
   méthode désapprouvent) ; aucune gate, lecture en revue (rejetée — une
   ligne imprimée que personne ne lit est le mode d'échec documenté).
7. *Totalité du vérificateur (fuzz)* : **zéro panique sur toute suite
   d'octets** — seuil binaire, non négociable (S-G3, 12 §5) ; budgets
   candidats : ≥ 15 min par CI, ≥ 4 h en nightly, corpus de graines
   committé et croissant de chaque contre-exemple. Alternative : S-G3
   lexicale seule (rejetée — elle ne dit rien du binaire sur une entrée
   hostile) ; fuzz nightly seul (acceptable au démarrage si la release
   est gatée dessus).

### Alternative considérée

**(a) Le « testing trophy » (Dodds, copie datée — page datée du 3 juin 2021).** L'alternative industrielle, instruite au texte et rejetée sur les pièces de l'article lui-même. (i) Son auteur en borne le domaine : « I never considered whether it applied to microservices or even backend services at all. I considered my codebase in isolation », et en conclusion « It definitely has applicability in backends, but I've only considered it for monoliths not microservices or even serverless functions ». Shōgen n'est ni un monolithe ni une base de code unique : c'est un cœur, un vérificateur séparé, et des adapters dont l'isolement mutuel est la décision (ADR-0001, gates S-G1/S-G2). (ii) La couche « static » qui distingue le trophy de la pyramide est ajoutée pour une raison que l'auteur nomme : « I added "static" to the trophy because in the world of JavaScript that's not a given like it is in the predominant languages when the testing pyramid was introduced ». Chez nous cette couche est déjà tenue par le typage et les gates (ADR-0009/0010) — l'ajout est vide. (iii) Son critère est un retour sur investissement en confiance : « "return" is "confidence" and "investment" is "time" ». Un projet qui vend de la provenance recalculable ne peut pas prendre la confiance subjective pour métrique de sa propre suite. **Ce qu'on lui garde** : sa mise en garde sur la classification, qu'il emprunte à Tim Bray — « let's not kid ourselves that our software-testing tenets constitute scientific knowledge » (Bray, cité par Dodds) — d'où la sélection par chemin plutôt que par nom de couche, point 1.

**(b) Example-based seul.** Rejeté : le round-trip canonique et l'unicité de représentation sont des énoncés universellement quantifiés sur des octets ; aucune table d'exemples ne les épuise, et c'est précisément la configuration que Claessen & Hughes visent (fonctions pures, propriétés à grain fin).

**(c) Property-based seul.** Rejeté : le générateur peut mentir par omission. Les auteurs de QuickCheck le démontrent sur leur propre exemple — la distribution s'effondre sur les cas triviaux et ils le disent (« it is worrying that very short lists dominate the test cases so strongly »). D'où l'obligation d'imprimer la distribution et de figer chaque contre-exemple en test nommé.

**(d) Couverture-cible (un pourcentage à atteindre, ou une exigence MC/DC façon DO-178B).** Rejeté sur pièce, et sur la pièce la plus proche du cas : Inozemtseva & Holmes examinent nommément l'exigence MC/DC du standard FAA et concluent qu'elle « may increase expenses without necessarily increasing quality ». Adopter une cible de couverture serait acheter un chiffre présentable au prix d'un instrument que l'artefact détenu qualifie de mauvais indicateur.

**(e) Analyse de mutation sur tout le workspace.** Rejeté sur le coût, nommé par le survey : « the high computational cost of executing the enormous number of mutants against a test set » est le premier problème listé. Et les adapters font de l'I/O : muter un adapter mesure surtout la stabilité de son environnement. La mutation se pose donc là où elle est bornée et déterministe — le cœur pur.

**(f) Aucun plancher, revue humaine seule.** Rejeté : le corpus doc 02 rend les gates bloquantes et non discrétionnaires (R-22), et DEVOPS §5 nomme le cas réel — « la protection vaut surtout contre l'agent et contre soi-même à 2 h du matin ». Une revue humaine solo n'est pas un instrument, c'est une intention.

### La source qui tranche

Deux sources sur deux questions distinctes, une fondation avec sa limite, et **une non-source dite comme telle**.

**Sur la hiérarchie des instruments — la couverture descend, la mutation monte.** Inozemtseva & Holmes 2014 (détenue, lue p. 1, p. 8, p. 9, p. 10 de la copie). L'abstract : « coverage, while useful for identifying under-tested parts of a program, should not be used as a quality target because it is not a good indicator of test suite effectiveness ». La discussion p. 8 donne la formulation opérationnelle exacte de notre point 5 : « While coverage measures are useful for identifying under-tested parts of a program, and low coverage may indicate that a test suite is inadequate, high coverage does not indicate that a test suite is effective. » Et la conclusion p. 10 ferme la porte à la cible : « using a fixed coverage value as a quality target is unlikely to produce an effective test suite ». Le même article porte la contrepartie positive, p. 9 : « we currently feel that mutation score may be a good substitute for coverage in this context » — c'est cette phrase, dans l'artefact qui disqualifie la couverture, qui promeut la mutation au rang de validateur chez nous. Assiette de l'étude, à sa lettre : « we generated 31,000 test suites for five systems consisting of up to 724,000 lines of source code » — cinq systèmes Java open source ; nous en héritons le résultat comme *une mesure sur ce périmètre*, pas comme une loi.

**Sur le property-based.** Claessen & Hughes 2000 (détenue, lue pp. 1-3 de la copie). L'abstract décrit exactement la configuration d'ADR-0010 : « Random testing is especially suitable for functional programs because properties can be stated at a fine grain. » Et §1 : « It is generally accepted that pure functions are much easier to test than side-effecting ones, because one need not be concerned with a state before and after execution. » La propriété d'exemple de l'article est un round-trip — `reverse (reverse xs) = xs` (§2.1) — soit la forme même de notre propriété (a).

**Sur le mutant semé : sa fondation et sa limite, dans la même source.** DeMillo, Lipton & Sayward 1978 (détenue, tiré *Computer* authentique, pp. 34-41 lues). Le principe : « *The coupling effect*: Test data that distinguishes all programs differing from a correct one by only simple errors is so sensitive that it also implicitly distinguishes more complex errors. » (p. 35). Et immédiatement après, la limite, que le projet doit reprendre à son compte : « There is, of course, no hope of "proving" the coupling effect; it is an empirical principle. » (p. 35).

**Point de rigueur, à ne pas manquer** (trouvaille de passe consignée à l'INDEX, entrée `demillo`) : la locution « competent programmer hypothesis » **n'apparaît pas** dans l'article de 1978. La p. 34 écrit : « competent programmers, in their many iterations through the design process, are constantly whittling away the distance between what their programs look like now and what they are intended to look like ». La **nomination** est postérieure et appartient à Jia & Harman 2011, §II.A (p. 3 de la copie) : « The CPH was first introduced by DeMillo et al. in 1978 » et « It states that programmers are competent, which implies that they tend to develop programs close to the correct version ». Les deux se citent séparément : la phrase de 1978 pour le fait, la nomination de 2011 pour le nom. L'une pour l'autre serait un faux d'attribution.

**La non-source : la forme pyramidale elle-même.** Le primaire — Cohn, *Succeeding with Agile* — **n'est pas détenu** ; la demande de procurement est formée et déposée (12 §4.2 ; WISHLIST §Priorité 3, sweep du 2026-08-12). L'attribution passe par la copie datée de Vocke (martinfowler.com, page datée du 26 février 2018) : « Mike Cohn came up with this concept in his book *Succeeding with Agile* », trois couches « Unit Tests / Service Tests / User Interface Tests », et deux acquis à retenir : « Write tests with different granularity » et « The more high-level you get the fewer tests you should have ». Le secondaire relativise lui-même le modèle : « Unfortunately the concept of the test pyramid falls a little short if you take a closer look. » **La pyramide entre donc ici en heuristique attribuée à un secondaire, pas en source-qui-tranche.** Ce qui la retient n'est pas son autorité : c'est qu'elle coïncide avec une structure déjà décidée ailleurs — le socle large tombe là où le code est pur et sans I/O (ADR-0010, DEVOPS §2). C'est un fait d'architecture, pas un fait de littérature, et c'est ainsi qu'il faut le lire.

### Ce que la décision coûte

1. **Le score de mutation ne monte jamais mécaniquement à 1.** Jia & Harman, §II.B (p. 4) : « Automatically detecting all equivalent mutants is impossible » — l'équivalence de programmes est indécidable — et le but déclaré de l'analyse (« The goal of mutation analysis is to raise the mutation score to 1 ») est donc un but, pas un état atteignable par outil. L'ordre de grandeur du reste à trier, deux mesures, chacune avec son périmètre : DeMillo *et al.* estiment sans mesure jointe « well under 1 percent equivalent mutants » sur des programmes de production (p. 39), après avoir observé « approximately 2 percent » sur leur cas d'étude FIND ; Inozemtseva & Holmes, dans leur protocole, déclarent en menace à la validité avoir classé « up to 35% of the generated mutants as equivalent » (p. 9, §6.1) — le grand écart entre 1 % et 35 % est exactement l'ampleur du travail humain que la décision achète. **Coût opérationnel** : chaque mutant survivant est trié à la main et justifié en une ligne ; un survivant non justifié est une dette nue, interdite (règle du 2026-08-05).

2. **Le temps de calcul.** Jia & Harman, §II.C (p. 4) : le coût de calcul est le premier problème listé de la technique. D'où le seuil de budget CI et le renvoi du run complet en nightly — et d'où, aussi, le refus d'étendre la mutation aux adapters.

3. **Le property-based coûte des générateurs et une surveillance.** L'article fournit lui-même le contre-exemple : « OK, passed 100 tests (43% trivial) », puis « only 19 cases tested insertion into a list with more than one element » — jugé « worrying » par ses auteurs, qui en tirent la règle « it is always important to investigate the proportion of trivial cases among those actually tested ». Et le compte par défaut est déclaré arbitraire par eux (note 1, p. 2 : « 100 is a rather arbitrary number »). Nos comptes sont donc des choix de budget assumés, jamais des héritages.

4. **L'instrumentation ne doit pas contaminer le vérificateur.** Couverture et mutation restent en dépendances de développement et en profil de test uniquement : une dépendance d'instrumentation qui entrerait dans le graphe du vérificateur contredirait ADR-0002 (`no_std` à terme) et la gate S-G2 — l'outillage de test réfutant l'architecture qu'il teste. Contrainte à porter dans ADR-0012 (politique de dépendances).

5. **Les planchers fail-closed bloqueront des PR légitimes.** C'est le prix choisi (12 §2 : mieux vaut un seuil provisoire strict qu'aucun). Le desserrage passe par une ADR, jamais par un `#[allow]` ou un `--no-verify` (charte §2). Coût réel : une ADR de plus, et un mainteneur dérangé — c'est le mécanisme, pas un effet de bord.

6. **Le refus de la cible de couverture coûte un chiffre facile à montrer** à un tiers ou dans un README. Contrepartie assumée : un projet qui vend de la provenance recalculable ne peut pas publier comme indicateur de qualité une mesure que l'artefact qu'il détient qualifie de mauvais indicateur d'efficacité — ce serait l'auto-réfutation, à l'échelle de sa propre chaîne (DEVOPS, en-tête).

7. **Aucun des nombres proposés n'est adossé à un artefact détenu — et il faut le dire ici plutôt que le laisser croire.** Ce que les sources fondent, c'est le **régime** (garde-fou vs cible ; mutation comme validateur ; property-based sur le pur) ; aucune ne fournit de plancher chiffré, et celle qui parle le plus de chiffres explique pourquoi une valeur fixe ne vaut pas comme cible. Les sept valeurs ci-dessous sont donc des **candidates — ratification mainteneur due**, chacune avec son alternative instruite. Deux références qui pourraient adosser un plancher sont **nommées depuis la bibliographie de l'artefact détenu** (Inozemtseva & Holmes, réf. [3] Andrews *et al.* TSE 2006 ; réf. [27] Just *et al.*, UW-CSE-14-02-02, mars 2014 — la source du « mutation score may be a good substitute ») : elles ne sont **pas détenues**, donc pas citées ; elles sont candidates à procurement si le mainteneur veut un plancher adossé plutôt qu'un plancher assumé.

### Registres touchés

- **`docs/DEVOPS.md` §3** : le mutant semé cesse d'être une cicatrice et devient une décision fondée (points 3 et 4) ; la ligne de mesure imprimée avant verdict gagne deux contenus — couverture par rôle, et score de mutation du cœur. Cette ADR **ne crée aucune gate** : le nom, les chemins et la place dans le pipeline appartiennent à ADR-0013, la réécriture de DEVOPS à la phase D (12 §6.1).
- **`docs/09-vocabulaire.md`** : trois entrées candidates — « couverture élevée donc suite efficace » (annoncée en 12 §6.1) ; « le score de mutation prouve que la suite détecte les fautes » (interdit : le coupling effect est déclaré empirique par ses auteurs — on écrit « suite *tested* : N mutants, M tués, K survivants justifiés ») ; « mutant semé » employé indifféremment pour les trois registres du point 4.
- **`docs/08-assumptions.md`** : le registre fait foi et n'accueille aujourd'hui que des résidus de produit. Deux résidus **de méthode** apparaissent avec cette ADR — que la mutation des fautes simples soit représentative des fautes réelles (le coupling effect), et que le programmeur soit « compétent » au sens nommé en 2011. **Proposition, à trancher par l'orchestrateur** : ouvrir une troisième section « Résidus de méthode » avec `A(coupling-effect)` (énoncé : les fautes semées simples couvrent les fautes réelles par couplage ; source du résidu : DeMillo p. 35, « no hope of "proving" … an empirical principle » ; porteur : tout score de mutation publié ; assurance : aucune ; décharge : jamais totale — les résidus réels trouvés en production entrent au corpus de mutants). **Tant que la section n'est pas ouverte, l'identifiant ne s'écrit nulle part** : on écrit la phrase en toutes lettres. C'est la leçon des « identifiants morts » (ADR-0001, amendement du 2026-07-30).
- **`docs/12-fondations-ingenierie-design.md` §9** : les sept seuils candidats y remontent, avec leurs alternatives.
- **`biblio/INDEX.md`** : rien à ouvrir — les quatre artefacts sont enregistrés (section S2.5) ; la trouvaille `demillo` est appliquée telle quelle, pas reformulée.
- **`WISHLIST.md`** : rien de neuf sur Cohn (demande déjà déposée, §Priorité 3). Deux candidates de procurement conditionnelles sont nommées au §« Ce que la décision coûte », point 7 — elles ne deviennent des demandes formées que si le mainteneur exige un plancher adossé.
- **ADR-0008** : sa règle (`basis:doc` seule ne partitionne pas) devient une propriété du property-based du cœur, à l'atterrissage du calcul de partition en S3 — la migration hors du harnais jetable est due à ce moment-là, pas avant.
- **ADR-0002 / S-G2** : contrainte nouvelle portée vers ADR-0012 — l'outillage de couverture et de mutation reste hors du graphe de dépendances du vérificateur.

---

## ADR-0012 — Politique d'environnement : le lockfile fait foi, toute dépendance entre par revue, le vérificateur vise la reconstruction bit-à-bit

**Statut** : acceptée · 2026-08-12 · ratifiée le 2026-08-12 par délégation explicite du mainteneur (« je délègue cette décision à mon agent orchestrateur… les réponses doivent se baser sur une étude académique rigoureuse ») — seuils chiffrés ratifiés comme **budgets déclarés révisables par ADR**, au statut exact que leurs sources autorisent

**Adjudication orchestrateur (2026-08-12)** : draft rendu par un worker de
la passe S2.5 (run `wf_e704a674-9da`) ; les 35 citations du draft ont été
re-établies par l'orchestrateur avant écriture — Lamb & Zacchiroli relu aux
pp. 1-3 et 5 du préprint (Définition 1, toolchain-comme-entrée, 95 %
Debian, horloge +18 mois, 30+ variations), in-toto aux pp. 1393-1395,
Sigstore aux pp. 2353-2354, SLSA v1.2 et v1.0 re-greppées aux copies
datées (y compris « after-the-fact reproducible build », « trivial to
bypass or forge », « Status: Retired »), Saltzer §I.A.3 re-greppé, le
corpus doc 02 lu en entier par l'orchestrateur (R-5/R-8/R-12/R-22 aux
lignes citées) et le chiffre slopsquatting contrôlé au doc 01 l. 121. Le
jeu de variations du double-build, référencé par D6, est inliné ci-dessous.

### Contexte

`DEVOPS.md` §4 énonce une intention — « **`cargo-deny` + lockfile committé + toolchain épinglée** (`rust-toolchain.toml`) ; audit des nouvelles dépendances dans la PR qui les introduit », attestations de build sur le vérificateur, « **Zéro secret dans le dépôt et zéro autorité ambiante en CI** » — sous un statut qui se déclare lui-même « plan, rien n'est encore en place » (en-tête de DEVOPS.md). Cette ADR convertit cette intention en décision instruite et **fonde le §4**.

L'enjeu n'est pas d'hygiène d'outillage. ADR-0003 a décidé que le certificat est **recalculable offline par un binaire séparé**, et 02-vision promet une vérification « sans confiance dans Shōgen ». Le tiers qui exerce cette promesse exécute `shogen-verifier` : un exécutable. Lamb & Zacchiroli posent l'écart dès leur abstract — « trusting code is not the same as trusting its executable counterparts » (p. 1 du préprint). Si ce binaire ne peut être re-dérivé que par nous, la confiance qu'ADR-0003 a chassée du certificat rentre par l'exécutable : c'est la même auto-réfutation, décalée d'un cran. La politique d'environnement est donc la continuation de la promesse fondatrice sur l'artefact exécutable, pas une commodité de build.

Trois bornes encadrent la décision, et ne sont pas rouvertes :

- **ADR-0002** — vérificateur `no_std` à terme : le jeu de dépendances du vérificateur est minimal *par décision antérieure*, ce qui borne le coût de toute politique d'épinglage stricte sur ce périmètre ;
- **ADR-0003** — « offline » qualifie la **vérification**, jamais le **build**. Aucune clause ci-dessous ne prétend construire hors ligne, et le vendoring n'est donc pas un moyen de tenir ADR-0003 (voir Alternatives, option 4) ;
- **DEVOPS §1** — le dépôt passe **public à S3** : tout ce qu'il contient à cette date devient redistribué, ce qui est déjà la raison pour laquelle `biblio/` n'y entre pas.

Deux règles du référentiel s'appliquent **sans être choisies ici** : **R-12** — « SBOM régénérée à chaque release ; lockfiles committés » — et **R-8** — « toute dépendance nouvelle est vérifiée (existence sur le registre officiel, ancienneté, mainteneurs, téléchargements) **avant** installation ; les installations proposées par IA ne s'exécutent jamais telles quelles ». Elles sont non discrétionnaires (R-22). L'ADR décide **comment** on les tient et ce qu'elles coûtent, jamais **si**.

Enfin, **ADR-0009 (langage/toolchain) est adjugée dans la même passe** : les clauses D1, D2, D4–D7 sont énoncées indépendamment du langage ; l'instanciation nommée (`Cargo.lock`, `rust-toolchain.toml`, `cargo-deny`) ne prend effet **que si 0009 retient Rust**, sinon les mêmes clauses se réalisent dans l'outillage du langage retenu.

### Décision

**D1 — Le lockfile committé fait foi à la construction ; le manifeste fait foi à l'évolution.** Le lockfile est versionné pour tout le workspace et **désigne** l'ensemble des dépendances, directes et transitives, avec leurs empreintes. Il n'est pas une commodité : il est la moitié « désignation » de la définition de reproductibilité retenue en D6 (« after designating a specific version of its source code **and all of its build dependencies** », Lamb & Zacchiroli, Def. 1, p. 2). Le manifeste, lui, ne dit pas ce qui *est* construit : il dit ce qui *serait admissible* comme mise à jour. **Toute construction en CI est verrouillée** : une construction qui devrait réécrire le lockfile échoue au lieu de re-résoudre silencieusement. Un désaccord manifeste/lockfile est donc un échec visible, jamais une résolution tacite.

**D2 — La toolchain est une dépendance de build, épinglée en fichier versionné** (version exacte + composants), au même titre que les bibliothèques. Raison, au texte : les entrées d'un build incluent « the entire build toolchain including the compiler, linker and build system » (Lamb & Zacchiroli, p. 3). Un compilateur flottant rend la clause D1 décorative. *(La valeur — MSRV, edition, canal — appartient à ADR-0009 et n'est pas fixée ici : couture, pas doublon.)*

**D3 — Épinglage exact au manifeste sur le périmètre cœur + vérificateur ; plages semver ailleurs.** Dans `crates/shogen-core` et `crates/shogen-verifier`, chaque dépendance directe porte une version **exacte** ; dans `adapters/*` et `xtask/`, des plages semver, le lockfile faisant foi (D1). Motif : sur le périmètre que le tiers reconstruit, tout changement de dépendance directe doit être un **acte de revue visible dans le manifeste**, pas seulement une ligne dans un fichier machine que la revue survole — c'est l'accroche mécanique de R-8 et de R-5 (« 100 % du code généré est relu et compris avant intégration »). Cette clause est un **seuil candidat — ratification mainteneur due**, et elle raffine le critère « version non exacte » de la gate S-G7 (DEVOPS §3) en le **portant par rôle, à chemins exacts** — la forme déjà retenue pour S-G1/S-G2/S-G3.

**D4 — Registre, pas vendoring, aujourd'hui.** Les dépendances viennent du registre officiel, liées par les empreintes du lockfile. Le vendoring n'est pas retenu (voir Alternatives, option 4) et sera réévalué **sur événement nommé**, pas sur impression : (a) disparition ou retrait d'une dépendance du registre, (b) exigence explicite de construction sans réseau, (c) une obligation de licence qui rendrait la copie en arbre préférable à la référence.

**D5 — R-8 mécanisé en deux moitiés qui ne se remplacent pas.** *Moitié humaine* : toute dépendance directe nouvelle entre par une PR qui **porte son contrôle de registre écrit** — existence sur le registre officiel, ancienneté, mainteneurs, téléchargements — avant installation, jamais après. *Moitié mécanique* : la gate S-G7 (`cargo-deny` si 0009 retient Rust) casse sur licence hors liste, advisory non traitée, source hors registres déclarés. Aucune des deux ne dispense de l'autre : « Point solutions designed to secure individual supply chain steps cannot guarantee the security of the entire chain as a whole » (in-toto, p. 1395). Une advisory qu'on choisit de ne pas corriger n'est **jamais** un ignore silencieux : elle devient une entrée de dette formée (R-13), avec propriétaire et échéance, ou la gate reste rouge.

**D6 — Reproductibilité : cible bit-à-bit sur le vérificateur, provenance attestée en complément — jamais en substitut.** La norme retenue est la Définition 1 de Lamb & Zacchiroli : « every build produces bit-for-bit identical artifacts, no matter the environment in which the build is performed » (p. 2). Cible **candidate — ratification mainteneur due** : bit-à-bit pour `shogen-verifier`, **Linux x86_64 d'abord**, Windows *à terme* et sans date ; contrôlée dès le walking skeleton par un **double-build à environnement varié** dont les empreintes sont comparées, gate bloquante (R-22 : pas d'advisory). Le jeu de variations est lui-même un
**candidat — ratification mainteneur due**, calqué en plus petit sur la
pratique Debian décrite p. 5 : **6 variations** entre les deux builds —
horloge système (second build décalé de +18 mois, la variation nommée par
la source), nom d'hôte, locale/langue, fuseau horaire, chemin absolu du
répertoire de build, utilisateur. Alternatives instruites : double-build
sans variation (rejeté — il ne teste que le déterminisme du compilateur,
pas l'indépendance à l'environnement, donc pas la Définition 1) ; reprise
du jeu Debian complet 30+ (non retenu au squelette pour son coût —
réévaluable à S3). En parallèle, la **provenance attestée** (piste SLSA, D7) : les deux ne sont pas des options rivales — la spec elle-même les joint, la provenance signée pouvant être produite « during the original build, **an after-the-fact reproducible build**, or some equivalent system » (SLSA v1.2, Build L2, Requirements).

**D7 — Niveau SLSA visé, et zéro autorité ambiante en CI.** Niveau **candidat — ratification mainteneur due** : **Build L2 au premier binaire `shogen-verifier` publié (S3)** ; L1 est sans objet tant que rien n'est publié (dépôt privé, DEVOPS §1) ; L3 n'est pas visé à ce stade. Le mécanisme de signature retient les clés **éphémères** liées à une identité, non des clés longue durée détenues par un humain — Sigstore : « it enables developers to use ephemeral keys to sign their artifacts, reducing the inconvenience and risk of key management » (p. 2353), et le cas d'usage est exactement le nôtre : « allows for automated workers (e.g., GitHub Actions) to sign and release a package on behalf of a developer » (p. 2353, §1). La règle d'autorité de DEVOPS §4 est fondée, elle, sur le principe de 1975 : « Every program and every user of the system should operate using the least set of privileges necessary to complete the job » (Saltzer & Schroeder, §I.A.3 f). Conséquence opérationnelle inchangée : jetons de portée minimale et éphémères, aucun secret de longue durée, le job de release seul porteur du droit de publier, sur tag protégé.

**Registre d'assurance de cette ADR** : rien ici n'est *proven* ni *tested* au 2026-08-12. Ce sont des décisions à appliquer ; le double-build de D6 deviendra *tested* (avec compte d'exécutions CI) quand le squelette sera vert, et pas avant.

### Alternative considérée

1. **Plages semver + lockfile, uniformément sur tout le workspace** (pas d'exact au manifeste). Instruite, et **retenue hors du périmètre cœur/vérificateur** (c'est la seconde moitié de D3). Rejetée *sur* ce périmètre : elle laisse le seul enregistrement du changement de dépendance directe dans un fichier écrit par la machine, alors que R-8 exige un contrôle **avant** installation et R-5 une relecture intégrale — la trace de l'acte doit être là où la revue regarde. C'est aussi la **position de repli** si l'option 2 des seuils (exact) produit des jeux de contraintes insatisfiables en pratique.
2. **Épinglage exact partout, y compris adapters et xtask.** Rejetée pour deux coûts : (a) chaque correctif de sécurité devient une édition manuelle sur un ensemble qui **croît d'un adapter par transport** (ADR-0001), pour un périmètre qu'aucun tiers ne reconstruit ; (b) une contrainte exacte sur un graphe large rend insatisfiable toute exigence transitive incompatible — propriété logique des contraintes d'égalité dans un résolveur semver, énoncée ici comme **raisonnement, non comme mesure** (aucune mesure détenue).
3. **Manifeste seul, lockfile non committé** (l'habitude « bibliothèque »). Rejetée sans discussion de goût : elle contredit **R-12** frontalement, et elle laisse les dépendances transitives **non désignées** — la Définition 1 devient inatteignable, donc la revendication « un tiers reconstruit le vérificateur » meurt avec elle.
4. **Vendoring des sources en arbre plutôt que registre.** Instruite sérieusement — elle immunise contre la disparition d'un paquet et met tout sous les yeux de la revue. Rejetée aujourd'hui pour trois raisons : (a) **elle ne sert pas ADR-0003**, dont la promesse offline porte sur la vérification et non sur le build — l'invoquer serait une confusion de couches ; (b) **le dépôt passe public à S3** (DEVOPS §1) : y copier des sources tierces fait de nous un redistributeur, avec les obligations d'attribution correspondantes — le dépôt refuse déjà cette position pour `biblio/`, pour la même raison ; (c) l'intégrité qu'elle apporterait est **déjà** apportée par les empreintes du lockfile, tandis que le diff d'une mise à jour devient illisible en revue ordinaire — on paierait en lisibilité de revue ce qu'on n'achèterait pas en intégrité. Conservée en contingence sur les événements nommés en D4.
5. **Reproductibilité bit-à-bit seule, sans provenance attestée.** Rejetée : un rebuild identique établit que *ces sources donnent ces octets*, et ne dit **rien** de quel commit, quelle plateforme et quel processus ont produit le binaire distribué — c'est précisément l'objet de la provenance (« Provenance showing how the package was built », SLSA v1.2, tableau Build L1). Et aucune évidence détenue ne porte la reproductibilité bit-à-bit sur Windows, plateforme de CI du projet (DEVOPS §3).
6. **Provenance attestée seule, sans cible de reproductibilité** (rester en L1/L2 et s'en tenir là). Rejetée comme état final : la spec qualifie elle-même le premier barreau — la provenance L1 est « trivial to bypass or forge » (SLSA v1.2, Build L1, Summary) — et une provenance signée déplace la confiance vers la plateforme de build, quand la promesse d'ADR-0003 est justement une décharge **sans tiers de confiance**. Le rebuild indépendant est la seule décharge de cette forme.
7. **Gates de dépendances en advisory (non bloquantes) le temps du squelette.** Rejetée par règle, pas par préférence : R-22 — ni urgence, ni prototype ne suspend un gate.
8. **Viser Build L3 immédiatement.** Rejetée : ses exigences (« prevent runs from influencing one another », « prevent secret material used to sign the provenance from being accessible to the user-defined build steps ») sont des **propriétés de la plateforme**, que nous n'implémentons pas et que nous ne détenons aucune pièce pour établir ; la spec note d'ailleurs que L3 « usually requires significant changes to existing build platforms ». Écrire un niveau non établi sur pièce serait exactement l'erreur du **déclaré pris pour du mesuré** qu'ADR-0008 refuse au cœur du produit.

### La source qui tranche

**Lamb & Zacchiroli, Définition 1 (p. 2 du préprint détenu)** : « The build process of a software product is reproducible if, after designating a specific version of its source code and all of its build dependencies, every build produces bit-for-bit identical artifacts, no matter the environment in which the build is performed. » Elle tranche parce qu'elle **nomme les deux moitiés au même endroit** : la *désignation* (lockfile + toolchain épinglée : D1, D2) et l'*identité du résultat* (bit-à-bit : D6). Toute politique d'environnement qui n'a que la première produit un build répétable par nous ; c'est la seconde qui rend la promesse « sans confiance dans Shōgen » exécutable par un tiers, et le mécanisme social qui va avec est décrit au même endroit : la confiance s'établit « by comparing outputs acquired from multiple, independent builders » (p. 2).

**SLSA v1.2, page « Build: Track Basics » (statut « Approved » sur la copie datée du 2026-08-12)** fournit l'échelle graduée entre les deux extrêmes que le mainteneur a demandé d'instruire, et **joint** les deux approches plutôt que de les opposer (L2 admet « an after-the-fact reproducible build » comme producteur de provenance). *Note de version, sur pièce* : les copies v1.0 détenues portent « Status: Retired » et « Version 1.2 is the current version » — la v1.0 n'est pas la source citable, la v1.2 l'est.

**Saltzer & Schroeder (§I.A.3 f, copie MIT datée)** fonde la clause d'autorité de CI (D7) : *least privilege*, 1975, énoncé de principe et non usage contemporain. **Sigstore (CCS 2022, p. 2353)** fournit le mécanisme qui rend ce principe tenable sans clé longue durée à protéger, et l'échelle constatée par les auteurs — « more than 2.2M signatures over critical software such as Kubernetes and Distroless » — dit que ce n'est pas un pari d'outillage exotique. **in-toto (USENIX Sec. 2019)** fonde D5 : la chaîne se tient par la liaison des étapes (« artifact flow integrity: All of the artifacts created, transformed, and used by steps must not be altered in-between steps », p. 1395), et non par la somme de contrôles ponctuels ; le lien avec la reproductibilité est constaté par les auteurs eux-mêmes — « in-toto is used in Debian to verify packages were not tampered with as part of the reproducible builds project » (p. 1394).

**Ce qui n'est pas tranché par une source mais par une règle** : R-8 et R-12 du référentiel s'imposent (R-22) ; D5 et D1 en sont l'exécution, pas le choix.

### Ce que la décision coûte

- **La reproductibilité est un effort long, à l'échelle où elle a été mesurée.** Chiffre détenu : « Seven years later, over 95% of the 30 000+ packages in Debian's development branch can now be built reproducibly » (Lamb & Zacchiroli, p. 5). C'est **précisément pourquoi la cible de D6 est restreinte à un binaire** — `shogen-verifier`, dépendances minimales par ADR-0002 — et non au workspace. Étendre la cible au workspace importerait un coût d'un ordre que ce projet ne peut pas payer.
- **Le double-build coûte une construction supplémentaire par push sur le job concerné** (temps de CI ≈ ×2 sur ce job ; aucune mesure détenue — le chiffre réel est dû au premier vert du squelette, avec compte d'exécutions).
- **Un jeu de variations réduit valide moins.** Debian applique « (30+) » variations et les auteurs écrivent que ce grand nombre « can validate build reproducibility to a high degree of accuracy » (p. 5) ; notre sous-ensemble candidat (6 variations) **achète donc moins de confiance**, et ce déficit se publie au lieu de se taire. Un build reproductible sous 6 variations n'autorise aucun énoncé sur les autres.
- **La montée de correctifs devient manuelle.** Exact au manifeste (D3) + R-8 interdisent la fusion automatique d'un bump de dépendance. Coût réel : une advisory qui tombe sur une dépendance transitive non corrigeable immédiatement met la CI au rouge et **force le travail** — c'est l'effet recherché, mais c'est un jour de travail non planifié, et la seule sortie licite est une dette formée (R-13), jamais un fichier d'exceptions édité au passage.
- **Le refus du vendoring nous laisse dépendants de la disponibilité du registre.** La mutation d'un paquet est déjà attrapée par les empreintes du lockfile ; le résidu est la **disparition** — qui casse le build (fail-closed) au lieu de corrompre l'artefact. Coût accepté, événement de réévaluation nommé (D4).
- **Asymétrie de plateforme publiée.** La CI tourne Windows **et** Linux (DEVOPS §3) ; la gate de reproductibilité ne tournera d'abord que sur Linux. Cette asymétrie doit être écrite là où un lecteur pourrait croire l'inverse, sur le patron d'ADR-0007 (« nous ne couvrons pas cette classe »).
- **Ce que le niveau SLSA visé ne dit pas.** Viser Build L2 engage aussi le **consommateur** — « Validate the authenticity of the provenance » : il nous faut publier la commande de contrôle et la maintenir, sinon le niveau est décoratif. Et le niveau réellement atteignable dépend de propriétés de la plateforme de build que **nous ne détenons aucune pièce pour établir** (voir manques) : tant qu'elles ne sont pas établies sur pièce, aucun document sortant n'écrit un numéro de niveau.
- **Le coût de ne pas décider était mesuré ailleurs** : le référentiel doc 01 §5.1, citant Spracklen et al. (USENIX Security 2025 — **non détenu ici**), rapporte que **19,7 % des paquets suggérés n'existent pas** sur 576 000 échantillons de code générés par 16 LLM, et que 43 % des noms hallucinés réapparaissent d'une répétition à l'autre. Chiffres **de seconde main**, cités comme tels ; ils ne fondent pas D5, ils en chiffrent l'enjeu — et la fondation de D5 reste R-8.

### Registres touchés

- **`docs/DEVOPS.md` §4** : passe de « plan » à « décidé », clauses D1–D7 substituées à l'énoncé d'intention — *à porter par l'orchestrateur en phase D*.
- **`docs/DEVOPS.md` §3, ligne S-G7** : le critère « version non exacte » est **porté par rôle à chemins exacts** (D3), et la gate gagne l'entrée « contrôle de registre R-8 absent de la PR qui introduit une dépendance directe » — *à porter*.
- **`docs/09-vocabulaire.md`** : trois formulations **candidates** à l'interdit — (1) « build reproductible » employé en qualificatif d'assurance sans compte de rebuilds ni jeu de variations nommé → écrire « rebuild identique sous [n] variations, [k] exécutions » ; (2) « chaîne d'approvisionnement sécurisée » → écrire la liste des contrôles et ce qu'ils ne couvrent pas ; (3) « SLSA niveau N » écrit sans que les propriétés de plateforme correspondantes soient établies sur pièce → écrire « provenance attestée par [plateforme] ; niveau SLSA non établi ».
- **`docs/08-assumptions.md`** : entrée **candidate** `A(verifier-binary)` — « le binaire `shogen-verifier` qu'un tiers exécute correspond au code source publié » ; source du résidu : Lamb & Zacchiroli p. 1 ; porteur : la promesse offline d'ADR-0003 et 02-vision ; assurance : aucune à ce jour ; décharge : rebuild bit-à-bit indépendant (décharge complète) ou provenance attestée (décharge **partielle** — elle déplace le résidu vers la plateforme de build). Le registre fait foi : cette entrée est une proposition au bureau de l'orchestrateur, pas une écriture.
- **`docs/12-fondations-ingenierie-design.md` §9** : trois seuils de plus au paquet de ratification (épinglage, reproductibilité, niveau SLSA) — plus le jeu de variations.
- **`biblio/INDEX.md`** : rien de neuf ; les cinq artefacts de cette ADR y sont déjà enregistrés (S2.5).
- **Couture avec ADR-0009** : MSRV, edition et canal de toolchain restent à 0009 ; cette ADR n'en fixe que le **régime** (épinglé, versionné, entrée de build).

---

## ADR-0013 — DevOps : gates et flux en doctrine ratifiée

**Statut** : acceptée · 2026-08-12 · ratifiée le 2026-08-12 par délégation explicite du mainteneur (« je délègue cette décision à mon agent orchestrateur… les réponses doivent se baser sur une étude académique rigoureuse ») — seuils chiffrés ratifiés comme **budgets déclarés révisables par ADR**, au statut exact que leurs sources autorisent

**Adjudication orchestrateur (2026-08-12)** : draft rendu par un worker de
la passe S2.5 (run `wf_e704a674-9da`) ; les 41 citations du draft ont été
re-établies par l'orchestrateur avant écriture — le corpus doc 02 (v1.4)
lu en entier par l'orchestrateur (Nature l. 5, G0 l. 31, G2 anti-métrique
l. 42, G7 l. 71, R-22 l. 111, R-23 l. 112, R-25 l. 114), DeMillo relu aux
pp. 34-36 et 39, Jia & Harman pp. 1 et 3, Inozemtseva & Holmes p. 1,
in-toto pp. 1393-1395, Sigstore pp. 2353-2354, et les documents internes
(DEVOPS, DECISIONS, 12, JOURNAL, WISHLIST, charte shogen-devops)
contrôlés en lecture directe. **Une citation corrigée à l'écriture** : le
draft portait « secure but accessible » là où Sigstore p. 2354 §2.1 écrit
« secure and accessible » — corrigée ci-dessous à la forme du texte.
*(Adjudication inversée — réparée le 2026-08-12, ouverture de S3 : la
page 2354 relue visuellement au fichier ET l'extraction texte concordent
sur « secure **but** accessible » ; le draft du worker était fidèle, la
« correction » ci-dessus était le faux. Site rétabli. Première prise de
la gate S-G5 le jour de son instanciation.)*

### Contexte

`docs/DEVOPS.md` porte, depuis le 2026-07-30, sept gates (§3, S-G1…S-G7),
une chaîne d'approvisionnement auto-imposée (§4) et des règles de flux (§5)
— et se déclare lui-même « plan, rien n'est encore en place ». Ces
prescriptions n'ont aucune ADR de rattachement. Or le référentiel qualité du
mainteneur, opposable à ce dépôt depuis le 2026-08-12 (CLAUDE.md projet ;
corpus doc 02, R-24), pose en preuve de G0 qu'« un composant sans ADR de
rattachement ne se code pas ». La phase C de S2.5 (12 §6.1) doit écrire du
code de gate et de CI : sans cette ADR, elle écrirait hors G0.

Trois faits du dépôt bornent la rédaction, et ne sont pas rouverts :
`main` est déjà protégée et les signatures déjà exigées (DEVOPS, état
d'exécution du 2026-07-30 : « force-push interdit, suppression interdite »,
signatures de commit requises, admins inclus) ; ADR-0003 fait de la
recalculabilité offline par un tiers la promesse centrale du produit ; le
walking skeleton de 12 §5 exige d'exercer la vraie « CI (Windows ET Linux) »
avant tout code produit.

Cette ADR ne fixe aucun plancher de couverture ni de score de mutation
(ADR-0011), aucune politique d'épinglage de dépendances ni cible de
reproductibilité (ADR-0012). Elle décide **la forme des gates et du flux**,
et le régime — bloquant ou consultatif — sous lequel elles vivent.

### Décision

**1. Les sept gates sont bloquantes et non discrétionnaires.** S-G1…S-G7
(DEVOPS §3) sont la forme d'exécution locale des gates G3 (vérification
automatique) et G4 (santé architecturale) du corpus, S-G7 portant en outre
le volet dépendances de G6. Aucune n'est consultative. Un rouge arrête
l'intégration. La seule voie licite de relâchement est une ADR qui modifie
la gate ; jamais un `--no-verify`, un `#[allow]` ponctuel, une exception de
chemin, ni une dérogation orale. Aucun « break-glass » administrateur n'est
créé — la protection incluant déjà les admins reste telle.

**2. Quatre invariants de construction, opposables à toute gate présente ou
future** (doctrine gatewright, `shogen-devops` §2) :

- *sélection par rôle à chemins exacts* — une gate énumère les chemins
  qu'elle couvre ; elle ne fait jamais confiance à un nom qu'un fichier se
  choisit lui-même ;
- *ligne de couverture avant verdict* — « Une gate imprime sa couverture
  (N examinés sur N présents) » **avant** de dire vert ou rouge. La
  couverture est un signal affiché, jamais le critère de succès de la
  gate ;
- *mutant semé tué avant tout vert* — « Aucun vert n'est rapporté sans
  mutant semé » : la violation que la gate existe à attraper est
  introduite, vue mourir, restaurée, puis committée comme test permanent.
  Une gate jamais exercée ainsi n'a pas de registre d'assurance. Le plancher
  — au moins un mutant semé et tué par gate **et par modification de
  gate** — est un seuil candidat (« candidat — ratification mainteneur
  due », §seuils) ;
- *l'évasion devient test permanent* — toute violation constatée qui a
  franchi une gate entre au corpus de mutants de cette gate, dans la même
  unité de travail que le correctif.

**Registre que ces invariants autorisent** : une gate ainsi exercée est
*tested* — avec son compte (n mutants semés, n tués, date). Jamais *proven*.
Un vert de CI n'atteste que ce que les mutants semés ont montré ; hors de
ce corpus, la gate ne dit rien.

**3. Flux trunk-based sur `main` protégée.** PR obligatoire, gates requises
au vert, « pas de force-push, tags protégés », historique linéaire,
signatures exigées, admins inclus. Aucune branche de long cours (`develop`,
`release/*`, `hotfix/*`) : les branches sont courtes et meurent à
l'intégration. Un dépôt/branche `throwaway` reste licite pour un prototype
assumé (corpus R-22) et ne peut pas être promu sans repasser G0–G7 — c'est
le régime déjà appliqué à `s2-harness/` (12 §1).

**4. CI Windows ET Linux, bloquantes toutes deux, sur chaque push**, et les
mêmes gates rejouables en local (« sur chaque push, mêmes gates en local via
`just verify` »). Le nombre de plateformes est un seuil candidat
(« candidat — ratification mainteneur due », §seuils : 2).

**5. Chaîne signée et épinglée.** Commits signés (déjà exigés par la
protection de branche) ; actions GitHub épinglées par SHA de commit, jamais
par tag — « la version taguée d'une action est une page mutable ». Ce que
cette ADR revendique ici est exactement borné : signer les commits et
épingler les actions sont des mesures *par étape*, nécessaires et
insuffisantes ; la propriété de chaîne (attestations, provenance de build)
relève d'ADR-0012 et n'est pas revendiquée ici.

**6. Traçabilité par unité de travail.** « Une ligne de `JOURNAL.md` par
unité de travail » devient opposable, et la PR porte : son ADR de
rattachement, sa ligne de journal, la sortie des gates avec leur ligne de
couverture, et le compte de mutants tués si une gate a été touchée. La
**mécanisation** de la ligne de journal (gate candidate S-G8) est assignée à
la phase C : jusqu'à ce qu'elle existe, la règle vit dans la checklist de
PR, et cette assignation est nommée ici pour ne pas devenir une dette nue.

**7. PR petites et unitaires** : un sujet par PR, une ADR de rattachement,
commits mécaniques (fmt, renommages, fins de ligne) séparés des commits de
fond. La borne chiffrée exigée par R-25 est un seuil candidat
(« candidat — ratification mainteneur due », §seuils) : la part qualitative
est décidée maintenant, la valeur numérique reste sans source détenue.

**8. Ce que le flux ne délègue pas** : seul l'orchestrateur committe
(corpus R-19/R-20), le réviseur n'est jamais le générateur (P6/R-6), et
aucun objectif de délai n'est opposable à une revue (anti-métrique du
corpus). La vitesse de revue n'est pas une métrique de ce projet.

### Alternative considérée

**A — Gates consultatives (avertissement, CI verte quand même).** Rejetée
frontalement par le référentiel : « les gates sont non discrétionnaires : ni
« urgence », ni « prototype », ni « on repassera dessus » ne suspend un
gate », et « tout gate rouge bloque sans exception ni dérogation orale ».
Rejet renforcé par un argument interne : une gate consultative n'a pas de
mutant à tuer — rien ne distingue son avertissement de son silence, donc
elle ne porte aucun registre d'assurance et son coût de maintenance est
payé sans contrepartie mesurable.

**B — git-flow (`develop`, `release/*`, `hotfix/*`).** Rejetée pour trois
raisons, dont la dernière est une limite déclarée : (a) R-25 borne la taille
de lot — des branches de long cours grossissent mécaniquement le lot et
diffèrent l'intégration, ce que la règle existe pour empêcher ; (b) la
machinerie de git-flow répond au maintien parallèle de plusieurs versions
livrées, problème que ce dépôt n'a pas — un seul committant par règle
(R-20), une seule ligne, aucun binaire publié avant S3 ; (c) **la base
empirique habituellement invoquée pour le trunk-based n'est pas détenue** :
Humble & Farley 2010 et Forsgren-Humble-Kim 2018 sont en procurement formé
depuis le 2026-08-12 (WISHLIST §Priorité 3, usage nommé « ADR-0013 »).
Le rejet de git-flow est donc ici *reviewed* (orchestrateur, à la date
d'adjudication), adossé à R-25 et aux faits du dépôt — jamais *proven* ni
*tested* — et cette ADR se relit à réception des deux ouvrages, le point B
étant le premier à re-instruire.

**C — CI Linux seule (moitié moins de minutes, pipeline plus rapide).**
Rejetée : ADR-0003 (« Le certificat est recalculable offline, jamais
seulement émis ») fait du recalcul par un tiers la promesse du produit ; un
vérificateur exercé sur un seul OS aurait sa recalculabilité *tested* sur
une plateforme et affirmée sur les autres — exactement le glissement que le
registre de vocabulaire interdit. L'environnement Windows du mainteneur a
de plus déjà produit un incident de plateforme — la « leçon des 1476 lignes
CRLF de Kraidle » (DEVOPS §5 ; le dépôt frère, pas celui-ci) — qu'une CI
mono-plateforme n'aurait pas vu.

**D — Actions GitHub référencées par tag.** Rejetée : un tag est mutable,
donc le contenu d'une étape de la chaîne peut changer sans que la
description de la chaîne change. C'est l'interposition que le modèle de
menace d'in-toto nomme, et l'inverse de l'exigence d'intégrité de plan de
chaîne (« no steps can be added or removed, and no steps can be
reordered »).

**E — Un « break-glass » administrateur pour débloquer une CI cassée par
une panne amont.** Rejetée : R-22 ne prévoit aucun passage exceptionnel, et
la protection de branche inclut déjà les admins (fait constaté du
2026-07-30). La voie licite est une ADR — ou une gate rendue robuste à la
panne — jamais un contournement ponctuel.

**F — Mécaniser d'abord, semer les mutants ensuite (« on vérifiera les
gates quand elles seront toutes écrites »).** Rejetée : c'est précisément
l'ordre que la doctrine interdit (« mutant semé tué avant de croire le
premier vert »), et la littérature de mutation dit pourquoi — un jeu de
tests ne se mesure que par ce qu'il est capable de distinguer, pas par le
fait qu'il passe.

### La source qui tranche

**1. Le référentiel du mainteneur — la source qui tranche la question
posée** (« bloquantes ou consultatives ? »). Corpus « Compliance et
ingénierie logicielle et architecturale », doc 02 v1.4 (2026-08-12) : en
tête, « Un gate non franchi bloque ; il n'existe pas de passage
« exceptionnel » » ; R-22 : « les gates sont non discrétionnaires : ni
« urgence », ni « prototype », ni « on repassera dessus » ne suspend un
gate » ; G7 : « tout gate rouge bloque sans exception ni dérogation orale ».
Assurance de cette source : **reviewed** (mainteneur, 2026-08-12) — le même
registre qu'ADR-0006, dont la source qui tranche est « Décision du
mainteneur, énoncée le 2026-07-30 — assurance : *reviewed* ». Ce n'est ni
un résultat expérimental ni une mesure, et cette ADR ne le présente pas
comme tel.

**2. La fondation académique du mutant semé.** DeMillo, Lipton & Sayward
1978 (détenu) décrivent le geste exact que la doctrine gatewright
transpose : un système de mutation « determine[s] the extent to which a
given set of test data has adequately tested a Fortran program by direct
measurement of the number and kinds of errors it is capable of uncovering »
(p. 36) — ce qui est mesuré, c'est la capacité de détection, pas le succès.
Les auteurs bornent eux-mêmes leur principe : « There is, of course, no hope
of "proving" the coupling effect; it is an empirical principle » (p. 35) —
d'où le registre *tested*, jamais *proven*, imposé au §2 de la Décision.
Jia & Harman 2011 (détenu) portent le vocabulaire : « the seeded fault
denoted by the mutant is detected », et « The mutation score is the ratio of
the number of detected faults over the total number of the seeded faults »
(p. 1 du fichier, §I).

**Le pas de transposition, nommé plutôt que masqué** : ces travaux mesurent
un *jeu de tests* en semant une faute dans un *programme*. Ici l'objet
mesuré est une *gate* et la faute semée est la violation que la gate existe
à attraper. C'est une analogie de méthode, argumentée — pas un résultat
importé. Elle hérite de la même hypothèse de représentativité que la
mutation classique, celle que Jia & Harman formulent ainsi : « It states
that programmers are competent, which implies that they tend to develop
programs close to the correct version » (p. 3, §II.A). Sur une gate, cela se
lit : le mutant semé ressemble aux violations réelles. Rien ne l'établit —
c'est la raison de l'invariant « l'évasion devient test permanent », qui
fait de chaque contre-exemple réel un mutant supplémentaire.

**3. La couverture comme signal, jamais comme cible.** Inozemtseva & Holmes
2014 (détenu), abstract : « coverage, while useful for identifying
under-tested parts of a program, should not be used as a quality target
because it is not a good indicator of test suite effectiveness ». C'est ce
qui fonde l'ordre imposé — la ligne de couverture s'imprime *avant* le
verdict et ne le décide pas. (Les planchers chiffrés restent à ADR-0011.)

**4. La chaîne signée : ce qu'elle vaut et où elle s'arrête.** Torres-Arias
et al. 2019 (détenu) situent exactement les mesures retenues au §5 :
« Currently, supply chain security strategies are limited to securing each
individual step within it. For example, Git commit signing controls which
developers can modify a repository » (p. 1393, §1), et « These piecemeal
measures by themselves can not stop malicious actors because there is no
mechanism to verify that: 1) the correct steps were followed and 2) that
tampering did not occur in between steps » (p. 1393, §1) ; « Point solutions
designed to secure individual supply chain steps cannot guarantee the
security of the entire chain as a whole » (p. 1395, §3). Lecture honnête
pour Shōgen : commits signés et actions épinglées sont nécessaires et
insuffisants, et cette ADR ne prétend pas à la propriété de chaîne. Le même
papier fonde l'épinglage par SHA — « All of the steps defined in a supply
chain are performed in the specified order. This means that no steps can be
added or removed, and no steps can be reordered » (p. 1395, §2.3) — et la
traçabilité par PR : « software rarely (if ever) includes information about
what tools were run or their results » (p. 1395, §3) est exactement le vide
que la ligne de JOURNAL et les sorties de gates attachées à la PR
comblent localement.

**5. Pourquoi la signature doit être imposée par la protection, pas par la
discipline.** Newman, Meyers & Torres-Arias 2022 (détenu) : « Software
signing, a promising mitigation for many of these attacks, has seen limited
adoption in open-source and enterprise ecosystems » (p. 2353, abstract), et
« the vast majority of packages in popular software repositories that
support signatures, such as the Python Package Index (PyPI), are unsigned »
(p. 2353, §1). Signer est le comportement minoritaire de l'écosystème :
laissé à la discipline, il s'érode ; c'est la branch protection qui le
tient, et elle le tient déjà.

### Ce que la décision coûte

- **Le gel.** Une gate rouge arrête tout, y compris quand la cause est une
  panne amont (registre d'actions, runner indisponible), et aucun
  contournement n'existe. Coût non chiffré : aucune source détenue ne mesure
  la fréquence ou la durée de tels gels. La contrepartie assumée est celle
  du référentiel — l'existence et le caractère bloquant ne se paramètrent
  pas.
- **Le mutant semé.** Un cycle supplémentaire par gate *et par modification
  de gate* : semer, voir mourir, restaurer, committer le mutant. Le corpus
  de mutants croît de façon monotone (l'évasion s'y ajoute), donc le temps
  de CI croît avec l'historique des incidents. Coût non chiffré : aucune
  source détenue ne mesure ce surcoût — DeMillo et al. discutent le coût du
  système de mutation, pas celui de cette transposition.
- **La double plateforme.** Deux exécutions par job à chaque push (facteur
  2 sur les minutes de CI, arithmétique et non mesurée ici), plus la
  lenteur relative des runners Windows et la gestion des fins de ligne — le
  `.gitattributes` exigé dès le premier commit (DEVOPS §5) est la mitigation
  déjà décidée, née de la « leçon des 1476 lignes CRLF de Kraidle » — dépôt
  frère, même environnement Windows.
- **La signature.** Garde de clé : « Traditionally, the signer must keep the
  private signing key secure but accessible; this is the source of many
  usability issues » (Sigstore, p. 2354, §2.1). Le dépôt a déjà payé cette
  facture une fois : clé SSH dédiée, bascule d'identité git, puis « Commit
  fondateur amendé, » « re-signé, re-poussé » (DEVOPS, état d'exécution du
  2026-07-30) — un ancien hash a cessé d'exister.
- **L'épinglage par SHA.** Aucune mise à jour automatique des actions : une
  corvée de renouvellement, et la charge de savoir qu'une action épinglée
  est devenue vulnérable. Ce point est **assigné à ADR-0012** (politique de
  dépendances et d'advisories), pas laissé ouvert ici.
- **Les PR petites.** Plus de PR, donc plus de cycles de revue, sans
  possibilité de compenser par la vitesse : « Aucun objectif de délai de
  revue ne peut être opposé à un réviseur au titre de ce référentiel ». Le
  coût est du temps réel, et il est revendiqué. Le seul chiffre disponible
  sur l'enjeu est de seconde main et se cite comme tel : −7,2 % de stabilité
  de livraison pour +25 points d'adoption d'IA, **rapporté par le corpus doc
  02 (R-25) citant DORA 2024** — l'artefact DORA n'est pas détenu côté
  Shōgen.
- **Le trunk sans branche de long cours.** Aucun entretien parallèle d'une
  version livrée. Acceptable tant que le dépôt est privé et pré-S3 ; le jour
  où une version publiée du vérificateur doit être corrigée sans embarquer
  le tronc, cette ADR se rouvre (c'est le déclencheur nommé, pas une dette).
- **La ligne de JOURNAL non mécanisée.** Tant que S-G8 n'existe pas, la
  règle vit dans une checklist humaine — l'exact type de contrôle dont ce
  dépôt écrit qu'il « ne vaut rien » s'il ne tourne que quand on y pense.
  Assigné à la phase C ; l'écart est nommé, daté et porté, pas toléré.

### Registres touchés

- **`docs/DEVOPS.md` §3 et §5** : cessent d'être un « plan » et deviennent
  l'exécution de cette ADR (réécriture en phase D, 12 §6.1) ; §4 reste
  gouverné par ADR-0012.
- **`docs/12` §3, entrée ADR-0013** : fermée par ce draft (adjudication
  orchestrateur).
- **`docs/09-vocabulaire.md`** : entrée candidate — « CI verte donc code
  correct » / « gate verte donc conforme » (une gate verte n'atteste que ce
  que ses mutants ont montré ; on écrit « gate S-Gx verte, n mutants semés
  tués le [date] »). Proposée, non écrite par ce worker.
- **`docs/08-assumptions.md`** : assumption candidate — A(gate-adequacy) :
  « les mutants semés d'une gate représentent les violations réelles que la
  gate doit attraper ». Indéchargeable en général ; sa seule voie de
  réduction connue est l'invariant « l'évasion devient test permanent ».
  Proposée, non écrite par ce worker.
- **`JOURNAL.md`** : la règle « une ligne par unité de travail » devient
  opposable ; mécanisation (S-G8) assignée à la phase C de S2.5.
- **`WISHLIST.md` §Priorité 3** : les deux ouvrages d'usage « ADR-0013 »
  (Humble & Farley 2010 ; Forsgren, Humble & Kim 2018) restent en
  procurement ; à réception, relecture de cette ADR — alternative B en
  premier.
- **ADR-0011 / ADR-0012** : cette ADR leur renvoie explicitement les
  planchers de couverture et de mutation (0011) et la politique
  d'épinglage/advisories des actions et dépendances (0012). Aucun seuil de
  ces deux domaines n'est fixé ici.

---

## ADR-0014 — Licence du dépôt : décision contractée à l'entrée de S3 ; crates non publiables d'ici là

**Statut** : acceptée (ratifiée par délégation mainteneur du 2026-08-12) · 2026-08-12

### Contexte

La phase C de S2.5 a laissé le champ `license` des trois crates vide —
délibérément : le choix appartient au mainteneur. Conséquence, vue par
l'orchestrateur : `cargo deny check licenses` est rouge sur `shogen-core`,
`shogen-verifier` et `xtask` (`error[unlicensed]`), et l'étape CI
correspondante bloquerait tout push. Faits de cadre : le dépôt est privé
jusqu'à S3 et son passage public est l'événement qui rend la licence
opposable (DEVOPS §1) ; la vision exige qu'à cette date le vérificateur
soit ouvert (« un vérificateur fermé contredit la vision ») ; `publish =
false` est déjà posé au niveau workspace — aucune crate n'est publiable
aujourd'hui, c'est un fait de manifeste, pas une intention. Choisir une
licence est une décision juridique et stratégique de produit ; **aucune
pièce détenue dans `biblio/` n'instruit ses conséquences** — la trancher
ce soir serait une préférence non tracée, le défaut exact que le motif
« Zig, rejeté faute de pièce » d'ADR-0009 refuse.

### Décision

1. **Le choix de licence est une décision d'entrée de S3**, au déclencheur
   nommé : le passage public du dépôt (DEVOPS §1, §7 pt 6). L'instruction
   due à ce moment est cadrée d'avance — options à instruire : « MIT OR
   Apache-2.0 » (la convention de l'écosystème Rust, permissive, avec la
   concession de brevets d'Apache-2.0) ; AGPL-3.0 (protectrice) ; licences
   **différenciées par crate**, le vérificateur au régime le plus ouvert
   (c'est l'artefact de confiance). Propriétaire : le mainteneur.
   Échéance : l'événement S3, pas une date.
2. **D'ici là, la gate S-G7-licences accepte les crates non publiables** :
   `private = { ignore = true }` dans `deny.toml` — modification de gate
   **portée par cette ADR** (charte `shogen-devops` §2 : jamais
   d'affaiblissement sans ADR). Périmètre exact de l'assouplissement : les
   seules crates `publish = false` du workspace ; les 18 crates tierces
   restent contrôlées, `include-dev = true` inchangé.
3. **Le re-serrage est mécanique** : l'ignore ne couvre que les crates non
   publiables. Rendre une crate publiable sans licence remet la gate au
   rouge d'elle-même — au moment exact où la décision devient exigible.

### Alternative considérée

**(a) Choisir « MIT OR Apache-2.0 » maintenant.** Rejetée : aucune pièce
détenue n'instruit les conséquences juridiques et stratégiques pour un
produit commercial ; décider sans pièce serait une préférence non tracée.
L'option reste la première à instruire à S3.

**(b) Laisser le rouge en place jusqu'à S3.** Rejetée : un rouge permanent,
connu et non actionnable détruit la valeur d'alerte de la gate — le mode
d'échec « une ligne imprimée que personne ne lit » (ADR-0011) — et le
référentiel exige qu'un point ouvert vive dans un registre contracté
(R-13, G5), pas dans une CI rouge qu'on apprend à ignorer.

**(c) Poser l'ignore sans ADR.** Interdit : la charte `shogen-devops` §2
refuse tout affaiblissement de gate sans ADR — c'est précisément le cas
que la clause existe pour couvrir.

### La source qui tranche

Corpus « Compliance et ingénierie logicielle et architecturale », doc 02
(v1.4, lu en entier par l'orchestrateur le 2026-08-12), G5 : le seul cas
licite de dette résiduelle est la « dette *prudente et délibérée* au sens
du quadrant de Fowler, contractée par écrit », consignée dans un
« registre de dette avec propriétaire et échéance ». **Cette ADR est ce
contrat écrit** : propriétaire (mainteneur), échéance (entrée de S3),
déclencheur de re-serrage mécanique. Assurance : *reviewed* — délégation
explicite du mainteneur du 2026-08-12 (« je délègue cette décision à mon
agent orchestrateur »), exercée sur le référentiel qu'il a rendu opposable.

### Ce que la décision coûte

- La décision reste ouverte et arrivera avec l'entrée de S3, un moment
  déjà chargé — mitigé par le cadrage d'avance (options nommées au pt 1)
  et par le re-serrage mécanique (pt 3) qui rend l'oubli impossible.
- Jusqu'à S3, la gate licences ne surveille plus nos propres crates ; elle
  continue de surveiller tout le graphe tiers, dev compris.

### Registres touchés

- `deny.toml` : `[licenses] private = { ignore = true }` — la
  modification est portée par cette ADR et committée avec elle.
- `docs/12-fondations-ingenierie-design.md` §10, item 1 : résolu par
  contrat (cette ADR) ; item 6 (CI Linux) : débloqué.
- `WISHLIST.md` : rien — aucune pièce à procurer pour ce report ;
  l'instruction de S3 dira si l'analyse juridique exige des acquisitions.

## ADR-0015 — Le transport de S3 : TLSNotary en mode Notary, avec vérification déléguée à un binaire compagnon épinglé

**Statut** : acceptée (adjugée par l'orchestrateur sur pièces le 2026-08-13
— révision mainteneur ouverte) · 2026-08-13

> **Note d'adjudication (2026-08-13).** Draft de worker (`claude-opus-5`,
> run `wf_8db62dce-162`), adjugé par l'orchestrateur : les affirmations
> porteuses re-vérifiées une à une sur les pièces détenues — `use std::fmt;`
> dans `presentation.rs` épinglé (1 occurrence), champs `license` absents de
> `tlsn-attestation` et `tlsn-formats` et présents sur les 6 autres
> manifestes détenus, aucun `LICENSE` à la racine amont (12 entrées d'API,
> zéro) et `"license":null` aux métadonnées, 8 jobs CI amont tous
> `ubuntu-latest` (zéro windows/macos), 15 releases toutes
> `prerelease: true` (alpha.15 publiée 2026-05-21T19:47:08Z), et chaque
> citation-clé greppée sur sa copie. **Une requalification d'adjudication** :
> le compte de fermeture de dépendances de la forme α — le chiffre du
> worker (116, fermeture à features déclarées) et le recompte majorant de
> l'orchestrateur (359, fermeture sans élagage de features depuis les mêmes
> manifestes et le même lock) sont TOUS DEUX portés au tableau avec leur
> méthode ; l'écart mesure la sensibilité aux features, pas une incertitude
> sur l'ordre de grandeur (plus de cent crates tierces dans les deux cas),
> et le compte définitif est la mesure R-8 du compagnon, due en phase C.

### Contexte

S3 doit produire le premier chemin complet sur **un** transport : source
réelle → témoignage canonique → vérification offline par un binaire séparé
qui nomme le résidu (05 §S3 ; 13 §1). Le critère de sortie est écrit et
binaire : une commande `shogen verify <lot>` retourne « valide sous
A(notary-neutrality) » sur un témoignage réel, et échoue fail-closed sur
trois mutants semés. Le candidat nommé par la roadmap est TLSNotary.

Deux questions se posent ensemble, et l'une commande l'autre :

1. **Quel transport, et sous quelle de ses formes ?** TLSNotary offre deux
   formes distinctes — un *Verifier* qui co-conduit la session, et un
   *Notary* qui la co-conduit à la place d'un vérificateur absent et signe
   une attestation portable.
2. **Sous quelle forme la vérification du transport entre-t-elle dans
   `shogen-verifier` ?** C'est la tension nommée en 13 §2 : le contrôle (1)
   de 03 §4 exige l'outil de vérification du transport, or `shogen-verifier`
   est aujourd'hui à **zéro dépendance tierce** (`cargo tree -p
   shogen-verifier -e normal` : une seule arête, `shogen-core`) et vise
   `#![no_std]` + `alloc` en gate à S3 (ADR-0009 pt 6).

Le corpus §S3 de l'INDEX a été acquis à l'ouverture de la passe (67 pièces,
sha256 recalculés en destination, 0 divergence). Il consigne cinq faits
d'état que cette ADR doit instruire, et non contourner : serveur notaire
déprécié, aucun vérificateur autonome, crates non publiées sur crates.io,
version alpha, TLS 1.2 seulement avec contradiction interne sur TLS 1.3.

### Décision

#### A. Le transport : `tlsn-mpc/1`, **mode Notary**, notaire opéré par Shōgen en S3

1. **Le transport de S3 est TLSNotary en MPC-TLS**, identifiant de champ
   `transport` = `tlsn-mpc/1` — la valeur déjà écrite en 03 §2, aucune
   invention de vocabulaire.

2. **La forme retenue est le mode Notary** (attestation → présentation), et
   non le mode Verifier direct. **Motif structurel, pas préférentiel** : le
   critère de S3 exige un artefact vérifiable *offline*, par un binaire
   séparé, après la session. Le mode Verifier direct ne produit aucun tel
   artefact — la preuve ne convainc que le participant. Le projet l'écrit
   lui-même : « Every zkTLS protocol today is designated-verifier in this
   way. » (billet officiel du 2026-06-17, détenu). Choisir le mode Verifier
   direct, ce serait choisir un mode où `shogen verify <lot>` n'a **rien** à
   vérifier. La roadmap avait donc déjà tranché sans le dire : en nommant
   A(notary-neutrality) dans son critère, elle nommait le résidu de la
   délégation, donc le mode Notary.

3. **Le rôle de Notary est joué par un processus opéré par Shōgen**,
   construit depuis la bibliothèque amont épinglée — et **non** par un
   service hébergé. Fait d'état contraignant, sur pièce : « The Notary
   server was removed from the TLSNotary project in alpha.13. » (page
   « Notary Server (Deprecated) », détenue), le service public a été
   arrêté, et « The project's scope was narrowed to focus on the core
   TLSNotary libraries and the upcoming SDK. » Le rôle survit comme rôle de
   bibliothèque : « TLSNotary also supports a workflow where a Verifier
   (acting as Attestor) attests to the proven data. » (Rust Quick Start,
   détenu).

4. **Le résidu de ce montage est nommé, aggravé, et écrit dans le verdict.**
   A(notary-neutrality) n'est pas seulement non déchargée en S3 : elle est
   portée par Shōgen lui-même, c'est-à-dire par la partie dont 02-vision
   exige qu'on ne lui fasse pas confiance. Une entrée nouvelle est due au
   registre 08 — **A(self-attestation)** — et le verdict de S3 la porte à
   côté d'A(notary-neutrality). Ce que S3 démontre est **la chaîne et la
   forme de l'artefact**, pas la neutralité ; ce que S3 ne démontre pas se
   dit dans la même phrase que ce qu'il démontre.

5. **Une condition de bascule mécanique, décidée d'avance.** TLSNotary
   « currently supports TLS 1.2. Support for TLS 1.3 is on the roadmap. »
   (page intro, copie du 2026-08-12) — et la FAQ courante dit l'inverse :
   « There are no immediate plans to support TLS 1.3. » **Aucune pièce
   détenue n'établit qu'un endpoint du pool S2 (10 §3.1) accepte encore une
   poignée de main TLS 1.2.** Une mesure est donc due en tête de phase C :
   négociation TLS 1.2 tentée contre les 11 sources répondantes, résultat
   consigné. **Si zéro endpoint du pool accepte TLS 1.2, le chemin réel de
   S3 est mécaniquement inconduisible** et l'alternative (c) ci-dessous
   prend effet **par règle**, sans improvisation ni renégociation du
   critère. La décision porte donc son propre fail-closed.

#### B. La forme d'intégration : **vérification déléguée à un binaire compagnon** (forme β)

6. **`shogen-verifier` n'importe aucune crate du transport.** Il reste à
   zéro dépendance tierce, et l'échéance contractée « `#![no_std]` +
   `alloc` devient une gate en S3 » (ADR-0009 pt 6, 13 §3 item 3) **reste
   due telle quelle** — elle n'est ni repositionnée ni reportée.

7. **Un binaire compagnon `shogen-tlsn-verify`**, hors membres du workspace
   (comme `adapters/` l'est déjà), construit depuis l'amont épinglé par
   révision git exacte, exécute `Presentation::verify(&CryptoProvider)` et
   imprime un résultat structuré : clé de vérification, `server_name`,
   `connection_info.time`, longueurs de transcript, et le hash des octets
   révélés. C'est un **adapter** au sens d'ADR-0001 — « les transports sont
   des adapters » — donc « testé, jamais prouvé ».

8. **`shogen-verifier` vérifie la liaison, et nomme ce qu'il ne vérifie
   pas.** Ses contrôles, tous purs et sans dépendance :
   - (a) le lot décode dans le sous-ensemble canonique CBOR et se ré-encode
     à l'octet près (acquis S2.5, conservé) ;
   - (b) le hash de `utterance` porté par le témoignage égale le hash des
     octets révélés rapportés par le compagnon (ADR-0005 règle 1 : le hash
     des octets exacts « lie le témoignage à sa preuve de transport ») ;
   - (c) le hash des octets de `transport_proof` égale celui que le
     compagnon déclare avoir consommé — c'est ce qui interdit qu'on vérifie
     une preuve et qu'on en livre une autre ;
   - (d) `residual` résout dans le registre publié (08) ;
   - (e) **le verdict nomme la délégation**, chaîne proposée : "valide sous
     A(notary-neutrality), A(self-attestation) et
     A(transport-check-delegated) — le contrôle cryptographique de la preuve
     de transport a été exécuté par shogen-tlsn-verify [révision amont],
     jamais par ce binaire".
   Le contrôle (1) de 03 §4 n'est donc pas escamoté : il est **exécuté
   ailleurs et déclaré comme tel**, ce que 13 §2 autorisait explicitement
   (« le vérificateur Shōgen vérifie alors la chaîne hash→proof et nomme ce
   qu'il n'a PAS vérifié lui-même »).

9. **Trois résidus nouveaux sont dus au registre 08** : A(self-attestation),
   A(transport-check-delegated), A(upstream-alpha). Aucun ne se déduit d'un
   autre.

10. **Où atterrit COSE (ADR-0002, `Cose_Sign1`).** Sur l'**enveloppe
    Shōgen**, jamais sur la preuve de transport, et **pas en S3**.
    - *Jamais sur la preuve* : l'attestation TLSNotary est signée par son
      propre schéma — `SignatureAlgId::SECP256K1` / `SECP256R1` /
      `SECP256K1ETH` (`signing.rs` amont épinglé) — et sérialisée en
      `bcs`/`bincode` (dépendance `bcs` au manifeste `tlsn-attestation` ;
      l'exemple officiel lit la présentation par `bincode::deserialize`).
      La ré-emballer en COSE serait re-spécifier un transport, ce
      qu'ADR-0001 interdit. `transport_proof` reste ce que 03 §1 dit qu'il
      est : des octets « opaque pour Shōgen ».
    - *Sur l'enveloppe* : le slot de `Cose_Sign1` est la signature du
      **lot** — la structure taguée est « identified by the CBOR tag 18. »
      (RFC 9052 §4.2, détenue) — au-dessus du payload CBOR des « Core
      Deterministic Encoding Requirements » (RFC 8949 §4.2.1, détenue).
    - *Pas en S3* : ADR-0003 pose que la signature de Shōgen est « un
      commodité de cache, jamais la racine de confiance » (graphie du
      registre). Sur un lot à un témoignage dont la vérification est un
      recalcul (13 §6 pt 2), il n'y a rien dont la signature soit utile.
      **S3 laisse le slot nommé et vide** ; l'émission effective de
      `Cose_Sign1` appartient à S4, avec le certificat. C'est un état
      écrit, pas un oubli.

11. **Condition de réouverture, nommée d'avance** (pour que la forme β ne
    devienne pas un dogme) : la forme α (vérification embarquée dans
    `shogen-verifier`) redevient instruisible dès que **les trois**
    conditions sont réunies chez l'amont — (i) publication sur crates.io
    avec version de registre, (ii) champ `license` présent au manifeste de
    la crate portant `Presentation::verify`, (iii) un chemin de
    vérification `no_std`. Aucune n'est vraie au 2026-08-13, et le
    §« coûts » chiffre pourquoi chacune compte.

### Alternative considérée

#### (a) Forme α — vérification embarquée dans `shogen-verifier`

Rejetée. Chiffrée sur les pièces détenues (manifestes amont + lock amont
`tlsn-repo-cargo-lock-2026-08-12.lock`), **deux comptes, deux méthodes,
portés ensemble** (note d'adjudication en tête) :

| grandeur | aujourd'hui | forme α |
|---|---|---|
| dépendances tierces du graphe normal de `shogen-verifier` | **0** | **116** (fermeture à features déclarées, calcul worker) à **359** (fermeture majorante sans élagage de features, recompte orchestrateur) — compte définitif : mesure R-8 du compagnon, phase C |
| dont épinglées git (hors registre) | 0 | ≥ 1 (`rs_merkle`, fork `tlsnotary/rs-merkle`, rev `85f3e82`) |
| crates à chaîne C / build natif | 0 | `ring`, `cc`, `libc`, `windows-sys` |
| crate d'horloge dans le graphe | 0 | `web-time` |
| lock amont complet (référence de taille, comptage direct des blocs `[[package]]`) | — | 700 paquets, dont 29 git et 21 locaux |

Cinq motifs de rejet, chacun sur pièce :

1. **La forme α contredit ADR-0009 pt 6, elle ne le repositionne pas.** La
   crate qui porte `Presentation::verify` **est `std`** : `presentation.rs`
   ouvre par « use std::fmt; », et ses erreurs portent
   `Box<dyn std::error::Error + Send + Sync>`. `#![no_std]` n'est donc pas
   « déplaçable » : il devient **impossible** tant que l'amont n'a pas
   changé. L'amont vise bien les cibles contraintes — sa CI exécute un test
   dédié sous `getrandom_backend="unsupported"` — mais *sans syscall* n'est
   pas *`no_std`*, et la distinction est exactement celle qu'une gate
   mesure.
2. **S-G2 tomberait sur le fond, pas sur la lettre.** La gate porte
   « (arêtes, horloge, réseau) » ; la fermeture α importe `web-time`
   (horloge) et la pile `rustls-webpki`/`webpki-roots` (validation de
   chaînes de certificats). Le vérificateur cesserait d'être ce que son
   propre manifeste déclare : « Ne dépend que du cœur : ni réseau, ni
   horloge, ni adapter. »
3. **R-8 et la gate licences se retournent contre nous.** Contrôle registre
   fait : les crates `tlsn*` **n'existent pas sur crates.io** — l'épinglage
   serait git par révision. Et le manifeste de `tlsn-attestation` — la
   crate même qui porte la vérification — **ne porte aucun champ
   `license`** (là où `tlsn-core` porte `license = "MIT OR Apache-2.0"` et
   `tlsn-tls-core` `"Apache-2.0 OR ISC OR MIT"`), tandis que le dépôt
   n'expose aucun fichier `LICENSE` à sa racine et que l'API GitHub rend
   `license` nul. L'intention du projet est pourtant claire au README :
   « All crates in this repository are licensed under either of »
   Apache-2.0 ou MIT. Mais `cargo deny check licenses` lit le manifeste,
   pas le README : la forme α produirait un `error[unlicensed]` **sur une
   crate tierce**, que l'assouplissement d'ADR-0014 pt 2 **ne couvre pas**
   (son périmètre exact : « les seules crates `publish = false` du
   workspace »). Il faudrait donc une clause `clarify` — un affaiblissement
   de gate porté par ADR, pour un confort d'architecture. La charte
   `shogen-devops` §2 permet de le faire ; rien ici ne justifie de le
   faire.
4. **ADR-0012 D6 (rebuild bit-à-bit du vérificateur sous 6 variations)
   deviendrait un autre problème.** D6 a été restreint à un binaire
   précisément parce qu'il est à dépendances minimales par décision
   antérieure. Faire entrer `ring` + `cc` — une chaîne C invoquée au
   build — dans la cible même de D6, c'est déplacer la difficulté au pire
   endroit, à la passe qui doit la livrer.
5. **La couverture de plateforme de l'amont ne rencontre pas la nôtre.** Le
   workflow CI amont détenu porte **8 jobs, tous `runs-on: ubuntu-latest`,
   zéro Windows, zéro macOS** (comptage orchestrateur re-fait sur la
   copie) ; notre critère de clôture exige vert sur Windows **et** Linux
   (S2.5, run `31645277610`). La forme α ferait dépendre notre vert Windows
   d'un code que son auteur ne construit jamais sous Windows.

*(À retenir de cette instruction : la « frontière `no_std` repositionnée »
que 13 §2 présentait comme une **troisième** forme n'en est pas une. Elle
ne résout aucun des motifs 2 à 5 — la fermeture de dépendances, `web-time`,
l'absence de champ `license`, `ring`+`cc`, l'amont ubuntu-seul restent
identiques. Elle est la **pré-condition** de la forme α, pas son
alternative. La nommer comme une option distincte donnerait trois choix là
où il y en a deux.)*

#### (b) Reclaim (proxy-witness) comme transport de S3

Rejetée, sur quatre pièces détenues.

1. **Le résidu est strictement plus lourd, et il est décrit comme tel par
   Reclaim.** L'attestor **voit du clair** : « The attestor validates the
   claim by decrypting only the necessary data portions, verifying its
   integrity, and signing the claim. » Là où le notaire TLSNotary reste
   aveugle : « the Notary does not gain knowledge of either the plaintext
   or the identity of the server with which the Prover communicated. » Et
   la parade nommée par Reclaim contre la forge est un vœu d'architecture,
   pas un contrôle : « The only protection against fake proofs here is
   decentralisation or self-hosting of the attestor. » (déjà porté au
   registre comme A(attestor-honesty)).
2. **L'implémentation n'est pas dans notre langage.** `attestor-core` est
   une « implementation of the attestor server & the SDK to interact with
   it. » en TypeScript. La forme β (compagnon) exigerait un runtime Node
   dans l'artefact de confiance du projet : incompatible avec ADR-0009
   (Rust pour les trois rôles) et avec D6.
3. **La licence est AGPL-3.0** (« AGPL-3.0 license », README détenu).
   ADR-0014 pose que le vérificateur doit être « au régime le plus ouvert
   (c'est l'artefact de confiance) » ; brancher le premier transport sur
   une pièce AGPL préempterait, de fait, une décision qui appartient au
   mainteneur et dont l'échéance est cette passe même. On ne décide pas une
   licence par un choix de dépendance.
4. **Reclaim reste dans le corpus comme le second transport candidat** — sa
   qualité de contre-exemple est déjà employée. Le rejeter comme *premier*
   transport n'est pas le rejeter comme transport.

#### (c) Différer le transport réel (garder le témoignage trivial)

Rejetée **par défaut** — mais **retenue comme branche mécanique** au pt 5
de la décision. L'honnêteté de cette alternative est réelle : le squelette
S2.5 marche déjà de bout en bout et l'amont dit de lui-même qu'il « should
not be used in production. Expect bugs and regular major breaking
changes. »

Ce qui la fait perdre : S3 n'a pas d'autre objet. Différer le transport
laisserait la passe sans son critère, et le pont S2.5 → S3 sans son
tablier. Surtout, le motif d'alarme (l'état alpha) est exactement ce que la
forme β **absorbe** : le code alpha vit dans un compagnon jetable et
remplaçable, pas dans l'artefact de confiance du projet. Différer serait
payer le coût de l'alpha (pas de chemin réel) sans en prendre le bénéfice
(la chaîne montrée).

Ce qui la garde vivante : la mesure TLS 1.2 du pt 5. Si le pool ne parle
plus TLS 1.2, ce n'est plus un arbitrage — c'est un fait, et (c)
s'applique.

### La source qui tranche

**Pour A (le mode Notary) — le billet officiel du projet, « Zero-knowledge
≠ trustless » (2026-06-17, détenu).** Il énonce la ligne exacte que le
critère de S3 suppose : « A zkTLS proof isn't checked by the world. It's
checked by whoever trusts the verifier that witnessed it. » Il nomme le
rôle sans le mystifier : « A notary is just a verifier you didn't run
yourself. » Il refuse d'appeler *trustless* ce qui est portable : « You
don't get public verifiability and zero trust at the same time; you get
public verifiability because you accepted a notary. » Et il ferme la porte
au mode Verifier direct pour notre usage : le vérificateur participant
« has to be online during the session », or notre vérificateur est offline
par décision fondatrice (ADR-0003).

La FAQ courante donne la mécanique, mot pour mot : quand un vérificateur ne
peut pas être en session, « they may choose to delegate the verification of
the online phase of the protocol to an entity called the » Notary, qui
« produces an attestation trusted by the » Verifier, puis « in the offline
phase, the Verifier is able to ascertain data authenticity based on the
attestation. » — c'est la définition de la phase que `shogen verify <lot>`
occupe. Et elle énonce le résidu dans la graphie même du registre 08 : si
le vérificateur n'a pas conduit le MPC, « they must trust in the notary's
neutrality ».

La FAQ dit aussi « The protocol does not have trust assumptions. » Cette
phrase est retenue **avec son périmètre** : elle porte sur le protocole
entre Prover et Verifier participants, pas sur le tiers qui lit une
attestation — le billet du 2026-06-17 le corrige explicitement pour ce
tiers (« Anyone else has no way to rule out that collusion, so to them the
proof is only as good as their trust that the verifier played fair. »).
Deux pièces officielles, deux périmètres : la contradiction n'est
qu'apparente, et la citer sans son périmètre serait la surclamation que 09
interdit.

**Pour B (la délégation) — l'amont lui-même.** `presentation.rs` (épinglé
0fe3c32d) : « A presentation is self-contained and can be verified by a
Verifier without » accès à des données externes ; « The Verifier need only
check that the key » utilisée pour signer vient d'un notaire de confiance.
C'est exactement le périmètre d'un compagnon : une fonction pure sur un
fichier, sans réseau. Et la même crate, quelques lignes plus haut, dit
pourquoi elle ne peut pas entrer chez nous : « use std::fmt; ».

**Pour le pt 10 (COSE) — RFC 9052 et RFC 8949**, versées à cette phase
(INDEX §phase B) : « The COSE_Sign1 signature structure is used when only
one signature is » placée sur un message ; la structure taguée est
« identified by the CBOR tag 18. » Le slot est donc parfaitement défini, ce
qui permet de le déclarer *nommé et vide* en S3 sans ambiguïté. (Ces deux
RFC étaient jusqu'ici des références inter-projets non détenues côté Shōgen
— 08, note 2. La note reste ouverte pour le Lemme 8 OCR et RFC 5280 §3.3.)

**Pour le régime de la décision — le corpus doc 02.** R-8 (registre avant
installation) est ce qui a produit le contrôle crates.io ; G5 est ce qui
interdit de laisser « alpha » comme un dû nu : ici l'alpha est *contracté*
(A(upstream-alpha) au registre) et *confiné* (dans un compagnon), avec une
condition de réouverture écrite (pt 11) et une condition de bascule
mécanique (pt 5).

**Assurance de cette ADR** : *reviewed* (draft worker 2026-08-13 ;
adjudication orchestrateur sur pièces le même jour, requalification du
compte de fermeture consignée en note). Aucune mesure n'est ici *tested* :
la mesure TLS 1.2 du pt 5 et la conduite d'une session réelle sont dues en
phase C.

### Ce que la décision coûte

1. **Deux binaires au lieu d'un.** La promesse d'un binaire unique qui
   recalcule tout offline devient : un binaire qui recalcule la chaîne,
   plus un compagnon nommé qui vérifie la preuve du transport.
   A(verifier-binary) et le double-build D6 gardent leur cible sur
   `shogen-verifier` seul (comme ADR-0012 le restreint), donc **le
   compagnon n'est pas bit-à-bit reproductible en S3** — et cela se dit,
   plutôt que de s'omettre.
2. **Un résidu de plus dans le verdict, et il est de notre fait.**
   A(transport-check-delegated) n'existerait pas dans la forme α. C'est le
   prix franc de la délégation : nous échangeons une fermeture de plus de
   cent crates contre une phrase de verdict plus longue. Le vocabulaire 09
   accueille la formulation fautive correspondante ("transport vérifié par
   shogen-verifier").
3. **Le verdict de S3 est démonstratif, pas probant.** Avec un notaire
   opéré par Shōgen, « valide sous A(notary-neutrality) » est littéralement
   vrai et pratiquement creux : le tiers qui lit devrait nous croire. Aucun
   montage disponible ne fait mieux à cette date — le service public est
   arrêté, le binaire notaire est retiré de l'amont. **A(self-attestation)
   est la dette contractée**, décharge nommée : un notaire tiers, ou un
   quorum de notaires. Rien de public-facing ne peut s'appuyer sur le
   verdict de S3.
4. **Le coût opératoire de MPC-TLS est réel et chiffré par l'amont.**
   Surcoût d'upload du prouveur : « ~25MB (a fixed cost per one TLSNotary
   session) + ~10 MB per every 1KB of outgoing data + ~40KB per every 1 KB
   of incoming data. » ; « our MPC-TLS protocol involves ~40 communication
   rounds » ; et, sur la machine de référence de l'amont, « the native
   build completes in ~5 s » pour une réponse d'environ 10 KB (billet
   benchmarks d'août 2025, détenu). Un témoignage n'est donc pas gratuit,
   et la fenêtre de fraîcheur de S4 devra vivre avec cet ordre de grandeur.
   *(Ces chiffres datent d'août 2025 et décrivent des alphas antérieures ;
   ils bornent l'ordre de grandeur, ils ne mesurent pas notre montage.)*
5. **La rupture de format amont est probable, pas seulement possible.**
   « Expect bugs and regular major breaking changes. » — le format de
   `Presentation` peut changer d'une alpha à l'autre, et un
   `transport_proof` archivé peut cesser d'être vérifiable par le compagnon
   courant. Conséquence à porter : la révision amont exacte devient une
   donnée du témoignage ou du lot, pas un détail de build. *(Sous-décision
   à instruire, pas tranchée ici : où elle est portée — champ du lot, ou
   registre de versions du compagnon.)*
6. **Une divergence documentaire nous suit.** Sur TLS 1.3, deux pages
   officielles se contredisent (« Support for TLS 1.3 is on the
   roadmap. » vs « There are no immediate plans to support TLS 1.3. »), et
   le Rust Quick Start renvoie encore à `--branch v0.1.0-alpha.14` alors
   qu'alpha.15 est publiée (2026-05-21). La doc amont n'est pas versionnée
   (Docusaurus « current »). Nos citations restent donc datées à la copie
   détenue, jamais à « la doc ».
7. **La sous-décision `subject` reste ouverte.** ADR-0002 la laisse
   explicitement non réglée, et un témoignage réel ne peut plus la
   différer : c'est ADR-0016, pas cette ADR. Nommée ici pour qu'elle ne se
   perde pas dans l'ombre de 0015.

### Registres touchés

- **`docs/08-assumptions.md`** — trois entrées nouvelles (portées à
  l'adjudication) : A(self-attestation) (résidus de transport),
  A(transport-check-delegated) et A(upstream-alpha) (résidus de couche).
- **`docs/09-vocabulaire.md`** — trois entrées nouvelles (adjugées depuis
  les candidates du draft).
- **`docs/03-temoignage.md`** — §2 : la ligne `tlsn-mpc` gagne
  A(self-attestation) à côté d'A(notary-neutrality) pour la durée de S3 ;
  §4 point (1) : la forme de la délégation y est fixée par cette ADR.
- **`docs/13-temoignage-e2e-design.md`** §2 — la tension d'intégration est
  close : forme β retenue, la « frontière repositionnée » requalifiée en
  pré-condition de α. §3 item 3 (`no_std` en gate) : confirmé dû, non
  repositionné.
- **`Cargo.toml` (workspace)** — `shogen-tlsn-verify` n'entre **pas** dans
  `members` : comme `adapters/`, il vit hors workspace pour que la
  fermeture contrôlée par S-G2/S-G7a reste celle du cœur et du
  vérificateur.
- **`deny.toml`** — **inchangé**. C'est un résultat de la forme β, pas un
  effet secondaire : la forme α aurait exigé une clause `clarify` pour
  `tlsn-attestation`.
- **`WISHLIST.md`** — les manques nommés par le draft y sont portés
  (§S3) : papier QuickSilver (identité à confirmer avant citation),
  analyse de sécurité arbitrée du protocole courant, pages `/docs/mpc/*`,
  README des exemples `basic`/`proxy`, source du test amont
  `no_syscall_verify` ; la taille d'un artefact `Presentation` se résout
  par MESURE en phase C (pas un procurement).
- **`biblio/INDEX.md`** — les deux RFC versées pendant la rédaction sont
  inscrites (§phase B, 5/5 sha256 concordants).

---

## ADR-0016 — La canonicalisation de `subject` : forme construite, prédicat au vérificateur, aucun tri de requête

**Statut** : acceptée (adjugée par l'orchestrateur sur pièces le 2026-08-13
— révision mainteneur ouverte) · 2026-08-13

> **Note d'adjudication (2026-08-13).** Draft de worker (`claude-opus-5`,
> run `wf_8db62dce-162`), livré avec sa propre table de contrôle
> une-citation-un-grep (58 fragments, comptes d'occurrences portés).
> Adjudication : échantillon adversarial de 10 fragments re-greppé par
> l'orchestrateur (10/10 trouvés à l'artefact annoncé, dont l'ABNF en
> chaîne fixe et l'apostrophe en entité HTML de C2PA §8.4.2.2) ; les trois
> réserves du worker levées une à une — la déduction de grammaire sur
> l'endpoint Pyth **re-contrôlée et confirmée** (10 §3.1 ligne 11 : la
> graphie réelle porte `ids[]=`, et les crochets sont absents de l'ABNF
> `query`/`pchar` citée) ; enfin S-G5 contrôle mécaniquement chaque
> citation de ce texte à chaque `verify`. **Deux mises à jour d'état** :
> les workers ayant tourné en parallèle, le draft croyait RFC 8949 et
> RFC 9052 non détenues — elles ont été versées par le draft ADR-0015 le
> même soir (INDEX §phase B) ; son « manque 4 » est donc résolu et ne
> figure plus ci-dessous. Les trois pièces acquises par ce draft
> (RFC 3986, RFC 9110, WHATWG URL) sont versées et contrôlées : provenance
> re-téléchargée à octets identiques par le worker, sha256 recalculés par
> l'orchestrateur (5/5 de la phase, INDEX §phase B).

### Contexte

ADR-0002 a tranché le conteneur et a laissé, à la lettre, une
sous-décision ouverte : « La canonicalisation de `subject` (URL + requête
normalisées) est une sous-décision séparée, ouverte, qui n'est pas réglée
par le choix du conteneur. » `03-temoignage.md` §5, item 1, porte la même
mention. Elle a pu rester ouverte tant que le témoignage était trivial :
le squelette S2.5 encode trois champs factices dont aucun n'est une URL.

S3 la ferme par force. Le motif est celui d'ADR-0002 lui-même — deux
encodeurs honnêtes doivent produire les mêmes octets — transposé d'un cran
plus bas : si deux graphies d'une même requête produisent deux `subject`,
alors le hash du témoignage dépend de la **graphie**, et deux témoignages
du même dire deviennent incomparables. Le critère de S3 exige un
`shogen verify <lot>` sur un témoignage **réel** ; un témoignage réel
désigne un endpoint réel, avec scheme, hôte, chemin et — pour une partie
des endpoints du pool S2 (10 §3.1) — une chaîne de requête.

Trois faits du dépôt bornent la rédaction et ne sont pas rouverts :
**ADR-0003** (recalculable offline : ce que le vérificateur ne peut pas
faire hors réseau n'entre pas dans la forme canonique) ; **ADR-0009 pt 6
et ADR-0012 D3** (dépendances minimales, `no_std` visé, épinglage exact —
toute canonicalisation qui exige une table Unicode ou un résolveur est un
coût de graphe) ; **ADR-0010 et la posture déjà codée** — le décodeur du
cœur est strict par décision : `temoignage.rs` écrit qu'un encodage valide
mais non canonique est « refusé, pas normalisé ». La question n'est donc
pas seulement *quelles normalisations* mais **où elles ont lieu**.

Enfin, `subject` n'est pas le porteur d'intégrité du témoignage :
ADR-0005 règle 1 — le « hash des octets exacts est toujours porté ». Une
erreur de désignation ne peut pas faire passer un dire faux ; elle peut
faire croire que deux dires portent sur la même chose, ou l'inverse. C'est
exactement le mode d'erreur que RFC 3986 §6 traite.

### Décision

#### C0 — Le principe : la forme canonique est **construite**, jamais réécrite après coup

`subject` est **la requête effectivement émise, octet pour octet, dans sa
forme canonique**. La normalisation a lieu **une fois, à la construction,
dans l'adapter** (la coquille impérative d'ADR-0010) — le seul rang à
savoir ce qui a été interrogé — et l'adapter émet ensuite exactement les
octets qu'il a inscrits dans `subject`. Le cœur et le vérificateur ne
normalisent **rien** : ils évaluent un **prédicat de canonicité** total
sur des octets, et un `subject` hors forme est un **refus nommé**, jamais
une réécriture silencieuse.

C'est la posture déjà codée pour le CBOR, étendue au champ. Sa conséquence
décide de tout le reste : un vérificateur qui **refuse** n'a besoin d'être
cru que sur son refus ; un vérificateur qui **normalise** devrait être cru
pour normaliser exactement comme le producteur — deux implémentations, une
égalité à établir, hors réseau, des années plus tard.

Au rang du vérificateur, la comparaison de deux `subject` redevient la
moins chère de l'échelle de RFC 3986 §6.2.1 — « If two URIs, when
considered as character strings, are identical, then it is safe to
conclude that they are equivalent » — parce que le coût de normalisation a
été payé une fois, en amont. La RFC nomme cette discipline comme la voie
de réduction des alias : « Unnecessary aliases can be reduced, regardless
of the comparison method, by consistently providing URI references in an
already-normalized form ».

#### C1 — Grammaire de la forme canonique (S3)

Le `subject` canonique est une **chaîne d'octets US-ASCII**, encodée en
texte CBOR (ADR-0002), de la forme :

```
subject = "https://" host [ ":" port ] path [ "?" query ]
```

et satisfaisant C2 à C9. Tout octet ≥ 0x80 est **refusé** (`OctetNonAscii`)
— un caractère hors US-ASCII doit déjà être percent-encodé au moment où le
`subject` existe (RFC 3986 §2.4 : « Once produced, a URI is always in its
percent-encoded form. »).

#### C2 — Scheme : `https` uniquement, en minuscules

Le scheme est la chaîne littérale `https`. Casse : RFC 3986 §3.1 —
« Although schemes are case-insensitive, the canonical form is
lowercase ». Restriction à `https` : elle **n'est pas** un jugement de
sécurité, c'est une conséquence de transport — le transport d'ADR-0015
atteste une session TLS ; un `subject` en `http` désignerait une
interrogation que le transport ne peut pas attester. RFC 9110 §4.2.2 pose
en outre que « Resources made available via the "https" scheme have no
shared identity with the "http" scheme. » — aucune normalisation ne peut
passer de l'un à l'autre. *Si un transport futur atteste du trafic
non-TLS, cette clause se rouvre par ADR ; pas autrement.*

#### C3 — Hôte : nom enregistré ASCII en minuscules ; ni IDN, ni littéral d'adresse

L'hôte est un **nom enregistré** en lettres ASCII minuscules, chiffres,
`-` et `.`. Une majuscule est normalisée à la construction et **refusée**
au prédicat (`HoteMajuscule`) — RFC 3986 §6.2.2.1 : « scheme and host are
case-insensitive and therefore should be normalized to lowercase ». Un
octet percent-encodé dans l'hôte est refusé (`HotePercentEncode`). Un
littéral d'adresse est refusé (`HoteLitteralAdresse`) : RFC 3986 §3.2.2
réserve les crochets au seul littéral IP — « This is the only place where
square bracket characters are allowed in the URI syntax. » — et §7.4
documente que l'interprétation des formes pointées dépend de la
plateforme (« many implementations allow dotted forms of three numbers,
wherein the last part is interpreted as a 16-bit quantity ») : une
désignation dont l'interprétation dépend de la plateforme du lecteur
n'est pas recalculable offline (ADR-0003). Un hôte non-ASCII (IDN) est
**refusé** (`HoteNonAscii`), pas converti en Punycode : la conversion
exige une table Unicode versionnée (alternative A1) que le vérificateur
`no_std` à dépendances minimales ne porte pas. Le refus est nommé et
chiffré au §Coûts.

#### C4 — Aucun `userinfo`

Un `@` séparant un `userinfo` de l'hôte est **refusé**
(`UserinfoPresent`). RFC 9110 §4.2.4 : « A sender MUST NOT generate the
userinfo subcomponent (and its "@" delimiter) when an "http" or "https"
URI reference is generated within a message as a target URI or field
value. » RFC 3986 §7.6 documente l'attaque sémantique que ce
sous-composant permet ; un `subject` porteur d'identifiant serait en
outre une fuite au sens de §7.5.

#### C5 — Port : omis quand il est le port par défaut du scheme

Le port est **absent** quand il vaut 443 ; présent, il est décimal sans
zéro de tête et différent de 443 (`PortParDefautExplicite`,
`PortNonDecimal`). RFC 3986 §3.2.3 : « URI producers and normalizers
should omit the port component and its ":" delimiter if port is empty or
if its value would be the same as that of the scheme's default » ; la
valeur du défaut vient du scheme — RFC 9110 §4.2.2 : « TCP port 443 (the
reserved port for HTTP over TLS) is the default. » ; §4.2.3 : « If the
port is equal to the default port for a scheme, the normal form is to
omit the port subcomponent. »

#### C6 — Chemin : jamais vide, sans segment pointillé

Un chemin vide est écrit `/` à la construction ; le prédicat refuse le
chemin vide (`CheminVide`) — RFC 9110 §4.2.3 : hors OPTIONS, « an empty
path component is equivalent to an absolute path of "/" ». Un segment `.`
ou `..` est **refusé** (`SegmentPointille`), graphies percent-encodées
comprises (contrôle après C7).

Sur ce point, la décision **s'écarte volontairement d'un « should » de la
source et le dit**. RFC 3986 §6.2.2.3 recommande de retirer : « URI
normalizers should remove dot-segments by applying the
remove_dot_segments algorithm to the path ». Nous **refusons** au lieu de
retirer : (a) retirer, c'est réécrire — C0 l'exclut au vérificateur, et
l'algorithme entrerait dans le binaire `no_std` ; (b) le refus produit la
même classe d'équivalence, amputée d'un alias qu'aucun endpoint du pool
n'emploie ; (c) c'est le geste du seul précédent structurel détenu — C2PA
2.4 §8.4.2.1 : « URIs shall not contain the sequence .. (a pair of
U+002E, Full Stop). » Le même appareil de manifeste signé **interdit** au
lieu de normaliser. Que les graphies encodées soient le même segment est
documenté par la pièce WHATWG détenue : le *double-dot URL path segment*
est « ".." or an ASCII case-insensitive match for ".%2e", "%2e.", or
"%2e%2e" ».

#### C7 — Percent-encoding : casse haute, triplets inutiles décodés, réservés intouchés

1. Chiffres hexadécimaux des triplets en **majuscules**
   (`TripletPercentMinuscule`) — RFC 3986 §2.1 : « For consistency, URI
   producers and normalizers should use uppercase hexadecimal digits for
   all percent-encodings. »
2. Un triplet codant un caractère **non réservé** est décodé à la
   construction et **refusé** au prédicat (`PercentEncodageInutile`) —
   RFC 3986 §2.3 : « URIs that differ in the replacement of an unreserved
   character with its corresponding percent-encoded US-ASCII octet are
   equivalent » ; RFC 9110 §4.2.3 en fait la forme normale http(s).
3. Tout `%` ouvre un triplet bien formé (`TripletPercentMalForme`) ;
   `%00` est **refusé** (`OctetNulEncode`) — RFC 3986 §7.3 : le NUL
   « should be rejected » hors donnée brute attendue.

**L'interdiction** : un caractère **réservé** n'est ni encodé ni décodé,
jamais, à aucun rang — RFC 3986 §2.2 : « URIs that differ in the
replacement of a reserved character with its corresponding percent-encoded
octet are not equivalent. » C'est la clause qui interdit à elle seule
toute « harmonisation » de séparateurs dans la requête. Et l'idempotence —
§2.4 : les implémentations « must not percent-encode or decode the same
string more than once » — interdit d'appliquer la normalisation deux
fois : elle a lieu une fois, à la construction (C0) ; le prédicat ne
transforme rien.

#### C8 — Requête : conservée **verbatim**, jamais triée, jamais dédupliquée

- Absente, ou présente et **non vide** — le `?` nu est refusé
  (`RequeteVide`) : RFC 3986 §6.2.3, « Normalization should not remove
  delimiters when their associated component is empty unless licensed to
  do so by the scheme specification. » — et le scheme http(s) ne donne pas
  cette licence (RFC 9110 §4.2.3 énumère ses règles, aucune sur la
  requête).
- La requête conforme à l'ABNF `query` de RFC 3986 §3.4 est reprise
  **octet pour octet**, dans l'ordre émis. **Aucun tri. Aucune
  déduplication. Aucune fusion de clés répétées. Aucune réécriture
  `+`/espace.** Seules les règles de C7 s'y appliquent (elles portent sur
  les octets, pas sur la structure clé/valeur).
- Un caractère hors grammaire — au premier chef `[` et `]` — est refusé
  (`CaractereHorsGrammaire`).

**Le tri des paramètres, instruit honnêtement** — c'est la normalisation
la plus tentante et celle que nous refusons :

1. **Aucun barreau de l'échelle ne la licencie.** RFC 3986 §6.2.2 énumère
   « case normalization, percent-encoding normalization, and removal of
   dot-segments » — trois techniques, pas de réordonnancement ; §6.2.3
   renvoie au scheme, et RFC 9110 §4.2.3 n'ajoute rien sur la requête ;
   §6.2.4 (protocol-based) est le geste des spiders, refusé en R2.
2. **La requête appartient à l'origine, pas à nous.** RFC 3986 §3.4 :
   « The query component contains non-hierarchical data » qui sert
   l'identification « within the scope of the URI's scheme and naming
   authority ». Réordonner, c'est affirmer une propriété du parseur de
   l'origine — que nous ne détenons pour aucune source du pool.
3. **L'asymétrie de RFC 3986 §6.1 tranche** : « comparison methods are
   designed to minimize false negatives while strictly avoiding false
   positives. » Le tri achète une réduction de faux négatifs au prix d'un
   faux positif possible — deux ressources distinctes sous un seul
   `subject`, le mode d'échec qu'aucun résidu nommé ne rattrape.
4. **Le tri ne ferme même pas l'alias qu'il promet.** Le seul tri normatif
   détenu (WHATWG, `URLSearchParams.sort()`) ordonne par **nom
   seulement** ; deux requêtes aux valeurs permutées restent distinctes.
   Et son motif déclaré n'est pas l'identité : « It can be useful to sort
   the name-value tuples in a URLSearchParams object, in particular to
   increase cache hits ».
5. **`+` n'est pas un espace au rang de l'URI.** `+` est un `sub-delim`,
   réservé, protégé par §2.2 ; l'équivalence `+`/espace appartient au
   format `application/x-www-form-urlencoded` (WHATWG : « Replace any
   0x2B (+) in name and value with 0x20 (SP) ») — appliquer une règle de
   format à une désignation d'URI serait le faux positif du point 3.

#### C9 — Aucun fragment

Un `#` est **refusé** (`FragmentPresent`). RFC 3986 §6.1 : pour
sélectionner une action réseau, les fragments « should be excluded from
the comparison » ; et §6.2.3 : « The fragment component is not subject to
any scheme-based normalization ». Un composant jamais émis vers l'origine
et non normalisable n'a pas de place dans la désignation de ce qui a été
interrogé.

#### C10 — Le prédicat vit au cœur ; le vérificateur ne fait que refuser

`shogen-core` porte une fonction **totale**
`subject_est_canonique(&[u8]) -> Result<(), ErreurSubject>` : sans I/O,
sans horloge, au régime d'ADR-0010, variantes d'erreur **nommées et
positionnées** au patron d'`ErreurDecodage`. Le vérificateur l'appelle et
propage : verdict fail-closed, raison structurée. Ce que l'adapter utilise
pour **construire** n'est pas tranché ici — il est dans la coquille, hors
périmètre `no_std`, sous une seule contrainte : ce qu'il produit satisfait
le prédicat du cœur, et son outillage éventuel passe R-8. Un désaccord
constructeur/prédicat est un **rouge** — deux implémentations qui se
contrôlent l'une l'autre.

#### Les refus explicites — ce que la canonicalisation ne fait pas

**R1 — Aucune résolution de noms.** RFC 3986 §3.2.2 : la présence d'un
hôte « does not imply that the scheme requires access to the given host on
the Internet », et la conformité du nom est déléguée à l'environnement —
la spec « delegates the issue of registered name syntax conformance to
the » système du lecteur : une forme dont le résultat dépend du système ne
serait pas recalculable (ADR-0003).

**R2 — Aucun suivi de redirection.** Le `subject` désigne **ce qui a été
interrogé**, jamais ce vers quoi l'origine a renvoyé — la normalisation
« protocol-based » de §6.2.4 est un geste de spider en ligne, non
rejouable hors ligne, et le vérificateur n'a pas de réseau (S-G2).

**R3 — Aucune revendication d'identité de ressource.** RFC 3986 §6.1 :
« URI comparison is not sufficient to determine whether two URIs identify
different resources. » Le vocabulaire de sortie le dit (§Registres).

**R4 — Aucune promesse de persistance.** RFC 3986 §7.1 : « There is no
guarantee that once a URI has been used to retrieve information, the same
information will be retrievable by that URI in the future. » Ce résidu est
déjà porté par `observed_at` (03 §1) ; aucune entrée nouvelle.

**R5 — Hors périmètre : les requêtes qu'aucune URI ne désigne.** La forme
couvre une interrogation **http(s) sans corps**. La source #12 du pool
(`eth_call` RPC) inclut un corps de requête qu'aucune URI ne porte : hors
périmètre de `subject` tel que décidé ; l'admettre exigera une ADR, due au
premier branchement d'une telle source.

**Régime d'assurance** : rien ici n'est *proven*. Le prédicat sera
*tested* en phase C (property-based + mutants, comptes à la date) ; d'ici
là, l'assurance est *reviewed* (draft worker, adjudication orchestrateur,
2026-08-13).

### Alternative considérée

**A1 — Le WHATWG URL Standard comme référence normative.** Instruite
sérieusement (c'est la spec des clients réels, détenue). Rejetée sur trois
constats de copie : (1) cible mouvante sans version — « Last Updated 6
July 2026 », aucune identité que « courant », le mode d'échec déjà
rencontré avec la doc TLSNotary ; (2) son but déclaré est de remplacer la
source, pas de la préciser — Goals : « Align RFC 3986 and RFC 3987 with
contemporary implementations and obsolete the RFCs in the process. » ;
(3) sa normalisation d'hôte importe une table Unicode versionnée (UTS #46,
« and not IDNA2008 », écarts « due to web compatibility ») — contre
ADR-0009 pt 6 et ADR-0012 D3, et un verdict dépendant du millésime de la
table. **Retenue comme pièce de corroboration** : graphies du segment
pointillé (C6), portée réelle du tri (C8 pt 4), localisation de
`+`/espace dans un format (C8 pt 5).

**A2 — Ne rien normaliser.** Rejetée comme décision, **retenue à
moitié** : c'est ce que fait le vérificateur (C0). Seule, elle ne ferme
pas ADR-0002 : sans discipline de construction, deux graphies restent deux
hashes — la RFC nomme la solution retenue (« in an already-normalized
form »), pas l'abstention.

**A3 — Toute l'échelle dans le vérificateur.** Rejetée : elle fait entrer
`remove_dot_segments`, le décodage percent et le pliage de casse dans un
binaire `no_std`, et surtout elle fait **réécrire au vérificateur ce qu'il
contrôle** — la posture que le cœur refuse déjà pour le CBOR.

**A4 — Trier les paramètres.** Rejetée, instruite en C8 points 1-5. La
seule alternative dont le rejet coûte quelque chose de mesurable, écrit au
§Coûts.

**A5 — Déléguer à une crate d'URL de l'écosystème.** Rejetée pour le
périmètre cœur/vérificateur : elle importe la sémantique d'A1 et ses
tables IDNA dans le graphe, contre ADR-0012 D3. R-8 non instruit car sans
objet ici ; il redevient dû si l'adapter (coquille) veut une telle crate
pour **construire** — ce que C10 laisse ouvert.

**A6 — Admettre le jeu de caractères de requête du WHATWG (`[`/`]`
bruts).** Instruite parce qu'immédiatement utile (source #11 du pool).
Rejetée à S3 : c'est A1 par la petite porte, pour un gain d'une source
quand le critère porte sur UN témoignage et que le pool en offre d'autres
en grammaire. Première option à instruire si une classe de faits l'exige.

### La source qui tranche

**RFC 3986 §6 « Normalization and Comparison » (détenue, lue §6.1-§6.2.4
par le worker, échantillon re-greppé par l'orchestrateur).** Elle seule
fait deux choses ensemble : elle **énumère** les normalisations licites et
elle **donne la règle de choix** — §6.1 : « comparison methods are
designed to minimize false negatives while strictly avoiding false
positives. » Cette asymétrie décide de tout le sous-ensemble : toutes les
normalisations que la source déclare préserver l'équivalence, **aucune**
de celles qu'elle ne licencie pas. Le geste est celui d'ADR-0008 : ne pas
prendre le déclaré pour du mesuré.

**RFC 9110 §4.2.3 (détenue)** est la seconde, indispensable : §6.2.3 de la
3986 renvoie au scheme, et l'énumération close de 9110 (port, chemin vide,
casse, non-réservés — rien sur la requête) fait du tri une invention et
non une normalisation. Elle porte aussi la clause qui **nomme le résidu** :
« distinct resources SHOULD NOT be identified by HTTP URIs that are
equivalent after normalization » — un SHOULD NOT adressé aux **origines**,
que rien ne nous permet de contrôler : d'où l'entrée
A(origin-normalization-conformance) au registre.

**Le précédent structurel : C2PA 2.4 §8.4 (détenu).** Le cousin le plus
proche fait trois choses reprises telles quelles : il **interdit au lieu
de normaliser** (« URIs shall not contain the sequence .. ») ; il **refuse
fail-closed sur l'ambiguïté** (« a validator shall treat the reference as
unresolved ») ; et il **ne fait jamais porter l'intégrité par l'URI**
(toute référence est URL **plus** hash). Ce dernier point borne l'enjeu de
cette ADR : chez nous aussi l'intégrité est portée par le hash des octets
(ADR-0005 règle 1) — une canonicalisation défaillante ne fait pas passer
un dire faux, elle apparie mal. Mode d'échec de **comptage** (quorum, S4),
pas d'authenticité.

### Ce que la décision coûte

- **Une source du pool sort du périmètre à sa graphie actuelle.**
  L'endpoint Pyth (10 §3.1, ligne 11) s'écrit avec `ids[]=` — crochets
  hors de l'ABNF `query`/`pchar` de RFC 3986 §3.4, réservés par §3.2.2 au
  littéral IP. Le prédicat refuse (`CaractereHorsGrammaire`). Réécrire en
  `ids%5B%5D=` n'est **pas** une normalisation (§2.2 : substituer un
  réservé n'est pas une équivalence) mais une requête différente, dont
  l'acceptation par l'origine est une question empirique non tranchée.
  **Conséquence assumée** : le témoignage réel de S3 se fait sur une des
  autres sources en grammaire ; l'admission de Pyth est une décision
  ultérieure (A6), pas un contournement.
- **Les sources IDN sont hors périmètre** (C3). Aucun endpoint du pool
  n'en porte : coût nul aujourd'hui, entier demain — la première source
  IDN exigera une ADR **et** des pièces non détenues (§Manques).
- **Deux graphies de requête = deux `subject` = deux hashes** (C8). Le
  prix explicite du refus de trier, payé à la construction où il est
  visible : la graphie d'un endpoint est fixée au registre du pool
  (10 §3.1) ; un changement de graphie est un changement de `subject` —
  constatable, jamais silencieux.
- **Le prédicat est un contrôleur, pas un normaliseur d'URI général** — et
  ne doit jamais être décrit comme tel (ni IDN, ni littéraux, ni schemes
  autres que `https`, ni corps de requête). Deux entrées de vocabulaire en
  découlent.
- **Nous nous écartons de deux « should » de la source, et nous le
  publions** : §6.2.2.3 (retirer les segments pointillés — nous refusons)
  et §6.2.2 (décoder les non-réservés — fait à la construction, refusé au
  contrôle). Les deux écarts sont *plus stricts*, jamais plus permissifs :
  des faux négatifs, jamais des faux positifs — le sens même de §6.1.
- **Un refus est un blocage opérateur** — l'effet recherché (fail-closed),
  et un travail non planifié à chaque source nouvelle, borné par le refus
  nommé et positionné (C10).
- **Aucune mesure ne chiffre le risque évité.** Aucune pièce détenue ne
  mesure la proportion d'origines sensibles à l'ordre des paramètres :
  l'argument de C8 est **normatif**, pas empirique, et il est écrit comme
  tel. Sans acquisition (§Manques), aucune phrase sortante ne chiffre ce
  risque.

### Registres touchés

- **ADR-0002** : la sous-décision ouverte est **fermée par la présente
  ADR** (note portée à la table des ADR ; le texte d'ADR-0002 reste
  historique).
- **`docs/03-temoignage.md` §1** : la ligne `subject` est précisée —
  paramètres de requête **conservés verbatim**, jamais normalisés en
  ordre (la rédaction antérieure laissait croire l'inverse). §5 item 1 :
  fermé — les quatre items du §5 sont tous clos.
- **`docs/08-assumptions.md`** : entrée nouvelle
  A(origin-normalization-conformance) (résidus de couche), portée à
  l'adjudication.
- **`docs/09-vocabulaire.md`** : deux entrées nouvelles (adjugées).
- **`crates/shogen-core`** : `ErreurSubject` (variantes nommées C2-C9) et
  le prédicat total — phase C ; `subject` entre au vocabulaire du
  témoignage avec les 7 champs de 03 §1 — phase C.
- **`docs/13-temoignage-e2e-design.md` §2** : le point 2 (« le cœur »)
  gagne le prédicat de canonicité comme charge utile de phase C.
- **`biblio/INDEX.md`** : les trois pièces du draft sont versées et
  enregistrées (§phase B).
- **`WISHLIST.md`** : manques 1-3 ci-dessous portés.

### Manques nommés

1. **RFC 5890/5891 (IDNA2008) et UTS #46** — requis seulement si une
   classe de faits admet une source IDN (C3). Localisation connue
   (rfc-editor.org ; unicode.org/reports/tr46/, la copie WHATWG référence
   la révision tr46-35 du 4 septembre 2025).
2. **RFC 5952 (représentation textuelle IPv6)** — requise seulement si un
   littéral d'adresse est un jour admis (C3).
3. **Une mesure de la sensibilité des origines à l'ordre des paramètres**
   — aucune pièce détenue, aucune candidate identifiée ; elle ne
   changerait pas C8 (fondée normativement) mais permettrait de chiffrer
   le risque évité, aujourd'hui qualitatif.

---
