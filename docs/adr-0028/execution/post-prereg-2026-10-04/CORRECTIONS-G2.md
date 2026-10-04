# CORRECTIONS — lot POST-PREREG : corrections G2 C-1 à C-6 et mesure du rejeu après DETTES-B1 (lot PP-CORR)

- Worker : `shogen-worker`, Gate 0 : modèle `claude-opus-5-5` (identifiant exact de la session), effort `max`.
- Brief : `dettes/PP-CORR/BRIEF-PP-CORR.md`, sha256 `f916d8ecdcdf676d4090175821f11329382a14d576a53424132c7488607ca4c0`
  (recalculé : égal). Ouverture : 2026-10-04 06:43:30 UTC (`date -u`).
- Rattachement : `docs/adr-0028/G0-lots-DETTES.md`, ligne POST-PREREG ; relecture G2 `dettes/G2-PP/G2-POST-PREREG.md`
  §5 (C-1 à C-6, liste fermée) et §6 (journal G1 à verser ; interaction DETTES-B1).
- Base des diffs : tête `dad3bc6f6c35537d7bb5f8510bbdb354afa966f5` (« Lot DETTES-B1 clos »), branche
  `partie-4-execution`. Travail commencé sur `3cc0892` (06:46), rebasé sur `dad3bc6` à 06:59 (voir E-3).
- Aucune opération git en écriture ; écritures limitées à `dettes/PP-CORR/`.

## 1. Ce qui a changé

Quatorze diffs, mêmes noms, contre `dad3bc6`, en série par `git apply --whitespace=error`. Huit sont identiques à
l'octet aux diffs livrés (01, 02, 04, 05, 09, 10, 11, 13). Six changent :

| diff | correction | contenu | lignes ajoutées (livré → corrigé) |
|---|---|---|---|
| 03-PP-b | C-1 | `test_sens_pool.py` : `test_critere_par_strate_contre_n_s` (100 fenêtres calmes, 20 de stress, e en panne dans 5 des 20 ; attendu à la main : ok calme 100 partout, ok stress a-d 20 et e 15, pools {calme : a-e, stress : a-e}, aucun refus) | 157 → 169 |
| 06-PP-d2 | C-3 | `test_hote_horloge.py` : `test_horloge_offsets_non_dyadiques_compte_pair` (offsets 0.1, 0.2, 0.7, 1.3 : min 0.1, médiane 0.45, max 1.3, étendue 1.2 en `Decimal` exacts, et ligne imprimée) | 42 → 53 |
| 07-PP-e1 | C-2 | `test_censure.py` : `test_maximum_sur_une_paire_non_voisine` (`bornes(40, 1, [4, 1, 2], 2)` : maximum = énumération exhaustive = 13692/√29264970, sommet (2, (0, 2)), aucun c relâché) | 129 → 141 |
| 08-PP-e2 | aucune | contenu inchangé ; ligne `index` et numéros de hunk décalés de 12 (le test C-2 précède dans le fichier) | 167 → 167 |
| 12-PP-i1 | C-6 | README des sorties : paragraphe « Version du harnais » (commit d'analyse `f35a70c` ; un rejeu se fait à cette version) | 176 → 185 |
| 14-PP-j | C-4, C-5, citation G1 | §11.1 : texte C-4 et C-5 du G2 §5 recopié mot pour mot (contrôle par programme) ; « journal G1 du worker (`docs/G1-lot-POST-PREREG.md`) » ; deux paragraphes remis à la largeur de 120 | 53 → 56 |

Aucun fichier de code d'analyse, aucune sortie, aucun `SHA256SUMS` des sorties ne change (le `SHA256SUMS` des sorties ne
liste pas le README). Aucun fichier de `s2-harness` touché. Les remarques non bloquantes du G2 (§7) ne sont pas traitées
(liste fermée).

## 2. Preuves

