# Rapport des corrections — PLAN-S2BIS-2, après la G2 (transcrit)

> Transcription par l'orchestrateur le 2026-10-08 14:15:22 UTC du rapport écrit par le worker de correction (agent a059a9ec1498192e1) dans `<scratchpad>/s2bis/plan2/corr/RAPPORT-CORRECTIONS.md` (sha256 26a756a1…), dont le résumé a été rendu par message ; contrôle FM-1.1 : fragments_l51_l14 = 0 ; modèle résolu au transcript : claude-opus-5-5. Texte du worker ci-dessous, sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Rapport — corrections du lot PLAN-S2BIS-2 après la G2 (C-1 à C-4, Q-P2R-3, REFUS-NON-NOMMES-1)

- **Gate 0** : modèle résolu `claude-opus-5-5` (worker `shogen-worker`, effort max). Je n'avais écrit ni relu aucun diff
  de ce lot avant cette passe.
- **Horloge** (`date -u`) : début le 2026-10-08 à 13:00:27 UTC ; fin à 14:13 UTC (clôture, §12).
- **Base** : tête `e6657dcc3154bf2d35c69b84d9deae1385e702a7` (`claude/compassionate-noether-szmdyj`), égale à celle du
  brief, relevée au début et avant ce rapport ; `git status --short` vide aux deux relevés.
- **Brief** : `corr/BRIEF-CORR-P2R.md` (sha256 `785b18cc…4aec`, 23 lignes), lu en entier et exécuté point par point ;
  brief de génération `code/BRIEF-P2R.md` (règles et interdits toujours en vigueur), lu en entier.
- Dossier : `<scratchpad>/s2bis/plan2/corr/` ; `TMPDIR` dédié `corr/tmp` (retiré à la clôture) ; `NOTES.md` tenu.

## 1. Résumé

1. **Livré** : 11 diffs en série sur e6657dc, chacun ≤ 200 lignes ajoutées : les 9 d'origine sous leurs noms (7
   corrigés en place, P2R-1a et P2R-1b inchangés dans leurs lignes), plus **P2R-6a** et **P2R-6b**. Une correction qui
   ne trouvait pas sa place (Q-P2R-3 et REFUS-NON-NOMMES-1 en P2R-1a : 101 lignes pour 71 de marge ; C-3 c en P2R-1b,
   déjà à 200 ; C-1 en P2R-5, à 196) va au diff neuf P2R-6 ; P2R-6 passait alors 200 lignes : **règle de coupe du §1**
   appliquée et déclarée (6a : C-1 et C-4 ; 6b : Q-P2R-3, REFUS-NON-NOMMES-1, C-3 c), chaque moitié avec ses tests.
2. **Épingle neuve** : sha256 de `scripts/plan-s2bis-2/SHA256SUMS` =
   **`fe46ebd62195d5d78e58163985e46a2691cefe9af9898c3c8e1257d8cad8f36f`** (12 lignes, `sha256sum -c` 12/12). L'ancienne
   (`a8bb826d…0e08`) ne vaut plus.
3. **Suite du lot** : 34 tests (28 + 6), verte sous 3.11, 3.12, 3.13 × `PYTHONHASHSEED` 0 et 1, en `-X dev -W error`,
   0 ligne d'avertissement ; 3.10 : échec d'import connu (`hashlib.file_digest`, PY310-1). DET-1 vert. Les 11
   instantanés sont verts : 2, 6, 7, 11, 14, 18, 20, 23, 28, 31, 34.
4. **Mutants** : G2 rejouée sur l'état final : 26 tués sur 27, **les 8 vivants tués** (G-03, G-10, G-14 adapté, G-18,
   G-19, G-21, G-23, G-26), G-05 équivalent (démonstration du réviseur vérifiée, §5) ; 36 mutants neufs, tous tués ; les
   71 du générateur rejoués, tous tués. 0 FATAL.
5. **Bout en bout sur fixtures** (vrais scripts, dépôt jetable) : S8, S9, S22 fermés ; une fenêtre hors grille sort en
   P2/lecture, code 5, `lancer.log` vide, aucune valeur de journal ; avant correction, 4 à 6 exécutions étrangères en
   code 0 et la valeur hors grille dans `lancer.log` (2 349 octets).
6. **xtask** : S-G1 à S-G8 VERT ; S-G9 ROUGE, 1 violation (`docs/17-modele-de-menace.md:70`, connue) ; fmt, no_std,
   clippy VERT ; verdict global ROUGE par S-G9 seule (identique à la G2).

## 2. Diffs

Dans `corr/diffs/`, à appliquer dans l'ordre (`git apply`) ; appliqués en série sur une copie `git archive` de e6657dc
avec `--check` puis `--whitespace=error-all`, sans retouche : chaque état est égal (diff -r) à `corr/snap/P2R-x`.
0 octet 92, 0 tabulation, 0 retour chariot, 0 ligne de plus de 120 caractères, 0 TODO ni FIXME dans les lignes ajoutées.

