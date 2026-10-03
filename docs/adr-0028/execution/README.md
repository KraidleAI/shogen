# Sorties de l'exécution unique de S2

Dossier parent de la sortie de `s2-harness/tools/rendu_unique.py` (`--sortie docs/adr-0028/execution/rendu-<date>`),
créé le 2026-10-02 avant l'exécution : le script crée son répertoire temporaire voisin de la cible (`tempfile.mkdtemp`,
`rendu_unique.py` l.426) hors de son `try` ; un dossier parent absent ferait échouer la production après les gardes, sans
ligne « échec de production » (constat H-1 de la relecture G2 de rattrapage R-C, annexe B.41). Procédure :
`docs/adr-0028/PROCEDURE-EXECUTION.md`. Les journaux scellés ne sont jamais versés ici.

> *Ajout daté du 2026-10-03 01:43:15 UTC (relecture G2 de la partie 4, `docs/G2-partie-4.md`, K-5 ; C-1 ; lignes ci-dessus conservées)* : depuis `4c831b8` (lot CORR, CORR-3b ; SHOGEN-RENDU-MKDTEMP-1 fermé, annexe B.44), `mkdtemp` est dans le `try` de `produire_tout` (`rendu_unique.py` l.431) : un dossier parent absent donne une ligne « échec de production », code 1, rien d'écrit. Le dossier reste requis (procédure §1).
