"""Calibration E1, estimateur FIV_série SB-10a (E-S-38, E-S-39 ; T-FIV-1) : valeurs écrites à la main (série 1, 1, 0,
0 de la fixture de PLAN-S2BIS, scripts/plan-s2bis/tests/test_episodes.py l.36-44 ; série à lacune), chaînes d'EP
l.128 (γ̂₀ et σ̂²_bloc à ℓ = 1 ne dépendent que de n et K), et comptage naïf des γ̂_k depuis leur définition (paires de
la grille, écarts à Ī, en Fraction) sur des séries aléatoires à lacunes ; chaque test nomme les mutations qui le
rougissent."""
import functools
import hashlib
import random
import unittest
from decimal import Decimal
from fractions import Fraction

import calib_fiv
import calibration
import commun
import sources

PRM = commun.charger_parametres(environ={})
K_ = PRM["calibration"]
TEXTE = commun.lire_entree(PRM, "episodes", environ={}).decode("utf-8")
EP = calibration.analyser(TEXTE, K_)["episodes"]


def bits(*positions):
    return sum(1 << p for p in positions)


@functools.lru_cache(maxsize=None)
def cal_e1():
    """Calendrier d'E1 (point (3) de l'ajout daté du G0 du 2026-10-05 15:05:43 UTC) : génération sur la portée d'EP l.6
    hors D5, positions présentes = masque mesuré de PLAN-S2BIS-2 ; lu une fois (jamais modifié par les tests)."""
    return calib_fiv.calendrier_e1(PRM, environ={})


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
        une retouche de forme, une borne hors du pas w, un segment vide, un t0 répété différent du début du segment
        (1 787 770 860, multiple de w, ligne canonique : C-2 de la G2 de la tranche 4) : CALIB/forme. Mutations M-10-09
        (ligne non contrôlée), R-06 du réviseur (t0 répété non contrôlé)."""
        self.assertEqual(calib_fiv.portee(TEXTE, PRM["calendrier"]), {
            "t0": 1787770800, "t_fin": 1790558880, "n_fixe": 38600, "plages": [(1790273880, 1790435280)]})
        lignes = TEXTE.split(chr(10))
        for a, b in (("portée : segment", "portée : Segment"), ("1790435280)", "1790435290)"),
                     ("[1787770800 ; 1790558880)", "[1787770800 ; 1787770800)"),
                     ("(t0 = 1787770800,", "(t0 = 1787770860,")):
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
        écart », position par position, sur les positions présentes de chaque strate (masque mesuré, point (3)) ;
        même (cellule, i) : mêmes octets ; i différent : autres octets. Mutations M-10-13 (I_t à « au moins un »),
        M-10-14 (strate ignorée : I_t pris sur la grille), M-15C-01 (positions générées au lieu du masque)."""
        cal = cal_e1()
        for point in (None, (Fraction(1, 10), Fraction(20), 240)):
            r = calib_fiv.replication(PRM, EP, cal, point, "E1-essai", 0)
            for s, (pres, val) in r["strates"].items():
                self.assertTrue(pres == cal["presentes"][s], s)          # masques de 46 468 bits : message court
                naif_ = sum(1 << j for j in range(cal["horizon"])
                            if pres >> j & 1 and sum(x >> j & 1 for x in r["etats"].values()) >= 2)
                self.assertEqual(val, naif_, (point, s))
            self.assertEqual(r, calib_fiv.replication(PRM, EP, cal, point, "E1-essai", 0))
            self.assertNotEqual(r, calib_fiv.replication(PRM, EP, cal, point, "E1-essai", 1))

    def test_composition_e1(self):
        """C-1 de la G2 de la tranche 4 (E-S-03, E-S-38 ; Q-T4-13) : composition du fond d'E1 écrite dans
        parametres.json (e1.fond, avec sa source) et lue par replication : f = 1, part des pannes longues 0, autres 1,
        hors-enveloppe 0, classe BTC (rang 0 de sources.CLASSES). États égaux, hôte par hôte, à ceux de
        sources.Replication sous ce fond écrit à la main (ni dérive, ni incident, ni unité faible) ; chaque retouche de
        e1.fond (f = 1/2, longues 1/2, hors-enveloppe 1/4 000, classe USDC, classe ETH à autres 2) donne les états du
        fond retouché écrit de même, autres que ceux du fond scellé ; classe inconnue : E1/classe. Mutations R-02 et
        R-03 du réviseur, transposées dans parametres.json et dans le code, M-14C-01 à M-14C-07."""
        e = PRM["e1"].get("fond", {})
        self.assertEqual({k: v for k, v in e.items() if k != "source"},
                         {"f": [1, 1], "longues": [0, 1], "autres": [1, 1], "hors_enveloppe": [0, 1], "classe": "BTC"})
        self.assertTrue(all(x in e["source"] for x in ("E-S-38", "PROPOSITION l.197", "Q-T4-13")), e["source"])
        cal = cal_e1()
        main = {"f": Fraction(1), "longues": Fraction(0), "autres": Fraction(1), "hors_enveloppe": Fraction(0)}

        def attendu(prm, point, fond, c):
            rep = sources.Replication(prm, EP, dict(fond, regime={s: point for s in cal["masques"]}), "E1-fond", 0,
                                      cal["masques"], cal["horizon"])
            return {h: rep.pannes(h) | rep.ecarts(h, c) for h in prm["sources"]["classes"][sources.CLASSES[c]]}

        def diff(a, b):
            """Hôtes dont l'état diffère, clés comprises (message court : masques de 46 468 bits)."""
            return sorted(h for h in set(a) | set(b) if a.get(h) != b.get(h))
        point = (Fraction(1, 10), Fraction(20), 240)
        r = calib_fiv.replication(PRM, EP, cal, point, "E1-fond", 0)["etats"]
        self.assertEqual(diff(r, attendu(PRM, point, main, 0)), [])
        scelle = attendu(PRM, None, main, 0)
        for cle, v, fond, c in (("f", [1, 2], dict(main, f=Fraction(1, 2)), 0),
                                ("longues", [1, 2], dict(main, longues=Fraction(1, 2)), 0),
                                ("hors_enveloppe", [1, 4000], dict(main, hors_enveloppe=Fraction(1, 4000)), 0),
                                ("classe", "USDC", main, 2), ("classe", "ETH", dict(main, autres=Fraction(2)), 1)):
            prm = dict(PRM, e1=dict(PRM["e1"], fond=dict(e, **{cle: v}, **({"autres": [2, 1]} if v == "ETH" else {}))))
            x = attendu(prm, None, fond, c)
            self.assertNotEqual(diff(x, scelle), [], (cle, v))
            self.assertEqual(diff(calib_fiv.replication(prm, EP, cal, None, "E1-fond", 0)["etats"], x), [], (cle, v))
        with self.assertRaises(commun.Refus) as r:
            calib_fiv.replication(dict(PRM, e1=dict(PRM["e1"], fond=dict(e, classe="XRP"))), EP, cal, None, "E1-x", 0)
        self.assertEqual(r.exception.code, "E1/classe")

    def test_taux_c0_e_s_39(self):
        """E-S-39 : sous C0, sans observateur, à f = 1, la part de fenêtres de calme où binance est en écart, sur 30
        réplications, égale le taux d'EP l.15 (372/24 585, écart propre nul) à 5 erreurs-types près (variance binomiale
        majorée par un facteur 2 ; dispersion des épisodes d'EP l.16 : 476/372) ; de même quand la ligne « panne » de
        binance est vidée (EP retouché en mémoire : l'écart vient alors de F seul). Mutations M-10-15 (f = 1/2),
        M-10-23 (état réduit à la panne H)."""
        cal = cal_e1()
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
        cal = cal_e1()
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


