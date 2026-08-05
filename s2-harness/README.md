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

## État (2026-08-05)

Décodeurs + journal + smoke + tests **tested** (11 tests unittest, 0 échec ;
smoke 12/12 flux live, fourchette ~0,11 %). À venir, dans l'ordre de 10 :
collecteur (fenêtres alignées UTC, w = 60 s, ≈ 2 semaines, 2 strates ex ante),
R1 (test K&L §5 : écarts, P̂_more, K, z, garde n·p(1−p) ≥ 10), estimateur L&M
(Var̂(Θ) forme par paires), R2 ASN + contenu, k_eff (appliquant ADR-0008),
rapport `11-mesures-pilotes.md`.