| diff | contenu | + / − | tests | sha256 |
|---|---|---|---|---|
| P2R-0a | origine ; C-3 b (SOC-5 : booléen dans `calendrier_hors_d5`) | +179 / −0 | 2 | `e01d5a8e1be82c5c34aa4f6f0efc5c4d429ede90c08fb1d35e5b67ef6c64ea4e` |
| P2R-0b | origine ; C-3 a (SOC-4 : liste de même longueur, `pas_ecart`) | +168 / −0 | 6 | `c239a4fb4194ede5882831b77d3ffea05046e35653e9cb6318983ae43d50498e` |
| P2R-1a | origine ; lignes +/− identiques, contexte décalé par 0a et 0b | +129 / −0 | 7 | `d9d008d399420225a4d27444d127545a8f1d2dcd2aa2b884b3654b993527365a` |
| P2R-1b | origine, identique octet pour octet | +200 / −0 | 11 | `d8210e5de41a3966ab584cb83e8e38ea2901e3e39ab3c6a716f11db96c39835b` |
| P2R-2 | origine ; C-2 (FIV-5 : chiffre de σ̂²_bloc à ℓ = 3 ; ligne D1-bis de plus) | +166 / −11 | 14 | `6e01ef1f196c805e2da339a3795b6dd593533b45647fc85100efa1c330b53467` |
| P2R-3 | origine ; C-2 (EPI-2 : entrée de plus, deux lignes) | +176 / −0 | 18 | `08f583965bb6f452b248953699795f2ffb22d145ef8b197372d95adf81655d48` |
| P2R-4a | origine ; C-3 d (LAN-6 : sortie à entrée cachée seule) | +174 / −0 | 20 | `3fd7797067327f36c04e13985e24132e7b8fe232f7cf6547ad9da04cd11f837a` |
| P2R-4b | origine ; C-3 e (LAN-5 : journal nommé « .cache.jsonl », présent, sha256 égal) | +91 / −0 | 23 | `b38b2e7b896728d88e6de8c7e60433b566c63b4fec4fa311fde5e85ca3716a58` |
| P2R-5 | origine ; `SHA256SUMS` recalculé sur l'état corrigé | +196 / −6 | 28 | `1fa876896045eea4e2d7d35acd8b13e5f2a5807ea8c291eb56aabe071a1e7e3f` |
| P2R-6a | C-1 a à d, C-4, règle au README ; `SHA256SUMS` | +132 / −37 | 31 | `23ef1e17ba60c1844fabe9dabb4f90d1aa06ac1b2b2d26ddd0eee94a65ce15ed` |
| P2R-6b | Q-P2R-3, REFUS-NON-NOMMES-1 (scripts et lanceur), C-3 c ; `SHA256SUMS` | +184 / −40 | 34 | `8b9660a9e0ff4c88bc4e2b2978dee17f1ba8043efb41710f18504fea7242d2f6` |

- Total 1 795 lignes ajoutées, 94 retirées : lot final de 1 701 lignes (13 fichiers), contre 1 425 avant la G2.
- Fichiers touchés par 6a : `lancer.sh`, `tests/test_lancer.py`, `README.md`, `SHA256SUMS` ; par 6b : `socle.py`,
  `masque_fiv.py`, `lancer.sh`, `tests/test_socle.py`, `tests/test_masque_fiv.py`, `tests/test_lancer.py`, `README.md`,
  `SHA256SUMS`. `parametres.json`, `intervalles.py`, `tests/__init__.py`, `tests/test_identite.py` : inchangés depuis
  l'origine. `scripts/plan-s2bis/` n'est jamais touché.
- sha256 des fichiers finaux (`SHA256SUMS` du lot) : `README.md` d77a28a0… ; `intervalles.py` a684d113… ; `lancer.sh`
  0293fdeb… ; `masque_fiv.py` d48d1422… ; `parametres.json` 7a6a7112… ; `socle.py` 21e6ebb7… ; `tests/__init__.py`
  834e6661… ; `tests/test_identite.py` a14a4ea8… ; `tests/test_intervalles.py` 8abb8319… ; `tests/test_lancer.py`
  d92c6526… ; `tests/test_masque_fiv.py` 14bb3d13… ; `tests/test_socle.py` 3fc14a3d… (fichier complet :
  `corr/snap/P2R-6b/scripts/plan-s2bis-2/SHA256SUMS`).

## 3. Corrections C-1 à C-4

Chaque test neuf a d'abord été vu rouge, par échec d'assertion (journaux `corr/journal/rouge-*`) : contre le code
d'avant quand le code change (C-1, C-3 c, Q-P2R-3) ; contre le mutant vivant de la G2 et mes mutants neufs quand seul le
test change (C-2, C-3 a, b, d, e : le code était juste). Ces mutants ont aussi été passés contre les tests d'origine,
où ils vivaient tous (`vivants-avant-*`).

