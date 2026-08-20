"""Tests du driver de lancement (run_campaign.py) — déterministes, SANS réseau.

Le driver est piloté par injection de dépendances (now_fn/sleep_fn/read_fn/
resolve_fn), comme collector.collect : lectures = fixtures gelées, horloge
scriptée, résolution ASN mockée. On exerce les propriétés PORTEUSES du driver :
  - `resolve_sigma_tau` FIDÈLE (ADR-0021) : demo/calibration → σ PAR CLASSE planchers
    ADR-0020 provisoires + τ=0,5 %% relatif ; campagne → σ/τ FINAUX committés via
    fichier (fail-closed si absent/malformé — ADR-0020 déc. 1) ; PLUS aucun scalaire
    INTERIM (voie 2 écartée, ADR-0021 :3154-3156) ;
  - la boucle par chunks vise n_windows fenêtres DISTINCTES (dédup marqueurs),
    réécrit run_params + clock_check à CHAQUE chunk (concordance §E vérifiée par
    effective_run_params), et re-mesure l'axe ASN par chunk ;
  - la reprise est IDEMPOTENTE (re-appel sur un journal déjà à n_windows ne
    collecte rien).
On ne re-teste PAS le harnais fermé (collector/r1/r2/report) : on vérifie que le
driver l'orchestre correctement et que la table §6 se rend de bout en bout.

RÉVISION TRACÉE ADR-0021 [C2b] : les tests σ/τ SCALAIRE/INTERIM (`DEMO_SIGMA_SECONDS`,
`DEMO_TAU_ABSOLUTE`, `--interim-*`) sont SUPPRIMÉS (C3 : aucun chemin scalaire ne
survit). Remplacés par les tests σ PAR CLASSE (demo/calibration = planchers
provisoires), le fail-closed de fourniture des σ/τ de campagne, et un test de
concordance qui DÉCODE les fixtures (G2 mineur : pas un ensemble codé en dur).
"""

from __future__ import annotations

import contextlib
import io
import json
import os
import tempfile
import unittest
from decimal import Decimal

from shogen_s2 import records, report, run_campaign, sources
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


