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

RÉVISION TRACÉE ADR-0021 [C2b] : `collector.collect` prend désormais `sigma_by_class`
(mapping classe→plancher) au lieu de `sigma_classe` scalaire, et `tau_classe` est une
FRACTION relative (au lieu d'un montant absolu). DEUX tests dépendaient du contrat
scalaire/absolu et sont convertis EXPLICITEMENT (jamais affaiblis) :
  - `test_no_false_staleness_realistic_sigma` : la source FIGÉE testée passe de
    `kraken` (classe `sans_horodatage` → staleness « non évaluable » par fidélité
    ADR-0020, quel que soit un source_ts injecté) à `bitstamp` (classe
    `place_horodatee`, σ évaluable) ; on VÉRIFIE de plus que kraken reste non
    évaluable même avec un horodatage injecté (le dispatch est PAR CLASSE) ;
  - `test_horsenveloppe_on_mixed_class_flags_bitfinex` : τ absolu 60 $ → τ RELATIF
    0,1 % (bitfinex rel 0.00107 > 0.001, seul hors-enveloppe ; okx_ticker 0.00085 et
    kraken 0.0000178 dedans — écarts LOO recalculés sur les fixtures).
"""

from __future__ import annotations

import contextlib
import io
import json
import os
import tempfile
import unittest
from decimal import Decimal

from datetime import datetime, timezone

from shogen_s2 import collector, lm, r1, records, window
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

# [C2b] Étaient `SIGMA = Decimal("1e12")` (σ SCALAIRE) et `TAU = Decimal("50")` (τ
# ABSOLU). σ PAR CLASSE : planchers énormes → jamais de staleness ; sans_horodatage
# = None (« non évaluable »). τ = FRACTION relative.
SIGMA_HUGE = Decimal("1e12")
TAU = Decimal("0.005")                             # τ RELATIF (fraction) — était 50 ABSOLU


def _taumap(t):
    """τ PAR CLASSE (ADR-0022) : diffuse un τ scalaire sur les 5 classes (adaptateur test)."""
    return {c: t for c in ("oracle_pyth", "oracle_chainlink", "agregateur",
                           "place_horodatee", "sans_horodatage")}


def sbc_huge() -> dict:
    """sigma_by_class « propre » : aucune staleness possible (planchers énormes)."""
    return {"place_horodatee": SIGMA_HUGE, "agregateur": SIGMA_HUGE,
            "sans_horodatage": None, "oracle_pyth": SIGMA_HUGE,
            "oracle_chainlink": SIGMA_HUGE}


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

    def _collect(self, read_fn=frozen_read_fn, clock=None, sigma_by_class=None):
        return collector.collect(
            self.specs, self.control, self.journal, self.raw, n_windows=3,
            sigma_by_class=sigma_by_class or sbc_huge(), tau_classe=_taumap(TAU),
            now_fn=FakeClock(clock or CLOCK), sleep_fn=lambda s: None, read_fn=read_fn,
        )


class TestCollectClean(CollectorCase):
    def test_end_to_end_clean_run(self):
        completed = self._collect()
        self.assertEqual(completed, 3)

        params_list, clocks, markers = records.parse_control(self.control)
        self.assertEqual(len(params_list), 1)
        self.assertEqual(params_list[-1]["pool"], SKELETON)
        # σ PAR CLASSE écrit en run_params (mapping) + dispatch flux→classe (ADR-0021).
        self.assertIsInstance(params_list[-1]["sigma_classe"], dict)
        self.assertEqual(params_list[-1]["sigma_class_of_flux"]["kraken"], "sans_horodatage")
        self.assertEqual(params_list[-1]["sigma_class_of_flux"]["coinbase"], "place_horodatee")
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
        # LE test qui aurait attrapé M-1 : σ RÉALISTE (place_horodatee=30 s),
        # échantillonnage en fin de fenêtre. Source FIGÉE (bitstamp, classe évaluable)
        # → stale ; sources fraîches → 0. [C2b] : bitstamp remplace kraken comme source
        # figée (kraken est `sans_horodatage` → staleness non évaluable PAR CLASSE, ce
        # qu'on vérifie AUSSI : un source_ts injecté ne la rend pas évaluable).
        w_r, delta_r = 60, 2.0
        buckets_r = [0, 60, 120]
        treads_r = [b + w_r - delta_r for b in buckets_r]      # 58, 118, 178
        nows_r = [5.0, 65.0, 125.0]
        clock_r = [1.0, nows_r[0], treads_r[0], nows_r[1], treads_r[1], nows_r[2], treads_r[2]]

        def read_fn(spec, ts):
            src = 1.0 if spec.flux_id == "bitstamp" else ts    # bitstamp figé, autres frais
            return Reading(flux_id=spec.flux_id, kind=spec.kind, endpoint=spec.endpoint,
                           fetch_ts=ts, status=Status.OK, http_status=200, raw=b"payload",
                           price=Decimal("64000"), currency=Currency.USD, source_ts=src)

        sleeps: list[float] = []
        # place_horodatee = 30 s (coinbase, bitstamp) ; sans_horodatage = None (kraken).
        collector.collect(self.specs, self.control, self.journal, self.raw, n_windows=3,
                          sigma_by_class={"place_horodatee": Decimal("30"),
                                          "sans_horodatage": None},
                          tau_classe=_taumap(TAU), w=w_r, sample_lead=delta_r,
                          now_fn=FakeClock(clock_r), sleep_fn=sleeps.append, read_fn=read_fn)
        # Épingle le MÉCANISME (pas seulement le comportement) : dors d'abord,
        # lis à ws+w−δ. sleep = (ws+w−δ) − now = 58−5 / 118−65 / 178−125 = 53 s.
        # Une régression `ts_sample = ws+δ` ne dormirait pas → sleeps ≠ [53,53,53].
        self.assertEqual(sleeps, [53.0, 53.0, 53.0])
        blk = r1.recompute_from_journal(self.control, self.journal)["strates"]["calme"]
        self.assertEqual(blk["n"], 3)
        self.assertEqual(blk["per_source"]["coinbase"]["staleness"], 0)   # fraîche → 0 (M-1)
        self.assertEqual(blk["per_source"]["bitstamp"]["staleness"], 3)   # figée place → stale
        self.assertEqual(blk["per_source"]["kraken"]["staleness"], 0)     # sans_horodatage → non éval.
        self.assertEqual(blk["per_source"]["bitstamp"]["phat"], Decimal(1))
        self.assertEqual(blk["per_source"]["coinbase"]["phat"], Decimal(0))
        self.assertEqual(blk["per_source"]["kraken"]["phat"], Decimal(0))  # jamais stale (classe)

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
        self._collect(sigma_by_class=sbc_huge())
        collector.collect(self.specs, self.control, self.journal, self.raw, n_windows=3,
                          sigma_by_class={"place_horodatee": Decimal("999"),
                                          "sans_horodatage": None},
                          tau_classe=_taumap(TAU),
                          now_fn=FakeClock(CLOCK), sleep_fn=lambda s: None, read_fn=frozen_read_fn)
        with self.assertRaises(ValueError):
            r1.recompute_from_journal(self.control, self.journal)

    def test_divergent_strate_calendar_fail_closed(self):
        # Changement de calendrier de strates mi-campagne → recalcul refusé
        # (strate_calendar est PORTEUR, §E/§5.3) : deux partitions ne se mélangent
        # pas en silence dans le même n par strate.
        self._collect()                                    # 1er démarrage : spec single
        collector.collect(self.specs, self.control, self.journal, self.raw, n_windows=3,
                          sigma_by_class=sbc_huge(), tau_classe=_taumap(TAU),
                          strate_spec=window.WEEKEND_STRATE_SPEC,  # 2ᵉ : calendrier différent
                          now_fn=FakeClock(CLOCK), sleep_fn=lambda s: None, read_fn=frozen_read_fn)
        with self.assertRaises(ValueError):
            r1.recompute_from_journal(self.control, self.journal)

    def test_missing_load_bearing_key_fail_closed(self):
        # Journal amputé d'une clé PORTEUSE : le harnais recalculerait sous défaut
        # silencieux là où un tiers refuse → présence fail-closed (§E). Les DEUX
        # chemins de recompute (r1, lm) lèvent (report passe par la même garde).
        self._collect()
        with open(self.control, encoding="utf-8") as fh:
            lines = fh.read().splitlines()
        for i, ln in enumerate(lines):
            obj = json.loads(ln)
            if obj.get("record") == "run_params":
                obj.pop("seuil_historique_valeur", None)   # clé porteuse retirée
                lines[i] = json.dumps(obj, ensure_ascii=False)
                break
        with open(self.control, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        with self.assertRaises(ValueError):
            r1.recompute_from_journal(self.control, self.journal)
        with self.assertRaises(ValueError):
            lm.recompute_lm_from_journal(self.control, self.journal)

    def test_legacy_scalar_sigma_classe_fail_closed(self):
        # [C3] TEST NOMMÉ : un journal LEGACY portant un `sigma_classe` SCALAIRE, lu
        # par le nouveau code, LÈVE via `effective_run_params` — jamais réinterprété
        # en σ unique (la déviation silencieuse d'ADR-0020 déc. 3 que la passe supprime).
        self._collect()
        with open(self.control, encoding="utf-8") as fh:
            lines = fh.read().splitlines()
        for i, ln in enumerate(lines):
            obj = json.loads(ln)
            if obj.get("record") == "run_params":
                obj["sigma_classe"] = "1000000000000"      # SCALAIRE legacy (str)
                lines[i] = json.dumps(obj, ensure_ascii=False)
                break
        with open(self.control, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        with self.assertRaisesRegex(ValueError, "SCALAIRE legacy"):
            r1.recompute_from_journal(self.control, self.journal)
        with self.assertRaisesRegex(ValueError, "SCALAIRE legacy"):
            lm.recompute_lm_from_journal(self.control, self.journal)


class TestTwoStrateCalendar(CollectorCase):
    """Calendrier 2-strates ex ante (§5.3) collecté de bout en bout : étiquettes
    de marqueur correctes, comptage PAR strate, et fail-closed sur trafiquage."""

    @staticmethod
    def _bucket(y, mo, d, h):
        ws = int(datetime(y, mo, d, h, tzinfo=timezone.utc).timestamp())
        return ws - ws % W

    def _collect_weekend(self):
        sat = self._bucket(2026, 8, 8, 12)     # samedi
        sun = self._bucket(2026, 8, 9, 12)     # dimanche
        mon = self._bucket(2026, 8, 10, 12)    # lundi
        # Sanity via l'autorité datetime (jamais une constante crue).
        self.assertEqual(datetime.fromtimestamp(sat, timezone.utc).weekday(), 5)
        self.assertEqual(datetime.fromtimestamp(mon, timezone.utc).weekday(), 0)
        buckets = [sat, sun, mon]
        treads = [b + W - DELTA for b in buckets]
        clock = [float(sat)]
        for b, tr in zip(buckets, treads):
            clock += [float(b) + 1.0, float(tr)]
        collector.collect(
            self.specs, self.control, self.journal, self.raw, n_windows=3,
            sigma_by_class=sbc_huge(), tau_classe=_taumap(TAU), strate_spec=window.WEEKEND_STRATE_SPEC,
            now_fn=FakeClock(clock), sleep_fn=lambda s: None, read_fn=frozen_read_fn,
        )
        return sat, sun, mon

    def test_markers_carry_calendar_strate_and_counts_per_strate(self):
        sat, sun, mon = self._collect_weekend()
        params_list, _c, markers = records.parse_control(self.control)
        by_ws = {m["window_start"]: m["strate"] for m in markers}
        self.assertEqual(by_ws[sat], "stress")
        self.assertEqual(by_ws[sun], "stress")
        self.assertEqual(by_ws[mon], "calme")
        # run_params porte la spec (recalculable + porteuse, §E).
        params = records.effective_run_params(params_list)
        self.assertEqual(params["strate_calendar"]["kind"], "weekend_utc")
        # Comptage PAR strate (§5.3) : la garde §5.4 et R1 se comptent par strate.
        out = r1.recompute_from_journal(self.control, self.journal)
        self.assertEqual(out["strates"]["stress"]["n"], 2)   # samedi + dimanche
        self.assertEqual(out["strates"]["calme"]["n"], 1)    # lundi

    def test_tampered_marker_strate_is_fail_closed(self):
        sat, _sun, _mon = self._collect_weekend()
        # Trafique l'étiquette d'un marqueur : samedi ré-étiqueté « calme » (≠ spec).
        with open(self.control, encoding="utf-8") as fh:
            lines = fh.read().splitlines()
        for i, ln in enumerate(lines):
            obj = json.loads(ln)
            if obj.get("record") == "window_close" and obj["window_start"] == sat:
                obj["strate"] = "calme"
                lines[i] = json.dumps(obj, ensure_ascii=False)
                break
        with open(self.control, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        # Les TROIS points d'entrée « recalculable » rejettent la strate trafiquée.
        with self.assertRaises(ValueError):
            r1.recompute_from_journal(self.control, self.journal)
        with self.assertRaises(ValueError):
            lm.recompute_lm_from_journal(self.control, self.journal)


class TestFullPool(CollectorCase):
    """Pool complet — 11 sources répondantes / 12 flux (10 §3.1), sur fixtures."""

    def setUp(self):
        super().setUp()
        self.specs = list(SPECS)                       # les 12 flux, décodeurs réutilisés

    def test_collect_all_twelve_flux_clean(self):
        completed = collector.collect(
            self.specs, self.control, self.journal, self.raw, n_windows=3,
            sigma_by_class=sbc_huge(), tau_classe=_taumap(Decimal("1e9")),   # τ relatif énorme → rien hors-env
            now_fn=FakeClock(CLOCK), sleep_fn=lambda s: None, read_fn=frozen_read_fn,
        )
        self.assertEqual(completed, 3)
        self.assertEqual(_count_lines(self.journal), 36)   # 3 fenêtres × 12 flux
        blk = r1.recompute_from_journal(self.control, self.journal)["strates"]["calme"]
        self.assertEqual(blk["n"], 3)
        for f in [s.flux_id for s in SPECS]:               # σ/τ énormes → rien en écart
            self.assertEqual(blk["per_source"][f]["ecart"], 0)
        # Devise MARQUÉE par flux (§2, décision 4) : 10 USD / 2 USDT dans le pool.
        readings = r1.parse_journal(self.journal)
        cur = {r["flux_id"]: r["currency"] for r in readings}
        self.assertEqual(cur["binance"], "USDT")
        self.assertEqual(cur["okx_ticker"], "USDT")
        self.assertEqual(sum(1 for c in cur.values() if c == "USDT"), 2)
        self.assertEqual(sum(1 for c in cur.values() if c == "USD"), 10)

    def test_horsenveloppe_on_mixed_class_flags_bitfinex(self):
        # Classe « BTC/USD-stable », devise marquée (§2/§9.4) : l'enveloppe
        # leave-one-out MÊLE USD et USDT. [C2b] τ RELATIF 0,1 % (était τ=60 ABSOLU $) ;
        # écarts LOO recalculés sur les fixtures (median_LOO par flux) :
        #   bitfinex rel = 69.25/64475.75  = 0.00107405  > 0.001 → HORS-ENVELOPPE (seul) ;
        #   okx_ticker rel = 54.95/64475.75 = 0.00085226 < 0.001 → dedans ;
        #   kraken   rel = 1.15/64475.75    = 0.00001784 < 0.001 → dedans.
        # (τ de test 0,1 % < τ campagne 0,5 % : les fixtures honnêtes ont un écart LOO
        #  max de 0,107 % — bitfinex, cohérent avec ADR-0020 « 0,118 %, §3.1 » — donc
        #  0,5 % ne flaggerait rien ; 0,1 % garde un hors-enveloppe à tester.)
        collector.collect(
            self.specs, self.control, self.journal, self.raw, n_windows=3,
            sigma_by_class=sbc_huge(), tau_classe=_taumap(Decimal("0.001")),
            now_fn=FakeClock(CLOCK), sleep_fn=lambda s: None, read_fn=frozen_read_fn,
        )
        blk = r1.recompute_from_journal(self.control, self.journal)["strates"]["calme"]
        self.assertEqual(blk["per_source"]["bitfinex"]["hors_enveloppe"], 3)
        self.assertEqual(blk["per_source"]["kraken"]["hors_enveloppe"], 0)
        self.assertEqual(blk["per_source"]["kraken"]["pas_ecart"], 3)
        # Un flux USDT (okx_ticker, rel 0.00085 < 0.001) reste dans l'enveloppe à ce τ.
        self.assertEqual(blk["per_source"]["okx_ticker"]["hors_enveloppe"], 0)


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
