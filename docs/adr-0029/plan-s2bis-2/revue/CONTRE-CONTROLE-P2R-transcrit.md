# Contre-contrôle des corrections de PLAN-S2BIS-2 et répétition à l'échelle (REPETITION-1) (transcrit)

> Transcription par l'orchestrateur le 2026-10-08 14:37:21 UTC du rapport écrit par le réviseur de la G2 (agent a77f6435bdf260604, reprise) dans `<scratchpad>/s2bis/plan2/cc/RAPPORT-CC.md` (sha256 3b927bc7…), dont le résumé a été rendu par message ; contrôle FM-1.1 : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte du réviseur ci-dessous, sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Contre-contrôle des corrections de PLAN-S2BIS-2, et répétition à l'échelle du lanceur (REPETITION-1)

- **Gate 0** : modèle résolu `claude-opus-5-5`. Je suis le réviseur de la G2 de ce lot et je n'ai écrit aucune correction.
- **Horloge** (`date -u`) : début le 2026-10-08 à 14:15:47 UTC, fin à 14:36 UTC.
- **Base** : tête `e6657dcc3154bf2d35c69b84d9deae1385e702a7`, relevée au début et à la fin ; `git status --short` vide aux deux relevés.
- **Pièces** :
  - `corr/BRIEF-CORR-P2R.md` ;
  - `corr/RAPPORT-CORRECTIONS-transcrit.md` ;
  - les 11 diffs de `corr/diffs/` ;
  - `corr/SHA256SUMS`, vérifié d'abord : sha256 `af5d12c3abb3…7766`, `sha256sum -c` OK sur 160 lignes. Il ne liste pas le rapport transcrit, posé ensuite, ni lui-même.

## 1. Verdict : CONFORME (liste fermée vide)

Toutes les corrections sont tenues :
- C-1 (a à d), C-2, C-3 (a à e) et C-4 ;
- Q-P2R-3 (refus P2/lecture, sans aucune valeur de journal) ;
- la fermeture de SHOGEN-PLAN-S2BIS-2-REFUS-NON-NOMMES-1.

Mes vecteurs S8, S9 et S22 sont fermés. Mes huit mutants restés vivants à la G2 sont tués. Aucun test n'est retiré ni affaibli. La forme est conforme. L'épingle neuve `fe46ebd62195d5d78e58163985e46a2691cefe9af9898c3c8e1257d8cad8f36f` est juste.

REPETITION-1 est faite sur journaux synthétiques à l'échelle de la campagne (§5) : code 0, A = B.

Une recommandation reste hors liste, à décider par l'orchestrateur (§4, Q-CORR-5) : lancer les scripts en `python3 -S`.

## 2. Application, épingle, suites

- **Application.** Les 11 diffs (P2R-0a à P2R-6b) s'appliquent en série sur une copie `git archive` de e6657dc (7 exclusions), **sans retouche** : `--check`, puis `--whitespace=error-all`. Chaque état est égal à `corr/snap/P2R-x`, sha256 fichier par fichier.
- **Épingle.** Après P2R-6b, sha256 de `scripts/plan-s2bis-2/SHA256SUMS` = `fe46ebd6…f36f`, et `sha256sum --strict -c` passe 12/12.
- **Suite finale : 34 tests OK** sous 3.11, 3.12 et 3.13 × `PYTHONHASHSEED` 0 et 1, en `-X dev -W error`, avec 0 ligne d'avertissement. DET-1 en fait partie.
  - 3.10 échoue à l'import, comme attendu (`hashlib.file_digest`, PY310-1).
- **Instantanés.** Les 11 instantanés sont verts : 2, 6, 7, 11, 14, 18, 20, 23, 28, 31 et 34 tests.
- **xtask** (`cargo --locked xtask verify` sur la copie corrigée, lignes de verdict seules) : S-G1 à S-G8 VERT ; S-G9 ROUGE, 1 violation, `docs/17-modele-de-menace.md:70` (connue) ; fmt, no_std et clippy VERT. C'est identique à la G2.

## 3. Tableau du contre-contrôle

