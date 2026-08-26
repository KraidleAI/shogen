"""Tests du calcul de CLÔTURE DE CALIBRATION (closure.py) — ADR-0021 item 4 (NEUF).

Vérifie la pièce ABSENTE du harnais M1c :
  - `percentile_nearest_rank` : méthode NOMMÉE (rang le plus proche), déterministe,
    valeurs à la main ;
  - `σ_s = max(plancher, 3 × P99 staleness honnête PAR CLASSE)` (ADR-0020 déc. 3) ;
  - clause de révision τ (P99 écart LOO relatif > 0,25 % → révision par ADR,
    fail-closed : τ committé None) ;
  - recalculabilité (déterminisme) + fail-closed (scalaire legacy, strate trafiquée).
Journaux construits via `collector.collect` (fixtures/read_fn injecté) — recalculables.
"""

from __future__ import annotations

import json
import os
import tempfile
import unittest
from decimal import Decimal

from shogen_s2 import closure, collector, sources
from shogen_s2.model import Currency, Reading, Status
from shogen_s2.sources import SPECS
from tests.test_collector import BY_ID
from tests.test_run_campaign import FakeClock

D = Decimal


def _clock(buckets, w=60, delta=2.0):
    clock = [1.0]
    for b in buckets:
        clock += [float(b) + 1.0, float(b) + w - delta]
    return clock


class TestPercentileNearestRank(unittest.TestCase):
    def test_hand_values(self):
        pr = closure.percentile_nearest_rank
        # 1..100 : rang = ceil(99·100/100) = 99 → valeur 99.
        self.assertEqual(pr([D(x) for x in range(1, 101)], 99), D(99))
        # 1..50 : rang = ceil(99·50/100) = ceil(49.5) = 50 → valeur 50 (le max).
        self.assertEqual(pr([D(x) for x in range(1, 51)], 99), D(50))
        # singleton : P99 = l'unique valeur ; liste vide → None (fail-closed).
        self.assertEqual(pr([D("7")], 99), D("7"))
        self.assertIsNone(pr([], 99))
        # médiane p=50 sur 1..10 : rang = ceil(5.0) = 5 → valeur 5.
        self.assertEqual(pr([D(x) for x in range(1, 11)], 50), D(5))

    def test_result_is_observed_value_no_interpolation(self):
        # Le résultat EST une valeur observée (jamais interpolée) → recalcul exact.
        vals = [D("1.5"), D("2.25"), D("100"), D("0.1")]
        self.assertIn(closure.percentile_nearest_rank(vals, 99), vals)

    def test_unsorted_input_sorted_internally(self):
        self.assertEqual(closure.percentile_nearest_rank([D(3), D(1), D(2)], 99), D(3))


class ClosureJournalCase(unittest.TestCase):
    def _collect(self, specs, read_fn, buckets, sigma_by_class=None, w=60, delta=2.0):
        d = tempfile.mkdtemp(prefix="s2clo_")
        control = os.path.join(d, "control.jsonl")
        journal = os.path.join(d, "journal.jsonl")
        raw = os.path.join(d, "raw.jsonl")
        collector.collect(specs, control, journal, raw, n_windows=len(buckets),
                          sigma_by_class=sigma_by_class or sources.default_sigma_by_class(),
                          tau_classe=sources.default_tau_by_class(), w=w, sample_lead=delta,
                          now_fn=FakeClock(_clock(buckets, w, delta)),
                          sleep_fn=lambda s: None, read_fn=read_fn)
        return control, journal


