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
- **S2 Phase A / M1b (cette extension)** — **pool complet 11 sources / 12 flux**
  (les 12 décodeurs réutilisés ; devise **marquée par flux**, classe
  « BTC/USD-stable ») ; **queue binomiale exacte** `P(K ≥ K_obs | Bin(n, P̂_more))`
  sous la garde (§5.4, `binomial_tail_ge`) ; **estimateur L&M** (`lm.py` : Ê(Θ),
  Ê(Θ²) forme par paires, Var̂(Θ), corrélations φ **signées** par paire de flux) ;
  **calendrier 2-strates ex ante** (`window.py`, spec committée + comptage par
  strate + fail-closed strate==calendrier) ; **rapport 6 blocs** (1–4 calculés).
  Tests : `python -m unittest discover -s tests -t .` (93 verts) + smoke 12/12.

À venir — **M1c** : R2 (ASN + contenu + méthode, ADR-0008), **k_eff** et le
**drapeau 2** (§5.6), corrélations L&M entre **clusters**, agrégation flux→source
(OKX), le résidu de peg USDT/USD = R2(2a) ; **blocs 5–6 du rapport** ; puis le
run 24–48 h (orchestrateur) et `11-mesures-pilotes.md` (Phase C).
