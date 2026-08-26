# Revue G2 — τ scalaire → PAR CLASSE (ADR-0022)

- **GATE 0 (R-1)** : modèle résolu `claude-opus-4-8[1m]` — préfixe `claude-opus-4-8` conforme.
- **Rôle** : relecteur G2, instance séparée (≠ générateur), contexte frais. LECTURE SEULE sur F:\Shogen ; écriture scratchpad seule.
- **Oracle** : `python -m unittest discover -s tests -t .` → **Ran 173 tests … OK** (rejoué moi-même).
- **Sonde adversariale** (import du VRAI code, entrées adverses, zéro écriture sur F:\Shogen) :
  `scratchpad\tau-facts\g2_probe.py` → **17 pass / 0 fail** (rejouable : `cd F:\Shogen\s2-harness && python …\g2_probe.py`).
- **Verdict** : points 1-5 et 7 **PASS** (correction fonctionnelle prouvée). Point 6 : code fail-closed sain,
  MAIS **scope rogné SANS déclaration = D1**. Deux obsolescences doc in-diff = **D2**.
  **PAS de PASS G2 propre tant que D1 + D2 ne sont pas corrigés** — aucun blocage ne porte sur le comportement du code.

---

## Point 1 — Dispatch : miroir fidèle + précédence — PASS

- `_tau_for_flux` (`r1.py:113-127`) est le **miroir exact** de `_sigma_floor_for_flux` (`r1.py:95-110`) :
  `klass = sigma_class_of_flux.get(flux_id)` → `if klass is None: return None` → `return {tau_by_class|sigma_by_class}.get(klass)`.
  Vérifié structurellement par sonde (`_tau_for_flux mirrors _sigma_floor structure`) et sémantiquement :
  flux inconnu→None, classe-sans-τ→None, présent→τ de la classe (3 probes vertes).
- `classify_ecart` applique le τ de la BONNE classe : `tau_flux = _tau_for_flux(flux_id, tau, sigma_class_of_flux)`
  puis `abs(price - m_loo)/m_loo > tau_flux` (`r1.py:185-190`). τ dispatché par flux→classe→τ.
- **Précédence panne > staleness > hors-enveloppe préservée** : panne `r1.py:163` (retour immédiat) ;
  staleness `r1.py:169-173` (avant le bloc enveloppe) ; le dispatch τ est DANS le bloc `n_responding >= n_min`
  (`r1.py:176-192`), donc strictement APRÈS staleness. Aucune réordonnance. Probes PAS_ECART / HORS_ENVELOPPE / STALENESS vertes.
- Threading : les 6 signatures sœurs (`_classify_window` `r1.py:311`, `classify_cells` `:341`, `compute_r1` `:365`,
  `lm.compute_lm` `lm.py:117`, r2 `r2.py:918/1036`, report) passent `tau` en pass-through vers `classify_ecart`.
  **Aucun consommateur ne déréférence le mapping comme scalaire** (grep exhaustif : seuls `_tau_for_flux`/`classify_ecart`/
  `collector.py:177`/`records.py:179` l'itèrent/dispatchent ; `closure` garde son propre `tau_base` scalaire SÉPARÉ,
  jamais le mapping threadé — `closure.py:106` jette `_tau`). Risque MAST step-repetition (a) écarté, preuve à l'appui.

## Point 2 — Garde fail-closed legacy τ — PASS

- `records.effective_run_params` (`records.py:145-151`) lève `ValueError("… SCALAIRE legacy …")` si
  `tau_classe` n'est pas un `dict` — miroir exact de la garde σ (`records.py:134-141`).
- **Le test mord RÉELLEMENT** : `test_legacy_scalar_tau_classe_fails_closed` (`test_closure.py:197-211`) mute
  le run_params vers `tau_classe = "0.005"` (scalaire str) puis exige `compute_closure` → `assertRaisesRegex(ValueError, "SCALAIRE legacy")`.
  La mutation ne laisse PAS σ scalaire (sigma_classe reste mapping via `_clean`) → c'est bien la garde τ qui mord, pas la garde σ.
