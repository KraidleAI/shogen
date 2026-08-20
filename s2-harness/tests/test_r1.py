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

RÉVISION TRACÉE ADR-0021 [C2b] (constantes ci-dessous + adaptateurs) : le contrat
verrouillé jusqu'ici était **σ SCALAIRE** + **τ ABSOLU** (`SIGMA=1e12`, `TAU=50 $`).
ADR-0021 rend le harnais fidèle à ADR-0020 : **σ PAR CLASSE** (classify reçoit le
flux et dispatche σ selon sa classe) et **τ RELATIF** (`|prix − médiane_LOO| /
médiane_LOO > τ`, τ FRACTION). Les tests de propriété historiques (précédence,
garde §5.4, identité élémentaire, harnais-down…) sont ORTHOGONAUX à la
représentation σ/τ : ils sont conservés à l'identique via les adaptateurs `classify`
/ `R1` (qui rangent les flux synthétiques dans une classe de test unique et
exercent le VRAI `classify_ecart`/`compute_r1`). Le nouveau contrat (τ relatif,
garde médiane>0, σ par classe) est verrouillé EXPLICITEMENT par `TestTauRelatif`
et `TestSigmaParClasse` — pas un affaiblissement silencieux.
"""

from __future__ import annotations

import unittest
from decimal import Decimal, localcontext

from shogen_s2 import r1
from shogen_s2.r1 import Ecart
from shogen_s2.sources import SIGMA_FLOORS_ADR0020_SECONDS

# [C2b] Étaient `SIGMA = Decimal("1e12")` (σ scalaire) et `TAU = Decimal("50")` (τ
# ABSOLU en $). Désormais : SIGMA_HUGE = un plancher de classe énorme (jamais de
# staleness) ; TAU = FRACTION relative 0,5 % (ADR-0020 déc. 2).
SIGMA_HUGE = Decimal("1e12")   # plancher de classe énorme → jamais de staleness
TAU = Decimal("0.005")         # τ RELATIF (fraction 0,5 %) — était Decimal("50") ABSOLU
D = Decimal
TCLASS = "place_horodatee"     # classe de test unique (horodatée, σ évaluable)


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


# ── Adaptateurs [C2b] : σ PAR CLASSE via une classe de test unique ────────────
def _sbc(sigma):
    """sigma_by_class à classe unique TCLASS ; `sigma=None` → classe « non
    évaluable » (staleness sautée, comme `sans_horodatage`)."""
    return {TCLASS: (None if sigma is None else Decimal(str(sigma)))}


def _scof(pool):
    """sigma_class_of_flux : tous les flux (synthétiques) rangés dans TCLASS."""
    return {f: TCLASS for f in pool}


def classify(reading, others, n_resp, win_end, sigma, tau=TAU, n_min=4, flux="a"):
    """Adaptateur : exerce le VRAI `r1.classify_ecart` (σ PAR CLASSE + τ RELATIF)
    en rangeant `flux` dans une classe unique de σ scalaire — conserve l'intention
    des tests de précédence historiques sous le nouveau contrat."""
    return r1.classify_ecart(reading, others, n_resp, win_end, flux,
                             _sbc(sigma), {flux: TCLASS}, tau, n_min)


def R1(markers, readings, pool, *, sigma, tau=TAU, w=60, n_min=4):
    """Adaptateur `compute_r1` : pool dans une classe unique (σ scalaire par classe)."""
    return r1.compute_r1(markers, readings, pool, w, _sbc(sigma), _scof(pool), tau,
                         n_min=n_min)


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


class TestBinomialTail(unittest.TestCase):
    """Queue binomiale exacte P(K ≥ K_obs | Bin(n, P̂_more)) — §5.4 (sous la garde)."""

    def test_k_ge_one_three_trials_hand_value(self):
        # P(K≥1 | Bin(3, 1/9)) = 1 − (8/9)³ = 1 − 512/729 = 217/729 (exact).
        # p ET ref construits à prec FIXÉE (comme P̂_more via poisson_binomial) :
        # la précision de la queue est bornée par celle de son entrée p_more.
        with localcontext() as ctx:
            ctx.prec = r1.DECIMAL_PREC
            p = D(1) / D(9)
            ref = D(217) / D(729)
        got = r1.binomial_tail_ge(1, 3, p)
        self.assertLess(abs(got - ref), D("1e-45"))

    def test_k_ge_zero_is_one(self):
        # P(K ≥ 0) = 1 quelle que soit la loi (toutes les fenêtres).
        self.assertEqual(r1.binomial_tail_ge(0, 100, D("0.3")), D(1))

    def test_k_gt_n_is_zero(self):
        # P(K ≥ k) = 0 pour k > n (aucune réalisation possible).
        self.assertEqual(r1.binomial_tail_ge(5, 3, D("0.3")), D(0))

    def test_full_support_sums_to_one(self):
        # P(K ≥ 0) − P(K ≥ n+1) = 1 ; et P(K≥1)+P(K=0) = 1 par construction.
        n, p = 7, D("0.25")
        with localcontext() as ctx:
            ctx.prec = r1.DECIMAL_PREC
            pmf0 = (D(1) - p) ** n                       # P(K = 0)
        self.assertLess(abs(r1.binomial_tail_ge(1, n, p) - (D(1) - pmf0)), D("1e-45"))

    def test_symmetric_p_half_median(self):
        # Bin(4, 0.5) : P(K≥2) = 1 − P(0) − P(1) = 1 − 1/16 − 4/16 = 11/16.
        got = r1.binomial_tail_ge(2, 4, D("0.5"))
        self.assertEqual(got, D("0.6875"))              # 11/16 exact à prec fixée

    def test_recurrence_matches_bruteforce_comb(self):
        # La récurrence O(n) doit égaler la somme brute C(n,x)p^x q^(n−x) (prec fixée).
        import math
        n, p = 40, D("0.05")
        with localcontext() as ctx:
            ctx.prec = r1.DECIMAL_PREC
            q = D(1) - p
            brute = sum((D(math.comb(n, x)) * (p ** x) * (q ** (n - x))
                         for x in range(3, n + 1)), D(0))
        self.assertLess(abs(r1.binomial_tail_ge(3, n, p) - brute), D("1e-45"))


class TestQueueUnderGuard(unittest.TestCase):
    """Intégration : sous la garde, compute_r1 publie la queue exacte (non dégénérée)
    ou « historique insuffisant » nu (dégénéré P̂_more ∈ {0,1})."""

    def test_queue_published_when_pmore_strict_interior(self):
        # 3 fenêtres, a & b en panne dans 1 seule → P_more ∈ (0,1), garde franchie.
        pool = ["a", "b", "c"]
        markers, readings = [], []
        for i, ws in enumerate((0, 60, 120)):
            markers.append(mk(ws))
            if i == 0:
                readings += [rd(ws, "a", status="panne_http", price=None),
                             rd(ws, "b", status="panne_http", price=None),
                             rd(ws, "c", price="64000", source_ts=D(ws + 59))]
            else:
                readings += [rd(ws, "a", price="64000", source_ts=D(ws + 59)),
                             rd(ws, "b", price="64000", source_ts=D(ws + 59)),
                             rd(ws, "c", price="64000", source_ts=D(ws + 59))]
        blk = R1(markers, readings, pool, sigma=D("30"))["strates"]["calme"]
        self.assertTrue(blk["flag_historique_insuffisant"])   # garde levée (n petit)
        self.assertTrue(blk["queue_exacte_applicable"])       # 0 < P_more < 1 → queue publiée
        self.assertIsNotNone(blk["queue_binomiale_P_K_ge_Kobs"])
        self.assertGreater(blk["queue_binomiale_P_K_ge_Kobs"], D(0))
        self.assertLessEqual(blk["queue_binomiale_P_K_ge_Kobs"], D(1))

    def test_bare_insufficient_when_pmore_degenerate(self):
        # a & b en panne PARTOUT → P_more = 1 (dégénéré) → pas de queue, message nu.
        pool = ["a", "b", "c"]
        markers, readings = [], []
        for ws in (0, 60, 120):
            markers.append(mk(ws))
            readings += [rd(ws, "a", status="panne_http", price=None),
                         rd(ws, "b", status="panne_http", price=None),
                         rd(ws, "c", price="64000", source_ts=D(ws + 59))]
        blk = R1(markers, readings, pool, sigma=D("30"))["strates"]["calme"]
        self.assertEqual(blk["P_more"], D(1))
        self.assertTrue(blk["flag_historique_insuffisant"])
        self.assertFalse(blk["queue_exacte_applicable"])      # dégénéré → pas de queue
        self.assertIsNone(blk["queue_binomiale_P_K_ge_Kobs"])
        self.assertIn("dégénérée", blk["queue_note"])

    def _build_cofailure(self, n_windows, n_cofail):
        # pool [a,b] ; a&b en panne ensemble dans `n_cofail` fenêtres, propres après.
        # p̂_a=p̂_b=n_cofail/n_windows ; K=n_cofail (chaque co-panne = 2 écarts).
        pool = ["a", "b"]
        markers, readings = [], []
        for i in range(n_windows):
            ws = i * 60
            markers.append(mk(ws))
            if i < n_cofail:
                readings += [rd(ws, "a", status="panne_http", price=None),
                             rd(ws, "b", status="panne_http", price=None)]
            else:
                readings += [rd(ws, "a", price="64000", source_ts=D(ws + 1)),
                             rd(ws, "b", price="64000", source_ts=D(ws + 1))]
        return pool, markers, readings

    def test_boundary_below_guard_publishes_queue(self):
        # n=52, 26 co-pannes → p̂=0.5, P_more=0.25, garde=52·0.1875=9.75 < 10 → sous
        # la garde : z NON publié, QUEUE EXACTE publiée (frontière §5.4).
        pool, markers, readings = self._build_cofailure(52, 26)
        blk = R1(markers, readings, pool, sigma=SIGMA_HUGE)["strates"]["calme"]
        self.assertEqual(blk["P_more"], D("0.25"))
        self.assertEqual(blk["gate_value"], D("9.7500"))
        self.assertTrue(blk["flag_historique_insuffisant"])
        self.assertIsNone(blk["z"])
        self.assertTrue(blk["queue_exacte_applicable"])
        q = blk["queue_binomiale_P_K_ge_Kobs"]
        self.assertIsNotNone(q)
        self.assertGreater(q, D(0))
        self.assertLessEqual(q, D(1))

    def test_boundary_above_guard_publishes_z_not_queue(self):
        # n=54, 27 co-pannes → p̂=0.5, P_more=0.25, garde=54·0.1875=10.125 ≥ 10 →
        # au-dessus : z publié, queue non applicable. (Frontière juste franchie.)
        pool, markers, readings = self._build_cofailure(54, 27)
        blk = R1(markers, readings, pool, sigma=SIGMA_HUGE)["strates"]["calme"]
        self.assertEqual(blk["P_more"], D("0.25"))
        self.assertEqual(blk["gate_value"], D("10.1250"))
        self.assertFalse(blk["flag_historique_insuffisant"])
        self.assertIsNotNone(blk["z"])
        self.assertFalse(blk["queue_exacte_applicable"])
        self.assertIsNone(blk["queue_binomiale_P_K_ge_Kobs"])

    def test_no_queue_when_z_published(self):
        # Historique suffisant (garde ≥ 10) : z publié, queue non applicable.
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
        blk = R1(markers, readings, pool, sigma=SIGMA_HUGE)["strates"]["calme"]
        self.assertFalse(blk["flag_historique_insuffisant"])
        self.assertIsNotNone(blk["z"])
        self.assertFalse(blk["queue_exacte_applicable"])
        self.assertIsNone(blk["queue_binomiale_P_K_ge_Kobs"])


class TestClassifyPrecedence(unittest.TestCase):
    def test_panne_beats_staleness_and_horsenv(self):
        # Panne : pas de valeur → écart (iii), précédence maximale, même si les
        # conditions de staleness et hors-enveloppe seraient réunies.
        reading = rd(0, "a", status="panne_transport", price=None, source_ts=None)
        kind = classify(reading, [D("1"), D("2"), D("3")], 5, 10 ** 9, sigma=D("60"))
        self.assertIs(kind, Ecart.PANNE)

    def test_staleness_beats_horsenv(self):
        # OK mais horodatage porté vieux (win_end − src = 1000 > σ=60) → (ii),
        # même si le prix serait hors-enveloppe.
        reading = rd(0, "a", price="999999", source_ts=D("0"))
        kind = classify(reading, [D("100"), D("101"), D("102")], 5, 1000, sigma=D("60"))
        self.assertIs(kind, Ecart.STALENESS)

    def test_horsenv_requires_four_responding(self):
        reading = rd(0, "a", price="999999", source_ts=D("999"))  # récent → pas stale
        others = [D("100"), D("101"), D("102")]
        # N=3 répondantes → enveloppe non définie → non évaluable (jamais « pas d'écart »).
        self.assertIs(
            classify(reading, others[:2], 3, 1000, sigma=SIGMA_HUGE),
            Ecart.NON_EVAL_HORSENV,
        )
        # N=4 répondantes, prix loin de la médiane → hors-enveloppe (i).
        self.assertIs(
            classify(reading, others, 4, 1000, sigma=SIGMA_HUGE),
            Ecart.HORS_ENVELOPPE,
        )

    def test_horsenv_inside_envelope_is_pas_ecart(self):
        reading = rd(0, "a", price="101", source_ts=D("999"))
        kind = classify(reading, [D("100"), D("101"), D("102")], 4, 1000, sigma=SIGMA_HUGE)
        self.assertIs(kind, Ecart.PAS_ECART)

    def test_staleness_nonevaluable_without_source_ts(self):
        # source_ts absent (ex. kraken) → staleness non évaluable : on passe à (i).
        reading = rd(0, "a", price="101", source_ts=None)
        # N<4 → non évaluable hors-env (et pas de staleness) :
        self.assertIs(
            classify(reading, [D("100")], 3, 10, sigma=D("1")),
            Ecart.NON_EVAL_HORSENV,
        )
        # N≥4, prix dans l'enveloppe → pas d'écart (staleness sautée proprement) :
        self.assertIs(
            classify(reading, [D("100"), D("101"), D("102")], 4, 10, sigma=D("1")),
            Ecart.PAS_ECART,
        )


class TestTauRelatif(unittest.TestCase):
    """[C2a] Contrat NEUF τ RELATIF : `|prix − médiane_LOO| / médiane_LOO > τ`.
    Le critère est la DIVISION par la médiane (l'`abs()` reste au NUMÉRATEUR) ;
    garde `médiane_LOO > 0` fail-closed."""

    def test_threshold_divides_by_median(self):
        # médiane_LOO = 100 ; prix 101 → écart relatif = 1/100 = 0.01.
        r = rd(0, "a", price="101", source_ts=None)
        self.assertIs(classify(r, [D(100)] * 4, 5, 10, sigma=None, tau=D("0.005")),
                      Ecart.HORS_ENVELOPPE)                 # 0.01 > 0.005
        self.assertIs(classify(r, [D(100)] * 4, 5, 10, sigma=None, tau=D("0.02")),
                      Ecart.PAS_ECART)                       # 0.01 < 0.02
        # frontière EXACTE : 0.01 n'est PAS > 0.01 → pas_ecart (comparaison stricte).
        self.assertIs(classify(r, [D(100)] * 4, 5, 10, sigma=None, tau=D("0.01")),
                      Ecart.PAS_ECART)

    def test_abs_stays_in_numerator_below_median_fires(self):
        # prix SOUS la médiane : |99 − 100|/100 = 0.01 > 0.005 → hors-enveloppe.
        r = rd(0, "a", price="99", source_ts=None)
        self.assertIs(classify(r, [D(100)] * 4, 5, 10, sigma=None, tau=D("0.005")),
                      Ecart.HORS_ENVELOPPE)

    def test_is_relative_not_absolute_scale_invariance(self):
        # PREUVE que le critère est RELATIF (pas la forme absolue nue) :
        #  (a) grand prix, grand écart ABSOLU mais petit RELATIF → PAS hors-env
        #      (|dev|=1e6 franchirait un τ absolu de 50 ; rel=1e6/1e9=1e-3 < 0.005).
        big = rd(0, "a", price=str(Decimal("1000000000") + Decimal("1000000")),
                 source_ts=None)
        self.assertIs(classify(big, [D("1000000000")] * 4, 5, 10, sigma=None,
                               tau=D("0.005")), Ecart.PAS_ECART)
        #  (b) petit prix, petit écart absolu mais grand RELATIF → hors-env
        #      (|dev|=0.1 NE franchirait PAS un τ absolu de 50 ; rel=0.1/10=0.01>0.005).
        small = rd(0, "a", price="10.1", source_ts=None)
        self.assertIs(classify(small, [D("10")] * 4, 5, 10, sigma=None,
                               tau=D("0.005")), Ecart.HORS_ENVELOPPE)

    def test_median_zero_guard_is_non_evaluable(self):
        # médiane_LOO = 0 → écart relatif indéfini → NON ÉVALUABLE (garde [C2a]),
        # jamais « pas d'écart », jamais une division par zéro.
        r = rd(0, "a", price="101", source_ts=None)
        self.assertIs(classify(r, [D(0)] * 4, 5, 10, sigma=None, tau=D("0.005")),
                      Ecart.NON_EVAL_HORSENV)

    def test_median_negative_guard_is_non_evaluable(self):
        # médiane_LOO < 0 (prix dégénéré) → non évaluable (garde `m_loo <= 0`).
        r = rd(0, "a", price="101", source_ts=None)
        self.assertIs(classify(r, [D(-100)] * 4, 5, 10, sigma=None, tau=D("0.005")),
                      Ecart.NON_EVAL_HORSENV)


class TestSigmaParClasse(unittest.TestCase):
    """Contrat NEUF σ PAR CLASSE : classify reçoit le flux et dispatche σ selon sa
    CLASSE (mapping classe→plancher), jamais un scalaire unique."""

    def test_same_staleness_different_class_verdict(self):
        # staleness = win_end − src = 1000 − 900 = 100 s. place_horodatee (30 s) →
        # stale ; agregateur (300 s) → pas stale. MÊME cellule, verdict PAR CLASSE.
        sbc = {"place_horodatee": D(30), "agregateur": D(300)}
        scof = {"p": "place_horodatee", "a": "agregateur"}
        r = rd(0, "p", price="100", source_ts=D(900))
        self.assertIs(
            r1.classify_ecart(r, [D(100)] * 4, 5, 1000, "p", sbc, scof, TAU),
            Ecart.STALENESS)
        r2 = rd(0, "a", price="100", source_ts=D(900))
        self.assertIs(
            r1.classify_ecart(r2, [D(100)] * 4, 5, 1000, "a", sbc, scof, TAU),
            Ecart.PAS_ECART)

    def test_none_floor_class_skips_staleness(self):
        # Classe à plancher None (ex. sans_horodatage, ou oracle_chainlink non
        # confirmé) → staleness NON évaluable même avec un horodatage porté ancien.
        sbc = {"sans": None}
        scof = {"k": "sans"}
        r = rd(0, "k", price="100", source_ts=D(0))       # très ancien
        self.assertIs(
            r1.classify_ecart(r, [D(100)] * 4, 5, 10 ** 9, "k", sbc, scof, TAU),
            Ecart.PAS_ECART)                               # pas STALENESS

    def test_real_adr0020_floors_dispatch(self):
        # Dispatch sur les VRAIS planchers ADR-0020 (sources) : staleness = 40 s.
        # place_horodatee(30)→stale ; oracle_pyth(30)→stale ; agregateur(300)→non ;
        # oracle_chainlink(5400)→non ; sans_horodatage(None)→non évaluable.
        floors = SIGMA_FLOORS_ADR0020_SECONDS
        sbc = {k: (None if v is None else Decimal(v)) for k, v in floors.items()}
        cases = {
            "place_horodatee": Ecart.STALENESS,
            "oracle_pyth": Ecart.STALENESS,
            "agregateur": Ecart.PAS_ECART,
            "oracle_chainlink": Ecart.PAS_ECART,
            "sans_horodatage": Ecart.PAS_ECART,     # plancher None → staleness sautée
        }
        for klass, expected in cases.items():
            r = rd(0, "f", price="100", source_ts=D(960))   # win_end 1000 → stale 40 s
            got = r1.classify_ecart(r, [D(100)] * 4, 5, 1000, "f", sbc,
                                    {"f": klass}, TAU)
            self.assertIs(got, expected, f"classe {klass}")

    def test_unknown_flux_staleness_non_evaluable(self):
        # Flux absent du dispatch → classe None → staleness non évaluable (fail-open
        # documenté ; le pipeline réel fail-close la couverture au WRITE, collector).
        sbc = {"place_horodatee": D(30)}
        r = rd(0, "z", price="100", source_ts=D(0))
        self.assertIs(
            r1.classify_ecart(r, [D(100)] * 4, 5, 10 ** 9, "z", sbc, {}, TAU),
            Ecart.PAS_ECART)


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
        out = R1(markers, readings, pool, sigma=SIGMA_HUGE)
        blk = out["strates"]["calme"]
        self.assertEqual(blk["n"], 2)                # 220 (orphelin) et 280 (absent) exclus
        for f in pool:
            # Aucune panne fabriquée pour les fenêtres non complétées.
            self.assertEqual(blk["per_source"][f]["panne"], 0)
            self.assertEqual(blk["per_source"][f]["ecart"], 0)
            self.assertEqual(blk["per_source"][f]["phat"], D(0))

    def test_no_markers_is_degenerate_flag(self):
        out = R1([], [rd(100, "a")], ["a"], sigma=SIGMA_HUGE)
        self.assertIn("aucune fenêtre complétée", out["note"])
        self.assertTrue(out["flag_historique_insuffisant"])


class TestComputeR1LastWins(unittest.TestCase):
    def test_marker_dedup_counts_window_once(self):
        self.assertEqual(r1.build_window_strate([mk(100), mk(100)]), {100: "calme"})

    def test_reading_last_wins(self):
        m = r1.build_reading_map([rd(100, "a", price="100"), rd(100, "a", price="200")])
        self.assertEqual(m[(100, "a")]["price"], "200")

    def test_duplicate_window_counted_once_end_to_end(self):
        out = R1([mk(100), mk(100)], [rd(100, "a")], ["a"], sigma=SIGMA_HUGE)
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
        out = R1([mk(0)], readings, pool, sigma=SIGMA_HUGE)
        ps = out["strates"]["calme"]["per_source"]
        for f in ("a", "b", "c"):
            self.assertEqual(ps[f]["non_eval_hors_env"], 1)
            self.assertEqual(ps[f]["ecart"], 0)
        for f in ("d", "e"):
            self.assertEqual(ps[f]["panne"], 1)

    def test_five_responding_horsenv_fires(self):
        pool = ["a", "b", "c", "d", "e"]
        # 4 sources à 100, une à 999999 → médiane_LOO de « e » = 100, rel ≫ τ.
        readings = [rd(0, f, price=p, source_ts=D("999999999"))
                    for f, p in zip(pool, ["100", "100", "100", "100", "999999"])]
        out = R1([mk(0)], readings, pool, sigma=SIGMA_HUGE)
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
        out = R1(markers, readings, pool, sigma=D("30"))
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
        out = R1(markers, readings, pool, sigma=SIGMA_HUGE)
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
