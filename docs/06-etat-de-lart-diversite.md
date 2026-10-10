# État de l'art — diversité mesurée et indépendance des sources (verdict R-1)

> **Statut.** Verdict de la passe R-1, 2026-07-30. Méthode : balayage
> multi-agents à 5 angles (lignée K&L, métriques de diversité, oracles
> blockchain, quorums distribués à fautes corrélées, littérature agents
> 2024-2026) — 50 candidats bruts, 45 classés après dédup, ~36 recherches
> vides documentées avec leurs requêtes. Les 6 artefacts critiques ont été
> **fetchés et vérifiés en page de titre** (INDEX) ; le reste des candidats
> est au rang **lead** (rapport de balayage, artefact non détenu) et chaque
> item ci-dessous porte son statut. Avant toute citation d'un lead dans une
> publication : fetch + lecture au texte, sans exception.

## 1. Le verdict en trois phrases

**Le geste générique — remplacer une indépendance postulée par une
dépendance mesurée — n'est pas nouveau : c'est une pratique réglementaire
nucléaire depuis ~1998 (NUREG/CR-5485, facteurs alpha — lead), un service
d'audit cloud depuis 2014 (INDaaS — détenu), et un compte effectif publié
pour des panels de juges LLM en mai 2026 (Kish n_eff — détenu).**

**Ce qui est inoccupé, sur dix angles de recherche vides vérifiés : le test
de co-défaillances style K&L transposé aux *sources de données* ; le chemin
observables-d'infrastructure → quorum effectif pour des sources ; le
certificat comme artefact vérifiable par décision de quorum ; et le terme
même de « certificat de diversité ».**

**Le claim de nouveauté de Shōgen doit donc être rescopé — non pas
« personne ne mesure l'indépendance » (faux depuis 1985, et la communauté
fiabilité tient l'indépendance pour fausse depuis Eckhardt-Lee/K&L/L&M),
mais : « l'indépendance d'un quorum de sources de données est *certifiée* —
depuis un historique de co-défaillances testé ET des observables
d'infrastructure, en un artefact par décision, vérifiable offline — au lieu
d'être postulée, déclarée, ou auditée hors ligne ».**

## 2. Ce qui est occupé — à citer, jamais à revendiquer

| travail | statut | ce qu'il occupe | ce qu'il laisse libre |
|---|---|---|---|
| Eckhardt & Lee 1985 (TM-86369) | **détenu**, summary lu | le modèle nul : l'intensité de co-erreurs, variation de difficulté | modèle, ne mesure pas ; versions, pas sources |
| Knight & Leveson 1986 | **détenu**, lu §1-8 | le test statistique de co-défaillances contre l'indépendance | jamais transposé aux sources de données (angle vide vérifié) |
| Littlewood & Miller 1989 | **détenu**, lu pp. 1596-1604 | Var(Θ), Corr·CV·CV comme mesure de dépendance ; diversité forcée ; Cov<0 | modèle de versions ; pas d'historique mesuré, pas de certificat |
| Littlewood, Popov & Strigini, ACM CS 2001 | lead | le survey de référence — l'homme de paille à éviter : la communauté *sait* l'indépendance fausse | évaluer une configuration diverse *donnée* reste ouvert — notre case |
| NUREG/CR-5485 (1998) + alpha factors | lead | le précédent réglementaire : dépendance estimée d'événements réels, re-prix du k-parmi-n | périmètre d'un exploitant ; composants physiques ; paramètre de PRA, pas certificat par décision |
| INDaaS, OSDI 2014 + RepAudit, OOPSLA 2017 | **détenu** (INDaaS, p.1 lue) / lead | « seemingly independent systems may share deep, hidden dependencies » — audit d'indépendance par observables structurels ; « close to 37% of failures are truly correlated » (Google, cité p.1) | graphes *déclarés/collectés*, pas d'historique de co-défaillances **testé** ; rapport d'audit, pas de certificat lié à une décision ; répliques cloud, pas sources |
| Kohli 2026, « Nine Judges, Two Effective Votes » | **détenu**, p.1 lue | **la menace la plus directe** : n_eff (Kish) + modèle nul de Condorcet — un compte effectif depuis corrélation mesurée, publié | juges LLM, pas sources ; pas d'observables d'infrastructure ; pas de partition ; pas d'artefact de certificat |
| He & Yu 2026, « Semantic Quorum Assurance » | **détenu**, p.1 lue | quorum + certification + modèle de défaillance cognitive corrélée + diversité dans le prédicat | diversité **imposée par étiquettes**, corrélation estimée en calibration — jamais **mesurée sur un historique de production** ; validateurs LLM, pas sources |
| Zhang et al., TIFS 2016 (network diversity) + Vendi Score (TMLR 2023) | **détenu** (TIFS, p.1 lue) / lead | les formes mathématiques du « nombre effectif » (biodiversité, entropie de similarité) | entrées déclarées (étiquettes, topologie) — pas de co-défaillances mesurées ; pas de quorum |
| Malkhi & Reiter 1998 (fail-prone systems) ; Junqueira & Marzullo 2003 (cores/survivor sets) | leads | les quorums **sous** dépendance : la sémantique côté consommation | la structure de dépendance y est *supposée* en entrée — **Shōgen produit l'objet que ce cadre consomme** |
| Lignée Gashi/Popov/Strigini (SQL 2007, AV 2011, OS/DSN 2011) ; van der Meulen 2008 ; Ron et al. 2026 (N-version par agents LLM) ; Nogueira et al. 2026 | leads | co-défaillances mesurées sur produits réels et versions LLM ; la méthode K&L rejouée en 2026 sur du code généré (429 co-déf. vs 115 prédites) | tous sur des versions/produits logiciels ; aucun sur des quorums de sources de données en production |
| Bakkaloglu et al. 2002 ; Nath et al., NSDI 2006 ; Ford et al., OSDI 2010 ; Weatherspoon 2002 | leads | la preuve en production que l'indépendance postulée fausse les calculs (stockage, datacenters) ; la boucle « corrélation observée → placement » | paramètres globaux ou principes de conception — pas de certificat par ensemble, pas de sources externes |