class TestSigmaTauFidele(unittest.TestCase):
    def test_demo_returns_per_class_provisional_floors(self):
        # [C2b] Était : demo → scalaires DÉMO (non-ADR-0020). Désormais : σ PAR CLASSE
        # = planchers ADR-0020 provisoires (mapping) + τ FRACTION relative.
        sigma_by_class, tau, regime = run_campaign.resolve_sigma_tau("demo")
        self.assertIsInstance(sigma_by_class, dict)
        self.assertEqual(sigma_by_class, sources.default_sigma_by_class())
        self.assertEqual(sigma_by_class["place_horodatee"], Decimal("30"))
        self.assertIsNone(sigma_by_class["sans_horodatage"])
        self.assertEqual(tau, sources.TAU_CLASSE_ADR0020_FRACTION)
        self.assertEqual(tau, Decimal("0.005"))
        self.assertIn("PROVISOIRES", regime)

    def test_calibration_returns_per_class_provisional_floors(self):
        # [C2b] Était : calibration SANS interim → fail-closed. Désormais : σ planchers
        # provisoires (la capture est SANS SEUIL ; les σ finaux = clôture P99 post-hoc).
        sigma_by_class, tau, regime = run_campaign.resolve_sigma_tau("calibration")
        self.assertEqual(sigma_by_class, sources.default_sigma_by_class())
        self.assertEqual(tau, Decimal("0.005"))
        self.assertIn("CALIBRATION", regime)

    def test_campagne_without_file_fails_closed(self):
        # [C2b] Était : campagne SANS interim → fail-closed. Toujours fail-closed, mais
        # désormais parce que les σ/τ FINAUX committés (fichier) manquent (ADR-0020 déc. 1).
        with self.assertRaises(run_campaign.SigmaTauNonRepresentable):
            run_campaign.resolve_sigma_tau("campagne")

    def test_campagne_with_committed_file_loads_per_class(self):
        # σ/τ FINAUX committés (artefact `closure`) → chargés en σ PAR CLASSE + τ.
        d = tempfile.mkdtemp(prefix="s2stf_")
        path = os.path.join(d, "sigma_tau.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"sigma_classe": {"place_horodatee": "390", "agregateur": "500",
                                        "sans_horodatage": None},
                       "tau_classe": "0.005"}, f)
        sigma_by_class, tau, regime = run_campaign.resolve_sigma_tau("campagne", path)
        self.assertEqual(sigma_by_class["place_horodatee"], Decimal("390"))
        self.assertEqual(sigma_by_class["agregateur"], Decimal("500"))
        self.assertIsNone(sigma_by_class["sans_horodatage"])
        self.assertEqual(tau, Decimal("0.005"))
        self.assertIn("CAMPAGNE", regime)

    def test_campagne_file_scalar_sigma_fails_closed(self):
        # Fichier committé avec `sigma_classe` SCALAIRE → fail-closed (jamais réinterprété).
        d = tempfile.mkdtemp(prefix="s2stf_")
        path = os.path.join(d, "bad.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"sigma_classe": "1000000000000", "tau_classe": "0.005"}, f)
        with self.assertRaises(run_campaign.SigmaTauNonRepresentable):
            run_campaign.resolve_sigma_tau("campagne", path)

    def test_campagne_file_absolute_tau_fails_closed(self):
        # [G7 durcissement ADR-0021] Fichier σ VALIDE (mapping) mais `tau_classe` HORS
        # (0,1) — un τ ABSOLU legacy « 50 » → fail-closed, jamais relu en fraction 5000 %.
        d = tempfile.mkdtemp(prefix="s2stf_")
        path = os.path.join(d, "abstau.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"sigma_classe": {"place_horodatee": "30"}, "tau_classe": "50"}, f)
        with self.assertRaises(run_campaign.SigmaTauNonRepresentable):
            run_campaign.resolve_sigma_tau("campagne", path)

    def test_campagne_file_tau_null_pending_revision_fails_closed(self):
        # τ null = révision τ EN ATTENTE (clause ADR-0020) → la campagne ne peut lancer.
        d = tempfile.mkdtemp(prefix="s2stf_")
        path = os.path.join(d, "taunull.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"sigma_classe": {"place_horodatee": "30"}, "tau_classe": None}, f)
        with self.assertRaises(run_campaign.SigmaTauNonRepresentable):
            run_campaign.resolve_sigma_tau("campagne", path)

    def test_ignored_file_warning_helper(self):
        # G2 mineur (seam d'avertissement, PROUVÉ sans réseau) : --sigma-tau-file n'a de
        # sens qu'en 'campagne' ; fourni à demo/calibration → message ; sinon None.
        self.assertIsNone(run_campaign._ignored_file_warning("campagne", "x.json"))
        self.assertIsNone(run_campaign._ignored_file_warning("demo", None))
        self.assertIn("IGNORÉ", run_campaign._ignored_file_warning("demo", "x.json"))
        self.assertIn("IGNORÉ", run_campaign._ignored_file_warning("calibration", "x.json"))

    def test_main_campagne_without_file_returns_failclosed_code(self):
        # [C2b] Était : main calibration → code 3, rien écrit. Désormais : campagne SANS
        # --sigma-tau-file → fail-closed AVANT toute collecte (code 3, aucun journal).
        d = tempfile.mkdtemp(prefix="s2drv_")
        # G2 mineur « bruit stderr » : le message fail-closed du driver va sur stderr
        # (stdout réservé) ; on le CAPTURE ici pour ne pas polluer la sortie des tests,
        # et on VÉRIFIE qu'il porte bien la raison (fail-closed lisible, pas muet).
        buf = io.StringIO()
        with contextlib.redirect_stderr(buf):
            rc = run_campaign.main(["--phase", "campagne", "--journal-dir", d,
                                    "--windows", "1"])
        self.assertEqual(rc, 3)     # fail-closed, code distinct
        self.assertIn("FAIL-CLOSED", buf.getvalue())
        self.assertFalse(os.path.exists(os.path.join(d, "control.jsonl")))

    def test_sigma_class_of_flux_covers_pool_matches_decoded_fixtures(self):
        # G2 mineur : concordance « sans_horodatage ⟺ décodeur rend source_ts=None »
        # VÉRIFIÉE en DÉCODANT les fixtures (pas un ensemble codé en dur). Le dispatch
        # (sources.SIGMA_CLASS_OF_FLUX) couvre le pool ET s'accorde aux décodeurs.
        from tests.test_collector import FIX
        pool = [s.flux_id for s in SPECS]
        for f in pool:
            self.assertIn(f, sources.SIGMA_CLASS_OF_FLUX)
        # Décoder chaque fixture → source_ts None ?  (les décodeurs réels de sources.py)
        decoded_none = set()
        for s in SPECS:
            path = os.path.join(FIX, s.flux_id + ".bin")
            if not os.path.exists(path):
                continue
            with open(path, "rb") as fh:
                _price, source_ts, _extra = s.decode(fh.read())
            if source_ts is None:
                decoded_none.add(s.flux_id)
        declared_sans = {f for f, c in sources.SIGMA_CLASS_OF_FLUX.items()
                         if c == "sans_horodatage"}
        # L'ensemble « sans_horodatage » déclaré == l'ensemble MESURÉ (décodé) à None.
        self.assertEqual(declared_sans, decoded_none)
        self.assertEqual(declared_sans, {"binance", "kraken", "bitfinex"})


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
        # [C2b] σ PAR CLASSE (planchers ADR-0020 provisoires, comme la phase demo réelle)
        # au lieu des scalaires DEMO supprimés.
        return run_campaign.run_segment(
            self.specs, self.d, "demo", n_windows,
            w=60, sample_lead=10.0, sigma_by_class=sources.default_sigma_by_class(),
            tau=sources.TAU_CLASSE_ADR0020_FRACTION, regime="TEST", chunk_windows=chunk,
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
        # concordance §E : les 2 run_params s'accordent sur les champs porteurs (dont
        # sigma_classe MAPPING + sigma_class_of_flux — ADR-0021)
        eff = records.effective_run_params(
            params_list,
            load_bearing=records.LOAD_BEARING_KEYS + records.R2_LOAD_BEARING_KEYS)
        self.assertEqual(list(eff["pool"]), SKELETON)
        self.assertIsInstance(eff["sigma_classe"], dict)
        self.assertEqual(eff["sigma_class_of_flux"]["kraken"], "sans_horodatage")
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
