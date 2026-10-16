# Adjudication — GARDE-FOUS phase 2, groupe B (orchestrateur, 2026-10-16 02:27:05 UTC, `date -u`)

## Contrôles
- Générateur : 325 champs `model` tous `claude-opus-5-5` ; FM-1.1 = 0 ; SHA256SUMS 30 OK ; GFB-1 à GFB-7 (GFB-2t compris) lus.
- G2 neuve (réviseur distinct, reprise après le redémarrage) : 236 champs `model` tous `claude-opus-5-5` ; FM-1.1 = 0 ; SHA256SUMS OK ; verdict **ACCEPTE-AVEC-CORRECTIONS, C-1 à C-8**.

## Décisions
1. **C-2 à C-8 adoptées telles quelles** : C-2 (régressions réelles de LN-6 : `$C`, `eval`, `os.system` en python ; les motifs d'avant jugent aussi ces formes) ; C-3 (boucles `while`/`until` à condition de sortie admises ; boucle sans fin admise seulement avec `break`/`exit`/`return`) ; C-4 (le marqueur de forge porte l'identifiant du run lu dans une preuve du journal de la session ; d'une autre session, invérifiable : refus) ; C-5 (liste des dossiers lue de `garde/dossiers.txt`) ; C-6 (cas des tests du crochet en chemin relatif ; cause côté R5 : item L-G6) ; C-7 (« fan out » ne vaut jeton que dans une phrase sans négation) ; C-8 (huit mutants tués).
2. **C-1** (sha256 du crochet cités au README, faux dès qu'un autre groupe le touche) : résolue par le lot d'intégration (ajout README final par groupe, sha256 recalculés).
3. **Conflits de sens avec le groupe A** à résoudre à l'intégration : P2A-4 lit la variable `cibles` que GFB-2 retire (sans recalage, erreur avalée par le crochet et **toute commande Bash passe sans contrôle** : point bloquant, test exigé) ; deux règles nommées R7 (renumérotation : la règle du groupe A devient R11, ou numérotation unique au lot d'intégration).
4. Limites L-G1 à L-G8 : items au versement ; E-4 de la G2 (`avant_acte.py diff` non lancé, sortie 3 sans dépôt git) : le contrôle se fait à l'intégration (dépôt jetable).
5. Écarts E-1 à E-3 admis.
