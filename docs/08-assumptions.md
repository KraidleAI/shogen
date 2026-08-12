# Shōgen — registre des assumptions (v3, 2026-08-13 ; v2 2026-08-12 ; v1 2026-07-30)

> **Le registre fait foi** : une assumption absente d'ici n'existe pas, et
> tout identifiant A(...) écrit ailleurs se résout ici (règle héritée du
> roll de Kraidle). Chaque entrée porte : l'énoncé, la source du résidu
> (artefact détenu), les sites porteurs, le niveau d'assurance actuel, et
> ce qui la déchargerait. Les classes de corpus (colonne « exercée par »)
> n'existent pas encore — S2/S3 les créeront ; d'ici là la colonne dit
> `aucune`, ce qui est un état, pas un oubli.

## Résidus de transport (un par mécanisme, jamais fusionnés — ADR-0001)

| id | énoncé | source du résidu | porteur dans | assurance | décharge | exercée par |
|---|---|---|---|---|---|---|
| A(notary-neutrality) | Le notaire d'un transport MPC (lignée TLSNotary) est neutre ; un vérificateur qui n'a pas conduit le MPC lui-même doit lui faire confiance pour l'authenticité | FAQ TLSNotary (détenue, grep) : « trust in the notary » ; preuve envers vérificateur désigné | 03 §2 ; futurs adapters `transport-tlsn` | aucune (énoncé de confiance) | co-conduite du MPC par le vérificateur, ou quorum de notaires — mesuré, pas déclaré | aucune |
| A(attestor-honesty) | L'attestor d'un transport proxy-witness ne forge pas de preuves | FAQ sécurité Reclaim (détenue) : un attestor compromis peut forger des preuves (« could generate fake proofs ») ; « The only protection … is decentralisation or self-hosting » | 03 §2 | aucune | self-hosting par le client, ou multi-attestor (ADR-0004 : k témoignages, l'ensemble d'attestors entre dans les observables R2) | aucune |
| A(enclave-integrity) | L'enclave d'un transport TEE et sa chaîne d'attestation sont intègres | DECO §3.1 (détenu, lu) : « If a single TEE is broken, TLS session content, including user credentials, can leak » | 03 §2 | aucune | hors de portée de Shōgen (matériel) ; l'atténuation est la diversité de transports dans le lot | aucune |
| A(source-key) | Pour un transport `source-sig`, la clé publiée par la source est la bonne et n'est pas compromise | à documenter — aucun artefact détenu ne porte ce résidu précis (transparence de clés : littérature à fetcher au moment du premier adapter `source-sig`) | 03 §2 | aucune | journal de transparence ou épinglage multi-canal — au premier adapter concerné | aucune |
| A(verifier-designation) | La preuve d'un transport à vérificateur participant (3P-handshake DECO, notaire TLSNotary) vaut envers ce participant ; sa transmission à un tiers repose sur la signature du participant, pas sur le transport | DECO §3.4 (détenu, lu) : clés de session secret-partagées entre P et V ; FAQ TLSNotary : vérificateur désigné | 03 §4, point (1) — citée au site depuis le 2026-07-30 | aucune | transports à preuve publiquement vérifiable (zk), ou le participant signe comme attestor et son résidu devient A(attestor-honesty) | aucune |
| A(self-attestation) | En S3, le notaire du transport `tlsn-mpc/1` est opéré par Shōgen : A(notary-neutrality) n'est pas seulement non déchargée, elle est portée par la partie même dont 02-vision exige qu'on ne lui fasse pas confiance — le verdict S3 est démonstratif, pas probant | page « Notary Server (Deprecated) » (détenue : service arrêté, binaire retiré en alpha.13) ; billet officiel du 2026-06-17 (détenu) : « A notary is just a verifier you didn't run yourself. » | tout verdict S3 ; ADR-0015 pt 4 | aucune | notaire tiers, ou quorum de notaires comptés en axe R2 (ADR-0004) | aucune |