class TestClosureStaleness(ClosureJournalCase):
    def test_sigma_s_is_max_floor_3xp99(self):
        # coinbase (place_horodatee, plancher 30) figé à src = win_end − 130 →
        # staleness = 130 s sur les 3 fenêtres → P99 = 130 → σ_s = max(30, 3·130) = 390.
        buckets = [0, 60, 120]

        def read_fn(spec, ts):
            # win_end = bucket + 60 ; ts ≈ bucket + 58 → src = ts − 128 → staleness ≈ 130
            return Reading(flux_id=spec.flux_id, kind=spec.kind, endpoint=spec.endpoint,
                           fetch_ts=ts, status=Status.OK, http_status=200, raw=b"x",
                           price=Decimal("64000"), currency=Currency.USD, source_ts=ts - 128.0)

        control, journal = self._collect([BY_ID["coinbase"]], read_fn, buckets,
                                         sigma_by_class={"place_horodatee": Decimal("30")})
        res = closure.compute_closure(control, journal,
                                      floors_by_class={"place_horodatee": 30,
                                                       "sans_horodatage": None})
        self.assertEqual(res["p99_staleness_par_classe"]["place_horodatee"], D("130"))
        self.assertEqual(res["sigma_classe"]["place_horodatee"], D("390"))   # max(30, 3·130)
        self.assertIsNone(res["sigma_classe"]["sans_horodatage"])            # plancher None → None
        self.assertEqual(res["staleness_multiplier"], 3)
        self.assertIn("nearest-rank", res["percentile_method"])

    def test_floor_wins_when_3xp99_below_floor(self):
        # staleness fraîche (~δ=2 s) → 3·P99 ≈ 6 < plancher 30 → σ_s = plancher 30.
        buckets = [0, 60, 120]

        def read_fn(spec, ts):
            return Reading(flux_id=spec.flux_id, kind=spec.kind, endpoint=spec.endpoint,
                           fetch_ts=ts, status=Status.OK, http_status=200, raw=b"x",
                           price=Decimal("64000"), currency=Currency.USD, source_ts=ts)

        control, journal = self._collect([BY_ID["coinbase"]], read_fn, buckets,
                                         sigma_by_class={"place_horodatee": Decimal("30")})
        res = closure.compute_closure(control, journal,
                                      floors_by_class={"place_horodatee": 30,
                                                       "sans_horodatage": None})
        self.assertEqual(res["sigma_classe"]["place_horodatee"], D("30"))    # plancher gagne

    def test_no_staleness_data_falls_back_to_floor(self):
        # Aucune staleness observée pour agregateur (aucun flux agrégateur au pool) →
        # P99 None → repli sur le plancher ADR-0020 (jamais deviné).
        buckets = [0, 60, 120]

        def read_fn(spec, ts):
            return Reading(flux_id=spec.flux_id, kind=spec.kind, endpoint=spec.endpoint,
                           fetch_ts=ts, status=Status.OK, http_status=200, raw=b"x",
                           price=Decimal("64000"), currency=Currency.USD, source_ts=ts)

        control, journal = self._collect([BY_ID["coinbase"]], read_fn, buckets,
                                         sigma_by_class={"place_horodatee": Decimal("30")})
        res = closure.compute_closure(control, journal)   # planchers ADR-0020 par défaut
        self.assertIsNone(res["p99_staleness_par_classe"]["agregateur"])
        self.assertEqual(res["sigma_classe"]["agregateur"], D("300"))        # plancher ADR-0020


class TestClosureTauRevision(ClosureJournalCase):
    def _pool_with_outlier(self, outlier_flux, factor):
        buckets = [0, 60, 120]

        def read_fn(spec, ts):
            price = Decimal("64000")
            if spec.flux_id == outlier_flux:
                price = price * factor
            # source_ts=None pour les sans_horodatage (fidélité) ; ts sinon.
            src = None if sources.SIGMA_CLASS_OF_FLUX[spec.flux_id] == "sans_horodatage" else ts
            return Reading(flux_id=spec.flux_id, kind=spec.kind, endpoint=spec.endpoint,
                           fetch_ts=ts, status=Status.OK, http_status=200, raw=b"x",
                           price=price, currency=spec.currency, source_ts=src)

        return self._collect(list(SPECS), read_fn, buckets)

    def test_revision_needed_when_p99_rel_above_threshold(self):
        # Un flux à +0,6 % → écart LOO relatif 0,006 > 0,25 % → révision τ EN ATTENTE :
        # τ committé = None (fail-closed : révision = décision ADR, jamais devinée).
        control, journal = self._pool_with_outlier("coinbase", Decimal("1.006"))
        res = closure.compute_closure(control, journal)
        self.assertGreater(res["p99_ecart_relatif"], Decimal("0.0025"))
        self.assertTrue(res["tau_revision_needed"])
        self.assertIsNone(res["tau_classe"])
        self.assertEqual(res["tau_base"], Decimal("0.005"))

    def test_no_revision_when_clean(self):
        # Tous à 64000 → écart LOO relatif 0 < seuil → τ committé = τ_base 0,5 %.
        control, journal = self._pool_with_outlier("coinbase", Decimal("1"))
        res = closure.compute_closure(control, journal)
        self.assertEqual(res["p99_ecart_relatif"], Decimal("0"))
        self.assertFalse(res["tau_revision_needed"])
        self.assertEqual(res["tau_classe"], Decimal("0.005"))


