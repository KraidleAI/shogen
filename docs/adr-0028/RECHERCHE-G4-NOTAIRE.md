# RAPPORT G4-RECHERCHE : notaire tiers pour les témoignages Shōgen (SHOGEN-G4-NOTAIRE-RECHERCHE-1 ; PX-Shogen-3 ; F-DP-35)

> *Note de versement de l'orchestrateur (2026-10-04)* : rapport versé tel que rendu, à une retouche typographique près : les citations anglaises de pages web **non versées à `biblio/`** (lues le 2026-10-04, copies hors dépôt) que la gate S-G5 signalait sont passées de « … » à “…” ; elles restent des lectures [lu] web, à verser à `biblio/` avant tout usage normatif (item SHOGEN-G4-BIBLIO-1).


Lecteur : `claude-sonnet-5-5` (effort `high` annoncé par la fiche ; l'effort n'est pas observable depuis la session, il est déclaré, pas constaté).
Dates : `date -u` en début de lecture = 2026-10-04 02:40 UTC ; toutes les lectures web ci-dessous sont du **2026-10-04** (02:40 à 02:55 UTC).
Brief : `g4/BRIEF-G4.md`, sha256 `6e4f5694…938f77e` recalculé et conforme.
Aucune installation. Aucun fichier suivi modifié. Aucune opération git. Pièces de la liste D.2, `docs/15-*`, `docs/16-*`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, `*.jsonl`, journaux de campagne : non ouverts (voir §0 pour un incident de grep à déclarer).

Étiquettes : [lu] lu sur place (URL ou fichier, date) ; [abs] absent de la source lue ; [2nd] seconde main ; [inféré] déduction du lecteur, à ne pas citer comme fait.

---

## 0. Déclarations de méthode (à lire d'abord)

1. **Incident de grep (exposition non voulue).** Mon premier `grep` sur `docs/adr-0028/*.md` (motifs `D9|G4|F-DP-35|PX-Shogen-3`) a imprimé deux lignes de `docs/adr-0028/AVIS-PRODUIT-APRES-S2.md` (l. 24 et l. 28 à 34) dont l'une contient un verdict sur l'état de R1 après S2. Je n'ai ni ouvert ce fichier ni exploité ces lignes ; rien de ce rapport n'en dépend. J'ignore si cette pièce figure en D.2 (je n'ai pas ouvert l'annexe D) ; à l'orchestrateur d'en juger et de consigner l'exposition si elle compte.
2. **Une commande refusée.** Une commande Bash (lecture de la réponse du proxy de session et de son README de diagnostic) a été refusée par le classifieur de permissions. Je n'ai pas cherché à la contourner ni à obtenir le même résultat autrement. Conséquence : pas de diagnostic du proxy ; les refus 403 de `github.com` / `api.github.com` restent inexpliqués (voir manques).
3. **Accès web.** `curl -sSL` seul, via le proxy de la session, sans contournement TLS. Les pages refusées sont listées au §6. Un moteur de recherche (duckduckgo) n'a pas répondu (connexion réinitialisée) : toute la recherche est par URL directe, donc **par construction non exhaustive** (un projet que je n'ai pas pensé à nommer n'est pas couvert).
4. **Pièces copiées** (hors dépôt) : `g4/web/` du scratchpad (copies brutes `.raw`, textes `.txt`, script `g4/get.sh`). Condensats courts des copies principales au §7.

---

## 1. Sources lues

### 1.1 Dans le dépôt (état de départ)