## Résidus de couche (Shōgen lui-même)

| id | énoncé | source | porteur dans | assurance | décharge | exercée par |
|---|---|---|---|---|---|---|
| A(typer-correctness) | Le typeur extrait du dire brut le fait annoncé (classe, valeur, unité) sans erreur de sens | 03 §3 — le typeur est un adapter, testé jamais prouvé | tout fait typé ; verdicts | aucune (cible : tested à S3, avec compte d'itérations par typeur) | n'est jamais déchargée — bornée par tests + identité du typeur dans le fait | aucune |
| A(axis-coverage) | Les axes R2 mesurés couvrent les modes communs *dominants* du pool ; un mode commun hors axes reste possible | 04 §4.1 (K&L appliqué à nous-mêmes) ; le signal « co-défaillance observée non expliquée par les axes R2 » (04 §3) existe précisément parce qu'elle peut être fausse | tout certificat ; k_eff | aucune (par construction indéchargeable en général) | jamais totalement ; R1 la *teste* en continu (z élevé + partition propre = axes insuffisants, motif de refus) | aucune |
| A(window-stationarity) | Les fenêtres d'observation R1 d'une classe de faits sont comparables — le processus d'entrée est suffisamment stationnaire pour que le test agrégé ait un sens | Eckhardt & Lee, TM-86369 (détenu, summary lu) : hypothèse (ii), « the system is required to execute on a stationary input series » — le même postulat, hérité et nommé | 04 §2 (le test R1) — citée au site depuis le 2026-07-30 | aucune | stratification des fenêtres par régime (calme/stress) quand S2 aura mesuré ; jusque-là l'hypothèse est écrite dans chaque certificat R1 | aucune |
| A(history-integrity) | L'historique de co-défaillances sur lequel R1 calcule n'a pas été altéré ni sélectionné (fenêtre de complaisance exclue par politique de classe — 04 §5) | 04 §5 (surface de jeu du certificat) | tout certificat R1 | aucune | l'historique est lui-même un lot de témoignages datés — la décharge est récursive et partielle, à spécifier en S4 | aucune |
| A(asn-attribution) | L'attribution IP → ASN rapportée par les services (RIPEstat, Team Cymru) reflète l'annonce BGP effective au moment de la mesure — l'axe ASN de R2 en dépend | 10 §4.1, résidu 6 (les services d'attribution sont eux-mêmes des témoins) ; concordance RIPEstat = Cymru 8/8 du 2026-08-05 (V1, re-mesure aveugle) — une observation, pas une décharge | 10 §4.1 (axe ASN) ; futur harnais R2 de S2 | aucune | jamais totale ; attribution croisée sur ≥ 2 bases BGP distinctes + re-mesure à chaque quorum | aucune |
| A(toolchain-soundness) | La solidité de `rustc` et de la bibliothèque standard (qui emploie `unsafe`) est supposée, jamais établie — RustBelt couvre un langage formalisé, pas le compilateur | RustBelt p. 66:3 (détenu, relu 2026-08-12 ; graphie re-vérifiée à la page le 2026-08-12, S3 — la première copie portait « language itself ») : « several soundness bugs have been found in Rust, both in the type system itself » et §1.2 « we do not consider the full Rust language » | ADR-0009 ; tout binaire du produit | aucune | aucune complète connue ; réduction par dépendances minimales (ADR-0009) et par la reproductibilité du binaire vérificateur (ADR-0012 D6) | aucune |
| A(verifier-binary) | Le binaire `shogen-verifier` qu'un tiers exécute correspond au code source publié | Lamb & Zacchiroli p. 1 (détenu, relu 2026-08-12) : « trusting code is not the same as trusting its executable counterparts » | ADR-0012 ; la promesse offline d'ADR-0003 et 02-vision | aucune | rebuild bit-à-bit indépendant (décharge complète — ADR-0012 D6) ; provenance attestée (décharge partielle : le résidu se déplace vers la plateforme de build) | aucune |
| A(transport-check-delegated) | Le contrôle (1) de 03 §4 est exécuté par `shogen-tlsn-verify` construit depuis l'amont épinglé ; `shogen-verifier` en contrôle la liaison (hash de `transport_proof`, hash d'`utterance`), jamais le contenu cryptographique | ADR-0015 pt 8 (forme β) — le verdict nomme la délégation | tout verdict S3 ; ADR-0015 | aucune | forme α (vérification embarquée), sous les trois conditions d'ADR-0015 pt 11 | aucune |
| A(upstream-alpha) | L'amont TLSNotary est en alpha, déclaré impropre à la production par ses auteurs ; aucune stabilité du format d'attestation n'est établie | README amont (détenu) : « should not be used in production. Expect bugs and regular major breaking changes. » ; releases API (détenue) : 15 releases, toutes `prerelease: true`, alpha.15 publiée 2026-05-21 | ADR-0015 ; tout `transport_proof` archivé | aucune | une version stable amont ; en attendant, la révision amont exacte voyage avec le lot (ADR-0015 coût 5, sous-décision ouverte) | aucune |

