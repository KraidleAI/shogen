# Journal de provenance G1 — lot DOCS11-EN (version anglaise du brouillon public de `docs/11`, non publiée)

Worker du lot (fiche `shogen-worker`), instance neuve. Brief horodaté 15:15:44 UTC (date du fichier) ; premier fichier du
lot écrit à 15:21:14 UTC ; journal écrit à partir de 16:43:22 UTC et complété à partir de 16:51 UTC (`date -u`), le 2026-10-04. Rien n'est publié. Aucune
opération git en écriture. Écritures limitées au dossier du lot `/tmp/claude-0/-home-user-shogen/7ba84933-ba6d-5813-9ef4-ca3ac4febd16/scratchpad/s2bis/en/`
(noté `en/` plus bas).

## Gate 0

Identifiant de modèle déclaré par l'environnement : `claude-opus-5-5` (préfixe attendu `claude-opus-5-5` : conforme).
Effort `max` demandé par l'orchestrateur ; il n'est pas observable de l'intérieur de la session.

## Brief et rattachement (G0)

- Brief `en/BRIEF-DOCS11-EN.md` [lu, 36 lignes] ; sha256 recompté
  `cfe6c0d5ea1db0241767c16e2ebf3aa4a1b9eba7a6715161b822bbbb958c0e69`, égal à la valeur donnée.
- Rattachement :
  - JOURNAL l.396, entrée du 2026-10-04 15:16:03 UTC : demande de l'investisseur (verbatim), lots DOCS11-EN et
    CONTACTS-PREAVIS lancés [lu ; entrée versée par le commit `6c37859`].
  - G0 `docs/adr-0029/G0-lots-S2BIS.md` l.13, ligne DOCS11-PUBLIC, dont la sortie est la source traduite [lu, 23 lignes].
  - Annexe B.57 d'ADR-0028 (`ANNEXE-B-items.md` l.937 à 954) : brouillon versé, non publié ; items
    SHOGEN-PUBLIC-MENTION-FEU-VERT-1 et SHOGEN-PUBLIC-PREAVIS-1 [lu].
- E-7 : `G0-lots-S2BIS.md` ne porte pas de ligne propre à DOCS11-EN (recherche `DOCS11` : l.13 et l.21 seulement). Le lot
  se rattache par l'entrée du JOURNAL et par le brief. Une ligne de G0 reste à poser par l'orchestrateur.

## État du dépôt (lecture seule)

- Branche `claude/compassionate-noether-szmdyj`.
- Base relevée au départ : `c354d15589edb80a8e7e692c873bbeb57f244aa5` (commit de 15:08:39 UTC, lot DOCS11-PUBLIC versé).
- À 16:35 UTC : HEAD `e16956b9fca722275cd662214581ec5939772c89`.
  - `git rev-list c354d15..e16956b` : 2 commits de l'orchestrateur, `6c37859` (15:17:34 UTC) et `e16956b` (16:22:29 UTC).
    Aucun n'est `aa04924` ; je l'ai contrôlé sur les empreintes avant d'afficher un sujet de commit.
  - `git diff --name-status` : ils ne touchent que `JOURNAL.md` et `docs/adr-0029/ADR-0029-campagne-S2-bis.md`.
  - `git diff --quiet c354d15 e16956b -- docs/publication docs/09-vocabulaire.md xtask docs/adr-0028/ANNEXE-B-items.md
    docs/adr-0028/ANNEXE-D-preenregistrement.md docs/adr-0029/G0-lots-S2BIS.md docs/G1-lot-DOCS11-PUBLIC.md s2-harness
    biblio` donne la sortie 0 : les entrées du lot sont identiques sur les deux bases (E-8).
- `git status --porcelain` : 0 ligne à 15:33 et à 16:37 UTC.
- À 16:52 UTC, après la suite finale, HEAD vaut `4a31685ab758423a973b90dfc75b5766028ef288`.
  - Six commits de l'orchestrateur, de 16:43:54 à 16:51:14 UTC, lot PLAN-S2BIS. Ils n'ajoutent que des fichiers
    sous `scripts/plan-s2bis/` (`git diff --name-status e16956b 4a31685`). Aucun n'est `aa04924`.
  - Un chemin non suivi : `scripts/plan-s2bis/episodes.py`. Il relève du même lot, pas du mien.
  - `git diff --quiet c354d15 4a31685 -- docs/publication/11-mesures-pilotes-public.md docs/09-vocabulaire.md xtask
    docs/adr-0028/ANNEXE-D-preenregistrement.md docs/adr-0029/G0-lots-S2BIS.md docs/G1-lot-DOCS11-PUBLIC.md
    s2-harness biblio` donne la sortie 0.
- `SHOGEN_S2_CAMPAGNE_CONTROL` n'est pas posée (`printenv`, sortie 1). Elle est retirée explicitement (`env -u`) à chaque
  lancement de la suite.

## Pièces interdites et périmètre de lecture

- Liste du brief : `docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`,
  `docs/adr-0028/monark-m009a/`, tout `*.jsonl`, toute pièce de D.2. Les pièces de D.2 n'ont été lues que par leurs noms
  (ANNEXE-D l.32 à 48).
- E-1 (exposition, déclarée) : en début de lot, deux commandes `grep -r` ont été lancées sur tout `docs/` pour relever la
  terminologie anglaise du projet. Elles ont donc lu les dossiers interdits.
  - La première n'a affiché que des comptes agrégés de termes.
  - La seconde a affiché 2 lignes de `docs/pocket-report/` (`POCKET-DISCLOSURE-REPORT.md` l.81, `G0-claims-register.md`
    l.52).
  - Aucune ligne de la cartographie l.51 ni d'ADR-0025 l.14 n'a été affichée ; aucune valeur de campagne non plus.
  - Rien de ces lignes n'entre dans la traduction, qui ne part que de la source. Les comptes agrégés ont pu peser sur
    le choix de `feed` et `staleness` ; la source et l'usage courant suffisent à justifier ces deux choix.
  - Remède appliqué : ensuite, uniquement des listes explicites de fichiers permis.
  - Demande : contrôle FM-1.1 de ma transcription par l'orchestrateur (`scripts/controle/fm11.py`). Je ne l'ouvre pas
    moi-même : c'est un `*.jsonl`.
