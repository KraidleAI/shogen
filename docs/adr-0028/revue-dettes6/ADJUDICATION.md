# Adjudication de l'orchestrateur sur le rapport du générateur de DETTES-T6 (2026-10-10 00:27:20 UTC, `date -u`)

Pièce : `RAPPORT-GENERATEUR.md` (générateur `claude-opus-5-5`, Gate 0 sur le transcript ; FM-1.1 : 0, deux versions de fm11) ; `SHA256SUMS` du dossier : contrôle OK ; série DT6-a à DT6-j, empreinte (concaténation dans l'ordre) `491d0e52…b0b57`. Règle « aucune dette ».

- **Q-1 à Q-7 : recommandations codées adoptées pour la G2** (âge du relevé D-3 en fenêtres ; « invalid » jugé D-3 ; IPv4 littérale canonique relevée directement ; numéro d'AS en chiffres ASCII seuls, écart à S2 écrit au FORMAT §15.4 ; compte d'octets dans le code et phrase au §8.4 ; grille de `status` bornée à 32 jours ; capture D-3 bornée par le délai de 2 s ; règle `env` en commentaire de `gates.yml`). La G2 juge chacune ; Q-5 en particulier au regard de la rétention locale de 7 jours et de la mémoire de `status` par les résumés quotidiens (adjudication de DB-0, point 7).
- **Précisions d'items existants adoptées** (portées à l'annexe B au versement) : SHOGEN-S2BIS-RB3-DEGRADATIONS-1 couvre aussi D-3 ; SHOGEN-S2BIS-CONFIG-PRODUCTION-1 scelle la commande `chronyc -n tracking`.
- **S-G9 ROUGE sur la copie creuse** (`docs/17` l.70 cite un emplacement interdit, absent de la copie) : artefact de copie, admis ; la chaîne de commits de l'orchestrateur rejoue `xtask verify` sur l'arbre complet (VERDICT GLOBAL VERT exigé).
- **Ordre de commit** : DETTES-T5 (DT5-21 porte le plancher s2bis à 342) se commet d'abord ; la série DT6 sera recalée de +1 sur le plancher s2bis (343 → 358 en fin de série) par le générateur avant la chaîne.
- E-0 (effort high demandé par le brief, contre `max` de la fiche) : décision de l'investisseur du 2026-10-08 (« baisse l'effort des agents Opus à high ») : admis, pas un écart. E-1 à E-13 admis ; E-10 (disque à 222 Mio vers 23:17-23:21 UTC) : cause traitée à 23:4x (nettoyage, 8,3 Go libres) ; consigne `df -h /` dans les briefs.
- Suite : G2 neuve à 100 %.

## Ajout daté du 2026-10-10 01:14:58 UTC (`date -u`) : adjudication de la G2 (ACCEPTE-AVEC-CORRECTIONS, C-1 à C-10)
Pièce : `g2/RAPPORT-G2.md` (réviseur neuf `claude-opus-5-5`, Gate 0 sur le transcript ; FM-1.1 : 0, deux versions) ; série relue `491d0e52…` sur `094fa5d`.
- **C-1 à C-10 adoptées** dans la forme de `g2/corrections/G2-corrections.diff` (`2b6d931a…`), appliquée après DT6-j (diffs DT6-k et suivants si R-25 l'exige), avec la date de l'ajout daté du FORMAT reportée (heure `date -u` de la dernière écriture) et une section METRIQUES pour ces corrections.
- **Q-1 à Q-7** : adoptées (Q-5 confirmée par la G2 : grille de 32 jours, rétention de 7 jours, mémoire par les résumés).
- **Précisions d'items** (versées à l'annexe B) : SHOGEN-S2BIS-STATUS-RETENTION-1 : le compte cumulé tiré des résumés ne passe pas par la grille d'`etat` ; SHOGEN-S2BIS-RB3-DEGRADATIONS-1 : le renvoi « §16.2 » de l.1331 se lit « §17.2 » (D-3 compris).
- **Recalage** : la tête porte maintenant DETTES-T5 (DT5-21 : plancher s2bis 342) ; le générateur recale la série DT6 de +1 sur le plancher s2bis à chaque diff, sur la tête du moment, avant le contre-contrôle.
- E-1 à E-7 admis. Suite : générateur (corrections et recalage), puis contre-contrôle neuf.

