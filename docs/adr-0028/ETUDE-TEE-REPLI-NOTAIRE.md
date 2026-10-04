# RAPPORT TEE : enclaves pour le notaire de repli de Shōgen, coûts compris (centralisés et décentralisés)

> *Note de versement de l'orchestrateur (2026-10-04)* : étude versée telle que rendue, à une retouche typographique près : les citations anglaises de pages web **non versées à `biblio/`** (lues le 2026-10-04, copies hors dépôt) que la gate S-G5 signalait sont passées de « … » à “…” ; lectures [lu] web, à verser avant tout usage normatif (item SHOGEN-G4-BIBLIO-1).


Question de l'investisseur (verbatim, brief) : « combien la solution de repli va nous couter, et pourquoi chez AWS? l enclave. étudiez d'autres vendors, méme les décentralisés comme phala. »

---

## 0. Gate 0 et déclarations de méthode

- **Gate 0** : modèle résolu `claude-sonnet-5-5` (annoncé par le harnais ; effort `high` annoncé par la fiche, non observable depuis la session : déclaré, pas constaté).
- **Date** : `date -u` = 2026-10-04 03:14 UTC au début ; toutes les lectures ci-dessous sont du **2026-10-04** (03:14 à 03:35 UTC).
- **Brief** : `tee/BRIEF-TEE.md`, sha256 recalculé `5910f7aa…0d37b`, conforme à l'annonce.
- **Aucune installation, aucun achat, aucun compte, aucun fichier suivi modifié, aucune opération git.** Écriture uniquement sous `scratchpad/tee/` (rapport, `web/`, `get.sh`, `totxt.py`, `awsx.py`, `awsy.py`, `azq.py`, `cost.py`).
- **Exposition (pré-enregistrement, ADR-0028 annexe D)** : aucune pièce de `docs/15-*`, `docs/16-*`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, aucun `*.jsonl`, aucune pièce de la liste D.2 ouverts. Deux incidents mineurs à déclarer : (1) `ls docs/adr-0028/` a imprimé les **noms** de fichiers du répertoire (dont `monark-m009a` et `ANNEXE-D-preenregistrement.md`), aucun n'a été ouvert ; (2) l'impression de `docs/17-modele-de-menace.md` l. 55-70 (tronquée par l'outil) contient des chaînes de chemins `F:/Monark@…` dans les cellules T-01 ; ce sont des chaînes de texte du tableau, pas une ouverture de `monark-m009a/`.
- **Pièces du dépôt lues** (autorisées par le brief) : `docs/adr-0028/AVIS-G4-NOTAIRE.md` (entier), `docs/adr-0028/RECHERCHE-G4-NOTAIRE.md` (entier), `docs/17-modele-de-menace.md` (seuls les ≈ 2 premiers Ko de l'impression de l. 55-70, ligne T-01 ; le reste cité d'après G4 et l'AVIS, non relu), `docs/08-assumptions.md` (recherches ciblées : l. 17 et l. 60-65 ; le reste cité d'après G4 et l'AVIS), `adapters/shogen-tlsn-verify/{Cargo.toml (recherche de la ligne `rev`), MESURE-R8.md (recherche ciblée), session/src/main.rs l. 1-40 et recherche ciblée, fixtures/ (tailles de fichiers)}`.
- **Accès web** : `curl -sSL` par le proxy de la session, sans contournement. Un moteur de recherche (Bing par `curl`) a répondu mais avec des résultats hors sujet : **non exploité**, toute la recherche est donc par URL directe, **non exhaustive par construction**. `github.com` et `api.github.com` : 403 (non contourné) ; `raw.githubusercontent.com` : accessible, utilisé pour les sources de dépôts.
- **Étiquettes** : [lu] lu sur place (source + date) ; [abs] absent de la source lue ou source illisible ; [2nd] seconde main ; [inféré] déduction du lecteur, à ne pas citer comme fait. Les copies sont dans `tee/web/` ; condensats en §9.
- **Constat de reproductibilité** : cinq pages relues aujourd'hui sont **octet pour octet identiques** aux copies du lecteur G4 (condensats `RECHERCHE-G4` §7) : `teefail`, `wiretap`, `batteringram`, billets TLSNotary 2026-05-10 et 2026-06-23, page AWS « verify-root ». Les pièces d'attaques n'ont donc pas bougé entre les deux lectures. **DDRop (CCS '26, septembre 2026) est en revanche absent de RECHERCHE-G4**, qui ne cite que TEE.fail, WireTap et Battering RAM (la page Battering RAM, identique, porte pourtant le bandeau DDRop) : voir §4.3.

---

## 1. Résumé pour l'investisseur

**Combien coûte le repli ?** Le repli retenu par la recherche G4 est un **notaire en enclave AWS Nitro, opéré par Shōgen** (RECHERCHE-G4 §3.2, l. 194-196). Au prix de liste AWS lu aujourd'hui :
- **Pilote** (quelques sessions par heure, hypothèse 4/h) : **≈ 154 $/mois (≈ 137 €)** pour une instance `c6i.xlarge` à Paris, 24 h/24, avec disque et adresse IPv4. Fourchette **66 à 170 $/mois** (66 $ = Graviton 2 vCPU, non validé ; 170 $ = instance mémoire 16 Gio).
- **Cadence du pool** (11 sources × 1 session/min) : **≈ 420 $/mois (≈ 375 €)** nominal (`c6i.2xlarge`, 8 vCPU) ; fourchette **170 à 1 860 $/mois**. L'écart vient d'**un seul paramètre non publié par l'amont** : la part de trafic **sortant** du notaire (AWS facture le sortant 0,09 $/Go, l'entrant est gratuit). Le notaire reçoit ≈ 27 à 30 Mo par session, soit **12,8 à 14,3 To/mois entrants** à cette cadence.
- **Ce qui n'est pas dans ces chiffres** : l'audit externe (la vraie dépense, AVIS §5.2b), l'ingénierie, un éventuel plan de support AWS, la TVA, et la **bande passante montante du collecteur Shōgen** (il téléverse ces 13 à 14 To vers le notaire).
- **Variante qui change l'ordre de grandeur** : le **mode proxy** (non adopté, ADR à instruire) supprime les 30 Mo de matériel MPC par session ; le poste bande passante disparaît et le pool coûte alors à peu près le prix d'une petite instance (≈ 150 à 170 $/mois) [inféré].

**Pourquoi AWS ?** [lu, RECHERCHE-G4 et AVIS-G4] Ce n'était **pas le résultat d'une comparaison**. La recherche G4 a retenu Nitro parce que (i) l'amont TLSNotary l'utilise comme exemple de référence d'enclave (billet 2026-06-23 : Peer migre vers Nitro), (ii) c'est le seul fournisseur dont elle a lu la documentation en détail (`je n'ai pas lu de documentation AMD SEV-SNP primaire`, l. 102 ; prix « non lu », l. 162 et 240), (iii) « aucun supplément » Nitro (l. 101). L'AVIS (l. 70) demandait un devis, « ne pas engager ». Cette étude fait la comparaison qui manquait.

