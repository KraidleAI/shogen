# Shōgen — registre bibliographique

**124 artefacts détenus** au 2026-08-13 (compte re-mesuré par listing du
dossier dans la passe qui écrit ce chiffre — mécanisé par la gate S-G6
depuis S3 ; +21 fetchés à la passe S2.5, +67 à l'ouverture de S3, +5 à la phase B (RFC + WHATWG), +3 à la phase C (NIST), +7 à la phase C vague 1 (2 RFC typeur + 5 sources amont épinglées), en bas
de registre ; les `*.sidecar`, extractions texte locales des PDF pour la
gate S-G5, ne comptent pas comme artefacts). Chaque
entrée porte : ce que la page de titre dit, ce qui a été lu, et le statut
de vérification des citations qui s'appuient dessus. **Des `*.sidecar` existent
désormais** (extractions texte locales des PDF pour la gate S-G5, cf. en-tête
ci-dessus) : les greps portent sur ces sidecars là où ils existent, sinon sur les
fichiers bruts ; les PDF sans sidecar restent sur lectures visuelles. (L'ancien
« pas de sidecars encore » — incohérent avec l'en-tête — corrigé le 2026-08-20,
dette 9b.)

| fichier | ce que c'est (page de titre / en-tête) | lu | citations vérifiées |
|---|---|---|---|
| `deco-2019.pdf` | Zhang, Maram, Malvai, Goldfeder, Juels, *DECO: Liberating Web Data Using Decentralized Oracles for TLS*, arXiv:1909.00938 (version étendue de CCS '20) | pp. 1-6 lues au fichier le 2026-07-30 (titre, abstract, §1–1.3, §2 TLS/MPC, §3 problème, modèle adversarial, F_Oracle, strawman, §3.4 aperçu, §4.1 début) | Vérifiées au texte p. 1 : « prove that a piece of data accessed via TLS came from a particular website » — provenance, pas vérité ; « without trusted hardware or server-side modifications ». §3 (pp. 3-4) : adversaire réseau **statique et malveillant**, sécurité maintenue « when either P or V is corrupted » ; prover-integrity : « A malicious P cannot forge content provenance » ; « oracles running DECO are trusted **only for integrity, not for privacy** » ; et le renvoi qui nomme le gap de Shōgen : « Smart contracts can further hedge against integrity failures by **querying multiple oracles and requiring, e.g., majority agreement** » — le quorum à indépendance postulée, délégué sans mécanisme. Preuve envers un vérificateur **participant** (handshake à trois parties) : résidu de désignation analogue à TLSNotary. |
| `knight-leveson-1986-full.pdf` | Knight & Leveson, *An Experimental Evaluation of the Assumption of Independence in Multi-Version Programming*, article complet (manuscrit, copie MIT OCW 16.358J, 46 p. ; version journal : IEEE TSE 12(1):96-109, 1986). Page de titre lue le 2026-07-30 — apporté par le mainteneur, remplace le résumé de séminaire KTH (supprimé). | pp. fichier 1-3 et 10-25 (abstract, intro, §4 résultats, §5 modèle et test, §6 fautes, §7 discussion, §8 conclusions) | Vérifiées au texte : abstract « the number of tests in which more than one program failed was substantially more than expected » ; §5 : N=27, n=1 000 000, K=1255, z=100,51 > 2,33 (point 99 %), « we reject the null hypothesis with a confidence level of 99% … Thus, we reject this assumption » ; §5 : « from an operational viewpoint, it does not matter *why* programs fail on the same input, it merely matters that they *do* » ; §4 : « In the preliminary analysis of common faults, *all* were found to involve versions from both schools » ; §8, la réserve de portée : « it is conditional on the application that we used. The result may or may not extend to other programs, we do not know » ; §8 : « approximately one half of the total software faults found involved two or more programs » ; §8, le mandat matériel : les concepteurs matériels « use sophisticated techniques to determine common failure modes and systematically alter their designs ». |
| `knight-leveson-1986-uva-report.pdf` | Page de titre lue le 2026-07-30 : *Detection of Faults and Software Reliability Analysis*, Annual Progress Report NASA NAG-1-605, juil. 1985–juin 1987, J.C. Knight, UVA Report UVA/528243/CS88/103, août 1987, 14 p. (NASA-CR-180347). Rapport d'avancement compagnon — intérêt marginal. | page 1 | aucune citation ne s'appuie dessus |
| `knight-leveson-reply.pdf` | Page de titre lue le 2026-07-30 : Knight & Leveson, *A Reply to the Criticisms of the Knight & Leveson Experiment*. Venue relevée par recherche web du 2026-07-30 (fiche ACM DL : SIGSOFT Software Engineering Notes 15(1), janv. 1990, pp. 24-35) — à vérifier sur l'artefact/DOI avant citation formelle. Documente la controverse avec Avizienis et al. ; p. 1 porte la citation d'Avizienis nommant l'indépendance « the fundamental conjecture of the NVP approach ». | page 1 | la citation Avizienis ci-contre est utilisable (lue p. 1) ; le reste non lu |
| `tlsnotary-faq.html` | FAQ officielle tlsnotary.org (page mutable — copie du 2026-07-30) | oui (fetch + grep sur la copie) | vérifiées par grep dans le fichier détenu : « does not solve the … Oracle Problem » (1 occurrence), « trust in the notary » (1 occurrence). Également au fichier (ligne 30) : ce que voit le notaire — liste exhaustive à quatre éléments : « the time of the TLS-session » (instant ou durée : non tranché ici, citer l'anglais), longueurs des requêtes/réponses, nombre d'aller-retours, cipher suite ; la preuve vaut envers un vérificateur désigné ; TLS 1.2 seulement. |
| `c2pa-spec-2.4.html` | C2PA Technical Specification v2.4 (spec.c2pa.org — copie du 2026-07-30) | sections modèle de données + trust model (via fetch) + §1.2 Scope (localisation vérifiée par grep) | vérifiée par grep dans le fichier détenu (1 occurrence, **§1.2 Scope**, bloc citant les Guiding Principles C2PA — pas le §14 Trust Model) : « SHOULD NOT provide value judgments » — la spec s'interdit de juger si la provenance est « bonne », elle valide seulement intégrité, association et non-altération. Modèle : assertions → claim signé → claim signature ; chaîne par ingredients. |
| `reclaim-security-faq.html` | *Is Reclaim Secure?* — FAQ sécurité officielle, blog.reclaimprotocol.org (page mutable — copie du 2026-07-30) | oui (fetch du 2026-07-30 ; « only protection against fake proofs » vérifié par grep, 2 occurrences) | un attestor compromis ne peut pas lire les données (TLS de bout en bout) mais **peut forger des preuves** — « The only protection against fake proofs here is decentralisation or self-hosting of the attestor » ; BGP surveillé via RIPE RIS, connexion coupée si reroutage suspect ; modèle à attestor unique (la décentralisation est une mitigation évoquée, pas l'architecture). |
| `reclaim-attestor-core-readme.html` | README du dépôt reclaimprotocol/attestor-core (« witness server ») — copie du 2026-07-30 | non lu au-delà du fetch de recherche | aucune citation ne s'appuie dessus |
| `eckhardt-lee-1985-tm86369.pdf` | Page de titre lue le 2026-07-30 : Eckhardt & Lee, *A Theoretical Basis for the Analysis of Redundant Software Subject to Coincident Errors*, NASA Technical Memorandum 86369, janv. 1985, Langley (NTRS 19850015006). Version mémorandum du papier IEEE TSE SE-11(12):1511-1517 (1985) — le tiré IEEE n'est pas détenu. | pp. 1-2 (titre, summary) | Vérifiée au texte p. 2 : la fonction centrale « intensity of coincident errors » — « the propensity of a population of programmers to introduce design faults in such a way that software components fail together when executing in the user environment » ; hypothèses (i) composants choisis en échantillon aléatoire, (ii) série d'entrées stationnaire. **À lire : le modèle formel (corps) avant de citer une inégalité.** |
| `littlewood-miller-1989-tse.pdf` | Page de titre lue le 2026-07-30 : Littlewood & Miller, *Conceptual Modeling of Coincident Failures in Multiversion Software*, IEEE TSE 15(12):1596-1614, déc. 1989 — **tiré journal authentique** (apporté par le mainteneur ; la pagination journal est citable depuis cette copie). | pp. 1596-1604 (abstract, §I, §II modèle et dualité, §III méthodologies diverses, §IV 1-out-of-n) | Vérifiées au texte : abstract — « independently developed program versions will fail dependently » et la **dualité** choix-d'entrée/choix-de-programme ; éq. (14)-(16) : P(deux versions indépendantes co-échouent) = E(Θ²) = Var(Θ)+(E(Θ))², l'écart à l'indépendance **est** Var(Θ) ; p. 1599 : sur les données K&L, le calcul naïf d'indépendance est « optimistic by two orders of magnitude ; the calculation error equals Var(Θ) » ; éq. (28) : P(B échoue \| A a échoué)/P(B échoue) = 1 + Corr(Θ_A,Θ_B)·CV(Θ_A)·CV(Θ_B) — **la corrélation des difficultés comme mesure du degré de dépendance** ; p. 1601 : « it is possible that Cov(Θ_A, Θ_B) < 0 ! » — faire *mieux* que l'indépendance est possible ; p. 1603, ré-analyse des données K&L en deux méthodologies (UVA/UCI) : ρ(Θ_A,Θ_B) = 0,1808, et P(co-échec) *diminue* en tirant une version de chaque école (10,944e-6) contre tirage aléatoire (12,963e-6) ; §IV éq. (41)-(44) : sous indifférence, « it is always better to force as much diversity of methodology on the different versions as possible » ; et la mise en garde (45)-(46) : ces résultats sont des *moyennes* — par entrée fixée, l'ordre s'inverse. |

### Fetchés par la passe R-1 (2026-07-30) — pages de titre lues, corps à lire avant citation détaillée

| fichier | ce que c'est (page de titre) | lu | notes |
|---|---|---|---|
| `kohli-2026-nine-judges.pdf` | Kohli (Apple), *Nine Judges, Two Effective Votes: Correlated Errors Undermine LLM Evaluation Panels*, arXiv:2605.29800 (cs.CL), 28 mai 2026 | p. 1 (titre, abstract, §1) | Vérifié p. 1 : Kish n_eff + modèle nul de Condorcet ; « roughly three-quarters of the panel's nominal independence is lost » ; « no prior work has quantified the effective independence of LLM judge panels ». La menace la plus directe au claim k_eff — à citer et distinguer (06 §2). |
| `he-yu-2026-sqa.pdf` | He & Yu (OpenKedge.io), *Semantic Quorum Assurance: Collective Certification for Non-Deterministic AI Infrastructure*, arXiv:2606.08021 (cs.LG), 6 juin 2026 | p. 1 (titre, abstract, §1) | Vérifié p. 1 : panel de validateurs-agents divers, « risk-adaptive quorum predicate » imposant diversité de modèle/archétype, « correlated cognitive failure model » ; 18,5 % → 0,3 % sur 500 scénarios. Diversité imposée par étiquettes, jamais mesurée sur historique — le contraste qui fonde R1 vs R3. |
| `zhai-2014-indaas.pdf` | Zhai, Chen, Wolinsky, Ford (Yale / Bell Labs), *Heading Off Correlated Failures through Independence-as-a-Service* (venue relevée par balayage : USENIX OSDI 2014 — à confirmer sur la fiche) | p. 1 (titre, abstract, §1) | Vérifié p. 1 : « seemingly independent systems may share deep, hidden dependencies » ; audit proactif par modules d'acquisition de dépendances ; cite Google : « close to 37% of failures are truly correlated ». Le jumeau structurel du certificat — sans historique testé ni artefact par décision. |
| `sevim-torres-2026-signals-spoils.pdf` | Sevim & Ferreira Torres, *Signals and Spoils: Speculative Oracle Extractable Value in the Era of Cross-Chain Interoperability*, arXiv:2606.03434 (cs.CR), 2 juin 2026 | p. 1 (titre, abstract, §1) | Vérifié p. 1 : « independent DONs consume largely identical off-chain price data nearly simultaneously yet publish updates at different times, creating statistically predictable cross-chain exploitation windows » ; 63 feeds Chainlink, 12 009 mises à jour, 2 986 liquidations Aave. La mesure du phénomène exact — sans l'instrument. |
| `chainlink-2017-whitepaper-v1.pdf` | Ellis, Juels, Nazarov, *ChainLink: A Decentralized Oracle Network*, whitepaper v1.0, 4 septembre 2017 | pp. 1, 11, 19 (titre ; §4.1 *Distributing sources* ; §5.3 *Certification Service*) | **Localisations vérifiées au texte le 2026-07-30.** §4.1 p. 11 — l'amont commun donné en exemple : « If site Src₁ = EchoEcho.com obtains its data from Src₂ = TheHorsesMouth.com, an error at Src₂ will always imply an error at Src₁ », suivi de « More subtle correlations between data sources can also occur » et de l'annonce jamais réalisée : « Chainlink also proposes to pursue research into **mapping and reporting the independence of data sources** in an easily digestible way so that oracles and users can avoid undesired correlations ». §5.3 p. 19 — le *mirroring* : « a Sybil attacker can adopt a behavior called *mirroring*, in which it causes oracles to send individual responses based on data obtained from a *single data-source query* … misbehaving oracles may share data off-chain but pretend to source data independently ». |
| `zhang-2016-network-diversity-tifs.pdf` | Zhang, Wang, Jajodia, Singhal, Albanese, *Network Diversity: A Security Metric for Evaluating the Resilience of Networks against Zero-Day Attacks*, IEEE TIFS (version auteurs ; fiche balayage : 11(5):1071-1086, 2016) | p. 1 (titre, abstract, §1) | Vérifié p. 1 : métrique « biodiversity-inspired … based on the effective number of distinct resources » ; « most existing efforts rely on intuitive and imprecise notions of diversity ». La forme du compte effectif à citer-et-distinguer pour k_eff. |

### Cas d'espèce (fetché le 2026-07-31)

| fichier | ce que c'est | lu | citations vérifiées |
|---|---|---|---|
| `galaxy-2026-07-31-tradexyz-oracle.html` | Galaxy Research, note hebdomadaire du 31 juillet 2026 — section sur les liquidations TradeXYZ / xyz:SKHYNIX (copie du 2026-07-31 ; page mutable) | sections liquidations + « Our take » (fetch, puis grep sur la copie) | Vérifiées par grep dans le fichier détenu (1 occurrence chacune) : « liquidations resulting from an **accurate but anomalous** third-party price feed reading » ; « a single share of chip manufacturer SK Hynix changed hands for **1,272,000** won (roughly $868) in the opening seconds of South Korea's **NextTrade** pre-market session … 29.96% below the previous close » ; la composition — « TradeXYZ's mark price is the **median of three inputs**: the oracle price, the oracle plus a 150-second exponential moving average of the book's deviation from it, and the median of best bid, best ask, and last trade » ; « That smoothing absorbed about 11 percentage points of a 30% corrupted input. It was not enough. The mark fell 18.7% » ; le verdict — « **The oracle worked. The risk system didn't.** Traditional markets **separated last trade**, index price, and fair value for risk purposes decades ago, precisely so one local execution cannot decide the fate of a leveraged account ». Porte ADR-0007. |

### Fetchés par la passe S2 (2026-08-05) — source du seuil statistique et précédent de détection de copie

Les quatre appuient `docs/10-mesures-pilotes-design.md`. Trois formes du
seuil d'approximation normale de la binomiale coexistent et **ne se
confondent pas** (10 §5.4) : c'est pourquoi les trois sources sont détenues.

| fichier | ce que c'est (page de titre / en-tête) | lu | citations vérifiées |
|---|---|---|---|
| `uconn-oer-math3160-ch9-2018.pdf` | University of Connecticut, OER Math 3160 (Probability), ch. 9 « Normal approximation to the binomial », p. 121 (`prob3160ch9.pdf`) | p. 121 lue au fichier le 2026-08-05 (V5 + grep de rédaction) | Vérifiée : sous le théorème 9.1, « This approximation is good if np(1 − p) ⩾ 10 and gets better the larger this quantity gets » (le « ⩾ » tombe à l'extraction texte, présent au rendu ; grep confirme la phrase). **Source du critère « historique insuffisant » de R1** (10 §5.4) — la forme produit-variance, en une inégalité. |
| `nist-sematech-ehandbook-prc24.html` | NIST/SEMATECH e-Handbook of Statistical Methods, §7.2.4 « Does the proportion of defectives meet requirements? » (copie du 2026-08-05 ; page mutable) | §7.2.4, sous-section « Restriction on sample size » (fetch + grep) | Vérifiée par grep : « min{Np₀, N(1 − p₀)} ≥ 5 » et « valid for large N, (N > 30) ». **Forme voisine distincte** (seuil 5, min des deux) — garde-fou de 10 §5.4, à ne pas confondre avec le produit-variance. Piège écarté (V5, verdict REFUTE) : la page « Binomial Distribution » §1.3.6.6.18 (`eda366i.htm`) ne contient aucun seuil d'approximation. |
| `psu-stat200-8-1-1-1.html` | Penn State STAT 200, §8.1.1.1 « Normal Approximation Formulas » (copie du 2026-08-05 ; page mutable) | §8.1.1.1 (fetch + grep) | Vérifiée par grep : « both np ≥ 10 and n(1−p) ≥ 10 » — deux comptes de succès/échec, **forme voisine distincte** (10 §5.4). |
| `dong-2010-pvldb-copying-R120.pdf` | Dong, Berti-Équille, Hu, Srivastava, *Global Detection of Complex Copying Relationships Between Sources*, PVLDB 3(1):1358-1369, 2010 (`vldb.org/pvldb/vol3/R120.pdf` — **R120**, pas R121) | page de titre + résumé + intro lus le 2026-08-05 (V5) ; **corps non lu** | Identité re-établie (titre, auteurs, venue, p. 1358). Précédent académique de l'axe R2 (2c), détection de copie par fautes partagées (10 §4.2). **(2c) ne le cite pas tant que le corps n'est pas lu** (dette 6). Prédécesseur du mécanisme pairwise : « Integrating Conflicting Data: The Role of Source Dependence », PVLDB 2, 2009 (non détenu). |

### Fetchés par la passe S2.5 (2026-08-12) — corpus des fondations d'ingénierie

Acquisition par 4 workers (12 §6.1 ; trois rapports rendus, le worker du
pack architecture mort au rendu — filtre de contenu — ses fichiers
contrôlés directement). **Contrôle orchestrateur du 2026-08-12, même
passe** : page de titre de chaque PDF ouverte au fichier par
l'orchestrateur ; marqueurs des HTML greppés sur la copie ; sha256
recalculé en destination ; pour `parnas` et `meyer` (pack sans rapport),
provenance re-établie par re-téléchargement à octets identiques depuis
l'URL candidate. Le **sha256 est porté par entrée** — le « à terme » de
DEVOPS §1 commence à cette section. Corps non lus sauf mention : les
lectures de section se font à la rédaction des ADR, une-citation-un-grep.

| fichier | ce que c'est (page de titre / en-tête) | lu | notes de conformité |
|---|---|---|---|
| `jung-2018-rustbelt-popl.pdf` | Jung, Jourdan, Krebbers, Dreyer, *RustBelt: Securing the Foundations of the Rust Programming Language*, PACMPL 2(POPL), art. 66, janv. 2018, 34 p. — **DOI 10.1145/3158154 imprimé en page de titre** ; copie auteurs (plv.mpi-sws.org) ; affiliation Krebbers : Delft (propre à la version POPL'18). sha256 `cadcc31e287cdb19b9faeffd807d85496c235b45259a16f9c1ac3a8acfad5cd9` | p. 1 lue au fichier le 2026-08-12 (titre, abstract, §1 ¶1-2) | Vu p. 1 : « the first formal (and machine-checked) safety proof for a language representing a realistic subset of Rust ». ADR-0009. |
| `jung-2021-safe-rust-cacm.pdf` | **Version auteur** datée « 2021/2/22 », titre étendu *Safe Systems Programming in Rust: The Promise and the Challenge* — aucun marquage CACM/DOI/pagination : la référence CACM 64(4):144-152 (2021) reste **candidate**, pagination non citable depuis cette copie. sha256 `43f7eb3eeb22354950f1aaffc23a90400f6847b0ee81a56e44234ddad89fc1bd` | p. 1 lue au fichier le 2026-08-12 | Vu p. 1 : « Microsoft recently reported that 70% of the security vulnerabilities they fix are due to memory safety violations [33] » — chiffre tiers, à citer avec sa référence [33], jamais nu. ADR-0009. |
| `cisa-2023-memory-safe-roadmaps.pdf` | CISA, NSA, FBI + ASD ACSC, CCCS, NCSC-UK, NCSC-NZ, CERT NZ : *The Case for Memory Safe Roadmaps — Why Both C-Suite Executives and Technical Experts Need to Take Memory Safe Coding Seriously*, « Publication: December 2023 », **TLP:CLEAR** (« may be distributed without restriction »). sha256 `dfe3e72e075738e345aab81a541f72ab4c0cd149235426108090bf48787bc34b` | page de titre lue au fichier le 2026-08-12 | Source primaire .gov. ADR-0009 (instruit l'alternative C/C++). |
| `parnas-1972-criteria-cacm.pdf` | Tiré CACM authentique : D.L. Parnas (Carnegie-Mellon), *On the Criteria To Be Used in Decomposing Systems into Modules*, CACM 15(12), déc. 1972, p. 1053, © 1972 ACM — **pagination journal citable**. Provenance re-établie (octets identiques à `win.tue.nl/~wstomv/edu/2ip30/references/criteria_for_modularization.pdf`). sha256 `7008fd6abc833ded750e52dbac4968e8eda339f66b462ca4427f1953f98df9c4` | p. 1053 lue au fichier le 2026-08-12 (abstract, intro) | ADR-0010 — la source-qui-tranche candidate de la décomposition. |
| `meyer-1992-dbc-computer.pdf` | Bertrand Meyer (Interactive Software Engineering), *Applying "Design by Contract"*, IEEE Computer, p. 40, bandeau « 0018-9162/92/1000-0040 © 1992 IEEE » (cohérent avec 25(10), oct. 1992 — candidat). Provenance re-établie (octets identiques à `se.inf.ethz.ch/~meyer/publications/computer/contract.pdf`). sha256 `bc1bab86f8753e5eafb40b7558e961b2c4bc9938c061e8dd8c141b839873ac07` | p. 40 lue au fichier le 2026-08-12 | Accroche vue p. 40 : « reduce bugs by building software components on the basis of carefully designed contracts ». ADR-0010 ; le livre OOSC2 reste en procurement (12 §4.2). |
| `claessen-hughes-2000-quickcheck-icfp.pdf` | Claessen & Hughes (Chalmers ×2), *QuickCheck: A Lightweight Tool for Random Testing of Haskell Programs*, ICFP '00 (Montréal), © 2000 ACM 1-58113-202-6/00/0009 — DOI non imprimé ; copie de cours (Tufts) paginée 1..N : pages ACM 268-279 non citables d'ici. sha256 `bfddcaa648f836e50804910fc0956cc037c1a8b3e3d6716fb12e4e1ffdcb5172` | p. 1 lue au fichier le 2026-08-12 (titre, abstract, §1) ; p. 1 relue visuellement le 2026-08-12 (S3) | ADR-0011 — fondation du property-based. **Citations vérifiées visuellement p. 1 (S3)** : abstract, « Random testing is especially suitable for functional programs because properties can be stated at a fine grain. » ; §1, « It is generally accepted that pure functions are much easier to test than side-effecting ones, because one need not be concerned with a state before and after execution. » **Limite d'extraction consignée** : la fonte du PDF n'a pas de mapping pour la ligature « fi » — pdftotext ET pypdf la perdent (« ne grain », « su ces ») ; le sidecar ne peut PAS porter ces phrases, le registre les porte ici, c'est le chemin couvert par S-G5. |
| `demillo-1978-hints-computer.pdf` | Tiré Computer authentique : DeMillo (Georgia Tech), Lipton & Sayward (Yale), *Hints on Test Data Selection: Help for the Practicing Programmer*, Computer 11(4), avr. 1978, p. 34, © 1978 IEEE (bandeau « 0018-9162/78/0400-0034 ») ; miroir de cours `gse.ufsc.br`. sha256 `3f0baffdc0cff1400caacf4318c6e6b72f2c5bf49511be77c1c3d739ff35c789` | p. 34 lue au fichier le 2026-08-12 ; corps lu par le worker (8 p.), **à relire avant citation** | **Trouvaille de passe** (worker ; corroborée p. 34 par l'orchestrateur) : la locution « competent programmer hypothesis » n'apparaît PAS dans l'article — p. 34 écrit « competent programmers, in their many iterations through the design process… », le « coupling effect » est en accroche (« this so-called coupling effect ») ; la **nomination** CPH est postérieure (Jia & Harman, §II.A). Citer la phrase de 1978 et la nomination de 2011, jamais l'une pour l'autre. ADR-0011. |
| `jia-harman-2011-mutation-survey-tse.pdf` | Jia & Harman (KCL/CREST), *An Analysis and Survey of the Development of Mutation Testing*, IEEE TSE — copie d'auteur (UCL, `www0.cs.ucl.ac.uk/staff/mharman/`) paginée 1..N : la référence 37(5):649-678 (2011) reste **candidate**, pagination non citable d'ici. sha256 `056ac9b99410321c7cb80a29284c4ca106456e1a0cf64b6f4d633ba83edff342` | p. 1 lue au fichier le 2026-08-12 (titre, abstract, §I) | Vu p. 1 : « mutation adequacy score », « The history of Mutation Testing can be traced back to 1971 in a student paper by Richard Lipton ». ADR-0011 — le survey qui porte la nomination CPH (§II.A, à greper à la rédaction). |
| `inozemtseva-holmes-2014-coverage-icse.pdf` | Inozemtseva & Holmes, *Coverage Is Not Strongly Correlated with Test Suite Effectiveness*, ICSE '14 (Hyderabad), © ACM 978-1-4503-2756-5/14/05 — DOI non imprimé, copie paginée 1..11 (pages ACM 435-445 non citables d'ici). **Affiliation imprimée : University of Waterloo** (la copie est hébergée sur la page UBC de Holmes — l'hébergement n'est pas l'affiliation). sha256 `e56c4dbe3f2255ecd774b1288c60c1cb68893f3b31b7fca39c0156672fdb8317` | p. 1 lue au fichier le 2026-08-12 (titre, abstract, §1) | Vu p. 1, abstract : « coverage, while useful for identifying under-tested parts of a program, should not be used as a quality target because it is not a good indicator of test suite effectiveness » — la phrase qui fonde les seuils-en-candidats. ADR-0011. |
| `lamb-zacchiroli-2022-reproducible-builds.pdf` | Préprint **arXiv:2104.06020v1** (13 avr. 2021, bandeau de marge) de *Reproducible Builds: Increasing the Integrity of Software Supply Chains*, Lamb (Reproducible Builds) & Zacchiroli (Université de Paris/Inria), pied « IEEE Software © 2021 IEEE » — vol/pages/DOI absents : IEEE Software 39(2):62-70 (2022) reste **candidat**. sha256 `eb185aea7b52f91376ae67c05be36e2f3910398bba95cfdb16857e383c175dc0` | p. 1 lue au fichier le 2026-08-12 (titre, abstract) | Définition vue p. 1 : reproductible = « when every build generates bit-for-bit identical results ». ADR-0012. |
| `torres-arias-2019-intoto-usenix.pdf` | Couverture USENIX officielle : Torres-Arias (NYU), Afzali (NJIT), Kuppusamy (Datadog), Curtmola (NJIT), Cappos (NYU), *in-toto: Providing farm-to-table guarantees for bits and bytes*, Proc. 28th USENIX Security Symposium, 14-16 août 2019, Santa Clara, ISBN 978-1-939133-06-9, open access. sha256 `55024dfc786504863c2d3d1932b5010394e09d9d65489e26afb3b050ef493662` | couverture lue au fichier le 2026-08-12 | ADR-0012. |
| `newman-2022-sigstore-ccs.pdf` | Newman, Meyers (Chainguard), Torres-Arias (Purdue), *Sigstore: Software Signing for Everybody*, CCS '22 (7-11 nov. 2022, Los Angeles), p. 2353, **DOI 10.1145/3548606.3560596 imprimé**, licence CC-BY 4.0, 15 p. sha256 `6622c6b0fc6b05a14c9328b956cb13e0898bf157ad17bab0d0ddd6dd1c0fc4cc` | p. 2353 lue au fichier le 2026-08-12 (titre, abstract, §1) | ADR-0012. Premier téléchargement écarté en quarantaine scratchpad (`.MAUVAIS` : placard HotSoS 2023 homonyme) — jamais versé. |
| `cockburn-walking-skeleton-2026-08-12.html` | Alistair Cockburn, page « Walking Skeleton », alistair.cockburn.us (page mutable — copie datée du 2026-08-12). sha256 `b60a1b91129e065395988d420dd3f23a39d2a93c6bffe4643186958cdca80b78` | grep orchestrateur du 2026-08-12 : « walking skeleton » ×21, « tiny implementation of the system » ×1 | Le locus de la définition (12 §5) ; à transcrire au fichier à la rédaction. Crystal Clear et GOOS restent en procurement. |
| `cockburn-walking-skeleton-webarchive-20171205-dl2026-08-12.html` | Instantané Web Archive du 2017-12-05 de la même page (téléchargé le 2026-08-12). sha256 `8234a307099797abaa0d8d4fd9245d780788976c8559cb9441090054dfe14da8` | non lu au-delà du fetch | Corrobore la stabilité d'une page mutable ; les citations se font sur la copie datée primaire. |
| `saltzer-schroeder-1975-protection-2026-08-12.html` | Page d'index MIT de *The Protection of Information in Computer Systems*, Saltzer & Schroeder (web.mit.edu, structure multi-parties — copie datée). sha256 `dcb1a668370b1d6974688b6548fadc82c960c06830835afa0be26b4be08bc934` | grep (« design principles » ×1) | L'artefact porteur est la partie Basic ci-dessous. |
| `saltzer-schroeder-1975-protection-Basic-2026-08-12.html` | Partie I (« Basic Principles ») de Saltzer & Schroeder, *The Protection of Information in Computer Systems*, Proc. IEEE 63(9), sept. 1975 — copie HTML MIT (mutable — datée). **Les huit principes de §I.A.3 tous présents au grep orchestrateur** : economy of mechanism ×3, fail-safe defaults ×2, complete mediation ×2, open design ×2, separation of privilege ×3, least privilege ×4, least common mechanism ×2, psychological acceptability ×2. **Seule la partie I est détenue** ; pagination journal (1278-1308) et DOI 10.1109/PROC.1975.9939 candidats, non portés par cette copie. sha256 `6bc487bbfb454e3bade962e769a6e7d87dff0d81c5d2b35b9ffaadc9beb3a61e` | greps du 2026-08-12 ; §I.A.3 à lire au fichier avant citation verbatim | ADR-0010 (fail-safe defaults → S-G3) et 0012 (least privilege → CI). |
| `slsa-spec-v1.0-levels-2026-08-12.html` | Spec SLSA v1.0, page « Levels » (slsa.dev — mutable, copie datée) ; Build L0-L3 présents au grep ; **bandeau « Retired » constaté sur la copie** — v1.2 est la version courante. sha256 `0534af68137bb9aa8709b1bd19e8acbd86de7236887a0d332cbe7d11fb08464a` | grep du 2026-08-12 | ADR-0012 — version historique ; la version à citer est l'entrée v1.2. |
| `slsa-spec-v1.0-about-2026-08-12.html` | Page « About » de SLSA v1.0 (mutable, copie datée) ; porte le renvoi vers v1.2. sha256 `94a6630c0ec4310ad583a35c0d4576a35100a027e1e6dbdd6ba0c9484e593247` | grep du 2026-08-12 (« Retired » ×1) | Contexte de l'entrée précédente. |
| `slsa-spec-v1.2-build-track-basics-2026-08-12.html` | Spec SLSA **v1.2 (courante)**, page « Build track basics » (mutable — copie datée, **fetch orchestrateur du 2026-08-12**) ; « Build L0-3 » ×19 au grep — la v1.2 a restructuré : plus de page « levels », les définitions des niveaux de build vivent ici. sha256 `3a09da943842375118b49b2df3ae7983f972befd843b7e6b90bc93b20cd61a54` | grep orchestrateur du 2026-08-12 ; sections à lire à la rédaction | ADR-0012 — la version à citer. |
| `vocke-2018-practical-test-pyramid-2026-08-12.html` | Ham Vocke, *The Practical Test Pyramid*, martinfowler.com, 26 févr. 2018 (mutable — copie datée). Attribution constatée au grep : « Mike Cohn » ×3, « Succeeding with Agile » ×1. sha256 `d5f669995439f1c7bb7109a8f5e52044f1b7f39e92115679518d2b762ca39eff` | grep du 2026-08-12 ; sections à lire à la rédaction | ADR-0011 — secondaire ; le primaire (Cohn) est en procurement. |
| `dodds-testing-trophy-2026-08-12.html` | Kent C. Dodds, *The Testing Trophy and Testing Classifications*, kentcdodds.com (mutable — copie datée) — **daté du 3 juin 2021 sur la page** ; le trophy lui-même naît, selon l'article, d'un tweet de févr. 2018. Corrige la date candidate « 2018 » du manifeste (12 §4.1). sha256 `6a144f47f54fd785533b60659fb5b3dcf9ade632780e160cf02a254c1bacaa38` | grep du 2026-08-12 (« Testing Trophy » ×26) ; sections à lire à la rédaction | ADR-0011 — l'alternative instruite à la pyramide. |

## Dettes de registre

1. ~~L'article original de Knight & Leveson~~ — **fermée le 2026-07-30** :
   article complet apporté par le mainteneur, lu aux sections citées
   (voir l'entrée). Reste ouverte la variante mineure : la copie est le
   manuscrit MIT OCW, pas le tiré IEEE — la pagination journal (96-109)
   ne doit pas être citée par numéro de page depuis cette copie.

2. ~~Pages de titre des deux PDFs compagnons~~ — **fermée le 2026-07-30**
   (entrées mises à jour). Venue du « Reply » : deux fiches web
   concordantes (ACM DL, DOI 10.1145/382294.382710 : SIGSOFT SEN 15(1),
   janv. 1990, pp. 24-35) — la page DOI elle-même refuse le fetch
   automatisé (403) ; résidu minime : contrôle visuel de la fiche avant
   citation formelle dans une publication.

3. ~~Artefact primaire Reclaim~~ — **fermée le 2026-07-30** (FAQ sécurité
   + README attestor-core détenus, voir les entrées). Restes : le
   whitepaper ou l'article technique du modèle proxy reste à fetcher avant
   toute citation *détaillée* du protocole (la FAQ couvre le modèle de
   menace déclaré, pas la construction) ; le README n'est pas lu au-delà
   du fetch ; les chiffres vendeur (889 sources, preuves en 2–4 s) restent
   non vérifiés sur artefact détenu.

4. Outillage sidecar (extraction texte des PDFs) — les greps de ce
   registre portent sur les HTML bruts et sur des lectures visuelles ; les
   PDFs ne sont pas encore greppables.

5. Le Lemme 8 de Chainlink OCR (« Observation integrity ») est détenu
   **dans la biblio Kraidle**
   (`F:\Kraidle\biblio\08-distributed\chainlink-ocr.pdf.sidecar`, grep
   vérifié le 2026-07-30 : « v is either the observation of a correct
   oracle or lies between the observations of two correct oracles »).
   Décision à prendre : copie locale ou référence croisée inter-projets.

6. **Corps de Dong et al. 2010** (`dong-2010-pvldb-copying-R120.pdf`) non
   lu (page de titre + intro seulement) ; le prédécesseur PVLDB 2009
   (« Integrating Conflicting Data: The Role of Source Dependence », où naît
   le mécanisme des fautes partagées) n'est pas détenu. À lire / fetcher
   avant que l'axe R2 (2c) ne cite le précédent (10 §4.2, dette §10.1).


### Fetchés à l'ouverture de S3 (2026-08-12) — corpus transport (TLSNotary) et corpus licence

Acquisition par 5 workers `claude-opus-5[1m]` (run `wf_f92df5a1-844`, gate
de résolution verte en tête) + 1 fetch orchestrateur. **Contrôle
orchestrateur du 2026-08-12, même passe** : sha256 recalculé en destination
pour les 67 pièces — **65/65 concordants avec les rapports de workers, 0
divergence** (l'entrée-alias « SEE-ABOVE » du pack T3 résolue : hash
concordant sous le nom réel) ; marqueurs greppés sur copie par
l'orchestrateur là où la colonne « lu » le dit. Corps non lus sauf
mention : les lectures de section se font à la rédaction des ADR,
une-citation-un-grep (S-G5 mécanise désormais l'existence au corpus).

**Faits d'état constatés par la passe, à instruire dans ADR-0015** :
(a) le serveur notaire est **déprécié** par le projet (page « Notary
Server (Deprecated) ») et `notary.pse.dev` ne répond plus — la
notarisation hébergée n'est pas un service sur lequel s'appuyer ;
(b) **aucun binaire vérificateur autonome, WASM de vérification ou service
de vérification n'existe** (résultat négatif établi par le pack T3 sur le
sitemap complet) — l'intégration passe par les crates ;
(c) les crates `tlsn*` **ne sont pas publiées sur crates.io** (contrôle
R-8 : recherche registre vide) — toute dépendance serait un épinglage git
par révision, pas une version de registre ;
(d) version amont : 0.1.0-alpha.15 publiée, alpha.16-pre en rustdoc — un
**alpha**, et la doc n'est pas versionnée (Docusaurus « current ») ;
(e) TLS 1.2 seulement ; sur TLS 1.3 deux pages officielles se
contredisent (intro « on the roadmap » vs FAQ « no immediate plans ») —
les deux copies sont détenues ;
(f) réserves des workers consignées aux rapports (run `wf_f92df5a1-844`) :
pages `/docs/mpc/*` non acquises (couverture partielle assumée du
protocole bas niveau), trois pièces T3 versées non dépouillées, taille de
l'artefact de preuve non documentée par l'amont.

**Pack T1 — documentation du protocole (12 pièces)**

| fichier | ce que c'est (constaté) | lu | sha256 |
|---|---|---|---|
| `tlsnotary-docs-intro-2026-08-12.html` | « Introduction \| TLSNotary », tlsnotary.org/docs/intro (Docusaurus, docs NON versionnées — aucune date de modification affichée ; éditeur revendiqué en page : Privacy Stewards of Ethereum). Modèle de confiance du notaire généraliste, oracle problem, TLS 1.2 | non, sauf marqueurs | `d12e4c4cfc813658742928634c742877b4c44f82cd692796a8fb8f305a30cff1` |
| `tlsnotary-docs-protocol-mpc-tls-2026-08-12.html` | « MPC-TLS \| TLSNotary » — en-tête de section : le vérificateur ne voit que le chiffré ; le prouveur ne peut ni construire seul ni forger | non, sauf marqueurs | `4c732f400967352976e3585ff665536578974d2bc44d11aaf6f98ae43c00e3cb` |
| `tlsnotary-docs-protocol-mpc-tls-handshake-2026-08-12.html` | « Handshake \| TLSNotary » — clé de session en parts (aucune partie ne détient la clé entière) ; face à un vérificateur malveillant la garantie est celle du MPC, plus celle de TLS | non, sauf marqueurs | `7c173e4f75ed7c13bd532a9511f7a77c8fe8185d23672b114856def70eccd454` |
| `tlsnotary-docs-protocol-mpc-tls-encryption-2026-08-12.html` | « Encryption, Decryption, and MAC Computation \| TLSNotary » — chiffrement aveugle ; la page se déclare elle-même simplifiée (« more nuanced than what we have described here ») | non, sauf marqueurs | `603e943046c22820ed69612d602b49c7350dee8c0d1d895f8bd21557a4d3354d` |
| `tlsnotary-docs-protocol-notarization-2026-08-12.html` | « Notarization \| TLSNotary » — engagements authentifiés signés par le notaire sans qu'il voie le clair | non, sauf marqueurs | `3b8660a65e28e52dd17c5cf6d6e45aedc1494a204c528510656097d360a554c6` |
| `tlsnotary-docs-protocol-verification-2026-08-12.html` | « Verification \| TLSNotary » — ce que contrôle le vérificateur d'une présentation | non, sauf marqueurs | `2d7e08356d3828d6218955d2d9385332e7db4210bbd56b998a2945c1d89de894` |
| `tlsnotary-docs-protocol-commit-strategy-2026-08-12.html` | « Commit Strategy \| TLSNotary » — stratégies d'engagement sur le transcript | non, sauf marqueurs | `42956d9763ba35b242bbf3a2263b91d4fcc0aef55baa19af1d62e9bbaa8b8f54` |
| `tlsnotary-docs-protocol-proxy-mode-2026-08-12.html` | « Proxy Mode \| TLSNotary » — le mode qui troque le MPC contre une hypothèse de chemin réseau | non, sauf marqueurs | `9bcc2ec907c33e0e773d13d497c4baf9f36de03cbcb356097fa6285480e35271` |
| `tlsnotary-docs-protocol-server-identity-privacy-2026-08-12.html` | « Server Identity Privacy \| TLSNotary » | non, sauf marqueurs | `78c3fce77885f07d14449c07519697fcf98490590a6f6903456483a79a2befbe` |
| `tlsnotary-docs-protocol-configuration-2026-08-12.html` | « Configuration \| TLSNotary » | non, sauf marqueurs | `55326bab41887b3adba1481fd2ed8ed0065f4dc72e0178a5a466bdb600aeb519` |
| `tlsnotary-docs-glossary-2026-08-12.html` | « Glossary \| TLSNotary » — vocabulaire officiel (Prover/Verifier/Notary/attestation/presentation) | non, sauf marqueurs | `ee38348beaca65c6358f7f19b8ca40978290bb94e0785c7f5a40d12f60b44be2` |
| `tlsnotary-docs-faq-2026-08-12.html` | « Frequently Asked Questions \| TLSNotary » — FAQ courante ; sur TLS 1.3 elle CONTREDIT la page intro (« no immediate plans » vs « on the roadmap ») — divergence consignée, les deux copies détenues | non, sauf marqueurs | `2f706555153e881fbe6a394224465bd295c6ea631ab07313e834e8b3e5331563` |

**Pack T2 — dépôt amont et contrôle R-8 (25 pièces)**

| fichier | ce que c'est (constaté) | lu | sha256 |
|---|---|---|---|
| `tlsn-repo-readme-raw-2026-08-12.md` | README.md brut de tlsnotary/tlsn (branche main) | non, sauf marqueurs | `b95e34f3c6315d5502d91bc3aa652419028e04216fba666338c0c0e9296ff657` |
| `tlsn-repo-readme-rendered-2026-08-12.html` | README rendu GitHub de tlsnotary/tlsn | non, sauf marqueurs | `7cf1fd1f22dc7d7359f82592a94c1203677b10806f4fcaa073567ab938d424af` |
| `tlsn-repo-metadata-api-2026-08-12.json` | métadonnées GitHub API du dépôt (licence déclarée du projet, langages, dates) | non, sauf marqueurs | `4717e7aa57978a5d9b764e31f4c4d710442d3455c19c8456e3a22a32029768e4` |
| `tlsn-repo-root-contents-api-2026-08-12.json` | inventaire API de la racine du dépôt (branche main) | non, sauf marqueurs | `d81800c0faf797f0e87cfa33521b4a689a8e79c1b52cdfcedbd3c64980ba6e5f` |
| `tlsn-repo-crates-dir-api-2026-08-12.json` | inventaire API de crates/ (les crates réelles du workspace amont) | non, sauf marqueurs | `3df954a06fac2598a8aa6ac77d1093d7659c25cd2d2c9e33e96dbc4c703c25ad` |
| `tlsn-repo-workspace-cargo-toml-2026-08-12.toml` | manifeste workspace Cargo de tlsnotary/tlsn | non, sauf marqueurs | `2acabd886a2460aa5ba705d67600bda1f9af8c185714af6b95c5fb52694bb427` |
| `tlsn-repo-cargo-lock-2026-08-12.lock` | Cargo.lock amont complet (graphe de dépendances réel du projet) | non, sauf marqueurs | `eff3d7223fcd9d8ce478042eb8d40a49202f1c3fc111c42db36cbc8b01f0f2a0` |
| `tlsn-repo-releases-api-2026-08-12.json` | liste API complète des releases amont | non, sauf marqueurs | `2f773294a63004885926d978c9000733055ed3d61721e863e629311901aa5d5a` |
| `tlsn-repo-releases-page-2026-08-12.html` | page releases rendue | non, sauf marqueurs | `1809b372e88a2a1ae0b925f54bbb8b109c64527d189a8202a879ba33e58b331c` |
| `tlsn-repo-ci-workflow-2026-08-12.yml` | workflow CI amont (.github/workflows/ci.yml) | non, sauf marqueurs | `5d0db5e752ac4a4f24abed57eb81a26e031a353151a58047e23708724e8f85c0` |
| `tlsn-crate-tlsn-cargo-toml-2026-08-12.toml` | manifeste crate `tlsn` (« The TLSNotary library ») | non, sauf marqueurs | `ed9bc7d226bc34ea6b3c9dedec9f9d83b92bb7e4fd8c3d4ca6afac6bfbe5dee1` |
| `tlsn-crate-core-cargo-toml-2026-08-12.toml` | manifeste crate `tlsn-core` | non, sauf marqueurs | `9c353a7559f88792092b13b5f06f24fc41b75d1988d72c32b8c16c5498249c39` |
| `tlsn-crate-attestation-cargo-toml-2026-08-12.toml` | manifeste crate `tlsn-attestation` | non, sauf marqueurs | `366c21831bd8376fa0996fbb1627be4578f49e4d3e555ff44b955a200b5687f3` |
| `tlsn-crate-formats-cargo-toml-2026-08-12.toml` | manifeste crate `tlsn-formats` | non, sauf marqueurs | `400ee619810f6c184c9ebc249bf51bd5609f1d353076c7a009888d0473854427` |
| `tlsn-crate-sdk-core-cargo-toml-2026-08-12.toml` | manifeste crate `tlsn-sdk-core` | non, sauf marqueurs | `e63b9712bc15e25e5bd65c5f327a80bd81bdc99b0fce5294c9800fcee473b0c8` |
| `tlsn-crate-mpc-tls-cargo-toml-2026-08-12.toml` | manifeste crate `tlsn-mpc-tls` | non, sauf marqueurs | `b1e986b2e6a0df50cca1e39b4d6ebe1072fb96010f990bb8dbcb9f66688ca2ea` |
| `tlsn-crate-tls-core-cargo-toml-2026-08-12.toml` | manifeste crate `tlsn-tls-core` | non, sauf marqueurs | `7ef5558491b3cdc03defea8f3539d1b22af507f37f45badc06b4908d6ca53078` |
| `tlsn-crate-wasm-cargo-toml-2026-08-12.toml` | manifeste crate `tlsn-wasm` | non, sauf marqueurs | `9de8d98b446eb4a1be0c7335f53ecca289676529545cde5138b4d1e0b4199b60` |
| `cratesio-search-tlsn-2026-08-12.json` | recherche crates.io q=tlsn — contrôle R-8 : les crates `tlsn*` du projet N'EXISTENT PAS sur le registre officiel (consommation git seulement) | non, sauf marqueurs | `4fccad39e4d21d9c2fa2c4a92c5790fe3a1ef9fd0b969c3ef1e4b1b50ac9e1d5` |
| `cratesio-notary-client-2026-08-12.json` | fiche crates.io `notary-client` (homonymie à surveiller — contrôle R-8) | non, sauf marqueurs | `79a7a09ca9d17935936e7184bc1d46c08090167ce2fc0679eed03060b314b256` |
| `cratesio-notary-client-owners-2026-08-12.json` | owners crates.io de `notary-client` | non, sauf marqueurs | `cf11dc5c13b12d5b9b606cde9847542b7bbd664fc41357e7c2d9ef0de9a8c3d5` |
| `cratesio-rangeset-owners-2026-08-12.json` | owners crates.io de `rangeset` (dépendance amont publiée par tlsnotary) | non, sauf marqueurs | `08115d768eb06cb8eb07dc38b25b4d5dc3badfbcf21e39285909b18ecd767659` |
| `cratesio-serio-owners-2026-08-12.json` | owners crates.io de `serio` (idem) | non, sauf marqueurs | `08115d768eb06cb8eb07dc38b25b4d5dc3badfbcf21e39285909b18ecd767659` |
| `cratesio-web-spawn-owners-2026-08-12.json` | owners crates.io de `web-spawn` (idem) | non, sauf marqueurs | `08115d768eb06cb8eb07dc38b25b4d5dc3badfbcf21e39285909b18ecd767659` |
| `tlsnotary-org-repos-api-2026-08-12.json` | liste API des 42 dépôts de l'organisation GitHub tlsnotary | non, sauf marqueurs | `2d0e1c7f5b8d26202541e94e222e21f89cc553f6bf621e87b524224189b01873` |

**Pack T3 — notariat, vérification, sources épinglées (20 pièces nouvelles ; 4 pages du pack recoupent T1 à octets identiques)**

| fichier | ce que c'est (constaté) | lu | sha256 |
|---|---|---|---|
| `tlsnotary-docs-notary-server-2026-08-12.html` | « Notary Server (Deprecated) \| TLSNotary » — LA pièce d'état : le serveur notaire est déprécié par le projet lui-même (« Deprecated » greppé par l'orchestrateur) | non, sauf marqueurs | `d624197d0b19e6a7f2e6f6766437a8acf07c77c4294c773bb70df34e7121c29f` |
| `tlsn-github-release-v0.1.0-alpha.13-api-2026-08-12.json` | release amont v0.1.0-alpha.13 (API GitHub) | non, sauf marqueurs | `2b598ca12755fb2a371af7210d4900fc3d489fdb2667b25db791facb8b429bc6` |
| `tlsn-github-release-v0.1.0-alpha.15-api-2026-08-12.json` | release amont v0.1.0-alpha.15 (API GitHub, published_at 2026-05) | non, sauf marqueurs | `6fa2b94a142208ca92af3d889908c6ca8940b83818e57dc535b4a8dddc2786c6` |
| `tlsn-crate-attestation-presentation-rs-g0fe3c32d.rs` | source amont crates/attestation/src/presentation.rs, épinglé au commit 0fe3c32d | non, sauf marqueurs | `0d03f8373ac9e6b7e03c1cc830e7c34c81a64ed47c1316363cb89c915c761de2` |
| `tlsn-crate-attestation-lib-rs-g0fe3c32d.rs` | source amont crates/attestation/src/lib.rs (doc de crate), épinglé 0fe3c32d | non, sauf marqueurs | `be78d7e5335170398141ba1d2b6dba3b516179071bd049d4088139d73b027a0b` |
| `tlsn-crate-attestation-proof-rs-g0fe3c32d.rs` | source amont crates/attestation/src/proof.rs, épinglé 0fe3c32d | non, sauf marqueurs | `7727ef53595f936beb0796786338d9ba81fbe2a9ebae0f122520bcd3dc304b6e` |
| `tlsn-crate-attestation-serialize-rs-g0fe3c32d.rs` | source amont crates/attestation/src/serialize.rs, épinglé 0fe3c32d | non, sauf marqueurs | `ec69c500a5da3f4a7de826cd964dc5fa7a18497857536b91e2ab0e92cbff1f05` |
| `tlsn-crate-attestation-signing-rs-g0fe3c32d.rs` | source amont crates/attestation/src/signing.rs, épinglé 0fe3c32d | non, sauf marqueurs | `7ebab2b84027a88f336944ff4e1fc0065770eeeac2aa7205988ef36601d62edb` |
| `tlsn-example-attestation-verify-rs-g0fe3c32d.rs` | exemple officiel attestation_verify (crates/examples/attestation/verify.rs), épinglé 0fe3c32d | non, sauf marqueurs | `70c76fe2beddadb78cbb19fec4dcc412ee8d2093ef990af9b2849e9b53fa0873` |
| `tlsn-example-attestation-present-rs-g0fe3c32d.rs` | exemple officiel attestation_present, épinglé 0fe3c32d (rapporté par le worker sous une entrée-alias « SEE-ABOVE » — hash concordant contrôlé par l'orchestrateur) | non, sauf marqueurs | `486515502b12b62cb93d334aec477f97639aa595ce6365d68f03ce392f96edf8` |
| `tlsn-example-attestation-readme-g0fe3c32d.md` | README de l'exemple attestation amont, épinglé 0fe3c32d | non, sauf marqueurs | `c8729e3ca737b1dc5dd324331830356dab197ac942a824db5faa7670201106b9` |
| `tlsnotary-blog-public-verifiability-2026-06-17-dl2026-08-12.html` | billet officiel « Zero-knowledge ≠ trustless: what “publicly verifiable” means… » (2026-06-17) — le projet lui-même sur la portée de la vérifiabilité | non, sauf marqueurs | `f6b499badf00c9c2356820cc78d265d947af95d43c145eeded46fdb709886dcc` |
| `tlsnotary-blog-where-trust-lives-2026-06-23-dl2026-08-12.html` | billet officiel « Where does your trust live? Cryptographic soundness and the TEE … » (2026-06-23) | non, sauf marqueurs | `8d6c6c658947fddef6a5896607fc96ebc719204c43c1bf99db93582801af6e6c` |
| `tlsnotary-blog-benchmarks-2025-08-31-dl2026-08-12.html` | billet officiel « TLSNotary Performance Benchmarks (August 2025) » | non, sauf marqueurs | `68cdeb7766d09e0ecf1b9b61de3861a6fd200e633a8f6c7525414de593866bca` |
| `tlsnotary-docs-extension-verifier-2026-08-12.html` | « Verifier Server \| TLSNotary » (rubrique Browser Extension) | non, sauf marqueurs | `5dfe57e579ac645323564b24290554715a4a4ca5d806498d9e9ff03ccf94e80b` |
| `tlsn-rustdoc-crate-tlsn-2026-08-12.html` | rustdoc générée du crate `tlsn`, version affichée 0.1.0-alpha.16-pre | non, sauf marqueurs | `b8ea6cacfab2e74f5c2af911754118f5cd0e41468cb809aaff0e2de9458d29fc` |
| `tlsn-rustdoc-crate-tlsn-core-2026-08-12.html` | rustdoc générée du crate `tlsn-core`, version affichée 0.1.0-alpha.16-pre | non, sauf marqueurs | `68196fdddd5d4e540a32dba248834180edb0fe51265988d1077b3aa1d5b3de49` |
| `tlsn-crate-attestation-cargo-toml-g0fe3c32d.toml` | manifeste crates/attestation/Cargo.toml épinglé 0fe3c32d (octets identiques à la copie T2 non épinglée — concordance constatée) | non, sauf marqueurs | `366c21831bd8376fa0996fbb1627be4578f49e4d3e555ff44b955a200b5687f3` |
| `tlsnotary-docs-quickstart-rust-2026-08-12.html` | « Rust Quick Start \| TLSNotary » | non, sauf marqueurs | `2e62b53da1e6fb5c896f850ebf57ea61645e2eaeda03925135ade5246ad3e8ad` |
| `tlsnotary-docs-quickstart-2026-08-12.html` | « Quick Start \| TLSNotary » (index de rubrique) | non, sauf marqueurs | `99929539df811f498372ae64d148e8388890c603df43d84530876506183037c6` |

**Pack L1 — textes canoniques des licences (ADR-0014) (5 pièces)**

| fichier | ce que c'est (constaté) | lu | sha256 |
|---|---|---|---|
| `apache-license-2.0-2026-08-12.txt` | texte canonique Apache License 2.0 (apache.org/licenses/LICENSE-2.0.txt) — §3 « Grant of Patent License » greppé par l'orchestrateur | marqueurs greppés | `cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30` |
| `apache-license-2.0-page-2026-08-12.html` | page canonique apache.org de la licence (HTML) | marqueurs greppés | `33492ade6e67d48fac256d155edd01b1a9a9866f77586698ff6d714b49699a5f` |
| `osi-mit-license-2026-08-12.html` | The MIT License, page canonique Open Source Initiative (opensource.org/license/mit) | marqueurs greppés | `4ce24f62a5dcaa89feb92913bc8f7a2608cf6965a84436578db3bbebf628f861` |
| `gnu-agpl-3.0-2026-08-12.txt` | texte intégral GNU AGPL-3.0 (gnu.org, text/plain, 661 lignes) — §13 « Remote Network Interaction » greppé par l'orchestrateur (la clause qui pèse sur un vérificateur offert en service) | marqueurs greppés | `0d96a4ff68ad6d4b6f1f30f713b18d5184912ba8dd389f86aa7710db079abcb0` |
| `gnu-agpl-3.0-2026-08-12.html` | page canonique gnu.org AGPL-3.0 (HTML) | marqueurs greppés | `3cea8a3640e0a825b1e6f975994ef107fe39b0aed40cddcf876970bb12a6bbcf` |

**Pack L2 — convention d'écosystème Rust (4 pièces)**

| fichier | ce que c'est (constaté) | lu | sha256 |
|---|---|---|---|
| `rust-lang-rust-copyright-2026-08-12.txt` | fichier COPYRIGHT du dépôt rust-lang/rust (branche master) — le compilateur lui-même est dual-licencié | marqueurs greppés | `172020dbfd5b53a226dfde77616190a48dcff519b0bc0e6deb91a8450782c4af` |
| `rust-lang-rust-readme-2026-08-12.md` | README.md de rust-lang/rust (section licence) | marqueurs greppés | `b3f6ef2fef88b98cb9ec013a5c86213095e53e40eb228679574e4d06517f33c8` |
| `rust-api-guidelines-necessities-2026-08-12.html` | Rust API Guidelines, page « Necessities » — ligne directrice C-PERMISSIVE (« permissive » greppé par l'orchestrateur) | marqueurs greppés | `1e0a791145f72b6e7ff496ca429fc9aa6e87367f7050e83cbbc3d26c814649ca` |
| `cargo-reference-manifest-2026-08-12.html` | The Cargo Book, « The Manifest Format » (canal stable) — champ `license` SPDX | marqueurs greppés | `3e02b4c928b55202e53599abf6a51fe8a24938bb14a446d8b7d5ebc77cd0cb57` |

**Acquisition orchestrateur (1 pièce)**

| fichier | ce que c'est (constaté) | lu | sha256 |
|---|---|---|---|
| `coingecko-methodology-2026-08-12.html` | CoinGecko, page méthodologie (coingecko.com/en/methodology) — fetch orchestrateur du 2026-08-12 ; « the VWAP of all remaining tickers » greppé sur la copie (2 occurrences) : la citation de 10 §3 est désormais adossée à des octets détenus (décharge partielle de la dette S2 §10.4) | grep VWAP | `8edbb0d566706f9f67ee0b7ee19cdcba305940c323c573ebcb862b1a8f80cd94` |


### Fetchés à la phase B de S3 (2026-08-13) — sources normatives des drafts ADR-0015/0016

Workers `claude-opus-5` (run `wf_8db62dce-162`) ; sha256 recalculés par
l'orchestrateur en destination : **5/5 concordants**. Textes IETF/WHATWG
librement redistribuables (les RFC portent leur licence dans le texte).

| fichier | ce que c'est (constaté) | lu | sha256 |
|---|---|---|---|
| `rfc-8949-cbor-2026-08-13.txt` | RFC 8949, STD 94 — Bormann & Hoffman, *Concise Binary Object Representation (CBOR)*, IETF Standards Track, déc. 2020 (obsolète RFC 7049) — le texte canonique que l'ADR-0002 invoquait au travers de la copie C2PA ; §4.2.1 Core Deterministic Encoding Requirements | worker : §4.2.1 lu ; orchestrateur : versement contrôlé | `f1164a5b31a39350ad46abe29b83575eb933ca6c45366989c118b6b1058a214a` |
| `rfc-9052-cose-2026-08-13.txt` | RFC 9052, STD 96 — Schaad, *CBOR Object Signing and Encryption (COSE): Structures and Process*, IETF Standards Track, août 2022 (obsolète RFC 8152) ; §4.2 Signing with One Signer (`Cose_Sign1`, tag 18) | worker : §4.2 lu ; orchestrateur : versement contrôlé | `01eecd7f646537600e7aad665b1fa581ce6ec33dae4ef4add0997aaf38cd0a45` |
| `rfc3986-uri-generic-syntax.txt` | RFC 3986, STD 66 — Berners-Lee, Fielding, Masinter, *Uniform Resource Identifier (URI): Generic Syntax*, janv. 2005 ; §6 Normalization and Comparison — la source-qui-tranche attendue d'ADR-0016 | worker : §6 lu ; orchestrateur : versement contrôlé | `3102dae4b68cebe40337730312fcb612297b8928547267e8b3d1ee6002b2d683` |
| `rfc9110-http-semantics.txt` | RFC 9110, STD 97 — Fielding, Nottingham, Reschke, *HTTP Semantics*, juin 2022 ; §4.2.3 (équivalence d'URI http/https) | worker : §4.2.3 lu ; orchestrateur : versement contrôlé | `21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a` |
| `whatwg-url-standard-dl2026-08-12.html` | WHATWG, *URL Standard*, Living Standard — « Last Updated 6 July 2026 » constaté à la balise `<time>` ; **page mutable et non versionnée** : l'ancre opposable est le couple (date de copie, sha256) — alternative instruite (et rejetée en draft) d'ADR-0016 | worker : sections normalisation lues ; orchestrateur : versement contrôlé | `a4295a30e0203fc5b63a83a10c04daeef8a9741ff727e9beec89d2ae0c50a0de` |


### Fetchés à la phase C de S3 (2026-08-13) — vecteurs d'autorité de l'empreinte SHA-256

Acquisition initiale par le worker cœur mort à la limite de session (aucune
URL consignée) ; **provenance re-établie par l'orchestrateur le
2026-08-13** : re-téléchargement depuis les URL officielles NIST, octets
identiques aux trois pièces locales (même geste que `parnas`/`meyer` en
S2.5), sha256 recalculés à l'écriture de cette section. Textes NIST : œuvre
du gouvernement fédéral américain, non soumise au copyright (17 U.S.C.
§105). Chaque vecteur employé par `crates/shogen-core/tests/`
`empreinte_vecteurs.rs` a été retrouvé au grep dans les `.rsp` officiels
par le worker de reprise, puis le mutant K0 vu tuer par l'orchestrateur.

| fichier | ce que c'est (constaté) | lu | sha256 |
|---|---|---|---|
| `nist-cavp-sha-byte-test-vectors-2026-08-13.zip` | NIST CAVP, *SHA Test Vectors for Hashing Byte-Oriented Messages* (`shabytetestvectors.zip`, csrc.nist.gov) — les `.rsp` SHA256ShortMsg/LongMsg | vecteurs employés greppés aux `.rsp` | `929ef80b7b3418aca026643f6f248815913b60e01741a44bba9e118067f4c9b8` |
| `nist-fips-180-4-secure-hash-standard-2026-08-13.pdf` | NIST, *FIPS PUB 180-4 — Secure Hash Standard (SHS)*, août 2015 (nvlpubs.nist.gov) — constantes §4.2.2, état initial §5.3.3, bourrage §5.1.1 | sections employées par empreinte.rs | `0455b406d89648d20cbde375561e19c245b9815e894164c2670772e3d54deb82` |
| `nist-sha256-examples-intermediate-values-2026-08-13.pdf` | NIST CSRC, *SHA-256 Examples* (valeurs intermédiaires, csrc.nist.gov) — « abc » et le message à deux blocs | exemples employés | `7006b6549dad2fc8c6f29417a921f2e48208157ef496a7e1e1d7d17c5cc1e7db` |

### Versés à la phase C de S3 (2026-08-13) — chantiers typeur et transport (vague 1)

Deux origines, une même adjudication orchestrateur du 2026-08-13 :
- **RFC du typeur** : acquises par le worker Y (chantier typeur) qui en avait
  besoin pour la grammaire du dire (JSON) et de l'instant (date-time) — il ne
  les a pas contournées, il les a acquises et a demandé le versement ;
  **provenance re-établie par l'orchestrateur** : re-téléchargement depuis
  rfc-editor.org, octets identiques (sha256 recalculés, concordants avec le
  rapport du worker). Textes IETF : reproduction autorisée par le Trust Legal
  Provisions pour usage de référence ; copies locales non redistribuées.
- **Sources amont du chantier T** : cinq fichiers du dépôt `tlsnotary/tlsn`
  au commit épinglé `0fe3c32d35382b3f290a43c4156399ca4512bb89` (le HEAD
  courant au 2026-08-13, constaté par `git ls-remote`), réellement employés
  par le conducteur de session et le compagnon — le worker T avait consigné
  que cinq de ses affirmations reposaient sur le clone local et non sur le
  registre ; **provenance établie par l'orchestrateur** : fetch
  raw.githubusercontent.com au commit exact, sha256 recalculés, 5/5
  concordants avec le rapport du worker.

| fichier | ce que c'est (constaté) | lu | sha256 |
|---|---|---|---|
| `rfc-8259-json-2026-08-13.txt` | RFC 8259, T. Bray (ed.), Textuality, *The JavaScript Object Notation (JSON) Data Interchange Format*, IETF Standards Track, déc. 2017 (obsolète RFC 7159), 28 360 octets — sections lues et citées par le typeur : §4 (unicité des noms), §6 (nombres), §7 (chaînes et échappements), §8.1 (UTF-8) | sections employées (worker Y) | `61a5378f4255c720beb2a4b4a63b29540147c140f36988bf086291989b4cd2d7` |
| `rfc-3339-datetime-2026-08-13.txt` | RFC 3339, G. Klyne (Clearswift) & C. Newman (Sun Microsystems), *Date and Time on the Internet: Timestamps*, Standards Track, juil. 2002, 35 064 octets — sections lues et citées : §5.6 (ABNF date-time, NOTE sur la casse de « T »/« Z »), §5.7 (bornes), Appendix C (bissextile) | sections employées (worker Y) | `9ab2b8864a85dca73a88f49b0927bc7bc85f596926e4fd1890905777924e700a` |
| `tlsn-example-attestation-prove-rs-g0fe3c32d.rs` | exemple officiel attestation_prove (crates/examples/attestation/prove.rs), épinglé 0fe3c32d — la notarisation, pièce centrale du montage Notary, modèle du conducteur de session | non, sauf marqueurs | `7f913bc5d63e05214d281ae38531c8cea8acc219fb713f4d798e9524d05dcaa5` |
| `tlsn-crate-examples-lib-rs-g0fe3c32d.rs` | crates/examples/src/lib.rs amont, épinglé 0fe3c32d — porte MAX_SENT_DATA/MAX_RECV_DATA repris par le conducteur | non, sauf marqueurs | `c77b526e0c1cce9c06477bdd544a4bdcb71aa940b265eb7a68ff85562a43183a` |
| `tlsn-crate-core-webpki-rs-g0fe3c32d.rs` | crates/core/src/webpki.rs amont, épinglé 0fe3c32d — `RootCertStore::mozilla()`, le magasin de racines compilé dans le compagnon | non, sauf marqueurs | `24dc64efd9371b37739b0f22e01efba03b5e2762295c73dbbca8582ae9960bc2` |
| `tlsn-crate-attestation-connection-rs-g0fe3c32d.rs` | crates/attestation/src/connection.rs amont, épinglé 0fe3c32d — la ligne qui établit que le certificat est validé à `connection_info.time` (les fixtures ne pourrissent pas à l'expiration du certificat) | non, sauf marqueurs | `7e54a13f969cb768cb270e2ab04360446d330745a501454d1bd3832515ebbeb3` |
| `tlsn-crate-attestation-provider-rs-g0fe3c32d.rs` | crates/attestation/src/provider.rs amont, épinglé 0fe3c32d — `CryptoProvider::default()` = `ServerCertVerifier::mozilla()` | non, sauf marqueurs | `f4f964789075a7606f3a10cd5b8542d2ebf9a970dfd5098d9db18a1c5f044657` |