T = 1796428560                                     # vendredi 2026-12-04 23:56 UTC (date -u -d @1796428560)
SEG = {"t0": T, "t_fin": T + 480, "n_fixe": 8, "plages": [(T + 360, T + 360)]}       # j 0-3 vendredi, 4-7 samedi
L5 = "  lacune j = 5 à 6 : 2 positions (calme 0, stress 2)"


def differents(a: dict, b: dict) -> list:
    """Clés dont les valeurs diffèrent, clés absentes comprises (message court : masques de 46 468 bits)."""
    return sorted(k for k in set(a) | set(b) if a.get(k) != b.get(k))


def masque_fictif(*remplacements) -> str:
    """masque_j28.txt fictif écrit à la main sur SEG (forme de scripts/plan-s2bis-2/masque_fiv.py) : D5 = j 6,
    lacunes j 1 et j 5-6, chaîne c-ccs--s (printf | sha256sum : 51633e11…) ; chaque (avant, après) remplacé."""
    t = chr(10).join([
        "préparation de S2-bis ; ne change pas le verdict de S2 (« R1 discrimine » = FAUX)", "en-tête du lot",
        "[MASQUE J28] positions j = (ws − t0)/w de la portée ; strate par jour UTC ; retenue = fenêtre retenue de la "
        "strate", f"  portée : t0 = {T} ; t_fin = {T + 480} ; positions = 8 ; plage D5 : j = 6 à 6 (1 positions)",
        "  « calme » : calendrier hors D5 = 4 ; retenues = 3 ; sautées hors D5 = 1",
        "  « stress » : calendrier hors D5 = 3 ; retenues = 2 ; sautées hors D5 = 1",
        "  contrôle : retenues = n du bloc 3 ; sautées = ADR-0029 l.31 ; strate de chaque retenue = calendrier : égaux",
        "  empreinte : sha256 de la chaîne de 8 caractères (c calme retenue, s stress retenue, - non retenue) = "
        "51633e111ca9087deff66039169933974ac07c1c88b85672d6e474a33b14c0b3",
        "  lacunes : 2 suites maximales de positions non retenues, plage D5 comprise, en ordre croissant",
        "  lacune j = 1 à 1 : 1 positions (calme 1, stress 0)", L5, ""])
    for a, b in remplacements:
        assert t.count(a) == 1, a
        t = t.replace(a, b)
    return t


