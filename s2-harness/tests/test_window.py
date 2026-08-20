"""Tests de l'alignement de fenêtre sur l'époque UTC (window.py).

La convention demi-ouverte `[début, fin)` est épinglée ici : collecteur et
oracle de recalcul ne doivent jamais diverger sur les bords (10 §5.3).
"""

from __future__ import annotations

import unittest
from datetime import datetime, timezone

from shogen_s2 import window


class TestWindowAlignment(unittest.TestCase):
    def test_half_open_boundary(self):
        # w = 60 : le bord droit appartient à la fenêtre SUIVANTE (demi-ouvert).
        self.assertEqual(window.window_start(1800.0, 60), 1800)
        self.assertEqual(window.window_start(1799.999, 60), 1740)
        self.assertEqual(window.window_start(1740.0, 60), 1740)
        self.assertEqual(window.window_start(1859.999, 60), 1800)
        self.assertEqual(window.window_start(1860.0, 60), 1860)

    def test_epoch_scale_exact_no_float_drift(self):
        # Un multiple exact de 60 à l'échelle epoch 2026 : pas de dérive flottante.
        self.assertEqual(window.window_start(1785931440.0, 60), 1785931440)
        self.assertEqual(window.window_start(1785931439.999, 60), 1785931380)
        self.assertEqual(window.window_start(1785931500.0, 60), 1785931500)

    def test_returns_int(self):
        self.assertIsInstance(window.window_start(1785931440.5, 60), int)

    def test_window_end(self):
        self.assertEqual(window.window_end(1785931440, 60), 1785931500)

    def test_negative_epoch_rejected(self):
        with self.assertRaises(ValueError):
            window.window_start(-1.0, 60)

    def test_default_strate_single(self):
        self.assertEqual(window.default_strate(1785931440), "calme")
        self.assertEqual(window.default_strate(0), "calme")


class TestWeekdayArithmetic(unittest.TestCase):
    """`weekday_utc` en arithmétique entière == `datetime.weekday()` (l'autorité).
    Aucune constante de jour crue sur parole (10 §5.3 ; conseil ADVISOR)."""

    def test_epoch_is_thursday(self):
        # 1970-01-01 = jeudi = 3 (convention lundi=0).
        self.assertEqual(window.weekday_utc(0), 3)

    def test_matches_datetime_weekday_over_two_weeks(self):
        # Croise chaque jour sur ~2 semaines à l'échelle epoch 2026, à des heures
        # variées (l'arithmétique entière doit tenir quelle que soit l'heure).
        base = 1785931440  # 2026-08-05 ~12:04 UTC (ancre doc 10 §3.1)
        for day in range(-3, 16):
            for hour in (0, 6, 13, 23):
                ws = base + day * 86400 + hour * 3600
                ws -= ws % 60                      # aligné fenêtre (sans importance ici)
                want = datetime.fromtimestamp(ws, timezone.utc).weekday()
                self.assertEqual(window.weekday_utc(ws), want, f"ws={ws}")

    def test_sk_hynix_motivating_date_is_a_tuesday(self):
        # 2026-07-28 (cas motivant §5.3) — on vérifie via datetime, pas une
        # constante crue : weekday_utc doit concorder avec l'autorité.
        ws = int(datetime(2026, 7, 28, 8, 0, tzinfo=timezone.utc).timestamp())
        self.assertEqual(window.weekday_utc(ws),
                         datetime.fromtimestamp(ws, timezone.utc).weekday())


class TestStrateCalendar(unittest.TestCase):
    """Calendrier 2-strates ex ante (§5.3) — fonction PURE de ws + spec committée."""

    def _ws_on_weekday(self, target_wd: int) -> int:
        # Un window_start UTC tombant sur le jour de semaine cible (via datetime).
        base = 1785931440
        for day in range(0, 7):
            ws = base + day * 86400
            ws -= ws % 60
            if datetime.fromtimestamp(ws, timezone.utc).weekday() == target_wd:
                return ws
        raise AssertionError("jour introuvable")

    def test_single_spec_always_calme(self):
        for wd in range(7):
            ws = self._ws_on_weekday(wd)
            self.assertEqual(window.strate_from_spec(ws, window.SINGLE_STRATE_SPEC), "calme")

    def test_weekend_spec_stress_on_sat_sun_calme_otherwise(self):
        spec = window.WEEKEND_STRATE_SPEC
        for wd in range(7):
            ws = self._ws_on_weekday(wd)
            expect = "stress" if wd in (5, 6) else "calme"
            self.assertEqual(window.strate_from_spec(ws, spec), expect, f"wd={wd}")

    def test_make_strate_fn_closes_over_spec(self):
        fn = window.make_strate_fn(window.WEEKEND_STRATE_SPEC)
        sat = self._ws_on_weekday(5)
        mon = self._ws_on_weekday(0)
        self.assertEqual(fn(sat), "stress")
        self.assertEqual(fn(mon), "calme")

    def test_unknown_spec_kind_raises(self):
        with self.assertRaises(ValueError):
            window.strate_from_spec(0, {"kind": "astrology"})

    def test_verify_markers_against_spec_detects_tamper(self):
        spec = window.WEEKEND_STRATE_SPEC
        sat = self._ws_on_weekday(5)
        mon = self._ws_on_weekday(0)
        good = [{"window_start": sat, "strate": "stress"},
                {"window_start": mon, "strate": "calme"}]
        self.assertEqual(window.verify_markers_against_spec(good, spec), [])
        # Étiquette trafiquée : samedi marqué « calme » → divergence détectée.
        bad = [{"window_start": sat, "strate": "calme"}]
        div = window.verify_markers_against_spec(bad, spec)
        self.assertEqual(len(div), 1)
        self.assertEqual(div[0], (sat, "calme", "stress"))


if __name__ == "__main__":
    unittest.main()
