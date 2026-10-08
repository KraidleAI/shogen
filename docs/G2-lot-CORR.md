# G2 du lot CORR (S2, partie 4) — relecture neuve (seconde instance, après interruption)

Ouverture : 2026-10-02T23:58:56Z (`date -u`). Réviseur : `shogen-worker` en rôle G2, n'a écrit aucune ligne du lot.
Brief : `g2-corr/BRIEF-G2-CORR.md`, sha256 `032ec2d6bf9cec96b47d855c7594be977d3861b053d2d129a0ba31cbd4c088d8` (recalculé : identique).
Dossier de travail : `g2-corr/r2/` (neuf). Le dossier `g2-corr/interrompu-1/` n'a été ni ouvert ni utilisé.

> Rapport écrit au fil de l'eau, clos le 2026-10-03 (§17 verdict, §18 clôture).

## 0. Gate 0

Modèle résolu : `claude-opus-5-5` (identifiant exact déclaré par l'environnement d'exécution). Effort : non lisible
depuis l'intérieur de la session ; non attesté par moi.

## 1. Attestation D.3

Forme finale, expositions, écarts de procédure et déclaration FM-1.1 : §16.

## 2. Pièces et empreintes

- Livraison : `sha256sum -c livraison/SHA256SUMS` : 7/7 OK (G1-lot-CORR.md, corr-1, corr-2, corr-3a, corr-3b, corr-3c, corr-3d).
- Dépôt : branche `partie-4-execution`, HEAD `19eb912`, arbre propre (`git status --short` vide).
- `git rev-parse e25d840:s2-harness 19eb912:s2-harness` : `5feb33dd…` = `5feb33dd…` (identiques).
- `git rev-parse e25d840:scripts 19eb912:scripts` : `28426cc5…` ≠ `e3d488fc…` ; `git diff --stat e25d840 19eb912 -- s2-harness scripts .github` :
  `scripts/controle/README.md` (1 ligne), `scripts/controle/SHA256SUMS` (+1), `scripts/controle/sorties-fm11/corr-worker.json` (+1537).
  Aucun `.py` touché : l'affirmation « code de `19eb912` identique à celui de `e25d840` » tient pour le code ; le dossier
  `scripts/` porte trois fichiers non-code de plus (observation, §11).
- `model.py` : `git rev-parse HEAD:… e25d840:… ed479c5:…` et `git hash-object` = `7264d3fea1a4519778c281edc83e82b491f64d46` (4 fois).

## 3. Application des diffs (copie `r2/corr`, extraction de `e25d840` avec les exclusions du brief)

