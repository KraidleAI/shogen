# Shōgen — cartographie générale (2026-10-02, reprise en session cloud)

Orchestrateur de la session cloud (`claude-opus-5-5` ; roster : `claude-fable-5-1`, écart consigné au JOURNAL).
Demande de l'investisseur, avant tout lancement de la partie 2 : « cartographie générale [...] afin de structurer
ton travail ». Faite par l'orchestrateur seul, en lecture et en mesure (décision investisseur du 2026-10-01
00:15 UTC : pas de circuit d'agents pour décider). Base : branche `claude/compassionate-noether-szmdyj` à `8dd28e2`
(= `d73327f` de la passation + la préparation de la partie 2). Référence antérieure :
`docs/rapports/cartographie-2026-09-29.md` (dite « carto 09-29 »).

## 1. Le projet en une table

| bloc | chemin | rôle | état mesuré le 2026-10-02 |
|---|---|---|---|
| cœur et vérificateur | `crates/shogen-core`, `crates/shogen-verifier` | témoignage canonique, vérification offline (S3) | `cargo test --locked --workspace` : 206 réussis, 0 échec (carto 09-29 : 205) |
| gates du dépôt | `xtask/` (S-G1 à S-G8, fmt, `no_std`, clippy) | doctrine ADR-0013 | `cargo --locked xtask verify` VERT ; S-G5 en régime partiel (0 artefact sur 125), S-G6 non contrôlable sans octets |
| adapters (workspaces autonomes) | `adapters/shogen-temoignage`, `shogen-typer`, `shogen-tlsn-verify` | témoignage réel, typeur, compagnon TLSNotary | témoignage 20/20 ; typeur 28/28 ; compagnon : 0 test exécuté à sa racine (4 tests sous `session/`, non lancés ici) |
| garde-fous de commit | `enforcement/` (hook, lint d'épinglage, gate des secrets) | D8a-c | runners 51 / 95 / 113 ok ; secrets 328 fichiers et 195 commits, 0 constat ; hook installé conforme |
| harnais S2 | `s2-harness/shogen_s2/` (`r1.py`, `r2.py`, `report.py`, collecte) | mesure R1/R2 de la campagne S2 | 307 tests OK, 2 sauts (tests nommés sans copie scellée : état normal) |
| registres | `JOURNAL.md`, `docs/DECISIONS.md`, `docs/adr-00xx/`, `docs/08`, `docs/09` | décisions et hypothèses | écarts au §4 |
| CI GitHub | `.github/workflows/` (gates, compagnon, témoignage, fuzz, mutation, reproductibilité, squelette) | jobs bloquants g1/g3/g5, `s2-harness-unittest` | ne tourne que pendant une fenêtre publique ouverte par l'investisseur ; aucun run sur la PR KraidleAI/shogen#1 |
| fuzz | `fuzz/` | distillation | reportée après S2 (SHOGEN-FUZZ-DISTILLATION-1) |

## 2. Où en est S2 (ADR-0028, méthode par parties)

| partie | lots | état |
|---|---|---|
| 1 — moteur | B-DEP-1, B-DEP-2, CRITERE, D5-AMEND | **fusionnée** (`eb1b13d`), sur la branche de passation ; pas encore dans la `main` de GitHub |
| 2 — intégration et gardes | DOCS-S2-b, RENDU-1, RENDU-2 | accord de l'investisseur donné le 2026-10-02 ; **non lancée** (cette cartographie d'abord) |
| 3 — texte scellé | PAQUET, sceau RFC 3161 préparé | à faire ; exige la biblio (Künsch 1989, Fisher 1921) |
| 4 — données | ancre, 24 h, exécution unique, `docs/11`, clôture S2 | sur le poste local seulement (copie scellée de campagne) |

Les lots d'avant les parties (CI-S2, B0, B-SEG-1/2, B, POOLEE, E1, DOCS-S2-a, SIM-NIVEAU, D8a-c) sont commis.

## 3. Items de l'annexe B : ce qui retombe sur chaque partie

Annexe B : 119 items distincts ; 7 marqués fermés dans le texte (d'autres sont soldés par des lots commis sans
mention « fermé » : tri à faire au lot registres). Classement par la colonne d'échéance, relu item par item pour
la partie 2.