class TestMasqueE1(unittest.TestCase):
    def test_masque_fictif(self):
        """Point (3) : masque relu sur la fixture : présentes calme j 0, 2, 3 et stress j 4, 7 ; génération (portée
        hors D5) inchangée : calme j 0-3, stress j 4, 5, 7 ; mêmes présentes sans plage exclue (« aucune ») et avec une
        plage hors de la portée (« aucune position »), stress hors D5 = 4. Mutations M-15B-01 (lacune comptée
        retenue), M-15B-02 (strate par la mauvaise initiale), M-15B-10 (comptes des lacunes hors D5)."""
        cal = PRM["calendrier"]
        self.assertEqual(calib_fiv.masque_j28(masque_fictif(), SEG, cal),
                         {"calme": bits(0, 2, 3), "stress": bits(4, 7)})
        for seg, d5 in ((dict(SEG, plages=[]), "aucune"), (dict(SEG, plages=[(T - 600, T - 540)]), "aucune position")):
            texte = masque_fictif(("j = 6 à 6 (1 positions)", d5), ("3 ; retenues = 2 ; sautées hors D5 = 1",
                                                                    "4 ; retenues = 2 ; sautées hors D5 = 2"))
            self.assertEqual(calib_fiv.masque_j28(texte, seg, cal), {"calme": bits(0, 2, 3), "stress": bits(4, 7)}, d5)
        self.assertEqual(calib_fiv.calendrier_j28(SEG, cal)["masques"],
                         {"calme": bits(0, 1, 2, 3), "stress": bits(4, 5, 7)})

    def test_masque_refus(self):
        """Chaque retouche de la fixture : E1/masque. Empreinte, retenues, plage D5, nombre de lacunes, comptes d'une
        lacune, t_fin, étiquette, section absente ; lacune coupée en deux (chaîne et empreinte inchangées, suites non
        maximales) ; lacunes désordonnées ; ligne de lacune illisible ; saut de ligne final absent, ligne en trop ;
        j 6 (D5) retenue, empreinte f5fe5be6… de c-ccs-ss et comptes cohérents ; lacune j 5 à 8, hors de la grille de
        8 positions, empreinte 38523657… de c-ccs--- et comptes cohérents. Mutations M-15B-03 à M-15B-07, M-15B-11."""
        f5 = "f5fe5be6f79cb00b34d28d1cb77d4cf9cb4899130c6fdf1deb2d2b790ca382ab"     # printf '%s' c-ccs-ss | sha256sum
        l55, l66 = ("  lacune j = 5 à 5 : 1 positions (calme 0, stress 1)",
                    "  lacune j = 6 à 6 : 1 positions (calme 0, stress 1)")
        l1, nl = "  lacune j = 1 à 1 : 1 positions (calme 1, stress 0)", chr(10)
        cas = [[("= 51633e", "= 51633f")], [("retenues = 3", "retenues = 4")], [("j = 6 à 6 (1", "j = 5 à 6 (2")],
               [("lacunes : 2", "lacunes : 3")], [("(calme 0, stress 2)", "(calme 1, stress 1)")],
               [(f"t_fin = {T + 480}", f"t_fin = {T + 540}")], [("= FAUX)", "= VRAI)")],
               [("[MASQUE J28]", "[MASQUE]")], [("lacunes : 2", "lacunes : 3"), (L5, l55 + nl + l66)],
               [(l1 + nl + L5, L5 + nl + l1)], [("j = 1 à 1 :", "j = 1 :")], [("stress 2)" + nl, "stress 2)")],
               [("stress 2)" + nl, "stress 2)" + nl + "fin" + nl)],
               [(L5, l55), ("= 51633e111ca9087deff66039169933974ac07c1c88b85672d6e474a33b14c0b3", "= " + f5),
                ("3 ; retenues = 2 ; sautées hors D5 = 1", "3 ; retenues = 3 ; sautées hors D5 = 0")],
               [(L5, "  lacune j = 5 à 8 : 4 positions (calme 0, stress 3)"),
                ("= 51633e111ca9087deff66039169933974ac07c1c88b85672d6e474a33b14c0b3",
                 "= 385236576d42550fda9651c6cca5599046c25e5c0e97d00ef620eb48e28c4651"),
                ("3 ; retenues = 2 ; sautées hors D5 = 1", "3 ; retenues = 1 ; sautées hors D5 = 2")]]
        for c in cas:
            with self.assertRaises(commun.Refus) as r:
                calib_fiv.masque_j28(masque_fictif(*c), SEG, PRM["calendrier"])
            self.assertEqual(r.exception.code, "E1/masque", c)

    def test_masque_reel(self):
        """masque_j28.txt versé, sous ses deux épingles : 46 468 positions ; présentes calme 24 585 et stress 11 397
        (n de l'en-tête du masque et n_s d'EP) ; génération sur la portée hors D5 : 30 286 et 13 491 ; positions
        relevées par un oracle hors dépôt (datetime, lacunes lues par découpage de texte) : j 0 c, 1550 -, 3180 s,
        4320 -, 6871 -, 6872 c, 41717 c, 41718 -, 44408 -, 44409 s, 46467 c ; chaîne c/s/- recalculée ici : sha256
        670dc46e… (ligne du fichier) ; présentes incluses dans la génération ; fichiers lus inscrits. Mutations
        M-15B-08 (masque non relu : présentes = génération), M-15B-09 (lu sous les sommes de PLAN-S2BIS)."""
        lus = {}
        cal = calib_fiv.calendrier_e1(PRM, lus, environ={})
        p, g = cal["presentes"], cal["masques"]
        self.assertEqual((cal["horizon"], p["calme"].bit_count(), p["stress"].bit_count(), g["calme"].bit_count(),
                          g["stress"].bit_count()), (46468, 24585, 11397, 30286, 13491))
        bc, bs = (format(p[s], "b")[::-1].ljust(46468, "0") for s in ("calme", "stress"))
        ch = "".join("c" if x == "1" else "s" if y == "1" else "-" for x, y in zip(bc, bs))
        self.assertEqual("".join(ch[j] for j in (0, 1550, 3180, 4320, 6871, 6872, 41717, 41718, 44408, 44409, 46467)),
                         "c-s--cc--sc")
        self.assertEqual(hashlib.sha256(ch.encode("ascii")).hexdigest(),
                         "670dc46eae832264875af8fdb5a586896750e0d7a78f04e28b4dae3cabe3a37f")
        self.assertEqual([(p[s] & ~g[s]).bit_count() for s in p], [0, 0])
        d = "docs/adr-0029/plan-s2bis"
        self.assertEqual(sorted(lus), [f"{d}-2/SHA256SUMS", f"{d}-2/masque_j28.txt", f"{d}/SHA256SUMS",
                                       f"{d}/episodes.txt"])

    def test_masque_apres_generation(self):
        """Point (3), à vérifier par la G2 : le masque s'applique après la génération. États D*(u) égaux à ceux d'une
        génération dont les positions présentes sont les positions générées ; I_t et séries des hôtes rendues = cette
        génération restreinte au masque, strate par strate ; masque et positions générées donnent des I_t différents.
        Mutation M-15C-02 (génération sur le masque)."""
        cal, point = cal_e1(), (Fraction(1, 10), Fraction(20), 240)
        r = calib_fiv.replication(PRM, EP, cal, point, "E1-masque", 0)
        g = calib_fiv.replication(PRM, EP, dict(cal, presentes=cal["masques"]), point, "E1-masque", 0)
        self.assertEqual(differents(r["etats"], g["etats"]), [])
        for s, m in cal["presentes"].items():
            self.assertTrue(r["strates"][s] == (m, g["strates"][s][1] & m), s)
            self.assertEqual(differents(r["unites"][s], {h: d & m for h, d in g["etats"].items()}), [], s)
        self.assertTrue(r["strates"] != g["strates"])

    def test_replication_refus_masque(self):
        """Calendrier sans positions présentes, ou présentes hors des positions générées de leur strate (j 6, dans
        D5 ; strate inconnue de la génération) : E1/masque, avant toute génération. Mutations M-15C-03 (inclusion non
        contrôlée), M-15C-04 (présentes absentes remplacées par les positions générées), M-15C-09 (strate inconnue
        admise)."""
        cal = calib_fiv.calendrier_j28(SEG, PRM["calendrier"])
        for faux in (cal, dict(cal, presentes={"calme": bits(0), "stress": bits(4, 6)}),
                     dict(cal, presentes={"calme": bits(0), "autre": bits(0)})):
            with self.assertRaises(commun.Refus) as r:
                calib_fiv.replication(PRM, EP, faux, None, "E1-refus", 0)
            self.assertEqual(r.exception.code, "E1/masque")
        ok = dict(cal, presentes={"calme": bits(0), "stress": bits(4, 7)})
        r = calib_fiv.replication(PRM, EP, ok, None, "E1-x", 0)
        self.assertEqual(sorted((s, x[0]) for s, x in r["strates"].items()), [("calme", 1), ("stress", bits(4, 7))])


L22 = Decimal("0.480453013918201424667102526326664971730552951594545586866864")     # bc -l : l(2)^2, scale = 60
EPS = Decimal("1E-45")
P1, P2, P3, P4 = ((Fraction(1, 100), Fraction(5), 60), (Fraction(1, 100), Fraction(50), 60),
                  (Fraction(1, 10), Fraction(5), 60), (Fraction(1, 10), Fraction(50), 60))