## 3. Ce qui est inoccupé — les angles vides vérifiés

Dix requêtes ciblées, verdict vide, requêtes archivées dans le rapport de
balayage (chemin en §6). Les quatre structurants :

1. **« Test K&L transposé aux sources de données »** — vide. La lignée
   versions-logicielles remonte, plus SQA (diversité imposée, non mesurée).
2. **« ASN / amont commun → k_eff pour un ensemble de sources »** — vide.
   Pages vendeurs, brevets hors-sujet. Les mesures ASN existent pour les
   *validateurs* PoS (concentration d'hébergement), jamais pour les
   sources d'un feed.
3. **« Nombre effectif de composants indépendants depuis co-défaillances
   mesurées »** — vide côté fiabilité/sûreté. Le n_eff n'existe que via
   l'écologie (TIFS 2016, Vendi) et les juges LLM (Kohli).
4. **« Certificat/attestation de diversité mesurée »** — vide. Le terme
   est libre au sens technique.

Plus deux résultats de bordure à conserver : **la piste VLDB à chasser** —
Dong et al., *Global Detection of Complex Copying Relationships Between
Sources* (VLDB 2010, lead) : la détection de copie entre sources par
**fautes partagées** est exactement le signal de l'axe amont-commun de
Shōgen, jamais convertie en métrique de diversité ni en quorum ; et **un
faux positif documenté** — un snippet attribuait à arXiv:2605.06738 une
indépendance-par-structure qui n'est pas dans son abstract (négatif
vérifié par le balayage ; quiconque relance la recherche retombera dessus).

## 4. Les renforts — le problème est reconnu, l'instrument absent

