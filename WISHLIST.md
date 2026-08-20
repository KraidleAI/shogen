# Shōgen — liste de courses bibliographique

Papiers que le projet doit détenir et que les canaux libres n'ont pas
fournis (recherches du 2026-07-30). Pour chacun : la référence complète,
pourquoi il est nécessaire, et où il se trouve derrière paywall.

## Priorité 1 — bloque R-1

- [x] ~~**Littlewood & Miller, IEEE TSE 15(12):1596-1614, déc. 1989**~~ —
  **apporté par le mainteneur le 2026-07-30** (tiré journal authentique),
  enregistré `biblio/littlewood-miller-1989-tse.pdf`, lu pp. 1596-1604,
  citations vérifiées à l'INDEX. R-1 n'est plus bloquée.

## Priorité 2 — utiles, non bloquants

- [ ] **Eckhardt & Lee, *A Theoretical Basis for the Analysis of
  Multiversion Software Subject to Coincident Errors*, IEEE TSE
  SE-11(12):1511-1517, décembre 1985.** DOI : `10.1109/TSE.1985.231895`.
  Le **mémorandum NASA équivalent est déjà détenu**
  (`biblio/eckhardt-lee-1985-tm86369.pdf`) — le tiré IEEE ne sert qu'à
  citer la pagination journal et à vérifier d'éventuelles différences
  TM/journal.
- [ ] **Knight & Leveson, IEEE TSE 12(1):96-109, janvier 1986 — le tiré
  journal.** Le manuscrit complet est détenu (copie MIT OCW) ; le tiré ne
  sert qu'à citer la pagination journal (dette 1 de l'INDEX).

## Priorité 3 — S2.5 fondations d'ingénierie (demandes formées le 2026-08-12)

Identités constatées sur fiche éditeur par le worker de sweep du
2026-08-12 (run `wf_e63a0e8d-7e7` ; ISBN lus sur fiche, jamais de
mémoire) ; tentatives de copie ouverte légitime toutes vides (les
rediffusions pirates — dokumen.pub, z-lib et parentes — sont traitées
comme inexistantes ; un prêt contrôlé Internet Archive n'est pas un accès
ouvert). Identité finale à re-établir sur l'exemplaire acquis.

- [ ] **Cohn, *Succeeding with Agile: Software Development Using Scrum*,
  Addison-Wesley Professional, 26 oct. 2009, 512 p. — ISBN-13
  978-0-321-57936-2 (ISBN-10 0-321-57936-4 ; eBook 978-0-321-77038-2).**
  Fiche : `informit.com/store/succeeding-with-agile-software-development-using-scrum-9780321579362`.
  Tentatives : fiche éditeur (pas de texte intégral) ; site auteur
  mountaingoatsoftware.com (chapitres d'échantillon contre e-mail
  seulement, lien blog 404). **Usage : ADR-0011** — origine de la pyramide
  de tests ; chapitre visé : ch. 22 « The Test Automation Pyramid ».
- [ ] **Humble & Farley, *Continuous Delivery: Reliable Software Releases
  through Build, Test, and Deployment Automation*, Addison-Wesley
  Signature Series (Fowler), 27 juil. 2010 (©2011), 512 p. — ISBN-13
  978-0-321-60191-9 (ISBN-10 0-321-60191-2 ; eBook 0321770420).**
  Fiche : `informit.com/store/continuous-delivery-reliable-software-releases-through-9780321601919`.
  Tentatives : fiche éditeur ; continuousdelivery.com (extraits contre
  inscription seulement). Divergence constatée : publication 2010,
  copyright 2011 — trancher sur l'exemplaire. **Usage : ADR-0013** — le
  pipeline.