**Le choix tient-il ?** **Oui, comme repli, avec réserves**, et pour des raisons qui ne sont **pas le coût** (les fournisseurs sérieux coûtent 130 à 190 $/mois pour 4 vCPU : le prix n'est pas le discriminant). Les discriminants sont :
1. **Qui peut forger l'attestation.** Sur TDX et SEV-SNP, des attaques **publiées** (TEE.fail, DDRop) extraient ou forgent les clés d'attestation avec un interposeur mémoire bon marché et produisent des attestations que la bibliothèque Intel accepte au niveau « UpToDate » [lu]. Aucune des quatre pages d'attaques ne cite Nitro [lu, absence ≠ preuve]. Pour un notaire dont l'adversaire est **l'opérateur lui-même** (Shōgen), une racine tenue par un fournisseur dont l'opérateur ne touche jamais le matériel est préférable à une racine « fabricant » à clé extractible.
2. **Vérifiabilité hors ligne** : Nitro a une racine publiée à empreinte connue, vie de 30 ans, document COSE/CBOR autoportant [lu] ; TDX/SNP exigent des « collatéraux » Intel/AMD [inféré].
3. **Aucune surcharge d'enclave** chez AWS et Google Confidential Space [lu].
4. **Nouveau constat sur l'horloge** (comble une lacune de l'AVIS, l. 15 et RECHERCHE l. 110) : en mode MPC, le notaire **refuse** toute poignée de main dont l'heure diffère de plus de **5 s** de **sa propre horloge système** (`MAX_TIME_DIFF = 5`, `follower.rs`, révision épinglée `0fe3c32d`) [lu]. L'horloge de l'enclave devient donc une dépendance de sécurité (antidatage) et de disponibilité ; Nitro fournit un horodatage **signé par AWS** dans chaque document d'attestation, utilisable comme recoupement [lu pour le champ ; recoupement = [inféré]].

**Limites à dire clairement** : (a) aucune enclave, chez aucun fournisseur, ne retire le verdict « auto-opéré » tant que l'opérateur est Shōgen (AVIS §1) ; l'option principale reste le notaire tiers indépendant (A-bis) ; (b) « AWS est la racine, sans condition » (billet amont) ; (c) rien n'a été **mesuré** sur la session Shōgen : CPU, mémoire et trafic sortant sont des hypothèses déclarées.

**Les décentralisés (Phala, Oasis, Marlin, Secret, iExec, Super Protocol)** : aucun ne supprime la racine « fabricant ou hyperscaler » ; plusieurs la **masquent** (Marlin = Nitro avec des opérateurs tiers ; Secret = GCP ; dstack tourne aussi sur GCP et Nitro). **Phala Cloud** est le plus sérieux (dstack open source, audité par zkSecurity en 2025 sur un périmètre limité, tarifs lisibles : **171 $/mois** pour 4 vCPU/8 Go) mais sa racine est Intel TDX **plus** Phala (hôtes et, par défaut, KMS), les hôtes sont surtout aux États-Unis, l'entité juridique n'est pas établie [abs], et TDX est exposé aux attaques d'interposeur. **Oasis ROFL** est le moins cher (**≈ 17 à 33 $/mois** en ROSE) mais le marché compte **2 fournisseurs et 4 nœuds**, paiement en jeton volatil, aucun audit lu. Voir §7 (recommandation).

---

## 2. Sources lues

Toutes lues le 2026-10-04 ; copies dans `tee/web/` (nom entre parenthèses) ; niveau [lu] sauf mention.

| Id | Source (URL) | Copie |
|---|---|---|
| S1 | TLSNotary FAQ `https://tlsnotary.org/docs/faq` | `tlsn_faq.raw` |
| S2 | TLSNotary, billet 2026-05-10 (benchmarks proxy) `…/blog/2026/05/10/blog-proxy-mode` | `tlsn_blog_proxy.raw` |
| S3 | TLSNotary, billet 2026-06-23 « Where does your trust live? » `…/blog/2026/06/23/where-trust-lives` | `tlsn_where.raw` |
| S4 | TLSNotary, billets 2026-05-19 (fast-reveal), 2026-01-19 (alpha.14), 2025-08-31 (benchmarks) | `tlsn_fastreveal.raw`, `tlsn_a14.raw`, `tlsn_bench2025.raw` |
| S5 | `tlsnotary/tlsn` @ `0fe3c32d35382b3f290a43c4156399ca4512bb89` : `crates/mpc-tls/src/follower.rs`, `leader.rs`, `crates/tlsn/src/verifier.rs`, `crates/core/src/connection.rs` (`raw.githubusercontent.com`) | `tlsn_crates_mpc-tls_src_*.raw`, `tlsn_conn.raw` |
| S6 | AWS Nitro Enclaves : `docs.aws.amazon.com/enclaves/latest/user/{nitro-enclave,verify-root,nitro-enclave-concepts}.html` | `aws_enc_*.raw` |
| S7 | AWS Price List Bulk API (fichiers officiels) : `pricing.us-east-1.amazonaws.com/offers/v1.0/aws/{AmazonEC2,AWSDataTransfer,AmazonVPC}/…` régions `eu-west-3`, `eu-central-1` (EC2 `publicationDate 2026-09-25T17:45:21Z` ; transfert 2026-09-16 ; VPC 2026-09-17) | `aws_extract_*.txt`, `aws_dt_*.json`, `aws_vpc_*.json` (les gros fichiers EC2 ont été supprimés après extraction) |
| S8 | AWS, whitepaper Nitro, « No AWS operator access » | `nitro_wp_intro.raw` |
| S9 | TEE.fail `tee.fail` ; WireTap `wiretap.fail` ; Battering RAM `batteringram.eu` ; DDRop `ddropattack.eu` | `teefail.raw`, `wiretap.raw`, `batteringram.raw`, `ddrop.raw` |
| S10 | dstack (`Dstack-TEE/dstack`, branche `master`) : README, `docs/security/{security-model,public-security-reports}.md`, `docs/design-and-hardening-decisions.md`, `docs/verification.md`, `docs/security/dstack-audit.pdf` (zkSecurity, 39 p.) | `dstack_*.raw` |
| S11 | Phala : `phala.com/{pricing,trust,about,compare/phala-vs-aws-nitro}`, `cloud.phala.com/about/{pricing,billing}`, API publique `cloud-api.phala.com/api/v1/{instance-types,attestations/nodes}`, `docs.phala.com/…` (compliance, cloud-vs-onchain-kms, dstack-cloud/overview, FAQ) | `phala_*.raw`, `phala_itypes.json`, `phala_nodes.json` |
| S12 | Google Cloud : `…/confidential-vm/pricing`, `…/confidential-space/{pricing,docs/confidential-space-overview}`, `…/supported-configurations` | `gcp_*.raw` |
| S13 | Azure : API publique `prices.azure.com/api/retail/prices` (France Central, West Europe), `learn.microsoft.com/…/dcasv6-series`, `…/confidential-vm-overview`, `…/attestation/overview` | `az_*.raw`, `az_dc4_france.json` |
| S14 | STACKIT `stackit.com/en/products/confidential/stackit-confidential-server` | `stackit_server.raw` |
| S15 | Marlin Oyster : `docs.marlin.org/oyster/…` (guarantees, actors, repro-builds, remote-attestations, quickstart), monorepo `marlinprotocol/oyster-monorepo` README | `marlin_*.raw` |
| S16 | Oasis ROFL : `docs.oasis.io/build/rofl/…`, `docs.oasis.io/node/…/set-up-tee`, indexeur public `nexus.oasis.io/v1/sapphire/roflmarket_{providers,offers,instances}` | `oasis_*.raw`, `oasis_offers.json`, `oasis_providers.json`, `oasis_inst.json` |
| S17 | Secret Network (SecretVM) `docs.scrt.network/…` ; iExec `docs.iex.ec/…` ; Super Protocol `superprotocol.com/` | `secret_*.raw`, `iexec_*.raw`, `super_home.raw` |
| S18 | CoinGecko API publique (sans clé) `api.coingecko.com/api/v3/simple/price` : lu 2026-10-04 03:22:40 UTC | `coingecko_2026-10-04.json` |
| S19 | Dépôt : `RECHERCHE-G4-NOTAIRE.md`, `AVIS-G4-NOTAIRE.md`, `docs/08`, `docs/17`, `fixtures/` (944 o reçus, 173 o envoyés) | [lu] |

