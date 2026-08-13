# S3 — le témoignage de bout en bout : conception de passe (2026-08-12)

> Statut : conception écrite à l'ouverture de la passe, sur sources détenues
> uniquement ; ce que la passe doit encore établir est marqué « à établir en
> phase A/B ». Régie par le corpus « Compliance et ingénierie logicielle et
> architecturale » (doc 02 : G0–G7, R-1..R-25 ; doc 03 : méthodologie de
> passe). Prédécesseur : S2.5 close le 2026-08-12 (12 §11), critère atteint,
> « S3 peut commencer ».

## 1. Périmètre — ce que S3 est, et n'est pas

**L'objet** (05 §S3) : le premier chemin complet sur UN transport —
source réelle → témoignage canonique → vérification offline par un binaire
séparé qui nomme le résidu. Candidat de transport nommé par la roadmap :
TLSNotary (open source, résidu documenté : A(notary-neutrality),
A(verifier-designation) — 08, résolus depuis le 2026-07-30).

**Le critère de sortie, binaire (05 §S3, repris à la lettre)** : une
commande `shogen verify <lot>` retourne « valide sous
A(notary-neutrality) » sur un témoignage réel, et échoue (fail-closed,
raison structurée) sur les 3 mutants semés : preuve altérée, hash
d'utterance faux, résidu non résolu. *(La règle gatewright : un
vérificateur qui n'a jamais rejeté n'a rien montré.)* S'y ajoutent les
échéances contractées du §3 — elles sont dans le critère parce qu'elles
sont contractées, pas parce que S3 les invente.

**Non-objets** : le verdict de quorum, l'estimateur de confinement, le
certificat embarqué, l'interface `gather` (tout cela est S4) ; la
publication académique (S5) ; tout transport au-delà du premier (ADR-0001 :
les transports sont des adapters — S3 en branche UN et prouve l'interface,
pas la collection) ; le calcul de partition k_eff (la migration de la règle
ADR-0008 en propriété du cœur est due « à l'atterrissage du calcul de
partition », ADR-0011 registres — si la partition n'atterrit pas en S3,
la migration n'est pas due).

## 2. L'objet technique — le chemin, pièce par pièce

Le squelette S2.5 marche déjà de bout en bout sur un témoignage trivial
(lot → CBOR canonique manuel → `shogen-verifier` séparé, fail-closed à
résidu nommé, vert CI Windows+Linux, run `31645277610`). S3 remplace le
trivial par le réel, sans casser ce qui est tested :

1. **L'adapter transport** (`adapters/`) : conduit une session attestée
   contre une source réelle du pool S2 (11 endpoints publics, 10 §2) via
   le transport choisi par ADR-0015, et produit la forme canonique 03 §1
   — les 7 champs, dont `transport_proof` (opaque pour Shōgen) et
   `residual` (résolu dans 08). Testé, jamais prouvé (ADR-0001).
2. **Le cœur** (`shogen-core`) : la forme canonique complète en CBOR
   déterministe (RFC 8949, ADR-0002) — extension des champs du squelette
   vers les 7 champs de 03 §1 ; le prédicat de canonicité de `subject` (ADR-0016 C10) et la liaison hash d'utterance (ADR-0005
   règle 1 : « le hash des octets exacts est toujours porté — il lie le
   témoignage à sa preuve de transport ») entre au cœur — c'est la charge
   utile que les 37 mutations acceptées de S2.5 attendaient (« liaison
   hash = S3 », JOURNAL phase C).
3. **Le vérificateur** (`shogen-verifier`) : les trois contrôles de 03 §4
   — (1) `transport_proof` vérifié avec l'outil du transport contre les
   clés épinglées d'`attestor` (sous A(verifier-designation) pour les
   transports à vérificateur participant), (2) hash d'`utterance`
   correspond, (3) `residual` résout dans le registre publié. Verdict :
   « valide sous A(...) » — jamais « vrai ». Fail-closed, raison
   structurée, sur chaque contrôle.
