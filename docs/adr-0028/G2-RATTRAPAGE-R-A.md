# R-A — Relecture G2 de rattrapage : `r1.py`, `records.py`, `window.py`, `model.py` (fichiers entiers, à HEAD)

Mission R-A, partie 4 (P4), SHOGEN-G2-HISTO-RECALCUL-1. Lacunes visées : G-1 (Phase A, ADR-0021), G-2 (`model.py`),
G-4 (CRITERE, lot A, B0), inventaire `INVENTAIRE-G2-RECALCUL.md` §4. Réviseur neuf : je n'ai écrit aucune ligne de ce
code. Rédaction le 2026-10-02 (`date -u` lu à 21:29:44 au départ, à 21:59:04, 22:01:28 et 22:14:44 en cours, et à
22:15:15 avant le remplissage du §9 et le calcul du sha256 de ce fichier). Aucun fichier du dépôt modifié ; aucune opération git en écriture ; aucun correctif
proposé à l'application (code gelé).

## 0. Gate 0, base, périmètre

- **Gate 0** : modèle résolu `claude-opus-5-5` (identifiant exact fourni par l'environnement de la session) ; préfixe
  attendu des workers (CLAUDE.md §7) : conforme ; effort `max` (fiche).
- **Base** : `/home/user/shogen`, branche `partie-4-execution`, HEAD `e586c0bf19360814a4814f00d4665e657ffb3ffa`,
  `git status --short` vide. `git diff --stat 41f087ef3e0a621ddb04fa4f2af8733e5fd5a0f9 HEAD -- s2-harness/shogen_s2
  s2-harness/tools` : vide (rc 0) ; le périmètre revu est donc celui du commit d'analyse scellé (paquet §13). HEAD est
  passé à `5f6dcb616d20f300f9fce8225a074b85311ff0f5` pendant la relecture (`35a601e`, `5f6dcb6`, documents) :
  `git diff --stat e586c0b HEAD -- s2-harness` vide, `git diff --quiet 41f087e HEAD -- s2-harness/shogen_s2
  s2-harness/tools` rc 0, mêmes blobs pour les quatre fichiers : la relecture vaut à la nouvelle tête.
- **Fichiers revus en entier** (à HEAD, = `41f087e`) :

| fichier | lignes | blob | sha256 du fichier |
|---|---|---|---|
| `s2-harness/shogen_s2/r1.py` | 836 | `7ae940ec5812823309e059f5cad4dc2ecbba78bb` (celui que cite le paquet §10.3 l.164) | `791868909992028733318238999f15d44c006e63aa7345df65b8412dd5bfdb5e` |
| `s2-harness/shogen_s2/records.py` | 419 | `f3d95aeb9308e1c86d4232dd9c5fab4053f5d835` | `eab3508083190088d1dde18f2cbded3be92829a7f47212029543146e7ca94abf` |
| `s2-harness/shogen_s2/window.py` | 139 | `1b9da3259fdcafab11e838f477db5e41548f3162` | `f8c3b79f7f7893f343a00b6d6563cbbb502e2bd7af7888db958f895b5bc5fb94` |
| `s2-harness/shogen_s2/model.py` | 70 | `7264d3fea1a4519778c281edc83e82b491f64d46` | `e56240c74be546e631189280711115095a2c9ff48690d28230c6461ff3948480` |

- `model.py`, `window.py` (et `journal.py`) ont à HEAD le **même blob qu'au commit de collecte `ed479c5`**
  (`git rev-parse ed479c5:<f>` = `HEAD:<f>`) : l'écrivain des journaux scellés et le lecteur partagent les mêmes octets
  pour `Status` et pour les strates. `records.py` à `ed479c5` = blob `ef3f7c43…` (référence de format du paquet §1).

## 1. Attestation D.3

> Je n'ai vu aucun z, aucun K, aucun P̂_more ni aucun φ de campagne, et je n'en ai calculé aucun ; je n'ai lu aucun taux
> d'écart, de présence ou de panne d'une source de la campagne, hormis les comptes de Pyth que porte D1 (déclarés
> ci-dessous). Je n'ai ouvert aucune pièce de la liste fermée D.2
> (points 1 à 12, liste lue à l'annexe D §D.2, l.32-47, sans en ouvrir le contenu). Je n'ai ouvert ni `JOURNAL.md`, ni
> `docs/rapports/`, ni rien sous `docs/adr-0025/`, ni aucun `*.jsonl` réel, ni rien hors du dépôt hors de mon dossier.
> `SHOGEN_S2_CAMPAGNE_CONTROL` n'a jamais été posée (toutes les commandes Python sous `env -u`).

Exposé à (déclaré ; classe M ou synthétique, déjà écrit dans des pièces autorisées ; **non recopié ici**) :
- les comptes de classe M que portent ADR-0028 (D1 l.25-26 : comptes de Pyth ; D4 l.52-53 ; D2 pt 6 l.37 ; D5 l.58-60,
  dont les deux pourcentages `resolve_failed`, santé du harnais DNS, D.1 n° 8 ; §1 bis.2 l.121-122), le paquet (§2 l.45,
  §3 l.50, §6 l.68-69 et l.76), l'annexe D (l.173 : nombre de `run_params` ; l.205-207, attestation (j), qui les reprend) ;
- un compte d'opération de réparation (lignes NUL excisées), cité par `docs/G1-partie-2-etape-B-2.md` l.253-254, vu en
  sortie d'une recherche ;
- les sorties synthétiques de SIM-NIVEAU et de l'étape S (paquet §10.3) ;
- des paramètres de conception antérieurs à la campagne : σ et τ par classe de `docs/adr-0022/sigma-tau.json` (affichés
  par une commande), constantes de `r1` et de `collector` ;
- procédure : `git archive HEAD | tar -x` a écrit dans ma copie `docs/rapports/` et `docs/adr-0025/` ; supprimés aussitôt
  (`rm -rf`), sans lecture ; aucune recherche ne les a parcourus. Une recherche (`grep -rn`, motifs « NUL »,
  `--include=*.md --include=*.py`) a parcouru `docs/adr-0028/` **y compris** `docs/adr-0028/monark-m009a/` (un `.py`
  examiné) : aucune ligne de ce dossier n'est apparue en sortie ; ses seuls noms de fichiers ont été listés (`ls`), son
  contenu n'a pas été affiché. Écart de précaution (le rédacteur de l'avis (j) l'avait évité) déclaré pour le contrôle
  FM-1.1 de l'orchestrateur.

## 2. Fichiers lus (niveau [lu] ; lignes)

- Brief `p4/BRIEF-G2-RATTRAPAGE.md` l.1-44 ; inventaire `p4/INVENTAIRE-G2-RECALCUL.md` l.1-311 (entiers).
- Les quatre fichiers du périmètre en entier (§0), deux passes.
- `docs/adr-0028/PAQUET-PREREG-S2.md` l.1-222 (entier) ; `docs/adr-0028/ADR-0028-decisions-sortie-S2.md` l.1-327 (entier).
- `docs/10-mesures-pilotes-design.md` : en-têtes (`grep -n "^#"`), l.376-585 (§5.1-§5.6, début de §6).
- `docs/adr-0028/ANNEXE-D-preenregistrement.md` : en-têtes ; l.32-61 (D.2, D.3 a) ; l.96-123 ; l.124-212 (D.4, D.5,
  attestations g à j).
- `docs/adr-0028/ANNEXE-B-items.md` : l.42, 319, 341, 356, 372, 403, 412, 525, 531, 535 (lignes rendues par `grep`).
- `docs/adr-0028/ANNEXE-A-lots.md` : l.9, 11, 16-18, 64-67, 69, 73-74 (par `grep`, colonnes tronquées).
- `docs/G1-lot-D5-AMEND-descriptifs.md` : l.1, 13, 29, 37-47, 55, 59, 62-63, 73, 77, 81, 127, 135-136, 145 (par `grep`).
- `docs/adr-0022/G2-review.md` (par `grep` : r1, records, verdict) ; `docs/adr-0022/sigma-tau.json` (clés et valeurs).
- Chemin d'appel, hors périmètre, lu pour situer mes fonctions dans la décision : `s2-harness/shogen_s2/report.py`
  l.36-265 ; `s2-harness/tools/rendu_unique.py` l.36-56 ; `s2-harness/shogen_s2/closure.py` l.1-60, l.95-150 ;
  `r2.py` (HEAD) l.900-935 et constantes l.183-256.
- Collecte à `ed479c5` (`git show`), pour établir ce que portent les journaux : `collector.py` l.150-275 ;
  `sources.py` l.84-236, l.296-318, l.378-405 ; `r2.py` l.311-340 (par `grep`) et l.341-380 ; `journal.py` l.29-61
  (par `grep`) ; `r1.py` l.54-57.
- Tests : `test_critere.py` l.1-80 ; `test_r1.py` l.395-440 ; recherches nommées dans `tests/*.py`.

## 3. Commandes et sorties (journal de provenance)

Copie : `git archive HEAD | tar -x -C R-A/arbre` ; toutes les exécutions dans la copie, sous
`env -u SHOGEN_S2_CAMPAGNE_CONTROL PYTHONDONTWRITEBYTECODE=1 python3 -B` (Python 3.11.15) ; 0 `__pycache__` créé
(`find … -name __pycache__` : 0 ; chaque copie de mutant : `pyc=0`). Scripts et sorties dans `R-A/sondes/` (sha256 en §9).

| commande | sortie |
|---|---|
| suite, copie de HEAD (`python -B -m unittest discover -s tests -t .`) | `Ran 383 tests in 39.929s` `OK (skipped=2)` |
| `git rev-parse {ed479c5,HEAD,41f087e}:s2-harness/shogen_s2/{model,window,journal,records,r1}.py` | model, window, journal : même blob aux trois ; records, r1 : HEAD = `41f087e` ≠ `ed479c5` |
| `git show ed479c5:…/collector.py` (l.184-187) et `…/r1.py` (l.54-56) | `run_params` écrits par la collecte : `seuil_historique_valeur = int(SEUIL_HIST)` = 10, `n_min_hors_enveloppe = 4`, `decimal_prec = 50` |
| `sonde2.py` (fonctions unitaires contre références indépendantes) | 10/10 : `window` (2·10⁵ tirages contre `datetime`), `block_long_run_variance` (400 séries à trous contre énumération en Fraction ; numérateur entier égal), `poisson_binomial`, `binomial_tail_ge`, `regle_critere` (35 cas × 1 225 paires), `fenetres_sautees`, `fenetres_sautees_vivant`, `filtre_lecture`/`t_fin_n_fixe`, `read_jsonl_tolerant`, `verifier_raw` |
| `compare.py` graines 1-179 ; 1000-1299 ; `RA_REGIMES=sous3_fort,sous3_fort_dep` 2000-2099 ; `RA_REGIMES=sous3_fort,sous3_fort_dep,dep_net,co_net` 3000-3005 `grand` | §4 : **0 écart** sur 585 journaux |
| `sonde6_d5.py` (hors décision : `recompute_d5_from_journal`, reprises insérées, garde de blocs abaissée dans le processus) | 40 journaux, 0 écart sur s par strate, part « harnais vivant » et bornes de censure (dont 42 strates avec bornes à σ̂_bloc) |
| `sonde4_memoire.py` (table réelle du J28 sur journal synthétique de taille campagne) | `parse_journal` 8,3 s (pic RSS 991 Mio) ; `recompute_from_journal` + `regle_critere` 12,7 s (pic 1 013 Mio) ; référence indépendante : **ÉGALE** |
| `sonde3.py`, `sonde5_rendu_nan.py` | §5, A-1 et C-1 ; `sonde3.py` (c) : pool d'un flux puis vide → garde §5.4, NON ÉVALUABLE, sans exception ; (d) n'a pas produit K = n (D1 a retiré les deux flux toujours en panne) : ce cas reste couvert par la table de `regle_critere` (`sonde2.py`) et par `test_critere` (K = n = 54) |
| `mutants.py` (20 mutants, suite complète chacun) | §6 : 18 tués, 2 survivent |

Incident de méthode, déclaré : au premier passage (graines 1-6), mon comparateur signalait 6 « écarts » sur z ; cause :
il élevait z au carré dans le contexte décimal par défaut (28 chiffres). Corrigé (carré exact en `Fraction`), puis
relancé ; les lots du §4 sont tous postérieurs à la correction. Tous ont tourné sur la version finale de `compare.py`
(sha256 en §9) ; les graines 1000-1299, d'abord passées sur la version précédente (sans les régimes optionnels
`sous3_fort`, `sous3_fort_dep` ni la variable `RA_REGIMES`), ont été rejouées sur la finale : ligne de résultat
identique (`compare-1000-1299.out` et `compare-1000-1299-final.out`, `diff` vide).

## 4. Méthode et résultat de l'oracle indépendant

`sondes/ref.py` est écrit depuis le texte, sans lire ni importer le code revu : garde §5.3 par `datetime` ; segment
[t0 ; t_fin), t_fin = n-ième fenêtre distincte ≥ t0 + w (D2 pt 6) ; exclusion fermée sur `window_start` (D5) ; dernière
lecture de la fenêtre (doc 10 §5.3) ; D1 cas (a) et (b) sur les fenêtres retenues ; classification de doc 10 §5.2
(précédence panne > staleness > hors-enveloppe ; N ≥ 4 ; τ relatif par classe, ADR-0022 ; σ par classe, ADR-0021) en
`Fraction` exacte ; p̂ᵢ, P₀, P₁, P̂_more exacts (doc 10 §5.1) ; σ̂²_bloc par **somme directe** des produits centrés
(n·I_t − K)(n·I_{t+k} − K) sur les paires de la grille (paquet §10.2 pt 3, E-2) ; règle par comparaisons exactes
(z ≥ 2,33 ⇔ num ≥ 0 ∧ num² ≥ 2,33²·garde ; idem z_bloc avec σ̂²) ; « R1 discrimine » et m (pt 6). Comparé à
`r1.recompute_from_journal` + `r1.regle_critere` (le chemin du rendu, `report.render_report` l.161-176, appelle les
mêmes `filtre_lecture`, `analysis_pools`, `compute_r1`, `regle_critere`) : pools par strate, n_s, K_s, p̂ᵢ, P̂_more,
garde, z², σ̂²_bloc, z_bloc², publication de z_bloc, décomposition de K (annexe D.5), valeur et cas par strate,
« R1 discrimine », m. Journaux synthétiques au format du collecteur : 12 flux réels et leurs classes, σ/τ committés,
fenêtres sautées, re-collectes (doublons), lectures orphelines, staleness, prix hors enveloppe, flux mort partout
(Pyth) ou dans une seule strate (cas b), chocs communs iid ou en runs (dépendance sérielle), segment à t_fin ou à n
fixe, plages D5 alignées ou non.

| lot | journaux | écarts | cas couverts (par strate) ; « R1 discrimine » |
|---|---|---|---|
| graines 1-179 | 179 | 0 | garde_5_4 140, z_sous_seuil 121, discordance 3, rejette 1, rejet_non_qualifiable 1 ; FAUX 97, NON ÉVALUABLE 81, VRAI 1 |
| graines 1000-1299 | 300 | 0 | garde_5_4 237, z_sous_seuil 199, discordance 7 ; FAUX 155, NON ÉVALUABLE 145 |
| graines 2000-2099 (chocs forts) | 100 | 0 | rejette 12, rejet_non_qualifiable 18, discordance 11, garde_5_4 104 ; VRAI 12, FAUX 9, NON ÉVALUABLE 79 |
| graines 3000-3005, **constantes de production** (ℓ = 240, garde de blocs 30·ℓ, 4 000 à 17 000 fenêtres par strate) | 6 | 0 | rejette 6, rejet_non_qualifiable 3 (dont n_s < 7 200), discordance 1, garde_5_4 2 ; VRAI 4, NON ÉVALUABLE 2 |
| sonde 4 : **table réelle du J28** (T0, n fixe et plage D5 de `rendu_unique.py` l.39 et l.46) sur journal synthétique de taille campagne (12 flux, ≈ 5·10⁵ lectures, 114 Mo) | 1 | 0 | z_sous_seuil ×2, z_bloc publié dans les deux strates ; FAUX |

Pour les petits journaux, la garde de blocs est abaissée dans le processus de la sonde (`r1.GARDE_BLOCS` ∈ {1, 2, 3, 25},
référence au même paramètre) afin d'atteindre les cinq cas ; ℓ reste 240. Les deux derniers lots tournent aux
constantes de production, sans aucune modification.

**Conclusion de l'oracle** : sur tout journal sans prix non fini, le chemin de la règle (pool D1, segment, exclusion D5,
classification des écarts, P̂_more, z, σ̂²_bloc, z_bloc, `regle_critere`) rend les mêmes pools, n_s, K_s, décomposition
de K, valeurs, cas, « R1 discrimine » et m que la référence exacte, avec p̂ᵢ, P̂_more, garde et σ̂²_bloc à 10⁻⁴⁴ près en
relatif, z² et z_bloc² à 10⁻⁴⁰ près (le code calcule en `Decimal` à 50 chiffres ; aucune comparaison au seuil n'a
basculé ; dans `sonde2.py`, le numérateur entier ℓ·n²·σ̂²_bloc est exactement égal à celui de l'énumération).

## 5. Constats

### A-1 — prix non fini dans une lecture « ok » : exception non nommée sur le chemin de la décision (A conditionnel ; plausibilité très faible [inféré])

- **Où** : `r1.py` l.180-181 (le prédicat de panne ne regarde que le statut et l'absence de prix), l.102-110 (`_median` :
  `sorted` sous `contexte_decimal()`, qui piège `InvalidOperation`), l.194, l.207 ; même prédicat dans
  `analysis_pools` l.433 et `compute_r1` l.572.
- **Scénario** : une ligne de `journal.jsonl` `{"status": "ok", "price": "NaN", …}` (ou `"nan"`, `"sNaN"`) dans une
  fenêtre retenue où au moins quatre flux répondent → la comparaison de tri lève `decimal.InvalidOperation` →
  `report.render_report` (run `j28`, et `j14-*` si la fenêtre est dans leur segment) et `r1.recompute_from_journal`
  (run `recalcul-tiers`) échouent ; l'enregistreur s'arrête au premier échec et rien ne reste (paquet §9 ; §12 pt 3).
  Aucune valeur fausse n'est rendue (arrêt, pas biais).
- **Preuve** : `sondes/sonde5_rendu_nan.py` (sortie `sonde5.out`) : journal synthétique à 12 flux, segment à n fixe et
  plage D5 ; intact → rendu produit ; une seule lecture `okx_index` à `"NaN"` → `decimal.InvalidOperation`, pile
  `r1.py:compute_r1:566 > _classify_window:465 > classify_ecart:194 > _median:106`. `sondes/sonde3.py` (a) : même
  exception pour `"NaN"`, `"nan"`, `"sNaN"` ; `"Infinity"` et `"-Infinity"` ne lèvent pas dans le cas courant : la
  cellule est un écart (hors-enveloppe, comme le serait une panne pour p̂ et K), le prix infini entre dans les médianes
  des autres flux de la fenêtre et τ observé `max` vaut Infinity ; deux prix infinis dans la même fenêtre lèveraient
  (médiane infinie, Inf/Inf).
- **Atteignabilité** : les décodeurs de la collecte (`sources.py` à `ed479c5` l.125-215) font `Decimal(str(…))` sans
  contrôle de finitude, et `_loads` (l.84-90) laisse `json` accepter les jetons `NaN`/`Infinity` ; une réponse HTTP 200
  portant un prix `"NaN"` aurait donc été journalisée au statut `ok`. Les `source_ts` sont, eux, tous dérivés d'entiers
  ou d'ISO (l.132-215) : finis, d'où aucun risque sur la staleness.
- **Rapport au texte** : doc 10 §5.2 (iii) range l'« indécodable » en panne ; le chemin de recalcul ne requalifie pas un
  prix qui n'est pas un décimal fini et lève sans refus nommé. Le dépôt nomme déjà ce défaut pour les horodatages de `control.jsonl`
  (`records.py` l.369-372, refus nommé SHOGEN-BLOC6-TS-NUM-1, G2 C-8 de la partie 2 ; `test_lecteur.py` l.105-113),
  pas pour les prix de `journal.jsonl` (aucun test : `grep` de `NaN|Infinity|nan` dans `tests/*.py`).
- **Plausible sur des journaux réels ?** Très faible [inféré] : aucune des douze API n'est connue pour servir un prix
  non fini ; non vérifiable ici (journaux scellés interdits, D.2 n° 7, D.4 a). Si le cas se présente, c'est le « cas
  non prévu » du pt 11 (déviation déclarée), après une tentative échouée.
- Item à former : §7, I-1.

### B — aucun

Rien trouvé qui fausse un rendu hors décision : bloc 2 (`classify_cells`, même aide que R1), décomposition de K et c_s
(égales à la référence sur tous les journaux), τ observé (C-4), fenêtres sautées et part « harnais vivant » (énumération
directe de la grille, `sonde2.py` et `sonde6_d5.py`), bornes de censure (formules de l'annexe D.5, `sonde6_d5.py`),
strate poolée, `verifier_raw` (accepte un couple cohérent, refuse
cinq altérations), `demarrages` (la double ouverture `run_params` puis `clock_check` « startup » de la collecte crée un
démarrage vide, ignoré par `fenetres_sautees_vivant`).

### C — sans effet sur les sorties (ou interprétation documentée)

- **C-1 (D1, « lectures ok »)** `r1.py` l.421-438 : ok(f, s) compte la **dernière** lecture de chaque fenêtre retenue
  (`build_reading_map`, l.412-418), pas toutes les lignes. Lecture conforme à doc 10 §5.3 (« 1 relevé/source/fenêtre :
  le dernier de la fenêtre »), écrite dans la docstring. Elle ne diffère d'un comptage de toutes les lignes que si les
  seules lectures `ok` d'un flux dans une strate ont toutes été remplacées par une re-collecte : `sonde3.py` (b) le
  construit (le flux est retiré, P̂_more et K changent) ; non plausible sur la campagne [inféré : ADR l.25, seul Pyth
  est sans aucune lecture `ok`, sur le journal entier].
- **C-2 (bords non épinglés par la suite)** : mutants M1 (`>` → `>=` pour la staleness, l.188-189) et M4 (`<` → `<=`
  pour la garde §5.4, l.632) survivent. Le code est conforme au texte (doc 10 §5.2 « > σ_classe » ; « < 10 » du pt 2).
  L'égalité à la garde est de mesure nulle ; l'égalité de staleness est possible pour les sources à horodatage entier
  (Bitstamp, CoinGecko, DefiLlama, Chainlink, σ entiers), et le code y rend « pas de staleness », comme le texte.
- **C-3 (commentaires de `records.py`)** : l.10 « Trois types » (il y en a quatre depuis `asn_attribution`) ; l.41-42
  « Les sept premiers sont les entrées de compute_r1 » : `decimal_prec` n'en est pas une (r1 calcule à `DECIMAL_PREC`
  sans comparer la valeur du journal) et `n_min_hors_enveloppe`, huitième, en est une. Sans effet : la collecte a écrit
  `decimal_prec = DECIMAL_PREC` = 50 (`collector.py` l.187 et `r1.py` l.54 à `ed479c5`).
- **C-4 (population de τ observé)** `r1.py` l.583-585, l.237-247 : seules les cellules arrivées à l'axe (i)
  (hors-enveloppe ou pas d'écart) entrent ; une cellule en staleness à prix connu n'y entre pas. Choix fixé par la
  décision D-2 (C-5) du G1 de D5-AMEND, revu au G2 du lot ; le texte de l'annexe D.5 et du paquet §11 ne précise pas la
  population. À noter pour PX-Shogen-13 : la clôture de calibration (`closure.py` l.120-147) prend **toutes** les cellules
  à enveloppe définie, staleness comprise ; les deux P99 ne portent pas sur la même population.
- **C-5 (`model.py` et la frontière de D6)** : la docstring (l.4-5) dit l'instrument « JETABLE » et ADR-0028 D6 (i)
  range `model` dans la collecte en quarantaine, alors que `r1` (chemin de recalcul) l'importe (`r1.py` l.55, l.76).
  Sans effet : le seul usage est la chaîne `"panne_transport"`, identique à l'écriture (même blob qu'à `ed479c5`) ;
  M19 montre que la suite épingle cette chaîne.
- Relu sans constat : `window.py` en entier (convention demi-ouverte, `weekday_utc` contre `datetime` sur 2·10⁵ tirages,
  garde §5.3 sur tous les marqueurs avant filtre) ; `records.filtre_horodatage`, `filtre_lecture`, `t_fin_n_fixe`,
  `exclusion_ranges` (bornes D4/D5 conformes au paquet §3 et §6) ; `read_jsonl_tolerant` (fins de ligne universelles,
  dernière ligne coupée tolérée, ligne illisible non finale refusée ; les lignes NUL des journaux scellés ont été
  excisées par les réparations [2nd : `docs/G1-partie-2-etape-B-2.md` l.253]) ; `effective_run_params` (les
  `run_params` de la collecte portent 10 et 4, [lu] `collector.py` l.184-185 à `ed479c5`) ; `poisson_binomial` exact ;
  `block_long_run_variance` (formule N = ℓ·n²·σ̂² vérifiée terme à terme ; σ̂² = (1/ℓ)·Σ B_j² ≥ 0, donc aucune racine
  négative) ; `bloc_strate` ; `regle_critere` (pts 4, 5, 6 et EMD du pt 8, table exhaustive) ; `strate_poolee` hors de
  `r1_out["strates"]` (pt 9).

## 6. Mutants (copie de l'arbre, suite complète, 383 tests)

| | mutation | résultat | tué par (premiers tests) |
|---|---|---|---|
| M1 | staleness `> σ` → `>= σ` (`r1.py` l.189) | **survit** | — (C-2) |
| M2 | staleness mesurée à `ws` au lieu de t_fin(j) (l.466) | tué (1) | `test_no_false_staleness_realistic_sigma` |
| M3 | enveloppe `N >= 4` → `N > 4` (l.193) | tué (9) | `test_horsenv_requires_four_responding`, … |
| M4 | garde §5.4 `< 10` → `<= 10` (l.632) | **survit** | — (C-2) |
| M5 | D1 : toute lecture comptée ok (l.433) | tué (10) | `test_a_flux_mort_partout_hors_r1_lm_r2_aux_quatre_points`, … |
| M6 | D1 cas (b) ignoré (l.557) | tué (5) | `test_b_mort_en_stress_seul_retire_de_cette_strate_seulement`, … |
| M7 | σ̂²_bloc sans le lag ℓ − 1 (l.347) | tué (8 + 1 erreur) | `test_couture_l3_valeurs_critique`, … |
| M8 | garde de blocs `n < 30·ℓ` → `n <= 30·ℓ` (l.382) | tué (6) | `test_garde_de_blocs_frontiere_et_garde_5_4`, … |
| M9 | « R1 discrimine » FAUX malgré un rejet non qualifiable (l.703) | tué (1) | `test_r1_discrimine_m_et_poolee` |
| M10 | EMD sans le plancher σ̂_bloc (l.696) | tué (4) | `test_j2_k0_negatif_et_emd_sigma_bloc`, … |
| M11 | P̂_more = 1 − P₀ (l.225) | tué (42 + 2) | `test_bloc3_tau_decomposition_bornes`, … |
| M12 | D5 `[A ; B]` → `[A ; B)` sur `window_start` (`records.py` l.376) | tué (22) | `test_bornes_egales_une_seule_fenetre`, … |
| M13 | D5 sans l'extension `B + w` pour `ts`, `harness_ts` (l.378) | tué (9) | `test_asn_retirees_ventilees_par_statut_sur_l_assiette`, … |
| M14 | n fixe compté à partir de `> t0` (l.388) | tué (3 + 1) | `test_forme_j28_cli_segment_n_fixe_et_plages`, … |
| M15 | segment `[t0 ; t_fin)` → `[t0 ; t_fin]` (l.373) | tué (4) | `test_bornes_tous_types_aux_quatre_points_et_cli`, … |
| M16 | lecteur : toute ligne illisible tolérée (l.96) | tué (2) | `test_corrupt_non_final_line_raises`, … |
| M17 | jour de semaine décalé (`window.py` l.95) | tué (81 + 13) | … |
| M18 | garde §5.3 neutralisée (`window.py` l.130) | tué (5) | `test_garde_53_sur_tous_les_marqueurs`, … |
| M19 | valeur de `Status.PANNE_TRANSPORT` (`model.py` l.35) | tué (2) | `test_dk_composantes_somme_inclusions`, `test_pool_un_flux_c_hors_de_K` |
| M20 | garde médiane_LOO `<= 0` → `< 0` (l.199) | tué (1 erreur) | `test_median_zero_guard_is_non_evaluable` |

Ajout aux mutants : aucun test de la suite ne porte un prix non fini (A-1) ; un mutant « prix non fini » n'est donc pas
constructible contre la suite actuelle.

## 7. Limites rendues comme items à former (règle PAROXYSME)

- **I-1 (de A-1), proposé : SHOGEN-PRIX-NON-FINI-1** : avant l'exécution unique, l'orchestrateur choisit entre (i) la
  limite écrite (un prix non fini fait échouer la tentative, consignée, puis déviation déclarée au sens du pt 11), et
  (ii) un comptage nommé « comptes seulement » des prix non finis de `journal.jsonl` sous D.4 a (aucun prix ni statut en
  sortie), par l'orchestrateur seul. Propriétaire : orchestrateur ; déclencheur : avant l'exécution unique. Je ne tranche
  pas (code gelé, lecture des journaux hors de mon rôle).
- **I-2 (de C-2)** : tests de bord manquants (égalité de staleness à σ_classe ; garde à exactement 10) et d'un prix non
  fini ; déclencheur : premier G0 qui touche `classify_ecart` ou la suite après S2 (la garde (2) du rendu couvre
  `shogen_s2` et `tools`, non `tests`, mais la suite tourne dans l'exécution : ne rien ajouter avant).
- **I-3 (de C-4)** : PX-Shogen-13 déclare que τ observé (axe (i) atteint) et le P99 de calibration (`closure.py`, toutes
  cellules évaluables) ne portent pas sur la même population.
- **Information pour SHOGEN-RENDU-COUT-1 et -TABLE-REELLE-1** (pas un constat) : la partie R1 de la table réelle du J28
  tourne de bout en bout sur un journal synthétique de taille campagne (sonde 4 : ≈ 21 s, pic ≈ 1 Gio pour 5·10⁵
  lectures, soit ≈ 2 Ko de mémoire par lecture chargée) et rend les valeurs de la référence. R2, L&M et le rendu complet
  ne sont pas mesurés ici (hors périmètre).
- **Hors de mon périmètre, non revu** : l'impression des valeurs de la règle et des énoncés du pt 8 par `report.py`,
  `r2.drapeau_2`, les décodeurs de `sources.py` (lus seulement pour l'atteignabilité d'A-1). Les diffs historiques des
  commits de Phase A ne sont pas relus ligne à ligne ; seul l'état de HEAD l'est, ce qui couvre ce qui produit les sorties.

## 8. Verdict

**CONSTAT-A** — un seul A, **conditionnel** (A-1 : exception non nommée sur un prix `NaN` dans une lecture « ok »,
plausibilité très faible [inféré] ; effet : arrêt de l'exécution, pas une valeur fausse) ; aucun B ; cinq C. Sur tout
journal sans prix non fini, le chemin de la règle SHOGEN-CRITERE-R1-1 revu ici (pool D1, segment, exclusion D5,
classification des écarts, P̂_more, z, σ̂²_bloc, z_bloc, `regle_critere`) rend les valeurs d'une référence indépendante
écrite depuis le texte scellé (§4), y compris aux constantes de production et sur la table réelle du J28 à l'échelle de
la campagne (journaux synthétiques).

## 9. Empreintes des preuves (`R-A/sondes/`)

| fichier | sha256 |
|---|---|
| `sondes/compare-1-179.out` | `9eea0a177ec4404c5a8cf54c4ae1589dc543dc6b6b0cd9b4f6a0cff2ab5ea0f5` |
| `sondes/compare-1000-1299-final.out` | `31f66c169ffa73740d361a86eb24ba69b45a31f9ac18d21290869b506dade4ee` |
| `sondes/compare-1000-1299.out` | `2622268f61661829b8121f7ce7ff6d0a743eee6a59b7ec5a058e15e98fd9e7bd` |
| `sondes/compare-2000-2099.out` | `15838263cdb807503d9a8111438df0bbc7c7ba6d8c29884e1205f7531b844fc2` |
| `sondes/compare-grand-3000-3005.out` | `d6aca9239437f33c835b8433074a6a27351c4fff167cbdcae718a95efb45502c` |
| `sondes/compare.py` | `cb0bb22f65f2378ad6b6aff7fa40cc3044aeb3ee014c35aa3498d8098f96b0f4` |
| `sondes/mutants.out` | `c5a6e03fc0807f4aff307a67760dc43acd0109331196f9fe31f718526f5ad5a6` |
| `sondes/mutants.py` | `bbdd41aeae4afc78e1633e2c37c2ec7ff76981bfd1c893b530ec164fed58d8e4` |
| `sondes/ref.py` | `bda10f2f894576a71239f5ae639278e0e0cb22719884373e462e5140a0f39605` |
| `sondes/sonde2.out` | `04dfaeee32ff9fc7fdcf3d15106c96d3823566bdacefd755d3535c1af7266edf` |
| `sondes/sonde2.py` | `18bfea1eb979d6802c312bf4e0b1a31cdd5166a73bb973846d54a07577666778` |
| `sondes/sonde3.out` | `413b31dce7dc8b400855060420220a96affcf6029c701fc70497f06f88b5b60e` |
| `sondes/sonde3.py` | `cf77681b333f15057bc62684b74c229d343ff570b17ad084e4012eccd6a2a0a6` |
| `sondes/sonde4-gen.out` | `d250e65033bcc159f8f6ce51a98dd81d4b76338952956782cb2033ddfd47391a` |
| `sondes/sonde4-mesure.out` | `8a47f7d24f34f12f7d4581f21af01b36d10a6d27b5bef0f7deb6e17cd4ba2112` |
| `sondes/sonde4_memoire.py` | `eaf006a2628e0c8c876ee94e57083433e044a8c920a4ac7fe940b27190abee21` |
| `sondes/sonde5.out` | `a4be126e55ef5595d5d592bae94ae39d7dd689e5d0cf4813723e911505424227` |
| `sondes/sonde5_rendu_nan.py` | `da498b33d8e8655f3dd610f69cc008da61fcf99bab2f891fd1a321c3b2794aee` |
| `sondes/sonde6.out` | `61abb19f995071842654a9ea5e8769bac7c3b4b581c26838c991af828dac8769` |
| `sondes/sonde6_d5.py` | `f0d75a5330a9061af0441e015e48a457ced5319dc2501c61eb151dcc83add3d1` |
