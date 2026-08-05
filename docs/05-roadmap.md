# Shōgen — feuille de route (v0, 2026-07-30)

> Format hérité de Kraidle : chaque jalon a un **critère de sortie
> binaire** — on peut répondre oui ou non sans discussion. Un jalon sans
> critère binaire n'est pas un jalon. Les jalons sont séquentiels sauf
> mention ; les recherches (R-x) peuvent courir en parallèle des jalons.

## S0 — Fondations épistémiques *(en cours, presque clos)*

Fait : vision (02), ADR-0001, forme canonique de témoignage (03),
certificat de diversité (04), biblio 8 artefacts + INDEX avec dettes
tracées, mémoire projet (memstack, groupe Shogen).

**Critère de sortie** : les trois dettes de lecture sont fermées —
(a) ~~K&L §6-8 lu~~ — fait le 2026-07-30 (INDEX ; récolte dans 04 §6.4) ;
(b) ~~DECO lu au modèle de menace~~ — fait le 2026-07-30 (INDEX : §3 lu,
    adversaire statique malveillant, propriétés, et le renvoi « multiple
    oracles … majority agreement » qui nomme le gap de Shōgen dans le
    papier fondateur du champ) ;
(c) ~~venue du « Reply »~~ — fait le 2026-07-30 (deux fiches concordantes,
    DOI 10.1145/382294.382710 ; résidu minime tracé à l'INDEX).

**→ S0 CLOS le 2026-07-30.** Bonus de passe : Eckhardt & Lee détenu
(TM-86369, NTRS) avec le concept central pour R1 — l'« intensity of
coincident errors » comme fonction de l'environnement d'entrée ;
Littlewood & Miller 1989 introuvable en accès libre → `WISHLIST.md`.
→ *Oui/non : chaque entrée d'INDEX.md citée par une spec porte « lu » sur
la section citée.*

## R-1 — La passe académique formelle *(recherche, avant toute publication)*

La revendication de nouveauté du certificat tient sur deux périmètres web.
Insuffisant pour un papier. Passe dédiée arXiv + ACM DL + IEEE + USENIX :

- mots-clés : *common-mode failure*, *failure diversity metrics*,
  *N-version diversity measurement*, *oracle independence*, *data feed
  correlation*, *Sybil detection data sources* ;
- lignée K&L aval : Eckhardt & Lee (modèle de corrélation par variation de
  difficulté), Littlewood & Miller (diversité forcée) — les deux sont les
  suites théoriques attendues de K&L, à fetcher et lire ;
- verdict écrit : soit « le cadre existe, on cite et on se positionne »,
  soit « searched, nothing newer » avec le périmètre — les deux sont des
  résultats.

**Critère** : un document `06-etat-de-lart-diversite.md` existe, avec
verdict et artefacts fetchés dans `biblio/`.

**→ R-1 RENDUE le 2026-07-30** : balayage 5 angles (50 candidats bruts,
45 classés, ~36 recherches vides documentées), 6 artefacts critiques
fetchés et vérifiés en page de titre, verdict écrit dans `06` — le geste
générique est occupé (NUREG, INDaaS, n_eff), les quatre angles propres à
Shōgen sont vides vérifiés, le claim de nouveauté est rescopé. Restent
les dettes de fetch de `06 §5.5` — bloquantes pour S5 (publication),
pas pour S1-S4.

## S1 — Le vocabulaire fait spec *(documentation)*

1. Registre des assumptions au format A(...) : A(attestor-honesty),
   A(notary-neutrality), A(enclave-integrity), A(source-key), + celles que
   R-1 fera émerger. Niveau d'assurance et condition de décharge par
   entrée.
2. ADR-0002 : encodage de la forme canonique (candidat : CBOR déterministe
   / COSE — examiner le précédent C2PA détenu).
3. ADR-0003 : certificat émis vs recalculable offline (le [à décider]
   majeur de 04 — la cohérence avec « sans confiance dans Shōgen » penche
   pour recalculable ; l'ADR paie le coût en volume de lot).
4. Vocabulaire interdit v1 (déjà amorcé : « quorum de k sources diverses »
   sans rangs ; « donnée vérifiée » ; « prix garanti correct » ; « fait
   signé » — l'attestation couvre les octets, le typage est un adapter).
5. ADR-0004 : multi-attestor — un témoignage à k attestors est-il un objet
   (co-signatures) ou k témoignages agrégés plus haut (03 §5, item 3 ;
   pèse sur le certificat de diversité).
6. ADR-0005 : politique de rétention des octets bruts — utterance complète
   vs hash + extraction (03 §5, item 4).

**Critère** : les quatre documents existent et l'auditor (skill Kraidle,
mutatis mutandis) passe sur l'ensemble docs/ sans trouver de claim sans
support.

**État au 2026-07-30** : livré — registre `08-assumptions.md` (9 entrées,
transport + couche), ADR-0002/0003/0004/0005 acceptées (DECISIONS.md),
vocabulaire interdit `09-vocabulaire.md` (11 entrées propres + héritées),
amendements portés dans 03 §5 et 04 §1/§4.

**→ S1 CLOSE le 2026-08-05.** L'audit de sortie s'est déroulé en deux
temps. **Passe 1 (2026-07-30)** — coupée par une limite d'usage à 1
dimension sur 3 (cohérence des registres) : 6 trouvailles vérifiées à la
main et corrigées (fermeture non portée de 04 §5 + identifiant mort
A(shogen-mesure), trois « registres touchés » périmés, deux assumptions
non citées à leur site, localisations Chainlink v1, 03 §2 périmé, 4ᵉ
référence inter-projets). **Passe 2 (2026-08-05)** — les deux dimensions
manquantes ont tourné jusqu'au bout (18 agents, 0 mort) : fidélité des
citations des ADR et projet contrôlé contre son propre vocabulaire
interdit. **11 confirmées, 5 réfutées**, toutes re-vérifiées à la main
(frontière de passe) et corrigées : cible « tested » écrite dans une case
d'état (→ « aucune »), ADR-0003 pointant GTM §4 pour une citation en §6,
« intends »→« proposes » (Chainlink), « 40 occurrences » = 40 lignes/56
occurrences, deux gloses françaises entre guillemets d'une citation
anglaise, et **deux graves de vocabulaire** : « faits signés » en page de
garde (→ « à provenance attestée »), « la source a dit vrai » et « valide
le certificat » dans la voix du projet en ADR-0007 (→ reformulés).
Rapport de passe 2 archivé : `docs/rapports/s1-exit-audit-2026-08-05.json`.
Le critère de sortie de S1 (audit sans claim sans support) est satisfait.

## S2 — Le prototype qui tranche *(code, premier)*

Pas le produit — l'instrument de mesure. Un harnais R1/R2 sur données
réelles :

- brancher 6-10 sources de prix publiques (la classe de faits du premier
  produit) ;
- collecter l'historique par fenêtres, implémenter le test K&L §5
  (binomiale, z) sur les co-écarts ;
- implémenter 2 axes R2 : ASN/hébergeur + corrélation de contenu
  (détection d'amont commun) ;
- calculer k_eff sur le pool réel.

**Pourquoi d'abord** : si les axes R2 ne sont pas observables en pratique,
ou si R1 ne discrimine rien sur données réelles, le cœur différenciant est
une hypothèse morte et il faut le savoir avant d'écrire une ligne de
produit. C'est le « prototype qui tranche » — jetable, résultat écrit.

**Critère** : un rapport `11-mesures-pilotes.md` (07 est occupé par le
GTM ; réconcilié le 2026-08-05, 10 §7) avec les chiffres réels : n
fenêtres, K, z du pool, la partition R2 constatée, k_eff vs k nominal.
*Résultat négatif = résultat* : « les axes ne discriminent pas » s'écrit
avec les chiffres et déclenche la révision de 04.

**État au 2026-08-05** : la conception de l'instrument est écrite —
`docs/10-mesures-pilotes-design.md` (classe pilote, pool, graphe d'amonts,
trois observables R2, statistique R1 sourcée, table de sortie recalculable,
6 décisions remontées, 11 dettes nommées) — sur faits re-établis à
l'aveugle uniquement (3 workers + 5 vérificateurs, même jour). La
faisabilité du pool est établie par mesure : 11 des 12 endpoints candidats
répondent 200 sans clé (12 flux, prix mutuellement cohérents à ~0,16 %,
re-mesure du 2026-08-05 ~12:02–12:04 UTC), CryptoCompare exige une clé
(401) et est écartée ; et l'axe R2 ASN est observable en une mesure
rejouable — 4 des 5 hôtes sondés partagent AS13335 (Cloudflare), soit côté
livraison k_eff = 2 pour k nominal = 5. L'axe corrélation de contenu reste
une conception non exécutée, et l'instrument n'a pas tourné : aucun
n, K, z encore. Le critère de sortie binaire ci-dessus reste inchangé
(seul le nom de fichier du rapport a été réconcilié en
`11-mesures-pilotes.md`, 07 étant occupé par le GTM). Les 6 décisions
remontées (10 §9) sont **prises le 2026-08-05** : pool = 11 sources,
oracles inclus ; classe « BTC/USD-stable », devise marquée par flux ;
≈ 2 semaines, w = 60 s, 2 strates ; CoinGecko strictement sans clé ;
lecture on-chain admise sous ADR-0006 ; règle `basis:doc` → ADR-0008
(proposée). **S2 passe à l'implémentation du harnais.**

## S3 — Le témoignage de bout en bout *(code)*

Premier chemin complet sur UN transport (candidat : TLSNotary, open
source, résidu documenté) : source réelle → témoignage canonique →
vérification offline par un binaire séparé qui nomme le résidu.

**Critère** : une commande `shogen verify <lot>` retourne « valide sous
A(notary-neutrality) » sur un témoignage réel, et échoue (fail-closed,
raison structurée) sur les 3 mutants semés : preuve altérée, hash
d'utterance faux, résidu non résolu. *(La règle gatewright : un
vérificateur qui n'a jamais rejeté n'a rien montré.)*

## S4 — Le verdict de quorum *(code + spec)*

Estimateur de confinement (médiane, lignée Lemme 8 — prouver ou citer,
jamais affirmer), fenêtre de fraîcheur, certificat de diversité embarqué,
lot vérifiable complet. Interface de sortie : le vocabulaire de faits que
le `gather` de Kraidle consomme (premier point d'intégration réel entre
les deux projets).

**Critère** : un lot de quorum réel (les sources de S2) vérifié offline,
certificat inclus, consommé par un stub `gather` côté Kraidle.

## S5 — Publication *(après R-1 et S2 seulement)*

Le papier : *« Measured diversity for data-source quorums »* — la
transposition K&L, les axes, k_eff, les mesures pilotes de S2 comme
évaluation. arXiv d'abord (dater l'antériorité), venue ensuite.
**Aucun claim de nouveauté sans le verdict R-1 ; aucun chiffre sans S2.**

## Ce qui n'est pas sur la route (non-buts re-dits)

Pas de transport propriétaire (ADR-0001). Pas de choix de sources pour le
client. Pas de moteur d'autorisation. **Pas de token — jamais, sur ce
projet comme sur ses frères — et pas de calcul on-chain** (ADR-0006).
L'*ancrage* d'un engagement sur chaîne (hash des certificats émis) est en
revanche une **question ouverte**, recommandée à partir de S2 : elle ne
demande de croire personne et serait la seule voie connue de décharge
partielle d'A(history-integrity).

Pas de notation de la **qualité du marché sous-jacent** — profondeur,
liquidité, fourchette (ADR-0007). Le certificat nomme l'amont, il ne le
note pas ; la classe de défaillance SK Hynix (28 juillet 2026) n'est pas
couverte et le certificat le publie.

## Règles de conduite héritées

Deux échecs même approche = changement de piste écrit. Toute figure
mesurée dans la passe. Tout artefact cité détenu et lu à la section. Les
skills `kraidle-*` s'appliquent jusqu'aux skills propres.