`git apply --check` puis `git apply` des six diffs dans l'ordre : tous appliqués sans rejet ni décalage signalé
(le dossier de copie n'est dans aucun dépôt git : `fatal: not a git repository`).

| diff | lignes ajoutées | retirées | fichiers |
|---|---|---|---|
| corr-1 | 94 | 1 | `tools/rendu_unique.py`, `tests/test_recalcul_json_copie.py` (neuf) |
| corr-2 | 142 | 2 | `shogen_s2/r1.py`, `tests/test_prix_non_fini.py` (neuf) |
| corr-3a | 122 | 0 | `tests/test_sceau.py`, `test_oracle_record.py`, `test_lecteur.py`, `test_r1.py`, `test_hote_deux_flux.py` (neuf) |
| corr-3b | 37 | 6 | `tools/rendu_unique.py`, `tests/test_rendu_production.py` |
| corr-3c | 26 | 15 | `shogen_s2/r1.py`, `records.py`, `r2.py`, `lm.py`, `report.py`, `tests/test_pool_analyse.py` |
| corr-3d | 23 | 4 | `shogen_s2/r2.py`, `tests/test_r2.py` |

R-25 : maximum 142 lignes ajoutées par diff (≤ 200). `diff -rq base corr` : 16 fichiers touchés, tous sous
`s2-harness/` ; `model.py` absent de la liste (Q-5 : retrait constaté).

## 4. Suite entière et « rouge avant » (rejoués par moi)

Toutes les exécutions : `env -u SHOGEN_S2_CAMPAGNE_CONTROL PYTHONDONTWRITEBYTECODE=1 python3 -B` (Python 3.11.15),
dans `r2/` hors dépôt ; `env | grep -c SHOGEN_S2_CAMPAGNE_CONTROL` = 0.

- Suite entière, base `e25d840` (`r2/base`) : `Ran 383 tests in 49.949s` `OK (skipped=2)`.
- Suite entière, arbre corrigé (`r2/corr`, six diffs) : `Ran 396 tests in 51.656s` `OK (skipped=2)` (+13 tests :
  2 CORR-1, 2 CORR-2, 6 de 3a, 2 de 3b, 1 de 3d ; 3a ajoute aussi un cas à une table, 3c modifie un test) ;
  0 `__pycache__` sous `r2/`.
- Rouge avant : arbre `r2/rouge` = code de `e25d840` (contrôlé : `diff -rq` sur `shogen_s2` et `tools` vide) + les
  fichiers de test corrigés ; chaque test lancé seul :

| test | sur `e25d840` | motif (lu dans le log) |
|---|---|---|
| `test_recalcul_json_copie…test_recalcul_tiers_paire_copie_en_liste_triee` | ERROR | `TypeError: frozenset hors du JSON du recalcul tiers` |
| `test_recalcul_json_copie…test_decimal_ensembles_en_listes_triees` | ERROR | idem |
| `test_prix_non_fini…test_rendu_et_recalcul_comme_prix_null` | ERROR | `decimal.InvalidOperation`, pile `report.py:174 > r1.py:566 compute_r1 > 465 > 194 classify_ecart > 106 _median` |
| `test_prix_non_fini…test_formes_lues_comme_absentes_ou_inchangees` | 15 FAIL | prix brut rendu, aucun avertissement |
| `test_rendu_production…test_parent_de_la_sortie_absent` | ERROR | `FileNotFoundError` non rattrapée (`…/absent/.sortie.xxxx`) |
| `test_rendu_production…test_raw_refus_sans_chemin_des_journaux` | FAIL | verdict porte `dans /tmp/s2suite_…/raw.jsonl` |
| `test_pool_analyse…test_a_flux_mort_partout_hors_r1_lm_r2_aux_quatre_points` | FAIL | libellé « (pool d'analyse, ADR-0028 D1) » absent |
| `test_r2…test_echec_et_base_muette_ne_sont_pas_des_divergences` | FAIL | divergences tirées des relevés en échec (h0 `(1, 1, 1.0) → (None, …)` en tête) |
| les 7 tests de 3a (`test_sceau`, `test_oracle_record` cas M24, `test_lecteur`, `TestBordsR1` ×2, `test_hote_deux_flux` ×2) | OK | attendu : tests seuls sur du code inchangé ; le critère est « mutant vivant avant, tué après » (§10) |

- SHOGEN-SCEAU-VERIFY-REQUETE-1 « tel quel » : `docs/G2-partie-3.md` l.296-308, retrait de 4 espaces, comparé par `diff`
  à `test_sceau.py` corrigé l.94-106 : identique ; l.1-94 du fichier inchangées.

## 5. Non-régression (rejouée par moi)

- `scripts/controle/SHA256SUMS` : `sha256sum -c` OK pour les 8 entrées de `e25d840` (copie `r2/base`) et les 9 de HEAD
  (dépôt, lecture seule) ; `regle_fixtures.py` `5557fb56…`, `render_fixture.py` `4084c42b…` (README de `e25d840`).
- `regle_fixtures.py` : base et arbre corrigé, exit 0, sha256 du JSON
  `ea3a2d94ef1075603e8f7cfc53c68b26e51729b61714028e3fb03dc32f79cb29` les deux fois ; sortie imprimée identique (`cmp`).
- `render_fixture.py` : base et arbre corrigé, exit 0 ; `sans_option 4e62fbb8a4a7a29c0761c719c8f731a8247ef407be7a7a04c44219bd093c9a01`,
  `avec_option d079dd9d62a3f585a136779330cb21017a300ae853bef5cb63024bb6412de608` les deux fois.
- `git hash-object` de `model.py` : `7264d3fea1a4519778c281edc83e82b491f64d46` dans `r2/corr` comme dans `r2/base` (et à
  `ed479c5`, HEAD, `e25d840` : §2).
- sha256 (16 premiers caractères) des modules changés, arbre corrigé : `rendu_unique.py` `06d189cf…`, `r1.py` `0a16e5de…`,
  `r2.py` `e9d9825c…`, `lm.py` `33943649…`, `report.py` `95aa549e…`, `records.py` `a2e9a774…` (égaux aux préfixes du
  journal G1 §22) ; `model.py` et `oracle_record.py` inchangés.

## 6. Conformité au G0 (contrôle 1 du brief)

Contrat lu : `git show e25d840:docs/adr-0028/G0-lot-CORR.md` (l.1-61). Les l.62-92 ajoutées à `19eb912`
(adjudication) ne sont lues qu'après mes mutants (§8), pour ne pas m'y ancrer ; les décisions Q-1 à Q-5 sont prises du
brief. Relues ensuite : l'adjudication ne contredit aucun de mes constats ; son huitième mutant (statut ignoré dans la
détection de divergence) est bien équivalent sur ce collecteur (`resolve_host_real` ne pose aucune des deux bases sur un
`resolve_failed`, `r2.py` l.328-341 : `None in (…)` l'écarte déjà).

Périmètre du code changé, mesuré par AST (`r2/fonctions_changees.py` : définitions de premier niveau dont l'AST hors
docstrings diffère, base contre arbre corrigé) :
`rendu_unique.py` → `_decimal`, `produire`, `produire_tout` ; `r1.py` → `parse_journal` (+ `import sys`) ;
`r2.py` → `compute_partition` ; `report.py` → `render_report` ; `lm.py`, `records.py` → docstrings et commentaires
seulement. Sous-lot 3c isolé (états `e3b` → `e3c` reconstruits par moi) : AST hors docstrings égal pour `r1`, `records`,
`r2`, `lm` ; `report.py` diffère par la seule ligne du libellé du bloc 4 (`diff` hors commentaires : l.490).

| item du G0 | construit comme dit | rien de plus |
|---|---|---|
| CORR-1 | `_decimal` : `set`/`frozenset` → `sorted(x)` ; Decimal et refus des autres types inchangés. `exact_copy_pairs` est une `list` de `frozenset` dans l'ordre de `combinations(pool, 2)` (`r2.py` l.742-759) : sortie déterministe ; liste triée cohérente avec `compute_partition` (`tuple(sorted(pair))`, l.823) | oui (annotation `-> str \| list`, D-5) |
| CORR-2 | `r1.parse_journal` : prix non fini → `None`, compte par `flux_id`, une ligne sur `sys.stderr` capturée par `produire` (`redirect_stderr`, l.394) puis réécrite sans dossier (l.411) | oui ; portée « quel que soit le statut » = Q-1, retenue |
| SCEAU-VERIFY-REQUETE-1 | test inséré tel quel (§4) | oui |
| RENDU-MKDTEMP-1 | `mkdtemp` dans le `try`, `tmp` initialisé à `None`, `finally` gardé ; ligne « échec de production », code 1 ; un test | oui |
| RAW-CHEMIN-1 | verdict de refus réécrit par le même `replace(os.path.join(a.journaux, ""), "")` que les avertissements ; un test | oui (une phrase de docstring) |
| TESTS-C8-SUITE-1 | un cas M24 ajouté à la table de `test_oracle_record` ; un test des trois champs sous segment et sous plage seule | oui |
| TESTS-HOTE-DEUX-FLUX-1 | `tests/test_hote_deux_flux.py` (deux tests) | oui |
| TESTS-BORDS-R1-1 | `TestBordsR1` (deux tests) ; valeurs recalculées par moi : p̂ = 20/40 = 1/2 par flux, P̂_more = 1 − 1/8 − 3/8 = 1/2, garde = 40·1/4 = 10, K = 20 (rangs 10-29), z = 0 | oui |
| R1-DOCSTRINGS-1 | `block_long_run_variance` et `regle_critere` ; textes conformes au paquet (§10.2 = texte de la règle, pts 1-11, l.113-132 ; §10.4 l.170 : correspondance Künsch « porte sur les poids et n'est qu'approchée ») ; `biblio/kunsch1989-aos-17-3-1217.pdf` sha256 `6d069c52…`, égal à `biblio/INDEX.md` l.336 | oui |
| commentaires et libellés | `records.py` l.10 et l.41-42 conformes à C-3 de R-A (`LOAD_BEARING_KEYS` relu : les cinq premiers + `seuil_historique_valeur` + `n_min_hors_enveloppe` sont les entrées de `compute_r1`) ; `r2.py` docstring de module et `lm.py` l.33-34, l.168 : C-4 de R-B (Q-3 confirmée) ; libellé du bloc 4 au cas (a) (Q-4 confirmée) ; **docstring de `model.py` : non faite** (Q-5, retrait ; blob `7264d3fe…` constaté) | oui |
| ASN-DIVERGENCE-ECHEC-1 | divergence entre relevés complets seulement (statut ok, deux bases non muettes), référence = dernier relevé complet ; `by_host` inchangé (dernier relevé quel qu'il soit) ; `asn_divergences` n'est lu que par `report.py` l.549 (impression) : k_eff et drapeau 2 ne le lisent pas (`grep`) | oui |

## 7. Effet sur la décision (contrôle 2 du brief)

### 7.1 Point unique de lecture des prix (recherche exhaustive, arbre corrigé)

`grep -n "parse_journal|read_jsonl|json.load|journal.jsonl|open(|read_text|read_bytes|readlines|parse_constant|parse_float"`
sur `shogen_s2/*.py` (collecte exclue) et `tools/*.py`, puis `grep -n "price|prix"` sur `r1`, `r2`, `lm`, `report`,
`records`, `window`, `tools/*` ; sites lus :
- lecteurs de `journal.jsonl` : `r1.parse_journal` (l.398) appelé par `r1.recompute_from_journal` (l.820 ;
  `recompute_d5_from_journal` passe par lui), `lm.recompute_lm_from_journal` (l.226), `r2.recompute_r2_from_journal`
  (l.1083), `report.render_report` (l.162 ; blocs 1 à 6 et [SENSIBILITÉ] l.684-685 sur la même liste), `closure.py`
  l.104 (quarantaine, hors runs) ;
- **seul autre lecteur** : `records.verifier_raw` (l.133), qui relit `journal.jsonl` par `read_jsonl_tolerant` sans
  `parse_journal`, mais ne lit que `window_start`, `flux_id`, `fetch_ts` (`cle`, l.119-120) et `sha256_raw` : aucun prix ;
- `rendu_unique.py` : ne lit aucun journal lui-même (`produire` appelle `records.verifier_raw`, `render_report` et les
  quatre `recompute_*`) ; `oracle_record.py` : ne lit aucun journal (lance les commandes, capture leurs octets) ;
- consommateurs de `price`, tous sur la liste rendue par `parse_journal` : `r1.classify_ecart` l.181 et l.202,
  `analysis_pools` l.453 (ok = statut ok **et** prix non nul : pool D1, conforme au G0 ; le seuil QUASI-MORT n'a pas
  de code, C-5),
  `_classify_window` l.478-480, `compute_r1` l.592-594, `r2._price_at` l.465-467, `r2.lnprice_by_window` l.479-480,
  `report` bloc 2 l.302 (`rd.get("price") or "-"`).
Conclusion : CORR-2 est le seul point ; un prix non fini devient `None` dans le dictionnaire même que consomment tous les
sites ci-dessus, d'où, par construction, le même effet qu'un `price` nul (même clé, même valeur).

### 7.2 Sonde différentielle indépendante (`r2/sonde/sonde_diff.py` `f92b7a4f…`, `compare.py` `332d8bec…`, sortie `compare.out` `6ce13814…`)

Journaux synthétiques seulement (collecteur réel de `e25d840`, lectures tirées à graine : neuf flux, 300 fenêtres
calme puis stress, pannes corrélées, hors-enveloppe, staleness, relevés ASN) ; familles F1 (ASN tous ok), F2 (F1 +
formes finies équivalentes : `E`, `+`, zéros de queue, espaces, jeton JSON numérique), F3 (ASN avec échecs, bases
muettes, un vrai changement), F4 (un flux mort partout : D1 cas a), F5 (sans ASN) ; et, pour F1, F3, F5, deux
variantes : N (25 lectures ok à prix non fini, douze formes dont jetons JSON `NaN`, `Infinity`, `-Infinity`, plus un
`"NaN"` sur une lecture en panne) et Z (les mêmes lectures à `null`). Trois variantes de lecture par journal (sans
segment ; segment `t_fin` ; `n_fixe` + plage). Sorties comparées : texte de `render_report`, `regle_critere`, les quatre
`recompute_*` (JSON), stderr.

| comparaison | résultat |
|---|---|
| base → corrigé, F1, F2, F5, F1-Z, F5-Z | **0 écart** (texte, règle, r1, d5, lm, r2, stderr) ; valeurs non triviales (z publiés, K > 0, pannes, hors-enveloppe, staleness) |
| base → corrigé, F3 et F3-Z | seules différences : 11 lignes « DIVERGENCE ASN » retirées par variante, toutes tirées d'un relevé en échec ou à base muette ; `r2.partition.asn_divergences` 12 → 1 (le vrai changement, ligne gardée à l'identique) |
| base → corrigé, F4 | seule différence : la ligne du bloc 4, « (pool) » → « (pool d'analyse, ADR-0028 D1) » |
| base sur N | `decimal.InvalidOperation` (`_median` l.106, ou `classify_ecart` l.207 de `e25d840`) : le constat A-1 reproduit |
| corrigé, Z → N (F1, F3, F5) | texte et JSON **identiques** ; seule différence : l'avertissement, une ligne par rendu, quatre par jeu de `recompute_*`, compte par flux = 25 lectures ok + 1 en panne (Q-1), aucune valeur |

Conclusion du contrôle 2 : aucune valeur de la règle ne change pour un prix fini (y compris sous des formes finies
non canoniques) ; un prix non fini produit le même rendu qu'un `null`, à l'avertissement près.

### 7.3 L-3 (SHOGEN-SOURCE-TS-NON-FINI-1) : inatteignabilité confirmée

`sources.py`, `journal.py`, `collector.py` : blobs égaux à `ed479c5` et `e25d840` (`70c5f163…`, `369012c2…`, `c9dc820e…`).
[lu] `sources.py` l.122-220 : chaque `source_ts` vaut `None` (binance, kraken, bitfinex), `_iso_to_epoch(...)`
(coinbase : `datetime.timestamp()`, fini), `int(...)/1000.0` (okx ×2, gemini), `float(int(...))` (bitstamp, coingecko,
defillama, pyth) ou `float(_u256(...))` (chainlink, < 2²⁵⁶) : `int()` d'un NaN ou d'un infini lève (`ValueError`,
`OverflowError`), rattrapé en `PANNE_DECODE` par `sources.read` l.395-399 ; un entier trop grand pour un flottant lève
`OverflowError` (même rattrapage). `journal.journal_entry` l.43 écrit ce flottant fini tel quel. Aucune `source_ts` non
finie ne peut donc être écrite par ce collecteur : L-3 se clôt sans code (décision de l'orchestrateur, sous ma
confirmation). Au passage : `journal_entry` l.42 écrit `str(r.price)` ou `null`, et `sources.read` ne pose un prix que
sur une lecture `ok` (l.401-402) : la remarque D-1 du worker (aucun prix sur une lecture non ok) est exacte.

## 8. Mutants du réviseur (contrôle 4 ; `r2/mutants_g2.py` `0b7b54eb…`)

Une substitution par mutant, motif présent exactement une fois (contrôlé), copie neuve de l'arbre corrigé, suite
entière sous `env -u SHOGEN_S2_CAMPAGNE_CONTROL` ; mort = code ≠ 0. Aucun ne reprend un mutant du journal G1 (M01-M18,
RC-/RB-/RA-/P3-, 3b-M1..M4, 3c-M1..M2, 3d-M1..M4).

| id | item | mutation | résultat | tué par |
|---|---|---|---|---|
| T00 | — | témoin | vit (396, OK) | — |
| G01 | CORR-1 | `return sorted(x)` → `return tuple(sorted(x))` (même JSON) | tué (1 F) | `test_decimal_ensembles_en_listes_triees` |
| G02 | CORR-2 | `not Decimal(p).is_finite()` → `Decimal(p).is_nan()` (infinis gardés) | tué (6 F, 1 E) | les deux tests de `test_prix_non_fini` |
| G03 | CORR-2 | ordre des flux de l'avertissement : `sorted(nf.items(), key=str)` → `nf.items()` (ordre du fichier) | **vit** | — (constat C-1) |
| G04 | CORR-2 | compte plafonné : `nf[f] += 1` → `nf[f] = 1` | tué (3 F) | `test_rendu_et_recalcul_comme_prix_null` |
| G05 | CORR-2 | `ArithmeticError` retiré de l'`except` (« abc » lève dans `parse_journal`) | tué (1 E) | `test_formes_lues_comme_absentes_ou_inchangees` |
| G06 | RENDU-MKDTEMP-1 | `mkdtemp(…, dir=None)` (temporaire hors du parent de la cible) | tué (10 F) | `test_parent_de_la_sortie_absent`, `test_echec_a_chaque_pas_rien_ne_reste` |
| G07 | ASN-DIVERGENCE-ECHEC-1 | relevé complet = Cymru seule non muette (`rec.get("asn_cymru") is not None`) | **vit** | — (constat C-2) |
| G08 | ASN-DIVERGENCE-ECHEC-1 | comparaison sur RIPEstat seule (`(prev_r, cur_c) != (cur_r, cur_c)`) | **vit** | — (constat C-3) |
| G09 | CORR-2 | requalification par le statut (`r["status"] = "panne_decode"`, prix gardé) au lieu du prix | tué (17 F) | les deux tests de `test_prix_non_fini` |

Bilan : 9 mutants, 6 tués, 3 survivants. Non-équivalence des survivants montrée (`r2/survivants.py`, même entrée sur
l'arbre corrigé et sur le mutant) :
- G03 : deux `NaN` (« zeta » puis « alpha » dans le fichier) → corrigé `alpha 1, zeta 1`, mutant `zeta 1, alpha 1` ;
- G07 : hôte ok(1, 1) → ok(None, 1) → ok(1, 1) → corrigé `[]`, mutant deux fausses divergences `(1, 1, 1.0) → (None, 1, 2.0)`
  et retour ;
- G08 : hôte ok(1, 1) → ok(1, 2) (changement Cymru seule) → corrigé une divergence, mutant `[]`.

## 9. Exécution fail-closed (contrôle 6)

`rendu_unique.py --gardes-seules`, script de l'arbre corrigé puis de la base, `--depot` = copie corrigée (hors dépôt,
sans `.git` : choix délibéré pour ne pas faire relire `JOURNAL.md` par `git show`), `--paquet` = `PAQUET-PREREG-S2.md` de
la copie, `--journaux` = dossier vide, `--sommes` = `scratchpad/sceau/SHA256SUMS-cloture-2026-09-28.txt` (sha256
`70910984…`, égal à la clé `sommes` du bloc, l.219 du paquet ; contenu non affiché), `--sortie` absente, `--auteur
claude-opus-5-5` :
- corrigé : **exit 2**, sortie standard vide (0 octet), aucune sortie créée ; refus (1), (2) dépôt illisible ; (3)
  `FileNotFoundError` (journal absent) ; **(4) `sha256 du script 06d189cf… ≠ sha256_script du bloc`** ; (5) T0
  indéterminé ; (6) ni jeton ni go ; la garde « bloc » passe (bloc bien formé) ;
- base : exit 2, mêmes refus, sauf (4) « non évaluée (dépôt illisible) » : le sha de `rendu_unique.py` de `e25d840`
  est celui du bloc scellé. Le script corrigé ne passe donc plus la garde (4) contre le paquet actuel, comme la garde
  (2) ne passera plus contre son `commit_analyse` : attendu, c'est le « nouveau bloc machine » de la suite du G0
  (rappel, pas un constat).
- Le chemin `--gardes-seules` sort avant `produire_tout` ; aucune fonction de garde n'est touchée par le lot (§6, AST).

## 10. Contre-épreuve des tests de 3a (tests seuls : « vivant avant, tué après » ; `r2/mutants_3a.py` `1193093…`)

Quatre des mutants que visent les tests de 3a, reconstruits par moi depuis la description des rapports R-A, R-B, R-C
(motif unique contrôlé), appliqués au code de `e25d840` ; suite de `e25d840` puis suite corrigée (arbre `rouge`) :

| mutant | mutation | suite de `e25d840` | avec les tests du lot : test visé |
|---|---|---|---|
| RA-M1 | staleness `> sigma` → `>= sigma` (`r1.py` l.189) | vit (OK) | `test_staleness_egale_a_sigma_pas_d_ecart` rouge |
| RA-M4 | garde `gate < seuil_hist` → `<=` (l.632) | vit | `test_garde_egale_a_10_z_publie` rouge |
| RB-M01 | borne supérieure ⇒ NON ÉVALUABLE même si k_eff < k nominal (`r2.py` l.974) | vit | `test_eteint_borne_superieure_sous_k_nominal` rouge |
| RC-M24 | `noms[1:] == list(PRODUCTION)` (`oracle_record.py` l.226) | vit | `test_verifier_un_refus_nomme_par_controle` rouge |

(Les autres échecs de l'arbre `rouge` sont les huit tests liés au code corrigé, attendus rouges sur `e25d840`, §4 ;
aucun autre.) Les sept autres mutants de 3a (RC-M29, RC-M30, RB-M03b, RB-M06, RB-M15, P3-M4, P3-M4b) ne sont pas
rejoués par moi : je m'appuie pour eux sur le journal G1 §13 [2nd].

## 11. Constats

**A — aucun.** Aucune valeur de la règle ne change pour un prix fini (§5, §7.2) ; l'exécution reste fail-closed (§9) ;
les tests neufs sont déterministes (aucun ne dépend du hachage, de l'heure ni du réseau ; `test_verify_lie_le_jeton_a_la_requete`
dépend d'`openssl` comme les tests déjà présents de sa classe).

**B — aucun.** Les seuls changements de rendu sont ceux que le G0 prescrit : avertissement de CORR-2, verdict `raw`
sans dossier, libellé du bloc 4 au cas (a), lignes « DIVERGENCE ASN » tirées d'un relevé incomplet retirées (§7.2).

**C — sans effet sur les sorties :**

- **C-1 (mutant G03 survivant ; CORR-2)** : l'ordre des flux dans l'avertissement (tri par nom, `sorted(…, key=str)`,
  `r1.py` l.418) n'est fixé par aucun test : la fixture du test d'intégration a ses prix non finis dans l'ordre
  alphabétique du fichier (bitfinex rang 10, gemini rang 60). Les deux ordres sont déterministes ; aucun effet sur une
  valeur. Correction K-2.
- **C-2 (mutant G07 survivant ; ASN-DIVERGENCE-ECHEC-1)** : le test de l'item ne pose qu'une base muette côté Cymru
  (`asn_rec("h1", 2, None, …)`) ; un contrôle réduit à Cymru survit. Le code (`None not in (ripestat, cymru)`, `r2.py`
  l.789) est juste. Cas de production plausible : `_ripestat_asn` peut rendre `None` quand Cymru répond (`r2.py`
  l.329-337). Correction K-1.
- **C-3 (mutant G08 survivant ; même item)** : aucun test ne pose un changement d'ASN sur une seule base entre deux
  relevés complets (le test antérieur `test_asn_divergence_published_not_overwritten` change les deux bases) ; une
  comparaison réduite à RIPEstat survit. Trou antérieur au lot, sur une ligne que le lot réécrit ; code juste.
  Correction K-1.
- **C-4 (journal G1 non mis à jour après Q-5)** : `G1-lot-CORR.md` (`1849053c…`), destiné à être versé, décrit encore
  le morceau `model.py` retiré : §12 (corr-3c « 29 / 16 », `2579c2d7…`, `model.py` listé), §15 (commentaire de
  `model.py`, AST « `model` »), §19 D-11, §22 (corr-3c `2579c2d7…`, `corr-lot.diff` 447 lignes, `model.py`
  `df1545e5…`). L'adjudication du G0 (`19eb912`, l.88-90) porte la décision et le sha révisé `85ee60e4…5a64`, égal à
  `livraison/SHA256SUMS`. Recommandation (hors liste fermée) : une note datée de l'orchestrateur en tête du journal
  versé, ou dans le message du commit, qui renvoie à Q-5.
- **C-5 (seuil SHOGEN-FLUX-QUASI-MORT-1 : garantie du G0 non portée par le code)** : le G0 dit qu'un prix non fini est
  « non `ok` au sens du pool D1 et du seuil SHOGEN-FLUX-QUASI-MORT-1 ». Pour D1 c'est vrai par construction
  (`analysis_pools` l.453 : statut ok ET prix non nul). Le seuil QUASI-MORT n'a aucun code à `e25d840` (`grep QUASI`
  sur `shogen_s2/` et `tools/` : 0 occurrence utile ; paquet l.84 et l.184 : sensibilité ajoutée après le
  pré-enregistrement). La lecture requalifiée garde `status: "ok"` (prix `None`) : une implémentation future qui
  compterait « ok » par le statut seul, ou relirait `journal.jsonl` sans `parse_journal`, compterait un prix non fini
  (comme un prix nul) en lecture ok. Item à former, §13.
- **C-6 (précision de docstring, sans correction exigée)** : `regle_critere` dit « (recopie d'ADR-0028 §1 bis.1) » ;
  le paquet l.171 précise « six écarts, chacun marqué dans le texte » (E-1 à E-6, §10.4). Le paquet étant désigné comme
  texte normatif, la parenthèse n'induit pas en erreur sur la norme ; formulation plus exacte possible :
  « (recopie d'ADR-0028 §1 bis.1, six écarts marqués : paquet §10.4) ».
- **C-7 (observation)** : la docstring de module de `r2.py` (3c) range « FAUX » sous ÉTEINT et « k_eff non évaluable »
  sous NON ÉVALUABLE sans dire la préséance (k_eff contrôlé d'abord) ; la docstring de `drapeau_2` la dit ; le texte
  scellé ne départage pas (C-1 de R-B). Aucune action.
- **Observation** : l'affirmation du brief « code de `19eb912` identique à celui de `e25d840` » tient pour le code ;
  `scripts/` diffère de trois fichiers non-code (README, SHA256SUMS, `sorties-fm11/corr-worker.json`), §2.

## 12. Corrections (liste fermée ; tests seuls, aucun code de `shogen_s2` ni de `tools` touché)

Vérifiées par moi sur une copie de l'arbre corrigé (`r2/corrK`, diff `r2/K-corrections.diff` `aae3daa6…`) : les deux
tests proposés passent ; suite entière `Ran 398 tests` `OK (skipped=2)` ; chaque test rougit sur le mutant visé
(`r2/verif_K.py` `d51d994a…` : G03 `FAILED (failures=1)`, G07 `FAILED (failures=1)`, G08 `FAILED (failures=1)`).
R-25 : corr-2 passerait à 152 lignes ajoutées, corr-3d à 32. Texte exact à l'octet : `r2/K-corrections.diff`
(`diff -u`, en-têtes `corr/…` → `corrK/…`, applicable par `git apply -p1` sur l'arbre corrigé) ; dans les blocs
ci-dessous, retirer les deux espaces d'indentation de liste Markdown.

- **K-1** — fichier `s2-harness/tests/test_r2.py` (sous-lot corr-3d), après la l.368 de l'arbre corrigé.
  Texte actuel (l.368-370) :
  ```
          self.assertEqual((part["k_eff"], part["k_eff_is_upper_bound"], part["unattributed"]), (4, True, ["h3"]))

      def test_rpc_read_path_caveat_carried(self):
  ```
  Texte proposé (une méthode insérée entre la l.368 et la ligne vide qui la suit) :
  ```
          self.assertEqual((part["k_eff"], part["k_eff_is_upper_bound"], part["unattributed"]), (4, True, ["h3"]))

      def test_ripestat_muette_et_changement_d_une_seule_base(self):
          """G2 du lot CORR (mutants G07, G08) : un relevé à RIPEstat muette n'est ni divergence ni référence (h0) ; un
          changement d'ASN d'une seule base entre deux relevés complets est une divergence (h1, Cymru seule)."""
          fh = self._fh(["h0", "h1"])
          recs = [asn_rec("h0", 6, 6, ts=1.0), asn_rec("h0", None, 6, ts=2.0), asn_rec("h0", 6, 6, ts=3.0),
                  asn_rec("h1", 7, 7, ts=1.0), asn_rec("h1", 7, 8, ts=2.0)]
          part = r2.compute_partition(recs, fh, list(fh), {"exact_copy_pairs": []})
          self.assertEqual(part["asn_divergences"], [{"host": "h1", "avant": (7, 7, 1.0), "apres": (7, 8, 2.0)}])

      def test_rpc_read_path_caveat_carried(self):
  ```
- **K-2** — fichier `s2-harness/tests/test_prix_non_fini.py` (sous-lot corr-2), après la l.117 de l'arbre corrigé.
  Texte actuel (l.117-120) :
  ```
                  self.assertEqual((lu["price"], err.getvalue()), (prix, AVERT.format(p, "x 1") + "\n" if avert else ""))


  if __name__ == "__main__":
  ```
  Texte proposé :
  ```
                  self.assertEqual((lu["price"], err.getvalue()), (prix, AVERT.format(p, "x 1") + "\n" if avert else ""))

      def test_flux_de_l_avertissement_tries_par_nom(self):
          """G2 du lot CORR (mutant G03) : flux de l'avertissement triés par nom, non dans l'ordre du fichier (zeta y
          précède alpha)."""
          p = os.path.join(tempfile.mkdtemp(prefix="s2nf_"), "journal.jsonl")
          Path(p).write_text('{"flux_id": "zeta", "status": "ok", "price": "NaN"}\n'
                             '{"flux_id": "alpha", "status": "ok", "price": "NaN"}\n', encoding="utf-8")
          with contextlib.redirect_stderr(io.StringIO()) as err:
              r1.parse_journal(p)
          self.assertEqual(err.getvalue(), AVERT.format(p, "alpha 1, zeta 1") + "\n")


  if __name__ == "__main__":
  ```

## 13. Limites rendues comme items à former (règle PAROXYSME ; propriétaire proposé : orchestrateur)

- **De C-5** — proposition : contrainte de construction ajoutée à SHOGEN-FLUX-QUASI-MORT-1 (annexe B l.101) : la
  sensibilité compte « ok » par le prédicat d'`r1.analysis_pools` (statut ok **et** prix non nul) sur la liste de
  `r1.parse_journal`, jamais par le statut seul ni par une relecture directe de `journal.jsonl` ; déclencheur :
  construction de la sensibilité (après l'exécution unique).
- **L-3** : confirmée inatteignable (§7.3) ; je ne forme pas d'item.
- **Non couvert par ma relecture** : les sept mutants de 3a non rejoués (§10) ; l'exécution réelle de
  `rendu_unique.py` sur un dépôt git (je n'ai lancé `--gardes-seules` que sur une copie sans `.git`, pour ne pas faire lire
  `JOURNAL.md` ; les fonctions de garde ne sont pas touchées par le lot) ; la mesure de coût de `parse_journal` à
  l'échelle de la campagne (chiffres du worker, §7 de son journal, non rejoués : information pour SHOGEN-RENDU-COUT-1).

## 14. Fichiers lus (niveau [lu] sauf mention ; lignes)

- `g2-corr/BRIEF-G2-CORR.md` (entier) ; `livraison/` : `SHA256SUMS`, les six diffs (entiers), `G1-lot-CORR.md` (entier).
- Dépôt, lecture seule : `CLAUDE.md` (contexte de session) ; `docs/adr-0028/ANNEXE-D-preenregistrement.md` l.1-170
  (D.1, **liste D.2 l.32-47 lue sans ouvrir aucune pièce**, D.3, D.4) ; `G0-lot-CORR.md` à `e25d840` l.1-61 et à HEAD
  l.62-92 (après mes mutants) ; `G2-RATTRAPAGE-R-B.md` l.88-200 (+ en-têtes) ; `G2-RATTRAPAGE-R-A.md` l.137-262
  (+ en-têtes) ; `G2-RATTRAPAGE-R-C.md` l.145-200, l.212-282 (+ en-têtes) ; `docs/G2-partie-3.md` l.285-312 ;
  `PAQUET-PREREG-S2.md` l.109-116, l.165-172, et lignes de `grep` (l.6, l.84, l.111-134 en-têtes, l.117, l.124,
  l.132, l.170, l.184, l.219 ; coupées à 90-700 caractères) ; `ANNEXE-B-items.md` lignes d'un `grep P-01` (l.13, 15,
  50, 98, 103, coupées à 200) ; `biblio/INDEX.md` l.3 et l.336 (`grep`) ; `s2-harness/shogen_s2/sources.py` l.80-220,
  l.370-402 et `journal.py` l.30-63 (HEAD = `ed479c5` pour ces blobs) ; `scripts/controle/README.md` et `SHA256SUMS`
  (copie de `e25d840`), diff `e25d840..19eb912` de ces deux fichiers.
- Copies (`r2/base`, `r2/corr`) : `tools/rendu_unique.py` (entier), `tools/oracle_record.py` (entier) ;
  `shogen_s2/r1.py` l.1-260, l.380-609, l.800-856 ; `records.py` l.1-145, l.267-292, l.398-423 ; `r2.py` l.300-344,
  l.381-421, l.450-600, l.725-1000, l.1060-1098 ; `lm.py` l.215-239 ; `report.py` l.85-110, l.150-200, l.270-320,
  l.480-560, l.755-787 ; `model.py` l.1-70 ; `window.py` et `collector.py` (lignes de `grep`) ; tests :
  `test_collector.py` l.1-105, `test_rendu_production.py` l.25-60, `test_r2.py` l.78-85, l.286-298, l.340-372.

## 15. Commandes principales et sorties (horloge `date -u` : départ 23:58:22Z le 2026-10-02 ; dernière 00:26:20Z le 2026-10-03)

| commande | sortie |
|---|---|
| `sha256sum` du brief ; `sha256sum -c livraison/SHA256SUMS` | `032ec2d6…88d8` ; 7 OK |
| `git rev-parse`, `git diff --stat e25d840 19eb912 -- s2-harness scripts .github`, `git hash-object` | §2 |
| `git archive e25d840 \| tar -x` (exclusions du brief) ×2 ; `git apply --check` + `git apply` ×6 | §3 |
| suite entière base / corrigé | 383 / 396 OK (2 sauts) ; logs `b2d4f313…`, `ccffc12d…` |
| 15 tests neufs ou modifiés, un par un, sur `rouge` | §4 |
| `regle_fixtures.py`, `render_fixture.py` base / corrigé | `ea3a2d94…cb29` ; `4e62fbb8…9a01`, `d079dd9d…e608` (`render.out` `2e366a91…` identiques) |
| `ast_sans_doc.py`, `fonctions_changees.py` | §6 |
| `mutants_g2.py` (10 suites, 3 en parallèle) | §8 ; `mut/resultats.json` `7ffe7b64…`, `mut-run.out` `19c36b3a…` |
| `survivants.py` | §8 |
| `sonde_diff.py gen` puis `calc` (base, corrigé) ; `compare.py` | §7.2 ; `calc-base.log` `f0fe842d…` (4 exceptions `InvalidOperation` sur N), `calc-corr.log` `5fe456cb…` |
| `rendu_unique.py --produire raw` sur F1-N et F1-Z (jeton posé sur un dossier `.jeton`) | exit 0 ; sorties identiques (`c17b0a65…`) |
| `rendu_unique.py --gardes-seules` (corrigé, base) | §9 ; `gardes-corr.err` `d74ddd3f…`, `gardes-base.err` `b8b19467…` |
| `mutants_3a.py` (8 suites) | §10 ; `mut3a-run.out` `4db8a2cb…` |
| `verif_K.py` ; suite sur `corrK` | §12 ; 398 OK |
| `grep` R-13, imports, longueurs (caractères) sur les diffs | 0 marqueur ; imports : bibliothèque standard et modules du projet ; aucune ligne ajoutée > 120 caractères |

## 16. Attestation D.3 et déclaration FM-1.1

« Le réviseur G2 du lot CORR (`claude-opus-5-5`) n'a vu aucun z, aucun K, aucun P̂_more ni aucun φ de campagne, et n'en a
calculé aucun ; il n'a lu aucun taux d'écart, de présence ou de panne d'une source réelle. Il n'a ouvert aucune pièce de
la liste fermée D.2 (points 1 à 12) ; il n'a rien lu sous `docs/rapports/`, `docs/adr-0025/`, ni
`docs/adr-0028/monark-m009a/`, ni `JOURNAL.md`, ni aucun `*.jsonl` réel ; `SHOGEN_S2_CAMPAGNE_CONTROL` n'a jamais été
posée (absente de l'environnement : `env | grep -c` = 0 ; toutes les exécutions sous `env -u`). Tous les journaux lus ou
produits sont des fixtures de tests ou des journaux synthétiques à graine (les miens, `r2/sonde/j`). Le fichier de
sommes `SHA256SUMS-cloture-2026-09-28.txt` n'a été que hashé et passé en argument, jamais affiché. Le dossier
`g2-corr/interrompu-1/` n'a été ni ouvert ni utilisé. »

Expositions déclarées : comptes de classe M que porte l'annexe D (D.1 n° 7 et n° 9, vus en lisant l.1-170 : plus que
la seule liste D.2) ; D.3 (a) masquée ; noms des pièces de D.2 (liste, brief, G0, journal G1, rapports R-A/R-B/R-C) ;
nom de fichier de D.2 n° 10 dans la sortie d'un `grep P-01` sur l'annexe B (l.50) ; sujets de commits de ce dépôt
(`git log --oneline -8`) ; valeurs de simulation SIM-NIVEAU du paquet l.165-170 (synthétiques).

Écarts de procédure, déclarés :
- **E-1** : une recherche récursive `grep -rln "QUASI-MORT" /home/user/shogen/docs/adr-0028/ --include=*.md` sans
  `--exclude-dir=monark-m009a` (le brief demande ces dossiers exclus à la source). Forme `-l` (noms seuls) ; sortie :
  sept fichiers de `docs/adr-0028/` (aucun sous `monark-m009a/`) ; aucun contenu affiché. Je n'ai pas sondé le dossier
  ensuite.
- **E-2** : des `grep -n` à contenu affiché sur des fichiers nommés et admis de `docs/` (paquet, annexes B et D,
  rapports R-A/R-B/R-C, `biblio/INDEX.md`), au lieu de `-l`/`-c` seuls : lignes listées au §14 ; aucune ne porte de
  z, K, P̂_more, φ ni de taux d'une source.

Occurrences de chemins de D.2 dans **mes appels d'outils** (entrées), pour le contrôle FM-1.1 :
1. l'extraction des copies : `--exclude=docs/rapports --exclude=docs/adr-0025 --exclude=docs/adr-0028/monark-m009a
   --exclude=JOURNAL.md` (deux fois, une commande), puis `test ! -e <copie>/docs/rapports`, `…/docs/adr-0025`,
   `…/docs/adr-0028/monark-m009a`, `…/JOURNAL.md` (contrôle d'absence dans la copie) ;
2. la recherche récursive de E-1 (chemin parent `docs/adr-0028/`, le sous-dossier n'y est pas nommé) ;
3. les écritures de ce rapport (`cat >> … <<'EOF'`), qui citent `JOURNAL.md`, `docs/rapports/`, `docs/adr-0025/`,
   `docs/adr-0028/monark-m009a/` comme noms (§9, §13, §16) ;
aucun autre : aucune lecture, aucun `cat`/`sed`/`grep` sur une pièce de D.2 ; aucun fragment de la cartographie l.51
ni d'ADR-0025 l.14 (jamais ouvertes).

## 17. Verdict : **ACCEPTE-AVEC-CORRECTIONS**

Liste fermée : **K-1** (`tests/test_r2.py`, sous-lot corr-3d) et **K-2** (`tests/test_prix_non_fini.py`, sous-lot
corr-2), §12 : deux tests ajoutés, vérifiés (verts sur l'arbre corrigé, suite 398 OK, chacun rouge sur le mutant
survivant qu'il vise). Aucune correction du code de `shogen_s2` ou de `tools` ; aucune valeur de la règle, aucune
épingle, aucun rendu ne change par elles.

Motifs : le lot est conforme à son G0 (neuf items de CORR-3 moins la docstring de `model.py` retirée par Q-5, CORR-1,
CORR-2), rien de plus (§6) ; CORR-2 est le seul point de lecture des prix et un prix non fini y produit le rendu d'un
`null` à l'avertissement près (§7) ; aucune valeur de la règle ne change pour un prix fini (§5, §7.2) ; chaque test
neuf lié à du code rougit sur `e25d840` et passe après, ceux de 3a tuent les mutants qu'ils visent (§4, §10) ; R-25,
R-13, R-8 tenus ; `--gardes-seules` reste fail-closed (§9). Trois de mes neuf mutants survivent, non équivalents : trous
de test de classe C (C-1 à C-3), que K-1 et K-2 ferment. Hors liste : recommandation C-4 (note sur le journal G1
versé) ; item à former de C-5 (§13) ; L-3 confirmé inatteignable (§7.3).

## 18. Clôture

- Dépôt : HEAD `19eb912`, `git status --short` vide, aucune opération git en écriture, aucune écriture dans le dépôt.
  Seul `__pycache__` du dépôt : `s2-harness/tests/__pycache__/` daté du 2026-10-02 04:36:57Z (ignoré par
  `.gitignore` l.33, déjà signalé par R-C H-2), antérieur à ma passe.
- Copies d'arbre supprimées à la fin (`r2/base`, `r2/corr`, `r2/rouge`, `r2/etats`, `r2/corrK`, dossiers de mutants) ;
  restent dans `g2-corr/r2/` : scripts (`mutants_g2.py`, `mutants_3a.py`, `survivants.py`, `verif_K.py`,
  `ast_sans_doc.py`, `fonctions_changees.py`, `sonde/sonde_diff.py`, `sonde/compare.py`), diff proposé
  `K-corrections.diff`, logs et sorties, journaux synthétiques `sonde/j`.
- R-13 : aucun marqueur de dette nu dans ce rapport ni dans mes scripts.
- Contre-vérification finale de K-1/K-2 : `git archive e25d840 s2-harness` dans une copie neuve (`r2/verifK2`, supprimée
  ensuite), six diffs puis `git apply -p1 K-corrections.diff` : `9 0 tests/test_r2.py`, `10 0 tests/test_prix_non_fini.py` ;
  `unittest tests.test_r2 tests.test_prix_non_fini` : `Ran 48 tests` `OK`.
- Fin de passe : 2026-10-03T00:29Z (`date -u`).
