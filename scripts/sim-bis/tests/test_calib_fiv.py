"""Calibration E1, estimateur FIV_série SB-10a (E-S-38, E-S-39 ; T-FIV-1) : valeurs écrites à la main (série 1, 1, 0,
0 de la fixture de PLAN-S2BIS, scripts/plan-s2bis/tests/test_episodes.py l.36-44 ; série à lacune), chaînes d'EP
l.128 (γ̂₀ et σ̂²_bloc à ℓ = 1 ne dépendent que de n et K), et comptage naïf des γ̂_k depuis leur définition (paires de
la grille, écarts à Ī, en Fraction) sur des séries aléatoires à lacunes ; chaque test nomme les mutations qui le
rougissent."""
import random
import unittest
from fractions import Fraction

import calib_fiv
import calibration
import commun

PRM = commun.charger_parametres(environ={})
K_ = PRM["calibration"]


def bits(*positions):
    return sum(1 << p for p in positions)


def naif(presentes: list, vals: dict, ell: int):
    """FIV_série(ℓ) depuis la définition (r1 de f35a70c, docstring de block_long_run_variance) : γ̂_k = Σ (I_t − Ī)
    (I_{t+k} − Ī) sur les paires (t, t + k) présentes toutes deux, σ̂² = γ̂₀ + 2 Σ_{k<ℓ} (1 − k/ℓ) γ̂_k ; None si
    γ̂₀ = 0."""
    m = Fraction(sum(vals[t] for t in presentes), len(presentes))
    g = [sum((vals[t] - m) * (vals[t + k] - m) for t in presentes if t + k in vals) for k in range(ell)]
    s2 = g[0] + 2 * sum((1 - Fraction(k, ell)) * g[k] for k in range(1, ell))
    return None if g[0] == 0 else s2 / g[0]


