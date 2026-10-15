# s2-harness/tools : règle d'usage de l'enregistreur d'oracle (`oracle_record.py`)

Rattachement : item SHOGEN-S2BIS-ENREG-ANCRE-1 (ADR-0028, annexe B, bloc B.73 ; observation O-2 du contre-contrôle de
la réserve R-1, `docs/adr-0029/s2bis/revue-r1/`), sous le G0 `docs/adr-0029/g0-collecte/G0-COLLECTE-RECALC-DEPLOI.md` ;
lot OUT-2, diff OUT-2c (2026-10-08). Ce fichier ne couvre que l'enregistreur ; `rendu_unique.py` a sa docstring.

## L'ancre de confiance est l'arbre de l'outil

Pour `suite-s2bis` et `suite-sim-bis`, l'enregistreur lance la ligne du vérificateur écrite dans le `gates.yml` du
commit, avec le vérificateur de ce commit (`enforcement/verdict-suite-s2.py` de l'extraction). Il exige que ce
vérificateur soit égal, octet pour octet (sha256), à celui de l'arbre d'où l'outil tourne (`VERIF`), à l'écriture
comme à la lecture (SHOGEN-S2BIS-ENREG-VERIF-COMMIT-1, lot R-1). La comparaison ne dit donc rien du vérificateur du
commit par elle-même : elle le ramène à celui de l'arbre de l'outil, qui seul porte la confiance.

## Règle d'usage

1. L'outil tourne depuis un arbre dont le vérificateur a été relu (lecture humaine de son diff, consignée par une
   revue), extrait à part du commit à enregistrer : la comparaison ne vaut qu'à cette condition.
2. Lancé depuis l'arbre du commit enregistré lui-même, l'outil compare ce vérificateur à lui-même : la comparaison
   est triviale, et un vérificateur complaisant passe. Un tel enregistrement ne prouve rien de plus que le code de
   sortie de la ligne du job.
3. La lecture (`--verifier`) suit la même règle : elle compare `tree.sha256` au vérificateur de l'arbre du lecteur.
4. Qui cite un enregistrement nomme l'arbre d'où l'outil a tourné (commit, et sha256 de son
   `enforcement/verdict-suite-s2.py`) et la revue qui a relu ce vérificateur. À défaut, la lecture humaine du
   vérificateur reste nécessaire à chaque verdict cité (réserve R-1 de l'accord de P1).

## Limite

Le schéma `shogen.oracle-record.v1` ne consigne pas l'arbre de l'outil : cette règle est une règle d'usage, aucun
contrôle ne l'impose. Consigner cet arbre (commit, sha256 de `VERIF`, état propre ou non) demanderait un schéma v2 et
une décision.

## Extraction sans emplacement interdit (ajout daté du 2026-10-10 04:16:22 UTC, lot DETTES-T7)

Item SHOGEN-ENREG-EXTRACTION-INTERDITS-1. L'enregistreur extrait le commit par `git archive` dans le `TMPDIR` de
l'agent qui l'emploie. Il n'écrit ni ne hache aucun fichier d'un emplacement interdit des briefs, ni un lien qui y
mène : la règle est le prédicat `interdit` de `enforcement/docs-sha256sums.py` (préfixes d'`INTERDITS`, égaux à la
liste de S-G5 par un cas ; tout composant en `.jsonl` ; casse pliée), lu dans l'arbre de l'outil, jamais recopié.
L'enregistrement consigne `tree.exclus` : le nombre de chemins exclus et le sha256 de leur liste triée, un par ligne,
jamais leurs noms. La lecture refuse (`exclus`) un `tree.sha256` qui porte un chemin interdit, et, avec `--depot`, un
`tree.exclus` autre que celui de la ré-extraction. Un enregistrement sans `tree.exclus`, écrit par un outil antérieur,
est refusé (`champs`) : il se refait avec l'outil courant.

## Ajouts datés du 2026-10-10 04:58:08 UTC (lot DETTES-T7)

**Le vérificateur juge aussi `suite`** (SHOGEN-S2BIS-TOOLS-README-SUITE-1). La commande `suite` ne lance pas la ligne
d'un job, mais elle passe par l'amorçage `AMORCE` de `VERIF` et son run sorti en 0 est jugé par `accord` de `VERIF`
(compte réel, OUT-2i). La règle d'usage ci-dessus vaut donc pour `suite` comme pour `suite-s2bis` et `suite-sim-bis` :
un `VERIF` complaisant dans l'arbre de l'outil rendrait conforme un run `suite` forgé.

**Règle de lecture des enregistrements d'un outil antérieur** (SHOGEN-S2BIS-ENREG-ANCIEN-OUTIL-1 ; décision proposée
Q-3 du générateur, à adjuger). Un enregistrement dont un run `suite` n'est pas lancé par l'amorçage (`-B -c`, outil
d'avant OUT-2i : `-m unittest`, sans compte réel) ou dont une autre commande de la liste fermée n'est pas lancée en
`-I` (outil d'avant OUT-2d : masque de `tools/` non écarté) est refusé à la lecture, nommément (`ancien outil`). Il
n'est jamais cité comme preuve : la preuve est un enregistrement neuf du même commit, écrit par l'outil courant. Un
enregistrement sans `tree.exclus` (outil d'avant DETTES-T7) est refusé de même (`champs`).

**Délai : arbre arrêté** (SHOGEN-ENREG-DELAI-ARBRE-1). Chaque commande tourne dans un groupe de processus neuf. Au
dépassement, l'outil arrête tout son arbre : sous POSIX, le groupe de chaque descendant vivant, lu par
`ps -A -o pid=,ppid=,pgid=` (la suite que le vérificateur lance dans sa propre session comprise) ; sous Windows,
`taskkill /T /F`. À la sortie normale, le groupe de la commande est arrêté (descendant resté, fork) avant tout
nettoyage. Limites : un descendant déjà détaché de son parent dans un autre groupe n'est pas suivi ; sous Windows, rien
n'est arrêté après une sortie normale (les numéros de processus y sont réemployés) ; la branche Windows n'est pas
mesurée sur l'hôte de la session (Linux) : elle l'est au premier rejeu de la suite sur un hôte Windows.

**Forme K et résidus** (SHOGEN-S2BIS-ANALYSEUR-RESIDUS-1). La ligne d'un job n'est lue que si `gates.yml` n'a aucun
résidu (`residus` de `VERIF` : N-12, N-14, LC-02, LC-13) et que le job suit la forme K (`gabarit` de `VERIF`, celui du
cas K-02 du runner) ; sinon refus qui nomme chaque écart. Limites : `residus` refuse plus que la forge (ancres et alias
de types valides, admis par la forge, compris) mais ne voit pas toute autre invalidité du fichier, que lisent
`enforcement/workflows-yaml.py` (job g1) et la forge. Limite L-4 de l'épreuve de forge (classe LC-09 et LC-10, hors
item) : les blancs Unicode que `str.strip` et `str.split` retirent (U+00A0, U+1680, U+2000 à U+200A, U+202F, U+205F,
U+3000) ne sont pas nommés ; en fin de ligne du vérificateur, la ligne est lue et lancée par l'outil sans eux, alors
que bash les garde dans le dernier argument : le job échoue à l'exécution (gate fermée), l'enregistrement atteste la
ligne.

**Code compilé** (SHOGEN-S2BIS-COMPILE-LIMITES-1). La règle `bytecode` (OUT-2h) ne voit que les fichiers compilés de
l'arbre extrait : du code compilé chargé autrement n'est pas vu (écrit pendant le run hors d'un `__pycache__`, archive
zip, dossier hors de la racine ajouté à `sys.path` par un test) ; la lecture humaine du diff des tests reste
nécessaire. `compiles` de `VERIF` suit les liens de dossiers : un lien vers un très grand dossier allonge la lecture.
Sous Windows sans droit de créer des liens, les cas du runner qui en posent échouent fermés.

**Variables de l'environnement et enfants `-I`** (SHOGEN-S2BIS-DRAPEAUX-LIMITES-1 ; décision proposée Q-5 du
générateur). `-I` implique `-E` : un enfant isolé ignore toute variable `PYTHON*` (mesuré sous 3.10 à 3.13). Une
ligne par variable :
- `PYTHONDEVMODE`, `PYTHONWARNINGS` : rendues en ligne de commande par `drapeaux` (`-X dev`, `-W`, OUT-2j).
- `PYTHONHASHSEED` : consignée (`env`), sans drapeau équivalent ; seule `suite` l'applique ; les autres commandes
  tournent sous une graine aléatoire (mesuré : `hash` change d'un lancement à l'autre sous `-I`).
- `PYTHONPATH` : consignée, écartée exprès des enfants `-I` (OUT-2d).
- `PYTHONUTF8` : non rendue (drapeau `-X utf8`) ; l'enfant `-I` suit la locale (mesuré : mode UTF-8 inactif sous
  `C.UTF-8`).
