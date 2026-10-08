# Relecture G2 — partie 2 de S2 (P0, A, B, C)

**Nature** : relecture G2 unique de la partie 2 (`docs/adr-0028/PLAN-PARTIE-2.md` §4), par une instance neuve qui n'a
écrit aucun lot de la partie (réviseur ≠ générateur). Aucune correction faite : verdict, liste fermée de corrections,
items à former, questions. Périmètre : `git diff cefe134 6eabaa4` (41 commits ; code : 25 fichiers, +2 874 −161 ;
documents : G0, plan, annexes A, B, D, ADR-0028, `docs/DEVOPS.md`, passation, journaux G1, `JOURNAL.md`).

## 0. Gate 0 et cadre

- **Modèle résolu sous lequel le réviseur a tourné : `claude-opus-5-5`** (identifiant exact fourni par l'environnement
  de la session ; préfixe attendu `claude-opus-5-5` : conforme). Effort : `max` (brief).
- Horloge (`date -u`) : 10:43:51 UTC au départ, 2026-10-02 ; clôture au §14.
- Dépôt : branche `partie-2-rendu`, tête `6eabaa413ba27075ce677c95ac44ef61539e26ae`, base `cefe134` ; `git status
  --short` vide au départ. Aucune opération git en écriture ; seul fichier écrit dans le dépôt : ce rapport (non
  suivi). Exports par `git archive` et sondes dans le scratchpad de la session, sous-dossier `g2-partie-2/`.
- Rattachement : brief de l'orchestrateur (relecture G2 de la partie 2) ; contrats : `docs/adr-0028/G0-partie-2.md`
  (sections P0, A, B, C et leurs ajouts datés, sha256 `eaab8f02…`) ; sources : ADR-0028 (§1 bis.1, D2, D4, D6 viii),
  annexe D (D.2, D.4 a, b, c), annexe B (blocs B.20 à B.27), annexe A (lignes P0 à C3f).

## 1. Méthode

1. Lecture de tout le diff de code (`xtask/src/sg4.rs`, `sg5.rs`, `xtask/tests/mutants.rs`, `s2-harness/shogen_s2/`
   `r1.py`, `lm.py`, `r2.py`, `records.py`, `report.py`, `s2-harness/tools/rendu_unique.py` et `oracle_record.py` en
   entier, tests neufs et modifiés) et des documents (G0, plan, annexes, journaux G1 de P0, A, B-1, B-2, B-3, C-1, C-2,
   C-3, lignes ajoutées de `JOURNAL.md`).
2. Oracles rejoués sur la tête : règle scellée (oracle imposé `regle_fixtures.py`, sha256 `5557fb56…`), gates (§6),
   rendus épinglés recalculés sur la base et la tête puis diffés ligne à ligne, suite rejouée sur l'export de chacun des
   24 commits de code du harnais.
3. Sondes sur fixtures seulement (D.4 a) : collecteur réel sur horloge factice, dépôts git jetables, autorité RFC 3161
   de test ; jamais de journal de campagne, jamais de copie scellée, jamais de réseau.
4. Mutants du réviseur : 29 mutants Python (gardes, contexte décimal, lecteur, `verifier_raw`, enregistreur, recalcul
   tiers, rendu, production) et 4 mutants Rust (lot P0), un témoin sans mutation par série ; tout vivant rejoué contre
   la suite entière (369 tests) avant d'être déclaré.
