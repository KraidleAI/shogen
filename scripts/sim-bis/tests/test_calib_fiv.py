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
TEXTE = commun.lire_entree(PRM, "episodes", environ={}).decode("utf-8")
EP = calibration.analyser(TEXTE, K_)["episodes"]


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



class TestModeleE1(unittest.TestCase):
    def test_portee_ep_l6(self):
        """EP l.6 : segment [1 787 770 800 ; 1 790 558 880), n fixe 38 600, plage D5 [1 790 273 880, 1 790 435 280] ;
        une retouche de forme, une borne hors du pas w, un segment vide : CALIB/forme. Mutation M-10-09 (ligne non
        contrôlée)."""
        self.assertEqual(calib_fiv.portee(TEXTE, PRM["calendrier"]), {
            "t0": 1787770800, "t_fin": 1790558880, "n_fixe": 38600, "plages": [(1790273880, 1790435280)]})
        lignes = TEXTE.split(chr(10))
        for a, b in (("portée : segment", "portée : Segment"), ("1790435280)", "1790435290)"),
                     ("[1787770800 ; 1790558880)", "[1787770800 ; 1787770800)")):
            faux = chr(10).join(lignes[:5] + [lignes[5].replace(a, b, 1)] + lignes[6:])
            with self.assertRaises(commun.Refus) as c:
                calib_fiv.portee(faux, PRM["calendrier"])
            self.assertEqual(c.exception.code, "CALIB/forme", b)

    def test_calendrier_j28(self):
        """Grille de 46 468 positions du mercredi 2026-08-26 19:00 au lundi 2026-09-28 01:28 UTC (date -u -d @…) :
        calme 300 + 2 880 + 4 × 7 200 + 88 = 32 068, stress 5 × 2 880 = 14 400 ; plage D5 du jeudi 24 18:18 au
        samedi 26 15:08 inclus : 342 + 1 440 = 1 782 positions de calme et 909 de stress retirées : 30 286 et 13 491.
        Position 41 718 (1 790 273 880) retirée, 41 717 en calme ; 44 408 retirée, 44 409 en stress ; 0 en calme ; 3 180
        (samedi 29 août 00:00) en stress ; une plage hors du segment (la veille d'un samedi) ne retire rien.
        Mutations M-10-10 (plage à borne haute exclue), M-10-11 (plage ignorée), M-10-12 (premier jour partiel
        ignoré), M-10-25 (plage hors du segment non écartée)."""
        c = calib_fiv.calendrier_j28(calib_fiv.portee(TEXTE, PRM["calendrier"]), PRM["calendrier"])
        m = c["masques"]
        self.assertEqual((c["horizon"], m["calme"].bit_count(), m["stress"].bit_count()), (46468, 30286, 13491))
        lu = [("calme" if m["calme"] >> j & 1 else "stress" if m["stress"] >> j & 1 else "-")
              for j in (41718, 41717, 44408, 44409, 0, 3180, 3179)]
        self.assertEqual(lu, ["-", "calme", "-", "stress", "calme", "stress", "calme"])
        seg = {"t0": 1796428800, "t_fin": 1796428800 + 3 * 86400, "plages": [(1796342400, 1796428680)]}
        self.assertEqual(calib_fiv.calendrier_j28(seg, PRM["calendrier"]),     # samedi 2026-12-05, plage la veille
                         {"masques": {"calme": ((1 << 1440) - 1) << 2880, "stress": (1 << 2880) - 1}, "horizon": 4320})

    def test_replication(self):
        """Une réplication d'E1 (C0, puis un point à régime) : I_t égal au comptage naïf « au moins deux hôtes en
        écart », position par position, sur les positions de chaque strate ; même (cellule, i) : mêmes octets ; i
        différent : autres octets. Mutations M-10-13 (I_t à « au moins un »), M-10-14 (strate ignorée : I_t pris sur
        la grille)."""
        cal = calib_fiv.calendrier_j28(calib_fiv.portee(TEXTE, PRM["calendrier"]), PRM["calendrier"])
        for point in (None, (Fraction(1, 10), Fraction(20), 240)):
            r = calib_fiv.replication(PRM, EP, cal, point, "E1-essai", 0)
            for s, (pres, val) in r["strates"].items():
                self.assertEqual(pres, cal["masques"][s])
                naif_ = sum(1 << j for j in range(cal["horizon"])
                            if pres >> j & 1 and sum(x >> j & 1 for x in r["etats"].values()) >= 2)
                self.assertEqual(val, naif_, (point, s))
            self.assertEqual(r, calib_fiv.replication(PRM, EP, cal, point, "E1-essai", 0))
            self.assertNotEqual(r, calib_fiv.replication(PRM, EP, cal, point, "E1-essai", 1))

    def test_taux_c0_e_s_39(self):
        """E-S-39 : sous C0, sans observateur, à f = 1, la part de fenêtres de calme où binance est en écart, sur 30
        réplications, égale le taux d'EP l.15 (372/24 585, écart propre nul) à 5 erreurs-types près (variance binomiale
        majorée par un facteur 2 ; dispersion des épisodes d'EP l.16 : 476/372) ; de même quand la ligne « panne » de
        binance est vidée (EP retouché en mémoire : l'écart vient alors de F seul). Mutations M-10-15 (f = 1/2),
        M-10-23 (état réduit à la panne H)."""
        cal = calib_fiv.calendrier_j28(calib_fiv.portee(TEXTE, PRM["calendrier"]), PRM["calendrier"])
        p, calme = Fraction(372, 24585), cal["masques"]["calme"]
        e = EP["calme", "binance", "ecart"]
        self.assertEqual(p, Fraction(e["cellules"], e["n_s"]))
        sans_panne = dict(EP)
        sans_panne["calme", "binance", "panne"] = dict(EP["calme", "binance", "panne"], cellules=0)
        for ep in (EP, sans_panne):
            x = sum((calib_fiv.replication(PRM, ep, cal, None, "E1-taux", i)["etats"]["binance"] & calme).bit_count()
                    for i in range(30))
            n = calme.bit_count() * 30
            self.assertLessEqual((Fraction(x, n) - p) ** 2, 25 * 2 * p * (1 - p) / n)

    def test_regime_groupe(self):
        """Régime caché d'E-S-12 appliqué : série de binance seule, en calme, FIV(240) sur 5 réplications : sous C0,
        au plus 1,41 (épisodes courts) ; au point (φ, κ, τ_D) = (1/10, 50, 1 440), au moins 12,05 (mesuré à la mise au
        point de ce test) : le plus petit sous régime dépasse 4 fois le plus grand sous C0. Mutation M-10-21 (régime
        ignoré : C0 partout)."""
        cal = calib_fiv.calendrier_j28(calib_fiv.portee(TEXTE, PRM["calendrier"]), PRM["calendrier"])
        c = cal["masques"]["calme"]

        def fiv(point, i):
            x = calib_fiv.replication(PRM, EP, cal, point, "E1-regime", i)["etats"]["binance"] & c
            return calib_fiv.courbe(c, x, [240], K_)[0]["fiv"]
        sous_c0 = [fiv(None, i) for i in range(5)]
        sous_regime = [fiv((Fraction(1, 10), Fraction(50), 1440), i) for i in range(5)]
        self.assertGreater(min(sous_regime), 4 * max(sous_c0))

    def test_moyenne(self):
        """Trois réplications : 1, 1, 0, 0 (FIV(2) = 5/4), série nulle (indéfinie), lacune 1, 1, ·, 0, 0 (FIV(2) =
        3/2) : moyenne des définies (5/4 + 3/2)/2 = 11/8 ; une indéfinie ; aucune définie : None ; liste vide :
        FIV/entree. Mutations M-10-16 (indéfinies comptées pour 0), M-10-26 (liste vide non refusée)."""
        cs = [calib_fiv.courbe(bits(0, 1, 2, 3), bits(0, 1), [1, 2], K_),
              calib_fiv.courbe(bits(0, 1), 0, [1, 2], K_), calib_fiv.courbe(bits(0, 1, 3, 4), bits(0, 1), [1, 2], K_)]
        self.assertEqual(calib_fiv.moyenne(cs), {"fiv": [1, Fraction(11, 8)], "definies": 2, "indefinies": 1})
        self.assertEqual(calib_fiv.moyenne(cs[1:2]), {"fiv": [None, None], "definies": 0, "indefinies": 1})
        with self.assertRaises(commun.Refus) as c:
            calib_fiv.moyenne([])
        self.assertEqual(c.exception.code, "FIV/entree")

if __name__ == "__main__":
    unittest.main()
