# G1 du lot DETTES-B1 (harnais `s2-harness`) — huit items du brief et SHOGEN-TEST-ENV-HERMETIQUE-1

- **Rattachement** : G0 `docs/adr-0028/G0-lots-DETTES.md` (lot DETTES-B1, l.22 ; règles communes l.9-14 ; lu en entier) ;
  brief `BRIEF-DETTES-B1.md` (sha256 `294c291dcd7f56bbd3977fffd7e9b6a37145b7c21cd55154afcad10f173641ee`, contrôlé au
  départ) ; état du registre `docs/adr-0028/ETAT-REGISTRE-2026-10-04.md` (l.49, 52, 53, 68-72, 165-169, 243, 269, 283,
  377-379, 384-385) ; définitions de l'annexe B : B.4 l.79 (SHOGEN-CI-S2-SAUT-1), B.9 l.174 (SHOGEN-KEFF-NOTE-1), B.12
  l.209 et B.13 l.226 (SHOGEN-SENS-POOLEE-1), B.44 l.639-641 (SHOGEN-PRIX-ILLISIBLE-1, SHOGEN-PRIX-HORS-CONTEXTE-1,
  SHOGEN-ASN-DIVERGENCE-PARTIELLE-1), B.46 l.681-682 (SHOGEN-BLOC5-LIBELLE-1, SHOGEN-RT-ETIQUETTE-INCLUSE-1) ; sous-lot
  D8a-3 : `docs/adr-0028/G0-lot-D8a.md` l.436 (item 13 ; le brief cite l.430-440). Item ajouté par l'orchestrateur en
  cours de passe (message reçu pendant la lecture des sources ; constat mesuré par lui à 03:59 UTC) :
  SHOGEN-TEST-ENV-HERMETIQUE-1, livré en sous-lot séparé.