| C | défaut (G2) | correction | où | test (rouge montré) | mutants tués |
|---|---|---|---|---|---|
| C-1 a | heredocs en `python3 -B -` : dossier courant et `PYTHON*` lus | `python3 -I -B -` pour les deux lectures de `parametres.json` | `lancer.sh`, P2R-6a | LAN-11 (S9) : rouge `(0, True, 4)` | M-P2R6-4, M-P2R6-5 |
| C-1 b | scripts sous l'environnement hérité ; bytecode voisin lu malgré `-B` | `env -i` avec PATH, LC_ALL, PYTHONHASHSEED de la passe, PYTHONDONTWRITEBYTECODE, PYTHONPYCACHEPREFIX vers `<travail>/pyc` (absolu) ; `<travail>/pyc` exigé absent (P2/sortie), puis créé | `lancer.sh`, P2R-6a | LAN-11 (S9) ; LAN-12 (S22, PLAN-S2BIS) ; LAN-6 fin (pyc déjà présent) : rouges `(0, True, 4)`, `(0, '', True)`, code 0 au lieu de 3 | M-P2R6-6, M-P2R6-7, M-P2R6-9 |
| C-1 c | entrée hors `SHA256SUMS` dans le dossier du lot exécutée | P2/epingle, code 3, si une entrée qui n'est pas un dossier, hors `SHA256SUMS` lui-même, n'est pas listée (`find`, sous-dossiers et noms cachés compris, `__pycache__` compris) | `lancer.sh`, P2R-6a | LAN-10 (S8 : `json.py`, `sous/.cache`) ; LAN-12 (S22, lot) : rouges `(0, '', True)` | M-P2R6-1, M-P2R6-2, M-P2R6-3, M-P2R6-8 |
| C-1 d | tests absents ; faux scripts lisant `FAUX_*` dans l'environnement | un test par vecteur (LAN-10, LAN-11, LAN-12) ; canal neuf : clé `faux` du `parametres.json` du lot (code par script, dépendance à la graine, écriture), lue par un faux `socle.py` qui charge aussi `commun` de PLAN-S2BIS par `spec_from_file_location` (forme de `socle.charger_module`) ; bytecode forgé par le `python3` du lanceur ; règle au README (Lancement, point 2) | `tests/test_lancer.py`, `README.md`, P2R-6a | ci-dessus ; LAN-7 et LAN-8 passent par le canal neuf | — |
| C-2 | (e) et (f) : chaînes et comptes de lignes non figés | FIV-5 : EP au dernier chiffre de σ̂²_bloc changé (ligne D1-bis, ℓ = 3) ; EP à une ligne D1-bis de plus. EPI-2 : EP à une entrée de plus (deux lignes). P2/ep, aucune valeur | `tests/test_masque_fiv.py` (P2R-2), `tests/test_intervalles.py` (P2R-3) | FIV-5, EPI-2 : rouges `0 != 1` | G-18, G-19, M-P2R2-4, M-P2R2-5 ; G-21, M-P2R3-4, M-P2R3-5 |
| C-3 a | (d) comparé par longueur | SOC-4 : liste `panne, pas_ecart, hors_enveloppe` : P2/ecarts | `tests/test_socle.py`, P2R-0b | SOC-4 : `Refus not raised` | G-03, M-P2R0-11, M-P2R0-12 |
| C-3 b | booléen admis dans les comptes | SOC-5 : `calendrier_hors_d5.calme = true` : P2/parametres | `tests/test_socle.py`, P2R-0a | SOC-5 : `Refus not raised` | G-10, M-P2R0-9, M-P2R0-10 |
| C-3 c | (b) par l'union des clés : strate manquante dans un seul dictionnaire, puis `KeyError` non nommée (Q-P2R-9) | chacun des deux comptes attendus doit porter exactement les strates de PLAN-S2BIS, sinon P2/masque ; MAS-3 : deux cas (un dictionnaire sans la strate) | `masque_fiv.py`, `tests/test_masque_fiv.py`, P2R-6b | MAS-3 : `'KeyError' != 'P2/masque'` | G-14 (adapté), M-P2R6-16, M-P2R6-17 |
| C-3 d | `ls -A` non éprouvé | LAN-6 : sortie ne contenant que `.cache` : P2/sortie | `tests/test_lancer.py`, P2R-4a | LAN-6 : `(5, 'REFUS P2/usage', …)` au lieu de P2/sortie | G-23, M-P2R4-9, M-P2R4-10 |
| C-3 e | nom de journal en « . » non éprouvé | LAN-5 : ligne de bloc `journal .cache.jsonl <sha256 égal>`, fichier présent : `REFUS P2/journal : nom de journal refusé` | `tests/test_lancer.py`, P2R-4b | LAN-5 : code 5 au lieu de 3 | G-26, M-P2R4-11, M-P2R4-12 |
| C-4 | commentaire d'ordre contraire au code | commentaire réécrit sur l'ordre du code, dans le même diff que C-1 (P2R-6a) : les sept autres pièces au point 3, juste après le `parametres.json` de PLAN-S2BIS et avant le paquet et le commit ; contrôles neufs nommés (entrées hors `SHA256SUMS`, cache de bytecode, liste fermée) ; codes complétés en 6b | `lancer.sh` l.6-28 | relu ligne à ligne contre le code | sans objet (commentaire) |

