"""Tests de la table §6 minimale (report.py) — recalculable, déterministe.

La table se régénère depuis les fichiers de journal SEULS (ADR-0003) ; on
vérifie le déterminisme (même journal → même texte), la présence des trois
blocs, du drapeau « historique insuffisant » (attendu sur skeleton court), de
la ligne A(window-stationarity) obligatoire (§5.3) et de la publication du
compte « hors-env non évaluable ».
"""

from __future__ import annotations

import os
import tempfile
import unittest
from decimal import Decimal

from shogen_s2 import collector, report
from tests.test_collector import CLOCK, FakeClock, SKELETON, frozen_read_fn, BY_ID

SIGMA = Decimal("1e12")
TAU = Decimal("50")


class TestReport(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp(prefix="s2rep_")
        self.control = os.path.join(self.d, "control.jsonl")
        self.journal = os.path.join(self.d, "journal.jsonl")
        self.raw = os.path.join(self.d, "raw.jsonl")
        collector.collect(
            [BY_ID[f] for f in SKELETON], self.control, self.journal, self.raw,
            n_windows=3, sigma_classe=SIGMA, tau_classe=TAU,
            now_fn=FakeClock(CLOCK), sleep_fn=lambda s: None, read_fn=frozen_read_fn,
        )

    def test_three_blocks_present(self):
        txt = report.render_report(self.control, self.journal)
        self.assertIn("[BLOC 1] PARAMÈTRES", txt)
        self.assertIn("[BLOC 2] JOURNAL BRUT", txt)
        self.assertIn("[BLOC 3] R1", txt)

    def test_flag_and_stationarity_and_noneval_published(self):
        txt = report.render_report(self.control, self.journal)
        self.assertIn("HISTORIQUE INSUFFISANT", txt)          # drapeau levé (skeleton court)
        self.assertIn("A(window-stationarity)", txt)          # obligatoire (§5.3)
        self.assertIn("nonÉv", txt)                           # compte non évaluable publié
        self.assertIn("P̂_more", txt)

    def test_corrections_published(self):
        txt = report.render_report(self.control, self.journal)
        self.assertIn("sample_lead", txt)                     # δ fin de fenêtre (A)
        self.assertIn("seuil_historique_valeur", txt)         # seuil numérique (C)
        self.assertIn("n_min_hors_enveloppe", txt)            # N≥4 numérique (C)
        self.assertIn("fail-open", txt)                       # résidu staleness kraken (G)
        self.assertIn("run_params_demarrages", txt)           # concordance publiée (E)
        # Classe DÉRIVÉE du pool réel (D) : mentionne les 3 flux configurés, pas un hardcode.
        self.assertIn("pool configuré = 3 flux", txt)

    def test_deterministic(self):
        a = report.render_report(self.control, self.journal)
        b = report.render_report(self.control, self.journal)
        self.assertEqual(a, b)

    def test_recalculable_reads_only_journal_files(self):
        # La table se calcule à partir des seuls chemins de journal (aucun
        # paramètre hors-bande) : c'est le claim de recalculabilité (ADR-0003).
        txt = report.render_report(self.control, self.journal)
        self.assertIn("coinbase", txt)
        self.assertIn("s2-harness/skeleton-S2A", txt)         # version depuis run_params


if __name__ == "__main__":
    unittest.main()