| point | état final (fichier, ligne ou test) | preuve | tenu |
|---|---|---|---|
| C-1 a heredocs en `-I` | `lancer.sh` : `python3 -I -B - … 2> /dev/null` (deux lectures) | LAN-11 ; mutants H-01 et H-10 tués ; S9 | oui |
| C-1 b liste fermée et bytecode | `PY=(env -i PATH LC_ALL=C PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX="$PYC")` ; `<travail>/pyc` exigé absent (P2/sortie), puis créé, absolu | LAN-11, LAN-12, LAN-6 fin ; H-02, H-03, H-09 tués ; S9, S22 (PLAN-S2BIS), S23 ; `pyc` vide après le lancement à l'échelle | oui |
| C-1 c entrée hors `SHA256SUMS` | `find . ! -type d ! -path ./SHA256SUMS` comparé aux noms de `SHA256SUMS` : P2/epingle, code 3 | LAN-10, LAN-12 (lot) ; H-04 tué ; S8, S22 (lot) | oui |
| C-1 d tests, canal, README | LAN-10 à LAN-12, un par vecteur ; canal `faux` du `parametres.json` du lot ; README, Lancement, point 2 | lus ; rouges du correcteur (`corr/journal/rouge-*`) | oui |
| C-2 (e) et (f) | FIV-5 : chiffre de σ̂²_bloc et ligne D1-bis de plus ; EPI-2 : une entrée de plus | G-18, G-19, G-21 tués | oui |
| C-3 a | SOC-4 : `panne, pas_ecart, hors_enveloppe` donne P2/ecarts | G-03 tué | oui |
| C-3 b | SOC-5 : booléen dans `calendrier_hors_d5` donne P2/parametres | G-10 tué | oui |
| C-3 c | `masque_fiv.controle_b` : chacun des deux comptes porte exactement les strates ; MAS-3 en deux cas | G-14 (adapté) et H-08 tués | oui |
| C-3 d | LAN-6 : sortie ne contenant que `.cache` donne P2/sortie | G-23 tué | oui |
| C-3 e | LAN-5 : `journal .cache.jsonl` donne P2/journal, « nom de journal refusé » | G-26 tué | oui |
| C-4 | commentaire « Ordre du code » | relu ligne à ligne contre le code, étapes 1 à 7 dans l'ordre exécuté | oui |
| Q-P2R-3 et REFUS-NON-NOMMES-1 | `socle.executer` : toute exception, P2/lecture nommé par son seul type ; P2/usage (code 2) et P2/sortie (code 1) sur stderr ; lanceur : chaque sortie hors 0 nommée | LEC-1 (12 chemins), LEC-2, LAN-13 ; H-05, H-06, H-07 tués ; e2e L1 et L2 | oui |
| aucun test retiré ni affaibli | 28 tests devenus 34, 0 retiré ; les 10 tests modifiés gardent leurs cas d'origine et autant d'assertions ou plus | comparaison par `ast` des deux états | oui |
| forme | voir §3.3 | — | oui |

### 3.1 Vecteurs et lecture de bout en bout (`outils/cc_e2e.py`)

Dépôt jetable, vrais scripts, fixtures seulement. Je n'ai jamais posé la variable de campagne.

