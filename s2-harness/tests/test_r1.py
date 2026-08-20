"""Tests de propriété de R1 (r1.py) — sur entrées construites, déterministes.

Familles exigées (mission M1a + raffinements ADVISOR) :
  - précédence des écarts panne > staleness > hors-enveloppe (10 §5.2) ;
  - frontière « historique insuffisant » n·P̂_more·(1−P̂_more) ≥ 10 (10 §5.4),
    testée en fonction (10−ε / 10 / 10+ε) ET en bout-en-bout ;
  - identité élémentaire P₀/P₁/P_more sur entrées connues (10 §5.1) ;
  - harnais-down non compté dans n (fenêtre absente ET lectures orphelines) ;
  - last-wins par (fenêtre, flux) + dédup des marqueurs (§5.3) ;
  - porte hors-enveloppe sur les RÉPONDANTES (N ≥ 4), pas la taille du pool ;
  - dégénérés P_more ∈ {0, 1} et n = 0 (pas de division par zéro).
"""

from __future__ import annotations

import unittest
from decimal import Decimal, localcontext

from shogen_s2 import r1
from shogen_s2.r1 import Ecart

SIGMA_HUGE = Decimal("1e12")   # jamais de staleness
TAU = Decimal("50")
D = Decimal


def rd(ws, flux, status="ok", price="64000", source_ts=None, currency="USD"):
    """Une ligne `journal.jsonl` telle que parsée (source_ts Decimal ou None)."""
    return {
        "window_start": ws, "flux_id": flux, "kind": "place", "currency": currency,
        "status": status, "http_status": 200 if status == "ok" else None,
        "price": price, "source_ts": source_ts, "fetch_ts": float(ws),
        "sha256_raw": "0" * 64, "extra": {},
    }


def mk(ws, strate="calme"):
    return {"record": "window_close", "window_start": ws, "strate": strate,
            "harness_ts": float(ws)}


class TestPoissonBinomialIdentity(unittest.TestCase):
    def test_known_values_two_sources(self):
        # p=(0.1,0.2) : P0=0.72, P1=0.1·0.8+0.2·0.9=0.26, P_more=0.02 (exact).
        p0, p1, pm = r1.poisson_binomial([D("0.1"), D("0.2")])
        self.assertEqual(p0, D("0.72"))
        self.assertEqual(p1, D("0.26"))
        self.assertEqual(pm, D("0.02"))

    def test_known_values_quarter_half(self):
        # p=(0.25,0.5) : P0=0.375, P1=0.25·0.5+0.5·0.75=0.5, P_more=0.125.
        p0, p1, pm = r1.poisson_binomial([D("0.25"), D("0.5")])
        self.assertEqual(p0, D("0.375"))
        self.assertEqual(p1, D("0.5"))
        self.assertEqual(pm, D("0.125"))

    def test_equal_p_matches_binomial(self):
        # N=3, p=0.1 : P0=0.9³=0.729 ; P1=3·0.1·0.9²=0.243 ; P_more=0.028 (exact).
        p0, p1, pm = r1.poisson_binomial([D("0.1")] * 3)
        self.assertEqual(p0, D("0.729"))
        self.assertEqual(p1, D("0.243"))
        self.assertEqual(pm, D("0.028"))

    def test_sum_is_one_by_construction(self):
        # P_more = 1 − P0 − P1 par construction : on vérifie l'invariant, pas
        # une découverte (les valeurs à la main ci-dessus testent P0 et P1).
        for phats in ([D("0.3"), D("0.7"), D("0.05")], [D("0")], [D("1"), D("0.4")]):
            p0, p1, pm = r1.poisson_binomial(phats)
            self.assertEqual(p0 + p1 + pm, D(1))


class TestGateBoundary(unittest.TestCase):
    def test_gate_function_10_minus_eps_and_plus(self):
        # P_more=0.5 → P_more·(1−P_more)=0.25 ; n·0.25 franchit 10 à n=40.
        self.assertEqual(r1.gate_value(40, D("0.5")), D("10.00"))
        self.assertFalse(r1.insufficient_history(40, D("0.5")))   # = 10 → suffisant
        self.assertTrue(r1.insufficient_history(39, D("0.5")))    # 9.75 < 10
        self.assertFalse(r1.insufficient_history(41, D("0.5")))   # 10.25 ≥ 10

    def test_pmore_zero_and_one_degenerate(self):
        # P_more ∈ {0,1} → variance produit = 0 → toujours insuffisant.
        self.assertEqual(r1.gate_value(10 ** 9, D("0")), D(0))
        self.assertEqual(r1.gate_value(10 ** 9, D("1")), D(0))
        self.assertTrue(r1.insufficient_history(10 ** 9, D("0")))
        self.assertTrue(r1.insufficient_history(10 ** 9, D("1")))


class TestZScore(unittest.TestCase):
    def test_hand_value_exact(self):
        # n=100, P_more=0.1, K=19 : mean=10, var=9, z=(19−10)/3 = 3 exact.
        self.assertEqual(r1.z_score(100, 19, D("0.1")), D(3))


