# ADR-0028 — Annexe D : pré-enregistrement (C-6, C-7, C-10, C-11, C-12, C-13)

Rédaction : 2026-09-29 (rédacteur `claude-opus-5-5`, contexte frais, pièces interdites de D.2 non ouvertes ; exposition déclarée en D.3 f).

**Règle d'écriture de cette annexe** : aucune valeur de taux par source, de z, de K, de P̂_more ni de φ n'y figure. Une lecture est décrite par sa nature, son lieu, sa date et ses lecteurs. Les seuls chiffres repris sont ceux que l'ADR porte déjà : les comptes de Pyth (D1), les diagnostics DNS du harnais (D5) et des comptes de fenêtres.

## D.1 Inventaire des lectures faites sur les données de campagne (C-6)

Classes : **R** = résultat (z, K, P̂_more, φ) ; **M** = marginale ou opérationnelle (composantes de P̂, disponibilité, comptes, santé du harnais).

| # | lecture (nature et lieu) | date | lecteurs connus | classe | valeurs dans ADR-0028 ? |
|---|---|---|---|---|---|
| 1 | G1 du lot A, étape 0 : `r1.recompute_from_journal` sur les copies scellées → `F:\tmp\shogen-j28\work\baseline_step0.out` (772 o, sha `5183e7d1…`, « bloc R1 non filtré », `docs/G1-lot-adr0025-filtre.md` l.114) | 2026-09-28 03:12Z | worker G1 `claude-opus-5-5[1m]` (G1 l.14 : « Les autres chiffres R1 de cette sortie ne sont pas repris ») | **R** | non |
| 2 | MONARK `scripts/measure-m009a.mjs` sur l'instantané du 18/09 → `docs/measure-M009a.md` (l.85-89), repris par ADR-M002 D6 (`critique.md` K-31). C'est une réimplémentation en float64 de `r1.classify_ecart` (`harnais-s2.md` §7) | 2026-09-18 | non établi (MONARK-S2-M009A-EXPOSITION-1) | **R** | non |
| 3 | Dimension « campagne » de la cartographie : `campagne.md` §5 (l.204-216 selon le cp-1) et ses caches `campagne\cache_*.json`. Taux marginaux de panne par source, hors et dans la plage ; pannes par jour et par groupe de flux | 2026-09-29 | worker de la dimension (`claude-opus-5-5`) ; worker critique (lit les sept dimensions « en entier », `critique.md` l.4) ; orchestrateur (D.3 a) ; validateur du cp-1 (l.204-216). Advisors : la CONSULTATION (l.5) prescrivait cette pièce ; advisor et advisor-marché ne la citent pas dans leurs listes de lecture déclarées (D.3 c, d) ; pour advisor-defi, ce n'est pas établi (D.3 b) | **M**, avec une information grossière de co-occurrence (cp-1 §4 pt 3 a) : la plus proche d'un résultat dans cet inventaire | non |
| 4 | Cartographie (synthèse), l.51 : taux marginaux de panne par source, hors et dans la plage. Commitée à `3d8c185` (`docs/rapports/cartographie-2026-09-29.md`) ; identique dans `F:\tmp\shogen-carto-2026-09-29\CARTOGRAPHIE-2026-09-29.md` (le sha256 de la ligne, `5cc89b56…`, est le même dans les deux fichiers ; mesuré par le rédacteur sans afficher la ligne) | 2026-09-29 | orchestrateur ; validateur du cp-1 ; advisor (AVIS-advisor l.9 : « CARTOGRAPHIE (en entier) ») ; tout lecteur du fichier commité | **M** | non |
| 5 | **ADR-0025 l.14** à `7f8b5cc` (l.12 à `d363070`, avant l'errata en tête) ; sha256 de la ligne `0fe88f1a3810244ecce91b31c1f4e2117f397a7c65d381a75afdbf0b9954b71f`, identique aux deux commits (calculé sans afficher la ligne). Taux marginal de pannes de transport d'une source, avant et pendant la plage. Commitée à `d363070` (2026-09-26), acceptée (décision 269). *Trouvaille de cette révision : absente de l'inventaire du cp-1* | 2026-09-26 (pendant la campagne) | auteur d'ADR-0025 (orchestrateur MONARK) ; advisor-defi (AVIS-advisor-defi l.121 cite « ADR-0025 l.12 ») ; lecteurs d'ADR-0025 aux cp-1, G1 et G2 du lot A ; rédacteur (sortie de `grep`, D.3 f) | **M** | non |
| 6 | ADR-0023 l.11 (à `5b6469a`, sha256 de la ligne `014df0caf7a0820c84ee90dea2be6ca68c1fd9e9774e25e9d2fa2ba3b7e7d7f6`) et l.27 ; index DECISIONS l.27 : Pyth, comptes de `panne_http` sur les fenêtres au 2026-09-03 | 2026-09-03 (pendant la campagne) | auteur d'ADR-0023 ; tout lecteur | **M** (un flux mort) | seuls les comptes finals de D1 |
| 7 | D1 : comptes de Pyth sur le journal entier (0 `ok` sur 40 804 ; `critique.md` K-35). Présence ou absence de lectures `ok` par flux et par strate, « sans aucun taux affiché » (AVIS-advisor-defi l.143) | 2026-09-29 | worker critique ; advisor-defi ; orchestrateur ; validateur ; rédacteur | **M** (indicateur binaire de disponibilité) | oui (D1) |
| 8 | D5 : `resolve_failed` dans et hors plage ; comptes `asn_attribution` et `clock_check` (AVIS-advisor-defi l.120, l.136-140) | 2026-09-29 | advisor-defi ; orchestrateur ; validateur ; rédacteur | **M** (santé du harnais DNS, pas une statistique de source) | oui (D5) |
| 9 | Comptes de fenêtres, doublons, heures par strate, couverture par week-end : ADR-0024 l.8-10 ; ADR-0025 l.10-13 et l.3 ; cartographie §1 ; G2 du lot A §5 ; `harnais-s2.md` §3 ; `critique.md` K-07 | du 2026-09-24 au 2026-09-29 | multiples | **M** (opérationnel) | oui, en partie (n = 35 982 ; 2 618 ; 17 314 ; 9 261) |
| 10 | Taux de présence par flux ; comptes de fenêtres et heures par strate (attestation D.3 a) | 2026-09-29 | orchestrateur | **M** | non |
| 11 | Validateur du cp-1 : `campagne.md` l.204-216 et cartographie l.51 (CP1 §2, l.23) | 2026-09-29 | validateur `claude-fable-5-1` | **M** | non |
| 12 | Exploitation de la campagne : `F:\shogen-campagne\` REPAIR-*, INCIDENT-2026-09-26, CLOTURE-2026-09-28, watchdog (`J0-STATUS.txt`, comptes bruts de `window_close`) | du 2026-08-26 au 2026-09-28 | orchestrateurs MONARK et Shōgen | **M** présumé : contenu non inventorié par le rédacteur (non lu, D.2) | non |
| 13 | Rédacteur de cette révision : la commande de mission (deux taux marginaux d'une source) et la sortie tronquée d'un `grep` sur ADR-0025 l.14 (D.3 f) | 2026-09-29 | rédacteur `claude-opus-5-5` | **M** | non |
| 14 | Worker G1 du lot B (vague 2, `wf_1c82774a-d5f`) : `git show cf696bd:docs/adr-0025/ADR-0025-periode-doublee-S2.md \| head -c 6000`, ADR-0025 affichée en entier, **l.14 comprise** (sha `0fe88f1a…b71f`), avant la lecture de D.2 ; déclarée E-2 au journal G1 `docs/G1-lot-B-sensibilite.md` l.14 ; mécanisme : la commande disait « Lis ADR-0025 déc. 4 » sans la procédure de D.2 n° 6 (C-8 de la revue G2 de B) | 2026-09-30 07:48-07:51Z | worker G1 `claude-opus-5-5` du lot B | **M** (même ligne que n° 5 et n° 13) | non |
| 15 | *Ajout daté du 2026-10-02 14:30 UTC (SHOGEN-EXPOSITION-ORCH-CLOUD-1)* : orchestrateur de la session cloud, cartographie du 2026-09-29 affichée en entier par `cat`, **l.51 comprise**, avant l'application de la lecture gardée de D.2 pt 5 (JOURNAL, entrée de 05:56 UTC) ; ADR-0025 l.14 non affichée | 2026-10-02 ≈ 02:47Z | orchestrateur de la session cloud (`claude-opus-5-5`) | **M** (même contenu que la lecture 4) | non |

Seules les lectures 1 et 2 sont de classe **R**. Lecture 14 (2026-09-30, C-8 de la revue G2 du lot B) : l'instance G1 du lot B n'occupe aucun rôle frais du paquet (rédacteur ou validateur, D2 et D.2) ; le contrôle FM-1.1 de sa transcription (chemins D.2 dans ses appels d'outils) est un acte de l'orchestrateur, joint au contrôle FM-1.1 du cp-1 complet du PAQUET ; toute commande qui dit « Lis ADR-0025 » porte désormais la procédure de D.2 n° 6 (repérer l.14 par son sha256 `0fe88f1a…` avant toute lecture). La lecture 1 a été faite par un worker G1, qui n'a pas repris les chiffres ; aucun décideur de cette ADR n'est connu pour l'avoir vue (D.3). Pour la lecture 2, le lecteur n'est pas établi (item MONARK).

## D.2 Pièces interdites aux rédacteurs et validateurs frais du paquet (C-7 ; liste fermée)

1. `F:\tmp\shogen-j28\work\` en entier, dont `baseline_step0.out` et `campagne-copie\`.
2. `F:\Monark\docs\measure-M009a.md` ; par précaution, `F:\Monark\docs\G1-lot-m009.md` et `G2-lot-m009.md` (lot qui a produit et revu M009a ; contenu non vérifié par le rédacteur) ; la décision D6 de `F:\Monark\docs\adr\ADR-M002-phase1-moteurs-hikae-ukemi.md` (l.185, l.193 selon `critique.md` K-31).
3. `F:\tmp\shogen-carto-2026-09-29\campagne.md` et le dossier `campagne\` (scripts, caches `cache_*.json`, sorties).
4. `F:\tmp\shogen-carto-2026-09-29\_result.json` et `_workflow-output.json`.
5. Cartographie **l.51**, dans ses deux copies : `docs/rapports/cartographie-2026-09-29.md` (à `3d8c185`) et `F:\tmp\shogen-carto-2026-09-29\CARTOGRAPHIE-2026-09-29.md`. La ligne est identifiée par son sha256, `5cc89b563f73d213e38021165a360c3bf2e297e36be467786a007021c71db358`. Le reste du fichier se lit par plages (l.1-50 et l.52-fin).
6. **ADR-0025 l.14** à `7f8b5cc` (ajout de cette révision). La ligne est identifiée par son sha256, `0fe88f1a3810244ecce91b31c1f4e2117f397a7c65d381a75afdbf0b9954b71f` : un errata posé en tête (§8 de l'ADR) déplacera son numéro, pas son contenu. Avant toute lecture, repérer le numéro courant de la ligne par ce sha, sans l'afficher (même geste que pour la cartographie l.51). Le reste d'ADR-0025 est nécessaire : lecture de toutes les autres lignes.
7. Les journaux scellés `F:\shogen-campagne\campagne\*.jsonl` et toute copie (`F:\tmp\shogen-g2-lotA\work\campagne-copie\`, copies G1). Seuls leurs sha256 sont admis, contre `SHA256SUMS-cloture-2026-09-28.txt`.
8. Par précaution, les autres fichiers de `F:\shogen-campagne\` (REPAIR-*, INCIDENT-*, CLOTURE-*, `J0-STATUS.txt`, `LISEZ-MOI.txt`), non inventoriés, sauf `SHA256SUMS-cloture-2026-09-28.txt`. Même précaution pour les rattachements d'ADR-0025 non lus par le rédacteur : `F:\PRODUITS\etude-2026-09-25-pocket\chercheurs\shogen-interne\ARCHIVE-shogen-interne.md` §10.2, §15.1, §15.2, et `F:\PRODUITS\etude-2026-09-25-pocket\AVIS-advisor-2026-09-26.md`.
9. Toute commande de mission ou transcription de session de l'orchestrateur Shōgen du 2026-09-29 qui porte les valeurs masquées en D.3 a.
10. *Ajout daté du 2026-10-02 14:30 UTC (SHOGEN-E1-D2-COMPLETUDE-1)* : le registre PAROXYSME hors dépôt `F:\PRODUITS\paroxysme-2026-09-27\PAROXYSME-Shogen.md` (sha256 de préfixe `a655c401…`, cartographie du 2026-09-29 §0 ; sha complet sur le poste local), qui porte deux taux marginaux (constat K-2 du G0 du lot E1, JOURNAL `e263bc7`). Motif du contrôle FM-1.1 : nom de fichier `PAROXYSME-Shogen.md`.
11. *Ajout daté du 2026-10-02 14:30 UTC (SHOGEN-EXPOSITION-ORCH-CLOUD-1)* : la transcription de la session cloud de l'orchestrateur du 2026-10-02 (session `session_013dvmubgZfL1zNfWnTTzBmw`), qui porte la cartographie l.51 ; aucun brief de rédacteur ou de validateur frais n'en recopie un extrait.

Ne sont **pas** interdits : ADR-0028 et ses annexes (écrites sans taux par source), les trois AVIS de ce dossier, le cp-1, `critique.md`, `harnais-s2.md`, `git-ci.md`, `dettes-paroxysme.md`, `monark.md`, la CONSULTATION, la revue G2 du lot A.

## D.3 Attestations d'exposition (C-6)

**(a) Auteur d'ADR-0028 — orchestrateur Shōgen, `claude-fable-5-1`** (texte dicté au rédacteur, inséré tel quel **sauf la parenthèse chiffrée, masquée**, voir la note) :

> « L'orchestrateur a été exposé, dans cette session, aux éléments suivants :
> - taux marginaux de panne par source, via la dimension campagne de la cartographie (dont binance [deux valeurs masquées par le rédacteur : taux marginaux de panne d'une source, hors plage et dans la plage ; texte intégral détenu par l'orchestrateur]) et le résumé de la cartographie ;
> - taux de présence par flux ;
> - comptes de fenêtres et heures par strate.
> Il n'a vu aucun z, aucun K, aucun P̂_more ni aucun φ. Il n'a ouvert ni baseline_step0.out ni measure-M009a.md. »

*Note du rédacteur* : si les deux valeurs étaient reproduites ici, ADR-0028 porterait un taux par source. Il faudrait alors l'inscrire elle-même en D.2, ce qui la rendrait illisible pour les rédacteurs frais du paquet qui doivent l'appliquer. Consultation CONS-1 tranchée par l'orchestrateur le 2026-09-29 : option (i), masquage maintenu (ADR §4.12).

**(b) advisor-defi** — `AVIS-advisor-defi-2026-09-29.md` (sha256 `fac21173…`), l.7, recopié :

> « **Interdit respecté.** Je n'ai calculé ni lu aucun z, K, P̂ ou φ. Je n'ai pas ouvert `baseline_step0.out` ni `measure-M009a.md`. Sur les journaux scellés, j'ai seulement lu et compté, avec `python -B`. Chaque commande est listée en fin d'avis. »

Complément de l'avis : section « Mesures effectuées (lecture seule, `python -B`, aucun z, K, P̂ ou φ calculé) », l.136-143.

*Faits vérifiables ajoutés par le rédacteur* : l'avis cite « ADR-0025 l.12 » (l.121), c'est-à-dire l'actuelle l.14, qui porte un taux marginal d'une source (D.1 n° 5). Il a compté la présence de lectures `ok` par flux et par strate (D.1 n° 7). Il ne dit pas s'il a lu `campagne.md`, que la CONSULTATION (l.5) prescrivait (SHOGEN-ATTEST-ADVISOR-1).

**(c) advisor** — `AVIS-advisor-2026-09-29.md` (sha256 `87e04420…`), l.7-16, recopié :

> « **Ce que j'ai lu :** la consultation ; CARTOGRAPHIE (en entier), critique.md (en entier), git-ci.md (en entier) ; monark.md §3-§7, harnais-s2.md §7-§10 ; dans le dépôt : `s2-harness/README.md:1-8`, `docs/DECISIONS.md:2960-3029` (D6/D8), `docs/DEVOPS.md:15-39`, `docs/16…md` (lignes 4 et 34, par grep), `docs/15…md` (ligne 10) ; corpus : `02-referentiel-gates-et-regles.md:108-114` (R-19, R-20, R-22, R-25). » (liste mise en ligne par le rédacteur)
>
> « Je n'ai ouvert aucune donnée de campagne. »

*Écart constaté par le rédacteur* : la déclaration n'énonce pas « aucune statistique de résultat (z, K, P̂_more, φ) vue », forme que demande C-6. De plus, « CARTOGRAPHIE (en entier) » comprend la l.51 (D.1 n° 4). La cartographie ne porte, par ailleurs, ni z, ni K, ni P̂_more, ni φ. Le rédacteur l'a lue hors l.51 ; la l.51 relève des marginales selon le cp-1 (CP1 l.23). Demande formée : SHOGEN-ATTEST-ADVISOR-1 (une ligne, canal 2, avant scellement).

**(d) advisor-marché** — `AVIS-advisor-marche-2026-09-29.md` (sha256 `592258d3…`), l.131, recopié :

> « Aucune statistique S2 n'a été lue ni calculée. »

Pièces lues déclarées (l.122-129) : CONSULTATION, `monark.md` §0-§12, 07-gtm, 02-vision, doc 15 §6, DECISIONS l.2910-3143, memstack. La CONSULTATION porte les comptes de Pyth (D.1 n° 7).

**(e) Validateur du cp-1** — `CP1-ADR-0028.md` (sha256 `a2d5bafb…`), l.23, recopié :

> « Exposition déclarée du validateur : pour établir l'inventaire des lectures intermédiaires, j'ai lu campagne.md l.204-216 (taux de panne marginaux par source, hors et dans la plage) et cartographie-2026-09-29.md l.51 (commité). Ce sont des composantes marginales de P̂, pas z, K, P̂_more ni φ ; je ne les reproduis pas ici. Aucune statistique S2 calculée ; baseline_step0.out et measure-M009a.md non ouverts (sha seul). »

**(f) Rédacteur de cette révision** — `claude-opus-5-5`, 2026-09-29 :
- **Pièces lues** :
  - cp-1 ; ADR-0028 dans sa version soumise au cp-1 ; les trois AVIS ;
  - cartographie (l.1-50 et l.52-112) ; `critique.md` ; `harnais-s2.md` ; `dettes-paroxysme.md` ; `git-ci.md` ; `monark.md` (l.126 et l.204, par grep) ; CONSULTATION ; TRANSMISSION-MONARK ; FAITS-PXP-30 ; revue G2 du lot A ; clés du schéma de `oracle-G2-substitution.json` ;
  - ADR-0022 (l.1-8, l.46-62, l.74-80) ; ADR-0023 ; ADR-0024 ; ADR-0025 (l.1-13 et l.15-44) ;
  - DECISIONS (l.1-30, l.305-316, l.1294-1332, l.1880-1910, l.2126-2134, l.2968-2980, l.3098-3110, l.3296-3305) ;
  - doc 10 (l.24-40, l.370-400, l.480-540, l.560-580) ; 05-roadmap (l.108-132) ; RUNBOOK (l.128-146) ; README de `s2-harness` (l.1-12) ; `gates.yml` ; JOURNAL (l.84-92) ; CLAUDE.md du dépôt (l.30-34) ;
  - CHANTIERS MONARK (l.1958, l.1959, l.1971, après un filtrage préalable de tout chiffre statistique) ;
  - `validateur-humain.md` (l.161-175) ; corpus doc 02 (l.111, l.114) et doc 06 (l.82, l.269-275) ;
  - `xtask/src/sg4.rs`, `sg5.rs`, `documents.rs` (en partie) ; `tests/test_exclusion.py` (par grep) ;
  - transparents Agresti 2016 (l.1-6, l.845-852, l.900-921, l.6755-6768, et les renvois « CDA » par grep) ;
  - arXiv:2503.13657v3 (passages de l'annexe A et de l'annexe N.9) ;
  - `docs/G1-lot-adr0025-filtre.md` (l.17-22) ; lignes 13 à 37 du JOURNAL, vues tronquées par une recherche de pourcentages (entrées d'août : phases S2.5 et S3) ; liste des fichiers de `s2-harness/tests/` ;
  - noms de fichiers seulement, contenu non ouvert : dossiers `F:\tmp\shogen-carto-2026-09-29\campagne\`, `F:\tmp\shogen-j28\`, `F:\tmp\shogen-g2-lotA\work\`, `F:\Monark\docs\` et `docs\adr\` (filtre m009/M002) ; comptes de lignes des blobs `adb2213:enforcement/*.sh` et du hook `pre-commit`.
- **Exposé à** :
  - la commande de mission de l'orchestrateur, qui porte deux taux marginaux de panne d'une source (hors et dans la plage) ;
  - la sortie tronquée à 220 caractères d'un `grep` sur ADR-0025 l.14 : deux taux marginaux de pannes de transport d'une source ;
  - les comptes de Pyth (ADR-0023 l.11, D1) ;
  - les diagnostics `resolve_failed` (D5, AVIS-advisor-defi) ;
  - les comptes de fenêtres et heures par strate (ADR-0024, ADR-0025, cartographie §1, G2 du lot A, `harnais-s2.md`) ;
  - les seuils τ de calibration par classe (ADR-0022 l.23-27), antérieurs à la campagne.
- Aucune de ces valeurs de taux n'est reproduite dans ADR-0028 ou ses annexes.
- **Non ouverts** : `baseline_step0.out`, `measure-M009a.md`, `campagne.md`, le dossier `campagne\`, `_result.json`, `_workflow-output.json`, `F:\tmp\shogen-j28\work\`, les journaux de campagne et leurs copies, ADR-M002. La l.51 de la cartographie n'a pas été affichée (seul son sha256 a été calculé).
- **Aucune statistique calculée. Aucun z, aucun K, aucun P̂_more, aucun φ vu.**

**(g) Rédacteur frais du paquet** — *ajout daté du 2026-10-02 17:1x UTC (les lignes qui précèdent sont inchangées)* : `shogen-worker`, Gate 0 `claude-opus-5-5`, rédaction de 16:06 à 16:42 UTC, corrections C-1..C-5 (16:43-16:48) et C-6, C-7 (17:06-17:14) ; journal `docs/G1-partie-3-R.md`, §1 et §10-11, recopié :

> « Je n'ai vu aucun z, aucun K, aucun P̂_more, aucun φ de campagne, et je n'en ai calculé aucun. Je n'ai lu aucun taux d'écart ni de panne d'une source de la campagne. Je n'ai ouvert aucune pièce de la liste fermée D.2 (points 1 à 11) »

Exposé à (déclaré) : comptes de classe M que porte l'ADR (D1, D5, fenêtres), annexe B l.38 (compte de fenêtres sautées), annexe D l.159, noms des pièces de D.2, résultats synthétiques, JOURNAL l.125 seule. Contrôle FM-1.1 de l'orchestrateur (annexe B.32 et B.33) : 0 fragment des lignes interdites dans sa transcription.

**(h) Validateur frais du paquet (cp-1 complet, puis cp-1 bref)** — *même ajout daté* : `shogen-validateur`, Gate 0 `claude-fable-5-1`, de 16:52 à 17:03 UTC et de 17:15 à 17:17 UTC ; rapport `docs/adr-0028/CP1-PAQUET-2026-10-02.md`, §1 et §7, recopié :

> « Je n'ai vu aucun z, aucun K, aucun P̂_more ni aucun φ de campagne, et n'en ai calculé aucun ; aucun taux d'une source réelle. Je n'ai ouvert aucune pièce de D.2 (points 1 à 11) »

Exposé à (déclaré) : comptes de classe M portés par l'ADR et ses annexes, noms des pièces de D.2, D.3 (a) masquée, JOURNAL l.125 seule, résultats synthétiques, sujets de commits. Contrôle FM-1.1 de l'orchestrateur (annexe B.33) : 0 fragment des lignes interdites dans sa transcription.

## D.4 Définitions de contrôle

**(a) « Fixtures seulement » (C-11) — option retenue : lectures « comptes seulement » admises nommément ; proposition du rédacteur, RATIFIÉE par l'orchestrateur le 2026-09-30 sous la délégation investisseur du même jour (JOURNAL), C-8 du cp-1 bref de B-SEG-1 et C-4 de son G2 ; ratification révocable par l'investisseur avant l'exécution unique.**
- Pendant les G1/G2 des lots B0, B-SEG-1, B-SEG-2, B, POOLEE, B-DEP-1 (ajout du 2026-10-01, revue G2 de B-DEP-1 §10), B-DEP-2 (ajout du 2026-10-02, revue G2 de B-DEP-2 §10), CRITERE (ajout du 2026-10-02, liste des actes de la correction de CRITERE §5), D5-AMEND (ajout du 2026-10-02, journal G1 de D5-AMEND §8), DOCS-S2-b (ajout du 2026-10-02, relecture G2 de la partie 2, C-10), RENDU-1 et RENDU-2, `SHOGEN_S2_CAMPAGNE_CONTROL` n'est posée que pour les tests nommés ci-dessous. Tout autre test qui lirait une copie scellée lève `SkipTest`.
- Tests admis nommément. Ce sont des comptes seulement : aucun statut, aucun prix en sortie.
  1. `tests/test_exclusion.py`, `test_ii_plage_adr0025_retire_2618_fenetres` : marqueurs `window_close` de `control.jsonl`, comptes par strate (oracle d'ADR-0025 déc. 2).
  2. Le test de comptes par type du lot B-SEG-1 : enregistrements de la plage comptés par type, lus sur les champs d'horodatage (`window_start`, `ts`, `harness_ts`) et de type seulement, jamais sur un champ de statut. Nom fixé au G0 de B-SEG-1 (2026-09-30) : `tests/test_exclusion.py::TestExclusionJournalReel::test_ii_plage_adr0025_comptes_par_type`. Exécuté par l'orchestrateur seul, sur copie, jamais par un G1/G2.
- Tout autre accès aux journaux réels pendant un G1 ou un G2 est interdit, y compris par un script de mesure du réviseur. Les comptes de paires doublées du G2 du lot A (compte seul) sont le précédent : admis a posteriori, soumis désormais à cette liste.
- L'enregistrement d'oracle (D6 viii) liste les tests lancés avec la variable.

**(b) « Un seul rendu » (C-12).**
- C'est une exécution unique, par l'orchestrateur, du script scellé des lots RENDU-1 et RENDU-2, dont le sha256 est écrit au paquet. Elle est consignée au JOURNAL (heure, sha de chaque sortie).
- Elle produit, dans cet ordre : J14 principal (D4) ; J14 second (coupe de 270) ; J28 (D2 pt 6) ; chaque sensibilité de la liste fermée (D2 pt 7) ; l'oracle tiers `recompute_*` sur chaque sortie ; l'enregistrement d'oracle (D6 viii), avec le sha de chaque sortie.
- **Fail-closed** : sortie ≠ 0 et aucune sortie écrite, si l'une des conditions suivantes est vraie.
  - (1) Le sha256 du paquet ne figure pas dans `JOURNAL.md` à HEAD.
  - (2) Le code d'analyse diffère de celui du paquet : `git diff --quiet <commit d'analyse final écrit au paquet> HEAD -- s2-harness/shogen_s2 s2-harness/tools` est faux, ou l'arbre de travail est modifié sur ces chemins.
  - (3) Le sha256 d'un journal scellé diffère de `SHA256SUMS-cloture-2026-09-28.txt`.
  - (4) Le sha256 du script diffère de celui du paquet. C'est une garde contre une édition accidentelle, pas une preuve.
  - (5) *Ajoutée le 2026-09-30 (A-7 ; CV2-29)* : la garde « T_now ≥ genTime + 24 h » est fausse. genTime est lu dans le jeton RFC 3161 du manifeste `PAQUET.sha256` (`openssl ts -reply -in paquet.tsr -text`), jamais dans un README ; sans ancre, l'heure du commit JOURNAL qui épingle le go « exécuter sans ancre » (condition (6), voie b) en tient lieu (limite déclarée : horloge du client ; C-1 du cp-1 de l'amendement, qui remplace « l'heure du commit JOURNAL du scellement »). La garde lit l'horloge locale : c'est une garde contre l'erreur, pas une preuve, comme (4). Elle n'ouvre jamais l'exécution seule : (6).
  - (6) *Ajoutée le 2026-09-30 (C-1 du cp-1 de l'amendement ; CA-2, CA-9)* : aucun acte de l'investisseur n'est constaté. L'exécution ne s'ouvre que sur l'une des deux preuves suivantes : (a) un jeton `paquet.tsr` sur `PAQUET.sha256` pour lequel `openssl ts -verify` (commande de FAITS-ancre-sceau §2 ; `cacert.pem` et `tsa.crt` aux SHA256 de D.4 c) sort 0 ; (b) un fichier de go de l'investisseur, daté, qui porte « exécuter sans ancre », et dont le sha256 figure dans `JOURNAL.md` à HEAD, sur une ligne postérieure à celle du scellement. Le repli « horloge du client » de (5) n'ouvre jamais l'exécution seul. Chemin et format du fichier de go : fixés au G0 du lot RENDU-1. Test : la fixture « ni jeton vérifié ni go épinglé » donne une sortie ≠ 0 et aucune sortie écrite (annexe A, RENDU-1 : chaque garde, avec son mutant). C'est une garde contre l'ouverture par l'horloge seule, pas une preuve d'identité de l'auteur du go (texte verbatim de l'investisseur, versé par l'orchestrateur).
- Une seconde exécution est une déviation déclarée : motif, puis sorties des deux exécutions conservées.
- Les G1/G2 des lots RENDU se font sur fixtures (a).

**(c) Sceau du paquet (C-13).**
- **Limite déclarée aujourd'hui : « sceau privé ».** Le sha du paquet n'est attesté que par le dépôt privé (commit signé SSH, main protégée) et par le bundle hors ligne. Un tiers ne peut pas vérifier que le sceau précède le rendu.
- Item de recherche PAROXYSME **SHOGEN-SCEAU-ANCRE-1** : trouver la construction qui donne un horodatage externe vérifiable du sha, avec son prix exact. Candidats à instruire, sans rien affirmer ici de leurs conditions :
  - un jeton d'horodatage RFC 3161 d'une autorité tierce ;
  - la publication du seul sha dans un dépôt public (par exemple MONARK) ;
  - OpenTimestamps.
- ADR-0006 pt 3 réserve l'ancrage d'un engagement au mainteneur « dès l'existence du benchmark public (S2) » (DECISIONS l.311-314) ; son pt 4 borne toute présence sur la chaîne à un engagement (l.315-316). L'ancre du paquet est le premier cas d'espèce.
- L'acte d'ancrage appartient à l'investisseur (§4.10 b). Sans ancre au scellement, la limite « sceau privé » est écrite au paquet et au rapport.
- **Amendement daté du 2026-09-30 (A-7, A-9 ; CV2-27 à CV2-33)** : recherche SHOGEN-SCEAU-ANCRE-1 rendue (FAITS-ancre-sceau, `926ed9fe…`, lecture sur place par l'orchestrateur).
  - *Objet horodaté* : le manifeste `PAQUET.sha256`, pas le paquet (CV2-33). Ses octets sont figés : UTF-8 sans BOM, fins de ligne LF, format `sha256sum`, attribut `-text` dans `.gitattributes`. Les deux sha (paquet et manifeste) sont écrits au JOURNAL.
  - *Ancre (1), condition d'exécution* (ou, sans ancre, le go écrit de l'investisseur « exécuter sans ancre » : D.4 b, condition (6), C-1 du cp-1 de l'amendement) : jeton RFC 3161 de FreeTSA, immédiat, gratuit, sans compte (FAITS §2). Vérifiable par quiconque fait confiance à l'autorité FreeTSA (cacert.pem SHA256 `2151b611…`, tsa.crt SHA256 `8bfb0305…`, FAITS §2), par `openssl ts -verify` (OpenSSL 3.5.7 présent sur l'hôte). Pérennité déclarée : opérateur individuel, aucun accord de niveau de service lu (CV2-32). DigiCert : second jeton optionnel.
  - *Ancre (2), complément de durabilité, hors des conditions d'exécution* : OpenTimestamps. Vérifiable sous confiance en la chaîne Bitcoin (nœud) ; avant `ots upgrade`, sous confiance en les calendriers (CV2-30, CV2-31). Le client est une dépendance nouvelle (R-8), installée sur go seulement (CV2-32).
  - *Ce que l'ancre n'atteste pas* : elle atteste l'existence des octets au plus tard à genTime, rien de plus ; rien sur des lectures antérieures des données (D.1, D.3) (CV2-31).
  - *Ordre* (C-1 du cp-1 de l'amendement) : avec ancre, go de l'investisseur → jeton (1) → délai de 24 h → exécution unique ; sans ancre, go écrit de l'investisseur « exécuter sans ancre » → délai de 24 h → exécution unique. (2) peut compléter après. L'horloge seule n'ouvre jamais l'exécution (D.4 b, condition (6)).
  - *Délai de rétractation (A-7)* : 24 h à compter du genTime du jeton (1) ; sans ancre, à compter de l'heure du commit JOURNAL qui épingle le go « exécuter sans ancre », postérieur au scellement (limite déclarée : horloge du client ; C-1 du cp-1 de l'amendement : l'heure du commit du scellement ne sert plus de point de départ). Choix de conception, fixé par l'orchestrateur sous délégation, révisable par l'investisseur ; recherche P-14 formée, non bloquante, première source P-10 (C-8 du cp-1 de l'amendement, annexe B.6) ; gardes (5) et (6) de D.4 b.
  - *Hors des octets scellés (CV2-27)* : un fichier ne porte pas son propre sha, et genTime n'existe qu'après l'acte. `docs/adr-0028/sceau/README.md` porte le sha du paquet, le sha du manifeste, genTime, l'échéance du délai et l'état de chaque ancre ; le paquet ne porte que les conditions.
  - *Préparé sans acte par l'orchestrateur* (lot PAQUET) : `paquet.tsq` (requête locale), `docs/adr-0028/sceau/README.md`, `scripts/sceau/verify.sh`, la ligne JOURNAL type. L'envoi du `.tsq`, `ots stamp` et le téléchargement de `cacert.pem` et `tsa.crt` sont des actes de l'investisseur (§4.10 b), après la lecture sur place des conditions d'usage (P-12).
  - *Routage* : investisseur (§4.10 b) et mainteneur (ADR-0006 pt 3) ; c'est la même personne, informée des deux titres.
  - **SOUS ESCALADE — en attente de l'investisseur** (cp-1 de l'amendement, ADR §1 bis.8). *Veto (A-8, CV2-28)* : un veto entre le scellement et l'exécution invalide le sceau (nouveau paquet, nouveau sha, nouvelle ancre, délai recommencé ; le premier sha reste cité).
  - *Ajout daté du 2026-10-02 (les lignes qui précèdent sont inchangées)* : l'escalade ci-dessus est **tranchée** : réponses de l'investisseur du 2026-09-30 23:33 UTC (JOURNAL) : « Oui » et, au veto, « Ok pour les quatre » (A-8 confirmé) ; voir l'erratum de statut d'ADR-0028 du 2026-10-02.
  - Sans l'ancre (1), la limite « sceau privé » reste écrite au paquet et au rapport.

## D.5 Traitements pré-enregistrés des items d'analyse ouverts (C-10 v) — proposés, à ratifier au paquet

| item | traitement | motif | sortie au rapport |
|---|---|---|---|
| SHOGEN-TAU-REDERIV-1 | descriptif seulement | τ committé (`sigma-tau.json`, identique dans les 4 093 `run_params`, `harnais-s2.md` P-6) pour tous les confirmatoires ; ADR-0022 pt 3 : « divergence = trouvaille, pas re-tune silencieux » | τ observé contre τ projeté, au bloc 3 ; re-dérivation = PX-Shogen-13 (C7), après le rendu |
| SHOGEN-HOST-DEGRADED-1 | descriptif seulement | ajouter une sensibilité après les lectures de D.1 élargirait les chemins d'analyse ; la voie retenue est la déclaration transparente de ce qui était su (principe de l'avis advisor Q2, l.181-183) | comptes au bloc 1 ; libellé à compléter (annexe B) |
| SHOGEN-CENSURE-INFO-1 | descriptif seulement | idem ; la censure informative n'est pas modélisée : limite déclarée, item PAROXYSME | fenêtres sautées par strate, au bloc 1 |
| SHOGEN-DP-JOURNAL-LOSS-1 | descriptif seulement | la plage est déjà exclue (D5) ; dans la sensibilité « plage incluse », les pertes sont déclarées | comptes de pertes, dans la sensibilité « plage incluse » |
| Bloc 6 (ADR-0026) | descriptif seulement | k_eff = nombre de classes de la partition R2 (doc 10 §5.6) ; aucune inférence ; ADR-0026 (G0 proposé) n'exige pas n_eff en S2 | partition nommée et **datée** (HS2-07, lot B), k_eff, k nominal, deux drapeaux ; G10 après J28 |

La liste fermée des sensibilités reste celle de D2 pt 7.

**Amendement daté du 2026-09-30 (A-6 ; AVIS-advisor-defi Q4 ; CV2-24, CV2-25, CV2-26).** Traitements ratifiés par l'orchestrateur sous délégation, révocables par l'investisseur avant l'exécution unique. Tous restent descriptifs, hors décision et sans paramètre ; aucun n'entre dans la règle SHOGEN-CRITERE-R1-1 ni dans la liste fermée des sensibilités (D2 pt 7 amendé). Code : lot D5-AMEND (annexe A). Items : annexe B.6.

| item | traitement ratifié et amendé | sortie au rapport |
|---|---|---|
| SHOGEN-TAU-REDERIV-1 | ratifié ; τ observé défini d'avance : P99 et maximum de \|v_i − m_−i\|/m_−i par classe sur le segment, sans aucune ré-estimation | bloc 3, à côté de τ_classe ; PX-Shogen-13 après le rendu |
| SHOGEN-HOST-DEGRADED-1 | ratifié ; libellé complété par l'orchestrateur avant le scellement, en mécanisme et comptes (M-5 de la critique v1) ; K_s décomposé par nombre de lectures `panne_transport` de la fenêtre (≥ 2, 1, 0) et K[tous les écarts hors_enveloppe] ; c_s = fenêtres où toutes les lectures du pool de la strate sont `panne_transport`. Le z confirmatoire inclut les modes communs de l'observateur (hôte, DNS, réseau) | bloc 3 ; SHOGEN-HOST-DEGRADED-2 après l'exécution |
| SHOGEN-CENSURE-INFO-1 | ratifié ; pertes par cause et par strate (limite d'exécution de tâche ; boucles NUL ; fenêtres sautées, harnais vivant), hypothèse déclarée H_perte : les pertes d'outillage sont non informatives (registre 08 : **A(loss-non-informative)**, entrée du 2026-09-30, C-3 du cp-1 de l'amendement). Bornes à P̂ = P̂_more fixé, s = fenêtres sautées de la strate : z_bas = (K − (n+s)·P̂)/√((n+s)·P̂(1−P̂)), z_haut = (K + s − (n+s)·P̂)/√((n+s)·P̂(1−P̂)), puis avec σ̂_bloc,s au dénominateur ; **étiquetées « non extérieures »**, sans lecture d'identification (CV2-24 : imputer un écart par fenêtre censurée élève P̂_more, la borne basse n'est pas extérieure). Le verdict n'est pas identifié sous censure arbitraire des fenêtres sautées (CV2-26) | blocs 1 et 3 ; bornes extérieures : SHOGEN-CENSURE-INFO-2 après l'exécution |
| SHOGEN-DP-JOURNAL-LOSS-1 | ratifié ; comptes de pertes par type d'enregistrement dans la sensibilité « plage incluse », étiquetée « biaisée vers le haut par construction ; documente l'exclusion D5 ; pas un estimateur alternatif » | sensibilité « plage incluse » |
| Bloc 6 (ADR-0026) | ratifié ; partition nommée et datée, k_eff, k nominal du segment (hôtes, `r2.py:783`) et k nominal_s par strate (D1 cas b), avec « comparaison hétérogène déclarée » s'ils diffèrent ; drapeau 1 ; drapeau 2 aligné sur la règle (ADR §1 bis.1 pt 10), strate poolée hors de ses entrées | bloc 6 |
| E-D1b (D1 cas b) | ratifié (CB-8, 2026-09-29) ; limite déclarée, sans règle ajoutée : un flux presque mort (lectures `ok` rares) reste au pool et pousse z vers le bas par absorption ; toute règle à seuil serait un chemin d'analyse. Item PAROXYSME de cette limite : **SHOGEN-FLUX-QUASI-MORT-1** (annexe B.6 ; C-4 du cp-1 de l'amendement), sensibilité après l'exécution unique, étiquetée « ajoutée après le pré-enregistrement » | bloc 1 (retraits nommés, avec leurs comptes) |