| scénario | G2 (état d'origine) | état corrigé |
|---|---|---|
| S0 nominal | 0 | 0 : écran propre, aucun témoin extrait, sortie égale à un lancement direct, `pyc` vide, `lancer.log` 0 octet |
| S8 `json.py` en trop dans le lot | 0, 4 exécutions étrangères | 3, P2/epingle, rien d'exécuté |
| S9 ombre `PYTHONPATH` | 0, 6 exécutions | 0, rien d'exécuté |
| S22 `.pyc` forgé dans le lot (`socle`) | 0, 4 exécutions | 3, P2/epingle, rien d'exécuté |
| S22 `.pyc` forgé dans PLAN-S2BIS (`commun`) | 0, 4 exécutions | 0, rien d'exécuté |
| S23 `PYTHONHOME`, `PYTHONINSPECT`, `PYTHONWARNINGS=error`, `PYTHONOPTIMIZE=2`, `TMPDIR` hostiles | non éprouvé | 0, quatre sorties |
| L1 fenêtre hors grille | 5, valeur dans `lancer.log` | 5, P2/lecture (ValueError) ; valeur absente de l'écran, de `lancer.log` (0 octet) et des sorties ; passe B non commencée |
| L2 ligne de journal corrompue non finale | non éprouvé | 5, P2/lecture (ValueError), `lancer.log` vide |

### 3.2 Mutants

Tous sont classés par la commande de la suite du lot, borne 300 s par mutant (le plus long a pris 10,4 s). Témoins : 34 OK au début et à la fin. Restauration contrôlée par sha256.
- **Campagne G2 rejouée sur l'état final** : 27 mutants, 26 tués, 0 FATAL. Le seul vivant est G-05, équivalent comme démontré à la G2. G-14 a été adapté au code corrigé ; il admet une strate absente d'un compte.
- **Mutants neufs à moi sur les corrections** (H-01 à H-10) : **10 tués sur 10**, 0 FATAL.
  - H-01 : second heredoc sans `-I` ;
  - H-02 : `PYTHONPYCACHEPREFIX` retiré ;
  - H-03 : `env` sans `-i` ;
  - H-04 : entrées cachées hors du contrôle ;
  - H-05 : P2/lecture recopie le message ;
  - H-06 : seule `ValueError` est rattrapée ;
  - H-07 : P2/usage en code 1 ;
  - H-08 : seul le calendrier est contrôlé par strate ;
  - H-09 : cache de bytecode déjà présent admis ;
  - H-10 : erreurs du heredoc à l'écran.

### 3.3 Forme des 11 diffs

Lignes ajoutées : 179, 168, 129, 200, 166, 176, 174, 91, 196, 132, 184, donc toutes ≤ 200. Les sha256 sont égaux à ceux du rapport du correcteur.

On compte 0 octet 92, 0 tabulation, 0 retour chariot, 0 ligne de plus de 120 caractères et 0 TODO ou FIXME dans les lignes ajoutées. Rien n'est touché hors de `scripts/plan-s2bis-2/`. Dans les 13 fichiers finaux, la plus longue ligne fait 120 caractères, et il n'y a ni octet 92 ni TODO ou FIXME.

## 4. Questions Q-CORR et items

| question ou item | avis | motif |
|---|---|---|
| Q-CORR-1 (P2R-6 coupé en 6a et 6b) | **tenir** | Coupe du §1 déclarée, chaque moitié avec ses tests. Les instantanés intermédiaires sont verts (31 après 6a). P2R-4a et 4b ont toujours un lanceur incomplet qui finit en code 5. |
| Q-CORR-2 (`except Exception` après les arguments) | **tenir** | C'est la seule forme qui tienne « aucune sortie non nommée » et « aucune valeur dans la trace ». Une faute du code sortirait en P2/lecture, nommée par son type ; sa cause se cherche sur fixtures, selon la lettre de Q-P2-08. `BaseException` (interruption) reste hors champ, ce qui est juste. |
| Q-CORR-3 (scripts : P2/usage en code 2, P2/sortie en code 1, sur stderr) | **tenir** | Cohérent avec le lanceur (2 = usage) et avec le §4 (scripts en 0 ou 1). Le lanceur rend 5 sur tout script hors 0. |
| Q-CORR-4 (`<travail>/pyc` exigé absent, puis créé) | **tenir** | Chemin déterministe et fraîcheur vérifiée. Mesuré vide après le lancement à l'échelle. |
| Q-CORR-5 (`-s` non posé aux scripts) | **décision à prendre**, je recommande de serrer | Sur cet hôte, le site utilisateur existe et est actif (`/root/.local/lib/python3.11/site-packages`, sans `.pth` aujourd'hui). Des `.pth` système existent et s'exécutent à chaque démarrage sans `-S` (`uno.pth`, `distutils-precedence.pth`) : `-s` seul ne les écarterait pas. J'ai mesuré `python3 -S` sans rien écrire dans le HOME (`outils/sans_site.py`) : les deux scripts du lot, bibliothèque standard seule, y donnent des sorties identiques à l'octet, et aucun `site-packages` n'est dans `sys.path`. Poser `-S` aux scripts dans `lancer.sh`, avec un test, coûte une ligne et ferme le site système comme le site utilisateur. |
| SHOGEN-PLAN-S2BIS-2-EPINGLE-INTERPRETE-1 | **juste** | Constat confirmé : site utilisateur actif, `.pth` système, `python3` pris au PATH, `git`, `tar` et `sha256sum` non épinglés. Construction juste (consigner au JOURNAL le chemin, la version et le sha256 de `python3`, et la version de `git`), complétée par l'option `-S` mesurée ci-dessus. Déclencheur juste : épinglage au JOURNAL. |
| SHOGEN-PLAN-S2BIS-2-TRACE-HARNAIS-1 | **juste** | Lu dans le harnais de `f35a70c` : `records.read_jsonl_tolerant` écrit sur stderr le chemin et le numéro d'une dernière ligne tronquée ; `r1.parse_journal` écrit le chemin et des comptes de prix non finis par flux. Ce sont des chemins et des comptes, jamais une valeur recopiée, et ils vont dans `lancer.log`. Construction (procédure : `lancer.log` lu par lignes nommées) et déclencheur (épinglage) justes. Dans mes lancements, `lancer.log` faisait 0 octet. |

Je n'ai pas d'avis différent du correcteur sur les autres items qu'il a maintenus : PY310-1, WERROR-IGNORE-1, ESTIMATION-1 (précisé à 1 701 lignes).

## 5. REPETITION-1 (E-P2-20), sur journaux synthétiques seulement

### 5.1 Forme

- **Dépôt jetable** `cc/rep/depot` :
  - `git init` ;
  - `f35a70c` amené par `git fetch --depth=1 /home/user/shogen f35a70c19ba8269f1f7e2bcd31775e4fc513da20`, protocole v2, en lecture seule (le dépôt de session est resté propre) ;
  - vrais scripts du lot corrigé, vraies pièces de PLAN-S2BIS (`commun`, `regles`, `episodes`, `tests/fixtures.py`, `SHA256SUMS`) ;
  - `parametres.json` de PLAN-S2BIS de fixture : faux paquet sur les sha256 des journaux synthétiques, faux rendu à bloc 3 recompté par r1, grille réelle des 17 ℓ ;
  - EP de fixture, produite par `episodes.main` épinglé ;
  - `parametres.json` du lot ré-épinglé sur ces pièces, et `SHA256SUMS` recalculé **dans la copie seule** (épingle `dac6434d3282…97f8`).
- **Journaux synthétiques** (`outils/rep_prep.py`, graine fixe), à l'échelle de la campagne :
  - grille réelle : t0 = 1787770800, plage D5 réelle, 46 468 positions, n fixe = 38 600 ;
  - 7 868 absences tirées au hasard, en suites ;
  - 38 600 fenêtres pour dix hôtes synthétiques, plus un flux au pool S2 ;
  - pannes en suites, pannes communes, périmés et hors-enveloppe ;
  - `journal.jsonl` de 92 596 944 octets et `control.jsonl` de 3 950 495 octets.

  Les absences retrouvent les comptes publics d'ADR-0029 l.31 : le masque calculé par ma sonde est **égal** aux comptes épinglés du lot (30 286 et 13 491 ; 5 701 et 2 094), dont la section `masque` reste donc la vraie.
- **Lancement.** Préparation : 47 s. Lanceur lancé **détaché**, accepté sans refus du contrôle de sécurité, sous un enveloppeur de mesure en bibliothèque standard (`outils/mesure.py`, `os.wait4`), car `/usr/bin/time` est absent de l'hôte (E-1).
  - PID : enveloppeur 8618, lanceur bash 8620.
  - Commande : `bash <depot>/scripts/plan-s2bis-2/lancer.sh <rep>/j <rep>/sortie <rep>/travail <épingle>`.
  - Aucun chemin des journaux réels ni du dossier de session n'a été passé.

### 5.2 Mesures

| mesure | valeur |
|---|---|
| code de sortie | **0** |
| A = B | **oui** : `SHA256SUMS` de A, de B et de la sortie identiques (`9a9fbec1…`) ; sortie égale à A, octet pour octet |
| durée murale | **111,9 s** |
| phases, depuis le lancement (heures des fichiers) | contrôles 0 à 0,2 s ; extraction 0,2 à 0,3 s ; A `masque_fiv` jusqu'à 34,5 s (34,2 s) ; A `intervalles` jusqu'à 53,8 s (19,3 s) ; B `masque_fiv` de 54,0 à 89,7 s (35,7 s) ; B `intervalles` jusqu'à 111,6 s (21,9 s) ; comparaison et copie jusqu'à 111,9 s |
| CPU | 101,7 s utilisateur, 4,5 s système |
| mémoire résidente maximale | **932 188 Kio** (environ 910 Mio ; la plus grande des descendances, mécanisme de GNU time) |
| extraction de `f35a70c` | 400 fichiers, **5 975 109 octets** après les 7 exclusions (mesurés sur le flux `git archive` filtré comme par le lanceur, noms jamais affichés) ; flux brut 6 632 500 octets de fichiers, archive de 7 004 160 octets ; les 7 dossiers exclus sont absents de l'extraction (`test -e`, comptes de `compgen`) ; `s2-harness` extrait |
| sortie | 4 fichiers : `fiv_unites.txt` 238 432 octets (680 lignes FIV_u : 340 entières et 340 réduites), `intervalles.txt` 50 811 octets (40 entrées), `masque_j28.txt` 67 524 octets, `SHA256SUMS` 244 octets ; une passe fait 357 011 octets |
| contenu du masque à l'échelle | 46 468 positions ; D5 de j = 41 718 à 44 408 (2 691 positions) ; calme 30 286, 24 585 retenues, 5 701 sautées ; stress 13 491, 11 397, 2 094 ; 1 032 lacunes. Ce sont les valeurs de PROPOSITION §2.2 |
| écran | 10 lignes, toutes noms, codes ou sha256 ; stderr du lanceur : 0 octet |
| `lancer.log` | 0 octet |
| `<travail>/pyc` | vide |

L'écart `df` mesuré (216 911 872 octets) n'est pas fiable, car l'hôte est partagé (E-2) ; il n'est pas retenu.

Au regard de la mesure du générateur, scripts seuls (masque_fiv 27 à 30 s, intervalles 20 s, 909 Mo), le lanceur entier ajoute peu : l'extraction prend environ 0,1 s et le contrôle des sha256 environ 0,2 s.

## 6. Écarts de ma propre exécution

- **E-1. Outil de mesure.** `/usr/bin/time` est absent de l'hôte. Je l'ai remplacé par `outils/mesure.py` (`os.wait4`, `ru_maxrss`), qui mesure la même chose, sans dépendance neuve.
- **E-2. Écart `df`.** Il n'est pas fiable sur un hôte partagé ; j'ai mesuré la taille de l'extraction sur le flux `git archive` filtré (`tarfile` en mémoire, noms jamais affichés).
- **E-3. Phase de fin d'extraction.** Une première estimation par l'heure du dossier `A` était fausse : elle suit sa dernière entrée. Je l'ai corrigée par les heures de `pyc` et de `lancer.log`, avec des naissances à la seconde.
- **E-4. Octets 92 générés.** `repr()` a écrit deux octets 92 (sauts de ligne échappés) dans `mutants/campagne2.py`. Je les ai retirés avant le lancement ; contrôle sur les octets : 0. Je n'ai tapé aucune barre oblique inverse dans mes commandes ce tour-ci.
- **E-5. Listages d'un niveau.** J'ai listé, noms seuls, un niveau de l'extraction de `f35a70c` (racine : dont `JOURNAL.md` et `docs/`, jamais ouverts) et le dossier du lot du dépôt jetable. Pour `docs/15-*` et `docs/16-*`, je n'ai compté les correspondances qu'en nombre.
- **E-6. Variable de campagne.** La suite du lot (LAN-6, exception A-3 écrite au G0 et au README) pose `SHOGEN_S2_CAMPAGNE_CONTROL` dans son seul sous-processus de lanceur, à chacun de mes passages de la suite. Je ne l'ai jamais posée moi-même ; l'écart E-8 de la G2 ne s'est pas reproduit.
- **E-7. Git.** Sur le dépôt réel, je n'ai fait que des opérations de lecture : `archive`, `cat-file`, `status`, `rev-parse`, et la source d'un `fetch`, qui est `upload-pack` en lecture. J'ai écrit seulement dans mon dépôt jetable (`init` et `fetch` peu profond).
- **E-8. Concurrence de calcul.** La suite de l'instantané P2R-6b a tourné pendant la compilation de xtask (16,5 s au lieu d'environ 8 s) ; seule la durée en est affectée.

## 7. Provenance (G1)

**Lu [lu].**
- `corr/BRIEF-CORR-P2R.md`, en entier.
- `corr/RAPPORT-CORRECTIONS-transcrit.md` (311 l.), en entier.
- Les diffs, par l'état final comparé à `code/snap/P2R-5` : `lancer.sh`, `socle.py`, `masque_fiv.py`, `README.md` et les tests en entier pour leurs parties changées ; `tests/test_lancer.py` l.286-351.
- Harnais de `f35a70c` : `records.py` l.80-113 et `r1.py`, `parse_journal`.

**Commandes et sorties** (`unshare -n` et `lo` allumée pour les suites, les campagnes, l'e2e et la répétition) :
- 14:16 SHA256SUMS de `corr` ;
- 14:17 série et épingle ;
- 14:19 suites ;
- 14:21 e2e ;
- 14:22 à 14:26 campagne G2 (PID 24521) ;
- 14:27 à 14:28 mutants neufs (PID 19917) ;
- 14:29 préparation (PID 8312) ;
- 14:30 à 14:32 lanceur à l'échelle (PID 8618 et 8620) ;
- 14:33 instantanés ;
- 14:33 à 14:34 xtask (PID 21878).

Les fins ont été constatées en sondant le PID ; les listes `ps` sont filtrées sur le nom exact du script.

**Recomptes [calc].** Tous par script : lignes ajoutées, octets 92, longueurs, TODO et FIXME, comparaison des tests par `ast`, classements des campagnes, mesures de la répétition (`rep/mesures.json`).

## 8. Fichiers produits

Tous sont sous `<scratchpad>/s2bis/plan2/cc/` :
- `RAPPORT-CC.md` (ce rapport) et `NOTES.md` ;
- `outils/` : `cc_e2e.py`, `e2e.py`, `compare.py`, `sonde.py`, `rep_prep.py`, `rep_mesures.py`, `mesure.py`, `sans_site.py` ;
- `mutants/` : `campagne.py`, `campagne.out`, `campagne2.py`, `campagne2.out` ;
- `rep/` : `manifeste.json`, `mesure.json`, `mesures.json`, `lanceur.out`, `lanceur.err`, `prep.out`, `df-avant.txt`, `lancement.txt`, et `sortie/` (les 4 fichiers de sortie synthétiques) ;
- `travail/` : `suite.sh`, `xtask.sh` ;
- `tmp/` : sorties des suites, de l'e2e et de xtask.

`SHA256SUMS` du dossier : 92 lignes, `-c` OK, ce rapport exclu ; sha256 `00a3d2a39a9ac6cd788270b38e45636d36efff35309c849cd5b91e5e12573f1f`. Aucun fichier du dossier ne porte d'octet 92.

Les copies lourdes ont été retirées : copie de e6657dc, harnais, cible cargo, copies de mutants, dépôt jetable avec `f35a70c`, dossier de travail avec l'extraction, journaux synthétiques et pièces. Le dépôt est intact : `git status` vide, HEAD e6657dc.

## 9. Attestation (forme D.3)

- Aucun journal réel de S2 ni de S2-bis n'a été lu, listé, cherché ni haché. Les seuls `*.jsonl` sont synthétiques ; ils ont été écrits et lus par les tests, l'e2e et la répétition sous mon dossier, puis retirés, jamais affichés.
- `lancer.sh` n'a tourné que dans des dépôts jetables, sur fixtures ou sur journaux synthétiques.
- Aucune pièce de la liste D.2 n'a été ouverte.
- Rien n'a été ouvert de `docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/` ni `docs/adr-0028/execution/`, qui étaient exclus de mes copies et de l'extraction.
- Je n'ai fait aucune recherche récursive sur `docs/`, sur le dépôt ni sur le scratchpad entier.
- Je n'ai fait aucune écriture git sur le dépôt, et rien sur Pocket.
- Je n'ai jamais posé `SHOGEN_S2_CAMPAGNE_CONTROL` moi-même.
- Exposition : aucune valeur de S2 affichée ; les comptes publics d'ADR-0029 l.31 ont servi à caler les absences synthétiques ; aucune donnée de S2-bis n'existe.