def reduit():
    """parametres.json à grille réduite (φ ∈ {1/100, 1/10}, κ ∈ {5, 50}, τ_D = 60) et ℓ ∈ {1, 2, 240}."""
    e1 = dict(PRM["e1"], phi=[[1, 100], [1, 10]], kappa=[5, 50], tau_D=[60])
    return dict(PRM, e1=e1, calibration=dict(K_, ell=[1, 2, 240]))


def m(*fiv):
    return {"fiv": [None if x is None else Fraction(x) for x in fiv], "definies": 1, "indefinies": 0}


def cible3():
    """Cible EP fictive : 1 et 2 à ℓ = 1 et 2 (gardés), 8 à ℓ = 240 (non gardé)."""
    return [{"ell": e, "fiv": Fraction(x), "garde": g} for e, x, g in ((1, 1, True), (2, 2, True), (240, 8, False))]


def fu(*fiv):
    """Points fictifs de fiv_unites.txt aux ℓ 1, 2, 240 (garde tenue aux deux premiers) ; None : F_u indéfini."""
    return [{"ell": e, "fiv": None if x is None else Fraction(x), "garde": e < 240} for e, x in zip((1, 2, 240), fiv)]


UNITES = {"calme": {"a": fu(1, 2, 4), "b": fu(1, 3, 9), "c": fu(None, None, None)}}     # c : K ∈ {0, n}, écarté


def par_hote(**moy):
    """moyennes_u fictives d'une strate : {point : {"calme" : {hôte : m(…)}}} ; points absents : a, b et c parfaits."""
    parfait = {"a": m(1, 2, 4), "b": m(1, 3, 9), "c": m(1, 1, 1)}
    return {p: {"calme": dict(parfait, **moy.get(n, {}))} for n, p in (("P1", P1), ("P2", P2), ("P3", P3), ("P4", P4))}


def choisir(prm, cible, moy, unites=None, moyennes_u=None):
    """selection sur une strate « calme » ; unités par défaut UNITES et par_hote() (Q₁ nul partout)."""
    return calib_fiv.selection(prm, {"calme": cible}, {p: {"calme": x} for p, x in moy.items()},
                               UNITES if unites is None else unites, par_hote() if moyennes_u is None else moyennes_u)