| Pièce | Ce que j'en tire | Niveau |
|---|---|---|
| `docs/17-modele-de-menace.md` l. 59, 65, 66 | T-01 : « le notaire, ou quiconque tient sa clé : ici tout lecteur du dépôt » ; T-07 : « aucune révocation consultée, le contrôle se faisant hors ligne [inféré] » ; T-08 : « instant antidaté par un notaire en collusion (T-01) » ; T-16 : ancre retenue pour le paquet = « jeton RFC 3161 sur `PAQUET.sha256`, OpenTimestamps en complément » | [lu] |
| `docs/03-temoignage.md` l. 32-35, 52-55, 81-90 | champs `transport`, `transport_proof`, `residual`, `attestor` (« identité(s) de l'attestateur/notaire/enclave impliqué, clés épinglées ») ; transports prévus `tlsn-mpc/1`, `proxy-witness/1`, `tee-sgx/1` ; chaque transport a son résidu | [lu] |
| `docs/08-assumptions.md` l. 15-20, 36-37 | A(notary-neutrality) : décharge « co-conduite du MPC par le vérificateur, ou quorum de notaires » ; A(self-attestation) : décharge « notaire tiers, ou quorum de notaires comptés en axe R2 (ADR-0004) » ; A(attestor-honesty), A(enclave-integrity), A(upstream-alpha) | [lu] |
| `docs/13-temoignage-e2e-design.md` §2-3 | forme déléguée retenue (compagnon `shogen-tlsn-verify`) ; `shogen-verifier` à zéro dépendance | [lu] |
| `docs/DECISIONS.md` ADR-0015 pt 3, 4, 5, 16 (l. 1675-1692 ; 1865-1869) | notaire opéré par Shōgen car le serveur notaire amont est arrêté ; pt 5 : TLS 1.2 seul, condition de bascule ; pt 16 : « la gestion de clé du notaire devient un objet à part entière » si la passe prétend à plus que la démonstration | [lu] |
| `adapters/shogen-tlsn-verify/Cargo.toml` | amont épinglé `rev = 0fe3c32d…`, version `0.1.0-alpha.16-pre` ; « les crates `tlsn*` N'EXISTENT PAS sur crates.io » | [lu] |
| `adapters/shogen-tlsn-verify/session/src/main.rs` l. 1-40, 86, 300-360 | prouveur et « Verifier acting as Attestor » = **deux tâches d'un même processus** reliées par un tube mémoire ; graine publique `GRAINE_DU_NOTAIRE` (l. 86, 331) ; branche `VerifierCommitStart::Proxy` **refusée** (ADR-0015 pt 1) ; signature `Secp256k1Signer` (k256) | [lu] |
| `adapters/shogen-tlsn-verify/src/main.rs` l. 20-30, 236-262 | contrôle (f) : la clé est lue **dans la présentation** avant `verify` ; sortie `attestor_cle_algorithme` / `attestor_cle_hex` | [lu] |
| `docs/adr-0028/ADR-0028-decisions-sortie-S2.md` D9 l. 229 ; §4 l. 258 ; `ANNEXE-B-items.md` l. 25 et 139 ; `G0-lots-apres-S2.md` l. 12 | G4-RECHERCHE = options, coût, intégration, risques, « aucune dépense » ; question à l'investisseur « G4 : accord et dépense si un notaire commercial est requis » ; SHOGEN-E1-SESSION-CHAINE-1 au G0 du premier lot G4 | [lu] |
| `docs/02-vision.md` l. 15 | « vérifiable offline par un tiers sans confiance dans Shōgen » | [lu] |
| `biblio/INDEX.md` l. 137-160 ; `biblio/tlsnotary-docs-notary-server-2026-08-12.html` ; `biblio/deco-2019.pdf` p. 1, 4 ; `biblio/reclaim-security-faq.html` | copies détenues relues sur place (voir 1.2 pour les citations) | [lu] |

### 1.2 Sources externes (primaires sauf mention)

| Source | URL / version | Lue le |
|---|---|---|
| TLSNotary : Introduction, FAQ, Proxy Mode, Notarization, Verification, Verifier Server, Rust Quick Start | `https://tlsnotary.org/docs/{intro,faq,protocol/proxy-mode,protocol/notarization,protocol/verification,extension/verifier,quick_start/rust}` (docs non versionnées) | 2026-10-04 |
| TLSNotary : billets 2026-04-22, 2026-05-10 (benchmarks proxy), 2026-06-17 (publicly verifiable), 2026-06-23 (where trust lives), 2026-01-19, 2025-08-31 | `https://tlsnotary.org/blog/…` | 2026-10-04 |
| Dépôt `tlsnotary/tlsn` : README, `crates/tlsn/Cargo.toml`, `crates/attestation/Cargo.toml`, exemple `attestation/README.md` | `raw.githubusercontent.com/tlsnotary/tlsn/main/…` (main au 2026-10-04 : `0.1.0-alpha.16-pre`) | 2026-10-04 |
| vlayer : docs plateforme (Web Prover Server, `/prove`, notary keys, audit), `book.vlayer.xyz`, docs Vouch, liste de clés, dépôt `notary-keys`, `Cargo.toml` du dépôt vlayer | `platform.vlayer.xyz/…`, `keys.vlayer.xyz/notary-keys.production.json`, `raw.githubusercontent.com/vlayer-xyz/{notary-keys,vlayer}/main/…` | 2026-10-04 |
| Veridise, *Audit Report: vlayer* (PDF 21 p., créé 2025-05-12 ; audit 2025-02-10 à 2025-03-21, commit a763614) | `https://platform.vlayer.xyz/audits/vlayer-audit.pdf` (identique octet pour octet à `book.vlayer.xyz/static/audits/audit-2025-q2-veridise.pdf`) | 2026-10-04 |
| Reclaim : docs, `attestor-core` README et `docs/avs.md` | `docs.reclaimprotocol.org`, `raw.githubusercontent.com/reclaimprotocol/attestor-core/main/…` | 2026-10-04 |
| Primus : « Understand Primus Network », « Attestor Security », « Overview of zkTLS » | `docs.primuslabs.xyz/primus-network/…` | 2026-10-04 |
| zkPass : Technical Overview (v2.0), Introduction | `docs.zkpass.org/overview/…` | 2026-10-04 |
| Opacity : page d'accueil seulement (docs en 403) | `https://opacity.network/` | 2026-10-04 |
| AWS Nitro Enclaves : concepts, “Verifying the root of trust”, page produit, whitepaper de conception | `docs.aws.amazon.com/enclaves/…`, `aws.amazon.com/ec2/nitro/nitro-enclaves/` | 2026-10-04 |
| Intel TDX : page d'aperçu | `intel.com/…/trust-domain-extensions/overview.html` | 2026-10-04 |
| TEE.fail (IEEE S&P '26), Battering RAM, WireTap (CCS '25) : pages officielles des auteurs | `tee.fail`, `batteringram.eu`, `wiretap.fail` | 2026-10-04 |
| RFC 3161 (texte), Rekor v2 GA (blog Sigstore, 2025-10-10), Rekor (doc Sigstore), OpenTimestamps (accueil, README du serveur de calendrier), FreeTSA | `rfc-editor.org/rfc/rfc3161.txt`, `blog.sigstore.dev/rekor-v2-ga/`, `docs.sigstore.dev/logging/overview/`, `opentimestamps.org`, `freetsa.org` | 2026-10-04 |
| DECO (Zhang et al., CCS '20, arXiv 1909.00938) | copie détenue `biblio/deco-2019.pdf`, p. 1 et 4 relues | 2026-10-04 |
| Registre crates.io (lecture seule, contrôle R-8 partiel) | `crates.io/api/v1/crates/{tlsn,tlsn-attestation,tlsn-core,aws-nitro-enclaves-nsm-api,aws-nitro-enclaves-cose,attestation-doc-validation,sigstore}` | 2026-10-04 |

---

## 2. Ce que les sources disent, par question

### 2.1 Le cadre fixé par l'amont TLSNotary (fondement de toutes les options)

- Un notaire est un vérificateur délégué : « A notary is just a verifier you didn't run yourself. » (billet 2026-06-17) [lu].
- La preuve n'est « vérifiable par tous » qu'au prix d'un notaire de confiance : « A zkTLS proof isn't checked by the world. It's checked by whoever trusts the verifier that witnessed it. » (même billet) [lu].
- Le « cadran de confiance » que l'amont décrit, du plus faible au plus fort (billet 2026-06-17) [lu] : exécuter le vérificateur soi-même ; un notaire réputé ; **plusieurs notaires indépendants (M-sur-N)**, chacun signant séparément, ce qui écarte la collusion prouveur-notaire avec un seul notaire ; notaires à enjeu économique (restaking), « not something TLSNotary ships itself » ; et un notaire MPC multi-parties qui serait « stronger still », mais « a multi-party MPC notary is not yet practical ».
- La page d'introduction dit la même chose pour la pluralité : « A data Verifier can also require signed data from multiple Notaries to rule out collusion between the Prover and a Notary. » (`docs/intro`) [lu].
- Le serveur notaire n'existe plus côté amont : « The Notary server was removed from the TLSNotary project in alpha.13. » et `notary.pse.dev` est arrêté (copie détenue de la page « Notary Server (Deprecated) », relue sur place) [lu]. La page est introuvable en direct aujourd'hui (404 sur `…/docs/notary/notary_server`) [lu].
- Le rôle survit en bibliothèque : « TLSNotary also supports a workflow where a Verifier (acting as Attestor) attests to the proven data. » (`docs/quick_start/rust`) [lu]. Le dépôt amont fournit en outre un « Verifier Server » HTTP/WebSocket (Rust) qui accepte aussi le mode proxy (`docs/extension/verifier`) [lu] ; il valide et émet des webhooks de transcripts rédigés, il ne publie pas de clé de notaire (champ [abs] sur cette page).
- Maturité : le README de `main` dit « should not be used in production. Expect bugs and regular major breaking changes. » ; `crates/tlsn/Cargo.toml` de `main` porte `0.1.0-alpha.16-pre`, **la même version que la révision épinglée** `0fe3c32d` [lu, 2026-10-04]. Le sha256 complet du README de `main` est identique à celui de la copie détenue du 2026-08-12 (INDEX) : inchangé en sept semaines ; idem pour `crates/tlsn/Cargo.toml` [lu]. Une sonde de balises `v0.1.0-alpha.16/17`, `v0.1.0-beta.1`, `v0.1.0`, `v0.2.0` sur `raw.githubusercontent.com` renvoie 404 ; `v0.1.0-alpha.15` existe [lu]. La liste des releases n'a pas pu être lue (403).
- Aucune page de `tlsnotary.org` lue (accueil, about, intro, FAQ, blogs cités, docs de protocole) ne mentionne un audit externe publié : le mot « audit » n'y figure que dans l'historique d'« Auditor (now called a Verifier) » [abs]. Je n'ai pas pu fouiller le dépôt (403) ni un moteur de recherche : **« aucun audit publié » n'est donc pas établi, seulement « non trouvé sur le site »**.
- Les crates `tlsn`, `tlsn-attestation`, `tlsn-core` n'existent toujours pas sur crates.io (HTTP 404, 2026-10-04) [lu] : la consommation reste git par révision (contrôle R-8 de l'adaptateur toujours valide).
- Surface protocolaire : MPC-TLS, TLS 1.2 ; la FAQ vivante porte deux énoncés sur TLS 1.3 (« on the roadmap » et « There are no immediate plans ») [lu] : divergence persistante (déjà consignée ADR-0015 pt 5). Le mode proxy prouve aussi la PRF TLS 1.2 (`docs/protocol/proxy-mode`) [lu].

### 2.2 Les options, une à une

**Option A : notaire opéré par un tiers indépendant, clé publiée par lui.**

- *vlayer* (seul exemple vérifié d'opérateur tiers de notaires TLSNotary avec clé publiée) [lu] :
  - « vlayer runs notary servers which notarize HTTP requests performed by calling /prove. » (`platform.vlayer.xyz/server-side/notary-keys`).
  - Liste de clés publiée, `schemaVersion 1`, `updatedAt 2026-09-24`, une clé secp256k1 (même courbe que `Secp256k1Signer` de la session Shōgen), `validFrom 2024-11-28`, `validUntil null`, URLs `notary.production.vlayer.xyz` et `notary.vlayer.xyz` (`keys.vlayer.xyz/notary-keys.production.json`).
  - Règle de vérification imposée par vlayer : faire correspondre l'empreinte de clé et exiger `validFrom <= tlsTimestamp < validUntil` ; “The list can contain concurrent keys during a rotation and retired keys needed to verify older proofs.” ; l'historique git du dépôt `notary-keys` est « the audit trail » (README du dépôt).
  - **Compatibilité de version défavorable** : l'API `/prove` renvoie `"version": "0.1.0-alpha.12"` et prend par défaut `notaryUrl https://notary.vlayer.xyz/v0.1.0-alpha.12` ; le `Cargo.toml` du dépôt vlayer épingle `tlsn … tag = "v0.1.0-alpha.12"` ; l'API est annoncée « Under Development … For production use, please contact our team » ; clé d'API requise ; `maxRecvData` ≤ 92160 [lu]. La pile Shōgen est épinglée à `0.1.0-alpha.16-pre`, après la suppression du serveur notaire (alpha.13) et sous « regular major breaking changes » : **une présentation vlayer alpha.12 n'est probablement pas lisible par `tlsn-attestation` à `0fe3c32d`** [inféré ; à trancher par un test sur fixture, sans installation de service tiers].
  - **Le notaire n'est pas dans le périmètre de l'audit publié** : Veridise (pagination PDF : p. 12, §4.1) pose en hypothèse « The vlayer labs TLSNotary Notary server will act honestly. » et classe les notaires approuvés parmi les rôles privilégiés ; le périmètre (§3.2, p. 5) est limité aux contrats Solidity et aux fichiers Rust fournis ; “Full validation of operational security practices is beyond the scope of this review” (p. 13) [lu]. L'audit est de février-mars 2025, sur le commit a763614 [lu].
  - Coût : non publié (« Book a call ») [abs].
- *Opacity* : le billet TLSNotary du 2026-06-17 cite Opacity Labs comme réseau de notaires à enjeu économique (restaking) bâti sur zkTLS [lu]. La page d'accueil lue aujourd'hui ne parle plus de zkTLS (« Tokenized Securities & TSV Technology », « reusable credentials ») et `docs.opacity.network` répond 403 : **aucune documentation de notaire accessible ; l'offre actuelle n'est pas établie** [lu pour la page ; [abs] pour le reste].
- *Opérateur tiers à définir (hors fournisseur commercial)* : institution partenaire, laboratoire, ou acheteur lui-même ; aucune source ne nomme de candidat. La page « Projects » de TLSNotary liste Keyring Network, Opacity Labs, Peer, Usher Labs, vlayer, Kapwork, ArchiveBox [lu] ; je n'ai lu aucun détail d'opérateur pour les autres.
- Dans tous les cas, la condition de l'amont est la même : « If a third party operates the Verifier, the Prover and the third-party Verifier must not collude » (`docs/protocol/proxy-mode`, valable pour le mode MPC d'après le billet du 2026-04-22) [lu].

**Option B : notaire en enclave attestée (SGX, TDX, SEV-SNP, Nitro).**

- Position de l'amont (billet 2026-06-23) [lu] :
  - une enclave “moves it from Peer to AWS, a far better-resourced and more accountable custodian” : amélioration d'intégrité contre un opérateur unique ;
  - « A measurement is a hash, not a meaning » : il faut les sources, une construction reproductible et le hash qui concorde ;
  - la racine est le fournisseur : « AWS is the root, unconditionally » ;
  - et la combinaison recommandée est « run the zkTLS verifier inside the enclave », la confidentialité restant du côté du prouveur. Pour Shōgen la confidentialité est sans objet (endpoints publics, sans clé : `session/src/main.rs` l. 20-25), seule l'intégrité compte.
- AWS Nitro Enclaves [lu] : un enclave « has no external network connectivity, and no persistent storage », ses CPU et sa mémoire “can't be accessed by the processes, applications, kernel, or users of the parent instance” ; le document d'attestation est signé par la PKI Nitro (autorité publiée), au format CBOR/COSE, avec PCR, clé publique et `user_data` ; “There are no additional charges for using AWS Nitro Enclaves other than the use of Amazon EC2 instances” (page produit). Le format COSE/CBOR est celui que le projet a retenu pour son enveloppe (ADR-0002) [inféré : synergie, non vérifiée].
- Intel TDX : “Attestation confirms that hardware and software configurations and policies are as expected” (page d'aperçu) [lu] ; je n'ai pas lu de documentation AMD SEV-SNP primaire.
- **Attaques physiques publiées sur la DRAM** [lu, pages des auteurs] :
  - TEE.fail (IEEE S&P '26) : extraction de clés d'attestation de TDX et de SEV-SNP avec Ciphertext Hiding, « including in some cases secret attestation keys from fully updated machines in trusted status » ; un quote TDX forgé est accepté par la bibliothèque DCAP d'Intel au niveau « UpToDate » ;
  - WireTap (CCS '25) : récupération de la clé ECDSA de la Quoting Enclave SGX et quote SGX forgé accepté (statut « SWHardeningNeeded », « best possible » pour le modèle de CPU) ;
  - Battering RAM : interposeur DDR4 « under $50 » ; Intel et AMD ont répondu que “physical attacks on DRAM are out of scope for their current products”.
  - Aucune de ces trois pages ne mentionne Nitro [abs] : je n'en déduis pas que Nitro est hors de cause.
- Conséquence pour le registre : l'enclave remplace A(self-attestation) par A(enclave-integrity), qui est déjà inscrit comme « hors de portée de Shōgen (matériel) » (`docs/08` l. 17) ; DECO le dit aussi : « If a single TEE is broken, TLS session content, including user credentials, can leak » (p. 3 de la copie détenue, pagination PDF ; confidentialité sans objet ici, intégrité visée) [lu].
- Qui opère l'enclave compte : si c'est l'équipe Shōgen, l'équipe choisit l'image et le compte cloud ; la garantie repose alors sur la reproductibilité de l'image (le projet a déjà la discipline D6 pour le vérificateur : A(verifier-binary), `docs/08` l. 35) et sur la vérification de l'attestation par l'acheteur [inféré].
- Horloge d'enclave : je n'ai trouvé nulle part comment `connection_info.time` serait daté dans un enclave Nitro ; je ne l'affirme pas (manque).

**Option C : pluralité (k-sur-n) de notaires.**

- Fondement amont : voir 2.1 (« Multiple independent notaries (M-of-N) … each notary signs on its own »). DECO le dit pour les oracles : « Smart contracts can further hedge against integrity failures by querying multiple oracles and requiring, e.g., majority agreement » (p. 4) [lu].
- Le registre l'appelle déjà décharge (`docs/08` l. 15 et 20) et ADR-0004 en fait un axe R2 : k témoignages agrégés, attestors comptés [lu].
- **Contrainte technique** : le protocole MPC-TLS est à deux parties (prouveur, vérificateur : « This requires two parties », `docs/extension/verifier`) ; un second notaire n'attestera donc pas *la même* session mais une **autre** session TLS, avec une réponse potentiellement différente (prix qui bouge) [inféré à partir des deux lectures]. Le « notaire MPC multi-parties » qui éviterait cela est « not yet practical » (billet 2026-06-17) [lu].
- Coût en bande passante, MPC : « ~30 MB of garbled-circuit material » à envoyer avant la poignée de main ; 3 à 15 s par attestation de 1 Ko / 2 Ko selon le réseau (billet 2026-05-10) [lu]. Illustration chiffrée **[inféré, hypothèse à contester]** : 11 sources × 1 session par minute × 30 Mo ≈ 330 Mo/min ≈ 475 Go/jour *par notaire* ; ce volume dépend du plan d'échantillonnage de S4, non décidé. Le mode proxy supprime ce poste (voir option E).

**Option D : réseaux de notaires ou de vérificateurs (projets zkTLS existants).**

| Projet | Ce que la source dit | Compatible avec la pile (`tlsn` épinglé) ? |
|---|---|---|
| Reclaim | « An "attestor" is a server that sits between the reclaim user & the internet » (README) ; protection contre un attestor compromis : « The only protection against fake proofs here is decentralisation or self-hosting of the attestor » (FAQ détenue, relue) ; décentralisation par un AVS Eigen, **exemple sur Holesky (chainId 17000)**, « Presently there is no claim fee » (`docs/avs.md`) [lu] | Non : implémentation TypeScript, mode proxy, format propre [inféré d'après le README] |
| Primus | nœuds attestors « inside a Trusted Execution Environment » (Phala), clés générées par le KMS dans la TEE ; mise en gage et pénalités ; **pénalités “not introduced on the first day of the mainnet”** ; “only authorized nodes will be allowed to join the network” en phase de démarrage ; modes MPC et proxy ; docs non datées (« Understand Primus Network », « Attestor Security ») [lu] | Non établi : protocole propre (QuickSilver, whitepaper non lu) |
| zkPass | mode hybride proxy + MPC ; le texte même dit que le mode MPC « still relies on a "trusted notary" … A malicious notary could cache session data and collude with a compromised client » ; « Decentralized MPC nodes verify data integrity before a proof is accepted » ; page « Get Started » « currently undergoing updates » [lu] | Non : protocole propre (VOLE-ZK) |
| vlayer | opérateur unique, voir option A | Version alpha.12 : à tester |
| Opacity | voir option A | Non établi |

Maturité commune [lu] : aucun de ces réseaux n'a publié de documentation que j'aie pu lire affirmant un audit du notaire ou de l'attestor lui-même ; le seul rapport trouvé (Veridise pour vlayer) exclut le notaire de son périmètre. Les pièces sont des pages marketing ou de documentation non datées ; aucun cadre de gouvernance opposable à un acheteur institutionnel n'y est décrit.

**Option E : mode proxy (TLSNotary).**

- Fonctionnement [lu] : le vérificateur est un proxy réseau entre le prouveur et le serveur ; il transmet le trafic chiffré, puis valide une preuve à divulgation nulle. « Running the Verifier yourself is sufficient to rule out collusion » ; reste « the network path between the Verifier and the Server » (détournement DNS ou BGP) ; si un tiers opère le vérificateur, « the Prover and the third-party Verifier must not collude ». Le serveur voit l'adresse IP du vérificateur, pas celle du prouveur ; pas de vérification aveugle (`docs/protocol/proxy-mode`, billet 2026-04-22).
- Performance [lu] (billet 2026-05-10) : 1 à 2 s pour 1 Ko / 2 Ko sur profils résidentiels et mobiles, contre 3 à 15 s en MPC ; pas de préchargement de circuits ; « full-reveal fast path » (clé d'écriture serveur remise au vérificateur quand toute la réponse est révélable) mentionné mais exclu des mesures : c'est le cas de Shōgen (la session révèle « la totalité » du transcript, `session/src/main.rs` l. 17-19).
- Dans la pile actuelle : la branche proxy existe dans l'amont épinglé (`VerifierCommitStart::Proxy`) mais la session la **refuse** (ADR-0015 pt 1 : le transport est `tlsn-mpc/1`). Activer le proxy serait un autre transport avec un autre résidu (cf. `docs/03` l. 53, `proxy-witness` : A(attestor-honesty)) : décision d'ADR, pas un réglage [inféré].
- Pour une source publique sans clé, le seul avantage du MPC (aveuglement du vérificateur et de la source) est sans objet ; l'amont le dit : pour les données publiques, « a less-resource-intensive man-in-the-middle approach is more economical » (FAQ) [lu]. **Le mode proxy tenu par un tiers est donc un témoin réseau plausible pour Shōgen**, avec l'hypothèse de chemin réseau en plus [inféré].

**Option F : horodatage externe et transparence (RFC 3161, Rekor, OpenTimestamps).**

- RFC 3161 : “A time-stamping service supports assertions of proof that a datum existed before a particular time.” (§1) [lu]. C'est une **borne supérieure** (« existait au plus tard à T »), pas une preuve de l'instant d'observation.
- Rekor v2 : GA le 2025-10-10 ; “The log no longer returns signed timestamps with proofs. Sigstore clients will fetch a signed timestamp from a dedicated service” ; instance publique « 99.5 % » de disponibilité, journal auditable par des moniteurs (blog Sigstore ; doc Rekor) [lu]. Crate `sigstore` 0.14.0, Apache-2.0, 1 048 851 téléchargements, mise à jour 2026-05-22 (contrôle R-8 partiel) [lu].
- OpenTimestamps : ancrage Bitcoin, calendriers gratuits « rely on donations » [lu].
- FreeTSA : TSA gratuite ; certificat renouvelé le 2026-03-16 (validité jusqu'en 2040) [lu] ; le projet l'a déjà retenue pour le paquet (`docs/17` l. 107 : jeton RFC 3161 et OpenTimestamps ; vérification `openssl ts -verify`) [lu]. Aucun TSA commercial ni qualifié eIDAS lu (voir manques).

### 2.3 Effets par option sur T-01, T-07, T-08 (analyse du lecteur, [inféré] sauf mention)

| Option | Retire de T-01 | Laisse de T-01 | T-07 (racines figées, pas de révocation) | T-08 (instant antidaté) |
|---|---|---|---|---|
| A tiers indépendant, clé à lui | la clé de démonstration publique (n'importe quel lecteur du dépôt ne peut plus signer) ; A(self-attestation) disparaît, la clé n'est plus dans le code | collusion prouveur-notaire (le prouveur est Shōgen) ; compromission de la clé du tiers ; neutralité non vérifiable pour un tiers : A(notary-neutrality) reste, nommée | inchangé (le contrôle de certificat reste hors ligne) | inchangé : l'instant est celui du notaire ; seul un tiers de confiance le date |
| B enclave attestée | signature arbitraire par l'opérateur ; extraction de la clé par l'opérateur (si l'attestation lie la clé à l'image) | opérateur qui choisit l'image si l'acheteur ne rejoue pas la construction ; racine du fournisseur ; attaques physiques sur TDX, SEV-SNP, SGX ; défaut du code notaire alpha | inchangé | dépend de la source d'heure de l'enclave : non établi ici |
| C k-sur-n indépendants | collusion avec un seul notaire | collusion de k notaires ; sessions distinctes, donc témoignages distincts (à intégrer à l'agrégation ADR-0004) ; indépendance réelle des opérateurs (même cloud, même code amont) à mesurer, pas à déclarer (`docs/08` l. 15) | inchangé | un notaire honnête suffit à contredire un instant s'ils sont comparés (non spécifié aujourd'hui) |
| D réseaux | selon le projet : opérateurs multiples, mise en gage | pénalités absentes au démarrage (Primus) ; format incompatible ; gouvernance et audits non lisibles | inchangé | inchangé |
| E mode proxy tiers | rien de plus que A | hypothèse de chemin réseau (DNS, BGP) en plus ; le tiers voit le trafic chiffré | le tiers pourrait valider le certificat en direct (révocation) : **non fait par l'amont** [lu : `Presentation::verify` hors ligne] | inchangé |
| F horodatage et journal | ne retire pas T-01 (une attestation forgée peut être horodatée) ; borne la fenêtre de forge a posteriori d'une clé compromise ou retirée : une attestation sans jeton antérieur à la rotation est suspecte ; empêche la substitution silencieuse d'un lot publié (journal ajout seul) | tout ce qui précède | l'instant validé devient « au plus tard T » avec une source externe | **retire l'antidatage au-delà de la fenêtre** si Shōgen (et non le notaire) obtient le jeton au moment de la collecte et si une fenêtre de fraîcheur compare `connection_info.time` au `genTime` ; ne dit rien sur un instant postdaté sur le plan de la vérité du prix |

### 2.4 Maturité, coût, compatibilité, dépendances (R-8)

| Option | Maturité (lu) | Coût et latence (lu, sinon [inféré]) | Compatibilité avec `adapters/shogen-tlsn-verify` | Dépendance nouvelle, R-8 : contrôle de registre avant installation, rien installé |
|---|---|---|---|---|
| A tiers, service (vlayer) | service en production selon l'éditeur ; API « Under Development » ; audit Veridise 2025 hors notaire | prix non publié ; clé d'API ; latence non publiée | **à tester** : alpha.12 contre alpha.16-pre | aucune côté pile si le tiers fournit la présentation ; en pratique, un second binaire amont à une autre révision serait nécessaire [inféré] |
| A tiers, opérateur du code Shōgen | code `session` scindé en demi-prouveur et demi-notaire ; aucune réalisation ; amont alpha | héberger un service Rust ; bande passante MPC (option C) [inféré] | **totale par construction** (même révision épinglée des deux côtés) | transport réseau entre prouveur et notaire (aujourd'hui tube mémoire) : la session a déjà `tokio`, `tokio-util` ; le Verifier Server amont montre un schéma WebSocket [lu] ; crate éventuelle à contrôler au registre au moment du lot |
| B enclave Nitro | fonctionnalité AWS ancienne ; attestation COSE documentée ; physique : cf. 2.2 | aucun supplément AWS au-delà de l'instance EC2 [lu] ; prix de l'instance non lu | compatible si l'enclave exécute la même demi-notaire ; clé liée à l'attestation : conception à faire | `aws-nitro-enclaves-nsm-api` 0.5.2 (Apache-2.0, 4 926 714 téléchargements, maj 2026-07-08) ; `aws-nitro-enclaves-cose` 0.6.0 (Apache-2.0, 1 297 251, maj 2026-10-02) ; `attestation-doc-validation` 0.10.1 (Evervault, Apache-2.0, 326 085, maj 2026-08-14) : existence et licence lues, **propriétaires, yanked par version, avis RUSTSEC non vérifiés** : contrôle R-8 complet à faire |
| C k-sur-n | principe décrit par l'amont et DECO ; aucun outil prêt | k sessions MPC : k × coût de A | l'agrégation existe en conception (ADR-0004), pas en code | selon A |
| D réseaux | alpha ou démarrage selon les propres docs | jetons, frais de tâche (Primus) ; autres non lus | non pour Reclaim, Primus, zkPass | hors pile : SDK TypeScript ou autres, jamais dans le vérificateur (ADR-0015 pt 6) |
| E proxy | amont : proxy mode annoncé 2026-04-22, benchmarks 2026-05-10, alpha | 1 à 2 s, bande passante faible (lu) | branche présente dans la révision épinglée, refusée par la session ; nouveau transport à déclarer | aucune nouvelle crate à ce niveau |
| F horodatage | RFC 3161 standardisé ; Rekor v2 GA 2025-10-10 ; OTS en production depuis des années | FreeTSA gratuit ; OTS calendriers gratuits ; latence OTS non lue ; TSA commerciaux non lus | indépendant du transport ; `openssl ts` déjà dans la chaîne du paquet | aucune pour RFC 3161 (outil système déjà utilisé) ; `sigstore` 0.14.0 si Rekor (contrôle R-8 complet à faire) |

### 2.5 Ce qu'un acheteur institutionnel exigera de la preuve tierce [inféré sauf indication] (question 2)

Aucune pièce lue ne décrit les exigences d'un acheteur institutionnel (les textes DORA et eIDAS n'ont pas pu être lus, voir manques). Ce qui suit est déduit de ce que les sources montrent sur la structure de la confiance, et à contester :

1. **Séparation des rôles** : le collecteur (Shōgen), l'opérateur du notaire et le consommateur du verdict sont trois entités distinctes ; pas de compte cloud, pas de clé, pas de poste partagés ; l'acheteur peut vérifier cette séparation, pas seulement la lire. Le billet 2026-06-17 donne la règle de fond : pour convaincre « anyone else, they have to trust whoever the verifier was » [lu].
2. **Clé hors de l'équipe**, produite et gardée par l'opérateur ou dans l'enclave, jamais dans un dépôt ; publication datée avec fenêtre de validité, rotation et retrait consignés, historique ajout seul : c'est le patron que vlayer publie [lu] et que ADR-0015 pt 16 annonce pour Shōgen.
3. **Attestation vérifiable par lui-même, hors ligne** : le compagnon et `shogen-verifier` rejouent déjà le contrôle sans réseau ; il faudrait y ajouter l'appartenance de la clé à la liste publiée à l'instant de connexion (règle vlayer) ; et, pour une enclave, l'attestation et les PCR rejouables contre une construction reproductible. Un « signe Veridise » ne suffit pas : l'audit lu **exclut** le notaire [lu].
4. **Journal public** des attestations et des jetons d'horodatage (RFC 3161 ; transparence type Rekor), de sorte qu'aucune substitution après coup ne passe inaperçue.
5. **Contrôles de l'opérateur opposables** : rapport d'assurance, plan de continuité, sortie de contrat, juridiction : le registre DORA des prestataires TIC tiers est cité par l'avis produit du dépôt (`ADR-0028` D9 (ii), « DORA art. 29 ») mais le texte n'est pas détenu : [inféré, non détenu].
6. **Réplicabilité** : l'acheteur peut être lui-même un notaire (« be the verifier »), ce que la source dit être sans confiance pour lui seul [lu : billet 2026-06-17].

---

## 3. Recommandation

### 3.1 Option principale : « notaire tiers indépendant à clé publiée, exécutant la révision épinglée de Shōgen, avec ancrage externe »

Composition (aucune dépense pour les trois premières étapes ; aucun code dans ce lot, qui est de recherche) :

1. **Étape 1, sans dépense : décider le contrat d'interface avant de choisir l'opérateur.** Écrire (G0 du futur lot G4, ADR) : (a) un format de liste de clés de notaires datée, avec `validFrom`/`validUntil`, empreinte SHA-256 de la clé compressée, historique git ajout seul, sur le patron de `vlayer-xyz/notary-keys` [lu] ; (b) la règle de vérification « clé dans la liste et `connection_info.time` dans la fenêtre » comme **contrôle nouveau** du compagnon ou du vérificateur (aujourd'hui le contrôle (f) compare la clé de la présentation au champ `attestor` du même faussaire, T-01) ; (c) les deux résidus à écrire au registre 08 : A(notary-neutrality) maintenu, A(self-attestation) retiré uniquement quand l'opérateur est hors équipe.
2. **Étape 2, sans dépense : scinder en conception la session** (prouveur Shōgen / vérificateur-attestor tiers) sur la **même révision** `0fe3c32d`, ce qui évite le problème alpha.12 / alpha.16-pre d'un notaire commercial ; le notaire tiers génère et garde sa clé. Le rôle « Verifier acting as Attestor » est un rôle de bibliothèque que l'amont documente encore [lu].
3. **Étape 3, sans dépense : ancrer chaque lot collecté** par un jeton RFC 3161 demandé par Shōgen à la collecte (pas par le notaire), selon la même chaîne que le paquet (`openssl ts`), et publier les empreintes dans un journal ajout seul (un dépôt public suffit au début ; Rekor v2 en option). Cela couvre T-08 au-delà d'une fenêtre et borne les forges a posteriori.
4. **Étape 4 : choisir l'opérateur** parmi, par ordre de préférence [inféré] : un acheteur ou partenaire de conception qui exécute le vérificateur (« be the verifier » pour lui) ; une institution ou un laboratoire indépendant ; un fournisseur commercial. Un second opérateur indépendant ensuite (k = 2), en comptant les opérateurs comme axe R2 (ADR-0004 ; `docs/08` l. 15 : « mesuré, pas déclaré »).

Raison : c'est la seule option qui change le signe de A(self-attestation) tout en restant compatible avec la pile épinglée ; elle s'appuie sur les décharges déjà écrites au registre (`docs/08` l. 15 et 20) et sur le cadran décrit par l'amont [lu].

### 3.2 Option de repli : « notaire en enclave Nitro opéré par Shōgen, image reproductible, attestation publiée », plus les mêmes ancrages

À retenir si aucun opérateur tiers n'est trouvable à temps. Elle supprime la clé en clair, la signature à volonté par l'opérateur, et laisse A(enclave-integrity) (racine AWS, attaques physiques sur DRAM pour les TEE x86 ; non établi pour Nitro), plus le fait que l'opérateur est toujours Shōgen : **le verdict doit continuer à dire que le notaire est auto-opéré**, avec le résidu réduit mais nommé. Gain mesurable seulement si l'acheteur rejoue la construction et l'attestation. Coût d'infrastructure : une instance EC2 sans supplément Nitro [lu] ; contrôle R-8 des crates d'attestation à compléter avant tout lot.

### 3.3 Ce que je ne recommande pas, avec sa raison

- **Réseaux de notaires (D)** comme premier pas : formats incompatibles avec le compagnon, pénalités non actives au démarrage chez Primus, documentation datée et incomplète, aucun audit du notaire lu.
- **Un notaire commercial sur alpha.12 (vlayer)** sans test de lisibilité : probable incompatibilité de version (cf. 2.2). À sonder, pas à adopter. Son audit ne couvre pas le notaire.
- **Mode proxy (E)** comme transport par défaut : plausible pour des sources publiques et utile pour le volume (cf. 475 Go/jour illustratifs en MPC), mais c'est une décision d'ADR (nouveau transport, nouveau résidu) ; à instruire avec A, pas à y substituer.

### 3.4 Questions à l'investisseur (aucune n'engage de dépense avant réponse)

1. **Autorisation de contacter** vlayer, l'équipe TLSNotary (PSE) et au moins un acheteur ou partenaire potentiel : quel opérateur tiers accepterait de tenir une clé de notaire, à quelles conditions, et pour quel prix ? (D9 §4 pt 6 : « G4 : accord et dépense si un notaire commercial est requis ».)
2. **Partenariat** : accepte-t-il qu'un acheteur nommé exécute le vérificateur sur des sessions de collecte (partage de l'horaire et des endpoints, pas des données privées : elles sont publiques) ?
3. **Budget borné** pour l'option de repli (instance cloud) et, le cas échéant, un fournisseur commercial : plafond, durée.
4. **Mode proxy** : accepte-t-il d'ouvrir l'instruction d'un transport `tlsn-proxy/1` (nouveau résidu) pour réduire le volume ?
5. **Périmètre de promesse** : tant que A(self-attestation) n'est pas retiré, le message public doit-il rester « démonstratif » (T-01 le dit déjà) ?

---

## 4. Premières étapes concrètes (sans dépense, dans l'ordre)

1. Faire un test de lisibilité **sur fixture** : si un fournisseur remet une présentation d'exemple, la passer au compagnon (aucune installation de service tiers). Sans exemple, la question reste ouverte.
2. Rédiger le G0 du lot G4 : liste de clés (format, règle de fenêtre), scission du `session`, nouveau contrôle d'appartenance, résidus, et reprise de SHOGEN-E1-SESSION-CHAINE-1 (`deny.toml`, job, test de la session : T-09).
3. Contrôle R-8 complet des crates candidates (propriétaires, yanked, avis RUSTSEC) si l'option repli est retenue ; `tlsn*` : toujours git seulement (404 registre le 2026-10-04).
4. Décider la règle de fraîcheur qui consomme les jetons (PX-Shogen-4, T-03 et T-08).

---

## 5. Table de rattachement aux menaces

| Menace | Option qui l'adresse | Résidu après l'option principale |
|---|---|---|
| T-01 clé de démonstration publique | A (clé du tiers, hors dépôt) ; B en repli | collusion Shōgen et tiers ; clé du tiers compromise ; neutralité non vérifiable : A(notary-neutrality) |
| T-01 notaire malveillant | C (k ≥ 2 indépendants) ; F (fenêtre de forge a posteriori) | collusion de k notaires ; indépendance à mesurer |
| T-07 racines et révocation | aucune des options ne le retire ; F précise « au plus tard T » | A(root-store) intact : SHOGEN-E1-RACINES-1 |
| T-08 horloge du transport | F (jeton de collecte obtenu par Shōgen) ; C par comparaison | postdatage non traité par F ; horloge d'enclave non établie |

---

## 6. Manques (rendus à l'orchestrateur, non comblés)

1. `github.com` et `api.github.com` : HTTP 403 (releases et dépôt de TLSNotary, GitHub d'Opacity, dépôts Primus), et `gh` : “GitHub access to this repository is not enabled for this session”. Conséquences : liste des releases de `tlsn` non lue ; état d'un éventuel dossier d'audit ou d'un `SECURITY.md` amont non établi (404 sur `main` pour `SECURITY.md` et `CHANGELOG.md`) ; audit de `mpz` non cherché hors de l'URL du README (200, non exploité).
2. Moteur de recherche inaccessible (duckduckgo : connexion réinitialisée) : exhaustivité non garantie ; aucun audit de TLSNotary n'a été *cherché* au-delà du site officiel.
3. `docs.opacity.network` : 403 ; page d'accueil lue : produit actuel autre ; offre notaire non établie. `docs.primus.xyz` : 502 (le domaine primuslabs.xyz a été lu à la place) ; whitepapers (Primus, Reclaim, zkPass) non lus.
4. EUR-Lex (eIDAS art. 41-42, DORA art. 28-30) : réponse HTTP 202 avec défi anti-robot (WAF) ; **non contourné** : les exigences institutionnelles du §2.5 restent [inféré], et le lien « horodatage qualifié eIDAS » n'est pas instruit.
5. Non lus : documentation AMD SEV-SNP primaire ; reproductibilité des images Nitro (EIF) ; source d'heure d'un enclave Nitro ; prix d'une instance EC2 compatible ; prix d'un TSA commercial ; prix de vlayer ; latence OpenTimestamps.
6. Compatibilité alpha.12 / alpha.16-pre : déduite des numéros de version et de l'avertissement « regular major breaking changes », **jamais testée**.
7. T-07 : aucun mécanisme de révocation vérifié dans les options (le compagnon vérifie hors ligne).
8. Le chiffre de 475 Go/jour est une illustration arithmétique à hypothèses déclarées, pas une mesure.
9. Les crates `aws-nitro-enclaves-*`, `attestation-doc-validation`, `sigstore` : existence, version et licence lues ; **propriétaires, yanked par version, avis non vérifiés** (R-8 incomplet).
10. Aucune audition ni source sur « qui accepterait d'être notaire tiers pour Shōgen » : la recherche d'opérateur est une étape 4, pas un résultat.

---

## 7. Traçabilité des copies (sha256, 16 premiers hex)

| Copie (`g4/web/`) | Condensat |
|---|---|
| `vlayer_keys.json` (liste de clés du 2026-09-24) | `6db2bcff750c1e17` |
| `veridise.pdf` (rapport d'audit, 707 142 octets) | `4910e9173db223d3` |
| `tlsn_readme.raw` (README `tlsn` main) | `b95e34f3c6315d55` (sha256 complet identique à l'INDEX du 2026-08-12) |
| `intro.raw` | `2c8e81d8bb327b96` |
| `blog_2026_06_17_public-verifiability.raw` | `117677327eecca65` |
| `blog_2026_06_23_where-trust-lives.raw` | `90389f34b2aaf42a` |
| `docs_protocol_proxy-mode.raw` | `4c572855b21c534c` |
| `blog_2026_05_10_blog-proxy-mode.raw` | `55f38c32b22dcf11` |
| `vl_prove.raw` | `0c83d3f3fb8818d8` |
| `getvouch_wp.raw` | `319c7243bfe0cf29` |
| `rfc3161plain.raw` | `39fd17644ff2d654` |
| `reclaim_avs.raw` | `3a4aa9eb0c02a00f` |
| `primus_understand-primus-network.raw` | `318bc1a2feca5148` |
| `primus_attestor-security.raw` | `4e8df2c34484fbac` |
| `zkp_tech.raw` | `0916037e311ee862` |
| `teefail.raw` / `batteringram.raw` / `wiretap.raw` | `90d624a736d3adfc` / `9b62976d86ec27f9` / `018da146f3a128fc` |
| `nitro_verify.raw` | `64d366a2ef19084b` |
| `rekorv2.raw` | `3acb6cbb365925eb` |
| `tlsn_crate.raw` (`crates/tlsn/Cargo.toml` main) | `ed9bc7d226bc34ea` (sha256 complet identique à `tlsn-crate-tlsn-cargo-toml-2026-08-12.toml` de l'INDEX : manifeste inchangé) |
