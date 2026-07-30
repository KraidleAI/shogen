# Shōgen (証言 — « témoignage »)

**Infrastructure de faits attestés pour agents IA — le pendant « perception »
du noyau d'autorité Kraidle.**

## La phrase fondatrice

Une attestation prouve **ce que la source a dit** — jamais que la source dit
vrai. Tout le projet tient dans cette distinction, et le nom la porte : un
témoignage est une déposition, pas une vérité.

## Le produit en une phrase (hypothèse de travail, non figée)

Une couche qui transforme les réponses du monde (APIs, flux, pages) en
**témoignages attestés, typés en faits datés à provenance traçable**
(l'attestation couvre les octets ; le typage est un adapter identifié —
03 §3), agrégés par **quorums dont la diversité est mesurée sur ses axes
observables** (infrastructure, dépendances amont) **et seulement déclarée
sur les autres** (juridiction, opérateur), rangs publiés (04 §1), et livrés
dans un vocabulaire qu'un noyau de décision — Kraidle en premier — peut
consommer, avec vérification offline du lot par un tiers.

## La relation à Kraidle

- Kraidle : *bounded authority* — aucune action irréversible sans permit lié
  aux bytes. La perception y est bornée et rendue visible, jamais empêchée.
- Shōgen : *attested perception* — aucun fait critique sans témoignage lié à
  sa source, et aucun quorum sans mesure d'indépendance.
- Le `gather` de Kraidle exige des faits signés par leurs sources
  (ADR-0017 Kraidle) et des quorums pour les classes critiques (ADR-0023) ;
  A(indépendance des sources) y est une dette nommée non déchargée. Shōgen
  est l'outil qui la décharge. Les deux projets restent souverains : Shōgen
  se vend à tout agent, avec ou sans Kraidle.

## État du projet

- 2026-07-30 : création. Trois idées candidates enregistrées
  (`docs/00-idees.md`), Shōgen retenue. Passe librarian exécutée
  (`docs/01-precedents.md`, `biblio/INDEX.md` — 8 artefacts) ; conclusion
  principale : le primitif de transport (zkTLS) est mûr et ne doit pas être
  reconstruit (ADR-0001, `docs/DECISIONS.md`) ; le gap est la couche
  sémantique/quorum/diversité au-dessus. Écrits le même jour : vision
  (`02`), forme canonique de témoignage (`03`), certificat de diversité
  (`04`), roadmap S0–S5 (`05`), plan DevOps (`DEVOPS.md`). Dépôt
  `Kraidle/shogen` créé (privé), commit fondateur signé. Un audit
  documentaire multi-agents (22 trouvailles confirmées) a été appliqué le
  même jour — ce texte en intègre les corrections.

## Discipline

Ce projet adopte dès le jour 1 la discipline de Kraidle, adaptée : les trois
mots d'assurance (proven/tested/reviewed), les sources ouvertes avant d'être
citées, les chiffres mesurés dans la passe, les décisions en ADR avec
alternative et coût. Les skills `kraidle-*` s'appliquent mutatis mutandis
jusqu'à ce que Shōgen ait les siens.
