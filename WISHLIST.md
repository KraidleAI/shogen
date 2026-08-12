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

*(La taille d'un artefact `Presentation` n'est PAS ici : elle se résout
par mesure en phase C — ADR-0015, manque 6.)*

## Déjà réglé (pour mémoire)

- ~~Knight & Leveson 1986, article complet~~ — apporté par le mainteneur.
- ~~Eckhardt & Lee 1985~~ — version TM-86369 fetchée sur NTRS.
- ~~Reply to the Criticisms~~ — détenu (sunnyday.mit.edu) ; venue
  confirmée par fiches web (SEN 15(1), 1990).
