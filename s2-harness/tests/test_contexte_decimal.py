"""Étape B de la partie 2, B0 (G0-partie-2.md §B, ajout du 2026-10-02) : SHOGEN-DECIMAL-CONTEXTE-1 et -ARRONDI-2
(annexe B.21) ; contexte ambiant hostile : ROUND_DOWN, Emin −20, piège Inexact. Attendus : oracle en fractions sans
decimal (arrondi pair à 50 chiffres, une opération à la fois) ou à la main. Chaque test nomme son mutant."""

from __future__ import annotations

import contextlib
import unittest
from decimal import (ROUND_DOWN, ROUND_HALF_EVEN, Decimal as D, DivisionByZero, Inexact, InvalidOperation, Overflow,
                     localcontext)

from shogen_s2 import lm, r1, r2, report
from tests.test_arrondi import CAS
from tests.test_critere import deux, journal, regle
from tests.test_r1 import _sbc, _scof, _tbc, mk, rd
from tests.test_rendu_blocs import SAM

L51 = D("1." + "0" * 48 + "16")                 # 51 chiffres : arrondi pair 1,0…02 ; ROUND_DOWN 1,0…01
LN = {0: {"a": L51, "b": D(0), "c": D(0)}}
PM = {(60 * i, f): {"status": "ok", "price": p} for f, ps in (("a", "123"), ("b", "124")) for i, p in enumerate(ps)}
CL = {"clusters": [{"n_members_flux": 3, "flux": list(f), "hosts": [f]} for f in ("abc", "def")]}
LC = [rd(0, "a", "panne_http", None)] + [rd(ws, f) for ws in (0, 60) for f in "abcdef" if (ws, f) != (0, "a")]
X = {   # site (ligne à 34e096f) : (appel, attendu) ; « piège » : seul le piège Inexact rougit le mutant
    "lm pairwise_second_moment l.73": (lambda: lm.pairwise_second_moment(2, 4), D("0.1" + "6" * 48 + "7")),
    "r2 pearson l.434": (lambda: r2.pearson([D(0), D(1), D(2)], [D(0), D(0), D(3)])[0],
                         D("0.86602540378443864676372317075293618347140262690518")),   # 3/√12, deux arrondis
    "r2 log_returns l.491": (lambda: r2.log_returns([0, 60], {0: {"a": D(0)}, 60: {"a": L51}}, "a", 60)[60],
                             D("1." + "0" * 48 + "2")),
    "r2 rho_resid l.524": (lambda: r2.rho_resid([0], LN, "a", "b", 2, 1)["n"], 1),                    # piège
    "r2 _quantize l.548": (lambda: r2._quantize(D("1.015"), "0.01"), D("1.02")),
    "r2 tick_identity l.584": (lambda: r2.tick_identity([0, 60, 120], PM, "a", "b", 60, 1, "exact", 1)["T"],
                               D("0." + "6" * 49 + "7")),                                              # 2/3
    "r2 _aberrance_by_window l.604": (lambda: r2._aberrance_by_window([0], LN, list("abc"), D(5)), {}),  # piège
    "r2 coaberrance_kz l.645": (lambda: r2.coaberrance_kz({0: {"a": 1, "b": 1}, 60: {"a": 1, "b": 1},
                                                           120: {"a": 0, "b": 0}}, "a", "b")["p_co"],
                                D("0." + "4" * 49 + "5")),                                       # (2/3 arrondi)²
    "r2 _jumps l.668": (lambda: r2._jumps([0, 60, 120, 180], {t: {"a": D(int(t == 180))} for t in (0, 60, 120, 180)},
                                          "a", 60, D(1)), {60: 0, 120: 0, 180: 1}),                    # piège
    "r2 cluster_lm_correlations l.937": (lambda: r2.cluster_lm_correlations(
        CL, [mk(0), mk(60)], LC, list("abcdef"), 60, _sbc(None), _scof("abcdef"), _tbc(D("0.005")), 4)[
        "cluster_pairs"]["[abc]×[def]"]["rho"], None),                                                  # piège
}


@contextlib.contextmanager
def hostile():
    with localcontext() as amb:
        amb.rounding, amb.Emin, amb.traps[Inexact] = ROUND_DOWN, -20, True
        yield


class TestContexteDecimalNomme(unittest.TestCase):
    def test_contexte_nomme_complet(self):
        """DefaultContext de la bibliothèque standard (_pydecimal.py), précision DECIMAL_PREC. Rougit si : un attribut
        change (prec, rounding, Emin, Emax, capitals, clamp, traps) ou un drapeau est levé."""
        k = r1.CONTEXTE_DECIMAL
        self.assertEqual((k.prec, k.rounding, k.Emin, k.Emax, k.capitals, k.clamp),
                         (50, ROUND_HALF_EVEN, -999999, 999999, 1, 0))
        self.assertEqual({s for s, v in k.traps.items() if v}, {InvalidOperation, DivisionByZero, Overflow})
        self.assertFalse(any(k.flags.values()))

    def test_sites_sous_contexte_hostile(self):
        """13 sites de r1 (CAS de test_arrondi), 10 de lm et r2 non exercés sur J2 (X), médiane de 1E-75 et 3E-75 (0E-69
        sous Emin −20). Rougit si : un de ces localcontext reprend le contexte appelant (Inexact, arrondi, Emin)."""
        cas = {**{f"r1 {k}": (f, D(v) if isinstance(v, str) else v) for k, (f, v) in CAS.items()}, **X,
               "r1 _median, Emin": (lambda: r1._median([D("1E-75"), D("3E-75")]), D("2E-75"))}
        for site, (appel, att) in cas.items():
            with self.subTest(site=site):
                self.assertEqual(appel(), att)
                with hostile():
                    obtenu = appel()
                self.assertEqual((obtenu, str(obtenu)), (att, str(att)))

    def test_rendu_j2_et_regle_sous_contexte_hostile(self):
        """Rendu de J2 (sans option, puis plage des 100 dernières fenêtres stress : écart de z inexact) et règle :
        hostile = défaut. Rougit si : un localcontext de lm, de r1, de r2 (ln) ou de report revient à l'appelant."""
        c, j = journal(200, 200, deux(50, 37))
        tout = (lambda: [report.render_report(c, j), regle(c, j),
                         report.render_report(c, j, exclude_ranges=[(SAM + 6000, SAM + 11940)])])
        defaut = tout()
        with hostile():
            self.assertEqual(tout(), defaut)
        self.assertIn("\n  stress   écart de z = ", defaut[2])


if __name__ == "__main__":
    unittest.main()
