"""SHOGEN-CONTENU-DEP-1 : variance par blocs de ρ̂ par sa fonction d'influence ; valeurs à la main (journal G1) ;
intégration : ρ̂ recalculés égaux à r2.rho_raw et r2.rho_resid (code tiers du module). Chaque test nomme la mutation
qui le rougit."""
import tempfile
import unittest
from decimal import Context, Decimal

import commun
import contenu
from shogen_s2 import r2
from tests import fixtures as fx


class TestContenu(unittest.TestCase):
    def test_influence_de_pearson_a_la_main(self):
        """x = (1, 2, 3, 4), y = (1, 3, 2, 4) : ρ = 4/5 ; IF = (0.36, −0.36, −0.36, 0.36) ; Var̂_0 = Σ IF²/N² = 0.0324 ;
        ℓ = 2 : Σ B² = 0.7776, Var̂_bloc = 0.7776/(2·16) = 0.0243 ; N_eff = 3 + 0.36²/0.0243 = 25/3, N_eff,0 = 7 ;
        SE de Fisher (1 − ρ²)/√(N − 3) = 0.36. Rougit si : facteur ρ/2 oublié ; division par N au lieu de N² ;
        blocs de bord omis ; 1 − ρ au lieu de 1 − ρ²."""
        serie = [(60 * t, Decimal(x), Decimal(y)) for t, (x, y) in enumerate(((1, 1), (2, 3), (3, 2), (4, 4)))]
        r = contenu.dependance(serie, 60, 2)
        self.assertEqual((r["N"], r["rho"], r["var0"], r["varbloc"], r["se_fisher"], r["neff0"]),
                         (4, Decimal("0.8"), Decimal("0.0324"), Decimal("0.0243"), Decimal("0.36"), Decimal(7)))
        self.assertLess(abs(r["neff"] - Context(prec=60).divide(25, 3)), Decimal("1e-45"))

    def test_rho_egaux_a_r2(self):
        """320 fenêtres, prix déterministes non constants : pour chaque paire, ρ_raw et ρ_resid du module égaux à ceux
        de r2.rho_raw et r2.rho_resid. Rougit si la série de résidus n'est pas leave-two-out ou si les rendements
        enjambent un trou."""
        d = tempfile.mkdtemp(prefix="pp_contenu_")
        ws = [fx.VEN + 60 * i for i in range(330) if i != 100]
        prix = lambda i, k: f"{60000 + (i * 7919) % 1000 - 500 + (i * (k + 3) * 104729) % 21 - 10}.{(i * k) % 100:02d}"
        pool = list("abcdefg")                    # sept flux : au moins quatre autres répondantes pour ρ_resid
        fx.journaux(d, ws, lambda i, f: ("ok", None, prix((ws[i] - fx.VEN) // 60, pool.index(f))), pool=pool)
        dd = commun.charger(d, {"t0": ws[0], "n_fixe": len(ws)}, [(0, 0)])
        res = contenu.analyse(dd, 300)
        wins, rmap = r2.price_map(dd["readings"], dd["markers"])
        lnp = r2.lnprice_by_window(wins, rmap)
        self.assertEqual(len(res["paires"]), 21)
        for (a, b), x in res["paires"].items():
            self.assertIsNotNone(x["resid"]["rho"])
            self.assertEqual((x["raw"]["rho"], x["resid"]["rho"]), (r2.rho_raw(wins, lnp, a, b, 60, 300)["rho"],
                                                                    r2.rho_resid(wins, lnp, a, b, 300)["rho"]))


if __name__ == "__main__":
    unittest.main()
