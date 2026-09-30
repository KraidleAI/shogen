# Audit d'entrée — Shogen — 2026-08-12

Objet : écart entre l'état courant et le référentiel (corpus « Compliance et ingénierie
logicielle et architecturale », doc 02 v1.4 — gates G0–G7, règles R-1..R-25), conformément
à R-24. Chaque écart est traité (procurement / recherche / ADR+travail) — jamais un « plus
tard » hors registre. Audit réalisé comme **pilote** du câblage complet, sur autorisation
mainteneur ; états ci-dessous **observés**, pas déclarés.

## 1. État par gate

| Gate | Exigence clé | État constaté (2026-08-12) | Écart | Traitement |
|---|---|---|---|---|
| G0 | Specs + ADRs + modèle de menace + exigences réglementaires | **Riche** : docs/00–12 (vision, témoignage, certificat-diversité, état de l'art, GTM, assumptions, vocabulaire, mesures pilotes), DECISIONS.md, roadmap. La distinction fondatrice (attestation ≠ vérité) est elle-même un cadrage de menace. | Modèle de menace non formalisé comme document unique ; passe « fondations d'ingénierie » en préparation (docs/12, autre session en cours). | À la passe fondations : formaliser le threat model (l'ossature existe dans 03/04) — élément de travail, véhicule déjà ouvert. |
| G1 | Provenance des artefacts générés | Aucun journal de provenance. | Écart réel. | Instaurer `docs/journal-provenance.md` (template corpus) au premier artefact généré post-audit ; ADR à la passe fondations. |
| G2 | Revue 100 % + checklist | Doctrine locale déjà conforme à l'esprit : orchestrateur garde d'écriture (.claude/agents/shogen-orchestrator). Checklist G2 du corpus non encore en usage. | Partiel. | Adopter la checklist du corpus (templates/checklist-revue-G2.md) dès la prochaine PR de code. |
| G3 | Tests, SAST, dépendances | **Pas de code produit** (gate d'entrée « aucun code avant fondations » — même doctrine que Vernier). s2-harness : tests présents mais instrument **jetable** (R-22, quarantaine déclarée dans son README : « il meurt après le rapport 11 ») — zéro dépendance hors stdlib, donc pas de surface slopsquatting. | Sans objet aujourd'hui ; s'applique au premier code produit. | Inscrit : à l'ouverture du code produit, instancier g3 (tests bloquants + couverture) AVANT le premier commit de code — condition posée dans la CI (commentaire d'en-tête). |
| G4 | Fitness functions + métriques + description d'architecture 42010 | Pas de code → métriques sans objet. Description d'architecture : docs 02/03/04 couvrent stakeholders/concerns/décisions au sens de la clause 6. | Baseline métrique à poser au premier code. | Point zéro des séries R-15 à relever au premier commit de code produit. |
| G5 | TODO nus ; registre de dette | **Scan effectué ce jour : 0 marqueur de dette nu** (motif « mot-clé suivi de deux-points », hors biblio/ et .claude/, exclusions motivées). DECISIONS.md tient lieu de registre de décisions ; dette : rien d'ouvert hors registre constaté. | Aucun aujourd'hui. | **CI g5 instanciée ce jour** (.github/workflows/gates.yml, bloquante) + hook pre-commit installé (2026-08-12) + hook Claude Code global : triple couche active. |
| G6 | SBOM, licences, réglementaire | Pas de code distribué → CRA/SBOM sans objet à ce stade. biblio/ contient des papiers de recherche : **usage privé de recherche — ne jamais rendre ce dépôt public sans purge de biblio/** (copyright). | Garde-fou à écrire. | Consigné ici comme contrainte de publication ; à transformer en ADR si une publication du dépôt est un jour envisagée. |
| G7 | Seul l'orchestrateur committe ; verdict | Doctrine locale déjà en place (agents) + **signatures de commit requises sur main** (mécanisme GitHub actif — vérifié). | Aucun. | Conforme — et mécanisé. |

## 2. Stock de code généré non revu

s2-harness (Python stdlib, ~6 modules + tests) : **quarantaine R-22 assumée et documentée
à la source** — jetable, mort programmée après le rapport 11-mesures-pilotes. Pas de
résorption à planifier ; l'interdiction de promotion (R-22 : un prototype ne se promeut
pas sans repasser G0–G7) s'applique et est la seule obligation.

## 3. Baseline métrique initiale (point zéro R-15)

| Métrique | Valeur au 2026-08-12 |
|---|---|
| Duplication | s.o. — pas de code produit |
| Churn < 2 sem. | s.o. |
| Ratio refactoring/ajout | s.o. |

À relever au premier commit de code produit (condition G3/G4 ci-dessus).

## 4. Verdict d'entrée

Shogen entre dans le référentiel **sans dette nue** : trois écarts réels (threat model
formalisé, journal de provenance, checklist G2) ont chacun un véhicule daté — la passe
« fondations d'ingénierie » déjà en préparation (docs/12) ; G5 est mécanisé dès ce jour
(CI bloquante + deux hooks) ; G3/G4/G6 sont conditionnés au premier code produit avec
leur déclencheur écrit. Le harnais jetable est en quarantaine conforme. Rien n'est laissé
en « plus tard » sans registre.

Auditeur : orchestrateur (session Compliance-Ingenierie), sur autorisation mainteneur.
Modifications non commitées d'une session concurrente (roadmap, DEVOPS, docs/12, agents)
constatées et **non touchées** par cet audit.

**Note datée du 2026-09-30 (lot E1 d'ADR-0028 ; lignes précédentes inchangées)** : l'écart G0 du modèle de menace, non formalisé en document unique (l.13 et l.41), est soldé par `docs/17-modele-de-menace.md` : surface servie, transport, vérificateur, chaîne d'approvisionnement, méthode et chemin S2, sous revue G2 et cp-2 ; ses items et exigences sont à l'annexe B d'ADR-0028.
