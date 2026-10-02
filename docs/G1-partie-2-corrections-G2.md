# Journal de correction — relecture G2 de la partie 2 (C-1 à C-11)

**Nature** : journal G1 du correcteur de la relecture G2 de la partie 2 de S2. Liste fermée C-1 à C-11 de
`docs/G2-partie-2.md` §10 appliquée telle quelle, C-10 exceptée (ajout daté de l'annexe D, écrit par l'orchestrateur,
brief). Aucun commit : six diffs, un par sous-lot, et ce journal, rendus à l'orchestrateur (R-19, R-20).

## 0. Gate 0 et cadre

- **Modèle résolu sous lequel le correcteur a tourné : `claude-opus-5-5`** (identifiant exact fourni par l'environnement
  de la session ; préfixe attendu `claude-opus-5-5` : conforme). Effort : `max` (brief).
- Horloge (`date -u`) : 11:34:56 UTC au départ, 2026-10-02 ; clôture au §9.4.
- Dépôt : branche `partie-2-rendu`, tête `54e38ac892aa59fcf1183852f0fcdf6dd5f2d454`, `git status --short` vide au
  départ. Le commit `54e38ac` ne touche que `JOURNAL.md`, `docs/G2-partie-2.md`, l'annexe B et le G0 (`git diff --stat
  6eabaa4 54e38ac`) : le code est celui de `6eabaa4`, les lignes citées au §10 du G2 valent. L'orchestrateur a commis
  C-10 neuf secondes après le départ (`e83b88a`, 11:35:05 UTC, annexe D seule) : `s2-harness/` est identique entre les
  deux commits (`git diff --quiet 54e38ac e83b88a -- s2-harness`), les diffs, calculés contre `54e38ac`, s'appliquent
  à l'identique sur `e83b88a` (§4, clone jetable). Aucune opération git en écriture sur le dépôt ; fichiers modifiés :
  les huit fichiers de `s2-harness/` du §2 ; fichier créé : ce journal.
- Rattachement (G0) : brief de l'orchestrateur ; contrat `docs/G2-partie-2.md` §10 (sha256 `0b45a458…`) ; décisions
  Q-1 à Q-4 du bloc B.28 (`docs/adr-0028/ANNEXE-B-items.md`, sha256 `f94d333a…`) : Q-1 jeton par variable
  d'environnement (C-1), Q-2 bornes basse et haute de la date du go (C-3), Q-3 étiquette du J28 complétée par le script,
  épingles inchangées (C-7), Q-4 hors code ; `docs/adr-0028/G0-partie-2.md`, section « G2 — corrections de la
  relecture » (sha256 `f47b6541…`).
- Pré-enregistrement : aucune pièce de D.2 ouverte ni prise dans une recherche (ADR-0025 et la cartographie du
  2026-09-29 jamais lues ; recherches limitées à `s2-harness/`, `xtask/src/`, `enforcement/` et aux sondes du réviseur,
  jamais à `arbres/tete-complet` de son scratchpad) ; `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée (`env | grep -c` : 0 au
  départ et à la clôture ; toute commande Python sous `env -u SHOGEN_S2_CAMPAGNE_CONTROL`) ; fixtures seulement
  (D.4 a) : dépôts git jetables, collecteur réel sur horloge factice, autorité RFC 3161 de test, aucun journal de
  campagne ; `JOURNAL.md`, les annexes, `docs/G2-partie-2.md`, `docs/pocket-report/` et `scripts/sceau/` non touchés.
- Espace de travail hors dépôt : `<S>/lot-G2corr/`, où `<S>` est le scratchpad de la session
  (`/tmp/claude-0/-home-user-shogen/7ba84933-ba6d-5813-9ef4-ca3ac4febd16/scratchpad`) ; `TMPDIR` posé sur
  `<S>/lot-G2corr/tmp`.

## 1. Méthode

1. Par correction : test écrit d'abord et lancé sur l'arbre non corrigé (échec consigné dans `preuves/<C-x>-avant.out`),
   correction, test vert (`preuves/<C-x>-apres.out`), puis mutants du correcteur : `outils/moteur.py` copie les fichiers
   suivis de `s2-harness/` et `enforcement/` (arbre de travail, ou un instantané du dépôt jetable), applique une mutation
   dont l'ancre figure une fois exactement, lance les tests nommés, témoin sans mutation d'abord.
2. Après chaque sous-lot : suite entière (`python -B -m unittest discover -s tests -t .`), puis instantané dans un dépôt
   git jetable du scratchpad (`outils/instantane.sh`) : diff contre l'instantané précédent (base `54e38ac`) et numstat.
3. Oracles imposés : règle scellée (`<S>/regle_fixtures.py`, sha256 `5557fb56…`) et épingles (`<S>/render_fixture.py`,
   sha256 `4084c42b…`) sur la base, après C-8 (seul sous-lot qui touche `shogen_s2/`) et sur l'arbre final ;
   `cargo --locked xtask verify` avant et après ce journal.
4. Clôture : tous les mutants rejoués sur l'arbre final ; suite rejouée sur l'export de chaque instantané ; hook
   pre-commit versionné lancé dans un clone jetable où le diff total et ce journal sont indexés.

## 2. Sous-lots (coupe du brief, chacun ≤ 200 lignes de code et tests)

