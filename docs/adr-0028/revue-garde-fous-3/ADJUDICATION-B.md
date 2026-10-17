# Adjudication de l'orchestrateur : GARDE-FOUS phase 3, groupe B (crochet GARDE-FAITS)

## Ajout daté du 2026-10-16 15:34:01 UTC (`date -u`)
- **Générateur** (`shogen-worker`, Gate 0 `claude-opus-5-5` : 238 occurrences, aucune autre ; FM-1.1 : 0) : cinq diffs B-1 à B-5 (erreur interne → refus pour les actes qui écrivent ; message humain à contenu chaîne ; règle R12, nombres d'une réponse contre leur pièce ; journal des passages en lecture seule ; disque du dépôt), plancher annoncé 177 → 191, 34 mutants tués.
- **G2 neuve** (`g2/RAPPORT-G2.md` `b3de4362…` ; réviseur distinct, Gate 0 `claude-opus-5-5` : 278 occurrences ; FM-1.1 : 0) : **ACCEPTE-AVEC-CORRECTIONS C-1 à C-5**, liste fermée, diffs byte-exacts `g2/diffs/` (concaténation `d181e070…`). Série rejouée sur la tête `fe9a72b`, Ran = 191 ; 15 mutants du générateur rejoués, tués ; 12 mutants neufs tués sur la copie corrigée.
- **C-1 adoptée** (bloquante) : sous erreur interne, `lecture_pure` laissait passer trois actes qui écrivent ou exécutent (`>&1b`, programme par chemin, `printf -v PATH`) ; cas Stop sous erreur interne ajouté (mutant G-5 vivant).
- **C-2 adoptée** : un refus du crochet relayé dans un message `user` comptait comme texte humain (R5, R6) ; effets de B-2 sur R6 consignés au README ; desserrage `J28` → « 28 jours » admis, E29 tenu par R12.
- **C-3 adoptée** (bloquante) : R12 non jugée quand R6 ou R10 refusait d'abord, et second arrêt qui laissait tout passer (le contournement « deux arrêts »).
- **C-4 adoptée** : faux refus de R12 sur un compte lu par `wc -l` (règle C-6 de R5).
- **C-5 adoptée** : cas qui garde le regard avant de `piece_porte` (mutant G-3 vivant).
- **Décision sur I-6** : R12 juge le texte écrit après le dernier appel d'outil ; le texte d'avant est jugé au tour suivant par le même mécanisme s'il est répété ; admis pour cette phase, item formé (SHOGEN-R12-TEXTE-AVANT-OUTIL-1). I-1 (entrée non objet : Claude Code l'écrit) : admis, pas d'item. I-2 (milliers, faux refus dans le sens sûr) : item formé (SHOGEN-R12-MILLIERS-1). I-3 (notifications du harnais dans la fenêtre) : item formé, mesure par l'orchestrateur seul (SHOGEN-R12-FENETRE-NOTIFICATIONS-1). I-4 : item formé (SHOGEN-R12-PASSAGE-VISIBLE-1). I-5 : la skill `shogen-avant-lancer` dit `df -h /` : à corriger dans l'intégration (ligne du skill vers `avant_acte.py disque --depot`), pas d'item.
- Écarts du réviseur E-1 à E-3 admis (aucune pièce interdite).
- **Suite** : série B-1 à B-5 puis C-1 à C-5 à l'intégrateur de la phase (avec A et C), contre-contrôle neuf de la série, chaîne de commits.
