# Relecture G2 — LINT-HAIKU (transcrit)

> Transcription par l'orchestrateur le 2026-10-08 12:11:04 UTC du rapport rendu par l'agent ae9f81b14c6c9942d (workflow wf_34ba9b2a-037) ; contrôle FM-1.1 : fragments_l51_l14 = 0 ; modèle résolu au transcript : claude-opus-5-5. Texte de l'agent ci-dessous, sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

**Gate 0 : `claude-opus-5-5`.** C'est l'identifiant exact donné par le contexte système de la session ; l'effort `max` ne se voit pas de l'intérieur. Je suis réviseur G2 neuf : je n'ai écrit aucun des diffs relus. Horloge relevée par `date -u` : de 2026-10-08T10:35:40Z à 11:05:37Z.

# Verdict : ACCEPTE-AVEC-CORRECTIONS (C-1 à C-3)

Le code du lint (LH-1) et la fiche (LH-2) sont acceptés tels quels. Les trois corrections portent sur le runner seul : un renvoi sans chemin versionné et trois cas de test à ajouter. Le critère de sortie « verify VERT » ne peut pas être atteint sur une copie : S-G9 sort ROUGE, de façon identique avec et sans le lot (Q-5).

| C | fichier:ligne (copie finale) | preuve | remède |
|---|---|---|---|
| C-1 | `enforcement/tests/run-fixtures-model-pinning.sh:14` et `:158` | Les deux lignes citent « G0 du lot, E-LH-1 et E-LH-2 ». Ce G0 n'est versionné nulle part (il est dans le scratchpad). La convention du dépôt donne un chemin (`docs/adr-0028/G0-lot-D8c.md`, l.13). | L'orchestrateur choisit un chemin versionné pour le G0, que les deux lignes citent. À défaut, renvoyer au bloc B qui consignera le lot. |
| C-2 | même fichier, après `:173` | Le mutant R-04 (seule la première lettre passe en minuscule) **survit** : 107 ok. Il admet `Claude-haiku-5-5` et `Claude-opus-5-5` ; le lint final les refuse. T-105 n'a que la forme à deux majuscules. C'est la classe « casse ignorée » que le G0 §4 exige. | Ajouter `arbre D 'model: Claude-haiku-5-5'; cas T-108 2 R-1/hors-liste`. |
| C-3 | même fichier, après `:173` | Deux mutants **survivent** : R-10 (espace insécable final retiré) et R-11 (U+200B et BOM retirés). Le lint final refuse ces formes (H-07, H-11, H-68), mais aucun cas ne fige ce refus. | Ajouter deux cas, écrits en octal par `printf` : `"model: claude-haiku-5-5$(printf '\302\240')"` (T-109) et `"model: claude-haiku-5-5$(printf '\342\200\213')"` (T-110), attendus `R-1/hors-liste`. Mettre à jour en conséquence « T-96 à T-107 » (l.14) et le commentaire des l.158-161. |

Remède éprouvé en brouillon (`<LH>/g2/tmp/proposition/`) :
- le runner proposé contre le lint final donne 110 ok, sortie 0, sous POSIX comme sous C.UTF-8 ;
- il tue R-04 par T-108, R-10 par T-109, R-11 par T-110 ;
- les octets 92 du runner passent de 48 à 53.

# 1. Exigences et ce qui les fige

| exigence | où | test qui la fige / mesure |
|---|---|---|
| G0 §2 : `ALLOWED` | `enforcement/lint-model-pinning.sh:36` (+1 identifiant, rien d'autre) | T-96 à T-100 |
| G0 §2 : en-tête | lint l.7-9 (CLAUDE.md l.23-49, contrôlé) ; l.27-28 (l.41-42, contrôlé) | relu |
| E-LH-1 | runner l.162-166 (T-96 à T-100) | rouge contre le lint de e6657dc : 101 ok, 6 échecs, sortie 1 ; vert : 107 ok, sortie 0, 3,5 s |
| E-LH-2 | l.167-173 (T-101 à T-107) ; T-48 (l.108) inchangé | voir le tableau des formes hostiles ci-dessous |
| E-LH-3 | aucune ligne de T-01 à T-95 retirée ni changée ; fixtures identiques | runner d'origine contre le lint final : 95 ok |
| E-LH-3, arbre | copie + LH-1 + LH-2 : `OK (R-1) : 7 fichier(s)`, sortie 0 (6 sur la base) | compte refait sur la liste de l'archive : 6 + 1 |
| E-LH-4 | fiche l.12 `effort: high` ; rôles et interdits l.3-10 et l.20-34 | **aucun test** (voir I-3) ; PyYAML lit model, effort et tools comme attendu |

Pour E-LH-3, le contrôle porte sur la copie avec exclusions. L'arbre complet sera jugé au commit par le hook (`pre-commit` l.39-46, sur l'index) puis par le job g1.

Autres points tenus :
- `git apply --check` et `patch -p1` passent en série.
- Les sha256 obtenus sont ceux du rapport : f806c036…, 9744dfb7…, 1974e9f9….
- Mon archive de base est identique à celle du générateur (c1f09c21…).
- Le SHA256SUMS du générateur (cece1463…, 54 lignes) passe `sha256sum -c`.

