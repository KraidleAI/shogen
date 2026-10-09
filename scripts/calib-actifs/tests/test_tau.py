"""Population de τ des places et médiane leave-one-out (T-CA-TAU-1 à 3 ; PROPOSITION §4.3) sur prix synthétiques ;
écarts calculés à la main. Chaque test nomme la mutation qui le rougit."""
import unittest
from decimal import Decimal
from fractions import Fraction as F

import tau

PLACES = ("bitfinex", "bitstamp", "coinbase", "kraken", "okx")


def cas(prix, ages=None, n_min=4, exclusion=None, strates=("calme",)):
    """Une minute (ou plus) : prix {place : liste}, âges nuls par défaut ; rend {strate : (écarts, places, âges)}."""
    closes = {p: [None if x is None else F(x) for x in v] for p, v in prix.items()}
    ages = ages or {p: [0] * len(v) for p, v in prix.items()}
    return tau.ecarts("ETH", closes, ages, list(strates), n_min, exclusion or {})


class TestTau(unittest.TestCase):
    def test_mediane_leave_one_out(self):
        """T-CA-TAU-1 : quatre places à 100, 101, 102 et 110 : pour 110, médiane des autres 101, écart 9/101 ; pour
        100, médiane 102, écart 2/102 ; 101 : 1/102 ; 102 : 1/101. Cinq places 100, 101, 103, 110, 120 : pour 120,
        médiane (101 + 103)/2 = 102, écart 18/102. Mutation M-CA-09 : médiane qui inclut la place."""
        e, pl, _a = cas(dict(zip(PLACES, ([100], [101], [102], [110]))))["calme"]
        self.assertEqual(dict(zip(pl, e)), {"bitfinex": F(2, 102), "bitstamp": F(1, 102), "coinbase": F(1, 101),
                                            "kraken": F(9, 101)})
        e, pl, _a = cas(dict(zip(PLACES, ([100], [101], [103], [110], [120]))))["calme"]
        self.assertEqual(e[pl.index("okx")], F(18, 102))

    def test_n_min(self):
        """T-CA-TAU-2 : trois places définies (la quatrième avant sa première minute active), N_min = 4 : minute
        exclue ; à la minute suivante, quatre définies : quatre cellules, en stress. Mutation M-CA-10 : N_min = 3."""
        r = cas(dict(zip(PLACES, ([100, 100], [101, 101], [102, 102], [None, 110]))), strates=("calme", "stress"))
        self.assertEqual((len(r["calme"][0]), len(r["stress"][0])), (0, 4))

    def test_exclusion(self):
        """T-CA-TAU-3 : coinbase à l'âge de 4 minutes, σ de 180 s (240 > 180) : sa cellule sort de la population, son
        prix (110) reste dans la médiane des autres : pour bitfinex (100), médiane de 101, 110, 102 = 102 ; à l'âge de 3
        (180, non > 180) : gardée. Mutation M-CA-11 : cellule retirée aussi des médianes (101,5)."""
        prix = dict(zip(PLACES, ([100], [101], [110], [102])))
        for age, attendu in ((4, ["bitfinex", "bitstamp", "kraken"]),
                             (3, ["bitfinex", "bitstamp", "coinbase", "kraken"])):
            ages = {p: [age if p == "coinbase" else 0] for p in prix}
            e, pl, ag = cas(prix, ages, exclusion={"coinbase": 180})["calme"]
            self.assertEqual((pl, e[0]), (attendu, F(2, 102)))
        self.assertEqual(ag, [0, 0, 3, 0])

    def test_mediane_nulle_et_rationnels(self):
        """Médiane leave-one-out nulle : CA/mediane, nommée par l'actif, la strate et la place ; clôtures Decimal
        converties en Fraction exactes (0,1 = 1/10), None gardé. Mutations : garde m ≤ 0 retirée ; conversion en
        flottant."""
        with self.assertRaises(tau.socle.Refus) as r:
            cas(dict(zip(PLACES, ([0], [0], [0], [1]))))
        self.assertEqual((r.exception.code, str(r.exception).endswith("strate calme ; place bitfinex")),
                         ("CA/mediane", True))
        self.assertEqual(tau.rationnels([Decimal("0.1"), None, Decimal("0.1")]), [F(1, 10), None, F(1, 10)])


if __name__ == "__main__":
    unittest.main()
