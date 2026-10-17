# Adjudication du lot ISOLE-ENV (orchestrateur, 2026-10-17 00:46:50 UTC, `date -u`)

GROUPES : aucun

- **G2 neuve** (`g2/RAPPORT-G2.md`, `shogen-worker` distinct du générateur ; Gate 0 `claude-opus-5-5` : 176 occurrences, aucune autre ; FM-1.1 : 0 ; `SHA256SUMS` du dossier : 92 lignes, toutes justes) : **ACCEPTE-AVEC-CORRECTIONS**, liste fermée C-1 à C-4.
- **C-1** (oracle indépendant `LUES`, mutants M4, M9, M10 tués) et **C-4** (apostrophes du README) : **fondues dans le diff** (v2, `ad59159c7593c66c…`, +53/−3), reprises à l'octet depuis `g2/diffs/`.
- **C-2** (`SHOGEN_GARDE_REFUS` par affectation dans `tests/__init__.py` et les cas du crochet ; cas `JournalJamaisHerite`, un test) et **C-3** (`ROUGE` posée vide par `lancer()`, cas rejoué sous `ROUGE=X-1`) : **adoptées, posées en pas INT-23** de la chaîne INTEGRATION-P3 (après le lot CAUSES ; `git apply` des deux diffs vert sur l'état final plus C-1 ; la tête les refuse, hunk d'INT-18), plancher final +1 ; README `readme/E.txt`.
- **Points du réviseur** : les cas du crochet hors de `gates.yml`, `ISOLE`, `CC`/`PYTHON`, `BASH_ENV` : un item daté, SHOGEN-CI-TESTS-CROCHET-1 (premier lot de S2-bis touchant `gates.yml`, butoir 2026-10-31), aucune dette nue. SHOGEN-CHAINE-BLANC-ENV-LANCEMENT-1 : fermé par la porte K8 du lot CAUSES au même versement.
- **Signal Haiku** (`haiku/SIGNAL-ISOLE-ENV-Cn.md`, extracteur `claude-haiku-5-5`) : table des C-n contrôlée par script, onze citations justes ; aucune décision prise sur ce signal.
- **Preuves exigées avant le commit** : suite `scripts/controle` sur la tête plus v2 au plancher 179, environnement normal et variables de lancement ; état final plus INT-23 au plancher 232, normal et hostile (`SHOGEN_GARDE_REFUS`, `ROUGE=X-1`, `DETACHE=1`), journal hostile vide ; cas du crochet verts (`preuves-v2/`).
- **Commit** : par le modèle de chaîne scellé (plan d'un pas, `chaine/preparer-isole.sh`, ce fichier passé par `CC`), avant INT-01 ; message `ISOLE-ENV : …`, `Diff-Id: ISOLE-ENV`, `Source-Sha` du rapport du générateur.