- **Worker** : `claude-opus-5-5` (Gate 0, §0), effort `max` selon la fiche `shogen-worker` (réglage non observable
  depuis l'agent).
- **Horloge** (`date -u`) : départ 2026-10-04 03:57:56Z ; dernière vérification 05:46:07Z ; journal clos à 05:48:54Z ;
  heures des étapes aux §3 à §11.
- **Dépôt** : `/home/user/shogen`, branche `partie-4-execution`, HEAD `5afbdd26dc3a0f773ffaa87f2ef6b3201766df1d`
  (`5afbdd2`), arbre propre (`git status --short` vide). git employé en lecture seule (`rev-parse`, `status`, `log -5`,
  `show HEAD:biblio/INDEX.md`) ; `git apply` employé hors de tout dépôt, sur mes copies. Aucune écriture dans le dépôt.
- **Copies** (dossier `DETTES-B1/`, ci-après `B1/`) : `B1/arbre` = `git archive HEAD | tar -x` avec les quatre
  exclusions du brief, plus `biblio/INDEX.md` (blob `bc572b86e8cdbbd574add16d49e69d3564003805`, égal à celui de HEAD) ;
  arbres de travail par sous-lot `B1/dev/<k>/` (copies de `s2-harness`, `enforcement`, `.github`, `scripts`) ; arbre
  série `B1/serie/` (copie complète de `B1/arbre`, puis les sept diffs).

## 0. Gate 0

Modèle résolu : **`claude-opus-5-5`** (identifiant exact fourni par l'environnement de la session) ; préfixe attendu des
workers (CLAUDE.md §7) : conforme.

## 1. Attestation et expositions déclarées

« Le worker G1 du lot DETTES-B1 (`claude-opus-5-5`) n'a ouvert aucune pièce de la liste fermée D.2 (liste lue à
l'annexe D l.32-47, sans ouvrir aucune pièce) ; il n'a rien lu sous `docs/rapports/`, `docs/adr-0025/`,
`docs/adr-0028/monark-m009a/` (exclus de la copie à la source), ni `docs/15-*`, `docs/16-*`, `docs/pocket-report/`
(présents dans la copie, jamais ouverts ni balayés par une recherche) ; il n'a lu ni produit aucun journal réel : tous
les journaux lus ou produits sont des fixtures de tests ou des journaux écrits par ses sondes. »

Expositions et écarts, déclarés :
1. **Valeurs de campagne publiées** : trois lectures ciblées de `docs/11-mesures-pilotes.md` (l.382-390, 636-646,
   890-904, constats (a) et (b) du rédacteur, origine de SHOGEN-BLOC5-LIBELLE-1 et SHOGEN-RT-ETIQUETTE-INCLUSE-1) et
   une sortie de `grep` sur ce fichier ont affiché des valeurs de campagne publiées (n, K, P̂_more, z et z_bloc de la
   variante incluse ; z_bloc arrondis du J14 principal). Lecture postérieure à l'exécution unique, sur le rapport
   validé et versé ; `docs/11` n'est pas une pièce de D.2 ; aucune de ces valeurs n'entre dans le code ni dans les
   tests du lot.
2. **Variable scellée posée sur un chemin fictif**, sur instruction explicite de l'orchestrateur pour
   SHOGEN-TEST-ENV-HERMETIQUE-1 (« rouge avant (variable posée sur un chemin fictif) ») : valeur
   `B1/fictif/inexistant/control.jsonl`, absente avant et après chaque exécution (contrôlé par `test -e`) ; aucune copie
   scellée à portée ; détail au §10 et écart E-13. Toutes les autres exécutions Python sous
   `env -u SHOGEN_S2_CAMPAGNE_CONTROL PYTHONDONTWRITEBYTECODE=1 python3 -B`.

## 2. Sources lues (niveaux)

Toutes [lu], lignes indiquées ; une seule de seconde main, signalée.
- Contrat et registre : G0-lots-DETTES (entier) ; ETAT-REGISTRE (lignes ci-dessus) ; annexe B, B.1-B.2 (l.1-62), B.4
  (l.70-81), B.9 (l.167-175), B.12-B.13 (l.203-226), B.43-B.46 (l.601-687) ; G0-lot-D8a l.395-474 ; G1-lot-D8a l.8,
  l.42, l.285-300 ; annexe D, D.2 (l.32-47) et D.4 (l.124-167) ; paquet scellé `PAQUET-PREREG-S2.md` §4 (l.54-59),
  §6-§7 (l.67-85), §10.2 pts 1-11 (l.116-134), bloc machine (clés `commit_analyse`, `sha256_script`).
- Origines des items : `docs/G1-lot-CORR.md` l.1-40 et l.160-284 (L-1, L-2, L-5, D-1 à D-8) ; `docs/11-mesures-pilotes.md`
  l.382-390, 636-646, 890-904 ; `docs/G1-rapport-docs11.md` (lignes 50, 70-73, 125, par `grep`) ;
  `docs/G1-lot-B-sensibilite.md` l.191, l.200 et `docs/G1-lot-POOLEE-strate-poolee.md` l.6-17, 77, 176, 186, 210
  (par `grep`). [2nd] : « trois z » d'ADR-0025 déc. 4, cité par le journal G1 du lot B (l.200) ; ADR-0025 n'est pas lue
  (exclue de la copie).
- Session : `docs/PASSATION-CLOUD.md` (entier), `.claude/agents/shogen-worker.md`, `CLAUDE.md`.
- Outils de contrôle : `scripts/controle/README.md`, `regle_fixtures.py`, `render_fixture.py`, `SHA256SUMS` (sha256 des
  deux scripts recalculés : `5557fb56…`, `4084c42b…`, égaux à `SHA256SUMS`).
- Code : `s2-harness/shogen_s2/r1.py` (entier), `r2.py` (l.381-401, 425-604, 700-1098), `report.py` (entier),
  `records.py` (l.80-120), `lm.py` (imports et l.226, par `grep`), `collector.py` (l.215, par `grep`) ;
  `s2-harness/tools/rendu_unique.py` et `oracle_record.py` (entiers) ; `.github/workflows/gates.yml` (entier) ;
  `enforcement/tests/run-fixtures-model-pinning.sh` (l.1-40 et fin), `enforcement/gate-secrets.sh` (l.1-61),
  `enforcement/hooks/pre-commit` (motif R-13, par `grep`) ; `xtask/src/*.rs` (références aux workflows, par `grep`).
- Tests : `tests/__init__.py`, `test_prix_non_fini.py` (entier), `test_r2.py` (l.78-85, 280-412), `test_bloc1.py`
  (l.1-80, 191-218), `test_hote_deux_flux.py` (entier), `test_rendu_production.py` (l.1-125, 179-206),
  `test_recalcul_json_copie.py` (l.50-91), `test_oracle_record.py` (l.1-140), `test_exclusion.py` (l.28-46,
  259-300), `test_pool_analyse.py` (l.30-44) ; `s2-harness/README.md` (l.87-88, par `grep`).

## 3. Commandes et sorties (provenance)

Préfixe de toute exécution Python : `env -u SHOGEN_S2_CAMPAGNE_CONTROL PYTHONDONTWRITEBYTECODE=1 python3 -B` (Python
3.11.15 du conteneur), sauf les exécutions à variable fictive du §10. Sorties conservées dans `B1/journal/`,
`B1/sondes/`, `B1/mutants/`, `B1/nonreg/` ; outils dans `B1/outils/` (`nouvel-arbre.sh`, `mkdiff.sh`, `mutants.py`,
`mutants_verdict.py`, `longueurs.py`, `r25.py`, `secrets-fichiers.sh`, `verif-serie.sh`).

| heure (Z) | commande | sortie |
|---|---|---|
| 03:57:56 | `sha256sum` du brief ; `date -u` | `294c291d…641ee` ; horloge |
| 03:58 | `git rev-parse` / `status --short` / `log --oneline -5` (lecture) | `partie-4-execution`, `5afbdd2`, arbre propre |
| 04:00 | suite de base sur `B1/arbre/s2-harness` | `Ran 398 tests in 65.310s` `OK (skipped=2)` |
| 04:00:42 | `regle_fixtures.py` et `render_fixture.py` sur la base | `ea3a2d94…` ; `4e62fbb8…`, `d079dd9d…` (égaux au brief) |
| 04:18 | suite -v de base (`nonreg/base/suite-v.log`) | deux lignes « skipped '…SHOGEN_S2_CAMPAGNE_CONTROL…' » ; fin : tirets, `Ran 398`, `OK (skipped=2)` |
| 04:20:47 | `sondes/sonde_prix.py` sur la base (`sondes/sonde_prix-base.out`) | voir §4 |
| 04:38:57 | `sondes/sonde_rt.py` sur la base (`sondes/sonde_rt-base.out`) | voir §7 et §8 |
| 04:53 | `sondes/sonde_env.py`, sans puis avec variable fictive | voir §10 |
| 05:20 → | `sondes/rejeux_ci.py` sur copies de la vraie suite (`sondes/rejeux_ci.out`) | voir §9 |
| 05:23:09 → | `outils/verif-serie.sh` sur `B1/serie` (`journal/verif-serie.log`) | voir §11 |
| 05:25 | `sondes/sonde_entier_long.out`, `sondes/sonde_exposant_extreme.out` | voir §13 et §14 |

Les journaux rouges et verts de chaque sous-lot sont aux §4 à §10 (`journal/<k>-*.log`). Les longueurs de ligne des
fichiers touchés sont contrôlées par `outils/longueurs.py` (120 caractères au plus pour les lignes ajoutées ; les
lignes de la base plus longues, l.6 de `test_r2.py` et l.506 de `r2.py`, ne sont pas touchées).

## 4. Sous-lot 1 — SHOGEN-PRIX-ILLISIBLE-1 et SHOGEN-PRIX-HORS-CONTEXTE-1 (`b1-1-prix.diff`)

**Sonde de la base** (fixture du lot CORR-2 : collecteur réel, cinq flux, prix de la lecture ok rang 10 / bitfinex
remplacé ; `sondes/sonde_prix-base.out`) : « abc » et « » → `decimal.InvalidOperation` dans `r1._classify_window`
(compréhension `resp_price`) ; `[1]` → `ValueError` au même point ; `"1E+1000000"` et `"-1E+1000000"` →
`decimal.Overflow` dans `r1.classify_ecart` ; booléen JSON `true` → **aucune exception, lu comme le prix 1** (classé
hors-enveloppe : valeur fausse silencieuse) ; « 1E+999999 » (exposant ajusté = Emax), « 1E-999999 », « 1E-1000000 »,
« 1E-2000000 », « 0E+2000000 » → aucune exception, classés comme le prix qu'ils sont ; prix ordinaire → inchangé. Les
deux mêmes résultats par `r1.recompute_from_journal` et `report.render_report`.

**Construction** (`r1.py`, +29 −10 ; tests +56 −5) : deux erreurs nommées, `r1.PrixIllisible` et `r1.PrixHorsContexte` (sous-classes
de `ValueError`), levées au point unique des lectures, `r1.parse_journal`, sous le contexte nommé, quel que soit le
statut, valeur jamais reproduite (message : item, chemin, `flux_id`, `window_start`) : prix ni chaîne ni nombre JSON
(booléen, liste, objet ; `float` admis pour les jetons `NaN` et `Infinity`, que `parse_float` ne lit pas) ou chaîne
que `Decimal` ne lit pas → `PrixIllisible` ; prix fini non nul d'exposant ajusté > `Emax` (999999) du contexte nommé →
`PrixHorsContexte` ; prix non fini → absent, compté (règle de CORR-2, inchangée) ; tout autre prix fini : inchangé. Le
message n'est mis en forme qu'au refus.

**Tests d'abord** (`tests/test_prix_non_fini.py`) :
- `test_illisible_ou_hors_contexte_refus_nomme` (neuf) : onze formes refusées (« abc », « », « 1,5 », `[1]`,
  `[0, [1], 0]`, `{}`, `true`, `false` ; `"1E+1000000"`, `"-1E+1000000"`, jeton `1E+1000000`), lecture ok et en
  panne, classe et message exacts ; cinq bornes inchangées sans avertissement (`"1E+999999"`, `"-9.5E+999999"`,
  « 0E+2000000 », « 1E-1000000 », jeton `1E+999999`). Attendus écrits à la main depuis la sémantique de `Decimal`
  (Emin = −999999, Emax = 999999).
- `test_recalcul_et_rendu_refus_nomme_au_lecteur` (neuf) : fixture de la classe, « abc » et « 1E+1000000 » →
  `(PrixIllisible|PrixHorsContexte, parse_journal)` depuis `recompute_from_journal` et `render_report` (dernier cadre
  lu par `try/except` : `assertRaises` retire la pile de l'exception qu'il garde).
- `test_formes_lues_comme_absentes_ou_inchangees` (existant) : « abc » et `[1]` retirés de la liste « inchangés »
  (ils sont désormais refusés), docstring mise à jour ; `setUpClass` garde `cls.src`.

**Rouge avant** (`journal/1-prix-rouge.log`, 04:23:56Z) : `Ran 5 tests`, `FAILED (failures=26)`, 0 erreur : 22
« ValueError not raised », et `('InvalidOperation', '<dictcomp>') != ('PrixIllisible', 'parse_journal')`,
`('Overflow', 'classify_ecart') != ('PrixHorsContexte', 'parse_journal')` (deux fois chacun). Première rédaction :
deux erreurs de structure du test (assertions hors du `subTest`, pile vide), corrigées avant toute correction du code.
**Vert après** : module `OK` ; suite de l'arbre `Ran 400 tests` `OK (skipped=2)` ; `regle_fixtures.py` `ea3a2d94…` ;
épingles inchangées ; sonde rejouée (`sondes/sonde_prix-1-prix.out`) : refus nommés au lecteur, bornes et prix
ordinaire identiques à la base. Premier essai de la correction : le test CORR-2 rougit sur les jetons `NaN` (lus en
`float`) ; `float` ajouté aux types admis. Relecture : l'assertion « valeur absente du message » portait sur un message
qui contient le chemin temporaire (suffixe aléatoire : « abc » pouvait y paraître, ≈ 10⁻⁴ par exécution) ; chemin
retiré avant la comparaison.

## 5. Sous-lot 2 — SHOGEN-ASN-DIVERGENCE-PARTIELLE-1 (`b1-2-asn.diff`)

**Construction** (`r2.compute_partition`, +18 −13 ; tests +30 −6) : comparaison base par base des valeurs non muettes ; la référence
de chaque base (RIPEstat, Cymru) est son dernier relevé ok où elle n'est pas muette ; un relevé ok dont une base non
muette diffère de sa référence publie une divergence par relevé de référence distinct (`avant`, `après` : relevés
entiers, format inchangé) ; un échec n'est ni divergence ni référence (SHOGEN-ASN-DIVERGENCE-ECHEC-1, inchangé) ;
`by_host` (k_eff) inchangé. Pour une suite de relevés complets, la sortie est celle du lot CORR (tests existants
inchangés dans leurs assertions ; deux docstrings mises à jour, qui énonçaient qu'une base muette n'est jamais une
référence).

**Test d'abord** : `test_r2.TestAsnPartition.test_base_muette_changement_visible_publie_une_fois` (neuf ; attendus à
la main) : (RIPEstat, Cymru), « − » = base muette : h0 (1,1) → (−,2) → (1,2) : une divergence, au relevé partiel ; h1
(3,3) → (4,−) ; h2 (5,5) → (−,5) → (6,6) :
deux entrées, une par relevé de référence ; h3 bases disjointes : aucune ; h4 à travers un échec. **Rouge avant**
(`journal/2-asn-rouge.log`) : la base publie h0 au seul relevé complet (t = 3.0) et manque h1, h4 et la seconde
entrée de h2. **Vert après** : `test_r2` `Ran 46` `OK` ; suite `Ran 399` `OK (skipped=2)` ; règle et épingles
inchangées.

## 6. Sous-lot 3 — SHOGEN-BLOC5-LIBELLE-1 et SHOGEN-KEFF-NOTE-1 (`b1-3-libelles.diff`)

**Constructions** : bloc 5 (d) (`report.py`), « aucun cluster à ≥ 2 flux (n) » devient « moins de deux clusters à ≥ 2
flux (n) : aucune paire de clusters → tout reste au φ par paire de flux (bloc 4) » (branche atteinte ssi
`n_multi_clusters` < 2) ; note k_eff (`r2.py` l.885), « (aucun enregistrement asn_attribution) » devient « (aucun
enregistrement asn_attribution retenu) », texte de l'item, aligné sur la ligne (a) du bloc 5.

**Tests d'abord** : `test_hote_deux_flux.test_bloc5_d_un_seul_cluster_a_deux_flux` (neuf ; fixture `journal4`, un AS
par hôte : www.okx.com porte deux flux, `n_multi_clusters` = 1 écrit à la main) ;
`test_bloc1.TestBloc1.test_note_keff_aucune_sonde_retenue` (neuf ; fixture de
`test_bloc5_sondes_toutes_retirees_message_vrai`, filtre qui retire les 5·H sondes, puis journal sans sonde). **Rouge
avant** (`journal/3-libelles-rouge.log`) : 2 FAIL. **Vert après** ; la suite rougit alors sur les deux épingles seules
(`journal/3-libelles-suite-avant-repin.log` : `test_iv_sans_option_octets_d_avant_le_lot`,
`test_epingle_sans_flux_mort_octets_de_base_avec_option`).