- **La garde est load-bearing (prouvé)** : sonde `sigma_tau_from_params on scalar -> AttributeError`. Sans la garde,
  `effective_run_params` passerait, puis `records.py:179` (`params["tau_classe"].items()`) lèverait `AttributeError`
  (type ≠ ValueError, message ≠ "SCALAIRE legacy") → le test ÉCHOUERAIT. Donc le test discrimine réellement présence/absence de la garde.

## Point 3 — Loader campagne `_load_committed_sigma_tau` — PASS

`run_campaign.py:107-139`, tout vérifié + prouvé par sonde :
- **mapping** : `tc is None` → lève « EN ATTENTE » (`:108-113`) ; `not isinstance(tc, dict)` → lève « jamais un scalaire » (`:114-118`).
  Probes `loader null tau raises` + `loader scalar tau raises`.
- **garde `0<τ<1` PAR CLASSE** : boucle `for k,v in tc.items()` → `if not (0 < Decimal(str(v)) < 1): lève` (`:119-128`).
  Probe `loader tau out-of-(0,1) raises` (τ=50 rejeté).
- **COMPLÉTUDE** : `missing = [k for k in sigma_by_class if k not in tau]` → lève si non vide (`:130-137`).
  Chaque classe de σ (y compris σ=None, ex. `sans_horodatage`) DOIT porter un τ → l'axe hors-enveloppe reste
  évaluable pour les classes à σ=None. Probes `loader incomplete tau raises` + `loader valid: sans_horodatage sigma=None but tau present`.
- **fail-close scalaire** : couvert par `isinstance(tc, dict)`.
- Résidu MINEUR (pré-existant, non-bloquant) : un τ NON numérique (`{"c":"abc"}`) → `Decimal("abc")` lève `InvalidOperation`
  (non `SigmaTauNonRepresentable`) → traceback au lieu du message propre. Identique au chemin σ (`:129`), non introduit par cette passe. Fail-closed quand même (la campagne ne démarre pas).

## Point 4 — Sérialisation `collector.py` + concordance §E — PASS

- `collector.py:177` : `"tau_classe": {k: str(v) for k, v in tau_classe.items()}` — MAPPING recalculable
  (`str(Decimal)` exact, aucun flottant).
- **Concordance §E (reprise idempotente) tient** : `effective_run_params` compare `p.get("tau_classe") != base.get("tau_classe")`
  sur des `dict` parsés — l'égalité de dict Python est **indépendante de l'ordre des clés**. Donc un ré-ordre de
  sérialisation entre démarrages NE flaggue PAS de divergence, et une VRAIE divergence de valeur flaggue.
  Prouvé par sonde : `§E same tau mapping different key order -> concordant (passes)` ET `§E divergent tau -> raises 'divergents'`.

## Point 5 — Changement sémantique (flux sans classe) — PASS

- `r1.py:185-189` : `tau_flux = _tau_for_flux(...)` ; `if tau_flux is None: return Ecart.NON_EVAL_HORSENV`.
  Flux sans classe → τ=None → **NON_EVAL_HORSENV** (était PAS_ECART sous τ scalaire).
