"""Tests de l'alignement de fenêtre sur l'époque UTC (window.py).

La convention demi-ouverte `[début, fin)` est épinglée ici : collecteur et
oracle de recalcul ne doivent jamais diverger sur les bords (10 §5.3).
"""

from __future__ import annotations

import unittest

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


if __name__ == "__main__":
    unittest.main()
