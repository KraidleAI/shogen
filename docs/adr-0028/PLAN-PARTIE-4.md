# Partie 4 de S2 — données : plan (2026-10-02 ; accord de l'investisseur du même jour)

Accord de l'investisseur (verbatim, 2026-10-02 21:1x UTC) : « oui, lance la partie 4 ». Il couvre la **préparation**
(étape P ci-dessous). L'**exécution unique** (étape E) exige un acte distinct de l'investisseur, après l'échéance du
délai de 24 h (2026-10-03T17:44:30Z ; annexe D.4 b (5)-(6) ; paquet §9). Rattachement : ADR-0028 D2, D.4 b-c, D6 (vi),
D9 ; `docs/adr-0028/PARTIES-S2.md` (partie 4 : ancre, 24 h, exécution unique, `docs/11`, clôture S2) ; méthode
`docs/METHODE-PARTIES.md` ; paquet scellé `docs/adr-0028/PAQUET-PREREG-S2.md` (sha256 `494d770d…`, inchangeable).

Branche : `partie-4-execution`, depuis `claude/compassionate-noether-szmdyj` (`b254b89`).

## 1. Étapes

| étape | contenu | qui | quand |
|---|---|---|---|
| **P1 — hôte** | hôte de l'exécution = session cloud Linux (SHOGEN-RENDU-HOTE-1 : `--gardes-seules` en refus fait avant le scellement, fichier de sommes réel lu) ; SHOGEN-HOTE-ATTRIBUTS-GIT-1 et SHOGEN-P3-HOTE-1 mesurés ; items propres à Windows sans objet (ENREG-TEST-BASH-1, HARNAIS-BASH-WSL-1), consignés | orchestrateur | avant E |
| **P2 — outils de contrôle versés** | `scripts/controle/` : `fm11.py` (SHOGEN-FM11-VERIFIABLE-1), `regle_fixtures.py` et `render_fixture.py` (SHOGEN-REGLE-EMPREINTE-OUTIL-1), avec leurs sha256 et sorties JSON ; hors des chemins gardés (2) et de la suite | orchestrateur ; relecture G2 de la partie | avant E |
| **P3 — seuil « flux presque mort »** | SHOGEN-FLUX-QUASI-MORT-1 : seuil fixé d'avance par un auteur **neuf, sans exposition** aux taux de présence par flux (attestation D.3), écrit à l'annexe B par amendement daté ; la sensibilité elle-même est un lot après E | advisor frais (`shogen-advisor`, `claude-fable-5-1`) | avant E |
| **P4 — G2 du chemin de recalcul** | SHOGEN-G2-HISTO-RECALCUL-1 : pour chaque module du chemin de recalcul, référence du G2 qui l'a couvert (rapport, sha) ; à défaut, G2 de rattrapage | lecteur (`shogen-lecteur`, `claude-sonnet-5-5`) ; orchestrateur | avant E |
| **P5 — procédure d'exécution** | `docs/adr-0028/PROCEDURE-EXECUTION.md` : téléchargement et contrôle des journaux (sha256 contre le bloc), nettoyage `__pycache__` (RENDU-PYCACHE-1), tailles et mémoire (RAW-MEMOIRE-1, RENDU-COUT-1), `--gardes-seules` puis production, lecture de l'enregistrement « rendu » (ENREG-VARIABLE-1, CP2-RUNS-RENDU-1), contrôle des comptes de la suite (SHOGEN-CI-S2-SAUT-1 : `Ran` et `skipped` attendus), échec sans sortie (RENDU-ECHEC-DIAG-1), consignes au JOURNAL, contrôle FM-1.1 de la transcription | orchestrateur ; relecture G2 de la partie | avant E |
| **E — exécution unique** | sur acte de l'investisseur après l'échéance ; procédure P5 ; sorties et sha256 au JOURNAL | orchestrateur | ≥ 2026-10-03T17:44:30Z |
| **R — rapport** | `docs/11` (rapport public de S2) : verdict de la règle, énoncés du pt 8, limites du paquet §12, déviations déclarées (D.1 n° 16) ; sensibilités ajoutées après le pré-enregistrement (FLUX-QUASI-MORT-1, HOST-DEGRADED-2, CENSURE-INFO-2…) étiquetées | rédacteur ; validateur ; investisseur (publication) | après E |
| **C — cp-2 et clôture** | cp-2 (dont CP2-RUNS-RENDU-1), items d'après l'exécution (SCEAU-VERIFY-REQUETE-1, R1-DOCSTRINGS-1), G7, clôture de S2 | validateur ; orchestrateur | après R |

Relecture G2 de la partie par une instance neuve, revue de partie, fusion `--no-ff`.

## 2. Règles propres à la partie

- Aucun changement dans `s2-harness/shogen_s2`, `s2-harness/tools` ni `s2-harness/tests` avant E (garde (2) ; décision de B.35 : la suite est la première commande de l'exécution).
- Les journaux scellés ne sont ni téléchargés ni ouverts avant l'acte de l'investisseur ; avant lui, seules leurs métadonnées Drive (nom, taille) sont lues.
- Aucune publication par l'orchestrateur ; `docs/11` est publié sur décision de l'investisseur.
- Pocket : aucune déclaration publique avant la date de divulgation coordonnée.
