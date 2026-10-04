# G0 des lots de fermeture des dettes d'après l'exécution (DETTES-*), 2026-10-04

Rattachement : directive de l'investisseur du 2026-10-04 (verbatim : « ne laisse pas de dettes, clos dés que possible ») ;
état exact du registre `docs/adr-0028/ETAT-REGISTRE-2026-10-04.md` (94 ouverts : A 13, B 25, C 10, D 2, E 26, F 9, G 9) ;
ADR-0028 (D6, D9, annexes A-D), paquet scellé §11-§12, rapport `docs/11-mesures-pilotes.md`. Créé le 2026-10-04 03:54:43 UTC (heure produite par
le script d'écriture). L'exécution unique est faite (2026-10-04) : la garde (2) ne s'applique plus ; tout changement de code
est postérieur aux rendus, n'y touche pas, et ne les réécrit jamais (les rendus versés restent la seule sortie de décision).

## Règles communes

Tests d'abord (rouge avant, vert après) ; R-25 (≤ 200 lignes ajoutées par commit) ; R-13 ; R-8 (aucune dépendance nouvelle
sans vérification de registre ; préférence : bibliothèque standard) ; travail des workers sur une copie, diffs livrés,
l'orchestrateur committe ; relecture G2 par une instance neuve avant commit ; FM-1.1 de chaque transcription ; interdits :
`docs/15-*`, `docs/16-*` (Pocket), `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`.

## Lots (listes fermées)

| lot | items | nature | lit les journaux scellés |
|---|---|---|---|
| **DETTES-A** (documents) | REGISTRES-S2-1, ERRATA-ADR0028-1, DOC-HARNAIS-2, HARNAIS-ECHAPPEMENTS-1, WORKTREE-BASE-HOOK-1, HARNAIS-TACHE-10MIN-1, HARNAIS-BASH-WSL-1, MUT-FATAL-1 | ajouts datés ; consignes versées à la fiche `.claude/agents/shogen-worker.md` (corps, jamais le champ `model`) | non |
| **DETTES-BIBLIO** | G4-BIBLIO-1, BIBLIO-GIT-CHECKOUT-1, E1-MAST-VERSEMENT-1 | versement à `biblio/` avec sha256 et ligne d'INDEX, page de titre lue | non |
| **DETTES-B1** (harnais) | PRIX-ILLISIBLE-1, PRIX-HORS-CONTEXTE-1, ASN-DIVERGENCE-PARTIELLE-1, BLOC5-LIBELLE-1, RT-ETIQUETTE-INCLUSE-1, KEFF-NOTE-1, SENS-POOLEE-1, CI-S2-SAUT-1 | correctifs et tests dans `s2-harness` ; règle `ea3a2d94…` et épingles inchangées sauf libellés déclarés | non (fixtures) |
| **DETTES-B2** (gates) | D8D-SECRETS-1 (et SECRETS-MESSAGES-1, -CHEMIN-ETAGE-1, -GREP-STATUT-1, -MASQUE-EXCLUSION-1), SECRETS-HORS-REFS-1, G5-ERREUR-GREP-1, CI-RUNNERS-1, E1-XTASK-REFS-1 | `xtask`, `enforcement/`, `.github/workflows/` | non |
| **DETTES-SIM** (synthétique) | BARTLETT-BIAIS-1, GARDE-NIVEAU-N-1, SIM-NIVEAU-MODELES-1, SIM-NIVEAU-P-1, FLUX-QUASI-MORT-2, FLUX-FAIBLE-1, POOLEE-BLOC-1 (b) | `scripts/sim/`, sorties versées | non |
| **POST-PREREG** (analyses ajoutées après le pré-enregistrement, hors décision) | FLUX-QUASI-MORT-1 (avec QUASI-MORT-PREDICAT-1, POOL-MIN-1), HOST-DEGRADED-2, CENSURE-INFO-2, DEP-FENETRES-2, R1-PLUGIN-1, CONTENU-DEP-1, FLUX-DEVIANT-1, HORLOGE-ETENDUE-1, SIGMA-BLOC-INDEP-1, POOLEE-BLOC-1 (a) | `scripts/post-s2/` ; chaque sortie étiquetée « ajoutée après le pré-enregistrement, hors décision » ; aucune ne remplace une valeur des rendus | **oui** (copie locale de la session, jamais affichée en entier ; aucun journal versé) |
| **CP2-G7** | INSTRUMENT-S2-1, CP2-RUNS-RENDU-1 | cp-2 d'un validateur frais, G7, clôture de S2 | non |

Classes E (jalons ultérieurs), F (décisions de l'investisseur) et G (poste local) : restent ouvertes avec leur déclencheur,
posées à l'investisseur en une fois ; elles ne sont pas des dettes oubliées.

## Déviations déclarées (constat de l'état du registre)

- Tests nommés de D.4 a sur la copie scellée, « dus avant l'exécution unique » : non rejoués avant l'exécution ; rejoués après
  par l'orchestrateur (SHOGEN-ENREG-VARIABLE-1), déviation consignée.
- Contrôle FM-1.1 de la transcription de l'exécution (procédure §5) : non consigné ; fait après par l'orchestrateur.
- Ancre OpenTimestamps (paquet §9) : formée en item (SHOGEN-SCEAU-OTS-1), décision de l'investisseur.

> *Ajout daté du 2026-10-04 06:52:35 UTC (relecture G2 du lot DETTES-B1, C-4 ; annexe B.4)* : pour SHOGEN-CI-S2-SAUT-1, l'orchestrateur retient un **plancher** du nombre de tests, et non un manifeste des modules (motifs du journal G1 du lot, §9 : le plancher refuse les deux pertes mesurées par le lot CI-S2, module renommé et retrait partiel, alors qu'un manifeste de modules ne voit pas un retrait partiel dans un module ; limite : après une croissance de la suite, un retrait inférieur à l'écart au plancher passe) ; valeur `PLANCHER = 405`, le compte mesuré après le lot ; il suit le compte aux lots suivants (SHOGEN-CI-PLANCHER-SUIVI-1). B.4 réservait ce choix à un G0 ; le G0 de D8a ne l'avait pas tranché.
