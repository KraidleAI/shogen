"""Gèle une réponse live de chaque flux en fixture déterministe.

Rejouer ce script re-capture les fixtures (les prix bougent — c'est voulu :
la fixture est un instantané figé, et test_sources.py décode ces octets figés
et compare à `expected.json`, capturé au même instant). Décodeur = pur, donc
le test est déterministe même si le monde change.
"""

from __future__ import annotations

import json
import os
import time

from shogen_s2.sources import EXCLUDED_CRYPTOCOMPARE, SPECS, _http_get, read

HERE = os.path.dirname(__file__)
FIX = os.path.join(HERE, "fixtures")


def main() -> int:
    os.makedirs(FIX, exist_ok=True)
    expected: dict = {}
    now = time.time()
    for spec in SPECS:
        r = read(spec, now)
        if not r.ok:
            print("SKIP (pas OK):", spec.flux_id, r.status.value, r.extra)
            continue
        with open(os.path.join(FIX, spec.flux_id + ".bin"), "wb") as f:
            f.write(r.raw)
        expected[spec.flux_id] = {
            "price": str(r.price),
            "currency": r.currency.value,
            "source_ts": r.source_ts,
            "extra": r.extra,
        }
    st, raw = _http_get(EXCLUDED_CRYPTOCOMPARE, 10.0)
    with open(os.path.join(FIX, "cryptocompare_401.bin"), "wb") as f:
        f.write(raw)
    expected["_cryptocompare_http"] = st
    with open(os.path.join(HERE, "expected.json"), "w", encoding="utf-8") as f:
        json.dump(expected, f, ensure_ascii=False, indent=2)
    n = len([k for k in expected if not k.startswith("_")])
    print(f"capturé {n} fixtures ; cryptocompare HTTP {st}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
