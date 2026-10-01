"""Lot B-DEP-1 d'ADR-0028 (A-1, A-2 ; §1 bis.1 pts 3 et 9) : variance de long terme par blocs de la
série I_t = 1{m_t ≥ 2} d'une strate (Künsch 1989, P-01, OCR seul, [2nd] : blocs mobiles, noyau de
Bartlett, forme non restreinte), à comptes entiers par lag sur la grille UTC. Oracles écrits sous
d'autres formes que le code : énumération explicite des paires (Fraction) ; sommes de blocs de la série
centrée complétée par des 0 (entiers, CRITIQUE v2 §4.1) ; valeurs à la main recopiées de la commande
(88/75, 208/75). Chaque test nomme la mutation qui le rougit."""

from __future__ import annotations

import random
import unittest
from decimal import Decimal, localcontext
from fractions import Fraction

from shogen_s2 import r1

W = 60
S1 = (0, 1, 1, 0, 0, 0, 1, 0, 0, 1)                # CRITIQUE v2 §4.1, recopiées de la commande
S2 = (1, 1, 0, 0, 0, 0, 0, 1, 1, 0)


def serie(bits, w=W, t0=0, pos=None) -> list:
    """Couples (window_start, I_t) aux positions `pos` (défaut 0..n−1) de la grille de pas w depuis t0."""
    return [(t0 + w * p, i) for p, i in zip(range(len(bits)) if pos is None else pos, bits)]