class TestClassifyPrecedence(unittest.TestCase):
    def test_panne_beats_staleness_and_horsenv(self):
        # Panne : pas de valeur → écart (iii), précédence maximale, même si les
        # conditions de staleness et hors-enveloppe seraient réunies.
        reading = rd(0, "a", status="panne_transport", price=None, source_ts=None)
        kind = r1.classify_ecart(reading, [D("1"), D("2"), D("3")], 5,
                                 win_end=10 ** 9, sigma=D("60"), tau=TAU)
        self.assertIs(kind, Ecart.PANNE)

    def test_staleness_beats_horsenv(self):
        # OK mais horodatage porté vieux (win_end − src = 1000 > σ=60) → (ii),
        # même si le prix serait hors-enveloppe.
        reading = rd(0, "a", price="999999", source_ts=D("0"))
        kind = r1.classify_ecart(reading, [D("100"), D("101"), D("102")], 5,
                                 win_end=1000, sigma=D("60"), tau=TAU)
        self.assertIs(kind, Ecart.STALENESS)

    def test_horsenv_requires_four_responding(self):
        reading = rd(0, "a", price="999999", source_ts=D("999"))  # récent → pas stale
        others = [D("100"), D("101"), D("102")]
        # N=3 répondantes → enveloppe non définie → non évaluable (jamais « pas d'écart »).
        self.assertIs(
            r1.classify_ecart(reading, others[:2], 3, win_end=1000, sigma=SIGMA_HUGE, tau=TAU),
            Ecart.NON_EVAL_HORSENV,
        )
        # N=4 répondantes, prix loin de la médiane → hors-enveloppe (i).
        self.assertIs(
            r1.classify_ecart(reading, others, 4, win_end=1000, sigma=SIGMA_HUGE, tau=TAU),
            Ecart.HORS_ENVELOPPE,
        )

    def test_horsenv_inside_envelope_is_pas_ecart(self):
        reading = rd(0, "a", price="101", source_ts=D("999"))
        kind = r1.classify_ecart(reading, [D("100"), D("101"), D("102")], 4,
                                 win_end=1000, sigma=SIGMA_HUGE, tau=TAU)
        self.assertIs(kind, Ecart.PAS_ECART)

    def test_staleness_nonevaluable_without_source_ts(self):
        # source_ts absent (ex. kraken) → staleness non évaluable : on passe à (i).
        reading = rd(0, "a", price="101", source_ts=None)
        # N<4 → non évaluable hors-env (et pas de staleness) :
        self.assertIs(
            r1.classify_ecart(reading, [D("100")], 3, win_end=10, sigma=D("1"), tau=TAU),
            Ecart.NON_EVAL_HORSENV,
        )
        # N≥4, prix dans l'enveloppe → pas d'écart (staleness sautée proprement) :
        self.assertIs(
            r1.classify_ecart(reading, [D("100"), D("101"), D("102")], 4,
                              win_end=10, sigma=D("1"), tau=TAU),
            Ecart.PAS_ECART,
        )


class TestComputeR1HarnessDown(unittest.TestCase):
    def test_absent_and_orphan_windows_not_counted(self):
        pool = ["a", "b", "c"]
        markers = [mk(100), mk(160)]                 # seules 100 et 160 complétées
        readings = [
            rd(100, "a"), rd(100, "b"), rd(100, "c"),
            rd(160, "a"), rd(160, "b"), rd(160, "c"),
            rd(220, "a"), rd(220, "b"),              # lectures ORPHELINES (pas de marqueur)
            # fenêtre 280 : totalement absente (ni marqueur ni lecture)
        ]
        out = r1.compute_r1(markers, readings, pool, w=60, sigma=SIGMA_HUGE, tau=TAU)
        blk = out["strates"]["calme"]
        self.assertEqual(blk["n"], 2)                # 220 (orphelin) et 280 (absent) exclus
        for f in pool:
            # Aucune panne fabriquée pour les fenêtres non complétées.
            self.assertEqual(blk["per_source"][f]["panne"], 0)
            self.assertEqual(blk["per_source"][f]["ecart"], 0)
            self.assertEqual(blk["per_source"][f]["phat"], D(0))

    def test_no_markers_is_degenerate_flag(self):
        out = r1.compute_r1([], [rd(100, "a")], ["a"], w=60, sigma=SIGMA_HUGE, tau=TAU)
        self.assertIn("aucune fenêtre complétée", out["note"])
        self.assertTrue(out["flag_historique_insuffisant"])


class TestComputeR1LastWins(unittest.TestCase):
    def test_marker_dedup_counts_window_once(self):
        self.assertEqual(r1.build_window_strate([mk(100), mk(100)]), {100: "calme"})

    def test_reading_last_wins(self):
        m = r1.build_reading_map([rd(100, "a", price="100"), rd(100, "a", price="200")])
        self.assertEqual(m[(100, "a")]["price"], "200")

    def test_duplicate_window_counted_once_end_to_end(self):
        out = r1.compute_r1([mk(100), mk(100)], [rd(100, "a")], ["a"],
                            w=60, sigma=SIGMA_HUGE, tau=TAU)
        self.assertEqual(out["strates"]["calme"]["n"], 1)


