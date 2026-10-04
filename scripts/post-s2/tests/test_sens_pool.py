"""SHOGEN-FLUX-QUASI-MORT-1 (avec QUASI-MORT-PREDICAT-1 et POOL-MIN-1) et SHOGEN-FLUX-DEVIANT-1 : retraits par strate
attendus à la main (comptes des fixtures) ; règle recalculée comparée à r1.compute_r1 puis r1.regle_critere sur le pool
privé des flux retirés (attendu métamorphique, jamais lu dans une sortie du code testé). Chaque test nomme la mutation
qui le rougit."""
import tempfile
import unittest

import commun
import sens_pool
from shogen_s2 import r1
from tests import fixtures as fx

WS = [fx.VEN + 60 * i for i in range(100)]          # 100 fenêtres calmes (vendredi)
SEG = {"t0": WS[0], "n_fixe": 100}


def reference(d, pools):
    r = commun.calculer(d, [x for x in d["markers"] if x["strate"] in pools], pools)
    return r, r1.regle_critere(r)


class TestSensPool(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp(prefix="pp_sens_")

    def test_quasi_mort_49_50_51_prix_nul_flux_sans_ligne(self):
        """ok(c) = 49 (la lecture ok sans prix ne compte pas), ok(d) = 50 (égalité : reste), ok(e) = 51, f sans ligne
        (D1) : pool calme a, b, d, e ; K = 49 (d et e en panne ensemble pour i ≥ 51). Rougit si : « ≤ » au lieu de « < »
        (d retiré) ; statut seul (ok(c) = 50, c reste) ; garde POOL-MIN à « ≤ 4 » (refus à tort) ; règle non
        recalculée sur le pool réduit."""
        def motif(i, f):
            return {"a": "ok", "b": "ok", "f": None, "c": "ok" if i < 49 else "nul" if i == 49 else "panne_transport",
                    "d": "ok" if i < 50 else "panne_transport", "e": "ok" if i < 51 else "panne_transport"}[f]
        fx.journaux(self.d, WS, motif, pool=list("abcdef"))
        d = commun.charger(self.d, SEG, [(0, 0)])
        s = sens_pool.sensibilite(d, sens_pool.QUASI_MORT)
        self.assertEqual(s["ok"]["calme"], {"a": 100, "b": 100, "c": 49, "d": 50, "e": 51, "f": 0})
        self.assertEqual((s["pools"], s["egalites"], s["refus"]), ({"calme": ["a", "b", "d", "e"]}, [("calme", "d")], []))
        self.assertEqual((s["r1"], s["regle"]), reference(d, {"calme": ["a", "b", "d", "e"]}))
        self.assertEqual(s["r1"]["strates"]["calme"]["K"], 49)

    def test_critere_par_strate_contre_n_s(self):
        """Correction G2 C-1 (avis §1 pt 5 : critère par strate ; forme « segment » écartée, §3 V4) : 100 fenêtres
        calmes, 20 de stress, e en panne dans 5 des 20 de stress : ok(e, stress) = 15, 2·15 ≥ 20 : aucun retrait,
        aucun refus (à la main). Rougit si le critère est comparé au n du segment (120 : 2·20 < 120, les cinq flux
        quittent le pool de stress, strate refusée)."""
        ws = WS + [fx.VEN + 86400 + 60 * i for i in range(20)]
        fx.journaux(self.d, ws, lambda i, f: "panne_transport" if f == "e" and 100 <= i < 105 else "ok")
        s = sens_pool.sensibilite(commun.charger(self.d, {"t0": ws[0], "n_fixe": 120}, [(0, 0)]), sens_pool.QUASI_MORT)
        self.assertEqual((s["ok"], s["pools"], s["refus"]),
                         ({"calme": dict.fromkeys(fx.POOL, 100), "stress": {**dict.fromkeys("abcd", 20), "e": 15}},
                          {"calme": fx.POOL, "stress": fx.POOL}, []))

    def test_pool_min_refus_nomme(self):
        """Pool a, b, c, d ; c à 10 lectures ok sur 100 : pool réduit de 3 flux < 4 : refus nommé, aucune règle
        recalculée, aucun « R1 discrimine » recalculé. Rougit si la garde POOL-MIN-1 est absente."""
        fx.journaux(self.d, WS, lambda i, f: "ok" if f != "c" or i < 10 else "panne_transport", pool=list("abcd"))
        s = sens_pool.sensibilite(commun.charger(self.d, SEG, [(0, 0)]), sens_pool.QUASI_MORT)
        self.assertEqual((s["refus"], s["pools"], s["r1"]["strates"]), (["calme"], {}, {}))
        self.assertTrue(any("refus nommé (SHOGEN-POOL-MIN-1)" in x for x in s["lignes"]))
        self.assertFalse(any("R1 discrimine" in x for x in s["lignes"]))

    def test_deviant_flux_stale_retire_egalite_reste(self):
        """e toujours ok mais stale (σ = 30 s, source_ts = ws − 100) dans 60 fenêtres : p̂_e = 0,6, retiré ; d en panne
        dans 50 fenêtres : 2·50 = n, reste ; QUASI-MORT ne retire rien. Rougit si : critère lu sur le taux ok (e
        reste) ; « ≥ » au lieu de « > » (d retiré) ; pool non réduit."""
        def motif(i, f):
            if f == "e":
                return ("ok", WS[i] - 100.0) if i < 60 else "ok"
            return "panne_transport" if f == "d" and i < 50 else "ok"
        fx.journaux(self.d, WS, motif, sigma_classe={"place": "1000000000", "lent": "30"},
                    sigma_class_of_flux={**{f: "place" for f in "abcd"}, "e": "lent"},
                    tau_classe={"place": "0.5", "lent": "0.5"})
        d = commun.charger(self.d, SEG, [(0, 0)])
        s = sens_pool.sensibilite(d, sens_pool.DEVIANT)
        self.assertEqual((s["pools"], s["egalites"]), ({"calme": ["a", "b", "c", "d"]}, [("calme", "d")]))
        self.assertEqual((s["r1"], s["regle"]), reference(d, {"calme": ["a", "b", "c", "d"]}))
        self.assertEqual(sens_pool.sensibilite(d, sens_pool.QUASI_MORT)["pools"], {"calme": list("abcde")})


if __name__ == "__main__":
    unittest.main()