- **CORRECT + fail-closed** : PAS_ECART était un fail-OPEN (l'ancien commentaire l'avouait) ; NON_EVAL est plus conservateur
  (n'alimente pas φ). Le nouveau test `test_unknown_flux_both_axes_non_evaluable` (`test_r1.py:437-446`) acte NON_EVAL_HORSENV.
- **Test non trivial** : la sonde trace que NON_EVAL provient SPÉCIFIQUEMENT de la branche τ=None (`r1.py:189`), pas du
  garde médiane ni de staleness (probe `classify unknown flux -> NON_EVAL_HORSENV`). Une régression vers PAS_ECART serait captée.

## Point 6 — closure.py NON modifié — CODE SAIN, mais D1 (déclaration)

**Défense côté code — SOLIDE et prouvée** :
- `closure.compute_closure` passe par `records.effective_run_params` (`closure.py:97`) → la garde τ-scalaire-legacy
  mord sur le journal de CALIBRATION legacy (rupture ADR-0003 C4 déclarée dans l'ADR — comportement VOULU, tag `36593b6`).
- La sortie de closure `tau_classe` reste scalaire `0.005` ou `None` (`closure.py:173`) = son ASSESSMENT de révision.
- **Aucun chemin où closure produirait un sigma-tau.json campagne VALIDE-mais-faux** : le loader REJETTE les DEUX branches —
  scalaire (`0.005`) → `not isinstance(dict)` lève ; `null` → « EN ATTENTE » lève. Probes `loader scalar tau raises` + `loader null tau raises`
  couvrent exactement ces deux sorties. Le fichier committé est ASSEMBLÉ (σ clôture + τ ADR), prouvé par le `test_roundtrip` réécrit.
- De plus, avec les données à queue lourde (P99 global ≈ 0,375 % > 0,25 %), `tau_revision_needed` est en pratique
  toujours vrai → closure émet toujours `tau_classe=None` → fail-close permanent du loader → assemblage humain FORCÉ. Fail-SAFE.

**D1 — DÉFAUT DE DÉCLARATION (zéro dette)** : ADR-0022 **ligne 48** (Conséquences item 1) liste explicitement
« `closure` clause de révision PAR CLASSE » parmi les livrables CODE de CETTE passe. L'implémentation ne l'a PAS faite,
et **le diff est muet sur l'abandon**. La ligne 50 (Régime) invoque `closure.tau_revision_needed` « (fail-closed, **existant**) » —
c'est une tension INTERNE à l'ADR (hypothèse pré-implémentation), PAS une déclaration que l'item est différé/coupé.
Vérifié : aucun journal de provenance ni note de report dans scratchpad ne déclare l'abandon (le rapport G1 n'est pas encore écrit).
Sous la règle Dettes du référentiel, un item de plan non livré ET non déclaré = **défaut de la passe** (« scope silencieusement rogné » — c'est précisément le cas).
- **Correction exigée (côté orchestrateur/ADR, PAS le code)** : un amendement ADR-0022 (ou note de provenance) qui **acte le report**
  de la clause de révision par-classe de `closure` vers la passe de re-dérivation post-week-end, avec justification =
  (sortie closure = assessment seul + fail-close du loader prouvé, cf. `g2_probe.py` et `test_roundtrip_closure_to_campagne_resolve`).
  Rien ne bloque sur le comportement du code ; le blocage d'un PASS propre est ce paragraphe de déclaration.

## Point 7 — Tests affaiblis ? — PASS (aucun test trivialement vrai)

- Adaptateurs `_taumap` (`test_collector.py:68-71`, `test_r2.py:46-49`, `test_report.py:38-41`) et `_tbc` (`test_r1.py:71-74`) :
  diffusent un τ scalaire sur le mapping par classe du flux — **fidèles à l'intention** (le même τ appliqué via la classe).
  Le collecteur exige désormais un `dict` (`.items()`) : un scalaire lèverait `AttributeError` → les adaptateurs exercent le vrai contrat.
- `test_unknown_flux_both_axes_non_evaluable` : **renforcement** (PAS_ECART fail-open → NON_EVAL fail-closed), pas affaiblissement.
- `test_roundtrip_closure_to_campagne_resolve` réécrit (`test_closure.py:216-236`) : prouve encore l'ASSEMBLAGE RÉEL —
  exécute le VRAI `closure.compute_closure`, prend son σ RÉEL (`res["sigma_classe"]`), l'assemble avec le τ ADR, écrit le fichier,
  résout via le VRAI `resolve_sigma_tau`, et asserte (a) σ round-trip depuis closure (`sigma_by_class["place_horodatee"] == res[...]`,
  `sigma_by_class["sans_horodatage"] is None`), (b) τ = valeurs ADR. La fidélité closure→loader (σ) est PRÉSERVÉE ; seul
  l'assert τ passe des valeurs closure aux valeurs ADR (correct : closure ne fournit plus le τ campagne). Non trivial.
- `test_run_campaign` : asserts renforcés en PAR CLASSE (`tau["agregateur"]==0.026`, `tau["place_horodatee"]==0.0045`).

**Cross-check table ADR (piège 100× nommé)** : `test_closure.py:229-231` code en dur
`oracle_pyth 0.0015, place_horodatee 0.0045, sans_horodatage 0.0045, oracle_chainlink 0.0165, agregateur 0.026` —
correspond exactement à la table ADR (0,15 % / 0,45 % / 0,45 % / 1,65 % / 2,60 %), conversion pourcent→fraction (÷100) CORRECTE. Pas d'erreur 100×.

---

## D2 — OBSOLESCENCES DOC IN-DIFF (à corriger dans le diff, sans effet comportemental)

1. **Annotations de retour périmées** : `run_campaign.py:82` (`_load_committed_sigma_tau`) et `run_campaign.py:145`
   (`resolve_sigma_tau`) déclarent encore `-> tuple[dict, Decimal, str]` ; les DEUX rendent désormais `(dict, dict, str)`
   (τ = mapping). Le générateur a mis à jour les docstrings ET les types de paramètres (collector.py:104, lm.py:117, r1.py, run_segment `tau: dict`)
   mais a **manqué ces 2 annotations de retour**. Correction : `-> tuple[dict, dict, str]`.
2. **Claims de provenance périmés** :
   - `run_campaign.py:25` (docstring module) : « `tau_classe` (FRACTION) » — décrit encore un scalaire ; ADR-0022 = mapping classe→fraction.
   - `run_campaign.py:83-84` et `:154` : décrivent le fichier committé comme « artefact `shogen_s2.closure` » / « artefact `closure` » —
     or c'est précisément la sortie BRUTE que le loader REJETTE maintenant (τ scalaire/null). Le fichier réel est ASSEMBLÉ (σ clôture + τ ADR).
     Le libellé CORRECT existe déjà à `:138-139` (« clôture + ADR τ par classe ») — aligner :83-84/:154/:25 dessus.
   Correction : purement documentaire (annotations + docstrings), aucun changement de comportement.

---

## Synthèse

| Point | Verdict | Preuve principale |
|---|---|---|
| 1 Dispatch/précédence | PASS | r1.py:113-127 miroir de :95-110 ; dispatch r1.py:185-190 ; sonde 6 probes |
| 2 Garde legacy τ | PASS | records.py:145-151 ; test_closure.py:197-211 ; load-bearing prouvé (probe AttributeError) |
| 3 Loader campagne | PASS | run_campaign.py:107-139 ; 5 probes (scalaire/range/complétude/null/valide) |
| 4 Sérialisation + §E | PASS | collector.py:177 ; concordance ordre-indépendante (2 probes §E) |
| 5 Changement sémantique | PASS | r1.py:185-189 ; test_r1.py:437-446 ; probe NON_EVAL ciblé |
| 6 closure non modifié | **D1** | code fail-closed sain (probes scalaire+null) MAIS drop non déclaré de l'item ADR l.48 |
| 7 Tests non affaiblis | PASS | adaptateurs fidèles ; roundtrip prouve l'assemblage réel ; cross-check 100× OK |

**DÉFAUTS** :
- **D1 (bloquant PASS propre — correction côté ADR/orchestrateur)** : déclarer le report de la clause de révision
  par-classe de `closure` (item ADR-0022 l.48) — le code ne bloque pas, la déclaration manque.
- **D2 (in-diff, documentaire)** : run_campaign.py:82 & :145 annotations `Decimal`→`dict` ; run_campaign.py:25/:83-84/:154 claims périmés.

Aucune correction manquée sur le COMPORTEMENT, aucune garde fail-closed absente, aucun test trivialement vrai.