## 4. Q-P2R-3 et SHOGEN-PLAN-S2BIS-2-REFUS-NON-NOMMES-1 (fermé dans ce lot, P2R-6b)

**Choix et motif du code de sortie.** P2/lecture est un refus de script : code 1, en-tête et une ligne de refus dans
chaque sortie, comme tout refus de script au §4 ; le lanceur sort alors en 5 (« un script hors 0 »), passe B non
commencée (P-7), rien dans `<sortie>`. Aucun code neuf n'est ajouté à la liste des codes du §4.

**Scripts** (`socle.executer`) : après les arguments, toute exception qui n'est pas un refus nommé devient
`REFUS P2/lecture : lecture ou traitement en échec (<Type>)` ; le message de l'exception n'est jamais recopié. Le
script n'écrit rien sur stderr en refus, donc rien dans `lancer.log` (hors les deux avertissements propres du harnais,
item TRACE-HARNAIS-1 du §8) ; un refus nommé garde son code. Arguments hors CLI :
`REFUS P2/usage` sur stderr, code 2 (aide retirée) ; sorties non écrites : `REFUS P2/sortie` sur stderr, code 1.

| chemin de sortie | refus | test (un cas par chemin) | mutants |
|---|---|---|---|
| journal absent (FileNotFoundError) | P2/lecture | LEC-1 cas 0 | M-P2R1-11 (Refus et ValueError seuls rattrapés) |
| ligne JSON corrompue non finale (ValueError) | P2/lecture | LEC-1 cas 1 | M-P2R1-12 (message recopié) |
| ligne non objet (AttributeError) | P2/lecture | LEC-1 cas 2 | M-P2R1-11 |
| **fenêtre hors grille** (ValueError de `r1.block_long_run_variance`, message portant la valeur) | P2/lecture, valeur absente des sorties et de stderr | LEC-1 cas 3 | M-P2R1-12 |
| strate journalisée incohérente (ValueError) | P2/lecture | LEC-1 cas 4 | — |
| strate hors `parametres.json` (ValueError) | P2/lecture | LEC-1 cas 5 | — |
| unité D1-bis hors du pool journalisé (ValueError) | P2/lecture | LEC-1 cas 6 | — |
| classe divergente (ValueError) | P2/lecture | LEC-1 cas 7 | — |
| rendu J28 absent (FileNotFoundError) | P2/lecture | LEC-1 cas 8 | M-P2R1-11 |
| prix illisible (InvalidOperation) | P2/lecture | LEC-1 cas 9 | M-P2R1-11 |
| lecture sans flux (KeyError) | P2/lecture | LEC-1 cas 10 | M-P2R1-11 |
| exception de l'analyse, message à valeur | P2/lecture, valeur absente | LEC-1 cas 11 | M-P2R1-12 |
| refus nommé levé dans le bloc (P2/coherence, P2/pool…) | son propre code | SOC-6 | M-P2R1-13 |
| `KeyError` de `controle_b` (C-3 c) | P2/masque | MAS-3 | G-14, M-P2R6-16, M-P2R6-17 |
| `--sortie` absent, `-h`, option inconnue | P2/usage, code 2, stderr | LEC-2 | M-P2R1-14, M-P2R1-15, M-P2R1-17 |
| sorties non écrites (OSError) | P2/sortie, code 1, stderr | LEC-2 | M-P2R1-16 |

**Lanceur** : toute sortie hors 0 est nommée à l'écran (noms et codes seuls) ; aucune trace Python ni de bash.

| chemin | avant | après | test (LAN-13) | mutant |
|---|---|---|---|---|
| erreur d'un heredoc | trace Python à l'écran, puis le refus | stderr des heredocs vers `/dev/null` ; refus P2/plan-s2bis seul | `passes` absent | M-P2R6-10 |
| pièce `parametres` absente des épingles du lot | variable non liée, code 1 de bash | P2/plan-s2bis | épingle renommée | M-P2R6-15 |
| création du travail impossible | `exit 4` muet | `extraction impossible : code 4` | travail = fichier | M-P2R6-11 |
| dossier de passe impossible | `exit 5` muet | `passe A : dossier impossible : code 5` | `<travail>/A` = fichier | M-P2R6-12 |
| sommes de passe impossibles | `exit 5` muet | `passe A : SHA256SUMS impossible : code 5` | script en 0 sans sorties | M-P2R6-13 |
| copie dans la sortie impossible | `exit 5` muet | `copie de la passe A impossible : code 5` | sortie sous un fichier | M-P2R6-14 |