class TestComputeR1RespondingGate(unittest.TestCase):
    def test_five_pool_two_pannes_gives_three_responding_noneval(self):
        # 5 sources, 2 pannes → 3 répondantes < 4 → hors-env non évaluable pour
        # les répondantes (porte sur les RÉPONDANTES, pas la taille du pool).
        pool = ["a", "b", "c", "d", "e"]
        readings = [
            rd(0, "a"), rd(0, "b"), rd(0, "c"),
            rd(0, "d", status="panne_http", price=None),
            rd(0, "e", status="panne_http", price=None),
        ]
        out = r1.compute_r1([mk(0)], readings, pool, w=60, sigma=SIGMA_HUGE, tau=TAU)
        ps = out["strates"]["calme"]["per_source"]
        for f in ("a", "b", "c"):
            self.assertEqual(ps[f]["non_eval_hors_env"], 1)
            self.assertEqual(ps[f]["ecart"], 0)
        for f in ("d", "e"):
            self.assertEqual(ps[f]["panne"], 1)

    def test_five_responding_horsenv_fires(self):
        pool = ["a", "b", "c", "d", "e"]
        readings = [rd(0, f, price=p, source_ts=D("999999999"))
                    for f, p in zip(pool, ["100", "100", "100", "100", "999999"])]
        out = r1.compute_r1([mk(0)], readings, pool, w=60,
                            sigma=SIGMA_HUGE, tau=TAU)
        ps = out["strates"]["calme"]["per_source"]
        self.assertEqual(ps["e"]["hors_enveloppe"], 1)     # e loin de la médiane 100
        self.assertEqual(ps["a"]["pas_ecart"], 1)


class TestComputeR1FlagEndToEnd(unittest.TestCase):
    def test_flag_fires_on_short_history(self):
        # 3 fenêtres, a et b en panne partout → K=3, P_more=1, garde=0 → drapeau.
        pool = ["a", "b", "c"]
        markers, readings = [], []
        for ws in (0, 60, 120):
            markers.append(mk(ws))
            readings += [
                rd(ws, "a", status="panne_http", price=None),
                rd(ws, "b", status="panne_http", price=None),
                rd(ws, "c", price="64000", source_ts=D(ws + 59)),
            ]
        out = r1.compute_r1(markers, readings, pool, w=60, sigma=D("30"), tau=TAU)
        blk = out["strates"]["calme"]
        self.assertEqual(blk["n"], 3)
        self.assertEqual(blk["K"], 3)                       # chaque fenêtre : 2 écarts
        self.assertEqual(blk["per_source"]["a"]["phat"], D(1))
        self.assertEqual(blk["per_source"]["b"]["phat"], D(1))
        self.assertEqual(blk["per_source"]["c"]["phat"], D(0))
        self.assertEqual(blk["P_more"], D(1))
        self.assertTrue(blk["flag_historique_insuffisant"])
        self.assertIsNone(blk["z"])

    def test_flag_clears_and_z_published_when_history_sufficient(self):
        # 60 fenêtres ; a,b en écart dans 30 → p̂=0.5 chacun, P_more=0.25,
        # garde=60·0.25·0.75=11.25 ≥ 10 → drapeau éteint, z publié.
        pool = ["a", "b"]
        markers, readings = [], []
        for i in range(60):
            ws = i * 60
            markers.append(mk(ws))
            if i < 30:
                readings += [rd(ws, "a", status="panne_http", price=None),
                             rd(ws, "b", status="panne_http", price=None)]
            else:
                readings += [rd(ws, "a", price="64000", source_ts=D(ws + 1)),
                             rd(ws, "b", price="64000", source_ts=D(ws + 1))]
        out = r1.compute_r1(markers, readings, pool, w=60, sigma=SIGMA_HUGE, tau=TAU)
        blk = out["strates"]["calme"]
        self.assertEqual(blk["n"], 60)
        self.assertEqual(blk["K"], 30)
        self.assertEqual(blk["per_source"]["a"]["phat"], D("0.5"))
        self.assertEqual(blk["P_more"], D("0.25"))
        self.assertEqual(blk["gate_value"], D("11.2500"))
        self.assertFalse(blk["flag_historique_insuffisant"])
        # z = (30 − 60·0.25)/√(11.25) = 15/√11.25 ≈ 4.4721 — référence à la même
        # précision (50) que z_score, sinon l'écart est celui du contexte par défaut.
        with localcontext() as ctx:
            ctx.prec = r1.DECIMAL_PREC
            ref = D(15) / D("11.25").sqrt()
        self.assertLess(abs(blk["z"] - ref), D("1e-40"))


if __name__ == "__main__":
    unittest.main()
