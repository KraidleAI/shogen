# ADR-0028 — Annexe B : items formés (C-15 ; CA-7)

Rédaction : 2026-09-29 (rédacteur `claude-opus-5-5`).
- « orch. » = orchestrateur Shōgen `claude-fable-5-1`.
- « avant scellement » = avant l'écriture du sha du paquet au JOURNAL (D2).
- « avant le rendu » = avant l'exécution unique (annexe D.4 b).
- Les définitions de CENSURE-INFO-1, HOST-DEGRADED-1, DP-JOURNAL-LOSS-1 et COLLECT-PREVWS-1 sont dans la dimension « campagne » de la cartographie. Cette pièce est interdite au rédacteur (annexe D.2) : leur libellé est **formé en demande** à l'orchestrateur (mécanisme et comptes, sans taux), il n'est pas deviné.

## B.1 Items d'ADR-0028 (reprise de l'ancien §5, déclencheurs complétés)

| item | objet | propriétaire | déclencheur | origine |
|---|---|---|---|---|
| SHOGEN-POOL-ANALYSE-PYTH-1 | D1 : règle du pool d'analyse, cas (a), (b), (c) | orch. | G0 du lot B0 (annexe A) ; au plus tard avant scellement | SUP-01 (`critique.md` l.165) ; AVIS-advisor-defi Q1 |
| SHOGEN-PREREG-S2-1 | D2 : paquet de pré-enregistrement | orch. ; rédaction et validation par agents frais | rédaction après le cp-1 bis de cette ADR ; scellement après les commits des lots POOLEE et RENDU, avant l'exécution unique | SUP-02 ; AVIS-advisor-defi Q2 ; AVIS-advisor Q2 ; absorbe SHOGEN-S2-INTERIM-READ-DISCLOSURE-1 (cartographie §5) |
| SHOGEN-POOLEE-STRATIFIEE-1 | D2 pt 4 : forme stratifiée, exploratoire, m = 2 ; supplante SHOGEN-STRATE-POOLEE-1 côté Shōgen | orch. | G0 du lot POOLEE | F-DP-01 ; décision 273 (CHANTIERS MONARK l.1971) ; AVIS-advisor-defi Q2 pt 4 |
| SHOGEN-DEP-FENETRES-1 | D2 pt 7 : sensibilité par blocs, taille de bloc fixée à l'aveugle | orch. (au paquet) | avant scellement | AVIS-advisor-defi Q2 pt 9 |
| SHOGEN-J14-TRONCATURE-1 | D4 : troncature de tous les types par horodatage | orch. | G0 du lot B-SEG-1 | HS2-08 |
| SHOGEN-EXCL-TOUS-TYPES-1 | D5 : exclusion ADR-0025 de tous les types | orch. | G0 du lot B-SEG-1 | Q-G2-3 ; AVIS-advisor-defi Q5 |
| SHOGEN-EXCL-COMPTE-1 | fenêtres retirées par plage et par strate au bloc 1 | orch. | G0 du lot B-SEG-2 | O-1 du G2 du lot A |
| SHOGEN-NEG-EPOCH-1 | refus des epochs négatifs (rc 2) | orch. | G0 du lot B-SEG-2 | Q-G2-5 |
| SHOGEN-TESTS-TMP-1 | nettoyage des `mkdtemp` de la suite | orch. | G0 du lot B0, premier lot qui touche `s2-harness/tests/` sous cette ADR | O-4 du G2 du lot A (« prochain lot touchant `tests/` ») |
| SHOGEN-INSTRUMENT-S2-1 | D6 : frontière recalcul/collecte, G0-G7 sur le chemin de recalcul | orch. | cp-1 bis de cette ADR, puis lot CI-S2 | HS2-13 ; GC-06 ; AVIS-advisor Q6 ; AVIS-advisor-marche Q6 ; cp-1 C-5 |
| SHOGEN-BUNDLE-CLOTURE-1 | D7 : bundle refait | orch. | chaque commit de clôture, tant que le push n'est pas complet | AVIS-advisor Q7 |
| SHOGEN-ENFORCEMENT-PORTAGE-1 | D8 : lots D8a, D8b, D8c, puis tag, puis suppression de la branche | orch. | G0 de D8a, après la confirmation §4.10 a (l'étape 1 est faite, `3d8c185`) | GC-05 ; REG-09 ; AVIS-advisor Q8 |
| SHOGEN-G4-NOTAIRE-RECHERCHE-1 | D9 : recherche du notaire tiers et de la clé du notaire (recherche de solutions, sources à l'appui) | orch. | maintenant (sans code) ; rendue avant tout lot G4 | PX-Shogen-3 ; F-DP-35 ; L-41 |
| SHOGEN-KRAIDLE-GATHER-1 | arête S4 → `gather` Kraidle | forme et transmission : orch. ; propriétaires de l'arête : orchestrateurs MONARK et Kraidle | G0 de S4 | CARTO-MK-08 ; AVIS-advisor-marche §5 |
| SHOGEN-E1-THREAT-MODEL-1 | D10 : modèle de menace | orch. | maintenant (lot E1) | F-DP-10 ; AUDIT-ENTREE G0 |
| SHOGEN-FUZZ-DISTILLATION-1 | D10 : distillation du corpus et gate | orch. | maintenant (lot FUZZ) | F-DP-09 ; 13 §7.3 |
| SHOGEN-PASSAGE-PUBLIC-EXPORT-1 | D10 : ADR « passage public par export filtré » | ADR : orch. ; décision : investisseur (§4.10 b) | clôture S2 (G7) | AVIS-advisor Q10 ; `docs/DEVOPS.md` l.21-39 |
| SHOGEN-TASK-72H-1 | aucune collecte longue ne repose sur une tâche planifiée à limite d'exécution par défaut (72 h, code `0x41306`) | orch. | G0 de la prochaine collecte longue (campagne C7 ou collecte S3). État : les quatre tâches ont été supprimées le 2026-09-29 (JOURNAL l.92) ; aucun risque actif | C-01 (cartographie §3 l.47) |
| SHOGEN-SCHED-MONITOR-1 | chaîne d'alerte vers un humain (watchdog → action) | orch. | G0 de la prochaine collecte longue. État : watchdog supprimé | arête E34 (« 54 alertes sans action », `critique.md` §4.1) |
| SHOGEN-TAU-REDERIV-1 | τ non re-dérivé après le 1er week-end | orch. | traitement au paquet avant scellement : **descriptif seulement** (annexe D.5) ; re-dérivation = PX-Shogen-13 (C7), après le rendu, jamais appliquée aux z confirmatoires | ADR-0022 pt 3 ; F-DP-06 ; cartographie §3 l.48 |

## B.2 Items ajoutés (C-15)

| item | objet | propriétaire | déclencheur | origine |
|---|---|---|---|---|
| SHOGEN-CENSURE-INFO-1 | fenêtres sautées alors que le harnais tournait (censure possiblement informative) | orch. ; libellé en mécanisme et comptes à compléter | traitement au paquet avant scellement : descriptif seulement (défaut proposé, annexe D.5) | dimension campagne C-10 ; cartographie l.34 (« 645 fenêtres ont été sautées alors que le harnais tournait ») |
| SHOGEN-HOST-DEGRADED-1 | hôte dégradé | orch. ; libellé à compléter | idem | dimension campagne C-11 (`critique.md` §6 étape 3) |
| SHOGEN-DP-JOURNAL-LOSS-1 | pertes du journal dans la plage | orch. ; libellé à compléter | idem | dimension campagne C-12 (`critique.md` §6 étape 3) |
| SHOGEN-COLLECT-PREVWS-1 | à qualifier : sa définition est dans la dimension campagne, non lue par le rédacteur | orch. | qualification avant scellement ; déclencheur définitif fixé à la qualification | `critique.md` §6 item 13 |
| SHOGEN-TORN-LINE-1 (reprise, collecteur) | isolement d'une ligne NUL non finale à la reprise | orch. | G0 de la prochaine collecte longue. Remplace « avant S3 », indéfini (`dettes-paroxysme.md` §A l.71) | REPAIR-2026-09-23 l.27-29 ; ADR-0024 l.23 ; HS2-04 |
| SHOGEN-TORN-LINE-UTF8-1 (lecteur) | `read_jsonl_tolerant` lève `UnicodeDecodeError` si la dernière ligne est coupée dans un caractère multi-octets | orch. | G0 du lot RENDU-2 : le lecteur appartient au chemin de recalcul (D6 i) | HS2-03 (`harnais-s2.md` l.134, l.210) |
| SHOGEN-UPS-1 | alimentation sans interruption ou hôte distant | achat matériel : investisseur ; hôte distant : orch. | G0 de la prochaine collecte longue. Remplace « avant S3 », indéfini | ADR-0024 l.23 ; `dettes-paroxysme.md` §A l.72 |
| SHOGEN-RAW-LECTEUR-1 | lecteur de `raw.jsonl` : la promesse « décodage recalculable » de `journal.py` n'a ni lecteur ni test | orch. | G0 du lot RENDU-2 : lecteur et oracle `sha256_raw` inclus, ou promesse déclarée limite au bloc 1, avec item PAROXYSME | HS2-02 |
| SHOGEN-FETCH-AVANT-PUB-1 | 11 dettes de fetch « avant publication » sans demande formée : à former au format doc 03 §3 (identité, DOI/ISBN, pages, tentatives datées, usage) | demandes : orch. ; procurement : mainteneur | demandes formées avant le G0 du lot G9 | F-DP-13 ; 06 §5.5 ; `dettes-paroxysme.md` B5 |
| SHOGEN-REPORT-FISHER-1 | `report.py:280` imprime « (Fisher) » sans source détenue ; dettes 10.1, 10.4, 10.7 et 2 à re-statuer | orch. ; source : procurement L-46 | G0 du lot RENDU-1 : source procurée, ou attribution retirée de la ligne imprimée | F-DP-14 ; `dettes-paroxysme.md` B1 ; touche D3 |
| SHOGEN-DOC-HARNAIS-1 | README (« 136 verts », option non documentée), RUNBOOK §9 c/e | orch. | lot DOCS-S2, avant le rendu | O-3 du G2 du lot A ; HS2-10 ; HS2-11 ; Q-G1-5 |
| SHOGEN-REGISTRES-S2-1 | REG-02 : index DECISIONS arrêté à ADR-0023 (mesuré ce jour, l.27) ; REG-04 : 05-roadmap figée (dernier commit `82e1cc9`, 2026-08-20) ; REG-05 : trou du JOURNAL du 2026-08-20 au 2026-09-18 (note datée, sans réécriture) | orch. | après le cp-1 bis ; lot registres découpé (R-25) | cp-1 C-15. REG-06 **fermé** : `742f1fc` figure au journal de provenance (1 occurrence, commit `7f8b5cc`). REG-08 **fermé en substance** : CLAUDE.md pt 8 mis au courant (`9621dc3`) ; AUDIT-ENTREE non rafraîchi, renvoi à la cartographie déclaré |
| SHOGEN-PAROXYSME-REGISTRE-1 | registre `F:/PRODUITS/paroxysme-2026-09-27/PAROXYSME-Shogen.md` (sha `a655c401…`, 13 limites sans item) versionné ou référencé par sha ; mise à jour L-36..L-53 et SUP-01/02/04. **Place de C7** : après l'exécution unique, jamais avant (ses items PX-Shogen-13, -21, -23, -25 liraient les données de campagne) ; ses résultats sont étiquetés « ajoutés après le pré-enregistrement » | référence dans le dépôt : orch. ; fichier : orchestrateur MONARK | référence : au commit de cette ADR (§8) ; mise à jour : cartographie de clôture S2 | cartographie §7 ; `dettes-paroxysme.md` §E-F |
| MONARK-S2-M009A-EXPOSITION-1 | mesurer qui, chez MONARK, a vu les valeurs de `measure-M009a.md` (l.85-89) et d'ADR-M002 D6 | orchestrateur MONARK (formé et transmis par Shōgen) | avant scellement | D2 pt 8 ; CARTO-MK-07 ; AVIS-advisor-defi Q2 pt 8 (b) |
| SHOGEN-ORACLE-ENREG-1 | D6 (viii) : schéma `shogen.oracle-record.v1` (**à ratifier**), puis enregistreur Python de la bibliothèque standard | orch. | schéma : dès la ratification ; enregistreur : G0 du lot RENDU-2 | Q-G2-4 ; CA-12 ; cp-1 C-4 |
| SHOGEN-CI-S2-1 | D6 (iii) : job CI `s2-harness-unittest`, en-tête de `gates.yml` | orch. | lot CI-S2, premier lot sous cette ADR | GC-06 ; cp-1 C-5 |
| SHOGEN-G2-HISTO-RECALCUL-1 | pour chaque module du chemin de recalcul, référence du G2 qui l'a couvert (rapport et sha) ; à défaut, G2 de rattrapage | orch. | avant le rendu | cp-1 C-5 ; JOURNAL l.41-42 (G2 déclarés, rapports non localisés) ; `docs/adr-0022/G2-review.md` ; G2 du lot A |
| SHOGEN-FORMAT-JOURNAUX-1 | format des journaux lus par le chemin de recalcul spécifié par référence (`records.py`, `journal.py` au commit `ed479c5` ; doc 10 §6) et scellé | orch. | avant le rendu | AVIS-advisor-marche Q6 (l.88) ; D6 (vii) |
| SHOGEN-CRITERE-R1-1 | règle opérationnelle « R1 discrimine » (D2 pt 10) | orch. (au paquet) | avant scellement | cp-1 C-10 (vi) ; doc 10 l.386-388, l.535-537, l.567-572 |
| SHOGEN-RENDU-UNIQUE-1 | script d'exécution unique, fail-closed (annexe D.4 b) | orch. | lots RENDU-1 et RENDU-2 ; sha du script au paquet, avant scellement | cp-1 C-12 |
| SHOGEN-SCEAU-ANCRE-1 | recherche PAROXYSME : construction qui donne un horodatage externe vérifiable du sha du paquet, avec son prix exact (annexe D.4 c) | recherche : orch. ; acte : investisseur ; ADR-0006 pt 3 : mainteneur | recherche rendue avant scellement ; sinon limite « sceau privé » déclarée au paquet | cp-1 C-13 ; ADR-0006 pt 3 (DECISIONS l.311-314) |
| SHOGEN-S2-TUYAU-MONARK-1 | test de composition `shogen_s2_report_offline_recompute_matches_published` (§3) | dépôt MONARK : orchestrateur MONARK ; `docs/11` et sha : Shōgen | G0 du lot G9 | cp-1 C-17 ; `monark.md` l.126, l.204 |
| SHOGEN-ATTEST-ADVISOR-1 | (i) attestation d'une ligne de l'advisor (Q6-Q10) : « aucune statistique de résultat (z, K, P̂_more, φ) vue ». Sa déclaration (AVIS l.16) ne l'énonce pas, et il a lu la cartographie en entier (annexe D.3 c). (ii) Déclaration de l'advisor-defi : a-t-il lu `campagne.md`, que la CONSULTATION (l.5) prescrivait, et la cartographie l.51 ? (annexe D.3 b) | orch. (re-consultation courte, canal 2) | avant scellement | cp-1 C-6 |
| SHOGEN-ERRATA-ADR0028-1 | actes d'écriture hors de `docs/adr-0028/` (§8 de l'ADR) | orch. | au commit de cette ADR | cp-1 C-9, D1, D5 ; E48 ; REG-02 |
| SHOGEN-VITRINE-MONARK-1 | écart registre public MONARK (Shōgen « built ») / réalité (fixture démonstrative, S2 upcoming) : dérogation datée à la règle Branchement ou correction | investisseur (décision) ; orchestrateur MONARK (exécution) ; transmis par Shōgen | exception datée accordée le 2026-09-29 ; échéance : premier des jalons G2 ou G9 (retrait de l'exception et mise en conformité du registre), ou toute nouvelle revendication publique sur Shōgen | cp-1 bis CB-3/CB-4 ; CARTO-MK-03 ; F-DP-28 ; ADR §4.11 |

## B.3 Items de campagne cités par la cartographie, déjà fermés

- **SHOGEN-LOOP-GUARD-1** : garde posée dans `run-campagne.bat` (test « campagne SCELLEE -- aucune relance », rc 0 ; JOURNAL l.92). Fermé.
- **`Startup\shogen-resume.bat`** : retiré (JOURNAL l.92). Fermé.
- **SHOGEN-BIBLIO-CUSTODY-1** (SUP-04) : sauvegarde de biblio/ (152 entrées) faite dans `D:\shogen-sauvegarde-2026-09-29\` (JOURNAL l.92). La refaire à chaque versement relève de SHOGEN-BUNDLE-CLOTURE-1.
