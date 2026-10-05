"""Sources SB-3 (E-S-09 à E-S-13, E-S-39, E-S-41, E-S-43 ; T-GEN-1) : chaîne à deux états de taux stationnaire
b/(1 − a + b) écrit à la main, moyenne simulée à 5 erreurs-types ; renouvellement alterné tiré pas à pas par des u
écrits à la main ; poids et paramètres refaits à la main en rationnels. Chaque test nomme les mutations qui le
rougissent. Les comparaisons « à 5 SE » se font en rationnels exacts, sans racine : (x̄ − r)² < 25·s²/R."""
import unittest
from fractions import Fraction

import aleas
import commun
import sources

PRM = commun.charger_parametres(environ={})
A = PRM["aleas"]


def suite(*u):
    """u() qui rend les valeurs données, dans l'ordre (StopIteration au-delà)."""
    return iter(u).__next__


def dans_5_se(x: list, r: Fraction) -> bool:
    """Moyenne des rationnels x à moins de 5 erreurs-types de r : (x̄ − r)² < 25·s²/R, s² variance sans biais."""
    m = sum(x, Fraction(0)) / len(x)
    s2 = sum(((y - m) * (y - m) for y in x), Fraction(0)) / (len(x) - 1)
    return (m - r) * (m - r) < 25 * s2 / len(x)


class TestSources(unittest.TestCase):
    def refus(self, code, f, *a):
        with self.assertRaises(commun.Refus) as c:
            f(*a)
        self.assertEqual(c.exception.code, code)

    def test_markov_t_gen_1(self):
        """a = 19/20, b = 1/30 : taux stationnaire b/(1 − a + b) = (1/30)/(1/20 + 1/30) = 2/5, à la main ; 2 000 chaînes
        de 40 fenêtres, flux distincts : part moyenne du temps en cours à moins de 5 SE de 2/5. Mutations M-GEN-1 (a et
        b inversés), M-GEN-2 (départ toujours hors épisode, non stationnaire), M-3A-02 (départ en cours avec la
        probabilité q au lieu de la part stationnaire)."""
        a, b = Fraction(19, 20), Fraction(1, 30)
        self.assertEqual(sources.stationnaire(1 / (1 - a), b), Fraction(2, 5))
        x = [Fraction(sum(f - d for d, f in sources.markov(aleas.flux(A, "T-GEN-1", r, "regime", 0), a, b, A, 40)),
                      40) for r in range(2000)]
        self.assertTrue(dans_5_se(x, Fraction(2, 5)))

    def test_alterner_pas_a_pas(self):
        """Loi 1×1 3×1 (moyenne 2), pauses géométriques q = 1/2 (seuils 1/2, 3/4, 7/8, …), part stationnaire 1/2 ; durée
        restante de poids 2, 1, 1 (seuils 1/2, 3/4). En cours à 0 (u = 0,1), reste 2 (0,6) ; pause 1 (0,3), durée 3
        (0,7) ; pause 3 (0,8), durée 1 (0,2) ; pause 7 (0,99), durée 3 coupée à l'horizon 20 (0,9). Hors épisode à 0
        (u = 0,5 = seuil exact), pause 2, durée 3 ; horizon atteint sans tirage de pause. Durée coupée par l'horizon ;
        q = 0 : rien. Mutations M-3A-03 (reste tiré dans la loi et non dans sa loi résiduelle), M-3A-04 (pause d'une
        fenêtre de moins), M-3A-05 (borne de la pause sans le « − 1 »), M-3A-06 (fin non coupée à l'horizon)."""
        loi = sources.Empirique([(1, 1), (3, 1)])
        q = Fraction(1, 2)
        self.assertEqual((loi.moyenne, sources.stationnaire(loi.moyenne, q)), (2, Fraction(1, 2)))
        segs = sources.alterner(suite(0.1, 0.6, 0.3, 0.7, 0.8, 0.2, 0.99, 0.9), loi, q, A, 20)
        self.assertEqual(segs, [(0, 2), (3, 6), (9, 10), (17, 20)])
        self.assertEqual(sources.masque(segs), 0b11100000001000111011)
        self.assertEqual(sources.alterner(suite(0.5, 0.6, 0.9), loi, q, A, 6), [(2, 5)])
        self.assertEqual(sources.alterner(suite(0.9, 0.6, 0.9), loi, q, A, 4), [(2, 4)])
        self.assertEqual(sources.alterner(suite(), loi, Fraction(0), A, 20), [])

    def test_residu_et_lois(self):
        """EP l.14 (1×301 2×24 3×6 5×1) : poids de la durée restante Σ_{l ≥ k} n_l = 332, 31, 7, 1, 1 pour k = 1..5
        (total 372 = cellules), moyenne 372/332 = 93/83 ; la géométrique de paramètre 1/20 a pour moyenne 20 et pour loi
        résiduelle elle-même ; longueur nulle ou non entière : SOURCES/loi. Mutations M-3A-07 (poids Σ_{l > k}), M-3A-08
        (longueur nulle admise)."""
        e = sources.Empirique([(1, 301), (2, 24), (3, 6), (5, 1)])
        self.assertEqual((e.moyenne, e.residu().hist), (Fraction(93, 83), ((1, 332), (2, 31), (3, 7), (4, 1), (5, 1))))
        g = sources.Geometrique(Fraction(1, 20), A)
        self.assertEqual((g.moyenne, g.residu() is g), (20, True))
        for h in ([(0, 3)], [(1.5, 2)], [(True, 1)]):
            self.refus("SOURCES/loi", sources.Empirique, h)

    def test_pause(self):
        """q = r/(μ(1 − r)) : r = 1/2, μ = 2 → 1/2 ; r = 3/10, μ = 1 → 3/7 ; r = 0 → 0 ; r = μ/(μ + 1) = 2/3 (μ = 2)
        admis, q = 1 ; r = 7/10 (μ = 2), r = 1, r < 0, r flottant : SOURCES/taux. Mutation M-3A-09 : borne μ/(μ + 1)
        retirée."""
        self.assertEqual([sources.pause(r, m) for r, m in ((Fraction(1, 2), 2), (Fraction(3, 10), 1), (Fraction(0), 1),
                                                           (Fraction(2, 3), 2))],
                         [Fraction(1, 2), Fraction(3, 7), 0, 1])
        for r in (Fraction(7, 10), Fraction(1), Fraction(-1, 10), 0.5):
            self.refus("SOURCES/taux", sources.pause, r, Fraction(2))
