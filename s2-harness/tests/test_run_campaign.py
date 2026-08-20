"""Tests du driver de lancement (run_campaign.py) — déterministes, SANS réseau.

Le driver est piloté par injection de dépendances (now_fn/sleep_fn/read_fn/
resolve_fn), comme collector.collect : lectures = fixtures gelées, horloge
scriptée, résolution ASN mockée. On exerce les propriétés PORTEUSES du driver :
  - `resolve_sigma_tau` FAIL-CLOSED (le CONSTAT σ/τ : jamais un scalaire silencieux
    présenté comme ADR-0020) ;
  - la boucle par chunks vise n_windows fenêtres DISTINCTES (dédup marqueurs),
    réécrit run_params + clock_check à CHAQUE chunk (concordance §E vérifiée par
    effective_run_params), et re-mesure l'axe ASN par chunk ;
  - la reprise est IDEMPOTENTE (re-appel sur un journal déjà à n_windows ne
    collecte rien).
On ne re-teste PAS le harnais fermé (collector/r1/r2/report) : on vérifie que le
driver l'orchestre correctement et que la table §6 se rend de bout en bout.
"""

from __future__ import annotations

import os
import tempfile
import unittest
from decimal import Decimal

from shogen_s2 import records, report, run_campaign
from shogen_s2.sources import SPECS

BY_ID = {s.flux_id: s for s in SPECS}
SKELETON = ["coinbase", "kraken", "bitstamp"]     # 3 places USD à fixtures gelées

# Horloge scriptée : collector.collect appelle now_fn 1 (start) + 2/fenêtre. Deux
# chunks d'1 fenêtre → 6 appels ; les deux fenêtres tombent dans DEUX buckets UTC
# distincts (1785946260 puis 1785946320) → 2 fenêtres distinctes.
CLOCK = [
    1785946290.0, 1785946291.0, 1785946310.0,     # chunk 1 : start, now(bucket 260), t_read
    1785946325.0, 1785946326.0, 1785946375.0,      # chunk 2 : start, now(bucket 320), t_read
]


class FakeClock:
    def __init__(self, times):
        self.times = list(times)
        self.i = 0

    def __call__(self):
        v = self.times[self.i]
        self.i += 1
        return v


def frozen_read_fn(spec, ts):
    from tests.test_collector import frozen_reading
    return frozen_reading(spec.flux_id, ts)


def mock_resolve(host, resolvers=None):
    """Résolution ASN déterministe (pas de réseau) : toutes concordantes AS111."""
    return {"host": host, "status": "ok", "resolver": "mock", "ip": "1.2.3.4",
            "ip_secondary": [], "cname_chain": [], "prefix": "1.2.3.0/24",
            "asn_ripestat": 111, "asn_cymru": 111, "holder": "MOCK-AS"}


class TestSigmaTauFailClosed(unittest.TestCase):
    def test_demo_returns_labeled_demo_scalars(self):
        sigma, tau, regime = run_campaign.resolve_sigma_tau("demo")
        self.assertEqual(sigma, run_campaign.DEMO_SIGMA_SECONDS)
        self.assertEqual(tau, run_campaign.DEMO_TAU_ABSOLUTE)
        self.assertIn("DÉMO", regime)
        self.assertIn("NON-ADR-0020", regime)

    def test_calibration_without_interim_fails_closed(self):
        with self.assertRaises(run_campaign.SigmaTauNonRepresentable):
            run_campaign.resolve_sigma_tau("calibration")

    def test_campagne_without_interim_fails_closed(self):
        with self.assertRaises(run_campaign.SigmaTauNonRepresentable):
            run_campaign.resolve_sigma_tau("campagne")

    def test_partial_interim_fails_closed(self):
        with self.assertRaises(run_campaign.SigmaTauNonRepresentable):
            run_campaign.resolve_sigma_tau("campagne", interim_sigma="30")

    def test_full_interim_is_declared_interim(self):
        sigma, tau, regime = run_campaign.resolve_sigma_tau(
            "calibration", interim_sigma="30", interim_tau="0.005")
        self.assertEqual(sigma, Decimal("30"))
        self.assertEqual(tau, Decimal("0.005"))
        self.assertIn("INTERIM", regime)

    def test_main_calibration_returns_failclosed_code(self):
        d = tempfile.mkdtemp(prefix="s2drv_")
        rc = run_campaign.main(["--phase", "calibration", "--journal-dir", d,
                                "--windows", "1"])
        self.assertEqual(rc, 3)     # fail-closed, code distinct
        # rien n'a été écrit (aucune fenêtre) : fail-closed AVANT toute collecte
        self.assertFalse(os.path.exists(os.path.join(d, "control.jsonl")))

    def test_adr0020_sigma_class_covers_pool_and_matches_source_ts(self):
        # Le dispatch flux→classe σ couvre le pool ET les « sans_horodatage » sont
        # EXACTEMENT les flux à source_ts=None (concordance CONSTAT).
        pool = [s.flux_id for s in SPECS]
        for f in pool:
            self.assertIn(f, run_campaign.SIGMA_CLASS_OF_FLUX)
        sans = {f for f, c in run_campaign.SIGMA_CLASS_OF_FLUX.items()
                if c == "sans_horodatage"}
        self.assertEqual(sans, {"binance", "kraken", "bitfinex"})


