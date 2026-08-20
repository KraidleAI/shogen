"""Tests de la table §6 minimale (report.py) — recalculable, déterministe.

La table se régénère depuis les fichiers de journal SEULS (ADR-0003) ; on
vérifie le déterminisme (même journal → même texte), la présence des trois
blocs, du drapeau « historique insuffisant » (attendu sur skeleton court), de
la ligne A(window-stationarity) obligatoire (§5.3) et de la publication du
compte « hors-env non évaluable ».
"""

from __future__ import annotations

import json
import os
import tempfile
import unittest
from decimal import Decimal

from shogen_s2 import collector, report
from shogen_s2.model import Currency, Reading, Status
from tests.test_collector import (
    BY_ID,
    CLOCK,
    SKELETON,
    TREADS,
    FakeClock,
    frozen_read_fn,
    frozen_reading,
)

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

    def test_lm_and_deferred_blocks_present(self):
        txt = report.render_report(self.control, self.journal)
        self.assertIn("[BLOC 4] L&M", txt)                    # estimateur L&M (§5.5)
        self.assertIn("Ê(Θ)", txt)
        self.assertIn("Var̂(Θ)", txt)
        self.assertIn("corrélations φ signées", txt)
        self.assertIn("[BLOC 5] R2", txt)                     # R2 différé (VIDE)
        self.assertIn("[BLOC 6] TÊTE DE CERTIFICAT", txt)     # certificat différé (VIDE)
        self.assertIn("DIFFÉRÉ À M1c", txt)
        self.assertIn("DRAPEAU 2", txt)                       # nommé, non calculé
        self.assertIn("renvoi M1c", txt)                      # renvois L&M nommés

    def test_currency_marked_class_published(self):
        txt = report.render_report(self.control, self.journal)
        self.assertIn("devise_composition", txt)              # composition du pool
        self.assertIn("BTC/USD-stable", txt)                  # classe à devise marquée
        self.assertIn("residu_peg_usdt_usd", txt)             # résidu peg nommé (→ M1c)
        self.assertIn("R2(2a)", txt)

    def test_strate_calendar_published(self):
        txt = report.render_report(self.control, self.journal)
        self.assertIn("strate_calendar", txt)                 # calendrier committé (§5.3)

    def test_missing_load_bearing_key_fail_closed(self):
        # 3ᵉ chemin recalculable : render_report refuse un journal amputé d'une
        # clé porteuse (présence fail-closed, §E), symétrique avec l'oracle.
        with open(self.control, encoding="utf-8") as fh:
            lines = fh.read().splitlines()
        for i, ln in enumerate(lines):
            obj = json.loads(ln)
            if obj.get("record") == "run_params":
                obj.pop("strate_calendar", None)
                lines[i] = json.dumps(obj, ensure_ascii=False)
                break
        with open(self.control, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        with self.assertRaises(ValueError):
            report.render_report(self.control, self.journal)

    def test_deterministic(self):
        a = report.render_report(self.control, self.journal)
        b = report.render_report(self.control, self.journal)
        self.assertEqual(a, b)

    def test_recalculable_reads_only_journal_files(self):
        # La table se calcule à partir des seuls chemins de journal (aucun
        # paramètre hors-bande) : c'est le claim de recalculabilité (ADR-0003).
        txt = report.render_report(self.control, self.journal)
        self.assertIn("coinbase", txt)
        self.assertIn("s2-harness/S2A-M1b", txt)              # version depuis run_params


class TestReportQueueExacte(unittest.TestCase):
    """La queue binomiale exacte s'affiche au bloc R1 sous la garde NON dégénérée
    (0 < P̂_more < 1) — §5.4, au lieu d'un z vide de sens."""

    def test_queue_shown_when_guard_nondegenerate(self):
        d = tempfile.mkdtemp(prefix="s2repq_")
        control = os.path.join(d, "control.jsonl")
        journal = os.path.join(d, "journal.jsonl")
        raw = os.path.join(d, "raw.jsonl")

        def read_fn(spec, ts):
            # kraken & bitstamp en panne dans la 2ᵉ fenêtre → K=1, P_more=1/9 ∈ (0,1).
            if spec.flux_id in ("kraken", "bitstamp") and ts == TREADS[1]:
                return Reading(flux_id=spec.flux_id, kind=spec.kind, endpoint=spec.endpoint,
                               fetch_ts=ts, status=Status.PANNE_TRANSPORT, currency=Currency.USD)
            return frozen_reading(spec.flux_id, ts)

        collector.collect([BY_ID[f] for f in SKELETON], control, journal, raw, n_windows=3,
                          sigma_classe=SIGMA, tau_classe=TAU,
                          now_fn=FakeClock(CLOCK), sleep_fn=lambda s: None, read_fn=read_fn)
        txt = report.render_report(control, journal)
        self.assertIn("queue exacte", txt)                    # publiée (non dégénérée)
        self.assertIn("Bin(n=3", txt)
        self.assertNotIn("queue dégénérée", txt)


if __name__ == "__main__":
    unittest.main()
