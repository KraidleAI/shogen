"""Tests bout-en-bout du collecteur (collector.py) — fixtures gelées, sans réseau.

Le collecteur est piloté par injection de dépendances (now_fn, sleep_fn,
read_fn) : les lectures viennent des fixtures `.bin` gelées décodées par les
vrais décodeurs (sources.py), l'horloge est scriptée. On exerce la chaîne
complète collecteur → journal → R1 (recompute_from_journal), dont l'exigence (a)
harnais-down ≠ source-en-panne, l'échantillonnage en FIN de fenêtre (M-1),
l'idempotence (append-only + dédup + last-wins), la concordance des run_params
(§E) et la tolérance à une ligne tronquée (§F).

NOTES fixtures (§H, traçabilité) : les `.bin` gelées et `expected.json` sont une
**re-capture live** du 2026-08-05 ~16:11 UTC (source_ts ≈ 1785946281 ⇒ started_utc
2026-08-05T16:11:xx), PAS les payloads de la table doc 10 §3.1 (~12:03 UTC). Les
valeurs STRUCTURELLES des décodeurs (positions, clés) sont épinglées séparément
dans `test_sources.TestQuirks` sur des octets synthétiques, indépendants de l'heure.
"""

from __future__ import annotations

import contextlib
import io
import os
import tempfile
import unittest
from decimal import Decimal

from shogen_s2 import collector, r1, records
from shogen_s2.model import Currency, Reading, Status
from shogen_s2.sources import SPECS

HERE = os.path.dirname(__file__)
FIX = os.path.join(HERE, "fixtures")
BY_ID = {s.flux_id: s for s in SPECS}

SKELETON = ["coinbase", "kraken", "bitstamp"]      # 3 places primaires USD
W = 60
DELTA = 5.0                                        # sample_lead par défaut du collecteur
BUCKETS = [1785946260, 1785946320, 1785946380]     # 3 fenêtres UTC-alignées
TREADS = [b + W - DELTA for b in BUCKETS]          # instants de lecture (fin de fenêtre)
NOWS = [1785946291.0, 1785946321.0, 1785946381.0]  # « now » en tête de boucle (dans chaque bucket)
START = 1785946290.0
# now_fn est appelé 1 (start) + 2/fenêtre (now en tête, t_read après sommeil).
CLOCK = [START, NOWS[0], TREADS[0], NOWS[1], TREADS[1], NOWS[2], TREADS[2]]
SIGMA = Decimal("1e12")                            # jamais de staleness (tests « propres »)
TAU = Decimal("50")


class FakeClock:
    def __init__(self, times):
        self.times = list(times)
        self.i = 0

    def __call__(self):
        v = self.times[self.i]
        self.i += 1
        return v


def frozen_reading(flux_id, fetch_ts):
    spec = BY_ID[flux_id]
    with open(os.path.join(FIX, flux_id + ".bin"), "rb") as f:
        raw = f.read()
    price, source_ts, extra = spec.decode(raw)
    return Reading(flux_id=spec.flux_id, kind=spec.kind, endpoint=spec.endpoint,
                   fetch_ts=fetch_ts, status=Status.OK, http_status=200, raw=raw,
                   price=price, currency=spec.currency, source_ts=source_ts, extra=extra)


def frozen_read_fn(spec, ts):
    return frozen_reading(spec.flux_id, ts)


def _count_lines(path):
    with open(path, encoding="utf-8") as f:
        return sum(1 for line in f if line.strip())


