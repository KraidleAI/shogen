"""Population de τ des places et médiane leave-one-out (T-CA-TAU-1 à 3 ; PROPOSITION §4.3) sur prix synthétiques ;
écarts calculés à la main. Chaque test nomme la mutation qui le rougit."""
import unittest
from decimal import Decimal
from fractions import Fraction as F

import socle
import tau

P = socle.lire()

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

    def test_places(self):
        """τ des places : P99,9 par strate (rang ⌈999·N/1000⌉), maximum sur les strates : calme 1..1000 /100 000 (P99,9
        = 0,00999), stress 1..10 /10 000 (0,0010) : 1,5 × 0,00999 = 0,014985, soit 0,0150 ; strate vide :
        CA/population ; règle ≥ 2,85 % : CA/borne. Mutations : maximum pris sur la première strate ; strate vide
        admise ; borne haute non refusée."""
        cel = {"calme": ([F(i, 100000) for i in range(1, 1001)], [], []),
               "stress": ([F(i, 10000) for i in range(1, 11)], [], [])}
        r = tau.places(P, "ETH", cel)
        self.assertEqual((r["tau"], r["p999"], r["strates"]["stress"][:2]),
                         (F(15, 1000), F(999, 100000), (10, F(1, 1000))))
        for ecarts, code in ((([], [], []), "CA/population"), (([F(2, 100)], [], []), "CA/borne")):
            with self.assertRaises(tau.socle.Refus) as e:
                tau.places(P, "USDC", cel | {"stress": ecarts})
            self.assertEqual(e.exception.code, code)
        self.assertEqual(getattr(e.exception, "valeur", None), ("τ des places", Decimal("0.0300")))  # 1,5 × 0,02 (C-13)

    def test_agregateurs(self):
        """T-CA-AGR-1 (valeurs synthétiques) : τ_places 0,0010, τ_agr_BTC 0,0265, classes de places de BTC 0,0045 et
        0,0050 : dénominateur 0,0050, produit 0,0053, τ_agr 0,0055 ; avec le minimum, 0,0060 (imprimé) ; τ_agr ≥
        τ_places : pas de drapeau ; drapeau descriptif si τ_agr < τ_places (Q-CA-06), aucun à l'égalité ; τ de BTC
        absent : CA/btc. Mutations M-CA-15 : minimum des deux classes ; drapeau à l'égalité."""
        btc = {("tau", "agregateur"): Decimal("0.0265"), ("tau", "place_horodatee"): Decimal("0.0045"),
               ("tau", "sans_horodatage"): Decimal("0.0050")}
        r = tau.agregateurs(P, "ETH", Decimal("0.0010"), btc)
        self.assertEqual((r["tau"], r["autres"]["minimum"], r["sous_places"]), (F(55, 10000), F(60, 10000), False))
        drapeaux = [tau.agregateurs(P, "ETH", Decimal("0.0100"), btc | {("tau", "agregateur"): Decimal(x)})
                    ["sous_places"] for x in ("0.0020", "0.0050")]
        self.assertEqual(drapeaux, [True, False])               # 0,0040 < 0,0100 ; à l'égalité (0,0100), aucun drapeau
        with self.assertRaises(tau.socle.Refus) as e:
            tau.agregateurs(P, "ETH", Decimal("0.0010"), {k: v for k, v in btc.items() if k[1] != "sans_horodatage"})
        self.assertEqual(e.exception.code, "CA/btc")

    def test_agregateurs_suite(self):
        """C-1 : classes de BTC inversées (0,0050 horodatée, 0,0045 sans horodatage) : dénominateur 0,0050, τ_agr
        0,0055 (0,0060 sous la seule classe sans horodatage). C-9 : τ de BTC nul pour une classe : CA/btc. C-13 :
        τ_places 0,0100 : règle 0,053 ≥ 2,85 %, CA/borne portant la valeur 0,0530 hors du message. Mutations : G01
        (dénominateur = classe sans horodatage) ; G13 (τ nul admis) ; valeur non portée."""
        btc = {("tau", "agregateur"): Decimal("0.0265"), ("tau", "place_horodatee"): Decimal("0.0050"),
               ("tau", "sans_horodatage"): Decimal("0.0045")}
        self.assertEqual(tau.agregateurs(P, "ETH", Decimal("0.0010"), btc)["tau"], F(55, 10000))
        for k in btc:
            with self.assertRaises(tau.socle.Refus) as e:
                tau.agregateurs(P, "ETH", Decimal("0.0010"), btc | {k: Decimal(0)})
            self.assertEqual(e.exception.code, "CA/btc", k)
        with self.assertRaises(tau.socle.Refus) as e:
            tau.agregateurs(P, "ETH", Decimal("0.0100"), btc)
        self.assertEqual((e.exception.code, getattr(e.exception, "valeur", None), "0.053" in str(e.exception)),
                         ("CA/borne", ("τ des agrégateurs", Decimal("0.0530")), False))


if __name__ == "__main__":
    unittest.main()
