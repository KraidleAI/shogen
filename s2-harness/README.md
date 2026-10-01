# s2-harness — l'instrument de mesure pilote S2 (chemin de recalcul sous G0-G7 ; collecte en quarantaine « jetable »)

Conception : [`docs/10-mesures-pilotes-design.md`](../docs/10-mesures-pilotes-design.md).

Cet instrument tranche la question de S2 (`05-roadmap.md` §S2) : les axes R2
sont-ils observables en pratique, et le test R1 discrimine-t-il quelque chose
sur données réelles ?

**Statut (ADR-0028 D6, 2026-09-29)** : le **chemin de recalcul** (`records`
hors `append_asn`, `window`, `r1`, `lm`, `r2` hors `collect_asn`, `report`, et leurs tests) est de
qualité produit, sous G0-G7 complets (R-22) ; la **collecte** (`collector`,
`sources`, `run_campaign`, `closure`, `smoke`, `journal`, `model`,
`r2.collect_asn`, `records.append_asn`) reste en quarantaine, **« jetable »** au sens de 10 §1 : elle
meurt après le rapport `11-mesures-pilotes.md`, sauf décision de l'investisseur
après le rendu (ADR-0028 D6 vi). Frontière : ADR-0028 D6 (i).

- **Zéro dépendance** hors bibliothèque standard Python (≥ 3.9) : `urllib` +
  décodage hex à la main. Aucune clé, aucun token, aucun cookie (décision
  « strictement sans clé », 10 §9.3).
- **Pool** : 12 flux / 11 sources répondantes (10 §3.1) ; CryptoCompare
  écartée (401 sans clé), ré-confirmée à chaque campagne.

## Structure