**Table des refus du §4, état final** (codes inchangés ; extensions de cette passe en gras) : P2/usage (lanceur ;
**scripts, code 2**) ; P2/variable ; P2/sortie (sortie non vide ; extraction **ou cache de bytecode** déjà présents ;
**scripts : sorties non écrites**) ; P2/epingle (argument ; `sha256sum -c` ; **entrée hors `SHA256SUMS`**) ;
P2/plan-s2bis (**épingles du lot illisibles, pièce `parametres` absente**) ; P2/paquet ; P2/journal ; P2/commit ;
P2/harnais ; P2/parametres ; P2/coherence ; P2/masque (**comptes attendus sans une strate**) ; P2/pool ; P2/ecarts ;
P2/ep ; **P2/lecture (neuf)** ; P2/identite ; codes 4 et 5 **nommés**.

**Bout en bout, vrais scripts** (`outils/e2e.py`, fixtures seules, dépôt jetable, `journal/e2e-*.json`) :

| scénario | origine (P2R-5 de la G2) | final (P2R-6b) |
|---|---|---|
| S0 nominal | 0 | 0, sorties égales à un lancement direct |
| S8 `json.py` dans le lot | 0, 4 exécutions étrangères | 3, P2/epingle, aucune |
| S9 ombre PYTHONPATH | 0, 6 exécutions | 0, aucune |
| S22 bytecode du lot (socle) | 0, 4 exécutions | 3, P2/epingle, aucune |
| S22 bytecode de PLAN-S2BIS (commun) | 0, 4 exécutions | 0, aucune |
| S19 chemins relatifs, graine posée à l'appel | 0 | 0 |
| L1 fenêtre hors grille | 5, `lancer.log` 2 349 octets portant la valeur | 5, P2/lecture, `lancer.log` 0 octet, valeur nulle part |

## 5. Mutants

Campagnes par la commande de la suite du lot (`outils/suite.sh`, réseau coupé), borne 300 s par mutant ; classement par
la sortie du runner : 0 VIVANT, 1 TUÉ, toute autre sortie FATAL ; une substitution par motif trouvé exactement une
fois, compilation contrôlée, restauration contrôlée par sha256, témoins verts au début et à la fin.

| campagne (état final P2R-6b) | mutants | tués | vivants | FATAL | journal |
|---|---|---|---|---|---|
| G2 rejouée (G-01 à G-27 ; G-14 adapté) | 27 | 26 | 1 : G-05, équivalent | 0 | `mutants-final-g2.json` (PID 6699) |
| neufs des corrections | 36 | 36 | 0 | 0 | `mutants-final-corr.json` (PID 20213) |
| générateur (71, M-P2R4-6 adapté) | 71 | 71 | 0 | 0 | `mutants-final-gen.json` (PID 11977) |
| **total** | **134** | **133** | **1 (équivalent)** | **0** | |

- Contrôle : la G2 rejouée sur l'état d'origine donne 18 tués et 9 vivants (G-03, G-05, G-10, G-14, G-18, G-19, G-21,
  G-23, G-26), comme au rapport de la G2 (`mutants-g2-sur-origine.json`, PID 30384).
- **G-05 équivalent**, vérifié sur le code : `commun.pool_d1bis` n'ajoute à `pools[st]` aucune unité retirée, et toute
  strate des retenues est dans `ps2["strates"]` (sinon `commun.charger` refuse) ; la comparaison du pool de
  `controle_c` refuse donc toujours avant le test des retraits.
- **Adaptations déclarées** (même sens, motif réécrit sur le code corrigé) : G-14 (« strate absente admise » :
  `set(attendu[k]) - set(strates)`) ; M-P2R4-6 du générateur (« extraction déjà présente admise » : seul le test de
  `$X` retiré).