4. **Le typeur** (adapter) : A(typer-correctness) porte « cible : tested à
   S3, avec compte d'itérations par typeur » (08, résidus de couche) — un
   premier typeur (JSON → fait prix typé) atteint *tested* dans la passe ;
   l'extraction reste hors témoignage (03 §3 : l'identité du typeur va
   dans le fait, pas dans le témoignage).

**Tension à instruire, pas à improviser (ADR-0015)** : le contrôle (1)
exige l'outil de vérification du transport dans le binaire vérificateur —
or `shogen-verifier` est à zéro dépendance (S2.5) et vise `no_std` + gate
à S3 (ADR-0009 pt 6). Trois formes possibles, à instruire sur pièces :
vérification du transport embarquée (dépendance entrant par revue R-8,
coût sur le graphe), déléguée à un binaire du transport invoqué à côté
(le vérificateur Shōgen vérifie alors la chaîne hash→proof et nomme ce
qu'il n'a PAS vérifié lui-même), ou frontière `no_std` repositionnée
(cœur `no_std`, vérificateur std) — chaque forme a un coût de résidu
différent et ADR-0015 le chiffre.

*(Close le 2026-08-13 par ADR-0015 : forme déléguée retenue — binaire
compagnon `shogen-tlsn-verify` hors workspace, `shogen-verifier` maintenu
à zéro dépendance, `no_std` en gate confirmé dû tel quel ; la « frontière
repositionnée » requalifiée en pré-condition de la forme embarquée, pas en
troisième forme. Résidus nouveaux au registre 08 : A(self-attestation),
A(transport-check-delegated), A(upstream-alpha).)*

## 3. Les échéances contractées qui arrivent à S3

Chacune a son contrat écrit ; aucune n'est optionnelle (G5, règle du
2026-08-05) :