class TestEstimateur(unittest.TestCase):
    def test_t_fiv_1(self):
        """I = 1, 1, 0, 0 : γ̂₀ = 1, γ̂₁ = 1/4, γ̂₂ = −1/2 ; ℓ = 1 : 1 ; ℓ = 2 : 1 + 1/4 = 5/4 ; ℓ = 3 : 1 + (4/3)(1/4)
        + (2/3)(−1/2) = 1 ; numérateur ℓ·n²·σ̂² : 16, 40, 48 ; chaînes « 1 », « 1.25 », « 1 » ; garde n ≥ 30ℓ non
        tenue. Mutations M-FIV-1 (poids 1 − (k + 1)/ℓ), M-10-01 (lag ℓ compté), M-10-02 (S_g et S_d confondus)."""
        c = calib_fiv.courbe(bits(0, 1, 2, 3), bits(0, 1), [1, 2, 3], K_)
        self.assertEqual([(x["ell"], x["n"], x["K"], x["numerateur"], str(x["FIV_serie"]), x["fiv"], x["garde"])
                          for x in c], [(1, 4, 2, 16, "1", 1, False), (2, 4, 2, 40, "1.25", Fraction(5, 4), False),
                                        (3, 4, 2, 48, "1", 1, False)])
        self.assertEqual((str(c[1]["gamma0"]), str(c[1]["sigma2_bloc"])), ("1", "1.25"))

    def test_lacune(self):
        """Positions 0, 1, 3, 4 (la 2 absente), I = 1, 1, ·, 0, 0 : la lacune ne forme aucune paire ; γ̂₁ = 1/4 + 1/4
        = 1/2 (paires 0-1 et 3-4), γ̂₂ = −1/4 (paire 1-3) ; FIV(2) = 1 + 1/2 = 3/2, FIV(3) = 1 + (4/3)(1/2)
        + (2/3)(−1/4) = 3/2 ; numérateurs 48 et 72. Mutation M-10-03 (série comprimée : paires à travers la
        lacune)."""
        c = calib_fiv.courbe(bits(0, 1, 3, 4), bits(0, 1), [2, 3], K_)
        self.assertEqual([(x["numerateur"], x["fiv"]) for x in c], [(48, Fraction(3, 2)), (72, Fraction(3, 2))])

    def test_bords(self):
        """K = 0 et K = n : γ̂₀ = 0, FIV indéfini (None) ; n = 0 : γ̂₀, σ̂² et FIV à None. Mutation M-10-04 (γ̂₀ = 0
        divisé)."""
        for val in (0, bits(0, 1, 2)):
            x = calib_fiv.courbe(bits(0, 1, 2), val, [2], K_)[0]
            self.assertEqual((str(x["gamma0"]), x["FIV_serie"], x["fiv"]), ("0", None, None))
        x = calib_fiv.courbe(0, 0, [1], K_)[0]
        self.assertEqual((x["n"], x["gamma0"], x["sigma2_bloc"], x["FIV_serie"]), (0, None, None, None))

    def test_chaines_d_ep_l128(self):
        """n = 24 585, K = 148 (EP l.128, D1-bis, calme, ℓ = 1) : γ̂₀ et σ̂²_bloc égaux aux valeurs imprimées par EP,
        sous le contexte décimal de r1 (précision 50, ROUND_HALF_EVEN). Mutation M-10-05 (contexte par défaut, 28
        chiffres)."""
        ep = calibration.charger(PRM, environ={})["fiv"]["D1-bis", "calme"][0]
        x = calib_fiv.courbe((1 << 24585) - 1, (1 << 148) - 1, [1], K_)[0]
        self.assertEqual((Fraction(str(x["gamma0"])), Fraction(str(x["sigma2_bloc"])), x["FIV_serie"]),
                         (ep["gamma0"], ep["sigma2"], 1))

    def test_garde(self):
        """60 positions : garde n ≥ 30·ℓ tenue à ℓ = 1 et 2 (60 ≥ 60), non tenue à ℓ = 3. Mutation M-10-06 (« > »)."""
        c = calib_fiv.courbe((1 << 60) - 1, 5, [1, 2, 3], K_)
        self.assertEqual([x["garde"] for x in c], [True, True, False])

    def test_comptage_naif(self):
        """300 séries aléatoires de 2 à 40 positions de grille, lacunes comprises, ℓ de 1 à 9 : FIV exact égal au
        comptage naïf des γ̂_k ; la chaîne décimale (deux quotients arrondis à 50 chiffres) à 10^-45 près, en relatif,
        du FIV exact. Mutation M-10-07 (M_k compté sur les seules positions à 1)."""
        g = random.Random(20261005)
        for _ in range(300):
            presentes = [t for t in range(g.choice(range(2, 41))) if g.random() < 0.8] or [0]
            vals = {t: int(g.random() < 0.3) for t in presentes}
            pres, val = sum(1 << t for t in presentes), sum(v << t for t, v in vals.items())
            c = calib_fiv.courbe(pres, val, list(range(1, 10)), K_)
            self.assertEqual([x["fiv"] for x in c], [naif(presentes, vals, ell) for ell in range(1, 10)])
            for x in (x for x in c if x["fiv"] is not None):
                self.assertLessEqual(abs(Fraction(str(x["FIV_serie"])) - x["fiv"]), x["fiv"] / 10 ** 45)

    def test_refus(self):
        """Série hors des positions présentes, masque négatif ou non entier, ℓ absents, nuls ou non entiers :
        FIV/entree. Mutation M-10-08 (contrôles des entrées retirés)."""
        for pres, val, ells in ((bits(0, 1), bits(2), [1]), (-1, 0, [1]), (True, 0, [1]), (bits(0), 0, []),
                                (bits(0), 0, [0]), (bits(0), 0, ["2"]), (bits(0), 0, [True])):
            with self.assertRaises(commun.Refus) as c:
                calib_fiv.courbe(pres, val, ells, K_)
            self.assertEqual(c.exception.code, "FIV/entree", (pres, val, ells))


if __name__ == "__main__":
    unittest.main()