- **Chainlink whitepaper v1 (2017, détenu, §4.1 p. 11 et §5.3 p. 19 lues
  au texte)** : nomme l'attaque par *mirroring* (§5.3), donne l'amont
  commun en exemple et annonce en travaux futurs « mapping and reporting
  the independence of data sources » (§4.1) — **jamais réalisée en neuf
  ans** (angle vide : le recouvrement des agrégateurs par feed n'est
  mesuré nulle part ; Chaos Labs Pt.4 (lead) constate que l'ensemble
  n'est même pas publié).
- **Sevim & Torres 2026 (détenu, p.1 lue)** : la mesure du phénomène
  exact — des DONs « indépendants » consomment « largely identical
  off-chain price data nearly simultaneously », fenêtres d'exploitation
  statistiquement prédictibles, 12 009 mises à jour de prix, 2 986
  liquidations Aave. Le phénomène est réel, mesurable, exploité comme
  MEV — et personne n'a construit l'instrument de défense.
- **DECO §3.1 (détenu, lu)** : la racine académique du champ délègue
  l'intégrité à « querying multiple oracles … majority agreement ».
- **Junqueira & Marzullo, Malkhi & Reiter** (leads) : la théorie des
  quorums sous dépendance attend en entrée exactement l'objet que le
  certificat produit.

## 5. Conséquences immédiates

1. **Le claim du papier S5 est rescopé** (§1, troisième phrase) — et le
   papier cite obligatoirement : E&L/K&L/L&M (le modèle nul et le test),
   LPS 2001 (anti-strawman), NUREG (le précédent réglementaire), INDaaS
   (observables structurels), Kohli (n_eff), SQA (certification de
   quorum), TIFS/Vendi (formes du compte effectif), Malkhi-Reiter
   (consommation), Sevim-Torres + Chainlink v1 (le gap sur l'objet).
2. **k_eff doit être nommé et défini explicitement** dans 04 — l'angle
   vide n°3 est un argument *pour* le nom, et TIFS/Vendi/Kohli sont les
   formes à citer-et-distinguer (notre entrée : co-défaillances mesurées +
   partition par observables, pas étiquettes ni similarité déclarée).
3. **L'axe amont-commun gagne un précédent méthodologique** : la détection
   de copie par fautes partagées (Dong et al., à fetcher) — R2 peut citer
   une lignée au lieu d'inventer.
4. **04 §1/§2 restent valides tels quels** — rien dans le balayage ne
   contredit les rangs ni la machinerie K&L/L&M ; SQA renforce même la
   distinction imposé/mesuré qui fonde R3 vs R1.
5. **Dettes de fetch ouvertes** (avant publication seulement) : LPS 2001,
   NUREG/CR-5485, RepAudit, Malkhi-Reiter, Junqueira-Marzullo, Dong 2010,
   Vendi, la lignée Gashi, Ron 2026, Nogueira 2026, Sevim-Torres au texte
   complet, SQA au texte complet, Kohli au texte complet, les deux SoK
   oracles (Eskandari 2021, Finkbeiner 2025 — vérifier si le gap y est
   listé comme problème ouvert).

## 6. Traçabilité

Rapport de balayage complet (45 candidats, 36 requêtes vides avec
verdicts) : sortie du workflow `shogen-r1-sweep` du 2026-07-30, archivée
dans le répertoire de session (`tasks/wm1ju9h7w.output`) — à copier dans le
dépôt si ce document est cité au-delà du dépôt. Artefacts détenus : voir
`biblio/INDEX.md` (les 6 fetchés de cette passe y portent leurs pages de
titre vérifiées).

## Ajouts datés en fin de document

*Ajout daté du 2026-10-10 04:55:38 UTC (`date -u`) ; lot DETTES-T14* : les
ajouts datés du lot DETTES-T14 sont placés ici, en fin de document, pour n'en
décaler aucune ligne, ce document étant cité ailleurs par numéro de ligne ;
chacun nomme la section qu'il vise, dont le texte est inchangé.

**Vise §5, point 5.** *Ajout daté du 2026-10-10 04:55:38 UTC (`date -u`) ;
lot DETTES-T14 ; SHOGEN-FETCH-AVANT-PUB-1 et décision Q-D de l'adjudication
du procurement du 2026-10-09 ; le point 5 de §5 est inchangé* : les onze
dettes de fetch du point 5 (ses quinze noms, moins Dong 2010, détenu, et
Sevim-Torres, SQA et Kohli, détenus, dont reste la lecture du texte complet)
sont formées et traitées le 2026-10-09 : identité, DOI, pages et tentatives
datées sont à `biblio/INDEX.md` (section du lot DETTES-T14). Détenues
(huit) : LPS 2001 (version de City Research Online) ; RepAudit (Zhai et al.,
PACMPL 1(OOPSLA), art. 97, 2017) ; Junqueira et Marzullo (ICDCS 2003) ; Vendi
(arXiv 2210.02410v2, publié à TMLR en 07/2023) ; la lignée Gashi (SQL 2007,
AV 2011, OS/DSN 2011 ; l'identité d'« AV 2011 » reste proposée, City Research
Online listant d'autres papiers antivirus de Gashi) ; Ron et al. 2026 (arXiv
2606.20158v1) ; Nogueira et al. 2026 (arXiv 2607.02808v1, quatre auteurs) ;
Eskandari et al. 2021 (arXiv 2106.00667v2). À l'achat (une) : Malkhi et
Reiter 1998 (DOI 10.1007/s004460050050 ; prix non lu, page de l'éditeur
derrière un contrôle anti-robot). Introuvables (deux) : NUREG/CR-5485 et
« Finkbeiner 2025 ». NUREG/CR-5485 est gardé là où il est cité (§1, §2, §5),
avec ce statut : copie non détenue ; page NRC (404) et document ADAMS (403)
inaccessibles au 2026-10-09 ; toute affirmation sur son contenu reste [2nd].
« Finkbeiner 2025 » : attribution non établie au 2026-10-09 (le seul SoK de
Finkbeiner relevé, ICBC 2025, traite du *selfish mining*, non des oracles) :
la référence est retirée. Eskandari 2021 répond à la question du point 5 :
aucun passage n'y pose la dépendance d'amont commun comme problème ouvert
[abs : recherche par mots-clés sur les quinze pages] ; un texte qui l'affirme
le fait en propre, et le dit. Au §2, le « 429 co-déf. vs 115 prédites » est
de Ron et al. (p. 1) ; le texte de Nogueira et al. ne porte ni 429 ni 115.