- Méthode de régénération (`outils/regen.py original`) : à partir de la tête et des diffs livrés, les 14 diffs livrés
  sont reproduits à l'octet sur `3cc0892` ; sur `dad3bc6`, 13 à l'octet et le 14 au seul en-tête `index` près (le
  `docs/11` de la tête porte l'ajout daté de 06:52:35 UTC en fin de §12 ; hunk identique).
- Application : diffs corrigés, `git apply --check --whitespace=error` puis `git apply --whitespace=error`, 01 à 14, sur
  une copie neuve de `dad3bc6` : 14 OK ; `diff -r` contre l'arbre de travail corrigé : vide.
- Rouge avant, vert après (mutants du réviseur, substitutions identiques à `G2-PP/mut/mutants_g2.py`, contrôlé par
  programme ; copie fraîche par mutant ; suite post-s2 entière ; `journal/mutants-avant-final.log`,
  `journal/mutants-apres-final.log`) :

| mutant | diffs livrés (29 tests) | diffs corrigés (32 tests) | test rougi et motif |
|---|---|---|---|
| R1 `Decimal(repr(x))` → `Decimal(x)` | VIVANT | TUÉ | C-3 : min `0.1000000000000000055511151231257827021181583404541015625` ≠ 0.1 |
| R2 critère contre le n du segment | VIVANT | TUÉ | C-1 : pools {calme : a-e}, refus [stress] |
| R3 paires voisines seulement | VIVANT | TUÉ | C-2 : argmax (2, (0, 1)) ≠ (2, (0, 2)) ; maximum ≈ 2,4407 |
| R10 médiane haute | VIVANT | TUÉ | C-3 : médiane 0.7 ≠ 0.45 |

- Références des nouveaux cas, indépendantes du code testé : C-1 et C-3 comptés à la main ; C-2 : P_more au sommet
  e' = (6, 1, 4)/42 = 115/6174, z' = (3·6174 − 42·115)/√(42·115·6059) = 13692/√29264970, dérivé à la main et recoupé
  par `outils/ref_c2.py` (64 imputations en `Fraction`, sans import du lot) : maximum 2.53100410096056530789…,
  atteint par la seule imputation e' = (6, 1, 4), K' = 3 ; maximum sur paires voisines 2.44071936137505990766….
- Suite post-s2 : 32 tests OK sur l'arbre corrigé ; après chaque diff de code, copie neuve : 4, 6, 10, 13, 16, 18, 22, 24,
  26, 30, 32 tests, OK à chaque pas (`journal/suite-par-pas.log`).
- Suite `s2-harness` (`env -u SHOGEN_S2_CAMPAGNE_CONTROL PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s
  tests -t .`) : `dad3bc6` + diffs corrigés, `Ran 405 tests in 65.927s`, `OK (skipped=2)` (07:02:28-07:03:36) ;
  base `3cc0892` + diffs livrés : `Ran 405 tests in 72.205s`, `OK (skipped=2)`.
- `CARGO_TARGET_DIR=<copie de target/> cargo --locked xtask verify` sur l'arbre corrigé (07:08:09-07:08:21) : rc 0,
  S-G1 à S-G8 `VERDICT : VERT (0 violation(s))`, `cargo fmt --check`, no_std, `clippy -D warnings` VERTS,
  `=== VERDICT GLOBAL : VERT ===` ; S-G4 : 132 fichiers `docs/**/*.md` ; S-G5 en régime « corpus incomplet » ; une ligne
  du journal cite `docs/15|16` (comptée, non affichée).
- R-25 (lignes `+` moins `+++`) : +144, +137, +169/−8, +89, +177, +53/−7, +141, +167/−2, +166/−3, +189, +144, +185, +75,
  +56 : tous ≤ 200. R-13 : 0 `TODO|FIXME|XXX` dans les lignes ajoutées et dans les fichiers du lot. R-8 : aucun import
  neuf (bibliothèque standard, harnais, modules du lot). Lignes neuves ≤ 120 caractères.

## 3. Mesure du point 3 (rejeu après DETTES-B1)

- Copie : `dad3bc6` + 14 diffs corrigés. `s2-harness/shogen_s2` et `s2-harness/tools` y diffèrent de `f35a70c` depuis
  `0221a74` (B1-1 : refus nommés de `r1.parse_journal`, appelé par `commun.charger` ; B1-2, B1-3 :
  `r2.compute_partition` et libellé de `report.py`, qu'aucun script du lot n'appelle ; B1-4 : `rendu_unique.py`, que
  les scripts n'importent pas ; `test_commun.py` n'en lit que les constantes de la sortie « j28 », inchangées) ;
  identiques entre `3cc0892` et `dad3bc6`.
- Journaux de la session : `sha256sum -c` contre le bloc machine du paquet (l.217-219) : control, journal, raw OK
  (07:03:56-07:03:57). Aucun journal affiché.
- Rejeu (`outils/rejeu.sh`, forme de `G2-PP/rejeu.sh`, chemins seuls changés ; trois scripts à la fois ;
  07:04:16-07:07:33) : 9 codes 0 ; 18 flux stdout/stderr de 0 octet ; aucun `PrixIllisible`, aucun `PrixHorsContexte`.
- Lignes d'en-tête retirées avant comparaison : **aucune**. C-1 à C-6 ne modifient aucun script : les sha256 de
  `commun.py` et des sept scripts sont ceux des en-têtes livrés (`72948a51…`, `3475aeac…`, `8d6b8cf2…`, `145241f1…`,
  `cb19845b…`, `0f1ce347…`, `db6b76f0…`, `f6f69d43…`) ; journaux et rendu J28 inchangés.
- Résultat : **identique**. `cmp` des neuf sorties rejouées : 9 IDENTIQUES aux sorties livrées (diffs 12-13) et 9
  IDENTIQUES au rejeu du réviseur G2 ; `sha256sum -c` du `SHA256SUMS` livré sur les sorties rejouées : 9 OK
  (`journal/comparaison-rejeu.log`). `parse_journal`, appelé par `commun.charger` sur `journal.jsonl` entier, n'a levé
  aucun refus nommé : avec le harnais de la tête `dad3bc6` (DETTES-B1 compris), les neuf scripts rendent les mêmes
  sorties qu'avec celui du commit d'analyse.

## 4. Écarts déclarés

- E-1 : la fiche du worker dit « fixtures seulement (D.4 a) » ; le point 3 du brief et la ligne POST-PREREG du G0
  (« lit les journaux scellés : oui ») font lire la copie de session par les scripts du lot. Tests et mutants sur
  fixtures seulement ; journaux lus par les seuls scripts du lot, jamais affichés, `SHOGEN_S2_CAMPAGNE_CONTROL` jamais
  posée. Même écart que E-7 du G1 et §10 du G2 ; item proposé par le G2 : SHOGEN-FICHE-WORKER-POSTEXEC-1 (appuyé).
- E-2 : la commande d'extraction du brief n'exclut ni `docs/15-*`, ni `docs/16-*`, ni `JOURNAL.md`, ni `biblio/` ; un
  `diff -r` entre deux copies complètes en a lu les octets par programme (sortie vide) ; `cargo xtask verify` les lit par
  construction. Aucun de ces fichiers ouvert ni affiché.
- E-3 : la tête a bougé pendant le travail (`3cc0892` à 06:46, `dad3bc6` à 06:56:49 : B1-6, B1-7, actes G2 de B1,
  clôture de B1). Copie refaite sur `dad3bc6`, corrections reportées (fichiers du lot identiques), diffs régénérés
  contre `dad3bc6`, tous les contrôles des §2 et §3 refaits sur `dad3bc6`.
- E-4 : C-6 dit aussi, en dernière phrase, que `s2-harness/shogen_s2` diffère de `f35a70c` depuis `0221a74` (fait lu
  par `git diff`, motif du G2) ; phrase détachable sans toucher au reste.
- E-5 : C-2 épingle aussi le sommet (2, (0, 2)) et C-3 la ligne imprimée, au-delà du seul maximum et des seules valeurs.

## 5. À l'orchestrateur

- Verser le journal G1 du worker (`dettes/POST-PREREG/G1-POST-PREREG.md`, sha256
  `0b84a1c378790e4f6c89d73db22dd4a636f2b37d72112bb6f5d204b8660bcf3a`) à `docs/G1-lot-POST-PREREG.md`, au plus tard dans
  le commit du diff 14, qui le cite.
- SHOGEN-PP-REJEU-B1-1 (G2 §6) : mesuré, rejeu identique à la tête `dad3bc6` ; l'item n'a plus d'objet si cette mesure est
  adjugée. Phrase possible, non appliquée (hors liste fermée), au README des sorties : « Rejeu à `dad3bc6` (harnais du lot
  DETTES-B1) : sorties identiques à l'octet. »
- Limite rappelée (G2 §4 et §8, non corrigée ici) : « fixés avant l'exécution » (C-4) et l'heure 04:18:36 ne sont
  attestés que par des horodatages de fichiers ; item proposé par le G2 : SHOGEN-POSTPREREG-PARAMS-SCEAU-1.
- Si la tête bouge encore : les diffs 01 à 13 ne touchent que des chemins créés par le lot (`scripts/post-s2/`,
  `docs/adr-0028/execution/post-prereg-2026-10-04/`) ; le 14 touche `docs/11` (un hunk, juste avant le §12).

## 6. Provenance

- [lu] brief PP-CORR (entier) ; brief POST-PREREG (entier) ; G2-POST-PREREG.md (entier) ; G1-POST-PREREG.md (entier) ;
  SECTION-11.md (entier) ; `G2-PP/rejeu.sh`, `G2-PP/mut/mutants_g2.py`, `G2-PP/mut/demo_survivants.py`,
  `BRIEF-G2-POST-PREREG.md` (entiers) ; `docs/adr-0028/G0-lots-DETTES.md` (entier) ; `ANNEXE-D-preenregistrement.md`
  l.1-60 (D.1, D.2 : noms des pièces, aucune ouverte) et l.120-211 ; `AVIS-SEUIL-FLUX-QUASI-MORT.md` l.1-60 et lignes
  V2, V4, L2 ; `PAQUET-PREREG-S2.md` l.211-222 (bloc machine) ; code et tests du lot (`scripts/post-s2/` : README,
  `commun.py`, `sens_pool.py`, `censure.py`, `hote_horloge.py`, leurs tests, `fixtures.py`) ; README et `SHA256SUMS` des
  sorties ; `docs/11` l.990-1047 ; `r1.py` (`_median`, `parse_journal` par diff), `records.py` (`filtre_lecture`,
  `t_fin_n_fixe`, `clock_check_record`, `parse_control`), `window.py` (spécification des strates) ; xtask `sg1`-`sg8`
  (en-têtes), `sg4.rs` l.30-101, `sg5.rs` (sélection des fragments) ; `git log`, `git diff` en lecture seule
  (`f35a70c..dad3bc6`, diffs de B1, ajouts datés de `3226dd2`) ; livrables B1 (noms de fichiers touchés seulement).
- [abs] : P-05, P-08 ; pièces de D.2 ; journaux (lus par les scripts du lot seulement) ; `docs/15-*`, `docs/16-*`,
  `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, `JOURNAL.md` : non ouverts.
- Pièces du worker (`dettes/PP-CORR/`) : `diffs/` et `diffs/SHA256SUMS` ; `outils/regen.py`, `corriger_texte.py`,
  `mutants_pp_corr.py`, `suite_par_pas.py`, `ref_c2.py`, `rejeu.sh`, `comparer_rejeu.sh` ; `journal/` (sorties des
  commandes) ; `rejeu/` (sorties rejouées, flux et codes) ; `arbre/` (copie corrigée), `tete/` (copie pristine de
  `dad3bc6`), `etats/` (états par sous-lot).
