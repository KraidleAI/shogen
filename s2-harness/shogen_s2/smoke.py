"""Smoke test LIVE — une lecture de chacun des 12 flux, décodée, tabulée.

But (10 forme d'exécution) : prouver la chaîne de bout en bout et rattraper
les bugs de décodage AVANT la collecte de 2 semaines, et RE-CONFIRMER que les
sources sont vivantes et sans clé à l'instant du lancement (les statuts de
10 §3.1 datent du 2026-08-05 ~12:02 UTC ; ce test les re-mesure).

Sortie : un tableau + la cohérence croisée (fourchette du pool) + le 401
re-confirmé de CryptoCompare (exclusion vérifiée, pas postulée). Code de
sortie 0 si les 12 flux décodent, non-zéro sinon — fail-closed.
"""

from __future__ import annotations

import sys
import time

from . import journal
from .model import Status
from .sources import EXCLUDED_CRYPTOCOMPARE, SPECS, TransportError, _http_get, read


def main() -> int:
    now = time.time()
    hdr = (f"{'flux':12} {'kind':10} {'http':>4} {'status':16} "
           f"{'price':>14} {'cur':4} {'src_ts':>12} {'sha8'}")
    print(hdr)
    print("-" * len(hdr))

    ok = 0
    priced: list[tuple[str, object, str]] = []
    for spec in SPECS:
        r = read(spec, now)
        sha = journal.sha256_hex(r.raw)[:8] if r.raw else "--"
        price = f"{r.price:.4f}" if r.price is not None else "-"
        cur = r.currency.value if r.currency else "-"
        srcts = f"{r.source_ts:.0f}" if r.source_ts else "-"
        http = str(r.http_status) if r.http_status is not None else "-"
        note = ""
        if r.status is not Status.OK:
            note = "  <-- " + str(r.extra.get("decode_error", r.status.value))
        print(f"{spec.flux_id:12} {spec.kind:10} {http:>4} {r.status.value:16} "
              f"{price:>14} {cur:4} {srcts:>12} {sha}{note}")
        if r.ok:
            ok += 1
            priced.append((spec.flux_id, r.price, r.currency.value))

    # Ré-confirmer l'exclusion CryptoCompare (attendu : 401 sans clé).
    try:
        cc_status, _ = _http_get(EXCLUDED_CRYPTOCOMPARE, 10.0)
    except TransportError as e:
        cc_status = f"transport error ({e})"
    print(f"\nCryptoCompare (écartée du pool) -> HTTP {cc_status} "
          f"[attendu 401 : {'OK' if cc_status == 401 else 'ÉCART'}]")

    # Cohérence croisée du pool (10 §3.1 : ~0,16 % attendu).
    if priced:
        vals = [p for _, p, _ in priced]
        lo, hi = min(vals), max(vals)
        spread = (hi - lo) / lo * 100
        n_usdt = sum(1 for _, _, c in priced if c == "USDT")
        print(f"Pool : {ok}/{len(SPECS)} flux OK ; fourchette "
              f"{lo:.2f}-{hi:.2f} ({spread:.3f} %) ; "
              f"{len(priced) - n_usdt} USD / {n_usdt} USDT")

    verdict = ok == len(SPECS)
    print(f"\nVerdict smoke : {'OK' if verdict else 'ÉCHEC'} "
          f"({ok}/{len(SPECS)} décodés)")
    return 0 if verdict else 1


if __name__ == "__main__":
    sys.exit(main())