## Ajout daté du 2026-10-10 02:53:55 UTC (`date -u`) : adjudication de la phase 2 du générateur (corrections C-1 à C-10, recalage +1)
Pièce : `RAPPORT-GENERATEUR.md` §10 (ajout daté de 02:52:05 UTC ; générateur `claude-opus-5-5`, Gate 0 sur le transcript : 1 137 occurrences, toutes `claude-opus-5-5` ; FM-1.1 : `{resultats: 0, entrees: 0}`, deux versions) ; `SHA256SUMS` du dossier (`4b80f081…`, 13 lignes, `sha256sum -c` relu par l'orchestrateur) ; sha256 des onze diffs relus, égaux au rapport.
- **DT6-k** (C-1 à C-10, +49) admis pour le contre-contrôle ; rouges reproduits (C-1, C-2 : FAIL 2 sur DT6-j ; C-5 à C-9 : FAIL 1 chacun) ; 13/13 mutants tués.
- **Recalage +1** admis : planchers s2bis a 344 … k 358 ; diffs identiques sur `ada4737`, `14597a6` et `39718f4` ; série a à k, empreinte `d70806e0a35260a887652c4ca51b2ab999ecaa26521dae0b7107e2974da31006`.
- S-G9 rouge sur copie creuse (`docs/17` l.70) : artefact admis ; VERDICT GLOBAL VERT exigé sur l'arbre complet dans la chaîne. Étape `git grep` de g5 et job g3-secrets non lancés par le générateur (recherche sur tout l'arbre, interdite aux agents) : la chaîne de l'orchestrateur et la CI les portent.
- **Coordination** : le correctif DT5-24 (alerte CodeQL de la PR n° 11) passe le plancher de `controle-unittest` de 36 à 37 dans `gates.yml` ; DT6 ne touche que la ligne du plancher s2bis : contrôle d'application au moment de la chaîne.
- E-14, E-15 admis. Suite : contre-contrôle neuf (`g2/cc/BRIEF-CC.md`).

## Ajout daté du 2026-10-10 03:52:42 UTC (`date -u`) : adjudication du contre-contrôle (CONFORME-AVEC-RÉSERVES, R-1 à R-7)
Pièce : `g2/cc/RAPPORT-CC.md` (`d06bb58f…` ; contre-contrôleur neuf `claude-opus-5-5`, Gate 0 sur le transcript : 412 occurrences ; FM-1.1 : 0, deux versions ; `g2/cc/SHA256SUMS` relu, 73 lignes). Série a à k (`d70806e0…`) conforme sur `ba5ea95` et applicable sur `57330fa` ; C-1 à C-10 dans la forme du réviseur ; recalage exact (Ran = plancher de a à k, 358 en fin) ; 12 phrases de fermeture vraies telles quelles, 4 vraies avec les réserves.
- **R-1 adoptée (défaut de code de DT6-e, de la classe de C-1)** : une `sante` hors FORMAT dont « System time » a 4 301 chiffres fait lever `ValueError` dans `status` et `resume` ; au-delà de `journal.CHIFFRES` chiffres, le relevé est illisible ; test (FAIL 1 avant, vert sous 3.10 à 3.13).
- **R-2 à R-6 adoptées** (tests seuls, chacun tue un mutant vivant non équivalent du contre-contrôleur) ; **R-metriques** adoptée (section METRIQUES DT6-l).
- **R-7 adoptée** (texte) : la phrase de fermeture de SHOGEN-S2BIS-STATUS-QUEUES-1 dit « du rapport local » ; portée au bloc daté de l'annexe B au versement.
- Forme : `g2/cc/propose/R-1.diff` (`6eb57a49…`) à `R-6.diff` et `R-metriques.diff` (`358d0396…`), repris **à l'identique** par le générateur sous les noms DT6-l à DT6-r (dans l'ordre R-1 … R-6, R-metriques), qui les relit et en répond (ils sont de la main du contre-contrôleur) et rejoue leurs rouges ; si l'identité à l'octet est constatée par l'orchestrateur, clôture CONFORME sans passe 2 (précédents : DT4-g, B.91 ; DT5-22 et DT5-23, B.92).
- E-1 à E-6 admis (E-1 : liste non récursive des noms de `docs/adr-0028/` filtrée, aucun nom interdit affiché).