5. Pré-enregistrement : ADR-0025 et `docs/rapports/cartographie-2026-09-29.md` jamais ouverts, exclus de toute
   recherche ; `docs/pocket-report/` non touché ; `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée (`env | grep -c` : 0 au
   départ et à la clôture ; toutes les commandes Python sous `env -u SHOGEN_S2_CAMPAGNE_CONTROL`).

## 2. Point 1 — correction des lots

### 2.1 Règle scellée SHOGEN-CRITERE-R1-1 : inchangée

Oracle imposé (`regle_fixtures.py`, 16 entrées : U1 à U8, J1, J1 à ℓ = 1, J2, J3 à ℓ = 1, J5, J4, seuil, ℓ) sur deux
exports `git archive` :

| arbre | sha256 du JSON |
|---|---|
| `cefe134` (code et fixtures de la base) | `ea3a2d94ef1075603e8f7cfc53c68b26e51729b61714028e3fb03dc32f79cb29` |
| `6eabaa4` (code et fixtures de la tête) | `ea3a2d94ef1075603e8f7cfc53c68b26e51729b61714028e3fb03dc32f79cb29` |
| code de la tête, fixtures de la base | `ea3a2d94ef1075603e8f7cfc53c68b26e51729b61714028e3fb03dc32f79cb29` |
| code de la base, fixtures de la tête | `ea3a2d94ef1075603e8f7cfc53c68b26e51729b61714028e3fb03dc32f79cb29` |

`cmp` : identiques. Le croisement écarte une modification jumelle du code et des fixtures (seule la constante `AX` de
`test_critere.py` a changé, énoncé d'AXES-ENONCE-1 ; elle n'entre pas dans les valeurs de la règle).

### 2.2 Rendus épinglés : seules les lignes des items changent

Fixture des épingles (`tests.test_exclusion.build_fixture`), construite une fois, rendue par la base puis par la tête
(`sondes/rendre.py`) : base `a7f5cbfd…` (sans option) et `b0b4f3b7…` (avec la plage), égales aux épingles de
`cefe134` ; tête `4e62fbb8…` et `d079dd9d…`, égales aux épingles en vigueur. Diff textuel (`preuves/rendus_diff.out`,
sha256 `c2c7bdba…`) : sans option, 2 lignes réécrites (renvoi τ de BLOC3-RENVOI-TAU-1, ligne N_min de
REPORT-FISHER-1) et 6 insérées (`run_params_non_porteurs`, quatre lignes `sautees_*`, ligne « sans ts » du bloc 6) ;
avec la plage, les mêmes et une ligne SENS-PERTES-2. Rien d'autre (FM-3.3 tenu). La ligne N_min égale à la lettre la
forme finale de `docs/G1-lot-DOCS-S2.md` l.77.

### 2.3 Contexte décimal (B0, B3) : tenu au-delà du test

Sonde `sonde_precision.py` (`preuves/sonde_precision.out`, `ed9404fe…`) : rendu J2 sans option, rendu J2 avec plage,
règle et JSON des quatre `recompute_*` sous contextes ambiants changés (précision 60 ; 28 et `ROUND_UP` ; 10 et
`ROUND_DOWN` ; 3, `ROUND_DOWN`, `capitals = 0`, Emin −20) : rendus et recalculs identiques à l'octet. La seule
différence signalée (règle, dernier contexte) vient de l'écriture des `Decimal` par la sonde elle-même hors du contexte
nommé : la comparaison valeur par valeur (`sonde_precision2.py`, `15475043…`) donne 0 valeur différente sous chacun
des quatre réglages.

### 2.4 Lot par lot (G0 et ajouts datés)

| lot | décision du G0 | constat du réviseur |
|---|---|---|
| P0 | S-G4 et S-G5 sur `docs/**/*.md` et `s2-harness/**/*.md`, couverture par chemin, refus sur répertoire absent | conforme ; `PERIMETRE` unique lu par les deux gates ; mutants RS1 à RS4 tués (§4) |
| A1 | `ROUND_HALF_EVEN` aux `localcontext` de `r1.py`, P_more sans annulation | conforme (14 sites comptés à `cefe134` ; le G0 en disait 15, import compris, écart déclaré) |
| A2 | REPORT-FISHER-1, GARDE-LIBELLE-1, BLOC3-RENVOI-TAU-1, RENDU-ZERO-1, AXES-ENONCE-1 (b), SENS-PLAGES-1 | conforme (§2.2) |
| A3 | BLOC1-RUNPARAMS-1, ASN-STATUT-1, SENS-PERTES-2 | conforme ; deux trous de test sur SENS-PERTES-2 (mutants R23, R24 : C-11) |
| B0 | contexte nommé complet pris par les 28 `localcontext` du chemin de recalcul | conforme ; seul `closure.py` (quarantaine) garde `localcontext()` (`grep`) |
| B1 | lecteur en octets, ligne finale non décodable consignée, non finale refusée ; BLOC6-TS-1 | conforme ; `ts` non numérique ou non fini : C-8 |
| B2 | `verifier_raw` : sha256 des octets, appariement par clé et multiplicité | conforme |
| B3 | `recompute_d5_from_journal` ; `_fmt_dec` sous le contexte nommé | conforme |
| B4a-c | enregistreur `shogen.oracle-record.v1`, `--verifier`, CLI | conforme au schéma ; `--verifier` n'exige pas les runs du rendu : C-6 ; consignation d'`env` non éprouvée (R17 : C-11) |
| B5 | CENSURE-CAUSES-1 option (a), deux lignes par strate, aucun seuil | conforme |
| B6a-b | `auteur` exact contre la liste blanche du lint, `--depot`, délai | conforme |
| C1-C2 | bloc machine, gardes (1) à (6), EX-E1-1, voie (a), voie (b) | conformes pour les cas testés ; ouvertures au §3 (C-2, C-3) |
| C3a-f | décisions Q1 à Q8, L3, SHOGEN-RENDU-T0-1, recalcul tiers, production atomique | conformes ; ouvertures et écarts au §3 (C-1, C-4, C-5, C-6, C-7) |

Le journal G1 de l'étape A est une transcription par l'orchestrateur du rapport du worker (versement interrompu par
une erreur de l'API, déclaré en tête du journal) : ses chiffres porteurs sont recomptés ici (§2.1, §2.2 et §8 : 310,
315, 318 tests).

Constantes de la table des sorties recalculées (`datetime`) : 1787770800 = 2026-08-26T19:00:00Z ; 1788980400 =
2026-09-09T19:00:00Z ; 1788480060 = 2026-09-04T00:01:00Z ; plage D5 [1790273880 ; 1790435280] =
[2026-09-24T18:18:00Z ; 2026-09-26T15:08:00Z] ; n fixe 38 600 : conformes à D4, D2 pt 6, D5 et aux décisions Q2, Q3.

## 3. Point 2 — refus par défaut du rendu unique

### 3.1 Gardes relues contre D.4 b

| garde | D.4 b | code (`rendu_unique.py`) | constat |
|---|---|---|---|
| bloc | (G0 §C) | `lire_bloc` l.76-98 | une ouverture exacte, clés uniques, sha complets ; refus sinon (tests et mutants du G1) |
| (1) | sha256 du paquet dans `JOURNAL.md` à HEAD | `g1` l.133-140 | sha entier, ni préfixe ni sous-chaîne ; HEAD relu ailleurs : C-2 |
| (2) | `git diff --quiet <commit> HEAD -- …` et arbre propre | `g2` l.143-152 | conforme ; ignorés et non suivis comptés |
| (3), EX-E1-1 | sha256 des journaux = sommes ; EX-E1-1 : = paquet aussi | `g3` l.155-165 | conforme (fichier = bloc = sommes ; sha des sommes au bloc) |
| (4) | sha256 du script = paquet | `g4` l.168-172 | le script qui s'exécute est contrôlé ; l'enregistreur voisin et le script de HEAD ne le sont pas : C-2 |
| (5) | T_now ≥ T0 + 24 h | `g5` l.245-251 | conforme ; horloge injectable en processus seulement |
| (6) | jeton vérifié ou go épinglé ; l'horloge seule n'ouvre jamais | `voie_a`, `voie_b`, `g6` | horloge seule : refus (tests, code) ; jeton lié à `PAQUET.sha256` qui liste le paquet (E2) ; voie (b) : C-3 |

Ce qui tient : l'horloge seule n'ouvre jamais ((5) et (6) refusent sans voie établie, même en 2100) ; le jeton est lié
aux octets du manifeste et le manifeste au sha du paquet ; aucune sortie ne reste après un échec rattrapé ; la
production n'imprime que des chemins et des sha256.

### 3.2 Ouvertures trouvées (chacune démontrée par une sonde sur fixture)

1. **Chemin non gardé, contenu sur la sortie standard** (`preuves/sonde_produire.out`, `6dfb424f…`) :
   `python -B s2-harness/tools/rendu_unique.py --produire j14-principal --journaux <dossier>` sort 0 et écrit le rendu
   complet (418 lignes, blocs 1 à 6) sur la sortie standard, sans `--depot`, `--paquet`, `--sommes` ni `--auteur` :
   aucune garde n'est évaluée (`main` l.395-396 aiguille avant toute garde). Même chemin pour `raw` (code 0, verdict
   sur la sortie standard) et pour `recalcul-tiers` (montré avec une table de fixture : la table réelle exige 38 600
   fenêtres). D.4 b : « sortie ≠ 0 et aucune sortie écrite, si l'une des conditions suivantes est vraie ».
   Cas d'erreur nommé : l'exécution en refus sur l'hôte prévue avant le scellement (SHOGEN-RENDU-HOTE-1) réunit
   l'outil et les journaux scellés sur le même poste. → **C-1**.
2. **Script et enregistreur hors du commit gardé** (`preuves/sonde_hors_depot.out`, `956abfe1…`) : le script, copié
   hors du dépôt avec un `oracle_record.py` voisin modifié (run `suite` retiré), lève toutes les gardes contre un dépôt
   conforme ; production code 0 ; l'enregistrement de rôle rendu n'a pas de run `suite`. Le test nominal
   `test_nominal_bout_en_bout` repose lui-même sur ce jeu : l'outil du harnais garde un dépôt dont
   `tools/rendu_unique.py` diffère (table de fixture, `test_rendu_production.py` l.184). → **C-2**.
3. **HEAD relu après les gardes** (`preuves/sonde_head.out`, `6b82cf33…`) : gardes levées sur X ; un commit Y retire
   le sha du paquet de `JOURNAL.md` et change `shogen_s2/r1.py` ; `produire_tout(c, …)` sort 0 et enregistre
   `tree.commit` = Y, que les gardes refusent ((1), (2), (5), (6)). Par la ligne de commande, la fenêtre est courte
   (entre `evaluer_gardes` et la résolution de HEAD par l'enregistreur), mais le lien gardes-production n'est pas
   construit. → **C-2**.
4. **Go épinglé dans le commit du scellement** (`preuves/sonde_go.out`, `e9d86195…`) : paquet et go épinglés par un
   seul commit : voie (b) établie, T0 = heure du commit du scellement. D.4 c : « à compter de l'heure du commit JOURNAL
   qui épingle le go « exécuter sans ancre », postérieur au scellement (… l'heure du commit du scellement ne sert plus
   de point de départ) ». Go daté du 2030-01-01 épinglé par un commit du 2026-09-01 : gardes levées le 2026-09-02. Les
   fixtures du test nominal de la voie (b) ont la même forme : `GO_OK` daté du 2026-10-03 (`test_rendu_unique.py`
   l.34), épinglé le 2026-09-01 (l.111), commit du scellement à l'heure réelle. → **C-3** (SHOGEN-GO-ORDRE-1).
5. **Sortie partielle laissée après une coupure** (`preuves/sonde_coupure.out`, `7c7dfb37…`) : arrêt brutal du groupe
   de processus (SIGKILL, comme une coupure de courant) pendant le run `j14-second` : `.sortie.<x>/` reste dans le
   dossier parent avec la sortie de la suite et la sortie `j14-principal` complète ; une nouvelle tentative n'est pas
   refusée (`--gardes-seules` : code 0). G0 §C, Q8 : « un échec avant le renommage final ne laisse rien ». → **C-4**.
6. **Sortie d'erreur mêlée aux sorties** (`preuves/sonde_produire.out`) : `oracle_record.enregistrer` capture
   `stderr=subprocess.STDOUT` (l.151-152). Avec une dernière ligne de `control.jsonl` tronquée (HS2-03, le cas même du
   lecteur tolérant), le fichier `j14-principal` commence par trois lignes d'avertissement (étiquette au rang 3, contre
   Q4 « en tête de chaque fichier de sortie ») ; `recalcul-tiers` porte 21 lignes d'avertissement avant le JSON
   (`json.loads` échoue) ; les avertissements portent le chemin absolu du dossier des journaux, donc les octets et le
   sha256 consigné dépendent de ce chemin. → **C-5**.
7. **`--verifier` du rôle rendu sans les runs** (`preuves/sonde_verifier_runs.out`, `f3b6cf6e…`) : un enregistrement
   de rôle `rendu` à un seul run (`raw`), produit par l'enregistreur du harnais, passe `--verifier --role rendu
   --depot` (code 0, conforme). G0 §B : « le rôle « rendu » exige `paquet.sha256` et le sha256 de chaque sortie ».
   → **C-6**.

## 4. Point 3 — tests discriminants : mutants du réviseur

Moteur `mutants/moteur.py` (`3e5869c0…`) : copie de l'export de `6eabaa4` (`s2-harness` et `enforcement`), une
mutation dont l'ancien texte figure une fois exactement, tests nommés, témoin sans mutation d'abord (VIVANT, 113 tests,
puis 369 tests pour le rejeu) ; liste `mutants/liste_g2.py` (`2aab487…`) ; sorties `resultats_g2.out` (`a5fb22a9…`)
et `resultats_g2_survivants.out` (`26f6b511…`).

| id | lieu | mutation | tests | issue |
|---|---|---|---|---|
| R01 | `voie_b` | première occurrence du go → dernière | suite entière | **vivant** (go cité avant puis après le scellement admis) |
| R02 | `GO` | décalage horaire quelconque admis | suite entière | **vivant** |
| R03 | `g2` | `--no-textconv` retiré de `git diff --quiet` | suite entière | vivant, **équivalent** (§4.1) |
| R04 | `voie_a` | sha du paquet cherché partout dans `PAQUET.sha256` | suite entière | **vivant** |
| R05 | `destination` | `lexists` → `exists` | suite entière | **vivant** (lien pendant en `--sortie` admis) |
| R06 | `g5` | T0 le plus ancien | `test_rendu_unique` | tué |
| R07 | `g3` | comparaison au bloc retirée (EX-E1-1) | `test_rendu_unique` | tué |
| R08 | `lire_bloc` | quatre journaux admis | `test_rendu_unique` | tué |
| R09 | `CONTEXTE_DECIMAL` | piège Overflow retiré | `test_contexte_decimal` | tué |
| R10 | `lm.pairwise_second_moment` | contexte de l'appelant | `test_contexte_decimal` | tué |
| R11 | lecteur | deux dernières lignes tolérées | `test_lecteur` | tué |
| R12 | lecteur | ligne blanche jugée sur les octets | `test_lecteur` | tué |
| R13 | `verifier_raw` | côtés d'absence inversés | `test_lecteur` | tué |
| R14 | `verifier_raw` | base64 non strict | `test_lecteur` | tué |
| R15 | `enregistrer` | auteur non contrôlé à l'écriture | `test_oracle_record` | tué |
| R16 | `liste_blanche` | ligne `ALLOWED` répétée admise | `test_oracle_record` | tué |
| R17 | `enregistrer` | `env` consigné sur un environnement vide | suite entière | **vivant** |
| R18 | `verifier` | `static_only` jugé par fausseté | `test_oracle_record` | tué |
| R19 | `recompute_d5_from_journal` | part vivante sans les plages | `test_censure_causes`, `test_rendu_production` | tué |
| R20 | `produire` | variante incluse prise sur les sorties sans plage | `test_rendu_production` | tué |
| R21 | `demarrages` | marqueur avant tout démarrage indexé | `test_censure_causes` | tué |
| R22 | `demarrages` | tout `clock_check` ouvre un démarrage | quatre modules | tué |
| R23 | SENS-PERTES-2 | borne haute de la plage exclue | suite entière | **vivant** |
| R24 | SENS-PERTES-2 | pool du `run_params` au lieu du pool D1 de la variante | suite entière | **vivant** |
| R25 | `_ligne_variante` | seuil 10 écrit en dur | `test_rendu_libelles`, `test_sensibilite` | tué |
| R26 | énoncé des axes | `any` → `all` | `test_critere`, `test_rendu_libelles` | tué |
| R27 | `produire_tout` | relecture sans `--depot` (`tree.sha256` non recalculé) | suite entière | **vivant** |
| R28 | `produire` | JSON écrit hors du contexte nommé | suite entière | vivant, **équivalent** (§4.1) |
| R29 | `fenetres_sautees_vivant` | portée ignorée | `test_censure_causes` | tué |

Mutants Rust du lot P0 (`rust/mutants_rs.py`, `9bd6a5a2…` ; `resultats_rs.out`, `076c7a17…` ; copie de l'espace de
travail, `cargo --locked --offline test -p xtask`) : témoin 31 + 9 verts ; RS1 (`PERIMETRE` ramené à `docs`) tué, 4
échecs ; RS2 (citations du harnais non contrôlées par S-G5) tué ; RS3 (locutions du harnais non contrôlées par S-G4)
tué ; RS4 (incident « répertoire absent » du harnais avalé par S-G4) tué.

**Bilan** : 33 mutants ; 23 tués ; 10 vivants, dont 2 équivalents (R03, R28) et 8 non équivalents (R01, R02, R04,
R05, R17, R23, R24, R27), chacun porté par une correction (C-3 pour R01 et R02, C-11 pour les six autres).

### 4.1 Équivalences démontrées

- **R03** (`preuves/sonde_git.out`, `0f30acad…`, git 2.43.0) : un textconv qui rend deux versions égales vide le
  patch affiché, mais `git diff --quiet` sort 1 avec et sans `--no-textconv` : la sortie de `--quiet` compare les
  objets. `--no-textconv` reste un serrage sans effet observable ici.
- **R28** : `produire` tourne toujours dans un processus neuf lancé par l'enregistreur ; le contexte décimal y est le
  `DefaultContext` (`capitals = 1`, comme le contexte nommé) et `str()` d'un `Decimal` est exact (ni précision ni
  arrondi). Le `localcontext` est une défense sans effet sur le chemin de production.

## 5. Point 4 — pré-enregistrement

- **D.2** : ADR-0025 et la cartographie du 2026-09-29 n'ont pas été ouvertes par le réviseur ni prises dans une
  recherche ; `git archive` de la tête entière (mutants Rust) les a copiées dans le scratchpad sans lecture ; la sortie
  de `cargo xtask verify`, qui les balaie mécaniquement, ne les nomme pas (`grep -c` sur la sortie, sans affichage :
  0 pour `cartographie-2026-09-29`, 0 pour `adr-0025`, 0 pour `pocket-report`).
- **Journaux G1** : chacun déclare la Gate 0 `claude-opus-5-5` (P0, A transcrit, B-1, B-2, B-3, C-1, C-2, C-3), D.2
  non ouverte, la variable scellée jamais posée (`env | grep -c` : 0) et des fixtures seules ; les lectures gardées de la cartographie (B-2 §1.2 : l.33-34 et l.36-50, l.51 repérée par son
  sha256 et jamais affichée) sont admises par D.2 pt 5. Le JOURNAL du 05:56 UTC consigne une exposition de
  l'orchestrateur de la session cloud (cartographie du 2026-09-29 affichée en entier, l.51 comprise, vers 02:47 UTC),
  « à porter à l'inventaire D.1 au G0 du PAQUET » : aucun item de l'annexe B ne la porte. → item **I-1**.
- **`SHOGEN_S2_CAMPAGNE_CONTROL`** : jamais posée par un G1 (déclarations), ni par le réviseur. L'enregistreur la
  consigne sans la poser ; sa consignation n'est pas testée sur un environnement réel (R17 : C-11).
- **D.4 a** : la liste des lots « fixtures seulement » (annexe D l.110) nomme RENDU-1 et RENDU-2 mais pas DOCS-S2-b
  (étape A : `report.py` et `r1.py`, chemin de recalcul), alors que B-DEP-1, B-DEP-2, CRITERE et D5-AMEND y ont été
  ajoutés par ajout daté. → **C-10**.
- **Étiquettes « hors décision »** (sonde `sonde_etiquettes.py`, `e3a6723f…`) : J14 principal et J14 second étiquetés
  en tête (Q4) ; J28 : étiquette « segment confirmatoire … ; la section [SENSIBILITÉ] … est hors décision ». Deux
  manques au regard du pt 9 de §1 bis.1 (« Hors décision, imprimés et étiquetés : … L&M (bloc 4) ; queue exacte ;
  … ») : (a) le JSON `recalcul-tiers` imprime les valeurs R1, L&M et R2 des deux J14 et de la variante incluse sans
  aucune étiquette de sortie (clés `segment`, `plages`, `r1`, `d5`, `lm`, `r2`) ; (b) le rendu J28 imprime le bloc 4
  (L&M) et les lignes de queue exacte du bloc 3 sans étiquette, et l'étiquette du J28 ne les nomme pas. → **C-7**.

## 6. Point 5 — gates (rejouées sur la tête, 10:44 à 10:47 UTC, puis avec ce rapport en place, §14)

| commande | résultat |
|---|---|
| `cd s2-harness && python -B -m unittest discover -s tests -t .` | `Ran 369 tests`, `OK (skipped=2)` |
| `cargo --locked xtask verify` (biblio présente : 152 fichiers) | `VERDICT GLOBAL : VERT` ; S-G4 79 sur 79 (77 + 2) ; S-G5 80 sur 80 (78 + 2), 252 fragments contrôlés, corpus 125 sur 125 ; S-G6 126 sur 126 ; S-G8 36 lignes |
| `cargo --locked test -p xtask` | 31 + 9 verts |
| `bash enforcement/tests/run-fixtures-hooks.sh` | `hooks : 51 ok, 0 échec` |
| `bash enforcement/tests/run-fixtures-model-pinning.sh` | `model-pinning : 95 ok, 0 échec` |
| `bash enforcement/tests/run-fixtures-secrets.sh` | `secrets : 113 ok, 0 échec` |
| `bash enforcement/gate-secrets.sh --tree` | OK, 350 fichiers |
| `bash enforcement/gate-secrets.sh --history` | OK, 238 commits |

Sorties : `gates/*.out` (`suite.out` `53a0334c…`, `xtask_verify.out` `96c6ab1c…`, `xtask_test.out` `88b2a470…`,
`hooks.out` `1b923027…`, `pinning.out` `44cd6951…`, `secrets.out` `48ca3737…`, `secrets_tree.out` `a1240fec…`,
`secrets_history.out` `ad2f222d…`). R-13 : aucun `TODO` ni `FIXME` nu ajouté (une seule occurrence dans le diff, une
phrase du journal de P0 qui dit leur absence).

## 7. Point 6 — items dont le déclencheur est cette relecture

| item | verdict | construction ou motif |
|---|---|---|
| SHOGEN-SENS-PLAGES-2 | **garder en item** | les sorties pré-enregistrées ne passent qu'une plage (`SORTIES` : J28 seul, `(PLAGE_D5,)`) : le singulier est exact pour chacune ; le pluriel ne vaut que pour un rendu exploratoire à plusieurs plages. Déclencheur à reporter : premier rendu à plusieurs plages, ou tout G0 qui touche la section [SENSIBILITÉ] ; limite écrite au PAQUET |
| SHOGEN-BLOC6-TS-NUM-1 | **à corriger** | C-8 |
| SHOGEN-CONTEXTE-MUTABLE-1 | **garder en item** | aucune écriture : les seuls usages sont `localcontext(CONTEXTE_DECIMAL)`, qui copient (`grep`) ; chaque commande nommée tourne dans un processus neuf. Déclencheur à reporter : tout G0 qui charge `shogen_s2` dans un processus de longue vie (D6 vi, benchmark continu) |
| SHOGEN-ENREG-EOL-1 | **fermer, sans code** | couverture lue : `git check-attr` rend `text: auto`, `eol: lf` pour les 63 fichiers suivis de `s2-harness/`, `eol: lf` pour les 358 fichiers suivis, aucun `export-subst`, `export-ignore`, `ident` ni `filter`. Résidu hors dépôt (attributs locaux de l'hôte) : item I-2 |
| SHOGEN-CAPITALS-REPORT-1 | **fermer, sans code** | audit fait (`sondes/audit_fstrings.py`, `4464abb4…`) : toute valeur `Decimal` écrite par `report.py` passe par `_fmt_dec` ; les autres champs interpolés sont des entiers, des chaînes, des flottants JSON (`parse_float` absent pour `control.jsonl`), le prix (chaîne, `r1.parse_journal`) ou `SEUIL_Z` sans exposant (note de `r2.py` l.652) ; rendus J2 identiques sous `capitals = 0` (§2.3) |
| SHOGEN-GO-ORDRE-1 | **à corriger** | C-3 |
| SHOGEN-RENDU-RENAME-POSIX-1 | **garder en item** | seul un répertoire vide peut être remplacé (non vide : le renommage échoue et rien ne reste), sans perte. Construction affinée : réserver le nom par `os.mkdir(--sortie)` exclusif avant la production (deux exécutions simultanées refusées tôt), renommer sur la réserve vide (POSIX) ou `rmdir` puis `rename` (Windows), retirer la réserve à l'échec. Déclencheur à reporter : SHOGEN-RENDU-HOTE-1 (sémantique Windows à éprouver sur l'hôte) |
| SHOGEN-RENDU-TABLE-DELIMITEURS-1 | **à corriger** | C-9 |

« Fermer, sans code » (ENREG-EOL-1, CAPITALS-REPORT-1) : la construction de ces deux items était une lecture ; elle
est faite ici, ne trouve aucun défaut dans le dépôt, et ne laisse ni correction ni item (le résidu hors dépôt
d'ENREG-EOL-1 devient I-2).

## 8. Point 7 — taille et messages de commit

Numstat de chaque commit, hors `docs/` et `JOURNAL.md` (code et tests), contre la ligne de l'annexe A ; suite rejouée
par le réviseur sur l'export `git archive` de chaque commit (`commits/suites_par_commit.sh`, sans la variable
scellée) contre le compte du message.

| commit | ligne | numstat | total | suite (message) | suite (rejouée) |
|---|---|---|---|---|---|
| `d9f824c` | P0 | +132 −33 | 165 | (annexe A : `cargo test` 31 + 9) | 31 + 9 (tête ; `xtask/` inchangé depuis `d9f824c`) |
| `957525a` | A1 | +125 −18 | 143 | 310 | 310, OK (2 sauts) |
| `37db486` | A2 | +142 −20 | 162 | 315 | 315, OK (2 sauts) |
| `1ed1c29` | A3 | +107 −19 | 126 | 318 | 318, OK (2 sauts) |
| `270d09a` | B0 | +125 −75 | 200 | 321 | 321, OK (2 sauts) |
| `1c35b49` | B1 | +132 −20 | 152 | 326 | 326, OK (2 sauts) |
| `fd498a0` | B2 | +83 −1 | 84 | 328 | 328, OK (2 sauts) |
| `5cb791e` | B3 | +71 −4 | 75 | 330 | 330, OK (2 sauts) |
| `0ad3655` | B4a | +200 −0 | 200 | 333 | 333, OK (2 sauts) |
| `cbd3f7d` | B4b | +88 −0 | 88 | 334 | 334, OK (2 sauts) |
| `ff4ce8c` | B4c | +109 −11 | 120 | 336 | 336, OK (2 sauts) |
| `24dd734` | B5 | +181 −4 | 185 | 340 | 340, OK (2 sauts) |
| `6fde16b` | B6a | +150 −21 | 171 | 342 | 342, OK (2 sauts) |
| `e5d989b` | B6b | +63 −15 | 78 | 343 | 343, OK (2 sauts) |
| `f939c05` | C1a | +102 −0 | 102 | 344 | 344, OK (2 sauts) |
| `b25d394` | C1b | +194 −5 | 199 | 347 | 347, OK (2 sauts) |
| `e52b216` | C1c | +102 −13 | 115 | 349 | 349, OK (2 sauts) |
| `6e779e1` | C2a | +188 −9 | 197 | 353 | 353, OK (2 sauts) |
| `a530dbd` | C2b | +91 −3 | 94 | 356 | 356, OK (2 sauts) |
| `124e2e9` | C3a | +75 −10 | 85 | 358 | 358, OK (2 sauts) |
| `c2cdbc1` | C3b | +152 −3 | 155 | 361 | 361, OK (2 sauts) |
| `4d42859` | C3c | +76 −11 | 87 | 363 | 363, OK (2 sauts) |
| `3626c71` | C3d | +120 −14 | 134 | 365 | 365, OK (2 sauts) |
| `397605c` | C3e | +166 −13 | 179 | 368 | 368, OK (2 sauts) |
| `eba5071` | C3f | +62 −1 | 63 | 369 | 369, OK (2 sauts) |

- Suites rejouées : les 24 commits du harnais sortent chacun `OK (skipped=2)`, au compte exact de leur message
  (11:15 à 11:29 UTC).
- R-25 : 25 commits de code, chacun ≤ 200 lignes (code et tests, ajouts et retraits) ; B0 et B4a au plafond (200).
  Les 16 autres commits de la plage ne portent que des documents.
- Messages : chaque numstat égale celui de sa ligne d'annexe A ; les épingles citées par les messages (A2
  `19865d4f`/`c1fd5391`, A3 `c4f45f47`/`d0f785eb`, B1 `37dfcacb`/`7b6059f5`, B5 `4e62fbb8`/`d079dd9d`) sont celles
  des fichiers de test à ces commits (`git show`). Auteur des 41 commits : l'orchestrateur (R-19, R-20).

## 9. Verdict global

**ACCEPTE-AVEC-CORRECTIONS.** La règle scellée est intacte, les lots A et B font ce que leur G0 dit, les gates sont
vertes, les gardes (1) à (6) tiennent sur les cas testés et l'horloge seule n'ouvre jamais. Mais le rendu unique n'est
pas encore en refus par défaut sur tous ses chemins (C-1 à C-6), deux manques d'étiquette touchent le texte scellé du
pt 9 (C-7), et huit mutants non équivalents survivent (C-3, C-11). Les corrections sont bornées et ne touchent ni la
règle ni les épingles (aucune ne change un rendu de fixture valide).

## 10. Corrections (liste fermée)

Chaque correction : fichier et lignes à `6eabaa4`, construction attendue, test qui la prouvera (échec montré avant la
correction, une mutation par test).

- **C-1 — `--produire` sans garde.** `s2-harness/tools/rendu_unique.py` l.315-347 (`produire`), l.395-396
  (aiguillage), l.350-379 (`produire_tout`). Construction : `produire_tout` pose `os.environ["SHOGEN_RENDU_PRODUCTION"]`
  = chemin absolu du temporaire voisin avant `orc.enregistrer` et la retire dans `finally` ; `produire` refuse (code 2,
  sortie standard vide, motif sur stderr : commande nommée réservée à l'exécution unique) si la variable est absente ou
  ne désigne pas un répertoire existant dont le nom commence par un point. Les tests qui appellent `--produire` posent
  la variable par `mock.patch.dict(os.environ, …)` ; ceux qui exigent le refus la retirent explicitement (la suite
  tourne aussi dans la production, où la variable est héritée). Test : `--produire j14-principal`, `recalcul-tiers`,
  `raw` en sous-processus sans la variable → code 2, sortie standard vide ; avec → code 0 ; test nominal inchangé.
  Mutant : contrôle retiré → rouge.
- **C-2 — script, enregistreur et HEAD liés au commit gardé.** `rendu_unique.py` l.48-50, l.133-172, l.210-226,
  l.264-277, l.362-370. Construction : (i) `evaluer_gardes` résout HEAD une fois (`git rev-parse --verify
  HEAD^{commit}`, sha complet `c["head"]`) ; g1 (`show <head>:JOURNAL.md`), g2 (`diff … <commit_analyse> <head>`),
  `voie_b` (`log … <head>`), `orc.enregistrer(…, c["head"], …)` et `orc.verifier(…, c["head"], …)` lisent ce sha ;
  (ii) g4 exige aussi sha256(`git cat-file blob <head>:s2-harness/tools/rendu_unique.py`) = `sha256_script`, et
  sha256 du fichier chargé comme `orc` = sha256(`<head>:s2-harness/tools/oracle_record.py`). Tests : la sonde
  `sonde_hors_depot.py` en test (copie hors dépôt, enregistreur voisin modifié) → refus (4), rien d'écrit ; la sonde
  `sonde_head.py` en test → `tree.commit` = sha gardé (X), jamais le commit Y posé après les gardes ; adaptations :
  `monter` (`test_rendu_unique.py` l.66-80) commite à c1 les octets de `tools/rendu_unique.py` et
  `tools/oracle_record.py` du harnais ; `monter_prod` (`test_rendu_production.py` l.177-202) lance la copie du dépôt (module chargé depuis
  `<dépôt>/s2-harness/tools/rendu_unique.py`, `sha256_script` = sha de cette copie). Mutants : (ii) retiré, puis
  « HEAD » rétabli dans `produire_tout` → chacun rouge.
- **C-3 — voie (b) : ordre des commits et date du go (SHOGEN-GO-ORDRE-1).** `rendu_unique.py` l.30-31 (`GO`),
  l.210-226 (`voie_b`). Construction : S = premier commit de `git log --no-textconv --reverse --format="%H %ct"
  -S<sha du paquet> <head> -- JOURNAL.md` ; Gc = même chose pour le sha du go ; refus si Gc = S, si S n'est pas
  ancêtre de Gc (`git merge-base --is-ancestor S Gc`), si ct(Gc) ≤ ct(S), ou si la date du go n'est pas dans
  [ct(S) ; ct(Gc)] ; T0 = ct(Gc), inchangé. Tests (`test_voie_b_refus`) : même commit ; go daté après son commit
  d'épinglage ; go daté avant le commit du scellement ; commit d'épinglage daté avant le scellement ; go cité avant le
  scellement puis après (tue R01) ; date à `+01:00` (tue R02). Fixtures : `monter` commite le scellement à une date
  fixe (`GIT_COMMITTER_DATE`, par exemple 2026-08-31T00:00:00Z), `GO_OK` daté entre ce commit et celui d'`epingler`.
  Mutant : contrôle d'ordre retiré → cas « même commit » rouge.
- **C-4 — débris d'une tentative interrompue.** `rendu_unique.py` l.293-306 (`destination`). Construction : refus
  `sortie` (code 2) si une entrée `.<nom de --sortie>.*` existe dans le dossier parent, motif nommant le chemin :
  tentative interrompue, à consigner au JOURNAL (heure, motif ; Q8) puis à retirer à la main. Test : dossier
  `.sortie.abcd` posé à côté de `--sortie` → refus `sortie`, rien d'écrit, avec et sans `--deviation`. Mutant :
  contrôle retiré → rouge.
- **C-5 — sortie d'erreur hors des sorties nommées.** `rendu_unique.py` l.315-347 (`produire`) ; constat né de
  `oracle_record.py` l.151-152. Construction : dans `produire`, calcul sous `contextlib.redirect_stderr(io.StringIO())` ;
  avertissements réécrits sans le préfixe absolu du dossier des journaux ; sorties de la table : étiquette, puis une
  ligne `[AVERTISSEMENT DU LECTEUR] …` par avertissement, puis le rendu ; `recalcul-tiers` : clé `avertissements`
  (liste) au premier niveau du JSON ; `raw` : verdict, puis avertissements. Test : fixture à dernière ligne de
  `control.jsonl` tronquée, commandes lancées comme par l'enregistreur (`stderr=STDOUT`) : première ligne de chaque
  sortie = étiquette (ou verdict), `json.loads` du `recalcul-tiers` réussit et `avertissements` est non vide, sorties
  identiques à l'octet depuis deux copies des journaux dans deux dossiers. Mutant : capture retirée → rouge.
- **C-6 — `--verifier` du rôle rendu : runs exigés.** `oracle_record.py` l.186-234 (`verifier`), l.31
  (`PRODUCTION`). Construction : au rôle `rendu`, `exige([r["nom"] for r in rec["runs"]] == ["suite", *PRODUCTION],
  "runs", …)`. Test : enregistrement de rôle rendu à un seul run → refus (runs) ; à six runs → conforme ; les
  enregistrements « rendu » de `test_oracle_record.py` (l.123, l.133, l.147) deviennent des copies d'un enregistrement
  conforme dont `runs` est réécrit en six runs à sorties écrites par le test. Mutant : contrôle retiré → rouge.
- **C-7 — étiquettes « hors décision » (§1 bis.1 pt 9).** `rendu_unique.py` l.336-342 (`recalcul-tiers`), l.42-44
  (étiquette du J28). Construction : (a) chaque entrée du JSON reçoit une clé `etiquette` : celle de `SORTIES` pour
  les trois sorties ; pour `j28-incluse` : « sensibilité « plage incluse » de la liste fermée (D2 pt 7), hors décision,
  biaisée vers le haut par construction » ; (b) étiquette du J28 complétée : « … ; hors décision aussi (§1 bis.1 pt
  9) : L&M (bloc 4), queues exactes, strate poolée, diagnostic de runs et drapeau « run maximal ≥ ℓ » » (texte de la
  décision Q4 : à arrêter par l'orchestrateur, question Q-3). Tests : `etiquette` de chaque entrée du JSON égale au
  texte écrit à la main ; `test_table_reelle_constantes` porte la nouvelle étiquette du J28. Mutants : clé retirée ;
  étiquette du J28 d'avant → rouges. Les épingles ne bougent pas (étiquettes hors de `render_report`).
- **C-8 — horodatage non numérique ou non fini (SHOGEN-BLOC6-TS-NUM-1).** `s2-harness/shogen_s2/records.py` l.363-367
  (`filtre_horodatage`). Constat (`preuves/sonde_ts.out`, `71d638e2…`) : sous un segment, `ts` = `true`, `NaN` ou
  `Infinity` écarté en silence (« hors segment ») ; `"abc"` → `TypeError` anonyme. Construction : après le contrôle
  d'absence, refus nommé (`ValueError`, horodatage non numérique ou non fini, SHOGEN-BLOC6-TS-NUM-1) si la valeur est
  un booléen, n'est ni `int` ni `float`, ou n'est pas finie (`math.isfinite`). Test : relevé `asn_attribution` à `ts`
  `true`, `NaN`, `"abc"` sous segment → refus nommé. Mutant : contrôle retiré → rouge.
- **C-9 — délimiteurs de la table des sorties (SHOGEN-RENDU-TABLE-DELIMITEURS-1).** `tests/test_rendu_production.py`
  l.177-186 (`monter_prod`). Construction : assertion que chacune des deux lignes de délimitation figure exactement une
  fois dans `rendu_unique.py` avant la substitution. Mutant : ligne d'ouverture dupliquée → rouge.
- **C-10 — D.4 a : DOCS-S2-b.** `docs/adr-0028/ANNEXE-D-preenregistrement.md` l.110. Construction : ajout daté
  « DOCS-S2-b (ajout du 2026-10-02, relecture G2 de la partie 2) » à la liste des lots, comme pour B-DEP-1. Oracle :
  lecture ; `cargo --locked xtask verify` VERT.
- **C-11 — tests manquants (mutants vivants non équivalents).** R04 : `test_voie_a_refus`, manifeste au format BSD
  (`SHA256 (…) = <sha>`), jeton sur ce manifeste → refus (5) et (6). R05 : lien symbolique pendant à la place de
  `--sortie` → refus `sortie`. R17 : `test_oracle_record`, `PYTHONHASHSEED` posé par `mock.patch.dict(os.environ)`
  (jamais la variable scellée) → `env` de l'enregistrement porte la valeur (au-delà de SHOGEN-ENREG-VARIABLE-1, qui
  vise la variable scellée : la consignation d'`env` n'est éprouvée sur aucune variable). R23 : `TestSensPertes`,
  marqueur sur la borne haute d'une plage avec une lecture absente → comptée. R24 : `TestSensPertes`, flux retiré du pool D1 de la
  variante incluse (0 lecture `ok` dans la strate) dont une lecture manque dans la plage → non comptée. R27 :
  `test_echec_a_chaque_pas_rien_ne_reste`, `.git/info/attributes` reçoit `*.py eol=crlf` pendant le dernier run → la
  relecture refuse (`tree.sha256`), rien ne reste. Chaque test rougit sous son mutant (liste `liste_g2.py`).

Coupe R-25 proposée : C-1, C-4, C-9 ; C-2 ; C-3 ; C-5 à C-8 ; C-11 ; C-10 (documents, hors compte).

## 11. Items à former (règle PAROXYSME)

- **I-1 — exposition de l'orchestrateur de la session cloud** : cartographie du 2026-09-29 affichée en entier (l.51
  comprise) vers 02:47 UTC le 2026-10-02 (JOURNAL, entrée de 05:56 UTC). Construction : ligne de l'inventaire D.1 et
  contrôle FM-1.1 de la transcription de cette session au G0 du PAQUET. Propriétaire : orchestrateur ; déclencheur :
  G0 du PAQUET ; prix : une ligne de D.1 et un contrôle [inféré].
- **I-2 — attributs git locaux de l'hôte** : `$GIT_DIR/info/attributes` change la sortie de `git archive` (sonde :
  `*.py eol=crlf` → fins CRLF dans l'extraction), donc `tree.sha256` et les octets extraits dépendent d'une
  configuration hors dépôt (de même `core.attributesFile`). Construction : sur l'hôte de l'exécution, avant le
  scellement, `.git/info/attributes` vide, `core.attributesFile` non posé, `git check-attr eol` LF sur tous les
  fichiers suivis ; ou extraction par blobs bruts. Déclencheur : SHOGEN-RENDU-HOTE-1 ; prix : une commande [inféré].
- **I-3 — rendu des journaux scellés hors du script** : la CLI `python -m shogen_s2.report <dossier> …` (antérieure à
  la partie 2) rend les journaux sans garde ; C-1 ferme le chemin de `rendu_unique.py`, pas celui-ci. Construction :
  texte de la procédure au PAQUET (aucun rendu des journaux scellés hors de `rendu_unique.py` ; contrôle FM-1.1 des
  transcriptions de l'exécution). Déclencheur : G0 du PAQUET ; prix : deux lignes de texte [inféré].
- Items gardés au §7 : SHOGEN-SENS-PLAGES-2, SHOGEN-CONTEXTE-MUTABLE-1, SHOGEN-RENDU-RENAME-POSIX-1, déclencheurs à
  reporter comme indiqué.

## 12. Questions pour l'orchestrateur

- **Q-1 (C-1)** : jeton de production par variable d'environnement (recommandé), ou limite déclarée au PAQUET avec
  I-3 ?
- **Q-2 (C-3)** : la borne basse « date du go ≥ heure du commit du scellement » est un serrage ; la retenez-vous avec
  la borne haute (date du go ≤ commit qui l'épingle) ?
- **Q-3 (C-7 b)** : texte de l'étiquette du J28 (décision Q4) : complété comme proposé, ou étiquette posée dans
  l'en-tête du bloc 4 par `report.py` (re-capture des deux épingles) ?
- **Q-4 (C-6)** : la règle « runs du rendu = suite puis liste de D.4 b » entre-t-elle aussi au contrôle du cp-2 (D6
  viii, schéma inchangé) ?

## 13. Journal de provenance

### 13.1 Sources lues (toutes [lu] ; aucune [abs] ni [2nd])

- `CLAUDE.md` (racine) ; `docs/PASSATION-CLOUD.md` l.1-273 ; `docs/adr-0028/PLAN-PARTIE-2.md` l.1-70 ;
  `docs/adr-0028/G0-partie-2.md` l.1-184 (sha256 `eaab8f02…`).
- `docs/adr-0028/ADR-0028-decisions-sortie-S2.md` l.1-328 (sha256 `bc146415…`) ; `ANNEXE-D-preenregistrement.md`
  l.1-173 (`5fc0cbc1…`) ; `ANNEXE-A-lots.md` l.1-113 (`1995066b…`) ; `ANNEXE-B-items.md` l.320-417 et titres
  (`2d965c9e…`).
- Journaux G1 : `docs/G1-partie-2-P0.md` l.1-60 ; `etape-A.md`, `etape-B-1.md`, `etape-B-2.md`, `etape-C-1.md`,
  `etape-C-2.md`, `etape-C-3.md` en entier ; `etape-B-3.md` l.1-30 et l.298-352 ; `docs/G1-lot-DOCS-S2.md` l.74-84.
- `JOURNAL.md` : les 18 lignes ajoutées par la partie 2 (`git diff cefe134 6eabaa4 -- JOURNAL.md`).
- Code, en entier : `s2-harness/tools/rendu_unique.py` (`428f7dc5…`), `oracle_record.py` (`4eb3ed8b…`) ; diffs de
  `r1.py` (`cde3a78d…`), `lm.py`, `r2.py`, `records.py` (`22924dfa…`), `report.py` (`52bbae68…`), `sg4.rs`
  (`b0f7f125…`), `sg5.rs` (`1d094243…`), `mutants.rs` (`5fb807ff…`) ; `report.py` l.1-310 et l.600-785 ;
  `records.py` l.1-75 et l.276-413 ; `r1.py` l.86-100 et l.386-400 ; `journal.py` l.1-63 ; `xtask/src/sg4.rs`
  l.30-96 ; `enforcement/gate-secrets.sh` l.1-40 ; `.gitattributes`, `fuzz/.gitattributes`,
  `adapters/shogen-tlsn-verify/.gitattributes`.
- Tests : `test_rendu_unique.py`, `test_rendu_production.py`, `test_contexte_decimal.py`, `test_lecteur.py` en entier ;
  `test_sensibilite.py` l.1-80 et l.322-352 ; `test_exclusion.py` et `test_pool_analyse.py` (épingles).

### 13.2 Commandes et sorties (scratchpad `g2-partie-2/`)

- Gates : `gates/run_gates.sh` (§6) ; `journal.txt` : début 10:44:42 UTC, fin 10:47:01 UTC, tous les codes 0.
- Règle : `regle_fixtures.py` sur `arbres/base`, `arbres/tete` et deux arbres croisés : quatre JSON `ea3a2d94…`.
- Rendus épinglés : `sondes/rendre.py` (`7d1a5a2c…`) ; `rendus/*.txt` ; `preuves/rendus_diff.out` (`c2c7bdba…`).
- Sondes (`preuves/`) : `sonde_precision.out` `ed9404fe…`, `sonde_precision2.out` `15475043…`,
  `sonde_produire.out` `6dfb424f…`, `sonde_go.out` `e9d86195…`, `sonde_hors_depot.out` `956abfe1…`,
  `sonde_coupure.out` `7c7dfb37…`, `sonde_ts.out` `71d638e2…`, `sonde_verifier_runs.out` `f3b6cf6e…`,
  `sonde_etiquettes.out` `e3a6723f…`, `sonde_head.out` `6b82cf33…`, `sonde_git.out` `0f30acad…`.
- Mutants : §4 ; suites par commit : `commits/resultats.out` (`6742490b…`, script `dc4ca1ee…`).
- Mesures recomptées : numstat des 41 commits (`git show --numstat`, 25 de code) ; `localcontext(` par module à
  `cefe134` (r1 14, lm 3, r2 10, report 1, closure 1) et à la tête (report 2) ; `git check-attr` (63 et 358
  fichiers) ; constantes de la table (`datetime.fromtimestamp`).

### 13.3 Pré-enregistrement du réviseur

Aucune pièce de D.2 ouverte ; aucun journal de campagne ni copie scellée lus ; `SHOGEN_S2_CAMPAGNE_CONTROL` absente
(`env | grep -c` : 0 à 11:12 UTC et à la clôture) ; aucune donnée de campagne dans ce rapport.

## 14. Clôture

- Gates rejouées avec ce rapport dans `docs/` (11:30 UTC et suivantes, `gates/final/`) : `cargo --locked xtask verify`
  `VERDICT GLOBAL : VERT`, S-G4 80 sur 80, S-G5 81 sur 81, 252 fragments contrôlés, corpus 125 sur 125, 0 violation ;
  suite `Ran 369 tests`, `OK (skipped=2)`. Gate des secrets sur ce rapport indexé dans un clone jetable du
  scratchpad (mode par défaut, contenu indexé) : OK, 1 fichier sans forme d'identifiant ; motif R-13 du hook : 0.
- `git status --short` : `?? docs/G2-partie-2.md` seul ; aucune opération git en écriture sur le dépôt.
- `SHOGEN_S2_CAMPAGNE_CONTROL` absente de l'environnement (`env | grep -c` : 0).
- Sha256 de ce rapport : dans le rapport de remise à l'orchestrateur (un fichier ne porte pas son propre sha).
- Dettes : aucune hors des corrections C-1 à C-11, des items I-1 à I-3 et des items gardés du §7, et des questions Q-1
  à Q-4, rendus à l'orchestrateur.