class TestClosureRecalculable(ClosureJournalCase):
    def _clean(self):
        def read_fn(spec, ts):
            return Reading(flux_id=spec.flux_id, kind=spec.kind, endpoint=spec.endpoint,
                           fetch_ts=ts, status=Status.OK, http_status=200, raw=b"x",
                           price=Decimal("64000"), currency=Currency.USD, source_ts=ts - 100.0)
        return self._collect([BY_ID["coinbase"]], read_fn, [0, 60, 120],
                             sigma_by_class={"place_horodatee": Decimal("30")})

    def test_deterministic(self):
        control, journal = self._clean()
        a = closure.compute_closure(control, journal)
        b = closure.compute_closure(control, journal)
        self.assertEqual(a["sigma_classe"], b["sigma_classe"])
        self.assertEqual(a["p99_staleness_par_classe"], b["p99_staleness_par_classe"])

    def test_legacy_scalar_sigma_classe_fails_closed(self):
        # Un journal legacy (sigma_classe scalaire) → clôture refusée (via
        # effective_run_params), jamais réinterprété.
        control, journal = self._clean()
        with open(control, encoding="utf-8") as fh:
            lines = fh.read().splitlines()
        for i, ln in enumerate(lines):
            obj = json.loads(ln)
            if obj.get("record") == "run_params":
                obj["sigma_classe"] = "30"          # SCALAIRE legacy
                lines[i] = json.dumps(obj, ensure_ascii=False)
                break
        with open(control, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        with self.assertRaisesRegex(ValueError, "SCALAIRE legacy"):
            closure.compute_closure(control, journal)

    def test_legacy_scalar_tau_classe_fails_closed(self):
        # Miroir τ (ADR-0022, C5/MAST) : un journal legacy portant `tau_classe` SCALAIRE
        # → clôture refusée (via effective_run_params), jamais réinterprété en τ unique.
        control, journal = self._clean()
        with open(control, encoding="utf-8") as fh:
            lines = fh.read().splitlines()
        for i, ln in enumerate(lines):
            obj = json.loads(ln)
            if obj.get("record") == "run_params":
                obj["tau_classe"] = "0.005"         # SCALAIRE legacy (str), plus un mapping
                lines[i] = json.dumps(obj, ensure_ascii=False)
                break
        with open(control, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        with self.assertRaisesRegex(ValueError, "SCALAIRE legacy"):
            closure.compute_closure(control, journal)

    def test_roundtrip_closure_to_campagne_resolve(self):
        # Round-trip RÉEL (ADR-0022) — le sigma-tau.json committé est ASSEMBLÉ : σ vient
        # de la clôture, τ PAR CLASSE vient de l'ADR-0022 (le τ SCALAIRE de la clôture est
        # désormais REJETÉ par le loader, fail-closed). Prouve que l'assemblage réel
        # (calibration → clôture σ + τ ADR → --sigma-tau-file → resolve) est consommable.
        from shogen_s2 import run_campaign
        control, journal = self._clean()
        res = closure.compute_closure(control, journal)
        self.assertFalse(res["tau_revision_needed"])
        tau_adr = {"oracle_pyth": "0.0015", "place_horodatee": "0.0045",
                   "sans_horodatage": "0.0045", "oracle_chainlink": "0.0165",
                   "agregateur": "0.026"}                      # valeurs ADR-0022 (par classe)
        assembled = {"sigma_classe": closure._jsonable(res)["sigma_classe"],
                     "tau_classe": tau_adr}
        d = tempfile.mkdtemp(prefix="s2rt_")
        path = os.path.join(d, "sigma_tau.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(assembled, f, ensure_ascii=False)
        sigma_by_class, tau, regime = run_campaign.resolve_sigma_tau("campagne", path)
        # σ chargés == σ calculés par la clôture ; τ == τ PAR CLASSE de l'ADR.
        self.assertEqual(sigma_by_class["place_horodatee"],
                         res["sigma_classe"]["place_horodatee"])
        self.assertIsNone(sigma_by_class["sans_horodatage"])
        self.assertEqual(tau["agregateur"], Decimal("0.026"))
        self.assertEqual(tau["oracle_chainlink"], Decimal("0.0165"))
        self.assertIn("CAMPAGNE", regime)

    def test_cli_emits_json(self):
        import io
        control, journal = self._clean()
        d = os.path.dirname(control)
        buf = io.BytesIO()
        # main écrit sur sys.stdout.buffer (UTF-8) ; on capture le flux binaire.
        real = closure.sys.stdout
        try:
            closure.sys.stdout = type("X", (), {"buffer": buf})()
            rc = closure.main([d])
        finally:
            closure.sys.stdout = real
        self.assertEqual(rc, 0)
        payload = json.loads(buf.getvalue().decode("utf-8"))
        self.assertIn("sigma_classe", payload)
        self.assertIn("percentile_method", payload)


if __name__ == "__main__":
    unittest.main()