## Ajout daté du 2026-10-10 04:28:30 UTC (`date -u`) : adjudication de la phase 3 (R-1 à R-6, R-metriques)
Pièce : `RAPPORT-GENERATEUR.md` §11 (ajout daté de 04:26:48 UTC ; générateur `claude-opus-5-5` ; FM-1.1 : 0, deux versions) ; `SHA256SUMS` du dossier (`69f2a722…`, 20 lignes, `sha256sum -c` relu).
- **DT6-l à DT6-r identiques à l'octet** aux formes `g2/cc/propose/R-1.diff` … `R-metriques.diff` (`cmp` refait par l'orchestrateur, 7 sur 7) ; le générateur les juge justes un par un ; rouges reproduits (R-1 FAIL 1 sur le code d'avant ; R-2 à R-6 sur leurs mutants) ; vert de la série a à r sur `0e03a9f` et `dda4bbc` (Ran 358, matrice 3.10 à 3.13, `cargo test` à la cible par défaut 269 tests). Aucun autre défaut de la classe de R-1 dans `status` et `resume` (sonde de 783 cas).
- **Avant clôture, trois ajouts (phase 4, « aucune dette »)** :
  - **O-5** : le titre de la section METRIQUES de DT6-r nomme DT6-l seul ; correction d'une ligne en **DT6-s** : « DT6-l à DT6-q ».
  - **O-6** : la borne exacte de R-1 (640 chiffres) n'est figée par aucun test (R1-M4 vivant hors FORMAT). Les deux lignes de `outils/r1m4_essai.py` (vertes sur le code, FAIL sur R1-M4 et R1-M3) deviennent un test, **DT6-t**.
  - **SHOGEN-S2BIS-TEST-SANTE-CHARGE-1** (constat du générateur de DB-1, E-6 : `test_sante` a échoué 1 fois sur 81 passages sous charge ; test existant du collecteur) : reproduire sous charge, trouver la cause, corriger le test ou le code, **DT6-u**. Si la cause n'est pas trouvable, le dire avec les mesures.
  - Ces trois diffs passent ensuite une passe 2 brève du contre-contrôleur du lot.
- **O-7** (un entier de 641 à 4 300 chiffres dans une ligne : verdict selon le réglage de l'interpréteur ; le collecteur n'en écrit jamais) : limite écrite au bloc daté du lot, sans item. **O-8** (34 dossiers temporaires) : déjà l'item SHOGEN-VERIFIER-TESTS-TMP-RESTES-1 (lot DETTES-T7).
- E-16 et E-17 admis.

## Ajout daté du 2026-10-10 05:11:14 UTC (`date -u`) : phase 4 (DT6-s, DT6-t, DT6-u)
Pièce : `RAPPORT-GENERATEUR.md` §12 (05:10:00 UTC) ; `SHA256SUMS` (`fe7bb1ee…`, 23 lignes, relu) ; FM-1.1 : 0. DT6-s (titre METRIQUES), DT6-t (borne exacte de R-1 : R1-M4 et R1-M3 tués ; plancher inchangé 358), DT6-u (`test_sonde_rendue_apres_l_echeance_avant_le_releve_vaut_null` : cause dans le test, qui n'attendait pas la sonde d3 ; 2 ERROR sur 10 000 passages chargés avant, 0 sur 10 000 après ; mutants U01 à U03 de la règle `fin` > E tués) admis pour la passe 2 du contre-contrôleur. Série a à u, empreinte `341f8a3cafb39243233aa0de754a6ee35854120f2e8af2bcf41bef6da226d9d1`. **Écart de l'orchestrateur, déclaré** : mon message de reprise ne nommait pas le test instable (E22 de la liste GARDE-FOUS-ORCH) ; E-18 et E-19 du générateur admis.

## Ajout daté du 2026-10-10 05:46:44 UTC (`date -u`) : contre-contrôle passe 2 (CONFORME-AVEC-RÉSERVES, R-8)
Pièce : `g2/cc/RAPPORT-CC.md` (ajout daté de 05:40:14 UTC ; même contre-contrôleur `claude-opus-5-5` ; FM-1.1 : 0, deux versions ; `g2/cc/SHA256SUMS` 105 lignes, relu). R-1 à R-7 levées (`cmp` refait, 7 sur 7) ; DT6-s, DT6-t, DT6-u justes. DT6-u : cause dans le test confirmée (20 000 passages chargés avant : 130 ERROR ; 10 000 après sous charge plus forte : 0) ; règle `fin` > E toujours vérifiée (mutants V1 à V3 tués).
- **R-8 adoptée** (test seul) : aucun test n'applique la règle `fin` > E à la sonde d3 (mutant V4 vivant avant et après DT6-u ; FORMAT §13.2 la pose pour D-3, D-4 et D-5). Forme : `g2/cc/propose/R-8.diff` (+2) et `R-8-metriques.diff`, reprises à l'identique par le générateur en **DT6-v** et **DT6-w**, qui les relit ; si l'identité est constatée, clôture CONFORME sans passe 3 (précédents : DT4-g, DT5-22 et DT5-23).
- E-7 à E-9 admis.

## Ajout daté du 2026-10-10 05:56:30 UTC (`date -u`) : phase 5 (DT6-v, DT6-w) et clôture
Pièce : `RAPPORT-GENERATEUR.md` §13 (05:55:36 UTC ; générateur `claude-opus-5-5`, Gate 0 sur le transcript : 1 476 occurrences, aucun autre modèle ; FM-1.1 : 0, deux versions) ; `SHA256SUMS` (`6528a47c…`, 25 lignes, `sha256sum -c` relu).
- **DT6-v et DT6-w identiques à l'octet** à `g2/cc/propose/R-8.diff` (`e0a8facb…`) et `R-8-metriques.diff` (`6389788b…`) : `cmp` refait par l'orchestrateur, 2 sur 2. Le générateur les juge justes ; rouge rejoué (V4 vivant sur l'état u, FAIL 1 sur a à w) ; vert de la série a à w sur `04f242d` et `953270e` (runner 137 ok ; job `s2bis` au texte de `gates.yml` : Ran 358 ; matrice 3.10 à 3.13 en `-X dev -W error` : Ran 358, 0 avertissement).
- **Clôture : CONFORME.** Le contrôle de la forme R-8 est celui de la passe 2 du contre-contrôleur, qui l'a écrite et testée ; les diffs commis sont ses octets (précédents DT4-g, DT5-22/23) ; aucune passe 3.
- Précision du générateur sur DT6-v (la limite 0 vaut parce que l'horloge monotone de Linux compte depuis le démarrage ; `min(fins) − 1` ne dépendrait de rien) : sans correction ; écrite au bloc daté du lot comme limite, avec O-7 et R-7.
- E-20 admis (script nommé par la commande de fond avant d'être écrit, écrit avant usage ; aucun résultat touché).
- Série commise : DT6-a à DT6-w (23 diffs), par `chaine_d6.sh`, après la chaîne de DETTES-T14.
