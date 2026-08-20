# s2-harness — l'instrument de mesure pilote S2 (jetable)

Conception : [`docs/10-mesures-pilotes-design.md`](../docs/10-mesures-pilotes-design.md).

Cet instrument tranche la question de S2 (`05-roadmap.md` §S2) : les axes R2
sont-ils observables en pratique, et le test R1 discrimine-t-il quelque chose
sur données réelles ? **Il est jetable** (10 §1) : il meurt après le rapport
`11-mesures-pilotes.md`, il n'est pas un ancêtre du produit.

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
python -m tests.capture                         # re-geler les fixtures
```

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
  Tests : `python -m unittest discover -s tests -t .` (**136 verts**) + smoke 12/12.

À venir : le **run réel 24–48 h** (orchestrateur — pas ce worker ; `collect_asn`
et `collector.collect` lancés au réseau) produisant la table §6 complète, recalculée
à l'identique par l'oracle ; puis `11-mesures-pilotes.md` (Phase C).