**Ré-épinglage** (tolérance du brief : libellés corrigés ; seules les lignes des items changent) : diff textuel des
rendus de `render_fixture.py`, base contre arbre (`nonreg/base/rendu`, `nonreg/3-libelles/rendu`) : sans option,
l.197 (bloc 5 (d)) et l.210 (note k_eff du bloc 6) ; avec option, l.192 et l.205 ; aucune autre ligne. Épingles :
`SHA_BASE_SANS_OPTION` `4e62fbb8…93c9a01` → `57a72f7f830a516344c636eb9fa762a4e7bc00f6d80a63e75b836e897011e686` ;
`SHA_BASE_AVEC_OPTION` `d079dd9d…12de608` → `f53fab05af0b8f4da0f4918a9d404f23faa7f4882a1213c3c9def908a3c694c6`
(historique des commentaires prolongé). Suite `Ran 400` `OK (skipped=2)` ; règle `ea3a2d94…` inchangée.

## 7. Sous-lot 4 — SHOGEN-RT-ETIQUETTE-INCLUSE-1 (`b1-4-rt.diff`)

**Sonde de la base** (`sondes/sonde_rt-base.out`) : dans le JSON du recalcul tiers, `r1_discrimine` n'apparaît qu'en
`<entrée>.r2.drapeau_2` (avec `rejette`, `etat`, `raison`) ; la strate poolée de chaque entrée porte sa propre clé
`etiquette`. **Construction** (`tools/rendu_unique.py`, +2 ; tests +27 −7) : le `drapeau_2` de chaque variante incluse reçoit
`etiquette` = l'étiquette de la variante (`INCLUSE`), même motif que `r1.poolee.etiquette` ; aucune autre entrée n'en
reçoit ; valeur de `r1_discrimine` inchangée. **Tests** : `test_rendu_production.test_r1_discrimine_de_la_variante_
incluse_etiquete` (neuf ; texte de l'étiquette écrit à la main) ; attendus de deux tests existants ajustés pour la
seule variante incluse (`test_recalcul_tiers_quatre_recompute_et_variante_incluse`,
`test_recalcul_json_copie.test_recalcul_tiers_paire_copie_en_liste_triee`). **Rouge avant**
(`journal/4-rt-rouge.log`) : 2 FAIL. **Vert après** : module `Ran 16` `OK` ; suite `Ran 399` `OK (skipped=2)` après
l'ajustement du second test existant (`journal/4-rt-suite1.log` montre le rouge qui l'a révélé). Le sha256 du script
passe de `06d189cf…` (égal à `sha256_script` du bloc machine scellé) à `5ee95dbf…` : écart E-8.