- Neufs, au moins deux par correction : C-1 : M-P2R6-1 à 9 ; C-2 : M-P2R2-4, 5, M-P2R3-4, 5 ; C-3 a : M-P2R0-11, 12 ;
  b : M-P2R0-9, 10 ; c : M-P2R6-16, 17 ; d : M-P2R4-9, 10 ; e : M-P2R4-11, 12 ; Q-P2R-3 et REFUS-NON-NOMMES-1 :
  M-P2R1-11 à 17 (ils portent sur `executer`, fonction de P2R-1a, modifiée en P2R-6b ; d'où leur préfixe) et
  M-P2R6-10 à 15 ; C-4 : sans objet (commentaire). Chacun a été vu tuer son test à l'état de son diff
  (`rouge-P2R-*.txt`), puis rejoué sur l'état final.

## 6. Épingle neuve

- `scripts/plan-s2bis-2/SHA256SUMS` : 12 lignes, `sha256sum --strict -c` 12/12 sur l'arbre après P2R-6b.
- **sha256 = `fe46ebd62195d5d78e58163985e46a2691cefe9af9898c3c8e1257d8cad8f36f`** (à inscrire au JOURNAL par
  l'orchestrateur, E-P2-21 ; l'ancienne `a8bb826d…0e08` est caduque). Épingles intermédiaires, pour mémoire : après
  P2R-5 `893024ab…eb17`, après P2R-6a `c2b121b3…d83e`.

## 7. Questions Q-CORR (périmètre muet ou en tension ; choix et raison, aucune valeur tranchée)

- **Q-CORR-1 (place et coupe).** Q-P2R-3 et REFUS-NON-NOMMES-1 portaient P2R-1a à 230 lignes : je les ai sortis de 1a
  vers P2R-6 (lettre du brief) ; P2R-6 dépassant 200, coupe du §1 en 6a et 6b, déclarée, chaque moitié avec ses tests.
- **Q-CORR-2 (portée de P2/lecture).** `except Exception` sur tout le traitement après les arguments, le refus nommé
  gardant son code : c'est la seule forme qui tienne « aucun chemin de sortie non nommé » et « aucune valeur dans la
  trace ». Prix : un défaut du code lui-même sortirait en P2/lecture (nommé par son type, sans valeur) ; sa cause se
  cherche sur fixtures (lettre de Q-P2-08).
- **Q-CORR-3 (codes des scripts).** P2/usage (code 2, comme argparse et le lanceur) et P2/sortie (code 1) étendus aux
  scripts, sur stderr ; codes 4 et 5 du lanceur inchangés, messages `<motif> : code n`.
- **Q-CORR-4 (dossier neuf du bytecode).** `<travail>/pyc` exigé absent (P2/sortie, joint à « extraction déjà
  présente »), puis créé, plutôt qu'un nom aléatoire : la fraîcheur se vérifie et le chemin est déterministe.
- **Q-CORR-5 (`-s` non posé aux scripts).** `-I` retirerait aussi PYTHONHASHSEED ; `-s` (site utilisateur) n'est pas
  demandé par C-1 et n'est pas éprouvable sans écrire dans le HOME réel (sous `env -i`, Python retrouve le HOME par
  `pwd`). Rendu en item (§8).

## 8. Items (règle PAROXYSME)

- **SHOGEN-PLAN-S2BIS-2-REFUS-NON-NOMMES-1 : fermé** par P2R-6b (tables du §4, LEC-1, LEC-2, LAN-13, MAS-3).
- **SHOGEN-PLAN-S2BIS-2-EPINGLE-INTERPRETE-1 (neuf)**. Constat : C-1 ferme les vecteurs du dossier du lot, de
  l'environnement et du bytecode voisin ; l'épingle ne couvre ni le `python3` du PATH et son installation (site-packages
  système et utilisateur, fichiers `.pth` exécutés au démarrage), ni `git`, `tar`, `sha256sum`. Construction : à
  l'épinglage, consigner au JOURNAL le chemin, la version et le sha256 de `python3` et la version de `git` (ou poser
  `-s` avec une procédure d'épreuve hors du HOME réel). Prix : deux lignes de procédure. Déclencheur : épinglage au
  JOURNAL.
- **SHOGEN-S2BIS-P1-ESTIMATION-1 (précisé)** : ≈ 980 lignes au périmètre, 1 425 au générateur, **1 701 après
  corrections** (× 1,74), en 11 diffs.
- Maintenus sans changement (non traités ici, comme le brief le dit) : SHOGEN-PLAN-S2BIS-2-PY310-1,
  SHOGEN-WORKER-WERROR-IGNORE-1, SHOGEN-PLAN-S2BIS-2-REPETITION-1 (contre-contrôle, journaux synthétiques).
- **SHOGEN-PLAN-S2BIS-2-TRACE-HARNAIS-1 (neuf)**. Constat : hors de tout refus, le harnais extrait écrit lui-même
  deux avertissements sur stderr, donc dans `lancer.log` : dernière ligne tronquée ignorée (`records.read_jsonl_tolerant` :
  chemin et numéro de ligne) ; prix non finis lus comme absents (`r1.parse_journal` : nombre par flux). Ce ne sont pas
  des valeurs de journal recopiées, mais des comptes tirés des journaux. Construction : l'écrire à la procédure de
  lancement (`lancer.log` lu par lignes nommées seulement, E-P2-07), ou filtrer ces deux lignes au lanceur. Prix : une
  ligne. Déclencheur : épinglage au JOURNAL.
- Observation O-5 de la G2 (code du refus d'un script hors de l'écran) : toujours ouverte, sans correction ; le refus
  nommé est la dernière ligne des sorties de passe, et le script n'écrit rien dans `lancer.log`.