| sous-lot | corrections | numstat par fichier | total | suite après | sha256 du diff |
|---|---|---|---|---|---|
| G2a | C-1, C-6 | `test_oracle_record.py` +14 −5 ; `test_rendu_production.py` +26 −3 ; `oracle_record.py` +4 −1 ; `rendu_unique.py` +10 −1 | +54 −10 = 64 | 370, OK (2 sauts) | `dc9a88852bdbba9038d46ae2c9f6aef7c7c2c1e90ca583c1903e7bf636a15f9e` |
| G2b | C-2 | `test_rendu_production.py` +54 −8 ; `test_rendu_unique.py` +31 −7 ; `rendu_unique.py` +27 −9 | +112 −24 = 136 | 373, OK (2 sauts) | `f67d20c3f9c1ee2963574714ea12fd3711e4dc76fcef2c51e1607a8ec461fad4` |
| G2c | C-3 | `test_rendu_production.py` +4 −2 ; `test_rendu_unique.py` +44 −16 ; `rendu_unique.py` +21 −5 | +69 −23 = 92 | 373, OK (2 sauts) | `8f86378ce97b1b0bb903888dbe5d000e8998b2d52c5d065a00d162c1fde0ef83` |
| G2d | C-4, C-5 | `test_rendu_production.py` +27 −1 ; `test_rendu_unique.py` +14 −0 ; `rendu_unique.py` +36 −18 | +77 −19 = 96 | 375, OK (2 sauts) | `deec7d7704c8f23d350b5f2da549c79a5d42d0086457493a680958beba86ca64` |
| G2e | C-7, C-8, C-9 | `records.py` +8 −2 ; `test_lecteur.py` +17 −0 ; `test_rendu_production.py` +15 −6 ; `rendu_unique.py` +7 −4 | +47 −12 = 59 | 376, OK (2 sauts) | `a7e09982353b5737c9a61b37f6d58bc71716466eef68183b7775cb1465c3dc2e` |
| G2f | C-11 | `test_oracle_record.py` +5 −4 ; `test_rendu_production.py` +15 −10 ; `test_rendu_unique.py` +13 −7 ; `test_sensibilite.py` +9 −3 | +42 −24 = 66 | 376, OK (2 sauts) | `2d1d8a4d25f48f4f63544e5a9a8dbdc72bdb087ab5cbc8c1cc48d00b0247300b` |

Diffs : `<S>/lot-G2corr/G2a.diff` à `G2f.diff`, chacun contre l'instantané précédent, à appliquer dans l'ordre. Diff
total `54e38ac` → arbre final (`git diff`, lecture seule) : 8 fichiers, +396 −107, `total-54e38ac-final.diff`, sha256
`ba2934b43da90bb48d4ec2123a0c0db537b37c8046ab7a1118d47ff78b4fcafc` ; il égale à l'octet le diff cumulé des six
instantanés (`cmp`). Départ de la suite : 369 tests (base rejouée, §4).

## 3. Par correction

### C-1 — `--produire` réservé à l'exécution unique (G2a)

- Provenance [lu] : G2 §3.2 pt 1 et §10 C-1 ; sonde `sonde_produire.py` du réviseur et sa sortie
  (`preuves/sonde_produire.out`, `6dfb424f…`) ; décision Q-1 (B.28).