- `shogen_s2/model.py` — le relevé (`Reading`, `Status`), `Decimal` partout
  (recalculable à l'octet, ADR-0003).
- `shogen_s2/sources.py` — les 12 décodeurs (un par flux) + `read()` ; chaque
  piège re-mesuré (10 §3.1) est codé et cité.
- `shogen_s2/journal.py` — le journal recalculable (JSONL : valeur décodée +
  sha256 ; octets bruts séparés pour recalculer aussi le décodage — ADR-0005).
- `shogen_s2/smoke.py` — smoke test LIVE (une lecture des 12 flux, décodée).
- `tests/` — régression sur fixtures gelées + pièges + fail-closed.

## Usage

```
cd s2-harness
python -m shogen_s2.smoke                       # une lecture live des 12 flux
python -m unittest discover -s tests -t . -v    # tests déterministes
python -m shogen_s2.report <dir> --exclude-window-start-range FROM TO   # rapport recalculé
python -m tests.capture                         # re-geler les fixtures
```

`<dir>` porte `control.jsonl` et `journal.jsonl`. `--exclude-window-start-range FROM TO`
(répétable ; `FROM`, `TO` = epoch UTC, plage **fermée** de `window_start`) retire ces fenêtres de n, K et P̂_more
(ADR-0025 déc. 1 ; bornes du rendu principal : ADR-0028 D4 et D5) ; l'exclusion vaut pour tout
enregistrement horodaté : `window_start`, et `ts` / `harness_ts` (`asn_attribution` / `clock_check`) sur la
même plage étendue à la durée de la dernière fenêtre (ADR-0028 D5). `--segment-from T0_EPOCH` avec
`--segment-to T_FIN_EPOCH` (fin exclue) ou `--segment-n-fixe N` (fin = `window_start` de la N-ième fenêtre
distincte ≥ T0, plus w ; ADR-0024) restreint l'analyse au segment semi-ouvert [T0 ; fin), tous types
d'enregistrement (ADR-0028 D4, D2 pt 6) ; les deux formes de fin s'excluent, et `--segment-from` exige l'une
des deux. Sans option, aucune ligne d'exclusion ni de segment n'est ajoutée ; le rendu est épinglé octet pour
octet (`SHA_BASE_SANS_OPTION`, `tests/test_exclusion.py`, test iv).

## État

- **2026-08-05** — décodeurs + journal + smoke + tests **tested** (fixtures
  gelées, pièges §3.1, fail-closed ; smoke 12/12 flux live).
- **S2 Phase A / walking skeleton** — collecteur fenêtré UTC (échantillonnage
  fin-de-fenêtre M-1, `Decimal` prec fixée, journal recalculable ADR-0003),
  R1 K&L (p̂ᵢ, P̂₀/P̂₁/P̂_more, K, z, garde `n·p(1−p) ≥ 10`), table §6 minimale.
- **S2 Phase A / M1b** — **pool complet 11 sources / 12 flux** (les 12 décodeurs
  réutilisés ; devise **marquée par flux**, classe « BTC/USD-stable ») ; **queue
  binomiale exacte** `P(K ≥ K_obs | Bin(n, P̂_more))` sous la garde (§5.4,
  `binomial_tail_ge`) ; **estimateur L&M** (`lm.py` : Ê(Θ), Ê(Θ²) forme par paires,
  Var̂(Θ), corrélations φ **signées** par paire de flux) ; **calendrier 2-strates ex
  ante** (`window.py`) ; rapport 6 blocs (1–4 calculés).
- **S2 Phase A / M1c (cette extension — FERME la Phase A)** — **R2** (`r2.py`) :
  axe **ASN** (§4.1) DNS→RIPEstat→Cymru, **attribution croisée ≥ 2 bases BGP**,
  résolveur **injectable** (DI ; mock en test, DoH+RIPEstat réels non lancés),
  table ASN datée au journal (`record:"asn_attribution"`) ; axe **contenu** (§4.2)
  — les 5 statistiques **par paire, jamais fusionnées** (ρ_raw, ρ_resid médiane
  leave-two-out, T/T_Δ au tick, (K,z) co-aberrance réutilisant la machinerie §5.1,
  δ direction), garde **N_min = 300** (« historique de contenu insuffisant ») ; axe
  **méthode** (§4.3) — 5 arêtes `basis:doc` (ADR-0008 : déclenchent (b), ne
  fusionnent pas) ; **k_eff** (§5.6) partition des **hôtes** (nœud = hôte ;
  okx_ticker+okx_index → un hôte) par recouvrements **measured**, **clusters nommés
  avec amonts** (ADR-0007), fail-closed « non évaluable » si ASN non mesuré ;
  **drapeau 2 tri-état** (levé/éteint/non évaluable) consommant la matrice de
  co-écarts M1b ; corrélations L&M entre **clusters** ; résidu de **peg USDT/USD**
  = R2(2a) ρ_resid ; **rapport §6 COMPLET (6 blocs)**. `HARNESS_VERSION` = S2A-M1c.
  Tests et smoke 12/12 de cet incrément ; le compte courant est la mesure datée ci-dessous.

- **2026-10-01 — mesure** (arbre de la branche `partie-1-moteur` au commit du lot B-DEP-1, sous-lot B-DEP-1c, après le lot POOLEE, le lot B,
  B-SEG-1/B-SEG-2, E1, DOCS-S2-a et SIM-NIVEAU, TMP sous `F:/tmp`, `SHOGEN_S2_CAMPAGNE_CONTROL` non posée ;
  re-mesurée par l'orchestrateur au commit, C-8 de la revue G2 du lot POOLEE, précédent C-7 de la revue G2
  du lot B) : `python -B -m unittest discover -s tests -t .` → « Ran 258 tests … OK (skipped=2) »
  (au commit de DOCS-S2-a : 216, et son G1 avait mesuré « Ran 207 » sur `aa0afdc` + a1, b, a2 ; le lot B
  en ajoute 13 : 219, 222, 224 puis 229 après B-a1, B-a2, B-b et B-c ; le lot POOLEE en ajoute 13 : 237,
  239 puis 242 après POOLEE-a, POOLEE-b et POOLEE-c ; le lot B-DEP-1 en ajoute 16 : 248, 256 puis 258 après
  B-DEP-1a, B-DEP-1b et B-DEP-1c ; DOCS-S2-b n'est pas encore commis).
  Les deux tests sautés sont les deux tests (ii) de `TestExclusionJournalReel`
  (`tests/test_exclusion.py`), qui lisent la copie scellée de la campagne (comptes seulement) : la
  variable n'est posée que par l'orchestrateur seul, sur copie (ADR-0028 annexe D.4 a). `aa0afdc`
  seul : 206 (DOCS-S2-b ajoute le test `test_v_ligne_nmin_suit_le_journal`). Ce compte se re-mesure à
  chaque lot qui change le compte.

À venir : le rendu servi de la sortie S2 (`docs/11-mesures-pilotes.md`), par la
chaîne de lots de l'ADR-0028 (annexe A : segments, pool d'analyse, rendu, paquet de
pré-enregistrement, exécution unique). Ce fichier ne porte aucun résultat de campagne.
