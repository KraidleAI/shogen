"""Sources SB-3 (E-S-09 à E-S-13, E-S-39, E-S-41, E-S-43 ; T-GEN-1) : chaîne à deux états de taux stationnaire
b/(1 − a + b) écrit à la main, moyenne simulée à 5 erreurs-types ; renouvellement alterné tiré pas à pas par des u
écrits à la main ; poids et paramètres refaits à la main en rationnels. Chaque test nomme les mutations qui le
rougissent. Les comparaisons « à 5 SE » se font en rationnels exacts, sans racine : (x̄ − r)² < 25·s²/R."""
import unittest
from fractions import Fraction

import aleas
import calibration
import commun
import sources

PRM = commun.charger_parametres(environ={})
A = PRM["aleas"]
EP = calibration.charger(PRM, environ={})["episodes"]


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

    def test_parametres_et_flux(self):
        """Composants de flux pré-déclarés (Q-4) et strate à loi regroupée (E-S-10) ; flux = aleas.flux du composant ;
        composant non déclaré : SOURCES/composant. Mutation M-3B-01 : contrôle du composant retiré."""
        s = PRM["sources"]
        self.assertEqual(s["composants"], ["regime", "panne", "panne-regime", "longues", "ecart", "ecart-regime",
                                           "hors-enveloppe", "derive", "derive-episodes", "incidents",
                                           "incidents-hotes", "faibles"])
        self.assertEqual(s["regroupees"], ["stress"])
        self.assertEqual(sources.flux(PRM, "N1", 0, "panne", 3)(), aleas.flux(A, "N1", 0, "panne", 3)())
        self.refus("SOURCES/composant", sources.flux, PRM, "N1", 0, "inconnu", 0)

    def test_taux_ep_q_3(self):
        """p = cellules/n_s exact (Q-3) : EP l.13 et l.15 (binance calme : panne 372, écart 372, n_s 24 585), l.17 et
        l.19 (bitfinex calme : 30 et 32), l.81 et l.83 (gemini stress : 19 et 21, n_s 11 397) ; écart
        propre = (écart − panne)/n_s (E-S-09) ; écart moins nombreux que la panne, ou n_s différents : SOURCES/taux.
        Mutations M-3B-02 (taux décimal imprimé au lieu de cellules/n_s), M-3B-03 (écart total au lieu de l'écart
        propre), M-3B-04 (contrôle retiré)."""
        self.assertEqual(sources.taux(EP, "calme", "binance"), (Fraction(372, 24585), 0))
        self.assertEqual(sources.taux(EP, "calme", "bitfinex"), (Fraction(30, 24585), Fraction(2, 24585)))
        self.assertEqual(sources.taux(EP, "stress", "gemini"), (Fraction(19, 11397), Fraction(2, 11397)))
        for champ, v in (("cellules", 371), ("n_s", 24584)):
            faux = dict(EP)
            faux["calme", "binance", "ecart"] = dict(EP["calme", "binance", "ecart"], **{champ: v})
            self.refus("SOURCES/taux", sources.taux, faux, "calme", "binance")

    def test_composantes_e_s_11_e_s_12(self):
        """p = 3/100, part longue λ = 1/5, régime φ = 1/10, κ = 5, à la main : r_L = λp = 3/500 ; reste p_A = (p − r_L)/
        (1 − r_L) = (12/500)/(497/500) = 12/497 ; r_E = p_A/(1 − φ + φκ) = (12/497)/(7/5) = 60/3 479 ; r' = r_E(κ − 1)/
        (1 − r_E) = 240/3 419 ; contrôle : 1 − (1 − r_E)(1 − φr')(1 − r_L) = 1 − (3 395/3 479)(497/500) = 3/100, car
        3 479 = 7 × 497. C0 (régime None) et λ = 0 : tout le taux en r_E. Rapport des taux de A en régime dégradé et
        normal : (r_E + (1 − r_E)r')/r_E = κ. Mutations M-3B-10 (r_E = p_A sans le facteur du régime), M-3B-11 (part
        longue retranchée sans renormaliser : p_A = p − r_L), M-3B-12 (r' sans le facteur 1/(1 − r_E))."""
        c = sources.composantes(Fraction(3, 100), Fraction(1, 5), (Fraction(1, 10), Fraction(5), 60))
        self.assertEqual(c, {"longues": Fraction(3, 500), "base": Fraction(60, 3479), "regime": Fraction(240, 3419)})
        self.assertEqual((c["base"] + (1 - c["base"]) * c["regime"]) / c["base"], 5)
        self.assertEqual(sources.composantes(Fraction(3, 100), Fraction(0), None),
                         {"longues": 0, "base": Fraction(3, 100), "regime": 0})

    def test_lois_regroupees_e_s_10(self):
        """Loi « tous épisodes » d'EP (adjudication Q-2) : calme, par hôte et par type (binance panne = EP l.14, gemini
        écart = EP l.44) ; stress, regroupée sur les dix hôtes (E-S-10 ; sommes faites à la main sur EP l.54 à l.92) :
        panne 1×662 2×11 (684 cellules), écart 1×662 2×12 (686). Mutations M-3B-05 (regroupement ignoré), M-3B-06
        (regroupement en toute strate), M-3B-07 (type ignoré)."""
        self.assertEqual(sources.loi_longueurs(PRM, EP, "calme", "binance", "panne").hist,
                         ((1, 301), (2, 24), (3, 6), (5, 1)))
        self.assertEqual(sources.loi_longueurs(PRM, EP, "calme", "gemini", "ecart").hist,
                         ((1, 53), (2, 3), (4, 1), (5, 1)))
        self.assertEqual(sources.loi_longueurs(PRM, EP, "stress", "okx", "panne").hist, ((1, 662), (2, 11)))
        self.assertEqual(sources.loi_longueurs(PRM, EP, "stress", "binance", "ecart").hist, ((1, 662), (2, 12)))

    def test_oracle_c0_e_s_39(self):
        """E-S-39 (C0, sans observateurs) : binance calme panne à f = 1, r = 372/24 585, loi d'EP l.14 ; 200
        réplications de 10 080 fenêtres : part du temps en épisode à moins de 5 SE de r ; parts des longueurs 1, 2, 3, 5
        parmi les épisodes entiers (ni coupés à 0 ni à l'horizon) à moins de 5 SE de (301, 24, 6, 1)/332, aucune autre
        longueur. Mutations M-3B-08 (durée de chaque épisode tirée dans la loi résiduelle), M-3B-09 (départ hors
        épisode)."""
        loi, r = sources.loi_longueurs(PRM, EP, "calme", "binance", "panne"), Fraction(372, 24585)
        q, x, n = sources.pause(r, loi.moyenne), [], {}
        for i in range(200):
            segs = sources.alterner(sources.flux(PRM, "E-S-39", i, "panne", 0), loi, q, A, 10080)
            x.append(Fraction(sum(f - d for d, f in segs), 10080))
            for d, f in segs:
                if 0 < d and f < 10080:
                    n[f - d] = n.get(f - d, 0) + 1
        self.assertTrue(dans_5_se(x, r))
        self.assertEqual(sorted(n), [1, 2, 3, 5])
        for lg, c in ((1, 301), (2, 24), (3, 6), (5, 1)):
            p, tot = Fraction(c, 332), sum(n.values())
            self.assertTrue((Fraction(n[lg], tot) - p) ** 2 < 25 * p * (1 - p) / tot, lg)

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