## 9. Écarts

- **E-1. Barres obliques inverses tapées** dans quatre commandes (deux séquences de saut de ligne dans des littéraux
  Python d'édition, l'une pour MAS-3, l'autre pour ce rapport ; l'échappement d'un dollar dans un `echo` vers NOTES ;
  un motif `od | grep`). Contrôle sur les octets : 0 octet 92 dans les 13 fichiers du lot, les 11 diffs, mes outils,
  NOTES.md et ce rapport.
- **E-2. TMPDIR.** Lors des deux premiers passages de l'e2e, le banc de fixtures (`tempfile.mkdtemp`) a écrit sous
  `/tmp` (TMPDIR non posé dans mon shell) ; retiré par le banc ; aucun reste. Les passages suivants ont posé
  `TMPDIR=corr/tmp`.
- **E-3. Défaut de mon test** vu à la suite : la fonction `renommer` de LAN-13 modifiait `tests.PRM` partagé par
  `ecrire()` (18 FAIL, 4 ERROR en un passage) ; corrigé par une copie (`dict(...)`) ; ce passage n'est pas compté
  comme rouge.
- **E-4. Affichage faux** : une commande a affiché « sortie 0 » pour des suites en échec (substitution de commande
  évaluée avant `$?` dans la même chaîne) ; les journaux portent `FAILED`.
- **E-5. Refus de l'outil.** Le lancement détaché du script de verdict de s2-harness
  (`enforcement/verdict-suite-s2.py --egal`) a été refusé par le classificateur du mode automatique ; je l'ai remplacé
  par la suite s2-harness au premier plan (`unittest`, réseau coupé) : Ran 407, OK (skipped=2), même compte que la G2 ;
  le verdict « conforme » du script lui-même n'a pas été obtenu.
- **E-6. P2R-4b** s'applique sur 4a corrigé avec un contexte réduit (`git apply -C1`) : hunk d'ajout en fin de
  `test_lancer.py` dont le contexte de tête portait une ligne de LAN-6 réindentée par C-3 d ; résultat contrôlé (diff
  -r : origine plus les seuls deltas). Les diffs livrés, eux, s'appliquent sans retouche.
- **E-7. Première construction** (`etats/`) : Q-P2R-3 en P2R-1a donnait +230 ; mesuré avant toute livraison, refait
  (`etats2/`, puis `snap/`) ; aucun diff de plus de 200 lignes n'est livré.
- **E-8. Isolement.** L'e2e et `xtask` ont tourné sans `unshare -n` (le brief le demande pour la suite, qui l'a eu) ;
  l'e2e n'appelle que git, bash et python en local.
- **E-9. Listes de processus** : un `ps | grep` sur un fragment de chemin a aussi montré un processus d'un autre worker
  (`outillage2/corr`) ; listé seulement, aucun signal ; mes PID réels sont identifiés par leur parent.
- **E-10.** La suite sim-bis n'a pas été rejouée (non demandée ; aucun de ses fichiers n'est touché).

## 10. Journal de provenance (G1)

**Lu [lu]** : brief corr (23 l.) ; `code/BRIEF-P2R.md` (43 l.) ; `g2/G2-P2R-transcrit.md` (411 l.) ;
`code/RAPPORT-WORKER-P2R-transcrit.md` (230 l.) ; `G0-PLAN-S2BIS-2.md` (23 l.) et `PERIMETRE-REDUIT.md` (277 l.), en
entier ; `PROPOSITION.md` l.126-215 et l.300-428 ; `AVIS.md` l.60-99 et l.134-203 ; code du lot (13 fichiers de
`code/snap/P2R-5`, en entier ; `snap/P2R-0a/tests/test_socle.py` ; hunk `test_lancer.py` de `P2R-4b.diff`) ;
PLAN-S2BIS : `commun.py`, `episodes.py`, `regles.py`, `tests/fixtures.py` en entier, `SHA256SUMS`, README l.32-34 ;
harnais extrait de `f35a70c` : `records.py` l.80-113 et l.295-423, `r1.py` l.59-69, l.85-97, l.321-357 et l.398-515,
`window.py` l.98-139 ; NOTES du générateur et du réviseur ; outils du réviseur (`campagne.py`, `e2e.py`,
`e2e_parade.py`, `e2e_pyc.py`, `horsgrille.py`, `s2suite.sh`, `xtask.sh`, `simbis.sh`) ; outils du générateur
(`mutants.py` l.1-60, `mutants_P2R-0.py` l.1-40, `mutants_P2R-2.py`) ; `isole.sh`, `lo_up.py` ; `xtask-verify.txt` du
générateur, lignes de verdict seules.
**Non lu [abs]** : `LETTRE-AJOUT-G0-SIM.md`, `CP1-AJOUT*.md`, briefs du dossier G0 ; `G0-SIM-BIS.md` ; ADR-0029 ;
annexes B et D ; JOURNAL ; EP réel (haché par `sha256sum -c` seulement) ; rendu J28 ; paquet ; `s2bis/`,
`docs/adr-0029/s2bis/`, `docs/adr-0028/sceau/` (jamais ouverts).