---

## 3. Charge du notaire (dimensionnement)

### 3.1 Ce que la source dit

- Formule amont de la charge montante du prouveur vers le vérificateur/notaire [lu, S1] : « ~25MB (a fixed cost per one TLSNotary session) + ~10 MB per every 1KB of outgoing data + ~40KB per every 1 KB of incoming data. » (FAQ, avec la réserve qu'elle date d'une « upcoming protocol upgrade planned for 2025 »).
- Mesure plus récente [lu, S2, billet 2026-05-10] : “MPC mode runtime is dominated by uploading ~30 MB of garbled-circuit material before the TLS handshake even begins.” (profil 1 Ko / 2 Ko). La direction est **prouveur → notaire** : le notaire **reçoit** ces 30 Mo. Durées MPC : 3 à 15 s sur profils résidentiels ; rapport MPC/proxy 1,8× à 1 Gbit/s contre 12,5× à 5 Mbit/s (S2).
- Charge Shōgen [lu, S19] : requête `sent` 173 o, réponse `recv` 944 o (fixtures) ; plafonds de la session : 4 Kio envoyés, 16 Kio reçus (`session/src/main.rs` l. 79-80) ; la session révèle la totalité du transcript (voie « full-reveal », S4 : le coût côté réponse devient constant).
- Matériel des mesures amont [lu, S4] : « AWS c5.4xlarge instance (16 vCPU, 3.0 GHz, 32 GB RAM) » (2025-08 et 2026-01) ; Ryzen 9 9950X 16 cœurs, 64 Go (2026-05-10). **Aucune consommation CPU ou mémoire par session n'est publiée** [abs, sur toutes les pages S1-S5 lues].

### 3.2 Hypothèses écrites (H1-H6)

| Id | Hypothèse | Statut |
|---|---|---|
| H1 | Entrant par session au notaire : **27 Mo** (formule FAQ : 25 + 10×0,173 + 0,04×0,944 ≈ 26,8) à **30 Mo** (billet) | [lu] + calcul |
| H2 | Durée par session : **≈ 2 s** (inter-datacentres ≥ 1 Gbit/s : proxy ≈ 1 s × 1,8) à **15 s** (pire profil lu) | borne basse [inféré] |
| H3 | Part sortante du notaire (notaire → prouveur) : **non publiée** ; scénarios **2 %, 10 %, 50 %, 100 %** de l'entrant | [abs] ; scénarios [inféré] |
| H4 | CPU et mémoire par session : **non publiés** ; dimensionnement par hypothèse (voir 3.3) | [abs] |
| H5 | Sessions **étalées** (gigue) ; si les 11 sources partent à la même seconde, pic de 11 sessions simultanées (≈ 330 Mo en quelques secondes) | [inféré] |
| H6 | 730 h/mois, 24 h/24 ; mois de 30 jours pour le comptage de sessions | convention |

### 3.3 Résultats

| | (a) Pilote | (b) Pool 11 sources × 1/min |
|---|---|---|
| Sessions/mois | 4/h → **2 880** | 11 × 60 × 24 × 30 = **475 200** |
| Entrant au notaire (H1) | **78 à 86 Go/mois** | **12,8 à 14,3 To/mois** (moyenne ≈ 44 Mbit/s ; crête ≥ 120 à 240 Mbit/s par session) |
| Sortant (H3) | 2 % → 2 Go ; 10 % → 8-9 Go ; 100 % → 78-86 Go (sous la franchise AWS de 100 Go) | 2 % → 257-285 Go ; 10 % → 1,3-1,4 To ; 50 % → 6,4-7,1 To ; 100 % → 12,8-14,3 To |
| Simultanéité moyenne (H2) | ≪ 1 | 11/60 s × (2 à 15 s) = **0,4 à 2,8** sessions ; pics selon H5 |
| vCPU / RAM proposés (**hypothèse**) | **4 vCPU / 8 Gio** (plus petite instance x86 éligible Nitro : voir 5.1) | **8 vCPU / 16 Gio**, réseau ≥ 1 Gbit/s, sessions étalées |
| Réseau | trivial | **le poste dominant** : MPC « bandwidth-bound » (S1 : « the protocol is bandwidth-bound ») |

**Côté prouveur** (collecteur Shōgen, hors devis du notaire) : il téléverse les mêmes 13-14 To/mois au pool. Si l'hébergeur actuel les facture au tarif sortant AWS (0,09 $/Go), ce poste vaudrait ≈ 1 250 $/mois ; l'hébergeur réel n'a pas été lu [abs]. C'est un coût caché du transport MPC à cette cadence (AVIS §2 : le mode proxy « supprime ce poste »).

**Faisabilité à mesurer avant tout engagement** (aucune mesure faite ici) : CPU, RSS, octets dans/hors, durée, sur la session Shōgen scindée (prouveur/notaire) à la révision `0fe3c32d`, y compris sous Nitro (réseau par `vsock`).

---

## 4. Comparatif des fournisseurs

Légende : [lu] source S-n ; [inféré] ; [abs]. « Vue acheteur » = ce qu'un acheteur institutionnel en penserait : **[inféré]** partout (aucun texte réglementaire détenu, comme dans RECHERCHE-G4 §2.5).

### 4.1 Technologie, racine de confiance, attestation, reproductibilité, horloge