**Partie 2 — 20 items, contre 12 dans la première version du plan** (corrigée ce jour, `PLAN-PARTIE-2.md`) :

| étape du plan | items (SHOGEN-…) |
|---|---|
| A — rendu (G0 de DOCS-S2-b et de RENDU-1) | REPORT-FISHER-1 ; GARDE-LIBELLE-1 ; BLOC3-RENVOI-TAU-1 ; RENDU-ZERO-1 ; AXES-ENONCE-1 ; SENS-PERTES-2 ; DECIMAL-ARRONDI-1 ; PMORE-RESIDU-1 ; **BLOC1-RUNPARAMS-1** ; **SENS-PLAGES-1** ; **ASN-STATUT-1** |
| B — RENDU-2 (G0 de RENDU-2) | ORACLE-ENREG-1 ; TORN-LINE-UTF8-1 ; RAW-LECTEUR-1 ; **BLOC6-TS-1** ; **D5-RECALCUL-TIERS-1** ; **CENSURE-CAUSES-1** |
| C — RENDU-1 | RENDU-UNIQUE-1 ; **HOOK-SUITE-S2-1** (suite `s2-harness` dans le hook, ou non : décision au G0) |
| avant le G0 de RENDU-1 | **ORACLE-PERIMETRE-1 (i)** : étendre S-G4 et S-G5 à `s2-harness/**/*.md`, avec mutants de gate (lot Rust dans `xtask/`) |

En gras : absents de la première version du plan. Hors partie 2 malgré un renvoi : PAQUET-ERRATUM-FISHER-1
(partie 3, avant le sha du paquet), DONG-CORPS-1 (G0 du lot G9, partie 4), COLLECTOR-FISHER-1 (prochain G0 de
collecte), DOC-HARNAIS-1 (porté par DOCS-S2-a2, à fermer au lot registres).

**Partie 3 — 15 items** (dont PREREG-S2-1, CRITERE-PT10-CLAUSE-1, CRITERE-GARDE-NIVEAU-1, POOLEE-SOURCE-1,
SCEAU-ANCRE-1, E1-D2-COMPLETUDE-1, PAQUET-ERRATUM-FISHER-1). **Partie 4 — 15 items** (dont PAROXYSME-REGISTRE-1,
PASSAGE-PUBLIC-EXPORT-1, VITRINE-MONARK-1, S2-TUYAU-MONARK-1, D8-AMONT-ERRATUM-1). **Hors S2** : environ 55
(gates, secrets, menaces, fuzz, S3).

## 4. Écarts registre / réalité constatés ce jour (règle Branchement : à solder avant toute pièce neuve qui en dépend)

1. **ADR-0028, statut périmé** : l'en-tête dit « G0 proposé [...] À soumettre au cp-1 bis » ; le cp-1 bis a eu lieu
   (JOURNAL l.96 : ACCEPTE-AVEC-CORRECTIONS CB-1..CB-10). Le §1 bis (l.63, l.80 A-8, l.152) dit encore « SOUS ESCALADE
   — en attente de l'investisseur » ; la réponse est au JOURNAL du 2026-09-30 23:33 UTC (« Oui » ; veto : « Ok pour
   les quatre »). Correction : ajout daté, sans réécriture, au premier commit de la partie 2.
2. **Index de `docs/DECISIONS.md`** : s'arrête à ADR-0023 (l.27) ; ADR-0024 à ADR-0028 absentes de l'index
   (SHOGEN-REGISTRES-S2-1, ouvert ; REG-02 de la carto 09-29). Hors partie 2 ; lot registres.
3. **Roadmap `docs/05`** : figée au 2026-08-20 (`82e1cc9`) ; l'état S2 qu'elle porte est périmé (même item).
4. **Biblio en cloud** : S-G5 tourne en régime partiel. SHOGEN-ORACLE-PERIMETRE-1 (ii), échéance « immédiat » :
   tout lot qui touche `docs/**/*.md` doit être rejoué en corpus complet. Concerne les deux documents écrits en
   session cloud (`PLAN-PARTIE-2.md`, cette cartographie) et tous les documents de la partie 2. **Bloqué** : le
   connecteur Google Drive de la session refuse la lecture (« Insufficient scope », constaté deux fois le
   2026-10-02, à 02:3x et 02:4x UTC).

