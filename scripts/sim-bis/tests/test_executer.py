"""Exécution SB-11 (E-S-40 à E-S-48, E-S-52) : attendus écrits à la main ou produits par un outil distinct (`bc -l`,
`sha256sum`) ; chaque test nomme les mutations qui le rougissent."""
import unittest
from decimal import Decimal
from fractions import Fraction

import commun
import executer

PRM = commun.charger_parametres(environ={})
K_ = PRM["calibration"]


def code_de(f, *a):
    """Code du refus nommé levé par f(*a), nom de l'exception sinon, None sans exception (rouge d'assertion)."""
    try:
        f(*a)
    except commun.Refus as e:
        return e.code
    except Exception as e:                                          # noqa: BLE001 (rouge d'assertion, jamais d'erreur)
        return type(e).__name__
    return None


class TestTaux(unittest.TestCase):
    def test_taux_e_s_40(self):
        """E-S-40 : x = 122 sur 10⁴ : r̂ = 61/5 000, SE = √(122·9 878/10¹²) (bc -l, à 10⁻⁵² près : 50 chiffres sous le
        contexte de r1), aucune borne ; x = 0 sur 10⁴ : SE nulle, borne 1 − 0,05^(1/10⁴) (bc -l :
        1 - e(l(0.05)/10000), à 10⁻⁴⁸ près) ; x = 1 sur 100 : SE = √(99/10⁶) ; x = R : SE nulle, aucune borne.
        Mutations M-11A-06 (SE sans racine), M-11A-07 (R − 1 au dénominateur), M-11A-08 (borne quand x > 0), M-11A-09
        (borne 1 − 0,05^R), M-11A-10 (contexte par défaut, 28 chiffres)."""
        se = Decimal("0.0010977777552856497920739905119903281276065317669013518111719989972695")
        t = executer.taux(122, 10000, K_)
        self.assertEqual((t["x"], t["R"], t["r"], t["borne"]), (122, 10000, Fraction(61, 5000), None))
        self.assertLess(abs(t["SE"] - se), Decimal("1E-52"))
        b = Decimal("0.0002995283597766120092834713389476236471831496972729805716154849335380")
        t = executer.taux(0, 10000, K_)
        self.assertEqual((t["r"], t["SE"]), (0, 0))
        self.assertLess(abs(t["borne"] - b), Decimal("1E-48"))
        se = Decimal("0.0099498743710661995473447982100120600517812656367680607911760464383494")
        self.assertLess(abs(executer.taux(1, 100, K_)["SE"] - se), Decimal("1E-52"))
        t = executer.taux(7, 7, K_)
        self.assertEqual((t["r"], t["SE"], t["borne"]), (1, 0, None))

    def test_borne_a_2000(self):
        """Borne à R = 2 000 (familles secondaires, Q-S-06) : 1 − 0,05^(1/2 000) (bc -l, à 10⁻⁴⁸ près). Mutation
        M-11A-09 (borne 1 − 0,05^R)."""
        b = Decimal("0.0014967448951882842161127126443267129932794737843594269185378142370390")
        x = executer.taux(0, 2000, K_)
        self.assertIsInstance(x["borne"], Decimal)
        self.assertLess(abs(x["borne"] - b), Decimal("1E-48"))

    def test_taux_refus(self):
        """x < 0, x > R, R = 0, booléen, R en Fraction : EXEC/taux, jamais une autre exception. Mutation M-11A-11
        (contrôle retiré)."""
        for x, r in ((-1, 10), (11, 10), (0, 0), (True, 10), (1, Fraction(10))):
            self.assertEqual(code_de(executer.taux, x, r, K_), "EXEC/taux", (x, r))


class TestFrequences(unittest.TestCase):
    R6 = [{"valeur": "REJETTE", "causes": []}, {"valeur": "NE REJETTE PAS", "causes": []},
          {"valeur": "NON ÉVALUABLE", "causes": ["unites", "k_crit", "runs"]},
          {"valeur": "NON ÉVALUABLE", "causes": ["k_crit", "runs"]}, {"valeur": "NON ÉVALUABLE", "causes": ["n_prime"]},
          {"valeur": "NON ÉVALUABLE", "causes": ["k_crit", "runs"]}]

    def test_frequences_e_s_52(self):
        """E-S-52 et AVIS-SIM-T3, observation 3 : six résultats écrits à la main ; valeurs 1, 1, 4 ; causes (non
        exclusives) unites 1, k_crit 3, runs 3, n_prime 1 ; information insuffisante (unites, k_crit ou runs) 3 ;
        combinaisons « unites+k_crit+runs » 1, « k_crit+runs » 2, « n_prime » 1, de somme 4, le compte de NON
        ÉVALUABLE. Mutations M-11A-12 (combinaisons omises), M-11A-13 (n_prime compté en information insuffisante),
        M-11A-14 (première cause seule comptée)."""
        f = executer.frequences(self.R6)
        self.assertEqual(f, {"valeurs": {"REJETTE": 1, "NE REJETTE PAS": 1, "NON ÉVALUABLE": 4},
                             "causes": {"unites": 1, "k_crit": 3, "runs": 3, "n_prime": 1}, "insuffisante": 3,
                             "combinaisons": {"unites+k_crit+runs": 1, "k_crit+runs": 2, "n_prime": 1}})
        self.assertEqual(sum(f["combinaisons"].values()), f["valeurs"]["NON ÉVALUABLE"])

    def test_frequences_refus(self):
        """« NON TESTÉ (séquence) » (présentation de regle.strate, non une valeur du moteur), cause inconnue, causes
        dans le désordre ou en double, NON ÉVALUABLE sans cause, REJETTE avec une cause : EXEC/frequences. Mutation
        M-11A-15 (contrôle retiré)."""
        for v, c in (("NON TESTÉ (séquence)", []), ("NON ÉVALUABLE", ["garde"]), ("NON ÉVALUABLE", ["runs", "k_crit"]),
                     ("NON ÉVALUABLE", ["runs", "runs"]), ("NON ÉVALUABLE", []), ("REJETTE", ["runs"])):
            self.assertEqual(code_de(executer.frequences, self.R6 + [{"valeur": v, "causes": c}]), "EXEC/frequences",
                             (v, c))


if __name__ == "__main__":
    unittest.main()
