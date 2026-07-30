# Shōgen — registre bibliographique

**6 artefacts détenus** au 2026-07-30. Chaque entrée porte : ce que la page
de titre dit, ce qui a été lu, et le statut de vérification des citations
qui s'appuient dessus. Pas de sidecars encore (outillage à monter — les
greps ci-dessous ont été faits sur les fichiers bruts).

| fichier | ce que c'est (page de titre / en-tête) | lu | citations vérifiées |
|---|---|---|---|
| `deco-2019.pdf` | Zhang, Maram, Malvai, Goldfeder, Juels, *DECO: Liberating Web Data Using Decentralized Oracles for TLS*, arXiv:1909.00938 (version étendue de CCS '20) | abstract (via fetch du 2026-07-30) | « prove that a piece of data accessed via TLS came from a particular website » — provenance, pas vérité ; « without trusted hardware or server-side modifications ». **À relire au texte : §modèle de menace.** |
| `knight-leveson-1986-full.pdf` | Knight & Leveson, *An Experimental Evaluation of the Assumption of Independence in Multi-Version Programming*, article complet (manuscrit, copie MIT OCW 16.358J, 46 p. ; version journal : IEEE TSE 12(1):96-109, 1986). Page de titre lue le 2026-07-30 — apporté par le mainteneur, remplace le résumé de séminaire KTH (supprimé). | pp. 1-3, 10-16 (abstract, intro, §4 résultats, §5 modèle et test, début §6) | Vérifiées au texte : abstract « the number of tests in which more than one program failed was substantially more than expected » ; §5 : N=27, n=1 000 000, K=1255, z=100,51 > 2,33 (point 99 %), « we reject the null hypothesis with a confidence level of 99% … Thus, we reject this assumption » ; §4 : « In the preliminary analysis of common faults, *all* were found to involve versions from both schools » — l'axe deux-universités n'a pas produit l'indépendance. |
| `knight-leveson-1986-uva-report.pdf` | Page de titre lue le 2026-07-30 : *Detection of Faults and Software Reliability Analysis*, Annual Progress Report NASA NAG-1-605, juil. 1985–juin 1987, J.C. Knight, UVA Report UVA/528243/CS88/103, août 1987, 14 p. (NASA-CR-180347). Rapport d'avancement compagnon — intérêt marginal. | page 1 | aucune citation ne s'appuie dessus |
| `knight-leveson-reply.pdf` | Page de titre lue le 2026-07-30 : Knight & Knight/Leveson, *A Reply to the Criticisms of the Knight & Leveson Experiment* (~1990, forum SIGSOFT SEN d'après le contexte — venue exacte à confirmer avant citation). Documente la controverse avec Avizienis et al. ; p. 1 porte la citation d'Avizienis nommant l'indépendance « the fundamental conjecture of the NVP approach ». | page 1 | la citation Avizienis ci-contre est utilisable (lue p. 1) ; le reste non lu |
| `tlsnotary-faq.html` | FAQ officielle tlsnotary.org (page mutable — copie du 2026-07-30) | oui (fetch + grep sur la copie) | vérifiées par grep dans le fichier détenu : « does not solve the … Oracle Problem » (1 occurrence), « trust in the notary » (1 occurrence). Également relevé au fetch : le notaire ne voit que métadonnées de session (durée, longueurs, cipher suite) ; la preuve vaut envers un vérificateur désigné ; TLS 1.2 seulement. |
| `c2pa-spec-2.4.html` | C2PA Technical Specification v2.4 (spec.c2pa.org — copie du 2026-07-30) | sections modèle de données + trust model (via fetch) | vérifiée par grep dans le fichier détenu (1 occurrence) : « SHOULD NOT provide value judgments » — la spec s'interdit de juger si la provenance est « bonne », elle valide seulement intégrité, association et non-altération. Modèle : assertions → claim signé → claim signature ; chaîne par ingredients. |

| `reclaim-security-faq.html` | *Is Reclaim Secure?* — FAQ sécurité officielle, blog.reclaimprotocol.org (page mutable — copie du 2026-07-30) | oui (fetch du 2026-07-30) | relevé au fetch (grep sur copie à refaire si citée dans une publication) : un attestor compromis ne peut pas lire les données (TLS de bout en bout) mais **peut forger des preuves** — « The only protection against fake proofs here is decentralisation or self-hosting of the attestor » ; BGP surveillé via RIPE RIS, connexion coupée si reroutage suspect ; modèle à attestor unique (la décentralisation est une mitigation évoquée, pas l'architecture). |
| `reclaim-attestor-core-readme.html` | README du dépôt reclaimprotocol/attestor-core (« witness server ») — copie du 2026-07-30 | non lu au-delà du fetch de recherche | aucune citation ne s'appuie dessus |

## Dettes de registre (à fermer prochaine passe)

1. ~~L'article original de Knight & Leveson~~ — **fermée le 2026-07-30** :
   article complet apporté par le mainteneur, lu aux sections citées
   (voir l'entrée). Reste ouverte la variante mineure : la copie est le
   manuscrit MIT OCW, pas le tiré IEEE — la pagination journal (96-109)
   ne doit pas être citée par numéro de page depuis cette copie.
2. ~~Pages de titre des deux PDFs~~ — **fermée le 2026-07-30** (entrées
   mises à jour). Reste : venue exacte du « Reply » à confirmer avant
   citation formelle.
2bis. ~~Artefact primaire Reclaim~~ — **fermée le 2026-07-30** (FAQ
   sécurité + README attestor-core détenus). Reste : lecture au texte du
   README si le modèle proxy est cité en détail.
3. Outillage sidecar (extraction texte des PDFs) — les greps ci-dessus
   portent sur les HTML bruts et sur des lectures visuelles ; les PDFs ne
   sont pas encore greppables.
4. Reclaim Protocol : aucun artefact primaire détenu (le « zkTLS Canon »
   est un index, pas une source) — fetcher le whitepaper ou l'article
   technique du modèle proxy avant toute affirmation sur son modèle de
   menace.
5. Le lemme 8 de Chainlink OCR est détenu **dans la biblio Kraidle**
   (`F:\Kraidle\biblio\08-distributed\chainlink-ocr.pdf.sidecar`, grep
   vérifié le 2026-07-30 : « v is either the observation of a correct
   oracle or lies between the observations of two correct oracles »).
   Décision à prendre : copie locale ou référence croisée inter-projets.