## Résidus de méthode (la chaîne d'ingénierie elle-même — S2.5, 2026-08-12)

Section ouverte par l'orchestrateur sur proposition des ADR-0011/0013 :
les résidus ci-dessous portent sur **notre façon de tester**, pas sur le
produit. Tant qu'un identifiant n'était pas ici, il ne s'écrivait nulle
part (leçon des identifiants morts, ADR-0001).

| id | énoncé | source du résidu | porteur dans | assurance | décharge | exercée par |
|---|---|---|---|---|---|---|
| A(coupling-effect) | Les fautes semées simples couvrent les fautes réelles par couplage — la prémisse de tout score de mutation | DeMillo, Lipton & Sayward p. 35 (détenu, relu 2026-08-12) : « There is, of course, no hope of "proving" the coupling effect; it is an empirical principle » | tout score de mutation publié (ADR-0011 pt 3) | aucune | jamais totale ; les fautes réelles trouvées en production entrent au corpus de mutants (l'évasion devient test) | aucune |
| A(gate-adequacy) | Les mutants semés d'une gate représentent les violations réelles que la gate doit attraper | transposition du geste de mutation aux gates, nommée comme analogie de méthode (ADR-0013, source qui tranche, pt 2) — rien ne l'établit | tout vert de gate (ADR-0013 pt 2 : un vert n'atteste que ce que ses mutants ont montré) | aucune | jamais totale ; l'invariant « l'évasion devient test permanent » fait de chaque contre-exemple réel un mutant de plus | xtask/tests/mutants.rs — 13 mutants + 1 témoin, vus verts par l'orchestrateur le 2026-08-12 |

## Notes de registre

1. **Aucune entrée D** pour l'instant : les énoncés de déploiement
   n'existeront qu'avec du code déployable (S3+). Le registre les
   accueillera au même rang, sans les confondre avec les A(...).
2. **Références inter-projets** (détenues côté Kraidle, absentes du
   registre Shōgen) : il en reste **deux** — le Lemme 8 de Chainlink OCR
   (INDEX, dette 5) et **RFC 5280 §3.3**, invoquée par 03 §2 pour la règle
   des latences par mécanisme. RFC 8949 (CBOR) et RFC 9052 (COSE),
   porteuses d'ADR-0002, sont **détenues côté Shōgen depuis le 2026-08-13**
   (phase B de S3, INDEX §phase B — fermeture partielle de cette note).
   La décision copie-locale vs référence croisée ne porte plus que sur les
   deux restantes (historique : quatre, pas trois — corrigé le 2026-07-30,
   audit S1).
3. La règle de rédaction : citer la feuille, pas le parapluie — un site
   qui ne dépend que d'A(attestor-honesty) ne cite pas « les résidus de
   transport » en bloc.