- `PYTHONOPTIMIZE` : non rendue (drapeau `-O`) ; les assertions restent actives dans l'enfant `-I` (mesuré).
- `PYTHONIOENCODING` : non rendue, sans drapeau équivalent ; flux encodés selon la locale.
- `PYTHONDONTWRITEBYTECODE`, `PYTHONSAFEPATH`, `PYTHONNOUSERSITE` : sans objet (`-B` est passé ; `-I` écarte déjà
  le dossier du script et le site de l'utilisateur).
- toute autre variable `PYTHON*` (`PYTHONINTMAXSTRDIGITS`, `PYTHONWARNDEFAULTENCODING`, `PYTHONFAULTHANDLER`,
  `PYTHONTRACEMALLOC`, `PYTHONPYCACHEPREFIX`, `PYTHONUNBUFFERED`…) : non rendue.
Règle : une variable ajoutée à la matrice des versions entre d'abord à `drapeaux` (par un lot, avec son test), ou sa
limite s'écrit ici ; sinon elle ne vaut que pour `suite`.

## Ajouts datés de la relecture G2 du lot DETTES-T7

- *Ajout daté du 2026-10-10 07:18:55 UTC (correction C-2 ; SHOGEN-ENREG-DELAI-ARBRE-1)* : après l'arrêt de l'arbre au
  délai, l'outil ne lit plus la sortie que `RELIQUAT` s (5 s). Un descendant détaché de son parent (double fork,
  `setsid`) qui garde le tuyau n'est pas attendu au-delà : il reste vivant et sa sortie au-delà est perdue (avant
  C-2, il était attendu sans borne : mesure M-D1 de la relecture, 90 s d'attente pour un descendant de 90 s).
- *Ajout daté du 2026-10-10 07:19:46 UTC (correction C-3 ; SHOGEN-ENREG-EXTRACTION-INTERDITS-1)* : un lien qui mène au
  dossier d'un emplacement interdit lui-même (`docs/x -> rapports`, cible sans barre finale, que le prédicat seul
  ne voit pas) est exclu comme un lien vers un fichier interdit ; avant C-3, il était écrit, pendant, et le hachage
  échouait (mesure M-B1 de la relecture). Limite : un lien qui n'y mène qu'à travers un autre lien
  (`a -> b/d.md`, `b -> rapports`) est écrit, pendant ; le hachage échoue alors (`FileNotFoundError`, sortie 2) :
  aucun enregistrement, aucun fichier interdit écrit (mesure M-B2).
