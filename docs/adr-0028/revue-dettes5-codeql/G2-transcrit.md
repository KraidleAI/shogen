# Relecture G2 neuve du correctif DT5-24 (transcrit)

> Transcription par l'orchestrateur le 2026-10-10 03:49:26 UTC du fichier g2/RAPPORT-G2.md ; contrôle FM-1.1 du transcript du réviseur G2, par le fm11.py versé et par celui de DT3-E : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Relecture G2 du correctif DT5-24 (alerte CodeQL py/redos de la PR n° 11, lot DETTES-T5)

**Gate 0 : modèle résolu `claude-opus-5-5`** (identifiant exact donné par l'environnement de la session ; effort `max`
demandé, que je ne peux pas observer de l'intérieur). Je suis un réviseur neuf. Je n'ai écrit ni le correctif ni aucune
pièce du lot : l'auteur est l'orchestrateur.

`date -u` au départ : 2026-10-10 02:41:49 UTC ; au début de la rédaction : 03:21:32 UTC ; à sa fin : 03:26:45 UTC.

## 0. Cadre, pièces, base

- **Dépôt** `/home/user/shogen`, en lecture seule. Je n'y ai fait aucune écriture git ni aucun commit, et je n'y ai
  modifié aucun fichier. Tête à mon départ : `6e017729c1640e151f3004603823eda8b77b82ad`. Tête à la rédaction :
  `612b19dd05db5b8762e745b890c643d694d9feaf` (commits FUZZ de l'orchestrateur, faits pendant ma relecture). `ba5ea95`
  est un ancêtre de ces deux têtes (`git merge-base --is-ancestor` : 0). Les quatre fichiers en jeu ont, à `ba5ea95`
  comme à `612b19d`, les mêmes blobs : `gates.yml` 01b0354, `runners-epingles.py` dae1862, le fichier de test ebd7dd4 et
  `scripts/controle/README.md` 2d43110. Les trois premiers sont égaux aux lignes `index` du diff. Les entrées indexées
  visibles dans `git status` (ajouts sous `crates/shogen-verifier/fuzz-corpus/`, puis modifications sous `xtask/tests/`)
  sont celles de l'orchestrateur : je n'y ai pas touché.
- **Pièces** :
  - `DT5-24.diff` : sha256 recalculé `97cc54ee3777bf9c22dc24ea1e3bb5ec7537b984030d61c06259233e81092ac6`, égal à celui du
    brief. C'est l'empreinte des diffs relus (un seul diff dans la série).
  - `equivalence.py` : sha256 `dbfb2bae420be99720ef7b9627d397120b3e74b103f9ff3ad3704a0efaa49249`. Je l'ai lu, mais ni
    lancé ni réutilisé : mes preuves suivent d'autres méthodes (§2).
- **Copies**, toutes sous `g2/` :
  - `base` : `git archive ba5ea95`.
  - `copie` : `base` plus DT5-24, appliqué par `git apply --check` puis `git apply`. Les blobs après application
    (b18c9b7, de268ea, 809a991) sont ceux des lignes `index` du diff.
  - `rouge` : le code de `ba5ea95` avec le seul fichier de test du diff.
  - `mut`, `mut-corrige`, `mut-base` : arbres à muter, restaurés après chaque run et vérifiés par sha256 et `diff -r`.
  - `corrige`, `corrige2` : `copie` plus les corrections C-1 à C-3, pour les valider.
  - `base-c3` : le code de `ba5ea95` avec le test corrigé.
  - `tete` : `git archive 612b19d` plus DT5-24.
- **Environnement des runs de suite, de job et de script** (`g2/outils/lancer.sh`) :
  - `env -u SHOGEN_S2_CAMPAGNE_CONTROL -u HTTPS_PROXY -u HTTP_PROXY -u https_proxy -u http_proxy -u ALL_PROXY -u
    all_proxy -u NO_PROXY -u no_proxy`, avec `TMPDIR=g2/tmp` et `PYTHONDONTWRITEBYTECODE=1` ;
  - puis `isole.sh` (sha256 `ebaa1c78…`, avec `lo_up.py` `b532be4b…`).
  - Contrôle de l'isolement : `1.1.1.1:443` répond `Errno 101 Network is unreachable` ; `127.0.0.1:9` répond `Errno 111`
    (lo allumée) ; la variable S2 est absente.
  - La variable S2 n'est pas non plus posée dans mon environnement de départ (`env | grep -c` : 0).
  - Python 3.11.15. La CI utilise l'interpréteur de l'image ubuntu-24.04 (3.12 [inféré], non mesuré ici).
- **Interdits** : je n'ai ouvert aucune pièce de la liste D.2. Je n'ai rien lu sous `docs/15-*`, `docs/16-*`,
  `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/` ni
  `docs/adr-0028/execution/`, et aucun `*.jsonl`. Aucune recherche récursive sur `docs/`, sur le dépôt entier ou sur le
  scratchpad entier. Les seules recherches récursives ont porté sur `enforcement/`, `scripts/controle/` et `.github/` de
  ma copie. Les seuls documents de `docs/` lus sont `docs/adr-0028/CP2-S2.md` l.1-60 (§8, O-2).

## 1. Verdict : **ACCEPTE-AVEC-CORRECTIONS** (C-1, C-2, C-3)

Le code corrigé est juste :

- l'égalité exacte des langages est prouvée, pour VIDE, pour BLOC et pour le sous-motif que nomme le commentaire ;
- le retour arrière exponentiel a disparu, et aucune ambiguïté polynomiale ne le remplace ;
- le job est vert.

Les trois corrections portent sur le test, le README et la couverture :

- **C-1** : une des trois valeurs du test est inerte, et la docstring du test est inexacte.
- **C-2** : le README de `scripts/controle` donne un compte de tests et un plancher périmés.
- **C-3** : sept mutants non équivalents du diff survivent. L'un d'eux, M10, est une perte de couverture créée par la
  réécriture.

## 2. Équivalence exacte des langages (point 1)

### 2.1 Raisonnement

Notation :

- W : l'ensemble des caractères que reconnaît `\s`. Ce sont 29 points de code, exactement ceux pour lesquels
  `str.isspace` est vrai : vérifié sur tout Unicode (§2.2).
- N : le complément de W (`\S`).
- A = {`&`, `!`}, B = {`|`, `>`} et D = {`-`, `+`, `0`…`9`}. Ces trois ensembles sont inclus dans N.
- Un « mot » est une suite maximale de caractères de N.

Les formes en jeu :

- VIDE, ancienne forme : `W*(A N* W*)*` ; nouvelle forme : `W*(A N* W+)*(A N*)?`.
- BLOC : le même préfixe, suivi de `B D* W*` dans les deux formes.

**Lemme.** L(VIDE ancienne) = L(VIDE nouvelle) = V, où V est l'ensemble des chaînes dont chaque mot commence par un
caractère de A.

- **Ancienne ⊆ V.** Écrivons s = w0 b1 … bk avec w0 dans W\* et bi = ai ui wi (ai dans A, ui dans N\*, wi dans W\*).
  Prenons un mot qui commence en p. Le caractère s[p] est dans N, et p = 0 ou s[p-1] est dans W. Ce caractère n'est ni
  dans w0 ni dans un wi. Ce n'est pas non plus un caractère de ui, car son prédécesseur (ai ou un caractère de ui)
  serait dans N. C'est donc un ai, qui est dans A.
- **V ⊆ nouvelle.** Écrivons s = w0 r1 w1 … rk wk, où les ri sont les mots (ri dans A N\*) et les wi intérieurs sont
  dans W+.
  - Si k = 0, s = w0 : l'étoile est prise 0 fois et l'optionnel est absent.
  - Si wk n'est pas vide : (ri wi) est dans A N\* W+ pour chaque i, et l'optionnel est absent.
  - Si wk est vide : l'étoile prend r1 w1 … r(k-1) w(k-1), et l'optionnel vaut rk, qui est dans A N\*.
- **Nouvelle ⊆ ancienne.** A N\* W+ est inclus dans A N\* W\*, et A N\* aussi (avec W\* vide).

**BLOC.** Dans les deux formes, BLOC est la concaténation de L(VIDE) et du même suffixe `B D* W*`. Deux langages égaux,
concaténés au même suffixe, donnent des langages égaux.

**Sous-motif du commentaire.** Le même argument, sans w0, montre que `(?:[&!]\S*\s*)*` et `(?:[&!]\S*\s+)*(?:[&!]\S*)?`
ont le même langage.

**Le moteur re décide bien ce langage.** Aucun corps répété ne reconnaît la chaîne vide : `[&!]\S*\s*` consomme au moins
1 caractère, `[&!]\S*\s+` au moins 2. La protection de sre contre les itérations vides ne coupe donc aucune analyse, et
`fullmatch` répond par l'appartenance au langage.

**Le script ne dépend que de ces langages.**

- Il ne lit VIDE et BLOC que par `VIDE.fullmatch(valeur) is not None` et par la valeur de vérité de
  `BLOC.fullmatch(valeur)` (l.61 et 64 du script corrigé). Un objet Match est toujours vrai, None est faux.
- Les motifs n'ont pas de drapeau ; `\s` est donc unicode dans les deux formes.
- `valeur` peut porter tous les caractères sauf LF : CR, VT, FF, U+001C à U+001F, U+0085, U+2028, etc. La partition
  ci-dessous les couvre tous.

### 2.2 Preuve mécanique par automates (autre méthode que l'énumération de l'auteur)

L'outil `outils/automate.py` lit les motifs dans le source par son arbre syntaxique (`outils/motifs.py`) ; ils ne sont
jamais retapés. Il procède en quatre étapes.

1. **Partition** de U+0000 à U+10FFFF, substituts compris, par le vecteur d'appartenance aux atomes des motifs (`\s`,
   `\S`, `[&!]`, `[|>]`, `[-+0-9]`). Le moteur re classe chaque caractère lui-même. On obtient 5 classes :

   | classe | points de code |
   |---|---|
   | autres non-blancs | 1 114 067 |
   | blancs | 29 |
   | `[&!]` | 2 |
   | `[-+0-9]` | 12 |
   | `[|>]` | 2 |

   Le total vaut 1 114 112 = 0x110000. Les 29 blancs sont U+0009-000D, U+001C-001F, U+0020, U+0085, U+00A0, U+1680,
   U+2000-200A, U+2028, U+2029, U+202F, U+205F et U+3000. Deux contrôles passent : `\S` est le complément de `\s`, et
   `\s` coïncide avec `str.isspace` sur tout Unicode.
2. **Automates.** Automate de Glushkov de chaque motif sur ces 5 classes, rendu déterministe par sous-ensembles.
   L'égalité des langages s'établit par un parcours du produit, valable pour toutes les longueurs.
3. **Ambiguïté** (§3.2).
4. **Témoins de non-vacuité.** Quatre variantes non équivalentes, fabriquées par remplacement de texte, sont toutes
   distinguées, et chaque contre-exemple est rejoué sur re : VIDE sans l'optionnel (`'!'`), optionnel en `\S+` (`'!'`),
   BLOC sans l'étoile (`'!\t>'`), BLOC sans l'optionnel (`'!>'`).

Résultats (`sorties/automate.out`, 1,7 s) :

| paire | Glushkov (ancienne / nouvelle) | déterministes | minimaux | langages égaux | couples du produit parcourus |
|---|---|---|---|---|---|
| VIDE | 5 / 7 | 7 / 6 | 3 / 3 | **oui** | 7 |
| BLOC | 8 / 10 | 13 / 12 | 7 / 7 | **oui** | 13 |
| sous-motif du commentaire | 4 / 6 | 6 / 5 | 4 / 4 | **oui** | 6 |

### 2.3 Contre-épreuve sur le moteur re, à trois voix, en caractères réels

L'outil `outils/moteur.py` compare trois voix : l'ancienne forme, la nouvelle et l'automate déterministe de §2.2. Les
classes de caractères sont tirées de réservoirs que le moteur classe lui-même :

- les 29 blancs ;
- pour les autres non-blancs : 3 119 caractères, dont des substituts isolés, U+10FFFF, des signes et chiffres pleine
  chasse, U+200B, U+FEFF et U+180E, plus 3 000 points de code tirés au hasard.

Les réservoirs comptent 3 036 caractères non ASCII. Résultats :

| jeu | chaînes | acceptées par VIDE | acceptées par BLOC |
|---|---|---|---|
| exhaustif, longueurs 0 à 9 sur les 5 classes | 2 441 406 | 237 963 | 93 919 |
| aléatoire structuré en mots, longueurs 10 à 120 | 200 000 | 61 495 | 46 232 |
| écrit à la main (ancre, étiquette, en-tête, U+3000, U+2028, U+0085, U+001C, U+D800, etc.) | 32 | | |

Total : **2 641 438 chaînes, 0 écart** entre les trois voix (`sorties/moteur.out`, 34 s).

**Conclusion du point 1 : égalité exacte, aucune correction bloquante.**

## 3. Retour arrière (point 2)

### 3.1 Raisonnement

**Ancienne forme.** Dans `(?:[&!]\S*\s*)*`, le `\s*` final peut être vide et `[&!]` est inclus dans `\S`. Un mot qui
porte k caractères de A se découpe alors en itérations de 2^(k-1) façons. Sur un suffixe qui fait échouer la
correspondance, le moteur les essaie toutes.

L'annotation CodeQL lue au §3.4 pointe exactement ce terme : les colonnes 31 à 33 de la l.26 sont le `\S*` du groupe
étoilé.

**Nouvelle forme.** Une itération finit par `\s+`, donc par au moins un blanc, et la suivante commence par `[&!]`, un
non-blanc. Une frontière d'itération ne peut donc tomber qu'à un passage blanc → non-blanc. Dans une itération,
`[&!]\S*` prend le mot entier, car `\S` et `\s` sont disjoints : chaque mot n'a qu'une lecture.

Il reste trois choix, et aucun n'est sur un cycle :

- au début d'un mot, après des blancs : une itération ou l'optionnel final ;
- dans BLOC, sur un `|` ou un `>` du dernier mot : continuer `\S*` ou prendre `[|>]` ;
- `[-+0-9]*` contre `\s*` : classes disjointes.

Ces branches ne rentrent jamais dans l'étoile. Elles coûtent au plus un balayage linéaire de plus.

### 3.2 Ambiguïté mécanique (critère de Weber et Seidl, sur l'automate de Glushkov)

Les deux critères :

- **EDA** (ambiguïté exponentielle) : une composante fortement connexe de A × A contient un couple (q, q) et un couple
  (p, p') avec p ≠ p'.
- **IDA** (ambiguïté polynomiale) : il existe un chemin de (p, p, q) à (p, q, q) dans A × A × A, avec p ≠ q.

Résultats :

- **Anciennes formes, VIDE, BLOC et sous-motif : EDA oui.** Témoin : l'état `\s*` de l'étoile, dans la même composante
  qu'un couple (`\S`, `[&!]`). Elles sont aussi IDA (p = `[&!]`, q = `\S`, mot `'!'`).
- **Nouvelles formes : ni EDA ni IDA.**

Un automate émondé sans EDA ni IDA est d'ambiguïté finie. Le nombre de lectures d'un préfixe y est borné par une
constante, et la recherche par retour arrière est linéaire. Le critère et cette conséquence relèvent de ma connaissance
de relecteur [2nd] ; je ne les ai pas relus ici. Les mesures du §3.3 les corroborent.

### 3.3 Mesures sur des entrées adverses que j'ai construites

`outils/redos.py` lance chaque série dans un processus enfant, qui s'arrête de lui-même dès qu'une mesure dépasse 2 s.

**Nouvelles formes.** Sur 12 familles et pour n de 10^3 à 10^6, le temps est multiplié par environ 10 à chaque décade
(rapports observés de 5,1 à 14,9 ; les petits rapports sont du bruit aux tailles minimes). Valeurs à n = 10^6 :

| famille | VIDE (ms) | BLOC (ms) |
|---|---|---|
| F1 ` `+`!`\*n+`x b` | 26,0 | 27,0 |
| F2 ` `+`&`\*n+` b` | 22,7 | 30,2 |
| F3 ` `+`!`\*n+`|x` | 13,8 | 26,9 |
| F4 ` `+`! `\*n+`b` | 202,3 | 206,0 |
| F5 ` `+`!`\*n+` |x` | 25,2 | 26,5 |
| F6 ` !`+`|1`\*n+` b` | 51,3 | 100,5 |
| F7 ` `+U+3000\*n+`x` | 56,6 | 65,7 |
| F8 ` `+(`!`+U+2028)\*n+`x` | 208,2 | 210,7 |
| F9 ` `+`!`\*n+`|`+`1`\*n+`x` | 23,4 | 73,2 |
| F10 ` `+`&a `\*n+`|`+` `\*n+`x` (4 millions de caractères) | 194,4 | 228,9 |
| F11 ` |`+`-`\*n+` `\*n+`x` | 0,01 | 20,9 |
| F12 ` `+`!&`\*n+`x`+U+0085+`b` | 44,4 | 79,7 |

**Anciennes formes.** Le temps double à chaque caractère ajouté ; la dernière mesure avant l'arrêt est :

| famille | VIDE | BLOC |
|---|---|---|
| F1 | n = 25 : 2,48 s (rapports 2,02 à 2,89) | n = 25 : 2,72 s |
| F2 | n = 26 : 3,82 s | n = 25 : 2,14 s |
| F3 | aucune explosion | n = 25 : 3,31 s |
| F5 | n = 26 : 4,05 s | n = 25 : 2,41 s |
| F12 | n = 13 : 4,91 s (×4 par `!&`) | n = 13 : 5,62 s |

F3 n'explose pas pour l'ancienne VIDE, qui accepte la valeur. F4 et F8 n'explosent pour aucune forme : leurs mots d'un
seul caractère ne se découpent pas.

**Script de bout en bout, corrigé** (`outils/valeurs_test.py`) : 0,16 à 0,24 s sur les valeurs du test portées à
n = 10^6, sortie 0.

### 3.4 CodeQL py/redos

**L'alerte [lu].** Je l'ai lue par l'API, en lecture seule. Le run CodeQL 114111040759 de `ba5ea95` est en échec
(« 1 new alert including 1 high severity security vulnerability »). Il porte une seule annotation :

- emplacement : `enforcement/runners-epingles.py` l.26, colonnes 31 à 34 (soit `\S*`) ;
- titre : « Inefficient regular expression » ;
- message : le texte cité par le brief.

La l.25 (VIDE) n'est pas annotée. Explication [inféré] : CodeQL ignore le `fullmatch` appliqué plus loin, et VIDE, sans
ancre de fin, n'a pas de suffixe qui la fasse échouer.

**La règle [2nd, je ne peux pas lancer CodeQL].** La requête signale une répétition dont le corps lit une même chaîne de
deux façons : un état porte deux cycles distincts de même étiquette (une chaîne « pompable »), suivis d'un suffixe
rejeté.

**Nouvelles formes.** Les seuls recouvrements sont des sorties, jamais des cycles :

- `[&!]` de l'itération contre `[&!]` de l'optionnel ;
- `\S*` contre `[|>]` dans BLOC.

Une fois sorti de l'étoile, aucun chemin n'y rentre : il n'y a aucune chaîne pompable. Le calcul mécanique le confirme
(aucune EDA, §3.2). **Un analyseur du type py/redos ne devrait plus voir d'ambiguïté.** py/polynomial-redos ne
s'applique pas, faute de source distante [inféré], et l'IDA est absente de toute façon.

La fermeture effective de l'alerte reste à constater sur la forge après la poussée (O-1).

**Conclusion du point 2 : conforme.**

## 4. Le test ajouté (point 3)

### 4.1 Rouge à `ba5ea95`, vert corrigé

| arbre | commande | résultat |
|---|---|---|
| `rouge` : code de `ba5ea95`, test du diff | test seul | **ERROR** `subprocess.TimeoutExpired` sur la 1re valeur, « Ran 1 test in 20.023s », FAILED (errors=1) |
| `rouge` | ligne du job | **sortie 1**, Ran 37, errors=1 (`test_valeur_adverse_en_temps_borne` seul), deux refus du vérificateur |
| `base` : `ba5ea95` tel quel, sa ligne (plancher 36) | ligne du job | sortie 0, Ran 36, conforme (état de départ) |
| `copie` : corrigé | ligne du job | **sortie 0**, Ran 37, conforme |

### 4.2 Séparation VIDE / BLOC, valeur par valeur

`outils/valeurs_test.py` juge les valeurs par le script lui-même, sous la borne du test de 20 s, avec n = 5000 comme
dans le test. « borne » signifie que la borne de 20 s est atteinte (mesuré 20,02 s).

| variante du script | v1 `!`\*n+`x b` | v2 `&`\*n+` b` | v3 `!`\*n+`|x` | v4 `!`\*n+` |x` (proposée en C-1) |
|---|---|---|---|---|
| corrigé | 0,05 s, sortie 0 | 0,03 s | 0,03 s | 0,03 s |
| VIDE ancienne seule | **borne** | **borne** | 0,02 s, sortie 0 | **borne** |
| BLOC ancienne seule | **borne** | **borne** | 0,02 s, sortie 0 | **borne** |
| les deux anciennes (motifs de `ba5ea95`) | **borne** | **borne** | 0,02 s, sortie 0 | **borne** |

v1 et v2 attrapent **chacune séparément** le retour de VIDE et celui de BLOC. v3 n'attrape rien, même sur `ba5ea95` :
c'est un seul mot qui commence par `!`, que VIDE accepte en temps linéaire dans les deux formes. Le script s'arrête
alors à `vide or …` et n'évalue jamais BLOC. La docstring dit pourtant que l'ancienne forme « y faisait un retour
arrière exponentiel » : c'est faux pour v3 (C-1).

### 4.3 Mutants du diff, jugés par la ligne du job

`outils/mutants.py`, sha256 `82150c33…` :

- une mutation par run ;
- la ligne est lue dans le `gates.yml` de l'arbre muté ;
- réseau coupé ;
- arbre restauré et vérifié après chaque run ;
- classement SHOGEN-MUT-FATAL-1 : sortie 1 = tué, 0 = vivant, autre = FATAL ;
- témoins non mutés au début et à la fin, sortie 0 exigée.

`outils/decision.py` classe en plus chaque mutant selon la décision du script, qui ne dépend que du langage VIDE ∪ BLOC.
La campagne s'est déroulée de 03:15:28 à 03:19:32 UTC. Un premier passage, de 03:04:23 à 03:08:20, avait donné le même
classement (E-4). Résultat : **28 mutants, 20 tués, 8 vivants, 0 FATAL** ; témoins T0 et T1 en sortie 0.

| mutant | sortie | tué par | décision du script (plus court témoin) |
|---|---|---|---|
| M01 VIDE : retour à l'ancienne forme | 1 | test de temps borné | identique ; temps exponentiel |
| M02 BLOC : retour à l'ancienne forme | 1 | test de temps borné | identique ; temps exponentiel |
| M03 VIDE : `\s+` de l'étoile en `\s*` | 1 | test de temps borné | identique ; temps exponentiel |
| M04 BLOC : `\s+` de l'étoile en `\s*` | 1 | test de temps borné | identique ; temps exponentiel |
| M05 VIDE : optionnel retiré | 1 | `test_formes_hors_ligne` | `'!'` |
| M06 VIDE : optionnel obligatoire | 1 | 3 tests | `''` |
| M07 VIDE : `[&!]` de l'optionnel en `[&]` | 1 | `test_formes_hors_ligne` | `'!'` |
| M08 VIDE : `[&!]` de l'optionnel en `[!]` | 1 | `test_formes_hors_ligne` | `'&'` |
| M09 VIDE : `[&!]` de l'étoile en `[!]` | 1 | `test_formes_hors_ligne` | `'&\t'` |
| **M10** VIDE : `[&!]` de l'étoile en `[&]` | **0** | — | `'!\t'` : `runs-on: !!str # c` puis un bloc |
| M11 VIDE : `\s*` de tête retiré | 1 | `test_formes_hors_ligne` | `'\t'` |
| M12 VIDE : `\s*` de tête en `\s+` | 1 | 3 tests | `''` |
| **M13** VIDE : `\S*` de l'optionnel en `\S+` | **0** | — | `'!'` : `runs-on: !` puis un bloc |
| **M14** VIDE : `\S*` de l'étoile en `\S+` | **0** | — | `'!\t'` : `runs-on: ! &a` |
| **M15** VIDE : `\s+` de l'étoile en `\s` | **0** | — | `'!\t\t'` : `runs-on: &r  # c` |
| M16 BLOC : optionnel retiré | 0 | — | **identique, mutant équivalent déclaré** |
| **M17** BLOC : étoile retirée | **0** | — | `'!\t>'` : `runs-on: &a >-` |
| M18 BLOC : `[|>]` en `[|]` | 1 | `test_formes_hors_ligne` | `'>'` |
| M19 BLOC : `[|>]` en `[>]` | 1 | `test_formes_hors_ligne` | `'|'` |
| M20 BLOC : `[-+0-9]*` retiré | 1 | `test_formes_hors_ligne` | `'>+'` |
| M21 BLOC : `[-+0-9]*` en `[-+]*` | 1 | `test_formes_hors_ligne` | `'>0'` |
| **M22** BLOC : `\s*` final retiré | **0** | — | `'>\t'` : `runs-on: >-  # c` |
| M23 BLOC : `\s*` de tête retiré | 1 | `test_formes_hors_ligne` | `'\t>'` |
| M24 `gates.yml` : plancher 37 en 36 | 1 | vérificateur : « Ran 37 > plancher 36 (--egal) » | — |
| M25 `gates.yml` : plancher 37 en 38 | 1 | vérificateur : « Ran 37 < plancher 38 » | — |
| **M26** BLOC : `[&!]` de l'étoile en `[!]` | **0** | — | `'&\t>'` : `runs-on: &a >-` |
| M27 VIDE : `?` de l'optionnel en `*` | 1 | test de temps borné | identique ; temps exponentiel |
| M28 BLOC : `?` de l'optionnel en `*` | 1 | test de temps borné | identique ; temps exponentiel |

**Mutant équivalent : M16.** Le script teste VIDE avant BLOC, et VIDE ∪ BLOC = VIDE ∪ BLOC(M16) sur toutes les chaînes
(produit d'automates). BLOC(M16) est en outre sans EDA. L'optionnel de BLOC ne sert donc qu'à l'égalité exacte avec
l'ancienne BLOC que revendique le commentaire (O-3).

**Mutants non équivalents vivants : M10, M13, M14, M15, M17, M22, M26.** Dans chacun, le script cesse de lire le bloc
qui suit une forme YAML valide, ce qui fait un refus en moins. `outils/mutants_anciens.py` lance leurs analogues sur la
forme de `ba5ea95`, avec sa suite de 36 tests :

| analogue | à `ba5ea95` | lecture |
|---|---|---|
| A10 (`[&!]` en `[&]`) | **tué** par `test_formes_hors_ligne` | **M10 est une perte de couverture créée par la réécriture** : la classe est désormais dédoublée entre l'étoile et l'optionnel, et la suite ne place jamais d'étiquette avant un blanc |
| A13 (`\S*` en `\S+`) | vivant | M13 et M14 sont des trous déjà présents |
| A17 (étoile retirée) | vivant | trou déjà présent |
| A22 (`\s*` final retiré) | vivant | trou déjà présent |
| A26 (`[&!]` en `[!]`) | vivant | trou déjà présent |

M15 n'a pas d'analogue propre, car l'ancienne étoile reste exponentielle sous `\s?`. Son témoin réaliste est une ancre
suivie de deux blancs puis d'un commentaire, la forme même que le fichier de test emploie (`ubuntu-latest-4core  # grand
runner`).

Le brief demande au moins 8 mutants tués : **20 le sont**. Les 7 vivants non équivalents motivent **C-3**. Avec C-1 à
C-3 appliquées (§7), il reste **27 tués, 1 vivant (M16, équivalent), 0 FATAL**.

## 5. Le job (point 4)

Toutes ces commandes tournent par `lancer.sh` sur `copie` (`ba5ea95` plus DT5-24), répertoire courant à la racine de la
copie.

| commande | sortie | résultat |
|---|---|---|
| étape 1 du job : `python3 -B enforcement/tests/run-fixtures-verdict-suite-s2.py` | 0 | « 137 ok, 0 échec », dont K-04 controle-unittest : le gabarit admet la ligne de commentaire ajoutée, d'indentation 4 |
| étape 2 : `python3 --version` | — | Python 3.11.15 |
| étape 2 : `python3 -B enforcement/verdict-suite-s2.py scripts/controle --aucun-saut --egal --plancher 37`, ligne exacte de `gates.yml` | **0** | « Ran 37 tests in 4.154s », OK, « verdict-suite-s2 : conforme (code 0, résumé final, aucun saut, Ran = 37) » |
| `python3 -B enforcement/runners-epingles.py .` | 0 | conforme (7 workflow(s), 22 clé(s) runs-on/os lues) ; même sortie sur `base` |
| `/usr/bin/python3 -B enforcement/workflows-yaml.py .` | 0 | conforme (7 workflow(s), PyYAML 6.0.1) ; même sortie sur `base` |
| `run-fixtures-workflows-yaml.py` | 0 | 16 ok |

En plus, j'ai repris l'étape 1, la ligne du job, `runners-epingles` et `workflows-yaml` sur la tête actuelle (`612b19d`
plus DT5-24), parce que `fuzz.yml` y a changé depuis `ba5ea95` :

- étape 1 : 137 ok ;
- job : sortie 0, Ran 37 ;
- `runners-epingles` et `workflows-yaml` : conformes, 7 workflows et 22 clés.

## 6. Forme (point 5)

- **Longueur des lignes ajoutées** : 120 caractères au plus, la plus longue en fait 119.
  - Les deux lignes de docstring du test font 119 caractères (122 octets en UTF-8).
  - Le commentaire de `gates.yml` fait 118 caractères ; les quatre lignes de `runners-epingles.py` font 110, 110, 107
    et 98.
  - Aucune tabulation, aucune espace de fin.
  - Les trois fichiers n'ont aucune ligne au-delà de 120, hors 4 lignes de `gates.yml` antérieures au diff.
- **R-13** : aucun marqueur de tâche nu dans les lignes ajoutées ; la recherche des trois marqueurs usuels, en
  capitales, ne trouve rien.
- **Commentaire de `runners-epingles.py`** : exact. « mêmes chaînes acceptées que la forme `(?:[&!]\S*\s*)*` » est
  prouvé (§2.1 et §2.2, paire « sous-motif du commentaire »). « aucun découpage ambigu d'un mot, donc aucun retour
  arrière exponentiel » est confirmé (§3).
- **Commentaire de `gates.yml`** : exact (un test, Ran 36 → 37 mesuré ; plancher 37). La date 2026-10-10 est le jour
  `date -u` de son écriture : le diff a été écrit à 2026-10-10 02:41:17 UTC (mtime), et mon `date -u` de départ donne
  02:41:49 UTC.
- **Docstring du test** : inexacte pour v3, qui n'est pas une valeur « puis d'un mot qui n'est ni ancre ni étiquette »,
  et sur laquelle l'ancienne forme ne fait aucun retour arrière exponentiel. Elle est aussi inexacte pour v2, faite de
  `&` et non de `!` (C-1).
- **`scripts/controle/README.md`**, hors du diff, est rendu faux par lui. L.65-67 disent « 10 tests » et « plancher du
  job `controle-unittest` 36 » ; après DT5-24, le fichier compte 11 tests et le plancher vaut 37 (C-2).

## 7. Corrections (liste fermée)

Forme exacte complète : `g2/corrections-C1-C3.diff` (sha256 `4072efdb…`, voir SHA256SUMS).

- Il s'applique par `git apply` sur `ba5ea95` plus DT5-24 (contrôlé par `--check`, puis appliqué).
- Le résultat est identique, à l'octet, à ma copie de validation `corrige2`, à l'horodatage près.
- Le seul gabarit est `AAAA-MM-JJ hh:mm:ss` (C-2), à remplacer par `date -u` au moment de l'écriture.

**C-1. `scripts/controle/tests/test_runners_epingles.py`, `test_valeur_adverse_en_temps_borne`.**

- **Constat** : la 3e valeur `"!" * 5000 + "|x"` est inerte (§4.2), et la docstring est inexacte.
- **Forme exacte** : remplacer les trois lignes

```
        """Alerte CodeQL de la PR n° 11 : une valeur faite de « ! » en grand nombre puis d'un mot qui n'est ni ancre ni
        étiquette se juge en temps borné (l'ancienne forme de VIDE et BLOC y faisait un retour arrière exponentiel)."""
        for valeur in ("!" * 5000 + "x b", "&" * 5000 + " b", "!" * 5000 + "|x"):
```

par

```
        """Alerte CodeQL de la PR n° 11 : une valeur faite de « ! » ou de « & » en grand nombre puis d'un mot qui n'est
        ni ancre ni étiquette (en-tête de bloc invalide compris) se juge en temps borné (l'ancienne forme de VIDE et de
        BLOC y faisait un retour arrière exponentiel)."""
        for valeur in ("!" * 5000 + "x b", "&" * 5000 + " b", "!" * 5000 + " |x"):
```

- **Effet mesuré** : la nouvelle 3e valeur (v4 du §4.2) atteint BLOC par l'en-tête invalide `|x`. Elle est jugée en
  0,03 s par le code corrigé, et atteint la borne de 20 s sous l'ancienne VIDE seule, sous l'ancienne BLOC seule et sous
  les deux.

**C-2. `scripts/controle/README.md`.**

- **Constat** : compte de tests et plancher périmés.
- **Forme exacte** : ajouter à la fin du fichier, après la ligne « > refusées dans le même job par
  `enforcement/workflows-yaml.py`, après lecture YAML (relecture G2, C-8). », une ligne vide puis

```
> *Ajout daté du AAAA-MM-JJ hh:mm:ss UTC (`date -u` ; correctif DT5-24, alerte CodeQL de la PR n° 11 ; relecture G2,
> C-2)* : VIDE et BLOC de `enforcement/runners-epingles.py` réécrits sans retour arrière exponentiel, mêmes chaînes
> acceptées ; `tests/test_runners_epingles.py` compte 11 tests (un test de temps borné sur des valeurs adverses ;
> `test_formes_hors_ligne` étendu, relecture G2 C-3), plancher du job `controle-unittest` 37 ; le compte de 10 tests et
> le plancher 36 de l'ajout du 2026-10-09 22:24:59 UTC précèdent ce correctif.
```

- **Remarques** :
  - L'horodatage est celui de `date -u` à l'écriture.
  - Si C-3 n'était pas retenue à l'adjudication, il faudrait retirer « ; `test_formes_hors_ligne` étendu, relecture G2
    C-3 ».
  - Les lignes de cette forme font 116, 115, 113, 119 et 78 caractères.

**C-3. Même fichier de test, `test_formes_hors_ligne`.**

- **Constat** : sept mutants non équivalents vivants (§4.3), dont M10, perte créée par la réécriture.
- **Forme exacte** :
  - dans la docstring, remplacer `        suite de flux."""` par les deux lignes

```
        suite de flux. Relecture G2 du correctif DT5-24 (C-3) : étiquette puis ancre suivies d'un commentaire ;
        étiquette `!` suivie d'une ancre, puis seule ; ancre puis en-tête de bloc suivis d'un commentaire."""
```

  - dans la liste, remplacer `            "      windows-latest", "    include: [os: macos-latest]", ""]),` par

```
            "      windows-latest", "    include: [os: macos-latest]",
            "    runs-on: !!str &a  # étiquette, ancre, commentaire", "      ubuntu-latest", "    runs-on: ! &a",
            "      windows-latest", "    runs-on: !", "      macos-latest",
            "    runs-on: &a >-  # en-tête, commentaire", "      ubuntu-latest", ""]),