class TestDistinctCompleted(unittest.TestCase):
    def test_absent_file_is_zero(self):
        self.assertEqual(run_campaign.distinct_completed("/nonexistent/x.jsonl"), 0)


class RunSegmentCase(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp(prefix="s2drv_")
        self.control = os.path.join(self.d, "control.jsonl")
        self.journal = os.path.join(self.d, "journal.jsonl")
        self.specs = [BY_ID[f] for f in SKELETON]

    def _run(self, n_windows, clock, chunk=1):
        return run_campaign.run_segment(
            self.specs, self.d, "demo", n_windows,
            w=60, sample_lead=10.0, sigma=run_campaign.DEMO_SIGMA_SECONDS,
            tau=run_campaign.DEMO_TAU_ABSOLUTE, regime="TEST", chunk_windows=chunk,
            now_fn=FakeClock(clock), sleep_fn=lambda s: None,
            read_fn=frozen_read_fn, resolve_fn=mock_resolve, log=lambda m: None,
        )

    def test_two_chunks_distinct_windows_and_concordant_run_params(self):
        done = self._run(2, CLOCK, chunk=1)
        self.assertEqual(done, 2)
        self.assertEqual(run_campaign.distinct_completed(self.control), 2)
        params_list, clocks, markers = records.parse_control(self.control)
        asn = records.parse_asn(self.control)
        # un run_params + un clock_check PAR chunk (réécrits à chaque (re)démarrage)
        self.assertEqual(len(params_list), 2)
        self.assertEqual(len(clocks), 2)
        # 3 hôtes distincts × 2 chunks (cadence ASN ≥ 1/chunk)
        self.assertEqual(len(asn), 6)
        # concordance §E : les 2 run_params s'accordent sur les champs porteurs
        eff = records.effective_run_params(
            params_list,
            load_bearing=records.LOAD_BEARING_KEYS + records.R2_LOAD_BEARING_KEYS)
        self.assertEqual(list(eff["pool"]), SKELETON)
        # 2 fenêtres distinctes journalées
        self.assertEqual(len({int(m["window_start"]) for m in markers}), 2)

    def test_resume_is_idempotent_no_overcollect(self):
        self._run(2, CLOCK, chunk=1)
        # ré-appel visant le MÊME total : la boucle ne doit RIEN re-collecter
        # (idempotence de reprise). Aucune tick d'horloge consommée (liste vide OK).
        done = self._run(2, [], chunk=1)
        self.assertEqual(done, 2)
        self.assertEqual(run_campaign.distinct_completed(self.control), 2)

    def test_end_to_end_table6_renders(self):
        self._run(2, CLOCK, chunk=1)
        text = report.render_report(self.control, self.journal)
        self.assertIn("TABLE §6", text)
        self.assertIn("[BLOC 6]", text)
        # déterminisme : un second rendu est identique (répétition de l'oracle)
        self.assertEqual(text, report.render_report(self.control, self.journal))


if __name__ == "__main__":
    unittest.main()
