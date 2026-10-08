# Journal G1 — partie 2 de S2, étape C, sous-lot C3 (code)

**Nature de ce journal** : journal de provenance du worker de la session cloud, seconde passe de C3, travail du
2026-10-02 à partir de 09:11 UTC (horloge lue par `date -u` : 09:11:02 à la reprise, 10:09:33 avant la rédaction,
10:26:26 à la clôture, §9). Contrat : `docs/adr-0028/G0-partie-2.md` (sha256 `eaab8f02…`), section « C — RENDU-1 »
(l.106-145), ajout daté du 08:44 UTC (l.170-172) et ajout daté du 09:09 UTC (l.174-184 : décisions Q1 à Q8 et L3 sur
les questions de la première passe) ; annexe B, bloc B.26 (l.399-405). Base `4d97a6a` (HEAD inchangé pendant le
travail ; le journal de la première passe, `docs/G1-partie-2-etape-C-2.md`, y est versé, sha256 `8f6503fd…`, non
modifié). Aucune opération git en écriture sur le dépôt ; seuls des dépôts jetables (tests, sondes) sont écrits.
Livrables : arbre de travail portant C3 coupé en six sous-lots C3a à C3f (chacun sous 200 lignes) ; diffs dans
`…/scratchpad/lot-C3/` ; ce journal.

## 0. Gate 0

Modèle résolu sous lequel le worker a tourné : **`claude-opus-5-5`** (identifiant exact fourni par l'environnement de la
session ; préfixe attendu `claude-opus-5-5` : conforme). Effort : `max` (fiche du worker et brief).

## 1. Provenance

### 1.1 Sources lues (toutes [lu] ; aucune [abs] ni [2nd])

