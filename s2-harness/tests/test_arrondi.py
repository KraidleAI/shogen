"""Partie 2 de S2, étape A, sous-lot A1 (docs/adr-0028/G0-partie-2.md, section A) : SHOGEN-DECIMAL-ARRONDI-1
(annexe B l.232 : ROUND_HALF_EVEN dans chaque localcontext de r1.py, EMD de regle_critere compris) et
SHOGEN-PMORE-RESIDU-1 (annexe B l.298 : P_more sans annulation). Valeurs attendues écrites depuis un oracle en
fractions, sans le module decimal (arrondi pair à 50 chiffres d'un rationnel exact, une seule opération
inexacte par cas ; ROUND_DOWN y tronque le dernier chiffre). Chaque test nomme la mutation qui le rougit."""

from __future__ import annotations

import unittest
from decimal import ROUND_DOWN, Decimal as D, localcontext

from shogen_s2 import r1
from shogen_s2.r1 import Ecart
from tests.test_critere import NN, blk, deux, regle
from tests.test_r1 import R1, mk, rd
from tests.test_rendu_blocs import journal

DT = "0." + "6" * 49 + "7"                       # 2/3 arrondi au pair (ROUND_DOWN : 0,6…66)


def p_hat(n: int, pannes: dict) -> dict:
    """compute_r1 (pool a, b, c ; trois flux, hors-enveloppe non évaluable ; σ non évaluable) sur n fenêtres :
    pannes = {flux : rangs en panne}. Rend la strate « calme »."""
    m = [mk(60 * i) for i in range(n)]
    lec = [rd(60 * i, f, "panne_http" if i in pannes.get(f, ()) else "ok") for i in range(n) for f in "abc"]
    return R1(m, lec, list("abc"), sigma=None)["strates"]["calme"]


CAS = {   # site (ligne de r1.py à 8a2a4b3) : (appel, valeur par défaut, de l'oracle)
    "_median l.93": (lambda: r1._median([D(1), D("1." + "0" * 48 + "3")]), "1." + "0" * 48 + "2"),
    "classify_ecart l.167": (lambda: r1.classify_ecart({"status": "ok", "price": "5"}, [D(3)] * 3, 4, 60, "a",
                                                       {"c": None}, {"a": "c"}, {"c": D("0." + "6" * 50)}),
                             Ecart.HORS_ENVELOPPE),                         # 2/3 > τ = 0,6…6 (50 six)
    "poisson_binomial l.208": (lambda: r1.poisson_binomial([D("0.0" + "3" * 50)])[0], "0.9" + "6" * 48 + "7"),
    "_ecart_relatif l.229": (lambda: r1._ecart_relatif(dict(a=D(5), b=D(3), c=D(3), d=D(3)), "a"), DT),
    "gate_value l.250": (lambda: r1.gate_value(1, D("0." + "1" * 50)), "0.0" + "987654320" * 5 + "98765"),
    "z_score l.263": (lambda: r1.z_score(100, 12, D("0.1")), DT),             # (12 − 10)/√9
    "binomial_tail_ge l.290": (lambda: r1.binomial_tail_ge(1, 1, D("0." + "6" * 51)), DT),
    "z_pool_stratifie l.312": (lambda: r1.z_pool_stratifie([(100, 12, D("0.1"))])[2], DT),
    "block_long_run_variance l.353": (lambda: r1.block_long_run_variance([(0, 1), (1, 0), (2, 0)], 1, 1)["gamma0"],
                                      DT),                                  # γ̂₀ = (3·1 − 1)/3
    "bloc_strate l.379": (lambda: r1.bloc_strate(list(enumerate((1, 1, 1, 0, 1, 0, 1))), 1, D("0.5"),
                                                 D(1))["runs"]["longueur_moyenne"], "1." + "6" * 48 + "7"),
    "compute_r1 l.605": (lambda: p_hat(3, {"a": (1, 2)})["per_source"]["a"]["phat"], DT),
    "regle_critere l.701": (lambda: r1.regle_critere({"strates": {"a": blk("1", "5", "16", "9", 7)}})["strates"][
        "a"]["emd_fraction"], "1.8123" + "428571" * 7 + "429"),                # (2,33 + 0,8416)·√16/7
    "bornes_censure l.752": (lambda: r1.bornes_censure(100, 12, D("0.1"), 0, D(9))["z_bloc_bas"], DT),
}