## 5. Contraintes d'environnement (session cloud)

| contrainte | effet | conduite |
|---|---|---|
| Drive illisible (droit de lecture non accordé au connecteur) | pas de biblio : S-G5 partiel, rejeu ORACLE-PERIMETRE-1 (ii) impossible, partie 3 bloquée | l'investisseur reconnecte Google Drive avec la lecture des fichiers, puis ouvre une nouvelle session |
| effort `max` explicite des workers (roster) | l'outil d'agents de la session ne porte pas l'effort ; une fiche d'agent projet le porte, active au démarrage d'une session | fiche `.claude/agents/shogen-worker.md` (`claude-opus-5-5`, `effort: max`) commise avec cette cartographie ; active à la nouvelle session |
| copie scellée de campagne absente | tests nommés sautent ; partie 4 locale | leur rejeu sur la tête de la partie 2 se fait sur le poste local |
| `main` de GitHub protégée, PR KraidleAI/shogen#1 bloquée (une approbation) | `main` non poussée | travail sur branches ; acte de l'investisseur |
| OpenSSL 3.0.13 (hôte : 3.5.7) | jetons RFC 3161 de fixture | produits et vérifiés par la même version ; vérification réelle sur l'hôte (partie 4) |
| Firecrawl en cloud : outils `mcp__Firecrawl__*`, pas l'UUID de CLAUDE.md | les fiches qui nomment l'UUID ne le reçoivent pas | sans effet sur la partie 2 |

## 6. Risque à décision de l'investisseur (valeur, droit : non technique)

- **Rapport Pocket dans le dépôt** : `docs/pocket-report/` (rapport de divulgation, lettre, registre des
  affirmations) est versionné ; le dépôt passe en public pendant chaque fenêtre de CI. Pocket a accepté le
  2026-10-01 une **divulgation coordonnée à 90 jours** ; une fenêtre publique rend ce rapport lisible et clonable
  avant la date convenue. La décision du 2026-10-01 00:24 UTC (« personne n ira chercher un papier pocket chez
  nous ») est antérieure à cet accord. Aucun acte de l'orchestrateur ; décision rendue à l'investisseur.

## 7. Ordre de travail qui en découle

1. **Nouvelle session** (Drive lisible, fiche des workers active), sur la branche `claude/compassionate-noether-szmdyj`.
2. Recopie de la biblio (§5 bis de la passation), jamais committée ; `xtask verify` en régime complet (S-G6 = 125) ;
   rejeu des deux documents cloud en corpus complet (ORACLE-PERIMETRE-1 (ii)) ; lien du Drive inscrit dans la
   passation par un commit daté.
3. Branche `partie-2-rendu` ; premier commit : correction datée du statut d'ADR-0028 (§4, point 1).
4. ORACLE-PERIMETRE-1 (i) (S-G4/S-G5 sur `s2-harness/**/*.md`), puis étapes A, B, C du plan ; une relecture G2 ;
   une revue de partie ; fusion locale, poussée sur une branche.
5. Partie 3 (lectures Künsch et Fisher sur la biblio recopiée, rédacteurs frais) ; partie 4 sur le poste local.

## 8. Registre PAROXYSME (rappel obligatoire)

Registre hors dépôt (`F:/PRODUITS/paroxysme-2026-09-27/PAROXYSME-Shogen.md`, sha `a655c401…`, périmé ;
SHOGEN-PAROXYSME-REGISTRE-1, échéance clôture S2), illisible en cloud. Procurements P-01 Künsch et P-03 Fisher
**reçus**, non lus (biblio non recopiée) ; P-15 Shostack et SHOGEN-POOLEE-SOURCE-1 (Mantel-Haenszel 1959,
Cochran 1954, Agresti 2013) en attente ; FUZZ reporté après S2. Aucun item neuf formé ce jour : les limites
déclarées aux §4 et §5 sont portées par des items existants (ORACLE-PERIMETRE-1, REGISTRES-S2-1,
PAROXYSME-REGISTRE-1) ou seront formées au G0 qui les rencontre (plan, §5).
