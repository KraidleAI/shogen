"""SHOGEN-SIGMA-BLOC-INDEP-1 : variance par blocs et classification indépendantes de r1. Références : valeur à la main
(variance) ; r1 lui-même, code tiers du module testé (classification cellule par cellule, σ̂²_bloc chaîne pour
chaîne). Chaque test nomme la mutation qui le rougit."""
import tempfile
import unittest
from decimal import Decimal

import commun
import sigma_indep
from tests import fixtures as fx

WS = [fx.VEN + 60 * i for i in range(40)]


class TestSigmaIndep(unittest.TestCase):
    def test_variance_a_la_main(self):
        """Grille 0, 1, 2, 4 (3 absente), I = 1, 1, 0, 1, ℓ = 2 : c = 4·I − 3 = (1, 1, −3, ·, 1) ; blocs (série complétée
        par des 0) 1, 2, −2, −3, 1, 1 ; Σ B² = 20 ; σ̂² = 20/(2·16) = 0.625 (= γ̂₀ + γ̂₁ = 0.75 − 0.125). Rougit si : blocs
        de bord omis ; position absente qui forme une paire ; division par ℓ·n oubliée."""
        v = sigma_indep.variance([(0, 1), (60, 1), (120, 0), (240, 1)], 60, 2)
        self.assertEqual((v["n"], v["K"], v["gamma0"], v["sigma2"]), (4, 3, Decimal("0.75"), Decimal("0.625")))

    def test_classification_et_sigma_egaux_a_r1(self):
        """Fixture à toutes les branches : panne, prix nul, staleness (σ = 30 s) et son égalité (âge = σ : pas stale),
        hors-enveloppe (200 contre 100) et son égalité (150 : écart = τ·m, pas hors-enveloppe), médiane leave-one-out à
        quatre répondantes (a et d à 200, e absente : d hors-enveloppe, pas avec sa propre lecture), moins de 4
        répondantes (d à 200 avec la seule e : non évaluable), médiane nulle (prix 0), classe sans τ. Rougit si : prix
        nul non compté en panne ; « ≥ » au lieu de « > » (staleness ou enveloppe) ; médiane qui inclut le flux ; n_min
        ignoré."""
        prix = {(9, "d"): "200", (20, "d"): "200", (22, "a"): "200", (22, "d"): "200", (25, "d"): "150"}

        def motif(i, f):
            if (i < 4 and f in "ab") or (8 <= i < 12 and f in "abc"):
                return "panne_transport"
            if f == "c" and i in (5, 6, 7):
                return "nul" if i == 5 else ("ok", WS[i] - 100.0 if i == 6 else WS[i] + 30.0)
            if i == 22 and f == "e":
                return None
            return ("ok", None, "0" if i == 30 else prix.get((i, f), "100"))
        d = tempfile.mkdtemp(prefix="pp_sigma_")
        fx.journaux(d, WS, motif, sigma_classe={"place": "1000000000", "lent": "30"},
                    sigma_class_of_flux={**{f: "place" for f in "abd"}, "c": "lent", "e": "sans"},
                    tau_classe={"place": "0.5", "lent": "0.5"})
        dd = commun.charger(d, {"t0": WS[0], "n_fixe": 40}, [(0, 0)])
        r = sigma_indep.recalcul(dd)
        b = dd["base"]["strates"]["calme"]
        self.assertEqual(r["desaccords"], {"calme": 0})
        self.assertEqual((r["strates"]["calme"]["K"], r["strates"]["calme"]["sigma2"]), (b["K"], b["bloc"]["sigma2_bloc"]))
        self.assertEqual(r["ecarts"]["calme"], {f: b["per_source"][f]["ecart"] for f in fx.POOL})
        self.assertEqual([r["ecarts"]["calme"][f] for f in "acd"], [9, 6, 2])    # comptés à la main (journal G1)


if __name__ == "__main__":
    unittest.main()