```

  - dans les refus attendus, remplacer `             "23 : macos-latest"])` par

```
             "23 : macos-latest", "25 : ubuntu-latest", "27 : windows-latest", "29 : macos-latest",
             "31 : ubuntu-latest"])
```

- **Effet** : le compte de tests ne change pas (37), ni le plancher, ni le commentaire de `gates.yml`. Les quatre formes
  sont du YAML valide et ne sont lues que par VIDE ou par BLOC ; chaque clé est au retrait 4, hors du bloc de la
  précédente.

**Validation de C-1 à C-3** (copies `corrige` et `corrige2`) :

| contrôle | résultat |
|---|---|
| ligne du job sur `corrige2` (forme finale) | sortie 0, « Ran 37 tests in 4.804s », OK, conforme |
| étape 1 sur `corrige2` | 137 ok |
| campagne complète de 28 mutants sur `corrige` | **27 tués, 1 vivant (M16, équivalent), 0 FATAL** ; témoins en sortie 0 ; M10, M13, M14, M15, M17, M22 et M26 tués par `test_formes_hors_ligne` |
| `test_formes_hors_ligne` corrigé, sur le code de `ba5ea95` (`base-c3`) | OK |

`corrige` et `corrige2` ne diffèrent que par deux lignes de docstring de C-3 (rédaction affinée, E-5) : le code des
tests est identique. Le dernier contrôle montre que les cas de C-3 épinglent le langage commun aux deux formes et non un
comportement nouveau.

## 8. Observations et items à former (non bloquants)

- **O-1, fermeture de l'alerte sur la forge.** CodeQL ne se lance pas ici. Après la poussée du correctif, il faut
  constater que le contrôle CodeQL de la PR n° 11 est vert, ou que l'alerte de la l.26 est close, et qu'aucune alerte
  nouvelle n'apparaît aux l.27-28, où VIDE et BLOC se trouvent après le correctif. Item pour l'orchestrateur.
- **O-2, enregistrement du rôle G2 (SHOGEN-G2-ENREG-ROLE-1)** : non retenue par l'orchestrateur ; enregistrement
  fait au §12. Texte d'origine : à ma lecture, il ne s'applique pas. Ce lot est un
  correctif de contrôle CI (images de runner). Il n'appartient pas au dossier de S2 soumis au cp-2, clos le 2026-10-04
  (`docs/adr-0028/CP2-S2.md` l.1-60, [lu]). Je n'ai donc produit aucun enregistrement. À confirmer par l'orchestrateur :
  s'il en juge autrement, l'enregistrement se fait à `612b19d` (ou à la base retenue), avec l'empreinte des diffs relus
  `97cc54ee…`.
- **O-3, optionnel de BLOC.** Il est redondant pour la décision du script (M16 équivalent) et nécessaire à l'égalité
  exacte que revendique le commentaire. Aucune action.
- **O-4, écart de versions de Python.** Mesures et suite tournent sous Python 3.11.15 ; la CI tourne sous 3.12 [inféré].
  La preuve par automates ne dépend pas du moteur ; la contre-épreuve sur le moteur et les mesures, si.
- **O-5, limite rencontrée hors du diff (PAROXYSME).** `FLOTTANT`, inchangé par DT5-24, est quadratique en `findall` sur
  une longue suite de caractères de libellé sans `-latest` : ×4 par doublement,
  4,7 s pour 32 000 `a` et 2,1 s pour 16 000 `-` (`sorties/flottant.out`).
  - L'entrée vient des workflows du dépôt.
  - CodeQL py/redos ne le voit pas, puisque ce n'est pas exponentiel, et py/polynomial-redos non plus, faute de source
    distante [inféré].
  - Item proposé : « SHOGEN-RUNNERS-FLOTTANT-QUADRATIQUE-1 », borner la longueur lue ou ancrer le motif. Non requis par
    ce lot.
- **O-6, coût d'une régression.** Une régression vers une forme exponentielle coûte 20 s au job (borne du test, mesuré
  23,4 à 26,0 s par run de la suite), dans la limite `timeout-minutes: 10`.

## 9. Écarts

- **E-1.** Une commande qui passait par `sh -c` a été refusée par la garde de sécurité du harnais et n'a pas été lancée.
  Je l'ai remplacée par deux commandes séparées ; aucun effet sur les résultats.
- **E-2, exposition.** En découvrant le dossier, j'ai listé jusqu'à 50 chemins de `a/`, `b/` et `g/`, l'espace de
  l'auteur, dont `a/.git/…` (commande `find a b g -maxdepth 6`, sortie coupée à 50 lignes). Seuls des noms sont
  apparus, et je n'ai lu ni utilisé aucun contenu.
- **E-3.** Le point d'API des alertes code-scanning a répondu 403. J'ai lu à la place l'annotation du run CodeQL (§3.4).
- **E-4.** `mutants.py` a reçu un filtre facultatif après le premier passage de la campagne ; la sha256 de la version
  initiale n'a pas été relevée. La campagne complète a été relancée avec la version finale (`82150c33…`). Son classement
  est identique, mutant par mutant, à celui du premier passage, et c'est elle qui fait foi au §4.3.
- **E-5.** La rédaction de la docstring de C-3 a été affinée après la campagne sur `corrige`. Le garde de longueur de
  `corrections.py` a aussi arrêté trois premiers jets, à 121, 122 et 121 caractères, avant toute écriture. Le code des
  tests est le même dans `corrige` et `corrige2`, et la forme finale est revalidée (§7).
- **E-6.** La tête du dépôt a avancé pendant la relecture (6e01772 → 612b19d, commits de l'orchestrateur). Les quatre
  fichiers en jeu sont inchangés depuis `ba5ea95`, et DT5-24 s'applique et reste vert sur 612b19d (§5).
- **E-7.** Les outils d'analyse pure (`automate`, `moteur`, `redos`, `decision`, `valeurs_test`, mesure de `FLOTTANT`)
  ont tourné en `python3 -I -B` hors de `isole.sh`. Ils n'utilisent pas le réseau, et la variable S2 est absente de mon
  environnement.

## 10. Journal de provenance (G1)

**Sources lues :**

- [lu] `CLAUDE.md` (contexte de la session) ;
- [lu] `DT5-24.diff`, en entier ;
- [lu] `equivalence.py`, en entier ;
- [lu] à `ba5ea95` : `enforcement/runners-epingles.py` (122 l.) et `scripts/controle/tests/test_runners_epingles.py`
  (124 l.), en entier ;
- [lu] `gates.yml` l.110-160 et l.325-359 ;
- [lu] `enforcement/verdict-suite-s2.py`, en entier ;
- [lu] `enforcement/tests/run-fixtures-verdict-suite-s2.py` l.540-630 et des lignes éparses entre l.6 et l.623, trouvées
  par grep sur `controle`, `plancher`, `gates.yml` et `K-0` ;
- [lu] `enforcement/workflows-yaml.py` l.1-22 ;
- [lu] `scripts/controle/README.md` l.22-34 et l.36-68 ;
- [lu] `scripts/controle/SHA256SUMS`, qui ne couvre pas `tests/` ;
- [lu] `s2-harness/tools/README.md` l.1-31 ;
- [lu] `docs/adr-0028/CP2-S2.md` l.1-60 ;
- [lu] `isole.sh` et `lo_up.py` ;
- [lu] run CodeQL 114111040759 et son annotation (API GitHub, lecture seule) ;
- [2nd] le critère de la règle py/redos et le résultat de Weber et Seidl : connaissance du relecteur, non relue ici.

**Commandes et sorties :** toutes sont consignées dans `g2/sorties/`. Les plus importantes :

- `date -u` ;
- `git rev-parse` et `git merge-base` ;
- `sha256sum` des pièces ;
- `git archive` puis `git apply` ;
- `lancer.sh`, et le contrôle d'isolement ;
- le job en deux étapes : `job-etape1.out`, `job-etape2.out` ;
- `scripts-copie-base.out` ;
- `automate.out` ;
- `moteur.out` ;
- `redos.out` ;
- `valeurs_test.out` ;
- `rouge-test-seul.out`, `rouge-job.out` et `base-job-36.out` ;
- `mutants.out` et `mutants.json` (premier passage), `mutants-final.*` (campagne de référence), `mutants-corrige.*` ;
- `mutants-anciens.*` ;
- `decision.out` ;
- `corrige-job.out`, `corrige2-job.out` et `corrige2-etape1.out` ;
- `base-c3-formes.out` ;
- `tete-job.out` et `tete-etape1.out` ;
- `flottant.out`.

**Chiffres recomptés :** tous les chiffres de ce rapport viennent de ces sorties. Aucun n'est repris du brief ni de
l'auteur, sauf le texte de l'alerte, que j'ai relu sur la forge.

## 11. Fichiers produits

- `g2/RAPPORT-G2.md` : ce rapport.
- `g2/SHA256SUMS` : sommes du rapport, du diff de corrections, des outils et des sorties.
- `g2/corrections-C1-C3.diff` : forme exacte de C-1 à C-3.
- `g2/outils/` : `motifs.py`, `automate.py`, `moteur.py`, `redos.py`, `valeurs_test.py`, `mutants.py`,
  `mutants_anciens.py`, `decision.py`, `corrections.py` et `lancer.sh`.
- `g2/sorties/` : les sorties des commandes.
- `g2/shogen-ba5ea95-G2-20261010T033744Z-15258.json` et `g2/shogen-ba5ea95-G2-20261010T033744Z-15258.0-suite.out` :
  enregistrement du rôle G2 et sortie de son run (§12).
- Les copies de travail ne sont pas sommées. `base`, `copie`, `corrige2` et `variantes` restent sur disque. `rouge`,
  `mut`, `mut-corrige`, `mut-base`, `corrige`, `base-c3`, `tete` et `verif-diff` ont été supprimées après usage pour
  libérer le disque partagé (81 % occupé) ; elles se refont par `git archive`, DT5-24 et `corrections-C1-C3.diff`.

## 12. Enregistrement du rôle G2 (ajout daté du 2026-10-10 03:39:48 UTC, `date -u`)

Demande de l'orchestrateur, reçue après la remise du rapport : O-2 n'est pas retenue. La G2 du lot DETTES-T5 a
enregistré son rôle (`shogen-c1122de-G2-20261009T220715Z-28656.json`, B.92), et DT5-24 est un correctif de ce même lot.
J'applique donc la règle du bloc de gabarit de `.claude/agents/shogen-worker.md` (l.78-89, [lu]).

**Arbre de l'outil.**

- `git archive ba5ea95`, extrait dans `g2/enreg-outil`.
- sha256 de son `enforcement/verdict-suite-s2.py` :
  `120782608370db88d40d1fb39390aed9de7143d596a21e7efb419cc88b275980` ; de `s2-harness/tools/oracle_record.py` :
  `4d0e4503fc8552e0345e631866d4bf0e3a680808abbb031c86af9e3b275ee13e`.
- Revue qui a relu ce vérificateur (règle 4 de `s2-harness/tools/README.md`) : sa dernière modification avant `ba5ea95`
  est `ada4737` (DETTES-T5 DT5-21), dont le message, [lu], dit « G2 neuve, corrections C-1 a C-11, contre-controle
  CONFORME en trois passes ». Je l'ai en outre lu en entier dans cette relecture (§10).
- Règle 2 du même README : l'outil a tourné depuis l'arbre du commit enregistré. La comparaison des vérificateurs
  (OUT-1b) n'a pas d'objet ici, puisque seule la commande `suite` a tourné, par l'AMORCE du vérificateur.

**Dépôt (`--depot`) et écart à la lettre de la demande.**

- `oracle_record.py` lit le commit par `git -C <depot> rev-parse` puis par `git archive` (l.81-89 et 213-216). Une
  extraction `git archive` n'est pas un dépôt git : `--depot <copie git archive>` ne peut pas s'exécuter.
- Ma copie de dépôt est donc un clone local sans extraction :
  `git clone --no-hardlinks --no-checkout /home/user/shogen g2/enreg-depot`, en lecture seule sur l'original. C'est la
  forme qu'a employée le validateur du cp-2 (`docs/adr-0028/CP2-S2.md` l.26-27).

**Écriture.**

- Lancement le 2026-10-10 de 03:37:44 à 03:38:34 UTC.
- Répertoire courant : l'arbre de l'outil. Environnement par `lancer.sh` :
  - `env -u SHOGEN_S2_CAMPAGNE_CONTROL` et `-u` des variables de mandataire ;
  - `PYTHONDONTWRITEBYTECODE=1` et `TMPDIR=g2/tmp` ;
  - `isole.sh` : réseau coupé.
- Commande : `python3 -B s2-harness/tools/oracle_record.py --role G2 --commit ba5ea95 --auteur claude-opus-5-5 --depot
  g2/enreg-depot --sortie g2`, sortie **0**.
- Enregistrement : `g2/shogen-ba5ea95-G2-20261010T033744Z-15258.json`, sha256
  **`cb8872c1f4b2656d04b78125b2fc0a9cac4b3ed31fb27968dd75a97db58b2777`**.
- Contenu de l'enregistrement :
  - `schema` `shogen.oracle-record.v1`, `role` G2, `auteur` `claude-opus-5-5` ;
  - `tree.commit` `ba5ea95709e122349448c5e3f024b0ca08d83e91` (`git archive`), 1 141 fichiers hachés ;
  - `static_only` false, `served_from` et `base` nuls ; `paquet.sha256` et `sceau.genTime` nuls ;
  - `env` : SHOGEN_S2_CAMPAGNE_CONTROL, PYTHONHASHSEED et PYTHONPATH nuls ;
  - Python 3.11.15, écrit à 2026-10-10T03:37:44Z, `exit` 0.
- Run `suite` (s2-harness, AMORCE) : exit 0.
  - Sortie `g2/shogen-ba5ea95-G2-20261010T033744Z-15258.0-suite.out`, sha256
    `bc1621c0c9105d17a933c92929a5f301124869fe6a6cd056d60cafc90f7dc2be`.
  - « Ran 419 tests in 47.325s », « OK (skipped=2) » : les deux sauts nomment SHOGEN_S2_CAMPAGNE_CONTROL. 419 est le
    PLANCHER du vérificateur à `ba5ea95`. `tests_avec_variable` est vide.

**Vérification** (03:38:54 à 03:38:56 UTC, même arbre, même environnement).

- Commande : `python3 -B s2-harness/tools/oracle_record.py --verifier g2/shogen-ba5ea95-G2-20261010T033744Z-15258.json
  --role G2 --commit ba5ea95709e122349448c5e3f024b0ca08d83e91 --depot g2/enreg-depot`.
- Sortie **0** : « conforme : … (rôle G2, tree.commit ba5ea95709e122349448c5e3f024b0ca08d83e91 ; tree.sha256 recalculé
  sur …/g2/enreg-depot) » (`sorties/verification.out`).

**Empreinte des diffs relus, dans l'ordre de la série.**

- `DT5-24.diff` : sha256 `97cc54ee3777bf9c22dc24ea1e3bb5ec7537b984030d61c06259233e81092ac6`, 3 532 octets.
- `corrections-C1-C3.diff` : sha256 `4072efdbe184ae8a0cb076f25adaf6dbdc18b2347bf6e6094f16fc1c9154209b`, 4 655 octets ;
  l'horodatage de C-2 y est sous le gabarit `AAAA-MM-JJ hh:mm:ss`.
- sha256 de leur concaténation (8 187 octets) :
  **`fc2c2269823fee44fbfa804feca64b8641d9789219eafc62aed5a91d2028713d`**.
- Le diff qui sera appliqué, avec la date posée par l'orchestrateur, différera du diff relu par ces seuls 19 caractères.

**Portée.** L'enregistrement atteste la base `ba5ea95` et la suite s2-harness lancée sur elle, non les diffs. Il se
vérifie à `ba5ea95`, et seul ce rapport le relie aux diffs, par l'empreinte ci-dessus. Les fichiers de DT5-24 et des
corrections sont hors de `s2-harness` : la suite enregistrée ne les exerce pas, c'est le job `controle-unittest` qui le
fait (§5 et §7).

**Copies.** `g2/enreg-outil` et `g2/enreg-depot` sont supprimées après la mise à jour de `SHA256SUMS`.
