# G1 du lot CORR (partie 4) — CORR-1, CORR-2, puis CORR-3

- **Rattachement** : G0 `docs/adr-0028/G0-lot-CORR.md` (CORR-1, CORR-2 : texte inchangé de `f6c5d83` à `e25d840` ;
  extension CORR-3 ajoutée à `1f74183`, erratum d'heure à `e25d840` ; sha256 du fichier à `e25d840` :
  `7ce75d57fdb5653326c4ba1870ead8861485eefbc967cba579e5ada455abb1f9`) ; annexe B.42 (R-B, A-1,
  SHOGEN-RECALCUL-JSON-COPIE-1), B.43 (R-A, A-1, SHOGEN-PRIX-NON-FINI-1) ; ADR-0028 D2, D.4 a et b, A-8.
- **Worker** : `claude-opus-5-5` (Gate 0 ci-dessous), effort `max` selon la fiche (réglage non observable depuis l'agent).
- **Horloge** (`date -u`) : départ 2026-10-02 22:20:08Z ; section CORR-1/CORR-2 close à 22:5xZ (heures des commandes
  au §3) ; CORR-3 de 22:56:23Z (lecture de `e25d840`) à 23:38:55Z (dernière non-régression) ; heures au §12.
- **Ordre** (message du coordinateur pendant la passe) : CORR-1 et CORR-2 d'abord (§0-§11, diffs séparés), puis les
  neuf items de CORR-3 en sous-lots R-25 empilés (§12-§22).
- **Dépôt** : `/home/user/shogen`, branche `partie-4-execution` ; HEAD `f6c5d83` au départ, `e25d840` depuis 22:2xZ
  (commits de l'orchestrateur `1f74183`, `e25d840` : `JOURNAL.md` et le G0 seuls ; `git diff --name-only f6c5d83 e25d840
  -- s2-harness scripts enforcement` vide). Aucune écriture dans le dépôt, aucune opération git en écriture ; tout le
  travail dans `scratchpad/corr/` (ci-après `corr/`).
- **Copies** : `git archive HEAD | tar -x -C corr/<copie> --exclude=docs/rapports --exclude=docs/adr-0025
  --exclude=docs/adr-0028/monark-m009a --exclude=JOURNAL.md` (exclusion à la source, écart D-6) ; `corr/base` (HEAD
  intact), `corr/arbre` (copie de travail).

## 0. Gate 0

Modèle résolu : **`claude-opus-5-5`** (identifiant exact fourni par l'environnement de la session) ; préfixe attendu des
workers (CLAUDE.md §7) : conforme.

## 1. Attestation (forme D.3) et expositions déclarées

« Le worker G1 du lot CORR (`claude-opus-5-5`) n'a vu aucun z, aucun K, aucun P̂_more ni aucun φ de campagne, et n'en a
calculé aucun ; il n'a lu aucun taux d'écart, de présence ou de panne d'une source de la campagne. Il n'a ouvert aucune
pièce de la liste fermée D.2 (n° 1 à 12, liste lue à l'annexe D l.32-47 sans en ouvrir le contenu) ; il n'a rien lu
sous `docs/rapports/` ni sous `docs/adr-0025/`, ni `JOURNAL.md`, ni aucun `*.jsonl` réel ; il n'a jamais posé
`SHOGEN_S2_CAMPAGNE_CONTROL` (variable absente de l'environnement, contrôlé par nom ; toutes les exécutions Python sous
`env -u SHOGEN_S2_CAMPAGNE_CONTROL PYTHONDONTWRITEBYTECODE=1 python3 -B`). Tous les journaux qu'il a lus ou produits sont
des fixtures de tests ou des journaux synthétiques (les siens ; ceux de R-B, `p4/R-B/small-*`, `synth-a` ; le
générateur de R-A, `p4/R-A/sondes/ref.py`). »

Expositions et écarts, déclarés :
1. Sortie d'un `grep -n "D\.2\|D\.3\|D\.4"` sur l'annexe D : lignes de l'inventaire D.1 (n° 3, 5, 10, 12 à 16) vues
   en entier ; elles décrivent des lectures (pièces, dates, classes M/R) sans porter de valeur. Lignes D.3 (h) à (j)
   (attestations) vues de même.
2. Rapports de R-A et R-B lus en entier : ils portent des résultats synthétiques et nomment des comptes de classe M
   sans les recopier ; rien de campagne n'y figure.
3. `git status --short` a montré, en noms seuls, `JOURNAL.md` et le G0 modifiés dans l'arbre de travail (commits
   `1f74183`, `e25d840` de l'orchestrateur, pendant la passe) ; `JOURNAL.md` n'a pas été ouvert ; le diff du G0 a été lu.
4. Écritures machine sans affichage : aucune ; les pièces D.2 n° 5 et 6 ne sont pas extraites (exclusion à la source).
5. Une commande sans effet, sans écriture : `git archive e25d840 | tar -x -O e25d840` (membre inexistant, rien extrait).

## 2. Sources lues

| pièce | niveau | lignes | motif |
|---|---|---|---|
| `docs/adr-0028/G0-lot-CORR.md` | [lu] | entier (à `f6c5d83`, puis l.38-61 à `e25d840`) | contrat |
| `docs/adr-0028/G2-RATTRAPAGE-R-B.md`, `G2-RATTRAPAGE-R-A.md` | [lu] | entiers | constats A-1, sondes, mutants |
| `docs/adr-0028/ANNEXE-B-items.md` | [lu] | l.547-613 (B.39-B.43) | items, rattachement |
| `docs/adr-0028/ANNEXE-D-preenregistrement.md` | [lu] | l.32-49 (D.2), sortie de `grep` (§1) | pièces interdites |
| `docs/PASSATION-CLOUD.md` | [lu] | l.97-139 (§4), en-têtes | règles |
| `s2-harness/shogen_s2/records.py`, `s2-harness/tools/rendu_unique.py` | [lu] | entiers | lecteur, rendu |
| `s2-harness/shogen_s2/r1.py` | [lu] | entier | point unique, consommateurs |
| `s2-harness/shogen_s2/r2.py` | [lu] | l.420-790, l.1000-1092 | consommateurs R2 |
| `s2-harness/shogen_s2/lm.py`, `report.py` | [lu] | lm entier ; report l.36-325 | consommateurs |
| `s2-harness/shogen_s2/journal.py`, `model.py`, `collector.py` l.130-252, `sources.py` l.80-95, l.370-402 | [lu] | | format écrit, atteignabilité |
| tests : `test_rendu_production.py`, `test_lecteur.py`, `capture.py` (entiers) ; `test_collector.py` l.1-126, l.380-460 ; `test_sensibilite.py` l.1-110 ; `test_rendu_unique.py` l.1-47 ; `test_rendu_blocs.py` l.26-157 ; `test_critere.py` l.1-60 ; `tests/__init__.py` | [lu] | | style, fixtures, aides |
| `scripts/controle/regle_fixtures.py`, `render_fixture.py`, `README.md`, `SHA256SUMS` | [lu] | entiers | non-régression |
| sondes `p4/R-B/probe_frozenset.py` (`14f6de26…b3d9`), `p4/R-A/sondes/sonde5_rendu_nan.py` (`da498b33…4aee`), `ref.py` l.1-112 (`grep`) | [lu] | | reproduction |
| `git rev-parse ed479c5:<f>` et `HEAD:<f>` pour `journal.py`, `sources.py`, `model.py` | [lu] | blobs égaux | collecte = lecteur |

## 3. Commandes et sorties (provenance)

| heure (Z) | commande | sortie |
|---|---|---|
| 22:20:08 | `date -u` | départ |
| 22:2x | `sha256sum -c scripts/controle/SHA256SUMS` (copie) | 8 fichiers OK |
| 22:23:27 | suite de référence sur `corr/base` | `Ran 383 tests in 39.856s` `OK (skipped=2)`, 0 `__pycache__` |
| 22:2x | `regle_fixtures.py corr/base/s2-harness …` ; `render_fixture.py …` | `ea3a2d94…cb29` ; `4e62fbb8…9a01`, `d079dd9d…e608` |
| 22:24:22 | `probe_frozenset.py corr/base/s2-harness p4/R-B/small-copie p4/R-B/small-temoin` | copie : `TypeError : frozenset hors du JSON du recalcul tiers` (json.dumps et `--produire recalcul-tiers`) ; témoin : code 0, 308 095 octets |
| 22:24:35 | `sonde5_rendu_nan.py corr/base/s2-harness` | NaN : `decimal.InvalidOperation`, pile `r1.py:compute_r1:566 > _classify_window:465 > classify_ecart:194 > _median:106` ; sortie identique à l'octet à `sonde5.out` de R-A (`a4be126e…4227`) |
| 22:30:00 | `explore/explore_nan.py corr/base/s2-harness` (fixture 5 flux) | NaN : exception dans r1 et r2 ; Infinity : exception dans r2 (`_jumps`), r1 sans exception ; −Infinity : aucune exception (valeurs différentes, §6) |
| 22:33:37 | tests CORR-1 seuls sur l'arbre non corrigé | §5 : 2 ERROR (`TypeError`) |
| 22:34:15 | tests CORR-2 seuls sur l'arbre non corrigé | §6 : 1 ERROR (`InvalidOperation`), 15 FAIL |
| 22:34:48 | les 4 tests après correction | `Ran 4 tests in 1.305s` `OK` |
| 22:34:56 | suite entière, arbre corrigé | `Ran 387 tests in 41.960s` `OK (skipped=2)` |
| 22:35:51 | sondes R-B et R-A sur l'arbre corrigé | copie : code 0, 308 334 octets, JSON relisible ; NaN : rendu produit, avertissement `okx_index 1` |
| 22:37 à 22:38 | `patch -p1` des diffs sur trois extractions neuves (v1, v2, v12) ; suites | 385, 385, 387 tests `OK (skipped=2)` |
| 22:38:20 | `explore/compare_sorties.py` (base, arbre) × (`small-temoin`, `small-copie`) | §7 |
| 22:41:07 à 22:44:47 | `mutants.py` (première version) | §8 ; M18 non lancé (motif présent 15 fois), corrigé, rejoué seul à 22:44:59 (tué) |
| 22:45 à 22:47 | relecture : longueurs de ligne (convention ≤ 120 caractères du dépôt, mesurée) ; 5 lignes ajoutées à 121-123 raccourcies | commentaires et docstrings seulement ; fonctionnel inchangé |
| 22:48:22 | tests finaux sur HEAD non corrigé (`corr/rouge/r1`, `corr/rouge/r2` = HEAD + un fichier de test) | rouge : §5, §6 |
| 22:48:57 | diffs finaux sur extractions neuves, suites et non-régression | §7 |
| 22:49:52 à 22:53:35 | `mutants.py` final (`8cc2e7c9…9e60`), 19 exécutions | §8 |
| 22:55:06 à 22:55:55 | sondes d'exploration rejouées sur la version finale, sorties dans `explore/out/` | §6, §7, §10 |

## 4. Travail 1 — le point unique des lectures de `journal.jsonl`

Établi par lecture (`grep -n "parse_journal\|read_jsonl_tolerant\|journal\.jsonl\|json\.loads"` et `grep -n
"price\|prix"` sur `shogen_s2/` et `tools/`, puis lecture des sites) : **`r1.parse_journal`** (`r1.py` l.396-400 à
HEAD) est le seul endroit où les lignes de `journal.jsonl` deviennent les dictionnaires consommés.

Appelants (HEAD) : R1 `r1.recompute_from_journal` l.800 (et `r1.recompute_d5_from_journal` l.827, par lui) ; L&M
`lm.recompute_lm_from_journal` l.226 ; R2 `r2.recompute_r2_from_journal` l.1077 ; rapport `report.render_report` l.162
(blocs 1 à 6 et [SENSIBILITÉ], même liste `readings`) ; hors chaîne de rendu : `closure.py` l.104 (calibration, en
quarantaine, D6 i ; jamais lancé par `rendu_unique`). `rendu_unique.produire` n'appelle que `render_report` (runs
texte) et les quatre `recompute_*` (run `recalcul-tiers`), `rendu_unique.py` l.389-407.

Sites qui consomment `price` (HEAD), tous alimentés par la liste rendue par `parse_journal` :

| site | lignes | usage |
|---|---|---|
| `r1.classify_ecart` | l.180 ; l.201 | prédicat de panne ; `Decimal(reading["price"])` |
| `r1.analysis_pools` | l.433 | ok = statut ok et prix (pool D1 ; seuil SHOGEN-FLUX-QUASI-MORT-1) |
| `r1._classify_window` | l.454-460 | répondantes ; `Decimal(...)` (médiane leave-one-out, `_median` l.102-110) |
| `r1.compute_r1` | l.572-574 ; `_ecart_relatif` l.228-234 par `rep` | ok_windows ; τ observé |
| `r2._price_at` (par `tick_identity` l.553-554) | l.461-465 | copie exacte, T, T_Δ |
| `r2.lnprice_by_window` | l.476-480 | ln p (ρ, co-aberrance, sauts) |
| `report.render_report` bloc 2 | l.302 | affichage du prix |
| `closure.py` | l.127-129 | calibration (hors rendu) |

Hors consommateurs : `records.verifier_raw` (l.129) relit `journal.jsonl` sans `parse_journal`, mais ne lit que
`window_start`, `flux_id`, `fetch_ts`, `sha256_raw` (verdict du run `raw` inchangé par CORR-2). Les tests appellent
aussi `parse_journal` (`test_collector` l.401, `test_pool_analyse` l.89, `test_poolee` l.84) ou passent des lectures
en mémoire aux `compute_*` : fixtures à prix finis, inchangées.

## 5. Sous-lot CORR-1 (SHOGEN-RECALCUL-JSON-COPIE-1)

**Test d'abord** : `s2-harness/tests/test_recalcul_json_copie.py` (neuf, 91 lignes). Fixture : collecteur réel, w = 60 s,
330 fenêtres depuis T0 = 1787770800, flux coinbase, coingecko, defillama ; prix de coingecko = defillama = 64000 +
j/100 (non constant), coinbase = ce prix + 7 ; table de fixture : j14-principal (320 fenêtres), j28 (`n_fixe` 320,
plage fermée de 10 fenêtres : 310 fenêtres communes), d'où j28-incluse (320).
- `test_recalcul_tiers_paire_copie_en_liste_triee` : `rendu_unique --produire recalcul-tiers` (en processus, jeton
  posé) : code 0, JSON relisible, clés et `avertissements` vides ; dans chaque variante, `exact_copy_pairs ==
  [["coingecko", "defillama"]]` (écrit à la main) et r1, d5, lm, r2 égaux aux quatre `recompute_*` relus par un
  convertisseur écrit dans le test (Decimal en chaîne, ensemble en liste triée) : sérialisation seule.
- `test_decimal_ensembles_en_listes_triees` : `_decimal(frozenset)` et `_decimal({8, 1})` en listes triées (sous
  CPython, `{8, 1}` s'itère 8 puis 1 : `list()` rougit sans dépendre du hachage des chaînes), Decimal en chaîne, autres
  types (`object()`, `bytes`, `complex`) : `TypeError` nommé.

**Rouge avant** (tests finaux sur HEAD, `corr/rouge/r1`, log `rouge-final-corr1.log` `d312e3e8…ff93`) : `Ran 2 tests`
`FAILED (errors=2)`, les deux en `TypeError: frozenset hors du JSON du recalcul tiers` (`rendu_unique.py` l.366 par
l.411).

**Correction** (`rendu_unique.py`, 3 lignes ajoutées, 1 retirée) :
```python
def _decimal(x) -> str | list:
    ...
    if isinstance(x, (set, frozenset)):
        return sorted(x)                                # r2, copie exacte : liste triée (SHOGEN-RECALCUL-JSON-COPIE-1)
    raise TypeError(...)
```
**Vert après** : les deux tests OK ; suite §7. sha256 de `rendu_unique.py` corrigé : `5babbd53…285b` (HEAD :
`67b897a9…f8d9`) ; `sha256_script` du bloc machine change donc (suite du G0 : nouveau bloc).

## 6. Sous-lot CORR-2 (SHOGEN-PRIX-NON-FINI-1)

**Test d'abord** : `s2-harness/tests/test_prix_non_fini.py` (neuf, 121 lignes). Fixture : collecteur réel, cinq flux
(coinbase, kraken, bitstamp, bitfinex, gemini ; lectures gelées), w = 60 s, 100 fenêtres de part et d'autre du samedi
2026-08-08 00:00Z (calme, stress) ; coinbase en panne aux rangs multiples de 3, kraken aux rangs impairs ; table de
fixture j14-principal (80 fenêtres), j28 (`n_fixe` 90, plage fermée des rangs 20 à 24). Variante A : lectures ok
(rang 10, bitfinex) « NaN », (60, gemini) « Infinity », (70, bitfinex) « NaN » ; variante B : les mêmes à `null` ; le
reste à l'octet. Aux rangs 10 et 70, cinq flux répondent, au rang 60 quatre : la médiane leave-one-out est atteinte.
- `test_rendu_et_recalcul_comme_prix_null` : `--produire` j14-principal, j28, recalcul-tiers sur A et B : code 0 ; sortie
  texte de A = celle de B avec une ligne `[AVERTISSEMENT DU LECTEUR] [s2-harness] AVERTISSEMENT : prix non fini(s) lu(s)
  comme absent(s) dans journal.jsonl, fichier entier — par flux : bitfinex 2, gemini 1 (SHOGEN-PRIX-NON-FINI-1 : panne
  au sens de classify_ecart ; valeurs non reproduites).` après l'étiquette ; JSON de A = JSON de B hors
  `avertissements` (douze fois la ligne pour A : quatre lectures par variante, trois variantes ; vide pour B) ; au bloc
  R1 du J28, panne = 1 pour (calme, bitfinex), (stress, bitfinex), (stress, gemini) (comptes écrits à la main).
- `test_formes_lues_comme_absentes_ou_inchangees` : `r1.parse_journal` sur une ligne, sous-tests : 14 formes non finies
  (`"NaN"`, `"nan"`, `"-NaN"`, `"sNaN"`, `"-sNaN"`, `"NaN12"`, `" nan "`, `"Infinity"`, `"-Infinity"`, `"inf"`,
  `"+INF"`, jetons JSON `NaN`, `Infinity`, `-Infinity`) et `"NaN"` sur une lecture `panne_http` : prix `None`,
  avertissement « x 1 » (texte entier comparé) ; 8 formes inchangées sans avertissement : `"64475.75"`, `"-0"`, `"1E+2"`,
  `3`, `1.5` (Decimal), `null`, `"abc"`, `[1]`.

**Rouge avant** (tests finaux sur HEAD, `corr/rouge/r2`, log `rouge-final-corr2.log` `bfbf3dc0…6f3b`) : `Ran 2 tests`
`FAILED (failures=15, errors=1)` : l'intégration lève `decimal.InvalidOperation` à `s = sorted(values)` (`_median`), les
15 sous-tests non finis rendent le prix brut sans avertissement. Rouge par valeur sur la fixture du test
(`explore/rouge_par_valeur.py`, sortie `rouge_par_valeur-r2.out` `34d3fa78…dcdd9`) : NaN seul → `InvalidOperation` dans
`r1.classify_ecart:194 > _median:106` (j28 et recalcul-tiers) ; Infinity seul → `InvalidOperation` dans
`r2.delta_direction:676 > _jumps:663` ; −Infinity seul → aucune exception mais sortie différente (75 451 octets contre
75 774 après correction).

**Correction** (`r1.py`, 20 lignes ajoutées, 2 retirées : `import sys` ; `parse_journal`) : sous le contexte nommé
(`contexte_decimal()`, qui piège `InvalidOperation` : une chaîne illisible lève et reste inchangée, jamais lue NaN),
toute ligne dict dont `price` n'est pas `None` et dont `Decimal(price)` n'est pas fini reçoit `price = None` ; compte
par `flux_id` ; si au moins un, une ligne sur `stderr` (texte ci-dessus, chemin du fichier tel que passé ; `rendu_unique`
le réécrit sans dossier). Exceptions de `Decimal(...)` (`TypeError`, `ValueError`, `ArithmeticError`) : ligne
inchangée. sha256 de `r1.py` corrigé : `acbafc4d…2f7d` (HEAD : `79186890…db5e`).

**Vert après** : les deux tests OK ; rouge par valeur rejoué sur l'arbre corrigé (`rouge_par_valeur-arbre.out`) :
toutes les variantes code 0, Infinity et −Infinity donnent la même sortie (75 774 et 108 150 octets).

**Équivalence avec `null` hors des fixtures du lot** (générateur de R-A, 12 flux, 900 fenêtres, graine 5, segment
`n_fixe` 800, plage) : `explore/nan_null_ra.py` (okx_index « NaN », gemini « −Infinity ») : HEAD lève dans les quatre
chemins ; corrigé : rendu, r1, lm, r2 égaux à la variante `null`, quatre avertissements « gemini 1, okx_index 1 ».
`explore/minf_null_ra.py` (gemini « −Infinity » seul) : HEAD **sans exception mais différent** de `null` (4 lignes du
rendu ; r1 calme gemini : panne 8, hors-enveloppe 4, ok 741 contre 9, 3, 740) ; corrigé : égal.

## 7. Non-régression (CORR-1, CORR-2)

- Diffs appliqués par `patch -p1` sur des extractions neuves de HEAD : v1 (CORR-1), v2 (CORR-2), v12 (les deux) ; v12 =
  `corr/arbre` alors (`diff -rq` vide sur `s2-harness`) ; aucun `.orig` ni `.rej`. Les deux diffs s'appliquent aussi à
  `e25d840` (vérifié : `corr/verif-e25`, égal à `corr/arbre`).
- Suite entière : v1 `Ran 385 tests in 39.839s OK (skipped=2)` ; v2 `Ran 385 tests in 39.773s OK (skipped=2)` ; v12
  `Ran 387 tests in 41.017s OK (skipped=2)` (référence HEAD : 383). 0 `__pycache__` dans toutes les copies.
- `regle_fixtures.py` sur v1, v2, v12 : sha256 du JSON `ea3a2d94ef1075603e8f7cfc53c68b26e51729b61714028e3fb03dc32f79cb29`
  ; sortie imprimée identique à celle de HEAD (`cmp`).
- `render_fixture.py` sur v1, v2, v12 : `4e62fbb8a4a7a29c0761c719c8f731a8247ef407be7a7a04c44219bd093c9a01`,
  `d079dd9d62a3f585a136779330cb21017a300ae853bef5cb63024bb6412de608`.
- Sorties de production sur journaux synthétiques de R-B (12 flux, 338 fenêtres ; table de fixture de la sonde R-B) :
  `small-temoin` : j14-principal, j28, recalcul-tiers, raw **identiques à l'octet** entre HEAD et l'arbre corrigé ;
  `small-copie` : j14-principal, j28, raw identiques ; recalcul-tiers : HEAD `TypeError`, corrigé code 0, 308 334
  octets ; son JSON égal, variante par variante, aux quatre `recompute_*` **de HEAD** relus par un convertisseur
  indépendant (`explore/serialisation_seule.py`) : sérialisation seule.
- Coût de lecture (`synth-a` de R-B, 481 920 lectures, 141 Mo) : `parse_journal` 6,02 et 5,66 s (HEAD) contre 6,56 et
  5,42 s (corrigé) ; RSS max 1 070 Mio dans les deux cas : différence dans le bruit (information pour
  SHOGEN-RENDU-COUT-1).

## 8. Mutants (CORR-1, CORR-2)

Copie neuve de l'arbre corrigé par mutant, une substitution (motif présent une fois), suite complète ; mort = code ≠ 0.
Script `mutants.py` `8cc2e7c9…9e60`, exécution finale 22:49:52-22:53:35Z, résultats `mut/mut-res.json` `46c596e4…2eb8`.

| id | mutation | résultat | tué par |
|---|---|---|---|
| M00 | témoin | vit (387, OK) | — |
| M01 | ensembles refusés (HEAD) | tué (2 E) | les deux tests CORR-1 |
| M02 | `list()` au lieu de `sorted()` | tué (1 F) | `test_decimal_ensembles_en_listes_triees` (l'intégration seulement selon le hachage) |
| M03 | frozenset seul | tué (1 E) | `test_decimal_…` |
| M04 | ordre décroissant | tué (4 F) | les deux tests CORR-1 |
| M05 | refus des autres types retiré | tué (3 F) | `test_decimal_…` |
| M06 | aucune requalification | tué (15 F, 1 E) | les deux tests CORR-2 |
| M07 | avertissement retiré | tué (18 F) | les deux tests CORR-2 |
| M08 | compte total seul | tué (18 F) | les deux tests CORR-2 |
| M09 | prix remplacé par « 0 » | tué (18 F) | les deux tests CORR-2 |
| M10 | chaînes seules | tué (3 F) | `test_formes_…` |
| M11 | libellés exacts | tué (10 F) | `test_formes_…` |
| M12 | NaN seul | tué (6 F, 1 E) | les deux tests CORR-2 |
| M13 | statut ok exigé | tué (1 F) | `test_formes_…` |
| M14 | illisible lu comme absent | tué (2 F) | `test_formes_…` |
| M15 | zéro lu comme absent (`is_normal`) | tué (1 F) | `test_formes_…` |
| M16 | flux sans compte | tué (18 F) | les deux tests CORR-2 |
| M17 | requalification au seul `r1.recompute_from_journal` (point non unique) | tué (15 F, 1 E) | les deux tests CORR-2 |
| M18 | contexte sans pièges | tué (1 F) | `test_formes_…` |

Chaque test neuf tue au moins un mutant ; 18 mutations, 18 tuées. Première série (même script avant la correction du
motif de M18, 22:41-22:44Z) : mêmes verdicts M00-M17 ; elle n'est pas la référence.

## 9. Écarts et interprétations (CORR-1, CORR-2)

- **D-1 (règle sans condition de statut)** : la requalification porte sur tout prix non fini, quel que soit le statut
  (G0 : « un prix non fini est traité comme un prix absent » ; la portée « une lecture ok » est celle du défaut). Effet
  sur une lecture non ok : affichage du bloc 2 (« - » au lieu de la valeur, comme `null`) et compte de
  l'avertissement ; aucun effet sur R1, L&M, R2 (statut ≠ ok = panne). Le collecteur n'écrit jamais de prix sur une
  lecture non ok ([lu] `sources.read` l.378-402, `journal.journal_entry` l.42 ; blobs égaux à `ed479c5`). Le mutant M13
  (statut ok exigé) est tué par le cas `panne_http`. Question Q-1.
- **D-2 (prix illisible)** : un prix que `Decimal` ne lit pas (`"abc"`, liste) reste inchangé (hors de la liste fermée)
  ; le contexte nommé est posé pour que ce cas ne devienne jamais NaN (M18). Limite L-1.
- **D-3 (portée et multiplicité de l'avertissement)** : compte sur le fichier entier (avant segment, exclusion et
  « dernier de la fenêtre »), une ligne par appel de `parse_journal` : une par run texte, quatre par variante du
  recalcul tiers (seize en production, quatre variantes), comme l'avertissement de ligne tronquée de
  `read_jsonl_tolerant`.
- **D-4 (closure.py)** : la calibration en quarantaine lit par `parse_journal` ; la règle s'y applique aussi. Hors des
  runs de l'exécution unique ; `test_closure` inchangé et vert.
- **D-5 (annotation)** : `_decimal(x) -> str` devient `-> str | list` (ligne modifiée, annotation exacte).
- **D-6 (copies)** : exclusion à la source de `docs/rapports`, `docs/adr-0025`, `docs/adr-0028/monark-m009a`,
  `JOURNAL.md` (serrage du `git archive HEAD | tar -x` du brief) ; la suite n'en dépend pas (vérifié : vert).
- **D-7 (R-25)** : 236 lignes ajoutées en tout, donc deux diffs : `corr-1.diff` (94 ajoutées, 1 retirée), `corr-2.diff`
  (142 ajoutées, 2 retirées), indépendants (fichiers disjoints) ; `corr.diff` = leur concaténation, pour référence.
- **D-8 (texte du bloc 3)** : la définition imprimée « panne = lecture absente, statut ≠ ok ou prix absent » n'est pas
  modifiée (elle changerait les rendus épinglés) ; l'avertissement porte l'information ; la mention datée de CORR-2 au
  paquet révisé (G0, « Suite ») la complète.

## 10. Limites rendues comme items (règle PAROXYSME ; propositions, propriétaire : orchestrateur)

Mesurées par `explore/limites.py` (fixture CORR-2 ; sorties `limites-r2.out` sur HEAD, `limites-arbre.out` corrigé :
identiques au numéro de ligne près) :
- **L-1, SHOGEN-PRIX-ILLISIBLE-1** : prix illisible par `Decimal` (`"abc"`) → `decimal.InvalidOperation` non nommée dans
  `_classify_window` (avant et après CORR-2). Inatteignable depuis le collecteur (prix écrit `str(Decimal)` ou `null`)
  [lu]. Déclencheur proposé : après S2.
- **L-2, SHOGEN-PRIX-HORS-CONTEXTE-1** : prix fini d'exposant au-delà d'Emax du contexte nommé (`"1E+1000000"`) →
  `decimal.Overflow` non nommée dans `classify_ecart` (avant et après). Atteignable seulement si une API servait un tel
  nombre (`_loads` lit tout nombre en Decimal) ; plausibilité très faible [inféré]. Déclencheur proposé : après S2.
- **L-3, SHOGEN-SOURCE-TS-NON-FINI-1** : `source_ts` jeton JSON NaN → `decimal.InvalidOperation` dans `classify_ecart`
  (l.189). Inatteignable depuis le collecteur : toute `source_ts` y est dérivée par `int(...)`, `float(int(...))` ou
  `_iso_to_epoch` ([lu] `sources.py` l.132-216). À clore sans code si l'orchestrateur accepte la preuve d'inatteignabilité.

## 11. Livrables CORR-1, CORR-2 (dans `corr/`)

| fichier | sha256 |
|---|---|
| `corr-1.diff` (CORR-1 : `rendu_unique.py`, `tests/test_recalcul_json_copie.py`) | `8dd2741548a72b60d33f99ec1efa4d928126eccbd6a95c64dd7c2aa0bdd1b252` |
| `corr-2.diff` (CORR-2 : `r1.py`, `tests/test_prix_non_fini.py`) | `0847c663e60f7ce26c44d7d301228585ea37fdd54d785745ba25fb303e785240` |
| `corr.diff` (concaténation, référence) | `3c4cfa1bf2d6a28d72f08bb46adfc31e19b2d73b428d28ea54704eaa04e668ba` |
| `tests/test_recalcul_json_copie.py` ; `tests/test_prix_non_fini.py` (dans l'arbre corrigé) | `0f5a0f4f…9fb4` ; `100ea741…b876` |
| logs : `rouge-final-corr1.log`, `rouge-final-corr2.log`, `verif/suite-v1.log`, `-v2`, `-v12`, `suite-base.log` | `d312e3e8…ff93`, `bfbf3dc0…6f3b`, `6df04b64…6039`, `19f7e88b…fe4b`, `86ded9a0…527e`, `c02c7c03…9b86` |
| `mutants.py`, `mut/mut-res.json`, `mut-log-final.txt` | `8cc2e7c9…9e60`, `46c596e4…2eb8`, `7c7dca4a…7c78` |
| sondes rejouées : `sondes/probe_frozenset-{base,corr}.out`, `sondes/sonde5-{base,corr}.out` | `956a0304…7763`, `9c29d200…1411`, `a4be126e…4227`, `06754b37…7501` |
| exploration : `explore/*.py` et `explore/out/*.out` | §22 |

## 12. CORR-3 — sources, plan, commandes

Sources lues, toutes [lu] : G0 l.38-61 à `e25d840` (sha256 `7ce75d57…b1f9`) ; `docs/adr-0028/G2-RATTRAPAGE-R-C.md` entier
(H-1, B-1, C-2, C-3 ; mutants M24, M29, M30) ; `docs/G2-partie-3.md` l.128-147 et l.262-321 (C-1 : texte du test, mutants
M4, M4b) ; annexe B l.466-480 (B.32) et l.505-522 (B.35) ; `PAQUET-PREREG-S2.md` l.109-118 et l.170 (§10.2 pt 3, §10.4),
lignes d'un `grep « Künsch »` (coupées à 250 caractères) et en-têtes ; `biblio/INDEX.md` l.336 (Künsch 1989 versé ;
`biblio/kunsch1989-aos-17-3-1217.pdf` mesuré : sha256 `6d069c52…3a64`, égal à l'index) ; ADR-0028 l.184-190 (D6 i) et lignes d'un `grep D6|quarantaine` ; scripts de mutants des réviseurs,
sha égaux à ceux de leurs rapports : `p4/R-B/mutants.py` `68468c58…83dd`, `p4/R-A/sondes/mutants.py` `bbdd41ae…d8e4`,
`p4/R-C/mutants/liste.py` `c675b42c…3280` ; code : `oracle_record.py` l.1-60, l.180-274 ; `r2.py` l.1-60, l.220-240,
l.343-420, l.770-1000 ; `report.py` l.325-787 ; `lm.py` l.28-35, l.166-170 ; `records.py` l.1-48 ; `model.py` l.1-10 ;
`r1.py` l.320-331, l.696-706 ; `scripts/sceau/verify.sh` entier ; tests : `test_sceau.py` l.1-97, `test_oracle_record.py`
l.1-66 et l.117-164, `test_critere.py` l.60-110, l.192-215, l.270-445, `test_r1.py` l.1-135, l.225-310 et fin,
`test_r2.py` l.78-85 et l.287-360, `test_pool_analyse.py` l.40-140, `test_exclusion.py` l.20-86, `tests/__init__.py`.

Sous-lots, chacun appliqué sur le précédent (états figés `snap/e0` = HEAD + CORR-1 + CORR-2, puis `e3a` à `e3d`) :

| sous-lot | items | fichiers | lignes ajoutées / retirées | diff (sha256) |
|---|---|---|---|---|
| corr-3a | SCEAU-VERIFY-REQUETE-1, TESTS-C8-SUITE-1, TESTS-HOTE-DEUX-FLUX-1, TESTS-BORDS-R1-1 (tests seuls) | `test_sceau.py`, `test_oracle_record.py`, `test_lecteur.py`, `test_r1.py`, `test_hote_deux_flux.py` (neuf) | 122 / 0 | `c658037514cf289ce7df4d8638e5b665b26f818caa64bb16ea7ce2a4e5ba6da8` |
| corr-3b | RENDU-MKDTEMP-1, RAW-CHEMIN-1 | `rendu_unique.py`, `test_rendu_production.py` | 37 / 6 | `c0043861f526951d307b7a52ea7ba2640e8e875f4c8d02aac1ccc8fc690bc54d` |
| corr-3c | R1-DOCSTRINGS-1 ; commentaires et libellés (C-3, C-5 de R-A ; C-4 de R-B) | `r1.py`, `records.py`, `model.py`, `r2.py`, `lm.py`, `report.py`, `test_pool_analyse.py` | 29 / 16 | `2579c2d7663c1547241f0e1e103da6d700ea374d3cfd6f2c2278d5c9712ebf8c` |
| corr-3d | ASN-DIVERGENCE-ECHEC-1 | `r2.py`, `test_r2.py` | 23 / 4 | `d19ee0a87972570c807a0f9d5b115ce0807f7d9403609e52faf5b7e031e24733` |

Commandes (toutes sous `env -u SHOGEN_S2_CAMPAGNE_CONTROL PYTHONDONTWRITEBYTECODE=1 python3 -B`) :

| heure (Z) | commande | sortie |
|---|---|---|
| 22:56:23 | `git rev-parse HEAD`, `git log f6c5d83..HEAD`, `git diff --name-only f6c5d83 HEAD -- s2-harness scripts enforcement` | `e25d840` ; 2 commits de documents ; 0 fichier de code |
| 22:5x | `patch -p1` de `corr-1.diff`, `corr-2.diff` sur une extraction de `e25d840` | égale à `corr/arbre` |
| 23:06:33 | état `snap/e0` figé | — |
| 23:08:24 | tests de 3a sur `e0` + tests | 8 tests OK |
| 23:09:03-23:11:19 | `mutants3.py snap/e0 … e0` (11 mutants + témoin) | tous **vivants** (387 OK chacun) |
| 23:11:24-23:13:49 | même série sur `e0` + tests de 3a | 11 **tués**, témoin vivant (393 OK) |
| 23:14:10 | `nonreg.sh snap/e3a` | 393 OK (2 sauts) ; `ea3a2d94…` ; `4e62fbb8…`, `d079dd9d…` |
| 23:15:38 | tests de 3b avant correctif | rouge (1 ERROR, 1 FAIL) |
| 23:16:16 | après correctif | vert |
| 23:16:56-23:18:21 | mutants 3b ; `nonreg.sh snap/e3b` | 3 tués, 1 équivalent ; 395 OK ; règle et épingles inchangées |
| 23:19:54 | test du libellé (3c) avant correctif | rouge (1 FAIL) |
| 23:2x | AST hors docstrings, `e3b` → `e3c` | égal pour `r1`, `records`, `model`, `r2`, `lm` ; `report` diffère (libellé) |
| 23:21:16-23:21:59 | mutants 3c ; `nonreg.sh snap/e3c` | 2 tués ; 395 OK ; règle et épingles inchangées |
| 23:23:16 | test ASN (3d) avant correctif | rouge (6, puis 7 fausses divergences avec h3) |
| 23:24:15-23:25:41 | mutants 3d ; `nonreg.sh snap/e3d` | 4 tués ; 396 OK ; règle et épingles inchangées |
| 23:2x | `explore/asn_rendu.py` sur `e3c` et `e3d`, `diff` | §16 |
| 23:27:45-23:31:31 | `mutants.py` (série CORR-1/CORR-2) sur l'état final | 18 tués, témoin vivant (396 OK) |
| 23:31:35-23:36:10 | `mutants3.py` (série CORR-3 entière) sur l'état final | 20 tués, 1 équivalent (3b-M3), témoin vivant |
| 23:36 à 23:38:55 | docstring de Künsch reformulée (§15) ; états `e3c`, `e3d` mis à jour ; chaîne des six diffs rejouée sur `e25d840` ; `nonreg.sh` sur `e3c`, `e3d` | chaîne : 0 écart à chaque état ; 395 et 396 OK ; règle et épingles inchangées |

## 13. Sous-lot 3a — tests seuls

- **SHOGEN-SCEAU-VERIFY-REQUETE-1** : `test_verify_lie_le_jeton_a_la_requete` inséré **tel quel** après la l.93 de
  `tests/test_sceau.py` : 13 lignes extraites de `docs/G2-partie-3.md` l.296-308, retrait de l'indentation de liste de 4
  espaces seulement (`c1-bloc.txt`, sha256 `585d05aa…e265`).
- **SHOGEN-TESTS-C8-SUITE-1** : (i) `test_oracle_record.test_verifier_un_refus_nomme_par_controle` : un cas ajouté à la
  table des refus, enregistrement à six runs dont le premier n'est pas `suite` (`runs[0]["nom"] = "raw"`) → refus
  `runs` ; (ii) `test_lecteur.TestTsNumerique.test_trois_champs_sous_segment_ou_plage_seule` : `window_start`
  (window_close), `harness_ts` (clock_check), `ts` (asn_attribution), valeurs `true`, `NaN`, `"1787770900"`, sous segment
  et sous plage seule → refus nommé SHOGEN-BLOC6-TS-NUM-1.
- **SHOGEN-TESTS-HOTE-DEUX-FLUX-1** : `tests/test_hote_deux_flux.py` (neuf, 73 lignes). Collecteur réel, J1 de
  `test_critere` (`deux(25, 29)`) sur coinbase, kraken, okx_ticker, okx_index (trois hôtes), 200 + 200 fenêtres, ℓ = 1
  par la couture de B-DEP-2. (i) un AS par hôte : drapeau 2 LEVÉ, k_eff 3 = k nominal 3, k nominal_s {calme : 4, stress :
  4} ; énoncé REJETTE « k nominal_s = 4 flux » ; ligne d'entrées « … = 3 ; … « calme » = 4, « stress » = 4 — comparaison
  hétérogène déclarée … » ; (ii) coinbase et kraken sur un même AS, www.okx.com discordant : ÉTEINT, k_eff ≤ 2 (borne
  supérieure) < 3, raison exacte écrite à la main.
- **SHOGEN-TESTS-BORDS-R1-1** : `test_r1.TestBordsR1` : âge win_end − source_ts = σ = 60 → pas de staleness (N = 3 : non
  évaluable), 61 → staleness ; 40 fenêtres, trois flux chacun 20 fois en panne : P̂_more = 1/2, garde = 10 exactement,
  K = 20, z = 0 publié (valeurs à la main).

Preuve « mutant vivant avant, tué après » (`mutants3.py`, logs `mut3/log-e0.txt` `d22cadb2…e3189`,
`mut3/log-e3a.txt` `64c07f05…abf7`) :

| mutant (origine) | mutation | sur `e0` | avec 3a | tué par |
|---|---|---|---|---|
| RC-M24 | `noms[1:] == list(PRODUCTION)` | vit | tué | `test_verifier_un_refus_nomme_par_controle` |
| RC-M29 | contrôle C-8 sous segment seulement | vit | tué | `test_trois_champs_sous_segment_ou_plage_seule` |
| RC-M30 | contrôle C-8 sur `ts` seulement | vit | tué | même test |
| RB-M01 | borne supérieure ⇒ NON ÉVALUABLE même si k_eff < k nominal | vit | tué | `test_eteint_borne_superieure_sous_k_nominal` |
| RB-M03b | k nominal du drapeau 2 en flux des clusters | vit | tué | les deux tests de `test_hote_deux_flux` |
| RB-M06 | « comparaison hétérogène » seulement si k nominal_s < k nominal | vit | tué | `test_leve_k_nominal_en_hotes_k_nominal_s_en_flux` |
| RB-M15 | énoncé REJETTE : k nominal_s en hôtes | vit | tué | même test |
| RA-M1 | staleness `>=` σ | vit | tué | `test_staleness_egale_a_sigma_pas_d_ecart` |
| RA-M4 | garde `<=` 10 | vit | tué | `test_garde_egale_a_10_z_publie` |
| P3-M4 | `verify.sh` l.15 (`-queryfile`) retirée | vit | tué | `test_verify_lie_le_jeton_a_la_requete` |
| P3-M4b | écart `-queryfile` ignoré (`\|\| true`) | vit | tué | même test |

Non-régression de 3a : `Ran 393 tests in 45.212s OK (skipped=2)` ; règle `ea3a2d94…` ; épingles `4e62fbb8…`,
`d079dd9d…` ; 0 `__pycache__`.

## 14. Sous-lot 3b — `rendu_unique.py` (SHOGEN-RENDU-MKDTEMP-1, SHOGEN-RAW-CHEMIN-1)

- **Tests d'abord** (`tests/test_rendu_production.py`) : `TestProduction.test_parent_de_la_sortie_absent` (dépôt jetable
  `monter`, go épinglé, runs factices ; `--sortie <parent absent>/sortie`) : code 1, « gardes levées » seul sur la sortie
  standard, « rendu_unique : échec de production à <heure> : FileNotFoundError : … » sur stderr, aucun run, parent
  toujours absent ; `TestSortiesNommees.test_raw_refus_sans_chemin_des_journaux` : `raw.jsonl` à ligne 2 coupée, mêmes
  journaux dans deux dossiers : deux sorties identiques, verdict écrit à la main « refus — ligne JSON corrompue NON finale
  dans raw.jsonl (ligne 2) : recalcul impossible (fail-closed) ».
- **Rouge** (`rouge-corr3b.log` `e628dd0e…7450`) : `FileNotFoundError` non rattrapée
  (`…/absent/.sortie.y00f2qey`) ; verdict portant `dans /tmp/s2suite_…/raw.jsonl`.
- **Correctifs** : `mkdtemp` dans le `try` (`tmp` initialisé à `None` ; le `finally` ne retire `tmp` que s'il existe) ;
  verdict de refus réécrit par le même `replace(os.path.join(a.journaux, ""), "")` que les avertissements ; docstring de
  `produire` complétée d'une phrase.
- **Vert**, puis mutants : 3b-M1 (`mkdtemp` hors du `try`, forme de HEAD) tué par `test_parent_de_la_sortie_absent` ;
  3b-M2 (verdict avec le chemin) et 3b-M4 (réécriture sans le séparateur final) tués par
  `test_raw_refus_sans_chemin_des_journaux` ; **3b-M3** (garde `tmp is not None` retirée) **vit : équivalent**,
  `shutil.rmtree(None, ignore_errors=True)` est sans effet sous Python 3.11.15 (vérifié) ; la garde est gardée pour la
  lisibilité et contre une autre version de Python.
- Non-régression : `Ran 395 tests OK (skipped=2)` ; règle et épingles inchangées.

## 15. Sous-lot 3c — docstrings, commentaires, libellé

- **SHOGEN-R1-DOCSTRINGS-1** : `block_long_run_variance` : « Künsch 1989 (P-01, OCR seul, [2nd]) » devient « Künsch 1989
  (P-01, versé et lu : Thm 3.1, éq. (3.9), p. 1224 ; avec ces γ̂_k centrés sur Ī, correspondance par les poids, approchée
  : paquet §10.4) » [sources : paquet l.117 et l.170, `biblio/INDEX.md` l.336] ; `regle_critere` : texte normatif = « le
  paquet de pré-enregistrement scellé, docs/adr-0028/PAQUET-PREREG-S2.md §10.2, pts 1-11 (recopie d'ADR-0028 §1 bis.1) ».
  Première formulation (« correspondance des poids seulement ») corrigée à la relecture contre le paquet l.170
  (« porte sur les poids et n'est qu'approchée »).
- **Commentaires** : `records.py` l.10 (quatre types, `asn_attribution` nommé) et l.41-42 (entrées de `compute_r1` : les
  cinq premiers, `seuil_historique_valeur`, `n_min_hors_enveloppe` ; `decimal_prec` n'en est pas une) ; `model.py`
  (module de la collecte en quarantaine, D6 i, dont `Status` est lu par le recalcul) ; `r2.py` docstring du module
  (drapeau 2 selon la règle, pt 10) ; `lm.py` l.33-34 et l.168 (C(N,2) paires, sans nombre).
- **Preuve « texte seulement »** : AST des modules, docstrings retirées, égal entre `e3b` et `e3c` pour `r1`, `records`,
  `model`, `r2`, `lm`.
- **Libellé du bloc 4** (`report.py`, C-4 de R-B) : « N = … flux (pool d'analyse, ADR-0028 D1) » quand le pool d'analyse
  diffère du pool configuré sans cas (b) ; « (pool) » inchangé sinon (épingles intactes). Test d'abord :
  `test_pool_analyse.test_a_flux_mort_partout_hors_r1_lm_r2_aux_quatre_points` exige la nouvelle ligne et garde l'égalité
  de tout le reste du rendu (à partir du bloc 3) avec la collecte sans le flux, cette ligne seule normalisée ; rouge
  avant (`rouge-corr3c.log` `11245c13…0b97`), vert après. Mutants : 3c-M1 (libellé retiré) tué par ce test ; 3c-M2
  (libellé partout) tué par ce test et les deux tests d'épingle.
- Non-régression : `Ran 395 tests OK (skipped=2)` ; règle et épingles inchangées (aucune fixture épinglée n'a de retrait
  D1).

## 16. Sous-lot 3d — SHOGEN-ASN-DIVERGENCE-ECHEC-1

- **Règle appliquée** : une divergence se constate entre deux relevés **complets** d'un hôte (statut ok, RIPEstat et
  Cymru non muets), le second comparé au dernier relevé complet précédent ; un relevé en échec ou à base muette n'est ni
  une divergence ni la référence de la suivante ; `by_host` (dernier relevé par hôte, k_eff et drapeau 2) inchangé.
- **Test d'abord** (`test_r2.TestAsnPartition.test_echec_et_base_muette_ne_sont_pas_des_divergences`) : h0 ok → échec →
  ok (même AS) ; h1 ok → base muette → ok ; h2 ok(3) → échec → ok(4) ; h3 ok → échec. Attendu à la main : une seule
  divergence (h2 : (3, 3, 1.0) → (4, 4, 3.0)) ; k_eff 4, borne supérieure, non attribué ["h3"]. Rouge sur le code d'avant
  (sept fausses divergences ; `rouge-corr3d.log` `2a3bcc3e…288a`), vert après.
- **Mutants** : 3d-M1 (référence = dernier relevé quel qu'il soit), 3d-M2 (relevés incomplets admis), 3d-M3 (base muette
  admise), 3d-M4 (k_eff lu sur le dernier relevé complet) : tués par ce test.
- **Rendus** : la fixture des épingles n'a aucun relevé ASN : épingles inchangées, aucun ré-épinglage. Diff textuel d'un
  rendu synthétique dédié (`explore/asn_rendu.py` `d6aa2294…225d` : trois sondes, kraken en échec puis bitstamp à base
  muette, coinbase changeant d'AS ; sorties `asn_rendu-e3c.txt` `6f163fe5…25b7`, `asn_rendu-e3d.txt` `5f383a42…a008`,
  `diff-asn-rendu.txt` `3479d11d…0383`), lu : **quatre lignes « DIVERGENCE ASN » retirées** (kraken ×2, bitstamp ×2),
  la ligne du vrai changement de coinbase gardée, aucune autre ligne changée.
- Non-régression : `Ran 396 tests OK (skipped=2)` ; règle et épingles inchangées.

## 17. État final et non-régression du lot

| état | contenu | suite | règle | épingles |
|---|---|---|---|---|
| HEAD (`f6c5d83` = `e25d840` pour le code) | — | 383 OK (2 sauts) | `ea3a2d94…` | `4e62fbb8…`, `d079dd9d…` |
| v1 | + CORR-1 | 385 OK | idem | idem |
| e0 | + CORR-2 | 387 OK | idem | idem |
| e3a | + 3a | 393 OK | idem | idem |
| e3b | + 3b | 395 OK | idem | idem |
| e3c | + 3c | 395 OK (`nonreg/e3c/suite.log` `feedfa10…b3fd`) | idem | idem |
| e3d (final) | + 3d | 396 OK (`nonreg/e3d/suite.log` `6d186229…d2ed6`) | idem | idem |

Chaîne : les six diffs appliqués dans l'ordre (`patch -p1`) sur une extraction neuve de `e25d840` reproduisent chaque
état (0 écart, aucun `.orig` ni `.rej`). 0 `__pycache__` dans toutes les copies. Dépôt : HEAD `e25d840`,
`git status --short` vide, aucun `__pycache__` sous `s2-harness/shogen_s2` ni `s2-harness/tools`.

## 18. Mutants de l'état final

- Série CORR-1/CORR-2 (`mutants.py` `8cc2e7c9…9e60`, `mutf/log-corr12-final.txt` `f16a0772…790f`) : témoin vivant (396
  OK), **M01 à M18 tués**.
- Série CORR-3 (`mutants3.py` `338fcd38…2d94`, version finale ; `mutf/log-corr3-final.txt` `73bd558b…8d98`,
  `mutf/res-final.json` `681aa698…cc1d`) : témoin vivant ; RC-M24, RC-M29, RC-M30, RB-M01, RB-M03b, RB-M06, RB-M15,
  RA-M1, RA-M4, P3-M4, P3-M4b, 3b-M1, 3b-M2, 3b-M4, 3c-M1, 3c-M2, 3d-M1 à 3d-M4 **tués** (20) ; 3b-M3 **vivant,
  équivalent** (§14).
- Ces deux séries ont tourné avant la reformulation de la docstring de Künsch (§15) ; l'AST hors docstrings de `r1.py`
  est inchangé par cette reformulation, et la suite a été rejouée après (396 OK).
- Chaque test neuf ou modifié du lot tue au moins un mutant.

## 19. Écarts et interprétations (CORR-3)

- **D-9 (portée de C-4 de R-B)** : la colonne « construction » du G0 nomme `records.py`, `model.py` et `report.py` ;
  l'item nomme « C-4 de R-B », qui couvre aussi `r2.py` l.45-48 et `lm.py` l.33-34, l.168 : inclus (texte seul, AST
  égal). Question Q-3.
- **D-10 (libellé du bloc 4)** : changé seulement quand le pool d'analyse diffère du pool configuré sans cas (b) (cas
  (a)), ce qui garde les épingles ; une assertion existante de `test_pool_analyse` (rendu du cas (a) égal, à partir du
  bloc 3, à celui d'une collecte sans le flux) est remplacée par l'exigence de la nouvelle ligne plus l'égalité de tout
  le reste. Le J28 réel imprimera « (pool d'analyse, ADR-0028 D1) » au bloc 4 (cas (a) déclaré par D1). Question Q-4.
- **D-11 (model.py)** : sa docstring change, donc son blob n'est plus celui de `ed479c5` (R-A s'appuyait sur l'égalité de
  blob pour `Status`) ; l'AST hors docstrings est égal : valeurs de `Status` inchangées.
- **D-12 (C-1 tel quel)** : texte inséré à l'octet près, indentation de liste Markdown retirée ; aucune autre ligne de
  `test_sceau.py` touchée.
- **D-13 (test M24)** : un cas ajouté à une table de test existante plutôt qu'un test neuf (style du fichier).
- **D-14 (ASN, définition)** : « complet » = statut ok et deux bases non muettes ; une discordance (deux bases présentes,
  différentes) reste comparable ; les hôtes hors du pool d'analyse restent comparés (portée inchangée) ; un relevé
  partiel est ignoré en entier (limite L-5).
- **D-15 (mutant équivalent 3b-M3)** : déclaré au §14.
- **D-16 (outillage)** : `mutants3.py` a reçu les entrées 3b, 3c, 3d entre les passes (3b-M1 redéfini avant tout
  lancement : sa première forme, sans `try`, n'était pas syntaxiquement valide, contrôle `ast.parse`) ; les entrées de
  3a n'ont pas changé ; la série finale tourne sur la version finale.

## 20. Limites rendues comme items (CORR-3 ; propositions, propriétaire : orchestrateur)

- **L-5, SHOGEN-ASN-DIVERGENCE-PARTIELLE-1** : un changement d'ASN visible sur une seule base d'un relevé partiel (base
  muette) n'est pas publié ; construction possible : comparaison base par base des valeurs non muettes. Déclencheur
  proposé : après S2.
- **L-6, SHOGEN-ASN-DIVERGENCE-HORS-POOL-1** : R-B (B-1) signale des divergences publiées pour des hôtes hors du pool
  d'analyse (hôte d'un flux retiré par D1 cas a) ; le G0 ne vise que les relevés en échec ou à base muette : non traité ;
  à décider (étiquette ou retrait) au rapport `docs/11`.
- Hors de mon brief, rencontré sans être traité : C-1 de R-C (`--sortie` à barre finale), procédure amendée selon B.41.

## 21. Questions à l'orchestrateur

- **Q-1 (D-1)** : la requalification d'un prix non fini vaut quel que soit le statut ; la restreindre aux lectures `ok` ?
  (effet nul sur des journaux écrits par ce collecteur).
- **Q-2** : former les items L-1, L-2, L-3 (CORR-2), L-5, L-6 (CORR-3) ?
- **Q-3 (D-9)** : confirmer l'inclusion de `lm.py` et `r2.py` sous C-4 de R-B.
- **Q-4 (D-10)** : confirmer le libellé conditionnel et l'adaptation du test du cas (a) ; la variante sans changement du
  rendu est de garder « (pool) » et d'écrire la limite au rapport.
- **Q-5** : `model.py` relève de la collecte en quarantaine (D6 i) ; son changement (docstring seule) suit le G0 du lot :
  à confirmer au regard de la garde de D6 (« tout changement du harnais hors des lots de l'annexe A exige un G0 »).

## 22. Livrables du lot (dans `corr/`) et clôture

| fichier | sha256 |
|---|---|
| `corr-1.diff` (CORR-1) | `8dd2741548a72b60d33f99ec1efa4d928126eccbd6a95c64dd7c2aa0bdd1b252` |
| `corr-2.diff` (CORR-2) | `0847c663e60f7ce26c44d7d301228585ea37fdd54d785745ba25fb303e785240` |
| `corr-3a.diff` | `c658037514cf289ce7df4d8638e5b665b26f818caa64bb16ea7ce2a4e5ba6da8` |
| `corr-3b.diff` | `c0043861f526951d307b7a52ea7ba2640e8e875f4c8d02aac1ccc8fc690bc54d` |
| `corr-3c.diff` | `2579c2d7663c1547241f0e1e103da6d700ea374d3cfd6f2c2278d5c9712ebf8c` |
| `corr-3d.diff` | `d19ee0a87972570c807a0f9d5b115ce0807f7d9403609e52faf5b7e031e24733` |
| `corr.diff` (CORR-1 + CORR-2, référence) | `3c4cfa1bf2d6a28d72f08bb46adfc31e19b2d73b428d28ea54704eaa04e668ba` |
| `corr-lot.diff` (six sous-lots concaténés, référence, 447 lignes ajoutées) | `580a229ee4d583d06a696a37f219070817c84d2fc7af710900f9d77f203f484a` |

Fichiers finaux (arbre `corr/arbre` = état `e3d`), sha256 : `tools/rendu_unique.py` `06d189cf…9050` (HEAD
`67b897a9…f8d9`) ; `shogen_s2/r1.py` `0a16e5de…cc7f` ; `r2.py` `e9d9825c…1685` ; `lm.py` `33943649…55b4` ; `report.py`
`95aa549e…9a7a` ; `records.py` `a2e9a774…edd2` ; `model.py` `df1545e5…6eef` ; tests : `test_recalcul_json_copie.py`
`0f5a0f4f…9fb4`, `test_prix_non_fini.py` `100ea741…b876`, `test_hote_deux_flux.py` `6a68d23a…95af6`, `test_sceau.py`
`525252a3…b722`, `test_oracle_record.py` `e37e8cdc…76d3`, `test_lecteur.py` `56638d4a…fb69`, `test_r1.py`
`9be42aa2…c92c`, `test_rendu_production.py` `8b758cdb…6938`, `test_pool_analyse.py` `0cd0b167…c605`, `test_r2.py`
`73942675…ee6d`. Outils : `mutants.py` `8cc2e7c9…9e60`, `mutants3.py` `338fcd38…2d94`, `nonreg.sh` `1a7f4e7d…685f` ;
exploration (`explore/`) : `compare_sorties.py` `4d9f7363…47f2`, `explore_nan.py` `051bbe87…4c5b`, `limites.py`
`29bef2f4…c608`, `minf_null_ra.py` `18597f0f…3872`, `nan_null_ra.py` `5e3b7957…4bdf`, `rouge_par_valeur.py`
`a3d4e37d…91cb`, `serialisation_seule.py` `bd5bf49c…c4f8`, `asn_rendu.py` `d6aa2294…225d`.

Clôture : 2026-10-02 23:3xZ (`date -u` de la dernière commande : 23:38:55Z). Aucune écriture dans le dépôt, aucune
opération git en écriture ; `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée ; R-13 : aucun marqueur de dette nu dans les diffs
(recherche des marqueurs usuels de dette sur les diffs : 0) ni dans ce journal. Copies de travail conservées dans `corr/` (`arbre`, `base`, `snap/`,
`verif*`, `chaine`, `rouge`) : aucune ne contient `docs/rapports`, `docs/adr-0025`, `docs/adr-0028/monark-m009a` ni
`JOURNAL.md` (exclus à l'extraction).