- [ ] **Forsgren, Humble, Kim, *Accelerate: The Science of Lean Software
  and DevOps: Building and Scaling High Performing Technology
  Organizations*, IT Revolution, 27 mars 2018, 288 p. — ISBN-13
  9781942788331 (eBook 9781942788355, Kindle 9781942788362).**
  Fiche : `itrevolution.com/product/accelerate/`. Titre complet à deux
  segments, constaté sur fiche (l'usage courant n'en cite qu'un).
  Tentatives : fiche éditeur (extrait seulement) ; TOC ETH Zurich
  (partiel). **Usage : ADR-0013** — base empirique DORA.
- [ ] **Cockburn, *Crystal Clear: A Human-Powered Methodology for Small
  Teams*, Agile Software Development Series, Addison-Wesley Professional,
  19 oct. 2004 (©2005), 336 p. — ISBN-13 978-0-201-69947-0 (ISBN-10
  0-201-69947-8).**
  Fiche : `informit.com/store/crystal-clear-a-human-powered-methodology-for-small-teams-9780201699470`.
  **Papier épuisé (constaté fiche) — préférer l'eBook InformIT (~30 $).**
  Tentatives : fiche éditeur (chapitre d'échantillon seul) ;
  alistair.cockburn.us/crystal-clear en 404. **Usage : 12 §5** —
  définition du walking skeleton (la page web de l'auteur est détenue en
  copie datée ; le chapitre du livre reste la source de rang livre).
- [ ] **Freeman & Pryce, *Growing Object-Oriented Software, Guided by
  Tests*, Addison-Wesley Signature Series (Beck), 12 oct. 2009 (©2010),
  384 p. — ISBN-13 978-0-321-50362-6 (ISBN-10 0-321-50362-7 ; eBook
  0321770358 ; ne pas confondre avec l'ISBN O'Reilly en ligne
  9780321574442).**
  Fiche : `informit.com/store/growing-object-oriented-software-guided-by-tests-9780321503626`.
  Tentatives : fiche éditeur ; growing-object-oriented-software.com
  (matériel d'accompagnement seulement). **Usage : 12 §5** — walking
  skeleton opérationnalisé.

### Réglé sans procurement (2026-08-12)

- **Meyer, *Object-Oriented Software Construction*, 2e éd., Prentice Hall
  PTR, 1997, 1254 p. — ISBN-13 9780136291558** (fiche Open Library
  OL657292M, corroborée ACM DL 10.5555/261119) : texte intégral
  **légalement accessible sur le site de l'auteur, avec la permission de
  Pearson** (« With Pearson's kind permission, this online version has
  been made available… ») — https://bertrandmeyer.com/OOSC2 .
  **Restriction constatée sur la page : « You are not permitted to copy it
  or redistribute it »** → lecture et citation par chapitre/page : oui ;
  copie dans `biblio/` ou le dépôt : non. ADR-0010 cite depuis cette URL,
  accès re-vérifié à chaque citation.

## Priorité 3 bis — S3 transport (manques nommés par ADR-0015, 2026-08-13)

Chacun avec son usage prévu ; aucun n'est bloquant pour la phase C (le
chemin de bout en bout se conduit sans eux), tous le sont pour un claim
public sur `tlsn-mpc/1`.

1. **QuickSilver (système de preuve VOLE-IZK employé par l'amont)** —
   demande à former sur identité confirmée : la FAQ amont détenue nomme le
   système ; identité bibliographique **probable, non vérifiée sur pièce** :
   Yang, Sarkar, Weng, Wang, *QuickSilver: Efficient and Affordable
   Zero-Knowledge Proofs for Circuits and Polynomials over Any Field*,
   ACM CCS 2021 — DOI à confirmer AVANT toute citation. Usage prévu : toute
   phrase qui qualifierait la solidité de la preuve ZK ; sans lui, rien ne
   se dit au-delà de la citation de la FAQ. Tentatives : aucune encore
   (nommé par le draft ADR-0015, 2026-08-13).
2. **Analyse de sécurité arbitrée du protocole TLSNotary courant**
   (lignée MPC-TLS 2022+, alpha.13–alpha.16) — DECO (détenu) est un
   protocole voisin, pas celui-ci : l'employer comme caution serait une
   substitution de source. Usage : argumenter le résidu du transport
   au-delà de la parole de l'éditeur. État : existence même d'une telle
   analyse non établie — recherche à conduire avant demande formée.
3. **Pages `/docs/mpc/*` de la doc amont** (6 pages au sitemap :
   key_exchange, commitments, deap, encryption, mac, ff-arithmetic) —
   fetch simple, non fait en phase A (réserve de worker consignée à
   l'INDEX). Usage : le protocole bas niveau.
4. **README des exemples amont `basic` et `proxy`** (seul `attestation`
   est détenu, épinglé 0fe3c32d) — fetch simple. Usage : conduire la
   session réelle en phase C sans deviner l'API.
5. **Source du test amont `no_syscall_verify`**
   (`crates/attestation/tests/no_syscall_verify.rs`) — fetch simple,
   épinglage même commit. Usage : la pièce qui établit ce qu'un chemin de
   vérification « sans syscall » recouvre — condition (iii) de réouverture
   de la forme α (ADR-0015 pt 11).

6. **RFC 5890/5891 (IDNA2008) + UTS #46** (ADR-0016 C3) — requis
   seulement si une classe de faits admet une source à domaine
   internationalisé. Localisation : rfc-editor.org ;
   unicode.org/reports/tr46/ (la copie WHATWG détenue référence tr46-35,
   4 septembre 2025).
7. **RFC 5952 (représentation textuelle IPv6)** (ADR-0016 C3) — requise
   seulement si un littéral d'adresse est un jour admis.
8. **Mesure de la sensibilité des origines à l'ordre des paramètres de
   requête** (ADR-0016 C8) — aucune pièce détenue, aucune candidate
   identifiée ; ne changerait pas la décision (normative) mais
   chiffrerait le risque évité.

*(La taille d'un artefact `Presentation` n'est PAS ici : elle se résout
par mesure en phase C — ADR-0015, manque 6.)*

## Priorité 4 — GTM / marché (dossier Shōgen-GTP, ADR-0019, 2026-08-20)

Procurements ouverts du dossier de stratégie (`F:\Shogen-GTP\docs\07` §3-4),
versés ici à la consignation. Aucun n'est bloquant pour le code S2 ; les deux
**décisionnels** (⚑) le sont pour un claim ou un séquencement de canal. Le budget
WebSearch de la mission était épuisé (200/200) ; une relance à budget restauré
clôt PS-03/06/07 (note d'outillage 07 §3, pas une dette).

### Marché (série PS)

- [ ] **PS-01 ⚑** — `docs.api3.org/oev-searchers/` (cessation de l'OEV Network
  public ~nov. 2025). Bloqué : 404 curl (2 variantes). **Usage : confirmer sur
  primaire le renversement de l'ancrage du canal 3 (API3 → Chainlink SVR)** —
  impact décisionnel (D3).
- [ ] **PS-02** — figure Venus « primes de liquidation année pleine 2024 »
  auditée (candidat : rapport Messari). Bloqué : WebSearch épuisé. Usage :
  trancher la contradiction 5,8 M$ vs 6,2 M$.
- [ ] **PS-03** — état des opérateurs de nœuds RedStone en août 2026 (Guard
  Program II ? AVS ?). Bloqué : WebSearch épuisé. Usage : borner l'actualité de
  « 5 nœuds internes » (datée 2023/24).
- [ ] **PS-04** — drill-down par validateur du dashboard Chronicle (exchanges
  interrogés). Bloqué : 429 rate-limit. Usage : trancher la cellule S2 de
  Chronicle.
- [ ] **PS-05** — article WSJ sur le prix de rachat Messari (« >10 M$ »).
  Bloqué : paywall. Usage : passer le montant de [2nd] à [lu] (PS-05 = source du
  chiffre repris [2nd] en ADR-0019).
- [ ] **PS-06 ⚑** — fiche + score S1–S5 de **Primus Labs** (omission de T1 ;
  TEE Phala vérifié, AlphaNet en [2nd]). Bloqué : WebSearch épuisé. Usage :
  compléter l'ensemble zkTLS avant publication (« unanime » actuellement
  surétendu).
- [ ] **PS-07** — leads d'institutions non bouclés : growthepie, Bluechip, DeFi
  Safety ; frontière Chainlink DECO ; Pluto, Clique. Bloqué : WebSearch épuisé.
  Usage : compléter la carte des institutions et des zkTLS.
- [ ] **PS-08** — omissions CV1 §9 : cabinets adjacents (Re7, MEV Capital,
  Apostro, Anthias) ; douleur OEV/liquidation côté Morpho/Euler/Spark ; identité
  de l'oracle du glitch du 10/03/2026 (27 M$ liquidés). Bloqué : WebSearch
  épuisé. Usage : compléter le périmètre demande + identifier une défaillance
  d'oracle nommée (cœur de thèse).
- [ ] **PS-09** — trajectoire de TVS RedStone (« ×46 depuis début 2023 ») sur
  primaire daté. Bloqué : non re-tracée. Usage : adjuger la figure de croissance
  de `07-gtm.md` (actuellement NON_VÉRIFIABLE).
- [ ] **PS-10** — antériorité de marque **avant** branding public (registres
  US/UE/FR/JP ; « 証言 » ; homonymes SaaS ; domaines). Non bloquante. Usage :
  dégager la marque Shōgen avant exposition (D1/D10, leçon Vernier/Seilkal).

### Académique (série PA-SH2 — chiffres portés en [2nd], sources primaires à acquérir)

- [ ] **PA-SH2-01** — Gangwal, Valluri & Conti 2022 (« 31 nœuds / 7 sources »,
  primaire). Usage : passer le chiffre porteur de [2nd] à [lu].
- [ ] **PA-SH2-03** — **Messias et al., FC 2023** (« 98,68 % des liquidations
  dépendent d'une MAJ Chainlink dans le même bloc »). Actuellement **[2nd] via
  Gansäuer et al. 2025** (lu au PDF) ; à passer en [lu] direct. Usage : le
  chiffre porteur du résultat central, repris [2nd] en ADR-0019 (annexe A).
- [ ] **PA-SH2-06** — Slager, Gond & Moon 2012 (FTSE4Good). **Possiblement déjà
  satisfait** via l'accès ouvert cité au doc 03 §3 — à adjuger sur pièce.
- [ ] **PA-SH2-02 / 04 / 05 / 07** — paternité du terme « OEV » ; contrefactuel
  d'échec de dashboard crypto ; textes intégraux restés [abs]. Usage : sourcer
  les figures et affirmations correspondantes avant tout claim public.

### Hors périmètre de ce versement (nommés pour zéro dette)

- **Extrait KRS officiel de L2BEAT Sp. z o.o.** (`ekrs.ms.gov.pl`) — agrégateurs
  KRS [2nd] concordants ; registre d'État direct non consulté (07 §4, CV2
  Aff. 6). Confort : l'entité est établie.
- **PA-01..PA-04** (07 §4) — corrections d'archive et confort **côté dossier GTP**
  (venue Pontikes 2012 ; pairage titre/DOI « DORA » 2023 ; contre-littérature
  open-core ; textes [abs]) : hors dépôt, laissés à la maintenance du dossier
  source, pas des procurements du dépôt.

## Priorité 5 — campagne S2 (ADR-0020, ratifiée 2026-08-20)

Deux procurements formés pour caler les paramètres ex ante de la campagne (ADR-0020) ;
deadline = clôture de la calibration 48 h.

- [ ] **PS-S2-01 ⚑ — heartbeat + seuil de déviation du feed Chainlink BTC/USD**
  (Ethereum mainnet, `data.chain.link/feeds/ethereum/mainnet/btc-usd`). Bloqué :
  **403** aux fetchs programmatiques (2 canaux + passe worker 2026-08-05 ; dette
  10 §10.6). **Usage** : `run_params.sigma[chainlink] = 1,5 × heartbeat` (branche (i)
  d'ADR-0020) et ancre de cohérence de τ ; sans lui, repli fail-closed (axe staleness
  Chainlink « non évaluable »). Voie : **visite navigateur** (une vraie session peut
  passer là où le fetch échoue), champs « deviation threshold » + « heartbeat » datés.
- [ ] **PS-S2-02 — rapport Kaiko primaire** sur le volume/liquidité BTC du week-end
  post-ETF (piste : `research.kaiko.com/reports` ; actuellement [2nd] via The Block).
  **Usage** : fonder l'ADR de strate (week-end=stress) sur pièce primaire plutôt que
  presse — les chiffres ~28 %→16-17 % à passer [lu].

## Déjà réglé (pour mémoire)

- ~~Knight & Leveson 1986, article complet~~ — apporté par le mainteneur.
- ~~Eckhardt & Lee 1985~~ — version TM-86369 fetchée sur NTRS.
- ~~Reply to the Criticisms~~ — détenu (sunnyday.mit.edu) ; venue
  confirmée par fiches web (SEN 15(1), 1990).