| Fournisseur | Enclave | Qui détient la racine | Forme de l'attestation ; vérifiable hors ligne ? | Image reproductible ? | Source d'heure |
|---|---|---|---|---|---|
| **AWS Nitro Enclaves** | Nitro (hyperviseur + cartes Nitro), pas TDX/SNP [S6] | **AWS** : PKI Nitro, racine publiée, « lifetime of 30 years », empreinte SHA-256 donnée [S6]. Billet amont : « AWS is the root, unconditionally. » [S3] | COSE_Sign1/CBOR : `module_id`, `timestamp`, `pcrs`, `certificate`, `cabundle`, `public_key`, `user_data`, `nonce` [S6]. Hors ligne : **oui en principe** (racine épinglée, pas de service) [lu pour la racine ; « hors ligne » = [inféré]] | PCR0 = condensat de l'EIF [S6]. Build déterministe **non documenté** dans les pages AWS lues [abs]. Marlin construit ses EIF par un pipeline **Nix** “instead of the official nitro-cli tool” [S15] (⇒ nitro-cli seul n'est pas présenté comme reproductible [inféré]) | Champ `timestamp` **signé** : « UTC time when document was created, in milliseconds since UNIX epoch » [S6]. Horloge **applicative** de l'enclave : [abs] |
| **Google Cloud Confidential Space / Confidential VM** | Intel TDX (C3), AMD SEV-SNP (N2D), AMD SEV [S12] | CPU : Intel/AMD ; **service d'attestation : Google** (Google Cloud Attestation, ou Intel Trust Authority) [S12] | Jetons d'identité émis par le service d'attestation [S12]. Hors ligne : [abs] ; vérification d'un jeton signé hors ligne = [inféré] | Image Confidential Space durcie ; reproductibilité de l'image [abs] | [abs] |
| **Azure Confidential VM / Containers** | AMD SEV-SNP (séries DCasv6…), Intel TDX (DCesv6) [S13] | AMD/Intel + **Microsoft Azure Attestation** [S13] | Jetons Azure Attestation ; rapport signé [S13]. Hors ligne : [abs] | [abs] | [abs] |
| **Européens** : STACKIT (Schwarz Digits) | « Confidential Server » (AMD SEV cité en exemple) [S14] | AMD + STACKIT | [abs] | [abs] : « support of individual images » seulement | [abs] |
| OVHcloud, Scaleway, IONOS | **Aucune offre TEE établie** : URL deviné → 404 ; sitemaps de Scaleway (pages, articles, docs), OVH (aide), IONOS : aucune URL contenant `confidential`, `tdx`, `sev-snp`, `enclave` | — | — | — | — |
| **Phala Cloud (dstack)** | **Intel TDX** (production) ; AMD SEV-SNP : “it is new and experimental” [S10] ; GPU NVIDIA | **Intel** (chaîne PCK/collatéral) **+ Phala** (hôtes ; **KMS Cloud** : « In Cloud KMS, Phala controls what code runs. » [S11]) ; option **KMS on-chain** (Ethereum/Base) [S11] | Quote TDX + journal d'événements (RTMR3) ; vérification par `dcap-qvl` (Rust, Python, JS/WASM, CLI) [S10]. Hors ligne : possible avec collatéral embarqué [inféré] ; l'audit note « Lack of Revocation Checks » dans `dcap-qvl` (sévérité Low) [S10] | **OS** : « Deterministic builds mean anyone can verify the OS image hash » ; conteneurs par digest SHA-256 ; `compose-hash` mesuré [S10] | `tsc=reliable no-kvmclock` + NTS ; **optionnel** : “If `secure_time` is disabled, time synchronization is not enforced before application launch.” [S10] |
| **dstack-cloud** (logiciel Phala, sur **votre** compte GCP ou AWS) | TDX sur GCP, Nitro sur AWS [S11] | Google ou AWS (+ KMS dstack) ; « AWS remains trusted » [S10] | NSM (Nitro) ou quote TDX [S11] | comme dstack [S10] | comme dstack (TDX) ; timestamp NSM (Nitro) |
| **Marlin Oyster** | **AWS Nitro** (NSM) : « guarantees … based on … the underlying TEE hardware manufacturer (AWS Nitro Enclaves) » [S15] | **AWS**, plus **opérateurs tiers** (comptes EC2), contrats sur Arbitrum, jetons POND/USDC [S15] | Document Nitro (même format) ; vérificateur ZK RISC Zero et enclave-vérificateur dans le monorepo [S15] | **Oui, Nix** pour EIF et outils [S15] | comme Nitro ; paramètres du protocole : « currently set to TBD » [S15] |
| **Oasis ROFL** | Intel **TDX** (conteneurs, défaut), TDX brut, ou SGX [S16] | Intel + **Oasis** (chaîne Sapphire, marché ROFL) | Vérification par la chaîne Oasis (détails [abs]) | [abs] | « node's local clock is synchronized (e.g. using NTP) » (exigence de nœud, pas garantie d'enclave) [S16] |
| **Secret Network (SecretVM)** | TDX, SEV-SNP, + GPU NVIDIA [S17] | Intel/AMD + **GCP** (VM lancée dans un projet GCP géré par Secret, ou le vôtre) [S17] | Rapport TDX/SNP + `secretvm-verify` [S17] | [abs] | [abs] |
| **iExec** | TDX (iApp), tâches par « workerpool » ; jeton RLC [S17] | Intel + opérateurs de workerpool | [abs] | [abs] | [abs] |
| **Super Protocol** | Aujourd'hui « Super Swarm » : « Provider-hosted. Never provider-controlled », multi-cloud/sur site [S17] | Fabricant + fournisseur | [abs] | [abs] | [abs] |
| **Automata** | **Pas un hébergeur** : couche d'attestation (vérificateur DCAP on-chain, services de collatéral) [S17] ; la FAQ Phala cite son vérificateur Solidity [S11] | — | — | — | — |

### 4.2 Maturité, audits, pérennité, juridiction, intégration Rust, vue acheteur

| Fournisseur | Maturité et audits publiés | Pérennité / juridiction | Intégrer un binaire Rust | Vue acheteur [inféré] |
|---|---|---|---|---|
| **AWS Nitro** | Nitro Enclaves ancien ; whitepaper : “By design the Nitro System has no operator access.” [S8]. Audits tiers du Nitro : non lus [abs]. Crates `aws-nitro-enclaves-nsm-api`, `-cose`, `attestation-doc-validation` : existence lue par G4 (non relue ici, R-8 incomplet) [2nd : RECHERCHE-G4 l. 162] | Hyperscaler ; société américaine [inféré] ; régions UE (Paris, Francfort) ; une région « AWS European Sovereign Cloud (Germany) » figure dans le fichier de prix [S7] (non étudiée) | Bon : `nsm-api` est « primarily written in Rust » [S15] ; EIF par `nitro-cli` ; réseau par `vsock` (proxy dans le parent) | Fournisseur déjà homologué dans la plupart des achats ; objection : racine unique, code fermé, « AWS est la racine ». Familier, donc acceptable en repli |
| **Google Conf. Space/VM** | Mature ; pas d'audit lu [abs] | Hyperscaler, américain [inféré] ; régions UE | Conteneur (Docker) sur CVM : correct | Idem AWS ; racine Intel/AMD **plus** Google ; exposition aux interposeurs |
| **Azure Conf. VM** | Mature ; pas d'audit lu [abs] | Hyperscaler, américain [inféré] | VM Linux : correct | Idem ; Microsoft Azure Attestation comme tiers de vérification |
| **STACKIT** | « currently only available to a limited extent and on request » [S14] ; pas de prix, pas d'audit | Schwarz Digits Cloud GmbH & Co. KG, Bad Friedrichshall (Allemagne) [S14] | VM : correct | Argument souveraineté, mais offre non généralisée ; à sonder, pas à retenir |
| **Phala Cloud / dstack** | **Audit zkSecurity** (2025-05-26 à 06-13, `dstack` @ `be9d0476`) : 14 constats = **1 High, 7 Medium, 4 Low, 2 Info** ; KMS et `dcap-qvl` **hors périmètre** (audits recommandés) [S10]. Suivi public des rapports jusqu'au 2026-06-30 [S10]. « Linux Foundation Confidential Computing Consortium project » et clients (OpenRouter, NEAR AI) : affirmations du README [S10, déclaratif]. **SOC 2 Type I** [S11] ; HIPAA : page Trust « Compliant » mais docs « Coming Soon » : **contradiction** [S11] | Phala Network / « Hashforest Technology » (pied de page) ; **pays de l'entité [abs]**. Hôtes (API publique) : 22 nœuds, dont **1 à Paris et 1 à Amsterdam** ; le tarif CPU dit “CPU machines run in US East. Europe is not open by default” [S11]. Jeton PHA : 0,0714 $ (rang 424) [S18] | **Très bon** : dstack-sdk Rust, `dcap-qvl` Rust, Docker Compose (un binaire Rust en conteneur) [S10] | Start-up web3 ; SOC 2 Type I seulement ; racine Intel + Phala ; dépendance à un petit prestataire TIC (registre DORA) ; atout : code ouvert, attestation reproductible |
| **Marlin Oyster** | Docs partielles (paramètres « TBD ») ; aucun audit lu [abs] | Marlin Foundation ; opérateurs tiers sur AWS ; paiement USDC (Arbitrum) | EIF Nix ; SDK Rust | Ajoute une contrepartie (opérateur anonyme) **sans** changer la racine AWS : moins bon que AWS en direct pour cet usage |
| **Oasis ROFL** | Réseau L1 établi ; ROFL récent ; aucun audit lu [abs] | Oasis Protocol Foundation : **2 fournisseurs, 4 nœuds** sur le marché ROFL (indexeur public) ; ROSE 0,00836 $ [S16, S18] | Conteneur TDX ; app à enregistrer sur Sapphire | Faible lisibilité institutionnelle ; paiement en jeton |
| **Secret / iExec / Super Protocol** | « SecretVM is currently under active development » [S17] ; iExec : modèle par tâches ; Super : pivot récent | Fondations/entreprises web3 | VM/conteneur | À écarter pour ce rôle |

