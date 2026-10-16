# Contre-contrôle de DETTES-T6 (passes 1 et 2 ; clôture CONFORME) (transcrit)

> Transcription par l'orchestrateur le 2026-10-10 09:08:09 UTC du fichier g2/cc/RAPPORT-CC.md ; contrôle FM-1.1 des transcripts du générateur-correcteur, du réviseur G2 et du contre-contrôleur, par le fm11.py versé et par celui de DT3-E : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# RAPPORT-CC — contre-contrôle neuf du lot DETTES-T6 (corrections C-1 à C-10 de la G2, recalage +1)

- **Rôle** : contre-contrôleur neuf (fiche `shogen-worker`) ; n'a ni écrit ni relu le lot. **Gate 0** : modèle résolu
  `claude-opus-5-5` (identifiant exact de l'invite système), écrit en tête de `NOTES.md` avant tout travail. Effort : non
  lisible depuis la session (fiche : `max`).
- **Brief** : `BRIEF-CC.md` `bc5d30e0c6b5d1544fabc7a7a970d6d1d818aedf7a5403f2c2e7ef52af2e186a` (préfixe attendu : conforme).
- **Heures** (`date -u`) : ouverture 2026-10-10 02:54:05 UTC ; rendu : §12.
- **Objet** : série `diffs/DT6-a.diff` à `DT6-k.diff`, dans l'ordre ; empreinte de la concaténation recalculée
  `d70806e0a35260a887652c4ca51b2ab999ecaa26521dae0b7107e2974da31006` = brief ; `SHA256SUMS` du lot : 13 OK. Base :
  `ba5ea95709e122349448c5e3f024b0ca08d83e91` (versement DETTES-T5).
- **Copie** : `tmp/clone` (`git clone --no-hardlinks --no-checkout` du dépôt, sparse non-cone : `/*` moins `docs/15-*`,
  `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`,
  `docs/adr-0028/execution/`, `*.jsonl`), checkout `ba5ea95` : 58 entrées sautées, 0 `.jsonl` extrait, dossiers interdits
  absents (contrôlés par nom). D.2 lue à l'annexe D (l.32-47, admise) : ses pièces sont hors du dépôt (poste local, lecteur F:,
  monark-governance, transcriptions) ou dans les exclusions (`docs/rapports/` l.51, `docs/adr-0025/` l.14, `*.jsonl`).
