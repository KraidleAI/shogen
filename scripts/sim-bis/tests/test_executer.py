"""Exécution SB-11 (E-S-40 à E-S-48, E-S-52) : attendus écrits à la main ou produits par un outil distinct (`bc -l`,
`sha256sum`) ; chaque test nomme les mutations qui le rougissent."""
import hashlib
import os
import tempfile
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


R2 = [{"i": 0, "x": Fraction(1, 3), "d": Decimal("0.5"), "t": (1, 2)}, {"i": 1, "x": Fraction(2), "d": None, "t": []}]


class TestLots(unittest.TestCase):
    def setUp(self):
        d = tempfile.TemporaryDirectory()
        self.addCleanup(d.cleanup)
        self.r = d.name

    def test_empreinte_e_s_44(self):
        """E-S-44 : sha256 de la suite ordonnée des enregistrements, JSON canonique d'une ligne chacun : Fraction en
        « num/den », Decimal en chaîne, tuple en liste ; attendu par echo | sha256sum (c4a6d8b4…). Mutations M-11B-01
        (ordre des enregistrements perdu), M-11B-02 (Fraction écrite autrement)."""
        self.assertEqual(executer.empreinte(R2), "c4a6d8b4f33a2487e1e7951af1da654f8d50f7064a1121a1de40deb5bece3afb")
        self.assertNotEqual(executer.empreinte(R2[::-1]), executer.empreinte(R2))

    def test_lot_octets(self):
        """E-S-45, E-S-05, E-S-06 : lot (N1, [0, 1)), entête ["e"] : étiquette en première ligne, puis le JSON canonique
        écrit à la main ; nom N1.000000-000001.lot ; sha256 rendu = echo | sha256sum (ccf13dfc…) ; réécriture :
        SORTIE/existe ; lot perdu, puis refait : mêmes octets. Mutations M-11B-03 (étiquette absente), M-11B-04
        (extension .jsonl)."""
        c, h = executer.ecrire_lot(self.r, "N1", 0, 1, [{"i": 0}], ["e"])
        h0 = "ccf13dfc9e5665f73fa08c0f64dbcb47c1267e0f28afcb1502c6972d3fc9d6b8"
        self.assertEqual((os.path.basename(c), h), ("N1.000000-000001.lot", h0))
        with open(c, "rb") as f:
            self.assertEqual(hashlib.sha256(f.read()).hexdigest(), h)
        self.assertEqual(code_de(executer.ecrire_lot, self.r, "N1", 0, 1, [{"i": 0}], ["e"]), "SORTIE/existe")
        os.unlink(c)
        self.assertEqual(executer.ecrire_lot(self.r, "N1", 0, 1, [{"i": 0}], ["e"]), (c, h))

    def test_lots_couverture(self):
        """E-S-45 : chaque i de [0, R) une fois et une seule. Lots [0, 2) et [2, 4) : quatre enregistrements dans
        l'ordre, ceux de N10 ignorés ; [2, 4) retiré : LOT/manquant ; [1, 3) ajouté : LOT/double ; R = 3 : LOT/surplus ;
        trou au milieu ([0, 2) et [3, 4)) : LOT/manquant ; dossier vide : LOT/manquant. Mutations M-11B-05 (trou
        admis), M-11B-06 (recouvrement admis), M-11B-07 (cellule par préfixe sans point)."""
        for a, b in ((0, 2), (2, 4)):
            executer.ecrire_lot(self.r, "N1", a, b, [{"i": i, "v": 10 * i} for i in range(a, b)], ["e"])
        executer.ecrire_lot(self.r, "N10", 0, 1, [{"i": 0, "v": 99}], ["e"])
        self.assertEqual([x["v"] for x in executer.lire_lots(self.r, "N1", 4, ["e"])], [0, 10, 20, 30])
        self.assertEqual(code_de(executer.lire_lots, self.r, "N1", 3, ["e"]), "LOT/surplus")
        executer.ecrire_lot(self.r, "N1", 1, 3, [{"i": i, "v": 10 * i} for i in (1, 2)], ["e"])
        self.assertEqual(code_de(executer.lire_lots, self.r, "N1", 4, ["e"]), "LOT/double")
        for n in ("N1.000001-000003.lot", "N1.000002-000004.lot"):
            os.unlink(os.path.join(self.r, n))
        self.assertEqual(code_de(executer.lire_lots, self.r, "N1", 4, ["e"]), "LOT/manquant")
        executer.ecrire_lot(self.r, "N1", 3, 4, [{"i": 3, "v": 30}], ["e"])
        self.assertEqual(code_de(executer.lire_lots, self.r, "N1", 4, ["e"]), "LOT/manquant")
        self.assertEqual(code_de(executer.lire_lots, self.r, "X1", 1, ["e"]), "LOT/manquant")

    def test_lot_forme(self):
        """Entête différente : LOT/entete ; enregistrement retouché (empreinte), étiquette retouchée, JSON non
        canonique : LOT/forme ; i hors de la plage, plage vide, nom de cellule à « / » ou à « . » : LOT/indices ou
        LOT/nom. Mutations M-11B-08 (empreinte non recalculée), M-11B-09 (entête non comparée), M-11B-10 (forme
        canonique non exigée)."""
        c, _h = executer.ecrire_lot(self.r, "N1", 0, 1, [{"i": 0, "v": 1}], ["e"])
        self.assertEqual(code_de(executer.lire_lots, self.r, "N1", 1, ["autre"]), "LOT/entete")
        with open(c, "rb") as f:
            o = f.read()
        for avant, apres in ((b'"v":1', b'"v":2'), (b"synth", b"Synth"), (b'"fin":1', b'"fin": 1')):
            with open(c, "wb") as f:
                f.write(o.replace(avant, apres))
            self.assertEqual(code_de(executer.lire_lots, self.r, "N1", 1, ["e"]), "LOT/forme", apres)
        for cel, a, b, e, code in (("N2", 0, 1, [{"i": 1}], "LOT/indices"), ("N2", 1, 1, [], "LOT/nom"),
                                   ("E1/1", 0, 1, [{"i": 0}], "LOT/nom"), ("N1.x", 0, 1, [{"i": 0}], "LOT/nom")):
            self.assertEqual(code_de(executer.ecrire_lot, self.r, cel, a, b, e, ["e"]), code, cel)


if __name__ == "__main__":
    unittest.main()