- Construction appliquée : `rendu_unique.py` : constante `JETON` = `SHOGEN_RENDU_PRODUCTION` ; `produire` refuse avant
  toute autre chose (code 2, sortie standard vide, motif sur stderr : commande nommée réservée à l'exécution unique) si
  la variable est absente ou ne désigne pas un répertoire existant dont le nom commence par un point ; `produire_tout`
  pose la variable sur le temporaire voisin (chemin absolu, nom `.<sortie>.xxxx`) avant `orc.enregistrer` et la retire
  dans `finally`.
- Tests : `test_produire_reserve_a_l_execution_unique` (neuf, `test_rendu_production.py`) : `--produire j14-principal`,
  `recalcul-tiers` et `raw` en sous-processus ; variable absente, vide, sur un répertoire sans point, sur un chemin
  absent, sur un fichier : code 2, sortie vide, motif ; sur un répertoire à point : code 0. Adaptations : le helper
  `produire` des tests pose la variable par `mock.patch.dict(os.environ, …)` ; le sous-processus de
  `test_raw_verdict_et_exit_0` la reçoit par `env` ; `test_nominal_bout_en_bout` inchangé (la variable lui vient de
  `produire_tout`).
- Échec avant : `preuves/C-1-C-6-avant.out` : 15 sous-tests rouges (code 0 et sortie non vide au lieu du refus).
  Après : `preuves/C-1-C-6-apres.out`, OK.
- Mutants : C1-a (contrôle retiré) tué, 15 échecs ; C1-b (nom à point non exigé) tué, 3 échecs ; C1-c (variable non
  posée par `produire_tout`) tué par `test_nominal_bout_en_bout` (run `j14-principal` en échec, code 2).

### C-6 — `--verifier` du rôle rendu : runs exigés (G2a)

- Provenance [lu] : G2 §3.2 pt 7 et §10 C-6 ; sonde `sonde_verifier_runs.py` (`preuves/sonde_verifier_runs.out`,
  `f3b6cf6e…`).
- Construction appliquée : `oracle_record.verifier`, au rôle `rendu`, après le contrôle de `paquet.sha256` : liste des
  noms des runs égale à `suite` puis `PRODUCTION`, dans l'ordre, sinon refus nommé `runs` ; docstring complétée.
- Tests : `test_verifier_un_refus_nomme_par_controle` : l'enregistrement de rôle rendu conforme devient une copie de
  celui de l'enregistreur dont `runs` est réécrit en six runs (noms écrits à la main, sorties écrites par le test) ;
  refus `runs` sur l'enregistrement à un seul run et sur la copie à six runs en ordre inverse.
- Échec avant : 2 sous-tests rouges (ValueError non levée). Après : OK.
- Mutants : C6-a (contrôle retiré) tué, 2 échecs ; C6-b (comparaison sans ordre) tué, 1 échec.
- Suite après G2a : 370 tests, OK (2 sauts) (`preuves/suite-G2a.out`).

### C-2 — script, enregistreur et HEAD liés au commit gardé (G2b)

- Provenance [lu] : G2 §3.2 pts 2 et 3 et §10 C-2 ; sondes `sonde_hors_depot.py` (`preuves/sonde_hors_depot.out`,
  `956abfe1…`) et `sonde_head.py` (`preuves/sonde_head.out`, `6b82cf33…`).
- Construction appliquée : (i) `head(c)` : HEAD résolu une fois par évaluation (`git rev-parse --verify HEAD^{commit}`,
  sha complet gardé dans le contexte sous la clé `head`, ValueError si illisible), lu par g1 (`show <head>:JOURNAL.md`),
  g2 (`diff … <commit_analyse> <head>`), g4, la voie (b) (`log … <head>`), `orc.enregistrer` et `orc.verifier` dans
  `produire_tout` ; (ii) g4 exige aussi que le sha256 de `git cat-file blob <head>:s2-harness/tools/rendu_unique.py`
  égale `sha256_script`, et que le sha256 du fichier chargé comme `orc` (`orc.__file__`) égale celui de
  `<head>:s2-harness/tools/oracle_record.py` ; docstrings et motif de g2 alignés sur le commit résolu.
- Tests : `test_garde_4_sha_du_script` étendu (outil ou enregistreur du commit gardé autres que ceux qui tournent, (2)
  levée par les mêmes octets à c1 : refus (4)) ; `test_script_hors_depot_enregistreur_voisin_modifie` (la sonde : copie
  du dépôt lancée hors du dépôt, `oracle_record.py` voisin modifié, run suite retiré : refus (4) seul, code 2, rien
  d'écrit) ; `test_head_lu_une_fois_production_sur_le_commit_garde` (la sonde : gardes levées sur X, commit Y qui retire
  le sha du paquet et change le code d'analyse, production : code 0, `tree.commit` = X) ;
  `test_gardes_lisent_le_head_resolu_une_fois` (ajouté, §5 pt 1). Adaptations : `monter` commite à c1 les octets de
  `tools/rendu_unique.py` et `tools/oracle_record.py` du harnais (paramètre `code` : fichiers de c1 remplacés) ;
  `monter_prod` charge le module depuis la copie du dépôt (`sha256_script` = sha256 de cette copie), commite le lint
  d'épinglage à c1 et charge le module sans écrire de cache ; `lancer` prend ce module quand il est posé.
- Échec avant : `preuves/C-2-avant.out` : 4 échecs (deux sous-tests de (4) ; hors dépôt : gardes levées, production
  lancée, code 1 ; HEAD : `tree.commit` = Y) ; `preuves/C-2-head-resolu-avant.out` (test ajouté, lancé sur
  l'instantané G2a) : refus (1), (2), (5), (6) au lieu de gardes levées. Après : `preuves/C-2-apres.out`,
  `preuves/C-2-head-resolu-apres.out`, OK.
- Mutants : C2-a ((ii) retiré) tué ; C2-b et C2-c (chaque moitié de (ii)) tués ; C2-d (HEAD rétabli dans
  `orc.enregistrer`) et C2-e (HEAD rétabli dans la relecture) tués ; C2-f à C2-i ((1), (2), (4), voie (b) relisent
  HEAD) tués par le test ajouté ; C2-i rejoué après C-3, ancre déplacée dans `premier` : tué
  (`preuves/mutants-G2c-head.out`).
- Suite après G2b : 373 tests, OK (2 sauts).

### C-3 — voie (b) : ordre des commits et date du go, SHOGEN-GO-ORDRE-1 (G2c)

- Provenance [lu] : G2 §3.2 pt 4, §4 (R01, R02) et §10 C-3 ; sonde `sonde_go.py` (`preuves/sonde_go.out`,
  `e9d86195…`) ; décision Q-2 (bornes basse et haute retenues).
- Construction appliquée : `premier(c, sha)` : premier commit de `git log --no-textconv --reverse --format=%H %ct
  -S<sha> <head> -- JOURNAL.md` (sha du commit et date de commit ; aucun : ValueError) ; S pour le sha du paquet, Gc
  pour celui du go ; `voie_b` refuse si Gc = S, si S n'est pas ancêtre de Gc (`git merge-base --is-ancestor S Gc`), si
  ct(Gc) ≤ ct(S), ou si la date du go n'est pas dans [ct(S) ; ct(Gc)] ; T0 = ct(Gc), inchangé ; `GO` inchangé ; le
  contrôle des lignes (première occurrence du go après la ligne du scellement) est gardé.
- Fixtures : constante `SCELLEMENT` = 2026-08-31T00:00:00+00:00, date de commit du scellement dans `monter` et
  `monter_prod` (helper `dater`, paramètre `date` de `poser`) ; `GO_OK` daté du 2026-08-31T12:00:00Z, entre le
  scellement et l'épinglage par défaut d'`epingler` (2026-09-01T00:00:00Z).
- Tests (`test_voie_b_refus`), refus (5) et (6), rien d'écrit : listés au §10 : même commit (go daté de l'heure du
  scellement) ; go daté une seconde après son commit d'épinglage ; go daté une seconde avant le commit du scellement ;
  commit d'épinglage daté avant le scellement ; go cité avant le scellement puis après (R01) ; date à +01:00, même
  instant UTC que `GO_OK` (R02) ; ajoutés (§5 pt 4) : épinglage au même instant que le scellement ; go épinglé sur une
  branche partie de c1, puis fusionnée (hors de la descendance du scellement). Les variantes existantes « date hors ISO »
  et « hors calendrier » sont réécrites sur la nouvelle date du go (mêmes contrôles).
- Échec avant : `preuves/C-3-avant.out` : 6 sous-tests rouges (les six variantes d'ordre et de date : gardes levées) ;
  les variantes R01 et R02 sont déjà refusées par le code et servent à tuer ces deux mutants. Après :
  `preuves/C-3-apres.out`, OK.
- Mutants : C3-a (contrôle d'ordre retiré en bloc) tué (même commit, même instant, hors descendance) ; C3-c (ascendance
  seule retirée), C3-d (ct(Gc) ≤ ct(S) seul retiré), C3-e (borne basse), C3-f (borne haute), C3-g (date non
  confrontée) tués ; R01 et R02 du réviseur (ancres de `liste_g2.py`) tués ; C3-b (Gc = S seul retiré) vivant,
  équivalent (§6).
- Suite après G2c : 373 tests, OK (2 sauts).

### C-4 — débris d'une tentative interrompue (G2d)

- Provenance [lu] : G2 §3.2 pt 5 et §10 C-4 ; sonde `sonde_coupure.py` (`preuves/sonde_coupure.out`, `7c7dfb37…`).
- Construction appliquée : `destination` refuse (refus `sortie`, code 2) si une entrée `.<nom de --sortie>.*` existe
  dans le dossier parent (`glob` sur le motif échappé), avec ou sans `--deviation` ; motif : le ou les chemins,
  tentative interrompue, à consigner au JOURNAL (heure, motif ; Q8), puis à retirer à la main.
- Test : `test_refus_debris_d_une_tentative_interrompue` : dossier `.sortie.abcd` à côté de `--sortie` : refus
  `sortie`, rien d'écrit, sans `--deviation` puis avec (première exécution présente) ; motif nommant le chemin.
- Échec avant : `preuves/C-4-avant.out` (code 0, gardes levées). Après : `preuves/C-4-apres.out`, OK.
- Mutant : C4-a (contrôle retiré) tué.

### C-5 — sortie d'erreur hors des sorties nommées (G2d)

- Provenance [lu] : G2 §3.2 pt 6 et §10 C-5 ; sonde `sonde_produire.py` (partie P5).
- Construction appliquée : `produire` calcule sous `contextlib.redirect_stderr(io.StringIO())` ; avertissements = lignes
  capturées, préfixe du dossier des journaux (`os.path.join(<journaux>, '')`) retiré ; sorties de la table : étiquette,
  une ligne `[AVERTISSEMENT DU LECTEUR] …` par avertissement, puis le rendu ; `recalcul-tiers` : clé `avertissements`
  (liste, vide sans avertissement) au premier niveau du JSON ; `raw` : verdict, puis les avertissements.
- Test : `test_avertissements_du_lecteur_dans_les_sorties` : dernière ligne de `control.jsonl` et de `raw.jsonl`
  tronquée, deux copies des journaux dans deux dossiers, cinq commandes lancées comme par l'enregistreur (stderr
  fusionnée à la sortie, jeton posé, table de fixture) : sorties identiques à l'octet ; première ligne = étiquette, puis
  un avertissement qui nomme `control.jsonl` sans dossier ; JSON de `recalcul-tiers` relisible, `avertissements` non
  vide ; `raw` : verdict conforme, puis un avertissement qui nomme `raw.jsonl`. Adaptation :
  `test_recalcul_tiers_quatre_recompute_et_variante_incluse` attend la clé `avertissements`, vide.
- Échec avant : `preuves/C-5-avant.out` (sorties différentes entre les deux dossiers : avertissements à chemin absolu
  en tête de sortie ; clé absente). Après : `preuves/C-5-apres.out`, OK.
- Mutants : C5-a (capture retirée), C5-b (réécriture du préfixe retirée), C5-c (clé retirée), C5-d (avertissements avant
  l'étiquette) tués.
- Suite après G2d : 375 tests, OK (2 sauts).

### C-7 — étiquettes « hors décision » (G2e)

- Provenance [lu] : G2 §5 et §10 C-7 ; sonde `sonde_etiquettes.py` (`preuves/sonde_etiquettes.out`, `e3a6723f…`) ;
  décision Q-3 (étiquette du J28 complétée par le script, épingles inchangées).
- Construction appliquée : (a) chaque entrée du JSON de `recalcul-tiers` reçoit `etiquette` : celle de `SORTIES` pour
  les trois sorties, la constante `INCLUSE` (texte du §10, posée hors des délimiteurs de la table) pour `j28-incluse` ;
  (b) étiquette du J28 complétée du texte du §10 (hors décision aussi, §1 bis.1 pt 9 : L&M, queues exactes, strate
  poolée, diagnostic de runs et drapeau du run maximal).
- Tests : `test_recalcul_tiers_quatre_recompute_et_variante_incluse` (étiquettes attendues écrites à la main : celles de
  la table de fixture et le texte de la variante incluse) ; `test_table_reelle_constantes` (nouvelle étiquette du J28
  écrite à la main).
- Échec avant : `preuves/C-7-C-8-avant.out` (étiquette du J28 d'avant ; clé absente des quatre entrées). Après :
  `preuves/C-7-C-8-C-9-apres.out`, OK.
- Mutants : C7-a (clé retirée), C7-b (étiquette du J28 d'avant), C7-c (étiquette du J28 reprise pour la variante
  incluse) tués.

### C-8 — horodatage non numérique ou non fini, SHOGEN-BLOC6-TS-NUM-1 (G2e)

- Provenance [lu] : G2 §7 et §10 C-8 ; sonde `sonde_ts.py` (`preuves/sonde_ts.out`, `71d638e2…`).
- Construction appliquée : `records.filtre_horodatage`, après le contrôle d'absence : ValueError nommée (non numérique
  ou non fini, SHOGEN-BLOC6-TS-NUM-1) si la valeur est un booléen, n'est ni `int` ni `float`, ou n'est pas finie
  (`math.isfinite`) ; le contrôle vaut pour les trois champs d'horodatage, comme celui d'absence ; docstring complétée.
- Test : `TestTsNumerique.test_ts_non_numerique_ou_non_fini_refus_nomme` (`test_lecteur.py`) : relevé `asn_attribution`
  sous segment, `ts` lu par `json.loads` : true, NaN, Infinity, chaîne, chaîne numérique : refus nommé ; entier et
  flottant fini : retenus.
- Échec avant : `preuves/C-7-C-8-avant.out` : true, NaN et Infinity écartés en silence, chaînes en TypeError anonyme.
  Après : OK.
- Mutants : C8-a (contrôle retiré), C8-b (booléen admis), C8-c (non fini admis) tués.

### C-9 — délimiteurs de la table des sorties, SHOGEN-RENDU-TABLE-DELIMITEURS-1 (G2e)

- Provenance [lu] : G2 §7 et §10 C-9.
- Construction appliquée : `monter_prod` exige, avant la substitution, une seule ligne de `rendu_unique.py` qui commence
  par chacun des deux préfixes de la substitution (`# --- table des sorties`, `# --- fin de la`), AssertionError sinon.
- Preuve : mutant C9-a (ligne d'ouverture dupliquée) vivant sur l'instantané G2d (`preuves/C-9-mutant-avant.out`),
  tué après C-9 (`test_nominal_bout_en_bout`).
- Suite après G2e : 376 tests, OK (2 sauts).

### C-10 — non faite

Ajout daté de l'annexe D (D.4 a, DOCS-S2-b) : écrit par l'orchestrateur (brief).

### C-11 — tests manquants (G2f)

- Provenance [lu] : G2 §4 et §10 C-11 ; mutants du réviseur `liste_g2.py` (`2aab4874…`), résultats
  `resultats_g2_survivants.out` (`26f6b511…`).
- Tests : R04 : variante « manifeste BSD » de `test_voie_a_refus` (manifeste au format BSD, jeton sur ce manifeste) :
  refus (5) et (6) ; R05 : lien symbolique pendant à la place de `--sortie` (`test_refus_auteur_sortie_deviation_noms`) :
  refus `sortie` ; R17 : `test_enregistrement_champs_et_sha` sous `mock.patch.dict(os.environ, …)` qui pose
  `PYTHONHASHSEED` (jamais la variable scellée) : `env` de l'enregistrement porte la valeur ; R23 et R24 :
  `TestSensPertes`, bitstamp retiré du journal à ven. 7 23:00Z, plages [ven. 7 22:00Z ; 23:00Z] et [lun. 10 00:00Z ;
  01:00Z] sous le segment [ven. 7 22:00Z ; lun. 10 03:00Z) : bitstamp, hors du pool D1 de la variante incluse en calme
  sous ce segment (aucune lecture ok), non compté (R24) ; kraken absent sur la borne haute de la seconde plage, compté
  (R23) ; R27 : cas « attributs » de `test_echec_a_chaque_pas_rien_ne_reste` (`.git/info/attributes` reçoit
  `*.py eol=crlf` pendant le dernier run) : relecture en refus `tree.sha256`, code 1, rien ne reste.
- Attendus R23 et R24 tirés de la fixture, pas du rendu : marqueurs présents à 22:00, 23:00, 00:00 et 01:00, donc aucune
  fenêtre de grille sans marqueur ; première plage : calme 0, stress 0 lecture absente comptée ; seconde : calme 1,
  stress 0.
- Échec avant : les six mutants vivants sur l'instantané G2e, tests de G2e (`preuves/mutants-G2f-avant.out`). Après :
  tués (`preuves/mutants-G2f.out` ; motifs dans `preuves/mutants-G2f-details.out` : variante BSD levée ; lien pendant
  admis ; `PYTHONHASHSEED` nul ; seconde plage calme 0 au lieu de 1 ; première plage calme 1 au lieu de 0 ; cas
  « attributs » en code 0). R27 : ancre déplacée par C-2 (relecture sur le commit résolu), même mutation (relecture
  sans `--depot`).
- Suite après G2f : 376 tests, OK (2 sauts) (`preuves/suite-G2f.out`).

## 4. Oracles et gates

- Règle scellée SHOGEN-CRITERE-R1-1 : `regle_fixtures.py` sur la base, après G2e et sur l'arbre final : sha256 du JSON
  `ea3a2d94ef1075603e8f7cfc53c68b26e51729b61714028e3fb03dc32f79cb29` les trois fois, `cmp` identiques.
- Épingles : `render_fixture.py` sur les mêmes arbres : sans option
  `4e62fbb8a4a7a29c0761c719c8f731a8247ef407be7a7a04c44219bd093c9a01`, avec option
  `d079dd9d62a3f585a136779330cb21017a300ae853bef5cb63024bb6412de608`, égales à `SHA_BASE_SANS_OPTION` et
  `SHA_BASE_AVEC_OPTION` ; rendus identiques à l'octet (`cmp`) ; aucune re-capture.
- Suite rejouée sur l'export de chaque instantané (`outils/suites_par_instantane.sh`,
  `preuves/suites-par-instantane.out`, `8f9a4b96…`, 12:22 à 12:28 UTC) : base 369, G2a 370, G2b 373, G2c 373, G2d
  375, G2e 376, G2f 376, chacune `OK (skipped=2)`.
- Mutants rejoués sur l'arbre final (`preuves/mutants-final.out`) : 41 mutants, 40 tués, 1 vivant équivalent (C3-b).
- `cargo --locked xtask verify` (biblio présente, 152 fichiers) : avant ce journal, `VERDICT GLOBAL : VERT`, S-G4 80 sur
  80, S-G5 81 sur 81, 252 fragments contrôlés, corpus 125 sur 125, S-G6 126 sur 126, S-G8 36 lignes
  (`preuves/xtask-verify-avant-journal.out`) ; avec ce journal : `VERDICT GLOBAL : VERT`, S-G4 81 sur 81 (79 + 2),
  S-G5 82 sur 82 (80 + 2), 252 fragments contrôlés, corpus 125 sur 125, S-G6 126 sur 126, S-G8 36 lignes ; la sortie
  ne nomme aucune pièce de D.2 (`grep -c` : 0) (`preuves/xtask-verify-avec-journal.out`, `f8315f3a…`, 12:29 à
  12:30 UTC ; rejoué sur la forme finale de ce journal : rapport de remise).
- R-13 : aucun marqueur de dette nu dans le diff total (motif du job g5 : 0 ligne). Hook pre-commit versionné dans un
  clone jetable (`git clone --no-local`, tête `e83b88a`), diff total appliqué (`git apply --check` puis `git apply`),
  ce journal copié, `git add -A` dans le clone, `bash enforcement/hooks/pre-commit` : `OK (hook) : aucune étape en
  refus sur l'index (images locales des jobs g5, g1 et g3)`, code 0 (`preuves/hook-clone-jetable.out`, `c25d34d5…`) :
  R-13, lint d'épinglage et gate des secrets, sur le contenu indexé.

## 5. Écarts (précisions d'application ; aucune construction changée)

1. C-2, test ajouté `test_gardes_lisent_le_head_resolu_une_fois` : les tests listés ne discriminent pas la lecture de
   HEAD par (1), (2), (4) et la voie (b) (HEAD ne bouge pas pendant l'évaluation) ; le test fait rendre X à la
   résolution par une enveloppe de `git` alors que HEAD est sur un commit Y sans parent. La résolution unique est
   paresseuse et mise en cache (première lecture dans g1), non un appel en tête d'`evaluer_gardes` : une résolution
   impossible reste un refus de chaque garde qui la lit.
2. C-2, sonde du HEAD en test : runs factices sur `monter` (et non runs réels sur `monter_prod`) ; le contrôle porté,
   `tree.commit` = X, passe par l'enregistreur et la relecture réels.
3. C-2, `monter_prod` : lint d'épinglage commis à c1 (le module chargé depuis la copie du dépôt lit la liste blanche à
   côté de lui) ; module chargé sans cache (la garde (2) refuse tout fichier ignoré sous ses chemins).
4. C-3, deux variantes ajoutées (épinglage au même instant ; hors de la descendance) : aucune variante listée ne
   discrimine seule la vérification d'ascendance ni ct(Gc) ≤ ct(S).
5. C-1, sous-processus lancés par une enveloppe (`python -c` qui charge l'outil et remplace `SORTIES` par la table de
   fixture : le J28 de la table réelle exige 38 600 fenêtres) ; valeurs refusées en plus de l'absence : vide, répertoire
   sans point, chemin absent, fichier ; les sous-processus reçoivent la variable par `env`.
6. C-5, avertissements gardés tels qu'émis, sans déduplication : une ligne par lecture d'un journal tronqué
   (`recalcul-tiers` en porte une par lecture) ; question Q-a.
7. C-6 : variante en ordre inverse ajoutée (comparaison de listes). C-8 : Infinity et chaîne numérique ajoutées aux
   refus, entier et flottant fini aux cas retenus. C-9 : comptage sur les deux préfixes de la substitution, lignes
   entières.
8. Reflow d'une ligne de 123 caractères introduite en G2a (`test_oracle_record.py`), vue en G2f : chaîne d'instantanés
   reconstruite (`jetable/`) avec ce reflow dès G2a ; `G2a.diff` recapturé (`dc9a8885…`, même numstat), `G2b.diff` à
   `G2e.diff` identiques à l'octet ; ancienne chaîne gardée (`jetable-avant-reflow/`). Sans effet sur le comportement :
   suite rejouée sur chaque instantané (§4).
9. Premier `git status --short` lancé sans `--no-optional-locks` (rafraîchissement possible des métadonnées de l'index,
   aucun contenu) ; ensuite, `--no-optional-locks` sur toutes les lectures git du dépôt.
10. Base des diffs : `54e38ac` (tête au départ) ; la tête a avancé à `e83b88a` (C-10, orchestrateur) sans toucher
   `s2-harness/` (§0).

## 6. Équivalences

- C3-b (seul le contrôle Gc = S retiré) : Gc = S implique ct(Gc) = ct(S), refusé par ct(Gc) ≤ ct(S) ; aucune entrée ne
  distingue le mutant. Le contrôle est gardé tel que la construction le nomme (redondant).
- R03 et R28 (réviseur, §4.1 du G2) : ancres toujours présentes, code inchangé sur ces points ; non rejoués.

## 7. Limites (items à former, règle PAROXYSME)

| item proposé | objet et construction | propriétaire | déclencheur | prix |
|---|---|---|---|---|
| SHOGEN-RENDU-JETON-MAIN-1 | le jeton de C-1 ferme l'appel accidentel de `--produire`, pas l'appel délibéré (la variable posée à la main sur un répertoire à point suffit) : texte de procédure au PAQUET, avec SHOGEN-RENDU-CLI-REPORT-1 (aucun `--produire` hors de l'exécution unique), contrôle FM-1.1 des transcriptions | orch. | G0 du PAQUET | une ligne [inféré] |
| SHOGEN-RENDU-ORC-OCTETS-1 | (4) hache `oracle_record.py` sur le disque au moment de la garde, pas les octets exécutés au chargement (de même pour le script) : lire les octets une fois, exécuter le module depuis ces octets, garder leur sha256 pour (4) | orch. | SHOGEN-RENDU-HOTE-1 | ≈ 6 lignes et un test [inféré] |
| SHOGEN-RENDU-STATUS-HEAD-1 | `git status` de (2) juge l'arbre de travail contre l'index et le HEAD courants, pas contre le commit résolu (la production extrait le commit résolu : l'effet se borne à la garde) : ajouter `git diff --quiet <head> -- CHEMINS` sur l'arbre de travail | orch. | G0 du PAQUET | ≈ 4 lignes et un test [inféré] |
| SHOGEN-GO-PICKAXE-1 | `git log -S` (construction de C-3) compte une sous-chaîne alors que (1) et l'ordre des lignes exigent le sha entier : un commit qui porte le sha dans une suite hexadécimale plus longue serait pris pour S ou Gc ; confirmer S et Gc par `lignes_avec` sur `git show <commit>:JOURNAL.md` | orch. | G0 du PAQUET | ≈ 6 lignes et un test [inféré] |

## 8. Questions pour l'orchestrateur

- **Q-a (C-5)** : dédupliquer les avertissements (une ligne par avertissement distinct) ? La construction dit une ligne
  par avertissement ; appliquée telle quelle, une ligne par émission.
- **Q-b** : les quatre items du §7 entrent-ils à l'annexe B (bloc daté) ?
- Q-4 (B.28) : hors code, item SHOGEN-CP2-RUNS-RENDU-1 ; rien dans les diffs.

## 9. Journal de provenance

### 9.1 Sources lues (toutes [lu] ; aucune [abs] ni [2nd])

- `CLAUDE.md` (racine, sha256 `04200485…`) ; `docs/PASSATION-CLOUD.md` l.1-273 (`f728657f…`) ; `docs/G2-partie-2.md`
  l.1-487 (`0b45a458…`) ; `docs/adr-0028/G0-partie-2.md` l.1-188 (`f47b6541…`) ; `docs/adr-0028/ANNEXE-B-items.md`
  l.417-427, bloc B.28 (`git diff 6eabaa4 54e38ac`) ; `JOURNAL.md` : les deux lignes ajoutées par `54e38ac` (même diff).
- Code, à `54e38ac`, en entier : `s2-harness/tools/rendu_unique.py` (`428f7dc5…`), `oracle_record.py` (`4eb3ed8b…`),
  `tests/test_rendu_unique.py` (`2e877ca1…`), `tests/test_rendu_production.py` (`80c67728…`),
  `tests/test_oracle_record.py` (`ee9dc5a5…`), `tests/test_lecteur.py` (`0682dda0…`) ; en partie :
  `shogen_s2/records.py` l.28-36, l.60-130, l.280-413 (`22924dfa…`), `shogen_s2/report.py` l.660-730,
  `shogen_s2/r1.py` l.385-398 et l.415-455, `tests/test_sensibilite.py` l.1-110 et l.318-352 (`87c746f8…`),
  `xtask/src/sg4.rs` l.38-175, `xtask/src/sg5.rs` l.1-80, `enforcement/gate-secrets.sh` l.1-40,
  `enforcement/hooks/pre-commit` l.1-60.
- Preuves du réviseur (`<S>/g2-partie-2/`), sha256 recalculés : sondes `sonde_produire.py` (`3e22ed2c…`),
  `sonde_hors_depot.py` (`1d0614bf…`), `sonde_head.py` (`bf212f81…`), `sonde_go.py` (`dfcb3bce…`),
  `sonde_coupure.py` (`de4af787…`), `sonde_ts.py` (`05a0382f…`), `sonde_verifier_runs.py` (`cba630ca…`),
  `sonde_etiquettes.py` (`0caf9e5e…`) ; sorties `preuves/*.out` (préfixes cités au §3, égaux à ceux du G2 §13.2) ;
  `mutants/moteur.py` (`3e5869c0…`), `liste_g2.py` (`2aab4874…`), `liste_g2_survivants.py` (`ace26dcb…`),
  `resultats_g2.out` (`a5fb22a9…`), `resultats_g2_survivants.out` (`26f6b511…`).

### 9.2 Commandes et sorties (`<S>/lot-G2corr/`)

- Outils : `outils/instantane.sh` (`804fb34c…`), `outils/moteur.py` (`fa526068…`), listes `mutants_G2a.py`
  (`85b01e1f…`), `mutants_G2b.py` (`807b5582…`), `mutants_G2c.py` (`fb0b8306…`), `mutants_G2c_head.py` (`60686d3a…`),
  `mutants_G2d.py` (`fde8fc39…`), `mutants_G2e.py` (`dd80c8a4…`), `mutants_G2f.py` (`0b96b13e…`), `reflow_g2a.py`
  (`f87607bb…`), `suites_par_instantane.sh` (`75bb0e78…`).
- Échecs avant et succès après : `preuves/C-1-C-6-avant.out` (`a04966b9…`), `C-1-C-6-apres.out` (`1dd1138f…`),
  `C-2-avant.out` (`72cfdfbe…`), `C-2-apres.out` (`224fbead…`), `C-2-head-resolu-avant.out` (`db653686…`),
  `C-2-head-resolu-apres.out` (`d024d7ba…`), `C-3-avant.out` (`92a3ce83…`), `C-3-apres.out` (`34705a8f…`),
  `C-4-avant.out` (`26683b7a…`), `C-4-apres.out` (`2d7f6d6b…`), `C-5-avant.out` (`4016e432…`), `C-5-apres.out`
  (`66285af0…`), `C-7-C-8-avant.out` (`2ac8ee79…`), `C-7-C-8-C-9-apres.out` (`9b507278…`), `C-9-mutant-avant.out`
  (`ee83847f…`), `C-11-tests-code-courant.out` (`7fd62706…`).
- Mutants : `preuves/mutants-G2a.out` (`25a5ee5d…`), `mutants-G2a-C6-rejeu.out` (`4cda4209…`), `mutants-G2b.out`
  (`22ecba46…`), `mutants-G2b-rejeu-de.out` (`6c8bfecb…`), `mutants-G2c.out` (`b160fc72…`), `mutants-G2c-head.out`
  (`d73ca7e7…`), `mutants-G2d.out` (`da964802…`), `mutants-G2e.out` (`2f868e38…`), `mutants-G2f-avant.out`
  (`25c86702…`), `mutants-G2f.out` (`67334b18…`), `mutants-G2f-details.out` (`2a39737f…`), `mutants-final.out`
  (`78f8ea2f…`).
- Suites : `preuves/suite-G2a.out` à `suite-G2f.out` (369 au départ, à 11:36 UTC ; puis 370, 373, 373, 375, 376, 376,
  toutes `OK (skipped=2)`).
- Oracles : `regle-base.json`, `regle-G2e.json`, `regle-final.json` (`ea3a2d94…` chacun) ; `rendus-base/`,
  `rendus-G2e/`, `rendus-final/`.
- Gates : `preuves/xtask-verify-avant-journal.out` (`830316d4…`), `preuves/xtask-verify-avec-journal.out`
  (`f8315f3a…`), `preuves/hook-clone-jetable.out` (`c25d34d5…`) ; rejeux sur la forme finale de ce journal :
  `preuves/xtask-verify-final.out` et `preuves/hook-clone-jetable-final.out`, sha256 dans le rapport de remise.

### 9.3 sha256 des fichiers finaux (arbre de travail ; base `54e38ac` entre parenthèses)

| fichier | final | base |
|---|---|---|
| `s2-harness/shogen_s2/records.py` | `eab3508083190088d1dde18f2cbded3be92829a7f47212029543146e7ca94abf` | `22924dfa…` |
| `s2-harness/tests/test_lecteur.py` | `0d8c99a65ab8e991e0942f9e5d65559cad045536894f36de386918838d651819` | `0682dda0…` |
| `s2-harness/tests/test_oracle_record.py` | `b00fcd8a5f428689b94f058f9f955fab4f0793a734eb61c7be544dd89c1a3f3d` | `ee9dc5a5…` |
| `s2-harness/tests/test_rendu_production.py` | `8a56fbbcff6e4b824c507b3b76fe231ac020aae5896008e93d8b96c886e9018c` | `80c67728…` |
| `s2-harness/tests/test_rendu_unique.py` | `90973bde46a1aba17c17cdb4acc746689785ce9bee7abcdd78ee722bb10095ce` | `2e877ca1…` |
| `s2-harness/tests/test_sensibilite.py` | `faab6cfbfd3c77089f0d61563945e24a4ae83a2970f0e7dd8e8a5f8de90a0905` | `87c746f8…` |
| `s2-harness/tools/oracle_record.py` | `9be02e6b5a50162c4a3595a7b1c1f10d7dc82a201eaf0a38d39a4eeb97c9824f` | `4eb3ed8b…` |
| `s2-harness/tools/rendu_unique.py` | `fac88ec2fbce0ecbc46f43d856377804643de2a9be11979732871336a9faa1b5` | `428f7dc5…` |

### 9.4 Clôture

- Horloge : fin de rédaction à 12:31 UTC ; gates rejouées ensuite sur la forme finale (rapport de remise).
- `SHOGEN_S2_CAMPAGNE_CONTROL` absente de l'environnement de la session (`env | grep -c` : 0) ; `SHOGEN_RENDU_PRODUCTION`
  absente aussi (0) : seuls `produire_tout` et les tests la posent, dans leur processus.
- `git status --short` (sans verrou optionnel) : les huit fichiers du §2 modifiés, ce journal non suivi ; aucune
  opération git en écriture sur le dépôt ; dépôts git en écriture : seulement les dépôts jetables du scratchpad.
- Sha256 de ce journal : dans le rapport de remise (un fichier ne porte pas son propre sha).
- Dettes : aucune hors des items proposés au §7 et des questions du §8.