- Celles de la première passe (journal `docs/G1-partie-2-etape-C-2.md` §1.1), non relues sauf ci-dessous.
- `docs/adr-0028/G0-partie-2.md` l.165-184 (ajouts datés de l'étape C, dont les décisions du 09:09 UTC) ;
  `docs/adr-0028/ANNEXE-B-items.md` (`75908b63…`) l.395-405 (fin de B.25, bloc B.26).
- `git show --stat HEAD` (fichiers du commit `4d97a6a`) ; `git show HEAD -- JOURNAL.md`, filtré sur les lignes
  ajoutées et coupé à 80 caractères : le début de la ligne de l'orchestrateur qui verse la première passe, rien d'autre.
- Code : `shogen_s2/r1.py` l.813-830 ; `tools/rendu_unique.py`, `tools/oracle_record.py` (en entier, à chaque pas) ;
  `tests/test_censure_causes.py` l.1-123 ; `tests/test_sensibilite.py` l.1-215 (fixture réutilisée).
- Enforcement : `enforcement/lint-model-pinning.sh` l.33 (ligne `ALLOWED`).
- Scratchpad : listes de mutants des passes antérieures, lues pour être rejouées sans modification de leurs fichiers
  (`lot-C1/outils/mutants_c1a.py` à `mutants_final.py`, `lot-B2/outils/mutants_b3.py`, `mutants_b4a.py` à
  `mutants_b4c.py`, `lot-B3/outils/mutants_b4_sur_final.py`, `mutants_b6a.py`, `mutants_b6b.py`) ; moteurs
  `lot-B3/outils/mutants_enf.py` (`677cce97…`) et `lot-C1/outils/faire_diff.py` (`1d7e4b56…`), recopiés à l'identique ;
  `regle_fixtures.py` (`5557fb56…`) et `render_fixture.py` (`4084c42b…`), imposés, utilisés tels quels ;
  `lot-B2/outils/precheck_md.py` (`1b46b7cb…`), pré-contrôle de ce journal avant `xtask` (locutions, guillemets).

### 1.2 Pré-enregistrement (annexe D)

- D.4 a : fixtures seulement (collecteur réel de `tests/test_sensibilite.py`, dépôts git jetables, autorité RFC 3161
  de test produite par `openssl`) ; aucun journal de campagne, aucune copie scellée, aucun réseau.
- D.2 : aucune pièce ouverte ; ADR-0025, la cartographie du 2026-09-29, `docs/pocket-report/` et la copie de
  `JOURNAL.md` du scratchpad exclus de toute lecture et de tout `grep`. Exposition : les 80 premiers caractères d'une
  ligne de `JOURNAL.md` ajoutée par `4d97a6a` (§1.1), sans chiffre de campagne.
- `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée : `env | grep -c` rend 0 ; suites, sondes et moteurs de mutants tournent
  sous `env -u SHOGEN_S2_CAMPAGNE_CONTROL`.
- Fichiers temporaires : depuis 10:01:56 UTC, `TMPDIR` pointe sur `…/scratchpad/lot-C3/tmp` (moteur de mutants et
  suites) ; un dossier `mutB3_…` laissé dans `/tmp` par un rejeu interrompu a été retiré (E10).

### 1.3 Outils écrits (scratchpad `lot-C3/outils/`, sha256)

`mutants_c3a.py` `610a1e14…` ; `mutants_c3b.py` `ea3d0cfe…` ; `mutants_c3c.py` `fb2db4fc…` ; `mutants_c3d.py`
`3da4a2a8…` ; `mutants_c3e.py` `3a3fcc91…` ; `mutants_c3f.py` `5ca5feb4…` (pouvoir du seul test nominal) ;
`mutants_b6_sur_c3.py` `f210513e…` et `mutants_b3_sur_c3.py` `c3211155…` (listes de B6a, B6b et B3, ancres déplacées
par C3 remplacées par leur forme C3, mutation identique) ; `rejeu_final.py` `3a58de42…` (rejeu de toutes les listes
sur l'arbre final, par groupes, avec un témoin sans mutation par groupe) ; `ancres.py` `4624d696…` et `ancres_b4.py`
`9a12af41…` (comptage des ancres) ; `faire_c3b.py` `28a2a227…` et `faire_c3e.py` `3cc10655…` (arbres intermédiaires
par retrait textuel) ; `suite_arbre.sh` `e9fa3019…` (suite sur une copie d'arbre, lint d'épinglage en voisin) ;
`bilan_rejeu.py` `8811f6d6…` (décompte des sorties du rejeu, §4) ; `sonde_sorties.py` `e51f9a81…` (première passe).

### 1.4 État de départ (arbre `4d97a6a`, exporté par `git archive` dans `lot-C3/arbres/base`)

- `s2-harness/` identique à celui de `1bc1142` (`git diff --stat 1bc1142 4d97a6a -- s2-harness` vide) et à l'arbre de
  travail. Suite : `Ran 356 tests`, `OK (skipped=2)`. Règle scellée : `ea3a2d94…`. Rendus épinglés : `4e62fbb8…`
  (sans option), `d079dd9d…` (avec option).

## 2. Décisions appliquées (G0 §C, ajout du 09:09 UTC)

| décision | construction | où | tests |
|---|---|---|---|
| Q1 | sensibilité « plage incluse » = section `[SENSIBILITÉ]` du rendu J28 ; seconde coupe = sortie J14 second ; trois rendus | `rendu_unique.SORTIES` | `test_table_reelle_constantes`, `test_sortie_etiquette_puis_rendu` |
| Q2 | aucune plage aux deux J14 ; déclaré dans l'étiquette : « plage D5 non passée : hors du segment (D2 pt 6 l'applique au J28) » | `SORTIES`, `HORS_J28` | idem |
| Q3 | J14 second `{"t0": 1787770800, "t_fin": 1788480060}` | `SORTIES` | `test_table_reelle_constantes` (bornes recalculées depuis les dates) |
| Q4 | étiquette `[ÉTIQUETTE] <nom> : <texte du G0>` en tête de chaque fichier, écrite par la commande nommée (`--produire`), hors de `render_report` | `rendu_unique.produire` | `test_sortie_etiquette_puis_rendu`, test nominal |
| Q5 | chaque sortie = sortie d'un run nommé de l'enregistreur (`j14-principal`, `j14-second`, `j28`, `recalcul-tiers`, `raw`) ; dossier des journaux substitué au marqueur `JOURNAUX` | `oracle_record.COMMANDES`, `enregistrer(journaux=…)` | `test_journaux_substitues_et_arret_au_premier_echec`, test nominal |
| Q6 | `recalcul-tiers` : JSON `{sortie : {segment, plages, r1, d5, lm, r2}}`, plus `j28-incluse` (sans plage) ; `d5` porte `fenetres_sautees_vivant` | `produire`, `r1.recompute_d5_from_journal` | `test_recalcul_tiers_quatre_recompute_et_variante_incluse`, `test_recalcul_tiers_ventilation` |
| Q7 | commande `raw` : verdict `conforme — lectures N ; avec octets M` ou `refus — <motif>`, code 0 dans les deux cas | `produire` | `test_raw_verdict_et_exit_0` |
| Q8 | runs dans l'ordre `suite`, sorties, `recalcul-tiers`, `raw` ; arrêt au premier échec ; temporaire voisin renommé en une fois ; tout échec : rien ne reste, code 1, heure et run en échec sur stderr ; aucun contenu sur la sortie standard | `rendu_unique.RUNS`, `produire_tout` | `test_echec_a_chaque_pas_rien_ne_reste`, `test_deviation_seconde_sortie_premiere_intacte`, test nominal |
| L3 | noms du bloc exigés `control.jsonl`, `journal.jsonl`, `raw.jsonl` : refus `noms` avant tout rendu | `rendu_unique.main` | `test_refus_auteur_sortie_deviation_noms` |
| C3 (G0 08:44) | SHOGEN-RENDU-T0-1 (`evaluer_gardes`, `ouverture`) ; SHOGEN-ENREG-AUTEUR-ECRITURE-1 ; `--deviation` ; SHOGEN-RAW-FIN-1 ; SHOGEN-RECALCUL-TIERS-CLI-1 ; SHOGEN-CENSURE-CAUSES-TIERS-1 | voir §3 | voir §3 |

## 3. Sous-lots

Coupe R-25 : six sous-lots, chacun mesuré par `faire_diff.py` contre l'arbre précédent. C3b et C3c, puis C3e et C3f,
ont été écrits d'un tenant (228 et 229 lignes), puis coupés : l'arbre intermédiaire est construit depuis l'arbre suivant
par retrait textuel (`faire_c3b.py`, `faire_c3e.py`), puis éprouvé seul (suite, échec avant, mutants). Chaque « échec
avant » est la suite des tests du sous-lot posés sur le code de l'arbre précédent (`suite_arbre.sh`).

### 3.1 C3a — enregistreur : auteur à l'écriture, marqueur JOURNAUX, arrêt au premier échec

- Code (`tools/oracle_record.py`) : `auteur_admis(a)` (prédicat unique, partagé par l'écriture et `verifier`) ;
  `enregistrer(…, journaux=None, arret_premier_echec=False)` : auteur hors liste blanche refusé avant tout git et
  toute commande ; dossier des journaux exigé si une commande porte le marqueur `JOURNAUX`, chemin rendu absolu,
  substitué dans `commande` ; aucun run après un run en échec si l'option est posée.
- Tests (`tests/test_oracle_record.py`) : `test_auteur_refuse_a_l_ecriture` (banni nu et `[1m]`, tier nu, casse,
  `[2m]`, blanc, `None`, entier : refus, `git` remplacé par une fonction qui lève ; CLI : code 2 ; `[1m]` admis et
  conforme) ; `test_journaux_substitues_et_arret_au_premier_echec` (dépôt jetable dont `tools/rendu_unique.py` imprime
  ses arguments ; commande de test posée dans la liste fermée par `mock.patch.dict`). Test existant adapté :
  `test_cli_ecriture_verifier_et_git_dir_herite` passe un auteur admis aux cas « commit inconnu » et « commande en
  échec » (E4).
- Échec avant (`preuves/C3a-avant.out` `3917fa7d…`) : `FAILED (failures=9, errors=1)`. Après : `Ran 11 tests … OK`.
- Mutants (`preuves/C3a-mutants.out` `a1b255cb…`) : **10 tués sur 10** — E1 contrôle absent, E2 contrôle après git, E3
  prédicat par préfixe, E4 `[1m]` refusé, J1 marqueur non remplacé, J2 chemin relatif laissé, J3 dossier absent admis,
  A1 arrêt absent, A2 arrêt inconditionnel, A3 arrêt sans l'option. Listes B6a et B6b rejouées (ancres d'auteur
  déplacées vers `auteur_admis`) : **28 sur 28** (`preuves/C3a-mutants-b6.out` `8ee3959f…`).
- Suite : `Ran 358 tests`, `OK (skipped=2)` (`eaadf77b…`). Règle : `ea3a2d94…`.
- Numstat : outil +27 −8 ; tests +48 −2 ; total **85 lignes**.

### 3.2 C3b — table des sorties, commande `--produire` (sorties et `raw`), commandes nommées

- Code : `tools/rendu_unique.py` : bloc délimité `# --- table des sorties …` / `# --- fin de la table des sorties ---`
  (`T0`, `PLAGE_D5`, `HORS_J28`, `SORTIES`) ; `NOMS_JOURNAUX` ; `HARNAIS` ; chargement de l'enregistreur voisin
  (`orc`) ; `produire(argv)` : sortie de la table (étiquette, puis `render_report` avec ses seules options) ou verdict
  `raw` (code 0) ; aiguillage `--produire` en tête de `main`. `tools/oracle_record.py` : `PRODUCTION` et commandes
  `[-B, tools/rendu_unique.py, --produire, <nom>, --journaux, JOURNAUX]` dans la liste fermée.
- Tests (`tests/test_rendu_production.py`, neuf) : `test_table_reelle_constantes` (bornes recalculées par
  `datetime.fromisoformat` depuis les dates d'ADR-0028, étiquettes du G0, commandes nommées, noms des journaux) ;
  `test_sortie_etiquette_puis_rendu` (table de fixture par `mock`, attendu = étiquette puis `render_report` avec les
  options écrites à la main) ; `test_raw_verdict_et_exit_0` (comptes recomptés dans `raw.jsonl` ; refus sur une copie
  dont une lecture porte un `sha256_raw` faux, par la ligne de commande : code 0).
- Échec avant (`preuves/C3b-avant.out` `6d1ff39c…`) : `FAILED (errors=3)`.
- Mutants (`preuves/C3b-mutants.out` `ed7c5384…`) : **13 tués sur 13** — P1 étiquette absente, P2 plages non
  transmises, P3 segment non transmis, W1 refus en code non nul, W2 comptes absents, W3 refus tenu pour conforme, D1
  `--produire` non aiguillé, C1 commande sans dossier des journaux, T1 J14 second sans + w, T2 J28 à 35 982, T3 plage
  au J14 principal, T4 déclaration Q2 absente, N1 noms des journaux permutés.
- Suite : `Ran 361 tests`, `OK (skipped=2)` (`1e4928a5…`). Règle : identique.
- Numstat : `rendu_unique.py` +51 −2 ; `oracle_record.py` +4 −1 ; tests +97 ; total **155 lignes**.

### 3.3 C3c — recalcul tiers et ventilation (SHOGEN-RECALCUL-TIERS-CLI-1, SHOGEN-CENSURE-CAUSES-TIERS-1)

- Code : `r1.recompute_d5_from_journal` rend aussi `fenetres_sautees_vivant` (même appel que le bloc 1 : marqueurs du
  journal entier, `records.demarrages`, portée, plages) ; `produire recalcul-tiers` : JSON des quatre `recompute_*`
  par sortie et pour `j28-incluse`, `Decimal` en chaîne sous `CONTEXTE_DECIMAL` ; `recalcul-tiers` ajouté à
  `PRODUCTION`.
- Tests : `test_recalcul_tiers_ventilation` (`tests/test_censure_causes.py` ; attendus écrits à la main depuis la
  géométrie : sans option calme 1, stress 4 ; plages stress 3 ; segment calme 1, stress 2 ; égaux à la première ligne
  du bloc 1) ; `test_recalcul_tiers_quatre_recompute_et_variante_incluse` (JSON égal aux quatre fonctions appelées
  ici avec les options de la table de fixture ; n et K de `j28-incluse` égaux aux lignes « incluse » du rendu J28).
- Échec avant (`preuves/C3c-avant.out` `b017ed43…`) : `FAILED (errors=3)`.
- Mutants (`preuves/C3c-mutants.out` `7dbbc821…`) : **10 tués sur 10** — R1 clé absente, R2 sans les plages, R3 hors
  de la portée, P4 sans lm, P5 sans r2, P6 sans d5, P7 variante incluse absente, P8 variante sous plage, P9 recalcul
  sans les plages, C2 `recalcul-tiers` hors de la liste fermée. Liste B3 rejouée (ancres de `recompute_d5_from_journal`
  factorisées) : **10 sur 10** (`preuves/C3b-mutants-b3.out` `310308db…`).
- Suite : `Ran 363 tests`, `OK (skipped=2)` (`f3f6a73c…`). Règle : identique.
- Numstat : `r1.py` +7 −3 ; `rendu_unique.py` +20 −4 ; `oracle_record.py` +1 −1 ; tests +48 −3 ; total **87 lignes**.

### 3.4 C3d — ouverture, auteur, sortie et déviation, noms, mode `--gardes-seules`

- Code (`tools/rendu_unique.py`) : `evaluer_gardes` (refus et contexte ; `verifier_gardes` en rend les seuls refus) ;
  `ouverture(c)` (SHOGEN-RENDU-T0-1 : voie, T0 le plus tardif, genTime de la voie (a) ou nul, ISO 8601 UTC) ;
  `destination(sortie, motif)` ; options `--auteur` (exigée), `--deviation MOTIF`, `--gardes-seules` ; refus `sortie`
  et `auteur` avant toute garde, refus `noms` après les gardes ; production refusée (« construite au sous-lot C3e »),
  état transitoire en refus par défaut.
- Tests (`tests/test_rendu_unique.py`) : `argv()` des tests de gardes porte `--auteur` et `--gardes-seules` ;
  `lancer(f, *plus)` ; `test_ouverture_voie_t0_gentime` (voie (b), voie (a) avec genTime lu ici dans `openssl ts
  -reply -text` par `datetime.strptime`, deux voies) ; `test_refus_auteur_sortie_deviation_noms`.
- Échec avant (`preuves/C3d-avant.out` `4ec40c2a…`) : `FAILED (errors=49)` (options inconnues de l'ancienne ligne de
  commande ; `evaluer_gardes` absent).
- Mutants (`preuves/C3d-mutants.out` `f81bef9d…`) : **12 tués sur 12** — O1 genTime de la voie (b), O2 T0 le plus
  ancien, O3 voie figée, U1 auteur non contrôlé, N1 noms non contrôlés, S1 sortie présente admise, S2 déviation sans
  première exécution, S3 motif vide, S4 motif sur deux lignes, S5 suffixe repris, G1 `--gardes-seules` ignoré, G2
  production non construite admise.
- Suite : `Ran 365 tests`, `OK (skipped=2)` (`db3889bc…`). Règle : identique.
- Numstat : outil +59 −11 ; tests +61 −3 ; total **134 lignes**.

### 3.5 C3e — production (Q5, Q8)

- Code (`tools/rendu_unique.py`) : `RUNS` ; `produire_tout(c, a, cible)` : temporaire `tempfile.mkdtemp` dans le
  dossier parent de la cible ; `DEVIATION.txt` au besoin ; `orc.enregistrer(tmp, "rendu", auteur, racine, "HEAD",
  RUNS, base=commit_analyse, paquet_sha256, sceau_gentime=genTime, journaux, arret_premier_echec=True)` ; run en échec
  nommé (nom, code) ; relecture `orc.verifier(…, "rendu", sha de HEAD, racine)` (exit 0, sha256 de chaque sortie,
  `tree.sha256` recalculé) ; `os.rename` ; `finally` : temporaire retiré à tout échec ; sortie standard : ligne
  `sorties : <cible> (voie … ; T0 … ; genTime …)`, puis nom, sha256 et chemin de chaque run, puis l'enregistrement.
  `main` : la production remplace le refus transitoire de C3d.
- Tests (`tests/test_rendu_production.py`) : runs factices (`subprocess.run` remplacé pour les seules commandes lancées
  par `sys.executable`, git et openssl passent) ; `test_echec_a_chaque_pas_rien_ne_reste` (échec à chacun des six
  runs ; sortie altérée pendant le dernier run ; extraction ; renommage ; gardes refusées sans `--gardes-seules`) ;
  `test_deviation_seconde_sortie_premiere_intacte` ; `test_gentime_du_jeton_dans_l_enregistrement` (voie (a), autorité
  de test). Retiré de `test_rendu_unique.py` : le contrôle du refus transitoire de C3d (E9).
- Échec avant (`preuves/C3e-avant.out` `b6e1203f…`) : `FAILED (failures=11)`.
- Mutants (`preuves/C3e-mutants.out` `7c0fb377…`) : **15 tués sur 15** — M1 temporaire non retiré, M2 temporaire hors
  du dossier parent, M3 arrêt absent, M4 suite après les sorties, M5 `recalcul-tiers` avant les sorties, M6
  enregistrement non relu, M7 renommage absent, M8 motif non écrit, M9 genTime non transmis, M10 base non transmise,
  M11 contenu imprimé, M12 heure absente, M13 production malgré `--gardes-seules`, M14 dossier des journaux non
  transmis, M15 run en échec non nommé.
- Suite : `Ran 368 tests`, `OK (skipped=2)` (`39186fce…`). Règle : identique.
- Numstat : outil +47 −7 ; tests +119 −6 ; total **179 lignes**.

### 3.6 C3f — test nominal de bout en bout (tests seuls)

- `monter_prod` : dépôt jetable dont le commit d'analyse porte `shogen_s2/` et `tools/` du harnais, la seule table des
  sorties de `rendu_unique.py` remplacée par la table de fixture (entre les deux lignes de délimitation), une suite
  triviale ; journaux du collecteur réel et sommes hors dépôt ; paquet, `JOURNAL.md`, go épinglé.
  `test_nominal_bout_en_bout` : code 0 ; seul ajout au dossier parent : la sortie ; runs dans l'ordre `suite`,
  `j14-principal`, `j14-second`, `j28`, `recalcul-tiers`, `raw` (liste écrite à la main) ; chaque sortie égale à son
  attendu ; `oracle_record.py --verifier … --role rendu --commit <HEAD> --depot <dépôt>` : code 0 ; `paquet.sha256`,
  genTime nul (voie (b)), `base` = commit d'analyse, rôle `rendu` ; sortie standard égale à l'affichage attendu.
- Échec avant (test posé sur le code de C3d, `preuves/C3f-avant.out` `64cee1c0…`) : `FAILED (failures=1)` (code 2, rien
  d'écrit).
- Pouvoir du seul test nominal (`preuves/C3f-nominal-mutants.out` `43e16be3…`) : listes C3e et C3b rejouées contre lui
  seul : 12 sur 28 tués (ordre, renommage, base, contenu imprimé, dossier des journaux, étiquette, options, aiguillage,
  commande, noms) ; les autres sont des chemins d'échec ou des constantes, tués par les tests de C3b et C3e.
- Suite : `Ran 369 tests`, `OK (skipped=2)` (`38b0205d…`). Règle : identique.
- Numstat : tests +62 −1 ; total **63 lignes**.

## 4. Rejeu de toutes les listes sur l'arbre final

- Outil : `rejeu_final.py` (`3a58de42…`), moteur `mutants_enf.py` recopié (lint d'épinglage en voisin), sur
  `s2-harness/` de l'arbre de travail (égal à l'instantané C3f : `diff -r` vide), sous `env -u
  SHOGEN_S2_CAMPAGNE_CONTROL`, `TMPDIR` au scratchpad. Par groupe : un témoin sans mutation (il doit rester VIVANT),
  puis chaque mutant avec les tests de sa liste ; une ancre absente ou multiple sur l'arbre final est déclarée
  OBSOLÈTE et n'est pas lancée. Quatre lancements parallèles de 10:09 à 10:24 UTC, par indices de groupe : A `0 1`, B
  `2 3`, C `4 11 12`, D `5 6 7 8 9 10` ; chacun finit sur `fin rc=0`.
- Sorties : `preuves/rejeu-final-A.out` `1d130e9c…`, `-B.out` `3e17afab…`, `-C.out` `ae479373…`, `-D.out`
  `e511ce1b…`. Décompte par `bilan_rejeu.py` (`8811f6d6…`), sortie `preuves/rejeu-final-bilan.out` `b12e9446…` ; chaque
  groupe y égale la ligne `--- N tués` de l'outil, et les lignes `TOTAL` des quatre lancements (30, 32, 42, 121)
  somment au total du bilan.

| liste (dossier du scratchpad) | tests | listés | tués | vivants | obsolètes | témoin |
|---|---|---|---|---|---|---|
| `mutants_c1a.py` (`lot-C1`) | `test_rendu_unique` | 13 | 13 | 0 | 0 | VIVANT |
| `mutants_c1c.py` (`lot-C1`) | `test_rendu_unique` | 17 | 17 | 0 | 0 | VIVANT |
| `mutants_c2a.py` (`lot-C1`) | `test_rendu_unique` | 16 | 16 | 0 | 0 | VIVANT |
| `mutants_c2b.py` (`lot-C1`) | `test_rendu_unique` | 16 | 16 | 0 | 0 | VIVANT |
| `mutants_final.py` (`lot-C1` : C1b sans N1 ni neutralisations) | `test_rendu_unique` | 17 | 17 | 0 | 0 | VIVANT |
| `mutants_b4_sur_final.py` (`lot-B3` : B4a à B4c réancrées) | `test_oracle_record` | 50 | 50 | 0 | 0 | VIVANT |
| `mutants_b6_sur_c3.py` (`lot-C3` : B6a et B6b) | `test_oracle_record` | 28 | 28 | 0 | 0 | VIVANT |
| `mutants_b3_sur_c3.py` (`lot-C3` : B3) | un test de `test_d5_amend`, un de `test_contexte_decimal` | 10 | 10 | 0 | 0 | VIVANT |
| `mutants_c3a.py` | `test_oracle_record` | 10 | 10 | 0 | 0 | VIVANT |
| `mutants_c3b.py` | `test_rendu_production`, `test_censure_causes` | 13 | 13 | 0 | 0 | VIVANT |
| `mutants_c3c.py` | `test_rendu_production`, `test_censure_causes` | 10 | 10 | 0 | 0 | VIVANT |
| `mutants_c3d.py` | `test_rendu_unique` | 12 | 10 | 0 | 2 | VIVANT |
| `mutants_c3e.py` | `test_rendu_production`, `test_rendu_unique` | 15 | 15 | 0 | 0 | VIVANT |
| **total** (13 groupes) | | **227** | **225** | **0** | **2** | 13 VIVANT |

- Obsolètes : G1 (`--gardes-seules` ignoré) et G2 (production non construite admise) de C3d ; leurs ancres sont
  celles du refus transitoire retiré par C3e (E9). Le comportement de G1 est tenu sur l'arbre final par M13 (tué).
- Hors preuve : `preuves/rejeu-final-interrompu.out` (`f4e82e99…` ; groupe C1a seul, 9 tués, témoin VIVANT) et
  `rejeu-final-interrompu-2.out` (`4438442b…` ; groupe C1a seul, 12 tués, témoin VIVANT). Le premier lancement
  séquentiel (10:00 UTC) a été arrêté par le worker pour ajouter le motif d'échec nommé (E11) ; le second (10:07 UTC,
  code final) a été arrêté pour sa durée, puis relancé en quatre parts. Leurs groupes sont tous repris par A à D.

## 5. Empreintes

- Diffs (étiquettes `a/s2-harness/…`, `b/s2-harness/…`, sans opération git), chacun contre l'arbre précédent :
  `C3a.diff` `8fe80c048671cd60b114d09ed4c475706ac53c432d0f01885725b820c95d0bf5` (contre `4d97a6a`) ; `C3b.diff`
  `d6190c983653d7677d8f86dc133e5d3875e267513099b9d4c5c7f2f84ca07c38` ; `C3c.diff`
  `aa0df8eaf27fa9962aeed7b8795813bd8da3c21fd84b62aa765014e8c20bdc22` ; `C3d.diff`
  `8281aad98838608a90adc51b1fb4b6c54fe0931d519c03ce70cb93cb4f15dc70` ; `C3e.diff`
  `9edce39e772b3c5071adb4e75b8e5d04522b2545c526b16be8a34fea62db8cab` ; `C3f.diff`
  `50c621ae5e2b5d013f70403319fe23daf161cb72c04630c03f00d57c44c9ca2c`. Contrôle : export de `4d97a6a`, `patch -p1` de
  chaque diff dans l'ordre : chaque instantané est reproduit, la fin de chaîne égale l'arbre de travail (`diff -r`
  vide). Total : 703 lignes.
- Fichiers finaux (sha256) : `s2-harness/tools/rendu_unique.py`
  `428f7dc59057e858bf1539710c2195ceaee5f7351bf2e11b74bfd71b52235887` (425 lignes) ; `s2-harness/tools/oracle_record.py`
  `4eb3ed8ba5089ec7ba4ff602fd948a2ffd4a1e91cdaa49b91a0481abb9be9179` (271) ; `s2-harness/shogen_s2/r1.py`
  `cde3a78de1b7e57f5b1cb756e7f7d80e31f657302cb738f0115475383c594ec0` ; `s2-harness/tests/test_rendu_production.py`
  `80c67728ff1270e3d4f6d64b4c2e08208aa442ff1a7dcae12f64d8371156de05` (neuf, 308) ;
  `s2-harness/tests/test_rendu_unique.py` `2e877ca144380b1b404063d6910ab75907f1d756b2e82f03e61e22a30192f737` ;
  `s2-harness/tests/test_oracle_record.py`
  `ee9dc5a5561b002df765eb21c61d7f9df118a1d6633707e81752230019646794` ; `s2-harness/tests/test_censure_causes.py`
  `860349fa9f2aa05af81bda701259b679263fa49e184caa3d7516d68ac5b6af6b`.
- Suites recomptées : 356 (départ) → 358 (C3a) → 361 (C3b) → 363 (C3c) → 365 (C3d) → 368 (C3e) → 369 (C3f), deux sauts
  à chaque pas (les deux tests de la variable scellée).
- Règle scellée : `ea3a2d94…` sur les sept arbres (`regle/*.json`, `cmp` identiques). Épingles : `report.py` n'est pas
  touché ; rendus de la fixture des épingles identiques à l'octet sur la base et l'arbre final (`4e62fbb8…` sans option,
  `d079dd9d…` avec option) : aucune re-capture.
- R-13 et secrets : motif R-13 du hook et motifs VENDOR et GENERIC de la gate des secrets rejoués par `grep` sur les
  sept fichiers touchés et ce journal : 0 occurrence. Aucune dépendance neuve (`importlib`, `json`, `decimal`,
  `tempfile`, `glob`, `contextlib` : bibliothèque standard).

## 6. Écarts

- **E1 (coupe)** : six sous-lots au lieu des trois proposés (C3b et C3c coupés, C3e et C3f coupés) ; arbres
  intermédiaires construits par retrait textuel, chacun éprouvé seul.
- **E2 (mode `--gardes-seules`)** : option neuve, hors des décisions : gardes, refus préalables et noms évalués, rien de
  produit, « gardes levées », code 0. Elle garde les tests de gardes sans production et sert l'exécution en refus sur
  l'hôte avant le scellement (SHOGEN-RENDU-HOTE-1).
- **E3 (refus préalables)** : `--auteur` exigé ; refus `auteur` (prédicat `auteur_admis` du lint) et refus `sortie`
  (destination) avant toute garde ; refus `noms` (L3) après les gardes, avant tout rendu, en production comme en mode
  `--gardes-seules`.
- **E4 (test existant adapté)** : `test_cli_ecriture_verifier_et_git_dir_herite` passait l'auteur `a` ; l'écriture le
  refuse désormais : auteur admis pour les cas « commit inconnu » et « commande en échec ».
- **E5 (déviation)** : répertoire `<sortie>.deviation-<k>` (premier libre), fichier `DEVIATION.txt` (« seconde exécution
  déclarée (ADR-0028 annexe D.4 b) ; première : … ; motif : … »), motif d'une ligne non vide ; refus sans première
  exécution.
- **E6 (textes)** : étiquette `[ÉTIQUETTE] <nom> : <texte>` ; textes de Q4 repris à la lettre ; déclaration de Q2
  rédigée par le worker : « plage D5 non passée : hors du segment (D2 pt 6 l'applique au J28) » ; verdict `raw` rédigé
  par le worker.
- **E7 (verdict `raw`)** : imprimé par sa commande dans sa sortie capturée (sha256 enregistré), jamais recopié sur la
  sortie standard de l'exécution (Q8 : aucun contenu de sortie imprimé).
- **E8 (genTime)** : `sceau.genTime` = genTime lu par `gentime()`, en ISO 8601 UTC à la seconde (fraction portée à la
  seconde suivante, le T0 de la garde (5)).
- **E9 (transitoire)** : en C3d, la production refusait (« construite au sous-lot C3e ») ; ce refus et son contrôle
  dans `test_rendu_unique.py` sont retirés par C3e ; les mutants G1 et G2 de C3d sont sans ancre sur l'arbre final
  (G1 y est couvert par M13).
- **E10 (fichiers temporaires)** : le moteur de mutants recopié écrit sous `tempfile` ; un rejeu interrompu a laissé un
  dossier dans `/tmp`, retiré ; depuis, `TMPDIR` pointe sur le scratchpad.
- **E11 (motif d'échec)** : le run en échec est nommé (nom, code) sur stderr, ajouté après une première série de
  preuves de C3e ; C3e et C3f rejoués ensuite en entier (arbres, diffs, suites, échec avant, mutants).
- **E12 (enregistrement)** : `tree.commit` = HEAD du dépôt (extraction par l'enregistreur) ; `base` = `commit_analyse`
  du bloc.

## 7. Limites rencontrées (items à former, règle PAROXYSME)

- **L1 — SHOGEN-RENDU-ECHEC-DIAG-1** : à l'échec, rien ne reste (Q8), pas même la sortie du run en échec ; le motif ne
  porte que le nom et le code. Diagnostiquer une sortie en échec demande une nouvelle tentative (consignée, Q8).
  Construction : garder sur stderr la fin de la sortie du seul run `suite` (sans donnée de campagne), ou consigner au
  PAQUET que la suite se rejoue d'abord en enregistrement de rôle G1. Déclencheur : G0 du PAQUET. Prix ≈ 5 lignes ou
  une ligne de texte [inféré].
- **L2 — SHOGEN-RENDU-COUT-1** : coût des runs sur les journaux réels non mesurable avant l'exécution (D.4 a) ; le
  délai par commande reste `DELAI_DEFAUT` (3 600 s) pour le rendu J28 et pour `recalcul-tiers` (quatre recalculs sur
  quatre variantes). Un dépassement = tentative échouée. Construction : mesure sur un journal synthétique à la taille de
  la campagne avant l'exécution, puis délai écrit au PAQUET (SHOGEN-RAW-MEMOIRE-1 voisin). Déclencheur : partie 3 ou 4.
  Prix : une mesure [inféré].
- **L3 — SHOGEN-RENDU-RENAME-POSIX-1** : l'absence de la cible est contrôlée avant les gardes ; sous POSIX, `os.rename`
  d'un répertoire sur un répertoire vide apparu entre-temps le remplace (sous Windows, refus). Construction : second
  contrôle juste avant le renommage, ou nom de cible réservé par un fichier marqueur. Déclencheur : relecture G2 de la
  partie 2. Prix ≈ 3 lignes et un test [inféré].
- **L4 — SHOGEN-RENDU-TABLE-DELIMITEURS-1** : le test nominal remplace la table des sorties entre les lignes
  `# --- table des sorties` et `# --- fin de la table des sorties ---` ; ces deux lignes font partie du contrat du test
  (SHOGEN-RENDU-TABLE-REELLE-1, B.26). Construction : test qui exige chacune une fois. Déclencheur : relecture G2.
  Prix ≈ 3 lignes [inféré].

## 8. Questions ouvertes

- **Q1** : la déclaration de Q2 dans l'étiquette des J14 (texte du worker, E6) convient-elle, ou faut-il un texte de
  l'orchestrateur ?
- **Q2** : le mode `--gardes-seules` (E2) entre-t-il à la procédure d'exécution (partie 4 : exécution en refus sur
  l'hôte avant le scellement, SHOGEN-RENDU-HOTE-1) ?
- **Q3** : L1 : faut-il garder un diagnostic du run `suite` en échec, malgré « rien ne reste » ?

## 9. Clôture

- Suite finale (10:14 UTC, arbre de travail, `TMPDIR` au scratchpad, `env -u SHOGEN_S2_CAMPAGNE_CONTROL`) : `Ran 369
  tests in 48.230s`, `OK (skipped=2)` (`preuves/suite-finale.out` `69cbf2fb…`). Départ : 356 tests (§1.4).
- Mutants : par sous-lot, 60 tués sur 60 (C3a à C3e), plus les listes B6a, B6b et B3 rejouées (38 sur 38) ; au rejeu
  final, 225 tués sur 227 listés, 0 vivant, 2 obsolètes, 13 témoins VIVANT (§4).
- Règle scellée `ea3a2d94…` et épingles inchangées (§5) ; la règle, recalculée à 10:27 UTC par `regle_fixtures.py`
  sur l'arbre de travail final, est identique à l'octet à `regle/HEAD.json`. R-13, secrets : 0 (§5, rejoués sur ce
  journal achevé).
- `SHOGEN_S2_CAMPAGNE_CONTROL` : absente de l'environnement (`env | grep -c` : 0) à la reprise comme à la clôture ;
  aucun dossier temporaire laissé (`lot-C3/tmp` vide ; rien dans `/tmp` daté de cette passe hors des fichiers de
  l'environnement).
- État du dépôt (10:26 UTC) : HEAD `4d97a6a`, branche `partie-2-rendu` ; `git status --short` : six fichiers modifiés
  (`s2-harness/shogen_s2/r1.py`, `s2-harness/tests/test_censure_causes.py`, `s2-harness/tests/test_oracle_record.py`,
  `s2-harness/tests/test_rendu_unique.py`, `s2-harness/tools/oracle_record.py`, `s2-harness/tools/rendu_unique.py`),
  deux neufs (`s2-harness/tests/test_rendu_production.py`, ce journal) ; aucune opération git en écriture. Chaîne des
  six diffs rejouée à 10:27 UTC depuis l'export de `4d97a6a` : chaque instantané reproduit, fin de chaîne égale à
  l'arbre de travail.
- `cargo --locked xtask verify` sur ce journal achevé, à cette ligne près (10:28 à 10:29 UTC, code 0,
  `preuves/xtask-cloture.out` `ace8a001…`) : `VERDICT GLOBAL : VERT` ; huit gates (S-G1 à S-G6, S-G7a, S-G8) à 0
  violation ; S-G4 79 fichiers sur 79 (77 sous `docs/`, ce journal compris, et 2 sous `s2-harness/`) ; S-G5 80 sur
  80, 252 fragments contrôlés, 2 912 écartés sous seuil, corpus 125 sur 125 ; `cargo fmt --check`, `no_std` du
  vérificateur, `cargo clippy -D warnings` : VERT.
- Dettes : aucune hors des items L1 à L4 (§7) et des questions Q1 à Q3 (§8), rendus à l'orchestrateur.