### 4.3 Exposition aux attaques publiées

| Attaque (pages d'auteurs, S9) | Ce que la page dit [lu] | Technologies concernées | Nitro ? |
|---|---|---|---|
| **TEE.fail** (IEEE S&P '26) | « extract cryptographic keys from Intel TDX and AMD SEV-SNP with Ciphertext Hiding, including in some cases secret attestation keys » ; quote TDX forgé accepté par la DCAP d'Intel au niveau « UpToDate » ; interposeur DDR5 « briefcase » | TDX, SEV-SNP, GPU NVIDIA CC (via clés extraites) | non cité [abs] |
| **WireTap** (CCS '25) | clé d'attestation SGX extraite sur machine en état de confiance ; attaques de bout en bout sur des déploiements SGX | SGX (DDR4) | non cité [abs] |
| **Battering RAM** (S&P '26) | interposeur DDR4 « $50 » ; « fully breaks … Intel SGX and AMD SEV-SNP » ; Intel/AMD : “physical attacks on DRAM are out of scope for their current products” (cité par la page DDRop) | SGX, SEV-SNP | non cité [abs] |
| **DDRop** (CCS '26, **septembre 2026**) | “on Intel TDX, even forge the security evidence used to prove that a virtual machine is trusted” ; ne dépend pas d'un bogue logiciel ; fraîcheur de la mémoire non assurée par TDX, SGX scalable, SEV-SNP | TDX, SEV-SNP, SGX scalable, Arm CCA | non cité [abs] |

Portée pour Shōgen [inféré] : ces attaques exigent un **accès physique** à un serveur. L'adversaire que le notaire doit contenir est **Shōgen lui-même** (l'opérateur). Sur TDX/SEV-SNP, un opérateur qui possède **une** machine compatible peut en extraire une clé d'attestation et **forger des citations pour n'importe quelle mesure** (page TEE.fail : citation forgée acceptée par la bibliothèque Intel) ; la parade est d'**épingler l'identité de plateforme** (Phala publie les PPID et identifiants de ses nœuds par API publique, 21 PPID sur 22 nœuds [lu, S11] ; liste d'autorisation d'appareils du KMS on-chain [lu, titre de page S11]). Sur Nitro, la clé d'attestation est tenue dans le matériel et la PKI d'AWS : forger exige de compromettre AWS. **« Aucune page d'attaque ne cite Nitro » n'est pas une preuve de résistance** ; je n'ai trouvé aucune déclaration AWS sur les interposeurs DRAM dans les pages Nitro lues [abs].

---

## 5. Coûts

Règle : tous les prix viennent de **pages ou API publiques lues aujourd'hui** (URL, date, [lu]). Conversion USD→EUR : 1 $ = 0,888 € (CoinGecko, `usd-coin`/eur, 2026-10-04 03:22 UTC) [S18]. Hypothèse : 730 h/mois. Calculs reproductibles : `tee/cost.py`.

### 5.1 Prix lus

| Fournisseur | Unité minimale admissible / supplément enclave | Prix lu | Stockage, transfert | Source, date |
|---|---|---|---|---|
| **AWS Nitro** (Paris `eu-west-3`) | Parent Nitro x86 : toute famille M/C/R **sauf `.large`** (donc **xlarge = 4 vCPU minimum**) ; Graviton : tout sauf `.medium` (donc `.large` 2 vCPU admis) [S6]. `T3` : absent de la liste [lu]. **Supplément Nitro : aucun** : « There are no additional charges for using Nitro Enclaves. » [S6] | `c6i.xlarge` (4 vCPU, 8 Gio) **0,202 $/h** ; `c7i.xlarge` 0,2121 ; `m6i.xlarge` (16 Gio) 0,224 ; `c6i.2xlarge` (8 vCPU, 16 Gio) 0,404 ; `c6g.large` (Graviton, 2 vCPU, 4 Gio) 0,081 ; réservation 1 an standard sans avance `c6i.xlarge` 0,13335 $/h | EBS gp3 **0,0928 $/Go-mois** ; IPv4 publique **0,005 $/h** ; entrée **0 $/Go** ; sortie : 100 Go/mois gratuits (agrégés), puis **0,09 $/Go** (10 premiers To), 0,085 ensuite | AWS Price List Bulk API, EC2 `publicationDate 2026-09-25T17:45:21Z`, transfert 2026-09-16, VPC 2026-09-17 ; lu 2026-10-04 |
| AWS autres régions | | `c6i.xlarge` : Francfort 0,194 ; N. Virginie 0,170 | gp3 : Francfort 0,0952 ; N. Virginie 0,08 ; sortie 0,09 $/Go (idem) | idem |
| **Google Cloud** | Confidential VM : **surcharge** par vCPU et par Gio sur le prix Compute Engine ; **Confidential Space : “There is no additional cost to use Confidential Space.”** [S12] | TDX (C3) **0,0033982 $/vCPU-h + 0,0004555 $/Gio-h** (4 vCPU/16 Gio : 0,0209 $/h ≈ **15 $/mois**) ; SEV-SNP (N2D) 0,0027502 + 0,0003686 (≈ 12 $/mois) | **prix de base de la VM : non lu** [abs] (tables dynamiques, aucune API publique sans clé) ; sortie : non lue | `cloud.google.com/confidential-computing/confidential-vm/pricing` et `…/confidential-space/pricing`, 2026-10-04 |
| **Azure** | VM confidentielle : pas de ligne de surcharge ; VMGS (petit disque) « might incur a monthly storage cost » ; disques OS chiffrés plus chers « From March 30 2026 » [S13] | France Central, Linux : `DC2as_v6` (SEV-SNP, 2 vCPU/8 Gio) **0,117 $/h** ; `DC4as_v6` (4/16) **0,235** ; West Europe : `DC2es_v6` (TDX, 2 vCPU, mémoire non lue) 0,133 ; `DC4es_v6` 0,266 ; `DC4as_v6` 0,242 | Sortie : 100 Go gratuits puis **0,087 $/Go** (France Central) ; disques : non lus | API `prices.azure.com/api/retail/prices`, entrées au 2026-09-01 / 2026-10-01, lu 2026-10-04 |
| **Phala Cloud** | Pas de supplément ; machine entière (CVM TDX) facturée **à la minute** ; « Compute stops. Storage stays until you delete it. » | `tdx.small` (1 vCPU/2 Go) **0,058 $/h** ; `tdx.medium` (2/4) **0,116** ; `tdx.large` (4/8) **0,232** ; `tdx.xlarge` (8/16) **0,464** ; `tdx.2xlarge` (16/32) 0,928 | Disque **0,000139 $/Go-h (≈ 0,10 $/Go-mois)**, 20 Go minimum ; bande passante : « Each machine includes bandwidth based on its size » (**volume [abs]**) ; “CPU machines run in US East. Europe is not open by default; contact support to enable it.” ; SLA 99,9 % réservé à l'offre entreprise | `cloud-api.phala.com/api/v1/instance-types` (API publique), `cloud.phala.com/about/pricing` (mise à jour 2026-07-03), `phala.com/pricing` (arrondis 0,06/0,12/0,23) ; lu 2026-10-04 |
| **Oasis ROFL** (fournisseur Oasis Protocol Foundation, Sapphire) | Offres **publiques** (conteneur TDX [inféré : `tee: 2`]) | `small` (1 vCPU/2 Gio/3 Go) **1 ROSE/h** ou 500 ROSE/mois ; `medium` (2/4/10) **2 ROSE/h** ou 1 000/mois ; `large` (4/8/40) **4 ROSE/h** ou **2 000 ROSE/mois** ; mention « Limited-time offer! Lifetime 50% discount » (prix possiblement ×2 à la fin de la remise) | ROSE = **0,00836 $** (CoinGecko, 2026-10-04 03:22 UTC) ; frais de gaz et bande passante : [abs] | indexeur `nexus.oasis.io/v1/sapphire/roflmarket_providers/{adresse}/offers`, lu 2026-10-04 |
| **Marlin Oyster** | Opérateurs tiers, paiement USDC (Arbitrum) | **[abs]** (le démarrage rapide exige « 1 USDC and 0.001 ETH » pour 15 min, ce n'est pas un tarif) | POND = 0,00162 $ [S18] | `docs.marlin.org/oyster/build-cvm/quickstart` |
| **Secret** (SCRT 0,00889 $), **iExec** (RLC 0,367 $), **Super Protocol**, **STACKIT** | | **[abs]** : aucun tarif lu | | |
| **Automata** | | non applicable (couche de vérification) | | |

### 5.2 Coût mensuel estimé

#### (a) Pilote : 4 sessions/h, 2 880 sessions/mois, ≈ 80 Go entrants (H1, H6)

| Option | Composition | **Mensuel** (USD) | € |
|---|---|---|---|
| **AWS Nitro, Paris, `c6i.xlarge` (nominal)** | 147,5 + EBS 30 Go 2,8 + IPv4 3,6 + sortie 0 | **≈ 154** | ≈ 137 |
| AWS bas : `c6g.large` Graviton (2 vCPU/4 Gio) | 59,1 + 2,8 + 3,6 | **≈ 66** | ≈ 58 |
| AWS bas « engagé » : `c6i.xlarge` réservation 1 an | 97,3 + 2,8 + 3,6 | ≈ 104 | ≈ 92 |
| AWS haut : `m6i.xlarge` (16 Gio) | 163,5 + 2,8 + 3,6 | **≈ 170** | ≈ 151 |
| AWS N. Virginie `c6i.xlarge` (juridiction US) | 124,1 + 2,4 + 3,6 | ≈ 130 | ≈ 116 |
| Azure SEV-SNP `DC4as_v6` France Central | 171,5 + disque (non lu) | ≈ 172 + disque | ≈ 152 |
| Azure SEV-SNP `DC2as_v6` | 85,4 + disque | ≈ 85 + disque | ≈ 76 |
| Google TDX 4 vCPU/16 Gio | surcharge 15,2 + **base VM non lue** | ≥ 15 + base [abs] | |
| **Phala Cloud `tdx.large`** | 169,4 + disque 20 Go 2,0 | **≈ 171** | ≈ 152 |
| Phala `tdx.medium` (2 vCPU/4 Go) | 84,7 + 2,0 | ≈ 87 | ≈ 77 |
| **Oasis ROFL `large`** | 4 ROSE/h → 2 920 ROSE ; ou 2 000 ROSE (terme mensuel) | **≈ 17 à 24** (≈ 33 si fin de la remise) | ≈ 15 à 29 |
| Marlin, Secret, iExec, Super, STACKIT | tarif non lu | non chiffrable | |

Sensibilité jeton (Oasis) : si ROSE ×3 → ≈ 50 $/mois ; si ROSE ÷3 → ≈ 6 $/mois. Le prix de l'offre est fixé **en ROSE** par le fournisseur : le coût en dollars suit le cours.

#### (b) Cadence du pool : 475 200 sessions/mois, 12,8 à 14,3 To entrants (H1, H6)

Le sortant (H3) fait varier le coût AWS ; entrant gratuit. Valeurs pour 30 Mo/session.

| Sortant (H3) | Sortant/mois | AWS Paris `c6i.xlarge` | AWS Paris **`c6i.2xlarge`** | AWS 2 × `c6i.2xlarge` (haute dispo.) |
|---|---|---|---|---|
| 2 % | 285 Go | 171 $ | **318 $** | 619 $ |
| **10 % (nominal)** | 1,4 To | 273 $ | **421 $** (≈ 374 €) | 722 $ |
| 50 % | 7,1 To | 786 $ | 934 $ | 1 235 $ |
| 100 % | 14,3 To | 1 408 $ | 1 556 $ | **1 857 $** |

Autres fournisseurs, même hypothèse nominale (10 %) [inféré, calculs `cost.py`] :
- **Azure** : 2 × `DC4as_v6` France Central = 343 $ + sortie (1,4 To − 100 Go) × 0,087 ≈ 115 $ → **≈ 460 $** (disques non lus).
- **Phala** : `tdx.xlarge` (8 vCPU/16 Go) **≈ 341 $** + bande passante **non chiffrable** (« included based on size », volume [abs] ; 14 To/mois entrants risquent de dépasser l'inclus [inféré]).
- **Oasis** : 2 × `large` ≈ 33 à 67 $ + bande passante [abs].
- **Google** : surcharge 8 vCPU/32 Gio ≈ 30,5 $ + base VM non lue.

**Fourchette AWS à retenir** : pilote **66 à 170 $/mois (nominal 154)** ; pool **170 à 1 860 $/mois (nominal 421)** ; **la borne haute est une borne de stress** (sortant = entrant), pas une prévision.

**Mode proxy** [inféré, non adopté] : sans les 30 Mo de matériel MPC, le trafic par session tombe à quelques Ko ; le pool reste dans l'ordre de **150 à 170 $/mois** (une `c6i.xlarge`). Le mode proxy est un autre transport avec un autre résidu (AVIS §2).

### 5.3 Ce que ces chiffres ne contiennent pas

- Audit externe du compagnon et de la demi-notaire (AVIS §5.2b : « la vraie dépense »), ingénierie de l'enclave, CI de build reproductible.
- Plan de support AWS, KMS, journaux et supervision, nom de domaine/DNS, TVA : **non lus** [abs].
- Remises d'engagement négociées, crédits : non lus.
- Bande passante montante du collecteur (voir 3.3).
- Aucun devis n'a été demandé (aucun contact, aucun compte) : **ce sont des prix de liste**.

---

## 6. Pourquoi AWS a été proposé (recherche G4), et le choix tient-il ?

### 6.1 Ce que la recherche G4 a réellement établi [lu]

- **Origine du choix.** `RECHERCHE-G4` §2.2 option B (l. 94-110) : l'amont TLSNotary décrit l'enclave via l'exemple de Peer sur **AWS Nitro** (billet 2026-06-23) ; la recherche relit ce billet (“moves it from Peer to AWS, a far better-resourced and more accountable custodian”) ; elle lit la doc Nitro (concepts, “Verifying the root of trust”, page produit, whitepaper) mais **seulement la page d'aperçu Intel TDX** et **« pas de documentation AMD SEV-SNP primaire »** (l. 102). Raisons avancées pour Nitro : attestation COSE/CBOR documentée, **aucun supplément** (l. 101, 162, 196), format COSE/CBOR proche de l'enveloppe du projet (l. 101, explicitement « [inféré : synergie, non vérifiée] »), crates d'attestation existantes (l. 162).
- **Ce qui n'a pas été fait** : aucune comparaison de fournisseurs, aucun prix d'instance (« prix de l'instance non lu », l. 162 ; manque 5, l. 240), aucune source d'heure (l. 110), aucune étude de reproductibilité des images Nitro (l. 240). L'AVIS (§1, §5.2a) maintient Nitro **comme repli** (déclencheur : aucun opérateur tiers trouvé à l'échéance) et demande un devis.
- **Conclusion** : AWS a été **le candidat le mieux documenté**, pas le vainqueur d'une comparaison.

### 6.2 Verdict après comparaison (cette étude)

| Critère | AWS Nitro | GCP/Azure (TDX/SNP) | Phala/dstack | Marlin | Oasis |
|---|---|---|---|---|---|
| Coût 4 vCPU/mois | ≈ 154 $ | ≈ 172 $ (Azure SNP) ; GCP non lu | ≈ 171 $ | non lu | ≈ 17-33 $ (jeton) |
| Surcharge d'enclave | aucune | GCP : +15 $ (TDX) ; Space : aucune | aucune | — | — |
| Racine | AWS | CPU + Google/Microsoft | Intel + Phala (+ KMS) | AWS + opérateur | Intel + Oasis |
| Clé d'attestation extractible par attaque publiée | non cité (≠ preuve) | **oui** (TEE.fail, DDRop) | **oui** (TDX) | non cité | **oui** (TDX/SGX) |
| Attestation vérifiable hors ligne | racine épinglée, 30 ans | collatéral/jeton en ligne [inféré] | `dcap-qvl` + collatéral | idem Nitro | [abs] |
| Image reproductible | non documentée (pipeline Nix possible) | [abs] | **oui (OS + digests)** | **oui (Nix)** | [abs] |
| Horloge | **timestamp signé AWS** + horloge d'enclave [abs] | [abs] | TSC + NTS optionnel | idem Nitro | [abs] |
| Audit publié | Nitro : [abs] | [abs] | **zkSecurity 2025** (périmètre partiel) | [abs] | [abs] |
| Rust | bon | correct | **très bon** | bon | correct |
| Juridiction / acheteur | US, familier | US, familier | entité [abs], atypique | atypique | atypique |

Le choix d'AWS **tient** pour le rôle de repli **si** les trois conditions de §7.3 sont remplies. Il ne tient **pas** comme « la meilleure enclave en soi » : la différence avec dstack-sur-GCP/Nitro ou Azure tient à des garanties de racine et d'outillage, pas au prix.

---

## 7. Recommandation

### 7.1 Principale (pour le repli B) : **AWS Nitro Enclaves, région UE (Paris), opéré par Shōgen, avec les mêmes ancrages que l'AVIS**

Motifs : coût nominal le plus bas des offres établies (≈ 154 $/mois pilote), aucune surcharge d'enclave, racine publiée à vie longue vérifiable hors ligne, attestation autoportante avec horodatage signé, pas d'attaque physique publiée citant Nitro (réserve : absence ≠ preuve), écosystème Rust (`nsm-api`), pas de nouvel intermédiaire.
**Le verdict reste « auto-opéré, en enclave » ; A(enclave-integrity) devient porteur ; l'option principale de l'AVIS (notaire tiers indépendant) n'est pas remplacée.**

### 7.2 Repli du repli (à garder ouvert) : **dstack sur **votre** compte** (GCP Confidential VM TDX, ou Nitro)

Motifs : logiciel ouvert, attestation et KMS déjà outillés, **OS reproductible**, audité par zkSecurity (2025, périmètre partiel : KMS et `dcap-qvl` hors périmètre), SDK Rust, fonctionne sur **deux** hyperscalers (pas de verrou). C'est la meilleure réponse à « étudiez d'autres vendors » : on obtient la reproductibilité qu'AWS seul ne documente pas. **Phala Cloud géré** (171 $/mois) est utilisable **seulement comme banc d'essai** : racine Intel + Phala, KMS Cloud contrôlé par Phala par défaut, hôtes surtout aux États-Unis, SOC 2 Type I seulement.
Azure DC-series (SEV-SNP, ≈ 172 $/mois) est le substitut centralisé si AWS devient impossible (jurisdiction, contrat).

### 7.3 Conditions pour que le repli AWS soit défendable devant un acheteur [inféré]

1. **Image reproductible** : deux constructions indépendantes de l'EIF donnent le même PCR0 (sinon pipeline Nix du type Marlin) ; PCR0 publié dans la liste de clés datée (AVIS §4.2).
2. **Horloge** : traiter `MAX_TIME_DIFF = 5 s` comme une dépendance de sécurité : l'enclave recoupe son heure avec le `timestamp` signé du document d'attestation (refus au-delà d'un seuil) ; sans cela l'hôte contrôle l'heure et la protection d'antidatage est vide.
3. **Clé générée dans l'enclave**, jamais exportée, publiée avec son PCR0 et le jeton RFC 3161 de la liste ; vérificateur hors ligne avec racine Nitro épinglée (empreinte lue : `64:1A:03:21:…:BB:5B`).

### 7.4 À écarter (pour ce rôle, maintenant)

- **Marlin Oyster** : même racine AWS **plus** un opérateur tiers anonyme, jetons, paramètres « TBD » ; strictement moins bon qu'AWS en direct.
- **Oasis ROFL** : le moins cher, mais 2 fournisseurs et 4 nœuds, prix en ROSE fixé par le fournisseur (volatilité ×3 plausible), TDX/SGX exposés aux interposeurs, aucun audit lu.
- **Secret/SecretVM** (« under active development », hébergé sur GCP), **iExec** (modèle de tâches), **Super Protocol** (pivot, pas de tarif/doc lue) : hors sujet pour un service persistant.
- **OVHcloud, Scaleway, IONOS** : aucune offre TEE trouvée (non établi, pas prouvé inexistant). **STACKIT** : « sur demande », à sonder si la souveraineté devient un critère.
- **Automata** : n'héberge rien ; utile seulement comme vérificateur on-chain, hors besoin.

### 7.5 Ce qui reste à vérifier avant tout engagement

1. **Mesurer** CPU, RSS, octets entrants/sortants, durée par session sur la session Shōgen scindée (révision `0fe3c32d`) : lève H3 et H4, qui font varier le coût de 170 à 1 860 $.
2. **Faisabilité** de `tlsn` alpha.16-pre **dans** une enclave Nitro : réseau par `vsock`, x86 contre Graviton, comportement de `UNIX_EPOCH` dans l'enclave (échec si l'écart dépasse 5 s).
3. **Reproductibilité de l'EIF** (essai de deux constructions).
4. **R-8 complet** des crates `aws-nitro-enclaves-nsm-api`, `-cose`, `attestation-doc-validation` (G4 n'a lu que l'existence et la licence) ; `dcap-qvl` si dstack.
5. **Devis AWS réel** (support, TVA, engagements) ; question juridique (société américaine, accès légal) à poser à un juriste, pas à ce lecteur.
6. **Posture d'AWS face aux interposeurs DRAM** : question à AWS ou lecture d'un audit tiers du Nitro ; aucune pièce lue ici.
7. **Ne rien engager** sans accord de l'investisseur (aucun contact, aucun compte créé dans cette étude).

---

## 8. Manques (rendus à l'orchestrateur, non comblés)

1. **Google** : prix de base des VM (C3, N2D) non lu (tables dynamiques, pas d'API publique sans clé) ; donc aucun total GCP ; tarif de sortie non lu ; vérification hors ligne des jetons de Google Cloud Attestation non lue.
2. **Azure** : mémoire de `DC2es_v6` non lue ; disques et VMGS non chiffrés en prix ; vérification hors ligne de MAA non lue.
3. **Européens** : URL de produits devinées → 404 chez OVHcloud, Scaleway, IONOS ; sitemaps sans occurrence ; moteur de recherche inutilisable. STACKIT : offre « sur demande », pas de prix. **Aucune conclusion négative n'est établie.**
4. **AMD SEV-SNP** : le livre blanc AMD a renvoyé une page HTML de 2,5 Ko (non lu) ; pas de documentation primaire AMD (même lacune que G4).
5. **Phala** : pays et entité juridique [abs] ; fournisseurs d'hébergement (« subprocessors ») non rendus par la page statique ; volume de bande passante « inclus » [abs] ; pages Trust incohérentes sur HIPAA ; rapport SOC 2 non ouvert ; `dcap-qvl` README : 404 ; l'audit date de mai-juin 2025 et exclut KMS et `dcap-qvl`.
6. **Marlin, Secret, iExec, Super Protocol** : aucun tarif ; Oasis : tarifs **mainnet** lus via l'indexeur public (non via la documentation), signification de `tee: 2` = TDX [inféré], frais de gaz et bande passante non lus ; reproductibilité du build ROFL non lue.
7. **AWS** : reproductibilité de l'EIF par `nitro-cli` non documentée dans les pages lues ; **horloge de l'enclave** non documentée ; aucun audit tiers du Nitro lu ; posture DRAM-interposeur non lue ; plans de support/KMS/CloudWatch non chiffrés.
8. **TLSNotary** : aucune consommation CPU/mémoire par session publiée ; direction exacte du trafic sortant du notaire non publiée (seul « prover uploads » est lu) ; la FAQ chiffre la charge d'après un protocole « planned for 2025 » (le billet 2026 donne ~30 Mo : cohérent).
9. **Jetons** : cours lus à un instant unique (03:22 UTC) sur CoinGecko ; PHA, ROSE, POND, SCRT, RLC ; aucune série historique lue.
10. **Vue acheteur et juridiction** : [inféré] partout (aucun texte DORA/eIDAS/SecNumCloud lu).
11. `github.com`/`api.github.com` : 403 (non contourné) : releases et dépôts non listés ; seul `raw.githubusercontent.com` utilisé.
12. Aucune mesure sur la session Shōgen ; aucune session réelle lancée (SHOGEN-E1-SESSION-CHAINE-1 n'est pas levé).

---

## 9. Traçabilité des copies (sha256, 16 premiers hex ; `tee/web/`)

| Copie | Condensat | Remarque |
|---|---|---|
| `phala_itypes.json` (API instance-types) | `b0d6a91e01f1c512` | prix Phala au centième |
| `phala_nodes.json` (API nœuds) | `ad20a77f1854420f` | 22 nœuds, 21 PPID |
| `phala_cloudpricing.raw` / `phala_pricing.raw` | `077361343d954c30` / `4060bcce5bc70fd4` | |
| `phala_compl.raw` / `phala_trust.raw` / `phala_cloudvsonchain.raw` / `phala_dstackcloud.raw` | `4cef16f979c237f2` / `b9c7667be73b06e0` / `a660e252b63b336f` / `026e4d9bad0669b1` | |
| `dstack_gh.raw` / `dstack_secmodel.raw` / `dstack_design.raw` / `dstack_audit.raw` | `5108b45f99d6a8b0` / `f8bab643c5a58b07` / `2f86152181aa81e9` / `4999598cf54c1782` | audit : PDF 39 p., créé 2025-06-28 |
| `aws_enc_nitro.raw` / `aws_enc_verify.raw` / `nitro_wp_intro.raw` | `05474fd203c266a8` / `64d366a2ef19084b` (identique à G4 `nitro_verify`) / `a075a190cdb24135` | |
| `aws_extract_eu-west-3_instances.txt` / `_storage.txt` / `aws_dt_eu-west-3.json` / `aws_vpc_eu-west-3.json` | `3631601b9a5fa186` / `82a7ea0269beb8ac` / `f0f774c5d90d6e90` / `64bccedb22a055aa` | extraits du Price List officiel |
| `gcp_cvm_price.raw` / `gcp_cs_pricing.raw` / `gcp_cs_overview.raw` | `7b260665c37d2fb6` / `9b9c5931d0d08b31` / `e1f5d733cd1184fc` | |
| `az_dc4_france.json` / `az_dcasv6.raw` / `az_attest.raw` | `1f60c529baa485df` / `3a293e9eec3294e6` / `0e801768b629d738` | |
| `stackit_server.raw` | `14466efaef7b92f0` | |
| `marlin_protocol_cvm_guarantees.raw` / `marlin_repro.raw` / `marlin_attest.raw` / `marlin_mono.raw` | `8f87d906a03efef3` / `b71568ba481ec2c2` / `e7e57de8bdbf5715` / `158840a19cbf5739` | |
| `oasis_offers.json` / `oasis_providers.json` / `oasis_inst.json` | `c029559ee3dd70aa` / `86ce1cf8d8ddad1b` / `a8bb65788c34c356` | |
| `coingecko_2026-10-04.json` | `6f9c9fc5a0e7203e` | |
| `tlsn_faq.raw` / `tlsn_blog_proxy.raw` (= G4) / `tlsn_where.raw` (= G4) / `tlsn_fastreveal.raw` | `70488ae3cfb896f7` / `55f38c32b22dcf11` / `90389f34b2aaf42a` / `6f2bb7eeeb9231af` | |
| `tlsn_crates_mpc-tls_src_follower_rs.raw` / `…leader_rs.raw` | `c56fea0594a60070` / `f50874abb292afbb` | `0fe3c32d`, `follower.rs` l. 32-33 et 235-241 ; `leader.rs` l. 297-300 |
| `teefail.raw` / `wiretap.raw` / `batteringram.raw` (= G4) / `ddrop.raw` | `90d624a736d3adfc` / `018da146f3a128fc` / `9b62976d86ec27f9` / `e7e65c391ba7ff6a` | |
| `secret_vm_hw.raw` / `secret_gcp.raw` / `secret_econ.raw` / `iexec_iapp.raw` / `super_home.raw` | `ae92ced513ac7eb8` / `f61a232657cea7e2` / `8ae168d6ab7b6bc1` / `e53a915f220539f5` / `fb7675999327b8dc` | |

Scripts : `tee/get.sh` (téléchargement), `tee/totxt.py` (HTML → texte), `tee/awsx.py`, `tee/awsy.py` (extraits du Price List AWS), `tee/azq.py` (API prix Azure), `tee/cost.py` (tous les calculs du §5), `tee/bing.py` (essai de recherche, résultats non exploités).
