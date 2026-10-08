"""SHOGEN-DEP-FENETRES-2 (b) = SHOGEN-R1-PLUGIN-1 (a), SHOGEN-DEP-FENETRES-2 (c), SHOGEN-R1-PLUGIN-1 (b) : valeurs
dérivées à la main (journal G1) ; intégration contre r1 (runs, K). Chaque test nomme la mutation qui le rougit."""
import tempfile
import unittest
from decimal import Context, Decimal, localcontext
from fractions import Fraction

import commun
import influence
from tests import fixtures as fx

C60 = Context(prec=60)                          # références à 60 chiffres (le module calcule à 50)
# n = 6, N = 2 : D1 = (1, 1, 1, 0, 0, 0), D2 = (1, 1, 0, 0, 0, 0), I = D2 ; K = 2, p̂ = (1/2, 1/3), P̂_more = 1/6.
SERIE = [(60 * t, (int(t < 3), int(t < 2))) for t in range(6)]


class TestInfluence(unittest.TestCase):
    def test_influence_a_la_main(self):
        """g = (p̂_2, p̂_1) = (1/3, 1/2) ; IF = (1/6, 1/6, −1/3, 0, 0, 0) ; Σ IF² = 1/6 ; ℓ = 2 : Σ B² = 10/36,
        σ̂²_IF,bloc = 5/36 (= γ0 + γ1 = 6/36 − 1/36) ; K − n·P̂ = 1 ; z_IF,0 = √6, z_IF,bloc = 6/√5. Rougit si : poids
        g_i = p̂_i au lieu de p̂_j ; terme de plug-in omis ; Bartlett sans les blocs de bord."""
        r = influence.influence(SERIE, 60, 2)
        self.assertEqual((r["numerateur"], r["s0"], r["sbloc"]), (Fraction(1), Fraction(1, 6), Fraction(5, 36)))
        self.assertLess(abs(r["z0"] - Decimal(6).sqrt(C60)), Decimal("1e-45"))
        self.assertLess(abs(r["zbloc"] - C60.divide(6, Decimal(5).sqrt(C60))), Decimal("1e-45"))

    def test_runs_a_la_main(self):
        """Grille 0, 1, 2, 4, 5 (3 absente), I = 1, 1, 0, 1, 1, P = 1/4 : R = 2 ; μ = P si pas de prédécesseur, P(1 − P)
        sinon ; E[R] = 17/16 ; Var = 213/256 − 2·33/256 = 147/256 ; z_R = 15/√147. Rougit si : fenêtre absente qui
        prolonge un run ; covariance des voisins omise."""
        r = influence.runs([(0, 1), (60, 1), (120, 0), (240, 1), (300, 1)], 60, Fraction(1, 4))
        self.assertEqual((r["R"], r["E"], r["V"], r["longueurs"]), (2, Fraction(17, 16), Fraction(147, 256), {2: 2}))
        self.assertLess(abs(r["z"] - C60.divide(15, Decimal(147).sqrt(C60))), Decimal("1e-45"))

    def test_loi_de_m_a_la_main(self):
        """m_t = (2, 2, 1, 0, 0, 0) : observés (3, 1, 2) ; attendus n·PB(m ; 1/2, 1/3) = 6·(1/3, 1/2, 1/6) = (2, 3, 1).
        Rougit si la loi de Poisson-binomiale est remplacée par une binomiale à p moyen ou si un compte est décalé."""
        r = influence.loi_m(SERIE)
        self.assertEqual((r["observes"], r["attendus"]), ([3, 1, 2], [2, 3, 1]))

    def test_integration_runs_et_k_egaux_a_r1(self):
        """Fixture à deux strates, e mort en stress (D1 cas b), b parfois seule en panne : R et K de chaque strate égaux
        aux runs et à K de r1 ; Σ observés = n ; rapports imprimés au contexte nommé (constat C-4 de l'exécution, journal
        G1 §3). Rougit si les cellules ne viennent pas du pool D1 de la strate, ou si un rapport est calculé hors du
        contexte nommé."""
        d = tempfile.mkdtemp(prefix="pp_inf_")
        ws = [fx.VEN + 86400 - 1200 + 60 * i for i in range(40)]
        fx.journaux(d, ws, lambda i, f: "panne_transport" if (f in "ab" and i % 7 in (0, 1)) or (f == "b" and i % 5 == 3)
                    or (f == "e" and i >= 20) else "ok")
        dd = commun.charger(d, {"t0": ws[0], "n_fixe": 40}, [(0, 0)])
        res = influence.analyse(dd)
        for st, b in dd["base"]["strates"].items():
            x = res["strates"][st]
            self.assertEqual((x["runs"]["R"], x["inf"]["K"], sum(x["loi"]["observes"])),
                             (b["bloc"]["runs"]["nombre"], b["K"], b["n"]))
            with localcontext(commun.r1.contexte_decimal()):     # constat C-4 : rapports au contexte nommé (50)
                r0 = influence._d(x["inf"]["s0"]) / b["gate_value"]
            self.assertTrue(any(f"(rapport à n·P̂(1 − P̂) : {commun.dec(r0)})" in y for y in res["lignes"]))


if __name__ == "__main__":
    unittest.main()
