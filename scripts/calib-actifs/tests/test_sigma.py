"""σ (T-CA-SIG-1 à 3 ; PROPOSITION §4.6) sur âges synthétiques ; attendus calculés à la main : ⌈99 × 212/100⌉ = 210,
⌈99 × 101/100⌉ = 100. Chaque test nomme la mutation qui le rougit."""
import unittest
from decimal import Decimal

import sigma
import socle

P = socle.lire()
BTC = {("sigma", "agregateur"): Decimal(900), ("sigma", "place_horodatee"): Decimal("90.5")}


class TestSigma(unittest.TestCase):
    def test_troisieme_terme(self):
        """T-CA-SIG-1 : une strate de 212 minutes, 100 fois (active, sans échange), puis active, 10 minutes sans
        échange, active : P99 des 212 cellules au rang 210 = 8, soit 3 × 8 × 60 = 1 440 s ; P99 des 101 suites au rang
        100 = 1 (180 s), descriptif ; strate de stress vide ; deux places : cellules mises en commun. Mutation M-CA-17 :
        P99 sur les suites au lieu des cellules."""
        ages = [0, 1] * 100 + [0, *range(1, 11), 0]
        terme, detail = sigma.troisieme_terme(P, {"coinbase": ages}, ["calme"] * 212)
        self.assertEqual((terme, detail), (1440, {"calme": (212, 8, 1), "stress": (0, None, None)}))
        self.assertEqual(sigma.troisieme_terme(P, {}, ["calme"] * 212)[0], None)
        deux = sigma.troisieme_terme(P, {"coinbase": [0, 5], "bitstamp": [0, 9]}, ["stress"] * 2)[0]
        self.assertEqual(deux, 3 * 9 * 60)                  # cellules des deux places mises en commun : 0, 5, 0, 9

    def test_maximum_des_strates(self):
        """C-2 (l.189, maximum sur les deux strates) : âges (0, 2) en calme et (0, 7) en stress, puis l'inverse : P99 au
        rang 2 de chaque strate, 2 et 7, maximum 7, soit 3 × 7 × 60 = 1 260 s dans les deux ordres. Mutations : G14
        (première strate) ; dernière strate."""
        for st in (["calme"] * 2 + ["stress"] * 2, ["stress"] * 2 + ["calme"] * 2):
            terme, detail = sigma.troisieme_terme(P, {"coinbase": [0, 2, 0, 7]}, st)
            self.assertEqual((terme, sorted(d[1] for d in detail.values())), (1260, [2, 7]))

    def test_cellules_et_suites(self):
        """Âges (-, 0, 1, 2, 0, 1) sur les strates (c, c, c, s, s, s) : cellules {c : 0, 1 ; s : 2, 0, 1} ; suites
        {s : 2, 1} (suite comptée dans la strate de sa dernière minute, suite ouverte en fin de fenêtre comprise).
        Mutation : suite ouverte en fin de fenêtre perdue."""
        ages, st = [None, 0, 1, 2, 0, 1], ["calme"] * 3 + ["stress"] * 3
        self.assertEqual((sigma.cellules(ages, st), sigma.suites(ages, st)),
                         ({"calme": [0, 1], "stress": [2, 0, 1]}, {"stress": [2, 1]}))

    def test_classe_sans_derniere_transaction(self):
        """T-CA-SIG-2 : population d'USDC vide (lecture A), d'ETH = coinbase ; USDC : terme absent, σ des places
        horodatées = max(30, ⌈90,5⌉) = 91 ; ETH avec un terme de 1 440 s : 1 440 ; en planchers seuls : 91.
        Mutation M-CA-18 : terme pris sur les places horodatées de la lecture (bitstamp pour USDC)."""
        self.assertEqual((sigma.population(P, "USDC"), sigma.population(P, "ETH")), ([], ["coinbase"]))
        self.assertEqual([sigma.sigmas(P, a, BTC, t, m)["place_horodatee"] for a, t, m in
                          (("USDC", None, "calibre"), ("ETH", 1440, "calibre"), ("USDT", 1440, "planchers_seuls"))],
                         [91, 1440, 91])

    def test_classes(self):
        """T-CA-SIG-3 : sans horodatage : aucun σ ; agrégateurs max(300, σ_BTC) : 900, puis 300 si σ_BTC = 120 ;
        oracle d'USDT 129 600 ; σ_BTC absent : CA/btc. Mutation M-CA-19 : σ = 30 s pour les places sans horodatage."""
        s = sigma.sigmas(P, "USDT", BTC, None, "calibre")
        self.assertEqual((s["sans_horodatage"], s["agregateur"], s["oracle_chainlink"]), (None, 900, 129600))
        self.assertEqual(sigma.sigmas(P, "USDT", BTC | {("sigma", "agregateur"): Decimal(120)}, None,
                                      "calibre")["agregateur"], 300)
        with self.assertRaises(socle.Refus) as r:
            sigma.sigmas(P, "ETH", {("sigma", "agregateur"): Decimal(900)}, None, "calibre")
        self.assertEqual((r.exception.code, "classe place_horodatee" in str(r.exception)), ("CA/btc", True))


if __name__ == "__main__":
    unittest.main()