class TestCritereE1(unittest.TestCase):
    def test_parametres_e1(self):
        """Section « e1 » : grille φ × κ × τ_D de 64 points dans l'ordre déclaré, 200 réplications par point, pool
        D1-bis (cible EP l.128-161) ; e1.ell_c1 retiré (point (7) de l'ajout daté du G0 du 2026-10-05 15:05:43 UTC) ;
        source citée, masque (point (3)), règle de C1 (point (1)) et retrait (point (7)) compris ; cellules E1-C0-v2
        et E1-<num>_<den>-<κ>-<τ_D>, φ = num/den irréductible (Q-T4-8, forme modifiée par l'avis, AVIS-SIM-T4.md
        l.56-59 : aucun « / », le nom de cellule nommant aussi les fichiers partiels de calcul, E-S-45) : 65 noms
        distincts, aucun « / ». Mutations
        M-10-28 (grille sans τ_D = 4 320), M-10-29 (cellule sans φ), M-14C-08 (« / » remis), M-14C-09 (séparateur
        « - »), M-14G-01 (E1-C0 rétabli), M-15E-12 (ell_c1 rétabli, schéma compris)."""
        g = calib_fiv.grille(PRM)
        self.assertEqual((len(g), g[0], g[1], g[-1]), (64, (Fraction(1, 100), 5, 60), (Fraction(1, 100), 5, 240),
                                                        (Fraction(1, 10), 50, 4320)))
        e = PRM["e1"]
        self.assertEqual((e["replications"], e["pool"], "ell_c1" in e, "ell_c1" in commun.SCHEMA["e1"]),
                         (200, "D1-bis", False, False))
        self.assertTrue(all(x in e["source"] for x in ("E-S-38", "PROPOSITION l.197", "AVIS.md l.24", "point (1)",
                                                       "point (7)", "point (3)")))
        self.assertEqual([calib_fiv.cellule(PRM, x) for x in (None, P1, (Fraction(1, 20), Fraction(10), 4320),
                                                              (Fraction(2, 100), Fraction(5), 240))],
                         ["E1-C0-v2", "E1-1_100-5-60", "E1-1_20-10-4320", "E1-1_50-5-240"])
        noms = [calib_fiv.cellule(PRM, x) for x in [None] + g]
        self.assertEqual((len(set(noms)), [x for x in noms if "/" in x]), (65, []))

    def test_cellule_c0_renommee(self):
        """Décision de l'orchestrateur du 2026-10-05 sur l'item C-3 des corrections G2 de la tranche 4, avant E0 : la
        cellule de C0 s'appelle « E1-C0-v2 », nom jamais employé, et plus aucun nom d'E1 n'est « E1-C0 » (E-4 : valeurs
        de E1-C0 i = 0..9 possiblement vues en mise au point, 2026-10-05) ; le nom et ce motif sont écrits dans
        e1.questions (Q-T4-8). Mutations M-14G-01 (E1-C0 rétabli dans cellule), M-14G-02 (E1-C0 rétabli dans Q-T4-8),
        M-14G-03 (motif retiré)."""
        noms = [calib_fiv.cellule(PRM, x) for x in [None] + calib_fiv.grille(PRM)]
        self.assertEqual((noms[0], "E1-C0" in noms), ("E1-C0-v2", False))
        q = PRM["e1"]["questions"]["Q-T4-8"]
        self.assertEqual([x in q for x in ("cellules « E1-C0-v2 » pour C0",
                                           "E-4 : valeurs de E1-C0 i = 0..9 possiblement vues en mise au point, "
                                           "2026-10-05")], [True, True])

    def test_critere(self):
        """Somme des carrés des écarts de log aux ℓ dont la garde d'EP est tenue : modèle 2, 4, 1 contre cible 1, 2, 1
        (troisième ℓ non gardé) : 2·(ln 2)² ; modèle 3, 5, 7 contre 2, 3, 100 : (ln 3 − ln 2)² + (ln 5 − ln 3)² (bc -l,
        à 10^-45 près) ; FIV indéfini à un ℓ gardé : None, à un ℓ non gardé : sans effet ; ℓ ou longueurs
        discordants : E1/cible. Mutations M-10-30 (ℓ non gardés comptés), M-10-31 (écarts sans le carré), M-10-32 (log
        décimal), M-10-41 (alignement des ℓ non contrôlé)."""
        ctx = calib_fiv.contexte(K_)
        cible = [{"ell": e, "fiv": Fraction(x), "garde": g}
                 for e, x, g in ((1, 1, True), (2, 2, True), (240, 1, False))]
        ells = [1, 2, 240]
        ref = Decimal("0.960906027836402849334205052653329943461105903189091173733728")      # bc -l : 2*l(2)^2
        self.assertLess(abs(calib_fiv.critere([2, 4, 1], cible, ells, ctx) - ref), EPS)
        cible2 = [dict(c, fiv=Fraction(x)) for c, x in zip(cible, (2, 3, 100))]
        ref = Decimal("0.425344771789078895160682693819873579225181410410195394238949")
        self.assertLess(abs(calib_fiv.critere([3, 5, 7], cible2, ells, ctx) - ref), EPS)
        self.assertIsNone(calib_fiv.critere([2, None, 1], cible, ells, ctx))
        self.assertEqual(calib_fiv.critere([1, 2, None], cible, ells, ctx), 0)
        for modele, c, e in (([1, 2], cible, ells), ([1, 2, 1], cible[:2], ells), ([1, 2, 1], cible, [1, 2, 120])):
            with self.assertRaises(commun.Refus) as r:
                calib_fiv.critere(modele, c, e, ctx)
            self.assertEqual(r.exception.code, "E1/cible")

    def test_selection(self):
        """C2 (E-S-38, inchangé) : grille réduite, cible EP fictive 1, 2 (gardés), 8 (non gardé) ; C0 : 1, 1, 1. P1
        (1/100, 5, 60) : 1, 2, 4, critère 0 ; P2 (1/100, 50, 60) : 1, 2, 2, critère 0 ; P3 (1/10, 5, 60) : 1, 4, 3 ; P4
        (1/10, 50, 60) : 1, 1, 1. C2 : égalité P1, P2 départagée par le plus petit κ : P1. Critère de P3 : (ln 2)²
        (bc -l). Résidus de C2 : 0, 0. P1 à FIV indéfini à un ℓ gardé : écarté, C2 = P2 ; point manquant : E1/point ;
        aucun critère défini : E1/indefini ; FIV(240) de C0 indéfini : sans effet (C0 n'entre plus dans C1). Mutations
        M-10-33 (C2 au plus grand critère), M-10-34 (égalités au plus grand κ), M-10-36 (point indéfini compté pour
        0)."""
        moy = {None: m(1, 1, 1), P1: m(1, 2, 4), P2: m(1, 2, 2), P3: m(1, 4, 3), P4: m(1, 1, 1)}
        s = choisir(reduit(), cible3(), moy)["calme"]
        self.assertEqual((s["C2"], s["residus"]), (P1, [0, 0]))
        self.assertLess(abs(s["criteres"][P3] - L22), EPS)
        moy[P1], moy[None] = m(1, None, 4), m(1, 1, None)
        s = choisir(reduit(), cible3(), moy)["calme"]
        self.assertEqual((s["C2"], s["criteres"][P1]), (P2, None))
        for faux, code in (({p: x for p, x in moy.items() if p != P4}, "E1/point"),
                           ({p: m(1, None, 1) if p else x for p, x in moy.items()}, "E1/indefini")):
            with self.assertRaises(commun.Refus) as c:
                choisir(reduit(), cible3(), faux)
            self.assertEqual(c.exception.code, code)

    def test_egalites_kappa_puis_tau_d(self):
        """C-2 de la G2 de la tranche 4, lettre d'E-S-38 : égalités départagées par le plus petit κ, puis le plus petit
        τ_D, φ en dernier (Q-T4-9). Grille φ ∈ {1/100, 1/10}, κ ∈ {5, 50}, τ_D ∈ {60, 240} ; cible 1, 2 (gardés), 8
        (non gardé) ; points à 1, 4, 1 (critère (ln 2)²), sauf deux à 1, 2, 1 (critère 0) : (1/100, 5, 240) et
        (1/10, 5, 60), à κ égal : C2 = (1/10, 5, 60), τ_D avant φ ; (1/100, 5, 240) et (1/100, 50, 60) : C2 =
        (1/100, 5, 240), κ avant τ_D. Mutations R-04 du réviseur (φ avant τ_D), M-14D-04 (τ_D avant κ)."""
        prm = dict(PRM, e1=dict(PRM["e1"], phi=[[1, 100], [1, 10]], kappa=[5, 50], tau_D=[60, 240]),
                   calibration=dict(K_, ell=[1, 2, 240]))
        cible = cible3()
        f, t = Fraction, (Fraction(1, 100), Fraction(5), 240)
        for autre, c2 in (((f(1, 10), f(5), 60), (f(1, 10), f(5), 60)), ((f(1, 100), f(50), 60), t)):
            moy = {p: m(1, 2, 1) if p in (t, autre) else m(1, 4, 1) for p in calib_fiv.grille(prm)}
            moy[None] = m(1, 1, 1)
            u = {p: {"calme": {h: m(*(x["fiv"] for x in xs)) for h, xs in UNITES["calme"].items()}}
                 for p in calib_fiv.grille(prm)}
            s = choisir(prm, cible, moy, moyennes_u=u)["calme"]
            self.assertEqual((s["criteres"][t], s["criteres"][autre], s["C2"]), (0, 0, c2))

    def test_q1(self):
        """Point (1) : Q₁ = Σ_u Σ_ℓ (ln F̄_u − ln F_u)² aux ℓ gardés et aux hôtes à F_u défini (c écarté, sans effet de
        son modèle) : modèle a = 2, 4, 1 contre 1, 2, 4 ; b = 3, 3, 100 contre 1, 3, 9 : 2(ln 2)² + (ln 3)² (bc -l, à
        10^-45 près) ; F̄ indéfini à ℓ = 240 (non gardé) : sans effet ; à ℓ = 2 (gardé) : None ; hôte de la cible sans
        moyenne : E1/unite ; ℓ discordants : E1/cible. Mutations M-15E-01 (F_u indéfini retenu), M-15E-02 (somme
        réduite au dernier hôte), M-15E-03 (ℓ non gardés comptés)."""
        ctx, ells = calib_fiv.contexte(K_), [1, 2, 240]
        ref = Decimal("2.167854988648984827177984176502695857079569249818313158550455")   # 2*l(2)^2 + l(3)^2
        moy = {"a": m(2, 4, 1), "b": m(3, 3, 100), "c": m(None, 7, None)}
        self.assertLess(abs(calib_fiv.q1(moy, UNITES["calme"], ells, ctx) - ref), EPS)
        self.assertLess(abs(calib_fiv.q1(dict(moy, b=m(3, 3, None)), UNITES["calme"], ells, ctx) - ref), EPS)
        self.assertIsNone(calib_fiv.q1(dict(moy, a=m(2, None, 1)), UNITES["calme"], ells, ctx))
        for faux, e, code in (({"a": moy["a"], "c": moy["c"]}, ells, "E1/unite"), (moy, [1, 2, 120], "E1/cible")):
            with self.assertRaises(commun.Refus) as r:
                calib_fiv.q1(faux, UNITES["calme"], e, ctx)
            self.assertEqual(r.exception.code, code)

    def test_c1_par_q1(self):
        """Point (1) : C1 = point de Q₁ minimal. a, b parfaits (Q₁ nul) sauf : P1 a = 1, 4 ((ln 2)²) ; P3 b indéfini à
        ℓ = 2 (écarté) ; P4 a = 2, 2 ((ln 2)²) : C1 = P2 ; Q₁ imprimés (P3 : None). P1 parfait aussi : égalité P1, P2,
        plus petit κ : P1 ; P2 et P3 seuls parfaits (P1, P4 à (ln 2)²) : plus petit κ, φ de P3 plus grand : P3.
        Mutations M-15E-04 (C1 au plus grand Q₁), M-15E-05 (point écarté compté sans l'hôte indéfini), M-15E-06
        (égalités de C1 au plus petit φ d'abord)."""
        moy = {p: m(1, 2, 8) for p in (None, P1, P2, P3, P4)}
        u = par_hote(P1={"a": m(1, 4, 4)}, P3={"b": m(1, None, 9)}, P4={"a": m(2, 2, 4)})
        s = choisir(reduit(), cible3(), moy, moyennes_u=u)["calme"]
        self.assertEqual((s["C1"], s["Q1"][P2], s["Q1"][P3]), (P2, 0, None))
        self.assertLess(abs(s["Q1"][P1] - L22), EPS)
        u = par_hote(P3={"b": m(1, None, 9)}, P4={"a": m(2, 2, 4)})
        self.assertEqual(choisir(reduit(), cible3(), moy, moyennes_u=u)["calme"]["C1"], P1)
        u = par_hote(P1={"a": m(1, 4, 4)}, P4={"a": m(2, 2, 4)})
        self.assertEqual(choisir(reduit(), cible3(), moy, moyennes_u=u)["calme"]["C1"], P3)

    def test_c1_independant_de_c0_et_c2(self):
        """Point (1), convention du milieu des logs de C0 et de C2 retirée : C1 ne dépend ni de C0 ni de la courbe de
        I_t. Mêmes moyennes par hôte (C1 = P2) ; C2 = P1, puis P4, C0 à 1 puis à 1 000 en ℓ = 240 : C1 = P2 chaque
        fois, différent de C2. Mutations M-15E-07 (C1 = C2), M-15E-08 (C1 sur les courbes de I_t)."""
        u = par_hote(P1={"a": m(1, 4, 4)}, P3={"b": m(1, None, 9)}, P4={"a": m(2, 2, 4)})
        for c2, c0 in ((P1, 1), (P4, 1), (P1, 1000)):
            moy = {p: m(1, 2, 8) if p == c2 else m(2, 4, 8) for p in (P1, P2, P3, P4)}
            moy[None] = m(1, 1, c0)
            s = choisir(reduit(), cible3(), moy, moyennes_u=u)["calme"]
            self.assertEqual((s["C2"], s["C1"]), (c2, P2))

    def test_selection_refus_nommes(self):
        """C-2 et O-7 de la G2 de la tranche 4, étendus au point (1) : C0 absent des moyennes : E1/point ; strate de la
        cible sans courbe, pour un point ou pour C0, sans FIV_u, ou sans moyennes par hôte pour un point : E1/strate ;
        hôte de fiv_unites.txt sans moyenne : E1/unite ; tous les points à Q₁ indéfini, ou aucun (u, ℓ) retenu (F_u
        tous indéfinis) : E1/indefini ; jamais une erreur non nommée (KeyError, ValueError) ; entrée complète à deux
        strates : aucun refus. Mutations R-07 du réviseur (C0 non contrôlé), M-14D-01 à M-14D-03, M-15E-09 (strate
        des moyennes par hôte non contrôlée), M-15E-10 (aucun (u, ℓ) retenu admis), M-15E-11 (aucun Q₁ défini
        admis)."""
        def code_de(cible, moy, unites, mu):
            try:
                calib_fiv.selection(reduit(), cible, moy, unites, mu)
            except commun.Refus as e:
                return e.code
            except (KeyError, ValueError, IndexError) as e:
                return type(e).__name__
            return None
        cible, mu1 = {"calme": cible3(), "stress": cible3()}, par_hote()
        deux = {p: {"calme": x, "stress": x} for p, x in
                {None: m(1, 1, 1), P1: m(1, 2, 4), P2: m(1, 2, 2), P3: m(1, 4, 3), P4: m(1, 1, 1)}.items()}
        u2, mu2 = dict(UNITES, stress=UNITES["calme"]), {p: dict(x, stress=x["calme"]) for p, x in mu1.items()}
        tous = {p: {s: dict(x["calme"], b=m(1, None, 9)) for s in ("calme", "stress")} for p, x in mu1.items()}
        vide = {s: {"c": fu(None, None, None)} for s in ("calme", "stress")}
        cas = [({p: x for p, x in deux.items() if p is not None}, u2, mu2, "E1/point"),
               ({**deux, P3: {"calme": deux[P3]["calme"]}}, u2, mu2, "E1/strate"),
               ({**deux, None: {"stress": deux[None]["stress"]}}, u2, mu2, "E1/strate"),
               (deux, UNITES, mu2, "E1/strate"), (deux, u2, {**mu2, P4: mu1[P4]}, "E1/strate"),
               (deux, u2, {**mu2, P2: {s: {"a": m(1, 2, 4)} for s in ("calme", "stress")}}, "E1/unite"),
               (deux, u2, tous, "E1/indefini"), (deux, vide, mu2, "E1/indefini"), (deux, u2, mu2, None)]
        self.assertEqual([code_de(cible, x, u, mu) for x, u, mu, _c in cas], [c for _x, _u, _mu, c in cas])

    def test_c1_egalites_grille_scellee(self):
        """C-1 de la G2 de SIM-INTEG : départage de C1 sur la grille scellée (les 64 points de e1), Q₁ nul à deux
        points seulement, (ln 2)² ailleurs ; le premier de chaque paire gagne : (1/100, 5, 4 320) contre (1/100, 50,
        60), plus petit κ d'abord ; (1/10, 5, 60) contre (1/100, 5, 240), plus petit τ_D avant φ ; (1/100, 20, 240)
        contre (1/20, 20, 240), plus petit φ en dernier. Mutations MR-03 (τ_D avant κ), MR-04 (φ avant τ_D) et MR-05
        (plus grand φ) du réviseur, au site d'appel de C1."""
        f, prm = Fraction, dict(PRM, calibration=dict(K_, ell=[1, 2, 240]))
        g = calib_fiv.grille(prm)
        moy = {p: m(1, 2, 8) for p in [None] + g}
        for gagnant, perdant in (((f(1, 100), f(5), 4320), (f(1, 100), f(50), 60)),
                                 ((f(1, 10), f(5), 60), (f(1, 100), f(5), 240)),
                                 ((f(1, 100), f(20), 240), (f(1, 20), f(20), 240))):
            u = {p: {"calme": {"a": m(1, 2, 4) if p in (gagnant, perdant) else m(1, 4, 4), "b": m(1, 3, 9),
                               "c": m(1, 1, 1)}} for p in g}
            s = choisir(prm, cible3(), moy, moyennes_u=u)["calme"]
            self.assertEqual((len(g), s["C1"], s["Q1"][gagnant], s["Q1"][perdant]), (64, gagnant, 0, 0), perdant)

    def test_q1_dernier_hote_du_format(self):
        """C-2 de la G2 de SIM-INTEG : Q₁ sur les dix hôtes du format, dans son ordre (okx en dernier), F_u = 1, 2, 4
        aux ℓ 1, 2, 240 (gardes à 1 et 2) ; modèle égal à F_u, sauf pour un hôte, 16 fois F_u à ℓ = 2 : Q₁ = (ln 16)²
        = 16·(ln 2)² (bc -l, à 10^-45 près), que l'hôte soit le dernier ou le premier du format. Mutation MR-06 du
        réviseur (dernier hôte ignoré)."""
        ctx, hotes = calib_fiv.contexte(K_), [h for h, _f in K_["unites"]]
        ref = Decimal("7.687248222691222794673640421226639547688847225512729389869826")      # bc -l : 16*l(2)^2
        cible = {h: fu(1, 2, 4) for h in hotes}
        self.assertEqual((len(hotes), hotes[-1]), (10, "okx"))
        for h in (hotes[-1], hotes[0]):
            moy = {x: m(1, 32 if x == h else 2, 4) for x in hotes}
            self.assertLess(abs(calib_fiv.q1(moy, cible, [1, 2, 240], ctx) - ref), EPS, h)


