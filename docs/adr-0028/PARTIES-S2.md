# Fin de S2 en parties (méthode `docs/METHODE-PARTIES.md`, décision de l'orchestrateur, 2026-10-01 00:15 UTC)

Décision investisseur (verbatim, 2026-10-01 00:15 UTC) : « j'ai arrété le workflow que tu viens de lancer, pas 100000000000 gates encore pour prendre une décision, tu fais tout toi méme. » — le découpage est fixé par l'orchestrateur, sans circuit d'avis.

## Parties
| partie | contenu (lots d'ADR-0028, annexe A) | nature | branche |
|---|---|---|---|
| **1 — moteur** | B-DEP-1, B-DEP-2, CRITERE, D5-AMEND | calcul pur (`r1.py`, blocs 1/3/6 de `report.py`), rien d'exécuté sur les données de campagne | `partie-1-moteur` |
| **2 — intégration et gardes** | DOCS-S2-b, RENDU-1 (exécution unique fail-closed, gardes D.4 b), RENDU-2 (enregistreur d'oracle) | chemin d'exécution et ses gardes | `partie-2-rendu` |
| **3 — texte scellé** | PAQUET (pré-enregistrement, sceau, requête RFC 3161) | texte servi | `partie-3-paquet` |
| **4 — données** | ancre (acte investisseur), 24 h, exécution unique, `docs/11`, clôture S2 | données | `partie-4-execution` |

Hors parties (chantiers distincts, finissent leur circuit) : D8b, D8c (gates), CI-RUNNER-1 (runner auto-hébergé), FUZZ (reporté après S2).

## Règles appliquées
- **Par partie** : un plan court (fichiers, tests, risques) ; tests d'abord, valeurs de référence indépendantes du code, échec montré avant correction ; une mutation par test ; **une** relecture G2 par une instance neuve sur toute la partie ; **une** revue de partie par l'orchestrateur (siège propriétaire de la production : session unique, pas de messagerie), oracles rejoués ; **accord de l'investisseur une fois par partie**.
- **Supprimé** : cp-1 par lot, re-revues rr1 par lot, sous-lots émiettés, avis d'advisors systématiques (advisors seulement sur un choix technique réel).
- **Taille** : plafond 200 lignes de code par commit de lot (R-25), rempli au lieu d'émietté ; documents hors compte.
- **Git** : une branche par partie depuis `main` ; les lots y sont commis ; fusion dans `main` par **commit de fusion** (`--no-ff`) après la revue de partie ; jamais de rebase, de push forcé ni de réécriture d'historique. Une branche en retard se met à jour par fusion de `main`.
- **CI** : tant que le runner n'existe pas, la « CI verte » est l'ensemble des oracles locaux rejoués par l'orchestrateur sur la tête de la branche (suite `s2-harness`, tests nommés sur copie scellée, `cargo --locked xtask verify`, runners d'`enforcement/`) ; limite nommée, levée à l'installation du runner (CI-RUNNER-1).
- **Gardé intact** (intégrité du pré-enregistrement, pas des gates de décision) : D.2 (pièces interdites, rédacteurs frais du PAQUET), D.3 (attestations), D.4 (tests nommés, gardes d'exécution, ancre + 24 h), aucune exécution sans acte de l'investisseur.
- **Lots en vol** : B-DEP-1/2, CRITERE, D5-AMEND finissent leur run (`wf_1c82774a-d5f`) ; leurs livrables sont commis sur `partie-1-moteur` ; leurs G2 par lot tiennent lieu de relecture ; la revue de partie se fait une fois, à la fin, sur le diff entier de la branche.
