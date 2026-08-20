"""Tests de l'estimateur L&M (lm.py) — déterministes, sur entrées construites.

Familles (mission M1b + §5.5 + conseils ADVISOR) :
  - **test de propriété §5.5** : la forme par paires est sans biais sous le modèle
    binomial intra-fenêtre — `E[m(m−1)] = N(N−1)·θ²`, exercé par ESPÉRANCE EXACTE
    sur la pmf binomiale (déterministe, plus fort qu'un Monte-Carlo) ;
  - **identité de cohérence R1↔L&M** : `Ê(Θ) = (1/N)·Σ_i p̂_i` (même classification,
    mêmes marqueurs) — structurellement exacte (sum_m == Σ écarts_i) ;
  - Ê(Θ), Ê(Θ²), Var̂(Θ) sur un cas à la main (Var̂ < 0 admis, §5.5) ;
  - corrélations phi SIGNÉES : co-défaillance (+1), anti-corrélation (−1),
    indicatrice constante → None (jamais un 0 fabriqué) ;
  - par strate : les séries m_j se coupent par strate ;
  - dégénéré N < 2 → Ê(Θ²)/Var̂ non calculables (None), nommés.
"""

from __future__ import annotations

import math
import unittest
from decimal import Decimal, localcontext

from shogen_s2 import lm, r1
from tests.test_r1 import mk, rd

SIGMA_HUGE = Decimal("1e12")
TAU = Decimal("50")
D = Decimal
PREC = r1.DECIMAL_PREC


def panne(ws, flux):
    return rd(ws, flux, status="panne_http", price=None)


def clean(ws, flux, price="64000"):
    return rd(ws, flux, price=price, source_ts=None)


class TestPairwisePropertyEmmMinus1(unittest.TestCase):
    """§5.5 « à exercer par test de propriété en S2 » : sous m ~ Bin(N, θ),
    E[ m(m−1)/(N(N−1)) ] = θ² — donc la forme par paires estime E(Θ²) sans biais.
    Espérance EXACTE sur la pmf (aucune simulation, recalculable à prec fixée)."""

    def _expected_pairwise(self, N: int, theta: Decimal) -> Decimal:
        with localcontext() as ctx:
            ctx.prec = PREC
            q = D(1) - theta
            acc = D(0)
            for m in range(0, N + 1):
                pmf = D(math.comb(N, m)) * (theta ** m) * (q ** (N - m))
                acc += pmf * lm.pairwise_second_moment(m, N)
            return +acc

    def test_pairwise_estimator_unbiased_for_theta_squared(self):
        # θ à développement décimal fini → égalité à prec fixée (tol 1e-45).
        for N in (2, 3, 4, 5, 12):
            for theta in (D("0.25"), D("0.5"), D("0.1"), D("0.75")):
                got = self._expected_pairwise(N, theta)
                with localcontext() as ctx:
                    ctx.prec = PREC
                    ref = +(theta * theta)
                self.assertLess(abs(got - ref), D("1e-45"),
                                f"N={N} θ={theta} : {got} ≠ θ²={ref}")

    def test_pairwise_second_moment_hand_values(self):
        self.assertEqual(lm.pairwise_second_moment(0, 4), D(0))
        self.assertEqual(lm.pairwise_second_moment(1, 4), D(0))
        self.assertEqual(lm.pairwise_second_moment(4, 4), D(1))          # 12/12
        with localcontext() as ctx:                                      # 1/6 répété → prec fixée
            ctx.prec = PREC
            ref_sixth = D(2) / D(12)
        self.assertEqual(lm.pairwise_second_moment(2, 4), ref_sixth)     # 1/6, bit-identique


class TestConsistencyWithR1(unittest.TestCase):
    """Identité de cohérence Ê(Θ) = (1/N)·Σ_i p̂_i (résolution ADVISOR)."""

    def _build(self):
        # N=4 pool ; win0 : a,b panne (m=2) ; win1 : a panne (m=1).
        pool = ["a", "b", "c", "d"]
        markers = [mk(0), mk(60)]
        readings = [
            panne(0, "a"), panne(0, "b"), clean(0, "c"), clean(0, "d"),
            panne(60, "a"), clean(60, "b"), clean(60, "c"), clean(60, "d"),
        ]
        return pool, markers, readings

    def test_sum_m_equals_sum_of_r1_ecarts_exactly(self):
        pool, markers, readings = self._build()
        r1o = r1.compute_r1(markers, readings, pool, w=60, sigma=SIGMA_HUGE, tau=TAU)
        lmo = lm.compute_lm(markers, readings, pool, w=60, sigma=SIGMA_HUGE, tau=TAU)
        sum_ecart = sum(r1o["strates"]["calme"]["per_source"][f]["ecart"] for f in pool)
        self.assertEqual(lmo["strates"]["calme"]["sum_m"], sum_ecart)   # entier exact
        self.assertEqual(sum_ecart, 3)

    def test_e_theta_equals_mean_of_phats(self):
        pool, markers, readings = self._build()
        r1o = r1.compute_r1(markers, readings, pool, w=60, sigma=SIGMA_HUGE, tau=TAU)
        lmo = lm.compute_lm(markers, readings, pool, w=60, sigma=SIGMA_HUGE, tau=TAU)
        blk_r1 = r1o["strates"]["calme"]
        blk_lm = lmo["strates"]["calme"]
        with localcontext() as ctx:
            ctx.prec = PREC
            mean_phat = sum((blk_r1["per_source"][f]["phat"] for f in pool), D(0)) / D(len(pool))
        self.assertLess(abs(blk_lm["E_theta"] - mean_phat), D("1e-45"))
        self.assertEqual(blk_lm["E_theta"], D("0.375"))                  # 3/(2·4)

    def test_e_theta2_var_hand_values(self):
        pool, markers, readings = self._build()
        blk = lm.compute_lm(markers, readings, pool, w=60, sigma=SIGMA_HUGE, tau=TAU)["strates"]["calme"]
        with localcontext() as ctx:
            ctx.prec = PREC
            e_theta2_ref = D(1) / D(12)          # (1/6 + 0)/2
            var_ref = D(1) / D(12) - (D(3) / D(8)) ** 2   # 1/12 − 9/64 = −11/192
        self.assertLess(abs(blk["E_theta2"] - e_theta2_ref), D("1e-45"))
        self.assertLess(abs(blk["Var_theta"] - var_ref), D("1e-45"))
        self.assertLess(blk["Var_theta"], D(0))   # Var̂ < 0 admis en échantillon fini (§5.5)