HOTES = [h for h, _f in K_["unites"]]                                  # les dix hôtes du format
P0 = (Fraction(1, 100), Fraction(5), 60)                                  # aucune coordonnée extrême de la grille


def cible_bord(gardes=(True, True, True, False)):
    """F_u = 1, 4, 8, 16 aux ℓ 1, 60, 240, 1 440 pour les dix hôtes ; garde tenue sauf à 1 440 par défaut."""
    return {h: [{"ell": e, "fiv": Fraction(x), "garde": g}
                for e, x, g in zip((1, 60, 240, 1440), (1, 4, 8, 16), gardes)] for h in HOTES}


def modele_bord(n_bas, **autres):
    """Moyennes de C1 : les n_bas premiers hôtes sous la cible à ℓ = 60 et 240 (2, 4 ; au-dessus à 1 440 : 32), les
    autres au-dessus (8, 16) ; ℓ = 1 égal à la cible ; autres : {hôte : FIV par ℓ} imposés."""
    return {h: m(*autres.get(h, (1, 2, 4, 32) if j < n_bas else (1, 8, 16, 32))) for j, h in enumerate(HOTES)}


class TestBordE1(unittest.TestCase):
    PRM_B = dict(PRM, calibration=dict(K_, ell=[1, 60, 240, 1440]))         # grille scellée : 1/10, 50, 4 320

    def constat(self, point, moy, cible=None):
        return calib_fiv.bord(self.PRM_B, point, moy, cible or cible_bord(), calib_fiv.contexte(K_))

    def test_parametres_bord(self):
        """Point (8) : e1.bord = {ell : 60, hotes : 6}, source citant le point (8) et sa précision. Mutations M-15F-01
        (seuil 5), M-15F-02 (ℓ minimal 30)."""
        b = PRM["e1"]["bord"]
        self.assertEqual((b["ell"], b["hotes"]), (60, 6))
        self.assertTrue(all(x in b["source"] for x in ("point (8)", "précision d'adjudication", "six des dix")))

    def test_bord_par_les_residus(self):
        """Seconde condition, précision d'adjudication : C1 sans coordonnée extrême ; ℓ retenus ≥ 60 : 60 et 240 (1 440
        non gardé, 1 hors du seuil) ; 6 hôtes négatifs à 60 et à 240 : au bord ; 5 : non ; 6 dont un négatif à 60
        seulement (2, 16), un négatif à 240 seulement (8, 4), un nul à 60 (4, 4) : 5 chaque fois, non au bord.
        Mutations M-15F-03 (au moins un ℓ au lieu de chacun), M-15F-04 (ℓ > 60), M-15F-05 (résidu ≤ 0), M-15F-06
        (garde ignorée : 1 440 compté), M-15F-07 (ℓ < 60 comptés), M-15F-08 (seuil strict)."""
        b = self.constat(P0, modele_bord(6))
        self.assertEqual((b["extremes"], b["ells"], b["hotes"], b["sur"], b["au_bord"]), ([], [60, 240], 6, 10, True))
        self.assertEqual((self.constat(P0, modele_bord(5))["hotes"], self.constat(P0, modele_bord(5))["au_bord"]),
                         (5, False))
        for x in ((1, 2, 16, 32), (1, 8, 4, 32), (1, 4, 4, 32)):
            b = self.constat(P0, modele_bord(6, **{HOTES[0]: x}))
            self.assertEqual((b["hotes"], b["au_bord"]), (5, False), x)

    def test_bord_par_les_coordonnees(self):
        """Première condition : φ = 1/10 ; κ = 50 et τ_D = 4 320 : au bord sans hôte négatif ; plus petites valeurs de
        la grille (1/100, 5, 60) : non. Mutations M-15F-09 (extrêmes au minimum), M-15F-10 (« et » au lieu de
        « ou »)."""
        for point, ext in (((Fraction(1, 10), Fraction(5), 60), [("φ", Fraction(1, 10))]),
                           ((Fraction(1, 100), Fraction(50), 4320), [("κ", 50), ("τ_D", 4320)]), (P0, [])):
            b = self.constat(point, modele_bord(0))
            self.assertEqual((b["extremes"], b["hotes"], b["au_bord"]), (ext, 0, bool(ext)))

    def test_bord_sans_vacuite(self):
        """Aucun ℓ ≥ 60 gardé : liste vide, aucun hôte ne satisfait la condition (pas de vérité vide : Q-SI-1) ; hôte à
        F_u indéfini parmi les six négatifs : non compté (Q-SI-2). Mutations M-15F-11 (condition vide tenue),
        M-15F-12 (F_u indéfini compté)."""
        b = self.constat(P0, modele_bord(10), cible_bord((True, False, False, False)))
        self.assertEqual((b["ells"], b["hotes"], b["au_bord"]), ([], 0, False))
        c = cible_bord()
        c[HOTES[0]] = [dict(x, fiv=None) for x in c[HOTES[0]]]
        self.assertEqual(self.constat(P0, modele_bord(6), c)["hotes"], 5)

    def test_ligne_bord(self):
        """(8)(iv) : ligne nommée, écrite à la main. Mutation M-15F-13 (verdict inversé)."""
        b = self.constat((Fraction(1, 10), Fraction(50), 60), modele_bord(6))
        self.assertEqual(calib_fiv.ligne_bord("calme", b),
                         "[BORD E1] « calme » : C1 = (φ = 1/10, κ = 50, τ_D = 60) ; coordonnées extrêmes : φ = 1/10, "
                         "κ = 50 ; ℓ retenus ≥ 60 : 60, 240 ; hôtes à résidu négatif à chacun de ces ℓ : 6 sur 10 "
                         "(seuil 6) ; au bord : OUI")
        b = self.constat(P0, modele_bord(1), cible_bord((True, False, False, False)))
        self.assertEqual(calib_fiv.ligne_bord("stress", b),
                         "[BORD E1] « stress » : C1 = (φ = 1/100, κ = 5, τ_D = 60) ; coordonnées extrêmes : aucune ; "
                         "ℓ retenus ≥ 60 : aucun ; hôtes à résidu négatif à chacun de ces ℓ : 0 sur 10 (seuil 6) ; au "
                         "bord : NON")

    def test_bord_dans_selection(self):
        """(8)(i) : selection rend le constat du point C1 (non de C2), C1 inchangé même au bord (grille réduite : τ_D =
        60 extrême) ; aucune seconde sélection. Mutations M-15F-14 (bord de C2), M-15F-15 (C1 remplacé au bord)."""
        u = par_hote(P1={"a": m(1, 4, 4)}, P3={"b": m(1, None, 9)}, P4={"a": m(2, 2, 4)})
        s = choisir(reduit(), cible3(), {p: m(1, 2, 8) for p in (None, P1, P2, P3, P4)}, moyennes_u=u)["calme"]
        self.assertEqual((s["C2"], s["C1"], s["bord"]["C1"], s["bord"]["extremes"], s["bord"]["au_bord"]),
                         (P1, P2, P2, [("κ", 50), ("τ_D", 60)], True))

    def test_bord_derniers_hotes_du_format(self):
        """C-2 de la G2 de SIM-INTEG : les six hôtes négatifs à 60 et à 240 sont les six derniers du format (okx
        compris), les quatre premiers au-dessus : 6 sur 10, au bord ; okx remis au-dessus : 5, non. Mutation MR-26 du
        réviseur (dernier hôte ignoré)."""
        bas = {h: (1, 2, 4, 32) for h in HOTES[4:]}
        b = self.constat(P0, modele_bord(0, **bas))
        self.assertEqual((HOTES[-1], b["hotes"], b["sur"], b["au_bord"]), ("okx", 6, 10, True))
        b = self.constat(P0, modele_bord(0, **dict(bas, okx=(1, 8, 16, 32))))
        self.assertEqual((b["hotes"], b["au_bord"]), (5, False))

    def test_bord_selection_grille_scellee(self):
        """C-3 de la G2 de SIM-INTEG : selection sur la grille scellée (64 points), ℓ 1, 60 et 240 tous gardés, dix
        hôtes à F_u = 1, 4, 8 ; C2 = (1/10, 5, 60), seul point de critère nul ; C1 = (1/50, 10, 240), six hôtes à
        moitié de F_u à 60 et à 240 (Q₁ = 12·(ln 2)²), tous les autres points à quatre fois F_u pour les dix hôtes
        (Q₁ = 80·(ln 2)²) : constat de C1, sans coordonnée extrême, 6 hôtes, au bord ; avec les moyennes de C2 (quatre
        fois F_u) il ne le serait pas. Mutation MR-10 du réviseur (moyennes de C2 sous l'étiquette C1)."""
        f, prm = Fraction, dict(PRM, calibration=dict(K_, ell=[1, 60, 240]))
        g, c1, c2 = calib_fiv.grille(prm), (f(1, 50), f(10), 240), (f(1, 10), f(5), 60)
        cible = [{"ell": e, "fiv": f(x), "garde": True} for e, x in ((1, 1), (60, 4), (240, 8))]
        unites = {"calme": {h: [dict(c) for c in cible] for h in HOTES}}
        moy = {p: m(1, 4, 8) if p == c2 else m(1, 16, 32) for p in [None] + g}
        u = {p: {"calme": {h: m(1, 2, 4) if p == c1 and h in HOTES[2:8] else m(1, 4, 8) if p == c1 else
                           m(1, 16, 32) for h in HOTES}} for p in g}
        s = choisir(prm, cible, moy, unites, u)["calme"]
        b = s["bord"]
        self.assertEqual((s["C2"], s["C1"], b["C1"], b["extremes"], b["ells"], b["hotes"], b["au_bord"]),
                         (c2, c1, c1, [], [60, 240], 6, True))


if __name__ == "__main__":
    unittest.main()