# 2. Formes hostiles

Je les ai testées sur le lint final et le lint de base, avec un harnais à moi (`scripts/hostiles.py`). Résultat : 0 écart.

| volet | contenu | résultat |
|---|---|---|
| A | 68 cas à attendu écrit à la main : casse, suffixes, NBSP, homoglyphes, U+2011, ZWSP, guillemets, commentaires YAML, clé répétée, CR, skills, commandes, JSON | 0 écart |
| B | 840 comparaisons : 40 transformations × 7 contextes × 3 identifiants déjà admis. Oracle : final(t(haiku)) = base(t(id)), et final(t(id)) = base(t(id)) | 0 écart |
| C | 456 variantes × contextes : homoglyphes, invisibles insérés à chaque position, 26 identifiants voisins | toutes refusées, comme sur la base |

- Le tier nu `haiku` (et `HAIKU`, `"Haiku"`) reste refusé en `R-1/tier-nu`, en YAML comme en JSON.
- Rien d'autre n'est élargi : seules les formes dont la valeur normalisée vaut exactement `claude-haiku-5-5` passent, avec les mêmes règles que les autres identifiants.
- Mon premier passage du harnais avait 19 écarts : c'étaient des erreurs de mon oracle, pas du lint. Je les ai corrigées ; les sorties du lint n'ont pas changé.
- Le harnais donne des sorties identiques sous Python 3.10 à 3.13 en `-X dev -W error`, et sous LC_ALL=C.UTF-8.

# 3. Mutants

| campagne | classés par | tués | vivants | FATAL |
|---|---|---|---|---|
| mes 15 mutants du lint (R-01 à R-15), borne 300 s | runner final (1 tué / 0 vivant) | 12 | 3 : R-04, R-10, R-11 | 0 |
| mes 8 mutants de la fiche (F-01 à F-08) | commande du job (`lint .`, 2 tué / 0 vivant) | 4 : la ligne `model` | 4 : effort retiré, effort `medium`, outils d'écriture ajoutés, interdit advisor retiré | 0 |
| rejeu des 13 mutants du générateur | runner final | 13 | 0 | 0 |

- Le rejeu des mutants du générateur donne des listes de cas identiques à son `campagne.tsv`.
- Les trois mutants vivants du lint ne sont pas équivalents : chacun admet une forme que le lint final refuse (démontré par `scripts/temoin.sh`).

# 4. Matrice Python 3.10 à 3.13

- Les diffs ne contiennent aucun Python.
- Mes outils (`forme.py`, `hostiles.py`) donnent des sorties identiques sur les quatre versions en `-X dev -W error`.
- s2-harness sur la copie finale : 407 tests OK (2 sautés) sous 3.11, 3.12 et 3.13.
- Sous 3.10, s2-harness donne **77 échecs et 3 erreurs**. Le même ensemble apparaît sur la base, avec ou sans `-X dev` ; la cause relevée est `hashlib.file_digest`, qui n'existe qu'à partir de 3.11. C'est antérieur au lot.

# 5. Forme

| | lignes ajoutées | dont code | octets 92 ajoutés | > 120 caractères | TODO/FIXME | CR | littéral banni |
|---|---|---|---|---|---|---|---|
| LH-1, lint | +6 | 1 | 0 | 0 (max 101) | 0 | 0 | 0 |
| LH-1, runner | +17 | 12 | 0 | 0 (max 107) | 0 | 0 | 0 |
| LH-2, fiche | +34 | 0 | 0 | 0 (max 113) | 0 | 0 | 0 |

- Totaux d'octets 92 : 43 dans le lint et 48 dans le runner, avant comme après.
- Aucune dépendance neuve (R-8).
- `bash -n` passe sur le lint et le runner.
- La gate des secrets (`--tree`) sur la fiche seule : OK.

`cargo --locked xtask verify` sur la copie finale (sortie 1) :

| ligne de verdict | résultat |
|---|---|
| S-G1 à S-G8 (dont S-G7a) | VERT |
| S-G9 | ROUGE (1), `docs/17-modele-de-menace.md:70`, connue |
| fmt, no_std, clippy | VERT |
| global | ROUGE |

Sur la base sans les diffs : mêmes verdicts, et section S-G9 identique.

# 6. Rien de retiré ni d'affaibli

- Runner : 0 ligne retirée, 17 ajoutées.
- Lint : 3 lignes retirées, à savoir l'en-tête réécrit et `ALLOWED` étendu.
- Fixtures inchangées.
- Entre la base et la copie finale, seuls 3 fichiers diffèrent (`diff -rq`).

# 7. Mon avis sur Q-1 à Q-5

- **Q-1 : garder T-100**, puisque c'est le contrat E-LH-1. Mais il faut savoir qu'E-LH-1 va au-delà de B.76 et du roster, qui excluent advisor : c'est un élargissement à la clé `advisorModel`.
  - Le non-lien entre identifiant et rôle est antérieur au lot : le lint de base admet déjà `advisorModel` en `claude-opus-5-5` ou `claude-sonnet-5-5`.
  - Il faut former l'item I-4 ci-dessous.