**Commandes et sorties** (heures `date -u`) : 13:00 relevé de base ; 13:10 `git archive e6657dc` (7 exclusions,
absences contrôlées par `test -e`) et `git archive f35a70c s2-harness` (`docs` absent) ; 5 épingles du harnais égales ;
`sha256sum -c` de PLAN-S2BIS, d'EP et de `g0-plan2` OK ; 13:12 série d'origine : 9 états = `code/snap` ; épingle
`a8bb826d…` retrouvée ; 13:16 suite d'origine 28 OK ; 13:17-13:19 G2 sur l'origine 18/9/0 ; 13:18-13:44 rouges et
mutants par diff (journaux `rouge-*`, `vivants-avant-*`) ; 13:47 diffs, série sur la base, instantanés 2 à 34 ; 13:50
suite finale 3.11-3.13 × 0/1 ; 3.10 ; forme ; 13:50-14:12 campagnes finales ; 13:52, 13:59 et 14:00 e2e ; 13:52 PLAN-S2BIS :
Ran 37, OK ; 13:54 s2-harness : Ran 407, OK (skipped=2) ; 13:57 xtask (§1).

**PID réels** : G2 sur l'origine 30384 (enveloppe 30382) ; mutants de P2R-6 32151 (32150) ; campagnes finales : sh
6689 (setsid 6688), g2 6699, neufs 20213, générateur 11977 ; fins constatées en sondant le PID.

**Recomptes [calc]** (par script) : lignes ajoutées (`git apply --numstat`) ; octets 92, tabulations, retours chariot,
longueurs, TODO et FIXME (`outils/forme.py`) ; classements des campagnes ; 1 795 − 94 = 1 701 lignes = 1 689 (12
fichiers) + 12 (`SHA256SUMS`).

## 11. Attestation (forme D.3)

- Aucune pièce de la liste D.2 ouverte. Aucun journal réel de S2 ni de S2-bis lu, listé, cherché ni copié ; aucun
  `*.jsonl` réel ; les seuls `*.jsonl` sont synthétiques, écrits et lus par les tests et par l'e2e sous TMPDIR (ou sous
  `/tmp`, E-2), retirés, jamais affichés.
- `lancer.sh` n'a tourné que dans des dépôts jetables de fixtures (tests du lot, e2e).
- `SHOGEN_S2_CAMPAGNE_CONTROL` : jamais posée par moi ; posée seulement par la suite du lot elle-même (LAN-6, valeur
  fictive, sous-processus du lanceur : exception A-3 écrite au G0 et au README), à chaque passage de la suite.
- Rien d'ouvert de `docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`,
  `docs/adr-0028/monark-m009a/`, `docs/adr-0028/execution/` (exclus de mes copies) ; aucune recherche récursive sur
  `docs/`, le dépôt ou le scratchpad entier.
- Aucune écriture git sur le dépôt (lectures seules : `archive`, `rev-parse`, `status`, `log`, avec
  `--no-optional-locks`) ; dépôts git jetables seulement (`init`, `add`, `write-tree`, `mktree`, aucun commit). Rien sur
  Pocket.
- Exposition : aucune valeur de S2 affichée ; le `parametres.json` de PLAN-S2BIS n'a été lu par mes commandes que pour
  ses clés, ses types d'épisodes, ses strates, ses quantiles, les épingles du harnais et le commit d'analyse (son bloc 3
  n'a pas été affiché) ; EP réel haché seulement ; aucune donnée de S2-bis n'existe.

## 12. Fichiers et clôture

Sous `<scratchpad>/s2bis/plan2/corr/` : `diffs/P2R-{0a,0b,1a,1b,2,3,4a,4b,5,6a,6b}.diff` ; `snap/P2R-x/` (11
instantanés ; état final `snap/P2R-6b/scripts/plan-s2bis-2/`) ; `journal/` (rouges, vivants avant, campagnes, suites,
e2e, forme, verdicts xtask) ; `outils/` ; `NOTES.md` ; ce rapport ; `SHA256SUMS` du dossier (calculé après ce rapport,
il le couvre ; son sha256 est donné dans le message de rendu).

Clôture à 14:13 UTC : série rejouée depuis zéro après nettoyage (11 diffs, chaque état = `snap/P2R-x`, épingle
`fe46ebd6…f36f`, `-c` 12/12) ; copies lourdes retirées (copie de e6657dc, extraction de `f35a70c`, cible cargo, arbres de
travail, états intermédiaires) ; `tmp/` vidé puis retiré ; 0 `*.jsonl` restant ; dépôt intact (HEAD e6657dc, `git status` vide).
