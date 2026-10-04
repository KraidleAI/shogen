# Relecture G2 du lot DETTES-B1 (harnais `s2-harness`, gate D8a-3)

- Réviseur : worker neuf, modèle `claude-opus-5-5`, effort `max` (Gate 0). Je n'ai rien écrit de ce lot.
- Horloge lue (`date -u`) à l'ouverture : 2026-10-04 05:50:58 UTC.
- Brief : `BRIEF-G2-DETTES-B1.md`, sha256 `e5a02393…30ff9f5` recompté, conforme.
- Dépôt : `/home/user/shogen`, branche `partie-4-execution`, tête `3e275a2b2466245375041612c6d83b9ef2aafc10`.
  Arbre de travail : `scripts/controle/SHA256SUMS` modifié et fichiers `docs/adr-0029/…`, `scripts/controle/sorties-fm11/etude-*`
  non suivis (hors lot) ; la relecture se fait sur une copie `git archive HEAD`, jamais sur l'arbre de travail.
- Pièces : `LIVRABLES.sha256` vérifié par `sha256sum -c` : 8/8 OK.

(rapport rédigé au fil de l'eau ; sections ajoutées dans l'ordre des contrôles)

## Contrôle (1) — application sur la tête actuelle `3e275a2`

Copie : `git archive HEAD | tar -x -C G2-B1/arbre --exclude=docs/rapports --exclude=docs/adr-0025
--exclude=docs/adr-0028/monark-m009a` (dossier hors de tout dépôt : `git rev-parse` y rend « not a git repository » ;
`git apply` n'y est qu'un outil de correctif). Aucun `*.jsonl` suivi à la tête (`git ls-files '*.jsonl'` : 0).
- Chaque diff seul sur une copie neuve (`G2-B1/seul/<k>`) : `git apply --check` puis `git apply` : 7/7 OK.
- Série 1 → 7 (`G2-B1/serie`) : 7/7 OK ; 0 `.orig`/`.rej` ; 16 fichiers touchés (14 modifiés, 2 neufs).
- Ordre inverse 7 → 1 : arbres `s2-harness`, `enforcement`, `.github` identiques à la série (indépendance).
- Les 16 fichiers de ma série sont identiques à l'octet (`cmp`) à ceux de l'arbre série du générateur (`DETTES-B1/serie`).
- Lignes recomptées (+ / −) : b1-1 +85 −15 ; b1-2 +48 −19 ; b1-3 +36 −7 ; b1-4 +29 −7 ; b1-5 +15 −0 ; b1-6 +183 −8 ;
  b1-7 +4 −1 (égales à la table §16 du G1).

## Contrôle (3) — règle et épingles

Outils de la tête : `regle_fixtures.py` sha256 `5557fb56…`, `render_fixture.py` `4084c42b…`, égaux à
`scripts/controle/SHA256SUMS` de la tête (le `SHA256SUMS` modifié de l'arbre de travail n'est pas employé).
- `regle_fixtures.py` sur la base, sur chaque diff seul et sur la série : JSON
  `ea3a2d94ef1075603e8f7cfc53c68b26e51729b61714028e3fb03dc32f79cb29` partout ; sortie imprimée identique (`cmp`) base/série.
- `render_fixture.py` : base et diffs seuls 1, 2, 4, 5, 6, 7 : `4e62fbb8…`, `d079dd9d…` (inchangés) ; diff 3 seul et série :
  `57a72f7f830a516344c636eb9fa762a4e7bc00f6d80a63e75b836e897011e686`,
  `f53fab05af0b8f4da0f4918a9d404f23faa7f4882a1213c3c9def908a3c694c6`, égaux aux épingles écrites par le diff 3.
- Diff textuel base → série (`diff`) : sans option, l.197 (bloc 5 (d)) et l.210 (note k_eff) ; avec option, l.192 et
  l.205 ; aucune autre ligne ; nombre de lignes inchangé (225 et 239). Ré-épinglage justifié par les seules lignes de
  SHOGEN-BLOC5-LIBELLE-1 et SHOGEN-KEFF-NOTE-1.

## Contrôle (4) — suite entière, sans et avec la variable sur un chemin fictif

Préfixe : `env -u SHOGEN_S2_CAMPAGNE_CONTROL PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s tests -t .`
(Python 3.11.15, `TMPDIR` dans mon dossier), lancé dans `s2-harness` de chaque copie.
- Sans variable : base `Ran 398 tests` `OK (skipped=2)` (sortie 0) ; série `Ran 405 tests` `OK (skipped=2)` (sortie 0) ;
  les deux sauts nomment la variable (« SHOGEN_S2_CAMPAGNE_CONTROL absente : copie du control.jsonl scellé non
  fournie… »). Différence des noms de tests base → série : 7 ajoutés, 0 retiré (2 PRIX, 1 ASN, 1 bloc 5 (d), 1 note
  k_eff, 1 RT, 1 poolée).