- **Q-2 : garder la forme nue admise.** PyYAML 6.0.1 lit `model: claude-haiku-5-5 ` comme `'claude-haiku-5-5'`, et le traitement est le même pour tout identifiant (volet B). Je propose d'écrire cette lecture d'E-LH-2 dans le G0 une fois versionné.
- **Q-3 :** traité par C-1.
- **Q-4 : garder la phrase.** Elle restreint les rôles, elle ne les étend pas. Elle est cohérente avec la règle 8 du worker et le point 5 de la fiche lecteur.
- **Q-5 : oui.** Sur une copie, S-G9 est structurellement ROUGE.

# Écarts

1. **Exposition déclarée par le générateur, absente de son rapport.** Le journal G1 du générateur (§1) déclare avoir affiché les lignes 355 à 374 de la sortie de S-G9, dont des noms de références (« D.2 n° 10 »). C'est contraire à la consigne « lignes de verdict seules », et cet écart ne figure pas parmi ceux du rapport. Je ne l'ai pas remesuré, pour ne pas m'exposer moi-même. À l'orchestrateur de juger si une attestation D.3 est due.
2. E-LH-3 et verify n'ont été contrôlés que sur la copie avec exclusions. Le contrôle sur l'arbre complet est à constater par l'orchestrateur.
3. Le Python 3.10 de s2-harness est rouge, de façon antérieure au lot (§4).
4. L'en-tête cite CLAUDE.md l.23-49 et l.41-42. Si l'orchestrateur modifie CLAUDE.md dans le même commit, ces numéros sont à recontrôler.

# Items à former (règle PAROXYSME), tous antérieurs au lot

- **I-1, locale (le plus urgent).** Le verdict du lint dépend de la locale.
  - Sous C.UTF-8, le lint de base comme le lint final admet `model:<U+3000>id`, `model: <U+3000>id`, et les mêmes formes avec U+2003, U+1680 et U+2028 (sortie 0). Sous POSIX, il les refuse.
  - PyYAML ne lit pas ces formes comme l'identifiant : erreur de lecture, ou valeur `'<U+3000>id'`.
  - La locale du runner CI est C.UTF-8 selon moi, mais je ne l'ai pas mesurée [2nd]. Celle du hook sur cet hôte est POSIX (mesurée). Le job et le hook peuvent donc diverger.
  - Remède probable : `export LC_ALL=C` en tête du lint, plus 2 cas. Il faut un G0, car c'est hors du périmètre de ce lot.
- **I-2, clé `env` des réglages.** Le lint ne lit pas la clé `env` de `.claude/settings*.json` : `ANTHROPIC_MODEL` et `ANTHROPIC_DEFAULT_HAIKU_MODEL` y passent (H-61, H-62 : sortie 0). L'effet de ces variables sur Claude Code est [2nd]. Déclencheur : le premier réglage versionné ; il y en a 0 à e6657dc.
- **I-3, effort et outils.** Aucune gate ne lit `effort` ni `tools` (F-05 à F-08 vivants ; `effort` n'apparaît ni dans le lint, ni dans `xtask/src`, ni dans `enforcement`). E-LH-4 ne tient que par la relecture.
- **I-4, rôle.** Réserver `advisorModel` à `claude-fable-5-1`, ce qui inverserait T-100. C'est l'item 1 du générateur ; je suis d'accord.
- **I-5, Python 3.10.** s2-harness exige Python 3.11 ou plus (`hashlib.file_digest`), sans le déclarer.
- **Items 2 et 3 du générateur.** D'accord avec l'item 2. Je n'ai pas remesuré l'item 3 (`setsid`).

# Fichiers produits

Tous sous `<scratchpad>/lot-haiku/g2/` :
- `SHA256SUMS` : 101 lignes, `sha256sum -c` OK ; empreinte 3fd40e77ecc2c278cdda6db8c35cbea740b8cd58891a83408ee02b35622c6d53 ;
- `NOTES.md` : c9a633c60f2f2e266b214807ba275eaa4e6fc4f6d41bc5adcd63fbdb34ee51d2 ;
- `logs/campagne-g2.tsv` : 2c4095d2… ;
- `logs/rejeu-mutants-generateur.tsv` : 17d3a528… ;
- `logs/hostiles-py3.13.tsv` : 03533159… ;
- `logs/unicode-locale.tsv` : cc407ff2… ;
- `logs/proposition-C2-C3.txt` : c3bfdeda… ;
- `scripts/` : `hostiles.py`, `mutants_g2.py`, `rejeu_generateur.py`, `unicode_locale.py`, `forme.py`, `temoin.sh` ;
- `mutants/R-01` à `R-15` (`.sh`, `.diff`, `.sortie`) ;
- `tmp/proposition/run-fixtures-model-pinning.sh` : db670720….

Dépôt réel à la fin : HEAD e6657dc, status vide, 6 fiches sous `.claude/agents/`, aucune écriture git. Je n'ai ouvert aucune pièce de D.2, aucun `*.jsonl`, aucun dossier interdit.
