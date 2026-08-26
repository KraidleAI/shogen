"""R-21 : corrobore le fait externe Chainlink (seuil 0,5 % / heartbeat ~3600 s) sur
les DONNEES PROPRES de Shogen (journal de calibration). Pour chaque round chainlink
distinct (updatedAt = source_ts), gap temporel + delta de prix vs round precedent.
Signature attendue : gap long (~heartbeat) -> delta < 0,5 % ; gap court -> delta >= 0,5 %."""
import os, sys, statistics
from decimal import Decimal
sys.path.insert(0, r"F:\Shogen\s2-harness")
from shogen_s2.r1 import parse_journal

J = r"F:\shogen-campagne\calibration\journal.jsonl"
readings = parse_journal(J)

rounds = {}   # updatedAt(int) -> price(Decimal) ; dedup par round on-chain
for r in readings:
    if (r["flux_id"] == "chainlink" and r.get("status") == "ok"
            and r.get("price") is not None and r.get("source_ts") is not None):
        ts = int(Decimal(str(r["source_ts"])))
        rounds[ts] = Decimal(str(r["price"]))
seq = sorted(rounds.items())
print(f"rounds chainlink distincts (par updatedAt) dans la calibration 48h : {len(seq)}")

HB = 3000  # frontiere gap 'long/heartbeat' vs 'court/deviation' (heartbeat documente ~3600s)
TAU = Decimal("0.005")
cells = {"long_lt": 0, "long_ge": 0, "short_ge": 0, "short_lt": 0}
gaps, deltas = [], []
maxdelta = Decimal(0)
for (t0, p0), (t1, p1) in zip(seq, seq[1:]):
    gap = t1 - t0
    d = abs(p1 - p0) / p0
    gaps.append(gap); deltas.append(float(d) * 100); maxdelta = max(maxdelta, d)
    if gap >= HB:
        cells["long_ge" if d >= TAU else "long_lt"] += 1
    else:
        cells["short_ge" if d >= TAU else "short_lt"] += 1

print(f"gaps (s) : min={min(gaps)} median={int(statistics.median(gaps))} max={max(gaps)}  (heartbeat documente ~3600)")
print(f"deltas (%) : median={statistics.median(deltas):.4f}  max={float(maxdelta)*100:.4f}")
print("")
print(f"SIGNATURE 0,5 %/heartbeat (frontiere gap {HB}s) :")
print(f"  gap LONG (>={HB}s, heartbeat) : delta<0,5% = {cells['long_lt']:3d}   delta>=0,5% = {cells['long_ge']:3d}")
print(f"  gap COURT (<{HB}s, deviation) : delta>=0,5% = {cells['short_ge']:3d}   delta<0,5% = {cells['short_lt']:3d}")
tot = sum(cells.values())
coherent = cells["long_lt"] + cells["short_ge"]
print(f"  coherents avec la signature (long&lt OU court&ge) : {coherent}/{tot} = {coherent/tot*100:.1f}%")
