# Adjudication — lot INTEGRATION-P2 (orchestrateur, 2026-10-16 05:51:08 UTC, `date -u`)

## Contrôles
- Intégrateur : 366 champs `model` tous `claude-opus-5-5` ; FM-1.1 = 0 ; SHA256SUMS 97 OK ; 24 diffs lus (cibles : avant_acte.py, garde_commun.py, crochet, acte_shell.py, tests, skills, garde/, fm11.py, SHA256SUMS des contrôles ; aucun hunk sur le README ni sur la ligne du plancher : les deux diffs qui nomment ces fichiers ne le font qu'en contenu, D3) ; `planchers.tsv` : 48 tests, ordre C (INT-01..07), B (08..16), A (17..24).

## Décisions
1. **`readme/C-table.diff` adopté avec INT-01** (l.11 de la table du README, empreinte de `fm11.py` ; aucun renvoi par numéro ne la vise : relevé de la G2 de C).
2. Point bloquant `cibles` : résolu par recalage de P2A-4 sur `fc["ecrit"]` avec un test de non-régression (INT-20) : à rejouer par le contre-contrôle sur le crochet réel.
3. Règle « brief » du groupe A renumérotée R11 ; appel après R4, avant R9 (conflit de sens non relevé par les G2, trouvé et fermé par l'intégrateur).
4. **Contre-contrôle neuf** lancé (`cc/BRIEF-CC.md`) ; puis chaîne (24 commits + README par groupe, plancher = tête + n) ; clôture CONFORME sans passe 3 si les réserves sont des formes écrites et éprouvées.
5. Écarts E-1 à E-3 de l'intégrateur admis.

## Ajout daté du 2026-10-16 07:17:21 UTC (`date -u`) : adjudication du contre-contrôle neuf (CONFORME-AVEC-RÉSERVES, R-1 à R-3)

Contrôles : 304 champs `model` tous `claude-opus-5-5` ; FM-1.1 = 0 ; SHA256SUMS 222 OK. Série saine : 24 pas verts (Ran 127 → 174), fidélité aux sources vérifiée (seuls les écarts déclarés), point `cibles` prouvé sur le crochet réel (cinq interdites refusées, cinq permises passent ; avec `cibles` remis : tout passe sans contrôle), décisions des adjudications rejouées, D3/D4 par groupe en 0, matrice 3.11-3.13, 34 mutants (32 tués, CC-07 non équivalent → R-3, CC-22 équivalent admis).
- **R-1 à R-3 adoptées** : R-1 (paragraphe des cas par règle, README A) et R-2 (relevé du registre à la tête, README C) appliquées aux textes du lot ; R-3 (cas TMPDIR sous un interdit) devient le pas INT-25.
- **Limite** : D3 refuse un pas isolé aux neuf pas qui précèdent l'ajout README de leur groupe (jugement par groupe) ; item SHOGEN-GARDE-D3-MOT-COMMUN-1 formé au versement ; observations (doublons `OUTILS`/`RACINE`, en-tête du crochet) : forme, au lot suivant.
- **Clôture CONFORME sans passe 3.** Chaîne `chaine_int.sh` (25 commits ; plancher = tête + n ; README C/B/A aux pas 07, 16, 24, datés au pas ; table l.11 avec INT-01), vérifiée à blanc sur la tête `9c04eec` (24 + 2 diffs applicables), armée derrière les quatre versements. Copies jetables du contre-contrôle supprimées (disque).
- Écarts E-1 à E-4 du contre-contrôleur admis (E-3 : suites d'autres jobs lancées sur une copie, arrêtées sans reste).