## 8. Sous-lot 5 — SHOGEN-SENS-POOLEE-1 : décision écrite (`b1-5-sens-poolee.diff`, test seul)

**Décision proposée** (re-ciblage tranché ; propriétaire de l'item : l'orchestrateur, qui adjuge) : l'item se ferme
**sans ligne ajoutée** à la section `[SENSIBILITÉ]` du rendu. Motifs :
1. **Forme scellée** : le paquet fixe la liste fermée des sensibilités (§7 : plage ADR-0025 exclue ou incluse ;
   seconde coupe J14 ; « toute autre analyse est exploratoire ») et le lieu de « plage incluse » (section
   `[SENSIBILITÉ]` du rendu J28) ; la strate poolée y est exploratoire, hors famille, hors décision, imprimée au bloc 3
   (§4, §10.2 pt 9). La ligne demandée croiserait une analyse exploratoire et une sensibilité de la liste fermée,
   combinaison que le texte scellé ne liste pas ; l'exécution unique étant faite, elle ne serait plus qu'« ajoutée
   après le pré-enregistrement » (classe C, POST-PREREG).
2. **Information déjà publiée** : le JSON du recalcul tiers porte la strate poolée des deux variantes du J28
   (`j28.r1.poolee`, `j28-incluse.r1.poolee` : strates, numérateur, variance, `z_pool` ou motif), étiquetée
   « exploratoire, hors famille, hors décision » (et, pour la variante incluse, par l'étiquette d'entrée et, depuis le
   sous-lot 4, celle du drapeau 2) ; aucun nombre neuf ne serait produit.
3. **Épingle** : la fixture épinglée a deux strates et une plage ; la construction changerait `d079dd9d…` pour une
   raison qui n'est pas un libellé corrigé, hors de la tolérance du brief.
4. **Prémisse figée** : `test_rendu_production.test_poolee_des_deux_variantes_du_j28_dans_le_recalcul_tiers` (neuf) :
   poolée présente dans `j28` et `j28-incluse`, étiquette écrite à la main, égale à `recompute_from_journal` sous les
   options de la variante, différente entre les deux variantes. Test de caractérisation : vert sur la base (aucun code
   changé) ; sa force est montrée par trois mutants tués (§12).
Si l'orchestrateur préfère construire : ≈ 25 lignes (B.12), une re-capture de `d079dd9d…` hors de la tolérance du
brief, et une sortie sur journaux réels de classe C.

## 9. Sous-lot 6 — SHOGEN-CI-S2-SAUT-1, sous-lot D8a-3 (`b1-6-ci.diff`)

**Choix du G0 (plancher, et non manifeste)** : plancher committé `PLANCHER = 398` (compte de la suite à `5afbdd2`),
« Ran N ≥ plancher », sans égalité figée. Motifs : il refuse les deux pertes mesurées par le lot CI-S2 (MT-5 module
renommé, MT-6 retrait partiel), alors qu'un manifeste de modules ne voit pas un retrait partiel dans un module
conservé ; un seul entier, aucun couplage aux noms des modules ni au test de comptes de B-SEG-1 ; ajouter des tests
ne casse jamais le job. Limite : après une croissance de N, un retrait de N − plancher tests passe ; relever le
plancher à chaque lot qui ajoute des tests (L-4, Q-3). 398 et non 405 (compte après la série) : le sous-lot reste
applicable seul.