- Dépôt lu seulement (`git --no-optional-locks`), aucune écriture git dans le dépôt, aucun commit, aucun push ;
  `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée ; toute suite et toute campagne réseau coupé (`outils/iso.sh` : `isole.sh` de
  p1b `ebaa1c78…8a3e`, `lo_up.py` `b532be4b…083e`, puis `env -u SHOGEN_S2_CAMPAGNE_CONTROL -u HTTPS_PROXY -u HTTP_PROXY
  -u https_proxy -u http_proxy -u ALL_PROXY -u all_proxy -u NO_PROXY -u no_proxy`, `PYTHONDONTWRITEBYTECODE=1`, TMPDIR du
  dossier) ; un seul processus lourd à la fois ; `df -h /` avant chaque compilation (7,2 à 8,5 Go libres).

## 1. Verdict

**CONFORME-AVEC-RÉSERVES (R-1 à R-7).** C-1 à C-10 sont faites dans la forme du réviseur (`s2bis/` de DT6-k identique
octet pour octet à `G2-corrections.diff` ; deux écarts, tous deux demandés par l'adjudication : §3), justes, et leurs
rouges se reproduisent ; le recalage est exact (Ran = plancher à chaque état 0, a à k ; sections METRIQUES cohérentes,
tableaux recomptés) ; toutes les vérifications rejouées sont vertes, hors S-G9 sur la copie creuse (attendu). Constats :
- **R-1 (code, défaut de DT6-e, même classe que C-1)** : une `sante` JSON valide hors FORMAT (`ws` entier, `d3` au code 0,
  partie entière de System time de 4 301 chiffres) fait encore lever `status` et `resume` (`ValueError`, limite de
  conversion de `int()`), contre « jamais une trace » (I-3 de STATUS-QUEUES-1) ; forme exacte : `propose/R-1.diff`.
- **R-2 à R-6 (tests)** : cinq de mes douze mutants vivent sur l'état final, tous non équivalents, chacun une ligne de
  la série ou d'un item non figée par un test ; forme exacte : `propose/R-2.diff` à `R-6.diff` (tests seuls).
- **R-7 (texte)** : la phrase de fermeture proposée pour STATUS-QUEUES-1 dit « en dernière ligne du rapport » ; avec
  `--depot`, le compte à quorum suit : « du rapport local ».

Les sept réserves s'appliquent après DT6-k (R-1 à R-6 dans tout ordre essayé, même résultat ; R-25 +39 au total) ; avec
elles, la suite reste à 358 (cas ajoutés dans des tests existants) et les cinq vivants sont tués par la commande du job
(§6.2).

## 2. C-1 à C-10 : forme, justesse, rouge puis vert, défaut neuf

Forme : `s2bis/` de l'état j + DT6-k est identique octet pour octet à l'état j + `G2-corrections.diff`
(`2b6d931a…94ab`, `git apply --check` puis `git apply` sur l'état j recalé ; `diff -r`). Rouges rejoués par moi, sur
l'état k : C-1 et C-2 avec le `status.py` de l'état j ; C-5 à C-9 avec des mutants de mes formes, chacun sur la ligne
que le test éprouve, puis le même mutant sous les tests de l'état j (test absent : OK). Sorties :
`sorties/rouge-k-code.txt`, `sorties/rouges-C5-C9.json`.

| correction | forme du réviseur | juste (lu sur le code) | rouge (k) / tests de j | défaut neuf |
|---|---|---|---|---|
| C-1 (`ws` non entier jamais une clé) | identique | oui : `derniere` pour toute `sante`, `en_cours` et le relevé D-3 pour un `ws` entier seul ; aucun autre lecteur de `en_cours` | FAIL (`'TypeError' != "disque : non relevé ({'libre': 11})"`) | aucun ; mais la même classe de trace reste ouverte par une autre entrée (R-1, défaut de DT6-e) |
| C-2 (compte exact de la grille) | identique | oui : `len(range(debut, max(juges) + W, W))` = taille de la grille allouée ; `n` borné (début ≥ plancher, `ws` < fin du jour d'un nom AAAA-MM-JJ) : aucun `OverflowError` | FAIL (`RefusStatus not raised`) ; avec C-1 : FAIL 2, ERROR 0, comme le générateur | aucun |
| C-3 (sorties mêlées dans l'ordre des écritures) | identique (FORMAT §13.3, docstring de `horloge_systeme`, METRIQUES DT6-e) | oui : `stderr=subprocess.STDOUT`, un seul tube | sans objet (texte) | aucun |
| C-4 (« adoptée ») | identique (§17.2) | oui (adjudication Q-1) | sans objet | aucun |
| C-5 (`illisible (FileNotFoundError)`) | identique | oui : lien vers un absent, `os.open` lève, motif nommé | FAIL 1 sur « OSError non rattrapée » ; j : OK | aucun |
| C-6 (`ligne coupée` d'une ligne de plus de LIMITE) | identique | oui | FAIL 1 sur `readline()` ; j : OK | aucun ; borne exacte non figée : R-2 |
| C-7 (Root delay, Root dispersion, `sortie` non texte) | identique | oui (fenêtres 18 à 20 : D-3, dernier lisible à la fenêtre 15 ; marqueur sans `sante` porté à 21) | FAIL 1 sur chacun des trois contrôles retirés ; j : OK | aucun |
| C-8 (`_synchro` sans attente) | identique | oui : veille non sommée, tube posé après `stat`, `_synchro` ouvre en `O_NONBLOCK`, `_empreinte` refuse | FAIL 1 (« bloqué ») sur `O_NONBLOCK` retiré ; j : OK | aucun (O-1) |
| C-9 (1 à 10 chiffres) | identique | oui | FAIL 1 sur `[0-9]+` et sur `{1,9}` ; j : OK | aucun |
| C-10 (`ligne coupée` passagère) | identique (§17.4) | oui : la ligne en cours n'a pas de saut de ligne, `status` la lit coupée ; mesure du réviseur [2nd] | sans objet | aucun |

Défaut neuf dû aux corrections : aucun. Lignes ajoutées de plus de 120 caractères, `TODO`/`FIXME`, octet 92, blanc
final : aucun, dans DT6-a à DT6-k (1 118 lignes ajoutées) comme dans R-1 à R-6 (`outils/lignes.py`).

## 3. DT6-k comparé à `G2-corrections.diff` : écarts

Comparaison des arbres (état j + l'un, état j + l'autre ; `diff -r`), puis des diffs :
1. **FORMAT, ajout daté DETTES-T6** : date portée de « 2026-10-09 23:42:21 UTC » à « 2026-10-10 01:18:37 UTC », et
   phrase ajoutée « ; le diff DT6-k porte les corrections C-1 à C-10 de la G2 du lot (§13.3, §17.2, §17.4) ».
   Demandé par l'adjudication (« date de l'ajout daté du FORMAT reportée ») ; l'heure est celle que le journal du
   générateur donne pour sa dernière écriture du FORMAT (`NOTES.md` du lot l.150-151, [2nd]) ; aucune écriture du FORMAT
   ne la suit dans la série (le recalage ne touche que `gates.yml` et les lignes « Suite » de METRIQUES).
2. **METRIQUES** : section « DT6-k (2026-10-10) : corrections C-1 à C-10 de la G2 du lot » (34 lignes). Demandée par
   l'adjudication. Contenu vérifié : objet exact ; rouges reproduits (§2) ; tableau recompté (status.py 275, sante.py 111,
   test_status.py 535 et 24 tests, test_reprise.py 383 et 28, test_asn.py 151 et 6 : exact) ; « Suite : 358 » = état k ;
   « 13 mutants, 13 tués » : [2nd].
Aucun autre écart : les hunks de `status.py`, `sante.py`, des trois tests, du FORMAT (§13.3, §17.2, §17.4) et de la
section DT6-e de METRIQUES sont ceux du réviseur (seuls les numéros de ligne des en-têtes changent, par le recalage).

## 4. Recalage (+1) : planchers exacts et METRIQUES

Copie `tmp/clone` à `ba5ea95`, puis DT6-a à DT6-k appliqués un à un (`git apply --check` puis `git apply`) ; à chaque
état, le job `s2bis-unittest` entier, blocs `run` lus dans le `gates.yml` de l'état (`outils/etats.sh`,
`sorties/etats/`). Chaque état : runner « 137 ok, 0 échec », puis :

| état | plancher de `gates.yml` | verdict (ligne du vérificateur) | METRIQUES « Suite » de la section |
|---|---|---|---|
| 0 (ba5ea95) | 342 | conforme (code 0, résumé final, aucun saut, Ran = 342) | — |
| a | 344 | conforme, Ran = 344 | DT6-a : 344 |
| b | 345 | conforme, Ran = 345 | DT6-b : 345 |
| c | 347 | conforme, Ran = 347 | DT6-c : 347 |
| d | 351 | conforme, Ran = 351 | DT6-d : 351 |
| e | 353 | conforme, Ran = 353 | DT6-e : 353 |
| f | 354 | conforme, Ran = 354 | DT6-f : 354 |
| g | 355 | conforme, Ran = 355 | DT6-g : 355 |
| h | 356 | conforme, Ran = 356 | DT6-h : 356 |
| i | 358 | conforme, Ran = 358 | DT6-i : 358 |
| j | 358 | conforme, Ran = 358 | (pas de section : commentaire YAML) |
| k | 358 | conforme, Ran = 358 | DT6-k : 358 |

0 « Exception ignored » et 0 « Warning » à chaque état. Les 29 lignes des tableaux « fichier | lignes | tests » des
sections DT6-a à DT6-k, recomptées à l'état de leur section (états reconstruits `tmp/etats/0..k`, l'état k égal à la
copie finale ; `wc -l`, et tests par `unittest` `countTestCases`, `outils/tables.py`) : toutes exactes. R-25 recompté
(`git apply --numstat`, `.py` et `.yml`) : a 77, b 26, c 71, d 107, e 144, f 67, g 71, h 47, i 46, j 4, k 49 (= §10 du
rapport du générateur ; chacun ≤ 200).

## 5. Rejoue sur l'état final (ba5ea95 + DT6-a à DT6-k)

Lignes exactes des jobs, lues dans le `gates.yml` de la copie (`outils/job.py`, blocs `run` dans l'ordre) et lancées comme
`shell: bash` (`bash --noprofile --norc -eo pipefail`), réseau coupé ; `python3` = python3.12 (3.12.3, interpréteur de
l'image ubuntu-24.04) par un lien en tête du PATH ; sorties complètes `sorties/final/`.

| vérification | résultat |
|---|---|
| runner `enforcement/tests/run-fixtures-verdict-suite-s2.py` | `verdict-suite-s2 : 137 ok, 0 échec` (dans chaque job) |
| s2bis (`--aucun-saut --egal --plancher 358`) | `conforme (code 0, résumé final, aucun saut, Ran = 358)` |
| S2 (`--egal`) | `conforme (code 0, résumé final, sauts nommant SHOGEN_S2_CAMPAGNE_CONTROL, Ran = 419)` (OK, skipped=2) |
| sim-bis (279) ; calib-actifs (65) ; controle (36) | conformes, aucun saut, Ran = 279 ; 65 ; 36 |
| g1 : `runners-epingles.py .` | `runners-epingles : conforme (7 workflow(s), 22 clé(s) runs-on/os lues)` |
| g1 : workflows-yaml (cas, puis arbre) | `16 ok, 0 échec (16 cas joués, 16 exigés)` ; `conforme (7 workflow(s), PyYAML 6.0.1)` (python3-yaml 6.0.1-2build2 déjà présent : branche apt non prise ; `/usr/bin/python3` = 3.11.15 ici) |
| g1 : lint R-1 (cas, puis arbre) | `model-pinning : 227 ok, 0 échec` ; `OK (R-1) : 7 fichier(s)` |
| g1 : `journaux-modele.py .` | `conforme (52 journaux exemptés par nom et sha256)` |
| g1 : `docs-sha256sums.py .` | `conforme : 35 SHA256SUMS, 299 ligne(s), dont 11 absente(s) admise(s) (SHOGEN-SIM-SOMMES-1) ; 4 fichier(s) non listé(s), non refusés` |
| g5 : cas du crochet (`run-fixtures-hooks.sh`) | `hooks : 57 ok, 0 échec` (étape `git grep` : non lancée, recherche sur l'arbre interdite) |
| matrice `-X dev -W error`, `PYTHONDEVMODE=1`, `PYTHONWARNINGS=error` | 3.10.20, 3.11.15, 3.12.3, 3.13.14 : conforme, Ran = 358, sortie 0 ; 0 « Exception ignored », 0 « warning » (casse ignorée), chacune |
| `cargo --locked xtask verify` (lignes VERDICT) | S-G1 à S-G6, S-G7a, S-G8 : `VERDICT : VERT (0 violation(s))` (8 lignes) ; S-G9 : `VERDICT : ROUGE (1 violation(s))`, violation `docs/17-modele-de-menace.md:70` (copie creuse, attendu) ; `=== VERDICT GLOBAL : ROUGE — l'intégration s'arrête (ADR-0013, point 1) ===` ; étapes suivantes : `cargo fmt --check : VERT`, no_std : `VERT`, `cargo clippy -D warnings : VERT` ; rien d'autre ne rougit |
| `cargo --locked test`, cible cargo **par défaut** de la copie (règle I-1 : aucun `CARGO_TARGET_DIR`, `.cargo/config.toml` sans `target-dir` ; `tmp/clone/target` absent avant, créé par le run) | 26 lignes `test result: ok.` (passés, dans l'ordre : 0, 15, 5, 2, 3, 18, 3, 5, 4, 17, 11, 0, 0, 8, 6, 42, 9, 10, 11, 0, 0, 81, 9, 0, 0, 0), 259 tests, 0 échec, 0 ignoré |

## 6. Estimateur propre : mutants du contre-contrôleur

Formes écrites par moi (`mutants/cc.py`), distinctes de celles du générateur (sections DT6-a à DT6-k de METRIQUES) et du
réviseur (§7 de sa G2). Commande exacte du job `s2bis-unittest` (runner, puis ligne du vérificateur, lues dans le
`gates.yml` de la copie), réseau coupé, borne de 300 s (dépassement : FATAL), classement SHOGEN-MUT-FATAL-1 (runner en
sortie 0 exigé ; vérificateur : 1 TUÉ, 0 VIVANT, autre FATAL) ; chaque remplacement présent une fois, syntaxe
contrôlée, fichier restauré et contrôlé par sha256 (`outils/campagne.py`) ; témoin T00 d'abord ; copie `tmp/mut` (copie
de l'état final, restaurée : `diff -rq` nul). Durée 46 à 52 s par exécution.

### 6.1 Sur l'état final (`sorties/mutants-cc.{log,json}`)

| id | mutant | verdict | tests en échec |
|---|---|---|---|
| T00 | témoin | VIVANT (conforme, Ran = 358) | — |
| M01 | `status` : `readline(LIMITE + 1)` (borne de C-6) | **VIVANT** | — (R-2) |
| M02 | D-3 : « Delete second » jugé D-3 (`SYNCHRO[:2]`) | TUÉ | `test_d3_jugee_sur_la_sortie_gelee` |
| M03 | D-3 : `codes + ["D-3"]` sans tri | **VIVANT** | — (R-3) |
| M06 | `canonique` : deux-points des clés non comptés | TUÉ | `test_octets_comptes_par_occurrence_avant_le_serialiseur` |
| M07 | `canonique` : l'entier 0 compté 0 octet | **VIVANT** | — (R-4) |
| M08 | `run_params` : `prec` hors du calcul de taille | TUÉ | `test_run_params_qui_passerait_limite_refus_de_configuration` |
| M09 | ASN : 2^32 admis | TUÉ | `test_cymru_premier_txt_lisible_forme_de_s2`, `test_ripestat_forme_de_s2_bornes_et_base_muette` |
| M10 | Cymru : `except ValueError` seul (premier champ vide) | **VIVANT** | — (R-5) |
| M11 | sonde D-3 : sortie gardée à SORTIE + 1 caractères | TUÉ | `test_horloge_systeme_sortie_brute_ou_erreur_typee`, `test_sortie_d_erreur_gardee_dans_la_borne` |
| M12 | D-3 : `code > 0` refusé seulement (code négatif lu comme un succès) | **VIVANT** | — (R-6) |
| M15 | DNS : identifiant 65 536 admis (`<=`) | TUÉ | `test_identifiant_hors_de_16_bits_refus_nomme` |
| M17 | lecture : `_trop_profonde` relâché d'un niveau | TUÉ | `test_copie_du_compte_des_niveaux` (fitness, copie textuelle) |

Bilan : 12 mutants, 7 tués, 5 vivants, 0 FATAL. Équivalents : aucun parmi les vivants (chacun change un comportement
observable : M01 lit une ligne de LIMITE + 1 octets que le FORMAT borne à LIMITE ; M03 publie des codes non triés, que
`lire_resume` des autres observateurs refuse ; M07 viole la borne « au plus 8 fois sa borne » que le test affirme pour une
valeur simple ; M10 fait lever `releve`, documenté « ne lève jamais » ; M12 lit comme lisible le relevé d'une commande
tuée). M17 est équivalent en comportement (`canonique` recompte les niveaux, même verdict) ; seule la copie textuelle
exigée par `test_fitness` le tue. Les mutants tués l'ont été par le test visé (listes d'échecs relues).

### 6.2 Sur l'état final + R-1 à R-6 (`sorties/reserves/`)

Copie `tmp/mut` restaurée (égale à l'état final), R-1 à R-6 appliqués (`--check` puis `git apply`), même commande et
même outil (`outils/reserves.sh`, spécifications `mutants/reserves.py` et `mutants/r1.py`) :

| id | mutant | verdict | test en échec |
|---|---|---|---|
| T00 | témoin | VIVANT (conforme, Ran = 358) | — |
| M01, M03, M07, M10, M12 | les cinq vivants du §6.1 | TUÉS | respectivement `test_fichiers_arretes_avant_leur_fin_nommes`, `test_d3_jugee_sur_la_sortie_gelee`, `test_octets_comptes_par_occurrence_avant_le_serialiseur`, `test_cymru_premier_txt_lisible_forme_de_s2`, `test_d3_jugee_sur_la_sortie_gelee` |
| R1-M1 | R-1 défait (partie entière non bornée) | TUÉ | `test_ligne_hors_format_jamais_une_trace` |
| R1-M2 | borne à 4 300 chiffres | TUÉ | même test (641 chiffres sous la limite 640) |
| R1-M3 | borne à 641 chiffres | TUÉ | même test |
| R1-M4 | borne à 639 chiffres | VIVANT, **équivalent** | — : ne diffère qu'à 640 chiffres ; une sortie réelle en a 19 au plus (O-4) |

Matrice sur cet état (`-X dev -W error`, `PYTHONDEVMODE=1`, `PYTHONWARNINGS=error`) : 3.10.20, 3.11.15, 3.12.3,
3.13.14 : conforme, Ran = 358, sortie 0 ; 0 « Exception ignored », 0 « warning », chacune.

## 7. Items (liste fermée) : la phrase de fermeture proposée est-elle vraie sur le code ?

Phrases : §2 de `RAPPORT-GENERATEUR.md`. Lu sur l'état final.

| item (SHOGEN-S2BIS-…) | jugement | preuve du contre-contrôleur |
|---|---|---|
| CORPS-BORNE-1 | vraie | `_parcours` : chemin = ancêtres de la pile, cycle vu avant `json.dumps`, chaque conteneur développé une fois ; `test_cycle_refuse_avant_le_serialiseur` (espion) vert |
| CANONIQUE-OCTETS-1 | vraie ; R-4 (le compte de 0 n'est pas figé) | `_octets` relu : borne basse pour chaîne (≥ 1 octet par caractère), entier (3/10 < log10 2 ; 0 : 1 chiffre), null/booléens (4), nombre à virgule (3) ; conteneurs : crochets, virgules, clés et deux-points comptés (exact dès un élément ; vide : 1 pour 2) ; rapport 8 (24/3) ; M06 tué, M07 vivant |
| R25-COMPTE-1 | vraie | en-tête de METRIQUES l.9-12 ; compte recompté (§4) |
| DECODEURS-BORNE-TEST-1 | vraie | `test_borne_d_exposant_figee` lu ; cinq sites d'appel de `_entier` (l.66, 85, 104, 105, 109) = cinq gabarits ; docstring exacte |
| JOURNAL-FICHIER-SPECIAL-1 | vraie, avec C-8 à citer | toute lecture de fichier du journal passe par `ordinaire` ou `O_NONBLOCK` (`_empreinte`, `_lire`, `_sommes`, `_synchro`, `status.enregistrements`) ; contrôle `stat` dans `ouvrir` avant `_reprendre`/`_creer` ; O-1 |
| STATUS-QUEUES-1 | **vraie seulement avec C-1, C-2, C-5, C-6, C-10 et R-1, R-2, R-7** | I-3 : une `sante` JSON valide hors FORMAT lève encore (R-1, sonde S1) ; borne exacte de C-6 non figée (M01, R-2) ; « en dernière ligne du rapport » : avec `--depot`, les lignes du quorum suivent (`rapport`, l.275 : `*arretes] + (quorum(...))`) : « du rapport local » (R-7) |
| CHRONYC-FORMAT-1 | vraie avec C-3, C-4, C-7 et R-1, R-3, R-6 | forme relue par moi dans `client.c` 4.6.1 (`process_cmd_tracking`, `%O`, `%L`), extrait de l'archive `571ff73f…` : `client.c` `7e515f33…2d6d`, `util.c` `4a11cb32…`, `chronyc.adoc` `dc955e0f…c5a7` ; aucun `setlocale` ; `chronyc.adoc` l.147-159 = fixture (`07d2a472…934b`) ; R-1 : lecteur qui lève ; R-3, R-6 : ordre des codes et code négatif non figés |
| DNS-ID-16BITS-1 (de fait) | vraie | `requete` : `0 <= ident < 1 << 16`, ValueError nommée ; M15 (65 536 admis) tué |
| ECRIVAIN-REFUS-ARRET-1 | vraie | `_run_params` relu (19 chiffres, GENESE, refus `CONFIG/…` avant `construire`) ; `decoder` : `canonique` avant le rendu ; M08 tué |
| ECRIVAIN-IMBRICATION-OCTETS-1 (de fait) | vraie | `_lire` : `_trop_profonde` avant `json.loads` ; M17 tué par la fitness seule (comportement équivalent) |
| TARDIVES-BORNE-1 (de fait) | vraie | `boucle._lire` : `set_result` dans le `finally`, `release` dans le `finally` intérieur ; aucun `cancel` de futur dans `boucle.py` |
| ASN-HOTE-IPV4-1 | vraie | `_litterale` (forme canonique d'`ipaddress`), `releve` : `a` null, `ip` l'hôte |
| ASN-LECTURE-1 | vraie avec C-9 et R-5 | `_asn` : `[0-9]{1,10}` (ASCII seul en motif texte) ; M09 tué ; M10 vivant (premier champ vide de Cymru non éprouvé : R-5) |
| SECONDAIRE-CONFORMITE-1 | vraie | `test_secondaire.Conformite` présent, vert (suite) ; « tue 9 des 10 mutants » : [2nd] |
| FORMAT-P2B-TESTS-1 | vraie | 23 phrases du §16 et 23 du §17 recomptées dans `test_format` ; bornes égales au code (1 024, 16, 65 536 ; 46 080, 131 072) |
| ENV-ETAPE-1 | vraie | commentaire au job `s2bis-unittest` ; leurres L-10, L-12, L-19, L-33 relus dans le runner (l.642-655) ; purge des mandataires dans `s2bis/tests/__init__.py` l.18-19 (à ba5ea95) |

**Précisions de l'adjudication** :
- SHOGEN-S2BIS-STATUS-RETENTION-1 (annexe B l.1347 lue) : « le compte cumulé tiré des résumés ne passe pas par la
  grille d'`etat` » : vraie sur le code. Aucun chemin n'en fait passer un par `etat` : `quorum` ne lit les résumés des
  autres que pour les jours de la grille locale, `resumes` publie la grille jour par jour ; le compte cumulé reste à
  bâtir sur les résumés publiés (adjudication de DB-0, point 7, [2nd]) : la précision le contraint, rien ne la contredit.
- SHOGEN-S2BIS-RB3-DEGRADATIONS-1 : l.1331 cite « FORMAT §16.2, CB-17a » ; à l'état final, le §16.2 est « Statut d'une
  réponse (RFC 3161 §2.4.2) » (l.726) et le §17.2 « Jugement d'une santé (CB-17a …) » (l.816), D-3 compris depuis DT6-e :
  « §16.2 » se lit bien « §17.2 ».

## 8. Réserves (forme exacte ; à appliquer après DT6-k)

Les diffs `propose/R-1.diff` à `R-6.diff` s'appliquent sur l'état k (`git apply --check` puis `git apply`), seuls ou
ensemble, dans les ordres 1→6, 6→1 et 3, 6, 1, 4, 2, 5 (même arbre final) ; `--check` aussi sur la tête relue à la fin
(§12) avec la série. Aucun ne change le FORMAT ni le nombre de tests (358) ; R-25 : +17, +10, +5, +3, +3, +1 (`.py`).
Section METRIQUES proposée pour l'ensemble (un diff DT6-l, si l'orchestrateur les adopte ensemble) :
`propose/R-metriques.diff` (`358d0396ee93298ec30fe35008782f6598f619457a00f7f3888e5d01d31a03eb`, +28 lignes `.md`,
hors compte de R-25 ; s'applique après R-1 à R-6 comme sur l'état k seul ; à retailler si une partie seulement est
adoptée). Scripts de remplacement exacts qui les ont produits : `propose/r1_tests.py`, `r1_code.py`, `r2_tests.py` à
`r6_tests.py`, `r_metriques.py`. Chaque rouge ci-dessous : test seul, `python3 -B -m unittest`, réseau coupé.

- **R-1 (code ; STATUS-QUEUES-1, I-3 ; CHRONYC-FORMAT-1)**. Constat : `status.chrony` (DT6-e) convertit par `int()` la
  partie entière de System time, Root delay et Root dispersion sans la borner. Sonde S1 (`sondes/s1_chrony_chiffres.py`,
  python3.12, état final) : `sante` JSON valide hors FORMAT, `ws` entier, `d3` au code 0, System time de N chiffres :
  N = 4 300, rapport rendu ; N = 4 301 et 5 000 : `status.rapport` lève `ValueError` (« Exceeds the limit (4300 digits)
  for integer string conversion »). `entree._status` ne rattrape que `RefusStatus`, `ErreurJournal`, `OSError` : trace
  Python, sortie 1, pour `status` et pour `resume` (même `etat`). Sous `PYTHONINTMAXSTRDIGITS=640` (plus petite limite
  non nulle, `journal.CHIFFRES`), une partie entière de 641 chiffres, dans une sortie de moins de 4 096 caractères, lève
  de même. Le collecteur n'écrit jamais une telle ligne (sortie ≤ 4 096 caractères ; `%.9f` d'un double : 309 chiffres
  entiers au plus) : c'est une ligne hors FORMAT, la classe d'I-3 (« jamais une trace ») que C-1 fermait pour `ws`.
  Forme : `propose/R-1.diff` (`6eb57a49fee9b498b4ab2d8655252f0e49d5eec2ac7ed8c95d6195ca2779b531`) : dans `chrony`,
  `if not (o and r and d) or max(len(x[1]) for x in (o, r, d)) > journal.CHIFFRES:` → `None` (relevé illisible), et la
  docstring ; dans `test_ligne_hors_format_jamais_une_trace`, deux `sante` de plus (4 301 chiffres sous la limite par
  défaut ; 641 sous `sys.set_int_max_str_digits(640)`, rendue par `addCleanup`) : disque « non relevé », sans lever.
  FORMAT inchangé : le §17.2 exige déjà « la forme du §13.3 » (`%.9f`), qu'une telle valeur n'a pas. Rouge sur le code
  d'avant : FAIL 1, ERROR 0 (`'ValueError' != "disque : non relevé ({'libre': 13})"`, `sorties/r1-rouge.txt`) ; vert sous
  3.12, et sous 3.10, 3.11, 3.13 en `-X dev -W error`. Mutants : §6.2.
- **R-2 (test ; STATUS-QUEUES-1, C-6)**. Constat : M01 (`readline(LIMITE + 1)`) vit : la ligne de C-6 compte LIMITE + 102
  octets (recompté), la borne exacte n'est pas figée (une ligne de LIMITE + 1 octets, hors FORMAT, serait lue). Forme :
  `propose/R-2.diff` (`ec0fbdb6e59bbf97fa1955e1d50c44cb769eb8a2bd48187a7bc6c720a0aff808`) : la ligne de
  `pool-2026-10-05-7.jsonl` fait exactement LIMITE + 1 octets (coupée) ; puis, réécrite à exactement LIMITE octets, elle
  est lue par `status.enregistrements`, sans arrêt. Rouge : FAIL 1 sur `readline(LIMITE + 1)`, sur `readline(LIMITE - 1)`
  et sur `readline()` ; vert sur le code.
- **R-3 (test ; CHRONYC-FORMAT-1)**. Constat : M03 (codes non triés quand D-3 s'ajoute) vit : aucune fenêtre ne porte
  D-3 avec D-4 ou D-5 ; un résumé ainsi publié serait refusé par `lire_resume` des autres (`RESUME/champs`). Forme :
  `propose/R-3.diff` (`03123c167e9a35b2f04032fa5326dda5149cd71ef6a5b15ef5da9ebd83bea7db`) : dans
  `test_d3_jugee_sur_la_sortie_gelee`, une fenêtre 22 (`sante(d3=None, d4=[temoin("delai")] * 3)`), attendue
  `["D-3", "D-4"]`. Rouge : FAIL 1 sur M03 ; vert sur le code.
- **R-4 (test ; CANONIQUE-OCTETS-1)**. Constat : M07 (`_octets(0)` = 0) vit ; la boucle « une valeur simple en écrit au
  plus 8 fois sa borne » n'a pas l'entier 0. Forme : `propose/R-4.diff`
  (`94fdf8aedf9855a099260380a8e346834a846310d3d6270a657b8d676b031db4`) : `0` ajouté à cette boucle, docstring. Rouge :
  FAIL 1 sur M07 (`(0, 0, 1)`) ; vert.
- **R-5 (test ; ASN-LECTURE-1)**. Constat : M10 (Cymru : `except ValueError` seul) vit : aucun TXT au premier champ
  vide ; `releve`, documenté « ne lève jamais », lèverait `IndexError`. Forme : `propose/R-5.diff`
  (`4c0238a4dd72cf9228688b480d79856cfc6a83d7164138ff56781ebfb599f719`) : premiers champs `""` et `" "` (None), puis
  `(" | x", "64501 | y")` (64501 : la réponse suivante est lue). Rouge : ERROR 1 (`IndexError`) sur M10 — le mutant lève,
  aucun échec d'assertion n'est possible sans rattraper l'exception ; vert.
- **R-6 (test ; CHRONYC-FORMAT-1)**. Constat : M12 (`code > 0` refusé seul : une commande tuée par un signal, code
  négatif, lue comme lisible) vit. Forme : `propose/R-6.diff`
  (`9005b69debdc80dbd4a0ea2d7c4a62e64cdbd87570d8f95ecba2c5d18f9b22bf`) : la neuvième variante `{**D3, "code": 1}` devient
  `{**D3, "code": -9}` (commentée) ; le code 1 reste figé par la première variante (mutant « code 1 admis » : FAIL).
  Rouge : FAIL 1 sur M12 ; vert.
- **R-7 (texte de la phrase de fermeture de STATUS-QUEUES-1, à verser à l'annexe B)**. Remplacer « chaque fichier
  arrêté avant sa fin nommé avec son motif en dernière ligne du rapport » par « chaque fichier arrêté avant sa fin
  nommé avec son motif en dernière ligne du rapport local (le compte à quorum suit, avec `--depot` : FORMAT §17.6) »,
  et citer, avec O-1 de la G2 (C-1, C-2, C-5, C-6, C-10), R-1 et R-2 si l'orchestrateur les adopte ; de même R-1, R-3,
  R-6 pour CHRONYC-FORMAT-1, R-4 pour CANONIQUE-OCTETS-1, R-5 pour ASN-LECTURE-1.

## 9. Observations (sans correction)

- **O-1** C-8 éprouve `_synchro` avec l'espion de fsync. Avec `os.fsync` réel, un tube posé au nom de la veille après le
  contrôle par `stat` fait lever `fsync` (EINVAL sur un tube, Linux [inféré de la page fsync(2), non mesuré]) : refus par
  `OSError` (casse) plutôt que `JOURNAL/fichier`, toujours sans attente. Le FORMAT §7.7 ne promet que la lecture sans
  attente : rien à corriger ; course de temps entre `stat` et `_synchro`, hors usage.
- **O-2** M17 n'est tué que par `test_fitness` (copie textuelle du compte du recalcul) : la borne de `_trop_profonde` à
  un niveau près ne change aucun verdict, `canonique` recomptant les niveaux (refus `JOURNAL/imbrication`).
- **O-3** Si R-1 est adopté, la règle de validité du recalcul (RB-3, SHOGEN-S2BIS-RB3-DEGRADATIONS-1 et sa précision
  D-3) doit lire D-3 avec la même borne (import de `status.chrony`, ou test croisé) : déjà dans le texte de l'item
  (« import des définitions de `status`, ou test croisé »), rien à ajouter.
- **O-4** `client.c` passe à `%.9f` des valeurs converties par `UTI_FloatNetworkToHost` (`util.c` l.966-983, lu :
  coefficient de 25 bits, exposant de 7 bits, `coef * pow(2.0, exp)` avec exp ≤ 63 − 25) : |valeur| < 2^62, soit
  19 chiffres entiers au plus ; la borne de R-1 (640) ne retire rien à une sortie réelle.

## 10. Écarts du contre-contrôleur (déclarés)

- **E-1** Pour situer l'annexe D, une liste non récursive des noms de `docs/adr-0028/` à `ba5ea95` filtrée par
  « annexe » (`git ls-tree --name-only … | grep -i annexe`) : cinq noms d'annexes, aucun nom ni contenu interdit ; puis
  lecture de l'annexe D l.28-50 (admise : « Ne sont pas interdits : ADR-0028 et ses annexes ») : la l.28 affichée est la
  ligne 16 de D.1 (journal d'exposition), sans valeur masquée. Écart à la lettre « aucune liste par motif sur docs/ ».
- **E-2** Un `grep -c` non récursif à glob `s2bis/tests/*.py` sur ma copie (comptes et noms de modules seuls), pour
  savoir si la suite s2bis appelle git : aucun dossier `docs/`, aucun contenu interdit.
- **E-3** `ls` non récursif de `travail/` et `tmp/` du lot (dossiers nommés), pour retrouver l'archive de chrony
  téléchargée par le générateur ; archive ouverte par `tar -x` de trois fichiers nommés dans un dossier neuf, aucune
  exécution de son contenu.
- **E-4** `python3` des suites = python3.12 (lien en tête du PATH, comme l'image) ; l'étape workflows-yaml appelle
  `/usr/bin/python3`, ici 3.11.15 (image : 3.12.3) ; mes outils tournent sous `python3` 3.11.15.
- **E-5** Le rouge de R-5 est une erreur (`IndexError`), non un échec d'assertion (§8).
- **E-6** `SHA256SUMS` écrit par un `find -type f` borné à mon seul dossier `g2/cc/` (mes fichiers rendus), non au
  scratchpad.

## 11. Journal de provenance (G1 du contre-contrôleur)

Sources (niveau ; sha256) :
- [lu] `BRIEF-CC.md` `bc5d30e0…186a` ; `ADJUDICATION.md` `90088431…322c` (trois sections) ; `g2/RAPPORT-G2.md`
  `6c2f62dc…97da` (entier) ; `g2/corrections/G2-corrections.diff` `2b6d931a…94ab` (entier) ; `RAPPORT-GENERATEUR.md`
  `a717d31b…d80c` (§1 à §10) ; `BRIEF-DETTES-T6.md` `48edfb43…17fd` ; `ITEMS-ANNEXE-B.md` `712b2c52…4d79` ; `NOTES.md` du
  lot `82685823…` (l.18, l.108-166, grep ciblé) ; `s2bis/dettes4/NOTES.md` `21cac76f…a070` (l.1-40 : méthode de copie).
- [lu] diffs : DT6-c, DT6-d, DT6-j, DT6-k entiers ; DT6-b, DT6-f, DT6-h (lignes changées) ; DT6-e (FORMAT, METRIQUES,
  liste des hunks) ; DT6-i (lignes ajoutées) ; DT6-a et DT6-g par le code et les tests finals et leurs sections de
  METRIQUES ; `--numstat` de tous.
- [lu] copie à `ba5ea95` + série : `status.py` entier (`29678a0f…6584`), `journal.py` entier, `asn.py` entier,
  `sante.py` l.1-60, `decodeurs.py` l.30-80 et `decoder`, `dns.py` (contrôle de l'identifiant), `boucle._lire`,
  `entree.py` (`_status`, `_run_params`), tests touchés par les corrections et par mes réserves, `test_tetes.sans_attente`,
  `verdict-suite-s2.py` (`lancer`, `main`), `gates.yml` (jobs lus) `3c168b76…a434`, runner (L-10, L-12, L-19, L-33),
  `s2bis/tests/__init__.py` (purge des mandataires), FORMAT `799c8291…f5a6` (§17 l.797-815, §16.2 l.726, §17.2 l.816,
  hunks de la série), METRIQUES `49281cab…89aa` (en-tête, sections DT6), annexe B `a8d727c3…650e` (l.1331, l.1347 :
  grep ciblé du seul fichier), annexe D à `ba5ea95` `deb64179…0eaf` (l.28-50), `CP2-S2.md` `eb00a2e3…83a0` (l.13-17),
  `.cargo/config.toml`, `rust-toolchain.toml` (1.97.1).
- [lu] chrony 4.6.1, extrait par moi de l'archive téléchargée par le générateur (`571ff73f…9c5c`, recalculé ; 4.9
  `4924c6f5…64d0` et signature `df077dae…671d` : sha256 recalculés seulement) : `client.c` `7e515f33…2d6d`
  (l.1740-1778, 2173-2222), `util.c` `4a11cb32…` (l.958-983), `doc/chronyc.adoc` `dc955e0f…c5a7` (l.147-159 =
  fixture). Authenticité de l'archive : non vérifiable hors réseau (L-5 du générateur, partagée).
- [2nd, non refait] comptes des campagnes du générateur et du réviseur ; heure d'écriture du FORMAT (01:18:37) ;
  mesure de C-10 (sonde P5b du réviseur) ; adjudication de DB-0 (points 7, 8).

Commandes et sorties (réseau coupé ; `sorties/`) : `etats.sh` (`etats.log`, `etats/`) ; `final.sh` (`final.log`,
`final/`) ; `campagne.py` (`mutants-cc.{log,json}`) ; `rouges.py` (`rouges-C5-C9.json`) ; rouge C-1/C-2
(`rouge-k-code.txt`) ; sondes S1, S2 ; R-1 (`r1-rouge.txt`, `r1-vert.txt`) ; `reserves.sh` (`reserves.log`,
`reserves/`) ; `cargo.sh` (`cargo/`) ; `tables.py`, `lignes.py`. Chiffres recomptés par moi : empreinte de la série,
13 sommes, R-25, planchers et « Suite », 29 lignes de tableaux, 46 phrases de `test_format`, sites de `_entier`, hashes
de chrony.

## 12. Tête relue, fichiers rendus

**Tête relue à la fin** (03:39:33 UTC) : `57330facc659acfb9bc1bfc337e0456188e2c129` (« FUZZ versement : pièces de revue »).
La série DT6-a à DT6-k s'y applique (`git apply --check` puis `git apply` à chaque pas, sur un `git archive` des
fichiers de la série, `*.jsonl` exclus) ; le résultat est égal à l'état final relu ici (`status.py` `29678a0f…`, FORMAT
`799c8291…`, METRIQUES `49281cab…`) ; R-1 à R-6 et `R-metriques.diff` : `--check` OK sur cette tête + la série. Entre
`ba5ea95` et cette tête, aucun changement sous `s2bis/`, `docs/adr-0029/s2bis/`, `gates.yml`, `enforcement/`,
`s2-harness/tests`, `scripts/controle` (`git diff --stat` vide). Têtes vues pendant le travail : `1eb10cc` (02:55),
`3aa0275` (03:25), `3a3da93` (03:26), `3a97142` (03:38), `57330fa` (03:39), toutes du lot FUZZ.

Rendu le 2026-10-10, heure en tête de `NOTES.md` (dernière ligne). Dans `<scratchpad>/s2bis/dettes6/g2/cc/` :
`RAPPORT-CC.md` (ce rapport), `NOTES.md`, `propose/` (R-1 à R-6, `R-metriques.diff`, scripts de remplacement),
`mutants/` (`cc.py`, `r1.py`, `reserves.py`), `outils/` (`iso.sh`, `job.py`, `jobs.py`, `etats.sh`, `final.sh`,
`campagne.py`, `rouges.py`, `reserves.sh`, `cargo.sh`, `tables.py`, `lignes.py` ; `py3/python3`, lien vers
`/usr/bin/python3.12`, hors sommes), `sondes/` (S1, S2), `sorties/` ; `SHA256SUMS` écrit en dernier (tous les fichiers
du dossier hors lui-même et le lien). Copies, cible cargo et temporaires supprimés (`tmp/`). Aucun commit, aucun push,
aucune écriture dans le dépôt.

## Ajout daté du 2026-10-10 05:40:14 UTC (`date -u`) : passe 2 (DT6-s, DT6-t, DT6-u ; série a à u sur dda4bbc)

**Verdict final : CONFORME-AVEC-RÉSERVES (R-8).** R-1 à R-7 sont levées : adoptées et versées en DT6-l à DT6-r
(identité à l'octet refaite par `cmp`, 7 sur 7). DT6-s, DT6-t et DT6-u sont justes. Reste une réserve neuve, R-8 (test
seul, deux lignes), née de mon contrôle de DT6-u.

Pièces lues : message du coordinateur ; `ADJUDICATION.md` `a4f36a20…8fa70` (ajouts de 03:52:42, 04:28:30 et 05:11:14) ;
`RAPPORT-GENERATEUR.md` §12 (05:10:00) ; `outils/charge.py` `c245f955…`, `repete_test.py` `466a6245…` ; résumés des
`sorties/p4-*.json` nommées au §12 (avant 2/10 000, après 0/10 000, rouge 200/200, vert 0/200, module 0/200 et 0/200 :
conformes au §12) ; FORMAT §13.2 l.532-536 [lu]. `SHA256SUMS` du lot : 23 OK. Empreinte a à u recalculée :
`341f8a3cafb39243233aa0de754a6ee35854120f2e8af2bcf41bef6da226d9d1`, égale au message. DT6-s `a5057683…`, DT6-t
`250e78ad…` et DT6-u `f73b8ebd…` sont égaux au message. Tête : `dda4bbcc2b0f480eb0c39d7891237e0e3d2b0918`, lue à 05:11:12
et à 05:38:53. À 05:40:44, la tête est passée à `4b4810816c2493bcd4d58f42c824de335e2c03ad` (DETTES-T14 DT14-a,
`biblio/INDEX.md`). Depuis `dda4bbc`, aucun chemin de la série n'a changé ; a à u, puis R-8 et `R-8-metriques.diff`, y
passent `--check`. Copie : clone creux à `dda4bbc` (58 entrées sautées, 0 `.jsonl`) ; DT6-a à DT6-u appliqués,
`git apply --check` à chaque pas.

**1. DT6-u est juste.**
- **Cause dans le test, non dans le code.** Dans l'état t, l'`attendre` injecté du test n'attendait que les deux
  témoins (`futurs[2:]`). Il avançait ensuite l'horloge factice à E puis à E + 1 ms. Or le FORMAT §13.2 et la boucle
  de production attendent les sondes « avec les lectures, jusqu'à l'échéance » : `Boucle.attendre` par défaut attend
  tous les futurs, d3 compris (`jusqu_a`, `boucle.py` l.52-58 et 76-77). Quand le fil de d3 était retardé,
  `Sondes.joindre` appliquait sa règle exacte : sonde inachevée, null ; `fin` > E, null.
- **Avant, sous 3 processus de charge** (boucle Python vide, groupes tués à la fin, charge relevée toutes les 2 s ;
  état t, `outils/repete_cc.py` sous `outils/sous_charge.py`) : 20 000 passages, **130 ERROR**. Toutes sont
  `TypeError: 'NoneType' object is not subscriptable` à `enr["d3"]["code"]`, le symptôme du constat. Le relevé, observé
  en enveloppant `joindre` sans rien changer, se répartit ainsi :
  - 118 fois, d3 n'est pas finie au relevé ;
  - 12 fois, d3 est finie à E + 1 ms, au-delà de la limite ;
  - les témoins sont toujours à E et à E + 1 ms.
  Charge sur 1 min : moyenne 5,37 (de 1,57 à 6,98).
- **Après** (état u, mêmes conditions) : 10 000 passages, **0 échec**, charge plus haute (moyenne 7,11, de 6,18 à 8,04).
  Le module `test_sante`, lancé en 50 interpréteurs sous charge : 50 OK (moyenne 8,14, de 7,54 à 9,32).
- **Sans charge, mécanisme isolé :**
  - état t avec d3 retardée de 20 ms : 50/50 ERROR, avec le même relevé ;
  - état u avec d3 retardée de 20 ms, 0,5 s et 2 s : respectivement 50/50, 10/10 et 3/3 OK.
- **Ce que le test vérifiait est gardé.** Les assertions sont inchangées ; il n'y a aucun saut ; seule borne ajoutée :
  5 s, celle de ses autres attentes. Mes mutants de la règle, joués par la commande du job sur l'état u, sont tous tués
  par le test corrigé :
  - V1 (`fin >= limite`) ;
  - V2 (1 ms de grâce) ;
  - V3 (limite prise au relevé et non à E).
- **Aucun défaut du collecteur n'est masqué.** La seule différence est l'attente de la lecture et de d3 avant E, que la
  production fait déjà. La pause de 20 ms rend le rouge certain sans cette attente.
- **Constat.** V4 (d3 exemptée de la règle `fin` > E) vit avant comme après DT6-u : aucun test n'applique la règle à
  d3, que le FORMAT §13.2 nomme pourtant (D-3, D-4, D-5). Ce n'est pas une régression de DT6-u : voir R-8.

**2. DT6-t et DT6-s.**
- DT6-t : R1-M4 (639) et R1-M3 (641) sont tués par `test_ligne_hors_format_jamais_une_trace`, par la commande du job
  sur l'état u. Avec le test seul :
  - à l'état s (sans DT6-t) : R1-M4 OK, donc vivant ;
  - à l'état t : FAIL, « unexpectedly None ».
- DT6-s est exact : la section décrit R-1 à R-6, c'est-à-dire DT6-l à DT6-q, et DT6-r l'apporte.
- Tableaux recomptés : `test_status.py` 559 lignes et 24 tests ; `test_sante.py` 288 lignes et 14 tests.
- R-25 recompté : s +0, t +4, u +5 (`numstat`). Lignes ajoutées de s, t et u : aucune de plus de 120 caractères, aucun
  `TODO` ou `FIXME`, aucun octet 92, aucun blanc final.

**3. Série a à u sur `dda4bbc`** (réseau coupé, `python3` = 3.12.3) :
- runner : `verdict-suite-s2 : 137 ok, 0 échec` ;
- ligne exacte du job s2bis : `verdict-suite-s2 : conforme (code 0, résumé final, aucun saut, Ran = 358)` ;
- matrice 3.10.20, 3.11.15, 3.12.3, 3.13.14 en `-X dev -W error` : conforme, Ran = 358, 0 « Exception ignored »,
  0 « warning », sortie 0, pour chacune.

**R-8 (test seul ; SHOGEN-S2BIS-TEST-SANTE-CHARGE-1 et règle `fin` > E de SONDES-ECHEANCE-1).**
- Forme : `propose/R-8.diff` (`e0a8facb96ac7fae2bf12a105eadd0d7e7b0084d99f8a013323d7519173c4e7e`, +2). Dans
  `test_sondes_en_parallele_arguments_et_ordre`, `joindre(lancees, 0)`, avec une limite antérieure à toute fin, doit
  nuller chaque sonde : d3, les trois témoins et les deux noms.
- Rouge : FAIL 1 sur V4 ; vert sur le code ; module `test_sante` vert sous 3.10 à 3.13 en `-X dev -W error`.
- Sur `dda4bbc` + a à u + R-8, commande du job : témoin VIVANT (Ran = 358, plancher inchangé), V4 TUÉ.
- Section METRIQUES proposée : `propose/R-8-metriques.diff` (`6389788b…b0`, +18 `.md`, « DT6-v »).
- Les deux diffs s'appliquent après DT6-u (`--check`).

**Écarts de la passe 2.**
- E-7 : `ls` non récursif de `dettes6/` et de `dettes6/diffs/`.
- E-8 : machine partagée. Les trois mesures sous charge (11 min en tout) se sont faites l'une après l'autre, sans autre
  calcul lourd de ma part ; la charge relevée a atteint 9,32 avec les travaux d'autres agents. Les processus de charge
  ont été tués ; contrôle par `ps` : 0 restant.
- E-9 : le taux d'échec avant (0,65 %) dépasse celui du générateur (0,02 %), sur une charge plus forte et un passage
  plus court. Les deux mesures concordent sur le sens : échecs avant, aucun après.

Sorties : `sorties/p2/` (mesures, relevés de charge, contrôles sans charge, job, matrice, campagnes `mutants-p2.json` et
`mutants-r8.json`). Outils : `outils/repete_cc.py`, `sous_charge.py`, `mesures_p2.sh`, `p2_suite.sh`. Mutants :
`mutants/p2.py`, `mutants/r8.py`. Le dossier `tmp/` (copies) est supprimé. Aucun commit, aucun push, aucun réseau.