class CollectorCase(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp(prefix="s2col_")
        self.control = os.path.join(self.d, "control.jsonl")
        self.journal = os.path.join(self.d, "journal.jsonl")
        self.raw = os.path.join(self.d, "raw.jsonl")
        self.specs = [BY_ID[f] for f in SKELETON]

    def _collect(self, read_fn=frozen_read_fn, clock=None, sigma=SIGMA):
        return collector.collect(
            self.specs, self.control, self.journal, self.raw, n_windows=3,
            sigma_classe=sigma, tau_classe=TAU,
            now_fn=FakeClock(clock or CLOCK), sleep_fn=lambda s: None, read_fn=read_fn,
        )


class TestCollectClean(CollectorCase):
    def test_end_to_end_clean_run(self):
        completed = self._collect()
        self.assertEqual(completed, 3)

        params_list, clocks, markers = records.parse_control(self.control)
        self.assertEqual(len(params_list), 1)
        self.assertEqual(params_list[-1]["pool"], SKELETON)
        self.assertEqual(len(clocks), 1)
        self.assertEqual(sorted(m["window_start"] for m in markers), BUCKETS)
        self.assertEqual(_count_lines(self.journal), 9)   # 3 fenêtres × 3 sources
        self.assertEqual(_count_lines(self.raw), 9)

        cc = clocks[0]
        self.assertIn("coinbase", cc["offsets"])
        self.assertIn("bitstamp", cc["offsets"])
        self.assertNotIn("kraken", cc["offsets"])         # kraken ne porte pas d'horodatage
        self.assertIsNotNone(cc["median_offset"])

    def test_recompute_from_journal_clean(self):
        self._collect()
        out = r1.recompute_from_journal(self.control, self.journal)
        blk = out["strates"]["calme"]
        self.assertEqual(blk["n"], 3)
        for f in SKELETON:
            s = blk["per_source"][f]
            self.assertEqual(s["phat"], Decimal(0))
            self.assertEqual(s["ecart"], 0)
            self.assertEqual(s["non_eval_hors_env"], 3)   # N=3<4 partout (publié)
        self.assertEqual(blk["per_source"]["coinbase"]["axes_evaluables"], ["panne", "staleness"])
        self.assertEqual(blk["per_source"]["kraken"]["axes_evaluables"], ["panne"])
        # Résidu fail-open visible (§G) : kraken répond sans horodatage porté.
        self.assertEqual(blk["residu_staleness_fail_open"], ["kraken"])
        self.assertTrue(blk["per_source"]["kraken"]["staleness_fail_open"])
        self.assertTrue(blk["flag_historique_insuffisant"])
        self.assertIsNone(blk["z"])


class TestEndOfWindowSampling(CollectorCase):
    def test_no_false_staleness_realistic_sigma(self):
        # LE test qui aurait attrapé M-1 : σ RÉALISTE (30 s), échantillonnage en
        # fin de fenêtre. Sources fraîches (source_ts = instant de lecture) →
        # staleness ≈ δ ≪ σ → 0 ; source figée (source_ts ancien) → stale.
        w_r, delta_r = 60, 2.0
        buckets_r = [0, 60, 120]
        treads_r = [b + w_r - delta_r for b in buckets_r]      # 58, 118, 178
        nows_r = [5.0, 65.0, 125.0]
        clock_r = [1.0, nows_r[0], treads_r[0], nows_r[1], treads_r[1], nows_r[2], treads_r[2]]

        def read_fn(spec, ts):
            src = 1.0 if spec.flux_id == "kraken" else ts      # kraken figé, autres frais
            return Reading(flux_id=spec.flux_id, kind=spec.kind, endpoint=spec.endpoint,
                           fetch_ts=ts, status=Status.OK, http_status=200, raw=b"payload",
                           price=Decimal("64000"), currency=Currency.USD, source_ts=src)

        sleeps: list[float] = []
        collector.collect(self.specs, self.control, self.journal, self.raw, n_windows=3,
                          sigma_classe=Decimal("30"), tau_classe=TAU, w=w_r, sample_lead=delta_r,
                          now_fn=FakeClock(clock_r), sleep_fn=sleeps.append, read_fn=read_fn)
        # Épingle le MÉCANISME (pas seulement le comportement) : dors d'abord,
        # lis à ws+w−δ. sleep = (ws+w−δ) − now = 58−5 / 118−65 / 178−125 = 53 s.
        # Une régression `ts_sample = ws+δ` ne dormirait pas → sleeps ≠ [53,53,53].
        self.assertEqual(sleeps, [53.0, 53.0, 53.0])
        blk = r1.recompute_from_journal(self.control, self.journal)["strates"]["calme"]
        self.assertEqual(blk["n"], 3)
        self.assertEqual(blk["per_source"]["coinbase"]["staleness"], 0)   # fraîche → 0 (M-1)
        self.assertEqual(blk["per_source"]["bitstamp"]["staleness"], 0)
        self.assertEqual(blk["per_source"]["kraken"]["staleness"], 3)     # figée → stale
        self.assertEqual(blk["per_source"]["kraken"]["phat"], Decimal(1))
        self.assertEqual(blk["per_source"]["coinbase"]["phat"], Decimal(0))

    def test_read_instant_is_in_window_half_open(self):
        # Le t_read (fin de fenêtre) tombe bien DANS la fenêtre, jamais dans la
        # suivante (piège demi-ouvert) : les marqueurs portent les bons buckets.
        self._collect()
        _p, _c, markers = records.parse_control(self.control)
        self.assertEqual(sorted(m["window_start"] for m in markers), BUCKETS)


class TestCollectWithPannes(CollectorCase):
    def test_injected_pannes_flow_to_r1(self):
        # kraken et bitstamp en panne dans la 2ᵉ fenêtre (instant de lecture TREADS[1]).
        def read_fn(spec, ts):
            if spec.flux_id in ("kraken", "bitstamp") and ts == TREADS[1]:
                return Reading(flux_id=spec.flux_id, kind=spec.kind, endpoint=spec.endpoint,
                               fetch_ts=ts, status=Status.PANNE_TRANSPORT, currency=Currency.USD)
            return frozen_reading(spec.flux_id, ts)

        self._collect(read_fn=read_fn)
        blk = r1.recompute_from_journal(self.control, self.journal)["strates"]["calme"]
        self.assertEqual(blk["n"], 3)
        self.assertEqual(blk["K"], 1)                     # 1 fenêtre à ≥ 2 écarts
        third = Decimal(1) / Decimal(3)
        self.assertLess(abs(blk["per_source"]["kraken"]["phat"] - third), Decimal("1e-20"))
        self.assertLess(abs(blk["per_source"]["bitstamp"]["phat"] - third), Decimal("1e-20"))
        self.assertEqual(blk["per_source"]["coinbase"]["phat"], Decimal(0))
        self.assertLess(abs(blk["P_more"] - Decimal(1) / Decimal(9)), Decimal("1e-20"))
        self.assertTrue(blk["flag_historique_insuffisant"])


class TestAppendOnlyIdempotent(CollectorCase):
    def test_second_run_appends_and_is_idempotent(self):
        # Un redémarrage qui re-collecte les mêmes fenêtres : append-only + dédup
        # des marqueurs + last-wins → n inchangé (reprise tolérée).
        self._collect()
        self.assertEqual(_count_lines(self.journal), 9)
        self._collect()                                   # 2ᵉ passe, mêmes fenêtres, mêmes params
        self.assertEqual(_count_lines(self.journal), 18)  # APPEND (pas de troncature)
        params_list, clocks, markers = records.parse_control(self.control)
        self.assertEqual(len(params_list), 2)             # un run_params par démarrage
        self.assertEqual(len(clocks), 2)
        self.assertEqual(len(markers), 6)                 # 2×3 marqueurs bruts
        out = r1.recompute_from_journal(self.control, self.journal)
        self.assertEqual(out["strates"]["calme"]["n"], 3)  # dédupliqués à 3 fenêtres


class TestRunParamsConcordance(CollectorCase):
    def test_divergent_run_params_fail_closed(self):
        # 2 démarrages avec σ différents → recalcul refusé (fail-closed, §E).
        self._collect(sigma=SIGMA)
        collector.collect(self.specs, self.control, self.journal, self.raw, n_windows=3,
                          sigma_classe=Decimal("999"), tau_classe=TAU,
                          now_fn=FakeClock(CLOCK), sleep_fn=lambda s: None, read_fn=frozen_read_fn)
        with self.assertRaises(ValueError):
            r1.recompute_from_journal(self.control, self.journal)


class TestTruncatedLine(CollectorCase):
    def test_truncated_last_line_tolerated_and_logged(self):
        self._collect()
        with open(self.journal, "a", encoding="utf-8") as f:
            f.write('{"window_start": 999, "flux_id": "coinba')   # ligne torse (crash mi-écriture)
        buf = io.StringIO()
        with contextlib.redirect_stderr(buf):
            out = r1.recompute_from_journal(self.control, self.journal)
        self.assertEqual(out["strates"]["calme"]["n"], 3)         # torse ignorée
        self.assertIn("tronquée", buf.getvalue())                 # consigné, non silencieux

    def test_corrupt_non_final_line_raises(self):
        self._collect()
        with open(self.journal, encoding="utf-8") as fh:
            lines = fh.read().splitlines()
        lines[0] = '{"torse'                                      # 1re ligne cassée (non finale)
        with open(self.journal, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        with self.assertRaises(ValueError):
            r1.recompute_from_journal(self.control, self.journal)


if __name__ == "__main__":
    unittest.main()