**Construction** : `enforcement/verdict-suite-s2.py` (neuf, bibliothèque standard) : lance la suite
(`python3 -B -m unittest discover -s tests -t . -v`), variable scellée retirée de l'environnement de la suite, recopie
sa sortie, puis exige : code 0 ; en fin du flux de unittest (stderr), tirets, `Ran N tests in …s`, ligne vide, `OK` ou
`OK (skipped=k)` ; exactement k lignes « … skipped '<motif>' », chaque motif nommant `SHOGEN_S2_CAMPAGNE_CONTROL` ;
N ≥ 398 ; sorties 0 conforme, 1 refus (motifs sur stderr), 3 erreur. `enforcement/tests/run-fixtures-verdict-suite-
s2.py` (neuf) : 20 cas (V-01 à V-13 sur sorties écrites, E-01 à E-05 sur suites factices en dossiers temporaires,
C-01, C-02 par le point d'entrée sur une suite factice de 398 tests). `gates.yml`, job `s2-harness-unittest` seul :
étape des cas, puis la suite jugée par le vérificateur ; commentaires mis à jour (YAML relu par `yaml.safe_load`,
PyYAML présent dans le conteneur, non installé : trois étapes lues).

**Rouge avant** : lanceur de cas sans vérificateur → « ERREUR : vérificateur illisible », code 3. **Vert après** :
20 ok, 0 échec, en 1,1 s (Python 3.11.15). **Sous Python 3.12.3 et 3.13.14** (présents dans le conteneur ; 3.12 est
la version inférée de l'image du runner) : le cas E-04 d'origine rougissait, car une découverte vide sort en code 5
sans « OK » à partir de 3.12 (3.11 imprimait « Ran 0 … OK ») ; le vérificateur refusait dans les deux cas, mais le
cas attendait le motif du plancher et n'avait qu'un module. Cas corrigé, fidèle à MT-5 (un module renommé parmi
d'autres, plancher égal au compte sans renommage ; contrôle sans renommage : conforme sous 3.11 et 3.12) : 20 ok sous
3.11, 3.12 et 3.13. **Rejeux sur copies de la vraie suite** (`sondes/rejeux_ci.out`) : voir §11.

## 10. Sous-lot 7 — SHOGEN-TEST-ENV-HERMETIQUE-1 (`b1-7-env.diff`, item ajouté par l'orchestrateur)

**Cause** (`sondes/sonde_env.py`, dépôt jetable du test) : sans variable, l'enregistreur consigne
`SHOGEN_S2_CAMPAGNE_CONTROL: None` et `tests_avec_variable: []` ; avec la variable fictive, il consigne sa valeur et
`['tests.test_t.T.test_a']`, comme il le doit (annexe D.4 a) : c'est le test qui lit l'environnement ambiant
(`mock.patch.dict(os.environ, {"PYTHONHASHSEED": "17"})` ne retire pas une variable déjà posée). **Construction**
(test seul, `oracle_record.py` inchangé) : dans ce `patch.dict`, `os.environ.pop("SHOGEN_S2_CAMPAGNE_CONTROL", None)` ;
`patch.dict` rend `os.environ` intact à la sortie (contrôlé : variable fictive toujours posée après le test).

**Rouge avant / vert après** (variable fictive `B1/fictif/inexistant/control.jsonl`, absente avant et après) :
- base, module `test_oracle_record`, sans variable : `OK` ; avec variable fictive : `FAILED (failures=1)`
  (`test_enregistrement_champs_et_sha` ; `journal/7-env-rouge.log`) ;
- corrigé, avec et sans variable : `OK` ;
- suite entière avec variable fictive (`journal/7-env-suite-fictive-*.log`) : base `Ran 398` `FAILED (failures=1,
  errors=2)` (le test non hermétique, plus les deux tests nommés de `test_exclusion` en `FileNotFoundError` sur le
  chemin fictif, attendu : ils n'existent que pour la copie scellée) ; corrigé `Ran 398` `FAILED (errors=2)` (les deux
  tests nommés seuls) : aucun autre test ne dépend de la variable ambiante ;
- suite entière sans variable, corrigé : `Ran 398` `OK (skipped=2)`.
Avec la copie scellée, l'état attendu après correction est `Ran 398` `OK` (deux tests nommés exécutés), à rejouer par
l'orchestrateur (Q-8).

## 11. Série, rejeux du lot CI-S2, non-régression, xtask

**Application** : les sept diffs s'appliquent chacun seul sur une extraction neuve de `5afbdd2` (`git apply --check`,
puis arbre identique à l'arbre de développement), en série dans l'ordre 1 → 7, et en ordre inverse 7 → 1 (arbre final
identique dans les deux ordres) : ils sont indépendants. Aucun fichier `.orig` ni `.rej`.

**Rejeux du lot CI-S2 sur copies de la vraie suite** (`sondes/rejeux_ci.out`, `sondes/rejeux_ci-mt9.out` ; copie de
`s2-harness` avec ses voisins `enforcement`, `scripts`, `.github`) — verdict de la commande actuelle du job (code de
sortie seul) contre celui du vérificateur :

| rejeu | mutation de la suite | job actuel | vérificateur |
|---|---|---|---|
| témoin | aucune | VERT (code 0, Ran 398) | conforme |
| R8 | saut ajouté, motif « motif autre » | VERT (code 0, Ran 399) | refus : motif sans la variable |
| MT-5 | `test_window.py` renommé hors du motif | VERT (code 0, Ran 384) | refus : Ran 384 < 398 |
| MT-6 | dernière classe de `test_sources.py` retirée | VERT (code 0, Ran 391) | refus : Ran 391 < 398 |
| MT-7 | `@unittest.skip('décorateur')` | VERT (code 0, Ran 398) | refus : motif sans la variable |
| MT-9 | `os._exit(0)` dans un test | VERT (code 0, aucune ligne Ran) | refus : résumé final absent |

Les cinq pertes passent le job actuel et sont toutes refusées ; la suite réelle est conforme : c'est l'oracle de D8a-3
(G1-lot-D8a l.42). Le point d'entrée rend 1 exactement quand le verdict porte un refus (cas C-01, C-02, mutant MV-12).

**Arbre série** (copie complète de `B1/arbre`, sept diffs appliqués ; `outils/verif-serie.sh`,
`journal/verif-serie-final.log`, de 05:39:22Z à 05:46:07Z) :
- suite sans variable : `Ran 405 tests in 89.562s` `OK (skipped=2)` (398 + 7 tests neufs : 2 PRIX, 1 ASN, 2
  libellés, 1 RT, 1 poolée ; le sous-lot 7 n'en ajoute pas) ;
- cas du vérificateur : 20 ok, 0 échec, sous Python 3.11.15, 3.12.3 et 3.13.14 ;
- vérificateur sur la vraie suite : code 0, `conforme` (`Ran 405`, deux sauts nommant la variable), sous 3.11.15 et sous
  3.12.3 (`journal/serie-verdict*.out`) ;
- `regle_fixtures.py` : `ea3a2d94ef1075603e8f7cfc53c68b26e51729b61714028e3fb03dc32f79cb29`, sortie imprimée identique
  à celle de la base (`cmp`) ;
- `render_fixture.py` : `57a72f7f…`, `f53fab05…` (épingles re-capturées au §6) ;
- `cargo --locked xtask verify` : code 0, `VERDICT GLOBAL : VERT`, huit gates vertes (S-G1 à S-G8 ;
  `journal/serie-xtask.log`) ; S-G5 en régime partiel (corpus = INDEX seul, 0 artefact sur 128 déclarés : 303
  fragments contrôlés, 268 non contrôlés ici) ; le lot ne touche aucun fichier `.md` du périmètre de S-G4 et S-G5 ;
  rapport identique à celui de `xtask verify` sur la base intacte (`journal/base-xtask.log`, hors chemins et lignes
  de compilation) ;
- 0 `__pycache__` ; R-13 (motif du job g5) : aucun marqueur dans les 16 fichiers touchés ; motifs `VENDOR` et
  `GENERIC` de la gate des secrets, lus dans le script, appliqués aux 16 fichiers (`outils/secrets-fichiers.sh`, sans
  dépôt git) : aucun constat ; fins de ligne LF, sans BOM ; extraction du motif g5 par le cas H-20 du lanceur des
  hooks : identique entre base et série (ma retouche de `gates.yml` ne touche pas le job g5).

## 12. Mutants (récapitulatif)

Méthode : copie neuve par mutant (`s2-harness` et `enforcement` voisins), une substitution (motif présent une seule
fois), modules de test nommés ; témoin non muté exigé vert d'abord ; mort = code ≠ 0. Résultats JSON dans
`B1/mutants/*-res.json`. Une première série a été écartée (E-17).

| sous-lot | mutants | témoin | tués | tués par un test neuf |
|---|---|---|---|---|
| 1 PRIX | P-M1 illisible inchangé ; M2 booléen lu ; M3 liste lue comme triplet ; M4 borne ≥ Emax ; M5 zéro refusé ; M6 valeur dans le message ; M7 hors contexte non contrôlé au lecteur ; M8 refus limité aux lectures ok ; M9 classes permutées ; M10 jetons NaN/Infinity refusés | passe | 10/10 | M1-M9 (M10 : test CORR-2 existant) |
| 2 ASN | A-M1 relevé partiel ignoré ; M2 référence non mise à jour par un partiel ; M3 une entrée par relevé ; M4 référence unique par hôte ; M5 dédoublonnage par valeur | passe | 5/5 | 5/5 (M4 survit aux tests existants) |
| 3 libellés | L-M1 libellé (d) d'origine ; M2 compte = paires de clusters ; M3 note d'origine ; M4 note « au journal » | passe | 4/4 | 4/4 (M2 invisible aux épingles) |
| 4 RT | R-M1 étiquette absente ; M2 sur toutes les entrées ; M3 texte autre ; M4 étiquette dans la valeur ; M5 au niveau de r2 | passe | 5/5 | 5/5 |
| 5 poolée | S-M1 poolée retirée de la variante incluse ; M2 étiquette de la poolée autre ; M3 variante incluse sous la plage | passe | 3/3 | 3/3 |
| 6 CI | MV-1 code ignoré ; 2 résumé absent admis ; 3 motif non contrôlé ; 4 plancher absent ; 5 égalité figée ; 6 compte des sauts ; 7 autre statut OK ; 8 résumé hors fin de flux ; 9 guillemets doubles ; 10 variable laissée ; 11 sans -v ; 12 point d'entrée ignore les refus ; 13 tout saut refusé ; 14 « OK » sans saut refusé ; 15 plancher strict | passe | 15/15 | chacun des 20 cas tue au moins un mutant |
| 7 env | E-M0 retrait de la variable supprimé (test) ; E-M1 `tests_avec_variable` toujours rempli ; E-M2 variable consignée par défaut | passe (sans et avec variable fictive) | sans variable : 2/3 (E-M0 survit : retrait sans objet) ; avec : 3/3 | E-M0 tué sous la variable : c'est la ligne ajoutée qui rend le test hermétique ; sur la base, le témoin échoue sous la variable (le test d'origine ne discriminait plus rien) |

## 13. Écarts et interprétations

- **E-1 (PRIX, types JSON)** : « illisible » lu au sens JSON : booléen, liste, objet refusés, bien que `Decimal` lise
  `true`/`false` comme 1/0 et une liste de trois éléments comme un triplet (valeurs fausses silencieuses à la base,
  mesurées : `true` lu comme le prix 1). Serrage déclaré (Q-1).
- **E-2 (PRIX, portée)** : refus quel que soit le statut et la fenêtre (fichier entier, point unique), comme la règle de
  CORR-2 (D-1, D-3 de son G1) : plus strict que la base pour une lecture que l'analyse n'aurait pas utilisée (non ok,
  hors segment ou plage) ; effet sur les journaux réels non mesurable (interdits) ; le collecteur n'écrit que
  `str(Decimal)` ou `null` [inféré, G1 du lot CORR L-1].
- **E-3 (PRIX, borne)** : borne Emax seule (portée de l'item) ; sous Emin, aucune exception et un classement juste
  (sonde) : pas de refus. Exposant au-delà de la limite de l'implémentation (`MAX_EMAX` = 999999999999999999) :
  `Decimal` ne lit pas la chaîne, donc `PrixIllisible` ; exposant égal à `MAX_EMAX` : `PrixHorsContexte`
  (`sondes/sonde_exposant_extreme.out`).
- **E-4 (ASN)** : `avant` = relevé de référence de la base changée, tel qu'enregistré (éventuellement partiel) ; deux
  entrées quand deux bases changent depuis deux relevés de référence distincts.
- **E-5 (épingles)** : re-capture dans la tolérance du brief, diff textuel au §6 (deux lignes par rendu, celles des
  items).
- **E-6 (BLOC5)** : libellé unique, juste pour n = 0 comme pour n = 1 (il change aussi la ligne n = 0 épinglée), plutôt
  qu'une branche pour n = 1.
- **E-7 (RT, forme)** : étiquette au niveau de l'objet `drapeau_2` (clé `etiquette`), et non dans la valeur ni dans le
  nom de la clé : domaine de valeur et schéma conservés ; la ligne `"r1_discrimine": …` seule ne porte toujours pas
  l'étiquette (clé voisine du même objet ; au JSON trié, `etiquette` précède `r1_discrimine`) ; les deux autres formes
  sont possibles sur décision (Q-5).
- **E-8 (RT, script scellé)** : `rendu_unique.py` change (sha256 `06d189cf…` → `5ee95dbf…`) ; avec les sous-lots 1 à 3
  (`shogen_s2`), les gardes (2) et (4) refuseraient une ré-exécution à la tête : toute ré-exécution du rendu (déviation
  déclarée, ou SHOGEN-REJEU-HOTE-1) se fait au commit d'analyse `f35a70c`, jamais à la tête (G0-lots-DETTES l.6-7 :
  la garde (2) ne s'applique plus aux changements postérieurs).
- **E-9 (SENS-POOLEE)** : fermeture par décision, sans code, test de caractérisation sans rouge avant (§8).
- **E-10 (CI, plancher)** : 398 et non 405 (§9) ; à relever au commit de la série (Q-3).
- **E-11 (CI, flux jugé)** : seul le flux de unittest (stderr) est jugé ; la sortie standard des tests est recopiée
  après lui ; une ligne non vide après le résumé sur stderr fait refuser (refus possible à tort si un test écrivait sur
  stderr à la fin de l'interpréteur ; aucun aujourd'hui).
- **E-12 (CI, commentaires)** : dans l'étape touchée, « le test (ii) … seul lecteur » devient « les deux tests nommés …
  (annexe D.4 a) » ; mesure de durée datée ajoutée au commentaire du délai.
- **E-13 (variable fictive)** : contradiction littérale avec la règle 3 de la fiche (« tu ne poses jamais
  SHOGEN_S2_CAMPAGNE_CONTROL »), levée par l'instruction explicite de l'orchestrateur pour cet item ; valeur fictive,
  absente, aucune copie scellée lue ; exécutions : module `test_oracle_record` (base et corrigé), deux suites entières
  (§10), mutants E-M0 à E-M2 ; ailleurs, variable retirée par nom.
- **E-14 (PyYAML)** : présent dans le conteneur, employé seulement pour relire `gates.yml` ; aucune installation (R-8).
- **E-15 (TMP)** : mes premiers scripts créaient leurs temporaires sous `/tmp` ; un résidu (`/tmp/rejeu_odop5asc`,
  d'une exécution interrompue) a été retiré ; ensuite `TMPDIR` dans `B1/tmp`. Les autres entrées de `/tmp` créées
  pendant la passe (`pp_*`, `shogen-mutant-sg9-*`, etc.) ne sont pas de ce worker : non touchées. La suite elle-même
  range ses temporaires sous un dossier retiré à la sortie (SHOGEN-TESTS-TMP-1).
- **E-16 (incident)** : un `pkill -f` visant mon script de rejeux a aussi interrompu ma propre commande (motif dans sa
  ligne de commande) ; sans effet hors de `B1/` ; rejeux relancés.
- **E-17 (mutants et rejeux)** : une première série de mutants copiait `s2-harness` seul (tests de l'enregistreur en
  erreur faute de `../enforcement`) et n'avait pas de témoin ; toutes les tables ont été rejouées avec témoin et
  voisins ; deux mutants mal écrits (A-M4 d'abord sans référence du tout, MV-2 d'abord équivalent au code) ont été
  réécrits avant la série de référence. Les rejeux ont connu les mêmes défauts : copie sans voisins (témoin rouge),
  puis une mutation MT-9 mal formée (`import os` placé avant `from __future__`, donc erreur d'import et code 1) ;
  séries de référence : `sondes/rejeux_ci.out` (témoin à MT-7) et `sondes/rejeux_ci-mt9.out`.
- **E-18 (README)** : le compte « Ran 307 » de `s2-harness/README.md` l.87 n'est pas touché (SHOGEN-DOC-HARNAIS-2,
  lot DETTES-A) ; compte après la série : 405 (Q-7).
- **E-19 (tête mouvante)** : constat de fin de passe (05:49Z, `git status`, `git log` en lecture) : la tête du dépôt est
  passée de `5afbdd2` à `3e275a2` (sept commits de l'orchestrateur, dont `a28dd9e`, qui forme l'item de l'environnement
  et `4c46d9a`, lot DETTES-BIBLIO), et l'arbre porte des fichiers modifiés ou non suivis
  (`scripts/controle/SHA256SUMS`, `docs/adr-0029/…`, `scripts/controle/sorties-fm11/etude-*.json`) : aucun n'est de ce
  worker. `git diff --name-only 5afbdd2 3e275a2 -- s2-harness enforcement .github` est vide ; les sept diffs
  s'appliquent aussi sur une extraction de `3e275a2` (`git archive`) et y donnent les mêmes arbres que la série
  vérifiée.

## 14. Limites rendues comme items (règle PAROXYSME ; propositions, propriétaire : orchestrateur)

- **SHOGEN-PRIX-ARITH-RESIDU-1** : dépassement `Decimal` non nommé encore possible par combinaison de prix dans la plage
  du contexte : somme de deux prix ≥ 5E+999999 à la médiane paire (`r1._median`) ; rapport |p − m|/m ≥ 1E+1000000
  sous une médiane minuscule (`classify_ecart`, `_ecart_relatif`). Plausibilité nulle (au moins deux prix absurdes dans
  une fenêtre) [inféré]. Construction possible : plage de plausibilité des prix (choix de conception) ou capture nommée
  en ces deux points. Déclencheur : prochain lot qui touche `r1.py`.
- **SHOGEN-JSON-ENTIER-LONG-1** : un entier JSON de plus de 4300 chiffres (`sys.get_int_max_str_digits()` de Python ≥
  3.11) dans `journal.jsonl` ou `control.jsonl` lève un `ValueError` générique du décodeur dans
  `records.read_jsonl_tolerant`, même en dernière ligne (hors de la tolérance « ligne tronquée ») ; mesuré
  (`sondes/sonde_entier_long.out`, 5001 chiffres). Inatteignable depuis le collecteur [inféré : prix écrits en
  chaînes]. Construction possible : refus nommé au lecteur. Déclencheur : prochain lot qui touche `records.py`.
- **SHOGEN-RT-ETIQUETTE-J14-1** (à trancher) : `r1_discrimine` des entrées J14 du JSON du recalcul tiers (hors décision,
  §10.2 pt 9) étiqueté au seul niveau de l'entrée, comme leurs rendus texte par la ligne `[ÉTIQUETTE]` ; même forme que
  la variante incluse avant le sous-lot 4. Hors de l'item ; décision : pt 9 tenu au niveau de l'entrée, ou même
  construction (deux lignes).
- **SHOGEN-CI-PLANCHER-SUIVI-1** : le plancher ne suit pas la croissance de N (un retrait de N − plancher tests passe) ;
  construction : règle écrite « tout lot qui ajoute des tests relève le plancher au compte mesuré » (annexe A ou
  RUNBOOK §9), ou manifeste des modules en plus. Déclencheur : prochain lot qui ajoute des tests.
- Premier passage des deux étapes neuves sur la forge : relève de SHOGEN-CI-S2-FORGE-1 (déjà formé ; le vérificateur
  n'emploie que la bibliothèque standard, `subprocess.run(capture_output=…)`, Python ≥ 3.7).

## 15. Questions à l'orchestrateur

- **Q-1** : accepter E-1 (booléens, listes, objets refusés comme illisibles) ou s'en tenir à « illisible par
  `Decimal` » (une ligne à retirer) ?
- **Q-2** : adopter la décision du §8 (SENS-POOLEE-1 fermé sans ligne ajoutée) ou construire (re-capture de `d079dd9d…`
  hors tolérance du brief) ?
- **Q-3** : relever `PLANCHER` à 405 au commit de la série (une ligne de `enforcement/verdict-suite-s2.py`) ?
- **Q-4** : amender la liste des commandes du G3 opérant local (ADR-0028 §4.11 l.171) avec
  `python3 -B enforcement/tests/run-fixtures-verdict-suite-s2.py` et `python3 -B enforcement/verdict-suite-s2.py`
  (précédent : cp-1 C-5 de D8a) ?
- **Q-5** : forme de l'étiquette RT (E-7) : clé `etiquette` du drapeau 2 (livrée), étiquette dans la valeur, ou clé
  renommée ?
- **Q-6** : SHOGEN-RT-ETIQUETTE-J14-1 (§14) : former l'item ou décider que pt 9 est tenu ?
- **Q-7** : compte pour SHOGEN-DOC-HARNAIS-2 (DETTES-A) : 405 tests après la série (398 sans le lot).
- **Q-8** : rejouer la suite avec la copie scellée après le sous-lot 7 (attendu : `Ran 398`, ou 405 avec la série,
  `OK`, sans saut) ?

## 16. Lignes proposées pour l'annexe A (acte de l'orchestrateur)

| lot | objet | fichiers | oracle | taille (R-25) | tuyau |
|---|---|---|---|---|---|
| DETTES-B1-1 (2026-10-04) | SHOGEN-PRIX-ILLISIBLE-1, SHOGEN-PRIX-HORS-CONTEXTE-1 : refus nommés au lecteur | `r1.py`, `tests/test_prix_non_fini.py` | 26 sous-tests rouges, 10 mutants | +85 −15 | `journal.jsonl` → `parse_journal` → R1, L&M, R2, rapport |
| DETTES-B1-2 | SHOGEN-ASN-DIVERGENCE-PARTIELLE-1 : comparaison base par base | `r2.py`, `tests/test_r2.py` | 1 test, 5 mutants | +48 −19 | `asn_attribution` → `compute_partition` → bloc 5 (a), JSON |
| DETTES-B1-3 | SHOGEN-BLOC5-LIBELLE-1, SHOGEN-KEFF-NOTE-1 ; épingles re-capturées | `report.py`, `r2.py`, quatre tests | 2 tests, 4 mutants, diff textuel | +36 −7 | `r2_out` → blocs 5 et 6 |
| DETTES-B1-4 | SHOGEN-RT-ETIQUETTE-INCLUSE-1 | `tools/rendu_unique.py`, deux tests | 1 test, 5 mutants | +29 −7 | recalcul-tiers → JSON → lecteur tiers |
| DETTES-B1-5 | SHOGEN-SENS-POOLEE-1 fermé par décision ; test de caractérisation | `tests/test_rendu_production.py` | 3 mutants | +15 −0 | JSON du recalcul tiers |
| **D8a-3** (DETTES-B1-6) | SHOGEN-CI-S2-SAUT-1 : verdict du job sur la sortie de la suite, plancher 398 | `enforcement/verdict-suite-s2.py`, `enforcement/tests/run-fixtures-verdict-suite-s2.py`, `gates.yml` | 20 cas (3.11, 3.12, 3.13), rejeux R8, MT-5, MT-6, MT-7, MT-9, 15 mutants | +183 −8 | suite unittest → vérificateur → job (G3 opérant local ; forge : SHOGEN-CI-S2-FORGE-1) |
| DETTES-B1-7 | SHOGEN-TEST-ENV-HERMETIQUE-1 | `tests/test_oracle_record.py` | rouge sous variable fictive, 3 mutants | +4 −1 | — |

## 17. Livrables (dossier `B1/livrables/`) et clôture

Diffs unifiés par sous-lot, applicables par `git apply` sur `5afbdd2`, chacun seul ou en série dans un ordre
quelconque (§11) ; sha256 au fichier `LIVRABLES.sha256` du même dossier (ce journal y figure ; il ne porte pas son
propre sha256) :

| diff | items | sha256 |
|---|---|---|
| `b1-1-prix.diff` | SHOGEN-PRIX-ILLISIBLE-1, SHOGEN-PRIX-HORS-CONTEXTE-1 | `ddfb5d0b643aa77fac874cab197c7951bf784d59206676e8f5512495c3b77e81` |
| `b1-2-asn.diff` | SHOGEN-ASN-DIVERGENCE-PARTIELLE-1 | `5e27a2880254fa9d8318cce3a03ac4245016b48d193edbd31ebfca2fe562ad7a` |
| `b1-3-libelles.diff` | SHOGEN-BLOC5-LIBELLE-1, SHOGEN-KEFF-NOTE-1 | `02b25b8beadee12f5c09e6856184cd13d1f060c84bdcb042799db7fdd669bac4` |
| `b1-4-rt.diff` | SHOGEN-RT-ETIQUETTE-INCLUSE-1 | `2220264e73c55c68e4502584460ac28ad9a2585379546ef44e80a98fe6498a52` |
| `b1-5-sens-poolee.diff` | SHOGEN-SENS-POOLEE-1 (décision, test) | `3be34e44db6c5892d560793d362e5f9b95534d6d754a009c5976b2ef4d03722e` |
| `b1-6-ci.diff` | SHOGEN-CI-S2-SAUT-1 (D8a-3) | `f0b2be51e2255c00e52c78406789bcefc5a7d5f47d5167f16ecab9a61a7d2790` |
| `b1-7-env.diff` | SHOGEN-TEST-ENV-HERMETIQUE-1 | `991678aed91afd5ab0b47393a6acdc42633e321e567f88683526da74ea7e6b13` |

Pièces de travail conservées (non livrées au dépôt) : `B1/outils/`, `B1/sondes/`, `B1/mutants/`, `B1/journal/`,
`B1/nonreg/`, arbres `B1/dev/` et `B1/serie/`.