| # | échéance | contrat | véhicule S3 |
|---|---|---|---|
| 1 | ~~**Licence du dépôt**~~ — **soldée le 2026-08-13 par ADR-0017** : « MIT OR Apache-2.0 » uniforme, décidée sur délégation explicite du mainteneur (dossier d'instruction : docs/14 ; textes en racine, champ au workspace, deny inchangé vert) | fermé |
| 2 | **Passage public + purge `biblio/`** | DEVOPS §1 : « privé de S0 à S2, public à S3 », calé sur l'existence du vérificateur ; « `biblio/` ne va PAS dans le dépôt public » (AUDIT-ENTREE G6 : jamais public sans purge) | phase E — décision mainteneur (le moment exact lui appartient) ; la purge et le contrôle `.gitignore`/historique sont une unité orchestrateur AVANT tout passage |
| 3 | ~~**`no_std` du vérificateur en gate**~~ — **tenue le 2026-08-13 (phase C vague 1)** : `shogen-core` et la bibliothèque de `shogen-verifier` (scission lib `no_std`+`alloc` / coquille `std` mince) construisent pour `thumbv7em-none-eabi` dans `cargo xtask verify` et en CI ; contrôle négatif fait (`use std::` → E0433 rouge) | ADR-0009 pt 6 : « `#![no_std]` + `alloc` devient une gate en S3 » — ADR-0015 pt 6 l'a maintenue telle quelle | fermé (gate dans `verify`, hors numérotation S-Gn comme D6) |
| 4 | ~~**Score de mutation ≥ 80 % du cœur**~~ — **tenue le 2026-08-13 (phase C vague 1)** : 94,2857 % mesuré (417 mutants, 363 tués, 22 survivants tous justifiés une-ligne dans `crates/shogen-core/survivants.txt`, 32 non viables, dénominateur non-équivalents 385) ; gate `cargo xtask mutation` + `mutation.yml` (PR `--in-diff` ≤ 10 min, nightly complet — le run complet mesure 12 min 12 s à parallélisme 4 déclaré, la scission est donc la seule forme qui tienne le contrat) | ADR-0011 seuil 3, régime deux temps : « dès la logique (S3) », mutants non équivalents (Jia & Harman p. 4), chaque survivant justifié en une ligne | fermé (R-8 cargo-mutants fait AVANT installation le 2026-08-13 — la mention « fait en S2.5 » de cette table était inexacte, cf. docs/R-8-outillage.md) |
| 5 | ~~**Fuzz du vérificateur**~~ — **tenue le 2026-08-13, mot « instrumenté » compris** : harnais en arbre (900 s = 678 528 272 cas, zéro panique) PLUS les deux moteurs guidés par la couverture ratifiés par le mainteneur — libFuzzer sur nightly-2026-08-10 épinglée (74 595 254 exécutions en 11 min, zéro panique) et AFL++ 4.40c sur la stable (28 200 402 exécutions cumulées en deux campagnes, zéro plantage zéro blocage) ; workspace `fuzz/` (deny local vert, NCSA bornée), jobs CI aux budgets ratifiés, revue G2 dédiée (1 bloquante + 6 majeures + 5 mineures, toutes fermées) | ADR-0011 seuil 7 : zéro panique sur toute suite d'octets (binaire, non négociable) ; budgets ratifiés ≥ 15 min CI, ≥ 4 h nightly, corpus committé croissant | fermé (chantier `wf_3b4417e1-26f` adjugé + revue `wf_6603a162-bc6` fermée ; premier run réel des jobs = donnée à surveiller au push) |
| 6 | **Build L2 + double-build D6** | ADR-0012 : Build L2 à S3 ; dette 12 §10 item 3 : D6 (6 variations, bit-à-bit Linux d'abord) — « orchestrateur + shogen-devops, après ratification » (ratification faite) | unité dédiée, avec l'attestation de build sur le vérificateur (DEVOPS §7 pt 6) |
| 7 | **Gates S-G4/S-G5/S-G6/S-G8** | dette 12 §10 item 2 : gates documentaires (docs/, biblio/, journal), « unité orchestrateur, après ratification » | unité orchestrateur, tôt dans la passe (elles gardent les écritures de la passe elle-même) |
| 8 | ~~**Typeur tested**~~ — **tenue le 2026-08-13 (phase C vague 1)** : `adapters/shogen-typer/` (JSON → fait prix typé, décimal exact mantisse×10^expo au patron du tag 4 RFC 8949 §3.4.4, fail-closed à 51 refus nommés dont 13 sur dires réels, 2 dires réels acceptés dont un à exposant nul) ; 28 tests verts, compte d'itérations MESURÉ 3 053 = déclaré (un test échoue si la déclaration ment) | 08, A(typer-correctness) : « cible : tested à S3, avec compte d'itérations par typeur » | fermé (l'identité du typeur va dans le fait, pas dans le témoignage — 03 §3 tenu) |

## 4. Phases

- **Phase 0 — ouverture** *(cette unité)* : conception écrite, JOURNAL,
  roadmap portée à « lancée ».
- **Phase A — corpus** : le génie du transport entre dans `biblio/` comme
  la statistique et l'ingénierie l'ont fait. Pack transport : documentation
  TLSNotary courante (protocole MPC-TLS, modèle de confiance, format de
  preuve/attestation, versions et crates, licence du projet TLSNotary
  lui-même — elle entre dans notre graphe), état du dépôt amont, contrôle
  R-8 des crates candidates ; DECO déjà détenu (relectures aux sections
  transport par l'orchestrateur). Pack licence : textes canoniques
  (Apache-2.0, MIT, AGPL-3.0) + la convention d'écosystème Rust sur pièce.
  Gate de résolution des modèles en tête de workflow (12 §9.3 : à chaque
  passe). Versement contrôlé : sha256 à l'INDEX, page de titre lue ou grep
  vérifié par l'orchestrateur.
- **Phase B — ADR** : ADR-0015 (le transport de S3 et la forme de son
  intégration au vérificateur — la tension du §2) ; ADR-0016
  (canonicalisation de `subject` — la sous-décision qu'ADR-0002 laisse
  explicitement ouverte et qu'un témoignage réel ne peut plus différer) ;
  l'instruction licence pour ADR-0014 (options chiffrées sur pièces —
  la décision reste au mainteneur) ; atterrissage COSE (ADR-0002 :
  `Cose_Sign1` — dans le périmètre exact qu'ADR-0015 fonde). Drafts par
  workers, adjudication citation par citation par l'orchestrateur.
- **Phase C — code sous gates** : §2 points 1-4 + échéances 3, 4, 5 du §3.
  Les 3 mutants semés du critère de sortie sont des cas de test nommés,
  pas des démonstrations manuelles.
- **Phase D — registres et gates orchestrateur** : échéances 6, 7 ;
  08-assumptions v3 (résidus du transport branché, au niveau d'assurance
  constaté), 09-vocabulaire (candidates des ADR), DEVOPS v2 (état
  d'instanciation).
- **Phase E — audit de sortie, remontées mainteneur et clôture** :
  **audit de sortie multi-dimensions** au patron de l'audit S1
  (2026-08-05), AVANT le rapport de clôture — workers auditeurs
  indépendants, re-vérification orchestrateur de chaque trouvaille :
  (1) *fidélité et attribution* des citations des écritures de la passe
  (ADR-0015/0016/0017, docs/13/14, INDEX §S3) contre les pièces — S-G5
  mécanise l'existence, l'audit juge la fidélité, l'emploi et le
  périmètre (la leçon sigstore : une citation existante peut être
  inversée) ; (2) *vocabulaire* : balayage complet contre 09, au-delà du
  sous-ensemble mécanisé par S-G4 ; (3) *cohérence des registres* :
  identifiants A(...) résolus, renvois croisés 03/08/09/13/DECISIONS/
  INDEX/WISHLIST, comptes déclarés ; (4) *code* : G2 tenues (réviseur ≠
  générateur par unité), score de mutation et fuzz aux seuils d'ADR-0011
  constatés. Chaque trouvaille confirmée est corrigée en classe dans la
  passe ; le verdict d'audit entre au rapport de clôture. Puis : licence
  (~~décision~~ — prise, ADR-0017), passage public (décision + purge
  exécutée avant), commit/push (autorisation), CI verte deux plateformes
  zéro étape non-verte, rapport de clôture dans ce document.

L'ordre A→E est le chemin nominal ; les unités orchestrateur (échéance 7)
peuvent précéder la phase B — elles gardent les écritures de la passe.

## 5. Ce qui remonte au mainteneur

1. **La licence** (ADR-0014 : propriétaire mainteneur) — instruite en
   phase B, tranchée par lui.
2. **Le passage public du dépôt et son moment** — DEVOPS §1 le cale sur
   l'existence du vérificateur ; l'acte est irréversible (l'historique
   devient public) et lui appartient. Pré-condition mécanique : purge
   `biblio/` vérifiée + contrôle d'historique (aucun octet de biblio/
   jamais committé — `.gitignore` de S2.5 à re-vérifier sur l'historique
   entier, pas seulement l'état courant).
3. **Les 5 procurements S2.5** (WISHLIST §Priorité 3) — toujours à sa
   main ; rien de neuf à moins que la phase B n'en forme d'autres.
4. **Commit/push par incrément** — comme aux passes précédentes, aucun
   push sans son accord.

## 6. Décisions de conception prises dans ce document

1. **Numéro de document : 13** (12 = conception S2.5 ; 11 reste réservé au
   rapport des mesures pilotes de S2, 05 §S2).
2. **Le lot de S3 est un lot à un témoignage** : `shogen verify <lot>`
   du critère opère sur la structure de lot du squelette S2.5, peuplée
   d'un témoignage réel unique. Le lot multi-témoignages à fenêtre de
   fraîcheur est S4 (05 §S4) — en faire un objet S3 serait de
   l'anticipation sans critère.
3. **La source réelle du critère vient du pool S2** (10 §2, 11 endpoints
   mesurés répondant sans clé) — aucune source nouvelle à qualifier pour
   S3 ; la classe est déjà « BTC/USD-stable » par décision du 2026-08-05.
4. **S2 (harnais jetable) continue en parallèle et n'est pas gaté** —
   reconduction 12 §hors-champ ; S3 ne consomme rien de s2-harness
   (R-22 : un prototype ne se promeut pas).

## 7. Dettes

Ouvre vide. Tout non-résolu à la clôture sera une demande de procurement
formée, une recherche documentée, ou une unité nommée avec propriétaire
(règle absolue du 2026-08-05 ; G5).

| # | dette | propriétaire | échéance | verrous anti-perpétuel |
|---|---|---|---|---|
| 1 | **Couverture du vérificateur sous le seuil candidat** — mesurée 82,90 % lignes le 2026-08-13 (lib 79,14 %, main 86,26 % ; cœur : 96,29 %) contre ≥ 90 % par rôle (ADR-0011 seuil 1). Contrôle discriminant fait (avis R-26 Q4, condition de validité) : le non-couvert résiduel vit dans `analyser_constat` et ses chemins d'erreur — exactement ce que le chantier vérificateur de la **vague 2** réécrit (contrat du constat réel, ADR-0015 pt 13) — plus la branche défensive `NonCanonique` dont l'inatteignabilité est mesurée (678 528 272 cas de fuzz, classe « décodés-non-canoniques » = 0) ; les régions stables hors périmètre vague 2 ont été testées SÉANCE TENANTE (`tests/aides_stables.rs`, 8 tests, 78,84 → 82,90 %) | orchestrateur | **vague 2 de cette passe** — jamais « plus tard » | (1) G5 : la clôture de S3 est impossible avec cette entrée ouverte ; (2) « couverture vérificateur ≥ 90 % mesurée et imprimée » entre au critère de sortie de la vague 2 ; (3) le chiffre s'imprime à chaque mesure (ADR-0011 pt 5) — toute régression pendant la vague 2 est visible |
| 2 | ~~**Couche fuzz instrumentée (couverture-guidée)**~~ — **FERMÉE le 2026-08-13** : chantier `wf_3b4417e1-26f` livré et adjugé (deux moteurs, deux campagnes réelles zéro panique, workspace fuzz/, deny local, jobs CI), revue G2 `wf_6603a162-bc6` « accepter avec corrections » toutes appliquées (dont la bloquante : le deny du workspace est désormais GATÉ au job cargo-afl) | orchestrateur | fermée | reste au registre : premier run réel des jobs au push (donnée, pas formalité) |
| 3 | **Distillation du corpus dérivé** (adjudication R-26 du 2026-08-13, option (d) de l'avis ADVISOR) : les campagnes instrumentées atteignent 789 arêtes hors corpus committé (1055 → 1844 sur 3024) ; plutôt que verser 171 blobs illisibles, ANALYSER le top-20 (471/789 arêtes), nommer les formes exercées, ÉTENDRE le générateur `fuzz-corpus` pour qu'elles deviennent des `dirigee-*` régénérables — gate d'acceptation : le corpus régénéré atteint ≥ 471 des 789 arêtes au même outillage de mesure ; repli graine-par-graine en catégorie `derivee-*` portée par amendement ADR-0011 (squelette à l'avis) pour l'innommable. Pièces : `scratch/proposition-graines-derivees*.tar.gz` + SHA256SUMS (hors dépôt, durables) | orchestrateur | **vague 2** — au critère de sortie, à côté de la dette 1 (couverture ≥ 90 %) | (1) G5 : clôture de S3 impossible avec l'entrée ouverte ; (2) c'est l'application du seuil 6 (« générateur à corriger ») — ni (a) ni (b) n'en dispensait |