class TestArrondiDecimal(unittest.TestCase):
    def test_round_down_ambiant_rend_la_valeur_par_defaut(self):
        """SHOGEN-DECIMAL-ARRONDI-1 : chaque site calculant de r1, appelé sous un contexte ambiant ROUND_DOWN, rend
        la valeur du contexte par défaut (valeur et chaîne). Rougit si : `ctx.rounding = ROUND_HALF_EVEN` retiré
        d'un des 13 sites calculants (le localcontext de compute_r1 l.646 ne compare que des Decimal publiées :
        mutant équivalent, déclaré au journal G1)."""
        for site, (appel, att) in CAS.items():
            with self.subTest(site=site):
                att = att if isinstance(att, Ecart) else D(att)
                self.assertEqual(appel(), att)
                with localcontext() as amb:
                    amb.rounding = ROUND_DOWN
                    obtenu = appel()
                self.assertEqual((obtenu, str(obtenu)), (att, str(att)))

    def test_regle_scellee_fixture_j2_sous_round_down(self):
        """Non-régression de SHOGEN-CRITERE-R1-1 (G0 de l'étape A, risque (c)) : fixture J2 de test_critere,
        ℓ = 240, valeurs scellées écrites à la main (NE REJETTE PAS, z < 2,33, dans les deux strates ; FAUX ; m = 2) ;
        sous ROUND_DOWN ambiant, sortie de compute_r1 et de la règle (EMD compris) égale à celle du contexte par
        défaut. Rougit si : arrondi ambiant hérité par z_score (l.263) ou l'EMD (l.701) : z et EMD de la strate
        calme au dernier chiffre."""
        j = journal(200, 200, deux(50, 37))
        defaut = regle(*j)
        with localcontext() as amb:
            amb.rounding = ROUND_DOWN
            bas = regle(*j)
        g = defaut[1]
        self.assertEqual([(e["valeur"], e["cas"]) for e in g["strates"].values()], [(NN, "z_sous_seuil")] * 2)
        self.assertEqual((g["r1_discrimine"], g["m"], r1.SEUIL_Z, r1.ELL_BLOC), ("FAUX", 2, D("2.33"), 240))
        self.assertEqual(bas, defaut)


class TestPmoreResidu(unittest.TestCase):
    def test_un_seul_flux_en_ecart_p_more_nul_exact(self):
        """SHOGEN-PMORE-RESIDU-1 : p̂ = (0, 1/28, 0) ⇒ P̂_more == 0 exact, P̂₁ = p̂, P̂₀ = 1 − p̂ arrondi une fois
        (oracle) ; au bout de compute_r1 (28 fenêtres, b en panne dans une seule) : garde 0, queue dégénérée.
        Rougit si : P_more = 1 − P₀ − P₁ en Decimal (résidu 4E-51, garde ≈ 1E-49, « queue exacte » publiée)."""
        p = D("0.035714285714285714285714285714285714285714285714286")            # 1/28 arrondi au pair
        p0, p1, pm = r1.poisson_binomial([D(0), p, D(0)])
        self.assertEqual((pm, p1, p0), (0, p, D("0.96428571428571428571428571428571428571428571428571")))
        b = p_hat(28, {"b": (5,)})
        self.assertEqual((b["per_source"]["b"]["phat"], b["P_more"], b["gate_value"]), (p, 0, 0))
        self.assertEqual((b["queue_exacte_applicable"], b["queue_binomiale_P_K_ge_Kobs"]), (False, None))
        self.assertIn("dégénérée", b["queue_note"])


if __name__ == "__main__":
    unittest.main()
