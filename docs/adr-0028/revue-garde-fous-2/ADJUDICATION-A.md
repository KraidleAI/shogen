# Adjudication — GARDE-FOUS phase 2, groupe A (orchestrateur, 2026-10-16 02:26:29 UTC, `date -u`)

## Contrôles
- Générateur : 403 champs `model` tous `claude-opus-5-5` ; FM-1.1 = 0 ; SHA256SUMS 236 OK ; P2A-1 à P2A-7 lus (fichiers touchés : avant_acte.py, garde_commun.py, crochet, skills, tests, README, gates.yml).
- G2 neuve (réviseur distinct, reprise après le redémarrage du conteneur) : 219 champs `model` tous `claude-opus-5-5` ; FM-1.1 = 0 ; SHA256SUMS 48 OK ; verdict **ACCEPTE-AVEC-CORRECTIONS, C-1 à C-8**.

## Décisions
1. **C-1 à C-8 adoptées telles quelles** (C-1 : « soldé » et « sans objet » ferment un item ; C-2 : règle git dans le brief lui-même, fiche nommée au refus ; C-3, C-4 : formes de B2/B3 ; C-5 : consigne de plus de **1500 caractères** sans `BRIEF*.md` refusée, seuil adopté ; C-6 : compte lu par `grep -c`/`wc -l` admis ; C-7 : faux vert exponentiel du détecteur corrigé ; C-8 : trois mutants tués).
2. **`outils/recaler.py` du générateur écarté** (réintroduirait un défaut corrigé) : le recalage se fait depuis les diffs livrés, par le lot d'intégration.
3. **Intégration des trois groupes** (A, B, C) : un lot INTEGRATION-P2 (worker neuf) : une seule série ordonnée sur la tête, hunks README remplacés par un ajout daté final par groupe (sha256 recalculés, dates croissantes, DATE-PASSEE respectée), planchers recalculés, dépendances croisées résolues (LN-6 refait les cibles de R2 ; LECTURE-SEULE remplace l'index temporaire de `diff` ; crochet Agent/Write) ; tests et mutants rejoués sur l'état final ; puis contre-contrôle neuf ; puis chaîne. Les briefs de l'orchestrateur eux-mêmes devront passer B2 (constat relayé avec fichier:ligne) : règle de brief adoptée.
4. Items : les 9 du rapport G2 formés au versement (dont `faits_et_appels` sur un message humain à contenu chaîne : hors lot, à corriger par le crochet au lot suivant) ; K16 (forme absente des journaux réels) et K19 (équivalent) admis.
5. Écarts E-1 à E-7 admis.