- E-9 (compaction du contexte) : le contexte de travail a été résumé une fois pendant le lot.
  - La note de reprise proposait le chemin de la transcription de la session (`*.jsonl`). Je ne l'ai pas ouvert : c'est
    interdit par le brief, et D.2 n° 11 couvre la transcription de l'orchestrateur.
  - Trois informations viennent de mes relevés d'avant la compaction : les heures de fixation et d'amendement du
    glossaire (15:45:05, 15:49:11, 16:10:29), l'heure de la suite d'avant (15:33:12) et la description de E-1.
  - Pour le reste, les preuves sont dans des fichiers. Les empreintes du glossaire sont dans
    `en/explo/glossaire-fixation.sha256`. L'heure de A-4 (16:19:43) concorde avec la date de ce fichier et avec celle
    de `outils/glossaire_en.py`.

## Sources lues

| source | niveau | empreinte, taille | usage |
|---|---|---|---|
| `docs/publication/11-mesures-pilotes-public.md` | [lu], intégral | `4de98654…7688` (égal au brief), 1081 lignes, 99 352 octets | source traduite |
| `docs/09-vocabulaire.md` | [lu], intégral | `001b9606…2f31`, 63 lignes | registre transposé en anglais |
| `xtask/src/sg4.rs` | [lu] | `b0f7f125…9bdb`, 166 lignes | 15 locutions ; exclusions (citations, code) |
| `xtask/src/sg5.rs` | [lu], parties utiles | `e2629451…1f3d`, 426 lignes | extraction des citations « … » anglaises |
| `xtask/src/main.rs`, `xtask/src/lib.rs` | [lu], parties utiles | `ec0c7e47…daa2`, `002e2cdd…5690` | sous-commande `gates`, racine du workspace |
| `docs/adr-0028/ANNEXE-B-items.md` | [lu], partiel (B.56, B.57) | `31da5b35…6fbd` | rattachement, items |
| `docs/adr-0028/ANNEXE-D-preenregistrement.md` | [lu], partiel (l.32 à 48, noms des pièces de D.2) | `deb64179…0eaf` | liste interdite |
| `docs/adr-0029/G0-lots-S2BIS.md` | [lu], intégral | `25a82120…a130`, 23 lignes | rattachement |
| `JOURNAL.md` | [lu], partiel (fin ; l.396 ; diff `c354d15..e16956b`) | `1213c10d…0814` à `e16956b` | demande de l'investisseur |
| `docs/G1-lot-DOCS11-PUBLIC.md` | [lu], partiel (plan, extraits) | `5c3719c7…d0c7` | plan du journal ; motifs |
| `scripts/controle/README.md` | [lu], partiel (FM-1.1) | — | FM-1.1, outil de l'orchestrateur |
| dossier du lot DOCS11-PUBLIC (`…/scratchpad/s2bis/docs11pub/`) : brief, `outils/controle_public.py`, `tests/lancer_tests.py`, extraits de campagne | [lu] | — | motifs repris ; contrat de runner |
| `docs/publication/interne/TABLE-CORRESPONDANCE.md` | [abs] | — | citée par le brief ; pièce interne, non ouverte : la traduction part de la seule source publique |
| documents cités par la source (doc 10, ADR, paquet scellé, JOURNAL, réponses de l'investisseur) | [abs] | — | citations traduites depuis le texte que la source recopie ; originaux non rouverts |

## Méthode

1. Relevé de la source par scripts (`en/explo/`) : titres, blocs de code, nombres et citations. La source porte 120
   citations « … » de premier niveau (96 textes distincts, `explo/distinctes.txt`) et une citation anglaise “ … ” (l.704).
2. Glossaire fixé avant toute ligne traduite (`outils/glossaire_en.py`, données seules). Il contient :
   - 58 titres ;
   - 55 gloses ;
   - 9 passages neutres ;
   - 41 citations traduites ;
   - 30 passages protégés ;
   - 7 libellés comptés ;
   - 54 lignes de termes ;
   - l'en-tête et 1 exception de registre.
3. Tests d'abord, sur le script de contrôle :
   - module factice (`outils-factice/controle_en.py`) et étape rouge ;
   - puis le contrôle réel et l'étape verte ;
   - chaque correction d'outil qui a suivi est passée par un test d'abord (étapes rouges 2, 3 et 4).
4. Traduction à la main, par parties (`parties/p1.md` à `p5.md`), une ligne par paragraphe. `outils/assembler_en.py`
   recopie à l'octet les 9 blocs de code depuis la source et remplit le glossaire final depuis le module.
5. Vérifications finales :
   - contrôle en onze points ;
   - relecture des 410 unités alignées, une par une (`explo/paires-relecture.txt`) ;
   - gates réelles S-G4 et S-G5 sur une copie réduite ;
   - campagne de mutants ;
   - relevé informatif de l'emploi des termes ;
   - réassemblage (même sha256) ;
   - suite `s2-harness` avant et après.

## Glossaire : fixation et amendements

| étape | heure UTC | sha256 du module | objet |
|---|---|---|---|
| fixation | 15:45:05 (horloge d'écriture 15:41:28, inscrite dans le module) | `cdd30845c1823b667e981f19e3a8aec5dd5b78ebe06bc17ff004110ca448816c` | — |
| A-1 | 15:49:11, avant toute ligne traduite | `7d10a8df89f1da4dc8f2eb20a51d4b1974c0eaf516dd3c02ae453766945451f8` | terme « recopié » précisé : copie verbatim des sorties, citation traduite des documents |
| A-2 et A-3 | 16:10:29, pendant la traduction, avant tout passage du contrôle sur elle | `a3dee6886d99d051cfcfffacbe51238e953163e0669b3395b15652bd1c625f0f` | A-2 : « go exécution » gardé et glosé (G-55), car la source le dit verbatim. A-3 : P-02 rendu `has the value` (« vaut »), car `is` rend aussi deux « est FAUX » (l.376, l.972) |
| A-4 | 16:19:43, après les deuxième et troisième passages du contrôle | `e8fd4ee94150c6ac960c5110d87ae65b2b92b2faadaca7c68484071e91b0aeea` | la note du terme « valider » ne cite plus le qualificatif d'assurance interdit |
| A-5 | 16:48:57, après le relevé informatif de l'emploi des termes | `9a44cda655195310810b3b24504fcc7809b49fa62495df0ef23a15b449155d9c` | sens « contrôle d'horloge » du terme « écart » ajouté, rendu `offset`, comme la source écrit elle-même « offset médian » (l.1024) ; seule la ligne du glossaire final change (l.716), aucune ligne du corps |

## Commandes et sorties (chronologie ; heures `date -u` ou dates de fichiers)

| heure UTC | commande | sortie |
|---|---|---|
| 15:33:12 à 15:34:00 | suite `s2-harness`, avant : `env -u SHOGEN_S2_CAMPAGNE_CONTROL TMPDIR=en/tmp-suite python3 -B -m unittest discover -s tests -t .` | `Ran 405 tests in 46.920s`, `OK (skipped=2)`, sortie 0 |
| 15:52:33 | étape rouge sur le module factice : `python3 -B tests/lancer_tests.py outils-factice` | `Ran 90 tests`, `FAILED (failures=72)`, 0 erreur, sortie 1 |
| 15:59:15 | étape verte 1 sur `outils` | 1 échec : `test_main_conforme` (le « EN » d'un titre de test pris pour le mot français « en ») |
| 15:59:37 | étape verte 2, après correction (mots tout en capitales exclus des résidus) | `Ran 90 tests`, `OK` |
| 16:16:34 | contrôle 1, traduction `e9c912f9…` | NON CONFORME (1, 2, 3, 5, 7). Les 205 problèmes de structure viennent de la l.431 de la source, suite de paragraphe qui commence par une barre verticale, prise pour une ligne de table |
| 16:18:11 | étape rouge 2 | 3 échecs : `test_mots_composes_non_comptes`, `test_unites_ligne_pipe_dans_paragraphe`, `test_unites_table_avec_delimiteur` |
| 16:18:30 | étape verte 3 | `Ran 93 tests`, `OK` |
| 16:18:43 | contrôle 2, traduction `2e76e52e…` | NON CONFORME (2, 5, 7) |
| 16:19:21 | étape rouge 3 | 2 échecs : `test_libelles_espaces_normalises`, `test_mots_tiers_non_compte` |
| 16:19:22 | étape verte 4 | `Ran 95 tests`, `OK` |
| 16:19:32 | contrôle 3 | NON CONFORME (7 : registre, dans la note du terme « valider ») ; amendement A-4 |
| 16:19:44 | contrôle 4, traduction `1fe6ca70…`, glossaire `e8fd4ee9…` | CONFORME, sortie 0 |
| 16:20:06 à 16:21:19 | paires de relecture écrites, relecture des 410 unités, retouches de forme | — |
| 16:21:20 | assemblage final `97211cd0…`, contrôle 5 | CONFORME, sortie 0 |
| 16:21:46 | gates réelles sur la copie réduite | S-G4 VERT, S-G5 VERT (détail plus bas) |
| 16:23:12 | étape rouge 4, puis étape verte 5 | 1 échec (`test_nombres_echanges_dans_une_unite`), puis `Ran 96 tests`, `OK` |
| 16:23:13 | contrôle 6 | CONFORME, sortie 0 |
| 16:25:25 | étape verte 6 | `Ran 97 tests`, `OK` |
| avant 16:30 | campagne de mutants, passages 1 et 2 | invalides, refaits, non comptés : un octet 0x5c dans MC-28 au passage 1 ; MC-65 FATAL au passage 2 |
| 16:30:01 | campagne de mutants, passage 3 : `python3 -B mutants/campagne_mutants.py` | `BILAN : 97 mutants ; tués 97 ; vivants 0 ; FATAL 0 ; témoins OK` |
| 16:30:48 | contrôle final avec `--table TABLE-CORRESPONDANCE-EN.md` | `VERDICT : CONFORME — onze contrôles sur onze (sortie 0)` |
| 16:34:33 | contrôle 7 (sans `--table`) et réassemblage depuis les parties | sortie identique hors ligne de table ; sha256 du réassemblage = `97211cd0…` |
| 16:34:43 | étape verte 7 sur `outils` ; module factice | `Ran 97 tests`, `OK`, sortie 0 ; factice : 79 échecs sur 97, sortie 1 |
| 16:36:12 à 16:37:00 | suite `s2-harness`, après (même commande) | `Ran 405 tests in 47.050s`, `OK (skipped=2)`, sortie 0 ; `git status` 0 ligne |
| 16:43:22 à 16:45:26 | écriture de ce journal ; gates sur une copie qui le contient | S-G4 VERT (5 fichiers), S-G5 VERT |
| 16:47:27 | relevé informatif de l'emploi des termes : `python3 -B explo/termes_survey.py SOURCE TRADUCTION` (88 règles) | 23 manques à inspecter (`explo/termes_survey-1.sortie.txt`) ; 22 expliqués ; 1 sens absent du glossaire : « écarts médians du contrôle d'horloge » (l.871), rendu `median offsets` |
| 16:48:57 à 16:49:06 | amendement A-5 du glossaire | module `9a44cda6…` |
| 16:49:13 | réassemblage ; étape verte 8 ; contrôle final avec `--table` | traduction `ad5289a9…` (seule la l.716, ligne du glossaire final, change) ; `Ran 97 tests`, `OK`, sortie 0 ; CONFORME, sortie 0 |
| 16:49:26 | relevé des termes refait, règle « écart » complétée par `offsets?` | 22 manques, tous expliqués (section suivante) |
| 16:49:37 à 16:50:14 | campagne de mutants, passage 4, sur la traduction amendée | `BILAN : 97 mutants ; tués 97 ; vivants 0 ; FATAL 0 ; témoins OK` ; sortie identique à l'octet à celle du passage 3 |
| 16:50:28 | gates réelles sur la copie mise à jour | S-G4 VERT, S-G5 VERT, S-G6 VERT ; sortie identique à l'octet à celle de 16:21:46 |
| 16:51:41 à 16:52:25 | suite `s2-harness`, finale (même commande) | `Ran 405 tests in 43.517s`, `OK (skipped=2)`, sortie 0 |

## Chiffres recomptés (sortie finale du contrôle, recopiée)

Commande : `python3 -B outils/controle_en.py /home/user/shogen/docs/publication/11-mesures-pilotes-public.md 11-pilot-measurements-public-en.md --table TABLE-CORRESPONDANCE-EN.md` (dans `en/`).

```text
--- 1. Structure et alignement ---
  unités : source 410 ; traduction : corps 410, en-tête ajouté 2, glossaire final 116
  titres alignés : 58 ; blocs de code : 9 ; lignes de table : 133
--- 2. Nombres (par unité, puis global) ---
  composites : source 1037 distincts / 2491 occurrences ; traduction 1037 distincts / 2491 occurrences
  suites de chiffres : source 806 distincts / 3785 occurrences ; traduction 806 distincts / 3785 occurrences
  multiensemble global normalisé : inventés 0, perdus 0 — identique
--- 3. Citations ---
  source : 120 citations « … » de premier niveau, 96 distinctes ; traduction (corps) : 78 gardées « … », 43 traduites “ … ”
--- 4. Gloses (première occurrence) ---
  gloses déclarées 55 ; trouvées dans le corps 55
--- 5. Passages protégés et libellés de verdict ---
  30 passages protégés ; 7 libellés comptés
--- 6. Motifs interdits (0 exigé dans la traduction) ---
  46 motifs ; présents dans la source : 0 ; dans la traduction : 0
--- 7. Registre du doc 09 en anglais (S-G4 comprise) ---
  15 locutions S-G4 + 52 locutions anglaises + motif « k sources » ; occurrences admises : 2
VERDICT : CONFORME — onze contrôles sur onze (sortie 0)
```

Les nombres écrits en lettres, comptés par langue de zone, sont identiques des deux côtés :
`{'0': 1, '1/2': 1, '10': 2, '14': 1, '1er': 15, '2': 44, '2e': 15, '3': 6, '4': 8, '5': 4, '6': 1, '7': 4, '8': 2}`.

Les 43 citations “ … ” du corps se décomposent ainsi :
- 42 citations traduites (41 textes distincts) ;
- la citation anglaise “is not a CA cert”, déjà présente dans la source.

On retrouve les 120 citations de premier niveau de la source : 78 gardées + 42 traduites. On retrouve aussi ses 96 textes
distincts : 55 gardés + 41 traduits (recompte par `citations_fr` et `citations_en` sur la source et sur le corps).

Les 2 occurrences admises au registre sont la glose `10 sources / 11 feeds` du libellé scellé « 10 sources / 11 flux ».
On la trouve dans la table du §2.2 et dans le glossaire A.

Après l'amendement A-5, la sortie du contrôle ne diffère de la précédente que par les empreintes de la traduction et
du glossaire (comparaison par `diff`, empreintes neutralisées) : tous les comptes ci-dessus restent valables.

## Emploi des termes (relevé informatif, hors contrôle à gate)

Le contrôle compare le glossaire final au module, mais il ne vérifie pas l'emploi des 54 lignes de termes dans le corps.
Le relevé `explo/termes_survey.py` mesure cet emploi :
- 88 règles français → anglais ;
- pour chaque paire d'unités alignées hors code, si la zone française (hors code et hors « … ») porte le terme, la zone
  anglaise (hors code, hors « … » gardées, hors gloses) doit porter l'une de ses formes anglaises.

Le premier passage relève 23 manques. L'un d'eux est un sens absent du glossaire, d'où l'amendement A-5. Le second
passage relève 22 manques, tous expliqués à la main (`explo/termes_detail.sortie.txt`) :
- 5 dans des libellés scellés gardés en français, glosés à leur première occurrence : `strate` ×2, `panne` ×1,
  `[SENSIBILITÉ]` ×2 ;
- 3 où « rendu » est un participe (`rendered`, `returned`), et non le nom du glossaire ;
- 9 où le terme est rendu par un composé à trait d'union, que les bornes du relevé excluent : `degraded-host`,
  `oracle-class`, `single-execution` ×2, `local-workstation`, `block standard-error` ×2, `raw-journal` ×2 ;
- 2 où une coordination sépare les mots du terme : `multi-resolver and multi-vantage probe`, `main and second J14` ;
- 1 locution figée : « en lecture seule » → `read-only` ;
- 2 symboles gardés dans des formules : `z_pool,bloc` et `z_IF,bloc`.

Ce relevé n'est ni testé ni soumis aux mutants ; il ne remplace pas la relecture (I-5, I-12). La version du script du
premier passage n'est pas gardée : la seule différence est l'ajout de `offsets?` à la règle « écart », par une
substitution exacte contrôlée.

## Tests et mutants

- 97 tests (`tests/test_controle_en.py`, 612 lignes), lancés par `tests/lancer_tests.py`. Contrat du runner : 0 tout
  passe, 1 un test échoue, 3 erreur fatale.
- Étapes rouges : 72 échecs sur 90, puis 3, 2 et 1. Chaque test a été vu en échec au moins une fois, dans une étape
  rouge ou sous un mutant : 97 sur 97 (ligne de la campagne).
- Mutants : 65 de programme (MC-01 à MC-65) et 32 de texte (MT-01 à MT-32, dont MT-30, témoin négatif : la source
  passée comme traduction), soit 97.
- Résultat : 97 tués (sortie 1), 0 vivant, 0 FATAL. Témoins T-0a (tests sur le module réel) et T-0b (contrôle réel sur
  la traduction) : sortie 0.
- Faiblesse trouvée en concevant les mutants : deux nombres échangés dans une même unité gardaient le multiensemble. Le
  contrôle de l'ordre par unité a été ajouté, test d'abord (étape rouge 4).

## Gates réelles sur copie réduite

- Copie `en/gates/copie/` : `Cargo.toml` (racine), `WISHLIST.md`, `docs/09-vocabulaire.md`, les deux brouillons sous
  `docs/publication/`, `s2-harness/README.md`, `s2-harness/RUNBOOK-campagne.md`, `biblio/`. Les deux brouillons de la
  copie ont les sha256 `4de98654…7688` et `97211cd0…072a` à 16:21:46, puis `4de98654…7688` et `ad5289a9…e36d` à
  16:50:28 (après A-5).
- Commande : `/home/user/shogen/target/debug/xtask gates`, lancée dans la copie.
- Résultat (identique aux deux passages) :
  - S-G4 VERT (0 violation, 4 fichiers examinés) ;
  - S-G5 VERT (4 fragments contrôlés, 474 sous le seuil, corpus 155 sur 155) ;
  - S-G6 VERT ;
  - les autres gates sont ROUGES par couverture : `crates/`, `JOURNAL.md` et les documents du modèle de menace sont
    absents de la copie, ce qui est attendu.
- 16:45 UTC, même commande dans `en/gates/copie-g1/` : c'est la même copie, plus ce journal sous
  `docs/G1-lot-DOCS11-EN.md`. Résultat : S-G4 VERT (0 violation, 5 fichiers) ; S-G5 VERT (4 fragments
  contrôlés, 499 sous le seuil). Sortie complète dans `gates/gates-fr-en-g1.sortie.txt`. Le passage a été refait
  sur la version finale du journal ; son sha256 est donné au rapport.

## Écarts déclarés

- **E-1** — Exposition de deux lignes de `docs/pocket-report/` (voir plus haut). Demande de FM-1.1.
- **E-2** — Phrase d'en-tête du brief, point 6 : le mot `validated` est remplacé par `as accepted at validation`.
  - Raison : S-G4 refuse ce mot dans la prose de `docs/**/*.md`.
  - La phrase du brief est gardée dans le module (`ENTETE_PHRASE_BRIEF`).
  - Adjugé le 2026-10-04 : `English translation of the accepted report` (C-1 de la relecture G2, appliquée à
    17:45:42 UTC ; voir l'ajout daté en fin de journal).
- **E-3** — Ajout d'un paragraphe `Translation conventions.` dans l'en-tête. Il dit :
  - ce qui reste en français, et la forme des gloses ;
  - que les citations d'autres documents sont traduites et que l'original prévaut ;
  - la convention des nombres.

  Le brief ne le prévoit pas ; il ne porte aucun nombre. Gardé par adjudication ; une phrase est corrigée par C-2 de
  la relecture G2 (les blocs de code ne sont pas glosés).
- **E-4** — Le glossaire a été amendé après sa fixation (A-1 à A-5). Chaque amendement a son heure et son empreinte.
  - Le contrôle établit que les éléments suivants suivent le module amendé : les titres, les gloses, les citations
    traduites, les passages protégés, les libellés, l'en-tête et le glossaire final.
  - L'emploi des termes dans le corps repose sur la relecture et sur le relevé informatif (section dédiée).
- **E-5** — Corrections de l'outil après les premiers passages réels. Chacune est passée par un test d'abord :
  - tables reconnues par leur ligne de délimitation ;
  - mots composés à trait d'union ;
  - `third party` ;
  - libellés coupés par un retour à la ligne ;
  - ordre des nombres par unité.
- **E-6** — Tests renforcés pendant la conception des mutants :
  - assertions sur les messages de diagnostic ;
  - `test_verifier_donnees_ok` attrape l'erreur fatale et échoue (au lieu de rendre une erreur), après MC-65 FATAL au
    passage 2.
- **E-7** — Pas de ligne propre au lot dans `G0-lots-S2BIS.md` (voir plus haut).
- **E-8** — La base a avancé pendant le lot par des commits de l'orchestrateur : de `c354d15` à `e16956b`, puis à
  `4a31685` (lot PLAN-S2BIS). Les entrées du lot sont identiques sur ces bases (`git diff --quiet`, sortie 0).
- **E-9** — Compaction du contexte : le chemin de transcription proposé n'a pas été ouvert ; trois informations viennent
  de mes relevés d'avant (voir plus haut).

## Limites rendues comme items à former (règle PAROXYSME)

| item proposé | constat | déclencheur |
|---|---|---|
| I-1 (E-2) | formulation de la phrase d'en-tête | adjugé (C-1 de la relecture G2) |
| I-2 (E-3) | paragraphe de conventions ajouté | gardé par adjudication ; corrigé par C-2 |
| I-3 | les 9 blocs de code restent en français, à l'octet ; seuls les libellés du texte courant sont glosés | décision : aide de lecture anglaise hors des blocs, ou non |
| I-4 | bornes du contrôle des nombres en lettres : « neuf » non compté (sens de « nouveau ») ; mots composés à trait d'union et `third party` exclus | relecture G2 |
| I-5 | la fidélité du sens hors des nombres repose sur ma relecture | relecture G2 par un réviseur autre que moi, lecteur des deux langues |
| I-6, SHOGEN-SG5-GUILLEMETS-ANGLAIS-1 | S-G5 n'extrait que les « … » : les citations “ … ” d'un document anglais échappent au contrôle de citation | versement d'un document anglais sous `docs/` |
| I-7, SHOGEN-SG4-CITATIONS-TRADUITES-1 | S-G4 exclut les “ … ”, donc les citations traduites ; mon contrôle les couvre (registre anglais appliqué aux citations traduites) | même déclencheur |
| I-8, extension de SHOGEN-PUBLIC-MENTION-FEU-VERT-1 | la mention `Draft — not published` attend le feu vert écrit de l'investisseur, comme la version française | feu vert |
| I-9, SHOGEN-PUBLIC-EN-SYNCHRO-1 | toute retouche du brouillon français exige la retouche de l'anglais et un nouveau passage du contrôle | retouche de la source |
| I-10 | réponses de l'investisseur citées en traduction ; « go exécution » gardé (A-2) | adjudication |
| I-11, SHOGEN-HARNAIS-COMPACTION-TRANSCRIPT-1 | après compaction, la note de reprise propose le chemin de la transcription de session (`*.jsonl`), pièce interdite ; un worker qui la suit enfreint le brief | clause de brief, ou fiche worker |
| I-12, SHOGEN-PUBLIC-EN-TERMES-1 | l'emploi des termes du glossaire dans le corps n'est mesuré que par un relevé informatif, sans tests ni mutants | relecture G2, ou prochaine retouche du contrôle |

## Observation

O-1 : le brief cite la demande de l'investisseur avec l'orthographe corrigée (« doit être »). L'entrée du JOURNAL, dite
verbatim, porte « daoit étre ». L'écart est sans effet sur le lot.

## Empreintes des livrables à 16:53 UTC (sha256, `en/`)

Valeurs d'avant la relecture G2 ; celles de fin de passe sont dans l'ajout daté en fin de journal.

| fichier | sha256 |
|---|---|
| `11-pilot-measurements-public-en.md` (760 lignes, 110 747 octets) | `ad5289a9bf0e917adae37ba1589dbb77b265a21fe283f49d1435fec8d692e36d` |
| `TABLE-CORRESPONDANCE-EN.md` (64 lignes) | `a647b9b305290e72099f3d2c564810ffb2315c85853e92dcadfea3a8a249cf2d` |
| `controle_en.sortie.txt` | `386bacc772f260788beac3ad129329f644bf2d44c18cc469da233a680c0a173f` |
| `outils/controle_en.py` (1114 lignes) | `f4eb2fb3a45433aec7d5c6d71209a75080eb30529653639e01a30f9df213ea8c` |
| `outils/glossaire_en.py` (492 lignes) | `9a44cda655195310810b3b24504fcc7809b49fa62495df0ef23a15b449155d9c` |
| `outils/assembler_en.py` | `07f8d40da17b86b6926757e0329fcc7561c69d521746818e5c833c262077a6d0` |
| `outils-factice/controle_en.py` | `ad2546730af2656cbb7bcc0bb0e7d65f56b9cf4a45d33ae6f53887a017723721` |
| `tests/test_controle_en.py` (612 lignes) | `185016348447ecd32195cb3b84668f6ad8ed63b70fb9ed77d41a9e6cb84574be` |
| `tests/lancer_tests.py` | `a21bbddfac23d0c366caf61d4b1706e61a711002b44a4b6a3de0e8410feb0b4f` |
| `tests/etape-verte-8.sortie.txt` | `478dd763507f4d987d0a4b1eb237aa974a0e31567d81985e7ba87fd2cd000174` |
| `mutants/campagne_mutants.py` | `9cab546024bbfc4f8c1551236a61d767264de83a0802335d5a444cebe9af0e3c` |
| `mutants/campagne.sortie.txt` (passages 3 et 4, identiques) | `f966a888e73e7e199ace89fd99bb20f08ec16147b87f42189cc9a7c4854af203` |
| `gates/gates-fr-en.sortie.txt` (16:21:46 et 16:50:28, identiques) | `b68eb8569dc8c6fbc2d008d536ec0b92601dfa45ac15294e2a334146ffa9d023` |
| `explo/termes_survey.py` | `7c9361f24d3609db809adac1b8c1c04304660421dcc120b4e24d41f54c55b5cc` |
| `explo/termes_survey.sortie.txt` | `d02685d3880ad305b0e8347fb31e8cfe480b0c773965197d0ed8d8b1fcd3e236` |
| `explo/termes_detail.py` | `15ef1a02662dcf7d1f6e13372a3a92df13eb70d984e527cb974a059f842c5e28` |
| `explo/termes_detail.sortie.txt` | `af2e631a924926e88c1f1f1b72396cf4b57496a5445f6c9656b27d00ecdbe635` |
| `explo/glossaire-fixation.sha256` | `1ed1127304523588ca807e64d51b37139bb424c8910e6fa9ef6d8e995dc643a6` |
| `tmp-suite/suite-avant.sortie.txt` | `b5181b2f447fb259b78dbd12de248dfa14caa44f20d6d0cf6874f3d046485df2` |
| `tmp-suite/suite-apres.sortie.txt` | `a96ca96889f08ac5a6c26d5c113e375e172c6bcee380001e62ab8596fa7b2e8b` |
| `tmp-suite/suite-finale.sortie.txt` | `5e84d3246d88e97ed2797003f068e8c11172bacd6a1796ab2127ae1a679ef482` |

Version de la traduction avant A-5 gardée pour comparaison : `explo/traduction-avant-A5.md`
(`97211cd0df8e7b4d3b941f2b19871145c3fa9556669b12b50ee56be73388072a`). Elle ne diffère de la version finale que par la
l.716.

Octets 0x5c : 0 dans les livrables du lot (traduction, table, `outils/`, `outils-factice/`, `tests/*.py`,
`mutants/`, `parties/`, ce journal), compte fait sur les octets écrits. En portent sept scripts d'exploration
(`explo/ctx.py`, `distinctes.py`, `mots.py`, `premiers.py`, `quotes.py`, `survey.py`, `verif_glossaire.py` : de 3 à
16 octets chacun, échappements Python écrits sans gabarit) et deux sorties (`tests/etape-rouge.sortie.txt`,
`explo/factice-final.txt` : 2 chacune) ; les comptes du journal qui venaient de ces scripts sont refaits par le
contrôle (contrôle 3 : 120 citations, 96 distinctes). Aucun marqueur de tâche ouverte (R-13).

## Résumé court

La traduction anglaise du brouillon public est écrite, mais elle n'est pas publiée. Elle garde la structure de la
source : 58 sections, 410 unités alignées, 9 blocs de code identiques à l'octet. Les nombres sont identiques, unité par
unité et dans l'ordre (0 inventé, 0 perdu). Les sorties, verdicts et libellés scellés restent en français ; chacun porte
une glose anglaise à sa première occurrence (55 gloses) et figure au glossaire final.

Le contrôle par script rend 0 motif interdit et 0 formule du registre hors exception déclarée ; il passe 11 contrôles
sur 11. Les gates S-G4 et S-G5 sont vertes. 97 tests sont verts, et 97 mutants sur 97 sont tués. Un relevé informatif
de l'emploi des termes a conduit à un amendement du glossaire (A-5) ; ses 22 manques restants sont tous expliqués.

Deux écarts étaient à adjuger : la phrase d'en-tête (E-2) et le paragraphe de conventions (E-3) ; ils le sont depuis
(ajout daté en fin de journal). L'exposition E-1 est
déclarée ; elle demande un FM-1.1.

## Ajout daté du 2026-10-04 (17:41 à 17:5x UTC) : corrections de la relecture G2 et retouche E-19 de la source

Demande de l'orchestrateur (message reçu à 17:41 UTC) : appliquer les corrections C-1 à C-10 de la relecture G2
bilingue, puis reporter dans la traduction la retouche E-19 de la source française. Ensuite, rejouer les contrôles et
ajouter les tests nécessaires, rouges avant, verts après. Mettre aussi à jour la table anglaise. Gate 0 :
`claude-opus-5-5`, conforme.

### Pièces d'entrée (sha256 recomptés)

- Relecture G2 `en/g2/G2-DOCS11-EN.md` : `14e1d7183d82f9221d7a575f881f5dc74534447ebc276d2edf5d6bc3610fe6cf`, égal au
  message [lu, intégral]. Verdict : ACCEPTE-AVEC-CORRECTIONS, liste fermée C-1 à C-10.
- `en/g2/appliquer_corrections.py` : `26e3e0c9…fcb0` [lu, intégral].
- `en/g2/corrections-G2.diff` : `09a641ba…d1a9` [abs] ; la comparaison porte sur les empreintes attendues du rapport.
- Nouvelle source : `docs/publication/11-mesures-pilotes-public.md`, commit `786a865` de 17:42:34 UTC, identique à
  `…/s2bis/docs11pub/11-mesures-pilotes-public.md`. Empreinte `c101998bb0bb9ea7107475f8c42b0f450f835ec6dfadfae8246ff86f15d16561`,
  égale au message.
  - [lu] l.3 à 14 et l.1066 à 1081.
  - Diff complet contre la version `4de98654…` (extraite de `c354d15` par `git show`, copie `explo/source-4de98654.md`) :
    2 lignes changent, l.11 et l.1076.
- `…/docs11pub/TABLE-CORRESPONDANCE.md` : `d78b65fd…040ec` [lu, partiel] : en-tête (l.1 à 8) et lignes E-19a et E-19b
  (l.33 et 34) ; le reste n'a pas été affiché.
- Base : HEAD `786a865859e5216b9309fad773e0c26a7d5c83c3` de 17:44 à 17:52 UTC ; `git status` 0 ligne.

### Étapes (heures `date -u`)

| heure UTC | étape | résultat |
|---|---|---|
| 17:44:41 | archive de l'état livré (`archive/avant-G2-E19/`, empreintes dans `explo/archive-avant-G2-E19.sha256`) | 17 fichiers ; empreintes égales à celles de ce journal (traduction `ad5289a9…`, journal `5a738619…`) |
| 17:44:49 à 17:45:34 | suite `s2-harness`, avant | `Ran 405 tests in 44.127s`, `OK (skipped=2)`, sortie 0 |
| 17:45:42 | `python3 -B g2/appliquer_corrections.py` sur le dossier du lot | `15 remplacements appliqués dans 6 fichiers`, sortie 0 |
| 17:45:42 | comparaison avec les valeurs attendues de la relecture | égalité : p1 `396f0648…`, p2 `03ed057e…`, p3 inchangée, p4 `a7d4b623…`, p5 `39a8e3ab…`, module `65591349…`, campagne `32615ccb…` |
| 17:45:51 | réassemblage contre l'ancienne source ; contrôle avec `--table` | traduction `f8865abe…`, table `9aedd60d…` : égales aux valeurs attendues ; CONFORME, sortie 0 ; seules les l.3, 5, 7, 182, 457, 468, 529, 579, 635, 693 et 694 changent |
| 17:45:58 | contrôle : nouvelle source, traduction corrigée, données d'avant | `FATAL : P-30 : passage protégé absent de la source`, sortie 3 |
| 17:46:33 | tests écrits avant le code (3 de `TestEpingleSource`, plus `test_main_source_non_epinglee`) ; `SOURCE_SHA256` ajouté aux données réduites des tests | 101 tests |
| 17:46:48 | étape rouge 5 : `verifier_epingle` déclarée sans effet | `FAILED (failures=3)`, sortie 1 (`test_epingle_absente`, `test_epingle_autre_source`, `test_main_source_non_epinglee`) ; module factice : 82 échecs sur 101 |
| 17:46:59 | épingle écrite et appelée par `main` | étape verte 9 : `Ran 101 tests`, `OK`, sortie 0 |
| 17:47:27 | amendements A-6 (corrections C-1, C-5, C-6 dans le module) et A-7 (E-19) du glossaire | module `4beaf064…` |
| 17:47:49 | contrôle : nouvelle source, traduction sans E-19, données amendées | NON CONFORME, sortie 1. Seul le contrôle 5 échoue : P-30 à P-33, source 1, traduction 0 |
| 17:47:49 | même contrôle, avec l'ancienne source | `FATAL : source non épinglée`, sortie 3 |
| 17:47:57 | traduction des deux passages E-19 (`parties/p1.md`, `parties/p5.md`) | — |
| 17:48:04 | réassemblage contre la nouvelle source ; contrôle avec `--table` | traduction `60f7dc7a…` (seules les l.7 et 635 changent) ; CONFORME, onze contrôles sur onze, sortie 0 |
| 17:48:39 | campagne étendue : MC-66 à MC-69 (épingle), MT-33 à MT-35 (E-19), ancrage de MT-15 suivi, témoin T-0c | — |
| 17:48:51 à 17:49:28 | campagne de mutants | `BILAN : 104 mutants ; tués 104 ; vivants 0 ; FATAL 0 ; témoins OK` ; T-0c : sortie 3, refus attendu ; 101 tests vus en échec |
| 17:49:40 | étape verte 10 ; module factice ; relevé des termes | `Ran 101 tests`, `OK` ; factice : 82 échecs ; 22 manques, les mêmes qu'avant |
| 17:49:49 | gates sur la copie réduite (nouvelles versions des deux brouillons) | S-G4 VERT, S-G5 VERT, S-G6 VERT ; sortie identique à l'octet à celle de 16:50:28 |
| 17:50:36 | C-10 appliquée à ce journal (texte exact du rapport G2) | — |
| 17:51:43 à 17:52:28 | suite `s2-harness`, après | `Ran 405 tests in 44.474s`, `OK (skipped=2)`, sortie 0 |

### Textes traduits (retouche E-19)

- E-19a, en-tête de la source :
  `the sealed package, the seal, the renderings, the records and the scripts are provided on request, under agreement`.
- E-19b, §12 :
  `The sealed package, the seal, the renderings, the records and the scripts are in the same private repository and are not published: documents provided on request, under agreement. Checking the seal requires the sealed package, which is provided together with the seal on request: a third party who is given the sealed package, the seal and the renderings without the journals can check the seal and the arithmetic of the renderings, not recompute the renderings.`
- Choix de traduction :
  - `records` rend « enregistrements » (glossaire B) ;
  - `together with` rend « avec », dans « remis avec le sceau ».
- Aucun nombre n'est ajouté ni changé.
- Les passages protégés P-30 à P-33 obligent le contrôle à trouver ces textes dans la traduction.

### Épingle de la source

- `verifier_epingle` refuse toute source dont le sha256 diffère de `SOURCE_SHA256` (glossaire). Le contrôle sort alors
  en 3, avant tout calcul.
- L'épingle mécanise en partie I-9 (SHOGEN-PUBLIC-EN-SYNCHRO-1) : une retouche du brouillon français arrête le contrôle
  anglais jusqu'à la retouche de la traduction et des données.

### Chiffres recomptés (sortie finale du contrôle, `controle_en.sortie.txt`)

| mesure | source | traduction |
|---|---|---|
| unités | 410 | 410, plus 2 d'en-tête et 116 de glossaire |
| titres | 58 | 58 |
| blocs de code | 9 | 9 |
| composites | 1037 distincts / 2491 occurrences | 1037 distincts / 2491 occurrences |
| suites de chiffres | 806 / 3785 | 806 / 3785 |
| nombres inventés, perdus | — | 0, 0 |
| citations « … » de premier niveau | 120 (96 distinctes) | 78 gardées, 43 “ … ” traduites |
| gloses | — | 55 |
| motifs interdits (46) | 0 | 0 |

Passages protégés : 33. Libellés comptés : 7. Registre : 2 occurrences admises (même exception qu'avant). Table de
correspondance : 58 sections, toutes « oui » ; elle ne diffère de la table de la relecture que par les deux empreintes.

### Octets 0x5c (recompte de cette passe)

- Périmètre : `en/` hors `g2/`, `archive/`, copies des gates, `tmp-suite/`, `*.jsonl` et `fm11-traducteur.json`, soit
  75 fichiers examinés.
- 11 fichiers portent l'octet :
  - les 7 scripts d'exploration de C-10 ;
  - 4 sorties de tests sur le module factice : `tests/etape-rouge.sortie.txt`, `explo/factice-final.txt`, et deux
    nouvelles de cette passe, `explo/factice-E19.txt` et `explo/factice-final-E19.txt` (2 octets chacune).
- Dans ces sorties, l'octet vient de la représentation Python d'une chaîne dans un message d'assertion de `unittest`,
  pas d'un texte tapé.
- Livrables : 0.

### Écarts de cette passe

- **E-10** — La relecture G2 a été appliquée par son propre script, sur le dossier du lot. Les empreintes obtenues
  égalent ses valeurs attendues.
- **E-11** — `corrections-G2.diff` n'a pas été ouvert. Les empreintes attendues suffisent à la comparaison.
- **E-12** — L'épingle de la source resserre le contrôle, hors de la liste C-1 à C-10. Elle ajoute 4 tests, 4 mutants
  de programme et le témoin T-0c.
- **E-13** — MT-15 change d'ancrage, parce que son texte est retouché par E-19. La mutation reste la même : pièces
  présentées comme remises avec ce rapport.

### Items

- I-G2-5 : traité par la retouche E-19 de la source et par sa traduction.
- I-9 (SHOGEN-PUBLIC-EN-SYNCHRO-1) : en partie mécanisé par l'épingle.
- I-1 et I-2 : adjugés (C-1 ; C-2).
- Restent ouverts : I-3 à I-8 et I-10 à I-12 de ce journal ; I-G2-1 à I-G2-4 de la relecture.

### Empreintes de fin de passe (sha256, `en/`)

| fichier | sha256 |
|---|---|
| `11-pilot-measurements-public-en.md` (760 lignes, 110 993 octets) | `60f7dc7a7b6784a2d528e5d5f2ffe1798bef20b20c12156be688e92a7b2021d6` |
| `TABLE-CORRESPONDANCE-EN.md` (64 lignes) | `74bf368080877d4e2792092e2ad022b8cc9a964e0449311822ab279f228c31b1` |
| `controle_en.sortie.txt` | `80db6884dc1d6d9560d15b74d53b4f893cf6c3fb65840ace92fc78f0659370d6` |
| `outils/controle_en.py` (1126 lignes) | `b42777dbbe9229720c14135ecf9f546e2969028e887512626cd0cc875be0bb4c` |
| `outils/glossaire_en.py` (514 lignes) | `4beaf0643faad055eb87f66d5b7facbdc45823dbe14ded874cdd2335e844d76c` |
| `outils/assembler_en.py` (inchangé) | `07f8d40da17b86b6926757e0329fcc7561c69d521746818e5c833c262077a6d0` |
| `outils-factice/controle_en.py` | `c79890c379568af3020b5a849136fa5ea38d3e04a14dee075a92b2d3e43e858e` |
| `tests/test_controle_en.py` (646 lignes, 101 tests) | `9544da4cfb943a2eef02038f45a59b4c96efbfa4bc6a7bf12916d71343a4675b` |
| `tests/lancer_tests.py` (inchangé) | `a21bbddfac23d0c366caf61d4b1706e61a711002b44a4b6a3de0e8410feb0b4f` |
| `tests/etape-rouge-5.sortie.txt` | `460e2d6f654a62a6a111dbcec3afe4bb2e5934db68cbfecdf07e12974c38787e` |
| `tests/etape-verte-10.sortie.txt` | `91318ad2cacf3cc3455f01b092bbf76b2322471b631018735c00e0ee669e2270` |
| `mutants/campagne_mutants.py` (336 lignes) | `2581f2dded3b97f132459b8d7843da1d0bf847da8d11ef83527af90e1e4cb68f` |
| `mutants/campagne.sortie.txt` | `244e738e1918081b9884eee55c18726dfa9f54bc705f608a0552b0f95a3a8f41` |
| `parties/p1.md` | `10a3898a58e548def8fc43f640421c2eb4eb70b22ea22f5bdc154e530c3cc457` |
| `parties/p2.md` | `03ed057e4f9ce31b2fd046bfb87be92e9544427233e60c1807aa4c1662655946` |
| `parties/p3.md` (inchangée) | `3a434421f3a44831c05b6818a4553c66e7d5a53d0939f9bd144002a6d8d27f85` |
| `parties/p4.md` | `a7d4b623515ff988825687aa72402083e9fc2b67f6f4b6d9a483c0d147ca1b00` |
| `parties/p5.md` | `76812e5796ffa8ab8386096e622332310d642f3a4f598cf4ec3306976cfdc15a` |
| `gates/gates-fr-en.sortie.txt` (identique) | `b68eb8569dc8c6fbc2d008d536ec0b92601dfa45ac15294e2a334146ffa9d023` |
| `explo/termes_survey-E19.sortie.txt` | `824ba75cc15396f96de53f246608cfea90cc1e53e86bd9635857675db6f7c9e1` |
| `explo/source-4de98654.md` (source précédente, pour T-0c) | `4de986544cee9622a0848f585103cea594352df65d02e8f51e6ef4c593fc7688` |
| `explo/traduction-G2-ancienne-source.md` | `f8865abe003189a382c0fe22366a72fbc6614442b4273f99630326cbc31a1b3f` |
| `explo/table-G2-ancienne-source.md` | `9aedd60d0cbe2b024f2c6ea59f2d4c0c58258229ba2a67af5607f4d482107d0c` |
| `explo/archive-avant-G2-E19.sha256` | `4d9e75ceeb6ab8650575a6e47af4e9159b3e22066fc4d2f1d76935ca504b176f` |
| `tmp-suite/suite-avant-G2.sortie.txt` | `26be1114d60bdce28191e3ef4c8b8dae7601499a6349e556a40a1cc5b6964e8b` |
| `tmp-suite/suite-apres-G2.sortie.txt` | `980e84087314d99569283329497cf4ea7713e0293fe9a3646d937481fec42a7e` |

### Résumé court de la passe

- Les dix corrections de la relecture G2 sont appliquées : neuf par le script du réviseur, aux empreintes attendues, et
  C-10 à la main dans ce journal.
- La retouche E-19 est traduite : la liste des pièces remises sur demande, sous accord, et la phrase sur le contrôle du
  sceau.
- Le contrôle épingle désormais la source française. Toute autre version l'arrête (sortie 3).
- Résultats :
  - contrôle : onze points sur onze, avec des nombres identiques ;
  - tests : 101 verts, après une étape rouge de 3 échecs ;
  - mutants : 104 tués sur 104 ;
  - gates S-G4 et S-G5 : vertes ;
  - suite `s2-harness` : verte avant et après.