def blocs_numerateur(s, w, ell) -> int:
    """Oracle : N = Σ_j (Σ_{t ∈ bloc j} (n·I_t − K))², blocs de longueur ℓ sur la grille complétée
    par des 0 (identité de la CRITIQUE v2 §4.1) ; N = ℓ·n²·σ̂²."""
    n, k = len(s), sum(i for _, i in s)
    y = {(x - s[0][0]) // w: n * i - k for x, i in s}
    return sum(sum(y.get(t, 0) for t in range(j, j + ell)) ** 2 for j in range(1 - ell, max(y) + 1))


def demi_ulp(d: Decimal, exact: Fraction) -> bool:
    """Vrai si d est à au plus une demi-unité de son 50e chiffre significatif de la valeur exacte."""
    return abs(Fraction(d) - exact) <= Fraction(10) ** (d.adjusted() - r1.DECIMAL_PREC + 1) / 2


def d50(num, den) -> Decimal:
    with localcontext() as ctx:
        ctx.prec = r1.DECIMAL_PREC
        return Decimal(num) / Decimal(den)


class TestVarianceBlocsPure(unittest.TestCase):
    def test_valeurs_a_la_main_n10_l3(self):
        """n = 10, ℓ = 3 : σ̂² = 88/75 et 208/75, N = 352 et 832, γ̂₀ = 12/5 (CRITIQUE v2
        §4.1) ; Decimal égaux (== et str) à la division correctement arrondie à la précision 50.
        Rougit si : poids 1 − k/ℓ omis ; centrage omis ; γ̂₀ non centré ; lag ℓ inclus ; poids
        du lag 0 doublé ; S_g + S_d remplacé ; précision par défaut."""
        for bits, num, a in ((S1, 352, 88), (S2, 832, 208)):
            v = r1.block_long_run_variance(serie(bits), W, 3)
            self.assertEqual((v["n"], v["K"], v["numerateur"]), (10, 4, num))
            for x, y in ((v["sigma2_bloc"], d50(a, 75)), (v["gamma0"], Decimal("2.4"))):
                self.assertEqual((x, str(x)), (y, str(y)))

    def test_identite_l1_gamma0(self):
        """ℓ = 1 : σ̂²_bloc = γ̂₀ = n·Ī(1 − Ī) = K(n − K)/n, avec ou sans trous (CRITIQUE
        v2 §4.1). Rougit si : γ̂₀ non centré ; poids du lag 0 doublé."""
        for bits, pos in ((S1, None), ((1, 0, 1, 1, 0), (0, 3, 4, 9, 11)), ((1, 1, 1), None),
                          ((0, 1, 1), None)):
            v = r1.block_long_run_variance(serie(bits, pos=pos), W, 1)
            exact = Fraction(sum(bits) * (len(bits) - sum(bits)), len(bits))
            self.assertEqual(v["sigma2_bloc"], v["gamma0"])
            self.assertTrue(demi_ulp(v["gamma0"], exact), (bits, v))

    def test_serie_a_runs_facteur_calcule(self):
        """Série à runs I = (1,1,1,1,0,0,0,0), ℓ = 4 (valeur à la main du journal G1, §4) :
        γ̂₀ = 2, σ̂² = 17/4, σ̂²/γ̂₀ = 17/8 > 1 ; sommes de blocs : N = 4·8²·17/4 = 1 088.
        Rougit si : poids 1 − k/ℓ omis ; centrage omis."""
        s = serie((1, 1, 1, 1, 0, 0, 0, 0))
        v = r1.block_long_run_variance(s, W, 4)
        self.assertEqual((v["numerateur"], v["gamma0"], v["sigma2_bloc"]),
                         (1088, Decimal(2), Decimal("4.25")))
        self.assertEqual(Fraction(v["sigma2_bloc"]) / Fraction(v["gamma0"]), Fraction(17, 8))
        self.assertEqual(blocs_numerateur(s, W, 4), 1088)

    def test_positivite_trous_sommes_de_blocs(self):
        """Grilles trouées tirées (graine fixe), ℓ ∈ {1, 2, 3, 5, 8}, w ∈ {60, 3600}, origine
        quelconque : N égale l'oracle des sommes de blocs (entier) ; σ̂² ≥ 0, à une demi-unité du
        50e chiffre de N/(ℓ·n²) ; σ̂² = 0 ⇔ K ∈ {0, n}. Rougit si : paire hors grille (rang au
        lieu de position) ; M_k sans trous (n − k) ; poids ou centrage omis."""
        rnd = random.Random(20260930)
        for cas in range(120):
            w, ell = rnd.choice((60, 3600)), rnd.choice((1, 2, 3, 5, 8))
            p, pos = rnd.choice((0.0, 0.3, 0.7, 1.0)), sorted(rnd.sample(range(40), rnd.randint(1, 25)))
            s = serie([int(rnd.random() < p) for _ in pos], w, t0=rnd.randint(0, 10 ** 6), pos=pos)
            v, n, k = r1.block_long_run_variance(s, w, ell), len(s), sum(i for _, i in s)
            self.assertEqual(v["numerateur"], blocs_numerateur(s, w, ell), (cas, s, ell))
            self.assertTrue(demi_ulp(v["sigma2_bloc"], Fraction(v["numerateur"], ell * n * n)))
            self.assertGreaterEqual(v["sigma2_bloc"], 0)
            self.assertEqual(v["sigma2_bloc"] == 0, k in (0, n), (cas, s, ell))

    def test_bit_identite_deux_appels(self):
        """Deux appels sur une série trouée : sorties égales, Decimal de même str (ADR-0003) ; ℓ par
        défaut = 240. Rougit si : sortie non déterministe ou non Decimal ; ELL_BLOC ≠ 240."""
        s = serie((1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1), pos=(0, 1, 2, 4, 5, 6, 9, 10, 11, 13, 14))
        a, b = r1.block_long_run_variance(s, W), r1.block_long_run_variance(tuple(s), W)
        self.assertEqual((a, a), (b, r1.block_long_run_variance(s, W, 240)))
        for c in ("gamma0", "sigma2_bloc"):
            self.assertIs(type(a[c]), Decimal)
            self.assertEqual(str(a[c]), str(b[c]))

    def test_contrat_entree(self):
        """Contrat d'entrée (C-2) : écart w/2 ou 1,5·w, window_start dupliqué ou décroissant,
        I_t = 2, window_start non entier, w = 0, ℓ = 0 : ValueError ; série vide : n = 0, sorties
        à None. Rougit si : écart non multiple de w accepté ; doublon accepté."""
        for s, w, ell in (([(0, 1), (30, 0)], 60, 3), ([(0, 1), (90, 0)], 60, 3),
                          ([(0, 1), (0, 0)], 60, 3), ([(120, 1), (60, 0)], 60, 3), ([(0, 2)], 60, 3),
                          ([(0.0, 1)], 60, 3), ([(0, 1)], 0, 3), ([(0, 1)], 60, 0)):
            with self.assertRaises(ValueError, msg=(s, w, ell)):
                r1.block_long_run_variance(s, w, ell)
        self.assertEqual(r1.block_long_run_variance([], W),
                         {"n": 0, "K": 0, "numerateur": None, "gamma0": None, "sigma2_bloc": None})


if __name__ == "__main__":
    unittest.main()