class TestPhiSigned(unittest.TestCase):
    """phi signé par paire de flux — Cov<0 possible (L&M p.j.1601), publié."""

    def _phi_ab(self, wins_spec):
        # wins_spec : liste de (a_panne, b_panne) par fenêtre ; pool = [a,b].
        pool = ["a", "b"]
        markers, readings = [], []
        for i, (ap, bp) in enumerate(wins_spec):
            ws = i * 60
            markers.append(mk(ws))
            readings.append(panne(ws, "a") if ap else clean(ws, "a"))
            readings.append(panne(ws, "b") if bp else clean(ws, "b"))
        out = lm.compute_lm(markers, readings, pool, w=60, sigma=SIGMA_HUGE, tau=TAU)
        return out["strates"]["calme"]["pair_phi"]["a×b"]

    def test_perfect_co_failure_is_plus_one(self):
        cell = self._phi_ab([(1, 1), (1, 1), (0, 0), (0, 0)])
        self.assertEqual(cell["phi"], D(1))
        self.assertEqual(cell["signe"], "+")
        self.assertEqual((cell["n11"], cell["n00"], cell["n10"], cell["n01"]), (2, 2, 0, 0))

    def test_perfect_anti_correlation_is_minus_one(self):
        cell = self._phi_ab([(1, 0), (0, 1), (1, 0), (0, 1)])
        self.assertEqual(cell["phi"], D(-1))
        self.assertEqual(cell["signe"], "−")            # Cov<0 publié (§5.5)

    def test_constant_indicator_phi_none(self):
        # a en panne PARTOUT (indicatrice constante) → marge nulle → phi non défini.
        cell = self._phi_ab([(1, 1), (1, 0), (1, 1), (1, 0)])
        self.assertIsNone(cell["phi"])
        self.assertEqual(cell["signe"], "non_définie")


class TestPerStrate(unittest.TestCase):
    def test_m_series_cut_per_strate(self):
        # 2 fenêtres « calme », 2 « stress » ; écarts différents par strate.
        pool = ["a", "b", "c", "d"]
        markers = [mk(0, "calme"), mk(60, "calme"), mk(120, "stress"), mk(180, "stress")]
        readings = []
        for ws in (0, 60):                      # calme : a panne seul (m=1)
            readings += [panne(ws, "a"), clean(ws, "b"), clean(ws, "c"), clean(ws, "d")]
        for ws in (120, 180):                   # stress : a,b,c panne (m=3)
            readings += [panne(ws, "a"), panne(ws, "b"), panne(ws, "c"), clean(ws, "d")]
        out = lm.compute_lm(markers, readings, pool, w=60, sigma=SIGMA_HUGE, tau=TAU)
        calme, stress = out["strates"]["calme"], out["strates"]["stress"]
        self.assertEqual(calme["sum_m"], 2)     # 1+1
        self.assertEqual(stress["sum_m"], 6)    # 3+3
        with localcontext() as ctx:
            ctx.prec = PREC
            self.assertEqual(calme["E_theta"], +(D(2) / (D(2) * D(4))))   # 0.25
            self.assertEqual(stress["E_theta"], +(D(6) / (D(2) * D(4))))  # 0.75


class TestDegenerate(unittest.TestCase):
    def test_n_lt_2_pool_e_theta2_none(self):
        # Pool à 1 flux → N=1 → forme par paires N(N−1) inexistante → None (nommé).
        out = lm.compute_lm([mk(0)], [panne(0, "a")], ["a"], w=60, sigma=SIGMA_HUGE, tau=TAU)
        blk = out["strates"]["calme"]
        self.assertIsNone(blk["E_theta2"])
        self.assertIsNone(blk["Var_theta"])
        self.assertIsNotNone(blk["E_theta"])    # Ê(Θ) reste défini (N=1) : m/N = 1

    def test_renvois_m1c_present(self):
        out = lm.compute_lm([mk(0)], [panne(0, "a"), clean(0, "b")], ["a", "b"],
                            w=60, sigma=SIGMA_HUGE, tau=TAU)
        blk = out["strates"]["calme"]
        self.assertIn("CLUSTERS", blk["renvoi_m1c_clusters"])
        self.assertIn("flux→source", blk["renvoi_m1c_flux_source"])


if __name__ == "__main__":
    unittest.main()
