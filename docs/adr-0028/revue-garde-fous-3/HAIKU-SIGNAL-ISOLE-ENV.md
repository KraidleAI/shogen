# Signal Haiku (shogen-extracteur, claude-haiku-5-5, effort high) : corrections C-1 à C-3 proposées par la G2 d'ISOLE-ENV — 2026-10-17 00:38:11 UTC (`date -u`)

Contrôle par script de l'orchestrateur : 11 citations de NOTES.md sur 11 justes, mot pour mot et à la bonne ligne (NOTES.md : 14 lignes). Sources relues avant tout acte : les trois diffs.

| C-n | fichiers | changement (signal) | motif dans NOTES |
|---|---|---|---|
| C-1 | scripts/controle/tests/test_aide_garde.py | la constante LUES (neuf variables des modèles) remplace l'assertion sur DETACHE seule | aucun constat explicite (l.12 le plus proche) |
| C-2 | .claude/hooks/tests/test_garde_faits.py ; scripts/controle/tests/__init__.py ; scripts/controle/tests/test_garde_refus.py | affectation directe de SHOGEN_GARDE_REFUS à os.devnull au lieu de setdefault ; classe JournalJamaisHerite | l.10, l.11 (journal ambiant écrit, cause setdefault) |
| C-3 | scripts/controle/tests/test_aide_garde.py ; scripts/controle/tests/test_gabarit_chaine.py | ROUGE=X-1 ambiant dans le cas rejoué ; ROUGE posée vide dans lancer() | l.7 (variable ROUGE lue dans le diff, pas dans NOTES) |

Usage : préparation de l'adjudication ; le verdict se prend sur RAPPORT-G2.md et les diffs, pas sur ce signal.