- Avec `SHOGEN_S2_CAMPAGNE_CONTROL=G2-B1/fictif/inexistant/control.jsonl` (chemin et dossiers parents absents avant et
  après, `test -e`) : base `Ran 398` `FAILED (failures=1, errors=2)` (FAIL `test_enregistrement_champs_et_sha`, le
  constat de l'item ; ERROR des deux tests nommés de D.4 a) ; diff 7 seul `Ran 398` `FAILED (errors=2)` ; série
  `Ran 405` `FAILED (errors=2)` : seuls les deux tests nommés, en `FileNotFoundError` sur le chemin fictif.
- Restauration : le test corrigé, lancé seul sous la variable fictive, passe, et la variable est toujours posée après
  lui (`mock.patch.dict` rend `os.environ` intact).
- **Écart déclaré (règle 3 de la fiche)** : la fiche dit « tu ne poses jamais SHOGEN_S2_CAMPAGNE_CONTROL » ; le brief de
  cette relecture l'ordonne pour ce contrôle (« avec et sans … posée sur un chemin fictif »). Geste limité à un chemin
  fictif absent de mon dossier, contrôlé avant et après ; aucune copie scellée cherchée ni lue ; exécutions : trois
  suites entières (base, diff 7 seul, série), le test de l'enregistreur seul, et les mutants G-E1f/T-7f. À adjuger par
  l'orchestrateur.

## Contrôle (5) — mutants du réviseur (distincts de ceux du générateur quand c'était possible)

Outil : `G2-B1/outils/mutants_g2.py` (copie neuve de `s2-harness`, `enforcement`, `scripts`, `.github` de la série par
mutant ; une substitution dont le motif est présent exactement une fois ; modules nommés ; mort = code ≠ 0) ; sortie
`G2-B1/journal/mutants-g2.json`. Témoins non mutés : 7/7 verts (dont T-7f sous la variable fictive). Durée 06:05:40Z →
06:08:13Z. Bilan : 18 mutants (13 tués, 5 survivants ; G-E1 rejoué sans et avec variable fictive) et une sonde.

| id | sous-lot | mutation | verdict |
|---|---|---|---|
| G-P1 | 1 | `d.adjusted() > ctx.Emax` → `d.as_tuple().exponent > ctx.Emax` (exposant brut) | **SURVIT** → C-1 |
| G-P2 | 1 | capture réduite à `ValueError` (InvalidOperation non capturée) | tué |
| G-P3 | 1 | filtre `x.get("price") is not None` → `x.get("price")` (prix vide ignoré) | tué |
| G-P4 | 1 | borne `> ctx.Emax + 1` | tué |
| G-P5 | 1 | `int` retiré des types lus (entier JSON refusé) | tué |
| G-P6 | 1 | `not d.is_finite()` → `d.is_nan()` (Infinity gardé) | tué |
| G-A1 | 2 | référence d'une base mise à jour seulement sur changement | tué |
| G-A2 | 2 | comparaison du couple entier, non base par base | tué |
| G-A3 | 2 | base muette du relevé courant comparée (None ≠ valeur) | tué |
| G-L1 | 3 | compte du bloc 5 (d) figé à `(1)` | tué (par les épingles ; le test neuf seul ne le voit pas, n = 1) |
| G-R1 | 4 | étiquette posée sur l'entrée à plage (`j28`) au lieu de `j28-incluse` | tué |
| G-S1 | 5 | variante incluse calculée sur le segment de la première sortie | tué |
| G-V1 | 6 | motif des sauts sans `re.M` | tué |
| G-V2 | 6 | `len(sauts) != k` → `len(sauts) < k` (plus de lignes « skipped » que k admis) | **SURVIT** (O-3) |
| G-V3 | 6 | sortie de unittest non recopiée (`err + out` → `out`) | **SURVIT** (O-3) |
| G-V4 | 6 | variable cherchée dans tout le flux au lieu du motif du saut | tué |
| G-V5 | 6 | dossier `s2-harness` par défaut mal résolu (un `dirname` de moins) | **SURVIT** (O-3) |
| G-V6 | 6 | sonde Q-3 : `PLANCHER = 405` seul | « tué » : 5 cas sur 20 échouent (V-01, V-03, V-12, V-13, C-01) → C-2 |
| G-E1 / G-E1f | 7 | `os.environ.pop` sorti du `patch.dict` (fuite durable de l'environnement), sans / avec variable fictive | **SURVIT** (O-3) |

Preuves des corrections proposées (brouillons hors livrables) :
- C-1 : ajouter `'"12E+999999"'` (exposant ajusté 1 000 000, exposant brut 999 999, mesuré) aux refus « hors contexte »
  de `test_illisible_ou_hors_contexte_refus_nomme` : code livré `OK` ; mutant G-P1 `FAILED (failures=2)` (« ValueError
  not raised », lectures ok et en panne).
- C-2 : quatre lignes du lanceur de cas rendues relatives à `v.PLANCHER` (défaut de `sortie`, V-03, V-04, C-01) : 20 ok
  avec `PLANCHER = 398` et 20 ok avec `PLANCHER = 405`.

## Contrôle (2) — conformité à chaque item, rien de plus

Définitions lues [lu] : annexe B l.79 (B.4), l.174 (B.9), l.209 (B.12), l.226 (B.13), l.639-641 (B.44), l.681-682
(B.46), l.710 (B.47) ; registre `ETAT-REGISTRE-2026-10-04.md` l.49, 52, 53, 68-72, 243, 269, 283, 377-379, 384-385 ;
G0-lots-DETTES (entier) ; G0-lot-D8a §11 item 13 (l.436).

- **SHOGEN-PRIX-ILLISIBLE-1, SHOGEN-PRIX-HORS-CONTEXTE-1** : conformes. Deux erreurs nommées (`r1.PrixIllisible`,
  `r1.PrixHorsContexte`, sous-classes de `ValueError`) levées au point unique de lecture (`r1.parse_journal`), au lieu
  de `InvalidOperation`/`Overflow` non nommées ; prix fini ordinaire inchangé (lu dans le code : la valeur n'est
  jamais réécrite, seule la forme non finie passe à `None`, règle de CORR-2 inchangée). Le contexte nommé piège
  `InvalidOperation`, `DivisionByZero`, `Overflow` (`r1.py` l.66-67, lu) : « abc » lève, jamais NaN. Au-delà de la
  lettre, déclarés : E-1 (booléen, liste, objet refusés : à la base `Decimal(True)` vaut 1, valeur fausse silencieuse)
  et E-2 (refus quel que soit le statut) ; ce sont des serrages sur des entrées que le collecteur n'écrit pas
  (`str(Decimal)` ou `null`), cohérents avec le point unique de CORR-2 ; recommandation pour Q-1 : garder E-1.
  Trou de test : survivant G-P1 (C-1).
- **SHOGEN-ASN-DIVERGENCE-PARTIELLE-1** : conforme. Comparaison base par base des valeurs non muettes ; référence de
  chaque base = son dernier relevé ok non muet ; un échec n'est ni divergence ni référence ; `by_host` inchangé. Pour
  une suite de relevés complets, les deux références sont le même relevé : une entrée au plus par relevé, identique
  au lot CORR (tests existants verts, assertions inchangées ; `test_asn_divergence_published_not_overwritten` tient
  la déduplication). Attendus du test neuf recalculés à la main (h0 : une entrée au relevé partiel ; h2 : deux
  entrées, une par référence ; h3 : aucune ; h4 : à travers l'échec). Observations : O-2.
- **SHOGEN-BLOC5-LIBELLE-1** : conforme (une ligne, un test). Le libellé neuf est vrai : `cluster_pairs` reçoit une
  entrée par paire de clusters à ≥ 2 flux (`r2.py` l.934-955, lu), donc la branche est atteinte si et seulement si
  `n_multi_clusters` < 2.
- **SHOGEN-KEFF-NOTE-1** : conforme (texte de l'item mot pour mot ; test sur la fixture et le filtre
  `[w0 ; w5 − 1]` de `test_bloc5_sondes_toutes_retirees_message_vrai`, l.191-200, lu ; journal sans sonde compris).
- **SHOGEN-RT-ETIQUETTE-INCLUSE-1** : conforme. `r1_discrimine` n'existe, dans les sorties des quatre `recompute_*`,
  qu'au `drapeau_2` de `r2` (`grep` : `r1.py` l.742 dans `regle_critere`, appelée seulement par `r2.drapeau_2` et
  par le rendu texte) ; `drapeau_2` rend toujours un dictionnaire neuf sans clé `etiquette` (`r2.py` l.960-996, lu) :
  ajout purement additif, sur la seule variante incluse.
- **SHOGEN-SENS-POOLEE-1** : décision écrite, test de caractérisation seul ; voir contrôle (6).
- **SHOGEN-CI-S2-SAUT-1** : conforme à la construction de B.4 (résumé final exigé, sauts admis seulement s'ils nomment
  la variable, plancher committé sans égalité figée, bibliothèque standard). Au-delà, documenté dans la docstring mais
  absent des écarts du G1 : « OK (expected failures=…) » refusé (V-10) : serrage. Le choix « plancher » est celui du
  générateur ; B.4 le réserve à un G0 (C-4). Q-3 du G1 inexacte (C-2).
- **SHOGEN-TEST-ENV-HERMETIQUE-1** : conforme (+4 −1, test seul ; `oracle_record.py` inchangé) ; rouge avant / vert
  après mesurés au contrôle (4).
- **Rien de plus** : 16 fichiers, tous rattachés à un item ; les retouches hors code neuf sont nécessaires (docstrings
  de deux tests ASN dont la sémantique change ; « abc » et `[1]` retirés de la liste « inchangés » ; `cls.src` ;
  commentaires du job, E-12 : le renvoi « annexe D.2 pt 7 » devient « annexe D.4 a », qui nomme les deux tests).

## Contrôle (6) — la décision sur SHOGEN-SENS-POOLEE-1 au regard du paquet scellé §7

Lu [lu] : paquet `PAQUET-PREREG-S2.md` §4 (l.54-59), §6-§7 (l.67-85), §10.2 pts 1-11 (l.110-134), bloc machine
(l.213-222 : `commit_analyse f35a70c19ba8269f1f7e2bcd31775e4fc513da20`, `sha256_script 06d189cf…9050`) ; ADR-0028 l.35
(D2 pt 4), l.38 et l.118 (D2 pt 7 et son amendement), l.273 (décision 273 : « famille de trois tests ramenée à deux
confirmatoires ») ; `report.py` l.386-399 (poolée au bloc 3) et l.684-730 (`[SENSIBILITÉ]` : lignes par strate
confirmatoire seulement) ; `rendu_unique.py` à `f35a70c` (`git show`, lecture) l.403 : la variante `j28-incluse`
existe au recalcul tiers ; `r1.py` à `f35a70c` l.693 : clé `poolee` dans la sortie de `recompute_from_journal`.

**Verdict : la décision est juste**, pour trois raisons tirées du texte scellé et du code d'analyse :
1. §7 fixe la liste fermée (plage exclue ou incluse ; seconde coupe J14) et le lieu de « plage incluse » (section
   `[SENSIBILITÉ]` du rendu J28) ; la forme de cette section est scellée par référence (commit d'analyse et
   `sha256_script`) et ne porte que les strates confirmatoires. L'exécution unique est faite et les rendus ne sont
   jamais réécrits (G0-lots-DETTES l.6-7) : une troisième ligne ne pourrait être, pour S2, qu'une analyse « ajoutée
   après le pré-enregistrement » (classe C), jamais une sensibilité du paquet.
2. La strate poolée est exploratoire, hors famille, hors décision (§4, §10.2 pt 9 ; ADR-0028 D2 pt 4 et décision 273,
   qui ramène la famille à deux tests confirmatoires) ; ses valeurs sous les deux variantes du J28 sont déjà publiées
   par le JSON du recalcul tiers (`j28.r1.poolee`, `j28-incluse.r1.poolee`, vérifié au code de `f35a70c`) : aucune
   valeur n'est perdue.
3. Le test de caractérisation fige cette prémisse (poolée présente dans les deux variantes, étiquetée, égale à
   `recompute_from_journal`, différente entre variantes) ; il tue G-S1 (le générateur rapporte trois autres mutants
   tués, S-M1 à S-M3, non rejoués ici).

Nuances (non bloquantes, O-5) : (a) le motif 1 du G1 dit « combinaison que le texte scellé ne liste pas » ; §7 dit
aussi « toute autre analyse est exploratoire », qui n'interdit pas une ligne exploratoire : l'argument décisif est le
moment (après l'exécution) et la publication au JSON, non une interdiction du texte ; (b) le motif 3 (tolérance des
épingles du brief) est de procédure, non de fond ; (c) les « trois z » d'ADR-0025 déc. 4 sont cités de seconde main
([2nd], journal G1 du lot B l.200) ; ADR-0025 est hors de ma lecture (exclue de la copie) ; leur lien avec la famille
de trois tests de la décision 273 est [inféré] ; (d) portée : la décision vaut pour S2 ; pour S2-bis, la forme de
`[SENSIBILITÉ]` relève de son propre pré-enregistrement (ADR-0029), à écrire dans la ligne de clôture.

## Contrôle (8) — la conséquence E-8 est-elle écrite là où un tiers la lira ?

Mesuré : `git diff --quiet f35a70c HEAD -- s2-harness/shogen_s2 s2-harness/tools` sort **0** à la tête `3e275a2` :
aujourd'hui, la tête et le commit d'analyse coïncident sur les chemins gardés. Après la série, `rendu_unique.py` passe
de `06d189cf…9050` (égal à `sha256_script`) à `5ee95dbf4a6800ed8aa61bf6bfa52c0662100385cf4e15efa57010e6569cf4b8`, et
`shogen_s2/r1.py`, `r2.py`, `report.py` changent : à la tête, les gardes (2) et (4) refuseront, et les points d'entrée
`recompute_*` ne reproduiront plus à l'identique les sorties versées (libellé du bloc 5 (d), note k_eff, clé
`etiquette` du drapeau 2 de `j28-incluse`, et les divergences ASN de relevés partiels, que la tête publie désormais).

Lu : `docs/11-mesures-pilotes.md` §12 « Reproduire » (l.992-1011) et `docs/adr-0028/PROCEDURE-EXECUTION.md` (entier).
- §12 désigne déjà, avant ce lot, le code de reproduction : « commit d'analyse `f35a70c…` », script `06d189cf…`, et
  « une nouvelle production par `rendu_unique.py` serait une seconde exécution » : l'essentiel est écrit.
- Mais ni §12 ni la procédure ne disent que la tête s'écarte de `f35a70c` à partir du commit de ce lot, ni que tout
  rejeu ou ré-exécution doit se faire sur une extraction de `f35a70c`. La procédure §1 fait même lire la garde (2)
  contre `HEAD`. La conséquence n'est écrite qu'au journal G1 (E-8), qu'un tiers ne lit pas.
- **Réponse : non** → C-3. Elle touche aussi SHOGEN-REJEU-HOTE-1 (B.46 : rejeu des rendus sur un second hôte, avant
  G9 ou S2-bis), qui devra se faire à `f35a70c`.

## Contrôle (7) — vérificateur `enforcement/verdict-suite-s2.py` et job `gates.yml`

Relecture du code (diff 6, lu en entier) : `verdict` exige code 0, résumé final ancré en fin de flux (`FIN`, tirets,
`Ran N tests in …s`, ligne vide, `OK` ou `OK (skipped=k)`), exactement k lignes « … skipped » (`SAUT`, `re.M`), chaque
motif nommant la variable, `N ≥ PLANCHER` ; `lancer` retire la variable de l'environnement de la suite ; `main` rend 0,
1 ou 3 ; imports : `os`, `re`, `subprocess`, `sys` (bibliothèque standard). YAML relu par PyYAML 6.0.1 déjà présent
(`/usr/lib/python3/dist-packages`, aucune installation) : job `s2-harness-unittest`, `runs-on: ubuntu-24.04`,
`timeout-minutes: 10`, étapes : checkout épinglé, cas du vérificateur, suite jugée par le vérificateur.
- Cas du vérificateur : `20 ok, 0 échec`, sortie 0, sous Python 3.11.15, 3.12.3 et 3.13.14.
- Rejeu du job (outil `G2-B1/outils/rejouer_job.py` : étapes `run` lues dans `gates.yml`, chacune sous
  `bash --noprofile --norc -eo pipefail -c`, depuis la racine de l'arbre, arrêt à la première étape en échec) :
  | arbre | suite (unittest seul) | vérificateur | job |
  |---|---|---|---|
  | série intacte | `Ran 405` `OK (skipped=2)` | conforme | **VERT** |
  | `test_window.py` renommé hors du motif (MT-5) | `Ran 391` `OK (skipped=2)` | refus : `Ran 391 < plancher 398` | **ÉCHEC** |
  | module neuf, saut « autre motif » (R8) | `Ran 406` `OK (skipped=3)` | refus : motif sans la variable | **ÉCHEC** |
  Dans les deux derniers cas, l'ancienne commande du job (code de sortie seul) aurait rendu VERT.
- Mutants : G-V1 et G-V4 tués ; G-V2, G-V3, G-V5 survivent (O-3) ; sonde G-V6 : le plancher ne se relève pas en une
  ligne (C-2).
- Consommateur : forge morte (SHOGEN-CI-S2-FORGE-1) ; le G3 opérant est l'oracle local (ADR-0028 §4.11, l.291) et ses
  amendements datés ajoutent les commandes des jobs de D8a, D8b, D8c (l.296-298), pas encore celles de D8a-3 : sans
  cet ajout, le vérificateur ne tourne nulle part (C-5, réponse à Q-4 du G1).

## Contrôle (9) — R-25, R-13, R-8, `xtask`

- R-25 : sept diffs, +85, +48, +36, +29, +15, +183, +4 lignes ajoutées : chacun ≤ 200 (un commit par diff).
- R-13 : motif du job g5 (`gates.yml` l.66) appliqué aux 16 fichiers de la série : aucun constat (code 1 de `grep`) ;
  aucun `TODO`, `FIXME`, `XXX`, `HACK` dans les diffs.
- R-8 : aucune dépendance neuve ; bibliothèque standard seule (imports relus) ; PyYAML n'est employé que par les
  outils de relecture (du G1 comme du G2), jamais par le code livré.
- Longueurs : aucune ligne ajoutée au-delà de 120 caractères (compte en caractères) ; fichiers neufs en mode 0644,
  UTF-8 sans BOM.
- `cargo --locked xtask verify` sur la série (cible `CARGO_TARGET_DIR` dans mon dossier) : sortie 0,
  `VERDICT GLOBAL : VERT`, S-G1 à S-G8 vertes, clippy `-D warnings` vert ; S-G5 en régime partiel (« 0 artefact(s)
  présent(s) sur 155 déclaré(s) », octets de `biblio/` non versionnés), comme au G1 ; le lot ne touche aucun `.md`.

### Contrôle (7), suite — le plancher 398 sous une suite de 405

Huit modules au moins comptent 7 tests ou moins dans la série (comptes par module de la sortie `-v`) ; trois d'entre
eux ne sont importés par aucun autre module (`test_hote_deux_flux` 3, `test_sceau` 4, `test_censure_causes` 5).
Rejeu du job, `test_hote_deux_flux.py` renommé `hote_deux_flux.py` (ses 3 tests disparaissent, dont le test neuf de
SHOGEN-BLOC5-LIBELLE-1) :
| plancher | cas du vérificateur | suite | vérificateur | job |
|---|---|---|---|---|
| 398 (livré) | 20 ok | `Ran 402` `OK (skipped=2)` | **conforme** | **VERT** (perte non vue) |
| 405, cas relatifs à `v.PLANCHER` (C-2) | 20 ok | `Ran 402` `OK (skipped=2)` | refus : `Ran 402 < plancher 405` | ÉCHEC |
À la tête de la série, le cas (2) de B.4 (« un module de test sorti du motif `test*.py` par renommage ») n'est donc
refusé que pour un module de plus de 7 tests : l'écart vient des 7 tests que le lot ajoute lui-même (C-2).

### Compléments mesurés (06:15-06:19 UTC)

- États intermédiaires de la série (un commit par diff, ordre 1 → 7), suite sans variable : c1 `Ran 400`, c1-2 `Ran 401`,
  c1-3 `Ran 403`, c1-4 `Ran 404`, c1-5 `Ran 405`, c1-6 `Ran 405`, série `Ran 405` : tous `OK (skipped=2)`, sortie 0. La
  suite reste verte à chaque commit.
- Vérificateur sur la vraie suite de la série sous Python 3.12.3 (version inférée de l'image `ubuntu-24.04`) : sortie 0,
  `Ran 405` `OK (skipped=2)`, « conforme », stderr vide.
- Hygiène : 0 `__pycache__` dans mes arbres ; aucun temporaire des tests ni du lanceur de cas hors de mon dossier
  (`find /tmp -maxdepth 1 -newer` le brief) ; aucune écriture dans `/home/user/shogen`.
- Durées de la suite sous charge (charge moyenne 14 à 16 sur 4 cœurs, autres agents actifs) : 78 à 280 s ; le délai
  de 10 min du job tient.

## Verdict

**ACCEPTE-AVEC-CORRECTIONS** — horloge lue avant d'écrire : 2026-10-04 06:19:26 UTC.

Les sept diffs s'appliquent seuls et en série sur `3e275a2` ; chaque item est construit et conforme à sa définition ;
la règle `ea3a2d94…` est inchangée ; le ré-épinglage des deux rendus est justifié par les seules lignes de
SHOGEN-BLOC5-LIBELLE-1 et SHOGEN-KEFF-NOTE-1 ; la suite est verte (405, et seulement les deux tests nommés en erreur
sous la variable fictive) ; `xtask` vert ; R-25, R-13, R-8 tenus ; la décision sur SHOGEN-SENS-POOLEE-1 est juste.
Les corrections portent sur un trou de test (C-1), sur le plancher du vérificateur (C-2), et sur trois actes
d'écriture de l'orchestrateur (C-3 à C-5), sans lesquels la conséquence E-8 resterait invisible d'un tiers et la
fermeture de SHOGEN-CI-S2-SAUT-1 incomplète.

### Liste fermée des corrections

- **C-1 (diff 1, test ; générateur ou orchestrateur)** : ajouter `'"12E+999999"'` aux refus « hors contexte » de
  `test_illisible_ou_hors_contexte_refus_nomme` (coefficient à plusieurs chiffres : exposant ajusté 1 000 000 > Emax,
  exposant brut 999 999), et « exposant brut au lieu de l'exposant ajusté » à sa liste « Rougit si ». Motif : survivant
  G-P1. Preuve : code livré `OK`, mutant `FAILED (failures=2)`.
- **C-2 (diff 6 ; générateur ou orchestrateur)** : (a) rendre les cas du lanceur relatifs à `v.PLANCHER` : défaut de
  `sortie(n=…)`, V-03 (`n` et fragment `plancher …`), V-04, C-01 ; quatre lignes (libellés de V-01, V-03, C-01 à
  ajuster) ; preuve : 20 ok à 398 comme à 405 ;
  (b) relever `PLANCHER` à 405, le compte mesuré après les diffs 1 à 5 (le diff 7 n'ajoute aucun test), au commit de la
  série, et mettre à jour son commentaire ; motif : avec 398 sous 405, un module de 7 tests ou moins sorti du motif
  passe le job (rejeu mesuré : `test_hote_deux_flux.py` renommé, job VERT), alors que B.4 vise ce cas (2) ; (c)
  corriger Q-3 et L-4 du journal G1 : relever le plancher n'y est pas « une ligne » (sonde G-V6 : V-01, V-03, V-12,
  V-13, C-01 échouent).
- **C-3 (orchestrateur, documents ; contrôle 8)** : écrire la conséquence E-8, par ajout daté, là où un tiers la lit :
  `docs/11` §12 (points « Code » et « Rejeu ») et `PROCEDURE-EXECUTION.md` (garde (2) du §1, lue contre `HEAD`), ainsi
  que dans la ligne de SHOGEN-REJEU-HOTE-1. Texte : à partir du commit du lot DETTES-B1, `s2-harness/shogen_s2` et
  `s2-harness/tools` diffèrent du commit d'analyse `f35a70c` (sha256 de `rendu_unique.py` `5ee95dbf…` ≠
  `sha256_script` `06d189cf…`) : les gardes (2) et (4) refusent à la tête ; tout rejeu (`recompute_*`) ou ré-exécution
  du rendu de S2 se fait sur une extraction de `f35a70c` ; à la tête, les sorties diffèrent par construction (bloc 5
  (d), note k_eff, clé `etiquette` du drapeau 2 de `j28-incluse`, divergences ASN de relevés partiels).
- **C-4 (orchestrateur, G0)** : consigner dans un G0 (ligne DETTES-B1 de `G0-lots-DETTES.md`, ou amendement daté de
  `G0-lot-D8a.md` §11 item 13) le choix « plancher, et non manifeste » et sa valeur, avec le motif du journal G1 §9 :
  B.4 réserve ce choix à un G0 (« choix au G0 ») et le G0 de D8a ne l'a pas tranché.
- **C-5 (orchestrateur, ADR-0028 §4.11 ; réponse à Q-4)** : amendement daté, sur le précédent de D8a, D8b et D8c
  (l.296-298) : à partir du commit de D8a-3, le G3 opérant comprend les deux commandes du job `s2-harness-unittest`,
  `python3 -B enforcement/tests/run-fixtures-verdict-suite-s2.py` (attendu `verdict-suite-s2 : 20 ok, 0 échec`) et
  `python3 -B enforcement/verdict-suite-s2.py` (attendu « conforme », `Ran 405`), à la place de la suite nue. Sans
  lui, tant que la forge est morte (SHOGEN-CI-S2-FORGE-1), le vérificateur ne tourne nulle part.

### Limites rendues comme items à former (règle PAROXYSME ; propositions, propriétaire : orchestrateur)

- **SHOGEN-ASN-PARTIELLE-S2-1** (nom proposé) : effet de SHOGEN-ASN-DIVERGENCE-PARTIELLE-1 sur les journaux scellés de S2
  non mesuré. Les rendus versés (`f35a70c`) appliquent la sémantique du lot CORR (relevés complets seuls ;
  `asn_divergences: []` partout, B.46) ; un changement d'ASN visible sur une seule base n'y est pas cherché. Mesure
  possible seulement par une analyse « ajoutée après le pré-enregistrement, hors décision » (lot POST-PREREG, lecture
  des journaux par l'orchestrateur), ou limite déclarée au rapport. Déclencheur : G0 de POST-PREREG.
- **SHOGEN-CI-S2-CABLAGE-1** (nom proposé) : aucun test automatique ne lit les étapes du job `s2-harness-unittest`
  (`xtask` ne lit pas `gates.yml` ; le cas H-20 des hooks n'extrait que le motif du job g5) : ramener l'étape à la
  commande nue passerait tous les contrôles locaux. Construction possible : un cas qui extrait les lignes `run` du job
  (forme de H-20) et exige l'appel du vérificateur. Déclencheur : SHOGEN-CI-S2-FORGE-1, ou prochain lot qui touche
  `gates.yml`.
- J'appuie les quatre items proposés par le G1 (§14) ; SHOGEN-CI-PLANCHER-SUIVI-1 reste nécessaire après C-2 (le
  plancher doit suivre N aux lots suivants).

### Observations non bloquantes

- **O-1** (diff 1) : E-1 et E-2 sont des serrages déclarés, sans effet sur ce que le collecteur écrit ; pour Q-1, je
  recommande de garder E-1.
- **O-2** (diff 2) : une transition comme (5,5) → (−,5) → (6,6) publie deux entrées dont la seconde redit la première
  (E-4, déclaré) ; la ligne « DIVERGENCE ASN » imprime les tuples tels quels, donc `None` pour une base muette, là où
  le tableau voisin écrit `-`.
- **O-3** (diffs 6 et 7) : survivants G-V2 (plus de lignes « skipped » que k), G-V3 (sortie non recopiée), G-V5
  (dossier par défaut, celui qu'emploie le job ; une erreur y rendrait le job rouge, non vert) et G-E1 (fuite durable
  de l'environnement, masquée par l'ordre des modules ; le code livré restaure, mesuré) ; un cas chacun suffirait.
- **O-4** (diff 6) : « OK (expected failures=…) » est refusé (V-10) : serrage documenté dans la docstring, absent des
  écarts du G1.
- **O-5** (décision SENS-POOLEE) : nuances du contrôle (6) (motif 1 formulé trop fort ; motif 3 de procédure ; « trois
  z » d'ADR-0025 de seconde main ; portée S2, S2-bis renvoyé à son pré-enregistrement), à écrire dans la ligne de
  clôture.
- **O-6** (journal G1) : la citation « ADR-0028 §4.11 l.171 » de Q-4 ne tombe plus sur la liste du G3 opérant à la tête
  (l.291 et l.296-298).

### Réponses proposées aux questions du G1 (l'orchestrateur adjuge)

Q-1 : garder E-1. Q-2 : adopter la décision, avec la portée de O-5. Q-3 : oui, par C-2. Q-4 : oui, C-5. Q-5 : garder la
forme livrée (clé `etiquette` du drapeau 2 : schéma et domaine de valeur conservés). Q-6 : former l'item. Q-7 : 405
(mesuré). Q-8 : acte de l'orchestrateur.

## Journal de provenance (G1 de la relecture)

**Sources** (niveau ; plages) :
- [lu] brief de relecture (entier, sha256 recompté) ; brief du lot `BRIEF-DETTES-B1.md` (entier) ; journal G1
  `G1-DETTES-B1.md` (entier) ; les sept diffs (entiers) ; `LIVRABLES.sha256`.
- [lu] `docs/adr-0028/G0-lots-DETTES.md` (entier) ; `ETAT-REGISTRE-2026-10-04.md` (lignes des items, par `grep`) ;
  `ANNEXE-B-items.md` l.195-230, l.625-711, et l.72, 79, 174 (par `grep`) ; `ANNEXE-D-preenregistrement.md` l.25-50
  (D.2) et l.124-140 (D.4 a-b) ; `G0-lot-D8a.md` l.405-460 ; `PAQUET-PREREG-S2.md` l.54-86, l.110-135, l.210-223 ;
  `ADR-0028-decisions-sortie-S2.md` l.35, 38, 118, 273 (par `grep`), l.165-175, l.287-300 ; `PROCEDURE-EXECUTION.md`
  (entier) ; `docs/11-mesures-pilotes.md` : titres (par `grep`) et §12 l.992-1011 seulement.
- [lu] code de la série : `r1.py` l.62-76, l.395-445 ; `r2.py` l.915-996, l.1040-1100 ; `report.py` l.380-400,
  l.540-556, l.590-615, l.684-730 ; `rendu_unique.py` l.1-58, l.161-202, l.395-422 ; tests touchés (contextes lus) ;
  `scripts/controle/README.md` l.1-60, `render_fixture.py` (entier), `SHA256SUMS` ; `gates.yml` (lignes du job et
  l.60-67) ; `.cargo/config.toml`, `rust-toolchain.toml`. Au commit `f35a70c` (`git show`, lecture) :
  `rendu_unique.py` (l.47-53, l.402-412, et son sha256), `r1.py` (l.563, l.693).
- [2nd] « trois z » d'ADR-0025 déc. 4, cité par le journal G1 du lot B l.200 (ADR-0025 non lue, hors copie).
- [abs] aucun.

**Commandes et sorties** (préfixe Python : `env -u SHOGEN_S2_CAMPAGNE_CONTROL PYTHONDONTWRITEBYTECODE=1 python3 -B`,
`TMPDIR` dans `G2-B1/tmp`, sauf les exécutions à variable fictive déclarées) ; journaux dans `G2-B1/journal/` :
- 05:50:58Z `sha256sum` du brief (`e5a02393…`) ; `sha256sum -c LIVRABLES.sha256` : 8 OK ; `git rev-parse HEAD` :
  `3e275a2…` ; `git status --short` (lecture).
- `git archive HEAD | tar -x` (exclusions du brief) ; `git apply --check` / `git apply` : seuls 7/7, série 7/7, inverse
  identique ; `cmp` avec l'arbre série du générateur : 16/16 identiques ; comptes R-25.
- 05:55:55Z → 05:59:43Z suites `-v` : base `Ran 398` `OK (skipped=2)` (`base-suite-v.log`) ; série `Ran 405`
  `OK (skipped=2)` (`serie-suite-v.log`).
- `regle_fixtures.py` et `render_fixture.py` sur 9 arbres (`G2-B1/nonreg/`) ; `diff` des rendus base/série.
- 06:02:14Z → 06:07:24Z suites sous variable fictive (`*-suite-fictive.log`) ; test de l'enregistreur seul sous
  variable fictive (restauration vérifiée).
- Cas du vérificateur sous 3.11.15, 3.12.3, 3.13.14 (`cas-python3.1x.log`) : 20 ok chacun.
- 06:05:40Z → 06:08:13Z mutants (`outils/mutants_g2.py`, `mutants-g2.json`, `mutants-g2.log`).
- 06:08:18Z → 06:09:04Z `cargo --locked xtask verify` sur la série (`serie-xtask.log`) : VERT.
- 06:09:50Z → 06:14:11Z rejeux du job (`outils/rejouer_job.py`, `job-ok.log`, `job-mt5.log`, `job-r8.log`) ;
  06:15:30Z → 06:16:51Z `job-hdf398.log`, `job-hdf405.log`, états c1, c1-2 ; 06:17:13Z → 06:19:18Z états c1-3 à c1-6
  (`cum-c*.log`) et vérificateur sous 3.12 (`verdict-py312.out`).
- Brouillons de preuve des corrections : `G2-B1/mut/c1-*` (C-1), `G2-B1/mut/c2-398`, `c2-405` (C-2), `G2-B1/mut/v6`.

**Chiffres recomptés par moi** : 8 empreintes ; 16 fichiers ; +85/+48/+36/+29/+15/+183/+4 lignes ajoutées ; 398 → 405
tests (7 noms neufs, 0 retiré) ; deux sauts ; quatre empreintes de rendu et l'empreinte de la règle ; deux lignes de
diff par rendu ; 20 cas × 3 versions ; 18 mutants (13 tués, 5 survivants, G-E1 rejoué sous deux environnements),
une sonde (G-V6) et 7 témoins ; comptes de tests par module ;
`Ran` des rejeux (405, 391, 406, 402, 402) ; sha256 de `rendu_unique.py` à la tête, à `f35a70c` et après la série.

## Attestation

Je n'ai ouvert aucune pièce de la liste D.2 ; je n'ai rien lu sous `docs/rapports/`, `docs/adr-0025/`,
`docs/adr-0028/monark-m009a/` (exclus de ma copie), ni `docs/15-*`, `docs/16-*` (présents dans la copie pour `xtask`,
jamais ouverts ni balayés : chaque recherche visait des fichiers ou dossiers nommés) ; je n'ai ouvert aucun `*.jsonl`
(aucun n'est suivi à la tête ; les seuls journaux lus par les tests sont leurs fixtures, écrites en temporaire). Une
seule exposition volontaire : `docs/11` §12 (l.992-1011, sans valeur de campagne) et les titres de `docs/11`. Aucune
opération git en écriture ; aucune écriture hors de `G2-B1/`. Écart déclaré : variable scellée posée sur un chemin
fictif, sur ordre du brief (contrôle 4).

## Clôture (06:21:23 UTC)

Tête toujours `3e275a2`. L'arbre de travail du dépôt a changé pendant la relecture, sans moi : `JOURNAL.md` modifié ;
non suivis neufs `docs/adr-0029/CONTRE-EXPERTISE-DECISIONS.md`, `scripts/controle/sorties-fm11/contre-expertise.json`,
`etude-p6.json` (actes d'autres agents, travaux ADR-0029). Mes seules commandes dans `/home/user/shogen` ont été des
lectures git (`rev-parse`, `status`, `log`, `ls-files`, `show`, `diff --quiet`, `archive`) ; toutes mes écritures sont
sous `G2-B1/`. Les diffs du lot ne touchent aucun de ces fichiers.
